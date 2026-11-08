"""Read-only issue 32 audit; --self-test mutates text only in memory.

Checks exact native rule adoption and preservation of every unrelated token.
This does not run the game or simulate the engine's occupation/peace behavior.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE32_WAR_GOALS_2026_11_08'
FILES = tuple('common/war_goal_types/' + n for n in
              ('00_annex_country.txt', '03_conquer_state.txt', '27_unification.txt'))
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[?<>!=]+|[^\s{}?<>!=#]+')


def read(path):
    return path.read_bytes().decode('utf-8-sig').replace('\r\n', '\n')


def tokens(text):
    return [m.group() for m in TOKEN.finditer(text) if not m.group().startswith('#')]


def digest(text):
    return hashlib.sha256(json.dumps(tokens(text), ensure_ascii=False).encode()).hexdigest()


def one(nodes, key):
    found = [n for n in nodes if n.key == key]
    if len(found) != 1:
        raise ValueError(f'Expected one {key}; found {len(found)}')
    return found[0]


def mask(text):
    roots = parse(text)
    if len(roots) != 1:
        raise ValueError('Expected exactly one war goal')
    for n in sorted([n for n in roots[0].children() if n.key in
                     ('infamy', 'mirrored_wargoal')], key=lambda n: n.start, reverse=True):
        text = text[:n.start] + text[n.end:]
    return digest(text)


def audit(mod=ROOT, replacements=None):
    contract = json.loads(read(LOT / 'CONTRACT.json'))
    checks = []

    def check(name, condition):
        checks.append({'check': name, 'passed': bool(condition)})

    for path in FILES:
        text = replacements[path] if replacements and path in replacements else read(mod / path)
        expected = contract['files'][path]
        try:
            roots = parse(text)
            check(path + '.one_goal', len(roots) == 1)
            goal = one(roots, expected['goal'])
            infamy = one(goal.children(), 'infamy')
            mirror = one(goal.children(), 'mirrored_wargoal')
            check(path + '.preserved_rules', mask(text) == expected['preserved_token_hash'])
            check(path + '.current_infamy', tokens(text[infamy.start:infamy.end]) == expected['infamy_tokens'])
            check(path + '.native_territorial_mirror', tokens(text[mirror.start:mirror.end]) == expected['mirror_tokens'])
            check(path + '.no_legacy_infamy_scaling', not any(n.value in
                  ('define:NDiplomacy|WAR_GOAL_INFAMY_POPULATION_SCALING_FACTOR',
                   'define:NDiplomacy|WAR_GOAL_INFAMY_POPULATION_SCALING_MULTIPLIER',
                   'define:NDiplomacy|WAR_GOAL_INFAMY_POPULATION_SCALING_MULTIPLIER_MAX_TOTAL',
                   'define:NDiplomacy|WAR_GOAL_INFAMY_POPULATION_SCALING_MULTIPLIER_MAX_PER_STATE')
                  for n in walk(infamy.children()) if isinstance(n.value, str)))
        except (ValueError, StopIteration) as exc:
            check(path + '.structure: ' + str(exc), False)

    # Resolve the actual file provider: a same-path mod mask must not silently
    # hide the new native formulas, values, or trigger.
    game = Path(contract['canonical_game'])
    for path, source in contract['native_dependencies'].items():
        effective = mod / path if (mod / path).exists() else game / path
        check(path + '.effective_provider', effective.is_file())
        if effective.is_file():
            data = read(effective)
            check(path + '.effective_token_contract', digest(data) == source['token_hash'])
            names = [n.key for n in parse(data)]
            for key in source['required_keys']:
                check(path + '.' + key, names.count(key) == 1)

    failed = [c for c in checks if not c['passed']]
    return {'status': 'FAIL' if failed else 'PASS_STATIC_ONLY', 'passed': len(checks)-len(failed),
            'total': len(checks), 'errors': failed, 'checks': checks,
            'engine_tested': False, 'human_accepted': False}


def self_test(mod=ROOT):
    texts = {p: read(mod / p) for p in FILES}
    cases = []
    for path in FILES:
        cases.append((path + '.missing_mirror', path, texts[path].replace(
            '\tmirrored_wargoal = {\n\t\tmethod = territorial\n\t}\n', '', 1)))
        cases.append((path + '.wrong_mirror_method', path, texts[path].replace(
            'method = territorial', 'method = no_mirror', 1)))
    cases.extend([
        ('annex.wrong_infamy_scope', FILES[0], texts[FILES[0]].replace('add = country_infamy_value', 'add = state_infamy_value', 1)),
        ('conquer.wrong_infamy_scope', FILES[1], texts[FILES[1]].replace('add = state_infamy_value', 'add = country_infamy_value', 1)),
        ('conquer.missing_claim_guard', FILES[1], texts[FILES[1]].replace('save_temporary_scope_as = infamy_ignores_claim', '', 1)),
        ('conquer.missing_imperial_factor', FILES[1], texts[FILES[1]].replace('add = scope:target_state.modifier:state_aor1776_imperial_conquest_infamy_mult', 'add = 0', 1)),
        ('annex.removed_hre_guard', FILES[0], texts[FILES[0]].replace('aor1776_hre_any_native_bond = no', 'always = yes', 1)),
        ('unification.changed_priority', FILES[2], texts[FILES[2]].replace('execution_priority = 200', 'execution_priority = 80', 1)),
    ])
    results = []
    for name, path, changed in cases:
        if changed == texts[path]:
            raise ValueError('Negative control did not mutate: ' + name)
        results.append({'case': name, 'detected': audit(mod, {path: changed})['status'] == 'FAIL'})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mod-root', type=Path, default=ROOT)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.mod_root)
    if args.self_test:
        result['negative_controls'] = self_test(args.mod_root)
        if not all(c['detected'] for c in result['negative_controls']):
            result['status'] = 'FAIL'
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
    sys.exit(result['status'] == 'FAIL')
