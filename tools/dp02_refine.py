"""DP-02: bounded current-workspace refinements; prepare/apply/audit are separate.

Whole-cell approximations, not surveyed historical borders. No new people or units.
DP-01 preimages and receipts are immutable inputs, never restored wholesale.
"""
from dp01_install import inside, renamed, normalized_owners, LAWS
from dp01 import ROOT,GAME,effective,provs,sha,runtime,text,state_nodes,encoded,edit,rgb_block,parse,walk,scalar,normalized
from arabia01_install import popstock,buildingstock
import collections as C,json,re,sys
from pathlib import Path
OUT=ROOT/'docs/reports/map/DURRANI_PUNJAB_1776/DP-02'
ST='common/history/states/00_states.txt'
SCOPE=['STATE_BALUCHISTAN','STATE_PUNJAB','STATE_HILL_PUNJAB','STATE_KASHMIR']
NEW={
 'D2J':('Jammu','Jammu','STATE_KASHMIR','pahari','hindu','Ranjit Dev',None,[191,120,78]),
 'D2K':('Kangra','Kangra','STATE_HILL_PUNJAB','pahari','hindu','Sansar Chand II',10,[161,153,71]),
 'D2C':('Chamba','Chamba','STATE_HILL_PUNJAB','pahari','hindu','Raj Singh',20,[188,111,129]),
 'D2M':('Mandi','Mandi','STATE_HILL_PUNJAB','pahari','hindu','Shamsher Sen',53,[87,142,95]),
 'D2U':('Kullu','Kullu','STATE_HILL_PUNJAB','pahari','hindu','Pritam Singh',None,[137,110,180]),
 'D2S':('Sirmur','Sirmur','STATE_HILL_PUNJAB','pahari','hindu','Jagat Prakash',None,[185,152,116]),
 'D2B':('Bashahr','Bashahr','STATE_HILL_PUNJAB','pahari','hindu','Ugar Singh',None,[109,153,176])}
EXISTING={
 'BHW':('bhw - bahawalpur.txt','panjabi','sunni','Muhammad Bahawal Khan II',22),
 'LAD':('lad - ladakh.txt','tibetan','mahayana','Tsewang Namgyal II',None),
 'GAR':('gar - garwhal.txt','pahari','hindu','Lalit Shah',None),
 'MAK':('mak - makran.txt','baluchi','sunni',None,None),
 'KHR':('khr - kharan.txt','baluchi','sunni',None,None),
 'LBL':('lbl - las bela.txt','baluchi','sunni','Ghulam Shah',None)}
TARGETS={
 'BHW':('STATE_PUNJAB','022D2B D597DC 30122F CF602F 706940 2DBD82 19E5C0 EFC3B4 CA516D B4E322'),
 'LAD':('STATE_KASHMIR','CDB7DB F28F90 D25436 43B99F 9666D9 AA60FC 72F7C2 B637A4 56684E C49B8C 2B6E7C 2D5D46 EDCC3E 21F020 A09736 6AA44A 2DDFDB 18CED8'),
 'D2J':('STATE_KASHMIR','24EF26 FD692B 217021'),
 'D2K':('STATE_HILL_PUNJAB','251424 572FB9'),
 'D2C':('STATE_HILL_PUNJAB','8FF69F'),
 'D2M':('STATE_HILL_PUNJAB','3264B7'),
 'D2U':('STATE_HILL_PUNJAB','59BBCE F202E0'),
 'D2B':('STATE_HILL_PUNJAB','E31B4E D52082 E0C455 E60F80'),
 'D2S':('STATE_HILL_PUNJAB','45AF2E 607020'),
 'GAR':('STATE_HILL_PUNJAB','0003C6 F4C868'),
 'PTA':('STATE_HILL_PUNJAB','DB91D3 66C9D9 A0F0A0 0C25D9'),
 'MAK':('STATE_BALUCHISTAN','C6E602 951063 968562 675BCE 2FF46D E87BBF 7FE584 2E7961 978421 45F2DD F9577D 3C9B5F 56CF62 97C017 D6DD8A 556C63 BB836E'),
 'KHR':('STATE_BALUCHISTAN','4B2EAD D4EC50 954C12 0279A0'),
 'LBL':('STATE_BALUCHISTAN','113E0B C070E0 B0F79E 8ED831 407060 4E09C5'),
 'KAL':('STATE_BALUCHISTAN','1EF53E 1161D9 62BEAA 7D60E7 4F800F')}
