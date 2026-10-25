"""SC4 Savoy-Nice: evidence, bounded changes and conservation checks."""
import collections as C
import contextlib
import copy
import csv
import io
import json
import os
import subprocess
import unittest
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc4_italian_states as prior

os.environ['GIT_OPTIONAL_LOCKS']='0'
ROOT=prior.ROOT
rm=prior.rm
core=prior.core
reg=prior.reg
sha=prior.sha
TASK='SC4-SAVOY-NICE'
OUT=rm.OUT/TASK
PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
ADMIN_FILES={
    'STATE_SAVOY':'common/history/buildings/1776_sc4_savoy_administration.txt',
    'STATE_PROVENCE':'common/history/buildings/1776_sc4_nice_administration.txt',
}
SUB_IDS={'STATE_SAVOY':'SN-I-SAV','STATE_PROVENCE':'SN-I-NIC'}
PMS=prior.PMS

def load(p): return rm.load_json(p)
def dump(name,obj): rm.write_json(OUT/name,obj)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    state=load(rm.OUT/'ROADMAP_STATE.json')
    assert state['events'][-1]['id']=='SERG-RM-0018' and rm.progress(state)['next_task']==TASK
    assert rm.check()['status']=='PASS'
    receipt=next(t for t in state['tasks'] if t['id']==prior.TASK)
    assert rm.partial_runtime_evidence(receipt)
    OUT.mkdir(exist_ok=True)
    accepted=load(prior.OUT/'ACCEPTANCE_SESSION_BEFORE_2026_10_23.json')
    # Acceptance writes only reports. Its fresh world inventory and runtime hashes remain current.
    accepted['roadmap']=state
    protected={}
    for p in rm.OUT.rglob('*'):
        if p.is_file() and OUT not in p.parents:
            protected[p.relative_to(ROOT).as_posix()]=sha(p)
    accepted['report_hashes']=protected
    accepted['tool_hashes']={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py')}
    dump('BASELINE.json',accepted)
    print('Savoy-Nice baseline captured; selection and Italian partial receipt verified',flush=True)

def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    rights={r['rgb']:r for r in b['registry']}
    sids={'STATE_SAVOY','STATE_PROVENCE','STATE_PIEDMONT','STATE_RHONE','STATE_WEST_SWITZERLAND','STATE_EAST_SWITZERLAND'}
    rows=[]
    for rgb,(sid,tag) in sorted(owners.items()):
        if sid not in sids and tag!='SAR': continue
        y,x=np.where(a==int(rgb[1:],16));neighbors=C.Counter()
        for yy,xx in zip(y,x):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                k='x'+format(int(a[yy+dy,xx+dx]),'06X')
                if k!=rgb: neighbors[k]+=1
        rows.append(dict(rgb=rgb,state_before=sid,state_after=sid,owner_before=tag,owner_after=tag,
            cells_before=len(x),cells_after=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())],
            centroid=[float(x.mean()),float(y.mean())],registry=rights.get(rgb),
            neighbors=[dict(rgb=k,state=owners.get(k,[inv['geometry'].get(k),''])[0],owner=owners.get(k,['',''])[1],edges=v) for k,v in sorted(neighbors.items())]))
    summary={sid:dict(rgb=[r['rgb'] for r in rows if r['state_before']==sid and r['owner_before']=='SAR'],
        cells=sum(r['cells_before'] for r in rows if r['state_before']==sid and r['owner_before']=='SAR'),
        population=sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[sid,'SAR']),
        pops=[r for r in inv['regional_pop'] if r['key'][:2]==[sid,'SAR']],
        buildings=[r for r in inv['buildings'] if r['key'][:2]==[sid,'SAR']],
        units=[r for r in inv['units'] if r['key'][0]=='SAR' and r['key'][2]==sid])
        for sid in sorted({r['state_before'] for r in rows if r['owner_before']=='SAR'})}
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,sardinian_states=summary,registry=[r for r in b['registry'] if r['beneficiary']=='SAR']))
    print(json.dumps({k:{f:v[f] for f in ['rgb','cells','population']} for k,v in summary.items()},ensure_ascii=False),flush=True)

