"""Prepare and verify the bounded native dependencies for issue25 AI.

Writes new evidence/candidates only; never installs gameplay files or changes
old journal/event/law definitions. The native social-revolution reward event is
given a separate ID to preserve the authored communist-welfare event.
"""
import argparse
from collections import defaultdict
import copy
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE25_AI_SCOPE_TRIAGE_2026_11_09'
DLOT = LOT / 'dependencies_R2'
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/compatibility')]
from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from issue24_map_dlc_audit import Audit, plain, bare
from issue25_ai_context_audit import sha, write_json

EVENT = 'aor1776_v115_ai_progression.1'
SPECS = [
    ('strategies', 'common/ai_strategies', 'ai_strategy_consolidation_agenda',
     'common/ai_strategies/zz_1776_v115_restored_agendas.txt'),
    ('strategies', 'common/ai_strategies', 'ai_strategy_confrontation_agenda',
     'common/ai_strategies/zz_1776_v115_restored_agendas.txt'),
    ('laws', 'common/laws', 'law_revolutionary_guard',
     'common/laws/zz_1776_v115_revolutionary_guard.txt'),
    ('journals', 'common/journal_entries', 'je_social_revolution',
     'common/journal_entries/zz_1776_v115_social_revolution.txt'),
    ('events', 'events', 'communism.6', 'events/zz_1776_v115_ai_social_revolution.txt'),
    ('movements', 'common/political_movements', 'movement_anti_communist',
     'common/political_movements/zz_1776_v115_anti_communist.txt'),
]
FOLDERS = dict((cat, folder) for cat, folder, key, rel in SPECS)
FOLDERS.update(ideologies='common/ideologies', technologies='common/technology/technologies',
               modifiers='common/static_modifiers', institutions='common/institutions',
               groups='common/interest_groups', movements='common/political_movements',
               triggers='common/scripted_triggers', effects='common/scripted_effects',
               values='common/script_values', journal_groups='common/journal_entry_groups',
               bars='common/scripted_progress_bars',
               movement_categories='common/political_movement_categories',
               support_factors='common/political_movement_pop_support')


def norm(node):
    return json.loads(json.dumps(normalized(node.children())))


def prepare():
    native = Audit(ROOT, GAME, True)
    pools = {cat: native.load(cat, folder) for cat, folder in dict((c, f) for c, f, k, p in SPECS).items()}
    contents, objects = defaultdict(list), []
    for cat, folder, key, rel in SPECS:
        n, source, raw = pools[cat][key][0]
        body = raw[n.start:n.end]
        installed_key = EVENT if cat == 'events' else key
        if cat == 'events':
            body = body.replace('communism.6 = {', EVENT + ' = {', 1)
        if cat == 'journals':
            assert body.count('id = communism.6') == 1
            body = body.replace('id = communism.6', 'id = ' + EVENT, 1)
        parsed = parse(body)[0]
        contents[rel].append(body)
        objects.append({'category': cat, 'id': installed_key, 'native_id': key,
                        'native_source': source, 'native_source_sha256': native.hashes[source],
                        'native_line': raw.count('\n', 0, n.start) + 1,
                        'native_fields': norm(n), 'expected_fields': norm(parsed), 'installed_path': rel})
    files = {}
    for rel, blocks in contents.items():
        prefix = '# Native 1.15 compatibility definitions; issue25 AI dependency closure.\n'
        if rel.startswith('events/'):
            prefix += '# Separate event ID preserves the authored communism.6 reward.\nnamespace = aor1776_v115_ai_progression\n'
        if '/journal_entries/' in rel:
            prefix += '# Native conclusion calls the separate native-reward event; existing journals are preserved.\n'
        text = prefix + '\n' + '\n\n'.join(blocks) + '\n'
        content = text.encode('utf-8-sig')
        path = DLOT / 'candidate' / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(content)
        files[rel] = {'sha256': sha(content), 'bytes': len(content)}
    write_json('dependencies_R2/CONTRACT.json', {'objects': objects, 'files': files,
               'namespace': 'aor1776_v115_ai_progression', 'new_event': EVENT,
               'old_event_preserved': 'communism.6', 'activation_history_write': False})
    print(json.dumps({'candidate_files': files, 'objects': [x['id'] for x in objects]}, indent=2))


