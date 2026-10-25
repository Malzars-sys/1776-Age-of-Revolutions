"""Ligurian jurisdictions: explicit native inventory and bounded corrections."""
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
from PIL import Image, ImageDraw, ImageFont
import serg_sc4_savoy_nice as prior

os.environ['GIT_OPTIONAL_LOCKS']='0'
ROOT=prior.ROOT
rm=prior.rm
core=prior.core
reg=prior.reg
sha=prior.sha
TASK='SC4-LIGURIAN-FIEFS'
OUT=rm.OUT/TASK
PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
BUILDINGS='common/history/buildings/01_south_europe.txt'
SUB='LF-GEN-ADM-PM'
OLD_PM='pm_horizontal_drawer_cabinets'
NEW_PM='pm_simple_organization'

def load(p):return rm.load_json(p)
def dump(name,obj):rm.write_json(OUT/name,obj)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    state=load(rm.OUT/'ROADMAP_STATE.json')
    assert state['events'][-1]['id']=='SERG-RM-0020' and rm.progress(state)['next_task']==TASK and rm.check()['status']=='PASS'
    assert rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']==prior.TASK))
    b=load(prior.OUT/'ACCEPTANCE_SESSION_BEFORE_2026_10_23.json')
    assert prior.prior.runtime_hashes()==b['hashes']
    b['roadmap']=state
    older=load(prior.prior.OUT/'BASELINE.json')['report_hashes']
    protected={p:sha(ROOT/p) for p in older if (ROOT/p).is_file()}
    for p in rm.OUT.rglob('*'):
        if p.is_file() and OUT not in p.parents:protected[p.relative_to(ROOT).as_posix()]=sha(p)
    b['report_hashes']=protected
    b['tool_hashes']={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py')}
    b['tracking_fix']=dict(file='tools/serg_closure_roadmap.py',before=b['roadmap_tool_sha_before'],after=sha(ROOT/'tools/serg_closure_roadmap.py'),reason='Render actual accepted partial-sub-lot count, including two Savoy-Nice administrations; no scoring or evidence rule changed.')
    OUT.mkdir(exist_ok=True);dump('BASELINE.json',b)
    print('Ligurian baseline captured; 82/235; receipt and priority confirmed',flush=True)

def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']};rights={r['rgb']:r for r in b['registry']}
    context={'STATE_PIEDMONT','STATE_LOMBARDY','STATE_EMILIA','STATE_TUSCANY','STATE_PROVENCE'};rows=[]
    for rgb,(sid,tag) in sorted(owners.items()):
        if sid not in context and tag!='GEN':continue
        y,x=np.where(a==int(rgb[1:],16));neighbors=C.Counter()
        for yy,xx in zip(y,x):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                k='x'+format(int(a[yy+dy,xx+dx]),'06X')
                if k!=rgb:neighbors[k]+=1
        rows.append(dict(rgb=rgb,state_before=sid,state_after=sid,owner_before=tag,owner_after=tag,cells_before=len(x),cells_after=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())],centroid=[float(x.mean()),float(y.mean())],registry=rights.get(rgb),neighbors=[dict(rgb=k,state=owners.get(k,[inv['geometry'].get(k),''])[0],owner=owners.get(k,['',''])[1],edges=v) for k,v in sorted(neighbors.items())]))
    tags=sorted({r['owner_before'] for r in rows})
    countries={tag:dict(rgb=[r['rgb'] for r in rows if r['owner_before']==tag],cells=sum(r['cells_before'] for r in rows if r['owner_before']==tag),
        population=sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag),pops=[r for r in inv['regional_pop'] if r['key'][1]==tag],
        buildings=[r for r in inv['buildings'] if r['key'][1]==tag],units=[r for r in inv['units'] if r['key'][0]==tag],definition=inv['countries'].get(tag),registry=[r for r in b['registry'] if r['beneficiary']==tag]) for tag in tags}
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],provinces=rows,countries=countries,core_tag='GEN',other_tags_are_context_only=True))
    gen=countries['GEN']
    print(json.dumps(dict(GEN={k:gen[k] for k in ['rgb','cells','population','buildings','units','definition','registry']},core_geometry=[r for r in rows if r['owner_before']=='GEN']),ensure_ascii=False),flush=True)

