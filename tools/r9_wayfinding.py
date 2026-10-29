"""Render player wayfinding from current ownership/RGB data; no runtime edits."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,sha
from hbc06_integrate import ownership

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/RUNTIME_WAYFINDING_2026-10-29'
def main():
 OUT.mkdir(exist_ok=True)
 source=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
 packed=(source[:,:,0]<<16)|(source[:,:,1]<<8)|source[:,:,2];owners=ownership()
 targets=[('Sacramento','Uruguay — portion brésilienne','x4E1443','BRZ'),('Tabatinga','Pastaza — portion brésilienne','x3C0D20','BRZ'),('Secteur de Chiloé','Araucanie — portion espagnole','x553B3F','SC3'),('Puerto Soledad','Îles de l’Atlantique Sud — portion espagnole','x3020D0','SC4')]
 palette={'BRZ':(103,172,208),'SC2':(238,205,106),'SC3':(238,205,106),'SC4':(238,205,106),'AP7':(231,224,200),'GNI':(217,220,198),'PAT':(231,218,200),'H91':(144,175,126),'GBR':(198,110,108),'FRA':(127,148,201),'NET':(217,159,91)}
 coords=[]
 for name,region,rgb,tag in targets:
  assert any(t==tag for s,t in owners[rgb]),(name,owners[rgb])
  ys,xs=np.where(packed==int(rgb[1:],16));x,y=int(np.median(xs)),int(np.median(ys));coords.append((x,y))
 def render(box,size):
  x0,y0,x1,y1=box;a=packed[y0:y1,x0:x1];im=np.full((*a.shape,3),(35,57,72),np.uint8)
  for c in np.unique(a):
   v=owners.get(f'x{int(c):06X}',set())
   if v:im[a==c]=palette.get(next(iter(v))[1],(148,155,137))
  # Outline state/province geometry without inventing location markers.
  border=np.zeros(a.shape,bool);border[:,1:]|=a[:,1:]!=a[:,:-1];border[1:]|=a[1:]!=a[:-1];im[border]=np.maximum(im[border].astype(int)-25,0)
  return Image.fromarray(im).resize(size,Image.Resampling.NEAREST)
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
 canvas=Image.new('RGB',(1450,1540),(27,40,51));d=ImageDraw.Draw(canvas)
 d.text((25,16),'Où cliquer pour contrôler les petites possessions R9',font=font,fill='white')
 d.text((25,55),'Repères tirés des provinces du mod ; les numéros ne sont pas des villes ajoutées au jeu.',font=small,fill=(219,227,232))
 box=(2250,1800,3700,min(3550,packed.shape[0]));x0,y0,x1,y1=box;mapbox=(25,100,910,1440);mw,mh=mapbox[2]-mapbox[0],mapbox[3]-mapbox[1]
 canvas.paste(render(box,(mw,mh)),mapbox[:2]);d=ImageDraw.Draw(canvas)
 for i,((name,region,rgb,tag),(x,y)) in enumerate(zip(targets,coords),1):
  xx=25+(x-x0)*mw/(x1-x0);yy=100+(y-y0)*mh/(y1-y0)
  d.ellipse((xx-18,yy-18,xx+18,yy+18),fill=(213,61,89),outline='white',width=2);d.text((xx-7,yy-13),str(i),font=bold,fill='white')
  top=110+(i-1)*335;d.text((940,top),f'{i}. {name}',font=bold,fill='white')
  # Region label wraps explicitly to avoid clipping.
  split=region.split(' — ');d.text((940,top+32),split[0],font=small,fill=(248,216,119));d.text((940,top+57),split[1],font=small,fill=(248,216,119))
  radius=[38,80,85,45][i-1];bx=(max(0,x-radius),max(0,y-radius),min(packed.shape[1],x+radius),min(packed.shape[0],y+radius))
  inset=render(bx,(475,220));canvas.paste(inset,(940,top+90));d=ImageDraw.Draw(canvas)
  ix=940+(x-bx[0])*475/(bx[2]-bx[0]);iy=top+90+(y-bx[1])*220/(bx[3]-bx[1]);d.ellipse((ix-9,iy-9,ix+9,iy+9),outline=(255,82,117),width=3)
 d.text((25,1465),'Bleu : Brésil • Jaune : colonies espagnoles • Clair : territoires autochtones • Rouge : repère',font=small,fill='white')
 d.text((25,1500),'Noms régionaux à chercher : Uruguay, Pastaza, Araucanie, Îles de l’Atlantique Sud.',font=small,fill=(248,216,119))
 canvas.save(OUT/'R9_REPERES_JOUEUR.png')
 (OUT/'GEOMETRY_RECEIPT.json').write_text(json.dumps({'inputs':{r:sha(ROOT/r) for r in ['map_data/provinces.png','common/history/states/00_states.txt']},'targets':[dict(number=i,name=t[0],search_region=t[1],rgb=t[2],owner=t[3],bitmap_xy=xy) for i,(t,xy) in enumerate(zip(targets,coords),1)],'runtime_files_modified':[],'source_of_locations':'Existing delivered province proxies, not newly researched precise historical town positions. Chiloé marker is the existing Spanish port hub.'},ensure_ascii=False,indent=2),encoding='utf8')
 print(str(OUT/'R9_REPERES_JOUEUR.png'))
if __name__=='__main__':main()
