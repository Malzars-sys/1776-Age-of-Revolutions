"""Russian1776 decentralisation: current geometry, bounded political proxies.

No incorporation-only patch. No Git, vanilla, SERG or unrelated owner writes.
"""
import argparse,json,re,shutil,csv,difflib
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_russia01 as r
ROOT,LOT,b,n,ST=r.ROOT,r.LOT,r.b,r.n,r.ST
raw,dump,load=r.raw,r.dump,r.load
REGIONS=['STATE_NENETSIA','STATE_OB','STATE_KOLYMA','STATE_CHUKOTKA']
POPS=['common/history/pops/14_siberia.txt','common/history/pops/15_russia.txt']
AI='common/ai_strategies/00_default_strategy.txt'
PREFIX='1776_world_russia01'
HOSTS=['STATE_ROSTOV','STATE_URALSK','STATE_SAMARA','STATE_ASTRAKHAN']
NTECH=['improved_husbandry','traditional_food_processing','organized_textile_production','organized_workshops']
EXISTING=[ST,r.COUNTRY,AI]+POPS

def geo():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
 pack=a[:,:,0]*65536+a[:,:,1]*256+a[:,:,2];del a
 values,inverse,counts=np.unique(pack,return_inverse=True,return_counts=True)
 inv=inverse.reshape(pack.shape);del inverse
 count=len(values);xx=np.broadcast_to(np.arange(pack.shape[1]),pack.shape);yy=np.broadcast_to(np.arange(pack.shape[0])[:,None],pack.shape)
 sx=np.bincount(inv.ravel(),weights=xx.ravel(),minlength=count);sy=np.bincount(inv.ravel(),weights=yy.ravel(),minlength=count)
 xmin=np.full(count,pack.shape[1]);xmax=np.zeros(count,int);ymin=np.full(count,pack.shape[0]);ymax=np.zeros(count,int)
 np.minimum.at(xmin,inv,xx);np.maximum.at(xmax,inv,xx);np.minimum.at(ymin,inv,yy);np.maximum.at(ymax,inv,yy)
 owners=n.b4.inventory()['owners'];cat=b.a.catalog('map_data/state_regions');rows=[]
 geo={int(v):dict(center=[round(float(sx[j]/counts[j]),2),round(float(sy[j]/counts[j]),2)],bbox=[int(xmin[j]),int(ymin[j]),int(xmax[j]),int(ymax[j])],pixels=int(counts[j])) for j,v in enumerate(values)}
 for sid in REGIONS:
  reg,path=cat[sid]
  for color in b.a.ids(reg,'provinces'):
   color='x'+color.strip('"')[1:].upper();d=geo[int(color[1:],16)]
   rows.append(dict(index=len(rows),RGB=color,state=sid,owners=owners.get(color),**d))
 dump('FRONTIER_CELLS.json',rows)
 hubs=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')))
 dump('FRONTIER_HUBS.json',[h for h in hubs if h['State_ID'] in REGIONS])
 render(owners,'BEFORE',pack,hubs,True)
 print('Frontier cells',len(rows))
 for sid in REGIONS:
  z=[q for q in rows if q['state']==sid];print(sid,'bbox',min(q['bbox'][0] for q in z),min(q['bbox'][1] for q in z),max(q['bbox'][2] for q in z),max(q['bbox'][3] for q in z))

