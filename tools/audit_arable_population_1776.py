"""Read-only land/employment screening plus reconciliation with a native save.

This never changes runtime files. A job-capacity warning is not a famine diagnosis.
Run --help. Unknown PMs, split-state allocation and duplicate histories stay explicit.
"""
from pathlib import Path
import argparse,collections as C,csv,hashlib,html,json,math,re
from datetime import datetime,timezone
import audit_starting_tech_1776 as core
from validate_diplomacy_ottoman_1776 import parse,walk,scalar
from hbc06_integrate import state_nodes

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Games/Victoria 3/game')
DEFAULT_OUT=ROOT/'docs/reports/economy/ARABLE_POPULATION_1776/ARABLE-01/diagnostic'

def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def num(v,default=0):
 try:return float(scalar(v))
 except (TypeError,ValueError):return default

def vals(n,k):return core.values(n,k)
def ref(p):return core.ref(p)

def declared_levels(n):
 """Explicit level takes precedence. Ownership amounts describe the same levels."""
 for k in ('level','levels'):
  if n.children(k):return num(n.one(k)), 'explicit_'+k
 owners=[x for a in n.children('add_ownership') for x in a.children() if x.key in ['country','building']]
 if owners and all(x.children('levels') for x in owners):return sum(num(x.one('levels')) for x in owners),'ownership_levels'
 return None,'unknown_levels'

def share_land(total,owned,region_provinces):
 return math.floor(total*owned/region_provinces+0.5) if region_provinces else None

def prime_land_weight():
 p=ROOT/'common/defines/00_defines.txt'
 if not p.exists():p=GAME/'common/defines/00_defines.txt'
 m=re.search(r'^\s*SPLIT_STATE_PRIME_LAND_WEIGHT\s*=\s*([\d.]+)',p.read_text(encoding='utf-8-sig'),re.M)
 if not m:raise ValueError('Missing SPLIT_STATE_PRIME_LAND_WEIGHT')
 return float(m[1])

def land_weights(region,owned,prime_weight):
 """Habitable provinces only; prime land carries the effective define weight."""
 imp=set(vals(region,'impassable'));prime=set(vals(region,'prime_land'))
 weights={r:(prime_weight if r in prime else 1) for r in vals(region,'provinces') if r not in imp}
 return sum(weights.get(r,0) for r in set(owned)),sum(weights.values())

def pressure(population,capacity,ratio):
 return max(0,population*ratio-capacity)

