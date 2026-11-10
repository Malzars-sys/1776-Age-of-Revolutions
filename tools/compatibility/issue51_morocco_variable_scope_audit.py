"""Read-only contract and scoped arithmetic fixtures for Morocco #51.

Reads captured before/native sources, candidate or live file; writes only a new
result. Fixtures model explicit country/state dictionaries, not the game engine.
"""
import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, with_ancestors
from issue44_event_targets_audit import payload

EVIDENCE = ROOT/'docs/reports/compatibility/V1_15_ISSUE51_MOROCCO_COUNTRY_VARIABLES_2026_11_10'
AREAS = ('al_rif', 'marrakech', 'inner_morocco')
VARS = tuple(area+'_progress_bar_current_var' for area in AREAS)


def inspect(data):
    raw = data.decode('utf-8-sig')
    nodes = parse(raw)
    entry = next(n for n in nodes if n.key == 'je_lands_of_anarchy')
    readers, writers = [], []
    for node, parents in with_ancestors(entry.children()):
        phase = 'monthly' if any(p.key == 'on_monthly_pulse' for p in parents) else 'initial'
        if node.key == 'set_variable' and node.one('name') in VARS:
            writers.append({'variable': node.one('name'), 'value': node.one('value'), 'phase': phase,
                            'state_nested': any(p.key == 'random_scope_state' or p.key.startswith('scope:') for p in parents),
                            'payload': payload([node]), 'line': raw.count('\n', 0, node.start)+1})
        if node.key != 'add_modifier' or node.one('name') != 'state_of_anarchy_scaled_mod':
            continue
        multipliers = node.children('multiplier')
        if len(multipliers) != 1:
            raise ValueError('Expected one multiplier per selected modifier')
        multiplier = multipliers[0]
        expression = multiplier.one('value')
        variable = expression.split('var:', 1)[-1] if isinstance(expression, str) else None
        readers.append({'variable': variable, 'expression': expression, 'phase': phase,
                        'state_nested': any(p.key == 'random_scope_state' or p.key.startswith('scope:') for p in parents),
                        'multiplier': multiplier, 'line': raw.count('\n', 0, multiplier.start)+1})
    return raw, nodes, entry, readers, writers


def calculate(row, country, state):
    expression = row['expression']
    if expression.startswith('root.var:'):
        value = country[row['variable']]
    elif expression.startswith('var:'):
        value = state[row['variable']]
    else:
        raise ValueError('Unsupported expression')
    multiplier = row['multiplier']
    return Decimal(str(value))/Decimal(multiplier.one('divide')) + Decimal(multiplier.one('add'))


