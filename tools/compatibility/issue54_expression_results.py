"""Consolidate actual UI-only expression trials; no launch or input automation."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE54_EXPRESSIONS_2026_11_12'


def run():
    plan = json.loads((REPORT / 'PLAN.json').read_text(encoding='utf-8'))
    observations = {v['id']: v for v in json.loads((REPORT / 'FPS_OBSERVATIONS.json').read_text())}
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    checks, rows = [], []
    def check(name, passed, **detail):
        checks.append(dict(check=name, passed=bool(passed), **detail))
    for trial in ('EDGE_OFF_1', 'CARD_OFF_1', 'BOTH_OFF_1', 'OPTIMIZED_1R', 'COMPACT_1', 'CONTROL_REPEAT', 'COMPACT_2'):
        runs = [p for p in REPORT.glob(trial + '_*') if p.is_dir() and (p / 'LAUNCH.json').is_file()]
        check(trial + '_single_run', len(runs) == 1)
        if len(runs) != 1:
            continue
        folder = runs[0]
        launch = json.loads((folder / 'LAUNCH.json').read_text(encoding='utf-8-sig'))
        check(trial + '_pinned_inputs', launch['executable_sha256'] == plan['executable_sha256'] and
              launch['settings_sha256'] == plan['settings_sha256'] and
              sha(folder / 'SETTINGS.json') == plan['settings_sha256'] and
              sha(folder / 'tech_tree.gui') == launch['gui_sha256'])
        check(trial + '_completed', (folder / 'EXIT.json').is_file())
        error_path = folder / 'logs/error.log'
        errors = error_path.read_text(encoding='utf-8-sig', errors='replace') if error_path.exists() else ''
        gui_errors = [line for line in errors.splitlines() if re.search(
            r'gui[/\\]tech_tree\.gui|TechTree|Technology\.IsResearchable|GetKey', line)]
        check(trial + '_no_technology_gui_errors', not gui_errors, error_count=len(gui_errors))
        encoding_debt = [line for line in errors.splitlines() if 'lexer.cpp' in line and 'tech_tree_' in line]
        check(trial + '_encoding_debt_classified', all('utf8-bom encoding' in line for line in encoding_debt),
              preexisting_technology_named_script_encoding_warnings=len(encoding_debt))
        # debug.log rotates while loading; use the segment containing this probe
        # mount, rather than inherited historical debug segments from the profile.
        segments = [p.read_text(encoding='utf-8-sig', errors='replace') for p in (folder / 'logs').glob('debug*.log')]
        current = [s for s in segments if 'Mounted Data: ' + plan['probe'].replace('\\', '/') in s]
        dlc = sorted({line.strip() for segment in current for line in segment.splitlines()
                      if re.fullmatch(r'[^|]+\|dlc/[^|]+\.dlc', line.strip())})
        check(trial + '_same_effective_dlc', dlc == ['Victoria 2 Remastered Soundtrack|dlc/dlc001_preorder/dlc001.dlc'], effective_dlc=dlc)
        for suffix, phase, category in [('closed', 'closed_paused', 'none'),
                                        ('production', 'tree_stationary', 'production'),
                                        ('military', 'tree_stationary', 'military'),
                                        ('society', 'tree_stationary', 'society'),
                                        ('pan', 'tree_pan', 'society')]:
            prefix = folder / 'measurements' / (trial + '_' + suffix)
            metadata = Path(str(prefix) + '_metadata.json')
            check(trial + '_' + suffix + '_captured', metadata.is_file())
            if not metadata.is_file():
                continue
            meta = json.loads(metadata.read_text(encoding='utf-8-sig'))
            check(trial + '_' + suffix + '_ui_state_and_duration',
                  meta['phase'] == phase and meta['category'] == category and
                  14.8 <= meta['seconds_actual'] <= 18 and not meta['startup_benchmark'] and
                  (REPORT / meta['ui_state_evidence']).is_file())
            samples = list(csv.DictReader(Path(str(prefix) + '_cpu.csv').open(encoding='utf-8-sig')))
            number = lambda s: float(s.replace(',', '.'))
            seconds = sum(number(s['interval_s']) for s in samples)
            cpu_s = sum(number(s['cpu_delta_ms']) for s in samples) / 1000
            fps = observations.get(trial + '_' + suffix, {})
            check(trial + '_' + suffix + '_actual_samples', len(samples) >= 14 and len(samples) == meta['samples'])
            if suffix != 'closed':
                check(trial + '_' + suffix + '_observed_fps', all(isinstance(fps.get(k), (int, float)) for k in ('fps_before', 'fps_after')))
            rows.append(dict(trial=trial, phase=phase, category=category,
                             seconds=round(seconds, 3), samples=len(samples),
                             cpu_machine_percent=round(100 * cpu_s / seconds / meta['logical_processors'], 3),
                             fps_before=fps.get('fps_before'), fps_after=fps.get('fps_after')))
    lab = Path(plan['probe']).parent
    frozen = json.loads((lab / 'evidence/FROZEN_MANIFEST.json').read_text(encoding='utf-8-sig'))['files']
    probe = Path(plan['probe'])
    drift = [name for name, spec in frozen.items() if name != 'gui/tech_tree.gui' and
             (not (probe / name).is_file() or sha(probe / name) != spec['sha256'])]
    check('all_non_gui_probe_inputs_preserved', not drift, count=len(frozen)-1, drift=drift)
    check('original_working_gui_unchanged', sha(ROOT / 'gui/tech_tree.gui') == plan['base_gui_sha256'])
    return dict(status='PASS' if all(c['passed'] for c in checks) else 'INCOMPLETE_OR_FINDINGS',
                passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                measurements=rows, new_startup_cpu_benchmarks=0,
                fps_kind='Approximate native counter snapshots, not a continuous average',
                exact_frame_time_or_input_latency_measured=False,
                human_validation_claimed=False)


if __name__ == '__main__':
    result = run()
    destination = REPORT / sys.argv[1]
    assert not destination.exists(), 'Retain previous results'
    destination.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
    print(json.dumps([c for c in result['checks'] if not c['passed']], indent=2))
