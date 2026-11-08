"""Scoped Upper Guelders political B core; never writes Git or vanilla."""
import collections
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import serg_prussian_west as prior
from map2l_belgium import packed, components, allocate
from map2l_franconia import inside

ROOT, CANON = prior.ROOT, prior.CANON
OUT = CANON / 'CLEVE_GUELDRE_MARK_2026_11_05'
SID, PARENT, CHILD = 'STATE_GELRE', 'x0000DF', 'xEEC600'


def sha(path):
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def geometry():
    assert prior.runtime() == load('BASELINE.json')['runtime']
    a = packed(OUT / 'provinces_before.png')
    t = load('TRACING.json')
    yy, xx = np.mgrid[800:827, 4215:4248]
    local = inside(np.c_[(xx + .5).ravel(), (yy + .5).ravel()], np.array(t['native_outline'])).reshape(xx.shape)
    # The outline is already an inward political core. A further whole-cell
    # erosion would omit Venray and leave only 33 cells; it is not installed.
    local &= a[800:827, 4215:4248] == int(PARENT[1:], 16)
    moved = np.zeros(a.shape, dtype=bool)
    moved[800:827, 4215:4248] = local
    assert moved.sum() == 53 and not (a == int(CHILD[1:], 16)).any()
    core = moved.copy()
    # The B53-only draft would leave a northern BEO pocket. This pocket is
    # reviewed separately, not reassigned merely because it is disconnected:
    # Bohn's Cleves/Guelders sheet, Nijmegen's Middelaar archival authority,
    # and Maastricht's chronology agree on Prussian rule here before 1776.
    northern = np.zeros(a.shape, dtype=bool)
    for part in components((a == int(PARENT[1:], 16)) & ~core):
        if len(part) == 19 and max(y for y,x in part) == 812:
            for y,x in part:
                northern[y,x] = True
    assert northern.sum() == 19 and not (core & northern).any()
    moved |= northern
    t.update(margin_native_cells=0, margin_method='Source outline already inset; northern Cleves/Guelders B19 separately reviewed', ownership_cells=72)
    ys, xs = np.where(moved)
    t['cells'] = [[int(x), int(y)] for y, x in zip(ys, xs)]
    dump('TRACING.json', t)
    assignments = []
    for rgb, tag, mask in [(PARENT, 'BEO', (a == int(PARENT[1:], 16)) & ~moved), (CHILD, 'PRU', moved)]:
        ys, xs = np.where(mask)
        assignments.append(dict(rgb=rgb, parent_rgb=PARENT, state=SID, previous_owner='BEO', owner=tag,
            pixels=int(mask.sum()), cells=[[int(x), int(y)] for y, x in zip(ys, xs)],
            components_4=sorted([len(c) for c in components(mask)], reverse=True)))
    z = a.copy()
    z[moved] = int(CHILD[1:], 16)
    Image.fromarray(np.stack(((z >> 16) & 255, (z >> 8) & 255, z & 255), axis=-1).astype(np.uint8)).save(OUT / 'provinces_candidate.png')
    dump('GEOMETRY.json', dict(classification='B_POLITICAL_GENERALISATION', historical_cadastral_precision=False,
        parents=[PARENT], new_provinces=[dict(rgb=CHILD, parent_rgb=PARENT)], assignments=assignments,
        ownership_cells=72, changed_pixels=72, hub_rebindings=[], candidate_sha256=sha(OUT / 'provinces_candidate.png'),
        sub_lots=[dict(id=name, pixels=int(mask.sum()), cells=[[int(x),int(y)] for y,x in zip(*np.where(mask))], status='PREPARED_NOT_INSTALLED') for name,mask in [('PW-GUELDRE-B53',core),('PW-CLEVE-GUELDRE-NORTH-B19',northern)]],
        excluded=[v for v in t['excluded'] if v!='Afferden northern finger'], all_other_parent_pixels_immutable=True))
    render()
    print('72 cells BEO -> PRU (53+19); 165 BEO cells retained')


