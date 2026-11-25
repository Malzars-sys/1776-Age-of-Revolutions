"""Freeze main and prepare isolated benchmark profiles and common telemetry.

Does not launch the game or write the normal mod, native installs or profiles.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
LAB=Path('C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117')
EXE=Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/binaries/victoria3.exe')
NORMAL=ROOT.parent.parent
RUNTIME=('common','events','gfx','gui','localization','map_data','music','.metadata')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as stream:json.dump(value,stream,indent=2,ensure_ascii=False)
def script(p,text):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8-sig',newline='\n') as stream:stream.write(text)

def main():
    if LAB.exists():raise SystemExit('Keep prior lab; inspect it before preparing another.')
    REPORT.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert head=='bd776919f625016cb9e63b2359cc04796c681ef5','Review changed reference main.'
    assert sha(ROOT/'gui/tech_tree.gui')=='94fb72b75640fe1c8bbde01af235993225dff662d11974c8a267eaeca85ff9c0'
    files=sorted(p for name in RUNTIME for p in (ROOT/name).rglob('*') if p.is_file())
    if (ROOT/'descriptor.mod').is_file():files.append(ROOT/'descriptor.mod')
    inputs={p.relative_to(ROOT).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in files}
    normal_paths=[NORMAL/p for p in ('pdx_settings.json','launcher-v2.sqlite','content_load.json','dlc_load.json') if (NORMAL/p).exists()]
    normal_paths.extend(p for p in (NORMAL/'save games').rglob('*') if p.is_file())
    before=dict(utc=datetime.now(timezone.utc).isoformat(),head=head,index_sha256=sha(ROOT/'.git/index'),runtime=inputs,
         normal_profile={str(p):sha(p) for p in normal_paths},
         protected_diplomacy={str(ROOT/p):sha(ROOT/p) for p in ('common/diplomatic_actions/1776_protected_state.txt','common/history/diplomacy/00_subject_relationships.txt','common/subject_types/zz_1776_protected_state.txt')},
         executable=str(EXE),executable_sha256=sha(EXE),remote_head=head)
    write(REPORT/'PRESERVATION_BEFORE.json',before)
    base=LAB/'main_frozen'
    for rel,spec in inputs.items():
        source,target=ROOT/rel,base/rel;target.parent.mkdir(parents=True,exist_ok=True)
        assert sha(source)==spec['sha256'],'Concurrent runtime modification.'
        shutil.copyfile(source,target)
    assert all(sha(base/rel)==spec['sha256'] for rel,spec in inputs.items())
    write(LAB/'FROZEN_MANIFEST.json',dict(head=head,files=inputs))
    telemetry=LAB/'telemetry'
    write(telemetry/'.metadata/metadata.json',dict(name='ISSUE56 common simulation telemetry',version='1',supported_game_version='1.15.*',game_custom_data=dict(multiplayer_synchronized=True)))
    # All benchmark windows use fourteen simulated days. Both starting years
    # 1776 and 1836 are leap years: Apr 1 = day 91, Jul 1 = day 182.
    windows=[('INITIAL',1,15),('FEBRUARY',31,45),('APRIL',91,105),('JULY',182,196),('NEXT_JANUARY',366,380)]
    lines=['on_game_started_after_lobby = { on_actions = { aor56_telemetry_start } }','aor56_telemetry_start = { effect = {',
           ' debug_log = "SIM56|INIT|date=[TimeKeeper.GetCurrentDate.GetString]"',
           ' every_country = { debug_log = "SIM56|COUNTRY|name=[THIS.GetCountry.GetNameNoFormatting]" }',
           ' debug_log = "SIM56|COUNTRY_DONE"',
           ' c:FRA ?= { trigger_event = { id = aor56.100 days = 1 }']
    event_lines=['namespace = aor56']
    number=1
    for label,start,end in windows:
        for edge,day in [('START',start),('END',end)]:
            lines.append(f'  trigger_event = {{ id = aor56.{number} days = {day} }}')
            event_lines.append(f'aor56.{number} = {{ type = country_event hidden = yes immediate = {{ debug_log = "SIM56|WINDOW|{label}|{edge}|offset={day}|date=[TimeKeeper.GetCurrentDate.GetString]" }} }}')
            number+=1
    lines.extend([' }','} }'])
    event_lines.append('aor56.100 = { type = country_event hidden = yes immediate = { debug_log = "SIM56|DAY|date=[TimeKeeper.GetCurrentDate.GetString]" trigger_event = { id = aor56.100 days = 1 } } }')
    script(telemetry/'common/on_actions/zz_aor56_telemetry.txt','\n'.join(lines)+'\n')
    script(telemetry/'events/aor56_telemetry.txt','\n'.join(event_lines)+'\n')
    # Reuse only the same-executable laboratory settings/cache; never normal
    # saves or registration databases. Game/autosave controls are common.
    seed=Path('C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/A1/user_data')
    settings=json.loads((seed/'pdx_settings.json').read_text(encoding='utf-8-sig'))
    settings['game']['pause_on_event']=False
    settings['game']['autosave']='never'
    settings['game']['save_on_exit']=False
    profiles={}
    for label in ('MAIN1','VANILLA1'):
        profile=LAB/'profiles'/label
        profile.mkdir(parents=True)
        write(profile/'pdx_settings.json',settings)
        for folder in ('shadercache','user_bindings'):
            if (seed/folder).exists():shutil.copytree(seed/folder,profile/folder)
        mods=[dict(path=str(base).replace('\\','/'))] if label.startswith('MAIN') else []
        mods.append(dict(path=str(telemetry).replace('\\','/')))
        write(profile/'content_load.json',dict(enabledMods=mods,disabledDLC=[],enabledUGC=[]))
        profiles[label]=dict(path=str(profile),mods=[r['path'] for r in mods],settings_sha256=sha(profile/'pdx_settings.json'),
                             expected_year=1776 if label.startswith('MAIN') else 1836)
    plan=dict(utc=datetime.now(timezone.utc).isoformat(),issue=56,reference_head=head,lab=str(LAB),main_frozen=str(base),telemetry=str(telemetry),
              executable=str(EXE),executable_sha256=sha(EXE),profiles=profiles,windows=[dict(label=l,start_offset_days=s,end_offset_days=e,simulated_days=e-s) for l,s,e in windows],
              first_window_note='Initial window begins after the first simulated day; paused setup and the first partial day are excluded.',
              instrumentation_runtime_verified=False,simulation_results=None,normal_profile_modified=False,diagnostics=[])
    write(REPORT/'PREPARATION.json',plan)
    print(json.dumps(dict(files=len(inputs),bytes=sum(s['bytes'] for s in inputs.values()),head=head,lab=str(LAB),profiles=profiles),indent=2))

if __name__=='__main__':main()
