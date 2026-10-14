"""Execute actual Clausewitz AST against explicit fixtures, NOT the game engine.

No prices, hiring, construction, profitability or AI budgeting are simulated.
--write-report records generated QA artifacts; default is read-only.
"""
from __future__ import annotations
import copy
import hashlib
import json
import operator
import re
import subprocess
import sys
from pathlib import Path
import validate_diplomacy_ottoman_1776 as script
import regional_infrastructure_shortage_patch as patch

ROOT, REPORT = patch.ROOT, patch.REPORT
TRIGGERS = {n.key: n for n in script.parse(script.read(patch.TRIGGERS))}
EFFECTS = {n.key: n for n in script.parse(script.read(patch.EFFECTS))}
VALUES = {n.key: n for n in script.parse(script.read(patch.VALUES))}
PM_DEFS = patch.catalog('common/production_methods')
RECIPES = {pm: patch.inputs(PM_DEFS[pm][2]) for pm in patch.PM_NAMES}
GOODS = sorted({g for recipe in RECIPES.values() for g in recipe})
GROUP_NAMES = {'roads': 'pmg_base_building_land_transport_network',
               'rail': 'pmg_base_building_railway', 'wagons': 'pmg_passenger_trains',
               'canals': 'pmg_land_transport_canals'}
PM_GROUP = {pm: GROUP_NAMES[g] for g, names in patch.GROUPS.items() for pm in names}
COMPARE = {'=': operator.eq, '?=': operator.eq, '<': operator.lt, '>': operator.gt,
           '<=': operator.le, '>=': operator.ge, '!=': operator.ne}


