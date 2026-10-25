"""SC2 Anterior Austria: bounded foreland and Adriatic evidence."""
import collections as C
import io
import json
import subprocess
import sys
import unittest
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc2_inner_austria as prior
import serg_closure_roadmap as rm
import map2l_registry as reg

ROOT=prior.ROOT
OUT=rm.OUT/'SC2-ANTERIOR-AUSTRIA'
TASK='SC2-ANTERIOR-AUSTRIA'
WEST={'STATE_BADEN','STATE_WURTTEMBERG','STATE_BAVARIA'}
ADMIN_FILES={
    'STATE_BADEN':'common/history/buildings/1776_sc2_anterior_austria_forelands.txt',
    'STATE_ISTRIA':'common/history/buildings/1776_sc2_anterior_austria_adriatic.txt',
}
PORT_FILE='common/history/buildings/01_south_europe.txt'
core=prior.shared.core
sha=prior.shared.sha
runtime_hashes=prior.shared.runtime_hashes


def load(p):return rm.load_json(p)
def dump(name,obj):rm.write_json(OUT/name,obj)


def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=prior.shared.core.packed(ROOT/'map_data/provinces.png')
    own={r['key'][0]:r['key'][1:] for r in inv['owners']};registered={r['rgb']:r for r in b['registry']}
    keys=sorted(k for k,sid in inv['geometry'].items() if sid=='STATE_ISTRIA' or sid in WEST and own[k][1]=='AUS')
    rows=[]
    for rgb in keys:
        y,x=np.where(a==int(rgb[1:],16));sid,tag=own[rgb];neighbors=C.Counter()
        for yy,xx in zip(y,x):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                other='x'+format(int(a[yy+dy,xx+dx]),'06X')
                if other!=rgb:neighbors[other]+=1
        rows.append(dict(rgb=rgb,state_before=sid,state_after=sid,owner_before=tag,owner_after=tag,
            cells_before=len(x),cells_after=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())],
            centroid=[float(x.mean()),float(y.mean())],registry=registered.get(rgb),
            scope='PROTECTED_WESTERN_CORE' if sid in WEST else 'ADRIATIC_APPROXIMATION_TO_AUDIT',
            neighbors=[dict(rgb=q,state=own.get(q,[inv['geometry'].get(q),''])[0],owner=own.get(q,['',''])[1],edges=n) for q,n in sorted(neighbors.items())]))
    regions={}
    for sid in sorted(WEST|{'STATE_ISTRIA'}):
        regions[sid]={tag:dict(population=sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[sid,tag]),
            population_groups=[r for r in inv['regional_pop'] if r['key'][:2]==[sid,tag]],
            buildings=[r for r in inv['buildings'] if r['key'][:2]==[sid,tag]],
            units=[r for r in inv['units'] if r['key'][0]==tag and r['key'][2]==sid])
            for tag in (['AUS','VEN'] if sid=='STATE_ISTRIA' else ['AUS'])}
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,regions=regions,territory_changed=False,cadastral_precision=False))
    for name,box,anchors in [('WEST',(4250,885,4350,947),[(4274.973,918.303,'Fribourg (jeu)'),(4302.231,925.839,'Constance (jeu)')]),
            ('ADRIATIC',(4380,950,4440,1020),[(4412.139,990.417,'Trieste'),(4405.898,968.58,'Udine (jeu)'),(4414.215,977.657,'Gorizia'),(4412.25,1007.361,'Pula'),(4418.629,995.616,'Opatija')])]:
        x0,y0,x1,y1=box;scale=9
        im=Image.new('RGB',((x1-x0)*scale+90,(y1-y0)*scale+100),'#faf8ef');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
        for y in range(y0,y1):
            for x in range(x0,x1):
                k='x'+format(int(a[y,x]),'06X');tag=own.get(k,['',''])[1]
                col={'AUS':'#ddc37d','VEN':'#afc9dd','BAD':'#c1d5ae','WUR':'#d0bccd','FRA':'#d9c6b2','SWI':'#c5d4d5'}.get(tag,'#e2e1df')
                u,v=45+(x-x0)*scale,45+(y-y0)*scale
                d.rectangle((u,v,u+scale,v+scale),fill=col)
                if a[y,x]!=a[y,x-1]:d.line((u,v,u,v+scale),fill='#7d7c77')
                if a[y,x]!=a[y-1,x]:d.line((u,v,u+scale,v),fill='#7d7c77')
        for i,r in enumerate(rows,1):
            x,y=r['centroid']
            if x0<=x<x1 and y0<=y<y1:
                r['map_number']=i;d.text((45+(x-x0)*scale,45+(y-y0)*scale),str(i),font=font,fill='black',stroke_width=1,stroke_fill='white')
        for x,y,label in anchors:
            u,v=45+(x-x0)*scale,45+(y-y0)*scale;d.ellipse((u-3,v-3,u+3,v+3),fill='#152e33');d.text((u+5,v+3),label,font=font,fill='black',stroke_width=1,stroke_fill='white')
        d.text((10,10),'SC2-ANTERIOR-AUSTRIA : données natives, sans frontière historique superposée',font=font,fill='black')
        d.text((10,im.height-38),'Ocre AUS; bleu VEN; vert BAD; violet WUR. Numéros RGB de l’inventaire.',font=font,fill='black')
        d.text((10,im.height-20),'Les locators économiques ne prouvent ni souveraineté ni limite historique.',font=font,fill='black')
        im.save(OUT/('NATIVE_'+name+'.png'))
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,regions=regions,territory_changed=False,cadastral_precision=False))
    for r in rows:print(r['rgb'],r['state_before'],r['owner_before'],r['cells_before'],r['bounds'],flush=True)


