"""Accept TR-I-CORE only; retain the territorial Trento task as BLOCKED."""
import contextlib
import copy
import io
import json
import os
import subprocess
from pathlib import Path
import serg_sc1_trento as lot

DATE='2026_10_23'
PREFIX=lot.PREFIX
SOURCE=Path('C:/Users/simeo/.codex/attachments/48d13c37-0556-446d-867a-f7442a0f7efa/Texte collé.txt')
CAPTURE=lot.OUT/('ACCEPTANCE_SESSION_BEFORE_'+DATE+'.json')
os.environ['GIT_OPTIONAL_LOCKS']='0'

def capture():
    assert not CAPTURE.exists()
    state=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');assert state['events'][-1]['id']=='SERG-RM-0028'
    manifest=lot.load(lot.OUT/'DELIVERY_MANIFEST.json')['files']
    changed=[p for p,h in manifest.items() if not (lot.ROOT/p).is_file() or lot.sha(lot.ROOT/p)!=h]
    hashes=lot.prior.italian.runtime_hashes();old=lot.load(lot.OUT/'SESSION_AFTER.json')['hashes']
    concurrent=sorted(p for p in set(hashes)|set(old) if hashes.get(p)!=old.get(p))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=lot.ROOT,text=True).strip()
    lot.rm.write_json(CAPTURE,dict(roadmap=state,inventory=lot.core.qa.inventory(),hashes=hashes,
        registry=lot.load(lot.reg.active_registry_path()),delivery_manifest_changes=changed,concurrent_runtime_changes=concurrent,
        git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=lot.sha(lot.ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal'))))
    print(json.dumps(dict(manifest_changes=changed,concurrent_changes=concurrent)),flush=True)

def run():
    out,rm=lot.OUT,lot.rm;b=lot.load(CAPTURE);state=lot.load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==b['roadmap'] and state['events'][-1]['id']=='SERG-RM-0028'
    receipt='RUNTIME_USER_ATTESTATION_'+DATE+'.json';assert not (out/receipt).exists()
    checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    ck('103-file Trento delivery manifest intact',not b['delivery_manifest_changes'])
    owned=set(lot.load(out/'FILES_MODIFIED.json')['runtime_files'])
    ck('Concurrent changes outside delivered Trento files',not owned.intersection(b['concurrent_runtime_changes']))
    ck('Current runtime matches captured entry',lot.prior.italian.runtime_hashes()==b['hashes'])
    ck('World history inventory matches delivered static inventory',b['inventory']==lot.load(out/'SESSION_AFTER_STATIC.json')['inventory'])
    rel=lot.reg.active_registry_path().relative_to(lot.ROOT).as_posix()
    ck('576 imperial rights retained',len(b['registry'])==576 and lot.sha(lot.reg.active_registry_path())==lot.load(out/'DELIVERY_MANIFEST.json')['files'][rel])
    v=lot.load(out/'VALIDATION.json');ck('156/156 static evidence preserved',v['passed']==v['total']==156 and not v['failed'])
    ck('24 qualified tasks remain credited',sum(rm.qualifications(state).values())==24)
    t=next(t for t in state['tasks'] if t['id']==lot.TASK)
    ck('Only TR-I-CORE was pending',t['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and [s['id'] for s in t['installed_sub_lots']]==['TR-I-CORE'])
    import numpy as np
    bitmap=lot.core.packed(lot.ROOT/'map_data/provinces.png');ys,xs=np.where(bitmap==int(lot.RGB[1:],16))
    ck('Exact twelve delivered cells retained',sorted(map(list,zip(xs.tolist(),ys.tolist())))==sorted(lot.CELLS))
    assert all(c['passed'] for c in checks),checks
    checkfile='ACCEPTANCE_CHECK_'+DATE+'.json'
    rm.write_json(out/checkfile,dict(task_ids=[lot.TASK],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    sourcename='USER_VALIDATION_MISSION_'+DATE+'.txt';(out/sourcename).write_bytes(SOURCE.read_bytes())
    rm.write_json(out/receipt,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],sub_lot_ids=['TR-I-CORE'],
        scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-23',
        source=PREFIX+sourcename,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        explicitly_reported=['Nouvelle partie au 1er janvier 1776','TRT présent autour de Trente et noyau de 12 cellules fonctionnel',
            'Capitale dans le territoire TRT et fonctionnelle','Cristoforo Sizzo de Noris prince-évêque catholique',
            '9000 habitants initiaux et administration publique présents','Pacte défensif AUS présent et fonctionnel',
            'Appartenance impériale correctement représentée sans nouvel électorat',
            'Voisins Rovereto/Bolzano/Merano et possessions vénitiennes conservés',
            'Un mois complet sans anomalie','Sauvegarde et rechargement réussis','Aucun bug constaté pendant le protocole'],
        new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,actual_test_date=None,language_tested=None,
        automated_engine_test=False,reported_anomalies=[],additional_observations_invented=False,
        validated_scope=dict(tag='TRT',rgb=lot.RGB,cells=lot.CELLS,category='B',population=9000),
        excluded=['Clôture territoriale globale SC1-TRENTO','Diocèse entier','Val di Non et Val di Sole','Giudicarie',
            'Riva et Ledro','Pergine','Val di Fiemme','Autres juridictions et possessions périphériques','Toute nouvelle installation Brixen']))
    t['status']='BLOCKED';t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED'
    t['installed_sub_lots'][0].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receipt)
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receipt,
        scope='TR-I-CORE only: TRT, xEDBD00, twelve cells B, 9000 residents, Sizzo, public court, capital, AUS defensive pact and installed imperial rights. Full protocol explicitly confirmed; no entire principality or diocesan approval.')
    block=('P1 : seul TR-I-CORE est restitué et validé ; la couverture temporelle complète de Trente reste non démontrée. '
        'Val di Non/Sole, Giudicarie, Riva/Ledro, Pergine, Fiemme et autres juridictions ou possessions périphériques restent à examiner, '
        'en distinguant souveraineté, seigneurie et diocèse. Reprise depuis la carte Robert 1750 et le noyau existant : '
        'confronter une carte juridictionnelle détaillée antérieure à 1776 aux RGB AUS x039D0F/x1120FF/xD040E0 et au résidu xD0BF60, '
        'puis établir des cellules B et une population comparable avant extension. Aucun transfert intégral du Sud-Tyrol ni recalage R4 recyclé. '
        'Les limites documentées du pacte défensif et de la succession capitulaire ne sont pas effacées par ce reçu.')
    t['blocking_reason']=block;t['residual_uncertainty']=block
    t['remaining_territorial_obligations']=[dict(jurisdiction=j,status='OPEN_NOT_VALIDATED',required='Dated temporal jurisdiction, defensible cell list, comparable demography and institutional qualification before extension') for j in ['Val di Non / Val di Sole','Giudicarie','Riva / Ledro','Pergine','Val di Fiemme','Other relevant peripheral jurisdictions and possessions']]
    t['current_delivery_note']=('TR-I-CORE seul PASS_RUNTIME_USER_VALIDATED : protocole intégral confirmé, TRT/xEDBD00/12 cellules/9000 habitants, '
        'Sizzo, capitale et administration, pacte défensif AUS et droits impériaux sans nouvel électorat, voisins conservés, un mois, sauvegarde/rechargement, aucun bug. '
        'Aucune date effective, capture ou mesure moteur supplémentaire inventée. SC1-TRENTO devient BLOCKED P1 pour sa couverture territoriale restante ; '
        'pas de point global ni validation des vallées ou du diocèse.')
    accept='ACCEPTANCE_'+DATE+'.md'
    (out/accept).write_text('# Reçu humain limité à TR-I-CORE\n\n**TR-I-CORE : PASS_RUNTIME_USER_VALIDATED** selon la mission conservée dans USER_VALIDATION_MISSION_2026_10_23.txt. '
        'Confirmation intégrale du protocole : noyau TRT de 12 cellules, capitale, Sizzo catholique, 9000 habitants, administration, défense AUS, droits impériaux et conservations ; un mois, sauvegarde/rechargement, aucun bug. '
        'Date effective du test inconnue, aucune capture ou mesure moteur ajoutée.\n\n**SC1-TRENTO : BLOCKED P1**, couverture globale non clôturée. '
        'Les obligations Non/Sole, Giudicarie, Riva/Ledro, Pergine, Fiemme et possessions périphériques restent ouvertes. '
        'Rapport et preuves originaux conservés. Aucun point attribué : **82/235 = 34,89 %** avant/après.\n\n'
        'Après recalcul des preuves et dépendances, **SC1-BRIXEN P1** est la prochaine tâche admissible. SC2-TYROL demeure dépendant des deux tâches territoriales non clôturées ; '
        'la seule validation des résidences ne les termine pas. Une seule nouvelle tâche est autorisée.\n',encoding='utf8')
    t['implementation_report'].append(PREFIX+accept)
    state.pop('runtime_validation_hold',None)
    state['mission_status']='TRENTO_CORE_USER_VALIDATED_REGION_BLOCKED_READY_FOR_BRIXEN'
    state['events'].append(dict(id='SERG-RM-0029',date='2026-10-23',kind='PARTIAL_RUNTIME_USER_VALIDATION_WITH_TERRITORIAL_BLOCK',
        scope_version=state['scope_version'],source=PREFIX+receipt,
        changes=[dict(task_id=lot.TASK,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='BLOCKED')],
        sub_lot_changes=[dict(id='TR-I-CORE',before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],
        before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',
        evidence=[PREFIX+receipt,PREFIX+checkfile,PREFIX+accept],note=t['current_delivery_note']+' SC1-BRIXEN P1 admissible après Salzbourg ; une seule nouvelle tâche autorisée.'))
    assert [x for x in state['tasks'] if x['id']!=lot.TASK]==[x for x in original['tasks'] if x['id']!=lot.TASK]
    assert state['events'][:-1]==original['events']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state)
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC1-BRIXEN'),p
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();rm.write_json(out/('ACCEPTANCE_TRACKER_VALIDATION_'+DATE+'.json'),checked);assert checked['status']=='PASS',checked
    print(json.dumps(dict(acceptance_checks=len(checks),tracker=checked['status'],earned=p['earned_weight'],percent=p['percent'],next=p['next_task'])),flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
