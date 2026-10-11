"""Emit the narrow, human-reviewable MAP2H finishing patch. No gameplay writes."""
import difflib,json,re,sys
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import state,edits
from map2h_finishing import ROOT,OUT,BASE,dump,sha
WHOLE={'STATE_ACEH':'TOB','STATE_WEST_BORNEO':'KLT','STATE_EAST_BORNEO':'KLT'}
EXTRA=['common/laws/00_governance_principles.txt','common/laws/00_distribution_of_power.txt','localization/english/NM_Countries_l_english.yml','localization/french/NM_Countries_l_french.yml']
def originals(base):
 p=OUT/'SOURCE_BASELINE.json'
 if not p.exists():
  for name in EXTRA:assert sha(ROOT/name)==base['hashes'][name],'Concurrent change '+name
  dump('SOURCE_BASELINE.json',{name:(ROOT/name).read_text(encoding='utf-8-sig') for name in EXTRA})
 raw=dict(base['originals']);raw.update(json.loads(p.read_text()));return raw
def transform(base):
 old=originals(base);new=dict(old);moves=[];hq=[];scope_changes=[]
 path='common/history/states/00_states.txt';raw=new[path];ops=[]
 for sid,tag in WHOLE.items():
  node=next(n for n in state(raw,sid).children('create_state') if cw.scalar(n.one('country'))=='c:INDOP');country=node.children('country')[0];ops.append((country.start,country.end,'country = c:'+tag))
  for n in node.children('owned_provinces')[0].children():moves.append({'rgb':'x'+cw.scalar(n.value)[1:].upper(),'state':sid,'before':'INDOP','after':tag,'status':'DOCUMENTED_GAMEPLAY_APPROXIMATION'})
 new[path]=edits(raw,ops)
 for path,raw in list(old.items()):
  if not path.startswith(('common/history/pops/','common/history/population/','common/history/buildings/')):continue
  ops=[]
  for s in cw.walk(cw.parse(raw)):
   sid=s.key.removeprefix('s:');tag=WHOLE.get(sid)
   if not tag:continue
   for r in s.children('region_state:INDOP'):
    ops.append((r.start,r.start+len(r.key),'region_state:'+tag));scope_changes.append([path,sid,'INDOP',tag])
  # All holders stay INDOP. Its old offshore HQ selectors move to an owned
  # Sumatra subdivision. No building PM, reserves or ownership levels change.
  if path.startswith('common/history/buildings/'):
   for h in cw.walk(cw.parse(raw)):
    if h.key=='building' and cw.scalar(h.one('country'))=='c:INDOP' and cw.scalar(h.one('region')) in WHOLE:
     r=h.children('region')[0];hq.append([path,'INDOP',cw.scalar(r.value),'STATE_NORTH_SUMATRA']);ops.append((r.start,r.end,'region = "STATE_NORTH_SUMATRA"'))
  if ops:new[path]=edits(raw,ops)
 path='common/country_definitions/00_countries.txt';raw=new[path];ops=[]
 for n in cw.parse(raw):
  if n.key in ['TOB','KLT']:
   cap='STATE_ACEH' if n.key=='TOB' else 'STATE_WEST_BORNEO';cult='batak' if n.key=='TOB' else 'bornean dayak';color='135 87 154' if n.key=='TOB' else '75 149 121'
   replacement=n.key+' = { # MAP2H: regional communities, not a unitary kingdom.\n color = { '+color+' } country_type = decentralized tier = principality cultures = { '+cult+' } religion = animist capital = '+cap+'\n}'
   ops.append((n.start,n.end,replacement))
 new[path]=edits(raw,ops)
 path='common/country_definitions/02_modded_countries.txt';raw=new[path];n=next(n for n in cw.parse(raw) if n.key=='INDOP');c=n.children('cultures')[0]
 new[path]=edits(raw,[(c.start,c.end,'cultures = { sumatran batak }')]).replace('INDOP = { # Princely Indonesian States','INDOP = { # MAP2H: decentralized Sumatran communities; Batak and Borneo groups are separate.')
 # Keep KAU unrecognized/playable. Use the actual chiefdom/elder laws, with
 # a country-specific exception to their usual decentralized-only visibility.
 path='common/history/countries/kau - kaurna.txt';raw=new[path]
 raw=raw.replace('activate_law = law_type:law_parliamentary_republic # Tribal but the closest I can get','activate_law = law_type:law_chiefdom # Native customary-government abstraction; KAU remains playable.')
 raw=raw.replace('activate_law = law_type:law_census_voting # Would actually have been more akin to anarchy but gameplay','activate_law = law_type:law_elder_council')
 raw=raw.replace('\t\tactivate_law = law_type:law_elected_bureaucrats','\t\t# Retain the traditional initializer bureaucracy fallback, not elected officials.')
 raw=raw.replace('law_type:law_racial_segregation','law_type:law_subjecthood').replace('law_type:law_women_own_property','law_type:law_no_womens_rights').replace('law_type:law_homesteading','law_type:law_serfdom')
 raw=raw.replace('\t\tactivate_law = law_type:law_consumption_based_taxation','\t\tactivate_law = law_type:law_consumption_based_taxation\n\t\tactivate_law = law_type:law_censorship\n\t\tactivate_law = law_type:law_debt_slavery')
 new[path]=raw
 for path,key,blocks in [('common/laws/00_governance_principles.txt','law_chiefdom',['can_enact','is_visible']),('common/laws/00_distribution_of_power.txt','law_elder_council',['is_visible'])]:
  raw=new[path];n=next(n for n in cw.parse(raw) if n.key==key);ops=[]
  for block in blocks:
   b=n.children(block)[0];assert len(b.children())==1 and b.one('is_country_type')=='decentralized'
   v=b.children()[0];ops.append((v.start,v.end,'aor1776_customary_laws_country_allowed = yes'))
  new[path]=edits(raw,ops)
 new['common/scripted_triggers/1776_map2h_kaurna_customary_laws.txt']='''# Preserve the native rule for every other country. Only playable KAU gains an exception.
aor1776_customary_laws_country_allowed = {
 OR = {
  is_country_type = decentralized
  AND = { is_country_type = unrecognized exists = c:KAU c:KAU = ROOT }
 }
}
'''
 new['common/history/countries/1776_map2h_indop_communities.txt']='''# Native community initialization only; no historical ruler or modern technology invented.
COUNTRIES = {
 c:TOB ?= { effect_starting_politics_traditional = yes activate_law = law_type:law_elder_council }
 c:KLT ?= { effect_starting_politics_traditional = yes activate_law = law_type:law_elder_council }
}
'''
 new['common/history/diplomacy/1776_map2h_vietnam_rapprochement.txt']='''# The rapprochement of 1775 is temporary, not a permanent alliance or subject pact.
# 24 months is a gameplay duration, not a claimed historical treaty expiration.
DIPLOMACY = {
 c:DAI ?= {
  set_relations = { country = c:TSN value = 20 }
  create_bidirectional_truce = { country = c:TSN months = 24 }
 }
 c:TSN ?= {
  set_relations = { country = c:NGN value = -60 }
  create_diplomatic_pact = { country = c:NGN type = rivalry }
 }
 c:NGN ?= { create_diplomatic_pact = { country = c:TSN type = rivalry } }
}
'''
 for lang in ['english','french']:
  fr=lang=='french';path=f'localization/{lang}/NM_Countries_l_{lang}.yml';raw=new[path]
  raw=re.sub(r'^ INDOP:.*$', ' INDOP: "'+('Communautés de Sumatra' if fr else 'Sumatran Communities')+'"',raw,flags=re.M)
  raw=re.sub(r'^ INDOP_ADJ:.*$', ' INDOP_ADJ: "'+('sumatranes' if fr else 'Sumatran')+'"',raw,flags=re.M);new[path]=raw
  loc='\ufeffl_'+lang+':\n'
  pairs={'TOB':('Communautés batak' if fr else 'Batak Communities'),'TOB_ADJ':'batak' if fr else 'Batak','KLT':('Communautés dayak et bornéennes' if fr else 'Dayak and Bornean Communities'),'KLT_ADJ':('de Bornéo' if fr else 'Bornean'),'aor1776_map2h_tapanuli':'Tapanuli'}
  for k,v in pairs.items():loc+=' '+k+':0 "'+v+'"\n'
  new[f'localization/{lang}/replace/1776_map2h_communities_l_{lang}.yml']=loc
 new['common/scripted_effects/1776_map2h_tapanuli_name.txt']='assign_1776_map2h_tapanuli_name = { if = { limit = { state_region = s:STATE_ACEH is_split_state = yes owner = { c:TOB ?= this } } set_state_name = aor1776_map2h_tapanuli } }\n'
 new['common/on_actions/16_1776_map2h_tapanuli_name.txt']='''on_game_started = { on_actions = { aor1776_map2h_tapanuli_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_map2h_tapanuli_initialize } }
on_state_created = { on_actions = { aor1776_map2h_tapanuli_name_changed } }
on_state_owner_change = { on_actions = { aor1776_map2h_tapanuli_name_changed } }
aor1776_map2h_tapanuli_initialize = { effect = { every_state = { assign_1776_map2h_tapanuli_name = yes } } }
aor1776_map2h_tapanuli_name_changed = { effect = { assign_1776_map2h_tapanuli_name = yes } }
'''
 new['common/coat_of_arms/coat_of_arms/08_1776_map2h_communities.txt']='# Generic native identification banners, not authenticated historical flags.\nTOB = { pattern = "pattern_horizontal_split_01.tga" color1 = "purple" color2 = "white" }\nKLT = { pattern = "pattern_horizontal_split_01.tga" color1 = "green" color2 = "brown" }\n'
 changed={p:r for p,r in new.items() if r!=old.get(p)}
 return changed,{'files':list(changed),'transfers':moves,'whole_fragments':WHOLE,'headquarters':hq,'selector_changes':scope_changes,'reused_tags':['TOB','KLT'],'new_tags':[],'truce_months':24,'truce_end_nominal':'1778.1.1','territorial_authorization':'User explicitly approved splitting only INDOP with existing RGBs; no other historic states repartitioned.','KAU_playability':'unrecognized country_type unchanged; chiefdom and elder council laws gain KAU-only native eligibility exception.'},old
def build(review_only=False):
 base=json.loads(BASE.read_text());changed,plan,old=transform(base);patch='*** Begin Patch\n'
 for p,new in changed.items():
  if p not in old:patch+='*** Add File: '+str(ROOT/p).replace('\\','/')+'\n'+''.join('+'+l+'\n' for l in new.splitlines());continue
  if not review_only:assert (ROOT/p).read_text(encoding='utf-8-sig')==old[p],'Concurrent source edit '+p
  prev=old[p]
  if (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'):
   prev='\ufeff'+prev
   if not new.startswith('\ufeff'):new='\ufeff'+new
  patch+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
  for l in list(difflib.unified_diff(prev.splitlines(),new.splitlines(),n=4))[2:]:patch+=('@@' if l.startswith('@@') else l)+'\n'
 (OUT/'INTEGRATION.patch').write_text(patch+'*** End Patch\n',encoding='utf-8');dump('PLAN.json',plan);print('Prepared',len(changed),'files;',len(plan['transfers']),'INDOP RGBs')
if __name__=='__main__':build('--review-only' in sys.argv)
