"""One-shot recording of the user's explicit three-sub-lot runtime receipt."""
import copy
import hashlib
import subprocess
from pathlib import Path
import serg_sc2_inner_austria as lot

rm=lot.rm
CONCURRENT='common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt'


def run():
    out=lot.OUT
    capture=lot.load(out/'ACCEPTANCE_SESSION_BEFORE_2026_10_19.json')
    state=lot.load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==capture['roadmap'] and state['events'][-1]['id']=='SERG-RM-0013'
    receipt=out/'RUNTIME_USER_ATTESTATION_2026_10_19.json';assert not receipt.exists()
    b=lot.load(out/'BASELINE.json');inv=capture['inventory'];checks=[]
    def ck(name,ok):
        checks.append(dict(name=name,passed=bool(ok)))
    ck('Previous delivery manifest retained',not capture['previous_delivery_differences'])
    for sid,path in lot.ADMIN_FILES.items():
        ck('Tested administration contract '+sid,lot.admin_contract((lot.ROOT/path).read_text(encoding='utf8'),sid))
    for r in lot.load(out/'MARITIME_CLEANUP.json')['files']:
        ck('Tested maritime removal retained '+r['file'],lot.maritime_contract(
            (out/r['before_file']).read_bytes().decode('utf8'),(lot.ROOT/r['file']).read_bytes().decode('utf8')))
    ck('Geometry ownership population units and old diagnostics retained',all(inv[k]==b['inventory'][k]
        for k in inv if k not in ('buildings','building_levels_written')))
    expected=lot.shared.core.qa.counter(b['inventory']['buildings'])
    for sid,path in lot.ADMIN_FILES.items():
        node=lot.shared.core.region((lot.ROOT/path).read_text(encoding='utf8'),sid,'AUS').children('create_building')[0]
        expected[(sid,'AUS',lot.shared.core.qa.signature(node))]+=1
    for r in lot.load(out/'MARITIME_CLEANUP.json')['files']:
        for signature in r['removed_signatures']:
            expected[('STATE_SLOVENIA','AUS',signature)]-=1
    ck('Only tested building deltas present',lot.shared.core.qa.counter(inv['buildings'])==+expected)
    levels=lot.shared.core.qa.counter(b['inventory']['building_levels_written'])
    levels['building_government_administration']+=2;levels['building_port']-=6;levels['building_shipyard']-=2
    ck('Only tested written level deltas present',lot.shared.core.qa.counter(inv['building_levels_written'])==levels)
    ck('574-row registry retained',capture['registry']==b['registry'] and len(capture['registry'])==574)
    v=lot.load(out/'VALIDATION.json')
    ck('Original 96/96 static result retained',v['total']==v['passed']==96 and not v['failed'])
    ck('All 23 previous qualified tasks retain evidence',sum(rm.qualifications(state).values())==23)
    delta={p for p in set(capture['hashes'])|set(b['hashes']) if capture['hashes'].get(p)!=b['hashes'].get(p)}
    scoped=set(lot.ADMIN_FILES.values())|set(lot.MARITIME_FILES)
    extra=delta-scoped
    ck('One isolated concurrent technology change, no territorial change',extra=={CONCURRENT})
    # Read the old tracked text only to characterize the concurrent delta, never restore it.
    old=subprocess.check_output(['git','show','HEAD:'+CONCURRENT]).decode('utf8')
    ck('Old technology text identified by hash with native line endings',b['hashes'][CONCURRENT] in {
        hashlib.sha256(old.encode('utf8')).hexdigest(),
        hashlib.sha256(old.replace('\r\n','\n').replace('\n','\r\n').encode('utf8')).hexdigest()})
    node=next(n for n in lot.shared.core.cw.parse(old) if n.key=='macroeconomics')
    block=old[node.start:node.end]
    expected_tech=old[:node.start]+block.replace('classical_political_economy','international_exchange_standards')+old[node.end:]
    current=(lot.ROOT/CONCURRENT).read_bytes().decode('utf8')
    # Git blobs use LF while this workspace preserves CRLF.
    ck('Concurrent change is only the macroeconomics prerequisite',current.replace('\r\n','\n')==expected_tech.replace('\r\n','\n'))
    assert all(c['passed'] for c in checks),checks
    prefix='docs/reports/map/SERG_CLOSURE/SC2-INNER-AUSTRIA/'
    rm.write_json(out/'ACCEPTANCE_CHECK_2026_10_19.json',dict(task_ids=[lot.TASK],status='PASS',
        total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    rm.write_json(out/'ACCEPTANCE_CONCURRENT_REVIEW_2026_10_19.json',dict(file=CONCURRENT,
        previous_sha256=b['hashes'][CONCURRENT],current_sha256=capture['hashes'][CONCURRENT],
        change='macroeconomics prerequisite classical_political_economy -> international_exchange_standards',
        preserved_without_writing=True,territorial_history_changed=False,not_in_runtime_receipt_scope=True,
        first_check_rejected='Overbroad expectation of no other runtime differences; no receipt or status was written by that first check'))
    source=Path('C:/Users/simeo/.codex/attachments/3c0aedc6-5792-4504-8922-e4ac1191b08e/Texte collé.txt')
    (out/'USER_MISSION_2026_10_19.txt').write_bytes(source.read_bytes())
    rm.write_json(receipt,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],recorded_on='2026-10-19',
        source=prefix+'USER_MISSION_2026_10_19.txt',
        user_statement="J'ai suivi intégralement le protocole de validation en jeu de SC2-INNER-AUSTRIA. J'approuve explicitement PASS_RUNTIME_USER_VALIDATED pour SC2-INNER-AUSTRIA, dans le seul périmètre effectivement installé.",
        protocol=prefix+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        scope=dict(installed_sub_lots=['IA-I-ST','IA-I-C','IA-E-C'],classification='B',states=['STATE_STYRIA','STATE_SLOVENIA'],
            public_administration_levels_added=2,maritime_declarations_removed=4,retained_rgb_count=12,retained_cells=3130,
            cadastral_validation=False,other_tasks_included=False),
        explicitly_reported=['Nouvelle partie en 1776','Contrôles du sous-lot Styrie réussis','Contrôles du sous-lot Carniole réussis',
            'Suppression des installations maritimes incorrectes de Ljubljana vérifiée','Conservations et non-régressions prévues par le protocole vérifiées',
            'Un mois complet de simulation','Sauvegarde et rechargement réussis','Aucune anomalie constatée pendant les vérifications'],
        new_game_date='1776-01-01',new_game_date_basis='Integral confirmation of protocol starting on 1776-01-01',
        simulation_months=1,save_and_reload=True,reported_anomalies=[],automated_engine_test=False,actual_test_date=None,language_tested=None,
        limitations='Three installed sub-lots only. No additional measure, capture, budget, employment reading, language or date inferred. No cadastral/demographic certification, Innviertel, Teschen or Adriatic scope.'))
    task=next(t for t in state['tasks'] if t['id']==lot.TASK)
    assert task['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    task['status']='PASS_RUNTIME_USER_VALIDATED'
    task['runtime_validation'].update(status=task['status'],attestation=prefix+receipt.name,
        scope='IA-I-ST, IA-I-C and IA-E-C only; entire player protocol explicitly confirmed, month, save/reload, no anomaly reported.')
    task['current_delivery_note']='Protocole intégral des trois sous-lots IA-I-ST/IA-I-C/IA-E-C explicitement réussi par le joueur : nouvelle partie 1776, administrations Styrie/Carniole et retrait maritime de Ljubljana vérifiés, conservations prévues, un mois, sauvegarde/rechargement réussis, aucune anomalie. Quatre points acquis pour le seul périmètre installé; aucun cadastre, démographie historique, Innviertel, Teschen ou interface adriatique certifié.'
    task['residual_uncertainty']='Fonctionnement des trois sous-lots confirmé par le joueur. Agrégats politiques B conservés, limites internes non cadastrées et démographie héritée; aucune mesure supplémentaire déduite du reçu. Innviertel, Tyrol, Teschen et interface adriatique restent des tâches distinctes.'
    assert state['runtime_validation_hold']['task_id']==lot.TASK
    state.pop('runtime_validation_hold');state['mission_status']='SC2_INNER_AUSTRIA_USER_VALIDATED_READY_FOR_NEXT'
    after=rm.progress(state)
    assert (after['earned_weight'],after['total_weight'],after['percent'],after['next_task'],after['qualified_tasks'])==(82,235,'34.89','SC2-ANTERIOR-AUSTRIA',24)
    (out/'ACCEPTANCE_2026_10_19.md').write_text('# Autriche intérieure — validation utilisateur reçue le 19 octobre 2026\n\n**PASS_RUNTIME_USER_VALIDATED**, uniquement IA-I-ST, IA-I-C et IA-E-C. Le joueur confirme intégralement le protocole : nouvelle partie 1776, contrôles Styrie/Carniole et retrait maritime de Ljubljana, conservations prévues, un mois complet, sauvegarde/rechargement réussis, aucune anomalie. Aucun relevé, capture ou test supplémentaire inventé. Le rapport original reste intact.\n\n[Reçu](RUNTIME_USER_ATTESTATION_2026_10_19.json) · [Mission](USER_MISSION_2026_10_19.txt) · [Conservation](ACCEPTANCE_CHECK_2026_10_19.json) · [Concurrence préservée](ACCEPTANCE_CONCURRENT_REVIEW_2026_10_19.json).\n\nProgression : **78/235 = 33,19 % → 82/235 = 34,89 %**, 24 tâches qualifiées. SC2-AUSTRIA reste BLOCKED, sans approbation de conservation définitive de son erreur potentielle. Teschen reste indépendant. Aucun cadastre ou chiffre démographique historique certifié. Aucun journal joueur ajouté dans le lot ne nécessite une seconde passe immersive. Prochaine tâche recalculée : SC2-ANTERIOR-AUSTRIA, P0 sans dépendance.\n',encoding='utf8')
    task['implementation_report'].append(prefix+'ACCEPTANCE_2026_10_19.md')
    state['events'].append(dict(id='SERG-RM-0014',date='2026-10-19',kind='RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],
        source=prefix+receipt.name,changes=[dict(task_id=lot.TASK,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after=task['status'])],
        before_percent='33.19',after_percent='34.89',before_weight=78,after_weight=82,total_weight=235,
        evidence=[prefix+receipt.name,prefix+'ACCEPTANCE_CHECK_2026_10_19.json',prefix+'ACCEPTANCE_2026_10_19.md'],
        note=task['current_delivery_note']+' 78/235→82/235, 33,19 %→34,89 %. Prochaine sélection SC2-ANTERIOR-AUSTRIA, P0 indépendant; une seule nouvelle étape autorisée. Modification concurrente du prérequis de macroéconomie identifiée et préservée, hors reçu. Aucun fichier fonctionnel changé pour enregistrer cette validation.'))
    assert [t for t in state['tasks'] if t['id']!=lot.TASK]==[t for t in original['tasks'] if t['id']!=lot.TASK]
    assert not rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state);rm.render()
    checked=rm.check();rm.write_json(out/'ACCEPTANCE_TRACKER_VALIDATION_2026_10_19.json',checked)
    assert checked['status']=='PASS'
    print('Receipt accepted; tracker PASS; 82/235=34.89%; next SC2-ANTERIOR-AUSTRIA',flush=True)


if __name__=='__main__':
    run()
