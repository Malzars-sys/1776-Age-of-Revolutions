"""SC2-MORAVIA: immutable capture, protected MAP2A districts and scoped installation."""
import collections as C,json,shutil,subprocess,sys,re
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc2_bohemia as prior
import serg_closure_roadmap as rm
ROOT=prior.ROOT;OUT=ROOT/'docs/reports/map/SERG_CLOSURE/SC2-MORAVIA';core=prior.core;sha=prior.sha
SID='STATE_MORAVIA';PROTECTED={'x71E080','xF0E080'}
ADMIN_PATH='common/history/buildings/1776_sc2_moravia.txt'
PMS=['pm_simple_organization','pm_hereditary_bureaucrats','pm_religious_bureaucrats','pm_1776_no_organized_data_reporting']
CONCURRENT_PATHS={'common/battle_conditions/1776_land_fortifications.txt','common/scripted_triggers/1776_land_fortifications.txt','localization/english/1776_land_fortifications_l_english.yml','localization/french/1776_land_fortifications_l_french.yml'}
runtime_hashes=prior.prior.prior.pas.prior.q.economy.runtime_hashes

def load(p):return prior.load(p)
def dump(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def snapshot():
    assert not (OUT/'BASELINE.json').exists(),'Do not overwrite capture'
    state=load(rm.OUT/'ROADMAP_STATE.json');assert rm.progress(state)['next_task']=='SC2-MORAVIA'
    assert next(t for t in state['tasks'] if t['id']=='SC2-BOHEMIA')['status']=='PASS_RUNTIME_USER_VALIDATED'
    OUT.mkdir(parents=True,exist_ok=True);inv=core.qa.inventory();hashes=runtime_hashes()
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    dump('BASELINE.json',dict(date='2026-10-19',inventory=inv,hashes=hashes,roadmap=state,
        registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),git_index_sha256=sha(ROOT/'.git/index'),
        tool_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*') if p.is_file() and p.name!='serg_sc2_moravia.py'}))
    print('Captured actual workspace: 21 accepted tasks, 72/235; no runtime change')

def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(OUT/'provinces_before.png')
    own={r['key'][0]:r['key'][1:] for r in inv['owners']};rgb=[k for k,v in inv['geometry'].items() if v==SID]
    mask=np.isin(a,[int(k[1:],16) for k in rgb]);yy,xx=np.where(mask);box=[int(xx.min())-12,int(yy.min())-12,int(xx.max())+13,int(yy.max())+13]
    rows=[]
    for k in rgb:
        ys,xs=np.where(a==int(k[1:],16));neighbors=C.Counter()
        for y,x in zip(ys,xs):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                q='x'+format(int(a[y+dy,x+dx]),'06X')
                if inv['geometry'].get(q)!=SID:neighbors[tuple(own.get(q,[inv['geometry'].get(q),'UNOWNED']))]+=1
        rows.append(dict(rgb=k,state_before=SID,state_after=SID,state_id=53,owner_before=own[k][1],owner_after=own[k][1],
            cells_before=len(xs),cells_after=len(xs),protected_map2a=k in PROTECTED,
            bounds=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],centroid=[float(xs.mean()),float(ys.mean())],
            frontier_contacts=[dict(state=s,owner=t,cell_edges=n) for (s,t),n in sorted(neighbors.items())]))
    pop=[r for r in inv['regional_pop'] if r['key'][0]==SID];buildings=[r for r in inv['buildings'] if r['key'][0]==SID]
    dump('NATIVE_INVENTORY.json',dict(provinces=rows,total_cells=int(mask.sum()),box=box,populations=pop,total_population=sum(r['count'] for r in pop),
        buildings=buildings,units=[r for r in inv['units'] if r['key'][2]==SID]))
    old=core.region((ROOT/'common/history/pops/00_west_europe.txt').read_text(encoding='utf-8-sig'),SID,'AUS').children('create_pop')
    counts=[int(n.one('size')) for n in old];assert len(counts)==19 and sum(counts[-7:])==191139
    dump('DEMOGRAPHY.json',dict(task_ids=['SC2-MORAVIA'],state=SID,country='AUS',before=sum(counts),after=sum(counts),
        inherited_moravian_pool=sum(counts[:-7]),protected_map2a_opava_krnov_pool=sum(counts[-7:]),
        source_comparability='The technical region combines Moravia and retained Silesian districts; never compare its total to Moravia alone',
        exact_1776_census_claim=False,new_cultural_reconstruction=False,changed_populations=False))
    dump('BOUNDARY_AUDIT.json',dict(task_ids=['SC2-MORAVIA'],date='2026-10-19',provinces=rows,total_cells=int(mask.sum()),
        before_after_equal=True,classification='B_RETAINED_GENERALIZED_ENVELOPE',historical_cadastral_precision=False,
        excluded_tasks=['SC2-AUSTRIAN-SILESIA','SC2-TESCHEN','SC2-MAP2A-VALIDATION']))
    colors={'AUS':'#a6bbc8','PRU':'#8492bc','HUN':'#d3ac77','HAB':'#d3ac77','KRA':'#ba91ae','POL':'#b6ac87'}
    x0,y0,x1,y1=box;s=7;im=Image.new('RGB',((x1-x0)*s+90,(y1-y0)*s+120),'#faf8ef');d=ImageDraw.Draw(im)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
    rivers=np.array(Image.open(ROOT/'map_data/rivers.png'))
    for y in range(y0,y1):
        for x in range(x0,x1):
            k='x'+format(int(a[y,x]),'06X');tag=own.get(k,['',''])[1];col=colors.get(tag,'#dad5c8')
            if k in rgb:col='#e5b86f' if k in PROTECTED else '#b3caab'
            u=50+(x-x0)*s;v=55+(y-y0)*s;d.rectangle((u,v,u+s,v+s),fill=col)
            if rivers[y,x]<=15:d.rectangle((u+2,v+2,u+4,v+4),fill='#227bc3')
            if x>0 and a[y,x]!=a[y,x-1]:d.line((u,v,u,v+s),fill='#89877c')
            if y>0 and a[y,x]!=a[y-1,x]:d.line((u,v,u+s,v),fill='#89877c')
    for i,r in enumerate(rows,1):
        x,y=r['centroid'];d.text((50+(x-x0)*s,55+(y-y0)*s),str(i),font=f,fill='black',stroke_width=1,stroke_fill='white')
    for x in range(x0,x1,10):d.text((50+(x-x0)*s,32),str(x),font=small,fill='black')
    for y in range(y0,y1,10):d.text((5,55+(y-y0)*s),str(y),font=small,fill='black')
    d.text((12,8),'SC2-MORAVIA — inventaire natif, RGB numerotes (pas des villes)',font=f,fill='black')
    d.text((12,im.height-48),'Vert : noyau morave AUS. Orange : deux districts MAP2A proteges, inchanges.',font=f,fill='black')
    d.text((12,im.height-25),'Inventaire technique et hydrographie; aucune precision cadastrale revendiquee.',font=f,fill='black')
    im.save(OUT/'NATIVE_INVENTORY.png')
    print('Moravia:',len(rows),'RGB,',int(mask.sum()),'cells,',sum(counts),'population; core',sum(counts[:-7]),'+ MAP2A',sum(counts[-7:]))
    print('Existing building records:',len(buildings))
    for r in rows:print(r['rgb'],r['cells_before'],r['bounds'],[(n['state'],n['owner']) for n in r['frontier_contacts']])

def fetch():
    import urllib.request,concurrent.futures
    sources={
        'BERN_GENERAL_MANIFEST.json':'https://www.e-rara.ch/i3f/v20/29888408/manifest',
        'BERN_SPECIAL_MANIFEST.json':'https://www.e-rara.ch/i3f/v20/29506058/manifest',
        'GUBERNIUM.html':'https://starfos.tacr.cz/vysledky-vyzkumu/RIV%2F75081431%3A_____%2F16%3A00000750',
        'BRNO_PRESIDENT.html':'https://encyklopedie.brna.cz/home-mmb/?acc=profil-osobnosti&load=36927',
        'BRNO_TEXTILE_1763.html':'https://encyklopedie.brna.cz/home-mmb/?acc=profil-udalosti&load=5147',
        'SILESIAN_ATLAS.html':'https://mapa.atlas-slezska.cz/en.html',
        'REGIONAL_REFORMS.html':'https://cha.fsv.cvut.cz/en/mapp.php?map=2B',
        'DEMOGRAPHY_CSU.pdf':'https://csu.gov.cz/docs/107516/2bf75c51-6f38-3b58-d03a-7975e01ea77c/rok_2007_xxxvii_konf_sbornik_prispevku.pdf',
        'ARCHIVAL_AUTHORITY.pdf':'https://stands.nacr.cz/da-aip/_downloads/41e7d11ed22d648a23f272dc8a4cfe1b/Zakladni_pravidla_pro_zpracovani_archivalii_v3-1_-_20221006.pdf'}
    d=OUT/'EVIDENCE';d.mkdir(exist_ok=True)
    def one(pair):
        name,url=pair;p=d/name
        try:
            if not p.exists():
                with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'1776HistoricalResearch/1.0'}),timeout=25) as r:data=r.read(20_000_001)
                assert len(data)<=20_000_000;p.write_bytes(data)
            return dict(file=name,url=url,sha256=sha(p),bytes=p.stat().st_size,status='FETCHED')
        except Exception as e:return dict(file=name,url=url,status='UNAVAILABLE',error=str(e))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,sources.items()))
    dump('SOURCE_FETCH.json',rows)
    for r in rows:print(r['file'],r['status'],r.get('bytes',r.get('error')))

