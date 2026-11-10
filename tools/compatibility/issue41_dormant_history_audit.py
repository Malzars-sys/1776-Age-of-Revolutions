"""Read-only qualification and regression controls for issue 41.

Reads current providers and retained #24 before/after results. Writes one new
JSON under this mission's evidence directory; never edits runtime or Git files.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, walk, plain, with_ancestors

TARGETS = {'BKH', 'MNL', 'SVN', 'TKI'}
EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE41_DORMANT_HISTORY_2026_11_09'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scope_result(raw, defined=()):
    audit = Audit(ROOT, GAME)
    audit.definitions['countries'] = {key: [] for key in defined}
    for node in walk(parse(raw)):
        audit.history_country_scope(node, 'fixture', raw)
    return audit


def controls():
    cases = [
        ('absent_optional', 'c:BKH ?= { activate_law = law_type:law_serfdom }', (), 0, 1),
        ('absent_required', 'c:BKH = { activate_law = law_type:law_serfdom }', (), 1, 0),
        ('present_optional', 'c:BKH ?= { }', ('BKH',), 0, 0),
        ('present_required', 'c:BKH = { }', ('BKH',), 0, 0),
        ('no_tag_allowlist', 'c:FIXTURE_ONLY ?= { }', (), 0, 1),
        ('scalar_not_exempted', 'c:BKH ?= this', (), 1, 0),
        ('comment_ignored', '# c:BKH ?= { }\nc:TKI = { }', (), 1, 0),
        ('quoted_text_ignored', 'message = "c:BKH ?= { }"', (), 0, 0),
        ('nested_required_retained', 'c:BKH ?= { c:MNL = { } }', (), 1, 1),
        ('two_missing_scopes', 'c:TKI ?= { } c:SVN = { }', (), 1, 1),
    ]
    rows = []
    for name, raw, defined, required, optional in cases:
        result = scope_result(raw, defined)
        actual = (len(result.findings), len(result.optional_history_country_scopes))
        rows.append({'name': name, 'input': raw, 'defined': list(defined),
                     'expected': [required, optional], 'actual': list(actual),
                     'pass': actual == (required, optional)})
    audit = scope_result('c:BKH ?= { country = c:BKH }')
    audit.ref('countries', 'BKH', 'fixture state', 'fixture', 'initial state owner')
    rows.append({'name': 'initial_owner_not_exempted',
                 'pass': len(audit.findings) == 1 and
                         audit.findings[0]['role'] == 'initial state owner'})
    audit = scope_result('\n# line two\nc:BKH ?= { }')
    rows.append({'name': 'source_line_retained',
                 'pass': audit.optional_history_country_scopes[0]['line'] == 3})
    try:
        scope_result('c:BKH ?= {')
    except ValueError:
        rows.append({'name': 'parse_failure_not_suppressed', 'pass': True})
    else:
        rows.append({'name': 'parse_failure_not_suppressed', 'pass': False})
    return rows


def qualify(evidence):
    before = json.loads((evidence / 'MAP_BEFORE.json').read_text(encoding='utf-8'))
    after = json.loads((evidence / 'MAP_AFTER.json').read_text(encoding='utf-8'))
    checks = []

    def check(name, passed, **details):
        checks.append({'name': name, 'pass': bool(passed), **details})

    absent = [r for r in before['findings'] if r['kind'] == 'unresolved_countries']
    optional = after['optional_history_country_scopes']
    check('exact_four_before_findings', {r['target'] for r in absent} == TARGETS and len(absent) == 4)
    check('exact_four_optional_after', {r['target'] for r in optional} == TARGETS and len(optional) == 4)
    remaining = [r for r in before['findings'] if r not in absent]
    check('every_other_finding_retained', remaining == after['findings'])
    check('all_other_audit_payloads_preserved',
          {k: v for k, v in before.items() if k not in {'findings', 'finding_counts', 'optional_history_country_scopes'}} ==
          {k: v for k, v in after.items() if k not in {'findings', 'finding_counts', 'optional_history_country_scopes'}})

    audit = Audit(ROOT, GAME)
    countries = audit.load('countries', 'common/country_definitions')
    check('no_target_country_provider', TARGETS.isdisjoint(countries))
    check('no_target_initial_owner', not any(r['country'] in TARGETS for r in after['initial_state_allocations']))
    check('country_inventory_unchanged', before['counts']['countries'] == after['counts']['countries'] == len(countries))

    originals, counterfactuals = [], []
    for row in optional:
        path = GAME / row['source'].removeprefix('native/')
        raw = path.read_text(encoding='utf-8-sig')
        nodes = [n for n in walk(parse(raw)) if n.key == 'c:' + row['target']]
        check('native_single_optional_block_' + row['target'],
              len(nodes) == 1 and nodes[0].op == '?=' and isinstance(nodes[0].value, list))
        check('no_local_mask_' + row['target'], not (ROOT / path.relative_to(GAME)).exists())
        originals.append({'target': row['target'], 'source': row['source'],
                          'sha256': sha(path), 'script': raw})
        node = copy.deepcopy(nodes[0])
        node.op = '='
        fixture = Audit(ROOT, GAME)
        fixture.definitions['countries'] = countries
        fixture.history_country_scope(node, row['source'], raw)
        counterfactuals.append({'target': row['target'], 'mutated_operator': '=',
                               'findings': fixture.findings,
                               'pass': len(fixture.findings) == 1 and
                                       fixture.findings[0]['target'] == row['target']})

    consumers, source_hashes, parse_errors = [], {}, []
    # Read-only consumers; journal ownership and migration remain outside this task.
    local = {p.relative_to(ROOT).as_posix().casefold(): p
             for folder in ('common', 'events') for p in (ROOT / folder).rglob('*.txt')}
    native = [p for folder in ('common', 'events') for p in (GAME / folder).rglob('*.txt')
              if p.relative_to(GAME).as_posix().casefold() not in local
              and not any(p.relative_to(GAME).as_posix().startswith(x + '/')
                          for x in audit.replace_paths)]
    effective = sorted(p for p in native + list(local.values())
                       if '/journal_entries/' not in p.as_posix())
    literal = re.compile(r'\bc:(?:BKH|MNL|SVN|TKI)\b')
    for path in effective:
            raw = path.read_text(encoding='utf-8-sig')
            if not literal.search(raw):
                continue
            origin = GAME if path.is_relative_to(GAME) else ROOT
            source = ('native/' if origin == GAME else 'mod/') + path.relative_to(origin).as_posix()
            source_hashes[source] = sha(path)
            try:
                nodes = parse(raw)
            except ValueError as error:
                parse_errors.append({'source': source, 'error': str(error)})
                continue
            for node, ancestors in with_ancestors(nodes):
                for position, token in [('key', node.key), ('value', plain(node.value))]:
                    if token and token.startswith('c:') and token[2:] in TARGETS:
                        consumers.append({'target': token[2:], 'source': source,
                                          'line': raw.count('\n', 0, node.start) + 1,
                                          'position': position, 'operator': node.op,
                                          'block': isinstance(node.value, list),
                                          'ancestors': [n.key for n in ancestors]})
    check('consumer_parse_errors_absent', not parse_errors, errors=parse_errors)
    check('exact_four_inherited_history_consumers',
          len([r for r in consumers if '/common/history/' in r['source']]) == 4)
    check('no_local_target_consumers', not any(r['source'].startswith('mod/') for r in consumers))
    fixture_rows = controls()
    check('regression_cases_pass', all(r['pass'] for r in fixture_rows))
    check('four_required_operator_counterfactuals_detected', all(r['pass'] for r in counterfactuals))
    check('audit_source_hashes_still_current', all(
        sha((GAME if source.startswith('native/') else ROOT) / source.split('/', 1)[1]) == digest
        for source, digest in after['source_hashes'].items()))
    return {'status': 'PASS_STATIC_ONLY' if all(r['pass'] for r in checks) else 'FAIL_STATIC',
            'checks': checks, 'passed': sum(r['pass'] for r in checks), 'total': len(checks),
            'regression_cases': fixture_rows, 'required_operator_counterfactuals': counterfactuals,
            'original_native_histories': originals, 'consumers': consumers,
            'consumer_source_hashes': source_hashes, 'engine_tested': False,
            'decision': 'Retain the four optional native histories. Correct only audit classification; '
                        'no runtime file or 1776 starting data is changed.',
            'limitations': ['This is not an engine interpreter or a proof of runtime absence of errors.',
                           'The broader literal dependency inventory remains visible and unchanged.',
                           'Other-country AI, journal and historical semantics are not reviewed here.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new output path inside the issue 41 evidence directory.')
    result = qualify(EVIDENCE)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'passed': result['passed'],
                      'total': result['total'], 'consumers': len(result['consumers']),
                      'failed': [r['name'] for r in result['checks'] if not r['pass']]}))
    return 0 if result['status'] == 'PASS_STATIC_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())
