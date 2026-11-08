"""Read-only contracts for three artillery materials at two production tiers."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import audit_starting_tech_1776 as core
from validate_diplomacy_ottoman_1776 import walk

EVIDENCE = ROOT / 'docs/reports/economy/ARTILLERY_MATERIAL_PATHS_2026_11_08'
TIERS = [
    [('pm_cannons', 'iron', 15, 10, 25),
     ('pm_bronze_cannons', 'copper', 10, 15, 25),
     ('pm_aor1776_bronze_artillery', 'alloys', 4, 10, 30)],
    [('pm_smoothbores', 'iron', 20, 15, 45),
     ('pm_bronze_smoothbores', 'copper', 20, 20, 45),
     ('pm_aor1776_bronze_smoothbores', 'alloys', 7, 15, 55)],
]


def recipe(node):
    return {n.key: n.value for n in walk(node.children())
            if n.key.startswith('goods_') or n.key.startswith('building_employment_')}


def material_contract(rows):
    for tier in TIERS:
        employment = []
        for key, metal, amount, wood, output in tier:
            r = rows[key]
            assert r['goods_input_' + metal + '_add'] == str(amount), key
            assert r['goods_input_hardwood_add'] == str(wood), key
            assert r['goods_output_artillery_add'] == str(output), key
            for other in {'iron', 'copper', 'alloys'} - {metal}:
                assert 'goods_input_' + other + '_add' not in r, (key, 'mixed metals')
            employment.append(sum(float(v) for k, v in r.items()
                                  if k.startswith('building_employment_')))
        assert employment[0] == employment[1] == employment[2] == 5000
        assert tier[2][2] < min(tier[0][2], tier[1][2])
        assert tier[2][4] > max(tier[0][4], tier[1][4])
        assert tier[2][2] / tier[2][4] < min(tier[0][2] / tier[0][4], tier[1][2] / tier[1][4])


def main(output=None):
    pms, _, _ = core.objects('common/production_methods')
    groups, _, _ = core.objects('common/production_method_groups')
    techs, _, _ = core.objects('common/technology/technologies')
    goods, _, _ = core.objects('common/goods')
    rows = {key: recipe(node) for key, node in pms.items()}
    material_contract(rows)
    before = json.loads((EVIDENCE / 'BEFORE_RECIPES.json').read_text(encoding='utf-8'))
    intended_recipe_changes = {'pm_aor1776_bronze_artillery', 'pm_smoothbores'}
    changed = {key for key, old in before.items() if rows.get(key) != old}
    assert changed == intended_recipe_changes, changed
    assert set(rows) - set(before) == {'pm_aor1776_bronze_smoothbores'}
    foundries = core.values(groups['pmg_foundries'], 'production_methods')
    assert len(foundries) == len(set(foundries))
    for tier in TIERS:
        for key, *_ in tier:
            assert foundries.count(key) == 1
            for tech in core.values(pms[key], 'unlocking_technologies'):
                assert tech in techs and core.val(techs[tech], 'can_research') != 'no', (key, tech)
    assert set(core.values(pms['pm_aor1776_bronze_smoothbores'], 'unlocking_technologies')) == {'shell_gun', 'alloysworking'}
    # Known mod names must resolve once per language, including intentional
    # native overrides; labels must distinguish all six material choices.
    for lang in ('french', 'english'):
        texts = [p.read_text(encoding='utf-8-sig') for p in (ROOT / 'localization' / lang).rglob('*.yml')]
        labels = []
        for tier in TIERS:
            for key, *_ in tier:
                matches = [line for raw in texts for line in raw.splitlines()
                           if line.lstrip().startswith(key + ':')]
                assert len(matches) == 1, (lang, key, len(matches))
                labels.append(matches[0].split('"', 2)[1])
        assert len(set(labels)) == 6
    baseline = json.loads((EVIDENCE / 'BASELINE.json').read_text(encoding='utf-8'))
    allowed_files = {'common/production_methods/01_industry.txt',
                     'common/production_methods/1776_alloys_utensils.txt',
                     'common/production_methods/1776_v115_bronze_artillery.txt',
                     'common/production_method_groups/01_industry.txt',
                     'common/production_methods/13_tech6c5b_copper_production_and_consumers.txt'}
    concurrent = [key for key, sha in baseline['files'].items() if key not in allowed_files and
                  (not (ROOT / key).exists() or hashlib.sha256((ROOT / key).read_bytes()).hexdigest() != sha)]
    negative_controls = []
    for name, key, field, value in [
        ('alloy_output_advantage_removed', 'pm_aor1776_bronze_artillery', 'goods_output_artillery_add', '25'),
        ('alloy_quantity_not_lower', 'pm_aor1776_bronze_smoothbores', 'goods_input_alloys_add', '20'),
        ('iron_still_requires_alloy', 'pm_smoothbores', 'goods_input_alloys_add', '5'),
        ('native_copper_quantity_changed', 'pm_bronze_cannons', 'goods_input_copper_add', '11'),
    ]:
        mutated = {k: dict(v) for k, v in rows.items()}
        mutated[key][field] = value
        try:
            material_contract(mutated)
        except AssertionError:
            negative_controls.append(name)
        else:
            raise AssertionError('Undetected negative control: ' + name)
    materials = []
    for index, tier in enumerate(TIERS, 1):
        for key, metal, amount, wood, out in tier:
            prices = {g: float(core.val(goods[g], 'cost')) for g in (metal, 'hardwood', 'artillery')}
            materials.append({'tier': index, 'PM': key, 'input': {metal: amount, 'hardwood': wood},
                              'artillery': out, 'employment': 5000,
                              'metal_per_artillery': amount / out,
                              'base_price_input_value': amount * prices[metal] + wood * prices['hardwood'],
                              'base_price_output_value': out * prices['artillery'],
                              'base_price_flow_surplus_before_wages_and_other_costs': out * prices['artillery'] - amount * prices[metal] - wood * prices['hardwood']})
    alloy_consumers = [key for key, r in rows.items() if 'goods_input_alloys_add' in r]
    result = {'status': 'PASS_STATIC_ONLY', 'runtime_tested': False,
              'three_material_routes_at_two_tiers': materials,
              'changed_existing_recipes': sorted(changed),
              'unchanged_existing_recipes': len(before) - len(changed),
              'alloy_consumers_reviewed': sorted(alloy_consumers),
              'negative_controls_rejected': negative_controls,
              'protected_files': len(baseline['files']) - len(allowed_files),
              'concurrent_changes_preserved': concurrent,
              'limits': 'Full staffing, no other modifiers. Flow values use local definition prices, '
                        'not observed market prices or whole-building profit. Copper price collision 40/50 remains outside scope.'}
    if output:
        path = Path(output)
        assert not path.exists()
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'alloy_consumers_reviewed'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    main(parser.parse_args().output)
