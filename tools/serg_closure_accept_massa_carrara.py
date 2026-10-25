"""Record the player's explicit MC-I-CORE receipt, without regional credit."""
import contextlib
import copy
import io
import json
import os
import subprocess
from pathlib import Path
import serg_sc4_massa_carrara as lot

DATE = '2026_10_23'
PREFIX = 'docs/reports/map/SERG_CLOSURE/SC4-MASSA-CARRARA/'
CAPTURE = lot.OUT / ('ACCEPTANCE_SESSION_BEFORE_' + DATE + '.json')
SOURCE = Path('C:/Users/simeo/.codex/attachments/fa3eb65a-e925-4a80-977a-b93d2d39e32d/Texte collé.txt')


def capture():
    assert not CAPTURE.exists()
    state = lot.load(lot.rm.OUT / 'ROADMAP_STATE.json')
    assert state['events'][-1]['id'] == 'SERG-RM-0026'
    manifest = lot.load(lot.OUT / 'DELIVERY_MANIFEST.json')['files']
    changed = [p for p, h in manifest.items() if not (lot.ROOT / p).is_file() or lot.sha(lot.ROOT / p) != h]
    hashes = lot.italian.runtime_hashes()
    old = lot.load(lot.OUT / 'SESSION_AFTER.json')['hashes']
    concurrent = sorted(p for p in set(hashes) | set(old) if hashes.get(p) != old.get(p))
    inv = lot.core.qa.inventory()
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    git = lambda *args: subprocess.check_output(['git', *args], cwd=lot.ROOT, text=True, env=env).strip()
    lot.rm.write_json(CAPTURE, dict(roadmap=state, inventory=inv, hashes=hashes,
        registry=lot.load(lot.reg.active_registry_path()), delivery_manifest_changes=changed,
        concurrent_runtime_changes=concurrent,
        git=dict(head=git('rev-parse', 'HEAD'), branch=git('branch', '--show-current'),
                 index_sha256=lot.sha(lot.ROOT / '.git/index'), status=git('status', '--short', '--untracked-files=normal'))))
    print(json.dumps(dict(manifest_changes=changed, concurrent_changes=concurrent)), flush=True)


