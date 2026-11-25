"""Isolated paused-frame animation: test capture recovery without OS workarounds."""
from pathlib import Path
import copy, hashlib, json, shutil
from simperf56_ai_cohorts import LAB

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
planpath=LAB/'PREPARATION.json';before=planpath.read_bytes();plan=json.loads(before)
overlay=LAB/'pause_capture_probe_20261119';assert not overlay.exists()
gui=overlay/'gui/sim56_paused_capture.gui';gui.parent.mkdir(parents=True)
gui.write_text('''# LAB ONLY: animate only while paused; hidden throughout simulation windows.
window = {
 name = "sim56_paused_capture_probe"
 layer = layer_ingame_hud
 size = { 16 16 }
 position = { 700 150 }
 filter_mouse = none
 visible = "[IsGamePaused]"
 icon = {
  size = { 16 16 }
  texture = "gfx/interface/animation/rotate_glow_overlay.dds"
  state = { trigger_on_create = yes name = dim next = bright duration = 0.75 alpha = 0.2 }
  state = { name = bright next = dim duration = 0.75 alpha = 0.8 }
 }
}
''',encoding='utf-8')
specs={}
for label,parent in [('SCORP1','SCORG2'),('ECNP1','ECNG2'),
                     ('VAN_OFFP1','VAN_OFFG1'),('VAN_ONP1','VAN_ONG1')]:
    assert label not in plan['profiles'];old=plan['profiles'][parent]
    profile=LAB/'profiles'/label;assert not profile.exists()
    source=Path(old['seed_path']);assert sha(source)==old['common_save_sha256']
    (profile/'save games').mkdir(parents=True);seed=profile/'save games'/source.name
    shutil.copyfile(source,seed)
    setting_source=LAB/'profiles/ECNG2/pdx_settings.json'
    assert sha(setting_source)==old['settings_sha256']
    shutil.copyfile(setting_source,profile/'pdx_settings.json')
    shutil.copytree(Path(old['path'])/'user_bindings',profile/'user_bindings')
    content=json.loads((Path(old['path'])/'content_load.json').read_text(encoding='utf-8-sig'))
    at=len(old['mods'])-int(label.startswith('SCOR'))
    content['enabledMods'].insert(at,{'path':overlay.as_posix()})
    (profile/'content_load.json').write_text(json.dumps(content,indent=2),encoding='utf-8')
    spec=copy.deepcopy(old);mods=spec['mods'].copy();mods.insert(at,overlay.as_posix())
    spec.update(path=str(profile),seed_path=str(seed),mods=mods,
                pause_capture_probe=str(gui),
                comparison_group='pulse_mod_pair_20261119' if old['expected_year']==1776 else 'pulse_vanilla_OFF_ON_20261119')
    specs[label]=spec;plan['profiles'][label]=spec
with (LAB/'PAUSE_CAPTURE_PLAN_BEFORE_20261119.json').open('xb') as f:f.write(before)
assert planpath.read_bytes()==before
planpath.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'PAUSE_CAPTURE_SETUP_20261119.json').open('x',encoding='utf-8') as f:
    json.dump(dict(overlay=str(overlay),gui_sha256=sha(gui),profiles=specs,
                   operation='Native GUI alpha animation only while IsGamePaused; no keyboard injection or OS helper.',
                   not_yet_runtime_verified=True,hidden_when_running_declared_not_yet_observed=True,
                   source_and_common_telemetry_preserved=True,
                   SCORG2='Preparation reached Jan2 and camera changed before planned start; no performance result accepted.'),f,indent=2)
print(json.dumps({'profiles':list(specs),'gui':str(gui),'runtime_verification_required':True}))
