"""Write an evidence index after completed experiments, without pooling distinct lots."""
import hashlib, json
from datetime import datetime, timezone
from simperf56_ai_cohorts import LAB, PARENT

out=PARENT/'ECONOMIC_GOALS_2026_11_18'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
labels=['SCORC1','ECNC1','ECNC2','SCORC2','AIOFFC1','VAN_OFFC1','VAN_ONC1','VAN_ONR1','VAN_OFFR1']
runs={}
for label in labels:
    p=LAB/(label+'_RESULTS.json');d=read(p)
    assert d['complete_14_28_56'] and d['native_autosave_treatment_verified']
    w=[w for w in d['heartbeat_windows'] if w['window'] in d['accepted_windows']]
    runs[label]=dict(result=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        windows=[{k:x[k] for k in ('simulated_days','wall_seconds','cpu_machine_percent_approx','working_set_mib_mean')} for x in w],
        native_post_proof=d['native_proof'],source_proof=d['source_proof'])
data=dict(utc=datetime.now(timezone.utc).isoformat(),issue=56,lab=str(LAB),
    gameplay_preserving_optimization_validated=False,experimental_gameplay_changes_integrated=False,
    current_runs=runs,
    score_experiment=dict(order=['SCORC1','ECNC1','ECNC2','SCORC2'],
        changes='12 building ai_value callbacks replaced by their own bases in 9 files; all controllers and objectives retained',
        conclusion='No measured gain in either paired repetition. Two processes per condition do not establish an intrinsic regression.',
        normal_mean_seconds_56=95,diagnostic_mean_seconds_56=101,
        post_state='83 serialized sections equal in both April 1 pairs; only local_date_time differs; does not establish identical intermediate decisions or callback invocation.'),
    expansion_goal_experiment=dict(persistent_ablation_verified=False,
        evidence=['EXB1_PRE_GOAL_PROOF.json','EXB1_POST_GOAL_PROOF.json','EXB3_POST_GOAL_PROOF.json'],
        conclusion='All 400 removed objectives are already recreated in a native January 4 save. EXB1 timing is not a valid measurement of disabling expansion.'),
    restrictions=['Native one-second timestamps, nested 14/28/56 windows, no FPS measurement.',
        'Distinct historical settings and baseline lots are not pooled.',
        'No continuous certification of foreground state, physical-user input or automatic pauses.',
        'AI ablations change gameplay and do not partition CPU costs additively.',
        'Vanilla 1836 and mod 1776 have different world states and country populations.',
        'Script profiling is separate from standard throughput and does not expose all native engine costs.'],
    next_experiment='Persistently isolate one native economic decision category, with verified activity and contemporary controls; prioritize construction/profitability and PM evaluation. Do not rely on deleting regenerated goal instances.',
    native_script_profile=str(LAB/'PROFC1_SCRIPT_PROFILE_RESULTS.json'),
    native_script_profile_scope='5003 entries with declared seconds and call counts; 8 of 12 score callback locations observed. Separate profile includes paused UI periods and autosave, not an exclusive full native CPU profile.',
    measurement_quality=str(out/'MEASUREMENT_QUALITY.json'),csv=str(out/'MEASUREMENTS.csv'))
with (out/'SUMMARY.json').open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,ensure_ascii=False)
print(json.dumps({'runs':list(runs),'optimization_validated':False,'summary':str(out/'SUMMARY.json')}))
