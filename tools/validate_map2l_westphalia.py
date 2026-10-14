"""Rhine/Westphalia differential and historical-envelope reproducibility QA.

The imperfect game/source correspondence is explicitly reported, not certified
as physical city accuracy. Country additions and RGB references are exact.
"""
import json
import re
import numpy as np
import validate_map2l_mainz as validation
import map2l_westphalia as work
import validate_diplomacy_ottoman_1776 as parser
from map2l_belgium import packed,sha
from map2l_franconia import inside
from map_1776_audit import effective,values
from map2l_registry import approved_lot_dirs,ownership_rows
from validate_map2a import counter


def source_checks(check,out,current,baseline,alignment,tracing,plan):
    source=tracing['calibrated_sources'][0];matrix=np.array(source['matrix'])
    fit=[row for row in source['controls'] if row['role']=='FIT']
    reproduced=np.linalg.solve(np.array([[*row['source'],1] for row in fit]),np.array([row['game'] for row in fit]))
    check('Three disclosed approximate source/game anchors reproduce matrix',np.allclose(matrix,reproduced,rtol=0,atol=1e-9))
    residuals=[]
    for row in source['controls']:
        error=float(np.linalg.norm(np.array([*row['source'],1])@matrix-row['game']))
        residuals.append(dict(name=row['name'],role=row['role'],error_pixels=error,independent_physical_position_certified=False))
    work.core.dump('CALIBRATION_DIAGNOSTICS.json',dict(points=residuals,
        warning='Game locator comparisons, not surveyed physical ground truth. No sub-two-pixel or cadastral accuracy claimed. Existing Erfurt model untouched.'))
    check('Independent Cologne and Bonn mismatches not concealed',[r['error_pixels']>3 for r in residuals if r['role']=='CHECK']==[True,True])
    geometry=json.loads((out/'GEOMETRY.json').read_text());before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in current['owners']}
    old={r['key'][0]:r['key'][1:] for r in baseline['inventory']['owners']}
    check('Eight reviewed parents originally Prussian in the three allowed regions',len(geometry['parents'])==8 and all(old[r][0] in work.core.REGIONS and old[r][1]=='PRU' for r in geometry['parents']))
    totals={}
    lots=approved_lot_dirs();later=lots[lots.index(out)+1:]
    later_geometries=[json.loads((lot/'GEOMETRY.json').read_text()) for lot in later]
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y))
        points=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=np.full(len(cells),'PRU',dtype='U3')
        for polygon in tracing['polygons']:
            if parent not in polygon['parents']:continue
            selected=inside(points,polygon['points'])
            for hole in polygon.get('exclusions',[]):selected&=~inside(points,hole['points'])
            expected[selected]=polygon['owner']
        lookup={(int(cx),int(cy)):i for i,(cx,cy) in enumerate(cells)}
        for geo in later_geometries:
            for row in geo['assignments']:
                for cx,cy in row['cells']:
                    index=lookup.get((cx,cy))
                    if index is not None:expected[index]=row['owner']
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells])
        check('Every cell follows original source boundary and exact later reviewed corrections '+parent,np.array_equal(actual,expected))
        for tag in ['WPM','WPD','KPF']:totals[tag]=totals.get(tag,0)+int((actual==tag).sum())
    check('Exactly 1081 ownership cells restored',totals=={'WPM':427,'WPD':296,'KPF':358})
    expected_outside=counter([r for r in baseline['inventory']['owners'] if r['key'][1] not in work.core.REGIONS])
    lots=approved_lot_dirs()
    for later_lot in lots[lots.index(out)+1:]:
        declared=json.loads((later_lot/'REGISTRY_MIGRATION.json').read_text())
        for row in ownership_rows(declared,'previous'):
            if row['state'] not in work.core.REGIONS:expected_outside[(row['rgb'],row['state'],row['beneficiary'])]-=1
        for row in ownership_rows(declared,'updated'):
            if row['state'] not in work.core.REGIONS:expected_outside[(row['rgb'],row['state'],row['beneficiary'])]+=1
    check('All owners outside this lot unchanged except exact later reviewed migrations',
          +expected_outside==counter([r for r in current['owners'] if r['key'][1] not in work.core.REGIONS]))
    for tag in ['KCL','LIP','SCM']:
        expected_tag=counter([r for r in baseline['inventory']['owners'] if r['key'][2]==tag])
        for lot in later:
            declared=json.loads((lot/'REGISTRY_MIGRATION.json').read_text())
            for row in ownership_rows(declared,'previous'):
                if row['beneficiary']==tag:expected_tag[(row['rgb'],row['state'],tag)]-=1
            for row in ownership_rows(declared,'updated'):
                if row['beneficiary']==tag:expected_tag[(row['rgb'],row['state'],tag)]+=1
        check('Existing electorate/county allocation unchanged except exact later reviewed corrections '+tag,
              +expected_tag==counter([r for r in current['owners'] if r['key'][2]==tag]))
    regions={n.key:n for n in parser.parse((work.core.ROOT/'map_data/state_regions/00_west_europe.txt').read_text(encoding='utf-8-sig'))}
    original_regions={n.key:n for n in parser.parse(baseline['originals']['map_data/state_regions/00_west_europe.txt'])}
    for sid in work.core.REGIONS:
        old_prime=values(original_regions[sid],'prime_land');new_prime=values(regions[sid],'prime_land')
        check('Exact prime-land pixel footprint conserved '+sid,
              np.array_equal(np.isin(before,[int(r[1:],16) for r in old_prime]),np.isin(after,[int(r[1:],16) for r in new_prime])))
    anchors=json.loads((out/'NATIVE_ANCHORS.json').read_text());bindings=geometry['hub_rebindings']
    for row in anchors:
        x,y=int(float(row['Locator_X'])),int(float(row['Locator_Y']));binding=next((r for r in bindings if r['state']==row['State_ID'] and r['field']==row['Hub_Type']),None)
        expected_rgb=int(binding['after'][1:],16) if binding else int(before[y,x])
        check('Unmoved locator exact identity or declared rebinding '+row['Hub_Name'],int(after[y,x])==expected_rgb)
        if binding:
            check('Rebound state field resolves actual sampled child '+row['Hub_Name'],parser.scalar(regions[row['State_ID']].one(row['Hub_Type']))==binding['after'])
    check('Exactly the two reviewed locator reference updates',
          {(r['state'],r['field']) for r in bindings}=={('STATE_WESTPHALIA','wood'),('STATE_RUHR','mine')})
    # Sampling the historical printed marker is not treated as a sovereignty proof
    # for an entire parent; these checks concern only the unchanged engine hubs.
    for name,tag in [('Düsseldorf','KPF'),('Münster','WPM'),('Paderborn','WPD')]:
        row=next(r for r in anchors if r['Hub_Name']==name);x,y=int(float(row['Locator_X'])),int(float(row['Locator_Y']))
        check('Core engine anchor remains represented '+name,owners['x'+format(int(after[y,x]),'06X')]==tag)
    check('Existing Prussian recruiting subdivisions survive',all([sid,'PRU'] in current['states'] for sid in work.core.REGIONS))
    declared_new={'WPM','WPD'} | {tag for lot in later for tag in json.loads((lot/'REGISTRY_MIGRATION.json').read_text()).get('country_additions',{})}
    check('Exactly two original countries and explicit later additions',set(current['countries'])-set(baseline['inventory']['countries'])==declared_new)
    law_nodes={n.key:n for path in effective(work.core.ROOT,work.core.qa.GAME,'common/laws') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    template=(work.core.ROOT/'common/history/countries/fbm - franconian estate.txt').read_text(encoding='utf-8-sig')
    template_tech=set(re.findall(r'add_technology_researched\s*=\s*(\w+)',template))
    for tag in ['WPM','WPD']:
        check('New capital State Region is actually owned '+tag,['STATE_WESTPHALIA',tag] in current['states'])
        text=(work.core.ROOT/f'common/history/countries/{tag.lower()} - westphalian estate.txt').read_text(encoding='utf-8-sig')
        nodes=list(parser.walk(parser.parse(text)));tech={parser.scalar(n.value) for n in nodes if n.key=='add_technology_researched'}
        check('Existing early-modern template reused without extra technology '+tag,tech==template_tech and 'national_sovereignty' not in tech)
        for node in nodes:
            if node.key!='activate_law':continue
            key=parser.scalar(node.value).split(':')[1]
            check('Starting law and required research resolve '+tag+' '+key,key in law_nodes and set(values(law_nodes[key],'unlocking_technologies'))<=tech)
    for key in ['law_aor1776_westphalian_customs','law_aor1776_westphalian_free_status']:
        check('New law variant restricted to these two estates '+key,
              all('c:'+tag in (work.core.ROOT/'common/laws/1776_map2l_westphalian_start_variants.txt').read_text() for tag in ['WPM','WPD']) and parser.scalar(law_nodes[key].one('parent')) in law_nodes)
    for lang in ['french','english']:
        path=work.core.ROOT/f'localization/{lang}/1776_map2l_westphalia_l_{lang}.yml';text=path.read_text(encoding='utf-8-sig')
        check('Names/rulers/legal descriptions localized with BOM '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 ' in text for key in ['WPM','WPD','WPM_ADJ','WPD_ADJ','aor1776_wpm_first','aor1776_wpm_last','aor1776_wpd_first','aor1776_wpd_last','law_aor1776_westphalian_customs_desc','law_aor1776_westphalian_free_status_desc']))
    from map2k_imperial_system import MEMBERS,ELECTORS
    check('New estates members, neither invented electors nor new Cologne',{'WPM','WPD'}<=set(MEMBERS) and not {'WPM','WPD'}&set(ELECTORS.values()))
    check('Every new allocation nonnegative integer and input conserved',all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in plan['allocations']))
    check('No buildings file modified in this conservative allocation',not any('/buildings/' in path for path in plan['files']))


def validate():
    validation.OUT=work.OUT
    validation.REGIONS=work.core.REGIONS
    validation.CALIBRATION_CHECK=source_checks
    validation.dump=work.core.dump
    return validation.validate()


if __name__=='__main__':raise SystemExit(validate())
