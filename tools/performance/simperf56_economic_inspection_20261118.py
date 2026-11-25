"""Read-only native AI queries in PM1 only; no throughput comparison with this UI."""
from pathlib import Path
import hashlib, json, re
from simperf56_ai_cohorts import LAB, PREVIOUS

def sha(b):return hashlib.sha256(b).hexdigest()
src=PREVIOUS/'telemetry_profile/gui/frontend/frontend_ingame_menu.gui'
raw=src.read_bytes()
assert sha(raw)=='72732c19a7975194a348b7668c29d0000078d3bb5b8d44367a40e29f65f75d20'
queries=(('AI goals - lecture','show_goals'),
         ('AI strategies - lecture','ai_print_strategy_values'),
         ('Score construction publique','ai_evaluate_government_construction building_wheat_farm STATE_ILE_DE_FRANCE'),
         ('Score construction autonome','ai_evaluate_autonomous_construction building_wheat_farm STATE_ILE_DE_FRANCE'),
         ('Score PM agriculture simple','ai_evaluate_production_method building_wheat_farm pm_simple_farming STATE_ILE_DE_FRANCE'),
         ('Journal des taches moteur','log_ticktask_performance'))
text=raw.decode('utf-8-sig');i=0
def replace(m):
    global i
    label,command=queries[i];i+=1
    return f'  button = {{ using = default_button name = "sim56_econ_query_{i}" size = {{ 440 40 }} raw_text = "{label}" onclick = "[ExecuteConsoleCommand(\'{command}\')]" }}'
changed=re.sub(r'^  button = \{ using = default_button name = "sim56_[^\n]+',replace,text,flags=re.M)
assert i==len(queries)==6
overlay=LAB/'economic_inspection_overlay'
assert not overlay.exists()
dest=overlay/'gui/frontend/frontend_ingame_menu.gui';dest.parent.mkdir(parents=True)
with dest.open('xb') as f:f.write(changed.encode('utf-8'))
planpath=LAB/'PREPARATION.json';before=planpath.read_bytes();plan=json.loads(before)
spec=plan['profiles']['PM1'];assert len(spec['mods'])==2
contentpath=Path(spec['path'])/'content_load.json';content_before=contentpath.read_bytes();content=json.loads(content_before)
spec['mods'].append(overlay.as_posix());content['enabledMods'].append({'path':overlay.as_posix()})
spec['query_ui_only_not_a_throughput_trial']=True
for name,data in (('ECON_INSPECTION_PLAN_BEFORE.json',before),('ECON_INSPECTION_CONTENT_BEFORE.json',content_before)):
    with (LAB/name).open('xb') as f:f.write(data)
assert planpath.read_bytes()==before and contentpath.read_bytes()==content_before and src.read_bytes()==raw
planpath.write_text(json.dumps(plan,indent=2),encoding='utf-8')
contentpath.write_text(json.dumps(content,indent=2),encoding='utf-8')
with (LAB/'ECON_INSPECTION_SETUP.json').open('x',encoding='utf-8') as f:
    json.dump(dict(profile='PM1',queries=queries,reference_gui_sha256=sha(raw),overlay_gui_sha256=sha(dest.read_bytes()),
                   common_overlay_unchanged=True,only_isolated_pm1_profile_changed=True,
                   commands_registered_in_local_executable_not_yet_runtime_verified=True),f,indent=2)
print(json.dumps({'overlay':str(overlay),'queries':len(queries),'benchmark':False}))
