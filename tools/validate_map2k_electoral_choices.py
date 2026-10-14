"""Electoral regression models and script checks; no native execution claim."""
import re
import collections
import validate_diplomacy_ottoman_1776 as cw
from map2k_work import ROOT
from map2k_imperial_electoral_choices import JE, EF, DA, ARTICLE, TRIG, BREAK_INFAMY
from map2k_imperial_system import MEMBERS

def validate_electoral_choices(check,node,textnode):
 situation=node(JE,'je_aor1776_hre_situation')
 check('permanent_imperial_journal_pinned_by_native_country_context_flag',situation.one('should_be_pinned_by_default_uninvolved_or_context')=='yes')
 check('imperial_journal_visible_in_country_selection_before_global_init',situation.children('is_shown_in_lobby')[0].one('aor1776_hre_member')=='yes' and 'initialized' not in textnode(situation.children('is_shown_in_lobby')))
 check('permanent_journal_has_all_candidate_buttons_including_self',{n.value for n in situation.children('scripted_button')}=={'aor1776_hre_vote_'+t for t in MEMBERS})
 for t in MEMBERS:
  b=node('common/scripted_buttons/1776_imperial_voting.txt','aor1776_hre_vote_'+t)
  check('electoral_choice_button_uses_same_guarded_effect:'+t,'aor1776_hre_can_choose_electoral_vote' in textnode(b.children('possible')) and 'c:'+t in textnode(b.children('effect')) and 'aor1776_hre_choose_electoral_vote' in textnode(b.children('effect')) and 'has_variable' not in textnode(b.children('possible')))
 allowed=textnode(node(TRIG,'aor1776_hre_can_choose_electoral_vote'))
 check('choice_before_election_or_during_thirty_day_window',all(k in allowed for k in ['CANDIDATE','aor1776_hre_elector','aor1776_hre_ballot_candidate','aor1776_hre_deliberation','aor1776_hre_election_open','aor1776_hre_promised_candidate','is_ai']))
 cast=node(EF,'aor1776_hre_cast_vote');raw=textnode(cast)
 check('vote_changes_recount_instead_of_adding_duplicate_tallies','aor1776_hre_recount_ballot' in raw and 'change_variable' not in raw and 'change_global_variable' not in raw)
 penalties=[n for n in cw.walk(cast.children()) if n.key=='change_infamy']
 check('broken_human_pledge_exactly_ten_infamy_once',len(penalties)==1 and penalties[0].value==str(BREAK_INFAMY)==str(10) and 'remove_variable' in raw and 'aor1776_hre_promised_candidate' in raw and 'is_ai' in raw)
 start=textnode(node(EF,'aor1776_hre_start_ballot'))
 check('initial_choices_registered_after_voters_and_before_refresh',start.index('aor1776_hre_voter_this_round')<start.index('aor1776_hre_register_initial_ballot')<start.index('aor1776_hre_feedback_refresh') and 'aor1776_hre_deliberation' in start)
 initial=textnode(node(EF,'aor1776_hre_register_initial_ballot'))
 check('binding_promise_precedes_human_preference_and_AI_fallback',initial.index('aor1776_hre_promised_candidate')<initial.index('aor1776_hre_preferred_candidate')<initial.index('aor1776_hre_ai_ballot'))
 ai=textnode(node(EF,'aor1776_hre_ai_ballot'))
 check('AI_pledge_direct_choice_not_merely_score_bonus',ai.index('aor1776_hre_promised_candidate')<ai.index('ordered_country') and 'aor1776_hre_vote_preference' in ai)
 revising=textnode(node(EF,'aor1776_hre_update_unpledged_ballots'))
 check('only_unpledged_AI_may_revise_during_deliberation',all(k in revising for k in ['aor1776_hre_deliberation','aor1776_hre_voter_this_round','aor1776_hre_promised_candidate','aor1776_hre_ai_ballot','NOT','is_ai']))
 action=node(DA,'aor1776_hre_choose_electoral_candidate')
 check('candidate_country_panel_action_needs_no_candidate_approval',action.one('requires_approval')=='no' and 'aor1776_hre_choose_electoral_vote' in textnode(action.children('accept_effect')))
 article=node(ARTICLE,'aor1776_electoral_promise');score=textnode(article.children('ai')[0].children('inherent_accept_score'))
 check('electoral_pledge_requires_positive_duration_and_updates_preview',article.children('can_ratify')[0].children('scope:treaty.binding_period')[0].op=='>' and article.children('can_ratify')[0].one('scope:treaty.binding_period')=='0' and 'aor1776_hre_update_vote_preview' in textnode(article.children('on_entry_into_force')))
 check('pledge_acceptance_distinguishes_giving_and_receiving_country',all(k in score for k in ['scope:source_country','scope:target_country','aor1776_hre_vote_preference','aor1776_hre_pledge_accept_base','aor1776_hre_pledge_accept_receiving']))
 check('pledge_acceptance_values_historical_preference_obligation_duration',all(k in score for k in ['aor1776_hre_pledge_accept_preference','owes_obligation_to','binding_period','aor1776_hre_pledge_accept_duration']))
 gui=(ROOT/'gui/journal_entry_widgets/1776_imperial_widgets.gui').read_text(encoding='utf-8-sig')
 check('elector_card_vote_uses_player_as_voter_and_country_as_candidate',all(k in gui for k in ['aor1776_hre_card_vote','aor1776_hre_choose_vote_gui','SetRoot(GetPlayer.MakeScope)',"AddScope('hre_vote_choice', Country.MakeScope)"]))
 # A minimal independent model of the specified rule. Structural checks above
 # tie it to storing a single ballot and recounting, not to native execution.
 def vote(ballots,voter,candidate,promise=None,ai=False,window=True):
  if voter in ballots and (not window or (ai and promise)):return promise,0
  if promise and promise!=candidate and ai:return promise,0
  cost=BREAK_INFAMY if promise and promise!=candidate else 0
  ballots[voter]=candidate
  return (None if cost else promise),cost
 ballots={'PRU':'AUS','BAV':'BAV','SAX':'AUS'}
 promise,cost=vote(ballots,'PRU','PRU',promise='AUS')
 check('human_can_change_pledged_vote_and_pay_ten_model',cost==10 and promise is None and ballots['PRU']=='PRU' and len(ballots)==3)
 promise,cost=vote(ballots,'PRU','BAV',promise=promise)
 check('further_changes_do_not_recharge_broken_promise_model',cost==0 and len(ballots)==3 and collections.Counter(ballots.values())=={'AUS':1,'BAV':2})
 before=ballots.copy();vote(ballots,'SAX','PRU',promise='AUS',ai=True)
 check('pledged_AI_cannot_change_model',ballots==before)
 vote(ballots,'BAV','AUS',window=False)
 check('already_cast_vote_locked_after_deliberation_model',ballots==before)
 vote(ballots,'SAX','PRU',ai=True)
 check('unpledged_AI_may_revise_without_duplicating_ballot_model',ballots['SAX']=='PRU' and len(ballots)==3)
 for lang in ['english','french']:
  raw=(ROOT/f'localization/{lang}/1776_imperial_electoral_choices_l_{lang}.yml').read_text(encoding='utf-8-sig')
  keys=set(re.findall(r'^ ([^ :]+):0 ',raw,re.M))
  check('all_electoral_choice_UI_and_score_keys_localized:'+lang,{'aor1776_hre.choose_'+t for t in MEMBERS}|{'aor1776_hre_choose_vote_desc','aor1776_hre_choose_vote_result','aor1776_hre_card_vote_label','aor1776_hre_vote_selected','aor1776_hre_pledge_accept_base','aor1776_hre_pledge_accept_preference','aor1776_hre_pledge_accept_duration'}<=keys)
