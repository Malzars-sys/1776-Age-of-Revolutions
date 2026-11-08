"""Read-only bounded verification; evidence written only to this new folder."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
sys.path.insert(0, str(ROOT / 'tools'))
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
import serg_sc4_massa_carrara as a
from map2k_patch import ELECTORS


def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def parts(cells):
    left = set(cells)
    sizes = []
    while left:
        todo = [left.pop()]
        size = 0
        while todo:
            x, y = todo.pop()
            size += 1
            for point in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if point in left:
                    left.remove(point)
                    todo.append(point)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def main():
    base = load(OUT / 'BASELINE.json')
    checks = []
    def ck(name, value):
        checks.append(dict(name=name, passed=bool(value)))
    arr = a.core.packed(ROOT / 'map_data/provinces.png')
    def cells(rgb):
        yy, xx = np.where(arr == int(rgb[1:], 16))
        return set(zip(map(int, xx), map(int, yy)))
    core, parent = cells(a.RGB), cells(a.PARENT)
    ck('Exact validated eight-cell core preserved', core == set(map(tuple, a.CELLS)))
    ck('MOD residual 108 cells preserved', len(parent) == 108)
    ck('MCA and local MOD residual connected', parts(core) == [8] and parts(parent) == [108])
    ck('Former 116-cell footprint has no overlap', len(core | parent) == 116 and not core & parent)
    old_options = load(a.OUT / 'CARRARA_AVENZA_FINALISATION_2026_10_31/CURRENT_GEOMETRY_AND_OPTIONS.json')
    topology = []
    for row in old_options['candidates']:
        extra = set(map(tuple, row['transferred_cells']))
        ck('Candidate still solely MOD ' + row['id'], extra <= parent)
        mc, mo = parts(core | extra), parts(parent - extra)
        expected = {'A':([10],[106]), 'B':([13],[103]), 'C':([15],[101]), 'UNSAFE_OLD_THREE':([11],[104,1])}[row['id']]
        ck('Exact four-neighbor outcome ' + row['id'], (mc, mo) == expected)
        topology.append(dict(id=row['id'], MCA_components=mc, MOD_parent_components=mo, installed=False, historical_attribution_proven=False))
    inv = a.core.qa.inventory()
    for rgb, tag in [(a.RGB,'MCA'), (a.PARENT,'MOD')]:
        ck('Unique owner ' + rgb, [r for r in inv['owners'] if r['key'][0] == rgb] == [dict(key=[rgb,a.SID,tag],count=1)])
    pop = {t:sum(r['count'] for r in inv['regional_pop'] if r['key'][:2] == [a.SID,t]) for t in ['MCA','MOD']}
    ck('MCA 10000 and MOD Emilia 495752 unchanged', pop == dict(MCA=10000, MOD=495752))
    rows = load(a.reg.active_registry_path())
    ck('581 unique imperial titles retained', len(rows) == len({r['rgb'] for r in rows}) == 581)
    ck('Only one existing MCA title', [r['rgb'] for r in rows if r['beneficiary'] == 'MCA'] == [a.RGB])
    trigger = (ROOT / 'common/scripted_triggers/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
    elector = next(line for line in trigger.splitlines() if 'has_variable = aor1776_hre_electoral_privilege_granted' in line)
    ck('Nine electors in actual compiled trigger', len(ELECTORS) == 9 and elector.count(' ?= this') == 9 and all('c:'+tag+' ?= this' in elector for tag in ELECTORS.values()))
    runtime = a.italian.runtime_hashes()
    drift = {p:dict(before=base['runtime_sha256'].get(p), after=runtime.get(p)) for p in set(runtime)|set(base['runtime_sha256']) if runtime.get(p) != base['runtime_sha256'].get(p)}
    ck('No functional changes including neighbor histories', not drift)
    protected = {p:dict(before=h, after=sha(ROOT/p)) for p,h in base['protected_sha256'].items() if sha(ROOT/p) != h}
    ck('All previous reports receipts and instructions retained', not protected)
    state = load(a.rm.OUT / 'ROADMAP_STATE.json')
    before = load(OUT / 'ROADMAP_STATE_BEFORE.json')
    task = next(t for t in state['tasks'] if t['id'] == a.TASK)
    old_task = next(t for t in before['tasks'] if t['id'] == a.TASK)
    ck('Original MC-I-CORE receipt scope retained', task['runtime_validation'] == old_task['runtime_validation'] and task['installed_sub_lots'] == old_task['installed_sub_lots'])
    ck('Regional BLOCKED P0 weight three retained', (task['status'],task['priority'],task['weight']) == ('BLOCKED','P0',3))
    ck('Other eighty task records untouched', [t for t in state['tasks'] if t['id'] != a.TASK] == [t for t in before['tasks'] if t['id'] != a.TASK])
    ck('Previous event history preserved', state['events'][:len(before['events'])] == before['events'])
    ck('Teschen runtime hold unchanged', state.get('runtime_validation_hold') == before.get('runtime_validation_hold'))
    canon = a.rm.check()
    ck('Canonical PASS with same 93/235 progress', canon['status'] == 'PASS' and canon['progress'] == base['canonical_check']['progress'])
    ck('HEAD and branch unchanged', subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == base['git_head'] and subprocess.check_output(['git','branch','--show-current'],text=True).strip() == base['branch'])
    files = ['common/history/states/00_states.txt', 'map_data/state_regions/01_south_europe.txt', 'common/history/pops/01_south_europe.txt', 'common/history/buildings/01_south_europe.txt', 'common/scripted_effects/1776_imperial_constitution.txt']
    for path in files:
        a.core.cw.parse((ROOT/path).read_text(encoding='utf-8-sig'))
    ck('Five current targeted game scripts parse', True)
    result = dict(recorded_on='2026-11-01',status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,candidates=topology,populations=pop,world_population=sum(r['count'] for r in inv['pops']),runtime_drift=drift,protected_drift=protected,canonical=canon,engine_executed=False,gameplay_installed=False)
    (OUT/'STATIC_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'], result['passed'], '/', result['total'], [c['name'] for c in checks if not c['passed']], flush=True)


if __name__ == '__main__':
    assert ROOT == a.ROOT
    main()
