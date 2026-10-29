"""Arabia 1776: bounded current-workspace survey, then guarded installation."""
import collections as C,csv,json,re,sys,zipfile,unicodedata,datetime
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,state_nodes,ownership,encoded,edit,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from georeference.model import fit,evaluate,forward,inverse
OUT=ROOT/'docs/reports/map/ARABIA_1776/ARABIA-01'
ST='common/history/states/00_states.txt';PP='common/history/pops/08_middle_east.txt'
SCOPE=['STATE_NEJD','STATE_HAIL','STATE_HEDJAZ','STATE_OMAN','STATE_ABU_DHABI','STATE_YEMEN']
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def norm(s):return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('’',"'")
def raster():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);return (a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]
def survey():
 OUT.mkdir(parents=True,exist_ok=True);a=raster();own=ownership();regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};states=state_nodes(text(ROOT/ST));pops=state_nodes(text(ROOT/PP))
 base=OUT/'SURVEY_RUNTIME_MANIFEST.json'
 if not base.exists():dump(base.name,runtime())
 inv=[];rgbs={r for s in SCOPE for r in provs(regs[s],'provinces')};bounds={}
 mask=np.isin(a,np.array([int(r[1:],16) for r in rgbs],np.uint32));yy,xx=np.where(mask);box=[int(xx.min())-15,int(yy.min())-15,int(xx.max())+16,int(yy.max())+16];crop=a[box[1]:box[3],box[0]:box[2]]
 for s in SCOPE:
  inv.append(dict(state=s,hub_definitions={k:regs[s].one(k) for k in ['city','port','farm','mine','wood']},owners=[dict(tag=scalar(n.one('country'))[2:],provinces=len(provs(n,'owned_provinces'))) for n in states[s].children('create_state')],population=[dict(owner=rs.key.split(':')[1],cohorts=[dict(culture=scalar(p.one('culture')),religion=scalar(p.one('religion','DEFAULT')),size=int(p.one('size')),pop_type=scalar(p.one('pop_type','DEFAULT'))) for p in rs.children('create_pop')]) for rs in pops[s].children()]))
 for c in np.unique(crop):
  r=f'x{int(c):06X}'
  if r not in rgbs:continue
  y,x=np.where(crop==c);bounds[r]=dict(center=[float(x.mean()+box[0]),float(y.mean()+box[1])],bbox=[int(x.min()+box[0]),int(y.min()+box[1]),int(x.max()+box[0]),int(y.max()+box[1])],pixels=int(len(x)),owners=sorted(own.get(r,set())))
 dump('CURRENT_INVENTORY.json',inv);dump('PROVINCE_GEOMETRY.json',bounds);dump('VIEW_BOX.json',box)
 # Modern coordinates locate existing named anchors, not historical sovereignty.
 z=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip'
 names={'Riyadh':'Riyadh','Muscat':'Muscat','Manama':'Manama','Aden':'Aden','Mecca':'Mecca','Buraydah':'Buraydah','Salalah':'Salalah','Abu Dhabi':'Abu Dhabi','Sohar':'Sohar','Hail':"Ha'il",'Medina':'Medina','Doha':'Doha','Sur':'Sur','Tabük':'Tabuk','Jiddah':'Jeddah','Sana’a':"Sanaa"}
 geo=[]
 with zipfile.ZipFile(z) as zz:
  for line in zz.read('cities1000.txt').decode().splitlines():
   row=line.split('\t')
   if row[8] in ['SA','OM','BH','AE','YE','QA','KW']:geo.append(row)
 hubs=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')));controls=[];unmatched=[]
 for h in hubs:
  name=h['Hub_Name']
  if h['State_ID'] not in SCOPE or name not in names:continue
  name2=names[name];candidates=[r for r in geo if norm(name2) in [norm(r[1]),norm(r[2])]+[norm(x) for x in r[3].split(',')]]
  candidates=[r for r in candidates if r[6]=='P'];candidates.sort(key=lambda r:int(r[14]),reverse=True)
  x,y=float(h['Locator_X']),float(h['Locator_Y']);rgb=f'x{int(a[int(y),int(x)]):06X}'
  if not candidates or rgb!=h['Defined_Hub_RGB']:unmatched.append(dict(name=name,reason='GeoNames ambiguity/missing or locator RGB mismatch',candidates=[r[1] for r in candidates],sampled=rgb,defined=h['Defined_Hub_RGB']));continue
  r=candidates[0];role='CHECK' if name in ['Buraydah','Manama','Hail','Medina','Sur'] else 'FIT';controls.append(dict(name=name,geo=[float(r[5]),float(r[4])],pixel=[x,y],role=role,quality='native_locator_not_surveyed',geonames_id=r[0],source='retained GeoNames cities1000.zip; current bitmap sampled at native locator'))
 model=fit(controls,'miller_affine',(a.shape[1],a.shape[0]));dump('GEO_CONTROLS.json',dict(controls=controls,excluded=unmatched));dump('GEODETIC_MODEL.json',model);dump('GEODETIC_EVALUATION.json',evaluate(model,controls))
 sites=[('Diriyah',[46.575,24.735]),('Riyadh',[46.6753,24.6877]),('Uyayna',[46.38,24.9]),('Huraymila',[46.13,25.15]),('Shaqra',[45.25,25.25]),('Tharmada',[45.50,25.13]),('Majmaa',[45.33,25.91]),('Dalm',[47.16,23.99]),('Unaizah',[43.99,26.09]),('Buraydah',[43.97,26.36]),('Hail',[41.69,27.52]),('Hofuf',[49.59,25.38]),('Qatif',[50.0,26.57]),('Kuwait',[47.98,29.37]),('Zubarah',[51.03,25.98]),('Manama',[50.58,26.22]),('Doha',[51.53,25.29]),('Sharjah',[55.4,25.35]),('Ras al Khaimah',[55.94,25.79]),('Abu Dhabi',[54.37,24.47]),('Hodeida',[42.95,14.8]),('Sanaa',[44.21,15.35]),('Saada',[43.76,16.94]),('Lahj',[44.88,13.06]),('Aden',[45.03,12.78]),('Mukalla',[49.13,14.54]),('Seiyun',[48.79,15.94]),('Mahra Qishn',[51.68,15.42]),('Muscat',[58.59,23.61]),('Sohar',[56.74,24.35])]
 targets=[]
 for name,g in sites:
  x,y=forward(model,[g])[0];c=f'x{int(a[int(round(y)),int(round(x))]):06X}';targets.append(dict(name=name,geo=g,pixel=[float(x),float(y)],rgb=c,owners=sorted(own.get(c,set())),method='Approximate native-hub calibration; validate against neighbor cells before transfer'))
 dump('SITE_PROXIES.json',targets);preview(own,targets,'CURRENT_ARABIA.png')
 print(json.dumps({'regions':[(r['state'],r['owners']) for r in inv],'controls':len(controls),'excluded':unmatched,'sites':targets},ensure_ascii=False))
