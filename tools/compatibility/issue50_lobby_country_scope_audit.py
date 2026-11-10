"""Read-only #50 Acre lobby-guard contract and conservative boolean fixtures.

Not an engine interpreter: fixtures eagerly evaluate the three selected terms
and test both possible absent-target defaults of the optional comparison.
The required existence term must make the whole condition false either way.
No installation, log rotation, Git write or old-evidence overwrite.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from issue24_map_dlc_audit import ROOT, GAME, parse
from issue44_event_targets_audit import payload

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE50_LOBBY_COUNTRY_SCOPES_2026_11_10'


def selected(data):
    raw = data.decode('utf-8-sig')
    nodes = parse(raw)
    entries = [n for n in nodes if n.key == 'je_acre_dispute']
    if len(entries) != 1:
        raise ValueError('Expected one Acre entry')
    lobbies = entries[0].children('is_shown_in_lobby')
    if len(lobbies) != 1:
        raise ValueError('Expected one Acre lobby block')
    return raw, nodes, lobbies[0]


def evaluate(lobby, country, dlc, optional_absent):
    results = []
    for n in lobby.children():
        if n.key == 'has_dlc_feature' and n.value == 'rp1_content':
            results.append(dlc)
        elif n.key == 'exists' and n.value == 'c:BOL':
            results.append(country != 'absent')
        elif n.key == 'c:BOL' and n.value == 'THIS':
            if country == 'absent':
                if n.op != '?=':
                    raise ValueError('Unset country scope')
                results.append(optional_absent)
            else:
                results.append(country == 'matching')
        else:
            raise ValueError('Unsupported fixture predicate: ' + n.key)
    return all(results)


def verify(data, original, contract):
    checks = []
    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
    try:
        raw, nodes, lobby = selected(data)
        old_raw, old_nodes, old_lobby = selected(original)
    except (UnicodeError, ValueError) as error:
        return [{'name': 'parse_selected_entry', 'passed': False, 'error': str(error)}], []
    check('parse_selected_entry', True)
    check('BOM_preserved', data.startswith(b'\xef\xbb\xbf') == original.startswith(b'\xef\xbb\xbf'))
    check('exact_two_line_patch', data == original.replace(contract['old'].encode(), contract['new'].encode(), 1))
    check('reversible_to_original_bytes', data.replace(contract['new'].encode(), contract['old'].encode(), 1) == original)
    check('outside_lobby_bytes_preserved', raw[:lobby.start] + raw[lobby.end:] == old_raw[:old_lobby.start] + old_raw[old_lobby.end:])
    # Compare all parsed fields after removing ONLY the selected lobby nodes.
    after_tree = copy.deepcopy(nodes)
    before_tree = copy.deepcopy(old_nodes)
    for tree in (after_tree, before_tree):
        entry = next(n for n in tree if n.key == 'je_acre_dispute')
        entry.value = [n for n in entry.children() if n.key != 'is_shown_in_lobby']
    check('outcomes_activation_effects_and_other_objects_unchanged', payload(after_tree) == payload(before_tree))
    check('explicit_country_exists_once', [(n.op, n.value) for n in lobby.children('exists')] == [('=', 'c:BOL')])
    check('safe_identity_comparison_once', [(n.op, n.value) for n in lobby.children('c:BOL')] == [('?=', 'THIS')])
    check('DLC_gate_preserved', payload(lobby.children('has_dlc_feature')) == payload(old_lobby.children('has_dlc_feature')))
    check('only_three_expected_terms', len(lobby.children()) == 3 and {n.key for n in lobby.children()} == {'has_dlc_feature', 'exists', 'c:BOL'})
    check('country_provider_unique', len([n for n in parse((ROOT/'common/country_definitions/00_countries.txt').read_text(encoding='utf-8-sig')) if n.key=='BOL']) == 1)
    cases = []
    for country in ('absent', 'matching', 'other'):
        for dlc in (False, True):
            try:
                outcomes = [evaluate(lobby, country, dlc, default) for default in (False, True)]
                expected = country == 'matching' and dlc
                passed = all(value == expected for value in outcomes)
                cases.append({'country': country, 'DLC': dlc, 'expected': expected,
                              'optional_absent_false_or_true': outcomes, 'passed': passed})
            except ValueError as error:
                cases.append({'country': country, 'DLC': dlc, 'passed': False, 'error': str(error)})
    check('six_context_cases_pass', all(c['passed'] for c in cases))
    try:
        preserved = all(evaluate(lobby, c, d, False) == evaluate(old_lobby, c, d, False) for c in ('matching', 'other') for d in (False, True))
    except ValueError:
        preserved = False
    check('existing_country_behavior_preserved', preserved)
    return checks, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new output path in the issue50 evidence directory.')
    contract = json.loads((EVIDENCE/'CONTRACT.json').read_text(encoding='utf-8'))
    rel = contract['relative_path']
    original = (EVIDENCE/'before'/rel).read_bytes()
    path = EVIDENCE/'candidate'/rel if args.candidate else ROOT/rel
    data = path.read_bytes()
    checks, cases = verify(data, original, contract)
    controls = []
    if args.controls:
        mutations = [
            ('missing_exists_guard', data.replace(b'\t\texists = c:BOL', b'\t\t# removed existence guard', 1), 'explicit_country_exists_once'),
            ('strict_comparison_restored', data.replace(b'c:BOL ?= THIS', b'c:BOL = THIS', 1), 'safe_identity_comparison_once'),
            ('wrong_country', data.replace(b'c:BOL ?= THIS', b'c:BRZ ?= THIS', 1), 'safe_identity_comparison_once'),
            ('DLC_gate_removed', data.replace(b'has_dlc_feature = rp1_content', b'has_dlc_feature = other_content', 1), 'DLC_gate_preserved'),
            ('outcome_changed', data.replace(b'id = acre_dispute.3', b'id = acre_dispute.4', 1), 'outcomes_activation_effects_and_other_objects_unchanged'),
            ('unrelated_bytes_changed', data + b'\n# unauthorized extra data\n', 'outside_lobby_bytes_preserved'),
        ]
        for name, mutated, required in mutations:
            result, _ = verify(mutated, original, contract)
            controls.append({'case': name, 'detected_by': required, 'passed': any(x['name']==required and not x['passed'] for x in result)})
    result = {'status': 'PASS_SCOPED_STATIC_ONLY' if all(x['passed'] for x in checks+controls) else 'FAIL_STATIC',
              'mode': 'candidate' if args.candidate else 'live', 'checks': checks, 'cases': cases, 'controls': controls,
              'source': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'engine_tested': False,
              'limits': 'Three-predicate conservative fixture model, not an engine, general scope interpreter, or test of all journal reachability.'}
    with output.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({'status': result['status'], 'checks': [sum(x['passed'] for x in checks),len(checks)],
                      'context_cases': [sum(x['passed'] for x in cases),len(cases)],
                      'controls': [sum(x['passed'] for x in controls),len(controls)],
                      'failed': [x['name'] for x in checks if not x['passed']]}))
    return 0 if result['status']=='PASS_SCOPED_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