def illustrate():
    d=load(OUT/'NATIVE_INVENTORY.json');a=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in load(OUT/'BASELINE.json')['inventory']['owners']}
    x0,y0,x1,y1,scale=4260,987,4340,1047,10
    im=Image.new('RGB',((x1-x0)*scale+80,(y1-y0)*scale+110),'#faf8ef');draw=ImageDraw.Draw(im)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    colors={'SAR':'#e8c26f','GEN':'#d5b0c5','AUS':'#b6cde7','PAR':'#b8d09f','MOD':'#e5b19c','TUS':'#c3badb','LUC':'#c6bc9f'}
    for y in range(y0,y1):
        for x in range(x0,x1):
            rgb='x'+format(int(a[y,x]),'06X');u,v=40+(x-x0)*scale,40+(y-y0)*scale
            draw.rectangle((u,v,u+scale,v+scale),fill=colors.get(owners.get(rgb),'#eceae4'))
            if a[y,x]!=a[y,x-1]:draw.line((u,v,u,v+scale),fill='#77756f')
            if a[y,x]!=a[y-1,x]:draw.line((u,v,u+scale,v),fill='#77756f')
    for n,r in enumerate([r for r in d['provinces'] if r['owner_before']=='GEN'],1):
        r['map_number']=n;x,y=r['centroid'];draw.text((40+(x-x0)*scale,40+(y-y0)*scale),str(n),font=font,fill='black',stroke_width=1,stroke_fill='white')
    draw.text((10,9),'Ligurie : proprietaires natifs; numeros = trois RGB GEN',font=font,fill='black')
    draw.text((10,im.height-57),'Violet GEN; ocre SAR; bleu AUS; vert PAR; rose MOD; mauve TUS.',font=font,fill='black')
    draw.text((10,im.height-36),'Contours du jeu seulement; aucun calage historique ni limite cadastrale.',font=font,fill='black')
    draw.text((10,im.height-16),'Les petites juridictions historiques ne sont pas localisees par ces numeros.',font=font,fill='black')
    im.save(OUT/'NATIVE_READING.png')
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf8',newline='') as f:
        fields=['map_number','rgb','state_before','state_after','owner_before','owner_after','cells_before','cells_after']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        w.writerows({k:r.get(k,'') for k in fields} for r in d['provinces'])
    dump('NATIVE_INVENTORY.json',d)

def initial_policy(tag,effects,laws):
    paths=list((ROOT/'common/history/countries').glob(tag.lower()+' - *.txt'));assert len(paths)==1,(tag,paths)
    country=core.cw.parse(paths[0].read_text(encoding='utf-8-sig'))[0].children()[0];selected={}
    def apply(key):
        value=key.removeprefix('law_type:')
        node=laws.get(value) or laws.get('INJECT_OR_CREATE:'+value)
        assert node is not None,value
        selected[core.cw.scalar(node.one('group'))]=value
    for n in country.children():
        if n.key=='effect_starting_politics_reactionary':
            assert core.cw.scalar(n.value)=='yes'
            for e in effects[n.key].children():
                if e.key=='activate_law':apply(core.cw.scalar(e.value))
                elif e.key=='else':
                    for law in e.children('activate_law'):apply(core.cw.scalar(law.value))
        elif n.key=='activate_law':apply(core.cw.scalar(n.value))
    return dict(laws=selected,technologies=[core.cw.scalar(n.value) for n in country.children('add_technology_researched')],basis='Catholic branch of effective reactionary setup, then direct overrides in source order; not an executed game observation.',source=paths[0].relative_to(ROOT).as_posix())

