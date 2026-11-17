"""Verify the GUI researchability fast path against the exact legacy predicates.

Read-only; accepts a frozen baseline and its 291-node graph, never starts a game.
The engine meaning of IsResearchable must additionally be verified at runtime.
"""
from pathlib import Path
import argparse
import ast
import json
import re


def predicates(text):
    values = re.findall(r'visible\s*=\s*"\[([^"\r\n]{2000,})\]"', text)
    assert len(values) == 2, 'Expected only the two known compatibility filters'
    return values


def expression(text):
    text = re.sub(
        r"ObjectsEqual\((?:TechTreeLine.GetTargetTech|Technology)\.Self, GetTechnology\('([^']+)'\)\.Self\)",
        r"Eq('\1')", text)
    text = text.replace('Technology.ShouldShow(GetPlayer.Self)', 'Shown')
    text = text.replace('TechTreeLine.GetTargetTech.IsResearchable', 'Researchable')
    text = text.replace('Technology.IsResearchable', 'Researchable')
    return ast.parse(text, mode='eval').body


def evaluate(node, key, shown, researchable):
    if isinstance(node, ast.Name):
        return {'Shown': shown, 'Researchable': researchable}[node.id]
    assert isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    op = node.func.id
    if op == 'Eq':
        return key == ast.literal_eval(node.args[0])
    if op == 'Not':
        assert len(node.args) == 1
        return not evaluate(node.args[0], key, shown, researchable)
    assert len(node.args) == 2
    if op == 'Or':
        return any(evaluate(arg, key, shown, researchable) for arg in node.args)
    assert op == 'And'
    return all(evaluate(arg, key, shown, researchable) for arg in node.args)


def verify(baseline, candidate, graph):
    before = baseline.read_text(encoding='utf-8-sig')
    after = candidate.read_text(encoding='utf-8-sig')
    old, new = predicates(before), predicates(after)
    nodes = json.loads(graph.read_text(encoding='utf-8-sig'))['nodes']
    results = []
    recovered = after
    for i, (left, right) in enumerate(zip(old, new)):
        a, b = expression(left), expression(right)
        cases = [(key, shown) for key in [*nodes, '__unknown_technology__'] for shown in (False, True)]
        failures = [(key, shown) for key, shown in cases if
                    evaluate(a, key, shown, nodes.get(key, {}).get('can_research', 'yes') != 'no') !=
                    evaluate(b, key, shown, nodes.get(key, {}).get('can_research', 'yes') != 'no')]
        assert not failures, failures
        results.append({'filter': ['edges', 'cards'][i], 'cases': len(cases), 'failures': failures})
        assert recovered.count(right) == 1
        recovered = recovered.replace(right, left, 1)
    assert recovered == before, 'Change outside the two expression spans'
    hidden = set(re.findall(r"GetTechnology\('([^']+)'\)", old[0])) - {'joint_stock_companies'}
    assert len(nodes) == 291
    assert sum(len(n['parents']) for n in nodes.values()) == 392
    assert len(hidden) == 40
    assert all(nodes[k]['can_research'] == 'no' for k in hidden)
    # Prove the guard matters: making a blacklisted alias researchable must fail.
    assert any(evaluate(expression(old[0]), k, True, True) !=
               evaluate(expression(new[0]), k, True, True) for k in hidden)
    # Preserve explicit exceptions even when normal ShouldShow is false.
    assert all(evaluate(expression(new[1]), k, False, nodes[k]['can_research'] != 'no')
               for k in ('joint_stock_companies', 'stock_exchange'))
    return {'status': 'PASS_STATIC', 'technology_count': len(nodes),
            'prerequisite_connections': 392, 'hidden_alias_count': len(hidden),
            'only_two_expression_spans_changed': True, 'predicate_comparisons': results,
            'changed_alias_researchability_detected': True,
            'engine_binding_verified': False, 'performance_verified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--graph', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.baseline, args.candidate, args.graph)
    payload = json.dumps(result, indent=2)
    if args.output:
        assert not args.output.exists(), 'Retain previous evidence'
        args.output.write_text(payload, encoding='utf-8')
    print(payload)
