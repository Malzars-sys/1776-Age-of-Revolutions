"""1776 northern New Spain and pre-company Aleutian trade-post representation.

All limits are whole-province regional approximations. Land corridors are the
player's gameplay concession; the Aleutian maritime exception is explicit.
"""
import collections as C,heapq,io,json,sys,csv
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from northwest01_geometry import OUT,SCOPE,load,dump
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,NATIVE_LAWS
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from colonies01_frontier import owners,totals
from hbc02_map_candidates import graph
from r8_south_correct import allocate,pop_signature,components
from hbc04_land_links import pair
from r8_south_geometry import bitmap
from georeference.model import forward,inverse

ST='common/history/states/00_states.txt';PP='common/history/pops/05_north_america.txt';BB='common/history/buildings/05_north_america.txt';REG='map_data/state_regions/05_north_america.txt';CD='common/country_definitions/00_countries.txt'
AK='STATE_ALASKA';POST='STATE_UNALASKA_TRADING_POST';PREFIX='1776_northwest_frontiers'
# Regional representations, not modern reservations or a claim of a single
# centralized Indigenous government over each area. Existing culture families
# and cohort identities are retained; fine ethnographic POP work is separate.
GROUPS=[
 ('A71','Unangans','Unangan',['inuit'],AK,[171,148,74]),
 ('A72','Sugpiaqs','Sugpiaq',['inuit'],AK,[77,151,145]),
 ('A73','Yupiks','Yupik',['inuit'],AK,[121,166,96]),
 ('A74','Iñupiat','Iñupiat',['inuit'],AK,[119,150,183]),
 ('A75','Dena’ina','Dena’ina',['athabaskan'],AK,[176,107,83]),
 ('A76','Tlingits et Haïdas','Tlingit and Haida',['athabaskan'],AK,[154,107,173]),
 ('C71','Peuples de Californie du Nord','Northern California peoples',['hokan'],'STATE_CALIFORNIA',[130,155,83]),
 ('C72','Peuples de la vallée centrale','Central Valley peoples',['hokan'],'STATE_CALIFORNIA',[175,139,77]),
 ('C73','Peuples de Californie du Sud','Southern California peoples',['hokan'],'STATE_CALIFORNIA',[170,101,114]),
 ('S71','O’odham','O’odham',['oodham'],'STATE_SONORA',[183,161,78]),
 ('S72','Peuples du Colorado','Colorado River peoples',['hokan','paiute','oodham'],'STATE_ARIZONA',[87,156,162]),
 ('S73','Hopis','Hopi',['pueblo'],'STATE_ARIZONA',[151,119,174]),
 ('S74','Seris','Seri',['hokan','oodham'],'STATE_SONORA',[89,148,112]),
 ('T71','Apaches lipans','Lipan Apache',['apache'],'STATE_TEXAS',[175,120,72]),
 ('T72','Tonkawas','Tonkawa',['comanche','apache'],'STATE_TEXAS',[157,143,83]),
 ('T73','Peuples du littoral texan','Texas coastal peoples',['comanche','apache'],'STATE_TEXAS',[105,161,153]),
]
CORE={'STATE_'+s for s in ['BAJA_CALIFORNIA','DURANGO','RIO_GRANDE','SINALOA']}
TARGET=SCOPE-{'STATE_NEVADA','STATE_UTAH'}
CLAIM_SCOPE=TARGET|{'STATE_NEVADA','STATE_UTAH','STATE_WASHINGTON','STATE_OREGON','STATE_BRITISH_COLUMBIA'}
SITES=[
 ('Caborca','STATE_SONORA',[-112.15,30.72]),('Altar','STATE_SONORA',[-111.83,30.71]),('Magdalena','STATE_SONORA',[-110.97,30.62]),('Fronteras','STATE_SONORA',[-109.56,30.90]),
 ('Yuma crossing (corridor only)','STATE_ARIZONA',[-114.62,32.72]),('Tubac','STATE_ARIZONA',[-111.05,31.61]),('San Xavier del Bac','STATE_ARIZONA',[-111.01,32.11]),
 ('San Diego','STATE_CALIFORNIA',[-117.16,32.72]),('San Gabriel','STATE_CALIFORNIA',[-118.105,34.10]),('San Luis Obispo','STATE_CALIFORNIA',[-120.66,35.28]),('San Antonio de Padua','STATE_CALIFORNIA',[-121.237,35.97]),('Monterey','STATE_CALIFORNIA',[-121.90,36.60]),
 ('Janos','STATE_CHIHUAHUA',[-108.19,30.89]),('Casas Grandes','STATE_CHIHUAHUA',[-107.94,30.37]),('El Carrizal','STATE_CHIHUAHUA',[-106.65,30.56]),('El Paso del Norte','STATE_CHIHUAHUA',[-106.48,31.74]),
 ('Albuquerque','STATE_NEW_MEXICO',[-106.65,35.08]),('Socorro (corridor only)','STATE_NEW_MEXICO',[-106.89,34.06]),('Santa Fe','STATE_NEW_MEXICO',[-105.94,35.69]),('Abiquiu','STATE_NEW_MEXICO',[-106.32,36.21]),('Taos','STATE_NEW_MEXICO',[-105.57,36.41]),
 ('Laredo','STATE_TEXAS',[-99.51,27.51]),('San Antonio','STATE_TEXAS',[-98.49,29.43]),('La Bahia','STATE_TEXAS',[-97.39,28.65]),('Bucareli','STATE_TEXAS',[-95.74,31.05]),
]

