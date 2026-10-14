"""Independent conservation and focused MAP2I static checks; never launch the game."""
import collections as C,contextlib,io,json,re,subprocess
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from validate_map2f import population_profiles,unit_profiles
from map_1776_audit import effective,values
from map2a_patch import edits
from map2i_work import ROOT,GAME,OUT,BASE,sha,source_bitmap,dump
import map2i_patch as patch
def originals():
 return {p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names','common/government_types'] for p in (ROOT/f).rglob('*.txt')}
def building_profiles(inv,normalize_hq=False):
 out=C.Counter()
 for row in inv['buildings']:
  sid,tag,body=row['key'];n=json.loads(body)
  for h in n[2]:
   if h[0]=='add_ownership':
    for own in h[2]:
     if normalize_hq and own[0]=='building' and any(v[0]=='country' and v[2]=='c:PER' for v in own[2]):
      for v in own[2]:
       if v[0]=='region' and v[2]=='STATE_KHORASAN':v[2]='STATE_KERMAN'
  out[(sid,json.dumps(n,sort_keys=True))]+=row['count']
 return out
def military(inv):
 out=C.Counter()
 for r in inv['units']:
  fields={k:v for k,op,v in json.loads(r['key'][3])[2]};out[(r['key'][0],r['key'][2],fields.get('service_type','regular'))]+=int(fields['count'])*r['count']
 return out
def nonunits(raw):
 def f(n):
  if n[0]=='combat_unit':return None
  return [n[0],n[1],[v for child in n[2] if (v:=f(child)) is not None]] if isinstance(n[2],list) else n
 return [f(qa.norm(n)) for n in cw.parse(raw)]
def validate():
 base=json.loads(BASE.read_text());before=base['inventory'];after=qa.inventory();now=originals();planned,plan=patch.transform(base);checks=[]
 def check(name,passed,detail=None):checks.append({'name':name,'status':'PASS' if passed else 'FAIL','detail':detail})
 expected=qa.counter(before['owners'])
 for r in plan['territorial']:expected[(r['rgb'],r['state'],r['before'])]-=1;expected[(r['rgb'],r['state'],r['after'])]+=1
 check('exact_owner_manifest_75',len(plan['territorial'])==75 and +expected==qa.counter(after['owners']))
 check('same_all_owned_RGBs',{r['key'][0] for r in before['owners']}=={r['key'][0] for r in after['owners']})
 check('geometry_identical',before['geometry']==after['geometry']);check('bitmap_identical',sha(source_bitmap())==base['bitmap_sha256'])
 check('no_new_duplicate_44',before['duplicates']==after['duplicates'] and len(after['duplicates'])==44)
 check('no_new_orphans',not set(map(str,after['errors']))-set(map(str,before['errors'])),after['errors'])
 check('global_population_835804980',sum(r['count'] for r in after['pops'])==835804980)
 check('culture_religion_populations_preserved',before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
 a,b,c=population_profiles(base['originals']);d,e,f=population_profiles(now)
 check('every_population_attribute_global',a==d);check('every_population_attribute_by_region',b==e)
 expect=C.Counter()
 for (sid,tag,attrs),n in c.items():expect[(sid,'AFH' if (sid,tag)==('STATE_KHORASAN','PER') else tag,attrs)]+=n
 check('exact_population_political_reassignment',expect==f)
 check('written_building_levels_preserved',before['building_levels_written']==after['building_levels_written'])
 check('building_types_PM_reserves_and_holders',building_profiles(before,True)==building_profiles(after))
 expected_b=qa.counter(before['buildings']);rewritten=C.Counter()
 for (sid,tag,body),n in expected_b.items():
  parsed=cw.parse('x = '+body) if False else json.loads(body)
  for h in parsed[2]:
   if h[0]=='add_ownership':
    for own in h[2]:
     if own[0]=='building' and any(v[0]=='country' and v[2]=='c:PER' for v in own[2]):
      for v in own[2]:
       if v[0]=='region' and v[2]=='STATE_KHORASAN':v[2]='STATE_KERMAN'
  rewritten[(sid,'AFH' if (sid,tag)==('STATE_KHORASAN','PER') else tag,json.dumps(parsed,ensure_ascii=False,separators=(',',':')))]+=n
 check('exact_physical_building_manifest',rewritten==qa.counter(after['buildings']))
 check('all_national_units_types_services_formations',unit_profiles(before)==unit_profiles(after))
 check('all_non_Persian_recruitment_unchanged',[r for r in before['units'] if r['key'][0]!='PER']==[r for r in after['units'] if r['key'][0]!='PER'])
 counts=military(before);expected_units=counts.copy()
 for source,dest,service,num in plan['military_recruitment']:expected_units[('PER',source,service)]-=num;expected_units[('PER',dest,service)]+=num
 check('exact_five_recruitment_moves',+expected_units==military(after) and sum(r[3] for r in plan['military_recruitment'])==5)
 check('Persia_32_regular_38_conscripts',sum(n for (t,s,k),n in military(after).items() if t=='PER' and k=='regular')==32 and sum(n for (t,s,k),n in military(after).items() if t=='PER' and k=='conscript')==38)
 states={tuple(s) for s in after['states']};check('all_Persian_recruitment_owned',all((r['key'][2],'PER') in states for r in after['units'] if r['key'][0]=='PER'))
 p='common/history/military_formations/04_military_formations_middle_east.txt';check('commanders_formations_HQs_unchanged',nonunits(base['originals'][p])==nonunits(now[p]))
 for sid in ['STATE_TABRIZ','STATE_FARS','STATE_ISFAHAN','STATE_IRAKAJEMI','STATE_SEMNAN']:check('protected_recruitment_'+sid,[r for r in before['units'] if r['key'][2]==sid]==[r for r in after['units'] if r['key'][2]==sid])
 check('only_PER_capital_and_AFH_country_defined',set(after['countries'])==set(before['countries'])|{'AFH'} and all(after['countries'][t]==v for t,v in before['countries'].items() if t!='PER'))
 for tag,sid in [('PER','STATE_FARS'),('AFH','STATE_KHORASAN')]:
  definition=json.loads(after['countries'][tag]);cap=next(v[2] for v in definition[2] if v[0]=='capital');check(tag+'_capital_valid',cap==sid and (sid,tag) in states)
 geo=json.loads((OUT/'GEOGRAPHY.json').read_text())['locators']
 for sid,tag in [('STATE_KHORASAN','AFH'),('STATE_FARS','PER')]:
  g=geo[sid+'|city'];check(sid+'_physical_city_selector',g['rgb']==g['selector'] and any(r['key']==[g['rgb'],sid,tag] for r in after['owners']),g)
 check('actual_PATCH_sources_match',all((ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff') for p,raw in planned.items()))
 altered=[p for p,h in base['hashes'].items() if sha(ROOT/p)!=h];check('no_other_runtime_or_prior_report_changed',set(altered)<=set(plan['files']),altered)
 for p in plan['files']:
  if p.endswith('.txt'):cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))
 check('changed_Paradox_script_syntax',True)
 t=cw.parse(now['common/history/treaties/07_1776_map2i_afsharids.txt'])[0].children('create_treaty');check('one_native_Durrani_guarantee_not_subject',len(t)==1 and t[0].one('first_country')=='c:DUR' and t[0].one('second_country')=='c:AFH' and 'create_diplomatic_pact' not in now['common/history/diplomacy/07_1776_map2i_afsharids.txt'])
 check('native_guarantee_article_exists',(GAME/'common/treaty_articles/02_guarantee_independence.txt').exists())
 af=cw.parse(now['common/history/countries/afh - afsharid khorasan.txt'])[0].children()[0];tech={cw.scalar(n.value) for n in af.children('add_technology_researched')};check('AFH_Persian_initial_technology_parity',tech=={cw.scalar(n.value) for n in cw.parse(now['common/history/countries/per - persia.txt'])[0].children()[0].children('add_technology_researched')})
 ruler=cw.parse(now['common/history/characters/afh - afsharid khorasan.txt'])[0].children()[0].children('create_character');check('one_historical_Shahrokh',len(ruler)==1 and ruler[0].one('ruler')=='yes' and ruler[0].one('first_name')=='aor1776_map2i_shahrokh')
 raw=now['common/dynamic_country_names/00_dynamic_country_names.txt'];per=next(n for n in cw.parse(raw) if n.key=='PER');zand=next(n for n in per.children('dynamic_country_name') if n.one('name')=='dyn_c_zand_iran');check('Zand_context_not_permanent','per_karim_khand_zand_template' in raw[zand.start:zand.end] and 'qajar_iran' in raw[zand.start:zand.end])
 war=now['common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt'];old=base['originals']['common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt'];norm=lambda raw:[qa.norm(n) for n in cw.parse(raw)];check('Basra_only_war_switch_same_system',norm(war.replace('war = yes','war = no'))==norm(old))
 check('Basra_not_annexed',[r for r in before['owners'] if r['key'][1]=='STATE_BASRA']==[r for r in after['owners'] if r['key'][1]=='STATE_BASRA'])
 suites={}
 import validate_regional_infrastructure_shortage as infr
 for name,fn in [('Ottoman_objectives',cw.model_tests),('Infrastructure_AI',infr.model_tests)]:
  log=io.StringIO()
  try:
   with contextlib.redirect_stdout(log):answer=fn()
   suites[name]={'status':'PASS','result':answer,'output':log.getvalue()};check(name,True)
  except Exception as ex:suites[name]={'status':'FAIL','error':str(ex)};check(name,False,str(ex))
 check('primary_Git_HEAD_refs_index_preserved',subprocess.check_output([__import__('map2i_work').GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git']['head'] and subprocess.check_output([__import__('map2i_work').GIT,'show-ref'],cwd=ROOT,text=True).strip()==base['git']['refs'] and sha(ROOT/'.git/index')==base['git']['index'])
 # Reuse the existing employment model, redirecting ALL its report writes here.
 import persian_recruitment_map2e as pr
 model=OUT/'CAPACITY_MODEL_INPUT.json';model.write_text(json.dumps({'inventory':after}),encoding='utf-8');pr.BASE=model;pr.write=lambda name,data:dump('CAPACITY_'+name,data)
 with contextlib.redirect_stdout(io.StringIO()):pr.diagnose()
 modeldata=json.loads((OUT/'CAPACITY_CANDIDATES.json').read_text());recipients={r[1] for r in plan['military_recruitment']};rows=[r for r in modeldata['rows'] if r['state'] in recipients]
 check('recipient_peacetime_nominal_reserves',all(r['infrastructure_full_staffing_floor']-r['civilian_usage_model']-.2*r['regular_before']>0 for r in rows),[{k:r[k] for k in ['state','population','regular_before','conscript_before','infrastructure_full_staffing_floor','civilian_usage_model']} for r in rows])
 check('recipient_free_workforce_model',all(r['workforce_model_25pct']-r['civilian_jobs_explicit_full_capacity']-1000*r['regular_before']>0 for r in rows))
 profiles=[]
 for (sid,tag,attrs),n in sorted(c.items()):
  if sid=='STATE_KHORASAN':
   pp={k:v for k,op,v in json.loads(attrs)};profiles.append([sid,tag,'AFH',pp.get('culture'),pp.get('religion','DEFAULT:'+pp.get('culture')),pp.get('pop_type','native_default'),n,n,0])
 dump('TABLE_DATA.json',{'territorial':plan['territorial'],'population':profiles,'population_total':sum(r[6] for r in profiles),'military_moves':plan['military_recruitment']})
 result={'status':'PASS_STATIC' if all(r['status']=='PASS' for r in checks) else 'FAIL_STATIC','native_test':'NOT_RUN_PLAYER_WILL_TEST','checks':checks,'regression_suites':suites,'world_population':835804980,'duplicates_before':44,'duplicates_after':len(after['duplicates']),'transferred_RGBs':75,'transferred_people':sum(r[6] for r in profiles),'new_tags':['AFH'],'modified_runtime_files':plan['files'],'capacity_limitations':modeldata['limitations'],'backup':base['backup'],'accepted_limits':['Coarse Afsharid regional aggregation','Local Qajar authority not mapped into a new empire','BHN coastal/island abstraction retained with Nasr al-Madhkur','Native loading, foreign holdings and new markets require player test']}
 dump('MAP2I_VALIDATION.json',result);print(result['status'],len(checks),'checks; people',result['transferred_people'])
 for r in checks:
  if r['status']=='FAIL':print('FAIL',r['name'],r['detail'])
 return result
if __name__=='__main__':validate()
