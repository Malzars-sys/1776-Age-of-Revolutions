"""Cross-check published local deliverables against native result receipts, read-only inputs."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,re
from simperf56_ai_cohorts import LAB,PARENT

out=PARENT/'ECONOMIC_GOALS_2026_11_18'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
quality=read(out/'MEASUREMENT_QUALITY.json')
with (out/'MEASUREMENTS.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==71
seen=set()
for row in rows:
    trial=row['trial'];days=int(row['days']);assert (trial,days) not in seen;seen.add((trial,days))
    d=read(LAB/(trial+'_RESULTS.json'))
    windows=[w for w in d['heartbeat_windows'] if w['window'].startswith('FIRST_AFTER_LOAD_') and w['simulated_days']==days]
    assert len(windows)==1;(w,)=windows
    assert float(row['seconds'])==w['wall_seconds']
    assert row['start_utc']==w['start']['utc'] and row['end_utc']==w['end']['utc']
    assert (datetime.fromisoformat(row['end_utc'])-datetime.fromisoformat(row['start_utc'])).total_seconds()==float(row['seconds'])
    assert row['quality']==quality[trial]['status']
    assert (row['usable_for_causal_treatment_comparison']=='True')==quality[trial]['causal_treatment_comparison_accepted']
for t in ('AI_DEC1','EXB1','SCORQ1','ECNG1','SCORG1','VAN_OFFC1','VAN_ONC1'):
    assert quality[t]['causal_treatment_comparison_accepted'] is False
summary=read(out/'SUMMARY.json');assert not summary['gameplay_preserving_optimization_validated']
for label,item in summary['current_runs'].items():
    assert sha(item['result'])==item['sha256']
    d=read(item['result']);assert d['complete_14_28_56'] and d['seed_integrity_verified'] and d['native_autosave_treatment_verified']
    proof=read(item['native_post_proof']);assert proof['treatment_verified'] and not proof['unexpected_flags']
    assert sha(proof['save'])==proof['sha256']
    source=read(item['source_proof']);assert sha(source['save'])==source['sha256']
profile=read(LAB/'PROFC1_SCRIPT_PROFILE_RESULTS.json')
assert profile['not_a_throughput_benchmark'] and profile['parsed_entries']==5003 and profile['callbacks_observed']==8
assert sha(profile['native_export'])==profile['native_export_sha256']
audit=read(out/'PRESERVATION_FINAL_20261119.json');assert all(not x['changes'] for x in audit['groups'].values())
baseline=read(LAB/'ECONOMIC_PRESERVATION_BEFORE_20261118.json')
for p,h in baseline['groups']['git_index'].items():assert sha(p)==h
assert read(LAB/'CURRENT_NATIVE_DLC_INVENTORY_20261119.json')['all_identical']
pub=read(out/'GITHUB_PUBLICATION_20261119.json')
assert pub['comment_verified_equal_to_draft'] and pub['original_issue_body_preserved'] and not pub['final_measurements_update_pending']
broken=[];links=0
for p in out.glob('*.md'):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
        if '://' in target or target.startswith('#'):continue
        links+=1
        if not (p.parent/target.split('#',1)[0]).exists():broken.append(dict(file=p.name,target=target))
assert not broken,broken
result=dict(utc=datetime.now(timezone.utc).isoformat(),checked_csv_rows=len(rows),
    checked_current_benchmarks=len(summary['current_runs']),native_profile_verified=True,
    checked_local_links=links,broken_links=broken,all_protected_audit_groups_unchanged=True,
    git_index_still_unchanged=True,publication_readback_receipt_verified=True,
    scope='Deliverable consistency and evidence integrity; not an additional gameplay or performance run.')
with (out/'FINAL_VALIDATION_20261119.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
