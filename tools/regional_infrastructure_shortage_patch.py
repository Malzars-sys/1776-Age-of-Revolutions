"""Build an isolated patch from parsed recipes; --patch prints for apply_patch.

Only --snapshot writes generated QA evidence. Runtime edits use apply_patch.
No game simulation, forced construction, Git mutation or MAP report updates.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
import validate_diplomacy_ottoman_1776 as script

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/reports/ai_regional_infrastructure_shortage_2026-10-10'
EFFECTS = 'common/scripted_effects/1776_ai_regional_infrastructure_effects.txt'
TRIGGERS = 'common/scripted_triggers/1776_ai_regional_infrastructure_shortage.txt'
VALUES = 'common/script_values/1776_ai_regional_infrastructure_shortage.txt'
GROUPS = {
    'roads': ['pm_paved_road_network', 'pm_engineered_road_network',
              'pm_turnpike_road_network', 'pm_traditional_road_network'],
    # Rank infrastructure, not merely technology: electric principle gives 24,
    # normal diesel 17. Electric/steam principle tie at 14: prefer electricity.
    'rail': ['pm_diesel_trains_principle_transport_3',
             'pm_electric_trains_principle_transport_3', 'pm_diesel_trains',
             'pm_electric_trains', 'pm_steam_trains_principle_transport_3',
             'pm_steam_trains', 'pm_early_trains', 'pm_no_rail_network'],
    'wagons': ['pm_aluminium_passenger_carriages', 'pm_steel_passenger_carriages',
               'pm_wooden_passenger_carriages', 'pm_no_passenger_trains'],
    'canals': ['pm_engineered_canals', 'pm_industrial_canals', 'pm_no_canal_network'],
}
PM_NAMES = {pm for group in GROUPS.values() for pm in group}
SUPPLIERS = {
    'building_logging_camp': ['wood'], 'building_tooling_workshop': ['tools'],
    'building_limestone_quarry': ['limestone'], 'building_cement_works': ['cement'],
    'building_oil_refinery': ['heavy_petroleum_products', 'refined_fuels'],
    'building_coal_mine': ['coal'], 'building_motor_industry': ['engines'],
    'building_power_plant': ['electricity'], 'building_iron_mine': ['iron'],
    'building_steel_mill': ['steel'], 'building_alloys_plant': ['aluminium'],
}


def catalog(folder, root=ROOT):
    result = {}
    for path in sorted((root / folder).glob('*.txt')):
        raw = path.read_text(encoding='utf-8-sig')
        for node in script.parse(raw):
            result[node.key.removeprefix('REPLACE_OR_CREATE:')] = (path, raw, node)
    return result


def inputs(pm):
    return {n.key[len('goods_input_'):-len('_add')]: float(n.value)
            for n in script.walk(pm.children())
            if n.key.startswith('goods_input_') and n.key.endswith('_add')}


def generated():
    pms = catalog('common/production_methods')
    recipes = {pm: inputs(pms[pm][2]) for pm in PM_NAMES}
    goods = sorted({g for recipe in recipes.values() for g in recipe})
    assert set(goods) == {g for gs in SUPPLIERS.values() for g in gs}
    # Conservative reserve: maximum consumption per group, summed over groups.
    # Current demand is not subtracted. This double-counts existing consumption
    # deliberately; partial employment must not make an upgrade appear safe.
    reserves = {g: sum(max(recipes[pm].get(g, 0) for pm in group)
                       for group in GROUPS.values()) for g in goods}
    changes = {}
    triggers = ['# State scope. All automatic intervention is AI-only.',
        'aor1776_ai_regional_infrastructure_shortage = {',
        '\towner = { is_ai = yes }',
        '\tany_scope_building = {',
        '\t\tis_building_type = building_railway',
        '\t\tbuilding_has_goods_shortage = yes', '\t}', '}', '']
    values = ['# MG/SG scope. Saved state is set before candidate selection.',
              '# Reserve includes full employment and all four PM groups.', '']
    demands = []
    for good in goods:
        var = f'aor1776_ai_need_{good}'
        connected = f'aor1776_ai_connected_need_{good}'
        sustainable = f'aor1776_ai_supply_{good}'
        # Electricity is local. All other goods can use a connected market OR
        # sufficient local production. Theoretical import potential alone fails.
        local = (f'\t\tsg:{good} = {{\n'
                 f'\t\t\tstate_goods_production > 0\n'
                 f'\t\t\tstate_goods_production >= aor1776_ai_local_reserve_{good}\n'
                 f'\t\t}}')
        market = (f'\t\tmarket_access >= 0.95\n'
                  f'\t\tis_isolated_from_market = no\n'
                  f'\t\tmarket = {{ mg:{good} = {{\n'
                  f'\t\t\tmarket_goods_has_goods_shortage = no\n'
                  f'\t\t\tmarket_goods_sell_orders > 0\n'
                  f'\t\t\tmarket_goods_sell_orders >= aor1776_ai_market_reserve_{good}\n'
                  f'\t\t}} }}')
        triggers += [f'{sustainable} = {{', f'\tsg:{good} = {{',
                     '\t\tstate_goods_has_local_goods_shortage = no',
                     '\t\tstate_goods_pricier <= 0.25', '\t}']
        if good == 'electricity':
            triggers += [local]
        else:
            triggers += ['\tOR = {', f'\t\tAND = {{\n{market}\n\t\t}}', local, '\t}']
        triggers += ['}', '', f'aor1776_ai_prioritize_{good} = {{',
                     '\towner = { is_ai = yes }', '\tOR = {',
                     f'\t\thas_variable = {var}']
        if good != 'electricity':
            triggers += ['\t\tAND = {', '\t\t\tmarket_access >= 0.95',
                         '\t\t\tis_isolated_from_market = no',
                         f'\t\t\towner = {{ has_variable = {connected} }}', '\t\t}']
        triggers += ['\t}', '}', '']
        for kind, getter in [('local', 'state_goods_consumption'), ('market', 'market_goods_buy_orders')]:
            values += [f'aor1776_ai_{kind}_reserve_{good} = {{', f'\tvalue = {getter}',
                       '\tadd = {', '\t\tvalue = scope:aor1776_ai_regional_state.var:aor1776_ai_regional_levels',
                       f'\t\tmultiply = {reserves[good]:g}', '\t}', '\tmultiply = 0.9', '}', '']
        active = sorted(pm for pm, recipe in recipes.items() if good in recipe)
        demands += ['\tif = {', '\t\tlimit = {',
                    '\t\t\taor1776_ai_regional_infrastructure_shortage = yes', '\t\t\tany_scope_building = {',
                    '\t\t\t\tis_building_type = building_railway', '\t\t\t\tOR = {']
        demands += [f'\t\t\t\t\thas_active_production_method = {pm}' for pm in active]
        demands += ['\t\t\t\t}', '\t\t\t}', f'\t\t\tNOT = {{ {sustainable} = yes }}',
                    '\t\t}', f'\t\tset_variable = {{ name = {var} days = 180 }}']
        if good != 'electricity':
            demands += ['\t\tif = {', '\t\t\tlimit = {', '\t\t\t\tmarket_access >= 0.95',
                        '\t\t\t\tis_isolated_from_market = no',
                        f'\t\t\t\tsg:{good} = {{ state_goods_has_local_goods_shortage = no }}', '\t\t\t}',
                        f'\t\t\towner = {{ set_variable = {{ name = {connected} days = 180 }} }}', '\t\t}']
        demands += ['\t}', '']
    for pm in sorted(PM_NAMES):
        triggers += [f'aor1776_ai_sustainable_{pm} = {{']
        triggers += [f'\taor1776_ai_supply_{g} = yes' for g in sorted(recipes[pm])]
        triggers += ['\tOR = {', '\t\tany_scope_building = {', '\t\t\tis_building_type = building_railway',
                     f'\t\t\thas_active_production_method = {pm}', '\t\t}',
                     '\t\tcan_activate_production_method = {', '\t\t\tbuilding_type = building_railway',
                     f'\t\t\tproduction_method = {pm}', '\t\t}', '\t}', '}', '']
    changes[TRIGGERS] = '\n'.join(triggers)
    changes[VALUES] = '\n'.join(values)
    effect = ['# AI-only sustainable maintenance. No construction, resources or subsidies.',
              '# Generated from recipes by tools/regional_infrastructure_shortage_patch.py.',
              'aor1776_ai_apply_regional_infrastructure_pm = {', '\tif = {',
              '\t\tlimit = { NOT = { any_scope_building = {', '\t\t\tis_building_type = building_railway',
              '\t\t\thas_active_production_method = $PM$', '\t\t} } }',
              '\t\tactivate_production_method = { building_type = building_railway production_method = $PM$ }',
              '\t\tset_variable = { name = aor1776_ai_regional_cooldown days = 180 }', '\t}', '}', '',
              '# Rank all states, avoiding out-of-range positions in small countries.',
              'aor1776_ai_mark_canal_gdp_position = {', '\tif = {', '\t\tlimit = { num_states > $POSITION$ }',
              '\t\tordered_scope_state = {', '\t\t\torder_by = gdp', '\t\t\tposition = $POSITION$',
              '\t\t\tcheck_range_bounds = no', '\t\t\tset_variable = aor1776_ai_top_gdp_canal_state',
              '\t\t}', '\t}', '}', '']
    for group, candidates in GROUPS.items():
        effect += [f'aor1776_ai_choose_regional_{group} = {{']
        for i, pm in enumerate(candidates):
            effect += [f'\t{"if" if i == 0 else "else_if"} = {{',
                       f'\t\tlimit = {{ aor1776_ai_sustainable_{pm} = yes }}',
                       f'\t\taor1776_ai_apply_regional_infrastructure_pm = {{ PM = {pm} }}', '\t}']
        effect += ['}', '']
    effect += ['aor1776_ai_record_regional_supply_needs = {'] + demands + ['}', '',
              'aor1776_ai_select_sustainable_regional_infrastructure = {',
              '\taor1776_ai_choose_regional_roads = yes', '\taor1776_ai_choose_regional_rail = yes',
              '\tif = {', '\t\tlimit = { any_scope_building = {',
              '\t\t\tis_building_type = building_railway', '\t\t\thas_active_production_method = pm_no_rail_network',
              '\t\t} }', '\t\taor1776_ai_apply_regional_infrastructure_pm = { PM = pm_no_passenger_trains }',
              '\t}', '\telse = { aor1776_ai_choose_regional_wagons = yes }',
              '\tif = {', '\t\tlimit = { has_variable = aor1776_ai_top_gdp_canal_state }',
              '\t\taor1776_ai_choose_regional_canals = yes', '\t}',
              '\telse = { aor1776_ai_apply_regional_infrastructure_pm = { PM = pm_no_canal_network } }', '}', '',
              '# Two consecutive observed shortages; not an estimate of engine penalty.',
              '# Healthy upgrades wait 180 days after any actual PM change.',
              'aor1776_ai_refresh_regional_infrastructure = {', '\tif = {',
              '\t\tlimit = { is_ai = yes any_scope_building = { is_building_type = building_railway } }',
              '\t\tevery_scope_state = {', '\t\t\tlimit = { has_variable = aor1776_ai_top_gdp_canal_state }',
              '\t\t\tremove_variable = aor1776_ai_top_gdp_canal_state', '\t\t}']
    effect += [f'\t\taor1776_ai_mark_canal_gdp_position = {{ POSITION = {i} }}' for i in range(10)]
    effect += ['\t\tevery_scope_state = {', '\t\t\tlimit = { has_building = building_railway }',
               '\t\t\tsave_scope_as = aor1776_ai_regional_state',
               '\t\t\tset_variable = { name = aor1776_ai_regional_levels value = b:building_railway.level }',
               '\t\t\taor1776_ai_record_regional_supply_needs = yes', '\t\t\tif = {',
               '\t\t\t\tlimit = { aor1776_ai_regional_infrastructure_shortage = yes }', '\t\t\t\tif = {',
               '\t\t\t\t\tlimit = { has_variable = aor1776_ai_regional_shortage_previous }',
               '\t\t\t\t\taor1776_ai_select_sustainable_regional_infrastructure = yes', '\t\t\t\t}',
               '\t\t\t\tset_variable = { name = aor1776_ai_regional_shortage_previous days = 45 }', '\t\t\t}',
               '\t\t\telse = {', '\t\t\t\tremove_variable = aor1776_ai_regional_shortage_previous',
               '\t\t\t\tif = {', '\t\t\t\t\tlimit = { NOT = { has_variable = aor1776_ai_regional_cooldown } }',
               '\t\t\t\t\taor1776_ai_select_sustainable_regional_infrastructure = yes', '\t\t\t\t}',
               '\t\t\t}', '\t\t}', '\t}', '}', '']
    changes[EFFECTS] = '\n'.join(effect)

    # Change only the selected PMs' static AI weights. No economic recipe edits.
    for pm in PM_NAMES:
        path, raw, node = pms[pm]
        relative = path.relative_to(ROOT).as_posix()
        current = changes.get(relative, raw)
        match = next(n for n in script.parse(current) if n.key.removeprefix('REPLACE_OR_CREATE:') == pm)
        weight = match.children('ai_weight')
        if weight:
            n = weight[0]
            current = current[:n.start] + 'ai_weight = 1' + current[n.end:]
        changes[relative] = current

    # Native construction scores keep their original base and journal bonuses.
    # Multiplication is LAST so those bonuses cannot bypass the shortage guard.
    building_catalog = catalog('common/buildings')
    path, raw, node = building_catalog['building_railway']
    relative = path.relative_to(ROOT).as_posix()
    av = node.children('ai_value')[0]
    guard = '\n\t\tif = {\n\t\t\tlimit = { aor1776_ai_regional_infrastructure_shortage = yes }\n\t\t\tmultiply = 0\n\t\t}\n\t'
    raw = raw[:av.end - 1] + guard + raw[av.end - 1:]
    node = next(n for n in script.parse(raw) if n.key == 'building_railway')
    auto = node.children('should_auto_expand')[0]
    raw = raw[:auto.start] + ('can_build_government = {\n\t\tNOT = { aor1776_ai_regional_infrastructure_shortage = yes }\n\t}\n'
           '\tcan_build_private = {\n\t\tNOT = { aor1776_ai_regional_infrastructure_shortage = yes }\n\t}\n\n\t') + raw[auto.start:]
    node = next(n for n in script.parse(raw) if n.key == 'building_railway')
    auto = node.children('should_auto_expand')[0]
    raw = raw[:auto.start + len('should_auto_expand = {')] + ('\n\t\t# Player automation is unchanged; guard all three AI construction paths.\n'
          '\t\tOR = {\n\t\t\towner = { is_ai = no }\n\t\t\tbuilding_has_goods_shortage = no\n\t\t}') + raw[auto.start + len('should_auto_expand = {'):]
    changes[relative] = raw
    for building, supplied_goods in SUPPLIERS.items():
        path, original, _ = building_catalog[building]
        relative = path.relative_to(ROOT).as_posix()
        raw = changes.get(relative, original)
        node = next(n for n in script.parse(raw) if n.key == building)
        eligibility = '\n'.join(f'\t\t\t\t\taor1776_ai_prioritize_{good} = yes' for good in supplied_goods)
        boost = ('\n\t\t# Native eligibility, costs, resources and AI budgets still apply.\n'
                 '\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tOR = {\n' + eligibility + '\n\t\t\t\t}\n'
                 '\t\t\t\tNOT = { any_scope_building = {\n'
                 f'\t\t\t\t\tis_building_type = {building}\n'
                 '\t\t\t\t\tOR = { is_under_construction = yes building_has_goods_shortage = yes }\n'
                 '\t\t\t\t} }\n\t\t\t}\n\t\t\tmultiply = 4\n\t\t}\n\t')
        avs = node.children('ai_value')
        if avs and isinstance(avs[0].value, list):
            at = avs[0].end - 1
            raw = raw[:at] + boost + raw[at:]
        elif avs:
            av = avs[0]
            raw = raw[:av.start] + 'ai_value = {\n\t\tvalue = ' + str(av.value) + boost + '}' + raw[av.end:]
        else:
            at = node.end - 1
            raw = raw[:at] + '\n\tai_value = {\n\t\tvalue = 1000' + boost + '}\n' + raw[at:]
        changes[relative] = raw
    # Supply requests retained through temporary fallback; native AI decides
    # production/trade. Existing strategy stances are not overwritten.
    return changes, recipes, reserves


def snapshot(extra=False):
    REPORT.mkdir(parents=True, exist_ok=True)
    target = REPORT / ('baseline_other.json' if extra else 'baseline.json')
    assert not target.exists(), 'Baseline already exists; never overwrite initial evidence'
    folders = ('gfx', 'events', 'localization', '.metadata', 'docs/workshop', 'docs/reports/map') if extra else ('common', 'map_data', 'docs/reports/map/MAP1C')
    paths = [p for folder in folders
             for p in (ROOT / folder).rglob('*') if p.is_file()]
    data = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    target.write_text(json.dumps({'files': data}, indent=2), encoding='utf-8')
    print(f'Baseline captured: {len(data)} files')


def emit_patch(changes):
    out = ['*** Begin Patch']
    for relative, new in sorted(changes.items()):
        path = ROOT / relative
        if path.exists():
            old = path.read_text(encoding='utf-8')
            if old.startswith('\ufeff'):
                new = '\ufeff' + new
            if old == new:
                continue
            # Full context avoids ambiguous, structurally identical PM/value
            # blocks being matched to an adjacent definition by apply_patch.
            out += [f'*** Update File: {relative}', '@@']
            out += ['-' + line for line in old.splitlines()]
            out += ['+' + line for line in new.splitlines()]
        else:
            out += [f'*** Add File: {relative}']
            out += ['+' + line for line in new.splitlines()]
    print('\n'.join(out + ['*** End Patch']))


def reserve_patch():
    """Prevent multiple states spending the same market reserve in one pulse."""
    raw = (ROOT / EFFECTS).read_text(encoding='utf-8-sig')
    assert 'aor1776_ai_reserve_regional_demand = {' not in raw, 'Country reserve patch already applied'
    pms = catalog('common/production_methods')
    goods = sorted({g for pm in PM_NAMES for g in inputs(pms[pm][2])})
    reserved = []
    for pm in sorted(PM_NAMES):
        recipe = inputs(pms[pm][2])
        if not recipe:
            continue
        reserved += ['\tif = {', '\t\tlimit = { any_scope_building = {',
                     '\t\t\tis_building_type = building_railway',
                     f'\t\t\thas_active_production_method = {pm}', '\t\t} }', '\t\towner = {']
        for good, cost in sorted(recipe.items()):
            reserved += ['\t\t\tchange_variable = {',
                         f'\t\t\t\tname = aor1776_ai_reserved_{good}', '\t\t\t\tadd = {',
                         '\t\t\t\t\tvalue = scope:aor1776_ai_regional_state.var:aor1776_ai_regional_levels',
                         f'\t\t\t\t\tmultiply = {cost:g}', '\t\t\t\t}', '\t\t\t}']
        reserved += ['\t\t}', '\t}', '']
    raw += ('\n# Country reserve counts full demand of every changed state in this pulse.\n'
            '# Unchanged states are already included in native current buy orders.\n'
            'aor1776_ai_reserve_regional_demand = {\n' + '\n'.join(reserved) + '\n}\n')
    marker = '\t\tevery_scope_state = {\n\t\t\tlimit = { has_variable = aor1776_ai_top_gdp_canal_state }'
    resets = '\n'.join(f'\t\tset_variable = {{ name = aor1776_ai_reserved_{g} value = 0 }}' for g in goods)
    assert marker in raw
    raw = raw.replace(marker, resets + '\n' + marker, 1)
    marker = '\t\t\tsave_scope_as = aor1776_ai_regional_state'
    raw = raw.replace(marker, '\t\t\tremove_variable = aor1776_ai_regional_changed_this_pulse\n' + marker, 1)
    node = next(n for n in script.parse(raw) if n.key == 'aor1776_ai_refresh_regional_infrastructure')
    state_loop = node.children('if')[0].children('every_scope_state')[-1]
    at = state_loop.end - 1
    raw = raw[:at] + ('\tif = {\n\t\t\t\tlimit = { has_variable = aor1776_ai_regional_changed_this_pulse }\n'
                     '\t\t\t\taor1776_ai_reserve_regional_demand = yes\n\t\t\t}\n\t\t') + raw[at:]
    values = (ROOT / VALUES).read_text(encoding='utf-8-sig')
    for node in reversed(script.parse(values)):
        if node.key.startswith('aor1776_ai_market_reserve_'):
            good = node.key.removeprefix('aor1776_ai_market_reserve_')
            at = node.children('multiply')[-1].start
            values = values[:at] + (f'add = scope:aor1776_ai_regional_state.owner.var:aor1776_ai_reserved_{good}\n\t') + values[at:]
    emit_patch({EFFECTS: raw, VALUES: values})


def patch():
    assert 'aor1776_ai_regional_cooldown' not in (ROOT / EFFECTS).read_text(encoding='utf-8-sig'), 'Initial patch already applied'
    changes, _, _ = generated()
    emit_patch(changes)


def reserve_values_patch():
    _, recipes, reserves = generated()
    lines = ['# MG/SG scope. Saved state is set before candidate selection.',
             '# Reserve includes full employment and all four PM groups.', '']
    for good in sorted(reserves):
        for kind, getter in [('local', 'state_goods_consumption'), ('market', 'market_goods_buy_orders')]:
            lines += [f'aor1776_ai_{kind}_reserve_{good} = {{', f'\tvalue = {getter}', '\tadd = {',
                      '\t\tvalue = scope:aor1776_ai_regional_state.var:aor1776_ai_regional_levels',
                      f'\t\tmultiply = {reserves[good]:g}', '\t}']
            if kind == 'market':
                lines += [f'\tadd = scope:aor1776_ai_regional_state.owner.var:aor1776_ai_reserved_{good}']
            lines += ['\tmultiply = 0.9', '}', '']
    emit_patch({VALUES: '\n'.join(lines)})


def supplier_technology_patch():
    """Do not boost a supplier before one of its output PMs is researched."""
    buildings = catalog('common/buildings')
    game = Path('C:/Games/Victoria 3/game')
    groups = {**catalog('common/production_method_groups', game), **catalog('common/production_method_groups')}
    pms = {**catalog('common/production_methods', game), **catalog('common/production_methods')}
    triggers = (ROOT / TRIGGERS).read_text(encoding='utf-8-sig')
    assert 'aor1776_ai_can_produce_tools = {' not in triggers, 'Supplier technology guards already applied'
    changes = {}
    for building, goods in SUPPLIERS.items():
        path, original, node = buildings[building]
        group_names = [script.scalar(n.value) for n in node.children('production_method_groups')[0].children()]
        methods = [script.scalar(n.value) for group in group_names
                   for n in groups[group][2].children('production_methods')[0].children()]
        for good in goods:
            candidates = []
            for pm in methods:
                definition = pms[pm][2]
                produces = any(n.key == f'goods_output_{good}_add' and float(n.value) > 0
                               for n in script.walk(definition.children()))
                if produces:
                    techs = {script.scalar(n.value) for t in definition.children('unlocking_technologies') for n in t.children()}
                    candidates.append(tuple(sorted(techs)))
            assert candidates, (building, good)
            triggers += f'\n# Production PM technology guard for {building}; construction eligibility remains native.\naor1776_ai_can_produce_{good} = {{\n\towner = {{\n\t\tOR = {{\n'
            for techs in sorted(set(candidates)):
                if not techs:
                    triggers += '\t\t\talways = yes\n'
                else:
                    triggers += '\t\t\tAND = {\n'
                    for tech in techs:
                        triggers += f'\t\t\t\thas_technology_researched = {tech}\n'
                    triggers += '\t\t\t}\n'
            triggers += '\t\t}\n\t}\n}\n'
        relative = path.relative_to(ROOT).as_posix()
        raw = changes.get(relative, original)
        for good in goods:
            old = f'aor1776_ai_prioritize_{good} = yes'
            new = f'AND = {{ aor1776_ai_prioritize_{good} = yes aor1776_ai_can_produce_{good} = yes }}'
            assert raw.count(old) == 1, (relative, good)
            raw = raw.replace(old, new)
        changes[relative] = raw
    changes[TRIGGERS] = triggers
    emit_patch(changes)


if __name__ == '__main__':
    if '--validator-entrypoint-patch' in sys.argv:
        emit_patch({'tools/validate_ai_regional_infrastructure_1776.py':
            '"""Compatibility entry point for the current regional infrastructure validator.\n\n'
            'The previous suite assumed unconditional upgrades. Its regression cases\n'
            'are retained in the new shortage-aware, actual-script AST fixture suite.\n'
            'These checks do not execute the Victoria 3 engine.\n"""\n'
            'from validate_regional_infrastructure_shortage import run\n\n\n'
            'def run_tests():\n    return run()\n\n\n'
            "if __name__ == '__main__':\n    run_tests()\n"})
    elif '--snapshot-extra' in sys.argv:
        snapshot(extra=True)
    elif '--snapshot' in sys.argv:
        snapshot()
    elif '--patch' in sys.argv:
        patch()
    elif '--reserve-patch' in sys.argv:
        reserve_patch()
    elif '--reserve-values-patch' in sys.argv:
        reserve_values_patch()
    elif '--supplier-technology-patch' in sys.argv:
        supplier_technology_patch()
    else:
        _, recipes, reserves = generated()
        print(json.dumps({'recipes': recipes, 'reserves': reserves}, indent=2))