def natives(s,lon,lat,prior):
 if s in CORE:return 'SC1'
 if s==AK:
  if lon<-160 and lat<56.7:return 'A71'
  if lon>-141 and lat<60.5:return 'A76'
  if lat>66 or lon<-162 and lat>64.7:return 'A74'
  if lon<-157 and lat<65.5:return 'A73'
  if -154<lon<-147 and 60<lat<63.4:return 'A75'
  if lat<61.3:return 'A72'
  return 'ATB'
 if s=='STATE_CALIFORNIA':
  if lat>36.8 and lon<-120.5:return 'C71'
  if lat>34.5 and lon>-121.3:return 'C72'
  return 'C73'
 if s=='STATE_ARIZONA':
  if 35.3<lat<36.6 and -111.3<lon<-109.7:return 'S73'
  if lat>35.5 and lon>-112.5:return 'NVJ'
  if lon<-113 or lat>34.3 and lon<-112:return 'S72'
  if lat<33.5 and lon<-110.5:return 'S71'
  return 'APC'
 if s=='STATE_NEW_MEXICO':return 'NVJ' if lon<-107.4 and lat>34.7 else ('COM' if lon>-104.8 and lat>33.1 else 'APC')
 if s=='STATE_SONORA':
  if 28.8<lat<30.4 and lon<-111.8:return 'S74'
  if lat>29.5 and lon<-111.2:return 'S71'
  if lat>30.0 and lon>-110.0:return 'APC'
  return 'SC1'
 if s=='STATE_CHIHUAHUA':return 'APC' if lat>30.0 or lon>-105.0 and lat>28.8 else 'SC1'
 if s=='STATE_TEXAS':
  if prior in ['CAD','WCH']:return prior
  # Lower Rio Grande settler districts; all other Spanish posts are connected
  # below with explicitly labeled routes, not a blanket modern-Texas border.
  river=float(np.interp(lat,[25.9,26.2,27.5,28.7,29.5,30.2,31.8],[-97.5,-98.5,-99.5,-100.5,-101.2,-104.7,-106.5]))
  if lat<27.7 and lon<river+.5:return 'SC1'
  if lat<30.3 and lon>-98.3:return 'T73'
  if lat<32.5 and lon<-99.3:return 'T71'
  if lat<32.8 and lon>-99.3:return 'T72'
  return 'COM'
 raise ValueError(s)

