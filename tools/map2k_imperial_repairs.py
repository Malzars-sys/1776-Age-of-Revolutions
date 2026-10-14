"""Player-tested defects: bounded military calls, native liberation, readable replies.

Compile only; apply the generated patch explicitly. No save/game mutations.
"""
import re
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2k_imperial_feedback import block,child,replace_node,append_inside,EF,EV,OA,DA,WG,DP
from map2k_work import GAME

GOAL='aor1776_hre_liberate_estate'
VALUES='common/script_values/1776_imperial_diplomacy.txt'

def gui_end(raw,start):
 opening=raw.index('{',start);depth=1
 for tok in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',raw[opening+1:]):
  if tok.group()=='{':depth+=1
  elif tok.group()=='}':depth-=1
  if depth==0:return opening+1+tok.end()
 raise ValueError('Unclosed GUI block')

def map_menu_range(raw):
 start=raw.rfind('right_click_menu = {',0,raw.index('name = "map_modes_right_click_menu"'))
 return start,gui_end(raw,start)

def augment_repairs(files,ledger,members):
 loc={}
 def L(k,en,fr):loc[k]=(en,fr)
 L('aor1776_hre.ack','We shall take note before the Diet.','Nous en prendrons acte devant la Diète.')
 # These are symbolic, consumed explicitly by scripts, not code modifiers.
 rel='common/modifier_type_definitions/1776_imperial_modifier_types.txt'
 for n in reversed(cw.parse(files[rel])):
  if not n.children('script_only'):files[rel]=edits(files[rel],[(n.end-1,n.end-1,'\n script_only = yes\n')])
 # Scripted-button ai_chance is a script value, unlike event ai_chance.
 for rel in ['common/scripted_buttons/1776_imperial_voting.txt','common/scripted_buttons/1776_imperial_centralization.txt']:
  files[rel]=files[rel].replace('ai_chance = { base = 0 }','ai_chance = { value = 0 }')
 # Auto-support pacts bypass all filters and drag captive estates into the
 # initiator's camp. Military obligations are now exclusively filtered below.
 files[DA]=re.sub(r'\s*auto_support_type = dp_aor1776_hre_(?:restitution|subject_release)', '',files[DA])
 # No recursive response to every backer change. Start, weekly play pulse and
 # war start suffice; persistent per-play stamps also bound repeated calls.
 files[OA]=files[OA].replace(' on_diplo_play_join_side = { on_actions = { aor1776_hre_defense_hook } }','')
 defense='''if = { limit = { NOT = { has_variable = aor1776_hre_adjusting_backers } exists = global_var:aor1776_hre_emperor_country exists = scope:initiator exists = scope:target }
 set_variable = aor1776_hre_adjusting_backers
 global_var:aor1776_hre_emperor_country = { save_scope_as = hre_military_emperor }
 if = { limit = { scope:target = { aor1776_hre_member = yes } scope:initiator = { aor1776_hre_member = no }
  NOT = { scope:target = scope:hre_military_emperor } NOT = { has_variable = aor1776_hre_emperor_called_target }
  scope:hre_military_emperor.power_bloc ?= { has_principle_group = principle_group:aor1776_hre_group_circles } }
  set_variable = aor1776_hre_emperor_called_target
  if = { limit = { scope:hre_military_emperor = { NOT = { is_diplomatic_play_ally_of = scope:target } } } add_target_backers = { scope:hre_military_emperor } }
 }
 if = { limit = { scope:initiator = { aor1776_hre_member = yes } scope:target = { aor1776_hre_member = no }
  NOT = { scope:initiator = scope:hre_military_emperor } NOT = { has_variable = aor1776_hre_emperor_called_initiator }
  scope:hre_military_emperor.power_bloc ?= { OR = { has_principle = principle:aor1776_hre_circles_2 has_principle = principle:aor1776_hre_circles_3 } } }
  set_variable = aor1776_hre_emperor_called_initiator
  if = { limit = { scope:hre_military_emperor = { NOT = { is_diplomatic_play_ally_of = scope:initiator } } } add_initiator_backers = { scope:hre_military_emperor } }
 }
 if = { limit = { scope:initiator = { aor1776_hre_member = yes } scope:target = { aor1776_hre_member = yes }
  NOT = { scope:target = scope:hre_military_emperor } NOT = { scope:initiator = scope:hre_military_emperor }
  NOT = { has_variable = aor1776_hre_internal_neutrality_applied } }
  set_variable = aor1776_hre_internal_neutrality_applied
  if = { limit = { scope:hre_military_emperor = { is_diplomatic_play_ally_of = scope:initiator } } remove_initiator_backers = { scope:hre_military_emperor } }
  if = { limit = { scope:hre_military_emperor = { is_diplomatic_play_ally_of = scope:target } } remove_target_backers = { scope:hre_military_emperor } }
 }
'''
 for t in members:
  for side,enemy in [('initiator','target'),('target','initiator')]:
   special=' OR = { scope:hre_military_emperor.power_bloc ?= { has_principle = principle:aor1776_hre_circles_3 } is_diplomatic_play_type = dp_aor1776_hre_restitution is_diplomatic_play_type = dp_aor1776_hre_subject_release }' if side=='initiator' else 'scope:hre_military_emperor.power_bloc ?= { has_principle = principle:aor1776_hre_circles_3 }'
   defense+=f'''if = {{ limit = {{ scope:{side} = scope:hre_military_emperor scope:{enemy} = {{ aor1776_hre_member = no }} {special}
    NOT = {{ has_variable = aor1776_hre_called_{side}_{t} }} c:{t} ?= {{ aor1776_hre_member = yes NOT = {{ aor1776_hre_emperor = yes }}
     NOT = {{ is_subject_of = scope:{enemy} }} NOT = {{ top_overlord ?= scope:{enemy} }} }} }}
    set_variable = aor1776_hre_called_{side}_{t}
    if = {{ limit = {{ c:{t} = {{ NOT = {{ is_diplomatic_play_ally_of = scope:{side} }} NOT = {{ is_diplomatic_play_ally_of = scope:{enemy} }} }} }} add_{side}_backers = {{ c:{t} }} }}
   }}
'''
 defense+=' remove_variable = aor1776_hre_adjusting_backers\n}'
 files[EF]=replace_node(files[EF],'aor1776_hre_defend_external_attack',block('aor1776_hre_defend_external_attack',defense))
 # Country-target liberation must target the estate, with its overlord as
 # stakeholder. Native contestion then refers to THAT estate, not Stockholm.
 files[WG]=child(files[WG],'aor1776_hre_subject_release','possible','possible = { always = no } # Legacy saves only; replaced after new goals are verified.')
 files[WG]+=block(GOAL,'''icon = "gfx/interface/icons/war_goals/aor1776_hre_subject_release.dds"
kind = liberate_subject
settings = { overlord_is_stakeholder targets_enemy_subject has_other_stakeholder validate_conflicts_war_goals_all validate_conflicts_existing_subject }
execution_priority = 58
contestion_type = control_half_target_country_states
target_type = country
possible = { aor1776_hre_emperor = yes scope:target_country = { aor1776_hre_member = yes is_subject = yes top_overlord ?= { aor1776_hre_member = no has_variable = aor1776_hre_release_refused } } }
valid = { aor1776_hre_emperor = yes scope:target_country = { aor1776_hre_member = yes overlord = scope:stakeholder } }
maneuvers = { value = 20 }
infamy = { value = 0 }
on_enforced = {
 scope:target_country = { save_scope_as = hre_freed_estate save_scope_as = hre_holder aor1776_hre_snapshot_one_subject = yes }
 if = { limit = { scope:target_country = { exists = var:aor1776_hre_liberation_holder } }
  scope:target_country.var:aor1776_hre_liberation_holder = { save_scope_as = hre_reply_holder }
 } else = { scope:stakeholder = { save_scope_as = hre_reply_holder } }
 scope:target_country = {
  aor1776_hre_return_released_subject_provinces = yes
  if = { limit = { is_subject = no NOT = { is_in_same_power_bloc = global_var:aor1776_hre_emperor_country } }
   join_power_bloc = global_var:aor1776_hre_emperor_country
  }
  if = { limit = { is_subject = no NOT = { is_in_same_power_bloc = global_var:aor1776_hre_emperor_country } } set_variable = aor1776_hre_release_bloc_pending }
  remove_variable = aor1776_hre_liberation_holder
 }
 # Only the selected goal is enforced. The separate country-wide diplomatic
 # request has its own package effect; a single-subject war goal must not.
 trigger_event = { id = aor1776_hre.35 popup = yes }
}
ai = { is_significant_demand = yes }''')
 files[EF]+=block('aor1776_hre_snapshot_one_subject','\n'.join(f'if = {{ limit = {{ c:{t} ?= this }} save_scope_as = hre_reply_subject_{t} }}' for t in members))
 # The engine creates the selected subject's initial goal natively. Do not
 # expand it into all captives. has_war_goal is WAR-only, not diplomatic-play
 # scoped: the former weekly loop therefore added duplicate goals forever.
 # Keep this compatibility effect solely for bounded captive-side correction.
 prepare='''if = { limit = { is_diplomatic_play_type = dp_aor1776_hre_subject_release initiator = { aor1776_hre_emperor = yes }
 NOT = { has_variable = aor1776_hre_liberation_prepared } }
 initiator = { save_scope_as = initiator } target = { save_scope_as = target save_scope_as = hre_foreign_holder }
 if = { limit = { scope:target = { aor1776_hre_member = yes is_subject = yes } } scope:target.top_overlord = { save_scope_as = hre_foreign_holder } }
 set_variable = aor1776_hre_liberation_prepared
'''
 for t in members:
  prepare+=f'''if = {{ limit = {{ c:{t} ?= {{ aor1776_hre_member = yes is_subject_of = scope:hre_foreign_holder }} }}
   c:{t} = {{ set_variable = {{ name = aor1776_hre_liberation_holder value = scope:hre_foreign_holder days = 3650 }} }}
   # Repair old mistaken backing once, not on each join notification.
   if = {{ limit = {{ NOT = {{ has_variable = aor1776_hre_captive_corrected_{t} }} }}
    set_variable = aor1776_hre_captive_corrected_{t}
    if = {{ limit = {{ c:{t} = {{ is_diplomatic_play_ally_of = scope:initiator }} }} remove_initiator_backers = {{ c:{t} }} }}
    if = {{ limit = {{ c:{t} = {{ NOT = {{ is_diplomatic_play_ally_of = scope:target }} }} }} add_target_backers = {{ c:{t} }} }}
   }}
  }}
'''
 prepare+='}'
 files[EF]+=block('aor1776_hre_prepare_liberation_goals',prepare)
 files[DP]=child(files[DP],'dp_aor1776_hre_subject_release','war_goal','war_goal = '+GOAL)
 files[DP]=child(files[DP],'dp_aor1776_hre_subject_release','possible','''possible = { aor1776_hre_emperor = yes aggressive_diplomatic_plays_permitted = yes
scope:target_country = { aor1776_hre_member = yes is_subject = yes top_overlord ?= { aor1776_hre_member = no has_variable = aor1776_hre_release_refused } }
diplomatic_play_has_no_relations_blocker_with_overlord = yes }''')
 weekly='on_weekly_pulse = { initiator = { save_scope_as = initiator } target = { save_scope_as = target } aor1776_hre_prepare_liberation_goals = yes aor1776_hre_defend_external_attack = yes }'
 for key in ['dp_aor1776_hre_subject_release','dp_aor1776_hre_restitution']:
  files[DP]=child(files[DP],key,'on_weekly_pulse',weekly)
  files[DP]=child(files[DP],key,'initiator_can_add_war_goals','initiator_can_add_war_goals = yes')
 files[OA]=append_inside(files[OA],'aor1776_hre_defense_hook','')
 n=next(n for n in cw.parse(files[OA]) if n.key=='aor1776_hre_defense_hook').children('effect')[0]
 files[OA]=edits(files[OA],[(n.start,n.end,files[OA][n.start:n.end].replace('aor1776_hre_defend_external_attack = yes','aor1776_hre_prepare_liberation_goals = yes aor1776_hre_defend_external_attack = yes'))])
 L(GOAL,'Liberation of an imperial estate','Libération d’un État impérial')
 L('war_goal_'+GOAL, 'Liberation of an imperial estate','Libération d’un État impérial')
 L('war_goal_'+GOAL+'_type_name','Liberation of an imperial estate','Libération d’un État impérial')
 L('war_goal_'+GOAL+'_name',"Liberate [SCOPE.sCountry('target_country').GetName]","Libérer [SCOPE.sCountry('target_country').GetName]")
 L('war_goal_'+GOAL+'_desc',"Free [SCOPE.sCountry('target_country').GetName] from its overlord. Occupation requirements concern the targeted estate, not the external overlord’s capital.","Libérer [SCOPE.sCountry('target_country').GetName] de son suzerain. Les exigences d’occupation concernent l’État visé, et non la capitale du suzerain extérieur.")
 L('war_goal_'+GOAL+'_on_enforced',"[SCOPE.sCountry('target_country').GetName] becomes independent; its wrongly held registered imperial provinces are restored and its imperial membership is re-established.","[SCOPE.sCountry('target_country').GetName] devient indépendant ; ses provinces impériales enregistrées détenues indûment sont restituées et son appartenance impériale est rétablie.")
 L('dp_aor1776_hre_subject_release_tooltip','Select an imperial subject of the refusing external power. Each targeted subject receives its own primary liberation goal. Occupy the targeted estates, not the foreign capital.','Sélectionner un sujet impérial de la puissance extérieure ayant refusé. Chaque sujet visé reçoit son propre objectif principal de libération. Occuper les États visés, et non la capitale étrangère.')
 # Native accept_score examples (join/invite bloc, violate sovereignty) use
 # scope:actor for the proposer and ROOT for the evaluating recipient. The
 # old scope:target compared the recipient to itself and read its own bloc.
 values=block('aor1776_hre_foreign_allied_strength','''value = 0
every_scope_ally = { add = army_power_projection }
min = 0''')
 values+=block('aor1776_hre_imperial_available_strength','''value = army_power_projection
power_bloc ?= { every_power_bloc_member = { if = { limit = { aor1776_hre_member = yes is_power_bloc_leader = no NOT = { top_overlord ?= { aor1776_hre_member = no } } } add = army_power_projection } } }
min = 1''')
 score='''value = 0
add = { value = -25 desc = aor1776_hre_accept_base }
add = { value = "relations(scope:target)" multiply = 0.5 desc = aor1776_hre_accept_relations }
add = { value = "scope:target.ai_army_comparison(root)" multiply = 2 min = -50 max = 50 desc = aor1776_hre_accept_army }
add = { value = aor1776_hre_foreign_allied_strength divide = { value = scope:target.aor1776_hre_imperial_available_strength min = 1 } multiply = -40 min = -60 max = 0 desc = aor1776_hre_accept_allies }
if = { limit = { scope:target.power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } }
 add = { value = scope:target.power_bloc.current_cohesion_number subtract = 50 multiply = 0.75 desc = aor1776_hre_accept_cohesion }
}
if = { limit = { owes_obligation_to = scope:target } add = { value = 60 desc = aor1776_hre_accept_obligation } }
'''
 score=score.replace('scope:target','scope:actor')
 values+=block('aor1776_hre_external_acceptance',score)
 files[VALUES]=values
 for key in ['aor1776_hre_request_subject_release','aor1776_hre_request_restitution']:
  files[DA]=child(files[DA],key,'requires_approval','requires_approval = yes')
  scoreblock=score if key.endswith('subject_release') else '''if = { limit = { aor1776_hre_member = yes NOT = { scope:actor = { owes_obligation_to = root } } }
 value = 0 add = { value = 1000 desc = aor1776_hre_accept_imperial_duty }
} else = { '''+score+' }'
  ai=next(n for n in cw.parse(files[DA]) if n.key==key).children('ai')[0]
  revised=child(files[DA][ai.start:ai.end],'ai','accept_score','accept_score = { '+scoreblock+' }')
  files[DA]=edits(files[DA],[(ai.start,ai.end,revised)])
 # Territorial demand now uses the same native approval/preview, not a hidden
 # 60/40 event roll disconnected from the displayed score.
 files[DA]=child(files[DA],'aor1776_hre_request_restitution','accept_effect','''accept_effect = {
 scope:second_state = { aor1776_hre_preview_provinces = yes }
 hidden_effect = {
  save_scope_as = hre_request_emperor scope:target_country = { save_scope_as = hre_holder save_scope_as = hre_reply_holder }
  scope:second_state = { save_scope_as = hre_request_state aor1776_hre_snapshot_reply_provinces = yes }
  aor1776_hre_return_requested_provinces = yes
  trigger_event = { id = aor1776_hre.32 popup = yes }
 }
}''')
 files[DA]=child(files[DA],'aor1776_hre_request_restitution','decline_effect','''decline_effect = {
 save_scope_as = hre_request_emperor
 scope:target_country = { save_scope_as = hre_reply_holder
  scope:second_state = { save_scope_as = hre_request_state aor1776_hre_snapshot_reply_provinces = yes }
  if = { limit = { aor1776_hre_member = no } aor1776_hre_record_external_refusal = yes }
 }
 trigger_event = { id = aor1776_hre.33 popup = yes }
}''')
 # AI +1000 is not a rule binding human players. Keep a separate immediate
 # internal enforcement action for unprotected members, and native approval
 # only for outsiders or members protected by an obligation.
 n=next(n for n in cw.parse(files[DA]) if n.key=='aor1776_hre_request_restitution')
 internal=files[DA][n.start:n.end].replace('aor1776_hre_request_restitution = {','aor1776_hre_enforce_internal_restitution = {',1)
 internal=child(internal,'aor1776_hre_enforce_internal_restitution','requires_approval','requires_approval = no')
 internal=child(internal,'aor1776_hre_enforce_internal_restitution','potential','''potential = {
 NOT = { this = scope:target_country }
 NOT = { owes_obligation_to = scope:target_country }
 scope:target_country = { aor1776_hre_member = yes any_scope_state = { aor1776_hre_restitution_state = yes } }
}''')
 ni=next(n for n in cw.parse(internal));decline=ni.children('decline_effect')[0]
 internal=edits(internal,[(decline.start,decline.end,'')])
 files[DA]+=internal+'\n'
 files[DA]=child(files[DA],'aor1776_hre_request_restitution','potential','''potential = {
 NOT = { this = scope:target_country }
 OR = { scope:target_country = { aor1776_hre_member = no } owes_obligation_to = scope:target_country }
 scope:target_country = { any_scope_state = { aor1776_hre_restitution_state = yes } }
}''')
 L('aor1776_hre_enforce_internal_restitution','Enforce imperial restitution','Imposer la rétrocession impériale')
 L('aor1776_hre_enforce_internal_restitution_desc','An imperial estate must immediately restore the listed registered provinces. It cannot refuse unless the Emperor owes it an obligation; that case uses the approval-based request instead.','Un État impérial doit immédiatement restituer les provinces enregistrées indiquées. Il ne peut refuser que si l’empereur lui doit une obligation ; ce cas utilise alors la demande soumise à approbation.')
 # Snapshot the exact province set BEFORE transfer; split-state scopes can
 # disappear during transfers, so save each beneficiary and RGB flag instead.
 snap=''
 for r in ledger:
  snap+=f'''if = {{ limit = {{ c:{r['beneficiary']} ?= {{ aor1776_hre_member = yes }} p:{r['rgb']}.state ?= this NOT = {{ owner = c:{r['beneficiary']} }} }}
   set_variable = aor1776_hre_reply_dummy # Country/state variables are NOT used for the message.
   save_scope_as = hre_reply_province_{r['rgb']}
   c:{r['beneficiary']} = {{ save_scope_as = hre_reply_owner_{r['rgb']} }}
  }}
'''
 snap=snap.replace('   set_variable = aor1776_hre_reply_dummy # Country/state variables are NOT used for the message.\n','')
 files[EF]+=block('aor1776_hre_snapshot_reply_provinces',snap)
 # Record whether this refusal actually charged infamy; repeated refusals
 # within the protected period must not be described as a new penalty.
 for key in ['aor1776_hre_record_release_refusal','aor1776_hre_record_external_refusal']:
  n=next(n for n in cw.parse(files[EF]) if n.key==key)
  revised=files[EF][n.start:n.end].replace('change_infamy = 5','change_infamy = 5 save_scope_as = hre_reply_new_infamy_holder')
  files[EF]=edits(files[EF],[(n.start,n.end,revised)])
 L('aor1776_hre_reply_infamy',"[SCOPE.sCountry('hre_reply_new_infamy_holder').GetName] received 5 infamy for this first refusal. The imperial casus belli lasts ten years; existing truces remain binding.","[SCOPE.sCountry('hre_reply_new_infamy_holder').GetName] a reçu 5 points d’infamie pour ce premier refus. Le casus belli impérial dure dix ans ; les trêves existantes restent applicables.")
 reply='if = { limit = { exists = scope:hre_reply_new_infamy_holder } custom_tooltip = aor1776_hre_reply_infamy }\n'
 for t in members:
  reply+=f'if = {{ limit = {{ exists = scope:hre_reply_subject_{t} }} custom_tooltip = aor1776_hre_reply_line_{t} }}\n'
 for r in ledger:
  rgb=r['rgb'];key='aor1776_hre_reply_rgb_'+rgb
  L(key,f"{rgb} → [SCOPE.sCountry('hre_reply_owner_{rgb}').GetName]",f"{rgb} → [SCOPE.sCountry('hre_reply_owner_{rgb}').GetName]")
  reply+=f'if = {{ limit = {{ exists = scope:hre_reply_owner_{rgb} }} custom_tooltip = {key} }}\n'
 files[EF]+=block('aor1776_hre_reply_details',reply)
 # Goal settlement snapshot is before the mutable transfer.
 n=next(n for n in cw.parse(files[WG]) if n.key=='aor1776_hre_restitution').children('on_enforced')[0]
 raw=files[WG][n.start:n.end].replace('save_scope_as = hre_request_state','save_scope_as = hre_request_state aor1776_hre_snapshot_reply_provinces = yes')
 files[WG]=edits(files[WG],[(n.start,n.end,raw)])
 # Meaningful acknowledgement tooltips describe ALREADY applied outcomes;
 # they never repeat transfers, infamy or emancipation on clicking the button.
 descriptions={
 30:("[SCOPE.sCountry('hre_reply_holder').GetName] has released the imperial estates listed in our council’s settlement. Their liberty and registered territorial rights have been restored.","[SCOPE.sCountry('hre_reply_holder').GetName] a libéré les États impériaux désignés par notre conseil. Leur liberté et leurs droits territoriaux enregistrés ont été rétablis."),
 31:("[SCOPE.sCountry('hre_reply_holder').GetName] has rejected the liberation demand. The council may now pursue an imperial liberation play, once any truce has expired.","[SCOPE.sCountry('hre_reply_holder').GetName] a rejeté la demande de libération. Le conseil peut désormais engager une manœuvre de libération impériale, une fois toute trêve expirée."),
 32:("[SCOPE.sCountry('hre_reply_holder').GetName] has restored the registered provinces to their lawful imperial holders. The settlement’s exact territories appear below.","[SCOPE.sCountry('hre_reply_holder').GetName] a restitué les provinces enregistrées à leurs titulaires impériaux légitimes. Les territoires précis du règlement sont indiqués ci-dessous."),
 33:("[SCOPE.sCountry('hre_reply_holder').GetName] has rejected the territorial summons. An external holder’s refusal authorises restitution proceedings; a protected imperial member retains the right to refuse.","[SCOPE.sCountry('hre_reply_holder').GetName] a rejeté la sommation territoriale. Le refus d’un détenteur extérieur ouvre la voie à une rétrocession ; un membre impérial protégé conserve son droit de refus."),
 34:("[SCOPE.sCountry('hre_reply_holder').GetName] has submitted to the imperial settlement. The subjects and registered territories concerned are recorded below.","[SCOPE.sCountry('hre_reply_holder').GetName] s’est soumis au règlement impérial. Les sujets et territoires enregistrés concernés sont consignés ci-dessous."),
 35:("[SCOPE.sCountry('hre_freed_estate').GetName] is released from foreign overlordship. The settlement restores its imperial standing and returns only those registered provinces it held contrary to other estates’ rights.","[SCOPE.sCountry('hre_freed_estate').GetName] est libéré de la suzeraineté étrangère. Le règlement rétablit sa place dans l’Empire et ne restitue que les provinces enregistrées détenues en violation des droits d’autres États.")}
 files[EV]+=block('aor1776_hre.35','''type = country_event placement = root
title = aor1776_hre.35.t desc = aor1776_hre.35.d flavor = aor1776_hre.35.f
event_image = { video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }
option = { name = aor1776_hre.ack default_option = yes }''')
 L('aor1776_hre.35.t','An imperial estate regains its liberty','Un État impérial retrouve sa liberté')
 flavors={
 1:('He left nine places for the seals, and a tenth for the silence of the dead Emperor. No envoy wished to speak first.','Il réserva neuf places aux sceaux, et une dixième au silence de l’empereur mort. Aucun envoyé ne voulait parler le premier.'),
 20:('The border had moved on the map, but not in the old register. The envoy set both upon the table and waited.','La frontière avait bougé sur la carte, mais non dans le vieux registre. L’envoyé posa les deux sur la table et attendit.'),
 21:('Beneath the foreign seal lay three smaller impressions. The clerk traced each one with a finger, as if freeing a name from its wax.','Sous le sceau étranger reposaient trois empreintes plus petites. Le clerc les suivit du doigt, comme pour libérer un nom de sa cire.'),
 30:('At dawn, the city gates opened without a shot. The messenger read the decree twice; the second time, the crowd answered.','À l’aube, les portes de la ville s’ouvrirent sans un coup de feu. Le messager lut deux fois le décret ; à la seconde, la foule répondit.'),
 31:('The letter returned with its seal unbroken. In the council chamber, the rustle of paper sounded louder than an insult.','La lettre revint, son sceau intact. Dans la salle du conseil, le froissement du papier retentit plus fort qu’une insulte.'),
 32:('The surveyor rubbed out the latest line. Beneath it, faint but stubborn, the older boundary remained.','L’arpenteur effaça le trait le plus récent. Dessous, pâle mais obstinée, demeurait l’ancienne frontière.'),
 33:('The envoy folded the rejected summons. Outside, a groom held his horse; inside, no one offered him a chair.','L’envoyé replia la sommation rejetée. Dehors, un palefrenier retenait son cheval ; dedans, personne ne lui offrit de chaise.'),
 34:('When the final seal cooled, the clerk carried the register back to its shelf. For once, the ink and the border agreed.','Lorsque le dernier sceau eut refroidi, le clerc remit le registre sur son étagère. Pour une fois, l’encre et la frontière s’accordaient.'),
 35:('The old banner rose slowly over the square. No one cheered until its shadow reached the courthouse steps.','La vieille bannière s’éleva lentement au-dessus de la place. Nul n’acclama avant que son ombre atteignît les marches du tribunal.'),
 41:('They removed the empty chair from the wall and brought it back to the council table. Its owner had never ceased to claim his place.','On retira la chaise vide du mur pour la remettre à la table du conseil. Son propriétaire n’avait jamais cessé de réclamer sa place.'),
 60:('Each envoy brought a different map. By nightfall, they had begun to argue over a single page.','Chaque envoyé avait apporté une carte différente. À la nuit tombée, ils avaient commencé à débattre d’une seule page.'),
 61:('The prince kept his keys, his court and his guards. Only the oath at the bottom of the parchment had changed.','Le prince conserva ses clefs, sa cour et ses gardes. Seul le serment au bas du parchemin avait changé.'),
 62:('Orders now arrived beneath the same eagle. The old seals remained, but the clerk no longer asked which road the letter should take.','Les ordres arrivaient désormais sous le même aigle. Les vieux sceaux demeuraient, mais le clerc ne demandait plus quel chemin devait prendre la lettre.'),
 63:('The shelves still bore the names of the former courts. One register lay open upon the desk; for the first time, it named them all.','Les étagères portaient encore les noms des anciennes cours. Un registre ouvert reposait sur le bureau ; pour la première fois, il les nommait toutes.')}
 for num,(en,fr) in flavors.items():
  key='aor1776_hre.'+str(num)
  files[EV]=child(files[EV],key,'flavor','flavor = '+key+'.f')
  L(key+'.f','#italic “'+en+'”#! — The Letters of the Imperial Clerk (imaginary novel).','#italic « '+fr+' »#! — Les lettres du greffier impérial (roman imaginaire).')
  opt=next(n for n in cw.parse(files[EV]) if n.key==key).children('option')[0]
  if num in descriptions:
   den,dfr=descriptions[num];L(key+'.d',den,dfr)
   L(key+'.result',den+'\nThe following list records this settlement, not a new action:',dfr+'\nLa liste suivante décrit ce règlement, pas une nouvelle action :')
   files[EV]=edits(files[EV],[(opt.end-1,opt.end-1,'\n custom_tooltip = '+key+'.result\n aor1776_hre_reply_details = yes\n')])
  elif num>=60:
   tooltip='je_aor1776_hre_centralization_status' if num==60 else 'aor1776_hre_centralize_'+str(num-60)+'_desc'
   files[EV]=edits(files[EV],[(opt.end-1,opt.end-1,'\n custom_tooltip = '+tooltip+'\n')])
  elif num==41:
   files[EV]=edits(files[EV],[(opt.end-1,opt.end-1,'\n custom_tooltip = aor1776_hre.41.d\n')])
 # All visible options of recipient events list the still-applicable targets.
 for num,effect in [(20,'scope:hre_request_state ?= { aor1776_hre_preview_provinces = yes }'),(21,'aor1776_hre_preview_subjects = yes')]:
  n=next(n for n in cw.parse(files[EV]) if n.key==f'aor1776_hre.{num}')
  for o in reversed(n.children('option')):
   changes=[(o.end-1,o.end-1,'\n '+effect+'\n')]
   if num==20:
    opening=files[EV].index('{',o.start)+1
    changes.append((opening,opening,'\n hidden_effect = { scope:hre_request_state ?= { aor1776_hre_snapshot_reply_provinces = yes } }\n'))
   files[EV]=edits(files[EV],changes)
 # Real UI pact key differs from the diplomatic action description key.
 L('aor1776_imperial_obligation_pact_desc','An imperial constitutional bond without tribute or native overlordship. The estate retains diplomatic autonomy; leaving requires a successful secession play. Military duties follow the Imperial Circles and special restitution rules.','Un lien constitutionnel impérial sans tribut ni suzeraineté native. L’État conserve son autonomie diplomatique ; quitter l’Empire exige une sécession victorieuse. Les obligations militaires suivent les Cercles impériaux et les règles spéciales de rétrocession.')
 # Legacy atlas construction/migration. The final atlas_access pass now strips
 # these standalone UI additions; only the journal bitmap remains, alongside
 # the separately integrated native shader map mode.
 rel='gui/right_click_menu.gui';raw=files[rel]
 # Rebuild only our atlas additions, keeping native choices and unrelated
 # GUI changes. The old shortcut sat beyond the long scrollable native list.
 if 'aor1776_hre_atlas_open' in raw:
  original=(GAME/rel).read_text(encoding='utf-8-sig')
  a,b=map_menu_range(raw);x,y=map_menu_range(original)
  raw=edits(raw,[(a,b,original[x:y])])
  marker='name = "aor1776_hre_imperial_atlas"'
  if marker in raw:
   start=raw.rfind('widget = {',0,raw.index(marker))
   raw=edits(raw,[(start,gui_end(raw,start),'')])
   native_final_newlines=len(original)-len(original.rstrip('\n'))
   raw=raw.rstrip('\n')+'\n'*native_final_newlines
 if 'aor1776_hre_atlas_open' not in raw:
  menu_start,menu_end=map_menu_range(raw)
  start=raw.index('blockoverride "title_text"',menu_start)
  shortcut='''blockoverride "fixed_top" {
   button = { using = default_button_action size = { 350 45 } margin = { 16 6 }
   onclick = "[GetVariableSystem.Toggle('aor1776_hre_atlas_open')]"
   onclick = "[RightClickMenuManager.Close]"
   tooltip = "aor1776_hre_atlas_help"
   textbox = { position = { 8 0 } size = { 295 45 } text = "aor1776_hre_atlas_title" fontsize = 14 }
   icon = { parentanchor = right|vcenter position = { -5 0 } size = { 35 35 } texture = "gfx/interface/icons/map_mode_icons/aor1776_hre_territories.dds" }
   }
  }
  '''
  raw=edits(raw,[(start,start,shortcut)])
  raw+='''
widget = {
 name = "aor1776_hre_imperial_atlas"
 layer = confirmation
 parentanchor = center widgetanchor = center size = { 760 670 }
 visible = "[GetVariableSystem.Exists('aor1776_hre_atlas_open')]"
 background = { using = paper_bg }
 vbox = { position = { 20 15 } spacing = 10
  textbox = { size = { 720 40 } text = "aor1776_hre_atlas_title" using = fontsize_large }
  icon = { size = { 720 533 } texture = "gfx/interface/journal_entries/aor1776_hre_registered_map.dds" }
  textbox = { size = { 720 55 } text = "aor1776_hre_atlas_help" multiline = yes using = fontsize_medium }
 }
 button = { using = default_button_action parentanchor = top|right position = { -5 5 } size = { 35 35 }
  shortcut = "close_window"
  onclick = "[GetVariableSystem.Toggle('aor1776_hre_atlas_open')]"
  textbox = { size = { 35 35 } text = "×" }
 }
}
'''
 # A standalone widget definition in a context-menu file is not an instance
 # of the HUD. Mount the atlas as an actual child of the active ingame_hud.
 marker='name = "aor1776_hre_imperial_atlas"'
 start=raw.rfind('widget = {',0,raw.index(marker));end=gui_end(raw,start)
 popup=raw[start:end]
 original=(GAME/rel).read_text(encoding='utf-8-sig')
 raw=edits(raw,[(start,end,'')])
 raw=raw.rstrip('\n')+'\n'*(len(original)-len(original.rstrip('\n')))
 files[rel]=raw
 hud_rel='gui/ingame_hud.gui'
 hud_path=__import__('map2k_work').ROOT/hud_rel
 hud=(hud_path if hud_path.exists() else GAME/hud_rel).read_text(encoding='utf-8-sig')
 if marker in hud:
  start=hud.rfind('widget = {',0,hud.index(marker));end=gui_end(hud,start)
  hud=edits(hud,[(start,end,popup)])
 else:
  start=hud.rfind('widget = {',0,hud.index('name = "ingame_hud"'))
  opening=hud.index('{',start)+1
  hud=edits(hud,[(opening,opening,'\n'+popup+'\n')])
 files[hud_rel]=hud
 L('aor1776_hre_atlas_title','Imperial de jure territories — atlas','Territoires impériaux de jure — atlas')
 L('aor1776_hre_atlas_help','Yellow: registered imperial provinces, regardless of their current owner. This is a dedicated atlas, not a native main-map overlay. The imperial journal lists the current owners and clickable states.','Jaune : provinces impériales enregistrées, quel que soit leur propriétaire actuel. Il s’agit d’un atlas dédié, pas d’un filtre de la carte principale. Le journal impérial liste les propriétaires actuels et les États cliquables.')
 for suffix,en,fr in [
 ('base','Reluctance to surrender imperial holdings','Réticence à abandonner les possessions impériales'),
 ('relations','Relations with the Emperor','Relations avec l’empereur'),
 ('army','Military balance with the Emperor','Rapport de force militaire avec l’empereur'),
 ('allies','Military support of our allies','Soutien militaire de nos alliés'),
 ('cohesion','Cohesion of the imperial bloc','Cohésion du bloc impérial'),
 ('obligation','Obligation owed to the Emperor','Obligation due à l’empereur'),
 ('imperial_duty','Binding imperial territorial obligation','Obligation territoriale impériale contraignante')]:L('aor1776_hre_accept_'+suffix,en,fr)
 for lang,idx in [('english',0),('french',1)]:
  # Remove old duplicate keys before writing one authoritative value.
  for rel,raw in list(files.items()):
   if rel.startswith('localization/'+lang+'/'):
    files[rel]='\n'.join(line for line in raw.split('\n') if not any(re.match(r'\s*'+re.escape(k)+r':',line) for k in loc))
  files[f'localization/{lang}/1776_imperial_repairs_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[idx].replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())
 return files
