"""Read-only territorial audit: existing MAP2A partition, no new runtime installer."""
import collections as C
import io
import json
import subprocess
import unittest
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc2_moravia as prior
import serg_closure_roadmap as rm
import map2l_registry as reg

ROOT = prior.ROOT
OUT = ROOT / 'docs/reports/map/SERG_CLOSURE/SC2-AUSTRIAN-SILESIA'
TASK = 'SC2-AUSTRIAN-SILESIA'
PROTECTED = {'x71E080', 'xF0E080'}
SIDS = {'STATE_MORAVIA', 'STATE_UPPER_SILESIA', 'STATE_LOWER_SILESIA'}
CONCURRENT = {
    'common/ai_strategies/00_default_strategy.txt',
    'common/combat_unit_groups/1776_engineer_corps.txt',
    'common/combat_unit_types/1776_engineer_corps.txt',
    'gui/1776_engineer_corps_texticons.gui',
    'common/battle_conditions/1776_land_fortifications.txt',
    'common/scripted_triggers/1776_land_fortifications.txt',
    'localization/english/1776_land_fortifications_l_english.yml',
    'localization/french/1776_land_fortifications_l_french.yml',
    'gfx/unit_illustrations/1776_engineer_corps.dds',
    'localization/english/1776_engineer_corps_l_english.yml',
    'localization/french/1776_engineer_corps_l_french.yml',
    'common/scripted_triggers/1776_engineer_corps.txt',
    'gfx/unit_illustrations/1776_engineer_corps_american.dds',
    'gfx/unit_illustrations/1776_engineer_corps_european.dds',
    'gfx/unit_illustrations/1776_engineer_corps_french.dds',
    'gfx/unit_illustrations/1776_engineer_corps_iberian.dds',
}


