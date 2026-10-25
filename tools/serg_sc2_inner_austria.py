"""SC2 Inner Austria: bounded inventory, installation and conservation evidence."""
import collections as C
import io
import json
import subprocess
import sys
import unittest
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc2_moravia as shared
import serg_sc2_austria as previous
import serg_closure_roadmap as rm
import map2l_registry as reg

ROOT = shared.ROOT
OUT = rm.OUT / 'SC2-INNER-AUSTRIA'
TASK = 'SC2-INNER-AUSTRIA'
SIDS = {'STATE_STYRIA', 'STATE_SLOVENIA'}
CONTEXT = {'STATE_TYROL', 'STATE_ISTRIA', 'STATE_CROATIA', 'STATE_TRANSDANUBIA'}
ADMIN_FILES = {
    'STATE_STYRIA': 'common/history/buildings/1776_sc2_inner_austria_styria.txt',
    'STATE_SLOVENIA': 'common/history/buildings/1776_sc2_inner_austria_carniola.txt',
}
PMS = shared.PMS
MARITIME_FILES = ['common/history/buildings/01_south_europe.txt',
    'common/history/buildings/98_build_start_1776_world_redistribution.txt']
MARITIME_TYPES = {'building_port', 'building_shipyard'}


def load(path):
    return rm.load_json(path)


def dump(name, obj):
    rm.write_json(OUT / name, obj)


def inventory():
    b = load(OUT / 'BASELINE.json')
    inv = b['inventory']
    a = shared.core.packed(ROOT / 'map_data/provinces.png')
    owners = {r['key'][0]: r['key'][1:] for r in inv['owners']}
    registered = {r['rgb']: r for r in b['registry']}
    rows = []
    for rgb, sid in sorted(inv['geometry'].items()):
        if sid not in SIDS | CONTEXT:
            continue
        yy, xx = np.where(a == int(rgb[1:], 16))
        contacts = C.Counter()
        for y, x in zip(yy, xx):
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                other = 'x' + format(int(a[y + dy, x + dx]), '06X')
                if other != rgb:
                    contacts[other] += 1
        rows.append(dict(rgb=rgb, state_before=sid, state_after=sid,
            owner_before=owners[rgb][1], owner_after=owners[rgb][1],
            cells_before=len(xx), cells_after=len(xx),
            bounds=[int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())],
            centroid=[float(xx.mean()), float(yy.mean())], registry=registered.get(rgb),
            scope='AUDITED_AGGREGATE' if sid in SIDS else 'NEIGHBOR_CONTEXT_ONLY',
            neighbors=[dict(rgb=k, state=owners.get(k, ['', ''])[0],
                owner=owners.get(k, ['', ''])[1], edges=n) for k, n in sorted(contacts.items())]))
    core = [r for r in rows if r['state_before'] in SIDS]
    for i, row in enumerate(core, 1):
        row['map_number'] = i
    dump('NATIVE_INVENTORY.json', dict(task_ids=[TASK], provinces=rows,
        audited_rgb=len(core), audited_cells=sum(r['cells_before'] for r in core),
        regions={sid: dict(population=sum(r['count'] for r in inv['regional_pop'] if r['key'][0] == sid),
            population_groups=[r for r in inv['regional_pop'] if r['key'][0] == sid],
            buildings=[r for r in inv['buildings'] if r['key'][0] == sid],
            units=[r for r in inv['units'] if r['key'][2] == sid]) for sid in sorted(SIDS)},
        cadastral_precision=False, political_boundaries_changed=False))
    x0, y0, x1, y1, scale = 4370, 920, 4490, 1000, 8
    im = Image.new('RGB', ((x1-x0)*scale+80, (y1-y0)*scale+100), '#faf8ef')
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
    for y in range(y0, y1):
        for x in range(x0, x1):
            rgb = 'x' + format(int(a[y, x]), '06X')
            sid, tag = owners.get(rgb, ['', ''])
            col = {'STATE_STYRIA':'#e7c77a', 'STATE_SLOVENIA':'#adceb6'}.get(sid,
                '#b4c8e0' if tag == 'VEN' else '#e3d8ce' if tag == 'AUS' else '#d4c7d7')
            u, v = 40+(x-x0)*scale, 45+(y-y0)*scale
            d.rectangle((u, v, u+scale, v+scale), fill=col)
            if a[y, x] != a[y, x-1]:
                d.line((u,v,u,v+scale), fill='#807d77')
            if a[y, x] != a[y-1, x]:
                d.line((u,v,u+scale,v), fill='#807d77')
    for r in core:
        x, y = r['centroid']
        d.text((40+(x-x0)*scale,45+(y-y0)*scale),str(r['map_number']),font=font,fill='black',stroke_width=1,stroke_fill='white')
    for x,y,name in [(4447.991,949.445,'Graz'),(4423.581,960.823,'Klagenfurt'),
            (4430.156,977.532,'Ljubljana'),(4446.185,962.969,'Maribor'),
            (4459.184,961.528,'Ptuj'),(4412.139,990.417,'Trieste')]:
        u,v=40+(x-x0)*scale,45+(y-y0)*scale
        d.ellipse((u-3,v-3,u+3,v+3),fill='#102e34')
        d.text((u+4,v+3),name,font=font,fill='black',stroke_width=1,stroke_fill='white')
    d.text((10,10),'SC2-INNER-AUSTRIA : régions techniques actuelles, numéros RGB',font=font,fill='black')
    d.text((10,im.height-40),'Ocre : STATE_STYRIA. Vert : STATE_SLOVENIA. Aucun tracé historique superposé.',font=font,fill='black')
    d.text((10,im.height-22),'Marqueurs : locators du jeu, pas preuves de souveraineté. Bleu : VEN.',font=font,fill='black')
    im.save(OUT/'NATIVE_READING.png')
    print(len(core),'RGB',sum(r['cells_before'] for r in core),'cells',flush=True)
    for r in core:
        print(r['rgb'],r['state_before'],r['cells_before'],r['bounds'],flush=True)


