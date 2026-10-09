"""Prepare and verify the approved British agriculture/turnpike follow-up.

Records the immediately preceding revision, checks unrelated runtime files,
and edits final effective building placements rather than summing overlays.
Source changes are emitted as context-rich apply_patch patches, never written.
"""
from pathlib import Path
import argparse
import collections
import difflib
import hashlib
import json
import re
import build_start_1776_world_apply as world
import build_start_1776_research_input_pack as cat
import audit_british_colonial_start as naval

ROOT = world.ROOT
CACHE = ROOT / '.asset-cache/oct09_balance_revision'
RECORD = CACHE / 'gbr_agriculture_followup.json'
RYE = {'STATE_HOME_COUNTIES': 2, 'STATE_LANCASHIRE': 1,
       'STATE_YORKSHIRE': 2, 'STATE_MIDLANDS': 2,
       'STATE_EAST_ANGLIA': 2, 'STATE_LOWLANDS': 1}
REDUCTIONS = {('GBR', s, 'building_rye_farm'): n for s, n in RYE.items()}
REDUCTIONS.update({('GBR', 'STATE_LANCASHIRE', 'building_tooling_workshop'): 1,
                   ('GBR', 'STATE_MIDLANDS', 'building_tooling_workshop'): 2,
                   ('GBR', 'STATE_YORKSHIRE', 'building_iron_mine'): 1,
                   ('GBR', 'STATE_MIDLANDS', 'building_iron_mine'): 1,
                   ('GBR', 'STATE_LANCASHIRE', 'building_limestone_quarry'): 1,
                   ('GBR', 'STATE_MIDLANDS', 'building_limestone_quarry'): 1})
# Retain at least the previous direct road/canal output, except Home Counties:
# its screenshot shows only 106 used infrastructure; 16 turnpikes give 112
# before the population bonus, ports, traits and country/state modifiers.
ROADS = {('GBR', 'STATE_HOME_COUNTIES'): 16, ('GBR', 'STATE_HIGHLANDS'): 1,
         ('GBR', 'STATE_MIDLANDS'): 8, ('GBR', 'STATE_EAST_ANGLIA'): 5,
         ('GBR', 'STATE_JAMAICA'): 3, ('GBR', 'STATE_BAHAMAS'): 1,
         ('GBR', 'STATE_NEWFOUNDLAND'): 2, ('FRA', 'STATE_AQUITAINE'): 1,
         ('FRA', 'STATE_AUVERGNE_LIMOUSIN'): 1, ('FRA', 'STATE_LANGUEDOC'): 1}
COTTON = {'STATE_VIRGINIA': 3, 'STATE_NORTH_CAROLINA': 3}
POP_TARGETS = {'STATE_JAMAICA': 520000, 'STATE_NEWFOUNDLAND': 200000}
NEW_BUILDINGS = 'common/history/buildings/99b_1776_british_agricultural_balance.txt'
NEW_LITERACY = 'common/history/population/zz_1776_turnpike_qualifications.txt'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_buildings():
    text = '# Approved British agricultural balance, 9 October 2026.\nBUILDINGS = {\n'
    for owner, levels, building, pms in [
        ('GBR', RYE, 'building_livestock_ranch', ['pm_open_air_stockyards', 'pm_sheep_farms', 'pm_standard_fences', 'pm_unrefrigerated']),
        ('USA', COTTON, 'building_cotton_plantation', ['default_building_cotton_plantation', 'worker_exploitation_cotton', 'pm_road_carts'])]:
        for state, n in levels.items():
            text += f'''\ts:{state} = {{
\t\tregion_state:{owner} = {{
\t\t\tcreate_building = {{
\t\t\t\tbuilding = "{building}"
\t\t\t\tadd_ownership = {{
\t\t\t\t\tbuilding = {{
\t\t\t\t\t\ttype = "building_manor_house"
\t\t\t\t\t\tcountry = "c:{owner}"
\t\t\t\t\t\tregion = "{state}"
\t\t\t\t\t\tlevels = {n}
\t\t\t\t\t}}
\t\t\t\t}}
\t\t\t\treserves = 1
\t\t\t\tactivate_production_methods = {{ {' '.join('"'+p+'"' for p in pms)} }}
\t\t\t}}
\t\t}}
\t}}
'''
    return text + '}\n'


