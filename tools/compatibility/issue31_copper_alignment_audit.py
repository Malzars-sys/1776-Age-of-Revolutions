"""Read-only native copper alignment audit, with optional staged candidates.

Resource distribution and custom non-native extensions must remain unchanged.
Static resolution is a model of file masking, not an engine test receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE31_COPPER_NATIVE_ALIGNMENT_2026_11_08'
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

GROUPS = ['pmg_' + s + '_building_copper_mine' for s in ('mining_equipment', 'explosives', 'steam_automation', 'train_automation')]
METHODS = ['pm_' + s + '_building_copper_mine' for s in ('picks_and_shovels', 'atmospheric_engine_pump', 'condensing_engine_pump', 'diesel_pump', 'nitroglycerin', 'dynamite')]
GOOD = 'common/goods/13_tech6c5b_copper.txt'
PMGS = 'common/production_method_groups/13_tech6c5b_copper_pmgs.txt'
PMS = 'common/production_methods/13_tech6c5b_copper_production_and_consumers.txt'
BUILDING = 'common/buildings/13_tech6c5b_copper_mine.txt'
REGISTRY = 'common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt'
ICON = 'gui/tech6c_goods_texticons.gui'
REGISTRATIONS = {'goods_input_copper_add', 'goods_output_copper_add', 'building_copper_mine_throughput_add'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sig(nodes):
    return [(n.key, n.op, sig(n.value) if isinstance(n.value, list) else n.value) for n in nodes]


def audit(candidate=False, replacements=None, protected=True):
    replacements = replacements or {}
    checks, errors = [], []

    def check(name, ok):
        checks.append(name)
        if not ok:
            errors.append(name)

    def read(rel):
        if rel in replacements:
            return replacements[rel]
        staged = LOT / 'candidate' / rel
        return (staged if candidate and staged.exists() else ROOT / rel).read_bytes().decode('utf-8-sig')

    def native(rel):
        return (GAME / rel).read_bytes().decode('utf-8-sig')

    def before(rel):
        return (LOT / 'before' / rel).read_bytes().decode('utf-8-sig')

    def effective(folder, base_only=False):
        local = {} if base_only else {p.name.casefold(): p for p in (ROOT / folder).glob('*.txt')}
        paths = [p for p in (GAME / folder).glob('*.txt') if p.name.casefold() not in local] + list(local.values())
        normal, explicit = {}, {}
        for p in sorted(paths):
            text = native(p.relative_to(GAME).as_posix()) if p.is_relative_to(GAME) else read(p.relative_to(ROOT).as_posix())
            for n in parse(text):
                directive, sep, name = n.key.partition(':')
                key = name if sep and directive in ('REPLACE', 'REPLACE_OR_CREATE') else n.key
                (explicit if key != n.key else normal).setdefault(key, []).append((p, n))
        normal.update(explicit)
        return normal

    def unique(objects, key):
        found = objects.get(key, [])
        check('unique effective ID: ' + key, len(found) == 1)
        return found[0] if len(found) == 1 else (None, None)

    manifest = json.loads((LOT / 'BASELINE.json').read_text(encoding='utf-8'))
    for rel, sha in manifest['native'].items():
        check('canonical input unchanged: ' + rel, digest((GAME / rel).read_bytes()) == sha)

    goods = effective('common/goods')
    path, copper = unique(goods, 'copper')
    check('copper inherits canonical goods file', path == GAME / 'common/goods/00_goods.txt')
    if copper:
        check('native base price 40, prestige 3, traded quantity 5', copper.one('cost') == '40' and copper.one('prestige_factor') == '3' and copper.one('traded_quantity') == '5')
    check('no local copper good declaration', not parse(read(GOOD)))

    groups = effective('common/production_method_groups')
    for key in GROUPS:
        path, group = unique(groups, key)
        check('native group provider: ' + key, path == GAME / 'common/production_method_groups/03_mines.txt')
        if group:
            ref = next(n for n in parse(native('common/production_method_groups/03_mines.txt')) if n.key == key)
            check('native group payload: ' + key, sig(group.children()) == sig(ref.children()))
    check('custom groups preserved', sig(parse(read(PMGS))) == sig([n for n in parse(before(PMGS)) if n.key not in GROUPS]))

    methods = effective('common/production_methods')
    references = effective('common/production_methods', base_only=True)
    for key in GROUPS:
        _, group = unique(groups, key)
        if group:
            for block in group.children('production_methods'):
                for entry in block.children():
                    if isinstance(entry.value, str):
                        unique(methods, entry.value.strip('"'))
    for key in METHODS:
        _, pm = unique(methods, key)
        _, ref = unique(references, key)
        if pm and ref:
            expected = json.dumps(sig(ref.children())).replace('watertube_boiler', 'condensing_steam_engines')
            check('native mining payload with 1776 tech mapping: ' + key, json.dumps(sig(pm.children())) == expected)
            for n in walk(pm.children()):
                if n.key.startswith('goods_input_') and n.key.endswith('_add'):
                    check('resolved mining input: ' + key + ':' + n.key, n.key[12:-4] in goods)
    check('custom ore, sheathing and other consumers preserved', sig([n for n in parse(read(PMS)) if n.key not in METHODS]) == sig([n for n in parse(before(PMS)) if n.key not in METHODS]))
    consumer_count = 0
    for key, definitions in references.items():
        if len(definitions) != 1:
            continue
        node = definitions[0][1]
        inputs = [n.value for b in node.children('building_modifiers') for w in b.children('workforce_scaled') for n in w.children('goods_input_copper_add')]
        if inputs:
            _, current = unique(methods, key)
            values = [n.value for b in current.children('building_modifiers') for w in b.children('workforce_scaled') for n in w.children('goods_input_copper_add')] if current else []
            check('native consumer copper coefficient: ' + key, values == inputs)
            consumer_count += 1
    check('all 28 native consumers inventoried', consumer_count == 28)

    building = parse(read(BUILDING))[0]
    ref = next(n for n in parse(native('common/buildings/03_mines.txt')) if n.key == 'building_copper_mine')
    check('native standard building fields, no custom AI bias', sig([n for n in building.children() if n.key != 'production_method_groups']) == sig([n for n in ref.children() if n.key != 'production_method_groups']))
    check('1776 custom building groups preserved', sig(building.children('production_method_groups')) == sig(parse(before(BUILDING))[0].children('production_method_groups')))
    registry = parse(read(REGISTRY))
    check('non-duplicate registry extensions preserved', sig(registry) == sig([n for n in parse(before(REGISTRY)) if n.key not in REGISTRATIONS]))
    registered = effective('common/modifier_type_definitions')
    for key in REGISTRATIONS:
        path, _ = unique(registered, key)
        check('native modifier provider: ' + key, path == GAME / 'common/modifier_type_definitions/01_building_modifier_types.txt')

    is_copper = lambda n: n.key == 'texticon' and n.one('icon') == 'copper'
    check('native copper texticon replaces local placeholder', not any(is_copper(n) for n in parse(read(ICON))) and sum(is_copper(n) for n in parse(native('gui/goods_texticons.gui'))) == 1 and not (ROOT / 'gui/goods_texticons.gui').exists())
    check('all other texticons preserved', sig(parse(read(ICON))) == sig([n for n in parse(before(ICON)) if not is_copper(n)]))
    removals = json.loads((LOT / 'LOCALIZATION_REMOVALS.json').read_text(encoding='utf-8'))
    for rel, keys in removals.items():
        text = read(rel)
        filtered = ''.join(line for line in before(rel).splitlines(True) if not re.match(r'^\s*(' + '|'.join(map(re.escape, keys)) + r'):\d*\s+', line))
        check('only native-colliding localization removed: ' + rel, text == filtered)
        check('no reintroduced native localization: ' + rel, not any(re.search(r'^\s*' + re.escape(key) + r':', text, re.M) for key in keys))
        check('localization BOM: ' + rel, (LOT / 'candidate' / rel if candidate else ROOT / rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    concurrent = []
    if protected:
        for rel, sha in manifest['protected'].items():
            p = ROOT / rel
            if not p.exists() or digest(p.read_bytes()) != sha:
                concurrent.append(rel)
    return {'status': 'PASS_STATIC_ONLY' if not errors else 'FAIL_STATIC', 'checks': len(checks),
            'passed': len(checks) - len(errors), 'errors': errors, 'native_consumers': consumer_count,
            'protected_files_checked': len(manifest['protected']) if protected else 0,
            'concurrent_changes': concurrent, 'runtime_tested': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--candidate', action='store_true')
    ap.add_argument('--negative-controls', action='store_true')
    args = ap.parse_args()
    result = audit(args.candidate)
    if args.negative_controls:
        get = lambda rel: (LOT / 'candidate' / rel if args.candidate else ROOT / rel).read_bytes().decode('utf-8-sig')
        mutations = {
            'duplicate copper good and old price': {GOOD: (LOT / 'before' / GOOD).read_bytes().decode('utf-8-sig')},
            'duplicate standard mining groups': {PMGS: (LOT / 'before' / PMGS).read_bytes().decode('utf-8-sig')},
            'lowered basic mine output': {PMS: get(PMS).replace('goods_output_copper_add = 20', 'goods_output_copper_add = 15', 1)},
            'wrong diesel fuel': {PMS: get(PMS).replace('goods_input_oil_add = 5', 'goods_input_refined_fuels_add = 3', 1)},
            'local deer texticon restored': {ICON: (LOT / 'before' / ICON).read_bytes().decode('utf-8-sig')},
            'duplicate native localization restored': {'localization/english/tech6c5b_copper_l_english.yml': get('localization/english/tech6c5b_copper_l_english.yml') + '\n copper:0 "Copper"\n'},
        }
        result['negative_controls'] = {}
        for label, replacements in mutations.items():
            try:
                detected = bool(audit(args.candidate, replacements, protected=False)['errors'])
            except (ValueError, KeyError, IndexError):
                detected = True
            result['negative_controls'][label] = detected
        if not all(result['negative_controls'].values()):
            result['errors'].append('Undetected negative control')
            result['status'] = 'FAIL_STATIC'
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result['errors'])


if __name__ == '__main__':
    raise SystemExit(main())
