"""Read-only phase-one inventory for issue 39; never rewrites gameplay files.

Resolves file masks and replacement directives, retaining ambiguous duplicate
providers instead of inventing a load-order winner. Structural classification
does not evaluate triggers, scopes, DLC availability or engine behavior.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue27_journal_outcomes_audit import fields, signature, LEGACY
sys.path.insert(0, str(ROOT_PATH := Path(__file__).resolve().parents[1]))
from validate_diplomacy_ottoman_1776 import parse, walk

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
FOLDER = 'common/journal_entries'
DIRECTIVES = {'INJECT', 'REPLACE', 'REPLACE_OR_CREATE'}


def read(path):
    return path.read_bytes().decode('utf-8-sig')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provider_map(base, folder, suffix):
    return {p.relative_to(base).as_posix().casefold(): p
            for p in (base / folder).rglob('*' + suffix)}


def inspect_entry(body):
    fs = fields(body)
    legacy = [f.key for f in fs if f.key in LEGACY]
    outcomes, problems = [], []
    for index, outcome in enumerate(f for f in fs if f.key == 'outcome'):
        parts = fields(outcome.body)
        names = Counter(f.key for f in parts)
        flag = next((f for f in parts if f.key == 'flags'), None)
        flags = list(signature(flag.body)) if flag else []
        missing = [k for k in ['conclusion_desc'] if names[k] != 1]
        if 'hidden' not in flags:
            missing += [k for k in ['header', 'effect_header'] if names[k] != 1]
        if 'timeout' not in flags and names['trigger'] != 1:
            missing.append('trigger')
        if 'timeout' in flags and names['trigger']:
            missing.append('timeout_has_trigger')
        if 'invalid_outcome' in flags and 'hidden' not in flags:
            missing.append('visible_invalidation')
        if missing:
            problems.append({'outcome_index': index, 'issues': missing})
        outcomes.append({'index': index, 'flags': flags,
                         'metadata': {f.key: f.value for f in parts
                                      if not f.block and f.key in ['header', 'effect_header', 'conclusion_desc']},
                         'trigger_tokens': list(signature(next((f.body for f in parts if f.key == 'trigger'), ''))),
                         'effect_sha256': hashlib.sha256(json.dumps(list(signature(next((f.body for f in parts if f.key == 'effect'), '')))).encode()).hexdigest()})
    guards = {f.key: list(signature(f.body)) for f in fs
              if f.key in ['possible', 'is_shown_when_inactive', 'complete', 'fail', 'invalid']
              and signature(f.body) in [('always', '=', 'no'), ('always', '=', 'yes')]}
    orphan = [k for k in legacy if k.startswith('on_')
              and k.removeprefix('on_').removesuffix('_all_involved') not in
              [f.key for f in fs]]
    return {'classification': 'LEGACY_CONCLUSION_CONTRACT' if legacy else
            'OUTCOME_METADATA_REVIEW' if problems else
            'OUTCOMES_PRESENT_RUNTIME_UNVERIFIED' if outcomes else
            'NO_OUTCOME_NOT_AUTOMATICALLY_BROKEN',
            'legacy_fields': legacy, 'outcomes': outcomes, 'metadata_problems': problems,
            'constant_guards_for_manual_review': guards, 'orphan_handlers': orphan,
            'timeout': [f.value for f in fs if f.key == 'timeout'],
            'top_level_fields': [f.key for f in fs],
            'context': [f.value for f in fs if f.key == 'context'],
            'dlc_badge': [f.value for f in fs if f.key == 'dlc'],
            'dlc_trigger_mentions': sorted(set(re.findall(r'\bhas_dlc_feature\s*=\s*([\w]+)', ' '.join(signature(body))))),
            'body_token_sha256': hashlib.sha256(json.dumps(list(signature(body))).encode()).hexdigest()}


def inventory(mod=ROOT, game=GAME):
    native, local = provider_map(game, FOLDER, '.txt'), provider_map(mod, FOLDER, '.txt')
    replace_paths = re.findall(r'\breplace_path\s*=\s*"([^"]+)"', read(mod / 'descriptor.mod'))
    excluded = {rel for rel in native if any(rel.startswith(v.strip('/').casefold() + '/') for v in replace_paths)}
    active = {rel: p for rel, p in native.items() if rel not in excluded}
    active.update(local)
    entries, errors, masks, directives = defaultdict(list), [], [], []
    all_hashes = {str(p): sha(p) for p in set(native.values()) | set(local.values())}
    for rel in sorted(set(native) & set(local)):
        old = [f.key for f in fields(read(native[rel])) if f.block]
        new = [f.key.partition(':')[2] if f.key.partition(':')[0] in DIRECTIVES else f.key
               for f in fields(read(local[rel])) if f.block]
        masks.append({'path': rel, 'native_ids': old, 'local_ids': new,
                      'native_ids_absent_from_same_local_file': sorted(set(old) - set(new))})
    for rel, p in sorted(active.items()):
        try:
            raw = read(p)
            for node in fields(raw):
                if not node.block:
                    continue
                prefix, colon, key = node.key.partition(':')
                directive = prefix if colon and prefix in DIRECTIVES else None
                key = key if directive else node.key
                row = dict(id=key, provider=str(p), relative_path=rel,
                           origin='mod' if rel in local else 'native', directive=directive,
                           line=raw.count('\n', 0, node.start) + 1,
                           **inspect_entry(node.body))
                (directives if directive else entries[key]).append(row)
        except (ValueError, UnicodeError) as exc:
            errors.append({'path': str(p), 'error': str(exc)})
    # These directives replace an entire object. INJECT is deliberately left
    # unresolved here: repeated-field merge semantics need their own review.
    replaced = []
    for row in directives:
        key = row['id']
        if row['directive'] in ['REPLACE', 'REPLACE_OR_CREATE']:
            replaced += entries.get(key, [])
            entries[key] = [row]
        else:
            entries[key].append(row)
    duplicates = {k: v for k, v in entries.items() if len(v) != 1}
    resolved = [v[0] for k, v in sorted(entries.items()) if k not in duplicates]
    native_ids = {f.key for p in native.values() for f in fields(read(p)) if f.block}
    missing_native = sorted(native_ids - set(entries))
    # Presence-only localization check: absence from both native and mod is
    # conclusive; presence does not prove the engine's final duplicate winner.
    loc = {}
    for lang in ['english', 'french']:
        available = set()
        for base in [game, mod]:
            for p in (base / 'localization' / lang).rglob('*.yml'):
                available.update(re.findall(r'^\s*([\w.\-]+):(?:\d+)?\s*"', read(p), re.M))
        loc[lang] = available
    for row in resolved:
        keys = {row['id']}
        keys.update(value.strip('"') for outcome in row['outcomes'] for value in outcome['metadata'].values())
        row['localization_keys_absent_from_union'] = {lang: sorted(keys - values) for lang, values in loc.items()}
    counts = Counter(row['classification'] for row in resolved)
    result = {'phase': 'INVENTORY_ONLY_NOT_FULL_SEMANTIC_REVIEW',
              'counts': {'native_files': len(native), 'local_files': len(local), 'effective_files': len(active),
                         'effective_ids': len(entries), 'unambiguous_ids': len(resolved),
                         'same_path_masks': len(masks), 'directives': len(directives),
                         'legacy_fields': sum(len(r['legacy_fields']) for r in resolved),
                         'classifications': dict(counts)},
              'entries': resolved, 'ambiguous_providers': duplicates, 'parse_errors': errors,
              'file_masks': masks, 'directive_replaced_providers': replaced,
              'missing_native_ids': missing_native, 'replace_path_exclusions': sorted(excluded),
              'source_hashes': all_hashes, 'runtime_tested': False,
              'limits': ['No trigger evaluation, effect execution or 1776 activation inference.',
                         'Constant guards are review leads, not an assertion of authored permanent/disabled intent.',
                         'Full scope/dependency/consumer and bilingual localization review remains pending.',
                         'A DLC badge is not an availability gate; mentions do not prove safe DLC-off behavior.',
                         'Missing native IDs may be deliberate historical suppressions; do not restore automatically.']}
    return result


def self_test():
    fixtures = [
        ('legacy', 'complete = { always = yes } on_complete = {}', 'LEGACY_CONCLUSION_CONTRACT'),
        ('visible_missing_headers', 'outcome = { conclusion_desc = x trigger = {} }', 'OUTCOME_METADATA_REVIEW'),
        ('hidden_invalidation', 'outcome = { flags = { hidden invalid_outcome } conclusion_desc = x trigger = {} }', 'OUTCOMES_PRESENT_RUNTIME_UNVERIFIED'),
        ('timeout_with_trigger', 'outcome = { flags = { hidden timeout } conclusion_desc = x trigger = {} }', 'OUTCOME_METADATA_REVIEW'),
        ('empty_is_not_failure', 'possible = { always = no }', 'NO_OUTCOME_NOT_AUTOMATICALLY_BROKEN'),
        ('comments_ignored', '# complete = {}\noutcome = { header = h effect_header = e conclusion_desc = d trigger = {} }', 'OUTCOMES_PRESENT_RUNTIME_UNVERIFIED')]
    return [{'case': name, 'passed': inspect_entry(raw)['classification'] == expected}
            for name, raw, expected in fixtures]


def consumers(ids, mod=ROOT, game=GAME):
    references, errors = [], []
    for folder in ['common', 'events']:
        active = provider_map(game, folder, '.txt')
        active.update(provider_map(mod, folder, '.txt'))
        for rel, path in sorted(active.items()):
            raw = read(path)
            if 'add_journal_entry' not in raw:
                continue
            try:
                for node in walk(parse(raw)):
                    if node.key != 'add_journal_entry':
                        continue
                    key = node.one('type')
                    references.append({'id': key, 'path': str(path),
                                       'line': raw.count('\n', 0, node.start) + 1,
                                       'defined': key in ids,
                                       'parameterized': bool(key and '$' in key),
                                       'origin': 'mod' if path.is_relative_to(mod) else 'native',
                                       'not_a_claim_of_execution': True})
            except (ValueError, UnicodeError) as exc:
                errors.append({'path': str(path), 'error': str(exc)})
    return {'references': references, 'parse_errors': errors,
            'unresolved_literal_ids': {key: [v for v in references if v['id'] == key]
                                       for key in sorted({v['id'] for v in references
                                                          if v['id'] and not v['defined'] and not v['parameterized']})},
            'parameterized_references': [v for v in references if v['parameterized']],
            'limits': 'Static additions, including guarded/unreachable branches; not full dependency closure. The current descriptor only replaces technology folders, without JE additions.'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    result = inventory()
    additions = consumers({row['id'] for row in result['entries']})
    result['consumer_summary'] = {'additions': len(additions['references']),
                                  'unresolved_literal_ids': list(additions['unresolved_literal_ids']),
                                  'parameterized_reference_count': len(additions['parameterized_references']),
                                  'parse_errors': additions['parse_errors']}
    if args.self_test:
        result['self_tests'] = self_test()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    (args.output.parent / 'ADD_JOURNAL_CONSUMERS.json').write_text(json.dumps(additions, indent=2) + '\n', encoding='utf-8')
    with (args.output.parent / 'CATALOGUE.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['id', 'origin', 'path', 'line', 'classification', 'legacy_fields', 'outcomes', 'literal_add_consumers'])
        uses = Counter(v['id'] for v in additions['references'])
        for row in result['entries']:
            writer.writerow([row['id'], row['origin'], row['relative_path'], row['line'], row['classification'],
                             ';'.join(row['legacy_fields']), len(row['outcomes']), uses[row['id']]])
    print(json.dumps({'counts': result['counts'], 'parse_errors': result['parse_errors'],
                      'ambiguous_ids': list(result['ambiguous_providers']),
                      'missing_native_ids': result['missing_native_ids'],
                      'consumer_summary': result['consumer_summary'],
                      'self_tests': result.get('self_tests')}))
    raise SystemExit(bool(result['parse_errors']) or any(not c['passed'] for c in result.get('self_tests', [])))