def find_route(adj,start,goals,positions):
 q=[(0,start)];dist={start:0};previous={};finish=None
 while q:
  d,u=heapq.heappop(q)
  if d!=dist[u]:continue
  if u in goals:finish=u;break
  for v in sorted(adj.get(u,{})):
   cost=d+float(np.linalg.norm(np.array(positions[u])-positions[v]))+1
   if cost<dist.get(v,1e40):dist[v]=cost;previous[v]=u;heapq.heappush(q,(cost,v))
 assert finish is not None,'No passable land connection'
 route=[finish]
 while route[-1]!=start:route.append(previous[route[-1]])
 return route[::-1]

def prepare():
 assert not (OUT/'APPLIED.json').exists();base=runtime();own=owners();a=bitmap();model=load(OUT/'SOUTHWEST_MODEL.json');rows=load(OUT/'PROVINCES.json');defs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))}
 assert base['map_data/provinces.png']==load(OUT/'GEOMETRY_INPUTS.json')['bitmap_sha256']
 # Baseline includes known overlaps; choose the historical representation by
 # position, never simply treat both owners as valid sovereigns.
 desired={};meta={r['rgb']:r for r in rows if r['state'] in TARGET};positions={int(r['rgb'][1:],16):r['pixel'] for r in rows}
 for r,v in meta.items():
  before=own[r];prior='SC1' if any(t=='SC1' for s,t in before) else sorted(t for s,t in before)[0]
  desired[r]=(v['state'],natives(v['state'],*v['geo'],prior))
 desired['xC00000']=(AK,'A71') # This native RGB wraps along the Aleutian chain.
 # Recolor only the existing island component: no new coastline or sea bridge.
 island=load(OUT/'UNALASKA_COMPONENT_CANDIDATE.json');pixels=island['pixels'];newrgb=0xC00001
 assert newrgb not in set(map(int,np.unique(a)));assert all(a[y,x]==0xC00000 for x,y in pixels)
 for x,y in pixels:a[y,x]=newrgb
 rgb=f'x{newrgb:06X}';desired[rgb]=(POST,'ALK');positions[newrgb]=list(np.mean(pixels,axis=0))
 port_candidate=min(pixels,key=lambda p:(p[0]-309)**2+(p[1]-734)**2);px,py=port_candidate
 # Choose a true coastal point on the component near Unalaska Bay.
 seas={int(r[1:],16):int(n.one('id')) for p in effective('map_data/state_regions') if 'sea' in p.name for n in parse(text(p)) for r in provs(n,'provinces')}
 coast=[]
 for x,y in pixels:
  water=[seas.get(int(a[y+dy,x+dx])) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=x+dx<a.shape[1] and 0<=y+dy<a.shape[0]]
  water=[v for v in water if v is not None]
  if water:coast.append((float((x-309)**2+(y-734)**2),x,y,water[0]))
 assert coast;_,px,py,naval=min(coast)
 used={int(n.one('id')) for n in defs.values()};newid=next(v for v in range(3160,9000) if v not in used)
 # Land adjacency respects side contacts and explicit impassable rules.
 outside_core={int(r[1:],16) for r,v in own.items() if any(t=='SC1' for s,t in v) and r not in meta}
 colors={int(r[1:],16) for r in meta if meta[r]['state']!=AK}|outside_core
 yy,xx=np.where(np.isin(a,sorted(outside_core)));ids,inv,cnt=np.unique(a[yy,xx],return_inverse=True,return_counts=True);sx=np.bincount(inv,weights=xx);sy=np.bincount(inv,weights=yy)
 positions.update({int(v):[float(sx[i]/cnt[i]),float(sy[i]/cnt[i])] for i,v in enumerate(ids)})
 adj=graph(a,sorted(colors));imp={int(r[1:],16) for n in defs.values() for r in provs(n,'impassable')};blocked=set()
 ap=ROOT/'map_data/adjacencies.csv';ap=ap if ap.exists() else GAME/'map_data/adjacencies.csv'
 for z in csv.DictReader(ap.open(encoding='utf-8-sig'),delimiter=';'):
  if all(z.get(k,'').startswith('x') for k in ['From','To']) and (z.get('Type') in ['sea','impassable'] or z.get('adjacency_rule_name','').strip()):blocked.add(pair(int(z['From'][1:],16),int(z['To'][1:],16)))
 adj={u:{v:c for v,c in vs.items() if v not in imp and pair(u,v) not in blocked} for u,vs in adj.items() if u not in imp}
 # Every post joins the same capital-connected mainland, not whichever
 # disconnected Spanish remnant happens to be nearest.
 initial_spanish={int(r[1:],16) for r,(s,t) in desired.items() if t=='SC1'}|outside_core
 capital=int(scalar(defs['STATE_MEXICO'].one('city'))[1:],16)
 def closure(cells):
  assert capital in cells;seen={capital};stack=[capital]
  while stack:
   for v in adj.get(stack.pop(),{}):
    if v in cells and v not in seen:seen.add(v);stack.append(v)
  return seen
 goals=closure(initial_spanish);sites=[];routes=[]
 for name,sid,geo in SITES:
  point=forward(model,[geo])[0];x,y=map(int,point);sample=f'x{int(a[y,x]):06X}'
  candidates=[r for r,v in meta.items() if v['state']==sid and int(r[1:],16) in adj]
  r=sample if sample in candidates else min(candidates,key=lambda r:np.linalg.norm(np.array(meta[r]['pixel'])-point))
  seq=find_route(adj,int(r[1:],16),goals,positions)
  for v in seq:
   rr=f'x{v:06X}'
   if rr in meta:desired[rr]=(meta[rr]['state'],'SC1')
  initial_spanish.update(seq);goals=closure(initial_spanish);sites.append(dict(name=name,state=sid,geo=geo,projected=list(map(float,point)),rgb=r,precision='REGIONAL_PROXY_NOT_SURVEYED_POINT'))
  routes.append(dict(site=name,rgb=[f'x{v:06X}' for v in seq],gameplay_concession=True))
 # Keep a country capital in an owned share. Hubs are selected below.
 by=C.defaultdict(set)
 for r,(s,t) in desired.items():by[s,t].add(r)
 for g in GROUPS:assert any(t==g[0] for s,t in by),g[0]+' has no defensible current province'
 files={};raw=text(ROOT/ST);ns=state_nodes(raw);edits=[];claim_changes=[]
 for sid in TARGET:
  n=ns[sid];parts=[]
  for (s,t),cells in sorted(by.items()):
   if s!=sid:continue
   state_type=' state_type = incorporated' if t=='SC1' else ''
   parts.append('create_state = { country = c:'+t+' owned_provinces = '+rgb_block(cells)+state_type+' }')
  old=n.children('create_state');edits += [(v.start,v.end,'\n'.join(parts) if i==0 else '') for i,v in enumerate(old)]
 # Existing central New Spain blocks are retained byte-for-byte when their
 # ownership hasn't changed, instead of normalizing unrelated fields.
 raw=edit(raw,edits);ns=state_nodes(raw);edits=[]
 for sid in CLAIM_SCOPE:
  n=ns[sid];old=[scalar(v.value) for v in n.children('add_claim')];new=set(old)
  if sid==AK:new.discard('c:ALK')
  else:
   new.discard('c:USA');new.add('c:SC1')
   if sid in {'STATE_WASHINGTON','STATE_OREGON','STATE_BRITISH_COLUMBIA'}:new.discard('c:HBC')
  if set(old)!=new:
   claims=n.children('add_claim');replacement='\n'.join('add_claim = '+t for t in sorted(new))
   if claims:edits += [(v.start,v.end,replacement if i==0 else '') for i,v in enumerate(claims)]
   else:edits.append((n.end-1,n.end-1,'\n'+replacement+'\n'))
   claim_changes.append(dict(state=sid,before=old,after=sorted(new)))
 root=parse(raw)[0];edits.append((root.end-1,root.end-1,'\n s:'+POST+' = { create_state = { country = c:ALK state_type = incorporated owned_provinces = { '+rgb+' } } add_claim = c:ALK }\n'))
 files[ST]=encoded(ROOT/ST,edit(raw,edits))
 # Cohorts stay in their original region; ALASKA + POST is one conservation
 # domain. No inflation, culture conversion or loss of religious/type identity.
 raw=text(ROOT/PP);ns=state_nodes(raw);edits=[];ledger=[];newpost=[]
 for sid in TARGET:
  n=ns.get(sid)
  if not n:continue
  buckets=C.defaultdict(list)
  for rs in n.children():
   if not rs.key.startswith('region_state:'):continue
   oldtag=rs.key.split(':')[1]
   for pop in rs.children('create_pop'):
    cu=scalar(pop.one('culture'));count=int(pop.one('size'));candidates={t:len(cells) for (s,t),cells in by.items() if s==sid}
    if sid==AK:
     if cu=='russian':allocation={'ALK':count}
     else:
      # Keep 1,200 inherited inuit-family people at the mixed trading station.
      station=min(1200,count) if oldtag=='ALK' and cu=='inuit' else 0
      eligible={'A71','A72','A73','A74'} if cu=='inuit' else {'ATB','A75','A76'}
      allocation=allocate(count-station,{t:w for t,w in candidates.items() if t in eligible})
      if station:allocation['ALK']=station
    elif cu in ['mexican','afro_caribeno']:allocation={'SC1':count}
    else:
     preferences={'navajo':{'NVJ'},'pueblo':({'S73'} if sid=='STATE_ARIZONA' else {'SC1'}),'apache':({'APC'} if sid!='STATE_TEXAS' else {'T71',oldtag}),'oodham':{'S71','SC1'},'hokan':{'C71','C72','C73','S72','SC1'}}
     eligible=preferences.get(cu,{oldtag} if oldtag in candidates and oldtag not in ['COM','APC'] else set(candidates)-{'SC1'})
     weights={t:w for t,w in candidates.items() if t in eligible}
     if not weights:weights={t:w for t,w in candidates.items() if t!='SC1'} or candidates
     allocation=allocate(count,weights)
    for t,size in allocation.items():
     if not size:continue
     z=pop.children('size')[0];block=raw[pop.start:pop.end];block=block[:z.start-pop.start]+'size = '+str(size)+block[z.end-pop.start:]
     if sid==AK and t=='ALK':newpost.append(block)
     else:buckets[t].append(block)
     ledger.append(dict(state=sid,before=oldtag,after=t,culture=cu,pop_type=pop.one('pop_type'),religion=pop.one('religion'),size=size))
  content='\n'.join('region_state:'+t+' = {\n'+'\n'.join(blocks)+'\n}' for t,blocks in sorted(buckets.items()))
  edits.append((n.start,n.end,'s:'+sid+' = {\n'+content+'\n}'))
 root=parse(raw)[0];edits.append((root.end-1,root.end-1,'\n s:'+POST+' = { region_state:ALK = {\n'+'\n'.join(newpost)+'\n} }\n'))
 files[PP]=encoded(ROOT/PP,edit(raw,edits))
 # Preserve every preexisting building command and economic ownership. Only
 # empty scopes whose old country has left the region may disappear.
 raw=text(ROOT/BB);ns=state_nodes(raw);edits=[]
 for sid in TARGET:
  if sid not in ns:continue
  for rs in ns[sid].children():
   if not rs.key.startswith('region_state:'):continue
   tag=rs.key.split(':')[1]
   if (sid,tag) not in by:
    assert not rs.children('create_building'),sid+' '+tag+' has assets requiring a separate transfer review'
    edits.append((rs.start,rs.end,''))
 root=parse(raw)[0];edits.append((root.end-1,root.end-1,'\n s:'+POST+' = { region_state:ALK = { create_building = { building = building_port level = 1 reserves = 1 activate_production_methods = { pm_aor1776_traditional_commercial_harbor pm_1776_no_raw_data_reporting } } } }\n'))
 files[BB]=encoded(ROOT/BB,edit(raw,edits))
 # Native country initialization, no uniform European technology tier.
 existing={n.key for p in effective('common/country_definitions') for n in parse(text(p))};definitions=[];hist=['COUNTRIES = {'];flags=[];coas=[];locs={'french':['l_french:'],'english':['l_english:']}
 culture_ids={n.key for p in effective('common/cultures') for n in parse(text(p))}
 for tag,fr,en,cultures,capital,color in GROUPS:
  assert tag not in existing and set(cultures)<=culture_ids,(tag,cultures)
  if (capital,tag) not in by:capital=next(s for s,t in by if t==tag)
  definitions.append(tag+' = { color = { '+' '.join(map(str,color))+' } country_type = decentralized tier = principality cultures = { '+' '.join(cultures)+' } religion = animist capital = '+capital+' }')
  hist.append('c:'+tag+' ?= { add_technology_researched = traditional_food_processing\n'+''.join('activate_law = law_type:law_'+law+'\n' for law in NATIVE_LAWS)+' effect_native_conscription_10 = yes }')
  flags.append(tag+' = { flag_definition = { coa = aor1776_northwest_'+tag.lower()+' priority = 100 allow_overlord_canton = no } }')
  coas.append('aor1776_northwest_'+tag.lower()+' = { pattern = "pattern_solid.tga" color1 = "green" colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 0.8 0.8 } } } }')
  for lang,name in [('french',fr),('english',en)]:locs[lang] += [f' {tag}:0 "{name}"',f' {tag}_ADJ:0 "{name}"']
 hist.append('}')
 for folder,content in [('country_definitions',definitions),('history/countries',hist),('flag_definitions',flags),('coat_of_arms/coat_of_arms',coas)]:files[f'common/{folder}/{PREFIX}.txt']=('\n'.join(content)+'\n').encode()
 raw=text(ROOT/CD);n=next(n for n in parse(raw) if n.key=='ALK');z=n.children('capital')[0];files[CD]=encoded(ROOT/CD,edit(raw,[(z.start,z.end,'capital = '+POST)]))
 # No chartered company in 1776; keep later definitions available.
 rh='common/history/countries/rus - russia.txt';raw=text(ROOT/rh);edits=[]
 for n in walk(parse(raw)):
  if n.key=='add_company' and scalar(n.value)=='company_type:company_russian_american_company' or n.key=='company:company_russian_american_company':edits.append((n.start,n.end,''))
 assert len(edits)==2;files[rh]=encoded(ROOT/rh,edit(raw,edits))
 ah='common/history/countries/alk - alyaska.txt';raw=text(ROOT/ah);n=parse(raw)[0].children('c:ALK')[0];files[ah]=encoded(ROOT/ah,edit(raw,[(n.end-1,n.end-1,'\n add_technology_researched = traditional_food_processing\n')]))
 dip='common/history/diplomacy/00_subject_relationships.txt';raw=text(ROOT/dip);ns=[n for n in walk(parse(raw)) if n.key=='create_diplomatic_pact' and n.one('country')=='c:ALK'];assert len(ns)==1;z=ns[0].children('type')[0];files[dip]=encoded(ROOT/dip,edit(raw,[(z.start,z.end,'type = colony')]))
 dyn='common/dynamic_country_names/00_dynamic_country_names.txt';raw=text(ROOT/dyn);n=next(n for n in parse(raw) if n.key=='ALK');edits=[(n.end-1,n.end-1,'\n dynamic_country_name = { name = dyn_c_1776_aleutian_traders adjective = dyn_c_1776_aleutian_traders_adj is_main_tag_only = yes priority = 100 trigger = { current_date < 1799.1.1 } }\n')]
 comp=next(v for v in n.children('dynamic_country_name') if v.one('name')=='dyn_c_russian_american_company');tr=comp.children('trigger')[0];edits.append((tr.end-1,tr.end-1,'\n current_date >= 1799.1.1\n'));files[dyn]=encoded(ROOT/dyn,edit(raw,edits))
 # Province data: split, never add land. Regional capacities conserved.
 raw=text(ROOT/REG);ns={n.key:n for n in parse(raw)};n=ns[AK];arable=int(n.one('arable_land'));assert arable>=2;z=n.children('arable_land')[0];edits=[(z.start,z.end,'arable_land = '+str(arable-2))]
 fish=n.children('capped_resources')[0].children('building_fishing_wharf')[0];assert int(fish.value)>=2;edits.append((fish.start,fish.end,'building_fishing_wharf = '+str(int(fish.value)-2)))
 new='\n'+POST+' = { id = '+str(newid)+' subsistence_building = building_subsistence_fishing_village provinces = { '+rgb+' } city = '+rgb+' port = '+rgb+' farm = '+rgb+' mine = '+rgb+' wood = '+rgb+' arable_land = 2 arable_resources = { building_livestock_ranch } capped_resources = { building_fishing_wharf = 2 } naval_exit_id = '+str(naval)+' }\n'
 hubs=[]
 for sid,name,kind in [('STATE_CALIFORNIA','Monterey','city'),('STATE_CALIFORNIA','Monterey','port'),('STATE_ARIZONA','Tubac','city'),('STATE_TEXAS','San Antonio','city')]:
  site=next(v for v in sites if v['name']==name);r=site['rgb'];ys,xs=np.where(a==int(r[1:],16));point=np.array(site['projected']);j=int(np.argmin((xs-point[0])**2+(ys-point[1])**2));xy=[int(xs[j]),int(ys[j])];z=ns[sid].children(kind)[0];edits.append((z.start,z.end,kind+' = "'+r+'"'));hubs.append(dict(state=sid,id=int(ns[sid].one('id')),kind=kind,rgb=r,pixel=xy,name=name))
 files[REG]=encoded(ROOT/REG,edit(raw,edits)+new)
 for kind in ['city','port','farm','mine','wood']:
  rel=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';raw=text(ROOT/rel if (ROOT/rel).exists() else GAME/rel);instances=parse(raw)[0].children('instances')[0];template=next(n for n in instances.children() if n.one('id')=='269');edits=[]
  for h in [v for v in hubs if v['kind']==kind]:
   n=next(n for n in instances.children() if n.one('id')==str(h['id']));z=n.children('position')[0];vals=[v.value for v in z.children()];vals[0]=str(h['pixel'][0]+.25);vals[2]=str(a.shape[0]-h['pixel'][1]-.25);edits.append((z.start,z.end,'position = { '+' '.join(vals)+' }'))
  newraw=raw[template.start:template.end];z=template.children('position')[0];vals=[v.value for v in z.children()];vals[0]=str(px+.25);vals[2]=str(a.shape[0]-py-.25);local=[(z.start-template.start,z.end-template.start,'position = { '+' '.join(vals)+' }')];z=template.children('id')[0];local.append((z.start-template.start,z.end-template.start,'id = '+str(newid)));newraw=edit(newraw,local)
  edits.append((instances.end-1,instances.end-1,'\n'+newraw+'\n'));p=ROOT/rel if (ROOT/rel).exists() else GAME/rel;files[rel]=encoded(p,edit(raw,edits))
 # Include the new island region in the same strategic area as its parent.
 sr='common/strategic_regions/north_america_strategic_regions.txt';raw=text(ROOT/sr);found=[n for n in walk(parse(raw)) if n.key=='states' and any(v.value==AK for v in n.children())];assert len(found)==1;z=found[0];files[sr]=encoded(ROOT/sr,edit(raw,[(z.end-1,z.end-1,' '+POST+' ')]))
 terrains='map_data/province_terrains.txt';raw=text(ROOT/terrains);z=next(n for n in parse(raw) if n.key.lower()=='xc00000');files[terrains]=encoded(ROOT/terrains,raw+'\n'+rgb+' = '+scalar(z.value)+'\n')
 buf=io.BytesIO();im=Image.fromarray(np.stack([(a>>16)&255,(a>>8)&255,a&255],axis=-1).astype('uint8'));im.save(buf,format='PNG');files['map_data/provinces.png']=buf.getvalue()
 for lang in locs:
  locs[lang] += [f' {POST}:0 "Unalaska"',f' dyn_c_1776_aleutian_traders:0 "'+('Comptoirs russes des Aléoutiennes' if lang=='french' else 'Russian Aleutian Trading Posts')+'"',f' dyn_c_1776_aleutian_traders_adj:0 "'+('des comptoirs russes' if lang=='french' else 'Russian Aleutian')+'"']
  for kind in ['city','port','farm','mine','wood']:locs[lang].append(f' HUB_NAME_{POST}_{kind}:0 "Unalaska"')
  for sid,kind,name in [('STATE_CALIFORNIA','city','Monterey'),('STATE_CALIFORNIA','port','Monterey'),('STATE_ARIZONA','city','Tubac'),('STATE_TEXAS','city','San Antonio')]:locs[lang].append(f' HUB_NAME_{sid}_{kind}:0 "{name}"')
  files[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']=b'\xef\xbb\xbf'+('\n'.join(locs[lang])+'\n').encode('utf8')
 for rel,data in files.items():
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 dump('BASELINE_RUNTIME.json',base);dump('BASELINE_OWNERS.json',{r:sorted(v) for r,v in own.items()});dump('PATCH.json',dict(input_sha256={r:base.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files}))
 dump('PLAN.json',dict(date='2026-10-27',scope=sorted(TARGET),rows=[dict(rgb=r,state=s,after=t,before=sorted(own.get(r,[]))) for r,(s,t) in sorted(desired.items())],sites=sites,corridors=routes,claims=claim_changes,hubs=hubs,groups=GROUPS,new_province=dict(rgb=rgb,source_rgb='xC00000',pixels=pixels,region=POST,id=newid,port_pixel=[px,py],naval_exit=naval),population_ledger=ledger,maritime_exception='Explicit user authorization: Oui, exception maritime pour les îles',status='PREPARED',engine_tested=False))
 assert runtime()==base,'Concurrent runtime change; review before staging'
 print(json.dumps(dict(files=len(files),new_countries=len(GROUPS),new_province=rgb,post_id=newid,by_country=dict(C.Counter(t for s,t in desired.values())),sites=len(sites))))

def apply():
 assert not (OUT/'APPLIED.json').exists();p=load(OUT/'PATCH.json');v=load(OUT/'STAGED_VALIDATION.json');assert v['all_pass']
 for r,h in p['input_sha256'].items():assert (sha(ROOT/r) if (ROOT/r).exists() else None)==h,r+' changed; do not overwrite concurrent work'
 for r,h in p['output_sha256'].items():assert sha(OUT/'patch'/r)==h,r+' patch changed'
 for r in p['output_sha256']:
  target=ROOT/r;original=target if target.exists() else GAME/r
  if original.exists():
   dest=OUT/'before'/r;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(original.read_bytes())
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False,maritime_exception_user_authorized=True))
 print('Installed North-West frontier correction.')

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 else:raise SystemExit('Use --prepare or --apply')
