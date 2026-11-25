"""Prepare reverse vanilla repetitions after contradictory C1 results, outside the repo."""
import copy,hashlib,json,shutil
from pathlib import Path
from simperf56_ai_cohorts import LAB
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pp=LAB/'PREPARATION.json';old=pp.read_bytes();plan=json.loads(old);created={}
for label,parent in [('VAN_ONR1','VAN_ONC1'),('VAN_OFFR1','VAN_OFFC1')]:
    assert label not in plan['profiles'];base=plan['profiles'][parent]
    runs=list((LAB/'runs').glob(parent+'_*'));assert len(runs)==1
    run=runs[0];assert (run/'EXIT.json').exists()
    seed_source=Path(base['seed_path']);assert sha(seed_source)==base['common_save_sha256']
    assert sha(run/'SETTINGS.json')==base['settings_sha256']
    dest=LAB/'profiles'/label;assert not dest.exists();(dest/'save games').mkdir(parents=True)
    seed=dest/'save games'/seed_source.name;shutil.copyfile(seed_source,seed)
    shutil.copyfile(run/'SETTINGS.json',dest/'pdx_settings.json')
    shutil.copyfile(run/'CONTENT_LOAD.json',dest/'content_load.json')
    shutil.copytree(Path(base['path'])/'user_bindings',dest/'user_bindings')
    shutil.copytree(Path(base['path'])/'shadercache',dest/'shadercache')
    spec=copy.deepcopy(base);spec.update(path=str(dest),seed_path=str(seed),
        comparison_group='stable_controls_vanilla_reverse_ON_OFF_20261119')
    plan['profiles'][label]=spec;created[label]=spec
with (LAB/'VANILLA_REPEAT_PLAN_BEFORE_20261119.json').open('xb') as f:f.write(old)
assert pp.read_bytes()==old;pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'VANILLA_REPEAT_SETUP_20261119.json').open('x',encoding='utf-8') as f:
    json.dump(dict(reason='C1 pair contradicts Q1; no pooled vanilla effect accepted.',
        order=list(created),profiles=created,settings_unchanged=True,
        preparation_target='Approximately 90 seconds paused after Continue for each; actual times recorded, no claim of exact equality.'),f,indent=2)
print(json.dumps(dict(prepared=list(created),cache_copied=True)))
