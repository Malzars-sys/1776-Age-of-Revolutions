"""Static Minutemen reform checks, with R6 finance/war/HUD regressions.

The small projector below reads the actual trigger/effect AST. Native facts
(war, political support, legitimacy) are supplied as scenario inputs; it does
not simulate Victoria 3, enactment checkpoints, save loading or AI behaviour.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import subprocess

import validate_american_revolution_r6 as r6
from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from localization_duplicate_audit import entries

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/reports/military/CONTENT-USA-MINUTEMEN-REFORM'
TRIG = 'common/scripted_triggers/1776_usa_minutemen_reform.txt'
FX = 'common/scripted_effects/1776_usa_minutemen_reform.txt'
LAWFILE = 'common/laws/1776_usa_reorganized_militia.txt'
EVENT = 'events/1776_usa_minutemen_reform.txt'
DECISION = 'common/decisions/1776_usa_minutemen_reform.txt'
FINISHFILE = 'common/scripted_effects/1776_usa_content_r1.txt'
JOURNAL = 'common/journal_entries/06_usa_independence_mod.txt'
NEW_SCRIPTS = [TRIG, FX, LAWFILE, EVENT, DECISION]
LOCFILES = [f'localization/{lang}/1776_usa_minutemen_reform_l_{lang}.yml'
            for lang in ['french', 'english']]
MINUTEMEN = 'law_type:law_aor1776_minutemen'
TARGET = 'law_type:law_aor1776_reorganized_militia'
PEASANT = 'law_type:law_peasant_levies'
TECH = 'permanent_engineer_services'
RESOLVED = 'aor1776_minutemen_reform_resolved'
PENDING = 'aor1776_minutemen_reform_event_pending'
CHOICE = 'aor1776_minutemen_reform_choice'
PREFIX = 'aor1776_minutemen_reform_'
EVENT_ID = 'aor1776_usa_minutemen_reorganization.1'
prior = r6.prior


def reform_checks():
    check, definition, sub, contains = prior.check, prior.definition, prior.sub, prior.contains
    triggers = {n.key: n for n in prior.tree(TRIG)}
    effects = {n.key: n for n in prior.tree(FX)}
    target = definition(LAWFILE, TARGET.split(':')[1])
    event = definition(EVENT, EVENT_ID)
    decision = definition(DECISION, 'aor1776_review_revolutionary_militias')
    finish = definition(FINISHFILE, 'aor1776_content_finish_effect')
    base = json.loads((REPORT / 'BASELINE.json').read_text(encoding='utf-8'))
    audit = json.loads((REPORT / 'AUDIT.json').read_text(encoding='utf-8'))
    cases = []

    def condition(node, state):
        key, value = node.key, node.value
        if key in {'AND', 'limit', 'trigger', 'is_shown', 'possible', 'can_enact', 'is_visible'}:
            return conditions(node.children(), state)
        if key == 'OR': return any(condition(n, state) for n in node.children())
        if key in {'NOT', 'NOR'}: return not any(condition(n, state) for n in node.children())
        if key == 'custom_tooltip':
            return conditions([n for n in node.children() if n.key != 'text'], state)
        if key in triggers: return conditions(triggers[key].children(), state) == (value == 'yes')
        if key == 'c:USA': return state['country'] == 'USA'
        if key == 'power_bloc':
            return not state['has_bloc'] or conditions(node.children(), state)
        if key == 'has_identity': return state['military_bloc']
        if key == 'has_variable': return value in state['variables']
        if key == 'has_modifier': return value in state['modifiers']
        if key == 'has_technology_researched': return value in state['techs']
        if key == 'has_law': return state['law'] == value
        if key == 'has_law_or_variant': return value in state['other_laws'] or state['law'] == value
        if key == 'is_enacting_law': return state['enacting'] == value
        if key == 'enacting_any_law': return bool(state['enacting']) == (value == 'yes')
        if key in {'is_subject', 'is_power_bloc_leader', 'aor1776_usa_independence_war_active'}:
            field = {'is_subject': 'subject', 'is_power_bloc_leader': 'bloc_leader',
                     'aor1776_usa_independence_war_active': 'revolution'}[key]
            return state[field] == (value == 'yes')
        if key == 'government_legitimacy':
            assert node.op == '>='
            return state['legitimacy'] >= float(value)
        if key == f'enactment_chance_for_law({TARGET})':
            assert node.op == '>'
            return state['chance'] > float(value)
        if key == 'always': return value == 'yes'
        raise ValueError('Unmodelled trigger: ' + key)

    def conditions(nodes, state):
        return all(condition(n, state) for n in nodes)

    def apply(nodes, state):
        for node in nodes:
            key = node.key
            if key == 'if':
                if conditions(node.children('limit')[0].children(), state):
                    apply([n for n in node.children() if n.key != 'limit'], state)
            elif key in effects:
                apply(effects[key].children(), state)
            elif key == 'set_variable':
                name = node.value if isinstance(node.value, str) else node.one('name')
                state['variables'][name] = True if isinstance(node.value, str) else node.one('value', True)
                if node.one('days') is not None: state['expiry_days'][name] = int(node.one('days'))
            elif key == 'remove_variable':
                state['variables'].pop(node.value, None)
                state['expiry_days'].pop(node.value, None)
            elif key == 'trigger_event': state['events'].append(node.one('id'))
            elif key == 'start_enactment':
                state['enacting'] = node.value
                state['started'].append(node.value)
            elif key == 'cancel_enactment':
                state['cancelled'].append(state['enacting'])
                state['enacting'] = None
            elif key == 'activate_law':
                state['law'] = node.value
                state['activated'].append(node.value)
            elif key == 'remove_modifier':
                state['modifiers'].discard(node.value)
                state['removed_modifiers'].append(node.value)
            elif key in {'name', 'trigger', 'show_as_unavailable', 'default_option', 'ai_chance', 'custom_tooltip'}:
                continue
            else: raise ValueError('Unmodelled effect: ' + key)

    def state(**updates):
        result = dict(country='USA', law=MINUTEMEN, subject=True, revolution=True,
                      bloc_leader=False, has_bloc=False, military_bloc=False,
                      legitimacy=75, chance=25, enacting=None, techs=set(), other_laws=set(),
                      variables={}, expiry_days={}, modifiers=set(), events=[], started=[], cancelled=[],
                      activated=[], removed_modifiers=[])
        result.update(updates)
        return result

    def allowed(name, scenario):
        return conditions(triggers[PREFIX + name].children(), scenario)

    def project_case(name, scenario, effect):
        before = deepcopy(scenario)
        apply(effect.children(), scenario)
        # Compact serializable evidence: no claim that the engine ran this case.
        cases.append({'case': name, 'method': 'STATIC_AST_PROJECTION',
                      'before_law': before['law'], 'after_law': scenario['law'],
                      'before_enactment': before['enacting'], 'after_enactment': scenario['enacting'],
                      'events': scenario['events'], 'variables': scenario['variables'].copy(),
                      'started': scenario['started'], 'cancelled': scenario['cancelled'],
                      'activated': scenario['activated']})

    # A: live law and existing war context, not an arbitrary calendar deadline.
    start = state()
    check('Minutemen.A.initial_law_and_technology_unchanged',
          audit['destination_tech_available_at_start'] is False
          and contains(definition('common/history/countries/zz_1776_usa_revolution_r2.txt', 'COUNTRIES'),
                       'activate_law', MINUTEMEN))
    check('Minutemen.A.start_offer_available_reform_locked', allowed('can_offer', start) and not allowed('can_begin', start))
    project_case('A.wartime_decision', start, effects['aor1776_minutemen_reorganization_offer_effect'])
    check('Minutemen.A.single_pending_event', start['events'] == [EVENT_ID] and not allowed('can_offer', start))
    apply(effects['aor1776_minutemen_reorganization_offer_effect'].children(), start)
    check('Minutemen.A.repeated_invocation_not_duplicated', start['events'] == [EVENT_ID])
    check('Minutemen.A.pending_outlasts_event', start['expiry_days'][PENDING] > int(event.one('duration')))
    check('Minutemen.A.unavailable_choice_visible', event.children('option')[0].children('show_as_unavailable')[0].one('always') == 'yes')
    check('Minutemen.A.no_new_calendar_or_pulse', not any(n.key in
          {'on_daily_pulse', 'on_monthly_pulse', 'on_yearly_pulse', 'date', 'current_date'}
          for path in NEW_SCRIPTS for n in walk(prior.tree(path))))

    # B: a native enactment starts; current law is not replaced by the event.
    eligible = state(techs={TECH})
    check('Minutemen.B.valid_start_allowed', allowed('can_begin', eligible))
    project_case('B.start_native_enactment', eligible, event.children('option')[0])
    check('Minutemen.B.only_native_enactment_started', eligible['started'] == [TARGET]
          and eligible['law'] == MINUTEMEN and eligible['activated'] == [] and eligible['cancelled'] == [])
    check('Minutemen.B.choice_recorded_once', eligible['variables'].get(CHOICE) == '1'
          and not allowed('can_offer', eligible) and not allowed('can_begin', eligible))
    for name, updates in [
        ('technology_missing', {}), ('other_law_enacting', {'techs': {TECH}, 'enacting': 'law_type:law_wealth_voting'}),
        ('legitimacy_below_threshold', {'techs': {TECH}, 'legitimacy': 24}),
        ('no_political_support', {'techs': {TECH}, 'chance': 0}),
        ('wrong_country', {'techs': {TECH}, 'country': 'FRA'}),
        ('subject_after_defeat', {'techs': {TECH}, 'revolution': False}),
        ('Edo_conflict', {'techs': {TECH}, 'other_laws': {'law_type:law_strict_edo_system'}}),
        ('military_bloc_leader', {'techs': {TECH}, 'bloc_leader': True, 'has_bloc': True, 'military_bloc': True}),
        ('wrong_active_law', {'techs': {TECH}, 'law': PEASANT}),
    ]:
        blocked = state(**updates)
        original = deepcopy(blocked)
        check('Minutemen.B.guard.' + name, not allowed('can_begin', blocked))
        project_case('B.blocked.' + name, blocked, effects['aor1776_minutemen_reorganization_begin_effect'])
        check('Minutemen.B.no_mutation_when_blocked.' + name, blocked == original)
    check('Minutemen.B.native_engineer_gate', [n.value for n in target.children('unlocking_technologies')[0].children()] == [TECH])
    check('Minutemen.B.same_army_model_parent', target.one('group') == 'lawgroup_army_model'
          and target.one('parent') == 'law_national_militia')
    check('Minutemen.B.not_internal_security_National_Guard', 'law_national_guard' not in prior.read(LAWFILE))

    # C: declining changes flags only and cannot veto subsequent ordinary laws.
    keep = state(techs={TECH}, subject=False, revolution=False)
    project_case('C.retain_Minute_Men', keep, event.children('option')[1])
    check('Minutemen.C.unchanged_law_no_extra_bonus', keep['law'] == MINUTEMEN and not keep['activated']
          and not keep['started'] and not keep['cancelled'] and not keep['removed_modifiers'])
    check('Minutemen.C.event_not_repeated', keep['variables'].get(CHOICE) == '2' and not allowed('can_offer', keep))
    check('Minutemen.C.ordinary_target_enactment_stays_open', conditions(target.children('can_enact')[0].children(), keep)
          and conditions(target.children('is_visible')[0].children(), keep))
    check('Minutemen.C.no_resolution_lock_on_law', not contains(target, 'has_variable', RESOLVED))

    # D: compare the actual journal AST to the pre-edit snapshot, then exercise
    # only the modified finish effect with supplied native war-result facts.
    old_journal = parse((REPORT / 'baseline' / JOURNAL).read_text(encoding='utf-8-sig'))
    new_journal = prior.tree(JOURNAL)
    stripped = deepcopy(new_journal)
    for node in walk(stripped):
        if isinstance(node.value, list):
            node.value[:] = [n for n in node.value if n.key != 'aor1776_minutemen_reorganization_offer_effect']
    check('Minutemen.D.journal_only_adds_victory_offer', normalized(stripped) == normalized(old_journal))
    victory_calls = [n for n in walk(new_journal) if n.key == 'aor1776_minutemen_reorganization_offer_effect']
    check('Minutemen.D.exactly_one_victory_hook', len(victory_calls) == 1
          and any(contains(n, 'aor1776_minutemen_reorganization_offer_effect') for n in walk(new_journal) if n.key == 'on_complete')
          and not any(contains(n, 'aor1776_minutemen_reorganization_offer_effect') for n in walk(new_journal) if n.key == 'on_fail'))
    old_finish_tree = parse((REPORT / 'baseline' / FINISHFILE).read_text(encoding='utf-8-sig'))
    current_finish_tree = prior.tree(FINISHFILE)
    stripped_finish_tree = deepcopy(current_finish_tree)
    removed = []
    for node in walk(stripped_finish_tree):
        if isinstance(node.value, list):
            for child in list(node.value):
                if child.key == 'if' and contains(child, 'cancel_enactment'):
                    removed.append(child)
                    node.value.remove(child)
    check('Minutemen.D.original_defeat_fallback_and_other_content_unchanged',
          len(removed) == 1 and normalized(stripped_finish_tree) == normalized(old_finish_tree))
    check('Minutemen.D.cancellation_limited_to_new_reform_and_subject',
          normalized(removed[0].children('limit')[0].children()) == [
              ('is_subject', '=', 'yes'), ('is_enacting_law', '=', TARGET)])
    won = state(subject=False, revolution=False)
    project_case('D.victory_keeps_Minute_Men_before_choice', won, finish)
    apply(effects['aor1776_minutemen_reorganization_offer_effect'].children(), won)
    check('Minutemen.D.victory_offers_choice_without_replacing_law', won['law'] == MINUTEMEN and won['events'] == [EVENT_ID])
    peace = state(subject=False, revolution=False, techs={TECH}, enacting=TARGET)
    project_case('D.independent_peace_preserves_enactment', peace, finish)
    check('Minutemen.D.valid_enactment_continues_at_peace', peace['enacting'] == TARGET and not peace['cancelled'])
    for enacting in [None, TARGET, 'law_type:law_wealth_voting']:
        lost = state(revolution=False, enacting=enacting)
        project_case('D.defeat.' + str(enacting), lost, finish)
        check('Minutemen.D.defeat_retains_peasant_fallback.' + str(enacting), lost['law'] == PEASANT)
        check('Minutemen.D.only_own_enactment_cancelled.' + str(enacting),
              lost['enacting'] == (None if enacting == TARGET else enacting))

    # E: structural persisted flags and JSON state round-trips are NOT a
    # Victoria 3 save/reload test. The runtime checklist covers native saves.
    for name, scenario in [('pending', start), ('reform_chosen', eligible), ('retained', keep)]:
        saved = json.loads(json.dumps({'variables': scenario['variables'], 'expiry_days': scenario['expiry_days'],
                                      'enacting': scenario['enacting']}))
        restored = deepcopy(scenario)
        restored.update(saved)
        check('Minutemen.E.persisted_guards.' + name, not allowed('can_offer', restored))
    check('Minutemen.E.resolution_has_no_expiry', all(n.one('days') is None for n in walk(prior.tree(FX))
          if n.key == 'set_variable' and (n.value == RESOLVED or n.one('name') == RESOLVED)))

    # F: bounded changes, actual catalog entries, translations and preservation.
    min_node = definition('common/laws/00_army_model.txt', 'law_aor1776_minutemen')
    min_stats = {n.key: float(n.value) for n in min_node.children('modifier')[0].children()}
    new_stats = {n.key: float(n.value) for n in target.children('modifier')[0].children()}
    expected = dict(state_conscription_rate_add=.05, state_building_barrack_max_level_add=25,
                    state_building_conscription_center_max_level_add=50,
                    military_formation_mobilization_speed_mult=.05, building_training_rate_mult=.15,
                    country_military_goods_cost_mult=.10, unit_morale_loss_mult=-.05)
    check('Minutemen.F.bounded_recruitment_training_cost_tradeoff', new_stats == expected
          and new_stats['state_building_barrack_max_level_add'] == min_stats['state_building_barrack_max_level_add'])
    check('Minutemen.F.no_new_attack_defense_home_security_bonuses', not any(
          any(part in key for part in ['offense', 'defense', 'home_affairs', 'suppression', 'institution']) for key in new_stats))
    forbidden = {'activate_law', 'add_technology_researched', 'add_technology_progress', 'add_modifier',
                 'create_character', 'create_building', 'create_military_formation', 'create_combat_unit',
                 'destroy_building', 'add_treasury', 'create_treaty', 'cancel_enactment'}
    check('Minutemen.F.no_instant_adoption_units_tech_money_or_modifiers', not any(
          n.key in forbidden for path in NEW_SCRIPTS for n in walk(prior.tree(path))))
    for key in new_stats:
        check('Minutemen.F.native_modifier.' + key, any(key in p.read_text(encoding='utf-8-sig')
              for p in (prior.GAME / 'common/modifier_type_definitions').glob('*.txt')))
    check('Minutemen.F.existing_video_and_icon',
          (prior.GAME / 'dlc/dlc018_ep2/gfx/event_pictures/ep2_intellectual_writer.bk2').exists()
          and (prior.GAME / target.one('icon').strip('"')).exists()
          and (prior.GAME / event.one('icon').strip('"')).exists())
    keysets = []
    for lang, path in zip(['french', 'english'], LOCFILES):
        text = prior.read(path)
        lines = text.splitlines()
        matches = [re.fullmatch(r'\s+([A-Za-z0-9_.-]+):0 "([^"\n]|\\")*"', line)
                   for line in lines[1:] if line.strip()]
        keys = {m.group(1) for m in matches if m}
        catalog = entries(lang)
        check('Minutemen.F.localization.syntax_BOM.' + lang,
              (ROOT / path).read_bytes().startswith(b'\xef\xbb\xbf') and lines[0] == f'l_{lang}:' and all(matches))
        check('Minutemen.F.localization.no_duplicate_keys.' + lang, all(len(catalog[k]) == 1 for k in keys))
        required = {TARGET.split(':')[1], TARGET.split(':')[1] + '_desc', decision.key, decision.key + '_desc'}
        for script in NEW_SCRIPTS:
            required.update(n.value for n in walk(prior.tree(script)) if isinstance(n.value, str)
                            and n.key in {'title', 'desc', 'flavor', 'text', 'custom_tooltip', 'name'}
                            and (n.value.startswith(EVENT_ID + '.') or n.value.endswith('_tt')))
        check('Minutemen.F.localization.complete_UI.' + lang, required <= keys)
        check('Minutemen.F.localization.no_development_prose.' + lang, not any(
              word in text.lower() for word in ['tiré d’un roman', 'roman imaginaire', 'runtime', 'scripted_effects', 'law_type:']))
        keysets.append(keys)
    check('Minutemen.F.localization.same_FR_EN_keys', keysets[0] == keysets[1])
    changed_protected = [path for path, sha in base['protected'].items()
                         if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha]
    check('Minutemen.F.all_protected_files_unchanged', changed_protected == [])
    check('Minutemen.F.git_HEAD_preserved', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
          text=True).strip() == base['head'])
    check('Minutemen.F.git_index_preserved', hashlib.sha256((ROOT / '.git/index').read_bytes()).hexdigest() == base['index_sha256'])
    (REPORT / 'SCENARIOS.json').write_text(json.dumps({
        'method': 'STATIC_AST_PROJECTION_NOT_GAME_EXECUTION', 'cases': cases,
        'protected_file_count': len(base['protected']), 'changed_protected_files': changed_protected,
        'minutemen_modifiers': min_stats, 'reorganized_modifiers': new_stats,
        'runtime': 'NOT_RUN', 'native_save_reload': 'NOT_RUN', 'native_enactment_rules': 'REQUIRES_RUNTIME_VALIDATION',
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return [{'case': c['case'], 'method': c['method']} for c in cases]


def combined_checks():
    return r6.opening_checks() + reform_checks()


if __name__ == '__main__':
    raise SystemExit(prior.main(report=REPORT, extend_checks=combined_checks, superseded_checks=(
        'startup.after_three_days.aor1776_american_diplomacy.1',
        'startup.after_three_days.aor1776_american_diplomacy.7',
        'images.all_seven_visible_events_have_writer',
    )))
