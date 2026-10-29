"""Bounded DP-03 installation. Whole native cells; historical limits in DP-03/REPORT.md.

Separate prepare/apply with current-file hash guards. Never rewrites earlier proofs.
"""
from dp01 import ROOT,GAME,effective,provs,sha,runtime,text,state_nodes,encoded,edit,rgb_block,parse,walk,scalar,normalized
from dp01_install import normalized_owners,LAWS,split_pops
from dp02_refine import stock_units
from arabia01_install import popstock
import collections as C,json,re,sys

OUT=ROOT/'docs/reports/map/DURRANI_PUNJAB_1776/DP-03'
ST='common/history/states/00_states.txt'
POP='common/history/pops/10_india.txt'
MIL='common/history/military_formations/04_military_formations_middle_east.txt'
UNIT='common/history/military_formations/1776_dp03.txt'
REG='map_data/state_regions/10_india.txt'
SCOPE=['STATE_KASHMIR','STATE_HILL_PUNJAB']
NEW={
 'D3G':dict(name='Gilgit',culture='kho',religion='shiite',ruler='Guritham',color=[137,169,105]),
 'D3S':dict(name='Skardu',culture='tibetan',religion='shiite',ruler='Murad Khan II',color=[151,117,171])}
MOVES=[
 ('x251424','STATE_HILL_PUNJAB','D2K','D2C','Chamba court core; Yale map; DP-02 dated court research'),
 ('xE31B4E','STATE_HILL_PUNJAB','D2B','D2U','Kullu court core; Yale map; DP-02 dated court research'),
 ('x0003C6','STATE_HILL_PUNJAB','GAR','D2B','Rampur/Bashahr court core; Yale map; DP-02 dated court research'),
 ('x5990A7','STATE_KASHMIR','DUR','LAD','Purig/Kargil; Grist p99: incorporation into Ladakh in 1758'),
 ('x5A0252','STATE_KASHMIR','DUR','D3G','Gilgit; Keene 1909 pp44-45 local rule, Guritham after circa 1770'),
 ('x6326A6','STATE_KASHMIR','DUR','D3S','Skardu; Murad II local court; 1779 Afghan expedition not anticipated')]
LOC={
 'city':dict(point=[5800.5,0.0,2319.5],rgb='x3FDA5A'),
 'mine':dict(point=[5829.5,0.0,2331.5],rgb='x5990A7')}

def dump(n,v):
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def put(files,rel,s):files[rel]=encoded(ROOT/rel,s) if (ROOT/rel).exists() else s.encode('utf8')

def tech(name,tags):
 from validate_starting_technology_1776 import collect_snapshot,audit_country
 snapshot=collect_snapshot()
 rows=[audit_country(t,snapshot,{'historical_evidence':'DP-03/SOURCES.md and REPORT.md: local agrarian courts, traditional food processing and irregular levies only; no industrial profile.'}) for t in tags]
 dump(name,rows);return rows

