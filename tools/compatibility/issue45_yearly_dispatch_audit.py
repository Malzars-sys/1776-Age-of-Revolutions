"""Read-only additive on_action/list audit and yearly-dispatch checks for #45.

Only one new JSON under the evidence directory is written. Candidate overlays
and controls stay in memory; there is no installer or Git operation.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, walk, plain

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE45_YEARLY_DISPATCH_2026_11_09'
SOURCE = 'common/on_actions/phase1_japan_tenpo_on_actions.txt'
MAIN = 'common/on_actions/00_code_on_actions.txt'
HOOK = 'on_yearly_pulse'
CHILD = 'aor1776_phase1_japan_yearly_pulse'
LIST_FIELDS = {'events': 'events', 'random_events': 'events', 'first_valid': 'events',
               'on_actions': 'actions', 'random_on_actions': 'actions', 'first_valid_on_action': 'actions'}


def candidate(before):
    bom = b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b''
    raw = before[len(bom):]
    nodes = parse(raw.decode('utf-8'))
    assert len(nodes) == 1 and nodes[0].key == HOOK
    newline = b'\r\n' if b'\r\n' in raw else b'\n'
    prefix = ('on_yearly_pulse = {\n\ton_actions = { ' + CHILD + ' }\n}\n\n').encode('utf-8').replace(b'\n', newline)
    return bom + prefix + raw.replace(HOOK.encode(), CHILD.encode(), 1)


def collisions(actions):
    result = []
    for key, entries in actions.items():
        for field in ('effect', 'trigger'):
            rows = [{'source': source, 'line': raw.count('\n', 0, node.start) + 1}
                    for parent, source, raw in entries for node in parent.children(field)]
            if len(rows) > 1:
                result.append({'action': key, 'field': field, 'providers': rows})
    return result


def inventory(audit, override=None):
    events = audit.load('events', 'events')
    actions = audit.load('actions', 'common/on_actions')
    if override is not None:
        actions = {k: [r for r in rows if r[1] != 'mod/' + SOURCE] for k, rows in actions.items()}
        actions = {k: rows for k, rows in actions.items() if rows}
        raw = override.decode('utf-8-sig')
        for node in parse(raw):
            actions.setdefault(node.key, []).append((node, 'mod/' + SOURCE, raw))
    refs, dynamic, skipped = [], [], defaultdict(int)
    for owner, entries in actions.items():
        for node, source, raw in entries:
            for block in node.children():
                if block.key == 'fallback':
                    items, category = [block], 'actions'
                elif block.key in LIST_FIELDS:
                    items, category = block.children(), LIST_FIELDS[block.key]
                else:
                    continue
                for child in items:
                    if child.key in ('chance_to_happen', 'chance_of_no_event', 'delay'):
                        skipped[child.key] += 1
                        continue
                    target = plain(child.value)
                    if target == '0':
                        skipped['no_event_sentinel'] += 1
                        continue
                    if target is None:
                        skipped['nonliteral_entry'] += 1
                        continue
                    row = {'owner': owner, 'field': block.key, 'target': target, 'category': category,
                           'source': source, 'line': raw.count('\n', 0, child.start) + 1}
                    (dynamic if any(c in target for c in '$[]@') else refs).append(row)
    missing = [r for r in refs if r['target'] not in (events if r['category'] == 'events' else actions)]
    return {'actions': len(actions), 'event_definitions': len(events), 'references': refs,
            'missing': missing, 'dynamic': dynamic, 'metadata_not_targets': dict(skipped),
            'collisions': collisions(actions), 'parse_errors': audit.errors}, actions, events


def verify(data, before, main_data, main_before, inv, actions, events):
    checks = []

    def check(name, value):
        checks.append({'name': name, 'pass': bool(value)})

    check('exact_two_span_transformation', data == candidate(before))
    old_raw, raw = before.decode('utf-8-sig'), data.decode('utf-8-sig')
    old, = parse(old_raw)
    nodes = parse(raw)
    check('only_hook_and_child_definitions', [n.key for n in nodes] == [HOOK, CHILD])
    root = next((n for n in nodes if n.key == HOOK), None)
    child = next((n for n in nodes if n.key == CHILD), None)
    check('hook_has_only_additive_dispatch', root is not None and len(root.children()) == 1
          and root.children()[0].key == 'on_actions')
    targets = [plain(n.value) for b in root.children('on_actions') for n in b.children()] if root else []
    check('single_correct_child_link', targets == [CHILD])
    check('child_has_only_one_effect', child is not None and len(child.children()) == 1
          and child.children()[0].key == 'effect')
    if child and len(child.children('effect')) == 1:
        effect = child.children('effect')[0]
        original, = old.children('effect')
        check('effect_body_byte_text_preserved', raw[effect.start:effect.end] == old_raw[original.start:original.end])
    else:
        check('effect_body_byte_text_preserved', False)
    check('main_and_manila_bytes_preserved', main_data == main_before)
    check('one_merged_root_effect', sum(len(n.children('effect')) for n, _, _ in actions.get(HOOK, [])) == 1)
    check('one_child_provider_and_effect', len(actions.get(CHILD, [])) == 1 and
          sum(len(n.children('effect')) for n, _, _ in actions.get(CHILD, [])) == 1)
    check('no_duplicate_effect_or_trigger_blocks', not inv['collisions'])
    check('parsed_inputs_valid', not inv['parse_errors'])
    old_calls = [plain(n.one('id')) for n in walk([old]) if n.key == 'trigger_event']
    new_calls = [plain(n.one('id')) for n in walk([child]) if n.key == 'trigger_event'] if child else []
    check('six_identical_event_calls', old_calls == new_calls and len(new_calls) == 6)
    check('six_event_providers_unique', all(len(events.get(key, [])) == 1 for key in old_calls))
    prior = json.loads((EVIDENCE / 'INVENTORY_BEFORE.json').read_text(encoding='utf-8'))['inventory']
    check('six_unrelated_missing_targets_retained', inv['missing'] == prior['missing'] and len(prior['missing']) == 6)
    check('exactly_one_new_list_reference', len(inv['references']) == len(prior['references']) + 1)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--native', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new evidence output path.')
    if args.native and not args.inventory:
        parser.error('--native is an inventory-only control.')
    before = (EVIDENCE / 'before' / SOURCE).read_bytes()
    main_before = (EVIDENCE / 'before' / MAIN).read_bytes()
    data = ((EVIDENCE / 'candidate' / SOURCE) if args.candidate else ROOT / SOURCE).read_bytes()
    audit = Audit(ROOT, GAME, args.native)
    inv, actions, events = inventory(audit, data if args.candidate else None)
    result = {'inventory': inv, 'engine_tested': False}
    if not args.inventory:
        checks = verify(data, before, (ROOT / MAIN).read_bytes(), main_before, inv, actions, events)
        controls = []
        if args.controls:
            for name, bad in [('old_conflicting_hook', before),
                              ('broken_child_link', data.replace(CHILD.encode(), b'aor1776_missing_child', 1)),
                              ('changed_japanese_date', data.replace(b'1787.1.1', b'1788.1.1', 1))]:
                fixture = Audit(ROOT, GAME)
                bad_inv, bad_actions, bad_events = inventory(fixture, bad)
                bad_checks = verify(bad, before, (ROOT / MAIN).read_bytes(), main_before,
                                    bad_inv, bad_actions, bad_events)
                failed = [r['name'] for r in bad_checks if not r['pass']]
                controls.append({'name': name, 'detected_by': failed, 'pass': bool(failed)})
            bad_checks = verify(data, before, main_before + b'\n# drift\n', main_before, inv, actions, events)
            controls.append({'name': 'changed_main_file', 'pass': any(not r['pass'] and
                             r['name'] == 'main_and_manila_bytes_preserved' for r in bad_checks)})
            fragments = [(n, 'fixture', '') for n in parse('hook = { on_actions = { first } } hook = { on_actions = { second } }')]
            controls.append({'name': 'valid_additive_definitions_positive_control',
                             'kind': 'positive', 'pass': not collisions({'hook': fragments})})
        result.update({'checks': checks, 'controls': controls,
                       'status': 'PASS_SCOPED_STATIC_ONLY' if all(r['pass'] for r in checks + controls) else 'FAIL_STATIC'})
    else:
        result['status'] = 'FINDINGS_STATIC_ONLY' if inv['missing'] or inv['collisions'] else 'PASS_STATIC_ONLY'
    result['source_hashes'] = audit.hashes
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'actions': inv['actions'], 'references': len(inv['references']),
                      'remaining_missing': len(inv['missing']), 'effect_trigger_conflicts': len(inv['collisions']),
                      'checks': [sum(r['pass'] for r in result.get('checks', [])), len(result.get('checks', []))],
                      'controls': [sum(r['pass'] for r in result.get('controls', [])), len(result.get('controls', []))],
                      'failed': [r['name'] for r in result.get('checks', []) if not r['pass']]}))
    return 1 if result['status'] == 'FAIL_STATIC' else 0


if __name__ == '__main__':
    raise SystemExit(main())
