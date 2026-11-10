"""Read-only qualification of residual allocation/capital candidates.

Keeps ownership conflicts and guarded alternatives visible. Does not select a
historical owner, simulate history order or infer the winner of duplicate writes.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue24_map_dlc_audit import Audit, ROOT, GAME, with_ancestors, plain, color


def classify_allocations(rows):
    if any(row['guards'] for row in rows):
        return 'guarded_repeated_allocation_requires_review'
    pairs = {(row['state'], row['country']) for row in rows}
    if len(pairs) > 1:
        return 'conflicting_unconditional_owner_instructions'
    if len({(row['source'], row['list_start']) for row in rows}) == 1:
        return 'same_owner_duplicate_token_in_one_list'
    return 'repeated_same_owner_across_blocks_requires_review'


def qualify_capital(default, owned, explicit):
    capital = explicit[-1]['target'] if explicit else default
    if capital in owned:
        return 'consistent_explicit_history_capital' if explicit else 'consistent_default_capital'
    return 'unowned_capital_requires_review'


def self_test():
    row = dict(state='STATE_A', country='AAA', source='fixture', list_start=10, guards=[])
    cases = [
        ('same list repetition', classify_allocations([row, dict(row)]) == 'same_owner_duplicate_token_in_one_list'),
        ('conflicting owner preserved', classify_allocations([row, dict(row, country='BBB')]) == 'conflicting_unconditional_owner_instructions'),
        ('different state preserved', classify_allocations([row, dict(row, state='STATE_B')]) == 'conflicting_unconditional_owner_instructions'),
        ('guard does not become acceptance', classify_allocations([row, dict(row, guards=['if'])]) == 'guarded_repeated_allocation_requires_review'),
        ('two same-owner blocks not auto-deduplicated', classify_allocations([row, dict(row, list_start=20)]) == 'repeated_same_owner_across_blocks_requires_review'),
        ('owned default', qualify_capital('STATE_A', {'STATE_A'}, []) == 'consistent_default_capital'),
        ('owned explicit override', qualify_capital('STATE_B', {'STATE_A'}, [dict(target='STATE_A')]) == 'consistent_explicit_history_capital'),
        ('bad override retained', qualify_capital('STATE_A', {'STATE_A'}, [dict(target='STATE_B')]) == 'unowned_capital_requires_review'),
    ]
    assert all(ok for _, ok in cases), cases
    return [{'case': name, 'passed': ok} for name, ok in cases]


def run():
    audit = Audit(ROOT, GAME)
    countries = audit.load('countries', 'common/country_definitions')
    states = audit.load('states', 'map_data/state_regions')
    allocations, holdings, explicit = defaultdict(list), defaultdict(set), defaultdict(list)
    guarded_capitals = []
    for path in audit.paths('common/history/states'):
        nodes, raw, source = audit.read(path)
        for n, ancestors in with_ancestors(nodes):
            if n.key != 'create_state':
                continue
            state_nodes = [a for a in ancestors if a.key.startswith('s:STATE_')]
            if not state_nodes:
                continue
            state = state_nodes[-1].key[2:]
            country = (plain(n.one('country')) or '').removeprefix('c:')
            guards = [a.key for a in ancestors if a.key in {'if', 'else_if', 'else', 'random', 'random_list'}]
            for block in n.children('owned_provinces'):
                for token in block.children():
                    if token.key or not isinstance(token.value, str):
                        continue
                    province = color(token.value)
                    allocations[province].append(dict(state=state, country=country, source=source,
                        line=raw.count('\n', 0, token.start)+1, token_start=token.start,
                        list_start=block.start, guards=guards))
                    if not guards:
                        holdings[country].add(state)
    for path in audit.paths('common/history/countries'):
        nodes, raw, source = audit.read(path)
        for n, ancestors in with_ancestors(nodes):
            if not n.key.startswith('c:') or not isinstance(n.value, list):
                continue
            tag = n.key[2:]
            for field, parents in with_ancestors(n.children()):
                if field.key != 'set_capital':
                    continue
                row = dict(target=plain(field.value), source=source, line=raw.count('\n', 0, field.start)+1)
                if parents or any(a.key not in {'COUNTRIES'} for a in ancestors):
                    guarded_capitals.append(dict(country=tag, **row))
                else:
                    explicit[tag].append(row)
    capitals = []
    for tag, owned in sorted(holdings.items()):
        definitions = countries.get(tag, [])
        if len(definitions) != 1:
            continue
        node, source, raw = definitions[0]
        default = plain(node.one('capital'))
        history = explicit[tag]
        capitals.append(dict(country=tag, default=default, definition_source=source,
            owned_states=sorted(owned), direct_history_overrides=history,
            selected_in_this_model=history[-1]['target'] if history else default,
            classification=qualify_capital(default, owned, history)))
    repeated = [dict(province=p, classification=classify_allocations(rows), occurrences=rows)
                for p, rows in sorted(allocations.items()) if len(rows)>1]
    unallocated = []
    for key, definitions in states.items():
        if len(definitions) != 1:
            continue
        node, source, raw = definitions[0]
        if node.one('subsistence_building') is None:
            continue
        impassable = {color(x.value) for b in node.children('impassable') for x in b.children() if not x.key}
        for block in node.children('provinces'):
            for token in block.children():
                p=color(token.value)
                if not token.key and p not in allocations and p not in impassable:
                    unallocated.append(dict(province=p, state=key, source=source,
                        classification='unallocated_passable_province_requires_historical_review'))
    return dict(status='QUALIFIED_STATIC_ONLY', repeated_allocations=repeated,
        repeated_classification_counts=dict(Counter(r['classification'] for r in repeated)),
        capitals=capitals, capital_classification_counts=dict(Counter(r['classification'] for r in capitals)),
        guarded_capital_instructions=guarded_capitals, unallocated_candidates=unallocated,
        parse_errors=audit.errors, source_hashes=audit.hashes, engine_tested=False,
        limits=['Direct literal history instructions only; helper/dynamic capital effects are not evaluated.',
                'No execution-order winner inferred from conflicting ownership instructions.',
                'No historical capital, border or owner selected by this tool.'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(ROOT/'docs/reports/compatibility') or output.exists():
        parser.error('Use a new path inside compatibility reports; preserve old evidence.')
    result=run()
    if args.self_test:result['classification_controls']=self_test()
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:result[k] for k in ['status','repeated_classification_counts','capital_classification_counts','unallocated_candidates','parse_errors']},ensure_ascii=False))


if __name__=='__main__':main()