def expected_admin(sid):
    assert sid in ADMIN_FILES
    return prior.expected_admin('STATE_STYRIA').replace('SC2-INNER-AUSTRIA',TASK).replace(
        'Inner Austrian public administration',
        'the Freiburg foreland government' if sid=='STATE_BADEN' else 'the Adriatic public offices existing on 1 January 1776').replace(
        's:STATE_STYRIA','s:'+sid)


def admin_contract(raw,sid):
    assert [core.qa.signature(n) for n in core.cw.parse(raw)]==[
        core.qa.signature(n) for n in core.cw.parse(expected_admin(sid))], 'Administration scope leak'
    return True


def port_candidate(raw):
    region=core.region(raw,'STATE_ISTRIA','AUS')
    nodes=[n for n in region.children('create_building') if core.cw.scalar(n.one('building'))=='building_port']
    assert len(nodes)==1, 'Exactly one scoped port declaration required'
    node=nodes[0]
    baseline=load(OUT/'BASELINE.json')['inventory']['buildings']
    allowed=[r['key'][2] for r in baseline if r['key'][:2]==['STATE_ISTRIA','AUS'] and 'building_port' in r['key'][2]]
    assert allowed==[core.qa.signature(node)], 'Concurrent port payload or already applied correction'
    ownership=node.children('add_ownership');assert len(ownership)==1
    holders=ownership[0].children('country');assert len(holders)==1
    countries=holders[0].children('country');assert len(countries)==1
    field=countries[0];assert core.cw.scalar(field.value)=='c:VEN'
    assert core.cw.scalar(holders[0].one('levels'))=='2'
    token=raw[field.start:field.end];assert token.count('"c:VEN"')==1
    candidate=core.edits(raw,[(field.start,field.end,token.replace('"c:VEN"','"c:AUS"'))])
    return candidate,node


def port_contract(before,after):
    assert after==port_candidate(before)[0], 'Change outside the single national port owner'
    return True