def context():
    effects=prior.prior.definitions('common/scripted_effects');laws=prior.prior.definitions('common/laws')
    tags=['GEN','SAR','AUS','MOD','PAR','TUS','LUC'];pol={t:initial_policy(t,effects,laws) for t in tags}
    rows=[]
    for folder in ['common/history/diplomacy','common/history/treaties','common/history/power_blocs']:
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            text=p.read_text(encoding='utf-8-sig')
            hits=[dict(line=n,text=line.strip()) for n,line in enumerate(text.splitlines(),1) if any('c:'+tag in line for tag in tags)]
            if hits:rows.append(dict(file=str(p),hits=hits))
    trigger=(ROOT/'common/scripted_triggers/1776_imperial_constitution.txt').read_text(encoding='utf8')
    member=core.cw.parse(trigger)[0]
    dump('INITIAL_CONTEXT.json',dict(task_ids=[TASK],policies=pol,diplomacy_and_power_bloc_references=rows,
        gen_referenced_in_effective_diplomacy_or_treaties=any('c:GEN' in h['text'] for r in rows if '/power_blocs/' not in r['file'].replace('\\','/') for h in r['hits']),
        gen_in_imperial_member_trigger='c:GEN' in trigger[member.start:member.end],
        gen_in_power_bloc=any('c:GEN' in h['text'] for r in rows if '/power_blocs/' in r['file'].replace('\\','/') for h in r['hits']),
        gen_registry_rights=0,sar_rights=9,imperial_rights=574,scope_is_source_inventory_not_live_diplomacy=True))
    print('Initial context recorded; GEN laws',pol['GEN']['laws'],flush=True)

def gen_admin(raw):
    region=core.region(raw,'STATE_PIEDMONT','GEN')
    nodes=[n for n in region.children('create_building') if core.cw.scalar(n.one('building'))=='building_government_administration']
    assert len(nodes)==1,'Expected one existing GEN administration'
    return nodes[0]

def candidate(raw):
    """One scalar edit on the fresh shared file; reject replay or altered core payload."""
    node=gen_admin(raw)
    assert [n.key for n in node.children()]==['building','add_ownership','reserves','activate_production_methods'],'Unexpected extra administration instructions'
    ownership=node.children('add_ownership');assert len(ownership)==1
    country=ownership[0].children('country');assert len(country)==1
    assert len(ownership[0].children())==1 and [n.key for n in country[0].children()]==['country','levels']
    assert core.cw.scalar(country[0].one('country'))=='c:GEN' and core.cw.scalar(country[0].one('levels'))=='1'
    assert core.cw.scalar(node.one('reserves'))=='1'
    pms=node.children('activate_production_methods');assert len(pms)==1
    values=pms[0].children()
    assert [core.cw.scalar(n.value) for n in values]==['pm_religious_bureaucrats','pm_hereditary_bureaucrats',OLD_PM], 'Unexpected or already corrected GEN methods'
    target=values[-1];token=raw[target.start:target.end]
    assert token=='"'+OLD_PM+'"',(token,target)
    result=core.edits(raw,[(target.start,target.end,'"'+NEW_PM+'"')])
    assert result[:target.start]==raw[:target.start] and result[target.start+len(NEW_PM)+2:]==raw[target.end:]
    assert core.cw.parse(result)
    return result

def install():
    b=load(OUT/'BASELINE.json');p=ROOT/BUILDINGS
    assert not (OUT/'BUILDINGS_BEFORE.txt').exists(),'Do not overwrite the shared-file preimage'
    assert prior.prior.runtime_hashes()==b['hashes'],'Concurrent runtime update requires reconciliation'
    before=p.read_bytes();text=before.decode('utf8');after=candidate(text).encode('utf8')
    assert sha(p)==b['hashes'][BUILDINGS]
    (OUT/'BUILDINGS_BEFORE.txt').write_bytes(before)
    assert p.read_bytes()==before,'Concurrent shared-file edit detected'
    p.write_bytes(after)
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        sub_lots=[dict(id=SUB,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',tag='GEN',state='STATE_PIEDMONT',category='B',
            scope='Existing one-level public GEN administration only: replace technology-incompatible base organization method; preserve ownership, capacity, other two methods and every other building.',file=BUILDINGS)],
        before_pm=OLD_PM,after_pm=NEW_PM,levels_before=1,levels_after=1,public_owner_before='GEN',public_owner_after='GEN',
        before_sha256=b['hashes'][BUILDINGS],after_sha256=sha(p),functional_files_modified=[BUILDINGS],
        territory_changed=False,population_changed=False,registry_changed=False,new_tags=[],points_awarded=0,automated_engine_test=False,engine_executed=False))
    print('Installed one GEN method correction; fresh shared-file preimage preserved',flush=True)

