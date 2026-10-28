"""R9-04: bounded 1776 Araucanian/Huilliche autonomy; no bitmap redrawing.

Prepare from the current workspace, then hash-guard apply and independently verify.
Existing cohorts move intact; regional native aggregates are not surveyed states.
"""
import collections as C
import json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,NATIVE_LAWS,ownership
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from central01 import cohorts

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-04'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt'
PREFIX='1776_r904_huilliche';TAG='H91'
MOVES={
 'STATE_LOS_RIOS':('PAT','xF2263F x90C050 x90C0D0 x02C052 x49F9FC x3D3ED8 xCFB481 x142AEF x83D701'.split()),
 'STATE_ARAUCANIA':(TAG,'x521B0A x9EF738 x45155F x144683 x4A805F xB79F3F x592AB4'.split())}
LEDGER=[('STATE_LOS_RIOS','PAT',33682),('STATE_ARAUCANIA',TAG,2246)]
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def assigns(raw):
 return C.Counter((r,s,scalar(z.one('country'))[2:]) for s,n in state_nodes(raw).items() for z in n.children('create_state') for r in provs(z,'owned_provinces'))
def prepare():
 assert not (OUT/'APPLIED.json').exists();OUT.mkdir(parents=True,exist_ok=True)
 base=runtime();defs={n.key for p in effective('common/country_definitions') for n in parse(text(p))};assert TAG not in defs
 raw=text(ROOT/ST);nodes=state_nodes(raw);edits=[]
 for sid,(tag,rgbs) in MOVES.items():
  n=nodes[sid];old=[z for z in n.children('create_state') if z.one('country')=='c:SC3'];assert len(old)==1
  z=old[0];v=z.children('owned_provinces')[0];before=provs(z,'owned_provinces');assert set(rgbs)<=set(before)
  assert not any(z.one('country')=='c:'+tag for z in n.children('create_state'))
  edits.append((v.start,v.end,'owned_provinces = '+rgb_block([r for r in before if r not in rgbs])))
  edits.append((n.end-1,n.end-1,'\n\t\tcreate_state = { country = c:'+tag+' owned_provinces = '+rgb_block(rgbs)+' state_type = incorporated }\n\t'))
  # Territorial pretension retained, without confusing it with administration.
  if not any(scalar(c.value)=='c:SC3' for c in n.children('add_claim')):
   edits.append((n.end-1,n.end-1,'\n\t\tadd_claim = c:SC3\n\t'))
 files={ST:encoded(ROOT/ST,edit(raw,edits))}
 raw=text(ROOT/PP);nodes=state_nodes(raw);edits=[]
 for sid,tag,amount in LEDGER:
  n=nodes[sid];rs=n.children('region_state:SC3')[0];p=[z for z in rs.children('create_pop') if scalar(z.one('culture'))=='patagonian'];assert len(p)==1 and int(p[0].one('size'))==amount
  z=p[0];assert not n.children('region_state:'+tag)
  edits.extend([(z.start,z.end,''),(n.end-1,n.end-1,'\n\t\tregion_state:'+tag+' = { '+raw[z.start:z.end]+' }\n\t')])
 files[PP]=encoded(ROOT/PP,edit(raw,edits))
 files['common/country_definitions/'+PREFIX+'.txt']=('''# R9-04: regional autonomous Huilliche chiefdoms, not a unified monarchy.
H91 = { color = { 139 164 80 } country_type = decentralized tier = principality
 cultures = { patagonian } religion = animist capital = STATE_ARAUCANIA }
''').encode()
 hist='COUNTRIES = { c:H91 ?= {\n # Subsistence profile only; no imported industrial/military tier.\n add_technology_researched = traditional_food_processing\n'+''.join(' activate_law = law_type:law_'+v+'\n' for v in NATIVE_LAWS)+' } }\n'
 files['common/history/countries/'+PREFIX+'.txt']=hist.encode()
 files['common/flag_definitions/'+PREFIX+'.txt']=('H91 = { flag_definition = { coa = aor1776_r904_huilliche priority = 100 allow_overlord_canton = no } }\n').encode()
 files['common/coat_of_arms/coat_of_arms/'+PREFIX+'.txt']=('''# Generic game emblem; no claim to an attested eighteenth-century flag.
aor1776_r904_huilliche = { pattern = "pattern_solid.tga" color1 = "green"
 colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 0.8 0.8 } } } }
''').encode()
 for lang,name,adj in [('french','Huilliches du Futahuillimapu','huilliche'),('english','Futahuillimapu Huilliche','Huilliche')]:
  files[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']=b'\xef\xbb\xbf'+f'l_{lang}:\n H91:0 "{name}"\n H91_ADJ:0 "{adj}"\n'.encode('utf8')
 files['common/history/buildings/1776_r904_chiloe_port.txt']=('''# Chiloé/Calbuco maritime supply; mainland autonomy interrupts the land route.
BUILDINGS = { s:STATE_ARAUCANIA = { region_state:SC3 = {
 create_building = { building = building_port level = 1 reserves = 1
 activate_production_methods = { pm_aor1776_traditional_commercial_harbor pm_1776_no_raw_data_reporting } }
} } }
''').encode()
 m=dict(input_sha256={},output_sha256={})
 for rel,data in files.items():
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  p=ROOT/rel;b=OUT/'before'/rel;q=OUT/'patch'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  if p.exists():b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(p.read_bytes())
  m['input_sha256'][rel]=sha(p) if p.exists() else None;m['output_sha256'][rel]=sha(q)
 dump('PATCH.json',m);dump('PREPARE_RUNTIME.json',base)
 dump('PLAN.json',dict(date='2026-10-28',reference_date='1776-01-01',transfers=MOVES,population_transfers=LEDGER,population_added=0,new_state_regions=0,bitmap_changed=False,new_country=TAG,representation='Regional Huilliche chiefdom aggregate; existing coarse patagonian culture retained, not an ethnographic census.',port_added='SC3 STATE_ARAUCANIA, level 1, historical maritime dependency',historical_limits='SOURCES.md',engine_tested=False))
 dump('TECH_EXPECTATIONS.json',{TAG:dict(required=['traditional_food_processing'],allowed=['traditional_food_processing'],historical_evidence='R9-04/SOURCES.md: autonomous subsistence chiefdoms; no installed industrial buildings, military formations or European tier copied.')})
 print(json.dumps(dict(files=len(files),provinces=sum(len(v[1]) for v in MOVES.values()),population_moved=sum(x[2] for x in LEDGER),new_population=0)))
def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists()
 assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==h for r,h in m['input_sha256'].items()),'Current shared content changed; re-examine patch'
 assert all(sha(OUT/'patch'/r)==h for r,h in m['output_sha256'].items())
 for r in m['output_sha256']:(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
def verify():
 m=load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();checks={}
 checks['installed_hashes']=all(sha(ROOT/r)==h for r,h in m['output_sha256'].items())
 checks['modified_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'] if r.endswith('.txt'))
 old=assigns(text(OUT/'before'/ST));expected=old.copy()
 for sid,(tag,rgbs) in MOVES.items():
  for r in rgbs:assert expected[r,sid,'SC3']==1;expected[r,sid,'SC3']-=1;expected[r,sid,tag]+=1
 actual=assigns(text(ROOT/ST));checks['only_16_authorized_owner_transfers']=+expected==actual
 oldby=C.Counter();newby=C.Counter()
 for (r,s,t),v in old.items():oldby[r]+=v
 for (r,s,t),v in actual.items():newby[r]+=v
 checks['no_new_duplicate_or_unowned_province']=oldby==newby
 ns=state_nodes(text(ROOT/ST));checks['all_created_portions_nonempty']=all(provs(z,'owned_provinces') for sid in MOVES for z in ns[sid].children('create_state'))
 checks['same_regional_population_and_identity']=cohorts(text(OUT/'before'/PP))==cohorts(text(ROOT/PP))
 def popcounts(raw):
  return C.Counter({(sid,rs.key,json.dumps(normalized([p]),sort_keys=True)):1 for sid,n in state_nodes(raw).items() for rs in n.children() for p in rs.children('create_pop')})
 a=popcounts(text(OUT/'before'/PP));b=popcounts(text(ROOT/PP));expectedpop=a.copy()
 for sid,tag,amount in LEDGER:
  before=next(k for k in a if k[0]==sid and k[1]=='region_state:SC3' and 'patagonian' in k[2]);expectedpop[before]-=1;expectedpop[(sid,'region_state:'+tag,before[2])]+=1
 checks['only_two_intact_cohort_owner_changes']=+expectedpop==b
 shares={(s,scalar(z.one('country'))[2:]) for s,n in ns.items() for z in n.children('create_state')}
 checks['changed_populations_have_owned_land']=all((sid,rs.key.split(':')[1]) in shares for sid in MOVES for rs in state_nodes(text(ROOT/PP))[sid].children() if rs.children('create_pop'))
 checks['existing_building_files_identical']=all(now.get(r)==h for r,h in base.items() if r.startswith('common/history/buildings/'))
 checks['existing_countries_diplomacy_formations_identical']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/country_definitions/','common/history/countries/','common/history/diplomacy/','common/history/military_formations/')))
 checks['bitmap_regions_terrain_locators_identical']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/')))
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))}
 checks['province_membership_verified']=all(set(rs)<=set(provs(regs[sid],'provinces')) for sid,(tag,rs) in MOVES.items())
 own=ownership();checks['spanish_forts_and_coastal_nodes_retained']=all(own[r]=={(s,'SC3')} for r,s in [('x1A5ED2','STATE_LOS_RIOS'),('xF68D31','STATE_LOS_RIOS'),('x8848C6','STATE_LOS_RIOS'),('xF0CA34','STATE_LOS_RIOS'),('x9040D0','STATE_LOS_RIOS'),('x42A6B5','STATE_LOS_RIOS'),('xEFB409','STATE_ARAUCANIA'),('x553B3F','STATE_ARAUCANIA'),('xC42462','STATE_ARAUCANIA')])
 checks['new_capital_has_land']=('STATE_ARAUCANIA',TAG) in shares
 checks['chiloe_port_on_retained_spanish_hub']=scalar(regs['STATE_ARAUCANIA'].one('port'))=='x553B3F' and own['x553B3F']=={('STATE_ARAUCANIA','SC3')}
 rel='common/history/buildings/1776_r904_chiloe_port.txt';bs=[z for z in walk(parse(text(ROOT/rel))) if z.key=='create_building']
 checks['only_one_level_of_port_added']=len(bs)==1 and bs[0].one('building')=='building_port' and bs[0].one('level')=='1'
 laws={n.key for p in effective('common/laws') for n in parse(text(p))};checks['new_requested_laws_exist']=all('law_'+v in laws for v in NATIVE_LAWS)
 tech={n.key:n for p in effective('common/technology/technologies') for n in parse(text(p))};checks['new_technology_exists']='traditional_food_processing' in tech
 cultures={n.key for p in effective('common/cultures') for n in parse(text(p))};religions={n.key for p in effective('common/religions') for n in parse(text(p))};checks['new_culture_and_religion_exist']='patagonian' in cultures and 'animist' in religions
 checks['generic_flag_assets_exist']=all(any((p/f).exists() for p in [ROOT,GAME]) for f in ['gfx/coat_of_arms/patterns/pattern_solid.tga','gfx/coat_of_arms/colored_emblems/ce_bend_dexter.dds'])
 checks['french_english_localizations_valid']=all((ROOT/f'localization/{l}/replace/{PREFIX}_l_{l}.yml').read_bytes().startswith(b'\xef\xbb\xbf') and len(re.findall(r'^ H91(?:_ADJ)?:0 "[^"\n]+"$',text(ROOT/f'localization/{l}/replace/{PREFIX}_l_{l}.yml'),re.M))==2 for l in ['french','english'])
 defs=[n for p in effective('common/country_definitions') for n in parse(text(p)) if n.key==TAG];checks['one_decentralized_huilliche_definition']=len(defs)==1 and defs[0].one('country_type')=='decentralized'
 checks['prior_central_and_sacramento_cores_retained']=all(own[r]=={(sid,t)} for r,sid,t in [('x4E1443','STATE_URUGUAY','BRZ'),('xB0243F','STATE_COSTA_RICA','G81'),('xBB820B','STATE_PANAMA','K81'),('x446C64','STATE_WEST_INDIES','C81')])
 external={r:dict(before=base.get(r),after=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change']=not external
 checks={k:bool(v) for k,v in checks.items()};dump('VALIDATION.json',dict(date='2026-10-28',checks=checks,passed=sum(checks.values()),total=len(checks),engine_tested=False,human_validated=False))
 print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())
def preview():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];box=(2395,2965,2500,3170);x0,y0,x1,y1=box;crop=a[y0:y1,x0:x1];own=ownership();oldown={}
 for r,s,t in assigns(text(OUT/'before'/ST)):oldown[r]=t
 colors={'SC3':(227,190,75),'PAT':(183,83,74),'H91':(139,164,80),'THL':(73,142,147),'SLK':(139,101,156)}
 scale=4;w=(x1-x0)*scale;h=(y1-y0)*scale;out=Image.new('RGB',(w*2+40,h+155),(34,47,58));d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 for index,owners in enumerate([oldown,{r:next(iter(v))[1] for r,v in own.items() if len(v)==1}]):
  rgb=np.full((*crop.shape,3),[34,47,58],dtype='uint8')
  for c in np.unique(crop):
   tag=owners.get(f'x{int(c):06X}');rgb[crop==c]=colors.get(tag,(72,80,78))
  boundary=np.zeros(crop.shape,dtype=bool);boundary[1:,:]|=crop[1:,:]!=crop[:-1,:];boundary[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[boundary]=rgb[boundary]//2
  out.paste(Image.fromarray(rgb).resize((w,h),Image.Resampling.NEAREST),(10+index*(w+20),55));d.text((10+index*(w+20),18),['Avant','R9-04 installé — 1er janvier 1776'][index],font=font,fill='white')
 d.text((12,h+70),'Or : SC3 | Rouge : Mapuche | Vert : Huilliches | Bleu : Tehuelche',font=small,fill='white')
 d.text((12,h+95),'16 provinces transférées ; 35 928 habitants déplacés, aucun ajouté.',font=small,fill='white')
 d.text((12,h+118),'Frontières approximées par provinces existantes. Validation en jeu à effectuer.',font=small,fill='white');out.save(OUT/'R9_04_AVANT_APRES.png')
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
 elif '--preview' in sys.argv:preview()