def install():
    b=load(OUT/'BASELINE.json')
    assert load(rm.OUT/'ROADMAP_STATE.json')==b['roadmap'], 'Concurrent tracker change'
    assert rm.progress(b['roadmap'])['next_task']==TASK
    assert all((OUT/n).is_file() for n in ['AUTHORIZATION.md','SOURCES.md','SECTOR_AUDIT.md'])
    anchor=load(OUT/'INSTALL_BASELINE.json')['hashes'] if (OUT/'INSTALL_BASELINE.json').exists() else b['hashes']
    assert runtime_hashes()==anchor, 'Concurrent runtime change requires fresh review'
    assert not (OUT/'IMPLEMENTATION.json').exists()
    assert all(not (ROOT/p).exists() for p in ADMIN_FILES.values())
    for sid in ADMIN_FILES:
        assert not any(r['key'][:2]==[sid,'AUS'] and 'building_government_administration' in r['key'][2]
            for r in b['inventory']['buildings'])
    target=ROOT/PORT_FILE;before=target.read_bytes();after,_=port_candidate(before.decode('utf8'))
    port_contract(before.decode('utf8'),after)
    (OUT/'PUBLIC_PORT_BEFORE.txt').write_bytes(before)
    (OUT/'PUBLIC_PORT_CANDIDATE.txt').write_bytes(after.encode('utf8'))
    assert sha(target)==b['hashes'][PORT_FILE] and target.read_bytes()==before
    for sid,path in ADMIN_FILES.items():
        raw=expected_admin(sid);admin_contract(raw,sid)
        with (ROOT/path).open('xb') as f:f.write(raw.encode('utf8'))
    assert target.read_bytes()==before, 'Concurrent shared-file edit'
    target.write_bytes(after.encode('utf8'))
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_PENDING_STATIC_CHECKS',
        sub_lots=[dict(id='AN-I-W' if sid=='STATE_BADEN' else 'AN-I-A',state=sid,file=p,
            building='building_government_administration',levels_before=0,levels_after=1,owner='c:AUS',production_methods=prior.PMS)
            for sid,p in ADMIN_FILES.items()]+[dict(id='AN-P-A',file=PORT_FILE,state='STATE_ISTRIA',
                building='building_port',levels_before=2,levels_after=2,owner_before='c:VEN',owner_after='c:AUS')],
        territory_changed=False,population_changed=False,registry_changed=False,
        shipyard_changed=False,private_ownership_changed=False,automated_engine_test=False))
    print('Installed two regional administrations and one national port owner correction',flush=True)


