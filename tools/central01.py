"""Bounded CENTRAL-01 correction. No new TAGs or invented coastlines.

--prepare produces hash-guarded before/patch files; --apply installs only these.
--verify compares exact ownership, population identity and unrelated commands.
"""
import collections as C,json,sys,re,csv
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from central01_audit import OUT,CENTRAL,ISLANDS,SCOPE,dump,load
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from colonies01_frontier import owners
from hbc02_map_candidates import graph
from hbc04_land_links import flood,pair

ST='common/history/states/00_states.txt';PP='common/history/pops/06_central_america.txt'
TRANSFERS={
 'x600AC6':('STATE_HONDURAS','SC1','MKT','Mosquitia hondurienne / abords du Río Tinto'),
 'x907080':('STATE_HONDURAS','SC1','MKT','Raccord régional de la Mosquitia hondurienne'),
 'x528F3B':('STATE_HONDURAS','SC1','MKT','Cabo Gracias a Dios / littoral hondurien'),
 'x5299CA':('STATE_WEST_INDIES','GBR','FRA','Sainte-Lucie'),
 'x707080':('STATE_WEST_INDIES','GBR','SPA','Trinité'),
}
CLAIMS=['STATE_GUATEMALA','STATE_HONDURAS','STATE_NICARAGUA']

def staged(r):return OUT/'patch'/r
def prepare():
 assert not (OUT/'APPLIED.json').exists()
 own=owners();raw=text(ROOT/ST);nodes=state_nodes(raw);edits=[]
 for r,(s,b,t,label) in TRANSFERS.items():assert own[r]=={(s,b)},(r,own[r])
 for sid in sorted({s for s,b,t,l in TRANSFERS.values()}|set(CLAIMS)):
  n=nodes[sid];desired={}
  for z in n.children('create_state'):
   tag=scalar(z.one('country'))[2:];vals=set(provs(z,'owned_provinces'))
   for r,(s,b,t,l) in TRANSFERS.items():
    if s==sid:
     if tag==b:vals.discard(r)
     if tag==t:vals.add(r)
   desired[tag]=vals
   owned=z.children('owned_provinces')[0];edits.append((owned.start,owned.end,'owned_provinces = '+rgb_block(vals)))
  if sid=='STATE_HONDURAS':
   vals={r for r,(s,b,t,l) in TRANSFERS.items() if s==sid}
   edits.append((n.end-1,n.end-1,'\n\t\tcreate_state = { country = c:MKT owned_provinces = '+rgb_block(vals)+' state_type = incorporated }\n\t'))
  if sid in CLAIMS and not any(z.value=='c:SC1' for z in n.children('add_claim')):
   edits.append((n.end-1,n.end-1,'\n\t\t# CENTRAL-01: nominal Spanish claim, not proof of effective control.\n\t\tadd_claim = c:SC1\n\t'))
 newst=edit(raw,edits)
 # The existing Honduras cohort explicitly labeled Cape Gracias a Dios follows
 # that territory. No conversion, population growth or pixel-based census.
 oldpp=text(ROOT/PP);h=state_nodes(oldpp)['STATE_HONDURAS'];source=h.children('region_state:SC1')[0]
 pop=[z for z in source.children('create_pop') if scalar(z.one('culture'))=='miskito'];assert len(pop)==1 and int(pop[0].one('size'))==1803
 z=pop[0];newpp=edit(oldpp,[(z.start,z.end,''),(h.end-1,h.end-1,'\n\t\tregion_state:MKT = {\n\t\t\t'+oldpp[z.start:z.end]+'\n\t\t}\n\t')])
 patch={ST:encoded(ROOT/ST,newst),PP:encoded(ROOT/PP,newpp)}
 manifest=dict(input_sha256={},output_sha256={})
 for r,data in patch.items():
  dst=staged(r);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
  old=OUT/'before'/r;old.parent.mkdir(parents=True,exist_ok=True);old.write_bytes((ROOT/r).read_bytes())
  manifest['input_sha256'][r]=sha(ROOT/r);manifest['output_sha256'][r]=sha(dst)
 dump('PATCH.json',manifest);dump('PREPARE_RUNTIME.json',runtime())
 dump('PLAN.json',dict(date='2026-10-27',transfers=[dict(rgb=r,state=s,before=b,after=t,label=l) for r,(s,b,t,l) in TRANSFERS.items()],claims=CLAIMS,miskito_population_transfer=1803,new_countries=0,bitmap_changed=False,caribbean_population_policy='Existing national cohorts within the shared State Region retained; no invented island-level census or forced reclassification.',historical_boundary_accuracy='Regional approximation; Talamanca, Darien, Belize extent and grouped micro-islands remain open.',engine_tested=False))
 print('Prepared 5 province transfers, 3 nominal claim regions, 1803 existing Miskito people; 2 runtime files.')

