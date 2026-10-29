"""Current bitmap/hub evidence, with explicit modern-coordinate uncertainty."""
from dp01 import *
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from georeference.model import fit,evaluate,forward
from hbc02_map_candidates import graph
SCOPE=['STATE_BALUCHISTAN','STATE_NORTHERN_BALUCHISTAN','STATE_QUETTA','STATE_PUNJAB','STATE_HILL_PUNJAB','STATE_KASHMIR','STATE_SINDH','STATE_PASHTUNISTAN','STATE_KABUL','STATE_KANDAHAR','STATE_CENTRAL_HIGHLANDS','STATE_HERAT','STATE_BALKH','STATE_SISTAN']
def survey():
 b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};own={r.upper():vs for r,vs in ownership().items()}
 rr={r.upper() for s in SCOPE for r in provs(regs[s],'provinces')};yy,xx=np.where(np.isin(a,[int(r[1:],16) for r in rr]));box=[int(xx.min())-10,int(yy.min())-10,int(xx.max())+11,int(yy.max())+11]
 crop=a[box[1]:box[3],box[0]:box[2]];geo={}
 for c in np.unique(crop):
  r=f'x{int(c):06X}'
  if r.upper() not in rr:continue
  y,x=np.where(crop==c);geo[r]=dict(center=[float(x.mean()+box[0]),float(y.mean()+box[1])],pixels=len(x),bbox=[int(x.min()+box[0]),int(y.min()+box[1]),int(x.max()+box[0]),int(y.max()+box[1])],owners=sorted(own.get(r.upper(),set())))
 names={(r['State_ID'],r['Hub_Type']):r['Hub_Name'] for r in csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig'))}
 locs=[]
 for kind in ['city','port','farm','mine','wood']:
  rel=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';p=ROOT/rel
  if not p.exists():p=GAME/rel
  pos={ident:(float(x),3616-float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',text(p))}
  for s in SCOPE:
   ident=str(regs[s].one('id'))
   if ident not in pos:continue
   x,y=pos[ident];r=f'x{int(a[int(y),int(x)]):06X}'
   locs.append(dict(state=s,kind=kind,name=names.get((s,kind)),pixel=[x,y],sampled_rgb=r,defined_rgb=scalar(regs[s].one(kind)),owners=sorted(own.get(r.upper(),set())),source=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)))
 coords={'Kabul':[69.1723,34.5281],'Kandahar':[65.7101,31.6133],'Herat':[62.1997,34.3482],'Quetta':[67.0011,30.1841],'Kalat':[66.5881,29.0225],'Karachi':[67.0011,24.8608],'Hyderabad':[68.3737,25.3924],'Lahore':[74.3436,31.5497],'Peshawar':[71.5785,34.0151],'Srinagar':[74.8810,34.0857],'Multan':[71.5249,30.1968],'Bahawalpur':[71.6833,29.4],'Gwadar':[62.322,25.1216]}
 controls=[]
 for z in locs:
  if z['name'] in coords:
   controls.append(dict(name=z['name'],geo=coords[z['name']],pixel=z['pixel'],role='CHECK' if z['name'] in ['Kalat','Multan','Quetta','Bahawalpur'] else 'FIT',source='Modern settlement coordinates; current effective named locator, NOT surveyed historic boundary',quality='native_locator_not_surveyed'))
 model=fit(controls,'miller_affine',(a.shape[1],a.shape[0]));ev=evaluate(model,controls)
 sites={**coords,'Mastung':[66.85,29.8],'Khuzdar':[66.61,27.81],'Wad':[66.36,27.35],'Sibi':[67.88,29.55],'Dhadar':[67.65,29.47],'Pishin':[66.99,30.58],'Chaman':[66.45,30.92],'Nushki':[66.02,29.55],'Panjgur':[64.1,26.97],'Turbat/Kech':[63.05,26.0],'Kharan':[65.42,28.58],'Las Bela':[66.31,26.23],'Jammu':[74.87,32.73],'Kangra':[76.27,32.1],'Chamba':[76.13,32.55],'Nurpur':[75.9,32.3],'Patiala':[76.4,30.34],'Sirhind':[76.39,30.64],'Ambala':[76.78,30.38],'Ludhiana':[75.85,30.9],'Jalandhar':[75.58,31.33],'Gujranwala':[74.19,32.16],'Amritsar':[74.87,31.63],'Jhang':[72.32,31.27],'Dera Ghazi Khan':[70.63,30.06],'Dera Ismail Khan':[70.9,31.83],'Attock':[72.37,33.77],'Rawalpindi':[73.05,33.6],'Leh':[77.58,34.16],'Gilgit':[74.31,35.92]}
 targets=[]
 for name,g in sites.items():
  x,y=forward(model,[g])[0];r=f'x{int(a[round(y),round(x)]):06X}';targets.append(dict(name=name,geo=g,pixel=[float(x),float(y)],rgb=r,owners=sorted(own.get(r.upper(),set()))))
 dump('GEOMETRY.json',geo);dump('CURRENT_LOCATORS.json',locs);dump('GEO_CONTROLS.json',controls);dump('GEO_MODEL.json',model);dump('GEO_EVALUATION.json',ev);dump('SITE_PROXIES.json',targets);dump('VIEW_BOX.json',box)
 draw(a,own,targets,box,'CURRENT_MAP.png')
 print(json.dumps(dict(controls=len(controls),evaluation=ev,sites=targets),ensure_ascii=False))
def draw(a,own,sites,box,filename):
 x0,y0,x1,y1=box;crop=a[y0:y1,x0:x1];colors={'DUR':(87,158,165),'PAN':(231,150,54),'KAL':(112,112,192),'MAK':(165,135,101),'SIN':(172,139,91),'KAS':(92,147,76),'BPA':(180,137,185),'HPA':(173,171,95),'PTA':(199,190,76),'LAD':(155,120,123)}
 unique,ix=np.unique(crop,return_inverse=True);pal=[]
 for c in unique:
  vs=own.get(f'X{int(c):06X}',set());t=next(iter(vs))[1] if vs else None;pal.append(colors.get(t,(37,53,64) if t is None else (131,137,132)))
 arr=np.array(pal,np.uint8)[ix].reshape((*crop.shape,3));bd=np.zeros(crop.shape,bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];arr[bd]=arr[bd]//2
 scale=3;im=Image.new('RGB',((x1-x0)*scale,(y1-y0)*scale+85),(29,44,55));im.paste(Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST),(0,45));d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 d.text((10,10),'Durrani / Pendjab — propriétaires actuels et repères approximatifs',font=f,fill='white')
 for z in sites:
  x,y=z['pixel'];x=(x-x0)*scale;y=(y-y0)*scale+45
  d.ellipse((x-2,y-2,x+2,y+2),fill='white');d.text((x+3,y-12),z['name'],font=f,fill='white',stroke_width=2,stroke_fill=(25,35,42))
 d.text((10,im.height-28),'Coordonnées modernes : repérage uniquement ; aucune frontière historique prouvée par ces points.',font=f,fill='white');im.save(OUT/filename)
if __name__=='__main__':survey()
