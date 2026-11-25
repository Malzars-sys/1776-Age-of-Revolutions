"""Qualify both scheduled and derived intervals without deleting raw metrics."""
from pathlib import Path
from datetime import datetime,timezone
import json
def qualify(data):
    excluded=[]
    for trial,run in data.items():
        for field in ('windows','heartbeat_windows'):
            for row in run.get(field,[]):
                start=datetime.fromisoformat(row['start']['utc']);end=datetime.fromisoformat(row['end']['utc'])
                state='USABLE_WITH_LIMITATIONS';reason='Native clock resolution <1 s; no automatic foreground/pause certification.'
                if trial=='MAIN1':state='PILOT_ONLY';reason='Interrupted collector pilot.'
                if trial=='MAIN2':
                    for low,high in [('2026-11-17T02:33:49+00:00','2026-11-17T02:33:58+00:00'),('2026-11-17T02:34:17+00:00','2026-11-17T02:34:26+00:00')]:
                        if start<=datetime.fromisoformat(high) and end>=datetime.fromisoformat(low):
                            state='EXCLUDED_UI_INTERVENTION';reason='Interval overlaps an event-choice action or its timing uncertainty.'
                if trial=='MAIN3' and end>=datetime.fromisoformat('2026-11-17T03:24:19+00:00'):
                    state='EXCLUDED_SPEED_CHANGED';reason='Interval intersects or follows the reduction to speed 1; no verified speed-5 restoration.'
                row['quality']=state;row['quality_reason']=reason
                if field=='heartbeat_windows' and state.startswith('EXCLUDED'):
                    excluded.append(dict(trial=trial,window=row['window'],quality=state,reason=reason))
    return excluded
if __name__=='__main__':
    root=Path(__file__).resolve().parents[2]/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
    path=root/'BENCHMARKS_EXTENDED.json';before=path.read_bytes();data=json.loads(before)
    exclusions=qualify(data)
    qualitypath=root/'BENCHMARK_QUALITY.json';qualitybefore=qualitypath.read_bytes();quality=json.loads(qualitybefore)
    quality['excluded_derived_windows']=exclusions
    for target,original in [(path,before),(qualitypath,qualitybefore)]:
        with target.with_name(target.stem+'_BEFORE_DERIVED_QUALIFICATION.json').open('xb') as out:out.write(original)
        assert target.read_bytes()==original
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    qualitypath.write_text(json.dumps(quality,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(dict(excluded_derived_windows=exclusions,all_raw_metrics_preserved=True),indent=2))
