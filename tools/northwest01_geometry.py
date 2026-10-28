"""Read-only localization of existing provinces; no political or bitmap edits."""
import collections as C,csv,json,sys,zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,state_nodes
from validate_diplomacy_ottoman_1776 import parse,scalar
from r8_south_geometry import bitmap,norm
from georeference.model import fit,evaluate,forward,inverse

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/NORTHWEST-01'
SCOPE={'STATE_'+s for s in ['ALASKA','CALIFORNIA','ARIZONA','NEW_MEXICO','TEXAS','SONORA','CHIHUAHUA','DURANGO','RIO_GRANDE','BAJA_CALIFORNIA','SINALOA','NEVADA','UTAH']}
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def main():
 OUT.mkdir(parents=True,exist_ok=True);a=bitmap();defs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};loc={}
 for k in ['city','port','farm','mine','wood']:
  rel=f'gfx/map/map_object_data/generated_map_object_locators_{k}.txt';p=ROOT/rel if (ROOT/rel).exists() else GAME/rel
  for n in parse(text(p))[0].children('instances')[0].children():
   if n.one('id') is None:continue
   vals=[float(z.value) for z in n.children('position')[0].children()];loc[int(n.one('id')),k]=[vals[0],a.shape[0]-vals[2]]
 with zipfile.ZipFile(ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip') as z:records=[r for line in z.read('cities1000.txt').decode().splitlines() if (r:=line.split('\t'))[8] in ['US','MX']]
 aliases={'New Archangel':'Sitka','$Fairbanks$':'Fairbanks','San Quentin':'San Quintín','Santa fe':'Santa Fe','Ruidose':'Ruidoso','Cuauhtemoc':'Ciudad Cuauhtémoc','Cajeme':'Ciudad Obregón','El Paso del Norte':'Ciudad Juárez'}
 controls=[]
 for row in csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')):
  sid,k,name=row['State_ID'],row['Hub_Type'],row['Hub_Name']
  if sid not in SCOPE:continue
  expected=aliases.get(name,name);country='US' if sid in {'STATE_'+s for s in ['ALASKA','CALIFORNIA','ARIZONA','NEW_MEXICO','TEXAS','NEVADA','UTAH']} else 'MX'
  matches=[r for r in records if norm(r[1])==norm(expected) and r[8]==country]
  us_admin={'STATE_ALASKA':'AK','STATE_CALIFORNIA':'CA','STATE_ARIZONA':'AZ','STATE_NEW_MEXICO':'NM','STATE_TEXAS':'TX','STATE_NEVADA':'NV','STATE_UTAH':'UT'}
  if sid in us_admin:matches=[r for r in matches if r[10]==us_admin[sid]]
  mx_admin={'STATE_SONORA':{'26'},'STATE_CHIHUAHUA':{'06'},'STATE_DURANGO':{'10'},'STATE_SINALOA':{'25'},'STATE_BAJA_CALIFORNIA':{'02','03'},'STATE_RIO_GRANDE':{'07','19','28'}}
  if sid in mx_admin:matches=[r for r in matches if r[10] in mx_admin[sid]]
  if sid=='STATE_RIO_GRANDE' and name=='Matamoros':matches=[r for r in matches if float(r[5])>-100]
  if name=='Nogales':matches=[r for r in matches if float(r[4])>30]
  if name=='Jimenez':matches=[r for r in matches if float(r[4])>26]
  if not matches:continue
  rec=max(matches,key=lambda r:int(r[14] or 0));pos=loc[int(defs[sid].one('id')),k];observed=f'x{int(a[int(pos[1]),int(pos[0])]):06X}';defined=scalar(defs[sid].one(k))
  original_pos=list(pos);snap=0
  if observed!=defined:
   if sid=='STATE_ALASKA':dump('ALASKA_EXCLUDED_ANCHOR.json',dict(name=name,defined_rgb=defined,observed_rgb=observed,reason='Native locator does not sample declared province; not moved or used as a fit control.'))
   continue
  fit_city=k=='city' and sid not in {'STATE_SINALOA','STATE_DURANGO','STATE_RIO_GRANDE','STATE_BAJA_CALIFORNIA'}
  controls.append(dict(name=name,state=sid,kind=k,geo=[float(rec[5]),float(rec[4])],pixel=pos,original_locator_pixel=original_pos,snap_pixels=snap,rgb=observed,geonames_id=rec[0],role=('FIT' if (fit_city or sid=='STATE_ALASKA' and k in ['farm','port']) else 'CHECK')))
 for title,rows in [('SOUTHWEST',[r for r in controls if r['state']!='STATE_ALASKA']),('ALASKA',[r for r in controls if r['state']=='STATE_ALASKA'])]:
  m=fit(rows,'miller_affine',a.shape[::-1]);dump(title+'_CONTROLS.json',rows);dump(title+'_MODEL.json',m);dump(title+'_EVALUATION.json',evaluate(m));print(title,len(rows),evaluate(m).get('summary'))
 colors={int(r[1:],16) for sid in SCOPE for r in provs(defs[sid],'provinces')};ys,xs=np.where(np.isin(a,sorted(colors)));ids,inv,cnt=np.unique(a[ys,xs],return_inverse=True,return_counts=True);xx=np.bincount(inv,weights=xs);yy=np.bincount(inv,weights=ys)
 rows=[];south=load(OUT/'SOUTHWEST_MODEL.json');alaska=load(OUT/'ALASKA_MODEL.json')
 by={r:sid for sid in SCOPE for r in provs(defs[sid],'provinces')}
 for i,v in enumerate(ids):
  r=f'x{int(v):06X}';sid=by[r];p=[float(xx[i]/cnt[i]),float(yy[i]/cnt[i])];geo=list(map(float,inverse(alaska if sid=='STATE_ALASKA' else south,[p])[0]));rows.append(dict(rgb=r,state=sid,pixel=p,geo=geo,pixels=int(cnt[i])))
 dump('PROVINCES.json',rows);dump('GEOMETRY_INPUTS.json',dict(bitmap_sha256=sha(ROOT/'map_data/provinces.png'),method='Native named hubs, empirical Miller affine; not surveyed historical borders. Alaska western extrapolation requires island-shape cross-check.'))
 # Show projected islands and their candidate RGBs for manual coastline review.
 im=Image.open(ROOT/'map_data/provinces.png').convert('RGB');pts=[]
 for name,geo in [('Unalaska',[-166.529,53.873]),('Kodiak',[-152.407,57.79]),('Attu',[173.18,52.87])]:
  p=forward(alaska,[geo])[0];x,y=map(int,p);r=f'x{int(a[y,x]):06X}' if 0<=x<a.shape[1] and 0<=y<a.shape[0] else None;pts.append(dict(name=name,geo=geo,pixel=list(map(float,p)),sampled_rgb=r))
 dump('ALASKA_SITE_PROXIES.json',pts);print('AK SITES',json.dumps(pts))
 # Political-neutral colored raster, with province colors and centroids.
 x0,y0,x1,y1=0,330,1500,1320;im=im.crop((x0,y0,x1,y1));d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
 for p in pts:
  x,y=p['pixel'];d.ellipse((x-5,y-y0-5,x+5,y-y0+5),fill='white');d.text((x+8,y-y0),p['name'],font=font,fill='white',stroke_width=2,stroke_fill='black')
 im.save(OUT/'ALASKA_LOCALIZATION.png')

if __name__=='__main__':main()
