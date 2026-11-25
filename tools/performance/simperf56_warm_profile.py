"""Prepare a fresh process profile from the late isolated MAIN3 save only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('save',type=Path)
args=parser.parse_args()
planpath=REPORT/'PREPARATION.json';oldplan=planpath.read_bytes();plan=json.loads(oldplan)
lab=Path(plan['lab']);seed=lab/'profiles/MAIN3';source=args.save.resolve()
assert source.parent==(seed/'save games').resolve(),'Use the isolated MAIN3 save only.'
with source.open('rb') as stream:head=stream.read(4096)
found=re.search(rb'\bgame_date=(\d+)\.(\d+)\.(\d+)',head)
assert found and int(found[1])>=1777,'The world must already have completed a year.'
saved_date='.'.join(x.decode() for x in found.groups())
source_hash=sha(source)
profile=lab/'profiles/WARM1';profile.mkdir()
settings=(REPORT/'runtime/MAIN2_20261117T022325277Z/SETTINGS.json').read_bytes()
(profile/'pdx_settings.json').write_bytes(settings)
for folder in ('shadercache','user_bindings'):
    if (seed/folder).exists():shutil.copytree(seed/folder,profile/folder)
(profile/'save games').mkdir();shutil.copyfile(source,profile/'save games'/source.name)
assert sha(profile/'save games'/source.name)==source_hash
mods=[{'path':Path(plan[key]).as_posix()} for key in ('main_frozen','telemetry')]
(profile/'content_load.json').write_text(json.dumps(dict(enabledMods=mods,disabledDLC=[],enabledUGC=[]),indent=2),encoding='utf-8')
plan['profiles']['WARM1']=dict(path=str(profile),mods=[p['path'] for p in mods],settings_sha256=sha(profile/'pdx_settings.json'),expected_year=int(found[1]),common_save_sha256=source_hash,saved_date=saved_date)
assert planpath.read_bytes()==oldplan
(REPORT/'PREPARATION_BEFORE_WARM.json').write_bytes(oldplan)
planpath.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
result=dict(utc=datetime.now(timezone.utc).isoformat(),profile=str(profile),saved_date=saved_date,save=str(source),save_sha256=source_hash,
 note='Fresh process, mature world. Use native DAY endpoints FIRST_AFTER_LOAD_14/28/56. If saved on January 1, NEXT_JANUARY events remain pending; keep after those events until the heartbeat target.',
 launch_arguments='-Trial WARM1 -MaxSeconds 1800 -KeepAfterWindows -StopAfterHeartbeatDays 91')
with (REPORT/'WARM_PREPARATION.json').open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,ensure_ascii=False)
print(json.dumps(result,indent=2,ensure_ascii=False))
