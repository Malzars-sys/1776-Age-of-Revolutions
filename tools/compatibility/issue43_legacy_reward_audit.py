"""Read-only legacy-reward checks for issue 43; controls stay in memory.

Candidate mode overlays only this task's three evidence files. No runtime,
Git or previous-result write is performed; output must be a new evidence JSON.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, walk, plain

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE43_LEGACY_COMMUNIST_REWARD_2026_11_09'
KEY = 'institutions_of_socialism_modifier'
MODIFIER = 'common/static_modifiers/1776_legacy_communist_reward.txt'
LOCS = {lang: f'localization/{lang}/1776_legacy_communist_reward_l_{lang}.yml'
        for lang in ('english', 'french')}
FILES = [MODIFIER, *LOCS.values()]


def payload(nodes):
    return [(n.key, n.op, payload(n.value) if isinstance(n.value, list) else n.value) for n in nodes]


def reference_scan(audit, modifiers):
    references, missing = 0, []
    for folder in ('events', 'common/scripted_effects', 'common/scripted_buttons', 'common/on_actions'):
        for path in audit.paths(folder):
            nodes, raw, source = audit.read(path)
            for node in walk(nodes):
                if node.key not in ('add_modifier', 'remove_modifier', 'has_modifier'):
                    continue
                target = plain(node.one('name')) if isinstance(node.value, list) else plain(node.value)
                if not target or '$' in target or ':' in target:
                    continue
                references += 1
                if target not in modifiers:
                    missing.append({'target': target, 'operation': node.key, 'source': source,
                                    'line': raw.count('\n', 0, node.start) + 1})
    return {'references': references, 'missing': missing, 'parse_errors': audit.errors,
            'limits': 'Literal modifier IDs in four script families; no reachability or engine simulation.'}


def validate(modifiers, data, event_data, localizations, legacy, type_registered, icon_exists):
    checks = []

    def check(name, value):
        checks.append({'name': name, 'pass': bool(value)})

    entries = modifiers.get(KEY, [])
    check('provider_present_and_unique', len(entries) == 1)
    nodes = parse(data[MODIFIER].decode('utf-8-sig'))
    check('one_legacy_modifier_only', len(nodes) == 1 and nodes[0].key == KEY)
    check('exact_historical_modifier_payload', payload(nodes) == payload(parse(legacy['modifier']['text'])))
    check('bureaucracy_field_registered', type_registered)
    check('icon_resolves', icon_exists)
    current = [n for n in parse(event_data.decode('utf-8-sig')) if n.key == 'communism.6']
    check('existing_event_matches_historical_reward', payload(current) == payload(parse(legacy['event']['text'])))
    if len(current) == 1:
        options = [n for n in current[0].children('option') if plain(n.one('name')) == 'communism.6.a']
        blocks = options[0].children('add_modifier') if len(options) == 1 else []
        check('existing_country_event_scope', plain(current[0].one('type')) == 'country_event')
        check('existing_reward_call_and_duration', len(blocks) == 1 and plain(blocks[0].one('name')) == KEY
              and plain(blocks[0].one('days')) == 'long_modifier_time')
    else:
        check('existing_event_unique', False)
    for lang, path in LOCS.items():
        raw = data[path]
        check(lang + '.bom_and_header', raw.startswith(b'\xef\xbb\xbf')
              and raw.decode('utf-8-sig').splitlines()[0] == 'l_' + lang + ':')
        expected = re.search(r'"(.+)"', legacy['localization'][lang]['lines'][0]).group(1)
        rows = localizations[lang]
        check(lang + '.unique_historical_name', len(rows) == 1 and rows[0]['text'] == expected)
        declared = re.findall(r'^\s*([A-Za-z0-9_]+):\d*\s+"', raw.decode('utf-8-sig'), re.MULTILINE)
        check(lang + '.one_consumed_key_only', declared == [KEY])
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new output path in the issue 43 evidence directory.')
    legacy = json.loads((EVIDENCE / 'LEGACY_PROVENANCE.json').read_text(encoding='utf-8'))
    base = EVIDENCE / 'candidate' if args.candidate else ROOT
    data = {path: (base / path).read_bytes() for path in FILES}
    event_data = (ROOT / 'events/communism.txt').read_bytes()
    audit = Audit(ROOT, GAME)
    modifiers = audit.load('modifiers', 'common/static_modifiers')
    if args.candidate:
        for node in parse(data[MODIFIER].decode('utf-8-sig')):
            modifiers.setdefault(node.key, []).append((node, 'candidate/' + MODIFIER, ''))
    types = audit.load('modifier_types', 'common/modifier_type_definitions')
    icon = plain(parse(legacy['modifier']['text'])[0].one('icon'))
    localizations = {}
    localization_hashes = {}
    for lang in LOCS:
        local = {p.relative_to(ROOT).as_posix().casefold(): p
                 for p in (ROOT / 'localization' / lang).rglob('*.yml')}
        effective = [p for p in (GAME / 'localization' / lang).rglob('*.yml')
                     if p.relative_to(GAME).as_posix().casefold() not in local] + list(local.values())
        rows = []
        for path in effective:
            raw = path.read_bytes()
            for match in re.finditer(r'^\s*' + KEY + r':\d*\s+"(.+)"', raw.decode('utf-8-sig'), re.MULTILINE):
                rows.append({'source': str(path), 'text': match.group(1)})
                localization_hashes[str(path)] = hashlib.sha256(raw).hexdigest()
        if args.candidate:
            raw = data[LOCS[lang]].decode('utf-8-sig')
            rows += [{'source': 'candidate/' + LOCS[lang], 'text': m.group(1)}
                     for m in re.finditer(r'^\s*' + KEY + r':\d*\s+"(.+)"', raw, re.MULTILINE)]
        localizations[lang] = rows
    arguments = [modifiers, data, event_data, localizations, legacy,
                 'country_bureaucracy_mult' in types, (ROOT / icon).exists() or (GAME / icon).exists()]
    checks = validate(*arguments)
    frozen = (EVIDENCE / 'before/events/communism.txt').read_bytes()
    checks.append({'name': 'event_bytes_preserved', 'pass': frozen == event_data})
    controls = []
    if args.controls:
        variants = []
        missing = copy.copy(modifiers)
        missing.pop(KEY, None)
        variants.append(('missing_provider', [missing, *arguments[1:]]))
        duplicate = copy.copy(modifiers)
        duplicate[KEY] = modifiers[KEY] * 2
        variants.append(('duplicate_provider', [duplicate, *arguments[1:]]))
        wrong_bonus = dict(data)
        wrong_bonus[MODIFIER] = data[MODIFIER].replace(b'= 0.2', b'= 2.0')
        variants.append(('wrong_bonus', [modifiers, wrong_bonus, *arguments[2:]]))
        missing_text = copy.deepcopy(localizations)
        missing_text['french'] = []
        variants.append(('missing_french_name', [*arguments[:3], missing_text, *arguments[4:]]))
        wrong_event = event_data.replace(b'name = institutions_of_socialism_modifier\r\n\t\t\tdays = long_modifier_time',
                                        b'name = institutions_of_socialism_modifier\r\n\t\t\tdays = very_long_modifier_time')
        variants.append(('changed_event_duration', [*arguments[:2], wrong_event, *arguments[3:]]))
        for name, args_bad in variants:
            failed = [r['name'] for r in validate(*args_bad) if not r['pass']]
            controls.append({'name': name, 'detected_by': failed, 'pass': bool(failed)})
    references = reference_scan(audit, modifiers)
    checks.append({'name': 'literal_modifier_references_resolve',
                   'pass': not references['missing'] and not references['parse_errors']})
    result = {'status': 'PASS_STATIC_ONLY' if all(r['pass'] for r in checks + controls) else 'FAIL_STATIC',
              'candidate': args.candidate, 'checks': checks, 'controls': controls,
              'references': references, 'localization': localizations,
              'source_hashes': audit.hashes, 'localization_source_hashes': localization_hashes,
              'delivery_hashes': {path: hashlib.sha256(raw).hexdigest() for path, raw in data.items()},
              'engine_tested': False}
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'checks': [sum(r['pass'] for r in checks), len(checks)],
                      'controls': [sum(r['pass'] for r in controls), len(controls)],
                      'missing': references['missing'], 'references': references['references']}))
    return 0 if result['status'] == 'PASS_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
