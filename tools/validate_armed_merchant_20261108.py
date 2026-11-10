"""Read-only ship-designer contract for the armed merchant rework.

Checks live data, native modifier identifiers, design choices, progression,
startup compatibility, art references and comparative roles. No engine claims.
"""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

SHIP = 'common/ship_types/1776_usa_armed_merchantman.txt'
MODS = 'common/ship_modifications/1776_usa_armed_merchantman.txt'
KEY = 'ship_type_aor1776_armed_merchantman'
REPORT = ROOT / 'docs/reports/naval/ARMED_MERCHANT_REWORK_2026_11_08'


def read(path):
    return path.read_bytes().decode('utf-8-sig')


def bare(node):
    return [n.value.strip('"') for n in node.children()
            if not n.key and isinstance(n.value, str)]


def catalog(folder, native=False):
    files = {p.relative_to(GAME).as_posix(): p
             for p in (GAME / folder).rglob('*.txt')}
    if not native:
        files.update({p.relative_to(ROOT).as_posix(): p
                      for p in (ROOT / folder).rglob('*.txt')})
        if folder.startswith('common/technology/technologies'):
            files = {k: v for k, v in files.items() if v.is_relative_to(ROOT)}
    result = {}
    for path in files.values():
        for node in parse(read(path)):
            if isinstance(node.value, list):
                result[node.key.split(':')[-1]] = node
    return result


def stats(node):
    block = node.children('modifier')
    return {n.key: float(n.value) for n in block[0].children()} if block else {}