def expected_admin(sid):
    assert sid in SIDS
    # Same national PM abstraction as the accepted Moravia installation.
    return shared.expected_admin().replace('SC2-MORAVIA', TASK).replace(
        'minimal representation of the Moravian gubernium at Brno.',
        'minimal regional representation of Inner Austrian public administration.').replace(
        's:STATE_MORAVIA', 's:'+sid).replace(
        '# The technical state includes protected MAP2A districts; no 1783 legal merger is asserted.',
        '# Regional aggregate; distinct duchies and offices are not legally merged.')


def admin_contract(raw, sid):
    normalize = lambda text: [shared.core.qa.signature(n) for n in shared.core.cw.parse(text)]
    assert normalize(raw) == normalize(expected_admin(sid)), 'Out-of-scope administration, owner, level, PM or effect'
    return True


def install():
    b = load(OUT/'BASELINE.json')
    assert load(rm.OUT/'ROADMAP_STATE.json') == b['roadmap'], 'Concurrent tracker change requires review'
    assert rm.progress(b['roadmap'])['next_task'] == TASK
    assert all((OUT/p).is_file() for p in ['AUTHORIZATION.md','SOURCES.md','SECTOR_AUDIT.md'])
    assert all(not (ROOT/path).exists() for path in ADMIN_FILES.values()), 'Never overwrite a concurrent file'
    current = shared.runtime_hashes()
    delta = {p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)}
    assert delta <= previous.CONCURRENT, 'Review unexpected concurrent change: '+str(delta-previous.CONCURRENT)
    inv = shared.core.qa.inventory()
    for sid in SIDS:
        assert not any(r['key'][0]==sid and 'building_government_administration' in r['key'][2]
            for r in inv['buildings']), 'Effective administration already exists in '+sid
    dump('INSTALL_BASELINE.json', dict(hashes=current, concurrent_runtime_files=sorted(delta),
        concurrent_hashes={p:current.get(p) for p in delta}, all_preserved_without_writing=True))
    for sid, path in ADMIN_FILES.items():
        raw = expected_admin(sid)
        admin_contract(raw, sid)
        # Exclusive creation protects a file introduced since the checks above.
        with (ROOT/path).open('xb') as f:
            f.write(raw.encode('utf8'))
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_PENDING_STATIC_CHECKS',
        sub_lots=[dict(id='IA-I-ST' if sid=='STATE_STYRIA' else 'IA-I-C', state=sid, file=path,
            building='building_government_administration',levels_before=0,levels_after=1,owner='c:AUS',
            production_methods=PMS) for sid,path in ADMIN_FILES.items()],
        territory_changed=False,population_changed=False,registry_changed=False,
        historical_staff_count_claim=False,cadastral_precision=False,automated_engine_test=False))
    print('Installed two independently testable files: one public AUS level per aggregate',flush=True)


