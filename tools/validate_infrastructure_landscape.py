"""Read-only regression tests; --capture writes only a new report baseline.

Tests script definitions and a small interpreter, NOT engine spline selection.
No game launch, saves, Git writes, building changes or shader edits.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import validate_diplomacy_ottoman_1776 as cw

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
OUT = ROOT / 'docs/reports/graphics/REGIONAL_INFRASTRUCTURE_LANDSCAPE'
ROUTES = 'gfx/map/spline_network/route_graphics/02_railroad_vehicles.txt'
TRIGGERS = 'common/scripted_triggers/1776_infrastructure_landscape.txt'
GUARD = 'aor1776_gfx_local_rail_network'
ALLOWED = {ROUTES, TRIGGERS}
KINDS = {'passenger_train', 'mining_train', 'forestry_train', 'military_mobilization_railroad'}


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def runtime_hashes():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for folder in ('common', 'gfx', 'map_data', 'gui', 'events', 'localization')
            for p in sorted((ROOT / folder).rglob('*')) if p.is_file()
            and p.relative_to(ROOT).as_posix() not in ALLOWED}


def git_state():
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    index = subprocess.check_output(['git', 'rev-parse', '--git-path', 'index'], cwd=ROOT, text=True).strip()
    return {'HEAD': head, 'index_sha256': sha(ROOT / index)}


def capture():
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / 'BASELINE.json'
    if target.exists():
        raise RuntimeError('Baseline already exists; do not overwrite')
    baseline = {'runtime': runtime_hashes(), 'git': git_state(),
                'native_routes_sha256': sha(GAME / ROUTES)}
    target.write_text(json.dumps(baseline, indent=2), encoding='utf-8')
    print('Baseline captured; existing runtime files:', len(baseline['runtime']))


def evaluate(nodes, state=None, building=None):
    """Only the syntax used by this helper; fail closed on unexpected keys."""
    def one(n):
        if n.key == 'scope:state':
            return state is not None and evaluate(n.children(), state=state)
        if n.key == 'any_scope_building':
            return any(evaluate(n.children(), state=state, building=b) for b in state)
        if n.key == 'OR':
            return any(one(c) for c in n.children())
        if n.key == 'is_building_type':
            return building['type'] == cw.scalar(n.value)
        if n.key == 'level' and n.op == '>=':
            return building['level'] >= float(n.value)
        if n.key == 'has_active_production_method':
            return cw.scalar(n.value) in building['pms']
        raise AssertionError('Unexpected trigger syntax: ' + n.key)
    return all(one(n) for n in nodes)


def validate():
    checks = []
    def check(label, condition):
        checks.append({'check': label, 'pass': bool(condition)})
    before = json.loads((OUT / 'BASELINE.json').read_text(encoding='utf-8'))
    check('all pre-existing runtime files preserved, no unrelated additions', runtime_hashes() == before['runtime'])
    check('HEAD and primary index unchanged', git_state() == before['git'])
    check('native route source unchanged', sha(GAME / ROUTES) == before['native_routes_sha256'])
    native = cw.parse((GAME / ROUTES).read_text(encoding='utf-8-sig'))
    actual = cw.parse((ROOT / ROUTES).read_text(encoding='utf-8-sig'))
    check('same four route definitions as native', {n.key for n in actual} == KINDS)
    for route in actual:
        possible = route.children('possible')
        check(route.key + ' single possible block', len(possible) == 1)
        guards = possible[0].children(GUARD)
        check(route.key + ' mandatory PM guard', len(guards) == 1 and guards[0].value == 'yes')
        possible[0].value = [n for n in possible[0].value if n.key != GUARD]
    check('removing guards recovers exact native AST', cw.normalized(actual) == cw.normalized(native))
    helper_nodes = cw.parse((ROOT / TRIGGERS).read_text(encoding='utf-8-sig'))
    check('one unique helper', [n.key for n in helper_nodes] == [GUARD])
    helper = helper_nodes[0]
    pmg = cw.parse((ROOT / 'common/production_method_groups/24_tech7a_wave_c_rail_pmgs.txt').read_text())
    pm_nodes = pmg[0].children('production_methods')[0].children()
    expected_pms = {cw.scalar(n.value) for n in pm_nodes} - {'pm_no_rail_network'}
    actual_pms = {cw.scalar(n.value) for n in cw.walk(helper.children()) if n.key == 'has_active_production_method'}
    check('all real rail PMs, no no-rail fallback', actual_pms == expected_pms and len(actual_pms) == 7)
    def b(pm, level=1, kind='building_railway'):
        return {'type': kind, 'level': level, 'pms': {pm}}
    for pm in sorted(actual_pms):
        check(pm + ' enabled', evaluate(helper.children(), [b(pm)]))
        check(pm + ' zero level rejected', not evaluate(helper.children(), [b(pm, 0)]))
        check(pm + ' wrong building rejected', not evaluate(helper.children(), [b(pm, kind='building_port')]))
    for label, state in [('no local building', []), ('no saved state', None),
                         ('no rail PM', [b('pm_no_rail_network')]),
                         ('road PM only', [b('pm_turnpike_road_network')]),
                         ('canal PM only', [b('pm_industrial_canals')]),
                         ('no PM data', [{'type': 'building_railway', 'level': 1, 'pms': set()}])]:
        check(label + ' rejected', not evaluate(helper.children(), state))
    check('road plus real rail accepted', evaluate(helper.children(), [
        {'type': 'building_railway', 'level': 2, 'pms': {'pm_turnpike_road_network', 'pm_early_trains'}}]))
    check('mixed building state accepted', evaluate(helper.children(), [b('unrelated', kind='building_port'), b('pm_early_trains')]))
    installed = json.loads((ROOT / 'docs/reports/map/MAP2N/COMPLETION/INSTALLED_MANIFEST.json').read_text())
    check('all MAP2N installed runtime hashes preserved', all(sha(ROOT / p) == v for p, v in installed['functional_files'].items()))
    check('MAP2N registry preserved', sha(ROOT / 'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json') == installed['registry_sha256'])
    result = {'status': 'PASS_STATIC_PARTIAL' if all(x['pass'] for x in checks) else 'FAIL',
              'passed': sum(x['pass'] for x in checks), 'total': len(checks),
              'runtime_tested': False, 'full_landscape_request_complete': False,
              'implemented': 'PM guard for civilian and legacy mobilization train route graphics only',
              'unresolved': ['rail ground splines', 'road growth controlled by infrastructure',
                             'modern military route renderer', 'PM-dependent road textures', 'canal splines'],
              'checks': checks}
    (OUT / 'VALIDATION.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
    for item in checks:
        if not item['pass']:
            print('FAIL:', item['check'])
    return 0 if all(x['pass'] for x in checks) else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--capture']:
        capture()
    else:
        sys.exit(validate())
