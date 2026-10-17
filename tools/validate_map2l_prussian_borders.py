"""Differential checks for the conservative Swedish northern coastal core."""
import json
import numpy as np
import map2l_prussian_borders as work
import validate_map2l_mainz as validation
from map2l_registry import territorial_holder_overrides,rightful_holder_condition
from map2l_belgium import packed,sha

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    root=work.core.ROOT
    before=packed(root/baseline['bitmap_backup']);after=packed(root/'map_data/provinces.png')
    geometry=json.loads((out/'GEOMETRY.json').read_text())
    check('Whole existing province; no manufactured frontier or new RGB',geometry['parents']==['x567452'] and geometry['new_provinces']==[] and np.array_equal(before,after))
    owners={r['key'][0]:r['key'][2] for r in current['owners']}
    check('Northern Swedish core unique 341 cells',owners['x567452']=='SWE' and int((after==0x567452).sum())==341)
    check('Unresolved mainland remains Prussian',all(owners[r]=='PRU' for r in ['xE1A03A','xA04121','x6A53CF']))
    check('Danzig remains Polish and Thorn unchanged pending fine boundary',owners['x80A0A0']=='PLC' and owners['x41A021']=='PRU')
    check('Netze not silently completed by a town locator',owners['xFCC7B7']=='PLC')
    check('No new country and Swedish capital/government preserved',plan['new_tags']==[] and current['countries']==baseline['inventory']['countries'])
    from map2k_imperial_system import MEMBERS,ELECTORS
    check('Sweden not added to imperial country membership or electorate','SWE' not in MEMBERS and 'SWE' not in ELECTORS.values())
    overrides=territorial_holder_overrides()
    check('External ducal title explicitly restricted to Pomerania',overrides=={'SWE':{'STATE_POMERANIA'}})
    registry=json.loads((out.parent/'IMPERIAL_DE_JURE_REGISTRY.json').read_text())
    check('Only the reviewed Swedish core registered, not Sweden proper',[r['rgb'] for r in registry if r['beneficiary']=='SWE']==['x567452'])
    check('Surviving Swedish territorial right does not require false bloc membership',rightful_holder_condition(dict(beneficiary='SWE',state='STATE_POMERANIA'))=='exists = c:SWE')
    check('Other imperial beneficiaries still require real membership','aor1776_hre_member = yes' in rightful_holder_condition(dict(beneficiary='PRU',state='STATE_BRANDENBURG')))
    check('Projection is explicitly not claimed as calibrated','not a source-to-game calibration' in tracing['calibrated_sources'][0]['basis'])
    check('No out-of-scope Prussian economic edits',all(sha(root/rel)==digest for rel,digest in baseline['hashes'].items() if rel.startswith('common/history/buildings/') and ('prussia' in rel or 'prussian' in rel)))
    check('No other territorial region or historical lot changed',all(sha(root/rel)==digest for rel,digest in baseline['hashes'].items() if rel.startswith('map_data/state_regions/') and rel!='map_data/state_regions/00_west_europe.txt'))

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS
    def dump(name,data):
        if name=='VALIDATION.json':
            data.update(runtime_status='NOT_YET_TESTED',completion_status='PARTIAL_NORTHERN_COASTAL_CORE_ONLY',cumulative_scope='All prior effective reviewed geometry and exact baseline preservation; not a fresh run of all 17 historical scripts')
        work.core.dump(name,data)
    validation.dump=dump;validation.CALIBRATION_CHECK=source_checks
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
