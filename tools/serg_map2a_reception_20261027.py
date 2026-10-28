"""Document-only MAP2A reception. No installer, gameplay write or Git write.

prepare runs preservation and canonical tests before creating new evidence.
receive records only the player's supplied MAP2A attestation, then renders views.
finish checks the bounded change and writes new evidence; old proofs stay intact.
"""
import ast
import contextlib
import datetime
import io
import os
from pathlib import Path
import sys
import traceback
import unittest
from unittest.mock import patch

import map2a_patch as plan
import serg_closure_roadmap as rm
import test_serg_closure_roadmap as tracker_tests
import validate_map2a as qa

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
ROOT = rm.ROOT
TASK = 'SC2-MAP2A-VALIDATION'
LOT = rm.OUT / TASK
OUT = LOT / 'ACCEPTANCE_2026_10_27'
PREFIX = OUT.relative_to(ROOT).as_posix() + '/'
RECEIPT = LOT / 'RUNTIME_USER_ATTESTATION_2026_10_27.json'
SOURCE = Path('C:/Users/simeo/.codex/attachments/9444cbe6-9472-4cd2-afa2-d95148c31311/Texte collé.txt')
CAMPAIGN = rm.OUT / 'CLOSURE_CAMPAIGN_2026_10_26'
OLD_PROTOCOL = rm.OUT / 'SC2-LUXEMBOURG-VALIDATION/ACCEPTANCE_2026_10_26/PLAYER_TEST_PROTOCOL_GROUPED.md'
ASSIGNMENTS = [('x9AC196', 'STATE_LOMBARDY', 'SWI'), ('x71E080', 'STATE_MORAVIA', 'AUS'),
               ('xF0E080', 'STATE_MORAVIA', 'AUS'), ('x9061E0', 'STATE_WEST_GALICIA', 'AUS')]
VIEWS = ['ROADMAP.md', 'NEXT_ACTION.md', 'BLOCKERS.md', 'PROGRESS_HISTORY.md',
         'CLOSURE_CHECKLIST.md', 'DEFERRED_P2.md', 'PROGRESS_SNAPSHOT.json']


def rel(p): return p.relative_to(ROOT).as_posix()
def load(p): return rm.load_json(p)
def sha(p): return rm.digest(p)
def dump(name, obj): rm.write_json(OUT / name, obj)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git_state():
    return dict(head=rm.git('rev-parse', 'HEAD'), branch=rm.git('branch', '--show-current'),
                index=sha(ROOT / rm.git('rev-parse', '--git-path', 'index')))


