"""Read-only TECH-R3 resumption; all new evidence stays in this directory."""
import collections
import contextlib
import io
import json
import os
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import audit_starting_tech_1776_r3 as a

OUT = Path(__file__).resolve().parent
ORIGINAL = a.OUT
os.environ['GIT_OPTIONAL_LOCKS'] = '0'


def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def changes(before, after):
    return {p: {'before': before.get(p), 'after': after.get(p)}
            for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)}


def git_state():
    return {'head': a.git('rev-parse', 'HEAD'), 'branch': a.git('branch', '--show-current'),
            'index': a.sha(ROOT / '.git/index'), 'status': a.git('status', '--porcelain')}


def manifest_review(path, files):
    return {'manifest': path.relative_to(ROOT).as_posix(), 'files': len(files),
            'differences': {p: {'expected': h, 'current': a.sha(ROOT / p) if (ROOT / p).is_file() else None}
                            for p, h in files.items()
                            if not (ROOT / p).is_file() or a.sha(ROOT / p) != h}}


def main():
    assert not (OUT / 'ENTRY.json').exists(), 'Use a new review directory for another execution.'
    stamp = datetime.now(timezone.utc).isoformat()
    protected = {}
    for folder in [a.r1.OUT, a.r2.OUT, ORIGINAL, a.r1.rm.OUT,
                   ROOT / 'docs/reports/map/WORLD_1776_CLOSURE',
                   ROOT / 'docs/reports/economy/ALLOYS_1776_REBALANCE']:
        protected.update(a.proof_hashes(folder))
    current = a.r1.runtime.runtime_hashes()
    start_git = git_state()
    old = a.load(ORIGINAL / 'SESSION_AFTER_STATIC.json')['hashes']
    delivered = a.load(ORIGINAL / 'FILES_MODIFIED.json')['sha256']
    dump('ENTRY.json', {'recorded_on': '2026-10-25', 'started_at_utc': stamp,
                        'git': start_git, 'functional_hashes': current,
                        'protected_proofs': protected,
                        'functional_delta_since_last_R3_static': changes(old, current),
                        'R3_owned': manifest_review(ORIGINAL / 'FILES_MODIFIED.json', delivered),
                        'R3_historical_git': a.load(ORIGINAL / 'BASELINE.json')['git']})
    print('Entry recorded; R3 own files:', len(delivered), '; post-delivery functional delta:', len(changes(old, current)), flush=True)

    # Existing static checker has report side effects. Redirect its outputs;
    # leave all reads pointing at the immutable historical delivery.
    original_dump = a.dump
    original_write = Path.write_bytes

    def routed_dump(name, obj, base=None):
        assert base is None or base == ORIGINAL, ('Unexpected output base', base)
        dump(name, obj)

    def guarded_write(path, data):
        if path.parent == ORIGINAL:
            return original_write(OUT / path.name, data)
        if path.is_relative_to(OUT):
            return original_write(path, data)
        raise RuntimeError('Unexpected checker write: ' + str(path))

    a.dump = routed_dump
    Path.write_bytes = guarded_write
    stream = io.StringIO()
    try:
        with contextlib.redirect_stdout(stream):
            a.static()
    except AssertionError:
        print('Static check has failures; see isolated TEST_RESULTS.json', flush=True)
    finally:
        a.dump = original_dump
        Path.write_bytes = original_write
        (OUT / 'STATIC.log').write_text(stream.getvalue(), encoding='utf-8')
    static = a.load(OUT / 'TEST_RESULTS.json')
    print('Static:', static['passed'], '/', static['total'], flush=True)

    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromName('test_starting_tech_audit_1776_r3'))
    (OUT / 'TARGETED_TESTS.log').write_text(stream.getvalue(), encoding='utf-8')
    failures = [{'id': t.id(), 'traceback': trace} for t, trace in result.failures + result.errors]
    targeted = {'total': result.testsRun, 'passed': result.testsRun - len(failures) - len(result.skipped),
                'failed': failures, 'skipped': [{'id': t.id(), 'reason': why} for t, why in result.skipped],
                'automated_engine_test': False}
    dump('TARGETED_TESTS.json', targeted)
    print('Targeted:', targeted['passed'], '/', targeted['total'], flush=True)

    snapshot = a.contract.collect_snapshot()
    audits = [a.contract.audit_country(tag, snapshot) for tag in sorted(snapshot['starts'])]
    dump('CURRENT_COUNTRY_AUDIT.json', audits)
    codes = collections.Counter(f['code'] for row in audits for f in row['findings'])
    dump('CURRENT_AUDIT_SUMMARY.json', {
        'countries': len(audits), 'codes': dict(sorted(codes.items())),
        'focus_scopes': {name: sum(k[2] in kinds for k in snapshot['selected']) for name, kinds in a.FOCUS.items()},
        'alloy_parents': snapshot['graph']['alloysworking'],
        'country_counts': {t: len(snapshot['starts'][t]['technologies']) for t in ['PRU', 'TUS', 'RAG']},
        'selection_model': 'Last explicit method per group; no engine activity inferred.',
        'runtime_tested': False})

    econ_path = ROOT / 'docs/reports/economy/ALLOYS_1776_REBALANCE/FILES_MODIFIED.json'
    econ = a.load(econ_path)
    econ_files = {r['path']: r['sha256'] for r in econ['files']}
    world_path = ROOT / 'docs/reports/map/WORLD_1776_CLOSURE/BALKANS-02/FILES_MODIFIED.json'
    world_files = {r['file']: r['after'] for r in a.load(world_path)}
    dump('CURRENT_PEER_MANIFESTS.json', {
        'ECON': manifest_review(econ_path, econ_files),
        'WORLD_BALKANS02': manifest_review(world_path, world_files),
        'peer_human_validation_created': False})

    current_after = a.r1.runtime.runtime_hashes()
    proof_after = {p: a.sha(ROOT / p) if (ROOT / p).is_file() else None for p in protected}
    end_git = git_state()
    checks = {
        'R3_eight_delivered_files_exact': all(current_after.get(p) == h for p, h in delivered.items()),
        'No_functional_delta_since_R3_latest_static': not changes(old, current_after),
        'No_functional_file_changed_during_review': not changes(current, current_after),
        'All_prior_proofs_and_peer_documentation_preserved': not changes(protected, proof_after),
        'Git_head_branch_index_preserved_during_review': all(start_git[k] == end_git[k] for k in ['head', 'branch', 'index']),
        'Static_checks_pass': static['status'] == 'PASS',
        'Targeted_checks_pass': result.wasSuccessful(),
        'R1_R2_remain_user_validated': all(a.load(p / 'AUDIT_STATE.json')['status'] == 'PASS_RUNTIME_USER_VALIDATED' for p in [a.r1.OUT, a.r2.OUT]),
        'R3_pending_without_human_receipt': a.load(ORIGINAL / 'AUDIT_STATE.json')['status'] == 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and not list(ORIGINAL.glob('RUNTIME_USER_ATTESTATION*')),
        'Alloy_parents_preserved': set(snapshot['graph']['alloysworking']) == {'shaft_mining', 'organized_workshops'},
        'R4_not_started_by_review': not a.load(ORIGINAL / 'AUDIT_STATE.json')['R4_started'],
    }
    dump('FINAL_CHECKS.json', {'status': 'PASS' if all(checks.values()) else 'FAIL',
                             'passed': sum(checks.values()), 'total': len(checks), 'checks': checks,
                             'functional_changes_during_review': changes(current, current_after),
                             'prior_proof_changes': changes(protected, proof_after),
                             'git_after': end_git, 'ended_at_utc': datetime.now(timezone.utc).isoformat(),
                             'automated_engine_test': False, 'human_validation': None,
                             'cumulative_suite_rerun': False})
    print('Final:', sum(checks.values()), '/', len(checks), flush=True)
    return int(not all(checks.values()))


if __name__ == '__main__':
    sys.exit(main())