def dependencies():
 result=[]
 for folder in ['buildings','military_formations','characters']:
  for p in effective('common/history/'+folder):
   raw=text(p)
   for n in walk(parse(raw)):
    if folder=='buildings' and n.key.startswith('s:') and n.key[2:] in SCOPE:
     for rs in n.children():
      for b in rs.children('create_building'):
       result.append(dict(folder=folder,file=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),state=n.key[2:],owner=rs.key,building=b.one('building'),levels=[z.value for z in walk(b.children()) if z.key=='levels'],PM=provs(b,'activate_production_methods'),line=raw.count('\n',0,b.start)+1))
    elif folder!='buildings' and n.key in ['c:NEJ','c:NBB','c:BHN','c:ZAI','c:JBB','c:HDJ']:
     result.append(dict(folder=folder,file=str(p),country=n.key,line=raw.count('\n',0,n.start)+1,body=raw[n.start:n.end][:2800]))
 dump('CURRENT_DEPENDENCIES.json',result);print(json.dumps(result,ensure_ascii=False))
def plan():
 from hbc02_map_candidates import graph
 import heapq
 a=raster();own=ownership();g=load('PROVINCE_GEOMETRY.json');sites=load('SITE_PROXIES.json');ns=state_nodes(text(ROOT/ST));regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};imp={r for n in regs.values() for r in provs(n,'impassable')}
 allowed={r for r,v in own.items() if len(v)==1 and next(iter(v))[0] in ['STATE_NEJD','STATE_HAIL'] and r not in imp};x0,y0,x1,y1=load('VIEW_BOX.json');adj=graph(a[y0:y1,x0:x1],np.array([int(r[1:],16) for r in allowed],np.uint32))
 def connect(points,permitted):
  result={points[0]}
  for target in points[1:]:
   q=[(0,int(r[1:],16)) for r in result];heapq.heapify(q);cost={c:0 for v,c in q};prev={};t=int(target[1:],16)
   while q:
    d,u=heapq.heappop(q)
    if d!=cost[u]:continue
    if u==t:break
    for v,border in adj[u].items():
     r=f'x{v:06X}'
     if r not in permitted or border<2:continue
     nd=d+1
     if nd<cost.get(v,1e9):cost[v]=nd;prev[v]=u;heapq.heappush(q,(nd,v))
   assert t in cost,('No bounded land connection',target)
   while f'x{t:06X}' not in result:result.add(f'x{t:06X}');t=prev[t]
  return sorted(result)
 # Conservative attested settlement core. Qasim, Dalm/Kharj and Hail excluded.
 points=[next(s['rgb'] for s in sites if s['name']==name) for name in ['Diriyah','Riyadh','Huraymila','Shaqra','Majmaa']]
 permitted={r for r,z in g.items() if z['owners']==[['STATE_NEJD','NBB']] and 5110<=z['center'][0]<=5175 and 1490<=z['center'][1]<=1547 and r not in imp}
 saudi=connect(points,permitted);coast=provs(next(n for n in ns['STATE_HAIL'].children('create_state') if n.one('country')=='c:NBB'),'owned_provinces')
 permitted={r for r,z in g.items() if z['owners'] and z['owners'][0][1]=='NBB' and 5200<=z['center'][0]<=5275 and 1430<=z['center'][1]<=1550 and r not in imp}|set(coast)
 khalid=sorted(set(coast)|set(connect(['x4C5D5F','x04600E','x3F4AE7','x0ACC6B'],permitted)))
 assert not set(saudi)&set(khalid)
 rows=[]
 for r in saudi:rows.append(dict(rgb=r,state='STATE_NEJD',before='NBB',after='NEJ',basis='Diriyah/Riyadh, al-Washm and Sudayr settlement core; bounded whole-province gameplay approximation'))
 for r in khalid:rows.append(dict(rgb=r,state=next(iter(own[r]))[0],before='NBB',after='A91',basis='Banu Khalid al-Hasa/Qatif coastal and oasis core; no Saudi coastal conquest before its late eighteenth-century chronology'))
 for r in ['x2768F8','xEF5020']:rows.append(dict(rgb=r,state='STATE_ABU_DHABI',before='BHN',after='A92',basis='Separate collective Qatari coastal communities, including Utub settlement at Zubarah; not a unified Al Thani or Bahraini emirate'))
 for r in provs(next(n for n in ns['STATE_YEMEN'].children('create_state') if n.one('country')=='c:HDJ'),'owned_provinces'):rows.append(dict(rgb=r,state='STATE_YEMEN',before='HDJ',after='ZAI',basis='Luhayya/Hodeida/Mokha Tihama administration accountable to the Qasimid imam in Niebuhr, not Meccan annexation'))
 for z in rows:assert own[z['rgb']]=={(z['state'],z['before'])}
 after={r:set(v) for r,v in own.items()}
 for z in rows:after[z['rgb']]={(z['state'],z['after'])}
 dump('PLAN.json',dict(date='1776-01-01',scope=SCOPE,transfers=rows,saudi_core=saudi,banu_khalid_core=khalid,bahrain='BHN remains the island governorate under a new Persian subject relation; the island itself does not change owner',new_tags=['A91','A92'],reactivated_tag='NEJ',no_bitmap_or_state_region_change=True,uncertainty='Georeferencing uses native hubs, with no independently established pixel accuracy. Corridors and entire province envelopes are explicit gameplay proxies. No 1800/1810 maximal Saudi extent.'))
 preview(after,sites,'PROPOSED_ARABIA.png');print(json.dumps({'transfers':len(rows),'Saudi':len(saudi),'Banu_Khalid':len(khalid),'Qatar':2,'Yemen':5,'new_tags':['A91','A92']}))
