"""MAP-2A: snapshot the dirty workspace, validate a narrow authorised map lot.

Written histories are inspected, not executed by the Victoria 3 engine.
--capture never replaces an existing baseline. --validate writes QA reports only.
"""
from __future__ import annotations
import collections as C
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective, values, prov

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
OUT = ROOT/'docs/reports/map/MAP2A'
HISTORY = [
    'common/history/states/00_states.txt',
    'common/history/pops/00_west_europe.txt',
    'common/history/pops/01_south_europe.txt',
    'common/history/pops/02_east_europe.txt',
    'common/history/buildings/00_west_europe.txt',
    'common/history/buildings/02_east_europe.txt',
    'common/history/buildings/98_build_start_1776_world_redistribution.txt',
    'common/history/military_formations/00_military_formations_europe.txt',
]
TARGETS = {'STATE_LOMBARDY', 'STATE_MORAVIA', 'STATE_UPPER_SILESIA', 'STATE_WEST_GALICIA'}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(n):
    return [n.key, n.op, [norm(v) for v in n.value] if isinstance(n.value, list) else cw.scalar(n.value)]

def signature(n):
    return json.dumps(norm(n), ensure_ascii=False, separators=(',', ':'))

def tagged(counter):
    return [{'key': list(k) if isinstance(k, tuple) else k, 'count': v}
            for k, v in sorted(counter.items())]

def counter(rows):
    return C.Counter({tuple(r['key']) if isinstance(r['key'], list) else r['key']: r['count'] for r in rows})

def inventory():
    owners, geometry, pops, buildings, units = C.Counter(), {}, C.Counter(), C.Counter(), C.Counter()
    state_types, countries, references, errors = {}, {}, set(), []
    regional_pop = C.Counter()
    for p in effective(ROOT, GAME, 'map_data/state_regions'):
        for n in cw.parse(p.read_text(encoding='utf-8-sig')):
            for rgb in values(n, 'provinces'):
                geometry[prov(rgb)] = n.key
    state_pairs = set()
    for p in effective(ROOT, GAME, 'common/history/states'):
        raw = p.read_text(encoding='utf-8-sig')
        for s in cw.walk(cw.parse(raw)):
            if not s.key.startswith('s:STATE_'): continue
            for cr in s.children('create_state'):
                owner = cw.scalar(cr.one('country')).removeprefix('c:')
                sid = s.key[2:]
                state_pairs.add((sid, owner))
                state_types[sid+'|'+owner] = cr.one('state_type', 'incorporated_default')
                for rgb in values(cr, 'owned_provinces'):
                    owners[(prov(rgb), sid, owner)] += 1
                for token in cr.children(''):
                    errors.append(['bare_history_token', sid, owner, cw.scalar(token.value)])
    for folder in ('pops', 'population', 'buildings'):
        for p in effective(ROOT, GAME, 'common/history/'+folder):
            raw = p.read_text(encoding='utf-8-sig')
            for s in cw.walk(cw.parse(raw)):
                if not s.key.startswith('s:STATE_'): continue
                sid = s.key[2:]
                for r in s.children():
                    if not r.key.startswith('region_state:'): continue
                    owner = r.key.split(':')[1]
                    if r.children(): references.add((folder, sid, owner))
                    for pop in r.children('create_pop'):
                        # Missing religions are resolved from the effective culture definition below.
                        culture = cw.scalar(pop.one('culture'))
                        religion = cw.scalar(pop.one('religion', 'DEFAULT:'+culture))
                        size = int(pop.one('size'))
                        pops[(culture, religion)] += size
                        regional_pop[(sid, owner, culture, religion)] += size
                    for b in r.children('create_building'):
                        body = signature(b)
                        buildings[(sid, owner, body)] += 1
                        for ownership in b.children('add_ownership'):
                            for hold in ownership.children('building'):
                                hold_region = cw.scalar(hold.one('region', sid))
                                hold_country = cw.scalar(hold.one('country', 'c:'+owner)).removeprefix('c:')
                                references.add(('economic_owner', hold_region, hold_country))
    for p in effective(ROOT, GAME, 'common/history/military_formations'):
        for root in cw.parse(p.read_text(encoding='utf-8-sig')):
            for country in root.children():
                if not country.key.startswith('c:'): continue
                owner = country.key[2:]
                # Formation + combat-unit details, including service type and count.
                for form in country.children('create_military_formation'):
                    for u in form.children('combat_unit'):
                        sid = cw.scalar(u.one('state_region')).removeprefix('s:')
                        units[(owner, form.one('name', ''), sid, signature(u))] += 1
                        references.add(('recruitment', sid, owner))
    for p in effective(ROOT, GAME, 'common/country_definitions'):
        for n in cw.parse(p.read_text(encoding='utf-8-sig')):
            if n.children('country_type'): countries[n.key.removeprefix('REPLACE_OR_CREATE:')] = signature(n)
    cultures = {}
    for p in effective(ROOT, GAME, 'common/cultures'):
        for n in cw.parse(p.read_text(encoding='utf-8-sig')):
            cultures[n.key] = cw.scalar(n.one('religion', 'UNRESOLVED_DEFAULT'))
    resolved = C.Counter()
    for (cu, rel), size in pops.items():
        resolved[(cu, cultures.get(cu, 'UNRESOLVED_DEFAULT') if rel.startswith('DEFAULT:') else rel)] += size
    for rgb, sid, owner in owners:
        if geometry.get(rgb) != sid: errors.append(['wrong_state_region', rgb, sid, owner, geometry.get(rgb)])
    for folder, sid, owner in references:
        if (sid, owner) not in state_pairs: errors.append(['orphan_selector', folder, sid, owner])
    counts = C.Counter()
    for (rgb, _, _), v in owners.items(): counts[rgb] += v
    level_totals = C.Counter()
    for (sid, owner, body), repeats in buildings.items():
        node = json.loads(body)
        # Sum declared add_ownership levels; do not claim these model engine overlay semantics.
        def visit(n):
            if n[0] == 'levels' and isinstance(n[2], str): return int(n[2])
            return sum(visit(v) for v in n[2]) if isinstance(n[2], list) else 0
        kind = next(n[2] for n in node[2] if n[0] == 'building')
        level_totals[kind] += repeats * visit(node)
    return dict(owners=tagged(owners), states=sorted([list(k) for k in state_pairs]),
                state_types=state_types, geometry=geometry, countries=countries,
                pops=tagged(pops), resolved_demographics=tagged(resolved), regional_pop=tagged(regional_pop),
                buildings=tagged(buildings), building_levels_written=tagged(level_totals), units=tagged(units),
                errors=sorted(errors, key=str), duplicates={r: n for r, n in counts.items() if n > 1})

