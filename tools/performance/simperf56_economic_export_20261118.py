"""Export existing native-clock evidence; never accept a failed goal treatment."""
from pathlib import Path
import argparse, csv, hashlib, json
from datetime import datetime
from simperf56_ai_cohorts import LAB, PARENT

OUT = PARENT / 'ECONOMIC_GOALS_2026_11_18'
ap=argparse.ArgumentParser();ap.add_argument('--dry-run',action='store_true');args=ap.parse_args()
TRIALS = ('AI_OFF3R', 'AI_ON3', 'AI_DEC1', 'AI_OTHER1', 'AI_DEC2',
          'AI_ON4', 'AI_ON4R', 'AI_OFF4', 'ECN1', 'EXB1', 'VAN_ON2', 'VAN_OFF2',
          'VAN_ON3', 'VAN_OFF3', 'VAN_ONQ1', 'VAN_OFFQ1', 'VAN_OFFQ2', 'VAN_ONQ2',
          'SCORQ1', 'ECNQ1', 'ECNQ2', 'SCORQ2', 'SCORQ3', 'ECNQ3',
          'ECNG1', 'SCORG1', 'SCORG2', 'ECNG2', 'VAN_OFFG1', 'VAN_ONG1',
          'SCORP1','ECNP1','VAN_OFFP1','VAN_ONP1',
          'SCORC1','ECNC1','ECNC2','SCORC2','AIOFFC1','VAN_OFFC1','VAN_ONC1',
          'VAN_ONR1','VAN_OFFR1','PROFC1')

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def receipt(p):
    d = read(p)
    return dict(file=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                **{k: d[k] for k in ('date', 'controllers', 'enabled_counts', 'treatment_verified',
                    'all_present_controllers_match_expected', 'missing_initial_controllers',
                    'missing_controllers', 'new_controllers') if k in d},
                target_goal_remaining_count=len(d.get('target_goal_remaining', {})),
                unexpected_flags_count=len(d.get('unexpected_flags', {})))