def inspect_sources():
    import html
    for name in ['BERN_GENERAL','BERN_SPECIAL']:
        m=load(OUT/'EVIDENCE'/(name+'_MANIFEST.json'))
        print(name,html.unescape(m['label']),len(m['sequences'][0]['canvases']))
        for i,c in enumerate(m['sequences'][0]['canvases']):print(i,c.get('label'),c['images'][0]['resource']['service']['@id'])
        for row in m.get('structures',[]):
            if any(k in str(row).lower() for k in ['moravi','brun','olom','znoi','circul']):print(str(row)[:1500])

def fetch_source_maps():
    import urllib.request
    # Narrow selections verified from the catalogues and contact sheet, not whole atlases.
    selected=load(OUT/'MAP_SELECTION.json')
    for row in selected:
        url=row['service']+'/full/3000,/0/default.jpg';p=OUT/'EVIDENCE'/(row['name']+'.jpg')
        if not p.exists():
            with urllib.request.urlopen(url,timeout=30) as r:data=r.read(20_000_001)
            assert len(data)<=20_000_000;p.write_bytes(data)
        im=Image.open(p);im.thumbnail((1700,1700));im.save(OUT/(row['name']+'_READING.png'))
        row.update(image_url=url,sha256=sha(p))
        print(row['name'],im.size)
    dump('MAP_FILES.json',selected)

