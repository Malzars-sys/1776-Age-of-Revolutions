"""Focused northern Qing-band evidence. No full-mod snapshot or Git writes."""
import collections as C
import contextlib, difflib, io, json, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective, values, prov
from map2c_work import ROOT, GAME, sha, source_bitmap, packed, geo_data
from map2e_work import GIT
from map2a_patch import state, edits, append
from map2e_patch import apportion, body_rewrite
from validate_map2f import population_profiles, unit_profiles

OUT = ROOT/'docs/reports/map/MAP2G/NORTHERN_BAND'
BASE = OUT/'BASELINE.json'
REGIONS = ['STATE_JETISY','STATE_ALTAI','STATE_DZUNGARIA','STATE_ULIASTAI','STATE_URGA',
           'STATE_TUVA','STATE_GANSU','STATE_ALXA','STATE_TIANSHAN']
# Explicit coarse southern Chuya / Saylugem corridor, not a nineteenth-century
# international boundary or an automated latitude-to-sovereignty rule.
SOUTH_ALTAI = 'x9ED072 x1CB0A5 xDCF182 x59E500 x5D2376 x2A620D xC59F9C x3F4FA0 xA4752E x3C450E xD3E0F7 xE90206 x141B8F xAE00C4 x7E4C4C'.split()

