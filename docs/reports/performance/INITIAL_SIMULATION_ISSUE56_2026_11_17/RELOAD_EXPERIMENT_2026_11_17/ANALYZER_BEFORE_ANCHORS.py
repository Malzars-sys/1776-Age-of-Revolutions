"""Use ENGINE timestamps, never buffered log-arrival times, for issue 56.

Native stamps have one-second resolution. CPU/RAM samples are aligned to those
stamps and are approximate; neither FPS nor an absence of pauses is inferred.
"""
from pathlib import Path
from datetime import datetime,timedelta,timezone
from statistics import mean
import argparse,bisect,csv,json,re

UTC=timezone.utc
MONTHS={m:i+1 for i,m in enumerate(('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'))}
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def dt(value):return datetime.fromisoformat(value.replace('Z','+00:00'))
def game_date(raw):
    found=re.fullmatch(r'([\wûé]+)\s+(\d+),\s*(\d+)',raw.strip())
    if not found or found[1] not in MONTHS:return None
    return datetime(int(found[3]),MONTHS[found[1]],int(found[2])).date()
def engine_day_number(date):
    # Runtime markers prove a 365-day engine year even for 1776/1836.
    if date.month==2 and date.day==29:raise ValueError('Review changed engine calendar.')
    return date.year*365+sum((31,28,31,30,31,30,31,31,30,31,30,31)[:date.month-1])+date.day-1
