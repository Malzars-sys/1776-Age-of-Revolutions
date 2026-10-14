"""Independent conservation invariants for MAP2H. Not a native engine test."""
import collections as C,contextlib,hashlib,io,json,re,subprocess
import numpy as np
from PIL import Image
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from validate_map2f import population_profiles,unit_profiles
from map_1776_audit import effective
from map2h_work import ROOT,GAME,OUT,BASE,TARGETS,GIT,sha,source_bitmap,dump
import map2h_patch as patcher

def economic_profiles(inv):
 result=C.Counter()
 for row in inv['buildings']:
  sid,tag,body=row['key'];n=json.loads(body);rest=[v for v in n[2] if v[0]!='add_ownership'];kind=next(v[2] for v in rest if v[0]=='building')
  for own in [v for v in n[2] if v[0]=='add_ownership']:
   for h in own[2]:
    fields=[v for v in h[2] if v[0]!='levels'];country=next((v[2] for v in fields if v[0]=='country'),'c:'+tag)
    for field in fields:
     if field[0]=='region' and (country,field[2])==('c:DAI','STATE_MEKONG'):field[2]='STATE_TONKIN'
    area=sid
    if kind=='building_barrack' and country=='c:DAI' and sid in {'STATE_TONKIN','STATE_ANNAM','STATE_MEKONG'}:area='TRINH_BARRACK_POOL'
    if kind=='building_port' and country=='c:DEI' and sid in {'STATE_WEST_JAVA','STATE_MALAYA'}:area='DEI_BATAVIA_MALACCA_PORT_POOL'
    result[json.dumps([area,rest,h[0],fields],ensure_ascii=False,sort_keys=True)]+=int(next(v[2] for v in h[2] if v[0]=='levels'))*row['count']
 return result

def regional_levels(inv,sid,tag,kind):
 return sum(row['count']*int(v[2]) for row in inv['buildings'] if row['key'][:2]==[sid,tag] and any(c[0]=='building' and c[2]==kind for c in json.loads(row['key'][2])[2]) for o in json.loads(row['key'][2])[2] if o[0]=='add_ownership' for h in o[2] for v in h[2] if v[0]=='levels')

