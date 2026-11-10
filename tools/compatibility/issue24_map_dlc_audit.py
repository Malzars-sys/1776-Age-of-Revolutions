"""Read-only map/startup and non-journal DLC inventory for issue 24.

Models same-path masks and replacement directives. Checks literal references,
not historical accuracy, script reachability, engine loading or DLC ownership.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(value):
    return value.strip('"') if isinstance(value, str) else None


def bare(node):
    return [plain(n.value) for n in node.children() if not n.key and isinstance(n.value, str)]


def color(value):
    value = plain(value)
    return value.upper() if value and re.fullmatch(r'x[0-9a-fA-F]{6}', value) else value


def with_ancestors(nodes, ancestors=()):
    for node in nodes:
        yield node, ancestors
        yield from with_ancestors(node.children(), ancestors + (node,))


class Audit:
    def __init__(self, mod, game, native=False):
        self.mod, self.game, self.native = mod, game, native
        descriptor = (mod / 'descriptor.mod').read_text(encoding='utf-8-sig')
        metadata = json.loads((mod / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))
        self.replace_paths = [] if native else sorted(set(
            re.findall(r'replace_path\s*=\s*"([^"]+)"', descriptor) +
            metadata.get('game_custom_data', {}).get('replace_paths', [])))
        self.hashes, self.masks, self.errors, self.findings = {}, [], [], []
        self.cache, self.definitions = {}, {}
        self.optional_history_country_scopes = []

    def paths(self, folder):
        local = {} if self.native else {p.relative_to(self.mod).as_posix().casefold(): p
                 for p in (self.mod / folder).rglob('*.txt')}
        replaced = any(folder == x or folder.startswith(x + '/') for x in self.replace_paths)
        native = [] if replaced else [p for p in (self.game / folder).rglob('*.txt')
                  if p.relative_to(self.game).as_posix().casefold() not in local]
        self.masks.extend(p.relative_to(self.mod).as_posix() for p in local.values()
                          if (self.game / p.relative_to(self.mod)).exists())
        return sorted(native + list(local.values()))

    def read(self, path):
        origin = 'native' if path.is_relative_to(self.game) else 'mod'
        rel = origin + '/' + path.relative_to(self.game if origin == 'native' else self.mod).as_posix()
        self.hashes[rel] = sha(path)
        if rel not in self.cache:
            raw = path.read_text(encoding='utf-8-sig')
            try:
                nodes = parse(raw)
            except ValueError as error:
                self.errors.append({'source': rel, 'error': str(error)})
                nodes = []
            self.cache[rel] = (nodes, raw, rel)
        return self.cache[rel]

    def load(self, category, folder):
        pool, explicit = defaultdict(list), defaultdict(list)
        for path in self.paths(folder):
            nodes, raw, rel = self.read(path)
            for n in nodes:
                if not isinstance(n.value, list) or not n.key:
                    continue
                directive, sep, key = n.key.partition(':')
                target = key if sep and directive in ('REPLACE', 'REPLACE_OR_CREATE') else n.key
                (explicit if target != n.key else pool)[target].append((n, rel, raw))
        pool.update(explicit)
        self.definitions[category] = pool
        return pool

    def finding(self, kind, owner, source, target=None, **extra):
        self.findings.append(dict(kind=kind, owner=owner, source=source, target=target, **extra))

    def ref(self, category, target, owner, source, role):
        if target is None:
            return
        if target not in self.definitions[category]:
            self.finding('unresolved_' + category, owner, source, target, role=role)

    def history_country_scope(self, node, source, raw):
        """Keep absent optional history blocks visible without requiring a provider.

        This only classifies the direct c:TAG ?= { ... } form. It does not
        evaluate enclosing guards or suppress other references in the block.
        """
        if not re.fullmatch(r'c:[A-Za-z0-9_]+', node.key):
            return
        target = node.key[2:]
        if (node.op == '?=' and isinstance(node.value, list)
                and target not in self.definitions['countries']):
            self.optional_history_country_scopes.append({
                'target': target, 'source': source, 'operator': node.op,
                'line': raw.count('\n', 0, node.start) + 1,
                'classification': 'absent_optional_country_history_scope',
                'note': 'Direct optional block; not a required provider. '
                        'No engine execution or nested-reference exemption is implied.'})
            return
        self.ref('countries', target, 'history scope', source, 'literal country scope')

    def run(self, pixels=True):
        states = self.load('states', 'map_data/state_regions')
        regions = self.load('regions', 'common/strategic_regions')
        countries = self.load('countries', 'common/country_definitions')
        for cat, folder in [('cultures', 'common/cultures'), ('religions', 'common/religions'),
                            ('traits', 'common/state_traits'), ('buildings', 'common/buildings')]:
            self.load(cat, folder)
        duplicate = {cat: {key: [x[1] for x in values] for key, values in pool.items() if len(values) > 1}
                     for cat, pool in self.definitions.items()}
        numbers, province_states, state_provinces, state_region = defaultdict(list), defaultdict(list), {}, defaultdict(list)
        land, climate = [], {}
        for key, values in states.items():
            if len(values) != 1:
                continue
            n, source, raw = values[0]
            provinces = [color(x) for b in n.children('provinces') for x in bare(b)]
            state_provinces[key] = set(provinces)
            numbers[plain(n.one('id'))].append(key)
            for p in provinces:
                province_states[p].append(key)
            for p, count in Counter(provinces).items():
                if count > 1:
                    self.finding('repeated_province_in_state', key, source, p, count=count)
            is_land = n.one('subsistence_building') is not None
            if is_land:
                land.append(key)
                self.ref('buildings', plain(n.one('subsistence_building')), key, source, 'subsistence building')
            for field in ('city', 'farm', 'mine', 'wood', 'port', 'center_province'):
                target = color(n.one(field))
                if target is not None and target not in state_provinces[key]:
                    self.finding('hub_outside_state', key, source, target, field=field)
            for field in ('prime_land', 'impassable'):
                for b in n.children(field):
                    for target in bare(b):
                        if color(target) not in state_provinces[key]:
                            self.finding('listed_province_outside_state', key, source, color(target), field=field)
            for b in n.children('traits'):
                for target in bare(b):
                    self.ref('traits', target, key, source, 'state trait')
            minimum, maximum = n.one('min_cold_effect'), n.one('max_cold_effect')
            climate[key] = {'minimum': minimum, 'maximum': maximum, 'source': source}
            if minimum is not None or maximum is not None:
                try:
                    low, high = float(minimum or 0), float(maximum or 0)
                    if not 0 <= low <= high <= 1:
                        self.finding('invalid_cold_range', key, source, [minimum, maximum])
                except ValueError:
                    self.finding('nonscalar_cold_range', key, source, [minimum, maximum])
        for number, keys in numbers.items():
            if number is None or len(keys) > 1:
                self.finding('missing_or_duplicate_state_numeric_id', keys, 'state pool', number)
        for p, keys in province_states.items():
            if len(set(keys)) > 1:
                self.finding('province_in_multiple_states', keys, 'state pool', p)
        for key, values in states.items():
            if len(values) == 1:
                n, source, _ = values[0]
                exit_id = plain(n.one('naval_exit_id'))
                if exit_id is not None and exit_id not in numbers:
                    self.finding('unresolved_naval_exit', key, source, exit_id)
        for key, values in regions.items():
            for n, source, _ in values:
                for b in n.children('states'):
                    for target in bare(b):
                        self.ref('states', target, key, source, 'strategic region member')
                        state_region[target].append(key)
        for key in land:
            memberships = state_region[key]
            if len(memberships) != 1:
                self.finding('strategic_region_membership_count', key, states[key][0][1], memberships)
        for key, values in countries.items():
            for n, source, _ in values:
                self.ref('states', plain(n.one('capital')), key, source, 'country capital')
                self.ref('religions', plain(n.one('religion')), key, source, 'country religion')
                for b in n.children('cultures'):
                    for target in bare(b):
                        self.ref('cultures', target, key, source, 'country primary culture')
        allocation, created, owners = defaultdict(list), [], defaultdict(set)
        for path in self.paths('common/history/states'):
            nodes, raw, source = self.read(path)
            for state, ancestors in with_ancestors(nodes):
                if not state.key.startswith('s:STATE_'):
                    continue
                state_id = state.key[2:]
                conditional = [{'block': a.key, 'line': raw.count('\n', 0, a.start) + 1,
                                'limit': raw[a.start:a.end][:2000]}
                               for a in ancestors if a.key in ('if', 'else_if', 'else', 'random_list', 'random')]
                self.ref('states', state_id, 'state history', source, 'history state scope')
                for b in state.children('create_state'):
                    target = plain(b.one('country'))
                    tag = target[2:] if target and target.startswith('c:') else target
                    self.ref('countries', tag, state_id, source, 'initial state owner')
                    provinces = [color(x) for p in b.children('owned_provinces') for x in bare(p)]
                    created.append({'state': state_id, 'country': tag, 'provinces': provinces,
                                    'source': source, 'conditional_ancestors': conditional})
                    owners[tag].add(state_id)
                    for p in provinces:
                        allocation[p].append({'state': state_id, 'country': tag, 'source': source,
                                              'conditional_ancestors': conditional})
                        if p not in state_provinces.get(state_id, set()):
                            self.finding('owned_province_outside_state', state_id, source, p, country=tag)
                for b in state.children('add_homeland'):
                    target = plain(b.value)
                    self.ref('cultures', target[3:] if target and target.startswith('cu:') else target,
                             state_id, source, 'initial homeland')
        for p, assignments in allocation.items():
            if len(assignments) > 1:
                self.finding('multiple_initial_province_allocations', p, 'state history', assignments)
        unallocated = sorted(p for state in land for p in state_provinces[state]
                             if p not in allocation and not any(color(x) == p for block in states[state][0][0].children('impassable') for x in bare(block)))
        startup_refs = []
        for folder in ('common/history/countries', 'common/history/global'):
            for path in self.paths(folder):
                nodes, raw, source = self.read(path)
                for n in walk(nodes):
                    self.history_country_scope(n, source, raw)
                    for target in [n.key, plain(n.value)]:
                        if target and re.fullmatch(r's:STATE_[A-Z0-9_]+', target):
                            self.ref('states', target[2:], 'history', source, 'literal state reference')
                            startup_refs.append({'target': target, 'source': source})
        dlc_rows, native_features, script_findings = [], set(), []
        folders = ('common/history/countries', 'common/history/global', 'common/on_actions',
                   'common/scripted_effects', 'common/scripted_triggers', 'events')
        for folder in folders:
            for path in (self.game / folder).rglob('*.txt'):
                # Native vocabulary is a reference, not a feature-definition schema.
                raw = re.sub(r'#[^\n]*', '', path.read_text(encoding='utf-8-sig'))
                native_features.update(re.findall(r'has_dlc_feature\s*=\s*([A-Za-z0-9_]+)', raw))
            for path in self.paths(folder):
                nodes, raw, source = self.read(path)
                for n in walk(nodes):
                    if n.key in ('has_dlc_feature', 'has_dlc') and isinstance(n.value, str):
                        dlc_rows.append({'feature': plain(n.value), 'operator': n.key, 'source': source,
                                         'line': raw.count('\n', 0, n.start) + 1,
                                         'classification': 'native-vocabulary' if plain(n.value) in native_features else 'unclassified'})
                    for target in (n.key, plain(n.value)):
                        match = re.fullmatch(r'(s|c|cu|rel|sr):([A-Za-z0-9_]+)', target or '')
                        if match:
                            prefix, key = match.groups()
                            category = {'s': 'states', 'c': 'countries', 'cu': 'cultures',
                                        'rel': 'religions', 'sr': 'regions'}[prefix]
                            if key not in self.definitions[category]:
                                script_findings.append({'category': category, 'target': key, 'source': source,
                                                        'line': raw.count('\n', 0, n.start) + 1,
                                                        'note': 'Literal dependency only; optional scope/guard/reachability not evaluated.'})
        pop_candidates = []
        for path in self.paths('common/history/pops'):
            nodes, raw, source = self.read(path)
            for n, ancestors in with_ancestors(nodes):
                if n.key != 'create_pop':
                    continue
                culture = plain(n.one('culture'))
                if culture and culture not in self.definitions['cultures']:
                    pop_candidates.append({'culture': culture, 'authored_size': plain(n.one('size')),
                                           'source': source, 'line': raw.count('\n', 0, n.start) + 1,
                                           'ancestor_scopes': [a.key for a in ancestors],
                                           'note': 'Authored record, not measured in-game population loss.'})
        image_path = (self.mod / 'map_data/provinces.png') if not self.native and (self.mod / 'map_data/provinces.png').exists() else self.game / 'map_data/provinces.png'
        palette = {}
        if pixels:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(image_path) as image:
                colors = image.convert('RGB').getcolors(2**24)
                palette = {'size': list(image.size), 'unique_colors': len(colors), 'source': str(image_path), 'sha256': sha(image_path)}
                available = {f'X{red:02X}{green:02X}{blue:02X}' for count, (red, green, blue) in colors}
            for p, keys in province_states.items():
                if p not in available:
                    self.finding('province_without_map_pixels', keys, 'provinces.png', p)
        for row in dlc_rows:
            row['classification'] = ('native-vocabulary' if row['feature'] in native_features else 'unclassified')
        active_capitals = []
        for tag, holding in owners.items():
            if len(countries.get(tag, [])) == 1:
                capital = plain(countries[tag][0][0].one('capital'))
                if capital is not None and capital not in holding:
                    active_capitals.append({'country': tag, 'definition_capital': capital,
                                            'note': 'Candidate only: country history may override capital.'})
        return {'status': 'FINDINGS_STATIC_ONLY' if self.findings or self.errors else 'PASS_STATIC_ONLY',
                'mode': 'native-control' if self.native else 'effective-mod',
                'counts': {**{cat: len(pool) for cat, pool in self.definitions.items()},
                           'land_states': len(land), 'state_provinces': len(province_states),
                           'created_states': len(created), 'initial_owners': len(owners), 'initial_allocated_provinces': len(allocation)},
                'findings': self.findings, 'finding_counts': dict(Counter(x['kind'] for x in self.findings)),
                'parse_errors': self.errors, 'duplicate_definitions': duplicate,
                'same_path_masks': sorted(set(self.masks)), 'replace_paths': self.replace_paths,
                'unallocated_passable_province_candidates': unallocated, 'active_capital_candidates': active_capitals,
                'palette': palette, 'climate': climate, 'initial_state_allocations': created,
                'dlc_gate_inventory': dlc_rows, 'native_feature_vocabulary': sorted(native_features),
                'script_literal_dependency_candidates': script_findings,
                'optional_history_country_scopes': self.optional_history_country_scopes,
                'initial_pop_culture_candidates': pop_candidates,
                'source_hashes': self.hashes, 'engine_tested': False,
                'limits': ['No reachability evaluation or interpretation of country-history capital overrides.',
                           'DLC inventory records gates, not proof that every consumer is guarded.',
                           'Palette/reference checks do not validate adjacency, raster geometry or engine loading.',
                           'Unallocated and capital candidates require semantic review; no ownership is invented.',
                           'Journal definitions and outcome migration are excluded.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--native', action='store_true')
    p.add_argument('--skip-pixels', action='store_true')
    args = p.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'docs/reports/compatibility'):
        p.error('Output must stay inside compatibility reports.')
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        p.error('Use a new result path; preserve previous evidence.')
    result = Audit(ROOT, GAME, args.native).run(not args.skip_pixels)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'counts', 'finding_counts', 'parse_errors')}, indent=2))


if __name__ == '__main__':
    main()
