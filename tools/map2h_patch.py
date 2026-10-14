"""Reviewed, reversible MAP2H integration from the immutable dirty-tree baseline.

Text is emitted as apply_patch, never written directly to gameplay files.
The optional bitmap operation is a bounded mechanical rewrite of existing RGB IDs,
not an image-generation operation. Every changed pixel has a reversible receipt.
"""
import collections as C,difflib,json,re,sys
from PIL import Image
import numpy as np
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2a_patch import state,edits,append
from map2e_patch import apportion,body_rewrite
from map2h_work import ROOT,GAME,OUT,BASE,TARGETS,sha,source_bitmap,packed,dump
WHOLE={('STATE_ARAKAN','KKI'):'ARK',('STATE_LAOS','SIA'):'VIE',('STATE_TASMANIA','WTI'):'PLW',('STATE_SOUTH_ISLAND','NTO'):'TTI',('STATE_NORTH_ISLAND','NTO'):'UNT'}
PARTIAL={
 ('STATE_ANNAM','DAI'):{'TSN':['xC46194','xEDBFB1','xFAB663','xEF3060']},
 ('STATE_MEKONG','DAI'):{'TSN':['x3C8C22'],'NGN':'REMAINDER'},
 ('STATE_CENTRAL_JAVA','DEI'):{'YOG':['x62742E'],'SRK':['x20DF70']},
 ('STATE_MALAYA','JOH'):{'DEI':['x8080B0']},
 ('STATE_WESTERN_NEW_GUINEA','TID'):{'PPU':['x817083']},
 ('STATE_WEST_MICRONESIA','PHI'):{'MCR':['x6E4206']},
 ('STATE_HAWAIIAN_ISLANDS','HAW'):{'HMA':['x6090C0'],'HWA':['xB5403E']},
}
DEFS={
 'ARK':('STATE_ARAKAN','unrecognized','kingdom','burmese','theravada',[206,146,78]),
 'VIE':('STATE_LAOS','unrecognized','kingdom','lao','theravada',[197,166,57]),
 'TSN':('STATE_MEKONG','unrecognized','principality','vietnamese','confucian',[167,64,77]),
 'NGN':('STATE_MEKONG','unrecognized','principality','vietnamese','confucian',[81,142,176]),
 'PLW':('STATE_TASMANIA','decentralized','principality','aborigine','animist',[149,101,79]),
 'TTI':('STATE_SOUTH_ISLAND','decentralized','principality','maori','animist',[125,182,174]),
 'HMA':('STATE_HAWAIIAN_ISLANDS','unrecognized','principality','hawaiian','animist',[200,122,70]),
 'HWA':('STATE_HAWAIIAN_ISLANDS','decentralized','principality','hawaiian','animist',[155,142,198]),
}
NAMES={
 'ARK':('Kingdom of Mrauk-U','Arakanese','Royaume de Mrauk-U','arakanais'),
 'VIE':('Kingdom of Vientiane','Vientiane','Royaume de Vientiane','de Vientiane'),
 'DAI':('Trinh Court','Trinh','Cour des Trịnh','des Trịnh'),
 'NGN':('Nguyen Lords','Nguyen','Seigneurs Nguyễn','des Nguyễn'),
 'TSN':('Tay Son Uprising','Tay Son','Insurrection Tây Sơn','Tây Sơn'),
 'PLW':('Palawa Communities','Palawa','Communautés palawa','palawa'),
 'TTI':('Te Tau Ihu Communities','Te Tau Ihu','Communautés de Te Tau Ihu','de Te Tau Ihu'),
 'UNT':('Northern Maori Communities','Maori','Communautés maories du Nord','maori'),
 'LAN':('Mandor Mining Communities','Mandor','Communautés minières de Mandor','de Mandor'),
 'HAW':('Hawaii Island','Hawaiian','Île d’Hawaï','hawaïen'),
 'HMA':('Maui Chiefdom','Maui','Chefferie de Maui','de Maui'),
 'HWA':('Leeward Island Chiefdoms','Leeward Hawaiian','Chefferies des îles sous le vent','des îles sous le vent'),
}
CASE={
 'ARK':('ARAKAN','Independent Mrauk-U before the Burmese conquest of 1784; whole native coastal Arakan subdivision, not a reconstruction of each frontier valley.'),
 'VIE':('VIENTIANE','Vientiane and middle Lao districts before Siamese conquest in 1778. Native RGB group is a broad kingdom abstraction.'),
 'TSN':('TAY_SON','Rebel base, Quang Ngai and Quy Nhon/Phu Yen by 1775. The large coastal x3C8C22 extends beyond individual contemporary districts; no royal proclamation of March 1776 or unification anticipated.'),
 'NGN':('NGUYEN','Nguyen authority in southern Dang Trong after loss of Phu Xuan to Trinh in 1774; no unified 1802 Vietnam.'),
 'PLW':('TASMANIA','Tasmanian Palawa communities replace mainland Anangu/Wati tag. Collective, not a unitary monarchy; inherited generic aborigine culture and 200 people conserved.'),
 'TTI':('TE_TAU_IHU','Indigenous communities of northern South Island before Ngati Toa invasions in the 1820s. Regional collective, not a claim that one iwi held all six provinces.'),
 'UNT':('NORTHERN_MAORI','Remove anticipated Ngati Toa control around Wellington; existing UNT becomes decentralized regional communities rather than the federation declared in 1835.'),
 'YOG':('JAVANESE_COURTS','One contiguous interior RGB west/northwest of Yogyakarta returned to the autonomous Mataram court; north-coast VOC ports retained. Approximate division, not a cadastral Giyanti map.'),
 'SRK':('JAVANESE_COURTS','One contiguous interior RGB east of Solo returned to Surakarta after Giyanti 1755; not direct VOC administration. Mangkunegaran remains grouped with the eastern court.'),
 'DEI':('MALACCA','Existing west-coast RGB approximates Dutch Malacca and a limited hinterland, held since 1641. Some neighbouring Malay settlements are necessarily included in this coarse province.'),
 'PPU':('PAPUAN_INTERIOR','Only the inland non-coastal RGB x817083 moves from Tidore to decentralized Papuan communities. Coastal tributary network abstraction retained, not European sovereignty over New Guinea.'),
 'MCR':('PALAU','Palau returns to local communities: Spanish colonial administration began in 1885. Generic Micronesian collective, not a unified trans-oceanic state.'),
 'HMA':('HAWAII','Maui/Lanai/Kahoolawe represented separately from Hawaii. Hana/Kauiki contested and partly held by Hawaii is not separable with these three retained RGB IDs.'),
 'HWA':('HAWAII','Oahu, Molokai, Kauai and Niihau grouped as decentralized distinct chiefdoms, not ruled by Maui or a fictional common king. Their separate aliinui remain an engine abstraction.'),
}
HUB_FIXES={'STATE_ANNAM':{'farm':'x307020'},'STATE_MEKONG':{'city':'xDF070D','farm':'x4923A3','wood':'x3C8C22'},'STATE_MINDANAO':{'port':'x16C9FB','wood':'xC3EC2D'},'STATE_WEST_MICRONESIA':{'port':'x414170'},'STATE_HAWAIIAN_ISLANDS':{'farm':'xB5403E','mine':'x492B26'}}

