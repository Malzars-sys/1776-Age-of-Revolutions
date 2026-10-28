"""Bounded January 1776 Spanish Rio Grande/Santa Tecla correction.

Five whole existing provinces; no new TAG, coastline, demographic growth or
claim to have surveyed the colonial frontier. Prepare/apply are hash guarded.
"""
import collections as C,csv,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from central01 import owned,cohorts
from hbc02_map_candidates import graph
from hbc04_land_links import pair

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-02'
ST='common/history/states/00_states.txt'
PP='common/history/pops/07_south_america.txt'
BUILD=['common/history/buildings/07_south_america.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']
SID='STATE_RIO_GRANDE_DO_SUL'
CELLS={'x52B247','xD3A197','xCC2135','xCD9ECD','xD9D235'}
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def raster():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
 return (a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]

def landproof(own):
 a=raster();span={int(r[1:],16) for r,v in own.items() if any(t=='SC4' for s,t in v)};new={int(r[1:],16) for r in CELLS}
 imp={int(r[1:],16) for p in effective('map_data/state_regions') for n in parse(text(p)) for r in provs(n,'impassable')}
 blocked=set();p=ROOT/'map_data/adjacencies.csv';p=p if p.exists() else GAME/'map_data/adjacencies.csv'
 for row in csv.DictReader(p.open(encoding='utf-8-sig'),delimiter=';'):
  if all(row.get(k,'').startswith('x') for k in ['From','To']) and (row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip()):blocked.add(pair(int(row['From'][1:],16),int(row['To'][1:],16)))
 assert not new&imp
 adj=graph(a,np.array(sorted((span|new)-imp),dtype=np.uint32));seed=0x302DDA;seen={seed};q=C.deque([seed])
 while q:
  u=q.popleft()
  for v in adj.get(u,{}):
   if v not in seen and pair(u,v) not in blocked:seen.add(v);q.append(v)
 assert new<=seen,'No isolated continental post or invented sea bridge'
 return dict(seed='x302DDA',seed_name='Montevideo',reached=sorted(f'x{v:06X}' for v in new&seen),blocked_adjacencies_respected=True,impassable_excluded=True)

def prepare():
 assert not (OUT/'APPLIED.json').exists()
 base=runtime();old=owned(text(ROOT/ST));assert all(old[r]=={(SID,'BRZ')} for r in CELLS)
 dump('LAND_CONTINUITY.json',landproof(old))
 files={};raw=text(ROOT/ST);n=state_nodes(raw)[SID];src=n.children('create_state');assert len(src)==1 and src[0].one('country')=='c:BRZ'
 z=src[0].children('owned_provinces')[0]
 files[ST]=encoded(ROOT/ST,edit(raw,[(z.start,z.end,'owned_provinces = '+rgb_block(set(provs(src[0],'owned_provinces'))-CELLS)),(n.end-1,n.end-1,'\n\t\t# R9-02: Spanish occupied core, before the March-April 1776 reconquest.\n\t\tcreate_state = { country = c:SC4 owned_provinces = '+rgb_block(CELLS)+' state_type = incorporated }\n\t')]))
 raw=text(ROOT/PP);n=state_nodes(raw)[SID];rs=n.children('region_state:BRZ')[0];p=[z for z in rs.children('create_pop') if scalar(z.one('culture'))=='sulista'];assert len(p)==1 and int(p[0].one('size'))==53059
 z=p[0].children('size')[0]
 # Documented nearby April 1776 observation, used only as a bounded technical
 # allocation of existing free settlers. Not a January census or area ratio.
 files[PP]=encoded(ROOT/PP,edit(raw,[(z.start,z.end,'size = 52373'),(n.end-1,n.end-1,'\n\t\t# R9-02: existing free settlers; dated proxy and limits in the dossier.\n\t\tregion_state:SC4 = { create_pop = { culture = sulista size = 686 } }\n\t')]))
 for path in BUILD:
  raw=text(ROOT/path);n=state_nodes(raw)[SID];rs=n.children('region_state:BRZ')[0];ports=[z for z in rs.children('create_building') if scalar(z.one('building'))=='building_port'];assert len(ports)==1
  z=ports[0];chunk=raw[z.start:z.end].replace('c:BRZ','c:SC4')
  files[path]=encoded(ROOT/path,edit(raw,[(z.start,z.end,''),(n.end-1,n.end-1,'\n region_state:SC4 = {\n'+chunk+'\n}\n')]))
 m=dict(input_sha256={},output_sha256={})
 for r,data in files.items():
  before=OUT/'before'/r;patch=OUT/'patch'/r;before.parent.mkdir(parents=True,exist_ok=True);patch.parent.mkdir(parents=True,exist_ok=True)
  before.write_bytes((ROOT/r).read_bytes());patch.write_bytes(data);m['input_sha256'][r]=sha(ROOT/r);m['output_sha256'][r]=sha(patch)
 assert all(sha(ROOT/r)==h for r,h in m['input_sha256'].items())
 dump('PATCH.json',m);dump('PREPARE_RUNTIME.json',base)
 dump('PLAN.json',dict(date='2026-10-27',reference_date='1776-01-01',state=SID,from_tag='BRZ',to_tag='SC4',cells=sorted(CELLS),population_redistributed=686,population_added=0,population_method='April 1776 free-settler observation: dated proxy, not January census; existing sulista identity retained.',port_commands_reassigned=2,other_building_commands_unchanged=True,bitmap_changed=False,full_frontier_certified=False))
 print(json.dumps(dict(provinces=len(CELLS),population_redistributed=686,files=len(files))))

