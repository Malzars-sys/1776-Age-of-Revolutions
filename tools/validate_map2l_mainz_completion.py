"""Southern completion checks, including explicit northern non-implementation."""
import json
import numpy as np
import validate_map2l_mainz as validation
from map2l_belgium import packed
from map2l_franconia import inside
from map2l_mainz import ROOT

OUT=ROOT/'docs/reports/map/MAP2L/MAINZ_COMPLETION'

def validate_southern_controls(check,out,current,baseline,alignment,tracing):
    source=next(row for row in alignment['sources'] if row['key']=='HL')
    matrix=np.array(source['matrix']);geo=np.array(source['matrix_source_to_geo']);game=np.array(source['matrix_geo_to_game'])
    owners={tuple(row['key']):row['count'] for row in current['owners']}
    bmp=packed(ROOT/'map_data/provinces.png')
    for row in tracing['southern_controls']:
        point=np.array(row['source']+[1]);predicted=point@matrix
        error=float(np.linalg.norm((point@geo-np.array(row['geo_lon_lat']))@game[:2]))
        check('Independent southern source check '+row['name'],row['role']=='CHECK' and error<1,str(error)+' game pixel equivalent; source check, not an independent proof of game geography')
        # A drawn town symbol can straddle a cell edge (Tauber projects to
        # x=4313.999949). Verify the continuous jurisdiction first; do not
        # enlarge the raster boundary or call a floor sample cadastral proof.
        jurisdiction=False
        for polygon in tracing['polygons']:
            take=inside(np.array([row['source']]),polygon['points'])
            for hole in polygon.get('exclusions',[]):take&=~inside(np.array([row['source']]),hole['points'])
            jurisdiction|=bool(take[0])
        check('Town symbol inside traced Mainz jurisdiction '+row['name'],jurisdiction)
        represented=[];x0,y0=np.floor(predicted).astype(int)
        for y in range(y0-1,y0+2):
            for x in range(x0-1,x0+2):
                if np.linalg.norm(np.array([x+.5,y+.5])-predicted)>.75:continue
                rgb='x'+format(int(bmp[y,x]),'06X');sid=current['geometry'][rgb]
                if owners.get((rgb,sid,'KMZ'))==1:represented.append(rgb)
        check('Town represented by a Mainz cell within subpixel footprint '+row['name'],bool(represented),str(represented)+'; 0.75 pixel centre-distance, no border enlargement')
    north={'STATE_SAXONY','STATE_HANNOVER','STATE_BRUNSWICK','STATE_ANHALT','STATE_WESTPHALIA','STATE_HESSE'}
    check('Every northern territorial owner left unchanged',
        [r for r in current['owners'] if r['key'][1] in north]==[r for r in baseline['inventory']['owners'] if r['key'][1] in north])
    assessment=json.loads((out/'NORTHERN_CALIBRATION_ASSESSMENT.json').read_text())
    check('Rejected northern calage neither silently accepted nor installed',assessment['status']=='REJECTED_NOT_APPLIED' and min(row['error_px'] for row in assessment['first_checks'])>9)

def validate():
    validation.OUT=OUT;validation.REGIONS={'STATE_BADEN','STATE_WURTTEMBERG'}
    def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    validation.dump=dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