def apply():
 p=load('PATCH.json')
 assert all(sha(ROOT/r)==h for r,h in p['input_sha256'].items()),'Shared files changed: re-examine before applying'
 assert all(sha(staged(r))==h for r,h in p['output_sha256'].items())
 for r in p['output_sha256']:(ROOT/r).write_bytes(staged(r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
 print('Applied 2 hash-guarded runtime files.')

def owned(raw):
 out=C.defaultdict(set)
 for s,n in state_nodes(raw).items():
  for z in n.children('create_state'):
   for r in provs(z,'owned_provinces'):out[r].add((s,scalar(z.one('country'))[2:]))
 return dict(out)
def cohorts(raw):
 out=C.Counter()
 for s,n in state_nodes(raw).items():
  for rs in n.children():
   for z in rs.children('create_pop'):
    sig=tuple(sorted((q.key,str(q.value)) for q in z.children() if q.key!='size'))
    out[s,sig]+=int(z.one('size'))
 return out
def verify(staging=False):
 m=load('PATCH.json');checks={}
 def get(r):return text(staged(r) if staging else ROOT/r)
 oldst=text(OUT/'before'/ST);newst=get(ST);a=owned(oldst);b=owned(newst);old=state_nodes(oldst);new=state_nodes(newst)
 checks['manifest_sources_or_outputs_current']=all(sha(ROOT/r)==h for r,h in m['input_sha256' if staging else 'output_sha256'].items())
 checks['staged_patch_hashes']=all(sha(staged(r))==h for r,h in m['output_sha256'].items())
 checks['all_modified_scripts_parse']=all(parse(get(r)) is not None for r in m['output_sha256'])
 checks['exact_five_transfers']=all(b[r]=={(s,t)} and a[r]=={(s,prior)} for r,(s,prior,t,l) in TRANSFERS.items())
 checks['every_other_province_owner_unchanged']=all(b.get(r)==v for r,v in a.items() if r not in TRANSFERS) and set(a)==set(b)
 checks['no_new_duplicate_or_unowned_province']=all(len(v)==1 or v==a.get(r) for r,v in b.items()) and all(b[r] for r in a)
 regs={n.key:set(provs(n,'provinces')) for p in effective('map_data/state_regions') for n in parse(text(p))}
 checks['transferred_rgb_have_correct_region']=all(r in regs[s] for r,(s,prior,t,l) in TRANSFERS.items())
 checks['nominal_spanish_claims_added']=all(any(z.value=='c:SC1' for z in new[s].children('add_claim')) for s in CLAIMS)
 checks['all_other_claims_preserved']=all(normalized(n.children('add_claim'))==normalized(old[s].children('add_claim')) for s,n in new.items() if s not in CLAIMS)
 checks['other_state_commands_and_portions_preserved']=all(normalized([z for z in n.children() if z.key not in ['create_state','add_claim']])==normalized([z for z in old[s].children() if z.key not in ['create_state','add_claim']]) for s,n in new.items())
 checks['every_existing_state_portion_keeps_its_other_commands']=all(normalized([q for q in z.children() if q.key!='owned_provinces'])==normalized([q for q in next(v for v in new[s].children('create_state') if v.one('country')==z.one('country')).children() if q.key!='owned_provinces']) for s,n in old.items() for z in n.children('create_state'))
 oldpp=text(OUT/'before'/PP);newpp=get(PP)
 checks['population_identity_and_regional_totals_conserved']=cohorts(oldpp)==cohorts(newpp)
 def scopes(raw):return {(s,rs.key):normalized(rs.children()) for s,n in state_nodes(raw).items() for rs in n.children()}
 u=scopes(oldpp);v=scopes(newpp)
 checks['all_other_population_scopes_unchanged']=all(v[k]==value for k,value in u.items() if k[0]!='STATE_HONDURAS')
 h=state_nodes(newpp)['STATE_HONDURAS'];mp=h.children('region_state:MKT')[0].children('create_pop')
 checks['exact_existing_honduran_miskito_cohort_transferred']=len(mp)==1 and int(mp[0].one('size'))==1803 and scalar(mp[0].one('culture'))=='miskito'
 shares={(s,scalar(z.one('country'))[2:]) for s,n in new.items() for z in n.children('create_state')}
 checks['all_nonempty_modified_pop_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s,n in state_nodes(newpp).items() for rs in n.children() if rs.children('create_pop'))
 base=load('PREPARE_RUNTIME.json');now=runtime();external={r:dict(before_sha256=base.get(r),observed_sha256=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)}
 dump('CONCURRENT_FILES.json',external)
 checks['bitmap_regions_locators_unchanged']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/map_object_data/')))
 checks['all_buildings_military_and_country_profiles_unchanged']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/military_formations/','common/history/countries/','common/country_definitions/')))
 # Direct shared-edge continuity, not a diagonal or maritime connection.
 raw=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);raster=(raw[:,:,0]<<16)|(raw[:,:,1]<<8)|raw[:,:,2]
 mkt={int(r[1:],16) for r,vv in b.items() if any(t=='MKT' for s,t in vv)}
 definitions=[n for p in effective('map_data/state_regions') for n in parse(text(p))]
 imp={int(r[1:],16) for n in definitions for r in provs(n,'impassable')};blocked=set()
 ap=ROOT/'map_data/adjacencies.csv';ap=ap if ap.exists() else GAME/'map_data/adjacencies.csv'
 for z in csv.DictReader(ap.open(encoding='utf-8-sig'),delimiter=';'):
  if all(z.get(k,'').startswith('x') for k in ['From','To']) and (z.get('Type') in ['sea','impassable'] or z.get('adjacency_rule_name','').strip()):blocked.add(pair(int(z['From'][1:],16),int(z['To'][1:],16)))
 mask=np.isin(raster,list(mkt-imp));yy,xx=np.where(mask);x0,x1=int(xx.min()),int(xx.max())+1;y0,y1=int(yy.min()),int(yy.max())+1
 crop=raster[y0:y1,x0:x1];allowed=mask[y0:y1,x0:x1];seed=int(np.flatnonzero(allowed.ravel())[0]);parents,_=flood(crop,allowed,{seed},blocked)
 reached={int(crop.ravel()[i]) for i in parents}
 checks['miskito_seven_provinces_one_passable_pixel_component']=len(mkt)==7 and mkt<=reached
 dump('MISKITO_LAND_WITNESS.json',dict(rgbs=sorted(f'x{r:06X}' for r in reached),pixel_count=len(parents),bbox=[x0,y0,x1,y1],blocked_adjacencies_respected=True,impassable_provinces_excluded=True))
 spanish={int(r[1:],16) for r,vv in b.items() if any(t=='SC1' for s,t in vv)}-imp
 adj=graph(raster,np.array(sorted(spanish),dtype=np.uint32));visited=set();sizes=[]
 for seed in sorted(spanish):
  if seed in visited:continue
  q=C.deque([seed]);visited.add(seed);size=0
  while q:
   u=q.popleft();size+=1
   for v in adj.get(u,{}):
    if v not in visited and pair(u,v) not in blocked:visited.add(v);q.append(v)
  sizes.append(size)
 checks['new_spain_501_provinces_remain_connected_by_land']=sizes==[501]
 dump('NEW_SPAIN_CONTINUITY.json',dict(provinces=len(spanish),component_sizes=sizes,method='Shared-edge province graph, explicit forbidden adjacencies and impassable provinces excluded; original provinces not redrawn.'))
 checks['no_new_country_or_technology']=not any(r.startswith(('common/country_definitions/','common/history/countries/','common/technology/')) for r in m['output_sha256'])
 checks['no_runtime_files_added_or_removed']=set(base)==set(now)
 dump('STAGED_VALIDATION.json' if staging else 'VALIDATION.json',dict(date='2026-10-27',checks=checks,all_pass=all(checks.values()),passed=sum(checks.values()),total=len(checks),external_files=list(external),engine_tested=False,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'))
 print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v],external_files=list(external))))
 assert all(checks.values())