def verify(data, original, native, contract):
    checks, cases = [], []
    def check(name, result):
        checks.append({'name': name, 'passed': bool(result)})
    try:
        raw, nodes, entry, readers, writers = inspect(data)
        _, old_nodes, old_entry, _, old_writers = inspect(original)
        _, _, _, native_readers, native_writers = inspect(native)
    except (ValueError, StopIteration, UnicodeError) as error:
        return [{'name': 'parse_and_selected_entry', 'passed': False, 'error': str(error)}], [], [], []
    check('parse_and_selected_entry', True)
    candidate, reversed_data = original, data
    for change in contract['changes']:
        candidate = candidate.replace(change['old'].encode(), change['new'].encode())
        reversed_data = reversed_data.replace(change['new'].encode(), change['old'].encode())
    check('exact_six_prefix_patch', data == candidate)
    check('all_other_bytes_reversible', reversed_data == original)
    check('BOM_preserved', data.startswith(b'\xef\xbb\xbf') == original.startswith(b'\xef\xbb\xbf'))
    check('six_readers_three_per_phase', len(readers)==6 and Counter(r['phase'] for r in readers)==Counter(initial=3, monthly=3))
    check('each_variable_in_both_phases', Counter((r['phase'],r['variable']) for r in readers)==Counter((p,v) for p in ('initial','monthly') for v in VARS))
    check('readers_are_state_nested', all(r['state_nested'] for r in readers))
    check('country_writers_preserved', [r['payload'] for r in writers] == [r['payload'] for r in old_writers])
    check('six_writers_not_state_nested', len(writers)==6 and not any(r['state_nested'] for r in writers))
    check('initial_values_remain_260', sorted((r['variable'],r['value']) for r in writers if r['phase']=='initial') == sorted((v,'260') for v in VARS))
    check('monthly_bar_sources_match_native', sorted((r['variable'],r['value']) for r in writers if r['phase']=='monthly') == sorted((r['variable'],r['value']) for r in native_writers if r['phase']=='monthly'))
    check('all_outcomes_preserved', payload(entry.children('outcome')) == payload(old_entry.children('outcome')))
    check('DLC_and_lobby_preserved', payload(entry.children('is_shown_in_lobby')) == payload(old_entry.children('is_shown_in_lobby')))
    native_index = {(r['phase'],r['variable']):r for r in native_readers}
    for row in readers:
        identity = row['phase']+'.'+str(row['variable'])
        check(identity+'.explicit_country_root', row['expression']=='root.var:'+str(row['variable']))
        native_row = native_index.get((row['phase'],row['variable']))
        check(identity+'.native_multiplier_payload', native_row is not None and payload([row['multiplier']])==payload([native_row['multiplier']]))
        country = dict.fromkeys(VARS, 260) if row['phase']=='initial' else dict(zip(VARS, (400,100,515)))
        state = {} if row['phase']=='initial' else dict.fromkeys(VARS,999)
        try:
            value = calculate(row, country, state)
            expected = Decimal(str(country[row['variable']]))/Decimal(-100)+Decimal('5.15')
            passed = value == expected
            cases.append({'case': identity, 'country_value': country[row['variable']], 'state_value': state.get(row['variable']),
                          'multiplier': str(value), 'expected': str(expected), 'passed': passed})
        except (KeyError, ValueError, ArithmeticError) as error:
            cases.append({'case': identity, 'passed': False, 'error': str(error)})
    check('state_absent_or_conflicting_values_ignored', len(cases)==6 and all(c['passed'] for c in cases))
    return checks, cases, readers, writers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new evidence output path under issue51.')
    contract = json.loads((EVIDENCE/'CONTRACT.json').read_text(encoding='utf-8'))
    rel = contract['path']
    original = (EVIDENCE/'before'/rel).read_bytes()
    native = (EVIDENCE/'native'/rel).read_bytes()
    path = EVIDENCE/'candidate'/rel if args.candidate else ROOT/rel
    data = path.read_bytes()
    checks, cases, readers, writers = verify(data, original, native, contract)
    controls = []
    if args.controls:
        # Each of the six scope mistakes must be detected by its own scope test.
        for row in readers:
            target = ('value = '+row['expression']).encode()
            found = [m.start() for m in re.finditer(re.escape(target), data)]
            position = found[0 if row['phase']=='initial' else 1]
            changed = data[:position]+target.replace(b'root.var:',b'var:')+data[position+len(target):]
            result, _, _, _ = verify(changed,original,native,contract)
            name = row['phase']+'.'+row['variable']+'.explicit_country_root'
            controls.append({'case': 'wrong_scope.'+name, 'passed': any(r['name']==name and not r['passed'] for r in result)})
        for name,changed,required in [
            ('wrong_coefficient',data.replace(b'divide = -100',b'divide = -10',1),'initial.al_rif_progress_bar_current_var.native_multiplier_payload'),
            ('unrelated_outcome',data.replace(b'trigger_event = lands_of_anarchy.2',b'trigger_event = lands_of_anarchy.99',1),'all_outcomes_preserved'),
        ]:
            result, _, _, _ = verify(changed,original,native,contract)
            controls.append({'case': name, 'passed': changed != data and any(r['name']==required and not r['passed'] for r in result)})
    result = {'status': 'PASS_SCOPED_STATIC_ONLY' if all(x['passed'] for x in checks+controls) else 'FAIL_STATIC',
              'mode': 'candidate' if args.candidate else 'live', 'checks': checks, 'cases': cases, 'controls': controls,
              'readers': [{k:v for k,v in r.items() if k!='multiplier'} for r in readers], 'writers': writers,
              'sha256': hashlib.sha256(data).hexdigest(), 'engine_tested': False,
              'limits': 'Explicit source contract and six country/state fixtures; no engine simulation or transferred-state cleanup certification.'}
    with output.open('x', encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':result['status'], 'checks':[sum(x['passed'] for x in checks),len(checks)],
                      'cases':[sum(x['passed'] for x in cases),len(cases)],'controls':[sum(x['passed'] for x in controls),len(controls)],
                      'failed':[x['name'] for x in checks if not x['passed']]}))
    return 0 if result['status']=='PASS_SCOPED_STATIC_ONLY' else 1


if __name__=='__main__':
    raise SystemExit(main())
