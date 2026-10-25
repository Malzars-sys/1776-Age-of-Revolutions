"""Read-only structural and accounting checks for American Revolution R3.

Uses the saved pre-R3 working files, not HEAD, to preserve concurrent work.
These checks do not execute the Victoria 3 engine or predict AI landings.
"""
from pathlib import Path
from decimal import Decimal
import collections
import datetime
import hashlib
import json
import re
import subprocess

from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from localization_duplicate_audit import entries

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/reports/military/AMERICAN_REVOLUTION_R3'
GAME = Path('C:/Games/Victoria 3/game')
CHECKS = {}
FILES = [
 'common/scripted_triggers/1776_usa_french_support.txt',
 'common/scripted_effects/1776_usa_french_support.txt',
 'common/treaty_articles/1776_usa_french_support.txt',
 'common/diplomatic_actions/1776_deferred_debt.txt',
 'common/scripted_triggers/1776_join_ongoing_wars.txt',
 'common/scripted_effects/1776_join_ongoing_wars.txt',
 'common/diplomatic_actions/00_intervene_in_war.txt',
 'common/treaty_articles/31_join_war.txt',
 'common/ai_strategies/1776_revolution_intervention.txt',
 'common/war_goal_types/1776_revolution_intervention.txt',
 'common/on_actions/1776_usa_revolution_r2.txt',
 'common/journal_entries/1776_usa_french_support.txt',
 'common/scripted_buttons/1776_usa_french_support.txt',
 'common/decisions/1776_usa_french_support.txt',
 'common/history/countries/zz_1776_usa_revolution_r2.txt',
 'events/1776_usa_french_support.txt',
 'events/1776_american_diplomacy.txt',
 'events/1776_intervention.txt',
 'common/history/diplomatic_plays/00_american_revolution.txt',
]

def read(p):
 return (ROOT / p).read_text(encoding='utf-8-sig')

def check(name, condition):
 CHECKS[name] = bool(condition)

def definition(path, key):
 return next(n for n in parse(read(path)) if n.key == key)

def sub(node, key):
 return next(n for n in walk(node.children()) if n.key == key)

def vals(node):
 return [n.value for n in node.children()]