class Catalog:
 def __init__(self):
  self.inputs={};self.objects={};self.locations={};self.collisions=[]
  for folder in ['map_data/state_regions','common/buildings','common/building_groups','common/production_methods','common/production_method_groups']:
   defs={};loc={}
   for p in core.effective(folder):
    self.inputs[str(p)]=digest(p);raw=p.read_text(encoding='utf-8-sig')
    for n in parse(raw):
     k=n.key.removeprefix('REPLACE_OR_CREATE:').removeprefix('REPLACE:')
     if k in defs:self.collisions.append(dict(folder=folder,key=k,before=loc[k],after=ref(p)))
     defs[k]=n;loc[k]=dict(file=ref(p),line=raw.count('\n',0,n.start)+1)
   self.objects[folder]=defs;self.locations[folder]=loc
  self.regions=self.objects['map_data/state_regions'];self.buildings=self.objects['common/buildings'];self.groups=self.objects['common/building_groups'];self.pms=self.objects['common/production_methods'];self.pmgs=self.objects['common/production_method_groups']

 def group_field(self,group,key,default=None,trail=()):
  if group not in self.groups or group in trail:return default
  n=self.groups[group]
  if n.children(key):return scalar(n.one(key))
  return self.group_field(scalar(n.one('parent_group','')),key,default,trail+(group,))

 def is_rural(self,kind):
  b=self.buildings.get(kind)
  return b is not None and self.group_field(scalar(b.one('building_group')),'land_usage')=='rural'

 def pm_vector(self,key):
  n=self.pms.get(key);jobs=C.Counter();grain=0;unknown=[]
  if n is None:return jobs,0,['unknown_pm:'+key]
  for b in n.children('building_modifiers'):
   for scale in b.children():
    for q in scale.children():
     m=re.fullmatch(r'building_employment_(.+)_add',q.key)
     if m:
      if scale.key=='level_scaled' and re.fullmatch(r'-?[\d.]+',str(q.value)):jobs[m[1]]+=num(q.value)
      else:unknown.append('nonlevel_or_dynamic_employment:'+key+':'+q.key)
     if q.key.startswith('building_employment_') and q.key.endswith('_mult'):unknown.append('employment_multiplier:'+key)
     if q.key=='goods_output_grain_add' and scale.key=='workforce_scaled':grain+=num(q.value)
  return jobs,grain,unknown

 def capacity(self,kind,selected):
  if kind not in self.buildings:return dict(jobs_min=0,jobs_max=0,grain_min=0,grain_max=0,unknown=['unknown_building:'+kind],assumed_groups=[])
  low=high=glo=ghi=0;unknown=[];assumed=[]
  groups=vals(self.buildings[kind],'production_method_groups');assigned={};unused=[]
  for pm in selected:
   matching=[g for g in groups if g in self.pmgs and pm in vals(self.pmgs[g],'production_methods')]
   if not matching:unused.append(pm)
   for g in matching:assigned[g]=pm
  unknown+=['unassigned_pm:'+p for p in unused]
  for g in groups:
   options=[assigned[g]] if g in assigned else (vals(self.pmgs[g],'production_methods') if g in self.pmgs else [])
   if not options:unknown.append('unknown_or_empty_pmg:'+g);continue
   if len(options)>1:assumed.append(g)
   choices=[self.pm_vector(p) for p in options]
   # Negative automation jobs must offset base jobs: clamp only after combining groups.
   low+=min(sum(j.values()) for j,gr,u in choices);high+=max(sum(j.values()) for j,gr,u in choices)
   glo+=min(gr for j,gr,u in choices);ghi+=max(gr for j,gr,u in choices)
   unknown.extend(v for j,gr,u in choices for v in u)
  return dict(jobs_min=max(0,low),jobs_max=max(0,high),grain_min=glo,grain_max=ghi,unknown=sorted(set(unknown)),assumed_groups=assumed)

