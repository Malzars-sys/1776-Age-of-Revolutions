"""Bounded acceptance of the two administrations; regional P0 remains blocked."""
import contextlib
import copy
import io
import json
import subprocess
from pathlib import Path
import serg_sc4_savoy_nice as lot

DATE='2026_10_23'
PREFIX=lot.PREFIX
IDS=['SN-I-SAV','SN-I-NIC']
CAPTURE=lot.OUT/('ACCEPTANCE_SESSION_BEFORE_'+DATE+'.json')

def capture():
    assert not CAPTURE.exists()
    state=lot.load(lot.rm.OUT/'ROADMAP_STATE.json')
    assert state['events'][-1]['id']=='SERG-RM-0019'
    manifest=lot.load(lot.OUT/'DELIVERY_MANIFEST.json')['files']
    changed=[p for p,h in manifest.items() if not (lot.ROOT/p).is_file() or lot.sha(lot.ROOT/p)!=h]
    hashes=lot.prior.runtime_hashes();old=lot.load(lot.OUT/'SESSION_AFTER.json')['hashes']
    concurrent=sorted(p for p in set(hashes)|set(old) if hashes.get(p)!=old.get(p))
    print('Delivery differences:',changed,'; runtime changes:',concurrent,flush=True)
    inv=lot.core.qa.inventory()
    def git(*args):return subprocess.check_output(['git',*args],cwd=lot.ROOT,text=True).strip()
    lot.rm.write_json(CAPTURE,dict(roadmap=state,inventory=inv,hashes=hashes,registry=lot.load(lot.reg.active_registry_path()),delivery_manifest_changes=changed,concurrent_runtime_changes=concurrent,
        git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=lot.sha(lot.ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal')),
        roadmap_tool_sha_before=lot.sha(lot.ROOT/'tools/serg_closure_roadmap.py')))
    print('Acceptance baseline captured',flush=True)

def run():
    out,rm=lot.OUT,lot.rm;capture=lot.load(CAPTURE)
    state=lot.load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==capture['roadmap'] and state['events'][-1]['id']=='SERG-RM-0019'
    assert not (out/('RUNTIME_USER_ATTESTATION_'+DATE+'.json')).exists()
    checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    ck('Previous delivery manifest intact at entry',not capture['delivery_manifest_changes'])
    ck('Tested runtime unchanged since delivery',not capture['concurrent_runtime_changes'])
    ck('Current runtime still matches entry',lot.prior.runtime_hashes()==capture['hashes'])
    ck('Full world inventory equals delivered static inventory',capture['inventory']==lot.load(out/'SESSION_AFTER_STATIC.json')['inventory'])
    for sid,p in lot.ADMIN_FILES.items():ck('Tested administration '+sid,lot.admin_contract((lot.ROOT/p).read_text(encoding='utf8'),sid))
    ck('574 imperial rights retained',len(capture['registry'])==574 and capture['registry']==lot.load(out/'BASELINE.json')['registry'])
    v=lot.load(out/'VALIDATION.json');ck('101/101 static evidence retained',v['passed']==v['total']==101 and not v['failed'])
    ck('24 qualified tasks retained',sum(rm.qualifications(state).values())==24)
    t=next(t for t in state['tasks'] if t['id']==lot.TASK)
    ck('Blocked P0 with exactly two pending installations',t['status']=='BLOCKED' and t['priority']=='P0' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and sorted(s['id'] for s in t['installed_sub_lots'])==sorted(IDS))
    assert all(c['passed'] for c in checks),checks
    checkname='ACCEPTANCE_CHECK_'+DATE+'.json'
    rm.write_json(out/checkname,dict(task_ids=[lot.TASK],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    source=Path('C:/Users/simeo/.codex/attachments/e0e88dfb-be03-4c40-891e-e6e7c6e116a9/Texte collé.txt')
    sourcename='USER_VALIDATION_MISSION_'+DATE+'.txt';(out/sourcename).write_bytes(source.read_bytes())
    receiptname='RUNTIME_USER_ATTESTATION_'+DATE+'.json'
    rm.write_json(out/receiptname,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],sub_lot_ids=IDS,scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-23',source=PREFIX+sourcename,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        explicitly_reported=['Nouvelle partie au 1er janvier 1776','Administration SAR présente et fonctionnelle en Savoie','Administration SAR présente et fonctionnelle dans la subdivision niçoise de Provence','Quatre niveaux administratifs piémontais conservés','Souveraineté SAR, Victor-Amédée III et capitale Turin conservés','Aucune anomalie dans les territoires, populations et bâtiments contrôlés','Un mois complet réussi','Sauvegarde et rechargement réussis','Aucun bug constaté'],new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,automated_engine_test=False,actual_test_date=None,language_tested=None,reported_anomalies=[],additional_observations_invented=False,
        excluded=['Clôture globale Savoie-Nice','Correspondance des frontières 1754/1760','Qualification du statut impérial','Droits d’investiture/vicariat','Traduction constitutionnelle','Correction du registre','Toute installation ligure nouvelle']))
    t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED'
    for s in t['installed_sub_lots']:s.update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receiptname)
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receiptname,scope='SN-I-SAV and SN-I-NIC only; full protocol explicitly confirmed. No regional, territorial or constitutional closure and no points.')
    t['current_delivery_note']='SN-I-SAV et SN-I-NIC seulement sont PASS_RUNTIME_USER_VALIDATED selon confirmation intégrale du protocole : nouvelle partie 1776, administrations SAR fonctionnelles, quatre niveaux piémontais, souveraineté SAR, Victor-Amédée III et Turin conservés, territoires/populations/bâtiments contrôlés sans anomalie, un mois, sauvegarde/rechargement, aucun bug. SC4-SAVOY-NICE reste BLOCKED P0 pour frontières et droits impériaux; aucun point ni clôture territoriale ou constitutionnelle.'
    t['residual_uncertainty']=t['blocking_reason']+' Les deux administrations seules sont validées en jeu; aucune observation supplémentaire inventée.'
    acceptname='ACCEPTANCE_'+DATE+'.md'
    (out/acceptname).write_text('# Validation des seules administrations Savoie et Nice\n\n**SN-I-SAV et SN-I-NIC : PASS_RUNTIME_USER_VALIDATED**, selon confirmation intégrale du protocole conservée dans USER_VALIDATION_MISSION_2026_10_23.txt. Le reçu ne précise aucune date effective de test, langue, capture ou mesure non fournie.\n\n**SC4-SAVOY-NICE reste BLOCKED P0** : frontières de 1754/1760, statut impérial, investiture/vicariat, traduction constitutionnelle et éventuelle correction du registre restent ouverts. Aucun point : **82/235 = 34,89 %** avant et après. Rapport et preuves d’installation d’origine intacts.\n\nLe suivi confirme SC4-LIGURIAN-FIEFS, P0 sans dépendance, comme seule nouvelle étape autorisée. Le rendu des validations partielles affiche désormais leur nombre réel, deux pour cette région et trois pour les anciennes régions concernées.\n',encoding='utf8')
    t['implementation_report'].append(PREFIX+acceptname)
    state['mission_status']='SC4_SAVOY_NICE_ADMINISTRATIONS_USER_VALIDATED_REGION_BLOCKED_READY_FOR_LIGURIA'
    state['events'].append(dict(id='SERG-RM-0020',date='2026-10-23',kind='PARTIAL_RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],source=PREFIX+receiptname,changes=[dict(task_id=lot.TASK,before='BLOCKED',after='BLOCKED')],sub_lot_changes=[dict(id=k,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED') for k in IDS],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+receiptname,PREFIX+checkname,PREFIX+acceptname],note=t['current_delivery_note']+' Suivi recalculé : SC4-LIGURIAN-FIEFS reste la prochaine P0 admissible sans dépendance; une seule nouvelle étape autorisée.'))
    assert [x for x in state['tasks'] if x['id']!=lot.TASK]==[x for x in original['tasks'] if x['id']!=lot.TASK] and state['events'][:-1]==original['events']
    assert t['blocking_reason']==next(x for x in original['tasks'] if x['id']==lot.TASK)['blocking_reason']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state)
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC4-LIGURIAN-FIEFS')
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();rm.write_json(out/('ACCEPTANCE_TRACKER_VALIDATION_'+DATE+'.json'),checked);assert checked['status']=='PASS'
    text=(rm.OUT/'BLOCKERS.md').read_text(encoding='utf8')
    assert '- SC4-SAVOY-NICE : 2 sous-lots installés validés' in text
    print(json.dumps(dict(acceptance_checks=len(checks),tracker=checked['status'],earned=p['earned_weight'],percent=p['percent'],next=p['next_task'])),flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
