"""Read-only static/model checks; not a substitute for Victoria 3 runtime tests."""
from __future__ import annotations

import copy
import subprocess
from pathlib import Path

import validate_diplomacy_ottoman_1776 as script

ROOT = Path(__file__).resolve().parents[1]
BASE = '4b299b14b1f30c26f51c2c03250c12e503c594d1'
EFFECTS_PATH = 'common/scripted_effects/1776_ai_regional_infrastructure_effects.txt'
HOOKS_PATH = 'common/on_actions/13_1776_ai_regional_infrastructure.txt'
effects = {n.key: n for n in script.parse(script.read(EFFECTS_PATH))}
groups = {}
for path in (ROOT / 'common/production_method_groups').glob('*.txt'):
    for node in script.parse(path.read_text(encoding='utf-8-sig')):
        key = node.key.removeprefix('REPLACE_OR_CREATE:')
        if key in {'pmg_base_building_land_transport_network', 'pmg_base_building_railway',
                   'pmg_passenger_trains', 'pmg_land_transport_canals'}:
            groups[key] = node
pm_group = {script.scalar(pm.value): name for name, group in groups.items()
            for pm in group.children('production_methods')[0].children()}


def resolve(value, params):
    value = script.scalar(value)
    return params[value[1:-1]] if value.startswith('$') and value.endswith('$') else value


def buildings(scope):
    if 'states' in scope:
        return [s['building'] for s in scope['states'] if s['building']]
    return [scope['building']] if scope.get('building') else []


def condition(nodes, scope, params):
    def one(node):
        value = resolve(node.value, params) if not isinstance(node.value, list) else None
        if node.key == 'OR':
            return any(one(child) for child in node.children())
        if node.key == 'NOT':
            return not condition(node.children(), scope, params)
        if node.key == 'is_ai':
            return scope['ai'] == (value == 'yes')
        if node.key == 'has_building':
            assert value == 'building_railway'
            return bool(scope['building'])
        if node.key == 'has_variable':
            return value in scope['variables']
        if node.key == 'any_scope_building':
            return any(condition(node.children(), b, params) for b in buildings(scope))
        if node.key == 'is_building_type':
            return scope['type'] == value
        if node.key == 'has_active_production_method':
            return value in scope['active'].values()
        if node.key == 'can_activate_production_method':
            assert node.one('building_type') == 'building_railway'
            pm = resolve(node.one('production_method'), params)
            # Also exercise the conservative case where an already active PM
            # cannot be activated again: selectors must not downgrade it.
            return pm in scope['available'] and pm not in scope['building']['active'].values()
        raise AssertionError(f'Unsupported test trigger: {node.key}')
    return all(one(node) for node in nodes)


def execute(nodes, scope, params=None):
    params = params or {}
    matched = False
    for node in nodes:
        if node.key in {'if', 'else_if', 'else'}:
            if node.key == 'if':
                matched = False
            if matched:
                continue
            limits = node.children('limit')
            if not limits or condition(limits[0].children(), scope, params):
                matched = True
                execute([c for c in node.children() if c.key != 'limit'], scope, params)
        elif node.key == 'every_scope_state':
            limits = node.children('limit')
            for state in scope['states']:
                if not limits or condition(limits[0].children(), state, params):
                    execute([c for c in node.children() if c.key != 'limit'], state, params)
        elif node.key == 'ordered_scope_state':
            assert node.one('order_by') == 'gdp'
            assert node.one('check_range_bounds') == 'no'
            assert not node.children('limit'), 'GDP ranking must include all owned states'
            index = int(resolve(node.one('position'), params))
            ordered = sorted(scope['states'], key=lambda s: -s['gdp'])
            if index < len(ordered):
                execute([c for c in node.children() if c.key not in
                         {'order_by', 'position', 'check_range_bounds'}], ordered[index], params)
        elif node.key in {'set_variable', 'remove_variable'}:
            variable = resolve(node.value, params)
            if node.key == 'set_variable':
                scope['variables'].add(variable)
            else:
                scope['variables'].discard(variable)
        elif node.key == 'activate_production_method':
            assert node.one('building_type') == 'building_railway'
            pm = resolve(node.one('production_method'), params)
            assert scope['building'], 'Must not create an infrastructure building'
            assert pm in scope['available'], f'Locked PM forced: {pm}'
            scope['building']['active'][pm_group[pm]] = pm
            scope['changes'].append(pm)
        elif node.key in effects:
            arguments = {n.key: resolve(n.value, params) for n in node.children()}
            execute(effects[node.key].children(), scope, arguments)
        else:
            raise AssertionError(f'Unsupported test effect: {node.key}')


def country(count, ai=True, available=None):
    defaults = {key: script.scalar(group.children('production_methods')[0].children()[0].value)
                for key, group in groups.items()}
    return {'ai': ai, 'states': [
        {'gdp': 1000 - i, 'variables': set(), 'available': set(available or pm_group),
         'building': {'type': 'building_railway', 'active': defaults.copy(), 'levels': 2},
         'changes': []} for i in range(count)]}


def refresh(scope):
    execute(effects['aor1776_ai_refresh_regional_infrastructure'].children(), scope)


def selected(scope):
    return [s for s in scope['states'] if 'aor1776_ai_top_gdp_canal_state' in s['variables']]


