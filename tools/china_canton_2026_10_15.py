"""Targeted Canton-system startup correction; preserves unrelated runtime bytes."""
import collections as C
import json
import os
import subprocess
import sys
import start_buildings_2026_10_15 as b
import map2a_patch

ROOT = b.ROOT
OUT = ROOT / 'docs/reports/economy/START_BUILDINGS_2026_10_15/CHINA_CANTON'
HOOK = 'common/on_actions/14_1776_china_canton_start.txt'
STATE = 'STATE_GUANGDONG'


def dump(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def git_head():
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output([b.GIT, 'rev-parse', 'HEAD'], cwd=ROOT, env=env, text=True).strip()


def record(rows):
    return sorted((s, t, b.qa.signature(n)) for s, t, n, p in rows)


def prepare():
    assert not (OUT / 'BASELINE.json').exists(), 'Do not replace the pre-edit baseline'
    assert not (ROOT / HOOK).exists()
    rows = b.declarations()
    edits, changes, totals = {}, [], b.totals(rows)
    assert totals[STATE, 'CHI', 'building_port'] == 2
    for s, t, n, p in rows:
        if t != 'CHI':
            continue
        kind = b.cw.scalar(n.one('building'))
        if kind == 'building_trade_center' and s != STATE:
            edits.setdefault(p, []).append((n.start, n.end, ''))
            changes.append(dict(state=s, owner=t, building=kind, delta=-b.levels(n), file=p.relative_to(ROOT).as_posix()))
        elif s == STATE and kind == 'building_port':
            level_nodes = [v for v in b.cw.walk(n.children()) if v.key == 'levels']
            assert len(level_nodes) == 1 and b.levels(n) == 2
            v = level_nodes[0]
            edits.setdefault(p, []).append((v.start, v.end, 'levels=5'))
            changes.append(dict(state=s, owner=t, building=kind, delta=3, file=p.relative_to(ROOT).as_posix()))
    files = {p.relative_to(ROOT).as_posix(): map2a_patch.edits(p.read_text(encoding='utf-8-sig'), e) for p, e in edits.items()}
    expected_rows = [r for r in rows if r[3].relative_to(ROOT).as_posix() not in files]
    for rel, text in files.items():
        expected_rows += b.parse_addon(text)
    dump('BASELINE.json', dict(hashes=b.runtime_hashes(), head=git_head(), index_sha256=b.sha(ROOT / '.git/index'),
                              declarations=record(rows), expected_declarations=record(expected_rows),
                              original_files={rel: (ROOT/rel).read_text(encoding='utf-8-sig') for rel in files},
                              expected_files=files, changes=changes))
    old = b.patchwork.OUT
    try:
        b.patchwork.OUT = OUT
        b.patchwork.emit(files, 'CHANGES.patch')
    finally:
        b.patchwork.OUT = old
    print(json.dumps(changes, indent=2))


def validate():
    baseline = json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    rows = b.declarations()
    totals = b.totals(rows)
    checks = []
    def check(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))
    check('Exact expected building declarations, ownership and PMs worldwide', record(rows) == [tuple(r) for r in baseline['expected_declarations']])
    check('Five Canton trade-center levels retained', totals[STATE, 'CHI', 'building_trade_center'] == 5)
    check('No Chinese trade centers outside Western Guangdong', not any(t == 'CHI' and s != STATE and k == 'building_trade_center' and v for (s,t,k),v in totals.items()))
    check('Western Guangdong Chinese port total exactly five', totals[STATE, 'CHI', 'building_port'] == 5)
    for rel, text in baseline['expected_files'].items():
        check('Expected file content: '+rel, (ROOT/rel).read_text(encoding='utf-8-sig') == text)
        check('Parse modified history: '+rel, bool(b.cw.parse(text)))
    allowed = set(baseline['expected_files']) | {HOOK}
    hashes = b.runtime_hashes()
    for rel in sorted(set(hashes) | set(baseline['hashes'])):
        if rel not in allowed:
            check('Unchanged runtime file: '+rel, hashes.get(rel) == baseline['hashes'].get(rel))
    law = b.catalog('common/laws')['law_canton_system']
    check('Canton belongs to trade-policy group', law.one('group') == 'lawgroup_trade_policy')
    check('Canton still disallows trade outside Guangdong', any(n.key == 'country_disallow_trade_outside_canton_bool' and n.value == 'yes' for n in b.cw.walk(law.children())))
    history = (ROOT/'common/history/countries/chi - china.txt').read_text(encoding='utf-8-sig')
    check('Original Canton law and Traditionalism history retained', 'activate_law = law_type:law_canton_system' in history and 'activate_law = law_type:law_traditionalism' in history)
    hook_text = (ROOT/HOOK).read_text(encoding='utf-8-sig')
    hooks = b.cw.parse(hook_text)
    check('One-shot campaign initialization only; no periodic or loading hook', [n.key for n in hooks] == ['on_game_started_after_lobby', 'aor1776_china_canton_initialize'])
    check('Startup only activates Canton, never overrides economic laws', [n.value for n in b.cw.walk(hooks) if n.key == 'activate_law'] == ['law_type:law_canton_system'])
    check('HEAD unchanged', git_head() == baseline['head'])
    check('Git index unchanged', b.sha(ROOT/'.git/index') == baseline['index_sha256'])
    removed = -sum(r['delta'] for r in baseline['changes'] if r['building'] == 'building_trade_center')
    check('24 Chinese trade-center levels removed', removed == 24)
    result = dict(status='PASS_STATIC_PENDING_RUNTIME' if all(c['passed'] for c in checks) else 'FAIL',
                  passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                  trade_center_levels_removed=removed, port_before=2, port_after=5,
                  runtime_test='Not performed; user new-game verification required',
                  cause='Country history already activates Canton. No definite overriding script found; one-shot post-lobby safeguard added, not a permanent law lock.',
                  colgrep=dict(calls=1, result='Access denied resolving repository; fallback exact search; local model execution not confirmed'))
    dump('VALIDATION.json', result)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}, indent=2))
    for c in checks:
        if not c['passed']: print('FAIL:', c['name'])
    assert result['status'] != 'FAIL'


if __name__ == '__main__':
    {'prepare': prepare, 'validate': validate}[sys.argv[1]]()
