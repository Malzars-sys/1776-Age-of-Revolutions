"""Read-only, scoped 1.15 toll-treaty audit; --candidate checks staged text.

The small evaluator below checks script arithmetic on synthetic dependencies.
It does not simulate the engine, final diplomatic acceptance or treaty effects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE29_TOLL_TREATIES_2026_11_08'
GAME = Path('C:/Games/Victoria 3/game')
FILES = ('31_toll_exemption.txt', '32_no_tolls.txt')
BLOCKS = ('visible', 'possible', 'ai')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def signature(nodes):
    return [(n.key, n.op, signature(n.value) if isinstance(n.value, list) else n.value) for n in nodes]


def one(nodes, key):
    selected = [n for n in nodes if n.key == key]
    assert len(selected) == 1, (key, len(selected))
    return selected[0]


def masked(text):
    obj = parse(text)[0]
    for n in sorted([one(obj.children(), key) for key in BLOCKS], key=lambda n: n.start, reverse=True):
        text = text[:n.start] + '<SCOPED_BLOCK:' + n.key + '>' + text[n.end:]
    return text


def atom(value, current, env):
    value = str(value).strip('"')
    if value == 'this':
        return current
    if value == 'root':
        return env['root']
    if value.startswith('scope:'):
        return env[value]
    if value == 'define:NDiplomacy|STRAIT_GRIEVANCE_MIN_DEPENDENCE':
        return 5.0
    match = re.fullmatch(r'(strait_trade_dependence_by|strait_toll_grievance_against)\((scope:[a-z_]+)\)', value)
    if match:
        function, target = match.groups()
        data = env['dependence' if function == 'strait_trade_dependence_by' else 'grievance']
        return data[(current, env[target])]
    return float(value)


def condition(nodes, current, env):
    for n in nodes:
        if n.key == 'NOT':
            ok = not condition(n.children(), current, env)
        elif n.key.startswith('scope:') and isinstance(n.value, list):
            ok = condition(n.children(), env[n.key], env)
        elif n.key == 'has_law_or_variant':
            assert n.value == 'law_type:law_free_trade'
            ok = env['free_trade'][current]
        else:
            left, right = atom(n.key, current, env), atom(n.value, current, env)
            ok = {'=': lambda: left == right, '?=': lambda: left == right,
                  '<': lambda: left < right, '>': lambda: left > right}[n.op]()
        if not ok:
            return False
    return True


def evaluate(nodes, current, env, initial=0.0):
    result, previous_if = initial, None
    for n in nodes:
        if n.key in ('desc', 'save_temporary_scope_as'):
            continue
        if n.key == 'if':
            previous_if = condition(one(n.children(), 'limit').children(), current, env)
            if previous_if:
                result = evaluate([x for x in n.children() if x.key != 'limit'], current, env, initial=result)
            continue
        if n.key == 'else':
            assert previous_if is not None
            if not previous_if:
                result = evaluate(n.children(), current, env, initial=result)
            continue
        if n.key.startswith('scope:'):
            result = evaluate(n.children(), env[n.key], env, initial=result)
            continue
        value = evaluate(n.children(), current, env) if isinstance(n.value, list) else atom(n.value, current, env)
        if n.key == 'value':
            result = value
        elif n.key == 'add':
            result += value
        elif n.key == 'multiply':
            result *= value
        elif n.key == 'min':
            result = max(result, value)  # Script min is a lower bound.
        elif n.key == 'max':
            result = min(result, value)  # Script max is an upper bound.
        else:
            raise ValueError('Unsupported arithmetic: ' + n.key)
    return result


def environment(role='S', d=20, reverse=60, grievance=50, free=False):
    return {'root': role, 'scope:source_country': 'S', 'scope:target_country': 'T',
            'dependence': {('T', 'S'): d, ('S', 'T'): reverse},
            'grievance': {('T', 'S'): grievance, ('S', 'S'): grievance},
            'free_trade': {'S': free, 'T': free}}


def inspect_text(name, text, before, native):
    checks, errors = [], []

    def check(label, ok):
        checks.append(label)
        if not ok:
            errors.append(label)

    obj, ref = parse(text)[0], parse(native)[0]
    check('outside three authorized blocks byte-for-byte', masked(text) == masked(before))
    check('no removed link or GDP formula', 'strait_trade_importance_by' not in text and not any(n.key == 'divide' and n.value == 'gdp' for n in walk(obj.children('ai'))))
    for key in BLOCKS:
        check(key + ' matches canonical native AST', signature(obj.children(key)) == signature(ref.children(key)))
    for key in ('visible', 'possible'):
        check(key + ' uses source root, no undefined role scope', not any('scope:source_country' in str(n.value) or 'scope:target_country' in str(n.value) for n in walk(obj.children(key))))

    ai = one(obj.children(), 'ai')
    acceptance = one(ai.children(), 'inherent_accept_score')
    exemption = name.startswith('31_')
    for d in (0, 4.99, 5, 20, 100):
        for reverse in (0, 100):
            for role in ('S', 'T'):
                env = environment(role, d, reverse)
                actual = evaluate(acceptance.children(), role, env)
                if role == 'S':
                    expected = -10 - (min((d + reverse) * 0.125, 25) if exemption else min(d * 0.5, 50))
                else:
                    expected = -10 if d < 5 else min(d * (0.25 if exemption else 0.15), 25 if exemption else 15)
                check(f'acceptance {role}, D(T,S)={d}, D(S,T)={reverse}', abs(actual - expected) < 1e-8)
    for role in ('S', 'T'):
        for free in (False, True):
            for grievance in (0, 50):
                env = environment(role, grievance=grievance, free=free)
                proposal = evaluate(one(ai.children(), 'proposal_weight').children(), role, env)
                favored_law = free != exemption
                expected = 0 if role == 'T' and not favored_law else 1 + grievance * 0.04
                check(f'proposal {role}, free={free}, grievance={grievance}', abs(proposal - expected) < 1e-8)
                goal = evaluate(one(ai.children(), 'wargoal_score_multiplier').children(), role, env)
                expected = 1 + grievance * 0.15 if favored_law and grievance > 0 else 0
                check(f'AI enforcement preference {role}, free={free}, grievance={grievance}', abs(goal - expected) < 1e-8)
    return {'checks': len(checks), 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((EVIDENCE / 'BASELINE.json').read_text(encoding='utf-8'))
    result = {'status': 'PASS_STATIC_ONLY', 'mode': 'candidate' if args.candidate else 'installed',
              'files': {}, 'negative_controls': {}, 'errors': []}
    all_text = {}
    for name in FILES:
        rel = 'common/treaty_articles/' + name
        old_bytes = (EVIDENCE / 'inputs/mod' / name).read_bytes()
        ref_bytes = (EVIDENCE / 'inputs/native' / name).read_bytes()
        assert sha(old_bytes) == manifest['mod'][rel]
        assert sha(ref_bytes) == manifest['native'][rel]
        assert sha((GAME / rel).read_bytes()) == manifest['native'][rel], 'Native reference changed: ' + rel
        path = EVIDENCE / 'inputs/mod' / (name + '.candidate') if args.candidate else ROOT / rel
        text, old, native = path.read_bytes().decode('utf-8-sig'), old_bytes.decode('utf-8-sig'), ref_bytes.decode('utf-8-sig')
        all_text[name] = (text, old, native)
        audit = inspect_text(name, text, old, native)
        result['files'][name] = audit | {'sha256': sha(path.read_bytes()), 'baseline_legacy_links': old.count('strait_trade_importance_by')}
        result['errors'] += [name + ': ' + e for e in audit['errors']]
        try:
            rejected = bool(inspect_text(name, old, old, native)['errors'])
        except (ValueError, AssertionError):
            rejected = True
        result['negative_controls'][name + ': legacy baseline rejected'] = rejected
    name = FILES[0]
    text, old, native = all_text[name]
    mutations = {
        'obsolete link restored': text.replace('strait_trade_dependence_by', 'strait_trade_importance_by', 1),
        'dependence direction reversed': text.replace('strait_trade_dependence_by(scope:source_country)', 'strait_trade_dependence_by(scope:target_country)', 1),
        'controller score sign reversed': text.replace('multiply = -0.25', 'multiply = 0.25', 1),
        'dependence threshold branch corrupted': text.replace('STRAIT_GRIEVANCE_MIN_DEPENDENCE', 'STRAIT_GRIEVANCE_INVALID', 1),
        'undefined visibility scope': text.replace('has_any_strait_province_in_hierarchy = yes', 'has_any_strait_province_in_hierarchy = scope:source_country', 1),
        'historical prerequisite changed': text.replace('commercial_insurance_markets', 'international_relations', 1),
        'war-goal execution priority changed': text.replace('execution_priority = 21', 'execution_priority = 22', 1),
        'free-trade preference inverted': text.replace('NOT = { has_law_or_variant = law_type:law_free_trade }', 'has_law_or_variant = law_type:law_free_trade', 1),
    }
    for label, mutated in mutations.items():
        assert mutated != text, label
        try:
            detected = bool(inspect_text(name, mutated, old, native)['errors'])
        except (ValueError, AssertionError, KeyError):
            detected = True
        result['negative_controls'][label] = detected
    result['protected_files_checked'] = len(manifest['protected'])
    result['concurrent_changes'] = [rel for rel, digest in manifest['protected'].items() if not (ROOT / rel).is_file() or sha((ROOT / rel).read_bytes()) != digest]
    result['errors'] += [label for label, detected in result['negative_controls'].items() if not detected]
    if result['errors']:
        result['status'] = 'FAIL_STATIC'
    result['checks_passed'] = sum(row['checks'] - len(row['errors']) for row in result['files'].values())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
