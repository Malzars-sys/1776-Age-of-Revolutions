"""Focused R5 regression cases against the actual script trees.

The tiny predicate evaluator below handles only the boolean interest rule and
offer selectors. It does not simulate treaty creation or the Victoria 3 engine.
"""
import hashlib
import json
from decimal import Decimal
from validate_diplomacy_ottoman_1776 import parse, walk, normalized


def run_cases(root, check, read, tree, definition, sub, contains):
    fx = 'common/scripted_effects/1776_usa_french_support.txt'
    art = 'common/treaty_articles/1776_usa_french_support.txt'
    ev = 'events/1776_american_diplomacy.txt'
    jt = 'common/scripted_triggers/1776_join_ongoing_wars.txt'
    baseline = root / 'docs/reports/military/AMERICAN_REVOLUTION_R5/baseline'
    previous = parse((baseline / art).read_text(encoding='utf-8-sig'))

    # This is the exact illegal link reported by the player's engine. The
    # article options used during ratification are not a runtime article.
    def invalid_options_links(nodes, options=False):
        errors = []
        for n in nodes:
            typed_options = options or n.key in {'scope:article', 'scope:article_options'}
            if options and n.key == 'treaty':
                errors.append(n.key)
            errors += invalid_options_links(n.children(), typed_options)
        return errors

    old_requirements = [r for n in previous for r in n.children('requirement_to_maintain')]
    new_requirements = [r for n in tree(art) + tree('common/treaty_articles/31_join_war.txt')
                        for r in n.children('requirement_to_maintain')]
    check('R5.reproduces_three_old_options_scope_violations',
          len(invalid_options_links(old_requirements)) == 3)
    check('R5.no_options_to_runtime_treaty_link', not invalid_options_links(new_requirements))
    for key in ['aor1776_support_money', 'aor1776_revolution_military_assistance', 'aor1776_support_supplies']:
        requirement = sub(definition(art, key), 'requirement_to_maintain')
        check('R5.proposal_valid_before_activation.' + key,
              contains(requirement, 'has_variable', 'aor1776_support_offer')
              and contains(requirement, 'has_variable', 'aor1776_support_active'))
    money_possible = sub(definition(art, 'aor1776_support_money'), 'possible')
    check('R5.recipient_default_does_not_block_aid', money_possible.children()[0].key == 'c:FRA'
          and len(money_possible.children()) == 1)
    conclude = definition(fx, 'aor1776_support_conclude_effect')
    commit = definition(fx, 'aor1776_support_commit_contract_effect')
    committed = next(n for n in walk(conclude.children()) if n.key == 'if'
                     and n.children('aor1776_support_commit_contract_effect'))
    check('R5.no_debt_before_native_treaty_exists', sub(committed, 'limit').one('aor1776_support_treaty_exists') == 'yes'
          and not contains(conclude, 'aor1776_debt_open_effect'))
    actual = definition('common/scripted_triggers/1776_usa_french_support.txt', 'aor1776_support_treaty_exists')
    check('R5.postcondition_requires_finance_IOU_instructors_and_two_supplies',
          {n.value for n in walk(actual.children()) if n.key == 'has_type'} == {
              'aor1776_support_money', 'aor1776_deferred_debt_article',
              'aor1776_revolution_military_assistance', 'aor1776_support_supplies'}
          and any(n.key == 'count' and n.op == '>=' and n.value == '2' for n in walk(actual.children())))
    failure = definition(fx, 'aor1776_support_failed_ratification_effect')
    check('R5.failure_cannot_issue_claim_or_obligation', not contains(failure, 'aor1776_debt_open_effect')
          and not contains(failure, 'set_owes_obligation_to') and contains(failure, 'aor1776_support_stop_effect'))
    accept = definition(fx, 'aor1776_support_accept_effect')
    check('R5.no_temporary_activation_to_fool_native_guard', not any(n.key == 'set_variable'
          and n.one('name') == 'aor1776_support_active' for n in walk(accept.children())))
    check('R5.interest_commit_uses_approved_snapshot', any(n.key == 'if'
          and contains(sub(n, 'limit'), 'var:aor1776_support_offered_interest', '5')
          and any(x.key == 'set_variable' and x.one('name') == 'aor1776_debt_interest'
                  and x.one('value') == '5' for x in n.children()) for n in commit.children('if')))

    # Evaluate the real boolean clauses, with explicit synthetic country/war
    # inputs. Unknown predicate types fail rather than silently passing a case.
    def evaluate(nodes, current, world):
        def one(n):
            k, v = n.key, n.value
            children = n.children()
            if k == 'OR': return any(one(x) for x in children)
            if k in {'AND', 'trigger', 'limit'}: return all(one(x) for x in children)
            if k == 'NOT': return not all(one(x) for x in children)
            if k == 'custom_tooltip': return all(one(x) for x in children if x.key != 'text')
            if k == 'always': return v == 'yes'
            if k in {'$ACTOR$', '$FRIEND$'}:
                return evaluate(children, world[k], world)
            if k.startswith('c:'):
                return current == k if v == 'this' else evaluate(children, k, world)
            data = world.get(current, {})
            if k.startswith('var:'): return str(data.get(k[4:], -1)) == v
            if k == 'has_variable': return v in data
            if k == 'is_war_participant': return v in world['participants']
            if k == 'has_interest_marker_in_region': return v in data.get('interests', [])
            if k == 'has_war_with': return v in data.get('enemies', [])
            if k == 'is_in_war_together': return v in data.get('war_friends', [])
            if k == 'any_scope_treaty':
                return any(evaluate(children, '__treaty_' + p, world)
                           for p in data.get('allies', []))
            if k == 'binds': return data.get('partner') == v
            if k == 'any_scope_article': return all(one(x) for x in children)
            if k == 'has_type': return v == 'alliance'
            if k == 'has_diplomatic_pact':
                return n.one('type') == 'rivalry' and n.one('who') in data.get('rivals', [])
            raise ValueError('Unsupported test predicate: ' + k)
        return all(one(n) for n in nodes)

    offer = definition(ev, 'aor1776_american_diplomacy.4')
    check('R5.loan_title_and_description_have_only_triggered_branches', all(
        len(offer.children(part)[0].children()[0].children('triggered_desc')) == 2
        and not offer.children(part)[0].children()[0].children('desc') for part in ['title', 'desc']))
    fr = definition(ev, 'aor1776_american_diplomacy.3')
    check('R5.French_request_uses_native_fallback_structure',
          not sub(fr, 'desc').children()[0].children('desc'))
    results = []
    for level, approved in [(1, 0), (2, 5)]:
        world = {'c:USA': {'aor1776_support_offer_level': level}}
        snapshot = definition(fx, 'aor1776_support_issue_offer_effect').children()[0]
        for n in snapshot.children():
            if n.key == 'set_variable': world['c:USA'][n.one('name')] = int(n.one('value', '0'))
            elif n.key == 'if' and evaluate(n.children('limit')[0].children(), 'c:USA', world):
                for s in n.children('set_variable'):
                    world['c:USA'][s.one('name')] = int(s.one('value'))
        check('R5.approved_terms_snapshot.' + str(approved), world['c:USA']['aor1776_support_offered_interest'] == approved)
        # Changing the old negotiation level afterwards must not change the
        # offered title/description or the interest copied into the contract.
        world['c:USA']['aor1776_support_offer_level'] = 3 - level
        selected = {}
        for part in ['title', 'desc']:
            for branch in offer.children(part)[0].children()[0].children('triggered_desc'):
                if evaluate(branch.children('trigger')[0].children(), 'c:USA', world):
                    selected[part] = branch.one('desc'); break
        expected = {'title': 'aor1776_american_diplomacy.4.' + ('t_high' if approved else 't'),
                    'desc': 'aor1776_american_diplomacy.4.' + ('d_high' if approved else 'd')}
        check('R5.distinct_immutable_offer_text.' + str(approved), selected == expected)
        options = [n for n in offer.children('option') if n.one('name') != 'aor1776_american_diplomacy.4.b']
        matching = []
        for option in options:
            conditions = [n for n in option.children('trigger')[0].children()
                          if n.key != 'aor1776_french_support_can_accept']
            if evaluate(conditions, 'c:USA', world): matching.append(option)
        check('R5.only_correct_ratification_option.' + str(approved), len(matching) == 1
              and matching[0].one('name') == 'aor1776_american_diplomacy.4.' + ('c' if approved else 'a'))
        check('R5.failure_branch_hidden_from_preview.' + str(approved), len(matching) == 1
              and bool(matching[0].children('hidden_effect')))
        principal = Decimal(30000) * 3650 / 7
        due = principal * (Decimal('1.05') if approved else 1)
        results.append({'approved_interest': approved, 'selected_text': selected,
                        'nominal_due': str(due)})

    rule = definition(jt, 'aor1776_intervention_stake_in_war')
    cases = [
        ('Naples_without_Atlantic_interest', 'c:SIC', 'c:GBR', False, False, False, True, False),
        ('Ottomans_without_Atlantic_interest', 'c:TUR', 'c:GBR', False, False, False, True, False),
        ('Portugal_British_ally', 'c:POR', 'c:GBR', False, True, False, True, True),
        ('Portugal_without_alliance', 'c:POR', 'c:GBR', False, False, False, True, False),
        ('Spain_with_France', 'c:SPA', 'c:FRA', False, False, False, True, True),
        ('Spain_supporting_Britain', 'c:SPA', 'c:GBR', False, False, False, True, False),
        ('France_with_insurgents', 'c:FRA', 'c:USA', False, False, False, True, True),
        ('regional_interest_British_side', 'c:NET', 'c:GBR', True, False, False, True, True),
        ('regional_interest_American_side', 'c:NET', 'c:USA', True, False, False, True, True),
        ('rival_against_Britain', 'c:NET', 'c:USA', False, False, True, True, True),
        ('rival_may_not_help_Britain', 'c:TUR', 'c:GBR', False, False, True, True, False),
        ('other_conflict_unchanged', 'c:SIC', 'c:GBR', False, False, False, False, True),
    ]
    for name, actor, friend, interest, alliance, rival, american, expected in cases:
        world = {'$ACTOR$': actor, '$FRIEND$': friend,
                 'participants': {'c:USA', 'c:GBR'} if american else {'c:GBR', 'c:RUS'},
                 actor: {'interests': ['sr:region_atlantic_coast'] if interest else [],
                         'allies': ['c:GBR'] if alliance else [], 'rivals': ['c:GBR'] if rival else []},
                 friend: {'enemies': ['c:GBR'] if friend in {'c:USA', 'c:FRA'} else []},
                 '__treaty_c:GBR': {'partner': 'c:GBR'}}
        actual_result = evaluate(rule.children(), 'war', world)
        check('R5.intervention.' + name, actual_result == expected)
        results.append({'intervention_case': name, 'allowed': actual_result, 'expected': expected})
    check('R5.interest_gate_in_eligibility_and_each_joined_war',
          contains(definition(jt, 'aor1776_can_intervene_trigger'), 'aor1776_intervention_stake_in_war')
          and contains(definition('common/scripted_effects/1776_join_ongoing_wars.txt', 'aor1776_intervene_effect'), 'aor1776_intervention_stake_in_war'))

    monument = definition('common/buildings/08_monuments.txt', 'building_white_house')
    vanilla = parse((root.__class__('C:/Games/Victoria 3/game/common/buildings/08_monuments.txt')).read_text(encoding='utf-8-sig'))
    old = next(n for n in vanilla if n.key == 'building_white_house')
    check('R5.White_House_buildable_with_liberal_constitution', monument.one('buildable') == 'yes'
          and [n.value for n in sub(monument, 'unlocking_technologies').children()] == ['liberal_constitutionalism'])
    check('R5.White_House_unique_and_in_DC', monument.one('unique') == 'yes'
          and monument.one('expandable') == 'no' and sub(monument, 'potential').one('state_region') == 's:STATE_DISTRICT_OF_COLUMBIA')
    check('R5.White_House_other_properties_preserved', normalized([n for n in monument.children()
          if n.key not in {'buildable', 'unlocking_technologies'}]) == normalized([n for n in old.children() if n.key != 'buildable']))
    check('R5.other_monuments_preserved', normalized([n for n in tree('common/buildings/08_monuments.txt')
          if n.key != 'building_white_house']) == normalized([n for n in vanilla if n.key != 'building_white_house']))
    check('R5.no_White_House_granted_at_start', 'building_white_house' not in read('common/history/buildings/05_north_america.txt'))
    protected = json.loads((baseline.parent / 'BASELINE.json').read_text())
    for path, sha in protected['files'].items():
        if path.startswith(('map_data/', 'common/history/pops/', 'common/history/states/', 'common/history/military_formations/')) or path in {
                'common/history/buildings/05_north_america.txt', 'common/history/countries/zz_1776_usa_revolution_r2.txt'}:
            check('R5.protected.' + path, hashlib.sha256((root / path).read_bytes()).hexdigest() == sha)
    return results
