"""SC2-BOHEMIA: snapshot, independent sub-lots, explicit historical corrections."""
import collections as C,csv,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc1_salzburg as prior
import serg_closure_roadmap as rm
ROOT=prior.ROOT
OUT=ROOT/'docs/reports/map/SERG_CLOSURE/SC2-BOHEMIA'
core=prior.core
sha=prior.sha
POP_PATH='common/history/pops/00_west_europe.txt'
SID='STATE_BOHEMIA'
TARGET=2_500_000
def load(p):return prior.load(p)
def dump(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def snapshot():
    assert not (OUT/'BASELINE.json').exists(),'Do not overwrite capture'
    state=load(rm.OUT/'ROADMAP_STATE.json');assert rm.progress(state)['next_task']=='SC2-BOHEMIA'
    assert next(t for t in state['tasks'] if t['id']=='SC1-SALZBURG')['status']=='PASS_RUNTIME_USER_VALIDATED'
    OUT.mkdir(parents=True,exist_ok=True)
    inv=core.qa.inventory();hashes=prior.prior.pas.prior.q.economy.runtime_hashes()
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    dump('BASELINE.json',dict(date='2026-10-19',inventory=inv,hashes=hashes,roadmap=state,
        registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),git_index_sha256=sha(ROOT/'.git/index'),
        tool_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*') if p.is_file() and p.name!='serg_sc2_bohemia.py'}))
    print('SC2 snapshot:',len(hashes),'runtime files, 20 accepted tasks, 66/235')

def inventory():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png');inv=b['inventory']
    own={r['key'][0]:r['key'][1:] for r in inv['owners']};rgb=[k for k,v in inv['geometry'].items() if v=='STATE_BOHEMIA']
    mask=np.isin(a,[int(k[1:],16) for k in rgb]);yy,xx=np.where(mask);box=[int(xx.min())-12,int(yy.min())-12,int(xx.max())+13,int(yy.max())+13]
    rows=[]
    for k in rgb:
        yy,xx=np.where(a==int(k[1:],16));rows.append(dict(rgb=k,state=own[k][0],owner=own[k][1],pixels=len(xx),
            bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],centroid=[float(xx.mean()),float(yy.mean())]))
    pop=[r for r in inv['regional_pop'] if r['key'][0]=='STATE_BOHEMIA']
    dump('NATIVE_INVENTORY.json',dict(box=box,provinces=rows,populations=pop,total_population=sum(r['count'] for r in pop),
        buildings=[r for r in inv['buildings'] if r['key'][0]=='STATE_BOHEMIA'],units=[r for r in inv['units'] if r['key'][2]=='STATE_BOHEMIA']))
    colors={'AUS':'#9eb6c5','PRU':'#7d8dba','SAX':'#d8b578','BAV':'#cfba8d','ANS':'#b6a3cb','FBM':'#c09daf'}
    x0,y0,x1,y1=box;s=6;im=Image.new('RGB',((x1-x0)*s+90,(y1-y0)*s+120),'#faf8ef');d=ImageDraw.Draw(im)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13);tiny=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
    rivers=np.array(Image.open(ROOT/'map_data/rivers.png'))
    for y in range(y0,y1):
        for x in range(x0,x1):
            k='x'+format(int(a[y,x]),'06X');tag=own.get(k,['',''])[1];col=colors.get(tag,'#dbd7ca')
            if k in rgb:col='#b3caab'
            u=50+(x-x0)*s;v=55+(y-y0)*s;d.rectangle((u,v,u+s,v+s),fill=col)
            if rivers[y,x]<=15:d.rectangle((u+2,v+2,u+4,v+4),fill='#227bc3')
            if x>0 and a[y,x]!=a[y,x-1]:d.line((u,v,u,v+s),fill='#8e8c80')
            if y>0 and a[y,x]!=a[y-1,x]:d.line((u,v,u+s,v),fill='#8e8c80')
    for i,r in enumerate(rows,1):
        x,y=r['centroid'];d.text((50+(x-x0)*s,55+(y-y0)*s),str(i),font=f,fill='black',stroke_width=1,stroke_fill='white')
    for x in range(x0,x1,10):d.text((50+(x-x0)*s,32),str(x),font=tiny,fill='black')
    for y in range(y0,y1,10):d.text((5,55+(y-y0)*s),str(y),font=tiny,fill='black')
    d.text((12,8),'SC2-BOHEMIA / AVANT — RGB numerotes, proprietaires actuels, hydrographie native',font=f,fill='black')
    d.text((12,im.height-48),'Vert : STATE_BOHEMIA, AUS / violet : PRU / ocre : SAX. Numeros = RGB, pas villes.',font=f,fill='black')
    d.text((12,im.height-25),'Cette carte est un inventaire technique, pas une preuve des frontieres de 1776.',font=f,fill='black')
    im.save(OUT/'NATIVE_INVENTORY.png')
    for i,r in enumerate(rows,1):r['number']=i
    dump('PROVINCES.json',rows)
    print('Bohemia:',len(rows),'RGB,',int(mask.sum()),'cells, population',sum(r['count'] for r in pop),'bounds',box)
    for i,r in enumerate(rows,1):print(i,r['rgb'],r['owner'],r['pixels'],r['bounds'])

