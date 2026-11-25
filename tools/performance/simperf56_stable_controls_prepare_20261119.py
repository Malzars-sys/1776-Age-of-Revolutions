"""Contemporary diagnostic/control profiles with stable secondary-screen controls."""
from pathlib import Path
import copy, hashlib, json, shutil
from simperf56_ai_cohorts import LAB, PREVIOUS

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
planpath=LAB/'PREPARATION.json';before=planpath.read_bytes();plan=json.loads(before)
basepath=LAB/'profiles/ECNG2/pdx_settings.json';base=json.loads(basepath.read_bytes())
assert sha(basepath)==plan['profiles']['ECNG2']['settings_sha256']
native=json.loads((LAB/'profiles/SCORP1/pdx_settings.json').read_bytes())
mode=native['System']['screen_edge_scroll_mode'];assert mode=='screen_edge_scroll_mode_disabled'
base['System']['screen_edge_scroll_mode']=mode
settings=json.dumps(base,indent=2,ensure_ascii=False).encode('utf-8');shash=hashlib.sha256(settings).hexdigest()
overlay=LAB/'stable_capture_controls_v2_20261119';assert not overlay.exists()
gui=overlay/'gui/frontend/frontend_ingame_menu.gui';gui.parent.mkdir(parents=True)
source=PREVIOUS/'telemetry_profile/gui/frontend/frontend_ingame_menu.gui'
assert sha(source)=='72732c19a7975194a348b7668c29d0000078d3bb5b8d44367a40e29f65f75d20'
raw=source.read_bytes();old=b'  parentanchor = right|vcenter\r\n  position = { -480 -180 }'
if old not in raw:old=old.replace(b'\r\n',b'\n')
assert raw.count(old)==1
replacement=old.replace(b'right|vcenter',b'top|left').replace(b'{ -480 -180 }',b'{ 700 240 }')
gui.write_bytes(raw.replace(old,replacement))
pulse=LAB/'pause_capture_probe_20261119/gui/sim56_paused_capture.gui'
shutil.copyfile(pulse,overlay/'gui/sim56_paused_capture.gui')
specs={}
pairs=[('SCORC1','SCORG2'),('ECNC1','ECNG2'),('ECNC2','ECNG2'),('SCORC2','SCORG2'),
       ('VAN_OFFC1','VAN_OFFG1'),('VAN_ONC1','VAN_ONG1')]
for label,parent in pairs:
    assert label not in plan['profiles'];oldspec=plan['profiles'][parent]
    profile=LAB/'profiles'/label;assert not profile.exists()
    seed_source=Path(oldspec['seed_path']);assert sha(seed_source)==oldspec['common_save_sha256']
    (profile/'save games').mkdir(parents=True);seed=profile/'save games'/seed_source.name
    shutil.copyfile(seed_source,seed);(profile/'pdx_settings.json').write_bytes(settings)
    shutil.copytree(Path(oldspec['path'])/'user_bindings',profile/'user_bindings')
    content=json.loads((Path(oldspec['path'])/'content_load.json').read_bytes())
    at=len(oldspec['mods'])-int(label.startswith('SCOR'))
    content['enabledMods'].insert(at,{'path':overlay.as_posix()})
    (profile/'content_load.json').write_text(json.dumps(content,indent=2),encoding='utf-8')
    spec=copy.deepcopy(oldspec);mods=spec['mods'].copy();mods.insert(at,overlay.as_posix())
    spec.update(path=str(profile),seed_path=str(seed),settings_sha256=shash,mods=mods,
       control_overlay=str(overlay),
       comparison_group='stable_controls_mod_ABBA_20261119' if oldspec['expected_year']==1776 else 'stable_controls_vanilla_OFF_ON_20261119')
    specs[label]=spec;plan['profiles'][label]=spec
with (LAB/'STABLE_CONTROLS_PLAN_BEFORE_20261119.json').open('xb') as f:f.write(before)
assert planpath.read_bytes()==before and source.read_bytes()==raw
planpath.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'STABLE_CONTROLS_SETUP_20261119.json').open('x',encoding='utf-8') as f:
    json.dump(dict(order=[x[0] for x in pairs],profiles=specs,settings_sha256=shash,
      changed_preference={'System.screen_edge_scroll_mode':mode},
      common_overlay_original_preserved=True,normal_profiles_untouched=True,
      control_overlay={'path':str(overlay),'menu_gui_sha256':sha(gui),'pulse_gui_sha256':sha(overlay/'gui/sim56_paused_capture.gui')},
      gui_change='Only lab-button anchor/position changed in copied pause menu; native paused animation shared by all C profiles.',
      SCORG2='Rejected preparation: Jan2 and camera movement before planned start, no benchmark.',
      SCORP1='Operational setup only, no simulated DAY, no benchmark.'),f,indent=2)
print(json.dumps({'order':[x[0] for x in pairs],'settings_sha256':shash}))