def analyze(run):
    launch=load(run/'LAUNCH.json');observer=load(run/'OBSERVER.json')
    # Tested machine: Romance Standard Time (Paris). Reject rather than guess a
    # different timezone. November 2026 is UTC+1; record this assumption.
    assert observer['timezone']=='Romance Standard Time'
    started=dt(launch['started_utc'])
    assert started.year==2026 and started.month==11,'Review DST/date alignment.'
    tz=timezone(timedelta(hours=1))
    logdir=run/'logs'
    if not logdir.exists():logdir=Path(launch['profile'])/'logs'
    logfiles=sorted(logdir.glob('debug*.log'),key=lambda p:int(re.search(r'\.(\d+)\.log$',p.name)[1]) if re.search(r'\.(\d+)\.log$',p.name) else 0,reverse=True)
    records=[];countries=0;country_done=False
    seen=set()
    pattern=re.compile(r'^\[(\d\d:\d\d:\d\d)\].*SIM56\|(.*)$')
    prior=started.astimezone(tz)
    for path in logfiles:
        for line in path.read_text(encoding='utf-8-sig',errors='replace').splitlines():
            hit=pattern.search(line)
            if not hit:continue
            payload=hit[2]
            if payload.startswith('COUNTRY|'):countries+=1
            if payload.startswith('COUNTRY_DONE'):country_done=True
            if not payload.startswith(('WINDOW|','DAY|','INIT|')):continue
            key=payload
            if key in seen:continue
            seen.add(key)
            clock=datetime.strptime(hit[1],'%H:%M:%S').time()
            stamp=datetime.combine(prior.date(),clock,tzinfo=tz)
            if stamp<prior-timedelta(hours=12):stamp+=timedelta(days=1)
            prior=stamp
            records.append(dict(payload=payload,utc=stamp.astimezone(UTC).isoformat(),native_clock=hit[1]))
    samples=[]
    with (run/'CONTINUOUS_CPU_RAM.csv').open(encoding='utf-8-sig',newline='') as stream:
        for row in csv.DictReader(stream):
            samples.append(dict(time=dt(row['utc']).timestamp(),cpu=float(row['cpu_total_ms']),ram=float(row['working_set_mib'])))
    times=[s['time'] for s in samples]
    def cpu_at(stamp):
        i=bisect.bisect_right(times,stamp)
        if not 0<i<len(samples):return None
        a,b=samples[i-1],samples[i]
        if b['time']-a['time']>2:return None
        return a['cpu']+(b['cpu']-a['cpu'])*(stamp-a['time'])/(b['time']-a['time'])
    windows={}
    for rec in records:
        hit=re.fullmatch(r'WINDOW\|([A-Z_]+)\|(START|END)\|offset=(\d+)\|date=(.*)',rec['payload'])
        if hit:windows.setdefault(hit[1],{})[hit[2]]=dict(rec,offset_days=int(hit[3]),date_raw=hit[4])
    def measure(name,a,b,days,basis):
        start,end=dt(a['utc']).timestamp(),dt(b['utc']).timestamp()
        elapsed=end-start
        realdates=[game_date(r['date_raw']) for r in (a,b)]
        actual=engine_day_number(realdates[1])-engine_day_number(realdates[0]) if all(realdates) else None
        cpua,cpub=cpu_at(start),cpu_at(end)
        subset=[s for s in samples if start<=s['time']<=end]
        gaps=[b['time']-a['time'] for a,b in zip(subset,subset[1:])]
        assert elapsed>0 and days>0 and actual==days,'Invalid date or wall-clock interval.'
        return dict(window=name,start=a,end=b,simulated_days=days,calendar_days_verified=actual,calendar_model='365-day engine year',measurement_basis=basis,
            wall_seconds=elapsed,wall_resolution_error_less_than_seconds=1,
            days_per_second=days/elapsed,throughput_bounds_from_clock_resolution=[days/(elapsed+1),days/(elapsed-1)] if elapsed>1 else None,
            cpu_machine_percent_approx=100*(cpub-cpua)/(1000*elapsed*observer['logical_processors']) if cpua is not None and cpub is not None else None,
            working_set_mib_mean=mean(s['ram'] for s in subset) if subset else None,
            working_set_mib_min=min(s['ram'] for s in subset) if subset else None,
            working_set_mib_max=max(s['ram'] for s in subset) if subset else None,
            cpu_samples=len(subset),max_sample_gap_seconds=max(gaps) if gaps else None)
    results=[]
    for name,pair in windows.items():
        if set(pair)!= {'START','END'}:continue
        a,b=pair['START'],pair['END']
        results.append(measure(name,a,b,b['offset_days']-a['offset_days'],'Scheduled WINDOW markers'))
    # DAY records provide a cold-reload window even when the save has already
    # consumed its original ten scheduled WINDOW events. Preserve real payloads.
    daily=[]
    for rec in records:
        if rec['payload'].startswith('DAY|date='):
            daily.append(dict(rec,date_raw=rec['payload'].split('DAY|date=',1)[1]))
    consecutive=all(engine_day_number(game_date(b['date_raw']))-engine_day_number(game_date(a['date_raw']))==1 for a,b in zip(daily,daily[1:]))
    derived=[]
    if daily and consecutive:
        starts={'FIRST_AFTER_LOAD':0}
        for name,pair in windows.items():
            if 'START' in pair:
                matches=[i for i,r in enumerate(daily) if r['date_raw']==pair['START']['date_raw']]
                if len(matches)==1:starts[name]=matches[0]
        for name,index in starts.items():
            for length in (14,28,56):
                if index+length<len(daily):derived.append(measure(name+'_'+str(length),daily[index],daily[index+length],length,'Consecutive DAY heartbeat endpoints; first partial day excluded'))
    return dict(trial=launch['trial'],run=str(run),reference_head=launch['reference_head'],executable_sha256=launch['executable_sha256'],settings_sha256=launch['settings_sha256'],runtime_countries=countries if country_done else None,
        timing_basis='Native engine HH:mm:ss timestamps, aligned to continuous CPU/RAM samples; NOT log arrival',
        native_timezone_assumption='Europe/Paris UTC+1, November 2026',logical_processors=observer['logical_processors'],
        no_fps_measurement=True,pause_absence_automatically_verified=False,windows=results,heartbeat_windows=derived,heartbeat_sequence_consecutive=consecutive,markers_seen=len(windows),daily_heartbeats=len(daily))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('run',type=Path);parser.add_argument('--output',type=Path);parser.add_argument('--summary',action='store_true')
    args=parser.parse_args();result=analyze(args.run)
    if args.output:
        with args.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,ensure_ascii=False)
    shown=result
    if args.summary:shown={k:result[k] for k in ('trial','runtime_countries','heartbeat_sequence_consecutive','daily_heartbeats')};shown['windows']=[{k:r[k] for k in ('window','wall_seconds','days_per_second','cpu_machine_percent_approx','working_set_mib_mean')} for r in result['windows'] or result['heartbeat_windows']]
    print(json.dumps(shown,indent=2,ensure_ascii=False))