def targeted():
    original = load(qa.OUT / 'MAP2A_BASELINE.json')
    expected = plan.transform(original['originals'])
    inv = qa.inventory()
    campaign = load(CAMPAIGN / 'BASELINE.json')['inventory']
    checks = []
    def ck(name, ok): checks.append(dict(name=name, passed=bool(ok)))
    owners = qa.counter(inv['owners'])
    for rgb, sid, tag in ASSIGNMENTS + [('x867A90', 'STATE_LOMBARDY', 'VEN')]:
        ck('Unique owner and State Region ' + rgb, owners[rgb, sid, tag] == 1
           and sum(n for k, n in owners.items() if k[0] == rgb) == 1 and inv['geometry'][rgb] == sid)
    for path, sid, tag in [(qa.HISTORY[2], 'STATE_LOMBARDY', 'SWI'),
                           (qa.HISTORY[1], 'STATE_MORAVIA', 'AUS'),
                           (qa.HISTORY[3], 'STATE_WEST_GALICIA', 'AUS'),
                           (qa.HISTORY[3], 'STATE_UPPER_SILESIA', 'PRU'),
                           (qa.HISTORY[3], 'STATE_WEST_GALICIA', 'GAL')]:
        ck('Exact delivered population ' + sid + ' ' + tag,
           qa.signature(plan.region(expected[path], sid, tag)) ==
           qa.signature(plan.region((ROOT / path).read_text(encoding='utf-8-sig'), sid, tag)))
    for path in qa.HISTORY[5:7]:
        ck('Exact Teschen buildings PM ownership reserves ' + path,
           qa.signature(plan.region(expected[path], 'STATE_WEST_GALICIA', 'AUS')) ==
           qa.signature(plan.region((ROOT / path).read_text(encoding='utf-8-sig'), 'STATE_WEST_GALICIA', 'AUS')))
    for tag in ['AUS', 'PRU']:
        a = next(n for n in qa.cw.walk(qa.cw.parse(expected[qa.HISTORY[-1]])) if n.key == 'c:' + tag)
        z = next(n for n in qa.cw.walk(qa.cw.parse((ROOT / qa.HISTORY[-1]).read_text(encoding='utf-8-sig'))) if n.key == 'c:' + tag)
        ck('Exact delivered formations units commanders HQ ' + tag, qa.signature(a) == qa.signature(z))
    # The October 26 campaign already includes the later, separately tracked
    # Lombardy redistributions. Never restore October 10's wider population pool.
    for key, index in [('regional_pop', 0), ('buildings', 0), ('units', 2)]:
        for sid in sorted(qa.TARGETS):
            ck('Conservation since October 26 ' + key + ' ' + sid,
               [v for v in campaign[key] if v['key'][index] == sid] ==
               [v for v in inv[key] if v['key'][index] == sid])
    ck('No invalid Austrian Upper Silesia state', ['STATE_UPPER_SILESIA', 'AUS'] not in inv['states'])
    ck('No orphan or wrong-region issue in receipt scope', not [e for e in inv['errors']
       if (e[0] == 'wrong_state_region' and e[1] in [a[0] for a in ASSIGNMENTS])
       or (e[0] == 'orphan_selector' and e[2:4] in [['STATE_WEST_GALICIA', 'AUS'], ['STATE_LOMBARDY', 'SWI']])])
    ck('Canonical tracker', rm.check()['status'] == 'PASS')
    return dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL', task_ids=[TASK],
                total=len(checks), passed=sum(c['passed'] for c in checks),
                failed=[c for c in checks if not c['passed']], checks=checks,
                runtime_sha256_collected_by_agent=rm.hashes(), automated_engine_test=False), inv


def tracker_result():
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(tracker_tests.RoadmapTests)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return dict(status='PASS' if result.wasSuccessful() else 'FAIL', total=result.testsRun,
                passed=result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
                skipped=[dict(test=str(t), reason=r) for t, r in result.skipped],
                failed=[dict(test=str(t), traceback=r) for t, r in result.failures + result.errors],
                raw_output=stream.getvalue(), automated_engine_test=False)