def select_maps():
    import urllib.request,html
    choices=[('MORAVIA_GENERAL',29887973,29887974),('BRNO_NORTH',29506018,29506019),('ZNOJMO_JIHLAVA',29505886,29505887),('HRADISTE',29505880,29505881)]
    rows=[]
    for name,record,canvas in choices:
        url=f'https://www.e-rara.ch/i3f/v20/{record}/manifest';p=OUT/'EVIDENCE'/(name+'_MANIFEST.json')
        if not p.exists():
            with urllib.request.urlopen(url,timeout=25) as r:p.write_bytes(r.read())
        m=load(p);c=next(c for c in m['sequences'][0]['canvases'] if c['@id'].endswith('/'+str(canvas)))
        meta=m.get('metadata');print(name,html.unescape(m['label']),meta)
        rows.append(dict(name=name,catalogue=f'https://www.e-rara.ch/bes_1/content/titleinfo/{record}',manifest_url=url,manifest_file=p.name,
            service=c['images'][0]['resource']['service']['@id'],metadata=meta))
    dump('MAP_SELECTION.json',rows)

def review_source_fetch():
    rows=load(OUT/'SOURCE_FETCH.json')
    for r in rows:
        if r['status']=='FETCHED' and r['file'].endswith('.pdf'):
            p=OUT/'EVIDENCE'/r['file']
            if not p.read_bytes().startswith(b'%PDF-'):
                dest=p.with_suffix('.response.html');assert not dest.exists();p.rename(dest)
                r.update(file=dest.name,status='CONTENT_NOT_PDF',error='Endpoint returned HTML, not a readable PDF; retained as failed-fetch evidence, not used as a local PDF source')
    dump('SOURCE_FETCH.json',rows)

def expected_admin():
    return '''# SC2-MORAVIA: minimal representation of the Moravian gubernium at Brno.
# One public level is a game-scale abstraction, not historical headcount.
# The technical state includes protected MAP2A districts; no 1783 legal merger is asserted.
BUILDINGS = {
    s:STATE_MORAVIA = {
        region_state:AUS = {
            create_building = {
                building = "building_government_administration"
                add_ownership = {
                    country = {
                        country = "c:AUS"
                        levels = 1
                    }
                }
                reserves = 1
                activate_production_methods = {
                    "pm_simple_organization"
                    "pm_hereditary_bureaucrats"
                    "pm_religious_bureaucrats"
                    "pm_1776_no_organized_data_reporting"
                }
            }
        }
    }
}
'''

def admin_contract(raw):
    def norm(nodes):return [core.qa.signature(n) for n in nodes]
    assert norm(core.cw.parse(raw))==norm(core.cw.parse(expected_admin())),'Installation exceeds the single public level and approved PMs'
    return True

def install():
    b=load(OUT/'BASELINE.json');assert (OUT/'SOURCES.md').exists() and (OUT/'SECTOR_AUDIT.md').exists()
    assert not (ROOT/ADMIN_PATH).exists(),'Never overwrite a concurrent file'
    current=runtime_hashes();delta={p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)}
    assert delta<=CONCURRENT_PATHS,'Review unexpected concurrent runtime changes before installation: '+str(delta-CONCURRENT_PATHS)
    # Keep the initial capture immutable. Adopt only the independently observed fortification files.
    dump('INSTALL_BASELINE.json',dict(hashes=current,initial_baseline_sha256=sha(OUT/'BASELINE.json'),
        concurrent_runtime_files=sorted(delta),concurrent_sha256={p:current[p] for p in delta},all_preserved_without_writing=True))
    buildings=[r for r in b['inventory']['buildings'] if r['key'][0]==SID]
    assert not any('building_government_administration' in r['key'][2] for r in buildings),'An effective administration already exists'
    raw=expected_admin();admin_contract(raw);(ROOT/ADMIN_PATH).write_bytes(raw.encode('utf8'))
    dump('EXPECTED_TEXT.json',{ADMIN_PATH:raw})
    dump('IMPLEMENTATION.json',dict(task_ids=['SC2-MORAVIA'],installed_sub_lot='MOR-I',country='AUS',state=SID,state_id=53,
        city_rgb='xD9A784',building='building_government_administration',levels_before=0,levels_after=1,owner='c:AUS',production_methods=PMS,
        historical_headcount_claim=False,government_country_changed=False,territory_changed=False,population_changed=False))
    print('Installed: one new file, one public AUS administration level in Moravia')

