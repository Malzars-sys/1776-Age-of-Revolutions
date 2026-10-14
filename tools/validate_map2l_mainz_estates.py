"""Mainz estates: cumulative differential QA plus reproducible local calibration."""
import collections as C
import json
import numpy as np
import validate_map2l_mainz as validation
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map_1776_audit import effective
from map2l_mainz import ROOT
from map2l_belgium import packed
from map2l_franconia import inside

OUT=ROOT/'docs/reports/map/MAP2L/MAINZ_ESTATES'

def validate_calibration(check,out,current,baseline,alignment,tracing,plan):
    hl=next(r for r in alignment['sources'] if r['key']=='HL')
    fit=[r for r in hl['controls'] if r['source_role']=='FIT']
    points=np.array([r['source']+[1] for r in fit],dtype=float)
    geo=np.array([r['geo_lon_lat'] for r in fit])
    source_matrix=np.linalg.lstsq(points,geo,rcond=None)[0]
    native=hl['native_geo_controls']
    native_matrix=np.linalg.lstsq(np.array([r['geo_lon_lat']+[1] for r in native]),np.array([r['game'] for r in native]),rcond=None)[0]
    composite=np.column_stack((source_matrix,[0,0,1]))@native_matrix
    check('Source-to-geography fit reproduced',np.allclose(source_matrix,hl['matrix_source_to_geo'],atol=1e-10,rtol=0))
    check('Native local geography fit reproduced',np.allclose(native_matrix,hl['matrix_geo_to_game'],atol=1e-6,rtol=0))
    check('Two-stage source-to-game matrix reproduced',np.allclose(composite,hl['matrix'],atol=1e-6,rtol=0))
    residual=np.linalg.norm((points@source_matrix-geo)@native_matrix[:2],axis=1)
    check('Stored source residuals reproduced',np.allclose(residual,hl['source_fit_residuals_game_px'],atol=1e-7,rtol=0))
    test=next(r for r in hl['controls'] if r['source_role']=='CHECK')
    error=float(np.linalg.norm((np.array(test['source']+[1])@source_matrix-np.array(test['geo_lon_lat']))@native_matrix[:2]))
    check('Independent Wertheim check under one game pixel',abs(error-hl['independent_source_check_game_px'])<1e-7 and error<1, str(error)+'; not a cadastral boundary confidence estimate')
    geometry=json.loads((out/'GEOMETRY.json').read_text())
    for row in geometry['assignments']:
        if not row['source_zone']:continue
        polygon=tracing['polygons'][row['source_zone']-1]
        source=next(s for s in alignment['sources'] if s['key']==polygon['source'])
        matrix=np.array(source['matrix']);inverse=np.linalg.inv(matrix[:2])
        xy=np.array(row['cells'],dtype=float)+.5
        points=(xy-matrix[2])@inverse
        take=inside(points,polygon['points'])
        for hole in polygon.get('exclusions',[]):take&=~inside(points,hole['points'])
        check('Every traced cell inside jurisdiction and outside exclusions '+row['rgb'],bool(take.all()) and row['owner']==polygon['owner'])
    # Compare planned inputs to original populations, not the evolving edited tree.
    inputs=C.Counter()
    for alloc in plan['allocations']:
        if alloc['kind']=='population':
            culture,religion=alloc['profile'].split('/')
            inputs[(alloc['state'],alloc['source'],culture,'DEFAULT:'+culture if religion=='DEFAULT' else religion)]+=alloc['before']
    before={tuple(r['key']):r['count'] for r in baseline['inventory']['regional_pop']}
    check('Every allocation input taken exactly once from immutable baseline',all(before[k]==v for k,v in inputs.items()))
    check('All allocated population and building quantities nonnegative integers',all(isinstance(v,int) and v>=0 for alloc in plan['allocations'] for v in alloc['after'].values()))
    def private_holders(original):
        result=C.Counter()
        for path in effective(ROOT,qa.GAME,'common/history/buildings'):
            rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
            raw=baseline['originals'].get(rel,path.read_text(encoding='utf-8-sig')) if original else path.read_text(encoding='utf-8-sig')
            for region in cw.walk(cw.parse(raw)):
                if not region.key.startswith('s:STATE_'):continue
                for subdivision in region.children():
                    if not subdivision.key.startswith('region_state:'):continue
                    for building in subdivision.children('create_building'):
                        for ownership in building.children('add_ownership'):
                            for holder in ownership.children('building'):
                                signature=json.dumps([qa.norm(n) for n in holder.children() if n.key!='levels'],sort_keys=True)
                                result[(region.key,building.one('building'),signature)]+=int(holder.one('levels'))
        return result
    check('Private ownership levels and every holder attribute conserved',private_holders(True)==private_holders(False))
    bmp=packed(ROOT/'map_data/provinces.png')
    anchors=json.loads((out.parent/'RHINE_CENTRAL/NATIVE_ANCHORS.json').read_text())
    owners={tuple(r['key']):r['count'] for r in current['owners']}
    for name,tag in [('Fulda','HEK'),('Würzburg','WZB'),('Frankfurt','FRM')]:
        anchor=next(r for r in anchors if r['Hub_Name']==name)
        x,y=int(float(anchor['Locator_X'])),int(float(anchor['Locator_Y']))
        rgb='x'+format(int(bmp[y,x]),'06X')
        check('Protected native hub controller '+name,owners.get((rgb,anchor['State_ID'],tag))==1)

def validate():
    validation.OUT=OUT
    validation.REGIONS={'STATE_HESSE','STATE_BADEN','STATE_FRANCONIA'}
    def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    validation.dump=dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
