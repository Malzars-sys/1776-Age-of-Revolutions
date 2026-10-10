"""Read-only structural audit and regression checks for the 1776 diplomacy lot.

No game files, saves or previous reports are written. --audit prints inventories;
the default checks the implementation against the pre-intervention Git revision.
This is a static validator, not a substitute for Victoria 3 runtime testing.
"""
from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
import copy
import itertools
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
BASE = 'a62be0b'
EGYPT = {'STATE_LOWER_EGYPT', 'STATE_MIDDLE_EGYPT', 'STATE_UPPER_EGYPT', 'STATE_MATRUH', 'STATE_SINAI'}
LEVANT = {'STATE_ALEPPO', 'STATE_SYRIA', 'STATE_LEBANON', 'STATE_PALESTINE', 'STATE_TRANSJORDAN'}
ADMIN_CUTS = {
    'STATE_EASTERN_THRACE': ('common/history/buildings/01_south_europe.txt', 30, 26),
    'STATE_ANKARA': ('common/history/buildings/08_middle_east.txt', 23, 19),
    'STATE_SYRIA': ('common/history/buildings/08_middle_east.txt', 11, 9),
}
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[?<>!=]+|[^\s{}?<>!=#]+')


@dataclass
class Node:
    key: str
    op: str
    value: str | list
    start: int
    end: int

    def children(self, key=None):
        return [n for n in self.value if key is None or n.key == key] if isinstance(self.value, list) else []

    def one(self, key, default=None):
        found = self.children(key)
        return found[0].value if found else default


def parse(raw):
    tokens = [(m.group(), m.start(), m.end()) for m in TOKEN.finditer(raw) if not m.group().startswith('#')]
    i = 0

    def group(nested=False):
        nonlocal i
        result = []
        while i < len(tokens):
            word, start, end = tokens[i]
            if word == '}':
                if not nested:
                    raise ValueError(f'Unexpected closing brace at {start}')
                i += 1
                return result, end
            if word == '{':
                i += 1
                value, end = group(True)
                result.append(Node('', '', value, start, end))
                continue
            i += 1
            if i < len(tokens) and tokens[i][0] in ('=', '?=', '<', '>', '<=', '>=', '!='):
                op = tokens[i][0]
                i += 1
                if i >= len(tokens):
                    raise ValueError(f'Missing value for {word}')
                value, _, end = tokens[i]
                i += 1
                if value == '{':
                    value, end = group(True)
                elif i < len(tokens) and tokens[i][0] == '{' and value in ('rgb', 'hsv', 'hsv360'):
                    i += 1
                    value, end = group(True)
                result.append(Node(word.strip('"'), op, value, start, end))
            else:
                result.append(Node('', '', word, start, end))
        if nested:
            raise ValueError('Unclosed brace')
        return result, len(raw)

    return group()[0]


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.children())


def read(path, base=False):
    path = Path(path)
    if base:
        return subprocess.check_output(['git', 'show', f'{BASE}:{path.as_posix()}'], cwd=ROOT).decode('utf-8-sig')
    return (ROOT / path).read_text(encoding='utf-8-sig')


def scalar(v):
    return str(v).strip('"')


def normalized(nodes, normalize_owner=False):
    result = []
    for n in nodes:
        key = n.key
        if key == 'state_type':
            continue
        if normalize_owner:
            key = key.replace('region_state:EGY', 'region_state:TUR')
        value = normalized(n.value, normalize_owner) if isinstance(n.value, list) else scalar(n.value)
        if normalize_owner and value == 'c:EGY':
            value = 'c:TUR'
        result.append((key, n.op, value))
    return result


def admin_ownership(nodes):
    """Government-owned starting levels, not the number of create_building blocks."""
    result = {}
    for state in walk(nodes):
        if not state.key.startswith('s:'):
            continue
        for region in state.children('region_state:TUR'):
            for building in region.children('create_building'):
                if scalar(building.one('building')) != 'building_government_administration':
                    continue
                for ownership in building.children('add_ownership'):
                    for country in ownership.children('country'):
                        if scalar(country.one('country')) == 'c:TUR':
                            result[state.key[2:]] = country.children('levels')[0]
    return result


def apply_expected_admin_cuts(nodes, file):
    for state, level in admin_ownership(nodes).items():
        if state in ADMIN_CUTS and ADMIN_CUTS[state][0] == file:
            _, old, new = ADMIN_CUTS[state]
            assert level.value == str(old), (state, level.value)
            level.value = str(new)


def ottoman_admin_building_checks():
    before, after = {}, {}
    for file in sorted((ROOT/'common/history/buildings').glob('*.txt')):
        rel = file.relative_to(ROOT).as_posix()
        old, new = parse(read(rel, True)), parse(read(rel))
        # Egypt's 22 levels were already transferred to EGY by the previous lot.
        before.update({state: int(level.value) for state, level in admin_ownership(old).items() if state not in EGYPT})
        after.update({state: int(level.value) for state, level in admin_ownership(new).items()})
        if rel in {row[0] for row in ADMIN_CUTS.values()}:
            apply_expected_admin_cuts(old, rel)
            assert normalized(old) == normalized(new), 'Other buildings, owners, reserves or PM changed: '+rel
    assert before == {state: old for state, (_, old, _) in ADMIN_CUTS.items()}, before
    assert after == {state: new for state, (_, _, new) in ADMIN_CUTS.items()}, after
    assert sum(before.values()) - sum(after.values()) == 10
    assert set(before) == set(after) and all(after.values())
    print('PASS: exactly 10 directly Ottoman government administration levels removed (64 -> 54); all three buildings and their PM/ownership preserved; Egypt and other owners untouched')


def inventories(base=False):
    totals = {}
    for folder in ('states', 'pops', 'buildings'):
        states = {}
        for file in sorted((ROOT / 'common/history' / folder).glob('*.txt')):
            rel = file.relative_to(ROOT)
            if base and subprocess.run(['git', 'cat-file', '-e', f'{BASE}:{rel.as_posix()}'], cwd=ROOT, capture_output=True).returncode:
                continue
            nodes = parse(read(rel, base))
            if base and folder == 'buildings':
                apply_expected_admin_cuts(nodes, rel.as_posix())
            for n in walk(nodes):
                if n.key.startswith('s:') and n.key[2:] in EGYPT | LEVANT:
                    states.setdefault(n.key[2:], []).append((rel.as_posix(), normalized(n.children(), True)))
        totals[folder] = states
    units = collections.Counter()
    for file in sorted((ROOT / 'common/history/military_formations').glob('*.txt')):
        rel = file.relative_to(ROOT)
        if base and subprocess.run(['git', 'cat-file', '-e', f'{BASE}:{rel.as_posix()}'], cwd=ROOT, capture_output=True).returncode:
            continue
        for country in [n for wrapper in parse(read(rel, base)) for n in wrapper.children()]:
            if country.key not in ('c:TUR', 'c:EGY'):
                continue
            for formation in country.children('create_military_formation'):
                for unit in formation.children('combat_unit'):
                    units[(scalar(unit.one('state_region')), scalar(unit.one('type')), scalar(unit.one('service_type', 'regular')))] += int(unit.one('count'))
    totals['units'] = sorted((list(key), value) for key, value in units.items())
    return totals


