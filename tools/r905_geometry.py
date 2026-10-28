"""R9-05 diagnostic routes. Existing whole provinces, never a cadastral proof.

Routes preserve the user's connected-post gameplay rule. A river traffic route
does not establish continuous colonial government of every selected province.
"""
import json,heapq,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,provs
from hbc06_integrate import ownership,text,state_nodes
from hbc02_map_candidates import graph
from georeference.model import forward,inverse
from audit_hbc_1776 import effective
from validate_diplomacy_ottoman_1776 import parse

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-05'
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def main():
 img=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(img[:,:,0]<<16)|(img[:,:,1]<<8)|img[:,:,2]
 own=ownership();model=load('GEODETIC_MODEL.json');allowed={int(r[1:],16) for r,v in own.items() if len(v)==1 and next(iter(v))[0] in ['STATE_AMAZONAS','STATE_MATO_GROSSO','STATE_PASTAZA','STATE_PARA','STATE_GOIAS','STATE_ECUADOR','STATE_CAJAMARCA']}
 regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))}
 impassable={int(r[1:],16) for n in regs.values() for r in provs(n,'impassable')}
 adj=graph(a,np.array(sorted(allowed-impassable),dtype=np.uint32));centers={};sizes={};anchors=[]
 # Restrict raster work to the region, with an explicit halo for connections.
 crop=a[1850:2650,2180:3130]
 for c in np.unique(crop):
  if int(c) in allowed:
   yy,xx=np.where(crop==c);centers[int(c)]=np.array([xx.mean()+2180,yy.mean()+1850]);sizes[int(c)]=int(len(xx))
 def sample(g,permitted):
  x,y=forward(model,[g])[0];original=int(a[int(round(y)),int(round(x))])
  if original in permitted:return original
  # No invisible corridor through an engine-impassable river/forest token.
  # Keep the historical target and the bounded adjacent playable proxy separate.
  x0,y0=int(x)-16,int(y)-16;window=a[y0:y0+33,x0:x0+33];yy,xx=np.where(np.isin(window,list(permitted)))
  assert len(xx),'No nearby passable historical-site proxy'
  i=np.argmin((xx+x0-x)**2+(yy+y0-y)**2);delta=float(np.hypot(xx[i]+x0-x,yy[i]+y0-y));assert delta<=12,(g,delta)
  result=int(window[yy[i],xx[i]]);anchors.append(dict(geo=g,predicted=[float(x),float(y)],original_rgb=f'x{original:06X}',proxy_rgb=f'x{result:06X}',proxy_pixel=[int(xx[i]+x0),int(yy[i]+y0)],distance_px=delta,reason='Adjacent passable token; no change to impassable data'))
  return result
 def guide(geo):
  xy=forward(model,geo);pts=[]
  for aa,bb in zip(xy[:-1],xy[1:]):
   pts.extend(np.linspace(aa,bb,max(2,int(np.linalg.norm(bb-aa)))))
  return np.array(pts)
 def route(name,geo,sids,river_names=()):
  allowed0={c for c in centers if c not in impassable and next(iter(own[f'x{c:06X}']))[0] in sids};start=sample(geo[0],allowed0);end=sample(geo[-1],allowed0);assert start in allowed0 and end in allowed0,(name,f'{start:06X}',f'{end:06X}')
  pts=guide(geo)
  if river_names:
   rivers=json.loads((ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson').read_text())['features'];low=np.min(geo,axis=0)-[.6,.6];high=np.max(geo,axis=0)+[.6,.6];extra=[]
   for f in rivers:
    if f['properties'].get('name') not in river_names or f['geometry']['type']!='LineString':continue
    pp=np.array(f['geometry']['coordinates']);pp=pp[np.all((pp>=low)&(pp<=high),axis=1)]
    if len(pp):extra.extend(forward(model,pp).tolist())
   # Modern river geometry supplies routing proximity, not historical possession.
   if extra:pts=np.vstack([pts,np.array(extra)])
  dist={c:float(np.min(np.linalg.norm(pts-centers[c],axis=1))) for c in allowed0}
  queue=[(0,start)];cost={start:0};prev={}
  while queue:
   d,u=heapq.heappop(queue)
   if d!=cost[u]:continue
   if u==end:break
   for v,border in adj[u].items():
    if v not in allowed0 or border<2:continue
    nd=d+1+(dist[v]/10)**2+np.linalg.norm(centers[u]-centers[v])/40
    if nd<cost.get(v,float('inf')):cost[v]=nd;prev[v]=u;heapq.heappush(queue,(nd,v))
  assert end in cost,name
  path=[end]
  while path[-1]!=start:path.append(prev[path[-1]])
  path.reverse();return dict(name=name,geo=geo,rgb=[f'x{c:06X}' for c in path],routing_status='GAMEPLAY_APPROXIMATION_ON_EXISTING_LAND_PROVINCES',guide='Modern physical rivers plus documented historical endpoints; not a cadastral boundary')
 routes=[]
 # Main stem: each documented settlement is a forced waypoint. No shortcut
 # across a large forest can substitute for reaching the historical sites.
 stem=[('Tabatinga',[-69.94,-4.23]),('Olivença',[-68.87,-3.38]),('Ega',[-64.71,-3.35]),('Coari',[-63.14,-4.08]),('Barra',[-60.021,-3.119]),('Serpa',[-58.44,-3.14]),('Obidos',[-55.52,-1.92])]
 for (n1,g1),(n2,g2) in zip(stem[:-1],stem[1:]):routes.append(route('AMAZONAS '+n1+'–'+n2,[g1,g2],['STATE_AMAZONAS','STATE_PASTAZA','STATE_PARA'],['Amazonas']))
 negro=[('Barra',[-60.021,-3.119]),('Barcelos',[-62.926,-.974]),('São Gabriel',[-67.09,-.13]),('Marabitanas',[-67.40,1.10])]
 for (n1,g1),(n2,g2) in zip(negro[:-1],negro[1:]):routes.append(route('NEGRO '+n1+'–'+n2,[g1,g2],['STATE_AMAZONAS'],['Rio Negro']))
 routes.append(route('BRANCO axe de ravitaillement',[[ -61.85,-1.42],[-61.2,.3],[-61.0,1.8],[-60.495,3.015]],['STATE_AMAZONAS'],['Branco']))
 routes.append(route('MADEIRA Barra–Borba',[[-60.021,-3.119],[-59.59,-4.39]],['STATE_AMAZONAS'],['Madeira']))
 routes.append(route('MATO GROSSO Vila Bela–Cuiabá',[[-59.951,-15.008],[-58.3,-15.2],[-56.097,-15.601]],['STATE_MATO_GROSSO']))
 routes.append(route('GOIÁS raccord terrestre documenté 1736–1737',[[-56.097,-15.601],[-54.7,-15.9],[-52.3,-15.9],[-50.14,-15.934]],['STATE_MATO_GROSSO','STATE_GOIAS']))
 # Maynas missions: riverine network and access to the Spanish Andean cores.
 routes.append(route('MAYNAS Borja–Omaguas',[[-77.54,-4.47],[-76.8,-4.45],[-75.6,-4.8],[-74.5,-4.5],[-73.426,-4.297]],['STATE_PASTAZA'],['Marañón','Amazonas']))
 routes.append(route('MAYNAS Jeberos–Yurimaguas',[[-76.28,-5.28],[-76.08,-5.90]],['STATE_PASTAZA']))
 routes.append(route('MAYNAS Borja–Jeberos',[[-77.54,-4.47],[-76.28,-5.28]],['STATE_PASTAZA']))
 routes.append(route('MAYNAS Andoas',[[-76.4,-2.90],[-76.7,-3.7],[-76.8,-4.45]],['STATE_PASTAZA']))
 routes.append(route('MAYNAS rattachement occidental',[[-77.54,-4.47],[-77.7,-4.8],[-76.971,-6.035]],['STATE_PASTAZA','STATE_CAJAMARCA']))
 # A route's missing links may be joined only inside its already documented
 # basin. This explicit connector avoids disconnected BRANCO/MADEIRA branches.
 portuguese=set(r for row in routes if not row['name'].startswith('MAYNAS') for r in row['rgb'])
 # Keep the native and actual city tokens together where the inherited Manaus
 # hub definition and locator differ. Do not silently rewrite either source.
 ns=state_nodes(text(ROOT/'common/history/states/00_states.txt'))
 portuguese.add(regs['STATE_AMAZONAS'].one('city').strip('"'))
 # No other provinces are taken automatically merely because they adjoin a road.
 spanish=set(r for row in routes if row['name'].startswith('MAYNAS') for r in row['rgb'])
 # Bounded mid/upper Tapajós sector. A regional native aggregate, not an ethnic
 # polygon: contemporary attacks and resistance disprove uniform colonial rule.
 # Retain lower-river town/farm/wood/port/mine hubs and all existing buildings.
 # Select only existing cells intersected by the middle/upper river, rather
 # than cutting an invented rectangular ethnic territory from the forest.
 # Outside this conservative core, no conclusion is installed by this pass.
 native_tokens=set()
 riverdata=json.loads((ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson').read_text())['features']
 for f in riverdata:
  if f['properties'].get('name')!='Tapajós' or f['geometry']['type']!='LineString':continue
  pp=np.array(f['geometry']['coordinates']);xy=forward(model,pp)
  for ga,gb,aa,bb in zip(pp[:-1],pp[1:],xy[:-1],xy[1:]):
   for g,point in zip(np.linspace(ga,gb,max(2,int(np.linalg.norm(bb-aa)*2))),np.linspace(aa,bb,max(2,int(np.linalg.norm(bb-aa)*2)))):
    if not (-58.1<g[0]<-55.4 and -8.4<g[1]<-3.4):continue
    x,y=map(int,point);r=f'x{int(a[y,x]):06X}'
    if own.get(r)=={('STATE_PARA','BRZ')}:native_tokens.add(r)
 native_para=sorted(native_tokens)
 assert native_para
 reserved_hubs={regs['STATE_PARA'].one(k).strip('"') for k in ['city','port','farm','mine','wood']}
 assert not (set(native_para)&(reserved_hubs|portuguese))
 result={}
 for sid in ['STATE_AMAZONAS','STATE_MATO_GROSSO','STATE_PASTAZA','STATE_PARA']:
  current={r:t for r,vs in own.items() for s,t in vs if s==sid}
  target=dict(current)
  for r in portuguese&set(current):target[r]='BRZ'
  if sid=='STATE_PASTAZA':
   for r in current:
    if r not in portuguese:target[r]='SC2' if r in spanish else 'AP7'
  if sid=='STATE_PARA':
   for r in native_para:target[r]='AP7'
  result[sid]=dict(before=current,after=target)
 dump('GEOMETRY_PROPOSAL.json',dict(routes=routes,regions=result,native_para=native_para,passable_site_proxies=anchors,warning='Historical endpoints documented; connecting whole provinces are explicit gameplay approximations. Read and visually inspect before installing.'))
 for sid,v in result.items():
  from collections import Counter
  print(sid,Counter(v['after'].values()),'changes',sum(t!=v['before'][r] for r,t in v['after'].items()))
 # Diagnostic overview uses full current ownership with the proposed changes.
 new={r:next(iter(v))[1] for r,v in own.items() if len(v)==1}
 for v in result.values():new.update(v['after'])
 x0,y0,x1,y1=2250,1950,3020,2540;crop=a[y0:y1,x0:x1];rgb=np.full((*crop.shape,3),[34,47,58],dtype='uint8');colors={'BRZ':(227,190,75),'AP7':(100,145,100),'SC3':(182,93,73),'SC2':(120,139,191)}
 for c in np.unique(crop):rgb[crop==c]=colors.get(new.get(f'x{int(c):06X}'),(75,83,83))
 edge=np.zeros(crop.shape,bool);edge[1:,:]|=crop[1:,:]!=crop[:-1,:];edge[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edge]//=2
 im=Image.fromarray(rgb).resize((1540,1180),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
 for s in load('SITES.json'):
  x,y=s['pixel'];x=(x-x0)*2;y=(y-y0)*2
  if 0<=x<im.width and 0<=y<im.height:d.ellipse((x-3,y-3,x+3,y+3),fill='white');d.text((x+5,y-14),s['name'],font=font,fill='white',stroke_width=2,stroke_fill='black')
 im.save(OUT/'R905_PROPOSAL.png')
if __name__=='__main__':main()