def validate():
    import map2l_registry as reg
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    raw=(ROOT/ADMIN_PATH).read_text(encoding='utf8');ck('Exact single-building public-ownership contract',admin_contract(raw))
    for field in inv:
        if field not in ['buildings','building_levels_written']:ck('Unchanged inventory '+field,inv[field]==b['inventory'][field])
    n=core.region(raw,SID,'AUS').children('create_building')[0]
    expected=core.qa.counter(b['inventory']['buildings']);expected[(SID,'AUS',core.qa.signature(n))]+=1
    ck('Exactly one added administration, all previous building declarations unchanged',core.qa.counter(inv['buildings'])==expected)
    levels=core.qa.counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=1
    ck('Only one public level added worldwide',core.qa.counter(inv['building_levels_written'])==levels)
    current=runtime_hashes();anchor=load(OUT/'INSTALL_BASELINE.json')['hashes']
    changed=sorted(p for p in set(current)|set(anchor) if current.get(p)!=anchor.get(p))
    concurrent=[p for p in changed if p in CONCURRENT_PATHS]
    ours=[p for p in changed if p not in CONCURRENT_PATHS]
    ck('Only our administration differs outside observed concurrent fortifications',ours==[ADMIN_PATH],dict(ours=ours,concurrent=concurrent))
    ck('Entire province bitmap byte-identical',sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png'])
    ck('574-row imperial registry unchanged',load(reg.active_registry_path())==b['registry'] and len(b['registry'])==574)
    ck('Cumulative approved registry chain retained',reg.approved_lot_dirs()[-1]==prior.prior.OUT)
    before_a=core.packed(OUT/'provinces_before.png');after_a=core.packed(ROOT/'map_data/provinces.png')
    for k in sorted(PROTECTED):
        ck('Protected MAP2A footprint/owner '+k,np.array_equal(before_a==int(k[1:],16),after_a==int(k[1:],16)) and
            [r for r in inv['owners'] if r['key'][0]==k]==[r for r in b['inventory']['owners'] if r['key'][0]==k])
    ck('Bohemia tested population file preserved',sha(ROOT/prior.POP_PATH)==b['hashes'][prior.POP_PATH])
    state=load(rm.OUT/'ROADMAP_STATE.json');done=rm.qualifications(state);was_done=rm.qualifications(b['roadmap'])
    ck('All 21 accepted tasks and receipts remain justified',sum(done.values())==21 and all(done[k] for k,v in was_done.items() if v))
    ck('Salzburg and Bohemia receipts preserved',done['SC1-SALZBURG'] and done['SC2-BOHEMIA'])
    game=core.qa.GAME
    def definitions(folder):
        return {n.key:n for p in core.qa.effective(ROOT,game,folder) for n in core.cw.parse(p.read_text(encoding='utf-8-sig'))}
    pms=definitions('common/production_methods');groups=definitions('common/production_method_groups');buildings=definitions('common/buildings')
    aus=core.cw.parse((ROOT/'common/history/countries/aus - austria.txt').read_text(encoding='utf-8-sig'))[0].children()[0]
    laws={core.cw.scalar(n.value).removeprefix('law_type:') for n in aus.children('activate_law')}
    tech={core.cw.scalar(n.value) for n in aus.children('add_technology_researched')}
    pmgroups=[core.cw.scalar(n.value) for n in buildings['building_government_administration'].children('production_method_groups')[0].children()]
    for key in PMS:
        ck('Production method exists '+key,key in pms)
        node=pms[key];unlock={core.cw.scalar(n.value) for n in node.children('unlocking_laws')[0].children()} if node.children('unlocking_laws') else set()
        disallow={core.cw.scalar(n.value) for n in node.children('disallowing_laws')[0].children()} if node.children('disallowing_laws') else set()
        required={core.cw.scalar(n.value) for n in node.children('unlocking_technologies')[0].children()} if node.children('unlocking_technologies') else set()
        ck('PM available under existing AUS laws/technologies '+key,(not unlock or bool(unlock&laws)) and not disallow&laws and required<=tech)
        matches=[g for g in pmgroups if key in {core.cw.scalar(n.value) for n in groups[g].children('production_methods')[0].children()}]
        ck('PM belongs to one effective building group '+key,len(matches)==1,matches)
    ck('Exactly one selected PM per effective administration group',len(PMS)==len(pmgroups))
    ck('Native Brno city remains in own region',inv['geometry']['xD9A784']==SID and (ROOT/'map_data/state_regions/00_west_europe.txt').read_text(encoding='utf-8-sig').count('city = "xD9A784"')==1)
    tools_changed=[p for p,h in b['tool_hashes'].items() if sha(ROOT/p)!=h]
    ck('Existing territorial tools/tests untouched',set(tools_changed)<={'tools/build_land_fortification_battles.py','tools/validate_land_fortifications.py'},tools_changed)
    ck('Git HEAD/index/branch unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and sha(ROOT/'.git/index')==b['git_index_sha256'] and subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()==b['git_branch'])
    for r in load(OUT/'SOURCE_FETCH.json'):
        if r['status']=='FETCHED':ck('Archived source hash '+r['file'],sha(OUT/'EVIDENCE'/r['file'])==r['sha256'])
    for r in load(OUT/'MAP_FILES.json'):ck('Read map image hash '+r['name'],sha(OUT/'EVIDENCE'/(r['name']+'.jpg'))==r['sha256'])
    result=dict(task_ids=['SC2-MORAVIA'],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'STATIC_REVIEW_REQUIRED',
        passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,
        automated_engine_test=False,engine_executed=False,runtime_validation='PENDING_USER',world_population=sum(r['count'] for r in inv['pops']),
        inherited_duplicate_RGBs=len(inv['duplicates']),inherited_invalid_references=len(inv['errors']))
    dump('VALIDATION.json',result);dump('FILES_MODIFIED.json',dict(runtime_files=ours,sha256={p:current[p] for p in ours},existing_tools_changed=tools_changed,
        concurrent_runtime_files=sorted(CONCURRENT_PATHS),concurrent_sha256={p:current[p] for p in CONCURRENT_PATHS if p in current},concurrent_files_not_written_by_this_pass=True,
        new_tools=['tools/serg_sc2_moravia.py','tools/test_serg_sc2_moravia.py']))
    print('Static:',result['passed'],'/',result['total'],result['failed']);assert not result['failed']

def tests():
    import io,unittest
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01',
        'test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion',
        'test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc',
        'test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia']
    log=io.StringIO();r=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    (OUT/'TESTS.log').write_text(log.getvalue(),encoding='utf8');fs=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions']);new=[f for f in fs if f['id'] not in inherited]
    dump('TESTS.json',dict(task_ids=['SC2-MORAVIA'],total=r.testsRun,passed=r.testsRun-len(fs)-len(r.skipped),failed=fs,
        skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=new,automated_engine_test=False))
    scoped_names=['test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia']
    log=io.StringIO();q=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(scoped_names))
    (OUT/'SCOPED_TESTS.log').write_text(log.getvalue(),encoding='utf8');qs=[dict(id=t.id(),traceback=s) for t,s in q.failures+q.errors]
    dump('SCOPED_TESTS.json',dict(task_ids=['SC2-MORAVIA'],status='PASS' if not qs else 'FAIL',total=q.testsRun,passed=q.testsRun-len(qs)-len(q.skipped),failed=qs,
        skipped=[dict(id=t.id(),reason=s) for t,s in q.skipped],automated_engine_test=False))
    dump('TEST_REVIEW.json',dict(task_ids=['SC2-MORAVIA'],historical_final_layer_assertions=[f['id'] for f in fs if f['id'] in inherited],unexplained_failures=new,
        old_tests_not_modified=True,raw_logs_preserved=True,explanation='The same three obsolete final-layer assertions predate Moravia; the unchanged registry still ends at the accepted Salzburg layer. Current cumulative-chain guard and exact registry conservation pass.',
        initial_only_skip='No-edit initialization invariant is inapplicable after authorized implementations',engine_executed=False))
    print('Cumulative:',r.testsRun-len(fs)-len(r.skipped),'/',r.testsRun,';',len(fs),'inherited failures;',len(new),'unexplained')
    print('Scoped:',q.testsRun-len(qs)-len(q.skipped),'/',q.testsRun,';',len(qs),'failures')
    for f in new+qs:print(f['id'],f['traceback'][-1600:])
    assert not new and not qs and {f['id'] for f in fs}==inherited