def preview(staging=False):
 own=owned(text(staged(ST) if staging else ROOT/ST));defs={n.key:set(provs(n,'provinces')) for p in effective('map_data/state_regions') for n in parse(text(p))}
 raw=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);raster=(raw[:,:,0]<<16)|(raw[:,:,1]<<8)|raw[:,:,2]
 pal={'SC1':(228,184,63),'SC2':(207,137,55),'MKT':(57,166,153),'GBR':(184,109,143),'FRA':(91,143,204),'NET':(215,137,71),'SPA':(228,184,63),'DENNOR':(172,91,101),'HAI':(91,143,204),'GR5':(228,184,63),'PCO':(228,184,63),'CUB':(228,184,63)}
 font_path='C:/Windows/Fonts/arial.ttf'
 ft=lambda n:ImageFont.truetype(font_path,n)
 panels=[('CENTRAL_AMERICA_1776.png',[1975,1660,2355,1950],4,'Amérique centrale — corrections au 1er janvier 1776',[
 ('Nouvelle-Espagne',(2045,1780)),('Belize : établissements britanniques',(2084,1695)),('Mosquitia',(2181,1761)),('Nicaragua espagnol',(2148,1824)),('Costa Rica',(2181,1880)),('Panama / Nouvelle-Grenade',(2278,1901))]),
 ('CARIBBEAN_1776.png',[2410,1620,2765,1885],4,'Petites Antilles — souverainetés corrigées pour 1776',[
 ('Sainte-Lucie → France',(2707,1786)),('Trinité → Espagne',(2694,1862)),('Martinique',(2708,1767)),('Guadeloupe',(2702,1727)),('Tobago : britannique',(2715,1845)),('Grenade : britannique',(2690,1828)),('Antilles néerlandaises',(2530,1810))])]
 for filename,(x0,y0,x1,y1),scale,title,labels in panels:
  crop=raster[y0:y1,x0:x1];pixels=np.full((*crop.shape,3),[35,49,59],dtype=np.uint8)
  for rgb in np.unique(crop):
   r=f'x{int(rgb):06X}';v=own.get(r);color=pal.get(next(iter(v))[1],(103,114,94)) if v else (35,49,59)
   if v:pixels[crop==rgb]=color
  border=np.zeros(crop.shape,dtype=bool);border[:,1:]|=crop[:,1:]!=crop[:,:-1];border[1:]|=crop[1:]!=crop[:-1];pixels[border]=[37,48,52]
  mapim=Image.fromarray(pixels).resize((crop.shape[1]*scale,crop.shape[0]*scale),Image.Resampling.NEAREST)
  im=Image.new('RGB',(mapim.width,mapim.height+145),(35,49,59));im.paste(mapim,(0,80));d=ImageDraw.Draw(im);d.text((20,15),title,font=ft(28),fill='white')
  for name,(x,y) in labels:
   xx=(x-x0)*scale;yy=(y-y0)*scale+80;d.text((xx,yy),name,font=ft(19),fill='white',stroke_width=2,stroke_fill=(25,34,42))
  d.text((18,mapim.height+93),'Jaune : Espagne / colonies ; turquoise : Miskitu ; rose : Grande-Bretagne ; bleu : France.',font=ft(17),fill='white')
  d.text((18,mapim.height+118),'Limites régionales approximatives. Autonomies du Darién et du Talamanca encore à préciser.',font=ft(17),fill='white')
  im.save(OUT/filename)

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify('--staged' in sys.argv)
 elif '--preview' in sys.argv:preview('--staged' in sys.argv)
