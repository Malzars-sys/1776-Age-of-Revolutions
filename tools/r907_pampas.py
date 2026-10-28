"""Additive R9-07 correction of deep Cuyo/Pampas interior, using current files."""
import collections as C,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,ownership
from validate_diplomacy_ottoman_1776 import parse,scalar,normalized
from r904 import assigns
from central01 import cohorts
OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-07/PAMPAS_CUYO'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt'
MOVES={'STATE_LA_PAMPA':'x31058F xEF8010 x6FD2C8 x7B3596 x056575'.split(),'STATE_RIO_NEGRO':'x2B18E0 xFDEBB0 x745CF8 x08B647 x3F05E8 x443E92 xDC370A x11E04B xD81D58 xEBA1B5 xC1D1A9 x4178C7 x537183 x8976A7 xC1A1C8 x8C91D6 xB00090 xF5005C x30E94A xF8B9BC x2B5897'.split()}
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def prepare():
 OUT.mkdir(exist_ok=True);assert not (OUT/'APPLIED.json').exists();own=ownership();raw=text(ROOT/ST);ns=state_nodes(raw);ed=[]
 for s,rr in MOVES.items():
  n=ns[s];parts=n.children('create_state');target={scalar(z.one('country'))[2:]:set(provs(z,'owned_provinces')) for z in parts}
  for r in rr:assert own[r]=={(s,'SC4')};target['SC4'].remove(r);target.setdefault('PAT',set()).add(r)
  for z in parts:
   tag=scalar(z.one('country'))[2:];p=z.children('owned_provinces')[0];ed.append((p.start,p.end,'owned_provinces = '+rgb_block(target[tag])))
  if s=='STATE_LA_PAMPA':
   ed.append((n.end-1,n.end-1,'\n\t\tcreate_state = { country = c:PAT owned_provinces = '+rgb_block(target['PAT'])+' }\n\t\tadd_claim = c:SC4\n\t'))
 files={ST:encoded(ROOT/ST,edit(raw,ed))};raw=text(ROOT/PP);ps=state_nodes(raw);ed=[]
 for sid,size in [('STATE_LA_PAMPA','8871'),('STATE_RIO_NEGRO','3815')]:
  n=ps[sid];rs=n.children('region_state:SC4')[0];pops=[z for z in rs.children('create_pop') if z.one('culture')=='patagonian'];assert len(pops)==1 and pops[0].one('size')==size;z=pops[0];ed.append((z.start,z.end,''));dest=n.children('region_state:PAT')
  if dest:ed.append((dest[0].end-1,dest[0].end-1,'\n'+raw[z.start:z.end]+'\n'))
  else:ed.append((n.end-1,n.end-1,'\n\t\tregion_state:PAT = { '+raw[z.start:z.end]+' }\n\t'))
 files[PP]=encoded(ROOT/PP,edit(raw,ed))
 for lang,name,adj in [('french','Peuples mapuche et pampéens','mapuche et pampéen'),('english','Mapuche and Pampas peoples','Mapuche and Pampas')]:
  files[f'localization/{lang}/replace/1776_r907_pampas_l_{lang}.yml']=b'\xef\xbb\xbf'+f'l_{lang}:\n PAT:0 "{name}"\n PAT_ADJ:0 "{adj}"\n'.encode()
 m={'input_sha256':{},'output_sha256':{}}
 for r,b in files.items():
  if r.endswith('.txt'):parse(b.decode('utf-8-sig'))
  p=ROOT/r;q=OUT/'patch'/r;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
  if p.exists():z=OUT/'before'/r;z.parent.mkdir(parents=True,exist_ok=True);z.write_bytes(p.read_bytes())
  m['input_sha256'][r]=sha(p) if p.exists() else None;m['output_sha256'][r]=sha(q)
 dump('PATCH.json',m);dump('PREPARE_RUNTIME.json',runtime());dump('PLAN.json',{'reference_date':'1776-01-01','transfers':MOVES,'province_count':sum(map(len,MOVES.values())),'population_reassigned':12686,'new_population':0,'new_TAG':False,'historical_limit':'Conservative deep interior beyond documented San Carlos frontier. Retained intermediate provinces remain reservations, not a certified 1776 frontier. PAT is a regional gameplay aggregate, not a single historical Mapuche state.'});print(json.dumps({'files':len(files),'transfers':sum(map(len,MOVES.values())),'population_reassigned':12686}))
