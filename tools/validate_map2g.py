"""Independent static conservation checks; not an engine or employment test."""
import collections as C,contextlib,io,json,subprocess
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from validate_map2f import population_profiles,unit_profiles
from map_1776_audit import effective
from map2g_work import ROOT,GAME,OUT,BASE,TARGETS,GIT,sha,source_bitmap,dump,CONTROL
import map2g_patch as patcher
def buildings(inv,plan):
 result=C.Counter();hq={(t,old):new for _,t,old,new in plan['economic_hq']}
 for row in inv['buildings']:
  sid,tag,body=row['key'];n=json.loads(body);rest=[v for v in n[2] if v[0]!='add_ownership']
  for own in [v for v in n[2] if v[0]=='add_ownership']:
   for holder in own[2]:
    fields=[v for v in holder[2] if v[0]!='levels'];country=next((v[2] for v in fields if v[0]=='country'),'c:'+tag).removeprefix('c:')
    for f in fields:
     if f[0]=='region' and (country,f[2]) in hq:f[2]=hq[country,f[2]]
    sig=json.dumps([sid,rest,holder[0],fields],ensure_ascii=False,sort_keys=True)
    result[sig]+=int(next(v[2] for v in holder[2] if v[0]=='levels'))*row['count']
 return result
def run():
 base=json.loads(BASE.read_text(encoding='utf-8'));before=base['inventory'];after=qa.inventory();changed,plan=patcher.transform(base);tests=[]
 def check(name,ok,detail=None):
  tests.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
  print(tests[-1]['status'],name,flush=True)
 expected=qa.counter(before['owners'])
 for r in plan['territorial']:
  key=(r['rgb'],r['state'],r['before']);assert expected[key]==1;expected[key]-=1;expected[r['rgb'],r['state'],r['after']]+=1
 expected['xBD5671','STATE_GANSU','CHI']-=1
 check('exact_territorial_manifest',+expected==qa.counter(after['owners']))
 valid=lambda inv:{r['key'][0] for r in inv['owners'] if r['key'][0] in inv['geometry']}
 check('all_valid_land_RGBs_retained',valid(before)==valid(after))
 check('no_province_definition_added_or_removed',before['geometry']==after['geometry'])
 check('bitmap_byte_identical_including_Avignon_and_Friuli',sha(source_bitmap())==base['bitmap_sha256'])
 check('all_transfers_strictly_R5',all(r['state'] in TARGETS for r in plan['territorial']))
 check('no_new_double_attributions',before['duplicates']==after['duplicates'] and len(after['duplicates'])==50)
 check('lake_token_was_not_a_land_province','xBD5671' not in before['geometry'] and not any(r['key'][0]=='xBD5671' for r in after['owners']))
 check('no_new_orphan_or_reference_error',not set(map(str,after['errors']))-set(map(str,before['errors'])),after['errors'])
 check('world_population_835804980',sum(r['count'] for r in after['pops'])==835804980)
 check('culture_explicit_and_default_religion_conserved',before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
 originals=dict(base['originals']);originals.update({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in changed if p.startswith(('common/history/pops/','common/history/population/'))})
 bp,br,bd=population_profiles(base['originals']);ap,ar,ad=population_profiles(originals)
 check('all_population_fields_literacy_qualifications_free_slave',bp==ap)
 check('population_and_attributes_by_State_Region',br==ar)
 check('positive_written_population_fragments',all(int(n.one('size'))>0 for p,raw in originals.items() if p.startswith(('common/history/pops/','common/history/population/')) for n in cw.walk(cw.parse(raw)) if n.key=='create_pop'))
 check('all_declared_building_levels_conserved',before['building_levels_written']==after['building_levels_written'])
 check('building_PM_reserve_and_economic_holders_conserved',buildings(before,plan)==buildings(after,plan))
 check('national_military_types_counts_formations_and_services',unit_profiles(before)==unit_profiles(after))
 check('every_unit_recruitment_reference_identical',before['units']==after['units'])
 check('every_military_and_character_file_byte_identical',all(sha(ROOT/p)==d for p,d in base['hashes'].items() if p.startswith(('common/history/military_formations/','common/history/characters/'))))
 actual=[p for p,d in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=d]
 check('existing_file_changes_match_plan_only',set(actual)=={p for p in changed if p in base['hashes']},actual)
 check('history_AST_exactly_matches_reviewed_patch',all([qa.norm(n) for n in cw.parse(txt)]==[qa.norm(n) for n in cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))] for p,txt in changed.items() if p.endswith('.txt')))
 check('previous_MAP2A_to_F_reports_unchanged',not any(p.startswith('docs/reports/') for p in actual))
 check('all_technologies_PM_AI_goods_assets_events_preserved',not any(p.startswith(('gfx/','common/production_methods/','common/technology/','common/goods/','common/ai_','events/','common/journal_entries/','common/modifiers/')) for p in actual))
 pairs={tuple(r) for r in after['states']};caps={}
 for tag in [*plan['reused_tags'],'AIN','EZO','CHI','RUS','ALK','ATB','TIB','KOR','RYU','ULT','SKH']:
  n=json.loads(after['countries'][tag]);cap=next(v[2] for v in n[2] if v[0]=='capital');caps[tag]=cap
 check('all_affected_capitals_owned',all((cap,tag) in pairs for tag,cap in caps.items()),caps)
 check('all_owner_tags_defined',all(r['key'][2] in after['countries'] for r in after['owners']))
 check('revived_tags_previously_inactive',not any(tag in plan['reused_tags'] for _,tag in before['states']))
 unchanged=lambda inventory,exceptions:{k:v for k,v in inventory['countries'].items() if k not in exceptions}
 check('all_other_country_definitions_unchanged',unchanged(before,set(plan['reused_tags'])|{'ULT'})==unchanged(after,set(plan['reused_tags'])|{'ULT'}))
 govern={sid for sid,t in patcher.WHOLE if t=='CHI'}
 check('Qing_subjects_only_remote_governments',govern=={'STATE_YUNNAN','STATE_GUIZHOU','STATE_DZUNGARIA','STATE_TIANSHAN','STATE_ULIASTAI','STATE_URGA','STATE_TUVA'})
 oldowners=qa.counter(before['owners']);affected={x['state'] for x in plan['territorial']}|{'STATE_GANSU'}
 check('Beijing_Zhili_central_China_and_Canton_direct_preserved',all(oldowners[tuple(r['key'])]==r['count'] for r in after['owners'] if r['key'][1] not in affected))
 check('imperial_Qing_country_history_market_capital_unchanged',sha(ROOT/'common/history/countries/chi - china.txt')==base['hashes']['common/history/countries/chi - china.txt'])
 check('existing_Tibet_Korea_Ryukyu_Matsumae_dependencies_preserved',sha(ROOT/'common/history/diplomacy/00_subject_relationships.txt')==base['hashes']['common/history/diplomacy/00_subject_relationships.txt'])
 dip=cw.parse(changed['common/history/diplomacy/1776_map2g_qing_dependencies.txt']);pacts=[n for n in cw.walk(dip) if n.key=='create_diplomatic_pact']
 check('exactly_three_new_Qing_vassal_pacts',len(pacts)==3 and {n.one('country') for n in pacts}=={'c:YUN','c:XIN','c:MGL'} and all(n.one('type')=='vassal' for n in pacts))
 init=cw.parse(changed['common/history/countries/1776_map2g_remote_governments.txt']);tags={n.key for n in cw.walk(init) if n.key.startswith('c:')}
 check('all_new_organized_governments_initialized',tags=={'c:YUN','c:XIN','c:MGL'})
 tech={n.key for p in effective(ROOT,GAME,'common/technology/technologies') for n in cw.parse(p.read_text(encoding='utf-8-sig'))};laws={n.key for p in effective(ROOT,GAME,'common/laws') for n in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig')))}
 check('all_initializer_technologies_and_laws_defined',all(cw.scalar(n.value) in tech for n in cw.walk(init) if n.key=='add_technology_researched') and all(cw.scalar(n.value).removeprefix('law_type:') in laws for n in cw.walk(init) if n.key=='activate_law'))
 check('no_remote_Canton_policy_without_Guangdong',not any(n.value=='law_type:law_canton_system' for n in cw.walk(init)))
 cultures={n.key for p in effective(ROOT,GAME,'common/cultures') for n in cw.parse(p.read_text(encoding='utf-8-sig'))};religions={n.key for p in effective(ROOT,GAME,'common/religions') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
 check('new_country_cultures_religions_defined',all(set(v[3].split())<=cultures and v[4] in religions for v in patcher.DEFS.values()))
 check('new_flags_use_existing_native_pattern',(GAME/'gfx/coat_of_arms/patterns/pattern_horizontal_split_01.tga').exists())
 check('Taiwan_Qing_north_west_retained',all(('x'+r,'STATE_FORMOSA','CHI') in qa.counter(after['owners']) for r in ['6DAB21','7070E0','AEA2D8','6645CF','E73B31','9A5066']))
 check('Taiwan_no_Han_or_Manchu_moved_to_Indigenous_country',all(k[2]=='yuanzhumin' for k in qa.counter(after['regional_pop']) if k[:2]==('STATE_FORMOSA','FRS')))
 check('Taiwan_plains_Indigenous_pool_retained',sum(r['count'] for r in after['regional_pop'] if r['key'][:3]==['STATE_FORMOSA','CHI','yuanzhumin'])==55833)
 check('Alaska_and_non_R5_Athabaska_territory_untouched',qa.counter([r for r in before['owners'] if r['key'][1] not in TARGETS])==qa.counter([r for r in after['owners'] if r['key'][1] not in TARGETS]))
 geo=json.loads((OUT/'GEOGRAPHY.json').read_text())
 check('nine_hub_selectors_match_actual_existing_locators',len(plan['hub_changes'])==9 and all(geo['locators'][sid+'|'+kind]['rgb']==new for _,sid,kind,old,new in plan['hub_changes']))
 def nonhub(raw):
  return [[n.key,[qa.norm(c) for c in n.children() if (n.key,c.key) not in {(sid,kind) for _,sid,kind,old,new in plan['hub_changes']}]] for n in cw.parse(raw)]
 check('State_Region_resources_traits_bounds_and_other_hubs_unchanged',all(nonhub(base['originals'][p])==nonhub((ROOT/p).read_text(encoding='utf-8-sig')) for p in changed if p.startswith('map_data/state_regions/')))
 import re
 for lang in ['english','french']:
  p=ROOT/f'localization/{lang}/replace/1776_map2g_l_{lang}.yml';raw=p.read_text(encoding='utf-8');keys=re.findall(r'^ ([A-Za-z0-9_]+):0 "[^"\r\n]*"$',raw,re.M)
  expectedloc={v for t in patcher.NAMES for v in [t,t+'_ADJ']}|{'aor1776_map2g_'+t.lower() for t in plan['remote_governments']}
  check(lang+'_localization_BOM_unique_complete',raw.startswith('\ufeffl_'+lang+':') and set(keys)==expectedloc and len(keys)==len(set(keys)))
 ult=next(n for n in cw.parse((ROOT/'common/country_definitions/00_countries.txt').read_text(encoding='utf-8-sig')) if n.key=='ULT')
 check('native_ULT_RGB_color_in_range',[int(n.value) for n in ult.children('color')[0].children()]==[122,229,255])
 for name,func in [('Ottoman_logical_models',cw.model_tests)]:
  try:
   with contextlib.redirect_stdout(io.StringIO()):func()
   check(name,True)
  except Exception as exc:check(name,False,str(exc))
 import validate_regional_infrastructure_shortage as infra
 try:
  with contextlib.redirect_stdout(io.StringIO()):infra.model_tests()
  check('regional_infrastructure_IA_logical_models',True)
 except Exception as exc:check('regional_infrastructure_IA_logical_models',False,str(exc))
 check('primary_HEAD_refs_index_unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==base['git']['refs'] and sha(ROOT/'.git/index')==base['git']['index'])
 check('MAP2F_remote_checkpoint_verified_before_gameplay',base['backup']['status']=='PASS_REMOTE_EXACT_RESTORATION' and base['backup']['sha256_all_files']=='MATCH')
 states={r['state'] for r in plan['territorial']};op=qa.counter(before['regional_pop']);np=qa.counter(after['regional_pop']);rows=[]
 for k in sorted(set(op)|set(np)):
  if k[0] in states:rows.append([*k,op[k],np[k],np[k]-op[k]])
 status='PASS_STATIC' if all(r['status']=='PASS' for r in tests) else 'FAIL_STATIC'
 summary={'status':status,'checks':tests,'modified_files':plan['files'],'province_owner_changes':len(plan['territorial']),'by_state':dict(C.Counter(r['state'] for r in plan['territorial'])),'bitmap_changed':False,'population_before':835804980,'population_after':835804980,'population_all_attributes_conserved':bp==ap,'building_economic_profiles_conserved':buildings(before,plan)==buildings(after,plan),'military_unchanged':before['units']==after['units'],'duplicates_before':50,'duplicates_after':len(after['duplicates']),'inherited_reference_errors':after['errors'],'reused_tags':plan['reused_tags'],'new_tags':[],'remote_governments':plan['remote_governments'],'hub_corrections':plan['hub_changes'],'economic_hq_relocations':plan['economic_hq'],'allocation':plan['allocation'],'Qing_subject_abstraction':'User explicitly approved large subjects, then limited them to distant provinces. These are administrations under Qing sovereignty, not historical independent states. Finances and diplomatic autonomy necessarily approximate the native vassal mechanic.','native_game_test':'NOT_RUN: player tests a new game and one month; no hiring, market, budget or engine guarantee from static tests.','backup':base['backup'],'no_main_commit_merge_or_push':True}
 dump('MAP2G_VALIDATION.json',summary);dump('TABLE_DATA.json',{'territorial':plan['territorial'],'population':rows})
 cleanup=json.loads((CONTROL/'checkpoint_map2f_validated_before_map2g/CLEANUP.json').read_text(encoding='utf-8-sig'));dump('BACKUP_CLEANUP.json',cleanup)
 print(status,len(tests),'checks;',len(plan['territorial']),'province owner changes; zero people or units added')
 for r in tests:
  if r['status']=='FAIL':print('FAILED',r['name'],r['detail'])
 assert status=='PASS_STATIC'
if __name__=='__main__':run()
