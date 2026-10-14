"""Small MAP2I Basra follow-up baseline and independent checks. No main Git writes."""
import collections as C,contextlib,inspect,io,json,re,subprocess,sys
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from validate_map2f import unit_profiles,population_profiles
from map2i_work import ROOT,GAME,GIT,sha,source_bitmap
from map_1776_audit import effective,values
OUT=ROOT/'docs/reports/map/MAP2I/BASRA_SIEGE_FIX';BASE=OUT/'BASELINE.json'
MIL='common/history/military_formations/04_military_formations_middle_east.txt'
PLAY='common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt'
AID='common/history/treaties/08_1776_basra_ottoman_assistance.txt'
def dump(name,data):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def capture():
 assert not BASE.exists(),'Never replace pre-fix baseline'
 folders=['common','map_data','gfx','events','localization','gui','music','.metadata']+[f'docs/reports/map/MAP2{x}' for x in 'ABCDEFGHI']
 hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file() and OUT not in p.parents}
 originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/history').rglob('*.txt')}
 git={k:subprocess.check_output([GIT,*v],cwd=ROOT,text=True).strip() for k,v in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 inv=qa.inventory();assert sum(r['count'] for r in inv['pops'])==835804980
 dump('BASELINE.json',{'hashes':hashes,'originals':originals,'inventory':inv,'git':git,'bitmap_sha256':sha(source_bitmap()),'user_native_test':'MAP2I territory, capital, Khorasan, recruitment and infrastructure confirmed. Basra escalates to Ottoman-led coalition; deployment not measured.'})
 print('Captured current MAP2I; no ZIP or backup push')
def capacity(label):
 import persian_recruitment_map2e as pr
 b=json.loads(BASE.read_text());inv=b['inventory'] if label=='before' else qa.inventory();f=OUT/('CAPACITY_INPUT_'+label+'.json');f.write_text(json.dumps({'inventory':inv}),encoding='utf-8')
 src=inspect.getsource(pr.diagnose).replace("'PER'","'IR1'").replace("'c:PER'","'c:IR1'").replace("'region_state:PER'","'region_state:IR1'")
 scope=dict(pr.__dict__);scope['BASE']=f;scope['write']=lambda name,data:dump('CAPACITY_'+label+'_'+name,data)
 def scoped_unit_counts(inv):
  out=C.Counter()
  for (owner,sid,kind,service),n in counts(inv).items():
   if owner=='IR1':out[(sid,service)]+=n
  return out
 scope['unit_counts']=scoped_unit_counts
 exec(compile(src,'<existing capacity model scoped to IR1>','exec'),scope)
 with contextlib.redirect_stdout(io.StringIO()):scope['diagnose']()
 data=json.loads((OUT/('CAPACITY_'+label+'_CANDIDATES.json')).read_text())
 print(json.dumps([{k:r[k] for k in ['state','population','regular_before','conscript_before','civilian_usage_model','infrastructure_full_staffing_floor','workforce_model_25pct','civilian_jobs_explicit_full_capacity']} for r in data['rows']],indent=2));return data
def counts(inv):
 out=C.Counter()
 for r in inv['units']:
  n={k:v for k,op,v in json.loads(r['key'][3])[2]};out[(r['key'][0],r['key'][2],n['type'],n.get('service_type','regular'))]+=int(n['count'])*r['count']
 return out
def without_units(raw):
 def f(n):
  if n[0]=='combat_unit':return None
  return [n[0],n[1],[v for child in n[2] if (v:=f(child)) is not None]] if isinstance(n[2],list) else n
 return [f(qa.norm(n)) for n in cw.parse(raw)]
def save_evidence():
 original=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/save games/autosave_exit.v3');melted=ROOT/'.asset-cache/basra_siege_fix/latest_autosave_readonly.txt'
 with melted.open(encoding='utf-8') as stream:prefix=stream.read(3000)
 date=re.search(r'game_date=([^\s]+)',prefix).group(1)
 dump('SAVE_EVIDENCE.json',{'source_name':original.name,'source_sha256':sha(original),'decoded_game_date':date,'conversion':'Existing Rakaly read-only conversion, original save not changed','valid_January1776_deployment_evidence':False,'reason':'Latest autosave is October1777, not the initial January1776 war. Coalition totals from user are availability figures, not verified deployed forces. No native post-fix game launched.'})
 print('Latest autosave date',date,'not valid initial deployment evidence')
def validate():
 b=json.loads(BASE.read_text());before=b['inventory'];after=qa.inventory();checks=[]
 def check(name,passed,detail=None):checks.append({'name':name,'status':'PASS' if passed else 'FAIL','detail':detail})
 for key in before:
  if key!='units':check('preserved_inventory_'+key,before[key]==after[key])
 old=counts(before);new=counts(after);expected=old.copy();expected[('IR1','STATE_BAGHDAD','unit_type:combat_unit_type_irregular_infantry','regular')]-=5;expected[('IR1','STATE_BAGHDAD','unit_type:combat_unit_type_musket_infantry','regular')]+=5
 expected[('IR1','STATE_BASRA','unit_type:combat_unit_type_musket_infantry','regular')]+=10
 check('exact_IR1_upgrade_and_ten_new_permanents',+expected==new)
 check('IR1_20_regular_9_conscripts',sum(n for (t,s,u,k),n in new.items() if t=='IR1' and k=='regular')==20 and sum(n for (t,s,u,k),n in new.items() if t=='IR1' and k=='conscript')==9)
 check('non_IR1_units_unchanged',[r for r in before['units'] if r['key'][0]!='IR1']==[r for r in after['units'] if r['key'][0]!='IR1'])
 raw=(ROOT/MIL).read_text(encoding='utf-8-sig');check('commanders_formations_and_HQs_unchanged',without_units(b['originals'][MIL])==without_units(raw))
 country=cw.parse((ROOT/'common/history/countries/ir1 - mamluk iraq.txt').read_text(encoding='utf-8-sig'))[0].children()[0];owned={cw.scalar(n.value) for n in country.children('add_technology_researched')}
 units={n.key:n for p in effective(ROOT,GAME,'common/combat_unit_types') for n in cw.parse(p.read_text(encoding='utf-8-sig'))};required=set(values(units['combat_unit_type_musket_infantry'],'unlocking_technologies'));check('musket_technology_already_owned',required<=owned,sorted(required))
 check('new_recruitment_owned_and_populated',('STATE_BASRA','IR1') in map(tuple,after['states']) and sum(r['count'] for r in after['regional_pop'] if r['key'][:2]==['STATE_BASRA','IR1'])>0)
 cap=json.loads((OUT/'CAPACITY_after_CANDIDATES.json').read_text());row=next(r for r in cap['rows'] if r['state']=='STATE_BASRA');reserve=row['infrastructure_full_staffing_floor']-row['civilian_usage_model']-.2*row['regular_before'];workforce=row['workforce_model_25pct']-row['civilian_jobs_explicit_full_capacity']-1000*row['regular_before'];check('Basra_nominal_peacetime_reserve',reserve>0,round(reserve,3));check('Basra_free_workforce_proxy_margin',workforce>0,workforce)
 subj=(ROOT/'common/history/diplomacy/00_subject_relationships.txt').read_text(encoding='utf-8-sig');check('protectorate_and_all_other_subjects_identical',subj==b['originals']['common/history/diplomacy/00_subject_relationships.txt'])
 aid=(ROOT/AID).read_text(encoding='utf-8-sig');treaties=cw.parse(aid)[0].children('create_treaty');t=treaties[0];article=t.children('articles_to_create')[0].children()[0];check('one_directed_native_ottoman_assistance',len(treaties)==1 and t.one('first_country')=='c:TUR' and t.one('second_country')=='c:IR1' and article.one('article')=='military_assistance' and article.one('source_country')=='c:TUR' and article.one('target_country')=='c:IR1')
 check('native_assistance_definition_not_changed',sha(ROOT/'common/treaty_articles/12_military_assistance.txt')==b['hashes']['common/treaty_articles/12_military_assistance.txt'])
 changed=[p for p,h in b['hashes'].items() if sha(ROOT/p)!=h];check('only_authorized_existing_files_modified',set(changed)<={MIL,PLAY},changed)
 new_runtime={p.relative_to(ROOT).as_posix() for folder in ['common','map_data','gfx','events','localization','gui','music','.metadata'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in b['hashes']};check('only_assistance_runtime_file_added',new_runtime=={AID},sorted(new_runtime))
 for p in [MIL,PLAY,AID]:cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))
 check('changed_scripts_parse',True)
 check('one_Basra_mechanism_no_second_war_or_JE',sum(1 for p in effective(ROOT,GAME,'common/history/diplomatic_plays') for n in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))) if n.key=='add_war_goal' and n.one('target_state')=='s:STATE_BASRA.region_state:IR1' and n.one('holder')=='c:PER')==1 and not any(p.name.lower().startswith('basra') for p in (ROOT/'common/journal_entries').glob('*.txt')))
 current=(ROOT/PLAY).read_text(encoding='utf-8-sig');plays=[n for n in cw.walk(cw.parse(current)) if n.key=='create_diplomatic_play'];mode='COUNTEROFFENSIVE' if cw.parse(current)[0].children()[0].key=='c:IR1' else 'ORIGINAL_UNCHANGED'
 if mode=='COUNTEROFFENSIVE':
  play=plays[0];check('one_active_regional_native_play',len(plays)==1 and play.one('war')=='yes')
  check('PER_defender_and_OMA_IR1_backer',play.one('target_country')=='c:PER' and values(play,'add_initiator_backers')==['c:OMA'])
  check('no_TUR_backer_or_target','c:TUR' not in current)
  check('PER_primary_Basra_goal',any(n.one('holder')=='c:PER' and n.one('target_state')=='s:STATE_BASRA.region_state:IR1' and n.one('primary_demand')=='yes' for n in play.children('add_war_goal')))
  subjects={n.key:n for p in effective(ROOT,GAME,'common/subject_types') for n in cw.parse(p.read_text(encoding='utf-8-sig'))};check('native_protectorate_can_initiate_own_play',subjects['subject_type_protectorate'].one('can_start_own_diplomatic_plays')=='yes')
 else:check('regional_conflict_decision_pending',False,'Original offensive still auto-escalates; awaiting user choice.')
 suites={}
 import validate_regional_infrastructure_shortage as infra
 for name,fn in [('Ottoman_reforms',cw.model_tests),('Infrastructure_AI',infra.model_tests)]:
  log=io.StringIO()
  try:
   with contextlib.redirect_stdout(log):answer=fn()
   suites[name]={'status':'PASS','scenario_count':len(answer) if isinstance(answer,list) else None,'output':log.getvalue()};check(name,True)
  except Exception as ex:suites[name]={'status':'FAIL','error':str(ex)};check(name,False,str(ex))
 check('primary_Git_HEAD_refs_index_unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==b['git']['refs'] and sha(ROOT/'.git/index')==b['git']['index'])
 result={'status':'PASS_STATIC_NATIVE_TEST_REQUIRED' if all(c['status']=='PASS' for c in checks) else 'FAIL_OR_INCOMPLETE','mechanism':mode,'checks':checks,'regression_suites':suites,'changed_runtime_files':changed+[AID],'population':835804980,'IR1_regular_before':10,'IR1_regular_after':20,'IR1_conscripts':9,'native_post_fix_test':'NOT_RUN','native_protectorate_nonintervention':'HYPOTHESIS_REQUIRES_NEW_GAME_NOT_ESTABLISHED_BY_AST','Basra_capacity':row,'Basra_nominal_reserve':reserve,'Basra_workforce_proxy':workforce,'military_assistance_unlock':'general_staff absent: predefined historical treaty, native initialization to verify; no technology granted or global unlock altered.'}
 dump('VALIDATION.json',result);print(result['status'],len(checks),'checks')
 for c in checks:
  if c['status']=='FAIL':print(c['name'],c['detail'])
 return result
if __name__=='__main__':
 op=sys.argv[1]
 if op=='capture':capture()
 elif op=='save-evidence':save_evidence()
 elif op=='validate':validate()
 else:capacity(op)
