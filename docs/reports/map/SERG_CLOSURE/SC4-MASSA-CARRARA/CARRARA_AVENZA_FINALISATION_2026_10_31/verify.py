"""Bounded verification of Carrara/Avenza research; no installer or receipt writer."""
from pathlib import Path
import ast,hashlib,io,json,os,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
os.environ['GIT_OPTIONAL_LOCKS']='0'
import serg_sc4_massa_carrara as a
from map2k_patch import ELECTORS

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

def suites():
    results=[]
    for name in ['test_serg_sc4_massa_carrara','test_serg_closure_roadmap']:
        stream=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromName(name)
        r=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
        (OUT/(name+'.log')).write_text(stream.getvalue(),encoding='utf-8')
        results.append(dict(module=name,total=r.testsRun,passed=r.testsRun-len(r.failures)-len(r.errors)-len(r.skipped),failures=[dict(test=t.id(),traceback=s) for t,s in r.failures],errors=[dict(test=t.id(),traceback=s) for t,s in r.errors],skipped=[dict(test=t.id(),reason=s) for t,s in r.skipped],successful=r.wasSuccessful()))
    write('EXISTING_TEST_RESULTS.json',dict(recorded_on='2026-10-31',suites=results,engine_executed=False,legacy_test_sources_changed=False))
    print([(r['module'],r['total'],r['passed'],len(r['failures']),len(r['errors']),len(r['skipped'])) for r in results],flush=True)

