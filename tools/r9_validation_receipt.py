"""Archive read-only evidence and compare two actual engine saves for R9."""
import json,collections as C,datetime,shutil,os
from pathlib import Path
from r9_saved_validation import objects,field
from r9_final_validation import OUT,BASE,load,dump
from audit_hbc_1776 import ROOT,sha,runtime
from audit_1776_runtime_logs import messages,signature

def save_inventory(path):
 countries={};states={};builds=[]
 for sec,i,r,n in objects(path):
  if sec=='country_manager':countries[str(i)]=field(r,'definition')
  elif sec=='states':states[str(i)]=(field(r,'region'),field(r,'country'))
  elif sec=='building_manager':builds.append((field(r,'state'),field(r,'building'),int(field(r,'levels') or 0)))
 return countries,states,builds

def main():
 co,st,bs=save_inventory(OUT/'INITIAL_OLD_MELTED.txt');old=C.Counter()
 for s,b,n in bs:
  if s in st:old[st[s][0],co.get(st[s][1]),b]+=n
 rows=load(OUT/'FRESH_SAVE_BUILDING_MAX_DIAGNOSTIC.json')
 for z in rows:z['older_loaded_session_levels']=old[z['region'],z['owner'],z['building']];z['same_in_older_session']=z['older_loaded_session_levels']==z['loaded']
 dump('PREEXISTING_ENGINE_BUILDING_DIFFERENCES.json',rows)
 logs=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/logs');dest=OUT/'runtime_followup_2026-10-29';dest.mkdir(exist_ok=True)
 prior=set()
 for p in (OUT/'runtime_before/logs').glob('*.log'):
  for no,comp,msg in messages(p.read_text(encoding='utf-8-sig',errors='replace')):prior.add(signature(comp,msg))
 scope={z['region'] for z in load(OUT/'FRESH_SAVE_STATES.json')};inventory=[];related=[]
 for p in sorted(logs.glob('*.log')):
  target=dest/p.name
  if not target.exists():shutil.copy2(p,target)
  inventory.append(dict(file=p.name,bytes=target.stat().st_size,mtime=datetime.datetime.fromtimestamp(target.stat().st_mtime,datetime.timezone.utc).isoformat(),sha256=sha(target)))
  for no,comp,msg in messages(target.read_text(encoding='utf-8-sig',errors='replace')):
   # This is a bounded evidence search, not proof that all engine errors are absent.
   if any(s in msg for s in scope) or any(k in msg for k in ['1776_sacramento','1776_r904','1776_r907','4E1443','STATE_COLONIA_DO_SACRAMENTO']):
    related.append(dict(file=p.name,line=no,component=comp,message=msg,seen_before_audit=signature(comp,msg) in prior))
 dump('FOLLOWUP_LOG_INVENTORY.json',inventory);dump('FOLLOWUP_R9_LOG_MESSAGES.json',related)
 now=runtime();before=load(OUT/'AUDIT_RUNTIME_MANIFEST.json');drift={r:dict(audited=before.get(r),now=now.get(r)) for r in before.keys()|now.keys() if before.get(r)!=now.get(r)}
 dump('WORKSPACE_DRIFT_AT_HANDOVER.json',drift)
 delivered=set()
 for rel in ['R9-01/PATCH.json','R9-02/PATCH.json','R9-03/SHARED_URUGUAY_FEEDBACK/PATCH.json','R9-04/PATCH.json','R9-05/PATCH.json','R9-06/PATCH.json']:delivered.update(load(BASE/rel)['output_sha256'])
 delivered.update(load(BASE/'R9-07/FINAL_PATCH_MANIFEST.json'))
 scoped={r:v for r,v in drift.items() if r in delivered};dump('R9_DELIVERED_FILE_DRIFT_AT_HANDOVER.json',scoped)
 from r904 import assigns
 from hbc06_integrate import text
 expected=C.Counter({tuple(z['key']):z['count'] for z in load(OUT/'GLOBAL_CURRENT_INVENTORY.json')['owners'] if z['key'][1] in scope})
 current=C.Counter({k:v for k,v in assigns(text(ROOT/'common/history/states/00_states.txt')).items() if k[1] in scope})
 dump('R9_OWNERSHIP_AT_HANDOVER.json',{'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'same_R9_ownership_as_audit':expected==current,'missing':list((expected-current).items()),'unexpected':list((current-expected).items()),'note':'The shared states file changed concurrently; this bounded comparison checks all R9 assignments, without restoring the global file.'})
 saves=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/save games');fresh=list(saves.glob('*R9_fresh_initial_20261028.v3'));receipt={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fresh_save':[],'old_session_archive':{'file':'INITIAL_LOADED_SESSION.v3','sha256':sha(OUT/'INITIAL_LOADED_SESSION.v3')},'actual_UI_observations':['Fresh main menu Victoria 3 Macha 1.13.11 checksum 0352 modified','New sandbox scenario country SPA, 1776.1.1, paused','Manual local save created with unique suffix _R9_fresh_initial_20261028','Input and image capture initially worked; FrameArrived timed out twice after attempted zoom; inputs ceased'],'not_observed':['R9 visual tour','simulation beyond initial date','manual save reload','sustained market access and population food security'],'baseline_process_flag_caveat':'RUNTIME_BASELINE running_game_before=false came from an unreliable shell process check; CUA subsequently observed a running older game. This flag does not establish the initial absence of a game.','R9_02_status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','human_validated':False,'R9_files_changed_since_audit':scoped,'runtime_files_changed_since_audit_count':len(drift),'log_time_caveat':'Followup logs were copied on 2026-10-29 and include later launches/rotations; do not attribute all messages to the single fresh R9 save test.'}
 for p in fresh:
  out=OUT/'FRESH_INITIAL_SESSION.v3'
  if not out.exists():shutil.copy2(p,out)
  receipt['fresh_save'].append({'original_path':str(p),'archive':out.name,'sha256':sha(p),'bytes':p.stat().st_size,'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()})
 dump('RUNTIME_RECEIPT.json',receipt)
 print(json.dumps({'older_building_findings':rows,'R9_log_mentions':len(related),'runtime_files_changed_since_audit':len(drift),'R9_delivered_files_changed_since_audit':list(scoped),'save_archived':bool(fresh)},ensure_ascii=False))
if __name__=='__main__':main()
