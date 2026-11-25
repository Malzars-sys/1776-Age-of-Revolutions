"""Accept native DAY windows only with an intact seed and native autosave witness."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
import argparse, hashlib, json, re, shutil
from simperf56_ai_cohorts import LAB
from simperf56_analyze import analyze, game_date
from simperf56_economic_goals_20261118 import goal_state

ap=argparse.ArgumentParser();ap.add_argument('trial');a=ap.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=read(LAB/'PREPARATION.json');spec=plan['profiles'][a.trial];year=spec['expected_year']
setup_path=Path(spec.get('setup_proof',LAB/('QUARTER_REFERENCE_SETUP_20261118.json' if year==1836 else 'SCORE_BASES_SETUP_20261118.json')))
setup=read(setup_path)
assert spec['common_save_sha256']==sha(Path(spec['seed_path']))
seed_receipt=dict(trial=a.trial,phase='SOURCE_NOT_NATIVE_PRE',save=spec['seed_path'],sha256=spec['common_save_sha256'],
    seed_integrity_verified=True,setup=str(setup_path))
source_proof_path=LAB/(a.trial+'_SOURCE_PROOF.json')
if source_proof_path.exists():assert read(source_proof_path)==seed_receipt
else:
    with source_proof_path.open('x',encoding='utf-8') as f:json.dump(seed_receipt,f,indent=2)
witness_dir=LAB/'autosave_witnesses'/a.trial
records=[read(p) for p in witness_dir.glob('*.json')]
witnesses=[d for d in records if d.get('event')=='native_autosave_preserved' and d['stable_copy_verified'] and d['game_date'] and tuple(map(int,d['game_date'].split('.')))[:3]>=(year,3,1)]
assert witnesses,'No stable native post-window autosave: no validated result'
witness=min(witnesses,key=lambda d:tuple(map(int,d['game_date'].split('.'))));save=Path(witness['preserved'])
assert sha(save)==witness['sha256']
text=save.read_text(encoding='utf-8-sig');actual=goal_state(text)
assert re.search(r'(?m)^speed=(\d+)',text)[1]=='4'
expected=setup['source_controller_ids'] if year==1836 else read(LAB/'ECONOMIC_SOURCE_GOALS_20261118.json')['controllers']
wrong={k:x['enabled'] for k,x in actual.items() if x['enabled']!=spec['expected_enabled']}
missing=sorted(set(expected)-set(actual));new=sorted(set(actual)-set(expected));goal_diff={}
if year==1776:
    goal_diff={k:dict(expected=expected[k]['goals'],actual=actual[k]['goals']) for k in set(expected)&set(actual) if expected[k]['goals']!=actual[k]['goals']}
proof=dict(trial=a.trial,phase='POST',save=str(save),sha256=sha(save),date=witness['game_date'],controllers=len(actual),
    enabled_counts=dict(Counter(x['enabled'] for x in actual.values())),expected_flag=spec['expected_enabled'],
    unexpected_flags=wrong,missing_controllers=missing,new_controllers=new,goal_differences=goal_diff,
    native_autosave=True,source_is_prepared_save_not_native_PRE=True,
    treatment_verified=not wrong and not goal_diff,
    population_evolution_explicitly_accounted=True,
    validation_rule='Every present controller must have the intended flag; initial missing and newly created IDs are retained explicitly. A fixed post-run country count is not required for an evolving world.',
    actual={k:dict(controller_id=v['controller_id'],enabled=v['enabled'],goals=v['goals']) for k,v in actual.items()})
proofpath=LAB/(a.trial+'_POST_'+('AI_PROOF' if year==1836 else 'GOAL_PROOF')+'.json')
if proofpath.exists():
    previous=read(proofpath)
    assert previous['save']==proof['save'] and previous['sha256']==proof['sha256'] and previous['unexpected_flags']==proof['unexpected_flags']
    proof['previous_count_check_retained_at']=str(proofpath)
    proof['review_reason']='The prior fixed-population check rejected natural country creation even though every controller had the intended flag. No flag requirement has been relaxed.'
    proofpath=proofpath.with_name(proofpath.stem+'_POPULATION_REVIEW.json')
with proofpath.open('x',encoding='utf-8') as f:json.dump(proof,f,indent=2)
assert proof['treatment_verified'],'Native autosave treatment check failed'
runs=list((LAB/'runs').glob(a.trial+'_*'));assert len(runs)==1
raw=runs[0];exit_data=read(raw/'EXIT.json');assert exit_data
dest=LAB/'analysis'/a.trial;assert not dest.exists();dest.mkdir();(dest/'logs').mkdir()
manifest=dict(raw_run=str(raw),excluded_tail=[],files={})
for name in ('LAUNCH.json','OBSERVER.json','CONTINUOUS_CPU_RAM.csv'):shutil.copyfile(raw/name,dest/name)
for p in (raw/'logs').glob('debug*.log'):
    content=p.read_bytes();lines=content.splitlines(keepends=True);kept=[]
    for i,line in enumerate(lines):
        s=line.decode('utf-8-sig',errors='replace')
        if 'SIM56|DAY|date=' in s and game_date(s.split('SIM56|DAY|date=',1)[1].strip()) is None:
            assert p.name=='debug.log' and i==len(lines)-1 and not line.endswith((b'\r',b'\n'))
            manifest['excluded_tail'].append(dict(file=p.name,line=s));continue
        kept.append(line)
    clean=b''.join(kept);(dest/'logs'/p.name).write_bytes(clean)
    manifest['files'][p.name]=dict(source_sha256=hashlib.sha256(content).hexdigest(),analysis_sha256=hashlib.sha256(clean).hexdigest())
result=analyze(dest);assert result['heartbeat_sequence_consecutive']
accepted=[w for w in result['heartbeat_windows'] if w['window'].startswith('FIRST_AFTER_LOAD_')]
assert [w['simulated_days'] for w in accepted]==[14,28,56]
actions=[json.loads(s) for s in (LAB/'actions'/(a.trial+'.jsonl')).read_text(encoding='utf-8').splitlines()]
starts=[d for d in actions if d['event']=='unpause_for_native_DAY_windows']
reconciliation_path=LAB/(a.trial+'_START_RECONCILIATION.json')
if len(starts)>1:
    reconciliation=read(reconciliation_path)
    assert len(starts)==2 and reconciliation['retained_input_verified'] is True
    assert reconciliation['observed_paused_date']==f'{year}.1.1'
    assert starts[0]['utc']==reconciliation['superseded_attempt_utc']
    assert starts[1]['utc']==reconciliation['retained_start_utc']
    starts=starts[1:]
operator_assisted=False
if not starts or (LAB/(a.trial+'_OPERATOR_START_REQUEST.json')).exists():
    request=read(LAB/(a.trial+'_OPERATOR_START_REQUEST.json'))
    assert request['event']=='operator_start_requested' and request['exact_click_time_known'] is False
    starts=[request];operator_assisted=True
assert len(starts)==1
start=datetime.fromisoformat(starts[0]['utc'].replace('Z','+00:00'));end=datetime.fromisoformat(exit_data['ended_utc'].replace('Z','+00:00'))
for w in accepted:
    assert game_date(w['start']['date_raw']).isoformat()==f'{year}-01-02'
    assert start-timedelta(seconds=1)<=datetime.fromisoformat(w['start']['utc']) and datetime.fromisoformat(w['end']['utc'])<=end
events=[json.loads(s) for s in (witness_dir/'FILE_EVENTS.jsonl').read_text(encoding='utf-8').splitlines()]
inside=[d for d in events if d['event']=='native_autosave_file_observed' and d.get('game_date') and (year,1,2)<=tuple(map(int,d['game_date'].split('.')))[:3]<(year,3,1)]
assert not inside,'Autosave occurred inside the measurement period'
ready=read(witness_dir/'WATCHER_READY.json');assert datetime.fromisoformat(ready['utc'])<=start
post_start_actions=[d for d in actions if datetime.fromisoformat(d['utc'].replace('Z','+00:00'))>start]
assert not post_start_actions,'Investigate UI actions after starting before accepting a continuous run'
result.update(raw_run=str(raw),accepted_windows=[w['window'] for w in accepted],complete_14_28_56=True,
    expected_first_complete_day=f'{year}-01-02',method='continuous_with_native_quarter_autosave',
    native_autosave_treatment_verified=True,seed_integrity_verified=True,no_autosave_inside_measurement=True,
    native_proof=str(proofpath),source_proof=str(LAB/(a.trial+'_SOURCE_PROOF.json')),
    native_autosave_witness=witness,measurement_start_action=starts[0],analysis_input_manifest=manifest,
    operator_assisted=operator_assisted,exact_unpause_click_time_known=not operator_assisted,
    start_reconciliation=str(reconciliation_path) if reconciliation_path.exists() else None,
    quality_note='Native timestamps only; first partial day and all post-window autosave/copy work excluded. Continuous run has no recorded agent input after starting. Initial proof is the verified prepared seed, not a native PRE saved in the UI. Physical-user or automatic pauses cannot be excluded by the native DAY sequence alone.')
with (LAB/(a.trial+'_RESULTS.json')).open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps(dict(trial=a.trial,post_date=proof['date'],controllers=proof['controllers'],flags=proof['enabled_counts'],
    accepted=[{k:w[k] for k in ('window','wall_seconds','cpu_machine_percent_approx')} for w in accepted]),indent=2))
