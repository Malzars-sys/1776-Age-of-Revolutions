"""Track the scoped Magdeburg/Saale delivery, without human validation."""
import copy
import json
import subprocess
import sys
import unittest

import serg_magdeburg_halberstadt as w
import serg_closure_roadmap as rm


def track():
    assert w.load('VALIDATION.json')['status']=='PASS'
    old=w.load('BEFORE_ROADMAP_STATE.json');s=rm.load_json(w.CANON/'ROADMAP_STATE.json')
    assert s==old,'Concurrent tracking changes must be reconciled'
    assert (w.OUT/'REPORT.md').exists()
    s=copy.deepcopy(s);ref=w.OUT.relative_to(w.ROOT).as_posix()
    target='SC3-BRANDENBURG';t=next(t for t in s['tasks'] if t['id']==target)
    assert t['status']=='BLOCKED' and t['priority']=='P1' and not t['depends_on']
    t['status']='IN_PROGRESS';t.pop('blocking_reason',None)
    t['implementation_report'].append(ref+'/REPORT.md');t['historical_sources'].append(ref+'/SOURCES.md')
    t['installed_lots'].append('SERG_CLOSURE/'+w.OUT.name)
    t['static_tests']=dict(status='PASS',evidence=t['static_tests']['evidence']+[ref+'/VALIDATION.json'])
    for lot in w.load('GEOMETRY.json')['sub_lots']:
        t['installed_sub_lots'].append(dict(id=lot['id'],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',cells=lot['pixels'],classification='B_POLITICAL_GENERALISATION',scope='Mersebourg/Querfurt/Weißenfels/Naumbourg' if lot['id']=='MH-SAALE-CORE' else 'Office de Gommern ; Barby non clôturé',attestation=None))
    t['runtime_validation'].update(status='NOT_RUN',protocol=ref+'/PLAYER_TEST_PROTOCOL_GROUPED.md',deferred_until_prussia_finished_by_user=True)
    t['runtime_validation']['scopes']+=['MH-SAALE-CORE','MH-GOMMERN-CORE']
    t['installed_delivery_status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    t['current_delivery_note']='77 cellules PRU→SAX : Saale 69, Gommern 8 ; 23 202 habitants existants réaffectés techniquement. Halle/Magdebourg/Halberstadt et tous les noyaux non PRU conservés. Bâtiments, PM, unités et anciennes installations inchangés. Deux sous-lots prêts au moteur, aucun reçu.'
    t['residual_uncertainty']='Noyaux politiques B partiels, pas cadastre ni recensement. Barby recoupe la représentation Anhalt protégée ; Mansfeld et la succession de 1780, les enclaves du Harz et les autres obligations régionales restent ouverts. Fragment PRU ancien de 11 cellules conservé sans certification. Tests moteur différés par le joueur.'
    t['next_bounded_action']='Tri des seuls gros écarts prussiens restants en Gueldre/Clèves/Mark, sans relancer automatiquement les anciens recalages ou micro-enclaves. Tests moteur groupés à la fin de la Prusse ; aucune Bavière commencée.'
    s['mission_status']='MAGDEBURG_SAALE_GOMMERN_CORES_INSTALLED_ENGINE_TESTS_DEFERRED'
    s['release_focus'].update(current_pass='MAGDEBURG_HALBERSTADT',current_pass_status='PARTIAL_B_CORES_INSTALLED',current_delivery=ref+'/REPORT.md',continuation_authority='Utilisateur : Okvaziñ, après la proposition Magdebourg/Halberstadt et interfaces Saxe/Anhalt.',next_implementation_candidate='SC5-PRUSSIAN-WEST (tri des grands écarts résiduels uniquement)',next_pass_started=False,next_requested_pass=None,next_action='Tri prussien occidental recommandé, non commencé ; réception moteur groupée à la fin de la Prusse.')
    s['runtime_validation_hold'].update(protocol=ref+'/PLAYER_TEST_PROTOCOL_GROUPED.md',next_implementation_candidate='SC5-PRUSSIAN-WEST',scope_note='Sous-lots antérieurs conservés ; MH-SAALE-CORE et MH-GOMMERN-CORE ajoutés. Maintien Glatz/Silésie approuvé séparément ; aucune réception moteur. Tests différés jusqu’à la fin de la Prusse, sans bloquer les travaux autorisés.')
    before=rm.progress(old);after=rm.progress(s)
    assert (before['earned_weight'],before['total_weight'],before['qualified_tasks'],before['percent'])==(after['earned_weight'],after['total_weight'],after['qualified_tasks'],after['percent'])==(93,235,32,'39.57')
    assert s['events'][-1]['id']=='SERG-RM-0068'
    s['events'].append(dict(id='SERG-RM-0069',date='2026-11-05',kind='MAGDEBURG_SAALE_GOMMERN_PARTIAL_B_INSTALLATION',scope_version='1.0.0',source=ref+'/REPORT.md',changes=[dict(task_id=target,before='BLOCKED',after='IN_PROGRESS')],before_weight=93,after_weight=93,total_weight=235,before_percent='39.57',after_percent='39.57',note='77 cellules PRU→SAX, Saale 69 et Gommern 8 ; trois subdivisions, 595→598 titres et même étendue impériale. 23 202 habitants existants redistribués techniquement. Noyaux Anhalt/Saxe/Thuringe, Glatz/Silésie et autres corrections préservés. Deux sous-lots prêts au moteur, tests différés à la fin de la Prusse. Barby/Mansfeld et obligations régionales non clôturés ; aucun point ou reçu humain. Prochaine candidate occidentale identifiée, non commencée.',evidence=[ref+'/'+n for n in ['SOURCES.md','GEOMETRY.json','INSTALLATION.json','VALIDATION.json','PLAYER_TEST_PROTOCOL_GROUPED.md']]))
    intro='''## Magdebourg / Saale / Gommern — deux noyaux installés, 5 novembre 2026

**77 cellules PRU→SAX, catégorie B** : `MH-SAALE-CORE` **69** autour de Mersebourg/Querfurt/Weißenfels/Naumbourg ; `MH-GOMMERN-CORE` **8**. Halle, Magdebourg et Halberstadt restent PRU. Tous les noyaux non prussiens et les corrections antérieures sont conservés. **23 202 habitants existants réaffectés techniquement**, pas un recensement. Bâtiments, PM, unités et locators physiques inchangés. [Rapport](MAGDEBURG_HALBERSTADT_2026_11_05/REPORT.md), [avant/après](MAGDEBURG_HALBERSTADT_2026_11_05/BEFORE_AFTER.png), [sources](MAGDEBURG_HALBERSTADT_2026_11_05/SOURCES.md).

`SC3-BRANDENBURG` : **IN_PROGRESS**, deux nouveaux sous-lots **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Barby, Mansfeld et les autres franges non démontrées restent ouverts. 595→598 titres impériaux, même étendue physique, mêmes membres et neuf électeurs. **93/235 = 39,57 %, 32/81**, aucun reçu ni point nouveau.

**Tests moteur regroupés à la fin de la Prusse**, selon le joueur : [protocole groupé](MAGDEBURG_HALBERSTADT_2026_11_05/PLAYER_TEST_PROTOCOL_GROUPED.md). Le maintien approuvé de Glatz/Silésie est conservé et ne vaut pas test des nouvelles installations. Prochaine candidate : tri des grands écarts résiduels de Gueldre/Clèves/Mark, sans relancer automatiquement les anciens recalages occidentaux ou micro-États. Candidate identifiée, non commencée ; aucune Bavière. Les encadrés antérieurs sont des archives de priorité.

'''
    names=['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']
    for name in names:assert (w.CANON/name).read_bytes()==(w.OUT/('BEFORE_'+name)).read_bytes(),'Concurrent '+name
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        original=(w.OUT/('BEFORE_'+name)).read_bytes();head,body=original.split(b'\n',1);text=body.decode('utf8')
        if name=='NEXT_ACTION.md':head='# Prochaine action — finitions visibles prussiennes ; Saale et Gommern prêts au moteur'.encode('utf8')
        if name=='ROADMAP.md':
            start=text.index('#### SC3-BRANDENBURG');end=text.index('#### SC3-SILESIA-LUSATIA',start)
            section=text[start:end];assert section.count('`BLOCKED`')==1
            text=text[:start]+section.replace('`BLOCKED`','`IN_PROGRESS`')+text[end:]
        if name=='BLOCKERS.md':
            lines=text.splitlines(keepends=True)
            for i,line in enumerate(lines):
                if line.startswith('- SC3-BRANDENBURG : '):lines[i]='- SC3-BRANDENBURG : IN_PROGRESS ; Saale 69 et Gommern 8 installés, prêts au moteur ; Barby/Mansfeld et obligations régionales encore ouverts. Voir MAGDEBURG_HALBERSTADT_2026_11_05.\n'
            text=''.join(lines)
        assert (w.CANON/name).read_bytes()==original
        (w.CANON/name).write_bytes(head+b'\n\n'+intro.encode('utf8')+text.encode('utf8'))
    prior=(w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes();assert (w.CANON/'PROGRESS_HISTORY.md').read_bytes()==prior
    addition='''

## SERG-RM-0069 — 5 novembre 2026 — Saale et Gommern, deux noyaux saxons rétablis

SC3-BRANDENBURG BLOCKED→IN_PROGRESS. 77 cellules PRU→SAX, catégorie B : Saale 69 (Mersebourg/Querfurt/Weißenfels/Naumbourg), Gommern 8. Trois nouvelles provinces, même région économique ; 23 202 habitants existants réaffectés sans modifier leurs profils ou le total mondial. Halle/Magdebourg/Halberstadt, tous les noyaux non PRU et les anciennes corrections conservés. Aucun bâtiment/PM/unité/locator physique modifié. Trois titres ajoutés, 595→598, même étendue impériale et neuf électeurs. Barby, Mansfeld et les autres obligations régionales restent ouverts. Deux sous-lots IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; aucun reçu humain ni point : 93/235, 39,57 %, 32/81. Tests moteur toujours différés à la fin de la Prusse. Prochain tri occidental recommandé, non commencé ; aucune Bavière ou micro-État. [Rapport](MAGDEBURG_HALBERSTADT_2026_11_05/REPORT.md).
'''
    (w.CANON/'PROGRESS_HISTORY.md').write_bytes(prior+addition.encode('utf8'))
    assert rm.load_json(w.CANON/'ROADMAP_STATE.json')==old
    rm.write_json(w.CANON/'ROADMAP_STATE.json',s);rm.write_json(w.CANON/'PROGRESS_SNAPSHOT.json',rm.progress(s))
    print('SERG-RM-0069; partial READY; 93/235, 39.57%; no human receipt')


def tests():
    modules=['test_serg_closure_roadmap','test_map2l_registry','test_map2l_runtime_receipt','test_map_georeference','test_serg_versioned_receipts']
    suite=unittest.TestLoader().loadTestsFromNames(modules)
    with (w.OUT/'TEST_RESULTS_RAW.txt').open('w',encoding='utf8') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    w.dump('TEST_RESULTS.json',dict(status='PASS' if result.wasSuccessful() else 'FAIL',command='python -B -X utf8 tools/serg_magdeburg_tracking.py tests',modules=modules,tests_run=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),skipped=[dict(test=str(t),reason=reason) for t,reason in result.skipped],failures=[dict(test=str(t),traceback=msg) for t,msg in result.failures],errors=[dict(test=str(t),traceback=msg) for t,msg in result.errors],engine_test=False,prior_results_reused=False))
    print('Targeted tests',result.testsRun,'run;',len(result.skipped),'skipped; PASS=',result.wasSuccessful());assert result.wasSuccessful()


def final():
    old=w.load('BEFORE_ROADMAP_STATE.json');s=rm.load_json(w.CANON/'ROADMAP_STATE.json');checks=[]
    def ck(n,v):checks.append(dict(name=n,status='PASS' if v else 'FAIL'))
    target='SC3-BRANDENBURG';t=next(t for t in s['tasks'] if t['id']==target);previous=next(t for t in old['tasks'] if t['id']==target)
    ck('static_installation_validation',w.load('VALIDATION.json')['status']=='PASS')
    ck('80_other_tasks_preserved',[t for t in s['tasks'] if t['id']!=target]==[t for t in old['tasks'] if t['id']!=target])
    ck('all_old_events_preserved',s['events'][:-1]==old['events'] and s['events'][-1]['id']=='SERG-RM-0069')
    ck('old_installed_sub_lots_preserved',t['installed_sub_lots'][:-2]==previous['installed_sub_lots'])
    ck('partial_ready_without_human_receipt',t['status']=='IN_PROGRESS' and all(z['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and z['attestation'] is None for z in t['installed_sub_lots'][-2:]) and t['runtime_validation']['status']=='NOT_RUN' and t['runtime_validation']['attestation'] is None)
    ck('old_root_receipt_records_unchanged',all(s[k]==old[k] for k in old if k not in {'tasks','events','mission_status','release_focus','runtime_validation_hold'}))
    ck('history_additive',(w.CANON/'PROGRESS_HISTORY.md').read_bytes().startswith((w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()))
    ck('engine_tests_remain_deferred',s['runtime_validation_hold']['deferred_until_prussia_finished_by_user'] and s['runtime_validation_hold']['does_not_block_implementation'])
    p=rm.progress(s);ck('scope_and_progress_unchanged',(p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['total_tasks'],p['percent'])==(93,235,32,81,'39.57') and s['scope_version']=='1.0.0')
    result=rm.check();w.dump('CANONICAL_CHECK.json',result);ck('canonical_validator',result['status']=='PASS')
    ck('targeted_tests',w.load('TEST_RESULTS.json')['status']=='PASS')
    paths=[row['file'] for row in w.load('INSTALLATION.json')['changes']]+['tools/serg_magdeburg_halberstadt.py','tools/serg_magdeburg_tracking.py']+[str((w.CANON/n).relative_to(w.ROOT)) for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]
    args=['git','--no-optional-locks','diff','--check','--',*paths];diff=subprocess.run(args,cwd=w.ROOT,capture_output=True,text=True);w.dump('DIFF_CHECK.json',dict(command=args,exit_code=diff.returncode,stdout=diff.stdout,stderr=diff.stderr));ck('diff_check',diff.returncode==0)
    w.dump('FINAL_CHECKS.json',dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),progress=p,new_human_receipts=0,engine_test=False))
    print('Final',len(checks),'checks;', [c for c in checks if c['status']!='PASS']);assert all(c['status']=='PASS' for c in checks)


if __name__=='__main__':
    {'track':track,'tests':tests,'final':final}[sys.argv[1]]()
