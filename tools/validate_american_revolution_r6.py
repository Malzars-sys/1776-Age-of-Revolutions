"""French-first opening regressions plus the unchanged R5 checks.

Option projections below read the real script's flags and scheduled recipients;
they do not run native events, AI or treaty creation in Victoria 3.
"""
from pathlib import Path
import hashlib
import json

import validate_american_revolution_r5 as prior
from validate_diplomacy_ottoman_1776 import parse, walk, normalized

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/reports/military/AMERICAN_REVOLUTION_R6'
AUTH = 'aor1776_french_support_invitation_authorized'
PERMIT = 'aor1776_french_support_invitation'
EVENTS = 'events/1776_american_diplomacy.txt'
FX = 'common/scripted_effects/1776_usa_french_support.txt'
TRIGGERS = 'common/scripted_triggers/1776_usa_french_support.txt'
prior.FILES.append('common/laws/00_army_model.txt')


def opening_checks():
    check, definition, sub, contains = prior.check, prior.definition, prior.sub, prior.contains
    startup = definition('common/on_actions/1776_usa_revolution_r2.txt', 'aor1776_usa_support_startup')
    scheduled = [n for n in walk(startup.children()) if n.key == 'trigger_event']
    check('R6.startup_only_schedules_French_opener_and_existing_war_deadline',
          {n.one('id') for n in scheduled} == {'aor1776_american_diplomacy.8', 'aor1776_intervention.1'})
    french_country = next(n for n in walk(startup.children()) if n.key == 'c:FRA'
                          and any(e.one('id') == 'aor1776_american_diplomacy.8' for e in n.children('trigger_event')))
    check('R6.first_event_France_after_three_days', french_country.children('trigger_event')[0].one('days') == '3')
    check('R6.French_opener_scheduled_once', all(contains(startup, 'has_variable', v) for v in
          ['aor1776_french_approach_scheduled', 'aor1776_french_approach_resolved']))
    french_gate = next(n for n in walk(startup.children()) if n.key == 'if'
                      and contains(n, 'trigger_event') and contains(n, 'aor1776_support_stop_effect'))
    check('R6.signed_contracts_not_reset', all(contains(sub(french_gate, 'limit'), 'has_variable', v)
          for v in ['aor1776_support_active', 'aor1776_debt_creditor']))
    opener = definition(EVENTS, 'aor1776_american_diplomacy.8')
    check('R6.French_opener_is_visible_and_national', opener.one('hidden') != 'yes'
          and contains(opener.children('trigger')[0], 'c:FRA', 'this'))
    check('R6.French_opener_two_choices', len(opener.children('option')) == 2)
    check('R6.no_forced_human_or_AI_French_choice', not any(n.key in {'is_ai', 'is_player', 'is_local_player'}
          for n in walk(opener.children('trigger'))))
    check('R6.no_money_treaty_or_immediate_war_in_initial_choice', not any(n.key in
          {'add_treasury', 'create_treaty', 'create_diplomatic_pact', 'join_war', 'start_war'}
          for n in walk(opener.children('option'))))

    # Project only deterministic effects present in these two choices.
    def project(nodes, country, flags, queue):
        for n in nodes:
            if n.key == 'hidden_effect': project(n.children(), country, flags, queue)
            elif n.key.startswith('c:') and isinstance(n.value, list): project(n.children(), n.key, flags, queue)
            elif n.key == 'set_variable': flags.setdefault(country, set()).add(n.value if isinstance(n.value, str) else n.one('name'))
            elif n.key == 'trigger_event': queue.append({'country': country, 'id': n.one('id'), 'days': n.one('days')})
            elif n.key not in {'name', 'default_option', 'ai_chance', 'custom_tooltip'}:
                raise ValueError('Unsupported initial-choice effect: ' + n.key)

    scenarios = []
    for option, consent in zip(opener.children('option'), [True, False]):
        flags, queue = {}, []
        project(option.children(), 'c:FRA', flags, queue)
        check('R6.French_permission.' + str(consent), (PERMIT in flags.get('c:FRA', set())) == consent)
        check('R6.French_choice_resolved.' + str(consent), 'aor1776_french_approach_resolved' in flags.get('c:FRA', set()))
        if consent:
            check('R6.French_yes_invites_only_America_next_day', queue == [
                {'country': 'c:USA', 'id': 'aor1776_american_diplomacy.1', 'days': '1'},
                {'country': 'c:USA', 'id': 'aor1776_american_diplomacy.7', 'days': '1'}])
        else:
            check('R6.French_no_sends_no_American_event', queue == []
                  and 'aor1776_french_approach_declined' in flags.get('c:FRA', set()))
        scenarios.append({'French_consent': consent, 'flags': {k: sorted(v) for k, v in flags.items()}, 'scheduled': queue})

    for number in [1, 2, 3, 4, 7]:
        event = definition(EVENTS, f'aor1776_american_diplomacy.{number}')
        check('R6.previously_queued_event_requires_French_consent.' + str(number),
              contains(event.children('trigger')[0], AUTH, 'yes'))
    for key in ['aor1776_french_support_can_request', 'aor1776_french_support_can_offer', 'aor1776_french_support_can_accept']:
        check('R6.central_consent_guard.' + key, contains(definition(TRIGGERS, key), AUTH, 'yes'))
    journal = definition(FX, 'aor1776_support_open_journal_effect')
    check('R6.journal_itself_requires_consent', sub(journal, 'limit').one(AUTH) == 'yes')
    recovery = definition('common/decisions/1776_usa_french_support.txt', 'aor1776_open_french_support_correspondence')
    check('R6.recovery_cannot_bypass_French_no', contains(recovery.children('is_shown')[0], AUTH, 'yes'))
    human = definition(EVENTS, 'aor1776_american_diplomacy.1')
    ai = definition(EVENTS, 'aor1776_american_diplomacy.7')
    check('R6.American_invitation_delivered_once_for_human_or_AI', all(
        contains(n.children('trigger')[0], 'has_variable', 'aor1776_american_invitation_seen')
        and contains(n, 'set_variable', 'aor1776_american_invitation_seen') for n in [human, ai]))
    check('R6.human_can_request_only_after_opening_journal',
          contains(human.children('option')[0], 'aor1776_support_open_journal_effect')
          and not contains(human, 'aor1776_support_request_effect'))
    check('R6.American_AI_still_requests_from_French_player', ai.one('hidden') == 'yes'
          and contains(ai, 'is_ai', 'yes') and contains(ai, 'aor1776_support_ai_request_effect'))
    visible = [n for n in prior.tree(EVENTS) if n.key != 'namespace' and n.one('hidden') != 'yes']
    check('R6.all_eight_visible_events_have_existing_writer_image', len(visible) == 8
          and all(sub(n, 'event_image').one('video') == '"ep2_intellectual_writer"' for n in visible))

    base = json.loads((REPORT / 'BASELINE.json').read_text())
    old_effects = parse((REPORT / 'baseline' / FX).read_text(encoding='utf-8-sig'))
    for name in ['aor1776_support_conclude_effect', 'aor1776_support_commit_contract_effect',
                 'aor1776_support_accept_effect', 'aor1776_support_stop_effect',
                 'aor1776_debt_repay_effect', 'aor1776_debt_refuse_effect']:
        old = next(n for n in old_effects if n.key == name)
        check('R6.financial_terms_preserved.' + name, normalized(old.children()) == normalized(definition(FX, name).children()))
    for path, sha in base['protected'].items():
        check('R6.protected.' + path, hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha)
    laws = prior.tree('common/laws/00_army_model.txt')
    militia = next(n for n in laws if n.key == 'law_national_militia')
    companies = next(n for n in laws if n.key == 'law_aor1776_minutemen')
    check('R6.HUD.parent_hidden_only_for_USA', normalized(militia.children('is_visible')[0].children())
          == [('NOT', '=', [('c:USA', '?=', 'this')])])
    check('R6.HUD.companies_visible_only_for_USA', normalized(companies.children('is_visible')[0].children())
          == [('c:USA', '?=', 'this')])
    order = [n.key for n in laws]
    check('R6.HUD.companies_in_militia_position_before_mass_conscription',
          order.index('law_aor1776_minutemen') == order.index('law_national_militia') + 1
          and order.index('law_mass_conscription') == order.index('law_aor1776_minutemen') + 1)
    old_variant = parse((REPORT / 'baseline/common/laws/1776_usa_minutemen.txt').read_text(encoding='utf-8-sig'))[0]
    check('R6.HUD.variant_rules_and_effects_preserved', normalized(companies.children()) == normalized(old_variant.children()))
    old_laws = parse((REPORT / 'baseline/common/laws/00_army_model.txt').read_text(encoding='utf-8-sig'))
    check('R6.HUD.other_army_laws_preserved', normalized([n for n in laws if n.key not in
          {'law_national_militia', 'law_aor1776_minutemen'}]) == normalized([n for n in old_laws if n.key != 'law_national_militia']))
    old_militia = next(n for n in old_laws if n.key == 'law_national_militia')
    check('R6.HUD.militia_stats_and_enactment_preserved', normalized([n for n in militia.children()
          if n.key != 'is_visible']) == normalized(old_militia.children()))
    all_variants = [n for p in (ROOT / 'common/laws').glob('*.txt')
                    for n in parse(p.read_text(encoding='utf-8-sig')) if n.key == 'law_aor1776_minutemen']
    check('R6.HUD.exactly_one_variant_definition', len(all_variants) == 1)
    return scenarios


if __name__ == '__main__':
    raise SystemExit(prior.main(report=REPORT, extend_checks=opening_checks, superseded_checks=(
        'startup.after_three_days.aor1776_american_diplomacy.1',
        'startup.after_three_days.aor1776_american_diplomacy.7',
        'images.all_seven_visible_events_have_writer',
    )))
