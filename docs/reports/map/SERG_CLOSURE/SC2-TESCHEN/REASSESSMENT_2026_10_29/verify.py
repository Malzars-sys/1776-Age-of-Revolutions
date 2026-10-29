"""Read-only Teschen reassessment; outputs confined to this new research folder.

Never call the old installer/validate/report writer or regenerate canonical views.
Run with the repository Python and -B -X utf8. Existing test failures stay raw.
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
sys.path.insert(0, str(ROOT / 'tools'))
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
import serg_sc2_teschen as a
import map2k_imperial_system as compiler
from map2k_patch import ELECTORS


def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run_tests():
    results = []
    for module in ['test_serg_sc2_teschen', 'test_serg_closure_roadmap']:
        stream = io.StringIO()
        suite = unittest.defaultTestLoader.loadTestsFromName(module)
        r = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        (OUT / (module + '.log')).write_text(stream.getvalue(), encoding='utf-8')
        results.append(dict(module=module, executed=r.testsRun,
                            passed=r.testsRun-len(r.failures)-len(r.errors)-len(r.skipped),
                            failures=[dict(test=t.id(), traceback=s) for t, s in r.failures],
                            errors=[dict(test=t.id(), traceback=s) for t, s in r.errors],
                            skipped=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                            successful=r.wasSuccessful()))
    write('EXISTING_TEST_RESULTS.json', dict(recorded_on='2026-10-29', suites=results,
          engine_executed=False, old_test_sources_modified=False))
    print('Existing suites:', [(r['module'], r['executed'], r['passed'], len(r['failures']), len(r['errors']), len(r['skipped'])) for r in results], flush=True)


def verify():
    checks = []
    def ck(name, ok):
        checks.append(dict(name=name, passed=bool(ok)))
    base = a.load(OUT / 'BASELINE.json')
    old = a.load(a.OUT / 'BASELINE.json')
    native = a.load(a.OUT / 'NATIVE_INVENTORY.json')
    migration = a.load(a.OUT / 'REGISTRY_MIGRATION.json')
    inv = a.core.qa.inventory()
    bitmap = a.core.packed(ROOT / 'map_data/provinces.png')
    yy, xx = a.np.where(bitmap == int(a.RGB[1:], 16))
    cells = sorted([[int(x), int(y)] for x, y in zip(xx, yy)])
    rows = a.load(a.reg.active_registry_path())
    ck('Same exact 179 cells as installed delivery', cells == native['cells'] == migration['extent_added_cells'] and len(cells) == 179)
    ck('Unique AUS ownership in WEST_GALICIA', [r for r in inv['owners'] if r['key'][0] == a.RGB] == [dict(key=[a.RGB, a.SID, a.TAG], count=1)])
    ck('Physical definition remains WEST_GALICIA', inv['geometry'][a.RGB] == a.SID)
    ck('581 unique imperial titles, one Teschen addition', len(rows) == len({r['rgb'] for r in rows}) == 581 and [r for r in rows if r['rgb'] != a.RGB] == old['registry'])
    ck('Only x9061E0 imperial in WEST_GALICIA', [r for r in rows if r['state'] == a.SID] == [r for r in rows if r['rgb'] == a.RGB] and next(r for r in rows if r['rgb'] == a.RGB)['beneficiary'] == a.TAG)
    ck('Exact province override only', a.reg.provincial_membership_overrides() == {(a.RGB, a.SID, a.TAG)})
    ck('No whole Galician region in compiler or member overrides', a.SID not in compiler.REGIONS and a.SID not in a.reg.member_region_overrides().get(a.TAG, set()) and a.SID not in a.reg.territorial_holder_overrides().get(a.TAG, set()))
    oldmask = a.np.isin(bitmap, [int(r['rgb'][1:], 16) for r in old['registry']])
    newmask = a.np.isin(bitmap, [int(r['rgb'][1:], 16) for r in rows])
    ck('Imperial extent added exactly target cells', a.np.array_equal(newmask & ~oldmask, bitmap == int(a.RGB[1:], 16)) and not a.np.any(oldmask & ~newmask))
    ck('Declared imperial extent migration exact', a.np.array_equal(a.reg.migrate_extent(oldmask, [migration]), newmask))
    ck('No ownership migration in TE-R-CORE', a.reg.ownership_rows(migration, 'previous') == a.reg.ownership_rows(migration, 'updated') == [])
    scoped = {}
    for key in ['regional_pop', 'buildings']:
        scoped[key] = [r for r in inv[key] if r['key'][:2] == [a.SID, a.TAG]]
        previous = [r for r in old['inventory'][key] if r['key'][:2] == [a.SID, a.TAG]]
        ck('Current Teschen ' + key + ' equals installed snapshot', scoped[key] == previous)
    pop = sum(r['count'] for r in scoped['regional_pop'])
    ck('Seven population groups total 135753', pop == 135753 and len(scoped['regional_pop']) == 7)
    scoped['units'] = [r for r in inv['units'] if r['key'][0] == a.TAG and r['key'][2] == a.SID]
    ck('Teschen military recruitment unchanged', scoped['units'] == [r for r in old['inventory']['units'] if r['key'][0] == a.TAG and r['key'][2] == a.SID] and len(scoped['units']) == 1)
    scoped['owners'] = [r for r in inv['owners'] if r['key'][1] in [a.SID, 'STATE_MORAVIA', 'STATE_UPPER_SILESIA']]
    ck('Neighboring Galician Moravian Silesian ownership unchanged', scoped['owners'] == [r for r in old['inventory']['owners'] if r['key'][1] in [a.SID, 'STATE_MORAVIA', 'STATE_UPPER_SILESIA']])
    effects = (ROOT / 'common/scripted_effects/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
    triggers = (ROOT / 'common/scripted_triggers/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
    ck('Restitution province-bound AUS command', 'country = c:AUS provinces = { x9061E0 }' in effects)
    ck('No neighbor Galician province in restitution', all('p:' + rgb + '.state' not in effects for rgb in ['x906060', 'x1161E0']))
    ck('Rightful-holder trigger scoped to target province', 'p:x9061E0.state ?= this' in triggers)
    elector_line = next(line for line in triggers.splitlines() if 'has_variable = aor1776_hre_electoral_privilege_granted' in line)
    ck('Nine original electors in compiled trigger', len(ELECTORS) == 9 and all('c:' + tag + ' ?= this' in elector_line for tag in ELECTORS.values()) and elector_line.count(' ?= this') == 9)
    paths = sorted(set(a.load(a.OUT / 'EXPECTED_TEXT.json')) | {'common/history/states/00_states.txt', 'common/history/pops/00_west_europe.txt', 'common/history/buildings/02_east_europe.txt', 'common/history/buildings/98_build_start_1776_world_redistribution.txt', 'common/history/military_formations/00_military_formations_europe.txt'})
    parsed = []
    for rel in paths:
        p = ROOT / rel
        if p.suffix == '.txt' and p.exists():
            a.core.cw.parse(p.read_text(encoding='utf-8-sig'))
            parsed.append(rel)
    ck('Installed scoped script files parse', len(parsed) >= 4)
    for lang in ['french', 'english']:
        for family in ['feedback', 'repairs']:
            p = ROOT / f'localization/{lang}/1776_imperial_{family}_l_{lang}.yml'
            data = p.read_bytes()
            ck('Localization BOM and header ' + family + ' ' + lang, data.startswith(b'\xef\xbb\xbf') and data.decode('utf-8-sig').startswith('l_' + lang + ':'))
    current = a.rm.check()
    write('CANONICAL_CHECK.json', current)
    ck('Canonical validator PASS with unchanged progress', current['status'] == 'PASS' and current['progress'] == base['canonical_before']['progress'])
    task = next(t for t in a.load(a.rm.OUT / 'ROADMAP_STATE.json')['tasks'] if t['id'] == a.TASK)
    ck('Regional task BLOCKED P1 without receipt or credit', task['status'] == 'BLOCKED' and task['priority'] == 'P1' and task['runtime_validation']['attestation'] is None and not list(a.OUT.glob('RUNTIME_USER_ATTESTATION*')))
    ck('TE-R-CORE still awaiting human validation', task['installed_delivery_status'] == 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and task['installed_sub_lots'][0]['status'] == 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
    drift = {rel: dict(before=h, after=sha(ROOT / rel)) for rel, h in base['protected_sha256'].items() if sha(ROOT / rel) != h}
    ck('All preexisting Teschen evidence and canonical instructions preserved', not drift)
    runtime = a.runtime.runtime_hashes()
    functional_drift = {rel: dict(before=base['runtime_before_sha256'].get(rel), after=runtime.get(rel)) for rel in sorted(set(runtime) | set(base['runtime_before_sha256'])) if runtime.get(rel) != base['runtime_before_sha256'].get(rel)}
    # Preserve the complete drift, including unrelated concurrent music removals.
    # No broad green claim about all concurrent work; fail any Teschen-linked drift.
    scoped_paths = set(paths) | {a.reg.active_registry_path().relative_to(ROOT).as_posix(), 'map_data/provinces.png', 'map_data/state_regions/02_east_europe.txt'}
    scoped_drift = {p: v for p, v in functional_drift.items() if p in scoped_paths}
    ck('No functional change to Teschen dependencies during reassessment', not scoped_drift)
    git = dict(head=a.git('rev-parse', 'HEAD'), branch=a.git('branch', '--show-current'), index=sha(ROOT / '.git/index'))
    ck('Git HEAD branch and index unchanged', git == base['git'])
    old_snapshot_differences = {rel: dict(delivery=h, current=sha(ROOT / rel)) for rel, h in old['hashes'].items() if rel in runtime and sha(ROOT / rel) != h}
    write('CURRENT_SCOPE.json', dict(rgb=a.RGB, cells=cells, count=len(cells), population=pop, bounds=[int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())], inventory=scoped, parsed_scripts=parsed, electors=ELECTORS, registry_count=len(rows)))
    write('CONSERVATION_CHECK.json', dict(protected_file_drift=drift, functional_drift_since_reassessment=functional_drift, teschen_dependency_drift=scoped_drift, outside_teschen_drift={p:v for p,v in functional_drift.items() if p not in scoped_paths}, older_delivery_runtime_differences=old_snapshot_differences, git=git, runtime_sha256=runtime, protected_count=len(base['protected_sha256'])))
    write('DEMOGRAPHIC_ARITHMETIC.json', dict(mod=pop, political_1770_71=112850, ecclesiastical_1770=112752, nominal_difference=112850-112752, mod_minus_political=pop-112850, mod_minus_ecclesiastical=pop-112752, excess_relative_to_political_percent=(pop/112850-1)*100, excess_relative_to_ecclesiastical_percent=(pop/112752-1)*100, spyra_confessional_sum=78406+34346, nesladkova_printed_confessional_sum=78406+34342, nesladkova_printed_difference=108, mechanically_required_growth_percent_by_elapsed_years={str(y): ((pop/112850)**(1/y)-1)*100 for y in [5,6]}, interpretation='Arithmetic only; no growth estimate, replacement total or permitted tolerance inferred.'))
    result = dict(recorded_on='2026-10-29', status='PASS' if all(r['passed'] for r in checks) else 'FAIL', passed=sum(r['passed'] for r in checks), total=len(checks), checks=checks, engine_executed=False, canonical_written=False, gameplay_written=False)
    write('SCOPED_STATIC_RESULTS.json', result)
    print('Scoped checks:', result['status'], result['passed'], '/', result['total'], [c['name'] for c in checks if not c['passed']], flush=True)


if __name__ == '__main__':
    assert ROOT.name == '1776_Age_of_Revolutions_fork', ROOT
    if sys.argv[1:] == ['tests']:
        run_tests()
    elif sys.argv[1:] == ['scoped']:
        verify()
    else:
        raise SystemExit('Choose tests or scoped; writes only this new research folder.')
