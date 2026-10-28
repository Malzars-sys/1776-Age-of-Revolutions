"""Six explicit SERG receipts, documentary only; no installers or Git writes.

prepare verifies current installations before creating evidence. receive records
only independently passing tasks. finish checks preservation and renders history.
Older validators and proofs are never rewritten or made artificially green.
"""
import ast
import contextlib
import copy
import functools
import io
import json
from pathlib import Path
import re
import sys
import traceback
import unittest

import numpy as np
import map2l_registry as reg
from map2l_belgium import packed
import serg_map2a_reception_20261027 as prior
import validate_map2k_imperial as imperial

rm=prior.rm; qa=prior.qa; ROOT=rm.ROOT
OUT=rm.OUT/'GROUPED_RECEPTION_2026_10_27'
PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
SOURCE=Path('C:/Users/simeo/.codex/attachments/83a49f33-8704-4f32-9002-37374048115a/Texte collé.txt')
OLD_PROTOCOL=rm.OUT/'SC2-MAP2A-VALIDATION/ACCEPTANCE_2026_10_27/PLAYER_TEST_PROTOCOL_GROUPED.md'
CASES={
 'SC4-MILAN-VALIDATION':(['MILAN_CREMONESE'],{'AUS'}),
 'SC4-PIEDMONT-VALIDATION':(['PIEDMONT'],{'SAR'}),
 'SC5-MINDEN-VALIDATION':(['MINDEN_RAVENSBERG'],{'PRU'}),
 'SC5-COLOGNE-VALIDATION':(['DUCHY_WESTPHALIA'],{'KCL'}),
 'SC5-MAINZ-VALIDATION':(['MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION'],{'KMZ'}),
 'SC6-SWABIA-CONTINUATION-VALIDATION':(['SWABIA_CONTINUATION'],{'SFU','SEW'})}
VIEWS=prior.VIEWS
rel=prior.rel; sha=prior.sha; load=prior.load; now=prior.now
def dump(name,obj): rm.write_json(OUT/name,obj)
def receipt_path(task): return rm.OUT/task/'RUNTIME_USER_ATTESTATION_2026_10_27.json'
def validation_path(task):
    latest=OUT/('AT_RECEPTION_VALIDATION_'+task+'.json')
    if latest.exists(): return latest
    newer=OUT/('RECHECK_VALIDATION_'+task+'.json')
    return newer if newer.exists() else OUT/('VALIDATION_'+task+'.json')
def event_id(state): return 'SERG-RM-'+str(max(int(e['id'].split('-')[-1]) for e in state['events'])+1).zfill(4)
SEMANTIC_SHARED={'common/history/states/00_states.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt'}
def runtime_delta(before,after):
    return [dict(path=p,before=before.get(p),after=after.get(p)) for p in sorted(set(before)|set(after)) if before.get(p)!=after.get(p)]
def critical_changes(changes,checks):
    dependencies={p for r in checks.values() for p in r['current_dependency_sha256']}
    return [c for c in changes if c['path'] in dependencies-SEMANTIC_SHARED]
def protected_proof(path):
    return path.startswith(('docs/reports/map/SERG_CLOSURE/','docs/reports/map/MAP2L/','docs/reports/map/MAP2A/','docs/reports/hre/'))
def country_history_selected(raw,tags):
    keys={'c:'+t for t in tags}
    return any(n.key in keys for root in qa.cw.parse(raw) for n in (root.children() if root.key=='COUNTRIES' else [root]))


def restitution_binding_valid(effect,rgb,sid,tag):
    # Province clauses are nested inside region guards, not direct children.
    bindings=[n for n in qa.cw.walk(effect.children()) if n.key=='if' and 'p:'+rgb+'.state' in imperial.textnode(n.children('limit'))]
    return len(bindings)==1 and any(s.key=='s:'+sid and any(b.one('country')=='c:'+tag and rgb in qa.values(b,'provinces') for b in s.children('set_owner_of_provinces')) for s in bindings[0].children())