def prepare_evidence():
 """Capture small inherited source texts and exact Hawaii pixel substitutions once."""
 p=OUT/'SUPPLEMENTAL_BASELINE.json'
 if p.exists():return
 paths=['common/country_definitions/01_pacific_and_australasia.txt']+[f'common/history/characters/{n}.txt' for n in ['dai - dai nam','haw - hawaii','lan - lanfang']]+[f'gfx/map/map_object_data/generated_map_object_locators_{k}.txt' for k in ['wood','mine']]
 original={}
 for path in paths:
  src=ROOT/path if (ROOT/path).exists() else GAME/path
  original[path]={'text':src.read_text(encoding='utf-8-sig'),'source':str(src),'sha256':sha(src),'in_workspace':(ROOT/path).exists()}
 rgb=packed(source_bitmap());small=rgb[1580:1680,435:585];mask=np.isin(small,[0x492B26,0x6090C0,0xB5403E]);seen=set();components=[];pixels=[]
 from collections import deque
 for y,x in zip(*np.where(mask)):
  if (int(y),int(x)) in seen:continue
  q=deque([(int(y),int(x))]);seen.add((int(y),int(x)));coords=[]
  while q:
   a,b=q.popleft();coords.append((a+1580,b+435))
   for u,v in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
    if 0<=u<mask.shape[0] and 0<=v<mask.shape[1] and mask[u,v] and (u,v) not in seen:seen.add((u,v));q.append((u,v))
  cy=sum(a for a,b in coords)/len(coords);cx=sum(b for a,b in coords)/len(coords)
  # Connected islands, not a latitude line cutting across land.
  new=0x492B26 if cy>1633 else 0x6090C0 if cx>516 and cy>1618 else 0xB5403E
  components.append({'pixels':len(coords),'box':[min(b for a,b in coords),min(a for a,b in coords),max(b for a,b in coords)+1,max(a for a,b in coords)+1],'after_rgb':'x%06X'%new})
  for a,b in coords:
   old=int(rgb[a,b])
   if old!=new:pixels.append([b,a,'x%06X'%old,'x%06X'%new])
 assert len(components)==7 and len(pixels)==705
 dump('SUPPLEMENTAL_BASELINE.json',{'sources':original,'hawaii_components':components,'pixels':pixels,'bitmap_before_sha256':sha(source_bitmap())})

