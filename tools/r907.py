"""R9-07 bounded Chaco/Malvinas installation. Never restores shared baselines."""
import collections as C,json,sys,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,ownership
from validate_diplomacy_ottoman_1776 import parse,scalar,normalized
from central01 import cohorts
from r904 import assigns
from hbc02_map_candidates import graph
OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-07'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt'
MOVES=[('STATE_SANTA_FE','x7F79B5','GNI','SC4'),('STATE_SANTA_FE','x453036','GNI','SC4')]+[('STATE_SOUTH_ATLANTIC_ISLANDS',r,'GBR','SC4') for r in ['x3020D0','x5E9DB3','x9EF337']]
PORT='common/history/buildings/1776_r907_malvinas_port.txt'
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def prepare():
 assert not (OUT/'APPLIED.json').exists()
 own=ownership();raw=text(ROOT/ST);ns=state_nodes(raw);ed=[]
 for sid in ['STATE_SANTA_FE','STATE_SOUTH_ATLANTIC_ISLANDS']:
  n=ns[sid];old=n.children('create_state');target={scalar(z.one('country'))[2:]:set(provs(z,'owned_provinces')) for z in old}
  for s,r,b,t in MOVES:
   if s==sid:
    assert own[r]=={(s,b)};target[b].remove(r);target.setdefault(t,set()).add(r)
  for z in old:
   tag=scalar(z.one('country'))[2:];p=z.children('owned_provinces')[0];ed.append((p.start,p.end,'owned_provinces = '+rgb_block(target[tag])))
  if sid=='STATE_SOUTH_ATLANTIC_ISLANDS':
   ed.append((n.end-1,n.end-1,'\n\t\tcreate_state = { country = c:SC4 owned_provinces = '+rgb_block(target['SC4'])+' state_type = unincorporated }\n\t\tadd_claim = c:GBR\n\t'))
 files={ST:encoded(ROOT/ST,edit(raw,ed))}
 raw=text(ROOT/PP);n=state_nodes(raw)['STATE_SOUTH_ATLANTIC_ISLANDS'];assert not n.children('region_state:SC4')
 # 115 is an observed April 1774 count reused as a dated proxy, not a 1776 census.
 # Spanish administrative-cultural aggregate; the historical French families are
 # not assigned an invented 1776 ethnic fraction. Existing British stock preserved.
 ins='\n\t\tregion_state:SC4 = { create_pop = { culture = spanish religion = catholic size = 115 } }\n\t'
 files[PP]=encoded(ROOT/PP,edit(raw,[(n.end-1,n.end-1,ins)]))
 files[PORT]=('''# Maritime supply proxy for Puerto Soledad; existing western-island port locator.
# No historical Fox Bay town or full staffing/market access is asserted.
BUILDINGS = { s:STATE_SOUTH_ATLANTIC_ISLANDS = { region_state:SC4 = {
 create_building = { building = building_port level = 1 reserves = 1
 activate_production_methods = { pm_aor1776_traditional_commercial_harbor pm_1776_no_raw_data_reporting } }
} } }
''').encode()
 for lang,name,adj,port in [('french','Peuples du Chaco','chaquéen','Mouillage des Malouines'),('english','Chaco peoples','Chaco','Falklands anchorage')]:
  names={'city':'Puerto Soledad','port':port,'farm':'Campagne de Soledad' if lang=='french' else 'Soledad countryside','mine':'Environs de Soledad' if lang=='french' else 'Soledad surroundings','wood':'Côtes des Malouines' if lang=='french' else 'Falklands coast'}
  s=f'l_{lang}:\n GNI:0 "{name}"\n GNI_ADJ:0 "{adj}"\n'+''.join(f' HUB_NAME_STATE_SOUTH_ATLANTIC_ISLANDS_{k}:0 "{v}"\n' for k,v in names.items())
  files[f'localization/{lang}/replace/1776_r907_chaco_malvinas_l_{lang}.yml']=b'\xef\xbb\xbf'+s.encode('utf8')
 m={'input_sha256':{},'output_sha256':{}}
 for r,b in files.items():
  if r.endswith('.txt'):parse(b.decode('utf-8-sig'))
  p=ROOT/r;q=OUT/'patch'/r;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
  if p.exists():z=OUT/'before'/r;z.parent.mkdir(parents=True,exist_ok=True);z.write_bytes(p.read_bytes())
  m['input_sha256'][r]=sha(p) if p.exists() else None;m['output_sha256'][r]=sha(q)
 dump('PATCH.json',m);dump('PREPARE_RUNTIME.json',runtime());dump('PLAN.json',{'reference_date':'1776-01-01','transfers':MOVES,'new_population':115,'population_proxy_date':'1774-04-04','population_reassigned':0,'preserved_british_composite_region_population':10469,'new_buildings':{'port_level':1},'new_countries':0,'new_state_regions':0,'new_RGBs':0,'engine_tested':False})
 print(json.dumps({'files':len(files),'province_transfers':len(MOVES),'new_population':115,'new_port_levels':1}))