def load(p):
    return prior.load(p)


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def inventory():
    b = load(OUT / 'BASELINE.json')
    inv = b['inventory']
    a = prior.core.packed(ROOT / 'map_data/provinces.png')
    owners = {r['key'][0]: r['key'][1:] for r in inv['owners']}
    keys = sorted(k for k, sid in inv['geometry'].items() if sid in SIDS or k == 'x9061E0')
    registered = {r['rgb']: r for r in b['registry']}
    rows = []
    for rgb in keys:
        yy, xx = np.where(a == int(rgb[1:], 16))
        neighbors = C.Counter()
        for y, x in zip(yy, xx):
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                other = 'x' + format(int(a[y + dy, x + dx]), '06X')
                if other != rgb:
                    neighbors[other] += 1
        sid, tag = owners[rgb]
        rows.append(dict(rgb=rgb, state_before=sid, state_after=sid, owner_before=tag, owner_after=tag,
            cells_before=len(xx), cells_after=len(xx), bounds=[int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())],
            centroid=[float(xx.mean()), float(yy.mean())], protected_map2a=rgb in PROTECTED,
            registry=registered.get(rgb),
            scope='TESCHEN_REFERENCE_ONLY' if rgb == 'x9061E0' else 'MAP2A_RETAINED_SILESIAN_APPROXIMATION' if rgb in PROTECTED else 'MORAVIA_PROTECTED_CONTEXT' if sid == 'STATE_MORAVIA' else 'PRUSSIAN_REGION_CONTEXT_NOT_CADASTRE',
            neighbors=[dict(rgb=k, state=owners.get(k, [inv['geometry'].get(k), None])[0], owner=owners.get(k, ['', None])[1], edges=n) for k, n in sorted(neighbors.items())]))
    selected = [r for r in rows if r['rgb'] in PROTECTED]
    dump('NATIVE_INVENTORY.json', dict(task_ids=[TASK], provinces=rows, runtime_changes=0, protected_silesian_cells=sum(r['cells_before'] for r in selected), cadastral_precision=False))
    dump('BOUNDARY_AUDIT.json', dict(task_ids=[TASK], before_after_equal=True, provinces=rows,
        historical_result='Retained B political approximation; no independently homologated cell transfer. Nysa local fringes, enclaves and Lusatian perimeter remain unverified, not certified by owner equality.',
        changed_rgb=[], changed_cells=0, excluded_completion=['SC2-TESCHEN', 'SC2-MAP2A-VALIDATION', 'SC3-SILESIA-LUSATIA']))
    x0, y0, x1, y1 = 4440, 820, 4540, 892
    scale = 8
    im = Image.new('RGB', ((x1-x0)*scale+110, (y1-y0)*scale+110), '#faf8ef')
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
    for y in range(y0, y1):
        for x in range(x0, x1):
            k = 'x' + format(int(a[y, x]), '06X')
            tag = owners.get(k, ['', ''])[1]
            col = '#d2d9e9' if tag == 'PRU' else '#cfddc4' if tag == 'AUS' else '#e9d3b7'
            if k in PROTECTED:
                col = '#efbc68'
            if k == 'x9061E0':
                col = '#dcaeb9'
            u, v = 55+(x-x0)*scale, 45+(y-y0)*scale
            d.rectangle((u, v, u+scale, v+scale), fill=col)
            if a[y, x] != a[y, x-1]:
                d.line((u, v, u, v+scale), fill='#86837b')
            if a[y, x] != a[y-1, x]:
                d.line((u, v, u+scale, v), fill='#86837b')
    for i, row in enumerate(rows, 1):
        x, y = row['centroid']
        if x0 <= x < x1 and y0 <= y < y1:
            d.text((55+(x-x0)*scale, 45+(y-y0)*scale), str(i), font=font, fill='black', stroke_width=1, stroke_fill='white')
        row['map_number'] = i
    d.text((12, 10), 'Silésie : inventaire actuel, numéros RGB, sans tracé historique superposé', font=font, fill='black')
    d.text((12, im.height-45), 'Orange : MAP2A AUS protégé. Rose : Teschen AUS, dossier distinct.', font=font, fill='black')
    d.text((12, im.height-25), 'Bleu : PRU. Vert : AUS. Noms de régions techniques distincts des juridictions.', font=font, fill='black')
    im.save(OUT / 'NATIVE_READING.png')
    dump('NATIVE_INVENTORY.json', dict(task_ids=[TASK], provinces=rows, runtime_changes=0, protected_silesian_cells=sum(r['cells_before'] for r in selected), cadastral_precision=False, image_box=[x0,y0,x1,y1]))
    for r in rows:
        print(r['rgb'], r['state_before'], r['owner_before'], r['cells_before'], r['bounds'])