def prepare():
    assert not OUT.exists() and not RECEIPT.exists(), 'Reception already exists; do not overwrite'
    state = load(rm.OUT / 'ROADMAP_STATE.json')
    start = dict(roadmap=state, progress=rm.progress(state), runtime_hashes=rm.hashes(), git=git_state(),
                 recorded_at=now(), tracker_source=(ROOT / 'tools/serg_closure_roadmap.py').read_text(encoding='utf-8'),
                 root_texts={n:(rm.OUT / n).read_text(encoding='utf-8') for n in VIEWS},
                 proofs={rel(p):sha(p) for p in (ROOT / 'docs').rglob('*') if p.is_file()},
                 instructions={rel(p):sha(p) for p in [ROOT / 'AGENTS.md', *(ROOT / '.agents').rglob('*.md')]})
    assert (start['progress']['earned_weight'], start['progress']['qualified_tasks']) == (83, 25)
    result, inventory = targeted()
    print('Preservation:', result['passed'], '/', result['total'], flush=True)
    legacy = dict(command='python -B -X utf8 tools/validate_map2a.py', automated_engine_test=False)
    stream = io.StringIO()
    try:
        # Ensure this old report-writing entry point can never replace an archive.
        with contextlib.redirect_stdout(stream), patch.object(Path, 'write_text', side_effect=RuntimeError('Legacy report writing disabled')):
            qa.validate()
        legacy.update(status='PASS')
    except Exception as ex:
        legacy.update(status='FAIL', exception_type=type(ex).__name__, message=str(ex), traceback=traceback.format_exc())
    legacy['raw_output'] = stream.getvalue()
    legacy['classification'] = 'OBSOLETE_GLOBAL_SNAPSHOT_OUTSIDE_MAP2A_SCOPE; full October 10 ownership equality rejects later authorized lots; original validator and old raw reports retained.'
    tests = tracker_result()
    assert result['status'] == tests['status'] == 'PASS', 'New scope regression; do not record receipt'
    assert legacy.get('message') == 'Unexpected territorial change.', 'Review unexpected legacy result'
    assert rm.hashes() == start['runtime_hashes'], 'Concurrent runtime change during preflight; reread'
    assert load(rm.OUT / 'ROADMAP_STATE.json') == state, 'Concurrent tracker change; reread'
    assert all((ROOT / n).is_file() and sha(ROOT / n) == h for n, h in start['proofs'].items()), 'Concurrent evidence change; reread'
    # All preflight checks precede these first evidence writes.
    OUT.mkdir(parents=True)
    dump('BASELINE.json', start)
    dump('ACCEPTANCE_CHECKS.json', result)
    dump('CURRENT_INVENTORY.json', inventory)
    dump('LEGACY_MAP2A_READONLY_RAW.json', legacy)
    dump('PREWRITE_TRACKER_TESTS.json', tests)
    dump('PREWRITE_CANONICAL_CHECK.json', rm.check())
    (OUT / 'USER_ATTESTATION.md').write_bytes(SOURCE.read_bytes())
    print('Preflight passed; tracker', tests['passed'], 'passed,', len(tests['skipped']), 'skipped', flush=True)