def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists()
 assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==h for r,h in m['input_sha256'].items()),'Shared file changed: re-examine patch'
 assert all(sha(OUT/'patch'/r)==h for r,h in m['output_sha256'].items())
 for r in m['output_sha256']:(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',{'date':'2026-10-28','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','engine_tested':False})
def verify():
 m=load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();ck={};old=assigns(text(OUT/'before'/ST));new=assigns(text(ROOT/ST));expected=old.copy()
 for s,r,b,t in MOVES:assert expected[r,s,b]==1;expected[r,s,b]-=1;expected[r,s,t]+=1
 ck['only_five_authorized_transfers']=+expected==new
 def counts(c):
  z=C.Counter()
  for (r,s,t),v in c.items():z[r]+=v
  return z
 ck['no_new_duplicate_or_unowned_province']=counts(old)==counts(new)
 ck['installed_files_match_manifest']=all(sha(ROOT/r)==h for r,h in m['output_sha256'].items())
 ck['modified_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'] if r.endswith('.txt'))
 ns=state_nodes(text(ROOT/ST));oldns=state_nodes(text(OUT/'before'/ST));ps=state_nodes(text(ROOT/PP));oldps=state_nodes(text(OUT/'before'/PP))
 ck['all_other_state_blocks_preserved']=all(normalized([n])==normalized([oldns[s]]) for s,n in ns.items() if s not in ['STATE_SANTA_FE','STATE_SOUTH_ATLANTIC_ISLANDS'])
 ck['all_other_population_regions_preserved']=all(normalized([n])==normalized([oldps[s]]) for s,n in ps.items() if s!='STATE_SOUTH_ATLANTIC_ISLANDS')
 n=ps['STATE_SOUTH_ATLANTIC_ISLANDS'];oldn=oldps['STATE_SOUTH_ATLANTIC_ISLANDS'];ck['british_10469_cohort_preserved']=normalized(n.children('region_state:GBR'))==normalized(oldn.children('region_state:GBR'))
 pop=n.children('region_state:SC4')[0].children('create_pop');ck['dated_115_spanish_proxy_only']=len(pop)==1 and pop[0].one('size')=='115' and pop[0].one('culture')=='spanish' and pop[0].one('religion')=='catholic'
 oldc=cohorts(text(OUT/'before'/PP));newc=cohorts(text(ROOT/PP));ck['world_population_delta_exactly_115']=sum(newc.values())-sum(oldc.values())==115 and not (oldc-newc)
 ck['all_existing_buildings_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith('common/history/buildings/'))
 ck['only_one_new_building_file']=set(r for r in now if r.startswith('common/history/buildings/') and r not in base)=={PORT}
 ck['bitmap_regions_terrain_locators_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/')))
 ck['country_definitions_profiles_diplomacy_units_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/country_definitions/','common/history/countries/','common/history/diplomacy/','common/history/military_formations/')))
 regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))};own=ownership()
 ck['transferred_RGBs_belong_to_region_and_are_passable']=all(r in provs(regs[s],'provinces') and r not in provs(regs[s],'impassable') for s,r,b,t in MOVES)
 ck['no_other_atlantic_island_transferred']=all(own[r]=={('STATE_SOUTH_ATLANTIC_ISLANDS','GBR')} for r in ['x0CB556','xB0BDDF','xB5100C','xB5760C'])
 ck['british_claim_retained']=any(scalar(z.value)=='c:GBR' for z in ns['STATE_SOUTH_ATLANTIC_ISLANDS'].children('add_claim'))
 ck['asuncion_santiago_san_fernando_preserved']=all(own[r]=={(s,t)} for r,s,t in [('xB63BAD','STATE_BAJO_PARAGUAY','SC4'),('xCCC385','STATE_BAJO_PARAGUAY','SC4'),('xE0C49E','STATE_CHACO','SC4'),('xB0C011','STATE_CHACO','GNI')])
 ck['prior_R9_CENTRAL_witnesses_preserved']=all(own[r]=={(s,t)} for r,s,t in [('xC564C3','STATE_ANTIOQUIA','WYU'),('x7B4B5E','STATE_GUAYANA','NET'),('x439BC2','STATE_GUAYANA','FRA'),('x6C6251','STATE_GUAYANA','NET'),('x3C0D20','STATE_PASTAZA','BRZ'),('x144683','STATE_ARAUCANIA','H91'),('xF2263F','STATE_LOS_RIOS','PAT'),('x4E1443','STATE_URUGUAY','BRZ'),('xB0243F','STATE_COSTA_RICA','G81'),('xBB820B','STATE_PANAMA','K81'),('x446C64','STATE_WEST_INDIES','C81')])
 shares={(s,scalar(z.one('country'))[2:]) for s,n in ns.items() for z in n.children('create_state')};ck['all_affected_population_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s in ['STATE_SANTA_FE','STATE_SOUTH_ATLANTIC_ISLANDS'] for rs in ps[s].children() if rs.children('create_pop'))
 r=regs['STATE_SOUTH_ATLANTIC_ISLANDS'];ck['malvinas_city_and_port_owned_by_SC4']=all(own[scalar(r.one(k))]=={('STATE_SOUTH_ATLANTIC_ISLANDS','SC4')} for k in ['city','port'])
 bs=parse(text(ROOT/PORT))[0].children()[0].children()[0].children('create_building');ck['one_traditional_port_level']=len(bs)==1 and bs[0].one('level')=='1' and scalar(bs[0].one('building'))=='building_port'
 ck['localization_BOM_keys_and_language_headers']=all((ROOT/f'localization/{l}/replace/1776_r907_chaco_malvinas_l_{l}.yml').read_bytes().startswith(b'\xef\xbb\xbf') and text(ROOT/f'localization/{l}/replace/1776_r907_chaco_malvinas_l_{l}.yml').startswith('l_'+l+':') and len(re.findall(r'(?m)^\s+\w+:0 ',text(ROOT/f'localization/{l}/replace/1776_r907_chaco_malvinas_l_{l}.yml')))==7 for l in ['french','english'])
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];colors=[int(r[1:],16) for r,v in own.items() if ('STATE_SANTA_FE','SC4') in v];g=graph(a,np.array(colors,dtype=np.uint32));route=['x7F79B5','x453036','x257673'];ck['san_jeronimo_connected_land_route']=all(g[int(u[1:],16)].get(int(v[1:],16),0)>=2 for u,v in zip(route[:-1],route[1:]))
 external={r:{'before':base.get(r),'after':now.get(r)} for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);ck['no_unlisted_runtime_change_since_prepare']=not external
 ck={k:bool(v) for k,v in ck.items()};dump('VALIDATION.json',{'date':'2026-10-28','checks':ck,'passed':sum(ck.values()),'total':len(ck),'engine_tested':False,'human_validated':False});print(json.dumps({'passed':sum(ck.values()),'total':len(ck),'failed':[k for k,v in ck.items() if not v]}));assert all(ck.values())
