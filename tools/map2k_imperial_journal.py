"""Country-context imperial dashboard; display predictions, never cast a vote."""
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2k_imperial_feedback import block,append_inside,child,EF,EV

def augment_journal(files):
 loc={}
 def L(k,en,fr):loc[k]=(en,fr)
 group='je_group_aor1776_imperial_affairs'
 files['common/journal_entry_groups/1776_imperial_affairs.txt']=block(group,'context = country')
 L(group,'Imperial affairs','Affaires impériales')
 # Without an explicit country-context group, the default JE can be evaluated
 # without an owning country: the player's log reports invalid RHS "this".
 for rel in ['common/journal_entries/1776_imperial_situation.txt','common/journal_entries/1776_imperial_centralization.txt']:
  for key in [n.key for n in cw.parse(files[rel])]:files[rel]=child(files[rel],key,'group','group = '+group)
 files[EF]+=block('aor1776_hre_update_vote_preview','''save_scope_as = hre_voter
 remove_variable = aor1776_hre_ui_vote_choice
 remove_variable = aor1776_hre_ui_vote_cast
 remove_variable = aor1776_hre_ui_vote_promised
 if = { limit = { has_global_variable = aor1776_hre_election_open has_variable = aor1776_hre_voted exists = var:aor1776_hre_voted_for }
  set_variable = { name = aor1776_hre_ui_vote_choice value = var:aor1776_hre_voted_for }
  set_variable = aor1776_hre_ui_vote_cast
 }
 else_if = { limit = { exists = var:aor1776_hre_promised_candidate var:aor1776_hre_promised_candidate = { aor1776_hre_ballot_candidate = yes } }
  set_variable = { name = aor1776_hre_ui_vote_choice value = var:aor1776_hre_promised_candidate }
  set_variable = aor1776_hre_ui_vote_promised
 }
 else_if = { limit = { is_ai = yes }
  ordered_country = {
   limit = { aor1776_hre_ballot_candidate = yes }
   order_by = aor1776_hre_vote_preference position = 0 check_range_bounds = no
   scope:hre_voter = { set_variable = { name = aor1776_hre_ui_vote_choice value = prev } }
  }
 }
''')
 refresh=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_feedback_refresh')
 raw=files[EF][refresh.start:refresh.end]
 raw=raw.replace('clear_variable_list = aor1776_hre_electors_list','clear_variable_list = aor1776_hre_electors_list clear_variable_list = aor1776_hre_free_cities_list')
 raw=raw.replace('scope:hre_current_emperor = { add_to_variable_list = { name = aor1776_hre_electors_list target = prev } }','scope:hre_current_emperor = { add_to_variable_list = { name = aor1776_hre_electors_list target = prev } }\n aor1776_hre_update_vote_preview = yes')
 raw=raw.replace('if = { limit = { aor1776_hre_free_city = yes var:aor1776_hre_relation_to_emperor < 0 }','if = { limit = { aor1776_hre_free_city = yes } scope:hre_current_emperor = { add_to_variable_list = { name = aor1776_hre_free_cities_list target = prev } } }\n if = { limit = { aor1776_hre_free_city = yes var:aor1776_hre_relation_to_emperor < 0 }')
 files[EF]=edits(files[EF],[(refresh.start,refresh.end,raw)])
 # Reuse the existing delayed guard, refreshing once a week for the current
 # Emperor, not a whole-world scan every day for every estate.
 files[EV]=files[EV].replace('aor1776_hre_restore_membership = yes\n   aor1776_hre_reform_controller = yes','aor1776_hre_restore_membership = yes\n   if = { limit = { NOT = { has_variable = aor1776_hre_dashboard_refreshed } } set_variable = { name = aor1776_hre_dashboard_refreshed days = 7 } aor1776_hre_feedback_refresh = yes }\n   aor1776_hre_reform_controller = yes')
 files[EF]=append_inside(files[EF],'aor1776_hre_cast_vote','if = { limit = { aor1776_hre_elector = yes } aor1776_hre_update_vote_preview = yes }')
 # The normal initialization/refresh adds missing country JEs even when the
 # one-time imperial initialization flag is already set in an old save.
 gui='gui/journal_entry_widgets/1776_imperial_widgets.gui'
 raw=files[gui]
 old='text = "[Country.GetName] — [Country.GetRuler.GetFullNameNoFormatting]"'
 new='text = "[Country.GetName] — [Country.GetRuler.GetFullNameNoFormatting]\\n[Country.GetCustom(\'aor1776_hre_vote_display\')]"'
 assert old in raw
 raw=raw.replace(old,new).replace('addrow = 85','addrow = 110').replace('size = { 380 75 }','size = { 380 100 }').replace('size = { 370 70 }','size = { 370 95 }')
 raw=raw.replace('name = "aor1776_hre_elector_row"\n    size = { 500 85 }','name = "aor1776_hre_elector_row"\n    size = { 500 110 }')
 cities='''textbox = { using = fontsize_medium size = { 500 40 } text = "aor1776_hre_free_cities_heading" }
 fixedgridbox = {
  datamodel = "[JournalEntry.GetCountry.MakeScope.Var('aor1776_hre_ui_emperor').GetCountry.MakeScope.GetList('aor1776_hre_free_cities_list')]"
  addcolumn = 500 addrow = 45
  item = { button = {
   datacontext = "[Scope.GetCountry]" size = { 500 42 }
   onclick = "[InformationPanelBar.OpenCountryPanel(Country.AccessSelf)]"
   textbox = { using = fontsize_medium size = { 490 40 } text = "[Country.GetName] — [Country.MakeScope.Var('aor1776_hre_relation_to_emperor').GetValue|=0]" }
  } }
 }
 textbox = { using = fontsize_medium size = { 500 75 } text = "aor1776_hre_dashboard_decisions" multiline = yes }
'''
 raw=raw.replace(' textbox = { using = fontsize_medium size = { 500 35 } text = "aor1776_hre_states_heading" }',cities+' textbox = { using = fontsize_medium size = { 500 35 } text = "aor1776_hre_states_heading" }')
 files[gui]=raw
 choice="[SCOPE.GetRootScope.GetCountry.MakeScope.Var('aor1776_hre_ui_vote_choice').GetCountry.GetName]"
 for suffix,en,fr in [('cast','Vote cast: ','Vote exprimé : '),('promised','Binding pledge: ','Promesse en vigueur : '),('predicted','Current AI preference (not binding): ','Préférence IA actuelle (non contraignante) : ')]:L('aor1776_hre_vote_'+suffix,en+choice,fr+choice)
 L('aor1776_hre_vote_human','Player’s choice: no binding commitment','Choix du joueur : aucun engagement contraignant')
 L('aor1776_hre_vote_none','No eligible candidate','Aucun candidat éligible')
 custom=block('aor1776_hre_vote_display','''type = country
 text = { trigger = { has_variable = aor1776_hre_ui_vote_cast exists = var:aor1776_hre_ui_vote_choice } localization_key = aor1776_hre_vote_cast }
 text = { trigger = { has_variable = aor1776_hre_ui_vote_promised exists = var:aor1776_hre_ui_vote_choice } localization_key = aor1776_hre_vote_promised }
 text = { trigger = { is_ai = no NOT = { exists = var:aor1776_hre_ui_vote_choice } } localization_key = aor1776_hre_vote_human }
 text = { trigger = { exists = var:aor1776_hre_ui_vote_choice } localization_key = aor1776_hre_vote_predicted }
 text = { localization_key = aor1776_hre_vote_none }''')
 files['common/customizable_localization/1776_imperial_electoral_display.txt']=custom
 L('aor1776_hre_free_cities_heading','The imperial free cities — relations with the Emperor','Les villes libres impériales — relations avec l’empereur')
 L('aor1776_hre_dashboard_decisions','Imperial deliberations: electors vote in the election journal during the thirty-day ballot. The Emperor’s centralization decisions unlock after all four principles reach III. Further imperial decisions will be added here when their rules are agreed.','Délibérations impériales : les électeurs votent dans le journal électoral pendant le scrutin de trente jours. Les décisions de centralisation de l’empereur s’ouvrent après les quatre principes III. D’autres décisions impériales seront ajoutées ici après définition de leurs règles.')
 for lang,idx in [('english',0),('french',1)]:
  files[f'localization/{lang}/1776_imperial_dashboard_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[idx].replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())
 return files
