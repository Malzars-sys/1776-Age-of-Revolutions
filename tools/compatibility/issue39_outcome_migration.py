"""Prepare and audit explicit, per-entry issue39 outcome mappings.

Preparation writes only an evidence/candidate directory. Installation is a
separate, hash-guarded operation; this tool never writes live gameplay files.
Only direct fields assigned in MANIFEST.json are moved. Nested conditions,
effects, descriptions and all-involved scopes are compared independently.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue27_journal_outcomes_audit import fields, signature, LEGACY

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
KINDS = ['complete', 'fail', 'invalid', 'timeout']
PRESENTATION = {
    'complete': {'custom_completion_header': 'header', 'custom_on_completion_header': 'effect_header',
                 'event_outcome_completed_desc': 'event_outcome_desc',
                 'event_outcome_completed_effect_desc': 'event_outcome_effect_desc'},
    'fail': {'custom_failure_header': 'header', 'custom_on_failure_header': 'effect_header',
             'event_outcome_failed_desc': 'event_outcome_desc',
             'event_outcome_failed_effect_desc': 'event_outcome_effect_desc'},
    'invalid': {},
    'timeout': {'event_outcome_timeout_desc': 'event_outcome_desc',
                'event_outcome_timeout_effect_desc': 'event_outcome_effect_desc'},
}
MOVED = LEGACY | {key for mapping in PRESENTATION.values() for key in mapping}
DEFAULTS = {
    'complete': ('je_standard_completion_header', 'je_standard_on_completion_header',
                 'je_standard_completion_conclusion_desc', '"gold_positive"'),
    'fail': ('je_standard_failure_header', 'je_standard_on_failure_header',
             'je_standard_failure_conclusion_desc', '"blue_negative"'),
    'invalid': (None, None, 'je_standard_failure_conclusion_desc', None),
    'timeout': ('JOURNAL_ENTRY_TIMEOUT', 'JOURNAL_ENTRY_ON_TIMEOUT', 'JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC', None),
}


def read(path):
    return path.read_bytes().decode('utf-8-sig')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def payload(field):
    return list(signature(field.body if field.block else field.value))


def single(fs, key):
    matches = [f for f in fs if f.key == key]
    if len(matches) > 1:
        raise ValueError('Ambiguous repeated field: ' + key)
    return matches[0] if matches else None


def entry_plan(root, native=None):
    fs = fields(root.body)
    if not any(f.key in LEGACY for f in fs):
        return None
    if any(f.key == 'outcome' for f in fs):
        raise ValueError('Mixed old/new contract: ' + root.key)
    plans = []
    for kind in KINDS:
        predicate = single(fs, kind) if kind != 'timeout' else None
        effect = single(fs, 'on_' + kind)
        involved = single(fs, 'on_' + kind + '_all_involved')
        duration = single(fs, 'timeout') if kind == 'timeout' else None
        presentation = [f for f in fs if f.key in PRESENTATION[kind]]
        if not (predicate or effect or involved or duration or presentation):
            continue
        if any(f and not f.block for f in [predicate, effect, involved]):
            raise ValueError('Non-block conclusion: ' + root.key + ':' + kind)
        computed_native_match = False
        if duration and duration.block:
            native_duration = single(fields(native.body), 'timeout') if native else None
            computed_native_match = bool(native_duration and signature(duration.value) == signature(native_duration.value))
            if not computed_native_match:
                raise ValueError('Computed duration needs native evidence: ' + root.key)
        for key in PRESENTATION[kind]:
            if key.startswith('custom_'):
                value = single(fs, key)
                if value and value.block:
                    raise ValueError('Dynamic header needs manual mapping: ' + root.key)
        dormant = not predicate and (kind != 'timeout' or not duration)
        flags = ['hidden', 'invalid_outcome'] if kind == 'invalid' else ['timeout'] if kind == 'timeout' else []
        if dormant and 'hidden' not in flags:
            flags.insert(0, 'hidden')
        anchor = predicate.start if predicate else effect.start if effect else involved.start if involved else len(root.body)
        if presentation and not (predicate or effect or involved or duration):
            anchor = presentation[0].start
        plans.append({'kind': kind, 'anchor': anchor, 'dormant': dormant, 'flags': flags,
                      'predicate': predicate.key if predicate else None,
                      'effect': effect.key if effect else None,
                      'effect_all_involved': involved.key if involved else None,
                      'duration_preserved': duration.value if duration else None,
                      'computed_timeout_native_match': computed_native_match,
                      'presentation_mapping': [{'source': f.key, 'target': PRESENTATION[kind][f.key],
                                                'tokens': payload(f)} for f in presentation]})
    plans.sort(key=lambda p: p['anchor'])
    return {'id': root.key, 'outcomes': plans,
            'moved_fields': [{'key': f.key, 'tokens': payload(f)} for f in fs if f.key in MOVED],
            'body_token_sha256_before': digest(json.dumps(list(signature(root.body))).encode())}


def indent_value(value):
    return value.replace('\n', '\n\t')


def render(root, plan, newline):
    fs = fields(root.body)
    out = ['outcome = {']
    kind = plan['kind']
    header, effect_header, conclusion, color = DEFAULTS[kind]
    hidden = 'hidden' in plan['flags']
    if not hidden:
        custom_header = single(fs, 'custom_completion_header' if kind == 'complete' else 'custom_failure_header') if kind in ['complete', 'fail'] else None
        custom_effect = single(fs, 'custom_on_completion_header' if kind == 'complete' else 'custom_on_failure_header') if kind in ['complete', 'fail'] else None
        out += ['\t\theader = ' + (custom_header.value if custom_header else header),
                '\t\teffect_header = ' + (custom_effect.value if custom_effect else effect_header)]
        if color:
            out.append('\t\tcolor = ' + color)
    out.append('\t\tconclusion_desc = ' + conclusion)
    if plan['flags']:
        out.append('\t\tflags = { ' + ' '.join(plan['flags']) + ' }')
    if kind != 'timeout':
        predicate = single(fs, plan['predicate']) if plan['predicate'] else None
        out.append('\t\ttrigger = ' + indent_value(predicate.value).replace('\r\n', '\n') if predicate else '\t\ttrigger = { always = no }')
    for source, target in [(plan['effect'], 'effect'), (plan['effect_all_involved'], 'effect_all_involved')]:
        value = single(fs, source) if source else None
        if value:
            out.append('\t\t' + target + ' = ' + indent_value(value.value).replace('\r\n', '\n'))
        elif target == 'effect':
            out.append('\t\teffect = {}')
    occurrences = Counter()
    for item in plan['presentation_mapping']:
        if item['target'] in ['header', 'effect_header']:
            continue
        # Multiple description blocks are supported and remain in source order.
        originals = [f for f in fs if f.key == item['source']]
        index = occurrences[item['source']]
        occurrences[item['source']] += 1
        out.append('\t\t' + item['target'] + ' = ' + indent_value(originals[index].value).replace('\r\n', '\n'))
    out.append('\t}')
    # Relocated blocks use the native indentation style without introducing
    # tab-only blank lines or carrying trailing whitespace onto changed lines.
    lines = '\n'.join(out).replace('\r\n', '\n').split('\n')
    return newline.join(line.rstrip() for line in lines)


def transform(raw, plans):
    roots = {n.key: n for n in fields(raw) if n.block}
    edits = []
    newline = '\r\n' if '\r\n' in raw else '\n'
    for plan in plans:
        root = roots[plan['id']]
        fs = fields(root.body)
        base = root.end - len(root.value) + 1
        anchors = {p['anchor']: p for p in plan['outcomes']}
        for field in fs:
            if field.key in MOVED:
                replacement = render(root, anchors.pop(field.start), newline) if field.start in anchors else ''
                start, end = base + field.start, base + field.end
                if not replacement:
                    # Remove the empty line left by a relocated field, rather
                    # than leaving its former indentation as trailing tabs.
                    line_start = raw.rfind('\n', 0, start) + 1
                    prefix_is_indent = not raw[line_start:start].strip()
                    while start > line_start and raw[start - 1] in ' \t':
                        start -= 1
                    line_end = raw.find('\n', end)
                    if line_end < 0:
                        line_end = len(raw)
                    if prefix_is_indent and not raw[end:line_end].strip():
                        end = min(line_end + 1, len(raw))
                edits.append((start, end, replacement))
        for anchor, outcome in anchors.items():
            if anchor != len(root.body):
                raise ValueError('Unmapped anchor: ' + plan['id'])
            edits.append((base + anchor, base + anchor, '\t' + render(root, outcome, newline) + newline))
    edits.sort()
    result, cursor, recorded = '', 0, []
    for start, end, replacement in edits:
        if start < cursor:
            raise ValueError('Overlapping edits')
        result += raw[cursor:start]
        after_start = len(result)
        result += replacement
        recorded.append({'before_start': start, 'before_end': end,
                         'after_start': after_start, 'after_end': len(result),
                         'before': raw[start:end], 'after': replacement})
        cursor = end
    return result + raw[cursor:], recorded


def prepare(directory, source_root=ROOT):
    if (directory / 'MANIFEST.json').exists():
        raise ValueError('Preparation already exists; use a new directory')
    manifest = {'phase': 'CANDIDATE_ONLY', 'files': {}, 'blocked': [],
                'engine_tested': False, 'human_accepted': False,
                'native_contract_sha256': digest((GAME / 'common/journal_entries/journal_entries.md').read_bytes())}
    source_root = source_root.resolve()
    for path in sorted((source_root / 'common/journal_entries').glob('*.txt')):
        raw = read(path)
        native_path = GAME / path.relative_to(source_root)
        native_nodes = {n.key: n for n in fields(read(native_path)) if n.block} if native_path.is_file() else {}
        plans = []
        for node in fields(raw):
            if not node.block:
                continue
            try:
                plan = entry_plan(node, native_nodes.get(node.key))
                if plan:
                    plans.append(plan)
            except ValueError as exc:
                manifest['blocked'].append({'file': path.name, 'id': node.key, 'reason': str(exc)})
        if not plans:
            continue
        rel = path.relative_to(source_root)
        before = path.read_bytes()
        after, edits = transform(raw, plans)
        encoded = (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + after.encode('utf-8')
        for folder, content in [('before', before), ('candidate', encoded)]:
            target = directory / folder / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        manifest['files'][rel.as_posix()] = {'before_sha256': digest(before), 'candidate_sha256': digest(encoded),
                                            'bom': before.startswith(b'\xef\xbb\xbf'), 'entries': plans, 'edits': edits}
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def audit_entry(old, new, plan):
    checks = []
    def check(label, ok):
        checks.append({'check': plan['id'] + '.' + label, 'passed': bool(ok)})
    before, after = fields(old.body), fields(new.body)
    unchanged_before = [(f.key, list(signature(f.value))) for f in before if f.key not in MOVED]
    unchanged_after = [(f.key, list(signature(f.value))) for f in after if f.key != 'outcome']
    check('untouched_fields', unchanged_before == unchanged_after)
    check('no_legacy_fields', not any(f.key in MOVED for f in after))
    outcomes = [f for f in after if f.key == 'outcome']
    check('outcome_count', len(outcomes) == len(plan['outcomes']))
    for i, (expected, actual) in enumerate(zip(plan['outcomes'], outcomes)):
        parts = fields(actual.body)
        def get(key):
            return single(parts, key)
        kind = expected['kind']
        prefix = str(i) + '.' + kind + '.'
        flag = get('flags')
        check(prefix + 'flags', (list(signature(flag.body)) if flag else []) == expected['flags'])
        trigger = get('trigger')
        original_trigger = single(before, expected['predicate']) if expected['predicate'] else None
        check(prefix + 'predicate', trigger is None if kind == 'timeout' else
              trigger is not None and list(signature(trigger.body)) ==
              (payload(original_trigger) if original_trigger else ['always', '=', 'no']))
        for source, target in [(expected['effect'], 'effect'), (expected['effect_all_involved'], 'effect_all_involved')]:
            original = single(before, source) if source else None
            installed = get(target)
            check(prefix + target, (payload(installed) if installed else []) == (payload(original) if original else []))
        check(prefix + 'conclusion_desc', get('conclusion_desc') is not None and get('conclusion_desc').value == DEFAULTS[kind][2])
        hidden = 'hidden' in expected['flags']
        for source, target, default in [
                ('custom_completion_header' if kind == 'complete' else 'custom_failure_header', 'header', DEFAULTS[kind][0]),
                ('custom_on_completion_header' if kind == 'complete' else 'custom_on_failure_header', 'effect_header', DEFAULTS[kind][1])]:
            original = single(before, source) if kind in ['complete', 'fail'] else None
            header = get(target)
            check(prefix + target, header is None if hidden else header is not None and header.value == (original.value if original else default))
        check(prefix + 'color', (get('color').value if get('color') else None) == (None if hidden else DEFAULTS[kind][3]))
        for target in ['event_outcome_desc', 'event_outcome_effect_desc']:
            sources = {k for k, v in PRESENTATION[kind].items() if v == target}
            expected_values = [list(signature(f.value)) for f in before if f.key in sources]
            actual_values = [list(signature(f.value)) for f in parts if f.key == target]
            check(prefix + target, expected_values == actual_values)
        allowed = {'header', 'effect_header', 'color', 'conclusion_desc', 'flags', 'trigger', 'effect',
                   'effect_all_involved', 'event_outcome_desc', 'event_outcome_effect_desc'}
        check(prefix + 'no_extra_fields', all(f.key in allowed for f in parts))
    return checks


def audit(directory, live=False, replacements=None, roundtrip=True, only_files=None):
    manifest = json.loads((directory / 'MANIFEST.json').read_text(encoding='utf-8'))
    checks, errors = [], []
    for rel, spec in manifest['files'].items():
        if only_files is not None and rel not in only_files:
            continue
        try:
            old_bytes = (directory / 'before' / rel).read_bytes()
            before = old_bytes.decode('utf-8-sig')
            current = (ROOT if live else directory / 'candidate') / rel
            raw = replacements[rel] if replacements and rel in replacements else read(current)
            old, new = fields(before), fields(raw)
            checks.append({'check': rel + '.root_set_and_order', 'passed': [n.key for n in old] == [n.key for n in new]})
            original = {n.key: n for n in old}
            installed = {n.key: n for n in new}
            mapped = {p['id'] for p in spec['entries']}
            for plan in spec['entries']:
                checks += audit_entry(original[plan['id']], installed[plan['id']], plan)
            for key in set(original) - mapped:
                checks.append({'check': key + '.untouched_entry', 'passed': original[key].value == installed[key].value})
            if roundtrip:
                restored = raw
                for edit in reversed(spec['edits']):
                    if restored[edit['after_start']:edit['after_end']] != edit['after']:
                        raise ValueError('Candidate span changed')
                    restored = restored[:edit['after_start']] + edit['before'] + restored[edit['after_end']:]
                encoded = (b'\xef\xbb\xbf' if spec['bom'] else b'') + restored.encode('utf-8')
                checks.append({'check': rel + '.all_other_bytes_preserved', 'passed': encoded == old_bytes and digest(old_bytes) == spec['before_sha256']})
                checks.append({'check': rel + '.bom_preserved', 'passed': current.read_bytes().startswith(b'\xef\xbb\xbf') == spec['bom']})
        except (ValueError, KeyError, StopIteration) as exc:
            errors.append({'file': rel, 'error': str(exc)})
    failures = [c['check'] for c in checks if not c['passed']]
    return {'status': 'FAIL_STATIC' if failures or errors else 'PASS_STATIC_ONLY',
            'passed': len(checks) - len(failures), 'total': len(checks), 'failures': failures,
            'errors': errors, 'checks': checks, 'engine_tested': False}


def negative_controls(directory):
    from dataclasses import replace
    manifest = json.loads((directory / 'MANIFEST.json').read_text(encoding='utf-8'))
    objects = {}
    for rel, spec in manifest['files'].items():
        old = {n.key: n for n in fields(read(directory / 'before' / rel))}
        new = {n.key: n for n in fields(read(directory / 'candidate' / rel))}
        for plan in spec['entries']:
            objects[plan['id']] = old[plan['id']], new[plan['id']], plan
    results = []
    def run(name, key, mutation, suffix):
        old, new, plan = objects[key]
        try:
            bad = replace(new, body=mutation(new.body))
            failures = [c['check'] for c in audit_entry(old, bad, plan) if not c['passed']]
            detected = any(c.endswith(suffix) for c in failures)
        except ValueError:
            failures, detected = ['parser_or_duplicate_field_error'], suffix == 'syntax'
        results.append({'case': name, 'detected_by_expected_check': detected, 'failures': failures})
    def change(body, outcome_index, field, replacement):
        outcome = [f for f in fields(body) if f.key == 'outcome'][outcome_index]
        target = single(fields(outcome.body), field)
        if not target:
            raise ValueError('Fixture missing field')
        raw = outcome.body[:target.start] + replacement + outcome.body[target.end:]
        return body[:outcome.start] + 'outcome = {' + raw + '}' + body[outcome.end:]
    run('changed_success_predicate', 'je_fr_rev_summon_estates',
        lambda b: change(b, 0, 'trigger', 'trigger = { always = yes }'), '.predicate')
    run('lost_success_reward', 'je_communism_2',
        lambda b: change(b, 0, 'effect', 'effect = {}'), '.effect')
    run('lost_all_involved_scope', 'je_great_eastern_crisis',
        lambda b: change(b, 0, 'effect_all_involved', 'effect_all_involved = {}'), '.effect_all_involved')
    run('visible_invalidation', 'je_great_eastern_crisis',
        lambda b: change(b, 1, 'flags', 'flags = { invalid_outcome }'), '.flags')
    run('timeout_made_conditional', 'je_fr_rev_summon_estates',
        lambda b: b.replace('flags = { timeout }', 'flags = { timeout } trigger = { always = yes }', 1), '.predicate')
    run('deadline_changed', 'je_communism_1',
        lambda b: b.replace('timeout = 1095', 'timeout = 1', 1), '.untouched_fields')
    run('dormant_failure_enabled', 'je_tutorial_expand_basic_building',
        lambda b: b.replace('trigger = { always = no }', 'trigger = { always = yes }', 1), '.predicate')
    # Select an entry with an actual authored header rather than a generic one.
    custom = next(k for k, (_, _, p) in objects.items() if any(
        any(x['target'] == 'header' for x in o['presentation_mapping']) for o in p['outcomes']))
    custom_index = next(i for i, o in enumerate(objects[custom][2]['outcomes']) if any(x['target'] == 'header' for x in o['presentation_mapping']))
    run('custom_header_lost', custom,
        lambda b: change(b, custom_index, 'header', 'header = wrong_header'), '.header')
    run('event_preview_lost', 'je_montenegrin_raiding',
        lambda b: change(b, 2, 'event_outcome_desc', 'event_outcome_desc = {}'), '.event_outcome_desc')
    run('legacy_reintroduced', 'je_communism_2',
        lambda b: b + '\ncomplete = { always = yes }', '.no_legacy_fields')
    run('disabled_chain_reactivated', 'je_peru_bolivia',
        lambda b: b.replace('always = no', 'always = yes', 1), '.untouched_fields')
    run('progress_target_changed', 'je_communism_2',
        lambda b: b.replace('add = 60', 'add = 61', 1), '.untouched_fields')
    run('wrong_journal_scope', 'je_fr_rev_summon_estates',
        lambda b: b.replace('scope:journal_entry', 'scope:target', 1), '.predicate')
    run('broken_braces', 'je_communism_2', lambda b: b + '{', 'syntax')
    return results


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory', type=Path, required=True)
    ap.add_argument('--prepare', action='store_true')
    ap.add_argument('--source-root', type=Path, default=ROOT)
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--negative-controls', action='store_true')
    args = ap.parse_args()
    if args.prepare:
        manifest = prepare(args.directory, source_root=args.source_root)
        print(json.dumps({'files': len(manifest['files']),
                          'entries': sum(len(v['entries']) for v in manifest['files'].values()),
                          'outcomes': sum(len(p['outcomes']) for v in manifest['files'].values() for p in v['entries']),
                          'blocked': manifest['blocked']}))
    result = audit(args.directory, live=args.live)
    if args.negative_controls:
        result['negative_controls'] = negative_controls(args.directory)
    (args.directory / ('LIVE_VALIDATION.json' if args.live else 'CANDIDATE_VALIDATION.json')).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ['checks', 'negative_controls']}))
    if args.negative_controls:
        print(json.dumps({'negative_controls': result['negative_controls']}))
    raise SystemExit(result['status'] != 'PASS_STATIC_ONLY' or any(not n['detected_by_expected_check'] for n in result.get('negative_controls', [])))
