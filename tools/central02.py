"""CENTRAL-02: sourced Indigenous autonomy, conserving existing inhabitants.

No invented land or new State Region. Tiny Saint Vincent split is a coarse
representation of the 1773 treaty; all data are staged and hash guarded.
"""
import collections as C,json,sys,io,re
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,NATIVE_LAWS
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from central01 import owned,cohorts

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/CENTRAL-02'
ST='common/history/states/00_states.txt';PP='common/history/pops/06_central_america.txt';REG='map_data/state_regions/06_central_america.txt';BIT='map_data/provinces.png';PREFIX='1776_central02_autonomies'
GROUPS=[('G81','Guatusos du Río Frío','Rio Frio Guatusos','STATE_COSTA_RICA','central_american',[109,158,100],'decentralized'),('K81','Guna de San Blas','San Blas Guna','STATE_PANAMA','cariban',[81,168,151],'decentralized'),('C81','Caraïbes de Saint-Vincent','Saint Vincent Caribs','STATE_WEST_INDIES','afro_caribbean',[162,137,87],'unrecognized')]
TRANSFERS={'xB0243F':('STATE_COSTA_RICA','SC1','G81'),'xBB820B':('STATE_PANAMA','SC2','K81')}
def dump(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))

def prepare():
 assert not (OUT/'APPLIED.json').exists();OUT.mkdir(parents=True,exist_ok=True);base=runtime();own=owned(text(ROOT/ST))
 defs={n.key for p in effective('common/country_definitions') for n in parse(text(p))};assert not defs&{g[0] for g in GROUPS}
 old_image=Image.open(ROOT/BIT).convert('RGB');arr=np.asarray(old_image,dtype=np.uint32);a=(arr[:,:,0]<<16)|(arr[:,:,1]<<8)|arr[:,:,2];assert not np.any(a==0x446C64)
 yy,xx=np.where(a==0x446C63);allpixels=list(zip(map(int,xx),map(int,yy)))
 # 1773 line reaches further south on the windward/eastern side. Existing
 # resolution is 33 pixels for the entire island: no cadastral precision.
 pixels=[(x,y) for x,y in allpixels if y<=1798 or y==1799 and x>=2701 or y==1800 and x>=2703]
 assert len(allpixels)==33 and len(pixels)==11
 for x,y in pixels:a[y,x]=0x446C64
 new_image=Image.fromarray(np.stack([(a>>16)&255,(a>>8)&255,a&255],axis=2).astype('uint8'));buf=io.BytesIO();new_image.save(buf,format='PNG')
 files={BIT:buf.getvalue()};raw=text(ROOT/ST);nodes=state_nodes(raw);edits=[]
 for r,(s,b,t) in TRANSFERS.items():
  assert own[r]=={(s,b)};n=nodes[s];z=next(z for z in n.children('create_state') if z.one('country')=='c:'+b);v=z.children('owned_provinces')[0];edits.append((v.start,v.end,'owned_provinces = '+rgb_block(set(provs(z,'owned_provinces'))-{r})))
  edits.append((n.end-1,n.end-1,'\n create_state = { country = c:'+t+' owned_provinces = { '+r+' } state_type = incorporated }\n'))
  if not any(z.value=='c:'+b for z in n.children('add_claim')):edits.append((n.end-1,n.end-1,'\n add_claim = c:'+b+'\n'))
 n=nodes['STATE_WEST_INDIES'];edits.append((n.end-1,n.end-1,'\n create_state = { country = c:C81 owned_provinces = { x446C64 } state_type = incorporated }\n'))
 files[ST]=encoded(ROOT/ST,edit(raw,edits))
 raw=text(ROOT/REG);n=next(z for z in parse(raw) if z.key=='STATE_WEST_INDIES');z=n.children('provinces')[0];files[REG]=encoded(ROOT/REG,edit(raw,[(z.start,z.end,'provinces = { '+' '.join('"'+r+'"' for r in provs(n,'provinces')+['x446C64'])+' }')]))
 terrain='map_data/province_terrains.txt';raw=text(ROOT/terrain);assert 'x446C63="plains"' in raw and 'x446C64' not in raw;files[terrain]=encoded(ROOT/terrain,raw+'\nx446C64="plains"\n')
 # Preserve every existing cohort identity. Numbers are redistribution of
 # baseline stock, not added residents or an ethnicity inferred from pixels.
 ledger=[('STATE_COSTA_RICA','SC1','G81','central_american',1000),('STATE_PANAMA','SC2','K81','cariban',2881),('STATE_WEST_INDIES','GBR','C81','afro_caribbean',5000)]
 raw=text(ROOT/PP);nodes=state_nodes(raw);edits=[]
 for sid,b,t,culture,amount in ledger:
  n=nodes[sid];rs=n.children('region_state:'+b)[0];pops=[z for z in rs.children('create_pop') if scalar(z.one('culture'))==culture and not z.one('pop_type')];assert len(pops)==1
  z=pops[0];old=int(z.one('size'));assert old>=amount
  if old==amount:edits.append((z.start,z.end,''))
  else:
   size=z.children('size')[0];edits.append((size.start,size.end,'size = '+str(old-amount)))
  pop=raw[z.start:z.end];size=z.children('size')[0];pop=pop[:size.start-z.start]+'size = '+str(amount)+pop[size.end-z.start:]
  edits.append((n.end-1,n.end-1,'\n region_state:'+t+' = { '+pop+' }\n'))
 files[PP]=encoded(ROOT/PP,edit(raw,edits))
 definitions=[];hist=['COUNTRIES = {'];flags=[];coas=[];loc={l:['l_'+l+':'] for l in ['french','english']}
 for tag,fr,en,capital,culture,color,kind in GROUPS:
  definitions.append(tag+' = { color = { '+' '.join(map(str,color))+' } country_type = '+kind+' tier = principality cultures = { '+culture+' } religion = animist capital = '+capital+' }')
  hist.append('c:'+tag+' ?= { add_technology_researched = traditional_food_processing\n'+''.join('activate_law = law_type:law_'+law+'\n' for law in NATIVE_LAWS)+' }')
  flags.append(tag+' = { flag_definition = { coa = aor1776_central02_'+tag.lower()+' priority = 100 allow_overlord_canton = no } }')
  coas.append('aor1776_central02_'+tag.lower()+' = { pattern = "pattern_solid.tga" color1 = "green" colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 0.8 0.8 } } } }')
  for lang,name in [('french',fr),('english',en)]:loc[lang]+=[f' {tag}:0 "{name}"',f' {tag}_ADJ:0 "{name}"']
 hist.append('}')
 for folder,contents in [('country_definitions',definitions),('history/countries',hist),('flag_definitions',flags),('coat_of_arms/coat_of_arms',coas)]:files['common/'+folder+'/'+PREFIX+'.txt']=('\n'.join(contents)+'\n').encode()
 for lang,lines in loc.items():files['localization/'+lang+'/replace/'+PREFIX+'_l_'+lang+'.yml']=b'\xef\xbb\xbf'+('\n'.join(lines)+'\n').encode()
 dip='common/history/diplomacy/00_subject_relationships.txt';raw=text(ROOT/dip);gb=parse(raw)[0].children('c:GBR')[0];files[dip]=encoded(ROOT/dip,edit(raw,[(gb.end-1,gb.end-1,'\n # CENTRAL-02: 1773 settlement, internal autonomy under British suzerainty.\n create_diplomatic_pact = { country = c:C81 type = protectorate }\n')]))
 # Read the current effective mine locator; the split must not put it on the
 # new Carib token. Reposition only if needed, preserving its old RGB.
 rel='gfx/map/map_object_data/generated_map_object_locators_mine.txt';raw=text(ROOT/rel)
 match=next(m for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s*([-\d.]+)\s*\}',raw) if m[1]=='348')
 oldxy=[float(match[2]),a.shape[0]-float(match[4])];sample=int(a[int(oldxy[1]),int(oldxy[0])]);mine=dict(before=oldxy,after=oldxy,changed=False,sampled_rgb=f'x{sample:06X}')
 if sample!=0x446C63:
  x,y=min([(x,y) for x,y in allpixels if (x,y) not in pixels],key=lambda p:(p[0]-oldxy[0])**2+(p[1]-oldxy[1])**2);replacement=re.sub(r'position\s*=\s*\{[^}]*\}',lambda m:f'position = {{ {x+.1} {match[3]} {a.shape[0]-y-.1} }}',match[0])
  assert replacement!=match[0];files[rel]=encoded(ROOT/rel,raw[:match.start()]+replacement+raw[match.end():]);mine.update(after=[x+.1,y+.1],changed=True,sampled_rgb='x446C63')
 dump('PLAN.json',dict(date='2026-10-27',transfers=TRANSFERS,groups=GROUPS,population_ledger=ledger,new_rgb='x446C64',old_rgb='x446C63',island_pixels=pixels,old_island_pixels=allpixels,mine_locator=mine,new_population=0,new_state_regions=0,talamanca='No installation: no defensible local 1776 cohort allocation; mixed Matina/Talamanca province must be separated using stronger geometry and demographic evidence.',belize_peten_yucatan='Existing major post-1697 colonial cores retained; no later Caste War entity retroprojected. Fine control unresolved.',engine_tested=False))
 p=dict(input_sha256={},output_sha256={})
 for r,data in files.items():
  original=ROOT/r;before=OUT/'before'/r;patch=OUT/'patch'/r;patch.parent.mkdir(parents=True,exist_ok=True);patch.write_bytes(data)
  if original.exists():before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(original.read_bytes())
  p['input_sha256'][r]=sha(original) if original.exists() else None;p['output_sha256'][r]=sha(patch)
 dump('PATCH.json',p);dump('PREPARE_RUNTIME.json',base)
 dump('TECH_EXPECTATIONS.json',{g[0]:dict(required=['traditional_food_processing'],allowed=['traditional_food_processing'],historical_evidence='CENTRAL-02/SOURCES.md: local subsistence communities, no installed industrial buildings or imported European tier.') for g in GROUPS})
 print(json.dumps(dict(runtime_files=len(files),new_population=0,population_redistributed=8881,island_pixels=len(pixels))))