class Model:
    def __init__(self, scope):
        self.root = scope
        self.saved = {}
        self.day = 0
        self.positions = []

    def variable(self, scope, key):
        var = scope['variables'].get(key)
        return var['value'] if var and var['expires'] > self.day else 0

    def has_variable(self, scope, key):
        var = scope['variables'].get(key)
        return bool(var and var['expires'] > self.day)

    def value(self, value, scope, params=None):
        if isinstance(value, list):
            return self.score(value, scope, params)
        value = script.scalar(value)
        if value.startswith('$'):
            return self.value(params[value[1:-1]], scope)
        if value in VALUES:
            return self.score(VALUES[value].children(), scope, params)
        if value.startswith('scope:'):
            name, chain = value.removeprefix('scope:').split('.', 1)
            target = self.saved[name]
            while chain.startswith('owner.'):
                target = target['owner']
                chain = chain.removeprefix('owner.')
            assert chain.startswith('var:'), chain
            return self.variable(target, chain.removeprefix('var:'))
        if value == 'b:building_railway.level':
            return scope['building']['levels']
        if value.startswith('var:'):
            return self.variable(scope, value.removeprefix('var:'))
        if value in scope:
            return scope[value]
        try:
            return float(value)
        except ValueError:
            return value

    def score(self, nodes, scope, params=None):
        total = 0
        matched = False
        for node in nodes:
            if node.key in ('if', 'else_if', 'else'):
                if node.key == 'if':
                    matched = False
                if matched:
                    continue
                limit = node.children('limit')
                if not limit or self.condition(limit[0].children(), scope, params):
                    matched = True
                    nested = [n for n in node.children() if n.key != 'limit']
                    # Script values retain the current accumulator through if.
                    for operation in nested:
                        amount = self.value(operation.value, scope, params)
                        if operation.key == 'multiply':
                            total *= amount
                        elif operation.key == 'add':
                            total += amount
                        else:
                            raise AssertionError(operation.key)
            else:
                amount = self.value(node.value, scope, params)
                if node.key == 'value':
                    total = amount
                elif node.key == 'add':
                    total += amount
                elif node.key == 'multiply':
                    total *= amount
                else:
                    raise AssertionError(node.key)
        return total

    def buildings(self, scope):
        if 'states' in scope:
            return [b for state in scope['states'] for b in self.buildings(state)]
        return ([scope['building']] if scope.get('building') else []) + scope.get('suppliers', [])

    def condition(self, nodes, scope, params=None):
        params = params or {}
        def one(node):
            key = node.key
            if key in ('OR', 'AND', 'NOT', 'NOR', 'NAND'):
                results = [one(n) for n in node.children()]
                return {'OR': any, 'AND': all, 'NOT': lambda v: not all(v),
                        'NOR': lambda v: not any(v), 'NAND': lambda v: not all(v)}[key](results)
            if key in TRIGGERS:
                answer = self.condition(TRIGGERS[key].children(), scope, params)
                return answer == (script.scalar(node.value) == 'yes')
            if key in ('owner', 'state', 'market'):
                return self.condition(node.children(), scope[key], params)
            if key.startswith(('sg:', 'mg:')):
                return self.condition(node.children(), scope['goods'][key[3:]], params)
            if key == 'any_scope_building':
                return any(self.condition(node.children(), b, params) for b in self.buildings(scope))
            if key == 'can_activate_production_method':
                assert node.one('building_type') == 'building_railway'
                pm = script.scalar(node.one('production_method'))
                return pm in scope['available'] and pm not in scope['building']['active'].values()
            value = self.value(node.value, scope, params)
            if key == 'is_ai':
                return scope['ai'] == (value == 'yes')
            if key == 'always':
                return value == 'yes'
            if key == 'has_technology_researched':
                return value in scope['technologies']
            if key == 'has_variable':
                return self.has_variable(scope, value)
            if key == 'has_building':
                return any(b['type'] == value for b in self.buildings(scope))
            if key == 'is_building_type':
                return scope['type'] == value
            if key == 'has_active_production_method':
                return value in scope.get('active', {}).values()
            if key in ('building_has_goods_shortage', 'is_under_construction',
                       'state_goods_has_local_goods_shortage', 'market_goods_has_goods_shortage',
                       'is_isolated_from_market'):
                return scope.get(key, False) == (value == 'yes')
            if key == 'num_states':
                return COMPARE[node.op](len(scope['states']), value)
            if key in ('market_access', 'infrastructure_delta', 'occupancy',
                       'state_goods_pricier', 'state_goods_production', 'state_goods_consumption',
                       'market_goods_sell_orders', 'market_goods_buy_orders'):
                return COMPARE[node.op](scope[key], value)
            raise AssertionError(f'Unsupported fixture trigger {key}')
        return all(one(n) for n in nodes)

    def execute(self, nodes, scope, params=None):
        params = params or {}
        matched = False
        for node in nodes:
            key = node.key
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    matched = False
                if matched:
                    continue
                limit = node.children('limit')
                if not limit or self.condition(limit[0].children(), scope, params):
                    matched = True
                    self.execute([n for n in node.children() if n.key != 'limit'], scope, params)
            elif key == 'every_scope_state':
                limit = node.children('limit')
                for state in scope['states']:
                    if not limit or self.condition(limit[0].children(), state, params):
                        self.execute([n for n in node.children() if n.key != 'limit'], state, params)
            elif key == 'ordered_scope_state':
                assert node.one('order_by') == 'gdp'
                assert not node.children('limit'), 'Rank ALL owned states'
                index = int(self.value(node.one('position'), scope, params))
                states = sorted(scope['states'], key=lambda s: -s['gdp'])
                assert index < len(states), 'Out-of-range GDP position attempted'
                self.positions.append(index)
                self.execute([n for n in node.children() if n.key not in
                              ('order_by', 'position', 'check_range_bounds')], states[index], params)
            elif key in ('owner', 'state', 'market'):
                self.execute(node.children(), scope[key], params)
            elif key == 'save_scope_as':
                self.saved[script.scalar(node.value)] = scope
            elif key == 'set_variable':
                if node.children():
                    name = script.scalar(node.one('name'))
                    value = self.value(node.one('value', '1'), scope, params)
                    duration = float(node.one('days', '1000000'))
                else:
                    name, value, duration = script.scalar(node.value), 1, 1000000
                scope['variables'][name] = {'value': value, 'expires': self.day + duration}
            elif key == 'remove_variable':
                scope['variables'].pop(script.scalar(node.value), None)
            elif key == 'change_variable':
                name = script.scalar(node.one('name'))
                value = self.variable(scope, name) + self.value(node.one('add'), scope, params)
                scope['variables'][name] = {'value': value, 'expires': 1000000}
            elif key == 'activate_production_method':
                pm = self.value(node.one('production_method'), scope, params)
                assert pm in scope['available'], f'Locked PM activated: {pm}'
                assert scope['building'], 'No building creation allowed'
                scope['building']['active'][PM_GROUP[pm]] = pm
                scope['changes'].append({'day': self.day, 'pm': pm})
            elif key in EFFECTS:
                args = {n.key: self.value(n.value, scope, params) for n in node.children()}
                self.execute(EFFECTS[key].children(), scope, args)
            else:
                raise AssertionError(f'Unsupported fixture effect {key}')

    def refresh(self, day=None):
        if day is not None:
            self.day = day
        self.execute(EFFECTS['aor1776_ai_refresh_regional_infrastructure'].children(), self.root)


