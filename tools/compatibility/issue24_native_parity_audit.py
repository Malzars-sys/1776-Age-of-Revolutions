"""Read-only provenance for repeated initial province-owner instructions.

Retains every raw candidate from issue24_residual_scope_audit. Exact native
parity describes the source baseline, not historical correctness, engine order,
or an exemption for a changed condition, owner, state or multiplicity.
"""
import argparse
from collections import Counter, defaultdict
import copy
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue24_map_dlc_audit import Audit, ROOT, GAME, color, plain, with_ancestors
from issue24_residual_scope_audit import run as qualify


def ast(node):
    return [node.key, node.op, [ast(c) for c in node.value]
            if isinstance(node.value, list) else node.value]


def allocations(audit):
    rows = defaultdict(list)
    for path in audit.paths('common/history/states'):
        nodes, raw, source = audit.read(path)
        for node, ancestors in with_ancestors(nodes):
            if node.key != 'create_state':
                continue
            state = [a for a in ancestors if a.key.startswith('s:STATE_')]
            if not state:
                continue
            # Preserve the full enclosing control AST, not just an if/else label.
            controls = [ast(a) for a in ancestors
                        if a.key != 'STATES' and not a.key.startswith('s:STATE_')]
            for block in node.children('owned_provinces'):
                for token in block.children():
                    if token.key or not isinstance(token.value, str):
                        continue
                    rows[color(token.value)].append({
                        'state': state[-1].key[2:],
                        'country': (plain(node.one('country')) or '').removeprefix('c:'),
                        'controls': controls,
                        'operators': [state[-1].op, node.op, block.op],
                        'source': source, 'line': raw.count('\n', 0, token.start) + 1})
    return rows


def signature(rows):
    return [{k: row[k] for k in ('state', 'country', 'controls', 'operators')}
            for row in rows]


def classify(mod, native):
    if any(row['controls'] for row in mod):
        return 'controlled_instructions_require_review'
    if native and signature(mod) == signature(native):
        return 'identical_unconditional_owner_instructions_in_native'
    return 'mod_specific_or_changed_owner_instructions_require_review'


def controls():
    a = dict(state='STATE_A', country='AAA', controls=[], operators=['=', '=', '='])
    b = dict(a, country='BBB')
    native = [a, b]
    variants = [
        ('same pairs and order', copy.deepcopy(native), native, True),
        ('different owner', [a, dict(b, country='CCC')], native, False),
        ('different state', [a, dict(b, state='STATE_B')], native, False),
        ('missing native instruction', native, [], False),
        ('reversed source order', native[::-1], native, False),
        ('different multiplicity', native + [a], native, False),
        ('conditional alternative', [a, dict(b, controls=[['if', '=', []]])], native, False),
        ('different operator', [a, dict(b, operators=['=', '?=', '='])], native, False),
    ]
    results = []
    for name, mod, base, expected in variants:
        actual = classify(mod, base) == 'identical_unconditional_owner_instructions_in_native'
        results.append({'case': name, 'passed': actual == expected})
    assert all(r['passed'] for r in results), results
    return results


def run():
    raw = qualify()
    mod, native = Audit(ROOT, GAME), Audit(ROOT, GAME, native=True)
    mod_rows, native_rows = allocations(mod), allocations(native)
    rows = []
    for candidate in raw['repeated_allocations']:
        province = candidate['province']
        local, baseline = mod_rows[province], native_rows.get(province, [])
        rows.append({'province': province, 'raw_classification': candidate['classification'],
                     'classification': classify(local, baseline),
                     'mod_instructions': local, 'native_instructions': baseline})
    return {'status': 'PROVENANCE_QUALIFIED_STATIC_ONLY',
            'raw_qualification': raw, 'repeated_owner_provenance': rows,
            'provenance_counts': dict(Counter(r['classification'] for r in rows)),
            'parse_errors': mod.errors + native.errors,
            'source_hashes': {**raw['source_hashes'], **mod.hashes, **native.hashes},
            'classification_controls': controls(), 'engine_tested': False,
            'limits': [
                'Exact source parity does not establish historical correctness or runtime behavior.',
                'Sequence is source traversal order; no engine execution winner is inferred.',
                'All raw conflicts, unallocated provinces and capital candidates remain visible.',
                'No owner, population, bitmap or native file is changed by this tool.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'docs/reports/compatibility') or output.exists():
        parser.error('Use a new compatibility-report output; preserve previous evidence.')
    result = run()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({'status': result['status'], 'provenance_counts': result['provenance_counts'],
                      'unallocated': result['raw_qualification']['unallocated_candidates'],
                      'parse_errors': result['parse_errors'],
                      'controls_passed': sum(r['passed'] for r in result['classification_controls'])}))