def targeted():
    inv=qa.inventory(); campaign=load(prior.CAMPAIGN/'BASELINE.json')
    before=campaign['inventory']; bmp=packed(ROOT/'map_data/provinces.png')
    colors,counts=np.unique(bmp,return_counts=True); sizes=dict(zip(map(int,colors),map(int,counts)))
    owners=qa.counter(inv['owners']); rights=load(reg.active_registry_path()); lookup={r['rgb']:r for r in rights}
    node=functools.lru_cache(None)(imperial.node)
    effect='common/scripted_effects/1776_imperial_constitution.txt'
    member=imperial.textnode(node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_member'))
    refresh=imperial.textnode(node(effect,'aor1776_hre_feedback_refresh'))
    restitution=node(effect,'aor1776_hre_return_requested_provinces')
    bloc=next(n for n in qa.cw.walk(qa.cw.parse((ROOT/'common/history/power_blocs/00_power_blocs.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:AUS')
    nodes=[n for n in qa.cw.walk(bloc.children()) if n.key=='member']
    results={}
    for task,(folders,tags) in CASES.items():
        checks=[]
        def ck(name,ok,detail=None): checks.append(dict(name=name,passed=bool(ok),detail=detail))
        paths=[ROOT/'docs/reports/map/MAP2L'/f for f in folders]
        if task=='SC4-PIEDMONT-VALIDATION':
            selected=load(paths[0]/'EXTENSION.json')['provinces']; regions={'STATE_PIEDMONT','STATE_SARDINIA'}
            ck('Nine exact Piedmont entries retained',len(selected)==9 and all(lookup.get(r['rgb'])==r for r in selected))
            ck('Sardinia remains outside registered territorial scope',not any(r['beneficiary']=='SAR' and r['state']=='STATE_SARDINIA' for r in rights))
            ck('SAR registered scope remains Piedmont alone',{r['rgb'] for r in rights if r['beneficiary']=='SAR'}=={r['rgb'] for r in selected})
            ck('Sardinian provinces have no registered markers',all('p:'+r['key'][0]+'.state' not in refresh for r in inv['owners'] if r['key'][1:]==['STATE_SARDINIA','SAR']))
        else:
            geometry=reg.effective_assignments([load(p/'GEOMETRY.json') for p in paths])
            selected=[r for r in geometry if r['owner'] in tags]; regions={r['state'] for r in geometry}
        ck('Nonempty delivered scope',bool(selected))
        for row in selected:
            rgb,sid,tag=row['rgb'],row['state'],row.get('owner',row.get('beneficiary'))
            ck('Unique owner and technical State Region '+rgb,owners[rgb,sid,tag]==1 and sum(n for k,n in owners.items() if k[0]==rgb)==1 and inv['geometry'][rgb]==sid)
            ck('Imperial rightful holder retained '+rgb,lookup.get(rgb,{}).get('beneficiary')==tag and lookup.get(rgb,{}).get('state')==sid)
            ck('Initial registered marker refresh '+rgb,'p:'+rgb+'.state' in refresh)
            ck('Exact restitution country region and province '+rgb,restitution_binding_valid(restitution,rgb,sid,tag))
            if 'cells' in row:
                ck('Exact reviewed cells, with no shape expansion '+rgb,sizes.get(int(rgb[1:],16))==row['pixels'] and all(int(bmp[y,x])==int(rgb[1:],16) for x,y in row['cells']))
        for tag in sorted(tags):
            ck('Member declaration '+tag,'c:'+tag in member)
            ck('Starting imperial bloc member or leader '+tag,bloc.key=='c:'+tag or sum(qa.cw.scalar(n.value)=='c:'+tag for n in nodes)==1)
            ck('Country definition and capital retained since campaign '+tag,inv['countries'].get(tag)==before['countries'].get(tag))
        for key,index in [('owners',1),('regional_pop',0),('buildings',0),('units',2)]:
            ck('Current whole-region conservation since October 26 '+key,
               [r for r in before[key] if r['key'][index] in regions]==[r for r in inv[key] if r['key'][index] in regions])
        if task=='SC4-MILAN-VALIDATION':
            ck('64-cell Austrian connection',sum(r.get('pixels',0) for r in selected)==64)
            ck('Bergamo VEN and Three Leagues SWI preserved',owners['x867A90','STATE_LOMBARDY','VEN']==1 and owners['x9AC196','STATE_LOMBARDY','SWI']==1)
        if task=='SC5-MINDEN-VALIDATION':
            ck('Minden 76 cells only',sum(r['pixels'] for r in selected)==76)
            ck('Bielefeld/Ravensberg not absorbed into Minden',owners['x165E05','STATE_HANNOVER','HAN']==1)
        if task=='SC5-COLOGNE-VALIDATION': ck('Cologne 84 cells, not all Westphalia',sum(r['pixels'] for r in selected)==84)
        if task=='SC5-MAINZ-VALIDATION': ck('Three reviewed layers, Erfurt excluded',len(paths)==3 and not any(r['state']=='STATE_THURINGIA' for r in selected))
        if task=='SC6-SWABIA-CONTINUATION-VALIDATION':
            for tag,capital in [('SFU','STATE_BADEN'),('SEW','STATE_FRANCONIA')]:
                ck('Delivered State Region capital '+tag,any(n[:2]==['capital','='] and n[2]==capital for n in json.loads(inv['countries'][tag])[2]))
        # Histories may have acquired legitimate TECH work since initial delivery.
        # Check against the already-audited October 26 workspace, not an old restore.
        dependencies=set()
        for p in paths:
            if (p/'PLAN.json').exists(): dependencies.update(load(p/'PLAN.json')['files'])
            dependencies.update(load(p/'IMPERIAL_FILES.json')['files'])
        histories={p for p in campaign['hashes'] if p.startswith('common/history/countries/') and country_history_selected((ROOT/p).read_text(encoding='utf-8-sig'),tags)}
        ck('Target starting country histories and technologies retained since campaign',bool(histories) and all(sha(ROOT/p)==campaign['hashes'][p] for p in histories),sorted(histories))
        results[task]=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',task_ids=[task],total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c for c in checks if not c['passed']],checks=checks,
            selected_provinces=selected,reviewed_regions=sorted(regions),installed_reports=[rel(p/'REPORT.md') for p in paths],
            delivered_functional_paths=sorted(dependencies),current_dependency_sha256={p:sha(ROOT/p) for p in sorted(dependencies|histories) if (ROOT/p).is_file()},automated_engine_test=False)
    return results,inv


def regressions():
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(m) for m in [
        'test_serg_closure_roadmap','test_map2l_registry','test_map2l_runtime_receipt','test_hre_centralization_01','test_hre_subject_feedback_01'])
    stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    return dict(status='PASS' if result.wasSuccessful() else 'FAIL',total=result.testsRun,
        passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
        failed=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors],
        skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],raw_output=stream.getvalue(),automated_engine_test=False)


def legacy_shared():
    node=functools.lru_cache(None)(imperial.node); rights=load(reg.active_registry_path()); rows=[]
    for module,fn,args in [('validate_map2k_feedback','validate_feedback',[rights]),('validate_map2k_reforms','validate_reforms',[]),('validate_map2k_repairs','validate_repairs',[rights]),('validate_map2k_dashboard','validate_dashboard',[]),('validate_map2k_demand_feedback','validate_demand_feedback',[]),('validate_map2k_atlas_access','validate_atlas_access',[]),('validate_map2k_electoral_choices','validate_electoral_choices',[])]:
        checks=[]; error=None; stream=io.StringIO()
        def ck(name,ok,detail=''): checks.append(dict(name=name,passed=bool(ok),detail=detail))
        try:
            with contextlib.redirect_stdout(stream): getattr(__import__(module),fn)(ck,node,imperial.textnode,*args)
        except Exception as ex: error=dict(type=type(ex).__name__,message=str(ex),traceback=traceback.format_exc())
        rows.append(dict(module=module,entrypoint=fn,total_executed=len(checks),passed=sum(c['passed'] for c in checks),failed=[c for c in checks if not c['passed']],checks=checks,error=error,completed=error is None,raw_output=stream.getvalue()))
    old=load(prior.CAMPAIGN/'BASELINE.json')['hashes']
    paths=['common/scripted_effects/1776_imperial_constitution.txt','common/scripted_triggers/1776_imperial_constitution.txt']
    preserved={p:dict(campaign_sha256=old[p],current_sha256=sha(ROOT/p),unchanged=old[p]==sha(ROOT/p)) for p in paths}
    failed=[(r['module'],c['name']) for r in rows for c in r['failed']]; errors=[r for r in rows if r['error']]
    known=(failed==[('validate_map2k_reforms','same_country_native_leader_branch_preserves_principles')]
           and len(errors)==1 and errors[0]['module']=='validate_map2k_reforms' and errors[0]['error']['type']=='StopIteration'
           and all(v['unchanged'] for v in preserved.values()))
    return dict(status='FAIL_RAW_RETAINED' if failed or errors else 'PASS',rows=rows,known_preexisting_structure_mismatch=known,
        classification='Old reform validator expects direct succession children; installed centralized-subject wrapper delegates to the legacy effect. Existing current centralization and feedback contracts are tested separately, without editing the old validator.',
        source='docs/reports/hre/HRE_CENTRALIZATION_01/REPORT.md',current_contract='tools/test_hre_centralization_01.py:92',
        preserved_dependencies=preserved,automated_engine_test=False)