def fetch():
    import urllib.request,concurrent.futures
    sources={
      'ATLAS_BORDERS.html':'https://cha.fsv.cvut.cz/en/mapp.php?map=1C',
      'ATLAS_REGIONS.html':'https://cha.fsv.cvut.cz/en/mapp.php?map=2B',
      'GUBERNIUM.html':'https://www.nacr.cz/en/about-us/from-the-history-of-the-national-archives',
      'CENSUS_METHOD.html':'https://statistikaamy.csu.gov.cz/cisarovno-marie-terezie-diky-za-scitani',
      'MILITARY_SURVEY.html':'https://chartae-antiquae.cz/en/maps/1military',
      'BOHEMIA_1780_POP.html':'https://austria-forum.org/web-books/en/kpwde14de1894onb/00000358',
      'NORTH_1778_MANIFEST.json':'https://www.e-rara.ch/i3f/v20/29682321/manifest',
      'NORTHEAST_1757_MANIFEST.json':'https://www.e-rara.ch/i3f/v20/29505229/manifest',
      'SOUTH_1757_MANIFEST.json':'https://www.e-rara.ch/i3f/v20/29505238/manifest'}
    sources['OVERVIEW_1730_1760_MANIFEST.json']='https://www.e-rara.ch/i3f/v20/29505178/manifest'
    d=OUT/'EVIDENCE';d.mkdir(exist_ok=True)
    def one(pair):
        name,url=pair;p=d/name
        try:
            if not p.exists():
                with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'1776HistoricalResearch/1.0'}),timeout=25) as r:data=r.read(8_000_001)
                assert len(data)<=8_000_000
                p.write_bytes(data)
            return dict(file=name,url=url,sha256=sha(p),bytes=p.stat().st_size,status='FETCHED')
        except Exception as e:return dict(file=name,url=url,status='UNAVAILABLE',error=str(e))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,sources.items()))
    dump('SOURCE_FETCH.json',rows)
    for r in rows:print(r['file'],r['status'],r.get('bytes',r.get('error')))

def fetch_maps():
    import urllib.request
    for name in ['NORTH_1778','NORTHEAST_1757','SOUTH_1757','OVERVIEW_1730_1760']:
        m=load(OUT/'EVIDENCE'/(name+'_MANIFEST.json'))
        c=m['sequences'][0]['canvases'][0];service=c['images'][0]['resource']['service']['@id']
        url=service+'/full/2500,/0/default.jpg';p=OUT/'EVIDENCE'/(name+'.jpg')
        if not p.exists():
            with urllib.request.urlopen(url,timeout=30) as r:data=r.read(20_000_001)
            assert len(data)<=20_000_000;p.write_bytes(data)
        im=Image.open(p);im.thumbnail((1600,1600));im.save(OUT/(name+'_READING.png'))
        dump(name+'_SOURCE.json',dict(manifest=name+'_MANIFEST.json',image_url=url,sha256=sha(p),canvas=c.get('label'),metadata=m.get('metadata')))
        print(name,im.size,service)