def literacy():
    text = '# Local qualification floor for the approved turnpike states.\n'
    text += '# Runs after native national starting literacy; never lowers it.\n'
    text += '# No changes to culture, religion, profession, or national education.\nPOPULATION = {\n'
    for owner in ['GBR', 'FRA']:
        states = [s for o, s in ROADS if o == owner]
        lines = '\n'.join('\t\t\t\t\t\tstate_region = s:' + s for s in states)
        text += f'''\tc:{owner} ?= {{
\t\tevery_scope_pop = {{
\t\t\tlimit = {{
\t\t\t\tliteracy_rate < 0.35
\t\t\t\tNOT = {{ is_pop_type = slaves }}
\t\t\t\tstate = {{
\t\t\t\t\tOR = {{
{lines}
\t\t\t\t\t}}
\t\t\t\t}}
\t\t\t}}
\t\t\tset_pop_literacy = {{ literacy_rate = 0.35 }}
\t\t}}
\t}}
'''
    return text + '}\n'


def prepare(revise=False):
    if RECORD.exists():
        assert revise, 'Preserve the approved preceding reference'
        prior = json.loads(RECORD.read_text(encoding='utf-8'))
        for rel, before in prior['before'].items():
            assert ((ROOT / rel).read_text(encoding='utf-8-sig') if (ROOT / rel).exists() else None) == before, 'Cannot revise a plan already applied'
        snapshot = RECORD.with_suffix('.initial.json')
        assert not snapshot.exists()
        snapshot.write_text(json.dumps(prior, indent=2), encoding='utf-8')
    raws, rows = world.all_placements(world.HISTORY)
    last = {p.key: p for p in rows}
    assert set(REDUCTIONS) <= set(last)
    edits = collections.defaultdict(list)
    report = []
    for p in rows:
        updated = p.text
        if last[p.key] is p and p.key in REDUCTIONS:
            n = p.level - REDUCTIONS[p.key]
            assert n >= 1
            updated = world.rescale_ownership(updated, n)
            report.append({'key': p.key, 'before': p.level, 'after': n})
        if p.owner == 'GBR' and p.building == 'building_rye_farm':
            assert 'pm_no_secondary' in p.pms
            updated = world.replace_active_pms(updated, ['pm_apple_orchards' if x == 'pm_no_secondary' else x for x in p.pms])
        if (p.owner, p.state) in ROADS and p.building == 'building_railway':
            assert 'pm_traditional_road_network' in p.pms
            updated = world.replace_active_pms(updated, ['pm_turnpike_road_network' if x == 'pm_traditional_road_network' else x for x in p.pms])
            if last[p.key] is p:
                n = ROADS[p.owner, p.state]
                assert n <= p.level
                updated = world.rescale_ownership(updated, n)
                report.append({'key': p.key, 'before': p.level, 'after': n})
        if updated != p.text:
            edits[p.path].append((p.start, p.end, updated))
    for state in RYE:
        assert ('GBR', state, 'building_livestock_ranch') not in last
    for state in COTTON:
        assert ('USA', state, 'building_cotton_plantation') not in last
    pop_report = []
    for path in (ROOT / 'common/history/pops').glob('*.txt'):
        raw = path.read_text(encoding='utf-8-sig')
        for state, a, b in world.block_spans(raw, r's:STATE_\w+', 1):
            state = state.split(':')[1]
            if state not in POP_TARGETS:
                continue
            block = raw[a:b]
            regions = world.block_spans(block, 'region_state:GBR', 1)
            assert len(regions) == 1
            _, x, y = regions[0]
            region = block[x:y]
            sizes = list(re.finditer(r'\bsize\s*=\s*(\d+)', region))
            original = [int(m[1]) for m in sizes]
            target = POP_TARGETS[state]
            exact = [v * target / sum(original) for v in original]
            allocation = [int(v) for v in exact]
            for i in sorted(range(len(exact)), key=lambda i: -(exact[i] - allocation[i]))[:target-sum(allocation)]:
                allocation[i] += 1
            for m, n in reversed(list(zip(sizes, allocation))):
                region = region[:m.start(1)] + str(n) + region[m.end(1):]
            updated = block[:x] + region + block[y:]
            raws[path] = raw
            edits[path].append((a, b, updated))
            pop_report.append({'state': state, 'before': sum(original), 'after': target})
    before = {}; expected = {}
    for path, replacements in edits.items():
        rel = path.relative_to(ROOT).as_posix()
        before[rel] = raws[path]
        updated = raws[path]
        for a, b, replacement in sorted(replacements, reverse=True):
            updated = updated[:a] + replacement + updated[b:]
        expected[rel] = updated
    for rel, content in [(NEW_BUILDINGS, new_buildings()), (NEW_LITERACY, literacy())]:
        assert not (ROOT / rel).exists()
        before[rel] = None
        expected[rel] = content
    canal = 'common/production_methods/23_tech7a_wave_b_canals_production.txt'
    before[canal] = (ROOT / canal).read_text(encoding='utf-8-sig')
    expected[canal] = before[canal].replace('building_economy_of_scale_level_cap_add = 0.1', 'building_economy_of_scale_level_cap_add = 0.5').replace('building_economy_of_scale_level_cap_add = 0.05', 'building_economy_of_scale_level_cap_add = 0.1')
    protected = {p.relative_to(ROOT).as_posix(): digest(p) for folder in ['common', 'gfx', 'gui', 'localization'] for p in (ROOT / folder).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in expected}
    record = {'before': before, 'expected': expected, 'protected': protected,
              'levels': report, 'populations': pop_report, 'engine_tested': False}
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    emit_patch(record)