def render():
    b, g = load('BASELINE.json'), load('GEOMETRY.json')
    owners = {r['key'][0]: r['key'][2] for r in b['inventory']['owners']}
    colors = {'PRU': (112, 158, 206), 'BEO': (220, 175, 112), 'NET': (225, 199, 75), 'KPF': (189, 160, 208), 'KCL': (150, 195, 147), 'LGE': (205, 130, 130)}
    box, scale = (4218, 800, 4248, 833), 18
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    panels = []
    for title, path, own in [('AVANT', OUT/'provinces_before.png', owners), ('APRES - B POLITIQUE', OUT/'provinces_candidate.png', owners | {CHILD: 'PRU'})]:
        a = packed(path)[box[1]:box[3], box[0]:box[2]]
        rgb = np.full((*a.shape, 3), 225, dtype=np.uint8)
        for value in np.unique(a):
            rgb[a == value] = colors.get(own.get('x' + format(int(value), '06X')), (225, 225, 225))
        im = Image.new('RGB', (540, 664), 'white')
        im.paste(Image.fromarray(rgb).resize((540, 594), Image.Resampling.NEAREST), (0, 35))
        d = ImageDraw.Draw(im)
        d.text((8, 8), title, fill='black', font=font)
        d.text((8, 638), 'Bleu PRU ; ocre BEO ; jaune NET', fill='black', font=font)
        for r in load('TRACING.json')['readings']:
            if r['name'] not in {'Venray', 'Horst', 'Straelen', 'Venlo', 'Roermond'}:
                continue
            x, y = r['reference_native']; x = (x-box[0])*scale; y = (y-box[1])*scale+35
            d.ellipse((x-2, y-2, x+2, y+2), fill='black')
            d.text((x+3, y+3), r['name'], font=font, fill='black', stroke_width=1, stroke_fill='white')
        panels.append(im)
    image = Image.new('RGB', (1080, 664), 'white')
    image.paste(panels[0]); image.paste(panels[1], (540, 0))
    image.save(OUT / ('BEFORE_AFTER.png' if (OUT/'INSTALLATION.json').exists() else 'BEFORE_CANDIDATE.png'))