rows=[]; quality={}
for trial in TRIALS:
    if trial=='PROFC1':
        profile=LAB/'PROFC1_SCRIPT_PROFILE_RESULTS.json'
        assert profile.exists()
        quality[trial]={'status':'PROFILE_ONLY_NOT_A_THROUGHPUT_BENCHMARK',
            'profile_evidence':str(profile),'native_post_proof':str(LAB/'PROFC1_POST_GOAL_PROOF.json')}
        continue
    p=LAB/(trial+'_RESULTS.json')
    if not p.exists():
        quality[trial]={'status':'NOT_COMPLETED_NO_RESULT'}
        continue
    d=read(p)
    accepted=d.get('accepted_windows')
    derived_fields=[]
    if accepted is None:
        assert trial=='AI_OFF3R'
        accepted=[w['window'] for w in d['heartbeat_windows'] if w['window'].startswith('FIRST_AFTER_LOAD_')]
        actions=[json.loads(line) for line in (LAB/'actions'/(trial+'.jsonl')).read_text(encoding='utf-8').splitlines()]
        pause=next(x['utc'] for x in actions if x['event']=='pause_after_measurement')
        pause=datetime.fromisoformat(pause.replace('Z','+00:00'))
        assert all(datetime.fromisoformat(w['end']['utc'])<pause for w in d['heartbeat_windows'] if w['window'] in accepted)
        derived_fields.append('accepted_windows: actual FIRST_AFTER_LOAD endpoints before recorded pause')
    complete={w['simulated_days'] for w in d['heartbeat_windows'] if w['window'] in accepted}=={14,28,56}
    if 'complete_14_28_56' in d:assert d['complete_14_28_56']==complete
    else:derived_fields.append('complete_14_28_56: actual accepted 14/28/56 DAY windows')
    raw_run=d.get('raw_run',d['run'])
    quarter=d.get('method')=='continuous_with_native_quarter_autosave'
    if quarter:
        proofs=[receipt(Path(d['source_proof'])),receipt(Path(d['native_proof']))]
        valid=d['native_autosave_treatment_verified'] and d['seed_integrity_verified'] and d['no_autosave_inside_measurement']
        if trial.startswith('SCOR') and trial!='SCORQ1':
            rp=LAB/(trial+'_RUNTIME_SCORE_PROOF.json')
            valid=valid and rp.exists() and read(rp)['actual_engine_loaded_changes_verified']
    else:
        proofs=[receipt(q) for phase in ('PRE','POST') for suffix in ('AI_PROOF','GOAL_PROOF')
                if (q:=LAB/(trial+'_'+phase+'_'+suffix+'.json')).exists()]
        valid=len(proofs)==2 and not any(x.get('treatment_verified') is False or
              x['unexpected_flags_count'] for x in proofs)
    status='VALIDATED' if valid else 'INVALID_TREATMENT'
    if quarter and valid:status='VALIDATED_SOURCE_AND_NATIVE_AUTOSAVE_POST'
    if valid and not complete:status+='__PARTIAL_WINDOWS_ONLY'
    if trial=='EXB1':
        assert any(x.get('treatment_verified') is False for x in proofs)
        status='INVALID_RECREATED_OBJECTIVES'
    missing=sorted({str(x.get('country_id',x)) if isinstance(x,dict) else str(x)
                    for proof in proofs for key in ('missing_initial_controllers','missing_controllers')
                    for x in proof.get(key,[])})
    if valid and missing:status='VALID_PRESENT_FLAGS_WITH_MISSING_CONTROLLER'
    view_path=LAB/(trial+'_VIEW_COMPARABILITY.json')
    view=read(view_path) if view_path.exists() else None
    causal_valid=valid and not (view and view.get('causal_performance_comparison_accepted') is False)
    if valid and not causal_valid:status='VALID_TREATMENT__UI_VIEW_CONFOUNDED'
    if missing:
        causal_valid=False
    if trial=='SCORQ1':
        status='NO_COMPLETED_CONTEMPORARY_CONTROL'
        causal_valid=False
    if trial=='ECNG1':
        status='VALID_BASELINE__PAIRED_DIAGNOSTIC_UI_CONFOUNDED'
        causal_valid=False
    if trial in ('VAN_OFFC1','VAN_ONC1'):
        status='VALID_TREATMENT__UNEQUAL_PAUSED_PREPARATION__EXPLORATORY'
        causal_valid=False
    quality[trial]=dict(status=status, proofs=proofs, complete=complete,
                       raw_run=raw_run, accepted_windows=accepted,legacy_fields_derived=derived_fields,
                       source_is_native_PRE=not quarter,operator_assisted=d.get('operator_assisted',False),
                       view_comparability=view,causal_treatment_comparison_accepted=causal_valid,
                       continuous_foreground_or_physical_user_pause_absence_certified=False,
                       timing_resolution_absolute_error_seconds_less_than=1)
    for w in d['heartbeat_windows']:
        if w['window'] not in accepted:continue
        if quarter:
            group = ('stable_controls_mod_ABBA_20261119' if trial in ('SCORC1','ECNC1','ECNC2','SCORC2') else
                     'stable_controls_mod_AI_OFF_positive_control_20261119' if trial=='AIOFFC1' else
                     'stable_controls_vanilla_OFF_ON_20261119' if trial in ('VAN_OFFC1','VAN_ONC1') else
                     'stable_controls_vanilla_reverse_ON_OFF_20261119' if trial in ('VAN_ONR1','VAN_OFFR1') else
                     'pulse_mod_pair_20261119' if trial in ('SCORP1','ECNP1') else
                     'pulse_vanilla_OFF_ON_20261119' if trial in ('VAN_OFFP1','VAN_ONP1') else
                     'secondary_vanilla_OFF_ON_20261119' if trial in ('VAN_OFFG1','VAN_ONG1') else
                     'secondary_mod_ABBA_20261119' if trial in ('ECNG1','SCORG1','SCORG2','ECNG2') else
                     'vanilla_quarter_pair1_20261118' if trial in ('VAN_ONQ1','VAN_OFFQ1') else
                     'vanilla_quarter_pair2_UNRUN' if trial in ('VAN_OFFQ2','VAN_ONQ2') else
                     'score_prior_session_NO_CONTEMPORARY_CONTROL' if trial=='SCORQ1' else
                     'score_interrupted_or_UNRUN')
        else:
            group = ('cohorts_day' if trial in ('AI_ON4R','AI_OFF4') else
                     'goal_persistence' if trial in ('ECN1','EXB1') else 'cohorts_night')
        rows.append(dict(trial=trial,world='vanilla_1836' if trial.startswith('VAN_') else 'mod_1776',comparison_group=group,
            days=w['simulated_days'],seconds=w['wall_seconds'],days_per_second=w['days_per_second'],
            cpu_machine_percent=w.get('cpu_machine_percent_approx'),
            working_set_mib=w.get('working_set_mib_mean'),quality=status,
            usable_for_causal_treatment_comparison=causal_valid,
            source_is_native_PRE=not quarter,operator_assisted=d.get('operator_assisted',False),
            start_utc=w['start']['utc'],end_utc=w['end']['utc']))
if not args.dry_run:
    with (OUT/'MEASUREMENTS.csv').open('x',encoding='utf-8-sig',newline='') as f:
        cw=csv.DictWriter(f,fieldnames=list(rows[0]));cw.writeheader();cw.writerows(rows)
    with (OUT/'MEASUREMENT_QUALITY.json').open('x',encoding='utf-8') as f:
        json.dump(quality,f,indent=2,ensure_ascii=False)
print(json.dumps({'rows':len(rows),'quality':{k:v['status'] for k,v in quality.items()}},indent=2))
