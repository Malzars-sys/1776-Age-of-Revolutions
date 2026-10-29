"""CENTRAL-ASIA-01: bounded native-province political approximation, 1776.

Preflight is non-functional; apply is single-use with immediate preimages.
The separate Durrani/Punjab work and all its country portions are reserved.
"""
import argparse,json,shutil,re
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_centralasia01 as c
import world1776_sahel0205 as m
import validate_starting_technology_1776 as tech
ROOT,LOT,ST=c.ROOT,c.LOT,c.ST
b=c.n.b;raw=b.a.raw;dump=c.dump;load=c.load
PREFIX='1776_world_centralasia01'
ARMY='common/history/military_formations/00_military_formations_europe.txt'
DIP='common/history/diplomacy/00_subject_relationships.txt'
CRAFT=['improved_husbandry','improved_agricultural_implements','international_relations','organized_textile_production','traditional_food_processing','organized_workshops']
PROFILES={
 'TSH':dict(fr='Tachkent',en='Tashkent',adj_fr='tachkentois',adj_en='Tashkent',kind='unrecognized',capital='STATE_FERGANA',culture=['uzbek'],religion='sunni',color=[177,132,78],tech=CRAFT,
  basis='Pospelov1800 introduction: four separately governed dahas before Yunus1784; aggregate urban polity, not an already unified khanate. Irrigated oasis, weaving, workshops and caravan diplomacy; early capabilities only.'),
 'URT':dict(fr='Oura-Tépa',en='Ura-Tepa',adj_fr='oura-tépien',adj_en='Ura-Tepa',kind='unrecognized',capital='STATE_FERGANA',culture=['uzbek','tajik'],religion='sunni',color=[137,111,168],tech=CRAFT,
  basis='Beisembiev/Levi, initial18c stage and Bregel: autonomous Yuz domains around Ura-Tepa/Khujand, intermittently contested. Native western Fergana envelope; irrigated cultivation and urban crafts, no19c army or banking grant.'),
 'QTG':dict(fr='Karategin',en='Karategin',adj_fr='karategin',adj_en='Karategin',kind='unrecognized',capital='STATE_TAJIKISTAN',culture=['tajik'],religion='sunni',color=[170,149,76],tech=CRAFT,
  basis='Bregel: mountain principality before Kokand1830s expansion; Garm/Rasht valley native approximation. Small-stock cultivation, textiles, local crafts and external negotiation, no industrial knowledge inferred.'),
 'DVA':dict(fr='Darvaz',en='Darvaz',adj_fr='darvazi',adj_en='Darvaz',kind='unrecognized',capital='STATE_TAJIKISTAN',culture=['tajik'],religion='sunni',color=[166,100,101],tech=['improved_husbandry','improved_agricultural_implements','international_relations','traditional_food_processing','organized_workshops'],
  basis='Grevemeyer, Darvaz: autonomous indigenous dynasty since mid17c, narrow cultivated valleys and kinship patronage. Northern nucleus only; southern Panj bank reserved to Durrani interface. Household craft and small-stock capability, no urban-textile grant.'),
 'KLB':dict(fr='Koulab',en='Kulob',adj_fr='koulabi',adj_en='Kulobi',kind='unrecognized',capital='STATE_TAJIKISTAN',culture=['tajik'],religion='sunni',color=[185,133,97],tech=['improved_husbandry','improved_agricultural_implements','international_relations','traditional_food_processing','organized_workshops'],
  basis='Bregel lists Kolab among mountain principalities independent of the later Kokand/Bukharan annexations. Two native cells east of inherited Bukharan Hissar portion, west of Darvaz; northern nucleus only, no southern-bank transfer. Lowland cultivation, craft and local external negotiation.'),
 'SHG':dict(fr='Choughnan et Rouchan',en='Shughnan and Rushan',adj_fr='choughnani',adj_en='Shughnani',kind='unrecognized',capital='STATE_TAJIKISTAN',culture=['tajik'],religion='shiite',color=[118,158,153],tech=['improved_husbandry','improved_agricultural_implements','international_relations','traditional_food_processing','organized_workshops'],
  basis='Grevemeyer, Darvaz: eastern semiautonomous Shughnan/Rushan, generally tied to Badakhshan. Two courts aggregated in northern native cells; precise1776 allegiance not proved, no invented DUR pact. Native Tajik/Shiite catalogue proxies for Pamiri/Ismaili populations; no POP assimilation.'),
 'KYR':dict(fr='Clans kirghiz',en='Kyrgyz Clans',adj_fr='kirghiz',adj_en='Kyrgyz',kind='decentralized',capital='STATE_KIRGHIZIA',culture=['kirgiz'],religion='sunni',color=[168,177,126],tech=['improved_husbandry','improved_agricultural_implements','traditional_food_processing','organized_textile_production','organized_workshops'],
  basis='Saparaliyev2011 pp142,144,148,155 cites18c independent Kyrgyz authorities and Osh-Alay/highland communities. Decentralized aggregate, not modern Kyrgyzstan or a unified kingdom; pastoral cultivation and household crafts, no blanket diplomacy/military tier.')}
