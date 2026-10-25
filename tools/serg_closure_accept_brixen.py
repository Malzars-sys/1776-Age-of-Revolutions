"""Record the player's BR-I-CORE receipt, never close the whole region."""
import contextlib,copy,io,json,os,subprocess,sys
from pathlib import Path
import numpy as np
import serg_sc1_brixen as lot
DATE='2026_10_23';PREFIX=lot.PREFIX
SOURCE=Path('C:/Users/simeo/.codex/attachments/1e4e02a3-f955-41a1-bae1-adb66732e090/Texte collé.txt')
CAPTURE=lot.OUT/('ACCEPTANCE_SESSION_BEFORE_'+DATE+'.json')
os.environ['GIT_OPTIONAL_LOCKS']='0'

def capture():
    assert not CAPTURE.exists()
    state=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');assert state['events'][-1]['id']=='SERG-RM-0030'
    manifest=lot.load(lot.OUT/'DELIVERY_MANIFEST.json')['files']
    changed=[p for p,h in manifest.items() if not (lot.ROOT/p).is_file() or lot.sha(lot.ROOT/p)!=h]
    hashes=lot.prior.prior.italian.runtime_hashes();old=lot.load(lot.OUT/'SESSION_AFTER.json')['hashes']
    concurrent=sorted(p for p in set(hashes)|set(old) if hashes.get(p)!=old.get(p))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=lot.ROOT,text=True).strip()
    lot.rm.write_json(CAPTURE,dict(roadmap=state,inventory=lot.core.qa.inventory(),hashes=hashes,registry=lot.load(lot.reg.active_registry_path()),delivery_manifest_changes=changed,concurrent_runtime_changes=concurrent,git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=lot.sha(lot.ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal'))))
    print(json.dumps(dict(manifest_changes=changed,concurrent_changes=concurrent)),flush=True)

def run():
    out,rm=lot.OUT,lot.rm;b=lot.load(CAPTURE);state=lot.load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==b['roadmap'] and state['events'][-1]['id']=='SERG-RM-0030'
    receipt='RUNTIME_USER_ATTESTATION_'+DATE+'.json';assert not (out/receipt).exists();checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    ck('111-file Brixen delivery manifest intact',not b['delivery_manifest_changes'])
    owned=set(lot.load(out/'FILES_MODIFIED.json')['runtime_files']);ck('Concurrent changes outside delivered Brixen files',not owned.intersection(b['concurrent_runtime_changes']))
    ck('Current runtime equals captured entry',lot.prior.prior.italian.runtime_hashes()==b['hashes'])
    ck('World history inventory equals delivered Brixen inventory',b['inventory']==lot.load(out/'SESSION_AFTER_STATIC.json')['inventory'])
    rel=lot.reg.active_registry_path().relative_to(lot.ROOT).as_posix();ck('577 imperial rights retained',len(b['registry'])==577 and lot.sha(lot.reg.active_registry_path())==lot.load(out/'DELIVERY_MANIFEST.json')['files'][rel])
    v=lot.load(out/'VALIDATION.json');ck('166/166 static evidence intact',v['passed']==v['total']==166 and not v['failed'])
    ck('24 justified tasks remain credited',sum(rm.qualifications(state).values())==24)
    t=next(t for t in state['tasks'] if t['id']==lot.TASK);ck('Only BR-I-CORE pending in BLOCKED P1 region',t['status']=='BLOCKED' and t['priority']=='P1' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and [s['id'] for s in t['installed_sub_lots']]==['BR-I-CORE'])
    bitmap=lot.core.packed(lot.ROOT/'map_data/provinces.png');ys,xs=np.where(bitmap==int(lot.RGB[1:],16));ck('Exact nine delivered cells retained',sorted(map(list,zip(xs.tolist(),ys.tolist())))==sorted(lot.CELLS))
    assert all(c['passed'] for c in checks),checks
    checkfile='ACCEPTANCE_CHECK_'+DATE+'.json';rm.write_json(out/checkfile,dict(task_ids=[lot.TASK],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    sourcename='USER_VALIDATION_MISSION_'+DATE+'.txt';(out/sourcename).write_bytes(SOURCE.read_bytes())
    rm.write_json(out/receipt,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[lot.TASK],sub_lot_ids=['BR-I-CORE'],scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-23',source=PREFIX+sourcename,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,
        explicitly_reported=['Nouvelle partie au 1er janvier 1776','BRX apparaît correctement ; noyau de neuf cellules fonctionnel','Brixen capitale à l’intérieur du territoire BRX','Leopold Maria Joseph von Spaur prince-évêque présent','Gouvernement théocratique catholique fonctionnel','3000 habitants initiaux présents','Chancellerie publique de 200 postes fonctionnelle','Pacte défensif AUS–BRX correctement représenté','BRX dans le système impérial sans dixième électeur','Trente, Bolzano, Merano, Innsbruck, Lienz et voisins contrôlés préservés','Un mois complet sans anomalie','Sauvegarde et rechargement réussis','Aucun problème pendant le protocole'],
        new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,actual_test_date=None,language_tested=None,automated_engine_test=False,reported_anomalies=[],additional_observations_invented=False,
        validated_scope=dict(tag='BRX',rgb=lot.RGB,cells=lot.CELLS,category='B',population=3000),excluded=['Clôture territoriale globale SC1-BRIXEN','Bruneck et juridictions du Pustertal','Klausen et Feldthurns','Ressorts ruraux','Enclaves et possessions éloignées','Limites complètes des souverainetés et droits','Population des territoires non installés','Toute nouvelle installation Berchtesgaden']))
    obligations=copy.deepcopy(t['remaining_territorial_obligations']);block=t['blocking_reason']
    t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED';t['installed_sub_lots'][0].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receipt,scope='BR-I-CORE only; nine-cell political residence B with all delivered protocol explicitly confirmed by the player. No complete territorial or diocesan closure.')
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=PREFIX+receipt,scope='BR-I-CORE only: BRX, xEDBE00, nine cells B, 3000 residents, Leopold, theocracy, public chancery, capital, AUS defensive pact and installed imperial rights. No entire principality approval.')
    t['current_delivery_note']=('BR-I-CORE seul PASS_RUNTIME_USER_VALIDATED : protocole intégral confirmé par le joueur, BRX/xEDBE00/neuf cellules/3000 habitants, capitale Brixen dans le noyau, Leopold, théocratie catholique, chancellerie publique de 200 postes, pacte AUS–BRX et droits impériaux sans dixième électeur ; voisins contrôlés préservés, un mois sans anomalie, sauvegarde/rechargement réussis. Aucune date effective, capture ou mesure moteur ajoutée. SC1-BRIXEN reste BLOCKED P1 pour ses juridictions, enclaves, frontières et populations périphériques ; zéro point régional.')
    accept='ACCEPTANCE_'+DATE+'.md';(out/accept).write_text('# Attestation humaine limitée à BR-I-CORE\n\n'+t['current_delivery_note']+'\n\n'+block+'\n\nLes cinq obligations structurées restent exactement ouvertes. Rapport et preuves d’installation originaux conservés. **82/235 = 34,89 %** avant/après. Après recalcul et validateur, SC1-BERCHTESGADEN P1 est la prochaine étape indépendante admissible ; le Tyrol demeure dépendant des deux régions Trente/Brixen non closes.\n',encoding='utf8');t['implementation_report'].append(PREFIX+accept)
    state.pop('runtime_validation_hold',None);state['mission_status']='BRIXEN_CORE_USER_VALIDATED_REGION_BLOCKED_READY_FOR_BERCHTESGADEN'
    state['events'].append(dict(id='SERG-RM-0031',date='2026-10-23',kind='PARTIAL_RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],source=PREFIX+receipt,changes=[dict(task_id=lot.TASK,before='BLOCKED',after='BLOCKED')],sub_lot_changes=[dict(id='BR-I-CORE',before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+receipt,PREFIX+checkfile,PREFIX+accept],note=t['current_delivery_note']+' Obligations restantes conservées ; SC1-BERCHTESGADEN P1 admissible après Salzbourg, seule nouvelle étape autorisée.'))
    assert t['status']=='BLOCKED' and t['remaining_territorial_obligations']==obligations and t['blocking_reason']==block
    assert [x for x in state['tasks'] if x['id']!=lot.TASK]==[x for x in original['tasks'] if x['id']!=lot.TASK] and state['events'][:-1]==original['events']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state)
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,'SC1-BERCHTESGADEN'),p
    assert not rm.structural_errors(state),rm.structural_errors(state);rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();rm.write_json(out/('ACCEPTANCE_TRACKER_VALIDATION_'+DATE+'.json'),checked);assert checked['status']=='PASS',checked
    print(json.dumps(dict(acceptance_checks=len(checks),tracker=checked['status'],earned=p['earned_weight'],percent=p['percent'],next=p['next_task'])),flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
