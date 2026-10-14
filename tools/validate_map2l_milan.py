"""Milan continuity, source-derived raster and exact scoped conservation checks."""
import json
import numpy as np
import validate_map2l_mainz as validation
import map2l_milan as work
from map2l_belgium import packed,components,sha
from map2l_franconia import inside
from map2l_registry import approved_lot_dirs,ownership_rows
from validate_map2a import counter

def calibration(check,out,current,baseline,alignment,tracing,plan):
    source=tracing['calibrated_sources'][0]
    controls=source['controls'];fit=[r for r in controls if r['role']=='FIT']
    matrix=np.linalg.solve(np.array([[*r['source'],1] for r in fit]),np.array([r['game'] for r in fit]))
    check('Reproducible reviewed city-only matrix',np.allclose(matrix,np.array(source['matrix']),rtol=0,atol=1e-9))
    for r in controls:
        residual=float(np.linalg.norm(np.array([*r['source'],1])@matrix-r['game']))
        check('Every fitted/check residual retained '+r['name'],residual<1e-8 if r['role']=='FIT' else abs(residual-r['residual_px'])<.001)
    geometry=json.loads((out/'GEOMETRY.json').read_text())
    before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png')
    ys,xs=np.where(before==int('4713EE',16));cells=np.column_stack((xs,ys))
    historical=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=inside(historical,tracing['polygons'][0]['points'])
    owners={r['key'][0]:r['key'][2] for r in current['owners'] if r['key'][1]=='STATE_LOMBARDY'}
    actual=np.array([owners['x'+format(int(after[y,x]),'06X')]=='AUS' for x,y in cells])
    check('All 325 parent cells classified by reviewed source polygon only',np.array_equal(expected,actual) and len(cells)==325)
    check('Exactly 64 Venetian cells transferred, no artificial connecting dilation',int(actual.sum())==64 and geometry['parents']==['x4713EE'])
    old_aus=[int(r['key'][0][1:],16) for r in baseline['inventory']['owners'] if r['key'][1:]==['STATE_LOMBARDY','AUS']]
    new_aus=[int(r['key'][0][1:],16) for r in current['owners'] if r['key'][1:]==['STATE_LOMBARDY','AUS']]
    check('Austrian Lombardy previously had two disconnected components',len(components(np.isin(before,old_aus)))==2)
    check('Milan and Mantuan possessions now form one FOUR-connected land component',len(components(np.isin(after,new_aus)))==1)
    right_rows=json.loads(work.core.active_registry_path().read_text());rights={r['rgb']:r for r in right_rows}
    check('Only Austrian new child registered, Venetian child remains outside Empire',rights['xEDA701']['beneficiary']=='AUS' and 'xEDA700' not in rights and 'x4713EE' not in rights)
    owners_all={r['key'][0]:r['key'][2] for r in current['owners']}
    for name,point in [('Bergamo',[1169,433]),('Brescia',[1287,439]),('Crema',[1210,520]),('Asola',[1425,549])]:
        x,y=np.floor(np.array([*point,1])@matrix).astype(int);rgb='x'+format(int(after[y,x]),'06X')
        check('Retained historical Venetian town not assigned to Milan '+name,owners_all.get(rgb)=='VEN',rgb)
    anchors=json.loads((out/'NATIVE_ANCHORS.json').read_text())
    for r in anchors:
        x,y=int(float(r['Locator_X'])),int(float(r['Locator_Y']))
        check('Every Italian native locator retains its RGB '+r['Hub_Name'],after[y,x]==before[y,x])
    expected_outside=counter([r for r in baseline['inventory']['owners'] if r['key'][1]!='STATE_LOMBARDY'])
    lots=approved_lot_dirs()
    for later in lots[lots.index(out)+1:]:
        declared=json.loads((later/'REGISTRY_MIGRATION.json').read_text())
        for row in ownership_rows(declared,'previous'):
            if row['state']!='STATE_LOMBARDY':expected_outside[(row['rgb'],row['state'],row['beneficiary'])]-=1
        for row in ownership_rows(declared,'updated'):
            if row['state']!='STATE_LOMBARDY':expected_outside[(row['rgb'],row['state'],row['beneficiary'])]+=1
    check('Non-Lombard ownership unchanged except exact approved later migrations',
          +expected_outside==counter([r for r in current['owners'] if r['key'][1]!='STATE_LOMBARDY']))
    migration=json.loads((out/'REGISTRY_MIGRATION.json').read_text())
    check('Imperial mask gains precisely all returned cells and loses none',len(migration['extent_added_cells'])==64 and not migration['extent_removed_cells'])

def validate():
    validation.OUT=work.OUT
    validation.REGIONS={'STATE_LOMBARDY'}
    validation.REGION_FILE=work.core.REGION_FILE
    validation.CALIBRATION_CHECK=calibration
    validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