def illustrate():
    d=load(OUT/'NATIVE_INVENTORY.json');a=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in load(OUT/'BASELINE.json')['inventory']['owners']}
    x0,y0,x1,y1,scale=4195,944,4300,1055,7
    im=Image.new('RGB',((x1-x0)*scale+80,(y1-y0)*scale+100),'#faf8ef');draw=ImageDraw.Draw(im)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    colors={'SAR':'#e8c26f','FRA':'#b6cde7','SWI':'#bed0a6','GEN':'#d5b0c5','AUS':'#e0d7c8'}
    for y in range(y0,y1):
        for x in range(x0,x1):
            rgb='x'+format(int(a[y,x]),'06X');u,v=40+(x-x0)*scale,40+(y-y0)*scale
            draw.rectangle((u,v,u+scale,v+scale),fill=colors.get(owners.get(rgb),'#eceae4'))
            if a[y,x]!=a[y,x-1]:draw.line((u,v,u,v+scale),fill='#77756f')
            if a[y,x]!=a[y-1,x]:draw.line((u,v,u+scale,v),fill='#77756f')
    focus=[r for r in d['provinces'] if r['state_before']=='STATE_SAVOY' or r['rgb']=='x5080E0']
    for n,r in enumerate(focus,1):
        r['map_number']=n;x,y=r['centroid'];draw.text((40+(x-x0)*scale,40+(y-y0)*scale),str(n),font=font,fill='black',stroke_width=1,stroke_fill='white')
    draw.text((10,10),'Savoie-Nice : propriétaires natifs, numéros du tableau RGB',font=font,fill='black')
    draw.text((10,im.height-40),'Ocre SAR; bleu FRA; vert SWI; violet GEN. Aucun calage historique.',font=font,fill='black')
    draw.text((10,im.height-20),'Les contours du jeu ne certifient ni enclaves ni frontières cadastrales.',font=font,fill='black')
    im.save(OUT/'NATIVE_READING.png')
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['map_number','rgb','state_before','state_after','owner_before','owner_after','cells_before','cells_after']);w.writeheader()
        w.writerows({k:r[k] for k in w.fieldnames} for r in focus)
    dump('NATIVE_INVENTORY.json',d)

def expected_admin(sid):
    assert sid in ADMIN_FILES
    label='the Savoy public offices at Chambery' if sid=='STATE_SAVOY' else 'the Nice public offices and senate'
    return prior.expected_admin('MOD').replace(prior.TASK,TASK).replace('the ducal government at Modena',label).replace('s:STATE_EMILIA','s:'+sid).replace('region_state:MOD','region_state:SAR').replace('"c:MOD"','"c:SAR"')

def admin_contract(raw,sid):
    assert [core.qa.signature(n) for n in core.cw.parse(raw)]==[core.qa.signature(n) for n in core.cw.parse(expected_admin(sid))], 'Out-of-scope administration payload'
    return True

def install():
    b=load(OUT/'BASELINE.json')
    assert load(rm.OUT/'ROADMAP_STATE.json')==b['roadmap'] and rm.progress(b['roadmap'])['next_task']==TASK
    assert all((OUT/n).is_file() for n in ['AUTHORIZATION.md','SOURCES.md','SECTOR_AUDIT.md'])
    assert prior.runtime_hashes()==b['hashes'],'Concurrent runtime change requires review'
    assert not (OUT/'IMPLEMENTATION.json').exists()
    for sid,p in ADMIN_FILES.items():
        assert not (ROOT/p).exists()
        assert not any(r['key'][:2]==[sid,'SAR'] and 'building_government_administration' in r['key'][2] for r in b['inventory']['buildings'])
    for sid,p in ADMIN_FILES.items():
        raw=expected_admin(sid);admin_contract(raw,sid)
        with (ROOT/p).open('xb') as f:f.write(raw.encode('utf8'))
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_PENDING_STATIC_CHECKS',
        sub_lots=[dict(id=SUB_IDS[sid],tag='SAR',state=sid,file=p,building='building_government_administration',levels_before=0,levels_after=1,owner='c:SAR',production_methods=PMS) for sid,p in ADMIN_FILES.items()],
        territory_changed=False,population_changed=False,registry_changed=False,diplomacy_changed=False,imperial_membership_changed=False,
        automated_engine_test=False,historical_staff_count_claim=False))
    print('Two independently testable public administrations installed',flush=True)