def validate():
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for field in inv:
        if field!='buildings':ck('World inventory retained: '+field,inv[field]==b['inventory'][field])
    before=(OUT/'BUILDINGS_BEFORE.txt').read_bytes();after=(ROOT/BUILDINGS).read_bytes()
    old=gen_admin(before.decode('utf8'));new=gen_admin(after.decode('utf8'))
    ck('Exactly one scalar change; all other shared-file bytes retained',after==candidate(before.decode('utf8')).encode('utf8'))
    ck('Fresh preimage matches baseline',sha(OUT/'BUILDINGS_BEFORE.txt')==b['hashes'][BUILDINGS])
    expected=core.qa.counter(b['inventory']['buildings'])
    expected[('STATE_PIEDMONT','GEN',core.qa.signature(old))]-=1
    expected[('STATE_PIEDMONT','GEN',core.qa.signature(new))]+=1
    ck('Exactly one GEN building method changed; all other world building payloads retained',core.qa.counter(inv['buildings'])==expected)
    ck('Three initial GEN methods retained apart from available organization',
        [core.cw.scalar(n.value) for n in new.children('activate_production_methods')[0].children()]==['pm_religious_bureaucrats','pm_hereditary_bureaucrats',NEW_PM])
    current=prior.prior.runtime_hashes();delta=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    ck('Only one existing functional file changed',delta==[BUILDINGS],delta)
    ck('No functional additions or deletions; 2411 files',set(current)==set(b['hashes']) and len(current)==2411)
    ck('Every other functional file retained byte for byte',all(current.get(p)==h for p,h in b['hashes'].items() if p!=BUILDINGS))
    ck('574 imperial rights unchanged',len(b['registry'])==574 and load(reg.active_registry_path())==b['registry'])
    ck('Nine approved SAR Piedmont rights unchanged',len([r for r in b['registry'] if r['beneficiary']=='SAR'])==9 and reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}})
    ck('No imperial GEN right invented',not [r for r in b['registry'] if r['beneficiary']=='GEN'])
    ck('Approved cumulative registry layer retained',reg.approved_lot_dirs()[-1].name=='SC1-SALZBURG')
    ck('World population retained',sum(r['count'] for r in inv['pops'])==834926252)
    ck('GEN population retained',sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='GEN')==510000)
    native=load(OUT/'NATIVE_INVENTORY.json');focus=[r for r in native['provinces'] if r['owner_before']=='GEN']
    ck('Three GEN RGB and 328 cells retained',len(focus)==3 and sum(r['cells_before'] for r in focus)==328)
    for row in native['provinces']:
        ck('Native owner retained '+row['rgb'],[r for r in inv['owners'] if r['key'][0]==row['rgb']]==[dict(key=[row['rgb'],row['state_before'],row['owner_before']],count=1)])
    pol=load(OUT/'INITIAL_CONTEXT.json')['policies']['GEN'];pms=prior.prior.definitions('common/production_methods')
    groups=prior.prior.definitions('common/production_method_groups');buildings=prior.prior.definitions('common/buildings')
    pmgroups=[core.cw.scalar(n.value) for n in buildings['building_government_administration'].children('production_method_groups')[0].children()]
    def values(node,f):return {core.cw.scalar(n.value) for n in node.children(f)[0].children()} if node.children(f) else set()
    for key in ['pm_religious_bureaucrats','pm_hereditary_bureaucrats',NEW_PM]:
        ck('Effective PM exists '+key,key in pms);node=pms[key]
        ck('GEN initial law/technology compatibility '+key,(not values(node,'unlocking_laws') or bool(values(node,'unlocking_laws')&set(pol['laws'].values()))) and not values(node,'disallowing_laws')&set(pol['laws'].values()) and values(node,'unlocking_technologies')<=set(pol['technologies']))
        ck('Exactly one compatible group '+key,len([g for g in pmgroups if key in values(groups[g],'production_methods')])==1)
    ck('Old method has an absent effective technology prerequisite',values(pms[OLD_PM],'unlocking_technologies')=={'systematic_population_registration'} and 'systematic_population_registration' not in pol['technologies'])
    ck('Republican merchant laws retained',pol['laws']['lawgroup_governance_principles']=='law_presidential_republic' and pol['laws']['lawgroup_distribution_of_power']=='law_merchant_republic')
    ck('GEN character and every history character file retained',all(current[p]==h for p,h in b['hashes'].items() if p.startswith('common/history/characters/')))
    ck('Only organization slot changes; inherited fourth reporting-group initialization left unchanged',len(new.children('activate_production_methods')[0].children())==len(old.children('activate_production_methods')[0].children())==3 and len(pmgroups)==4)
    for task in ['SC2-ANTERIOR-AUSTRIA','SC4-EXISTING-ITALIAN-STATES','SC4-SAVOY-NICE']:
        t=next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']==task)
        ck('Prior human partial receipt remains bounded '+task,rm.partial_runtime_evidence(t) and t['status']=='BLOCKED' and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),b['roadmap']))
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    old_changes=[p for p,h in b['report_hashes'].items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    ck('All older historical evidence and attestations retained',not old_changes,old_changes)
    tool_changes=[p for p,h in b['tool_hashes'].items() if p!='tools/serg_sc4_ligurian_fiefs.py' and sha(ROOT/p)!=h]
    ck('All previous tools and tests retained',not tool_changes,tool_changes)
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index retained',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    v=dict(task_ids=[TASK],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False,regional_status='BLOCKED',points_awarded=0)
    dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current))
    dump('FILES_MODIFIED.json',dict(runtime_files_written_by_this_pass=delta,new_runtime_files=[],sha256={p:current[p] for p in delta},baseline_count=len(b['hashes']),current_count=len(current),all_other_runtime_files_byte_identical=all(current.get(p)==h for p,h in b['hashes'].items() if p!=BUILDINGS),shared_file_only_one_token_changed=after==candidate(before.decode('utf8')).encode('utf8')))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']

