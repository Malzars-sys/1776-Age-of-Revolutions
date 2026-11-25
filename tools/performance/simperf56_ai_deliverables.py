"""Export compact accepted measurements; keep raw runtime evidence external."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,subprocess
from simperf56_ai_cohorts import LAB,REPORT,ROOT,sha,write

plan=json.loads((LAB/'PREPARATION.json').read_text(encoding='utf-8'))
trials=[];csvrows=[]
for path in sorted(LAB.glob('*_RESULTS.json')):
    r=json.loads(path.read_text(encoding='utf-8'));label=r['trial']
    accepted=[w for w in r['heartbeat_windows'] if w['window'] in r.get('accepted_windows',('FIRST_AFTER_LOAD_14','FIRST_AFTER_LOAD_28','FIRST_AFTER_LOAD_56'))]
    assert accepted and r['heartbeat_sequence_consecutive']
    proofs={}
    for phase in ('PRE','POST'):
        candidates=[p for p in (LAB/(label+'_'+phase+'_AI_PROOF.json'),LAB/(label+'_'+phase+'_GOAL_PROOF.json')) if p.exists()]
        assert len(candidates)==1,(label,phase,candidates)
        p=candidates[0];full=json.loads(p.read_text(encoding='utf-8'))
        proofs[phase]={k:v for k,v in full.items() if k not in ('actual',)}
        if 'treatment_verified' in full:assert full['treatment_verified']
    windows=[]
    for w in accepted:
        item={k:w[k] for k in ('window','simulated_days','wall_seconds','days_per_second','cpu_machine_percent_approx','working_set_mib_mean','cpu_samples','max_sample_gap_seconds')}
        item.update(start_date=w['start']['date_raw'],end_date=w['end']['date_raw'],start_utc=w['start']['utc'],end_utc=w['end']['utc'])
        windows.append(item)
        csvrows.append(dict(trial=label,**item,initial_disabled=proofs['PRE']['enabled_counts'].get('no',0),initial_enabled=proofs['PRE']['enabled_counts'].get('yes',0)))
    trials.append(dict(trial=label,source_result=str(path),source_sha256=sha(path),windows=windows,proofs=proofs,
        raw_run=r.get('raw_run',r['run']),expected_year=plan['profiles'][label]['expected_year'],
        cohort=plan['profiles'][label].get('diagnostic_cohort'),complete_14_28_56=len(windows)==3))
with (REPORT/'MEASUREMENTS.csv').open('x',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(csvrows[0]));writer.writeheader();writer.writerows(csvrows)
write(REPORT/'SUMMARY.json',dict(utc=datetime.now(timezone.utc).isoformat(),lab=str(LAB),
    native_clock_resolution_less_than_seconds=1,logical_processors=16,trials=trials,
    qualifications=['Native producer timestamps, not buffered log arrival','Only explicitly listed initial DAY windows accepted',
        'First partial day, loading, menus, preparation and first measurement pause excluded',
        'No FPS measurements; disabling AI or an AI goal changes gameplay and is diagnostic only',
        'Compare contemporary controls; do not pool absolute times across batches']))
before=json.loads((LAB/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
audit=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),groups={})
for k,paths in before['groups'].items():
    changed=[p for p,h in paths.items() if not Path(p).exists() or sha(p)!=h]
    audit['groups'][k]=dict(checked=len(paths),unchanged=len(paths)-len(changed),changes=changed)
write(LAB/'PRESERVATION_FINAL.json',audit);write(REPORT/'PRESERVATION_FINAL.json',audit)
for name in ('LAUNCHER_RESUME_20261118.json','TOOL_COLLISION_RECOVERY.json','NATIVE_PRE_HEADER_COMPARISON.json','NATIVE_PRE_SECTION_DIFFERENCES.json','AI_ON3_TICKTASK_VISUAL.json'):
    write(REPORT/name,json.loads((LAB/name).read_text(encoding='utf-8')))
print(json.dumps(dict(trials=len(trials),accepted_windows=len(csvrows),audit=audit),indent=2))
