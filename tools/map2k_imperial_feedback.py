"""Compile the player-feedback revision; never write runtime files directly."""
import re
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits

EF='common/scripted_effects/1776_imperial_constitution.txt'
OA='common/on_actions/1776_imperial_constitution.txt'
DA='common/diplomatic_actions/1776_imperial_actions.txt'
EV='events/1776_imperial_constitution_events.txt'
WG='common/war_goal_types/1776_imperial_war_goals.txt'
DP='common/diplomatic_plays/1776_imperial_plays.txt'
ID='common/power_bloc_identities/1776_imperial_federation.txt'
def block(k,s):return k+' = {\n'+s+'\n}\n'
def append_inside(raw,key,body):
 n=next(n for n in cw.parse(raw) if n.key==key)
 return edits(raw,[(n.end-1,n.end-1,'\n'+body+'\n')])
def replace_node(raw,key,new):
 n=next(n for n in cw.parse(raw) if n.key==key)
 return edits(raw,[(n.start,n.end,new.rstrip())])
def child(raw,key,field,new):
 n=next(n for n in cw.parse(raw) if n.key==key);cs=n.children(field)
 if not cs:return append_inside(raw,key,new)
 return edits(raw,[(cs[0].start,cs[0].end,new)])

def augment(files,ledger,members,electors):
 loc={}
 def L(k,en,fr):loc[k]=(en,fr)
 # Native textures are explicit, not inferred from action identifiers.
 for k in ['aor1776_imperial_obligation','aor1776_hre_request_restitution','aor1776_hre_request_subject_release']:
  files[DA]=append_inside(files[DA],k,'texture = "gfx/interface/icons/diplomatic_action_icons/'+k+'.dds"')
 files[DA]=append_inside(files[DA],'aor1776_imperial_obligation','')
 # auto_support_type is documented as repeatable; support both imperial plays.
 p=next(n for n in cw.parse(files[DA]) if n.key=='aor1776_imperial_obligation').children('pact')[0]
 files[DA]=edits(files[DA],[(p.end-1,p.end-1,'\n auto_support_type = dp_aor1776_hre_subject_release\n')])
 trig='common/scripted_triggers/1776_imperial_constitution.txt'
 files[trig]+=block('aor1776_hre_under_imperial_authority','aor1776_hre_member = yes\nNOT = { top_overlord ?= { aor1776_hre_member = no } }')
 from map2l_registry import additional_free_cities
 cities=list(dict.fromkeys(['LUB','HAM','BRE','FRM']+[t for t in additional_free_cities() if t in members]))
 files[trig]+=block('aor1776_hre_free_city','aor1776_hre_member = yes\nOR = { '+' '.join('c:'+t+' ?= this' for t in cities)+' }')
 L('aor1776_hre_under_imperial_authority_tt','An imperial estate not subject to an external overlord.','Un État impérial non soumis à un suzerain extérieur.')
 L('aor1776_hre_free_city_tt','A recognised imperial free city.','Une ville libre impériale reconnue.')

 # Native acceptance is visible in the native action confirmation. No hidden
 # 60/40 event roll inconsistent with the preview.
 preview='scope:target_country = { aor1776_hre_preview_subjects = yes }'
 files[DA]=child(files[DA],'aor1776_hre_request_subject_release','requires_approval','requires_approval = yes')
 files[DA]=child(files[DA],'aor1776_hre_request_subject_release','accept_effect','''accept_effect = {
 custom_tooltip = aor1776_hre_release_effect_tt
 '''+preview+'''
 hidden_effect = {
  save_scope_as = hre_request_emperor
  scope:target_country = { save_scope_as = hre_reply_holder aor1776_hre_release_imperial_subjects = yes }
  trigger_event = { id = aor1776_hre.30 popup = yes }
 }
}''')
 files[DA]=append_inside(files[DA],'aor1776_hre_request_subject_release','''decline_effect = {
 save_scope_as = hre_request_emperor
 scope:target_country = { save_scope_as = hre_reply_holder aor1776_hre_record_release_refusal = yes }
 trigger_event = { id = aor1776_hre.31 popup = yes }
}''')
 files[DA]=child(files[DA],'aor1776_hre_request_subject_release','ai','''ai = {
 evaluation_chance = { value = 0.2 }
 will_propose = { aor1776_hre_emperor = yes }
 will_propose_even_if_not_accepted = { aor1776_hre_emperor = yes }
 propose_score = { value = 100 }
 accept_score = {
  value = -25
  add = { value = "relations(scope:target)" multiply = 0.5 desc = aor1776_hre_accept_relations }
  add = { value = scope:target.prestige subtract = prestige multiply = 0.2 min = -40 max = 40 desc = aor1776_hre_accept_prestige }
  if = { limit = { owes_obligation_to = scope:target } add = { value = 60 desc = aor1776_hre_accept_obligation } }
 }
}''')
 L('aor1776_hre_accept_relations','Relations with the Emperor','Relations avec l’empereur')
 L('aor1776_hre_accept_prestige','Relative diplomatic weight','Poids diplomatique relatif')
 L('aor1776_hre_accept_obligation','Obligation owed to the Emperor','Obligation due à l’empereur')

 # A real province list, retaining RGB as the precise identifier: generic
 # unnamed provinces must not be presented as invented historical cities.
 state_lines=[]
 for r in ledger:
  rgb,tag,sid=r['rgb'],r['beneficiary'],r['state'];key='aor1776_hre_province_'+rgb
  L(key,f"{rgb} — [SCOPE.sState('hre_preview_state').GetName] → [GetCountry('{tag}').GetName]",f"{rgb} — [SCOPE.sState('hre_preview_state').GetName] → [GetCountry('{tag}').GetName]")
  state_lines.append(f'if = {{ limit = {{ c:{tag} ?= {{ aor1776_hre_member = yes }} p:{rgb}.state ?= this NOT = {{ owner = c:{tag} }} }} save_temporary_scope_as = hre_preview_state custom_tooltip = {key} }}')
 files[EF]+=block('aor1776_hre_preview_provinces','\n'.join(state_lines))
 files[EF]+=block('aor1776_hre_preview_subjects','every_subject_or_below = { limit = { aor1776_hre_member = yes } save_temporary_scope_as = hre_preview_subject custom_tooltip = aor1776_hre_subject_line }')
 # Event-local saved scopes survive emancipation; do not reread the subject
 # iterator after independence or rely on a shared mutable notification list.
 files[EF]+=block('aor1776_hre_snapshot_reply_subjects','every_subject_or_below = { limit = { aor1776_hre_member = yes }\n'+''.join(f'if = {{ limit = {{ c:{t} ?= this }} save_scope_as = hre_reply_subject_{t} }}\n' for t in members)+'}')
 custom='';replytext=''
 L('aor1776_hre_empty','','')
 for t in members:
  custom+=block('aor1776_hre_reply_'+t,f'type = country\ntext = {{ trigger = {{ exists = scope:hre_reply_subject_{t} }} localization_key = aor1776_hre_reply_line_{t} }}\ntext = {{ localization_key = aor1776_hre_empty }}')
  L('aor1776_hre_reply_line_'+t,f"\n• [SCOPE.sCountry('hre_reply_subject_{t}').GetName]",f"\n• [SCOPE.sCountry('hre_reply_subject_{t}').GetName]")
  replytext+=f"[SCOPE.GetRootScope.GetCountry.GetCustom('aor1776_hre_reply_{t}')]"
 files['common/customizable_localization/1776_imperial_reply_lists.txt']=custom
 files[DA]=files[DA].replace('save_scope_as = hre_reply_holder aor1776_hre_release_imperial_subjects','save_scope_as = hre_reply_holder aor1776_hre_snapshot_reply_subjects = yes aor1776_hre_release_imperial_subjects').replace('save_scope_as = hre_reply_holder aor1776_hre_record_release_refusal','save_scope_as = hre_reply_holder aor1776_hre_snapshot_reply_subjects = yes aor1776_hre_record_release_refusal')
 L('aor1776_hre_subject_line',"[SCOPE.sCountry('hre_preview_subject').GetName]", "[SCOPE.sCountry('hre_preview_subject').GetName]")
 # Show the filtered list in normal action previews and in the target event.
 n=next(n for n in cw.parse(files[DA]) if n.key=='aor1776_hre_request_restitution').children('accept_effect')[0]
 raw=files[DA][n.start:n.end].replace('accept_effect = {','accept_effect = {\nscope:second_state = { aor1776_hre_preview_provinces = yes }',1)
 files[DA]=edits(files[DA],[(n.start,n.end,raw)])
 files[DA]=files[DA].replace('aor1776_hre_return_requested_provinces = yes','aor1776_hre_return_requested_provinces = yes\n scope:target_country = { save_scope_as = hre_reply_holder } trigger_event = { id = aor1776_hre.32 popup = yes }')
 for option in ['aor1776_hre.20']:
  e=next(n for n in cw.parse(files[EV]) if n.key==option)
  a=e.children('option')[0]
  files[EV]=edits(files[EV],[(a.end-1,a.end-1,'\n scope:hre_request_state ?= { aor1776_hre_preview_provinces = yes }\n')])
 # Explicit messages go to the Emperor, not only to the responding country.
 for event,opt,num in [('aor1776_hre.20',0,32),('aor1776_hre.20',1,33)]:
  e=next(n for n in cw.parse(files[EV]) if n.key==event);o=e.children('option')[opt]
  files[EV]=edits(files[EV],[(o.end-1,o.end-1,'\n hidden_effect = { save_scope_as = hre_reply_holder scope:hre_request_emperor = { trigger_event = { id = aor1776_hre.'+str(num)+' popup = yes } } }\n')])
 # Also notify responses to requests still pending in an older save.
 for opt,num in [(0,30),(1,31)]:
  e=next(n for n in cw.parse(files[EV]) if n.key=='aor1776_hre.21');o=e.children('option')[opt]
  original=files[EV][o.start:o.end]
  revised=original.replace('option = {','option = {\n hidden_effect = { save_scope_as = hre_reply_holder aor1776_hre_snapshot_reply_subjects = yes }',1)
  revised=revised[:-1]+'\n hidden_effect = { scope:hre_request_emperor = { trigger_event = { id = aor1776_hre.'+str(num)+' popup = yes } } }\n}'
  files[EV]=edits(files[EV],[(o.start,o.end,revised)])
 for num,en,fr in [(30,'The imperial estates are free','Les États impériaux sont libres'),(31,'Our demand has been refused','Notre demande a été refusée'),(32,'The provinces have been restored','Les provinces ont été restituées'),(33,'The imperial summons is rejected','La sommation impériale est rejetée'),(34,'The imperial settlement is enforced','Le règlement impérial est appliqué')]:
  files[EV]+=block('aor1776_hre.'+str(num),f'''type = country_event
 placement = root
 title = aor1776_hre.{num}.t
 desc = aor1776_hre.{num}.d
 event_image = {{ video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }}
 option = {{ name = aor1776_hre.ack default_option = yes }}''')
  L(f'aor1776_hre.{num}.t',en,fr)
  if num in [30,32,34]:
   L(f'aor1776_hre.{num}.d',"[SCOPE.sCountry('hre_reply_holder').GetName] has yielded to the imperial demand. The settlement has been applied. An accepted demand can create a truce without a war; this is not a failed declaration.","[SCOPE.sCountry('hre_reply_holder').GetName] a cédé à la demande impériale. Le règlement a été appliqué. Une demande acceptée peut créer une trêve sans guerre : il ne s’agit pas d’une déclaration ratée.")
  else:L(f'aor1776_hre.{num}.d',"[SCOPE.sCountry('hre_reply_holder').GetName] has refused our summons. The relevant imperial casus belli is now available against an external holder, subject to normal truces. A member protected by an obligation receives no infamy or casus belli.","[SCOPE.sCountry('hre_reply_holder').GetName] a refusé notre sommation. Le casus belli impérial correspondant est disponible contre un détenteur extérieur, sous réserve des trêves normales. Un membre protégé par une obligation ne reçoit ni infamie ni casus belli.")
 for num in [30,31,34]:
  en,fr=loc[f'aor1776_hre.{num}.d'];L(f'aor1776_hre.{num}.d',en+'\n'+replytext,fr+'\n'+replytext)
 L('aor1776_hre.ack','The council has been informed.','Le conseil en est informé.')
 # Peace/backdown enforcement already works in the player's test. Keep it;
 # add notifications, rather than replacing normal diplomacy with forced war.
 for key in ['aor1776_hre_subject_release','aor1776_hre_restitution']:
  n=next(n for n in cw.parse(files[WG]) if n.key==key).children('on_enforced')[0]
  files[WG]=edits(files[WG],[(n.end-1,n.end-1,'\n scope:target_country = { save_scope_as = hre_reply_holder } trigger_event = { id = aor1776_hre.34 popup = yes }\n')])
 files[WG]=files[WG].replace('scope:target_country = { aor1776_hre_release_imperial_subjects = yes }','scope:target_country = { aor1776_hre_snapshot_reply_subjects = yes aor1776_hre_release_imperial_subjects = yes }')
 # Demand accepted before a play exists: native hook uses the initiator ROOT.
 # The player confirmed that the goal's on_enforced runs on accepted demands.
 # Do not also notify through on_demand_accepted: that would duplicate messages.
 files[OA]=files[OA].replace('on_diplomatic_play_started =','on_diplo_play_start =')
 files[OA]=files[OA].replace('effect = { aor1776_hre_defend_external_attack = yes }','effect = { initiator = { save_scope_as = initiator } target = { save_scope_as = target } aor1776_hre_defend_external_attack = yes }')

 # One month of deliberation for EVERY ballot, even when every elector is AI.
 files[EF]=files[EF].replace('name = aor1776_hre_vote_deadline days = 90','name = aor1776_hre_vote_deadline days = 30')
 start=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_start_ballot')
 body=files[EF][start.start:start.end]
 body=body.replace('if = { limit = { is_ai = yes } aor1776_hre_ai_ballot = yes }\n  else =','if = { limit = { is_ai = no }')
 body=body.replace(' aor1776_hre_tally_ballot = yes',' global_var:aor1776_hre_emperor_country = { set_variable = { name = aor1776_hre_deliberation days = 30 } trigger_event = { id = aor1776_hre.3 days = 30 popup = no } }\n aor1776_hre_feedback_refresh = yes')
 files[EF]=replace_node(files[EF],'aor1776_hre_start_ballot',block('aor1776_hre_start_ballot','''
 set_global_variable = { name = aor1776_hre_elector_count value = 0 }
 set_global_variable = { name = aor1776_hre_ballots_cast value = 0 }
 every_country = { limit = { aor1776_hre_member = yes } set_variable = { name = aor1776_hre_votes value = 0 } remove_variable = aor1776_hre_voted remove_variable = aor1776_hre_voted_for remove_variable = aor1776_hre_voter_this_round }
 global_var:aor1776_hre_emperor_country = { set_variable = { name = aor1776_hre_deliberation days = 30 } trigger_event = { id = aor1776_hre.3 days = 30 popup = no } }
 every_country = { limit = { aor1776_hre_elector = yes } set_variable = aor1776_hre_voter_this_round set_variable = { name = aor1776_hre_vote_deadline days = 30 } change_global_variable = { name = aor1776_hre_elector_count add = 1 } }
 every_country = { limit = { has_variable = aor1776_hre_voter_this_round is_ai = no } trigger_event = { id = aor1776_hre.1 popup = yes } }
 aor1776_hre_feedback_refresh = yes
'''))
 tally=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_tally_ballot')
 body=files[EF][tally.start:tally.end].replace('global_var:aor1776_hre_elector_count > 0','NOT = { global_var:aor1776_hre_emperor_country = { has_variable = aor1776_hre_deliberation } } global_var:aor1776_hre_elector_count > 0')
 files[EF]=edits(files[EF],[(tally.start,tally.end,body)])
 files[EV]+=block('aor1776_hre.3','''type = country_event
 hidden = yes
 trigger = { has_global_variable = aor1776_hre_election_open NOT = { has_variable = aor1776_hre_deliberation } }
 immediate = {
  every_country = { limit = { aor1776_hre_elector = yes has_variable = aor1776_hre_voter_this_round NOT = { has_variable = aor1776_hre_voted } }
   aor1776_hre_ai_ballot = yes
  }
  aor1776_hre_tally_ballot = yes
 }
''')
 files[OA]=files[OA].replace('OR = { is_ai = yes NOT = { has_variable = aor1776_hre_vote_deadline } }','NOT = { has_variable = aor1776_hre_vote_deadline } NOT = { global_var:aor1776_hre_emperor_country = { has_variable = aor1776_hre_deliberation } }')
 # A binding promise is attached to the COUNTRY, not a deceased individual.
 files['common/treaty_articles/1776_imperial_electoral_promise.txt']=block('aor1776_electoral_promise','''
 kind = directed
 cost = 0
 maintenance_paid_by = target_country
 usage_limit = once_per_side
 icon = "gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_obligation.dds"
 visible = { OR = { aor1776_hre_elector = yes aor1776_hre_emperor = yes } }
 possible = { aor1776_hre_member = yes scope:other_country = { aor1776_hre_member = yes } }
 can_ratify = {
  scope:source_country = { aor1776_hre_elector = yes NOT = { has_variable = aor1776_hre_promised_candidate } }
  scope:target_country = { aor1776_hre_candidate = yes OR = { aor1776_hre_elector = yes aor1776_hre_emperor = yes } }
  NOT = { has_global_variable = aor1776_hre_election_open }
 }
 can_withdraw = { scope:source_country = { NOT = { has_variable = aor1776_hre_promised_candidate } } }
 on_entry_into_force = {
  scope:article_options.source_country = {
   set_variable = { name = aor1776_hre_promised_candidate value = scope:article_options.target_country days = { value = scope:treaty_options.binding_period multiply = 365 } }
  }
 }
 on_withdrawal = { scope:article.source_country = { if = { limit = { var:aor1776_hre_promised_candidate ?= scope:article.target_country } remove_variable = aor1776_hre_promised_candidate } } }
 on_break = {}
 ai = {
  treaty_categories = { power_bloc }
  article_ai_usage = { request offer }
  evaluation_chance = { value = 0.1 }
  inherent_accept_score = { value = -50 }
 }
''')
 L('aor1776_electoral_promise','Pledge an imperial electoral vote','Promettre une voix impériale')
 L('aor1776_electoral_promise_desc','The elector pledges its next imperial ballot to the other treaty party while the binding period lasts. Negotiate money or other articles in exchange. After expiry the elector is free again. The commitment does not make an ineligible candidate eligible.','L’électeur promet son prochain vote impérial à l’autre partie pendant la durée d’engagement du traité. Négocier une somme ou d’autres articles en échange. À l’expiration, il retrouve sa liberté. La promesse ne rend pas éligible un candidat qui ne l’est pas.')
 score='common/script_values/1776_imperial_elections.txt'
 files[score]=append_inside(files[score],'aor1776_hre_vote_preference','if = { limit = { scope:hre_voter = { var:aor1776_hre_promised_candidate ?= root } } add = 1000 }')
 # Human votes obey a still-active promise; expired/ineligible promises do not.
 promise='OR = { NOT = { exists = var:aor1776_hre_promised_candidate } var:aor1776_hre_promised_candidate ?= scope:hre_vote_choice var:aor1776_hre_promised_candidate ?= { aor1776_hre_ballot_candidate = no } }'
 cast=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_cast_vote');lim=cast.children('if')[0].children('limit')[0]
 files[EF]=edits(files[EF],[(lim.end-1,lim.end-1,'\n'+promise+'\n')])
 cast=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_cast_vote');ok=cast.children('if')[0]
 files[EF]=edits(files[EF],[(ok.end-1,ok.end-1,'\n if = { limit = { var:aor1776_hre_promised_candidate ?= scope:hre_vote_choice } set_variable = aor1776_hre_promise_cast }\n')])
 files[EF]=append_inside(files[EF],'aor1776_hre_finish_investiture','every_country = { limit = { has_variable = aor1776_hre_promise_cast } remove_variable = aor1776_hre_promised_candidate remove_variable = aor1776_hre_promise_cast }')

 # Cohesion is based on territorial authority and named political relations,
 # not on whether an estate is a native subject of the Emperor.
 files[ID]=files[ID].replace('  power_bloc_cohesion_per_member_add = -1','  power_bloc_cohesion_per_member_add = 0')
 ident=next(n for n in cw.parse(files[ID]));co=ident.children('cohesion')[0]
 files[ID]=edits(files[ID],[(co.start,co.end,'''cohesion = {
 value = 90
 if = { limit = { has_global_variable = aor1776_hre_outside_provinces } subtract = { value = global_var:aor1776_hre_outside_provinces divide = 278 multiply = 40 desc = aor1776_hre_cohesion_territories } }
 if = { limit = { has_global_variable = aor1776_hre_hostile_electors } subtract = { value = global_var:aor1776_hre_hostile_electors multiply = 5 desc = aor1776_hre_cohesion_electors } }
 if = { limit = { has_global_variable = aor1776_hre_hostile_cities } subtract = { value = global_var:aor1776_hre_hostile_cities multiply = 3 desc = aor1776_hre_cohesion_cities } }
 min = 0
 max = 100
}''')])
 L('aor1776_hre_cohesion_territories','Imperial provinces outside imperial authority','Provinces impériales hors autorité impériale')
 L('aor1776_hre_cohesion_electors','Electors with negative relations','Électeurs aux relations négatives')
 L('aor1776_hre_cohesion_cities','Free cities with negative relations','Villes libres aux relations négatives')
 surcharge='state_aor1776_imperial_conquest_infamy_mult'
 files['common/modifier_type_definitions/1776_imperial_modifier_types.txt']=block(surcharge,'decimals = 0\ncolor = bad\npercent = yes\ngame_data = { ai_value = 0 }')
 files['common/static_modifiers/1776_imperial_territory.txt']=block('aor1776_hre_registered_territory','icon = "gfx/interface/icons/timed_modifier_icons/aor1776_hre_registered_territory.dds"\n'+surcharge+' = 0.25')
 from map2k_work import ROOT,GAME
 conquer_rel='common/war_goal_types/03_conquer_state.txt'
 source=ROOT/conquer_rel
 if not source.exists():source=GAME/conquer_rel
 conquer=source.read_text(encoding='utf-8-sig')
 if surcharge not in conquer:
  infamy=cw.parse(conquer)[0].children('infamy')[0]
  conquer=edits(conquer,[(infamy.end-1,infamy.end-1,'\n multiply = { desc = '+surcharge+' value = 1 add = scope:target_state.modifier:'+surcharge+' }\n')])
 files[conquer_rel]=conquer
 L(surcharge,'Additional infamy for conquering this state','Infamie supplémentaire pour conquérir cet État')
 L(surcharge+'_desc','Applied only to the Conquer State war goal. Imperial restitution is exempt.','S’applique uniquement au but de guerre Conquérir l’État. Les rétrocessions impériales sont exemptées.')
 L('aor1776_hre_registered_territory','Registered imperial territory','Territoire impérial enregistré')
 L('aor1776_hre_registered_territory_desc','This state contains registered imperial provinces, even under foreign control. Conquering it generates 25% additional infamy. The marker does not claim that every province in the entire state region is imperial.','Cet État contient des provinces impériales enregistrées, même sous contrôle étranger. Sa conquête génère 25 % d’infamie supplémentaires. Le marqueur ne signifie pas que toutes les provinces de la région de jeu sont impériales.')
 refresh='''
 if = { limit = { exists = global_var:aor1776_hre_emperor_country }
 global_var:aor1776_hre_emperor_country = { save_scope_as = hre_current_emperor clear_variable_list = aor1776_hre_states_list clear_variable_list = aor1776_hre_electors_list }
 set_global_variable = { name = aor1776_hre_outside_provinces value = 0 }
 set_global_variable = { name = aor1776_hre_hostile_electors value = 0 }
 set_global_variable = { name = aor1776_hre_hostile_cities value = 0 }
 every_country = { every_scope_state = { set_variable = { name = aor1776_hre_registered_count value = 0 } } }
'''
 for r in ledger:
  refresh+=f'''p:{r['rgb']}.state ?= {{ change_variable = {{ name = aor1776_hre_registered_count add = 1 }}
 if = {{ limit = {{ owner = {{ aor1776_hre_under_imperial_authority = no }} }} change_global_variable = {{ name = aor1776_hre_outside_provinces add = 1 }} }}
}}
'''
 refresh+='''
 every_country = {
  every_scope_state = {
   if = { limit = { var:aor1776_hre_registered_count > 0 }
    if = { limit = { NOT = { has_modifier = aor1776_hre_registered_territory } } add_modifier = { name = aor1776_hre_registered_territory } }
    scope:hre_current_emperor = { add_to_variable_list = { name = aor1776_hre_states_list target = prev } }
   }
   else_if = { limit = { has_modifier = aor1776_hre_registered_territory } remove_modifier = aor1776_hre_registered_territory }
  }
  if = { limit = { aor1776_hre_member = yes }
   set_variable = { name = aor1776_hre_relation_to_emperor value = "relations(scope:hre_current_emperor)" }
   if = { limit = { aor1776_hre_elector = yes }
    scope:hre_current_emperor = { add_to_variable_list = { name = aor1776_hre_electors_list target = prev } }
    if = { limit = { var:aor1776_hre_relation_to_emperor < 0 } change_global_variable = { name = aor1776_hre_hostile_electors add = 1 } }
   }
   if = { limit = { aor1776_hre_free_city = yes var:aor1776_hre_relation_to_emperor < 0 } change_global_variable = { name = aor1776_hre_hostile_cities add = 1 } }
  }
 }
 every_country = { limit = { aor1776_hre_member = yes }
  set_variable = { name = aor1776_hre_ui_emperor value = scope:hre_current_emperor }
  set_variable = { name = aor1776_hre_ui_person value = global_var:aor1776_hre_emperor_person }
  set_variable = { name = aor1776_hre_outside_provinces value = global_var:aor1776_hre_outside_provinces }
  set_variable = { name = aor1776_hre_under_authority value = 278 }
  change_variable = { name = aor1776_hre_under_authority subtract = global_var:aor1776_hre_outside_provinces }
  set_variable = { name = aor1776_hre_hostile_electors value = global_var:aor1776_hre_hostile_electors }
  set_variable = { name = aor1776_hre_hostile_cities value = global_var:aor1776_hre_hostile_cities }
  if = { limit = { NOT = { has_journal_entry = je_aor1776_hre_situation } } add_journal_entry = { type = je_aor1776_hre_situation } }
  if = { limit = { aor1776_hre_elector = yes has_global_variable = aor1776_hre_election_open NOT = { has_journal_entry = je_aor1776_hre_vote } } add_journal_entry = { type = je_aor1776_hre_vote } }
 }
 }
'''
 refresh=refresh.replace('name = aor1776_hre_under_authority value = 278','name = aor1776_hre_under_authority value = '+str(len(ledger)))
 files[EF]+=block('aor1776_hre_feedback_refresh',refresh)
 files[ID]=files[ID].replace('divide = 278','divide = '+str(len(ledger)))
 files[EF]=append_inside(files[EF],'aor1776_hre_initialize','aor1776_hre_feedback_refresh = yes')
 files[OA]=files[OA].replace('aor1776_hre_refresh_pacts = yes','aor1776_hre_refresh_pacts = yes\n   aor1776_hre_feedback_refresh = yes')
 for key in ['aor1776_hre_return_requested_provinces','aor1776_hre_release_imperial_subjects','aor1776_hre_finish_investiture']:
  files[EF]=append_inside(files[EF],key,'aor1776_hre_feedback_refresh = yes')
 # A complete return may destroy the old owner-state scope. Keep its region
 # reference before any RGB transfer, instead of dereferencing it afterwards.
 ret=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_return_requested_provinces')
 body=files[EF][ret.start:ret.end]
 body=re.sub(r'scope:hre_request_state = \{ state_region = (s:STATE_\w+) \}',r'scope:hre_request_region = \1',body)
 body=body.replace('aor1776_hre_return_requested_provinces = {','aor1776_hre_return_requested_provinces = {\nscope:hre_request_state ?= { state_region = { save_scope_as = hre_request_region } }',1)
 files[EF]=edits(files[EF],[(ret.start,ret.end,body)])

 # Country-context journals work for AI estates and human electors alike.
 je=block('je_aor1776_hre_situation','''
 icon = "gfx/interface/icons/central_identity_pillars_icons/aor1776_imperial_federation_v2.dds"
 is_shown_when_inactive = { aor1776_hre_member = yes }
 possible = { has_global_variable = aor1776_hre_initialized }
 invalid = { aor1776_hre_member = no }
 complete = { always = no }
 widget = { gui = "gui/journal_entry_widgets/1776_imperial_widgets.gui" name = "aor1776_hre_situation_widget" container = "custom_widget_container_5" }
 weight = 20
''')
 je+=block('je_aor1776_hre_vote','''
 icon = "gfx/interface/icons/central_identity_pillars_icons/aor1776_imperial_federation_v2.dds"
 is_shown_when_inactive = { aor1776_hre_elector = yes has_global_variable = aor1776_hre_election_open }
 possible = { aor1776_hre_elector = yes has_global_variable = aor1776_hre_election_open }
 complete = { NOT = { has_global_variable = aor1776_hre_election_open } }
 invalid = { aor1776_hre_elector = no }
 weight = 100
'''+''.join('scripted_button = aor1776_hre_vote_'+t+'\n' for t in members))
 files['common/journal_entries/1776_imperial_situation.txt']=je
 buttons=''
 for t in members:
  # The native scripted-button UI supplies a precise country label and checks.
  buttons+=block('aor1776_hre_vote_'+t,f'''name = aor1776_hre.vote_{t}
 desc = aor1776_hre_vote_button_desc
 visible = {{ c:{t} ?= {{ aor1776_hre_ballot_candidate = yes }} }}
 possible = {{ aor1776_hre_elector = yes has_variable = aor1776_hre_voter_this_round NOT = {{ has_variable = aor1776_hre_voted }}
 OR = {{ NOT = {{ exists = var:aor1776_hre_promised_candidate }} var:aor1776_hre_promised_candidate ?= c:{t} var:aor1776_hre_promised_candidate ?= {{ aor1776_hre_ballot_candidate = no }} }} }}
 effect = {{ c:{t} = {{ save_scope_as = hre_vote_choice }} aor1776_hre_cast_vote = yes aor1776_hre_tally_ballot = yes }}
 ai_chance = {{ base = 0 }}''')
 files['common/scripted_buttons/1776_imperial_voting.txt']=buttons
 L('je_aor1776_hre_situation','Holy Roman Empire','Saint-Empire romain germanique')
 L('je_aor1776_hre_situation_reason','The imperial estates share rights and obligations without becoming provinces of the Emperor. The yellow map shows the registered imperial extent regardless of its occupiers. Consult the list for current holders.','Les États impériaux partagent des droits et des obligations sans devenir des provinces de l’empereur. La carte jaune montre le périmètre impérial enregistré indépendamment de ses occupants. La liste indique les détenteurs actuels.')
 L('je_aor1776_hre_situation_status',"Provinces under imperial authority: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_under_authority').GetValue|0]/278\nOutside imperial authority: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_outside_provinces').GetValue|0]\nElectors with negative relations: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_hostile_electors').GetValue|0] (−5 each)\nFree cities with negative relations: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_hostile_cities').GetValue|0] (−3 each)","Provinces sous autorité impériale : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_under_authority').GetValue|0]/278\nHors autorité impériale : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_outside_provinces').GetValue|0]\nÉlecteurs aux relations négatives : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_hostile_electors').GetValue|0] (−5 chacun)\nVilles libres aux relations négatives : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_hostile_cities').GetValue|0] (−3 chacune)")
 L('je_aor1776_hre_vote','The imperial election','L’élection impériale')
 L('je_aor1776_hre_vote_reason','Choose a living eligible candidate below, including your own country when eligible. Each ballot lasts thirty days before the count can install an Emperor. AI electors retain their rules. A binding electoral promise restricts your vote until its expiry.','Choisissez ci-dessous un candidat vivant et éligible, y compris votre propre pays s’il est éligible. Chaque scrutin dure trente jours avant de pouvoir installer l’empereur. Les électeurs IA conservent leurs règles. Une promesse électorale en vigueur limite votre vote jusqu’à son expiration.')
 L('je_aor1776_hre_vote_status','The electoral crowns deliberate. The majority cannot install an Emperor before thirty days have passed.','Les couronnes électorales délibèrent. La majorité ne peut installer un empereur avant trente jours.')
 L('aor1776_hre_vote_button_desc','Cast your vote for this country. A still-binding electoral promise must be respected.','Voter pour ce pays. Une promesse électorale encore en vigueur doit être respectée.')
 L('aor1776_hre_map_legend','Yellow: registered imperial provinces, regardless of owner. Grey: other land; blue: water.','Jaune : provinces impériales enregistrées, quel que soit leur propriétaire. Gris : autres terres ; bleu : eaux.')
 L('aor1776_hre_electors_heading','The electoral crowns — click to negotiate in the country panel','Les couronnes électorales — cliquer pour négocier dans le panneau du pays')
 L('aor1776_hre_states_heading','Current states containing registered imperial provinces','États actuels contenant des provinces impériales enregistrées')
 gui='''flowcontainer = {
 name = "aor1776_hre_situation_widget"
 direction = vertical
 spacing = 8
 layoutpolicy_horizontal = expanding
 textbox = { size = { 500 125 } text = "je_aor1776_hre_situation_status" multiline = yes }
 icon = { size = { 500 370 } texture = "gfx/interface/journal_entries/aor1776_hre_registered_map.dds" }
 textbox = { size = { 500 50 } text = "aor1776_hre_map_legend" multiline = yes }
 textbox = { size = { 500 40 } text = "aor1776_hre_electors_heading" multiline = yes }
 fixedgridbox = {
  datamodel = "[JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.MakeScope.GetList('aor1776_hre_electors_list')]"
  addcolumn = 500
  addrow = 85
  item = {
   widget = {
    name = "aor1776_hre_elector_row"
    size = { 500 85 }
   hbox = {
    layoutpolicy_horizontal = expanding
    layoutpolicy_vertical = expanding
    datacontext = "[Scope.GetCountry]"
    visible = "[Scope.GetCountry.IsValid]"
    spacing = 8
    widget = {
     size = { 80 80 }
     character_portrait_medium = { datacontext = "[Country.AccessRuler]" blockoverride "show_hat" {} blockoverride "highlight" {} blockoverride "rank_icon" {} }
    }
    button = {
     size = { 380 75 }
     onclick = "[InformationPanelBar.OpenCountryPanel(Country.AccessSelf)]"
     tooltip = "aor1776_hre_elector_card_tt"
     textbox = { size = { 370 70 } text = "[Country.GetName] — [Country.GetRuler.GetFullNameNoFormatting]" multiline = yes }
    }
   }
   }
  }
 }
 textbox = { size = { 500 35 } text = "aor1776_hre_states_heading" }
 fixedgridbox = {
  datamodel = "[JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.MakeScope.GetList('aor1776_hre_states_list')]"
  addcolumn = 500
  addrow = 38
  item = {
   button = {
    datacontext = "[Scope.GetState]"
    size = { 500 35 }
    onclick = "[InformationPanelBar.OpenStatePanel(State.AccessSelf)]"
    textbox = { size = { 490 32 } text = "[State.GetName] — [State.GetOwner.GetName] ([State.MakeScope.Var('aor1776_hre_registered_count').GetValue|0])" }
   }
  }
 }
}
'''
 # A flowcontainer must own a sized widget, never an hbox/vbox directly.
 # The old direct hbox provoked a layout stack overflow on opening the JE.
 emperor='''widget = {
 name = "aor1776_hre_emperor_row"
 size = { 500 85 }
 hbox = {
 layoutpolicy_horizontal = expanding
 layoutpolicy_vertical = expanding
 visible = "[JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_person').GetCharacter.IsValid]"
 spacing = 8
 widget = { size = { 80 80 } character_portrait_medium = { datacontext = "[JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_person').GetCharacter]" blockoverride "show_hat" {} blockoverride "highlight" {} blockoverride "rank_icon" {} } }
 textbox = { size = { 410 75 } text = "aor1776_hre_emperor_person" multiline = yes }
}
}
'''
 gui=gui.replace(' textbox = { size = { 500 125 }',emperor+' textbox = { size = { 500 125 }',1)
 mapbutton='''button = {
 size = { 500 50 }
 onclick = "[GetVariableSystem.Toggle('aor1776_hre_map_collapsed')]"
 tooltip = "aor1776_hre_map_legend"
 icon = { size = { 45 45 } texture = "gfx/interface/icons/map_mode_icons/aor1776_hre_territories.dds" }
 textbox = { position = { 55 0 } size = { 440 45 } text = "aor1776_hre_map_toggle" }
}
'''
 gui=gui.replace(' icon = { size = { 500 370 }',mapbutton+' icon = { visible = "[Not(GetVariableSystem.Exists(\'aor1776_hre_map_collapsed\'))]" size = { 500 370 }',1)
 gui=gui.replace('textbox = {','textbox = { using = fontsize_medium')
 L('aor1776_hre_map_toggle','Show / hide the imperial map','Afficher / masquer la carte impériale')
 L('aor1776_hre_elector_card_tt',"Recognised imperial elector: [Country.GetName]\nRelations with the Emperor: [Country.MakeScope.Var('aor1776_hre_relation_to_emperor').GetValue|=0]\nOpen this country to negotiate an electoral pledge in the native treaty editor.","Électeur impérial reconnu : [Country.GetName]\nRelations avec l’empereur : [Country.MakeScope.Var('aor1776_hre_relation_to_emperor').GetValue|=0]\nOuvrir ce pays pour négocier une promesse électorale dans l’éditeur de traité natif.")
 L('aor1776_hre_emperor_person',"Emperor: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_person').GetCharacter.GetFullNameNoFormatting]\nImperial country: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.GetName]","Empereur : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_person').GetCharacter.GetFullNameNoFormatting]\nPays impérial : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.GetName]")
 files['gui/journal_entry_widgets/1776_imperial_widgets.gui']=gui
 # Native wargoal loc follows war_goal_<key>_* (not the bare identifier).
 sgui='''aor1776_hre_subject_preview = { scope = country effect = { aor1776_hre_preview_subjects = yes } }
 aor1776_hre_province_preview = { scope = state effect = { aor1776_hre_preview_provinces = yes } }
'''
 files['common/scripted_guis/1776_imperial_previews.txt']=sgui
 # Kick is a code-side command, not a diplomatic action. No unverified
 # can_kick field or global AI/PowerBloc defines: protect both player entry
 # points, intercept the documented native catalyst, and reconcile drift.
 files[trig]+=block('aor1776_hre_illegal_expulsion','''aor1776_hre_member = yes
 scope:target_country ?= {
  aor1776_hre_emperor = yes is_power_bloc_leader = yes
  power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation }
 }''')
 files['common/scripted_guis/1776_imperial_previews.txt']+=block('aor1776_hre_allow_native_kick','''scope = country
 is_valid = { NOT = { power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } } }
 effect = {}''')
 for rel,original in [('gui/power_bloc_panel.gui','[IsValid(PowerBloc.Kick(Country.Self))]'),('gui/right_click_menu.gui','[IsValid(Country.GetPowerBloc.Kick(Country.Self))]')]:
  source=ROOT/rel
  if not source.exists():source=GAME/rel
  raw=source.read_text(encoding='utf-8-sig')
  guard="[And("+original[1:-1]+", GetScriptedGui('aor1776_hre_allow_native_kick').IsValid(GuiScope.SetRoot(Country.MakeScope).End))]"
  if original in raw:raw=raw.replace(original,guard)
  elif guard not in raw:raise ValueError('Native kick GUI changed: '+rel)
  tooltip="[SelectLocalization(GetScriptedGui('aor1776_hre_allow_native_kick').IsValid(GuiScope.SetRoot(Country.MakeScope).End), 'POWER_BLOC_KICK_MEMBER_TOOLTIP', 'aor1776_hre_cannot_expel_tt')]"
  raw=raw.replace('tooltip = "POWER_BLOC_KICK_MEMBER_TOOLTIP"','tooltip = "'+tooltip+'"')
  files[rel]=raw
 L('aor1776_hre_cannot_expel_tt','An imperial estate cannot be expelled by a simple decision of the Emperor. Leaving the Empire requires an enforced secession demand.','Un État impérial ne peut pas être expulsé par une simple décision de l’empereur. Quitter l’Empire exige une demande de sécession imposée.')
 files[EF]+=block('aor1776_hre_restore_membership','''
 if = { limit = { exists = global_var:aor1776_hre_emperor_country
  global_var:aor1776_hre_emperor_country = { is_power_bloc_leader = yes power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } } }
  global_var:aor1776_hre_emperor_country = { save_scope_as = hre_guard_emperor }
  every_country = {
   limit = { aor1776_hre_member = yes is_subject = no
    NOT = { this = scope:hre_guard_emperor }
    NOT = { is_in_same_power_bloc = scope:hre_guard_emperor }
    NOT = { is_diplomatic_play_enemy_of = scope:hre_guard_emperor }
   }
   set_variable = aor1776_hre_membership_pending
   join_power_bloc = scope:hre_guard_emperor
   if = { limit = { is_in_same_power_bloc = scope:hre_guard_emperor }
    remove_variable = aor1776_hre_membership_pending
    if = { limit = { is_ai = no NOT = { has_variable = aor1776_hre_membership_notice } }
     set_variable = { name = aor1776_hre_membership_notice days = 90 }
     trigger_event = { id = aor1776_hre.41 popup = yes }
    }
   }
  }
 }
''')
 files[EF]+=block('aor1776_hre_schedule_membership_guard','''
 if = { limit = { exists = global_var:aor1776_hre_emperor_country }
  global_var:aor1776_hre_emperor_country = {
   if = { limit = { NOT = { has_variable = aor1776_hre_membership_guard_scheduled } }
    set_variable = { name = aor1776_hre_membership_guard_scheduled days = 2 }
    trigger_event = { id = aor1776_hre.40 days = 1 popup = no }
   }
  }
 }
''')
 files[EV]+=block('aor1776_hre.40','''type = country_event
 hidden = yes
 immediate = {
  remove_variable = aor1776_hre_membership_guard_scheduled
  if = { limit = { this = global_var:aor1776_hre_emperor_country }
   aor1776_hre_restore_membership = yes
   aor1776_hre_schedule_membership_guard = yes
  }
 }''')
 files[EV]+=block('aor1776_hre.41','''type = country_event
 placement = root
 title = aor1776_hre.41.t
 desc = aor1776_hre.41.d
 event_image = { video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }
 option = { name = aor1776_hre.41.a default_option = yes }''')
 L('aor1776_hre.41.t','Our imperial rights are upheld','Nos droits impériaux sont maintenus')
 L('aor1776_hre.41.d','Without a recognised secession, our estate remains part of the Empire. An invalid exclusion has been reversed and our membership restored.','Sans sécession reconnue, notre État demeure dans l’Empire. Une exclusion invalide a été annulée et notre appartenance au bloc rétablie.')
 L('aor1776_hre.41.a','Our place in the Empire is preserved.','Notre place dans l’Empire est préservée.')
 for key in ['aor1776_hre_initialize','aor1776_hre_finish_investiture']:
  files[EF]=append_inside(files[EF],key,'aor1776_hre_restore_membership = yes\naor1776_hre_schedule_membership_guard = yes')
 files[OA]=files[OA].replace('aor1776_hre_refresh_pacts = yes','aor1776_hre_restore_membership = yes\n   aor1776_hre_schedule_membership_guard = yes\n   aor1776_hre_refresh_pacts = yes')
 # The catalyst is the only documented code-side expulsion hook. Suppress
 # its collateral penalties only for an illegal imperial exclusion. Preserve
 # all other catalysts and vanilla behavior for every non-imperial bloc.
 rel='common/diplomatic_catalysts/00_diplomatic_catalysts.txt'
 source=ROOT/rel
 if not source.exists():source=GAME/rel
 raw=source.read_text(encoding='utf-8-sig')
 cat=next(n for n in cw.parse(raw) if n.key=='catalyst_kicked_out_of_bloc')
 catraw=raw[cat.start:cat.end]
 if 'aor1776_hre_illegal_expulsion' not in catraw:
  cns=cw.parse(catraw)[0]
  eff=cns.children('effect')[0]
  old=catraw[eff.start:eff.end]
  effectbody=old[old.index('{')+1:old.rfind('}')]
  catraw=edits(catraw,[(eff.start,eff.end,'effect = {\n if = { limit = { aor1776_hre_illegal_expulsion = yes } aor1776_hre_restore_membership = yes }\n else = { '+effectbody+' }\n}')])
  cns=cw.parse(catraw)[0]
  changes=[]
  for field in ['political_lobby_creation','ai_country_goal_recalculation']:
   for n in cns.children(field):
    if n.children('trigger'):raise ValueError('Upstream kick trigger changed; preserve manually')
    changes.append((n.start+catraw[n.start:n.end].index('{')+1,)*2+('\n trigger = { aor1776_hre_illegal_expulsion = no }\n',))
  catraw=edits(catraw,changes)
 files[rel]=edits(raw,[(cat.start,cat.end,catraw)])
 for key,en,fr in [('aor1776_hre_subject_release','Liberation of imperial estates','Libération des États impériaux'),('aor1776_hre_restitution','Imperial restitution','Rétrocession impériale'),('aor1776_hre_secession','Imperial secession','Sécession impériale')]:
  L('war_goal_'+key+'_type_name',en,fr)
  L('war_goal_'+key+'_type_desc',en+' — see the exact demand below.',fr+' — consulter la demande exacte ci-dessous.')
  L('war_goal_'+key,en,fr)
  if key.endswith('subject_release'):
   detail="[GetScriptedGui('aor1776_hre_subject_preview').ExecuteTooltip(GuiScope.SetRoot(WAR_GOAL_DRAFT.GetTarget.MakeScope).End)]"
   L('war_goal_'+key+'_desc',"[WAR_GOAL_DRAFT.GetHolder.GetName] demands the release of the following imperial subjects of [WAR_GOAL_DRAFT.GetTarget.GetName]:\n"+detail,"[WAR_GOAL_DRAFT.GetHolder.GetName] exige la libération des sujets impériaux suivants de [WAR_GOAL_DRAFT.GetTarget.GetName] :\n"+detail)
  elif key.endswith('restitution'):
   detail="[GetScriptedGui('aor1776_hre_province_preview').ExecuteTooltip(GuiScope.SetRoot(WAR_GOAL_DRAFT.GetTargetState.MakeScope).End)]"
   L('war_goal_'+key+'_desc',"Registered provinces to return:\n"+detail,"Provinces enregistrées à restituer :\n"+detail)
  else:L('war_goal_'+key+'_desc','Leave the imperial bloc through an enforced demand.','Quitter le bloc impérial par une demande imposée.')
  L('war_goal_'+key+'_sway_desc',en,fr)
  L('dp_'+key+'_desc',en+' — normal demand acceptance and escalation apply.',fr+' — les règles normales d’acceptation et d’escalade s’appliquent.')
 # Avoid overwriting immersive prose; correct only the obsolete timing.
 for lang in ['english','french']:
  rel=f'localization/{lang}/1776_imperial_constitution_l_{lang}.yml'
  files[rel]=files[rel].replace('After three months without instructions','After thirty days without instructions').replace('Après trois mois sans instruction','Après trente jours sans instruction')
  files[f'localization/{lang}/1776_imperial_feedback_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[0 if lang=='english' else 1].replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())
 return files
