"""Scoped tracking and checks for Cleves/Upper Guelders; no human receipt."""
import ast
import copy
import json
import subprocess
import sys
import unittest

import serg_western_reserves as w
import serg_closure_roadmap as rm

NAMES = ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']
TARGET = 'SC5-PRUSSIAN-WEST'
REF = w.OUT.relative_to(w.ROOT).as_posix()


def track():
    assert w.load('VALIDATION.json')['status']=='PASS'
    old=w.load('BEFORE_ROADMAP_STATE.json')
    assert rm.load_json(w.CANON/'ROADMAP_STATE.json')==old
    for name in NAMES:
        assert (w.CANON/name).read_bytes()==(w.OUT/('BEFORE_'+name)).read_bytes(),'Concurrent tracking: '+name
    assert (w.OUT/'REPORT.md').is_file()
    s=copy.deepcopy(old);t=next(t for t in s['tasks'] if t['id']==TARGET)
    assert t['status']=='IN_PROGRESS' and t['priority']=='P1' and not t['depends_on']
    t['implementation_report'].append(REF+'/REPORT.md');t['historical_sources'].append(REF+'/SOURCES_AND_ARBITRATION.md')
    t['installed_lots'].append('SERG_CLOSURE/'+w.OUT.name)
    t['static_tests']['status']='PASS';t['static_tests']['evidence'].append(REF+'/VALIDATION.json')
    for lot in w.load('GEOMETRY.json')['sub_lots']:
        t['installed_sub_lots'].append(dict(id=lot['id'],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',cells=lot['pixels'],classification='B_POLITICAL_GENERALISATION',attestation=None,scope='Noyau néerlandais de Venlo, BEO→NET' if 'VENLO' in lot['id'] else 'Bande néerlandaise Beesel/Belfeld, BEO→NET'))
    t['runtime_validation']['scopes']+=['PW-VENLO-NET-B4','PW-BEESEL-NET-B4']
    t['runtime_validation'].update(status='NOT_RUN',protocol=REF+'/PLAYER_TEST_PROTOCOL_GROUPED.md',deferred_until_prussia_finished_by_user=True)
    t['western_arbitration']=dict(status='AGENT_DECISION_UNDER_USER_DELEGATION',evidence=REF+'/ARBITRATION.json',runtime_human_attestation=None,terminal_approval=False)
    t['current_delivery_note']='Réserves occidentales arbitrées : Venlo 4 et Beesel/Belfeld 4 cellules BEO→NET ; 1 171 habitants existants redistribués techniquement. Aucun droit BEO de restitution sur ces noyaux ; aucun titre ou membre NET ajouté, 599 titres inchangés, étendue enregistrée réduite de 8 cellules. Clèves/Mark/Berg conservés en B pour la V1, aucune ancienne cellule PRU touchée. Aucun bâtiment/PM/unité/locator modifié.'
    t['investigation_status']='WESTERN_RESERVES_ARBITRATED_FOR_V1_READY_FOR_GROUPED_RUNTIME'
    t['residual_uncertainty']='Arbitrage V1 borné, pas une certification cadastrale ou une réception régionale complète. Franges Emmerich, Unna/Meinerzhagen et Berg conservées en B ; ancien candidat Berg non démontré écarté. Venlo/Beesel représentés par noyaux B, pas tout Staats-Opper-Gelre. Obligations historiques intégrales non effacées ; aucune validation humaine ni point acquis. Tests groupés différés selon le joueur.'
    t['next_bounded_action']='Réception moteur groupée des installations prussiennes et des deux noyaux néerlandais. Aucune nouvelle frontière, Bavière ou relance automatique de précision.'
    s['mission_status']='WESTERN_RESERVES_ARBITRATED_DUTCH_CORES_INSTALLED_ENGINE_TESTS_DEFERRED'
    s['release_focus'].update(current_pass='WESTERN_RESERVES_ARBITRATION',current_pass_status='WESTERN_V1_ARBITRATION_COMPLETED_RUNTIME_PENDING',current_delivery=REF+'/REPORT.md',continuation_authority='Utilisateur : Continue sur ta lancée, arbitre les réserves occidentales.',next_implementation_candidate=None,next_pass_started=False,next_requested_pass=None,next_action='Prochaine action : réception moteur prussienne groupée lorsque le joueur sera prêt ; aucun nouveau territoire lancé.',western_arbitration=REF+'/ARBITRATION.json')
    s['runtime_validation_hold'].update(protocol=REF+'/PLAYER_TEST_PROTOCOL_GROUPED.md',next_implementation_candidate=None,scope_note='Sous-lots antérieurs préservés ; deux noyaux NET ajoutés. Les réserves occidentales de précision sont arbitrées pour la V1 sans clôture régionale fictive. Réception groupée au rythme du joueur ; aucun reçu nouveau.')
    assert s['events'][-1]['id']=='SERG-RM-0070'
    before,after=rm.progress(old),rm.progress(s)
    assert (before['earned_weight'],before['total_weight'],before['qualified_tasks'],before['percent'])==(after['earned_weight'],after['total_weight'],after['qualified_tasks'],after['percent'])==(93,235,32,'39.57')
    s['events'].append(dict(id='SERG-RM-0071',date='2026-11-05',kind='WESTERN_RESERVES_ARBITRATION_DUTCH_CORES_INSTALLATION',scope_version='1.0.0',source=REF+'/REPORT.md',changes=[dict(task_id=TARGET,before='IN_PROGRESS',after='IN_PROGRESS')],before_weight=93,after_weight=93,total_weight=235,before_percent='39.57',after_percent='39.57',note='Arbitrage délégué par le joueur : maintenir Clèves/Mark/Berg en B pour la V1 sans garantie cadastrale ; ne pas installer le candidat Berg non démontré. Venlo 4 et Beesel/Belfeld 4 cellules BEO→NET, 1 171 habitants existants redistribués ; aucun nouveau pays, titre NET ou membre impérial. 599 titres inchangés, domaine enregistré de restitution réduit exactement de 8 cellules pour ne pas restituer ces possessions néerlandaises à BEO. Tous les noyaux PRU et travaux antérieurs préservés. Deux nouveaux sous-lots prêts au moteur ; aucun reçu ou point, prochaine réception groupée uniquement.',evidence=[REF+'/'+n for n in ['SOURCES_AND_ARBITRATION.md','ARBITRATION.json','GEOMETRY.json','INSTALLATION.json','VALIDATION.json','PLAYER_TEST_PROTOCOL_GROUPED.md']]))
    intro="## Réserves occidentales — arbitrage V1 et noyaux néerlandais, 5 novembre 2026\n\n**Arbitrage délégué exécuté : maintien Clèves/Mark/Berg en approximation B pour la V1, sans certification cadastrale.** L'ancien candidat Berg de 39 cellules n'est pas installé ; aucun recalage relancé. **Venlo 4 et Beesel/Belfeld 4 cellules BEO→NET**, deux sous-lots prêts au moteur ; 1 171 habitants existants redistribués techniquement. Aucune ancienne cellule PRU, bâtiment, PM, unité ou locator changé. Roermond et 157 cellules du parent restent BEO. [Rapport](WESTERN_RESERVES_ARBITRATION_2026_11_05/REPORT.md), [arbitrage et sources](WESTERN_RESERVES_ARBITRATION_2026_11_05/SOURCES_AND_ARBITRATION.md), [avant/après](WESTERN_RESERVES_ARBITRATION_2026_11_05/BEFORE_AFTER.png).\n\n**599 titres impériaux inchangés**, même liste de membres et neuf électeurs. Le domaine enregistré de restitution perd exactement les huit cellules NET : aucun droit BEO sur ces noyaux, aucun titre ou membre NET créé. `SC5-PRUSSIAN-WEST` reste **IN_PROGRESS** ; aucune validation humaine ou clôture régionale implicite. **93/235 = 39,57 %, 32/81**, inchangés.\n\n**Prochaine action : [réception moteur prussienne groupée](WESTERN_RESERVES_ARBITRATION_2026_11_05/PLAYER_TEST_PROTOCOL_GROUPED.md), lorsque le joueur sera prêt.** Le report des essais reste en vigueur ; aucune autre frontière, Bavière ou micro-État lancé. Les limites historiques intégrales restent déclarées, sans recherche de précision automatique. Les encadrés antérieurs conservent leur valeur d'archive.\n\n"
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        original=(w.OUT/('BEFORE_'+name)).read_bytes();head,body=original.split(b'\n',1)
        if name=='NEXT_ACTION.md':head='# Prochaine action — réception prussienne groupée ; réserves occidentales arbitrées'.encode('utf8')
        assert (w.CANON/name).read_bytes()==original
        (w.CANON/name).write_bytes(head+b'\n\n'+intro.encode('utf8')+body)
    history=(w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()
    addition="\n\n## SERG-RM-0071 — 5 novembre 2026 — Réserves occidentales arbitrées pour la V1\n\nSur autorisation explicite d'arbitrer, maintien actuel Clèves/Mark/Berg en catégorie B, sans certification des franges ni installation du candidat Berg non démontré. Deux noyaux néerlandais corrigés : Venlo 4 et Beesel/Belfeld 4 cellules BEO→NET ; 1 171 habitants existants redistribués techniquement, profils et total mondial conservés. Deux nouvelles provinces, aucun pays nouveau. Les 599 titres impériaux restent identiques ; leur domaine enregistré perd exactement ces huit cellules, sans droit BEO de restitution ni adhésion nationale NET. Roermond, tous les anciens noyaux PRU, bâtiments/PM/unités/locators et travaux concurrents préservés. SC5-PRUSSIAN-WEST reste IN_PROGRESS, deux sous-lots IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; aucune réception humaine ni point : 93/235, 39,57 %, 32/81. Prochaine action : test joueur prussien groupé lorsque le joueur sera prêt, sans nouveau territoire. [Rapport](WESTERN_RESERVES_ARBITRATION_2026_11_05/REPORT.md).\n"
    assert (w.CANON/'PROGRESS_HISTORY.md').read_bytes()==history
    (w.CANON/'PROGRESS_HISTORY.md').write_bytes(history+addition.encode('utf8'))
    assert rm.load_json(w.CANON/'ROADMAP_STATE.json')==old
    rm.write_json(w.CANON/'ROADMAP_STATE.json',s);rm.write_json(w.CANON/'PROGRESS_SNAPSHOT.json',rm.progress(s))
    print('SERG-RM-0071; western arbitration, partial READY; 93/235, no human receipt')


def tests():
    modules = ['test_serg_closure_roadmap','test_map2l_registry','test_map2l_runtime_receipt','test_map_georeference','test_serg_versioned_receipts']
    suite = unittest.TestLoader().loadTestsFromNames(modules)
    with (w.OUT/'TEST_RESULTS_RAW.txt').open('w',encoding='utf8') as stream:
        result = unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    w.dump('TEST_RESULTS.json',dict(status='PASS' if result.wasSuccessful() else 'FAIL',
        command='python -B -X utf8 tools/serg_western_reserves_tracking.py tests',modules=modules,
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
    ck('all_old_events_preserved',s['events'][:-1]==old['events'] and s['events'][-1]['id']=='SERG-RM-0071')
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
    scripts = ['tools/serg_western_reserves.py','tools/serg_western_reserves_tracking.py']
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
