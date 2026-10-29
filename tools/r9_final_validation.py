"""Read-only current-workspace R9 audit. Writes a new proof dossier only."""
import collections as C,csv,json,sys,datetime,re
from pathlib import Path
import numpy as np
from PIL import Image
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,state_nodes,ownership
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from central01 import cohorts
from r904 import assigns
import validate_map2a as qa

BASE=ROOT/'docs/reports/map/SOUTH_AMERICA_1776'
OUT=BASE/'FINAL_VALIDATION_2026-10-28'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt';BB='common/history/buildings/07_south_america.txt'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def table(n,rows):
 if not rows:return
 with (OUT/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def move_records():
 rows=[]
 def add(lot,s,r,b,t):rows.append(dict(lot=lot,state=s,rgb=r,before=b,after=t))
 p=load(BASE/'R9-01/PLAN.json')
 for r in p['ica']:add('R9-01','STATE_ICA',r,'IQU','SC3')
 for r in p['la_paz']:add('R9-01','STATE_LA_PAZ',r,'AP7','SC3')
 p=load(BASE/'R9-02/PLAN.json')
 for r in p['cells']:add('R9-02',p['state'],r,p['from_tag'],p['to_tag'])
 import r904
 for s,(t,rr) in r904.MOVES.items():
  for r in rr:add('R9-04',s,r,'SC3',t)
 for z in load(BASE/'R9-05/TRANSFERS.json'):add('R9-05',z['state'],z['rgb'],z['before'],z['after'])
 import r906
 for s,r,b,t in r906.TRANSFERS:add('R9-06',s,r,b,t)
 for z in load(BASE/'R9-07/FINAL_PLAN.json')['final_transfers']:add('R9-07',z['state'],z['rgb'],z['from'],z['to'])
 return rows
def audit():
 OUT.mkdir(exist_ok=True);now=runtime();dump('AUDIT_RUNTIME_MANIFEST.json',now)
 inv=qa.inventory();dump('GLOBAL_CURRENT_INVENTORY.json',inv)
 canonical=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/inputs/regional_originals/R9_SOUTH_AMERICA_RECOMMENDATIONS.csv').open(encoding='utf-8-sig')));scope={r['State_ID'] for r in canonical};regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))};own=ownership();checks={};issues=[]
 checks['canonical_R9_scope_present']=all(s in regs for s in scope)
 rgbscope={r for s in scope for r in provs(regs[s],'provinces')};counts=C.Counter()
 for z in inv['owners']:
  rgb,s,t=z['key']
  if s in scope:counts[rgb]+=z['count']
 missing=[r for r in rgbscope if not counts[r]];duplicate={r:n for r,n in counts.items() if n!=1}
 dump('R9_OWNER_GAPS_AND_DUPLICATES.json',{'missing':missing,'non_unique_counts':duplicate})
 checks['R9_all_defined_land_provinces_owned_once']=not missing and not duplicate
 checks['R9_owner_regions_match_geometry']=not any(z[0]=='wrong_state_region' and z[2] in scope for z in inv['errors'])
 rows=move_records();assert len(rows)==212
 for z in rows:z['current_owners']=sorted(own.get(z['rgb'],set()));z['matches']=own.get(z['rgb'])=={(z['state'],z['after'])}
 dump('TRANSFER_VERIFICATION.json',rows);checks['all_212_delivered_transfers_present']=all(z['matches'] for z in rows)
 original=assigns(text(BASE/'R9-01/before'/ST));expected=original.copy()
 for z in rows:
  k=(z['rgb'],z['state'],z['before']);assert expected[k]==1,k;expected[k]-=1;expected[z['rgb'],z['state'],z['after']]+=1
 expected['x6C6251','STATE_GUAYANA','AP7']-=1;expected['x4E1443','STATE_URUGUAY','BRZ']+=1
 current=assigns(text(ROOT/ST));filt=lambda c:C.Counter({k:v for k,v in c.items() if k[1] in scope and v>0})
 delta={'unexpected':[{'key':k,'count':v} for k,v in (filt(current)-filt(expected)).items()],'missing':[{'key':k,'count':v} for k,v in (filt(expected)-filt(current)).items()]};dump('R9_GLOBAL_OWNER_DELTA.json',delta)
 checks['whole_R9_ownership_equals_documented_deliveries']=not delta['unexpected'] and not delta['missing']
 checks['Sacramento_shared_Uruguay_and_no_obsolete_region']='STATE_COLONIA_DO_SACRAMENTO' not in regs and own.get('x4E1443')=={('STATE_URUGUAY','BRZ')} and own.get('x4E1442')=={('STATE_URUGUAY','SC4')}
 checks['Guayana_dual_assignment_resolved']=own.get('x6C6251')=={('STATE_GUAYANA','NET')}
 imp={r for n in regs.values() for r in provs(n,'impassable')};shares={tuple(z) for z in inv['states']};rs_rows=[]
 countries={n.key.removeprefix('REPLACE_OR_CREATE:'):n for f in effective('common/country_definitions') for n in parse(text(f)) if n.children('country_type')};cultures={n.key:n for f in effective('common/cultures') for n in parse(text(f))};religions={n.key for f in effective('common/religions') for n in parse(text(f))}
 pop_refs=[];building_refs=[];commands=[]
 for folder in ['pops','population','buildings']:
  for f in effective('common/history/'+folder):
   raw=text(f)
   for s in walk(parse(raw)):
    sid=s.key[2:]
    if not s.key.startswith('s:STATE_') or sid not in scope:continue
    for rs in s.children():
     if not rs.key.startswith('region_state:'):continue
     tag=rs.key.split(':')[1]
     if not rs.children():continue
     rec=dict(folder=folder,state=sid,owner=tag,has_state=(sid,tag) in shares,has_passable_land=any((sid,tag) in v and r not in imp for r,v in own.items()),file=str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else 'VANILLA:'+str(f.relative_to(GAME)),line=raw.count('\n',0,rs.start)+1)
     rs_rows.append(rec)
     for pop in rs.children('create_pop'):
      cu=scalar(pop.one('culture'));rel=scalar(pop.one('religion',cultures[cu].one('religion') if cu in cultures else 'UNKNOWN'));pop_refs.append(dict(**rec,culture=cu,culture_exists=cu in cultures,religion=rel,religion_exists=rel in religions,size=int(pop.one('size'))))
     for b in rs.children('create_building'):
      kind=scalar(b.one('building'));commands.append(dict(**rec,building=kind,explicit_level=b.one('level'),economic_levels=[int(q.value) for o in b.children('add_ownership') for q in walk(o.children()) if q.key=='levels'],PM=provs(b,'activate_production_methods')))
 checks['R9_all_pop_and_building_selectors_have_owner_state']=all(r['has_state'] for r in rs_rows)
 checks['R9_all_pop_and_building_selectors_have_passable_land']=all(r['has_passable_land'] for r in rs_rows)
 checks['R9_population_culture_and_religion_references_resolve']=all(r['culture_exists'] and r['religion_exists'] and r['size']>0 for r in pop_refs)
 dump('R9_SCOPES.json',rs_rows);dump('R9_POPULATION_COHORTS.json',pop_refs);dump('R9_BUILDING_COMMANDS.json',commands)
 active={t for s,t in shares if s in scope};caps=[]
 for t in sorted(active):
  n=countries.get(t);cap=scalar(n.one('capital','UNKNOWN')) if n else 'UNKNOWN';caps.append(dict(tag=t,definition_exists=n is not None,capital=cap,capital_owned=(cap,t) in shares))
 dump('R9_ACTIVE_COUNTRIES_AND_CAPITALS.json',caps);checks['R9_active_countries_and_capitals_resolve']=all(z['definition_exists'] and z['capital_owned'] for z in caps)
 # Distinguish subsequent collaborator population edits, rather than restore them.
 finalpop=state_nodes(text(BASE/'R9-07/PAMPAS_CUYO/patch'/PP));livepop=state_nodes(text(ROOT/PP));changed=[s for s in finalpop.keys()|livepop.keys() if s not in finalpop or s not in livepop or normalized([finalpop[s]])!=normalized([livepop[s]])];dump('SUBSEQUENT_POPULATION_EDITS.json',{'changed_regions':sorted(changed),'before_sha256':sha(BASE/'R9-07/PAMPAS_CUYO/patch'/PP),'current_sha256':sha(ROOT/PP),'classification':'Subsequent edits; preserved, not attributed or historically certified by this territorial audit'})
 originalpop=cohorts(text(BASE/'R9-01/before'/PP));delivered=cohorts(text(BASE/'R9-07/PAMPAS_CUYO/patch'/PP));actualpop=cohorts(text(ROOT/PP));allstates={s for s,k in originalpop}|{s for s,k in actualpop};popdelta=[]
 for s in sorted(allstates):
  b=sum(v for (sid,k),v in originalpop.items() if sid==s);d=sum(v for (sid,k),v in delivered.items() if sid==s);a=sum(v for (sid,k),v in actualpop.items() if sid==s);popdelta.append(dict(state=s,before_R9=b,delivered_R9=d,current=a,R9_delta=d-b,subsequent_delta=a-d))
 table('POPULATION_RECONCILIATION.csv',popdelta);checks['delivered_R9_population_delta_is_115']=sum(delivered.values())-sum(originalpop.values())==115
 checks['all_other_delivered_cohorts_conserved']=not (originalpop-delivered) and sum((delivered-originalpop).values())==115
 checks['current_population_total_preserved_outside_disclosed_followups']=all(a==b for k,a in delivered.items() for b in [actualpop.get(k,0)] if k[0] not in changed) and all(k in delivered or k[0] in changed for k in actualpop)
 new_orphans=[r for r in rs_rows if not r['has_state'] or not r['has_passable_land']];dump('CURRENT_R9_ORPHAN_SCOPES.json',new_orphans)
 # Final per-file manifests: later R9 changes supersede only the same path.
 ms=[BASE/'R9-01/PATCH.json',BASE/'R9-02/PATCH.json',BASE/'R9-03/SHARED_URUGUAY_FEEDBACK/PATCH.json',BASE/'R9-04/PATCH.json',BASE/'R9-05/PATCH.json',BASE/'R9-06/PATCH.json']
 latest={}
 for m in ms:latest.update(load(m)['output_sha256'])
 latest.update(load(BASE/'R9-07/FINAL_PATCH_MANIFEST.json'))
 drift=[dict(path=r,delivered=h,current=now.get(r)) for r,h in latest.items() if now.get(r)!=h];dump('DELIVERY_FILE_DRIFT.json',drift)
 checks['R9_delivery_files_exact_except_disclosed_population_followups']=all(z['path']==PP for z in drift)
 # Explicit fiscal/ownership commands in the inherited building file, after
 # the documented IQU consolidation and Rio Grande port reassignment.
 expectedbuild=state_nodes(text(BASE/'R9-02/patch'/BB));livebuild=state_nodes(text(ROOT/BB));bd=[s for s in expectedbuild.keys()|livebuild.keys() if s not in expectedbuild or s not in livebuild or normalized([expectedbuild[s]])!=normalized([livebuild[s]])];dump('EXISTING_BUILDING_FILE_DELTA.json',{'changed_regions_since_R9_02':bd});checks['all_existing_South_American_buildings_preserved_after_R9_02']=not bd
 newports=['common/history/buildings/1776_sacramento.txt','common/history/buildings/1776_r904_chiloe_port.txt','common/history/buildings/1776_r907_malvinas_port.txt'];checks['all_three_added_port_files_match_delivery']=all(r in latest and now.get(r)==latest[r] for r in newports)
 # Unique IDs / raster validity, scoped region ownership and one approved cut.
 ids=C.defaultdict(list)
 for s,n in regs.items():ids[scalar(n.one('id','UNKNOWN'))].append(s)
 checks['R9_state_numeric_ids_unique']=all(len(ids[scalar(regs[s].one('id'))])==1 for s in scope)
 image=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);packed=(image[:,:,0]<<16)|(image[:,:,1]<<8)|image[:,:,2];colors,sizes=np.unique(packed,return_counts=True);pixels={f'x{int(c):06X}':int(v) for c,v in zip(colors,sizes)};checks['all_R9_province_RGBs_present_in_bitmap']=all(pixels.get(r,0)>0 for r in rgbscope);checks['Sacramento_51_visible_pixels_retained']=pixels.get('x4E1443')==51
 dump('GLOBAL_OWNERSHIP_ISSUES.json',{'duplicates':inv['duplicates'],'structural_errors':inv['errors'],'R9_errors':[z for z in inv['errors'] if any(v in scope for v in z if isinstance(v,str))]})
 checks['no_R9_orphan_or_wrong_region_structural_errors']=not [z for z in inv['errors'] if any(v in scope for v in z if isinstance(v,str))]
 external=load(OUT/'BASELINE_RUNTIME.json');during={r:{'before':external.get(r),'now':now.get(r)} for r in external.keys()|now.keys() if external.get(r)!=now.get(r)};dump('CONCURRENT_RUNTIME_DURING_AUDIT.json',during)
 checks['no_runtime_files_changed_by_audit']=not during
 passed=sum(bool(v) for v in checks.values());dump('STATIC_VALIDATION.json',{'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'passed':passed,'total':len(checks),'failed':[k for k,v in checks.items() if not v],'scope_regions':len(scope),'scope_unique_provinces':len(rgbscope),'transfers_verified':len(rows),'current_SA_population':sum(actualpop.values()),'delivered_SA_population':sum(delivered.values()),'baseline_SA_population':sum(originalpop.values()),'engine_validated':False,'human_validated':False});print(json.dumps({'passed':passed,'total':len(checks),'failed':[k for k,v in checks.items() if not v],'population_followups':changed,'delivery_drift':[z['path'] for z in drift]}))
if __name__=='__main__':audit()
