"""Piombino/Elba: dated jurisdiction audit and native map evidence."""
import collections as C
import contextlib
import copy
import csv
import io
import json
import os
import re
import subprocess
import unittest
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc4_ligurian_fiefs as prior

os.environ['GIT_OPTIONAL_LOCKS']='0'
ROOT=prior.ROOT;rm=prior.rm;core=prior.core;reg=prior.reg;sha=prior.sha
TASK='SC4-PIOMBINO';OUT=rm.OUT/TASK;PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
def load(p):return rm.load_json(p)
def dump(n,o):rm.write_json(OUT/n,o)

def elba_component(rows):
    row=next(r for r in rows if r['rgb']=='x6A7662')
    assert row['owner_before']=='TUS' and row['state_before']=='STATE_TUSCANY'
    assert row['cells_before']==219 and sorted(c['cells'] for c in row['components'])==[54,165]
    island=next(c for c in row['components'] if c['cells']==54)
    assert island['bounds']==[4325,1060,4335,1068]
    assert len(island['pixels'])==54 and len({tuple(p) for p in island['pixels']})==54
    assert len(components(*zip(*island['pixels'])))==1
    return copy.deepcopy(island)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    state=load(rm.OUT/'ROADMAP_STATE.json')
    assert state['events'][-1]['id']=='SERG-RM-0022' and rm.progress(state)['next_task']==TASK and rm.check()['status']=='PASS'
    assert rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']==prior.TASK))
    b=load(prior.OUT/'ACCEPTANCE_SESSION_BEFORE_2026_10_23.json');assert prior.prior.prior.runtime_hashes()==b['hashes']
    b['roadmap']=state
    protected={p:sha(ROOT/p) for p in load(prior.OUT/'BASELINE.json')['report_hashes'] if (ROOT/p).is_file()}
    for p in rm.OUT.rglob('*'):
        if p.is_file() and OUT not in p.parents:protected[p.relative_to(ROOT).as_posix()]=sha(p)
    b['report_hashes']=protected;b['tool_hashes']={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py')}
    OUT.mkdir(exist_ok=True);dump('BASELINE.json',b)
    print('Piombino baseline: receipt valid, selected P0, 82/235',flush=True)

def components(xs,ys):
    todo=set(zip(map(int,xs),map(int,ys)));out=[]
    while todo:
        p=todo.pop();stack=[p];area=[p]
        while stack:
            x,y=stack.pop()
            for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if n in todo:todo.remove(n);stack.append(n);area.append(n)
        ax,ay=zip(*area);out.append(dict(cells=len(area),bounds=[min(ax),min(ay),max(ax),max(ay)],centroid=[sum(ax)/len(ax),sum(ay)/len(ay)],pixels=[list(p) for p in sorted(area)]))
    return sorted(out,key=lambda r:-r['cells'])

def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in inv['owners']};rows=[]
    for rgb,(sid,tag) in sorted(owners.items()):
        if sid not in {'STATE_TUSCANY','STATE_CORSICA','STATE_EMILIA','STATE_ROMAGNA','STATE_LAZIO','STATE_SARDINIA'}:continue
        y,x=np.where(a==int(rgb[1:],16));neighbors=C.Counter()
        for yy,xx in zip(y,x):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                n='x'+format(int(a[yy+dy,xx+dx]),'06X')
                if n!=rgb:neighbors[n]+=1
        rows.append(dict(rgb=rgb,state_before=sid,state_after=sid,owner_before=tag,owner_after=tag,cells_before=len(x),cells_after=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())],centroid=[float(x.mean()),float(y.mean())],components=components(x,y),registry=next((r for r in b['registry'] if r['rgb']==rgb),None),neighbors=[dict(rgb=k,state=owners.get(k,['',''])[0],owner=owners.get(k,['',''])[1],edges=v) for k,v in sorted(neighbors.items())]))
    tags=['TUS','SIC','MOD','PAR','LUC','PAP','FRA','SAR'];countries={tag:dict(definition=inv['countries'].get(tag),pops=[r for r in inv['regional_pop'] if r['key'][1]==tag],buildings=[r for r in inv['buildings'] if r['key'][1]==tag],units=[r for r in inv['units'] if r['key'][0]==tag],registry=[r for r in b['registry'] if r['beneficiary']==tag]) for tag in tags}
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,countries=countries,other_tags_are_context_only=True))
    print(json.dumps([dict(rgb=r['rgb'],cells=r['cells_before'],components=[dict(cells=c['cells'],bounds=c['bounds']) for c in r['components']]) for r in rows if r['state_before']=='STATE_TUSCANY'],ensure_ascii=False),flush=True)
    x0,y0,x1,y1,scale=4280,1020,4390,1160,6
    im=Image.new('RGB',((x1-x0)*scale+80,(y1-y0)*scale+95),'#faf8ef');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    colors={'TUS':'#b9a2d2','SIC':'#cba591','PAP':'#dabbb7','LUC':'#e0c39d','MOD':'#bcd390','PAR':'#aec7a1','SAR':'#e6c36b','FRA':'#8fbcda','GEN':'#cca6bb'}
    for yy in range(y0,y1):
        for xx in range(x0,x1):
            rgb='x'+format(int(a[yy,xx]),'06X');u,v=40+(xx-x0)*scale,30+(yy-y0)*scale
            d.rectangle((u,v,u+scale,v+scale),fill=colors.get(owners.get(rgb,['',''])[1],'#dcebf1'))
            if rgb in owners:
                if a[yy,xx]!=a[yy,xx-1]:d.line((u,v,u,v+scale),fill='#777')
                if a[yy,xx]!=a[yy-1,xx]:d.line((u,v,u+scale,v),fill='#777')
    for n,r in enumerate([r for r in rows if r['state_before']=='STATE_TUSCANY'],1):
        r['map_number']=n
        for comp in r['components']:
            x,y=comp['centroid'];d.text((40+(x-x0)*scale,30+(y-y0)*scale),str(n),font=font,fill='black',stroke_width=1,stroke_fill='white')
    d.text((10,8),'Toscane et iles : proprietaires natifs, numeros = RGB toscans',font=font,fill='black')
    d.text((10,im.height-43),'Mauve TUS; ocre SAR; bleu FRA; rose PAP; brun SIC.',font=font,fill='black')
    d.text((10,im.height-23),'Bitmap natif seulement; aucun calage historique ou nouveau territoire.',font=font,fill='black')
    im.save(OUT/'NATIVE_READING.png');dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,countries=countries,other_tags_are_context_only=True))
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf8',newline='') as f:
        fields=['map_number','rgb','state_before','state_after','owner_before','owner_after','cells_before','cells_after'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r.get(k,'') for k in fields} for r in rows)

