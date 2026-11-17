"""Read-only regression check for the exact technology-card/edge visibility contract.

Runs against the supplied checkout (default: this repository). This models GUI
booleans; engine loading, rendering and performance require separate UI tests.
"""
from pathlib import Path
import argparse
import ast
import json
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_diplomacy_ottoman_1776 import parse

HIDDEN = set('''academia admiralty army_reserves artillery banking central_archives
central_banking currency_standards democracy dialectics drydocks empiricism
gunsmithing hydraulic_cranes international_trade law_enforcement line_infantry
mandatory_service mass_communication mechanized_workshops military_drill
napoleonic_warfare navigation power_of_the_purse prospecting psychiatry rationalism
screw_frigate standing_army steelworking tech_bureaucracy triage urban_planning
urbanization enclosure intensive_agriculture manufacturies lathe corporate_charters
pharmaceuticals'''.split())
FORCED = {'joint_stock_companies', 'stock_exchange'}
RETAINED = set('''hydraulic_turbines traditional_glassmaking mysorean_iron_cased_rocketry
explosive_field_ammunition standardized_military_rockets codified_practical_knowledge
sericulture organized_naval_establishments'''.split())


def load_graph(root):
    nodes = {}
    for path in sorted((root / 'common/technology/technologies').glob('*.txt')):
        for node in parse(path.read_text(encoding='utf-8-sig')):
            if not node.key or not isinstance(node.value, list):
                continue
            assert node.key not in nodes, f'Duplicate technology: {node.key}'
            parents = [n.value.strip('"') for b in node.children('unlocking_technologies')
                       for n in b.children() if not n.key and isinstance(n.value, str)]
            nodes[node.key] = {'parents': parents, 'can_research': node.one('can_research', 'yes')}
    return nodes


def compile_predicate(expression):
    text = re.sub(r"GetTechnology\('([a-zA-Z0-9_]+)'\)\.Self", r"'\1'", expression)
    text = text.replace('TechTreeLine.GetTargetTech.Self', 'tech').replace('Technology.Self', 'tech')
    text = text.replace('Technology.ShouldShow(GetPlayer.Self)', 'shown')
    text = text.replace('TechTreeLine.GetTargetTech.IsResearchable', 'researchable')
    text = text.replace('Technology.IsResearchable', 'researchable')
    tree = ast.parse(text, mode='eval')
    names = {'Or', 'And', 'Not', 'ObjectsEqual', 'tech', 'shown', 'researchable'}
    for node in ast.walk(tree):
        assert isinstance(node, (ast.Expression, ast.Call, ast.Name, ast.Load, ast.Constant)), ast.dump(node)
        if isinstance(node, ast.Name):
            assert node.id in names, node.id
        if isinstance(node, ast.Call):
            assert isinstance(node.func, ast.Name) and node.func.id in names - {'tech', 'shown', 'researchable'}
            assert len(node.args) == (1 if node.func.id == 'Not' else 2)
    code = compile(tree, '<technology visibility>', 'eval')
    functions = {'Or': lambda a, b: a or b, 'And': lambda a, b: a and b,
                 'Not': lambda a: not a, 'ObjectsEqual': lambda a, b: a == b}
    return lambda tech, shown, researchable: eval(code, {'__builtins__': {}}, dict(
        functions, tech=tech, shown=shown, researchable=researchable))


def run(root, gui=None):
    nodes = load_graph(root)
    raw = (gui or root / 'gui/tech_tree.gui').read_text(encoding='utf-8-sig')
    assert parse(raw), 'Malformed GUI braces'
    expressions = [t for t in re.findall(r'visible\s*=\s*"\[([^"\r\n]+)\]"', raw) if 'GetTechnology(' in t]
    assert len(expressions) == 2
    edge = next(t for t in expressions if 'TechTreeLine.GetTargetTech.Self' in t)
    card = next(t for t in expressions if 'Technology.ShouldShow' in t)
    assert len(nodes) == 291, f'Technology inventory changed: {len(nodes)}'
    assert sum(len(n['parents']) for n in nodes.values()) == 392
    assert HIDDEN | FORCED <= nodes.keys()
    assert all(nodes[k]['can_research'] == 'no' for k in HIDDEN)
    assert {k for k, n in nodes.items() if n['can_research'] == 'no'} - HIDDEN == RETAINED
    assert all(p in nodes for n in nodes.values() for p in n['parents'])
    cases = [(key, shown) for key in [*nodes, '__unknown_technology__'] for shown in (False, True)]
    tested = 0
    for kind, expression, specification in [
        ('edges', edge, lambda k, shown: k not in HIDDEN),
        ('cards', card, lambda k, shown: k in FORCED or (shown and k not in HIDDEN)),
    ]:
        predicate = compile_predicate(expression)
        researchable = lambda k: nodes.get(k, {}).get('can_research', 'yes') != 'no'
        failures = [(key, shown) for key, shown in cases if predicate(key, shown, researchable(key)) != specification(key, shown)]
        assert not failures, (kind, failures)
        # A real filtering regression must be detected rather than rubber-stamped.
        damaged_key = 'hydraulic_turbines' if 'IsResearchable' in expression else 'academia'
        damaged = compile_predicate(expression.replace("'" + damaged_key + "'", "'__wrong_alias__'", 1))
        assert any(damaged(key, shown, researchable(key)) != specification(key, shown) for key, shown in cases)
        tested += len(cases)
    return {'status': 'PASS_STATIC', 'technologies': len(nodes), 'prerequisite_connections': 392,
            'hidden_compatibility_aliases': len(HIDDEN), 'forced_cards': sorted(FORCED),
            'visibility_cases': tested, 'negative_controls_passed': 2,
            'engine_or_performance_validation': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--gui', type=Path, help='Optional candidate GUI; technology definitions still come from --root')
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.gui), indent=2))