def inland_cleanup(raw):
    """Remove only the two coastal-only declarations in the inland AUS aggregate."""
    region=shared.core.region(raw,'STATE_SLOVENIA','AUS')
    selected=[n for n in region.children('create_building')
        if shared.core.cw.scalar(n.one('building')) in MARITIME_TYPES]
    assert len(selected)==2, 'Expected precisely one inland port and one shipyard'
    assert {shared.core.cw.scalar(n.one('building')) for n in selected}==MARITIME_TYPES
    # Node signatures must agree with the captured region, including ownership and PMs.
    baseline=load(OUT/'BASELINE.json')['inventory']['buildings']
    permitted={r['key'][2] for r in baseline if r['key'][:2]==['STATE_SLOVENIA','AUS']}
    assert all(shared.core.qa.signature(n) in permitted for n in selected), 'Concurrent maritime payload differs'
    edits=[]
    for n in selected:
        start=raw.rfind('\n',0,n.start)+1
        assert not raw[start:n.start].strip(), 'Building declaration does not start on its own line'
        edits.append((start,n.end,''))
    return shared.core.edits(raw,edits), selected


def maritime_contract(before, after):
    expected,_=inland_cleanup(before)
    assert after == expected, 'Change outside the four scoped maritime declarations'
    return True


def cleanup_maritime():
    assert not (OUT/'MARITIME_CLEANUP.json').exists(), 'Never replay a completed correction'
    b=load(OUT/'BASELINE.json')
    before_dir=OUT/'MARITIME_BEFORE';before_dir.mkdir()
    records=[]
    for path in MARITIME_FILES:
        target=ROOT/path;old=target.read_bytes()
        assert shared.sha(target)==b['hashes'][path], 'Concurrent file change requires review: '+path
        candidate,nodes=inland_cleanup(old.decode('utf8'))
        before_path=before_dir/target.name;before_path.write_bytes(old)
        candidate_path=OUT/('MARITIME_CANDIDATE_'+target.name);candidate_path.write_bytes(candidate.encode('utf8'))
        assert target.read_bytes()==old, 'Concurrent edit after capture: '+path
        target.write_bytes(candidate.encode('utf8'))
        records.append(dict(file=path,before_file=str(before_path.relative_to(OUT)).replace('\\','/'),
            candidate_file=candidate_path.name,before_sha256=b['hashes'][path],after_sha256=shared.sha(target),
            removed_signatures=[shared.core.qa.signature(n) for n in nodes]))
    dump('MARITIME_CLEANUP.json',dict(task_ids=[TASK],sub_lot='IA-E-C',files=records,
        reason='Both coastal-only building types are declared in an inland native region without port locator or naval exit; historical Carniola is distinct from the Adriatic jurisdictions.',
        affected_state='STATE_SLOVENIA',removed_declarations=4,declared_port_levels_removed=6,declared_shipyard_levels_removed=2,
        effective_engine_levels_claimed=False,neighboring_coastal_buildings_changed=False,population_changed=False))
    print('Removed four inland maritime declarations; other bytes retained',flush=True)