def context():
    d=load(OUT/'NATIVE_INVENTORY.json');elba=elba_component(d['provinces']);effects=prior.prior.prior.definitions('common/scripted_effects');laws=prior.prior.prior.definitions('common/laws')
    pol={tag:prior.initial_policy(tag,effects,laws) for tag in ['TUS','SIC','MOD','PAR','LUC','SAR']}
    refs=[]
    for folder in ['common/history/diplomacy','common/history/treaties','common/history/characters','common/history/power_blocs']:
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            raw=p.read_text(encoding='utf-8-sig');lines=raw.splitlines();indices=[n for n,line in enumerate(lines) if 'c:TUS' in line or 'c:SIC' in line]
            if indices:
                keep=sorted({j for n in indices for j in range(max(0,n-2),min(len(lines),n+15))})
                refs.append(dict(file=str(p),lines=[dict(line=j+1,text=lines[j]) for j in keep]))
    b=load(OUT/'BASELINE.json');dump('INITIAL_CONTEXT.json',dict(task_ids=[TASK],policies=pol,references=refs,piombino_tag_PIO_present='PIO' in b['inventory']['countries'],no_functional_write=True))
    dump('ELBA_NATIVE_EVIDENCE.json',dict(task_ids=[TASK],island_exists=True,shared_rgb='x6A7662',state='STATE_TUSCANY',owner='TUS',island=elba,mainland_cells_same_rgb=165,total_cells_shared_rgb=219,independent_province=False,historical_sovereignties_not_separated=True,read_only_evidence=True))
    # Diagrammatic enlargement of the actual cells; colors identify components,
    # not a proposal of new sovereignty or a reconstruction of a coastal survey.
    a=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};points={tuple(p) for p in elba['pixels']}
    x0,y0,x1,y1,scale=4321,1040,4365,1079,13
    im=Image.new('RGB',((x1-x0)*scale+60,(y1-y0)*scale+115),'#faf8ef');dr=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for y in range(y0,y1):
        for x in range(x0,x1):
            rgb='x'+format(int(a[y,x]),'06X');u,v=30+(x-x0)*scale,65+(y-y0)*scale
            fill='#e6bd68' if (x,y) in points else '#b6a0c8' if rgb=='x6A7662' else '#dbd3e5' if owners.get(rgb)=='TUS' else '#b5c9d4' if rgb in owners else '#e2eef2'
            dr.rectangle((u,v,u+scale,v+scale),fill=fill)
            if rgb in owners:
                if a[y,x]!=a[y,x-1]:dr.line((u,v,u,v+scale),fill='#858585')
                if a[y,x]!=a[y-1,x]:dr.line((u,v,u+scale,v),fill='#858585')
    dr.text((10,8),'Elbe existe : 54 cellules, actuellement TUS',font=font,fill='black')
    dr.text((10,30),'Ile ocre + continent violet = meme RGB x6A7662 (219 cellules)',font=font,fill='black')
    x,y=elba['centroid'];dr.text((30+(x-x0)*scale-28,65+(y-y0)*scale),'ELBE',font=font,fill='black',stroke_width=1,stroke_fill='white')
    dr.text((10,im.height-36),'Couleurs de lecture : aucune nouvelle souverainete installee.',font=font,fill='black')
    dr.text((10,im.height-16),'Contours natifs ; les trois juridictions de 1776 ne sont pas separees.',font=font,fill='black')
    im.save(OUT/'ELBA_DETAIL.png')