# The main Darvaz valley falls across the explicitly reserved Durrani state.
# Do not instantiate a misleading isolated Darvaz tag from a Rushan locator.
del PROFILES['DVA']
CAPITALS={'OZH':'STATE_AKMOLINSK','UZH':'STATE_SYRDARYA'}
PALETTE={'KZH':[220,179,89],'OZH':[138,179,204],'UZH':[113,180,154],'KOK':[176,110,126],'BUK':[188,164,204],'KHI':[210,158,130],'TRM':[197,191,159],'RUS':[154,174,117],'DUR':[172,150,163],'CHI':[213,191,124],'XIN':[213,191,124]}
PALETTE.update({t:r['color'] for t,r in PROFILES.items()})

def make_plan():
 cells=load('GEOMETRY_CELLS.json');by={r['index']:r for r in cells};result=[];used=set()
 def pick(source,target,ids,basis):
  rr=[by[i] for i in ids];assert not set(ids)&used;used.update(ids)
  assert all(r['owners']==[[r['state'],source]] for r in rr),(source,target)
  for sid in dict.fromkeys(r['state'] for r in rr):result.append(dict(state=sid,source=source,target=target,RGBs=[r['RGB'] for r in rr if r['state']==sid],historical_basis=basis,precision='NATIVE_CELL_POLITICAL_APPROXIMATION_NOT_CADASTRAL'))
 pick('KZH','RUS',[r['index'] for r in cells if r['state']=='STATE_SAMARA'],'Samara and Orenburg Russian administrative/fortified line before1776; native regional extent is coarse, not uniform control beyond the line.')
 pick('KZH','RUS',[r['index'] for r in cells if r['RGB'] in ['x0A5203','xEFFD2B']],'Yaik/Uralsk and actual drawn Guryev Russian fortified nodes. The native mine pointer xD1364F is45 pixels east of sampled locator xEFFD2B; do not transfer that erroneous eastern cell. No arbitrary corridor or broad steppe annexation.')
 pick('OZH','RUS',[448,463,465],'Koryakovsky/Pavlodar1720, Semipalatinsk1718 and Ust-Kamenogorsk1720 Russian fort nodes along Irtysh. State identifier SEMIRECHE misleading: these are actual northeastern locators, not the Senior Zhuz south of Balkhash. No broad Russian steppe annexation.')
 pick('KOK','OZH',[1006,996,1120,975,1125,955,1063,945,1053,1142,993,998,1041,960,1112],'Turkistan-facing western Syr Darya steppe outside pre19c Kokand; approximate Kazakh internal jurisdiction.')
 pick('KOK','UZH',[977,979,987,1020,1024,1044,1070,1086,1089,1109,1111,1143],'Shymkent/Tashkent-facing Senior Zhuz steppe, not Kokand19c extension; boundary among Kazakh jurisdictions approximate.')
 pick('KOK','TSH',[876,942],'Tashkent city and adjoining oasis cell: native city locator and empirical physical-position check disagree by several pixels; two-cell political envelope, four autonomous dahas represented together, no Yunus1784 unification.')
 pick('KOK','UZH',[877,884,886],'Chirchiq/Angren approaches outside the inner Fergana basin, native political approximation at Tashkent/Senior Zhuz interface.')
 pick('KOK','URT',[878,887,888,889,108,126],'Ura-Tepa/Khujand western valley Yuz domain, contested and not a later Kokand provincial annexation.')
 pick('KOK','QTG',[113,114,118,131,127,137],'Garm/Rasht/Karategin northern mountain-valley principality; exact pass boundaries not cadastral.')
 pick('KOK','KLB',[110,122],'Kulob northern valley nucleus west of Darvaz, east of Bukharan Hissar portion; no change to Durrani southern-bank interface.')
 pick('BUK','KLB',[138],'Kulob core indicated by physical-position sanity check, east of Hissar; independent local authority rather than nominal Bukharan provincial administration. Native envelope approximate.')
 pick('KOK','SHG',[112,128,134,116,140],'Northern Shughnan/Rushan Pamir-valley aggregate; cell140 spans Rushan/Vanj interface with historical Darvaz, boundary unresolved, no fabricated diplomatic dependence on the concurrent Durrani reconstruction.')
 pick('KOK','KYR',[r['index'] for r in cells if r['state']=='STATE_KIRGHIZIA' and r['owners']==[[r['state'],'KOK']] and r['RGB']!='xE5AD64'],'Independent Kyrgyz mountain communities; Osh valley native city cell retained as Fergana/Kokand approximation, exact urban boundary open.')
 pick('KOK','KYR',[107,111,115,121,125,133,135,136,139,141],'Eastern highland pastoral communities, not Kokand1830s imperial maximum; native envelope and internal clan geography approximate.')
 return result

