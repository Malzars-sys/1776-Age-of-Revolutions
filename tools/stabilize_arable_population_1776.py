"""ARABLE-02: bounded gameplay capacity corrections, with staged, guarded writes.

No famine prediction. Uses a dated native baseline only when its inputs still match.
Decentralized transfers use real neighbouring portions and existing culture ranges.
"""
from pathlib import Path
import argparse,collections as C,csv,hashlib,json,math,re,sys
import numpy as np
from PIL import Image
import audit_arable_population_1776 as a
from hbc06_integrate import edit,encoded

ROOT=a.ROOT
OUT=ROOT/'docs/reports/economy/ARABLE_POPULATION_1776/ARABLE-02'
PRIOR=OUT.parent/'ARABLE-01'
CANADA={f'H{i:02}' for i in range(1,14)}

def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def key(r):return r['state']+'|'+r['owner']

def required_land(workers,other_jobs,rural_levels,jobs_per_level):
 if jobs_per_level<=0:raise ValueError('No known subsistence employment')
 return int(math.ceil(max(0,workers-other_jobs)/jobs_per_level-1e-10)+rural_levels)

def minimum_region_land(required,owned_weight,total_weight,current):
 if owned_weight<=0:return None
 # Floor guarantees enough land despite engine allocation remainder tie-breaking.
 return max(int(current),math.ceil(required*total_weight/owned_weight-1e-10))