def validate():
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for field in inv:
        if field not in {'buildings','building_levels_written'}:
            ck('Whole effective inventory retained: '+field,inv[field]==b['inventory'][field])
    expected=core.qa.counter(b['inventory']['buildings'])
    for sid,path in ADMIN_FILES.items():
        raw=(ROOT/path).read_text(encoding='utf8');ck('Exact administration contract: '+sid,admin_contract(raw,sid))
        node=core.region(raw,sid,'AUS').children('create_building')[0]
        expected[(sid,'AUS',core.qa.signature(node))]+=1
    before=(OUT/'PUBLIC_PORT_BEFORE.txt').read_bytes().decode('utf8')
    after=(ROOT/PORT_FILE).read_bytes().decode('utf8')
    ck('Shared building file: one country token only, other bytes identical',port_contract(before,after))
    oldnode=port_candidate(before)[1]
    newnode=next(n for n in core.region(after,'STATE_ISTRIA','AUS').children('create_building')
        if core.cw.scalar(n.one('building'))=='building_port')
    expected[('STATE_ISTRIA','AUS',core.qa.signature(oldnode))]-=1
    expected[('STATE_ISTRIA','AUS',core.qa.signature(newnode))]+=1
    ck('Only two administrations plus one port owner changed worldwide',core.qa.counter(inv['buildings'])==+expected)
    levels=core.qa.counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=2
    ck('Global written capacity delta: two administration levels only',core.qa.counter(inv['building_levels_written'])==levels)
    current=runtime_hashes();anchor=load(OUT/'INSTALL_BASELINE.json')['hashes']
    delta=sorted(p for p in set(current)|set(anchor) if current.get(p)!=anchor.get(p))
    ck('Exactly three runtime files written',set(delta)==set(ADMIN_FILES.values())|{PORT_FILE},delta)
    ck('All other current runtime files byte-identical, including concurrent additions',all(current.get(p)==h for p,h in anchor.items() if p!=PORT_FILE))
    ck('Full province bitmap retained',current['map_data/provinces.png']==b['hashes']['map_data/provinces.png'])
    ck('All 574 imperial registry rows retained',len(b['registry'])==574 and load(reg.active_registry_path())==b['registry'])
    ck('Accepted Salzburg registry tail retained',reg.approved_lot_dirs()[-1]==prior.shared.prior.prior.OUT)
    rows=load(OUT/'NATIVE_INVENTORY.json')['provinces']
    ck('Five protected foreland RGB and 116 cells',len([r for r in rows if r['state_before'] in WEST])==5 and sum(r['cells_before'] for r in rows if r['state_before'] in WEST)==116)
    ck('Six Adriatic RGB and 795 cells',len([r for r in rows if r['state_before']=='STATE_ISTRIA'])==6 and sum(r['cells_before'] for r in rows if r['state_before']=='STATE_ISTRIA')==795)
    for r in rows:
        ck('Native political core retained: '+r['rgb'],[x for x in inv['owners'] if x['key'][0]==r['rgb']]==[
            dict(key=[r['rgb'],r['state_before'],r['owner_before']],count=1)] and inv['geometry'][r['rgb']]==r['state_before'])
        if r['owner_before']=='AUS':ck('Imperial beneficiary retained: '+r['rgb'],r['registry']['beneficiary']=='AUS')
    for sid,tag,total in [('STATE_BADEN','AUS',68095),('STATE_WURTTEMBERG','AUS',1973),
            ('STATE_BAVARIA','AUS',10194),('STATE_ISTRIA','AUS',339850),('STATE_ISTRIA','VEN',340246)]:
        ck('Initial population retained: '+sid+'/'+tag,sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[sid,tag])==total)
    ck('World population retained',sum(r['count'] for r in inv['pops'])==834926252)
    ck('Inherited 44 duplicates and 12 invalid references unchanged',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    ck('Ljubljana region byte-identical in shared file',
        core.qa.signature(core.region(before,'STATE_SLOVENIA','AUS'))==core.qa.signature(core.region(after,'STATE_SLOVENIA','AUS')))
    ck('Accepted Ljubljana overlay file byte-identical',current['common/history/buildings/98_build_start_1776_world_redistribution.txt']==b['hashes']['common/history/buildings/98_build_start_1776_world_redistribution.txt'])
    for sid in ['STATE_STYRIA','STATE_SLOVENIA']:
        ck('Inner Austrian administration retained: '+sid,current[prior.ADMIN_FILES[sid]]==b['hashes'][prior.ADMIN_FILES[sid]])
    ck('Moravia administration retained',current[prior.shared.ADMIN_PATH]==b['hashes'][prior.shared.ADMIN_PATH])
    state=load(rm.OUT/'ROADMAP_STATE.json');qualified=rm.qualifications(state)
    ck('All 24 acquired tasks remain qualified',sum(qualified.values())==24 and all(qualified[k] for k,v in rm.qualifications(b['roadmap']).items() if v))
    ck('Inner Austria human receipt retained',next(t for t in state['tasks'] if t['id']==prior.TASK)['status']=='PASS_RUNTIME_USER_VALIDATED')
    ck('Innviertel remains blocked and Teschen independent',next(t for t in state['tasks'] if t['id']=='SC2-AUSTRIA')['status']=='BLOCKED' and next(t for t in state['tasks'] if t['id']=='SC2-TESCHEN')['status']=='NOT_STARTED')
    ck('Previous reports and attestations byte-identical',all(sha(ROOT/p)==h for p,h in b['report_hashes'].items() if (ROOT/p).parent!=rm.OUT))
    changed_tools=[p for p,h in b['tool_hashes'].items() if sha(ROOT/p)!=h]
    ck('Old tools unchanged except documented roadmap renderer extension',set(changed_tools)<={'tools/serg_closure_roadmap.py'},changed_tools)
    def definitions(folder):
        return {n.key:n for p in core.qa.effective(ROOT,core.qa.GAME,folder) for n in core.cw.parse(p.read_text(encoding='utf-8-sig'))}
    pms=definitions('common/production_methods');groups=definitions('common/production_method_groups');buildings=definitions('common/buildings')
    aus=core.cw.parse((ROOT/'common/history/countries/aus - austria.txt').read_text(encoding='utf-8-sig'))[0].children()[0]
    laws={core.cw.scalar(n.value).removeprefix('law_type:') for n in aus.children('activate_law')}
    tech={core.cw.scalar(n.value) for n in aus.children('add_technology_researched')}
    pmgroups=[core.cw.scalar(n.value) for n in buildings['building_government_administration'].children('production_method_groups')[0].children()]
    for key in prior.PMS:
        ck('Effective production method exists: '+key,key in pms)
        node=pms[key]
        values=lambda f:{core.cw.scalar(n.value) for n in node.children(f)[0].children()} if node.children(f) else set()
        ck('Method available to initial AUS: '+key,(not values('unlocking_laws') or bool(values('unlocking_laws')&laws)) and not values('disallowing_laws')&laws and values('unlocking_technologies')<=tech)
        ck('One compatible method group: '+key,len([g for g in pmgroups if key in {core.cw.scalar(n.value) for n in groups[g].children('production_methods')[0].children()}])==1)
    ck('One selected method per group',len(prior.PMS)==len(pmgroups))
    ck('Git HEAD, branch and index unchanged',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==b['git_head'] and subprocess.check_output(['git','branch','--show-current'],text=True).strip()==b['git_branch'] and sha(ROOT/'.git/index')==b['git_index_sha256'])
    for r in load(OUT/'SOURCE_FILES.json'):
        ck('Source file retained: '+r['file'],sha(ROOT/r['file'])==r['sha256'])
    v=dict(task_ids=[TASK],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'FAIL',
        total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,
        engine_executed=False,automated_engine_test=False,runtime_validation='PENDING_USER',regional_status='BLOCKED',points_awarded=0)
    dump('VALIDATION.json',v)
    dump('FILES_MODIFIED.json',dict(runtime_files_written_by_this_pass=delta,existing_runtime_files_written_by_this_pass=[PORT_FILE],
        sha256={p:current[p] for p in delta},baseline_runtime_file_count=len(b['hashes']),install_runtime_file_count=len(anchor),current_runtime_file_count=len(current),
        concurrent_additions=load(OUT/'INSTALL_BASELINE.json')['concurrent_files'],
        concurrent_technology_preserved=current['common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt']==b['hashes']['common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt'],old_tools_changed=changed_tools))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True)
    assert not v['failed']