def report():
    v=load(OUT/'VALIDATION.json');t=load(OUT/'TESTS.json');s=load(OUT/'SCOPED_TESTS.json')
    assert v['passed']==v['total'] and not v['failed'] and s['status']=='PASS' and not t['unexplained_failures']
    (OUT/'REPORT.md').write_text(f'''# SC2-MORAVIA — livraison du 19 octobre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 30,64 %**

Phase 2, priorité P0, poids 3, **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Livraison `READY_FOR_SCOPED_RUNTIME_VALIDATION`; aucune validation humaine de la Moravie créée.

## Progression et validation effectivement reçue

Début de demande : **66/235 = 28,09 %**, 20 jalons acquis. La rectification directe du joueur confirme un mois de simulation, le rechargement sans crash ni bug et la réussite globale des vérifications pour SC2-BOHEMIA. Elle remplace la mention de lancement seul de la pièce jointe. Après contrôle de conservation, reçu borné enregistré : **72/235 = 30,64 %**, 21 jalons justifiés. Aucun relevé démographique, économique, langue, date de test ou nom de sauvegarde inventé. [Attestation bohémienne](../SC2-BOHEMIA/RUNTIME_USER_ATTESTATION_2026_10_19.json).

SC2-MORAVIA est sélectionnée par le validateur, P0 sans dépendance, avant les autres tâches de phase 2 et les P1 alpines. Le document joint autorise **une seule nouvelle étape**. Après livraison Moravie non testée : **72/235 = 30,64 %**, zéro point supplémentaire. Dénominateur, barème et périmètre 1.0.0 inchangés.

## Travaux historiques et décisions concrètes

Audit [MOR-W/E/N/I/D](SECTOR_AUDIT.md) : interfaces Jihlava/Znojmo avec Bohême/Autriche, vallée morave/Hradiště face à Hongrie, interface silésienne protégée, gouvernement provincial à Brno, populations/économie/unités. Quatre cartes Müller/Homann **1720–1730** ont été lues, confrontées à la chronologie institutionnelle 1735/1763/1783. Elles ne sont ni datées abusivement de 1776 ni appliquées comme cadastre contemporain. [Sources, limites et échecs de consultation](SOURCES.md).

Une omission est attestée : le gubernium morave existe à Brno depuis 1763/64, avec activité documentée avant 1776; aucun bâtiment administratif n'est déclaré dans la région effective. La seule installation est **un niveau d'administration public AUS**, sous-lot MOR-I. Le niveau est une approximation B minimale, pas un comptage du personnel historique.

Fichier fonctionnel nouveau : `common/history/buildings/1776_sc2_moravia.txt`. Méthodes existantes : organisation simple, bureaucrates héréditaires, administration religieuse, rapports organisés de recherche désactivés. Le PM professionnel est incompatible avec la loi AUS actuelle des états provinciaux; aucune réforme nationale ajoutée pour l'imposer. L'office historique n'est pas qualifié d'héréditaire : la traduction reprend l'abstraction nationale du moteur. Aucun nouveau souverain, loi, régime, TAG ou texte de journal.

## Avant / après et conservation

| Élément | Avant | Après |
| --- | --- | --- |
| Géographie technique STATE_MORAVIA, id 53 | 10 RGB, 2 250 cellules, AUS | Identique |
| Noyau de travail hors réparations | 8 RGB, 1 939 cellules, AUS | Identique |
| x71E080 / xF0E080 protégés MAP2A | 92 / 219 cellules, AUS | Identique |
| Population région technique | 1 570 622 | Identique |
| Pool morave hérité / pool Opava-Krnov | 1 379 483 / 191 139 | Identiques, 19 groupes conservés |
| Teschen technique WEST_GALICIA | Pool 135 753 et territoire antérieurs | Identiques, hors installation |
| Administration publique en Moravie | 0 niveau déclaré | **1 niveau AUS** |
| Manufacture et réseau routier | Déclarations, PM, réserves, propriétaires hérités | Identiques |
| Recrutement morave | 5 unités de conscrits | Identique |
| Registre impérial | 574 entrées, neuf électeurs | Identique |
| Population mondiale écrite | 834 926 252 | Identique |

[Inventaire avant](NATIVE_INVENTORY.json), [carte technique numérotée](NATIVE_INVENTORY.png), [RGB/propriétaires avant-après exhaustifs](BOUNDARY_AUDIT.json), [population et comparabilité](DEMOGRAPHY.json), [installation](IMPLEMENTATION.json).

La région technique inclut des districts silésiens : la capacité fiscale agrégée du bâtiment n'est pas une fusion juridique Moravie-Silésie avant 1783. Les deux réparations ne sont ni déplacées ni reconstruites. Les tâches SC2-AUSTRIAN-SILESIA, SC2-TESCHEN et SC2-MAP2A-VALIDATION restent distinctes. La manufacture existante est historiquement défendable; ses niveaux ne sont pas gonflés à partir de chiffres postérieurs. Les deux déclarations routières base/superposition ne sont pas additionnées comme résultat moteur assuré.

Les 21 jalons acquis, dont Bohême et Salzbourg, leurs reçus, populations et géométries restent conservés. Les fichiers fonctionnels préexistants sont identiques à l'instantané d'installation, sous réserve des modifications de fortifications concurrentes observées et documentées : quatre fichiers de conditions de bataille, déclencheurs et localisations FR/EN, ainsi que deux outils du même chantier, préservés sans écriture de notre part. L'instantané initial est immuable; INSTALL_BASELINE.json consigne les trois premières divergences avant installation. Le déclencheur parallèle apparu ensuite est documenté dans CONCURRENT_REVIEW.json, avec le contrôle interrompu conservé dans VALIDATION_CONCURRENT_REVIEW.json. Aucun changement concurrent n'est restauré ou attribué à cette passe.

## Contrôles et limites

- **{v['passed']}/{v['total']} contrôles statiques réussis** : nouveau bâtiment/propriété/niveau/PM, lois et technologies compatibles, géométrie, souveraineté, groupes démographiques, fichiers préexistants, registre et couches approuvées, acquis, preuves et état Git. [VALIDATION.json](VALIDATION.json).
- Suite cumulative : **{t['passed']} réussites sur {t['total']}**, **3 échecs hérités** d'anciennes assertions de dernière couche du registre, **1 exclusion d'initialisation**, aucun nouvel échec inexpliqué. Anciens tests conservés et journal brut livré. [TESTS.json](TESTS.json), [TESTS.log](TESTS.log), [analyse](TEST_REVIEW.json).
- Contrats courants : **{s['passed']} réussites sur {s['total']}**, aucune erreur, une exclusion. Les tests négatifs refusent niveaux supplémentaires, autre région/pays/propriétaire, PM incompatible, données de recherche ajoutées, population ou autre bâtiment et extension des reçus voisins. [SCOPED_TESTS.json](SCOPED_TESTS.json).
- **44 doublons RGB et 12 références invalides hérités** inchangés, aucun nouveau dans l'inventaire. Ces dettes ne sont pas résolues par la présence d'un bâtiment administratif.
- Aucun moteur exécuté par l'agent; aucune nouvelle attestation Moravie. Aucun commit, staging, push, merge, reset, rebase ou changement de branche, ni vanilla modifié; HEAD/branche/index vérifiés.

Les micro-frontières et enclaves locales restent non certifiées; pas de nouvelle série de population exacte au périmètre des huit RGB, proportions culturelles/sociales héritées. La comparaison historique publiée donne un agrégat Moravie + reste de la Silésie; sa proximité avec le total technique ne suffit pas à prouver l'équivalence des périmètres. Aucun recalage arbitraire ou rééquilibrage démographique pour produire un changement.

Le nouveau niveau change emplois, coût public et capacité administrative. Leur comportement réel et la persistance du bâtiment attendent le joueur. [Protocole ciblé](PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776 sous Autriche, contrôle du niveau public et PM, contours/populations/dépendances conservés, un mois, sauvegarde/rechargement.

## Suivi et prochaine action

RM-0006 reçoit la validation globale de Bohême; RM-0007 livre Moravie sans points acquis. ROADMAP_STATE.json, ROADMAP.md, NEXT_ACTION.md, BLOCKERS.md et historique régénérés. Les autres 80 fiches et les événements antérieurs à cette installation sont conservés tels qu'après l'acceptation bohémienne. [Validation du suivi](TRACKER_VALIDATION.json), [conservation](TRACKER_PRESERVATION.json), [manifeste](DELIVERY_MANIFEST.json).

Prochaine action : **test joueur SC2-MORAVIA**. Candidate suivante d'implémentation : **SC2-AUSTRIAN-SILESIA**, P0 sans dépendance actuelle, **NOT_STARTED**. Aucune recherche propre ou installation de cette tâche n'est commencée; seules ses interfaces nécessaires à la protection de MAP2A sont consultées ici. Arrêt de cette mission après la seule étape morave; sélection à revérifier lors de la prochaine mission autorisée.
''',encoding='utf8')
    print('Report prepared with actual evidence and remaining limits')