def prepare():
    import validate_diplomacy_ottoman_1776 as cw
    from map_1776_audit import values
    from map2a_patch import edits
    from map2b_patch import state, region, append
    from map2l_registry import active_registry_path
    import map2m_r9 as locators
    b, g = load('BASELINE.json'), load('GEOMETRY.json')
    assert prior.runtime() == b['runtime']
    before, files, allocations = {}, {}, []
    def read(rel):
        raw = (ROOT/rel).read_bytes().decode('utf-8')
        if rel in b['runtime']:
            assert sha(ROOT/rel) == b['runtime'][rel], rel
        before[rel] = raw
        return raw.lstrip('\ufeff')
    rel = 'common/history/states/00_states.txt'; raw = read(rel); n = state(raw, SID)
    assert not any(cw.scalar(z.one('country')) == 'c:PRU' for z in n.children('create_state'))
    source = next(z for z in n.children('create_state') if cw.scalar(z.one('country')) == 'c:BEO')
    assert values(source, 'owned_provinces') == [PARENT]
    files[rel] = edits(raw, [(n.end-1, n.end-1, '\n\t\t# Prussian Upper Guelders political B core; see CLEVE_GUELDRE_MARK_2026_11_05.\n\t\tcreate_state = { country = c:PRU owned_provinces = { '+CHILD+' } }\n\t')])
    rel = 'map_data/state_regions/00_west_europe.txt'; raw = read(rel)
    n = next(z for z in cw.parse(raw) if z.key == SID); field = n.children('provinces')[0]
    ops = [(field.end-1, field.end-1, ' "'+CHILD+'" ')]
    a, z = packed(OUT/'provinces_before.png'), packed(OUT/'provinces_candidate.png')
    for kind in ['city', 'farm', 'mine', 'wood', 'port']:
        if not n.children(kind) or cw.scalar(n.one(kind)) != PARENT:
            continue
        loc = next(r for r in locators.locators(a) if r['Kind'] == kind and r['ID'] == int(n.one('id')))
        x, y = loc['X'], loc['Y']; actual = 'x'+format(int(z[int(y), int(x)]), '06X')
        assert int(a[int(y), int(x)]) == int(PARENT[1:], 16)
        if actual != PARENT:
            f = n.children(kind)[0]; ops.append((f.start, f.end, kind+' = "'+actual+'"'))
            g['hub_rebindings'].append(dict(state=SID, field=kind, before=PARENT, after=actual, point=[x, y], locator_moved=False))
    if PARENT in values(n, 'prime_land'):
        f = n.children('prime_land')[0]; ops.append((f.end-1, f.end-1, ' "'+CHILD+'" '))
    files[rel] = edits(raw, ops)
    weights = {'BEO': 165, 'PRU': 72}
    for rel in b['originals']:
        if '/pops/' not in rel:
            continue
        original = read(rel)
        try:
            n = region(original, SID, 'BEO')
        except StopIteration:
            continue
        ops, pieces = [], []
        for pop in n.children('create_pop'):
            size = pop.children('size')[0]; count = int(size.value); amounts = allocate(count, weights)
            ops.append((size.start, size.end, 'size = '+str(amounts['BEO'])))
            if amounts['PRU']:
                pieces.append(edits(original[pop.start:pop.end], [(size.start-pop.start, size.end-pop.start, 'size = '+str(amounts['PRU']))]))
            allocations.append(dict(file=rel, state=SID, source='BEO', target='PRU', profile=[pop.one('culture'), pop.one('religion', 'DEFAULT')], before=count, after=amounts))
        updated = append(edits(original, ops), SID, 'PRU', '\n'.join(pieces))
        files[rel] = updated
    assert sum(r['before'] for r in allocations) == 34721
    assert not [r for r in b['inventory']['buildings'] if r['key'][:2] == [SID, 'BEO']]
    rel = 'map_data/province_terrains.txt'; raw = read(rel)
    terrains = {k.upper(): v for k, v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"', raw)}
    files[rel] = raw+'\n'+CHILD+' = "'+terrains[PARENT.upper()]+'"\n'
    rel = active_registry_path().relative_to(ROOT).as_posix(); ledger = json.loads(read(rel))
    previous = [r for r in ledger if r['state'] == SID]
    assert len(ledger) == 598 and any(r['rgb'] == PARENT and r['beneficiary'] == 'BEO' for r in previous)
    added = [dict(rgb=CHILD, state=SID, beneficiary='PRU', basis='Upper Guelders partition 1713/1716, Maastricht and Bohn 1793 corroboration; CLEVE_GUELDRE_MARK_2026_11_05/REPORT.md; partial political B core')]
    files[rel] = json.dumps(sorted(ledger+added, key=lambda r: (r['rgb'], r['state'], r['beneficiary'])), ensure_ascii=False, indent=2)+'\n'
    dump('REGISTRY_MIGRATION.json', dict(replaced_regions=[SID], previous=previous, updated=previous+added,
        new_members=[], free_cities=[], country_additions={}, new_provinces=g['new_provinces'],
        region_reference_changes=g['hub_rebindings'], extent_added_cells=[], extent_removed_cells=[]))
    rel = 'tools/map2l_registry.py'; raw = read(rel); anchor = '    return result\n\ndef provincial_membership_overrides'
    if '\r\n' in raw:
        anchor = anchor.replace('\n', '\r\n')
    assert raw.count(anchor) == 1
    guard = """    gueldre=ROOT/'docs/reports/map/SERG_CLOSURE/CLEVE_GUELDRE_MARK_2026_11_05'
    if (gueldre/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((gueldre/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((gueldre/'GEOMETRY.json').read_text(encoding='utf8'))
        assert magdeburg in result
        assert m['replaced_regions']==['STATE_GELRE']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==72
        assert [(z['id'],z['pixels']) for z in g['sub_lots']]==[('PW-GUELDRE-B53',53),('PW-CLEVE-GUELDRE-NORTH-B19',19)]
        assert g['parents']==['x0000DF'] and g['new_provinces']==[{'rgb':'xEEC600','parent_rgb':'x0000DF'}]
        assert {(z['owner'],z['previous_owner'],z['state']) for z in g['assignments']}=={('BEO','BEO','STATE_GELRE'),('PRU','BEO','STATE_GELRE')}
        old={z['rgb']:z for z in m['previous']};new={z['rgb']:z for z in m['updated']}
        assert all(new[k]==v for k,v in old.items()) and len(new)==len(old)+1
        assert new['xEEC600']['beneficiary']=='PRU'
        result.append(gueldre)
"""
    if '\r\n' in raw:
        guard = guard.replace('\n', '\r\n')
    files[rel] = raw.replace(anchor, guard+anchor)
    for rel, text in list(files.items()):
        old = before[rel]
        if old.startswith('\ufeff'):
            text = '\ufeff'+text.lstrip('\ufeff')
        if '\r\n' in old and old.count('\n') == old.count('\r\n'):
            text = text.replace('\r\n', '\n').replace('\n', '\r\n')
        oldlines, newlines, parts = old.splitlines(True), text.splitlines(True), []
        for op, i, j, k, l in difflib.SequenceMatcher(None, oldlines, newlines, autojunk=False).get_opcodes():
            lines = newlines[k:l]
            if op != 'equal':
                lines = [line if line.strip() else ('\r\n' if line.endswith('\r\n') else '\n') for line in lines]
            parts.extend(lines)
        files[rel] = ''.join(parts)
        if rel.endswith('.txt'):
            cw.parse(files[rel].lstrip('\ufeff'))
    dump('GEOMETRY.json', g); dump('TEXT_BEFORE.json', before); dump('EXPECTED_TEXT.json', files)
    dump('PLAN.json', dict(files=sorted(files), population_allocations=allocations, weights=weights,
        moved_population=sum(r['after']['PRU'] for r in allocations),
        population_method='Exact-integer technical redistribution of existing BEO/Gelre profiles; not a historical census',
        source_has_no_buildings=True, buildings_units_technologies_unchanged=True, runtime_installed=False))
    print('Prepared', len(files), 'text files; moved population', sum(r['after']['PRU'] for r in allocations), 'hubs', g['hub_rebindings'])


def compile_prepare():
    import serg_prussia_v1 as compiler
    compiler.OUT = OUT; compiler.compile_prepare()


def install():
    import serg_prussia_v1 as installer
    assert prior.runtime() == load('BASELINE.json')['runtime'], 'Reconcile functional concurrency before installation'
    installer.OUT = OUT; installer.install()


def verify():
    import importlib
    import validate_map2a as qa
    import map2l_registry as reg
    import validate_diplomacy_ottoman_1776 as cw
    # Installation changes this module; a combined prepare/install/verify
    # process must inspect the installed chain rather than its imported draft.
    reg = importlib.reload(reg)
    b, g = load('BASELINE.json'), load('GEOMETRY.json')
    inv = qa.inventory(); dump('INVENTORY_AFTER.json', inv)
    a, z = packed(OUT/'provinces_before.png'), packed(ROOT/'map_data/provinces.png')
    expected = load('EXPECTED_TEXT.json'); changed = {r['file'] for r in load('INSTALLATION.json')['changes']}
    checks = []
    def ck(name, value):
        checks.append(dict(name=name, status='PASS' if value else 'FAIL'))
    ck('prepared_text_installed_exactly', all((ROOT/p).read_bytes().decode('utf-8') == raw for p, raw in expected.items()))
    now = prior.runtime()
    ck('all_other_functional_files_preserved', {p:h for p,h in now.items() if p not in changed} == {p:h for p,h in b['runtime'].items() if p not in changed})
    ck('bitmap_exactly_reviewed', sha(ROOT/'map_data/provinces.png') == g['candidate_sha256'])
    ck('exactly_72_changed_cells', int((a != z).sum()) == 72)
    wanted = {tuple(c) for lot in g['sub_lots'] for c in lot['cells']}; ys, xs = np.where(a != z)
    ck('only_documented_cells_changed', set(zip(xs.tolist(), ys.tolist())) == wanted)
    ck('retained_BEO_parent_connected', len(components(z == int(PARENT[1:],16))) == 1)
    ck('new_PRU_core_connected', len(components(z == int(CHILD[1:],16))) == 1)
    ck('all_other_parents_pixels_preserved', np.array_equal(a[a != int(PARENT[1:],16)], z[a != int(PARENT[1:],16)]))
    for r in g['assignments']:
        ys, xs = np.where(z == int(r['rgb'][1:], 16))
        ck('exact_geometry_'+r['rgb'], set(zip(xs.tolist(), ys.tolist())) == {tuple(c) for c in r['cells']})
    wantedowners = qa.counter(b['inventory']['owners']).copy(); wantedowners[CHILD, SID, 'PRU'] += 1
    ck('worldwide_ownership_exact_delta', qa.counter(inv['owners']) == wantedowners)
    for field in ['pops', 'resolved_demographics', 'buildings', 'building_levels_written', 'units', 'countries']:
        ck('inventory_'+field+'_preserved', inv[field] == b['inventory'][field])
    ck('states_only_PRU_GELRE_added', sorted(inv['states']) == sorted(b['inventory']['states'] + [[SID, 'PRU']]))
    ck('state_types_only_incorporated_PRU_GELRE_added', inv['state_types'] == b['inventory']['state_types'] | {SID+'|PRU':'incorporated_default'})
    ck('inherited_reference_errors_unchanged', inv['errors'] == b['inventory']['errors'])
    ck('inherited_duplicate_debt_unchanged', inv['duplicates'] == b['inventory']['duplicates'])
    ck('new_province_one_owner', [r for r in inv['owners'] if r['key'][0] == CHILD] == [dict(key=[CHILD, SID, 'PRU'], count=1)])
    ck('global_population_preserved', sum(r['count'] for r in inv['pops']) == sum(r['count'] for r in b['inventory']['pops']))
    wantedpop = qa.counter(b['inventory']['regional_pop']).copy()
    for r in load('PLAN.json')['population_allocations']:
        culture, religion = r['profile']; religion = 'DEFAULT:'+culture if religion == 'DEFAULT' else religion
        culture, religion = culture.strip('"'), religion.strip('"')
        amount = r['after']['PRU']; wantedpop[SID,'BEO',culture,religion] -= amount; wantedpop[SID,'PRU',culture,religion] += amount
    ck('regional_population_exact_redistribution', +qa.counter(inv['regional_pop']) == +wantedpop)
    old = json.loads(load('TEXT_BEFORE.json')[reg.active_registry_path().relative_to(ROOT).as_posix()])
    ledger = json.loads(reg.active_registry_path().read_text(encoding='utf-8-sig')); rows = {r['rgb']:r for r in ledger}
    ck('registry_598_to_599_unique', len(old) == 598 and len(ledger) == len(rows) == 599)
    ck('all_previous_titles_preserved', all(rows[r['rgb']] == r for r in old))
    ck('only_new_title_PRU', rows[CHILD]['beneficiary'] == 'PRU')
    ck('imperial_physical_extent_preserved', np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in old]), np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    ck('explicit_migration_chain_appended', reg.approved_lot_dirs()[-1] == OUT)
    from map2k_patch import ELECTORS
    ck('nine_electors_preserved', len(ELECTORS) == 9)
    ck('all_physical_locators_preserved', not any('/map_object_data/' in p for p in changed))
    ck('no_building_country_military_technology_changes', not any(any(s in p for s in ['/buildings/','/countries/','/military','/technology/','/production_methods/']) for p in changed))
    terrain = dict((k.upper(),v) for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')))
    ck('child_terrain_inherited', terrain[CHILD.upper()] == terrain[PARENT.upper()])
    for r in g['hub_rebindings']:
        x,y = r['point']; ck('hub_reference_'+r['field'], int(z[int(y),int(x)]) == int(r['after'][1:],16) and not r['locator_moved'])
    protected = dict(b['protected'])
    for p in OUT.glob('PROTECT_*.json'):
        protected.update(load(p.name))
    ck('all_prior_evidence_and_approvals_preserved', all((ROOT/p).is_file() and sha(ROOT/p) == h for p,h in protected.items()))
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        value = subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
        ck('git_'+name+'_preserved', value == b['git'][name])
    ck('git_index_preserved', sha(Path(b['git']['git_dir'])/'index') == b['git']['index_sha256'])
    for rel,raw in expected.items():
        if rel.endswith('.txt'):
            cw.parse(raw.lstrip('\ufeff'))
    ck('changed_scripts_parse', True)
    result = dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL', checks=checks,
        passed=sum(c['status']=='PASS' for c in checks), total=len(checks), inherited_errors=inv['errors'],
        inherited_duplicates=inv['duplicates'], moved_population=load('PLAN.json')['moved_population'],
        global_written_population=sum(r['count'] for r in inv['pops']), engine_test=False, human_attestation=None)
    dump('VALIDATION.json', result)
    print('Validation',result['passed'],'/',result['total'],[c for c in checks if c['status']!='PASS'])
    assert result['status'] == 'PASS'


if __name__ == '__main__':
    {'geometry':geometry,'prepare':prepare,'compile':compile_prepare,'install':install,'render':render,'verify':verify}[sys.argv[1]]()
