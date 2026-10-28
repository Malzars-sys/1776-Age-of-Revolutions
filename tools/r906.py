"""R9-06: documented colonial cores and bounded autonomous interiors.

Existing provinces and WYU definition. No new population, RGB or buildings.
Prepare uses current shared files; apply refuses changed inputs.
"""
import collections as C,json,sys,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,ownership
from validate_diplomacy_ottoman_1776 import parse,scalar,normalized
from central01 import cohorts
from r904 import assigns
from hbc04_land_links import flood,pair,path

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-06'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt'
TRANSFERS=[('STATE_ANTIOQUIA','xC564C3','SC2','WYU'),('STATE_ANTIOQUIA','xF2F0CC','SC2','WYU'),('STATE_GUAYANA','x7B4B5E','AP7','NET'),('STATE_GUAYANA','x439BC2','AP7','FRA'),('STATE_GUAYANA','x148FB5','FRA','AP7'),('STATE_GUAYANA','x9F0090','FRA','AP7'),('STATE_GUAYANA','xC2E46E','NET','AP7')]
DUPLICATE='x6C6251';PREFIX='1776_r906_wayuu'
# Core institutional abstractions only. No imported industrial/military tier,
# forced closed-border/isolationist package, or modern commercial-insurance grant.
LAWS=['chiefdom','state_religion','hereditary_bureaucrats','subjecthood','traditionalism','peasant_levies','consumption_based_taxation','guild_system','no_migration_controls']
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def prepare():
 assert not (OUT/'APPLIED.json').exists();own=ownership();assert own[DUPLICATE]=={('STATE_GUAYANA','AP7'),('STATE_GUAYANA','NET')}
 raw=text(ROOT/ST);ns=state_nodes(raw);edits=[]
 for sid in ['STATE_ANTIOQUIA','STATE_GUAYANA']:
  n=ns[sid];old=n.children('create_state');target={scalar(z.one('country'))[2:]:set(provs(z,'owned_provinces')) for z in old}
  for s,r,b,t in TRANSFERS:
   if s!=sid:continue
   assert own[r]=={(s,b)};target[b].remove(r);target.setdefault(t,set()).add(r)
  if sid=='STATE_GUAYANA':target['AP7'].remove(DUPLICATE)
  for z in old:
   tag=scalar(z.one('country'))[2:];p=z.children('owned_provinces')[0];edits.append((p.start,p.end,'owned_provinces = '+rgb_block(target[tag])))
  if sid=='STATE_ANTIOQUIA':
   assert not any(z.one('country')=='c:WYU' for z in old)
   edits.append((n.end-1,n.end-1,'\n\t\tcreate_state = { country = c:WYU owned_provinces = '+rgb_block(target['WYU'])+' state_type = incorporated }\n\t'))
   if not any(scalar(z.value)=='c:SC2' for z in n.children('add_claim')):edits.append((n.end-1,n.end-1,'\n\t\tadd_claim = c:SC2\n\t'))
 files={ST:encoded(ROOT/ST,edit(raw,edits))}
 raw=text(ROOT/PP);n=state_nodes(raw)['STATE_ANTIOQUIA'];rs=n.children('region_state:SC2')[0];pops=[z for z in rs.children('create_pop') if z.one('culture')=='guajiro'];assert len(pops)==1 and pops[0].one('size')=='7600' and not n.children('region_state:WYU');z=pops[0]
 files[PP]=encoded(ROOT/PP,edit(raw,[(z.start,z.end,''),(n.end-1,n.end-1,'\n\t\tregion_state:WYU = { '+raw[z.start:z.end]+' }\n\t')]))
 hist='COUNTRIES = { c:WYU ?= {\n # Autonomous pastoral/fishing communities; no imported European tier.\n add_technology_researched = traditional_food_processing\n'+''.join(' activate_law = law_type:law_'+k+'\n' for k in LAWS)+'} }\n'
 files['common/history/countries/'+PREFIX+'.txt']=hist.encode()
 files['common/flag_definitions/'+PREFIX+'.txt']=('WYU = { flag_definition = { coa = aor1776_r906_wayuu priority = 100 allow_overlord_canton = no } }\n').encode()
 files['common/coat_of_arms/coat_of_arms/'+PREFIX+'.txt']=('''# Generic game emblem, not an attested eighteenth-century Wayuu national flag.
aor1776_r906_wayuu = { pattern = "pattern_solid.tga" color1 = "green"
 colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 0.8 0.8 } } } }
''').encode()
 m=dict(input_sha256={},output_sha256={})
 for r,b in files.items():
  parse(b.decode('utf-8-sig'));p=ROOT/r;q=OUT/'patch'/r;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
  if p.exists():z=OUT/'before'/r;z.parent.mkdir(parents=True,exist_ok=True);z.write_bytes(p.read_bytes())
  m['input_sha256'][r]=sha(p) if p.exists() else None;m['output_sha256'][r]=sha(q)
 dump('PATCH.json',m);dump('PREPARE_RUNTIME.json',runtime());dump('PLAN.json',dict(reference_date='1776-01-01',transfers=TRANSFERS,duplicate_removed=dict(rgb=DUPLICATE,removed_owner='AP7',retained_owner='NET'),population_reassigned=7600,new_population=0,guiana_population_owner_stocks='Retained: both colonial owners and AP7 keep populated portions; no subprovince census justifies reallocating their aggregate cohorts.',reactivated_existing_country='WYU',new_country_definitions=0,new_state_regions=0,bitmap_changed=False,engine_tested=False))
 dump('TECH_EXPECTATIONS.json',{'WYU':dict(required=['traditional_food_processing'],allowed=['traditional_food_processing'],historical_evidence='R9-06/SOURCES.md: autonomous pastoral/fishing communities, no installed industries or military formations. Minimal explicit subsistence knowledge; imported firearms do not establish a European technology tier.')})
 print(json.dumps(dict(files=len(files),province_transfers=len(TRANSFERS),double_assignment_removed=1,population_reassigned=7600,population_added=0)))