def dump(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def snapshot():
    assert not BASE.exists(), 'Do not overwrite the live pre-correction baseline'
    folders = ['common','map_data','gfx','gui','events','localization','music','.metadata']
    folders += [f'docs/reports/map/MAP2{x}' for x in 'ABCDEF']
    folders += ['docs/reports/historical_workforce_revision_1776']
    hashes = {p.relative_to(ROOT).as_posix():sha(p) for f in folders
              for p in (ROOT/f).rglob('*') if p.is_file()}
    paths = ['common/history/states/00_states.txt',
             'localization/french/replace/1776_map2g_l_french.yml',
             'localization/english/replace/1776_map2g_l_english.yml']
    paths += [p.relative_to(ROOT).as_posix() for f in ['pops','population','buildings']
              for p in (ROOT/'common/history'/f).rglob('*.txt')]
    inv = qa.inventory()
    assert sum(r['count'] for r in inv['pops']) == 835804980
    git = {k:subprocess.check_output([GIT,*args],cwd=ROOT,text=True).strip()
           for k,args in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()}
    git['index'] = sha(ROOT/'.git/index')
    dump('BASELINE.json', {'hashes':hashes,'originals':{p:(ROOT/p).read_text(encoding='utf-8-sig') for p in paths},
        'inventory':inv,'bitmap_sha256':sha(source_bitmap()),'git':git,
        'game_test':'Player confirmed MAP2G before this follow-up; follow-up not yet tested'})
    print('Light baseline saved; no map copy; world',sum(r['count'] for r in inv['pops']))

def inspect():
    base = json.loads(BASE.read_text(encoding='utf-8'));inv=base['inventory']
    rgb=packed(source_bitmap());defs,hubs,names=geo_data()
    meta={n.key:n for p in effective(ROOT,GAME,'map_data/state_regions') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
    loc={}
    for kind in ['city','farm','wood','mine','port']:
        path=ROOT/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        if not path.exists():path=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        positions={ident:(float(x),rgb.shape[0]-float(z)) for ident,x,z in re.findall(
            r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',path.read_text(encoding='utf-8-sig'))}
        for sid in REGIONS:
            pos=positions.get(meta[sid].one('id'))
            if pos:
                x,y=pos
                loc[sid+'|'+kind]={'x':x,'y':y,'rgb':'x%06X'%int(rgb[int(y),int(x)]),
                    'selector':hubs[sid].get(kind),'name':names.get('HUB_NAME_'+sid+'_'+kind)}
    records=[]
    for sid in REGIONS:
        vs=defs[sid];mask=np.isin(rgb,[int(v[1:],16) for v in vs]);ys,xs=np.where(mask)
        record={'state':sid,'rgb_count':len(vs),'box':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
                'owners':dict(C.Counter(r['key'][2] for r in inv['owners'] if r['key'][1]==sid)),
                'population':[r for r in inv['regional_pop'] if r['key'][0]==sid],
                'buildings':[r for r in inv['buildings'] if r['key'][0]==sid],
                'units':[r for r in inv['units'] if r['key'][2]==sid]}
        records.append(record)
        print(sid,record['box'],record['owners'],'pop',sum(r['count'] for r in record['population']),
              'building fragments',len(record['buildings']),'unit groups',len(record['units']))
    dump('GEOGRAPHY.json',{'bitmap_size':[rgb.shape[1],rgb.shape[0]],'regions':records,'locators':loc})
    preview('before', inv)

def preview(label, inv=None):
    inv=inv or qa.inventory();geo=json.loads((OUT/'GEOGRAPHY.json').read_text(encoding='utf-8'))
    boxes={r['state']:r['box'] for r in geo['regions']}
    a=boxes['STATE_ALTAI'];u=boxes['STATE_ULIASTAI'];d=boxes['STATE_DZUNGARIA']
    j=boxes['STATE_JETISY']
    box=(min(a[0],d[0],j[0])-30,min(a[1],u[1])-35,max(u[2],d[2])+35,max(a[3],u[3],d[3])+25)
    rgb=packed(source_bitmap());x0,y0,x1,y1=box;crop=rgb[y0:y1,x0:x1]
    owner={r['key'][0]:r['key'][2] for r in inv['owners']};defs,hubs,names=geo_data()
    state={v:s for s,vs in defs.items() for v in vs}
    colors={'CHI':(208,176,80),'XIN':(157,135,194),'MGL':(193,157,111),'RUS':(124,159,118),
            'KAZ':(177,143,102),'KHI':(101,157,160),'TIB':(191,149,122),'SEA':(49,72,90)}
    canvas=np.empty((*crop.shape,3),dtype=np.uint8);sv=np.zeros(crop.shape,dtype=np.int16);ov=np.zeros(crop.shape,dtype=np.int16)
    states={s:i+1 for i,s in enumerate(sorted(set(state.values())))};tags={t:i+1 for i,t in enumerate(sorted(set(owner.values())))}
    for c in np.unique(crop):
        v='x%06X'%int(c);mask=crop==c;t=owner.get(v,'SEA');s=state.get(v,'')
        canvas[mask]=colors.get(t,(128,143,132));sv[mask]=states.get(s,0);ov[mask]=tags.get(t,0)
    bd=np.zeros(crop.shape,dtype=bool);bd[1:]|=sv[1:]!=sv[:-1];bd[:,1:]|=sv[:,1:]!=sv[:,:-1];canvas[bd]=(96,87,68)
    bd=np.zeros(crop.shape,dtype=bool);bd[1:]|=ov[1:]!=ov[:-1];bd[:,1:]|=ov[:,1:]!=ov[:,:-1];canvas[bd]=(35,39,36)
    scale=3;im=Image.fromarray(canvas).resize((crop.shape[1]*scale,crop.shape[0]*scale),Image.Resampling.NEAREST)
    page=Image.new('RGB',(im.width,im.height+92),'#f2ead8');page.paste(im,(0,92));draw=ImageDraw.Draw(page)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    draw.text((18,8),'MAP-2G | Northern Qing frontier | '+label.upper(),font=font,fill='#222222')
    draw.text((18,35),'CHI: direct Qing   XIN: Ili   MGL: Uliastai / Mongolian frontier   RUS: Russia',font=small,fill='#333333')
    draw.text((18,60),'Same native province bitmap; dark borders = owners, brown borders = State Regions',font=small,fill='#333333')
    for sid in REGIONS:
        if sid not in boxes:continue
        vs=defs[sid];mask=np.isin(crop,[int(v[1:],16) for v in vs]);ys,xs=np.where(mask)
        if len(xs)<100:continue
        cx,cy=np.median(xs)*scale,np.median(ys)*scale+92
        draw.text((cx,cy),sid.removeprefix('STATE_'),font=small,fill='white',stroke_fill='#202020',stroke_width=2,anchor='mm')
    for key,p in geo['locators'].items():
        if not key.endswith('|city'):continue
        x,y=p['x'],p['y']
        if not(x0<=x<x1 and y0<=y<y1):continue
        xx,yy=(x-x0)*scale,(y-y0)*scale+92
        draw.ellipse((xx-3,yy-3,xx+3,yy+3),fill='#ffe98c',outline='#222222')
        draw.text((xx+6,yy+4),p['name'] or key.split('|')[0],font=small,fill='#ffe98c',stroke_fill='#202020',stroke_width=1)
    page.save(OUT/('BAND_'+label+'.png'))
    print('Preview',OUT/('BAND_'+label+'.png'))

def transform(base):
    originals=base['originals'];result=dict(originals);sid='STATE_JETISY'
    path='common/history/states/00_states.txt';raw=originals[path]
    cr=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:CHI')
    jetisy=[prov(v) for v in values(cr,'owned_provinces')]
    n=cr.children('country')[0];raw=edits(raw,[(n.start,n.end,'country = c:XIN')])
    cr=next(n for n in state(raw,'STATE_ALTAI').children('create_state') if n.one('country')=='c:CHI')
    n=cr.children('owned_provinces')[0];vs=[prov(v) for v in values(cr,'owned_provinces')]
    assert set(SOUTH_ALTAI)<set(vs)
    raw=edits(raw,[(n.start,n.end,'owned_provinces = { '+' '.join(v for v in vs if v not in SOUTH_ALTAI)+' }')])
    s=state(raw,'STATE_ALTAI')
    raw=edits(raw,[(s.end-1,s.end-1,'\n        # MAP2G northern band: southern Uriankhai corridor; northern mixed Russian/Qing claims left unchanged.\n        create_state = { country = c:MGL owned_provinces = { '+' '.join(SOUTH_ALTAI)+' } state_type = unincorporated }\n    ')])
    result[path]=raw
    # Populations are state-level pools, not a census by RGB. Use documented
    # native land-area weights ONLY within existing cultural/religious groups.
    geometry=json.loads((OUT/'ALTAI_RGB_GEOMETRY.json').read_text(encoding='utf-8'))
    weights={'MGL':sum(r['pixels'] for r in geometry if r['rgb'] in SOUTH_ALTAI),
             'CHI':sum(r['pixels'] for r in geometry if r['rgb'] not in SOUTH_ALTAI)}
    allocation=[]
    for path,original in originals.items():
        if not path.startswith(('common/history/pops/','common/history/population/','common/history/buildings/')):continue
        ops=[];pending=[];isp=path.startswith(('common/history/pops/','common/history/population/'))
        for s in cw.walk(cw.parse(original)):
            for r in s.children():
                if r.key!='region_state:CHI':continue
                if s.key=='s:STATE_JETISY':
                    frag=original[r.start:r.end];ops.append((r.start,r.end,frag.replace('region_state:CHI','region_state:XIN',1)))
                    if isp:
                        allocation += [{'state':'STATE_JETISY','culture':p.one('culture'),'religion':p.one('religion','culture default'),
                                        'before_CHI':int(p.one('size')),'after_CHI':0,'after_XIN':int(p.one('size')),'after_MGL':0}
                                       for p in r.children('create_pop')]
                elif isp and s.key=='s:STATE_ALTAI':
                    for p in r.children('create_pop'):
                        size=int(p.one('size'));sizes=apportion(size,weights)
                        assert all(n>0 for n in sizes.values())
                        ops.append((p.start,p.end,body_rewrite(original,p,'size',sizes['CHI'])))
                        pending.append(body_rewrite(original,p,'size',sizes['MGL']))
                        allocation.append({'state':'STATE_ALTAI','culture':p.one('culture'),'religion':p.one('religion','culture default'),
                                           'before_CHI':size,'after_CHI':sizes['CHI'],'after_XIN':0,'after_MGL':sizes['MGL']})
        raw=edits(original,ops)
        if pending:raw=append(raw,'STATE_ALTAI','MGL','\n'.join(pending))
        if raw!=original:result[path]=raw
    for lang,old,new,adj in [('french','Administration des bannières khalkhas','Administration d’Ouliastaï','d’Ouliastaï'),
                             ('english','Khalkha Banner Administration','Uliastai Frontier Administration','Uliastai')]:
        path=f'localization/{lang}/replace/1776_map2g_l_{lang}.yml'
        raw=originals[path].replace(old,new)
        raw=re.sub(r'( MGL_ADJ:0 )"[^"]*"',lambda m:m[1]+'"'+adj+'"',raw)
        result[path]=raw
    changed={p:raw for p,raw in result.items() if raw!=originals[p]}
    moves=[{'state':'STATE_JETISY','rgb':v,'before':'CHI','after':'XIN','basis':'Ili / Tarbagatai frontier delegation; imperial ownership unchanged'} for v in jetisy]
    moves += [{'state':'STATE_ALTAI','rgb':v,'before':'CHI','after':'MGL','basis':'Southern Uriankhai / Kobdo corridor, grouped under Uliastai; coarse documented approximation'} for v in SOUTH_ALTAI]
    plan={'territorial':moves,'population':allocation,'area_weights':weights,'modified_files':list(changed),
          'northern_altai_retained_CHI':[v for v in vs if v not in SOUTH_ALTAI],
          'new_tags':[],'bitmap_changed':False,'new_buildings':0,'new_units':0}
    return changed,plan

def propose():
    base=json.loads(BASE.read_text(encoding='utf-8'));changed,plan=transform(base)
    dump('IMPLEMENTATION.json',plan)
    lines=['*** Begin Patch\n']
    for p,new in changed.items():
        assert sha(ROOT/p)==base['hashes'][p], 'Intervening source edit: '+p
        lines.append('*** Update File: '+(ROOT/p).as_posix()+'\n')
        # Source patch preserves localization BOM already present in the file.
        old=base['originals'][p]
        if p.endswith('.yml'):old='\ufeff'+old;new='\ufeff'+new
        for line in list(difflib.unified_diff(old.splitlines(True),new.splitlines(True),n=3))[2:]:
            if line.startswith('@@'):line='@@\n'
            lines.append(line if line.endswith('\n') else line+'\n')
    lines.append('*** End Patch\n')
    (OUT/'INTEGRATION.patch').write_text(''.join(lines),encoding='utf-8')
    print(len(plan['territorial']),'RGB; files',list(changed));print('Population',allocation_summary(plan))

def allocation_summary(plan):
    return {tag:sum(r['after_'+tag] for r in plan['population']) for tag in ['CHI','XIN','MGL']}

def validate():
    base=json.loads(BASE.read_text(encoding='utf-8'));before=base['inventory'];after=qa.inventory()
    changed,plan=transform(base);tests=[]
    def check(name,ok,detail=None):
        tests.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
        print(tests[-1]['status'],name,flush=True)
    expected=qa.counter(before['owners'])
    for r in plan['territorial']:
        k=(r['rgb'],r['state'],r['before']);assert expected[k]==1
        expected[k]-=1;expected[r['rgb'],r['state'],r['after']]+=1
    check('exact_136_RGB_manifest',+expected==qa.counter(after['owners']) and len(plan['territorial'])==136)
    check('no_province_added_removed_or_redrawn',before['geometry']==after['geometry'] and sha(source_bitmap())==base['bitmap_sha256'])
    check('no_new_double_attribution',before['duplicates']==after['duplicates'])
    check('no_new_orphan_or_wrong_region_reference',before['errors']==after['errors'],after['errors'])
    check('world_population_835804980',sum(r['count'] for r in after['pops'])==835804980)
    check('global_cultures_and_resolved_religions_conserved',before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
    updated=dict(base['originals']);updated.update({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in changed})
    bp,br,bd=population_profiles(base['originals']);ap,ar,ad=population_profiles(updated)
    check('all_demographic_fields_including_social_status_conserved',bp==ap)
    check('every_State_Region_demographic_profile_conserved',br==ar)
    check('only_two_regions_pop_selectors_changed',{k:v for k,v in bd.items() if k[0] not in ['STATE_JETISY','STATE_ALTAI']}=={k:v for k,v in ad.items() if k[0] not in ['STATE_JETISY','STATE_ALTAI']})
    pop=qa.counter(after['regional_pop'])
    check('both_Altai_fragments_populated',all(sum(v for k,v in pop.items() if k[:2]==('STATE_ALTAI',t))>0 for t in ['CHI','MGL']))
    check('Jetisy_exact_133642_residents_preserved',sum(v for k,v in pop.items() if k[:2]==('STATE_JETISY','XIN'))==133642)
    check('all_buildings_PM_reserves_economic_holders_byte_profiles_unchanged',before['buildings']==after['buildings'])
    check('all_declared_building_levels_unchanged',before['building_levels_written']==after['building_levels_written'])
    check('national_units_types_formations_commanders_and_recruitment_unchanged',before['units']==after['units'] and unit_profiles(before)==unit_profiles(after))
    check('no_scheduled_garrison_or_civilian_building_in_transferred_provinces',not any(r['key'][0] in ['STATE_JETISY','STATE_ALTAI'] for r in after['buildings']) and not any(r['key'][2] in ['STATE_JETISY','STATE_ALTAI'] for r in after['units']))
    check('only_country_selector_changed_for_empty_Jetisy_building_scope','region_state:XIN' in (ROOT/'common/history/buildings/09_central_asia.txt').read_text())
    check('all_country_definitions_capitals_cultures_colors_unchanged',before['countries']==after['countries'])
    pairs={tuple(r) for r in after['states']}
    caps={}
    for t in ['CHI','XIN','MGL']:
        caps[t]=next(n[2] for n in json.loads(after['countries'][t])[2] if n[0]=='capital')
    check('Qing_Ili_Mongolian_capitals_owned',all((s,t) in pairs for t,s in caps.items()),caps)
    actual=[p for p,d in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=d]
    check('no_other_runtime_file_or_MAP2A_to_F_report_changed',set(actual)==set(changed),actual)
    check('reviewed_patch_matches_current_AST',all([qa.norm(n) for n in cw.parse(txt)]==[qa.norm(n) for n in cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))] for p,txt in changed.items() if p.endswith('.txt')))
    check('three_original_Qing_vassal_pacts_unchanged',sha(ROOT/'common/history/diplomacy/1776_map2g_qing_dependencies.txt')==base['hashes']['common/history/diplomacy/1776_map2g_qing_dependencies.txt'])
    check('all_hubs_resources_locators_state_geometry_preserved',not any(p.startswith(('map_data/','gfx/')) for p in actual))
    current_owners=qa.counter(after['owners'])
    check('Ezo_Formosa_and_other_MAP2G_owner_changes_preserved',all(current_owners.get(tuple(r['key']))==r['count'] for r in before['owners'] if r['key'][1] not in ['STATE_JETISY','STATE_ALTAI']))
    # Primary sources do not justify annexing all of the northern Russian Altai
    # to Kobdo. Preserve that unresolved sector instead of beautifying it.
    check('northern_Altai_39_RGB_kept_CHI',len(plan['northern_altai_retained_CHI'])==39 and all(current_owners[(v,'STATE_ALTAI','CHI')]==1 for v in plan['northern_altai_retained_CHI']))
    for lang in ['french','english']:
        p=f'localization/{lang}/replace/1776_map2g_l_{lang}.yml';raw=(ROOT/p).read_text(encoding='utf-8')
        check(lang+'_localization_preserves_BOM_and_all_other_keys',raw.startswith('\ufeffl_'+lang+':') and [line for line in raw.splitlines() if not re.match(r' (MGL|MGL_ADJ|aor1776_map2g_mgl):',line)]==[line for line in ('\ufeff'+base['originals'][p]).splitlines() if not re.match(r' (MGL|MGL_ADJ|aor1776_map2g_mgl):',line)])
    for name,func in [('Ottoman_logic_preserved',cw.model_tests)]:
        try:
            with contextlib.redirect_stdout(io.StringIO()):func()
            check(name,True)
        except Exception as e:check(name,False,str(e))
    import validate_regional_infrastructure_shortage as infra
    try:
        with contextlib.redirect_stdout(io.StringIO()):infra.model_tests()
        check('infrastructure_IA_logic_preserved',True)
    except Exception as e:check('infrastructure_IA_logic_preserved',False,str(e))
    check('primary_HEAD_index_refs_untouched',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==base['git']['refs'] and sha(ROOT/'.git/index')==base['git']['index'])
    p='common/history/pops/14_siberia.txt';j0=state(base['originals'][p],'STATE_OUTER_MANCHURIA');j1=state((ROOT/p).read_text(encoding='utf-8-sig'),'STATE_OUTER_MANCHURIA')
    old=json.loads((ROOT/'docs/reports/map/MAP2G/MAP2G_BASELINE.json').read_text(encoding='utf-8'))
    check('Jilin_508_inherited_before_MAP2G_and_not_changed',qa.norm(j0)==qa.norm(j1)==qa.norm(state(old['originals'][p],'STATE_OUTER_MANCHURIA')) and sum(r['count'] for r in after['regional_pop'] if r['key'][0]=='STATE_OUTER_MANCHURIA')==508)
    check('no_new_technology_law_building_unit_or_country',not any(p.startswith(('common/technology/','common/laws/','common/country_definitions/','common/history/military_formations/')) for p in actual))
    status='PASS_STATIC' if all(t['status']=='PASS' for t in tests) else 'FAIL_STATIC'
    dump('VALIDATION.json',{'status':status,'checks':tests,'manifest':plan,'population_world_before':835804980,'population_world_after':835804980,
         'population_split_method':'Native land-area weighting of existing Altai cultural/religious pools, not a historical census',
         'native_game_test':'Not run for this follow-up; player to test a NEW game, then one month',
         'economic_note':'No explicit civilian/military buildings in the two states; no added declared infrastructure demand. Subsistence, hiring, market access and budgets require native game observation.',
         'inherited_Jilin_problem':{'population':508,'siberian':453,'manchu':55,'arable_land':25,'cause_of_no_peasants':'Not established by static inspection','historical_estimate':'Not validated; no unauthorized demographic edit'},
         'no_commit_merge_push':True})
    print(status,len(tests),'checks');assert status=='PASS_STATIC'

if __name__=='__main__':
    {'snapshot':snapshot,'inspect':inspect,'propose':propose,'validate':validate,
     'preview_before':lambda:preview('before',json.loads(BASE.read_text(encoding='utf-8'))['inventory']),
     'preview_after':lambda:preview('after')}[sys.argv[1]]()