def startup(c):
 owners=C.defaultdict(C.Counter);owned_cells=C.defaultdict(set);pop=C.Counter();decl=C.defaultdict(list);population_sources=C.defaultdict(list)
 for folder in ['common/history/states','common/history/pops','common/history/buildings']:
  for p in core.effective(folder):
   c.inputs[str(p)]=digest(p);raw=p.read_text(encoding='utf-8-sig')
   for sid,n in state_nodes(raw).items():
    if folder.endswith('/states'):
     for q in n.children('create_state'):
      tag=scalar(q.one('country'))[2:];cells=vals(q,'owned_provinces')
      owners[sid][tag]+=len(cells);owned_cells[sid,tag].update(cells)
    else:
     for rs in n.children():
      if not rs.key.startswith('region_state:'):continue
      tag=rs.key.split(':',1)[1];key=(sid,tag)
      if folder.endswith('/pops'):
       pop[key]+=sum(int(q.one('size','0')) for q in rs.children('create_pop'))
       population_sources[key].append(dict(file=ref(p),line=raw.count('\n',0,rs.start)+1))
      else:
       for q in rs.children('create_building'):
        level,method=declared_levels(q);kind=scalar(q.one('building'))
        decl[key].append(dict(building=kind,levels=level,level_source=method,pms=vals(q,'activate_production_methods'),source=dict(file=ref(p),line=raw.count('\n',0,q.start)+1)))
 rows=[];prime_weight=prime_land_weight()
 for sid,tag in sorted(set(pop)|{(s,t) for s,d in owners.items() for t in d}):
  key=sid,tag;r=c.regions.get(sid);warning=[]
  if r is None:continue
  a=num(r.one('arable_land'));nprov=len(vals(r,'provinces'))
  own_weight,region_weight=land_weights(r,owned_cells[key],prime_weight)
  region_weight=sum(land_weights(r,owned_cells[sid,t],prime_weight)[0] for t in owners[sid])
  share=share_land(a,own_weight,region_weight) if region_weight else 0
  if not owners[sid][tag] and pop[key]:warning.append('unknown_ownership_for_population_history')
  if share is None:warning.append('unknown_land_allocation');share=0
  rural_lo=rural_hi=jobs_lo=jobs_hi=grain_lo=grain_hi=0;by=C.defaultdict(list);detail=[]
  for d in decl[key]:by[d['building']].append(d)
  for kind,ds in by.items():
   known=[d['levels'] for d in ds if d['levels'] is not None]
   if len(known)!=len(ds):warning.append('unknown_levels:'+kind)
   # History duplicate semantics may differ. Publish an envelope, never sum silently.
   levels_lo=min(known,default=0);levels_hi=sum(known)
   if len(ds)>1:warning.append('duplicate_history_declarations:'+kind)
   cap=c.capacity(kind,[p for d in ds for p in d['pms']]);warning+=cap['unknown']
   if cap['assumed_groups']:warning.append('unspecified_PM_envelope:'+kind)
   jobs_lo+=levels_lo*cap['jobs_min'];jobs_hi+=levels_hi*cap['jobs_max']
   grain_lo+=levels_lo*cap['grain_min'];grain_hi+=levels_hi*cap['grain_max']
   if c.is_rural(kind):rural_lo+=levels_lo;rural_hi+=levels_hi
   detail.append(dict(building=kind,level_min=levels_lo,level_max=levels_hi,capacity_per_level=cap,declarations=ds))
  subs=scalar(r.one('subsistence_building','building_subsistence_farm'));sc=c.capacity(subs,[]);warning+=sc['unknown']
  remaining_lo=max(0,share-rural_hi);remaining_hi=max(0,share-rural_lo)
  jlo=jobs_lo+remaining_lo*sc['jobs_min'];jhi=jobs_hi+remaining_hi*sc['jobs_max']
  pops=pop[key]
  invalid=any(x.startswith(('unknown_','nonlevel_','employment_multiplier:','unassigned_pm:')) for x in warning)
  severity='A_EXAMINER' if invalid else ('PRESSION_ROBUSTE' if pressure(pops,jhi,.25)>0 else ('PRESSION_A_30_PCT' if pressure(pops,jhi,.30)>0 else 'PAS_DE_SATURATION_DEMONTREE'))
  required30=(math.ceil(max(0,pops*.30-jobs_hi)/sc['jobs_max'])+rural_lo) if sc['jobs_max'] else None
  rows.append(dict(state=sid,owner=tag,population=pops,arable_region=a,arable_owner_estimate=share,owner_provinces=owners[sid][tag],region_provinces=nprov,owner_land_weight=own_weight,region_land_weight=region_weight,land_allocation_method='habitable_provinces_prime_land_weighted',subsistence_building=subs,subsistence_jobs_per_level_min=sc['jobs_min'],subsistence_jobs_per_level_max=sc['jobs_max'],agricultural_levels_min=rural_lo,agricultural_levels_max=rural_hi,subsistence_levels_min=remaining_lo,subsistence_levels_max=remaining_hi,other_jobs_min=jobs_lo,other_jobs_max=jobs_hi,total_jobs_min=jlo,total_jobs_max=jhi,job_gap_25=pressure(pops,jhi,.25),job_gap_30=pressure(pops,jhi,.30),job_gap_35=pressure(pops,jhi,.35),arable_owner_needed_30_scenario=required30,grain_market_base_min=grain_lo+remaining_lo*sc['grain_min'],grain_market_base_max=grain_hi+remaining_hi*sc['grain_max'],screening=severity,warnings=sorted(set(warning)),population_sources=population_sources[key],buildings=detail))
 return rows

