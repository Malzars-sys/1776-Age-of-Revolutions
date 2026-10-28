"""First authorized R9 correction: Iquicha anachronism and La Paz Andean core.

Research baselines are retained. No blanket award of the Amazonian foothills,
new population, bitmap change, or imported colonial technology package.
"""
import collections as C,json,sys,re,csv
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from central01 import owned,cohorts
from hbc02_map_candidates import graph
from hbc04_land_links import pair
from georeference.model import fit,evaluate,forward,inverse

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-01'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt';BB='common/history/buildings/07_south_america.txt';REG='map_data/state_regions/07_south_america.txt'
def dump(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def raster():
 b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);return (b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]

def survey():
 assert not (OUT/'APPLIED.json').exists(),'Do not overwrite the delivered geometry survey.'
 a=raster();regs={n.key:n for n in parse(text(ROOT/REG))};loc={};raw=text(ROOT/'gfx/map/map_object_data/generated_map_object_locators_city.txt')
 for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s*([-\d.]+)\s*\}',raw):loc[int(m[1])]=[float(m[2]),a.shape[0]-float(m[4])]
 anchors=[('Lima','STATE_LIMA',[-77.04,-12.05]),('Cusco','STATE_ICA',[-71.967,-13.531]),('Arequipa','STATE_AREQUIPA',[-71.537,-16.399]),('Cajamarca','STATE_CAJAMARCA',[-78.512,-7.164]),('La Paz','STATE_LA_PAZ',[-68.119,-16.49]),('Potosi','STATE_POTOSI',[-65.753,-19.573]),('Santa Cruz','STATE_SANTA_CRUZ',[-63.183,-17.783])]
 controls=[]
 for name,sid,geo in anchors:
  n=regs[sid];p=loc[int(n.one('id'))];rgb=f'x{int(a[int(p[1]),int(p[0])]):06X}'
  controls.append(dict(name=name,state=sid,geo=geo,pixel=p,rgb=rgb,declared_rgb=scalar(n.one('city')),role='CHECK' if name in ['Cusco','La Paz'] else 'FIT'))
 model=fit(controls,'miller_affine',a.shape[::-1]);dump('GEODETIC_CONTROLS.json',controls);dump('GEODETIC_MODEL.json',model);dump('GEODETIC_EVALUATION.json',evaluate(model))
 selected={int(r[1:],16):(s,r) for s in ['STATE_ICA','STATE_LA_PAZ'] for r in provs(regs[s],'provinces')};rows=[];own=owned(text(ROOT/ST))
 # One scan over all unique colours; no province-area population inference.
 ids,idx,count=np.unique(a,return_inverse=True,return_counts=True);yy,xx=np.indices(a.shape);sx=np.bincount(idx.ravel(),weights=xx.ravel());sy=np.bincount(idx.ravel(),weights=yy.ravel())
 for i,c in enumerate(ids):
  if int(c) not in selected:continue
  s,r=selected[int(c)];pixel=[float(sx[i]/count[i]),float(sy[i]/count[i])];rows.append(dict(state=s,rgb=r,pixel=pixel,geo=inverse(model,[pixel])[0].tolist(),pixels=int(count[i]),owners=sorted(own[r])))
 dump('PROVINCES.json',rows)
 print(json.dumps({k:v for k,v in evaluate(model).items() if k in ['fit','check']}))