def validate():
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();current=prior.prior.prior.runtime_hashes();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for field in inv:ck('World inventory retained: '+field,inv[field]==b['inventory'][field])
    ck('All 2411 functional files byte-identical',current==b['hashes'] and len(current)==2411)
    ck('574 imperial rights retained',load(reg.active_registry_path())==b['registry'] and len(b['registry'])==574)
    ck('Cumulative Salzburg registry layer retained',reg.approved_lot_dirs()[-1].name=='SC1-SALZBURG')
    ck('Nine approved Piedmont rights only',reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}} and len([r for r in b['registry'] if r['beneficiary']=='SAR'])==9)
    native=load(OUT/'NATIVE_INVENTORY.json');island=elba_component(native['provinces'])
    row=next(r for r in native['provinces'] if r['rgb']=='x6A7662')
    ck('Shared Tuscan province comprises 54 island and 165 mainland cells',island['cells']==54 and row['cells_before']==219)
    a=core.packed(ROOT/'map_data/provinces.png');land={r['key'][0] for r in inv['owners']};coast=True
    ps={tuple(p) for p in island['pixels']}
    for x,y in ps:
        for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if (nx,ny) not in ps and 'x'+format(int(a[ny,nx]),'06X') in land:coast=False
    ck('Island component bounded by sea, not an arbitrary mainland rectangle',coast)
    ck('No new Piombino country created','PIO' not in inv['countries'])
    tus=[r for r in native['provinces'] if r['owner_before']=='TUS' and r['state_before']=='STATE_TUSCANY']
    ck('Six Tuscan RGB and 1321 cells retained',len(tus)==6 and sum(r['cells_before'] for r in tus)==1321)
    ck('TUS population 1273269 retained',sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='TUS')==1273269)
    ck('GEN accepted correction retained',(ROOT/prior.BUILDINGS).read_bytes()==prior.candidate((prior.OUT/'BUILDINGS_BEFORE.txt').read_bytes().decode('utf8')).encode('utf8'))
    for task in ['SC2-ANTERIOR-AUSTRIA','SC4-EXISTING-ITALIAN-STATES','SC4-SAVOY-NICE','SC4-LIGURIAN-FIEFS']:
        t=next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']==task)
        ck('Bounded prior human receipt '+task,rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),b['roadmap']))
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    old=[p for p,h in b['report_hashes'].items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    ck('All older evidence retained',not old,old)
    changed=[p for p,h in b['tool_hashes'].items() if p!='tools/serg_sc4_piombino.py' and sha(ROOT/p)!=h]
    ck('Older tools and tests retained',not changed,changed)
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    ck('Initial priority confirmed',rm.progress(b['roadmap'])['next_task']==TASK)
    ck('No historical-conservation approval or engine receipt invented',next(t for t in b['roadmap']['tasks'] if t['id']==TASK)['runtime_validation']['attestation'] is None)
    ck('Jurisdiction matrix and concrete B proposal present',all((OUT/n).is_file() for n in ['JURISDICTION_MATRIX.csv','B_PROPOSAL.md','PLAYER_TEST_PROTOCOL.md','SOURCES.md']))
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False,no_functional_changes=True,regional_status='BLOCKED',points_awarded=0)
    dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current));dump('FILES_MODIFIED.json',dict(task_ids=[TASK],runtime_files_written_by_this_pass=[],all_2411_existing_runtime_files_preserved=True))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']