MODULES=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc','test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia','test_serg_sc2_inner_austria','test_serg_sc2_anterior_austria','test_serg_sc4_italian_states','test_serg_sc4_savoy_nice','test_serg_sc4_ligurian_fiefs']

def run_tests(label,modules,inherited):
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
    # Write reports only after every read-only tracker test has completed.
    (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
    failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
    unexplained=[f for f in failures if f['id'] not in inherited]
    dump(label+'.json',dict(task_ids=[TASK],status='PASS' if not failures else 'INHERITED_FAILURES_ONLY' if not unexplained else 'FAIL',total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],unexplained_failures=unexplained,automated_engine_test=False))
    print(label,result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,'unexplained',len(unexplained),flush=True)
    assert not unexplained,unexplained
    assert {f['id'] for f in failures}==set(inherited)

def tests():
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    run_tests('TESTS',MODULES,inherited)
    run_tests('SCOPED_TESTS',MODULES[-9:],set())
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),unexplained_failures=[],old_tests_not_modified=True,automated_engine_test=False,explanation='Three inherited assertions expect former registry tails; the approved cumulative Salzburg layer passes. One initial no-edit check is skipped.'))

def tracking():
    v=load(OUT/'VALIDATION.json');tested=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert v['passed']==v['total'] and not v['failed'] and not tested['unexplained_failures'] and not scoped['failed']
    assert (OUT/'REPORT.md').is_file() and (OUT/'PLAYER_TEST_PROTOCOL.md').is_file()
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==load(OUT/'BASELINE.json')['roadmap'],'Concurrent tracker update requires reconciliation'
    assert state['events'][-1]['id']=='SERG-RM-0020' and rm.progress(state)['next_task']==TASK
    t=next(t for t in state['tasks'] if t['id']==TASK);implementation=load(OUT/'IMPLEMENTATION.json')
    block='P0 : juridictions ligures autonomes ou féodales non représentées séparément et qualification des droits GEN/SAR/Doria/Spinola/Fieschi/Pallavicini incomplète au 1er janvier 1776. Torriglia/Santo Stefano et les curies survivantes sont attestés ; Cabella reste Pallavicini avant sa vente de 1783. Aucun ensemble de cellules et aucune répartition de population encore homologués pour une représentation politique B ou un TAG borné ; Noli distincte de la protection génoise, statut impérial à qualifier. Confronter les pièces datées aux vallées et aux agrégats côtiers/voisins, ou arbitrage explicite ; ne pas déclarer conforme toute GEN ni étendre automatiquement son impérialité. La méthode administrative corrigée est indépendante et ne clôture pas ces questions.'
    t.update(status='BLOCKED',blocking_reason=block,installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=implementation['sub_lots'],
        installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',scope='LF-GEN-ADM-PM only: initial method on the existing one-level public GEN administration. No territory, population, capacity, diplomatic or imperial-right change.'),
        decision=None,residual_uncertainty=block+' LF-GEN-ADM-PM attend le protocole moteur du joueur ; absence de preuve cadastrale ou de budget historique certifié.',
        current_delivery_note='Audit régional Ligurie et interfaces de 1776 livré ; une incompatibilité technologique de la méthode administrative GEN corrigée dans le bâtiment existant, sans niveau supplémentaire. Trois RGB/328 cellules et 510000 habitants GEN, toutes propriétés et capacités, unités, souverain, capitale et 574 droits conservés. Un seul token du fichier partagé courant changé ; tous autres octets et travaux concurrents conservés. LF-GEN-ADM-PM IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; tâche globale BLOCKED P0 pour représentation territoriale et qualification des droits. Aucun reçu humain nouveau ni point. Savoie/Nice : deux administrations PASS limité, région BLOCKED. Prochaine candidate Piombino identifiée sans commencement.')
    t['historical_sources'].append(PREFIX+'SOURCES.md:1')
    t['identified_problem'].append('Fiefs survivants et parts de souveraineté à distinguer des propriétés privées, cessions antérieures et transmissions postérieures ; PM administratif génois initial incompatible avec la technologie explicitement recherchée, correction indépendante installée.')
    t['delivered_scope']=dict(classification='B_EXISTING_ADMINISTRATION_METHOD_CORRECTION',sub_lots=[SUB],native_audited_rgb=3,native_audited_cells=328,audited_population=510000,territory_changed=False,population_changed=False,building_levels_changed=False,registry_changed=False,cadastral_validation=False,regional_acceptance_complete=False)
    state['mission_status']='SC4_LIGURIAN_FIEFS_PARTIAL_CORRECTION_AWAITING_USER_TERRITORIAL_LEGAL_BLOCK'
    candidate=rm.progress(state)['next_task'];assert candidate=='SC4-PIOMBINO'
    note=f'Reçu explicite SN-I-SAV/SN-I-NIC enregistré préalablement par SERG-RM-0020, sans clôture Savoie–Nice. Une seule nouvelle P0 : SC4-LIGURIAN-FIEFS, admissibilité confirmée après validateur. Sources archivistiques et carte 1750 réutilisées ; juridictions Doria, Spinola, Fieschi et Pallavicini distinguées de GEN/SAR et des transmissions postérieures ; hypothèses B documentées, aucun transfert arbitraire. Correction indépendante LF-GEN-ADM-PM : méthode disponible dans l’administration publique GEN existante, un seul token du fichier courant changé ; trois RGB/328 cellules, 510000 habitants GEN, niveaux, propriétaires, unités, gouvernements, 574 droits et neuf électeurs conservés. Ensemble BLOCKED P0 pour géographie et qualification des droits ; installation IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION avec protocole joueur, aucun reçu fictif ni point. Statique {v["passed"]}/{v["total"]} ; suite cumulative {tested["passed"]}/{tested["total"]}, trois assertions héritées et une exclusion ; ciblée {scoped["passed"]}/{scoped["total"]}, une exclusion, aucun échec inexpliqué. Travaux antérieurs et concurrents conservés, autres blocages inchangés. Progression 82/235=34,89 % avant/après ; périmètre 1.0.0, 81 tâches, poids inchangés. Correction d’affichage du nombre de sous-lots acceptés (deux pour Savoie–Nice), sans changement du barème. Candidate SC4-PIOMBINO identifiée seulement, aucune deuxième étape commencée. Aucun Git ou vanilla écrit.'
    state['events'].append(dict(id='SERG-RM-0021',date='2026-10-23',kind='PARTIAL_IMPLEMENTATION_WITH_TERRITORIAL_LEGAL_BLOCK',scope_version=state['scope_version'],source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=note,evidence=[PREFIX+n for n in ['REPORT.md','SOURCES.md','SECTOR_AUDIT.md','JURISDICTION_MATRIX.csv','NATIVE_INVENTORY.json','RGB_BEFORE_AFTER.csv','IMPLEMENTATION.json','VALIDATION.json','TESTS.json','SCOPED_TESTS.json','PLAYER_TEST_PROTOCOL.md']]))
    assert [x for x in state['tasks'] if x['id']!=TASK]==[x for x in original['tasks'] if x['id']!=TASK]
    assert state['events'][:-1]==original['events'] and not rm.structural_errors(state),rm.structural_errors(state)
    after=rm.progress(state)
    assert (after['earned_weight'],after['total_weight'],after['percent'],after['qualified_tasks'],after['next_task'])==(82,235,'34.89',24,candidate)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked['errors']
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged_since_savoy_nice_acceptance=True,previous_20_events_unchanged=True,scope_version_unchanged=True,weights_and_denominator_unchanged=True,qualified_tasks=24,earned_weight=82,total_weight=235,percent='34.89',new_runtime_receipts=0,task_status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',next_candidate=candidate,next_candidate_started=False))
    print('Tracker PASS; 82/235=34.89%; one pending correction; next '+candidate+' not started',flush=True)

