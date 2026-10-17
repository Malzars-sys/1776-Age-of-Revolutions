"""Exact Swabian finish scope and conservation, not automated game loading."""
import json,re
import numpy as np
import map2l_swabia_finish as work
import validate_map2l_mainz as validation
import validate_diplomacy_ottoman_1776 as parser
from map2l_belgium import packed,sha
from map2l_franconia import inside
from map_1776_audit import effective,values

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    root=work.core.ROOT;before=packed(root/baseline['bitmap_backup']);after=packed(root/'map_data/provinces.png');g=json.loads((out/'GEOMETRY.json').read_text());t=np.array(tracing['calibrated_sources'][0]['matrix'])
    old={r['key'][0]:r['key'][2] for r in baseline['inventory']['owners']};owners={r['key'][0]:r['key'][2] for r in current['owners']}
    from map2l_registry import approved_lot_dirs,protected_core_preserved
    lots=approved_lot_dirs();later=lots[lots.index(out)+1:]
    check('Three exact provisional Swabian parents only',set(g['parents'])=={'xAEBA2A','xDBB84C','x704A5F'})
    for parent in g['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y));src=(cells+.5-t[2])@np.linalg.inv(t[:2]);expected=np.full(len(cells),old[parent],dtype='U3')
        for p in tracing['polygons']:
            if parent in p['parents']:expected[inside(src,p['points'])]=p['owner']
        positions={tuple(point):i for i,point in enumerate(cells)}
        for directory in later:
            for row in json.loads((directory/'GEOMETRY.json').read_text())['assignments']:
                for cx,cy in row['cells']:
                    index=positions.get((cx,cy))
                    if index is not None:
                        assert expected[index]==row['owner'] or expected[index]==old[parent], 'Later lot cannot alter a restored finish core'
                        expected[index]=row['owner']
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells]);check('Exact source envelope replay '+parent,np.array_equal(actual,expected))
    scope=np.isin(before,[int(r[1:],16) for r in g['parents']]);expected_raster=before.copy()
    for directory in later:
        for row in json.loads((directory/'GEOMETRY.json').read_text())['assignments']:
            for x,y in row['cells']:
                if not scope[y,x]:expected_raster[y,x]=int(row['rgb'][1:],16)
    check('Raster outside three masks identical except exact approved later cells',np.array_equal(expected_raster[~scope],after[~scope]))
    for name,total in [('SWABIA',211),('SWABIA_CONTINUATION',92)]:
        prior=json.loads((out.parent/name/'GEOMETRY.json').read_text());rows=[r for r in prior['assignments'] if r['source_zone']]
        check('All restored cores preserved with exact declared city exception '+name,sum(r['pixels'] for r in rows)==total and all(protected_core_preserved(r,after,owners,later) for r in rows))
    check('Exactly 63 justified ownership cells',sum(r['pixels'] for r in g['assignments'] if r['owner']!=r['previous_owner'])==63 and {tag:sum(r['pixels'] for r in g['assignments'] if r['owner']==tag) for tag in work.TAGS}=={'SLM':6,'SWW':8,'SWF':18,'SWX':19,'SWY':8,'SKC':4})
    check('No France/Alsace/Montbeliard/Erfurt transfer',all(r['state'] in {'STATE_BADEN','STATE_WURTTEMBERG','STATE_BAVARIA'} for r in g['assignments']))
    check('Six unused tags only, Sweden Swaziland Swat untouched',plan['new_tags']==work.TAGS and not set(work.TAGS)&set(baseline['inventory']['countries']) and all(current['countries'][tag]==baseline['inventory']['countries'][tag] for tag in ['SWE','SWZ','SWT']))
    for tag,sid in [('SLM','STATE_BADEN'),('SWW','STATE_WURTTEMBERG'),('SWF','STATE_WURTTEMBERG'),('SWX','STATE_WURTTEMBERG'),('SWY','STATE_WURTTEMBERG'),('SKC','STATE_BADEN')]:check('Capital in owned subdivision '+tag,[sid,tag] in current['states'])
    bindings=g['hub_rebindings'];check('One exact economic hub RGB rebound, no moved point',len(bindings)==1 and bindings[0]['state']=='STATE_WURTTEMBERG' and bindings[0]['field']=='mine' and bindings[0]['name']=='Lindau' and bindings[0]['pixel']==[4316,927] and bindings[0]['before']=='xDBB84C')
    for rel,digest in baseline['hashes'].items():
        if rel.startswith('gfx/map/map_object_data/'):check('No locator file edited '+rel,sha(root/rel)==digest)
    laws={n.key:n for path in effective(root,work.core.qa.GAME,'common/laws') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for tag in work.TAGS:
        raw=(root/f'common/history/countries/{tag.lower()} - swabia finish.txt').read_text(encoding='utf-8-sig');tech=set(re.findall(r'add_technology_researched\s*=\s*(\w+)',raw))
        for node in parser.walk(parser.parse(raw)):
            if node.key=='activate_law':
                key=parser.scalar(node.value).split(':')[1];check('Start law and technology resolve '+tag+' '+key,key in laws and set(values(laws[key],'unlocking_technologies'))<=tech)
    governments=parser.parse((root/'common/government_types/00_1776_map2l_swabia_finish.txt').read_text());effects={n.key for path in effective(root,work.core.qa.GAME,'common/scripted_effects') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for n in governments:
        power=parser.scalar(n.one('transfer_of_power'));check('Native succession hooks '+n.key,'change_to_'+power in effects and 'post_change_to_'+power in effects and power in {'hereditary','dictatorial'})
    for lang in ['english','french']:
        path=root/f'localization/{lang}/1776_map2l_swabia_finish_l_{lang}.yml';text=path.read_text(encoding='utf-8-sig');keys=work.TAGS+[tag+'_ADJ' for tag in work.TAGS]+[n.key+suffix for n in governments for suffix in ['', '_desc']]
        check('Names and government descriptions localised '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 "' in text for key in keys))
    from map2k_imperial_system import MEMBERS,ELECTORS
    from map2l_registry import additional_free_cities
    check('Imperial members, no invented elector or free city',set(work.TAGS)<=set(MEMBERS) and not set(work.TAGS)&(set(ELECTORS.values())|set(additional_free_cities())))
    diagnostics=json.loads((out/'ATLAS_CORRESPONDENCE.json').read_text());check('Fit residual not falsely labelled independent physical accuracy',diagnostics['physical_accuracy_certified'] is False and diagnostics['matrix']==tracing['calibrated_sources'][0]['matrix'])
    check('Primary 1765 Salem map unchanged and original dimensions',sha(out/'EVIDENCE/SALEM_1765.jpg')==json.loads((out/'SOURCES.json').read_text())['salem']['sha256'])

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS;validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
