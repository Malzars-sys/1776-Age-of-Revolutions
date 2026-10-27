"""One scoped Teschen pass; current workspace snapshots and explicit registry layer."""
import collections, contextlib, copy, io, json, os, re, subprocess, sys, unittest
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import serg_sc1_ortenburg as prior

ROOT=prior.ROOT; rm=prior.rm; core=prior.core; reg=prior.reg; runtime=prior.runtime
sha=prior.sha; load=prior.load
TASK='SC2-TESCHEN'; OUT=rm.OUT/TASK; PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
RGB='x9061E0'; SID='STATE_WEST_GALICIA'; TAG='AUS'
os.environ['GIT_OPTIONAL_LOCKS']='0'

def dump(name,obj): rm.write_json(OUT/name,obj)
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def capture():
    assert not OUT.exists()
    state=load(rm.OUT/'ROADMAP_STATE.json'); checked=rm.check()
    assert checked['status']=='PASS' and checked['progress']['next_task']==TASK
    assert rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']=='SC1-ORTENBURG'))
    OUT.mkdir()
    dump('BASELINE.json',dict(roadmap=state,hashes=runtime.runtime_hashes(),inventory=core.qa.inventory(),registry=load(reg.active_registry_path()),proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents},peer_proofs={p.relative_to(ROOT).as_posix():sha(p) for folder in ['docs/reports/technology','docs/reports/economy/ALLOYS_1776_REBALANCE','docs/reports/map/WORLD_1776_CLOSURE','docs/reports/agents','.agents'] for p in (ROOT/folder).rglob('*') if p.is_file()},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    (OUT/'USER_MISSION.txt').write_bytes((prior.OUT/'USER_VALIDATION_MISSION_2026_10_25.txt').read_bytes())
    dump('SELECTION.json',dict(status='PASS',selected=TASK,priority='P1',dependencies=[],canonical=checked,only_new_task=TASK))
    print('Current workspace captured; Teschen is the sole authorized new task.',flush=True)

def survey():
    b=load(OUT/'BASELINE.json'); a=core.packed(ROOT/'map_data/provinces.png')
    yy,xx=np.where(a==int(RGB[1:],16)); cells=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
    bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]
    inv=b['inventory']; relevant=[]
    for row in inv['owners']:
        rgb,sid,tag=row['key']
        if sid not in [SID,'STATE_MORAVIA','STATE_UPPER_SILESIA','STATE_EAST_GALICIA']:continue
        y,x=np.where(a==int(rgb[1:],16))
        relevant.append(dict(rgb=rgb,state=sid,owner=tag,cells=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())] if len(x) else None))
    info=dict(target=RGB,state=SID,owner=TAG,cells=cells,count=len(cells),bounds=bbox,regional_owners=relevant,registered=[r for r in b['registry'] if r['state']==SID],populations=[r for r in inv['regional_pop'] if r['key'][0]==SID],buildings=[r for r in inv['buildings'] if r['key'][0]==SID])
    dump('NATIVE_INVENTORY.json',info)
    x0,y0,x1,y1=bbox; margin=25
    image=Image.open(ROOT/'map_data/provinces.png').convert('RGB').crop((x0-margin,y0-margin,x1+margin+1,y1+margin+1)).resize(((x1-x0+2*margin+1)*8,(y1-y0+2*margin+1)*8),Image.Resampling.NEAREST)
    image.save(OUT/'NATIVE_SCOPE.png')
    print(json.dumps({k:v for k,v in info.items() if k in ['target','state','owner','count','bounds','registered','populations']},ensure_ascii=False),flush=True)

