"""Read-only entry-by-entry 1.15 migration completeness and presentation review.

Uses the current effective providers, including metadata replacement paths.
Records retained native-family omissions separately; does not invent outcomes,
evaluate trigger truth, choose duplicate localization winners or certify GUI.
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
from issue24_map_dlc_audit import Audit, ROOT, GAME, plain, bare, with_ancestors
from issue39_outcome_migration import MOVED

FLAGS = {'hidden', 'timeout', 'invalid_outcome', 'fails_subgoal', 'historical'}
DIRECTIVES = {'REPLACE', 'REPLACE_OR_CREATE', 'INJECT'}


def identity(key):
    prefix, sep, suffix = key.partition(':')
    return suffix if sep and prefix in DIRECTIVES else key


def run(manifest_path):
    audit = Audit(ROOT, GAME)
    journals = audit.load('journals', 'common/journal_entries')
    groups = audit.load('groups', 'common/journal_entry_groups')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    mapped = {identity(p['id']) for spec in manifest['files'].values() for p in spec['entries']}
    localizations, loc_hashes = {}, {}
    for language in ['french', 'english']:
        paths = {p.relative_to(GAME).as_posix().casefold(): p
                 for p in (GAME / 'localization' / language).rglob('*.yml')}
        paths.update({p.relative_to(ROOT).as_posix().casefold(): p
                      for p in (ROOT / 'localization' / language).rglob('*.yml')})
        keys = defaultdict(list)
        for path in paths.values():
            loc_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
            for i, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
                match = re.match(r'^\s*([\w.\-]+):(?:\d+)?\s*"', line)
                if match:
                    keys[match.group(1)].append({'path': str(path), 'line': i})
        localizations[language] = keys
    findings, records, loc_records = [], [], []
    for key, definitions in sorted(journals.items()):
        if len(definitions) != 1:
            findings.append({'journal': key, 'kind': 'ambiguous_provider'})
            continue
        node, source, raw = definitions[0]
        problems = []
        legacy = sorted({n.key for n in node.children()} & MOVED)
        if legacy:
            problems.append({'kind': 'legacy_conclusion_or_presentation_fields', 'fields': legacy})
        context = plain(node.one('context'))
        group = plain(node.one('group'))
        if context is None and len(groups.get(group, [])) == 1:
            context = plain(groups[group][0][0].one('context'))
        outcomes, required = [], {key: 'title'}
        reason = node.children('reason')
        if not reason:
            required[key + '_reason'] = 'default_reason'
        else:
            for field, _ in with_ancestors(reason):
                if field.key == 'desc' and isinstance(field.value, str):
                    required[plain(field.value)] = 'dynamic_reason'
        for index, outcome in enumerate(node.children('outcome')):
            flags = [v for block in outcome.children('flags') for v in bare(block)]
            counts = Counter(n.key for n in outcome.children())
            for field in ['flags', 'header', 'effect_header', 'conclusion_desc', 'trigger', 'effect', 'effect_all_involved']:
                if counts[field] > 1:
                    problems.append({'kind': 'repeated_outcome_field', 'index': index, 'field': field})
            if set(flags) - FLAGS:
                problems.append({'kind': 'unknown_outcome_flags', 'index': index, 'flags': sorted(set(flags) - FLAGS)})
            required_meta = ['conclusion_desc'] + ([] if 'hidden' in flags else ['header', 'effect_header'])
            for field in required_meta:
                value = outcome.one(field)
                if not isinstance(value, str) or not value.strip('"'):
                    problems.append({'kind': 'missing_scalar_outcome_metadata', 'index': index, 'field': field})
            for field in ['conclusion_desc', 'header', 'effect_header']:
                value = outcome.one(field)
                if isinstance(value, str):
                    required[plain(value)] = 'outcome_' + field
            if 'timeout' in flags:
                if counts['trigger']:
                    problems.append({'kind': 'timeout_has_trigger', 'index': index})
            elif counts['trigger'] != 1 or not isinstance(outcome.one('trigger'), list):
                problems.append({'kind': 'missing_non_timeout_trigger', 'index': index})
            if 'invalid_outcome' in flags and 'hidden' not in flags:
                problems.append({'kind': 'visible_invalidation', 'index': index})
            if counts['effect_all_involved'] and context != 'none':
                problems.append({'kind': 'all_involved_wrong_context', 'index': index, 'context': context})
            outcomes.append({'index': index, 'flags': flags, 'has_trigger': bool(counts['trigger']),
                             'trigger_is_literal_always_no': bool(outcome.children('trigger')) and
                             [(n.key, n.op, n.value) for n in outcome.children('trigger')[0].children()] == [('always', '=', 'no')]})
        for flag in ['timeout', 'invalid_outcome']:
            if sum(flag in o['flags'] for o in outcomes) > 1:
                problems.append({'kind': 'multiple_' + flag + '_outcomes'})
        if node.children('timeout') and not any('timeout' in o['flags'] for o in outcomes):
            problems.append({'kind': 'deadline_without_timeout_outcome'})
        loc_problems = []
        for language, keys in localizations.items():
            for name, role in sorted(required.items()):
                if '$' in name or name.startswith(('scope:', '[')):
                    loc_records.append({'journal': key, 'language': language, 'key': name, 'role': role,
                                        'status': 'parameterized_or_dynamic_not_resolved'})
                    continue
                providers = keys.get(name, [])
                status = 'missing' if not providers else 'present' if len(providers) == 1 else 'multiple_key_definitions_no_winner_inferred'
                loc_records.append({'journal': key, 'language': language, 'key': name, 'role': role,
                                    'status': status, 'providers': providers})
                if not providers:
                    loc_problems.append({'kind': 'missing_localization', 'language': language, 'key': name, 'role': role})
        findings.extend(dict(journal=key, source=source, **p) for p in problems + loc_problems)
        records.append({'id': key, 'source': source, 'line': raw.count('\n', 0, node.start) + 1,
                        'mapping_400_member': key in mapped, 'context': context,
                        'group': group, 'outcomes': outcomes, 'authored_no_outcome': not outcomes,
                        'structural_findings': problems, 'localization_findings': loc_problems})
    native = Audit(ROOT, GAME, native=True)
    native_ids = set(native.load('journals', 'common/journal_entries'))
    return {'status': 'FINDINGS_STATIC_ONLY' if findings or audit.errors else 'PASS_STATIC_ONLY',
            'counts': {'journals': len(records), 'outcomes': sum(len(r['outcomes']) for r in records),
                       'mapped_entries_accounted': sum(r['mapping_400_member'] for r in records),
                       'authored_no_outcome': sum(r['authored_no_outcome'] for r in records),
                       'findings': len(findings)},
            'entries': records, 'findings': findings, 'localization_checks': loc_records,
            'mapped_ids_absent_from_effective_catalogue': sorted(mapped - set(journals)),
            'native_ids_absent_from_effective_catalogue': sorted(native_ids - set(journals)),
            'parse_errors': audit.errors + native.errors,
            'source_hashes': {**audit.hashes, **native.hashes}, 'localization_hashes': loc_hashes,
            'schema_source': str(GAME / 'common/journal_entries/journal_entries.md'),
            'schema_sha256': hashlib.sha256((GAME / 'common/journal_entries/journal_entries.md').read_bytes()).hexdigest(),
            'engine_tested': False,
            'limits': ['No trigger truth, scope execution, outcome reachability or GUI appearance is evaluated.',
                       'Missing native families may be deliberate replacements; they are retained for review.',
                       'Multiple localization key definitions do not establish which text the engine displays.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'docs/reports/compatibility') or output.exists():
        parser.error('Use a new compatibility-report result and preserve earlier evidence.')
    result = run(args.manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({'status': result['status'], 'counts': result['counts'],
                      'finding_kinds': dict(Counter(r['kind'] for r in result['findings'])),
                      'missing_mapped_ids': result['mapped_ids_absent_from_effective_catalogue'],
                      'missing_native_ids': result['native_ids_absent_from_effective_catalogue'],
                      'parse_errors': result['parse_errors']}))