def policy():
    effects=prior.definitions('common/scripted_effects');laws=prior.definitions('common/laws');selected={}
    def apply(key):
        value=key.removeprefix('law_type:');assert value in laws
        selected[core.cw.scalar(laws[value].one('group'))]=value
    country=core.cw.parse((ROOT/'common/history/countries/sar - sardinia.txt').read_text(encoding='utf-8-sig'))[0].children()[0]
    for n in country.children():
        if n.key=='effect_starting_politics_reactionary':
            assert core.cw.scalar(n.value)=='yes'
            for e in effects[n.key].children():
                if e.key=='activate_law':apply(core.cw.scalar(e.value))
                elif e.key=='else':
                    for law in e.children('activate_law'):apply(core.cw.scalar(law.value))
        elif n.key=='activate_law':apply(core.cw.scalar(n.value))
    result=dict(laws=selected,technologies=[core.cw.scalar(n.value) for n in country.children('add_technology_researched')],basis='Effective reactionary setup, Catholic branch, then direct overrides in file order')
    dump('INITIAL_POLICIES.json',result);return result

def validate():
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for field in inv:
        if field not in {'buildings','building_levels_written'}:ck('World inventory retained: '+field,inv[field]==b['inventory'][field])
    expected=core.qa.counter(b['inventory']['buildings'])
    for sid,p in ADMIN_FILES.items():
        raw=(ROOT/p).read_text(encoding='utf8');ck('Exact independent administration '+sid,admin_contract(raw,sid))
        node=core.region(raw,sid,'SAR').children('create_building')[0]
        expected[(sid,'SAR',core.qa.signature(node))]+=1
    ck('Exactly two administrations; all other building payloads retained',core.qa.counter(inv['buildings'])==expected)
    levels=core.qa.counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=2
    ck('Only global written capacity delta: two administration levels',core.qa.counter(inv['building_levels_written'])==levels)
    current=prior.runtime_hashes();delta=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    ck('Only two new functional files',set(delta)==set(ADMIN_FILES.values()),delta)
    ck('Every existing functional file byte-identical',all(current.get(p)==h for p,h in b['hashes'].items()))
    ck('574 imperial rights unchanged',len(b['registry'])==574 and load(reg.active_registry_path())==b['registry'])
    ck('Only nine Piedmont SAR rights; no blanket Sardinian inclusion',len([r for r in b['registry'] if r['beneficiary']=='SAR'])==9 and reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}})
    ck('Approved cumulative registry layer retained',reg.approved_lot_dirs()[-1].name=='SC1-SALZBURG')
    for sid,total in [('STATE_SAVOY',365664),('STATE_PROVENCE',134316)]:
        ck('Population retained '+sid,sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[sid,'SAR'])==total)
    ck('World population retained',sum(r['count'] for r in inv['pops'])==834926252)
    native=load(OUT/'NATIVE_INVENTORY.json')
    for row in native['provinces']:
        ck('Native owner retained '+row['rgb'],[r for r in inv['owners'] if r['key'][0]==row['rgb']]==[dict(key=[row['rgb'],row['state_before'],row['owner_before']],count=1)])
    ck('Five audited core RGB and 979 cells retained',sum(len(native['sardinian_states'][sid]['rgb']) for sid in ADMIN_FILES)==5 and sum(native['sardinian_states'][sid]['cells'] for sid in ADMIN_FILES)==979)
    pol=policy();pms=prior.definitions('common/production_methods');groups=prior.definitions('common/production_method_groups');buildings=prior.definitions('common/buildings')
    pmgroups=[core.cw.scalar(n.value) for n in buildings['building_government_administration'].children('production_method_groups')[0].children()]
    for key in PMS:
        ck('Effective PM exists '+key,key in pms);node=pms[key]
        values=lambda f:{core.cw.scalar(n.value) for n in node.children(f)[0].children()} if node.children(f) else set()
        ck('PM compatible with SAR laws and technologies '+key,(not values('unlocking_laws') or bool(values('unlocking_laws')&set(pol['laws'].values()))) and not values('disallowing_laws')&set(pol['laws'].values()) and values('unlocking_technologies')<=set(pol['technologies']))
        ck('One compatible group '+key,len([g for g in pmgroups if key in {core.cw.scalar(n.value) for n in groups[g].children('production_methods')[0].children()}])==1)
    ck('One method per building group',len(PMS)==len(pmgroups))
    ck('Monarchy retained','law_monarchy' in pol['laws'].values())
    t=next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']==prior.TASK)
    ck('Three Italian human receipts remain bounded under regional block',rm.partial_runtime_evidence(t) and t['status']=='BLOCKED' and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),b['roadmap']))
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    old_changes=[p for p,h in b['report_hashes'].items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    ck('All older report evidence and attestations retained',not old_changes,old_changes)
    tool_changes=[p for p,h in b['tool_hashes'].items() if p!='tools/serg_sc4_savoy_nice.py' and sha(ROOT/p)!=h]
    ck('Existing tools and tests retained',not tool_changes,tool_changes)
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index retained',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    v=dict(task_ids=[TASK],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False,regional_status='BLOCKED',points_awarded=0)
    dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current))
    dump('FILES_MODIFIED.json',dict(runtime_files_written_by_this_pass=delta,existing_runtime_files_written_by_this_pass=[],sha256={p:current[p] for p in delta},baseline_count=len(b['hashes']),current_count=len(current),all_existing_runtime_files_preserved=all(current.get(p)==h for p,h in b['hashes'].items())))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']

