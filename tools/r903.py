"""Sacramento: player-authorized enlarged Portuguese coastal enclave, 1776.

Hash-guarded preparation/application; current shared files only. No new country,
fictional land corridor, coastline, technology grants or demographic growth.
"""
import collections as C,io,json,re,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,ownership
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from hbc02_map_candidates import graph

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-03'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt'
REG='map_data/state_regions/07_south_america.txt';BIT='map_data/provinces.png'
POST='STATE_COLONIA_DO_SACRAMENTO';PARENT='STATE_URUGUAY'
OLD='x4E1442';NEW='x4E1443';PREFIX='1776_sacramento'
LOC='gfx/map/map_object_data/generated_map_object_locators_'
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def raster(path):
 a=np.asarray(Image.open(path).convert('RGB'),dtype=np.uint32)
 return (a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]
def component_count(mask):
 remaining=set(zip(*np.where(mask)));count=0
 while remaining:
  count+=1;q=[remaining.pop()]
  while q:
   y,x=q.pop()
   for v in [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]:
    if v in remaining:remaining.remove(v);q.append(v)
 return count
def inhabitants(raw):
 result=C.Counter()
 for sid,n in state_nodes(raw).items():
  for rs in n.children():
   for z in rs.children('create_pop'):
    fields=tuple(sorted((v.key,scalar(v.value)) for v in z.children() if v.key!='size'))
    result[(PARENT if sid==POST else sid,fields)]+=int(z.one('size'))
 return result