def prepare():
    assert not OUT.exists(), 'Never overwrite a reception run'
    assert all(not receipt_path(t).exists() for t in CASES), 'A receipt already exists'
    state=load(rm.OUT/'ROADMAP_STATE.json')
    before=dict(recorded_at=now(),roadmap=state,progress=rm.progress(state),runtime_hashes=rm.hashes(),git=prior.git_state(),
        tracker_source=(ROOT/'tools/serg_closure_roadmap.py').read_text(encoding='utf-8'),
        root_texts={n:(rm.OUT/n).read_text(encoding='utf-8') for n in VIEWS},
        proofs={rel(p):sha(p) for p in (ROOT/'docs').rglob('*') if p.is_file()},
        instructions={rel(p):sha(p) for p in [ROOT/'AGENTS.md',*(ROOT/'.agents').rglob('*.md')]})
    checks,inv=targeted()
    print('Scoped preservation:',{t:(r['passed'],r['total']) for t,r in checks.items()},flush=True)
    raw=legacy_shared(); tests=regressions()
    assert tests['status']=='PASS', tests['failed']
    assert raw['status']=='PASS' or raw['known_preexisting_structure_mismatch'], 'Unclassified shared regression'
    assert rm.check()['status']=='PASS'
    current=rm.hashes(); delta=runtime_delta(before['runtime_hashes'],current)
    initial_checks=checks
    if delta:
        assert not critical_changes(delta,checks), 'Relevant dependency changed; review before reception'
        checks,inv=targeted()
        assert not critical_changes(runtime_delta(before['runtime_hashes'],rm.hashes()),checks)
    before['preflight_external_runtime_changes']=delta
    assert load(rm.OUT/'ROADMAP_STATE.json')==state, 'Concurrent state update; reread'
    altered=[dict(path=p,before=h,after=sha(ROOT/p) if (ROOT/p).is_file() else None) for p,h in before['proofs'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    assert not [r for r in altered if protected_proof(r['path'])], 'Relevant proof updated; reread'
    before['preflight_external_document_changes']=altered
    OUT.mkdir(parents=True)
    dump('BASELINE.json',before);dump('CURRENT_INVENTORY.json',inv)
    if delta:dump('INITIAL_PREFLIGHT_SCOPE_CHECKS.json',initial_checks)
    dump('ABORTED_INITIAL_PREFLIGHT.json',dict(status='ABORTED_BEFORE_ANY_RECEIPT',
        command='python -B -X utf8 tools/serg_six_receptions_20261027.py prepare',
        observed_checks={'SC4-MILAN-VALIDATION':[15,16],'SC4-PIEDMONT-VALIDATION':[40,49],'SC5-MINDEN-VALIDATION':[23,26],'SC5-COLOGNE-VALIDATION':[34,40],'SC5-MAINZ-VALIDATION':[74,90],'SC6-SWABIA-CONTINUATION-VALIDATION':[58,69]},
        raw_terminal_exception='AssertionError: Concurrent runtime change; reread before any reception',
        classification='First attempt stopped on external runtime evolution before persisting its in-memory baseline or receipts. The new reception checker also needed recursive traversal of region-nested restitution clauses; all non-restitution checks passed. No old validator or game file was changed.',
        superseded_by='Fresh current-workspace prepare with recursive exact RGB/State Region/country checks',initial_in_memory_snapshot_not_persisted=True,receipts_created=False))
    dump('PRESERVATION_SUMMARY.json',{t:{k:r[k] for k in ['status','passed','total','failed']} for t,r in checks.items()})
    for t,result in checks.items():dump('VALIDATION_'+t+'.json',result)
    dump('LEGACY_SHARED_TESTS_RAW.json',raw);dump('PREWRITE_TESTS.json',tests);dump('PREWRITE_CANONICAL_CHECK.json',rm.check())
    (OUT/'USER_ATTESTATION.md').write_bytes(SOURCE.read_bytes())
    print('Preflight:',tests['passed'],'passed,',len(tests['skipped']),'skipped; shared legacy mismatch classified',flush=True)


def recheck():
    baseline=load(OUT/'BASELINE.json')
    assert load(rm.OUT/'ROADMAP_STATE.json')==baseline['roadmap'], 'Concurrent SERG state edit; reread'
    initial={t:load(OUT/('VALIDATION_'+t+'.json')) for t in CASES}
    delta=runtime_delta(baseline['runtime_hashes'],rm.hashes())
    assert not critical_changes(delta,initial), 'Relevant dependency changed; reread'
    results,_=targeted()
    for task,result in results.items():
        original=load(OUT/('VALIDATION_'+task+'.json'))
        oldchecks={c['name']:c for c in original['checks']};newchecks={c['name']:c for c in result['checks']}
        assert len(oldchecks)==len(original['checks']) and len(newchecks)==len(result['checks']) and oldchecks.keys()==newchecks.keys()
        corrected=lambda n:n.startswith('Exact restitution country region and province ') or n=='Target starting country histories and technologies retained since campaign'
        assert all(oldchecks[n]==newchecks[n] for n in oldchecks if not corrected(n))
        assert all(corrected(c['name']) for c in original['failed'])
        dest=OUT/('RECHECK_VALIDATION_'+task+'.json')
        if dest.exists():
            stored=load(dest)
            assert {c['name']:c for c in stored['checks']}==newchecks, 'Do not overwrite different recheck evidence'
        else: dump(dest.name,result)
    effect=imperial.node('common/scripted_effects/1776_imperial_constitution.txt','aor1776_hre_return_requested_provinces')
    probes=dict(correct_binding=restitution_binding_valid(effect,'xEDA701','STATE_LOMBARDY','AUS'),
        wrong_country_rejected=not restitution_binding_valid(effect,'xEDA701','STATE_LOMBARDY','ZZZ'),
        wrong_region_rejected=not restitution_binding_valid(effect,'xEDA701','STATE_UNKNOWN','AUS'),
        wrong_province_rejected=not restitution_binding_valid(effect,'xFFFFFF','STATE_LOMBARDY','AUS'))
    assert all(probes.values())
    dump('RECHECK_TRAVERSAL_REVIEW.json',dict(status='PASS',initial_results_retained=True,
        correction='New reception checker initially inspected only direct restitution children and matched country histories using = alone. Actual restitution clauses are nested under State Region guards, and country histories use conditional ?= selectors. Recursive exact RGB/State Region/beneficiary checks and recognition of both selector operators correct these lookups; no game script, old validator or old raw result changed.',
        guard_probes=probes,checks_before_receipts=True,task_ids=list(CASES),external_changes_preserved=delta,automated_engine_test=False))
    print('RECHECK', {t:(r['passed'],r['total']) for t,r in results.items()},flush=True)


def preparation(state):
    old=load(prior.CAMPAIGN/'BLOCKED_MATRIX.json')
    byid={t['id']:t for t in state['tasks']}; rows=[]
    for original in old['rows']:
        task=byid[original['task_id']]
        if task['status']!='BLOCKED': continue
        row=copy.deepcopy(original)
        row.update(current_status=task['status'],installed_current=task.get('installed_sub_lots',[]),
            already_validated_sub_lots=[l['id'] for l in task.get('installed_sub_lots',[]) if l['status']=='PASS_RUNTIME_USER_VALIDATED'],
            current_essential_obligations=task.get('remaining_obligations',row['essential_obligations']),
            new_points=0,not_reclassified_as_P2=True)
        rows.append(row)
    remaining=set(rm.progress(state)['blocked']);assert {r['task_id'] for r in rows}==remaining
    recommendations=[dict(rank=1,task_id='SC2-TESCHEN',reason='TE-R-CORE already installed; complete its own player protocol and obtain explicit decision on documented B territorial/demographic scope. MAP2A is received but does not close this task.',ready_to_close_now=False),
        dict(rank=2,task_id='SC5-EAST-FRISIA-SOUTH',reason='MAP2P recommends no demonstrable additional transfer. An explicitly approved scoped B decision or nonblocking P1 deferral is the shortest decision route; positive historical conformity is not established.',ready_to_close_now=False),
        dict(rank=3,task_id='SC1-ORTENBURG',reason='OR-I-CORE already player-validated; qualify sovereign villages and comparable rural population, excluding Bavarian Hofmarken. This is the next short targeted dossier, not a closure obtainable from the existing core receipt alone.',ready_to_close_now=False)]
    dump('BLOCKED_CURRENT_MATRIX.json',dict(scope_version=state['scope_version'],task_count=len(rows),conditional_points=sum(byid[r['task_id']]['weight'] for r in rows),
        source=rel(prior.CAMPAIGN/'BLOCKED_MATRIX.json'),rows=rows,recommendations=recommendations,
        mission_action='Preparation only; no blocked task or obligation changed',points_awarded_to_blocked_tasks=0))
    tested=[r['task_id']+' ('+', '.join(r['already_validated_sub_lots'])+')' for r in rows if r['already_validated_sub_lots']]
    text=['# Préparation de clôture après les six réceptions — 27 octobre 2026','',
        'Cette note réutilise la matrice du 26 octobre, en retirant uniquement Luxembourg déjà clôturé. Aucun audit général nouveau, aucune installation ni décision B/P1 approuvée par défaut. Les 23 tâches restent BLOCKED ; leurs obligations et leurs points sont conservés.','',
        '## Trois voies les plus courtes à instruire','',
        '1. SC2-TESCHEN (P1, 2 points conditionnels) : correction du registre TE-R-CORE installée. Son protocole propre reste à confirmer ; la décision B proposée sur le périmètre et la population doit être explicitement arbitrée. Le reçu MAP2A ne les remplace pas. Aucune nouvelle frontière nécessaire à cette voie. Sources : [revue existante](../CLOSURE_CAMPAIGN_2026_10_26/TESCHEN_CLOSURE_REVIEW.md) et [proposition non approuvée](../CLOSURE_CAMPAIGN_2026_10_26/TESCHEN_PROPOSED_CLOSURE_DECISION.json).',
        '2. SC5-EAST-FRISIA-SOUTH (P1, 2 points conditionnels) : [MAP2P](../../MAP2P/REPORT.md) ne démontre aucun nouveau transfert prêt à installer. Préparer un arbitrage explicite de portée B ou un report P1 non bloquant motivé ; ne pas certifier une conformité historique non démontrée. Les 319 cellules PRU sont protégées ; les 1240 cellules candidates ne sont pas 1240 erreurs.',
        '3. SC1-ORTENBURG (P1, 1 point conditionnel) : OR-I-CORE est reçu. Restent les villages souverains et une population rurale comparable, séparés des Hofmarken bavaroises. [Sources existantes](../SC1-ORTENBURG/SOURCES.md). Cette troisième voie demande encore une instruction ciblée ; ni le noyau ni le repère de 1840 ne suffisent à clore le comté.','',
        'Aucune des trois tâches n’est prête à être marquée terminale aujourd’hui. Ce classement reprend les rangs 1, 3 et 4 de la matrice existante après retrait de Luxembourg. Il compare la proximité d’une décision, pas la gravité des omissions. Les P0 Innviertel, Carrare, Hohenberg/Fricktal, Italie impériale et Piombino restent indispensables ; aucun n’est converti en P2.','',
        '## Installations déjà testées, critères régionaux encore ouverts','',
        *['- '+s for s in tested],'',
        '## Obligations essentielles et précision facultative','',
        'Essentiel : souverainetés omises, grands ressorts ruraux et populations comparables, correspondance Innviertel/Hohenberg/Fricktal/Carrare, droits des fiefs et partage Elbe–Piombino. Une installation administrative ou une résidence testée ne les résout pas.',
        'Réserves de précision : cadastre exhaustif village par village, petites immunités et détails héraldiques documentés. Elles peuvent rester des limites de B/P2 lorsqu’une représentation politique suffisante est établie ; cette note ne déplace aucune obligation actuelle vers P2 et n’approuve aucun report.','',
        '## Tâches BLOCKED conservées','',
        *['- '+r['task_id']+' — '+r['priority']+' ; '+r['next_concrete_action'] for r in rows],'',
        'Les vérifications humaines encore ouvertes sont regroupées dans [PLAYER_TEST_PROTOCOL_REMAINING.md](PLAYER_TEST_PROTOCOL_REMAINING.md). SC3-HOLSTEIN et tout autre nouveau territoire restent non commencés.']
    (OUT/'CLOSURE_READINESS.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    return recommendations


def receive():
    b=load(OUT/'BASELINE.json'); path=rm.OUT/'ROADMAP_STATE.json'; raw=path.read_bytes(); state=load(path)
    assert state==b['roadmap'], 'Tracker evolved since preflight; reread'
    previous={t:load(validation_path(t)) for t in CASES}
    delta=runtime_delta(b['runtime_hashes'],rm.hashes())
    assert not critical_changes(delta,previous), 'Relevant dependency evolved; review before reception'
    fresh,_=targeted()
    for task,result in fresh.items():
        assert not (OUT/('AT_RECEPTION_VALIDATION_'+task+'.json')).exists()
        dump('AT_RECEPTION_VALIDATION_'+task+'.json',result)
    dump('AT_RECEPTION_CONCURRENT_SCOPE_CHECK.json',dict(status='SCOPE_RECHECKED',external_runtime_changes=delta,
        classification='External files and shared global state/build overlay evolved; each affected European region, exact core mask, owner, POP/building/PM/unit scope rechecked against October 26; no functional write by this mission.'))
    history_probes=dict(compact_conditional=country_history_selected('COUNTRIES = { c:SFU ?= { add_technology_researched = shaft_mining } }',{'SFU'}),
        multiline_conditional=country_history_selected('COUNTRIES = {\n c:SFU ?= { }\n}',{'SFU'}),
        ordinary_assignment=country_history_selected('COUNTRIES = { c:SFU = { } }',{'SFU'}),
        foreign_reference_not_a_country_declaration=not country_history_selected('COUNTRIES = { c:BAD ?= { c:SFU = { } } }',{'SFU'}))
    assert all(history_probes.values())
    dump('HISTORY_CHECKER_REVIEW.json',dict(status='PASS',guard_probes=history_probes,
        correction='Use the existing Clausewitz parser for direct country selectors in COUNTRIES, including compact one-line ?= histories; regex line anchoring missed SFU/SEW. Initial and intermediate raw reports remain intact. Actual country file hashes still compared exactly to the campaign.',automated_engine_test=False))
    source=(OUT/'USER_ATTESTATION.md').read_text(encoding='utf-8-sig')
    common=source.split('### Conditions communes réellement confirmées',1)[1].split('Ces conditions communes',1)[0]
    conditions=[line[2:] for line in common.splitlines() if line.startswith('- ')]
    assert len(conditions)==4
    accepted=[]; changes=[]
    for task in CASES:
        result=load(validation_path(task))
        if result['status']!='PASS':continue
        dest=receipt_path(task);assert not dest.exists(), 'Never overwrite '+str(dest)
        item=next(t for t in state['tasks'] if t['id']==task);assert item['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        section=source.split('### '+task+' — ',1)[1].split('\n### ',1)[0].split('\n## ',1)[0]
        observations=[line[2:] for line in section.splitlines() if line.startswith('- ')]
        assert observations
        receipt=dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[task],scope_type='TASK_PROTOCOL_ONLY',task_closure_approved=True,
            recorded_on='2026-10-27',actual_test_date=None,source=PREFIX+'USER_ATTESTATION.md',source_sha256=sha(OUT/'USER_ATTESTATION.md'),
            source_kind='Explicit current user attachment: SERG TERRITORIAL 1.0 — RÉCEPTION HUMAINE GROUPÉE DE SIX TÂCHES',
            source_quote="Je confirme avoir personnellement effectué et réussi l'intégralité des six protocoles suivants dans Victoria 3 :",
            common_conditions_explicitly_reported=conditions,explicitly_reported=observations,
            shared_session_reference=PREFIX+'USER_ATTESTATION.md',protocol=rel(OLD_PROTOCOL),protocol_row=task,
            new_game_date='1776-01-01',new_game_date_meaning='Scenario start, not real calendar test date',simulation_months=1,save_reload=True,
            personally_performed_by='user',automated_engine_test=False,extra_observations_invented=False,
            scope=dict(delivered_lots=item['installed_lots'],provinces=[dict(rgb=r['rgb'],state=r['state'],owner=r.get('owner',r.get('beneficiary'))) for r in result['selected_provinces']],
                       historical_scope=item['runtime_validation']['scope'],regional_closure_of_other_tasks=False),
            historical_reports=result['installed_reports'],acceptance_checks=rel(validation_path(task)),
            current_dependency_sha256_collected_by_agent=result['current_dependency_sha256'],tested_file_hashes_supplied_by_user=None,
            screenshots_provided=[],employment_statistics_provided=None,economic_measurements_provided=None,
            excluded_task_ids=[t['id'] for t in state['tasks'] if t['id']!=task],excluded_sub_lots=['TE-R-CORE','BG-E-SALT-NATIVE-R1'],
            limitations=['Only this task, not a generic six-task receipt','No full cadastral accuracy or regional outliers certified','No later corrections, WORLD, TECH or ECON work certified'])
        rm.write_json(dest,receipt)
        changes.append(dict(task_id=task,before=item['status'],after=receipt['status']))
        item.update(status=receipt['status'],static_tests=dict(status='PASS',evidence=[rel(validation_path(task))]))
        item['runtime_validation'].update(status=receipt['status'],attestation=rel(dest),protocol=rel(OLD_PROTOCOL),scope=item['runtime_validation']['scope'],new_details_invented=False)
        item['closure_audit'].update(status='TASK_CLOSED_USER_VALIDATED',remaining_controls=[],new_points=item['weight'],reception_report=PREFIX+'REPORT.md')
        item['current_delivery_note']='Protocole propre intégral explicitement réussi par le joueur : '+ '; '.join(observations)+' Nouvelle partie 1776, mois complet sans anomalie, sauvegarde/rechargement. Reçu distinct limité à '+task+' ; aucune extension aux autres tâches ou sous-lots.'
        item['residual_uncertainty']='Noyaux et mécanismes nommés uniquement ; franges non homologuées et précision cadastrale restent hors reçu. Aucun autre dossier clôturé.'
        accepted.append(task)
    assert accepted, 'No independently receivable task'
    pending=[t['id'] for t in state['tasks'] if t['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION']
    campaign=state['closure_campaign']
    campaign.update(pass_status='SIX_GROUPED_HUMAN_RECEIPTS_RECORDED' if len(accepted)==6 else 'PARTIAL_GROUPED_HUMAN_RECEIPTS',
        grouped_protocol=PREFIX+'PLAYER_TEST_PROTOCOL_REMAINING.md',next_closure_candidate='SC2-TESCHEN',
        current_resolution_task=None,current_reception_tasks=accepted,
        remaining_grouped_runtime_points=sum(t['weight'] for t in state['tasks'] if t['id'] in pending))
    campaign['grouped_reception']=dict(date='2026-10-27',task_ids=accepted,source=PREFIX+'USER_ATTESTATION.md',report=PREFIX+'REPORT.md',
        receipts={t:rel(receipt_path(t)) for t in accepted},readiness=PREFIX+'CLOSURE_READINESS.md',blocked_matrix=PREFIX+'BLOCKED_CURRENT_MATRIX.json',
        protocol=campaign['grouped_protocol'],next_recommendations=['SC2-TESCHEN','SC5-EAST-FRISIA-SOUTH','SC1-ORTENBURG'])
    state['mission_status']='SIX_GROUPED_TASKS_USER_VALIDATED_CLOSURE_PREPARATION_ONLY' if len(accepted)==6 else 'GROUPED_RECEPTION_PARTIAL'
    hold=state['runtime_validation_hold']
    hold.update(task_id=pending[0] if pending else 'SC2-TESCHEN',pending_task_ids=pending,protocol=campaign['grouped_protocol'],
        reason='Réception des installations terminée selon les seuls reçus distincts ; préparer les clôtures sans commencer de chantier.',
        test_summary='TE-R-CORE et BG-E-SALT-NATIVE-R1 restent à valider séparément ; aucune extension des six reçus. Une décision explicite est encore nécessaire pour la portée régionale de Teschen.',
        scope_note='Les 23 tâches BLOCKED restent inchangées. Les trois voies proposées sont préparatoires ; SC3-HOLSTEIN reste suspendu.')
    after=rm.progress(state)
    assert after['earned_weight']==b['progress']['earned_weight']+sum(t['weight'] for t in state['tasks'] if t['id'] in accepted)
    state['events'].append(dict(id=event_id(state),date='2026-10-27',kind='SIX_SCOPED_TASKS_EXPLICIT_HUMAN_RECEPTION',scope_version=state['scope_version'],source=PREFIX+'USER_ATTESTATION.md',
        changes=changes,before_weight=b['progress']['earned_weight'],after_weight=after['earned_weight'],total_weight=after['total_weight'],before_percent=b['progress']['percent'],after_percent=after['percent'],
        note='Six protocoles distincts personnellement et intégralement confirmés : nouvelle partie 1776, mois complet sans anomalie, sauvegarde/rechargement ; reçus séparés et limites propres. Aucune date effective, capture ou mesure économique inventée. Aucun point pour les tâches BLOCKED ; aucune nouvelle installation.'))
    preparation(state)
    protocol='''# Contrôles humains encore ouverts après réception groupée

Luxembourg, MAP2A et les six tâches explicitement reçues sont terminés dans leurs seuls périmètres. Leurs protocoles ne sont pas à refaire. Aucun nouveau territoire n’est lancé.

## Teschen — TE-R-CORE, registre uniquement

Le sous-lot attend sa propre confirmation intégrale selon le [protocole existant](../SC2-TESCHEN/PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776 avec Autriche ; portion AUS de Galicie occidentale reconnue impériale ; aucun titre de restitution à un autre souverain ; portions galiciennes voisines exclues ; neuf électeurs et noyaux voisins conservés ; population/bâtiments/technologies/unités de la portion conservés ; un mois et sauvegarde/rechargement, conservation des droits et propriétaires.

L’observation visuelle antérieure reste à sa portée. Les conditions communes attestées pour MAP2A et pour les six autres tâches ne sont pas étendues automatiquement au registre. Inutile de refaire un contrôle effectivement déjà réalisé : le confirmer explicitement pour TE-R-CORE. Aucune guerre artificielle demandée ; restitution après conquête étrangère distincte si non déclenchée.

Même reçu, TE-R-CORE ne clôturera pas à lui seul SC2-TESCHEN : l’arbitrage B sur le périmètre territorial/démographique reste non approuvé. Le pool technique de 135753 n’est pas certifié comme un recensement de 1776.

## Berchtesgaden — BG-E-SALT-NATIVE-R1 uniquement

Selon le [protocole existant](../SC1-BERCHTESGADEN/PLAYER_TEST_PROTOCOL_SALT_NATIVE_REVISION_2026_10_24.md) : nouvelle partie 1776, BGT ; mine de sel ordinaire de niveau 1 visible, partiellement employée ; 1000 habitants et chancellerie conservés ; production de sel, emploi et finances observés sans seuil de rentabilité imposé ; un mois puis sauvegarde/rechargement.

Le noyau BG-I-CORE reste reçu dans sa version historique. Aucun nouveau bâtiment spécial. Cette révision et le ressort rural régional ne sont pas validés par les six réceptions ; Gnotschaften et population comparable restent des obligations régionales.

Retour : nommer le sous-lot réellement contrôlé et confirmer les étapes réussies ou les anomalies. Aucune capture, date effective, statistique d’emploi ou mesure économique n’est présumée.
'''
    if pending: protocol+='\n## Réceptions non closes\n\n'+'\n'.join('- '+t+' : contrôler la divergence statique documentée avant toute clôture.' for t in pending)+'\n'
    (OUT/'PLAYER_TEST_PROTOCOL_REMAINING.md').write_text(protocol,encoding='utf-8')
    report=['# Réception humaine groupée de six tâches — 27 octobre 2026','',
        f"Progression calculée : {b['progress']['earned_weight']}/235 ({b['progress']['percent']} %, {b['progress']['qualified_tasks']}/81) → {after['earned_weight']}/235 ({after['percent']} %, {after['qualified_tasks']}/81). Périmètre 1.0.0 conservé.",'',
        'Les conditions communes (nouvelle partie 1776, mois sans anomalie, sauvegarde/rechargement) proviennent exclusivement de USER_ATTESTATION.md. Chaque tâche reçoit un fichier humain distinct, son périmètre et sa validation statique ; aucune date effective ou mesure supplémentaire.','',
        '| Tâche | Statut | Reçu | Conservation |','| --- | --- | --- | --- |']
    for t in CASES:
        result=load(validation_path(t)); item=next(i for i in state['tasks'] if i['id']==t)
        report.append('| '+t+' | '+item['status']+' | '+(rm.link(receipt_path(t)) if t in accepted else 'Non créé : contrôle en échec')+' | '+str(result['passed'])+'/'+str(result['total'])+' |')
    report+=['','Vérifications : RGB et cellules exacts des noyaux, unicité/State Regions/propriétaires, titres et restitutions, marqueurs initiaux, membres et capitales, voisins et subdivisions ; populations, bâtiments/PM/propriété et unités comparés à la campagne du 26 octobre ; histoires nationales et technologies conservées. Chaque reçu pointe vers son rapport statique effectif (RECHECK_VALIDATION_* ou AT_RECEPTION_VALIDATION_*) et ses empreintes courantes. Aucun ancien fichier restauré.','',
        'Régressions : PREWRITE_TESTS.json puis TEST_RESULTS.json conservent les suites du suivi, migrations, reçus, centralisation et retour sur les sujets impériaux. Un ancien contrôle initial reste désactivé selon son décorateur existant. LEGACY_SHARED_TESTS_RAW.json conserve séparément tous les callbacks de sept validateurs impériaux ; le validateur ancien des réformes échoue sur la forme directe de succession, puis lève StopIteration. Les scripts concernés sont identiques à la campagne du 26 octobre ; l’installation actuelle délègue au chemin antérieur depuis un garde des sujets centralisés. Contrat actuel vérifié par test_hre_centralization_01.py ; aucun ancien test corrigé ou masqué.','',
        'Précontrôles du nouvel outil : première tentative interrompue avant tout reçu sur évolution concurrente du runtime ; résultat observé dans ABORTED_INITIAL_PREFLIGHT.json. Deux erreurs de lecture ont été corrigées dans cet outil seulement : clauses de restitution imbriquées, et sélecteurs nationaux conditionnels ?=. Résultats initiaux conservés dans VALIDATION_*.json ; correction, contrôles de garde et résultats actuels dans RECHECK_TRAVERSAL_REVIEW.json et RECHECK_VALIDATION_*.json. Aucun ancien validateur, résultat brut ou fichier fonctionnel modifié pour ces contrôles. Les changements concurrents hors des six périmètres, notamment dans les fichiers globaux des États et de BUILD, restent installés et sont classés dans CONCURRENT_CHANGES.json après revérification des portions européennes.','',
        'Luxembourg, MAP2A et toutes les anciennes attestations restent intacts. Les 23 tâches BLOCKED et leurs obligations restent inchangées. [Matrice actuelle et préparation des trois voies](CLOSURE_READINESS.md). Aucune réserve historique substantielle transformée en P2.','',
        '[Protocoles humains encore ouverts : Teschen et mine de Berchtesgaden](PLAYER_TEST_PROTOCOL_REMAINING.md). Ni ces sous-lots, ni les travaux WORLD/TECH/ECON, ni les franges des régions ne sont couverts. Aucun nouveau chantier, SC3-HOLSTEIN compris.','',
        'Modifications documentaires seulement. Aucun fichier fonctionnel, vanilla ou Git écrit. Conservation finale et travaux concurrents : FINAL_CHECKS.json, CONCURRENT_CHANGES.json ; preuves antérieures et leurs échecs bruts conservés.']
    (OUT/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    assert not rm.structural_errors(state),rm.structural_errors(state)
    assert path.read_bytes()==raw,'Concurrent state edit before write'
    rm.write_json(path,state);rm.render()


def finish():
    b=load(OUT/'BASELINE.json'); state=load(rm.OUT/'ROADMAP_STATE.json'); after=rm.progress(state)
    checks,_=targeted();tests=regressions();dump('TEST_RESULTS.json',tests)
    for task,res in checks.items():dump('FINAL_VALIDATION_'+task+'.json',res)
    runtime=rm.hashes(); changes=[dict(path=p,before=b['runtime_hashes'].get(p),after=runtime.get(p)) for p in sorted(set(runtime)|set(b['runtime_hashes'])) if runtime.get(p)!=b['runtime_hashes'].get(p)]
    allowed={rel(rm.OUT/n) for n in VIEWS+['ROADMAP_STATE.json']}
    altered=[p for p,h in b['proofs'].items() if p not in allowed and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)]
    protected_altered=[p for p in altered if protected_proof(p)]
    dump('CONCURRENT_CHANGES.json',dict(functional_files_written_by_this_mission=[],external_runtime_changes=changes,
        external_document_changes=[dict(path=p,before=b['proofs'][p],after=sha(ROOT/p) if (ROOT/p).is_file() else None) for p in altered],
        scope_classification='Concurrent files preserved; exact six-region scopes rechecked; immutable SERG/MAP2L/MAP2A/HRE evidence protected separately from active peer documents.',
        critical_dependency_changes=critical_changes(changes,checks),automated_engine_test=False))
    funcs=lambda text:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
    oldf=funcs(b['tracker_source']);newf=funcs((ROOT/'tools/serg_closure_roadmap.py').read_text(encoding='utf-8'))
    fnchanges=[n for n in set(oldf)|set(newf) if oldf.get(n)!=newf.get(n)]
    oldtasks={t['id']:t for t in b['roadmap']['tasks']}; accepted=state['closure_campaign']['grouped_reception']['task_ids']
    receipts={t:load(receipt_path(t)) for t in accepted}; legacy=load(OUT/'LEGACY_SHARED_TESTS_RAW.json')
    assertions=dict(scoped_checks=all(checks[t]['status']=='PASS' for t in accepted),current_tests=tests['status']=='PASS',canonical=rm.check()['status']=='PASS',
        separate_receipts_for_passing_tasks=set(receipts)=={t for t,r in checks.items() if r['status']=='PASS'} and all(r['task_ids']==[t] for t,r in receipts.items()),
        unknown_test_details_preserved=all(r['actual_test_date'] is None and r['screenshots_provided']==[] and r['tested_file_hashes_supplied_by_user'] is None for r in receipts.values()),
        excluded_sub_lots_not_approved=all(r['excluded_sub_lots']==['TE-R-CORE','BG-E-SALT-NATIVE-R1'] for r in receipts.values()),
        only_six_tasks_changed=all(t==oldtasks[t['id']] for t in state['tasks'] if t['id'] not in accepted),
        all_81_tasks_weights_scope_preserved=state['scope_version']==b['roadmap']['scope_version']=='1.0.0' and [(t['id'],t['weight']) for t in state['tasks']]==[(t['id'],t['weight']) for t in b['roadmap']['tasks']],
        history_additive=state['events'][:len(b['roadmap']['events'])]==b['roadmap']['events'],
        progress_calculated=(after['earned_weight'],after['total_weight'],after['qualified_tasks'],after['total_tasks'])==(b['progress']['earned_weight']+sum(oldtasks[t]['weight'] for t in accepted),235,b['progress']['qualified_tasks']+len(accepted),81),
        only_unreceived_complete_protocols_pending=set(after['awaiting_runtime'])==set(CASES)-set(accepted),
        all_23_blocked_retained=after['blocked']==b['progress']['blocked'] and len(after['blocked'])==23,
        immutable_SERG_delivery_proofs_preserved=not protected_altered,
        external_runtime_changes_scoped_and_preserved=not critical_changes(changes,checks) and all(checks[t]['status']=='PASS' for t in accepted),
        instructions_preserved=all(sha(ROOT/p)==h for p,h in b['instructions'].items()),
        git_HEAD_branch_index_preserved=prior.git_state()==b['git'],only_renderer_changed=set(fnchanges)<={'render'},
        legacy_failure_raw_retained_and_classified=legacy['status']=='PASS' or legacy['known_preexisting_structure_mismatch'],
        no_Holstein_started=next(t for t in state['tasks'] if t['id']=='SC3-HOLSTEIN')==oldtasks['SC3-HOLSTEIN'],
        next_action_respects_unreceived_tasks=after['next_task']==(after['awaiting_runtime'][0] if after['awaiting_runtime'] else 'SC2-TESCHEN') and oldtasks['SC2-TESCHEN']==next(t for t in state['tasks'] if t['id']=='SC2-TESCHEN'))
    final=dict(status='PASS' if all(assertions.values()) else 'FAIL',recorded_at=now(),task_ids=accepted,passed=sum(assertions.values()),total=len(assertions),checks=assertions,
        failed=[n for n,ok in assertions.items() if not ok],progress_before=b['progress'],progress_after=after,old_proofs_changed=altered,tracker_functions_changed=fnchanges,
        functional_files_written=[],vanilla_files_written=[],git_write_operations=[],automated_engine_test=False)
    dump('FINAL_CHECKS.json',final);assert final['status']=='PASS',final['failed']
    path=rm.OUT/'ROADMAP_STATE.json';raw=path.read_bytes();assert load(path)==state,'Concurrent state change during checks; reread'
    state['events'].append(dict(id=event_id(state),date='2026-10-27',kind='SIX_RECEIPTS_FINAL_CHECKS_AND_CLOSURE_PREPARATION',scope_version=state['scope_version'],source=PREFIX+'FINAL_CHECKS.json',changes=[],
        before_weight=after['earned_weight'],after_weight=after['earned_weight'],total_weight=after['total_weight'],before_percent=after['percent'],after_percent=after['percent'],
        note='Six reçus indépendants ; conservation finale '+str(sum(r['passed'] for r in checks.values()))+'/'+str(sum(r['total'] for r in checks.values()))+' ; '+str(tests['passed'])+' tests réussis et '+str(len(tests['skipped']))+' contrôle initial désactivé. Ancien validateur des réformes : assertion de structure et StopIteration archivés, dépendances antérieures inchangées, contrats actuels réussis. Les 23 blocages sont conservés ; Teschen, Frise méridionale et Ortenbourg seulement proposés. Aucun nouveau sous-lot ni fichier fonctionnel modifié.'))
    assert path.read_bytes()==raw;rm.write_json(path,state);rm.render()
    dump('CANONICAL_CHECK.json',rm.check())
    dump('DELIVERY_MANIFEST.json',dict(recorded_at=now(),artifacts_sha256={rel(p):sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'},
        receipt_sha256={rel(receipt_path(t)):sha(receipt_path(t)) for t in accepted},tracking_sha256={rel(rm.OUT/n):sha(rm.OUT/n) for n in VIEWS+['ROADMAP_STATE.json']},
        tools_sha256={rel(p):sha(p) for p in [Path(__file__),ROOT/'tools/serg_closure_roadmap.py']},functional_files_written=[],automated_engine_test=False))
    print('FINAL',final['status'],final['passed'],'/',final['total'],'progress',after['percent'],flush=True)


if __name__=='__main__': {'prepare':prepare,'recheck':recheck,'receive':receive,'finish':finish}[sys.argv[1]]()