def prepare():
    from unittest.mock import patch
    import importlib
    import map2k_imperial_system as compiler
    b=load(OUT/'BASELINE.json'); native=load(OUT/'NATIVE_INVENTORY.json')
    assert native['count']==179 and native['registered']==[]
    assert [r for r in b['inventory']['owners'] if r['key'][0]==RGB]==[dict(key=[RGB,SID,TAG],count=1)]
    assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    row=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC2-TESCHEN: Bohemian-Crown/Austrian-Silesian extent, existing political approximation B; ducal and estate subdivisions not simulated; no Galician neighbors.')
    migration=dict(replaced_regions=[SID],previous=[],updated=[row],ownership_previous=[],ownership_updated=[],new_members=[],free_cities=[],country_additions={},new_provinces=[],region_reference_changes=[],extent_added_cells=native['cells'],extent_removed_cells=[],province_membership_overrides=[dict(rgb=RGB,state=SID,owner=TAG)])
    geometry=dict(classification='B_EXISTING_POLITICAL_REPRESENTATION_REGISTRY_ONLY',historical_cadastral_precision=False,selected_option='KEEP_AUS_AND_REGISTER_EXISTING_SILESIAN_PORTION_ONLY',parents=[],new_provinces=[],assignments=[],hub_rebindings=[],registry_extent_cells=native['cells'],physical_map_changed=False)
    dump('REGISTRY_MIGRATION.json',migration);dump('GEOMETRY.json',geometry)
    before={}; expected={}
    def read(p):
        before[p]=(ROOT/p).read_bytes().decode('utf8');return before[p]
    p='tools/map2l_registry.py'; raw=read(p)
    anchor='    return result\n\ndef reviewed_core_exception_owner'
    assert raw.count(anchor)==1
    addition='''    teschen=ROOT/'docs/reports/map/SERG_CLOSURE/SC2-TESCHEN'
    if (teschen/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((teschen/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((teschen/'GEOMETRY.json').read_text(encoding='utf8'))
        native=json.loads((teschen/'NATIVE_INVENTORY.json').read_text(encoding='utf8'))
        assert ortenburg in result
        assert m['replaced_regions']==['STATE_WEST_GALICIA'] and m['previous']==[]
        assert len(m['updated'])==1
        row=m['updated'][0]
        assert (row['rgb'],row['state'],row['beneficiary'])==('x9061E0','STATE_WEST_GALICIA','AUS')
        assert m['new_members']==m['free_cities']==m['new_provinces']==m['region_reference_changes']==[]
        assert m['country_additions']=={} and m['ownership_previous']==m['ownership_updated']==[]
        assert m['extent_removed_cells']==[]
        assert len(m['extent_added_cells'])==179 and len({tuple(p) for p in m['extent_added_cells']})==179
        assert m['extent_added_cells']==native['cells']==g['registry_extent_cells']
        assert native['target']=='x9061E0' and native['state']=='STATE_WEST_GALICIA' and native['owner']=='AUS'
        assert g['classification']=='B_EXISTING_POLITICAL_REPRESENTATION_REGISTRY_ONLY' and g['physical_map_changed'] is False
        assert not g['historical_cadastral_precision'] and g['parents']==g['new_provinces']==g['assignments']==g['hub_rebindings']==[]
        assert m['province_membership_overrides']==[dict(rgb='x9061E0',state='STATE_WEST_GALICIA',owner='AUS')]
        result.append(teschen)
    return result

def provincial_membership_overrides():
    """Exact reviewed RGB exceptions, never a whole State Region inclusion."""
    return {(r['rgb'],r['state'],r['owner']) for m in approved_territorial_migrations() for r in m.get('province_membership_overrides',[])}

def reviewed_core_exception_owner'''
    expected[p]=raw.replace(anchor,addition)
    p='tools/map2k_imperial_system.py'; raw=read(p)
    old='from map2l_registry import active_registry_path,additional_members,member_region_overrides,territorial_holder_overrides,rightful_holder_condition'
    assert raw.count(old)==1
    raw=raw.replace(old,old+',provincial_membership_overrides')
    old="files={};inv=qa.inventory();ledger=[];overrides=member_region_overrides();territorial=territorial_holder_overrides()"
    assert raw.count(old)==1;raw=raw.replace(old,old+';provincial=provincial_membership_overrides()')
    old='if (tag in MEMBERS and sid in overrides.get(tag,REGIONS)) or sid in territorial.get(tag,set()):'
    assert raw.count(old)==1
    expected[p]=raw.replace(old,'if (tag in MEMBERS and sid in overrides.get(tag,REGIONS)) or sid in territorial.get(tag,set()) or (rgb,sid,tag) in provincial:')
    registry=reg.active_registry_path(); key=registry.relative_to(ROOT).as_posix(); read(key)
    rows=sorted(b['registry']+[row],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    assert load(registry)==b['registry'] and len(rows)==581
    expected[key]=json.dumps(rows,ensure_ascii=False,indent=2)+'\n'
    # Simulate the exact province exception for preparation only. The installed
    # compiler will use the explicit tuple guard, not this temporary region set.
    owner_rows=b['inventory']['owners']; default=[r for r in owner_rows if r['key'][1]==SID and r['key'][2] in compiler.MEMBERS]
    assert default==[dict(key=[RGB,SID,TAG],count=1)]
    original_read=Path.read_text
    def read_candidate(path,*args,**kwargs):
        return expected[key] if path==registry else original_read(path,*args,**kwargs)
    compiler.OUT=OUT
    with patch.object(compiler,'REGIONS',compiler.REGIONS|{SID}),patch.object(Path,'read_text',read_candidate):
        outputs=compiler.compile_system()
    for p,raw in outputs.items():
        old=read(p);bom=old.startswith('\ufeff')
        candidate=('\ufeff' if bom else '')+raw.lstrip('\ufeff')
        if candidate.replace('\r\n','\n')!=old.replace('\r\n','\n'):
            if '\r\n' in old and old.count('\n')==old.count('\r\n'):
                candidate=candidate.replace('\r\n','\n').replace('\n','\r\n')
            expected[p]=candidate
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',expected)
    print('Prepared registry +1, explicit province guard and',len(expected),'files; no functional installation yet.',flush=True)

def install():
    before=load(OUT/'TEXT_BEFORE.json'); expected=load(OUT/'EXPECTED_TEXT.json')
    current=runtime.runtime_hashes(); b=load(OUT/'BASELINE.json')
    drift={p:dict(before=b['hashes'].get(p),after=current.get(p)) for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)}
    assert not set(drift)&set(expected),'Concurrent change on an owned path: reprepare.'
    dump('CONCURRENT_BEFORE_INSTALL.json',dict(functional_changes=drift,owned_overlap=[]))
    for p in expected:assert (ROOT/p).read_bytes().decode('utf8')==before[p],p
    for p,raw in expected.items():
        assert (ROOT/p).read_bytes().decode('utf8')==before[p],p
        (ROOT/p).write_bytes(raw.encode('utf8'))
    print('Installed Teschen registry only. No bitmap, ownership, POP or building writes.',flush=True)