def preview():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];oldsets=C.defaultdict(set)
 for r,s,t in assigns(text(OUT/'before'/ST)):oldsets[r].add(t)
 colors={'GNI':(90,157,116),'SC4':(207,147,75),'GBR':(104,137,186),'SC3':(153,106,73),'BRZ':(176,160,58)};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
 newsets={r:{t for s,t in v} for r,v in ownership().items()}
 for name,box,scale in [('CHACO',(2600,2530,2855,2870),2),('MALOUINES',(2690,3370,2790,3435),4)]:
  x0,y0,x1,y1=box;crop=a[y0:y1,x0:x1];w=(x1-x0)*scale;h=(y1-y0)*scale;im=Image.new('RGB',(w*2+30,h+100),(35,48,59));d=ImageDraw.Draw(im)
  for i,own in enumerate([oldsets,newsets]):
   rgb=np.full((*crop.shape,3),[35,48,59],dtype='uint8')
   for c in np.unique(crop):
    o=own.get(f'x{int(c):06X}',set());tag=next(iter(o)) if len(o)==1 else '';rgb[crop==c]=colors.get(tag,(35,48,59))
   edge=np.zeros(crop.shape,bool);edge[1:,:]|=crop[1:,:]!=crop[:-1,:];edge[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edge]//=2;im.paste(Image.fromarray(rgb).resize((w,h),Image.Resampling.NEAREST),(10+i*(w+10),35));d.text((10+i*(w+10),8),['Avant','R9-07 installé — 1776'][i],font=font,fill='white')
  d.text((12,h+45),'Vert : peuples du Chaco | Or : SC4 | Bleu : Grande-Bretagne',font=small,fill='white');d.text((12,h+69),'Limites par provinces existantes ; validation en jeu différée.',font=small,fill='white');im.save(OUT/f'R9_07_{name}_AVANT_APRES.png')
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
 elif '--preview' in sys.argv:preview()