def tests():
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01',
        'test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion',
        'test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc',
        'test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia',
        'test_serg_sc2_inner_austria','test_serg_sc2_anterior_austria']
    inherited=set(load(prior.previous.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    for label,modules in [('TESTS',names),('SCOPED_TESTS',names[-6:])]:
        stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
        unexplained=[f for f in failures if f['id'] not in inherited]
        dump(label+'.json',dict(task_ids=[TASK],status='PASS' if not failures else 'INHERITED_FAILURES_ONLY' if not unexplained else 'FAIL',
            total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,
            skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,'unexplained',len(unexplained),flush=True)
        for f in unexplained:print(f['id'],f['traceback'],flush=True)
        assert not unexplained
        assert {f['id'] for f in failures}==(inherited if label=='TESTS' else set())
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),unexplained_failures=[],
        old_tests_not_modified=True,engine_executed=False,
        explanation='Three old tests assume an obsolete registry tail. Current 574 rows and approved Salzburg tail pass. One initialization-only test is explicitly skipped. No old test changed.'))


def tracking():
    import copy
    v=load(OUT/'VALIDATION.json');tests_result=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert v['total']==v['passed'] and not v['failed']
    assert not tests_result['unexplained_failures'] and not scoped['failed']
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==load(OUT/'BASELINE.json')['roadmap'], 'Concurrent tracker update requires reconciliation'
    t=next(t for t in state['tasks'] if t['id']==TASK)
    assert t['status']=='NOT_STARTED' and rm.progress(state)['next_task']==TASK
    prefix='docs/reports/map/SERG_CLOSURE/SC2-ANTERIOR-AUSTRIA/'
    implementation=load(OUT/'IMPLEMENTATION.json')
    implementation['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    for sub in implementation['sub_lots']:sub['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    dump('IMPLEMENTATION.json',implementation)
    block='P0 : Hohenberg et Fricktal habsbourgeois en 1776 ne sont pas couverts de façon démontrée par les cinq noyaux occidentaux; candidats RGB et approximation politique B à établir, sans recalage forcé. P1 : propriété du chantier naval de la portion AUS à documenter; ni sa nationalisation autrichienne ni sa conservation définitive ne sont approuvées.'
    t.update(status='BLOCKED',blocking_reason=block,installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        installed_sub_lots=implementation['sub_lots'],installed_lots=['SERG_CLOSURE/SC2-ANTERIOR-AUSTRIA'],
        implementation_report=[prefix+'REPORT.md'],static_tests=dict(status='PASS',evidence=[prefix+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,new_details_invented=False,
            protocol=prefix+'PLAYER_TEST_PROTOCOL.md',scope='Only AN-I-W, AN-I-A, AN-P-A: two regional public administration levels and national port ownership VEN to AUS. Regional coverage block remains; no task credit from this test alone.'),
        decision=None,residual_uncertainty=block+' Les limites internes de l\'agrégat adriatique, les effectifs historiques et les droits patrimoniaux ne sont pas cadastrés. Les corrections B installées attendent le test du joueur.',
        current_delivery_note='Trois corrections partielles installées, statut IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION : une administration publique AUS dans STATE_BADEN, une dans STATE_ISTRIA, propriétaire national du seul port de la portion AUS corrigé VEN→AUS (deux niveaux conservés). Chantier naval et propriété privée VEN inchangés. 11 RGB/911 cellules inspectés et conservés, dont 8 RGB AUS/411 cellules; aucune population, frontière, unité ou ligne du registre modifiée. La tâche régionale reste BLOCKED pour Hohenberg/Fricktal et la propriété du chantier; aucun point ni nouveau reçu humain. Protocole joueur livré.')
    t['historical_sources'].append(prefix+'SOURCES.md:1')
    t['identified_problem'].append('Absence d\'administration initiale AUS à Fribourg et dans l\'agrégat adriatique; port public de cette portion attribué à VEN. Trois corrections installées séparément; couverture P0 Hohenberg/Fricktal non résolue et chantier naval à arbitrer.')
    t['delivered_scope']=dict(classification='B_POLITICAL_ADMINISTRATIVE_APPROXIMATION',sub_lots=['AN-I-W','AN-I-A','AN-P-A'],
        native_audited_rgb=11,native_audited_cells=911,austrian_rgb=8,austrian_cells=411,
        territory_changed=False,population_changed=False,cadastral_validation=False,regional_acceptance_complete=False)
    state['mission_status']='SC2_ANTERIOR_AUSTRIA_PARTIAL_INSTALLATION_AWAITING_USER_REGIONAL_BLOCK'
    next_candidate=rm.progress(state)['next_task'];assert next_candidate=='SC4-EXISTING-ITALIAN-STATES'
    note=f'Une seule nouvelle tâche P0 exécutée : SC2-ANTERIOR-AUSTRIA, recherche suivie de trois corrections B indépendantes. Deux administrations publiques AUS et propriété nationale du port de la portion AUS corrigée VEN→AUS; capacité portuaire inchangée. Aucun RGB, habitant, unité, registre ou institution impériale transféré. Couverture Hohenberg/Fricktal encore P0; propriété du chantier naval à documenter, sans nationalisation artificielle. Tâche régionale BLOCKED, trois sous-lots IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION; aucun reçu humain ni point. {v["passed"]}/{v["total"]} contrôles statiques; suite cumulative {tests_result["passed"]}/{tests_result["total"]}, trois échecs hérités et une exclusion; suite ciblée {scoped["passed"]}/{scoped["total"]}, une exclusion. Aucun échec inexpliqué. Reçu d\'Autriche intérieure et 24 tâches acquises conservés; macroéconomie et deux nouveaux scripts concurrents de fortifications préservés. 82/235=34,89 % maintenus. Prochaine action joueur : protocole partiel; candidate indépendante SC4-EXISTING-ITALIAN-STATES identifiée, non commencée. Innviertel BLOCKED et Teschen indépendant. Aucune écriture Git ou vanilla.'
    state['events'].append(dict(id='SERG-RM-0015',date='2026-10-19',kind='PARTIAL_IMPLEMENTATION_WITH_REGIONAL_BLOCK',
        scope_version=state['scope_version'],source=prefix+'AUTHORIZATION.md',
        changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_percent='34.89',after_percent='34.89',
        before_weight=82,after_weight=82,total_weight=235,note=note,
        evidence=[prefix+n for n in ['REPORT.md','SOURCES.md','SECTOR_AUDIT.md','NATIVE_INVENTORY.json','IMPLEMENTATION.json','VALIDATION.json','TESTS.json','SCOPED_TESTS.json','PLAYER_TEST_PROTOCOL.md']]))
    assert state['events'][:-1]==original['events']
    assert [x for x in state['tasks'] if x['id']!=TASK]==[x for x in original['tasks'] if x['id']!=TASK]
    assert not rm.structural_errors(state),rm.structural_errors(state)
    p=rm.progress(state)
    assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,next_candidate)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with __import__('contextlib').redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked['errors']
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged_since_inner_acceptance=True,
        previous_14_events_unchanged=True,scope_version_unchanged=True,weights_and_denominator_unchanged=True,
        qualified_tasks=24,earned_weight=82,total_weight=235,percent='34.89',new_runtime_receipts=0,
        task_status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        next_candidate=next_candidate,next_candidate_started=False))
    print('Tracking PASS: 82/235=34.89%; regional block and scoped pending runtime retained; next not started',flush=True)


if __name__=='__main__':
    {'inventory':inventory,'install':install,'validate':validate,'tests':tests,'tracking':tracking}[sys.argv[1]]()
