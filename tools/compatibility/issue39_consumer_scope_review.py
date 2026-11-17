"""Read-only effective consumers of literal journal IDs, including je: scopes.

Applies same-path masks and descendant replace_paths before scanning. Optional
missing targets remain findings: optional syntax prevents an invalid scope from
executing but does not reconnect an intended progress effect to an old family.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue24_map_dlc_audit import Audit, ROOT, GAME, plain, with_ancestors


def effective_paths(audit, folder):
    paths = {p.relative_to(GAME).as_posix().casefold(): p
             for p in (GAME / folder).rglob('*.txt')
             if not any(p.relative_to(GAME).as_posix().casefold().startswith(x.casefold().rstrip('/') + '/')
                        for x in audit.replace_paths)}
    paths.update({p.relative_to(ROOT).as_posix().casefold(): p
                  for p in (ROOT / folder).rglob('*.txt')})
    return sorted(paths.values())


def run():
    audit = Audit(ROOT, GAME)
    journals = audit.load('journals', 'common/journal_entries')
    # File-level resolution alone retains replaced native objects in a shared
    # source. Keep those references out of the effective consumer graph.
    object_folders = {
        'common/journal_entries': journals,
        'common/scripted_buttons': audit.load('buttons', 'common/scripted_buttons'),
        'common/scripted_effects': audit.load('effects', 'common/scripted_effects'),
    }
    active_objects = {folder: {(source, node.start) for values in pool.values()
                               for node, source, _ in values}
                      for folder, pool in object_folders.items()}
    references = []
    for folder in ['common', 'events']:
        for path in effective_paths(audit, folder):
            text = path.read_text(encoding='utf-8-sig')
            if 'je:' not in text and 'journal_entry' not in text:
                continue
            nodes, raw, source = audit.read(path)
            for node, ancestors in with_ancestors(nodes):
                root = ancestors[0] if ancestors else node
                if any('/' + folder + '/' in source and
                       (source, root.start) not in active_objects[folder]
                       for folder in active_objects):
                    continue
                targets = []
                if node.key == 'add_journal_entry':
                    targets.append(('add_journal_entry', plain(node.one('type'))))
                elif node.key in {'remove_journal_entry', 'has_journal_entry', 'has_inactive_journal_entry',
                                  'has_active_journal_entry'}:
                    targets.append((node.key, plain(node.value)))
                for position, value in [('key', node.key), ('value', plain(node.value))]:
                    if value and value.startswith('je:'):
                        targets.append(('journal_scope_' + position, value[3:]))
                for kind, target in targets:
                    if not target:
                        continue
                    expression = target
                    # je:ENTRY.var:NAME and je:ENTRY.scripted_bar_progress(...)
                    # select fields on an entry; the suffix is not part of its ID.
                    if kind.startswith('journal_scope_') and '$' not in target:
                        target = next((key for key in sorted(journals, key=len, reverse=True)
                                       if target == key or target.startswith(key + '.')),
                                      target.split('.', 1)[0])
                    parameter = '$' in target or target.startswith(('scope:', 'var:', 'ROOT'))
                    references.append({'id': target, 'kind': kind, 'operator': node.op,
                                       'expression': expression,
                                       'source': source, 'line': raw.count('\n', 0, node.start) + 1,
                                       'root_object': ancestors[0].key if ancestors else node.key,
                                       'ancestry': [n.key for n in ancestors],
                                       'parameterized': parameter,
                                       'defined': target in journals,
                                       'classification': 'dynamic_not_resolved' if parameter else
                                       'resolved_literal' if target in journals else
                                       'optional_missing_literal' if node.op == '?=' else 'missing_literal'})
    unresolved = [r for r in references if not r['defined'] and not r['parameterized']]
    return {'status': 'FINDINGS_STATIC_ONLY' if unresolved or audit.errors else 'PASS_STATIC_ONLY',
            'reference_count': len(references),
            'reference_kind_counts': dict(Counter(r['kind'] for r in references)),
            'unresolved_count': len(unresolved), 'unresolved': unresolved,
            'references': references, 'parse_errors': audit.errors,
            'source_hashes': audit.hashes, 'replace_paths': audit.replace_paths,
            'engine_tested': False,
            'limits': ['Literal provider resolution only; no trigger reachability or scope execution inferred.',
                       'Optional missing targets are retained even where the engine can skip them safely.',
                       'A resolved provider is not proof that progress effects use the correct counter.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'docs/reports/compatibility') or output.exists():
        parser.error('Use a new compatibility-report result.')
    result = run()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({k: result[k] for k in ['status', 'reference_count', 'reference_kind_counts',
                                           'unresolved_count', 'parse_errors']}))
    print(json.dumps(dict(Counter(r['id'] for r in result['unresolved']))))
