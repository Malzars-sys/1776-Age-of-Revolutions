"""Read-only #48/#49 source, dependency and policy checks; one new JSON output."""
from collections import Counter
import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from issue24_map_dlc_audit import ROOT, GAME, Audit, parse, walk, plain

EVIDENCE = ROOT / 'docs/reports/compatibility/PLAYER_ACCEPTANCE_AND_FOLLOWUP_2026_11_10'
EVENT = 'events/phase1_japan_tenpo_events.txt'
MODIFIERS = 'common/static_modifiers/1776_japan_famine_choices.txt'
PORTS = 'common/history/buildings/1776_british_guatemala_mosquito_ports.txt'


def signature(node):
    return (node.key, node.op, tuple(signature(n) for n in node.children())
            if isinstance(node.value, list) else node.value)


def run(candidate=False, mutation=None):
    manifest = json.loads((EVIDENCE / 'CANDIDATE_MANIFEST.json').read_text(encoding='utf-8'))
    data = {rel: ((EVIDENCE / 'candidate' / rel) if candidate else ROOT / rel).read_bytes()
            for rel in manifest}
    if mutation:
        mutation(data)
    checks = []
    findings = []

    def check(name, passed, detail=None):
        checks.append({'name': name, 'pass': bool(passed), 'detail': detail})

    audit = Audit(ROOT, GAME)
    pool = audit.load('modifiers', 'common/static_modifiers')
    for key in list(pool):
        pool[key] = [row for row in pool[key] if row[1] != 'mod/' + MODIFIERS]
        if not pool[key]:
            del pool[key]
    modifiers = parse(data[MODIFIERS].decode('utf-8-sig'))
    for n in modifiers:
        pool.setdefault(n.key, []).append((n, 'candidate/' + MODIFIERS, ''))
    types = audit.load('modifier_types', 'common/modifier_type_definitions')
    check('all_new_modifier_ids_unique', all(len(pool[n.key]) == 1 for n in modifiers))
    check('all_modifier_fields_native_defined', all(c.key in types for n in modifiers
                                                  for c in n.children() if c.key != 'icon'))
    check('all_modifier_icons_resolve', all((ROOT / plain(n.one('icon'))).is_file() or
                                           (GAME / plain(n.one('icon'))).is_file() for n in modifiers))
    raw = data[EVENT].decode('utf-8-sig')
    old_raw = (EVIDENCE / 'before' / EVENT).read_bytes().decode('utf-8-sig')
    events, old = parse(raw), parse(old_raw)
    check('six_event_ids_and_order_retained', [n.key for n in events] == [n.key for n in old])
    check('non_option_content_unchanged',
          [[signature(x) for x in n.children() if x.key != 'option'] for n in events] ==
          [[signature(x) for x in n.children() if x.key != 'option'] for n in old])
    bridge, old_bridge = events[-1], old[-1]
    check('dlc_tenpo_journal_bridge_byte_identical',
          raw[bridge.start:bridge.end] == old_raw[old_bridge.start:old_bridge.end])
    options = [opt for n in events if n.key.startswith('phase1_japan_tenpo.')
               and n.key != 'phase1_japan_tenpo.6' for opt in n.children('option')]
    check('fourteen_choices_with_real_non_population_effects', len(options) == 14 and
          all(any(n.key in ('add_modifier', 'add_treasury') for n in walk([o])) for o in options))
    refs = [(plain(n.one('name'))) for n in walk(events) if n.key == 'add_modifier']
    check('new_event_modifier_references_resolve', all(k in pool and len(pool[k]) == 1 for k in refs))
    costs = [n for n in walk(events) if n.key == 'add_treasury']
    check('treasury_costs_scale_to_country_gdp_and_are_negative', len(costs) > 0 and
          all(plain(n.one('value')) == 'root.gdp' and -0.005 <= float(n.one('multiply')) < 0 for n in costs))
    network = next(n for n in modifiers if n.key == 'aor1776_japan_granary_network')
    check('permanent_food_security_bonus_is_fifteen_points', plain(network.one('state_food_security_add')) == '0.15')
    first = options[0]
    applications = [n for n in walk([first]) if n.key == 'add_modifier'
                    and plain(n.one('name')) == network.key]
    check('network_applied_without_expiration', len(applications) == 1 and
          [n.key for n in applications[0].children()] == ['name'])
    check('first_choice_has_peasant_anger_and_both_ig_sides',
          any(n.key == 'add_radicals' and plain(n.one('pop_type')) == 'peasants' for n in walk([first]))
          and any(n.key == 'ig:ig_rural_folk' and any(plain(x.one('name')) == 'aor1776_japan_ig_opposition'
                  for x in n.children('add_modifier')) for n in first.children())
          and any(n.key == 'ig:ig_landowners' and any(plain(x.one('name')) == 'aor1776_japan_ig_support'
                  for x in n.children('add_modifier')) for n in first.children()))
    by_id = {n.key: n for n in modifiers}
    check('procurement_withdraws_grain_release_adds_it',
          float(by_id['aor1776_japan_grain_procurement'].one('state_sell_orders_grain_add')) == -10
          and float(by_id['aor1776_japan_emergency_distribution'].one('state_sell_orders_grain_add')) == 10)
    release = next(o for o in options if plain(o.one('name')) == 'phase1_japan_tenpo.5.a')
    gate = release.children('trigger')[0]
    check('release_requires_established_and_mature_reserves',
          any(n.key == 'has_variable' and plain(n.value) == 'aor1776_japan_grain_reserves' for n in walk([gate]))
          and any(n.key == 'NOT' and plain(n.one('has_variable')) == 'aor1776_japan_grain_procurement_active'
                  for n in walk([gate])))
    check('release_consumes_available_reserves_flag',
          plain(release.one('remove_variable')) == 'aor1776_japan_grain_reserves')
    check('no_script_changes_to_weather_or_harvest_definitions',
          not any(n.key in ('add_harvest_condition', 'remove_harvest_condition') for n in walk(events)))

    new_keys = {n.key for n in modifiers}
    new_keys.update(plain(n.value) for n in walk(events) if n.key == 'custom_tooltip' and isinstance(n.value, str))
    new_keys.update(plain(n.one('text')) for n in walk(events)
                    if n.key == 'custom_tooltip' and isinstance(n.value, list))
    for lang in ('french', 'english'):
        all_keys = Counter()
        for p in (ROOT / f'localization/{lang}').rglob('*.yml'):
            rel = p.relative_to(ROOT).as_posix()
            contents = data.get(rel, p.read_bytes()).decode('utf-8-sig')
            all_keys.update(re.findall(r'^\s*([^\s:#]+):(?:\d+)?\s*"', contents, re.M))
        for rel, contents in data.items():
            if rel.startswith(f'localization/{lang}/') and not (ROOT / rel).exists():
                all_keys.update(re.findall(r'^\s*([^\s:#]+):(?:\d+)?\s*"', contents.decode('utf-8-sig'), re.M))
        check(f'{lang}_all_new_player_keys_unique_and_defined', all(all_keys[k] == 1 for k in new_keys))
        for rel, contents in data.items():
            if rel.startswith(f'localization/{lang}/'):
                check(f'utf8_bom_and_header_{rel}', contents.startswith(b'\xef\xbb\xbf') and
                      contents.decode('utf-8-sig').startswith(f'l_{lang}:'))

    ports = parse(data[PORTS].decode('utf-8-sig'))[0]
    assignments = [(s.key, part.key, n) for s in ports.children()
                   for part in s.children() for n in part.children('create_building')]
    check('exact_two_requested_starting_ports',
          [(s, c, plain(n.one('building')), plain(n.one('level'))) for s, c, n in assignments] ==
          [('s:STATE_GUATEMALA', 'region_state:GBR', 'building_port', '1'),
           ('s:STATE_NICARAGUA', 'region_state:MKT', 'building_port', '1')])
    methods = audit.load('methods', 'common/production_methods')
    port_methods = [plain(x.value) for _, _, n in assignments
                    for b in n.children('activate_production_methods') for x in b.children()]
    check('port_methods_unique_and_available', all(len(methods.get(k, [])) == 1 for k in port_methods))
    check('no_new_runtime_parse_errors', not audit.errors and all(parse(contents.decode('utf-8-sig'))
          for rel, contents in data.items() if rel.endswith('.txt')))
    return {'status': 'PASS_SCOPED_STATIC_ONLY' if all(c['pass'] for c in checks) else 'FAIL_STATIC',
            'checks': checks, 'modifier_references': refs, 'new_player_keys': sorted(new_keys),
            'engine_tested': False, 'candidate': candidate, 'findings': findings}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    path = args.output.resolve()
    if path.exists() or not path.is_relative_to(EVIDENCE):
        p.error('Use a new path inside this mission evidence directory')
    result = run(args.candidate)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'checks': len(result['checks']),
                      'failures': [x for x in result['checks'] if not x['pass']]}), flush=True)
    return 0 if result['status'] == 'PASS_SCOPED_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
