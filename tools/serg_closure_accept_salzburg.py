"""Record the player's 2026-10-19 receipt for the installed SC1 nucleus only."""
import copy,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import serg_closure_roadmap as rm
import serg_sc1_salzburg as slz

OUT=slz.OUT
def write(name,obj):slz.dump(name,obj)

def run():
    receipt=OUT/'RUNTIME_USER_ATTESTATION_2026_10_19.json'
    assert not receipt.exists(),'Receipt already recorded; do not duplicate or overwrite'
    state=rm.load_json(rm.OUT/'ROADMAP_STATE.json');before=rm.progress(state);original=copy.deepcopy(state)
    task=next(t for t in state['tasks'] if t['id']=='SC1-SALZBURG')
    assert task['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    geo=slz.load(OUT/'GEOMETRY.json');current=slz.core.packed(slz.ROOT/'map_data/provinces.png')
    cells=next(r['cells'] for r in geo['assignments'] if r['owner']=='SLZ')
    yy,xx=np.where(current==0xEDBB00)
    assert sorted(map(list,zip(map(int,xx),map(int,yy))))==cells and len(cells)==12
    assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
    delivery=slz.load(OUT/'DELIVERY_MANIFEST.json')
    runtime=slz.prior.pas.prior.q.economy.runtime_hashes()
    changed=[p for p in slz.load(OUT/'FILES_MODIFIED.json')['runtime_files'] if runtime.get(p)!=delivery['sha256'][p]]
    assert not changed,'Review differences from tested scoped delivery first: '+str(changed)
    static=slz.load(OUT/'VALIDATION.json')
    assert static['passed']==static['total'] and not static['failed'] and 'SC1-SALZBURG' in static['task_ids']
    write('ACCEPTANCE_TRACKER_BEFORE_2026_10_19.json',state)
    write('ACCEPTANCE_CHECK_2026_10_19.json',dict(task_ids=['SC1-SALZBURG'],status='PASS',total=4,passed=4,failed=[],
        checks=['Exact installed 12-cell footprint','B classification retained','Tested functional delivery byte-identical','Existing 209/209 static evidence valid'],
        runtime_files_changed_since_delivery=changed,geometry_sha256=slz.sha(OUT/'GEOMETRY.json'),automated_engine_test=False))
    quote="J'ai effectué le protocole de validation en jeu de `SC1-SALZBURG` et toutes les vérifications ont réussi : nouvelle partie en 1776, contrôles du prince-archevêché de Salzbourg, un mois de simulation, sauvegarde et rechargement. Aucune anomalie constatée."
    write(receipt.name,dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=['SC1-SALZBURG'],recorded_on='2026-10-19',
        source='Explicit player confirmation in this Codex conversation, received 2026-10-19 (Europe/Paris)',user_statement=quote,
        scope=dict(classification='B_POLITICAL_APPROXIMATION',country='SLZ',rgb='xEDBB00',state='STATE_BAVARIA',state_id=71,cells=cells,count=12,
            geometry='docs/reports/map/SERG_CLOSURE/SC1-SALZBURG/GEOMETRY.json',peripheral_territories_included=False),
        protocol='docs/reports/map/SERG_CLOSURE/SC1-SALZBURG/PLAYER_TEST_PROTOCOL.md',new_game_date='1776-01-01',
        simulation_months=1,save_and_reload=True,reported_anomalies=[],automated_engine_test=False,
        limitations='Player confirms completion of the protocol as a whole; no additional itemized observations, language, save name, test date or engine log invented',
        actual_test_date=None,language_tested=None))
    prefix='docs/reports/map/SERG_CLOSURE/SC1-SALZBURG/'
    task['status']='PASS_RUNTIME_USER_VALIDATED'
    task['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=prefix+receipt.name)
    task['residual_uncertainty']='Noyau de résidence B de 12 cellules seulement, protocole global confirmé sans anomalie par le joueur. Périphéries (Berchtesgaden, Rupertiwinkel, Mühldorf, Pinzgau/Pongau/Lungau, possessions tyroliennes et autres) non reconstituées; résidus BAV/AUS non certifiés. Démographie urbaine arrondie, minorités non quantifiées; aucun résultat chiffré moteur supplémentaire inventé.'
    task['current_delivery_note']='Noyau B SLZ de 12 cellules validé explicitement par le joueur le 19 octobre 2026 : protocole nouvelle partie 1776, un mois, sauvegarde/rechargement réussi, aucune anomalie signalée. Six points acquis; aucune validation des périphéries.'
    state.pop('runtime_validation_hold',None)
    state['mission_status']='SC1_SALZBURG_USER_VALIDATED_READY_FOR_NEXT'
    after=rm.progress(state)
    assert (after['earned_weight'],after['total_weight'],after['percent'],after['next_task'])==(66,235,'28.09','SC2-BOHEMIA')
    state['events'].append(dict(id='SERG-RM-0004',date='2026-10-19',kind='RUNTIME_USER_VALIDATION',scope_version=state['scope_version'],
        source=prefix+receipt.name,changes=[dict(task_id='SC1-SALZBURG',before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],
        before_percent=before['percent'],after_percent=after['percent'],before_weight=60,after_weight=66,total_weight=235,
        evidence=[prefix+receipt.name,prefix+'ACCEPTANCE_CHECK_2026_10_19.json',prefix+'VALIDATION.json'],
        note='Confirmation utilisateur enregistrée pour le seul noyau B Salzbourg de 12 cellules. Nouvelle partie 1776, protocole global réussi, un mois, sauvegarde et rechargement; aucune anomalie déclarée. Aucun détail supplémentaire de test inventé; aucune frontière périphérique validée. 60/235 → 66/235, 25,53 % → 28,09 %. Sélection recalculée : SC2-BOHEMIA, P0 sans dépendance, autorisé dans la même demande.'))
    assert not rm.structural_errors(state),rm.structural_errors(state)
    assert [t for t in state['tasks'] if t['id']!='SC1-SALZBURG']==[t for t in original['tasks'] if t['id']!='SC1-SALZBURG']
    report=OUT/'REPORT.md';archived=OUT/'REPORT_INSTALLED_2026_10_18.md'
    assert not archived.exists();archived.write_bytes(report.read_bytes())
    text=report.read_text(encoding='utf8')
    text='# Validation reçue le 19 octobre 2026\n\n**PASS_RUNTIME_USER_VALIDATED — noyau B de Salzbourg, 12 cellules seulement.**\n\nLe joueur confirme le protocole complet : nouvelle partie en 1776, contrôles du prince-archevêché, un mois, sauvegarde et rechargement réussis, aucune anomalie signalée. Aucun détail supplémentaire n’est déduit. [Attestation](RUNTIME_USER_ATTESTATION_2026_10_19.json) · [Conservation de la livraison testée](ACCEPTANCE_CHECK_2026_10_19.json).\n\nProgression après validation : **66/235 = 28,09 %**, contre 60/235 = 25,53 %. Prochaine tâche recalculée : **SC2-BOHEMIA**, autorisée par le joueur. Les possessions périphériques restent exclues du reçu.\n\nLe rapport d’installation ci-dessous est conservé comme compte rendu daté du 18 octobre ; ses mentions de test encore attendu décrivent cet état antérieur. L’original immuable est [archivé ici](REPORT_INSTALLED_2026_10_18.md). Aucun texte de journal technique n’a été introduit par SC1 ; le gouvernement possède déjà son texte immersif FR/EN.\n\n---\n\n'+text
    report.write_text(text,encoding='utf8')
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state);rm.render()
    check=rm.check();assert check['status']=='PASS',check
    write('ACCEPTANCE_TRACKER_VALIDATION_2026_10_19.json',check)
    print('Accepted SC1-SALZBURG; 66/235 = 28.09%; next SC2-BOHEMIA')

if __name__=='__main__':run()
