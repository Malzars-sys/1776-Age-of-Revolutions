"""Build a reviewable patch from MAP2G baseline; no direct history writes.
Only remote Qing administrations become subjects. No national army is moved.
"""
import collections as C,difflib,json
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2a_patch import state,edits,append
from map2e_patch import apportion,body_rewrite
from map2g_work import ROOT,OUT,BASE,TARGETS
WHOLE={
 ('STATE_YUNNAN','CHI'):'YUN',('STATE_GUIZHOU','CHI'):'YUN',
 ('STATE_DZUNGARIA','CHI'):'XIN',('STATE_TIANSHAN','CHI'):'XIN',
 ('STATE_ULIASTAI','CHI'):'MGL',('STATE_URGA','CHI'):'MGL',('STATE_TUVA','CHI'):'MGL',
 ('STATE_HOKKAIDO','EZO'):'AIN',('STATE_HOKKAIDO','JAP'):'EZO',
 ('STATE_SAKHALIN','EZO'):'AIN',('STATE_SAKHALIN','ALK'):'RUS',
 ('STATE_CHUKOTKA','ATB'):'CKC',
}
REUSED=['YUN','XIN','MGL','CKC','FRS']
CASE={
 'YUN':('YUNGUI','Qing Yunnan-Guizhou governorship is a remote administrative dependency, not a sovereign Yi kingdom. Only these two southwest regions; no central province split.'),
 'XIN':('ILI','Ili military government and local oasis authorities after the 1750s conquests. Subject abstraction, not a restored Dzungar khanate or the provincial Xinjiang of 1884.'),
 'MGL':('KHALKHA','Uliastai/Urga and Tannu Uriankhai banner administration under Qing supremacy. One grouped subject, not an independent 1911 Mongolian state.'),
 'AIN':('AINU','Ainu communities beyond the southern Matsumae settlement zone; commerce and influence are not uniform direct Japanese territorial administration.'),
 'EZO':('MATSUMAE','Existing three southwest Oshima/Hakodate RGBs represent Matsumae Wajinchi. Existing Matsumae ruler and Japanese vassal link preserved.'),
 'RUS':('NORTHERN_KURILS','Replace the Russian-American colonial TAG with Russia in northern/central Kurils. Whole island-group RGBs abstract limited Russian posts, trade and yasak; not uniform control or a nineteenth-century treaty border.'),
 'CKC':('CHUKOTKA','Chukchi communities rather than North American Athabaska TAG. No anticipation of Russian negotiations of 1778; generic existing Siberian/Inuit/Russian cultures conserved.'),
 'FRS':('TAIWAN','One eastern/mountain RGB represents grouped Indigenous communities outside effective Qing lowland administration. West and north including Taipei/Takow remain Qing; coarse native border is an approximation.'),
}
DEFS={
 'YUN':('STATE_YUNNAN','unrecognized','principality','manchu han yi miao','confucian',[139,181,125]),
 'XIN':('STATE_DZUNGARIA','unrecognized','principality','manchu uighur mongol','confucian',[157,135,194]),
 'MGL':('STATE_ULIASTAI','unrecognized','principality','mongol','gelugpa',[193,157,111]),
 'CKC':('STATE_CHUKOTKA','decentralized','principality','siberian inuit','animist',[126,182,201]),
 'FRS':('STATE_FORMOSA','decentralized','principality','yuanzhumin','animist',[105,157,119]),
}
NAMES={
 'YUN':('Yungui Governorate','Yungui','Gouvernorat du Yungui','du Yungui'),
 'XIN':('Ili Military Government','Ili','Gouvernement militaire d’Ili','d’Ili'),
 'MGL':('Khalkha Banner Administration','Khalkha','Administration des bannières khalkhas','khalkha'),
 'CKC':('Chukchi Communities','Chukchi','Communautés tchouktches','tchouktche'),
 'FRS':('Taiwan Indigenous Communities','Formosan','Communautés autochtones de Taïwan','autochtone de Taïwan'),
 'EZO':('Matsumae Domain','Matsumae','Domaine de Matsumae','de Matsumae'),
}
HUB_FIXES={
 'STATE_FORMOSA':{'port':'xE73B31','mine':'x6DAB21'},
 'STATE_RYUKYU_ISLANDS':{'port':'xF0F061','farm':'xF0D080','wood':'xF0D080','mine':'xBB27F6'},
 'STATE_SAKHALIN':{'city':'x9E3A0A','wood':'x02BAB7','mine':'xE99CEA'},
}
def transform(base):
 result=dict(base['originals']);inv=base['inventory'];raw=result['common/history/states/00_states.txt'];moves=[]
 for (sid,old),tag in WHOLE.items():
  assert sid in TARGETS
  cr=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+old)
  vs=[cw.scalar(n.value) for n in cr.children('owned_provinces')[0].children()]
  exists=[n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+tag]
  if exists:
   at=exists[0].children('owned_provinces')[0].end-1
   raw=edits(raw,[(cr.start,cr.end,''),(at,at,' '+' '.join(vs)+' ')])
  else:
   n=cr.children('country')[0];ops=[(n.start,n.end,'country = c:'+tag)]
   if tag=='RUS':
    st=cr.children('state_type')
    ops.append((st[0].start,st[0].end,'state_type = unincorporated') if st else (cr.end-1,cr.end-1,' state_type = unincorporated '))
   raw=edits(raw,ops)
  for v in vs:
   case,note=CASE[tag];moves.append({'rgb':v,'state':sid,'before':old,'after':tag,'decision':'DOCUMENTED_GAMEPLAY_APPROXIMATION','case':case,'note':note})
 # Taiwan east; do not use land area to move lowland Han residents into mountains.
 cr=next(n for n in state(raw,'STATE_FORMOSA').children('create_state') if n.one('country')=='c:CHI');ps=cr.children('owned_provinces')[0]
 vs=[cw.scalar(n.value) for n in ps.children()];assert 'x44797F' in vs
 raw=edits(raw,[(ps.start,ps.end,'owned_provinces = { '+' '.join(v for v in vs if v!='x44797F')+' }')])
 s=state(raw,'STATE_FORMOSA');raw=edits(raw,[(s.end-1,s.end-1,'\n\t\t# MAP2G: coarse eastern Indigenous territory; western settlements remain Qing.\n\t\tcreate_state = { country = c:FRS owned_provinces = { x44797F } state_type = unincorporated }\n')])
 case,note=CASE['FRS'];moves.append({'rgb':'x44797F','state':'STATE_FORMOSA','before':'CHI','after':'FRS','decision':'DOCUMENTED_GAMEPLAY_APPROXIMATION','case':case,'note':note})
 # Invalid lake selector is not a land transfer or a lost province definition.
 cr=next(n for n in state(raw,'STATE_GANSU').children('create_state') if n.one('country')=='c:CHI');ps=cr.children('owned_provinces')[0]
 assert 'xBD5671' in raw[ps.start:ps.end] and 'xBD5671' not in inv['geometry']
 raw=edits(raw,[(ps.start,ps.end,raw[ps.start:ps.end].replace('xBD5671',''))]);result['common/history/states/00_states.txt']=raw
 # Regroup exact existing demographic fragments; no culture/religion/status edits.
 pop_alloc=[];bt=[]
 for path,original in base['originals'].items():
  isp=path.startswith(('common/history/pops/','common/history/population/'));isb=path.startswith('common/history/buildings/')
  if not (isp or isb):continue
  ops=[];pending=[]
  for s in cw.walk(cw.parse(original)):
   sid=s.key.removeprefix('s:')
   for r in s.children():
    old=r.key.removeprefix('region_state:');dest=WHOLE.get((sid,old))
    if dest:
     frag=original[r.start:r.end];content=frag[frag.index('{')+1:frag.rfind('}')]
     ops.append((r.start,r.end,''));pending.append((sid,dest,content))
     if isp:
      for p in r.children('create_pop'):pop_alloc.append([sid,old,dest,p.one('culture'),int(p.one('size'))])
     else:
      for b in r.children('create_building'):bt.append([path,sid,old,dest,b.one('building')])
    elif isp and sid=='STATE_FORMOSA' and old=='CHI':
     for p in r.children('create_pop'):
      if p.one('culture')!='yuanzhumin':continue
      size=int(p.one('size'));n=apportion(size,{'CHI':30,'FRS':70})
      # Plains Indigenous people remain within the Qing frontier/buffer system.
      ops.append((p.start,p.end,body_rewrite(original,p,'size',n['CHI'])))
      pending.append((sid,'FRS',body_rewrite(original,p,'size',n['FRS'])));pop_alloc.append([sid,'CHI','FRS','yuanzhumin',n['FRS']])
  raw=edits(original,ops)
  for sid,tag,frag in pending:raw=append(raw,sid,tag,frag)
  if raw!=original:result[path]=raw
 # Preserve foreign economic holders. Only now-orphaned HQ locations change.
 hq=[]
 for path,raw in list(result.items()):
  if not path.startswith('common/history/buildings/'):continue
  ops=[]
  for h in cw.walk(cw.parse(raw)):
   if h.key!='building' or not h.children('country') or not h.children('region'):continue
   tag=cw.scalar(h.one('country')).removeprefix('c:');sid=cw.scalar(h.one('region'))
   if (sid,tag) not in WHOLE:continue
   # EZO retains Hokkaido via Matsumae: its headquarters remains valid there.
   if (sid,tag)==('STATE_HOKKAIDO','EZO'):continue
   dest={'CHI':'STATE_HUNAN','JAP':'STATE_TOHOKU','EZO':'STATE_HOKKAIDO','ALK':'STATE_ALASKA','ATB':'STATE_NORTHWEST_TERRITORIES'}[tag]
   assert [dest,tag] in inv['states']
   n=h.children('region')[0];ops.append((n.start,n.end,'region = "'+dest+'"'));hq.append([path,tag,sid,dest])
  if ops:result[path]=edits(raw,ops)
 # Reuse inactive native tags. No central Chinese country changes.
 path='common/country_definitions/00_countries.txt';raw=result[path];ops=[]
 for n in cw.parse(raw):
  if n.key in DEFS:
   cap,kind,tier,cult,rel,color=DEFS[n.key]
   ops.append((n.start,n.end,n.key+' = { color = { '+' '.join(map(str,color))+' } country_type = '+kind+' tier = '+tier+' cultures = { '+cult+' } religion = '+rel+' capital = '+cap+' }'))
  if n.key=='ULT':
   c=n.children('color')[0];ops.append((c.start,c.end,'color = { 122 229 255 }'))
 result[path]=edits(raw,ops)
 path='common/history/countries/ezo - ezochi.txt';result[path]=result[path].replace('law_presidential_republic','law_monarchy')
 # Keep technological/administrative parity with imperial Qing jurisdictions.
 chi=next(n for n in cw.walk(cw.parse(result['common/history/countries/chi - china.txt'])) if n.key=='c:CHI')
 tech=[cw.scalar(n.value) for n in chi.children('add_technology_researched')]
 # Canton-specific policy requires owning Guangdong; remote subjects do not.
 # Its isolationist parent preserves the closed imperial trade framework.
 laws=[cw.scalar(n.value).replace('law_type:law_canton_system','law_type:law_isolationism') for n in chi.children('activate_law')]
 content='COUNTRIES = {\n'
 for tag in ['YUN','XIN','MGL']:
  content+=' c:'+tag+' ?= {\n'+''.join('  add_technology_researched = '+t+'\n' for t in tech)+'  effect_starting_politics_traditional = yes\n'+''.join('  activate_law = '+law+'\n' for law in laws)+'  set_tax_level = low\n }\n'
 content+='}\n';result['common/history/countries/1776_map2g_remote_governments.txt']=content
 result['common/history/diplomacy/1776_map2g_qing_dependencies.txt']='DIPLOMACY = {\n # Imperially appointed governments: vassal is an explicit engine approximation.\n c:CHI ?= {\n  create_diplomatic_pact = { country = c:YUN type = vassal }\n  create_diplomatic_pact = { country = c:XIN type = vassal }\n  create_diplomatic_pact = { country = c:MGL type = vassal }\n }\n}\n'
 # High-priority subject names suppress later clique/modern-state appellations.
 path='common/dynamic_country_names/00_dynamic_country_names.txt';raw=result[path];ops=[]
 for n in cw.parse(raw):
  if n.key in ['YUN','XIN','MGL']:
   ops.append((n.end-1,n.end-1,'\n dynamic_country_name = { name = aor1776_map2g_'+n.key.lower()+' adjective = '+n.key+'_ADJ is_main_tag_only = yes priority = 100 trigger = { exists = scope:actor scope:actor ?= { is_subject_of = c:CHI } } }\n'))
 result[path]=edits(raw,ops)
 # Correct only hub selectors to their already-existing physical locators.
 hub_changes=[]
 for path,original in base['originals'].items():
  if not path.startswith('map_data/state_regions/'):continue
  ops=[]
  for n in cw.parse(original):
   for kind,rgb in HUB_FIXES.get(n.key,{}).items():
    h=n.children(kind)[0];ops.append((h.start,h.end,kind+' = "'+rgb+'"'));hub_changes.append([path,n.key,kind,cw.scalar(h.value),rgb])
  if ops:result[path]=edits(original,ops)
 for lang in ['english','french']:
  fr=lang=='french';loc='\ufeffl_'+lang+':\n'
  for tag,v in NAMES.items():
   loc+=' '+tag+':0 "'+v[2 if fr else 0]+'"\n '+tag+'_ADJ:0 "'+v[3 if fr else 1]+'"\n'
   if tag in ['YUN','XIN','MGL']:loc+=' aor1776_map2g_'+tag.lower()+':0 "'+v[2 if fr else 0]+'"\n'
  result[f'localization/{lang}/replace/1776_map2g_l_{lang}.yml']=loc
 # Native-component identification banners, not claimed authentic historical flags.
 flags={tag:('green' if tag in ['YUN','FRS'] else 'blue' if tag in ['XIN','CKC'] else 'brown') for tag in REUSED}
 result['common/coat_of_arms/coat_of_arms/06_1776_map2g_identification.txt']='# Provisional native-component identifiers; not reconstructed historical banners.\n'+''.join(t+' = { pattern = "pattern_horizontal_split_01.tga" color1 = "'+color+'" color2 = "yellow" }\n' for t,color in flags.items())
 changed={p:v for p,v in result.items() if v!=base['originals'].get(p)}
 return changed,{'files':list(changed),'territorial':moves,'technical_lake_removed':'xBD5671','economic_hq':hq,'population_redistributions':pop_alloc,'building_territorial_selectors':bt,'hub_changes':hub_changes,'reused_tags':REUSED,'new_tags':[],'remote_governments':['YUN','XIN','MGL'],'military_changes':[],'allocation':'Whole owner subdivisions, except 70% of existing yuanzhumin pool to eastern Taiwan; 30% remains Qing. No ethnic recoding; technical split, not census.'}
def build(review_only=False):
 base=json.loads(BASE.read_text(encoding='utf-8'));changed,plan=transform(base);patch='*** Begin Patch\n'
 for p,new in changed.items():
  if p not in base['originals']:
   if not review_only:assert not (ROOT/p).exists(),'File collision '+p
   patch+='*** Add File: '+str(ROOT/p).replace('\\','/')+'\n'+''.join('+'+l+'\n' for l in new.splitlines())
  else:
   if not review_only:assert (ROOT/p).read_text(encoding='utf-8-sig')==base['originals'][p],'Concurrent edit '+p
   old=base['originals'][p]
   if (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'):old='\ufeff'+old
   if old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
   patch+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
   for line in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=4))[2:]:patch+=('@@' if line.startswith('@@') else line)+'\n'
 (OUT/'INTEGRATION.patch').write_text(patch+'*** End Patch\n',encoding='utf-8');(OUT/'PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Prepared',len(changed),'files,',len(moves:=plan['territorial']),'territorial owner changes; no national units changed')
if __name__=='__main__':
 import sys
 build('--refresh-manifest' in sys.argv)
