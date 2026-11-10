"""Read-only population/provider checks for issue 40; writes new evidence only.

No gameplay installer, Git writes or native modifications. --candidate overlays
only the five new paths; --baseline captures the live pre-installation state.
"""
import argparse
from collections import Counter, defaultdict
import copy
from decimal import Decimal
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
HERE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09'
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/compatibility'))
from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from issue24_map_dlc_audit import Audit, with_ancestors, bare, plain

IDS = ('north_caucasian', 'siberian')
CULTURES = 'common/cultures/zz_1776_legacy_cultures.txt'
TRAITS = 'common/discrimination_traits/zz_1776_legacy_languages.txt'
GROUPS = 'common/discrimination_trait_groups/zz_1776_legacy_languages.txt'
LOCS = {lang: f'localization/{lang}/1776_legacy_cultures_l_{lang}.yml'
        for lang in ('french', 'english')}
NEW = [CULTURES, TRAITS, GROUPS, *LOCS.values()]
NAME_FIELDS = ('male_common_first_names', 'female_common_first_names',
               'noble_last_names', 'common_last_names')
LANGS = {key: 'aor1776_language_' + key + '_aggregate' for key in IDS}
LANG_GROUPS = {key: 'aor1776_language_group_' + key + '_aggregate' for key in IDS}
EXPECTED_HERITAGE = {'north_caucasian': 'heritage_north_caucasian', 'siberian': 'heritage_siberian'}
MATCH = re.compile(r'(?<![A-Za-z0-9_])(north_caucasian|siberian)(?![A-Za-z0-9_])')
LOC = re.compile(r'^\s*([^#\s:]+):(?:\d+)?\s*"(.*)"\s*(?:#.*)?$')


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode('utf-8')).hexdigest()