def snapshot(candidate=None, override=None):
    a = Audit(ROOT, GAME)
    pools = {cat: a.load(cat, folder) for cat, folder in FOLDERS.items()}
    # Script values can be scalar definitions; generic object loading above
    # intentionally loads blocks only. Include the actual scalar providers.
    for path in a.paths('common/script_values'):
        nodes, raw, source = a.read(path)
        for n in nodes:
            if n.key and not n.key.startswith('@') and isinstance(n.value, str):
                pools['values'][n.key].append((n, source, raw))
    contract = json.loads((DLOT / 'CONTRACT.json').read_text(encoding='utf-8'))
    if candidate:
        for rel in contract['files']:
            cat = next(cat for cat, folder, key, path in SPECS if path == rel)
            for key in list(pools[cat]):
                pools[cat][key] = [row for row in pools[cat][key] if row[1] not in ('mod/' + rel, 'native/' + rel)]
                if not pools[cat][key]:
                    del pools[cat][key]
            text = override.get(rel) if override and rel in override else (candidate / rel).read_text(encoding='utf-8-sig')
            for n in parse(text):
                if n.children():
                    pools[cat][n.key].append((n, 'candidate/' + rel, text))
    loc = {}
    for lang in ('french', 'english'):
        keys = set()
        for base in (GAME, ROOT):
            for p in (base / 'localization' / lang).rglob('*.yml'):
                if base == GAME and (ROOT / p.relative_to(GAME)).exists():
                    continue
                keys.update(re.findall(r'^\s*([^#\s:]+):(?:\d+)?\s*"', p.read_text(encoding='utf-8-sig'), re.M))
        loc[lang] = keys
    return a, pools, loc, contract


def audit(candidate=None, override=None):
    checks, references = [], []
    def check(name, ok):
        checks.append({'check': name, 'pass': bool(ok)})
    try:
        a, pools, loc, contract = snapshot(candidate, override)
    except ValueError as exc:
        return {'status': 'FAIL_STATIC', 'passed': 0, 'total': 1,
                'checks': [{'check': 'syntax: ' + str(exc), 'pass': False}], 'engine_tested': False}
    check('parse_errors', not a.errors)
    def ref(owner, category, key):
        if isinstance(key, str):
            key = key.strip('"')
            if ':' in key:
                key = key.split(':', 1)[1]
            references.append({'owner': owner, 'category': category, 'target': key,
                               'providers': [x[1] for x in pools[category].get(key, [])]})
            check(owner + '.reference.' + category + '.' + key, len(pools[category].get(key, [])) == 1)
    for spec in contract['objects']:
        key, cat = spec['id'], spec['category']
        defs = pools[cat].get(key, [])
        check(key + '.unique_definition', len(defs) == 1)
        if len(defs) != 1:
            continue
        n, source, raw = defs[0]
        check(key + '.exact_native_fields_except_documented_event_id', norm(n) == spec['expected_fields'])
        native_path = GAME / spec['native_source'][7:]
        check(key + '.native_source_unchanged', sha(native_path.read_bytes()) == spec['native_source_sha256'])
        for lang, keys in loc.items():
            if cat in ('strategies', 'laws', 'journals', 'movements'):
                check(key + '.name_' + lang, key in keys)
            if cat == 'movements':
                for suffix in ('_short', '_name'):
                    check(key + '.loc_' + lang + suffix, key + suffix in keys)
            if cat == 'journals':
                check(key + '.reason_' + lang, key + '_reason' in keys)
        for x in walk(n.children()):
            value = plain(x.value)
            if x.key == 'has_strategy': ref(key, 'strategies', value)
            elif x.key in ('has_journal_entry', 'remove_journal_entry'): ref(key, 'journals', value)
            elif x.key in ('has_law_or_variant',): ref(key, 'laws', value)
            elif x.key in ('add_ideology', 'remove_ideology', 'has_ideology'): ref(key, 'ideologies', value)
            elif x.key == 'ideology': ref(key, 'ideologies', value)
            elif x.key == 'character_ideologies':
                for item in bare(x): ref(key, 'ideologies', item)
            elif x.key == 'is_political_movement_type': ref(key, 'movements', value)
            elif x.key == 'create_political_movement': ref(key, 'movements', plain(x.one('type')))
            elif x.key == 'category' and cat == 'movements': ref(key, 'movement_categories', value)
            elif x.key == 'pop_support_factors':
                for item in bare(x): ref(key, 'support_factors', item)
            elif x.key == 'has_modifier': ref(key, 'modifiers', value)
            elif x.key == 'group' and cat == 'journals': ref(key, 'journal_groups', value)
            elif x.key == 'group' and cat == 'laws':
                check(key + '.army_law_group', value == 'lawgroup_army_model')
            elif x.key == 'trigger_event':
                ref(key, 'events', plain(x.one('id')))
            elif x.key == 'add_modifier':
                ref(key, 'modifiers', plain(x.one('name')))
                if isinstance(x.one('days'), str): ref(key, 'values', plain(x.one('days')))
            elif x.key in ('pro_interest_groups', 'anti_interest_groups'):
                for item in bare(x): ref(key, 'groups', item)
            elif x.key in ('pro_movements', 'anti_movements'):
                for item in bare(x): ref(key, 'movements', item)
            elif x.key == 'institution_scores':
                for item in x.children(): ref(key, 'institutions', item.key)
            elif x.key == 'institution': ref(key, 'institutions', value)
            elif x.key == 'unlocking_laws':
                for item in bare(x): ref(key, 'laws', item)
            elif x.key == 'unlocking_technologies':
                for item in bare(x): ref(key, 'technologies', item)
            elif x.key in ('title', 'desc', 'flavor', 'text', 'custom_tooltip', 'name') and value:
                if cat == 'events' or x.key in ('text', 'custom_tooltip'):
                    # Modifier/variable names are identifiers, not localization fields.
                    if value in ('modifier_social_revolution', 'communist_welfare_low_consolidation_months_var'):
                        continue
                    for lang, keys in loc.items(): check(key + '.loc_' + lang + '.' + value, value in keys)
            if x.key in ('icon',) and value and value.startswith('gfx/'):
                check(key + '.icon_exists', (ROOT / value).exists() or (GAME / value).exists())
    for category, keys in [('triggers', ['has_radical_leftist_government', 'ai_has_reasons_to_not_oppose_law',
                    'has_enactment_je_or_law_commitment', 'had_revolutionary_socialism_victory',
                    'has_council_republic_law', 'has_reactionary_ideology', 'has_conservative_ideology',
                    'has_liberal_ideology', 'pressing_liberation_wargoal_against_adjacent_country',
                    'neighboring_country_has_insurrectionary_movement_trigger']),
                ('effects', ['je_social_revolution_cleanup', 'assign_random_revolutionary_ideology',
                    'add_movement_enthusiasm_modifier']),
                ('values', ['state_and_revolution_average_confrontation', 'state_and_revolution_peasant_fraction'])]:
        for key in keys: ref('shared_helpers', category, key)
    for key in ('je_state_and_revolution_political_bar', 'je_state_and_revolution_economic_bar'):
        ref('je_social_revolution', 'bars', key)
    builtin_doc = GAME / 'common/trigger_localization/00_trigger_localization.txt'
    check('native_builtin_approaching_bureaucracy_shortage', bool(re.search(
        r'^approaching_bureaucracy_shortage\s*=\s*\{', builtin_doc.read_text(encoding='utf-8-sig'), re.M)))
    for rel, info in contract['files'].items():
        p = candidate / rel if candidate else ROOT / rel
        if not override or rel not in override:
            check(rel + '.installed_bytes', sha(p.read_bytes()) == info['sha256'])
            check(rel + '.bom', p.read_bytes().startswith(b'\xef\xbb\xbf'))
    errors = [x for x in checks if not x['pass']]
    return {'status': 'PASS_STATIC_ONLY' if not errors else 'FAIL_STATIC',
            'passed': len(checks) - len(errors), 'total': len(checks), 'checks': checks,
            'errors': errors, 'references': references, 'input_hashes': a.hashes,
            'engine_tested': False, 'complete_transitive_dlc_parity': False}