def food_thresholds():
 """Use effective define constants; do not invent a jobs-to-famine conversion."""
 p=ROOT/'common/defines/00_defines.txt'
 if not p.exists():p=GAME/'common/defines/00_defines.txt'
 raw=p.read_text(encoding='utf-8-sig')
 def get(k):
  m=re.search(r'^\s*'+re.escape(k)+r'\s*=\s*([\d.]+)',raw,re.M)
  if not m:raise ValueError('Unresolved food-security define '+k)
  return float(m[1])
 return dict(starvation=get('@starvation_threshold'),severe=get('FOOD_SECURITY_SEVERE_STARVATION_THRESHOLD'),famine_starving_share=get('FAMINE_POPULATION_SHARE_IN_STARVATION'),famine_severe_share=get('FAMINE_POPULATION_SHARE_IN_SEVERE_STARVATION'),source=str(p),sha256=digest(p),famine_rule='Both population-share thresholds; engine HasFamine is authoritative')

def native_save(c,path):
 """Streaming melted save. Famine manager overrides inconsistent serialized POP caches."""
 import inspect_oct09_saved_crews as s
 s.SAVE=Path(path);countries={};states={};builds=C.defaultdict(list);pops=C.defaultdict(C.Counter);famines={};cache=C.Counter()
 for sec,ident,raw in s.objects():
  if sec=='country_manager':countries[ident]=s.field(raw,'definition')
  elif sec=='states':states[ident]=dict(native_id=ident,state=s.field(raw,'region'),country_id=int(s.field(raw,'country') or -1),arable_land=num(s.field(raw,'arable_land')),land_share=num(s.field(raw,'land')),serialized_unemployed=num(re.search(r'\bpopulation_unemployed_workforce=([\d.]+)',raw)[1]) if re.search(r'\bpopulation_unemployed_workforce=([\d.]+)',raw) else 0)
  elif sec=='building_manager':
   kind=s.field(raw,'building');sid=int(s.field(raw,'state') or -1);level=num(s.field(raw,'levels'));staff=num(s.field(raw,'staffing'))
   pms=re.search(r'^\t{3}production_methods=\{(.*?)^\t{3}\}',raw,re.M|re.S);pm=re.findall(r'"([^"]+)"',pms[1]) if pms else []
   if kind=='building_conscription_center' and s.field(raw,'active')!='yes':continue
   cap=c.capacity(kind,pm);builds[sid].append(dict(id=ident,building=kind,levels=level,staffing=staff,pms=pm,capacity=cap,rural=c.is_rural(kind)))
  elif sec=='pops':
   sid=int(s.field(raw,'location') or -1);w=int(s.field(raw,'workforce') or 0);d=int(s.field(raw,'dependents') or 0);kind=s.field(raw,'type');workplace=s.field(raw,'workplace');pop=pops[sid]
   pop['population']+=w+d;pop['workforce']+=w;pop['dependents']+=d
   if kind=='peasants':pop['peasants']+=w
   elif workplace and workplace!='4294967295':pop['salaried']+=w
   elif kind!='slaves':pop['unemployed']+=w
   else:pop['unemployed_slaves']+=w
   fs=re.search(r'\t{3}food_security=\{(.*?)\t{3}\}',raw,re.S)
   if fs:
    state=re.search(r'\bstate=(\w+)',fs[1]);cache[(state[1] if state else 'unknown')]+=w+d
  elif sec=='famine_manager':
   sid=int(s.field(raw,'state') or -1);famines[sid]=dict(id=ident,start=s.field(raw,'start_date'),raw=raw)
 rows=[]
 for ident,r in states.items():
  if not r['state']:continue
  r.update(owner=countries.get(r['country_id'],'?'),**dict(pops[ident]));bs=builds[ident]
  sub=[b for b in bs if b['building'] and b['building'].startswith('building_subsistence')]
  jmin=sum(b['levels']*b['capacity']['jobs_min'] for b in bs);jmax=sum(b['levels']*b['capacity']['jobs_max'] for b in bs)
  # Self-employed owner POPs can lack workplace IDs. The engine's own unemployment
  # statistic, checked against its UI, is authoritative; do not call them jobless.
  r['unassigned_workforce_reconstructed']=r.get('unemployed',0)
  r['unemployed']=r['serialized_unemployed']
  r['employed_observed']=r.get('workforce',0)-r['unemployed']
  r['unmodeled_employed_jobs']=max(0,r['employed_observed']-jmax)
  jmax=max(jmax,r['employed_observed'])
  r.update(famine_active=ident in famines,famine_details=famines.get(ident),subsistence_levels=sum(b['levels'] for b in sub),subsistence_jobs_max=sum(b['levels']*b['capacity']['jobs_max'] for b in sub),built_agricultural_levels=sum(b['levels'] for b in bs if b['rural'] and b not in sub),jobs_full_min=jmin,jobs_full_max=jmax,workforce_gap_full_capacity=max(0,r.get('workforce',0)-jmax),buildings=bs,starving_pct=None,mild_starving_pct=None,severe_starving_pct=None,food_cache_caveat='POP food_security values/states can be stale at initial pause. Do not infer 0% starvation or overwrite the engine famine flag from this cache.')
  rows.append(r)
 with Path(path).open(encoding='utf8') as f:head=f.read(12000)
 date=re.search(r'^date=([^\s]+)',head,re.M)
 return dict(path=str(Path(path).resolve()),sha256=digest(path),date=date[1] if date else None,states=rows,famine_states=len(famines),serialized_pop_food_security=dict(cache),runtime_observed=True,simulation_after_initial_date=False)