def bitmap(restore=False):
 evidence=json.loads((OUT/'SUPPLEMENTAL_BASELINE.json').read_text());p=source_bitmap();im=Image.open(p);assert im.mode=='RGB' and im.size==(8192,3616);a=np.array(im)
 if not restore:assert sha(p)==evidence['bitmap_before_sha256'],'Concurrent bitmap edit'
 for x,y,old,new in evidence['pixels']:
  expected,new=(new,old) if restore else (old,new)
  assert 'x%06X'%(int(a[y,x,0])*65536+int(a[y,x,1])*256+int(a[y,x,2]))==expected
  v=int(new[1:],16);a[y,x]=[v>>16,(v>>8)&255,v&255]
 # Mechanical bulk rewrite: no interpolation, palette quantization or new IDs.
 Image.fromarray(a).save(p,format='PNG')
 dump('BITMAP_RECEIPT.json',{'pixels_changed':len(evidence['pixels']),'before_sha256':evidence['bitmap_before_sha256'],'after_sha256':sha(p),'size':[8192,3616],'mode':'RGB','bounded_box':[435,1580,585,1680],'all_pixel_substitutions':'SUPPLEMENTAL_BASELINE.json','operation':'RESTORE' if restore else 'APPLY'})
 print('Hawaii existing-RGB mechanical rewrite:',len(evidence['pixels']),'pixels')