def negatives():
    candidate = DLOT / 'candidate'
    contract = json.loads((DLOT / 'CONTRACT.json').read_text(encoding='utf-8'))
    cases = []
    for spec in contract['objects']:
        rel = spec['installed_path']; raw = (candidate / rel).read_text(encoding='utf-8-sig')
        n = next(x for x in parse(raw) if x.key == spec['id'])
        bad = raw[:n.start] + raw[n.end:]
        r = audit(candidate, {rel: bad})
        cases.append({'case': 'remove_' + spec['id'], 'detected': r['status'] == 'FAIL_STATIC', 'errors': r.get('errors', r['checks'])})
    rel = next(x['installed_path'] for x in contract['objects'] if x['category'] == 'journals')
    raw = (candidate / rel).read_text(encoding='utf-8-sig')
    for name, bad in [('route_to_old_reward', raw.replace('id = ' + EVENT, 'id = communism.6')), ('broken_syntax', raw + '\n}')]:
        r = audit(candidate, {rel: bad})
        cases.append({'case': name, 'detected': r['status'] == 'FAIL_STATIC', 'errors': r.get('errors', r['checks'])})
    return {'detected': sum(x['detected'] for x in cases), 'total': len(cases), 'cases': cases}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepare', action='store_true')
    p.add_argument('--candidate', action='store_true')
    p.add_argument('--negative-controls', action='store_true')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.prepare:
        prepare(); return
    result = audit(DLOT / 'candidate' if args.candidate else None)
    if args.negative_controls: result['negative_controls'] = negatives()
    if args.output:
        dest = args.output.resolve()
        if not dest.is_relative_to(LOT): p.error('Output must stay inside this evidence directory')
        write_json(str(dest.relative_to(LOT)), result)
    print(json.dumps({k: result[k] for k in ('status', 'passed', 'total')}, indent=2))
    print('ERRORS', json.dumps(result.get('errors', []), indent=2))
    if args.negative_controls: print('NEGATIVE',result['negative_controls']['detected'],'/',result['negative_controls']['total'])
    if result['status'] != 'PASS_STATIC_ONLY': raise SystemExit(1)


if __name__ == '__main__': main()
