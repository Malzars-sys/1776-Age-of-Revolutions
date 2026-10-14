"""Emit a deterministic apply_patch payload. Never write gameplay directly."""
import collections as C,difflib,json,sys
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import state,edits
from map2i_work import ROOT,OUT,BASE
TAG='AFH'
def transform(base):
 originals=base['originals'];result=dict(originals);moves=[];hq=[];mil=[]
 p='common/history/states/00_states.txt';raw=result[p];s=state(raw,'STATE_KHORASAN');cr=s.children('create_state')[0];assert cw.scalar(cr.one('country'))=='c:PER'
 n=cr.children('country')[0];raw=edits(raw,[(n.start,n.end,'country = c:AFH')]);result[p]=raw
 geo={r['rgb']:r for r in json.loads((OUT/'GEOGRAPHY.json').read_text())['rgb']}
 for r in base['inventory']['owners']:
  v,sid,t=r['key']
  if (sid,t)==('STATE_KHORASAN','PER'):moves.append({'rgb':v,'state':sid,'before':t,'after':TAG,'decision':'DOCUMENTED_GAMEPLAY_APPROXIMATION','pixels':geo[v]['pixels'],'limits':'Regional aggregation under the Mashhad court includes autonomous local khans. Not proof of uniform Shahrokh administration.'})
 # Entire existing subdivision changes political ownership: no population split.
 for p,raw in originals.items():
  if not p.startswith(('common/history/pops/','common/history/population/','common/history/buildings/')):continue
  ops=[]
  for s in cw.walk(cw.parse(raw)):
   if s.key!='s:STATE_KHORASAN':continue
   for r in s.children('region_state:PER'):
    frag=raw[r.start:r.end].replace('region_state:PER','region_state:AFH',1);ops.append((r.start,r.end,frag))
  changed=edits(raw,ops)
  if p.startswith('common/history/buildings/'):
   ops=[]
   for h in cw.walk(cw.parse(changed)):
    if h.key=='building' and cw.scalar(h.one('country',''))=='c:PER' and cw.scalar(h.one('region',''))=='STATE_KHORASAN':
     n=h.children('region')[0];ops.append((n.start,n.end,'region = "STATE_KERMAN"'));hq.append([p,cw.scalar(h.one('type')),'PER','STATE_KHORASAN','STATE_KERMAN',int(h.one('levels'))])
   changed=edits(changed,ops)
  if changed!=raw:result[p]=changed
 # Keep Persian nationality, formations, commander and service types.
 p='common/history/military_formations/04_military_formations_middle_east.txt';raw=result[p];ops=[]
 for c in cw.walk(cw.parse(raw)):
  if c.key!='c:PER':continue
  for u in cw.walk([c]):
   if u.key=='combat_unit' and cw.scalar(u.one('state_region',''))=='s:STATE_KHORASAN':
    n=u.children('state_region')[0];service=cw.scalar(u.one('service_type','regular'));dest='STATE_KERMAN' if service=='regular' else None
    if dest:
     ops.append((n.start,n.end,'state_region = s:'+dest));mil.append(['STATE_KHORASAN',dest,service,int(u.one('count'))])
    else:
     assert int(u.one('count'))==4
     chunks=[]
     for dest,num in [('STATE_LURISTAN',1),('STATE_PERSIAN_KURDISTAN',1),('STATE_URMIA',1),('STATE_MAZANDARAN',1)]:
      frag=raw[u.start:u.end];nn=u.children('count')[0];chunks.append(edits(frag,[(n.start-u.start,n.end-u.start,'state_region = s:'+dest),(nn.start-u.start,nn.end-u.start,'count = '+str(num))]));mil.append(['STATE_KHORASAN',dest,service,num])
     ops.append((u.start,u.end,'\n\t\t\t'.join(chunks)))
 result[p]=edits(raw,ops)
 # Only PER capital changes. All buildings and military formations stay put.
 p='common/country_definitions/00_countries.txt';raw=result[p];per=next(n for n in cw.parse(raw) if n.key=='PER');cap=per.children('capital')[0];assert cap.value=='STATE_IRAKAJEMI';result[p]=edits(raw,[(cap.start,cap.end,'capital = STATE_FARS')])
 p='common/dynamic_country_names/00_dynamic_country_names.txt';raw=result[p];per=next(n for n in cw.parse(raw) if n.key=='PER');zand=next(n for n in per.children('dynamic_country_name') if n.one('name')=='dyn_c_zand_iran');tr=zand.children('trigger')[0]
 result[p]=edits(raw,[(tr.start,tr.end,'trigger = { scope:actor ?= { has_law = law_type:law_monarchy NOT = { has_variable = qajar_iran } ruler ?= { has_template = per_karim_khand_zand_template } } }')])
 # Reuse existing play rather than add a second conflict or predetermined victory.
 p='common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt';raw=result[p];assert raw.count('war = no')==1;result[p]=raw.replace('war = no','# MAP-2I: ongoing siege since 1775; Basra still belongs to IR1.\n\t\t\twar = yes')
 result['common/country_definitions/07_1776_map2i_afsharids.txt']='''# MAP-2I: regional Mashhad polity, not restored Nader Shah's empire.
AFH = {
 color = { 145 82 130 }
 country_type = unrecognized
 tier = kingdom
 cultures = { persian }
 religion = shiite
 capital = STATE_KHORASAN
}
'''
 per=cw.parse(originals['common/history/countries/per - persia.txt'])[0].children()[0]
 tech=[cw.scalar(n.value) for n in per.children('add_technology_researched')];laws=[cw.scalar(n.value) for n in per.children('activate_law')]
 result['common/history/countries/afh - afsharid khorasan.txt']='COUNTRIES = {\n c:AFH ?= {\n'+''.join('  add_technology_researched = '+v+'\n' for v in tech)+'''  ig:ig_landowners ?= { add_ruling_interest_group = yes }
  ig:ig_devout ?= { add_ruling_interest_group = yes }
  effect_starting_politics_conservative = yes
'''+''.join('  activate_law = '+v+'\n' for v in laws)+'  set_tax_level = medium\n }\n}\n'
 result['common/history/characters/afh - afsharid khorasan.txt']='''CHARACTERS = {
 c:AFH ?= {
  create_character = {
   first_name = aor1776_map2i_shahrokh
   last_name = aor1776_map2i_afshar
   historical = yes
   culture = cu:persian
   religion = rel:shiite
   home_region = STATE_KHORASAN
   age = 41 # Birth year 1734; no invented exact date.
   ruler = yes
   interest_group = ig_landowners
   ideology = ideology_traditionalist
  }
 }
}
'''
 result['common/government_types/00_1776_map2i_afsharids.txt']='''gov_1776_afsharid_khorasan = {
 transfer_of_power = hereditary
 male_ruler = "RULER_TITLE_SHAH"
 female_ruler = ""
 male_heir = "RULER_TITLE_CROWN_PRINCE"
 female_heir = ""
 possible = { has_law = law_type:law_monarchy c:AFH ?= ROOT NOT = { is_subject_type = subject_type_crown_land } }
 on_government_type_change = { change_to_hereditary = yes }
 on_post_government_type_change = { post_change_to_hereditary = yes }
}
'''
 # Native defensive guarantee acknowledges external Afghan protection/influence;
 # no vassal/tributary/treaty payment or permanent alliance is invented.
 result['common/history/diplomacy/07_1776_map2i_afsharids.txt']='''DIPLOMACY = {
 c:DUR ?= {
  set_relations = { country = c:AFH value = 20 }
 }
 c:AFH ?= { set_relations = { country = c:PER value = -10 } }
}
'''
 result['common/history/treaties/07_1776_map2i_afsharids.txt']='''TREATIES = {
 # Revocable gameplay representation of Durrani protection after the 1770 settlement.
 # The initialization date is mechanical, not a claimed surviving treaty date.
 create_treaty = {
  first_country = c:DUR
  second_country = c:AFH
  is_draft = no
  entered_into_force_on = 1776.1.1
  binding_period = { years = 1 }
  articles_to_create = {
   { article = guarantee_independence source_country = c:DUR target_country = c:AFH }
  }
 }
}
'''
 result['common/coat_of_arms/coat_of_arms/07_1776_map2i_identification.txt']='''# Provisional native-component identification banner, NOT an authenticated flag.
AFH = { pattern = "pattern_horizontal_split_01.tga" color1 = "purple" color2 = "yellow" }
'''
 for lang in ['french','english']:
  fr=lang=='french';vals={'AFH':'Khorassan afsharide' if fr else 'Afsharid Khorasan','AFH_ADJ':'Afsharide','dyn_c_zand_iran':'Perse zand' if fr else 'Zand Persia','RULER_TITLE_VAKIL':"Vakil al-Ra‘aya",'aor1776_map2i_shahrokh':'Shahrokh','aor1776_map2i_afshar':'Afshar','gov_1776_afsharid_khorasan':'Monarchie afsharide' if fr else 'Afsharid Monarchy','gov_1776_afsharid_khorasan_desc':'Le shah règne à Machhad avec sa cour et les autorités locales du Khorassan.' if fr else 'The shah rules in Mashhad alongside his court and the local authorities of Khorasan.'}
  if not fr:vals['AFH_ADJ']='Afsharid'
  result[f'localization/{lang}/replace/1776_map2i_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in vals.items())
 changed={p:v for p,v in result.items() if v!=originals.get(p)}
 return changed,{'files':list(changed),'territorial':moves,'economic_headquarters':hq,'military_recruitment':mil,'capital':['PER','STATE_IRAKAJEMI','STATE_FARS'],'new_tags':[TAG],'bitmap_changed':False,'population_split':False,'afsharid_representation':'Regional aggregation; autonomous Bayat/Kurdish/Arab/local authorities not individually tagged. Durrani guarantee is a revocable native approximation, not a proved 1776 treaty.'}
def build(review_only=False):
 base=json.loads(BASE.read_text());changed,plan=transform(base);payload='*** Begin Patch\n'
 for p,new in changed.items():
  if p not in base['originals']:
   if not review_only:assert not (ROOT/p).exists(),'New-file collision '+p
   payload+='*** Add File: '+str(ROOT/p).replace('\\','/')+'\n'+''.join('+'+l+'\n' for l in new.splitlines())
  else:
   if not review_only:assert (ROOT/p).read_text(encoding='utf-8-sig')==base['originals'][p],'Concurrent edit '+p
   old=base['originals'][p]
   if (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'):old='\ufeff'+old;new='\ufeff'+new if not new.startswith('\ufeff') else new
   payload+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
   for line in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=4))[2:]:payload+=('@@' if line.startswith('@@') else line)+'\n'
 (OUT/'INTEGRATION.patch').write_text(payload+'*** End Patch\n',encoding='utf-8');(OUT/'PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print('Prepared',len(changed),'files;',len(plan['territorial']),'RGB transfers')
if __name__=='__main__':build('--refresh-manifest' in sys.argv)
