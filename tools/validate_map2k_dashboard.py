"""Country-context dashboard regressions. Not a substitute for a UI test."""
import re
import validate_diplomacy_ottoman_1776 as cw
from map2k_work import ROOT

def validate_dashboard(check,node,textnode):
 group=node('common/journal_entry_groups/1776_imperial_affairs.txt','je_group_aor1776_imperial_affairs')
 check('imperial_journal_group_has_explicit_country_context',group.one('context')=='country')
 for k,rel in [('je_aor1776_hre_situation','1776_imperial_situation.txt'),('je_aor1776_hre_vote','1776_imperial_situation.txt'),('je_aor1776_hre_centralization','1776_imperial_centralization.txt')]:
  n=node('common/journal_entries/'+rel,k)
  check('imperial_journal_uses_country_not_null_context:'+k,n.one('group')=='je_group_aor1776_imperial_affairs')
 ef='common/scripted_effects/1776_imperial_constitution.txt'
 refresh=textnode(node(ef,'aor1776_hre_feedback_refresh'))
 check('dashboard_repairs_missing_journal_and_copies_territorial_counts',all(x in refresh for x in ['aor1776_hre_under_authority','aor1776_hre_outside_provinces','has_journal_entry','add_journal_entry','je_aor1776_hre_situation']))
 check('electoral_and_free_city_lists_rebuilt_without_duplicates',all(x in refresh for x in ['clear_variable_list','aor1776_hre_electors_list','aor1776_hre_free_cities_list','aor1776_hre_free_city','aor1776_hre_update_vote_preview']))
 preview=textnode(node(ef,'aor1776_hre_update_vote_preview'))
 check('vote_preview_reuses_actual_AI_score_but_never_votes',all(x in preview for x in ['ordered_country','aor1776_hre_vote_preference','aor1776_hre_ui_vote_choice','aor1776_hre_promised_candidate','aor1776_hre_voted_for']) and all(x not in preview for x in ['aor1776_hre_cast_vote','aor1776_hre_ai_ballot','aor1776_hre_tally_ballot','trigger_event']))
 timer=textnode(node('events/1776_imperial_constitution_events.txt','aor1776_hre.40'))
 check('shared_dashboard_refresh_throttled_to_seven_days','aor1776_hre_dashboard_refreshed' in timer and '"days", "=", "7"' in timer and 'aor1776_hre_feedback_refresh' in timer)
 gui=(ROOT/'gui/journal_entry_widgets/1776_imperial_widgets.gui').read_text(encoding='utf-8-sig')
 # Native crash logs explicitly reject direct hbox/vbox children of containers.
 def invalid_layouts(raw):
  return [n for n in cw.walk(cw.parse(raw)) if n.key in {'flowcontainer','container'} and any(c.key in {'hbox','vbox'} for c in n.children())]
 check('journal_has_no_native_forbidden_container_layout_child',not invalid_layouts(gui))
 check('layout_regression_detects_original_crashing_structure',bool(invalid_layouts('flowcontainer = { hbox = { spacing = 8 } }')) and not invalid_layouts('flowcontainer = { widget = { size = { 500 85 } hbox = {} } }'))
 rows={cw.scalar(n.one('name')):n for n in cw.walk(cw.parse(gui)) if n.key=='widget' and n.one('name')}
 for name,height in [('aor1776_hre_emperor_row',85),('aor1776_hre_elector_row',150)]:
  row=rows.get(name)
  check('portrait_layout_has_sized_wrapper:'+name,row is not None and bool(row.children('hbox')) and [x.value for x in row.children('size')[0].children()]==['500',str(height)])
 check('dashboard_shows_elector_portraits_predictions_free_cities_and_states',all(k in gui for k in ['character_portrait_medium','aor1776_hre_vote_display','aor1776_hre_free_cities_list','aor1776_hre_states_list','aor1776_hre_dashboard_decisions']))
 for lang in ['english','french']:
  loc='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'localization'/lang).glob('1776_imperial*_l_'+lang+'.yml'))
  check('dashboard_localizes_vote_statuses_and_future_decisions:'+lang,all(k+':0 ' in loc for k in ['aor1776_hre_vote_cast','aor1776_hre_vote_promised','aor1776_hre_vote_predicted','aor1776_hre_vote_human','aor1776_hre_vote_none','aor1776_hre_free_cities_heading','aor1776_hre_dashboard_decisions']))
