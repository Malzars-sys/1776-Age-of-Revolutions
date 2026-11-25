"""Thread CPU distribution within accepted native windows, without stacks."""
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import argparse,bisect,csv,json
from simperf56_ai_cohorts import LAB,write

def ts(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
ap=argparse.ArgumentParser();ap.add_argument('--output-name',default='THREAD_WINDOW_SUMMARY.json');args=ap.parse_args()
assert Path(args.output_name).name==args.output_name and args.output_name.endswith('.json')
out={}
for p in sorted(LAB.glob('*_RESULTS.json')):
    r=json.loads(p.read_text(encoding='utf-8'))
    windows=[w for w in r['heartbeat_windows'] if w['window']=='FIRST_AFTER_LOAD_56']
    if not windows:continue
    raw=Path(r.get('raw_run',r['run']))
    if not (raw/'THREAD_CPU.csv').exists():
        candidates=list((LAB/'runs').glob(r['trial']+'_*'));assert len(candidates)==1;raw=candidates[0]
    w=windows[0];a,b=ts(w['start']['utc']),ts(w['end']['utc'])
    rows=defaultdict(list);names={}
    with (raw/'THREAD_CPU.csv').open(encoding='utf-8-sig',newline='') as f:
        for x in csv.DictReader(f):
            t=ts(x['utc'])
            if a-2<=t<=b+2:
                rows[x['thread_id']].append((t,float(x['cpu_total_ms'])))
                if x['name']:names[x['thread_id']]=x['name']
    def at(seq,t):
        i=bisect.bisect_right([x[0] for x in seq],t)
        if not 0<i<len(seq):return None
        x,y=seq[i-1],seq[i]
        if y[0]-x[0]>2:return None
        return x[1]+(y[1]-x[1])*(t-x[0])/(y[0]-x[0])
    found=[];uncovered=[]
    for ident,seq in rows.items():
        left,right=at(seq,a),at(seq,b)
        if left is None or right is None:uncovered.append(ident);continue
        delta=right-left;assert delta>=0
        found.append(dict(thread_id=ident,name=names.get(ident,''),cpu_ms=delta,
            percent_of_one_logical_processor=100*delta/(1000*(b-a))))
    total=sum(x['cpu_ms'] for x in found)
    for x in found:x['share_of_covered_thread_cpu_percent']=100*x['cpu_ms']/total if total else None
    out[r['trial']]=dict(window=w['window'],wall_seconds=b-a,covered_threads=len(found),
        threads_without_boundary_coverage=uncovered,covered_thread_cpu_ms=total,
        process_cpu_ms_approx=w['cpu_machine_percent_approx']*(b-a)*16*10,
        top_threads=sorted(found,key=lambda x:x['cpu_ms'],reverse=True)[:10],
        qualification='Public per-thread CPU counters, linear interpolation with boundary gaps <=2s; no native stacks or engine function attribution. 16 logical processors. Missing boundary coverage reported.')
write(LAB/args.output_name,out)
print(json.dumps({k:dict(wall_seconds=v['wall_seconds'],coverage_ms=v['covered_thread_cpu_ms'],top=v['top_threads'][:3]) for k,v in out.items()},indent=2))