def prepare():
 assert not (OUT/'APPLIED.json').exists();own=owned(text(ROOT/ST));rows=load('PROVINCES.json');base=runtime();regs={n.key:n for n in parse(text(ROOT/REG))}
 ica={r for r,v in own.items() if ('STATE_ICA','IQU') in v};assert len(ica)==17 and all(len(own[r])==1 for r in ica)
 assert not any(t=='IQU' and s!='STATE_ICA' for v in own.values() for s,t in v)
 # Only the documented colonial city and its minimal mainland connection.
 # Do not invent a historical provincial boundary from a latitude threshold.
 city=scalar(regs['STATE_LA_PAZ'].one('city'));lapaz={city}
 # Require all selected provinces to connect by real land edges to Peru's
 # current core; no disconnected colonial post or invented bridge.
 a=raster();span={int(r[1:],16) for r,v in own.items() if any(t=='SC3' for s,t in v)};candidate={int(r[1:],16) for r in lapaz|ica}
 imp={int(r[1:],16) for path in effective('map_data/state_regions') for n in parse(text(path)) for r in provs(n,'impassable')};blocked=set();ap=ROOT/'map_data/adjacencies.csv';ap=ap if ap.exists() else GAME/'map_data/adjacencies.csv'
 for z in csv.DictReader(ap.open(encoding='utf-8-sig'),delimiter=';'):
  if all(z.get(k,'').startswith('x') for k in ['From','To']) and (z.get('Type') in ['sea','impassable'] or z.get('adjacency_rule_name','').strip()):blocked.add(pair(int(z['From'][1:],16),int(z['To'][1:],16)))
 assert not candidate&imp
 allowed=span|{int(r[1:],16) for r in provs(regs['STATE_LA_PAZ'],'provinces')}|{int(r[1:],16) for r in ica};adj=graph(a,np.array(sorted(allowed-imp),dtype=np.uint32))
 start=int(city[1:],16);previous={start:None};q=C.deque([start]);end=None;goals=span|{int(r[1:],16) for r in ica}
 while q:
  u=q.popleft()
  if u in goals:end=u;break
  for v in sorted(adj.get(u,{})):
   if v not in previous and pair(u,v) not in blocked:previous[v]=u;q.append(v)
 assert end is not None
 route=[]
 while end is not None:route.append(end);end=previous[end]
 lapaz={f'x{v:06X}' for v in route if f'x{v:06X}' not in ica and v not in span};candidate={int(r[1:],16) for r in lapaz|ica}
 adj={u:{v:c for v,c in vs.items() if v in span|candidate} for u,vs in adj.items() if u in span|candidate}
 seed=int(scalar(regs['STATE_LIMA'].one('city'))[1:],16);assert seed in span;seen={seed};q=C.deque([seed])
 while q:
  u=q.popleft()
  for v in adj.get(u,{}):
   if v not in seen and pair(u,v) not in blocked:seen.add(v);q.append(v)
 assert candidate<=seen,'New colonial cells must all connect to the inherited mainland'
 dump('LAND_CONTINUITY.json',dict(capital_seed=f'x{seed:06X}',new_provinces_reached=sorted(f'x{v:06X}' for v in candidate&seen),new_provinces_total=len(candidate),explicit_blocked_adjacencies_respected=True,impassable_provinces_excluded=True))
 assert len(lapaz)<89 and all(own[r]=={('STATE_LA_PAZ','AP7')} for r in lapaz)
 files={};raw=text(ROOT/ST);n=state_nodes(raw);edits=[]
 for sid,prior,cells in [('STATE_ICA','IQU',ica),('STATE_LA_PAZ','AP7',lapaz)]:
  node=n[sid];z=next(v for v in node.children('create_state') if v.one('country')=='c:'+prior)
  if cells==set(provs(z,'owned_provinces')):edits.append((z.start,z.end,''))
  else:
   v=z.children('owned_provinces')[0];edits.append((v.start,v.end,'owned_provinces = '+rgb_block(set(provs(z,'owned_provinces'))-cells)))
  targets=[v for v in node.children('create_state') if v.one('country')=='c:SC3']
  if targets:
   z=targets[0];v=z.children('owned_provinces')[0];edits.append((v.start,v.end,'owned_provinces = '+rgb_block(set(provs(z,'owned_provinces'))|cells)))
  else:edits.append((node.end-1,node.end-1,'\n create_state = { country = c:SC3 owned_provinces = '+rgb_block(cells)+' state_type = incorporated }\n'))
 files[ST]=encoded(ROOT/ST,edit(raw,edits))
 raw=text(ROOT/PP);n=state_nodes(raw);edits=[]
 # Entire Iquicha portion joins the existing colonial administration. In La
 # Paz, move only the inherited Hispanic-Andean cohort with the city core.
 # The other cohorts retain their original owner pending finer local mapping.
 z=n['STATE_ICA'].children('region_state:IQU')[0];edits.append((z.start,z.start+len(z.key),'region_state:SC3'))
 node=n['STATE_LA_PAZ'];rs=node.children('region_state:AP7')[0];moved=[z for z in rs.children('create_pop') if scalar(z.one('culture'))=='south_andean'];assert len(moved)==1
 chunks=[]
 for z in moved:chunks.append(raw[z.start:z.end]);edits.append((z.start,z.end,''))
 edits.append((node.end-1,node.end-1,'\n region_state:SC3 = {\n'+'\n'.join(chunks)+'\n}\n'));files[PP]=encoded(ROOT/PP,edit(raw,edits))
 raw=text(ROOT/BB);node=state_nodes(raw)['STATE_ICA'];src=node.children('region_state:IQU')[0];dest=node.children('region_state:SC3')[0]
 sb=[z for z in src.children('create_building') if scalar(z.one('building'))=='building_barrack'];db=[z for z in dest.children('create_building') if scalar(z.one('building'))=='building_barrack'];assert len(sb)==len(db)==1 and len(src.children())==1
 levels=[v for z in sb+db for cap in z.children('add_ownership') for cc in cap.children() for v in cc.children() if v.key=='levels'];assert sum(int(v.value) for v in levels)==4
 level=next(v for cap in db[0].children('add_ownership') for cc in cap.children() for v in cc.children() if v.key=='levels');files[BB]=encoded(ROOT/BB,edit(raw,[(level.start,level.end,'levels = 4'),(src.start,src.end,'')]))
 dip='common/history/diplomacy/00_subject_relationships.txt';raw=text(ROOT/dip);z=[z for z in walk(parse(raw)) if z.key=='create_diplomatic_pact' and z.one('country')=='c:IQU'];assert len(z)==1;files[dip]=encoded(ROOT/dip,edit(raw,[(z[0].start,z[0].end,'# R9-01: Iquicha is not a separate colony in January 1776.')]))
 p=dict(input_sha256={},output_sha256={})
 for r,data in files.items():
  old=OUT/'before'/r;patch=OUT/'patch'/r;old.parent.mkdir(parents=True,exist_ok=True);patch.parent.mkdir(parents=True,exist_ok=True);old.write_bytes((ROOT/r).read_bytes());patch.write_bytes(data);p['input_sha256'][r]=sha(ROOT/r);p['output_sha256'][r]=sha(patch)
 dump('PATCH.json',p);dump('PREPARE_RUNTIME.json',base);dump('PLAN.json',dict(date='2026-10-27',ica=sorted(ica),la_paz=sorted(lapaz),new_owner='SC3',la_paz_population_moved=sum(int(z.one('size')) for z in moved),la_paz_population_retained=458067,population_added=0,bitmap_changed=False,claim_changes=0,all_south_america_complete=False,engine_tested=False))
 print(json.dumps(dict(ica_provinces=len(ica),la_paz_provinces=len(lapaz),la_paz_population_moved=sum(int(z.one('size')) for z in moved),files=len(files))))

