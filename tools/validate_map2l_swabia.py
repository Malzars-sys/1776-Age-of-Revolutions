"""Swabian differential QA: exact data conservation, approximate geography."""
import json
import re
import numpy as np
import map2l_swabia as work
import validate_map2l_mainz as validation
import validate_diplomacy_ottoman_1776 as parser
from map2l_belgium import packed
from map2l_franconia import inside
from map_1776_audit import effective,values

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    source=tracing['calibrated_sources'][0];matrix=np.array(source['matrix'])
    fit=[r for r in source['controls'] if r['role']=='FIT']
    reproduced=np.linalg.lstsq(np.array([[*r['source'],1] for r in fit]),np.array([r['game'] for r in fit]),rcond=None)[0]
    check('Five-point approximate correspondence reproducible',np.allclose(matrix,reproduced,rtol=0,atol=1e-9))
    residuals=[dict(name=r['name'],role=r['role'],native_locator_error_px=float(np.linalg.norm(np.array([*r['source'],1])@matrix-r['game'])),physical_accuracy_certified=False) for r in source['controls']]
    holdouts=[r['native_locator_error_px'] for r in residuals if r['role']=='CHECK']
    work.core.dump('CALIBRATION_DIAGNOSTICS.json',dict(points=residuals,holdout_mean_px=float(np.mean(holdouts)),holdout_max_px=max(holdouts),warning='Economic locators, not surveyed urban centres. Lindau mismatch retained; no cadastral accuracy claimed. Erfurt profile untouched.'))
    check('Large independent Lindau mismatch disclosed, not threshold-waived',len(holdouts)==1 and holdouts[0]>9)
    before=packed(work.core.ROOT/baseline['bitmap_backup']);after=packed(work.core.ROOT/'map_data/provinces.png');geometry=json.loads((out/'GEOMETRY.json').read_text())
    owners={r['key'][0]:r['key'][2] for r in current['owners']};old={r['key'][0]:r['key'][2] for r in baseline['inventory']['owners']};totals={}
    check('Exactly eight original parents, no prior Mainz RGB recut',set(geometry['parents'])=={'xB08061','xAEBA2A','x8F0060','x908060','xDBB84C','x118060','xC347B1','x704A5F'})
    for parent in geometry['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y));points=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);expected=np.full(len(cells),old[parent],dtype='U3')
        for polygon in tracing['polygons']:
            if parent not in polygon['parents']:continue
            selected=inside(points,polygon['points'])
            for hole in polygon.get('exclusions',[]):selected&=~inside(points,hole['points'])
            expected[selected]=polygon['owner'];totals[polygon['territory']]=totals.get(polygon['territory'],0)+int(selected.sum())
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells])
        check('Exact source-envelope replay '+parent,np.array_equal(actual,expected))
    work.core.dump('SOURCE_ENVELOPE_COUNTS.json',totals)
    transferred={tag:sum(r['pixels'] for r in geometry['assignments'] if r['owner']==tag and r['previous_owner']!=tag) for tag in ['AUS','HSG','SUU','SAG','SKE']}
    check('Exactly 211 ownership cells, with no province wholesale assumption',transferred=={'AUS':114,'HSG':22,'SUU':11,'SAG':47,'SKE':17})
    protected=~np.isin(before,[int(r[1:],16) for r in geometry['parents']]);check('All raster outside eight parent masks identical',np.array_equal(before[protected],after[protected]))
    for name in ['RHINE_WESTPHALIA_COMPLETION','DUCHY_WESTPHALIA','MINDEN_RAVENSBERG','FRANCONIA_CONTINUATION','MILAN_CREMONESE']:
        prior=json.loads((out.parent/name/'GEOMETRY.json').read_text())
        check('Every prior cell and owner preserved '+name,all(int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and owners[r['rgb']]==r['owner'] and all(after[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in prior['assignments']))
    check('No locator physical movement or RGB rebinding',geometry['hub_rebindings']==[] and all(before[int(float(r['Locator_Y'])),int(float(r['Locator_X']))]==after[int(float(r['Locator_Y'])),int(float(r['Locator_X']))] for r in json.loads((out/'NATIVE_ANCHORS.json').read_text())))
    check('Four new estates, no tiny Constance bishopric or extra Baden tag',plan['new_tags']==work.TAGS and not {'SKO','BDU','BBA'}&set(current['countries']))
    for tag,sid in [('HSG','STATE_WURTTEMBERG'),('SUU','STATE_WURTTEMBERG'),('SAG','STATE_BAVARIA'),('SKE','STATE_BAVARIA')]:check('New capital lies in owned shared subdivision '+tag,[sid,tag] in current['states'])
    for tag in ['BAD','WUR','HOH','BAV']:check('Original private-holder/recruitment subdivision survives '+tag,any(r[1]==tag for r in current['states']))
    migration=json.loads((out/'REGISTRY_MIGRATION.json').read_text())
    check('Only WUR tier corrected, no capital colour culture change',len(migration.get('country_tier_corrections',[]))==1 and migration['country_tier_corrections'][0]['tag']=='WUR' and json.loads(current['countries']['WUR'])[2]==json.loads(migration['country_tier_corrections'][0]['after_signature'])[2])
    definitions={n.key:n for path in effective(work.core.ROOT,work.core.qa.GAME,'common/laws') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for tag in work.TAGS:
        text=(work.core.ROOT/f'common/history/countries/{tag.lower()} - swabian estate.txt').read_text(encoding='utf-8-sig');tech=set(re.findall(r'add_technology_researched\s*=\s*(\w+)',text))
        for node in parser.walk(parser.parse(text)):
            if node.key!='activate_law':continue
            key=parser.scalar(node.value).split(':')[1];check('Start law and technology resolve '+tag+' '+key,key in definitions and set(values(definitions[key],'unlocking_technologies'))<=tech)
    governments=(work.core.ROOT/'common/government_types/00_1776_map2l_swabia.txt').read_text()
    check('Baden margraviate and Hohenzollern princes explicitly named',all(k in governments for k in ['gov_aor1776_baden_margraviate','aor1776_baden_margrave_title','gov_aor1776_swabian_principality','RULER_TITLE_PRINCE']))
    ruler=(work.core.ROOT/'common/history/characters/hoh - hohenzollern.txt').read_text()
    check('Hechingen ruler born in 1717 replaces native future Sigmaringen templates','birth_date = 1717.11.12' in ruler and 'HOH_karl_anton' not in ruler and 'HOH_leopold' not in ruler)
    for lang in ['english','french']:
        path=work.core.ROOT/f'localization/{lang}/1776_map2l_swabia_l_{lang}.yml';text=path.read_text(encoding='utf-8-sig')
        check('New names governors and BOM resolve '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 ' in text for key in work.TAGS+['HOH','aor1776_hoh_first','gov_aor1776_ulm_council']))
        check('All Swabian government tooltip descriptions resolve '+lang,all(' '+node.key+'_desc:0 "' in text for node in parser.parse(governments)))
    from map2k_imperial_system import MEMBERS,ELECTORS
    from map2l_registry import additional_free_cities
    cities=additional_free_cities()
    check('New members without invented electors',set(work.TAGS)<=set(MEMBERS) and not set(work.TAGS)&set(ELECTORS.values()))
    triggers=parser.parse((work.core.ROOT/'common/scripted_triggers/1776_imperial_constitution.txt').read_text())
    free=next(n for n in triggers if n.key=='aor1776_hre_free_city')
    tags={n.key[2:] for n in parser.walk(free.children()) if n.key.startswith('c:')}
    check('Ulm actually compiled into city trigger and journal list','SUU' in cities and tags=={'LUB','HAM','BRE','FRM','NUR','SUU'} and not {'SAG','SKE','HSG'}&tags)
    check('Allocation quantities are exact nonnegative integers',all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in plan['allocations']))

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS;validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