def audit():
    summary = {'base': BASE, 'egypt_states': sorted(EGYPT), 'levant_states': sorted(LEVANT), 'armies': {}}
    for file in (ROOT / 'common/history/military_formations').glob('*.txt'):
        for country in [n for wrapper in parse(file.read_text(encoding='utf-8-sig')) for n in wrapper.children()]:
            if country.key not in ('c:TUR', 'c:EGY', 'c:GBR'):
                continue
            for formation in country.children('create_military_formation'):
                counts = collections.Counter()
                for unit in formation.children('combat_unit'):
                    counts[scalar(unit.one('service_type', 'regular'))] += int(unit.one('count'))
                summary['armies'].setdefault(country.key, []).append({'name': formation.one('name'), 'hq': formation.one('hq_region'), 'counts': dict(counts)})
    summary['treaties'] = []
    for treaty in walk(parse(read('common/history/treaties/00_historical_treaties.txt'))):
        if treaty.key == 'create_treaty':
            summary['treaties'].append({'name': treaty.one('name'), 'first': treaty.one('first_country'), 'second': treaty.one('second_country'), 'date': treaty.one('entered_into_force_on'), 'articles': [n.one('article') for n in treaty.children('articles_to_create')[0].children()]})
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def effective(folder):
    """File overrides first, then object definitions; technologies replace vanilla."""
    paths = {}
    bases = (ROOT,) if folder == 'common/technology/technologies' else (GAME, ROOT)
    for base in bases:
        for p in sorted((base / folder).glob('*.txt')):
            paths[p.name] = p
    objects = {}
    for p in paths.values():
        for n in parse(p.read_text(encoding='utf-8-sig')):
            if n.key and isinstance(n.value, list):
                objects[n.key] = n
    return objects


def localizations(language):
    keys = set()
    for base in (GAME, ROOT):
        for p in (base / 'localization' / language).rglob('*.yml'):
            keys.update(re.findall(r'^\s+([\w.\-]+):', p.read_text(encoding='utf-8-sig'), re.M))
    return keys


def technology_audit():
    def metrics(base):
        techs = {}
        duplicates = []
        for p in sorted((base / 'common/technology/technologies').glob('*.txt')):
            for n in parse(p.read_text(encoding='utf-8-sig')):
                if not n.key or not isinstance(n.value, list):
                    continue
                if n.key in techs:
                    duplicates.append(n.key)
                techs[n.key] = n
        graph = {k: {scalar(n.value) for b in t.children('unlocking_technologies') for n in b.children()} for k, t in techs.items()}
        missing = sorted({p for parents in graph.values() for p in parents if p not in graph})
        colours = {}
        stack = []
        cycles = []
        def visit(k):
            if colours.get(k) == 1:
                cycles.append(stack[stack.index(k):] + [k])
                return
            if colours.get(k) == 2:
                return
            colours[k] = 1
            stack.append(k)
            for p in graph[k]:
                if p in graph:
                    visit(p)
            stack.pop()
            colours[k] = 2
        for k in graph:
            visit(k)
        icons = []
        placeholders = []
        for k, t in techs.items():
            icon = scalar(t.one('texture', ''))
            if not icon or not (ROOT / icon).is_file() and not (GAME / icon).is_file():
                icons.append((k, icon))
            if 'error_dir' in icon or 'placeholder' in icon:
                placeholders.append(k)
        loc_missing = {}
        for language in ('english', 'french'):
            loc = localizations(language)
            loc_missing[language] = [key for k in techs for key in (k, k+'_desc') if key not in loc]
        return {'nodes': len(graph), 'edges': sum(map(len, graph.values())), 'max_direct_prerequisites': max(map(len, graph.values()), default=0),
                'duplicates': duplicates, 'cycles': cycles, 'missing_prerequisites': missing, 'missing_icons': icons,
                'placeholder_icons': placeholders, 'missing_localization': loc_missing}
    gui = read('gui/tech_tree.gui')
    return {'mod': metrics(ROOT), 'vanilla': metrics(GAME), 'gui_difference': {
        'mod_ObjectsEqual_calls': gui.count('ObjectsEqual('),
        'vanilla_ObjectsEqual_calls': (GAME / 'gui/tech_tree.gui').read_text(encoding='utf-8-sig').count('ObjectsEqual('),
        'longest_gui_line': max(map(len, gui.splitlines())),
    }}


