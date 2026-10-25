"""Existing Italian polities: bounded institutional corrections and honest regional blockers."""
import collections as C
import contextlib
import io
import json
import os
import subprocess
import sys
import unittest
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc2_anterior_austria as prior

os.environ['GIT_OPTIONAL_LOCKS']='0'

ROOT=prior.ROOT
rm=prior.rm
core=prior.core
reg=prior.reg
sha=prior.sha
runtime_hashes=prior.runtime_hashes
TASK='SC4-EXISTING-ITALIAN-STATES'
OUT=rm.OUT/TASK
TAGS={'MOD','PAR','TUS','LUC'}
ADMIN_TAGS={'MOD','PAR','LUC'}
ADMIN_FILES={tag:'common/history/buildings/1776_sc4_'+tag.lower()+'_administration.txt' for tag in ADMIN_TAGS}
PMS=prior.prior.PMS


def load(p):return rm.load_json(p)
def dump(name,obj):rm.write_json(OUT/name,obj)


def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']};rights={r['rgb']:r for r in b['registry']}
    rows=[]
    for rgb,(sid,tag) in sorted(owners.items()):
        if tag not in TAGS and sid not in {'STATE_EMILIA','STATE_TUSCANY','STATE_ROMAGNA','STATE_LOMBARDY','STATE_VENETIA','STATE_PIEDMONT'}:continue
        y,x=np.where(a==int(rgb[1:],16));neighbors=C.Counter()
        for yy,xx in zip(y,x):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                k='x'+format(int(a[yy+dy,xx+dx]),'06X')
                if k!=rgb:neighbors[k]+=1
        rows.append(dict(rgb=rgb,state_before=sid,state_after=sid,owner_before=tag,owner_after=tag,
            cells_before=len(x),cells_after=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())],
            centroid=[float(x.mean()),float(y.mean())],registry=rights.get(rgb),
            scope='EXISTING_POLITY_AUDIT' if tag in TAGS else 'NEIGHBOR_CONTEXT_ONLY',
            neighbors=[dict(rgb=k,state=owners.get(k,[inv['geometry'].get(k),''])[0],owner=owners.get(k,['',''])[1],edges=v) for k,v in sorted(neighbors.items())]))
    native=[r for r in rows if r['owner_before'] in TAGS]
    for i,r in enumerate(native,1):r['map_number']=i
    summary={tag:dict(rgb=len([r for r in native if r['owner_before']==tag]),
        cells=sum(r['cells_before'] for r in native if r['owner_before']==tag),
        population=sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag),
        buildings=[r for r in inv['buildings'] if r['key'][1]==tag],units=[r for r in inv['units'] if r['key'][0]==tag],
        registered=[r for r in b['registry'] if r['beneficiary']==tag]) for tag in sorted(TAGS)}
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,countries=summary,
        native_audited_rgb=len(native),native_audited_cells=sum(r['cells_before'] for r in native),territory_changed=False,cadastral_precision=False))
    x0,y0,x1,y1,scale=4290,955,4420,1090,6
    im=Image.new('RGB',((x1-x0)*scale+100,(y1-y0)*scale+95),'#faf8ef');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    colors={'MOD':'#eecc79','PAR':'#afc78d','TUS':'#b5c6dd','LUC':'#d7abd5','AUS':'#d8c9af','PAP':'#edd7bc','VEN':'#a7d5d2','SAR':'#cbcdcd','GEN':'#edb3a0'}
    for y in range(y0,y1):
        for x in range(x0,x1):
            rgb='x'+format(int(a[y,x]),'06X');tag=owners.get(rgb,['',''])[1];u,v=45+(x-x0)*scale,40+(y-y0)*scale
            d.rectangle((u,v,u+scale,v+scale),fill=colors.get(tag,'#e3e1db'))
            if a[y,x]!=a[y,x-1]:d.line((u,v,u,v+scale),fill='#8d8b86')
            if a[y,x]!=a[y-1,x]:d.line((u,v,u+scale,v),fill='#8d8b86')
    for r in native:
        x,y=r['centroid'];d.text((45+(x-x0)*scale,40+(y-y0)*scale),str(r['map_number'])+' '+r['owner_before'],font=font,fill='black',stroke_width=1,stroke_fill='white')
    d.text((10,8),'SC4 : propriétaires natifs, numéros RGB de l’inventaire; aucune frontière historique superposée',font=font,fill='black')
    d.text((10,im.height-35),'Ocre MOD; vert PAR; bleu TUS; violet LUC. Voisins AUS/PAP/VEN/SAR/GEN conservés.',font=font,fill='black')
    d.text((10,im.height-17),'Un pays présent au registre n’est pas une preuve d’investiture pour chacune de ses possessions.',font=font,fill='black')
    im.save(OUT/'NATIVE_READING.png')
    print(json.dumps({tag:{k:v for k,v in data.items() if k in {'rgb','cells','population'}} for tag,data in summary.items()}),flush=True)


