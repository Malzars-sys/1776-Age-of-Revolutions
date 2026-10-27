"""Bounded Spanish Louisiana 1776 correction. No bitmap, vanilla or Git writes.

Prepare captures current hashes and a reviewable patch. Apply refuses stale inputs.
Whole-cell corridors implement the player's rule, not surveyed Spanish sovereignty.
"""
import collections as C
import csv,heapq,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from colonies01_frontier import owners,totals
from hbc02_map_candidates import graph
from hbc04_land_links import pair,flood,path
from r8_south_geometry import bitmap
from r8_south_correct import allocate,components,pop_signature
from georeference.model import forward,inverse

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/LOUISIANA-01'
ST='common/history/states/00_states.txt';PP='common/history/pops/05_north_america.txt'
REG='map_data/state_regions/05_north_america.txt'
LOC='gfx/map/map_object_data/generated_map_object_locators_city.txt'
MODEL=ROOT/'docs/reports/map/NORTH_AMERICA_1776/R8-CORRECTIONS-01/GEODETIC_MODEL.json'
LA='STATE_LOUISIANA';AR='STATE_ARKANSAS';MO='STATE_MISSOURI';WF='STATE_WEST_FLORIDA';MS='STATE_MISSISSIPPI'
BRIT={'x4FA3C4','x86BC13','xC1273E'}
CADDO={'x0CF7A4','x1BF244','x71BEC1','xD658E7','xEE0FAA','xEFB99C'}
# Central Mississippi/Missouri basin. Mountain and headwater State Regions are
# only partial-basin claims; overlaps are explicitly recorded, never 1819 lines.
LOU_CLAIMS={LA,AR,MO,'STATE_IOWA','STATE_NEBRASKA','STATE_KANSAS','STATE_OKLAHOMA','STATE_NORTH_DAKOTA','STATE_SOUTH_DAKOTA','STATE_COLORADO','STATE_MONTANA','STATE_WYOMING','STATE_MINNESOTA'}
SITES={
 'New Orleans':(LA,[-90.0715,29.9511]),
 'Natchitoches':(LA,[-93.0863,31.7607]),
 'Arkansas Post 1756-1779 vicinity':(AR,[-91.09,33.92]),
 'Ste Genevieve old town vicinity':(MO,[-90.18,37.94]),
 'St Louis':(MO,[-90.1994,38.627]),
 'St Charles':(MO,[-90.481,38.7887]),
}

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def nodebody(raw,n):return raw[raw.index('{',n.start)+1:n.end-1]

def geometry(a,own,scope):
 colors={int(r[1:],16) for r,v in own.items() if any(s in scope for s,t in v)}
 y,x=np.where(np.isin(a,sorted(colors)));ids,inv,cnt=np.unique(a[y,x],return_inverse=True,return_counts=True)
 sx=np.bincount(inv,weights=x);sy=np.bincount(inv,weights=y)
 centers={f'x{int(v):06X}':[float(sx[i]/cnt[i]),float(sy[i]/cnt[i])] for i,v in enumerate(ids)}
 adj=graph(a,sorted(colors));blocked=set()
 p=ROOT/'map_data/adjacencies.csv';p=p if p.exists() else GAME/'map_data/adjacencies.csv'
 for r in csv.DictReader(p.open(encoding='utf-8-sig'),delimiter=';'):
  if all(r.get(k,'').startswith('x') for k in ['From','To']) and (r.get('Type') in ['sea','impassable'] or r.get('adjacency_rule_name','').strip()):blocked.add(pair(int(r['From'][1:],16),int(r['To'][1:],16)))
 for u in list(adj):
  for v in list(adj[u]):
   if pair(u,v) in blocked:del adj[u][v]
 return centers,adj,blocked

