"""Regression checks against user-reported failures; static/model tests only."""
import re,math
import validate_diplomacy_ottoman_1776 as cw
from map2k_work import ROOT,GAME
from map2k_imperial_system import MEMBERS
from map2k_imperial_repairs import GOAL,VALUES

def menu_range(raw):
 start=raw.rfind('right_click_menu = {',0,raw.index('name = "map_modes_right_click_menu"'))
 opening=raw.index('{',start);depth=1
 for t in re.finditer(r'"(?:\\.|[^"\\])*"|[{}]',raw[opening+1:]):
  if t.group()=='{':depth+=1
  elif t.group()=='}':depth-=1
  if depth==0:return start,opening+1+t.end()
 raise ValueError('Unclosed GUI menu')

def without_atlas(raw,original):
 a,b=menu_range(raw);x,y=menu_range(original)
 result=raw[:a]+original[x:y]+raw[b:]
 suffix='\nwidget = {\n name = "aor1776_hre_imperial_atlas"'
 if suffix in result:result=result[:result.index(suffix)]
 return result

def validate_repairs(check,node,textnode,ledger):
 da='common/diplomatic_actions/1776_imperial_actions.txt';ef='common/scripted_effects/1776_imperial_constitution.txt';wg='common/war_goal_types/1776_imperial_war_goals.txt'
 goal=node(wg,GOAL)
 check('liberation_native_kind_targets_subject_not_suzerain',goal.one('kind')=='liberate_subject' and goal.one('target_type')=='country' and 'overlord' in textnode(goal.children('valid')) and 'aor1776_hre_member' in textnode(goal.children('possible')))
 check('liberation_contestion_on_subject_land',goal.one('contestion_type')=='control_half_target_country_states' and 'overlord_is_stakeholder' in textnode(goal.children('settings')) and 'control_target_country_capital' not in textnode(goal))
 dp=node('common/diplomatic_plays/1776_imperial_plays.txt','dp_aor1776_hre_subject_release')
 check('liberation_play_uses_subject_goal_and_overlord_blockers',dp.one('war_goal')==GOAL and 'diplomatic_play_has_no_relations_blocker_with_overlord' in textnode(dp))
 prep=node(ef,'aor1776_hre_prepare_liberation_goals');commands=list(cw.walk(prep.children()));s=textnode(prep)
 check('selected_subject_native_goal_never_automatically_expands',dp.one('war_goal')==GOAL and not any(n.key in {'add_war_goal','remove_war_goal','has_war_goal'} for n in commands))
 check('liberation_preparation_marked_before_side_repairs',s.index('aor1776_hre_liberation_prepared')<s.index('aor1776_hre_captive_corrected_'))
 check('single_subject_enforcement_cannot_release_remaining_package','aor1776_hre_release_imperial_subjects' not in textnode(goal.children('on_enforced')) and 'aor1776_hre_return_released_subject_provinces' in textnode(goal.children('on_enforced')))
 check('imperial_play_initiators_can_spend_remaining_maneuvers',all(node('common/diplomatic_plays/1776_imperial_plays.txt',k).one('initiator_can_add_war_goals')=='yes' for k in ['dp_aor1776_hre_subject_release','dp_aor1776_hre_restitution']))
 check('captives_reassigned_once_not_on_join_callbacks','aor1776_hre_captive_corrected_MST' in s and 'remove_initiator_backers' in s and 'add_target_backers' in s and 'on_diplo_play_join_side' not in (ROOT/'common/on_actions/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig'))
 defense=node(ef,'aor1776_hre_defend_external_attack');calls=[n for n in defense.children('if')[0].children('if') if n.children('set_variable') and any('aor1776_hre_called_' in str(x.value) for x in n.children('set_variable'))]
 check('every_ordinary_call_has_persistent_stamp_and_foreign_subject_exclusion',len(calls)==2*len(MEMBERS) and all('is_subject_of' in textnode(n.children('limit')) and 'top_overlord' in textnode(n.children('limit')) and 'has_variable' in textnode(n.children('limit')) and 'is_diplomatic_play_ally_of' in textnode(n) for n in calls))
 # Simplified dependency/backing fixture, not a claim about code-side switching.
 graph={'LUB':'SWE','MEC':'SWE','MST':'MEC','HAN':'GBR','PRU':None,'AUS':None}
 def top(c):
  while graph.get(c) is not None:c=graph[c]
  return c
 enemy={c for c in graph if top(c)=='SWE'};calls_fixture={c for c in graph if c!='AUS' and top(c)!='SWE'}
 check('nested_captives_never_in_attacking_call_fixture',enemy=={'LUB','MEC','MST'} and not enemy&calls_fixture)
 registered=set();notifications=[]
 for pulse in range(20):
  for c in calls_fixture:
   if c not in registered:registered.add(c);notifications.append(c)
 check('twenty_pulses_generate_at_most_one_call_per_estate_model',len(notifications)==len(calls_fixture))
 for k in ['aor1776_hre_request_subject_release','aor1776_hre_request_restitution']:
  a=node(da,k);score=textnode(a.children('ai')[0].children('accept_score'))
  check('native_visible_acceptance_all_requested_factors:'+k,a.one('requires_approval')=='yes' and all(x in score for x in ['aor1776_hre_accept_base','aor1776_hre_accept_relations','aor1776_hre_accept_army','aor1776_hre_accept_allies','aor1776_hre_accept_cohesion']) and 'trigger_event' not in textnode(a.children('accept_effect'))[:1])
 score=node(VALUES,'aor1776_hre_external_acceptance')
 check('acceptance_compares_recipient_with_proposing_emperor_not_itself','scope:target' not in textnode(score) and all(x in textnode(score) for x in ['relations(scope:actor)','scope:actor.ai_army_comparison(root)','scope:actor.aor1776_hre_imperial_available_strength','scope:actor.power_bloc.current_cohesion_number','owes_obligation_to']))
 internal=node(da,'aor1776_hre_enforce_internal_restitution')
 check('internal_restitution_binds_humans_not_just_AI',internal.one('requires_approval')=='no' and 'owes_obligation_to' in textnode(internal.children('potential')) and 'aor1776_hre_return_requested_provinces' in textnode(internal.children('accept_effect')) and not internal.children('decline_effect'))
 check('every_score_contribution_labelled',all(n.children('desc') for n in cw.walk(score.children()) if n.key=='add'))
 def accept(rel,army,allies,cohesion,owed=False):return -25+rel*.5+max(-50,min(50,army*2))-max(0,min(60,allies*40))+(cohesion-50)*.75+(60 if owed else 0)
 check('acceptance_monotonic_in_relations_force_cohesion_model',accept(25,20,.2,80)>accept(0,20,.2,80) and accept(0,30,.2,80)>accept(0,20,.2,80) and accept(0,20,.2,90)>accept(0,20,.2,80) and accept(0,20,.8,80)<accept(0,20,.2,80))
 for k in ['state_aor1776_imperial_conquest_infamy_mult','country_aor1776_hre_authority_per_estate_add']:
  check('symbolic_modifier_flagged_script_only:'+k,node('common/modifier_type_definitions/1776_imperial_modifier_types.txt',k).one('script_only')=='yes')
 for rel in ['common/scripted_buttons/1776_imperial_voting.txt','common/scripted_buttons/1776_imperial_centralization.txt']:
  check('scripted_button_ai_chance_uses_value_not_event_base:'+rel,all(not n.children('base') and n.one('value')=='0' for n in cw.walk(cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))) if n.key=='ai_chance'))
 visible=[n for n in cw.parse((ROOT/'events/1776_imperial_constitution_events.txt').read_text(encoding='utf-8-sig')) if n.one('type')=='country_event' and n.one('hidden')!='yes']
 for lang in ['english','french']:
  loc={}
  for p in (ROOT/'localization'/lang).glob('1776_imperial*_l_'+lang+'.yml'):
   loc.update(dict(re.findall(r'^ ([^ :]+):0 "(.*)"$',p.read_text(encoding='utf-8-sig'),re.M)))
  check('all_visible_imperial_events_have_literary_flavor:'+lang,all(cw.scalar(n.one('flavor')) in loc and '#italic' in loc[cw.scalar(n.one('flavor'))] for n in visible))
  check('pact_description_actual_UI_key_localized:'+lang,'aor1776_imperial_obligation_pact_desc' in loc)
  check('new_liberation_goal_native_UI_keys:'+lang,all('war_goal_'+GOAL+s in loc for s in ['_type_name','_name','_desc','_on_enforced']))
  check('snapshot_RGB_names_present:'+lang,all('aor1776_hre_reply_rgb_'+r['rgb'] in loc for r in ledger))
 for num in [30,31,32,33,34,35]:
  option=node('events/1776_imperial_constitution_events.txt','aor1776_hre.'+str(num)).children('option')[0]
  check('acknowledgement_shows_result_without_reapplying_it:'+str(num),bool(option.children('custom_tooltip')) and option.one('aor1776_hre_reply_details')=='yes' and {n.key for n in option.children()}<={'name','default_option','custom_tooltip','aor1776_hre_reply_details'})
 raw=(ROOT/'gui/right_click_menu.gui').read_text(encoding='utf-8-sig');a,b=menu_range(raw)
 hud=(ROOT/'gui/ingame_hud.gui').read_text(encoding='utf-8-sig')
 check('obsolete_atlas_context_shortcut_removed','aor1776_hre_atlas_open' not in raw[a:b] and 'MapModeList.GetMapModes' in raw[a:b])
 check('native_context_map_choices_preserved',raw[a:b]==(GAME/'gui/right_click_menu.gui').read_text(encoding='utf-8-sig')[slice(*menu_range((GAME/'gui/right_click_menu.gui').read_text(encoding='utf-8-sig')))])
 marker='name = "aor1776_hre_imperial_atlas"'
 native=(GAME/'gui/ingame_hud.gui').read_text(encoding='utf-8-sig')
 check('obsolete_standalone_bitmap_atlas_removed',marker not in raw and marker not in hud and 'aor1776_hre_atlas_open' not in hud)
 check('all_other_HUD_content_exactly_preserved',hud==native)
