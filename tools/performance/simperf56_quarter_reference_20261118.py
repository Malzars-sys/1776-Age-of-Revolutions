"""Prepare a vanilla pair with native post-window autosaves; normal profile untouched."""
from pathlib import Path
from collections import Counter
import hashlib, json, re, shutil
from simperf56_ai_cohorts import LAB, PREVIOUS, db_chunks, sha
from simperf56_save_state import sections

source=Path('C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117/profiles/VANILLA1/save games/france_1836_01_01.v3')
assert sha(source)=='3b9a4448bd1a31e95e1bb55b7a34eef59d29834f4eaf6038a78d3580904d794f'
raw=source.read_bytes();text=raw.decode('utf-8-sig')
on,n=re.subn(r'(?m)^speed=2\r?$', 'speed=4',text);assert n==1
ss=sections(on);edits=[];controllers={}
for rid,a,b,node in db_chunks(on,ss['ai']):
    country=str(node.one('country'));assert node.one('enabled')=='yes'
    controllers[country]=rid
    es=node.children('enabled');assert len(es)==1
    e=es[0];segment=on[a+e.start:a+e.end];m=re.search(r'yes$',segment);assert m
    edits.append((a+e.start+m.start(),a+e.start+m.end()))
assert len(controllers)==len(edits)==449
off=on
for a,b in sorted(edits,reverse=True):off=off[:a]+'no'+off[b:]
ai_a,ai_b=ss['ai'];assert off[:ai_a]==on[:ai_a] and off[ai_b-449:]==on[ai_b:]
assert on==text.replace('\nspeed=2\n','\nspeed=4\n',1)
pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before)
original_settings=(LAB/'profiles/VAN_OFF3/pdx_settings.json').read_bytes()
assert hashlib.sha256(original_settings).hexdigest()=='49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c'
settings=json.loads(original_settings);settings['game']['autosave']='quarteryear';settings['game']['save_to_cloud']=False
settings_bytes=json.dumps(settings,indent=2,ensure_ascii=False).encode('utf-8')
manifest=dict(source=str(source),source_sha256=sha(source),source_controller_ids=controllers,
    source_speed='2',prepared_speed='4',pair_only_world_difference='449 native enabled flags',
    outside_ai_identical_between_pair=True,settings_change={'game.autosave':'quarteryear','game.save_to_cloud':False},
    autosave_schedule_not_yet_runtime_verified=True,requires_no_autosave_inside_day_windows=True,profiles={})
for label,payload,wanted in (('VAN_ONQ1',on,'yes'),('VAN_OFFQ1',off,'no')):
    assert label not in plan['profiles']
    profile=LAB/'profiles'/label;assert not profile.exists();(profile/'save games').mkdir(parents=True)
    seed=profile/'save games'/(label+'_S0.v3')
    with seed.open('xb') as f:f.write((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+payload.encode('utf-8'))
    (profile/'pdx_settings.json').write_bytes(settings_bytes)
    shutil.copytree(LAB/'profiles/VAN_OFF3/user_bindings',profile/'user_bindings')
    mods=[(PREVIOUS/'telemetry_profile').as_posix()]
    (profile/'content_load.json').write_text(json.dumps(dict(enabledMods=[{'path':x} for x in mods],disabledDLC=[],enabledUGC=[]),indent=2),encoding='utf-8')
    spec=dict(path=str(profile),mods=mods,settings_sha256=sha(profile/'pdx_settings.json'),expected_year=1836,
        saved_date='1836.1.1',common_save_sha256=sha(seed),seed_path=str(seed),expected_enabled=wanted,
        reference_scope='Vanilla1836; quarterly local autosave witness after the 56-day window; all other settings preserved')
    plan['profiles'][label]=spec;manifest['profiles'][label]=spec
with (LAB/'QUARTER_REFERENCE_PLAN_BEFORE_20261118.json').open('xb') as f:f.write(before)
assert pp.read_bytes()==before;pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'QUARTER_REFERENCE_SETUP_20261118.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,indent=2)
print(json.dumps({'controllers':len(controllers),'settings_sha256':hashlib.sha256(settings_bytes).hexdigest(),'profiles':list(manifest['profiles'])}))