def validate():
    import ast, importlib
    import map2k_imperial_system as compiler
    b=load(OUT/'BASELINE.json'); expected=load(OUT/'EXPECTED_TEXT.json'); checks=[]
    def ck(name,ok): checks.append(dict(name=name,passed=bool(ok)))
    inv=core.qa.inventory(); current=runtime.runtime_hashes(); rows=load(reg.active_registry_path())
    for p,raw in expected.items():
        ck('Exact installed scope '+p,(ROOT/p).read_bytes().decode('utf8')==raw)
        if p.endswith('.py'):ast.parse(raw);ck('Python syntax '+p,True)
        elif p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'));ck('Paradox syntax '+p,True)
    native=load(OUT/'NATIVE_INVENTORY.json');a=core.packed(ROOT/'map_data/provinces.png')
    yy,xx=np.where(a==int(RGB[1:],16));actual=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
    ck('Same 179 current cells',actual==native['cells'] and len(actual)==179)
    ck('AUS sole current owner',[r for r in inv['owners'] if r['key'][0]==RGB]==[dict(key=[RGB,SID,TAG],count=1)])
    ck('Only one exact new title',len(rows)==len(b['registry'])+1==581 and [r for r in rows if r['rgb']!=RGB]==b['registry'])
    ck('Only AUS title in technical Galicia',[r['rgb'] for r in rows if r['state']==SID]==[RGB])
    ck('Province exception only',reg.provincial_membership_overrides()=={(RGB,SID,TAG)} and SID not in compiler.REGIONS)
    ck('No broad regional member override',SID not in reg.member_region_overrides().get(TAG,set()) and SID not in reg.territorial_holder_overrides().get(TAG,set()))
    oldmask=np.isin(a,[int(r['rgb'][1:],16) for r in b['registry']]);newmask=np.isin(a,[int(r['rgb'][1:],16) for r in rows])
    ck('179 newly recognized imperial cells only',np.array_equal(newmask&~oldmask,a==int(RGB[1:],16)) and not np.any(oldmask&~newmask))
    ck('Declared extent delta exact',np.array_equal(reg.migrate_extent(oldmask,[load(OUT/'REGISTRY_MIGRATION.json')]),newmask))
    ck('No ownership migration',reg.ownership_rows(load(OUT/'REGISTRY_MIGRATION.json'),'previous')==reg.ownership_rows(load(OUT/'REGISTRY_MIGRATION.json'),'updated')==[])
    for key in ['owners','geometry','pops','resolved_demographics','regional_pop','buildings','units','countries']:
        ck('Preserved inventory '+key,inv[key]==b['inventory'][key])
    ck('World demographic total retained',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in b['inventory']['pops']))
    from map2k_patch import ELECTORS
    ck('Nine unchanged electors',len(ELECTORS)==9)
    ck('No new member or free city',reg.approved_territorial_migrations()[-1]['new_members']==reg.approved_territorial_migrations()[-1]['free_cities']==[])
    compiler.OUT=OUT;generated=compiler.compile_system()
    for p,raw in generated.items():ck('Installed compiler output '+p,(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    effects=(ROOT/'common/scripted_effects/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
    ck('Restitution is province bound','country = c:AUS provinces = { '+RGB+' }' in effects)
    for lang in ['french','english']:
        for family in ['feedback','repairs']:
            p=ROOT/f'localization/{lang}/1776_imperial_{family}_l_{lang}.yml';data=p.read_bytes();text=data.decode('utf-8-sig')
            ck('BOM and language '+family+' '+lang,data.startswith(b'\xef\xbb\xbf') and text.startswith('l_'+lang+':'))
            keys=re.findall(r'^\s*(\S+):\d*\s',text,re.M);ck('Unique local keys '+family+' '+lang,len(keys)==len(set(keys)))
    nested={p:dict(before=h,after=sha(ROOT/p) if (ROOT/p).exists() else None) for p,h in b['proofs'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and (not (ROOT/p).exists() or sha(ROOT/p)!=h)}
    ck('Prior nested SERG proofs and receipts intact',not nested)
    peers={p:dict(before=h,after=sha(ROOT/p) if (ROOT/p).exists() else None) for p,h in b['peer_proofs'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h}
    foreign={p:dict(before=b['hashes'].get(p),after=current.get(p)) for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p) and p not in expected}
    dump('CONCURRENT_CHANGES.json',dict(functional=foreign,peer_documentary=peers,prior_SERG_proof_changes=nested,old_versions_not_restored=True))
    ck('Map bitmap not rewritten',current['map_data/provinces.png']==b['hashes']['map_data/provinces.png'])
    ck('No functional writes outside registry compilation',not foreign)
    ck('Git HEAD branch index retained',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    ck('ORT receipt remains scoped and regional block unchanged',rm.partial_runtime_evidence(next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']=='SC1-ORTENBURG')))
    ck('No Teschen human receipt',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    dump('FILES_MODIFIED.json',dict(runtime_files=sorted(p for p in expected if p in current),runtime_sha256={p:current[p] for p in expected if p in current},tool_files=sorted(p for p in expected if p.startswith('tools/'))+['tools/serg_sc2_teschen.py'],registry=reg.active_registry_path().relative_to(ROOT).as_posix(),human_validation=None,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'))
    dump('SESSION_AFTER_STATIC.json',dict(hashes=current,inventory=inv))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',task_ids=[TASK],passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False)
    dump('VALIDATION.json',result);print('Static',result['passed'],'/',result['total'],result['failed'],flush=True)
    assert not result['failed']

def track():
    path=rm.OUT/'ROADMAP_STATE.json'; raw=path.read_bytes(); state=json.loads(raw); b=load(OUT/'BASELINE.json')
    assert state==b['roadmap'] and load(OUT/'VALIDATION.json')['status']=='PASS'
    t=next(t for t in state['tasks'] if t['id']==TASK);assert t['status']=='NOT_STARTED'
    t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',implementation_report=[PREFIX+'REPORT.md',PREFIX+'SOURCES.md'],installed_lots=['SERG_CLOSURE/SC2-TESCHEN'],installed_sub_lots=[dict(id='TE-R-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope='Existing x9061E0, 179 AUS cells: imperial registry only; no physical or population change',attestation=None)],blocking_reason='Le défaut de registre des 179 cellules existantes est réparé en B ; correspondance d’ensemble du ressort historique et des seigneuries distinctes avec le RGB technique, puis démographie comparable de 1776 restent à établir. Le dénombrement régional 1770–1771 ne justifie pas automatiquement de remplacer le pool actuel. Aucun cadastre parfait exigé ni correction artificielle installée.',remaining_territorial_obligations=[dict(id='TE-HISTORICAL-PERIMETER',status='OPEN_NOT_VALIDATED',scope='Comparable overall territorial coverage, distinct ducal/domain jurisdictions and excluded neighbors; no claim that Albert owns all local estates'),dict(id='TE-1776-DEMOGRAPHY',status='OPEN_NOT_VALIDATED',scope='Match the 1770–1771 regional census and its coverage to the existing 179-cell representation before any justified demographic correction')],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope='TE-R-CORE only',new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),residual_uncertainty='Existing political B representation; historical jurisdictional and census coverage incomplete. No runtime test of Teschen by the agent or user yet.',current_delivery_note='TE-R-CORE installé : x9061E0, 179 cellules AUS conservées dans WEST_GALICIA, un droit impérial explicite ajouté (580→581), aucun pays ni électeur nouveau. Bitmap, souverainetés, POPs, bâtiments, ressources, unités et technologies conservés. Seul le registre attend le joueur ; région BLOCKED P1 pour correspondance territoriale/démographique, zéro point. Le total régional 112850 en 1770–1771 n’est pas assimilé automatiquement au pool technique 135753.')
    t['historical_sources'] += [PREFIX+'SOURCES.md:1']
    p=rm.progress(state);candidate=p['next_task'];assert candidate=='SC3-HOLSTEIN'
    state['runtime_validation_hold']=dict(task_id=TASK,pending_task_ids=[TASK],protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,reason='Une seule nouvelle tâche autorisée ; le registre Teschen est livré, test joueur requis.',test_summary='Nouvelle partie 1776 avec AUS : portion autrichienne de Galicie occidentale reconnue impériale, autres portions galiciennes exclues, neuf électeurs, anciens noyaux conservés ; un mois complet puis sauvegarde/rechargement. TE-R-CORE uniquement, sans certification cadastrale ou démographique.',scope_note='OR-I-CORE est validé, SC1-ORTENBURG reste BLOCKED P1. Teschen : TE-R-CORE seul attend le joueur, correspondance des juridictions et population comparable restent ouvertes. SC3-HOLSTEIN identifié sans commencement.')
    state['mission_status']='ORTENBURG_CORE_ACCEPTED_TESCHEN_REGISTRY_PENDING_RUNTIME'
    eid='SERG-RM-'+str(max(int(e['id'].split('-')[-1]) for e in state['events'])+1).zfill(4)
    state['events'].append(dict(id=eid,date='2026-10-25',kind='TESCHEN_REGISTRY_ONLY_IMPLEMENTATION_WITH_REGIONAL_BLOCK',scope_version=state['scope_version'],source=PREFIX+'REPORT.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=t['current_delivery_note']))
    assert not rm.structural_errors(state),rm.structural_errors(state);assert path.read_bytes()==raw;rm.write_json(path,state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    dump('TRACKER_VALIDATION.json',rm.check());print('Tracked Teschen registry pending; 82/235; next candidate',candidate,'not started.',flush=True)

def tests():
    import serg_sc4_ligurian_fiefs as lig
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden','test_serg_sc1_passau_outliers','test_serg_versioned_receipts','test_serg_sc1_regensburg_demography','test_serg_sc1_ortenburg','test_serg_sc2_teschen']
    for label,names in [('TARGETED_TESTS',['test_serg_sc2_teschen']),('CUMULATIVE_TESTS',modules)]:
        stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        failed=[dict(id=t.id(),traceback=trace) for t,trace in result.failures+result.errors]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if failed else 'PASS',total=result.testsRun,passed=result.testsRun-len(failed)-len(result.skipped),failed=failed,skipped=[dict(id=t.id(),reason=why) for t,why in result.skipped],old_tests_not_modified=True,automated_engine_test=False))
        print(label,result.testsRun-len(failed)-len(result.skipped),'/',result.testsRun,'failures',len(failed),flush=True)

def finalize():
    from unittest.mock import patch
    b=load(OUT/'BASELINE.json'); v=load(OUT/'VALIDATION.json'); target=load(OUT/'TARGETED_TESTS.json'); suite=load(OUT/'CUMULATIVE_TESTS.json')
    old={f['id']:f for f in load(prior.OUT/'CUMULATIVE_TESTS.json')['failed']}
    prefix='test_serg_sc1_ortenburg.OrtenburgContracts.'
    new={prefix+'test_only_four_exact_pixels_change':'PREEXISTING_EXTERNAL_BITMAP_CHANGE_BEFORE_TESCHEN',prefix+'test_only_reviewed_new_registry_title':'HISTORICAL_580_TITLE_SNAPSHOT_SUPERSEDED_BY_EXACT_581_TITLE_LAYER',prefix+'test_ortenburg_not_human_validated':'REAL_EXPLICIT_ORTENBURG_RECEIPT_SUPERSEDES_ABSENCE_ASSERTION',prefix+'test_progress_and_no_second_task':'OLD_RUNTIME_HOLD_SUPERSEDED_BY_EXPLICIT_NEW_USER_MISSION',prefix+'test_tail_guard_rejects_wrong_country_or_coordinate':'HISTORICAL_LAST_LAYER_ASSERTION_SUPERSEDED_PRIOR_GUARD_RECHECKED'}
    unknown=[f for f in suite['failed'] if f['id'] not in set(old)|set(new)]
    assert not unknown,unknown
    assert (v['passed'],v['total'],target['passed'],target['total'],suite['passed'],suite['total'],len(suite['failed']),len(suite['skipped']))==(123,123,18,18,510,530,19,1)
    previous_review={r['id']:r for r in load(prior.OUT/'TEST_REVIEW.json')['failed']}
    review=[]
    for f in suite['failed']:
        review.append(dict(id=f['id'],classification=new.get(f['id'],previous_review.get(f['id'],{}).get('classification')),already_present_in_ortenburg_suite=f['id'] in old,evidence=PREFIX+'VALIDATION.json' if f['id'] not in old else prior.PREFIX+'TEST_REVIEW.json'))
    # The old tail assertion stops before its negative checks: execute those
    # against the full current chain, without altering the archived test.
    original=Path.read_text;m=load(prior.OUT/'REGISTRY_MIGRATION.json');g=load(prior.OUT/'GEOMETRY.json');negative={}
    wrong=copy.deepcopy(m);next(r for r in wrong['updated'] if r['rgb']==prior.RGB)['beneficiary']='BAV'
    shifted=copy.deepcopy(g);next(r for r in shifted['assignments'] if r['owner']=='ORT')['cells'][0]=[4391,901]
    for label,path,fake in [('Prior Ortenburg holder guard',prior.OUT/'REGISTRY_MIGRATION.json',wrong),('Prior Ortenburg coordinate guard',prior.OUT/'GEOMETRY.json',shifted)]:
        def read(p,*args,**kwargs):return json.dumps(fake) if p==path else original(p,*args,**kwargs)
        rejected=False
        with patch.object(Path,'read_text',read):
            try:reg.approved_territorial_migrations()
            except AssertionError:rejected=True
        negative[label]=rejected
    assert all(negative.values())
    oldbmp=core.packed(prior.OUT/'provinces_before.png');now=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(oldbmp!=now)
    outside=[list(p) for p in sorted(zip(map(int,xx),map(int,yy))) if list(p) not in prior.CELLS]
    assert len(outside)==41 and sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    dump('PREEXISTING_BITMAP_DIFFERENCES.json',dict(reference=prior.PREFIX+'provinces_before.png',reviewed_ortenburg_cells=prior.CELLS,other_cells_existing_before_teschen=outside,count=41,teschen_bitmap_before=b['hashes']['map_data/provinces.png'],teschen_bitmap_after=sha(ROOT/'map_data/provinces.png'),bitmap_written_by_teschen=False))
    dump('TEST_REVIEW.json',dict(status='NO_UNEXPLAINED_REGRESSION',raw_cumulative_status=suite['status'],failed=review,unexplained_failures=unknown,old_tests_not_modified=True,prior_guard_checks=negative,automated_engine_test=False))
    path=rm.OUT/'ROADMAP_STATE.json';raw=path.read_bytes();state=json.loads(raw);p=rm.progress(state)
    note='Teschen : 123/123 contrôles statiques, 18/18 ciblés, suite cumulative brute 510/530 avec 19 échecs classés et une exclusion héritée. Quatorze assertions déjà classées ; cinq nouveaux écarts expliqués par couche/reçu/autorisation explicites et 41 pixels externes antérieurs à la capture Teschen. Garde négatif Ortenbourg recontrôlé, aucun ancien test modifié, aucun échec inexpliqué. TE-R-CORE seul en attente du joueur ; région BLOCKED P1 et 82/235=34,89 % inchangés. SC3-HOLSTEIN seulement identifiée.'
    assert not any(e['kind']=='TESCHEN_FINAL_STATIC_AND_TEST_REVIEW' for e in state['events'])
    eid='SERG-RM-'+str(max(int(e['id'].split('-')[-1]) for e in state['events'])+1).zfill(4)
    state['events'].append(dict(id=eid,date='2026-10-25',kind='TESCHEN_FINAL_STATIC_AND_TEST_REVIEW',scope_version=state['scope_version'],source=PREFIX+'TEST_REVIEW.json',changes=[],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=note))
    assert path.read_bytes()==raw;rm.write_json(path,state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    current=runtime.runtime_hashes(); static=load(OUT/'SESSION_AFTER_STATIC.json')['hashes'];expected=load(OUT/'EXPECTED_TEXT.json')
    checks=dict(negative)
    checks.update({'123 static and 18 targeted checks pass':v['status']==target['status']=='PASS','All cumulative failures individually classified':not unknown and len(review)==19,'Functional snapshot retained since static validation':current==static,'Exact owned files retain checked bytes':all((ROOT/f).read_bytes().decode('utf8')==text for f,text in expected.items()),'Canonical validator passes':rm.check()['status']=='PASS','Scope and progress retained':(p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['total_tasks'])==(82,235,24,81) and state['scope_version']==b['roadmap']['scope_version'],'Only one new task changed':all(t==next(x for x in b['roadmap']['tasks'] if x['id']==t['id']) for t in state['tasks'] if t['id']!=TASK),'Existing event history additive':state['events'][:len(b['roadmap']['events'])]==b['roadmap']['events'],'Next Holstein task not started':next(t['status'] for t in state['tasks'] if t['id']=='SC3-HOLSTEIN')=='NOT_STARTED','Ortenburg receipt remains qualified only for core':rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']=='SC1-ORTENBURG')),'No Teschen receipt':not list(OUT.glob('RUNTIME_USER_ATTESTATION*')),'Prior nested SERG evidence retained':all(sha(ROOT/f)==h for f,h in b['proofs'].items() if Path(f).parent!=rm.OUT.relative_to(ROOT)),'Git revision branch index retained':git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index']})
    peers={f:dict(before=h,after=sha(ROOT/f) if (ROOT/f).exists() else None) for f,h in b['peer_proofs'].items() if not (ROOT/f).exists() or sha(ROOT/f)!=h}
    dump('FINAL_CONCURRENT_OBSERVATION.json',dict(peer_documentary_changes=peers,foreign_functional_changes={f:dict(before=b['hashes'].get(f),after=current.get(f)) for f in set(current)|set(b['hashes']) if current.get(f)!=b['hashes'].get(f) and f not in expected},no_old_version_restored=True))
    diff=subprocess.run(['git','-c','core.safecrlf=false','diff','--check','--',*expected],cwd=ROOT,text=True,capture_output=True)
    dump('DIFF_CHECK.json',dict(returncode=diff.returncode,stdout=diff.stdout,stderr=diff.stderr));checks['Owned diff has no whitespace errors']=diff.returncode==0
    result=dict(status='PASS' if all(checks.values()) else 'FAIL',task_ids=[TASK],passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v],checks=checks,automated_engine_test=False)
    dump('FINAL_CHECKS.json',result);dump('FINAL_TRACKER_VALIDATION.json',rm.check())
    report=OUT/'REPORT.md';text=report.read_text(encoding='utf8');assert '## Résultats finaux exécutés' not in text
    report.write_text(text+'\n## Résultats finaux exécutés\n\n'+note+'\n\nLe contrôle final et ses limites sont dans FINAL_CHECKS.json. Les 19 traces brutes sont conservées ; les nouvelles divergences ne sont pas appelées toutes « échecs hérités ». Aucun moteur lancé et aucune validation humaine de Teschen.\n',encoding='utf8')
    print('Final',result['passed'],'/',result['total'],result['failed'],flush=True);assert not result['failed']

if __name__=='__main__': globals()[sys.argv[1]]()
