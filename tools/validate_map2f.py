"""Independent conservation checks. Static results are NOT observations in game."""
import collections as C,contextlib,io,json,subprocess
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective
from map2f_work import ROOT,GAME,OUT,BASE,TARGETS,GIT,sha,source_bitmap,dump
import map2f_patch as patcher

def population_profiles(originals):
 glob=C.Counter();regional=C.Counter();detail=C.Counter()
 for path,raw in originals.items():
  if not path.startswith(('common/history/pops/','common/history/population/')):continue
  for s in cw.walk(cw.parse(raw)):
   if not s.key.startswith('s:STATE_'):continue
   for r in s.children():
    if not r.key.startswith('region_state:'):continue
    for p in r.children('create_pop'):
     attrs=[qa.norm(n) for n in p.children() if n.key!='size'];sig=json.dumps(attrs,ensure_ascii=False,sort_keys=True)
     n=int(p.one('size'));glob[sig]+=n;regional[(s.key,sig)]+=n;detail[(s.key[2:],r.key.split(':')[1],sig)]+=n
 return glob,regional,detail

def building_profiles(inv):
 result=C.Counter()
 for row in inv['buildings']:
  sid,tag,body=row['key'];n=json.loads(body);rest=[v for v in n[2] if v[0]!='add_ownership']
  for own in [v for v in n[2] if v[0]=='add_ownership']:
   for h in own[2]:
    fields=[v for v in h[2] if v[0]!='levels'];country=next((v[2] for v in fields if v[0]=='country'),'c:'+tag)
    for field in fields:
     if field[0]=='region' and (country,field[2])==('c:OMA','STATE_BALUCHISTAN'):field[2]='STATE_OMAN'
     if field[0]=='region' and (country,field[2])==('c:BIC','STATE_BUNDELKHAND'):field[2]='STATE_BIHAR'
    # Two exact planned BIC port redistributions are independently checked
    # against intended AST below; their economic/PM profile is conserved R4-wide.
    port=any(v[0]=='building' and v[2]=='building_port' for v in rest) and country=='c:BIC' and sid in TARGETS
    sig=json.dumps(['R4_BIC_PORT_POOL' if port else sid,rest,h[0],fields],ensure_ascii=False,sort_keys=True)
    result[sig]+=int(next(v[2] for v in h[2] if v[0]=='levels'))*row['count']
 return result

def unit_profiles(inv):
 result=C.Counter()
 for r in inv['units']:
  tag,name,_,body=r['key'];n=json.loads(body)
  fields=[v for v in n[2] if v[0] not in ['count','state_region']]
  count=int(next(v[2] for v in n[2] if v[0]=='count'))
  result[(tag,name,json.dumps(fields,sort_keys=True))]+=count*r['count']
 return result

