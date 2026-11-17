"""Analyze primary manual relay files without rewriting any raw measurements.

FPS are user-entered point readings. UI state is declared by the user, not
verified by automated screenshots. Synthetic tests and interrupted runs are
outside the explicitly selected session.
"""
from pathlib import Path
from datetime import datetime, timedelta, timezone
import csv
import difflib
import hashlib
import json
import math
import re

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
SESSION = HERE / 'MANUAL_20261117T000322802Z'
OUT = HERE / 'MANUAL_RESULTS_2026_11_17'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
instant = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
number = lambda s: float(s.replace(',', '.'))

def main():
    if OUT.exists():
        raise SystemExit('Retain previous analysis. Select a new output directory.')
    plan = read(HERE / 'PLAN_MANUAL.json')
    checks, rows, runs, matched_logs = [], [], [], {}
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    check('pinned_executable_current', sha(Path(plan['executable'])) == plan['executable_sha256'])
    check('common_save_current', sha(Path(plan['save'])) == plan['save_sha256'])
    check('isolated_settings_current', sha(Path(plan['profile']) / 'pdx_settings.json') == plan['settings_sha256'])
    specs = [('closed_paused', 'none'), ('tree_stationary', 'production'),
             ('tree_stationary', 'military'), ('tree_stationary', 'society'), ('tree_pan', 'society')]
    previous_end = None
    for trial in plan['order']:
        folder, spec = SESSION / trial, plan['trials'][trial]
        launch, exit_record = read(folder / 'LAUNCH.json'), read(folder / 'EXIT.json')
        start, end = instant(launch['started_utc']), instant(exit_record['ended_utc'])
        runs.append(dict(launch, ended_utc=exit_record['ended_utc'], exit_code=exit_record['exit_code']))
        check(trial + '_expected_variant_and_hashes', launch['trial'] == trial and
              launch['variant'] == spec['variant'] and launch['gui_sha256'] == spec['gui_sha256'] and
              launch['executable_sha256'] == plan['executable_sha256'] and
              launch['save_sha256'] == plan['save_sha256'] and not launch['startup_cpu_benchmark'])
        check(trial + '_GUI_still_matches', sha(Path(spec['mod']) / 'gui/tech_tree.gui') == spec['gui_sha256'])
        check(trial + '_same_saved_settings', sha(folder / 'SETTINGS.json') == plan['settings_sha256'])
        check(trial + '_serial_process_lifetime', end > start and (previous_end is None or start > previous_end))
        previous_end = end
        check(trial + '_no_interruption_or_capture_error', not list(folder.glob('INTERRUPTED*')) and
              not list(folder.glob('CAPTURE_ERROR*')))
        local_start = start.astimezone(timezone(timedelta(hours=1)))
        segments = []
        for log in sorted((folder / 'logs').glob('debug*.log')):
            text = log.read_text(encoding='utf-8-sig', errors='replace')
            clock = re.search(r'^\[(\d{2}):(\d{2}):(\d{2})\]', text)
            if not clock:
                continue
            log_start = local_start.replace(hour=int(clock[1]), minute=int(clock[2]), second=int(clock[3]), microsecond=0)
            if abs((log_start - local_start).total_seconds()) <= 5:
                segments.append((log.name, text))
        check(trial + '_one_matching_launch_log', len(segments) == 1, names=[s[0] for s in segments])
        startup_text = '\n'.join(s[1] for s in segments)
        mounts = re.findall(r'Mounted Data: ([^\r\n]+)', startup_text)
        expected_mod = spec['mod'].replace('\\', '/')
        mod_mounts = [m for m in mounts if '/aor1776_techperf54_20261111/' in m]
        dlcs = sorted(set(re.findall(r'Mounted Data: .*?/game/(dlc/[^\r\n]+)', startup_text)))
        check(trial + '_actual_mod_mount', mod_mounts == [expected_mod], mounted=mod_mounts)
        check(trial + '_actual_DLC_mask', dlcs == ['dlc/dlc001_preorder'], mounted=dlcs)
        matched_logs[trial] = dict(files=[s[0] for s in segments], mounted_mods=mod_mounts,
                                   mounted_dlcs=dlcs, steam_api_failure='Failed to initialize Steam' in startup_text)
        error_text = (folder / 'logs/error.log').read_text(encoding='utf-8-sig', errors='replace')
        gui_errors = [s for s in error_text.splitlines() if re.search(r'gui[/\\]tech_tree\.gui|TechTree|Technology\.IsResearchable|GetKey', s)]
        check(trial + '_no_technology_GUI_binding_errors', not gui_errors, lines=gui_errors)
        check(trial + '_five_primary_capture_pairs', len(list(folder.glob('*_metadata.json'))) == 5 and
              len(list(folder.glob('*_cpu.csv'))) == 5)
        phase_end = start
        for phase, category in specs:
            prefix = folder / (phase + '_' + category)
            meta_path = prefix.with_name(prefix.name + '_metadata.json')
            csv_path = prefix.with_name(prefix.name + '_cpu.csv')
            meta = read(meta_path)
            with csv_path.open(encoding='utf-8-sig', newline='') as stream:
                samples = list(csv.DictReader(stream))
            declared, began, ended = map(instant, (meta['ui_state_declaration_utc'], meta['started_utc'], meta['ended_utc']))
            seconds = sum(number(s['interval_s']) for s in samples)
            cpu_ms = sum(number(s['cpu_delta_ms']) for s in samples)
            cpu_percent = 100 * cpu_ms / (1000 * seconds * meta['logical_processors'])
            name = trial + '_' + phase + '_' + category
            check(name + '_real_UI_capture_metadata', meta['trial'] == trial and meta['phase'] == phase and
                  meta['category'] == category and not meta['self_test'] and not meta['startup_benchmark'] and
                  meta['ui_state_verified_by'] == 'User declaration via Mesurer button; no automated screenshot verification')
            check(name + '_handoff_and_lifetime', start < declared < began < ended < end and
                  declared > phase_end and 4.8 <= (began - declared).total_seconds() <= 6)
            phase_end = ended
            check(name + '_duration_samples_and_cpu', 15 <= seconds < 18 and
                  abs(meta['seconds_actual'] - seconds) < 0.1 and len(samples) == meta['samples'] and
                  len(samples) >= 14 and meta['logical_processors'] == 16 and
                  math.isfinite(cpu_percent) and 0 <= cpu_percent <= 100 and
                  all(number(s['interval_s']) > 0 and number(s['cpu_delta_ms']) >= 0 for s in samples))
            check(name + '_stored_CPU_formula', all(abs(number(s['cpu_percent_machine']) -
                  100 * number(s['cpu_delta_ms']) / (1000 * number(s['interval_s']) * meta['logical_processors'])) < 1e-6 for s in samples))
            check(name + '_FPS_manual_snapshot_recorded', isinstance(meta['fps_user_snapshot'], (int, float)) and
                  0 < meta['fps_user_snapshot'] < 1000 and not meta['fps_continuous_mean_measured'] and not meta['input_latency_measured'])
            rows.append(dict(trial=trial, variant=spec['variant'], phase=phase, category=category,
                             seconds=round(seconds, 6), samples=len(samples),
                             cpu_machine_weighted_percent=round(cpu_percent, 6),
                             fps_user_snapshot=meta['fps_user_snapshot'],
                             metadata_sha256=sha(meta_path), csv_sha256=sha(csv_path),
                             metadata=str(meta_path), csv=str(csv_path)))
    check('four_distinct_processes', len({r['process_id'] for r in runs}) == 4)
    check('twenty_genuine_UI_captures', len(rows) == 20)
    lookup = {(r['trial'], r['phase'], r['category']): r for r in rows}
    comparisons = []
    for phase, category in specs:
        values = [lookup[(t, phase, category)] for t in plan['order']]
        comparisons.append(dict(phase=phase, category=category,
            fps={r['trial']: r['fps_user_snapshot'] for r in values},
            cpu_machine_percent={r['trial']: r['cpu_machine_weighted_percent'] for r in values},
            both_compact_readings_above_both_controls=min(values[i]['fps_user_snapshot'] for i in (1,2)) > max(values[i]['fps_user_snapshot'] for i in (0,3))))
    before = Path(plan['trials']['CONTROL1']['mod']) / 'gui/tech_tree.gui'
    candidate = Path(plan['trials']['COMPACT1']['mod']) / 'gui/tech_tree.gui'
    source, after = (p.read_text(encoding='utf-8-sig') for p in (before, candidate))
    expressions = lambda text: [s for s in re.findall(r'visible\s*=\s*"\[([^"\r\n]+)\]"', text) if 'GetTechnology(' in s]
    a, b = expressions(source), expressions(after)
    check('two_visibility_expressions', len(a) == len(b) == 2)
    restored = after
    for old, new in zip(a, b):
        check('single_expression_span_' + str(len(old)), restored.count(new) == 1)
        restored = restored.replace(new, old, 1)
    check('only_two_expression_spans', restored == source)
    check('working_GUI_is_still_control', sha(ROOT / 'gui/tech_tree.gui') == sha(before))
    result = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
                  status='PASS_MEASUREMENT_FILES' if all(c['passed'] for c in checks) else 'FINDINGS',
                  session=str(SESSION), passed=sum(c['passed'] for c in checks), total=len(checks),
                  checks=checks, runs=runs, matched_launch_logs=matched_logs, measurements=rows,
                  comparisons=comparisons, snapshots_are_not_continuous_FPS_averages=True,
                  UI_states_automatically_verified=False, exact_opening_latency_measured=False,
                  frame_time_distribution_measured=False, performance_fix_installed=False,
                  historical_technology_definitions_changed=False,
                  player_feedback=dict(source='User reply to the question in this chat on 2026-11-17',
                                       quote='Aucun problème remarqué', scope='No noticed missing technologies, abnormal links or broken buttons during COMPACT',
                                       exhaustive_functionality_validation=False),
                  expression_text_counts=[dict(kind=k, old_lookups=x.count('GetTechnology('), new_lookups=y.count('GetTechnology('), old_length=len(x), new_length=len(y)) for k,x,y in zip(('edges','cards'),a,b)])
    OUT.mkdir()
    with (OUT / 'ANALYSIS.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
    patch = ''.join(difflib.unified_diff(source.splitlines(keepends=True), after.splitlines(keepends=True),
                    fromfile='a/gui/tech_tree.gui', tofile='b/gui/tech_tree.gui'))
    (OUT / 'COMPACT_REVIEW_ONLY.patch').write_text(patch, encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status','passed','total','comparisons','expression_text_counts')}, indent=2))
    print(json.dumps([c for c in checks if not c['passed']], indent=2))

if __name__ == '__main__':
    main()