def route(adj,start,goals,centers,model):
 q=[(0,start)];dist={start:0};prev={};end=None
 while q:
  d,u=heapq.heappop(q)
  if d!=dist[u]:continue
  if u in goals:end=u;break
  for v in sorted(adj.get(u,{})):
   lon,lat=map(float,inverse(model,[centers[f'x{v:06X}']])[0])
   river=float(np.interp(lat,[29.95,30.45,31,31.56,32.5,33.5,34.5,35.5,36.5,37.2,38.1,38.7],[-90.07,-91.2,-91.6,-91.4,-91.1,-91.15,-90.6,-89.9,-89.4,-89.5,-90.15,-90.2]))
   nd=d+1+min(abs(lon-river),5)*2
   if nd<dist.get(v,1e30):dist[v]=nd;prev[v]=u;heapq.heappush(q,(nd,v))
 assert end is not None,'No side-adjacent corridor'
 seq=[end]
 while seq[-1]!=start:seq.append(prev[seq[-1]])
 return seq[::-1]

def prepare():
 OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'APPLIED.json').exists()
 baseline=runtime();own=owners();a=bitmap();model=load(MODEL)
 scope={LA,AR,MO,WF,MS};centers,adj,blocked=geometry(a,own,scope)
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))}
 imp={int(r[1:],16) for n in regs.values() for r in provs(n,'impassable')}
 by=C.defaultdict(set)
 for r,v in own.items():
  if len(v)==1:
   s,t=next(iter(v));by[s,t].add(r)
 assert BRIT|CADDO<=by[LA,'LOU']
 selected={r:'LOU' for r in by[LA,'LOU']-BRIT-CADDO}
 allowed={int(r[1:],16) for r,v in own.items() if len(v)==1 and next(iter(v))[0] in {AR,MO}}|{int(r[1:],16) for r in selected}
 allowed-=imp
 ladj={u:{v:c for v,c in ns.items() if v in allowed} for u,ns in adj.items() if u in allowed}
 sites=[];routes=[];goals=set(int(r[1:],16) for r in selected)
 for name,(sid,geo) in SITES.items():
  point=forward(model,[geo])[0]
  eligible=[r for r,v in own.items() if len(v)==1 and next(iter(v))[0]==sid and int(r[1:],16) in allowed]
  # A surveyed native city anchor is preferable for St Louis; all other
  # positions are current-raster, province-scale geographic approximations.
  px,py=map(int,point);sample=f'x{int(a[py,px]):06X}'
  r=sample if sample in eligible else min(eligible,key=lambda r:np.linalg.norm(np.array(centers[r])-point))
  if name=='St Louis':r=scalar(regs[MO].one('city'))
  if name=='New Orleans':
   # Retain the checked native New Orleans port anchor. The regional fit
   # differs by about eight pixels here; do not turn that into a new town site.
   r=scalar(regs[LA].one('port'))
   rel='gfx/map/map_object_data/generated_map_object_locators_port.txt';pp=ROOT/rel if (ROOT/rel).exists() else GAME/rel
   z=next(n for n in parse(text(pp))[0].children('instances')[0].children() if n.one('id')==regs[LA].one('id')).children('position')[0]
   vals=[float(v.value) for v in z.children()];point=np.array([vals[0],a.shape[0]-vals[2]])
   assert f'x{int(a[int(point[1]),int(point[0])]):06X}'==r
  seq=route(ladj,int(r[1:],16),goals,centers,model)
  routes.append(dict(site=name,rgb=[f'x{v:06X}' for v in seq]))
  selected.update({f'x{v:06X}':'LOU' for v in seq});goals.update(seq)
  sites.append(dict(name=name,state=sid,geo=geo,rgb=r,projection=list(map(float,point)),precision='PROVINCE_SCALE_PROXY_NOT_SURVEY'))
 # One riverbank cell otherwise becomes a Quapaw pocket cut off by the
 # compulsory incorporated corridor. This is documented gameplay infill,
 # not a new assertion of Spanish occupation of the entire cell.
 selected['xBA821E']='LOU'
 # British parish corridor is kept in its existing West Florida State Region,
 # preventing a Louisiana-wide claim from implicitly claiming Baton Rouge.
 british=set(BRIT)
 bad={r:(next(iter(own[r]))[0],'CAD') for r in CADDO}
 changes={r:(next(iter(own[r]))[0],t) for r,t in selected.items() if own[r]!={(next(iter(own[r]))[0],t)}}|bad|{r:(WF,'GBR') for r in british}
 final={r:set(v) for r,v in own.items()}
 for r,target in changes.items():final[r]={target}
 # All incorporated colonial shares, not the whole mixed region.
 files={};raw=text(ROOT/ST);nodes=state_nodes(raw);edits=[]
 for sid in [LA,AR,MO,WF]:
  n=nodes[sid];rows=[]
  countries={t for r,v in final.items() for s,t in v if s==sid}
  for t in sorted(countries):
   cells={r for r,v in final.items() if (sid,t) in v}
   old=next((v for v in n.children('create_state') if v.one('country')=='c:'+t),None)
   if old:
    txt=raw[old.start:old.end];sub=old.children('owned_provinces')[0]
    txt=txt[:sub.start-old.start]+'owned_provinces = '+rgb_block(cells)+txt[sub.end-old.start:]
   else:txt='create_state = { country = c:'+t+' owned_provinces = '+rgb_block(cells)+' }'
   if t=='LOU':
    states=parse(txt)[0].children('state_type')
    if states:
     z=states[0];txt=txt[:z.start]+'state_type = incorporated'+txt[z.end:]
    else:txt=txt[:-1]+' state_type = incorporated }'
   rows.append(txt)
  replacements=n.children('create_state');edits += [(v.start,v.end,'\n'.join(rows) if i==0 else '') for i,v in enumerate(replacements)]
 raw=edit(raw,edits);nodes=state_nodes(raw);edits=[];claim_rows=[]
 for sid,n in nodes.items():
  if sid not in LOU_CLAIMS|{MS,'STATE_TEXAS'}:continue
  previous=[scalar(v.value) for v in n.children('add_claim')];claims=set(previous)
  if sid in LOU_CLAIMS:claims.discard('c:USA');claims.add('c:LOU')
  if sid==MS:claims.discard('c:LOU');claims.discard('c:SC1')
  if sid==LA:claims.discard('c:USA')
  if sid=='STATE_TEXAS':claims.discard('c:USA')
  if sorted(claims)!=sorted(previous):
   old=n.children('add_claim');new='\n'.join('add_claim = '+t for t in sorted(claims))
   if old:edits += [(v.start,v.end,new if i==0 else '') for i,v in enumerate(old)]
   else:edits.append((n.end-1,n.end-1,'\n'+new+'\n'))
   claim_rows.append(dict(state=sid,before=previous,after=sorted(claims)))
 raw=edit(raw,edits);nodes=state_nodes(raw);edits=[]
 # Existing Caddo homeland, no invented new tribal TAG.
 if 'cu:caddoan' not in [scalar(v.value) for v in nodes[LA].children('add_homeland')]:edits.append((nodes[LA].end-1,nodes[LA].end-1,'\n add_homeland = cu:caddoan\n'))
 files[ST]=encoded(ROOT/ST,edit(raw,edits))
 # Keep every original cohort identity and total. These allocations are
 # technical placement, expressly not newly claimed historical census counts.
 raw=text(ROOT/PP);ns=state_nodes(raw);edits=[];app=C.defaultdict(list);placements=[]
 src=ns[LA].children('region_state:LOU')[0]
 for n in src.children('create_pop'):
  cu=scalar(n.one('culture'));kind=scalar(n.one('pop_type')) if n.one('pop_type') else None
  moves={MO:1200,AR:300} if cu=='cajun' else ({MO:400,AR:100} if cu=='afro_american' and kind=='slaves' else {})
  if not moves:continue
  old=int(n.one('size'));z=n.children('size')[0];edits.append((z.start,z.end,'size = '+str(old-sum(moves.values()))))
  for sid,count in moves.items():
   block=raw[n.start:n.end];block=block[:z.start-n.start]+'size = '+str(count)+block[z.end-n.start:]
   app[sid].append(block);placements.append(dict(country='LOU',source=LA,destination=sid,culture=cu,pop_type=kind,count=count))
 # Existing Caddo population follows the restored northern Louisiana share,
 # while leaving its old Arkansas share populated; exact within-country sum.
 cad=ns[AR].children('region_state:CAD')[0].children('create_pop')[0];old=int(cad.one('size'));assert old>500
 z=cad.children('size')[0];edits.append((z.start,z.end,'size = '+str(old-500)))
 block=raw[cad.start:cad.end];block=block[:z.start-cad.start]+'size = 500'+block[z.end-cad.start:]
 edits.append((ns[LA].end-1,ns[LA].end-1,'\n region_state:CAD = { '+block+' }\n'))
 placements.append(dict(country='CAD',source=AR,destination=LA,count=500))
 for sid,blocks in app.items():edits.append((ns[sid].end-1,ns[sid].end-1,'\n region_state:LOU = {\n'+'\n'.join(blocks)+'\n }\n'))
 files[PP]=encoded(ROOT/PP,edit(raw,edits))
 # Shift only the three British parish RGBs into West Florida. Conserve all
 # regional resource/arable totals through an explicit coarse capacity split.
 raw=text(ROOT/REG);rs={n.key:n for n in parse(raw)};edits=[];resource_moves=[]
 for sid,cells in [(LA,set(provs(rs[LA],'provinces'))-british),(WF,set(provs(rs[WF],'provinces'))|british)]:
  n=rs[sid].children('provinces')[0];edits.append((n.start,n.end,'provinces = '+rgb_block(cells)))
 amount=13
 for sid,delta in [(LA,-amount),(WF,amount)]:
  n=rs[sid].children('arable_land')[0];edits.append((n.start,n.end,'arable_land = '+str(int(n.value)+delta)))
 for n in rs[LA].children('capped_resources')[0].children():
  move=round(int(n.value)*3/28);dest=rs[WF].children('capped_resources')[0].children(n.key);assert len(dest)==1
  d=dest[0];edits += [(n.start,n.end,n.key+' = '+str(int(n.value)-move)),(d.start,d.end,d.key+' = '+str(int(d.value)+move))]
  resource_moves.append(dict(type=n.key,capacity=move))
 for n in rs[LA].children('resource'):
  kind=n.one('type');dest=next(v for v in rs[WF].children('resource') if v.one('type')==kind)
  for z in n.children():
   if z.key not in ['discovered_amount','undiscovered_amount'] or int(z.value)==0:continue
   move=round(int(z.value)*3/28);d=dest.children(z.key)[0]
   edits += [(z.start,z.end,z.key+' = '+str(int(z.value)-move)),(d.start,d.end,d.key+' = '+str(int(d.value)+move))]
   resource_moves.append(dict(type=kind,field=z.key,capacity=move))
 rice=rs[WF].children('arable_resources')[0];edits.append((rice.end-1,rice.end-1,' building_rice_farm '))
 # Change just the two anachronistic/foreign colonial seats.
 hub_specs=[]
 for sid,name in [(LA,'New Orleans'),(AR,'Arkansas Post 1756-1779 vicinity')]:
  site=next(s for s in sites if s['name']==name);r=site['rgb'];n=rs[sid].children('city')[0]
  edits.append((n.start,n.end,'city = "'+r+'"'))
  ys,xs=np.where(a==int(r[1:],16));point=np.array(site['projection']);i=int(np.argmin((xs-point[0])**2+(ys-point[1])**2));pixel=[int(xs[i]),int(ys[i])]
  hub_specs.append(dict(state=sid,id=int(rs[sid].one('id')),rgb=r,pixel=pixel,name=name))
 files[REG]=encoded(ROOT/REG,edit(raw,edits))
 raw=text(ROOT/LOC);edits=[]
 for n in parse(raw)[0].children('instances')[0].children():
  if n.one('id') is None:continue
  h=next((h for h in hub_specs if h['id']==int(n.one('id'))),None)
  if h:
   z=n.children('position')[0];values=[scalar(v.value) for v in z.children()];values[0]=str(h['pixel'][0]+.25);values[2]=str(a.shape[0]-h['pixel'][1]-.25)
   edits.append((z.start,z.end,'position = { '+' '.join(values)+' }'))
 assert len(edits)==2;files[LOC]=encoded(ROOT/LOC,edit(raw,edits))
 for lang in ['french','english']:
  names=['La Nouvelle-Orléans','Poste des Arkansas'] if lang=='french' else ['New Orleans','Arkansas Post']
  files[f'localization/{lang}/replace/1776_louisiana_seats_l_{lang}.yml']=b'\xef\xbb\xbf'+(f'l_{lang}:\n HUB_NAME_STATE_LOUISIANA_city:0 "{names[0]}"\n HUB_NAME_STATE_ARKANSAS_city:0 "{names[1]}"\n').encode('utf8')
 for rel,data in files.items():
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 dump('BASELINE_RUNTIME.json',baseline);dump('BASELINE_OWNERS.json',{r:sorted(v) for r,v in own.items()})
 dump('PATCH.json',dict(input_sha256={r:baseline.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files},bitmap_sha256=sha(ROOT/'map_data/provinces.png')))
 rows=[dict(rgb=r,before=sorted(own[r]),after=list(target)) for r,target in sorted(changes.items())]
 dump('PLAN.json',dict(date='2026-10-27',transfers=rows,claims=claim_rows,sites=sites,corridors=routes,gameplay_infill=['xBA821E'],hubs=hub_specs,placements=placements,resource_moves=resource_moves,arable_move=13,model=str(MODEL.relative_to(ROOT)),model_sha256=sha(MODEL),final_lou_provinces=len(selected),precision='WHOLE_PROVINCE_REGIONAL_ARBITRATION_AND_PLAYER_GAMEPLAY_CORRIDORS',engine_tested=False))
 assert runtime()==baseline,'Concurrent runtime mutation during preparation'
 render(a,final,sites)
 print(json.dumps(dict(files=len(files),transfers=len(rows),lou_cells=len(selected),by_state=dict(C.Counter(s for r,(s,t) in changes.items() if t=='LOU')),claims_changed=len(claim_rows))))

