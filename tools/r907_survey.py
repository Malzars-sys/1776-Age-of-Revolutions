"""R9-07 read-only geographic survey; modern anchors locate, never prove rule."""
import csv,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,effective,provs
from hbc06_integrate import ownership,text
from validate_diplomacy_ottoman_1776 import parse
from georeference.model import fit,evaluate,forward,inverse
OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-07'
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def main():
 hubs=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')))
 coords={'Asunción':[-57.635,-25.264],'Resistencia':[-58.986,-27.451],'Santa Fe':[-60.7,-31.63],'Santiago del Estero':[-64.261,-27.795],'Pozo Colorado':[-58.797,-23.493],'Mariscal Estigarribia':[-60.61,-22.03],'Monte Quemado':[-62.83,-25.805],'Formosa':[-58.178,-26.185],'Corrientes':[-58.831,-27.469],'Rosario':[-60.639,-32.946],'Córdoba':[-64.188,-31.42]}
 controls=[]
 for r in hubs:
  if r['Hub_Name'] in coords:
   controls.append(dict(name=r['Hub_Name'],state=r['State_ID'],geo=coords[r['Hub_Name']],pixel=[float(r['Locator_X']),float(r['Locator_Y'])],role='CHECK' if r['Hub_Name'] in ['Monte Quemado','Rosario','Formosa'] else 'FIT'))
 model=fit(controls,'miller_affine',(8192,3616));dump('GEODETIC_CONTROLS.json',controls);dump('GEODETIC_MODEL.json',model);dump('GEODETIC_EVALUATION.json',evaluate(model,controls))
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];own=ownership()
 regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))}
 sids=['STATE_CHACO','STATE_ALTO_PARAGUAY','STATE_BAJO_PARAGUAY','STATE_SANTA_FE','STATE_SOUTH_ATLANTIC_ISLANDS']
 rows=[]
 for sid in sids:
  for r in provs(regs[sid],'provinces'):
   yy,xx=np.where(a==int(r[1:],16));cen=[float(xx.mean()),float(yy.mean())]
   rows.append(dict(state=sid,rgb=r,owners=sorted(own.get(r,[])),centroid=cen,geo=inverse(model,[cen])[0].tolist(),pixels=int(len(xx)),bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],impassable=r in provs(regs[sid],'impassable')))
 dump('CURRENT_PROVINCE_SURVEY.json',rows)
 sites={'Concepción 1773':[-57.435,-23.407],'Belén 1760':[-57.26,-23.466],'San Fernando abandonné 1773':[-58.986,-27.451],'San Javier 1743':[-59.93,-30.58],'San Jerónimo / arroyo del Rey':[-59.65,-29.14],'San Pedro mocoví':[-60.3,-30.4],'Timbó 1763':[-58.35,-26.25],'Santiago del Estero':coords['Santiago del Estero'],'Salta':[-65.41,-24.785],'Asunción':coords['Asunción']}
 points=[]
 for name,g in sites.items():
  x,y=forward(model,[g])[0];r=f'x{int(a[round(y),round(x)]):06X}';points.append(dict(name=name,geo=g,pixel=[float(x),float(y)],rgb=r,owners=sorted(own.get(r,[])),precision='Approximate point identification; no historical boundary'))
 dump('SITES.json',points)
 box=(2570,2500,2860,2890);x0,y0,x1,y1=box;scale=3;crop=a[y0:y1,x0:x1];rgb=np.full((*crop.shape,3),[35,48,59],dtype='uint8');colors={'GNI':(90,157,116),'SC4':(207,147,75),'SC3':(153,106,73),'BRZ':(176,160,58)}
 for c in np.unique(crop):
  o=own.get(f'x{int(c):06X}',set());tag=next(iter(o))[1] if len(o)==1 else '';rgb[crop==c]=colors.get(tag,(35,48,59))
 edges=np.zeros(crop.shape,bool);edges[1:,:]|=crop[1:,:]!=crop[:-1,:];edges[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edges]//=2
 im=Image.fromarray(rgb).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
 for z in points:
  x,y=z['pixel'];x=(x-x0)*scale;y=(y-y0)*scale;d.ellipse((x-3,y-3,x+3,y+3),fill='white');d.text((x+5,y),z['name'],font=font,fill='white',stroke_width=2,stroke_fill='black')
 im.save(OUT/'CURRENT_CHACO_SURVEY.png');print(json.dumps({'controls':len(controls),'sites':points,'islands':[r for r in rows if r['state']=='STATE_SOUTH_ATLANTIC_ISLANDS']},ensure_ascii=False))
if __name__=='__main__':main()