def emit_patch(record):
    before = record['before']; expected = record['expected']
    patch = '*** Begin Patch\n'
    for rel, content in expected.items():
        if before[rel] is None:
            patch += '*** Add File: ' + rel + '\n' + ''.join('+' + l + '\n' for l in content.splitlines())
        else:
            actual = (ROOT / rel).read_text(encoding='utf-8')
            desired = ('\ufeff' if actual.startswith('\ufeff') else '') + content
            patch += '*** Update File: ' + rel + '\n'
            for line in list(difflib.unified_diff(actual.splitlines(), desired.splitlines(), n=40))[2:]:
                patch += ('@@' if line.startswith('@@') else line.rstrip('\n')) + '\n'
    print(json.dumps({'patch': patch + '*** End Patch', 'levels': record['levels'], 'populations': record['populations']}))


def extend_final_requests():
    """Add subsequent, explicitly requested military/gate edits to this wave."""
    record = json.loads(RECORD.read_text(encoding='utf-8'))
    paths = ['common/history/military_formations/00_military_formations_europe.txt',
             'common/ship_types/00_ship_types.txt']
    patch_record = {'before': {}, 'expected': {}, 'levels': [], 'populations': []}
    for rel in paths:
        assert rel in record['protected'], 'Already extended or modified'
        assert digest(ROOT / rel) == record['protected'][rel]
        raw = (ROOT / rel).read_text(encoding='utf-8-sig')
        updated = raw
        if 'military_formations' in rel:
            countries = [(a, b) for name, a, b in naval.country_spans(raw) if name.split()[0] == 'c:GBR']
            assert len(countries) == 1
            a, b = countries[0]
            country = raw[a:b]
            blocks = [(x, y) for _, x, y in world.block_spans(country, 'create_military_formation', 1) if cat.scalar(country[x:y], 'name') == 'cleanup2d3b_gbr_land_4']
            assert len(blocks) == 1
            x, y = blocks[0]
            block = country[x:y]
            assert 'supply_hub' not in block
            new = block.replace('hq_region = sr:region_southern_europe', 'hq_region = sr:region_southern_europe\n\t\t\tsupply_hub = s:STATE_BALEARIC_ISLANDS', 1)
            updated = raw[:a+x] + new + raw[a+y:]
        else:
            edits = []
            for name, a, b in world.block_spans(raw, r'ship_type_\w+', 0):
                gate = {'ship_type_ship_of_the_line': ('standardized_naval_signals', 'marine_chronometry'),
                        'ship_type_frigate': ('marine_chronometry', 'scientific_naval_architecture')}.get(name)
                if gate:
                    block = raw[a:b]
                    old = 'unlocking_technologies = { ' + gate[0] + ' }'
                    new = 'unlocking_technologies = { ' + gate[1] + ' }'
                    assert block.count(old) == 1
                    edits.append((a, b, block.replace(old, new)))
            assert len(edits) == 2
            for a, b, text in sorted(edits, reverse=True):
                updated = updated[:a] + text + updated[b:]
        assert updated != raw
        record['before'][rel] = raw
        record['expected'][rel] = updated
        record['protected'].pop(rel)
        patch_record['before'][rel] = raw
        patch_record['expected'][rel] = updated
    RECORD.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
    emit_patch(patch_record)


