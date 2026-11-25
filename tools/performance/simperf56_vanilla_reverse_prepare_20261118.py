"""Create a reversed repetition from intact initial seeds, never from autosaves."""
from pathlib import Path
import copy, hashlib, json, shutil
from simperf56_ai_cohorts import LAB
pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before)
settings=(LAB/'profiles/ECNQ2/pdx_settings.json').read_bytes()
assert hashlib.sha256(settings).hexdigest()=='718eb8e11996500326bb3753c59f66b8513983bb8fc86e19eb2b782b8caafeaa'
specs={}
for label,parent in (('VAN_OFFQ2','VAN_OFFQ1'),('VAN_ONQ2','VAN_ONQ1')):
    old=plan['profiles'][parent];source=Path(old['seed_path'])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==old['common_save_sha256']
    assert label not in plan['profiles']
    profile=LAB/'profiles'/label;assert not profile.exists();(profile/'save games').mkdir(parents=True)
    seed=profile/'save games'/(label+'_S0.v3');shutil.copyfile(source,seed)
    (profile/'pdx_settings.json').write_bytes(settings)
    shutil.copytree(LAB/'profiles/VAN_OFF3/user_bindings',profile/'user_bindings')
    (profile/'content_load.json').write_text(json.dumps(dict(enabledMods=[{'path':x} for x in old['mods']],disabledDLC=[],enabledUGC=[]),indent=2),encoding='utf-8')
    spec=copy.deepcopy(old);spec.update(path=str(profile),seed_path=str(seed),repetition_of=parent)
    plan['profiles'][label]=spec;specs[label]=spec
with (LAB/'VANILLA_REVERSE_PLAN_BEFORE_20261118.json').open('xb') as f:f.write(before)
assert pp.read_bytes()==before;pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'VANILLA_REVERSE_SETUP_20261118.json').open('x',encoding='utf-8') as f:json.dump(dict(order=list(specs),profiles=specs,only_initial_seed_files_copied=True,autosaves_not_used_as_start=True),f,indent=2)
print(json.dumps({'prepared':list(specs),'same_initial_seed_hashes':True}))