def expected_admin(tag):
    assert tag in ADMIN_TAGS
    label={'MOD':'the ducal government at Modena','PAR':'the ducal government at Parma','LUC':'the oligarchic republican offices at Lucca'}[tag]
    return prior.expected_admin('STATE_BADEN').replace(prior.TASK,TASK).replace('the Freiburg foreland government',label).replace(
        's:STATE_BADEN','s:STATE_EMILIA').replace('region_state:AUS','region_state:'+tag).replace('"c:AUS"','"c:'+tag+'"').replace(
        '# Regional aggregate; distinct duchies and offices are not legally merged.',
        '# Capacity abstraction only; no territorial or constitutional change.')


def admin_contract(raw,tag):
    assert [core.qa.signature(n) for n in core.cw.parse(raw)]==[
        core.qa.signature(n) for n in core.cw.parse(expected_admin(tag))], 'Out-of-scope government addition'
    return True


def install():
    b=load(OUT/'BASELINE.json');assert load(rm.OUT/'ROADMAP_STATE.json')==b['roadmap']
    assert rm.progress(b['roadmap'])['next_task']==TASK
    assert all((OUT/n).is_file() for n in ['AUTHORIZATION.md','SOURCES.md','SECTOR_AUDIT.md'])
    assert runtime_hashes()==b['hashes'], 'Concurrent runtime change requires review'
    assert all(not (ROOT/p).exists() for p in ADMIN_FILES.values())
    for tag,p in sorted(ADMIN_FILES.items()):
        assert not any(r['key'][1]==tag and 'building_government_administration' in r['key'][2] for r in b['inventory']['buildings'])
        raw=expected_admin(tag);admin_contract(raw,tag)
        with (ROOT/p).open('xb') as f:f.write(raw.encode('utf8'))
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_PENDING_STATIC_CHECKS',
        sub_lots=[dict(id='IT-I-'+tag,tag=tag,state='STATE_EMILIA',file=p,building='building_government_administration',
            levels_before=0,levels_after=1,owner='c:'+tag,production_methods=PMS) for tag,p in sorted(ADMIN_FILES.items())],
        territory_changed=False,population_changed=False,diplomacy_changed=False,imperial_membership_changed=False,registry_changed=False,
        automated_engine_test=False,historical_staff_count_claim=False))
    print('Three independent initial public administrations installed',flush=True)


def definitions(folder):
    return {n.key:n for p in core.qa.effective(ROOT,core.qa.GAME,folder) for n in core.cw.parse(p.read_text(encoding='utf-8-sig'))}


def policy(tag,effects,laws):
    paths={'MOD':'mod - modena.txt','PAR':'par - parma.txt','LUC':'luc - lucca.txt','TUS':'tus - tuscany.txt'}
    country=core.cw.parse((ROOT/'common/history/countries'/paths[tag]).read_text(encoding='utf-8-sig'))[0].children()[0]
    selected={}
    def apply(key):
        value=key.removeprefix('law_type:');assert value in laws
        group=core.cw.scalar(laws[value].one('group'));selected[group]=value
    for n in country.children():
        if n.key=='effect_starting_politics_reactionary':
            assert core.cw.scalar(n.value)=='yes'
            for e in effects[n.key].children():
                if e.key=='activate_law':apply(core.cw.scalar(e.value))
                elif e.key=='else':
                    # All four audited polities are Catholic; select the non-Islamic branch.
                    for law in e.children('activate_law'):apply(core.cw.scalar(law.value))
        elif n.key=='activate_law':apply(core.cw.scalar(n.value))
    return dict(laws=selected,technologies=[core.cw.scalar(n.value) for n in country.children('add_technology_researched')],
        basis='Effective reactionary setup; direct laws in file order, including republican Lucca overrides; Catholic branch only.')


