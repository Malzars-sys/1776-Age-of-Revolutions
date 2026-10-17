"""Bounded completion QA, including exactly authorised municipal abstractions."""
import json,re
import numpy as np
import map2l_swabia_completion as work
import validate_map2l_mainz as validation
from map2l_belgium import packed,sha
from map2l_franconia import inside
from map_1776_audit import effective,values
from map2l_registry import protected_core_preserved

def source_checks(check,out,current,baseline,alignment,tracing,plan):
    root=work.core.ROOT;parser=work.core.cw;before=packed(root/baseline['bitmap_backup']);after=packed(root/'map_data/provinces.png');g=json.loads((out/'GEOMETRY.json').read_text())
    old={r['key'][0]:r['key'][2] for r in baseline['inventory']['owners']};owners={r['key'][0]:r['key'][2] for r in current['owners']};matrices={r['key']:np.array(r['matrix']) for r in tracing['calibrated_sources']}
    check('Exactly reviewed provisional parents plus authorised Kempten core',set(g['parents'])=={'x118060','xC347B1','xDBB84C','xEDAD0D','xEDAF02'})
    for parent in g['parents']:
        y,x=np.where(before==int(parent[1:],16));cells=np.column_stack((x,y));expected=np.full(len(cells),old[parent],dtype='U3')
        for poly in tracing['polygons']:
            if parent not in poly['parents']:continue
            t=matrices[poly['source']];src=(cells+.5-t[2])@np.linalg.inv(t[:2]);expected[inside(src,poly['points'])]=poly['owner']
        actual=np.array([owners['x'+format(int(after[cy,cx]),'06X')] for cx,cy in cells]);check('Exact reviewed envelope replay '+parent,np.array_equal(actual,expected))
    mask=np.isin(before,[int(rgb[1:],16) for rgb in g['parents']]);check('Every pixel outside declared parent masks unchanged',np.array_equal(before[~mask],after[~mask]))
    check('Six free cities and one abbey, no empty-country creation',plan['new_tags']==work.TAGS and all(any(r['owner']==tag for r in g['assignments']) for tag in work.TAGS))
    check('Exactly sixteen changed ownership cells',sum(r['pixels'] for r in g['assignments'] if r['owner']!=r['previous_owner'])==16)
    for tag,point,parent in [('SAC',[4342,910],'xC347B1'),('SKI',[4324,928],'xEDAD0D')]:
        rows=[r for r in g['assignments'] if r['owner']==tag];check('Exactly authorised one-cell city '+tag,len(rows)==1 and rows[0]['pixels']==1 and rows[0]['cells']==[point] and rows[0]['parent_rgb']==parent)
    migration=json.loads((out/'REGISTRY_MIGRATION.json').read_text())
    for name in ['SWABIA','SWABIA_CONTINUATION','SWABIA_FINISH']:
        prior=json.loads((out.parent/name/'GEOMETRY.json').read_text());rows=[r for r in prior['assignments'] if r['source_zone']]
        check('Prior owner cores unchanged except exact approved municipal cell '+name,all(protected_core_preserved(r,after,owners,[out]) for r in rows))
    check('Kempten abbey remains sixteen cells with full original demographics',int((after==0xEDAD0D).sum())==16 and [r for r in current['regional_pop'] if r['key'][:2]==['STATE_BAVARIA','SKE']]==[r for r in baseline['inventory']['regional_pop'] if r['key'][:2]==['STATE_BAVARIA','SKE']])
    check('No locator rebindings or movements',g['hub_rebindings']==[] and all(sha(root/rel)==digest for rel,digest in baseline['hashes'].items() if rel.startswith('gfx/map/map_object_data/')))
    for tag in work.TAGS:
        definition=json.loads(current['countries'][tag]);capital=next(n[2] for n in definition[2] if n[0]=='capital');check('Capital lies in owned state '+tag,[capital,tag] in current['states'])
    laws={n.key:n for path in effective(root,work.core.qa.GAME,'common/laws') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    effects={n.key for path in effective(root,work.core.qa.GAME,'common/scripted_effects') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    governments=parser.parse((root/'common/government_types/00_1776_map2l_swabia_completion.txt').read_text())
    for tag in work.TAGS:
        raw=(root/f'common/history/countries/{tag.lower()} - swabia completion.txt').read_text();tech=set(re.findall(r'add_technology_researched\s*=\s*(\w+)',raw))
        for node in parser.walk(parser.parse(raw)):
            if node.key=='activate_law':
                key=parser.scalar(node.value).split(':')[1];check('Start law and technology resolve '+tag+' '+key,key in laws and set(values(laws[key],'unlocking_technologies'))<=tech)
    for n in governments:
        power=parser.scalar(n.one('transfer_of_power'));check('Native succession hooks '+n.key,'change_to_'+power in effects and 'post_change_to_'+power in effects and power in {'presidential_elective','dictatorial'})
    from map2k_imperial_system import MEMBERS,ELECTORS
    from map2l_registry import additional_free_cities
    check('Exact new members/free-city statuses, no invented electoral voice',set(work.TAGS)<=set(MEMBERS) and set(work.CITIES)<=set(additional_free_cities()) and 'SWG' not in additional_free_cities() and not set(work.TAGS)&set(ELECTORS.values()))
    for lang in ['english','french']:
        path=root/f'localization/{lang}/1776_map2l_swabia_completion_l_{lang}.yml';text=path.read_text(encoding='utf-8-sig');keys=work.TAGS+[t+'_ADJ' for t in work.TAGS]+[n.key+s for n in governments for s in ['', '_desc']]+['aor1776_swg_first','aor1776_swg_last','aor1776_completion_abbot_title']
        check('Names government descriptions and BOM resolve '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 "' in text for key in keys))
    characters=(root/'common/history/characters/1776_map2l_swabia_completion.txt').read_text();check('Documented Dominicus Schnizer, no invented birth date','aor1776_swg_first' in characters and 'birth_date' not in characters and 'age =' not in characters)
    check('Population allocation quantities exact and no added inhabitants',all(sum(r['after'].values())==r['before'] and all(isinstance(v,int) and v>=0 for v in r['after'].values()) for r in plan['allocations']))
    check('Urban allocation targets all own valid subdivision',all([r['state'],tag] in current['states'] for r in plan['allocations'] for tag,count in r['after'].items() if count))
    check('No unsupported physical precision asserted','not independently verified survey accuracy' in ' '.join(tracing['limitations']) and next(s for s in tracing['calibrated_sources'] if s['key']=='PX')['basis'].startswith('Explicit one-cell'))
    check('Baden and Ulm existing raw-key fixes retained',all('gov_aor1776_baden_margraviate_desc:0 "' in (root/f'localization/{lang}/1776_map2l_swabia_l_{lang}.yml').read_text(encoding='utf-8-sig') and 'gov_aor1776_ulm_council_desc:0 "' in (root/f'localization/{lang}/1776_map2l_swabia_l_{lang}.yml').read_text(encoding='utf-8-sig') for lang in ['english','french']))

def validate():
    validation.OUT=work.OUT;validation.REGIONS=work.core.REGIONS;validation.CALIBRATION_CHECK=source_checks;validation.dump=work.core.dump
    return validation.validate()

if __name__=='__main__':raise SystemExit(validate())