def country(count, ai=True, available=None):
    technologies = {script.scalar(n.value) for top in TRIGGERS.values()
                    for n in script.walk(top.children()) if n.key == 'has_technology_researched'}
    country = {'ai': ai, 'variables': {}, 'states': [], 'technologies': technologies, 'market': {'goods': {
        g: {'market_goods_has_goods_shortage': False, 'market_goods_sell_orders': 10000,
            'market_goods_buy_orders': 100} for g in GOODS}}}
    defaults = {GROUP_NAMES[g]: candidates[-1] for g, candidates in patch.GROUPS.items()}
    for i in range(count):
        state = {'owner': country, 'market': country['market'], 'variables': {},
                 'gdp': 1000 - i, 'market_access': 1, 'is_isolated_from_market': False,
                 'infrastructure_delta': -30, 'changes': [], 'suppliers': [],
                 'available': set(available if available is not None else patch.PM_NAMES),
                 'goods': {g: {'state_goods_has_local_goods_shortage': False,
                    'state_goods_pricier': 0, 'state_goods_production': 10000 if g == 'electricity' else 0,
                    'state_goods_consumption': 100} for g in GOODS + ['transportation']}}
        state['building'] = {'type': 'building_railway', 'active': defaults.copy(),
                             'levels': 2, 'occupancy': 1, 'owner': country, 'state': state,
                             'building_has_goods_shortage': False, 'is_under_construction': False}
        country['states'].append(state)
    return country


def public_snapshot(country):
    return {'variables': copy.deepcopy(country['variables']), 'states': [
        {'variables': copy.deepcopy(s['variables']), 'changes': copy.deepcopy(s['changes']),
         'active': copy.deepcopy(s['building']['active']) if s['building'] else None,
         'levels': s['building']['levels'] if s['building'] else None} for s in country['states']]}


def set_shortage(country, goods):
    for good in goods:
        country['market']['goods'][good].update(market_goods_sell_orders=0,
                                                market_goods_has_goods_shortage=True)
        for state in country['states']:
            state['goods'][good]['state_goods_production'] = 0
            state['goods'][good]['state_goods_pricier'] = .75
    for state in country['states']:
        state['building']['building_has_goods_shortage'] = True


def construction_checks(model, state, allowed):
    node = patch.catalog('common/buildings')['building_railway'][2]
    for name in ('can_build_government', 'can_build_private'):
        assert model.condition(node.children(name)[0].children(), state) == allowed, name
    assert model.condition(node.children('should_auto_expand')[0].children(), state['building']) == allowed