def merge_observations(native,path,thresholds):
 if native is None:raise ValueError('UI observations require their dated native save')
 data=json.loads(path.read_text(encoding='utf8'));assert data['native_save_sha256']==native['sha256'],'Observation/save version mismatch'
 assert data['date']==native['date'],'Observation/save date mismatch'
 by={(r['state'],r['owner']):r for r in native['states']};checks=[]
 for obs in data['observations']:
  key=obs['state'],obs['owner'];r=by[key];passed=[]
  if 'famine_active' in obs:passed.append(r['famine_active']==obs['famine_active'])
  for field in ['starving_pct','mild_starving_pct','severe_starving_pct']:
   if field in obs:
    assert 0<=obs[field]<=100; r[field]=obs[field]
  if r['starving_pct'] is not None and r['severe_starving_pct'] is not None:
   condition=r['starving_pct']/100>=thresholds['famine_starving_share'] and r['severe_starving_pct']/100>=thresholds['famine_severe_share']
   passed.append(condition==r['famine_active'])
  for field in ['unemployed','peasants','arable_land']:
   if field in obs:passed.append(abs(r[field]-obs[field])<=(0 if field=='arable_land' else obs.get('rounding_tolerance',0)))
  if all(r[k] is not None for k in ['starving_pct','mild_starving_pct','severe_starving_pct']):
   assert abs(r['starving_pct']-r['mild_starving_pct']-r['severe_starving_pct'])<=2,'Inconsistent rounded UI percentages'
  checks.append(dict(state=key[0],owner=key[1],pass_checks=all(passed),checks=len(passed),observation=obs))
 native['UI_reconciliation']=checks
 if not all(z['pass_checks'] for z in checks):raise ValueError('UI reconciliation failure; inspect observation version, units and rounding')

def reconciliation(rows,native):
 if native is None:return None
 by={(r['state'],r['owner']):r for r in rows};results=[]
 for n in native['states']:
  s=by.get((n['state'],n['owner']));delta=n.get('population',0)-s['population'] if s else None
  n['population_history_delta']=delta
  n['history_matches_save_population']=delta==0
  category=('FAMINE_ET_SATURATION' if n['workforce_gap_full_capacity']>0 else 'FAMINE_SANS_SATURATION_DEMONTREE') if n['famine_active'] else ('SATURATION_SANS_CRISE_DECLAREE' if n['workforce_gap_full_capacity']>0 else 'PAS_DE_CRISE_NI_SATURATION')
  n['diagnostic_category']=category
  results.append(dict(state=n['state'],owner=n['owner'],population_delta=delta,category=category))
 return dict(categories=dict(C.Counter(r['category'] for r in results)),population_mismatches=[r for r in results if r['population_delta']!=0],static_portions_absent_in_save=[dict(state=r['state'],owner=r['owner']) for r in rows if not any(n['state']==r['state'] and n['owner']==r['owner'] for n in native['states'])],note='A difference can come from initialization scripts, different loaded file versions or simulation. It is not automatically a lost population or a stale save.')

