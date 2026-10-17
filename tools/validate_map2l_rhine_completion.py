"""Differential conservation and source-envelope replay, not runtime testing."""
import json
import re
import numpy as np
import validate_map2l_mainz as validation
import map2l_rhine_completion as work
from map2l_belgium import packed
from map2l_franconia import inside
import validate_diplomacy_ottoman_1776 as parser
from map_1776_audit import effective,values

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    previous=json.loads((out.parent/'RHINE_WESTPHALIA/TRACING.json').read_text())['calibrated_sources'][0]
    source=tracing['calibrated_sources'][0];matrix=np.array(source['matrix'])
    check('Original Rhine bridge reused without false Osnabruck control',source['matrix']==previous['matrix'] and not any(r['source']==[1130,1148] for r in source['controls']))
    residuals=[dict(name=r['name'],role=r['role'],locator_comparison_error_px=float(np.linalg.norm(np.array([*r['source'],1])@matrix-r['game'])),physical_accuracy_certified=False) for r in source['controls']]
    work.core.dump('CALIBRATION_DIAGNOSTICS.json',dict(points=residuals,refit=False,rejected_old_point=[1130,1148],rejected_reason='Inside the named Tecklenburg jurisdiction, not a reliable Osnabruck urban control',old_Minden_cells_changed=False,warning='Native locator residuals do not certify geographic precision; northern extrapolation not independently surveyed.'))
    check('Old Cologne/Bonn discrepancies explicitly retained',all(r['locator_comparison_error_px']>7 for r in residuals if r['role']=='CHECK'))
    before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png')
    geometry=json.loads((out/'GEOMETRY.json').read_text());owners={r['key'][0]:r['key'][2] for r in current['owners']}
    check('Six explicit originally HAN/OLD parents, no Westphalia recut',set(geometry['parents'])=={'x4D62A0','xBF00DF','x4101E0','x8080E0','x784B8E','xC00161'} and all(r['state']=='STATE_HANNOVER' for r in geometry['assignments']))
    totals={}
    oldowners={r['key'][0]:r['key'][2] for r in baseline['inventory']['owners']}
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y));sourcepoints=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=np.full(len(cells),oldowners[parent],dtype='U3')
        for polygon in tracing['polygons']:
            if parent not in polygon['parents']:continue
            selected=inside(sourcepoints,polygon['points'])
            for hole in polygon.get('exclusions',[]):selected&=~inside(sourcepoints,hole['points'])
            expected[selected]=polygon['owner']
            totals[polygon['territory']]=totals.get(polygon['territory'],0)+int(selected.sum())
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells])
        check('Every pixel exactly follows source envelopes '+parent,np.array_equal(expected,actual))
    work.core.dump('SOURCE_ENVELOPE_COUNTS.json',totals)
    check('159 Osnabruck, 265 Niederstift and 65 Prussian cells',sum(r['pixels'] for r in geometry['assignments'] if r['owner']=='WPO')==159 and sum(r['pixels'] for r in geometry['assignments'] if r['owner']=='WPM')==265 and sum(r['pixels'] for r in geometry['assignments'] if r['owner']=='PRU')==65)
    for folder in ['RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA']:
        prior=json.loads((out.parent/folder/'GEOMETRY.json').read_text())
        rows=prior['assignments'] if folder!='RHINE_WESTPHALIA' else [r for r in prior['assignments'] if r['owner']!=r['previous_owner'] or r['rgb'] in {v['rgb'] for v in prior['new_provinces']}]
        check('Every protected prior cell and owner intact '+folder,all(int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and owners[r['rgb']]==r['owner'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in rows))
    check('All eight EDAB colours and 84 Cologne cells preserved',sum(r['pixels'] for r in json.loads((out.parent/'DUCHY_WESTPHALIA/GEOMETRY.json').read_text())['assignments'] if r['owner']=='KCL')==84 and all(np.array_equal(before==int('EDAB'+format(i,'02X'),16),after==int('EDAB'+format(i,'02X'),16)) for i in range(8)))
    check('No hub position or RGB reference moved',geometry['hub_rebindings']==[] and all(before[int(float(r['Locator_Y'])),int(float(r['Locator_X']))]==after[int(float(r['Locator_Y'])),int(float(r['Locator_X']))] for r in json.loads((out/'NATIVE_ANCHORS.json').read_text())))
    check('No new world population, units or building-level creation',all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in plan['allocations']))
    check('Only one new independent imperial estate and valid owned capital',plan['new_tags']==['WPO'] and all(['STATE_HANNOVER',tag] in current['states'] for tag in ['WPO','WPM','PRU','HAN','OLD']))
    text=(work.core.ROOT/'common/history/countries/wpo - osnabruck.txt').read_text(encoding='utf-8-sig')
    tech=set(re.findall(r'add_technology_researched\s*=\s*(\w+)',text))
    law_nodes={n.key:n for path in effective(work.core.ROOT,work.core.qa.GAME,'common/laws') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for n in parser.walk(parser.parse(text)):
        if n.key!='activate_law':continue
        key=parser.scalar(n.value).split(':')[1]
        check('New starting law resolves and technology available '+key,key in law_nodes and set(values(law_nodes[key],'unlocking_technologies'))<=tech)
    check('Mixed confession and nominal episcopal polity, no invented annexation',all(key in text for key in ['law_theocracy','law_freedom_of_conscience']) and 'c:HAN' not in text and 'c:WPM' not in text)
    ruler=(work.core.ROOT/'common/history/characters/1776_map2l_osnabruck_ruler.txt').read_text()
    check('Historical minor Protestant prince not replaced by invented adult','age = 12' in ruler and 'rel:protestant' in ruler)
    check('Flag emblem asset exists',(work.core.qa.GAME/'gfx/coat_of_arms/colored_emblems/ce_ship_wheel.dds').is_file())
    for lang in ['english','french']:
        path=work.core.ROOT/f'localization/{lang}/1776_map2l_osnabruck_l_{lang}.yml'
        check('New localization names and BOM '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 ' in path.read_text(encoding='utf-8-sig') for key in ['WPO','WPO_ADJ','aor1776_wpo_first','aor1776_wpo_last']))
    from map2k_imperial_system import MEMBERS,ELECTORS
    check('Osnabruck member, not a fabricated elector','WPO' in MEMBERS and 'WPO' not in ELECTORS.values())

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS
    validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
