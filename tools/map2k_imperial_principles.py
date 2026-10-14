"""User-approved four-pillar constitution. Emit through the explicit patch only."""
import math
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2k_imperial_feedback import block,append_inside,replace_node,child,EF,EV,OA,ID
from map2k_work import ROOT,GAME
from map_1776_audit import effective

FAMILIES=['diet','circles','justice','administration']
GROUPS={'aor1776_hre_group_'+g:['aor1776_hre_'+g+'_'+str(i) for i in range(1,4)] for g in FAMILIES}
GROUP_FILE='common/power_bloc_principle_groups/1776_imperial_principles.txt'
PRINCIPLE_FILE='common/power_bloc_principles/1776_imperial_principles.txt'
VALUES_FILE='common/script_values/1776_imperial_reforms.txt'
REFORM_EFFECTS='common/scripted_effects/1776_imperial_reforms.txt'
TRIG='common/scripted_triggers/1776_imperial_constitution.txt'
IDENTITY='identity_aor1776_imperial_federation'

def existing(rel):
 p=ROOT/rel
 return (p if p.exists() else GAME/rel).read_text(encoding='utf-8-sig')

def augment_principles(files):
 loc={}
 def L(k,en,fr):loc[k]=(en,fr)
 institutions=sorted({n.key for p in effective(ROOT,GAME,'common/institutions') for n in cw.parse(p.read_text(encoding='utf-8-sig'))})
 names={'diet':('Perpetual Diet','Diète perpétuelle'),'circles':('Imperial Circles','Cercles impériaux'),'justice':('Imperial Justice','Justice impériale'),'administration':('Imperial Administration','Administration impériale')}
 groups='';principles=''
 for g,levels in GROUPS.items():
  primary='primary_for_identity = '+IDENTITY+'\n' if g.endswith('diet') else ''
  groups+=block(g,primary+'unlocking_identity = '+IDENTITY+'\nlevels = { '+' '.join(levels)+' }')
  family=g.removeprefix('aor1776_hre_group_');en,fr=names[family]
  L(g,en,fr);L(g+'_desc',en+' — three levels of imperial cooperation.',fr+' — trois niveaux de coopération impériale.')
  for i,p in enumerate(levels,1):
   participant='';leader=''
   if family=='diet':
    participant=f'country_improve_relations_speed_mult = {i*.1:.2f}'
    leader=f'country_influence_add = {[50,250,1000][i-1]}\ncountry_aor1776_hre_authority_per_estate_add = {i*5}'
   elif family=='circles':
    participant=f'building_mobilization_cost_mult = {-i*.05:.2f}\nmilitary_formation_mobilization_speed_mult = {i*.05:.2f}'
   elif family=='justice':
    participant=f'country_law_enactment_stall_mult = {-i*.1:.2f}\ncountry_law_enactment_speed_mult = {i*.05:.2f}'
   else:
    participant=f'country_bureaucracy_mult = {i*.05:.2f}\n'+'\n'.join(f'country_institution_cost_{inst}_mult = {-i*.1:.2f}' for inst in institutions)
   principles+=block(p,f'''icon = "gfx/interface/icons/principles_icons/aor1776_hre_{family}.dds"
background = "gfx/interface/icons/principles_icons/principle_tier_{i}.dds"
visible = {{ power_bloc ?= {{ has_identity = identity:{IDENTITY} }} }}
possible = {{ aor1776_hre_emperor = yes power_bloc ?= {{ has_identity = identity:{IDENTITY} current_cohesion_number > 40 }} }}
member_modifier = {{ {participant} }}
leader_modifier = {{ {leader} }}
ai_weight = {{ value = {100 if i==1 else 1000} }}''')
   L(p,en+' '+['I','II','III'][i-1],fr+' '+['I','II','III'][i-1])
   detail=['The Emperor defends all imperial members against outside powers.','Previous obligation, and the Emperor joins members’ offensive plays against outside powers.','Previous obligations, and members join the Emperor’s defensive and offensive plays against outside powers.'][i-1] if family=='circles' else 'Bonuses are the total for this level, not cumulative with lower tiers.'
   detailfr=['L’empereur défend tous les membres contre les puissances extérieures.','Obligation précédente, plus participation de l’empereur aux manœuvres offensives des membres contre les puissances extérieures.','Obligations précédentes, plus participation des membres aux manœuvres défensives et offensives de l’empereur contre les puissances extérieures.'][i-1] if family=='circles' else 'Les bonus sont les totaux de ce niveau, sans cumul avec les niveaux inférieurs.'
   L(p+'_desc',detail+' New principles require cohesion above 40. On a change of imperial country, the last-added group is lost, or the sole group loses one level without going below I.',detailfr+' Une cohésion supérieure à 40 est nécessaire pour choisir un principe. Au changement de pays impérial, le dernier groupe ajouté est perdu, ou le groupe unique recule d’un niveau sans descendre sous I.')
 files[GROUP_FILE]=groups;files[PRINCIPLE_FILE]=principles
 # Exactly these four families fill the imperial slots; other identities retain
 # all native choices. Preserve all fields of every upstream group.
 for source in effective(ROOT,GAME,'common/power_bloc_principle_groups'):
  rel='common/power_bloc_principle_groups/'+source.name
  if rel==GROUP_FILE:continue
  raw=files.get(rel,source.read_text(encoding='utf-8-sig'))
  for n in reversed(cw.parse(raw)):
   if n.key in GROUPS or not n.children('levels'):continue
   if IDENTITY not in [cw.scalar(x.value) for x in n.children('blocking_identity')]:
    raw=edits(raw,[(n.end-1,n.end-1,'\n blocking_identity = '+IDENTITY+'\n')])
  files[rel]=raw
 # Also reject individual tiers, including an upgrade of a legacy vanilla
 # group in a loaded save. Visibility alone is not an enforceable selection
 # rule; possible is guarded as well. Other identities keep every condition.
 guard='NOT = { exists = power_bloc power_bloc ?= { has_identity = identity:'+IDENTITY+' } }'
 approved={p for levels in GROUPS.values() for p in levels}
 for source in effective(ROOT,GAME,'common/power_bloc_principles'):
  rel='common/power_bloc_principles/'+source.name
  if rel==PRINCIPLE_FILE:continue
  raw=files.get(rel,source.read_text(encoding='utf-8-sig'))
  # Script AND/NOT evaluation does not short-circuit the missing-bloc link.
  # Migrate only our prior guard; leave native fields untouched.
  raw=raw.replace(guard.replace('power_bloc ?=', 'power_bloc ='),guard)
  for key in [n.key for n in cw.parse(raw) if n.key not in approved and n.children('icon')]:
   for field in ['visible','possible']:
    n=next(n for n in cw.parse(raw) if n.key==key)
    condition=n.children(field)
    if condition:
     c=condition[0]
     if guard not in raw[c.start:c.end]:raw=edits(raw,[(c.end-1,c.end-1,'\n '+guard+'\n')])
    else:raw=append_inside(raw,key,field+' = { '+guard+' }')
  files[rel]=raw
 identity=files[ID]
 for field in ['power_bloc_mandate_progress_per_great_power_member_add','power_bloc_mandate_progress_per_major_power_member_add','power_bloc_mandate_progress_per_minor_power_member_add']:
  identity=identity.replace(field+' = '+{'power_bloc_mandate_progress_per_great_power_member_add':'10','power_bloc_mandate_progress_per_major_power_member_add':'5','power_bloc_mandate_progress_per_minor_power_member_add':'2'}[field],field+' = 0')
 files[ID]=child(identity,IDENTITY,'mandate_progress','mandate_progress = aor1776_hre_authority_progress')
 history='common/history/power_blocs/00_power_blocs.txt'
 aus=next(n for n in cw.walk(cw.parse(files[history])) if n.key=='c:AUS')
 body=files[history][aus.start:aus.end].replace('principle = principle_internal_trade_3','principle = aor1776_hre_diet_1')
 files[history]=edits(files[history],[(aus.start,aus.end,body)])
 # No native logarithm operator has been verified. Evaluate ln(N) exactly at
 # integer membership counts with a lookup, not an invented script command.
 # The frozen estate roster has <=37 members; cover 1..128 and cap safely above.
 logarithm='value = 1\n'
 for n in range(2,129):logarithm+=f'if = {{ limit = {{ num_power_bloc_members = {n} }} add = {math.log(n):.10f} }}\n'
 logarithm+=f'if = {{ limit = {{ num_power_bloc_members > 128 }} add = {math.log(128):.10f} }}\n'
 values=block('aor1776_hre_log_divisor',logarithm)
 values+=block('aor1776_hre_authority_progress','''value = 0
if = { limit = { current_cohesion_number > 40 }
 add = { value = current_cohesion_number subtract = 40 min = 0 desc = aor1776_hre_authority_from_cohesion }
 divide = { value = aor1776_hre_log_divisor desc = aor1776_hre_authority_from_size }
}
min = 0''')
 values+=block('aor1776_hre_estate_count','value = 0\nevery_power_bloc_member = { if = { limit = { aor1776_hre_member = yes is_power_bloc_leader = no } add = 1 } }')
 files[VALUES_FILE]=values
 files['common/modifier_type_definitions/1776_imperial_modifier_types.txt']+=block('country_aor1776_hre_authority_per_estate_add','decimals = 0\ncolor = good\ngame_data = { ai_value = 0 }')
 files['common/static_modifiers/1776_imperial_reforms.txt']=block('aor1776_hre_estates_authority','icon = "gfx/interface/icons/timed_modifier_icons/aor1776_hre_registered_territory.dds"\ncountry_authority_add = 1')
 L('country_aor1776_hre_authority_per_estate_add','Authority per other imperial member','Autorité par autre membre impérial')
 L('aor1776_hre_estates_authority','Authority of the imperial estates','Autorité des États impériaux')
 L('aor1776_hre_estates_authority_desc','The Diet gives the Emperor 5, 10 or 15 authority per other recognised member actually in the bloc. Non-imperial subjects are excluded.','La Diète donne à l’empereur 5, 10 ou 15 d’autorité par autre membre reconnu effectivement dans le bloc. Les sujets non impériaux sont exclus.')
 L('aor1776_hre_authority_from_cohesion','Imperial authority from cohesion above 40','Autorité impériale issue de la cohésion au-dessus de 40')
 L('aor1776_hre_authority_from_size','Coordination cost: 1 + ln(number of members)','Coût de coordination : 1 + ln(nombre de membres)')
 # Group addition is tracked independently of upgrades. Native principle
 # selection cooldown is 90 days, so daily sampling distinguishes normal buys.
 tracking='''if = { limit = { has_identity = identity:identity_aor1776_imperial_federation }
 if = { limit = { NOT = { has_global_variable = aor1776_hre_principle_serial } } set_global_variable = { name = aor1776_hre_principle_serial value = 0 } }
'''
 for g,ls in GROUPS.items():
  key='aor1776_hre_order_'+g
  tracking+=f'''if = {{ limit = {{ has_principle_group = principle_group:{g} NOT = {{ has_global_variable = {key} }} }}
 change_global_variable = {{ name = aor1776_hre_principle_serial add = 1 }} set_global_variable = {{ name = {key} value = global_var:aor1776_hre_principle_serial }} }}
else_if = {{ limit = {{ NOT = {{ has_principle_group = principle_group:{g} }} }} remove_global_variable = {key} }}
'''
 tracking+='}'
 effects=block('aor1776_hre_track_principle_order',tracking)
 loss='''set_variable = { name = aor1776_hre_saved_group_count value = 0 }
set_variable = { name = aor1776_hre_last_saved_order value = -1 }
remove_variable = aor1776_hre_loss_group
'''
 for j,(g,ls) in enumerate(GROUPS.items(),1):
  flags='OR = { '+' '.join('has_variable = aor1776_hre_saved_'+p for p in ls)+' }'
  loss+=f'''if = {{ limit = {{ {flags} }} change_variable = {{ name = aor1776_hre_saved_group_count add = 1 }}
 if = {{ limit = {{ has_global_variable = aor1776_hre_order_{g} global_var:aor1776_hre_order_{g} > var:aor1776_hre_last_saved_order }}
 set_variable = {{ name = aor1776_hre_last_saved_order value = global_var:aor1776_hre_order_{g} }} set_variable = {{ name = aor1776_hre_loss_group value = {j} }} }} }}
'''
 for j,(g,ls) in enumerate(GROUPS.items(),1):
  loss+=f'if = {{ limit = {{ var:aor1776_hre_loss_group ?= {j} }}\n'
  loss+='if = { limit = { var:aor1776_hre_saved_group_count > 1 } '+ ' '.join('remove_variable = aor1776_hre_saved_'+p for p in ls)+' }\n'
  loss+=f'''else_if = {{ limit = {{ has_variable = aor1776_hre_saved_{ls[2]} }} remove_variable = aor1776_hre_saved_{ls[2]} set_variable = aor1776_hre_saved_{ls[1]} }}
else_if = {{ limit = {{ has_variable = aor1776_hre_saved_{ls[1]} }} remove_variable = aor1776_hre_saved_{ls[1]} set_variable = aor1776_hre_saved_{ls[0]} }}
}}\n'''
 effects+=block('aor1776_hre_apply_succession_loss_to_snapshot',loss)
 # Migration is limited to the original single Internal Trade group, not
 # arbitrary old-save choices with an unknowable acquisition chronology.
 controller='''if = { limit = { exists = global_var:aor1776_hre_emperor_country }
 every_country = { limit = { NOT = { aor1776_hre_emperor = yes } has_modifier = aor1776_hre_estates_authority } remove_modifier = aor1776_hre_estates_authority remove_variable = aor1776_hre_applied_authority }
 global_var:aor1776_hre_emperor_country = {
  if = { limit = { is_power_bloc_leader = yes power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } }
   power_bloc = {
    if = { limit = { has_principle = principle:principle_internal_trade_3 NOT = { has_global_variable = aor1776_hre_principle_serial } }
     remove_principle = principle_internal_trade_3 add_principle = aor1776_hre_diet_1
    }
    aor1776_hre_track_principle_order = yes
   }
   set_variable = { name = aor1776_hre_ui_authority_gain value = power_bloc.aor1776_hre_authority_progress }
   set_variable = { name = aor1776_hre_ui_estates value = power_bloc.aor1776_hre_estate_count }
   set_variable = { name = aor1776_hre_diet_authority value = var:aor1776_hre_ui_estates }
   change_variable = { name = aor1776_hre_diet_authority multiply = modifier:country_aor1776_hre_authority_per_estate_add }
   if = { limit = { NOT = { var:aor1776_hre_applied_authority ?= var:aor1776_hre_diet_authority } }
    remove_modifier = aor1776_hre_estates_authority
    if = { limit = { var:aor1776_hre_diet_authority > 0 } add_modifier = { name = aor1776_hre_estates_authority multiplier = var:aor1776_hre_diet_authority } }
    set_variable = { name = aor1776_hre_applied_authority value = var:aor1776_hre_diet_authority }
   }
   if = { limit = { NOT = { has_global_variable = aor1776_hre_reform_stage } } set_global_variable = { name = aor1776_hre_reform_stage value = 0 } }
   if = { limit = { aor1776_hre_four_pillars_max = yes NOT = { has_global_variable = aor1776_hre_unified } NOT = { has_journal_entry = je_aor1776_hre_centralization } } add_journal_entry = { type = je_aor1776_hre_centralization } }
  }
 }
}'''
 effects+=block('aor1776_hre_reform_controller',controller)
 files[REFORM_EFFECTS]=effects
 # Snapshot loss is prepared before creation, never applied to the old bloc.
 install=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_install_elected_country')
 raw=files[EF][install.start:install.end]
 raw=raw.replace('limit = { is_power_bloc_leader = yes power_bloc ?=', 'limit = { this = scope:hre_old_imperial_country is_power_bloc_leader = yes power_bloc ?=',1)
 raw=raw.replace('aor1776_hre_snapshot_principles = yes','aor1776_hre_track_principle_order = yes\n   aor1776_hre_snapshot_principles = yes')
 raw=raw.replace('set_variable = aor1776_hre_creation_permitted','''if = { limit = { has_global_variable = aor1776_hre_election_pending NOT = { this = scope:hre_old_imperial_country } }
   aor1776_hre_apply_succession_loss_to_snapshot = yes
  }
  set_variable = aor1776_hre_creation_permitted''')
 files[EF]=edits(files[EF],[(install.start,install.end,raw)])
 for key in ['aor1776_hre_initialize','aor1776_hre_finish_investiture']:
  files[EF]=append_inside(files[EF],key,'aor1776_hre_reform_controller = yes')
 # Reuse the existing single delayed daily guard, not a second world scan.
 files[EV]=files[EV].replace('aor1776_hre_restore_membership = yes','aor1776_hre_restore_membership = yes\n   aor1776_hre_reform_controller = yes')
 files[OA]=files[OA].replace('aor1776_hre_feedback_refresh = yes','aor1776_hre_feedback_refresh = yes\n   aor1776_hre_reform_controller = yes')
 files[TRIG]+=block('aor1776_hre_four_pillars_max','power_bloc ?= { has_identity = identity:'+IDENTITY+'\n'+'\n'.join('has_principle = principle:'+ls[2] for ls in GROUPS.values())+' }')
 # Scripted military obligations use the actual imperial bloc's principles;
 # native all-members alliance booleans would erase internal-war neutrality.
 defense='''if = { limit = { NOT = { has_variable = aor1776_hre_adjusting_backers } exists = global_var:aor1776_hre_emperor_country exists = scope:initiator exists = scope:target }
 set_variable = aor1776_hre_adjusting_backers
 global_var:aor1776_hre_emperor_country = { save_scope_as = hre_military_emperor }
 if = { limit = { scope:target = { aor1776_hre_member = yes } scope:initiator = { aor1776_hre_member = no } NOT = { scope:target = scope:hre_military_emperor }
  scope:hre_military_emperor.power_bloc ?= { has_principle_group = principle_group:aor1776_hre_group_circles } }
  add_target_backers = { scope:hre_military_emperor }
 }
 if = { limit = { scope:initiator = { aor1776_hre_member = yes } scope:target = { aor1776_hre_member = no } NOT = { scope:initiator = scope:hre_military_emperor }
  scope:hre_military_emperor.power_bloc ?= { OR = { has_principle = principle:aor1776_hre_circles_2 has_principle = principle:aor1776_hre_circles_3 } } }
  add_initiator_backers = { scope:hre_military_emperor }
 }
 if = { limit = { scope:initiator = { aor1776_hre_member = yes } scope:target = { aor1776_hre_member = yes }
  NOT = { scope:target = scope:hre_military_emperor } NOT = { scope:initiator = scope:hre_military_emperor } }
  remove_initiator_backers = { scope:hre_military_emperor } remove_target_backers = { scope:hre_military_emperor }
 }
 if = { limit = { scope:target = scope:hre_military_emperor scope:initiator = { aor1776_hre_member = no }
  scope:hre_military_emperor.power_bloc ?= { has_principle = principle:aor1776_hre_circles_3 } }
  every_country = { limit = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } } save_scope_as = hre_backer root = { add_target_backers = { scope:hre_backer } } }
 }
 if = { limit = { scope:initiator = scope:hre_military_emperor scope:target = { aor1776_hre_member = no }
  OR = { scope:hre_military_emperor.power_bloc ?= { has_principle = principle:aor1776_hre_circles_3 } is_diplomatic_play_type = dp_aor1776_hre_restitution is_diplomatic_play_type = dp_aor1776_hre_subject_release } }
  every_country = { limit = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } } save_scope_as = hre_backer root = { add_initiator_backers = { scope:hre_backer } } }
 }
 remove_variable = aor1776_hre_adjusting_backers
}'''
 files[EF]=replace_node(files[EF],'aor1776_hre_defend_external_attack',block('aor1776_hre_defend_external_attack',defense))
 L('aor1776_hre_reforms_ui',"Imperial authority gained weekly: [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.MakeScope.Var('aor1776_hre_ui_authority_gain').GetValue|2]\nNo gains or principle purchases at cohesion ≤40. Larger membership slows gains logarithmically; it never removes points.","Autorité impériale gagnée par semaine : [JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.MakeScope.Var('aor1776_hre_ui_authority_gain').GetValue|2]\nAucun gain ni achat de principe à une cohésion ≤40. Le nombre de membres ralentit le gain logarithmiquement, sans retirer de points.")
 gui='gui/journal_entry_widgets/1776_imperial_widgets.gui'
 files[gui]=files[gui].replace(' textbox = { using = fontsize_medium size = { 500 125 }',' textbox = { using = fontsize_medium size = { 500 95 } text = "aor1776_hre_reforms_ui" multiline = yes }\n textbox = { using = fontsize_medium size = { 500 125 }',1)
 centralize(files,L)
 # Native leadership rank rules remain unchanged outside this constitution.
 rel='common/scripted_rules/00_scripted_rules.txt';raw=existing(rel)
 if 'aor1776_hre_creation_permitted' not in raw:
  n=next(n for n in cw.parse(raw) if n.key=='can_lead_power_bloc')
  old=raw[n.start:n.end];body=old[old.index('{')+1:old.rfind('}')]
  raw=edits(raw,[(n.start,n.end,block('can_lead_power_bloc','OR = { '+body+' aor1776_hre_emperor = yes has_variable = aor1776_hre_creation_permitted }'))])
 files[rel]=raw
 # Once the actual country is unified, native monarchical succession takes
 # over: do not open an election among extinct estates.
 hook=next(n for n in cw.parse(files[OA]) if n.key=='aor1776_hre_death_hook')
 raw=files[OA][hook.start:hook.end].replace('limit = { has_variable = aor1776_hre_emperor_character','limit = { NOT = { has_global_variable = aor1776_hre_unified } has_variable = aor1776_hre_emperor_character',1)
 files[OA]=edits(files[OA],[(hook.start,hook.end,raw)])
 for lang,idx in [('english',0),('french',1)]:
  files[f'localization/{lang}/1776_imperial_reforms_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[idx].replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())
 return files

def centralize(files,L):
 """Player-controlled stages; no historical file changes or automatic annexation."""
 files[TRIG]+=block('aor1776_hre_reform_safe','''aor1776_hre_emperor = yes aor1776_hre_four_pillars_max = yes
NOT = { has_global_variable = aor1776_hre_election_open }
NOT = { has_global_variable = aor1776_hre_election_pending }
power_bloc ?= { current_cohesion_number >= 75 }
is_at_war = no is_diplomatic_play_committed_participant = no
NOT = { any_country = { aor1776_hre_member = yes
 OR = { is_at_war = yes is_diplomatic_play_committed_participant = yes
  NOT = { is_in_same_power_bloc = root }
  top_overlord ?= { aor1776_hre_member = no }
 } } }''')
 # Genuine native subject types, available to all imperial estate ranks.
 subject='';action=''
 for kind,base,level in [('protectorate','subject_type_protectorate',2),('crownland','subject_type_crown_land',1)]:
  raw=existing('common/subject_types/00_subject_types.txt');n=next(n for n in cw.parse(raw) if n.key==base);s=raw[n.start:n.end]
  key='subject_type_aor1776_hre_'+kind
  s=s.replace(base+' = {',key+' = {',1)
  s=child(s,key,'diplomatic_action','diplomatic_action = aor1776_hre_'+kind)
  for field,val in [('overlord_must_be_higher_rank','no'),('can_have_subjects','yes'),('breaks_if_subject_not_protected','no'),('use_for_release_country','no')]:s=child(s,key,field,field+' = '+val)
  ranks='great_power major_power minor_power insignificant_power unrecognized_major_power unrecognized_regional_power unrecognized_power'
  s=child(s,key,'valid_subject_ranks','valid_subject_ranks = { '+ranks+' }');s=child(s,key,'valid_overlord_ranks','valid_overlord_ranks = { '+ranks+' }')
  s=child(s,key,'valid_subject_country_types','valid_subject_country_types = { recognized unrecognized colonial }')
  s=child(s,key,'lower_autonomy_subject_type_alternatives','lower_autonomy_subject_type_alternatives = { subject_type_aor1776_hre_crownland }' if level==2 else 'lower_autonomy_subject_type_alternatives = {}')
  s=child(s,key,'higher_autonomy_subject_type_alternatives','higher_autonomy_subject_type_alternatives = { subject_type_aor1776_hre_protectorate }' if level==1 else 'higher_autonomy_subject_type_alternatives = {}')
  s=child(s,key,'same_autonomy_subject_type_alternatives','same_autonomy_subject_type_alternatives = {}')
  subject+=s+'\n'
  action+=block('aor1776_hre_'+kind,f'''groups = {{ general power_bloc }} texture = "gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_obligation.dds"
show_in_lens = no potential = {{ always = no }}
pact = {{ cost = 0 has_junior_participant = yes subject_type = {key} income_transfer = 0
 actor_can_break = {{ always = no }} target_can_break = {{ always = no }} }}
ai = {{ will_break = {{ always = no }} will_propose = {{ always = no }} }}''')
  L(key,'Imperial '+kind,'Protectorat impérial' if level==2 else 'Terre de la couronne impériale')
  L('aor1776_hre_'+kind,'Imperial '+kind,'Protectorat impérial' if level==2 else 'Terre de la couronne impériale')
  L('aor1776_hre_'+kind+'_desc','A genuine imperial dependency established by the centralization journal. No tribute. Secession requires a diplomatic play.','Une dépendance impériale native établie par le journal de centralisation. Aucun tribut. La sécession exige une manœuvre diplomatique.')
 files['common/subject_types/1776_imperial_reforms.txt']=subject
 files['common/diplomatic_actions/1776_imperial_subjects.txt']=action
 # Native subject relation directions: Emperor (senior ROOT) -> estate (junior).
 effects=''
 for stage,kind in [(1,'protectorate'),(2,'crownland')]:
  effects+=block('aor1776_hre_bind_'+kind,'''save_scope_as = hre_reform_emperor
every_country = { limit = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } }
 save_scope_as = hre_reform_estate
 if = { limit = { is_direct_subject_of = scope:hre_reform_emperor }
  change_subject_type = subject_type_aor1776_hre_'''+kind+'''
 }
 else = {
  if = { limit = { is_subject = yes top_overlord ?= { aor1776_hre_member = yes } } make_independent = yes }
  scope:hre_reform_emperor = { create_diplomatic_pact = { country = scope:hre_reform_estate type = aor1776_hre_'''+kind+''' } }
 }
}''')
  effects+=block('aor1776_hre_stage_'+str(stage),'''if = { limit = { aor1776_hre_reform_safe = yes global_var:aor1776_hre_reform_stage = '''+str(stage-1)+''' NOT = { has_variable = aor1776_hre_reform_cooldown } }
 aor1776_hre_bind_'''+kind+''' = yes
 if = { limit = { NOT = { any_country = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } NOT = { is_direct_subject_of = root is_subject_type = subject_type_aor1776_hre_'''+kind+''' } } } }
  set_global_variable = { name = aor1776_hre_reform_stage value = '''+str(stage)+''' }
  set_variable = { name = aor1776_hre_reform_cooldown days = 730 }
  trigger_event = { id = aor1776_hre.'''+str(60+stage)+''' popup = yes }
 }
}''')
 effects+=block('aor1776_hre_stage_3','''if = { limit = { aor1776_hre_reform_safe = yes global_var:aor1776_hre_reform_stage = 2 NOT = { has_variable = aor1776_hre_reform_cooldown }
 NOT = { any_country = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } NOT = { is_direct_subject_of = root is_subject_type = subject_type_aor1776_hre_crownland } } } }
 save_scope_as = hre_reform_emperor
 every_country = { limit = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } } set_variable = aor1776_hre_unification_selected }
 every_country = { limit = { has_variable = aor1776_hre_unification_selected }
  save_scope_as = hre_reform_estate scope:hre_reform_emperor = { annex = scope:hre_reform_estate }
 }
 set_global_variable = { name = aor1776_hre_reform_stage value = 3 }
 set_global_variable = aor1776_hre_unified
 remove_modifier = aor1776_hre_estates_authority remove_variable = aor1776_hre_applied_authority
 trigger_event = { id = aor1776_hre.63 popup = yes }
}''')
 files[REFORM_EFFECTS]+=effects
 je=block('je_aor1776_hre_centralization','''icon = "gfx/interface/icons/central_identity_pillars_icons/aor1776_imperial_federation_v2.dds"
is_shown_when_inactive = { aor1776_hre_emperor = yes aor1776_hre_four_pillars_max = yes NOT = { has_global_variable = aor1776_hre_unified } }
possible = { aor1776_hre_four_pillars_max = yes }
invalid = { aor1776_hre_emperor = no }
complete = { has_global_variable = aor1776_hre_unified }
immediate = { set_variable = { name = aor1776_hre_reform_cooldown days = 730 } trigger_event = { id = aor1776_hre.60 popup = yes } }
scripted_button = aor1776_hre_centralize_1
scripted_button = aor1776_hre_centralize_2
scripted_button = aor1776_hre_centralize_3
weight = 50''')
 files['common/journal_entries/1776_imperial_centralization.txt']=je
 buttons=''
 for stage in [1,2,3]:
  extra='' if stage<3 else 'NOT = { any_country = { aor1776_hre_member = yes NOT = { aor1776_hre_emperor = yes } NOT = { is_direct_subject_of = root is_subject_type = subject_type_aor1776_hre_crownland } } }'
  buttons+=block('aor1776_hre_centralize_'+str(stage),f'''name = aor1776_hre_centralize_{stage}
desc = aor1776_hre_centralize_{stage}_desc
visible = {{ global_var:aor1776_hre_reform_stage = {stage-1} }}
possible = {{ aor1776_hre_reform_safe = yes NOT = {{ has_variable = aor1776_hre_reform_cooldown }} {extra} }}
effect = {{ custom_tooltip = aor1776_hre_centralize_{stage}_desc hidden_effect = {{ aor1776_hre_stage_{stage} = yes }} }}
ai_chance = {{ base = 0 }} # Consequential reforms require an explicit ruler/player decision.
''')
  L('aor1776_hre_centralize_'+str(stage),['Establish imperial protectorates','Establish imperial crown lands','Unite the Empire'][stage-1],['Établir les protectorats impériaux','Établir les terres de la couronne','Unifier l’Empire'][stage-1])
  L('aor1776_hre_centralize_'+str(stage)+'_desc',['All recognised members must be in the imperial bloc and free of external overlords. Establish autonomous native subjects without tribute.','Reduce native autonomy and independent diplomatic initiative, retaining each estate and its ruler; no tribute.','Annex all remaining imperial crown lands into the Emperor’s country, including their possessions outside the registered imperial perimeter. This is actual unification, not a province-marker change.'][stage-1]+' Requires all four principles III, cohesion ≥75, two years since the previous stage/opening and peace for every member.',['Tous les membres reconnus doivent être dans le bloc et libres de suzerains extérieurs. Établir des sujets natifs autonomes sans tribut.','Réduire l’autonomie native et l’initiative diplomatique indépendante, en conservant chaque État et son dirigeant ; aucun tribut.','Annexer toutes les terres de la couronne impériales au pays de l’empereur, y compris leurs possessions hors du périmètre impérial enregistré. Il s’agit d’une véritable unification, pas d’un changement de marqueur.'][stage-1]+' Exige les quatre principes III, une cohésion ≥75, deux ans depuis l’étape précédente/ouverture et la paix pour tous les membres.')
 files['common/scripted_buttons/1776_imperial_centralization.txt']=buttons
 L('je_aor1776_hre_centralization','The reform of the Empire','La réforme de l’Empire')
 L('je_aor1776_hre_centralization_reason','Four institutions have matured. The Emperor may now negotiate a closer constitution: autonomous protectorates, crown lands, then unification. Reforms are decisions, not automatic annexations. External personal unions must first be settled through the imperial liberation mechanisms.','Quatre institutions sont arrivées à maturité. L’empereur peut désormais établir une constitution plus étroite : protectorats autonomes, terres de la couronne, puis unification. Les réformes sont des décisions, pas des annexions automatiques. Les unions personnelles extérieures doivent d’abord être réglées par les mécanismes de libération impériale.')
 L('je_aor1776_hre_centralization_status','All four principles III, cohesion ≥75, peace and the two-year consolidation period are required for each reform. Losing a principle pauses the next stage.','Les quatre principes III, une cohésion ≥75, la paix et deux ans de consolidation sont nécessaires à chaque réforme. La perte d’un principe suspend l’étape suivante.')
 for num,en,fr in [(60,'The Empire considers its future','L’Empire considère son avenir'),(61,'The protection of the imperial crown','La protection de la couronne impériale'),(62,'The estates beneath one crown','Les États sous une même couronne'),(63,'One imperial state','Un seul État impérial')]:
  files[EV]+=block('aor1776_hre.'+str(num),f'''type = country_event placement = root
title = aor1776_hre.{num}.t desc = aor1776_hre.{num}.d flavor = aor1776_hre.{num}.f
event_image = {{ video = "gfx/event_pictures/europenorthamerica_art_gallery.bk2" }}
option = {{ name = aor1776_hre.{num}.a default_option = yes }}''')
  L(f'aor1776_hre.{num}.t',en,fr)
  L(f'aor1776_hre.{num}.d',['The Diet, circles, courts and offices have acquired a common foundation. A closer constitution is possible, but the estates have not yet surrendered their autonomy.','The imperial estates now stand under the protection of the Emperor as autonomous subjects, without tribute. Their rulers remain in office.','The estates remain distinct, but foreign policy and military obligations are now subordinate to the imperial crown.','The remaining imperial crown lands have been united under one government. Their people and lands now belong to the unified imperial state.'][num-60],['La Diète, les cercles, les tribunaux et les bureaux disposent désormais d’un socle commun. Une constitution plus étroite est possible, mais les États n’ont pas encore abandonné leur autonomie.','Les États impériaux sont désormais placés sous la protection de l’empereur comme sujets autonomes sans tribut. Leurs dirigeants demeurent en place.','Les États demeurent distincts, mais leur politique extérieure et leurs obligations militaires sont désormais subordonnées à la couronne impériale.','Les terres de la couronne impériales restantes sont réunies sous un seul gouvernement. Leurs habitants et leurs territoires appartiennent désormais à l’État impérial unifié.'][num-60])
  L(f'aor1776_hre.{num}.f','The clerk counted the seals, then looked towards the empty chair beneath the imperial eagle. Each signature weighed more than its wax.','Le greffier compta les sceaux, puis regarda le fauteuil sous l’aigle impérial. Chaque signature pesait davantage que sa cire.')
  L(f'aor1776_hre.{num}.a','We shall preserve the Empire through its renewal.','Nous préserverons l’Empire par son renouvellement.')
 # Preserve imperial elections after the estates become native subjects.
 candidate=next(n for n in cw.parse(files[TRIG]) if n.key=='aor1776_hre_candidate')
 raw=files[TRIG][candidate.start:candidate.end].replace('is_subject = no','OR = { is_subject = no AND = { is_direct_subject_of = global_var:aor1776_hre_emperor_country OR = { is_subject_type = subject_type_aor1776_hre_protectorate is_subject_type = subject_type_aor1776_hre_crownland } } }',1)
 files[TRIG]=edits(files[TRIG],[(candidate.start,candidate.end,raw)])
 # New elected estate must cease being the previous Emperor's native subject
 # before founding. If creation fails, restore its previous native dependency.
 raw=files[EF]
 raw=raw.replace('  create_power_bloc = {','''  if = { limit = { is_direct_subject_of = scope:hre_old_imperial_country OR = { is_subject_type = subject_type_aor1776_hre_protectorate is_subject_type = subject_type_aor1776_hre_crownland } }
   if = { limit = { is_subject_type = subject_type_aor1776_hre_protectorate } set_variable = aor1776_hre_was_protectorate }
   else = { set_variable = aor1776_hre_was_crownland }
   make_independent = yes
  }
  create_power_bloc = {''',1)
 raw=raw.replace('power_bloc = { aor1776_hre_restore_principles = yes }','''power_bloc = { aor1776_hre_restore_principles = yes }
   if = { limit = { has_global_variable = aor1776_hre_reform_stage global_var:aor1776_hre_reform_stage > 0 }
    set_global_variable = { name = aor1776_hre_emperor_country value = this }
    if = { limit = { global_var:aor1776_hre_reform_stage = 1 } aor1776_hre_bind_protectorate = yes }
    else_if = { limit = { global_var:aor1776_hre_reform_stage = 2 } aor1776_hre_bind_crownland = yes }
   }
   remove_variable = aor1776_hre_was_protectorate remove_variable = aor1776_hre_was_crownland''',1)
 raw=raw.replace('set_global_variable = aor1776_hre_native_transfer_blocked }','''set_global_variable = aor1776_hre_native_transfer_blocked
   if = { limit = { has_variable = aor1776_hre_was_protectorate }
    scope:hre_old_imperial_country = { create_diplomatic_pact = { country = scope:hre_elected_country type = aor1776_hre_protectorate } }
   }
   else_if = { limit = { has_variable = aor1776_hre_was_crownland }
    scope:hre_old_imperial_country = { create_diplomatic_pact = { country = scope:hre_elected_country type = aor1776_hre_crownland } }
   }
   remove_variable = aor1776_hre_was_protectorate remove_variable = aor1776_hre_was_crownland
  }''',1)
 files[EF]=raw
 # A centralized estate may still contest the imperial bond through the
 # dedicated secession play; the enforced goal releases its native dependency.
 eligible='OR = { is_subject = no is_subject_type = subject_type_aor1776_hre_protectorate is_subject_type = subject_type_aor1776_hre_crownland }'
 rel='common/diplomatic_plays/1776_imperial_plays.txt';n=next(n for n in cw.parse(files[rel]) if n.key=='dp_aor1776_hre_secession')
 raw=files[rel][n.start:n.end].replace('is_subject = no',eligible)
 files[rel]=edits(files[rel],[(n.start,n.end,raw)])
 rel='common/war_goal_types/1776_imperial_war_goals.txt';n=next(n for n in cw.parse(files[rel]) if n.key=='aor1776_hre_secession')
 raw=files[rel][n.start:n.end].replace('is_subject = no',eligible)
 raw=raw.replace('on_enforced = {','on_enforced = {\n if = { limit = { OR = { is_subject_type = subject_type_aor1776_hre_protectorate is_subject_type = subject_type_aor1776_hre_crownland } } make_independent = yes }',1)
 files[rel]=edits(files[rel],[(n.start,n.end,raw)])
 # Unified name only for the Emperor, with all upstream country names retained.
 rel='common/dynamic_country_names/00_dynamic_country_names.txt';raw=existing(rel)
 if 'dyn_c_aor1776_hre_unified' not in raw:
  n=next(n for n in cw.parse(raw) if n.key=='DEFAULT')
  raw=edits(raw,[(n.end-1,n.end-1,'\n dynamic_country_name = { name = dyn_c_aor1776_hre_unified adjective = dyn_c_aor1776_hre_unified_adj priority = 1000 trigger = { has_global_variable = aor1776_hre_unified aor1776_hre_emperor = yes } }\n')])
 files[rel]=raw
 L('dyn_c_aor1776_hre_unified','Holy Roman Empire','Saint-Empire romain germanique');L('dyn_c_aor1776_hre_unified_adj','Imperial','Impérial')
