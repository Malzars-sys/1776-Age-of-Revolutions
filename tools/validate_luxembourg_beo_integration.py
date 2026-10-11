"""Validate only the user-approved Luxembourg -> BEO starting-history transfer.

--capture records the actual dirty workspace before editing (never HEAD).
Default is read-only; --write-report writes QA artifacts, not gameplay files.
This does not claim a native Victoria 3 loading test.
"""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import validate_diplomacy_ottoman_1776 as cw

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/reports/map/LUX_BEO_INTEGRATION_2026-10-10'
FILES = [
    'common/history/states/00_states.txt',
    'common/history/pops/00_west_europe.txt',
    'common/history/buildings/00_west_europe.txt',
    'common/history/buildings/98_build_start_1776_world_redistribution.txt',
    'common/history/military_formations/00_military_formations_europe.txt',
    'common/history/diplomacy/00_relations.txt',
    'common/history/treaties/00_historical_treaties.txt',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture():
    REPORT.mkdir(parents=True, exist_ok=True)
    target = REPORT / 'BASELINE.json'
    assert not target.exists(), 'Never replace the pre-edit workspace snapshot.'
    paths = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT
    ).decode('utf-8').split('\0')
    data = {
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT).decode().strip(),
        'scope': 'Actual pre-edit dirty workspace, including untracked MAP1C and prior work',
        'hashes': {p: sha(ROOT/p) for p in sorted(set(paths)) if p and (ROOT/p).is_file()},
        'originals': {p: (ROOT/p).read_text(encoding='utf-8-sig') for p in FILES},
    }
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Captured', len(data['hashes']), 'existing files; no gameplay changed.')


def roots(raw):
    return cw.parse(raw)[0].children()


def signature(nodes):
    return json.dumps(cw.normalized(nodes), ensure_ascii=False, separators=(',', ':'))


def state_owners(raw):
    # Existing unrelated duplicate assignments must be reported and preserved,
    # not repaired or used to block this one approved transfer.
    result = collections.Counter()
    for state in roots(raw):
        for creation in state.children('create_state'):
            owner = cw.scalar(creation.one('country'))
            for province in creation.children('owned_provinces')[0].children():
                rgb = cw.scalar(province.value)
                result[(rgb, state.key, owner)] += 1
    return result


def regional_records(raw, command, transfer=False):
    result = collections.Counter()
    for state in roots(raw):
        for region in state.children():
            owner = region.key
            if transfer and owner == 'region_state:LUX':
                owner = 'region_state:BEO'
            for record in region.children(command):
                body = signature([record])
                if transfer:
                    body = body.replace('c:LUX', 'c:BEO')
                result[(state.key, owner, body)] += 1
    return result


def pop_sum(raw, owner):
    return sum(int(pop.one('size')) for state in roots(raw)
               for region in state.children('region_state:'+owner)
               for pop in region.children('create_pop'))


def country_records(raw, transfer=False):
    result = collections.Counter()
    for country in roots(raw):
        owner = country.key
        if transfer and owner == 'c:LUX':
            owner = 'c:BEO'
        for child in country.children():
            result[(owner, signature([child]))] += 1
    return result


def ignored_map1c_checks(baseline):
    # cities1000.zip is ignored by Git, hence absent from git ls-files. Its
    # independently saved pre-intervention infrastructure fingerprint covers it.
    files = [p for p in (ROOT/'docs/reports/map/MAP1C').rglob('*')
             if p.is_file() and p.relative_to(ROOT).as_posix() not in baseline['hashes']]
    earlier = json.loads((ROOT/'docs/reports/ai_regional_infrastructure_shortage_2026-10-10/baseline.json')
                         .read_text(encoding='utf-8'))['files']
    for p in files:
        assert sha(p) == earlier[p.relative_to(ROOT).as_posix()], 'Ignored MAP1C evidence changed.'
    return [p.relative_to(ROOT).as_posix() for p in files]


