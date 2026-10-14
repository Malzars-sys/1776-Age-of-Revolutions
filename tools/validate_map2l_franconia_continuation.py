"""Scoped source-envelope continuation and cumulative conservation validation.

Raster/source reproducibility is tested, not mislabelled as geographic accuracy.
The retained approximate fit is not optimized or certified by this validator.
"""
import json
import numpy as np
import validate_map2l_mainz as validation
import map2l_franconia_continuation as work
from map2l_belgium import packed
from map2l_franconia import inside


def source_checks(check,out,current,baseline,alignment,tracing,plan):
    retained=json.loads((out.parent/'FRANCONIA/TRACING.json').read_text())
    old_alignment=json.loads((out.parent/'FRANCONIA/ALIGNMENT.json').read_text())
    source=tracing['calibrated_sources'][0];matrix=np.array(source['matrix'])
    check('Retained Franconian matrix exactly reused, no optimization',
          source['matrix']==old_alignment['matrix_source_to_game'])
    for polygon in tracing['polygons']:
        matches=[p for p in retained['polygons'] if p['owner']==polygon['owner'] and p['jurisdiction']==polygon['territory']]
        check('Retained jurisdiction polygon unchanged '+polygon['territory'],
              len(matches)==1 and polygon['points']==matches[0]['points'])
    independent=next(p for p in source['controls'] if p['role']=='CHECK')
    residual=float(np.linalg.norm(np.array([*independent['source'],1])@matrix-independent['game']))
    check('Imperfect retained check disclosed, not falsely below three pixels',
          abs(residual-independent['residual_px'])<1e-9 and residual>3)
    geometry=json.loads((out/'GEOMETRY.json').read_text())
    before=packed(work.core.ROOT/baseline['bitmap_backup'])
    after=packed(work.core.ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in current['owners']}
    original_owners={r['key'][0]:r['key'][1:] for r in baseline['inventory']['owners']}
    check('Exactly four Bavarian parents, no prior Franconian polygon revisited',
          set(geometry['parents'])=={'x010AD7','x318021','x82F4B9','xA7094D'} and
          all(original_owners[r]==['STATE_BAVARIA','BAV'] for r in geometry['parents']))
    totals={}
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y))
        points=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2])
        expected=np.full(len(cells),'BAV',dtype='U3')
        for polygon in tracing['polygons']:
            if parent in polygon['parents']:
                expected[inside(points,polygon['points'])]=polygon['owner']
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells])
        check('Every parent cell classified by retained boundary '+parent,np.array_equal(expected,actual))
        for tag in ['ANS','EIC','FBM','NUR']:
            totals[tag]=totals.get(tag,0)+int((actual==tag).sum())
    check('Exactly 185 territorial cells reassigned, no broad provincial handover',
          totals=={'ANS':25,'EIC':59,'FBM':88,'NUR':13})
    # 25+59+88+13 = 185 cells; recolouring also splits untouched BAV pieces.
    check('Every owner outside Bavaria exactly unchanged',
          [r for r in current['owners'] if r['key'][1]!='STATE_BAVARIA']==
          [r for r in baseline['inventory']['owners'] if r['key'][1]!='STATE_BAVARIA'])
    anchors=json.loads((out/tracing['native_anchors']).read_text())
    for anchor in anchors:
        x,y=int(float(anchor['Locator_X'])),int(float(anchor['Locator_Y']))
        check('Retained local locator RGB unchanged '+anchor['Hub_Name'],after[y,x]==before[y,x])
    check('New subdivisions valid under existing countries',
          all(['STATE_BAVARIA',tag] in current['states'] for tag in totals))
    check('Conservation allocation uses nonnegative integers',
          all(isinstance(v,int) and v>=0 for r in plan['allocations'] for v in r['after'].values()))
    inputs={r['profile']:r['before'] for r in plan['allocations'] if r['kind']=='population'}
    check('Population profiles allocated exactly once',len(inputs)==3 and
          sum(inputs.values())==1311958+42901+3904)


def validate():
    validation.OUT=work.OUT
    validation.REGIONS=work.core.REGIONS
    validation.CALIBRATION_CHECK=source_checks
    validation.dump=work.core.dump
    return validation.validate()


if __name__=='__main__':raise SystemExit(validate())
