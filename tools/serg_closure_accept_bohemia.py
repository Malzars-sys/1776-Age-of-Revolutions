"""Record the user's explicit correction confirming the full Bohemia protocol."""
import copy,json,shutil
from pathlib import Path
import serg_sc2_bohemia as lot
import serg_closure_roadmap as rm

def run():
    out=lot.OUT;receipt=out/'RUNTIME_USER_ATTESTATION_2026_10_19.json'
    assert not receipt.exists(),'Never replace or duplicate a receipt'
    state=rm.load_json(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state);before=rm.progress(state)
    task=next(t for t in state['tasks'] if t['id']=='SC2-BOHEMIA')
    assert task['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    base=lot.load(out/'BASELINE.json');delivery=lot.load(out/'DELIVERY_MANIFEST.json');v=lot.load(out/'VALIDATION.json')
    checks=[]
    def ck(name,value):checks.append(dict(name=name,passed=bool(value)))
    ck('Tested population file byte-identical',all(lot.sha(lot.ROOT/p)==delivery['sha256'][p] for p in delivery['runtime_files']))
    ck('Installed nine-value correction and protected surrounding bytes',lot.validate_scope((out/'POPS_BEFORE.txt').read_bytes().decode('utf8'),(lot.ROOT/lot.POP_PATH).read_bytes().decode('utf8')))
    ck('35 static checks retained',v['passed']==v['total']==35 and not v['failed'])
    inv=lot.core.qa.inventory()
    ck('Geometry and sovereignty unchanged',all(inv[k]==base['inventory'][k] for k in ['owners','states','state_types','geometry','countries']))
    ck('Buildings units and dependencies unchanged',all(inv[k]==base['inventory'][k] for k in ['buildings','building_levels_written','units','errors','duplicates']))
    ck('Exact tested bitmap preserved',lot.sha(lot.ROOT/'map_data/provinces.png')==base['hashes']['map_data/provinces.png'])
    ck('Written Bohemia population remains 2500000',sum(r['count'] for r in inv['regional_pop'] if r['key'][0]=='STATE_BOHEMIA')==2_500_000)
    assert all(c['passed'] for c in checks),checks
    lot.dump('ACCEPTANCE_TRACKER_BEFORE_2026_10_19.json',original)
    lot.dump('ACCEPTANCE_CHECK_2026_10_19.json',dict(task_ids=['SC2-BOHEMIA'],status='PASS',total=len(checks),passed=len(checks),failed=[],checks=checks,automated_engine_test=False))
    attachment=Path('C:/Users/simeo/.codex/attachments/f0a5854b-11cd-490f-985c-acaceeb17bf0/Texte collé.txt')
    shutil.copyfile(attachment,out/'USER_MISSION_2026_10_19.txt')
    prefix='docs/reports/map/SERG_CLOSURE/SC2-BOHEMIA/'
    quote="rectification l'ai passé un moi et rechargé sans crash et sans bug tous passe"
    lot.dump(receipt.name,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=['SC2-BOHEMIA'],recorded_on='2026-10-19',
        source='Explicit current user correction in this Codex conversation, together with attached mission identifying the last installation as SC2-BOHEMIA',
        user_statement=quote,attachment=prefix+'USER_MISSION_2026_10_19.txt',
        supersedes='The attachment described launch only; the accompanying correction explicitly confirms one month, reload without crash/bug, and all checks passing',
        scope=dict(classification='B_GENERALIZED_ENVELOPE_RETAINED_WITH_DEMOGRAPHIC_CORRECTION',installed_sub_lot='BOH-D',state='STATE_BOHEMIA',state_id=52,country='AUS',population_written=2500000,
            rgb_count=21,cells=4412,other_sectors='BOH-W/N/E/S/I retained envelope and dependencies',cadastre_validated=False,other_tasks_included=False),
        protocol=prefix+'PLAYER_TEST_PROTOCOL.md',protocol_confirmed_as_whole=True,new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,
        reported_anomalies=[],automated_engine_test=False,actual_test_date=None,language_tested=None,
        limitations='Global success declaration only; no additional itemized demographic/economic readings, save name, language, actual test date or engine log inferred'))
    task['status']='PASS_RUNTIME_USER_VALIDATED';task['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=prefix+receipt.name)
    task['current_delivery_note']='Protocole global confirmé par rectification explicite du joueur : un mois et rechargement sans crash ni bug, toutes vérifications réussies. Reçu limité à la passe BOH-D et à son enveloppe conservée; six points acquis. Aucun relevé moteur détaillé supplémentaire inventé.'
    task['residual_uncertainty']='Validation fonctionnelle globale reçue. Enveloppe B générale, pas cadastre ni recalage cellule par cellule; micro-limites Eger/Asch/Glatz et enclaves non certifiées. Total de scénario 2,5 M arrondi, proportions culturelles/sociales héritées; aucun chiffre économique observé supplémentaire inventé.'
    state.pop('runtime_validation_hold',None);state['mission_status']='SC2_BOHEMIA_USER_VALIDATED_READY_FOR_NEXT'
    after=rm.progress(state);assert (after['earned_weight'],after['total_weight'],after['percent'],after['next_task'])==(72,235,'30.64','SC2-MORAVIA')
    state['events'].append(dict(id='SERG-RM-0006',date='2026-10-19',kind='RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],source=prefix+receipt.name,
        changes=[dict(task_id='SC2-BOHEMIA',before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],
        before_percent=before['percent'],after_percent=after['percent'],before_weight=66,after_weight=72,total_weight=235,
        evidence=[prefix+receipt.name,prefix+'ACCEPTANCE_CHECK_2026_10_19.json',prefix+'VALIDATION.json'],
        note='La rectification directe du joueur remplace la mention de lancement seul du document joint : un mois, rechargement sans crash/bug, toutes vérifications réussies. Validation globale du protocole SC2-BOHEMIA, sans inventer de relevés détaillés; pas extension à MAP2A, Moravie, Silésie ou cadastre. Population testée inchangée. 66/235→72/235, 28,09 %→30,64 %. Sélection recalculée SC2-MORAVIA P0 sans dépendance; une seule nouvelle étape autorisée par la mission jointe.'))
    assert [t for t in state['tasks'] if t['id']!='SC2-BOHEMIA']==[t for t in original['tasks'] if t['id']!='SC2-BOHEMIA']
    assert not rm.structural_errors(state)
    report=out/'REPORT.md';archived=out/'REPORT_INSTALLED_2026_10_19.md';assert not archived.exists();shutil.copyfile(report,archived)
    report.write_text('# Validation utilisateur reçue — 19 octobre 2026\n\n**PASS_RUNTIME_USER_VALIDATED — SC2-BOHEMIA, périmètre de la passe BOH-D et enveloppe conservée.**\n\nLa rectification du joueur confirme le mois de simulation, le rechargement sans crash ni bug et la réussite de toutes les vérifications. Elle remplace la mention de lancement seul du document joint. Aucun détail moteur supplémentaire inventé. [Attestation](RUNTIME_USER_ATTESTATION_2026_10_19.json) · [Conservation](ACCEPTANCE_CHECK_2026_10_19.json).\n\nProgression : **66/235 = 28,09 % → 72/235 = 30,64 %**. Prochaine étape autorisée et recalculée : **SC2-MORAVIA**, P0 sans dépendance. Les réserves historiques B restent conservées.\n\nLe [rapport d’installation archivé](REPORT_INSTALLED_2026_10_19.md) ci-dessous décrit la livraison avant ce reçu; ses mentions de test attendu sont datées.\n\n---\n\n'+archived.read_text(encoding='utf8'),encoding='utf8')
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state);rm.render();check=rm.check();lot.dump('ACCEPTANCE_TRACKER_VALIDATION_2026_10_19.json',check)
    assert check['status']=='PASS';print('Bohemia accepted: 72/235=30.64%; next SC2-MORAVIA')

if __name__=='__main__':run()
