"""Small immutable baseline and static verification for the MAP2H finish.
No Git writes; source edits are emitted through apply_patch separately.
"""
import collections as C,hashlib,json,re,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from validate_map2f import population_profiles
from map_1776_audit import effective
from map2h_work import ROOT,GAME,GIT,sha,source_bitmap,packed
OUT=ROOT/'docs/reports/map/MAP2H/FINISHING_GOVERNMENTS_NAMES';BASE=OUT/'BASELINE.json'
def dump(name,data):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def capture():
 assert not BASE.exists(),'Do not replace the actual pre-edit checkpoint'
 hashes={p.relative_to(ROOT).as_posix():sha(p) for f in ['common','map_data','gfx','events','localization','gui','music','.metadata'] for p in (ROOT/f).rglob('*') if p.is_file()}
 originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names'] for p in (ROOT/f).rglob('*.txt')}
 inv=qa.inventory();git={k:subprocess.check_output([GIT,*v],cwd=ROOT,text=True).strip() for k,v in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 dump('BASELINE.json',{'hashes':hashes,'originals':originals,'inventory':inv,'git':git})
 print('Captured validated MAP2H: population',sum(r['count'] for r in inv['pops']),'duplicates',len(inv['duplicates']))
def inspect():
 base=json.loads(BASE.read_text());inv=base['inventory'];active={t for _,t in inv['states']};polities={}
 for t,body in inv['countries'].items():
  n=json.loads(body);cultures=next((v[2] for v in n[2] if v[0]=='cultures'),[])
  if t in active and any(v[2]=='aborigine' for v in cultures):
   typ=next(v[2] for v in n[2] if v[0]=='country_type');hist=[]
   for p in effective(ROOT,GAME,'common/history/countries'):
    for c in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))):
     if c.key=='c:'+t:hist.append({'file':str(p),'explicit_laws':[cw.scalar(v.value) for v in c.children('activate_law')]})
   polities[t]={'country_type':typ,'history':hist}
 owners=[r for r in inv['owners'] if r['key'][2] in ['INDOP','KAU']]
 pops=[r for r in inv['regional_pop'] if r['key'][1] in ['INDOP','KAU']]
 units=[r for r in inv['units'] if r['key'][0] in ['INDOP','KAU']]
 buildings=[r for r in inv['buildings'] if r['key'][1] in ['INDOP','KAU']]
 dump('AUDIT.json',{'Australian_Indigenous':polities,'owners':owners,'pops':pops,'units':units,'buildings':buildings})
 print(json.dumps({'Australian_Indigenous':polities,'province_counts':dict(C.Counter(r['key'][1]+'|'+r['key'][2] for r in owners)),'pops':pops,'units':units,'buildings':buildings},ensure_ascii=False,indent=2))
def preview(label):
 base=json.loads(BASE.read_text());inv=base['inventory'] if label=='before' else qa.inventory();geo=json.loads((ROOT/'docs/reports/map/MAP2H/GEOGRAPHY.json').read_text());rgb=packed(source_bitmap());owners={r['key'][0]:r['key'][2] for r in inv['owners']};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
 for name,sids in [('sumatra',['STATE_ACEH','STATE_NORTH_SUMATRA','STATE_SOUTH_SUMATRA']),('borneo',['STATE_WEST_BORNEO','STATE_EAST_BORNEO']),('kaurna',['STATE_SOUTH_AUSTRALIA'])]:
  rows=[r for r in geo['rgb'] if r['state'] in sids];x0=min(r['box'][0] for r in rows)-5;x1=max(r['box'][2] for r in rows)+5;y0=min(r['box'][1] for r in rows)-5;y1=max(r['box'][3] for r in rows)+5
  crop=rgb[y0:y1,x0:x1];a=np.zeros((*crop.shape,3),dtype=np.uint8);colors={'INDOP':(180,151,70),'TOB':(135,87,154),'KLT':(75,149,121),'KAU':(245,212,134)}
  for c in np.unique(crop):a[crop==c]=colors.get(owners.get('x%06X'%c),(41,64,80))
  bd=np.zeros(crop.shape,dtype=bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];a[bd]=(25,29,32)
  scale=max(1,min(4,1000//max(crop.shape)));im=Image.fromarray(a).resize((crop.shape[1]*scale,crop.shape[0]*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
  for r in rows:
   if owners.get(r['rgb']) not in colors:continue
   x,y=r['centroid'];text=r['rgb'] if '--rgb' in sys.argv else owners[r['rgb']]
   d.text(((x-x0)*scale,(y-y0)*scale),text,font=font,fill='white',stroke_fill='black',stroke_width=1,anchor='mm')
  for key,p in geo['locators'].items():
   if key.split('|')[0] in sids and p['name'] and not p['locator_outside_bitmap']:
    x,y=p['x'],p['y'];d.text(((x-x0)*scale,(y-y0)*scale),p['name'],font=font,fill='#ffe198',stroke_fill='black',stroke_width=1)
  im.save(OUT/(name+'_'+label+('_rgb' if '--rgb' in sys.argv else '')+'.png'))
 print('Previews',label)
if __name__=='__main__':
 if sys.argv[1]=='capture':capture()
 elif sys.argv[1]=='inspect':inspect()
 else:preview(sys.argv[1])