class ScriptModel:
    """Small interpreter of the actual custom effects for deterministic tests.

    Country economy and diplomacy inputs are fixtures, NOT a game simulation.
    Unknown syntax fails loudly; it cannot silently turn a broken condition true.
    """
    def __init__(self):
        self.variables = {}
        self.journals = set()
        self.modifiers = set()
        self.events = []
        self.scoped_facts = []
        self.modifier_scales = {}
        self.modifier_updates = 0
        self.effects = effective('common/scripted_effects')
        self.triggers = effective('common/scripted_triggers')
        self.entries = effective('common/journal_entries')
        self.law_parents = {key: node.one('parent') for key, node in effective('common/laws').items()}
        self.facts = {'game_date': '1776.1.1', 'bureaucracy': 300, 'approaching_bureaucracy_shortage': False,
                      'government_legitimacy': 40, 'is_at_war': False, 'in_default': False, 'has_revolution': False,
                      'highest_secession_progress': 0.1, 'territory': True, 'egypt_subject': True,
                      'subjects': [20, 20], 'institutions': {'institution_police': 0, 'institution_schools': 0, 'institution_home_affairs': 0},
                      'laws': {'law_hereditary_bureaucrats', 'law_land_based_taxation'},
                      'technologies': set(),
                      'administrations': [{'is_building_type': 'building_government_administration',
                                            'building_has_goods_shortage': False, 'occupancy': 1}],
                      'states': [{'is_incorporated': True, 'tax_capacity': 100, 'tax_capacity_usage': 100}]}

    def numeric(self, value):
        if isinstance(value, str) and value.startswith('var:'):
            return self.variables.get(value[4:], 0)
        if self.scoped_facts and value in self.scoped_facts[-1]:
            return self.scoped_facts[-1][value]
        return float(value)

    def iterator(self, records, node):
        selected, matches = [], []
        filters = node.children('filter')
        tests = [n for n in node.children() if n.key not in ('filter', 'percent', 'count')]
        for record in records:
            self.scoped_facts.append(record)
            if not filters or self.condition(filters[0].children()):
                selected.append(record)
                if self.condition(tests):
                    matches.append(record)
            self.scoped_facts.pop()
        if node.children('percent'):
            return bool(selected) and self.compare(len(matches)/len(selected), node.children('percent')[0].op, node.one('percent'))
        if node.children('count'):
            return self.compare(len(matches), node.children('count')[0].op, node.one('count'))
        return bool(matches)

    @staticmethod
    def compare(actual, op, expected):
        expected = scalar(expected)
        if expected in ('yes', 'no'):
            expected = expected == 'yes'
        elif re.fullmatch(r'\d+\.\d+\.\d+', expected):
            actual, expected = tuple(map(int, str(actual).split('.'))), tuple(map(int, expected.split('.')))
        else:
            expected = float(expected)
        return {'=': lambda: actual == expected, '>=': lambda: actual >= expected, '>': lambda: actual > expected,
                '<=': lambda: actual <= expected, '<': lambda: actual < expected, '!=': lambda: actual != expected}[op]()

    def condition(self, nodes):
        return all(self.test(n) for n in nodes)

    def test(self, n):
        k, v = n.key, n.value
        if k in ('AND', 'limit'):
            return self.condition(n.children())
        if k == 'custom_tooltip':
            return self.condition([t for t in n.children() if t.key != 'text'])
        if k == 'OR':
            return any(self.test(x) for x in n.children())
        if k == 'NOT':
            return not self.condition(n.children())
        if k == 'NOR':
            return not any(self.test(x) for x in n.children())
        if k.startswith('ottoman_1776_'):
            return self.condition(self.triggers[k].children()) == (v == 'yes')
        if k == 'has_variable':
            return v in self.variables
        if k == 'has_journal_entry':
            return v in self.journals
        if k == 'has_modifier':
            return v in self.modifiers
        if k == 'has_law_or_variant':
            requested = scalar(v).removeprefix('law_type:')
            for law in self.facts['laws']:
                seen = set()
                while law and law not in seen:
                    if law == requested:
                        return True
                    seen.add(law)
                    law = self.law_parents.get(law)
            return False
        if k == 'has_technology_researched':
            return scalar(v) in self.facts['technologies']
        if k == 'owns_entire_state_region':
            return False if v == 'STATE_LOWER_EGYPT' else self.facts['territory']
        if k == 'exists':
            return v == 'c:EGY'
        if k == 'c:EGY':
            return self.facts['egypt_subject']
        if k == 'any_subject_or_below':
            return any(self.compare(x, t.op, t.value) for x in self.facts['subjects'] for t in n.children())
        if k == 'institution_investment_level':
            t = n.children('value')[0]
            return self.compare(self.facts['institutions'].get(n.one('institution'), 0), t.op, t.value)
        if k == 'any_scope_building':
            return self.iterator(self.facts['administrations'], n)
        if k == 'any_scope_state':
            return self.iterator(self.facts['states'], n)
        if self.scoped_facts and k in self.scoped_facts[-1]:
            actual = self.scoped_facts[-1][k]
            if k == 'is_building_type':
                return actual == v
            if v in self.scoped_facts[-1]:
                v = self.numeric(v)
            return self.compare(actual, n.op, v)
        if k.startswith('var:'):
            return self.compare(self.variables.get(k[4:], 0), n.op, self.numeric(v))
        if k in self.facts:
            return self.compare(self.facts[k], n.op, v)
        raise AssertionError('Unhandled model condition: '+k)

    def run(self, name):
        self.effect(self.effects[name].children())

    def effect(self, nodes):
        branch = False
        for n in nodes:
            k, v = n.key, n.value
            if k in ('if', 'else_if'):
                ok = (k == 'if' or not branch) and self.condition(n.children('limit')[0].children())
                if k == 'if':
                    branch = False
                if ok:
                    self.effect([x for x in n.children() if x.key != 'limit'])
                    branch = True
            elif k == 'else':
                if not branch:
                    self.effect(n.children())
                branch = False
            elif k == 'set_variable':
                self.variables[v if isinstance(v, str) else n.one('name')] = 1 if isinstance(v, str) else self.numeric(n.one('value', 1))
            elif k == 'change_variable':
                name = n.one('name')
                self.variables[name] += float(n.one('add', 0)) - float(n.one('subtract', 0))
            elif k == 'add_journal_entry':
                assert n.one('type') not in self.journals, 'Duplicate JE'
                self.journals.add(n.one('type'))
            elif k == 'add_modifier':
                self.modifiers.add(n.one('name'))
                self.modifier_scales[n.one('name')] = self.numeric(n.one('multiplier', 1))
                self.modifier_updates += 1
            elif k == 'remove_modifier':
                assert v in self.modifiers, 'Engine would log a missing timed modifier: '+v
                self.modifiers.discard(v)
                self.modifier_scales.pop(v, None)
            elif k == 'trigger_event':
                self.events.append(n.one('id'))
            elif k == 'hidden_effect':
                self.effect(n.children())
            elif k == 'custom_tooltip' and isinstance(v, str):
                pass  # Localization-only; no gameplay effect.
            elif k.startswith('ottoman_1776_'):
                self.run(k)
            else:
                raise AssertionError('Unhandled model effect: '+k)

    def month(self):
        self.activate_pending()
        for key in sorted(self.journals.copy()):
            if not key.startswith('je_1776_'):
                continue
            entry = self.entries[key]
            self.effect(entry.children('on_monthly_pulse')[0].children('effect')[0].children())
            for outcome in ('complete', 'fail'):
                condition = entry.children(outcome)
                if condition and self.condition(condition[0].children()):
                    self.journals.remove(key)
                    for modifier in entry.children('modifiers_while_active'):
                        for item in modifier.children():
                            self.modifiers.discard(item.value)
                    self.effect(entry.children('on_'+outcome)[0].children())
                    break

    def week(self):
        self.activate_pending()
        for key in self.journals.copy():
            if key.startswith('je_1776_'):
                for pulse in self.entries[key].children('on_weekly_pulse'):
                    self.effect(pulse.children('effect')[0].children())

    def activate_pending(self):
        """Model eligibility of engine-precreated INACTIVE custom entries.

        This tests the script guards, not the timing of the game's JE manager.
        """
        for key in ('je_1776_porte_burden', 'je_1776_many_masters'):
            entry = self.entries[key]
            if key not in self.journals and self.condition(entry.children('possible')[0].children()):
                assert self.condition(entry.children('is_shown_when_inactive')[0].children())
                self.journals.add(key)
                for modifier in entry.children('modifiers_while_active'):
                    self.modifiers.update(item.value for item in modifier.children())


