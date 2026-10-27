"""Compile the explicit constitutional registry into an apply_patch payload.

Never write runtime files directly. Generated de-jure rights freeze the approved
1776 province assignments, not every possession or future imperial conquest.
"""
import json,re,difflib,collections
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective,values
from map2k_patch import MEMBERS,ELECTORS,NEW
from map2k_work import ROOT,GAME,OUT
from map2a_patch import edits
from map2l_registry import active_registry_path,additional_members,member_region_overrides,territorial_holder_overrides,rightful_holder_condition,provincial_membership_overrides
MEMBERS=MEMBERS+['HAN']+additional_members()
REGIONS={'STATE_AUSTRIA','STATE_BOHEMIA','STATE_MORAVIA','STATE_ISTRIA','STATE_SLOVENIA','STATE_SOUTH_TYROL','STATE_STYRIA','STATE_TYROL','STATE_LOMBARDY','STATE_FLANDERS','STATE_GELRE','STATE_WALLONIA','STATE_BAVARIA','STATE_FRANCONIA','STATE_ANHALT','STATE_BRANDENBURG','STATE_BRUNSWICK','STATE_LOWER_SILESIA','STATE_UPPER_SILESIA','STATE_NORTH_RHINE','STATE_POMERANIA','STATE_RHINELAND','STATE_RUHR','STATE_WESTPHALIA','STATE_EMILIA','STATE_WURTTEMBERG','STATE_HESSE','STATE_MECKLENBURG','STATE_ELBE','STATE_HANNOVER','STATE_SAXONY','STATE_BADEN','STATE_TUSCANY','STATE_SCHLESWIG_HOLSTEIN'}
IDENTITY='identity_aor1776_imperial_federation'
def block(k,body):return k+' = {\n'+body+'\n}\n'
def scoped(tag,body):return 'c:'+tag+' ?= {\n'+body+'\n}\n'
def emit(files):
 p=['*** Begin Patch']
 for rel,new in files.items():
  target=ROOT/rel;old=target.read_text(encoding='utf-8') if target.exists() else None
  if old is not None and old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
  if old==new:continue
  if old is None:p+=['*** Add File: '+str(target)]+['+'+x for x in new.splitlines()]
  else:
   p+=['*** Update File: '+str(target)];p+=['@@' if x.startswith('@@') else x for x in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=30))[2:]]
 p+=['*** End Patch'];(OUT/'IMPERIAL_SYSTEM.patch').write_text('\n'.join(p)+'\n',encoding='utf-8')
 print('Prepared',len(files),'runtime files; apply IMPERIAL_SYSTEM.patch explicitly')
