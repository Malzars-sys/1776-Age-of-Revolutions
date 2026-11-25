"""Aggregate observed per-thread CPU over native, unpaused simulation windows."""
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse,csv,json,sys
sys.dont_write_bytecode=True
from simperf56_analyze import analyze
def summarize(run):
 result=analyze(run);rows=defaultdict(list);names={}
 with (run/'THREAD_CPU.csv').open(encoding='utf-8-sig',newline='') as f:
  for r in csv.DictReader(f):
   tid=int(r['thread_id']);rows[tid].append((datetime.fromisoformat(r['utc'].replace('Z','+00:00')).timestamp(),float(r['cpu_total_ms'])))
   if r['name']:names[tid]=r['name']
 windows=[]
 for w in result['heartbeat_windows']:
  if w['window'] not in ('FIRST_AFTER_LOAD_14','FIRST_AFTER_LOAD_28','FIRST_AFTER_LOAD_56'):continue
  windows.append(w)
 # Standard labeled windows are also useful for a later June/July comparison.
 windows.extend(result['windows'])
 outputs=[]
 for w in windows:
  a=datetime.fromisoformat(w['start']['utc']).timestamp();b=datetime.fromisoformat(w['end']['utc']).timestamp()
  totals=[]
  for tid,series in rows.items():
   inside=[p for p in series if a<=p[0]<=b]
   if len(inside)<2:continue
   delta=inside[-1][1]-inside[0][1]
   if delta<0:continue
   totals.append(dict(thread_id=tid,name=names.get(tid),cpu_ms=delta,sampled_seconds=inside[-1][0]-inside[0][0],one_core_percent=100*delta/(1000*(b-a))))
  total=sum(x['cpu_ms'] for x in totals)
  for x in totals:x['share_of_observed_thread_cpu_percent']=100*x['cpu_ms']/total if total else None
  totals.sort(key=lambda x:x['cpu_ms'],reverse=True)
  outputs.append(dict(window=w['window'],wall_seconds=b-a,simulated_days=w['simulated_days'],observed_cpu_ms=total,threads_recorded=len(totals),threads_with_at_least_one_percent_share=sum(x['share_of_observed_thread_cpu_percent']>=1 for x in totals) if total else 0,top_threads=totals[:12]))
 return dict(trial=result['trial'],windows=outputs,limitations='CPU counters only; unnamed threads cannot be assigned to engine functions. Startup excluded by native bounds. Endpoint sampling and exiting/new threads can lose CPU; no stack trace or PDB symbols.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('run',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();j=summarize(a.run)
 with a.output.open('x',encoding='utf-8') as f:json.dump(j,f,indent=2)
 print(json.dumps(dict(trial=j['trial'],windows=len(j['windows'])),indent=2))