def prepare():
 assert not (OUT/'APPLIED.json').exists(),'Already installed; preserve receipt'
 files={};before=runtime();ow=normalized_owners()
 definitions={n.key for p in effective('common/country_definitions') for n in parse(text(p))}
 assert not set(NEW)&definitions,'TAG collision'
 transfers=[]
 for r,s,a,b,source in MOVES:
  assert ow[r]=={(s,a)},(r,ow.get(r))
  transfers.append(dict(rgb=r,state=s,before=a,after=b,evidence=source,supersedes='DP-02' if a in ['D2K','D2B','GAR'] else None))
 raw=text(ROOT/ST);patch=[]
 for sid in SCOPE:
  n=state_nodes(raw)[sid];by=C.defaultdict(set);old={}
  for q in n.children('create_state'):
   tag=scalar(q.one('country'))[2:];by[tag]|=set(provs(q,'owned_provinces'));old[tag]=q
  for z in transfers:
   if z['state']==sid:by[z['before']].remove(z['rgb']);by[z['after']].add(z['rgb'])
  assert all(by[t] for t in old),'No accidental deletion of state portions'
  for t,q in old.items():
   if by[t]!=set(provs(q,'owned_provinces')):
    p=q.children('owned_provinces')[0];patch.append((p.start,p.end,'owned_provinces = '+rgb_block(by[t])))
  patch.append((n.end-1,n.end-1,''.join('\n create_state = { country = c:'+t+' owned_provinces = '+rgb_block(rs)+' }\n' for t,rs in by.items() if t not in old)))
 put(files,ST,edit(raw,patch))
 # Whole current cohorts, no invented residents, religious conversions or pixel densities.
 raw=text(ROOT/POP);n=state_nodes(raw)['STATE_KASHMIR'];src=n.children('region_state:DUR')[0]
 ps=src.children('create_pop')
 assert [(scalar(p.one('culture')),int(p.one('size'))) for p in ps]==[('kashmiri',933473),('tibetan',11661),('kashmiri',228050),('pashtun',43125),('kho',34533),('kashmiri',11559),('tibetan',7281),('panjabi',3575)]
 src,body,ledger=split_pops(raw,'STATE_KASHMIR',{'D3G':[4],'D3S':[1,5]})
 new=edit(raw,[(src.start,src.end,body)]);assert popstock(raw)==popstock(new)
 put(files,POP,new);dump('POP_LEDGER.json',dict(allocations=ledger,policy='Technical allocation of intact existing cohorts, not historical country censuses. Hill-country cohort stocks unchanged; fine resident allocation unresolved.'))
 # Reassign two existing conscripts, preserving regional unit stock and all regulars.
 raw=text(ROOT/MIL);matches=[u for c in walk(parse(raw)) if c.key=='c:DUR' for f in c.children('create_military_formation') for u in f.children('combat_unit') if scalar(u.one('state_region'))=='s:STATE_KASHMIR' and scalar(u.one('service_type','regular'))=='conscript']
 assert len(matches)==1 and int(matches[0].one('count'))==7
 q=matches[0].children('count')[0];put(files,MIL,edit(raw,[(q.start,q.end,'count = 5')]))
 unit='MILITARY_FORMATIONS = {\n'+''.join('c:'+t+' ?= { create_military_formation = { type = army hq_region = sr:region_north_india name = aor1776_dp03_levy combat_unit = { type = unit_type:combat_unit_type_irregular_infantry service_type = conscript state_region = s:STATE_KASHMIR count = 1 } } }\n' for t in NEW)+'}\n'
 assert stock_units(raw)==stock_units(files[MIL].decode('utf-8-sig'))+stock_units(unit)
 put(files,UNIT,unit)
 # Reuse bounded native law variants, restricting them to these two new governments.
 laws=text(ROOT/'common/laws/1776_dp02.txt').replace('aor1776_dp02','aor1776_dp03')
 patches=[]
 for n in parse(laws):
  for key in ['is_visible','can_enact']:
   q=n.children(key);assert len(q)==1
   patches.append((q[0].start,q[0].end,key+' = { OR = { c:D3G ?= this c:D3S ?= this } }'))
 put(files,'common/laws/1776_dp03.txt',edit(laws,patches))
 defs=[]
 for t,v in NEW.items():
  defs.append(t+' = { color = { '+' '.join(map(str,v['color']))+' } country_type = unrecognized tier = principality cultures = { '+v['culture']+' } religion = '+v['religion']+' capital = STATE_KASHMIR }')
  technologies=['improved_husbandry','international_relations','traditional_food_processing','organized_military_establishments']
  lawlist=[v for v in LAWS if v!='people_of_the_book']+['aor1776_dp03_customs','aor1776_dp03_customary_bondage','aor1776_dp03_toleration']
  put(files,'common/history/countries/1776_dp03_'+t.lower()+'.txt','COUNTRIES = { c:'+t+' ?= {\n'+''.join(' add_technology_researched = '+x+'\n' for x in technologies)+''.join(' activate_law = law_type:law_'+x+'\n' for x in lawlist)+' set_state_religion = rel:'+v['religion']+'\n ig:ig_landowners ?= { add_ruling_interest_group = yes }\n} }\n')
  put(files,'common/history/characters/1776_dp03_'+t.lower()+'.txt','CHARACTERS = { c:'+t+' ?= { create_character = { historical = yes ruler = yes first_name = aor1776_dp03_ruler_'+t.lower()+' last_name = aor1776_dp03_empty culture = cu:'+v['culture']+' religion = rel:'+v['religion']+' interest_group = ig_landowners ideology = ideology_traditionalist } } }\n')
 put(files,'common/country_definitions/1776_dp03.txt','\n'.join(defs)+'\n')
 # Symbolic plain banners, not claimed as attested historical flags.
 put(files,'common/coat_of_arms/coat_of_arms/1776_dp03.txt','aor1776_dp03_gilgit = { pattern = "pattern_solid.tga" color1 = "green" }\naor1776_dp03_skardu = { pattern = "pattern_solid.tga" color1 = "purple" }\n')
 put(files,'common/flag_definitions/1776_dp03.txt',''.join(t+' = { flag_definition = { coa = aor1776_dp03_'+v['name'].lower()+' priority = 100 allow_overlord_canton = no } }\n' for t,v in NEW.items()))
 # Loose Afghan allegiance, not direct administration or a retrospective 1779 conquest.
 put(files,'common/history/diplomacy/1776_dp03.txt','DIPLOMACY = { c:DUR ?= { create_diplomatic_pact = { country = c:D3S type = aor1776_dp02_allegiance } } }\n')
 # Native State_Region hubs must agree with locator points, not their old labels.
 raw=text(ROOT/REG);n=next(n for n in parse(raw) if n.key=='STATE_KASHMIR');patch=[]
 assert n.one('id')=='463'
 for kind,v in LOC.items():
  q=n.children(kind)[0];patch.append((q.start,q.end,kind+' = "'+v['rgb']+'"'))
 put(files,REG,edit(raw,patch))
 for kind,v in LOC.items():
  rel='gfx/map/map_object_data/generated_map_object_locators_'+kind+'.txt';raw=text(ROOT/rel)
  ns=[n for n in walk(parse(raw)) if n.children('id') and n.one('id')=='463' and n.children('position')]
  assert len(ns)==1,(kind,len(ns));q=ns[0].children('position')[0]
  put(files,rel,edit(raw,[(q.start,q.end,'position={ '+' '.join(f'{a:.6f}' for a in v['point'])+' }')]))
 for lang in ['french','english']:
  fr=lang=='french';vals={t:v['name'] for t,v in NEW.items()}
  vals.update({t+'_ADJ':('de '+v['name'] if fr else v['name']) for t,v in NEW.items()})
  vals.update({'aor1776_dp03_ruler_'+t.lower():v['ruler'] for t,v in NEW.items()})
  vals.update({'aor1776_dp03_empty':'','aor1776_dp03_levy':'Levée locale' if fr else 'Local levy'})
  vals.update({k.replace('dp02','dp03'):v for k,v in re.findall(r'^\s*(law_aor1776_dp02[^:]+):0\s+"(.*)"',text(ROOT/'localization'/lang/'replace'/('1776_dp02_l_'+lang+'.yml')),re.M)})
  files['localization/'+lang+'/replace/1776_dp03_l_'+lang+'.yml']=b'\xef\xbb\xbf'+('l_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in vals.items())).encode('utf8')
 manifest=[]
 for rel,data in files.items():
  p=ROOT/rel;old=p.read_bytes() if p.exists() else None
  if old==data:continue
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  q=OUT/'staged'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  if old is not None:q=OUT/'preimages'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
  manifest.append(dict(file=rel,before_sha256=sha(p) if p.exists() else None,after_sha256=sha(OUT/'staged'/rel)))
 dump('PREPARED.json',dict(files=manifest,world_before=before,ownership_before={r:sorted(v) for r,v in ow.items()}))
 dump('PLAN.json',dict(transfers=transfers,locators=LOC,policy='Existing native whole-cell cores; tiny shared jurisdictions remain abstracted, never certified as annexed.'))
 print(json.dumps(dict(files=len(manifest),transfers=len(transfers))))

def apply():
 assert not (OUT/'APPLIED.json').exists()
 m=load('PREPARED.json');tech('TECH_BEFORE.json',['DUR','PAN','LAD','D2K','D2C','D2U','D2B','GAR'])
 for z in m['files']:
  p=ROOT/z['file'];assert (sha(p) if p.exists() else None)==z['before_sha256'],('Concurrent change',z['file'])
  assert sha(OUT/'staged'/z['file'])==z['after_sha256']
 for z in m['files']:
  p=ROOT/z['file'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((OUT/'staged'/z['file']).read_bytes())
 dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files=m['files'],runtime_validated=False))
 print('DP-03 installed; independent static and runtime checks still required.')

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
