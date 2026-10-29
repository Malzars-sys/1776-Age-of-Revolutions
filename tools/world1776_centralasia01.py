"""Bounded Central Asian territorial pass, with Durrani interfaces reserved."""
import argparse,json,shutil,csv
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_nordic01 as n
ROOT=n.ROOT;WORLD=n.WORLD;LOT=WORLD/'CENTRAL-ASIA-01'
TAGS=['KHI','BUK','KOK','KZH','OZH','UZH','TRM']
ST=n.STATES
def dump(name,v):
 p=LOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((LOT/name).read_text('utf8'))
def survey():
 LOT.mkdir(exist_ok=True);assert not (LOT/'BEFORE.json').exists(),'Keep captured baseline; do not replay survey.'
 inv=n.b4.inventory();protected=n.hashes()
 dump('BEFORE.json',dict(historical_date='1776-01-01',captured_utc=datetime.now(timezone.utc).isoformat(),inventory=inv,protected=protected))
 for rel in [ST,'common/history/pops/09_central_asia.txt','common/history/pops/14_siberia.txt','common/history/diplomacy/00_subject_relationships.txt']:
  p=LOT/'survey_inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
 cat=n.b.a.catalog('map_data/state_regions');countries=n.b.a.catalog('common/country_definitions')
 states=n.b.a.raw(ROOT/ST);_,pop=n.demographics();regs=[]
 for node in n.b.walk(n.b.parse(states)):
  if not node.key.startswith('s:STATE_'):continue
  parts=node.children('create_state')
  if any(p.one('country').removeprefix('c:') in TAGS for p in parts):regs.append(node.key[2:])
 # Contact only: Durrani cells are never candidates for writing in this pass.
 contacts=['STATE_BALKH','STATE_HERAT','STATE_SINKIANG','STATE_DZUNGARIA','STATE_IRTYSH','STATE_OMSK','STATE_TOBOLSK','STATE_ORENBURG']
 regs=list(dict.fromkeys(regs+[s for s in contacts if s in cat]))
 raw=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
 packed=raw[:,:,0]*65536+raw[:,:,1]*256+raw[:,:,2]
 box=(4900,500,6500,1430);x0,y0,x1,y1=box;a=packed[y0:y1,x0:x1];cells=[];summ=[]
 for sid in regs:
  reg,p=cat[sid];st=n.b.one(states,'s:'+sid)
  summ.append(dict(state=sid,source=p.relative_to(ROOT).as_posix(),parts=[dict(owner=z.one('country')[2:],provinces=len(n.b.a.ids(z,'owned_provinces')),population=pop[sid,z.one('country')[2:]]) for z in st.children('create_state')],hubs={k:reg.one(k) for k in ['city','farm','mine','wood','port']}))
  for c in n.b.a.ids(reg,'provinces'):
   c='x'+c.strip('"')[1:].upper();yy,xx=np.where(a==int(c[1:],16))
   if not xx.size:continue
   cells.append(dict(index=len(cells),RGB=c,state=sid,owners=inv['owners'].get(c,[]),pixels=int(xx.size),centroid=[round(float(xx.mean())+x0,2),round(float(yy.mean())+y0,2)],bbox=[int(xx.min())+x0,int(yy.min())+y0,int(xx.max())+x0,int(yy.max())+y0]))
 dump('TERRITORIAL_INVENTORY.json',summ);dump('GEOMETRY_CELLS.json',cells)
 dump('COUNTRIES.json',[dict(TAG=t,source=str(countries[t][1]),definition=n.b.a.raw(countries[t][1])[countries[t][0].start:countries[t][0].end]) for t in TAGS])
 dump('OWNERSHIP_BOUNDARIES.json',dict(allowed_donors=TAGS,Russian_line_cells='Research and explicit named historical forts only; no indiscriminate Russian strip transfer',reserved_owners=['DUR','KAL','MAK','BHW','PAN','PTA','LAD','D2J','D2K','D2C','D2M','D2U','D2S','D2B','KHR','LBL'],reserved_states=['STATE_BALKH','STATE_HERAT','STATE_PASHTUNISTAN','STATE_CENTRAL_HIGHLANDS','STATE_KABUL','STATE_KANDAHAR','STATE_BALUCHISTAN','STATE_QUETTA','STATE_NORTHERN_BALUCHISTAN','STATE_KASHMIR','STATE_PUNJAB','STATE_HILL_PUNJAB'],reserved_tracking='docs/reports/map/DURRANI_PUNJAB_1776/ (read-only)',prohibited='No Durrani-country node or population pool, no DP territorial/character/economic data, no shared common recipe/graph rewrite.'))
 print(json.dumps(summ,ensure_ascii=False,indent=2));print('Cells',len(cells))
def maps():
 cells=load('GEOMETRY_CELLS.json');owners=n.b4.inventory()['owners'];cat=n.b.a.catalog('common/country_definitions')
 palette={'RUS':(162,185,139),'CHI':(215,186,112),'DUR':(190,157,183)}
 for t in TAGS:
  vals=n.b.a.ids(cat[t][0],'color')
  try:palette[t]=tuple(int(int(v)*.45+255*.55) for v in vals)
  except ValueError:palette[t]=(180,180,180)
 raw=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);pack=raw[:,:,0]*65536+raw[:,:,1]*256+raw[:,:,2]
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 hubs=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')))
 for name,box in [('TURKESTAN',(5250,850,6050,1250)),('KAZAKH',(5100,530,6200,1030))]:
  x0,y0,x1,y1=box;a=pack[y0:y1,x0:x1];lut=np.zeros((1<<24,3),dtype=np.uint8);lut[:]=(224,234,240)
  for c,parts in owners.items():lut[int(c[1:],16)]=palette.get(parts[0][1],(210,210,200))
  ar=lut[a];edge=np.zeros(a.shape,bool);edge[1:]|=a[1:]!=a[:-1];edge[:,1:]|=a[:,1:]!=a[:,:-1];ar[edge]=(110,110,105)
  scale=2;pic=Image.fromarray(ar).resize(((x1-x0)*scale,(y1-y0)*scale));d=ImageDraw.Draw(pic)
  for r in cells:
   x,y=r['centroid']
   if x0<x<x1 and y0<y<y1:d.text(((x-x0)*scale,(y-y0)*scale),str(r['index']),font=font,fill='black',stroke_width=1,stroke_fill='white')
  for h in hubs:
   if h['State_ID'] not in {r['state'] for r in cells}:continue
   x,y=float(h['Locator_X']),float(h['Locator_Y'])
   if x0<x<x1 and y0<y<y1:
    d.ellipse(((x-x0)*scale-3,(y-y0)*scale-3,(x-x0)*scale+3,(y-y0)*scale+3),fill='red');d.text(((x-x0)*scale+3,(y-y0)*scale-16),h['Hub_Name'],font=font,fill='#3f1010',stroke_width=2,stroke_fill='white')
  pic.save(LOT/(name+'_CURRENT.png'))
 print('Maps rendered.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--survey',action='store_true');p.add_argument('--maps',action='store_true');a=p.parse_args()
 if a.survey:survey()
 if a.maps:maps()