def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists();assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==h for r,h in m['input_sha256'].items()),'Shared content changed: re-examine patch';assert all(sha(OUT/'patch'/r)==h for r,h in m['output_sha256'].items())
 for r in m['output_sha256']:(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
def verify():
 m=load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();checks={};old=assigns(text(OUT/'before'/ST));new=assigns(text(ROOT/ST));expected=old.copy()
 for s,r,b,t in TRANSFERS:assert expected[r,s,b]==1;expected[r,s,b]-=1;expected[r,s,t]+=1
 expected[DUPLICATE,'STATE_GUAYANA','AP7']-=1
 checks['installed_manifest_exact']=all(sha(ROOT/r)==h for r,h in m['output_sha256'].items())
 checks['text_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'])
 checks['only_seven_transfers_and_one_duplicate_removal']=+expected==new
 before=C.Counter();after=C.Counter()
 for (r,s,t),v in old.items():before[r]+=v
 for (r,s,t),v in new.items():after[r]+=v
 before[DUPLICATE]-=1;checks['no_unowned_or_new_duplicate_rgb']=before==after
 own=ownership();checks['specific_dual_assignment_resolved']=own[DUPLICATE]=={('STATE_GUAYANA','NET')}
 ns=state_nodes(text(ROOT/ST));oldns=state_nodes(text(OUT/'before'/ST));ps=state_nodes(text(ROOT/PP));oldps=state_nodes(text(OUT/'before'/PP));checks['all_other_state_blocks_identical']=all(normalized([n])==normalized([oldns[s]]) for s,n in ns.items() if s not in ['STATE_ANTIOQUIA','STATE_GUAYANA'])
 checks['all_other_population_blocks_identical']=all(normalized([n])==normalized([oldps[s]]) for s,n in ps.items() if s!='STATE_ANTIOQUIA')
 checks['same_regional_population_culture_religion_and_status']=cohorts(text(ROOT/PP))==cohorts(text(OUT/'before'/PP))
 oldcohort=[z for z in oldps['STATE_ANTIOQUIA'].children('region_state:SC2')[0].children('create_pop') if z.one('culture')=='guajiro'];newcohort=ps['STATE_ANTIOQUIA'].children('region_state:WYU')[0].children('create_pop');checks['one_intact_7600_cohort_reassigned']=normalized(oldcohort)==normalized(newcohort) and len(newcohort)==1 and newcohort[0].one('size')=='7600'
 checks['guiana_population_stocks_by_owner_identical']=normalized([ps['STATE_GUAYANA']])==normalized([oldps['STATE_GUAYANA']])
 checks['no_existing_building_changed_or_added']=all(now.get(r)==h for r,h in base.items() if r.startswith('common/history/buildings/')) and not any(r.startswith('common/history/buildings/') and r not in base for r in now)
 checks['terrain_bitmap_regions_locators_identical']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/')))
 checks['all_existing_country_profiles_definitions_pacts_units_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/countries/','common/country_definitions/','common/history/diplomacy/','common/history/military_formations/')))
 shares={(s,scalar(z.one('country'))[2:]) for s,n in ns.items() for z in n.children('create_state')};checks['population_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s in ['STATE_GUAYANA','STATE_ANTIOQUIA'] for rs in ps[s].children() if rs.children('create_pop'))
 regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))};defs={n.key:n for f in effective('common/country_definitions') for n in parse(text(f))}
 checks['reactivated_wayuu_capital_owned']=('STATE_ANTIOQUIA','WYU') in shares and defs['WYU'].one('capital')=='STATE_ANTIOQUIA' and defs['WYU'].one('country_type')=='decentralized'
 checks['transferred_rgbs_in_correct_region']=all(r in provs(regs[s],'provinces') for s,r,b,t in TRANSFERS)
 checks['riohacha_sinamaica_maracaibo_preserved']=own['x49C3E3']=={('STATE_ANTIOQUIA','SC2')} and own['x9EB190']=={('STATE_ZULIA','SC2')}
 checks['cayenne_paramaribo_georgetown_preserved']=all(own[r]=={('STATE_GUAYANA',t)} for r,t in [('x8C64ED','FRA'),('x50D012','NET'),('x8E31E8','NET')])
 laws={n.key for f in effective('common/laws') for n in parse(text(f))};checks['requested_laws_exist']=all('law_'+k in laws for k in LAWS)
 checks['generic_flag_assets_exist']=all(any((p/f).exists() for p in [ROOT,GAME]) for f in ['gfx/coat_of_arms/patterns/pattern_solid.tga','gfx/coat_of_arms/colored_emblems/ce_bend_dexter.dds'])
 checks['existing_french_english_wayuu_localizations_available']=all(re.search(r'(?m)^\s*WYU:\s*(?:\d+\s*)?"Wayuu"',text(GAME/f'localization/{l}/countries_l_{l}.yml')) for l in ['french','english'])
 # Direct raster witnesses: neither restored colonial place is an isolated post.
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];imp={int(r[1:],16) for n in regs.values() for r in provs(n,'impassable')};blocked=set();import csv
 p=ROOT/'map_data/adjacencies.csv' if (ROOT/'map_data/adjacencies.csv').exists() else GAME/'map_data/adjacencies.csv'
 for row in csv.DictReader(p.open(encoding='utf-8-sig'),delimiter=';'):
  if all(row.get(k,'').startswith('x') for k in ['From','To']) and (row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip()):blocked.add(pair(int(row['From'][1:],16),int(row['To'][1:],16)))
 witnesses={}
 for t,start,end,label in [('NET','x8E31E8','x7B4B5E','Nassau_to_Dutch_coast'),('FRA','x8C64ED','x439BC2','Approuague_to_Cayenne')]:
  colors={int(r[1:],16) for r,v in own.items() if ('STATE_GUAYANA',t) in v}-imp;seed=int(np.flatnonzero(a.ravel()==int(start[1:],16))[0]);parents,_=flood(a,np.isin(a,list(colors)),[seed],blocked);endpixels=np.flatnonzero(a.ravel()==int(end[1:],16));reachable=[int(v) for v in endpixels if int(v) in parents];checks['passable_colonial_land_connection.'+label]=bool(reachable)
  if reachable:witnesses[label]=[[int(v%a.shape[1]),int(v//a.shape[1])] for v in path(parents,reachable[0])]
 dump('LAND_WITNESSES.json',dict(paths=witnesses,engine_market_access_tested=False))
 checks['prior_R9_and_CENTRAL_cores_preserved']=all(own[r]=={(s,t)} for r,s,t in [('x3C0D20','STATE_PASTAZA','BRZ'),('x144683','STATE_ARAUCANIA','H91'),('xF2263F','STATE_LOS_RIOS','PAT'),('x4E1443','STATE_URUGUAY','BRZ'),('xB0243F','STATE_COSTA_RICA','G81'),('xBB820B','STATE_PANAMA','K81'),('x446C64','STATE_WEST_INDIES','C81')])
 external={r:dict(before=base.get(r),after=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change_since_prepare']=not external
 checks={k:bool(v) for k,v in checks.items()};dump('VALIDATION.json',dict(date='2026-10-28',passed=sum(checks.values()),total=len(checks),checks=checks,engine_tested=False,human_validated=False));print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())
def preview():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];new={r:next(iter(v))[1] for r,v in ownership().items() if len(v)==1};oldsets=C.defaultdict(set)
 for r,s,t in assigns(text(OUT/'before'/ST)):oldsets[r].add(t)
 old={r:next(iter(v)) if len(v)==1 else 'DUAL' for r,v in oldsets.items()};colors={'SC2':(182,104,73),'NET':(225,174,72),'FRA':(99,140,203),'AP7':(100,145,100),'WYU':(64,181,168),'DUAL':(190,60,150),'BRZ':(205,183,80)};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
 for name,box,scale in [('GUAJIRA',(2395,1800,2480,1890),4),('GUYANES',(2695,1905,2950,2110),3)]:
  x0,y0,x1,y1=box;crop=a[y0:y1,x0:x1];w=(x1-x0)*scale;h=(y1-y0)*scale;im=Image.new('RGB',(w*2+30,h+125),(34,47,58));d=ImageDraw.Draw(im)
  for i,owners in enumerate([old,new]):
   rgb=np.full((*crop.shape,3),[34,47,58],dtype='uint8')
   for c in np.unique(crop):rgb[crop==c]=colors.get(owners.get(f'x{int(c):06X}'),(34,47,58))
   edge=np.zeros(crop.shape,bool);edge[1:,:]|=crop[1:,:]!=crop[:-1,:];edge[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edge]//=2;im.paste(Image.fromarray(rgb).resize((w,h),Image.Resampling.NEAREST),(10+i*(w+10),40));d.text((10+i*(w+10),8),['Avant','R9-06 installé — 1776'][i],font=font,fill='white')
  d.text((12,h+55),'Turquoise : Wayuu | Vert : AP7 | Bleu : France',font=small,fill='white');d.text((12,h+78),'Or : Pays-Bas | Brun : SC2 | Rose : double attribution',font=small,fill='white');d.text((12,h+101),'Approximation par provinces existantes ; vérification en jeu différée.',font=small,fill='white');im.save(OUT/('R9_06_'+name+'_AVANT_APRES.png'))
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
 elif '--preview' in sys.argv:preview()
