"""Read-only five-site naval modifier audit; no engine validation implied."""
import argparse, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse
LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE30_NAVAL_PROJECTION_2026_11_08'
OLD, NEW = 'ship_interest_gain_mult', 'ship_power_projection_mult'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[?<>!=]+|[^\s{}?<>!=#]+')

def read(path):
    return path.read_bytes().decode('utf-8-sig').replace('\r\n', '\n')

def digest(text):
    ts = [m.group() for m in TOKEN.finditer(text) if not m.group().startswith('#')]
    return hashlib.sha256(json.dumps(ts, ensure_ascii=False).encode()).hexdigest()

def one(nodes, key):
    found = [n for n in nodes if n.key == key]
    if len(found) != 1: raise ValueError(f'{key}: expected one, got {len(found)}')
    return found[0]

def audit(mod=ROOT, replacement=None):
    contract = json.loads(read(LOT / 'CONTRACT.json'))
    checks = []
    def check(name, ok): checks.append({'check': name, 'passed': bool(ok)})
    for path, spec in contract['files'].items():
        text = replacement[path] if replacement and path in replacement else read(mod / path)
        check(path + '.no_removed_key', not re.search(r'\b' + OLD + r'\s*=', text))
        check(path + '.site_count', len(re.findall(r'\b' + NEW + r'\s*=', text)) == len(spec['sites']))
        check(path + '.other_tokens_unchanged', digest(re.sub(r'\b'+NEW+r'\b', OLD, text)) == spec['before_token_hash'])
        try:
            roots = parse(text)
            check(path + '.syntax', True)
            for site in spec['sites']:
                node = one(one(one(roots, site['object']).children(), site['block']).children(), NEW)
                check(site['object'] + '.signed_multiplier', node.op == '=' and node.value == site['value'])
        except ValueError as exc: check(path + '.structure: ' + str(exc), False)
    game = Path(contract['canonical_game'])
    for path, spec in contract['providers'].items():
        effective = mod / path if (mod / path).exists() else game / path
        check(path + '.effective_provider', effective.is_file() and digest(read(effective)) == spec['token_hash'])
    errors = [c for c in checks if not c['passed']]
    return {'status': 'FAIL' if errors else 'PASS_STATIC_ONLY', 'passed': len(checks)-len(errors),
            'total': len(checks), 'errors': errors, 'checks': checks, 'engine_tested': False}

def self_test(mod=ROOT):
    contract = json.loads(read(LOT / 'CONTRACT.json')); results = []
    for path, spec in contract['files'].items():
        text = read(mod / path)
        for site in spec['sites']:
            node = one(one(one(parse(text), site['object']).children(), site['block']).children(), NEW)
            # Changing just this site to flat projection must be rejected.
            bad = text[:node.start] + text[node.start:node.end].replace(NEW, 'ship_power_projection_add', 1) + text[node.end:]
            results.append({'case': site['object'] + '.wrong_additive_unit', 'detected': audit(mod, {path: bad})['status'] == 'FAIL'})
        if 'country_flagship_interest_gain_mult' in text:
            bad = text.replace('country_flagship_interest_gain_mult', 'country_flagship_power_projection_mult', 1)
            results.append({'case': 'unrelated_flagship_modifier_changed', 'detected': audit(mod, {path: bad})['status'] == 'FAIL'})
        if 'law_merchant_navy' in text:
            bad = text.replace(NEW + ' = -0.1', NEW + ' = 0.1', 1)
            results.append({'case': 'merchant_navy_penalty_reversed', 'detected': audit(mod, {path: bad})['status'] == 'FAIL'})
    return results

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mod-root', type=Path, default=ROOT)
    p.add_argument('--self-test', action='store_true')
    p.add_argument('--output', type=Path)
    a = p.parse_args(); result = audit(a.mod_root)
    if a.self_test:
        result['negative_controls'] = self_test(a.mod_root)
        if not all(c['detected'] for c in result['negative_controls']): result['status'] = 'FAIL'
    if a.output: a.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'checks'}, indent=2))
    sys.exit(result['status'] == 'FAIL')
