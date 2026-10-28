"""Read-only runtime audit and geometric evidence for CENTRAL-01."""
import collections as C, json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from audit_hbc_1776 import ROOT, GAME, effective, provs, sha, runtime
from hbc06_integrate import text, state_nodes
from validate_diplomacy_ottoman_1776 import parse, scalar
from colonies01_frontier import owners
from georeference.model import fit, evaluate, forward, inverse

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/CENTRAL-01'
CENTRAL={'STATE_'+s for s in ['YUCATAN','CHIAPAS','SAN_SALVADOR','GUATEMALA','HONDURAS','NICARAGUA','COSTA_RICA','PANAMA']}
ISLANDS={'STATE_'+s for s in ['WESTERN_CUBA','CENTRAL_CUBA','EASTERN_CUBA','HAITI','SANTO_DOMINGO','PUERTO_RICO','BAHAMAS','WEST_INDIES','JAMAICA','BERMUDA']}
SCOPE=CENTRAL|ISLANDS
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 assert not (OUT/'APPLIED.json').exists(),'Baseline already installed: do not overwrite its audit.'
 if not (OUT/'BASELINE_RUNTIME.json').exists():dump('BASELINE_RUNTIME.json',runtime())
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p)) if n.key in SCOPE}
 own=owners();states=state_nodes(text(ROOT/'common/history/states/00_states.txt'))
 rows=[]
 for sid,n in regs.items():
  for r in provs(n,'provinces'):
   y,x=np.where(a==int(r[1:],16));rgb='x'+r[1:].upper()
   rows.append(dict(state=sid,rgb=rgb,owners=sorted(own.get(rgb,[])),pixels=len(x),pixel=[float(np.mean(x)),float(np.mean(y))],bbox=[int(x.min()),int(y.min()),int(x.max()),int(y.max())]))
 loc={}
 for kind in ['city','port','farm','mine','wood']:
  rel=Path('gfx/map/map_object_data/generated_map_object_locators_'+kind+'.txt');path=ROOT/rel if (ROOT/rel).exists() else GAME/rel;raw=text(path)
  for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\}',raw):
   loc[int(m[1]),kind]=dict(pixel=[float(m[2]),a.shape[0]-float(m[4])],file=str(path),line=raw.count('\n',0,m.start())+1)
 # Modern place coordinates are geodetic controls, not historical authority.
 anchors=[('Merida','STATE_YUCATAN',[-89.6237,20.9674]),('San Salvador','STATE_SAN_SALVADOR',[-89.1872,13.6894]),('Guatemala City','STATE_GUATEMALA',[-90.5069,14.6349]),('Tegucigalpa','STATE_HONDURAS',[-87.2068,14.0723]),('Managua','STATE_NICARAGUA',[-86.2362,12.1149]),('San Jose','STATE_COSTA_RICA',[-84.0907,9.9281]),('Panama City','STATE_PANAMA',[-79.5199,8.9824]),('Belize port','STATE_GUATEMALA',[-88.1962,17.5046])]
 controls=[]
 for name,sid,geo in anchors:
  k='port' if name=='Belize port' else 'city';d=loc[int(regs[sid].one('id')),k];px=d['pixel'];rgb=f'x{int(a[int(px[1]),int(px[0])]):06X}'
  controls.append(dict(name=name,geo=geo,role='CHECK' if name in ['San Salvador','Belize port'] else 'FIT',state=sid,rgb=rgb,declared_rgb=scalar(regs[sid].one(k)),**d))
 model=fit(controls,'miller_affine',a.shape[::-1]);dump('GEODETIC_CONTROLS.json',controls);dump('GEODETIC_MODEL.json',model);dump('GEODETIC_EVALUATION.json',evaluate(model))
 for r in rows:r['geo']=inverse(model,[r['pixel']])[0].tolist()
 dump('PROVINCES.json',rows)
 inventory=[]
 pops={};assets=C.defaultdict(list)
 for p in effective('common/history/pops'):
  for s,n in state_nodes(text(p)).items():
   if s in SCOPE:
    for rs in n.children():
     key=(s,rs.key.split(':')[-1]);prior=pops.get(key,dict(total=0,cultures=[],files=[]))
     pops[key]=dict(total=prior['total']+sum(int(z.one('size')) for z in rs.children('create_pop')),cultures=sorted(set(prior['cultures'])|{scalar(z.one('culture')) for z in rs.children('create_pop')}),files=prior['files']+[str(p)])
 for p in effective('common/history/buildings'):
  for s,n in state_nodes(text(p)).items():
   if s in SCOPE:
    for rs in n.children():
     for z in rs.children('create_building'):assets[s,rs.key.split(':')[-1]].append(dict(building=scalar(z.one('building')),level=z.one('level'),file=str(p)))
 for s in sorted(SCOPE):
  if s not in states:continue
  inventory.append(dict(state=s,claims=[v.value for v in states[s].children('add_claim')],shares=[dict(tag=scalar(z.one('country'))[2:],provinces=len(provs(z,'owned_provinces')),state_type=z.one('state_type'),population=pops.get((s,scalar(z.one('country'))[2:]),{}),buildings=assets[s,scalar(z.one('country'))[2:]]) for z in states[s].children('create_state')]))
 dump('INVENTORY.json',inventory)
 # Detailed whole-province visual, no ownership changes.
 bounds=[1800,1350,2900,2030];x0,y0,x1,y1=bounds;crop=a[y0:y1,x0:x1];rgb=np.full((*crop.shape,3),[33,47,57],dtype=np.uint8)
 palette={'SC1':[235,185,57],'SC2':[213,145,56],'MKT':[73,168,159],'GBR':[188,109,146],'FRA':[101,145,209],'NET':[228,139,67],'SPA':[215,177,86],'DENNOR':[185,82,84],'HAI':[100,130,209],'GR5':[221,171,76],'PCO':[221,171,76],'CUB':[221,171,76]}
 for r in rows:
  col=palette.get(r['owners'][0][1] if r['owners'] else '',[105,116,93]);rgb[crop==int(r['rgb'][1:],16)]=col
 edge=np.zeros(crop.shape,dtype=bool);edge[1:]|=crop[1:]!=crop[:-1];edge[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edge]=[40,50,51]
 im=Image.fromarray(rgb).resize((1650,1020));draw=ImageDraw.Draw(im)
 for r in rows:
  x,y=r['pixel']
  if x0<x<x1 and y0<y<y1:draw.text(((x-x0)*1.5,(y-y0)*1.5),r['rgb'][1:],fill='white',stroke_width=1,stroke_fill='black')
 im.save(OUT/'BASELINE_MAP.png');dump('PREVIEW_BOUNDS.json',bounds)
 print(json.dumps({'regions':len(inventory),'provinces':len(rows),'geodetic':evaluate(model)},ensure_ascii=False))
if __name__=='__main__':main()
