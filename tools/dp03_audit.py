"""Independent checks of staged/current DP-03. Static checks do not certify the engine."""
from dp03_refine import *
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from hbc02_map_candidates import graph

def audit(staged=False):
 m=load('PREPARED.json');plan=load('PLAN.json');checks={};files={z['file'] for z in m['files']}
 manifest=load('CURRENT_RUNTIME_MANIFEST.json')['files'] if not staged and (OUT/'CURRENT_RUNTIME_MANIFEST.json').exists() else m['files']
 def path(rel):return OUT/'staged'/rel if staged and rel in files else ROOT/rel
 def raw(rel):return text(path(rel))
 def check(k,v):checks[k]=bool(v)
 def outside(s,scope=SCOPE):return [(n.key,normalized([q for q in n.children() if q.key not in ['s:'+s for s in scope]])) for n in parse(s)]
 ow=C.defaultdict(set);counts=C.Counter()
 for p in effective('common/history/states'):
  s=raw(p.relative_to(ROOT).as_posix()) if p.is_relative_to(ROOT) else text(p)
  for sid,n in state_nodes(s).items():
   for c in n.children('create_state'):
    for r in provs(c,'owned_provinces'):
     r='x'+r[1:].upper();ow[r].add((sid,scalar(c.one('country'))[2:]));counts[r]+=1
 old={r:set(map(tuple,v)) for r,v in m['ownership_before'].items()}
 changes={r for r in set(old)|set(ow) if old.get(r)!=ow.get(r)}
 check('exact_six_owner_changes',changes=={z['rgb'] for z in plan['transfers']})
 check('planned_owners',all(ow[z['rgb']]=={(z['state'],z['after'])} for z in plan['transfers']))
 check('outside_scope_state_AST_unchanged',outside(text(OUT/'preimages'/ST))==outside(raw(ST)))
 regions={n.key:n for p in effective('map_data/state_regions') for n in parse(raw(p.relative_to(ROOT).as_posix()) if p.is_relative_to(ROOT) else text(p))}
 cells={r for s in SCOPE for r in provs(regions[s],'provinces')}
 check('scope_unique_complete_ownership',all(counts[r]==1 and len(ow[r])==1 for r in cells))
 check('correct_state_and_passable',all(z['rgb'] in provs(regions[z['state']],'provinces') and z['rgb'] not in provs(regions[z['state']],'impassable') for z in plan['transfers']))
 check('cohort_fields_and_total_conserved',popstock(text(OUT/'preimages'/POP))==popstock(raw(POP)))
 check('other_population_states_unchanged',outside(text(OUT/'preimages'/POP),['STATE_KASHMIR'])==outside(raw(POP),['STATE_KASHMIR']))
 check('military_region_type_service_counts_conserved',stock_units(text(OUT/'preimages'/MIL))==stock_units(raw(MIL))+stock_units(raw(UNIT)))
 for z in manifest:
  check('hash_'+z['file'],sha(path(z['file']))==z['after_sha256'])
  if z['file'].endswith('.txt'):parse(raw(z['file']))
 check('all_building_files_preserved',all(sha(ROOT/p)==h for p,h in m['world_before'].items() if p.startswith('common/history/buildings/')))
 check('bitmap_unchanged',sha(ROOT/'map_data/provinces.png')==m['world_before']['map_data/provinces.png'])
 check('other_state_region_files_preserved',all(sha(ROOT/p)==h for p,h in m['world_before'].items() if p.startswith('map_data/state_regions/') and p!=REG))
 a=text(OUT/'preimages'/REG);b=raw(REG);patch=[]
 n=next(n for n in parse(a) if n.key=='STATE_KASHMIR')
 for k,v in LOC.items():
  z=n.children(k)[0];patch.append((z.start,z.end,k+' = "'+v['rgb']+'"'))
 check('region_only_two_hub_pointers_changed',edit(a,patch)==b)
 bitmap=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),np.uint32)
 packed=(bitmap[:,:,0]<<16)|(bitmap[:,:,1]<<8)|bitmap[:,:,2]
 riverpath=ROOT/'map_data/rivers.png'
 if not riverpath.exists():riverpath=GAME/'map_data/rivers.png'
 rivers=np.asarray(Image.open(riverpath))
 for kind,v in LOC.items():
  rel='gfx/map/map_object_data/generated_map_object_locators_'+kind+'.txt'
  a=text(OUT/'preimages'/rel);n=next(n for n in walk(parse(a)) if n.children('id') and n.one('id')=='463' and n.children('position'));z=n.children('position')[0]
  expected=edit(a,[(z.start,z.end,'position={ '+' '.join(f'{x:.6f}' for x in v['point'])+' }')])
  check('only_id463_position_changed_'+kind,expected==raw(rel))
  x,_,z=v['point'];y=packed.shape[0]-z
  check('hub_matches_land_pixel_'+kind,f'x{int(packed[int(y),int(x)]):06X}'==v['rgb'] and rivers[int(y),int(x)] in [254,255])
  check('hub_owned_'+kind,ow[v['rgb']]=={('STATE_KASHMIR','DUR' if kind=='city' else 'LAD')})
 # Prior installations protected, except three explicitly named supersessions.
 for prior in ['DP-01','DP-02']:
  p=OUT.parent/prior/'PLAN.json';overrides={z['rgb']:z for z in plan['transfers']}
  previous=json.loads(p.read_text(encoding='utf8'))['transfers']
  check('protected_'+prior,all(ow[z['rgb']]=={(z['state'],overrides.get(z['rgb'],z)['after'])} for z in previous))
 affected=list(NEW)+['D2K','D2C','D2U','D2B','GAR','LAD','D2J','D2M','D2S','BHW','MAK','KHR','LBL','KAL','PTA']
 continuity={}
 for t in affected:
  ids={int(r[1:],16) for r,vs in ow.items() if any(tag==t for sid,tag in vs)}
  adj=graph(packed,np.array(sorted(ids),np.uint32));seen={next(iter(ids))};queue=list(seen)
  while queue:
   for v,num in adj[queue.pop()].items():
    if num>=2 and v in ids and v not in seen:seen.add(v);queue.append(v)
  continuity[t]=dict(cells=len(ids),connected=len(seen));check('land_continuity_'+t,ids==seen)
 # Check all POP/building references in the two State_IDs, including other history files.
 for folder in ['pops','buildings']:
  bad=[]
  for p in effective('common/history/'+folder):
   s=raw(p.relative_to(ROOT).as_posix()) if p.is_relative_to(ROOT) else text(p)
   for sid,n in state_nodes(s).items():
    if sid not in SCOPE:continue
    for q in n.children():
     if q.key.startswith('region_state:') and not any((sid,q.key.split(':',1)[1]) in v for v in ow.values()):bad.append((str(p),sid,q.key))
  check('valid_'+folder+'_owners',not bad)
 definitions=parse(raw('common/country_definitions/1776_dp03.txt'))
 pops=state_nodes(raw(POP))['STATE_KASHMIR'];population={}
 for t in NEW:
  d=next(n for n in definitions if n.key==t)
  check('capital_owned_'+t,any((scalar(d.one('capital')),t) in v for v in ow.values()))
  ps=pops.children('region_state:'+t);population[t]=sum(int(q.one('size')) for n in ps for q in n.children('create_pop'));check('population_present_'+t,population[t]>0)
  chars=parse(raw('common/history/characters/1776_dp03_'+t.lower()+'.txt'))
  rulers=[n for n in walk(chars) if n.key=='create_character' and n.one('ruler')=='yes']
  check('one_historical_ruler_'+t,len(rulers)==1 and rulers[0].one('historical')=='yes')
  if not staged:
   country=next(n for n in walk(parse(raw('common/history/countries/1776_dp03_'+t.lower()+'.txt'))) if n.key=='c:'+t)
   check('dynastic_religion_consistent_'+t,scalar(d.one('religion'))==NEW[t]['religion'] and scalar(rulers[0].one('religion'))=='rel:'+NEW[t]['religion'] and scalar(country.one('set_state_religion'))=='rel:'+NEW[t]['religion'])
 laws=parse(raw('common/laws/1776_dp03.txt'))
 check('new_laws_restricted_to_new_countries',all(set(re.findall(r'c:([A-Z0-9]+)',raw('common/laws/1776_dp03.txt')[q.start:q.end]))==set(NEW) for n in laws for k in ['is_visible','can_enact'] for q in n.children(k)))
 coa={n.key for n in parse(raw('common/coat_of_arms/coat_of_arms/1776_dp03.txt'))}
 flags=parse(raw('common/flag_definitions/1776_dp03.txt'))
 check('new_flags_resolve',all(scalar(n.one('coa')) in coa for n in walk(flags) if n.key=='flag_definition'))
 pattern=ROOT/'gfx/coat_of_arms/patterns/pattern_solid.tga'
 check('native_flag_pattern_exists',pattern.exists() or (GAME/'gfx/coat_of_arms/patterns/pattern_solid.tga').exists())
 for lang in ['french','english']:
  rel='localization/'+lang+'/replace/1776_dp03_l_'+lang+'.yml';s=raw(rel);keys=re.findall(r'^\s*([^ :]+):0\s+"',s,re.M);count=C.Counter(keys)
  for p in (ROOT/'localization'/lang).rglob('*.yml'):
   if p.relative_to(ROOT).as_posix()==rel:continue
   count.update(k for k in re.findall(r'^\s*([^ :]+):(?:\d+)?\s+"',text(p),re.M) if k in keys)
  check('localization_BOM_'+lang,path(rel).read_bytes().startswith(b'\xef\xbb\xbf'))
  check('unique_localization_'+lang,all(count[k]==1 for k in keys))
  needed=list(NEW)+[t+'_ADJ' for t in NEW]+['aor1776_dp03_levy','aor1776_dp03_empty']+['aor1776_dp03_ruler_'+t.lower() for t in NEW]+['law_aor1776_dp03_'+v+s for v in ['customs','customary_bondage','toleration'] for s in ['', '_desc']]
  check('localization_complete_'+lang,all(k in keys for k in needed))
 if not staged:
  rows=tech('TECH_AFTER.json',list(NEW)+['DUR','PAN','LAD','D2K','D2C','D2U','D2B','GAR'])
  check('new_profiles_pass',all(r['status']=='PASS_STATIC_ONLY' for r in rows if r['TAG'] in NEW))
  before={r['TAG']:r for r in load('TECH_BEFORE.json')};deltas=[]
  for r in rows:
   if r['TAG'] not in before:continue
   oldfind={json.dumps(z,sort_keys=True) for z in before[r['TAG']]['findings']}
   delta=[z for z in r['findings'] if json.dumps(z,sort_keys=True) not in oldfind];deltas.append(dict(tag=r['TAG'],new_findings=delta))
  check('existing_profiles_no_new_findings',all(not d['new_findings'] for d in deltas))
  current=runtime();unrelated={p:dict(before=m['world_before'].get(p),after=current.get(p)) for p in set(m['world_before'])|set(current) if m['world_before'].get(p)!=current.get(p) and p not in files}
 else:deltas=[];unrelated={}
 # Readable diagnostic from actual installed cells; never labelled as an engine screenshot.
 box=(5740,1220,5940,1420);x0,y0,x1,y1=box;crop=packed[y0:y1,x0:x1];u,ix=np.unique(crop,return_inverse=True)
 palette={'DUR':(83,151,161),'LAD':(68,172,193),'D3G':(137,169,105),'D3S':(151,117,171),'GAR':(70,145,112),'PAN':(227,145,58)}
 from dp02_refine import NEW as HILLS
 palette.update({t:v[-1] for t,v in HILLS.items()})
 colors=[palette.get(next(iter(ow.get(f'x{int(c):06X}',{('','?')})))[1],(72,76,80)) for c in u]
 arr=np.array(colors,np.uint8)[ix].reshape((*crop.shape,3));bd=np.zeros(crop.shape,bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];arr[bd]//=2
 im=Image.new('RGB',(1000,1120),(28,40,50));im.paste(Image.fromarray(arr).resize((1000,1000),Image.Resampling.NEAREST),(0,55));draw=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
 draw.text((12,12),'DP-03 — administrations installées, cellules natives (diagnostic hors jeu)',fill='white',font=font)
 labels=[('Gilgit',5786,1248),('Skardu',5817,1264),('Leh',5863,1293),('Kargil',5829,1284),('Srinagar',5800,1296),('Jammu',5800,1331),('Chamba',5830,1335),('Kangra',5833,1346),('Kullu',5853,1350),('Mandi',5849,1356),('Rampur',5865,1363),('Nahan',5858,1385)]
 for name,x,y in labels:
  px,py=(x-x0)*5,(y-y0)*5+55;draw.ellipse((px-3,py-3,px+3,py+3),fill='white');draw.text((px+5,py-12),name,font=font,fill='white',stroke_width=2,stroke_fill=(20,25,30))
 draw.text((12,1070),'Six réattributions. Petites juridictions partagées et démographie : réserves V2.',font=font,fill='white')
 draw.text((12,1094),'Srinagar/Kargil repositionnés ; chargement et rendu Victoria 3 non validés.',font=font,fill='white')
 im.save(OUT/('STAGED_MAP.png' if staged else 'INSTALLED_MAP.png'))
 result=dict(status='PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL_STATIC',staged=staged,checks=checks,transfers=len(changes),scope_provinces=len(cells),population_new=population,continuity=continuity,technology_delta=deltas,unrelated_runtime_deltas=unrelated,runtime_validated=False)
 name='PREFLIGHT.json' if staged else 'VALIDATION.json'
 if (OUT/name).exists():
  q=OUT/'audit_history'/(sha(OUT/name)[:16]+'.json');q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():q.write_bytes((OUT/name).read_bytes())
 dump(name,result)
 print(json.dumps(dict(status=result['status'],checks=len(checks),failed=[k for k,v in checks.items() if not v],unrelated=len(unrelated),technology_delta=[d for d in deltas if d['new_findings']]),ensure_ascii=False))
 return all(checks.values())

if __name__=='__main__':sys.exit(0 if audit('--staged' in sys.argv) else 1)
