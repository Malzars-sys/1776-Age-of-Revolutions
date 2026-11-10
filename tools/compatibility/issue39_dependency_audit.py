"""Read-only typed dependency/metadata audit for the full effective JE catalogue.

Checks literal references and records inherited debt separately from changes.
It does not execute triggers, evaluate scope types or certify optional DLC.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue39_journal_catalogue import inspect_entry


def read(path):
    return path.read_bytes().decode('utf-8-sig')


def effective(folder, candidate=None, native_only=False):
    paths = {p.relative_to(GAME).as_posix().casefold(): p for p in (GAME / folder).rglob('*.txt')}
    if not native_only:
        paths.update({p.relative_to(ROOT).as_posix().casefold(): p for p in (ROOT / folder).rglob('*.txt')})
    if candidate:
        paths.update({p.relative_to(candidate).as_posix().casefold(): p for p in (candidate / folder).rglob('*.txt')})
    return paths


def catalogue(folder, candidate=None, native_only=False):
    rows, directives = {}, []
    for rel, path in sorted(effective(folder, candidate, native_only).items()):
        for node in parse(read(path)):
            if not isinstance(node.value, list):
                continue
            if node.key.startswith(('INJECT:', 'REPLACE:', 'REPLACE_OR_CREATE:')):
                directives.append((node.key.partition(':')[2], node, path))
            else:
                rows[node.key] = (node, path)
    for key, node, path in directives:
        # No JE INJECT occurs in this candidate; replacement root identity is
        # sufficient for the typed dependency catalogues inspected here.
        rows[key] = (node, path)
    return rows


def scan(candidate=None, native_only=False):
    journals = catalogue('common/journal_entries', candidate, native_only)
    groups = catalogue('common/journal_entry_groups', candidate, native_only)
    buttons = catalogue('common/scripted_buttons', candidate, native_only)
    bars = catalogue('common/scripted_progress_bars', candidate, native_only)
    events = catalogue('events', candidate, native_only)
    failures, records, parameterized = [], [], []
    def ref(owner, kind, key, values):
        if not isinstance(key, str) or '$' in key or key.startswith('scope:'):
            parameterized.append({'journal': owner, 'kind': kind, 'value': key})
        elif key.strip('"') not in values:
            failures.append({'journal': owner, 'kind': kind, 'value': key})
    loc = {}
    for lang in ['french', 'english']:
        available = set()
        for base in ([GAME] if native_only else [GAME, ROOT]) + ([candidate] if candidate else []):
            for path in (base / 'localization' / lang).rglob('*.yml'):
                available.update(re.findall(r'^\s*([\w.\-]+):(?:\d+)?\s*"', read(path), re.M))
        loc[lang] = available
    for key, (node, path) in sorted(journals.items()):
        raw = read(path)
        body = raw[node.start:node.end]
        # A directive prefix does not affect direct-child inspection.
        data = inspect_entry(body[body.index('{') + 1:body.rfind('}')])
        if data['legacy_fields']:
            failures.append({'journal': key, 'kind': 'legacy_contract', 'value': ','.join(data['legacy_fields'])})
        for problem in data['metadata_problems']:
            failures.append({'journal': key, 'kind': 'outcome_metadata', 'value': json.dumps(problem)})
        for field, values in [('group', groups), ('scripted_button', buttons), ('scripted_progress_bar', bars)]:
            for child in node.children(field):
                ref(key, field, child.value, values)
        for lang, keys in loc.items():
            ref(key, 'name_' + lang, key, keys)
            for outcome in data['outcomes']:
                for field, value in outcome['metadata'].items():
                    ref(key, field + '_' + lang, value, keys)
        for child in walk(node.children()):
            if child.key == 'trigger_event':
                value = child.one('id') if isinstance(child.value, list) else child.value
                ref(key, 'trigger_event', value, events)
            elif child.key == 'add_journal_entry':
                ref(key, 'add_journal_entry', child.one('type'), journals)
            elif child.key in ['has_journal_entry', 'remove_journal_entry', 'has_inactive_journal_entry']:
                ref(key, child.key, child.value, journals)
        context = node.one('context')
        if not context:
            group = groups.get(node.one('group'))
            context = group[0].one('context') if group else None
        all_involved = any(o.children('effect_all_involved') for o in node.children('outcome'))
        if all_involved and context != 'none':
            failures.append({'journal': key, 'kind': 'all_involved_context', 'value': context})
        records.append({'id': key, 'source': str(path), 'outcomes': len(data['outcomes']),
                        'context': context, 'all_involved': all_involved,
                        'classification': data['classification']})
    return {'journals': records, 'findings': failures, 'parameterized_references': parameterized,
            'counts': {'journals': len(records), 'findings': len(failures)},
            'runtime_tested': False, 'scope_type_validation': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--candidate', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--native-only', action='store_true')
    args = ap.parse_args()
    result = scan(args.candidate, native_only=args.native_only)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    groups = defaultdict(list)
    for row in result['findings']:
        groups[row['kind']].append({'journal': row['journal'], 'value': row['value']})
    print(json.dumps({'counts': result['counts'], 'findings_by_kind': {k: len(v) for k, v in groups.items()},
                      'details_except_legacy': {k: v for k, v in groups.items() if k != 'legacy_contract'}}))