def prepare():
 assert not (OUT/'APPLIED.json').exists()
 base=runtime();own=ownership();assert own[OLD]=={(PARENT,'SC4')} and NEW not in own
 a=raster(ROOT/BIT);assert not np.any(a==int(NEW[1:],16))
 # Explicit player request: exaggerate the otherwise subpixel fortified town
 # for visibility. Clip the compact footprint to existing Spanish land.
 pixels=[(x,y) for y in range(2914,2921) for x in range(2772,2782) if a[y,x]==int(OLD[1:],16)]
 assert 40<=len(pixels)<=65
 for x,y in pixels:a[y,x]=int(NEW[1:],16)
 port=[2777,2920];assert tuple(port) in pixels and a[port[1]+1,port[0]]==0x1FDEFC
 hubs=dict(city=[2777,2916],port=port,farm=[2774,2915],mine=[2779,2916],wood=[2780,2914]);assert all(tuple(p) in pixels for p in hubs.values())
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};assert POST not in regs
 newid=max(int(n.one('id')) for n in regs.values() if n.one('id') is not None)+1
 assert newid==3161,'Re-examine concurrent region allocation'
 assert int(regs['STATE_RIVER_PLATE'].one('id'))==3065 and 'x1FDEFC' in provs(regs['STATE_RIVER_PLATE'],'provinces')
 files={};buf=io.BytesIO();Image.fromarray(np.stack([(a>>16)&255,(a>>8)&255,a&255],axis=-1).astype('uint8')).save(buf,format='PNG');files[BIT]=buf.getvalue()
 raw=text(ROOT/REG);n=next(n for n in parse(raw) if n.key==PARENT);z=n.children('arable_land')[0];fish=n.children('capped_resources')[0].children('building_fishing_wharf')[0]
 assert int(z.value)==100 and int(fish.value)==6
 raw=edit(raw,[(z.start,z.end,'arable_land = 99'),(fish.start,fish.end,'building_fishing_wharf = 5')])
 raw+='\n# R9-03: deliberately enlarged fortified Portuguese town; no hinterland claim.\n'+POST+' = {\n id = '+str(newid)+'\n subsistence_building = building_subsistence_farm\n provinces = { "'+NEW+'" }\n'+''.join(' '+k+' = "'+NEW+'"\n' for k in hubs)+' arable_land = 1\n arable_resources = { building_maize_farm }\n capped_resources = { building_fishing_wharf = 1 }\n naval_exit_id = 3065\n}\n'
 files[REG]=encoded(ROOT/REG,raw)
 raw=text(ROOT/ST);n=parse(raw)[0];assert POST not in raw
 files[ST]=encoded(ROOT/ST,edit(raw,[(n.end-1,n.end-1,'\n s:'+POST+' = { create_state = { country = c:BRZ state_type = incorporated owned_provinces = { '+NEW+' } } }\n')]))
 raw=text(ROOT/PP);n=state_nodes(raw)[PARENT];rs=n.children('region_state:SC4')[0];edits=[];moved=[]
 for culture,kind,amount,expected in [('brazilian',None,1742,8871),('afro_caribeno','slaves',1575,4812)]:
  pops=[z for z in rs.children('create_pop') if scalar(z.one('culture'))==culture and z.one('pop_type')==kind];assert len(pops)==1
  z=pops[0];assert int(z.one('size'))==expected;size=z.children('size')[0]
  edits.append((size.start,size.end,'size = '+str(expected-amount)))
  moved.append(edit(raw[z.start:z.end],[(size.start-z.start,size.end-z.start,'size = '+str(amount))]))
 root=parse(raw)[0];edits.append((root.end-1,root.end-1,'\n # R9-03: 1760 dated proxy, not a January 1776 census.\n s:'+POST+' = { region_state:BRZ = {\n'+'\n'.join(moved)+'\n} }\n'))
 files[PP]=encoded(ROOT/PP,edit(raw,edits))
 files['common/history/buildings/'+PREFIX+'.txt']=('BUILDINGS = {\n s:'+POST+' = { region_state:BRZ = { create_building = { building = building_port level = 1 reserves = 1 activate_production_methods = { pm_aor1776_traditional_commercial_harbor pm_1776_no_raw_data_reporting } } } }\n}\n').encode('utf8')
 references={}
 for kind,xy in hubs.items():
  rel=LOC+kind+'.txt';source=ROOT/rel if (ROOT/rel).exists() else GAME/rel;raw=text(source);instances=parse(raw)[0].children('instances')[0]
  template=next(z for z in instances.children() if z.one('id')=='370');chunk=raw[template.start:template.end];idnode=template.children('id')[0];pos=template.children('position')[0];vals=[z.value for z in pos.children()];vals[0]=str(xy[0]+.25);vals[2]=str(a.shape[0]-xy[1]-.25)
  chunk=edit(chunk,[(idnode.start-template.start,idnode.end-template.start,'id = '+str(newid)),(pos.start-template.start,pos.end-template.start,'position = { '+' '.join(vals)+' }')]);files[rel]=encoded(source,edit(raw,[(instances.end-1,instances.end-1,'\n'+chunk+'\n')]))
  if source.is_relative_to(GAME):references[str(source)]=sha(source)
 sr='common/strategic_regions/south_america_strategic_regions.txt';source=ROOT/sr if (ROOT/sr).exists() else GAME/sr;raw=text(source);z=[z for z in walk(parse(raw)) if z.key=='states' and any(scalar(v.value)==PARENT for v in z.children())];assert len(z)==1
 files[sr]=encoded(source,edit(raw,[(z[0].end-1,z[0].end-1,' '+POST+' ')]))
 if source.is_relative_to(GAME):references[str(source)]=sha(source)
 terrain='map_data/province_terrains.txt';raw=text(ROOT/terrain);n=[n for n in parse(raw) if n.key.lower()==OLD.lower()];assert len(n)==1;assert NEW.lower() not in raw.lower();files[terrain]=encoded(ROOT/terrain,raw+'\n'+NEW+' = '+scalar(n[0].value)+'\n')
 for lang,name in [('french','Colônia do Sacramento'),('english','Colonia do Sacramento')]:
  loc=['l_'+lang+':',f' {POST}:0 "{name}"']+[f' HUB_NAME_{POST}_{k}:0 "{name}"' for k in hubs]
  files[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']=b'\xef\xbb\xbf'+('\n'.join(loc)+'\n').encode('utf8')
 manifest=dict(input_sha256={},output_sha256={},canonical_reference_sha256=references)
 for rel,data in files.items():
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  original=ROOT/rel;before=OUT/'before'/rel;patch=OUT/'patch'/rel;patch.parent.mkdir(parents=True,exist_ok=True);patch.write_bytes(data)
  if original.exists():before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(original.read_bytes())
  manifest['input_sha256'][rel]=sha(original) if original.exists() else None;manifest['output_sha256'][rel]=sha(patch)
 dump('PATCH.json',manifest);dump('PREPARE_RUNTIME.json',base)
 dump('PLAN.json',dict(date='2026-10-27',reference_date='1776-01-01',state=POST,id=newid,parent=PARENT,new_rgb=NEW,source_rgb=OLD,pixels=pixels,hubs=hubs,owner='BRZ',crown='POR',naval_exit=3065,sea_rgb='x1FDEFC',population=3317,free_existing_brazilian=1742,existing_afro_caribeno_slaves=1575,population_added=0,demographic_proxy_year=1760,arable_transferred=1,fishing_capacity_transferred=1,new_port_levels=1,new_tags=0,player_authorized_visibility_exaggeration=True,no_land_corridor=True,engine_tested=False))
 print(json.dumps(dict(pixels=len(pixels),new_state_id=newid,people_redistributed=3317,files=len(files))))

def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists()
 assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==h for r,h in m['input_sha256'].items()),'Concurrent change: re-examine current file'
 assert all(sha(__import__('pathlib').Path(p))==h for p,h in m['canonical_reference_sha256'].items())
 assert all(sha(OUT/'patch'/r)==h for r,h in m['output_sha256'].items())
 for r in m['output_sha256']:(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-27',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))

def verify():
 m=load('PATCH.json');p=load('PLAN.json');base=load('PREPARE_RUNTIME.json');now=runtime();checks={};old=raster(OUT/'before'/BIT);new=raster(ROOT/BIT)
 y,x=np.where(old!=new);pixels=set(map(tuple,p['pixels']));checks['exact_enlarged_footprint_only']=set(zip(map(int,x),map(int,y)))==pixels and all(old[yy,xx]==int(OLD[1:],16) and new[yy,xx]==int(NEW[1:],16) for xx,yy in pixels)
 checks['installed_hashes']=all(now.get(r)==h for r,h in m['output_sha256'].items())
 checks['all_modified_text_parses']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'] if r.endswith('.txt'))
 regs={n.key:n for path in effective('map_data/state_regions') for n in parse(text(path))};newreg=regs[POST];oldreg={n.key:n for n in parse(text(OUT/'before'/REG))}
 checks['one_unique_new_state_id']=len([n for n in regs.values() if n.one('id')==str(p['id'])])==1 and set(oldreg)|{POST}=={n.key for n in parse(text(ROOT/REG))}
 occurrences=[n.key for n in regs.values() if NEW in provs(n,'provinces')];checks['new_rgb_in_one_region']=occurrences==[POST]
 own=ownership();prior=__import__('central01').owned(text(OUT/'before'/ST));checks['no_other_owner_changes']=own[NEW]=={(POST,'BRZ')} and set(own)==set(prior)|{NEW} and all(own[r]==v for r,v in prior.items())
 checks['old_province_retains_spanish_land']=own[OLD]=={(PARENT,'SC4')} and np.any(new==int(OLD[1:],16))
 checks['population_and_identities_conserved']=inhabitants(text(OUT/'before'/PP))==inhabitants(text(ROOT/PP))
 rs=state_nodes(text(ROOT/PP))[POST].children('region_state:BRZ')[0];checks['dated_proxy_exact']=sum(int(z.one('size')) for z in rs.children('create_pop'))==3317 and {scalar(z.one('culture')):int(z.one('size')) for z in rs.children('create_pop')}=={'brazilian':1742,'afro_caribeno':1575}
 checks['all_old_building_files_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith('common/history/buildings/'))
 checks['all_profiles_pacts_and_military_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/countries/','common/history/diplomacy/','common/history/military_formations/')))
 n=regs[PARENT];o=oldreg[PARENT];checks['regional_capacities_conserved']=int(n.one('arable_land'))+int(newreg.one('arable_land'))==int(o.one('arable_land')) and int(n.children('capped_resources')[0].one('building_fishing_wharf'))+int(newreg.children('capped_resources')[0].one('building_fishing_wharf'))==int(o.children('capped_resources')[0].one('building_fishing_wharf'))
 def without_caps(n):return normalized([v for v in n.children() if v.key not in ['arable_land','capped_resources']])
 checks['parent_hubs_provinces_traits_and_other_regions_preserved']=all(normalized([n])==normalized([oldreg[sid]]) for sid,n in {n.key:n for n in parse(text(ROOT/REG))}.items() if sid not in [POST,PARENT]) and without_caps(regs[PARENT])==without_caps(oldreg[PARENT])
 checks['only_one_fishing_capacity_removed']=normalized([z for z in regs[PARENT].children('capped_resources')[0].children() if z.key!='building_fishing_wharf'])==normalized([z for z in o.children('capped_resources')[0].children() if z.key!='building_fishing_wharf'])
 locchecks=[]
 for kind in p['hubs']:
  rel=LOC+kind+'.txt';raw=text(ROOT/rel);ns=parse(raw)[0].children('instances')[0].children();node=[z for z in ns if z.one('id')==str(p['id'])];assert len(node)==1
  xyz=[float(v.value) for v in node[0].children('position')[0].children()];locchecks.append(new[int(new.shape[0]-xyz[2]),int(xyz[0])]==int(NEW[1:],16))
  before=parse(text(OUT/'before'/rel))[0].children('instances')[0].children();locchecks.append(normalized(before)==normalized([z for z in ns if z.one('id')!=str(p['id'])]))
 checks['new_locators_on_land_old_locators_unchanged']=all(locchecks)
 x,y=p['hubs']['port'];checks['real_maritime_exit_no_coastline_change']=int(newreg.one('naval_exit_id'))==3065 and new[y+1,x]==0x1FDEFC and 'x1FDEFC' in provs(regs['STATE_RIVER_PLATE'],'provinces')
 neighbours=set()
 for x,y in pixels:
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   r=f'x{new[y+dy,x+dx]:06X}'
   if r!=NEW and r in own:neighbours.update(t for s,t in own[r])
 checks['spanish_land_ring_without_portuguese_corridor']=neighbours=={'SC4'}
 checks['strategic_region_membership_once']=sum(POST in [scalar(v.value) for v in z.children()] for q in effective('common/strategic_regions') for z in walk(parse(text(q))) if z.key=='states')==1
 terrain={n.key.lower():scalar(n.value) for n in parse(text(ROOT/'map_data/province_terrains.txt'))};checks['new_terrain_matches_source']=terrain[NEW.lower()]==terrain[OLD.lower()]
 checks['central_cores_and_r902_preserved']=all(own[r]==prior[r] for r in ['xB0243F','xBB820B','x446C64','x52B247','xD3A197','xCC2135','xCD9ECD','xD9D235'])
 checks['localized_both_languages']=all((ROOT/f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml').read_bytes().startswith(b'\xef\xbb\xbf') and len(re.findall(r'^ (?:STATE_|HUB_NAME_).*:0 ',text(ROOT/f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml'),re.M))==6 for lang in ['french','english'])
 checks['enclave_is_one_connected_visible_patch']=component_count(new[2890:2940,2750:2810]==int(NEW[1:],16))==1 and len(pixels)==51
 checks['source_province_not_fragmented']=component_count(new[2860:2940,2720:2840]==int(OLD[1:],16))<=component_count(old[2860:2940,2720:2840]==int(OLD[1:],16))
 sea={n.key:n for q in effective('map_data/state_regions') if q.name=='99_seas.txt' for n in parse(text(q))}
 goal_id=int(regs['STATE_RIO_DE_JANEIRO'].one('naval_exit_id'));goal=next(n for n in sea.values() if n.one('id')==str(goal_id));water={int(r[1:],16) for n in sea.values() for r in provs(n,'provinces')};adj=graph(new[2300:3000,2700:3350],np.array(sorted(water),dtype=np.uint32));dest={int(r[1:],16) for r in provs(goal,'provinces')};seen={0x1FDEFC:None};q=C.deque([0x1FDEFC]);end=None
 while q:
  u=q.popleft()
  if u in dest:end=u;break
  for v in adj.get(u,{}):
   if v not in seen:seen[v]=u;q.append(v)
 route=[]
 while end is not None:route.append(f'x{end:06X}');end=seen[end]
 checks['open_water_connection_to_existing_rio_exit']=bool(route)
 dump('MARITIME_SETUP.json',dict(enclave_exit=3065,rio_de_janeiro_exit=goal_id,water_rgb_route=list(reversed(route)),land_corridor=False,port_levels=1,commercial_harbor_workforce=700,merchant_marine_output_at_full_employment=6,engine_market_access_tested=False))
 newbuilding=state_nodes(text(ROOT/'common/history/buildings/1776_sacramento.txt'))[POST].children('region_state:BRZ')[0].children('create_building')[0]
 checks['one_explicit_commercial_port_initialized']=newbuilding.one('building')=='building_port' and newbuilding.one('level')=='1' and set(provs(newbuilding,'activate_production_methods'))=={'pm_aor1776_traditional_commercial_harbor','pm_1776_no_raw_data_reporting'}
 external={r:dict(before_sha256=base.get(r),observed_sha256=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change']=not external
 checks={k:bool(v) for k,v in checks.items()}
 dump('VALIDATION.json',dict(checks=checks,passed=sum(checks.values()),total=len(checks),all_pass=all(checks.values()),engine_tested=False));print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())

def preview(staged=False):
 a=raster(OUT/'patch'/BIT if staged else ROOT/BIT);x0,y0,x1,y1=2755,2890,2830,2945;b=a[y0:y1,x0:x1];own=ownership();img=np.full((*b.shape,3),[36,49,60],dtype=np.uint8)
 for r,v in own.items():
  color=[111,144,183] if any(t=='SC4' for s,t in v) else [125,123,93]
  img[b==int(r[1:],16)]=color
 img[b==int(NEW[1:],16)]=[250,208,60];border=np.zeros(b.shape,bool);border[:,1:]|=b[:,1:]!=b[:,:-1];border[1:]|=b[1:]!=b[:-1];img[border]=[46,60,70]
 canvas=Image.new('RGB',(1200,1040),(36,49,60));canvas.paste(Image.fromarray(img).resize((1200,880),Image.Resampling.NEAREST),(0,90));d=ImageDraw.Draw(canvas);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
 d.text((20,15),'Sacramento portugaise — 1er janvier 1776',font=f,fill='white');d.text((20,50),'Enclave agrandie pour être visible ; possessions espagnoles en bleu.',font=f,fill='white')
 p=load('PLAN.json');x,y=p['hubs']['city'];xx,yy=(x-x0)*16,(y-y0)*16+90;d.line((xx,yy,xx+120,yy-100),fill='white',width=2);d.text((xx+125,yy-120),'Colônia do Sacramento',font=f,fill='white');d.text((20,985),'Aucun corridor terrestre. Port et desserte maritime préparés ; test en jeu à effectuer.',font=f,fill='white');canvas.save(OUT/'R9_03_SACRAMENTO.png')

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:
  if (OUT/'SHARED_URUGUAY_FEEDBACK/APPLIED.json').exists():
   from r903_shared_uruguay import verify as verify_current
   verify_current()
  else:verify()
 elif '--verify-initial' in sys.argv:verify()
 elif '--preview' in sys.argv:preview('--staged' in sys.argv)
