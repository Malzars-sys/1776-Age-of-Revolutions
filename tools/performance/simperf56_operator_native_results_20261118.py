"""Native DAY timing with explicitly recorded human assistance, never invented clicks."""
from pathlib import Path
from datetime import datetime
import argparse, hashlib, json, shutil, re
from simperf56_ai_cohorts import LAB
from simperf56_analyze import analyze, game_date

ap=argparse.ArgumentParser();ap.add_argument('trial',choices=('VAN_ON3','VAN_OFF3'));a=ap.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
runs=list((LAB/'runs').glob(a.trial+'_*'));assert len(runs)==1
raw=runs[0];assert (raw/'EXIT.json').exists()
request=read(LAB/(a.trial+'_OPERATOR_START_REQUEST.json'))
actions=[json.loads(s) for s in (LAB/'actions'/(a.trial+'.jsonl')).read_text(encoding='utf-8').splitlines()]
ends=[x for x in actions if x['event']=='pause_after_measurement']
stop=ends[0] if ends else read(LAB/(a.trial+'_OPERATOR_STOP_REQUEST.json'))
proofs=[read(LAB/(a.trial+'_'+phase+'_AI_PROOF.json')) for phase in ('PRE','POST')]
assert proofs[0]['date'].startswith('1836.1.1') and len({p['expected_flag'] for p in proofs})==1
assert all(not p['unexpected_flags'] for p in proofs)
for p in proofs:
    text=Path(p['save']).open('rb').read(20000)
    assert re.search(rb'\nspeed=([^\r\n]+)',text)[1]==b'4'
dest=LAB/'analysis'/a.trial;assert not dest.exists();dest.mkdir();(dest/'logs').mkdir()
manifest=dict(raw_run=str(raw),excluded_tail=[],files={})
for name in ('LAUNCH.json','OBSERVER.json','CONTINUOUS_CPU_RAM.csv'):shutil.copyfile(raw/name,dest/name)
for p in (raw/'logs').glob('debug*.log'):
    content=p.read_bytes();lines=content.splitlines(keepends=True);kept=[]
    for i,line in enumerate(lines):
        s=line.decode('utf-8-sig',errors='replace')
        if 'SIM56|DAY|date=' in s and game_date(s.split('SIM56|DAY|date=',1)[1].strip()) is None:
            assert p.name=='debug.log' and i==len(lines)-1 and not line.endswith((b'\r',b'\n'))
            manifest['excluded_tail'].append(dict(file=p.name,line=s));continue
        kept.append(line)
    clean=b''.join(kept);(dest/'logs'/p.name).write_bytes(clean)
    manifest['files'][p.name]=dict(source_sha256=hashlib.sha256(content).hexdigest(),analysis_sha256=hashlib.sha256(clean).hexdigest())
result=analyze(dest);assert result['heartbeat_sequence_consecutive']
accepted=[w for w in result['heartbeat_windows'] if w['window'].startswith('FIRST_AFTER_LOAD_')]
assert [w['simulated_days'] for w in accepted]==[14,28,56]
for w in accepted:
    assert game_date(w['start']['date_raw']).isoformat()=='1836-01-02'
    assert dt(request['utc'])<=dt(w['start']['utc']) and dt(w['end']['utc'])<=dt(stop['utc'])
result.update(raw_run=str(raw),accepted_windows=[w['window'] for w in accepted],complete_14_28_56=True,
    expected_first_complete_day='1836-01-02',operator_assisted=True,operator_start_request=request,
    exact_unpause_click_time_known=False,stop_boundary=stop,analysis_input_manifest=manifest,
    quality_note='Native DAY times only. Human assistance requested for starting while capture was frozen. No unpause click timestamp inferred. Initial partial day excluded. All endpoints before the recorded stop boundary. Pauses inside the interval are not automatically excluded; preserve operator/UI evidence.')
with (LAB/(a.trial+'_RESULTS.json')).open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps(dict(trial=a.trial,operator_assisted=True,accepted=[{k:w[k] for k in ('window','wall_seconds','cpu_machine_percent_approx')} for w in accepted]),indent=2))
