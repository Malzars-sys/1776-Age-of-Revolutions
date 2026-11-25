"""Issue 56: short external paths, preserved sources, one-variable HRE lab."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,re,shutil,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
REPORT=OLD/'STATE_INVESTIGATION_2026_11_17'
LAB=Path('C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117')
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,indent=2,ensure_ascii=False);f.write('\n')
def snapshot():
 old=json.loads((OLD/'RELOAD_EXPERIMENT_2026_11_17/PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
 groups={k:{p:sha(p) for p in v} for k,v in old['groups'].items()}
 groups['prior_evidence']={str(p):sha(p) for p in OLD.rglob('*') if p.is_file() and REPORT not in p.parents}
 groups['tools']={str(p):sha(p) for p in (ROOT/'tools/performance').glob('*') if p.is_file()}
 return dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],text=True,cwd=ROOT).strip(),groups=groups)
def initialize():
 assert not LAB.exists(),'Preserve an existing laboratory.'
 LAB.mkdir();REPORT.mkdir(exist_ok=True)
 plan=json.loads((OLD/'PREPARATION.json').read_text(encoding='utf-8'))
 frozen=json.loads((Path(plan['lab'])/'FROZEN_MANIFEST.json').read_text(encoding='utf-8'))
 assert all(sha(Path(plan['main_frozen'])/rel)==v['sha256'] for rel,v in frozen['files'].items())
 assert sha(plan['executable'])==plan['executable_sha256']
 write(LAB/'PRESERVATION_BEFORE.json',snapshot())
 write(LAB/'SOURCE_PLAN.json',plan)
 # Existing launch/observer logic, with output and plan externalized only.
 launch=(ROOT/'tools/performance/simperf56_start_trial.ps1').read_text(encoding='utf-8-sig')
 launch=launch.replace("$report56=Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'", "$report56=$PSScriptRoot")
 launch=launch.replace("('runtime/'+$Trial+", "('runs/'+$Trial+")
 launch=launch.replace("$observerScript56=Join-Path $PSScriptRoot 'simperf56_observe.ps1'", "$observerScript56='"+str(ROOT/'tools/performance/simperf56_observe.ps1')+"'")
 (LAB/'run_trial.ps1').write_text(launch,encoding='utf-8-sig')
 diag=LAB/'no_hre_monthly';shutil.copytree(plan['main_frozen'],diag)
 sys.path.insert(0,str(ROOT/'tools'));from validate_diplomacy_ottoman_1776 import parse
 rel='common/on_actions/1776_imperial_constitution.txt';p=diag/rel;raw=p.read_bytes();text=raw.decode('utf-8-sig')
 nodes=[n for n in parse(text) if n.key=='aor1776_hre_monthly_hook'];assert len(nodes)==1;n=nodes[0]
 body='''aor1776_hre_monthly_hook = {
 effect = {
  debug_log = "SIM56|DIAG|HRE_MONTHLY_BYPASSED|date=[TimeKeeper.GetCurrentDate.GetString]"
 }
}'''
 new=text[:n.start]+body+text[n.end:];assert len(parse(new))==len(parse(text))
 p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+new.encode('utf-8'))
 diff=[r for r,v in frozen['files'].items() if sha(diag/r)!=v['sha256']];assert diff==[rel]
 (LAB/'HRE_MONTHLY_BEFORE.txt').write_bytes(raw)
 write(LAB/'HRE_MONTHLY_VARIANT.json',dict(changed_files=diff,source_sha256=hashlib.sha256(raw).hexdigest(),diagnostic_sha256=sha(p),scope='Only monthly HRE hook body bypassed. Daily HRE and regional AI files intact. Daily guard scheduling by this monthly hook necessarily absent; other daily schedules unchanged. Gameplay-changing diagnostic, not optimization.'))
 plan['profiles']={};plan['lab']=str(LAB);write(LAB/'PREPARATION.json',plan)
 write(REPORT/'LAB_LOCATION.json',dict(lab=str(LAB),runtime_evidence=str(LAB/'runs'),source_frozen=plan['main_frozen'],bulky_evidence_in_repository=False))
 print(json.dumps(dict(lab=str(LAB),changed_files=diff,exe=plan['executable']),indent=2))
def profile(label,runtime=None,save=None):
 assert re.fullmatch('[A-Z][A-Z0-9_]{2,30}',label)
 pp=LAB/'PREPARATION.json';raw=pp.read_bytes();plan=json.loads(raw);assert label not in plan['profiles']
 original=json.loads((LAB/'SOURCE_PLAN.json').read_text(encoding='utf-8'))
 source=Path(save) if save else Path(original['lab'])/'profiles/MAIN3/save games/royaume de france_1776_01_01.v3'
 assert source.is_file() and 'Temp' in source.parts
 path=LAB/'profiles'/label;assert not path.exists();path.mkdir(parents=True)
 settings=(OLD/'runtime/MAIN2_20261117T022325277Z/SETTINGS.json').read_bytes();(path/'pdx_settings.json').write_bytes(settings)
 seed=Path(original['lab'])/'profiles/MATURE1'
 for folder in ('shadercache','user_bindings'):
  if (seed/folder).exists():shutil.copytree(seed/folder,path/folder)
 (path/'save games').mkdir();shutil.copyfile(source,path/'save games'/source.name)
 date=re.search(rb'\bgame_date=(\d+)\.(\d+)\.(\d+)',source.open('rb').read(4096));assert date
 runtime=Path(runtime) if runtime else Path(original['main_frozen'])
 mods=[runtime.as_posix(),Path(original['telemetry']).as_posix()]
 write(path/'content_load.json',dict(enabledMods=[dict(path=x) for x in mods],disabledDLC=[],enabledUGC=[]))
 spec=dict(path=str(path),mods=mods,settings_sha256=sha(path/'pdx_settings.json'),expected_year=int(date[1]),saved_date='.'.join(x.decode() for x in date.groups()),common_save_sha256=sha(source))
 assert sha(path/'save games'/source.name)==spec['common_save_sha256']
 plan['profiles'][label]=spec;(LAB/('PLAN_BEFORE_'+label+'.json')).write_bytes(raw)
 assert pp.read_bytes()==raw;pp.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
 write(LAB/('PROFILE_'+label+'.json'),spec);print(json.dumps(dict(trial=label,**spec),indent=2))
def audit():
 before=json.loads((LAB/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'));groups={}
 for group,paths in before['groups'].items():
  changes=[p for p,h in paths.items() if not Path(p).is_file() or sha(p)!=h]
  groups[group]=dict(checked=len(paths),unchanged=len(paths)-len(changes),changes=changes)
 out=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],text=True,cwd=ROOT).strip(),groups=groups)
 write(LAB/'PRESERVATION_AFTER.json',out);write(REPORT/'PRESERVATION_AFTER.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=('init','profile','audit'));ap.add_argument('label',nargs='?');ap.add_argument('--runtime');ap.add_argument('--save');a=ap.parse_args()
 if a.action=='init':initialize()
 elif a.action=='profile':profile(a.label,a.runtime,a.save)
 else:audit()