def tests():
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    for label,names in [('TESTS',prior.MODULES+['test_serg_sc4_piombino']),('SCOPED_TESTS',prior.MODULES[-9:]+['test_serg_sc4_piombino'])]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8');failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
        unexplained=[f for f in failures if f['id'] not in inherited]
        dump(label+'.json',dict(task_ids=[TASK],status='PASS' if not failures else 'INHERITED_FAILURES_ONLY' if not unexplained else 'FAIL',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,'unexplained',len(unexplained),flush=True)
        assert not unexplained,unexplained
        assert {f['id'] for f in failures}==(inherited if label=='TESTS' else set())
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),old_tests_not_modified=True,unexplained_failures=[],automated_engine_test=False))

def tracking():
    v=load(OUT/'VALIDATION.json');tested=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert not v['failed'] and v['passed']==v['total'] and not tested['unexplained_failures'] and not scoped['failed']
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state);b=load(OUT/'BASELINE.json')
    assert state==b['roadmap'] and state['events'][-1]['id']=='SERG-RM-0022' and rm.progress(state)['next_task']==TASK,'Concurrent tracking update requires reconciliation'
    t=next(t for t in state['tasks'] if t['id']==TASK)
    block='P0 : Piombino absent comme principauté distincte et Elbe uniformément TUS malgré les ressorts princiers, toscan de Portoferraio et napolitain de Longone. Île native identifiée : 54 cellules de x6A7662, partagées avec 165 cellules continentales du même RGB ; ne transférer ni toute cette province ni toute l’île au prince. Attribution politique B des fragments continentaux/insulaires, population correspondante et articulation de l’investiture impériale avec le haut domaine napolitain encore insuffisamment établies. Proposition B1 ensemble continental/insulaire ou B2 noyau continental avec blocage insulaire, pièces et garanties documentées ; pas de cadastre parfait exigé, de bande arbitraire ou de frontière de 1801/1815. Aucune installation fonctionnelle, aucune conservation définitive approuvée, aucun point.'
    t.update(status='BLOCKED',blocking_reason=block,implementation_report=[PREFIX+'REPORT.md',PREFIX+'B_PROPOSAL.md'],
        static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope='No new functional installation in this audit; optional visual reconnaissance only. A future correction requires its own complete runtime protocol.',new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),
        decision=None,residual_uncertainty=block,
        current_delivery_note='Audit SC4-PIOMBINO livré sans correction fonctionnelle artificielle. Elbe existe : composante insulaire de 54 cellules TUS, même RGB x6A7662 que 165 cellules continentales ; pas une île à créer. Absence politique de Piombino et trois souverainetés insulaires distinguées ; Gaetano en 1776, succession Antonio seulement 1777. Sources, huit ensembles juridiques et proposition B bornée documentés ; géographie interne, population et liens supérieurs restent BLOCKED P0. Tous 2411 fichiers fonctionnels et 574 droits conservés, aucun reçu Piombino ni point. LF-GEN-ADM-PM désormais PASS limité, blocage ligure intact. Reconnaissance visuelle facultative, aucun nouveau mois moteur requis pour ce diagnostic. Candidate SC4-MASSA-CARRARA identifiée sans commencement.')
    t['historical_sources'].append(PREFIX+'SOURCES.md:1')
    t['identified_problem'].append('Principauté distincte de TUS omise ; Elbe présente mais regroupée au continent sous un seul RGB TUS, sans Portoferraio/Longone/domaine princier séparés. Absence de TAG ne signifie pas absence physique de l’île.')
    t['delivered_scope']=dict(classification='DATED_AUDIT_AND_B_PROPOSAL_NOT_INSTALLED',native_audited_tuscan_rgb=6,native_audited_tuscan_cells=1321,elba_native_cells=54,shared_rgb_cells=219,mainland_cells_same_rgb=165,audited_tuscan_population=1273269,no_functional_changes=True,territory_changed=False,population_changed=False,registry_changed=False,no_correction_required=False,retention_approved=False,regional_acceptance_complete=False)
    state['mission_status']='SC4_PIOMBINO_AUDIT_BLOCKED_READY_FOR_MASSA_CARRARA'
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC4-MASSA-CARRARA')
    note=f'Reçu humain LF-GEN-ADM-PM préalablement enregistré par SERG-RM-0022, sans clôture ligure. Une seule nouvelle étape P0 : SC4-PIOMBINO, admissibilité confirmée après validateur. Principat, Gaetano de 1776, Portoferraio TUS, Longone napolitain et droits impériaux/supérieurs étudiés ; île d’Elbe présente, 54 cellules TUS partagées avec 165 continentales dans x6A7662. Omission de souveraineté démontrée, mais découpe politique B, population et traduction des liens non suffisantes pour installation ; B1 ensemble princier ou B2 noyau continental documentés, pas de transfert arbitraire ni de conformité générale. Tâche BLOCKED P0, aucun fichier fonctionnel modifié, aucun reçu Piombino ou point. Statique {v["passed"]}/{v["total"]} ; cumulative {tested["passed"]}/{tested["total"]}, trois assertions héritées et une exclusion ; ciblée {scoped["passed"]}/{scoped["total"]}, une exclusion, aucun nouvel échec. Tous les 2411 fichiers fonctionnels, noyaux et travaux concurrents conservés ; 574 droits et neuf électeurs inchangés. Progression 82/235=34,89 % avant/après ; 81 tâches, périmètre 1.0.0 et poids inchangés. Reconnaissance visuelle facultative, aucun mois moteur requis pour ce diagnostic sans installation. SC4-MASSA-CARRARA prochaine candidate indépendante, laissée NOT_STARTED ; aucune deuxième tâche commencée. Autres blocages inchangés ; aucun Git ou vanilla écrit.'
    state['events'].append(dict(id='SERG-RM-0023',date='2026-10-23',kind='SCOPED_AUDIT_BLOCKED_NO_FUNCTIONAL_CHANGE',scope_version=state['scope_version'],source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=note,evidence=[PREFIX+n for n in ['REPORT.md','SOURCES.md','SECTOR_AUDIT.md','JURISDICTION_MATRIX.csv','B_PROPOSAL.md','ELBA_NATIVE_EVIDENCE.json','NATIVE_INVENTORY.json','RGB_BEFORE_AFTER.csv','VALIDATION.json','TESTS.json','SCOPED_TESTS.json','PLAYER_TEST_PROTOCOL.md']]))
    assert [t for t in state['tasks'] if t['id']!=TASK]==[t for t in original['tasks'] if t['id']!=TASK]
    assert state['events'][:-1]==original['events'] and not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked.get('errors')
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged_since_gen_acceptance=True,previous_22_events_unchanged=True,scope_version_unchanged=True,weights_and_denominator_unchanged=True,qualified_tasks=24,earned_weight=82,total_weight=235,percent='34.89',new_piombino_runtime_receipts=0,no_new_functional_installation=True,task_status='BLOCKED',next_candidate='SC4-MASSA-CARRARA',next_candidate_started=False))
    print('Tracker PASS; 82/235=34.89%; Piombino BLOCKED; Massa-Carrara not started',flush=True)