def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists()
 assert all(sha(ROOT/r)==h for r,h in m['input_sha256'].items()),'Concurrent edit: re-examine current file, do not restore old file'
 assert all(sha(OUT/'patch'/r)==h for r,h in m['output_sha256'].items())
 for r in m['output_sha256']:(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))

def verify():
 m=load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();old=owned(text(OUT/'before'/ST));new=owned(text(ROOT/ST));checks={}
 checks['installed_hashes']=all(now.get(r)==h for r,h in m['output_sha256'].items())
 checks['modified_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'])
 checks['exact_five_transfers_only']=set(new)==set(old) and all(new[r]==({(SID,'SC4')} if r in CELLS else v) for r,v in old.items())
 checks['no_new_duplicate_or_unowned_rgb']=all(new[r] and (len(new[r])==1 or new[r]==old[r]) for r in old)
 checks['population_cohorts_and_totals_conserved']=cohorts(text(OUT/'before'/PP))==cohorts(text(ROOT/PP))
 def amounts(raw):
  n=state_nodes(raw)[SID];return {rs.key:sum(int(z.one('size')) for z in rs.children('create_pop')) for rs in n.children()}
 checks['dated_proxy_exact_686']=amounts(text(ROOT/PP))=={'region_state:BRZ':91602,'region_state:SC4':686}
 def buildings(raw,remap=False):
  # Only the destination of the existing port commands is allowed to change.
  out=[]
  for sid,n in state_nodes(raw).items():
   for rs in n.children():
    for z in rs.children('create_building'):
     port=sid==SID and scalar(z.one('building'))=='building_port';key=rs.key
     fragment=raw[z.start:z.end]
     if remap and port:key='region_state:SC4';fragment=fragment.replace('c:BRZ','c:SC4')
     out.append((sid,key,json.dumps(normalized(parse(fragment)),sort_keys=True)))
  return C.Counter(out)
 checks['all_assets_preserved_only_ports_follow_control']=all(buildings(text(OUT/'before'/r),True)==buildings(text(ROOT/r)) for r in BUILD)
 pp=state_nodes(text(ROOT/PP));shares={(s,scalar(z.one('country'))[2:]) for s,n in state_nodes(text(ROOT/ST)).items() for z in n.children('create_state')}
 checks['population_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s,n in pp.items() for rs in n.children() if rs.children('create_pop'))
 checks['new_ports_have_land']=all((s,rs.key.split(':')[1]) in shares for r in BUILD for s,n in state_nodes(text(ROOT/r)).items() for rs in n.children() if s==SID and rs.children('create_building'))
 checks['new_sites_connect_to_montevideo']=set(landproof(new)['reached'])==CELLS
 checks['central02_cores_preserved']=all(new[r]=={v} for r,v in {'xB0243F':('STATE_COSTA_RICA','G81'),'xBB820B':('STATE_PANAMA','K81'),'x446C64':('STATE_WEST_INDIES','C81')}.items())
 checks['r901_cores_preserved']=all(new[r]==old[r] for r,v in old.items() if any(s in ['STATE_ICA','STATE_LA_PAZ'] for s,t in v))
 checks['portuguese_capital_and_north_bank_retained']=all(new[r]=={(SID,'BRZ')} for r in ['xC7E5A1','xE17D15'])
 checks['no_bitmap_regions_hubs_profiles_pacts_modified']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/','common/history/countries/','common/history/diplomacy/','common/history/military_formations/')))
 external={r:dict(before_sha256=base.get(r),observed_sha256=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)}
 dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change']=not external
 dump('VALIDATION.json',dict(date='2026-10-27',checks=checks,passed=sum(checks.values()),total=len(checks),all_pass=all(checks.values()),engine_tested=False));print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())

def preview():
 a=raster();x0,y0,x1,y1=2730,2760,2965,2950;b=a[y0:y1,x0:x1];own=owned(text(ROOT/ST));canvas=np.full((*b.shape,3),[37,49,59],dtype=np.uint8)
 for r,v in own.items():
  c=int(r[1:],16)
  if r in CELLS:color=[219,111,83]
  elif any(t=='SC4' for s,t in v):color=[120,147,188]
  elif any(t=='BRZ' for s,t in v):color=[186,157,84]
  else:color=[88,101,97]
  canvas[b==c]=color
 border=np.zeros(b.shape,bool);border[1:]|=b[1:]!=b[:-1];border[:,1:]|=b[:,1:]!=b[:,:-1];canvas[border]=[28,38,45]
 im=Image.new('RGB',(1175,1080),(37,49,59));im.paste(Image.fromarray(canvas).resize((1175,950),Image.Resampling.NEAREST),(0,80));d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
 d.text((15,12),'R9-02 — Rio Grande et Santa Tecla, 1 janvier 1776',fill='white',font=f)
 d.text((15,40),'Orange : cinq provinces corrigées ; bleu : SC4 ; or : Brésil portugais.',fill='white',font=f)
 for label,p in [('Montevideo',[2814.484,2927.956]),('Porto Alegre',[2932.483,2815.152]),('Rio Grande',[2907.096,2863.536]),('Santa Tecla (approx.)',[2862.87,2845.21])]:
  x,y=(p[0]-x0)*5,(p[1]-y0)*5+80;d.ellipse((x-4,y-4,x+4,y+4),fill='white');d.text((x-130,y+7),label,fill='white',font=f,stroke_width=2,stroke_fill='black')
 d.text((15,1040),'Installation technique partielle ; frontières intérieures et validation en jeu encore ouvertes.',fill='white',font=f);im.save(OUT/'R9_02_RIO_GRANDE.png')

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
 elif '--preview' in sys.argv:preview()
