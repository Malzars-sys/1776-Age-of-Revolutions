"""Read-only check of the one-line #47 annual-dispatch correction.

Writes one new report under this mission's evidence directory. In-memory
controls never modify gameplay files. No installer, engine or Git writes.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, plain
from issue45_yearly_dispatch_audit import inventory

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE47_OBSOLETE_MORTALITY_DISPATCH_2026_11_10'
SOURCE = 'common/on_actions/00_code_on_actions.txt'
TARGET = 'on_memento_mori'
HOOK = 'on_yearly_pulse_country'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def candidate(before):
    """Remove the single complete registration line, preserving every other byte."""
    lines = before.splitlines(keepends=True)
    found = [line for line in lines if TARGET.encode() in line]
    if len(found) != 1 or found[0].strip() != b'on_memento_mori # IG leader death':
        raise ValueError('Expected exactly the reviewed obsolete registration line')
    return before.replace(found[0], b'', 1)


def load(data=None, native=False):
    audit = Audit(ROOT, GAME, native)
    if data is not None:
        raw = data.decode('utf-8-sig')
        rel = 'mod/' + SOURCE
        # Audit.read will retain the live input hash while the parser reads this
        # explicitly identified projection; no temporary source is installed.
        audit.cache[rel] = (parse(raw), raw, rel)
    inv, actions, events = inventory(audit)
    return audit, inv, actions, events


def signature(node):
    return (node.key, node.op,
            tuple(signature(n) for n in node.children())
            if isinstance(node.value, list) else node.value)


def verify(data, before, inv, actions, prior, native_actions):
    checks = []

    def check(name, passed):
        checks.append({'name': name, 'pass': bool(passed)})

    expected = candidate(before)
    nodes, old_nodes = parse(data.decode('utf-8-sig')), parse(before.decode('utf-8-sig'))
    new_hook = [n for n in nodes if n.key == HOOK]
    old_hook = [n for n in old_nodes if n.key == HOOK]
    check('exact_one_line_removal_and_unrelated_bytes_preserved', data == expected)
    check('same_bom', data.startswith(b'\xef\xbb\xbf') == before.startswith(b'\xef\xbb\xbf'))
    check('same_top_level_hook_order', [n.key for n in nodes] == [n.key for n in old_nodes])
    check('single_country_yearly_hook_in_main', len(new_hook) == len(old_hook) == 1)
    check('all_other_main_hooks_semantically_identical',
          [signature(n) for n in nodes if n.key != HOOK] ==
          [signature(n) for n in old_nodes if n.key != HOOK])
    if len(new_hook) == len(old_hook) == 1:
        new_lists, old_lists = new_hook[0].children('on_actions'), old_hook[0].children('on_actions')
        check('one_annual_dispatch_list', len(new_lists) == len(old_lists) == 1)
        check('annual_effect_and_events_preserved',
              [signature(n) for n in new_hook[0].children() if n.key != 'on_actions'] ==
              [signature(n) for n in old_hook[0].children() if n.key != 'on_actions'])
        if len(new_lists) == len(old_lists) == 1:
            check('remaining_list_order_and_all_delays_preserved',
                  [signature(n) for n in new_lists[0].children()] ==
                  [signature(n) for n in old_lists[0].children() if plain(n.value) != TARGET])
    check('exact_preexisting_missing_registration', len(prior['missing']) == 1 and
          prior['missing'][0]['target'] == TARGET and prior['missing'][0]['owner'] == HOOK)
    check('no_missing_effective_list_or_fallback_targets', not inv['missing'])
    check('exactly_one_fewer_list_reference', len(inv['references']) == len(prior['references']) - 1)
    identity = lambda r: (r['owner'], r['field'], r['target'], r['category'], r['source'])
    check('only_obsolete_reference_removed',
          Counter(identity(r) for r in inv['references']) ==
          Counter(identity(r) for r in prior['references'] if r['target'] != TARGET))
    check('no_new_action_provider_or_empty_stub', len(actions) == prior['actions'] and TARGET not in actions)
    check('event_provider_count_preserved', inv['event_definitions'] == prior['event_definitions'])
    check('no_effect_or_trigger_collision', not inv['collisions'])
    check('no_parse_errors', not inv['parse_errors'])
    check('native_has_no_obsolete_provider', TARGET not in native_actions)
    native_registration = [plain(n.value) for parent, _, _ in native_actions.get(HOOK, [])
                           for block in parent.children('on_actions') for n in block.children()]
    check('native_has_no_obsolete_annual_registration', TARGET not in native_registration)
    check('character_death_creation_monthly_hooks_retained',
          all(k in actions for k in ('on_character_death', 'on_character_creation', 'on_monthly_pulse_character')))
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Choose a new output path inside the mission evidence directory')
    before = (EVIDENCE / 'before' / SOURCE).read_bytes()
    data = candidate(before) if args.candidate else (ROOT / SOURCE).read_bytes()
    _, prior, _, _ = load(before)
    _, native, native_actions, _ = load(native=True)
    audit, inv, actions, _ = load(data)
    checks = verify(data, before, inv, actions, prior, native_actions)
    controls = []
    if args.controls:
        fixtures = [('restored_missing_call', before),
                    ('changed_first_annual_delay', data.replace(b'delay = { days = 1 }',
                                                              b'delay = { days = 2 }', 1)),
                    ('empty_stub_instead_of_removal', before + b'\non_memento_mori = {}\n')]
        for name, bad in fixtures:
            _, bad_inv, bad_actions, _ = load(bad)
            failures = [c['name'] for c in verify(bad, before, bad_inv, bad_actions, prior,
                                                 native_actions) if not c['pass']]
            controls.append({'name': name, 'pass': bool(failures), 'detected_by': failures})
    result = {'status': 'PASS_SCOPED_STATIC_ONLY' if all(c['pass'] for c in checks + controls)
              else 'FAIL_STATIC', 'engine_tested': False,
              'projection': args.candidate, 'source_sha256': sha(data),
              'before_sha256': sha(before), 'checks': checks, 'controls': controls,
              'before_inventory': prior, 'after_inventory': inv,
              'native_inventory': native, 'effective_input_hashes': audit.hashes}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'checks': len(checks),
                      'failed': [c['name'] for c in checks if not c['pass']],
                      'controls_passed': sum(c['pass'] for c in controls),
                      'controls_total': len(controls), 'missing_before': len(prior['missing']),
                      'missing_after': len(inv['missing']), 'output': str(output)}))
    return 0 if result['status'] == 'PASS_SCOPED_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