def receive():
    b = load(OUT / 'BASELINE.json')
    assert not RECEIPT.exists(), 'Never overwrite a human receipt'
    assert rm.hashes() == b['runtime_hashes'], 'Concurrent runtime change; reread before receipt'
    path = rm.OUT / 'ROADMAP_STATE.json'
    raw = path.read_bytes()
    state = load(path)
    assert state == b['roadmap'], 'Concurrent tracker update; reread'
    assert load(OUT / 'ACCEPTANCE_CHECKS.json')['status'] == 'PASS'
    source = (OUT / 'USER_ATTESTATION.md').read_text(encoding='utf-8-sig')
    observations = [line[2:].strip() for line in source.split('## 1.', 1)[1].split('## 2.', 1)[0].splitlines() if line.startswith('- ')]
    quote = "Je confirme avoir testé personnellement et réussi l'intégralité du protocole `SC2-MAP2A-VALIDATION` dans Victoria 3."
    assert quote in source and len(observations) == 11
    receipt = dict(status='PASS_RUNTIME_USER_VALIDATED', task_ids=[TASK], scope_type='TASK_PROTOCOL_ONLY',
        task_closure_approved=True, recorded_on='2026-10-27', actual_test_date=None,
        source=PREFIX + 'USER_ATTESTATION.md', source_sha256=sha(OUT / 'USER_ATTESTATION.md'),
        source_kind='Explicit current user attachment: SERG TERRITORIAL 1.0 — RÉCEPTION HUMAINE DE MAP2A',
        source_quote=quote, explicitly_reported=observations,
        protocol=rel(OLD_PROTOCOL), protocol_row=TASK,
        historical_reports=['docs/reports/map/MAP2A/MAP2A_EXECUTIVE_SUMMARY.md', 'docs/reports/map/MAP2A/MAP2A_DEPENDENCIES.md'],
        new_game_date='1776-01-01', new_game_date_meaning='Scenario start, not actual calendar test date',
        simulation_months=1, save_reload=True, personally_performed_by='user', automated_engine_test=False,
        extra_observations_invented=False,
        scope=dict(assignments=[dict(rgb=a, state=s, owner=t) for a,s,t in ASSIGNMENTS], bergamo='x867A90 remains VEN',
                   populations='Original SWI 5000, Moravian allocation and Teschen 135753 preserved; later Lombardy redistributions separately documented',
                   teschen_buildings='Two textile levels plus one traditional-road infrastructure level; base/overlay declarations are not added together',
                   military='AUS recruitment, existing AUS/PRU formations units commanders and HQ retained'),
        excluded_task_ids=[t['id'] for t in state['tasks'] if t['id'] != TASK],
        excluded_sub_lots=['TE-R-CORE', 'BG-E-SALT-NATIVE-R1'],
        limitations=['No full cadastral certification of Silesia', 'No regional Teschen closure',
                     'No imperial registry validation implied', 'No validation of later Milan correction'],
        screenshots_provided=[], employment_statistics_provided=None, economic_measurements_provided=None,
        tested_file_hashes_supplied_by_user=None, acceptance_checks=PREFIX + 'ACCEPTANCE_CHECKS.json',
        current_file_hashes_collected_by_agent={p:b['runtime_hashes'][p] for p in qa.HISTORY})
    rm.write_json(RECEIPT, receipt)
    old_protocol = OLD_PROTOCOL.read_text(encoding='utf-8')
    protocol = old_protocol.replace('# SERG — sept validations complètes encore nécessaires', '# SERG — six validations complètes encore nécessaires')
    protocol = protocol.replace('Liste actualisée après réception humaine du Luxembourg. Le protocole Luxembourg est terminé : il n’est pas à refaire. Les protocoles antérieurs restent archivés.',
        'Liste actualisée après réception humaine du Luxembourg et de MAP2A. Leurs protocoles sont terminés et ne sont pas à refaire. Les protocoles antérieurs restent archivés.')
    protocol = protocol.replace('**Sept tâches installées, dix points conditionnels.**', '**Six tâches installées, huit points conditionnels.**')
    protocol = '\n'.join(line for line in protocol.splitlines() if not line.startswith('| SC2-MAP2A-VALIDATION')) + '\n'
    protocol = protocol.replace('**Prochaine validation recommandée : SC2-MAP2A-VALIDATION**', '**Prochaine validation recommandée : SC4-MILAN-VALIDATION**')
    protocol = protocol.replace('Aucun de ces contrôles n’est acquis grâce au reçu Luxembourg.', 'Aucun de ces contrôles du registre impérial n’est acquis grâce aux reçus Luxembourg ou MAP2A. Le mois et la sauvegarde/rechargement attestés pour MAP2A ne couvrent pas automatiquement TE-R-CORE.')
    (OUT / 'PLAYER_TEST_PROTOCOL_GROUPED.md').write_text(protocol, encoding='utf-8')
    task = next(t for t in state['tasks'] if t['id'] == TASK)
    before = task['status']
    task.update(status=receipt['status'], static_tests=dict(status='PASS', evidence=[PREFIX + 'ACCEPTANCE_CHECKS.json']))
    task['runtime_validation'].update(status=receipt['status'], attestation=rel(RECEIPT),
        scope='Four original MAP2A corrections and associated preserved populations/buildings/PM/military only; excludes TE-R-CORE and every other task',
        new_details_invented=False, protocol=rel(OLD_PROTOCOL))
    task['closure_audit'].update(status='TASK_CLOSED_USER_VALIDATED', remaining_controls=[], new_points=task['weight'],
                                 reception_report=PREFIX+'REPORT.md')
    task['current_delivery_note'] = 'Protocole MAP2A intégral explicitement réussi : quatre corrections et Bergame, populations, bâtiments/PM et recrutement conservés, nouvelle partie 1776, un mois, sauvegarde/rechargement. Reçu limité à SC2-MAP2A-VALIDATION ; Teschen/TE-R-CORE et les six autres validations restent distincts.'
    task['residual_uncertainty'] = 'Approximation politique conservée ; aucune précision cadastrale générale ni clôture de SC2-TESCHEN ou de SC4-MILAN-VALIDATION par ce reçu.'
    state['mission_status'] = 'MAP2A_USER_VALIDATED_SIX_GROUPED_TESTS_PENDING'
    hold = state['runtime_validation_hold']
    pending = [t['id'] for t in state['tasks'] if t['status'] == 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION']
    hold.update(task_id=pending[0], pending_task_ids=pending, protocol=PREFIX+'PLAYER_TEST_PROTOCOL_GROUPED.md',
        reason='Luxembourg et MAP2A reçus ; validations déjà installées uniquement, aucune nouvelle installation.',
        test_summary='Contrôler le raccord Milanais–Crémonais AUS et les voisins VEN/SWI en nouvelle partie 1776 puis un mois ; cinq autres validations possibles dans la même session.',
        scope_note='Seule MAP2A reçoit un nouveau statut. TE-R-CORE et la mine de sel restent séparés ; aucun nouveau territoire.')
    campaign = state['closure_campaign']
    campaign.update(pass_status='MAP2A_HUMAN_ACCEPTED', grouped_protocol=hold['protocol'],
        next_closure_candidate=pending[0], current_resolution_task=TASK,
        remaining_grouped_runtime_points=sum(t['weight'] for t in state['tasks'] if t['id'] in pending))
    campaign['map2a_reception'] = dict(date='2026-10-27', task_id=TASK, status=receipt['status'],
        attestation=rel(RECEIPT), report=PREFIX+'REPORT.md', checks=PREFIX+'ACCEPTANCE_CHECKS.json',
        final_checks=PREFIX+'FINAL_CHECKS.json')
    # The receipt is new, so compute the credited amount through the real gate.
    p = rm.progress(state)
    assert (p['earned_weight'], p['total_weight'], p['qualified_tasks'], p['total_tasks']) == (85,235,26,81)
    state['events'].append(dict(id='SERG-RM-0055', date='2026-10-27', kind='MAP2A_EXPLICIT_FULL_USER_VALIDATION',
        scope_version=state['scope_version'], source=rel(RECEIPT),
        changes=[dict(task_id=TASK, before=before, after=receipt['status'])],
        before_weight=b['progress']['earned_weight'], after_weight=p['earned_weight'], total_weight=p['total_weight'],
        before_percent=b['progress']['percent'], after_percent=p['percent'],
        note=task['current_delivery_note']))
    assert path.read_bytes() == raw, 'Concurrent tracker edit before write'
    rm.write_json(path, state)
    report = f'''# Réception humaine de MAP2A — 27 octobre 2026

`{TASK}` : `PASS_RUNTIME_USER_VALIDATED`, après attestation explicite intégrale du joueur.
Portée : x9AC196 SWI/Lombardie, x71E080 et xF0E080 AUS/Moravie, x9061E0 AUS/Galicie occidentale ; Bergame VEN ; populations, bâtiments, PM et recrutement associés. Deux niveaux textiles et un niveau de réseau routier à Teschen, sans addition artificielle des déclarations base/overlay. Formations, commandants et HQ AUS/PRU conservés.

Le joueur atteste nouvelle partie 1776, mois complet sans anomalie et sauvegarde/rechargement. Date effective du test, captures, statistiques économiques et mesures d’emploi non fournies ; aucune n’est inventée. Empreintes collectées par l’agent au moment de la réception, distinctes d’empreintes testées fournies par le joueur.

Conservation ciblée : voir [ACCEPTANCE_CHECKS.json](ACCEPTANCE_CHECKS.json). Ancien validateur global : échec `Unexpected territorial change.` conservé intégralement dans [LEGACY_MAP2A_READONLY_RAW.json](LEGACY_MAP2A_READONLY_RAW.json). Il exige encore toute la carte du 10 octobre, antérieure aux autres lots autorisés. Les quatre corrections sont présentes. Les pools lombards plus larges ont changé dans les redistributions ultérieures ; populations, bâtiments et unités des quatre régions identiques à l’audit du 26 octobre. Les transferts MAP2A SWI (5000), Moravie et Teschen (135753) restent exacts. Références : MAP2A_DEPENDENCIES.md ; MAP2L/MILAN_CREMONESE/REPORT.md et PLAN.json. Aucun ancien test, résultat brut ou baseline réécrit.

Progression calculée : {b['progress']['earned_weight']}/235 ({b['progress']['percent']} %, 25/81) → {p['earned_weight']}/235 ({p['percent']} %, 26/81). Deux points pour cette seule tâche. Les 23 tâches bloquées restent inchangées. SC2-TESCHEN et TE-R-CORE, limites cadastrales silésiennes, mine de Berchtesgaden, Milan et autres tâches ne sont pas validés par ce reçu. Le reçu Luxembourg est conservé.

Aucun fichier fonctionnel, vanilla ou Git écrit. Aucune installation ni nouveau test moteur par l’agent. Les résultats finaux et écarts concurrents sont consignés dans FINAL_CHECKS.json et CONCURRENT_CHANGES.json.

Suite recommandée : SC4-MILAN-VALIDATION, puis les cinq autres lignes du [protocole groupé actualisé](PLAYER_TEST_PROTOCOL_GROUPED.md), soit huit points conditionnels. Sous-lots TE-R-CORE et mine ordinaire maintenus séparément. Aucun nouveau territoire commencé.
'''
    (OUT / 'REPORT.md').write_text(report, encoding='utf-8')
    assert not rm.structural_errors(state), rm.structural_errors(state)
    rm.render()


def finish():
    b = load(OUT / 'BASELINE.json')
    state = load(rm.OUT / 'ROADMAP_STATE.json')
    p = rm.progress(state)
    result, _ = targeted()
    dump('FINAL_PRESERVATION_CHECKS.json', result)
    tests = tracker_result()
    dump('TRACKER_TESTS.json', tests)
    dump('CANONICAL_CHECK.json', rm.check())
    runtime = rm.hashes()
    changes = [dict(path=f, before=b['runtime_hashes'].get(f), after=runtime.get(f))
               for f in sorted(set(runtime) | set(b['runtime_hashes'])) if runtime.get(f) != b['runtime_hashes'].get(f)]
    dump('CONCURRENT_CHANGES.json', dict(functional_files_written_by_this_mission=[], external_runtime_changes=changes,
        changes_since_map2a_delivery='Global old snapshot differs; targeted four-region inventory equals October 26 campaign; see preserved raw legacy failure',
        automated_engine_test=False))
    old_functions = {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b['tracker_source']).body if isinstance(n,ast.FunctionDef)}
    new_functions = {n.name:ast.dump(n,include_attributes=False) for n in ast.parse((ROOT/'tools/serg_closure_roadmap.py').read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef)}
    functions_changed = [n for n in set(old_functions)|set(new_functions) if old_functions.get(n)!=new_functions.get(n)]
    allowed = {rel(rm.OUT/n) for n in VIEWS} | {rel(rm.OUT/'ROADMAP_STATE.json')}
    old_changed = [f for f,h in b['proofs'].items() if f not in allowed and (not (ROOT/f).is_file() or sha(ROOT/f)!=h)]
    old_tasks = {t['id']:t for t in b['roadmap']['tasks']}
    receipt = load(RECEIPT)
    checks = dict(targeted_preservation=result['status']=='PASS', tracker_tests=tests['status']=='PASS',
        canonical=rm.check()['status']=='PASS', calculated_progress=(p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['total_tasks'],p['percent'])==(85,235,26,81,'36.17'),
        only_MAP2A_task_changed=all(t==old_tasks[t['id']] for t in state['tasks'] if t['id']!=TASK),
        unchanged_81_tasks_and_weights=[(t['id'],t['weight']) for t in state['tasks']]==[(t['id'],t['weight']) for t in b['roadmap']['tasks']],
        existing_history_additive=state['events'][:len(b['roadmap']['events'])]==b['roadmap']['events'],
        all_prior_proofs_preserved=not old_changed, runtime_unchanged=not changes,
        instructions_unchanged=all(sha(ROOT/f)==h for f,h in b['instructions'].items()),
        git_HEAD_branch_index_unchanged=git_state()==b['git'], only_renderer_changed=set(functions_changed)<={'render'},
        receipt_only_MAP2A=receipt['task_ids']==[TASK] and 'SC2-TESCHEN' in receipt['excluded_task_ids'] and 'TE-R-CORE' in receipt['excluded_sub_lots'],
        no_invented_test_details=receipt['actual_test_date'] is None and receipt['screenshots_provided']==[] and receipt['tested_file_hashes_supplied_by_user'] is None,
        six_pending_eight_points=len(p['awaiting_runtime'])==6 and sum(old_tasks[t]['weight'] for t in p['awaiting_runtime'])==8,
        all_23_blocked_unchanged=p['blocked']==b['progress']['blocked'] and len(p['blocked'])==23,
        next_Milan=state['runtime_validation_hold']['task_id']==p['next_task']=='SC4-MILAN-VALIDATION',
        no_Holstein_started=next(t for t in state['tasks'] if t['id']=='SC3-HOLSTEIN')==old_tasks['SC3-HOLSTEIN'])
    final = dict(status='PASS' if all(checks.values()) else 'FAIL', task_ids=[TASK], recorded_at=now(),
        total=len(checks), passed=sum(checks.values()), failed=[k for k,v in checks.items() if not v], checks=checks,
        progress_before=b['progress'], progress_after=p, changed_old_proofs=old_changed,
        tracker_functions_changed=functions_changed, functional_files_written=[], git_write_operations=[], vanilla_files_written=[],
        automated_engine_test=False)
    dump('FINAL_CHECKS.json', final)
    assert final['status']=='PASS', final['failed']
    path = rm.OUT/'ROADMAP_STATE.json'; raw = path.read_bytes()
    assert load(path) == state, 'Concurrent tracker edit during final checks; reread before history write'
    if not any(e['id']=='SERG-RM-0056' for e in state['events']):
        state['events'].append(dict(id='SERG-RM-0056',date='2026-10-27',kind='MAP2A_RECEPTION_FINAL_CHECKS',scope_version='1.0.0',
            source=PREFIX+'FINAL_CHECKS.json',changes=[],before_weight=p['earned_weight'],after_weight=p['earned_weight'],
            total_weight=p['total_weight'],before_percent=p['percent'],after_percent=p['percent'],
            note=f"Réception MAP2A seule ; conservation {result['passed']}/{result['total']}, suivi {tests['passed']} réussis et {len(tests['skipped'])} test historique désactivé. Échec global MAP2A ancien archivé et classé hors périmètre. Six validations installées restent ouvertes (8 points) ; Teschen/TE-R-CORE et mine de sel séparés. Aucun fichier fonctionnel ni ancien reçu modifié."))
        assert path.read_bytes()==raw
        rm.write_json(path,state)
        rm.render()
    dump('POST_HISTORY_CANONICAL_CHECK.json',rm.check())
    dump('DELIVERY_MANIFEST.json',dict(recorded_at=now(),artifacts_sha256={rel(f):sha(f) for f in OUT.rglob('*') if f.is_file() and f.name!='DELIVERY_MANIFEST.json'},
        receipt_sha256=sha(RECEIPT),tracking_sha256={rel(rm.OUT/n):sha(rm.OUT/n) for n in VIEWS+['ROADMAP_STATE.json']},
        tools_sha256={rel(f):sha(f) for f in [Path(__file__),ROOT/'tools/serg_closure_roadmap.py']},
        functional_files_written=[],automated_engine_test=False))
    print('Final:',final['status'],final['passed'],'/',final['total'],p['percent'],flush=True)


if __name__ == '__main__':
    {'prepare':prepare,'receive':receive,'finish':finish}[sys.argv[1]]()