def save(path, data):
    path = path.resolve()
    if not path.is_relative_to(HERE):
        raise ValueError('Evidence output must stay inside this mission directory')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def snapshot(candidate=None):
    audit = Audit(ROOT, GAME)
    pools = {}
    for cat, folder in [('cultures', 'common/cultures'),
                        ('traits', 'common/discrimination_traits'),
                        ('groups', 'common/discrimination_trait_groups'),
                        ('religions', 'common/religions'),
                        ('graphics', 'common/culture_graphics'),
                        ('ethnicities', 'common/ethnicities'),
                        ('countries', 'common/country_definitions')]:
        pool = audit.load(cat, folder)
        if candidate and folder in [str(Path(p).parent).replace('\\', '/') for p in NEW[:3]]:
            rel = next(p for p in NEW[:3] if p.startswith(folder + '/'))
            raw = (candidate / rel).read_text(encoding='utf-8-sig')
            for key in list(pool):
                pool[key] = [item for item in pool[key] if item[1] not in ('mod/' + rel, 'native/' + rel)]
                if not pool[key]:
                    del pool[key]
            for node in parse(raw):
                if node.key and node.children():
                    pool[node.key].append((node, 'candidate/' + rel, raw))
        pools[cat] = pool
    cultures = {}
    for key, values in pools['cultures'].items():
        n, source, raw = values[0]
        cultures[key] = {'providers': [v[1] for v in values],
                         'fields': json.loads(json.dumps(normalized(n.children()))),
                         'heritage': plain(n.one('heritage')), 'language': plain(n.one('language')),
                         'traditions': [t for b in n.children('traditions') for t in bare(b)],
                         'religion': plain(n.one('religion')), 'graphics': plain(n.one('graphics')),
                         'ethnicities': [plain(x.value) for b in n.children('ethnicities') for x in b.children()],
                         'names': [x for f in NAME_FIELDS for b in n.children(f) for x in bare(b)],
                         'legacy_traits': bool(n.children('traits'))}
    descriptions = {}
    for cat in ('traits', 'groups'):
        descriptions[cat] = {key: {'providers': [v[1] for v in values],
                                  'type': plain(values[0][0].one('type')),
                                  'group': plain(values[0][0].one('trait_group'))}
                             for key, values in pools[cat].items()}
    legacy = json.loads((HERE / 'LEGACY_PROVENANCE.json').read_text(encoding='utf-8'))
    needed_keys = set(IDS) | set(LANGS.values()) | set(LANG_GROUPS.values())
    for item in legacy['definitions'].values():
        old = parse(item['text'])[0]
        needed_keys.update(x for f in NAME_FIELDS for b in old.children(f) for x in bare(b))
    locs, loc_files = {}, {}
    for lang in LOCS:
        entries = defaultdict(list)
        paths = []
        for origin, base in [('native', GAME), ('mod', ROOT)]:
            for path in (base / 'localization' / lang).rglob('*.yml'):
                rel = path.relative_to(base).as_posix()
                if origin == 'native' and (ROOT / rel).exists():
                    continue
                paths.append((origin + '/' + rel, path))
        if candidate:
            paths = [(source, path) for source, path in paths
                     if source not in ('mod/' + LOCS[lang], 'native/' + LOCS[lang])]
            paths.append(('candidate/' + LOCS[lang], candidate / LOCS[lang]))
        for source, path in paths:
            for line in path.read_text(encoding='utf-8-sig').splitlines():
                match = LOC.match(line)
                if match and match[1] in needed_keys:
                    entries[match[1]].append({'source': source, 'value': match[2]})
                    if source.startswith(('native/', 'mod/')):
                        audit.hashes[source] = digest(path.read_bytes())
        locs[lang] = dict(entries)
        chosen = candidate / LOCS[lang] if candidate else ROOT / LOCS[lang]
        if chosen.exists():
            content = chosen.read_bytes()
            loc_files[lang] = {'bom': content.startswith(b'\xef\xbb\xbf'),
                               'header': content.decode('utf-8-sig').splitlines()[0],
                               'sha256': digest(content)}
    consumers, lexical, errors = [], [], []
    # Scan every effective runtime txt in all script/GUI/map folders, not just
    # the narrower script folders inventoried by #24. Exact matches in ethnicity
    # definitions are listed separately and are never mistaken for culture refs.
    for folder in ('common', 'events', 'map_data', 'gui', 'gfx'):
        for path in audit.paths(folder):
            if path.is_relative_to(GAME):
                native_rel = path.relative_to(GAME).as_posix()
                if any(native_rel.startswith(prefix + '/') for prefix in audit.replace_paths):
                    continue
            raw = path.read_text(encoding='utf-8-sig')
            if not MATCH.search(raw):
                continue
            source = ('native/' + path.relative_to(GAME).as_posix()) if path.is_relative_to(GAME) else ('mod/' + path.relative_to(ROOT).as_posix())
            for line, text in enumerate(raw.splitlines(), 1):
                if MATCH.search(text):
                    lexical.append({'source': source, 'line': line, 'text': text})
            try:
                nodes = parse(raw)
            except ValueError as exc:
                errors.append({'source': source, 'error': str(exc)})
                continue
            for node, ancestors in with_ancestors(nodes):
                value = plain(node.value)
                kind, target = None, None
                if value in ('cu:north_caucasian', 'cu:siberian') or node.key in ('cu:north_caucasian', 'cu:siberian'):
                    target = (value if value and value.startswith('cu:') else node.key)[3:]
                    kind = 'culture_scope'
                elif value in IDS and node.key == 'culture':
                    target, kind = value, 'culture_field'
                elif value in IDS and not node.key and ancestors and ancestors[-1].key == 'cultures':
                    target, kind = value, 'primary_culture'
                if kind:
                    consumers.append({'source': source, 'line': raw.count('\n', 0, node.start) + 1,
                                      'culture': target, 'kind': kind, 'field': node.key,
                                      'scopes': [a.key for a in ancestors]})
    pop_rows, totals, region_totals, owner_totals, cultures_total = [], Counter(), Counter(), Counter(), Counter()
    pop_sources = {}
    all_records = []
    for path in audit.paths('common/history/pops'):
        nodes, raw, source = audit.read(path)
        pop_sources[source] = digest(path.read_bytes())
        for node, ancestors in with_ancestors(nodes):
            if node.key != 'create_pop':
                continue
            state = next((a.key[2:] for a in ancestors if a.key.startswith('s:STATE_')), None)
            owner = next((a.key.split(':', 1)[1] for a in ancestors if a.key.startswith('region_state:')), None)
            size = plain(node.one('size'))
            if size is None:
                raise ValueError(f'Missing pop size: {source}:{node.start}')
            amount = Decimal(size)
            culture = plain(node.one('culture'))
            totals['world'] += amount
            region_totals[state] += amount
            owner_totals[owner] += amount
            cultures_total[culture] += amount
            row = {'source': source, 'line': raw.count('\n', 0, node.start) + 1,
                   'state': state, 'owner': owner, 'culture': culture,
                   'size': size, 'religion': plain(node.one('religion')),
                   'type': plain(node.one('type')), 'scopes': [a.key for a in ancestors],
                   'block_sha256': digest(raw[node.start:node.end])}
            all_records.append(row)
            if culture in IDS:
                pop_rows.append(row)
    country_rows = []
    for key, values in pools['countries'].items():
        n, source, raw = values[0]
        cc = [x for b in n.children('cultures') for x in bare(b)]
        country_rows.append({'country': key, 'cultures': cc, 'source': source,
                             'providers': len(values)})
    initial_tags = set()
    for path in audit.paths('common/history/states'):
        nodes, raw, source = audit.read(path)
        for n in walk(nodes):
            if n.key == 'create_state':
                tag = plain(n.one('country'))
                if tag:
                    initial_tags.add(tag.removeprefix('c:'))
    hashes = {}
    for folder in ('common', 'events', 'localization', 'map_data', 'gui'):
        for p in (ROOT / folder).rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.txt', '.yml', '.gui', '.png'):
                hashes[p.relative_to(ROOT).as_posix()] = digest(p.read_bytes())
    for rel in ('descriptor.mod', '.metadata/metadata.json'):
        hashes[rel] = digest((ROOT / rel).read_bytes())
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, env=env, text=True).strip()
    idx = ROOT / '.git/index'
    return {'cultures': cultures, **descriptions, 'religions': list(pools['religions']),
            'graphics': list(pools['graphics']), 'ethnicities': list(pools['ethnicities']),
            'localizations': locs, 'localization_files': loc_files,
            'consumers': consumers, 'lexical_matches': lexical,
            'parse_errors': audit.errors + errors, 'population_records': pop_rows,
            'all_pop_record_digest': digest(json.dumps(all_records, sort_keys=True)),
            'all_pop_records_count': len(all_records), 'population_sources': pop_sources,
            'authored_world_total': str(totals['world']),
            'authored_state_totals': {k: str(v) for k, v in sorted(region_totals.items())},
            'authored_country_totals': {k: str(v) for k, v in sorted(owner_totals.items())},
            'authored_culture_totals': {k: str(v) for k, v in sorted(cultures_total.items())},
            'countries': country_rows, 'initial_owner_tags': sorted(initial_tags),
            'source_hashes': hashes, 'native_input_hashes': audit.hashes,
            'head': head, 'index_sha256': digest(idx.read_bytes()) if idx.exists() else None,
            'game_version': subprocess.check_output(['powershell', '-NoProfile', '-Command',
                    "(Get-Item -LiteralPath 'C:/Games/Victoria 3/binaries/victoria3.exe').VersionInfo.ProductVersion"], text=True).strip()}


