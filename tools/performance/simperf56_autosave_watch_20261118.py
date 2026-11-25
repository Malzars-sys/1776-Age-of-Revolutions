"""Observe only an isolated profile; preserve stable native post-window autosaves."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, shutil, time
from simperf56_ai_cohorts import LAB
ap=argparse.ArgumentParser();ap.add_argument('trial');a=ap.parse_args();assert re.fullmatch('[A-Z0-9_]{2,40}',a.trial)
runs=list((LAB/'runs').glob(a.trial+'_*'));assert len(runs)==1
run=runs[0];launch=json.loads((run/'LAUNCH.json').read_text(encoding='utf-8-sig'))
profile=Path(launch['profile']);assert profile.resolve().is_relative_to((LAB/'profiles').resolve())
year=launch['expected_year'];out=LAB/'autosave_witnesses'/a.trial;out.mkdir(parents=True,exist_ok=False)
events=(out/'FILE_EVENTS.jsonl').open('x',encoding='utf-8',buffering=1)
state={};copied=set();started=time.monotonic();exit_seen=None
def utc():return datetime.now(timezone.utc).isoformat()
def emit(d):events.write(json.dumps(dict(utc=utc(),**d),ensure_ascii=False)+'\n')
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
(out/'WATCHER_READY.json').write_text(json.dumps(dict(trial=a.trial,utc=utc(),run=str(run),profile=str(profile),
    poll_seconds=1,copy_only_after_day56_or_after_exit=True,settings_not_modified=True)),encoding='utf-8')
print(json.dumps({'watcher':a.trial,'ready':True}),flush=True)
while time.monotonic()-started<7200:
    exited=(run/'EXIT.json').exists()
    if exited and exit_seen is None:exit_seen=time.monotonic()
    for p in (profile/'save games').glob('*.v3'):
        if 'autosave' not in p.name.lower():continue
        try:
            st=p.stat();signature=(st.st_size,st.st_mtime_ns)
            with p.open('rb') as f:prefix=f.read(8192)
            match=re.search(rb'\bgame_date=([0-9.]+)',prefix)
            date=match[1].decode('ascii') if match else None
            old=state.get(p.name)
            if old is None or old[0]!=signature:
                emit(dict(event='native_autosave_file_observed',file=str(p),bytes=st.st_size,mtime_ns=st.st_mtime_ns,game_date=date))
                state[p.name]=(signature,time.monotonic());continue
            stable=time.monotonic()-old[1]>=2
            date_parts=tuple(map(int,date.split('.')))[:3] if date else None
            eligible=date_parts is not None and date_parts>=(year,3,1)
            token=(p.name,signature)
            if stable and token not in copied and (eligible or exited):
                target=out/(str(st.st_mtime_ns)+'_'+str(time.monotonic_ns())+'_'+p.name)
                with p.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
                after=p.stat();same=(after.st_size,after.st_mtime_ns)==signature
                source_hash=digest(p);target_hash=digest(target)
                valid=same and source_hash==target_hash and target.stat().st_size==st.st_size
                receipt=dict(event='native_autosave_preserved',source=str(p),preserved=str(target),game_date=date,
                    bytes=st.st_size,source_sha256=source_hash,sha256=target_hash,stable_copy_verified=valid,
                    copied_after_measurement_date=eligible,copied_after_exit=exited)
                emit(receipt)
                with target.with_suffix('.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
                copied.add(token)
        except (OSError,ValueError) as e:emit(dict(event='read_or_copy_retry',file=str(p),error=type(e).__name__))
    if exit_seen is not None and time.monotonic()-exit_seen>4:break
    time.sleep(1)
emit(dict(event='watcher_finished',copies=len(copied)));events.close()
print(json.dumps({'watcher':a.trial,'finished':True,'copies':len(copied)}),flush=True)
