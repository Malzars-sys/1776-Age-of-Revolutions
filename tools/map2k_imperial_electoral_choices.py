"""Anticipated country votes, amendable human ballots and valued treaty pledges."""
import re
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2k_imperial_feedback import block, child, append_inside, replace_node, EF, DA, EV

TRIG='common/scripted_triggers/1776_imperial_constitution.txt'
JE='common/journal_entries/1776_imperial_situation.txt'
ARTICLE='common/treaty_articles/1776_imperial_electoral_promise.txt'
BREAK_INFAMY=10

def augment_electoral_choices(files, members):
 loc={}
 def L(k,en,fr):loc[k]=(en,fr)
 for k in ['je_aor1776_hre_situation','je_aor1776_hre_vote']:
  files[JE]=child(files[JE],k,'should_be_pinned_by_default_uninvolved_or_context','should_be_pinned_by_default_uninvolved_or_context = yes')
 files[JE]=child(files[JE],'je_aor1776_hre_situation','is_shown_in_lobby','is_shown_in_lobby = { aor1776_hre_member = yes }')
 # Country-context pin flag and lobby trigger are documented by the installed
 # 1.13.11 journal_entries.md / 00_canada_australia.txt. No country history edit.
 files[JE]=append_inside(files[JE],'je_aor1776_hre_situation','\n'.join('scripted_button = aor1776_hre_vote_'+t for t in members))
 files[TRIG]+=block('aor1776_hre_can_choose_electoral_vote','''
 aor1776_hre_elector = yes
 $CANDIDATE$ ?= { aor1776_hre_ballot_candidate = yes }
 OR = {
  NOT = { has_global_variable = aor1776_hre_election_open }
  AND = { has_variable = aor1776_hre_voter_this_round
   global_var:aor1776_hre_emperor_country ?= { has_variable = aor1776_hre_deliberation }
  }
 }
 OR = {
  NOT = { exists = var:aor1776_hre_promised_candidate }
  var:aor1776_hre_promised_candidate ?= $CANDIDATE$
  var:aor1776_hre_promised_candidate ?= { aor1776_hre_ballot_candidate = no }
  AND = { is_ai = no has_global_variable = aor1776_hre_election_open }
 }
''')
 files[EF]+=block('aor1776_hre_choose_electoral_vote','''
 if = { limit = { aor1776_hre_can_choose_electoral_vote = { CANDIDATE = scope:hre_vote_choice } }
  set_variable = { name = aor1776_hre_preferred_candidate value = scope:hre_vote_choice }
  if = { limit = { has_global_variable = aor1776_hre_election_open }
   aor1776_hre_cast_vote = yes
   aor1776_hre_tally_ballot = yes
  }
  else = { aor1776_hre_update_vote_preview = yes }
 }
''')
 cast=f'''
 if = {{ limit = {{ aor1776_hre_elector = yes has_global_variable = aor1776_hre_election_open
  has_variable = aor1776_hre_voter_this_round
  exists = scope:hre_vote_choice scope:hre_vote_choice = {{ aor1776_hre_ballot_candidate = yes }}
  OR = {{ NOT = {{ has_variable = aor1776_hre_voted }}
   global_var:aor1776_hre_emperor_country ?= {{ has_variable = aor1776_hre_deliberation }}
  }}
  OR = {{ NOT = {{ exists = var:aor1776_hre_promised_candidate }}
   var:aor1776_hre_promised_candidate ?= scope:hre_vote_choice
   var:aor1776_hre_promised_candidate ?= {{ aor1776_hre_ballot_candidate = no }}
   is_ai = no
  }}
 }}
  if = {{ limit = {{ is_ai = no exists = var:aor1776_hre_promised_candidate
   var:aor1776_hre_promised_candidate ?= {{ aor1776_hre_ballot_candidate = yes }}
   NOT = {{ var:aor1776_hre_promised_candidate ?= scope:hre_vote_choice }}
  }}
   change_infamy = {BREAK_INFAMY}
   remove_variable = aor1776_hre_promised_candidate
   remove_variable = aor1776_hre_promise_cast
  }}
  remove_variable = aor1776_hre_promise_cast
  if = {{ limit = {{ var:aor1776_hre_promised_candidate ?= scope:hre_vote_choice }} set_variable = aor1776_hre_promise_cast }}
  set_variable = aor1776_hre_voted
  set_variable = {{ name = aor1776_hre_voted_for value = scope:hre_vote_choice }}
  set_variable = {{ name = aor1776_hre_preferred_candidate value = scope:hre_vote_choice }}
  # Rebuild totals from one stored ballot per elector; changing a vote never
  # increments the elector count or leaves the former candidate's vote behind.
  aor1776_hre_recount_ballot = yes
  aor1776_hre_update_vote_preview = yes
 }}
'''
 files[EF]=replace_node(files[EF],'aor1776_hre_cast_vote',block('aor1776_hre_cast_vote',cast))
 ai='''
 save_scope_as = hre_voter
 if = { limit = { exists = var:aor1776_hre_promised_candidate
  var:aor1776_hre_promised_candidate ?= { aor1776_hre_ballot_candidate = yes } }
  var:aor1776_hre_promised_candidate = { save_scope_as = hre_vote_choice }
  aor1776_hre_cast_vote = yes
 }
 else = {
  ordered_country = { limit = { aor1776_hre_ballot_candidate = yes }
   order_by = aor1776_hre_vote_preference position = 0 check_range_bounds = no
   save_scope_as = hre_vote_choice
   scope:hre_voter = { aor1776_hre_cast_vote = yes }
  }
 }
'''
 files[EF]=replace_node(files[EF],'aor1776_hre_ai_ballot',block('aor1776_hre_ai_ballot',ai))
 files[EF]+=block('aor1776_hre_update_unpledged_ballots','''
 if = { limit = { has_global_variable = aor1776_hre_election_open
  global_var:aor1776_hre_emperor_country ?= { has_variable = aor1776_hre_deliberation } }
  every_country = { limit = { is_ai = yes aor1776_hre_elector = yes
   has_variable = aor1776_hre_voter_this_round
   NOT = { var:aor1776_hre_promised_candidate ?= { aor1776_hre_ballot_candidate = yes } }
  } aor1776_hre_ai_ballot = yes }
 }
''')
 # Reuse the existing seven-day dashboard guard. Preview remains display-only.
 event=next(n for n in cw.parse(files[EV]) if n.key=='aor1776_hre.40')
 raw=files[EV][event.start:event.end]
 assert raw.count('aor1776_hre_feedback_refresh = yes')==1
 raw=raw.replace('aor1776_hre_feedback_refresh = yes','aor1776_hre_feedback_refresh = yes aor1776_hre_update_unpledged_ballots = yes')
 files[EV]=edits(files[EV],[(event.start,event.end,raw)])
 files[EF]+=block('aor1776_hre_register_initial_ballot','''
 if = { limit = { exists = var:aor1776_hre_promised_candidate
  var:aor1776_hre_promised_candidate ?= { aor1776_hre_ballot_candidate = yes } }
  var:aor1776_hre_promised_candidate = { save_scope_as = hre_vote_choice }
  aor1776_hre_cast_vote = yes
 }
 else_if = { limit = { is_ai = no exists = var:aor1776_hre_preferred_candidate
  var:aor1776_hre_preferred_candidate ?= { aor1776_hre_ballot_candidate = yes } }
  var:aor1776_hre_preferred_candidate = { save_scope_as = hre_vote_choice }
  aor1776_hre_cast_vote = yes
 }
 else_if = { limit = { is_ai = yes } aor1776_hre_ai_ballot = yes }
''')
 start=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_start_ballot')
 raw=files[EF][start.start:start.end]
 marker=' every_country = { limit = { has_variable = aor1776_hre_voter_this_round is_ai = no }'
 assert marker in raw
 raw=raw.replace(marker,' every_country = { limit = { has_variable = aor1776_hre_voter_this_round aor1776_hre_elector = yes } aor1776_hre_register_initial_ballot = yes }\n'+marker,1)
 files[EF]=edits(files[EF],[(start.start,start.end,raw)])
 # Native scripted buttons support choosing oneself; diplomatic actions to
 # another country provide the same operation from its country panel.
 files['common/scripted_buttons/1776_imperial_voting.txt']=''.join(block('aor1776_hre_vote_'+t,f'''
 name = aor1776_hre.choose_{t}
 desc = aor1776_hre_choose_vote_desc
 visible = {{ aor1776_hre_elector = yes c:{t} ?= {{ aor1776_hre_ballot_candidate = yes }} }}
 possible = {{ aor1776_hre_can_choose_electoral_vote = {{ CANDIDATE = c:{t} }} }}
 effect = {{ custom_tooltip = aor1776_hre_choose_vote_result
  hidden_effect = {{ c:{t} = {{ save_scope_as = hre_vote_choice }} aor1776_hre_choose_electoral_vote = yes }} }}
 ai_chance = {{ value = 0 }}
''') for t in members)
 files[DA]+=block('aor1776_hre_choose_electoral_candidate','''
 groups = { general power_bloc }
 requires_approval = no
 should_notify_third_parties = no
 show_in_lens = no
 show_effect_in_tooltip = yes
 texture = "gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_obligation.dds"
 selectable = { aor1776_hre_elector = yes }
 potential = { NOT = { this = scope:target_country } scope:target_country = { aor1776_hre_candidate = yes } }
 possible = { aor1776_hre_can_choose_electoral_vote = { CANDIDATE = scope:target_country } }
 accept_effect = { custom_tooltip = aor1776_hre_choose_vote_result
  hidden_effect = { scope:target_country = { save_scope_as = hre_vote_choice } aor1776_hre_choose_electoral_vote = yes } }
 ai = { will_propose = { always = no } }
''')
 # Explicit direct selection buttons on elector cards, including the viewer's
 # own card. The native country-panel button remains available as a fallback.
 files['common/scripted_guis/1776_imperial_electoral_choice.txt']=block('aor1776_hre_choose_vote_gui','''
 scope = country
 is_shown = { aor1776_hre_elector = yes }
 is_valid = { aor1776_hre_can_choose_electoral_vote = { CANDIDATE = scope:hre_vote_choice } }
 effect = { aor1776_hre_choose_electoral_vote = yes }
''')
 gui='gui/journal_entry_widgets/1776_imperial_widgets.gui';raw=files[gui]
 card=cw.parse(raw)
 candidate_row=next(n for n in cw.walk(card) if n.key=='widget' and cw.scalar(n.one('name'))=='aor1776_hre_elector_row')
 rowraw=raw[candidate_row.start:candidate_row.end]
 rowraw=rowraw.replace('size = { 500 110 }','size = { 500 150 }').replace('size = { 380 100 }','size = { 380 140 }')
 # A child button explicitly uses the local player as voter and the card's
 # Country as candidate; it does not ask the candidate to approve the vote.
 country_button=next(n for n in cw.walk(cw.parse(rowraw)) if n.key=='button')
 vote_button='''
     button = {
      name = "aor1776_hre_card_vote"
      position = { 0 102 } size = { 380 35 }
      using = default_button_action
      visible = "[GetScriptedGui('aor1776_hre_choose_vote_gui').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('hre_vote_choice', Country.MakeScope).End)]"
      enabled = "[GetScriptedGui('aor1776_hre_choose_vote_gui').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('hre_vote_choice', Country.MakeScope).End)]"
      onclick = "[GetScriptedGui('aor1776_hre_choose_vote_gui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('hre_vote_choice', Country.MakeScope).End)]"
      tooltip = "aor1776_hre_choose_vote_desc"
      textbox = { size = { 375 35 } using = fontsize_medium text = "aor1776_hre_card_vote_label" }
     }
'''
 # Use a sibling vote button within a sized wrapper, never a button inside
 # another clickable button (which could also open the country panel).
 buttonraw=rowraw[country_button.start:country_button.end]
 wrapper='widget = { size = { 380 140 }\n'+buttonraw.replace('size = { 380 140 }','size = { 380 100 }',1)+'\n'+vote_button+'\n}'
 rowraw=edits(rowraw,[(country_button.start,country_button.end,wrapper)])
 raw=edits(raw,[(candidate_row.start,candidate_row.end,rowraw)]).replace('addrow = 110','addrow = 150')
 files[gui]=raw
 # Preview ordering: actual ballot, binding treaty, human's free selection,
 # then historical AI estimate. It never casts a vote by itself.
 preview=next(n for n in cw.parse(files[EF]) if n.key=='aor1776_hre_update_vote_preview')
 raw=files[EF][preview.start:preview.end]
 raw=raw.replace('remove_variable = aor1776_hre_ui_vote_promised','remove_variable = aor1776_hre_ui_vote_promised\n remove_variable = aor1776_hre_ui_vote_selected')
 needle=' else_if = { limit = { is_ai = yes }'
 raw=raw.replace(needle,''' else_if = { limit = { is_ai = no exists = var:aor1776_hre_preferred_candidate
  var:aor1776_hre_preferred_candidate ?= { aor1776_hre_candidate = yes } }
  set_variable = { name = aor1776_hre_ui_vote_choice value = var:aor1776_hre_preferred_candidate }
  set_variable = aor1776_hre_ui_vote_selected
 }
'''+needle)
 files[EF]=edits(files[EF],[(preview.start,preview.end,raw)])
 custom='common/customizable_localization/1776_imperial_electoral_display.txt'
 n=next(n for n in cw.parse(files[custom]) if n.key=='aor1776_hre_vote_display')
 first=n.children('text')[2]
 files[custom]=edits(files[custom],[(first.start,first.start,'''text = { trigger = { has_variable = aor1776_hre_ui_vote_selected exists = var:aor1776_hre_ui_vote_choice } localization_key = aor1776_hre_vote_selected }
 ''')])
 # Treaty scoring is evaluated for each party: source = elector giving the
 # vote, target = country receiving it. Economic counter-offers are valued by
 # the engine's other articles, not added as free money by this pledge.
 score='''value = 0
 if = { limit = { scope:source_country ?= this }
  scope:source_country = { save_temporary_scope_as = hre_voter }
  add = { desc = aor1776_hre_pledge_accept_base value = -40 }
  add = { desc = aor1776_hre_pledge_accept_preference value = scope:target_country.aor1776_hre_vote_preference subtract = 20 min = -250 max = 100 }
  if = { limit = { owes_obligation_to = scope:target_country } add = { desc = aor1776_hre_pledge_accept_obligation value = 40 } }
  if = { limit = { exists = scope:treaty }
   if = { limit = { scope:treaty.binding_period >= 1825 }
    add = { desc = aor1776_hre_pledge_accept_duration value = scope:treaty.binding_period divide = 365 multiply = -2 min = -40 max = 0 }
   }
  }
 }
 else_if = { limit = { scope:target_country ?= this }
  add = { desc = aor1776_hre_pledge_accept_receiving value = 60 }
 }
'''
 files[ARTICLE]=child(files[ARTICLE],'aor1776_electoral_promise','ai',block('ai','''
 treaty_categories = { power_bloc }
 article_ai_usage = { request offer }
 evaluation_chance = { value = 0.1 }
 inherent_accept_score = { '''+score+''' }
'''))
 # The promise already supplies the initial country choice at the next death.
 article=next(n for n in cw.parse(files[ARTICLE]) if n.key=='aor1776_electoral_promise')
 entry=article.children('on_entry_into_force')[0]
 raw=files[ARTICLE][entry.start:entry.end]
 raw=raw.replace('scope:article_options.source_country = {','scope:article_options.source_country = {\n set_variable = { name = aor1776_hre_preferred_candidate value = scope:article_options.target_country }',1)
 source=cw.parse(raw)[0].children('scope:article_options.source_country')[0]
 raw=edits(raw,[(source.end-1,source.end-1,'\n aor1776_hre_update_vote_preview = yes\n')])
 files[ARTICLE]=edits(files[ARTICLE],[(entry.start,entry.end,raw)])
 n=next(n for n in cw.parse(files[ARTICLE]) if n.key=='aor1776_electoral_promise').children('can_ratify')[0]
 files[ARTICLE]=edits(files[ARTICLE],[(n.end-1,n.end-1,'\n scope:treaty.binding_period > 0 # A pledge must have a real binding duration.\n')])
 for t in members:L('aor1776_hre.choose_'+t,'Choose $'+t+'$ for the imperial vote','Choisir $'+t+'$ pour le vote impérial')
 L('aor1776_hre_choose_vote_desc','Choose a country for the next imperial election, including yourself if eligible. During the thirty-day ballot you may change your vote. Breaking a valid treaty pledge as a player costs 10 infamy once; an AI elector must honour its pledge.','Choisir un pays pour la prochaine élection impériale, y compris soi-même si éligible. Pendant les trente jours du scrutin, vous pouvez modifier votre vote. Un joueur qui rompt une promesse valide subit une fois 10 d’infamie ; un électeur IA doit respecter sa promesse.')
 L('aor1776_hre_choose_vote_result','Record this country as our electoral choice; if a ballot is open, replace our single ballot. A player changing away from a valid treaty pledge receives 10 infamy once.','Enregistrer ce pays comme notre choix électoral ; si le scrutin est ouvert, remplacer notre unique bulletin. Un joueur qui quitte le candidat d’une promesse valide reçoit une fois 10 d’infamie.')
 L('aor1776_hre_card_vote_label','Choose for my imperial vote','Choisir pour mon vote impérial')
 L('aor1776_hre_choose_electoral_candidate','Choose as imperial candidate','Choisir comme candidat impérial')
 L('aor1776_hre_choose_electoral_candidate_desc','Set our next imperial electoral choice. This is not a treaty pledge and does not require the candidate’s approval.','Définir notre choix pour la prochaine élection impériale. Ce n’est pas une promesse par traité et le candidat n’a pas à l’approuver.')
 L('aor1776_hre_vote_selected',"Chosen for next election: [SCOPE.GetRootScope.GetCountry.MakeScope.Var('aor1776_hre_ui_vote_choice').GetCountry.GetName]","Choix pour la prochaine élection : [SCOPE.GetRootScope.GetCountry.MakeScope.Var('aor1776_hre_ui_vote_choice').GetCountry.GetName]")
 L('je_aor1776_hre_vote_reason','Your anticipated choice is registered when the Emperor dies. Choose or change a candidate below during the thirty-day ballot, including yourself if eligible. Breaking a valid treaty pledge costs a player 10 infamy once. AI electors honour their pledges.','Votre choix anticipé est enregistré au décès de l’empereur. Choisissez ou changez de candidat ci-dessous pendant les trente jours du scrutin, y compris vous-même si éligible. Rompre une promesse valide coûte une fois 10 d’infamie à un joueur. Les électeurs IA respectent leurs promesses.')
 L('aor1776_hre_electors_heading','The electors — ballots and anticipated choices','Les électeurs — bulletins et choix anticipés')
 L('aor1776_hre_dashboard_decisions','Electors may choose a candidate now using the cards below or a country’s diplomatic actions; the journal’s candidate buttons also allow a self-vote when eligible. The choice becomes a ballot at the Emperor’s death and may be changed during thirty days. Centralization decisions unlock after all four principles reach III.','Les électeurs peuvent choisir un candidat dès maintenant depuis les fiches ci-dessous ou les actions diplomatiques du pays ; les boutons de candidats du journal permettent aussi de choisir son propre pays s’il est éligible. Le choix devient un bulletin au décès de l’empereur et peut être modifié pendant trente jours. Les décisions de centralisation s’ouvrent après les quatre principes III.')
 L('aor1776_hre.1.d','The imperial throne is vacant. Any valid treaty pledge or anticipated choice has already been registered as our ballot. We may choose or change a candidate in the imperial journal during the thirty-day deliberation. Breaking a valid pledge costs us 10 infamy; a free choice may be changed without this penalty. After deliberation, the electoral count seeks an absolute majority, with a runoff if needed.','Le trône impérial est vacant. Notre promesse valide ou notre choix anticipé a déjà été enregistré comme bulletin. Nous pouvons choisir ou changer de candidat dans le journal impérial pendant les trente jours de délibération. Rompre une promesse valide nous coûte 10 d’infamie ; un choix libre peut être modifié sans cette pénalité. À l’issue de la délibération, le dépouillement recherche une majorité absolue, avec un second tour si nécessaire.')
 for suffix,en,fr in [('base','Reluctance to bind our electoral freedom','Réticence à engager notre liberté électorale'),('preference','Historical electoral preference: relations, dynasty, religion, alliances and imperial continuity','Préférence électorale historique : relations, dynastie, religion, alliances et continuité impériale'),('obligation','Obligation owed to the candidate','Obligation due au candidat'),('duration','Long binding period','Longue durée d’engagement'),('receiving','Receiving an imperial electoral pledge','Obtention d’une promesse de voix impériale')]:L('aor1776_hre_pledge_accept_'+suffix,en,fr)
 for lang,idx in [('english',0),('french',1)]:
  for rel,raw in list(files.items()):
   if rel.startswith('localization/'+lang+'/'):
    files[rel]='\n'.join(line for line in raw.split('\n') if not any(re.match(r'\s*'+re.escape(k)+r':',line) for k in loc))
  files[f'localization/{lang}/1776_imperial_electoral_choices_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[idx].replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())
 files[EF]=files[EF].replace('var:aor1776_hre_promised_candidate = { aor1776_hre_ballot_candidate', 'var:aor1776_hre_promised_candidate ?= { aor1776_hre_ballot_candidate')
 return files
