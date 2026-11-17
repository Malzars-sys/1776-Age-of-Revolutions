"""Check the bounded Commune counter bridge; no live script writes."""
from pathlib import Path
import hashlib
import json
import sys
sys.dont_write_bytecode = True
LOT = Path(__file__).resolve().parent
ROOT = next(p for p in LOT.parents if (p / 'descriptor.mod').is_file())
sys.path.insert(0, str(ROOT / 'tools/compatibility'))
from issue24_map_dlc_audit import GAME, parse, plain

COUNTER = 'paris_commune_progress_var'
BAR = 'je_paris_commune_progress_bar'


def project(node, reverse_bridge=False):
    key = node.key.removeprefix('REPLACE_OR_CREATE:')
    if reverse_bridge and key == 'if':
        condition = node.children('limit')
        change = node.children('change_global_variable')
        if (len(condition) == len(change) == 1 and
                [(n.key, n.op, n.value) for n in condition[0].children()] ==
                [('has_global_variable', '=', COUNTER)] and
                change[0].one('name') == COUNTER):
            assert [n.key for n in node.children()] == ['limit', 'change_global_variable']
            assert [n.key for n in change[0].children()] == ['name', 'add']
            delta = change[0].one('add')
            return ['je:je_paris_commune', '?=', [
                ['add_progress', '=', [['value', '=', delta], ['name', '=', BAR]]]]]
    return [key, node.op, [project(n, reverse_bridge) for n in node.children()]
            if isinstance(node.value, list) else node.value]


def object_parity(native_raw, candidate_raw, selected=None):
    native = [n for n in parse(native_raw) if selected is None or n.key in selected]
    try:
        return ([project(n) for n in native] ==
                [project(n, True) for n in parse(candidate_raw)])
    except (ValueError, AssertionError):
        return False


def audit(live=False):
    contract = json.loads((LOT / 'CONTRACT.json').read_text(encoding='utf-8'))
    checks = []
    def check(name, result):
        checks.append({'case': name, 'passed': bool(result)})
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    for spec in contract['specs']:
        path = (ROOT if live else LOT / 'candidate') / spec['path']
        data = path.read_bytes(); raw = data.decode('utf-8-sig')
        original = (GAME / spec['source']).read_bytes().decode('utf-8-sig')
        selected = None if spec['copy_mode'].startswith('current native') else set(spec['objects'])
        check(spec['path'] + '.source_current', sha(GAME / spec['source']) == spec['native_sha256'])
        check(spec['path'] + '.candidate_bytes', sha(path) == spec['candidate_sha256'])
        check(spec['path'] + '.only_progress_bridge_changes', object_parity(original, raw, selected))
        check(spec['path'] + '.no_missing_journal_scope', 'je:je_paris_commune' not in raw)
        check(spec['path'] + '.each_progress_block_guarded',
              raw.count('has_global_variable = ' + COUNTER) == len(spec['changes']) and
              raw.count('name = ' + COUNTER) == len(spec['changes']))
    # Verify independently that the model being reconnected is actually authored
    # in the retained JE family and its start choices, without changing them.
    je = (ROOT / 'common/journal_entries/01_paris_commune.txt').read_text(encoding='utf-8-sig')
    start = (ROOT / 'events/agitators_events/paris_commune_events.txt').read_text(encoding='utf-8-sig')
    check('retained_journals_read_the_same_global_counter',
          je.count('value = global_var:' + COUNTER) == 2 and
          'global_var:' + COUNTER + ' >= 100' in je and 'global_var:' + COUNTER + ' <= 0' in je)
    check('existing_start_choices_initialize_counter',
          'name = ' + COUNTER + ' value = 40' in start and
          'name = ' + COUNTER + ' value = 60' in start)
    first = contract['specs'][0]
    original = (GAME / first['source']).read_text(encoding='utf-8-sig')
    raw = ((ROOT if live else LOT / 'candidate') / first['path']).read_text(encoding='utf-8-sig')
    mutations = [
        ('changed_delta', raw.replace('add = 10', 'add = 11', 1)),
        ('removed_guard', raw.replace('has_global_variable = ' + COUNTER, 'always = yes', 1)),
        ('wrong_counter', raw.replace('name = ' + COUNTER, 'name = wrong_counter', 1)),
    ]
    controls = [{'case': name, 'detected': not object_parity(original, text)}
                for name, text in mutations]
    check('counterfactual_delta_guard_and_counter_errors_rejected', all(r['detected'] for r in controls))
    return {'status': 'PASS_STATIC_ONLY' if all(c['passed'] for c in checks) else 'FAIL_STATIC',
            'passed': sum(c['passed'] for c in checks), 'total': len(checks),
            'checks': checks, 'negative_controls': controls, 'engine_tested': False}


if __name__ == '__main__':
    live = '--live' in sys.argv
    result = audit(live)
    dest = LOT / ('LIVE_VALIDATION.json' if live else 'CANDIDATE_VALIDATION.json')
    with dest.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}))
    print(json.dumps([c for c in result['checks'] if not c['passed']]))
    if result['status'] != 'PASS_STATIC_ONLY':
        raise SystemExit(1)
