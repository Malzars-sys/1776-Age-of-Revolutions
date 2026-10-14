"""MAP2H baseline, native RGB evidence and compact inventories. No primary Git writes."""
import csv,json,re,subprocess,sys,collections as C
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective,values,prov
from map2c_work import ROOT,GAME,sha,source_bitmap,packed,geo_data
from map2e_work import GIT
CONTROL=__import__('pathlib').Path('C:/Users/simeo/.codex/visualizations/2026/09/08/01a080b1-616e-71b2-85c3-0d7759724725')
OUT=ROOT/'docs/reports/map/MAP2H';BASE=OUT/'BASELINE.json'
TARGETS={r['State_ID'] for r in csv.DictReader((ROOT/'docs/reports/map/MAP_1776_9_REGIONS.csv').open(encoding='utf-8-sig')) if r['Region_ID']=='R6_SOUTHEAST_ASIA_OCEANIA'}
def dump(name,data):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def snapshot():
 assert not BASE.exists()
 receipt=json.loads((CONTROL/'checkpoint_map2g_validated_before_map2h/REMOTE_VALIDATION.json').read_text())
 assert receipt['status']=='PASS_REMOTE_EXACT_RESTORATION'
 folders=['common','map_data','gfx','gui','events','localization','music','.metadata']+[f'docs/reports/map/MAP2{x}' for x in 'ABCDEFG']
 hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
 originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names','map_data/state_regions'] for p in (ROOT/f).rglob('*.txt')}
 inv=qa.inventory();assert sum(r['count'] for r in inv['pops'])==835804980
 git={k:subprocess.check_output([GIT,*v],cwd=ROOT,text=True).strip() for k,v in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 dump('BASELINE.json',{'inventory':inv,'originals':originals,'hashes':hashes,'bitmap_sha256':sha(source_bitmap()),'git':git,'backup':receipt,'scope':sorted(TARGETS)})
 raw=subprocess.check_output([GIT,'show','georg3mx-map-rework:common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
 current={n.key:qa.norm(n) for n in cw.walk(cw.parse(originals['common/history/states/00_states.txt'])) if n.key.removeprefix('s:') in TARGETS}
 diff=[n.key for n in cw.walk(cw.parse(raw)) if n.key in current and qa.norm(n)!=current[n.key]]
 dump('COLLABORATOR_COMPARISON.json',{'different_state_scopes':diff,'method':'Read-only comparison; no global merge. Existing workspace corrections are authoritative.'})
 print('Baseline',len(TARGETS),'regions; 835804980 people; duplicates',len(inv['duplicates']),'collaborator differences',diff)
def inspect():
 inv=json.loads(BASE.read_text())['inventory'];rgb=packed(source_bitmap());defs,hubs,names=geo_data()
 ids={n.key:n.one('id') for p in effective(ROOT,GAME,'map_data/state_regions') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
 positions={}
 for kind in ['city','port','wood','farm','mine']:
  p=ROOT/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
  if not p.exists():p=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
  pos={i:(float(x),rgb.shape[0]-float(z)) for i,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',p.read_text(encoding='utf-8-sig'))}
  for sid in TARGETS:
   if ids.get(sid) in pos:
    x,y=pos[ids[sid]];inside=0<=int(y)<rgb.shape[0] and 0<=int(x)<rgb.shape[1]
    positions[sid+'|'+kind]={'x':x,'y':y,'rgb':'x%06X'%rgb[int(y),int(x)] if inside else None,'locator_outside_bitmap':not inside,'selector':hubs[sid].get(kind),'name':names.get('HUB_NAME_'+sid+'_'+kind)}
 wanted={int(v[1:],16) for s in TARGETS for v in defs[s]};rows=[]
 # One pass groups pixels without scanning the full world for each province.
 yy,xx=np.where(np.isin(rgb,list(wanted)));cs=rgb[yy,xx];order=np.argsort(cs);cs=cs[order];xx=xx[order];yy=yy[order]
 unique,starts,counts=np.unique(cs,return_index=True,return_counts=True);owners=C.defaultdict(list)
 for r in inv['owners']:owners[r['key'][0]].append(r['key'][2])
 byrgb={v:s for s,vs in defs.items() for v in vs}
 for c,start,count in zip(unique,starts,counts):
  xs=xx[start:start+count];ys=yy[start:start+count];v='x%06X'%c
  rows.append({'rgb':v,'state':byrgb[v],'owners':owners[v],'pixels':int(count),'box':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'centroid':[float(xs.mean()),float(ys.mean())]})
 dump('GEOGRAPHY.json',{'rgb':rows,'locators':positions})
 print('RGB evidence',len(rows),'records;',len(positions),'physical locators')
def preview(label):
 base=json.loads(BASE.read_text());inv=base['inventory'] if label=='before' else qa.inventory();rgb=packed(source_bitmap());geo=json.loads((OUT/'GEOGRAPHY.json').read_text());owners={r['key'][0]:r['key'][2] for r in inv['owners']}
 colors={t:tuple(int(n[2]) for n in json.loads(body)[2] if False) for t,body in []}
 for tag,body in inv['countries'].items():
  color=next((n[2] for n in json.loads(body)[2] if n[0]=='color'),[])
  try:colors[tag]=tuple(min(255,int(v[2])) for v in color)
  except (ValueError,TypeError):pass
 groups={'indochina':['TONKIN','ANNAM','MEKONG','LAOS','ARAKAN'],'java':['CENTRAL_JAVA','EAST_JAVA'],'mindanao':['MINDANAO'],'micronesia':['WEST_MICRONESIA'],'malaya':['MALAYA'],'papua':['WESTERN_NEW_GUINEA'],'pacific':['HAWAIIAN_ISLANDS'],'tasmania':['TASMANIA'],'aotearoa':['NORTH_ISLAND','SOUTH_ISLAND']}
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 for name,ss in groups.items():
  selected=[r for r in geo['rgb'] if r['state'] in ['STATE_'+s for s in ss]]
  x0=min(r['box'][0] for r in selected)-6;y0=min(r['box'][1] for r in selected)-6;x1=max(r['box'][2] for r in selected)+6;y1=max(r['box'][3] for r in selected)+6
  if name=='aotearoa':x0=7890;x1=8185 # Main islands; inherited wrap-seam fragments remain documented.
  if name=='java':y1=2320 # Offshore dependencies are unchanged, not needed for the court comparison.
  crop=rgb[y0:y1,x0:x1];canvas=np.zeros((*crop.shape,3),dtype=np.uint8)
  for c in np.unique(crop):canvas[crop==c]=colors.get(owners.get('x%06X'%c),(40,63,83))
  bd=np.zeros(crop.shape,dtype=bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];canvas[bd]=(28,31,35)
  scale=max(1,min(5,1000//max(crop.shape)));im=Image.fromarray(canvas).resize((crop.shape[1]*scale,crop.shape[0]*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
  for r in selected:
   if r['pixels']>50:
    x,y=r['centroid']
    if label!='before' and name=='pacific':
     ys,xs=np.where(crop==int(r['rgb'][1:],16));x=x0+float(xs.mean());y=y0+float(ys.mean())
    d.text(((x-x0)*scale,(y-y0)*scale),owners.get(r['rgb'],'UNOWNED'),font=font,fill='white',stroke_fill='black',stroke_width=1,anchor='mm')
  for key,p in geo['locators'].items():
   if key.endswith('|city') and key.split('|')[0] in ['STATE_'+s for s in ss]:
    x,y=p['x'],p['y'];d.text(((x-x0)*scale,(y-y0)*scale),p['name'] or '',font=font,fill='#ffe38a',stroke_fill='black',stroke_width=1)
  im.save(OUT/(name+'_'+label+'.png'))
 print('Preview',label)
if __name__=='__main__':
 op=sys.argv[1]
 if op=='snapshot':snapshot()
 elif op=='inspect':inspect()
 else:preview(op)
