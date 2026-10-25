"""Accept the explicitly tested GEN method only, without regional credit."""
import contextlib
import copy
import io
import json
import subprocess
from pathlib import Path
import serg_sc4_ligurian_fiefs as lot

DATE='2026_10_23'
PREFIX=lot.PREFIX
CAPTURE=lot.OUT/('ACCEPTANCE_SESSION_BEFORE_'+DATE+'.json')
SOURCE=Path('C:/Users/simeo/.codex/attachments/5d01cca3-5e5d-4018-a878-26383630ad17/Texte collé.txt')

def capture():
    assert not CAPTURE.exists()
    state=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');assert state['events'][-1]['id']=='SERG-RM-0021'
    manifest=lot.load(lot.OUT/'DELIVERY_MANIFEST.json')['files']
    changed=[p for p,h in manifest.items() if not (lot.ROOT/p).is_file() or lot.sha(lot.ROOT/p)!=h]
    hashes=lot.prior.prior.runtime_hashes();old=lot.load(lot.OUT/'SESSION_AFTER.json')['hashes']
    concurrent=sorted(p for p in set(hashes)|set(old) if hashes.get(p)!=old.get(p))
    print('Delivery differences:',changed,'; runtime changes:',concurrent,flush=True)
    inv=lot.core.qa.inventory()
    git=lambda *args:subprocess.check_output(['git',*args],cwd=lot.ROOT,text=True).strip()
    lot.rm.write_json(CAPTURE,dict(roadmap=state,inventory=inv,hashes=hashes,registry=lot.load(lot.reg.active_registry_path()),delivery_manifest_changes=changed,concurrent_runtime_changes=concurrent,
        git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=lot.sha(lot.ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal'))))
    print('Acceptance baseline captured',flush=True)

def run():
    out,rm=lot.OUT,lot.rm;b=lot.load(CAPTURE);state=lot.load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==b['roadmap'] and state['events'][-1]['id']=='SERG-RM-0021'
    receiptname='RUNTIME_USER_ATTESTATION_'+DATE+'.json';assert not (out/receiptname).exists()
    checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    ck('Delivered manifest intact at entry',not b['delivery_manifest_changes'])
    ck('Tested runtime unchanged since delivery',not b['concurrent_runtime_changes'])
    ck('Current runtime still matches entry',lot.prior.prior.runtime_hashes()==b['hashes'])
    ck('World inventory equals delivered static inventory',b['inventory']==lot.load(out/'SESSION_AFTER_STATIC.json')['inventory'])
    ck('Exact tested GEN correction retained',(lot.ROOT/lot.BUILDINGS).read_bytes()==lot.candidate((out/'BUILDINGS_BEFORE.txt').read_bytes().decode('utf8')).encode('utf8'))
    ck('574 rights retained',len(b['registry'])==574 and b['registry']==lot.load(out/'BASELINE.json')['registry'])
    v=lot.load(out/'VALIDATION.json');ck('87/87 static evidence retained',v['passed']==v['total']==87 and not v['failed'])
    ck('24 acquired tasks still qualified',sum(rm.qualifications(state).values())==24)
    t=next(t for t in state['tasks'] if t['id']==lot.TASK)
    ck('P0 blocked with the sole pending method correction',t['status']=='BLOCKED' and t['priority']=='P0' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and [s['id'] for s in t['installed_sub_lots']]==[lot.SUB])
    assert all(c['passed'] for c in checks),checks
    checkname='ACCEPTANCE_CHECK_'+DATE+'.json';rm.write_json(out/checkname,dict(task_ids=[lot.TASK],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    sourcename='USER_VALIDATION_MISSION_'+DATE+'.txt';(out/sourcename).write_bytes(SOURCE.read_bytes())
    rm.write_json(out/receiptname,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],sub_lot_ids=[lot.SUB],scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-23',source=PREFIX+sourcename,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        explicitly_reported=['Nouvelle partie au 1er janvier 1776','Administration publique GEN présente et fonctionnelle','Niveau administratif initial conservé','pm_simple_organization disponible et correctement appliquée','Aucune anomalie dans les autres méthodes, bâtiments, propriétés, territoires et populations contrôlés','Un mois complet réussi','Sauvegarde et rechargement réussis','Aucun problème constaté pendant le protocole'],
        new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,automated_engine_test=False,actual_test_date=None,language_tested=None,reported_anomalies=[],additional_observations_invented=False,
        excluded=['Clôture globale des fiefs ligures','Torriglia et Santo Stefano','Droits Doria/Spinola/Fieschi/Pallavicini','Délimitation et représentation territoriale','Qualification ou correction du registre impérial','Toute nouvelle correction de Piombino ou Elbe']))
    t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED'
    t['installed_sub_lots'][0].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receiptname)
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receiptname,scope='LF-GEN-ADM-PM only: full protocol explicitly confirmed for the existing GEN public administration method. No territorial/legal regional closure and no points.')
    t['current_delivery_note']='LF-GEN-ADM-PM seul PASS_RUNTIME_USER_VALIDATED selon confirmation intégrale du protocole : nouvelle partie 1776, administration publique GEN et niveau conservés, organisation simple disponible et appliquée, éléments contrôlés sans anomalie, un mois, sauvegarde/rechargement réussis, aucun problème. SC4-LIGURIAN-FIEFS reste BLOCKED P0 pour juridictions et droits territoriaux ; aucune clôture régionale, aucun nouveau TAG ou droit impérial, aucun point.'
    t['residual_uncertainty']=t['blocking_reason']+' Seule la méthode de l’administration génoise existante est désormais validée en jeu ; aucune observation supplémentaire inventée.'
    acceptname='ACCEPTANCE_'+DATE+'.md'
    (out/acceptname).write_text('# Validation de la seule méthode administrative génoise\n\n**LF-GEN-ADM-PM : PASS_RUNTIME_USER_VALIDATED**, protocole intégral confirmé par le joueur et conservé dans USER_VALIDATION_MISSION_2026_10_23.txt. Aucune date effective de test, capture, mesure, langue ou observation supplémentaire ajoutée.\n\n**SC4-LIGURIAN-FIEFS reste BLOCKED P0** : souverainetés, droits féodaux, géographie et registre territorial encore ouverts. Aucun point : **82/235 = 34,89 %** avant/après. Rapport, préimage fonctionnel et preuves d’installation originaux intacts.\n\nAprès contrôle des preuves et du suivi, SC4-PIOMBINO est la prochaine P0 admissible sans dépendance ; une seule nouvelle étape est autorisée.\n',encoding='utf8')
    t['implementation_report'].append(PREFIX+acceptname)
    state['mission_status']='SC4_LIGURIAN_METHOD_USER_VALIDATED_REGION_BLOCKED_READY_FOR_PIOMBINO'
    state['events'].append(dict(id='SERG-RM-0022',date='2026-10-23',kind='PARTIAL_RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],source=PREFIX+receiptname,changes=[dict(task_id=lot.TASK,before='BLOCKED',after='BLOCKED')],sub_lot_changes=[dict(id=lot.SUB,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+receiptname,PREFIX+checkname,PREFIX+acceptname],note=t['current_delivery_note']+' Candidate SC4-PIOMBINO confirmée après validateur, une seule nouvelle étape autorisée.'))
    assert [x for x in state['tasks'] if x['id']!=lot.TASK]==[x for x in original['tasks'] if x['id']!=lot.TASK] and state['events'][:-1]==original['events']
    assert t['blocking_reason']==next(x for x in original['tasks'] if x['id']==lot.TASK)['blocking_reason']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state)
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC4-PIOMBINO')
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();rm.write_json(out/('ACCEPTANCE_TRACKER_VALIDATION_'+DATE+'.json'),checked);assert checked['status']=='PASS'
    assert '- SC4-LIGURIAN-FIEFS : 1 sous-lots installés validés' in (rm.OUT/'BLOCKERS.md').read_text(encoding='utf8')
    print(json.dumps(dict(acceptance_checks=len(checks),tracker=checked['status'],earned=p['earned_weight'],percent=p['percent'],next=p['next_task'])),flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
