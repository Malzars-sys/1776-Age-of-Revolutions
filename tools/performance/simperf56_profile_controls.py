"""Mouse-accessible native diagnostic commands, common to both profiled trials.

Only an external telemetry GUI override is added. No main/Steam file is edited.
"""
from pathlib import Path
import hashlib,json,shutil,sys
sys.dont_write_bytecode=True
from simperf56_state_lab import ROOT,LAB,OLD,profile,sha,write
sys.path.insert(0,str(ROOT/'tools'))
from validate_diplomacy_ottoman_1776 import parse
plan=json.loads((LAB/'SOURCE_PLAN.json').read_text(encoding='utf-8'))
overlay=LAB/'telemetry_profile';assert not overlay.exists()
shutil.copytree(plan['telemetry'],overlay)
rel='gui/frontend/frontend_ingame_menu.gui'
source=Path(plan['main_frozen'])/rel
if not source.exists():source=Path(plan['executable']).parent.parent/'game'/rel
raw=source.read_bytes();text=raw.decode('utf-8-sig')
nodes=[n for n in parse(text) if n.key=='window' and n.one('name')=='"ingame_pausemenu"'];assert len(nodes)==1
n=nodes[0]
commands=[('tick','Journal des taches moteur','log_ticktask_performance'),('off','IA native : DESACTIVER','disable_ai all'),('on','IA native : ACTIVER','enable_ai all'),('script','Profiler scripts : activer','ScriptProfiling.Enable'),('dump','Exporter profil scripts','ScriptProfiling.Dump'),('gui','Ouvrir profileur scripts','Script.Profiling.Gui')]
body='\n # ISSUE56 LAB ONLY: common instrumentation, hidden with pause menu.\n vbox = {\n  name = "sim56_profile_controls"\n  parentanchor = right|vcenter\n  position = { -480 -180 }\n  spacing = 8\n  size = { 440 340 }\n  textbox = { raw_text = "LAB56 - DIAGNOSTIC ISOLE" size = { 440 36 } fontsize = 22 }\n'
for key,label,command in commands:
 body+='  button = { using = default_button name = "sim56_'+key+'" size = { 440 40 } raw_text = "'+label+'" onclick = "[ExecuteConsoleCommand(\''+command+'\')]" }\n'
body+=' }\n'
new=text[:n.end-1]+body+text[n.end-1:]
assert len(parse(new))==len(parse(text))
target=overlay/rel;target.parent.mkdir(parents=True);target.write_text(new,encoding='utf-8-sig')
write(LAB/'PROFILE_CONTROLS.json',dict(source=str(source),source_sha256=hashlib.sha256(raw).hexdigest(),override_sha256=sha(target),overlay=str(overlay),new_file=rel,commands={k:c for k,_,c in commands},purpose='Common instrumentation only. Buttons execute registered native in-game commands, no OS commands. Pause menu absent during throughput windows.',runtime_verified=False))
for label in ('ENG_ON','ENG_OFF'):
 profile(label)
 pp=LAB/'PREPARATION.json';old=pp.read_bytes();p=json.loads(old);spec=p['profiles'][label];spec['mods'][1]=overlay.as_posix()
 cp=Path(spec['path'])/'content_load.json';oldc=cp.read_bytes();c=json.loads(oldc);c['enabledMods'][1]['path']=overlay.as_posix()
 assert pp.read_bytes()==old and cp.read_bytes()==oldc
 (LAB/('PLAN_BEFORE_CONTROLS_'+label+'.json')).write_bytes(old)
 (LAB/('CONTENT_BEFORE_CONTROLS_'+label+'.json')).write_bytes(oldc)
 cp.write_text(json.dumps(c,indent=2),encoding='utf-8')
 pp.write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf-8')
 write(LAB/('PROFILE_CONTROLS_'+label+'.json'),spec)
print('Prepared ENG_ON / ENG_OFF with identical common mouse controls and unchanged initial save.')