def render(a,own,sites):
 colors={'LOU':(242,199,57),'GBR':(174,82,93),'CAD':(64,143,133),'QPW':(150,114,167),'OSG':(166,84,88),'COM':(127,115,76),'USA':(85,143,177)}
 x0,y0,x1,y1=1840,1115,2165,1450;b=a[y0:y1,x0:x1];out=np.empty((*b.shape,3),dtype=np.uint8);out[:]=[35,48,56]
 for v in np.unique(b):
  r=f'x{int(v):06X}'
  if r in own:out[b==v]=colors.get(next(iter(own[r]))[1],(103,114,102))
 edge=np.zeros(b.shape,bool);edge[:,1:]|=b[:,1:]!=b[:,:-1];edge[1:]|=b[1:]!=b[:-1];out[edge]=[48,53,48]
 im=Image.fromarray(out).resize((1300,1340),Image.Resampling.NEAREST);canvas=Image.new('RGB',(1300,1470),(35,48,56));canvas.paste(im,(0,90));d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
 d.text((12,10),'1776 — Louisiane espagnole : postes et corridors terrestres',font=font,fill='white');d.text((12,43),'Or : Louisiane ; rose : Britanniques ; autres couleurs : nations autochtones.',font=font,fill='white')
 model=load(MODEL)
 for s in sites:
  x,y=forward(model,[s['geo']])[0];x=(x-x0)*4;y=(y-y0)*4+90
  if 0<x<1250 and 90<y<1420:
   d.ellipse((x-3,y-3,x+3,y+3),fill='white');d.text((x+7,y-8),s['name'].replace(' vicinity',''),font=font,fill='white',stroke_width=2,stroke_fill=(20,25,30))
 d.text((12,1438),'Corridors : concession de jouabilité ; limites régionales approximatives.',font=font,fill='white');canvas.save(OUT/'LOUISIANA_1776.png')

def apply():
 p=load(OUT/'PATCH.json');assert not (OUT/'APPLIED.json').exists()
 assert sha(ROOT/'map_data/provinces.png')==p['bitmap_sha256']
 for r,h in p['input_sha256'].items():assert (sha(ROOT/r) if (ROOT/r).exists() else None)==h,r+' changed'
 for r,h in p['output_sha256'].items():assert sha(OUT/'patch'/r)==h
 for r in p['output_sha256']:
  t=ROOT/r
  if t.exists():b=OUT/'before'/r;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(t.read_bytes())
  t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
 print('Installed Louisiana correction.')

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 else:raise SystemExit('Use --prepare or --apply')
