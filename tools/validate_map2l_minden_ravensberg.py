"""Exact scoped conservation; approximate historical envelope, not cadastral QA."""
import json
import numpy as np
import validate_map2l_mainz as validation
import map2l_minden_ravensberg as work
from map2l_belgium import packed
from map2l_franconia import inside
from map2l_registry import approved_lot_dirs,ownership_rows,ancestor_rgb,expected_country_definitions
from validate_map2a import counter

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    source=tracing['calibrated_sources'][0];matrix=np.array(source['matrix'])
    fit=[r for r in source['controls'] if r['role']=='FIT']
    reproduced=np.linalg.lstsq(np.array([[*r['source'],1] for r in fit]),np.array([r['game'] for r in fit]),rcond=None)[0]
    check('Disclosed four-point regional approximation reproduced',np.allclose(matrix,reproduced,rtol=0,atol=1e-9))
    residuals=[dict(name=r['name'],role=r['role'],error_pixels=float(np.linalg.norm(np.array([*r['source'],1])@matrix-r['game'])),physical_accuracy_certified=False) for r in source['controls']]
    work.core.dump('CALIBRATION_DIAGNOSTICS.json',dict(points=residuals,warning='Approximate native locators, not surveyed city positions. No two-pixel accuracy claimed; Erfurt unchanged.'))
    check('Bielefeld residual retained above seven pixels, not hidden',next(r for r in residuals if r['name']=='Bielefeld')['error_pixels']>7)
    before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png')
    geometry=json.loads((out/'GEOMETRY.json').read_text());owners={r['key'][0]:r['key'][2] for r in current['owners']}
    old={r['key'][0]:r['key'][1:] for r in baseline['inventory']['owners']}
    check('Only two originally Hanoverian parents eligible',set(geometry['parents'])=={'x165E05','xBBA504'} and all(old[r]==['STATE_HANNOVER','HAN'] for r in geometry['parents']))
    totals={1:0,2:0}
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y))
        points=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=np.full(len(cells),'HAN',dtype='U3')
        for i,polygon in enumerate(tracing['polygons'],1):
            if parent not in polygon['parents']:continue
            take=inside(points,polygon['points']);expected[take]=polygon['owner'];totals[i]+=int(take.sum())
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells])
        check('Every cell follows retained source envelope '+parent,np.array_equal(actual,expected))
    check('Only Minden core transferred; zero Ravensberg claim',totals=={1:76,2:0})
    lots=approved_lot_dirs();later=lots[lots.index(out)+1:]
    expected_outside=counter([r for r in baseline['inventory']['owners'] if r['key'][1]!='STATE_HANNOVER'])
    allowed_parents={int(r[1:],16) for r in geometry['parents']};oldcolors=set(np.unique(before).tolist())
    for lot in later:
        declared=json.loads((lot/'REGISTRY_MIGRATION.json').read_text())
        for row in ownership_rows(declared,'previous'):
            if row['state']!='STATE_HANNOVER':expected_outside[(row['rgb'],row['state'],row['beneficiary'])]-=1
        for row in ownership_rows(declared,'updated'):
            if row['state']!='STATE_HANNOVER':expected_outside[(row['rgb'],row['state'],row['beneficiary'])]+=1
        geo=json.loads((lot/'GEOMETRY.json').read_text())
        allowed_parents.update(ancestor_rgb(r,oldcolors) for r in geo['parents'])
    check('No owner outside Hanover changed except exact later reviewed migrations',+expected_outside==counter([r for r in current['owners'] if r['key'][1]!='STATE_HANNOVER']))
    protected=~np.isin(before,list(allowed_parents))
    check('Every cell outside these parents and exact later parent masks byte-identical',np.array_equal(before[protected],after[protected]))
    preceding=json.loads((out.parent/'RHINE_WESTPHALIA/GEOMETRY.json').read_text())
    preserved={r['rgb'] for r in preceding['new_provinces']}|{r['rgb'] for r in preceding['assignments'] if r['owner']!=r['previous_owner']}
    check('Previous twenty RGB and 1081 restored cells retained; later unresolved PRU remainder reviewed separately',len(preceding['new_provinces'])==20 and sum(r['pixels'] for r in preceding['assignments'] if r['owner']!=r['previous_owner'])==1081 and all(int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in preceding['assignments'] if r['rgb'] in preserved))
    anchors=json.loads((out/tracing['native_anchors']).read_text())
    for row in anchors:
        x,y=int(float(row['Locator_X'])),int(float(row['Locator_Y']))
        check('Physical locator and RGB unchanged '+row['Hub_Name'],before[y,x]==after[y,x])
    check('Minden wood anchor belongs to transferred core',owners['xBBA504']=='PRU')
    check('Bielefeld not used to transfer whole mine province',owners['x165E05']=='HAN')
    later_migrations=[json.loads((lot/'REGISTRY_MIGRATION.json').read_text()) for lot in later]
    check('No country created by Minden; only exact later country additions',current['countries']==expected_country_definitions(baseline['inventory']['countries'],later_migrations) and plan['new_tags']==[])
    check('Both original recruiting subdivisions survive',all(['STATE_HANNOVER',tag] in current['states'] for tag in ['OLD','HAN']) and ['STATE_HANNOVER','PRU'] in current['states'])
    check('All building files unchanged; no added levels',not any('/buildings/' in r for r in plan['files']))
    population=[r for r in plan['allocations'] if r['kind']=='population']
    check('All four profiles allocated once with no artificial people',len(population)==len({r['profile'] for r in population})==4 and all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in population) and sum(r['after']['PRU'] for r in population)==33956)

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS
    validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
