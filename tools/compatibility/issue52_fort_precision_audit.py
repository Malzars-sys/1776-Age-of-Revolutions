"""Read-only four-decimal fort-cost audit; never run the historical report writer."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import validate_land_fortification_construction as legacy
from validate_diplomacy_ottoman_1776 import parse

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE52_FORT_NUMERIC_PRECISION_2026_11_10'
SOURCE = 'common/static_modifiers/1776_land_fortification_construction.txt'
JAPAN = 'common/static_modifiers/1776_japan_famine_choices.txt'
REPLACEMENTS = ((b'-0.181818', b'-0.1818'), (b'-0.307692', b'-0.3077'),
                (b'-0.470588', b'-0.4706'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def candidate(data):
    for old, new in REPLACEMENTS:
        if data.count(old) != 1:
            raise ValueError('Expected exactly one reviewed literal ' + old.decode())
        data = data.replace(old, new, 1)
    return data


def verify(data, japan_data):
    checks = []

    def check(name, passed):
        checks.append({'name': name, 'pass': bool(passed)})

    before = (EVIDENCE / 'before' / SOURCE).read_bytes()
    japan_before = (EVIDENCE / 'before' / JAPAN).read_bytes()
    modifiers = {n.key: n for n in parse(data.decode('utf-8-sig'))}
    previous = {n.key: n for n in parse(before.decode('utf-8-sig'))}
    check('exact_three_literal_patch_preserves_all_other_bytes', data == candidate(before))
    check('same_four_modifier_ids', list(modifiers) == list(previous) and len(modifiers) == 4)
    values = [n.one(legacy.MODTYPE) for n in modifiers.values()]
    check('all_coefficients_negative_at_most_four_decimals',
          all(re.fullmatch(r'-0\.\d{1,4}', value) for value in values))
    check('level_three_coefficient_unchanged', modifiers['aor1776_fort_construction_level_3'].one(legacy.MODTYPE) == '-0.4')
    check('only_existing_exact_group_modifier_type', all({n.key for n in m.children()} ==
          {'icon', legacy.MODTYPE} for m in modifiers.values()))
    check('icons_unchanged', all(modifiers[k].one('icon') == previous[k].one('icon') for k in modifiers))
    check('base_cost_still_900', legacy.DB['cost']['aor1776_land_fortification_construction_cost'].value == '900')
    check('efficiency_group_switch_retained', legacy.DB['group'][legacy.GROUP].one('construction_efficiency_modifier') == 'yes')
    native = (EVIDENCE / 'native/common/static_modifiers/00_code_static_modifiers.txt').read_text(encoding='utf-8-sig')
    check('canonical_static_modifier_four_decimal_witness',
          'state_trade_advantage_from_capacity_add = 0.0005' in native)
    baseline = json.loads((EVIDENCE / 'BASELINE.json').read_text(encoding='utf-8'))
    fort_errors = [row for row in baseline['observed_diagnostics'] if SOURCE in row['text']]
    check('three_observed_rejected_literals_pinned', len(fort_errors) == 3 and
          all(any(old.decode() in row['text'] for row in fort_errors) for old, _ in REPLACEMENTS))
    for index, target in enumerate((1100, 1300, 1500, 1700), 1):
        ideal = Decimal(900) / target - 1
        actual = Decimal(modifiers[f'aor1776_fort_construction_level_{index}'].one(legacy.MODTYPE))
        check(f'nearest_four_place_coefficient_level_{index}',
              actual == ideal.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))
    saved = legacy.DB['modifiers']
    cases = []
    try:
        legacy.DB['modifiers'] = modifiers
        for pm in (1, 2, 3):
            for staffing in (Decimal('0'), Decimal('.25'), Decimal('1')):
                for level, target in enumerate((900, 1100, 1300, 1500, 1700, 1700)):
                    country = legacy.country()
                    state = legacy.state(level, country, pm=pm, staffing=staffing, queued=5-level)
                    projection = legacy.Projection([country])
                    projection.effect(legacy.DB['effects']['aor1776_refresh_fort_construction_state'].children(), state)
                    expected = set() if level == 0 else {f'aor1776_fort_construction_level_{min(level,4)}'}
                    efficiency = 1 + legacy.penalty(state)
                    cost = Decimal(900) / efficiency
                    cases.append({'level_built': level, 'pm': pm, 'staffing': str(staffing),
                                  'tier_selection_correct': state['modifiers'] == expected,
                                  'efficiency': str(efficiency), 'effective_cost': str(cost),
                                  'target': target, 'error': str(cost - target)})
        check('actual_ast_preserves_tier_selection_for_54_cases',
              len(cases) == 54 and all(x['tier_selection_correct'] for x in cases))
        check('neutral_cost_error_below_005_points',
              all(abs(Decimal(x['error'])) < Decimal('.05') for x in cases))
        check('all_efficiencies_above_half', all(Decimal(x['efficiency']) > Decimal('.5') for x in cases))
        neutral = [x for x in cases if x['pm'] == 1 and x['staffing'] == '1' and x['level_built'] <= 4]
        total = sum((Decimal(x['effective_cost']) for x in neutral), Decimal(0))
        check('five_level_total_still_near_6500', abs(total - 6500) < Decimal('.05'))
    finally:
        legacy.DB['modifiers'] = saved
    check('japan_fix_only_adds_utf8_bom', japan_data == b'\xef\xbb\xbf' + japan_before)
    check('japan_modifier_payload_identical', japan_data.decode('utf-8-sig') == japan_before.decode('utf-8-sig'))
    return checks, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(EVIDENCE):
        parser.error('Choose a new evidence output; never overwrite earlier reports')
    base = EVIDENCE / 'candidate' if args.candidate else ROOT
    data, japan = (base / SOURCE).read_bytes(), (base / JAPAN).read_bytes()
    checks, cases = verify(data, japan)
    controls = []
    if args.controls:
        before = (EVIDENCE / 'before' / SOURCE).read_bytes()
        for name, fort_data, japan_data in (
            ('rejected_six_decimal_literals', before, japan),
            ('wrong_neutral_tier_cost', data.replace(b'-0.4', b'-0.3', 1), japan),
            ('changed_japanese_food_security', data, japan.replace(b'0.15', b'0.25', 1))):
            bad, _ = verify(fort_data, japan_data)
            failed = [x['name'] for x in bad if not x['pass']]
            controls.append({'name': name, 'pass': bool(failed), 'detected_by': failed})
    result = {'status': 'PASS_SCOPED_STATIC_ONLY' if all(x['pass'] for x in checks + controls)
              else 'FAIL_STATIC', 'checks': checks, 'controls': controls, 'cases': cases,
              'source_sha256': sha(data), 'japan_sha256': sha(japan), 'engine_tested': False,
              'qualification': 'Four-place literals follow the canonical witness. Neutral-cost Decimal/AST projections do not reproduce native fixed-point arithmetic or callback timing.'}
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'checks': len(checks),
                      'failed': [x['name'] for x in checks if not x['pass']],
                      'controls': controls}), flush=True)
    return 0 if result['status'] == 'PASS_SCOPED_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
