"""MAP2I immutable local baseline and native-map comparison, without Git writes."""
import collections as C,json,re,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective
from map2c_work import ROOT,GAME,sha,source_bitmap,packed,geo_data
from map2e_work import GIT
CONTROL=Path('C:/Users/simeo/.codex/visualizations/2026/09/08/01a080b1-616e-71b2-85c3-0d7759724725')
OUT=ROOT/'docs/reports/map/MAP2I';BASE=OUT/'BASELINE.json'
SCOPE={'STATE_'+s for s in ['FARS','ISFAHAN','IRAKAJEMI','LURISTAN','PERSIAN_KURDISTAN','URMIA','TABRIZ','MAZANDARAN','GILAN','SEMNAN','KHORASAN','KERMAN','SISTAN','BALUCHISTAN','KHUZESTAN','LARISTAN','BASRA','BAGHDAD','MOSUL','KABUL','KANDAHAR','HERAT','OMAN','ABU_DHABI']}
def dump(name,data):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def capture():
 assert not BASE.exists(),'Do not replace pre-edit baseline'
 receipt=json.loads((CONTROL/'checkpoint_map2h_validated_before_map2i/REMOTE_VALIDATION.json').read_text());assert receipt['status']=='PASS_REMOTE_EXACT_RESTORATION'
 folders=['common','map_data','gfx','events','localization','gui','music','.metadata']+[f'docs/reports/map/MAP2{x}' for x in 'ABCDEFGH']
 hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
 originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names','common/government_types'] for p in (ROOT/f).rglob('*.txt')}
 inv=qa.inventory();assert sum(r['count'] for r in inv['pops'])==835804980 and len(inv['duplicates'])==44
 git={k:subprocess.check_output([GIT,*v],cwd=ROOT,text=True).strip() for k,v in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 dump('BASELINE.json',{'inventory':inv,'originals':originals,'hashes':hashes,'bitmap_sha256':sha(source_bitmap()),'git':git,'backup':receipt})
 raw=subprocess.check_output([GIT,'show','georg3mx-map-rework:common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
 current={n.key:qa.norm(n) for n in cw.walk(cw.parse(originals['common/history/states/00_states.txt'])) if n.key.removeprefix('s:') in SCOPE}
 dump('COLLABORATOR_COMPARISON.json',{'different_scopes':[n.key for n in cw.walk(cw.parse(raw)) if n.key in current and qa.norm(n)!=current[n.key]],'method':'Read-only comparison. No global merge. Current validated Caucasus and Gwadar authoritative.'})
 print('Baseline: 835804980 people, 44 duplicate RGBs, checkpoint',receipt['commit'])
def geometry():
 rgb=packed(source_bitmap());defs,hubs,names=geo_data();wanted={int(v[1:],16) for s in SCOPE if s in defs for v in defs[s]};yy,xx=np.where(np.isin(rgb,list(wanted)));cs=rgb[yy,xx];order=np.argsort(cs);cs=cs[order];xx=xx[order];yy=yy[order];unique,starts,counts=np.unique(cs,return_index=True,return_counts=True);byrgb={v:s for s,vs in defs.items() for v in vs};rows=[]
 for c,i,n in zip(unique,starts,counts):
  xs=xx[i:i+n];ys=yy[i:i+n];v='x%06X'%c;rows.append({'rgb':v,'state':byrgb[v],'pixels':int(n),'box':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'centroid':[float(xs.mean()),float(ys.mean())]})
 ids={s.key:s.one('id') for p in effective(ROOT,GAME,'map_data/state_regions') for s in cw.parse(p.read_text(encoding='utf-8-sig'))};positions={}
 for kind in ['city','port','farm','wood','mine']:
  p=ROOT/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
  if not p.exists():p=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
  pos={i:(float(x),rgb.shape[0]-float(z)) for i,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',p.read_text(encoding='utf-8-sig'))}
  for sid in SCOPE:
   if ids.get(sid) in pos:
    x,y=pos[ids[sid]];positions[sid+'|'+kind]={'x':x,'y':y,'rgb':'x%06X'%rgb[int(y),int(x)],'selector':hubs[sid].get(kind),'name':names.get('HUB_NAME_'+sid+'_'+kind)}
 dump('GEOGRAPHY.json',{'rgb':rows,'locators':positions});print('Native geography',len(rows),'RGBs')
def preview(label):
 base=json.loads(BASE.read_text());inv=base['inventory'] if label=='before' else qa.inventory();rgb=packed(source_bitmap());geo=json.loads((OUT/'GEOGRAPHY.json').read_text());owners={r['key'][0]:r['key'][2] for r in inv['owners']};colors={}
 for tag,body in inv['countries'].items():
  color=next((n[2] for n in json.loads(body)[2] if n[0]=='color'),[])
  try:colors[tag]=tuple(min(255,int(v[2])) for v in color)
  except (ValueError,TypeError):pass
 rows=[r for r in geo['rgb'] if r['state'] in {'STATE_KHORASAN','STATE_SEMNAN','STATE_MAZANDARAN','STATE_SISTAN','STATE_KERMAN','STATE_FARS','STATE_IRAKAJEMI','STATE_ISFAHAN'}];x0=min(r['box'][0] for r in rows)-5;y0=min(r['box'][1] for r in rows)-5;x1=max(r['box'][2] for r in rows)+5;y1=max(r['box'][3] for r in rows)+5;crop=rgb[y0:y1,x0:x1];a=np.zeros((*crop.shape,3),dtype=np.uint8)
 for c in np.unique(crop):a[crop==c]=colors.get(owners.get('x%06X'%c),(35,50,67))
 bd=np.zeros(crop.shape,dtype=bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];a[bd]=(25,29,32);scale=3;im=Image.fromarray(a).resize((crop.shape[1]*scale,crop.shape[0]*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
 for key,p in geo['locators'].items():
  if key.endswith('|city') and x0<p['x']<x1 and y0<p['y']<y1:
   x,y=(p['x']-x0)*scale,(p['y']-y0)*scale;d.ellipse((x-3,y-3,x+3,y+3),fill='white');d.text((x+5,y),p['name']+' ('+owners.get(p['rgb'],'?')+')',font=font,fill='#ffe199',stroke_fill='black',stroke_width=1)
 d.text((12,12),'MAP-2I '+label+' — PER: blue / AFH: plum / DUR: inherited color',font=font,fill='white',stroke_fill='black',stroke_width=1);im.save(OUT/('persia_'+label+'.png'));print('Preview',label)
if __name__=='__main__':{'capture':capture,'geometry':geometry,'before':lambda:preview('before'),'after':lambda:preview('after')}[sys.argv[1]]()
