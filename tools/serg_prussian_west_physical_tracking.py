"""Track the authorized political B core; never manufacture a human receipt."""
import copy,json,subprocess,sys
import serg_prussian_west_physical as w
import serg_closure_roadmap as rm

def tracker():
    assert w.load('VALIDATION.json')['status']=='PASS'
    old=w.load('BEFORE_ROADMAP_STATE.json');s=rm.load_json(w.CANON/'ROADMAP_STATE.json');assert s==old,'Concurrent tracking change; reconcile before writing'
    s=copy.deepcopy(s);ref=w.OUT.relative_to(w.ROOT).as_posix();t=next(t for t in s['tasks'] if t['id']=='SC5-PRUSSIAN-WEST');assert t['status']=='BLOCKED'
    t['status']='IN_PROGRESS';t['implementation_report'].append(ref+'/REPORT.md');t['historical_sources'].append(ref+'/SOURCES.md');t['installed_lots'].append('SERG_CLOSURE/'+w.OUT.name)
    t['static_tests']=dict(status='PASS',evidence=t['static_tests']['evidence']+[ref+'/VALIDATION.json'])
    t['installed_delivery_status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    t['installed_sub_lots']=[dict(id='PW-RAVENSBERG-B32',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',cells=32,classification='B_POLITICAL_GENERALISATION',scope='Noyau partiel : 9 SCM, 6 WPM et 17 HAN vers PRU ; WPO, Lippe et anciennes cellules PRU conservées',attestation=None)]
    t['runtime_validation'].update(status='NOT_RUN',scope='PW-RAVENSBERG-B32',protocol=ref+'/PLAYER_TEST_PROTOCOL_GROUPED.md',deferred_until_prussia_finished_by_user=True)
    t.pop('blocking_reason',None)
    t['investigation_status']='BOUNDED_PHYSICAL_ATTEMPT_COMPLETED_POLITICAL_B_CORE_INSTALLED'
    t['current_delivery_note']='32 cellules PRU supplémentaires, 11 559 habitants existants réaffectés ; aucun bâtiment ou unité déplacé. Six repères physiques favorisent R5 pour une approximation B ; nouvel affine rejeté. Test moteur différé par le joueur à la fin de la Prusse.'
    t['residual_uncertainty']='Noyau partiel B, pas de cadastre ni de restitution complète de Ravensberg, Clèves ou Gueldre. Les franges protégées et le découpage entier de 1713 ne sont pas certifiés. Aucune réception humaine.'
    t['next_bounded_action']='Passer à une autre frontière prussienne ; candidate Glatz/Silésie. Ne pas relancer automatiquement la recherche de précision occidentale. Regrouper les tests moteur à la fin de la Prusse.'
    s['mission_status']='PRUSSIAN_WEST_B32_INSTALLED_ENGINE_TESTS_DEFERRED_UNTIL_PRUSSIA_FINISHED'
    s['release_focus'].update(current_pass='PRUSSIAN_WEST_PHYSICAL_ANCHORS',current_pass_status='PARTIAL_B_CORE_INSTALLED',current_delivery=ref+'/REPORT.md',continuation_authority='Utilisateur : essayer les repères ; si la précision bloque, donner des cellules à la Prusse puis passer à une autre frontière.',engine_tests_deferred_until_prussia_finished=True,western_precision_search_stopped_for_this_pass=True,next_implementation_candidate='SC3-SILESIA-LUSATIA (Glatz/frontière silésienne)',next_requested_pass=None,next_pass_started=False)
    hold=s['runtime_validation_hold'];hold['pending_task_ids']=list(dict.fromkeys(hold['pending_task_ids']+['SC5-PRUSSIAN-WEST']));hold.update(protocol=ref+'/PLAYER_TEST_PROTOCOL_GROUPED.md',reason='Instruction du joueur : tous les tests moteur seront effectués lorsque la Prusse sera finie ; cette attente ne bloque pas les corrections indépendantes autorisées.',deferred_until_prussia_finished_by_user=True,does_not_block_implementation=True,next_implementation_candidate='SC3-SILESIA-LUSATIA',scope_note='Anciennes installations saxonnes et polono-prussiennes plus PW-RAVENSBERG-B32 ; aucun reçu nouveau. Candidate suivante identifiée, non commencée.')
    before=rm.progress(old);after=rm.progress(s);assert (before['earned_weight'],before['total_weight'],before['qualified_tasks'],before['percent'])==(after['earned_weight'],after['total_weight'],after['qualified_tasks'],after['percent'])==(93,235,32,'39.57')
    assert s['events'][-1]['id']=='SERG-RM-0065'
    s['events'].append(dict(id='SERG-RM-0066',date='2026-11-05',kind='PRUSSIAN_WEST_PHYSICAL_READINGS_AND_B32_INSTALLATION',scope_version='1.0.0',source=ref+'/REPORT.md',changes=[dict(task_id=t['id'],before='BLOCKED',after='IN_PROGRESS')],before_weight=93,after_weight=93,total_weight=235,before_percent='39.57',after_percent='39.57',note='Six repères physiques identifiés ; R5 retenu seulement pour une approximation B, nouvel affine rejeté sur ses témoins. 32 cellules SCM/WPM/HAN vers PRU, 11 559 habitants techniques conservés, 595 titres impériaux et même étendue. Noyau partiel prêt au moteur ; tests différés par le joueur à la fin de la Prusse, aucun point ou reçu humain. Glatz/Silésie candidate non commencée.',evidence=[ref+'/PHYSICAL_ANCHORS.json',ref+'/GEOMETRY.json',ref+'/INSTALLATION.json',ref+'/VALIDATION.json',ref+'/PLAYER_TEST_PROTOCOL_GROUPED.md']))
    assert (w.CANON/'ROADMAP_STATE.json').read_bytes()==(w.OUT/'BEFORE_ROADMAP_STATE.json').read_bytes();rm.write_json(w.CANON/'ROADMAP_STATE.json',s)
    intro='''## Prusse occidentale — noyau B de Ravensberg installé, 5 novembre 2026

**PW-RAVENSBERG-B32 : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, 32 cellules SCM/WPM/HAN vers PRU. Six repères physiques comparés ; R5 retenu pour une approximation politique B, nouvel affine rejeté. Aucun ancien modèle modifié. Minden, Lingen, Tecklenburg, Osnabrück/WPO, Lippe et les anciennes cellules PRU conservés. [Rapport](PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05/REPORT.md), [avant/après](PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05/RAVENSBERG_BEFORE_AFTER.png).

`SC5-PRUSSIAN-WEST` reprend **IN_PROGRESS** : noyau partiel installé, région entière non clôturée. **93/235 = 39,57 %, 32/81**, aucun reçu humain ni point nouveau. Le registre compte 595 titres, même étendue impériale et neuf électeurs.

**Tests moteur différés par le joueur jusqu'à la fin de la Prusse**, sans suspendre les corrections indépendantes : [protocole groupé](PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05/PLAYER_TEST_PROTOCOL_GROUPED.md). La recherche de précision occidentale s'arrête pour cette passe. Prochaine frontière candidate : Glatz/Silésie, `SC3-SILESIA-LUSATIA`, non commencée ici. Aucun lancement de Bavière ou de micro-État. Les encadrés antérieurs ci-dessous sont conservés comme archives ; leurs anciennes demandes de test immédiat ne remplacent pas cette instruction.

'''
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        prior=(w.OUT/('BEFORE_'+name)).read_bytes();assert (w.CANON/name).read_bytes()==prior,'Concurrent '+name
        head,body=prior.split(b'\n',1);text=body.decode('utf-8')
        if name=='NEXT_ACTION.md':head='# Prochaine action — poursuivre les frontières prussiennes ; tests moteur différés'.encode('utf-8')
        if name=='ROADMAP.md':
            start=text.index('#### SC5-PRUSSIAN-WEST');end=text.index('#### SC5-JEVER',start);section=text[start:end];assert section.count('`BLOCKED`')==1;text=text[:start]+section.replace('`BLOCKED`','`IN_PROGRESS`')+text[end:]
        if name=='BLOCKERS.md':
            target='Tâches : SC5-PRUSSIAN-WEST `BLOCKED`. Correspondance native non résolue ; voir la passe PRUSSIAN_WEST_2026_11_05, aucune correction installée.';assert text.count(target)==1;text=text.replace(target,'Tâches : SC5-PRUSSIAN-WEST `IN_PROGRESS`. Noyau B de 32 cellules installé ; région entière encore ouverte. Tests moteur différés à la fin de la Prusse. Voir PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05.')
        (w.CANON/name).write_bytes(head+b'\n\n'+intro.encode('utf-8')+text.encode('utf-8'))
    prior=(w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes();assert (w.CANON/'PROGRESS_HISTORY.md').read_bytes()==prior
    addition='''

## SERG-RM-0066 — 5 novembre 2026 — Repères physiques et noyau prussien B de Ravensberg

SC5-PRUSSIAN-WEST BLOCKED→IN_PROGRESS ; PW-RAVENSBERG-B32 installé, prêt au moteur. Six repères physiques comparés, ancien R5 retenu seulement pour B ; nouvel affine rejeté sur les trois témoins. 32 cellules : SCM 9, WPM 6, HAN 17 vers PRU ; 11 559 habitants existants réaffectés, bâtiments/PM/unités/technologies et repères physiques conservés. 592→595 titres impériaux, même étendue et neuf électeurs. Noyaux Minden/Lingen/Tecklenburg/WPO/Lippe et anciennes cellules PRU protégés. Aucune certification régionale, attestation ou point ; 93/235, 39,57 %, 32/81 inchangés. Le joueur diffère tous les tests moteur à la fin de la Prusse ; cette attente n'arrête pas les corrections autorisées. Recherche de précision occidentale arrêtée pour cette passe ; Glatz/Silésie candidate non commencée, aucune Bavière. [Rapport](PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05/REPORT.md).
'''
    (w.CANON/'PROGRESS_HISTORY.md').write_bytes(prior+addition.encode('utf-8'));assert (w.CANON/'PROGRESS_SNAPSHOT.json').read_bytes()==(w.OUT/'BEFORE_PROGRESS_SNAPSHOT.json').read_bytes();rm.write_json(w.CANON/'PROGRESS_SNAPSHOT.json',rm.progress(s))
    print('SERG-RM-0066: IN_PROGRESS + partial installation; 93/235, 39.57%; engine tests deferred by user')

def final():
    b=w.load('BASELINE.json');old=w.load('BEFORE_ROADMAP_STATE.json');s=rm.load_json(w.CANON/'ROADMAP_STATE.json');checks=[]
    def ck(n,v):checks.append(dict(name=n,status='PASS' if v else 'FAIL'))
    ck('static_installation_validation',w.load('VALIDATION.json')['status']=='PASS');target='SC5-PRUSSIAN-WEST';task=next(t for t in s['tasks'] if t['id']==target)
    ck('80_other_tasks_preserved',[t for t in s['tasks'] if t['id']!=target]==[t for t in old['tasks'] if t['id']!=target])
    ck('scope_81_tasks_235_points',len(s['tasks'])==81 and sum(t['weight'] for t in s['tasks'])==235 and s['scope_version']=='1.0.0')
    ck('old_events_preserved',s['events'][:-1]==old['events'] and s['events'][-1]['id']=='SERG-RM-0066')
    ck('partial_installation_without_fictitious_receipt',task['status']=='IN_PROGRESS' and task['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and task['runtime_validation']['attestation'] is None and task['runtime_validation']['status']=='NOT_RUN')
    ck('all_old_receipt_records_preserved',all(s[k]==old[k] for k in ['closure_approval','external_prussian_deliveries','prussian_silesia_comparison','source_manifest']))
    ck('engine_tests_deferred_by_user',s['runtime_validation_hold']['deferred_until_prussia_finished_by_user'] is True and s['runtime_validation_hold']['does_not_block_implementation'] is True)
    ck('progress_history_additive',(w.CANON/'PROGRESS_HISTORY.md').read_bytes().startswith((w.OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()))
    p=rm.progress(s);ck('progress_no_new_credit',(p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['percent'])==(93,235,32,'39.57'))
    result=rm.check();w.dump('CANONICAL_CHECK.json',result);ck('canonical_validator',result['status']=='PASS')
    paths=[r['file'] for r in w.load('INSTALLATION.json')['changes']]+['tools/serg_prussian_west_physical.py','tools/serg_prussian_west_physical_tracking.py']+[str((w.CANON/n).relative_to(w.ROOT)) for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]
    args=['git','--no-optional-locks','diff','--check','--',*paths];r=subprocess.run(args,cwd=w.ROOT,capture_output=True,text=True);w.dump('DIFF_CHECK.json',dict(command=args,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr));ck('diff_check',r.returncode==0)
    w.dump('FINAL_CHECKS.json',dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),progress=p,new_human_receipts=0,engine_test=False));print('Final checks',len(checks),[c for c in checks if c['status']!='PASS']);assert all(c['status']=='PASS' for c in checks)

if __name__=='__main__':{'tracker':tracker,'final':final}[sys.argv[1]]()