def transform(base):
 supp=json.loads((OUT/'SUPPLEMENTAL_BASELINE.json').read_text());originals=dict(base['originals']);originals.update({p:v['text'] for p,v in supp['sources'].items()});result=dict(originals)
 inv=base['inventory'];geo=json.loads((OUT/'GEOGRAPHY.json').read_text());pixels={r['rgb']:r['pixels'] for r in geo['rgb']};pixels.update({'x492B26':626,'x6090C0':194,'xB5403E':468})
 raw=result['common/history/states/00_states.txt'];moves=[];alloc={};dedup=[]
 for sid,old in [*WHOLE,*PARTIAL]:
  assert sid in TARGETS
  cr=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+old);ps=cr.children('owned_provinces')[0];vs=['x'+cw.scalar(n.value)[1:].upper() for n in ps.children()]
  if (sid,old) in WHOLE:groups={WHOLE[sid,old]:vs}
  else:
   groups={k:v for k,v in PARTIAL[sid,old].items() if isinstance(v,list)};taken={v for vv in groups.values() for v in vv};assert taken<=set(vs)
   remain=next((k for k,v in PARTIAL[sid,old].items() if v=='REMAINDER'),old);groups[remain]=[v for v in vs if v not in taken]
  alloc[sid,old]={t:sum(pixels[v] for v in vs) for t,vs in groups.items() if vs}
  remaining=groups.pop(old,[])
  raw=edits(raw,[(ps.start,ps.end,'owned_provinces = { '+' '.join(remaining)+' }')]) if remaining else edits(raw,[(cr.start,cr.end,'')])
  for tag,vs in groups.items():
   if not vs:continue
   s=state(raw,sid);rs=[n for n in s.children('create_state') if n.one('country')=='c:'+tag]
   if rs:
    n=rs[0].children('owned_provinces')[0];raw=edits(raw,[(n.end-1,n.end-1,' '+' '.join(vs)+' ')])
   else:raw=edits(raw,[(s.end-1,s.end-1,'\n\t\t# MAP2H: documented coarse 1776 allocation.\n\t\tcreate_state = { country = c:'+tag+' owned_provinces = { '+' '.join(vs)+' } }\n')])
   for v in vs:
    case,note=CASE[tag];moves.append({'rgb':v,'state':sid,'before':old,'after':tag,'decision':'DOCUMENTED_GAMEPLAY_APPROXIMATION','case':case,'note':note})
 # Keep Maguindanao's existing southern lowland claim, remove duplicate Lumad claim.
 for sid,tag,extra in [('STATE_MINDANAO','MND',['xE90347']),('STATE_TAHITI','PLY',[])]:
  cr=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+tag);ps=cr.children('owned_provinces')[0];vs=['x'+cw.scalar(n.value)[1:].upper() for n in ps.children()];new=[]
  for v in vs:
   if v in new or v in extra:dedup.append({'rgb':v,'state':sid,'owner':tag,'reason':'retain MGD southern lowland ownership' if v in extra else 'repeated token in same owner list'})
   else:new.append(v)
  raw=edits(raw,[(ps.start,ps.end,'owned_provinces = { '+' '.join(new)+' }')])
 result['common/history/states/00_states.txt']=raw
 pop_alloc=[];building_changes=[];hq=[]
 for path,original in originals.items():
  isp=path.startswith(('common/history/pops/','common/history/population/'));isb=path.startswith('common/history/buildings/')
  if not (isp or isb):continue
  ops=[];pending=[]
  for s in cw.walk(cw.parse(original)):
   sid=s.key.removeprefix('s:')
   for r in s.children():
    old=r.key.removeprefix('region_state:');weights=alloc.get((sid,old))
    if isp and weights:
     ops.append((r.start,r.end,''))
     for p in r.children('create_pop'):
      shares=apportion(int(p.one('size')),weights)
      for tag,number in shares.items():
       if number:pending.append((sid,tag,body_rewrite(original,p,'size',number)));pop_alloc.append([sid,old,tag,p.one('culture'),number])
    elif isb:
     for b in r.children('create_building'):
      kind=cw.scalar(b.one('building'));levels=[n for n in cw.walk([b]) if n.key=='levels']
      if sid=='STATE_MEKONG' and old=='DAI' and kind=='building_barrack':
       assert [n.value for n in levels]==['15'];ops.append((b.start,b.end,''));building_changes.append([path,sid,'STATE_TONKIN|STATE_ANNAM',old,kind,15,'8 to Tonkin and 7 to Annam; no unit changes'])
      elif sid in ['STATE_TONKIN','STATE_ANNAM'] and old=='DAI' and kind=='building_barrack':
       assert [n.value for n in levels]==['20'];n=levels[0];new=28 if sid=='STATE_TONKIN' else 27;ops.append((n.start,n.end,'levels = '+str(new)))
      elif sid=='STATE_ANNAM' and old=='DAI' and kind=='building_railway':
       assert [n.value for n in levels]==['3'];n=levels[0];frag=original[b.start:b.end];one=frag[:n.start-b.start]+'levels = 1'+frag[n.end-b.start:];ops.append((n.start,n.end,'levels = 2'));pending.append((sid,'TSN',one));building_changes.append([path,sid,sid,old,kind,1,'One of three existing roads to rebel subdivision, original DAI private holder conserved'])
      elif sid=='STATE_WEST_JAVA' and old=='DEI' and kind=='building_port':
       assert [n.value for n in levels]==['3'];n=levels[0];frag=original[b.start:b.end];one=frag[:n.start-b.start]+'levels = 1'+frag[n.end-b.start:];ops.append((n.start,n.end,'levels = 2'));pending.append(('STATE_MALAYA','DEI',one));building_changes.append([path,sid,'STATE_MALAYA',old,kind,1,'Existing port level to Malacca; Batavia keeps two, same PM/reserves/DEI holder'])
      elif (sid,old) in WHOLE:
       ops.append((b.start,b.end,''));pending.append((sid,WHOLE[sid,old],original[b.start:b.end]));building_changes.append([path,sid,sid,old,kind,sum(int(n.value) for n in levels),'Territorial selector only; owners retained'])
      elif sid=='STATE_MEKONG' and old=='DAI':
       ops.append((b.start,b.end,''));pending.append((sid,'NGN',original[b.start:b.end]));building_changes.append([path,sid,sid,old,kind,sum(int(n.value) for n in levels),'Southern existing civil building; old DAI economic holder retained'])
  raw=edits(original,ops)
  for sid,tag,content in pending:raw=append(raw,sid,tag,content)
  # DAI no longer owns Mekong: preserve holder country, move its two HQ references.
  if isb:
   ops=[]
   for h in cw.walk(cw.parse(raw)):
    if h.key=='building' and cw.scalar(h.one('country'))=='c:DAI' and cw.scalar(h.one('region'))=='STATE_MEKONG':
     n=h.children('region')[0];ops.append((n.start,n.end,'region = "STATE_TONKIN"'));hq.append([path,'DAI','STATE_MEKONG','STATE_TONKIN'])
   raw=edits(raw,ops)
  if raw!=original:result[path]=raw
 # Reused native definitions and new tags; all other effective definitions retained.
 path='common/country_definitions/00_countries.txt';raw=result[path];ops=[]
 for n in cw.parse(raw):
  if n.key in ['ARK','VIE']:
   cap,kind,tier,cult,rel,color=DEFS[n.key];ops.append((n.start,n.end,n.key+' = { color = { '+' '.join(map(str,color))+' } country_type = '+kind+' tier = '+tier+' cultures = { '+cult+' } religion = '+rel+' capital = '+cap+' }'))
  elif n.key in ['DAI','DGR']:
   c=n.children('capital')[0];ops.append((c.start,c.end,'capital = '+('STATE_TONKIN' if n.key=='DAI' else 'STATE_MEKONG')))
 result[path]=edits(raw,ops)
 path='common/country_definitions/01_pacific_and_australasia.txt';raw=result[path];ops=[]
 for n in cw.parse(raw):
  if n.key=='UNT':
   c=n.children('country_type')[0];ops.append((c.start,c.end,'country_type = decentralized'));r=n.children('religion')[0];ops.append((r.start,r.end,'religion = animist'))
  elif n.key=='HAW':
   r=n.children('religion')[0];ops.append((r.start,r.end,'religion = animist'));c=n.children('is_named_from_capital')[0];ops.append((c.start,c.end,'is_named_from_capital = no'))
  elif n.key=='SRK':
   c=n.children('color')[0];ops.append((c.start,c.end,'color = { 169 127 72 }'))
 result[path]=edits(raw,ops)
 result['common/country_definitions/1776_map2h_countries.txt']='# MAP2H: generic collective tags are explicit engine abstractions.\n'+''.join(tag+' = { color = { '+' '.join(map(str,color))+' } country_type = '+kind+' tier = '+tier+' cultures = { '+cult+' } religion = '+rel+' capital = '+cap+' }\n' for tag,(cap,kind,tier,cult,rel,color) in DEFS.items() if tag not in ['ARK','VIE'])
 assert not (set(DEFS)-{'ARK','VIE'})&set(inv['countries'])
 # New organized governments inherit relevant existing regional technology sets.
 content='COUNTRIES = {\n'
 for tag,template in [('ARK','sia - siam'),('VIE','sia - siam'),('TSN','dai - dai viet'),('NGN','dai - dai viet'),('HMA','haw - hawaii')]:
  node=next(n for n in cw.walk(cw.parse(originals['common/history/countries/'+template+'.txt'])) if n.key.startswith('c:'))
  tech=[cw.scalar(n.value) for n in node.children('add_technology_researched')]
  content+=' c:'+tag+' ?= {\n'+''.join('  add_technology_researched = '+t+'\n' for t in tech)+'  effect_starting_politics_traditional = yes\n  activate_law = law_type:law_monarchy\n  activate_law = law_type:law_autocracy\n  activate_law = law_type:law_freedom_of_conscience\n  activate_law = law_type:law_debt_slavery\n  ig:ig_landowners ?= { add_ruling_interest_group = yes }\n }\n'
 content+='}\n';result['common/history/countries/1776_map2h_start.txt']=content
 path='common/history/countries/lan - lanfang.txt';raw=result[path];n=next(n for n in cw.walk(cw.parse(raw)) if n.key=='set_next_election_date');result[path]=edits(raw,[(n.start,n.end,'# MAP2H: no anticipated 1838 president/election date.')])
 path='common/history/diplomacy/00_subject_relationships.txt';raw=result[path];ops=[]
 for c in cw.walk(cw.parse(raw)):
  for n in c.children('create_diplomatic_pact'):
   if (c.key,n.one('country')) in [('c:SIA','c:CHP'),('c:SIA','c:LUA'),('c:CHI','c:LAN'),('c:DAI','c:CAM')]:ops.append((n.start,n.end,'# MAP2H: remove later suzerainty / no pre-Lanfang Qing tribute.'))
 result[path]=edits(raw,ops)
 # LUA's 1774 alliance was not the Siamese suzerainty of 1778.
 result['common/history/diplomacy/1776_map2h_lao_alliance.txt']='DIPLOMACY = { c:SIA ?= { create_diplomatic_pact = { country = c:LUA type = alliance } } }\n'
 # Preserve the existing 1776 rulers and every military commander; suppress only
 # inherited nineteenth-century ruler/heir templates in three newly recast polities.
 for name in ['dai - dai nam','haw - hawaii','lan - lanfang']:
  result['common/history/characters/'+name+'.txt']='# MAP2H: nineteenth-century templates excluded for the 1776 polity.\nCHARACTERS = { }\n'
 result['common/history/characters/1776_map2h_rulers.txt']='CHARACTERS = {\n c:DAI ?= { create_character = { first_name = aor1776_map2h_trinh_sam last_name = aor1776_map2h_empty historical = yes culture = primary_culture ruler = yes interest_group = ig_landowners ideology = ideology_traditionalist age = 37 } }\n c:HAW ?= { create_character = { first_name = aor1776_map2h_kalaniopuu last_name = aor1776_map2h_empty historical = yes culture = primary_culture ruler = yes interest_group = ig_landowners ideology = ideology_traditionalist age = 76 } }\n}\n'
 # Names remain those of the starting polities; no invented unification events.
 path='common/dynamic_country_names/00_dynamic_country_names.txt';raw=result[path];ops=[]
 for n in cw.parse(raw):
  if n.key in ['DAI','LAN','HAW','UNT']:
   ops.append((n.end-1,n.end-1,'\n dynamic_country_name = { name = aor1776_map2h_'+n.key.lower()+' adjective = '+n.key+'_ADJ priority = 100 is_main_tag_only = yes trigger = { exists = scope:actor } }\n'))
 result[path]=edits(raw,ops)
 for path,raw in list(result.items()):
  if not path.startswith('map_data/state_regions/'):continue
  ops=[]
  for n in cw.parse(raw):
   for kind,v in HUB_FIXES.get(n.key,{}).items():
    h=n.children(kind)[0];ops.append((h.start,h.end,kind+' = "'+v+'"'))
  if ops:result[path]=edits(raw,ops)
 # Hawaii wood locator was on Oahu; mine had an inherited disabled sentinel.
 for kind,x,y in [('wood',529.0,1624.0),('mine',545.0,1654.0)]:
  path=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';raw=result[path];pattern=r'(id\s*=\s*309\s+position\s*=\s*\{)[^}]+';assert len(re.findall(pattern,raw))==1
  result[path]=re.sub(pattern,lambda m:m.group(1)+f' {x:.6f} 0.000000 {3616-y:.6f} ',raw)
 for lang in ['english','french']:
  fr=lang=='french';loc='\ufeffl_'+lang+':\n'
  for tag,v in NAMES.items():
   name=v[2 if fr else 0];loc+=' '+tag+':0 "'+name+'"\n '+tag+'_ADJ:0 "'+v[3 if fr else 1]+'"\n'
   if tag in ['DAI','LAN','HAW','UNT']:loc+=' aor1776_map2h_'+tag.lower()+':0 "'+name+'"\n'
  loc+=' aor1776_map2h_trinh_sam:0 "Trịnh Sâm"\n aor1776_map2h_kalaniopuu:0 "Kalaniʻōpuʻu"\n aor1776_map2h_empty:0 ""\n'
  loc+=' aor1776_map2h_malacca:0 "'+('Malacca' if fr else 'Malacca')+'"\n'
  result[f'localization/{lang}/replace/1776_map2h_l_{lang}.yml']=loc
 result['common/scripted_effects/1776_map2h_state_names.txt']='assign_1776_map2h_split_state_name = { if = { limit = { state_region = s:STATE_MALAYA is_split_state = yes owner = { c:DEI ?= this } } set_state_name = aor1776_map2h_malacca } }\n'
 result['common/on_actions/15_1776_map2h_state_names.txt']='on_game_started = { on_actions = { aor1776_map2h_names_initialize } }\non_game_started_after_lobby = { on_actions = { aor1776_map2h_names_initialize } }\non_state_created = { on_actions = { aor1776_map2h_state_name_changed } }\non_state_owner_change = { on_actions = { aor1776_map2h_state_name_changed } }\naor1776_map2h_names_initialize = { effect = { every_state = { assign_1776_map2h_split_state_name = yes } } }\naor1776_map2h_state_name_changed = { effect = { assign_1776_map2h_split_state_name = yes } }\n'
 flags={t:('brown' if t in ['PLW','UNT','TTI','LAN'] else 'green' if t in ['HAW','VIE'] else 'red' if t=='TSN' else 'blue' if t in ['NGN','HWA'] else 'yellow') for t in [*DEFS,'UNT','LAN','HAW']}
 result['common/coat_of_arms/coat_of_arms/07_1776_map2h_identification.txt']='# Provisional native identification banners, not authentic historical flags.\n'+''.join(t+' = { pattern = "pattern_horizontal_split_01.tga" color1 = "'+c+'" color2 = "white" }\n' for t,c in flags.items())
 changed={p:v for p,v in result.items() if v!=originals.get(p)}
 return changed,{'files':list(changed),'territorial':moves,'duplicates_removed':dedup,'population_redistributions':pop_alloc,'economic_hq':hq,'building_changes':building_changes,'new_tags':sorted(set(DEFS)-{'ARK','VIE'}),'reused_tags':['ARK','VIE'],'recast_tags':['DAI','UNT','LAN','HAW'],'hub_fixes':HUB_FIXES,'bitmap_pixels_changed':705,'allocation':'Whole subdivisions or largest-remainder allocation of existing demographic profiles by native land pixel area; Hawaii uses corrected island groups. Technical approximation, not a 1776 census.'},originals