def validate(data, baseline, installed=False):
    checks = []
    def check(name, passed, detail=None):
        checks.append({'check': name, 'pass': bool(passed), 'detail': detail})
    check('no_parse_errors', not data['parse_errors'], data['parse_errors'])
    old = json.loads((HERE / 'LEGACY_PROVENANCE.json').read_text(encoding='utf-8'))
    keep = {'color', 'religion', *NAME_FIELDS, 'graphics', 'ethnicities'}
    for key in IDS:
        culture = data['cultures'].get(key)
        check(key + '.unique_provider', culture and len(culture['providers']) == 1)
        if not culture:
            continue
        before = parse(old['definitions'][key]['text'])[0]
        expected = normalized([n for n in before.children() if n.key in keep])
        actual = [n for n in culture['fields'] if n[0] in keep]
        check(key + '.legacy_payload_preserved', json.dumps(expected) == json.dumps(actual))
        check(key + '.modern_fields_only', not culture['legacy_traits'])
        check(key + '.heritage', culture['heritage'] == EXPECTED_HERITAGE[key])
        check(key + '.language', culture['language'] == LANGS[key])
        check(key + '.traditions', culture['traditions'] == (['tradition_caucasian'] if key == 'north_caucasian' else []))
        for field, kind in [('heritage', 'heritage'), ('language', 'language')]:
            trait = data['traits'].get(culture[field], {})
            group = data['groups'].get(trait.get('group'), {})
            check(key + '.' + field + '_provider', len(trait.get('providers', [])) == 1 and trait.get('type') == kind)
            check(key + '.' + field + '_group', len(group.get('providers', [])) == 1 and group.get('type') == kind)
        check(key + '.aggregate_group', data['traits'].get(LANGS[key], {}).get('group') == LANG_GROUPS[key])
        check(key + '.religion_provider', culture['religion'] in data['religions'])
        check(key + '.graphics_provider', culture['graphics'] in data['graphics'])
        check(key + '.ethnicity_providers', all(e in data['ethnicities'] for e in culture['ethnicities']))
        for lang, locs in data['localizations'].items():
            for name in culture['names']:
                check(key + '.' + lang + '.name.' + name, name in locs)
            for item in (key, LANGS[key], LANG_GROUPS[key]):
                check(key + '.' + lang + '.unique_loc.' + item, len(locs.get(item, [])) == 1)
    for key, culture in data['cultures'].items():
        if key not in IDS:
            check('unrelated_culture_preserved.' + key, culture == baseline['cultures'].get(key))
            check('no_aggregate_language_leak.' + key, culture['language'] not in LANGS.values())
    for lang, row in data['localization_files'].items():
        check('localization_bom.' + lang, row['bom'])
        check('localization_header.' + lang, row['header'] == 'l_' + lang + ':')
    check('two_localization_files', len(data['localization_files']) == 2)
    for row in data['consumers']:
        key = row['culture']
        check('consumer.' + row['source'] + ':' + str(row['line']), len(data['cultures'].get(key, {}).get('providers', [])) == 1)
    check('consumer_inventory_preserved', data['consumers'] == baseline['consumers'])
    for row in data['countries']:
        if row['country'] in data['initial_owner_tags']:
            check('initial_country_cultures.' + row['country'], row['cultures'] and all(c in data['cultures'] and len(data['cultures'][c]['providers']) == 1 for c in row['cultures']))
    for field in ('population_records', 'all_pop_record_digest', 'all_pop_records_count',
                  'population_sources', 'authored_world_total', 'authored_state_totals',
                  'authored_country_totals', 'authored_culture_totals', 'countries',
                  'initial_owner_tags', 'head', 'index_sha256'):
        check('preserved.' + field, data[field] == baseline[field])
    # Every pre-existing file with a typed consumer and every population source
    # is strictly protected. Other concurrent files are reported, never restored.
    protected = {r['source'][4:] for r in baseline['consumers'] if r['source'].startswith('mod/')}
    protected.update(p[4:] for p in baseline['population_sources'] if p.startswith('mod/'))
    protected.update(p for p in baseline['source_hashes'] if p.startswith('common/journal_entries/') or p.startswith('map_data/'))
    for rel in sorted(protected):
        check('protected_source.' + rel, baseline['source_hashes'].get(rel) == data['source_hashes'].get(rel))
    changed = {p: {'before': h, 'after': data['source_hashes'].get(p)} for p, h in baseline['source_hashes'].items() if data['source_hashes'].get(p) != h}
    added = sorted(set(data['source_hashes']) - set(baseline['source_hashes']))
    if installed:
        check('five_new_gameplay_paths', sorted(p for p in added if p in NEW) == sorted(NEW), added)
    return {'status': 'PASS_STATIC_ONLY' if all(c['pass'] for c in checks) else 'FAIL_STATIC',
            'passed': sum(c['pass'] for c in checks), 'total': len(checks), 'checks': checks,
            'changed_preexisting_paths': changed, 'added_runtime_paths': added,
            'concurrent_runtime_additions': [p for p in added if p not in NEW],
            'engine_tested': False, 'human_acceptance': False}