def write_csv(path,rows):
 keys=[k for k,v in rows[0].items() if not isinstance(v,(dict,list))] if rows else []
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)

def dashboard(path,data):
 payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
 template='''<!doctype html><html lang="fr"><meta charset="utf-8"><title>1776 — Terres, emplois et famines</title>
<style>body{font:16px system-ui;background:#132129;color:#e7eeee;margin:30px}h1{font-size:26px}p{max-width:1150px;color:#c3d3dc}input,select,button{font:inherit;padding:8px;background:#233b49;color:white;border:1px solid #7892a2;margin:5px}table{border-collapse:collapse;width:100%;font-size:14px}th{text-align:left;cursor:pointer;background:#2c4552;position:sticky;top:0}td,th{padding:9px;border-bottom:1px solid #39505d}tr:hover{background:#2c4552}.bad{color:#ffa89a}.good{color:#a4d4c5}small{color:#aabfc9}.bar{display:inline-block;height:10px;background:#e2ad6d;max-width:120px}#detail{white-space:pre-wrap;font-size:13px;padding:15px;background:#203743}a{color:#a9d9ff}</style>
<h1>1776 — Terres arables, emplois et famines</h1>
<p>Le manque de capacité d’emploi est un signal à examiner historiquement. La famine observée vient séparément de la sauvegarde du jeu. Ce tableau ne corrige aucun État automatiquement.</p>
<label>Recherche <input id="q" placeholder="Agra, MARATH, France…"></label><select id="mode"><option value="all">Tous les États</option><option value="gap">Manque d’emplois estimé</option><option value="famine">Famines observées en jeu</option><option value="mismatch">Famine sans saturation démontrée</option></select><label>Part de travailleurs : <select id="ratio"><option>.25</option><option selected>.30</option><option>.35</option></select></label><button id="native">Chiffres moteur : activés</button>
<p id="summary"></p><p><small>Terres d’un propriétaire estimées par les provinces habitables, pondérées pour les terres fertiles ; les arrondis de partage et certaines différences de carte restent à contrôler en jeu. Chiffres natifs prioritaires si disponibles. Emplois = capacité à effectif plein, pas embauches garanties. Les cultures et plantations utilisent des terres ; leur production de grain ne se confond pas avec leurs emplois. Les rendements de marché affichés dans le JSON sont avant bonus, intrants et accès au marché. Cliquez sur une ligne pour ses réserves et sources.</small></p>
<table><thead><tr><th data-key="name">État / propriétaire</th><th data-key="population">Habitants</th><th data-key="land">Terres</th><th data-key="farm">Agriculture bâtie</th><th data-key="workers">Travailleurs</th><th data-key="capacity">Emplois possibles</th><th data-key="gap">Écart de capacité</th><th data-key="jobless">Sans emploi moteur</th><th data-key="famine">Famine moteur</th><th>Faim % / grave % lus</th><th>Réserves</th></tr></thead><tbody id="rows"></tbody></table><pre id="detail">Sélectionnez un État pour ses données.</pre>
<script>const DATA=__DATA__;let useNative=true,sortKey='gap',desc=true;const $=x=>document.getElementById(x),fmt=x=>x==null?'—':Math.round(x).toLocaleString('fr-FR'),esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const nr=new Map((DATA.native?.states||[]).map(r=>[r.state+'|'+r.owner,r]));function render(){const rat=Number($('ratio').value),q=$('q').value.toLowerCase(),mode=$('mode').value;let rs=DATA.states.map(r=>{let n=useNative?nr.get(r.state+'|'+r.owner):null;let pop=n?.population??r.population,cap=n?.jobs_full_max??r.total_jobs_max,workers=n?.workforce??pop*rat;return {raw:r,native:n,name:(DATA.names[r.state]||r.state)+' / '+(DATA.names[r.owner]||r.owner)+' ('+r.owner+')',population:pop,land:n?.arable_land??r.arable_owner_estimate,farm:n?.built_agricultural_levels??r.agricultural_levels_max,workers,capacity:cap,gap:Math.max(0,workers-cap),famine:n?.famine_active,warning:r.warnings.length}}).filter(r=>(r.name+' '+r.raw.state).toLowerCase().includes(q)&&(mode==='all'||mode==='gap'&&r.gap>0||mode==='famine'&&r.famine||mode==='mismatch'&&r.famine&&r.gap===0));rs.sort((a,b)=>{let x=a[sortKey],y=b[sortKey];return (typeof x==='string'?x.localeCompare(y):(x||0)-(y||0))*(desc?-1:1)});$('summary').textContent=rs.length+' portions d’État affichées. '+(DATA.native?'Sauvegarde '+DATA.native.date+' : '+DATA.native.famine_states+' crises alimentaires actives.':'Aucune sauvegarde importée : famine non mesurée.');$('rows').innerHTML=rs.map((r,i)=>'<tr data-i="'+i+'"><td>'+esc(r.name)+'</td><td>'+fmt(r.population)+'</td><td>'+fmt(r.land)+'</td><td>'+fmt(r.farm)+'</td><td>'+fmt(r.workers)+'</td><td>'+fmt(r.capacity)+'</td><td class="'+(r.gap?'bad':'good')+'">'+fmt(r.gap)+'</td><td>'+(r.famine===true?'🔴 Oui':r.famine===false?'Non':'Non mesurée')+'</td><td>'+r.warning+'</td></tr>').join('');document.querySelectorAll('tbody tr').forEach(tr=>tr.onclick=()=>{$('detail').textContent=JSON.stringify(rs[+tr.dataset.i],null,2)});}['q','mode','ratio'].forEach(k=>$(k).oninput=render);$('native').onclick=()=>{useNative=!useNative;$('native').textContent='Chiffres moteur : '+(useNative?'activés':'désactivés');render()};document.querySelectorAll('th[data-key]').forEach(t=>t.onclick=()=>{sortKey=t.dataset.key;desc=!desc;render()});render();</script></html>'''
 template=template.replace('famine:n?.famine_active,warning:r.warnings.length','famine:n?.famine_active,jobless:n?.unemployed,warning:r.warnings.length+(n&&!n.history_matches_save_population?1:0)')
 template=template.replace("fmt(r.gap)+'</td><td>'+(r.famine", "fmt(r.gap)+'</td><td>'+fmt(r.jobless)+'</td><td>'+(r.famine")
 template=template.replace("'Non mesurée')+'</td><td>'+r.warning", "'Non mesurée')+'</td><td>'+fmt(r.native?.starving_pct)+' / '+fmt(r.native?.severe_starving_pct)+'</td><td>'+r.warning")
 path.write_text(template.replace('__DATA__',payload),encoding='utf8')