def compile_system():
 files={};inv=qa.inventory();ledger=[];overrides=member_region_overrides();territorial=territorial_holder_overrides();provincial=provincial_membership_overrides()
 for row in inv['owners']:
  rgb,sid,tag=row['key']
  if (tag in MEMBERS and sid in overrides.get(tag,REGIONS)) or sid in territorial.get(tag,set()) or (rgb,sid,tag) in provincial:
   assert row['count']==1,'Cannot register multiply assigned province '+rgb
   ledger.append(dict(rgb=rgb,state=sid,beneficiary=tag,basis='Frozen 1776 gameplay assignment; NOT a new historical territorial claim'))
 registry=active_registry_path()
 if registry.exists():
  reviewed=json.loads(registry.read_text(encoding='utf-8'))
  fields=lambda rows:[(r['rgb'],r['state'],r['beneficiary']) for r in rows]
  assert fields(reviewed)==fields(ledger),'Reviewed de-jure registry changed: review new territorial history explicitly before recompiling'
  ledger=reviewed
 else:registry.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
 groups=[]
 for p in effective(ROOT,GAME,'common/power_bloc_principle_groups'):
  for n in cw.parse(p.read_text(encoding='utf-8-sig')):
   levels=values(n,'levels')
   if levels:groups.append((n.key,levels))
 from map2k_imperial_principles import GROUPS
 for key,levels in GROUPS.items():
  if key not in {g for g,ls in groups}:groups.append((key,levels))
 (OUT/'PRINCIPLE_SNAPSHOT_SCHEMA.json').write_text(json.dumps(groups,indent=2),encoding='utf-8')
 tags=' '.join('c:'+t+' ?= this' for t in MEMBERS)
 titles=' '.join('c:'+t+' ?= this' for t in ELECTORS.values())
 triggers=block('aor1776_hre_member','NOT = { has_variable = aor1776_hre_seceded }\nOR = { '+tags+' }')
 triggers+=block('aor1776_hre_emperor','exists = global_var:aor1776_hre_emperor_country\nthis = global_var:aor1776_hre_emperor_country')
 triggers+=block('aor1776_hre_elector','aor1776_hre_member = yes\nOR = { has_law_or_variant = law_type:law_monarchy has_law_or_variant = law_type:law_theocracy }\nany_scope_state = { always = yes }\nOR = { '+titles+' }')
 male='is_character_alive = yes is_female = no age >= 18 NOT = { has_variable = aor1776_hre_deceased_emperor }'
 triggers+=block('aor1776_hre_candidate','aor1776_hre_member = yes\nis_subject = no\nhas_law_or_variant = law_type:law_monarchy\nOR = { ruler ?= { '+male+' } heir ?= { '+male+' } }')
 triggers+=block('aor1776_hre_ballot_candidate','aor1776_hre_candidate = yes\nOR = { NOT = { has_global_variable = aor1776_hre_runoff } has_variable = aor1776_hre_finalist }')
 # State trigger: selected state supplies its region and owner; RGB provenance
 # prevents returning somebody else's legitimate part of a split state.
 bystate=collections.defaultdict(list)
 for r in ledger:bystate[r['state']].append(r)
 checks=[];returns=[]
 for sid,rows in sorted(bystate.items()):
  opts=[];effects=[]
  for r in rows:
   tag,rgb=r['beneficiary'],r['rgb']
   rightful=rightful_holder_condition(r)
   restore_rightful='' if sid in territorial.get(tag,set()) else f'c:{tag} = {{ aor1776_hre_member = yes }}'
   valid=f'{rightful} NOT = {{ owner = c:{tag} }} p:{rgb}.state ?= this'
   opts.append('AND = { '+valid+' }')
   effects.append(f'if = {{ limit = {{ exists = c:{tag} {restore_rightful} p:{rgb}.state = {{ owner = scope:hre_holder }} NOT = {{ c:{tag} = scope:hre_holder }} }} s:{sid} = {{ set_owner_of_provinces = {{ country = c:{tag} provinces = {{ {rgb} }} }} }} }}')
  checks.append('AND = { state_region = s:'+sid+' OR = { '+' '.join(opts)+' } }')
  returns.append('if = { limit = { scope:hre_request_state = { state_region = s:'+sid+' } } '+'\n'.join(effects)+' }')
 triggers+=block('aor1776_hre_restitution_state','OR = {\n'+'\n'.join(checks)+'\n}')
 triggers+=block('aor1776_hre_restitution_cooldown','has_variable = aor1776_hre_restitution_cooldown\nvar:aor1776_hre_request_holder = owner')
 triggers+=block('aor1776_hre_external_imperial_overlord','aor1776_hre_member = no\nany_subject_or_below = { aor1776_hre_member = yes }')
 trigger_labels={
 'aor1776_hre_member':('Belongs to the recognised imperial estates and has not seceded.','Appartient aux États impériaux reconnus et n’a pas fait sécession.'),
 'aor1776_hre_emperor':('Holds the imperial crown.','Détient la couronne impériale.'),
 'aor1776_hre_elector':('Holds one of the nine recognised electoral titles, still has territory, and retains a monarchy or ecclesiastical government.','Détient l’un des neuf titres électoraux reconnus, possède encore un territoire et conserve une monarchie ou un gouvernement ecclésiastique.'),
 'aor1776_hre_candidate':('An independent imperial monarchy with a living adult male ruler or heir.','Une monarchie impériale indépendante avec un souverain ou héritier masculin majeur et vivant.'),
 'aor1776_hre_ballot_candidate':('Eligible for the current imperial ballot.','Éligible au scrutin impérial en cours.'),
 'aor1776_hre_restitution_state':('Contains registered imperial provinces held by someone other than their surviving rightful imperial holder.','Contient des provinces impériales enregistrées détenues par un autre pays que leur titulaire impérial légitime encore existant.'),
 'aor1776_hre_restitution_cooldown':('This holder has already received a demand for this territory during the waiting period.','Ce détenteur a déjà reçu une demande sur ce territoire pendant le délai d’attente.'),
 'aor1776_hre_external_imperial_overlord':('An external power holding at least one recognised imperial estate as a subject.','Une puissance extérieure détenant au moins un État impérial reconnu comme sujet.'),
 }
 pretty=[]
 for n in cw.parse(triggers):
  original=triggers[n.start:n.end];inside=original[original.index('{')+1:original.rindex('}')]
  pretty.append(block(n.key,'custom_tooltip = { text = '+n.key+'_tt\n'+inside+'\n}'))
 triggers='\n'.join(pretty)
 files['common/scripted_triggers/1776_imperial_constitution.txt']=triggers
 identity=block(IDENTITY,'''
 visible = { has_variable = aor1776_hre_creation_permitted }
 possible = { has_variable = aor1776_hre_creation_permitted }
 can_join = { aor1776_hre_member = yes }
 can_leave = { always = no }
 power_bloc_modifier = {
  power_bloc_customs_union_bool = yes
  power_bloc_mandate_progress_per_great_power_member_add = 10
  power_bloc_mandate_progress_per_major_power_member_add = 5
  power_bloc_mandate_progress_per_minor_power_member_add = 2
  power_bloc_cohesion_per_member_add = -1
 }
 leader_modifier = {}
 non_leader_modifier = {}
 mandate_progress = power_bloc_mandate_progress_by_rank
 cohesion = { value = 60 }
 ai_weight = { value = 0 }
 icon = "gfx/interface/icons/central_identity_pillars_icons/aor1776_imperial_federation_v2.dds"
 background = "gfx/interface/power_blocs/backgrounds/pb_background_generic.dds"
''')
 files['common/power_bloc_identities/1776_imperial_federation.txt']=identity
 history=(ROOT/'common/history/power_blocs/00_power_blocs.txt').read_text(encoding='utf-8-sig')
 aus=next(n for n in cw.walk(cw.parse(history)) if n.key=='c:AUS')
 section=history[aus.start:aus.end].replace('identity = identity_trade_league','identity = '+IDENTITY)
 section=section.replace('962.6.9 # Final agreement of the 1814 Congress of Vienna','962.6.9 # Imperial coronation of Otto I; constitution represented minimally.')
 # Restored electorates and explicitly reviewed later estates. Foreign unions kept.
 restored=list(NEW)+additional_members()
 seen=set();dedupe=[]
 for n in cw.walk(cw.parse(section)):
  if n.key=='member' and cw.scalar(n.value).removeprefix('c:') in restored:
   tag=cw.scalar(n.value)
   if tag in seen:dedupe.append((n.start,n.end,''))
   else:seen.add(tag)
 section=edits(section,dedupe)
 missing=[t for t in restored if 'c:'+t not in seen]
 if missing:section=section.replace('member = c:MOD','\n            '.join('member = c:'+t for t in missing)+'\n            member = c:MOD',1)
 files['common/history/power_blocs/00_power_blocs.txt']=history[:aus.start]+section+history[aus.end:]
 pact=block('aor1776_imperial_obligation','''
 groups = { power_bloc }
 requires_approval = no
 show_in_lens = no
 potential = { always = no } # Scripted constitutional pact, never a free invite.
 pact = {
  cost = 0
  is_two_sided_pact = no
  income_transfer = 0
  actor_can_break = { always = no }
  target_can_break = { always = no }
  auto_support_type = dp_aor1776_hre_restitution
 }
 ai = { will_break = { always = no } will_propose = { always = no } }
''')
 action=block('aor1776_hre_request_restitution','''
 groups = { general power_bloc }
 requires_approval = no # Forced members transfer immediately; others get an event.
 state_selection = second_required
 second_state_list = second_country
 should_notify_third_parties = yes
 show_effect_in_tooltip = yes
 selectable = { aor1776_hre_emperor = yes }
 potential = {
  NOT = { this = scope:target_country }
  scope:target_country = { any_scope_state = { aor1776_hre_restitution_state = yes } }
 }
 possible = {
  is_diplomatic_play_committed_participant = no
  NOT = { has_war_with = scope:target_country }
  scope:target_country = { is_diplomatic_play_committed_participant = no }
  exists = scope:second_state
  scope:second_state = { aor1776_hre_restitution_state = yes NOT = { aor1776_hre_restitution_cooldown = yes } }
 }
 second_state_trigger = {
  owner = scope:target_country
  aor1776_hre_restitution_state = yes
  NOT = { aor1776_hre_restitution_cooldown = yes }
  is_under_colonization = no
 }
 accept_effect = {
  save_scope_as = hre_request_emperor
  scope:target_country = { save_scope_as = hre_holder }
  scope:second_state = {
   save_scope_as = hre_request_state
   set_variable = { name = aor1776_hre_restitution_cooldown days = 90 }
   set_variable = { name = aor1776_hre_request_holder value = scope:target_country days = 90 }
  }
  if = {
   limit = { scope:target_country = { aor1776_hre_member = yes } NOT = { owes_obligation_to = scope:target_country } }
   aor1776_hre_return_requested_provinces = yes
  }
  else = { scope:target_country = { trigger_event = { id = aor1776_hre.20 popup = yes } } }
 }
 ai = {
  evaluation_chance = { value = 0.2 }
  will_propose = { aor1776_hre_emperor = yes }
  will_select_as_second_state = { aor1776_hre_restitution_state = yes NOT = { aor1776_hre_restitution_cooldown = yes } }
  propose_score = { value = 100 }
 }
''')
 action_nodes=cw.parse(action)
 accept=action_nodes[0].children('accept_effect')[0]
 accept_body=action[accept.start:accept.end]
 inside=accept_body[accept_body.index('{')+1:accept_body.rindex('}')]
 action=edits(action,[(accept.start,accept.end,'accept_effect = { custom_tooltip = aor1776_hre_request_effect_tt\n hidden_effect = { '+inside+' }\n}')])
 release_action=block('aor1776_hre_request_subject_release','''
 groups = { general power_bloc }
 requires_approval = no
 should_notify_third_parties = yes
 show_effect_in_tooltip = yes
 selectable = { aor1776_hre_emperor = yes }
 potential = { scope:target_country = { aor1776_hre_external_imperial_overlord = yes } }
 possible = {
  is_diplomatic_play_committed_participant = no
  NOT = { has_war_with = scope:target_country }
  scope:target_country = { is_diplomatic_play_committed_participant = no NOT = { has_variable = aor1776_hre_release_wait } }
 }
 accept_effect = {
  custom_tooltip = aor1776_hre_release_request_tt
  hidden_effect = {
   save_scope_as = hre_request_emperor
   scope:target_country = {
    set_variable = { name = aor1776_hre_release_wait days = 90 }
    trigger_event = { id = aor1776_hre.21 popup = yes }
   }
  }
 }
 ai = { evaluation_chance = { value = 0.2 } will_propose = { aor1776_hre_emperor = yes } propose_score = { value = 100 } }
''')
 files['common/diplomatic_actions/1776_imperial_actions.txt']=pact+action+release_action
 score=block('aor1776_hre_vote_preference','''
 value = 20
 add = { value = "relations(scope:hre_voter)" multiply = 0.3 }
 add = { value = prestige min = 0 max = 200 multiply = 0.05 }
 if = { limit = { this = global_var:aor1776_hre_emperor_country } add = 20 }
 if = { limit = { c:AUS ?= this } add = 15 }
 if = { limit = { this = scope:hre_voter } add = 10 }
 if = { limit = { has_war_with = scope:hre_voter } add = -200 }
 if = { limit = { has_diplomatic_pact = { who = scope:hre_voter type = rivalry } } add = -50 }
 if = { limit = { any_scope_treaty = { binds = scope:hre_voter any_scope_article = { has_type = alliance } } } add = 20 }
 if = { limit = { any_scope_treaty = { binds = scope:hre_voter any_scope_article = { has_type = defensive_pact } } } add = 10 }
 if = { limit = { has_variable = aor1776_hre_wittelsbach scope:hre_voter = { has_variable = aor1776_hre_wittelsbach } } add = 25 }
 if = { limit = { ruler ?= { religion = rel:catholic } scope:hre_voter = { ruler ?= { religion = rel:catholic } } } add = 15 }
 if = { limit = { NOT = { ruler ?= { religion = rel:catholic } } scope:hre_voter = { has_variable = aor1776_hre_spiritual_elector } } add = -25 }
 if = { limit = { has_variable = aor1776_hre_guarantees_privileges } add = 10 }
''')
 files['common/script_values/1776_imperial_elections.txt']=score
 effects=block('aor1776_hre_initialize','''
 if = {
  limit = { NOT = { has_global_variable = aor1776_hre_initialized } exists = c:AUS }
  set_global_variable = aor1776_hre_initialized
  set_global_variable = { name = aor1776_hre_emperor_country value = c:AUS }
  c:AUS = { every_scope_character = { limit = { has_variable = aor1776_hre_emperor_character } set_global_variable = { name = aor1776_hre_emperor_person value = this } } }
  every_country = { limit = { aor1776_hre_member = yes } set_variable = aor1776_hre_guarantees_privileges }
  c:BAV ?= { set_variable = aor1776_hre_wittelsbach }
  c:KPF ?= { set_variable = aor1776_hre_wittelsbach }
'''+''.join(scoped(t,'set_variable = aor1776_hre_catholic_court') for t in ['AUS','BAV','KPF','SAX','KMZ','KTR','KCL'])+''.join(scoped(t,'set_variable = aor1776_hre_spiritual_elector') for t in ['KMZ','KTR','KCL'])+'''
  aor1776_hre_refresh_pacts = yes
 }
''')
 effects+=block('aor1776_hre_refresh_pacts','''
 if = { limit = { exists = global_var:aor1776_hre_emperor_country }
  every_country = {
   limit = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } NOT = { has_diplomatic_pact = { who = global_var:aor1776_hre_emperor_country type = aor1776_imperial_obligation } } }
   create_diplomatic_pact = { country = global_var:aor1776_hre_emperor_country type = aor1776_imperial_obligation }
  }
 }
''')
 effects+=block('aor1776_hre_return_requested_provinces','\n'.join(returns)+'''
 scope:hre_request_state ?= {
  remove_variable = aor1776_hre_refusal_holder
  remove_variable = aor1776_hre_refusal_office
 }
''')
 penalties=[]
 for sid in sorted(bystate):
  penalties.append(f'if = {{ limit = {{ scope:hre_request_state = {{ state_region = s:{sid} }} NOT = {{ has_variable = aor1776_hre_refusal_penalty_{sid} }} }} change_infamy = 5 set_variable = {{ name = aor1776_hre_refusal_penalty_{sid} days = 3650 }} }}')
 effects+=block('aor1776_hre_record_external_refusal','\n'.join(penalties)+'''
 scope:hre_request_state = {
  set_variable = { name = aor1776_hre_refusal_holder value = root days = 3650 }
  set_variable = { name = aor1776_hre_refusal_office days = 3650 }
  set_variable = { name = aor1776_hre_restitution_cooldown days = 3650 }
  set_variable = { name = aor1776_hre_request_holder value = root days = 3650 }
 }
''')
 # Freeze eligible subjects before modifying any dependency. Independence is
 # explicit, not transfer_subject: no country becomes the Emperor's subject.
 effects+=block('aor1776_hre_release_imperial_subjects','''
 every_country = { remove_variable = aor1776_hre_release_selected }
 every_subject_or_below = { limit = { aor1776_hre_member = yes } set_variable = aor1776_hre_release_selected }
 every_country = { limit = { has_variable = aor1776_hre_release_selected } make_independent = yes }
 every_country = {
  limit = { has_variable = aor1776_hre_release_selected }
  save_scope_as = hre_holder
  aor1776_hre_return_released_subject_provinces = yes
  if = { limit = { NOT = { is_in_same_power_bloc = global_var:aor1776_hre_emperor_country } global_var:aor1776_hre_emperor_country = { is_power_bloc_leader = yes power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } } }
   join_power_bloc = global_var:aor1776_hre_emperor_country
  }
  if = { limit = { NOT = { is_in_same_power_bloc = global_var:aor1776_hre_emperor_country } } set_variable = aor1776_hre_release_bloc_pending }
  else = { remove_variable = aor1776_hre_release_bloc_pending }
 }
 every_country = { remove_variable = aor1776_hre_release_selected }
 remove_variable = aor1776_hre_release_refused
 remove_variable = aor1776_hre_release_wait
 aor1776_hre_refresh_pacts = yes
''')
 # Same exact frozen RGB rights as territorial restitution, but scan every
 # region of each released holder, not only a state selected in the UI.
 effects+=block('aor1776_hre_return_released_subject_provinces','\n'.join(
  f'if = {{ limit = {{ exists = c:{r["beneficiary"]} c:{r["beneficiary"]} = {{ aor1776_hre_member = yes }} p:{r["rgb"]}.state = {{ owner = scope:hre_holder }} NOT = {{ c:{r["beneficiary"]} = scope:hre_holder }} }} s:{r["state"]} = {{ set_owner_of_provinces = {{ country = c:{r["beneficiary"]} provinces = {{ {r["rgb"]} }} }} }} }}' for r in ledger))
 effects+=block('aor1776_hre_record_release_refusal','''
 if = { limit = { NOT = { has_variable = aor1776_hre_release_penalty } }
  change_infamy = 5
  set_variable = { name = aor1776_hre_release_penalty days = 3650 }
 }
 set_variable = { name = aor1776_hre_release_refused days = 3650 }
 set_variable = { name = aor1776_hre_release_wait days = 3650 }
''')
 effects+=block('aor1776_hre_open_election','''
 if = { limit = { NOT = { has_global_variable = aor1776_hre_election_open } }
  set_global_variable = aor1776_hre_election_open
  remove_global_variable = aor1776_hre_runoff
  aor1776_hre_start_ballot = yes
 }
''')
 effects+=block('aor1776_hre_start_ballot','''
 set_global_variable = { name = aor1776_hre_elector_count value = 0 }
 set_global_variable = { name = aor1776_hre_ballots_cast value = 0 }
 every_country = { limit = { aor1776_hre_member = yes } set_variable = { name = aor1776_hre_votes value = 0 } remove_variable = aor1776_hre_voted remove_variable = aor1776_hre_voted_for remove_variable = aor1776_hre_voter_this_round }
 every_country = { limit = { aor1776_hre_elector = yes } set_variable = aor1776_hre_voter_this_round set_variable = { name = aor1776_hre_vote_deadline days = 90 } change_global_variable = { name = aor1776_hre_elector_count add = 1 } }
 every_country = {
  limit = { has_variable = aor1776_hre_voter_this_round }
  if = { limit = { is_ai = yes } aor1776_hre_ai_ballot = yes }
  else = { trigger_event = { id = aor1776_hre.1 popup = yes } }
 }
 aor1776_hre_tally_ballot = yes
''')
 effects+=block('aor1776_hre_ai_ballot','''
 save_scope_as = hre_voter
 ordered_country = {
  limit = { aor1776_hre_ballot_candidate = yes }
  order_by = aor1776_hre_vote_preference
  position = 0
  check_range_bounds = no
  save_scope_as = hre_vote_choice
 }
 if = { limit = { exists = scope:hre_vote_choice } aor1776_hre_cast_vote = yes }
''')
 effects+=block('aor1776_hre_cast_vote','''
 if = { limit = { has_global_variable = aor1776_hre_election_open has_variable = aor1776_hre_voter_this_round NOT = { has_variable = aor1776_hre_voted } exists = scope:hre_vote_choice scope:hre_vote_choice = { aor1776_hre_ballot_candidate = yes } }
  set_variable = aor1776_hre_voted
  set_variable = { name = aor1776_hre_voted_for value = scope:hre_vote_choice }
  scope:hre_vote_choice = { change_variable = { name = aor1776_hre_votes add = 1 } }
  change_global_variable = { name = aor1776_hre_ballots_cast add = 1 }
 }
''')
 effects+=block('aor1776_hre_recount_ballot','''
 set_global_variable = { name = aor1776_hre_elector_count value = 0 }
 set_global_variable = { name = aor1776_hre_ballots_cast value = 0 }
 every_country = { limit = { aor1776_hre_member = yes } set_variable = { name = aor1776_hre_votes value = 0 } }
 every_country = { limit = { has_variable = aor1776_hre_voter_this_round aor1776_hre_elector = yes }
  change_global_variable = { name = aor1776_hre_elector_count add = 1 }
  if = { limit = { has_variable = aor1776_hre_voted exists = var:aor1776_hre_voted_for var:aor1776_hre_voted_for = { aor1776_hre_ballot_candidate = yes } }
   change_global_variable = { name = aor1776_hre_ballots_cast add = 1 }
   var:aor1776_hre_voted_for = { change_variable = { name = aor1776_hre_votes add = 1 } }
  }
  else = { remove_variable = aor1776_hre_voted }
 }
''')
 effects+=block('aor1776_hre_tally_ballot','''
 if = { limit = { has_global_variable = aor1776_hre_election_open } aor1776_hre_recount_ballot = yes }
 if = { limit = { has_global_variable = aor1776_hre_election_open global_var:aor1776_hre_elector_count > 0 global_var:aor1776_hre_ballots_cast >= global_var:aor1776_hre_elector_count }
  ordered_country = { limit = { aor1776_hre_ballot_candidate = yes } order_by = var:aor1776_hre_votes position = 0 check_range_bounds = no save_scope_as = hre_elected_country }
  if = { limit = { exists = scope:hre_elected_country }
   scope:hre_elected_country = { set_variable = { name = aor1776_hre_twice_votes value = var:aor1776_hre_votes } change_variable = { name = aor1776_hre_twice_votes multiply = 2 } }
   if = { limit = { scope:hre_elected_country = { var:aor1776_hre_twice_votes > global_var:aor1776_hre_elector_count } }
    scope:hre_elected_country = { aor1776_hre_install_elected_country = yes }
   }
   else_if = { limit = { NOT = { has_global_variable = aor1776_hre_runoff } }
    every_country = { limit = { aor1776_hre_member = yes } remove_variable = aor1776_hre_finalist }
    ordered_country = { limit = { aor1776_hre_candidate = yes } order_by = var:aor1776_hre_votes position = 0 check_range_bounds = no set_variable = aor1776_hre_finalist }
    ordered_country = { limit = { aor1776_hre_candidate = yes } order_by = var:aor1776_hre_votes position = 1 check_range_bounds = no set_variable = aor1776_hre_finalist }
    set_global_variable = aor1776_hre_runoff
    aor1776_hre_start_ballot = yes
   }
   else = { set_global_variable = aor1776_hre_election_deadlocked } # Never install a mere plurality or break a tie silently.
  }
 }
''')
 snapshots=[];restore=[];clear=[]
 for key,levels in groups:
  for i,level in enumerate(reversed(levels)):
   flag='aor1776_hre_saved_'+level
   snapshots.append(('if' if i==0 else 'else_if')+' = { limit = { has_principle = principle:'+level+' } scope:hre_elected_country = { set_variable = '+flag+' } }')
   restore.append('if = { limit = { scope:hre_elected_country = { has_variable = '+flag+' } } add_principle = '+level+' }')
   clear.append('remove_variable = '+flag)
 effects+=block('aor1776_hre_snapshot_principles','\n'.join(snapshots))
 effects+=block('aor1776_hre_restore_principles','\n'.join(restore))
 effects+=block('aor1776_hre_install_elected_country','''
 save_scope_as = hre_elected_country
 global_var:aor1776_hre_emperor_country = { save_scope_as = hre_old_imperial_country }
 # SAME NATIVE LEADER: absolutely no create, leave, join or principle changes.
 if = { limit = { is_power_bloc_leader = yes power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } }
  aor1776_hre_finish_investiture = yes
 }
 else = {
'''+ '\n'.join(clear)+'''
  scope:hre_old_imperial_country.power_bloc ?= {
   aor1776_hre_snapshot_principles = yes
   every_power_bloc_member = { set_variable = aor1776_hre_transfer_member }
  }
  set_variable = aor1776_hre_creation_permitted
  # No unverified leave/destroy effect and no destructive preamble. Native
  # create/join behavior for a founder already in a bloc requires engine testing.
  create_power_bloc = {
   name = HOLY_ROMAN_PB map_color = { 219 211 157 } founding_date = 962.6.9
   identity = identity_aor1776_imperial_federation
  }
  if = { limit = { is_power_bloc_leader = yes power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } }
   power_bloc = { aor1776_hre_restore_principles = yes }
   every_country = { limit = { has_variable = aor1776_hre_transfer_member NOT = { this = scope:hre_elected_country } } join_power_bloc = scope:hre_elected_country }
   every_country = { limit = { has_diplomatic_pact = { who = scope:hre_old_imperial_country type = aor1776_imperial_obligation } } remove_diplomatic_pact = { country = scope:hre_old_imperial_country type = aor1776_imperial_obligation } }
   aor1776_hre_finish_investiture = yes
  }
  else = { set_global_variable = aor1776_hre_native_transfer_blocked } # Keep old bloc and election ledger; do not fake success.
  remove_variable = aor1776_hre_creation_permitted
  every_country = { remove_variable = aor1776_hre_transfer_member }
 }
''')
 effects+=block('aor1776_hre_finish_investiture','''
 if = { limit = { ruler ?= { is_character_alive = yes is_female = no age >= 18 NOT = { has_variable = aor1776_hre_deceased_emperor } } }
  ruler = { set_variable = aor1776_hre_emperor_character set_global_variable = { name = aor1776_hre_emperor_person value = this } }
 }
 else = { heir ?= { set_variable = aor1776_hre_emperor_character set_global_variable = { name = aor1776_hre_emperor_person value = this } } }
 if = { limit = { NOT = { this = global_var:aor1776_hre_emperor_country } }
  every_country = { limit = { has_diplomatic_pact = { who = global_var:aor1776_hre_emperor_country type = aor1776_imperial_obligation } } remove_diplomatic_pact = { country = global_var:aor1776_hre_emperor_country type = aor1776_imperial_obligation } }
 }
 set_global_variable = { name = aor1776_hre_emperor_country value = this }
 remove_global_variable = aor1776_hre_election_open
 remove_global_variable = aor1776_hre_election_deadlocked
 remove_global_variable = aor1776_hre_native_transfer_blocked
 remove_global_variable = aor1776_hre_runoff
 every_country = { remove_variable = aor1776_hre_finalist remove_variable = aor1776_hre_voter_this_round remove_variable = aor1776_hre_voted remove_variable = aor1776_hre_voted_for remove_variable = aor1776_hre_vote_deadline }
 remove_global_variable = aor1776_hre_election_pending
 aor1776_hre_refresh_pacts = yes
''')
 effects+=block('aor1776_hre_defend_external_attack','''
 if = { limit = { NOT = { has_variable = aor1776_hre_adjusting_backers } exists = global_var:aor1776_hre_emperor_country exists = scope:initiator exists = scope:target }
  set_variable = aor1776_hre_adjusting_backers
  if = { limit = { scope:target = { aor1776_hre_member = yes } scope:initiator = { aor1776_hre_member = no } NOT = { scope:target = global_var:aor1776_hre_emperor_country } }
   add_target_backers = { global_var:aor1776_hre_emperor_country }
  }
  else_if = { limit = { scope:target = { aor1776_hre_member = yes } scope:initiator = { aor1776_hre_member = yes } NOT = { scope:target = global_var:aor1776_hre_emperor_country } NOT = { scope:initiator = global_var:aor1776_hre_emperor_country } }
   remove_initiator_backers = { global_var:aor1776_hre_emperor_country }
   remove_target_backers = { global_var:aor1776_hre_emperor_country }
  }
  if = { limit = { OR = { is_diplomatic_play_type = dp_aor1776_hre_restitution is_diplomatic_play_type = dp_aor1776_hre_subject_release } scope:initiator = { aor1776_hre_emperor = yes } scope:target = { aor1776_hre_member = no } }
   every_country = { limit = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } } save_scope_as = hre_backer root = { add_initiator_backers = { scope:hre_backer } } }
  }
  remove_variable = aor1776_hre_adjusting_backers
 }
''')
 files['common/scripted_effects/1776_imperial_constitution.txt']=effects
 onactions='''
 on_game_started_after_lobby = { on_actions = { aor1776_hre_initialize_hook } }
 on_character_death = { on_actions = { aor1776_hre_death_hook } }
 on_monthly_pulse = { on_actions = { aor1776_hre_monthly_hook } }
 on_diplomatic_play_started = { on_actions = { aor1776_hre_defense_hook } }
 on_diplo_play_join_side = { on_actions = { aor1776_hre_defense_hook } }
 on_diplo_play_war_start = { on_actions = { aor1776_hre_defense_hook } }
 on_wargoal_enforced = { on_actions = { aor1776_hre_native_exit_hook } }
 aor1776_hre_initialize_hook = { effect = { aor1776_hre_initialize = yes } }
 aor1776_hre_death_hook = {
  effect = { if = { limit = { has_variable = aor1776_hre_emperor_character this = global_var:aor1776_hre_emperor_person }
   set_variable = aor1776_hre_deceased_emperor
   set_global_variable = aor1776_hre_election_pending
   global_var:aor1776_hre_emperor_country = { trigger_event = { id = aor1776_hre.2 days = 1 popup = no } }
  } }
 }
 aor1776_hre_monthly_hook = {
  effect = {
   aor1776_hre_refresh_pacts = yes
   if = { limit = { exists = global_var:aor1776_hre_emperor_country global_var:aor1776_hre_emperor_country = { is_power_bloc_leader = yes power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } } }
    every_country = { limit = { aor1776_hre_member = yes is_subject = no has_variable = aor1776_hre_release_bloc_pending }
     if = { limit = { NOT = { is_in_same_power_bloc = global_var:aor1776_hre_emperor_country } } join_power_bloc = global_var:aor1776_hre_emperor_country }
     if = { limit = { is_in_same_power_bloc = global_var:aor1776_hre_emperor_country } remove_variable = aor1776_hre_release_bloc_pending }
    }
   }
   if = { limit = { has_global_variable = aor1776_hre_election_open NOT = { has_global_variable = aor1776_hre_native_transfer_blocked } NOT = { has_global_variable = aor1776_hre_election_deadlocked } }
    aor1776_hre_recount_ballot = yes
    every_country = { limit = { has_variable = aor1776_hre_voter_this_round aor1776_hre_elector = yes NOT = { has_variable = aor1776_hre_voted } OR = { is_ai = yes NOT = { has_variable = aor1776_hre_vote_deadline } } } aor1776_hre_ai_ballot = yes }
    aor1776_hre_tally_ballot = yes
   }
   if = { limit = { has_global_variable = aor1776_hre_election_deadlocked NOT = { has_global_variable = aor1776_hre_native_transfer_blocked } }
    remove_global_variable = aor1776_hre_election_deadlocked aor1776_hre_start_ballot = yes
   }
   if = { limit = { exists = global_var:aor1776_hre_emperor_country NOT = { has_global_variable = aor1776_hre_election_open } NOT = { has_global_variable = aor1776_hre_election_pending } }
    global_var:aor1776_hre_emperor_country = {
     if = { limit = { NOT = { is_power_bloc_leader = yes } } aor1776_hre_install_elected_country = yes }
    }
   }
  }
 }
 aor1776_hre_defense_hook = { effect = { aor1776_hre_defend_external_attack = yes } }
 aor1776_hre_native_exit_hook = { effect = {
  if = { limit = { aor1776_hre_member = yes scope:target ?= { aor1776_hre_emperor = yes } scope:diplomatic_play ?= { is_diplomatic_play_type = dp_leave_power_bloc } }
   set_variable = aor1776_hre_seceded
   remove_diplomatic_pact = { country = scope:target type = aor1776_imperial_obligation }
  }
 } }
'''
 files['common/on_actions/1776_imperial_constitution.txt']=onactions
 wargoal=block('aor1776_hre_restitution','''
 icon = "gfx/interface/icons/war_goals/aor1776_hre_restitution.dds"
 kind = custom
 settings = { require_target_be_part_of_war validate_conflicts_conquer_state }
 execution_priority = 70
 contestion_type = control_target_state
 target_type = state
 possible = {
  aor1776_hre_emperor = yes
  scope:target_country = { aor1776_hre_member = no }
  scope:target_state = { owner = scope:target_country has_variable = aor1776_hre_refusal_holder var:aor1776_hre_refusal_holder = scope:target_country aor1776_hre_restitution_state = yes }
 }
 valid = {
  aor1776_hre_emperor = yes
  scope:target_country = { aor1776_hre_member = no }
  scope:target_state = { owner = scope:target_country has_variable = aor1776_hre_refusal_holder var:aor1776_hre_refusal_holder = scope:target_country aor1776_hre_restitution_state = yes }
 }
 maneuvers = { value = 10 }
 infamy = { value = 0 }
 on_enforced = {
  scope:target_state = { save_scope_as = hre_request_state }
  scope:target_country = { save_scope_as = hre_holder }
  aor1776_hre_return_requested_provinces = yes
 }
 ai = { is_significant_demand = yes }
''')
 secession=(GAME/'common/war_goal_types/12_leave_power_bloc.txt').read_text(encoding='utf-8-sig').replace('leave_power_bloc = {','aor1776_hre_secession = {',1)
 start=secession.index('on_enforced = {');end=secession.index('\n\tai =',start)
 secession=secession[:start]+'''on_enforced = {
 set_variable = aor1776_hre_seceded
 remove_diplomatic_pact = { country = scope:target_country type = aor1776_imperial_obligation }
}\n'''+secession[end:]
 release_goal=block('aor1776_hre_subject_release','''
 icon = "gfx/interface/icons/war_goals/aor1776_hre_subject_release.dds"
 kind = custom
 settings = { require_target_be_part_of_war }
 execution_priority = 70
 contestion_type = control_half_target_country_states
 target_type = country
 possible = { aor1776_hre_emperor = yes scope:target_country = { aor1776_hre_external_imperial_overlord = yes has_variable = aor1776_hre_release_refused } }
 valid = { aor1776_hre_emperor = yes scope:target_country = { aor1776_hre_external_imperial_overlord = yes has_variable = aor1776_hre_release_refused } }
 maneuvers = { value = 20 }
 infamy = { value = 0 }
 on_enforced = { scope:target_country = { aor1776_hre_release_imperial_subjects = yes } }
 ai = { is_significant_demand = yes }
''')
 files['common/war_goal_types/1776_imperial_war_goals.txt']=wargoal+secession+release_goal
 plays=block('dp_aor1776_hre_restitution','''
 requires_interest_marker = no
 war_goal = aor1776_hre_restitution
 texture = "gfx/interface/icons/war_goals/aor1776_hre_restitution.dds"
 initiator_can_add_war_goals = no
 target_can_add_war_goals = yes
 selectable_in_lens = { aor1776_hre_emperor = yes }
 possible = { aor1776_hre_emperor = yes scope:target_country = { aor1776_hre_member = no } diplomatic_play_has_no_relations_blockers = yes }
''')+block('dp_aor1776_hre_secession','''
 requires_interest_marker = no
 war_goal = aor1776_hre_secession
 texture = "gfx/interface/icons/war_goals/leave_power_bloc.dds"
 initiator_can_add_war_goals = no
 target_can_add_war_goals = no
 selectable_in_lens = { aor1776_hre_member = yes aor1776_hre_emperor = no is_subject = no }
 possible = { aor1776_hre_member = yes aor1776_hre_emperor = no is_subject = no scope:target_country = { aor1776_hre_emperor = yes } diplomatic_play_has_no_relations_blockers = yes }
''')
 plays+=block('dp_aor1776_hre_subject_release','''
 requires_interest_marker = no
 war_goal = aor1776_hre_subject_release
 texture = "gfx/interface/icons/war_goals/aor1776_hre_subject_release.dds"
 initiator_can_add_war_goals = no
 target_can_add_war_goals = yes
 selectable_in_lens = { aor1776_hre_emperor = yes }
 possible = { aor1776_hre_emperor = yes scope:target_country = { aor1776_hre_external_imperial_overlord = yes has_variable = aor1776_hre_release_refused } diplomatic_play_has_no_relations_blockers = yes }
''')
 files['common/diplomatic_plays/1776_imperial_plays.txt']=plays
 events='namespace = aor1776_hre\n'+block('aor1776_hre.1','''
 type = country_event
 placement = root
 title = aor1776_hre.1.t
 desc = aor1776_hre.1.d
 flavor = aor1776_hre.1.f
 event_image = { video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }
 trigger = { has_global_variable = aor1776_hre_election_open has_variable = aor1776_hre_voter_this_round NOT = { has_variable = aor1776_hre_voted } }
 cancellation_trigger = { OR = { NOT = { has_global_variable = aor1776_hre_election_open } has_variable = aor1776_hre_voted } }
'''+''.join(block('option',f'name = aor1776_hre.vote_{t}\ntrigger = {{ c:{t} ?= {{ aor1776_hre_ballot_candidate = yes }} }}\nc:{t} = {{ save_scope_as = hre_vote_choice }}\naor1776_hre_cast_vote = yes\naor1776_hre_tally_ballot = yes\nai_chance = {{ base = 0 }}') for t in MEMBERS)+'''
''')
 events+=block('aor1776_hre.2','type = country_event\nhidden = yes\nimmediate = { aor1776_hre_open_election = yes }\n')
 events+=block('aor1776_hre.20','''
 type = country_event
 placement = scope:hre_request_state
 title = aor1776_hre.20.t
 desc = aor1776_hre.20.d
 flavor = aor1776_hre.20.f
 event_image = { video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }
 trigger = { exists = scope:hre_request_state exists = scope:hre_request_emperor scope:hre_request_emperor = { aor1776_hre_emperor = yes } scope:hre_request_state = { owner = root aor1776_hre_restitution_state = yes } }
 cancellation_trigger = { OR = { NOT = { exists = scope:hre_request_state } NOT = { scope:hre_request_emperor = { aor1776_hre_emperor = yes } } NOT = { scope:hre_request_state = { owner = root aor1776_hre_restitution_state = yes } } } }
 option = {
  name = aor1776_hre.20.a default_option = yes
  save_scope_as = hre_holder
  custom_tooltip = aor1776_hre_return_effect_tt
  hidden_effect = { aor1776_hre_return_requested_provinces = yes }
  ai_chance = { base = 60 modifier = { trigger = { aor1776_hre_member = yes } add = 35 } }
 }
 option = {
  name = aor1776_hre.20.b
  trigger = { OR = { aor1776_hre_member = no scope:hre_request_emperor = { owes_obligation_to = root } } }
  custom_tooltip = aor1776_hre_refusal_effect_tt
  if = { limit = { aor1776_hre_member = no }
   hidden_effect = { aor1776_hre_record_external_refusal = yes }
  }
  ai_chance = { base = 40 modifier = { trigger = { aor1776_hre_member = yes } add = -35 } }
 }
''')
 events+=block('aor1776_hre.21','''
 type = country_event
 placement = root
 title = aor1776_hre.21.t
 desc = aor1776_hre.21.d
 flavor = aor1776_hre.21.f
 event_image = { video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }
 trigger = { aor1776_hre_external_imperial_overlord = yes exists = scope:hre_request_emperor scope:hre_request_emperor = { aor1776_hre_emperor = yes } }
 cancellation_trigger = { OR = { aor1776_hre_external_imperial_overlord = no NOT = { scope:hre_request_emperor ?= { aor1776_hre_emperor = yes } } } }
 option = {
  name = aor1776_hre.21.a default_option = yes
  custom_tooltip = aor1776_hre_release_effect_tt
  hidden_effect = { aor1776_hre_release_imperial_subjects = yes }
  ai_chance = { base = 60 }
 }
 option = {
  name = aor1776_hre.21.b
  custom_tooltip = aor1776_hre_release_refusal_tt
  hidden_effect = { aor1776_hre_record_release_refusal = yes }
  ai_chance = { base = 40 }
 }
''')
 files['events/1776_imperial_constitution_events.txt']=events
 # Native heraldic rendering, not generated bitmap flags.
 flags='';coas=''
 symbols={'KPF':('black','yellow','ce_lion_rampant_crowned.dds'),'KMZ':('red','white','ce_cross_wheel.dds'),'KTR':('white','red','ce_cross_couped.dds'),'KCL':('white','black','ce_cross_couped.dds')}
 for t,(bg,fg,texture) in symbols.items():
  flags+=block(t,block('flag_definition',f'coa = AOR1776_{t}\npriority = 100\nallow_overlord_canton = no'))
  coas+=block('AOR1776_'+t,'pattern = "pattern_solid.tga"\ncolor1 = '+bg+'\n'+block('colored_emblem','texture = "'+texture+'"\ncolor1 = '+fg+'\ninstance = { position = { 0.5 0.5 } scale = { 0.75 0.75 } }'))
 files['common/flag_definitions/1776_imperial_electoral_flags.txt']=flags
 files['common/coat_of_arms/coat_of_arms/1776_imperial_electoral_flags.txt']=coas
 locs={
 'aor1776_hre_request_effect_tt':('Demand the return of the selected registered imperial provinces. A member must obey unless the Emperor owes it an obligation. An external holder may refuse; the first refusal for that country and region causes 5 infamy and grants an imperial restitution casus belli for ten years. Normal truces still apply.','Demander la restitution des provinces impériales enregistrées et sélectionnées. Un membre doit obéir, sauf si l’empereur lui doit une obligation. Un détenteur extérieur peut refuser : le premier refus pour ce pays et cette région entraîne 5 points d’infamie et un casus belli de rétrocession impériale valable dix ans. Les trêves ordinaires restent applicables.'),
 'aor1776_hre_return_effect_tt':('Return only the registered provinces wrongfully held in this state to their surviving imperial holders. No territory is annexed by the Emperor unless it was already registered as belonging to his country.','Rendre uniquement les provinces détenues indûment dans cet État à leurs titulaires impériaux encore existants. L’empereur n’annexe aucun territoire, sauf celui déjà enregistré comme appartenant à son pays.'),
 'aor1776_hre_refusal_effect_tt':('An imperial member protected by an obligation may refuse without infamy or a restitution casus belli. An external holder incurs 5 infamy on its first refusal for this region within ten years and grants the Emperor the restitution casus belli.','Un membre impérial protégé par une obligation peut refuser sans infamie ni casus belli de rétrocession. Un détenteur extérieur reçoit 5 points d’infamie lors de son premier refus pour cette région sur dix ans et ouvre le casus belli de rétrocession à l’empereur.'),
 'identity_aor1776_imperial_federation':('Holy Roman Empire','Saint-Empire romain germanique'),
 'identity_aor1776_imperial_federation_desc':('An elective imperial constitution: a common market, autonomous estates and a locked imperial bond without tribute.','Une constitution impériale élective : marché commun, États autonomes et lien impérial verrouillé sans tribut.'),
 'aor1776_imperial_obligation':('Imperial bond','Lien impérial'),
 'aor1776_imperial_obligation_desc':('An imperial obligation without tribute or native overlordship.','Une obligation impériale sans tribut ni suzeraineté native.'),
 'aor1776_hre_request_restitution':('Demand imperial restitution','Exiger une rétrocession impériale'),
 'aor1776_hre_request_restitution_desc':('Return the selected territory to its registered 1776 imperial holders. Imperial members must comply unless the Emperor owes them an obligation. An external refusal costs 5 infamy and authorises a restitution play for ten years, respecting normal truces. The penalty cannot be repeated against the same country for the same region during that period.','Restitue le territoire sélectionné à ses titulaires impériaux enregistrés en 1776. Les membres doivent accepter, sauf si l’empereur leur doit une obligation. Un refus extérieur coûte 5 points d’infamie et autorise une manœuvre de rétrocession pendant dix ans, dans le respect des trêves normales. La sanction ne peut être répétée contre le même pays pour la même région pendant cette période.'),
 'aor1776_hre_restitution':('Imperial restitution','Rétrocession impériale'),
 'dp_aor1776_hre_restitution':('Imperial restitution','Rétrocession impériale'),
 'dp_aor1776_hre_restitution_tooltip':('Restore the registered imperial provinces, not annex the entire state. Imperial estates support their Emperor.','Restaurer les provinces impériales enregistrées, sans annexer tout l’État. Les États impériaux soutiennent leur empereur.'),
 'aor1776_hre_secession':('Secession from the Empire','Sécession de l’Empire'),
 'dp_aor1776_hre_secession':('Imperial secession','Sécession impériale'),
 'aor1776_hre.1.t':('The empty throne','Le trône vacant'),
 'aor1776_hre.1.d':('The imperial crown has lost its bearer. The recognised electoral crowns must choose a successor. A majority of the active votes is required; if none prevails, the two leading candidates face a second ballot. After three months without instructions, our envoys will cast a vote according to our interests.','La couronne impériale a perdu son titulaire. Les couronnes électorales reconnues doivent désigner un successeur. La majorité des voix actives est nécessaire ; à défaut, les deux premiers candidats s’affrontent au second tour. Après trois mois sans instruction, nos envoyés voteront selon nos intérêts.'),
 'aor1776_hre.1.f':('The sealed letters lay before the envoys, each bearing a promise, a grievance or the memory of an old allegiance.','Les lettres scellées reposaient devant les envoyés, chacune portant une promesse, un grief ou le souvenir d’une ancienne fidélité.'),
 'aor1776_hre.20.t':('The imperial demand','La sommation impériale'),
 'aor1776_hre.20.d':('The Emperor demands that the provinces of [SCOPE.sState(\'hre_request_state\').GetName] be restored to their registered imperial holders. Compliance restores the recognised boundaries; it does not enrich the imperial domain.','L’empereur exige que les provinces de [SCOPE.sState(\'hre_request_state\').GetName] soient rendues à leurs titulaires impériaux reconnus. Obtempérer rétablit leurs frontières ; cela n’enrichit pas le domaine impérial.'),
 'aor1776_hre.20.f':('The envoy laid the imperial seal upon the table. Beyond the window, the sentries kept their eyes upon the road.','L’envoyé posa le sceau impérial sur la table. Au-delà de la fenêtre, les sentinelles gardaient les yeux fixés sur la route.'),
 'aor1776_hre.20.a':('We shall restore what is rightfully theirs.','Nous restituerons ce qui leur revient de droit.'),
 'aor1776_hre.20.b':('We will not yield these lands.','Nous ne céderons pas ces terres.'),
 }
 for t,v in NEW.items():locs[t]=(v[2],v[3]);locs[t+'_ADJ']=(v[2],v[3]);locs[v[4]]=(v[4].replace('_',' '),v[4].replace('_',' '));locs[v[5]]=(v[5].replace('_',' '),v[5].replace('_',' '))
 for t in MEMBERS:locs['aor1776_hre.vote_'+t]=(f"Support [GetCountry('{t}').GetName]",f"Soutenir [GetCountry('{t}').GetName]")
 locs.update({k+'_tt':v for k,v in trigger_labels.items()})
 locs.update({
 'aor1776_hre_request_subject_release':('Demand the release of imperial estates','Exiger la libération des États impériaux'),
 'aor1776_hre_request_subject_release_desc':('Demand that this external power release its recognised imperial subjects and restore their wrongly held registered imperial provinces.','Exiger de cette puissance extérieure la libération de ses sujets impériaux reconnus et la restitution de leurs provinces impériales enregistrées détenues indûment.'),
 'aor1776_hre_release_request_tt':('All recognised imperial estates subject to this external power are covered, including indirect subjects. Other subjects are excluded. Refusal grants the Emperor a ten-year liberation casus belli; normal truces apply.','La demande couvre tous les États impériaux reconnus soumis à cette puissance extérieure, y compris indirectement. Les autres sujets sont exclus. Un refus ouvre un casus belli de libération valable dix ans ; les trêves normales restent applicables.'),
 'aor1776_hre_release_effect_tt':('Release the recognised imperial subjects as independent countries, restore only their wrongly held registered provinces to surviving rightful holders, and reattach them to the imperial bond and bloc. The Emperor does not become their overlord.','Libérer les sujets impériaux reconnus comme pays indépendants, rendre leurs seules provinces enregistrées détenues indûment aux titulaires légitimes encore existants et rétablir leur lien et leur bloc impériaux. L’empereur ne devient pas leur suzerain.'),
 'aor1776_hre_release_refusal_tt':('The first refusal within ten years costs 5 infamy. The Emperor receives a ten-year casus belli to release the imperial estates; all recognised imperial members are called to his side.','Le premier refus sur dix ans coûte 5 points d’infamie. L’empereur reçoit un casus belli valable dix ans pour libérer les États impériaux ; tous les membres impériaux reconnus sont appelés à le soutenir.'),
 'aor1776_hre_subject_release':('Liberation of imperial estates','Libération des États impériaux'),
 'dp_aor1776_hre_subject_release':('Imperial liberation','Libération impériale'),
 'dp_aor1776_hre_subject_release_tooltip':('Release this external power’s imperial subjects and restore their registered boundaries, without annexation by the Emperor.','Libérer les sujets impériaux de cette puissance extérieure et rétablir leurs frontières enregistrées, sans annexion par l’empereur.'),
 'aor1776_hre.21.t':('The Emperor claims his estates','L’empereur réclame ses États'),
 'aor1776_hre.21.d':('An imperial envoy demands the release of the estates of the Empire held beneath our crown. Their registered territorial rights must also be restored. The Emperor invokes the liberty of the estates, not their submission to his own country.','Un envoyé impérial exige la libération des États de l’Empire placés sous notre couronne. Leurs droits territoriaux enregistrés doivent également être rétablis. L’empereur invoque la liberté des États, non leur soumission à son propre pays.'),
 'aor1776_hre.21.f':('The envoy unrolled a parchment crowded with seals. Each belonged to a prince or a city whose allegiance was now disputed.','L’envoyé déroula un parchemin chargé de sceaux. Chacun appartenait à un prince ou à une cité dont l’allégeance était désormais contestée.'),
 'aor1776_hre.21.a':('We shall release these estates and honour their rights.','Nous libérerons ces États et respecterons leurs droits.'),
 'aor1776_hre.21.b':('We will not surrender our authority.','Nous ne renoncerons pas à notre autorité.'),
 })
 for i,lang in enumerate(['english','french']):
  files[f'localization/{lang}/1776_imperial_constitution_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[i].replace('"','\\"')+'"\n' for k,v in locs.items())
 from map2k_imperial_feedback import augment
 files=augment(files,ledger,MEMBERS,ELECTORS)
 from map2k_imperial_principles import augment_principles
 files=augment_principles(files)
 from map2k_imperial_repairs import augment_repairs
 files=augment_repairs(files,ledger,MEMBERS)
 from map2k_imperial_journal import augment_journal
 files=augment_journal(files)
 from map2k_imperial_demand_feedback import augment_demand_feedback
 files=augment_demand_feedback(files)
 from map2k_imperial_atlas_access import augment_atlas_access
 files=augment_atlas_access(files)
 from map2k_imperial_electoral_choices import augment_electoral_choices
 from hre_centralization_01 import augment as augment_centralization
 return augment_centralization(augment_electoral_choices(files,MEMBERS),inv)
if __name__=='__main__':emit(compile_system())
