"""Record the explicit, bounded Italian administration receipt of 23 October."""
import contextlib
import copy
import io
import json
import subprocess
from pathlib import Path
import serg_sc4_italian_states as lot

DATE = '2026_10_23'
PREFIX = 'docs/reports/map/SERG_CLOSURE/SC4-EXISTING-ITALIAN-STATES/'
IDS = ['IT-I-MOD', 'IT-I-PAR', 'IT-I-LUC']


def run():
    out, rm = lot.OUT, lot.rm
    capture_path = out / ('ACCEPTANCE_SESSION_BEFORE_' + DATE + '.json')
    assert not capture_path.exists(), 'Acceptance must not overwrite an earlier receipt'
    state = lot.load(rm.OUT / 'ROADMAP_STATE.json')
    original = copy.deepcopy(state)
    assert state['events'][-1]['id'] == 'SERG-RM-0017'
    manifest = lot.load(out / 'DELIVERY_MANIFEST.json')['files']
    changes = [p for p, h in manifest.items() if not (lot.ROOT/p).is_file() or lot.sha(lot.ROOT/p) != h]
    runtime = lot.runtime_hashes()
    delivered = lot.load(out/'SESSION_AFTER.json')
    old_hashes = delivered.get('hashes', delivered.get('runtime_hashes'))
    assert old_hashes is not None, delivered.keys()
    concurrent = [p for p in set(runtime)|set(old_hashes) if runtime.get(p) != old_hashes.get(p)]
    inv = lot.core.qa.inventory()
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=lot.ROOT, text=True, encoding='utf8').strip()
    index = Path(git('rev-parse','--git-path','index'))
    if not index.is_absolute(): index = lot.ROOT/index
    capture = dict(roadmap=state, inventory=inv, hashes=runtime,
                   registry=lot.load(lot.reg.active_registry_path()),
                   delivery_manifest_changes=changes, concurrent_runtime_changes=sorted(concurrent),
                   git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),
                            index_sha256=lot.sha(index),status=git('status','--short','--untracked-files=normal')))
    rm.write_json(capture_path,capture)
    checks=[]
    def ck(name,ok): checks.append(dict(name=name,passed=bool(ok)))
    ck('Previous delivery manifest intact', not changes)
    ck('Delivered runtime has no intervening changes', not concurrent)
    b=lot.load(out/'BASELINE.json')
    ck('Geometry owners populations units diagnostics conserved', all(inv[k]==b['inventory'][k] for k in inv if k not in {'buildings','building_levels_written'}))
    expected=lot.core.qa.counter(b['inventory']['buildings'])
    for tag,path in sorted(lot.ADMIN_FILES.items()):
        raw=(lot.ROOT/path).read_text(encoding='utf8')
        ck('Tested public administration '+tag,lot.admin_contract(raw,tag))
        node=lot.core.region(raw,'STATE_EMILIA',tag).children('create_building')[0]
        expected[('STATE_EMILIA',tag,lot.core.qa.signature(node))]+=1
    ck('Exactly the three tested building additions; Tuscany unchanged',lot.core.qa.counter(inv['buildings'])==expected)
    levels=lot.core.qa.counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=3
    ck('Three written administration levels only',lot.core.qa.counter(inv['building_levels_written'])==levels)
    ck('574-row imperial registry unchanged',capture['registry']==b['registry'] and len(capture['registry'])==574)
    v=lot.load(out/'VALIDATION.json')
    ck('Original 91/91 static evidence intact',v['total']==v['passed']==91 and not v['failed'])
    ck('All 24 qualified regional tasks retained',sum(rm.qualifications(state).values())==24)
    t=next(x for x in state['tasks'] if x['id']==lot.TASK)
    ck('Blocked region and three pending sub-lots',t['status']=='BLOCKED' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and sorted(s['id'] for s in t['installed_sub_lots'])==sorted(IDS))
    assert all(c['passed'] for c in checks),checks
    checkname='ACCEPTANCE_CHECK_'+DATE+'.json'
    rm.write_json(out/checkname,dict(task_ids=[lot.TASK],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    source=Path('C:/Users/simeo/.codex/attachments/acc71d83-d345-4e58-b3ed-6785a15ec372/Texte collé.txt')
    sourcename='USER_MISSION_'+DATE+'.txt'
    (out/sourcename).write_bytes(source.read_bytes())
    receiptname='RUNTIME_USER_ATTESTATION_'+DATE+'.json'
    rm.write_json(out/receiptname,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],sub_lot_ids=IDS,
        scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-23',
        source=PREFIX+sourcename,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        explicitly_reported=['Nouvelle partie au 1er janvier 1776','Administration publique de Modène présente et fonctionnelle','Administration publique de Parme présente et fonctionnelle','Administration publique de Lucques présente et fonctionnelle','Gouvernement républicain de Lucques conservé','Administrations préexistantes de Toscane conservées','Vérifications de conservation du protocole réussies','Un mois complet sans anomalie','Sauvegarde et rechargement réussis','Aucun bug constaté'],
        new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,automated_engine_test=False,
        actual_test_date=None,language_tested=None,reported_anomalies=[],additional_observations_invented=False,
        excluded=['Clôture régionale italienne','Statut et obligations impériaux de Lucques','Droits de Parme et Guastalla','Rapports Parme Habsbourg Bourbons Espagne','Exactitude cadastrale','Toute installation Savoie-Nice']))
    t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED'
    for sub in t['installed_sub_lots']:
        sub.update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receiptname)
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receiptname,
        scope='IT-I-MOD, IT-I-PAR, IT-I-LUC only; full protocol explicitly confirmed by user. No regional or constitutional closure and no points.')
    t['current_delivery_note']='Les administrations IT-I-MOD, IT-I-PAR et IT-I-LUC sont PASS_RUNTIME_USER_VALIDATED selon le protocole intégral explicitement confirmé : nouvelle partie 1776, administrations fonctionnelles, république de Lucques et administrations toscanes conservées, contrôles de conservation, un mois, sauvegarde/rechargement, aucun bug. Tâche globale BLOCKED pour les droits impériaux de Lucques, Parme/Guastalla et les liens espagnols; aucun point supplémentaire ni clôture constitutionnelle.'
    t['residual_uncertainty']=t['blocking_reason']+' Les trois installations administratives seulement sont validées; aucune observation supplémentaire inventée.'
    acceptname='ACCEPTANCE_'+DATE+'.md'
    (out/acceptname).write_text('# Validation utilisateur des trois administrations italiennes\n\n**IT-I-MOD, IT-I-PAR, IT-I-LUC : PASS_RUNTIME_USER_VALIDATED.** Le joueur confirme intégralement le protocole, notamment nouvelle partie 1776, administrations fonctionnelles, république lucquoise et administrations toscanes conservées, contrôles de conservation, un mois sans anomalie et sauvegarde/rechargement réussis. Source intégrale et reçu dans ce dossier. Date effective du test, captures et mesures non fournies restent non renseignées.\n\n**SC4-EXISTING-ITALIAN-STATES reste BLOCKED** pour les droits de Lucques, Parme/Guastalla et les rapports espagnols. Aucun changement de pacte, suzeraineté ou registre. Aucun point : **82/235 = 34,89 %** avant et après. Les preuves d’installation originales restent intactes; cette attestation est additive.\n\nAprès contrôle canonique, seule SC4-SAVOY-NICE est sélectionnée pour la nouvelle passe autorisée.\n',encoding='utf8')
    t['implementation_report'].append(PREFIX+acceptname)
    state['mission_status']='SC4_ITALIAN_ADMINISTRATIONS_USER_VALIDATED_REGION_BLOCKED_READY_FOR_SAVOY'
    state['events'].append(dict(id='SERG-RM-0018',date='2026-10-23',kind='PARTIAL_RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],source=PREFIX+receiptname,
        changes=[dict(task_id=lot.TASK,before='BLOCKED',after='BLOCKED')],
        sub_lot_changes=[dict(id=k,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED') for k in IDS],
        before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',
        evidence=[PREFIX+receiptname,PREFIX+checkname,PREFIX+acceptname],note=t['current_delivery_note']+' SC4-SAVOY-NICE reste la prochaine P0 admissible sans dépendance; une seule nouvelle étape autorisée.'))
    assert [x for x in state['tasks'] if x['id']!=lot.TASK]==[x for x in original['tasks'] if x['id']!=lot.TASK]
    assert state['events'][:-1]==original['events']
    assert t['blocking_reason']==next(x for x in original['tasks'] if x['id']==lot.TASK)['blocking_reason']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state)
    p=rm.progress(state)
    assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC4-SAVOY-NICE')
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()): rm.render()
    checked=rm.check();rm.write_json(out/('ACCEPTANCE_TRACKER_VALIDATION_'+DATE+'.json'),checked)
    assert checked['status']=='PASS'
    print(json.dumps(dict(acceptance_checks=len(checks),tracker=checked['status'],progress=p),ensure_ascii=False),flush=True)


if __name__=='__main__': run()