def negative_controls(data, baseline):
    cases = []
    def run(name, mutation, expected):
        broken = copy.deepcopy(data)
        mutation(broken)
        result = validate(broken, baseline)
        failed = [c['check'] for c in result['checks'] if not c['pass']]
        cases.append({'case': name, 'detected': any(expected in x for x in failed), 'failed_checks': failed})
    run('missing culture', lambda d: d['cultures'].pop('siberian'), 'siberian.unique_provider')
    run('duplicate provider', lambda d: d['cultures']['siberian']['providers'].append('fixture'), 'siberian.unique_provider')
    run('old unsupported traits', lambda d: d['cultures']['siberian'].__setitem__('legacy_traits', True), 'siberian.modern_fields_only')
    run('wrong heritage', lambda d: d['cultures']['north_caucasian'].__setitem__('heritage', 'heritage_russian'), 'north_caucasian.heritage')
    run('wrong linguistic family', lambda d: d['traits'][LANGS['siberian']].__setitem__('group', 'language_group_turkic'), 'siberian.aggregate_group')
    run('missing group', lambda d: d['groups'].pop(LANG_GROUPS['siberian']), 'siberian.language_group')
    run('wrong group type', lambda d: d['groups'][LANG_GROUPS['siberian']].__setitem__('type', 'heritage'), 'siberian.language_group')
    run('missing FR name', lambda d: d['localizations']['french'].pop('siberian'), 'french.unique_loc.siberian')
    run('missing English character name', lambda d: d['localizations']['english'].pop('Soferbi'), 'english.name.Soferbi')
    run('invalid graphics', lambda d: d['cultures']['siberian'].__setitem__('graphics', 'missing_graphics'), 'siberian.graphics_provider')
    run('changed pop size', lambda d: d['population_records'][0].__setitem__('size', '1'), 'preserved.population_records')
    run('changed pop religion', lambda d: d['population_records'][0].__setitem__('religion', 'catholic'), 'preserved.population_records')
    run('changed world total', lambda d: d.__setitem__('authored_world_total', '1'), 'preserved.authored_world_total')
    run('removed event consumer', lambda d: d['consumers'].pop(), 'consumer_inventory_preserved')
    run('missing localization BOM', lambda d: d['localization_files']['english'].__setitem__('bom', False), 'localization_bom.english')
    return {'status': 'PASS_NEGATIVE_CONTROLS' if all(c['detected'] for c in cases) else 'FAIL_NEGATIVE_CONTROLS',
            'detected': sum(c['detected'] for c in cases), 'total': len(cases), 'cases': cases}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--baseline', action='store_true')
    p.add_argument('--before', type=Path)
    p.add_argument('--candidate', type=Path)
    p.add_argument('--negative-controls', action='store_true')
    args = p.parse_args()
    if not args.baseline and not args.before:
        p.error('--before is required for validation')
    data = snapshot(args.candidate)
    if args.baseline:
        save(args.output, data)
        print(json.dumps({'mode': 'BASELINE', 'culture_providers': {k: k in data['cultures'] for k in IDS},
                          'consumers': len(data['consumers']), 'affected_pop_records': len(data['population_records']),
                          'authored_affected_totals': {k: data['authored_culture_totals'].get(k) for k in IDS},
                          'authored_world_total': data['authored_world_total'], 'parse_errors': data['parse_errors']}, indent=2))
    else:
        before = json.loads(args.before.read_text(encoding='utf-8'))
        result = validate(data, before, installed=not args.candidate)
        if args.negative_controls:
            result['negative_controls'] = negative_controls(data, before)
        result['snapshot'] = data
        save(args.output, result)
        print(json.dumps({k: result[k] for k in ('status', 'passed', 'total', 'changed_preexisting_paths', 'added_runtime_paths')}, indent=2))
        print('FAILURES:', json.dumps([c for c in result['checks'] if not c['pass']], indent=2))
        if args.negative_controls:
            print('NEGATIVE CONTROLS:', result['negative_controls']['detected'], '/', result['negative_controls']['total'])
        if result['status'] != 'PASS_STATIC_ONLY':
            raise SystemExit(1)


if __name__ == '__main__':
    main()
