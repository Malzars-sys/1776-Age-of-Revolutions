"""Prepare a current AI-off control and a separate native-profiler session."""
from pathlib import Path
import copy, hashlib, json, re, shutil
from simperf56_ai_cohorts import LAB
from simperf56_save_state import sections

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before)
base=plan['profiles']['ECNC2'];source=Path(base['seed_path'])
assert sha(source)==base['common_save_sha256']
runs=list((LAB/'runs').glob('ECNC2_*'));assert len(runs)==1
assert sha(runs[0]/'SETTINGS.json')==base['settings_sha256']
raw=source.read_bytes();text=raw.decode('utf-8-sig');a,b=sections(text)['ai'];part=text[a:b]
yes=r'(?m)^([ \t]*enabled=)yes(?=\r?$)';no=r'(?m)^([ \t]*enabled=)no(?=\r?$)'
assert len(re.findall(yes,part))==646 and not re.search(no,part)
off,n=re.subn(yes,r'\g<1>no',part);assert n==646
assert re.sub(no,r'\g<1>yes',off)==part
offraw=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+(text[:a]+off+text[b:]).encode('utf-8')
assert len(offraw)==len(raw)-646
offpath=LAB/'S0_ALL_OFF_C_SPEED5.v3'
with offpath.open('xb') as f:f.write(offraw)
receiptpath=LAB/'CURRENT_AI_PROFILE_SETUP_20261119.json'
specs={}
for label,seed_source in [('AIOFFC1',offpath),('PROFC1',source)]:
    assert label not in plan['profiles'];profile=LAB/'profiles'/label;assert not profile.exists()
    (profile/'save games').mkdir(parents=True);seed=profile/'save games'/seed_source.name
    shutil.copyfile(seed_source,seed)
    shutil.copyfile(runs[0]/'SETTINGS.json',profile/'pdx_settings.json')
    shutil.copyfile(runs[0]/'CONTENT_LOAD.json',profile/'content_load.json')
    shutil.copytree(Path(base['path'])/'user_bindings',profile/'user_bindings')
    spec=copy.deepcopy(base)
    spec.update(path=str(profile),seed_path=str(seed),common_save_sha256=sha(seed),
        expected_enabled='no' if label=='AIOFFC1' else 'yes',
        diagnostic_cohort='OFF' if label=='AIOFFC1' else 'ON',
        comparison_group='stable_controls_AI_global_20261119' if label=='AIOFFC1' else 'DEDICATED_SCRIPT_PROFILING_NOT_THROUGHPUT',
        setup_proof=str(receiptpath),not_a_throughput_benchmark=label=='PROFC1')
    specs[label]=spec;plan['profiles'][label]=spec
backup=LAB/'PROFC1_PREPARED_SOURCE_PRESERVED.v3'
shutil.copyfile(source,backup);assert sha(backup)==base['common_save_sha256']
with (LAB/'CURRENT_AI_PROFILE_PLAN_BEFORE_20261119.json').open('xb') as f:f.write(before)
assert pp.read_bytes()==before
pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with receiptpath.open('x',encoding='utf-8') as f:
    json.dump(dict(profiles=specs,source_normal=str(source),source_normal_sha256=sha(source),
        source_off=str(offpath),source_off_sha256=sha(offpath),
        changed_fields=646,only_change='Every AI-controller enabled=yes becomes enabled=no; all other source bytes preserved.',
        restoring_flags_reconstructs_normal_source_exactly=True,
        original_source_preserved=str(backup),original_source_copy_sha256=sha(backup),
        PROF_scope='Separate supported native script profiler. No profiling run is accepted as a standard throughput benchmark.'),f,indent=2)
print(json.dumps({'profiles':list(specs),'flag_changes':646,'only_flags_changed':True}))