def final_tests():
    run_tests('FINAL_TESTS',['test_serg_closure_roadmap','test_serg_sc4_italian_states','test_serg_sc4_savoy_nice','test_serg_sc4_ligurian_fiefs'],set())

def finalize():
    b=load(OUT/'BASELINE.json');current=prior.prior.runtime_hashes();state=load(rm.OUT/'ROADMAP_STATE.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    ck('Runtime unchanged since successful static validation',current==load(OUT/'SESSION_AFTER_STATIC.json')['hashes'])
    delta=[p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)]
    ck('Only documented single-token functional correction',delta==[BUILDINGS] and (ROOT/BUILDINGS).read_bytes()==candidate((OUT/'BUILDINGS_BEFORE.txt').read_bytes().decode('utf8')).encode('utf8'),delta)
    ck('2411 runtime files; all other existing files retained',len(current)==len(b['hashes'])==2411 and set(current)==set(b['hashes']) and all(current[p]==h for p,h in b['hashes'].items() if p!=BUILDINGS))
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    changed=[p for p,h in b['report_hashes'].items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    ck('All previous map and SERG proofs retained',not changed,changed)
    tool_changes=[p for p,h in b['tool_hashes'].items() if p!='tools/serg_sc4_ligurian_fiefs.py' and sha(ROOT/p)!=h]
    ck('All older tools and tests retained after documented display fix',not tool_changes,tool_changes)
    ck('Previous 20 events unchanged',state['events'][:-1]==b['roadmap']['events'])
    ck('Other 80 task records unchanged',[t for t in state['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK])
    ck('24 previously acquired tasks still qualified',sum(rm.qualifications(state).values())==24)
    for task in ['SC2-ANTERIOR-AUSTRIA','SC4-EXISTING-ITALIAN-STATES','SC4-SAVOY-NICE']:
        ck('Previous scoped human acceptance retained '+task,rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']==task)))
    t=next(t for t in state['tasks'] if t['id']==TASK)
    ck('New correction pending; no fake receipt',t['status']=='BLOCKED' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['runtime_validation']['attestation'] is None and len(t['installed_sub_lots'])==1 and t['installed_sub_lots'][0]['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
    ck('Fixed progress and next candidate',rm.progress(state)['earned_weight']==82 and rm.progress(state)['percent']=='34.89' and rm.progress(state)['next_task']=='SC4-PIOMBINO')
    ck('Next candidate not started',next(t for t in state['tasks'] if t['id']=='SC4-PIOMBINO')['status']=='NOT_STARTED')
    ck('Player protocol and jurisdiction matrix present',all((OUT/n).is_file() for n in ['PLAYER_TEST_PROTOCOL.md','JURISDICTION_MATRIX.csv']))
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,encoding='utf8',capture_output=True)
    findings=[dict(file=m.group(1),line=int(m.group(2)),message=m.group(3)) for m in re.finditer(r'^([^:\r\n]+):(\d+): (.+)$',diff.stdout,re.M)]
    inherited=all(f['file']=='common/history/pops/00_west_europe.txt' and f['message']=='trailing whitespace.' and current[f['file']]==b['hashes'][f['file']] for f in findings)
    diff_ok=diff.returncode==0 or diff.returncode in {1,2} and len(findings)==4 and inherited and {f['line'] for f in findings}=={2983,2999,3015,3031}
    dump('DIFF_CHECK.json',dict(task_ids=[TASK],exit_code=diff.returncode,status='INHERITED_WHITESPACE_ONLY' if findings and diff_ok else 'PASS' if diff_ok else 'FAIL',findings=findings,existing_file_byte_identical=inherited,stdout=diff.stdout,stderr=diff.stderr,files_not_rewritten=True))
    ck('Only inherited whitespace findings in unchanged file',diff_ok,findings)
    checked=rm.check();ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    ck('All delivered static and scoped test proofs pass',load(OUT/'VALIDATION.json')['failed']==[] and load(OUT/'TESTS.json')['unexplained_failures']==[] and load(OUT/'SCOPED_TESTS.json')['failed']==[] and load(OUT/'FINAL_TESTS.json')['failed']==[])
    dump('FINAL_CHECKS.json',dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,prior_proof_files_checked=len(b['report_hashes'])-len(canonical&b['report_hashes'].keys()),automated_engine_test=False))
    dump('SESSION_AFTER.json',dict(hashes=current,git_head=git('rev-parse','HEAD'),git_branch=git('branch','--show-current'),git_index_sha256=sha(ROOT/'.git/index'),progress=rm.progress(state)))
    dump('TRACKER_VALIDATION_FINAL.json',checked)
    assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']
    files += [p for p in prior.OUT.glob('*2026_10_23*') if p.is_file()]
    files += [ROOT/BUILDINGS]
    files += [ROOT/'tools'/n for n in ['serg_sc4_ligurian_fiefs.py','test_serg_sc4_ligurian_fiefs.py','serg_closure_accept_savoy_nice.py','serg_closure_roadmap.py']]
    files += [rm.OUT/n for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json','CLOSURE_CHECKLIST.md','DEFERRED_P2.md']]
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK],files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(files))},automated_engine_test=False))
    assert all(sha(ROOT/p)==h for p,h in load(OUT/'DELIVERY_MANIFEST.json')['files'].items())
    print('Final checks',len(checks),'/',len(checks),'prior proofs',len(b['report_hashes']),flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