def audit(ship_text=None, mods_text=None):
    checks = []

    def check(name, condition):
        checks.append({'check': name, 'passed': bool(condition)})

    try:
        ship = parse(ship_text if ship_text is not None else read(ROOT / SHIP))[0]
        nodes = parse(mods_text if mods_text is not None else read(ROOT / MODS))
        check('syntax', True)
    except (ValueError, IndexError) as error:
        return {'status': 'FAIL_STATIC', 'checks': [], 'errors': [str(error)]}
    mods = {n.key: n for n in nodes}
    techs = catalog('common/technology/technologies')
    goods = catalog('common/goods')
    modifier_types = catalog('common/modifier_type_definitions', native=True)
    categories = catalog('common/ai_ship_categories', native=True)
    slots = catalog('common/ship_modification_slots', native=True)
    check('ship.identity', ship.key == KEY)
    check('ship.escort_group', ship.one('ship_group') == 'ship_group_cruisers')
    check('ship.valid_ai_category', ship.one('ai_ship_category') in categories)
    check('ship.escort_ai', ship.one('ai_ship_category') == 'ai_ship_category_screens')
    check('ship.designer_enabled', ship.one('use_modifications') == 'yes')
    check('equipment.unique_ids', len(mods) == len(nodes) == 15)
    check('startup.five_original_module_ids',
          all('aor1776_merchant_' + str(n) in mods for n in range(1, 6)))

    choices = ship.children('modifications')[0].children()
    defaults = {n.key: n.value for n in ship.children('default_modifications')[0].children()}
    for group in choices:
        identifiers = bare(group)
        check(group.key + '.slot_exists', group.key in slots)
        check(group.key + '.three_distinct_choices', len(set(identifiers)) == len(identifiers) == 3)
        eras = []
        for key in identifiers:
            check(key + '.exists', key in mods)
            if key not in mods:
                continue
            mod = mods[key]
            check(key + '.slot_matches', mod.one('type') == group.key)
            gates = bare(mod.children('unlocking_technologies')[0])
            check(key + '.one_gate', len(gates) == 1)
            check(key + '.gate_exists', all(t in techs for t in gates))
            if len(gates) == 1 and gates[0] in techs:
                eras.append(int(techs[gates[0]].one('era').split('_')[-1]))
        check(group.key + '.progresses_across_eras', len(eras) == 3 and eras[0] < eras[1] < eras[2])
        check(group.key + '.bronze_default', defaults.get(group.key) == identifiers[0])
    check('slots.all_four_required_present',
          {'ship_mod_slot_' + n for n in ['armor', 'guns', 'propulsion', 'range']}
          <= {n.key for n in choices})

    for node in [ship] + list(mods.values()):
        for key in stats(node):
            check(node.key + '.' + key + '.native_modifier', key in modifier_types)
            check(node.key + '.' + key + '.ship_scope', key.startswith('ship_'))
        for block in node.children('construction_goods') + node.children('materiel_goods'):
            for field in block.children():
                good = field.key.removeprefix('goods_input_').removesuffix('_add')
                check(node.key + '.' + good + '.good_exists', good in goods)
                check(node.key + '.' + good + '.positive_cost', float(field.value) > 0)
        for field in ['icon', 'profile_texture']:
            value = node.one(field)
            if value:
                rel = value.strip('"')
                check(node.key + '.' + field + '.file_exists',
                      (ROOT / rel).is_file() or (GAME / rel).is_file())

    caravel = catalog('common/ship_types')['ship_type_caravel']
    caravel_mods = catalog('common/ship_modifications')
    caravel_choices = caravel.children('modifications')[0].children()
    merchant_stats, caravel_stats = stats(ship), stats(caravel)
    totals = []
    for tier in range(3):
        def summed(base, groups, objects):
            result = dict(base)
            for group in groups:
                if 'utility' in group.key:
                    continue
                for key, value in stats(objects[bare(group)[tier]]).items():
                    result[key] = result.get(key, 0) + value
            return result
        merchant = summed(merchant_stats, choices, mods)
        warship = summed(caravel_stats, caravel_choices, caravel_mods)
        check('tier_' + str(tier) + '.less_hull_damage_than_caravel', merchant['ship_hull_damage_add'] < warship['ship_hull_damage_add'])
        check('tier_' + str(tier) + '.less_crew_damage_than_caravel', merchant['ship_crew_damage_add'] < warship['ship_crew_damage_add'])
        check('tier_' + str(tier) + '.more_transport_than_caravel', merchant['ship_carrying_capacity_add'] > warship['ship_carrying_capacity_add'])
        check('tier_' + str(tier) + '.more_provisions_than_caravel', merchant['ship_supply_capacity_add'] > warship['ship_supply_capacity_add'])
        totals.append({'tier': ['bronze', 'silver', 'gold'][tier], 'merchant_without_optional_escort': merchant, 'caravel_without_optional_utility': warship})

    own_keys = set(mods) | {KEY, KEY + '_desc'}
    for language in ['french', 'english']:
        occurrences = collections.Counter()
        for path in (ROOT / 'localization' / language).rglob('*.yml'):
            for key in re.findall(r'^\s*([\w.]+):(?:\d+)?\s*"', read(path), re.M):
                if key in own_keys:
                    occurrences[key] += 1
        for key in own_keys:
            check(language + '.' + key + '.one_localisation', occurrences[key] == 1)

    graphical = ROOT / 'gfx/map/fleet_entities/1776_usa_armed_merchantman.txt'
    check('graphics.type_mapping_present', graphical.is_file() and KEY in read(graphical))
    if graphical.exists():
        visual = parse(read(graphical))[0]
        check('graphics.complete_native_sailing_entity', visual.one('entity').strip('"') == 'sail_transport_ship_01_entity')
    protected = json.loads(read(REPORT / 'BEFORE.json'))
    for path in ['common/ship_types/10_1776_early_ships.txt',
                 'common/ship_modifications/10_1776_early_equipment.txt',
                 'common/technology/technologies/25_tech3a_naval.txt']:
        raw = (ROOT / path).read_bytes()
        unchanged = hashlib.sha256(raw).hexdigest() == protected[path]
        concurrent_receipt = REPORT / 'CONCURRENT_CHANGE.json'
        if not unchanged and concurrent_receipt.exists():
            receipt = json.loads(read(concurrent_receipt))
            # A separately reviewed, exact identifier-only migration by the
            # concurrent compatibility task; never waive other byte changes.
            if path == receipt['path']:
                old = (receipt['previous_identifier'] + ' = {').encode()
                new = (receipt['current_identifier'] + ' = {').encode()
                unchanged = (raw.count(new) == 1
                             and hashlib.sha256(raw).hexdigest() == receipt['current_sha256']
                             and hashlib.sha256(raw.replace(new, old, 1)).hexdigest() == protected[path])
        check(path + '.preserved_or_exact_documented_concurrent_rename', unchanged)
    failed = [c for c in checks if not c['passed']]
    return {'status': 'FAIL_STATIC' if failed else 'PASS_STATIC_ONLY',
            'passed': len(checks) - len(failed), 'total': len(checks),
            'errors': failed, 'checks': checks, 'totals': totals,
            'engine_tested': False, 'human_runtime_validated': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    result = audit()
    if args.negative_controls:
        base = read(ROOT / MODS)
        result['negative_controls'] = [
            {'case': 'undefined_gate', 'detected': audit(mods_text=base.replace('organized_workshops', 'invalid_merchant_gate', 1))['status'] == 'FAIL_STATIC'},
            {'case': 'invalid_modifier', 'detected': audit(mods_text=base.replace('ship_hit_points_max_add', 'ship_invalid_merchant_modifier_add', 1))['status'] == 'FAIL_STATIC'},
            {'case': 'wrong_slot', 'detected': audit(mods_text=base.replace('type = ship_mod_slot_armor', 'type = ship_mod_slot_guns', 1))['status'] == 'FAIL_STATIC'}]
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['status', 'passed', 'total', 'errors']}, ensure_ascii=False))
    if args.negative_controls:
        print(json.dumps(result['negative_controls']))
    return int(result['status'] != 'PASS_STATIC_ONLY' or any(not r['detected'] for r in result.get('negative_controls', [])))


if __name__ == '__main__':
    sys.exit(main())