def model_tests():
    base = ScriptModel()
    base.activate_pending()
    assert not base.journals, 'Journals must not activate for uninitialized countries'
    base.run('ottoman_1776_initialize')
    base.run('ottoman_1776_initialize')
    assert not base.journals, 'Initializer must not duplicate engine-precreated entries'
    base.activate_pending()
    assert not base.journals, 'New campaigns must wait for introductory choices'
    base.run('ottoman_1776_launch_introductions')
    base.run('ottoman_1776_launch_introductions')
    assert base.events == ['ottoman_1776.10', 'ottoman_1776.11'], 'Startup events must be queued once only'
    base.activate_pending()
    assert not base.journals, 'Showing an event must not activate the journal before its choice'
    intro_events = {n.key: n for n in parse(read('events/1776_ottoman_reforms.txt'))}
    def choose_intro(model, key):
        event = intro_events[key]
        assert model.condition(event.children('trigger')[0].children())
        model.effect(event.children('option')[0].children('hidden_effect')[0].children())
        model.activate_pending()
    choose_intro(base, 'ottoman_1776.10')
    assert base.journals == {'je_1776_porte_burden'}
    choose_intro(base, 'ottoman_1776.11')
    base.activate_pending()
    assert len(base.journals) == 2 and not base.variables.get('ottoman_1776_sick_man_started')
    assert 'ottoman_1776_admin_burden' in base.modifiers
    assert 'ottoman_1776_many_masters_pressure' in base.modifiers

    def clone(model):
        # Parsed definitions are immutable and shared; don't copy the entire game.
        result = copy.copy(model)
        for name in ('variables', 'journals', 'modifiers', 'events', 'facts', 'modifier_scales', 'scoped_facts'):
            setattr(result, name, copy.deepcopy(getattr(model, name)))
        return result

    # Choices can be accepted in reverse order and repeated effects remain inert.
    reverse = clone(base)
    reverse.variables = {}
    reverse.journals = set()
    reverse.modifiers = set()
    reverse.modifier_scales = {}
    reverse.events = []
    reverse.run('ottoman_1776_initialize')
    reverse.run('ottoman_1776_launch_introductions')
    choose_intro(reverse, 'ottoman_1776.11')
    assert reverse.journals == {'je_1776_many_masters'}
    choose_intro(reverse, 'ottoman_1776.10')
    snapshot = (reverse.variables.copy(), reverse.modifiers.copy(), reverse.modifier_updates)
    reverse.run('ottoman_1776_open_administration')
    reverse.run('ottoman_1776_open_politics')
    reverse.run('ottoman_1776_launch_introductions')
    assert snapshot == (reverse.variables, reverse.modifiers, reverse.modifier_updates)
    assert reverse.events == ['ottoman_1776.10', 'ottoman_1776.11']
    for key in ('ottoman_1776.10', 'ottoman_1776.11'):
        assert not reverse.condition(intro_events[key].children('trigger')[0].children())
    # Old saves do not replay introductions or lose their existing progress.
    prior_version = clone(base)
    for flag in ('ottoman_1776_intro_flow', 'ottoman_1776_admin_opened', 'ottoman_1776_political_opened'):
        del prior_version.variables[flag]
    prior_version.variables.update(ottoman_1776_admin_months=8, ottoman_1776_stability_months=9)
    prior_version.events.clear()
    previous_modifiers = prior_version.modifiers.copy()
    prior_version.run('ottoman_1776_launch_introductions')
    assert not prior_version.events
    prior_version.run('ottoman_1776_reconcile')
    prior_version.activate_pending()
    assert prior_version.journals == base.journals and not prior_version.events
    assert prior_version.variables['ottoman_1776_admin_months'] == 8
    assert prior_version.variables['ottoman_1776_stability_months'] == 9
    assert prior_version.modifiers == previous_modifiers

    def set_goals(model, bits):
        offices, balance, reserve, home_affairs, land, consumption, police, schools, capacity, staff = bits
        model.facts.update(bureaucracy=0 if balance else -1, approaching_bureaucracy_shortage=not reserve)
        model.facts['laws'] = set()
        for ok, law in ((offices, 'law_hereditary_bureaucrats'), (land, 'law_land_based_taxation'),
                        (consumption, 'law_consumption_based_taxation')):
            if not ok:
                model.facts['laws'].add(law)
        model.facts['institutions'] = {'institution_police': 3 if police else 2, 'institution_schools': 3 if schools else 2,
                                       'institution_home_affairs': 3 if home_affairs else 2}
        model.facts['administrations'] = [{'is_building_type': 'building_government_administration',
                                           'building_has_goods_shortage': True, 'occupancy': 0.8 if staff else 0.79}]
        model.facts['states'] = [{'is_incorporated': True, 'tax_capacity': 100 if capacity else 99, 'tax_capacity_usage': 100}]

    # Exercise the actual ten triggers and score effect for every input combination.
    # The reserve goal now also requires balance: a deficit cannot count as safe.
    # Contradictory-law fixtures exercise the arithmetic defensively, not a playable government.
    for bits in itertools.product((False, True), repeat=10):
        model = clone(base)
        set_goals(model, bits)
        model.week()
        score = sum(bits) - int(bits[2] and not bits[1])
        assert model.variables['ottoman_1776_admin_score'] == score
        assert model.modifier_scales.get('ottoman_1776_admin_relief', 0) == score
        assert model.condition(model.triggers['ottoman_1776_all_admin_goals'].children()) == all(bits)
        updates = model.modifier_updates
        model.week()
        assert updates == model.modifier_updates, 'Unchanged weekly score recreated its modifier'
        assert 0 <= 1 - 0.1*score + 1e-12 <= 1.000000000001

    # Each of the ten actual objectives offsets exactly one unit of both penalties.
    goals = [n.key for n in base.triggers['ottoman_1776_all_admin_goals'].children()]
    assert len(goals) == 10 and len(set(goals)) == 10
    all_true = clone(base)
    set_goals(all_true, (True,)*10)
    all_true.week()
    assert all_true.variables['ottoman_1776_admin_score'] == 10
    for goal in goals:
        isolated = clone(all_true)
        # Override only this condition to isolate its numerical contribution,
        # including the balance/reserve dependency in real game fixtures.
        isolated.triggers = dict(isolated.triggers)
        isolated.triggers[goal] = parse(f'{goal} = {{ bureaucracy < 0 }}')[0]
        isolated.week()
        assert isolated.variables['ottoman_1776_admin_score'] == 9, goal
        assert isolated.modifier_scales['ottoman_1776_admin_relief'] == 9, goal

    # Native iterator semantics: nonempty guards, exact percentages and inclusive thresholds.
    boundary = clone(base)
    boundary.facts['administrations'] = []
    for goal in ('staff',):
        assert not boundary.condition(boundary.triggers['ottoman_1776_goal_'+goal].children())
    # A non-approaching shortage is not sufficient when the balance is negative.
    for bureaucracy, approaching, expected in ((-1, False, False), (0, False, True),
                                               (1, False, True), (0, True, False), (-1, True, False)):
        boundary.facts.update(bureaucracy=bureaucracy, approaching_bureaucracy_shortage=approaching)
        assert boundary.condition(boundary.triggers['ottoman_1776_goal_reserve'].children()) == expected
    # Political technologies/law must not affect any administrative objective.
    eligibility = clone(base)
    set_goals(eligibility, (True,)*10)
    eligibility.facts['government_legitimacy'] = 75
    for techs in (set(), {'rifling'}, {'abolitionist_mobilization'}):
        eligibility.facts['technologies'] = techs
        assert eligibility.condition(eligibility.triggers['ottoman_1776_all_admin_goals'].children())
        assert not eligibility.condition(eligibility.triggers['ottoman_1776_politically_stable'].children())
    eligibility.facts['technologies'] = {'rifling', 'abolitionist_mobilization'}
    eligibility.facts['laws'].add('law_slave_trade')
    assert eligibility.condition(eligibility.triggers['ottoman_1776_all_admin_goals'].children())
    assert not eligibility.condition(eligibility.triggers['ottoman_1776_politically_stable'].children())
    eligibility.facts['laws'] = {'law_hereditary_slavery'}
    assert eligibility.condition(eligibility.triggers['ottoman_1776_all_admin_goals'].children()), 'Ending trade need not abolish all slavery'
    assert eligibility.condition(eligibility.triggers['ottoman_1776_politically_stable'].children())
    # Synthetic inherited law exercises the native has_law_or_variant contract.
    variant = clone(eligibility)
    variant.law_parents = dict(variant.law_parents, test_slave_trade_variant='law_slave_trade')
    variant.facts['laws'] = {'test_slave_trade_variant'}
    assert not variant.condition(variant.triggers['ottoman_1776_politically_stable'].children())
    assert variant.condition(variant.triggers['ottoman_1776_all_admin_goals'].children())
    for police, schools, home_affairs in itertools.product((2, 3), repeat=3):
        eligibility.facts['institutions'] = {'institution_police': police, 'institution_schools': schools,
                                            'institution_home_affairs': home_affairs}
        expected = police >= 3 and schools >= 3 and home_affairs >= 3
        assert eligibility.condition(eligibility.triggers['ottoman_1776_all_admin_goals'].children()) == expected
        assert eligibility.condition(eligibility.triggers['ottoman_1776_politically_stable'].children())
    # All political paths require research/law, but only centralisation has its
    # original police OR schools >=2 requirement; Home Affairs is never global.
    for path in ('institutions', 'compromise', 'administration'):
        gated = clone(base)
        gated.facts['government_legitimacy'] = {'institutions': 60, 'compromise': 75, 'administration': 50}[path]
        if path == 'administration':
            gated.variables['ottoman_1776_admin_complete'] = 1
        elif path == 'institutions':
            gated.facts['subjects'] = [30, 30]  # Prevent the compromise alternative.
        for rifling, abolition, trade_ended, police, schools, home_affairs in itertools.product((False, True), repeat=6):
            gated.facts['technologies'] = {t for t, ok in (('rifling', rifling), ('abolitionist_mobilization', abolition)) if ok}
            gated.facts['laws'] = set() if trade_ended else {'law_slave_trade'}
            gated.facts['institutions'] = {'institution_police': 2 if police else 0, 'institution_schools': 2 if schools else 0,
                                           'institution_home_affairs': 3 if home_affairs else 0}
            expected = rifling and abolition and trade_ended and (path != 'institutions' or police or schools)
            assert gated.condition(gated.triggers['ottoman_1776_politically_stable'].children()) == expected, path
    # Original legitimacy thresholds and strict compromise-subject threshold.
    for path, threshold in (('institutions', 60), ('compromise', 75), ('administration', 50)):
        gated = clone(base)
        gated.facts['technologies'] = {'rifling', 'abolitionist_mobilization'}
        gated.facts['laws'] = set()
        if path == 'institutions':
            gated.facts['institutions']['institution_police'] = 2
            gated.facts['subjects'] = [30]
        if path == 'administration':
            gated.variables['ottoman_1776_admin_complete'] = 1
        for legitimacy in (threshold-1, threshold):
            gated.facts['government_legitimacy'] = legitimacy
            assert gated.condition(gated.triggers['ottoman_1776_politically_stable'].children()) == (legitimacy == threshold)
        if path == 'compromise':
            gated.facts['subjects'] = [25]
            assert not gated.condition(gated.triggers['ottoman_1776_politically_stable'].children())
    boundary.facts['states'] = []
    assert not boundary.condition(boundary.triggers['ottoman_1776_goal_tax_capacity'].children())
    boundary.facts['states'] = [{'is_incorporated': True, 'tax_capacity': 100, 'tax_capacity_usage': 100} for _ in range(4)]
    boundary.facts['states'][0]['tax_capacity'] = 99
    assert boundary.condition(boundary.triggers['ottoman_1776_goal_tax_capacity'].children())
    boundary.facts['states'][1]['tax_capacity'] = 99
    assert not boundary.condition(boundary.triggers['ottoman_1776_goal_tax_capacity'].children())
    boundary.facts['administrations'] = [{'is_building_type': 'building_government_administration',
        'building_has_goods_shortage': i == 0, 'occupancy': 0.79 if i == 0 else 0.8} for i in range(10)]
    for goal in ('staff',):
        assert boundary.condition(boundary.triggers['ottoman_1776_goal_'+goal].children())
    boundary.facts['administrations'][1].update(building_has_goods_shortage=True, occupancy=0.79)
    for goal in ('staff',):
        assert not boundary.condition(boundary.triggers['ottoman_1776_goal_'+goal].children())
    # Political resolution does not imply administrative reform.
    political = clone(base)
    political.facts['technologies'] = {'rifling', 'abolitionist_mobilization'}
    # Compromise completes with all three institutions at zero.
    political.facts['institutions'] = {'institution_police': 0, 'institution_schools': 0, 'institution_home_affairs': 0}
    political.facts['government_legitimacy'] = 75
    for _ in range(36):
        political.month()
    assert 'ottoman_1776_political_complete' in political.variables
    assert 'je_1776_porte_burden' in political.journals
    # Administrative resolution does not imply political resolution.
    admin = clone(base)
    set_goals(admin, (True,)*10)
    admin.facts['laws'].add('law_slave_trade')
    for _ in range(12):
        admin.month()
    assert 'ottoman_1776_admin_complete' in admin.variables
    assert 'je_1776_many_masters' in admin.journals and admin.modifiers == {'ottoman_1776_many_masters_pressure'}
    admin.facts['technologies'] = {'rifling', 'abolitionist_mobilization'}
    admin.facts['laws'].remove('law_slave_trade')
    # Completed administrative reform is remembered even if institutions regress.
    admin.facts['institutions'] = {'institution_police': 0, 'institution_schools': 0, 'institution_home_affairs': 0}
    admin.facts['government_legitimacy'] = 50
    for _ in range(18):
        admin.month()
    assert 'ottoman_1776_political_complete' in admin.variables
    # Loss of reforms removes relief; interrupted progress resets.
    rollback = clone(base)
    set_goals(rollback, (True,)*10)
    for _ in range(11):
        rollback.month()
    assert 'ottoman_1776_admin_complete' not in rollback.variables
    assert rollback.variables['ottoman_1776_admin_months'] == 11
    rollback.facts['institutions']['institution_schools'] = 1
    rollback.week()
    assert rollback.modifier_scales['ottoman_1776_admin_relief'] == 9
    assert rollback.variables['ottoman_1776_admin_months'] == 0
    rollback.facts['institutions']['institution_schools'] = 3
    rollback.month()
    assert rollback.variables['ottoman_1776_admin_months'] == 1
    # Missing political research and slave trade do NOT reset admin consolidation.
    rollback.facts['technologies'].clear()
    rollback.facts['laws'].add('law_slave_trade')
    rollback.week()
    assert rollback.variables['ottoman_1776_admin_months'] == 1
    assert rollback.modifier_scales['ottoman_1776_admin_relief'] == 10
    rollback.month()
    assert rollback.variables['ottoman_1776_admin_months'] == 2
    rollback.facts['institutions']['institution_home_affairs'] = 2
    rollback.week()
    assert rollback.variables['ottoman_1776_admin_months'] == 0
    assert rollback.modifier_scales['ottoman_1776_admin_relief'] == 9
    set_goals(rollback, (False,)*10)
    rollback.week()
    assert 'ottoman_1776_admin_relief' not in rollback.modifiers
    # Legacy-score migration discards invalid old confirmation months and relief.
    legacy = clone(base)
    del legacy.variables['ottoman_1776_admin_v2']
    legacy.variables['ottoman_1776_admin_months'] = 11
    legacy.modifiers.add('ottoman_1776_admin_relief_2')
    legacy.week()
    assert legacy.variables['ottoman_1776_admin_months'] == 0 and 'ottoman_1776_admin_relief_2' not in legacy.modifiers
    # Serious pressure causes an early failure after 40 months at +3 crisis points/month.
    crisis = clone(base)
    crisis.facts.update(territory=False, bureaucracy=-50, is_at_war=True)
    for _ in range(39):
        crisis.month()
    assert 'je_1776_many_masters' in crisis.journals
    crisis.month()
    assert 'je_1776_many_masters' not in crisis.journals
    assert 'ottoman_1776_political_failed' in crisis.variables
    # A delayed event lost during regime change is recovered by the actual monthly hook.
    inherited = clone(crisis)
    inherited.events.clear()
    inherited.run('ottoman_1776_reconcile')
    snapshot = (inherited.variables.copy(), inherited.journals.copy(), inherited.modifiers.copy())
    inherited.run('ottoman_1776_reconcile')
    assert snapshot == (inherited.variables, inherited.journals, inherited.modifiers)
    assert 'je_sick_man_main' in inherited.journals and 'je_1776_many_masters' not in inherited.journals
    assert 'je_1776_porte_burden' in inherited.journals and 'outmoded_bureaucracy' not in inherited.modifiers
    assert 'ottoman_1776_many_masters_pressure' not in inherited.modifiers
    # Deadline is unconditional even when crisis is zero and the country is stable.
    deadline = clone(base)
    set_goals(deadline, (True,)*10)
    deadline.facts.update(game_date='1836.1.1', government_legitimacy=75, technologies={'rifling', 'abolitionist_mobilization'})
    deadline.variables.update(ottoman_1776_crisis_months=0, ottoman_1776_stability_months=35)
    deadline.month()
    assert 'ottoman_1776_political_failed' in deadline.variables
    assert 'ottoman_1776_political_complete' not in deadline.variables
    deadline.run('ottoman_1776_reconcile')
    assert 'je_sick_man_main' in deadline.journals
    political.activate_pending()
    assert 'je_1776_many_masters' not in political.journals, 'Completed political JE reactivated'
    admin.activate_pending()
    assert not admin.journals, 'Completed JEs reactivated'
    inherited.activate_pending()
    assert 'je_1776_many_masters' not in inherited.journals, 'Failed political JE reactivated'
    print('PASS: 1024 objective combinations, iterator boundaries, weekly idempotence, migration, independent resolutions, 12-month reset, early failure, firm 1836 deadline and delayed-transition recovery')
    print('PASS: ten individual relief contributions, three administrative institutions >=3, no administrative research/trade gates; 192 political path combinations with original police OR schools >=2, legitimacy boundaries and independent completion')
    print('PASS: two startup events once, journal activation only by their respective choices, either choice order, idempotent opening effects and old-save progress preservation')


