"""Scoped tracking and checks for Cleves/Upper Guelders; no human receipt."""
import ast
import copy
import json
import subprocess
import sys
import unittest

import serg_cleve_gueldre_mark as w
import serg_closure_roadmap as rm

NAMES = ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']
TARGET = 'SC5-PRUSSIAN-WEST'
REF = w.OUT.relative_to(w.ROOT).as_posix()


def track():
    assert w.load('VALIDATION.json')['status'] == 'PASS'
    old = w.load('BEFORE_ROADMAP_STATE.json')
    assert rm.load_json(w.CANON/'ROADMAP_STATE.json') == old
    for name in NAMES:
        assert (w.CANON/name).read_bytes() == (w.OUT/('BEFORE_'+name)).read_bytes(), 'Concurrent tracking: '+name
    assert (w.OUT/'REPORT.md').is_file()
    s = copy.deepcopy(old); t = next(t for t in s['tasks'] if t['id'] == TARGET)
    assert t['status'] == 'IN_PROGRESS' and t['priority'] == 'P1' and not t['depends_on']
    t['implementation_report'].append(REF+'/REPORT.md'); t['historical_sources'].append(REF+'/SOURCES.md')
    t['installed_lots'].append('SERG_CLOSURE/'+w.OUT.name)
    t['static_tests']['evidence'].append(REF+'/VALIDATION.json')
    t['static_tests']['status'] = 'PASS'
    for lot in w.load('GEOMETRY.json')['sub_lots']:
        t['installed_sub_lots'].append(dict(id=lot['id'], status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
            cells=lot['pixels'], classification='B_POLITICAL_GENERALISATION', attestation=None,
            scope='Noyau Venray/Horst/Sevenum–Straelen/Kessel, BEO→PRU' if lot['pixels']==53 else 'Complément nord Gennep/Middelaar–Afferden/Well, BEO→PRU'))
    # Preserve the previous precise scope; append explicit cumulative scopes.
    t['runtime_validation'].update(status='NOT_RUN', scopes=['PW-RAVENSBERG-B32','PW-GUELDRE-B53','PW-CLEVE-GUELDRE-NORTH-B19'],
        protocol=REF+'/PLAYER_TEST_PROTOCOL_GROUPED.md', deferred_until_prussia_finished_by_user=True)
    moved = w.load('PLAN.json')['moved_population']
    t['current_delivery_note'] = f'Complément occidental : 72 cellules BEO→PRU (53+19), {moved} habitants existants redistribués techniquement ; Clèves/Gueldre septentrionales et noyau Venray/Horst/Straelen. Mark et anciens noyaux conservés. Aucun bâtiment/PM/unité/locator déplacé. Sous-lots prêts au moteur, réception différée à la fin de la Prusse.'
    t['investigation_status'] = 'CLEVE_GUELDRE_MARK_BOUNDED_REVIEW_COMPLETED_TWO_B_CORES_INSTALLED'
    t['residual_uncertainty'] = 'Noyaux B partiels, pas de cadastre ni de restitution complète du partage. Venlo/Beesel restent BEO dans le jeu malgré leur souveraineté néerlandaise établie : réserve non approuvée, hors noyau PRU installé, titres impériaux à réconcilier avant correction NET. Franges Clèves/Mark/Berg, Emmerich et micro-enclaves non certifiées. Aucun reçu humain ; tests moteur différés.'
    t['next_bounded_action'] = 'Présenter les réserves occidentales pour arbitrage de périmètre V1 avant la réception moteur prussienne groupée. Ne pas lancer automatiquement une autre frontière, la Bavière, un micro-État ou les anciens recalages.'
    s['mission_status'] = 'CLEVE_GUELDRE_PARTIAL_B_CORES_INSTALLED_ENGINE_TESTS_DEFERRED'
    s['release_focus'].update(current_pass='CLEVE_GUELDRE_MARK', current_pass_status='PARTIAL_B_CORES_INSTALLED',
        current_delivery=REF+'/REPORT.md', continuation_authority='Utilisateur : continuer et vérifier les écarts restants entre Clèves, Gueldre et Mark.',
        next_implementation_candidate=None, next_pass_started=False, next_requested_pass=None,
        next_action='Réserves occidentales documentées ; arbitrage du périmètre V1 avant réception groupée, aucune nouvelle étape commencée.')
    s['runtime_validation_hold'].update(protocol=REF+'/PLAYER_TEST_PROTOCOL_GROUPED.md', next_implementation_candidate=None,
        scope_note='Anciennes obligations préservées ; PW-GUELDRE-B53 et PW-CLEVE-GUELDRE-NORTH-B19 ajoutés. Aucun reçu. Réception moteur groupée lorsque la Prusse sera prête selon le joueur ; les réserves historiques ne sont pas certifiées par un test moteur.')
    assert s['events'][-1]['id'] == 'SERG-RM-0069'
    before, after = rm.progress(old), rm.progress(s)
    assert (before['earned_weight'],before['total_weight'],before['qualified_tasks'],before['percent']) == (after['earned_weight'],after['total_weight'],after['qualified_tasks'],after['percent']) == (93,235,32,'39.57')
    s['events'].append(dict(id='SERG-RM-0070', date='2026-11-05', kind='CLEVE_GUELDRE_MARK_PARTIAL_B_INSTALLATION',
        scope_version='1.0.0', source=REF+'/REPORT.md', changes=[dict(task_id=TARGET,before='IN_PROGRESS',after='IN_PROGRESS')],
        before_weight=93,after_weight=93,total_weight=235,before_percent='39.57',after_percent='39.57',
        note=f'72 cellules BEO→PRU : Gueldre B53 et complément nord B19 ; {moved} habitants existants redistribués techniquement. Un RGB ajouté, 598→599 titres, même étendue impériale, mêmes membres et neuf électeurs. Mark, Clèves existantes, Ravensberg et toutes les installations antérieures préservés ; bâtiments/PM/unités/locators inchangés. Venlo/Beesel et franges non clôturés. Deux sous-lots prêts au moteur, aucun point ni reçu ; essais différés à la fin de la Prusse. Aucune autre étape lancée.',
        evidence=[REF+'/'+n for n in ['SOURCES.md','GEOMETRY.json','INSTALLATION.json','VALIDATION.json','PLAYER_TEST_PROTOCOL_GROUPED.md']]))
    intro = f'''## Clèves / Gueldre / Mark — complément occidental installé, 5 novembre 2026

**72 cellules BEO→PRU, catégorie B** : noyau Gueldre `PW-GUELDRE-B53` **53**, complément nord `PW-CLEVE-GUELDRE-NORTH-B19` **19**. **{moved} habitants existants redistribués techniquement**, pas un recensement. Une subdivision, 598→599 titres impériaux, même étendue physique, mêmes membres et neuf électeurs. Roermond et 165 cellules du parent BEO restent BEO. Clèves et Mark existantes, Ravensberg/Minden, anciens noyaux et travaux concurrents conservés ; aucun bâtiment, PM, unité ou locator déplacé. [Rapport]({w.OUT.name}/REPORT.md), [avant/après]({w.OUT.name}/BEFORE_AFTER.png), [sources et limites]({w.OUT.name}/SOURCES.md).

`SC5-PRUSSIAN-WEST` reste **IN_PROGRESS** ; deux nouveaux sous-lots **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. **93/235 = 39,57 %, 32/81**, aucun reçu humain ni point nouveau. **Venlo/Beesel restent une réserve réelle : leur attribution BEO actuelle n'est pas approuvée comme historiquement correcte.** Franges de Clèves/Mark/Berg non certifiées ; aucune précision cadastrale revendiquée.

Les tests moteur restent reportés à la fin de la Prusse par le joueur : [protocole groupé cumulatif]({w.OUT.name}/PLAYER_TEST_PROTOCOL_GROUPED.md). Prochaine action : présenter les réserves occidentales pour arbitrage du périmètre V1 avant cette réception ; aucune nouvelle frontière, Bavière ou micro-État commencé. Les encadrés plus anciens ci-dessous sont des archives de priorité.

'''
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        original = (w.OUT/('BEFORE_'+name)).read_bytes(); head, body = original.split(b'\n',1)
        if name == 'NEXT_ACTION.md':
            head = '# Prochaine action — réserves occidentales et réception prussienne groupée'.encode('utf8')
        assert (w.CANON/name).read_bytes() == original
        (w.CANON/name).write_bytes(head+b'\n\n'+intro.encode('utf8')+body)
    history = (w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()
    addition = f'''\n\n## SERG-RM-0070 — 5 novembre 2026 — Clèves/Gueldre, B53 et B19 installés

SC5-PRUSSIAN-WEST reste IN_PROGRESS. Relecture bornée Clèves/Gueldre/Mark : 72 cellules BEO→PRU, noyau Gueldre 53 et complément nord Gennep/Middelaar–Afferden/Well 19 ; {moved} habitants existants redistribués techniquement avec conservation des profils et du total mondial. Un RGB supplémentaire, 598→599 titres, même étendue impériale et neuf électeurs. Mark, noyaux Clèves/PRU existants, Ravensberg, Glatz/Silésie et corrections antérieures préservés. Aucun bâtiment/PM/unité/locator déplacé. Venlo/Beesel et les franges régionales restent ouverts, sans approbation de leur attribution actuelle. Deux sous-lots IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; aucun reçu ni point : 93/235, 39,57 %, 32/81. Tests moteur toujours différés à la fin de la Prusse. Prochain arbitrage de périmètre V1 identifié ; aucune deuxième étape ou Bavière lancée. [Rapport]({w.OUT.name}/REPORT.md).
'''
    assert (w.CANON/'PROGRESS_HISTORY.md').read_bytes() == history
    (w.CANON/'PROGRESS_HISTORY.md').write_bytes(history+addition.encode('utf8'))
    assert rm.load_json(w.CANON/'ROADMAP_STATE.json') == old
    rm.write_json(w.CANON/'ROADMAP_STATE.json',s); rm.write_json(w.CANON/'PROGRESS_SNAPSHOT.json',rm.progress(s))
    print('SERG-RM-0070; partial READY; 93/235, 39.57%; no human receipt')


def tests():
    modules = ['test_serg_closure_roadmap','test_map2l_registry','test_map2l_runtime_receipt','test_map_georeference','test_serg_versioned_receipts']
    suite = unittest.TestLoader().loadTestsFromNames(modules)
    with (w.OUT/'TEST_RESULTS_RAW.txt').open('w',encoding='utf8') as stream:
        result = unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    w.dump('TEST_RESULTS.json',dict(status='PASS' if result.wasSuccessful() else 'FAIL',
        command='python -B -X utf8 tools/serg_cleve_gueldre_tracking.py tests',modules=modules,
        tests_run=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
        skipped=[dict(test=str(t),reason=reason) for t,reason in result.skipped],
        failures=[dict(test=str(t),traceback=msg) for t,msg in result.failures],errors=[dict(test=str(t),traceback=msg) for t,msg in result.errors],
        engine_test=False,prior_results_reused=False))
    print('Tests',result.testsRun,'run;',len(result.skipped),'skipped; PASS=',result.wasSuccessful())
    assert result.wasSuccessful()


def final():
    old = w.load('BEFORE_ROADMAP_STATE.json'); s = rm.load_json(w.CANON/'ROADMAP_STATE.json')
    checks = []
    def ck(n,v):
        checks.append(dict(name=n,status='PASS' if v else 'FAIL'))
    t = next(t for t in s['tasks'] if t['id']==TARGET); previous = next(t for t in old['tasks'] if t['id']==TARGET)
    ck('static_installation_validation',w.load('VALIDATION.json')['status']=='PASS')
    ck('80_other_tasks_preserved',[t for t in s['tasks'] if t['id']!=TARGET]==[t for t in old['tasks'] if t['id']!=TARGET])
    ck('all_old_events_preserved',s['events'][:-1]==old['events'] and s['events'][-1]['id']=='SERG-RM-0070')
    ck('old_installed_sub_lots_preserved',t['installed_sub_lots'][:-2]==previous['installed_sub_lots'])
    ck('partial_ready_without_receipt',t['status']=='IN_PROGRESS' and all(z['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and z['attestation'] is None for z in t['installed_sub_lots'][-2:]) and t['runtime_validation']['status']=='NOT_RUN' and t['runtime_validation']['attestation'] is None)
    ck('old_root_receipts_preserved',all(s[k]==old[k] for k in old if k not in {'tasks','events','mission_status','release_focus','runtime_validation_hold'}))
    ck('history_additive',(w.CANON/'PROGRESS_HISTORY.md').read_bytes().startswith((w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()))
    ck('engine_tests_deferred',s['runtime_validation_hold']['deferred_until_prussia_finished_by_user'] and s['runtime_validation_hold']['does_not_block_implementation'])
    ck('no_next_pass_started',not s['release_focus']['next_pass_started'] and not s['release_focus']['bavaria_started'])
    p = rm.progress(s)
    ck('scope_progress_unchanged',(p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['total_tasks'],p['percent'])==(93,235,32,81,'39.57') and s['scope_version']=='1.0.0')
    result = rm.check(); w.dump('CANONICAL_CHECK.json',result); ck('canonical_validator',result['status']=='PASS')
    ck('targeted_tests',w.load('TEST_RESULTS.json')['status']=='PASS')
    installed = [r['file'] for r in w.load('INSTALLATION.json')['changes']]
    scripts = ['tools/serg_cleve_gueldre_mark.py','tools/serg_cleve_gueldre_tracking.py']
    paths = installed+scripts+[(w.CANON/n).relative_to(w.ROOT).as_posix() for n in NAMES]
    diff = subprocess.run(['git','--no-optional-locks','diff','--check','--',*paths],cwd=w.ROOT,capture_output=True,text=True)
    w.dump('DIFF_CHECK.json',dict(exit_code=diff.returncode,stdout=diff.stdout,stderr=diff.stderr)); ck('diff_check',diff.returncode==0)
    ck('new_tools_parse',all(ast.parse((w.ROOT/rel).read_text(encoding='utf8')) for rel in scripts))
    now = w.prior.runtime(); baseline = w.load('BASELINE.json')['runtime']
    drift = sorted(p for p in set(now)|set(baseline) if now.get(p)!=baseline.get(p) and p not in installed)
    w.dump('CONCURRENT_CHANGES.json',dict(unexpected_functional_drift=drift,changed_functional_files=[r for r in installed if r in now],other_mod_copy_untouched=True,vanilla_writes=False,git_writes=False))
    ck('concurrent_functional_work_preserved',not drift)
    w.dump('FILES_MODIFIED.json',dict(installed=w.load('INSTALLATION.json')['changes'],new_tools=[dict(file=p,sha256=w.sha(w.ROOT/p)) for p in scripts],tracking=[dict(file=(w.CANON/n).relative_to(w.ROOT).as_posix(),sha256=w.sha(w.CANON/n)) for n in NAMES],new_evidence_directory=REF,old_reports_modified=False))
    w.dump('FINAL_CHECKS.json',dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,
        passed=sum(c['status']=='PASS' for c in checks),total=len(checks),progress=p,new_human_receipts=0,engine_test=False))
    print('Final',len(checks),'checks;', [c for c in checks if c['status']!='PASS'])
    assert all(c['status']=='PASS' for c in checks)


if __name__ == '__main__':
    {'track':track,'tests':tests,'final':final}[sys.argv[1]]()