def tests():
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc','test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia','test_serg_sc2_inner_austria','test_serg_sc2_anterior_austria','test_serg_sc4_italian_states','test_serg_sc4_savoy_nice']
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    for label,modules in [('TESTS',names),('SCOPED_TESTS',names[-8:])]:
        stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
        unexplained=[f for f in failures if f['id'] not in inherited]
        dump(label+'.json',dict(task_ids=[TASK],status='PASS' if not failures else 'INHERITED_FAILURES_ONLY' if not unexplained else 'FAIL',total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,'unexplained',len(unexplained),flush=True)
        assert not unexplained,unexplained
        assert {f['id'] for f in failures}==(inherited if label=='TESTS' else set())
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),unexplained_failures=[],old_tests_not_modified=True,automated_engine_test=False,explanation='Three old assertions expect former registry tails; actual cumulative Salzburg tail passes. One initial no-edit check is skipped.'))

def tracking():
    v=load(OUT/'VALIDATION.json');tested=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert v['passed']==v['total'] and not v['failed'] and not tested['unexplained_failures'] and not scoped['failed']
    assert (OUT/'REPORT.md').is_file()
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==load(OUT/'BASELINE.json')['roadmap'],'Concurrent tracker update requires reconciliation'
    assert state['events'][-1]['id']=='SERG-RM-0018' and rm.progress(state)['next_task']==TASK
    t=next(t for t in state['tasks'] if t['id']==TASK)
    implementation=load(OUT/'IMPLEMENTATION.json');implementation['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    for sub in implementation['sub_lots']:sub['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    dump('IMPLEMENTATION.json',implementation)
    block='P0 : correspondance des limites de 1754/1760 aux RGB savoyards et niçois non homologuée, notamment franges genevoises et Haut-Var; droits continentaux d’investiture/vicariat à distinguer des restitutions automatiques du modèle impérial. Absence actuelle de droits Savoie/Nice non approuvée définitivement; aucune inclusion de toute SAR ni exclusion fondée sur son titre royal. Confronter cartes 1772 et plans de limitation, puis pièces 1773–1774 référencées ou arbitrage explicite pour une extension B bornée du registre. Les deux administrations locales constituent une correction indépendante, pas une clôture territoriale ou constitutionnelle.'
    t.update(status='BLOCKED',blocking_reason=block,installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=implementation['sub_lots'],
        installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',
            scope='SN-I-SAV and SN-I-NIC only: one public SAR administration per existing subdivision. No territorial, population, diplomatic or imperial-registry change.'),
        decision=None,residual_uncertainty=block+' Les deux sous-lots B attendent leur validation en jeu; aucun recensement historique certifié.',
        current_delivery_note='Audit Savoie–Nice et interfaces de 1776 livré; deux administrations publiques SAR installées : SN-I-SAV en Savoie et SN-I-NIC dans la seule portion SAR de Provence/Nice. Cinq RGB/979 cellules et 499980 habitants initiaux conservés; aucun fichier fonctionnel préexistant réécrit, aucun droit impérial modifié. Limites et traduction des droits d’investiture/vicariat encore BLOCKED P0; deux installations IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION, aucun reçu humain ni point. Trois administrations italiennes explicitement validées dans leur seul périmètre; leur blocage juridique demeure. Protocole joueur livré, fiefs ligures candidate indépendante non commencée.')
    t['historical_sources'].append(PREFIX+'SOURCES.md:1')
    t['identified_problem'].append('Offices publics savoyards et niçois attestés mais aucune administration locale initiale dans ces deux subdivisions; corrigé par deux niveaux B indépendants. Registre SAR limité au Piémont; qualification des droits continentaux et limites datées à poursuivre sans étendre automatiquement le titre royal.')
    t['delivered_scope']=dict(classification='B_ADMINISTRATIVE_APPROXIMATION',sub_lots=list(SUB_IDS.values()),native_audited_rgb=5,native_audited_cells=979,audited_population=499980,territory_changed=False,population_changed=False,registry_changed=False,cadastral_validation=False,regional_acceptance_complete=False)
    state['mission_status']='SC4_SAVOY_NICE_PARTIAL_INSTALLATION_AWAITING_USER_TERRITORIAL_LEGAL_BLOCK'
    candidate=rm.progress(state)['next_task'];assert candidate=='SC4-LIGURIAN-FIEFS'
    note=f'Une seule nouvelle tâche P0 : SC4-SAVOY-NICE, sélection confirmée après reçu italien et validateur. Frontières 1754/1760, offices locaux et droits impériaux étudiés; deux niveaux administratifs publics SAR B installés séparément, sans frontière arbitraire ni changement de pacte. Cinq RGB/979 cellules, 499980 habitants, tous bâtiments antérieurs, souverain, capitale, gouvernement, unités et 574 droits conservés. Tâche globale BLOCKED pour correspondance frontalière et traduction des droits d’investiture/vicariat; absence actuelle non approuvée définitivement. Deux installations IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION, aucun reçu humain ni point. Statique {v["passed"]}/{v["total"]}; suite cumulative {tested["passed"]}/{tested["total"]}, trois assertions héritées et une exclusion; ciblée {scoped["passed"]}/{scoped["total"]}, une exclusion, aucun échec inexpliqué. Tous fichiers fonctionnels préexistants et travaux concurrents conservés. Trois administrations italiennes PASS limité, tâche italienne BLOCKED. Progression 82/235=34,89 % avant/après, périmètre 1.0.0 inchangé. Prochaine action joueur : SN-I-SAV/SN-I-NIC; candidate SC4-LIGURIAN-FIEFS identifiée sans commencement. Innviertel, Hohenberg/Fricktal/chantier naval, droits italiens et Teschen restent distincts. Aucun Git ou vanilla écrit.'
    state['events'].append(dict(id='SERG-RM-0019',date='2026-10-23',kind='PARTIAL_IMPLEMENTATION_WITH_TERRITORIAL_LEGAL_BLOCK',scope_version=state['scope_version'],source=PREFIX+'AUTHORIZATION.md',
        changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=note,
        evidence=[PREFIX+n for n in ['REPORT.md','SOURCES.md','SECTOR_AUDIT.md','NATIVE_INVENTORY.json','RGB_BEFORE_AFTER.csv','IMPLEMENTATION.json','VALIDATION.json','TESTS.json','SCOPED_TESTS.json','PLAYER_TEST_PROTOCOL.md']]))
    assert [x for x in state['tasks'] if x['id']!=TASK]==[x for x in original['tasks'] if x['id']!=TASK]
    assert state['events'][:-1]==original['events'] and not rm.structural_errors(state),rm.structural_errors(state)
    after=rm.progress(state)
    assert (after['earned_weight'],after['total_weight'],after['percent'],after['qualified_tasks'],after['next_task'])==(82,235,'34.89',24,candidate)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked['errors']
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged_since_italian_acceptance=True,previous_18_events_unchanged=True,scope_version_unchanged=True,weights_and_denominator_unchanged=True,qualified_tasks=24,earned_weight=82,total_weight=235,percent='34.89',new_runtime_receipts=0,task_status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',next_candidate=candidate,next_candidate_started=False))
    print('Tracker PASS; 82/235=34.89%; two pending administrations; next '+candidate+' not started',flush=True)