def run():
 base=json.loads(BASE.read_text());before=base['inventory'];after=qa.inventory();changed,plan,originals=patcher.transform(base);tests=[]
 def check(name,ok,detail=None):
  tests.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(tests[-1]['status'],name,flush=True)
 expected=qa.counter(before['owners'])
 for r in plan['territorial']:
  k=r['rgb'],r['state'],r['before'];assert expected[k]==1;expected[k]-=1;expected[r['rgb'],r['state'],r['after']]+=1
 for r in plan['duplicates_removed']:expected[r['rgb'],r['state'],r['owner']]-=1
 check('exact_RGB_owner_manifest',+expected==qa.counter(after['owners']))
 check('no_province_lost_or_created',{r['key'][0] for r in before['owners']}=={r['key'][0] for r in after['owners']} and before['geometry']==after['geometry'])
 check('all_67_transfers_in_R6',len(plan['territorial'])==67 and all(r['state'] in TARGETS for r in plan['territorial']))
 check('six_duplicate_RGBs_removed_50_to_44',len(before['duplicates'])==50 and len(after['duplicates'])==44 and all(before['duplicates'].get(k,0)>=v for k,v in after['duplicates'].items()))
 check('Mindanao_disputed_RGB_solely_MGD',[(r['key'],r['count']) for r in after['owners'] if r['key'][0]=='xE90347']==[(['xE90347','STATE_MINDANAO','MGD'],1)])
 check('no_new_orphan_history_reference',not set(map(str,after['errors']))-set(map(str,before['errors'])),after['errors'])
 check('world_population_835804980',sum(r['count'] for r in after['pops'])==835804980)
 check('all_culture_and_religion_counts_conserved',before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
 updated=dict(originals);updated.update({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in changed if p.startswith(('common/history/pops/','common/history/population/'))})
 bp,br,_=population_profiles(originals);ap,ar,_=population_profiles(updated)
 check('all_pop_attributes_status_literacy_qualifications_conserved',bp==ap)
 check('all_demographic_profiles_by_State_Region_conserved',br==ar)
 check('every_written_population_positive',all(int(n.one('size'))>0 for p,raw in updated.items() if p.startswith(('common/history/pops/','common/history/population/')) for n in cw.walk(cw.parse(raw)) if n.key=='create_pop'))
 check('all_declared_building_type_levels_conserved',before['building_levels_written']==after['building_levels_written'])
 check('PM_reserves_economic_holders_conserved',economic_profiles(before)==economic_profiles(after))
 check('55_DAI_barracks_conserved_and_owned', [regional_levels(after,s,'DAI','building_barrack') for s in ['STATE_TONKIN','STATE_ANNAM','STATE_MEKONG']]==[28,27,0])
 check('only_one_existing_port_level_Batavia_to_Malacca',[regional_levels(after,s,'DEI','building_port') for s in ['STATE_WEST_JAVA','STATE_MALAYA']]==[2,1])
 check('three_Annam_road_levels_split_two_plus_one',[regional_levels(after,'STATE_ANNAM',t,'building_railway') for t in ['DAI','TSN']]==[2,1])
 check('all_units_types_counts_formations_recruitments_identical',before['units']==after['units'] and unit_profiles(before)==unit_profiles(after))
 check('all_existing_military_and_character_files_byte_identical',all(sha(ROOT/p)==d for p,d in base['hashes'].items() if p.startswith(('common/history/military_formations/','common/history/characters/'))))
 actual=[p for p,d in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=d]
 check('existing_changes_exactly_approved_plan_and_bitmap',set(actual)==({p for p in changed if p in base['hashes']}|{'map_data/provinces.png'}),actual)
 check('applied_text_AST_matches_reviewed_plan',all([qa.norm(n) for n in cw.parse(txt)]==[qa.norm(n) for n in cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))] for p,txt in changed.items() if p.endswith('.txt')))
 check('all_MAP2A_to_G_reports_byte_identical',not any(p.startswith('docs/reports/') for p in actual))
 check('Ottoman_AI_technologies_goods_PM_assets_preserved',not any(p.startswith(('common/production_methods/','common/technology/','common/goods/','common/ai_','events/','common/journal_entries/','common/modifiers/','gfx/')) for p in actual))
 check('territory_outside_R6_identical',qa.counter([r for r in before['owners'] if r['key'][1] not in TARGETS])==qa.counter([r for r in after['owners'] if r['key'][1] not in TARGETS]))
 pairs={tuple(r) for r in after['states']};caps={}
 for tag in [*patcher.DEFS,'DAI','DGR','HAW','UNT','SRK','YOG','DEI','MGD']:
  n=json.loads(after['countries'][tag]);caps[tag]=next(v[2] for v in n[2] if v[0]=='capital')
 check('affected_capitals_owned',all((cap,tag) in pairs for tag,cap in caps.items()),caps)
 check('all_owner_tags_defined',all(r['key'][2] in after['countries'] for r in after['owners']))
 exceptions=set(patcher.DEFS)|{'DAI','DGR','HAW','UNT','SRK'}
 check('all_other_country_definitions_identical',{k:v for k,v in before['countries'].items() if k not in exceptions}=={k:v for k,v in after['countries'].items() if k not in exceptions})
 pop_by=C.Counter()
 for r in after['regional_pop']:pop_by[tuple(r['key'][:2])]+=r['count']
 check('new_subdivisions_have_existing_redistributed_population',all(pop_by[r['state'],r['after']]>0 for r in plan['territorial']))
 check('six_new_two_reused_tags_initially_inactive',not any(t in patcher.DEFS for _,t in before['states']) and len(plan['new_tags'])==6 and len(plan['reused_tags'])==2)
 init=cw.parse(changed['common/history/countries/1776_map2h_start.txt']);tags={n.key for n in cw.walk(init) if n.key.startswith('c:')}
 check('five_organized_governments_initialized',tags=={'c:ARK','c:VIE','c:TSN','c:NGN','c:HMA'})
 tech={n.key for p in effective(ROOT,GAME,'common/technology/technologies') for n in cw.parse(p.read_text(encoding='utf-8-sig'))};laws={n.key for p in effective(ROOT,GAME,'common/laws') for n in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig')))}
 check('initializer_technologies_and_laws_defined',all(cw.scalar(n.value) in tech for n in cw.walk(init) if n.key=='add_technology_researched') and all(cw.scalar(n.value).removeprefix('law_type:') in laws for n in cw.walk(init) if n.key=='activate_law'))
 cultures={n.key for p in effective(ROOT,GAME,'common/cultures') for n in cw.parse(p.read_text(encoding='utf-8-sig'))};religions={n.key for p in effective(ROOT,GAME,'common/religions') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
 check('new_country_cultures_religions_defined',all(v[3] in cultures and v[4] in religions for v in patcher.DEFS.values()))
 check('provisional_flags_native_pattern_exists',(GAME/'gfx/coat_of_arms/patterns/pattern_horizontal_split_01.tga').exists())
 # Entire physical map must be identical after undoing the exact 705 substitutions.
 pixelbase=json.loads((OUT/'PIXEL_BASELINE.json').read_text());supp=json.loads((OUT/'SUPPLEMENTAL_BASELINE.json').read_text());im=Image.open(source_bitmap());a=np.asarray(im).copy();ids=(a[:,:,0].astype(np.uint32)<<16)|(a[:,:,1].astype(np.uint32)<<8)|a[:,:,2]
 check('bitmap_format_dimensions_RGB_set_unchanged',im.mode=='RGB' and list(im.size)==pixelbase['size'] and [int(v) for v in np.unique(ids)]==pixelbase['RGB_IDs'])
 check('exactly_705_existing_land_RGB_substitutions',len(supp['pixels'])==705 and all(int(ids[y,x])==int(new[1:],16) for x,y,old,new in supp['pixels']))
 for x,y,old,new in supp['pixels']:
  v=int(old[1:],16);a[y,x]=[v>>16,(v>>8)&255,v&255]
 check('all_other_pixels_bit_exact_Avignon_Friuli_protected',hashlib.sha256(a.tobytes()).hexdigest()==pixelbase['uncompressed_RGB_sha256'])
 # Hubs are checked against physical native locators, not convenient city labels.
 ge=json.loads((OUT/'GEOGRAPHY.json').read_text());hubrows=[]
 for sid,fixes in plan['hub_fixes'].items():
  for kind,new in fixes.items():
   pos=ge['locators'][sid+'|'+kind];x,y=int(pos['x']),int(pos['y'])
   if sid=='STATE_HAWAIIAN_ISLANDS' and kind=='mine':x,y=545,1654
   actual_rgb='x%06X'%int(ids[y,x]);hubrows.append([sid,kind,new,actual_rgb])
 check('every_corrected_hub_matches_physical_RGB',all(n==r for _,_,n,r in hubrows),hubrows)
 check('Hawaii_new_wood_mine_positions_on_correct_island',['x%06X'%int(ids[y,x]) for x,y in [(529,1624),(545,1654)]]==['x6090C0','x492B26'])
 for kind in ['wood','mine']:
  p=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';old=supp['sources'][p]['text'];new=(ROOT/p).read_text(encoding='utf-8-sig');pattern=r'(id\s*=\s*309\s+position\s*=\s*\{)[^}]+'
  check('only_Hawaii_'+kind+'_locator_moved',re.sub(pattern,r'\1 HAWAII_POSITION ',old)==re.sub(pattern,r'\1 HAWAII_POSITION ',new))
 def nonhub(raw):
  return [[n.key,[qa.norm(c) for c in n.children() if c.key not in plan['hub_fixes'].get(n.key,{})]] for n in cw.parse(raw)]
 check('regional_resources_traits_other_hubs_preserved',all(nonhub(originals[p])==nonhub((ROOT/p).read_text(encoding='utf-8-sig')) for p in changed if p.startswith('map_data/state_regions/')))
 # Verify the four and only four superseded pacts; preserve all unrelated diplomacy.
 def pacts(raw):
  return C.Counter((c.key,json.dumps(qa.norm(n),ensure_ascii=False)) for c in cw.walk(cw.parse(raw)) for n in c.children('create_diplomatic_pact'))
 path='common/history/diplomacy/00_subject_relationships.txt';oldp=pacts(originals[path]);newp=pacts((ROOT/path).read_text(encoding='utf-8-sig'))
 removed=oldp-newp;keep=True
 for (parent,body),count in removed.items():
  nodes=json.loads(body)[2];country=next(v[2] for v in nodes if v[0]=='country');keep &= (parent,country) in {('c:SIA','c:LUA'),('c:SIA','c:CHP'),('c:CHI','c:LAN'),('c:DAI','c:CAM')} and count==1
 check('only_four_superseded_R6_pacts_removed',len(removed)==4 and keep and not (newp-oldp))
 alliance=[n for n in cw.walk(cw.parse(changed['common/history/diplomacy/1776_map2h_lao_alliance.txt'])) if n.key=='create_diplomatic_pact']
 check('Luang_Prabang_1774_alliance_not_1778_suzerainty',len(alliance)==1 and alliance[0].one('country')=='c:LUA' and alliance[0].one('type')=='alliance')
 for lang in ['english','french']:
  p=ROOT/f'localization/{lang}/replace/1776_map2h_l_{lang}.yml';raw=p.read_text(encoding='utf-8');keys=re.findall(r'^ ([A-Za-z0-9_]+):0 "[^"\r\n]*"$',raw,re.M)
  expectedloc={v for t in patcher.NAMES for v in [t,t+'_ADJ']}|{'aor1776_map2h_'+t.lower() for t in ['DAI','LAN','HAW','UNT']}|{'aor1776_map2h_trinh_sam','aor1776_map2h_kalaniopuu','aor1776_map2h_empty','aor1776_map2h_malacca'}
  check(lang+'_localization_BOM_unique_complete',raw.startswith('\ufeffl_'+lang+':') and set(keys)==expectedloc and len(keys)==len(set(keys)))
 effect=next(n for n in cw.parse(changed['common/scripted_effects/1776_map2h_state_names.txt']) if n.key=='assign_1776_map2h_split_state_name');limit=effect.children('if')[0].children('limit')[0]
 check('Malacca_name_only_Dutch_split_Malaya',limit.one('state_region')=='s:STATE_MALAYA' and limit.one('is_split_state')=='yes' and [n.key for n in limit.children('owner')[0].children()]==['c:DEI'])
 import validate_regional_infrastructure_shortage as infra
 for name,func in [('Ottoman_logical_models',cw.model_tests),('Infrastructure_IA_logical_models',infra.model_tests)]:
  try:
   with contextlib.redirect_stdout(io.StringIO()):func()
   check(name,True)
  except Exception as exc:check(name,False,str(exc))
 check('primary_HEAD_refs_index_unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==base['git']['refs'] and sha(ROOT/'.git/index')==base['git']['index'])
 check('MAP2G_remote_SHA256_restoration_verified',base['backup']['status']=='PASS_REMOTE_EXACT_RESTORATION' and base['backup']['sha256_all_files']=='MATCH')
 regions={r['state'] for r in plan['territorial']};op=qa.counter(before['regional_pop']);npop=qa.counter(after['regional_pop']);rows=[[*k,op[k],npop[k],npop[k]-op[k]] for k in sorted(set(op)|set(npop)) if k[0] in regions]
 status='PASS_STATIC' if all(t['status']=='PASS' for t in tests) else 'FAIL_STATIC'
 dump('MAP2H_VALIDATION.json',{'status':status,'checks':tests,'modified_files':plan['files']+['map_data/provinces.png'],'owner_transfers':len(plan['territorial']),'bitmap_pixels_changed':705,'bitmap_existing_RGBs_redrawn':3,'new_tags':plan['new_tags'],'reused_tags':plan['reused_tags'],'population_before':835804980,'population_after':sum(r['count'] for r in after['pops']),'all_population_attributes_conserved':bp==ap and br==ar,'building_economic_profiles_conserved':economic_profiles(before)==economic_profiles(after),'military_identical':before['units']==after['units'],'duplicates_before':len(before['duplicates']),'duplicates_after':len(after['duplicates']),'preexisting_reference_errors':after['errors'],'building_redistributions':plan['building_changes'],'economic_hq':plan['economic_hq'],'affected_capitals':caps,'allocation':plan['allocation'],'backup':base['backup'],'primary_git_unchanged':tests[-2]['status']=='PASS','native_game_test':'NOT_RUN; player explicitly performs new-game and one-month tests. Static invariants do not guarantee hiring, infrastructure availability, AI budgets or loading.','MAP2H_push':'NOT_PERFORMED; remains local until player validation.'})
 dump('TABLE_DATA.json',{'territorial':plan['territorial'],'duplicates_removed':plan['duplicates_removed'],'population':rows})
 print(status,len(tests),'checks;',len(plan['territorial']),'owner transfers')
 for t in tests:
  if t['status']=='FAIL':print('FAILED',t['name'],t['detail'])
 assert status=='PASS_STATIC'
if __name__=='__main__':run()