def save(path,text,bom=False):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((b'\xef\xbb\xbf' if bom else b'')+text.encode('utf8'))

def geometry(owners,name='PROPOSED',indices=False):
 box=(5100,570,6000,1240);x0,y0,x1,y1=box
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)[y0:y1,x0:x1];pack=a[:,:,0]*65536+a[:,:,1]*256+a[:,:,2]
 tags=sorted({v[0][1] for v in owners.values()});ids={t:i+1 for i,t in enumerate(tags)};inverse={v:k for k,v in ids.items()}
 lut=np.zeros(1<<24,dtype=np.int32)
 for color,parts in owners.items():lut[int(color[1:],16)]=ids[parts[0][1]]
 code=lut[pack];adj=defaultdict(set)
 for aa,bb in [(code[1:],code[:-1]),(code[:,1:],code[:,:-1])]:
  for z,w in np.unique(np.stack([aa.ravel(),bb.ravel()],axis=1),axis=0):
   if z and w and z!=w:adj[inverse[z]].add(inverse[w]);adj[inverse[w]].add(inverse[z])
 province_adj=defaultdict(set)
 for aa,bb in [(pack[1:],pack[:-1]),(pack[:,1:],pack[:,:-1])]:
  for z,w in np.unique(np.stack([aa.ravel(),bb.ravel()],axis=1),axis=0):
   if z!=w:province_adj[int(z)].add(int(w));province_adj[int(w)].add(int(z))
 result=[];values,counts=np.unique(pack,return_counts=True);pixels=dict(zip(map(int,values),map(int,counts)))
 for tag in list(PROFILES)+['KOK','KZH','OZH','UZH']:
  remaining={int(z) for z in values if lut[z]==ids.get(tag,-1)};sizes=[]
  while remaining:
   start=remaining.pop();queue=[start];size=0
   while queue:
    z=queue.pop();size+=pixels[z];neighbors=province_adj[z]&remaining;remaining-=neighbors;queue.extend(neighbors)
   sizes.append(size)
  result.append(dict(TAG=tag,components=sorted(map(int,sizes),reverse=True),neighbors=sorted(adj[tag])))
 colors=np.zeros((len(tags)+1,3),dtype=np.uint8)+205;colors[0]=(224,234,240)
 for tag,i in ids.items():colors[i]=PALETTE.get(tag,[208,206,195])
 rgb=colors[code];edge=np.zeros(code.shape,bool);edge[1:]|=code[1:]!=code[:-1];edge[:,1:]|=code[:,1:]!=code[:,:-1];rgb[edge]=(65,68,63)
 scale=2;im=Image.fromarray(rgb).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
 for tag in list(PALETTE):
  yy,xx=np.where(code==ids.get(tag,-1))
  if len(xx)<10:continue
  j=np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2);d.text((int(xx[j])*scale,int(yy[j])*scale),tag,font=font,fill='white',stroke_width=2,stroke_fill='black')
 if indices:
  f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
  for r in load('GEOMETRY_CELLS.json'):
   x,y=r['centroid']
   if 5600<x<5920 and 1040<y<1240:d.text(((x-x0)*scale,(y-y0)*scale),str(r['index']),font=f,fill='black',stroke_width=1,stroke_fill='white')
 im.save(LOT/(name+'.png'));dump(name+'_GEOMETRY.json',result)
 return result

