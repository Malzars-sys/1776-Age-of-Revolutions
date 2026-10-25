"""Read-only R4 regressions: native finance, deferred debt and two player paths.

These are structural, reference, asset and arithmetic checks, not an execution
of Victoria 3. R2/R3 validators remain records of their superseded designs.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import struct
import subprocess

from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from localization_duplicate_audit import entries
from validate_american_revolution_r3 import FILES as R3_FILES

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/reports/military/AMERICAN_REVOLUTION_R4'
GAME = Path('C:/Games/Victoria 3/game')
CHECKS = {}
FILES = set(R3_FILES) | {'common/diplomatic_actions/1776_call_family_compact.txt',
                        'common/scripted_effects/1776_usa_echoes.txt'}
for folder in ['events', 'common/decisions', 'common/scripted_effects',
               'common/scripted_triggers', 'common/character_templates',
               'common/history/characters', 'common/history/countries',
               'common/on_actions', 'common/journal_entries', 'common/laws',
               'common/static_modifiers', 'common/ship_types',
               'common/ship_modifications', 'common/scripted_buttons']:
    FILES.update(str(p.relative_to(ROOT)).replace('\\', '/')
                 for p in (ROOT / folder).glob('*1776*usa*.txt'))
FILES = sorted(FILES)


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def tree(path):
    return parse(read(path))


def definition(path, key):
    return next(n for n in tree(path) if n.key == key)


def sub(node, key):
    return next(n for n in walk(node.children()) if n.key == key)


def check(name, value):
    CHECKS[name] = bool(value)


def contains(node, key, value=None):
    return any(n.key == key and (value is None or n.value == value)
               for n in walk(node.children()))


def main():
    for path in FILES:
        check('syntax.' + path, bool(tree(path)))
    fx = 'common/scripted_effects/1776_usa_french_support.txt'
    art = 'common/treaty_articles/1776_usa_french_support.txt'
    ev = 'events/1776_american_diplomacy.txt'
    trig = 'common/scripted_triggers/1776_usa_french_support.txt'
    on = 'common/on_actions/1776_usa_revolution_r2.txt'
    conclude = definition(fx, 'aor1776_support_conclude_effect')
    guard, create = sub(conclude, 'can_create_treaty'), sub(conclude, 'create_treaty')
    clauses = sub(create, 'articles_to_create').children()
    check('treaty.ratified_native_ten_years', create.one('is_draft') == 'no'
          and sub(create, 'binding_period').one('years') == '10')
    check('treaty.five_ordered_clauses', [n.one('article') for n in clauses] == [
        'aor1776_support_money', 'aor1776_deferred_debt_article',
        'aor1776_revolution_military_assistance', 'aor1776_support_supplies',
        'aor1776_support_supplies'])
    check('treaty.finance_guard_matches_created_prefix',
          normalized(sub(guard, 'articles_to_create').children()) == normalized(clauses[:3]))
    check('treaty.no_observed_unsupported_goods_in_can_create', not contains(guard, 'goods'))
    check('treaty.shipping_guard_present', contains(conclude, 'is_market_reachable_for_trade', 'c:USA.market'))
    check('treaty.money_France_to_US', clauses[0].one('source_country') == 'c:FRA'
          and clauses[0].one('target_country') == 'c:USA'
          and sub(clauses[0], 'quantity').value == '30000')
    check('treaty.IOU_US_to_France', clauses[1].one('source_country') == 'c:USA'
          and clauses[1].one('target_country') == 'c:FRA')
    check('treaty.fifteen_arms_one_artillery',
          [(sub(n, 'goods').value, sub(n, 'quantity').value) for n in clauses[3:]]
          == [('g:small_arms', '15'), ('g:artillery', '1')])
    money = definition(art, 'aor1776_support_money')
    check('finance.native_money_flag_and_input',
          any(n.value == 'is_money_transfer' for n in sub(money, 'flags').children())
          and any(n.value == 'quantity' for n in sub(money, 'required_inputs').children()))
    check('finance.no_central_banking_gate', not money.children('unlocked_by_technologies'))
    check('finance.native_default_freeze', sub(money, 'non_fulfillment').one('consequences') == 'freeze'
          and contains(money, 'in_default', 'yes'))
    check('finance.no_hidden_payment_in_ratification', not contains(conclude, 'add_treasury'))
    for key in ['aor1776_debt_advance_effect', 'aor1776_support_weekly_effect']:
        check('finance.retired_empty.' + key, definition(fx, key).children() == [])
    pact = definition('common/diplomatic_actions/1776_deferred_debt.txt', 'aor1776_deferred_debt')
    check('finance.no_second_weekly_payer', not contains(pact, 'weekly_effect'))
    check('finance.no_peace_or_1783_cutoff', not contains(money, 'aor1776_usa_independence_war_active')
          and not contains(definition(trig, 'aor1776_support_contract_parties_valid'), 'game_date'))
    check('finance.ten_year_active_flag', any(n.key == 'set_variable'
          and n.one('name') == 'aor1776_support_active' and n.one('years') == '10'
          for n in walk(definition(fx, 'aor1776_support_accept_effect').children())))
    check('debt.obligation_only_in_ratification', contains(conclude, 'set_owes_obligation_to'))
    principal = [n for n in walk(conclude.children()) if n.key == 'set_variable'
                 and n.one('name') == 'aor1776_debt_principal']
    check('debt.principal_uses_native_binding_days', len(principal) == 2
          and any(sub(n, 'value').one('multiply') == 'scope:aor1776_debt_contract.binding_period'
                  and sub(n, 'value').one('divide') == '7' for n in principal))
    check('debt.nested_numeric_formula_not_effect_siblings', all(
        {x.key for x in n.children()} == {'name', 'value'} for n in principal))
    check('debt.ten_year_fallback_lock', any(n.key == 'set_variable'
          and n.one('name') == 'aor1776_debt_binding_lock' and n.one('years') == '10'
          for n in walk(conclude.children())))
    maturity = definition(trig, 'aor1776_debt_mature')
    check('debt.no_call_during_original_or_extended_binding',
          contains(maturity, 'has_variable', 'aor1776_debt_binding_lock')
          and contains(maturity, 'has_type', 'aor1776_deferred_debt_article')
          and any(n.key == 'remaining_binding_period' and n.op == '>' and n.value == '0'
                  for n in walk(maturity.children())))
    demand = definition('common/diplomatic_actions/1776_deferred_debt.txt', 'aor1776_demand_debt_repayment')
    check('debt.demand_calls_maturity_guard', contains(demand, 'aor1776_debt_mature', 'yes'))
    check('debt.one_time_five_percent_interest', contains(demand, 'var:aor1776_debt_interest', '5')
          and sub(demand, 'change_variable').one('multiply') == '1.05')
    refusal = definition(fx, 'aor1776_debt_refuse_effect')
    check('debt.refusal_infamy_and_relations', sub(refusal, 'change_infamy').value == '10'
          and sub(refusal, 'change_relations').one('value') == '-40')
    check('debt.refusal_closes_claim_and_records_it', contains(refusal, 'aor1776_debt_close_effect')
          and any(n.key == 'set_variable' and n.one('name') == 'aor1776_debt_repudiated'
                  for n in walk(refusal.children())))
    check('debt.repay_one_debit_one_credit', sum(n.key == 'add_treasury'
          for n in walk(definition(fx, 'aor1776_debt_repay_effect').children())) == 2)
    initialization = definition(fx, 'aor1776_support_initialize_effect')
    check('migration.no_new_mass_debt_for_old_save', not any(n.key == 'set_variable'
          and n.one('name') == 'aor1776_debt_principal' for n in walk(initialization.children())))

    startup = definition(on, 'aor1776_usa_support_startup')
    for id in ['aor1776_american_diplomacy.1', 'aor1776_american_diplomacy.7']:
        check('startup.after_three_days.' + id, any(n.key == 'trigger_event'
              and n.one('id') == id and n.one('days') == '3' for n in walk(startup.children())))
    check('startup.human_intro_opens_journal_on_click', contains(definition(ev, 'aor1776_american_diplomacy.1'), 'is_ai', 'no')
          and contains(sub(definition(ev, 'aor1776_american_diplomacy.1'), 'option'), 'aor1776_support_open_journal_effect'))
    ai_event = definition(ev, 'aor1776_american_diplomacy.7')
    ai_request = definition(fx, 'aor1776_support_ai_request_effect')
    check('startup.AI_US_opens_journal_and_requests', ai_event.one('hidden') == 'yes'
          and contains(ai_event, 'is_ai', 'yes') and contains(ai_event, 'aor1776_support_open_journal_effect')
          and contains(ai_event, 'aor1776_support_ai_request_effect') and contains(ai_request, 'aor1776_support_send_request_effect'))
    check('startup.AI_request_reaches_France', sub(definition(fx, 'aor1776_support_send_request_effect'), 'trigger_event').one('id')
          == 'aor1776_american_diplomacy.3')
    check('startup.no_player_country_dependency', not any(n.key.startswith(('is_player', 'is_local_player'))
          for n in walk(startup.children() + ai_event.children() + ai_request.children())))
    check('startup.French_player_has_three_responses', len(definition(ev, 'aor1776_american_diplomacy.3').children('option')) == 3)
    hist = 'common/history/countries/zz_1776_usa_revolution_r2.txt'
    check('minutemen.active_in_starting_history', any(n.key == 'activate_law'
          and n.value == 'law_type:law_aor1776_minutemen' for n in walk(tree(hist))))
    check('minutemen.override_loaded_after_original_country', Path(hist).name > 'usa - usa.txt')
    for path in ['common/journal_entries/1776_usa_french_support.txt', 'common/journal_entries/1776_usa_revolutionary_spirit.txt']:
        complete = sub(tree(path)[0], 'complete')
        check('UI.readable_journal_completion.' + Path(path).stem,
              complete.children()[0].key == 'custom_tooltip')

    joinfx = 'common/scripted_effects/1776_join_ongoing_wars.txt'
    call = definition('common/diplomatic_actions/1776_call_family_compact.txt', 'aor1776_call_family_compact')
    check('Spain.French_call_requires_consent', call.one('requires_approval') == 'yes')
    check('Spain.requires_existing_alliance_and_American_war',
          contains(sub(call, 'potential'), 'has_type', 'alliance')
          and contains(sub(call, 'potential'), 'is_war_participant', 'c:USA')
          and contains(sub(call, 'potential'), 'is_war_participant', 'c:GBR'))
    cc = sub(call, 'create_treaty')
    jc = sub(cc, 'articles_to_create').children()[0]
    check('Spain.call_ratifies_join_article_in_right_direction', jc.one('article') == 'join_war'
          and jc.one('source_country') == 'c:SPA' and jc.one('target_country') == 'c:FRA')
    check('Spain.call_guard_matches_ratification', normalized(sub(call, 'can_create_treaty').children())
          == normalized([n for n in cc.children() if n.key != 'name']))
    check('Spain.French_AI_proposes_call', sub(call, 'propose_score').one('value') == '2000'
          and contains(sub(call, 'will_propose'), 'has_war_with', 'c:GBR'))
    check('Spain.can_decline_under_financial_pressure', contains(sub(call, 'accept_score'), 'in_default', 'yes')
          and contains(sub(call, 'accept_score'), 'add', '-250'))
    check('Spain.no_annual_roll_or_deadline', definition(joinfx, 'aor1776_spanish_entry_roll_effect').children() == []
          and 'aor1776_intervention.2' not in read(on)
          and 'aor1776_spanish_entry_roll_effect' not in str(definition(joinfx, 'aor1776_revolution_intervention_monthly_effect').value))
    check('Spain.call_join_scoped_to_American_war', 'aor1776_join_american_war_only' in str(call.value)
          and 'aor1776_join_american_war_only' in read(joinfx))
    warjoin = sub(definition(joinfx, 'aor1776_intervene_effect'), 'join_war')
    check('join.native_target_and_side_API', warjoin.one('target') == 'scope:aor1776_intervening_country'
          and warjoin.one('side') == 'scope:aor1776_supported_country')
    check('join.allied_backer_supported', 'has_type = alliance' in read('common/scripted_triggers/1776_join_ongoing_wars.txt'))
    fr = definition(joinfx, 'aor1776_french_entry_roll_effect')
    check('France.no_1776_automatic_entry', any(n.key == 'game_date' and n.op == '>='
          and n.value == '1777.1.1' for n in walk(fr.children())))
    check('France.45_then_75_then_guaranteed', {n.value for n in walk(fr.children()) if n.key == 'chance'} == {'45', '75'}
          and contains(fr, 'game_date', '1778.3.17'))
    check('France.human_not_forced', contains(fr, 'is_ai', 'yes'))
    check('join.no_unknown_play_participant_trigger', not any(n.key == 'is_diplomatic_play_participant'
          for path in FILES for n in walk(tree(path))))
    check('relations.no_unqualified_getter', not any(n.key.startswith('relations:')
          for path in FILES for n in walk(tree(path))))
    for path in [p for p in FILES if p.startswith('common/decisions/')]:
        check('decision.native_AI_value.' + Path(path).stem, all(n.one('value') is not None and n.one('base') is None
              for n in walk(tree(path)) if n.key == 'ai_chance'))

    visible = [n for n in tree(ev) if n.key != 'namespace' and n.one('hidden') != 'yes']
    check('images.all_seven_visible_events_have_writer', len(visible) == 7
          and all(sub(n, 'event_image').one('video') == '"ep2_intellectual_writer"' for n in visible))
    check('images.Great_Wave_video_exists', (GAME / 'dlc/dlc018_ep2/gfx/event_pictures/ep2_intellectual_writer.bk2').exists())
    icon = ROOT / 'gfx/interface/icons/diplomatic_treaties_articles_icons/aor1776_deferred_debt.dds'
    from PIL import Image
    im = Image.open(icon).convert('RGBA')
    data = icon.read_bytes()
    check('icon.lossless_256_BGRA_with_mips', im.size == (256, 256) and len(data) == 349652
          and struct.unpack_from('<I', data, 28)[0] == 9)
    check('icon.actual_transparency', im.getchannel('A').getextrema() == (0, 255))
    check('icon.second_clause_uses_supplied_art', sub(definition(art, 'aor1776_deferred_debt_article'), 'icon').value.strip('"')
          == str(icon.relative_to(ROOT)).replace('\\', '/'))
    keys_by_lang = []
    for lang in ['french', 'english']:
        own_keys = set()
        catalog = entries(lang)
        for stem in ['1776_american_diplomacy_r3', '1776_usa_revolution_r2']:
            path = ROOT / f'localization/{lang}/{stem}_l_{lang}.yml'
            lines = path.read_text(encoding='utf-8-sig').splitlines()
            check('localization.BOM.' + lang + '.' + stem, path.read_bytes().startswith(b'\xef\xbb\xbf'))
            matches = [re.fullmatch(r'\s+([A-Za-z0-9_.-]+):0 ".*"', line) for line in lines[1:] if line.strip()]
            check('localization.valid_lines.' + lang + '.' + stem, lines[0] == 'l_' + lang + ':' and all(matches))
            own_keys.update(m.group(1) for m in matches if m)
        check('localization.unique_keys.' + lang, all(len(catalog[k]) == 1 for k in own_keys))
        required = set()
        for path in FILES:
            for n in walk(tree(path)):
                if isinstance(n.value, str) and n.key in {'title', 'flavor', 'text', 'desc', 'custom_tooltip', 'name'}:
                    if n.value.startswith(('aor1776_', 'je_aor1776_')) and (n.key != 'name' or re.match(r'aor1776_(american_diplomacy|debt)\.\d+\.[a-z]', n.value)):
                        required.add(n.value)
        check('localization.all_explicit_UI_keys.' + lang, required <= catalog.keys())
        check('localization.French_counteroffer.' + lang, 'aor1776_american_diplomacy.3.c' in catalog)
        keys_by_lang.append(own_keys)
    check('localization.same_FR_EN_keys', keys_by_lang[0] == keys_by_lang[1])

    baseline = json.loads((REPORT / 'BASELINE.json').read_text(encoding='utf-8'))
    for path in ['common/history/military_formations/00_military_formations_europe.txt',
                 'common/history/diplomatic_plays/00_american_revolution.txt',
                 'common/static_modifiers/76mod_modifiers.txt',
                 'common/ai_strategies/1776_revolution_intervention.txt',
                 'common/war_goal_types/1776_revolution_intervention.txt']:
        check('protected.R3_preserved.' + path, hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == baseline['files'][path])
    check('git.HEAD_preserved', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == baseline['head'])
    check('git.index_preserved', hashlib.sha256((ROOT / '.git/index').read_bytes()).hexdigest() == baseline['index_sha256'])
    check('credits.Join_Ongoing_Wars_author', 'The Lizerd King' in read('docs/credits/JOIN_ONGOING_WARS.md'))

    import validate_american_revolution_r2 as prior
    prior.CHECKS.clear()
    prior.naval_checks()
    prior.content_r1_checks()
    prior.content_r2_checks()
    prior.reference_checks(FILES)
    # This old literal assertion requires the very relation syntax rejected by
    # the user's engine. Replace only that assertion with its corrected form.
    superseded = 'echoes.colonies_filtered_by_subject_and_political_contact'
    prior.CHECKS.pop(superseded)
    echo = read('common/scripted_effects/1776_usa_echoes.txt')
    check('echoes.corrected_subject_and_political_contact_filter', all(s in echo for s in [
        'is_subject = yes', 'has_law_or_variant = law_type:law_right_of_assembly', 'c:USA.relations:this >= 20']))
    CHECKS.update({'prior.' + k: v for k, v in prior.CHECKS.items()})
    scenarios = []
    for days in [3650, 3652, 3653]:
        principal_amount = Decimal(30000) * days / 7
        due = principal_amount * Decimal('1.05')
        check('arithmetic.positive_face_amount.' + str(days), principal_amount > 15000000 and due > principal_amount)
        before = Decimal(50000000)
        borrower, creditor = before - due, before + due
        check('arithmetic.settlement_cash_conserved.' + str(days), borrower + creditor == before * 2)
        scenarios.append({'binding_days': days, 'weekly_transfer': 30000,
                          'contract_face_principal': str(principal_amount), 'with_5_percent': str(due)})
    result = {'status': 'PASS_STATIC' if all(CHECKS.values()) else 'FAIL_STATIC',
              'passed': sum(CHECKS.values()), 'total': len(CHECKS),
              'failed': [k for k, v in CHECKS.items() if not v], 'checks': CHECKS,
              'superseded_prior_literal_assertion': superseded,
              'arithmetic': scenarios, 'files': FILES,
              'runtime': 'NOT_RUN', 'AI_landings': 'NOT_VERIFIED',
              'accounting': 'Contract face value of scheduled transfers, not a meter of frozen or cancelled payments.'}
    (REPORT / 'VALIDATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['status', 'passed', 'total', 'failed', 'runtime']}, ensure_ascii=False, indent=2))
    return 0 if all(CHECKS.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