def apportion(total,weights):
 if total<0 or total>sum(weights):raise ValueError('Invalid proportional transfer')
 if not total:return [0]*len(weights)
 s=sum(weights);base=[total*w//s for w in weights]
 for i in sorted(range(len(weights)),key=lambda i:(-(total*weights[i]%s),i))[:total-sum(base)]:base[i]+=1
 assert sum(base)==total and all(x<=w for x,w in zip(base,weights))
 return base

def compatible_communities(x,y):
 if x['country_type']!='decentralized' or y['country_type']!='decentralized':return False
 # The accepted 2.4M Canadian scenario is a closed pool, not a source for US/Alaska.
 if (x['owner'] in CANADA)!=(y['owner'] in CANADA):return False
 return x['owner']==y['owner'] or bool(x['profiles']&y['profiles']) or (x['owner'] in CANADA and y['owner'] in CANADA)

def canonical_profile(pop,religions):
 fields={n.key:a.scalar(n.value) for n in pop.children() if n.key!='size'}
 fields.setdefault('religion',religions.get(fields.get('culture',''),''))
 if not fields.get('culture') or not fields.get('religion'):raise ValueError('Unresolved source identity')
 return tuple(sorted(fields.items()))

def histories(preimages=False):
 religions={};types={};cultures={};inputs={}
 for p in a.core.effective('common/cultures'):
  inputs[str(p)]=a.digest(p)
  for n in a.parse(p.read_text(encoding='utf-8-sig')):religions[n.key]=a.scalar(n.one('religion',''))
 for p in a.core.effective('common/country_definitions'):
  inputs[str(p)]=a.digest(p)
  for n in a.parse(p.read_text(encoding='utf-8-sig')):
   types[n.key]=a.scalar(n.one('country_type','recognized'));cultures[n.key]=set(a.vals(n,'cultures'))
 # Retain country histories as guarded inputs; POP defaults follow their culture.
 for p in a.core.effective('common/history/countries'):
  inputs[str(p)]=a.digest(p)
 entries=C.defaultdict(list);regions={};texts={}
 for p in a.core.effective('common/history/pops'):
  inputs[str(p)]=a.digest(p)
  before=OUT/'preimages'/p.relative_to(ROOT) if p.is_relative_to(ROOT) else None
  readpath=before if preimages and before and before.exists() else p
  raw=readpath.read_bytes().decode('utf-8-sig');texts[str(p)]=raw
  for sid,n in a.state_nodes(raw).items():
   for rs in n.children():
    if not rs.key.startswith('region_state:'):continue
    tag=rs.key.split(':')[1];k=sid+'|'+tag;regions.setdefault(k,(str(p),rs))
    for q in rs.children('create_pop'):
     entries[k].append({'path':str(p),'node':q,'size':int(q.one('size','0')),'profile':canonical_profile(q,religions)})
 return inputs,entries,regions,texts,cultures

def adjacency(rows,catalog):
 """Side contact only, excludes impassable provinces and explicit barriers."""
 ids={};imp=set();owners={}
 for i,r in enumerate(rows,1):
  for rgb in r['owned_cells']:owners[int(rgb[1:],16)]=i
 for region in catalog.regions.values():imp.update(int(v[1:],16) for v in a.vals(region,'impassable'))
 raster=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
 rgb=(raster[:,:,0]<<16)|(raster[:,:,1]<<8)|raster[:,:,2]
 lu=np.zeros(1<<24,dtype=np.uint16)
 for v,i in owners.items():
  if v not in imp:lu[v]=i
 labels=lu[rgb];pairs=set();witness={}
 blocked=set();p=ROOT/'map_data/adjacencies.csv'
 if not p.exists():p=a.GAME/'map_data/adjacencies.csv'
 with p.open(encoding='utf-8-sig') as f:
  for q in csv.DictReader(f,delimiter=';'):
   if all(q.get(k,'').startswith('x') for k in ['From','To']) and (q.get('Type') in ['sea','impassable'] or q.get('adjacency_rule_name','').strip()):blocked.add(tuple(sorted(int(q[k][1:],16) for k in ['From','To'])))
 for axis in [0,1]:
  l=labels[:-1,:] if axis==0 else labels[:,:-1];r=labels[1:,:] if axis==0 else labels[:,1:]
  la=rgb[:-1,:] if axis==0 else rgb[:,:-1];ra=rgb[1:,:] if axis==0 else rgb[:,1:]
  mask=(l!=r)&(l>0)&(r>0)
  values=np.unique((la[mask].astype('uint64')<<24)|ra[mask])
  for z in values:
   x=int(z)>>24;y=int(z)&0xffffff
   if tuple(sorted((x,y))) in blocked:continue
   i,j=sorted((owners[x]-1,owners[y]-1));pairs.add((i,j));witness.setdefault((i,j),[f'x{x:06X}',f'x{y:06X}'])
 adj=C.defaultdict(set)
 for i,j in pairs:adj[i].add(j);adj[j].add(i)
 return adj,witness

def prepare():
 assert not (OUT/'PLAN.json').exists(),'Preserve existing plan; use a new dossier for a new pass.'
 data=json.loads((OUT/'CURRENT_INVENTORY.json').read_text());rows=data['rows'];cat=a.Catalog()
 old=json.loads((PRIOR/'delivery/DIAGNOSIS.json').read_text())
 changes=[]
 for p,h in old['input_manifest'].items():
  if a.digest(Path(p))!=h and Path(p)!=ROOT/'map_data/state_regions/10_india.txt':changes.append(p)
 assert not changes,('Native baseline inputs changed',changes)
 assert a.digest(ROOT/'map_data/state_regions/10_india.txt')=='92db3846c8363a98f7f54731642322527dac5c323aa7bebebd168d8e05534094','Reassess native baseline for changed India'
 inputs,entries,popregions,texts,cultures=histories();inputs.update(cat.inputs)
 owned=C.defaultdict(set)
 for p in a.core.effective('common/history/states'):
  inputs[str(p)]=a.digest(p)
  for sid,node in a.state_nodes(p.read_text(encoding='utf-8-sig')).items():
   for q in node.children('create_state'):owned[sid+'|'+a.scalar(q.one('country'))[2:]].update(a.vals(q,'owned_provinces'))
 for r in rows:r['owned_cells']=sorted(owned[key(r)])
 for p in [ROOT/'map_data/provinces.png',ROOT/'common/defines/00_defines.txt',ROOT/'map_data/adjacencies.csv']:
  if p.exists():inputs[str(p)]=a.digest(p)
 by_state=C.defaultdict(list)
 for r in rows:by_state[r['state']].append(r)
 for sid,rs in by_state.items():
  total=sum(r['owner_land_weight'] for r in rs)
  for r in rs:
   r['owned_weight_total']=total;r['land_fraction']=r['owner_land_weight']/total if total else 0
   r['planning_fraction']=r['land_fraction'];r['allocation_basis']='weighted_habitable_provinces'
   n=r['native'];r['native_usable']=bool(n and n.get('population')==r['population'] and r['population']>0)
   r['workers_before']=n['workforce'] if r['native_usable'] else r['population']*.30
   r['worker_ratio']=max(.30,r['workers_before']/r['population']) if r['population'] else .30
   r['land_before']=int(n['arable_land']) if n else int(r['arable_owner_estimate'])
   r['per_level']=r['subsistence_jobs_per_level_min']
   r['rural_built']=n['built_agricultural_levels'] if n else r['agricultural_levels_max']
   r['other_jobs']=max(0,n['jobs_full_max']-n['subsistence_jobs_max']) if n else r['other_jobs_min']
   r['jobs_before']=r['other_jobs']+max(0,r['land_before']-r['rural_built'])*r['per_level']
   # Recompute the current land for the accepted Agra change; dated save is before it.
   if sid=='STATE_AGRA':
    r['land_before']=a.share_land(r['arable_region'],r['owner_land_weight'],total)
    r['jobs_before']=r['other_jobs']+max(0,r['land_before']-r['rural_built'])*r['per_level']
   r['workers_projected']=r['workers_before'];r['population_after']=r['population'];r['transfer_in']=r['transfer_out']=0
   r['profiles']={dict(e['profile'])['culture'] for e in entries[key(r)]}
   if r['native_usable']:
    f=r.get('native_meta',{}).get('land_fraction')
    if f is None:f=1.0
    r['allocation_fraction_native']=f
    r['allocation_fraction_difference']=f-r['land_fraction']
    if abs(f-r['land_fraction'])>=.00011:
     # Existing map/history discrepancies are explicit. Use measured engine share,
     # with conservative serialized rounding allowance; do not pretend exact geometry.
     r['planning_fraction']=max(0,f-.00005)
     r['allocation_basis']='measured_native_fraction_lower_rounding_bound'
 adj,witness=adjacency(rows,cat);flows=[];pop_deltas=C.Counter()
 def compatible(i,j):
  x,y=rows[i],rows[j]
  return compatible_communities(x,y)
 # Prioritize actual deficits, then shortest admissible chains to spare capacity.
 for i in sorted(range(len(rows)),key=lambda i:rows[i]['workers_before']-rows[i]['jobs_before'],reverse=True):
  r=rows[i]
  if r['country_type']!='decentralized' or not r['native_usable'] or not entries[key(r)]:continue
  need=max(0,r['workers_projected']-r['jobs_before'])
  if need<=0:continue
  distance={i:0};previous={};queue=[i]
  for u in queue:
   if distance[u]>=3:continue
   for v in sorted(adj[u]):
    if v not in distance and compatible(i,v) and compatible(u,v):distance[v]=distance[u]+1;previous[v]=u;queue.append(v)
  candidates=[j for j in distance if j!=i and rows[j]['land_fraction']>0 and entries[key(rows[j])]]
  candidates.sort(key=lambda j:(rows[j]['owner']!=r['owner'],distance[j],-(rows[j]['jobs_before']-rows[j]['workers_projected'])))
  for j in candidates:
   y=rows[j];spare=max(0,y['jobs_before']-y['workers_projected']);ratio=max(r['worker_ratio'],y['worker_ratio'])
   # Retain a nonempty community; do not depopulate a country to make a check green.
   n=min(math.ceil(need/r['worker_ratio']-1e-9),math.floor(spare/ratio+1e-9),max(0,r['population_after']-min(1000,r['population'])))
   if n<=0:continue
   source=entries[key(r)]
   # Canonical counters handle repeated cohorts and successive transfers exactly.
   pools=C.Counter()
   for e in source:pools[e['profile']]+=e['size']
   for profile in pools:pools[profile]+=pop_deltas[key(r),profile]
   profiles=sorted(pools);amounts=apportion(n,[pools[z] for z in profiles])
   cohort=[]
   for z,v in zip(profiles,amounts):
    if v:pop_deltas[key(r),z]-=v;pop_deltas[key(y),z]+=v;cohort.append({'profile':dict(z),'population':v})
   route=[j]
   while route[-1]!=i:route.append(previous[route[-1]])
   route.reverse();edges=[witness[tuple(sorted((u,v)))] for u,v in zip(route,route[1:])]
   flows.append({'from':key(r),'to':key(y),'population':n,'cohorts':cohort,'neighbour_path':[key(rows[z]) for z in route],'edge_rgb_witnesses':edges,'same_owner':r['owner']==y['owner'],'canada_gameplay_pool':r['owner'] in CANADA and y['owner'] in CANADA})
   r['population_after']-=n;y['population_after']+=n;r['transfer_out']+=n;y['transfer_in']+=n
   r['workers_projected']-=n*r['worker_ratio'];y['workers_projected']+=n*ratio
   need=max(0,r['workers_projected']-r['jobs_before'])
   if need<1e-6:break
 land={};blocked=[]
 for r in rows:
  incorporated=r.get('native_meta',{}).get('incorporation')==1 if r.get('native_meta') else r.get('type_declared')=='incorporated'
  if r['country_type']=='decentralized' or not incorporated:continue
  if r['population']==0 or r['workers_projected']<=r['jobs_before']+1e-6:continue
  if not r['native_usable']:
   blocked.append({'portion':key(r),'reason':'No matching native population baseline'});continue
  needed=required_land(r['workers_projected'],r['other_jobs'],r['rural_built'],r['per_level'])
  target=minimum_region_land(needed,r['planning_fraction'],1,r['arable_region'])
  if target is None:
   blocked.append({'portion':key(r),'reason':'Owner has only impassable provinces; arable increase cannot reach it'});continue
  land[r['state']]=max(land.get(r['state'],int(r['arable_region'])),target)
 modifications=C.defaultdict(list)
 for sid,target in sorted(land.items()):
  source=cat.locations['map_data/state_regions'][sid]['file'];assert source.startswith('MOD:'),source
  p=ROOT/source[4:];raw=p.read_bytes().decode('utf-8-sig');node=next(n for n in a.parse(raw) if n.key==sid);field=node.children('arable_land');assert len(field)==1
  modifications[str(p)].append((field[0].start,field[0].end,'arable_land = '+str(target)))
 population_changes=[]
 for k in sorted({k for k,z in pop_deltas}):
  old_entries=entries[k];existing=C.defaultdict(list)
  for e in old_entries:existing[e['profile']].append(e)
  additions=[]
  for profile in sorted({z for kk,z in pop_deltas if kk==k}):
   delta=pop_deltas[k,profile]
   if not delta:continue
   population_changes.append({'portion':k,'profile':dict(profile),'delta':delta})
   es=existing[profile]
   if delta>0 and es:
    e=es[0];q=e['node'].children('size');assert len(q)==1
    modifications[e['path']].append((q[0].start,q[0].end,'size = '+str(e['size']+delta)))
   elif delta<0:
    removal=apportion(-delta,[e['size'] for e in es])
    for e,n in zip(es,removal):
     if not n:continue
     if n==e['size']:modifications[e['path']].append((e['node'].start,e['node'].end,''))
     else:
      q=e['node'].children('size');assert len(q)==1
      modifications[e['path']].append((q[0].start,q[0].end,'size = '+str(e['size']-n)))
   else:
    fields=' '.join(f'{name} = {value}' for name,value in profile)
    additions.append('\n\t\t\tcreate_pop = { '+fields+' size = '+str(delta)+' }')
  if additions:
   path,node=popregions[k];modifications[path].append((node.end-1,node.end-1,''.join(additions)+'\n\t\t'))
 files=[]
 for path,edits in modifications.items():
  p=Path(path);assert p.is_relative_to(ROOT);raw=p.read_bytes().decode('utf-8-sig')
  after=encoded(p,edit(raw,edits));rel=p.relative_to(ROOT);pre=OUT/'preimages'/rel;stage=OUT/'staged'/rel
  pre.parent.mkdir(parents=True,exist_ok=True);pre.write_bytes(p.read_bytes());stage.parent.mkdir(parents=True,exist_ok=True);stage.write_bytes(after)
  files.append({'path':rel.as_posix(),'before':a.digest(p),'after':a.digest(stage)})
 for r in rows:
  target=land.get(r['state'],int(r['arable_region']));r['arable_region_after']=target
  r['land_after_floor']=math.floor(target*r['planning_fraction']+1e-8) if r['state'] in land else r['land_before']
  r['jobs_after_floor']=r['other_jobs']+max(0,r['land_after_floor']-r['rural_built'])*r['per_level']
  r['remaining_gap']=max(0,r['workers_projected']-r['jobs_after_floor'])
  r['incorporated']=r.get('native_meta',{}).get('incorporation')==1 if r.get('native_meta') else r.get('type_declared')=='incorporated'
  r['famine_observed_before']=r['native']['famine_active'] if r['native'] else None
  r.pop('profiles',None)
 dump(OUT/'INPUTS.json',inputs);dump(OUT/'PLAN.json',{'status':'PREPARED_FOR_AUTHORIZED_INSTALLATION','policy':'User-authorized gameplay stabilization; not a historical population finding','canada_population_before':sum(r['population'] for r in rows if r['owner'] in CANADA),'canada_population_after':sum(r['population_after'] for r in rows if r['owner'] in CANADA),'flows':flows,'population_changes':population_changes,'land_changes':land,'blocked_centralized':blocked,'files':files,'native_source':{'file':'../ARABLE-01/delivery/DIAGNOSIS.json','date':old['native']['date'],'save_sha256':old['native']['sha256']}})
 dump(OUT/'PROJECTED_STATES.json',rows)
 a.write_csv(OUT/'WORLD_CONTROL.csv',[{k:r.get(k) for k in ['state','owner','country_type','incorporated','population','population_after','transfer_out','transfer_in','arable_region','arable_region_after','land_before','land_after_floor','workers_before','workers_projected','jobs_before','jobs_after_floor','remaining_gap','famine_observed_before']} for r in rows])
 print(json.dumps({'land_regions':len(land),'flows':len(flows),'population_moved':sum(f['population'] for f in flows),'blocked_centralized':blocked,'files':len(files),'remaining_decentralized_portions':sum(r['country_type']=='decentralized' and r['remaining_gap']>1e-6 for r in rows)}))

def apply():
 assert not (OUT/'APPLIED.json').exists(),'Already installed'
 plan=json.loads((OUT/'PLAN.json').read_text());inputs=json.loads((OUT/'INPUTS.json').read_text())
 for p,h in inputs.items():assert a.digest(Path(p))==h,('Concurrent input change; re-evaluate',p)
 for r in plan['files']:
  p=ROOT/r['path'];assert a.digest(p)==r['before'];assert a.digest(OUT/'staged'/r['path'])==r['after']
 baseline={str(p.relative_to(ROOT)):a.digest(p) for folder in ['common','map_data','localization','events','gui'] for p in (ROOT/folder).rglob('*') if p.is_file()}
 dump(OUT/'RUNTIME_BASELINE.json',baseline)
 for r in plan['files']:
  p=ROOT/r['path'];assert a.digest(p)==r['before'];p.write_bytes((OUT/'staged'/r['path']).read_bytes())
 dump(OUT/'APPLIED.json',{'status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','files':plan['files'],'human_authorization':'Current request: redistribute decentralized populations; preserve Canadian total; increase insufficient incorporated states arable land','runtime_after_changes_validated':False})
 validate()

def validate():
 plan=json.loads((OUT/'PLAN.json').read_text());rows=json.loads((OUT/'PROJECTED_STATES.json').read_text());checks={}
 base={p.replace('\\','/'):h for p,h in json.loads((OUT/'RUNTIME_BASELINE.json').read_text()).items()};expected={r['path']:r['after'] for r in plan['files']}
 actualchanges={p for p,h in base.items() if not (ROOT/p).exists() or a.digest(ROOT/p)!=h}
 checks['exact_planned_runtime_files_only']=actualchanges==set(expected)
 checks['staged_hashes_installed']=all(a.digest(ROOT/p)==h for p,h in expected.items())
 checks['canada_total_preserved']=plan['canada_population_before']==plan['canada_population_after']==2400000
 checks['world_population_preserved']=sum(r['population'] for r in rows)==sum(r['population_after'] for r in rows)
 profile_delta=C.Counter()
 for r in plan['population_changes']:profile_delta[tuple(sorted(r['profile'].items()))]+=r['delta']
 checks['all_culture_religion_type_cohorts_preserved']=all(v==0 for v in profile_delta.values())
 protected=['STATE_AGRA|MARATH','STATE_AGRA|GAR']
 checks['agra_population_and_764_preserved']=all(r['population_after']==r['population'] and r['arable_region_after']==764 for r in rows if key(r) in protected)
 blocked={r['portion'] for r in plan['blocked_centralized']}
 checks['incorporated_capacity_cleared_except_explicit_blockers']=all(r['remaining_gap']<1e-6 or key(r) in blocked for r in rows if r['country_type']!='decentralized' and r['incorporated'])
 checks['no_recipient_new_capacity_shortfall']=all(r['remaining_gap']<1e-6 for r in rows if r['transfer_in']>0)
 checks['no_depopulated_community']=all(r['population_after']>0 for r in rows if r['population']>0)
 # Independent reparsing of written histories, not just arithmetic in the plan.
 _,entries,_,_,_=histories();actual=C.Counter({k:sum(e['size'] for e in es) for k,es in entries.items()})
 checks['written_populations_match_plan']=all(actual[key(r)]==r['population_after'] for r in rows)
 _,before_entries,_,_,_=histories(preimages=True)
 def profiles(entries):
  c=C.Counter()
  for es in entries.values():
   for e in es:c[e['profile']]+=e['size']
  return c
 checks['written_world_cohorts_equal_preimages']=profiles(entries)==profiles(before_entries)
 def structural(nodes,skip):
  return [(n.key,n.op,structural(n.children(),skip) if isinstance(n.value,list) else n.value) for n in nodes if n.key not in skip]
 regions_unchanged=pops_other_fields=True
 for f in plan['files']:
  before=(OUT/'preimages'/f['path']).read_bytes().decode('utf-8-sig');after=(ROOT/f['path']).read_bytes().decode('utf-8-sig')
  if f['path'].startswith('map_data/state_regions/'):
   regions_unchanged &= structural(a.parse(before),{'arable_land'})==structural(a.parse(after),{'arable_land'})
  else:pops_other_fields &= structural(a.parse(before),{'create_pop'})==structural(a.parse(after),{'create_pop'})
 checks['province_ownership_geometry_resources_traits_hubs_unchanged']=bool(regions_unchanged)
 checks['population_history_other_commands_unchanged']=bool(pops_other_fields)
 cat=a.Catalog();checks['written_arable_matches_plan']=all(int(cat.regions[sid].one('arable_land'))==target for sid,target in plan['land_changes'].items())
 dump(OUT/'VALIDATION.json',{'status':'PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL','checks':checks,'runtime_files_preserved':len(base)-len(expected),'runtime_after_changes_validated':False})
 print(json.dumps(checks));assert all(checks.values())

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['prepare','apply','validate']);args=ap.parse_args();globals()[args.action]()