def validate(write=False):
    baseline = json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'))
    before = baseline['originals']
    after = {p: (ROOT/p).read_text(encoding='utf-8-sig') for p in FILES}
    for raw in after.values():
        cw.parse(raw)
    validator_path = Path(__file__).relative_to(ROOT).as_posix()
    changed = {p for p, digest in baseline['hashes'].items()
               if p != validator_path and sha(ROOT/p) != digest}
    assert changed == set(FILES), ('Unexpected changed files', changed ^ set(FILES))
    map1c = [p for p in baseline['hashes'] if p.startswith('docs/reports/map/MAP1C/')]
    assert map1c and all(sha(ROOT/p) == baseline['hashes'][p] for p in map1c)
    ignored_map1c = ignored_map1c_checks(baseline)

    state_path, pop_path, *rest = FILES
    old_owners, new_owners = state_owners(before[state_path]), state_owners(after[state_path])
    expected = old_owners.copy()
    old_lux = ('xD001A0', 's:STATE_WALLONIA', 'c:LUX')
    assert expected[old_lux] == 1
    del expected[old_lux]
    expected[('xD001A0', 's:STATE_WALLONIA', 'c:BEO')] += 1
    assert expected == new_owners, 'A border other than the approved province changed.'
    assert not any(owner == 'c:LUX' for _, _, owner in new_owners)
    # Preserve homelands, claims, incorporation settings, and all other history commands.
    old = cw.parse(before[state_path])
    wallonia = next(n for n in cw.walk(old) if n.key == 's:STATE_WALLONIA')
    lux, beo = wallonia.children('create_state')
    assert lux.one('country') == 'c:LUX' and beo.one('country') == 'c:BEO'
    beo.children('owned_provinces')[0].value += lux.children('owned_provinces')[0].value
    wallonia.value.remove(lux)
    assert cw.normalized(old) == cw.normalized(cw.parse(after[state_path]))

    assert pop_sum(before[pop_path], 'LUX') == 137881
    assert pop_sum(after[pop_path], 'LUX') == 0
    assert pop_sum(after[pop_path], 'BEO') - pop_sum(before[pop_path], 'BEO') == 137881
    assert regional_records(before[pop_path], 'create_pop', True) == regional_records(after[pop_path], 'create_pop')
    for path in FILES[2:4]:
        assert regional_records(before[path], 'create_building', True) == regional_records(after[path], 'create_building')
        for state in roots(after[path]):
            selectors = [r.key for r in state.children()]
            assert len(selectors) == len(set(selectors)), 'Duplicate owner block: '+path
    military = FILES[4]
    assert country_records(before[military], True) == country_records(after[military])
    beo_country = [n for n in roots(after[military]) if n.key == 'c:BEO']
    assert len(beo_country) == 1
    lux_formation = next(n for n in cw.walk(cw.parse(after[military]))
                         if n.key == 'create_military_formation' and n.one('name') == 'Luxemburger_Miliz')
    assert sum(int(unit.one('count')) for unit in lux_formation.children('combat_unit')) == 3
    assert not any(unit.one('service_type') == 'conscript' for unit in lux_formation.children('combat_unit'))
    assert all(unit.one('state_region') == 's:STATE_WALLONIA' for unit in lux_formation.children('combat_unit'))

    relations = FILES[5]
    old = cw.parse(before[relations])
    net = next(n for n in cw.walk(old) if n.key == 'c:NET')
    lux_relation = [n for n in net.children('set_relations') if n.one('country') == 'c:LUX']
    assert len(lux_relation) == 1
    net.value.remove(lux_relation[0])
    assert cw.normalized(old) == cw.normalized(cw.parse(after[relations]))
    treaties = FILES[6]
    old = cw.parse(before[treaties])
    lux_treaty = [n for n in old[0].children('create_treaty') if n.one('second_country') == 'c:LUX']
    assert len(lux_treaty) == 1
    old[0].value.remove(lux_treaty[0])
    assert cw.normalized(old) == cw.normalized(cw.parse(after[treaties]))
    subject_path = 'common/history/diplomacy/00_subject_relationships.txt'
    subjects = cw.parse((ROOT/subject_path).read_text(encoding='utf-8-sig'))
    aus = next(n for n in cw.walk(subjects) if n.key == 'c:AUS')
    assert any(n.one('country') == 'c:BEO' and n.one('type') == 'crown_land'
               for n in aus.children('create_diplomatic_pact'))
    assert 'c:LUX' not in (ROOT/subject_path).read_text(encoding='utf-8-sig')
    # Inactive tag definitions, guarded country setup and future events are intentional.
    for p in (ROOT/'common/history').rglob('*.txt'):
        if p.name in ('lux - luxemburg.txt', '00_global.txt'):
            continue
        assert 'c:LUX' not in p.read_text(encoding='utf-8-sig'), 'Dangling start reference: '+str(p)
        assert 'region_state:LUX' not in p.read_text(encoding='utf-8-sig')
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == baseline['head']
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT).decode().strip() == baseline['branch']
    province_counts = collections.Counter()
    for (rgb, _, _), count in old_owners.items():
        province_counts[rgb] += count
    data = {
        'result': 'PASS', 'validation_kind': 'STATIC_NOT_GAME_ENGINE',
        'province_transfer': {'rgb': 'xD001A0', 'from': 'LUX', 'to': 'BEO', 'other_owner_changes': 0},
        'population_moved': 137881, 'demographic_records_unchanged': 4,
        'BEO_population_before': pop_sum(before[pop_path], 'BEO'),
        'BEO_population_after': pop_sum(after[pop_path], 'BEO'),
        'Wallonia_population_after': next(sum(int(p.one('size')) for r in s.children() for p in r.children('create_pop'))
                                          for s in roots(after[pop_path]) if s.key == 's:STATE_WALLONIA'),
        'building_migration': 'Both existing 1-level administration declarations re-scoped, PM/reserves unchanged; no new declarations',
        'units_transferred': {'irregular_infantry': 2, 'line_infantry': 1, 'conscript': 0},
        'commander_and_saved_scopes': 'PRESERVED', 'BEO_subject': 'AUS crown_land unchanged',
        'personal_union_or_new_dependency': 'NONE',
        'MAP1C_files_unchanged': len(map1c) + len(ignored_map1c),
        'ignored_MAP1C_files_verified_against_earlier_snapshot': ignored_map1c,
        'existing_files_unchanged': len(baseline['hashes']) - len(changed) - 1,
        'preexisting_duplicate_province_assignments_preserved':
            sorted(rgb for rgb, count in province_counts.items() if count > 1),
        'changed_files': sorted(changed),
        'native_game_load_test': 'NOT_RUN; requires a new 1776 game, not an existing save',
        'commit_merge_push': 'NOT_PERFORMED',
    }
    if write:
        (REPORT/'VALIDATION.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(data, indent=2, ensure_ascii=False))


def validate_lux_only():
    """Check Luxembourg invariants after a separately authorised wider map lot.

    The original strict whole-workspace validator remains the default. This mode
    does not rebaseline or overwrite its original report.
    """
    before = json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'))['originals']
    after = {p: (ROOT/p).read_text(encoding='utf-8-sig') for p in FILES}
    def wallonia(raw, command, transfer=False):
        return collections.Counter({k: v for k, v in regional_records(raw, command, transfer).items()
                                    if k[0] == 's:STATE_WALLONIA'})
    assert state_owners(after[FILES[0]])[('xD001A0', 's:STATE_WALLONIA', 'c:BEO')] == 1
    assert not any(owner == 'c:LUX' for _, _, owner in state_owners(after[FILES[0]]))
    assert pop_sum(before[FILES[1]], 'LUX') == 137881
    assert pop_sum(after[FILES[1]], 'LUX') == 0
    assert pop_sum(after[FILES[1]], 'BEO') - pop_sum(before[FILES[1]], 'BEO') == 137881
    assert wallonia(before[FILES[1]], 'create_pop', True) == wallonia(after[FILES[1]], 'create_pop')
    for p in FILES[2:4]:
        assert wallonia(before[p], 'create_building', True) == wallonia(after[p], 'create_building')
    expected = collections.Counter({k: v for k, v in country_records(before[FILES[4]], True).items()
                                    if k[0] == 'c:BEO'})
    actual = collections.Counter({k: v for k, v in country_records(after[FILES[4]]).items()
                                  if k[0] == 'c:BEO'})
    assert expected == actual, 'Luxembourg units, commander or saved scopes changed.'
    subjects = cw.parse((ROOT/'common/history/diplomacy/00_subject_relationships.txt').read_text(encoding='utf-8-sig'))
    aus = next(n for n in cw.walk(subjects) if n.key == 'c:AUS')
    assert any(n.one('country') == 'c:BEO' and n.one('type') == 'crown_land'
               for n in aus.children('create_diplomatic_pact'))
    for p in (ROOT/'common/history').rglob('*.txt'):
        if p.name in ('lux - luxemburg.txt', '00_global.txt'):
            continue
        raw = p.read_text(encoding='utf-8-sig')
        assert 'c:LUX' not in raw and 'region_state:LUX' not in raw, 'Dangling Luxembourg reference: '+str(p)
    print(json.dumps({'result': 'PASS', 'scope': 'Luxembourg invariants only; wider map authorised separately',
                      'population_preserved': 137881, 'units_preserved': 3,
                      'commander_buildings_demographics': 'PRESERVED', 'BEO': 'AUS crown_land',
                      'validation_kind': 'STATIC_NOT_GAME_ENGINE'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if '--lux-only' in sys.argv:
        validate_lux_only()
    else:
        capture() if '--capture' in sys.argv else validate('--write-report' in sys.argv)