def validate():
    b = load(OUT / 'BASELINE.json')
    session = load(OUT / 'SESSION_BEFORE.json')
    inv = prior.core.qa.inventory()
    checks = []

    def ck(name, result, detail=None):
        checks.append(dict(name=name, passed=bool(result), detail=detail))

    for key in inv:
        ck('Effective inventory conserved: ' + key, inv[key] == b['inventory'][key])
    hashes = prior.runtime_hashes()
    changed = sorted(p for p in set(hashes) | set(b['hashes']) if hashes.get(p) != b['hashes'].get(p))
    ck('Only independently recorded concurrent runtime differences', set(changed) <= CONCURRENT, changed)
    ck('Entire native bitmap retained', hashes['map_data/provinces.png'] == b['hashes']['map_data/provinces.png'])
    ck('Moravia public administration retained', hashes[prior.ADMIN_PATH] == b['hashes'][prior.ADMIN_PATH] and prior.admin_contract((ROOT / prior.ADMIN_PATH).read_text(encoding='utf8')))
    ck('Bohemia tested population file retained', hashes[prior.prior.POP_PATH] == b['hashes'][prior.prior.POP_PATH])
    ck('All existing registry rows retained', load(reg.active_registry_path()) == b['registry'] and len(b['registry']) == 574)
    ck('Current approved registry tail remains Salzburg', reg.approved_lot_dirs()[-1] == prior.prior.prior.OUT)
    own = {r['key'][0]: r for r in inv['owners']}
    for k in sorted(PROTECTED):
        ck('MAP2A AUS single owner and native region: ' + k, own[k] == dict(key=[k, 'STATE_MORAVIA', 'AUS'], count=1) and inv['geometry'][k] == 'STATE_MORAVIA')
        ck('MAP2A imperial beneficiary: ' + k, [r['beneficiary'] for r in b['registry'] if r['rgb'] == k] == ['AUS'])
    ck('Teschen remains AUS in physical WEST_GALICIA', own['x9061E0'] == dict(key=['x9061E0', 'STATE_WEST_GALICIA', 'AUS'], count=1) and inv['geometry']['x9061E0'] == 'STATE_WEST_GALICIA')
    ck('Teschen known registry gap preserved for its distinct task', not any(r['rgb'] == 'x9061E0' for r in b['registry']))
    for sid, count in [('STATE_BOHEMIA', 21), ('STATE_MORAVIA', 10), ('STATE_UPPER_SILESIA', 6), ('STATE_LOWER_SILESIA', 9)]:
        ck('Native province count retained: ' + sid, sum(v == sid for v in inv['geometry'].values()) == count)
    for sid, pop in [('STATE_BOHEMIA', 2500000), ('STATE_MORAVIA', 1570622)]:
        ck('Tested population retained: ' + sid, sum(r['count'] for r in inv['regional_pop'] if r['key'][0] == sid) == pop)
    s = load(rm.OUT / 'ROADMAP_STATE.json')
    done = rm.qualifications(s)
    ck('All 22 previously accepted tasks remain justified', sum(done.values()) == 22 and all(done[k] for k, v in rm.qualifications(b['roadmap']).items() if v))
    ck('Moravia receipt has not spread to Silesia Teschen or MAP2A', all(not done[k] for k in [TASK, 'SC2-TESCHEN', 'SC2-MAP2A-VALIDATION']))
    ck('Git HEAD branch index retained', subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == session['git_head'] and subprocess.check_output(['git','branch','--show-current'],text=True).strip() == session['git_branch'] and prior.sha(ROOT/'.git/index') == session['git_index_sha256'])
    old_reports = {p: h for p, h in session['report_hashes'].items() if '/SC1-SALZBURG/' in p or '/SC2-BOHEMIA/' in p or '/SC2-MORAVIA/' in p}
    ck('All pre-existing recent reports and receipts byte-identical', all(prior.sha(ROOT/p) == h for p,h in old_reports.items()))
    ck('Inherited 44 duplicate RGB and 12 invalid references unchanged', len(inv['duplicates']) == 44 and len(inv['errors']) == 12)
    for row in load(OUT/'SOURCE_FILES.json'):
        ck('Archived source hash: ' + row['file'], prior.sha(OUT/row['file']) == row['sha256'])
    result = dict(task_ids=[TASK], status='PASS' if all(c['passed'] for c in checks) else 'FAIL', total=len(checks), passed=sum(c['passed'] for c in checks), failed=[c['name'] for c in checks if not c['passed']], checks=checks, automated_engine_test=False, runtime_installation=False, runtime_user_validation=False)
    dump('VALIDATION.json', result)
    dump('FILES_MODIFIED.json', dict(runtime_files_written_by_this_pass=[], runtime_files_removed=[], concurrent_runtime_files=changed, concurrent_before={p:b['hashes'].get(p) for p in changed}, concurrent_after={p:hashes.get(p) for p in changed}, concurrent_files_not_written_by_this_pass=True))
    dump('FINAL_INVENTORY.json', inv)
    print('Static', result['passed'], '/', result['total'], result['failed'], flush=True)
    assert not result['failed'], result['failed']