def model_tests():
    results = []
    # Eight required fixture families, followed by boundary/regression checks.
    healthy = country(13)
    model = Model(healthy)
    healthy['states'][0]['building'] = None
    model.refresh(0)
    assert len([s for s in healthy['states'] if model.has_variable(s, 'aor1776_ai_top_gdp_canal_state')]) == 10
    construction_checks(model, healthy['states'][1], True)
    for state in healthy['states'][1:]:
        assert state['building']['active'][GROUP_NAMES['roads']] == 'pm_paved_road_network'
        assert state['building']['active'][GROUP_NAMES['rail']] == 'pm_diesel_trains_principle_transport_3'
        assert state['building']['levels'] == 2
    initial = public_snapshot(healthy)
    model.refresh(30)
    assert [s['changes'] for s in initial['states']] == [s['changes'] for s in public_snapshot(healthy)['states']]
    healthy['states'][12]['gdp'] = 2000
    model.refresh(60)
    assert healthy['states'][9]['building']['active'][GROUP_NAMES['canals']] == 'pm_no_canal_network'
    model.refresh(240)
    assert healthy['states'][12]['building']['active'][GROUP_NAMES['canals']] == 'pm_engineered_canals'
    results.append({'scenario': 'infrastructure_deficit_without_shortage', 'result': 'PASS',
                    'construction_permission': True, 'observed_script_changes': initial})

    for name, missing, expected in [
        ('severe_tools_shortage', ['tools'], 'pm_traditional_road_network'),
        ('cement_limestone_shortage', ['cement', 'limestone'], 'pm_turnpike_road_network'),
        ('rail_input_shortage', ['engines'], 'pm_no_rail_network')]:
        c = country(1)
        m = Model(c)
        m.refresh(0)
        set_shortage(c, missing)
        timeline = []
        before = c['states'][0]['building']['active'].copy()
        for month in range(1, 9):
            m.refresh(month * 30)
            construction_checks(m, c['states'][0], False)
            timeline.append({'day': m.day, 'active': c['states'][0]['building']['active'].copy()})
        assert timeline[0]['active'] == before, 'Transient shock changed PMs'
        key = GROUP_NAMES['rail'] if name == 'rail_input_shortage' else GROUP_NAMES['roads']
        assert timeline[1]['active'][key] == expected
        assert all(row['active'] == timeline[1]['active'] for row in timeline[2:]), 'Persistent shock caused oscillation'
        for good in missing:
            assert m.has_variable(c['states'][0], f'aor1776_ai_need_{good}') or not any(
                good in RECIPES[pm] for pm in c['states'][0]['building']['active'].values())
        results.append({'scenario': name, 'result': 'PASS', 'timeline': timeline,
                        'construction_permission_during_shortage': False})

    absent = country(1)
    for good in ('cement', 'limestone', 'heavy_petroleum_products', 'engines', 'aluminium'):
        absent['market']['goods'][good]['market_goods_sell_orders'] = 0
    am = Model(absent)
    am.refresh(0)
    assert absent['states'][0]['building']['active'][GROUP_NAMES['roads']] == 'pm_turnpike_road_network'
    assert absent['states'][0]['building']['active'][GROUP_NAMES['rail']] == 'pm_no_rail_network'
    results.append({'scenario': 'market_with_no_required_production', 'result': 'PASS'})

    recovering = country(1)
    rm = Model(recovering)
    rm.refresh(0)
    set_shortage(recovering, ['tools'])
    rm.refresh(30)
    rm.refresh(60)
    fallback = recovering['states'][0]['building']['active'].copy()
    recovering['market']['goods']['tools'].update(market_goods_sell_orders=10000, market_goods_has_goods_shortage=False)
    recovering['states'][0]['goods']['tools']['state_goods_pricier'] = 0
    recovering['states'][0]['building']['building_has_goods_shortage'] = False
    for day in (90, 120, 150, 180, 210):
        rm.refresh(day)
        assert recovering['states'][0]['building']['active'] == fallback
        construction_checks(rm, recovering['states'][0], True)
    rm.refresh(240)
    assert recovering['states'][0]['building']['active'][GROUP_NAMES['roads']] == 'pm_paved_road_network'
    results.append({'scenario': 'supply_recovery_with_180_day_cooldown', 'result': 'PASS',
                    'changes': recovering['states'][0]['changes']})

    player = country(13, ai=False)
    set_shortage(player, ['tools', 'cement'])
    before = public_snapshot(player)
    pm = Model(player)
    for day in range(0, 361, 30):
        pm.refresh(day)
    assert public_snapshot(player) == before
    construction_checks(pm, player['states'][0], True)
    results.append({'scenario': 'human_country_exclusion', 'result': 'PASS'})

    mixed = country(3)
    mixed['states'][0]['market_access'] = .25
    mixed['states'][0]['is_isolated_from_market'] = True
    mixed['states'][0]['building']['active'][GROUP_NAMES['roads']] = 'pm_turnpike_road_network'
    mixed['states'][0]['building']['building_has_goods_shortage'] = True
    mixed['states'][0]['goods']['tools']['state_goods_has_local_goods_shortage'] = True
    mixed['states'][0]['goods']['wood']['state_goods_production'] = 0
    mm = Model(mixed)
    mm.refresh(0)
    assert not mm.has_variable(mixed, 'aor1776_ai_connected_need_tools'), 'Local crisis leaked to connected market'
    mm.refresh(30)
    assert mixed['states'][0]['building']['active'][GROUP_NAMES['roads']] == 'pm_traditional_road_network'
    assert mixed['states'][1]['building']['active'][GROUP_NAMES['roads']] == 'pm_paved_road_network'
    assert mm.condition(TRIGGERS['aor1776_ai_prioritize_tools'].children(), mixed['states'][0])
    assert not mm.condition(TRIGGERS['aor1776_ai_prioritize_tools'].children(), mixed['states'][1])
    # Isolated states may use adequate REAL local production, never hypothetical imports.
    local = mixed['states'][2]
    local['market_access'] = .1
    local['is_isolated_from_market'] = True
    local['goods']['tools']['state_goods_production'] = 1000
    mm.saved['aor1776_ai_regional_state'] = local
    assert mm.condition(TRIGGERS['aor1776_ai_supply_tools'].children(), local)
    results.append({'scenario': 'multiple_states_connected_and_isolated', 'result': 'PASS'})

    for size in (1, 5, 10, 11):
        c = country(size)
        for state in c['states']:
            state['gdp'] = 100
        m = Model(c)
        m.refresh()
        assert m.positions == list(range(min(size, 10)))
        assert sum(m.has_variable(s, 'aor1776_ai_top_gdp_canal_state') for s in c['states']) == min(size, 10)
    locked = country(2, available={names[-1] for names in patch.GROUPS.values()})
    Model(locked).refresh()
    assert all(not s['changes'] for s in locked['states'])
    middle = country(2, available={'pm_traditional_road_network', 'pm_turnpike_road_network',
        'pm_no_rail_network', 'pm_early_trains', 'pm_no_passenger_trains',
        'pm_wooden_passenger_carriages', 'pm_no_canal_network', 'pm_industrial_canals'})
    Model(middle).refresh()
    assert all(set(s['building']['active'].values()) == {
        'pm_turnpike_road_network', 'pm_early_trains', 'pm_wooden_passenger_carriages',
        'pm_industrial_canals'} for s in middle['states'])
    # Adequate electric principle (24) wins over normal diesel (17).
    ranked = country(1, available=patch.PM_NAMES - {'pm_diesel_trains_principle_transport_3'})
    Model(ranked).refresh()
    assert ranked['states'][0]['building']['active'][GROUP_NAMES['rail']] == 'pm_electric_trains_principle_transport_3'
    # Forecast gate: supply exists and no engine shortage yet, but too little
    # headroom for full employment. Do not blindly activate the highest PM.
    tight = country(1)
    tight['market']['goods']['tools'].update(market_goods_buy_orders=100, market_goods_sell_orders=100)
    Model(tight).refresh()
    assert tight['states'][0]['building']['active'][GROUP_NAMES['roads']] == 'pm_traditional_road_network'
    # Multiple states cannot spend the same market headroom within one pulse.
    limited = country(10)
    limited['market']['goods']['tools'].update(market_goods_buy_orders=100, market_goods_sell_orders=110)
    Model(limited).refresh()
    count = sum(s['building']['active'][GROUP_NAMES['roads']] == 'pm_paved_road_network' for s in limited['states'])
    assert 0 < count < 10, count
    results.append({'scenario': 'bounded_country_market_reserve', 'result': 'PASS', 'paved_states_in_first_pulse': count})

    # Actual supplier score multiplier, no boost while queued or itself short.
    supplier_country = country(1)
    state = supplier_country['states'][0]
    model = Model(supplier_country)
    model.execute(script.parse('set_variable = { name = aor1776_ai_need_tools days = 180 }'), state)
    tooling = patch.catalog('common/buildings')['building_tooling_workshop'][2].children('ai_value')[0]
    assert model.score(tooling.children(), state) == 8000
    for problem in ('is_under_construction', 'building_has_goods_shortage'):
        state['suppliers'] = [{'type': 'building_tooling_workshop', problem: True}]
        assert model.score(tooling.children(), state) == 2000
    state['suppliers'] = []
    model.day = 180
    assert model.score(tooling.children(), state) == 2000
    model.execute(script.parse('set_variable = { name = aor1776_ai_need_aluminium days = 180 }'), state)
    alloys = patch.catalog('common/buildings')['building_alloys_plant'][2].children('ai_value')[0]
    supplier_country['technologies'] = set()
    assert model.score(alloys.children(), state) == 1600, 'Boosted an aluminium producer with no output PM unlocked'
    supplier_country['technologies'] = {'bauxite_processing'}
    assert model.score(alloys.children(), state) == 6400
    results.append({'scenario': 'supplier_queue_shortage_and_expiration_guards', 'result': 'PASS'})
    return results