def update_tracking():
    state=load(rm.OUT/'ROADMAP_STATE.json');b=load(OUT/'BASELINE.json')['roadmap'];assert state==b,'Merge concurrent tracker changes explicitly'
    v=load(OUT/'VALIDATION.json');assert v['passed']==v['total'] and not v['failed'] and load(OUT/'SCOPED_TESTS.json')['status']=='PASS'
    assert not load(OUT/'TEST_REVIEW.json')['unexplained_failures']
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    t=next(t for t in state['tasks'] if t['id']=='SC2-MORAVIA');assert t['status']=='NOT_STARTED'
    t.update(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',historical_sources=t['historical_sources']+[prefix+'SOURCES.md:1'],
        implementation_report=[prefix+'REPORT.md'],installed_lots=['SERG_CLOSURE/SC2-MORAVIA/MOR-I'],static_tests=dict(status='PASS',evidence=[prefix+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='PENDING',attestation=None,scope='MOR-I: one public AUS government administration level in STATE_MORAVIA, inherited PMs; MOR-W/E/N/D retained geography, populations, MAP2A, buildings and conscripts; new 1776 game, one month, save/reload',new_details_invented=False),
        decision=dict(classification='B_RETAINED_TERRITORY_MINIMAL_PROVINCIAL_ADMINISTRATION',evidence=[prefix+'SOURCES.md',prefix+'SECTOR_AUDIT.md',prefix+'IMPLEMENTATION.json'],
            authority='Attached user mission authorizes one new admissible territorial step and defensible corrections; no Moravia runtime receipt'),
        residual_uncertainty='Enveloppe B générale; aucune limite cadastrale ou enclave locale certifiée. Pool technique mélange Moravie et districts Opava/Krnov; pas recensement exact ni répartition culturelle nouvelle. Un niveau public minimal, pas décompte historique des fonctionnaires; PM nationaux abstraits et capacité fiscale régionale ne signifient pas fusion juridique avant 1783. Emploi/coût/fonctionnement/persistance attendent le joueur.',
        current_delivery_note='Audit MOR-W/E/N/I/D livré : 10 RGB/2250 cellules AUS et 1570622 habitants conservés, dont réparations MAP2A protégées. Un niveau administratif public AUS ajouté pour le gubernium à Brno; un fichier nouveau seul. Contrôles statiques réussis, trois anciens échecs de dernière couche classés, aucun reçu humain ni point de Moravie acquis.')
    candidate=rm.progress(state)['next_task'];assert candidate=='SC2-AUSTRIAN-SILESIA'
    state['mission_status']='SC2_MORAVIA_INSTALLED_PENDING_USER_VALIDATION'
    state['runtime_validation_hold']=dict(task_id=t['id'],protocol=prefix+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,source=prefix+'AUTHORIZATION.md',
        reason='One new territorial step per attached user mission; stop after delivery and identify the next step without dispatching it',
        test_summary='Nouvelle partie 1776 sous Autriche : contrôler en Moravie le nouveau niveau public d’administration et ses PM, Brno, les populations et contours conservés, réparations MAP2A et cinq unités de conscrits; un mois puis sauvegarde/rechargement.',
        scope_note='Bohême et Salzbourg conservent leurs reçus bornés. Moravie n’a aucun reçu nouveau; la région technique incluant des districts silésiens ne constitue pas une fusion juridique avant 1783. Les micro-frontières et la démographie exacte restent incertaines.')
    after=rm.progress(state);assert (after['earned_weight'],after['total_weight'],after['percent'],after['next_task'])==(72,235,'30.64','SC2-MORAVIA')
    state['events'].append(dict(id='SERG-RM-0007',date='2026-10-19',kind='SCOPED_IMPLEMENTATION',scope_version=state['scope_version'],source=prefix+'AUTHORIZATION.md',
        changes=[dict(task_id=t['id'],before='NOT_STARTED',after=t['status'])],before_percent='30.64',after_percent='30.64',before_weight=72,after_weight=72,total_weight=235,
        evidence=[prefix+'REPORT.md',prefix+'VALIDATION.json',prefix+'TESTS.json',prefix+'SCOPED_TESTS.json',prefix+'PLAYER_TEST_PROTOCOL.md'],
        note='Une seule étape nouvelle après validation de Bohême : SC2-MORAVIA P0, sans dépendance. Audit daté des contours/interfaces, réparations MAP2A conservées. Gubernium attesté à Brno mais administration absente : un niveau public AUS ajouté, PM compatibles, un fichier nouveau. 10 RGB/2250 cellules et 1570622 habitants inchangés; bâtiments antérieurs, unités et registre conservés. Travaux concurrents de fortifications observés et préservés, aucune restauration. Tests statiques et contrats actuels réussis, trois assertions héritées classées. Aucun reçu Moravie; 72/235=30,64 % maintenus. Prochaine action test joueur; candidate SC2-AUSTRIAN-SILESIA non commencée. Aucun Git écrit.'))
    assert not rm.structural_errors(state);rm.write_json(rm.OUT/'ROADMAP_STATE.json',state);rm.render()
    check=rm.check();dump('TRACKER_VALIDATION.json',check);assert check['status']=='PASS'
    assert [t for t in state['tasks'] if t['id']!='SC2-MORAVIA']==[t for t in b['tasks'] if t['id']!='SC2-MORAVIA']
    assert state['events'][:-1]==b['events'] and state['source_manifest']==b['source_manifest']
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_identical=True,all_21_accepted_tasks_preserved=True,old_events_identical=True,source_manifest_identical=True,
        scope_unchanged=True,earned_weight=72,total_weight=235,percent='30.64',new_user_receipt=False,next_action='PLAYER_TEST_SC2_MORAVIA',next_candidate=candidate,candidate_started=False))
    print('Tracker PASS:72/235=30.64%; player test Moravia; Silesia not started')

