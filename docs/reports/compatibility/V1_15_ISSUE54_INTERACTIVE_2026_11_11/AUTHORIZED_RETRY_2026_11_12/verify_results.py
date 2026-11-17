"""Read-only checks for the completed, interactive series; never launches a game."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone, timedelta

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools/compatibility'))
from issue54_interactive_lab import LAB, REPORT, evaluator

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    checks = []
    def check(name, ok, **details):
        checks.append(dict(name=name, passed=bool(ok), **details))
    plan = read(HERE / 'PLAN.json')
    check('executable_unchanged', sha(Path(plan['executable'])) == plan['executable_sha256'])
    captures = read(HERE / 'CAPTURE_SUMMARIES.json')
    controlled = [c for c in captures if c['controlled']]
    expected = {(t, p, c) for t in plan['order'] for p, c in
                [('closed_paused', 'none'), ('tree_stationary', 'production'),
                 ('tree_stationary', 'military'), ('tree_stationary', 'society'),
                 ('tree_pan', 'society')]}
    check('twenty_controlled_ui_captures', len(controlled) == 20 and
          {(c['trial'], c['phase'], c['category']) for c in controlled} == expected)
    check('no_startup_cpu_capture', all(not c['startup_benchmark'] for c in captures))
    check('cpu_capture_lengths_and_samples', all(15 <= c['seconds_actual'] < 20 and
          c['samples'] == 15 and c['logical_processors'] == 16 for c in controlled))
    check('cpu_values_finite_and_plausible', all(0 < c['cpu_machine_weighted_percent'] < 100 for c in controlled))
    check('same_test_save', sha(Path(read(HERE / 'SAVE_BASELINE.json')['path'])) ==
          'e6abb3c2305036855a11db308657164f71cecca29002ac6fdc7822c66fd24791')
    dlcs, runs = {}, []
    for trial in plan['order']:
        all_paths = sorted(HERE.glob(trial + '_*/LAUNCH.json'))
        paths = [p for p in all_paths if list((p.parent / 'measurements').glob('*_fixed_*_metadata.json'))]
        check(trial + '_one_measured_launch', len(paths) == 1,
              unmeasured_attempts_retained=[p.parent.name for p in all_paths if p not in paths])
        if len(paths) != 1:
            continue
        launch_path = paths[0]
        launch = read(launch_path)
        run = launch_path.parent
        runs.append(launch)
        check(trial + '_owned_process_exited', (run / 'EXIT.json').is_file())
        check(trial + '_same_executable_profile', launch['executable_sha256'] == plan['executable_sha256'] and
              launch['profile'] == plan['shared_profile'] and not launch['startup_cpu_benchmark'])
        # The game rotates previous sessions into this same profile. Match the
        # launch clock instead of mixing historical DLC lists into this run.
        started = datetime.fromisoformat(launch['started_utc'].replace('Z', '+00:00'))
        local_start = started.astimezone(timezone(timedelta(hours=1)))
        matched_logs = []
        for path in sorted((run / 'logs').glob('debug*.log')):
            text = path.read_text(encoding='utf-8-sig', errors='replace')
            first = re.search(r'^\[(\d{2}):(\d{2}):(\d{2})\]', text)
            if not first:
                continue
            clock = local_start.replace(hour=int(first[1]), minute=int(first[2]), second=int(first[3]), microsecond=0)
            if abs((clock-local_start).total_seconds()) <= 5:
                matched_logs.append((path.name, text))
        check(trial + '_launch_log_matched', len(matched_logs) == 1,
              files=[name for name, _ in matched_logs])
        logs = '\n'.join(text for _, text in matched_logs)
        dlcs[trial] = sorted(set(re.findall(r'Mounted Data:.*?[/\\]game[/\\](dlc[/\\][^\r\n]+)', logs)))
        check(trial + '_DLC_mount_evidence_present', bool(dlcs[trial]), mounted=dlcs[trial])
        pan = next(c for c in controlled if c['trial'] == trial and c['phase'] == 'tree_pan')
        stamp = read(HERE / 'images' / (trial + '_fixed_society_pan_step1.json'))['utc']
        instant = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        check(trial + '_drag_observed_within_capture',
              datetime.fromisoformat(pan['started_utc'].replace('Z', '+00:00')) <= instant <=
              datetime.fromisoformat(pan['ended_utc'].replace('Z', '+00:00')))
    check('same_effectively_mounted_DLCs', len(dlcs) == 4 and len({tuple(v) for v in dlcs.values()}) == 1)
    check('four_distinct_owned_processes', len({r['process_id'] for r in runs}) == 4)
    manifest = read(LAB / 'evidence/FROZEN_MANIFEST.json')['files']
    for arm in ['A_current', 'B_vanilla_gui', 'C_simplified_gui']:
        folder = LAB / arm
        expected_files = set(manifest) - ({'gui/tech_tree.gui'} if arm == 'B_vanilla_gui' else set())
        actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
        changed = [f for f in expected_files if not (folder / f).is_file() or sha(folder / f) != manifest[f]['sha256']]
        check(arm + '_file_set', actual == expected_files)
        check(arm + '_bounded_changes', changed == (['gui/tech_tree.gui'] if arm == 'C_simplified_gui' else []), changed=changed)
    prep = read(REPORT / 'PREPARATION.json')
    graph = read(LAB / 'evidence/MOD_GRAPH.json')['nodes']
    raw = (LAB / 'C_simplified_gui/gui/tech_tree.gui').read_text(encoding='utf-8-sig')
    restored = raw
    for spec in prep['visibility_comparison']:
        before, after = evaluator(spec['before']), evaluator(spec['after'])
        failures = [(key, shown) for key in list(graph) + ['__unknown_technology__'] for shown in [False, True]
                    if before(key, shown) != after(key, shown)]
        check(spec['kind'] + '_truth_table', not failures, cases=2*(len(graph)+1))
        check(spec['kind'] + '_single_span', restored.count(spec['after']) == 1)
        restored = restored.replace(spec['after'], spec['before'], 1)
    check('C_only_two_expression_changes', restored == (LAB / 'A_current/gui/tech_tree.gui').read_text(encoding='utf-8-sig'))
    baseline = read(REPORT / 'NORMAL_INPUTS_BEFORE.json')
    drift = [p for p, h in baseline.items() if not Path(p).is_file() or sha(Path(p)) != h]
    app_state = [p for p in drift if Path(p).name in ['launcher-v2.sqlite', 'pdx_settings.json']]
    product_drift = [p for p in drift if p not in app_state]
    check('normal_product_and_git_index_preserved', not product_drift, changed=product_drift,
          baseline_inputs=len(baseline), application_state_drift=app_state)
    result = dict(utc=datetime.now(timezone.utc).isoformat(), checks=checks,
                  passed=sum(c['passed'] for c in checks), total=len(checks),
                  mounted_dlcs=dlcs, startup_cpu_benchmarks=0,
                  exact_input_latency_measured=False, frame_time_distribution_measured=False,
                  C_runtime_tested=False, performance_fix_installed=False)
    output = HERE / 'FINAL_VALIDATION.json'
    if output.exists():
        raise SystemExit('Retain the prior receipt; choose a new output before repeating.')
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(dict(passed=result['passed'], total=result['total'], findings=[c for c in checks if not c['passed']]), indent=2))

if __name__ == '__main__':
    main()
