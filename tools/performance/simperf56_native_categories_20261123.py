"""Separate 1.15.2 lab: supported native economic switches, immutable old trials."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, copy, hashlib, json, shutil, subprocess

ROOT = Path(__file__).resolve().parents[2]
PREVIOUS = Path('C:/Users/simeo/AppData/Local/Temp/aor56_ai_20261117')
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor56_native_20261123')
REPORT = ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/NATIVE_CATEGORIES_2026_11_23'
KEYS = ('PRODUCTION_BUILDING_CONSTRUCTION_ENABLED', 'AUTONOMOUS_INVESTMENT_CONSTRUCTION_ENABLED', 'GOVERNMENT_MONEY_SPENDING_ENABLED')

def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8') as f: json.dump(value, f, indent=2, ensure_ascii=False)

def init():
    assert not LAB.exists() and not REPORT.exists(), 'Do not replace an existing experiment.'
    old = read(PREVIOUS/'PREPARATION.json')
    base = old['profiles']['ECNC2']
    runs = list((PREVIOUS/'runs').glob('ECNC2_*')); assert len(runs) == 1
    settings = (runs[0]/'SETTINGS.json').read_bytes()
    assert hashlib.sha256(settings).hexdigest() == base['settings_sha256']
    seed = Path(base['seed_path']); assert sha(seed) == base['common_save_sha256']
    LAB.mkdir(); REPORT.mkdir(); (LAB/'requests').mkdir(); (LAB/'evidence').mkdir()
    inherited = read(PREVIOUS/'ECONOMIC_PRESERVATION_BEFORE_20261118.json')
    groups = {k: {p: sha(p) for p in paths} for k, paths in inherited['groups'].items()}
    for name, folder in [('all_previous_reports', REPORT.parent), ('all_previous_tools', ROOT/'tools/performance')]:
        groups[name] = {str(p): sha(p) for p in folder.rglob('*') if p.is_file() and REPORT not in p.parents}
    plan = copy.deepcopy(old); plan.update(lab=str(LAB), executable_sha256=sha(old['executable']), profiles={})
    baseline = dict(utc=datetime.now(timezone.utc).isoformat(), groups=groups,
        previous_executable_sha256=old['executable_sha256'], current_executable_sha256=plan['executable_sha256'],
        reference_head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'], cwd=ROOT, text=True).strip())
    write(LAB/'PRESERVATION_BEFORE.json', baseline)
    controls = LAB/'common_capture_controls'
    shutil.copytree(base['control_overlay'], controls)
    # This display is shared by all cases and disappears throughout simulation.
    panel = '''\nwindow = {
 name = "sim56_native_switch_values"
 layer = layer_ingame_hud
 position = { 700 260 }
 size = { 650 90 }
 visible = "[IsGamePaused]"
 filter_mouse = none
 vbox = {
  text_single = { text = "PUBLIC [GetDefine('NAI','PRODUCTION_BUILDING_CONSTRUCTION_ENABLED')]" }
  text_single = { text = "PRIVATE [GetDefine('NAI','AUTONOMOUS_INVESTMENT_CONSTRUCTION_ENABLED')]" }
  text_single = { text = "SPENDING [GetDefine('NAI','GOVERNMENT_MONEY_SPENDING_ENABLED')]" }
 }
}
'''
    (controls/'gui/sim56_native_switch_values.gui').write_text(panel, encoding='utf-8')
    cases = [('NPC1',None), ('NPU1',KEYS[0]), ('NPV1',KEYS[1]), ('NGM1',KEYS[2]), ('NPC2',None)]
    for label, disabled in cases:
        profile = LAB/'profiles'/label; (profile/'save games').mkdir(parents=True)
        target = profile/'save games'/seed.name; shutil.copyfile(seed, target)
        assert sha(target) == base['common_save_sha256']
        (profile/'pdx_settings.json').write_bytes(settings)
        shutil.copytree(Path(base['path'])/'user_bindings', profile/'user_bindings')
        overlay = LAB/'switches'/label; (overlay/'common/defines').mkdir(parents=True)
        define_text = 'NAI = {\n' + ''.join('    '+key+' = '+('no' if key == disabled else 'yes')+'\n' for key in KEYS) + '}\n'
        define_path = overlay/'common/defines/zzzz_sim56_native_categories.txt'
        define_path.write_text(define_text, encoding='utf-8')
        content = read(runs[0]/'CONTENT_LOAD.json')
        # Keep the frozen mod and old common telemetry, replacing only capture controls.
        content['enabledMods'][2]['path'] = controls.as_posix()
        content['enabledMods'].append(dict(path=overlay.as_posix()))
        write(profile/'content_load.json', content)
        spec = copy.deepcopy(base)
        spec.update(path=str(profile), seed_path=str(target), mods=[x['path'] for x in content['enabledMods']],
            native_disabled_define=disabled, native_define_file=str(define_path), native_define_sha256=sha(define_path),
            comparison_group='native_categories_1.15.2_20261123', control_overlay=str(controls),
            setup_proof=str(LAB/'SETUP.json'), expected_enabled='yes', gameplay_preserving=disabled is None)
        plan['profiles'][label] = spec
    shutil.copyfile(PREVIOUS/'run_profile_trial.ps1', LAB/'run_profile_trial.ps1')
    write(LAB/'PREPARATION.json', plan)
    write(LAB/'SETUP.json', dict(utc=baseline['utc'], plan=str(LAB/'PREPARATION.json'),
        executable=plan['executable'], executable_sha256=plan['executable_sha256'],
        old_results_not_pooled=True, common_source_sha256=base['common_save_sha256'],
        native_treatment_not_runtime_verified_yet=True, order=[x[0] for x in cases],
        definitions_reference='C:/Games/Victoria 3/game/common/defines/00_ai.txt:17,35,36',
        installed_steam_definitions_checked=True,
        diagnostic_scope='Only one persistent native economic switch per treatment; no controller, country, POP, history or recipe removed. No production optimization claimed.'))
    write(REPORT/'LAB_LOCATION.json', dict(lab=str(LAB), baseline=str(LAB/'PRESERVATION_BEFORE.json')))
    print(json.dumps(dict(lab=str(LAB), profiles=list(plan['profiles']), executable_sha256=plan['executable_sha256']), indent=2))

def audit():
    before = read(LAB/'PRESERVATION_BEFORE.json')
    result = dict(utc=datetime.now(timezone.utc).isoformat(), groups={})
    for name, paths in before['groups'].items():
        changes = [p for p,h in paths.items() if not Path(p).is_file() or sha(p) != h]
        result['groups'][name] = dict(checked=len(paths), changes=changes)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    write(REPORT/('PRESERVATION_AFTER_'+stamp+'.json'), result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('action', choices=('init','audit'))
    args = ap.parse_args(); init() if args.action == 'init' else audit()