def delivery():
    b=load(OUT/'BASELINE.json');v=load(OUT/'VALIDATION.json');assert v['passed']==v['total'] and not v['failed']
    c=rm.check();dump('FINAL_TRACKER_VALIDATION.json',c);assert c['status']=='PASS'
    raw=(ROOT/ADMIN_PATH).read_bytes();assert raw==expected_admin().encode('utf8') and sha(ROOT/'.git/index')==b['git_index_sha256']
    assert not any(s.rstrip()!=s for s in raw.decode('utf8').splitlines())
    dump('DIFF_CHECK.json',dict(new_runtime_files=[ADMIN_PATH],existing_runtime_files_written_by_this_pass=[],new_trailing_whitespace=[],git_writes=False,vanilla_modified=False))
    paths=[ADMIN_PATH,'tools/serg_sc2_moravia.py','tools/test_serg_sc2_moravia.py','tools/serg_closure_accept_bohemia.py']
    paths += [(rm.OUT/n).relative_to(ROOT).as_posix() for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]
    paths += [p.relative_to(ROOT).as_posix() for p in OUT.iterdir() if p.is_file() and p.name!='DELIVERY_MANIFEST.json']
    dump('DELIVERY_MANIFEST.json',dict(task_ids=['SC2-MORAVIA'],date='2026-10-19',status='READY_FOR_SCOPED_RUNTIME_VALIDATION',
        before_session_weight=66,after_bohemia_weight=72,after_moravia_weight=72,total_weight=235,before_percent='28.09',after_percent='30.64',
        runtime_files=[ADMIN_PATH],runtime_user_validation=False,git_writes=False,git_head=b['git_head'],git_branch=b['git_branch'],git_index_sha256=b['git_index_sha256'],
        static_passed=v['passed'],static_total=v['total'],test_review='TEST_REVIEW.json',
        concurrent_runtime_files_preserved=sorted(CONCURRENT_PATHS),next_action='PLAYER_TEST_SC2_MORAVIA',next_candidate='SC2-AUSTRIAN-SILESIA',candidate_started=False,
        sha256={p:sha(ROOT/p) for p in paths}))
    print('Delivery complete: one new runtime file; 72/235; no Git writes, no next step started')

if __name__=='__main__':globals()[sys.argv[1]]()
