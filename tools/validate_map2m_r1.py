"""R1 preserves all runtime bytes except the explicitly scoped trade GUI fix."""
import csv, json, subprocess, unittest
import map2m_r1_research as work
from map2l_hre_work import GIT
from map2l_registry import active_registry_path

def unauthorized_changes(before, after, ui):
    changed = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
    allowed = {work.GUI} if before.get(work.GUI) == ui.get('before_sha256') and after.get(work.GUI) == ui.get('after_sha256') else set()
    return sorted(changed - allowed)

def validate():
    baseline = json.loads((work.OUT/'BASELINE.json').read_text())
    hashes = {p.relative_to(work.ROOT).as_posix():work.previous.core.sha(p) for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for p in (work.ROOT/folder).rglob('*') if p.is_file()}
    checks = []
    def check(name, value): checks.append(dict(name=name, passed=bool(value)))
    ui_path = work.OUT/'UI_FIX.json'
    ui = dict(file=work.GUI,before_sha256=work.previous.core.sha(work.OUT/'building_details_panel.before.gui'),after_sha256=hashes[work.GUI],runtime_status='NOT_YET_TESTED',scope='Trade centre detail only: two PMGs per row, 150 px panel height. Third data-reporting selector wraps to row two. Other PM and list templates unchanged.')
    if ui_path.exists():
        check('GUI matches immutable reviewed implementation',json.loads(ui_path.read_text())==ui)
    else: work.dump(ui_path,ui)
    check('Only the authorized GUI runtime file differs', not unauthorized_changes(baseline['hashes'],hashes,ui))
    check('Original GUI snapshot matches baseline',ui['before_sha256']==baseline['hashes'][work.GUI])
    check('GUI fix actually differs from original',ui['after_sha256']!=ui['before_sha256'])
    inventory = work.previous.core.qa.inventory()
    check('Complete demographic/economic/political/military inventory unchanged',inventory==baseline['inventory'])
    check('World population unchanged',sum(r['count'] for r in inventory['pops'])==835804980)
    check('Registry unchanged',json.loads(active_registry_path().read_text())==baseline['registry'])
    check('Province bitmap unchanged',hashes['map_data/provinces.png']==baseline['bitmap_sha256'])
    owners = {row['key'][0]:row['key'][1:] for row in inventory['owners']}
    bmp = work.previous.core.packed(work.ROOT/'map_data/provinces.png')
    check('341 Swedish core cells intact',int((bmp==0x567452).sum())==341 and owners['x567452']==['STATE_POMERANIA','SWE'])
    check('Thorn unchanged and Danzig still Polish',owners['x41A021'][1]=='PRU' and owners['x80A0A0'][1]=='PLC')
    check('Inherited anomalies isolated: 44 duplicates, 12 invalid references',len(inventory['duplicates'])==44 and len(inventory['errors'])==12)
    refs = json.loads((work.OUT/'HYPOTHESES_REFERENCE.json').read_text())
    check('Initial hypothesis models and cells immutable',all(work.previous.core.sha(work.ROOT/path)==digest for path,digest in refs.items()))
    for sector,count in [('PEENE',79),('NETZE',162)]:
        with (work.OUT/sector/'CELL_CLASSIFICATION.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
        calibration=json.loads((work.OUT/sector/'CALIBRATION.json').read_text())
        check(sector+' all initial candidates uncertain and unapplied',len(rows)==count and all(r['Class']=='UNCERTAIN' and r['Applied']=='False' for r in rows))
        check(sector+' no fictional independent accuracy',calibration['independent_validation_points']==0 and calibration['independent_mean_error_px'] is None and calibration['independent_max_error_px'] is None)
        check(sector+' completion gates false',not calibration['geometry_complete'] and not calibration['historical_attribution_complete'])
    sources=json.loads((work.OUT/'SOURCES.json').read_text())
    check('Research source hashes valid',all(work.previous.core.sha(work.OUT/'EVIDENCE'/s['file'])==s['sha256'] for s in sources))
    check('1793 Kornik atlas not treated as pre-1776',next(s for s in sources if s['id']=='KORNIK')['pre_1776'] is False)
    check('Undated Homann specimen not silently dated 1773',next(s for s in sources if s['id']=='HOMANN_RYHINER')['pre_1776'] is None)
    check('HEAD unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=work.ROOT,text=True).strip()==baseline['git_head'])
    check('Git index unchanged',work.previous.core.sha(work.ROOT/'.git/index')==baseline['git_index_sha256'])
    suite=unittest.defaultTestLoader.discover(str(work.ROOT/'tools'),pattern='test_trade_center_pm_layout.py')
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    check('Trade centre GUI static regression tests',result.wasSuccessful() and result.testsRun==8)
    report=dict(status='MAP-2M_PARTIAL',research_pass='MAP-2M-R1',static_preservation='PASS' if all(c['passed'] for c in checks) else 'FAIL',allowed_runtime_changes=[work.GUI],applied_territorial_cells=0,new_RGBs=0,geometry_complete=False,historical_attribution_complete=False,engine_tested=False,ui_runtime_status='NOT_YET_TESTED',checks=checks,gui_tests_passed=result.testsRun-len(result.failures)-len(result.errors),gui_tests_total=result.testsRun,scope_note='Original MAP2M validator expects byte-identical GUI; R1 explicitly authorizes this one scoped UI change without rewriting that baseline or historical reports.')
    work.dump(work.OUT/'VALIDATION.json',report)
    print(report['status'],report['static_preservation'],sum(c['passed'] for c in checks),'/',len(checks),'checks; UI',report['gui_tests_passed'],'/',result.testsRun)
    return int(not all(c['passed'] for c in checks))

if __name__=='__main__':raise SystemExit(validate())