def allocate_counts(counts,target):
    assert target>0 and counts and all(n>0 for n in counts)
    total=sum(counts);out=[n*target//total for n in counts]
    order=sorted(range(len(counts)),key=lambda i:(-(counts[i]*target%total),i))
    for i in order[:target-sum(out)]:out[i]+=1
    assert sum(out)==target and all(n>0 for n in out)
    return out

def pop_nodes(raw):return core.region(raw,SID,'AUS').children('create_pop')

def descriptors(nodes):
    return [[(n.key,n.op,n.value) for n in p.children() if n.key!='size'] for p in nodes]

def validate_scope(old,new):
    a=core.state(old,SID);b=core.state(new,SID)
    assert old[:a.start]==new[:b.start] and old[a.end:]==new[b.end:],'Other state or byte outside Bohemia changed'
    left=pop_nodes(old);right=pop_nodes(new)
    assert len(left)==len(right)==9 and descriptors(left)==descriptors(right),'Population identity/profession/religion changed'
    expected=allocate_counts([int(p.one('size')) for p in left],TARGET)
    assert [int(p.one('size')) for p in right]==expected,'Unexpected demographic allocation'
    # Mask only the nine numeric values; all other characters must match, including comments/newlines.
    def masked(raw,nodes):
        ops=[]
        for p in nodes:
            n=p.children('size')[0];chunk=raw[n.start:n.end]
            ops.append((n.start,n.end,re.sub(r'\d+$','<SIZE>',chunk)))
        return core.edits(raw,ops)
    assert masked(old,left)==masked(new,right),'Edits exceed nine size values'
    return True

def prepare():
    b=load(OUT/'BASELINE.json');p=ROOT/POP_PATH
    assert sha(p)==b['hashes'][POP_PATH],'Concurrent population change: merge before proceeding'
    data=p.read_bytes();old=data.decode('utf8');nodes=pop_nodes(old)
    sizes=[int(n.one('size')) for n in nodes];assert sum(sizes)==3_375_003
    counts=allocate_counts(sizes,TARGET);ops=[];rows=[]
    for node,after in zip(nodes,counts):
        n=node.children('size')[0];ops.append((n.start,n.end,re.sub(r'\d+$',str(after),old[n.start:n.end])))
        rows.append(dict(culture=node.one('culture'),religion=node.one('religion','DEFAULT:'+node.one('culture')),
            pop_type=node.one('pop_type','DEFAULT'),before=int(n.value),after=after))
    new=core.edits(old,ops);validate_scope(old,new)
    (OUT/'POPS_BEFORE.txt').write_bytes(data);(OUT/'POPS_CANDIDATE.txt').write_bytes(new.encode('utf8'))
    dump('DEMOGRAPHY.json',dict(task_ids=['SC2-BOHEMIA'],state=SID,owner='AUS',before=sum(sizes),after=TARGET,delta=TARGET-sum(sizes),
        estimate=True,reference_year=1776,working_uncertainty_range=[2_350_000,2_600_000],range_is_modelling_judgment_not_census_confidence_interval=True,
        method='Rounded scenario estimate, bracketed by Bohemia-proper 1770 approx. 2.4m and 1780 2,563,527; not linear interpolation across the 1771-72 famine',
        cultural_and_occupational_shares='Inherited, proportionally rescaled by integer largest remainder; not a reconstructed 1776 cultural census',
        source='SOURCES.md: D1-D3',rows=rows))
    # Export actual frontier contacts rather than assigning modern city names to RGB centroids.
    a=core.packed(OUT/'provinces_before.png');g=b['inventory']['geometry'];own={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    rgb=[k for k,v in g.items() if v==SID];records=[]
    for k in rgb:
        ys,xs=np.where(a==int(k[1:],16));neighbors=C.Counter()
        for y,x in zip(ys,xs):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                q='x'+format(int(a[y+dy,x+dx]),'06X')
                if g.get(q)!=SID:neighbors[tuple(own.get(q,[g.get(q),'UNOWNED']))]+=1
        records.append(dict(rgb=k,state_before=SID,state_after=SID,state_id=52,owner_before='AUS',owner_after='AUS',
            cells_before=len(xs),cells_after=len(xs),frontier_contacts=[dict(state=s,owner=t,cell_edges=n) for (s,t),n in sorted(neighbors.items())]))
    dump('BOUNDARY_AUDIT.json',dict(task_ids=['SC2-BOHEMIA'],date='2026-10-19',status='B_GENERALIZED_ENVELOPE_RETAINED',
        total_cells=4412,provinces=records,bitmap_changed=False,ownership_changed=False,historical_cadastral_precision=False,
        source_trace_to_native_cells=False,reason='Dated outer geography compared by sector; no source-to-native calibration sufficient to justify any individual-cell transfer',
        detailed_sector_decisions='SECTOR_AUDIT.md',not_claimed=['modern Czech state border','1757 regional divisions as 1776 law','Glatz restored to Bohemia','cadastre or local enclave reconstruction']))
    print('Candidate:',sum(sizes),'->',TARGET,';',len(rows),'size values; all surrounding bytes preserved')

def install():
    assert (OUT/'SOURCES.md').exists() and (OUT/'SECTOR_AUDIT.md').exists()
    p=ROOT/POP_PATH;old=(OUT/'POPS_BEFORE.txt').read_bytes();new=(OUT/'POPS_CANDIDATE.txt').read_bytes()
    assert p.read_bytes()==old,'Concurrent change: never overwrite'
    validate_scope(old.decode('utf8'),new.decode('utf8'));p.write_bytes(new)
    print('Installed: Bohemia population only; nine numeric values, one file')

def validate():
    import map2l_registry as reg
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    old=(OUT/'POPS_BEFORE.txt').read_bytes();new=(ROOT/POP_PATH).read_bytes()
    ck('Nine sizes only, exact deterministic allocation, no concurrent overwrite',validate_scope(old.decode('utf8'),new.decode('utf8')))
    ck('Installed candidate byte exact',new==(OUT/'POPS_CANDIDATE.txt').read_bytes())
    for field in inv:
        if field not in ['pops','regional_pop','resolved_demographics']:ck('Unchanged inventory '+field,inv[field]==b['inventory'][field])
    def without_boh(rows):return [r for r in rows if r['key'][0]!=SID]
    ck('Every other regional population including SLZ unchanged',without_boh(inv['regional_pop'])==without_boh(b['inventory']['regional_pop']))
    current_boh=[r for r in inv['regional_pop'] if r['key'][0]==SID]
    ck('Bohemia total is rounded 2.5m',sum(r['count'] for r in current_boh)==TARGET)
    ck('World delta exactly -875003',sum(r['count'] for r in inv['pops'])-sum(r['count'] for r in b['inventory']['pops'])==-875003)
    expected=core.qa.counter(b['inventory']['pops'])
    for r in b['inventory']['regional_pop']:
        if r['key'][0]==SID:expected[tuple(r['key'][2:])]-=r['count']
    for r in current_boh:expected[tuple(r['key'][2:])]+=r['count']
    ck('World culture/confession delta confined to Bohemia',core.qa.counter(inv['pops'])==expected)
    cultures={}
    for p in core.qa.effective(ROOT,core.qa.GAME,'common/cultures'):
        for n in core.cw.parse(p.read_text(encoding='utf-8-sig')):cultures[n.key]=core.cw.scalar(n.one('religion','UNRESOLVED_DEFAULT'))
    resolved=C.Counter()
    for (cu,rel),count in expected.items():resolved[(cu,cultures.get(cu,'UNRESOLVED_DEFAULT') if rel.startswith('DEFAULT:') else rel)]+=count
    ck('Effective confession totals match only the intended demographic delta',core.qa.counter(inv['resolved_demographics'])==resolved)
    current=prior.prior.pas.prior.q.economy.runtime_hashes()
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    ck('Only authorized runtime file differs',changed==[POP_PATH],changed)
    ck('Entire native bitmap unchanged including 12 accepted Salzburg cells',sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png'])
    ck('574-row imperial registry unchanged',load(reg.active_registry_path())==b['registry'] and len(b['registry'])==574)
    ck('Cumulative registry guards accept existing territorial layers',reg.approved_lot_dirs()[-1]==prior.OUT)
    state=load(rm.OUT/'ROADMAP_STATE.json');done=rm.qualifications(state)
    ck('All 20 accepted tasks remain justified',sum(done.values())==20 and all(done[t['id']] for t in b['roadmap']['tasks'] if rm.qualifications(b['roadmap'])[t['id']]))
    ck('Salzburg receipt exact and still accepted',done['SC1-SALZBURG'] and load(prior.OUT/'RUNTIME_USER_ATTESTATION_2026_10_19.json')['scope']['classification']=='B_POLITICAL_APPROXIMATION')
    tools_changed=[p for p,h in b['tool_hashes'].items() if sha(ROOT/p)!=h]
    ck('Prior tools/tests preserved except generalized handoff renderer',set(tools_changed)<={'tools/serg_closure_roadmap.py'},tools_changed)
    ck('Git HEAD/index/branch unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and sha(ROOT/'.git/index')==b['git_index_sha256'] and subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()==b['git_branch'])
    for r in load(OUT/'SOURCE_FETCH.json'):
        ck('Archived source '+r['file'],r['status']=='FETCHED' and sha(OUT/'EVIDENCE'/r['file'])==r['sha256'])
    result=dict(task_ids=['SC2-BOHEMIA'],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'STATIC_REVIEW_REQUIRED',
        passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,
        engine_executed=False,automated_engine_test=False,runtime_validation='PENDING_USER',
        world_before=sum(r['count'] for r in b['inventory']['pops']),world_after=sum(r['count'] for r in inv['pops']),
        inherited_duplicate_RGBs=len(inv['duplicates']),inherited_invalid_references=len(inv['errors']))
    dump('VALIDATION.json',result);dump('FILES_MODIFIED.json',dict(runtime_files=changed,sha256={p:current[p] for p in changed},tools_changed=tools_changed))
    print('Static/non-regression:',result['passed'],'/',result['total'],'failed',result['failed'])
    assert not result['failed']

def tests():
    import io,unittest
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01',
        'test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion',
        'test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political',
        'test_map2w_r4bc','test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia']
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    (OUT/'TESTS.log').write_text(stream.getvalue(),encoding='utf8')
    failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
    expected=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    new=[f for f in failures if f['id'] not in expected]
    data=dict(task_ids=['SC2-BOHEMIA'],total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,
        skipped=[dict(id=t.id(),reason=reason) for t,reason in result.skipped],unexplained_failures=new,
        inherited_superseded_assertions=[f['id'] for f in failures if f['id'] in expected],
        classification='RAW_SUITE_HAS_INHERITED_FAILURES' if failures else 'PASS',automated_engine_test=False)
    dump('TESTS.json',data)
    scoped=unittest.defaultTestLoader.loadTestsFromNames(['test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia'])
    log=io.StringIO();r=unittest.TextTestRunner(stream=log,verbosity=2).run(scoped)
    (OUT/'SCOPED_TESTS.log').write_text(log.getvalue(),encoding='utf8')
    fs=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
    dump('SCOPED_TESTS.json',dict(task_ids=['SC2-BOHEMIA'],status='PASS' if not fs else 'FAIL',total=r.testsRun,
        passed=r.testsRun-len(fs)-len(r.skipped),failed=fs,skipped=[dict(id=t.id(),reason=reason) for t,reason in r.skipped],automated_engine_test=False))
    dump('TEST_REVIEW.json',dict(task_ids=['SC2-BOHEMIA'],unexplained_failures=new,historical_final_layer_assertions=data['inherited_superseded_assertions'],
        raw_failure_logs_preserved=True,old_tests_not_modified=True,
        explanation='Same three assertions already failed before SC2: they demand a previous lot be the final registry layer. The registry and all compiled outputs remain byte-identical to the SC2 baseline; Salzburg remains its last layer.',
        replacement='VALIDATION.json plus test_serg_sc1_salzburg.SalzburgContracts.test_exact_cumulative_tail',
        initial_only_skip='No-edit initialization invariant deliberately skipped after authorized installations',engine_executed=False))
    print('Cumulative:',data['passed'],'passed /',data['total'],';',len(failures),'inherited failures;',len(new),'unexplained')
    print('Scoped:',r.testsRun-len(fs)-len(r.skipped),'passed /',r.testsRun,';',len(fs),'failures')
    for f in new+fs:print(f['id'],f['traceback'][-1800:])
    assert not new and not fs and {f['id'] for f in failures}==expected

def update_tracking():
    p=rm.OUT/'ROADMAP_STATE.json';state=load(p);b=load(OUT/'BASELINE.json')['roadmap']
    assert state==b,'Concurrent tracker change: merge explicitly'
    v=load(OUT/'VALIDATION.json');tests=load(OUT/'SCOPED_TESTS.json')
    assert v['passed']==v['total'] and not v['failed'] and tests['status']=='PASS' and not load(OUT/'TEST_REVIEW.json')['unexplained_failures']
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    t=next(t for t in state['tasks'] if t['id']=='SC2-BOHEMIA');assert t['status']=='NOT_STARTED'
    before=rm.progress(state)
    t.update(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',historical_sources=t['historical_sources']+[prefix+'SOURCES.md:1'],
        implementation_report=[prefix+'REPORT.md'],installed_lots=['SERG_CLOSURE/SC2-BOHEMIA/BOH-D'],
        static_tests=dict(status='PASS',evidence=[prefix+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='PENDING',attestation=None,
            scope='BOH-D population 3375003 to rounded estimate 2500000 in STATE_BOHEMIA AUS; BOH-W/N/E/S/I generalized envelope and dependencies retained; new 1776 game, one month, save/reload',new_details_invented=False),
        decision=dict(classification='B_GENERALIZED_ENVELOPE_RETAINED_WITH_DEMOGRAPHIC_CORRECTION',evidence=[prefix+'SECTOR_AUDIT.md',prefix+'BOUNDARY_AUDIT.json',prefix+'DEMOGRAPHY.json'],
            authority='Current user request authorizes research and defensible implementation; no runtime approval for this installation'),
        residual_uncertainty='Enveloppe générale B conservée, pas cadastre ni recalage cellule par cellule; micro-limites Eger/Asch et près de Glatz, enclaves locales non certifiées. Total 1776 arrondi 2,5 M, plage de travail 2,35–2,60 M; proportions culturelles/sociales héritées non établies par un recensement de 1776. Abstraction gouvernement/loi AUS conservée. Viabilité emploi/fiscalité/conscription et rendu attendent le joueur.',
        current_delivery_note='Audit daté en six sous-lots, 21 RGB/4412 cellules AUS conservés; seule installation BOH-D : neuf tailles de population, 3375003→2500000. Statique et contrats courants réussis; trois anciennes assertions de dernière couche conservées dans le journal des tests. Aucun reçu humain SC2 ni point nouveau.')
    state['mission_status']='SC2_BOHEMIA_INSTALLED_PENDING_USER_VALIDATION'
    candidate=rm.progress(state)['next_task'];assert candidate=='SC2-MORAVIA'
    state['runtime_validation_hold']=dict(task_id=t['id'],protocol=prefix+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,source=prefix+'AUTHORIZATION.md',
        reason='Finish current pass with player validation; identify but do not start another geographical task',
        test_summary='Nouvelle partie au 1er janvier 1776 sous AUS : vérifier la Bohême à environ 2,5 millions, ses trois groupes de population hérités, bâtiments/conscrits, contours et voisins conservés, centre régional Prague et système impérial. Simuler un mois puis sauvegarder/recharger; signaler anomalies et limites d’observation.',
        scope_note='Salzbourg conserve son reçu limité au noyau B de 12 cellules. La Bohême reste une enveloppe générale B, sans nouveau tracé cadastral. Les micro-frontières et proportions culturelles de 1776 demeurent non certifiées; l’effet de la correction démographique sur emploi/fiscalité attend le test.')
    after=rm.progress(state);assert (after['earned_weight'],after['total_weight'],after['percent'],after['next_task'])==(66,235,'28.09','SC2-BOHEMIA')
    state['events'].append(dict(id='SERG-RM-0005',date='2026-10-19',kind='SCOPED_IMPLEMENTATION',scope_version=state['scope_version'],source=prefix+'AUTHORIZATION.md',
        changes=[dict(task_id=t['id'],before='NOT_STARTED',after=t['status'])],before_percent=before['percent'],after_percent=after['percent'],
        before_weight=66,after_weight=66,total_weight=235,evidence=[prefix+'REPORT.md',prefix+'VALIDATION.json',prefix+'TESTS.json',prefix+'SCOPED_TESTS.json',prefix+'PLAYER_TEST_PROTOCOL.md'],
        note='SC2-BOHEMIA sélectionné P0 sans dépendance après réception Salzbourg. Audit daté BOH-W/N/E/S/I : 21 RGB et 4412 cellules AUS conservés, sans faux tracé précis. Installation BOH-D : population 3375003→estimation arrondie 2500000, neuf tailles seules; autres régions/bâtiments/unités/registre inchangés. Tests statiques actuels réussis; trois anciennes assertions de dernière couche signalées, aucune nouvelle erreur inexpliquée. Validation joueur absente : 66/235 = 28,09 % maintenus. Prochaine action test Bohême; SC2-MORAVIA identifié P0 et laissé NOT_STARTED. Aucun Git écrit.'))
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(p,state);rm.render()
    result=rm.check();dump('TRACKER_VALIDATION.json',result)
    assert result['status']=='PASS',result
    assert [t for t in state['tasks'] if t['id']!='SC2-BOHEMIA']==[t for t in b['tasks'] if t['id']!='SC2-BOHEMIA']
    assert state['events'][:-1]==b['events'] and state['source_manifest']==b['source_manifest']
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_identical=True,all_20_accepted_tasks_preserved=True,old_events_identical=True,source_manifest_identical=True,
        scope_version_unchanged=True,earned_weight=66,total_weight=235,before_percent='28.09',after_percent='28.09',new_user_receipt=False,
        next_action='PLAYER_TEST_SC2_BOHEMIA',next_implementation_candidate='SC2-MORAVIA',candidate_started=False))
    print('Tracker PASS: 66/235, no new credit, player Bohemia; Moravia not started')

def report():
    v=load(OUT/'VALIDATION.json');t=load(OUT/'TESTS.json');s=load(OUT/'SCOPED_TESTS.json')
    assert v['passed']==v['total'] and not v['failed'] and s['status']=='PASS' and not t['unexplained_failures']
    text=f'''# SC2-BOHEMIA — livraison du 19 octobre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 28,09 %**

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — livraison `READY_FOR_SCOPED_RUNTIME_VALIDATION`. La nouvelle installation n'a aucun reçu humain. Le dossier comprend un audit daté des grands contours et juridictions et une correction démographique; aucune nouvelle frontière dessinée.

## Progression et sélection

Début de demande : 60/235 = 25,53 %, 19 jalons justifiés. Le reçu utilisateur explicite est enregistré pour le seul noyau Salzbourg de 12 cellules B : 66/235 = 28,09 %, 20 jalons justifiés. Le validateur sélectionne alors SC2-BOHEMIA, P0 sans dépendance. Après cette installation en attente : **66/235 = 28,09 %**, poids de la Bohême non acquis. Aucun changement de barème, de périmètre 1.0.0 ou de dénominateur.

Le reçu salzbourgeois est [conservé dans son dossier](../SC1-SALZBURG/RUNTIME_USER_ATTESTATION_2026_10_19.json). Il reprend uniquement le protocole global confirmé, un mois et sauvegarde/rechargement sans anomalie. Aucune langue, date réelle de test, mesure moteur ou observation détaillée supplémentaire n'est inventée.

## Correction installée et preuve de périmètre

Un seul fichier fonctionnel : `common/history/pops/00_west_europe.txt`, seulement **neuf valeurs size** dans STATE_BOHEMIA / AUS. Total **3 375 003 → 2 500 000**, soit **−875 003 habitants**. Le total est une estimation arrondie de scénario; les repères comparables de Bohême seule et les limites de méthode sont exposés dans [SOURCES.md](SOURCES.md) et [DEMOGRAPHY.json](DEMOGRAPHY.json). Ce n'est pas un recensement exact de 1776.

Les neuf groupes sont redimensionnés au prorata par plus forts restes, en conservant cultures, religions, métiers et ordre. Totaux initiaux attendus : tchèque 1 550 934, allemand du Sud 903 287, ashkénaze 45 779. Ces proportions héritées ne sont pas présentées comme un nouveau relevé historique. La population mondiale écrite passe de **{v['world_before']:,}** à **{v['world_after']:,}**; tout l'écart provient de Bohême, sans population déplacée ailleurs.

21 RGB, **4 412 cellules**, State_ID **52**, propriétaire **AUS**, inchangés. Liste exhaustive avant/après et contacts voisins dans [BOUNDARY_AUDIT.json](BOUNDARY_AUDIT.json); inventaire [NATIVE_INVENTORY.png](NATIVE_INVENTORY.png). Le statut B signifie une enveloppe politique généralisée conservée, sans précision cadastrale. [SECTOR_AUDIT.md](SECTOR_AUDIT.md) explique séparément BOH-W/N/E/S/I/D, les cartes effectivement lues et les décisions.

Aucun changement de province, pays, capitale, personnage, gouvernement, loi, bâtiment, niveau, propriétaire économique, PM ou unité. AUS conserve Marie-Thérèse, la capitale nationale Vienne, le centre régional Prague et son abstraction des états provinciaux. Le gubernium historique n'est pas transformé en souverain indépendant. Une substitution de PM bureaucratique a été rejetée car incompatible avec la loi AUS; aucune loi nationale n'est modifiée pour contourner cette contrainte.

Registre impérial **574 entrées**, neuf électeurs et fichiers compilés identiques à la capture immédiate. Pas de nouveau membre BOH ni duplication de son titre. Les noyaux déjà acquis, notamment Salzbourg, et toutes les autres populations régionales sont conservés. Le fichier de population est partagé avec Salzbourg : sa seule empreinte globale change, tandis que **tous les octets hors des neuf tailles bohémiennes restent identiques**, dont le bloc SLZ.

## Vérifications effectuées

- **{v['passed']}/{v['total']} contrôles statiques et de non-régression réussis** : portée textuelle exacte, analyse syntaxique, propriétaires/géométries, populations hors Bohême, variations globales culture/confession, bâtiments/unités, registre, preuves archivées, acquis et Git. [VALIDATION.json](VALIDATION.json).
- Suite cumulative : **{t['passed']} réussites sur {t['total']}**, **3 échecs hérités**, **1 exclusion d'initialisation**. Les trois échecs sont les mêmes assertions d'ancienne dernière couche déjà identifiées avant SC2; elles attendent une couche antérieure à Salzbourg en fin de registre. Elles ne sont ni supprimées ni rendues artificiellement vertes. **Aucun nouvel échec inexpliqué.** [TESTS.json](TESTS.json), [journal brut](TESTS.log), [analyse](TEST_REVIEW.json).
- Contrats courants de Bohême, Salzbourg et feuille de route : **{s['passed']} réussites sur {s['total']}**, aucune erreur et une exclusion d'initialisation. Tests négatifs : refus d'un changement de région, culture, religion, métier, nombre de groupes, commentaire ou total; invariants de progression et de passage au joueur. [SCOPED_TESTS.json](SCOPED_TESTS.json).
- Les **44 RGB dupliqués et 12 références invalides hérités** restent identiques à la capture; aucune nouvelle anomalie de ce type. Ce résultat ne les résout pas et ne signifie pas que l'ensemble du mod est sans défaut.
- Aucun moteur exécuté par l'agent. Aucun commit, push, staging, merge, reset, rebase ou changement de branche; HEAD, branche et empreinte de l'index sont conservés.

## Attente et limites restantes

Le total annuel exact de 1776, les proportions culturelles/sociales, micro-limites Eger/Asch, enclaves et détails près de Glatz ne sont pas établis. Les cartes anciennes sont contrôlées par les cessions de 1635/1742/1763 et les réformes de 1751/1763; leurs couleurs ou douze cercles ne deviennent pas le droit de 1776. Aucune correspondance source-vers-cellule assez précise n'a été établie pour justifier une retouche. Les régions Moravie, Silésie et Teschen ne sont pas déclarées auditées intégralement par cette passe.

La baisse de population agit sur emploi, fiscalité, consommation et recrutement; ces effets doivent être examinés dans une nouvelle partie. Les bâtiments et conscrits sont conservés, sans compensation arbitraire. **Validation utilisateur en attente.** [Protocole détaillé](PLAYER_TEST_PROTOCOL.md) : Autriche au 1er janvier 1776, contrôles par sous-lot, un mois, sauvegarde/rechargement. Tout résultat non observé doit rester signalé comme tel.

Prochaine action : **test joueur SC2-BOHEMIA**. Prochain candidat d'implémentation après résultat : **SC2-MORAVIA**, P0, dépendances actuelles satisfaites, **NOT_STARTED**. Aucune recherche ou installation de ce lot n'a été entreprise. La sélection sera recalculée à la réception du test et d'une mission autorisée.

Les événements de progression restent additifs : RM-0004 reçoit Salzbourg, RM-0005 livre la Bohême sans point supplémentaire. Les autres 80 fiches restent identiques à la capture qui suit l'acceptation salzbourgeoise. [Vérification du suivi](TRACKER_VALIDATION.json), [conservation](TRACKER_PRESERVATION.json), [manifeste final](DELIVERY_MANIFEST.json).
'''
    (OUT/'REPORT.md').write_text(text.replace('835,801,255','835 801 255').replace('834,926,252','834 926 252'),encoding='utf8')
    print('Report written; evidence counts and limitations explicit')

def delivery():
    b=load(OUT/'BASELINE.json');v=load(OUT/'VALIDATION.json');assert v['passed']==v['total'] and not v['failed']
    tracker=rm.check();assert tracker['status']=='PASS';dump('FINAL_TRACKER_VALIDATION.json',tracker)
    old=(OUT/'POPS_BEFORE.txt').read_bytes();new=(ROOT/POP_PATH).read_bytes();validate_scope(old.decode('utf8'),new.decode('utf8'))
    left=old.decode('utf8').splitlines();right=new.decode('utf8').splitlines();assert len(left)==len(right)
    changes=[(i,a,z) for i,(a,z) in enumerate(zip(left,right),1) if a!=z]
    assert len(changes)==9 and all(a.strip().startswith('size = ') and z.strip().startswith('size = ') for _,a,z in changes)
    # Context-free hunks avoid heuristic realignment of the repeated create_pop blocks.
    delta=['--- '+POP_PATH+' (before)','+++ '+POP_PATH+' (after)']
    for i,a,z in changes:delta += [f'@@ -{i} +{i} @@','-'+a,'+'+z]
    (OUT/'INSTALLED.patch').write_text('\n'.join(delta)+'\n',encoding='utf8')
    added=[s[1:] for s in delta if s.startswith('+') and not s.startswith('+++')]
    assert len(added)==9 and all(s.strip().startswith('size = ') for s in added)
    assert not any(s.rstrip()!=s for s in added)
    dump('DIFF_CHECK.json',dict(added_lines=9,removed_lines=9,all_changed_lines_are_size_values=True,new_trailing_whitespace=[],
        outside_nine_numeric_values_byte_identical=True,before_sha256=sha(OUT/'POPS_BEFORE.txt'),after_sha256=sha(ROOT/POP_PATH),git_writes=False))
    assert sha(ROOT/'.git/index')==b['git_index_sha256']
    paths=[POP_PATH,'tools/serg_sc2_bohemia.py','tools/test_serg_sc2_bohemia.py','tools/serg_closure_roadmap.py','tools/serg_closure_accept_salzburg.py']
    paths += [(rm.OUT/n).relative_to(ROOT).as_posix() for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]
    paths += [p.relative_to(ROOT).as_posix() for p in OUT.iterdir() if p.is_file() and p.name!='DELIVERY_MANIFEST.json']
    dump('DELIVERY_MANIFEST.json',dict(task_ids=['SC2-BOHEMIA'],date='2026-10-19',status='READY_FOR_SCOPED_RUNTIME_VALIDATION',
        session_before_percent='25.53',after_salzburg_percent='28.09',after_bohemia_percent='28.09',earned_weight=66,total_weight=235,
        runtime_files=[POP_PATH],runtime_user_validation=False,git_writes=False,git_head=b['git_head'],git_branch=b['git_branch'],git_index_sha256=b['git_index_sha256'],
        static_passed=v['passed'],static_total=v['total'],tests='TESTS.json',scoped_tests='SCOPED_TESTS.json',test_review='TEST_REVIEW.json',
        next_action='PLAYER_TEST_SC2_BOHEMIA',next_implementation_candidate='SC2-MORAVIA',candidate_started=False,
        sha256={p:sha(ROOT/p) for p in paths}))
    print('Delivery: one runtime file, nine sizes, 66/235, no Git writes; Moravia not started')

if __name__=='__main__':globals()[sys.argv[1]]()