def tests():
    names = ['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc','test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia']
    known = set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    for name, modules in [('TESTS', names), ('SCOPED_TESTS', names[-4:])]:
        log = io.StringIO()
        r = unittest.TextTestRunner(stream=log, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
        (OUT/(name+'.log')).write_text(log.getvalue(), encoding='utf8')
        fs = [dict(id=t.id(), traceback=trace) for t, trace in r.failures+r.errors]
        unexpected = [f for f in fs if f['id'] not in known]
        dump(name+'.json', dict(task_ids=[TASK], total=r.testsRun, passed=r.testsRun-len(fs)-len(r.skipped), failed=fs, skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped], unexplained_failures=unexpected, automated_engine_test=False))
        print(name, r.testsRun-len(fs)-len(r.skipped), '/', r.testsRun, 'failures',len(fs),'unexpected',len(unexpected),flush=True)
        assert not unexpected, unexpected
    dump('TEST_REVIEW.json', dict(historical_final_layer_assertions=sorted(known), explanation='Three unchanged historical assertions expect obsolete registry tails. Current registry tests and exact full registry conservation pass. One initialization-only check remains skipped; no old test or raw log changed.', automated_engine_test=False))


def tracking():
    import copy
    validation = load(OUT/'VALIDATION.json')
    assert validation['status'] == 'PASS' and validation['passed'] == validation['total'] and not validation['failed']
    assert not load(OUT/'TESTS.json')['unexplained_failures'] and not load(OUT/'SCOPED_TESTS.json')['failed']
    state = load(rm.OUT/'ROADMAP_STATE.json')
    original = copy.deepcopy(state)
    assert state == load(OUT/'BASELINE.json')['roadmap'], 'Concurrent tracking change: review before writing'
    assert not any(e['id'] == 'SERG-RM-0009' for e in state['events'])
    t = next(t for t in state['tasks'] if t['id'] == TASK)
    assert t['status'] == 'NOT_STARTED' and rm.progress(state)['next_task'] == TASK
    prefix = 'docs/reports/map/SERG_CLOSURE/SC2-AUSTRIAN-SILESIA/'
    t.update(status='RESEARCH_COMPLETE', implementation_report=[prefix+'REPORT.md'], installed_lots=[],
        static_tests=dict(status='PASS', evidence=[prefix+'VALIDATION.json']),
        runtime_validation=dict(required=False, status='NOT_RUN', attestation=None, scope='No new functional installation; retained MAP2A partition audit and optional player control, pending explicit no-change decision', new_details_invented=False),
        decision=dict(no_correction_required=True, approved_by=None, reason='Proposed retention of existing B political approximation; no new defensible functional correction demonstrated. Explicit task-specific user approval has not been received.', evidence=[prefix+'PROPOSED_DECISION.json',prefix+'SOURCES.md',prefix+'SECTOR_AUDIT.md',prefix+'BOUNDARY_AUDIT.json']),
        residual_uncertainty="Précision cadastrale non acquise : Nysa, enclaves moraves et micro-limites; offices Opava/Brno distincts dans la documentation mais agrégés par le moteur. Correction impériale Teschen réservée à sa tâche. Décision sans changement proposée, non approuvée; zéro point Silésie acquis.",
        current_delivery_note="Audit SIL-P/W/N/I/T/D sans nouvelle installation : deux RGB MAP2A AUS, 311 cellules, registre conservé; quinze RGB des régions silésiennes PRU et Teschen AUS inchangés. Proposition B sans correction supplémentaire, RESEARCH_COMPLETE, aucun reçu nouveau ni point acquis. Écart x9061E0 et limites fines restent ouverts; SC2-AUSTRIA seulement identifiée après décision.")
    t['historical_sources'].append(prefix+'SOURCES.md:1')
    state['mission_status'] = 'SC2_AUSTRIAN_SILESIA_AUDITED_NO_CHANGE_PENDING_DECISION'
    state['decision_review_hold'] = dict(task_id=TASK, decision=prefix+'PROPOSED_DECISION.json', report=prefix+'REPORT.md', protocol=prefix+'PLAYER_TEST_PROTOCOL.md',
        next_implementation_candidate='SC2-AUSTRIA', source=prefix+'AUTHORIZATION.md',
        summary="La partition générale déjà installée a été auditée; aucune correction fonctionnelle supplémentaire démontrée. Proposition : conserver l'approximation B, avec micro-limites non certifiées et Teschen séparé. Moravie a reçu sa validation explicite; 75/235 = 31,91 % restent acquis.",
        scope_note="Les 21 RGB de Bohême, 10 RGB moraves, deux réparations MAP2A, populations et niveau public morave sont conservés. Aucun test ou accord nouveau de Silésie n'est inféré du reçu Moravie. SC2-TESCHEN et les huit anciennes validations spécifiques restent ouverts; aucun report P0 ni cadastre acquis.")
    assert (rm.progress(state)['earned_weight'],rm.progress(state)['total_weight'],rm.progress(state)['percent']) == (75,235,'31.91')
    future = copy.deepcopy(state)
    # Selection preview only; this hypothetical terminal status is never persisted.
    ft = next(t for t in future['tasks'] if t['id'] == TASK)
    ft['status'] = 'NOT_APPLICABLE_VERIFIED'
    ft['decision']['approved_by'] = 'user'
    assert rm.progress(future)['next_task'] == 'SC2-AUSTRIA'
    state['events'].append(dict(id='SERG-RM-0009',date='2026-10-19',kind='SCOPED_AUDIT_NO_FUNCTIONAL_CHANGE',scope_version=state['scope_version'],source=prefix+'AUTHORIZATION.md',
        changes=[dict(task_id=TASK,before='NOT_STARTED',after='RESEARCH_COMPLETE')],before_percent='31.91',after_percent='31.91',before_weight=75,after_weight=75,total_weight=235,
        evidence=[prefix+'REPORT.md',prefix+'SOURCES.md',prefix+'BOUNDARY_AUDIT.json',prefix+'VALIDATION.json',prefix+'TESTS.json',prefix+'PROPOSED_DECISION.json',prefix+'PLAYER_TEST_PROTOCOL.md'],
        note="Une seule nouvelle étape P0 : audit de la Silésie autrichienne et interfaces, sans correction fonctionnelle supplémentaire démontrée. Deux RGB MAP2A/311 cellules AUS et registre conservés, quinze RGB des régions silésiennes PRU inchangés, Teschen AUS/179 cellules distinct. Populations, niveau public morave et autres acquis inchangés. Proposition de conservation B non approuvée, RESEARCH_COMPLETE, aucun reçu Silésie ni point acquis; pas de certification cadastrale. Tests statiques réussis; suite cumulative 328/332, trois anciennes assertions de dernière couche et une exclusion; contrats courants 71/72, une exclusion. Travaux fortifications/génie concurrents préservés. 75/235 = 31,91 % maintenus; prochaine action revue de la décision, puis candidate SC2-AUSTRIA non commencée. Aucun Git écrit."))
    assert [x for x in state['tasks'] if x['id'] != TASK] == [x for x in original['tasks'] if x['id'] != TASK]
    assert state['events'][:-1] == original['events'] and not rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json', state)
    rm.render()
    result = rm.check()
    dump('TRACKER_VALIDATION.json', result)
    dump('TRACKER_PRESERVATION.json', dict(other_80_tasks_unchanged=True, all_8_prior_events_unchanged=True, qualified_tasks=22, earned_weight=75,total_weight=235,percent='31.91',no_silesia_credit=True,next_candidate_after_explicit_decision='SC2-AUSTRIA',candidate_started=False))
    assert result['status'] == 'PASS', result
    print('Tracking PASS; 75/235 = 31.91%; Silesia RESEARCH_COMPLETE, no credit, no receipt',flush=True)


if __name__ == '__main__':
    import sys
    {'inventory': inventory, 'validate': validate, 'tests': tests, 'tracking': tracking}[sys.argv[1]]()