def preview(own,sites,filename):
 a=raster();x0,y0,x1,y1=load('VIEW_BOX.json');crop=a[y0:y1,x0:x1];colors={'NBB':(193,183,108),'JBB':(190,126,111),'NEJ':(101,161,104),'HDJ':(105,191,187),'ZAI':(187,126,73),'LAH':(226,149,148),'MBB':(146,155,95),'KBB':(110,150,111),'OMA':(98,140,180),'ABB':(163,139,171),'BHN':(209,176,113),'PER':(96,160,207),'A91':(189,154,83),'A92':(172,117,140)}
 unique,indices=np.unique(crop,return_inverse=True);pal=[]
 for c in unique:
  vs=own.get(f'x{int(c):06X}',set());t=next(iter(vs))[1] if vs else None;pal.append(colors.get(t,(37,53,64) if t is None else (131,137,132)))
 out=np.array(pal,dtype=np.uint8)[indices].reshape((*crop.shape,3));edge=np.zeros(crop.shape,bool);edge[:,1:]|=crop[:,1:]!=crop[:,:-1];edge[1:]|=crop[1:]!=crop[:-1];out[edge]=out[edge]//2
 scale=2;im=Image.new('RGB',((x1-x0)*scale,(y1-y0)*scale+95),(29,44,55));im.paste(Image.fromarray(out).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST),(0,55));d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);d.text((10,12),'Arabie — propriétaires du mod et repères géographiques approximatifs',font=f,fill='white')
 for z in sites:
  x,y=z['pixel'];x=(x-x0)*scale;y=(y-y0)*scale+55
  d.ellipse((x-3,y-3,x+3,y+3),fill='white');d.text((x+5,y-13),z['name'],font=f,fill='white',stroke_width=2,stroke_fill=(28,40,49))
 d.text((10,im.height-32),'Les repères modernes ne constituent pas des preuves de frontières de 1776.',font=f,fill='white');im.save(OUT/filename)
if __name__=='__main__':
 if '--dependencies' in sys.argv:dependencies()
 elif '--plan' in sys.argv:plan()
 else:survey()