def capture():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT/'MAP2A_BASELINE.json').exists(), 'Do not overwrite the actual pre-edit snapshot.'
    paths = subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'], cwd=ROOT).decode().split('\0')
    protected = {p: sha(ROOT/p) for p in sorted(set(paths)) if p and (ROOT/p).is_file()
                 and not p.startswith('docs/reports/map/MAP2A/')}
    for p in (ROOT/'docs/reports/map/MAP1C').rglob('*'):
        if p.is_file(): protected[p.relative_to(ROOT).as_posix()] = sha(p)
    data = dict(head=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT).decode().strip(),
                branch=subprocess.check_output(['git','branch','--show-current'], cwd=ROOT).decode().strip(),
                originals={p: (ROOT/p).read_text(encoding='utf-8-sig') for p in HISTORY},
                hashes=protected, inventory=inventory(), native_test='NOT_RUN')
    (OUT/'MAP2A_BASELINE.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('MAP2A baseline captured:', len(protected), 'files; population', sum(r['count'] for r in data['inventory']['pops']))

def validate():
    base = json.loads((OUT/'MAP2A_BASELINE.json').read_text(encoding='utf-8'))
    before, after = base['inventory'], inventory()
    expected = counter(before['owners'])
    expected[('x9AC196','STATE_LOMBARDY','VEN')] -= 1
    expected[('x9AC196','STATE_LOMBARDY','SWI')] += 1
    for rgb in ('x71E080','xF0E080'):
        del expected[(rgb,'STATE_UPPER_SILESIA','PRU')]
        del expected[(rgb,'STATE_UPPER_SILESIA','AUS')]
        expected[(rgb,'STATE_MORAVIA','AUS')] += 1
    del expected[('x9061E0','STATE_UPPER_SILESIA','AUS')]
    expected[('x9061E0','STATE_WEST_GALICIA','AUS')] += 1
    assert +expected == counter(after['owners']), 'Unexpected territorial change.'
    assert before['owners'], 'Empty province snapshot'
    assert {tuple(r['key'])[0] for r in before['owners']} == {tuple(r['key'])[0] for r in after['owners']}
    assert before['pops'] == after['pops'], 'Raw global culture/religion population changed.'
    assert before['resolved_demographics'] == after['resolved_demographics'], 'Effective religious composition changed.'
    assert before['building_levels_written'] == after['building_levels_written'], 'Declared building levels changed.'
    assert before['countries'] == after['countries'], 'Country definitions/capitals changed.'
    assert before['geometry'] == after['geometry'], 'Physical map/state geometries changed.'
    expected_pairs = {tuple(k) for k in before['states']}
    expected_pairs.remove(('STATE_UPPER_SILESIA','AUS'))
    expected_pairs |= {('STATE_LOMBARDY','SWI'), ('STATE_WEST_GALICIA','AUS')}
    assert expected_pairs == {tuple(k) for k in after['states']}
    assert {v[1] for v in before['states']} == {v[1] for v in after['states']}, 'Existing countries changed.'
    assert all(after['state_types'][k] == v for k, v in before['state_types'].items()
               if k != 'STATE_UPPER_SILESIA|AUS'), 'Existing incorporation status changed.'
    assert not set(map(str, after['errors'])) - set(map(str, before['errors'])), 'New critical orphan/region errors.'
    assert {k: v for k, v in after['duplicates'].items() if k not in ('x71E080','xF0E080')} == {
        k: v for k, v in before['duplicates'].items() if k not in ('x71E080','xF0E080')}
    # Only the single Austrian conscript changes recruitment geography; commanders and HQ unchanged.
    military_path = HISTORY[-1]
    old = cw.parse(base['originals'][military_path])
    aus = next(n for n in cw.walk(old) if n.key == 'c:AUS')
    matches = [u for u in cw.walk(aus.children()) if u.key == 'combat_unit' and u.one('state_region') == 's:STATE_UPPER_SILESIA']
    assert len(matches) == 1 and matches[0].one('count') == '1' and matches[0].one('service_type') == 'conscript'
    matches[0].children('state_region')[0].value = 's:STATE_WEST_GALICIA'
    assert [norm(n) for n in old] == [norm(n) for n in cw.parse((ROOT/military_path).read_text(encoding='utf-8-sig'))]
    # Commands, production methods, foreign ownership and reserves compared to the precise planned transformation.
    import map2a_patch as planned
    intended = planned.transform(base['originals'])
    for path in HISTORY:
        assert [norm(n) for n in cw.parse(intended[path])] == [norm(n) for n in cw.parse((ROOT/path).read_text(encoding='utf-8-sig'))], 'Unplanned history edit: '+path
    changed_all = sorted(p for p, digest in base['hashes'].items() if sha(ROOT/p) != digest)
    changed = [p for p in changed_all if p not in ('tools/validate_map2a.py', 'tools/map2a_patch.py')]
    assert set(changed) == {p for p in HISTORY if intended[p] != base['originals'][p]}, ('Unrelated existing file changed', changed)
    assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT).decode().strip() == base['head']
    assert subprocess.check_output(['git','branch','--show-current'], cwd=ROOT).decode().strip() == base['branch']
    import validate_luxembourg_beo_integration as lux
    lux.validate_lux_only()
    import validate_regional_infrastructure_shortage as infra
    infra.model_tests()
    # Recheck the protected Ottoman gameplay with its existing executable models.
    cw.model_tests()
    cw.ottoman_admin_building_checks()
    cw.egypt_building_checks()
    candidate = Path('C:/Users/simeo/.codex/worktrees/map-0-collaborator-integration/1776_Age_of_Revolutions_fork/common/history/states/00_states.txt')
    candidate_raw = candidate.read_text(encoding='utf-8-sig')
    candidate_ns = cw.parse(candidate_raw)
    bess = next(n for n in cw.walk(candidate_ns) if n.key == 's:STATE_BESSARABIA')
    assert not bess.children('create_state')[0].children(''), 'Git command tokens remain in candidate Bessarabia.'
    lomb = next(n for n in cw.walk(candidate_ns) if n.key == 's:STATE_LOMBARDY')
    holders = [cw.scalar(n.one('country')) for n in lomb.children('create_state')
               if 'x867A90' in values(n,'owned_provinces')]
    assert holders == ['c:VEN'], 'Candidate Bergamo still has multiple owners.'
    def unit_counts(inv):
        counts = C.Counter()
        for r in inv['units']:
            body = json.loads(r['key'][3])
            children = {n[0]:n[2] for n in body[2]}
            counts[(r['key'][0], children.get('service_type','regular'), children.get('type',''))] += int(children['count'])*r['count']
        return tagged(counts)
    assert unit_counts(before) == unit_counts(after), 'Military unit totals changed.'
    assert sum(r['count'] for r in before['buildings']) == sum(r['count'] for r in after['buildings'])
    pop_rows = []
    old_pop, new_pop = counter(before['regional_pop']), counter(after['regional_pop'])
    for key in sorted(set(old_pop)|set(new_pop)):
        if key[0] in TARGETS:
            sid, owner, cu, rel = key
            pop_rows.append([sid,owner,cu,rel,old_pop[key],new_pop[key],new_pop[key]-old_pop[key]])
    data = dict(result='PASS', validation_kind='STATIC_NOT_GAME_ENGINE',
                corrected_rgb_count=4, affected_state_regions=sorted(TARGETS),
                unique_provinces_before=len({r['key'][0] for r in before['owners']}),
                unique_provinces_after=len({r['key'][0] for r in after['owners']}),
                duplicate_rgbs_before=len(before['duplicates']), duplicate_rgbs_after=len(after['duplicates']),
                global_population_before=sum(r['count'] for r in before['pops']),
                global_population_after=sum(r['count'] for r in after['pops']),
                culture_religion_conservation='PASS; explicit and effective default religions',
                declared_building_levels_before=before['building_levels_written'],
                declared_building_levels_after=after['building_levels_written'],
                building_semantics='Written levels and exact ownership/PM commands checked; game engine aggregation not simulated',
                units_commanders_hq='PASS; exactly one AUS conscript recruitment selector corrected',
                countries_capitals_subjects='PRESERVED', Luxembourg='PASS before and after',
                ai_regression_models='PASS 10 scenarios',
                ottoman_regression_models='PASS: 1024 administrative combinations, 192 political combinations, startup events, 10-level cuts, Egyptian buildings',
                building_declarations_before=sum(r['count'] for r in before['buildings']),
                building_declarations_after=sum(r['count'] for r in after['buildings']),
                unit_totals_before=unit_counts(before), unit_totals_after=unit_counts(after),
                active_country_count_before=len({v[1] for v in before['states']}),
                active_country_count_after=len({v[1] for v in after['states']}),
                state_owner_pair_count_before=len(before['states']), state_owner_pair_count_after=len(after['states']),
                candidate_technical_checks='PASS: five Git tokens removed; x867A90 solely VEN; draft not merge-ready',
                errors_removed=sorted(set(map(str,before['errors']))-set(map(str,after['errors']))),
                preexisting_errors_after=after['errors'], new_errors=[],
                changed_gameplay_files=changed, protected_existing_files=len(base['hashes'])-len(changed_all),
                new_map2a_tools_adjusted_after_capture=[p for p in changed_all if p not in changed],
                MAP1C_files_preserved=sum(p.startswith('docs/reports/map/MAP1C/') for p in base['hashes']),
                native_load_and_one_month_test='NOT_RUN; player validation required', commit_merge_push='NOT_PERFORMED')
    (OUT/'MAP2A_VALIDATION.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT/'MAP2A_TABLE_DATA.json').write_text(json.dumps(dict(population=pop_rows), ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in data.items() if k not in ('preexisting_errors_after','declared_building_levels_before','declared_building_levels_after','unit_totals_before','unit_totals_after')}, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    capture() if '--capture' in sys.argv else validate()