def static_checks():
    catalogs = {folder: patch.catalog(f'common/{folder}') for folder in
                ('buildings', 'production_methods', 'production_method_groups')}
    # Every current recipe input must be tested, not only roads/tools.
    for pm, recipe in RECIPES.items():
        trigger = TRIGGERS[f'aor1776_ai_sustainable_{pm}']
        required = {n.key.removeprefix('aor1776_ai_supply_') for n in trigger.children()
                    if n.key.startswith('aor1776_ai_supply_')}
        assert required == set(recipe), (pm, required, recipe)
        weight = PM_DEFS[pm][2].one('ai_weight', '1')
        assert float(weight) == 1, (pm, weight)
    for group in ('roads', 'rail', 'canals'):
        nominal = []
        for pm in patch.GROUPS[group]:
            amounts = [float(n.value) for n in script.walk(PM_DEFS[pm][2].children())
                       if n.key == 'state_infrastructure_add']
            nominal.append(sum(amounts))
        assert all(a >= b for a, b in zip(nominal, nominal[1:])), (group, nominal)
    refs = set()
    for nodes in (TRIGGERS.values(), EFFECTS.values(), VALUES.values()):
        for top in nodes:
            for n in script.walk(top.children()):
                if n.key.startswith('aor1776_ai_'):
                    refs.add(n.key)
                if n.key in ('production_method', 'has_active_production_method', 'PM'):
                    value = script.scalar(n.value)
                    assert value.startswith('$') or value in patch.PM_NAMES
    assert refs <= set(TRIGGERS) | set(EFFECTS) | set(VALUES), refs - (set(TRIGGERS) | set(EFFECTS) | set(VALUES))
    technologies = patch.catalog('common/technology/technologies')
    for top in TRIGGERS.values():
        for n in script.walk(top.children()):
            if n.key == 'has_technology_researched':
                assert script.scalar(n.value) in technologies, script.scalar(n.value)
    forbidden = {'add_building', 'create_building', 'create_building_levels', 'add_technology',
                 'set_subsidized', 'create_pop', 'set_province_owner'}
    assert not forbidden & {n.key for e in EFFECTS.values() for n in script.walk(e.children())}
    hooks = {n.key: n for n in script.parse(script.read('common/on_actions/13_1776_ai_regional_infrastructure.txt'))}
    for name in ('on_game_started_after_lobby', 'on_monthly_pulse_country'):
        assert hooks[name].children('on_actions') and not hooks[name].children('effect')
    initial = json.loads((REPORT / 'baseline.json').read_text(encoding='utf-8'))['files']
    other = json.loads((REPORT / 'baseline_other.json').read_text(encoding='utf-8'))['files']
    expected = {patch.EFFECTS,
                'common/buildings/01_industry.txt', 'common/buildings/03_mines.txt',
                'common/buildings/06_urban_center.txt', 'common/buildings/09_misc_resource.txt',
                'common/buildings/10_tech6c1_limestone_quarry.txt',
                'common/buildings/11_private_infrastructure.txt',
                'common/buildings/11_tech6c1b_cement_works.txt',
                'common/buildings/12_tech6c4_oil_refinery.txt',
                'common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt',
                'common/production_methods/11_private_infrastructure.txt',
                'common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt',
                'common/production_methods/22_tech7a_wave_a_land_transport_production.txt'}
    changed = {relative for relative, digest in initial.items()
               if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != digest}
    assert changed == expected, (changed - expected, expected - changed)
    assert all(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest for relative, digest in other.items())
    # Exact parsed comparison to current pre-task HEAD: only AI metadata changes.
    for relative in changed - {patch.EFFECTS}:
        old = script.parse(subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=ROOT).decode('utf-8-sig'))
        current = script.parse(script.read(relative))
        if 'production_methods/' in relative:
            for nodes in (old, current):
                for n in nodes:
                    if n.key.removeprefix('REPLACE_OR_CREATE:') in patch.PM_NAMES:
                        n.value = [c for c in n.children() if c.key != 'ai_weight']
        else:
            for nodes in (old, current):
                for n in nodes:
                    if n.key in patch.SUPPLIERS:
                        n.value = [c for c in n.children() if c.key != 'ai_value']
                    elif n.key == 'building_railway':
                        n.value = [c for c in n.children() if c.key not in
                                   ('ai_value', 'should_auto_expand', 'can_build_government', 'can_build_private')]
        assert script.normalized(old) == script.normalized(current), relative
    # Original historical journal boosts are preserved, with the veto last.
    railway = catalogs['buildings']['building_railway'][2]
    original = next(n for n in script.parse(subprocess.check_output(
        ['git', 'show', 'HEAD:common/buildings/11_private_infrastructure.txt'], cwd=ROOT).decode('utf-8-sig')) if n.key == 'building_railway')
    av = railway.children('ai_value')[0].children()
    assert script.normalized(av[:-1]) == script.normalized(original.children('ai_value')[0].children())
    assert av[-1].one('multiply') == '0'
    for building, (path, _, current) in catalogs['buildings'].items():
        if building not in patch.SUPPLIERS:
            continue
        relative = path.relative_to(ROOT).as_posix()
        old = next(n for n in script.parse(subprocess.check_output(
            ['git', 'show', f'HEAD:{relative}'], cwd=ROOT).decode('utf-8-sig')) if n.key == building)
        old_av = old.children('ai_value')
        new_av = current.children('ai_value')[0].children()
        if old_av and isinstance(old_av[0].value, list):
            assert script.normalized(new_av[:-1]) == script.normalized(old_av[0].children()), building
        else:
            assert new_av[0].value == (old_av[0].value if old_av else '1000'), building
        assert new_av[-1].one('multiply') == '4', building
    for good in GOODS:
        local = VALUES[f'aor1776_ai_local_reserve_{good}']
        market = VALUES[f'aor1776_ai_market_reserve_{good}']
        assert not any(isinstance(n.value, str) and 'aor1776_ai_reserved_' in n.value for n in local.children())
        assert any(isinstance(n.value, str) and f'aor1776_ai_reserved_{good}' in n.value for n in market.children())
    for relative in changed | {patch.TRIGGERS, patch.VALUES}:
        script.parse(script.read(relative))
    return {'changed_existing_runtime_files': sorted(changed), 'new_runtime_files': [patch.TRIGGERS, patch.VALUES],
            'protected_files_verified': len(set(initial) | set(other)),
            'unchanged_MAP1C_files': sum(r.startswith('docs/reports/map/MAP1C/') for r in initial),
            'history_map_population_recipes_and_unlocks': 'UNCHANGED', 'journal_construction_boosts': 'PRESERVED'}