def validate():
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for field in inv:
        if field not in {'buildings','building_levels_written'}:ck('World inventory retained: '+field,inv[field]==b['inventory'][field])
    expected=core.qa.counter(b['inventory']['buildings'])
    for tag,p in sorted(ADMIN_FILES.items()):
        raw=(ROOT/p).read_text(encoding='utf8');ck('Exact independent administration: '+tag,admin_contract(raw,tag))
        node=core.region(raw,'STATE_EMILIA',tag).children('create_building')[0]
        expected[('STATE_EMILIA',tag,core.qa.signature(node))]+=1
    ck('Exactly three public administrations, all other building payloads retained',core.qa.counter(inv['buildings'])==expected)
    levels=core.qa.counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=3
    ck('Only global written capacity delta: three administrative levels',core.qa.counter(inv['building_levels_written'])==levels)
    current=runtime_hashes();delta=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    ck('Exactly three new runtime files; no shared runtime file edited',set(delta)==set(ADMIN_FILES.values()),delta)
    ck('Every existing runtime file byte-identical',all(current.get(p)==h for p,h in b['hashes'].items()))
    ck('Bitmap and province-terrain data retained',all(current[p]==b['hashes'][p] for p in ['map_data/provinces.png','map_data/province_terrains.txt']))
    ck('All 574 imperial registry entries retained',len(b['registry'])==574 and load(reg.active_registry_path())==b['registry'])
    ck('Approved cumulative Salzburg layer accepted',reg.approved_lot_dirs()[-1]==prior.prior.shared.prior.prior.OUT)
    native=load(OUT/'NATIVE_INVENTORY.json')
    ck('Eleven native RGB / 2410 cells inspected and retained',(native['native_audited_rgb'],native['native_audited_cells'])==(11,2410))
    for tag,total in [('MOD',505752),('PAR',368163),('TUS',1273269),('LUC',84558)]:
        ck('Population retained: '+tag,sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag)==total)
    ck('World population retained: 834926252',sum(r['count'] for r in inv['pops'])==834926252)
    for r in native['provinces']:
        if r['scope']!='EXISTING_POLITY_AUDIT':continue
        ck('Exact native owner retained: '+r['rgb'],[x for x in inv['owners'] if x['key'][0]==r['rgb']]==[dict(key=[r['rgb'],r['state_before'],r['owner_before']],count=1)])
    ck('No new duplicate RGB or invalid reference',inv['duplicates']==b['inventory']['duplicates'] and inv['errors']==b['inventory']['errors'])
    ck('Inherited diagnostic debt exactly 44 duplicates / 12 references',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    state=load(rm.OUT/'ROADMAP_STATE.json');qualified=rm.qualifications(state)
    ck('All 24 acquired tasks remain qualified',sum(qualified.values())==24 and all(qualified[k] for k,v in rm.qualifications(b['roadmap']).items() if v))
    anterior=next(t for t in state['tasks'] if t['id']==prior.TASK)
    ck('Anterior regional block retained and partial receipt qualified',anterior['status']=='BLOCKED' and rm.partial_runtime_evidence(anterior))
    ck('Partial receipt cannot award regional closure credit',not rm.terminal_evidence(dict(anterior,status='PASS_RUNTIME_USER_VALIDATED'),state))
    ck('Innviertel remains blocked and Teschen independent',next(t for t in state['tasks'] if t['id']=='SC2-AUSTRIA')['status']=='BLOCKED' and next(t for t in state['tasks'] if t['id']=='SC2-TESCHEN')['status']=='NOT_STARTED')
    ck('All protected previous reports and receipts retained',all(sha(ROOT/p)==h for p,h in b['report_hashes'].items() if (ROOT/p).parent!=rm.OUT))
    ck('Every older tool/test retained',all(sha(ROOT/p)==h for p,h in b['tool_hashes'].items()))
    pms=definitions('common/production_methods');groups=definitions('common/production_method_groups');buildings=definitions('common/buildings');laws=definitions('common/laws');effects=definitions('common/scripted_effects')
    policy_rows={tag:policy(tag,effects,laws) for tag in sorted(TAGS)};dump('INITIAL_POLICIES.json',policy_rows)
    pmgroups=[core.cw.scalar(n.value) for n in buildings['building_government_administration'].children('production_method_groups')[0].children()]
    for tag in sorted(ADMIN_TAGS):
        active=set(policy_rows[tag]['laws'].values());tech=set(policy_rows[tag]['technologies'])
        for key in PMS:
            ck('Effective PM exists: '+tag+'/'+key,key in pms)
            node=pms[key];values=lambda f:{core.cw.scalar(n.value) for n in node.children(f)[0].children()} if node.children(f) else set()
            ck('PM available under effective initial policies: '+tag+'/'+key,
                (not values('unlocking_laws') or bool(values('unlocking_laws')&active)) and not values('disallowing_laws')&active and values('unlocking_technologies')<=tech)
            ck('PM has exactly one compatible group: '+tag+'/'+key,len([g for g in pmgroups if key in {core.cw.scalar(n.value) for n in groups[g].children('production_methods')[0].children()}])==1)
    ck('One selected PM per group',len(PMS)==len(pmgroups))
    ck('Lucca oligarchy and republic overrides retained',{'law_presidential_republic','law_oligarchy'}<=set(policy_rows['LUC']['laws'].values()) and 'law_monarchy' not in policy_rows['LUC']['laws'].values())
    ck('Lucca remains outside current registry pending legal representation',not any(r['beneficiary']=='LUC' for r in b['registry']) and 'LUC' not in reg.additional_members())
    ck('Git HEAD, branch and index retained',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==b['git_head'] and subprocess.check_output(['git','branch','--show-current'],text=True).strip()==b['git_branch'] and sha(ROOT/'.git/index')==b['git_index_sha256'])
    for r in load(OUT/'SOURCE_FILES.json'):ck('Reused source byte-identical: '+r['file'],sha(ROOT/r['file'])==r['sha256'])
    v=dict(task_ids=[TASK],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False,regional_status='BLOCKED',points_awarded=0)
    dump('VALIDATION.json',v);dump('FILES_MODIFIED.json',dict(runtime_files_written_by_this_pass=delta,existing_runtime_files_written_by_this_pass=[],sha256={p:current[p] for p in delta},all_existing_runtime_files_preserved=all(current.get(p)==h for p,h in b['hashes'].items()),baseline_count=len(b['hashes']),current_count=len(current)))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']


def tests():
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc','test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia','test_serg_sc2_inner_austria','test_serg_sc2_anterior_austria','test_serg_sc4_italian_states']
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    for label,modules in [('TESTS',names),('SCOPED_TESTS',names[-7:])]:
        stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors];unexplained=[f for f in failures if f['id'] not in inherited]
        dump(label+'.json',dict(task_ids=[TASK],status='PASS' if not failures else 'INHERITED_FAILURES_ONLY' if not unexplained else 'FAIL',total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,'unexplained',len(unexplained),flush=True)
        for f in unexplained:print(f['id'],f['traceback'],flush=True)
        assert not unexplained
        assert {f['id'] for f in failures}==(inherited if label=='TESTS' else set())
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),unexplained_failures=[],old_tests_not_modified=True,automated_engine_test=False,explanation='Three inherited tests assume obsolete final registry layers. The approved current Salzburg tail passes. One initialization-only preservation check is excluded. No failures hidden or old tests rewritten.'))


