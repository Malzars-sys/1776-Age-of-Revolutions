"""Native clock analysis with explicit buffer-tail and pause quality checks."""
from pathlib import Path
from datetime import datetime, timedelta
import argparse, hashlib, json, shutil
from simperf56_analyze import analyze, game_date
from simperf56_ai_cohorts import LAB

ap=argparse.ArgumentParser();ap.add_argument('trial');ap.add_argument('--expected-start',default='1776-01-02');ap.add_argument('--analysis-suffix',default='');ap.add_argument('--allow-partial',action='store_true');a=ap.parse_args()
assert not a.analysis_suffix or all(c.isalnum() or c=='_' for c in a.analysis_suffix)
runs=list((LAB/'runs').glob(a.trial+'_*'));assert len(runs)==1
raw=runs[0];assert (raw/'EXIT.json').exists(), 'Wait for the owned process and observer to finish'
dest=LAB/'analysis'/(a.trial+a.analysis_suffix);assert not dest.exists();dest.mkdir(parents=True);(dest/'logs').mkdir()
manifest=dict(raw_run=str(raw),excluded_tail=[],files={})
for name in ('LAUNCH.json','OBSERVER.json','CONTINUOUS_CPU_RAM.csv'):
    shutil.copyfile(raw/name,dest/name)
for p in (raw/'logs').glob('debug*.log'):
    content=p.read_bytes();lines=content.splitlines(keepends=True);kept=[]
    for i,line in enumerate(lines):
        text=line.decode('utf-8-sig',errors='replace')
        if 'SIM56|DAY|date=' in text:
            date=text.split('SIM56|DAY|date=',1)[1].strip()
            if game_date(date) is None:
                assert p.name=='debug.log' and i==len(lines)-1 and not line.endswith((b'\r',b'\n'))
                manifest['excluded_tail'].append(dict(file=p.name,line=text));continue
        kept.append(line)
    clean=b''.join(kept);(dest/'logs'/p.name).write_bytes(clean)
    manifest['files'][p.name]=dict(source_sha256=hashlib.sha256(content).hexdigest(),analysis_sha256=hashlib.sha256(clean).hexdigest())
result=analyze(dest);assert result['heartbeat_sequence_consecutive']
accepted=[w for w in result['heartbeat_windows'] if w['window'].startswith('FIRST_AFTER_LOAD_')]
assert accepted and [w['simulated_days'] for w in accepted]==[14,28,56][:len(accepted)]
assert len(accepted)==3 or a.allow_partial, 'Incomplete series; use an explicitly labelled partial analysis only'
actions=[json.loads(s) for s in (LAB/'actions'/(a.trial+'.jsonl')).read_text(encoding='utf-8').splitlines()]
starts=[x for x in actions if x['event'] in ('unpause_for_native_DAY_windows','unpause_measurement')]
assert len(starts)==1, 'Ambiguous or missing measurement start action'
start=starts[0]['utc']
end=next(x['utc'] for x in actions if x['event']=='pause_after_measurement')
for w in accepted:
    assert datetime.fromisoformat(start.replace('Z','+00:00'))-timedelta(seconds=1)<=datetime.fromisoformat(w['start']['utc'])
    assert datetime.fromisoformat(w['end']['utc'])<=datetime.fromisoformat(end.replace('Z','+00:00'))+timedelta(seconds=1)
    assert game_date(w['start']['date_raw']).isoformat()==a.expected_start
result['raw_run']=str(raw);result['accepted_windows']=[w['window'] for w in accepted]
result['complete_14_28_56']=len(accepted)==3
result['quality_note']='Only listed initial windows accepted, all before the first measurement pause. Missing windows are not inferred. Any extension after saving/profiling is excluded. Native clock, not log arrival. Raw tail remains immutable.'
result['expected_first_complete_day']=a.expected_start
result['measurement_start_action']=starts[0]
result['analysis_input_manifest']=manifest
for suffix,obj in (('_RESULTS.json',result),('_ANALYSIS_INPUT.json',manifest)):
    with (LAB/(a.trial+suffix)).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,ensure_ascii=False)
print(json.dumps(dict(trial=a.trial,consecutive=True,days=result['daily_heartbeats'],accepted=[
    {k:w[k] for k in ('window','wall_seconds','days_per_second','cpu_machine_percent_approx','working_set_mib_mean')} for w in accepted]),indent=2))