def validate():
    b=load(OUT/'BASELINE.json'); session=load(OUT/'SESSION_BEFORE.json')
    inv=shared.core.qa.inventory(); checks=[]
    def ck(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for field in inv:
        if field not in ('buildings','building_levels_written'):
            ck('Effective inventory retained: '+field,inv[field]==b['inventory'][field])
    expected=shared.core.qa.counter(b['inventory']['buildings'])
    for sid,path in ADMIN_FILES.items():
        raw=(ROOT/path).read_text(encoding='utf8')
        ck('Exact bounded installation: '+sid,admin_contract(raw,sid))
        node=shared.core.region(raw,sid,'AUS').children('create_building')[0]
        expected[(sid,'AUS',shared.core.qa.signature(node))]+=1
    cleanup=load(OUT/'MARITIME_CLEANUP.json')
    for record in cleanup['files']:
        old=(OUT/record['before_file']).read_bytes().decode('utf8')
        candidate,_=inland_cleanup(old)
        ck('Exact scoped maritime removal, other bytes retained: '+record['file'],
            maritime_contract(old,(ROOT/record['file']).read_bytes().decode('utf8')))
        for signature in record['removed_signatures']:
            expected[('STATE_SLOVENIA','AUS',signature)]-=1
    expected=+expected
    ck('Only two administrations and four inland maritime removals',
        shared.core.qa.counter(inv['buildings'])==expected)
    levels=shared.core.qa.counter(b['inventory']['building_levels_written'])
    levels['building_government_administration']+=2
    levels['building_port']-=6;levels['building_shipyard']-=2
    ck('Only expected written level deltas worldwide',shared.core.qa.counter(inv['building_levels_written'])==levels)
    current=shared.runtime_hashes(); anchor=load(OUT/'INSTALL_BASELINE.json')['hashes']
    delta=sorted(p for p in set(current)|set(anchor) if current.get(p)!=anchor.get(p))
    concurrent=[p for p in delta if p in previous.CONCURRENT]
    ours=[p for p in delta if p not in previous.CONCURRENT]
    ck('Only four scoped files outside reviewed concurrent work',set(ours)==set(ADMIN_FILES.values())|set(MARITIME_FILES),dict(ours=ours,concurrent=concurrent))
    ck('All existing runtime files preserved outside targeted removals and concurrent paths',all(current.get(p)==digest for p,digest in b['hashes'].items() if p not in previous.CONCURRENT|set(MARITIME_FILES)))
    ck('Full province bitmap byte-identical',current['map_data/provinces.png']==b['hashes']['map_data/provinces.png'])
    ck('574 registry rows and beneficiaries retained',load(reg.active_registry_path())==b['registry'] and len(b['registry'])==574)
    ck('Approved registry tail remains Salzburg',reg.approved_lot_dirs()[-1]==shared.prior.prior.OUT)
    native=load(OUT/'NATIVE_INVENTORY.json')
    ck('12 audited RGB / 3130 cells',native['audited_rgb']==12 and native['audited_cells']==3130)
    for row in native['provinces']:
        if row['state_before'] not in SIDS:
            continue
        rgb=row['rgb']; sid=row['state_before']
        ck('Native owner and imperial beneficiary retained: '+rgb,
            [r for r in inv['owners'] if r['key'][0]==rgb]==[dict(key=[rgb,sid,'AUS'],count=1)]
            and inv['geometry'][rgb]==sid and row['registry']['beneficiary']=='AUS')
    for sid,total in [('STATE_STYRIA',599143),('STATE_SLOVENIA',395031)]:
        ck('Population retained: '+sid,sum(r['count'] for r in inv['regional_pop'] if r['key'][0]==sid)==total)
    ck('World population retained: 834926252',sum(r['count'] for r in inv['pops'])==834926252)
    ck('Tested Moravia administration retained',current[shared.ADMIN_PATH]==b['hashes'][shared.ADMIN_PATH])
    ck('Inherited diagnostics retained: 44 duplicate RGB / 12 references',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    state=load(rm.OUT/'ROADMAP_STATE.json');done=rm.qualifications(state)
    ck('23 acquired tasks retain their justified evidence',sum(done.values())==23 and all(done[k] for k,v in rm.qualifications(b['roadmap']).items() if v))
    austria=next(t for t in state['tasks'] if t['id']=='SC2-AUSTRIA')
    ck('Austria remains BLOCKED, no retention approval or receipt',austria['status']=='BLOCKED' and austria['decision']['no_correction_required'] is False and austria['runtime_validation']['attestation'] is None)
    ck('Silesia remains NA with separate Teschen',next(t for t in state['tasks'] if t['id']=='SC2-AUSTRIAN-SILESIA')['status']=='NOT_APPLICABLE_VERIFIED' and next(t for t in state['tasks'] if t['id']=='SC2-TESCHEN')['status']=='NOT_STARTED')
    ck('All previous pass reports and receipts byte-identical',all(shared.sha(ROOT/p)==digest for p,digest in session['report_hashes'].items() if (ROOT/p).parent != rm.OUT))
    def definitions(folder):
        return {n.key:n for p in shared.core.qa.effective(ROOT,shared.core.qa.GAME,folder)
            for n in shared.core.cw.parse(p.read_text(encoding='utf-8-sig'))}
    pms=definitions('common/production_methods');groups=definitions('common/production_method_groups');buildings=definitions('common/buildings')
    for key in MARITIME_TYPES:
        ck('Effective coastal requirement retained: '+key,
            any(shared.core.cw.scalar(n.one('is_coastal'))=='yes' for n in buildings[key].children('potential')))
    native_slovenia=next(n for n in shared.core.cw.parse((ROOT/'map_data/state_regions/01_south_europe.txt').read_text(encoding='utf-8-sig')) if n.key=='STATE_SLOVENIA')
    ck('Ljubljana aggregate has no native port or naval exit',not native_slovenia.children('port') and not native_slovenia.children('naval_exit_id'))
    ck('All four Ljubljana RGB have only owned terrestrial neighbors',all(
        r['neighbors'] and all(q['owner'] in {'AUS','VEN','HUN'} for q in r['neighbors'])
        for r in native['provinces'] if r['state_before']=='STATE_SLOVENIA'))
    ck('No inland maritime declarations remain',not any(r['key'][0]=='STATE_SLOVENIA' and any(k in r['key'][2] for k in MARITIME_TYPES) for r in inv['buildings']))
    neighbors=[r for r in native['provinces'] if r['state_before'] in CONTEXT]
    for sid,tag in [('STATE_CROATIA','AUS'),('STATE_TRANSDANUBIA','HUN')]:
        nearby=[r for r in neighbors if r['state_before']==sid and any(q['state'] in SIDS for q in r['neighbors'])]
        ck('Outer imperial interface retained: '+sid,bool(nearby) and all(r['owner_before']==tag and r['registry'] is None for r in nearby))
    aus=shared.core.cw.parse((ROOT/'common/history/countries/aus - austria.txt').read_text(encoding='utf-8-sig'))[0].children()[0]
    laws={shared.core.cw.scalar(n.value).removeprefix('law_type:') for n in aus.children('activate_law')}
    tech={shared.core.cw.scalar(n.value) for n in aus.children('add_technology_researched')}
    pmgroups=[shared.core.cw.scalar(n.value) for n in buildings['building_government_administration'].children('production_method_groups')[0].children()]
    for key in PMS:
        ck('Effective PM exists: '+key,key in pms)
        node=pms[key]
        values=lambda field: {shared.core.cw.scalar(n.value) for n in node.children(field)[0].children()} if node.children(field) else set()
        ck('Available with existing AUS laws/technologies: '+key,(not values('unlocking_laws') or bool(values('unlocking_laws')&laws)) and not values('disallowing_laws')&laws and values('unlocking_technologies')<=tech)
        matches=[g for g in pmgroups if key in {shared.core.cw.scalar(n.value) for n in groups[g].children('production_methods')[0].children()}]
        ck('Exactly one effective PM group: '+key,len(matches)==1,matches)
    ck('One selected PM per administration group',len(PMS)==len(pmgroups))
    changed_tools=[p for p,digest in b['tool_hashes'].items() if shared.sha(ROOT/p)!=digest]
    ck('Existing tools/tests retained',set(changed_tools)<={'tools/build_land_fortification_battles.py','tools/validate_land_fortifications.py','tools/build_engineer_corps_art.py'},changed_tools)
    ck('Git HEAD branch index retained',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==b['git_head'] and subprocess.check_output(['git','branch','--show-current'],text=True).strip()==b['git_branch'] and shared.sha(ROOT/'.git/index')==b['git_index_sha256'])
    for row in load(OUT/'SOURCE_FILES.json'):
        ck('Archived source hash: '+row['file'],shared.sha(OUT/row['file'])==row['sha256'])
    v=dict(task_ids=[TASK],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'STATIC_REVIEW_REQUIRED',
        total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,
        engine_executed=False,automated_engine_test=False,runtime_validation='PENDING_USER',world_population=sum(r['count'] for r in inv['pops']))
    dump('VALIDATION.json',v)
    dump('FILES_MODIFIED.json',dict(runtime_files_written_by_this_pass=ours,existing_runtime_files_written_by_this_pass=MARITIME_FILES,
        sha256={p:current[p] for p in ours},concurrent_runtime_files=concurrent,concurrent_sha256={p:current.get(p) for p in concurrent},
        concurrent_files_not_written_by_this_pass=True,old_tools_changed=changed_tools))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True)
    assert not v['failed']


def tests():
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01',
        'test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion',
        'test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political','test_map2w_r4bc',
        'test_serg_closure_roadmap','test_serg_sc1_salzburg','test_serg_sc2_bohemia','test_serg_sc2_moravia',
        'test_serg_sc2_inner_austria']
    inherited=set(load(previous.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    for label, modules in [('TESTS',names),('SCOPED_TESTS',names[-5:])]:
        stream=io.StringIO()
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
        unexplained=[f for f in failures if f['id'] not in inherited]
        dump(label+'.json',dict(task_ids=[TASK],status='PASS' if not failures else 'INHERITED_FAILURES_ONLY' if not unexplained else 'FAIL',
            total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,
            skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,'unexplained',len(unexplained),flush=True)
        for row in unexplained:
            print(row['id'],row['traceback'],flush=True)
        assert not unexplained
        assert {f['id'] for f in failures} == (inherited if label=='TESTS' else set())
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),unexplained_failures=[],
        old_tests_not_modified=True,explanation='Three inherited tests assume an older final registry layer. The current approved Salzburg tail and unchanged 574-row registry pass. No obsolete test is rewritten or hidden.',
        initial_only_skip='Read-only initialization invariant is not applicable after authorized installations.',engine_executed=False))


