"""Exact conservation and protected-core checks; no cadastral certification."""
import json,re
import numpy as np
import map2l_swabia_continuation as work
import validate_map2l_mainz as validation
import validate_diplomacy_ottoman_1776 as parser
from map2l_belgium import packed
from map2l_franconia import inside
from map_1776_audit import effective,values

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png');geometry=json.loads((out/'GEOMETRY.json').read_text());matrix=np.array(tracing['calibrated_sources'][0]['matrix'])
    old={r['key'][0]:r['key'][2] for r in baseline['inventory']['owners']};owners={r['key'][0]:r['key'][2] for r in current['owners']}
    check('Six exact provisional parents only',set(geometry['parents'])=={'xB00160','xEDAD00','x8F0060','xAEBA2A','x118060','xEDA218'})
    from map2l_registry import approved_lot_dirs,expected_locator_rgb
    lots=approved_lot_dirs();later=lots[lots.index(out)+1:]
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y));src=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=np.full(len(cells),old[parent],dtype='U3')
        for p in tracing['polygons']:
            if parent in p['parents']:expected[inside(src,p['points'])]=p['owner']
        positions={(int(cx),int(cy)):i for i,(cx,cy) in enumerate(cells)}
        for directory in later:
            for row in json.loads((directory/'GEOMETRY.json').read_text())['assignments']:
                for cx,cy in row['cells']:
                    index=positions.get((cx,cy))
                    if index is not None:
                        assert expected[index]==old[parent], 'Later lot must not modify a restored SFU/SEW core'
                        expected[index]=row['owner']
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells]);check('Exact reviewed source envelope '+parent,np.array_equal(actual,expected))
    protected=~np.isin(before,[int(r[1:],16) for r in geometry['parents']]);expected_raster=before.copy()
    for directory in later:
        for row in json.loads((directory/'GEOMETRY.json').read_text())['assignments']:
            for x,y in row['cells']:
                if protected[y,x]:expected_raster[y,x]=int(row['rgb'][1:],16)
    check('Every pixel outside six masks unchanged except exact later reviewed cells',np.array_equal(expected_raster[protected],after[protected]))
    restored=[r for r in geometry['assignments'] if r['source_zone']]
    check('All 92 SFU/SEW ownership cells and RGBs protected',sum(r['pixels'] for r in restored)==92 and all(owners[r['rgb']]==r['owner'] and int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in restored))
    prior=json.loads((work.previous.OUT/'GEOMETRY.json').read_text());core_rows=[r for r in prior['assignments'] if r['source_zone']]
    from map2l_registry import protected_core_preserved
    check('All 211 prior core cells exact except explicit single-cell Kempten authorisation',sum(r['pixels'] for r in core_rows)==211 and all(protected_core_preserved(r,after,owners,later) for r in core_rows))
    check('All fourteen prior RGB identities survive',all(np.any(after==int(r['rgb'][1:],16)) for r in prior['new_provinces']))
    for name in ['RHINE_WESTPHALIA_COMPLETION','DUCHY_WESTPHALIA','MINDEN_RAVENSBERG','FRANCONIA_CONTINUATION','MILAN_CREMONESE']:
        previous=json.loads((out.parent/name/'GEOMETRY.json').read_text());check('All reviewed cells preserved '+name,all(owners[r['rgb']]==r['owner'] and int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in previous['assignments']))
    check('Exactly 92 ownership cells for two estates',geometry['transfers']=={'STATE_BADEN/BAD->SFU':71,'STATE_WURTTEMBERG/WUR->SFU':1,'STATE_WURTTEMBERG/WUR->SEW':2,'STATE_FRANCONIA/BAV->SEW':18})
    check('Franconia dependency restricted to its retained Bavarian fringe',set(r['parent_rgb'] for r in geometry['assignments'] if r['state']=='STATE_FRANCONIA')=={'xEDA218'})
    check('Original continuation has no locator movement; exact later RGB rebindings only',geometry['hub_rebindings']==[] and all(expected_locator_rgb(int(before[int(float(r['Locator_Y'])),int(float(r['Locator_X']))]),(int(float(r['Locator_X'])),int(float(r['Locator_Y']))),later)==after[int(float(r['Locator_Y'])),int(float(r['Locator_X']))] for r in json.loads((out/'NATIVE_ANCHORS.json').read_text())))
    check('Two new countries only',plan['new_tags']==work.TAGS)
    for tag,sid in [('SFU','STATE_BADEN'),('SEW','STATE_FRANCONIA')]:check('Capital in owned shared subdivision '+tag,[sid,tag] in current['states'])
    laws={n.key:n for path in effective(work.core.ROOT,work.core.qa.GAME,'common/laws') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for tag in work.TAGS:
        raw=(work.core.ROOT/f'common/history/countries/{tag.lower()} - swabia continuation.txt').read_text(encoding='utf-8-sig');tech=set(re.findall(r'add_technology_researched\s*=\s*(\w+)',raw))
        for n in parser.walk(parser.parse(raw)):
            if n.key=='activate_law':
                key=parser.scalar(n.value).split(':')[1];check('Law technologies resolve '+tag+' '+key,key in laws and set(values(laws[key],'unlocking_technologies'))<=tech)
    governments=parser.parse((work.core.ROOT/'common/government_types/00_1776_map2l_swabia_continuation.txt').read_text())
    effects={n.key for path in effective(work.core.ROOT,work.core.qa.GAME,'common/scripted_effects') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    native_powers={parser.scalar(n.value) for path in effective(work.core.ROOT,work.core.qa.GAME,'common/government_types') if path.name!='00_1776_map2l_swabia_continuation.txt' for n in parser.walk(parser.parse(path.read_text(encoding='utf-8-sig'))) if n.key=='transfer_of_power'}
    for g in governments:
        power=parser.scalar(g.children('transfer_of_power')[0].value)
        check('Native government succession and hooks resolve '+g.key,power in native_powers and 'change_to_'+power in effects and 'post_change_to_'+power in effects)
    for lang in ['english','french']:
        path=work.core.ROOT/f'localization/{lang}/1776_map2l_swabia_continuation_l_{lang}.yml';text=path.read_text(encoding='utf-8-sig')
        keys=work.TAGS+[t+'_ADJ' for t in work.TAGS]+['aor1776_prince_provost_title']+[n.key+suffix for n in governments for suffix in ['', '_desc']]
        check('Government names descriptions countries and BOM resolve '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 "' in text for key in keys))
    characters=(work.core.ROOT/'common/history/characters/1776_map2l_swabia_continuation.txt').read_text()
    check('Dated prince and nominal prince-provost, no 1787 successor','birth_date = 1728.3.21' in characters and 'age = 64' in characters and 'Clemens' not in characters)
    from map2k_imperial_system import MEMBERS,ELECTORS
    check('Both new members, no invented electoral vote',set(work.TAGS)<=set(MEMBERS) and not set(work.TAGS)&set(ELECTORS.values()))
    check('No population invention in any allocation',all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in plan['allocations']))
    holdout=[r for r in tracing['calibrated_sources'][0]['controls'] if r['role']=='CHECK'][0]
    residual=float(np.linalg.norm(np.array([*holdout['source'],1])@matrix-holdout['game']))
    check('Inherited independent mismatch disclosed without claiming exact georeferencing',residual>9 and tracing['calibrated_sources'][0]['matrix']==json.loads((work.previous.OUT/'TRACING.json').read_text())['calibrated_sources'][0]['matrix'])
    work.core.dump('CALIBRATION_DIAGNOSTICS.json',dict(holdout_locator_error_px=residual,physical_accuracy_certified=False,reoptimized=False,warning='Native economic locator mismatch is not a certified urban-centre error; polygons are macro approximations, not cadastral boundaries'))

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS;validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