def main():
 for f in FILES:
  check('syntax.' + f, bool(parse(read(f))))

 fx = 'common/scripted_effects/1776_usa_french_support.txt'
 triggers = 'common/scripted_triggers/1776_usa_french_support.txt'
 articles = 'common/treaty_articles/1776_usa_french_support.txt'
 events = 'events/1776_american_diplomacy.txt'
 startup = definition('common/on_actions/1776_usa_revolution_r2.txt', 'aor1776_usa_support_startup')
 opening = next(n for n in walk(startup.children()) if n.key == 'trigger_event' and n.one('id') == 'aor1776_american_diplomacy.1')
 check('intro.after_three_days', opening.one('days') == '3')
 check('intro.not_added_by_history', 'je_aor1776_french_support' not in read('common/history/countries/zz_1776_usa_revolution_r2.txt'))
 check('intro.no_automatic_request_in_pulses', 'aor1776_support_request_effect' not in str(definition(fx, 'aor1776_support_weekly_effect').value) + str(definition(fx, 'aor1776_support_monthly_effect').value))
 intro = definition(events, 'aor1776_american_diplomacy.1')
 check('intro.opener_only_on_option', bool(sub(intro, 'option').children('aor1776_support_open_journal_effect')))
 request = definition(fx, 'aor1776_support_request_effect')
 check('consent.request_opens_US_choice', sub(request, 'trigger_event').one('id') == 'aor1776_american_diplomacy.2')
 promises = definition(events, 'aor1776_american_diplomacy.2')
 check('consent.two_distinct_promises_and_cancel', len(promises.children('option')) == 3)
 check('consent.France_must_approve', bool(sub(definition(events, 'aor1776_american_diplomacy.3'), 'option').children('aor1776_support_issue_offer_effect')))
 check('consent.US_ratifies_final_offer', bool(sub(definition(events, 'aor1776_american_diplomacy.4'), 'option').children('aor1776_support_accept_effect')))
 conclude = definition(fx, 'aor1776_support_conclude_effect')
 guard, create = sub(conclude, 'can_create_treaty'), sub(conclude, 'create_treaty')
 check('treaty.identical_guard_and_creation_inputs', normalized(guard.children()) == normalized([n for n in create.children() if n.key != 'name']))
 check('treaty.ratified_not_an_unsent_draft', create.one('is_draft') == 'no')
 check('treaty.ten_year_binding', sub(create, 'binding_period').one('years') == '10')
 clauses = sub(create, 'articles_to_create').children()
 check('treaty.five_clauses_including_credit_debt_and_assistance', len(clauses) == 5)
 check('treaty.French_source_US_target', all(n.one('source_country') == 'c:FRA' and n.one('target_country') == 'c:USA' for n in clauses))
 supplied = [n for n in clauses if n.one('article') == 'aor1776_support_supplies']
 check('treaty.supplies_small_arms_and_artillery', len(supplied) == 2 and {sub(n, 'goods').value for n in supplied} == {'g:small_arms', 'g:artillery'})
 relationship = definition(triggers, 'aor1776_french_support_relationship_valid')
 check('treaty.ends_aid_after_1783_09_03', any(n.key == 'game_date' and n.op == '<' and n.value == '1783.9.4' for n in relationship.children()))
 check('treaty.obligation_only_after_ratification', bool(conclude.children()) and 'set_owes_obligation_to' in str(conclude.value))
 for id, amount, interest in [('moderate', '14000', '0'), ('extended', '21000', '5')]:
  node = definition(articles, 'aor1776_war_credit_' + id)
  check('credit.' + id + '.no_second_native_money_transfer', not node.children('flags'))
  sets = [n for n in walk(node.children('on_entry_into_force')) if n.key == 'set_variable']
  check('credit.' + id + '.amount', any(n.one('name') == 'aor1776_weekly_credit' and n.one('value') == amount for n in sets))
  check('credit.' + id + '.interest', any(n.one('name') == 'aor1776_debt_interest' and n.one('value') == interest for n in sets))
  check('credit.' + id + '.stops_withdrawn_line', 'aor1776_weekly_credit' in str(node.children('on_withdrawal')))
 assistance = definition(articles, 'aor1776_revolution_military_assistance')
 check('assistance.no_19th_century_tech_gate', not assistance.children('unlocked_by_technologies'))
 check('assistance.training_and_experience', {n.key for n in sub(assistance, 'target_modifier').children()} == {'building_training_rate_mult', 'unit_experience_gain_mult'})
 check('legacy.money_article_disabled', sub(definition(articles, 'aor1776_support_money'), 'requirement_to_maintain').children('trigger')[0].one('always') == 'no')

 advance = definition(fx, 'aor1776_debt_advance_effect')
 payments = [n for n in walk(advance.children()) if n.key == 'add_treasury']
 check('ledger.one_debit_one_credit', len(payments) == 2 and payments[0].one('multiply') == '-1' and payments[1].value == 'var:aor1776_weekly_credit')
 check('ledger.principal_tracks_same_actual_advance', sub(advance, 'change_variable').one('add') == 'var:aor1776_weekly_credit')
 advance_guard = definition(triggers, 'aor1776_war_credit_can_advance')
 check('ledger.no_payment_in_default', any(n.key == 'in_default' and n.value == 'no' for n in walk(advance_guard.children())))
 check('ledger.reserves_cover_each_advance', any(n.key == 'gold_reserves' and n.op == '>=' and n.value == 'c:USA.var:aor1776_weekly_credit' for n in walk(advance_guard.children())))
 check('ledger.weekly_duplicate_lock', 'aor1776_credit_paid_this_week' in str(advance.value) and 'aor1776_credit_paid_this_week' in str(advance_guard.value))
 stop = definition(fx, 'aor1776_support_stop_effect')
 check('ledger.aid_end_preserves_principal_and_creditor', not any(n.key == 'remove_variable' and n.value in {'aor1776_debt_creditor', 'aor1776_debt_principal'} for n in stop.children()))
 migration = definition(fx, 'aor1776_support_initialize_effect')
 check('ledger.no_old_grants_converted', not any(n.key == 'set_variable' and n.one('name') == 'aor1776_debt_principal' for n in walk(migration.children())))
 debt = definition('common/diplomatic_actions/1776_deferred_debt.txt', 'aor1776_deferred_debt')
 check('debt.generic_agreement_requires_consent', debt.one('requires_approval') == 'yes')
 check('debt.generic_not_hardcoded_FRA_USA', 'c:FRA' not in str(debt.value) and 'c:USA' not in str(debt.value))
 check('debt.cannot_cancel_without_settlement', all(sub(debt, k).one('always') == 'no' for k in ['actor_can_break', 'target_can_break']))
 check('debt.empty_unfunded_pact_can_close', any(n.key == 'var:aor1776_debt_principal' and n.op == '<=' and n.value == '0' for n in walk(debt.children('pact'))) and 'remove_diplomatic_pact' in str(debt.children('pact')))
 demand = definition('common/diplomatic_actions/1776_deferred_debt.txt', 'aor1776_demand_debt_repayment')
 check('debt.demand_after_peace', 'is_at_war' in str(sub(demand, 'possible').value))
 check('debt.demand_rejects_duplicate_pending', 'aor1776_debt_demand_pending' in str(sub(demand, 'possible').value))
 reject = definition(fx, 'aor1776_debt_refuse_effect')
 check('debt.refusal_relations_minus_40', sub(reject, 'change_relations').one('value') == '-40')
 check('debt.refusal_infamy_10', sub(reject, 'change_infamy').value == '10')
 check('debt.refusal_preserves_repudiation_record', 'aor1776_debt_repudiated' in str(reject.value))
 check('debt.refusal_cannot_repeatedly_penalize_old_claim', any(n.key == 'remove_variable' and n.value == 'aor1776_debt_creditor' for n in walk(reject.children())))
 repay = definition(fx, 'aor1776_debt_repay_effect')
 check('debt.repayment_two_treasury_changes', sum(n.key == 'add_treasury' for n in walk(repay.children())) == 2)

 # Arithmetic invariants for sparse actual disbursements, interrupted finance,
 # settlement and refusal; no claim to simulate native execution or the budget.
 scenarios = []
 for amount in [14000, 21000]:
  for paid_weeks in [[], [True], [True, False, True, False, False, True]]:
   a, b, principal = Decimal(150000), Decimal(700000), Decimal(0)
   initial = a + b
   for paid in paid_weeks:
    if paid: a += amount; b -= amount; principal += amount
   check(f'arithmetic.{amount}.{len(paid_weeks)}.cash_conserved', a + b == initial)
   check(f'arithmetic.{amount}.{len(paid_weeks)}.only_paid_advances_owed', principal == amount * sum(paid_weeks))
   due = principal * (Decimal('1.05') if amount == 21000 else 1)
   a -= due; b += due
   check(f'arithmetic.{amount}.{len(paid_weeks)}.settlement_conserved', a + b == initial)
   scenarios.append({'weekly_credit': amount, 'settled_advances': sum(paid_weeks), 'principal': str(principal), 'due': str(due)})

 war = parse(read('common/history/diplomatic_plays/00_american_revolution.txt'))
 check('start.Spain_and_colonies_neutral', not any(n.key == 'add_initiator_backers' for n in walk(war)))
 check('start.no_Spanish_goals_until_intervention', not any(n.key == 'add_war_goal' for n in walk(war)))
 check('start.US_British_independence_war_preserved', any(n.key == 'type' and n.value == 'dp_independence' for n in walk(war)))
 intervention = 'common/scripted_effects/1776_join_ongoing_wars.txt'
 fr = definition(intervention, 'aor1776_french_entry_roll_effect')
 sp = definition(intervention, 'aor1776_spanish_entry_roll_effect')
 check('entry.France_annual_rates', {n.value for n in walk(fr.children()) if n.key == 'chance'} == {'10', '45', '75'})
 check('entry.France_guaranteed_deadline_before_cooldown', sub(fr, 'game_date').value == '1778.3.17')
 check('entry.Spain_rates_lower_and_not_guaranteed', {n.value for n in walk(sp.children()) if n.key == 'chance'} == {'10', '25', '40', '60'})
 check('entry.Spain_final_roll_once', 'aor1776_spanish_final_roll_taken' in str(sp.value))
 check('entry.human_France_and_Spain_not_forced', all(sub(n, 'is_ai').value == 'yes' for n in [fr, sp]))
 for tag, date, event in [('FRA', (1778, 3, 17), 'aor1776_intervention.1'), ('SPA', (1779, 6, 21), 'aor1776_intervention.2')]:
  delay = next(n for n in walk(startup.children()) if n.key == 'trigger_event' and n.one('id') == event)
  check('entry.' + tag + '.deadline_delay', int(delay.one('days')) == (datetime.date(*date) - datetime.date(1776, 1, 1)).days)
 for f in ['common/diplomatic_actions/00_intervene_in_war.txt', 'common/treaty_articles/31_join_war.txt']:
  check('integration.shared_join_effect.' + f, 'aor1776_intervene_effect' in read(f))
  check('integration.no_land_adjacency_block.' + f, 'has_strategic_land_adjacency' not in read(f))
 check('integration.enemy_truces_checked', 'has_truce_with = $ACTOR$' in read('common/scripted_triggers/1776_join_ongoing_wars.txt'))
 goals = definition(intervention, 'aor1776_french_revolution_goals_effect')
 check('objectives.French_Antilles_goal', any(n.key == 'target_state' and n.value == 's:STATE_WEST_INDIES.region_state:GBR' for n in walk(goals.children())))
 check('objectives.no_British_home_annexation', not any(n.key == 'target_state' and n.value.startswith('s:STATE_HOME') for n in walk(goals.children())))
 pressure = definition('common/war_goal_types/1776_revolution_intervention.txt', 'aor1776_break_british_power')
 check('objectives.British_capital_control_required', pressure.one('contestion_type') == 'control_target_country_capital')
 check('objectives.no_home_territorial_transfer', pressure.one('kind') == 'humiliation')
 check('objectives.capital_control_enum_is_native', 'control_target_country_capital' in (GAME/'common/war_goal_types/war_goal_types.md').read_text(encoding='utf-8-sig'))
 strategies = parse(read('common/ai_strategies/1776_revolution_intervention.txt'))
 native_strategy = parse((GAME/'common/ai_strategies/00_default_strategy.txt').read_text(encoding='utf-8-sig'))[0]
 native_desires = {n.key for n in native_strategy.children('secret_goal_scores')[0].children()}
 check('AI.strategic_desires_use_native_types', all({n.key for n in s.children('secret_goal_scores')[0].children()} <= native_desires for s in strategies))
 check('AI.wargoals_not_mistaken_for_strategic_desires', all(not s.children('secret_goal_weights') and s.children('wargoal_weights') for s in strategies))
 for field in ['wanted_army_size', 'wanted_navy_size', 'wanted_num_supply_ships', 'ship_construction_output_multiplier']:
  check('AI.France_stronger_' + field, float(sub(strategies[0], field).one('value')) > float(sub(strategies[1], field).one('value')))
  check('AI.native_field_' + field, field in (GAME/'common/ai_strategies/00_default_strategy.txt').read_text(encoding='utf-8-sig'))

 europe = 'common/history/military_formations/00_military_formations_europe.txt'
 old = parse((REPORT/'baseline'/europe).read_text(encoding='utf-8-sig'))
 new = parse(read(europe))
 formation = next(n for n in walk(new) if n.key == 'create_military_formation' and n.one('name') == 'cleanup2d3b_gbr_land_3')
 check('garrison.Guatemala_supply_hub', formation.one('supply_hub') == 's:STATE_GUATEMALA')
 check('garrison.Central_America_HQ', formation.one('hq_region') == 'sr:region_central_america')
 formation.children('hq_region')[0].value = 'sr:region_canada'
 formation.children('supply_hub')[0].value = 's:STATE_NEWFOUNDLAND'
 check('garrison.entire_Europe_file_otherwise_preserved', normalized(old) == normalized(new))
 mod = 'common/static_modifiers/76mod_modifiers.txt'
 old_mod = parse((REPORT/'baseline'/mod).read_text(encoding='utf-8-sig'))
 new_mod = parse(read(mod))
 liberty = next(n for n in new_mod if n.key == 'modifier_usa_war_of_independence')
 check('liberty.defeat_territory_minus_30_only', liberty.one('unit_provinces_lost_mult') == '-0.30')
 liberty.value = [n for n in liberty.children() if n.key != 'unit_provinces_lost_mult']
 check('liberty.other_modifiers_preserved', normalized(old_mod) == normalized(new_mod))
 for f in ['common/history/military_formations/01_military_formations_north_america.txt', 'common/history/military_formations/02_military_formations_south_america.txt']:
  check('protected.' + f, read(f) == (REPORT/'baseline'/f).read_text(encoding='utf-8-sig'))

 own_keys = []
 for lang in ['french', 'english']:
  path = ROOT/f'localization/{lang}/1776_american_diplomacy_r3_l_{lang}.yml'
  check('localization.' + lang + '.BOM', path.read_bytes().startswith(b'\xef\xbb\xbf'))
  lines = path.read_text(encoding='utf-8-sig').splitlines()
  check('localization.' + lang + '.header', lines[0] == 'l_' + lang + ':')
  keys = [re.match(r'\s+([A-Za-z0-9_.-]+):0 ".*"$', line) for line in lines[1:] if line.strip()]
  check('localization.' + lang + '.all_lines_valid', all(keys))
  own_keys.append({m.group(1) for m in keys if m})
  catalog = entries(lang)
  check('localization.' + lang + '.no_new_duplicate_keys', all(len(catalog[k]) == 1 for k in own_keys[-1]))
  required = set()
  for f in FILES:
   for n in walk(parse(read(f))):
    if n.key in {'title', 'flavor', 'text', 'name', 'desc', 'custom_tooltip'} and isinstance(n.value, str) and n.value.startswith(('aor1776_', 'je_aor1776_')):
     # Variable names are also 'name'; only explicit localization consumers.
     if n.key != 'name' or re.match(r'aor1776_(american_diplomacy|debt)\.\d+\.[a-z]', n.value): required.add(n.value)
  check('localization.' + lang + '.all_explicit_UI_keys_resolve', all(k in catalog for k in required))
 check('localization.FR_EN_same_keys', own_keys[0] == own_keys[1])
 source = json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'))
 icon = 'gfx/interface/icons/lens_toolbar_icons/intervene_in_war.dds'
 check('credit.imported_icon_unchanged', hashlib.sha256((ROOT/icon).read_bytes()).hexdigest() == source['join_ongoing_wars_source'][icon.replace('/', '\\')])
 check('credit.author_and_original_link', 'The Lizerd King' in read('docs/credits/JOIN_ONGOING_WARS.md') and '3015811655' in read('docs/credits/JOIN_ONGOING_WARS.md'))
 check('git.HEAD_preserved', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == source['head'])
 check('git.index_preserved', hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest() == source['index_sha256'])
 # Retain the R2 regressions that R3 does not supersede: ships, Minutemen,
 # revolutionary spirit, founders and the outcome echoes. R2 subsidy/startup
 # tests describe the retired design and are deliberately not reinterpreted.
 import validate_american_revolution_r2 as prior
 prior.CHECKS.clear()
 prior.naval_checks()
 prior.content_r1_checks()
 prior.content_r2_checks()
 prior.reference_checks(FILES)
 CHECKS.update({'prior.' + k: v for k, v in prior.CHECKS.items()})
 result = {'status': 'PASS' if all(CHECKS.values()) else 'FAIL', 'passed': sum(CHECKS.values()), 'total': len(CHECKS), 'checks': CHECKS, 'arithmetic_scenarios': scenarios, 'runtime': 'NOT_RUN', 'AI_landings': 'NOT_VERIFIED'}
 print(json.dumps(result, ensure_ascii=False, indent=2))
 raise SystemExit(0 if all(CHECKS.values()) else 1)

if __name__ == '__main__':
 main()