def tracking():
    import copy
    v=load(OUT/'VALIDATION.json'); tests_result=load(OUT/'TESTS.json'); scoped=load(OUT/'SCOPED_TESTS.json')
    assert v['total']==v['passed'] and not v['failed']
    assert not tests_result['unexplained_failures'] and not scoped['failed']
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==load(OUT/'BASELINE.json')['roadmap'], 'Concurrent tracker update requires reconciliation'
    t=next(t for t in state['tasks'] if t['id']==TASK)
    assert t['status']=='NOT_STARTED' and rm.progress(state)['next_task']==TASK
    p='docs/reports/map/SERG_CLOSURE/SC2-INNER-AUSTRIA/'
    t.update(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',implementation_report=[p+'REPORT.md'],
        installed_lots=['SERG_CLOSURE/SC2-INNER-AUSTRIA'],static_tests=dict(status='PASS',evidence=[p+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,new_details_invented=False,
            scope='IA-I-ST and IA-I-C: one public AUS administration per technical region; IA-E-C: removal of four inland maritime declarations; scoped conservation, new game, month, save/reload pending.'),
        residual_uncertainty='Approximation B des agrégats; aucune homologation cadastrale des limites internes, certification des populations historiques ou extension aux périphéries Salzbourg/Freising. Innviertel, Tyrol, Teschen et interface adriatique restent distincts. Trois sous-lots fonctionnels installés mais non testés par le joueur.',
        current_delivery_note='Audit des trois duchés et interfaces livré. Deux niveaux administratifs publics AUS ajoutés dans deux fichiers autonomes; quatre déclarations maritimes côtières impossibles retirées du seul agrégat intérieur de Ljubljana dans deux fichiers existants. 12 RGB/3130 cellules, propriétaires, 994174 habitants, unités et registre conservés. Aucun reçu humain ni point; test nouvelle partie 1776, trois sous-lots, un mois et sauvegarde/rechargement en attente.')
    t['historical_sources'].append(p+'SOURCES.md:1')
    t['identified_problem'].append('Absence de capacité administrative initiale dans les deux agrégats malgré les offices provinciaux attestés; déclarations de port/chantier maritime dans un agrégat intérieur sans accès naval. Corrections installées, test joueur requis.')
    t['delivered_scope']=dict(classification='B_POLITICAL_ADMINISTRATIVE_APPROXIMATION',sub_lots=['IA-I-ST','IA-I-C','IA-E-C'],
        native_rgb=12,native_cells=3130,territory_changed=False,population_changed=False,cadastral_validation=False)
    next_candidate=rm.progress(state)['next_task'];assert next_candidate=='SC2-ANTERIOR-AUSTRIA'
    state['mission_status']='SC2_INNER_AUSTRIA_IMPLEMENTED_AWAITING_USER'
    state['runtime_validation_hold']=dict(task_id=TASK,protocol=p+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=next_candidate,
        source=p+'AUTHORIZATION.md',reason='Three newly installed functional sub-lots require scoped user validation; one new step only in this mission.',
        test_summary='Nouvelle partie au 1er janvier 1776 : Autriche, un niveau administratif public dans la région de Graz–Carinthie et un dans celle de Ljubljana, PM utilisables; absence de port et chantier maritime dans cet agrégat intérieur, routes/commerce et régions voisines conservés. Simuler un mois complet puis sauvegarder/recharger et signaler les résultats des trois sous-lots.',
        scope_note="SC2-AUSTRIA reste BLOCKED : Innviertel bavarois en 1776, conservation définitive de l'erreur potentielle non approuvée. Aucun nouveau calage tenté. L'interface adriatique a seulement servi au bornage de cette passe; SC2-ANTERIOR-AUSTRIA reste une mission future non commencée. Aucun cadastre, chiffre historique de population, nouveau territoire salzbourgeois ou Teschen certifié.")
    note=f"Une seule nouvelle étape P0 : SC2-INNER-AUSTRIA. Trois cartes primaires lues et offices antérieurs à 1776 distingués des réformes de 1782/83. Deux niveaux publics AUS installés, un par agrégat; retrait de quatre déclarations de port/chantier maritime sans accès côtier dans STATE_SLOVENIA, autres octets des deux fichiers préservés. Aucun territoire, population ou registre modifié; trois sous-lots indépendants. {v['passed']}/{v['total']} contrôles statiques; suite cumulative {tests_result['passed']}/{tests_result['total']}, trois assertions héritées et une exclusion; contrats {scoped['passed']}/{scoped['total']}, une exclusion, aucun échec inexpliqué. Aucun reçu humain, Git écrit ou vanilla modifié. Travaux validés et concurrents préservés. 78/235 = 33,19 % maintenus; test joueur en attente, puis candidate SC2-ANTERIOR-AUSTRIA non commencée. Blocage Innviertel inchangé."
    state['events'].append(dict(id='SERG-RM-0013',date='2026-10-19',kind='SCOPED_IMPLEMENTATION',scope_version=state['scope_version'],source=p+'AUTHORIZATION.md',
        changes=[dict(task_id=TASK,before='NOT_STARTED',after=t['status'])],before_percent='33.19',after_percent='33.19',before_weight=78,after_weight=78,total_weight=235,
        evidence=[p+n for n in ['REPORT.md','SOURCES.md','SECTOR_AUDIT.md','BOUNDARY_AUDIT.json','IMPLEMENTATION.json','MARITIME_CLEANUP.json','VALIDATION.json','TESTS.json','SCOPED_TESTS.json','PLAYER_TEST_PROTOCOL.md']],note=note))
    assert state['events'][:-1]==original['events']
    assert [x for x in state['tasks'] if x['id']!=TASK]==[x for x in original['tasks'] if x['id']!=TASK]
    assert not rm.structural_errors(state)
    p_after=rm.progress(state)
    assert (p_after['earned_weight'],p_after['total_weight'],p_after['percent'],p_after['next_task'])==(78,235,'33.19',TASK)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state);rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS'
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged_since_acknowledgment=True,all_12_previous_events_unchanged=True,
        scope_version_unchanged=True,qualified_tasks=23,earned_weight=78,total_weight=235,percent='33.19',new_runtime_receipts=0,next_candidate=next_candidate,next_candidate_started=False))
    print('Tracking PASS, 78/235=33.19%, user validation pending; next candidate not started',flush=True)


if __name__ == '__main__':
    {'inventory': inventory, 'install': install, 'cleanup_maritime':cleanup_maritime, 'validate': validate, 'tests': tests, 'tracking':tracking}[sys.argv[1]]()