def validate():
 base=json.loads(BASE.read_text(encoding='utf-8'));before=base['inventory'];after=qa.inventory();changed,plan=patcher.transform(base)
 tests=[]
 def check(name,condition,detail=None):
  tests.append({'name':name,'status':'PASS' if condition else 'FAIL','detail':detail});return condition
 expected=qa.counter(before['owners'])
 for r in plan['territorial']:
  a=(r['rgb'],r['state'],r['before']);b=(r['rgb'],r['state'],r['after']);assert expected[a]==1;expected[a]-=1;expected[b]+=1
 for v in plan['duplicates_removed']:expected[(v,'STATE_ORISSA','NAG')]-=1
 check('exact_authorised_owner_manifest',+expected==qa.counter(after['owners']))
 check('all_existing_rgb_ids_retained',{r['key'][0] for r in before['owners']}=={r['key'][0] for r in after['owners']})
 check('no_new_rgb_or_state_geometry',before['geometry']==after['geometry'])
 check('bitmap_identical',sha(source_bitmap())==base['bitmap_sha256'])
 check('transfers_inside_R4',all(r['state'] in TARGETS for r in plan['territorial']))
 check('no_new_double_attribution',all(before['duplicates'].get(k,0)>=v for k,v in after['duplicates'].items()))
 check('three_Odisha_duplicates_removed',len(before['duplicates'])==53 and len(after['duplicates'])==50 and not set(plan['duplicates_removed'])&set(after['duplicates']))
 check('no_new_orphan_or_wrong_region',not set(map(str,after['errors']))-set(map(str,before['errors'])),after['errors'])
 check('world_population_835804980',sum(r['count'] for r in after['pops'])==835804980)
 check('global_culture_religion',before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
 originals=dict(base['originals']);originals.update({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in changed if p.startswith(('common/history/pops/','common/history/population/'))})
 bp,br,bd=population_profiles(base['originals']);ap,ar,ad=population_profiles(originals)
 check('all_population_fields_status_literacy_qualifications',bp==ap)
 check('regional_demographics_all_attributes',br==ar)
 check('no_empty_population_groups',all(v>0 for v in ap.values()))
 check('national_building_level_totals',before['building_levels_written']==after['building_levels_written'])
 check('regional_buildings_methods_reserves_economic_owners',building_profiles(before)==building_profiles(after))
 check('two_conserved_BIC_port_levels_to_Bombay_Madras',len(plan['port_redistributions'])==2 and sum(r['levels'] for r in plan['port_redistributions'])==2)
 check('national_units_types_services_formations',unit_profiles(before)==unit_profiles(after))
 desired=qa.counter(before['units'])
 for r in before['units']:
  tag,name,sid,body=r['key']
  if tag=='OMA' and sid=='STATE_BALUCHISTAN':
   desired[(tag,name,sid,body)]-=r['count'];new=body.replace('s:STATE_BALUCHISTAN','s:STATE_OMAN');desired[(tag,name,'STATE_OMAN',new)]+=r['count']
 check('only_ten_necessary_Omani_recruitments_relocated',+desired==qa.counter(after['units']) and sum(r[2] for r in plan['military_recruitment'])==10)
 actual_changed=[p for p,digest in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=digest]
 check('no_unplanned_existing_file_changes',set(actual_changed)=={p for p in changed if p in base['hashes']},actual_changed)
 check('all_MAP2A_B_C_D_E_reports_unchanged',not any(p.startswith('docs/reports/map/MAP') for p in actual_changed))
 check('exact_intended_history_AST',all([qa.norm(n) for n in cw.parse(txt)]==[qa.norm(n) for n in cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))] for p,txt in changed.items() if p.endswith('.txt')))
 pairs={tuple(r) for r in after['states']};capitals={}
 for tag in [*plan['reused_tags'],*plan['new_tags'],'JEY','COO','BIC','OMA','GWA']:
  n=json.loads(after['countries'][tag]);cap=next(v[2] for v in n[2] if v[0]=='capital');capitals[tag]=cap
 check('changed_or_revived_country_capitals_owned',all((cap,t) in pairs for t,cap in capitals.items()),capitals)
 check('all_owner_tags_defined',all(r['key'][2] in after['countries'] for r in after['owners']))
 oldchar=[(p,d) for p,d in base['hashes'].items() if p.startswith('common/history/characters/')]
 check('all_existing_rulers_and_commanders_preserved',all(sha(ROOT/p)==d for p,d in oldchar))
 perpath='common/history/military_formations/04_military_formations_middle_east.txt'
 per=lambda raw:[qa.norm(n) for n in cw.walk(cw.parse(raw)) if n.key=='c:PER']
 tab=lambda raw:[qa.norm(n) for n in cw.walk(cw.parse(raw)) if n.key=='s:STATE_TABRIZ']
 check('Tabriz_food_fix_and_Persian_garrisons_preserved',per(base['originals'][perpath])==per((ROOT/perpath).read_text(encoding='utf-8-sig')) and all(tab(base['originals'][p])==tab((ROOT/p).read_text(encoding='utf-8-sig')) for p in ['common/history/buildings/08_middle_east.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']))
 check('Ottoman_Russian_PLC_CRI_and_transit_preserved',all(sha(ROOT/p)==d for p,d in base['hashes'].items() if ('ottoman' in p or 'map2d' in p or 'transit' in p) and p not in changed))
 check('technologies_PM_AI_goods_and_assets_preserved',not any(p.startswith(('gfx/','common/production_methods/','common/technology/','common/goods/','common/ai_')) for p in actual_changed))
 check('primary_git_HEAD_refs_index_unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==base['git']['refs'] and sha(ROOT/'.git/index')==base['git']['index'])
 import validate_regional_infrastructure_shortage as infra
 for name,func in [('Ottoman_logical_models',cw.model_tests),('Infrastructure_IA_models',infra.model_tests)]:
  try:
   with contextlib.redirect_stdout(io.StringIO()):func()
   check(name,True)
  except Exception as exc:check(name,False,str(exc))
 # Native token checks for newly introduced countries, technologies and flags.
 tech={n.key for p in effective(ROOT,GAME,'common/technology/technologies') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
 newtech=[cw.scalar(n.value) for n in cw.walk(cw.parse(changed['common/history/countries/1776_map2f_carnatic_kandy.txt'])) if n.key=='add_technology_researched']
 check('new_country_researched_technologies_defined',set(newtech)<=tech)
 check('new_flag_native_emblem_exists',(GAME/'gfx/coat_of_arms/colored_emblems/ce_lion_rampant.dds').exists())
 stats=C.Counter()
 for r in plan['territorial']:stats[r['state']]+=1
 regions={r['state'] for r in plan['territorial']};op=qa.counter(before['regional_pop']);np=qa.counter(after['regional_pop']);rows=[]
 for key in sorted(set(op)|set(np)):
  if key[0] in regions:rows.append([*key,op[key],np[key],np[key]-op[key]])
 status='PASS_STATIC' if all(r['status']=='PASS' for r in tests) else 'FAIL_STATIC'
 dump('MAP2F_VALIDATION.json',{'status':status,'tests':tests,'transferred_provinces':len(plan['territorial']),'province_bitmap_changes':0,'by_region':dict(stats),'duplicates_before':53,'duplicates_after':len(after['duplicates']),'inherited_reference_errors':after['errors'],'population':835804980,'new_tags':plan['new_tags'],'reused_tags':plan['reused_tags'],'native_test':'NOT_RUN_USER_WILL_TEST; launch attempt timed out and no game window returned; all native interaction stopped at user request','primary_git_unchanged':True,'backup_checkpoint':'49377485f78136bd4e2fc29ded8f6ae26c63ee7c','modified_files':plan['files'],'all_population_attributes_verified':True,'allocation_basis':'integer native land area except bounded approximately 200000-person Bombay/Salsette pool; neither is a historical census','military':'10 Omani regular units relocated to owned Oman; no types/formations/commanders/counts changed','port_redistributions':plan['port_redistributions']})
 dump('TABLE_DATA.json',{'territorial':plan['territorial'],'population':rows})
 print(status,len(tests),'checks;',len(plan['territorial']),'transfers; population835804980; duplicates',len(after['duplicates']))
 for r in tests:
  if r['status']=='FAIL':print('FAILED',r['name'],r['detail'])
 assert status=='PASS_STATIC'
if __name__=='__main__':validate()