def final_tests():
    names=['test_serg_closure_roadmap','test_serg_sc4_italian_states','test_serg_sc4_savoy_nice','test_serg_sc4_ligurian_fiefs','test_serg_sc4_piombino']
    stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    (OUT/'FINAL_TESTS.log').write_text(stream.getvalue(),encoding='utf8');failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
    dump('FINAL_TESTS.json',dict(task_ids=[TASK],status='PASS' if not failures else 'FAIL',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],automated_engine_test=False))
    print('Final tests',r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,flush=True);assert not failures,failures

def finalize():
    b=load(OUT/'BASELINE.json');current=prior.prior.prior.runtime_hashes();state=load(rm.OUT/'ROADMAP_STATE.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    ck('All 2411 runtime files unchanged since capture and static check',len(current)==2411 and current==b['hashes']==load(OUT/'SESSION_AFTER_STATIC.json')['hashes'])
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    old=[p for p,h in b['report_hashes'].items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    ck('Every older proof and receipt retained',not old,old)
    changed=[p for p,h in b['tool_hashes'].items() if p!='tools/serg_sc4_piombino.py' and sha(ROOT/p)!=h]
    ck('All previous tools and tests retained',not changed,changed)
    ck('Previous 22 events unchanged',state['events'][:-1]==b['roadmap']['events'])
    ck('Other 80 task records unchanged',[t for t in state['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK])
    ck('24 previous tasks still qualified',sum(rm.qualifications(state).values())==24)
    t=next(t for t in state['tasks'] if t['id']==TASK)
    ck('Piombino P0 blocked without fictitious installation or receipt',t['status']=='BLOCKED' and t['priority']=='P0' and not t['installed_lots'] and t['runtime_validation']['attestation'] is None and t['delivered_scope']['no_functional_changes'] is True and t['decision'] is None)
    ck('GEN acceptance still scoped under regional block',rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']==prior.TASK)))
    p=rm.progress(state);ck('Scope weights and next candidate correct',(p['total_tasks'],p['total_weight'],p['earned_weight'],p['percent'],p['next_task'])==(81,235,82,'34.89','SC4-MASSA-CARRARA'))
    ck('Massa-Carrara remains unstarted',next(t for t in state['tasks'] if t['id']=='SC4-MASSA-CARRARA')['status']=='NOT_STARTED')
    ck('Elba evidence preserves 54+165 cells',elba_component(load(OUT/'NATIVE_INVENTORY.json')['provinces'])['cells']==54)
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch and index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,encoding='utf8',capture_output=True)
    findings=[dict(file=m.group(1),line=int(m.group(2)),message=m.group(3)) for m in re.finditer(r'^([^:\r\n]+):(\d+): (.+)$',diff.stdout,re.M)]
    inherited=all(f['file']=='common/history/pops/00_west_europe.txt' and f['message']=='trailing whitespace.' and current[f['file']]==b['hashes'][f['file']] for f in findings)
    ok=diff.returncode==0 or diff.returncode in {1,2} and len(findings)==4 and inherited and {f['line'] for f in findings}=={2983,2999,3015,3031}
    dump('DIFF_CHECK.json',dict(task_ids=[TASK],status='INHERITED_WHITESPACE_ONLY' if findings and ok else 'PASS' if ok else 'FAIL',exit_code=diff.returncode,findings=findings,stdout=diff.stdout,stderr=diff.stderr,existing_file_unchanged=inherited));ck('Only inherited whitespace findings',ok,findings)
    checked=rm.check();ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    ck('Static and cumulative/final evidence passes without new failures',not load(OUT/'VALIDATION.json')['failed'] and not load(OUT/'TESTS.json')['unexplained_failures'] and not load(OUT/'SCOPED_TESTS.json')['failed'] and not load(OUT/'FINAL_TESTS.json')['failed'])
    dump('FINAL_CHECKS.json',dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,prior_proof_files_checked=len(b['report_hashes'])-len(canonical&b['report_hashes'].keys()),automated_engine_test=False))
    dump('SESSION_AFTER.json',dict(hashes=current,git_head=git('rev-parse','HEAD'),git_branch=git('branch','--show-current'),git_index_sha256=sha(ROOT/'.git/index'),progress=p));dump('TRACKER_VALIDATION_FINAL.json',checked)
    assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']
    files += [p for p in prior.OUT.glob('*2026_10_23*') if p.is_file()]
    files += [ROOT/'tools'/n for n in ['serg_sc4_piombino.py','test_serg_sc4_piombino.py','serg_closure_accept_ligurian_fiefs.py']]
    files += [rm.OUT/n for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json','CLOSURE_CHECKLIST.md','DEFERRED_P2.md']]
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK],files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(files))},automated_engine_test=False,no_functional_installation=True))
    assert all(sha(ROOT/p)==h for p,h in load(OUT/'DELIVERY_MANIFEST.json')['files'].items())
    print('Final checks',len(checks),'/',len(checks),'previous proofs',len(b['report_hashes']),flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