TAGS=list(EXISTING)+list(NEW)
POPS=['common/history/pops/09_central_asia.txt','common/history/pops/10_india.txt']
BUILD=['common/history/buildings/09_central_asia.txt','common/history/buildings/10_india.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']
MIL='common/history/military_formations/04_military_formations_middle_east.txt'
def dump(n,v):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def put(files,rel,s):files[rel]=encoded(ROOT/rel,s) if (ROOT/rel).exists() else s.encode('utf8')
def stock_units(raw):
 c=C.Counter()
 for n in walk(parse(raw)):
  if n.key=='combat_unit':c[(scalar(n.one('state_region')),scalar(n.one('type')),scalar(n.one('service_type','regular')))]+=int(n.one('count','1'))
 return c
def distribute(raw,sid,schedules,ledger):
 """Preserve cohort fields and integer totals. Weights are technical, never census."""
 n=state_nodes(raw)[sid];src=n.children('region_state:DUR')[0];ps=src.children('create_pop');by=C.defaultdict(list)
 for i,p in enumerate(ps):
  weights=schedules[i];total=int(p.one('size'));keys=list(weights);allocated=0
  for j,t in enumerate(keys):
   num=total-allocated if j==len(keys)-1 else total*weights[t]//sum(weights.values());allocated+=num
   if not num:continue
   z=p.children('size')[0];s=raw[p.start:p.end];s=s[:z.start-p.start]+'size = '+str(num)+s[z.end-p.start:];by[t].append(s)
   ledger.append(dict(state=sid,source_cohort=i,to=t,size=num,policy='Conserved stock allocation, not a historical census or pixel-derived population'))
 patches=[];insert=[]
 for t,ss in by.items():
  nodes=n.children('region_state:'+t)
  if t!='DUR' and nodes:
   q=nodes[0];patches.append((q.end-1,q.end-1,'\n'+'\n'.join(ss)+'\n'))
  else:insert.append('region_state:'+t+' = {\n'+'\n'.join(ss)+'\n}')
 patches.append((src.start,src.end,'\n'.join(insert)))
 return edit(raw,patches)
def tech_audit(filename):
 from validate_starting_technology_1776 import collect_snapshot,audit_country
 s=collect_snapshot();rows=[audit_country(t,s,dict(historical_evidence='DP-02 SOURCES.md and REPORT.md; individually bounded agricultural/craft and military profiles, no industrial tier.')) for t in TAGS+['DUR','PAN','KAL','PTA']];dump(filename,rows);return rows
