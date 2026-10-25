"""Record the user's bounded receipt without closing or crediting the regional task."""
import copy
import io
import contextlib
from pathlib import Path
import serg_sc2_anterior_austria as lot


def run():
    out=lot.OUT;rm=lot.rm;capture=lot.load(out/'ACCEPTANCE_SESSION_BEFORE_2026_10_19.json')
    state=lot.load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==capture['roadmap'] and state['events'][-1]['id']=='SERG-RM-0015'
    receipt=out/'RUNTIME_USER_ATTESTATION_2026_10_19.json';assert not receipt.exists()
    b=lot.load(out/'BASELINE.json');inv=capture['inventory'];checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    ck('All previous delivery files retained',not capture['delivery_manifest_changes'])
    ck('No concurrent runtime change since delivered installation',not capture['concurrent_runtime_changes'])
    for sid,p in lot.ADMIN_FILES.items():ck('Tested administration '+sid,lot.admin_contract((lot.ROOT/p).read_text(encoding='utf8'),sid))
    before=(out/'PUBLIC_PORT_BEFORE.txt').read_bytes().decode('utf8');after=(lot.ROOT/lot.PORT_FILE).read_bytes().decode('utf8')
    ck('Single tested national port-owner correction retained',lot.port_contract(before,after))
    ck('World geometry owners pops units and diagnostics retained',all(inv[k]==b['inventory'][k] for k in inv if k not in {'buildings','building_levels_written'}))
    expected=lot.core.qa.counter(b['inventory']['buildings'])
    for sid,p in lot.ADMIN_FILES.items():
        node=lot.core.region((lot.ROOT/p).read_text(encoding='utf8'),sid,'AUS').children('create_building')[0]
        expected[(sid,'AUS',lot.core.qa.signature(node))]+=1
    old=lot.port_candidate(before)[1]
    new=next(n for n in lot.core.region(after,'STATE_ISTRIA','AUS').children('create_building') if lot.core.cw.scalar(n.one('building'))=='building_port')
    expected[('STATE_ISTRIA','AUS',lot.core.qa.signature(old))]-=1;expected[('STATE_ISTRIA','AUS',lot.core.qa.signature(new))]+=1
    ck('Only previously tested building deltas',lot.core.qa.counter(inv['buildings'])==+expected)
    levels=lot.core.qa.counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=2
    ck('Two written administration levels only',lot.core.qa.counter(inv['building_levels_written'])==levels)
    ck('574-row imperial registry retained',capture['registry']==b['registry'] and len(capture['registry'])==574)
    v=lot.load(out/'VALIDATION.json');ck('83/83 static proof retained',v['total']==v['passed']==83 and not v['failed'])
    ck('All 24 acquired tasks remain qualified',sum(rm.qualifications(state).values())==24)
    t=next(t for t in state['tasks'] if t['id']==lot.TASK)
    ck('Region is blocked and installed sub-lots pending',t['status']=='BLOCKED' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
    assert all(c['passed'] for c in checks),checks
    prefix='docs/reports/map/SERG_CLOSURE/SC2-ANTERIOR-AUSTRIA/'
    rm.write_json(out/'ACCEPTANCE_CHECK_2026_10_19.json',dict(task_ids=[lot.TASK],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    source=Path('C:/Users/simeo/.codex/attachments/b20af46e-beba-4969-8d76-eaa03c286e24/Texte collé.txt')
    (out/'USER_MISSION_2026_10_19.txt').write_bytes(source.read_bytes())
    rm.write_json(receipt,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],sub_lot_ids=['AN-I-W','AN-I-A','AN-P-A'],
        scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-19',
        source=prefix+'USER_MISSION_2026_10_19.txt',protocol=prefix+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        explicitly_reported=['Administration publique autrichienne ajoutée dans l’agrégat de Fribourg','Administration publique autrichienne ajoutée dans l’agrégat adriatique','Propriétaire du port de la portion autrichienne d’Istrie VEN vers AUS','Conservation des territoires, populations, bâtiments et autres éléments contrôlés','Un mois complet de simulation réussi','Sauvegarde et rechargement réussis','Aucune anomalie constatée'],
        new_game_date='1776-01-01',new_game_date_basis='Full protocol explicitly confirmed, including its new-game starting date',simulation_months=1,save_and_reload=True,
        automated_engine_test=False,actual_test_date=None,language_tested=None,reported_anomalies=[],
        excluded=['Hohenberg','Fricktal','Istrian shipyard ownership','Cadastral precision','Innviertel','Teschen','Any new Italian installation'],
        additional_observations_invented=False))
    t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED'
    for sub in t['installed_sub_lots']:sub['status']='PASS_RUNTIME_USER_VALIDATED';sub['attestation']=prefix+receipt.name
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=prefix+receipt.name,
        scope='AN-I-W, AN-I-A, AN-P-A only; full protocol explicitly confirmed by user. No territorial closure, cadastral certification, shipyard decision or points.')
    t['current_delivery_note']='Les trois sous-lots AN-I-W/AN-I-A/AN-P-A sont explicitement validés en jeu par le joueur : protocole intégral réussi, administrations Fribourg/Adriatique, propriétaire national du port, conservations prévues, un mois, sauvegarde/rechargement, aucune anomalie. PASS_RUNTIME_USER_VALIDATED limité aux installations; tâche régionale BLOCKED pour Hohenberg/Fricktal et propriété du chantier naval, sans point de clôture ni validation cadastrale.'
    t['residual_uncertainty']=t['blocking_reason']+' Les trois installations fonctionnent selon le protocole confirmé; aucune observation supplémentaire inventée.'
    (out/'ACCEPTANCE_2026_10_19.md').write_text('# Validation utilisateur des seules corrections installées\n\nAN-I-W, AN-I-A et AN-P-A : **PASS_RUNTIME_USER_VALIDATED**, selon confirmation intégrale du protocole conservée dans USER_MISSION_2026_10_19.txt et RUNTIME_USER_ATTESTATION_2026_10_19.json. Aucun détail supplémentaire inventé.\n\nLa tâche régionale reste **BLOCKED**, Hohenberg/Fricktal et propriété du chantier naval ouverts. Aucun état terminal global, aucune certification cadastrale, aucun point ajouté. **82/235 = 34,89 %** avant et après. Le rapport d’installation original et son manifeste restent intacts; le présent document est additif.\n\nProchaine tâche recalculée : SC4-EXISTING-ITALIAN-STATES, P0 sans dépendance, autorisée seule par cette mission.\n',encoding='utf8')
    t['implementation_report'].append(prefix+'ACCEPTANCE_2026_10_19.md')
    state['mission_status']='SC2_ANTERIOR_SUB_LOTS_USER_VALIDATED_REGION_BLOCKED_READY_FOR_ITALY'
    state['events'].append(dict(id='SERG-RM-0016',date='2026-10-19',kind='PARTIAL_RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],source=prefix+receipt.name,
        changes=[dict(task_id=lot.TASK,before='BLOCKED',after='BLOCKED')],sub_lot_changes=[dict(id=k,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED') for k in ['AN-I-W','AN-I-A','AN-P-A']],
        before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',
        evidence=[prefix+receipt.name,prefix+'ACCEPTANCE_CHECK_2026_10_19.json',prefix+'ACCEPTANCE_2026_10_19.md'],note=t['current_delivery_note']+' Progression maintenue 82/235=34,89 %. SC4-EXISTING-ITALIAN-STATES P0 sans dépendance sélectionné après contrôle; une seule nouvelle tâche autorisée.'))
    assert [x for x in state['tasks'] if x['id']!=lot.TASK]==[x for x in original['tasks'] if x['id']!=lot.TASK]
    assert state['events'][:-1]==original['events'] and t['blocking_reason']==next(x for x in original['tasks'] if x['id']==lot.TASK)['blocking_reason']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(t,state)
    assert not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state), 'Partial receipt must never close whole region'
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC4-EXISTING-ITALIAN-STATES')
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();rm.write_json(out/'ACCEPTANCE_TRACKER_VALIDATION_2026_10_19.json',checked);assert checked['status']=='PASS'
    print('Partial receipt accepted; region BLOCKED; tracker PASS; 82/235=34.89%; next SC4-EXISTING-ITALIAN-STATES',flush=True)


if __name__=='__main__':run()
