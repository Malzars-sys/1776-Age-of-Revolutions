"""Two separate user receipts, with the later BGT salt revision explicitly unvalidated."""
import contextlib,copy,io,json,os,shutil,subprocess,sys
from pathlib import Path
import numpy as np
import serg_sc1_passau_outliers as ps
ROOT=ps.ROOT;rm=ps.rm;core=ps.core;sha=ps.sha;load=ps.load
BG=ps.prior;OUT=rm.OUT/'ACCEPTANCES_2026_10_24';PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
SOURCE=Path('C:/Users/simeo/.codex/attachments/3fcb1fe5-d3af-4ea7-bd31-c21d285f20eb/Texte collé.txt')
DATE='2026_10_24';REVISION='BG-E-SALT-NATIVE-R1'
os.environ['GIT_OPTIONAL_LOCKS']='0'
def dump(n,data):rm.write_json(OUT/n,data)

def capture():
    assert not (OUT/'BASELINE.json').exists();OUT.mkdir(exist_ok=True)
    s=load(rm.OUT/'ROADMAP_STATE.json');assert s['events'][-1]['id']=='SERG-RM-0034';assert rm.check()['status']=='PASS'
    cur=BG.italian.runtime_hashes();previous=load(ps.OUT/'SESSION_AFTER_STATIC.json')['hashes'];git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    manifest=load(ps.OUT/'DELIVERY_MANIFEST.json')['files'];diff=[p for p,h in manifest.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    dump('BASELINE.json',dict(roadmap=s,hashes=cur,inventory=core.qa.inventory(),registry=load(ps.reg.active_registry_path()),manifest_changes=diff,concurrent_runtime_changes=sorted(p for p in set(cur)|set(previous) if cur.get(p)!=previous.get(p)),proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents},tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    shutil.copyfile(SOURCE,OUT/'USER_MISSION.txt');print('Acceptance baseline captured; manifest differences',diff,flush=True)

def run():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');assert s==b['roadmap']
    assert not b['manifest_changes'] and BG.italian.runtime_hashes()==b['hashes']
    # Preserve the tracker source before the version-aware structural extension.
    tracker='tools/serg_closure_roadmap.py'
    dump('TRACKER_CHANGE.json',dict(file=tracker,before_sha256=b['tools'][tracker],after_sha256=sha(ROOT/tracker),qualification_formula_changed=False,reason='Represent a historical accepted sub-lot and a later unvalidated revision separately; no task, weight or qualification change.'))
    checks={};a=core.packed(ROOT/'map_data/provinces.png')
    for module,subid,number,quote in [(BG,'BG-I-CORE',35,"J'ai suivi intégralement le protocole SC1-BERCHTESGADEN et toutes les vérifications ont réussi, notamment la capitale, la saline, les finances, un mois de simulation et la sauvegarde/rechargement."),(ps,'PS-OB-CORE',36,"J'ai suivi intégralement le protocole SC1-PASSAU-OUTLIERS : Obernberg fonctionne, toutes les vérifications ont réussi, y compris un mois de simulation et la sauvegarde/rechargement.")]:
        t=next(t for t in s['tasks'] if t['id']==module.TASK);old=copy.deepcopy(t)
        assert t['status']=='BLOCKED' and t['priority']=='P1' and len(t['remaining_territorial_obligations'])==6
        ys,xs=np.where(a==int(module.RGB[1:],16));assert sorted(map(list,zip(xs.tolist(),ys.tolist())))==sorted(module.CELLS)
        fn='RUNTIME_USER_ATTESTATION_'+DATE+'.json';ref=module.PREFIX+fn;source='USER_VALIDATION_MISSION_'+DATE+'.txt';assert not (module.OUT/fn).exists()
        (module.OUT/source).write_bytes(SOURCE.read_bytes())
        receipt=dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[module.TASK],sub_lot_ids=[subid],scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-24',source=module.PREFIX+source,source_type='EXPLICIT_USER_RESTATEMENT_OF_PRIOR_VALIDATION' if module is BG else 'EXPLICIT_USER_VALIDATION',verbatim_confirmation=quote,protocol=module.PREFIX+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,actual_test_date=None,language_tested=None,automated_engine_test=False,additional_observations_invented=False,common_game_claimed=False,validated_scope=dict(tag=module.TAG,rgb=module.RGB,cells=module.CELLS,population=module.POP,category='B'),reported_anomalies=[])
        if module is BG:
            receipt.update(validated_delivery_version='BG_ORIGINAL_SALINE_100_JOBS',tested_delivery_manifest=BG.PREFIX+'DELIVERY_MANIFEST.json',tested_delivery_manifest_sha256=sha(BG.OUT/'DELIVERY_MANIFEST.json'),excludes_later_revisions=True,excluded_revision_ids=[REVISION],explicitly_reported=['Capitale Berchtesgaden','Franz Anton Josef von Hausen-Gleichenstorff','Théocratie catholique','1000 habitants initiaux','Chancellerie publique 100 postes','Petite saline Frauenreuth 100 postes','Production du sel et finances selon protocole','Droits impériaux du noyau','Voisins contrôlés préservés','Un mois complet','Sauvegarde et rechargement'],excluded=['Mine de sel ordinaire ultérieure et toute autre version technique postérieure','Clôture régionale et possessions périphériques'])
        else:receipt.update(explicitly_reported=['Enclave Obernberg PAS fonctionnelle','Quatre cellules dans STATE_AUSTRIA','1400 habitants transférés','Noyau principal et capitale Passau conservés','Démographie et propriétaires voisins vérifiés conservés','Droits impériaux associés','Un mois sans anomalie','Sauvegarde et rechargement'],excluded=['Clôture régionale passavienne','Certification historique du voisinage Innviertel','Révision mine ordinaire BGT'])
        rm.write_json(module.OUT/fn,receipt)
        t['installed_sub_lots'][0].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=ref)
        if module is BG:
            protocol=BG.PREFIX+'PLAYER_TEST_PROTOCOL_SALT_NATIVE_REVISION_'+DATE+'.md'
            (ROOT/protocol).write_text('# Mine ordinaire de Berchtesgaden — révision seule\n\nLe noyau BG-I-CORE avec ancienne saline est déjà validé. Ce contrôle ne refait pas cette attestation.\n\nNouvelle partie 1776 : ouvrir BGT, vérifier une mine de sel standard de niveau 1, visible dans les bâtiments, partiellement employée avec 1000 habitants et chancellerie conservée. Observer production du sel, emploi et finances sans seuil de rentabilité imposé. Simuler un mois, sauvegarder puis recharger ; signaler les résultats réels. Aucun résultat présumé.\n',encoding='utf8')
            t['installed_sub_lots'][0]['validated_delivery_version']='BG_ORIGINAL_SALINE_100_JOBS'
            t['historical_validated_delivery_version']='BG_ORIGINAL_SALINE_100_JOBS'
            t['historical_runtime_validation']=dict(t['runtime_validation'],status='PASS_RUNTIME_USER_VALIDATED',attestation=ref,scope='Original BG-I-CORE with Frauenreuth special saline 100 jobs only; later native mine excluded.')
            t['installed_sub_lots'].append(dict(id=REVISION,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',supersedes_sub_lot=subid,supersedes_delivery_version='BG_ORIGINAL_SALINE_100_JOBS',attestation=None,protocol=protocol,scope='One ordinary salt mine level; partial staffing; no new population or political revision.'))
            t['runtime_validation'].update(status='RETEST_REQUIRED',attestation=None,protocol=protocol,pending_revision_ids=[REVISION],scope='Later ordinary salt mine revision only; historical core already accepted.')
            t['delivered_scope']['sub_lots'].append(REVISION)
            t['current_delivery_note']='BG-I-CORE PASS_RUNTIME_USER_VALIDATED dans sa version originale avec saline Frauenreuth de 100 postes. Reçu humain réel enregistré séparément. La mine de sel ordinaire ultérieure BG-E-SALT-NATIVE-R1 reste IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION et ne bénéficie pas du reçu. Région BLOCKED P1, six obligations conservées, zéro point.'
        else:
            t['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED';t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=ref,scope='PS-OB-CORE only; four cells and 1400 inhabitants; no Innviertel or regional approval.')
            t['current_delivery_note']='PS-OB-CORE seul PASS_RUNTIME_USER_VALIDATED : protocole Obernberg intégral confirmé, PAS/xEDC000/quatre cellules/1400 habitants, ancien noyau et capitale conservés, droits impériaux, voisins vérifiés, un mois et sauvegarde/rechargement. Région BLOCKED P1, six obligations conservées, zéro point.'
        assert t['remaining_territorial_obligations']==old['remaining_territorial_obligations'] and t['blocking_reason']==old['blocking_reason']
        note='ACCEPTANCE_'+DATE+'.md';(module.OUT/note).write_text('# Attestation humaine bornée — '+subid+'\n\n'+t['current_delivery_note']+'\n\nDate effective du test inconnue ; aucune capture ou mesure supplémentaire inventée. Protocoles distincts possibles, aucune nouvelle partie commune prétendue. Archives de livraison inchangées.\n',encoding='utf8');t['implementation_report'].append(module.PREFIX+note)
        s['events'].append(dict(id='SERG-RM-00'+str(number),date='2026-10-24',kind='VERSION_SCOPED_PARTIAL_RUNTIME_USER_VALIDATION',scope_version=s['scope_version'],source=ref,changes=[dict(task_id=module.TASK,before='BLOCKED',after='BLOCKED')],sub_lot_changes=[dict(id=subid,before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[ref,module.PREFIX+note],note=t['current_delivery_note']))
        checks[subid]=dict(exact_cells_verified=True,regional_obligations_preserved=True,receipt=ref,old_static_checks=load(module.OUT/'VALIDATION.json')['passed'])
    s.pop('runtime_validation_hold',None);s['mission_status']='TWO_SCOPED_RECEIPTS_RECORDED_BG_NATIVE_REVISION_PENDING_READY_FOR_REGENSBURG'
    p=rm.progress(s);assert (p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['next_task'])==(82,235,24,'SC1-REGENSBURG-DEMOGRAPHY'),p
    assert not rm.structural_errors(s),rm.structural_errors(s)
    assert s['events'][:-2]==b['roadmap']['events'] and rm.qualifications(s)==rm.qualifications(b['roadmap'])
    assert all(sha(ROOT/rel)==h for rel,h in b['proofs'].items() if Path(rel).parent!=rm.OUT.relative_to(ROOT))
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS'
    dump('ACCEPTANCE_CHECKS.json',dict(status='PASS',checks=checks,runtime_unchanged=BG.italian.runtime_hashes()==b['hashes'],previous_nested_proofs_unchanged=True,progress=p,automated_engine_test=False))
    print('Both scoped receipts recorded and canonical check PASS; selected',p['next_task'],flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
