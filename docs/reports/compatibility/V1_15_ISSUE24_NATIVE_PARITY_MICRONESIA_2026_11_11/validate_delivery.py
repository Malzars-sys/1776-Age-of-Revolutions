"""Read-only, bounded delivery validation. Writes only a new requested result."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
LOT = Path(__file__).resolve().parent
ROOT = next(p for p in LOT.parents if (p / 'descriptor.mod').is_file())
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools/compatibility'))
from issue24_map_dlc_audit import parse
from issue24_native_parity_audit import ast


def read(name):
    return json.loads((LOT / name).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate():
    base = read('BASELINE.json')
    before = read('PRE_INSTALL_QUALIFICATION.json')
    final = read('FINAL_QUALIFICATION.json')
    m = read('FINAL_MAP.json')
    native = read('NATIVE_CONTROL.json')
    je = read('CURRENT_JOURNAL_DEPENDENCIES.json')
    rsr = read('RUSSIAN_CIVIL_WAR_PROVIDER/INSTALLATION_CONTRACT.json')
    checks = []

    def check(name, result, **details):
        checks.append(dict(case=name, passed=bool(result), **details))

    shared = 'common/history/states/00_states.txt'
    raw = (ROOT / shared).read_bytes()
    original = (LOT / '00_states.before.txt').read_bytes()
    check('shared source only adds the one Mariana allocation token',
          raw.count(b'xA7F7E3 xEF50C0') == 1 and
          raw.replace(b'xA7F7E3 xEF50C0', b'xA7F7E3', 1) == original)
    check('installed state history matches the validated candidate',
          raw == (LOT / '00_states.candidate.txt').read_bytes())
    check('the prior single allocation hole is closed',
          [r['province'] for r in before['raw_qualification']['unallocated_candidates']] == ['XEF50C0']
          and not final['raw_qualification']['unallocated_candidates'])
    allocation = [r for r in m['initial_state_allocations'] if 'XEF50C0' in r['provinces']]
    check('new province allocated once to existing PHI state', len(allocation) == 1
          and allocation[0]['country'] == 'PHI'
          and allocation[0]['state'] == 'STATE_WEST_MICRONESIA')
    # The added token shifts diagnostic character positions by eight. Preserve
    # all other raw fields, and require that exact offset change where expected.
    expected_repeated = copy.deepcopy(before['raw_qualification']['repeated_allocations'])
    normalized_original = original.decode('utf-8-sig').replace('\r\n', '\n')
    insertion = normalized_original.index('xA7F7E3') + len('xA7F7E3')
    shifted = 0
    for row in expected_repeated:
        for occurrence in row['occurrences']:
            if occurrence['source'] == 'mod/' + shared:
                for key in ['token_start', 'list_start']:
                    if occurrence[key] >= insertion:
                        occurrence[key] += len(' xEF50C0')
                        shifted += 1
    check('raw repeated findings preserved with exact insertion-offset reconciliation',
          expected_repeated == final['raw_qualification']['repeated_allocations'],
          adjusted_offset_fields=shifted, inserted_characters=len(' xEF50C0'))
    check('all thirteen raw findings have exact native ownership provenance',
          final['provenance_counts'] == {'identical_unconditional_owner_instructions_in_native': 13})
    check('provenance counterexamples pass',
          len(final['classification_controls']) == 8 and
          all(r['passed'] for r in final['classification_controls']))
    check('all initially holding-country capitals remain consistent',
          final['raw_qualification']['capital_classification_counts'] ==
          {'consistent_default_capital': 642, 'consistent_explicit_history_capital': 4})
    check('map reader finds only the thirteen retained raw conflicts',
          m['finding_counts'] == {'multiple_initial_province_allocations': 13})
    check('no newly unresolved literal country target RSR',
          not any(r['target'] == 'RSR' for r in m['script_literal_dependency_candidates']))
    check('no unallocated land or unresolved authored POP culture',
          not m['unallocated_passable_province_candidates'] and not m['initial_pop_culture_candidates'])
    check('mod/native/qualification parsers report no error',
          not (m['parse_errors'] + native['parse_errors'] + final['parse_errors']))
    check('journal dependency handoff retains zero findings',
          je['counts'] == {'journals': 494, 'findings': 0} and not je['findings'])
    check('DLC gate inventory has no unknown feature vocabulary',
          len(m['dlc_gate_inventory']) == 286 and
          all(r['classification'] == 'native-vocabulary' for r in m['dlc_gate_inventory']))
    check('no dormant RSR initial state created',
          not any(r['country'] == 'RSR' for r in m['initial_state_allocations'])
          and m['counts']['initial_owners'] == 646)
    for s in rsr['specs']:
        path = ROOT / s['path']
        nodes = parse(path.read_text(encoding='utf-8-sig'))
        check(s['category'] + ' RSR provider matches validated native object',
              sha(path) == s['candidate_sha256'] and len(nodes) == 1 and
              ast(nodes[0]) == ast(parse(s['native_object'])[0]) and
              sha(GAME / s['source']) == s['source_sha256'])
    old = base['runtime_hashes']
    changed = [rel for rel, digest in old.items()
               if not (ROOT / rel).is_file() or sha(ROOT / rel) != digest]
    check('only the approved existing runtime path changed', changed == [shared], changed=changed)
    current = {p.relative_to(ROOT).as_posix() for folder in
               ['common', 'events', 'map_data', 'localization', 'gui', 'gfx', '.metadata']
               for p in (ROOT / folder).rglob('*') if p.is_file()}
    added = sorted(current - set(old))
    check('only three isolated RSR runtime providers added',
          added == sorted(s['path'] for s in rsr['specs']), added=added)
    check('all authored POP source bytes preserved',
          all(sha(ROOT / rel) == digest for rel, digest in old.items()
              if rel.startswith('common/history/pops/')))
    check('map pixels and resource/state definitions preserved',
          all(sha(ROOT / rel) == digest for rel, digest in old.items()
              if rel.startswith('map_data/')))
    check('journal and event implementations preserved',
          all(sha(ROOT / rel) == digest for rel, digest in old.items()
              if rel.startswith(('common/journal_entries/', 'events/'))))
    check('native baseline input bytes unchanged',
          all(sha(GAME / rel) == digest for rel, digest in base['native_hashes'].items()))
    # Validate the actual current scan inputs, including newly added providers.
    source_hashes = {**m['source_hashes'], **native['source_hashes'], **final['source_hashes']}
    drift = []
    for key, digest in source_hashes.items():
        origin, rel = key.split('/', 1)
        path = (GAME if origin == 'native' else ROOT) / rel
        if not path.is_file() or sha(path) != digest:
            drift.append(key)
    check('all current audit inputs still match scanned bytes', not drift, drift=drift)
    check('Git index retained without change',
          '.git/index' not in old or sha(ROOT / '.git/index') == old['.git/index'])
    check('new locale candidates not installed', all(
          not (ROOT / s['path']).exists() for s in
          read('RUSSIAN_CIVIL_WAR_PROVIDER/CONTRACT.json')['specs']
          if s['category'].startswith('localization')))
    return dict(status='PASS_STATIC_ONLY' if all(r['passed'] for r in checks) else 'FAIL_STATIC',
                passed=sum(r['passed'] for r in checks), total=len(checks), checks=checks,
                protected_existing_runtime_inputs=len(old), current_scanned_inputs=len(source_hashes),
                engine_tested=False, parent24_closed=False, parent19_closed=False,
                limits=['Raw native-parity ownership conflicts remain unresolved historical/runtime questions.',
                        'No scope execution, DLC on/off runtime or complete journal acceptance is inferred.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    path = args.output.resolve()
    if path.parent != LOT or path.exists():
        parser.error('Use a new result file in this delivery folder.')
    result = validate()
    with path.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({k: result[k] for k in ['status', 'passed', 'total',
                      'protected_existing_runtime_inputs', 'current_scanned_inputs']}))
    print(json.dumps([r for r in result['checks'] if not r['passed']]))
    if result['status'] != 'PASS_STATIC_ONLY':
        raise SystemExit(1)
