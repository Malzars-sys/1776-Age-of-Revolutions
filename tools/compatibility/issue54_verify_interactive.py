"""Read-only preservation and diagnostic checks; never starts a benchmark."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue54_interactive_lab import ROOT, LAB, OUT, REPORT, EXE, evaluator


def run():
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    plan = json.loads((OUT / 'PREPARATION.json').read_text(encoding='utf-8'))
    baseline = json.loads((REPORT / 'NORMAL_INPUTS_BEFORE.json').read_text(encoding='utf-8'))
    manifest = json.loads((LAB / 'evidence/FROZEN_MANIFEST.json').read_text(encoding='utf-8-sig'))['files']
    graph = json.loads((LAB / 'evidence/MOD_GRAPH.json').read_text(encoding='utf-8-sig'))['nodes']
    checks = []
    def check(name, ok, **detail):
        checks.append(dict(check=name, passed=bool(ok), **detail))
    source_drift = [name for name, digest in baseline.items()
                    if not Path(name).is_file() or sha(Path(name)) != digest]
    check('normal_captured_mod_playsets_settings_index_preserved', not source_drift,
          captured_inputs=len(baseline), changed=source_drift)
    check('same_executable_pinned', sha(EXE) == plan['executable_sha256'])
    expected_a = set(manifest)
    expected_b = expected_a - {'gui/tech_tree.gui'}
    expected_c = expected_a
    for arm, expected in [('A_current', expected_a), ('B_vanilla_gui', expected_b), ('C_simplified_gui', expected_c)]:
        folder = LAB / arm
        actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
        differences = [name for name in expected if not (folder / name).is_file()
                       or sha(folder / name) != manifest[name]['sha256']]
        intended = ['gui/tech_tree.gui'] if arm == 'C_simplified_gui' else []
        check(arm + '_file_set', actual == expected, files=len(actual))
        check(arm + '_only_intended_changes', sorted(differences) == intended, differences=sorted(differences))
    current = (LAB / 'C_simplified_gui/gui/tech_tree.gui').read_bytes()
    raw = current.decode('utf-8-sig')
    recovered = raw
    semantics = []
    for spec in plan['visibility_comparison']:
        old_eval, new_eval = evaluator(spec['before']), evaluator(spec['after'])
        failures = [(key, shown) for key in list(graph) + ['__unknown_technology__']
                    for shown in [False, True] if old_eval(key, shown) != new_eval(key, shown)]
        check(spec['kind'] + '_static_truth_table', not failures, cases=584)
        referenced = set(re.findall(r"GetTechnology\('([^']+)'\)", spec['after']))
        check(spec['kind'] + '_technology_targets_exist', referenced <= set(graph))
        bad = evaluator(spec['after'].replace("'academia'", "'__wrong_alias__'", 1))
        check(spec['kind'] + '_wrong_alias_detected', any(
            old_eval(key, shown) != bad(key, shown) for key in graph for shown in [False, True]))
        assert recovered.count(spec['after']) == 1
        recovered = recovered.replace(spec['after'], spec['before'], 1)
        semantics.append({k: v for k, v in spec.items() if k not in ['before', 'after']})
    restored = (b'\xef\xbb\xbf' if current.startswith(b'\xef\xbb\xbf') else b'') + recovered.encode('utf-8')
    check('diagnostic_only_two_exact_expression_spans', restored == (LAB / 'A_current/gui/tech_tree.gui').read_bytes())
    from issue24_map_dlc_audit import parse
    check('diagnostic_gui_braces_parse', bool(parse(raw)))
    profiles = []
    for spec in plan['trials']:
        profile = Path(spec['profile'])
        load = json.loads((profile / 'content_load.json').read_text(encoding='utf-8'))
        settings = sha(profile / 'pdx_settings.json')
        profiles.append({'trial': spec['trial'], 'settings_sha256': settings,
                         'settings_match_prepared': settings == spec['settings_sha256']})
        check(spec['trial'] + '_correct_isolated_mod', load == {
            'enabledMods': [{'path': spec['mod']}], 'disabledDLC': [], 'enabledUGC': []})
    check('profile_settings_currently_identical', len({p['settings_sha256'] for p in profiles}) == 1,
          profiles=profiles)
    rows = list(csv.DictReader((OUT / 'UI_RESULTS_TO_FILL.csv').open(encoding='utf-8-sig')))
    check('all_measurements_honestly_unmeasured', len(rows) == 28 and all(row['status'] == 'NOT_MEASURED' for row in rows))
    stop = json.loads((OUT / 'CAPABILITIES_AND_STOP.json').read_text())
    check('user_stop_recorded_without_ui_input_or_startup_sampling',
          stop['interactive_test_stopped'] and stop['remaining_victoria_windows_observed'] == 0
          and stop['desktop_input_calls_sent'] == stop['startup_cpu_benchmarks'] == 0)
    check('manual_launcher_copy_matches', sha(OUT / 'Start_UI_Trial.ps1') == sha(ROOT / 'tools/compatibility/issue54_start_ui_trial.ps1'))
    check('manual_sampler_copy_matches', sha(OUT / 'Measure_UI_CPU.ps1') == sha(ROOT / 'tools/compatibility/issue54_measure_ui_cpu.ps1'))
    return {'status': 'PASS_STATIC_ONLY' if all(c['passed'] for c in checks) else 'FINDINGS_STATIC_ONLY',
            'passed': sum(c['passed'] for c in checks), 'total': len(checks), 'checks': checks,
            'visibility_comparison': semantics, 'benchmark_results': None,
            'fps_measured': False, 'frame_timings_measured': False, 'startup_cpu_benchmarks': 0,
            'root_cause_established': False, 'performance_fix_verified': False,
            'limits': ['Static truth tables assume distinct valid technology identities; no engine binding or evaluation-cost proof.',
                       'No interactive measurement or input was completed before the user stopped the attempt.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(REPORT):
        parser.error('Use a new result under this report; retain prior evidence.')
    result = run()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ['checks', 'visibility_comparison']}))
    print([c for c in result['checks'] if not c['passed']])