def apply():
 m=load('PATCH.json');assert all(sha(ROOT/r)==h for r,h in m['input_sha256'].items())
 for r,h in m['output_sha256'].items():assert sha(OUT/'patch'/r)==h
 for r in m['output_sha256']:(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))

def verify():
 m=load('PATCH.json');p=load('PLAN.json');base=load('PREPARE_RUNTIME.json');now=runtime();checks={}
 old=owned(text(OUT/'before'/ST));new=owned(text(ROOT/ST));changed=set(p['ica']+p['la_paz']);expected={r:{('STATE_ICA' if r in p['ica'] else 'STATE_LA_PAZ','SC3')} for r in changed}
 checks['installed_hashes']=all(now.get(r)==h for r,h in m['output_sha256'].items());checks['modified_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'])
 checks['exact_transfers_only']=all(new[r]==v for r,v in expected.items()) and all(new.get(r)==v for r,v in old.items() if r not in changed) and set(new)==set(old)
 checks['no_new_duplicate_or_unowned_rgb']=all(len(v)==1 or v==old.get(r) for r,v in new.items()) and all(new.get(r) for r in old)
 checks['regional_population_and_identities_conserved']=cohorts(text(OUT/'before'/PP))==cohorts(text(ROOT/PP))
 ns=state_nodes(text(ROOT/PP));ap=ns['STATE_LA_PAZ'].children('region_state:AP7')[0];checks['other_la_paz_cohorts_retained_without_conversion']=sum(int(z.one('size')) for z in ap.children('create_pop'))==458067 and any(z.one('culture')=='amazonian' and int(z.one('size'))==33841 for z in ap.children('create_pop'))
 checks['iquicha_no_initial_territory']=not any(t=='IQU' for v in new.values() for s,t in v)
 checks['no_orphan_iquicha_economic_owner']='c:IQU' not in text(ROOT/BB) and 'region_state:IQU' not in text(ROOT/BB)
 def assets(raw):return C.Counter(json.dumps(normalized([z]),sort_keys=True) for z in walk(parse(raw)) if z.key=='create_building')
 def other_assets(raw):
  return C.Counter(json.dumps(normalized([z]),sort_keys=True) for sid,n in state_nodes(raw).items() for rs in n.children() for z in rs.children('create_building') if not (sid=='STATE_ICA' and scalar(z.one('building'))=='building_barrack'))
 checks['other_building_commands_preserved']=other_assets(text(OUT/'before'/BB).replace('c:IQU','c:SC3'))==other_assets(text(ROOT/BB))
 def barracks(raw):
  result=[]
  for rs in state_nodes(raw)['STATE_ICA'].children():
   for z in rs.children('create_building'):
    if scalar(z.one('building'))!='building_barrack':continue
    levels=sum(int(v.value) for cap in z.children('add_ownership') for cc in cap.children() for v in cc.children() if v.key=='levels');result.append((levels,provs(z,'activate_production_methods'),z.one('reserves')))
  return result
 b0=barracks(text(OUT/'before'/BB));b1=barracks(text(ROOT/BB));checks['ica_barrack_four_levels_same_PM_and_reserves']=sum(v[0] for v in b0)==sum(v[0] for v in b1)==4 and len(b1)==1 and all(v[1]==b1[0][1] and v[2]==b1[0][2] for v in b0)
 shares={(s,scalar(z.one('country'))[2:]) for s,n in state_nodes(text(ROOT/ST)).items() for z in n.children('create_state')}
 checks['pop_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s,n in ns.items() for rs in n.children() if rs.children('create_pop'))
 checks['no_bitmap_regions_hubs_or_profiles_changed']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/map_object_data/','common/history/countries/','common/history/military_formations/')))
 checks['central02_territories_preserved']=all(new[r]=={v} for r,v in {'xB0243F':('STATE_COSTA_RICA','G81'),'xBB820B':('STATE_PANAMA','K81'),'x446C64':('STATE_WEST_INDIES','C81')}.items())
 land=load('LAND_CONTINUITY.json');checks['new_territories_have_proved_lima_land_connection']=set(land['new_provinces_reached'])==changed and land['new_provinces_total']==len(changed) and land['explicit_blocked_adjacencies_respected'] and land['impassable_provinces_excluded']
 checks['other_pacts_preserved']=normalized([z for z in walk(parse(text(OUT/'before'/'common/history/diplomacy/00_subject_relationships.txt'))) if z.key=='create_diplomatic_pact' and z.one('country')!='c:IQU'])==normalized([z for z in walk(parse(text(ROOT/'common/history/diplomacy/00_subject_relationships.txt'))) if z.key=='create_diplomatic_pact'])
 external={r:dict(before_sha256=base.get(r),observed_sha256=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change']=not external
 dump('VALIDATION.json',dict(date='2026-10-27',checks=checks,passed=sum(checks.values()),total=len(checks),all_pass=all(checks.values()),engine_tested=False))
 print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())

if __name__=='__main__':
 if '--survey' in sys.argv:survey()
 elif '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