def check(quiet=False):
    record = json.loads(RECORD.read_text(encoding='utf-8'))
    for rel, expected in record['expected'].items():
        assert (ROOT / rel).read_text(encoding='utf-8-sig') == expected, 'Unexpected edit ' + rel
        cat.brace_maps(cat.clean_comments(expected))
    for rel, sha in record['protected'].items():
        assert digest(ROOT / rel) == sha, 'Protected file changed ' + rel
    _, rows = world.all_placements(world.HISTORY)
    last = {p.key: p for p in rows}
    for item in record['levels']:
        assert last[tuple(item['key'])].level == item['after'], item
    for p in rows:
        if p.owner == 'GBR' and p.building == 'building_rye_farm':
            assert 'pm_apple_orchards' in p.pms
        if (p.owner, p.state) in ROADS and p.building == 'building_railway':
            assert 'pm_turnpike_road_network' in p.pms
    tech = naval.technology_sets()
    for owner, _ in ROADS:
        assert 'turnpike_road_networks' in tech[owner]
    assert 'selective_breeding' in tech['GBR']
    for state, n in RYE.items():
        p = last['GBR', state, 'building_livestock_ranch']
        assert p.level == n and 'pm_sheep_farms' in p.pms
    states = cat.effective_objects('map_data/state_regions', r'STATE_\w+')
    buildings = cat.effective_objects('common/buildings', r'\w+')
    groups = cat.effective_objects('common/production_method_groups', r'\w+')
    for p in rows:
        if p.path.name != Path(NEW_BUILDINGS).name:
            continue
        group_ids = cat.tokens_flat(cat.braced_tokens(buildings[p.building].text, 'production_method_groups'))
        members = [set(cat.tokens_flat(cat.braced_tokens(groups[g].text, 'production_methods'))) for g in group_ids]
        assert all(sum(pm in m for pm in p.pms) == 1 for m in members), ('Wrong PM selection', p.key)
        assert all(any(pm in m for m in members) for pm in p.pms), ('Invalid PM', p.key)
        assert p.building in states[p.state].text
    assert sum(RYE.values()) == 10 and sum(COTTON.values()) == 6
    assert sum(p.level for p in last.values() if p.owner == 'GBR' and p.building == 'building_rye_farm') == 48
    assert sum(v for (o, s, b), v in REDUCTIONS.items() if b == 'building_tooling_workshop') == 3
    assert sum(v for (o, s, b), v in REDUCTIONS.items() if b == 'building_iron_mine') == 2
    assert sum(v for (o, s, b), v in REDUCTIONS.items() if b == 'building_limestone_quarry') == 2
    for state, n in COTTON.items():
        assert last['USA', state, 'building_cotton_plantation'].level == n
        assert 'building_cotton_plantation' in states[state].text
    pops = cat.parse_populations()
    for state, target in POP_TARGETS.items():
        assert pops[state, 'GBR'] == target
    # Population changes preserve each original culture/religion block;
    # largest-remainder rounding changes each share by less than one person.
    for rel, before in record['before'].items():
        if '/pops/' not in rel:
            continue
        after = record['expected'][rel]
        for state, a, b in world.block_spans(before, r's:STATE_\w+', 1):
            name = state.split(':')[1]
            new = next(after[x:y] for key, x, y in world.block_spans(after, r's:STATE_\w+', 1) if key == state)
            old = before[a:b]
            if name not in POP_TARGETS:
                assert old == new, ('Unrelated population changed', name)
            else:
                assert re.sub(r'(\bsize\s*=\s*)\d+', r'\1N', old) == re.sub(r'(\bsize\s*=\s*)\d+', r'\1N', new)
                old_sizes = list(map(int, re.findall(r'\bsize\s*=\s*(\d+)', old)))
                new_sizes = list(map(int, re.findall(r'\bsize\s*=\s*(\d+)', new)))
                assert all(abs(n - o * sum(new_sizes) / sum(old_sizes)) < 1 for o, n in zip(old_sizes, new_sizes))
    pms = cat.effective_objects('common/production_methods', r'\w+')
    assert cat.scalar(pms['pm_industrial_canals'].text, 'building_economy_of_scale_level_cap_add') == '0.1'
    assert cat.scalar(pms['pm_engineered_canals'].text, 'building_economy_of_scale_level_cap_add') == '0.5'
    if 'common/ship_types/00_ship_types.txt' in record['expected']:
        ships = cat.effective_objects('common/ship_types', r'ship_type_\w+')
        for hull, gate in [('ship_type_ship_of_the_line', 'marine_chronometry'), ('ship_type_frigate', 'scientific_naval_architecture')]:
            assert cat.tokens_flat(cat.braced_tokens(ships[hull].text, 'unlocking_technologies')) == [gate]
        military = record['expected']['common/history/military_formations/00_military_formations_europe.txt']
        country = next(military[a:b] for name, a, b in naval.country_spans(military) if name.split()[0] == 'c:GBR')
        med = next(country[a:b] for _, a, b in world.block_spans(country, 'create_military_formation', 1) if cat.scalar(country[a:b], 'name') == 'cleanup2d3b_gbr_land_4')
        assert 'supply_hub = s:STATE_BALEARIC_ISLANDS' in med
        assert 'hq_region = sr:region_southern_europe' in med
        state_raw = (ROOT / 'common/history/states/00_states.txt').read_text(encoding='utf-8-sig')
        balearic = next(state_raw[a:b] for name, a, b in world.block_spans(state_raw, 's:STATE_BALEARIC_ISLANDS', 1))
        assert 'country = c:GBR' in balearic
    workforce = []
    for state in POP_TARGETS:
        jobs = collections.Counter()
        for p in last.values():
            if (p.owner, p.state) != ('GBR', state):
                continue
            for pm in p.pms:
                for job, n in re.findall(r'building_employment_(\w+)_add\s*=\s*(-?[\d.]+)', pms[pm].text):
                    jobs[job] += float(n) * p.level
        # Conservative 25% workforce approximation, with a 10% reserve for
        # ownership buildings, urbanization and employment initialization.
        assert pops[state, 'GBR'] * 0.25 >= sum(jobs.values()) * 1.10
        workforce.append({'state': state, 'pm_jobs': sum(jobs.values()), 'estimated_workers': pops[state, 'GBR'] * 0.25, 'jobs_by_type': dict(jobs)})
    result = {'status': 'PASS_GBR_AGRICULTURE_FOLLOWUP', 'levels': record['levels'], 'populations': record['populations'], 'workforce_estimates': workforce, 'engine_tested': False}
    (CACHE / 'agriculture_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    if not quiet:
        print(json.dumps(result))
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--revise-unapplied', action='store_true')
    parser.add_argument('--patch', action='store_true')
    parser.add_argument('--extend-final-requests', action='store_true')
    args = parser.parse_args()
    if args.prepare or args.revise_unapplied:
        prepare(revise=args.revise_unapplied)
    elif args.extend_final_requests:
        extend_final_requests()
    elif args.patch:
        emit_patch(json.loads(RECORD.read_text(encoding='utf-8')))
    else:
        check()
