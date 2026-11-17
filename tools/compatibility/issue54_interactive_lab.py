"""Prepare isolated UI trials and a semantics-checked diagnostic GUI copy.

No game launch, input injection, startup benchmark, normal-profile edit or
technology change. The supported desktop controller supplies UI input later.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import collections
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111')
OUT = LAB / 'runtime_ui_controlled'
REPORT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE54_INTERACTIVE_2026_11_11'
NORMAL = ROOT.parent.parent
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/binaries/victoria3.exe')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def balanced(parts):
    if len(parts) == 1:
        return parts[0]
    split = len(parts) // 2
    return 'Or(' + balanced(parts[:split]) + ', ' + balanced(parts[split:]) + ')'


def evaluator(expression):
    text = expression.strip('[]')
    text = text.replace('Technology.ShouldShow(GetPlayer.Self)', 'shown')
    text = re.sub(r"GetTechnology\('([a-zA-Z0-9_]+)'\)\.Self", r"'\1'", text)
    text = text.replace('TechTreeLine.GetTargetTech.Self', 'tech').replace('Technology.Self', 'tech')
    tree = ast.parse(text, mode='eval')
    allowed_names = {'Or', 'And', 'Not', 'ObjectsEqual', 'tech', 'shown'}
    for node in ast.walk(tree):
        assert isinstance(node, (ast.Expression, ast.Call, ast.Name, ast.Load, ast.Constant)), ast.dump(node)
        if isinstance(node, ast.Name):
            assert node.id in allowed_names, node.id
        if isinstance(node, ast.Call):
            assert isinstance(node.func, ast.Name) and node.func.id in {'Or', 'And', 'Not', 'ObjectsEqual'}
    code = compile(tree, '<visibility predicate>', 'eval')
    functions = {'Or': lambda a, b: a or b, 'And': lambda a, b: a and b,
                 'Not': lambda a: not a, 'ObjectsEqual': lambda a, b: a == b}
    return lambda tech, shown: eval(code, {'__builtins__': {}}, dict(functions, tech=tech, shown=shown))


def main():
    assert not OUT.exists(), 'Retain earlier UI trials; do not overwrite.'
    assert not REPORT.exists(), 'Retain earlier evidence.'
    OUT.mkdir()
    REPORT.mkdir(parents=True)
    normal_paths = [NORMAL / 'launcher-v2.sqlite', NORMAL / 'content_load.json', NORMAL / 'pdx_settings.json',
                    ROOT / '.git/index', ROOT.parent / '1776_age_of_revolutions_fork.mod']
    frozen = json.loads((LAB / 'evidence/FROZEN_MANIFEST.json').read_text(encoding='utf-8-sig'))
    baseline = {str(p): sha(p) for p in normal_paths if p.is_file()}
    baseline.update({str(ROOT / rel): sha(ROOT / rel) for rel in frozen['files'] if (ROOT / rel).is_file()})
    (REPORT / 'NORMAL_INPUTS_BEFORE.json').write_text(json.dumps(baseline, indent=2), encoding='utf-8')
    gui_path = LAB / 'A_current/gui/tech_tree.gui'
    original = gui_path.read_bytes()
    raw = original.decode('utf-8-sig')
    matches = list(re.finditer(r'(?m)^(\s*visible\s*=\s*")([^"\r\n]{2000,})("[^\r\n]*)', raw))
    assert len(matches) == 2
    edge = next(m for m in matches if 'TechTreeLine.GetTargetTech.Self' in m[2])
    card = next(m for m in matches if 'Technology.ShouldShow' in m[2])
    edge_ids = set(re.findall(r"GetTechnology\('([^']+)'\)", edge[2]))
    card_ids = set(re.findall(r"GetTechnology\('([^']+)'\)", card[2]))
    assert card_ids == edge_ids | {'stock_exchange'}
    assert 'joint_stock_companies' in edge_ids and 'stock_exchange' not in edge_ids
    hidden = sorted(edge_ids - {'joint_stock_companies'})
    def equal(prefix, key):
        return f"ObjectsEqual({prefix}, GetTechnology('{key}').Self)"
    new_edge = '[Not(' + balanced([equal('TechTreeLine.GetTargetTech.Self', key) for key in hidden]) + ')]'
    forces = 'Or(' + equal('Technology.Self', 'joint_stock_companies') + ', ' + equal('Technology.Self', 'stock_exchange') + ')'
    new_card = '[Or(' + forces + ', And(Technology.ShouldShow(GetPlayer.Self), Not(' + balanced([equal('Technology.Self', key) for key in hidden]) + ')))]'
    graph = json.loads((LAB / 'evidence/MOD_GRAPH.json').read_text(encoding='utf-8-sig'))
    ids = list(graph['nodes']) + ['__unknown_technology__']
    cases = []
    for kind, old, new in [('edge', edge[2], new_edge), ('card', card[2], new_card)]:
        old_evaluate, new_evaluate = evaluator(old), evaluator(new)
        failures = [(key, shown) for key in ids for shown in [False, True] if old_evaluate(key, shown) != new_evaluate(key, shown)]
        assert not failures
        def depth(value):
            current = high = 0
            for character in value:
                current += (character == '(') - (character == ')')
                high = max(high, current)
            return high
        cases.append({'kind': kind, 'before': old, 'after': new, 'cases_compared': len(ids) * 2,
                      'semantic_failures': failures, 'before_characters': len(old), 'after_characters': len(new),
                      'before_gettechnology_tokens': old.count('GetTechnology('), 'after_gettechnology_tokens': new.count('GetTechnology('),
                      'before_max_parenthesis_depth': depth(old), 'after_max_parenthesis_depth': depth(new)})
    changed = raw
    for match, replacement in sorted([(edge, new_edge), (card, new_card)], key=lambda value: value[0].start(), reverse=True):
        changed = changed[:match.start(2)] + replacement + changed[match.end(2):]
    diagnostic = LAB / 'C_simplified_gui'
    assert not diagnostic.exists()
    shutil.copytree(LAB / 'A_current', diagnostic)
    (diagnostic / 'gui/tech_tree.gui').write_bytes((b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'') + changed.encode('utf-8'))
    diffs = []
    for rel, spec in frozen['files'].items():
        if sha(diagnostic / rel) != spec['sha256']:
            diffs.append(rel)
    assert diffs == ['gui/tech_tree.gui'], diffs
    template = LAB / 'runtime_151/A/user_data'
    trials = []
    for trial, arm in [('A1', 'A'), ('B1', 'B'), ('B2', 'B'), ('A2', 'A')]:
        profile = OUT / trial / 'user_data'
        profile.mkdir(parents=True)
        for name in ['pdx_settings.json', 'launcher-v2.sqlite']:
            shutil.copy2(template / name, profile / name)
        mod_path = LAB / ('A_current' if arm == 'A' else 'B_vanilla_gui')
        content = {'enabledMods': [{'path': str(mod_path)}], 'disabledDLC': [], 'enabledUGC': []}
        (profile / 'content_load.json').write_text(json.dumps(content, indent=2), encoding='utf-8')
        trials.append({'trial': trial, 'arm': arm, 'profile': str(profile), 'mod': str(mod_path),
                       'executable': str(EXE), 'arguments': ['--userdir=' + profile.as_posix(), '-debug_mode'],
                       'settings_sha256': sha(profile / 'pdx_settings.json')})
    result = {'status': 'PREPARED_INTERACTIVE_NOT_YET_MEASURED', 'prepared_utc': datetime.now(timezone.utc).isoformat(),
              'executable': str(EXE), 'executable_sha256': sha(EXE), 'trials': trials,
              'diagnostic_copy': str(diagnostic), 'diagnostic_differences': diffs, 'visibility_comparison': cases,
              'only_changes': 'Two GUI visibility expressions; no technology definitions changed.',
              'semantics_scope': 'Distinct defined technology identities, all 291 technology IDs plus an unknown ID, both ShouldShow states; not engine execution.',
              'performance_optimization_verified': False, 'game_started': False, 'normal_profile_modified': False}
    for base in [OUT, REPORT]:
        (base / 'PREPARATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ['visibility_comparison', 'trials']}, ensure_ascii=False))
    print(json.dumps([{k: v for k, v in c.items() if k not in ['before', 'after']} for c in cases]))


if __name__ == '__main__':
    main()
