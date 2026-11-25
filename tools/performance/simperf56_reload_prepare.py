"""Append isolated profiles for mature-world/reload experiments. No Git writes."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
ROUND=REPORT/'RELOAD_EXPERIMENT_2026_11_17'
ROUND.mkdir(exist_ok=True)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('label');parser.add_argument('--save',type=Path);parser.add_argument('--seed',default='MAIN3');parser.add_argument('--runtime',type=Path)
args=parser.parse_args()
assert re.fullmatch('[A-Z][A-Z0-9_]{2,30}',args.label)
planpath=REPORT/'PREPARATION.json';oldplan=planpath.read_bytes();plan=json.loads(oldplan)
lab=Path(plan['lab']);profile=lab/'profiles'/args.label
assert args.label not in plan['profiles'] and not profile.exists(),'Preserve existing trial.'
head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==plan['reference_head']
assert sha(Path(plan['executable']))==plan['executable_sha256']
source=args.save or lab/'profiles/MAIN3/save games/royaume de france_1776_01_01.v3'
source=source.resolve();assert lab.resolve() in source.parents,'Only laboratory saves.'
with source.open('rb') as stream:header=stream.read(4096)
match=re.search(rb'\bgame_date=(\d+)\.(\d+)\.(\d+)',header);assert match
date='.'.join(x.decode() for x in match.groups())
seed=lab/'profiles'/args.seed;assert seed.is_dir()
profile.mkdir();settings=(REPORT/'runtime/MAIN2_20261117T022325277Z/SETTINGS.json').read_bytes()
(profile/'pdx_settings.json').write_bytes(settings)
for folder in ('shadercache','user_bindings'):
    if (seed/folder).exists():shutil.copytree(seed/folder,profile/folder)
(profile/'save games').mkdir();shutil.copyfile(source,profile/'save games'/source.name)
source_hash=sha(source);assert sha(profile/'save games'/source.name)==source_hash
runtime=args.runtime or Path(plan['main_frozen']);assert lab.resolve() in runtime.resolve().parents
mods=[{'path':p.as_posix()} for p in (runtime,Path(plan['telemetry']))]
(profile/'content_load.json').write_text(json.dumps(dict(enabledMods=mods,disabledDLC=[],enabledUGC=[]),indent=2),encoding='utf-8')
plan['profiles'][args.label]=dict(path=str(profile),mods=[p['path'] for p in mods],settings_sha256=sha(profile/'pdx_settings.json'),expected_year=int(match[1]),common_save_sha256=source_hash,saved_date=date)
archive=ROUND/('PLAN_BEFORE_'+args.label+'.json');assert not archive.exists();archive.write_bytes(oldplan)
assert planpath.read_bytes()==oldplan
planpath.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
record=dict(utc=datetime.now(timezone.utc).isoformat(),trial=args.label,profile=str(profile),source_save=str(source),saved_date=date,save_sha256=source_hash,runtime=str(runtime),settings_sha256=sha(profile/'pdx_settings.json'),reference_head=head)
with (ROUND/('PROFILE_'+args.label+'.json')).open('x',encoding='utf-8') as out:json.dump(record,out,indent=2,ensure_ascii=False)
print(json.dumps(record,indent=2,ensure_ascii=False))