def scoped():
    b=read(OUT/'BASELINE.json');inv=a.core.qa.inventory();arr=a.core.packed(ROOT/'map_data/provinces.png');g=read(OUT/'CURRENT_GEOMETRY_AND_OPTIONS.json')
    checks=[]
    def ck(name,value):checks.append(dict(name=name,passed=bool(value)))
    core=set(map(tuple,g['actual_core_cells']));parent=set(map(tuple,g['actual_parent_cells']))
    ck('Validated Massa core retains exact eight cells',core==set(map(tuple,a.CELLS)) and len(core)==8)
    ck('MOD parent retains 108 cells',len(parent)==108)
    ck('Core and parent disjoint with complete 116-cell former footprint',not core&parent and len(core|parent)==116)
    ck('Actual core RGB uniquely owned by MCA',[r for r in inv['owners'] if r['key'][0]==a.RGB]==[dict(key=[a.RGB,a.SID,'MCA'],count=1)])
    ck('Actual parent RGB uniquely owned by MOD',[r for r in inv['owners'] if r['key'][0]==a.PARENT]==[dict(key=[a.PARENT,a.SID,'MOD'],count=1)])
    ck('Both RGB definitions remain in EMILIA',all(inv['geometry'][rgb]==a.SID for rgb in [a.RGB,a.PARENT]))
    expected={'A':(10,106),'B':(13,103),'C':(15,101)}
    diagnostic=[]
    owner={r['key'][0]:r['key'][2] for r in inv['owners']}
    mod_cells=set()
    for rgb,tag in owner.items():
        if tag=='MOD':
            yy,xx=a.np.where(arr==int(rgb[1:],16));mod_cells.update(zip(map(int,xx),map(int,yy)))
    def components(cells):
        left=set(cells);sizes=[]
        while left:
            todo=[left.pop()];n=0
            while todo:
                x,y=todo.pop();n+=1
                for pt in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if pt in left:left.remove(pt);todo.append(pt)
            sizes.append(n)
        return sorted(sizes,reverse=True)
    ck('Current MCA and MOD residual are locally connected',components(core)==[8] and components(parent)==[108])
    for row in g['candidates']:
        extra=set(map(tuple,row['transferred_cells']));name=row['id']
        ck('Candidate cells exist as MOD parent '+name,all(int(arr[y,x])==int(a.PARENT[1:],16) for x,y in extra) and extra<=parent)
        if name in expected:
            mc,mo=expected[name]
            ck('Four-neighbor topology and no lost cells '+name,components(core|extra)==[mc] and components(parent-extra)==[mo] and (core|extra)|(parent-extra)==core|parent)
            ck('No increase in country MOD connected components '+name,len(components(mod_cells-extra))==len(components(mod_cells)))
        else:ck('Rejected original three splits MOD 104 plus 1',components(parent-extra)==[104,1])
        neighbors=[dict(cell=[x,y],adjacent_owner_tags=sorted({owner.get('x'+format(int(arr[yy,xx]),'06X'),'NO_LAND_OWNER') for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]})) for x,y in sorted(extra)]
        diagnostic.append(dict(id=name,MOD_country_components_before=components(mod_cells),MOD_country_components_if_applied=components(mod_cells-extra),adjacency=neighbors,installed=False))
    write('CANDIDATE_COUNTRY_TOPOLOGY.json',diagnostic)
    for key in ['owners','geometry','countries','regional_pop','buildings','units']:
        ck('All current inventory preserved '+key,inv[key]==b['inventory_before'][key])
    world=sum(r['count'] for r in inv['pops']);oldworld=sum(r['count'] for r in b['inventory_before']['pops'])
    ck('World population strictly conserved',world==oldworld)
    populations={tag:sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[a.SID,tag]) for tag in ['MOD','MCA']}
    ck('Current MCA 10000 MOD Emilia 495752',populations=={'MOD':495752,'MCA':10000})
    for tag in ['MOD','GEN','LUC','TUS','PAR']:
        ck('Neighbor owner and population preserved '+tag,[r for r in inv['owners'] if r['key'][2]==tag]==[r for r in b['inventory_before']['owners'] if r['key'][2]==tag] and [r for r in inv['regional_pop'] if r['key'][1]==tag]==[r for r in b['inventory_before']['regional_pop'] if r['key'][1]==tag])
    rows=read(a.reg.active_registry_path())
    ck('581 unique imperial titles unchanged',len(rows)==len({r['rgb'] for r in rows})==581)
    ck('Single original MCA title no second title',[r['rgb'] for r in rows if r['beneficiary']=='MCA']==[a.RGB])
    trigger=(ROOT/'common/scripted_triggers/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
    elector=next(line for line in trigger.splitlines() if 'has_variable = aor1776_hre_electoral_privilege_granted' in line)
    ck('Nine electors preserved in compiled trigger',len(ELECTORS)==9 and all('c:'+t+' ?= this' in elector for t in ELECTORS.values()) and elector.count(' ?= this')==9)
    scripts=['common/history/states/00_states.txt','map_data/state_regions/01_south_europe.txt','common/history/pops/01_south_europe.txt','common/history/buildings/01_south_europe.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt','common/scripted_effects/1776_imperial_constitution.txt','common/scripted_triggers/1776_imperial_constitution.txt','common/country_definitions/1776_sc4_massa_carrara.txt']
    for rel in scripts:a.core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    ck('Eight targeted game scripts parse',True)
    current=a.italian.runtime_hashes()
    drift={p:dict(before=b['runtime_before_sha256'].get(p),after=current.get(p)) for p in set(current)|set(b['runtime_before_sha256']) if current.get(p)!=b['runtime_before_sha256'].get(p)}
    ck('No runtime file changed in isolated worktree',not drift)
    canonical={a.rm.OUT.relative_to(ROOT).as_posix()+'/'+n for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']}
    protected={p:dict(before=h,after=sha(ROOT/p)) for p,h in b['protected_sha256'].items() if p not in canonical and sha(ROOT/p)!=h}
    ck('Historical archives and original receipt unchanged',not protected)
    state=read(a.rm.OUT/'ROADMAP_STATE.json');task=next(t for t in state['tasks'] if t['id']==a.TASK)
    ck('Massa regional P0 BLOCKED unchanged',task['status']=='BLOCKED' and task['priority']=='P0' and task['weight']==3)
    ck('Only original MC-I-CORE receipt remains',task['runtime_validation']['attestation'].endswith('RUNTIME_USER_ATTESTATION_2026_10_23.json') and [p.name for p in a.OUT.glob('RUNTIME_USER_ATTESTATION*')]==['RUNTIME_USER_ATTESTATION_2026_10_23.json'])
    canon=a.rm.check();write('CANONICAL_CHECK.json',canon)
    ck('Canonical PASS and unchanged 93/235 progress',canon['status']=='PASS' and canon['progress']==b['canonical_before']['progress'])
    before=read(OUT/'ROADMAP_STATE_BEFORE.json')
    ck('Other eighty canonical tasks unchanged',[t for t in state['tasks'] if t['id']!=a.TASK]==[t for t in before['tasks'] if t['id']!=a.TASK])
    ck('Historical events unchanged prefix',state['events'][:len(before['events'])]==before['events'])
    ck('Teschen runtime hold unchanged',state.get('runtime_validation_hold')==before.get('runtime_validation_hold'))
    ck('Own verifier syntax valid',ast.parse(Path(__file__).read_text(encoding='utf-8')) is not None)
    result=dict(recorded_on='2026-10-31',status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,world_population_before=oldworld,world_population_after=world,populations=populations,proposed_only_if_territory_validated={'transfer':8010,'MCA':18010,'MOD':487742,'world_delta':0},engine_executed=False,installed=False,runtime_drift=drift,protected_archive_drift=protected)
    write('SCOPED_STATIC_RESULTS.json',result)
    print(result['status'],result['passed'],'/',result['total'],[c['name'] for c in checks if not c['passed']],flush=True)

if __name__=='__main__':
    assert a.ROOT==ROOT,(a.ROOT,ROOT)
    {'tests':suites,'scoped':scoped}[sys.argv[1]]()