def prepare():
 assert not (OUT/'APPLIED.json').exists()
 files={};before=runtime();ow=normalized_owners();transfers=[];ledger=[]
 definitions={n.key for p in effective('common/country_definitions') for n in parse(text(p))}
 assert not set(NEW)&definitions,'TAG collision'
 for t,(sid,rs) in TARGETS.items():
  for r in rs.split():
   r='x'+r;assert ow[r]=={(sid,'DUR')},(r,ow.get(r));transfers.append(dict(rgb=r,state=sid,before='DUR',after=t))
 raw=text(ROOT/ST);patch=[]
 for sid in SCOPE:
  n=state_nodes(raw)[sid];by=C.defaultdict(set);old={}
  for q in n.children('create_state'):
   t=scalar(q.one('country'))[2:];by[t]|=set(provs(q,'owned_provinces'));old[t]=q
  for z in transfers:
   if z['state']==sid:by[z['before']].remove(z['rgb']);by[z['after']].add(z['rgb'])
  for t,q in old.items():
   if not by[t]:patch.append((q.start,q.end,''))
   elif by[t]!=set(provs(q,'owned_provinces')):
    p=q.children('owned_provinces')[0];patch.append((p.start,p.end,'owned_provinces = '+rgb_block(by[t])))
  addition=''.join('\n create_state = { country = c:'+t+' owned_provinces = '+rgb_block(rs)+' }\n' for t,rs in by.items() if t not in old)
  patch.append((n.end-1,n.end-1,addition))
 put(files,ST,edit(raw,patch))
 # Entire country cores restored; finer allocations documented as conservation only.
 for rel in POPS:
  raw=text(ROOT/rel)
  if rel==POPS[0]:
   schedules=[{'MAK':80,'LBL':15,'DUR':5}]*3+[{'KHR':75,'DUR':25}]*3
   new=distribute(raw,'STATE_BALUCHISTAN',schedules,ledger)
  else:
   new=distribute(raw,'STATE_PUNJAB',[{'BHW':1}]*6,ledger)
   hills={'GAR':25,'D2K':20,'D2C':10,'D2M':15,'D2U':10,'D2S':10,'D2B':10}
   new=distribute(new,'STATE_HILL_PUNJAB',[{'PTA':1}]*5+[hills]*6,ledger)
   schedules=[{'DUR':88,'D2J':12},{'D2J':1},{'DUR':1},{'DUR':80,'D2J':20},{'DUR':1},{'D2J':1}]+[{'DUR':1}]*4+[{'LAD':1}]*3
   new=distribute(new,'STATE_KASHMIR',schedules,ledger)
  assert popstock(raw)==popstock(new);put(files,rel,new)
 # Reassign jurisdiction-owned civil facilities without changing any levels or recipes.
 for rel in BUILD:
  raw=text(ROOT/rel);patch=[]
  for sid in ['STATE_PUNJAB','STATE_HILL_PUNJAB']:
   s=state_nodes(raw).get(sid)
   if not s:continue
   for q in s.children('region_state:DUR'):
    if sid=='STATE_PUNJAB':patch.append((q.start,q.end,renamed(raw[q.start:q.end],'DUR','BHW')))
    else:
     rows=[]
     for b in q.children('create_building'):
      levels=[z for z in walk(b.children()) if z.key=='levels'];assert len(levels)==1 and int(levels[0].value)==2
      for t in ['D2K','D2M']:
       z=levels[0];body=raw[b.start:b.end];body=body[:z.start-b.start]+'levels = 1'+body[z.end-b.start:]
       rows.append('region_state:'+t+' = { '+renamed(body,'DUR',t)+' }')
     patch.append((q.start,q.end,'\n'.join(rows)))
  new=edit(raw,patch);assert buildingstock(raw)==buildingstock(new)
  if new!=raw:put(files,rel,new)
 # GAR is an independent hill kingdom, not a Maratha vassal.
 rel='common/history/diplomacy/00_subject_relationships.txt';raw=text(ROOT/rel);patch=[]
 for c in walk(parse(raw)):
  if c.key=='c:MARATH':
   for q in c.children('create_diplomatic_pact'):
    if scalar(q.one('country'))=='c:GAR':patch.append((q.start,q.end,'# DP-02: Garhwal is not a Maratha dependency.'))
 assert len(patch)==1;put(files,rel,edit(raw,patch))
 # Nominal Afghan allegiance and Kalat ties: no invented 30% fiscal extraction.
 subject=text(ROOT/'common/subject_types/1776_dp01.txt').replace('aor1776_kalat_suzerainty','aor1776_dp02_allegiance')
 action=text(ROOT/'common/diplomatic_actions/1776_dp01.txt').replace('aor1776_kalat_suzerainty','aor1776_dp02_allegiance')
 put(files,'common/subject_types/1776_dp02.txt',subject);put(files,'common/diplomatic_actions/1776_dp02.txt',action)
 put(files,'common/history/diplomacy/1776_dp02.txt','DIPLOMACY = { c:DUR ?= { create_diplomatic_pact = { country = c:BHW type = aor1776_dp02_allegiance } } c:KAL ?= { create_diplomatic_pact = { country = c:LBL type = aor1776_dp02_allegiance } } }\n')
 # Keep disputed Makran/Kharan collection arrangements open instead of asserting a date in 1776.
 # Explicit profiles, bounded to each restored polity; handicrafts are not industry.
 for t in TAGS:
  if t in NEW:
   _,_,cap,cu,relg,ruler,age,color=NEW[t];name='1776_dp02_'+t.lower()+'.txt'
  else:name,cu,relg,ruler,age=EXISTING[t]
  tech=['improved_husbandry','international_relations','traditional_food_processing']
  if t not in ['LAD','KHR']:tech+=['organized_textile_production']
  if t in ['BHW','GAR','D2K','D2M','D2J','LAD']:tech+=['organized_military_establishments']
  if t in ['GAR','MAK','D2B']:tech+=['organized_workshops']
  laws=[v for v in LAWS if v!='people_of_the_book']+['aor1776_dp02_customs','aor1776_dp02_customary_bondage',('aor1776_dp02_toleration' if t=='D2J' else 'state_religion')]
  put(files,'common/history/countries/'+name,'COUNTRIES = { c:'+t+' ?= {\n'+''.join(' add_technology_researched = '+v+'\n' for v in tech)+''.join(' activate_law = law_type:law_'+v+'\n' for v in laws)+' set_state_religion = rel:'+relg+'\n ig:ig_landowners ?= { add_ruling_interest_group = yes }\n} }\n')
  # Suppress inherited 1836 ruler templates; unnamed chiefs use generated names, never fabricated history.
  chname=name
  if t in ['KHR','LBL']:
   matches=[p.name for p in effective('common/history/characters') if p.name.lower().startswith(t.lower()+' ')];chname=matches[0] if matches else name
  char='create_character = { ruler = yes culture = cu:'+cu+' religion = rel:'+relg+' interest_group = ig_landowners ideology = ideology_traditionalist'
  if ruler:char+=' historical = yes first_name = aor1776_dp02_ruler_'+t.lower()+' last_name = aor1776_dp02_empty'
  if age is not None:char+=' age = '+str(age)
  put(files,'common/history/characters/'+chname,'CHARACTERS = { c:'+t+' ?= { '+char+' } } }\n')
 defs=''
 for t,(_,_,cap,cu,relg,ruler,age,color) in NEW.items():defs+=t+' = { color = { '+' '.join(map(str,color))+' } country_type = unrecognized tier = principality cultures = { '+cu+' } religion = '+relg+' capital = '+cap+' }\n'
 put(files,'common/country_definitions/1776_dp02.txt',defs)
 # Symbolic shared hill banner, explicitly not claimed as each dynasty's historic standard.
 put(files,'common/flag_definitions/1776_dp02.txt',''.join(t+' = { flag_definition = { coa = GAR priority = 100 allow_overlord_canton = no } }\n' for t in NEW))
 laws=text(ROOT/'common/laws/1776_dp01.txt').replace('aor1776_dp01','aor1776_dp02')
 laws=laws.replace('c:KAL ?= this c:PTA ?= this',' '.join('c:'+t+' ?= this' for t in TAGS))
 # The toleration variant is deliberately restricted to Jammu.
 laws=laws.replace('c:PTA ?= this','c:D2J ?= this')
 put(files,'common/laws/1776_dp02.txt',laws)
 # Conserved existing conscript counts: no new standing army or manpower.
 raw=text(ROOT/MIL);patch=[];newunit=[]
 for c in walk(parse(raw)):
  if c.key!='c:DUR':continue
  for f in c.children('create_military_formation'):
   for u in f.children('combat_unit'):
    sid=scalar(u.one('state_region'));count=int(u.one('count','1'))
    if scalar(u.one('service_type','regular'))!='conscript':continue
    allocation={'s:STATE_PUNJAB':{'BHW':1},'s:STATE_HILL_PUNJAB':{'D2K':1,'D2M':1},'s:STATE_KASHMIR':{'LAD':2,'D2J':1,'DUR':7},'s:STATE_BALUCHISTAN':{'MAK':1,'LBL':1}}.get(sid)
    if not allocation:continue
    assert sum(allocation.values())==count
    patch.append((u.start,u.end,''))
    for t,num in allocation.items():
     s=raw[u.start:u.end];z=u.children('count')[0];s=s[:z.start-u.start]+'count = '+str(num)+s[z.end-u.start:]
     if t=='DUR':patch.append((f.end-1,f.end-1,'\n'+s+'\n'))
     else:newunit.append((t,s))
 put(files,MIL,edit(raw,patch))
 put(files,'common/history/military_formations/1776_dp02.txt','MILITARY_FORMATIONS = {\n'+''.join('c:'+t+' ?= { create_military_formation = { type = army hq_region = sr:'+('region_greater_persia' if t in ['MAK','LBL'] else 'region_north_india')+' name = aor1776_dp02_levy '+s+' } }\n' for t,s in newunit)+'}\n')
 # Keep locators untouched; record inherited misplacements instead of relocating fictional cities.
 for lang in ['french','english']:
  fr=lang=='french';vals={}
  for t,(fn,en,*_) in NEW.items():vals[t]=fn if fr else en;vals[t+'_ADJ']=fn if fr else en
  for t in TAGS:
   ruler=NEW[t][5] if t in NEW else EXISTING[t][3]
   if ruler:vals['aor1776_dp02_ruler_'+t.lower()]=ruler
  vals.update({'aor1776_dp02_empty':'','aor1776_dp02_levy':'Levée locale' if fr else 'Local levy','aor1776_dp02_allegiance':'Allégeance traditionnelle' if fr else 'Traditional allegiance','aor1776_dp02_allegiance_desc':'Le prince conserve son gouvernement et ses forces sous une suzeraineté sans versement régulier.' if fr else 'The prince retains his government and forces under suzerainty without regular payments.','subject_type_aor1776_dp02_allegiance':'Principauté autonome' if fr else 'Autonomous principality','subject_type_aor1776_dp02_allegiance_desc':'La principauté garde ses institutions et ses initiatives diplomatiques.' if fr else 'The principality retains its institutions and diplomatic initiatives.'})
  vals['aor1776_dp02_allegiance_pact_desc']=vals['aor1776_dp02_allegiance_desc']
  vals.update({k:v for k,v in re.findall(r'^\s*(law_aor1776_dp01[^:]+):0\s+"(.*)"',text(ROOT/'localization'/lang/'replace'/('1776_dp01_l_'+lang+'.yml')),re.M)})
  vals={k.replace('aor1776_dp01','aor1776_dp02'):v for k,v in vals.items()}
  files['localization/'+lang+'/replace/1776_dp02_l_'+lang+'.yml']=b'\xef\xbb\xbf'+('l_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in vals.items())).encode('utf8')
 manifest=[]
 for rel,data in files.items():
  p=ROOT/rel;old=p.read_bytes() if p.exists() else None
  if old==data:continue
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  q=OUT/'staged'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  if old is not None:q=OUT/'preimages'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
  manifest.append(dict(file=rel,before_sha256=sha(p) if p.exists() else None,after_sha256=sha(OUT/'staged'/rel)))
 dump('POP_LEDGER.json',ledger);dump('PLAN.json',dict(transfers=transfers,policy='Coarse jurisdiction cores at existing cell resolution; see mapping limitations in REPORT.md.'))
 dump('PREPARED.json',dict(files=manifest,world_before=before,ownership_before={r:sorted(v) for r,v in ow.items()}))
 print(json.dumps(dict(files=len(manifest),transfers=len(transfers))))
def apply():
 assert not (OUT/'APPLIED.json').exists();m=load('PREPARED.json');tech_audit('TECH_BEFORE.json')
 for z in m['files']:
  p=ROOT/z['file'];assert (sha(p) if p.exists() else None)==z['before_sha256'],('Concurrent change',z['file']);assert sha(OUT/'staged'/z['file'])==z['after_sha256']
 for z in m['files']:
  p=ROOT/z['file'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((OUT/'staged'/z['file']).read_bytes())
 dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files=m['files'],runtime_validated=False))
 print('DP-02 applied; independent audit required.')
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
