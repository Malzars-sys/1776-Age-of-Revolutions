"""Compare identical world dates before and after cold reload via real DAYs."""
from pathlib import Path
from datetime import datetime
import argparse,json,sys
from simperf56_analyze import analyze,engine_day_number
ROOT=Path(__file__).resolve().parents[2]
ROUND=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/RELOAD_EXPERIMENT_2026_11_17'
parser=argparse.ArgumentParser();parser.add_argument('run',type=Path);parser.add_argument('--save-date',required=True);parser.add_argument('--output',type=Path);args=parser.parse_args()
saved=datetime(*map(int,args.save_date.split('.'))).date();first=engine_day_number(saved)+1
anchors={'SAVED_PLUS_'+str(offset):first+offset for offset in (0,14,28,42,56,70,84,98)}
result=analyze(args.run,extra_starts=anchors)
result['comparison_saved_date']=args.save_date
result['comparison_note']='Same world save date; S+1 excludes the first partial day and preceding save/setup pause.'
if args.output:
    with args.output.open('x',encoding='utf-8') as out:json.dump(result,out,indent=2,ensure_ascii=False)
print(json.dumps(dict(trial=result['trial'],daily_heartbeats=result['daily_heartbeats'],consecutive=result['heartbeat_sequence_consecutive'],windows=[{k:r[k] for k in ('window','wall_seconds','days_per_second','cpu_machine_percent_approx','working_set_mib_mean')} for r in result['heartbeat_windows'] if r['window'].startswith('SAVED_PLUS') and (r['window'].endswith('_14') or r['window'] in ('SAVED_PLUS_0_28','SAVED_PLUS_0_56','SAVED_PLUS_56_56'))]),indent=2,ensure_ascii=False))