def engine_evidence():
    exe = Path('C:/Games/Victoria 3/binaries/victoria3.exe')
    raw = exe.read_bytes()
    symbols = ['building_has_goods_shortage', 'state_goods_has_local_goods_shortage',
               'market_goods_has_goods_shortage', 'state_goods_production', 'state_goods_consumption',
               'market_goods_sell_orders', 'market_goods_buy_orders', 'can_build_government', 'can_build_private']
    found = {}
    for name in symbols:
        occurrences = [m.start() for m in re.finditer(re.escape(name.encode()), raw)]
        assert occurrences, f'Native engine symbol missing: {name}'
        found[name] = occurrences[:3]
    # This is symbol/documentation availability, not successful engine execution.
    return {'exe_sha256': hashlib.sha256(raw).hexdigest(), 'verified_symbols': found,
            'game_version': '1.13.11 (VersionInfo and system.log checked)',
            'runtime_validation': 'NOT_RUN', 'economic_measurements': 'NOT_AVAILABLE'}


def run(write=False):
    data = {'validation_kind': 'STATIC_AND_ACTUAL_SCRIPT_AST_FIXTURES_NOT_ENGINE',
            'static': static_checks(), 'scenarios': model_tests(), 'engine_evidence': engine_evidence()}
    if write:
        (REPORT / 'VALIDATION.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        baseline = json.loads((REPORT / 'baseline.json').read_text(encoding='utf-8'))['files']
        paths = (data['static']['changed_existing_runtime_files'] + data['static']['new_runtime_files'] +
                 ['tools/validate_ai_regional_infrastructure_1776.py',
                  'tools/validate_regional_infrastructure_shortage.py',
                  'tools/regional_infrastructure_shortage_patch.py'])
        manifest = {'purpose': 'Isolated regional infrastructure shortage correction',
                    'base_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
                    'runtime_validation': 'NOT_RUN', 'commit_merge_push': 'NOT_PERFORMED',
                    'files': [{'path': p, 'type': 'runtime' if p.startswith('common/') else 'validation_tool',
                               'before_workspace_sha256': baseline.get(p),
                               'after_workspace_sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
                              for p in paths],
                    'excluded': 'Pre-existing changes, MAP reports, borders, histories, populations, recipes, Steam Build'}
        (REPORT / 'PATCH_MANIFEST.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps({'result': 'PASS', 'scenarios': len(data['scenarios']), 'static': data['static'],
                      'runtime_validation': 'NOT_RUN'}, indent=2))
    return data


if __name__ == '__main__':
    run('--write-report' in sys.argv)