def run_tests():
    hooks = {n.key: n for n in script.parse(script.read(HOOKS_PATH))}
    for name in ('on_game_started_after_lobby', 'on_monthly_pulse_country'):
        hook = hooks[name]
        assert hook.children('on_actions') and not hook.children('effect')
        for child in hook.children('on_actions')[0].children():
            assert script.scalar(child.value) in hooks
    for name in ('pmg_base_building_land_transport_network', 'pmg_base_building_railway',
                 'pmg_passenger_trains'):
        assert groups[name].one('ai_selection') == 'most_productive'
    # Existing recipes, staffing, technologies, textures and unrelated PMs unchanged.
    weighted_files = [
        'common/production_methods/22_tech7a_wave_a_land_transport_production.txt',
        'common/production_methods/11_private_infrastructure.txt',
        'common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt']
    for path in weighted_files:
        original = script.parse(subprocess.check_output(['git', 'show', f'{BASE}:{path}'],
                                cwd=ROOT).decode('utf-8-sig'))
        current = script.parse(script.read(path))
        for node in current:
            if node.key in pm_group:
                node.value = [c for c in node.children() if c.key != 'ai_weight']
        assert script.normalized(original) == script.normalized(current), path
    path = 'common/production_method_groups/22_tech7a_wave_a_land_transport_pmgs.txt'
    original = script.parse(subprocess.check_output(['git', 'show', f'{BASE}:{path}'],
                            cwd=ROOT).decode('utf-8-sig'))
    current = script.parse(script.read(path))
    current[0].value = [c for c in current[0].children() if c.key != 'ai_selection']
    assert script.normalized(original) == script.normalized(current)
    definitions = {}
    for path in (ROOT / 'common/production_methods').glob('*.txt'):
        definitions.update({n.key.removeprefix('REPLACE_OR_CREATE:'): n
                           for n in script.parse(path.read_text(encoding='utf-8-sig'))})
    assert set(pm_group) <= definitions.keys()
    for name in ('pmg_base_building_land_transport_network', 'pmg_base_building_railway',
                 'pmg_passenger_trains'):
        pm_names = [script.scalar(n.value) for n in groups[name].children('production_methods')[0].children()]
        weights = [float(definitions[pm].one('ai_weight')) for pm in pm_names]
        assert all(a < b for a, b in zip(weights, weights[1:])), (name, weights)
    for name, effect in effects.items():
        for node in script.walk(effect.children()):
            if node.key in {'production_method', 'has_active_production_method', 'PM'}:
                pm = script.scalar(node.value)
                assert pm.startswith('$') or pm in pm_group, (name, pm)
    positions = [int(n.one('POSITION')) for n in script.walk(
        effects['aor1776_ai_refresh_regional_infrastructure'].children())
        if n.key == 'aor1776_ai_mark_canal_gdp_position']
    assert positions == list(range(10))

    large = country(13)
    large['states'][0]['building'] = None  # Richest state still counts in the top ten.
    refresh(large)
    assert len(selected(large)) == 10
    assert large['states'][0]['building'] is None
    for i, state in enumerate(large['states'][1:], 1):
        active = state['building']['active']
        assert active['pmg_base_building_land_transport_network'] == 'pm_paved_road_network'
        assert active['pmg_base_building_railway'] == 'pm_diesel_trains_principle_transport_3'
        assert active['pmg_passenger_trains'] == 'pm_aluminium_passenger_carriages'
        assert active['pmg_land_transport_canals'] == (
            'pm_engineered_canals' if i < 10 else 'pm_no_canal_network')
        assert state['building']['levels'] == 2
    counts = [len(s['changes']) for s in large['states']]
    refresh(large)
    assert counts == [len(s['changes']) for s in large['states']], 'Not idempotent'
    large['states'][12]['gdp'] = 2000
    refresh(large)
    assert large['states'][12]['building']['active']['pmg_land_transport_canals'] == 'pm_engineered_canals'
    assert large['states'][9]['building']['active']['pmg_land_transport_canals'] == 'pm_no_canal_network'

    for size in (1, 5, 10, 11):
        small = country(size)
        for state in small['states']:
            state['gdp'] = 100  # Ties must not admit more than ten states.
        refresh(small)
        assert len(selected(small)) == min(size, 10)
    player = country(13, ai=False)
    snapshot = copy.deepcopy(player)
    refresh(player)
    assert player == snapshot
    locked = country(2, available={'pm_traditional_road_network', 'pm_no_rail_network',
                                   'pm_no_passenger_trains', 'pm_no_canal_network'})
    refresh(locked)
    assert all(not s['changes'] for s in locked['states'])
    middle = country(2, available={'pm_traditional_road_network', 'pm_turnpike_road_network',
        'pm_no_rail_network', 'pm_early_trains', 'pm_no_passenger_trains',
        'pm_wooden_passenger_carriages', 'pm_no_canal_network', 'pm_industrial_canals'})
    refresh(middle)
    for state in middle['states']:
        assert set(state['building']['active'].values()) == {
            'pm_turnpike_road_network', 'pm_early_trains',
            'pm_wooden_passenger_carriages', 'pm_industrial_canals'}
    print('PASS: hooks, PM references, preserved recipes, top 10 GDP, ties/small countries,')
    print('      ranking changes, unlocked tiers, no new buildings, player protection, idempotence.')
    print('Static/model validation only: confirm engine behaviour and economy in game.')


if __name__ == '__main__':
    run_tests()