def run():
    out, rm = lot.OUT, lot.rm
    baseline = lot.load(CAPTURE)
    state = lot.load(rm.OUT / 'ROADMAP_STATE.json')
    original = copy.deepcopy(state)
    assert state == baseline['roadmap'] and state['events'][-1]['id'] == 'SERG-RM-0026'
    receiptname = 'RUNTIME_USER_ATTESTATION_' + DATE + '.json'
    assert not (out / receiptname).exists()
    checks = []
    def ck(name, ok):
        checks.append(dict(name=name, passed=bool(ok)))
    owned = set(lot.load(out / 'FILES_MODIFIED.json')['runtime_files'])
    ck('Original delivery manifest intact at entry', not baseline['delivery_manifest_changes'])
    ck('Concurrent changes do not touch the delivered core', not owned.intersection(baseline['concurrent_runtime_changes']))
    ck('Current runtime still matches captured entry', lot.italian.runtime_hashes() == baseline['hashes'])
    ck('World history inventory equals delivered static inventory', baseline['inventory'] == lot.load(out / 'SESSION_AFTER_STATIC.json')['inventory'])
    registry_rel = lot.reg.active_registry_path().relative_to(lot.ROOT).as_posix()
    ck('575 imperial rights retained', len(baseline['registry']) == 575
       and lot.sha(lot.reg.active_registry_path()) == lot.load(out / 'DELIVERY_MANIFEST.json')['files'][registry_rel])
    v = lot.load(out / 'VALIDATION.json')
    ck('134/134 static evidence retained', v['passed'] == v['total'] == 134 and not v['failed'])
    ck('24 acquired tasks remain qualified', sum(rm.qualifications(state).values()) == 24)
    t = next(t for t in state['tasks'] if t['id'] == lot.TASK)
    ck('Only MC-I-CORE is pending under regional P0 block', t['status'] == 'BLOCKED' and t['priority'] == 'P0'
       and t['installed_delivery_status'] == 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
       and [s['id'] for s in t['installed_sub_lots']] == ['MC-I-CORE'])
    bitmap = lot.core.packed(lot.ROOT / 'map_data/provinces.png')
    import numpy as np
    ys, xs = np.where(bitmap == int('EDBC00', 16))
    ck('Exact eight delivered cells still MCA core', sorted(map(list, zip(xs.tolist(), ys.tolist()))) == sorted(map(list, lot.CELLS)))
    assert all(c['passed'] for c in checks), checks
    checkname = 'ACCEPTANCE_CHECK_' + DATE + '.json'
    rm.write_json(out / checkname, dict(task_ids=[lot.TASK], status='PASS', total=len(checks), passed=len(checks), failed=[], checks=checks, automated_engine_test=False))
    sourcename = 'USER_VALIDATION_MISSION_' + DATE + '.txt'
    (out / sourcename).write_bytes(SOURCE.read_bytes())
    rm.write_json(out / receiptname, dict(status='PASS_RUNTIME_USER_VALIDATED', task_ids=[lot.TASK],
        sub_lot_ids=['MC-I-CORE'], scope_type='INSTALLED_SUB_LOTS_ONLY', regional_closure_approved=False,
        points_awarded=0, recorded_on='2026-10-23', source=PREFIX + sourcename,
        protocol=PREFIX + 'PLAYER_TEST_PROTOCOL.md', protocol_confirmed_as_whole=True,
        explicitly_reported=['Nouvelle partie au 1er janvier 1776', 'MCA présent et noyau de Massa correctement attribué',
            'Marie-Thérèse Cybo-Malaspina souveraine', 'Capitale et institutions fonctionnelles',
            '10000 habitants initiaux', 'Administration publique présente et fonctionnelle',
            'Droits impériaux installés fonctionnels dans leur périmètre', 'Voisins et populations conservés',
            'Un mois complet sans anomalie', 'Sauvegarde et rechargement réussis', 'Aucun problème constaté'],
        new_game_date='1776-01-01', simulation_months=1, save_and_reload=True,
        automated_engine_test=False, actual_test_date=None, language_tested=None,
        reported_anomalies=[], additional_observations_invented=False,
        validated_scope=dict(tag='MCA', rgb='xEDBC00', cells=lot.CELLS, category='B', population=10000),
        excluded=['Clôture régionale Massa-Carrare', 'Périmètre et population complète de Carrare',
            'Possessions périphériques', 'Sarzana/Lerici/Montignoso/Pietrasanta/Seravezza/Garfagnana',
            'Extension territoriale future', 'Cadastre', 'Tout nouveau sous-lot de Trente']))
    t['installed_delivery_status'] = 'PASS_RUNTIME_USER_VALIDATED'
    t['installed_sub_lots'][0].update(status='PASS_RUNTIME_USER_VALIDATED', attestation=PREFIX + receiptname)
    t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED', attestation=PREFIX + receiptname,
        scope='MC-I-CORE only: MCA, xEDBC00, eight cells, category B, 10000 people, Maria Teresa, capital, public court and corresponding imperial rights. Full protocol explicitly confirmed by the user; no complete Carrara or peripheral closure.')
    obsolete = 'Capitale automatique de la portion partagée et économie locale à contrôler en jeu avant acceptation ; aucun nouveau hub Massa ou port industriel prétendu.'
    assert obsolete in t['blocking_reason']
    t['blocking_reason'] = t['blocking_reason'].replace(obsolete,
        'Capitale et institutions du seul MC-I-CORE validées en jeu par le joueur ; aucun nouveau hub Massa ou port industriel prétendu. Cette validation ne résout pas la couverture territoriale et démographique complète de Carrare.')
    t['residual_uncertainty'] = t['blocking_reason']
    t['current_delivery_note'] = ('MC-I-CORE seul PASS_RUNTIME_USER_VALIDATED selon confirmation explicite du protocole intégral : '
        'MCA et huit cellules xEDBC00, 10000 habitants, Marie-Thérèse, capitale/institutions, administration et droits impériaux bornés, '
        'voisins et populations conservés, un mois sans anomalie, sauvegarde/rechargement réussis. '
        'Aucune date effective, capture, mesure moteur ou observation supplémentaire inventée. '
        'SC4-MASSA-CARRARA reste BLOCKED P0 pour Carrare et les périphéries ; aucun point régional.')
    acceptname = 'ACCEPTANCE_' + DATE + '.md'
    (out / acceptname).write_text('# Validation de MC-I-CORE uniquement\n\n'
        '**PASS_RUNTIME_USER_VALIDATED** : confirmation explicite du protocole intégral conservée dans USER_VALIDATION_MISSION_2026_10_23.txt. '
        'MCA, xEDBC00, huit cellules B et 10000 habitants ; souveraine, capitale/institutions, administration, droits bornés et conservations confirmés, un mois, sauvegarde/rechargement, aucune anomalie. '
        'Aucune date réelle de test, capture, mesure moteur ou vérification supplémentaire inventée.\n\n'
        '**SC4-MASSA-CARRARA reste BLOCKED P0**, sans clôture régionale ni point supplémentaire. '
        'Les possessions périphériques, l’étendue et la démographie complète de Carrare restent ouvertes ; les rapports et preuves de livraison originaux sont conservés.\n\n'
        'Progression **82/235 = 34,89 % avant/après**. Après recalcul des dépendances, **SC1-TRENTO P1** est la seule nouvelle étape autorisée. '
        'Les modifications concurrentes observées sont conservées et ne sont pas couvertes par ce reçu.\n', encoding='utf8')
    t['implementation_report'].append(PREFIX + acceptname)
    state.pop('runtime_validation_hold', None)
    state['mission_status'] = 'MASSA_CORE_USER_VALIDATED_REGION_BLOCKED_READY_FOR_TRENTO'
    state['events'].append(dict(id='SERG-RM-0027', date='2026-10-23', kind='PARTIAL_RUNTIME_USER_VALIDATION',
        scope_version=state['scope_version'], source=PREFIX + receiptname,
        changes=[dict(task_id=lot.TASK, before='BLOCKED', after='BLOCKED')],
        sub_lot_changes=[dict(id='MC-I-CORE', before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION', after='PASS_RUNTIME_USER_VALIDATED')],
        before_weight=82, after_weight=82, total_weight=235, before_percent='34.89', after_percent='34.89',
        evidence=[PREFIX + receiptname, PREFIX + checkname, PREFIX + acceptname],
        note=t['current_delivery_note'] + ' SC1-TRENTO P1 admissible après Salzbourg ; une seule nouvelle étape autorisée.'))
    assert [x for x in state['tasks'] if x['id'] != lot.TASK] == [x for x in original['tasks'] if x['id'] != lot.TASK]
    assert state['events'][:-1] == original['events']
    assert rm.partial_runtime_evidence(t) and not rm.terminal_evidence(dict(t, status='PASS_RUNTIME_USER_VALIDATED'), state)
    p = rm.progress(state)
    assert (p['earned_weight'], p['total_weight'], p['percent'], p['qualified_tasks'], p['next_task']) == (82, 235, '34.89', 24, 'SC1-TRENTO'), p
    assert not rm.structural_errors(state), rm.structural_errors(state)
    rm.write_json(rm.OUT / 'ROADMAP_STATE.json', state)
    with contextlib.redirect_stdout(io.StringIO()):
        rm.render()
    checked = rm.check()
    rm.write_json(out / ('ACCEPTANCE_TRACKER_VALIDATION_' + DATE + '.json'), checked)
    assert checked['status'] == 'PASS', checked
    print(json.dumps(dict(acceptance_checks=len(checks), tracker=checked['status'], earned=p['earned_weight'], percent=p['percent'], next=p['next_task'])), flush=True)


if __name__ == '__main__':
    import sys
    globals()[sys.argv[1]]()