def tracking():
    import copy
    v=load(OUT/'VALIDATION.json');tests_result=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert v['total']==v['passed'] and not v['failed'] and not tests_result['unexplained_failures'] and not scoped['failed']
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==load(OUT/'BASELINE.json')['roadmap'], 'Concurrent tracker update requires reconciliation'
    t=next(t for t in state['tasks'] if t['id']==TASK)
    assert t['status']=='NOT_STARTED' and rm.progress(state)['next_task']==TASK
    p='docs/reports/map/SERG_CLOSURE/SC4-EXISTING-ITALIAN-STATES/'
    implementation=load(OUT/'IMPLEMENTATION.json');implementation['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    for sub in implementation['sub_lots']:sub['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    dump('IMPLEMENTATION.json',implementation)
    block='P0 : droits et obligations impériaux de Lucques à traduire dans le modèle constitutionnel sans confondre titre juridique, protection et appartenance effective; étendue des droits impériaux de PAR/Guastalla et nature du protectorat SPA/PAR non démontrées au 1er janvier 1776. Aucun ajout automatique de LUC au registre ni suppression non étayée du pacte espagnol. Arbitrage documenté fondé sur actes et pratique diplomatique requis; les limites internes aux grands RGB restent non homologuées.'
    t.update(status='BLOCKED',blocking_reason=block,installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=implementation['sub_lots'],
        installed_lots=['SERG_CLOSURE/SC4-EXISTING-ITALIAN-STATES'],implementation_report=[p+'REPORT.md'],static_tests=dict(status='PASS',evidence=[p+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,new_details_invented=False,protocol=p+'PLAYER_TEST_PROTOCOL.md',
            scope='IT-I-MOD, IT-I-PAR and IT-I-LUC only: one initial public administration level per existing country. No territorial closure, diplomatic or imperial-membership correction.'),
        decision=None,residual_uncertainty=block+' Les trois installations administratives B attendent leur test propre; populations conservées sans certification historique.',
        current_delivery_note='Audit des quatre TAG existants MOD/PAR/TUS/LUC et de leurs interfaces livré. Trois sous-lots administratifs B installés et IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION : un niveau public MOD, PAR et LUC dans leurs subdivisions d’Émilie; les deux niveaux TUS déjà présents sont conservés. Onze RGB/2410 cellules et 2231742 habitants initiaux conservés; aucun pays, territoire, pacte, titulaire, unité ou droit impérial changé. Tâche régionale BLOCKED sur la qualification juridique de Lucques et de Parme, aucun point ni reçu humain nouveau. Protocole joueur livré; Savoie/Nice candidate indépendante non commencée.')
    t['historical_sources'].append(p+'SOURCES.md:1')
    t['identified_problem'].append('Absence d’administration initiale dans MOD/PAR/LUC malgré leurs offices attestés; trois corrections installées. Distinction entre droits féodaux, influence dynastique et obligations impériales encore requise pour Lucques et Parme, sans modifier arbitrairement les liens existants.')
    t['delivered_scope']=dict(classification='B_ADMINISTRATIVE_APPROXIMATION',sub_lots=['IT-I-MOD','IT-I-PAR','IT-I-LUC'],native_audited_rgb=11,native_audited_cells=2410,
        audited_population=2231742,administration_countries_population=958473,territory_changed=False,population_changed=False,cadastral_validation=False,regional_acceptance_complete=False)
    state['mission_status']='SC4_ITALIAN_STATES_PARTIAL_INSTALLATION_AWAITING_USER_LEGAL_BLOCK'
    candidate=rm.progress(state)['next_task'];assert candidate=='SC4-SAVOY-NICE'
    note=f'Une seule nouvelle tâche P0 : SC4-EXISTING-ITALIAN-STATES. Audit des quatre pays existants et de leurs interfaces; trois administrations initiales publiques MOD/PAR/LUC installées séparément, deux niveaux TUS conservés. Onze RGB/2410 cellules, populations, titulaires, gouvernements, pactes, unités et 574 lignes du registre inchangés. Lucques : statut juridique impérial distinct des obligations du modèle commun; Parme : qualification des droits et du lien espagnol à documenter. Tâche régionale BLOCKED; trois installations IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION, aucun reçu humain ni point. {v["passed"]}/{v["total"]} contrôles statiques; suite cumulative {tests_result["passed"]}/{tests_result["total"]}, trois assertions héritées et une exclusion; suite ciblée {scoped["passed"]}/{scoped["total"]}, une exclusion; aucun échec inexpliqué. Tous les fichiers fonctionnels préexistants et les travaux concurrents conservés. Reçu AN-I-W/AN-I-A/AN-P-A reconnu sans clôture d’Autriche antérieure. 82/235=34,89 % maintenus. Prochaine action joueur : protocole italien; candidate P0 indépendante SC4-SAVOY-NICE, non commencée. Hohenberg/Fricktal, chantier naval, Innviertel et Teschen restent séparés. Aucun Git ni vanilla écrit.'
    state['events'].append(dict(id='SERG-RM-0017',date='2026-10-19',kind='PARTIAL_IMPLEMENTATION_WITH_LEGAL_BLOCK',scope_version=state['scope_version'],source=p+'AUTHORIZATION.md',
        changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=note,
        evidence=[p+n for n in ['REPORT.md','SOURCES.md','SECTOR_AUDIT.md','NATIVE_INVENTORY.json','RGB_BEFORE_AFTER.csv','IMPLEMENTATION.json','VALIDATION.json','TESTS.json','SCOPED_TESTS.json','PLAYER_TEST_PROTOCOL.md']]))
    assert [x for x in state['tasks'] if x['id']!=TASK]==[x for x in original['tasks'] if x['id']!=TASK]
    assert state['events'][:-1]==original['events']
    assert not rm.structural_errors(state),rm.structural_errors(state)
    after=rm.progress(state)
    assert (after['earned_weight'],after['total_weight'],after['percent'],after['qualified_tasks'],after['next_task'])==(82,235,'34.89',24,candidate)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked['errors']
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged_since_partial_acceptance=True,previous_16_events_unchanged=True,scope_version_unchanged=True,
        weights_and_denominator_unchanged=True,qualified_tasks=24,earned_weight=82,total_weight=235,percent='34.89',new_runtime_receipts=0,
        task_status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',next_candidate=candidate,next_candidate_started=False))
    print('Tracker PASS; 82/235=34.89%; regional block and three pending installations retained; Savoy/Nice not started',flush=True)


if __name__=='__main__':{'inventory':inventory,'install':install,'validate':validate,'tests':tests,'tracking':tracking}[sys.argv[1]]()
