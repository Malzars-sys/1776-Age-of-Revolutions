"""Prepare bounded #48/#49 candidates and preimages; never install them."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

EVIDENCE = Path(__file__).resolve().parent
GAME = Path('C:/Games/Victoria 3/game')
EVENT = 'events/phase1_japan_tenpo_events.txt'
MODIFIERS = 'common/static_modifiers/1776_japan_famine_choices.txt'
PORTS = 'common/history/buildings/1776_british_guatemala_mosquito_ports.txt'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def treasury(fraction):
    return f'add_treasury = {{ value = root.gdp multiply = -{fraction} }}'


def ig(key, positive=True, days=1825):
    return (f'ig:ig_{key} ?= {{ add_modifier = {{ name = aor1776_japan_ig_'
            f'{"support" if positive else "opposition"} days = {days} }} }}')


def mod(name, days=None):
    return f'add_modifier = {{ name = aor1776_japan_{name}' + (f' days = {days}' if days else '') + ' }'


def states(name, days=None):
    return 'every_scope_state = { ' + mod(name, days) + ' }'


def pop(loyal=True, value='small_radicals', peasants=False):
    return (f'add_{"loyalists" if loyal else "radicals"} = {{ value = {value} '
            + ('pop_type = peasants' if peasants else 'strata = lower') + ' }')


def procurement(days):
    # Abstract standing reserves, not a physical inventory of immortal grain.
    return [f'set_variable = {{ name = aor1776_japan_grain_procurement_active days = {days} }}',
            'set_variable = aor1776_japan_grain_reserves',
            'every_scope_state = {',
            '  limit = { any_scope_building = { OR = {',
            '    is_building_type = building_rice_farm',
            '    is_building_type = building_wheat_farm',
            '    is_building_type = building_rye_farm',
            '    is_building_type = building_maize_farm',
            '    is_building_type = building_millet_farm',
            '    is_building_group = bg_subsistence_agriculture',
            '  } } }',
            '  ' + mod('grain_procurement', days),
            '}']


def option(key, effects, default=False, trigger=None):
    body = ['option = {', f'\tname = {key}']
    if default:
        body.append('\tdefault_option = yes')
    if trigger:
        body.append('\ttrigger = { ' + trigger + ' }')
    body.extend('\t' + line for line in effects)
    body.append('}')
    return '\n\t'.join(body)


def prepare():
    if (EVIDENCE / 'BASELINE.json').exists():
        raise SystemExit('Baseline already exists; do not overwrite evidence')
    protected = {}
    for folder in ('common', 'events', 'localization', 'map_data', 'gui'):
        for p in (ROOT / folder).rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.txt', '.yml', '.gui', '.csv', '.json'):
                with p.open('rb') as stream:
                    protected[p.relative_to(ROOT).as_posix()] = hashlib.file_digest(stream, 'sha256').hexdigest()
    baseline = {'time_utc': datetime.now(timezone.utc).isoformat(), 'sources': protected,
                'native_sources': {}, 'git_metadata': {}, 'engine_tested': False}
    for rel in ('common/modifier_type_definitions/00_modifier_types.txt',
                'common/modifier_type_definitions/modifier_types.md',
                'common/static_modifiers/00_ip4_04_modifiers.txt',
                'localization/french/concepts_l_french.yml'):
        data = (GAME / rel).read_bytes()
        baseline['native_sources'][rel] = sha(data)
        new(EVIDENCE / 'native' / rel, data)
    for rel in ('.git/HEAD', '.git/index'):
        if (ROOT / rel).is_file():
            baseline['git_metadata'][rel] = sha((ROOT / rel).read_bytes())

    choices = {
        '1.a': [treasury('0.005'), 'custom_tooltip = aor1776_japan_granary_policy_tt',
                *procurement(730), states('granary_network'), pop(False, peasants=True),
                ig('rural_folk', False), ig('landowners')],
        '1.b': [treasury('0.003'), states('village_relief', 1095), pop(), ig('rural_folk', days=1095)],
        '1.c': [mod('government_inaction', 1825), ig('landowners'), pop(False)],
        '2.a': [mod('kansei_discipline', 1825), ig('intelligentsia', False), pop(False, peasants=True)],
        '2.b': [treasury('0.002'), mod('relief_administration', 1825),
                states('harvest_watch', 1825), ig('rural_folk')],
        '2.c': [mod('domain_autonomy', 1825), ig('landowners')],
        '3.a': [treasury('0.002'), mod('coastal_vigilance', 1825),
                ig('armed_forces'), ig('industrialists', False)],
        '3.b': [treasury('0.001'), mod('cautious_diplomacy', 1825), ig('industrialists')],
        '3.c': [mod('government_inaction', 1095), ig('armed_forces', False, 1095)],
        '4.a': [treasury('0.001'), mod('relief_administration', 1095),
                states('harvest_watch', 1095), ig('rural_folk', days=1095)],
        '4.b': ['custom_tooltip = aor1776_japan_domain_stocks_tt', *procurement(365),
                states('village_relief', 1095), ig('landowners', False, 1095),
                pop(False, peasants=True)],
        '5.a': ['custom_tooltip = aor1776_japan_release_tt',
                'remove_variable = aor1776_japan_grain_reserves',
                states('emergency_distribution', 365), pop(), ig('rural_folk', days=1095)],
        '5.b': [treasury('0.002'), states('requisitioned_grain', 365),
                ig('industrialists', False, 1095), ig('landowners', False, 1095),
                ig('rural_folk', days=1095)],
        '5.c': [mod('government_inaction', 1095), states('unrelieved_shortages', 730),
                ig('landowners', days=1095), pop(False)],
    }
    before = (ROOT / EVENT).read_bytes()
    raw = before.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in raw else '\n'
    edits = []
    for event in parse(raw):
        for old in event.children('option'):
            name = old.one('name')
            suffix = name.removeprefix('phase1_japan_tenpo.') if isinstance(name, str) else ''
            if suffix not in choices:
                continue
            trigger = ('custom_tooltip = { text = aor1776_japan_reserves_ready_tt '
                       'has_variable = aor1776_japan_grain_reserves '
                       'NOT = { has_variable = aor1776_japan_grain_procurement_active } }') if suffix == '5.a' else None
            default = suffix in ('1.a', '2.a', '3.a', '4.a', '5.b')
            replacement = option(name, choices[suffix], default, trigger).replace('\n', newline)
            edits.append((old.start, old.end, replacement))
    assert len(edits) == 14
    after = raw
    for start, end, replacement in sorted(edits, reverse=True):
        after = after[:start] + replacement + after[end:]
    candidates = {EVENT: (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + after.encode()}

    # Two explicit levels in the existing territorial allocations; no new TAG.
    candidates[PORTS] = b'''# Player-requested 1776 market links; borders and country histories are unchanged.
BUILDINGS = {
 s:STATE_GUATEMALA = { region_state:GBR = {
  create_building = {
   building = building_port
   level = 1
   reserves = 1
   activate_production_methods = { pm_basic_port pm_1776_no_raw_data_reporting }
  }
 } }
 s:STATE_NICARAGUA = { region_state:MKT = {
  create_building = {
   building = building_port
   level = 1
   reserves = 1
   activate_production_methods = { pm_aor1776_traditional_commercial_harbor pm_1776_no_raw_data_reporting }
  }
 } }
}
'''
    definitions = {
        'granary_network': ('documents_positive', {'state_food_security_add': '0.15'}),
        'grain_procurement': ('coins_negative', {'state_sell_orders_grain_add': '-10'}),
        'emergency_distribution': ('coins_positive', {'state_sell_orders_grain_add': '10'}),
        'requisitioned_grain': ('coins_positive', {'state_sell_orders_grain_add': '5'}),
        'village_relief': ('documents_positive', {'state_food_security_add': '0.10'}),
        'harvest_watch': ('documents_positive', {'state_food_security_add': '0.05'}),
        'unrelieved_shortages': ('coins_negative', {'state_food_security_add': '-0.05'}),
        'relief_administration': ('documents_negative', {'country_bureaucracy_mult': '-0.05'}),
        'kansei_discipline': ('flag_positive', {'country_authority_mult': '0.10', 'country_legitimacy_base_add': '5'}),
        'domain_autonomy': ('documents_negative', {'country_authority_mult': '-0.10', 'country_bureaucracy_mult': '0.05'}),
        'coastal_vigilance': ('rifle_positive', {'battle_defense_owned_province_mult': '0.05', 'country_influence_mult': '-0.10'}),
        'cautious_diplomacy': ('flag_positive', {'country_influence_mult': '0.10', 'country_authority_mult': '-0.05'}),
        'government_inaction': ('flag_negative', {'country_legitimacy_base_add': '-5'}),
        'ig_support': ('flag_positive', {'interest_group_approval_add': '2'}),
        'ig_opposition': ('flag_negative', {'interest_group_approval_add': '-2'}),
    }
    blocks = []
    for name, (icon, values) in definitions.items():
        blocks.append('aor1776_japan_' + name + ' = {\n'
                      + f' icon = gfx/interface/icons/timed_modifier_icons/modifier_{icon}.dds\n'
                      + ''.join(f' {key} = {value}\n' for key, value in values.items()) + '}\n')
    candidates[MODIFIERS] = ('# Costs and benefits of the authored Tenmei-Tenpo lead-in.\n' + '\n'.join(blocks)).encode()

    labels = {
        'granary_network': ('Réseau de greniers de réserve', 'Reserve granary network'),
        'grain_procurement': ('Constitution des réserves de grain', 'Building grain reserves'),
        'emergency_distribution': ('Distribution des réserves de grain', 'Emergency grain distribution'),
        'requisitioned_grain': ('Grain accaparé réquisitionné', 'Requisitioned grain hoards'),
        'village_relief': ('Secours alimentaire aux villages', 'Village food relief'),
        'harvest_watch': ('Surveillance des greniers', 'Granary supervision'),
        'unrelieved_shortages': ('Pénuries laissées sans secours', 'Unrelieved food shortages'),
        'relief_administration': ('Administration des secours ruraux', 'Rural relief administration'),
        'kansei_discipline': ('Discipline des réformes Kansei', 'Kansei reform discipline'),
        'domain_autonomy': ('Autonomie des domaines', 'Domain autonomy'),
        'coastal_vigilance': ('Vigilance des défenses côtières', 'Coastal defence vigilance'),
        'cautious_diplomacy': ('Prudence envers les navires étrangers', 'Cautious foreign-ship policy'),
        'government_inaction': ('Autorité du Bakufu contestée', 'Contested Bakufu authority'),
        'ig_support': ('Politique approuvée', 'Policy supported'),
        'ig_opposition': ('Politique contestée', 'Policy opposed'),
        'granary_policy_tt': ('Les achats de réserve retirent temporairement du grain du marché et peuvent en renchérir le prix. Chaque État actuel reçoit un réseau de greniers permanent, donnant +15 points de sécurité alimentaire. Ce bonus protège contre la faim sans modifier le temps ni garantir le prix des aliments.', 'Reserve purchases temporarily withdraw grain from the market and can raise its price. Every currently owned state receives a permanent granary network, granting +15 percentage points of food security. This buffers hunger without changing the weather or fixing food prices.'),
        'domain_stocks_tt': ('Les domaines doivent retirer du grain du marché pendant un an pour constituer leurs réserves. Ces réserves ne pourront être ouvertes qu’une fois les achats terminés.', 'The domains must withdraw grain from the market for one year to establish reserves. They can only be released after procurement is complete.'),
        'reserves_ready_tt': ('Des réserves de grain ont été constituées et leurs achats sont terminés.', 'Grain reserves have been established and procurement is complete.'),
        'release_tt': ('Le grain réservé est remis en vente pendant un an. Cette distribution épuise les réserves mobilisables ; les greniers durables, s’ils ont été construits, restent en place.', 'Reserved grain is released onto the market for one year. This uses up the available emergency reserves; any permanent granary network remains in place.'),
    }
    replacements = {
        'french': {'phase1_japan_tenpo.1.a': 'Constituer des réserves de grain.',
                   'phase1_japan_tenpo.1.b': 'Financer le secours aux villages les plus touchés.',
                   'phase1_japan_tenpo.4.b': 'Imposer des réserves de grain aux domaines.',
                   'phase1_japan_tenpo.5.b': 'Réquisitionner les stocks de grain accaparés.'},
        'english': {'phase1_japan_tenpo.1.a': 'Establish grain reserves.',
                    'phase1_japan_tenpo.1.b': 'Fund relief for the hardest-hit villages.',
                    'phase1_japan_tenpo.4.b': 'Require the domains to establish grain reserves.',
                    'phase1_japan_tenpo.5.b': 'Requisition hoarded grain.'},
    }
    for index, lang in enumerate(('french', 'english')):
        rel = f'localization/{lang}/1776_japan_famine_choices_l_{lang}.yml'
        content = f'l_{lang}:\n' + ''.join(f' aor1776_japan_{key}:0 "{texts[index]}"\n' for key, texts in labels.items())
        candidates[rel] = content.encode('utf-8-sig')
        rel = f'localization/{lang}/phase1_japan_tenpo_l_{lang}.yml'
        original = (ROOT / rel).read_bytes()
        lines = original.decode('utf-8-sig').splitlines(keepends=True)
        used = set()
        for i, line in enumerate(lines):
            key = line.strip().partition(':')[0]
            if key in replacements[lang]:
                tail = '\r\n' if line.endswith('\r\n') else '\n'
                prefix = line[:line.index('"') + 1]
                lines[i] = prefix + replacements[lang][key] + '"' + tail
                used.add(key)
        assert used == set(replacements[lang])
        candidates[rel] = ''.join(lines).encode('utf-8-sig')

    manifest = {}
    for rel, data in candidates.items():
        p = ROOT / rel
        if p.exists():
            before = p.read_bytes()
            assert sha(before) == protected[rel]
            new(EVIDENCE / 'before' / rel, before)
        else:
            before = b''
        if p.suffix == '.txt':
            parse(data.decode('utf-8-sig'))
        new(EVIDENCE / 'candidate' / rel, data)
        diff = ''.join(difflib.unified_diff(before.decode('utf-8-sig').splitlines(True),
                                          data.decode('utf-8-sig').splitlines(True),
                                          fromfile='before/' + rel, tofile='candidate/' + rel))
        new(EVIDENCE / 'diff' / (rel.replace('/', '__') + '.patch'), diff.encode())
        manifest[rel] = {'before_sha256': sha(before) if p.exists() else None,
                         'after_sha256': sha(data), 'bytes': len(data)}
    new(EVIDENCE / 'BASELINE.json', (json.dumps(baseline, indent=2) + '\n').encode())
    new(EVIDENCE / 'CANDIDATE_MANIFEST.json', (json.dumps(manifest, indent=2) + '\n').encode())
    new(EVIDENCE / 'CHOICES.json', (json.dumps(choices, indent=2) + '\n').encode())
    print(json.dumps({'protected_sources': len(protected), 'candidate_files': len(candidates),
                      'options_replaced': len(edits), 'modifiers': len(definitions)}), flush=True)


if __name__ == '__main__':
    prepare()
