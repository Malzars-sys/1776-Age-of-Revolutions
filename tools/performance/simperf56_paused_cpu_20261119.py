"""Describe already-recorded pre-unpause CPU; never call it simulation throughput."""
import bisect, csv, json
from datetime import datetime
from statistics import mean
from simperf56_ai_cohorts import LAB

def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
out={}
for label in ('SCORC1','ECNC1'):
    r=json.loads((LAB/(label+'_RESULTS.json')).read_text(encoding='utf-8'))
    run=r['raw_run'];samples=[]
    with open(run+'/CONTINUOUS_CPU_RAM.csv',encoding='utf-8-sig',newline='') as f:
        for x in csv.DictReader(f):samples.append((dt(x['utc']),float(x['cpu_total_ms']),float(x['working_set_mib'])))
    times=[x[0] for x in samples]
    def at(t):
        i=bisect.bisect_right(times,t);assert 0<i<len(samples)
        a,b=samples[i-1],samples[i];assert b[0]-a[0]<=2
        return a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0])
    actions=[json.loads(x) for x in (LAB/'actions'/(label+'.jsonl')).read_text(encoding='utf-8').splitlines()]
    continued=dt(next(x['utc'] for x in actions if x['event']=='continue_initial_save'))
    start=dt(r['measurement_start_action']['utc']);end=start-1;begin=end-20
    assert begin>continued+20
    subset=[x for x in samples if begin<=x[0]<=end]
    out[label]=dict(scope='Last 20 seconds before unpause; process CPU including rendering, not function attribution or simulated-day performance.',
        seconds_after_continue=[begin-continued,end-continued],cpu_machine_percent=100*(at(end)-at(begin))/(1000*20*r['logical_processors']),
        working_set_mib_mean=mean(x[2] for x in subset),sample_count=len(subset),source_date_observed='1776.1.1',
        native_DAY_first_timestamp_after_start_verified=r['complete_14_28_56'])
with (LAB/'PAUSED_CPU_C1_20261119.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