def definition_additions():
 cache=load('DEFINITION_INPUTS.json');defs=[]
 for tag,r in PROFILES.items():
  body='color = { '+' '.join(map(str,r['color']))+' } country_type = '+r['kind']+' tier = principality cultures = { '+' '.join(r['culture'])+' } religion = '+r['religion']+' capital = '+r['capital']
  defs.append(('REPLACE_OR_CREATE:' if tag=='KYR' else '')+tag+' = { '+body+' }')
 for tag,capital in CAPITALS.items():
  text=cache[tag];n=b.parse(text)[0];f=n.children('capital')[0];text=b.edits(text,[(f.start,f.end,'capital = '+capital)])
  defs.append('REPLACE_OR_CREATE:'+text)
 return '\n\n'.join(defs)+'\n'

def additional():
 out={'common/country_definitions/'+PREFIX+'.txt':definition_additions()}
 for tag,r in PROFILES.items():
  effect='effect_aor1776_centralasia01_'+('clans' if r['kind']=='decentralized' else 'court')
  extra=' effect_native_conscription_3 = yes\n' if r['kind']=='decentralized' else ' activate_law = law_type:law_slave_trade\n'
  if tag=='TSH':extra+=' activate_law = law_type:law_oligarchy\n'
  out['common/history/countries/'+tag.lower()+' - 1776 central asia.txt']='COUNTRIES = { c:'+tag+' ?= {\n'+''.join(' add_technology_researched = '+t+'\n' for t in r['tech'])+' '+effect+' = yes\n'+extra+'} }\n'
 base=raw(ROOT/'common/scripted_effects/1776_world_congo01.txt').replace('congo01','centralasia01').replace('effect_aor1776_centralasia01_politics','effect_aor1776_centralasia01_court').replace('effect_aor1776_centralasia01_decentralised','effect_aor1776_centralasia01_clans')
 out['common/scripted_effects/'+PREFIX+'.txt']=base
 law,path=b.a.catalog('common/laws')['law_mercantilism'];f=law.children('modifier')[0];allowed=' '.join('c:'+t+' ?= this' for t,r in PROFILES.items() if r['kind']!='decentralized')
 out['common/laws/'+PREFIX+'.txt']='law_aor1776_centralasia01_trade_customs = { group = lawgroup_trade_policy parent = law_mercantilism icon = "gfx/interface/icons/law_icons/mercantilism.dds" progressiveness = 0 unlocking_technologies = { international_relations } is_visible = { OR = { '+allowed+' } } can_enact = { OR = { '+allowed+' } } '+raw(path)[f.start:f.end]+' }\n'
 # Private relation with independent diplomacy; do not alter Kalat or shared types.
 out['common/subject_types/'+PREFIX+'.txt']=raw(ROOT/'common/subject_types/1776_dp01.txt').replace('kalat_suzerainty','kazakh_nominal_protection').replace('valid_overlord_country_types = { unrecognized }','valid_overlord_country_types = { recognized }')
 out['common/diplomatic_actions/'+PREFIX+'.txt']=raw(ROOT/'common/diplomatic_actions/1776_dp01.txt').replace('kalat_suzerainty','kazakh_nominal_protection')
 for lang in ['french','english']:
  strings={}
  for t,r in PROFILES.items():strings[t]=r['fr' if lang=='french' else 'en'];strings[t+'_ADJ']=r['adj_fr' if lang=='french' else 'adj_en']
  if lang=='french':strings.update(law_aor1776_centralasia01_trade_customs='Droits des caravanes',law_aor1776_centralasia01_trade_customs_desc='Les autorités prélèvent les droits des marchés et protègent les voies caravanières.',aor1776_kazakh_nominal_protection='Protection nominale',aor1776_kazakh_nominal_protection_desc='Le khan reconnaît la protection russe tout en conservant sa diplomatie et ses guerres. Aucun versement régulier ni service militaire automatique ne sont imposés.',subject_type_aor1776_kazakh_nominal_protection='Khanat sous protection nominale',subject_type_aor1776_kazakh_nominal_protection_desc='Le khanat conserve ses autorités et sa politique extérieure sous une protection reconnue mais indirecte.')
  else:strings.update(law_aor1776_centralasia01_trade_customs='Caravan Dues',law_aor1776_centralasia01_trade_customs_desc='Local authorities collect market dues and protect caravan routes.',aor1776_kazakh_nominal_protection='Nominal Protection',aor1776_kazakh_nominal_protection_desc='The khan acknowledges Russian protection while retaining independent diplomacy and wars. Neither regular payments nor automatic military service are imposed.',subject_type_aor1776_kazakh_nominal_protection='Nominally Protected Khanate',subject_type_aor1776_kazakh_nominal_protection_desc='The khanate retains its authorities and foreign policy under acknowledged but indirect protection.')
  key='aor1776_kazakh_nominal_protection'
  strings.update({key+'_pact_desc':'$'+key+'_desc$',key+'_action_name':'$'+key+'$', 'subject_type_'+key+'_no_icon':'$subject_type_'+key+'$',key+'_action_break_name':'Renoncer à la protection' if lang=='french' else 'Renounce Protection',key+'_action_ask_to_break_name':'Rompre l’allégeance' if lang=='french' else 'End Allegiance',key+'_action_notification_break_name':'Protection rompue' if lang=='french' else 'Protection Ended',key+'_action_notification_break_desc':'Le lien de protection nominale a pris fin. Le khanat ne reconnaît plus cette allégeance.' if lang=='french' else 'The nominal protection arrangement has ended. The khanate no longer acknowledges this allegiance.'})
  out[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
 return out

def scopes(plan):
 regions={'s:'+r['state'] for r in plan};sources=defaultdict(set)
 for r in plan:sources['s:'+r['state']].add(r['source'])
 out={ST:regions,ARMY:{'c:KZH','c:KOK'},DIP:{'c:RUS','c:OZH','c:UZH'}}
 for folder in ['common/history/pops','common/history/buildings']:
  for path in b.tech.effective(folder):
   selected={n.key for n in b.walk(b.parse(raw(path))) if n.key in regions and any(n.children('region_state:'+t) for t in sources[n.key])}
   if selected:assert path.is_relative_to(ROOT);out[path.relative_to(ROOT).as_posix()]=selected
 return out

def portions(text,allocation,buildings):
 # Cohort allocation is technical (province counts), not a demographic claim.
 # Necessary urban services stay in a centralized valley; do not endow KYR
 # with imperial mills, trade centres and financial districts.
 ops=[]
 for sid in sorted({x[0] for x in allocation}):
  matches=[n for n in b.walk(b.parse(text)) if n.key=='s:'+sid]
  if not matches:continue
  state,=matches;removed=[];items=defaultdict(list)
  for part in state.children():
   source=part.key.removeprefix('region_state:')
   if (sid,source) not in allocation:continue
   weights=allocation[sid,source];targets=sorted(weights)
   for item in part.children('create_building' if buildings else 'create_pop'):
    fields=[n for n in b.walk([item]) if n.key==('levels' if buildings else 'size')];assert len(fields)==1
    f=fields[0];amount=int(f.value)
    if buildings and source=='KOK' and sid=='STATE_TAJIKISTAN':
     target='KYR' if item.one('building').strip('"')=='building_livestock_ranch' else 'QTG'
     assigned={target:amount}
    elif buildings and source=='KOK' and sid in ['STATE_KIRGHIZIA','STATE_FERGANA']:
     target='KYR' if sid=='STATE_KIRGHIZIA' and item.one('building').strip('"')=='building_livestock_ranch' else 'KOK';assigned={target:amount}
    elif buildings:assigned={max(targets,key=lambda t:weights[t]):amount}
    else:assigned=dict(zip(targets,m.s.allocate(amount,[weights[t] for t in targets])))
    for target,value in assigned.items():
     if not value:continue
     frag=text[item.start:item.end];frag=b.edits(frag,[(f.start-item.start,f.end-item.start,f.key+' = '+str(value))])
     if buildings:
      frag=frag.replace('c:'+source,'c:'+target)
      if source=='KOK' and sid=='STATE_TAJIKISTAN' and item.one('building').strip('"')=='building_trade_center':
       frag=frag.replace('"pm_trade_center_trade_quantity_normal"','"pm_trade_center_trade_quantity_limited"')
     items[target].append(frag)
   removed.append(part)
  if not removed:continue
  frag=text[state.start:state.end];ed=[(p.start-state.start,p.end-state.start,'') for p in removed]
  for tag,ii in items.items():
   exists=[p for p in state.children('region_state:'+tag) if p not in removed]
   if exists:
    p,=exists;ed.append((p.end-state.start-1,p.end-state.start-1,'\n'+'\n'.join(ii)+'\n'))
   else:ed.append((state.end-state.start-1,state.end-state.start-1,'\nregion_state:'+tag+' = {\n'+'\n'.join(ii)+'\n}\n'))
  ops.append((state.start,state.end,b.edits(frag,ed)))
 return b.edits(text,ops)

def transform(old,plan):
 allocation=m.allocations(old[ST],plan);out={ST:m.transform({ST:old[ST]},plan)[ST]}
 for rel,text in old.items():
  if rel==ST:continue
  if '/history/pops/' in rel or '/history/buildings/' in rel:out[rel]=portions(text,allocation,'/history/buildings/' in rel)
  elif rel==ARMY:
   ops=[]
   for tag,source,target in [('KZH','STATE_SAMARA','STATE_AKTOBE'),('KOK','STATE_TAJIKISTAN','STATE_FERGANA')]:
    node=b.one(text,'c:'+tag);fields=[n for n in b.walk([node]) if n.key=='state_region' and n.value=='s:'+source];assert len(fields)==1
    for f in fields:ops.append((f.start,f.end,'state_region = s:'+target))
   out[rel]=b.edits(text,ops)
  elif rel==DIP:
   node=b.one(text,'c:RUS');ops=[]
   for p in node.children('create_diplomatic_pact'):
    if p.one('country')=='c:KZH':
     f=p.children('type')[0];ops.append((f.start,f.end,'type = aor1776_kazakh_nominal_protection'))
   for p in node.children('if'):
    if any(q.one('country') in ['c:OZH','c:UZH'] for q in p.children('create_diplomatic_pact')):ops.append((p.start,p.end,''))
   assert len(ops)==3
   for tag in ['OZH','UZH']:
    node=b.one(text,'c:'+tag);fields=node.children('add_liberty_desire');assert len(fields)==1
    for f in fields:ops.append((f.start,f.end,''))
   out[rel]=b.edits(text,ops)
  else:raise AssertionError(rel)
 return out

def preflight():
 plan=make_plan();dump('PLAN.json',plan);dump('COUNTRY_PROFILES.json',PROFILES)
 if not (LOT/'DEFINITION_INPUTS.json').exists():
  cat=b.a.catalog('common/country_definitions');dump('DEFINITION_INPUTS.json',{t:raw(cat[t][1])[cat[t][0].start:cat[t][0].end] for t in CAPITALS})
 old={r:raw(ROOT/r) for r in scopes(plan)};proposed=transform(old,plan);new=additional()
 for rel,text in dict(proposed,**new).items():save(LOT/'staged'/rel,text,rel.endswith('.yml'))
 before=c.n.owner_map(old[ST]);after=c.n.owner_map(proposed[ST]);geometry(before,'BEFORE_MAP');rows=geometry(after,'PROPOSED',True)
 dump('SCOPES.json',{r:sorted(v) for r,v in scopes(plan).items()})
 if not (LOT/'STARTING_TECH_BEFORE.json').exists():
  snap=tech.collect_snapshot();dump('STARTING_TECH_BEFORE.json',[tech.audit_country(t,snap) for t in c.TAGS+['RUS','DUR','CHI']])
 print('Plan',sum(len(r['RGBs']) for r in plan),'RGB;',len(new),'private files; geometry:',rows)

def apply():
 assert not (LOT/'FILES_MODIFIED.json').exists(),'Already applied; do not replay.'
 plan=make_plan();scope=scopes(plan);new=additional();cat=b.a.catalog('common/country_definitions')
 for tag in PROFILES:
  if tag!='KYR':assert tag not in cat,tag
 assert all(not (ROOT/r).exists() for r in new),'New-file collision'
 old={r:raw(ROOT/r) for r in scope};sha={r:b.a.sha(ROOT/r) for r in scope};out=transform(old,plan);owners=c.n.owner_map(old[ST])
 for r in plan:
  for color in r['RGBs']:assert owners[color]==[[r['state'],r['source']]],color
 before=dict(captured_utc=datetime.now(timezone.utc).isoformat(),inventory=c.n.b4.inventory(),protected=c.n.hashes(),scope={r:sorted(v) for r,v in scope.items()})
 dump('APPLY_BEFORE.json',before)
 for rel in scope:
  dest=LOT/'apply_inputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
 assert all(b.a.sha(ROOT/r)==sha[r] for r in scope),'Concurrent change: reread.'
 for rel,text in out.items():
  assert b.a.sha(ROOT/rel)==sha[rel],rel;save(ROOT/rel,text,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
 for rel,text in new.items():assert not (ROOT/rel).exists(),rel;save(ROOT/rel,text,rel.endswith('.yml'))
 dump('FILES_MODIFIED.json',[dict(file=r,before=sha.get(r),after=b.a.sha(ROOT/r)) for r in list(out)+list(new)])
 print('Installed',len(out),'current files and',len(new),'private files.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');p.add_argument('--apply',action='store_true');a=p.parse_args()
 if a.preflight:preflight()
 if a.apply:apply()
