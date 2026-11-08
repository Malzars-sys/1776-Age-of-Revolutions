"""RUSSIA-01: Russian frontier incorporation and native1.15 Cossack access.

Survey is single-use and non-functional. Apply patches current RUS portions only.
No mass ownership changes, technology graph edits, Git writes or vanilla writes.
"""
import argparse,json,shutil,re,csv
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_nordic01 as n
ROOT,WORLD,ST=n.ROOT,n.WORLD,n.STATES
LOT=WORLD/'RUSSIA-01';COUNTRY='common/history/countries/rus - russia.txt'
GAME=n.b.a.GAME;b=n.b
def dump(name,v):
 p=LOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((LOT/name).read_text('utf8'))
def raw(p):return b.a.raw(p)
def survey():
 LOT.mkdir(parents=True,exist_ok=True);assert not (LOT/'BEFORE.json').exists(),'Do not overwrite baseline.'
 inv=n.b4.inventory();protected=n.hashes();dump('BEFORE.json',dict(historical_date='1776-01-01',captured_utc=datetime.now(timezone.utc).isoformat(),inventory=inv,protected=protected))
 for rel in [ST,COUNTRY,'common/defines/00_defines.txt','common/laws/01_colonial_affairs.txt']:
  p=LOT/'survey_inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
 text=raw(ROOT/ST);regs=b.a.catalog('map_data/state_regions');coh,parts=n.demographics();rows=[]
 for state in b.walk(b.parse(text)):
  if not state.key.startswith('s:STATE_'):continue
  for p in state.children('create_state'):
   if p.one('country')!='c:RUS':continue
   sid=state.key[2:];reg,path=regs[sid]
   rows.append(dict(state=sid,state_type=p.one('state_type','incorporated'),state_type_explicit=bool(p.children('state_type')),RGBs=['x'+x.strip('"')[1:].upper() for x in b.a.ids(p,'owned_provinces')],population=parts[sid,'RUS'],other_owners=[dict(TAG=q.one('country')[2:],provinces=len(b.a.ids(q,'owned_provinces'))) for q in state.children('create_state') if q.one('country')!='c:RUS'],hubs={k:reg.one(k) for k in ['city','farm','mine','wood','port']},region_file=str(path)))
 dump('RUSSIAN_PARTS_BEFORE.json',rows)
 for rel in ['common/laws/01_colonial_affairs.txt','common/buildings/15_special.txt','common/building_groups/00_building_groups.txt','common/production_methods/15_special.txt','common/production_method_groups/15_special.txt','common/amendments/00_amendments_ip5_04.txt','common/history/countries/rus - russia.txt','common/defines/00_defines.txt']:
  p=LOT/'native_inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(GAME/rel,p)
 dump('VERSION.json',dict(version_log=raw(Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/logs/system.log')).splitlines()[:2],native= {r: b.a.sha(GAME/r) for r in ['common/laws/01_colonial_affairs.txt','common/buildings/15_special.txt','common/defines/00_defines.txt']}))
 print('Survey',len(rows),'Russian portions;',sum(r['state_type']=='unincorporated' for r in rows),'already unincorporated; world',inv['world_population'])
def inspect_maps():
 rows=load('RUSSIAN_PARTS_BEFORE.json');owners=n.b4.inventory()['owners'];rgb=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);pack=rgb[:,:,0]*65536+rgb[:,:,1]*256+rgb[:,:,2];del rgb
 # Native state identities and current Russian portions, without political claims.
 kinds={c:(1 if r['state_type']=='unincorporated' else 2) for r in rows for c in r['RGBs']};lut=np.zeros((1<<24,3),np.uint8);lut[:]=(226,233,238)
 for color,parts in owners.items():lut[int(color[1:],16)]=(218,215,201)
 for color,kind in kinds.items():lut[int(color[1:],16)]=(219,177,88) if kind==1 else (140,174,128)
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
 for name,box in [('EUROPE',(4450,390,5650,1170)),('SIBERIA',(5500,300,7900,1230)),('PACIFIC',(6800,0,8192,1250))]:
  x0,y0,x1,y1=box;p=pack[y0:y1,x0:x1];colors=lut[p];edge=np.zeros(p.shape,bool);edge[1:]|=p[1:]!=p[:-1];edge[:,1:]|=p[:,1:]!=p[:,:-1];colors[edge]=(130,134,123)
  im=Image.fromarray(colors);d=ImageDraw.Draw(im)
  for r in rows:
   mask=np.isin(p,[int(c[1:],16) for c in r['RGBs']]);yy,xx=np.where(mask)
   if len(xx)>10:d.text((int(xx.mean()),int(yy.mean())),r['state'].removeprefix('STATE_'),font=font,fill='black',stroke_width=2,stroke_fill='white')
  im.save(LOT/(name+'_CURRENT.png'))
 # Special Sakhalin markers must be physically located before any owner proposal.
 for r in rows:
  if r['state']!='STATE_SAKHALIN':continue
  out=[]
  for color in r['RGBs']:
   yy,xx=np.where(pack==int(color[1:],16));out.append(dict(RGB=color,centroid=[float(xx.mean()),float(yy.mean())],bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],pixels=int(xx.size)))
  dump('SAKHALIN_CELL_READING.json',out);print('Sakhalin-labelled Russian cells',out)
 print('Maps rendered.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--survey',action='store_true');p.add_argument('--inspect',action='store_true');a=p.parse_args()
 if a.survey:survey()
 if a.inspect:inspect_maps()
