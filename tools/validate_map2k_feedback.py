"""Structural feedback checks and explicit models, never engine verification."""
import re
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2k_work import ROOT,GAME

def validate_feedback(check,node,textnode,ledger):
 ef='common/scripted_effects/1776_imperial_constitution.txt'
 oa='common/on_actions/1776_imperial_constitution.txt'
 da='common/diplomatic_actions/1776_imperial_actions.txt'
 trig='common/scripted_triggers/1776_imperial_constitution.txt'
 identity=node('common/power_bloc_identities/1776_imperial_federation.txt','identity_aor1776_imperial_federation')
 check('HRE_no_per_member_cohesion_penalty',identity.children('power_bloc_modifier')[0].one('power_bloc_cohesion_per_member_add')=='0')
 formula=textnode(identity.children('cohesion'))
 check('HRE_cohesion_only_territory_electors_free_cities',all(k in formula for k in ['aor1776_hre_outside_provinces','aor1776_hre_hostile_electors','aor1776_hre_hostile_cities']) and not any(k in formula for k in ['is_subject','num_power_bloc_members','independent','share_gdp','power_projection']))
 check('HRE_voluntary_exit_remains_locked',identity.children('can_leave')[0].one('always')=='no')
 for libre in [0,20,35]:
  # Actual formula contains no member-count input: fixed adverse conditions.
  score=max(0,min(100,90-40*20/278-5*2-3*1))
  check('cohesion_model_independence_invariant:'+str(libre),round(score,6)==round(90-40*20/278-13,6),'Arithmetic model, not engine result')
 raw=(ROOT/oa).read_text(encoding='utf-8-sig')
 check('native_diplomatic_play_start_hook_registered','on_diplo_play_start = ' in raw and 'on_diplomatic_play_started' not in raw)
 r=node(ef,'aor1776_hre_restore_membership');body=textnode(r)
 check('membership_repair_only_live_HRE_leader','identity:identity_aor1776_imperial_federation' in body and 'is_power_bloc_leader' in body)
 limit=next(n for n in r.children('if')[0].children('every_country')).children('limit')[0]
 check('membership_repair_protects_external_subjects_and_active_war',limit.one('aor1776_hre_member')=='yes' and limit.one('is_subject')=='no' and 'is_diplomatic_play_enemy_of' in textnode(limit))
 check('legal_secession_excluded_from_membership_repair','aor1776_hre_seceded' in textnode(node(trig,'aor1776_hre_member')))
 check('membership_repair_checks_success_before_notice','aor1776_hre_membership_pending' in body and 'is_in_same_power_bloc' in textnode(r.children('if')[0].children('every_country')[0].children('if')[0].children('limit')))
 check('daily_guard_uses_delayed_native_event_not_phantom_pulse','aor1776_hre.40' in textnode(node(ef,'aor1776_hre_schedule_membership_guard')) and 'on_daily_pulse' not in raw)
 check('daily_guard_follows_current_emperor','global_var:aor1776_hre_emperor_country' in textnode(node('events/1776_imperial_constitution_events.txt','aor1776_hre.40')))
 catrel='common/diplomatic_catalysts/00_diplomatic_catalysts.txt'
 new=cw.parse((ROOT/catrel).read_text(encoding='utf-8-sig'));old=cw.parse((GAME/catrel).read_text(encoding='utf-8-sig'))
 check('all_other_native_catalysts_unchanged',[qa.norm(n) for n in new if n.key!='catalyst_kicked_out_of_bloc']==[qa.norm(n) for n in old if n.key!='catalyst_kicked_out_of_bloc'])
 cat=node(catrel,'catalyst_kicked_out_of_bloc');oldcat=next(n for n in old if n.key==cat.key)
 check('nonimperial_expulsion_effect_unchanged',[qa.norm(n) for n in cat.children('effect')[0].children('else')[0].children()]==[qa.norm(n) for n in oldcat.children('effect')[0].children()])
 check('illegal_imperial_kick_intercepted','aor1776_hre_restore_membership' in textnode(cat.children('effect')[0].children('if')[0]) and all('aor1776_hre_illegal_expulsion' in textnode(n.children('trigger')) for field in ['political_lobby_creation','ai_country_goal_recalculation'] for n in cat.children(field)))
 for rel in ['gui/power_bloc_panel.gui','gui/right_click_menu.gui']:
  rawgui=(ROOT/rel).read_text(encoding='utf-8-sig')
  stripped=re.sub(r'\[And\((IsValid\([^\n]+?\)), GetScriptedGui\(\'aor1776_hre_allow_native_kick\'\).IsValid\(GuiScope.SetRoot\(Country.MakeScope\).End\)\)\]',r'[\1]',rawgui)
  stripped=stripped.replace("[SelectLocalization(GetScriptedGui('aor1776_hre_allow_native_kick').IsValid(GuiScope.SetRoot(Country.MakeScope).End), 'POWER_BLOC_KICK_MEMBER_TOOLTIP', 'aor1776_hre_cannot_expel_tt')]",'POWER_BLOC_KICK_MEMBER_TOOLTIP')
  if rel.endswith('right_click_menu.gui'):
   # The separately tested atlas shortcut is the only additional GUI change.
   from validate_map2k_repairs import without_atlas
   stripped=without_atlas(stripped,(GAME/rel).read_text(encoding='utf-8-sig'))
  check('GUI_only_native_kick_guard_changed:'+rel,stripped==(GAME/rel).read_text(encoding='utf-8-sig') and stripped!=rawgui)
 request=node(da,'aor1776_hre_request_subject_release')
 check('release_native_approval_has_visible_score',request.one('requires_approval')=='yes' and bool(request.children('ai')[0].children('accept_score')))
 check('release_notifications_for_both_responses',all('trigger_event' in textnode(request.children(k)) for k in ['accept_effect','decline_effect']))
 check('release_preview_lists_actual_subjects','aor1776_hre_preview_subjects' in textnode(request) and 'every_subject_or_below' in textnode(node(ef,'aor1776_hre_preview_subjects')))
 check('response_snapshots_before_release','aor1776_hre_snapshot_reply_subjects' in textnode(request.children('accept_effect')) and textnode(request.children('accept_effect')).index('aor1776_hre_snapshot_reply_subjects')<textnode(request.children('accept_effect')).index('aor1776_hre_release_imperial_subjects'))
 start=node(ef,'aor1776_hre_start_ballot');tally=node(ef,'aor1776_hre_tally_ballot')
 check('all_ballots_have_thirty_day_deliberation','aor1776_hre_deliberation' in textnode(start) and any(n.key=='days' and n.value=='30' for n in cw.walk(start.children())) and 'aor1776_hre_ai_ballot' not in textnode(start))
 check('majority_cannot_bypass_deliberation','aor1776_hre_deliberation' in textnode(tally.children('if')[1].children('limit')))
 article=node('common/treaty_articles/1776_imperial_electoral_promise.txt','aor1776_electoral_promise')
 check('electoral_pledge_native_binding_period','scope:treaty_options.binding_period' in textnode(article) and any(n.key=='multiply' and n.value=='365' for n in cw.walk(article.children())))
 check('vote_pledge_restricts_votes_until_expiry','aor1776_hre_promised_candidate' in textnode(node(ef,'aor1776_hre_cast_vote')) and 'aor1776_hre_promise_cast' in textnode(node(ef,'aor1776_hre_finish_investiture')))
 mod=node('common/static_modifiers/1776_imperial_territory.txt','aor1776_hre_registered_territory')
 surcharge='state_aor1776_imperial_conquest_infamy_mult'
 check('imperial_state_marker_exact_25_percent_only',mod.one(surcharge)=='0.25' and {n.key for n in mod.children()}=={'icon',surcharge})
 conquest=node('common/war_goal_types/03_conquer_state.txt','conquer_state')
 original=cw.parse((GAME/'common/war_goal_types/03_conquer_state.txt').read_text(encoding='utf-8-sig'))[0]
 check('conquer_goal_only_infamy_changed',[qa.norm(n) for n in conquest.children() if n.key!='infamy']==[qa.norm(n) for n in original.children() if n.key!='infamy'])
 check('imperial_restitution_liberation_no_surcharge',surcharge not in (ROOT/'common/war_goal_types/1776_imperial_war_goals.txt').read_text(encoding='utf-8-sig'))
 from map2k_imperial_principles import GROUPS
 check('exactly_four_user_approved_imperial_principle_groups',{n.key for p in (ROOT/'common/power_bloc_principle_groups').glob('*.txt') for n in cw.parse(p.read_text(encoding='utf-8-sig')) if n.key.startswith('aor1776')}==set(GROUPS))
 for lang in ['english','french']:
  rawloc=(ROOT/f'localization/{lang}/1776_imperial_feedback_l_{lang}.yml').read_text(encoding='utf-8-sig')
  check('native_wargoal_names_and_descriptions:'+lang,all('war_goal_'+k+'_type_name:0 ' in rawloc and 'war_goal_'+k+'_desc:0 ' in rawloc for k in ['aor1776_hre_subject_release','aor1776_hre_restitution','aor1776_hre_secession']))
  check('all_registered_RGBs_preview_localized:'+lang,all('aor1776_hre_province_'+r['rgb']+':0 ' in rawloc for r in ledger))
