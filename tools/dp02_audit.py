"""Current DP-02 checks. Static evidence only, never an engine-validation receipt."""
from dp02_refine import *
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from hbc02_map_candidates import graph

def outside(raw):
 return [(r.key,normalized([n for n in r.children() if n.key not in ['s:'+s for s in SCOPE]])) for r in parse(raw)]

def audit():
 m=load('PREPARED.json');ap=load('CURRENT_RUNTIME_MANIFEST.json') if (OUT/'CURRENT_RUNTIME_MANIFEST.json').exists() else load('APPLIED.json');plan=load('PLAN.json');ow=normalized_owners();old={r:set(map(tuple,v)) for r,v in m['ownership_before'].items()};checks={}
 def check(k,v):checks[k]=bool(v)
 all_changes={r for r in set(old)|set(ow) if old.get(r)!=ow.get(r)}
 changes={r for r in all_changes if any(s in SCOPE for s,t in old.get(r,set())|ow.get(r,set()))}
 external=all_changes-changes
 if (OUT/'CONCURRENT_REVIEW_01.json').exists():
  refown=C.defaultdict(set)
  for sid,s in state_nodes(text(OUT/'concurrent_postimages'/ST)).items():
   for cs in s.children('create_state'):
    for r in provs(cs,'owned_provinces'):refown['x'+r[1:].upper()].add((sid,scalar(cs.one('country'))[2:]))
  allowed={r for r,v in refown.items() if v!=old.get(r,set()) and not any(s in SCOPE for s,t in v|old.get(r,set()))}
  check('external_owner_changes_exactly_reviewed',external==allowed and all(ow[r]==refown[r] for r in external))
 else:check('no_external_owner_changes',not external)
 check('exact_planned_transfers',changes=={z['rgb'] for z in plan['transfers']})
 check('planned_owners',all(ow.get(z['rgb'])=={(z['state'],z['after'])} for z in plan['transfers']))
 regions={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};scope={r for s in SCOPE for r in provs(regions[s],'provinces')}
 counts=C.Counter()
 for p in effective('common/history/states'):
  for sid,s in state_nodes(text(p)).items():
   for q in s.children('create_state'):
    for r in provs(q,'owned_provinces'):counts['x'+r[1:].upper()]+=1
 check('scope_exactly_one_owner',all(counts[r]==1 and len(ow.get(r,set()))==1 for r in scope))
 check('transfers_in_correct_regions',all(z['rgb'] in provs(regions[z['state']],'provinces') for z in plan['transfers']))
 check('no_impassable_transfer',all(z['rgb'] not in provs(regions[z['state']],'impassable') for z in plan['transfers']))
 check('no_Durrani_direct_Hill_Punjab',not any(('STATE_HILL_PUNJAB','DUR') in v for v in ow.values()))
 poprows=[]
 for rel in POPS:
  a=text(OUT/'preimages'/rel);b=text(ROOT/rel);check('cohort_stock_'+rel,popstock(a)==popstock(b));check('outside_scope_'+rel,outside(a)==outside(b));poprows.append(dict(file=rel,before=sum(popstock(a).values()),after=sum(popstock(b).values())))
 for rel in BUILD:
  p=OUT/'preimages'/rel
  if p.exists():check('building_stock_'+rel,buildingstock(text(p))==buildingstock(text(ROOT/rel)));check('outside_scope_'+rel,outside(text(p))==outside(text(ROOT/rel)))
 concurrent=OUT/'CONCURRENT_REVIEW_01.json'
 if concurrent.exists():
  receipt=load('CONCURRENT_REVIEW_01.json');ref=OUT/'concurrent_postimages'/ST
  check('concurrent_reference_hash',sha(ref)==receipt['after_sha256'])
  check('outside_scope_states',outside(text(ref))==outside(text(ROOT/ST)))
  staged=state_nodes(text(OUT/'staged'/ST));now=state_nodes(text(ROOT/ST))
  check('our_states_match_tested_installation',all(normalized([staged[s]])==normalized([now[s]]) for s in SCOPE))
 else:check('outside_scope_states',outside(text(OUT/'preimages'/ST))==outside(text(ROOT/ST)))
 check('military_counts_types_services_regions_conserved',stock_units(text(OUT/'preimages'/MIL))==stock_units(text(ROOT/MIL))+stock_units(text(ROOT/'common/history/military_formations/1776_dp02.txt')))
 for z in ap['files']:
  check('hash_'+z['file'],sha(ROOT/z['file'])==z['after_sha256'])
  if z['file'].endswith('.txt'):parse(text(ROOT/z['file']))
 check('bitmap_preserved',sha(ROOT/'map_data/provinces.png')==m['world_before']['map_data/provinces.png'])
 check('all_state_region_files_preserved',all(sha(ROOT/p)==h for p,h in m['world_before'].items() if p.startswith('map_data/state_regions/')))
 # Current ownership must support every population, building and military reference in touched regions.
 for folder in ['pops','buildings']:
  bad=[]
  for p in effective('common/history/'+folder):
   for sid,s in state_nodes(text(p)).items():
    if sid not in SCOPE:continue
    for n in s.children():
     if n.key.startswith('region_state:') and not any((sid,n.key.split(':',1)[1]) in v for v in ow.values()):bad.append((str(p),sid,n.key))
  check('valid_'+folder+'_owners',not bad)
 # Protected earlier regional installations remain in force, even though shared file hashes evolve.
 for name,path in [('DP01','DURRANI_PUNJAB_1776/DP-01'),('Arabia01','ARABIA_1776/ARABIA-01')]:
  p=ROOT/'docs/reports/map'/path/'PLAN.json'
  if p.exists():check('protected_'+name,all(ow.get(z['rgb'])=={(z['state'],z['after'])} for z in json.loads(p.read_text(encoding='utf8'))['transfers']))
 b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2];connected={}
 defs={n.key:n for p in effective('common/country_definitions') for n in parse(text(p))}
 for t in TAGS+['KAL','PTA']:
  rs={int(r[1:],16) for r,v in ow.items() if any(tag==t for s,tag in v)};adj=graph(a,np.array(sorted(rs),np.uint32));seen={next(iter(rs))};q=list(seen)
  while q:
   for v,n in adj[q.pop()].items():
    if v in rs and n>=2 and v not in seen:seen.add(v);q.append(v)
  check('land_continuity_'+t,rs==seen);connected[t]=len(rs)
  cap=scalar(defs[t].one('capital'));check('capital_owned_'+t,any((cap,t) in v for v in ow.values()))
  check('population_present_'+t,any(n.key=='region_state:'+t for rel in POPS for n in walk(parse(text(ROOT/rel)))))
 for lang in ['french','english']:
  p=ROOT/'localization'/lang/'replace'/('1776_dp02_l_'+lang+'.yml');keys=re.findall(r'^\s*([^ :]+):0\s+"',text(p),re.M);counter=C.Counter()
  for f in (ROOT/'localization'/lang).rglob('*.yml'):counter.update(k for k in re.findall(r'^\s*([^ :]+):(?:\d+)?\s+"',text(f),re.M) if k in keys)
  check('BOM_'+lang,p.read_bytes().startswith(b'\xef\xbb\xbf'));check('localization_unique_'+lang,all(counter[k]==1 for k in keys))
  needed=['aor1776_dp02_allegiance_pact_desc','law_aor1776_dp02_customs','law_aor1776_dp02_customary_bondage','law_aor1776_dp02_toleration']+list(NEW)
  check('localization_required_'+lang,all(k in keys for k in needed))
 # Subject relation change has a bounded AST delta in its shared file.
 rel='common/history/diplomacy/00_subject_relationships.txt'
 def cleaned(raw):
  return normalized([r for r in parse(raw)])
 oldraw=text(OUT/'preimages'/rel);patch=[]
 for n in walk(parse(oldraw)):
  if n.key=='c:MARATH':
   for p in n.children('create_diplomatic_pact'):
    if scalar(p.one('country'))=='c:GAR':patch.append((p.start,p.end,''))
 check('diplomacy_only_remove_wrong_Garhwal_link',cleaned(edit(oldraw,patch))==cleaned(text(ROOT/rel)))
 profiles=tech_audit('TECH_AFTER.json');prev={z['TAG']:z for z in load('TECH_BEFORE.json')};deltas=[]
 for z in profiles:
  t=z['TAG'];previous={json.dumps(v,sort_keys=True) for v in prev[t]['findings']}
  deltas.append(dict(tag=t,status=z['status'],new_findings=[v for v in z['findings'] if json.dumps(v,sort_keys=True) not in previous]))
 check('restored_profiles_pass',all(z['status']=='PASS_STATIC_ONLY' for z in profiles if z['TAG'] in TAGS))
 check('protected_profiles_no_new_findings',all(not z['new_findings'] for z in deltas if z['tag'] in ['DUR','PAN','KAL','PTA']))
 # Character initialization must not silently retain the restored TAGs' 1836 courts.
 for t in ['BHW','LAD','GAR','MAK']:
  bodies=[text(p)[n.start:n.end] for p in effective('common/history/characters') for n in walk(parse(text(p))) if n.key=='c:'+t]
  check('no_1836_template_'+t,all('template =' not in body for body in bodies))
 for t in TAGS:
  rulers=[q for p in effective('common/history/characters') for n in walk(parse(text(p))) if n.key=='c:'+t for q in n.children('create_character') if q.one('ruler')=='yes']
  check('one_initial_ruler_'+t,len(rulers)==1)
 # Diagnostic map of installed owner cells, not a game screenshot.
 box=json.loads((OUT.parent/'DP-01/VIEW_BOX.json').read_text());x0,y0,x1,y1=box;crop=a[y0:y1,x0:x1];u,ix=np.unique(crop,return_inverse=True)
 palette={'DUR':(87,158,165),'PAN':(231,150,54),'KAL':(112,112,192),'PTA':(199,190,76),'MAK':(206,133,151),'BHW':(93,148,107),'LAD':(49,175,191),'GAR':(60,154,135),'KHR':(106,145,255),'LBL':(188,192,188)}
 palette.update({t:tuple(v[-1]) for t,v in NEW.items()});colors=[]
 for c in u:
  owner=next(iter(ow.get(f'x{int(c):06X}',{('','?')})))[1];colors.append(palette.get(owner,(75,78,79)))
 ar=np.array(colors,np.uint8)[ix].reshape((*crop.shape,3));bd=np.zeros(crop.shape,bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];ar[bd]//=2
 im=Image.new('RGB',((x1-x0)*3,(y1-y0)*3+100),(28,42,52));im.paste(Image.fromarray(ar).resize(((x1-x0)*3,(y1-y0)*3),Image.Resampling.NEAREST),(0,40));d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
 d.text((10,10),'DP-02 : administrations locales rétablies — diagnostic des propriétaires',font=f,fill='white')
 d.text((10,im.height-48),'Bahawalpur • Ladakh • Jammu • rajas des collines • Makran • Kharan • Las Bela • Kalat',font=f,fill='white')
 d.text((10,im.height-26),'Cellules existantes ; frontières fines et démographie à affiner. Validation en jeu encore requise.',font=f,fill='white');im.save(OUT/'INSTALLED_MAP.png')
 current=runtime();unrelated={p:dict(before=m['world_before'].get(p),after=current.get(p)) for p in set(m['world_before'])|set(current) if m['world_before'].get(p)!=current.get(p) and p not in {z['file'] for z in ap['files']}}
 result=dict(status='PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL_STATIC',checks=checks,transfers=len(changes),reviewed_external_owner_changes=len(external),scope_provinces=len(scope),populations=poprows,provinces_by_tag=connected,technology_delta=deltas,unrelated_runtime_deltas=unrelated,runtime_validated=False)
 if (OUT/'VALIDATION.json').exists():
  q=OUT/'audit_history'/(sha(OUT/'VALIDATION.json')[:16]+'.json');q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():q.write_bytes((OUT/'VALIDATION.json').read_bytes())
 dump('VALIDATION.json',result)
 print(json.dumps(dict(status=result['status'],checks=len(checks),failed=[k for k,v in checks.items() if not v],tech_new=[z for z in deltas if z['new_findings']],unrelated_deltas=len(unrelated)),ensure_ascii=False))
 return all(checks.values())
if __name__=='__main__':sys.exit(0 if audit() else 1)
