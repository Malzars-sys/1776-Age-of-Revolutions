"""Preserve and read a completed native Legacy script export; never infer native CPU shares."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil
from simperf56_ai_cohorts import LAB
from simperf56_economic_goals_20261118 import verify

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
label='PROFC1';runs=list((LAB/'runs').glob(label+'_*'));assert len(runs)==1
run=runs[0];assert (run/'EXIT.json').exists()
source=LAB/'profiles'/label/'logs/script_profiling.txt'
dest=LAB/'evidence/PROFC1_SCRIPT_PROFILING_NATIVE.txt'
with dest.open('xb') as f:f.write(source.read_bytes())
assert sha(source)==sha(dest)
lines=dest.read_text(encoding='utf-8-sig').splitlines()
assert lines[0].strip()=='# type, location, time (seconds), call count'
rows=[];unparsed=[]
for line in lines[1:]:
    if not line.strip():continue
    m=re.fullmatch(r'(\S+)\s+(\S+):(\d+)\s+([0-9.]+)\s+(\d+)',line)
    if not m:unparsed.append(line);continue
    rows.append(dict(type=m[1],file=m[2],line=int(m[3]),reported_seconds=float(m[4]),calls=int(m[5])))
assert rows and not unparsed,unparsed[:3]
setup=read(LAB/'SCORE_BASES_SETUP_20261118.json')
plan=read(LAB/'PREPARATION.json');frozen=Path(plan['profiles'][label]['mods'][0])
callbacks=[]
for change in setup['changes']:
    file=change['file'].replace('\\','/');assert sha(frozen/file)==change['original_file_sha256']
    found=[x for x in rows if x['type']=='script_value' and x['file']==file and x['line']==change['line']]
    assert len(found)<=1
    callbacks.append(dict(building=change['building'],file=file,line=change['line'],
        observed_in_export=bool(found),measurement=found[0] if found else None,
        absence_is_not_a_zero_cost_proof=not bool(found)))
witnesses=[read(p) for p in (LAB/'autosave_witnesses'/label).glob('*.json')
           if read(p).get('event')=='native_autosave_preserved']
assert witnesses;witness=witnesses[0];assert sha(Path(witness['preserved']))==witness['sha256']
verify(label,Path(witness['preserved']),'POST',None)
out=dict(trial=label,utc=datetime.now(timezone.utc).isoformat(),not_a_throughput_benchmark=True,
    native_export=str(dest),native_export_sha256=sha(dest),header=lines[0],parsed_entries=len(rows),
    units='seconds explicitly declared by the native export header',
    top_entries=sorted(rows,key=lambda x:x['reported_seconds'],reverse=True)[:25],
    tested_callbacks=callbacks,callbacks_observed=sum(x['observed_in_export'] for x in callbacks),
    native_post_proof=str(LAB/(label+'_POST_GOAL_PROOF.json')),
    scope='Legacy ScriptProfiling.Enable followed by ScriptProfiling.Dump in a separate session. Includes paused UI time before and after simulation and the April autosave. Not an exclusive or complete engine CPU profile; do not sum nested script rows into CPU shares.',
    gui_limit='At 100% UI scale lower diagnostic buttons were outside the captured client. Only this profile was changed to 70% so Enable and Dump were reachable. Jomini Start/Stop table was not captured in this session.',
    native_settings_before=sha(run/'SETTINGS.json'),native_settings_after=sha(LAB/'profiles'/label/'pdx_settings.json'))
with (LAB/'PROFC1_SCRIPT_PROFILE_RESULTS.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps({k:out[k] for k in ('parsed_entries','callbacks_observed','top_entries','tested_callbacks')},indent=2))
