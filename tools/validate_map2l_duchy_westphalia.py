"""Exact differential QA for Cologne's Westphalian cores, not engine QA."""
import json
import numpy as np
import validate_map2l_mainz as validation
import map2l_duchy_westphalia as work
from map2l_belgium import packed
from map2l_franconia import inside
from map2l_registry import approved_lot_dirs,ownership_rows,ancestor_rgb,expected_country_definitions
from validate_map2a import counter

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    vg,sk=tracing['calibrated_sources'];bridge=np.array(sk['matrix'])
    retained=json.loads((out.parent/'RHINE_WESTPHALIA/TRACING.json').read_text())['calibrated_sources'][0]
    check('Previous disclosed Schenk/game bridge exactly reused',sk['matrix']==retained['matrix'])
    fit=[r for r in vg['cross_controls'] if r['role']=='FIT']
    cross=np.linalg.lstsq(np.array([[*r['source'],1] for r in fit]),np.array([r['schenk'] for r in fit]),rcond=None)[0]
    matrix=np.vstack((np.column_stack((cross[:2],np.zeros(2))),[*cross[2],1]))@bridge
    check('Cross-map four-town approximation independently reproducible',np.allclose(cross,vg['matrix_to_schenk'],rtol=0,atol=1e-9) and np.allclose(matrix,vg['matrix'],rtol=0,atol=1e-9))
    check('Wrong northern Dusseldorf identification rejected before installation',fit[0]['source']==[645,425] and json.loads((out/'DRAFT_REJECTED.json').read_text())['old_candidate_was_installed'] is False)
    cross_errors=[]
    for row in vg['cross_controls']:
        delta=np.array([*row['source'],1])@cross-row['schenk']
        cross_errors.append(dict(name=row['name'],role=row['role'],map_to_map_residual_game_px=float(np.linalg.norm(delta@bridge[:2])),physical_accuracy_certified=False))
    native_errors=[]
    for row in sk['controls']:
        native_errors.append(dict(name=row['name'],role=row['role'],locator_comparison_error_px=float(np.linalg.norm(np.array([*row['source'],1])@bridge-row['game'])),physical_accuracy_certified=False))
    checks_only=[r['map_to_map_residual_game_px'] for r in cross_errors if r['role']=='CHECK']
    work.core.dump('CALIBRATION_DIAGNOSTICS.json',dict(cross_map_points=cross_errors,cross_map_holdout_mean_px=float(np.mean(checks_only)),cross_map_holdout_max_px=max(checks_only),native_locator_points=native_errors,warning='Map-to-map consistency is NOT independently surveyed geographic accuracy on the game bitmap. Native Cologne/Bonn discrepancies retained; no exact cadastral claim.'))
    check('Both map-to-map holdouts retained, including Ruthen above three pixels',len(checks_only)==2 and checks_only[0]>3 and checks_only[1]<1)
    check('Native bridge discrepancies not concealed',all(r['locator_comparison_error_px']>7 for r in native_errors if r['role']=='CHECK'))
    geometry=json.loads((out/'GEOMETRY.json').read_text());before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in current['owners']};old={r['key'][0]:r['key'][1:] for r in baseline['inventory']['owners']}
    check('Three reviewed PRU remnants only, all in state 61',set(geometry['parents'])=={'x418021','x4101A0','xA08061'} and all(old[r]==['STATE_WESTPHALIA','PRU'] for r in geometry['parents']))
    totals={1:0,2:0}
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y));points=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=np.full(len(cells),'PRU',dtype='U3')
        for i,polygon in enumerate(tracing['polygons'],1):
            if parent not in polygon['parents']:continue
            take=inside(points,polygon['points']);expected[take]=polygon['owner'];totals[i]+=int(take.sum())
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells])
        check('Every parent cell exactly classified by source envelope '+parent,np.array_equal(actual,expected))
    check('Exactly 69 duchy and 15 Vest cells transferred',totals=={1:69,2:15})
    lots=approved_lot_dirs();later=lots[lots.index(out)+1:]
    migrations=[json.loads((lot/'REGISTRY_MIGRATION.json').read_text()) for lot in later]
    allowed={int(r[1:],16) for r in geometry['parents']};oldcolors=set(np.unique(before).tolist())
    for lot in later:allowed.update(ancestor_rgb(r,oldcolors) for r in json.loads((lot/'GEOMETRY.json').read_text())['parents'])
    protected=~np.isin(before,list(allowed))
    check('Raster outside own masks and exact later parent masks unchanged',np.array_equal(before[protected],after[protected]))
    expected_outside=counter([r for r in baseline['inventory']['owners'] if r['key'][1]!='STATE_WESTPHALIA'])
    for migration in migrations:
        for row in ownership_rows(migration,'previous'):
            if row['state']!='STATE_WESTPHALIA':expected_outside[(row['rgb'],row['state'],row['beneficiary'])]-=1
        for row in ownership_rows(migration,'updated'):
            if row['state']!='STATE_WESTPHALIA':expected_outside[(row['rgb'],row['state'],row['beneficiary'])]+=1
    check('Owners outside Westphalia replay exact later migrations',+expected_outside==counter([r for r in current['owners'] if r['key'][1]!='STATE_WESTPHALIA']))
    for tag in ['WPM','WPD','KPF','LIP','SCM']:
        expected_tag=counter([r for r in baseline['inventory']['owners'] if r['key'][2]==tag])
        for migration in migrations:
            for row in ownership_rows(migration,'previous'):
                if row['beneficiary']==tag:expected_tag[(row['rgb'],row['state'],tag)]-=1
            for row in ownership_rows(migration,'updated'):
                if row['beneficiary']==tag:expected_tag[(row['rgb'],row['state'],tag)]+=1
        check('Restored allocation plus exact later changes '+tag,+expected_tag==counter([r for r in current['owners'] if r['key'][2]==tag]))
    previous=json.loads((out.parent/'RHINE_WESTPHALIA/GEOMETRY.json').read_text())
    preserved={r['rgb'] for r in previous['new_provinces']}|{r['rgb'] for r in previous['assignments'] if r['owner']!=r['previous_owner']}
    check('Previous twenty RGB and 1081 restored cells exact',len(previous['new_provinces'])==20 and sum(r['pixels'] for r in previous['assignments'] if r['owner']!=r['previous_owner'])==1081 and all(int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and owners[r['rgb']]==r['owner'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in previous['assignments'] if r['rgb'] in preserved))
    minden=json.loads((out.parent/'MINDEN_RAVENSBERG/GEOMETRY.json').read_text())
    check('All Minden cells and four new RGB unchanged',all(int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and owners[r['rgb']]==r['owner'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in minden['assignments']))
    anchors=json.loads((out/tracing['native_anchors']).read_text())
    for row in anchors:
        x,y=int(float(row['Locator_X'])),int(float(row['Locator_Y']))
        check('Unmoved native locator retains exact RGB '+row['Hub_Name'],before[y,x]==after[y,x])
    check('No locator rebinding; only declared prime-land expansion',geometry['hub_rebindings']==[] and all(r['field']=='prime_land' and r['state']=='STATE_WESTPHALIA' for r in plan['region_reference_changes']))
    for change in plan['region_reference_changes']:
        check('Prime-land physical footprint exact after subdivision '+change['state'],np.array_equal(np.isin(before,[int(r[1:],16) for r in change['before']]),np.isin(after,[int(r[1:],16) for r in change['after']])))
    for name in ['Dortmund','Essen']:
        row=next(r for r in anchors if r['Hub_Name']==name);x,y=int(float(row['Locator_X'])),int(float(row['Locator_Y']))
        check('Unresolved free-city/abbey locator not handed to Cologne '+name,owners['x'+format(int(after[y,x]),'06X')]=='PRU')
    check('No country created by duchy; exact later additions only',current['countries']==expected_country_definitions(baseline['inventory']['countries'],migrations) and plan['new_tags']==[])
    check('Prussia survives and Cologne has valid shared subdivision',all(['STATE_WESTPHALIA',tag] in current['states'] for tag in ['PRU','KCL']))
    check('No building file altered',not any('/buildings/' in path for path in plan['files']))
    population=[r for r in plan['allocations'] if r['kind']=='population']
    check('Three population profiles allocated exactly once, 27631 transferred without creation',len(population)==len({r['profile'] for r in population})==3 and sum(r['after']['KCL'] for r in population)==27631 and all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in population))

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS
    validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