def apply():
 p=load('PATCH.json');assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==v for r,v in p['input_sha256'].items()),'Shared files changed: re-examine patch'
 assert all(sha(OUT/'patch'/r)==h for r,h in p['output_sha256'].items())
 for r in p['output_sha256']:(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))

def verify():
 p=load('PATCH.json');plan=load('PLAN.json');base=load('PREPARE_RUNTIME.json');now=runtime();checks={}
 checks['installed_manifest_exact']=all(now.get(r)==h for r,h in p['output_sha256'].items())
 checks['all_text_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in p['output_sha256'] if r.endswith('.txt'))
 old=owned(text(OUT/'before'/ST));new=owned(text(ROOT/ST));desired={r:{(s,t)} for r,(s,b,t) in TRANSFERS.items()};desired['x446C64']={('STATE_WEST_INDIES','C81')}
 checks['exact_ownership_changes']=all(new[r]==v for r,v in desired.items()) and all(new.get(r)==v for r,v in old.items() if r not in desired) and set(new)-set(old)=={'x446C64'}
 checks['no_new_duplicate_or_unowned_rgb']=all(len(v)==1 or v==old.get(r) for r,v in new.items()) and all(new.get(r) for r in old)
 checks['population_identity_and_region_totals_conserved']=cohorts(text(OUT/'before'/PP))==cohorts(text(ROOT/PP))
 shares={(s,scalar(z.one('country'))[2:]) for s,n in state_nodes(text(ROOT/ST)).items() for z in n.children('create_state')}
 checks['pop_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s,n in state_nodes(text(ROOT/PP)).items() for rs in n.children() if rs.children('create_pop'))
 for sid,b,t,culture,amount in plan['population_ledger']:
  rs=state_nodes(text(ROOT/PP))[sid].children('region_state:'+t)[0];checks['existing_cohort_exact.'+t]=sum(int(z.one('size')) for z in rs.children('create_pop'))==amount
 before=np.asarray(Image.open(OUT/'before'/BIT).convert('RGB'));after=np.asarray(Image.open(ROOT/BIT).convert('RGB'));y,x=np.where(np.any(before!=after,axis=2));checks['only_11_approved_existing_land_pixels_recolored']=set(zip(map(int,x),map(int,y)))==set(map(tuple,plan['island_pixels'])) and all(tuple(before[yy,xx])==(0x44,0x6c,0x63) and tuple(after[yy,xx])==(0x44,0x6c,0x64) for xx,yy in plan['island_pixels'])
 regs={n.key:n for q in effective('map_data/state_regions') for n in parse(text(q))};checks['new_rgb_declared_in_existing_region']='x446C64' in provs(regs['STATE_WEST_INDIES'],'provinces')
 oldreg={n.key:n for n in parse(text(OUT/'before'/REG))};checks['all_regional_capacities_and_hubs_preserved']=all(normalized([z for z in n.children() if z.key!='provinces'])==normalized([z for z in oldreg[s].children() if z.key!='provinces']) for s,n in regs.items() if s in oldreg)
 checks['no_new_state_region']=set(oldreg)=={n.key for n in parse(text(ROOT/REG))}
 defs={n.key:n for q in effective('common/country_definitions') for n in parse(text(q))};checks['new_country_capitals_owned']=all((scalar(defs[g[0]].one('capital')),g[0]) in shares for g in GROUPS)
 checks['all_existing_buildings_and_formations_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/military_formations/')))
 checks['existing_country_profiles_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith('common/history/countries/'))
 checks['central01_corrected_owners_preserved']=all(new[r]=={(s,t)} for r,s,t in [('x600AC6','STATE_HONDURAS','MKT'),('x907080','STATE_HONDURAS','MKT'),('x528F3B','STATE_HONDURAS','MKT'),('x5299CA','STATE_WEST_INDIES','FRA'),('x707080','STATE_WEST_INDIES','SPA')])
 mine=text(ROOT/'gfx/map/map_object_data/generated_map_object_locators_mine.txt');v=next(m for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s*([-\d.]+)\s*\}',mine) if m[1]=='348')
 checks['british_mine_locator_stays_on_retained_british_land']=tuple(after[int(after.shape[0]-float(v[4])),int(float(v[2]))])==(0x44,0x6c,0x63)
 dip=[z for z in walk(parse(text(ROOT/'common/history/diplomacy/00_subject_relationships.txt'))) if z.key=='create_diplomatic_pact' and z.one('country')=='c:C81'];checks['carib_internal_autonomy_under_british_suzerainty']=len(dip)==1 and dip[0].one('type')=='protectorate'
 external={r:dict(before_sha256=base.get(r),observed_sha256=now.get(r)) for r in base.keys()|now.keys() if r not in p['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external)
 checks['no_unlisted_runtime_change']=not external
 checks['no_new_country_without_localization']=all(re.search(r'^ '+g[0]+r':0 ',text(ROOT/f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml'),re.M) for g in GROUPS for lang in ['french','english'])
 dump('VALIDATION.json',dict(date='2026-10-27',checks=checks,passed=sum(checks.values()),total=len(checks),all_pass=all(checks.values()),engine_tested=False))
 print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v],external_files=list(external))))
 assert all(checks.values())

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