BOXES={'NORTH_WEST':(4850,0,6030,620),'NORTH_EAST':(6800,40,8192,780)}
PALETTE={'RUS':(150,181,132),'NNT':(228,180,101),'CKC':(142,192,212),'CHI':(213,192,154)}
def render(owners,name,pack=None,hubs=None,indices=False):
 if pack is None:
  a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);pack=a[:,:,0]*65536+a[:,:,1]*256+a[:,:,2]
 if hubs is None:hubs=load('FRONTIER_HUBS.json')
 tags=sorted({p[0][1] for p in owners.values()});ids={t:i+1 for i,t in enumerate(tags)};lut=np.zeros(1<<24,np.int16)
 for color,parts in owners.items():lut[int(color[1:],16)]=ids[parts[0][1]]
 palette=np.full((len(tags)+1,3),(217,213,201),np.uint8);palette[0]=(222,234,243)
 for tag,color in PALETTE.items():
  if tag in ids:palette[ids[tag]]=color
 rivers=np.asarray(Image.open(ROOT/'map_data/rivers.png').convert('RGB'))
 for title,box in BOXES.items():
  x0,y0,x1,y1=box;p=pack[y0:y1,x0:x1];code=lut[p];ar=palette[code]
  edge=np.zeros(p.shape,bool);edge[1:]|=code[1:]!=code[:-1];edge[:,1:]|=code[:,1:]!=code[:,:-1];ar[edge]=(60,66,64)
  if indices:
   pe=np.zeros(p.shape,bool);pe[1:]|=p[1:]!=p[:-1];pe[:,1:]|=p[:,1:]!=p[:,:-1];ar[pe&~edge]=(119,141,114)
  rr=rivers[y0:y1,x0:x1];water=(rr[:,:,2]>rr[:,:,0]+20)&(rr[:,:,0]<240);ar[water]=(93,159,199)
  im=Image.fromarray(ar).resize(((x1-x0)*2,(y1-y0)*2),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
  if indices:
   for row in load('FRONTIER_CELLS.json'):
    x,y=row['center']
    if x0<x<x1 and y0<y<y1:d.text(((x-x0)*2,(y-y0)*2),str(row['index']),font=f,fill='#152218',stroke_width=1,stroke_fill='white')
  for h in hubs:
   x,y=float(h['Locator_X']),float(h['Locator_Y'])
   if x0<x<x1 and y0<y<y1:
    px,py=(x-x0)*2,(y-y0)*2;d.ellipse((px-4,py-4,px+4,py+4),fill='red');d.text((px+5,py-12),h['Hub_Name'],font=f,fill='#3f1010',stroke_width=2,stroke_fill='white')
  d.rectangle((0,0,im.width,34),fill='white');d.text((10,6),title+' — '+name+' | RUS vert / Nenets ocre / Tchouktches bleu',font=f,fill='black')
  im.save(LOT/(title+'_'+name+'.png'))

def plan():
 """Select an explicit reviewed native envelope; not a historical cadastral fit.

 Nenets tundra beyond the Pechora/Ob settlement axes. Do not transfer Novaya
 Zemlya, Pustozersk, Mezen, Obdorsk, Berezov, or any Bashkir/Khanty province
 merely for being indigenous. Chukotka already belongs to CKC.
 """
 class Poly:
  def __init__(self,points):self.points=points
  def contains_point(self,p):
   x,y=p;inside=False
   for (ax,ay),(bx,by) in zip(self.points,self.points[1:]+self.points[:1]):
    if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:inside=not inside
   return inside
 cells=load('FRONTIER_CELLS.json');by={x['RGB']:x for x in cells}
 # Mainland tundra: south edge is a deliberately coarse native-cell interface,
 # north of Pustozersk and the lower-Pechora axis; no drawn rectangular border.
 west=Poly([(5204,235),(5230,206),(5270,184),(5330,168),(5395,160),(5460,166),(5520,184),(5580,210),(5637,245),(5630,274),(5590,290),(5550,302),(5500,306),(5450,298),(5400,287),(5360,274),(5325,252),(5290,242),(5250,240)])
 # Yamal/Gydan north of the Obdorsk river approach. Preserve the lower Ob
 # settlement corridor; no implicit declaration of all Khanty lands independent.
 east=Poly([(5590,0),(5995,0),(5995,260),(5955,275),(5900,280),(5840,277),(5780,267),(5740,260),(5710,261),(5675,277),(5645,280),(5620,268),(5600,245),(5580,210),(5570,160)])
 rows=[]
 for sid,poly in [('STATE_NENETSIA',west),('STATE_OB',east)]:
  selected=[c for c in cells if c['state']==sid and c['owners']==[[sid,'RUS']] and poly.contains_point(c['center'])]
  # Keep offshore islands intact. Their permanent1776 settlement is not proved;
  # neither modern Nenets administrative districts nor this polygon assigns them.
  a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
  pack=a[:,:,0]*65536+a[:,:,1]*256+a[:,:,2];del a
  region_cells={int(c['RGB'][1:],16) for c in cells if c['state']==sid};adj=defaultdict(set)
  yy,xx=np.where(np.isin(pack,list(region_cells)));p=pack[yy.min():yy.max()+1,xx.min():xx.max()+1]
  edges=np.concatenate([np.stack([p[1:].ravel(),p[:-1].ravel()],axis=1),np.stack([p[:,1:].ravel(),p[:,:-1].ravel()],axis=1)])
  for aa,bb in np.unique(edges,axis=0):
   aa,bb=int(aa),int(bb)
   if aa in region_cells and bb in region_cells and aa!=bb:adj[aa].add(bb);adj[bb].add(aa)
  remaining=set(region_cells);components=[]
  while remaining:
   seed=remaining.pop();todo=[seed];component={seed}
   while todo:
    z=todo.pop();more=adj[z]&remaining;remaining-=more;component|=more;todo.extend(more)
   components.append(component)
  main=max(components,key=len);selected=[c for c in selected if int(c['RGB'][1:],16) in main]
  if sid=='STATE_NENETSIA':
   # Reviewed coastal closure: these seven unfortified Pai-Khoi mainland cells
   # otherwise become a new Russian enclave behind the tundra envelope.
   closure={'x0683CE','x6C631C','x87FEAE','x9D4CD7','x9EA5E8','xE8F9A4','xEEC8A0'}
   selected += [c for c in cells if c['state']==sid and c['RGB'] in closure and c not in selected]
  assert selected
  rows.append(dict(state=sid,source='RUS',target='NNT',RGBs=[c['RGB'] for c in selected],source_ids=['N1','N2','N3','M1776'],precision='NATIVE_TUNDRA_ENVELOPE_GAMEPLAY_ABSTRACTION_NOT_INDEPENDENT_NATION_OR_CADASTRE'))
 dump('PLAN.json',rows)
 owners=n.b4.inventory()['owners']
 for row in rows:
  for color in row['RGBs']:owners[color]=[[row['state'],row['target']]]
 render(owners,'PROPOSED',indices=False)
 print('Proposed',[(z['state'],len(z['RGBs'])) for z in rows],'; no incorporation-only changes.')

def extras():
 native=raw(r.GAME/'common/laws/01_colonial_affairs.txt');law=b.one(native,'law_internal_colonization')
 out={'common/laws/'+PREFIX+'.txt':'# Restore the single native1.15 law hidden by the older scenario file.\n'+native[law.start:law.end]+'\n'}
 out['common/defines/zz_'+PREFIX+'.txt']='''# Native1.15 Cossack parameters only; existing1776 global defines retained.
NCountry = { COSSACK_HOST_BUILDING = "building_cossack_host" }
NEconomy = {
 COSSACK_HOST_ARABLE_LAND_FRACTION = 0.2
 COSSACK_HOST_REMOVAL_COOLDOWN_MONTHS = 120
 COSSACK_HOST_REMOVAL_RADICALIZATION_FACTOR = 0.5
 COSSACK_HOST_RECENT_REMOVAL_YEARS = 5
}
'''
 out['common/country_definitions/'+PREFIX+'.txt']='''# Aggregate of tundra communities; no unified Nenets state is asserted.
NNT = {
 color = { 206 163 87 }
 country_type = decentralized
 tier = principality
 cultures = { ugrian }
 religion = animist
 capital = STATE_NENETSIA
}
'''
 out['common/history/countries/nnt - 1776 nenets tundra.txt']='COUNTRIES = { c:NNT ?= {\n'+''.join(' add_technology_researched = '+t+'\n' for t in NTECH)+''' activate_law = law_type:law_chiefdom
 activate_law = law_type:law_autocracy
 activate_law = law_type:law_hereditary_bureaucrats
 activate_law = law_type:law_state_religion
 activate_law = law_type:law_subjecthood
 activate_law = law_type:law_traditionalism
 activate_law = law_type:law_isolationism
 activate_law = law_type:law_peasant_levies
 activate_law = law_type:law_consumption_based_taxation
 activate_law = law_type:law_right_of_assembly
 activate_law = law_type:law_closed_borders
 activate_law = law_type:law_no_workers_rights
 effect_native_conscription_3 = yes
} }
'''
 out['common/history/buildings/99_'+PREFIX+'_cossacks.txt']='# Don, Yaik/Ural, Orenburg1748, Astrakhan1750; no later nineteenth-century hosts.\nBUILDINGS = {\n'+''.join(' s:'+s+' = { region_state:RUS = { establish_cossack_host = yes } }\n' for s in HOSTS)+'}\n'
 for language,lines in {'french':['NNT: "Communautés nenets"','NNT_ADJ: "nenets"','NNT_DEF: "les communautés nenets"'],'english':['NNT: "Nenets Communities"','NNT_ADJ: "Nenets"','NNT_DEF: "the Nenets communities"']}.items():
  out['localization/'+language+'/'+PREFIX+'_l_'+language+'.yml']='l_'+language+':\n'+''.join(' '+x+'\n' for x in lines)
 return out

def transform(old):
 out=dict(old);plans=load('PLAN.json');ops=[];text=old[ST]
 for row in plans:
  state=b.one(text,'s:'+row['state']);part=next(p for p in state.children('create_state') if p.one('country')=='c:RUS');field=part.children('owned_provinces')[0]
  vals=b.a.ids(part,'owned_provinces');remaining=[v for v in vals if 'x'+v.strip('"')[1:].upper() not in row['RGBs']]
  assert len(vals)-len(remaining)==len(row['RGBs']) and remaining
  ops.append((field.start,field.end,'owned_provinces = { '+' '.join('"'+v.strip('"')+'"' for v in remaining)+' }'))
  ops.append((state.end-1,state.end-1,'\n\t\tcreate_state = { country = c:NNT state_type = unincorporated owned_provinces = { '+' '.join('"'+c+'"' for c in row['RGBs'])+' } }\n\t'))
 out[ST]=b.edits(text,ops);ledger=[]
 for rel in POPS:
  text=old[rel];ops=[]
  for row in plans:
   found=[z for z in b.walk(b.parse(text)) if z.key=='s:'+row['state']]
   if not found:continue
   state,=found;part=state.children('region_state:RUS')[0];pops=[p for p in part.children('create_pop') if p.one('culture')=='ugrian'];assert len(pops)==1
   pop,=pops;size=pop.children('size')[0];before=int(size.value)
   s=b.one(old[ST],'s:'+row['state']);donor=next(z for z in s.children('create_state') if z.one('country')=='c:RUS');den=len(b.a.ids(donor,'owned_provinces'));num=len(row['RGBs']);moved=(before*num+den//2)//den
   assert 0<moved<before
   ops.append((size.start,size.end,'size = '+str(before-moved)))
   snippet=text[pop.start:pop.end];f=b.one(snippet,'size');snippet=b.edits(snippet,[(f.start,f.end,'size = '+str(moved))])
   ops.append((state.end-1,state.end-1,'\n\t\tregion_state:NNT = {\n'+snippet+'\n\t\t}\n\t'))
   ledger.append(dict(state=row['state'],culture='ugrian',religion=pop.one('religion'),source_before=before,source_after=before-moved,target_after=moved,rule='Only coarse indigenous pool split by existing-cell count; Russian and Tatar pools remain at settlement axes. Not a census, no pixel-density estimate.',numerator=num,denominator=den))
  out[rel]=b.edits(text,ops)
 text=old[r.COUNTRY];assert text.count('activate_law = law_type:law_colonial_resettlement')==1
 text=text.replace('activate_law = law_type:law_colonial_resettlement','activate_law = law_type:law_internal_colonization',1)
 country=b.one(text,'c:RUS');addition='''
		active_law:lawgroup_colonization ?= {
			add_amendment = { type = amendment_cossacks sponsor = PREV.ig:ig_rural_folk }
		}
		set_institution_investment_level = { institution = institution_colonial_affairs level = 1 }
	'''
 out[r.COUNTRY]=b.edits(text,[(country.end-1,country.end-1,addition)])
 native=raw(r.GAME/AI);node=b.one(native,'cossack_host_scores');text=old[AI];assert 'cossack_host_scores' not in text
 strategy=b.one(text,'ai_strategy_default');out[AI]=b.edits(text,[(strategy.end-1,strategy.end-1,'\n\t'+native[node.start:node.end]+'\n')])
 # Remove whitespace-only lines introduced by our insertions, retaining every
 # pre-existing line and the exact copied native AI field.
 for rel in [ST,r.COUNTRY]+POPS:
  a,z=old[rel].splitlines(keepends=True),out[rel].splitlines(keepends=True)
  for kind,a0,a1,z0,z1 in difflib.SequenceMatcher(None,a,z,autojunk=False).get_opcodes():
   if kind in ['insert','replace']:
    for j in range(z0,z1):
     if not z[j].strip():z[j]='\r\n' if z[j].endswith('\r\n') else '\n'
  out[rel]=''.join(z)
 for txt in out.values():b.parse(txt)
 return out,ledger

def preflight():
 import validate_starting_technology_1776 as tech
 assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed'
 old={p:raw(ROOT/p) for p in EXISTING};new,ledger=transform(old);additional=extras()
 for p,txt in additional.items():
  assert not (ROOT/p).exists(),p
  if p.endswith('.txt'):b.parse(txt)
 for p in EXISTING:
  dest=LOT/'apply_inputs'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
 snapshot=tech.collect_snapshot();dump('TECH_BEFORE.json',[tech.audit_country(t,snapshot) for t in ['RUS','CKC','UBD','KZH','OZH','UZH','CHI']])
 dump('POPULATION_ALLOCATION.json',ledger)
 dump('APPLY_BEFORE.json',dict(captured_utc=datetime.now(timezone.utc).isoformat(),inventory=n.b4.inventory(),protected=n.hashes(),files={p:b.a.sha(ROOT/p) for p in EXISTING},additional=list(additional),country_types={t:v[0].one('country_type') for t,v in b.a.catalog('common/country_definitions').items()}))
 for p,txt in new.items():
  dest=LOT/'proposed'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(txt,encoding='utf8',newline='')
 print('Preflight',len(new),'bounded shared files +',len(additional),'private files;',ledger)

def apply():
 assert not (LOT/'FILES_MODIFIED.json').exists(),'Do not replay'
 before=load('APPLY_BEFORE.json');old={p:raw(ROOT/p) for p in EXISTING}
 assert all(b.a.sha(ROOT/p)==h for p,h in before['files'].items()),'Concurrent modification; rerun preflight and review.'
 out,ledger=transform(old);out.update(extras());receipts=[]
 for rel,txt in out.items():
  path=ROOT/rel;pre=b.a.sha(path) if path.exists() else None
  assert pre==before['files'].get(rel),(rel,'Immediate preimage changed')
  path.parent.mkdir(parents=True,exist_ok=True);bom=path.read_bytes().startswith(b'\xef\xbb\xbf') if path.exists() else '/localization/' in '/'+rel
  path.write_bytes((b'\xef\xbb\xbf' if bom else b'')+txt.encode('utf8'))
  receipts.append(dict(file=rel,before=pre,after=b.a.sha(path)))
 dump('FILES_MODIFIED.json',receipts);print('Installed',len(receipts),'functional files. No bitmap, incorporation-only, or global population change.')

def coastal_repair():
 assert not (LOT/'COASTAL_CONTINUITY_REPAIR.json').exists(),'Already repaired'
 plans=load('PLAN.json');old={p:raw(LOT/'apply_inputs'/p) for p in EXISTING};expected,ledger=transform(old)
 affected=[ST]+POPS;pre={p:b.a.sha(ROOT/p) for p in affected};current={p:raw(ROOT/p) for p in affected}
 assert all(current[p]==expected[p] for p in affected),'Current shared preimages changed; review bounded nodes first'
 archive=LOT/'audit_history/initial_validation';archive.mkdir(parents=True,exist_ok=True)
 for name in ['PLAN.json','POPULATION_ALLOCATION.json','VALIDATION.json','CONTINUITY.json']:shutil.copy2(LOT/name,archive/name)
 cells={c['RGB']:c for c in load('FRONTIER_CELLS.json')};extra=load('CONTINUITY.json')['new_centralized_orphan_cells'];assert len(extra)==7 and all(cells[c]['state']=='STATE_NENETSIA' for c in extra)
 row=next(z for z in plans if z['state']=='STATE_NENETSIA');row['RGBs']+=extra;dump('PLAN.json',plans)
 proposed,ledger=transform(old);receipts=[]
 for p in affected:
  assert b.a.sha(ROOT/p)==pre[p]
  if proposed[p]==current[p]:continue
  dest=LOT/'coastal_repair_inputs'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
  bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf');(ROOT/p).write_bytes((b'\xef\xbb\xbf' if bom else b'')+proposed[p].encode('utf8'))
  receipts.append(dict(file=p,before=pre[p],after=b.a.sha(ROOT/p)))
 dump('POPULATION_ALLOCATION.json',ledger);dump('COASTAL_CONTINUITY_REPAIR.json',dict(added_RGBs=extra,reason='Unfortified Pai-Khoi coastal mainland pockets must not remain centralized enclaves behind decentralised tundra; no historical garrison identified in these cells.',files=receipts,population_delta=0))
 print('Coastal continuity repaired:',len(extra),'cells;',ledger)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--geo',action='store_true');p.add_argument('--plan',action='store_true');p.add_argument('--preflight',action='store_true');p.add_argument('--apply',action='store_true');p.add_argument('--coastal-repair',action='store_true');a=p.parse_args()
 if a.geo:geo()
 if a.plan:plan()
 if a.preflight:preflight()
 if a.apply:apply()
 if a.coastal_repair:coastal_repair()
