"""Finish a fresh contemporary A-B-B-A pair after interruption; keep old attempts."""
from pathlib import Path
import copy, hashlib, json, shutil
from simperf56_ai_cohorts import LAB
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before)
setup=json.loads((LAB/'SCORE_BASES_SETUP_20261118.json').read_text(encoding='utf-8'))
for row in setup['changes']:
    assert sha(Path(setup['overlay'])/row['file'])==row['diagnostic_file_sha256']
for label in ('ECNQ2','SCORQ2'):
    spec=plan['profiles'][label]
    assert not list((LAB/'runs').glob(label+'_*'))
    assert sha(Path(spec['path'])/'pdx_settings.json')==spec['settings_sha256']
    assert sha(spec['seed_path'])==spec['common_save_sha256']
specs={}
for label,parent in (('SCORQ3','SCORQ2'),('ECNQ3','ECNQ2')):
    old=plan['profiles'][parent];assert label not in plan['profiles']
    source=Path(old['seed_path']);profile=LAB/'profiles'/label;assert not profile.exists()
    (profile/'save games').mkdir(parents=True);seed=profile/'save games'/source.name;shutil.copyfile(source,seed)
    shutil.copyfile(Path(old['path'])/'pdx_settings.json',profile/'pdx_settings.json')
    shutil.copytree(Path(old['path'])/'user_bindings',profile/'user_bindings')
    shutil.copyfile(Path(old['path'])/'content_load.json',profile/'content_load.json')
    spec=copy.deepcopy(old);spec.update(path=str(profile),seed_path=str(seed),repetition_of=parent)
    assert sha(seed)==spec['common_save_sha256'];specs[label]=spec;plan['profiles'][label]=spec
with (LAB/'SCORE_RESUME_PLAN_BEFORE_20261119.json').open('xb') as f:f.write(before)
assert pp.read_bytes()==before;pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'SCORE_RESUME_SETUP_20261119.json').open('x',encoding='utf-8') as f:json.dump(dict(order=['ECNQ2','SCORQ2','SCORQ3','ECNQ3'],profiles=specs,prior_SCORQ1_retained_as_separate_session=True,prior_ECNQ1_no_simulated_days=True),f,indent=2)
print(json.dumps({'order':['ECNQ2','SCORQ2','SCORQ3','ECNQ3'],'prior_attempts_preserved':True}))
