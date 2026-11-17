"""Read-only final JE dependency closure and presentation-link review.

Complements the outcome/mapping audits. It never executes a journal or changes
runtime data. Multiple localization providers remain visible, not silently
resolved. A symbol graph is not proof of reachability or scope correctness.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue24_map_dlc_audit import Audit, ROOT, GAME, plain, with_ancestors

CATEGORIES = {
    'journals': 'common/journal_entries', 'buttons': 'common/scripted_buttons',
    'bars': 'common/scripted_progress_bars', 'effects': 'common/scripted_effects',
    'triggers': 'common/scripted_triggers', 'values': 'common/script_values',
    'events': 'events', 'on_actions': 'common/on_actions',
}
PRESENTATION = {
    'header', 'effect_header', 'conclusion_desc', 'reason', 'status_desc',
    'progress_desc', 'activation_description', 'event_outcome_desc',
    'event_outcome_effect_desc', 'event_outcome_activated_effect_desc',
}
# Parameters supplied by the native outcome GUI, not localization-key aliases.
GUI_PARAMETERS = {'EFFECT', 'TIMELEFT_STRING'}


def presentation_keys(obj, key):
    refs = {key}
    if not obj.children('reason'):
        refs.add(key + '_reason')
    for child in obj.children():
        if child.key not in PRESENTATION | {'outcome'}:
            continue
        if isinstance(child.value, str):
            refs.add(plain(child.value))
        else:
            for node, _ in with_ancestors(child.children()):
                if node.key in PRESENTATION | {'desc'} and isinstance(node.value, str):
                    refs.add(plain(node.value))
    for node, _ in with_ancestors(obj.children()):
        if node.key in {'custom_tooltip', 'custom_description'}:
            value = node.one('text') if isinstance(node.value, list) else node.value
            if isinstance(value, str):
                refs.add(plain(value))
    return refs


def localization(language):
    paths = {p.relative_to(GAME).as_posix().casefold(): p
             for p in (GAME / 'localization' / language).rglob('*.yml')}
    paths.update({p.relative_to(ROOT).as_posix().casefold(): p
                  for p in (ROOT / 'localization' / language).rglob('*.yml')})
    keys = defaultdict(list)
    hashes = {}
    for path in paths.values():
        hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        for i, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            match = re.match(r'^\s*([\w.\-]+):(?:\d+)?\s*"(.*)"\s*(?:#.*)?$', line)
            if match:
                keys[match[1]].append({'value': match[2], 'source': str(path), 'line': i})
    return keys, hashes


def follow_localization(refs, keys):
    seen, missing, parameters = set(), [], []
    pending = [(key, None) for key in sorted(refs)]
    while pending:
        key, parent = pending.pop()
        if key in seen:
            continue
        seen.add(key)
        if key not in keys:
            missing.append({'key': key, 'parent': parent})
            continue
        for provider in keys[key]:
            for alias in re.findall(r'\$([^$]+)\$', provider['value']):
                alias = alias.split('|')[0]
                if alias in GUI_PARAMETERS:
                    parameters.append({'key': key, 'parameter': alias})
                else:
                    pending.append((alias, key))
    return {'keys_visited': sorted(seen), 'missing': missing,
            'gui_parameters': parameters,
            'multiple_providers': {k: keys[k] for k in sorted(seen) if len(keys.get(k, [])) > 1}}


def dependency_closure(pools, native_pools):
    helpers = defaultdict(set)
    for category in ['effects', 'triggers', 'values']:
        for key in set(pools[category]) | set(native_pools[category]):
            helpers[key].add(category)
    seen, missing, dynamic, edges = set(), [], [], []
    pending = [('journals', key) for key in pools['journals']]
    while pending:
        category, key = pending.pop()
        if (category, key) in seen:
            continue
        seen.add((category, key))
        for obj, source, raw in pools[category].get(key, []):
            for node, _ in with_ancestors(obj.children()):
                refs = [(cat, node.key) for cat in helpers.get(node.key, [])]
                if node.key in {'scripted_button', 'scripted_progress_bar'}:
                    refs.append(('buttons' if node.key == 'scripted_button' else 'bars', plain(node.value)))
                if node.key == 'trigger_event':
                    if isinstance(node.value, list):
                        if node.one('on_action') is not None:
                            refs.append(('on_actions', plain(node.one('on_action'))))
                        else:
                            refs.append(('events', plain(node.one('id') or node.one('ID'))))
                    else:
                        refs.append(('events', plain(node.value)))
                if node.key in {'events', 'random_events', 'on_actions'} and isinstance(node.value, list):
                    target_category = 'on_actions' if node.key == 'on_actions' else 'events'
                    for child in node.children():
                        value = plain(child.value)
                        if value and not re.fullmatch(r'[0-9.]+', value):
                            refs.append((target_category, value))
                for target_category, target in refs:
                    edge = {'owner_category': category, 'owner': key, 'category': target_category,
                            'target': target, 'source': source, 'line': raw.count('\n', 0, node.start) + 1}
                    if target is None or '$' in target or target.startswith(('scope:', 'var:')):
                        dynamic.append(edge)
                    else:
                        edges.append(edge)
                        if target not in pools[target_category]:
                            missing.append(edge)
                        else:
                            pending.append((target_category, target))
    return {'reachable_counts': dict(Counter(category for category, _ in seen)),
            'reachable': [{'category': c, 'id': k} for c, k in sorted(seen)],
            'edges': edges, 'missing': missing, 'dynamic': dynamic}


def run():
    audit, native = Audit(ROOT, GAME), Audit(ROOT, GAME, native=True)
    pools = {k: audit.load(k, folder) for k, folder in CATEGORIES.items()}
    native_pools = {k: native.load(k, folder) for k, folder in CATEGORIES.items()}
    refs, per_entry = set(), []
    for key, definitions in sorted(pools['journals'].items()):
        for obj, source, raw in definitions:
            keys = presentation_keys(obj, key)
            refs.update(keys)
            per_entry.append({'id': key, 'source': source, 'keys': sorted(keys)})
    localization_results, loc_hashes = {}, {}
    for language in ['french', 'english']:
        keys, hashes = localization(language)
        for key in pools['journals']:
            if any('[' in p['value'] for p in keys.get(key, [])):
                refs.add(key + '_concluded')
        result = follow_localization(refs, keys)
        # Native definition of the English preview has the same bad alias. A
        # mod replace/ key intentionally overrides it; do not treat both as
        # equal effective providers for that one explicitly installed repair.
        effective_keys, overrides = dict(keys), []
        repairs = {'event_effects_utilitarian.1_tt', 'je_sol_invalid_desc', 'grand_exhibition_complete_tt'}
        repair_path = ROOT / 'localization' / language / 'replace' / ('1776_v115_journal_preview_links_l_' + language + '.yml')
        for repair in repairs:
            replacements = [p for p in keys.get(repair, []) if Path(p['source']) == repair_path]
            if len(replacements) == 1:
                effective_keys[repair] = replacements
                overrides.append({'key': repair, 'providers': keys[repair], 'effective': replacements[0]})
        if overrides:
            result = follow_localization(refs, effective_keys)
            result['explicit_overrides'] = overrides
        localization_results[language] = result
        loc_hashes.update(hashes)
    graph = dependency_closure(pools, native_pools)
    ambiguous = {cat: {k: [v[1] for v in ds] for k, ds in pool.items() if len(ds) != 1}
                 for cat, pool in pools.items()}
    failures = len(graph['missing']) + sum(len(v['missing']) for v in localization_results.values())
    return {'status': 'FINDINGS_STATIC_ONLY' if failures or audit.errors or native.errors else 'PASS_STATIC_ONLY',
            'journal_count': len(pools['journals']), 'presentation': localization_results,
            'entries': per_entry, 'dependency_graph': graph, 'ambiguous_providers': ambiguous,
            'parse_errors': audit.errors + native.errors,
            'source_hashes': {**audit.hashes, **native.hashes}, 'localization_hashes': loc_hashes,
            'runtime_tested': False,
            'limits': ['No script execution, trigger truth, GUI rendering or DLC ownership inferred.',
                       'Known helper-symbol edges only, not a full engine trigger/effect type checker.',
                       'Unselected localization duplicates remain candidates; no general load-order winner inferred.',
                       'Dynamic event/helper parameters are recorded, not certified.']}


def self_test():
    # Exercise nested preview extraction and transitive aliases: the former
    # completeness scan did not inspect these links.
    from validate_diplomacy_ottoman_1776 import parse
    obj = parse('test = { outcome = { event_outcome_desc = { first_valid = { triggered_desc = { desc = preview } } } } }')[0]
    assert 'preview' in presentation_keys(obj, 'test')
    keys = {'preview': [{'value': '$nested$ $EFFECT$', 'source': 'fixture', 'line': 1}],
            'nested': [{'value': 'Text', 'source': 'fixture', 'line': 2}]}
    assert not follow_localization({'preview'}, keys)['missing']
    assert follow_localization({'preview'}, {'preview': keys['preview']})['missing'] == [{'key': 'nested', 'parent': 'preview'}]
    assert follow_localization({'absent_preview'}, keys)['missing'][0]['key'] == 'absent_preview'
    assert follow_localization({'preview'}, keys)['gui_parameters'][0]['parameter'] == 'EFFECT'
    return {'checks_passed': 5, 'checks_total': 5, 'engine_tested': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(ROOT / 'docs/reports/compatibility'):
        parser.error('Use a new result under docs/reports/compatibility; preserve old evidence.')
    result = run()
    result['self_tests'] = self_test()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'journals': result['journal_count'],
                      'reachable': result['dependency_graph']['reachable_counts'],
                      'missing_dependencies': len(result['dependency_graph']['missing']),
                      'missing_presentation': {k: v['missing'] for k, v in result['presentation'].items()},
                      'parse_errors': result['parse_errors'], 'self_tests': result['self_tests']}))
