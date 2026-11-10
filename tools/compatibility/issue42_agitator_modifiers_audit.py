"""Read-only two-reference validator for issue 42; controls stay in memory.

The only output is one new JSON in the task evidence directory. No installer,
runtime write, Git operation or modification of older evidence is provided.
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

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE42_AGITATOR_MODIFIERS_2026_11_09'
SOURCE = 'events/agitators_events/agitator_law_events_2.txt'
TARGETS = [('agitator_legal_events.5', 'agitator_legal_events.5.a', 'scope:opposing_ig_leader'),
           ('agitator_legal_events.12', 'agitator_legal_events.12.b', 'scope:da_boss')]


def modifier_block(nodes, spec):
    event_id, option_id, recipient = spec
    event, = [n for n in nodes if n.key == event_id]
    option, = [n for n in event.children('option') if plain(n.one('name')) == option_id]
    scope, = option.children(recipient)
    block, = scope.children('add_modifier')
    return block


def expected_candidate(before):
    raw = before.decode('utf-8-sig')
    nodes = parse(raw)
    edits = []
    for spec in TARGETS:
        name, = modifier_block(nodes, spec).children('name')
        assert name.value == 'scandalous', 'Frozen source no longer has the obsolete target'
        span = raw[name.start:name.end]
        assert span.endswith('scandalous')
        edits.append((name.start, name.end, span[:-len('scandalous')] + 'modifier_scandalous'))
    for start, end, replacement in sorted(edits, reverse=True):
        raw = raw[:start] + replacement + raw[end:]
    return (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + raw.encode('utf-8')


def validate(data, before, modifiers, native_nodes):
    checks = []

    def check(name, value):
        checks.append({'name': name, 'pass': bool(value)})

    check('exactly_two_authorized_value_edits', data == expected_candidate(before))
    try:
        nodes = parse(data.decode('utf-8-sig'))
    except ValueError:
        check('parse', False)
        return checks
    check('parse', True)
    for spec in TARGETS:
        tag = spec[0]
        try:
            block = modifier_block(nodes, spec)
        except ValueError:
            check(tag + '.recipient_and_single_block', False)
            continue
        check(tag + '.recipient_and_single_block', True)
        target = plain(block.one('name'))
        check(tag + '.correct_typed_target', target == 'modifier_scandalous' and target in modifiers)
        check(tag + '.duration_preserved', plain(block.one('days')) == 'normal_modifier_time')
        check(tag + '.matches_native_modifier_block',
              [(n.key, n.op, n.value) for n in block.children()] ==
              [(n.key, n.op, n.value) for n in modifier_block(native_nodes, spec).children()])
    check('modifier_provider_unique', len(modifiers.get('modifier_scandalous', [])) == 1)
    check('trait_id_not_a_static_modifier', 'scandalous' not in modifiers)
    return checks


def scan(overrides=None):
    audit = Audit(ROOT, GAME)
    modifiers = audit.load('modifiers', 'common/static_modifiers')
    missing, references, dynamic = [], 0, []
    overrides = overrides or {}
    for folder in ('events', 'common/scripted_effects', 'common/scripted_buttons', 'common/on_actions'):
        for path in audit.paths(folder):
            nodes, raw, source = audit.read(path)
            if source in overrides:
                raw = overrides[source].decode('utf-8-sig')
                nodes = parse(raw)
                audit.hashes[source] = hashlib.sha256(overrides[source]).hexdigest()
            for node in walk(nodes):
                if node.key not in ('add_modifier', 'remove_modifier', 'has_modifier'):
                    continue
                target = plain(node.one('name')) if isinstance(node.value, list) else plain(node.value)
                if not target:
                    continue
                if '$' in target or ':' in target:
                    dynamic.append({'target': target, 'source': source})
                    continue
                references += 1
                if target not in modifiers:
                    missing.append({'target': target, 'operation': node.key, 'source': source,
                                    'line': raw.count('\n', 0, node.start) + 1})
    return {'modifier_count': len(modifiers), 'references': references, 'missing': missing,
            'parse_errors': audit.errors, 'dynamic_unresolved_by_this_tool': dynamic,
            'source_hashes': audit.hashes, 'engine_tested': False,
            'limits': 'Literal IDs in four named script families only; no scope/reachability simulation. '
                      'Journal definitions and other modifier commands are outside this inventory.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new output path inside the issue 42 evidence directory.')
    before = (EVIDENCE / 'before/agitator_law_events_2.txt').read_bytes()
    data = ((EVIDENCE / 'candidate/agitator_law_events_2.txt') if args.candidate else ROOT / SOURCE).read_bytes()
    audit = Audit(ROOT, GAME)
    modifiers = audit.load('modifiers', 'common/static_modifiers')
    traits = audit.load('traits', 'common/character_traits')
    native_nodes = parse((GAME / SOURCE).read_text(encoding='utf-8-sig'))
    checks = validate(data, before, modifiers, native_nodes)
    checks.append({'name': 'separate_character_trait_exists', 'pass': 'scandalous' in traits})
    modifier = modifiers['modifier_scandalous'][0][0]
    checks.append({'name': 'native_temporary_popularity_penalty',
                   'pass': plain(modifier.one('character_popularity_add')) == '-50'})
    icon = plain(modifier.one('icon'))
    checks.append({'name': 'modifier_icon_resolves', 'pass': (ROOT / icon).exists() or (GAME / icon).exists()})
    localization = {}
    for language in ('english', 'french'):
        local = {p.relative_to(ROOT).as_posix().casefold(): p for p in (ROOT / 'localization' / language).rglob('*.yml')}
        effective = [p for p in (GAME / 'localization' / language).rglob('*.yml')
                     if p.relative_to(GAME).as_posix().casefold() not in local] + list(local.values())
        rows = []
        for path in effective:
            match = re.search(r'^\s*modifier_scandalous\s*:\d*\s+"(.+)"',
                              path.read_text(encoding='utf-8-sig'), re.MULTILINE)
            if match:
                rows.append({'source': str(path), 'text': match.group(1)})
        localization[language] = rows
        checks.append({'name': language + '_name_provider_unique', 'pass': len(rows) == 1})
    controls = []
    if args.controls:
        raw = data.decode('utf-8-sig')
        event, = [n for n in parse(raw) if n.key == TARGETS[0][0]]
        option, = [n for n in event.children('option') if plain(n.one('name')) == TARGETS[0][1]]
        recipient, = option.children(TARGETS[0][2])
        duration, = modifier_block(parse(raw), TARGETS[0]).children('days')

        def mutate(node, old, new):
            span = raw[node.start:node.end]
            changed = raw[:node.start] + span.replace(old, new, 1) + raw[node.end:]
            return (b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b'') + changed.encode('utf-8')

        variants = {
            'obsolete_trait_target': data.replace(b'modifier_scandalous', b'scandalous', 1),
            'recipient_changed': mutate(recipient, TARGETS[0][2], 'scope:wrong_recipient'),
            'duration_changed': mutate(duration, 'normal_modifier_time', 'long_modifier_time'),
        }
        for name, bad in variants.items():
            failed = [r['name'] for r in validate(bad, before, modifiers, native_nodes) if not r['pass']]
            controls.append({'name': name, 'mutation_applied': bad != data, 'detected_by': failed,
                             'pass': bad != data and bool(failed)})
        duplicate = copy.copy(modifiers)
        duplicate['modifier_scandalous'] = modifiers['modifier_scandalous'] * 2
        failed = [r['name'] for r in validate(data, before, duplicate, native_nodes) if not r['pass']]
        controls.append({'name': 'duplicate_modifier_provider', 'detected_by': failed,
                         'pass': 'modifier_provider_unique' in failed})
    result = {'status': 'PASS_STATIC_ONLY' if all(r['pass'] for r in checks + controls) else 'FAIL_STATIC',
              'candidate': args.candidate, 'checks': checks, 'controls': controls,
              'localization': localization, 'scan': scan({'mod/' + SOURCE: data}), 'engine_tested': False}
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'checks': [sum(r['pass'] for r in checks), len(checks)],
                      'controls': [sum(r['pass'] for r in controls), len(controls)],
                      'remaining_missing': result['scan']['missing']}))
    return 0 if result['status'] == 'PASS_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
