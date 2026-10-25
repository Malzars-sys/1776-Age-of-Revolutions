"""One-shot recording of the player's explicit full Moravia protocol receipt."""
import copy
import json
import shutil
import serg_sc2_moravia as lot
import serg_closure_roadmap as rm


def run():
    out = lot.OUT
    receipt = out / 'RUNTIME_USER_ATTESTATION_2026_10_19.json'
    capture = lot.load(lot.ROOT / 'docs/reports/map/SERG_CLOSURE/SC2-AUSTRIAN-SILESIA/SESSION_BEFORE.json')
    state = rm.load_json(rm.OUT / 'ROADMAP_STATE.json')
    assert state == capture['roadmap']
    original = copy.deepcopy(state)
    assert not any(e['id'] == 'SERG-RM-0008' for e in state['events']), 'Acceptance already recorded'
    before = rm.progress(state)
    task = next(t for t in state['tasks'] if t['id'] == 'SC2-MORAVIA')
    assert task['status'] == 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    baseline = lot.load(out / 'BASELINE.json')
    delivery = lot.load(out / 'DELIVERY_MANIFEST.json')
    inv = capture['inventory']
    checks = []

    def ck(name, result):
        checks.append(dict(name=name, passed=bool(result)))

    ck('Moravia tested administration file byte-identical', lot.sha(lot.ROOT / lot.ADMIN_PATH) == delivery['sha256'][lot.ADMIN_PATH])
    ck('Administration contract', lot.admin_contract((lot.ROOT / lot.ADMIN_PATH).read_text(encoding='utf8')))
    ck('Prior 51/51 static result retained', lot.load(out / 'VALIDATION.json')['passed'] == lot.load(out / 'VALIDATION.json')['total'] == 51)
    ck('Geometry sovereignty populations units and inherited diagnostics retained', all(inv[k] == baseline['inventory'][k] for k in ['owners', 'states', 'state_types', 'geometry', 'countries', 'pops', 'resolved_demographics', 'regional_pop', 'units', 'errors', 'duplicates']))
    ck('Tested bitmap retained', lot.sha(lot.ROOT / 'map_data/provinces.png') == baseline['hashes']['map_data/provinces.png'])
    ck('Tested Bohemia population file retained', lot.sha(lot.ROOT / lot.prior.POP_PATH) == baseline['hashes'][lot.prior.POP_PATH])
    ck('Registry retained', capture['registry'] == baseline['registry'])
    for key in ['buildings']:
        delta = lot.core.qa.counter(inv[key]) - lot.core.qa.counter(baseline['inventory'][key])
        ck(key + ': only new Moravia administration, no removal', len(delta) == 1 and all(k[0:2] == ('STATE_MORAVIA', 'AUS') for k in delta) and not (lot.core.qa.counter(baseline['inventory'][key]) - lot.core.qa.counter(inv[key])))
    ck('Written level delta is exactly one public administration', lot.core.qa.counter(inv['building_levels_written']) - lot.core.qa.counter(baseline['inventory']['building_levels_written']) == {'building_government_administration': 1} and not (lot.core.qa.counter(baseline['inventory']['building_levels_written']) - lot.core.qa.counter(inv['building_levels_written'])))
    current = lot.runtime_hashes()
    changed = {p: h for p, h in current.items() if capture['hashes'].get(p) != h}
    concurrent = {'common/ai_strategies/00_default_strategy.txt', 'common/combat_unit_groups/1776_engineer_corps.txt', 'common/combat_unit_types/1776_engineer_corps.txt', 'gui/1776_engineer_corps_texticons.gui'}
    ck('Concurrent engineer files isolated from territorial history', set(changed) <= concurrent and not (set(capture['hashes']) - set(current)))
    assert all(c['passed'] for c in checks), checks
    lot.dump('ACCEPTANCE_CONCURRENT_OBSERVATION_2026_10_19.json', dict(changed_runtime_files=changed, previous_hashes={p: capture['hashes'].get(p) for p in changed}, preserved_without_writing=True, territorial_history_changed=False, note='Concurrent engineer type/group, UI and AI files only; their gameplay is outside this receipt'))
    prefix = 'docs/reports/map/SERG_CLOSURE/SC2-MORAVIA/'
    lot.dump('ACCEPTANCE_TRACKER_BEFORE_2026_10_19.json', original)
    lot.dump('ACCEPTANCE_CHECK_2026_10_19.json', dict(task_ids=['SC2-MORAVIA'], status='PASS', total=len(checks), passed=len(checks), failed=[], checks=checks, automated_engine_test=False))
    attachment = lot.ROOT.__class__('C:/Users/simeo/.codex/attachments/ad42cfe8-11bb-4258-85de-297d91148c03/Texte collé.txt')
    shutil.copyfile(attachment, out / 'USER_MISSION_2026_10_19.txt')
    if not receipt.exists():
        lot.dump(receipt.name, dict(status='PASS_RUNTIME_USER_VALIDATED', task_ids=['SC2-MORAVIA'], recorded_on='2026-10-19',
            source=prefix + 'USER_MISSION_2026_10_19.txt',
            user_statement="J'ai effectué l'intégralité du protocole de validation en jeu de SC2-MORAVIA. Je valide explicitement SC2-MORAVIA : PASS_RUNTIME_USER_VALIDATED.",
            protocol=prefix + 'PLAYER_TEST_PROTOCOL.md', protocol_confirmed_as_whole=True,
            scope=dict(installed_sub_lot='MOR-I', classification='B', state='STATE_MORAVIA', country='AUS', public_administration_levels=1,
                       retained_rgb_count=10, retained_cells=2250, cadastre_validated=False, other_tasks_included=False),
            explicitly_reported=['Nouvelle partie au 1er janvier 1776', 'Toutes les vérifications du protocole réussies', "Présence et fonctionnement du niveau d'administration publique ajouté", 'Aucune anomalie constatée dans les territoires, populations et éléments contrôlés', 'Un mois de simulation réussi', 'Sauvegarde et rechargement réussis', 'Aucun crash ni bug constaté'],
            new_game_date='1776-01-01', simulation_months=1, save_and_reload=True, reported_anomalies=[], automated_engine_test=False,
            actual_test_date=None, language_tested=None, limitations='Only the installed and tested Moravia pass; no cadastral certification, Silesia/Teschen receipt, detailed budget, employment reading, test date, language, save name or engine log inferred'))
    task['status'] = 'PASS_RUNTIME_USER_VALIDATED'
    task['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED', attestation=prefix + receipt.name)
    task['decision']['authority'] = 'Explicit user receipt in USER_MISSION_2026_10_19.txt, limited to installed Moravia pass'
    task['current_delivery_note'] = "Protocole intégral explicitement réussi par le joueur : nouvelle partie 1776, niveau public fonctionnel, éléments contrôlés sans anomalie, un mois, sauvegarde/rechargement sans crash ni bug. Trois points acquis pour la seule passe Moravie; pas de validation cadastrale, Silésie ou Teschen."
    task['residual_uncertainty'] = "Fonctionnement de MOR-I confirmé par le joueur. Enveloppe B conservée, micro-frontières non cadastrées, démographie culturelle héritée; capacité technique régionale n'implique pas fusion juridique Moravie-Silésie avant 1783. Aucun relevé moteur supplémentaire inventé."
    state.pop('runtime_validation_hold', None)
    state['mission_status'] = 'SC2_MORAVIA_USER_VALIDATED_READY_FOR_NEXT'
    after = rm.progress(state)
    assert (after['earned_weight'], after['total_weight'], after['percent'], after['next_task']) == (75, 235, '31.91', 'SC2-AUSTRIAN-SILESIA')
    state['events'].append(dict(id='SERG-RM-0008', date='2026-10-19', kind='RUNTIME_USER_VALIDATION', scope_version=state['scope_version'], source=prefix + receipt.name,
        changes=[dict(task_id=task['id'], before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION', after=task['status'])], before_percent=before['percent'], after_percent=after['percent'], before_weight=72, after_weight=75, total_weight=235,
        evidence=[prefix + receipt.name, prefix + 'ACCEPTANCE_CHECK_2026_10_19.json', prefix + 'ACCEPTANCE_2026_10_19.md'],
        note="Le joueur confirme explicitement l'intégralité du protocole Moravie : nouvelle partie 1776, administration présente et fonctionnelle, éléments contrôlés sans anomalie, un mois, sauvegarde/rechargement sans crash ni bug. Reçu limité à MOR-I et aux conservations testées; aucun cadastre, futur secteur silésien ou Teschen certifié. 72/235→75/235, 30,64 %→31,91 %. Sélection recalculée SC2-AUSTRIAN-SILESIA P0 sans dépendance; une seule nouvelle étape autorisée. Ancien rapport d'installation conservé intact."))
    assert [t for t in state['tasks'] if t['id'] != task['id']] == [t for t in original['tasks'] if t['id'] != task['id']]
    assert not rm.structural_errors(state)
    (out / 'ACCEPTANCE_2026_10_19.md').write_text("# Moravie — validation utilisateur reçue le 19 octobre 2026\n\n**PASS_RUNTIME_USER_VALIDATED**, uniquement la passe MOR-I installée et les conservations du protocole. Le joueur confirme intégralement la nouvelle partie 1776, le fonctionnement de l'administration, l'absence d'anomalie, un mois, sauvegarde/rechargement sans crash ni bug. Aucun relevé détaillé supplémentaire inventé.\n\n[Attestation](RUNTIME_USER_ATTESTATION_2026_10_19.json) · [Mission intégrale](USER_MISSION_2026_10_19.txt) · [Conservation](ACCEPTANCE_CHECK_2026_10_19.json). Le rapport REPORT.md reste le document historique de livraison avant reçu, intact.\n\nProgression vérifiée : **72/235 = 30,64 % → 75/235 = 31,91 %**. Les frontières cadastrales et tâches Silésie/Teschen/MAP2A restent distinctes. Prochaine tâche calculée : SC2-AUSTRIAN-SILESIA, P0 sans dépendance. Aucun texte de journal ajouté dans MOR-I ne nécessite de seconde passe immersive.\n", encoding='utf8')
    task['implementation_report'].append(prefix + 'ACCEPTANCE_2026_10_19.md')
    rm.write_json(rm.OUT / 'ROADMAP_STATE.json', state)
    rm.render()
    result = rm.check()
    lot.dump('ACCEPTANCE_TRACKER_VALIDATION_2026_10_19.json', result)
    assert result['status'] == 'PASS', result
    print('Moravia receipt recorded; tracker PASS; 75/235 = 31.91%; next SC2-AUSTRIAN-SILESIA')


if __name__ == '__main__':
    run()