def names(keys):
 result={};pattern=re.compile(r'^\s*([^ :]+):\d*\s+"(.*)"\s*$',re.M)
 for base in [GAME,ROOT]:
  for p in sorted((base/'localization/french').rglob('*.yml')):
   for k,v in pattern.findall(p.read_text(encoding='utf-8-sig',errors='replace')):
    if k in keys:result[k]=v
 return result

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--out',type=Path,default=DEFAULT_OUT,help='New report directory; runtime folders prohibited')
 parser.add_argument('--save-text',type=Path,help='Read-only melted Victoria 3 save; source never modified')
 parser.add_argument('--observations',type=Path,help='Dated UI observations JSON bound to the save SHA-256')
 args=parser.parse_args();out=args.out.resolve()
 if not out.is_relative_to(ROOT/'docs') and not out.is_relative_to(ROOT/'.asset-cache'):parser.error('Report output must be under docs/ or .asset-cache/')
 if (out/'DIAGNOSIS.json').exists():parser.error('Report exists; use a new --out directory to preserve evidence')
 out.mkdir(parents=True,exist_ok=True);c=Catalog();rows=startup(c);thresholds=food_thresholds()
 native=native_save(c,args.save_text) if args.save_text else None
 if args.observations:merge_observations(native,args.observations,thresholds)
 data=dict(schema=1,generated_utc=datetime.now(timezone.utc).isoformat(),states=rows,native=native,names=names({r['state'] for r in rows}|{r['owner'] for r in rows}),thresholds=thresholds,definition_collisions=c.collisions,limitations=['Read-only screening; no automatic runtime patch or historical census validation.','Static employment uses 25/30/35% workforce scenarios, not all inhabitants.','Unspecified PM groups use an envelope; upper bound may include unavailable technologies. No guaranteed hiring or food security.','Duplicate create_building declarations use minimum-to-sum level envelope; native save resolves actual levels.','Owner land is estimated from habitable provinces, with effective prime-land weighting and allocation rounding uncertainty; native arable_land overrides when available.','Food-security POP caches at initial pause may contradict engine famine_manager; native crisis flags and manually observed UI are separate authoritative observations.','Construction, future urban centers, ownership jobs and modifiers can alter static totals.','Full staffing is not proof of inputs, production, wages, market access or qualification.'])
 before={p:h for p,h in c.inputs.items()};changed=[p for p,h in before.items() if digest(p)!=h]
 if changed:raise RuntimeError('Inputs changed during reading; retry with fresh output: '+str(changed))
 data['input_manifest']=before
 data['reconciliation']=reconciliation(rows,native)
 (out/'DIAGNOSIS.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 write_csv(out/'STATES.csv',rows)
 if native:write_csv(out/'RUNTIME_STATES.csv',native['states'])
 # Editable historical follow-up list: unknown dates/numbers remain blank.
 targets=ROOT/'docs/research/population/POPULATION_1776_STATE_TARGETS.csv';prior={}
 if targets.exists():
  with targets.open(encoding='utf-8-sig',newline='') as f:
   for r in csv.DictReader(f):prior[(r.get('state'),r.get('owner'))]=r
 nr={(r['state'],r['owner']):r for r in native['states']} if native else {}
 queue=[]
 for r in rows:
  n=nr.get((r['state'],r['owner']));old=prior.get((r['state'],r['owner']),{})
  priority=1 if n and n['famine_active'] else 2 if (n and n['workforce_gap_full_capacity']>0 or r['job_gap_30']>0) else 3
  queue.append(dict(priority=priority,state=r['state'],owner=r['owner'],famine_observed=n['famine_active'] if n else None,unemployed_observed=n['unemployed'] if n else None,job_gap_scenario30=r['job_gap_30'],population_installed=r['population'],population_save=n.get('population') if n else None,population_history_delta=n.get('population_history_delta') if n else None,arable_owner=n['arable_land'] if n else r['arable_owner_estimate'],legacy_population_evidence=json.dumps(old,ensure_ascii=False),historical_population_1776=None,historical_population_perimeter=None,historical_famine_1776=None,historical_sources=None,decision='REVIEW_PENDING'))
 queue.sort(key=lambda r:(r['priority'],-(r['unemployed_observed'] or r['job_gap_scenario30'] or 0)))
 write_csv(out/'REVIEW_QUEUE.csv',queue)
 dashboard(out/'TABLEAU.html',data)
 print(json.dumps(dict(states=len(rows),robust_capacity_flags=sum(r['screening']=='PRESSION_ROBUSTE' for r in rows),native_states=len(native['states']) if native else 0,native_famines=native['famine_states'] if native else None,report=str(out/'TABLEAU.html')),ensure_ascii=False))

if __name__=='__main__':main()