def build(review_only=False):
 prepare_evidence();base=json.loads(BASE.read_text());changed,plan,originals=transform(base);patch='*** Begin Patch\n'
 if not (OUT/'PIXEL_BASELINE.json').exists():
  import hashlib
  evidence=json.loads((OUT/'SUPPLEMENTAL_BASELINE.json').read_text());assert sha(source_bitmap())==evidence['bitmap_before_sha256']
  a=np.asarray(Image.open(source_bitmap()));dump('PIXEL_BASELINE.json',{'uncompressed_RGB_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'RGB_IDs':sorted(int(v) for v in np.unique(packed(source_bitmap()))),'size':[8192,3616],'mode':'RGB'})
 for p,new in changed.items():
  if not (ROOT/p).exists():patch+='*** Add File: '+str(ROOT/p).replace('\\','/')+'\n'+''.join('+'+l+'\n' for l in new.splitlines());continue
  old=originals.get(p)
  if old is None:
   assert review_only,'File collision '+p
   continue
  if not review_only:assert (ROOT/p).read_text(encoding='utf-8-sig')==old,'Concurrent file edit '+p
  if (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'):old='\ufeff'+old
  if old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
  patch+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
  for line in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=4))[2:]:patch+=('@@' if line.startswith('@@') else line)+'\n'
 (OUT/'INTEGRATION.patch').write_text(patch+'*** End Patch\n',encoding='utf-8');dump('PLAN.json',plan)
 print('Prepared',len(changed),'text files;',len(plan['territorial']),'owner transfers;',len(plan['duplicates_removed']),'duplicate tokens removed')
if __name__=='__main__':
 if '--bitmap' in sys.argv:bitmap()
 elif '--restore-bitmap' in sys.argv:bitmap(True)
 else:build('--review-only' in sys.argv)