def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists();assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==h for r,h in m['input_sha256'].items())
 for r,h in m['output_sha256'].items():
  assert sha(OUT/'patch'/r)==h;(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',{'date':'2026-10-28','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','engine_tested':False})
def verify():
 m=load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();ck={};old=assigns(text(OUT/'before'/ST));new=assigns(text(ROOT/ST));expected=old.copy()
 for s,rr in MOVES.items():
  for r in rr:expected[r,s,'SC4']-=1;expected[r,s,'PAT']+=1
 ck['only_26_authorized_transfers']=+expected==new;ck['output_hashes_match']=all(now.get(r)==h for r,h in m['output_sha256'].items())
 ck['changed_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'] if r.endswith('.txt'))
 a=state_nodes(text(OUT/'before'/ST));b=state_nodes(text(ROOT/ST));pa=state_nodes(text(OUT/'before'/PP));pb=state_nodes(text(ROOT/PP));ck['all_other_state_blocks_identical']=all(normalized([n])==normalized([a[s]]) for s,n in b.items() if s not in MOVES);ck['all_other_population_blocks_identical']=all(normalized([n])==normalized([pa[s]]) for s,n in pb.items() if s not in MOVES)
 ck['all_regional_population_identities_conserved']=cohorts(text(ROOT/PP))==cohorts(text(OUT/'before'/PP))
 for sid,size in [('STATE_LA_PAMPA','8871'),('STATE_RIO_NEGRO','3815')]:
  aa=pa[sid].children('region_state:SC4')[0].children('create_pop');bb=pb[sid].children('region_state:SC4')[0].children('create_pop');native=[z for z in aa if z.one('culture')=='patagonian'];dest=pb[sid].children('region_state:PAT')[0].children('create_pop');ck['intact_cohort_'+sid]=len(native)==1 and native[0].one('size')==size and any(normalized([z])==normalized(native) for z in dest) and normalized([z for z in aa if z.one('culture')!='patagonian'])==normalized(bb)
 own=ownership();ck['all_31_R907_transfers_retained']=all(own[r]=={(s,t)} for s,r,_,t in __import__('r907').MOVES) and all(own[r]=={(s,'PAT')} for s,rr in MOVES.items() for r in rr)
 regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))};ck['correct_regions_no_impassable_transfers']=all(r in provs(regs[s],'provinces') and r not in provs(regs[s],'impassable') for s,rr in MOVES.items() for r in rr)
 ck['all_previous_buildings_profiles_units_diplomacy_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/countries/','common/country_definitions/','common/history/military_formations/','common/history/diplomacy/')))
 ck['bitmap_state_regions_locators_identical']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/')))
 ck['all_SC4_hubs_preserved']=all(own[scalar(regs[s].one(k))]=={(s,'SC4')} for s in MOVES for k in ['city','mine','wood']) and own['x700090']=={('STATE_LA_PAMPA','SC4')}
 ck['preexisting_PAT_farm_preserved']=own['x19A814']=={('STATE_RIO_NEGRO','PAT')}
 shares={(s,scalar(z.one('country'))[2:]) for s,n in b.items() for z in n.children('create_state')};ck['population_scopes_have_land']=all((s,rs.key.split(':')[1]) in shares for s in MOVES for rs in pb[s].children() if rs.children('create_pop'))
 ck['claims_retained']=all(any(scalar(z.value)=='c:SC4' for z in b[s].children('add_claim')) for s in MOVES)
 for l in ['french','english']:
  p=ROOT/f'localization/{l}/replace/1776_r907_pampas_l_{l}.yml';ck['localization_'+l]=p.read_bytes().startswith(b'\xef\xbb\xbf') and text(p).startswith('l_'+l+':')
 external={r:{'before':base.get(r),'after':now.get(r)} for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);ck['no_unlisted_change_since_prepare']=not external
 ck={k:bool(v) for k,v in ck.items()};dump('VALIDATION.json',{'date':'2026-10-28','checks':ck,'passed':sum(ck.values()),'total':len(ck),'engine_tested':False,'human_validated':False});print(json.dumps({'passed':sum(ck.values()),'total':len(ck),'failed':[k for k,v in ck.items() if not v]}));assert all(ck.values())
def preview():
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];x0,y0,x1,y1=2475,2850,2710,3020;crop=a[y0:y1,x0:x1];scale=3;w=(x1-x0)*scale;h=(y1-y0)*scale;im=Image.new('RGB',(w*2+30,h+100),(35,48,59));d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);old=C.defaultdict(set)
 for r,s,t in assigns(text(OUT/'before'/ST)):old[r].add(t)
 new={r:{t for s,t in v} for r,v in ownership().items()};colors={'SC4':(207,147,75),'SC3':(153,106,73),'PAT':(121,170,128),'H91':(65,126,107)}
 for i,own in enumerate([old,new]):
  rgb=np.full((*crop.shape,3),[35,48,59],dtype='uint8')
  for c in np.unique(crop):
   v=own.get(f'x{int(c):06X}',set());rgb[crop==c]=colors.get(next(iter(v)) if len(v)==1 else '',(35,48,59))
  edge=np.zeros(crop.shape,bool);edge[1:,:]|=crop[1:,:]!=crop[:-1,:];edge[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edge]//=2;im.paste(Image.fromarray(rgb).resize((w,h),Image.Resampling.NEAREST),(10+i*(w+10),35));d.text((10+i*(w+10),8),['Avant','R9-07 installé — 1776'][i],font=font,fill='white')
 d.text((12,h+45),'Vert : peuples mapuche et pampéens | Or : SC4 | Brun : SC3',font=font,fill='white');d.text((12,h+70),'Correction du noyau intérieur ; marges intermédiaires encore réservées.',font=font,fill='white');im.save(OUT/'R9_07_CUYO_PAMPAS_AVANT_APRES.png')
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
 elif '--preview' in sys.argv:preview()