def implementation_checks():
    touched = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT).decode().splitlines()
    touched += subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT).decode().splitlines()
    for p in touched:
        if p.endswith('.txt') and p.startswith(('common/', 'events/')):
            parse(read(p))
    treaties = [n for n in walk(parse(read('common/history/treaties/00_historical_treaties.txt'))) if n.key == 'create_treaty']
    assert not any(n.one('second_country') == 'c:USA' and n.one('first_country') in ('c:FRA', 'c:SPA') for n in treaties)
    cap = next(n for n in treaties if n.one('name') == 'treaty_1776_capitulations')
    articles = cap.children('articles_to_create')[0].children()
    assert len(articles) == 1 and articles[0].one('source_country') == 'c:TUR' and articles[0].one('target_country') == 'c:FRA'
    # Preserve every vanilla subjugation condition and effect except the one tenure gate.
    rel = 'common/diplomatic_actions/31_power_bloc_force_become_subject.txt'
    old = parse((GAME / rel).read_text(encoding='utf-8-sig'))
    new = parse(read(rel))
    target = next(n for n in new[0].children('possible')[0].children('scope:target_country') if n.children('OR'))
    gate = target.children('OR')[0]
    assert gate.children()[0].key == 'tenure_in_current_power_bloc_years' and gate.children()[0].value == '5'
    pair = gate.children('AND')[0].children()
    assert [(n.key, n.op, n.value) for n in pair] == [('c:CRI', '?=', 'this'), ('c:RUS', '?=', 'root')]
    target.value = [gate.children()[0]]
    assert normalized(old) == normalized(new), 'Unintended global diplomatic action change'
    states = {n.key[2:]: n for n in parse(read('common/history/states/00_states.txt'))[0].children()}
    for state in EGYPT:
        assert states[state].children('create_state')[0].one('country') == 'c:EGY'
    for state in LEVANT:
        entry = states[state].children('create_state')[0]
        assert entry.one('country') == 'c:TUR' and entry.one('state_type') == 'unincorporated'
    subjects = parse(read('common/history/diplomacy/00_subject_relationships.txt'))[0].children()
    tur = next(n for n in subjects if n.key == 'c:TUR')
    assert any(n.one('country') == 'c:EGY' and n.one('type') == 'puppet' for n in tur.children('create_diplomatic_pact'))
    assert not any(n.one('country') == 'c:CRI' for n in tur.children('create_diplomatic_pact'))
    assert 'egy_muhammad_ali_template' not in read('common/history/characters/egy - egypt.txt')
    je = parse(read('common/journal_entries/1776_ottoman_reforms.txt'))
    for n in je:
        assert n.one('can_revolution_inherit') == 'yes' and not n.children('timeout')
    for p in ('common/journal_entries/1776_ottoman_reforms.txt',
              'common/scripted_effects/1776_ottoman_reform_effects.txt', 'events/1776_ottoman_reforms.txt'):
        nodes = list(walk(parse(read(p))))
        assert not any(n.key == 'current_date' for n in nodes), 'Invalid engine trigger current_date'
        if p.startswith('common/journal_entries/'):
            assert any(n.key == 'game_date' for n in nodes), 'Missing actual engine date trigger'
    native = (GAME/'common/scripted_triggers/00_ai_triggers.txt').read_text(encoding='utf-8-sig')
    assert re.search(r'\bgame_date\s*<=', native), 'Date trigger not verified against installed game'
    entries = {n.key: n for n in je}
    admin = entries['je_1776_porte_burden']
    goals = [n for n in admin.children('complete')[0].children() if n.key == 'custom_tooltip']
    assert len(goals) == 10 and len({n.one('text') for n in goals}) == 10
    triggers = effective('common/scripted_triggers')
    def expanded(nodes, seen=frozenset()):
        result = list(walk(nodes))
        for node in list(result):
            if node.key in triggers and node.key not in seen:
                result.extend(expanded(triggers[node.key].children(), seen | {node.key}))
        return result
    # Audit activation, completion AND score/consolidation transitively.
    admin_nodes = expanded(admin.children()) + expanded(triggers['ottoman_1776_all_admin_goals'].children())
    assert not any(n.key == 'has_technology_researched' for n in admin_nodes)
    assert not any(n.key == 'has_law_or_variant' and n.value == 'law_type:law_slave_trade' for n in admin_nodes)
    assert not any(n.key == 'building_has_goods_shortage' for n in admin_nodes)
    assert 'ottoman_1776_goal_supply' not in triggers
    admin_goals = triggers['ottoman_1776_all_admin_goals'].children()
    assert len(admin_goals) == 10 and all(n.key.startswith('ottoman_1776_goal_') for n in admin_goals)
    for goal, institution in (('home_affairs', 'institution_home_affairs'), ('police', 'institution_police'), ('schools', 'institution_schools')):
        requirement = triggers['ottoman_1776_goal_'+goal].children('institution_investment_level')[0]
        assert requirement.one('institution') == institution
        threshold = requirement.children('value')[0]
        assert threshold.op == '>=' and threshold.value == '3'
        assert institution in effective('common/institutions')
    political_gates = triggers['ottoman_1776_political_completion_reforms']
    assert {n.value for n in political_gates.children('has_technology_researched')} == {'rifling', 'abolitionist_mobilization'}
    for technology in ('rifling', 'abolitionist_mobilization'):
        assert technology in effective('common/technology/technologies'), technology
    assert 'law_slave_trade' in effective('common/laws')
    assert political_gates.children('NOT')[0].one('has_law_or_variant') == 'law_type:law_slave_trade'
    stable = triggers['ottoman_1776_politically_stable']
    assert stable.one('ottoman_1776_political_completion_reforms') == 'yes'
    assert not stable.children('institution_investment_level')
    assert not any(n.key.startswith('ottoman_1776_goal_') for n in expanded(stable.children()))
    assert admin.children('on_complete')[0].children('hidden_effect')
    assert admin.children('on_complete')[0].one('custom_tooltip') == 'ottoman_1776_admin_completion_tt'
    assert admin.children('on_weekly_pulse') and admin.one('goal_add_value')[0].value == '12'
    assert all(n.one('group') == 'je_group_1776_imperial_crises' for n in je)
    modifiers = effective('common/static_modifiers')
    assert modifiers['ottoman_1776_admin_burden'].one('state_tax_waste_add') == '1.0'
    assert modifiers['ottoman_1776_admin_relief'].one('state_tax_waste_add') == '-0.10'
    assert modifiers['ottoman_1776_admin_relief'].one('country_bureaucracy_mult') == '0.01'
    # UI-only computation must mirror the unchanged tax-waste modifier per point.
    display_value = effective('common/script_values')['ottoman_1776_current_tax_relief']
    tax_value = display_value.children('if')[0]
    assert display_value.one('value') == '0'
    assert tax_value.one('value') == 'var:ottoman_1776_admin_score' and tax_value.one('multiply') == '10'
    for score in range(11):
        assert abs(score * 10 + float(modifiers['ottoman_1776_admin_relief'].one('state_tax_waste_add')) * score * 100) < 1e-9
    pressure = modifiers['ottoman_1776_many_masters_pressure']
    assert pressure.one('country_liberty_desire_of_subjects_add') == '0.15'
    assert not any(n.key in ('state_tax_waste_add', 'country_bureaucracy_mult', 'state_tax_capacity_mult')
                   for key in ('sick_man_of_europe', 'ottoman_1776_many_masters_pressure') for n in modifiers[key].children())
    effects = parse(read('common/scripted_effects/1776_ottoman_reform_effects.txt'))
    assert not any(n.key == 'add_modifier' and n.one('name') == 'outmoded_bureaucracy' for n in walk(effects))
    # On-actions merge their event lists across files; unlike object definitions,
    # they cannot be audited with effective()'s last-object-wins approximation.
    startup = next(n for n in parse(read('common/on_actions/00_code_on_actions.txt'))
                   if n.key == 'on_game_started_after_lobby').children('effect')[0]
    launch = startup.children('c:TUR')[0]
    assert launch.op == '?=' and launch.one('ottoman_1776_launch_introductions') == 'yes'
    # Preserve all pre-existing after-lobby startup logic outside the Ottoman hook.
    old_startup = next(n for n in parse(read('common/on_actions/00_code_on_actions.txt', True)) if n.key == 'on_game_started_after_lobby')
    assert normalized(old_startup.children('effect')[0].children()) == normalized([n for n in startup.children() if n is not launch])
    global_init = parse(read('common/history/global/99_1776_ottoman_reforms.txt'))
    assert not any(n.key == 'trigger_event' for n in walk(global_init)), 'Opening popup must wait until leaving lobby'
    intro_events = {n.key: n for n in parse(read('events/1776_ottoman_reforms.txt'))}
    for key, journal, flag in (('ottoman_1776.10', 'je_1776_porte_burden', 'ottoman_1776_admin_opened'),
                               ('ottoman_1776.11', 'je_1776_many_masters', 'ottoman_1776_political_opened')):
        event = intro_events[key]
        assert len(event.children('option')) == 1 and event.children('option')[0].one('default_option') == 'yes'
        assert event.one('flavor') == key+'.f' and event.one('desc') == key+'.d'
        for gate in ('possible', 'is_shown_when_inactive'):
            assert flag in [n.value for n in entries[journal].children(gate)[0].children('has_variable')]
        picture = scalar(event.children('event_image')[0].one('video'))
        assert (GAME/'gfx/event_pictures'/f'{picture}.bk2').is_file()
        for lang in ('french', 'english'):
            loc = read(f'localization/{lang}/1776_diplomacy_ottoman_l_{lang}.yml')
            for suffix in ('t', 'd', 'f', 'a', 'a.tt'):
                assert re.search(r'^ '+re.escape(key+'.'+suffix)+r': "', loc, re.M)
            flavor = re.search(r'^ '+re.escape(key+'.f')+r': "(.*)"$', loc, re.M).group(1)
            assert flavor.startswith('#italic ') and flavor.endswith('#!'), 'Fictional excerpt must be italic'
    sync = next(n for n in effects if n.key == 'ottoman_1776_sync_administration')
    assert len([n for n in walk(sync.children()) if n.key == 'change_variable' and n.one('name') == 'ottoman_1776_admin_score']) == 10
    assert any(n.key == 'multiplier' and n.value == 'var:ottoman_1776_admin_score' for n in walk(sync.children()))
    native_multiplier = (GAME/'common/journal_entries/05_montenegro_je.txt').read_text(encoding='utf-8-sig')
    assert 'multiplier = var:raiding_intensity' in native_multiplier
    native_capacity = (GAME/'common/buildings/07_government.txt').read_text(encoding='utf-8-sig')
    assert 'state.tax_capacity < state.tax_capacity_usage' in native_capacity
    native_ld = (GAME/'common/script_values/00_diplomacy_values.txt').read_text(encoding='utf-8-sig')
    assert 'root.first_country.modifier:country_liberty_desire_of_subjects_add' in native_ld
    political = entries['je_1776_many_masters']
    assert any(n.key == 'game_date' and n.op == '>=' and n.value == '1836.1.1' for n in walk(political.children('fail')))
    assert any(n.key == 'game_date' and n.op == '<' and n.value == '1836.1.1' for n in political.children('complete')[0].children())
    # Initial diplomacy is adjusted via real leverage/goals, never a recurring leave lock.
    bloc = next(n for n in parse(read('common/history/power_blocs/00_power_blocs.txt'))[0].children() if n.key == 'c:RUS')
    leverage = {n.one('target'): n.one('value') for n in walk(bloc.children()) if n.key == 'add_leverage'}
    assert leverage == {'c:PLC': '650', 'c:CRI': '550'}
    ai = parse(read('common/history/ai/00_secret_goals.txt'))[0]
    for country, target, goal in (('c:PLC', 'c:RUS', 'comply'), ('c:CRI', 'c:RUS', 'comply'),
                                  ('c:RUS', 'c:PLC', 'dominate'), ('c:RUS', 'c:CRI', 'dominate')):
        entry = next(n for n in ai.children() if n.key == country)
        assert next(n for n in entry.children('set_secret_goal') if n.one('country') == target).one('secret_goal') == goal
    assert not any(n.key == 'join_power_bloc' for n in walk(effects)), 'Recurring forced Russian bloc membership'
    # The native success/failure events also remove a modifier our scenario omits.
    # Preserve the rest of those events exactly, including event pictures/options.
    native_events = (GAME/'events/sick_man_events.txt').read_text(encoding='utf-8-sig')
    expected_events = native_events.replace('\t\tremove_modifier = outmoded_bureaucracy',
        '\t\tif = {\n\t\t\tlimit = { has_modifier = outmoded_bureaucracy }\n\t\t\tremove_modifier = outmoded_bureaucracy\n\t\t}')
    expected_events = expected_events.replace('\t\t\tadd_modifier = {\n\t\t\t\tname = outmoded_bureaucracy\n\t\t\t\tmonths = -1\n\t\t\t}',
        '\t\t\t# The independent Porte journal owns all fiscal penalties.\n\t\t\tif = {\n\t\t\t\tlimit = { NOT = { has_variable = ottoman_1776_initialized } }\n\t\t\t\tadd_modifier = { name = outmoded_bureaucracy months = -1 }\n\t\t\t}')
    assert normalized(parse(expected_events)) == normalized(parse(read('events/sick_man_events.txt')))
    units = effective('common/combat_unit_types')
    for unit, tech in (('combat_unit_type_musket_infantry', 'light_infantry_tactics'),
                       ('combat_unit_type_line_infantry', 'armament_standardization_inspection')):
        assert [n.value for n in units[unit].children('unlocking_technologies')[0].children()] == [tech]
    egypt_building_checks()
    plc = parse(read('common/journal_entries/07_poland_lithuania_mod.txt'))[0]
    assert plc.key == 'je_plc_reform' and not plc.children('timeout') and not plc.children('on_timeout')
    assert not any(n.key == 'set_state_owner' for n in walk(plc.children())), 'Automatic Polish partition remains'
    plc_entries = effective('common/journal_entries')
    education = plc_entries['je_plc_reform_education'].children('complete')[0].children('any_scope_state')[0]
    assert education.children('count')[0].op == '>=' and education.one('count') == '5'
    assert not education.children('value'), 'State-count trigger uses invalid value key'
    remove = plc_entries['je_plc_reform_great_power'].children('on_complete')[0].children('remove_modifier')[0]
    assert remove.value == 'the_white_eagle_reborn', 'remove_modifier expects scalar key'
    # Every newly used literal icon exists in the mod or game. No assets generated.
    for p in touched:
        if p.endswith('.txt') and '1776_ottoman' in p:
            for n in walk(parse(read(p))):
                if n.key in ('icon', 'texture') and isinstance(n.value, str):
                    path = scalar(n.value)
                    assert (ROOT/path).is_file() or (GAME/path).is_file(), path
    en = localizations('english')
    fr = localizations('french')
    custom = set(re.findall(r'^\s+([\w.]+):', read('localization/english/1776_diplomacy_ottoman_l_english.yml'), re.M))
    assert custom <= fr and custom <= en
    for p in ('localization/english/1776_diplomacy_ottoman_l_english.yml', 'localization/french/1776_diplomacy_ottoman_l_french.yml'):
        assert (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'), 'Missing localization BOM'
        loc = read(p)
        assert '[Country.MakeScope.Var(' not in loc, 'Status uses absent Country data context'
        for var in ('admin_score', 'admin_months', 'stability_months'):
            assert f"[ROOT.GetCountry.MakeScope.Var('ottoman_1776_{var}').GetValue|v0]" in loc
        localized = dict(re.findall(r'^ ([\w.]+): "(.*)"$', loc, re.M))
        assert 'ottoman_1776_goal_supply_tt' not in localized
        for goal in goals:
            assert goal.one('text') in localized
        assert 'ottoman_1776_goal_home_affairs_tt' in localized
        admin_status = localized['je_1776_porte_burden_status']
        for word in ('Rainurage', 'Abolitionnisme', 'Rifling', 'Abolitionism', 'slave trade', 'commerce d’esclaves'):
            assert word not in admin_status
        path = localized['ottoman_1776_path_institutions_tt']
        assert ('OU' in path or 'OR' in path) and '≥ 2' in path
    # The diesel request only changes the two previously-70 outputs.
    rel = 'common/production_methods/03_mines.txt'
    a, b = read(rel, True), read(rel)
    assert a.replace('goods_output_iron_add = 70', 'goods_output_iron_add = 85').replace('goods_output_lead_add = 70', 'goods_output_lead_add = 85') == b
    print('PASS: syntax, asymmetric privileges, scoped Crimea exception, Egypt subject/state coherence, inherited journals, icon paths, bilingual localization and diesel-only output delta')


def egypt_building_checks():
    country = parse(read('common/history/countries/egy - egypt.txt'))[0].children()[0]
    owned = {n.value for n in country.children('add_technology_researched')}
    buildings, pms = effective('common/buildings'), effective('common/production_methods')
    checked = 0
    for path in (ROOT/'common/history/buildings').glob('*.txt'):
        for region in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if region.key != 'region_state:EGY':
                continue
            for building in region.children('create_building'):
                objects = [buildings[scalar(building.one('building'))]]
                for methods in building.children('activate_production_methods'):
                    objects.extend(pms[scalar(n.value)] for n in methods.children())
                required = {scalar(n.value) for obj in objects
                            for block in obj.children('unlocking_technologies') for n in block.children()}
                assert required <= owned, (path.name, building.one('building'), sorted(required-owned))
                checked += 1
    assert checked > 0
    print(f'PASS: {checked} Egyptian building-history entries and their explicit PM unlocks')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', action='store_true')
    parser.add_argument('--tech', action='store_true')
    args = parser.parse_args()
    if args.audit:
        audit()
        return
    if args.tech:
        print(json.dumps(technology_audit(), indent=2, ensure_ascii=False))
        return
    before, after = inventories(True), inventories()
    ottoman_admin_building_checks()
    for kind in ('states', 'pops', 'buildings'):
        assert before[kind] == after[kind], f'{kind} inventory changed beyond owner/Levant status transfer and exact Ottoman administration cuts'
    expected_units = collections.Counter({tuple(key): value for key, value in before['units']})
    for region, count in (('EASTERN_THRACE', 8), ('BOSNIA', 4), ('BULGARIA', 4), ('ANKARA', 6)):
        expected_units[(f's:STATE_{region}', 'unit_type:combat_unit_type_musket_infantry', 'regular')] += count
    assert dict(expected_units) == {tuple(key): value for key, value in after['units']}, 'Unexpected unit change beyond the authorized 22 regular Ottoman infantry'
    army_counts = collections.Counter()
    for p in (ROOT/'common/history/military_formations').glob('*.txt'):
        for wrapper in parse(p.read_text(encoding='utf-8-sig')):
            for country in wrapper.children():
                if country.key not in ('c:TUR', 'c:EGY'):
                    continue
                for formation in country.children('create_military_formation'):
                    if formation.one('type') != 'army':
                        continue
                    for unit in formation.children('combat_unit'):
                        army_counts[(country.key, unit.one('service_type', 'regular'))] += int(unit.one('count'))
    assert army_counts == {('c:TUR', 'regular'): 72, ('c:TUR', 'conscript'): 114,
                           ('c:EGY', 'regular'): 15, ('c:EGY', 'conscript'): 25}, army_counts
    tur = parse(read('common/history/countries/tur - ottoman empire.txt'))[0].children()[0]
    techs = {n.value for n in tur.children('add_technology_researched')}
    musket = effective('common/combat_unit_types')['combat_unit_type_musket_infantry']
    assert {n.value for n in musket.children('unlocking_technologies')[0].children()} <= techs
    starting_states = parse(read('common/history/states/00_states.txt'))[0]
    for region in ('EASTERN_THRACE', 'BOSNIA', 'BULGARIA', 'ANKARA'):
        state = next(n for n in starting_states.children() if n.key == f's:STATE_{region}')
        assert any(n.one('country') == 'c:TUR' for n in state.children('create_state'))
    print('PASS: provinces/pops/other buildings conserved; Ottoman army 72 regular, 114 conscript; Egyptian army unchanged; reinforcement technology available')
    implementation_checks()
    model_tests()


if __name__ == '__main__':
    main()