def final_tests():
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_serg_closure_roadmap','test_serg_sc4_italian_states','test_serg_sc4_savoy_nice']))
    (OUT/'FINAL_TESTS.log').write_text(stream.getvalue(),encoding='utf8')
    failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
    dump('FINAL_TESTS.json',dict(task_ids=[TASK],status='PASS' if not failures else 'FAIL',total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],automated_engine_test=False))
    print('Final tests',result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,failures,flush=True)
    assert not failures

def finalize():
    # Retain the first diagnostic: its classifier assumed exit 1, whereas this
    # Git returns 2 for the four known whitespace findings. No game fix follows.
    for name in ['FINAL_CHECKS','DIFF_CHECK']:
        p=OUT/(name+'.json');archive=OUT/(name+'_ATTEMPT_1.json')
        if p.exists() and load(p)['status']=='FAIL' and not archive.exists():archive.write_bytes(p.read_bytes())
    b=load(OUT/'BASELINE.json');current=prior.runtime_hashes();state=load(rm.OUT/'ROADMAP_STATE.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    expected=load(OUT/'SESSION_AFTER_STATIC.json')['hashes']
    ck('Runtime unchanged since successful static validation',current==expected)
    ck('All 2409 previous runtime files retained',len(b['hashes'])==2409 and all(current.get(p)==h for p,h in b['hashes'].items()))
    ck('Only the two documented administration files added',set(current)-set(b['hashes'])==set(ADMIN_FILES.values()) and len(current)==2411)
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    old=load(prior.OUT/'BASELINE.json')['report_hashes']
    combined=dict(old);combined.update(b['report_hashes'])
    changed=[p for p,h in combined.items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    ck('All prior map and SERG evidence retained',not changed,changed)
    ck('All 18 previous events retained',state['events'][:-1]==b['roadmap']['events'])
    ck('Other 80 task records retained', [x for x in state['tasks'] if x['id']!=TASK]==[x for x in b['roadmap']['tasks'] if x['id']!=TASK])
    ck('24 acquired tasks still qualified',sum(rm.qualifications(state).values())==24)
    ck('Italian partial receipt remains valid without global credit',rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']==prior.TASK)))
    t=next(t for t in state['tasks'] if t['id']==TASK)
    ck('Two installations pending; no fake human attestation',t['status']=='BLOCKED' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['runtime_validation']['attestation'] is None and all(s['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' for s in t['installed_sub_lots']))
    ck('Progress and next candidate correct',rm.progress(state)['percent']=='34.89' and rm.progress(state)['earned_weight']==82 and rm.progress(state)['next_task']=='SC4-LIGURIAN-FIEFS')
    ck('Next task not started',next(t for t in state['tasks'] if t['id']=='SC4-LIGURIAN-FIEFS')['status']=='NOT_STARTED')
    ck('Runtime protocol present',(OUT/'PLAYER_TEST_PROTOCOL.md').is_file())
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    import re
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,encoding='utf8',capture_output=True)
    findings=[dict(file=m.group(1),line=int(m.group(2)),message=m.group(3)) for m in re.finditer(r'^([^:\r\n]+):(\d+): (.+)$',diff.stdout,re.M)]
    inherited=all(f['file']=='common/history/pops/00_west_europe.txt' and f['message']=='trailing whitespace.' and current[f['file']]==b['hashes'][f['file']] for f in findings)
    diff_ok=diff.returncode==0 or diff.returncode in {1,2} and len(findings)==4 and inherited and {f['line'] for f in findings}=={2983,2999,3015,3031}
    dump('DIFF_CHECK.json',dict(task_ids=[TASK],exit_code=diff.returncode,status='INHERITED_WHITESPACE_ONLY' if findings and diff_ok else 'PASS' if diff_ok else 'FAIL',findings=findings,existing_file_byte_identical=inherited,stdout=diff.stdout,stderr=diff.stderr,files_not_rewritten=True))
    ck('Diff whitespace findings are inherited in unchanged file',diff_ok,findings)
    checked=rm.check();ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    dump('FINAL_CHECKS.json',dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,prior_proof_files_checked=len(combined)-len(canonical&combined.keys()),automated_engine_test=False))
    dump('SESSION_AFTER.json',dict(hashes=current,git_head=git('rev-parse','HEAD'),git_branch=git('branch','--show-current'),git_index_sha256=sha(ROOT/'.git/index'),progress=rm.progress(state)))
    dump('TRACKER_VALIDATION_FINAL.json',checked)
    assert all(c['passed'] for c in checks),checks
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']
    files += [p for p in prior.OUT.glob('*2026_10_23*') if p.is_file()]
    files += [ROOT/p for p in ADMIN_FILES.values()]
    files += [ROOT/'tools'/n for n in ['serg_sc4_savoy_nice.py','test_serg_sc4_savoy_nice.py','serg_closure_accept_italian_states.py']]
    files += [rm.OUT/n for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json','CLOSURE_CHECKLIST.md','DEFERRED_P2.md']]
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK],files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(files))},automated_engine_test=False))
    print('Final checks',len(checks),'/',len(checks),'prior proof files',len(combined),flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
