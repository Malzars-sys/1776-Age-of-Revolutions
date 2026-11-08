"""Glatz/Silesia: read-only conservation checks and scoped documentary tracking.

No gameplay installer, vanilla write, Git mutation or human receipt generation.
"""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
import unittest

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import serg_closure_roadmap as rm
import serg_prussian_west as prior
from map2l_belgium import packed

ROOT = prior.ROOT
CANON = prior.CANON
OUT = CANON / 'GLATZ_SILESIA_2026_11_05'
TARGET = 'SC3-SILESIA-LUSATIA'
REF = OUT.relative_to(ROOT).as_posix()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def evidence():
    """Explain the existing native geometry without fitting a new projection."""
    b = load('BASELINE.json')
    a = packed(OUT / 'provinces_before.png')
    v = packed(Path('C:/Games/Victoria 3/game/map_data/provinces.png'))
    owners = {r['key'][0]: r['key'][1:] for r in b['inventory']['owners']}
    box = (4445, 815, 4545, 882)
    south = np.zeros(a.shape, dtype=bool)
    south[box[1]:box[3], box[0]:box[2]] = True
    correspondence = load('VANILLA_CORRESPONDENCE.json')
    southern = [r for r in correspondence['rows'] if r['current'][0] in
                {'STATE_BOHEMIA', 'STATE_MORAVIA', 'STATE_UPPER_SILESIA'}]
    saxon = np.isin(a, [int(rgb[1:], 16) for rgb, st in owners.items() if st == ['STATE_LOWER_SILESIA', 'SAX']])
    model_rows = load('TOWN_DIAGNOSTICS.json')['rows']
    # The initial exhaustive name lookup intentionally remains available.
    # Disambiguate homonyms by the bounded Silesian geographic window.
    towns = [r for r in model_rows if 49.4 <= r['geo'][1] <= 51.5]
    dump('SOURCE_TOWN_SELECTION.json', dict(rows=towns, excluded_homonyms=[r for r in model_rows if r not in towns],
        modern_coordinates_only=True, native_positions_certified=False,
        purpose='Sensitivity diagnostic only; projected Krnov/Hlucin points do not establish native ownership errors.'))
    summary = dict(
        scope='Glatz salient and Prussian/Austrian Silesian macro frontier only',
        status='RETAIN_EXISTING_B_PROPOSED_NOT_HUMAN_APPROVED', functional_files_changed=0,
        glatz_support_rgb='xC00121', glatz_support_cells=int((a == 0xC00121).sum()),
        glatz_support_is_entire_historical_county=False,
        glatz_support_owner=owners['xC00121'],
        glatz_support_geometry_equals_vanilla=bool(np.array_equal(a == 0xC00121, v == 0xC00121)),
        southern_window=list(box), southern_window_rgb_differences_from_vanilla=int(((a != v) & south).sum()),
        southern_window_previously_installed_lusatian_changes=int(((a != v) & south & saxon).sum()),
        southern_window_other_rgb_differences=int(((a != v) & south & ~saxon).sum()),
        bohemia_moravia_upper_silesia_rgb_geometries_equal_vanilla=all(r['same_rgb_geometry_as_vanilla'] for r in southern),
        upper_silesia_owners=sorted({tag for sid, tag in owners.values() if sid == 'STATE_UPPER_SILESIA'}),
        moravia_owners=sorted({tag for sid, tag in owners.values() if sid == 'STATE_MORAVIA'}),
        preserved_saxon_lower_silesia_cells=sum(int((a == int(rgb[1:], 16)).sum()) for rgb, st in owners.items() if st == ['STATE_LOWER_SILESIA', 'SAX']),
        protected_austrian_rgb_cells={rgb: int((a == int(rgb[1:], 16)).sum()) for rgb in ['x71E080', 'xF0E080', 'x9061E0']},
        interpretation='Existing native macro partition retained as political B; vanilla is a technical comparison, not a historical source. No cadastral claim or certification of every town. No 1815 Lusatian restoration.',
        source_maps=['SILESIA_LOTTER_OVERVIEW.jpg', 'GLATZ_SCULTETUS_1695.jpg'],
        rejected_inference='R5/Miller projected town ownership is not evidence that an Austrian core must be transferred. The local river diagnostic shows projection displacement.',
        new_fit=False, new_economic_region=False, shared_prussian_austrian_silesia_created=False,
        player_validation=False, new_human_receipt=False)
    dump('BOUNDARY_ASSESSMENT.json', summary)
    local = a[box[1]:box[3], box[0]:box[2]]
    colors = {'PRU': (110, 161, 210), 'AUS': (238, 201, 149), 'SAX': (159, 195, 128), 'PLC': (221, 143, 154), 'GAL': (224, 156, 192)}
    rgb = np.full((*local.shape, 3), 210, dtype=np.uint8)
    for val in np.unique(local):
        rgb[local == val] = colors.get(owners.get('x' + format(int(val), '06X'), ['', ''])[1], (190, 190, 190))
    scale = 12
    image = Image.new('RGB', (1200, 900), 'white')
    image.paste(Image.fromarray(rgb).resize((1200, local.shape[0] * scale), Image.Resampling.NEAREST), (0, 48))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
    draw.text((14, 10), 'Glatz / Silesie : trace actuel conserve ; approximation politique B', font=font, fill='black')
    for text, xy in [('SAX - Lusaces corrigees anterieurement', (8, 75)), ('SILESIE PRUSSIENNE', (430, 240)),
                     ('saillant de Glatz', (210, 600)), ('NOYAUX AUTRICHIENS', (490, 710)), ('PLC', (1080, 240))]:
        draw.text(xy, text, font=font, fill='black', stroke_width=1, stroke_fill='white')
    draw.line([(390, 615), (390, 568), (378, 532)], fill='black', width=2)
    draw.text((14, 860), 'Aucun transfert nouveau. Labels regionaux indicatifs ; aucune position urbaine certifiee.', font=font, fill='black')
    image.save(OUT / 'GLATZ_SILESIA_RETAINED.png')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def validate():
    import validate_map2a as qa
    from map2l_registry import active_registry_path
    b = load('BASELINE.json')
    current = prior.runtime()
    changed = {p: dict(before=b['runtime'].get(p), after=current.get(p)) for p in set(b['runtime']) | set(current) if b['runtime'].get(p) != current.get(p)}
    checks = []
    def ck(name, ok):
        checks.append(dict(name=name, status='PASS' if ok else 'FAIL'))
    ck('all_2859_runtime_files_preserved', not changed)
    inv = qa.inventory()
    ck('complete_inventory_identical', inv == b['inventory'])
    for key in ['owners', 'states', 'state_types', 'geometry', 'pops', 'resolved_demographics', 'regional_pop', 'buildings', 'units', 'countries']:
        ck(key + '_unchanged', inv[key] == b['inventory'][key])
    ck('no_new_inherited_reference_errors', inv['errors'] == b['inventory']['errors'])
    ck('no_new_duplicate_membership_or_owner_declarations', inv['duplicates'] == b['inventory']['duplicates'] and [r for r in inv['owners'] if r['count'] > 1] == [r for r in b['inventory']['owners'] if r['count'] > 1])
    protected = dict(b['protected'])
    for path in OUT.glob('PROTECT_*.json'):
        protected.update(json.loads(path.read_text()))
    missing = {p: h for p, h in protected.items() if not (ROOT / p).is_file() or sha(ROOT / p) != h}
    ck('all_prior_lots_and_austrian_approvals_preserved', not missing)
    registry = active_registry_path()
    installed = json.loads((CANON / 'PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05/INSTALLATION.json').read_text())
    row = next(r for r in installed['changes'] if r['file'] == registry.relative_to(ROOT).as_posix())
    ck('active_registry_matches_latest_preserved_installation_manifest', sha(registry) == row['after'])
    registry_tool = next(r for r in installed['changes'] if r['file'] == 'tools/map2l_registry.py')
    ck('registry_compiler_matches_latest_preserved_installation_manifest', sha(ROOT / registry_tool['file']) == registry_tool['after'])
    a = load('BOUNDARY_ASSESSMENT.json')
    ck('glatz_existing_prussian_support_288_cells', a['glatz_support_cells'] == 288 and a['glatz_support_owner'] == ['STATE_LOWER_SILESIA', 'PRU'])
    ck('native_southern_frontier_equals_vanilla_without_reversion', a['southern_window_other_rgb_differences'] == 0 and a['bohemia_moravia_upper_silesia_rgb_geometries_equal_vanilla'])
    ck('economic_regions_remain_separated', a['upper_silesia_owners'] == ['PRU'] and a['moravia_owners'] == ['AUS'])
    ck('all_418_saxon_lusatian_cells_preserved', a['preserved_saxon_lower_silesia_cells'] == 418)
    ck('approved_austrian_nuclei_preserved', a['protected_austrian_rgb_cells'] == {'x71E080': 92, 'xF0E080': 219, 'x9061E0': 179})
    git = {}
    for name, args in [('head', ['rev-parse', 'HEAD']), ('branch', ['branch', '--show-current'])]:
        git[name] = subprocess.run(['git', '--no-optional-locks', *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        ck('git_' + name + '_preserved', git[name] == b['git'][name])
    ck('git_index_preserved', sha(Path(b['git']['git_dir']) / 'index') == b['git']['index_sha256'])
    ck('no_new_installation_or_human_receipt', not (OUT / 'INSTALLATION.json').exists() and not list(OUT.glob('*ATTESTATION*')) and not list(OUT.glob('*RECEIPT*')))
    dump('CONCURRENT_CHANGES.json', dict(runtime_changed=changed, protected_artifacts_changed=missing, attribution='No functional writes in this pass; no functional concurrent drift since capture. Git worktree dirt predates this pass and is not restored.'))
    dump('VALIDATION.json', dict(status='PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL', checks=checks,
        passed=sum(c['status'] == 'PASS' for c in checks), total=len(checks), runtime_files=len(current), protected_artifacts=len(protected),
        inherited_reference_errors=inv['errors'], inherited_duplicates=inv['duplicates'], new_functional_changes=0, automated_engine_test=False))
    print('Conservation:', len(checks), 'checks;', [c for c in checks if c['status'] != 'PASS'])
    assert all(c['status'] == 'PASS' for c in checks)


def track():
    assert load('VALIDATION.json')['status'] == 'PASS'
    before = load('BEFORE_ROADMAP_STATE.json')
    state = rm.load_json(CANON / 'ROADMAP_STATE.json')
    assert state == before, 'Concurrent tracking changes: reconcile, never overwrite'
    state = copy.deepcopy(state)
    task = next(t for t in state['tasks'] if t['id'] == TARGET)
    assert task['status'] == 'BLOCKED' and not task['depends_on'] and task['priority'] == 'P1'
    task['status'] = 'IN_PROGRESS'
    task['implementation_report'].append(REF + '/REPORT.md')
    task['historical_sources'].append(REF + '/SOURCES.md')
    task['static_tests']['evidence'].append(REF + '/VALIDATION.json')
    task.pop('blocking_reason', None)
    task['boundary_review'] = dict(scope='Glatz et frontière prusso-autrichienne silésienne, hors nouvelle intervention sur les Lusaces',
        status='RETAIN_EXISTING_B_PROPOSED', decision=REF + '/PROPOSED_DECISION.json', new_functional_changes=0, human_approved=False)
    task['current_delivery_note'] = 'Glatz déjà PRU ; frontière méridionale native inchangée depuis le vanilla, rapprochée des sources. Maintien politique B proposé sans correction artificielle. Les 418 cellules lusaciennes antérieures restent installées et non reçues.'
    task['residual_uncertainty'] = 'Pas de précision cadastrale ni de certification urbaine : R5/Miller décalent les repères locaux. Maintien B proposé à recevoir ; test moteur du noyau lusacien différé à la fin de la Prusse. Démographie régionale non recertifiée, aucune clôture territoriale.'
    task['runtime_validation'].update(protocol=REF + '/PLAYER_TEST_PROTOCOL_GROUPED.md', deferred_until_prussia_finished_by_user=True)
    task['next_bounded_action'] = 'Décision sur le maintien B de Glatz/Silésie ; réception groupée des installations prussiennes lorsque le joueur termine la passe. Aucun nouveau territoire automatiquement.'
    state['mission_status'] = 'GLATZ_SILESIA_REVIEW_COMPLETE_B_RETENTION_PROPOSED_ENGINE_TESTS_DEFERRED'
    state['release_focus'].update(current_pass='GLATZ_SILESIA', current_pass_status='REVIEW_COMPLETE_NO_FUNCTIONAL_CHANGE_B_RETENTION_PROPOSED',
        current_delivery=REF + '/REPORT.md', continuation_authority='Utilisateur : Très bien, passons qu’à Glatz et la Silésien.',
        next_implementation_candidate=None, next_requested_pass=None, next_pass_started=False,
        next_action='Décision de maintien B et réception finale prussienne groupée ; aucune autre frontière lancée.')
    state['runtime_validation_hold'].update(protocol=REF + '/PLAYER_TEST_PROTOCOL_GROUPED.md', next_implementation_candidate=None,
        scope_note='Installations prussiennes antérieures inchangées ; ajout de témoins visuels Glatz/Silésie sans nouvelle installation. Tests toujours différés par le joueur jusqu’à la fin de la Prusse ; maintien B proposé, non approuvé.')
    p, q = rm.progress(before), rm.progress(state)
    assert (p['earned_weight'], p['total_weight'], p['qualified_tasks'], p['percent']) == (q['earned_weight'], q['total_weight'], q['qualified_tasks'], q['percent']) == (93, 235, 32, '39.57')
    assert state['events'][-1]['id'] == 'SERG-RM-0066'
    state['events'].append(dict(id='SERG-RM-0067', date='2026-11-05', kind='GLATZ_SILESIA_SCOPED_REVIEW_AND_B_RETENTION_PROPOSAL', scope_version='1.0.0', source=REF + '/REPORT.md',
        changes=[dict(task_id=TARGET, before='BLOCKED', after='IN_PROGRESS')], before_weight=93, after_weight=93, total_weight=235, before_percent='39.57', after_percent='39.57',
        note='Glatz déjà prussien ; tracé méridional native/vanilla identique. Maintien politique B proposé, pas de nouveau recalage, transfert, État économique partagé ou reçu. Noyaux autrichiens et 418 cellules saxonnes préservés. Clôture régionale et test joueur encore ouverts ; aucun point. Tests moteur toujours différés jusqu’à la fin de la Prusse.',
        evidence=[REF + '/' + n for n in ['SOURCES.md', 'BOUNDARY_ASSESSMENT.json', 'VANILLA_CORRESPONDENCE.json', 'VALIDATION.json', 'PROPOSED_DECISION.json', 'PLAYER_TEST_PROTOCOL_GROUPED.md']]))
    # Preflight all shared files immediately before the bounded documentary write.
    names = ['ROADMAP_STATE.json', 'ROADMAP.md', 'NEXT_ACTION.md', 'BLOCKERS.md', 'PROGRESS_HISTORY.md', 'PROGRESS_SNAPSHOT.json']
    for name in names:
        assert (CANON / name).read_bytes() == (OUT / ('BEFORE_' + name)).read_bytes(), 'Concurrent change: ' + name
    assert prior.runtime() == load('BASELINE.json')['runtime'], 'Reassess functional drift before tracking'
    intro = '''## Glatz / Silésie — 5 novembre 2026, examen ciblé terminé sans changement fonctionnel

Glatz est déjà prussien. Le saillant et la frontière méridionale silésienne ont conservé leur géométrie native vanilla ; les corrections lusaciennes antérieures restent installées. **Maintien politique B proposé**, fondé sur les sources et la continuité de la partition de 1742/1763, sans certification cadastrale ni urbaine. Aucun transfert nouveau ni État économique PRU/AUS partagé. [Rapport](GLATZ_SILESIA_2026_11_05/REPORT.md), [vue conservée](GLATZ_SILESIA_2026_11_05/GLATZ_SILESIA_RETAINED.png), [proposition à recevoir](GLATZ_SILESIA_2026_11_05/PROPOSED_DECISION.json).

`SC3-SILESIA-LUSATIA` : **IN_PROGRESS**, décision de maintien et réception du noyau lusacien encore ouvertes. Aucun blocage technique nouveau ni reprise d'un ancien recalage. Aucun nouveau reçu humain ou point : **93/235 = 39,57 %, 32/81**. La décision antérieure sur la Silésie autrichienne reste inchangée et ne reçoit aucune extension.

**Tests moteur toujours différés à la fin de la Prusse**, selon le joueur : [protocole groupé actualisé](GLATZ_SILESIA_2026_11_05/PLAYER_TEST_PROTOCOL_GROUPED.md). Les sous-lots prussiens déjà installés restent prêts à leur test, sans validation humaine. Prochaine action préparée : décision sur ce maintien B et réception prussienne groupée lorsque le joueur termine sa passe. Les réserves occidentales et polonaises déjà documentées demeurent ; aucune nouvelle frontière, Bavière ou micro-État commencé. Les encadrés datés antérieurs sont des archives de priorité.

'''
    updates = {}
    for name in ['ROADMAP.md', 'NEXT_ACTION.md', 'BLOCKERS.md']:
        data = (OUT / ('BEFORE_' + name)).read_bytes()
        head, body = data.split(b'\n', 1)
        text = body.decode('utf-8')
        if name == 'NEXT_ACTION.md':
            head = '# Prochaine action — maintien B Glatz/Silésie et réception prussienne groupée différée'.encode('utf-8')
        if name == 'ROADMAP.md':
            start = text.index('#### ' + TARGET)
            stop = text.find('\n#### ', start + 5)
            if stop < 0:
                stop = len(text)
            section = text[start:stop]
            assert section.count('`BLOCKED`') == 1
            text = text[:start] + section.replace('`BLOCKED`', '`IN_PROGRESS`') + text[stop:]
        if name == 'BLOCKERS.md':
            # Only the live task listing changes; dated historical notes stay archived.
            old_line = '- SC3-SILESIA-LUSATIA : '
            lines = text.splitlines(keepends=True)
            for idx, line in enumerate(lines):
                if line.startswith(old_line):
                    lines[idx] = '- SC3-SILESIA-LUSATIA : IN_PROGRESS ; maintien B de Glatz/Silésie proposé sans changement fonctionnel, réception du noyau lusacien différée à la fin de la Prusse. Voir GLATZ_SILESIA_2026_11_05.\n'
            text = ''.join(lines)
        updates[name] = head + b'\n\n' + intro.encode('utf-8') + text.encode('utf-8')
    addition = '''

## SERG-RM-0067 — 5 novembre 2026 — Glatz et frontière silésienne, maintien B proposé

Mission limitée à Glatz/Silésie. SC3-SILESIA-LUSATIA BLOCKED→IN_PROGRESS : examen borné terminé, sans nouveau changement fonctionnel ni maintien définitif approuvé. Glatz déjà PRU ; support xC00121 de 288 cellules, qui n'est pas le périmètre cadastral du comté. Tracé méridional identique au vanilla, confronté aux cartes historiques et à la partition de 1742/1763 ; positions urbaines projetées non certifiées. Aucun ancien recalage recommencé. Noyaux autrichiens, séparation économique PRU/AUS et 418 cellules lusaciennes saxonnes préservés. Décision B et réception du noyau lusacien demeurent ouvertes, tests moteur toujours différés par le joueur à la fin de la Prusse. Aucun reçu ou point : 93/235 = 39,57 %, 32/81. Aucune autre frontière ou Bavière commencée. [Rapport](GLATZ_SILESIA_2026_11_05/REPORT.md).
'''
    updates['PROGRESS_HISTORY.md'] = (OUT / 'BEFORE_PROGRESS_HISTORY.md').read_bytes() + addition.encode('utf-8')
    for name, data in updates.items():
        assert (CANON / name).read_bytes() == (OUT / ('BEFORE_' + name)).read_bytes()
        (CANON / name).write_bytes(data)
    assert rm.load_json(CANON / 'ROADMAP_STATE.json') == before
    rm.write_json(CANON / 'ROADMAP_STATE.json', state)
    rm.write_json(CANON / 'PROGRESS_SNAPSHOT.json', rm.progress(state))
    print('SERG-RM-0067:', TARGET, 'IN_PROGRESS; 93/235, 39.57%; no installation or receipt')


def tests():
    modules = ['test_serg_closure_roadmap', 'test_map2l_registry', 'test_map2l_runtime_receipt', 'test_map_georeference', 'test_serg_versioned_receipts']
    suite = unittest.TestLoader().loadTestsFromNames(modules)
    with (OUT / 'TEST_RESULTS_RAW.txt').open('w', encoding='utf-8') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    dump('TEST_RESULTS.json', dict(status='PASS' if result.wasSuccessful() else 'FAIL', command='python -B -X utf8 tools/serg_glatz_silesia.py tests', modules=modules,
        tests_run=result.testsRun, passed=result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        skipped=[dict(test=str(t), reason=reason) for t, reason in result.skipped], failures=[dict(test=str(t), traceback=msg) for t, msg in result.failures],
        errors=[dict(test=str(t), traceback=msg) for t, msg in result.errors], engine_test=False, prior_results_reused=False))
    print('Targeted tests:', result.testsRun, 'run;', len(result.skipped), 'skipped;', 'PASS' if result.wasSuccessful() else 'FAIL')
    assert result.wasSuccessful()


def final():
    old = load('BEFORE_ROADMAP_STATE.json')
    state = rm.load_json(CANON / 'ROADMAP_STATE.json')
    task = next(t for t in state['tasks'] if t['id'] == TARGET)
    checks = []
    def ck(name, ok):
        checks.append(dict(name=name, status='PASS' if ok else 'FAIL'))
    ck('conservation_checks', load('VALIDATION.json')['status'] == 'PASS')
    ck('all_80_other_tasks_identical', [t for t in state['tasks'] if t['id'] != TARGET] == [t for t in old['tasks'] if t['id'] != TARGET])
    ck('all_human_receipts_and_other_root_objects_unchanged', all(state[k] == old[k] for k in old if k not in {'mission_status', 'tasks', 'events', 'release_focus', 'runtime_validation_hold'}))
    ck('old_events_preserved', state['events'][:-1] == old['events'] and state['events'][-1]['id'] == 'SERG-RM-0067')
    ck('history_additive', (CANON / 'PROGRESS_HISTORY.md').read_bytes().startswith((OUT / 'BEFORE_PROGRESS_HISTORY.md').read_bytes()))
    ck('no_fictitious_terminal_status_or_decision', task['status'] == 'IN_PROGRESS' and task['decision'] is None and task['runtime_validation']['attestation'] is None and task['runtime_validation']['status'] == 'NOT_RUN')
    ck('existing_lusatian_installation_not_extended', task['installed_sub_lots'] == next(t for t in old['tasks'] if t['id'] == TARGET)['installed_sub_lots'])
    ck('engine_tests_remain_deferred', state['runtime_validation_hold']['deferred_until_prussia_finished_by_user'] and state['runtime_validation_hold']['does_not_block_implementation'])
    p = rm.progress(state)
    ck('unchanged_accounting_93_235_32_81', (p['earned_weight'], p['total_weight'], p['qualified_tasks'], p['total_tasks'], p['percent']) == (93, 235, 32, 81, '39.57'))
    check = rm.check()
    dump('CANONICAL_CHECK.json', check)
    ck('canonical_validator', check['status'] == 'PASS')
    ck('targeted_tests', load('TEST_RESULTS.json')['status'] == 'PASS')
    paths = ['tools/serg_glatz_silesia.py'] + [str((CANON / n).relative_to(ROOT)) for n in ['ROADMAP_STATE.json', 'ROADMAP.md', 'NEXT_ACTION.md', 'BLOCKERS.md', 'PROGRESS_HISTORY.md', 'PROGRESS_SNAPSHOT.json']]
    args = ['git', '--no-optional-locks', 'diff', '--check', '--', *paths]
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    dump('DIFF_CHECK.json', dict(command=args, exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr))
    ck('git_diff_check', result.returncode == 0)
    ck('runtime_still_identical_at_finish', prior.runtime() == load('BASELINE.json')['runtime'])
    dump('FINAL_CHECKS.json', dict(status='PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL', checks=checks, passed=sum(c['status'] == 'PASS' for c in checks), total=len(checks), progress=p,
        new_functional_changes=0, new_human_receipts=0, engine_test=False))
    print('Final:', len(checks), 'checks;', [c for c in checks if c['status'] != 'PASS'])
    assert all(c['status'] == 'PASS' for c in checks)


if __name__ == '__main__':
    {'evidence': evidence, 'validate': validate, 'track': track, 'tests': tests, 'final': final}[sys.argv[1]]()
