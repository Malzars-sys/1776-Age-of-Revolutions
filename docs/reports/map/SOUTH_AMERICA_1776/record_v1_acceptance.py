"""Record the explicit R9 V1 human acceptance; documentation only."""
import datetime,hashlib,json
from pathlib import Path

BASE=Path(__file__).resolve().parent
OUT=BASE/'USER_VALIDATION_V1_2026-10-29'
QUOTE="Ok. J'ai fait tous les contrôles et ça passe. Je pense bien sûr que ce n'est qu'une V1 et donc il y a encore beaucoup de choses à faire plus tard, mais pour la V1 de la carte, je pense que l'Amérique du Sud est terminée."
def digest(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def main():
 OUT.mkdir(exist_ok=True)
 receipt=OUT/'USER_RECEIPT.json'
 assert not receipt.exists(),'Acceptance already recorded; preserve the original receipt.'
 paths=[BASE/'CURRENT.json']+[BASE/f'R9-{i:02d}/STATUS.json' for i in range(1,8)]+[BASE/'FINAL_VALIDATION_2026-10-28/STATUS.json']
 originals={p:p.read_bytes() for p in paths};updates={};records={}
 for p,raw in originals.items():
  old=json.loads(raw.decode('utf-8-sig'));n=json.loads(raw.decode('utf-8-sig'));rel=p.relative_to(BASE).as_posix()
  snapshot=OUT/'before'/rel;snapshot.parent.mkdir(parents=True,exist_ok=True);assert not snapshot.exists();snapshot.write_bytes(raw)
  n.update(status='PASS_RUNTIME_USER_VALIDATED',human_validated=True,validated_on='2026-10-29',validation_scope='SOUTH_AMERICA_MAP_V1',historical_reservations_resolved=False,south_america_complete=True,south_america_completion_scope='V1 accepted by the player; not exhaustive historical closure')
  n['user_validation_receipt']=('USER_VALIDATION_V1_2026-10-29/USER_RECEIPT.json' if p.parent==BASE else '../USER_VALIDATION_V1_2026-10-29/USER_RECEIPT.json')
  if 'engine_tested' in n:n['engine_tested']=True
  if 'runtime_validation_deferred_by_user' in n:n['runtime_validation_deferred_by_user']=False
  if p.name=='CURRENT.json':
   n.update(date='2026-10-29',active_dossier='USER_VALIDATION_V1_2026-10-29',report='USER_VALIDATION_V1_2026-10-29/REPORT.md',next_action='USER_VALIDATION_V1_2026-10-29/FUTURE_PASSES.md')
   n['final_validation'].update(stage='PASS_RUNTIME_USER_VALIDATED_V1',human_validated=True,R9_02_human_validated=True,acceptance_receipt='USER_VALIDATION_V1_2026-10-29/USER_RECEIPT.json',next_action='USER_VALIDATION_V1_2026-10-29/FUTURE_PASSES.md')
   n['final_validation']['simulation_and_reload_observed']=False
   n['final_validation']['observation_scope']='The assistant observation flags describe the earlier interrupted test. The player now reports all controls passed, without separate durations or measurements.'
  elif p.parent.name=='FINAL_VALIDATION_2026-10-28':
   n.update(validation_stage='PASS_RUNTIME_USER_VALIDATED_V1',R9_02_human_validated=True,next_action='../USER_VALIDATION_V1_2026-10-29/FUTURE_PASSES.md',original_delivery_statuses_preserved=False,original_delivery_status_snapshots_preserved=True)
   n['assistant_observation_flags_retained']=True
   n['user_report']='All controls passed; individual test dates, durations, measurements and exact runtime hashes not supplied.'
  else:
   n['prior_readiness_annotations_retained']=True
   n['prior_readiness_annotations_note']='Detailed false/pending flags and delivery dates retained from the prior technical report are historical observations, superseded only at V1 acceptance level by USER_RECEIPT.json; no new measurements are inferred.'
  updates[p]=encoded(n);records[rel]={'before':digest(raw),'after':digest(updates[p])}
 assert all(p.read_bytes()==raw for p,raw in originals.items()),'Tracking changed concurrently; re-examine before recording.'
 evidence={'date':'2026-10-29','source':'Direct human message in this conversation following the R9 manual controls and screenshots','quote':QUOTE,'status':'PASS_RUNTIME_USER_VALIDATED','scope':'South American map V1, R9-01 through R9-07 including shared-Uruguay Sacramento amendment and final validation','R9_02_included':True,'reported_result':'All controls passed; South America accepted as complete for V1','tested_version':'Version running in the player session discussed immediately before acceptance; exact byte hashes not supplied by player','reference_dossiers':['../FINAL_VALIDATION_2026-10-28','../RUNTIME_WAYFINDING_2026-10-29'],'reference_dossiers_are_not_exact_user_version_attestations':True,'test_duration':None,'simulation_end_date':None,'independent_reexecution':False,'historically_exhaustive':False,'future_work_preserved':True,'modified_tracking_files':records,'runtime_data_modified':[],'git_write_operations':[]}
 receipt.write_bytes(encoded(evidence))
 for p,data in updates.items():p.write_bytes(data)
 (OUT/'HISTORY.jsonl').write_text(json.dumps({'date':'2026-10-29','event':'Explicit player acceptance of South America map V1','receipt':'USER_RECEIPT.json','previous_tracking_snapshots':'before/','new_mission_started':False},ensure_ascii=False)+'\n',encoding='utf8')
 for p in paths:assert json.loads(p.read_text(encoding='utf-8-sig'))['status']=='PASS_RUNTIME_USER_VALIDATED'
 print(json.dumps({'recorded':True,'tracking_files_updated':len(paths),'runtime_changes':0,'V1_complete':True,'historically_exhaustive':False}))
if __name__=='__main__':main()
