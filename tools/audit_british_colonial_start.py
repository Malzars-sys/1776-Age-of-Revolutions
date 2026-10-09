#!/usr/bin/env python3
"""Read-only planner/validator for the user-requested October 2026 start changes.

--prepare stores a baseline and emits an apply_patch document; it does not edit
gameplay files. Diagnostics live in the ignored asset cache.
"""
from __future__ import annotations
import argparse
import collections
import difflib
import hashlib
import json
import math
import re
from pathlib import Path
import build_start_1776_research_input_pack as catalog
import build_start_1776_world_apply as world
import build_start_1776_runtime_wave1 as infra
import build_start_1776_company_ownership_validate as companies

ROOT = world.ROOT
CACHE = ROOT / '.asset-cache/british_colonial_start_2026-10-08'
ADMIN = 'building_government_administration'
ROAD = 'building_railway'
GBR_REMOVE = {'STATE_HOME_COUNTIES': 9, 'STATE_LANCASHIRE': 4,
              'STATE_YORKSHIRE': 2, 'STATE_MIDLANDS': 3}
BIC_ADD = {'STATE_WEST_BENGAL': 60, 'STATE_EAST_BENGAL': 40,
           'STATE_BIHAR': 20, 'STATE_CIRCARS': 15, 'STATE_AWADH': 5}
CHEAP = {'ship_type_frigate': 'ship_type_caravel',
         'ship_type_ship_of_the_line': 'ship_type_galley',
         'ship_type_troop_ship': 'ship_type_cog'}
PUBLIC = {ADMIN, 'building_port', 'building_barrack',
          'building_naval_administration', 'building_naval_fortification'}

def country_spans(text):
    return world.block_spans(text, r'c:[A-Za-z0-9_]+[ \t]*\?', 1)

def ships(block):
    return [(catalog.scalar(block[a:b], 'type').removeprefix('ship_type:'),
             int(catalog.scalar(block[a:b], 'count', '0')))
            for _, a, b in world.block_spans(block, 'ship', 1)]

def technology_sets():
    effects = catalog.effective_objects('common/scripted_effects', r'[A-Za-z0-9_]+')
    result = collections.defaultdict(set)
    def expanded(text, seen):
        found = set(re.findall(r'\badd_technology_researched\s*=\s*([\w]+)', catalog.clean_comments(text)))
        for key in re.findall(r'\b(effect_starting_technology_[\w]+)\s*=\s*yes', catalog.clean_comments(text)):
            if key not in seen and key in effects:
                found |= expanded(effects[key].text, seen | {key})
        return found
    for path in sorted((ROOT / 'common/history/countries').glob('*.txt')):
        raw = path.read_text(encoding='utf-8-sig')
        for owner, a, b in country_spans(raw):
            result[owner.split()[0].removeprefix('c:')] |= expanded(raw[a:b], set())
    return result

def fleets(raws):
    result = []
    for path, raw in raws.items():
        for owner, a, b in country_spans(raw):
            country = raw[a:b]
            for _, x, y in world.block_spans(country, 'create_military_formation', 1):
                text = country[x:y]
                if catalog.scalar(text, 'type') == 'fleet':
                    result.append({'path': path, 'owner': owner.split()[0].removeprefix('c:'),
                                   'start': a+x, 'end': a+y, 'text': text,
                                   'name': catalog.scalar(text, 'name'), 'ships': ships(text)})
    return result

def target_ships(row, tech):
    original = row['ships']
    total = sum(n for _, n in original)
    target = max(1, (total * 4 + 2) // 5) if row['owner'] == 'GBR' else total
    # Largest-remainder allocation, permitting zero when a single ship is removed.
    exact = [n * target / total for _, n in original]
    counts = [math.floor(n) for n in exact]
    order = sorted(range(len(exact)), key=lambda i: (-(exact[i]-counts[i]), i))
    for i in order[:target-sum(counts)]: counts[i] += 1
    advanced = 'scientific_naval_architecture' in tech.get(row['owner'], set())
    out = []
    for (kind, _), n in zip(original, counts):
        if kind not in CHEAP:
            if n: out.append((kind, n))
            continue
        # Keep a quarter of the technologically available advanced hulls.
        retain = n // 4 if advanced and kind != 'ship_type_troop_ship' else 0
        if retain: out.append((kind, retain))
        if n-retain: out.append((CHEAP[kind], n-retain))
    return out

def normalized(text):
    return re.sub(r'\s+', '', catalog.clean_comments(text))

def replace_ships(text, target):
    spans = world.block_spans(text, 'ship', 1)
    if not spans: return text
    replacement = '\n'.join('\t\t\tship = {\n'
                             f'\t\t\t\ttype = ship_type:{kind}\n'
                             f'\t\t\t\tcount = {n}\n\t\t\t}}'
                             for kind, n in target)
    for index, (_, a, b) in reversed(list(enumerate(spans))):
        text = text[:a] + (replacement if index == 0 else '') + text[b:]
    return text

def owned(text, owner, building, state, level, company_set):
    if owner != 'BIC' or building in PUBLIC: return text
    if building in company_set:
        share = f'company = {{\n\t\t\t\t\t\ttype = company_east_india_company\n\t\t\t\t\t\tcountry = "c:GBR"\n\t\t\t\t\t\tlevels = {level}\n\t\t\t\t\t}}'
    else:
        holder = 'building_manor_house' if building.endswith('_farm') or building.endswith('_plantation') else 'building_financial_district'
        share = f'building = {{\n\t\t\t\t\t\ttype = "{holder}"\n\t\t\t\t\t\tcountry = "c:GBR"\n\t\t\t\t\t\tregion = "STATE_HOME_COUNTIES"\n\t\t\t\t\t\tlevels = {level}\n\t\t\t\t\t}}'
    replacement = 'add_ownership = {\n\t\t\t\t\t' + share + '\n\t\t\t\t}'
    spans = world.block_spans(text, 'add_ownership', 1)
    if not spans: raise ValueError(f'Missing ownership: {building}')
    for index, (_, a, b) in reversed(list(enumerate(spans))):
        text = text[:a] + (replacement if index == 0 else '') + text[b:]
    return text

def patch_file(path, old, new):
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3))
    if not diff: return ''
    body = '\n'.join('@@' if line.startswith('@@') else line for line in diff[2:])
    return f'*** Update File: {path}\n{body}\n'

def prepare():
    CACHE.mkdir(parents=True, exist_ok=True)
    baseline = CACHE / 'baseline.json'
    if baseline.exists(): raise ValueError('Baseline already exists; do not replace it')
    raws, ps = world.all_placements(world.HISTORY)
    naval_raws = {p.relative_to(ROOT).as_posix(): p.read_text(encoding='utf-8-sig')
                  for p in sorted((ROOT / 'common/history/military_formations').glob('*.txt'))}
    tech = technology_sets()
    before_fleets = fleets(naval_raws)
    targets = {row['name']+'@'+row['owner']: target_ships(row, tech) for row in before_fleets}
    updated = dict(raws)
    edits = collections.defaultdict(list)
    company_set = companies.supported_buildings()['company_east_india_company']
    levels, pms, _ = infra.actual_semantics()
    desired = dict(levels)
    for state, n in GBR_REMOVE.items(): desired['GBR', state, ADMIN] -= n
    for state, n in BIC_ADD.items(): desired['BIC', state, ADMIN] += n
    # Use the established infrastructure calculator but apply only to BIC.
    state_rows = infra.read_csv(infra.STATE_CATALOG)
    _, _, roads, _ = infra.infrastructure_plan(state_rows, desired, pms)
    for key, n in roads.items():
        if key[0] == 'BIC': desired[key] = n
    by_key = collections.defaultdict(list)
    for p in ps: by_key[p.key].append(p)
    for key, rows in by_key.items():
        owner, state, building = key
        if owner != 'BIC' and not (owner == 'GBR' and building == ADMIN and state in GBR_REMOVE): continue
        count = desired[key]
        allocated = world.allocate([p.level for p in rows], count)
        for p, n in zip(rows, allocated):
            text = world.rescale_ownership(p.text, n) if n != p.level else p.text
            text = owned(text, owner, building, state, n, company_set)
            if text != p.text: edits[p.path].append((p.start, p.end, text))
    # Fit GBR sailor establishments to the mixed fleet plus 20% reserve.
    ship_objects = catalog.effective_objects('common/ship_types', r'ship_type_[A-Za-z0-9_]+')
    new_crews = {'ship_type_caravel': 250, 'ship_type_galley': 400, 'ship_type_cog': 100}
    crew = sum(n * (new_crews[k] if k in new_crews else infra.number(ship_objects[k].text, 'ship_crew_max_add'))
               for row in before_fleets if row['owner'] == 'GBR'
               for k, n in targets[row['name']+'@'+row['owner']])
    naval = [p for p in ps if p.owner == 'GBR' and p.building == 'building_naval_administration']
    sailor_capacity = 1000
    naval_target = math.ceil(crew * 1.2 / sailor_capacity)
    for p, n in zip(naval, world.allocate([p.level for p in naval], naval_target)):
        edits[p.path].append((p.start, p.end, world.rescale_ownership(p.text, n)))
        desired[p.key] = n
    for path, changes in edits.items():
        for a, b, text in sorted(changes, reverse=True): updated[path] = updated[path][:a]+text+updated[path][b:]
    naval_updated = dict(naval_raws)
    changes = collections.defaultdict(list)
    for row in before_fleets:
        target = targets[row['name']+'@'+row['owner']]
        text = replace_ships(row['text'], target)
        if text != row['text']: changes[row['path']].append((row['start'], row['end'], text))
    for path, items in changes.items():
        for a, b, text in sorted(items, reverse=True): naval_updated[path] = naval_updated[path][:a]+text+naval_updated[path][b:]
    base = {'buildings': [{'path': p.path.relative_to(ROOT).as_posix(), 'owner': p.owner,
                          'state': p.state, 'building': p.building, 'level': p.level,
                          'pms': p.pms, 'text': p.text} for p in ps],
            'naval_raws': naval_raws, 'targets': targets,
            'desired_levels': [[*k,n] for k,n in desired.items()],
            'british_required_base_crew': crew, 'naval_administration_target': naval_target,
            'company_buildings': sorted(company_set),
            'runtime_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                               for folder in ('common','gui','gfx/map') for p in (ROOT/folder).rglob('*') if p.is_file()}}
    baseline.write_text(json.dumps(base, indent=2), encoding='utf-8')
    patch = '*** Begin Patch\n'
    for path, new in updated.items(): patch += patch_file(path.relative_to(ROOT).as_posix(), raws[path], new)
    for path, new in naval_updated.items(): patch += patch_file(path, naval_raws[path], new)
    patch += '*** End Patch'
    print(json.dumps({'patch': patch, 'crew': crew, 'naval_levels': naval_target,
                      'gbr_before': sum(sum(n for _,n in r['ships']) for r in before_fleets if r['owner']=='GBR'),
                      'gbr_after': sum(sum(n for _,n in targets[r['name']+'@'+r['owner']]) for r in before_fleets if r['owner']=='GBR'),
                      'road_additions': [[*k,desired[k]-n] for k,n in levels.items() if k[0]=='BIC' and k[2]==ROAD and desired[k]!=n]}))

def validate():
    base = json.loads((CACHE/'baseline.json').read_text())
    errors = []
    _, ps = world.all_placements(world.HISTORY)
    actual = collections.defaultdict(int)
    for p in ps: actual[p.key] += p.level
    desired = {(o,s,b): n for o,s,b,n in base['desired_levels']}
    if {k:n for k,n in actual.items() if n} != {k:n for k,n in desired.items() if n}:
        errors.append('Unexpected building-level totals')
    original = collections.defaultdict(list)
    for p in base['buildings']: original[p['owner'],p['state'],p['building'],p['path']].append(p)
    ownership = []
    for p in ps:
        old = original[p.owner,p.state,p.building,p.path.relative_to(ROOT).as_posix()].pop(0)
        if list(p.pms) != old['pms']: errors.append(f'PM changed: {p.key}')
        expected = world.rescale_ownership(old['text'], p.level) if p.level != old['level'] else old['text']
        expected = owned(expected,p.owner,p.building,p.state,p.level,set(base['company_buildings']))
        if normalized(p.text) != normalized(expected): errors.append(f'Unexpected ownership/body: {p.key}')
        if p.owner != 'BIC': continue
        ownership.append({'state':p.state,'building':p.building,'levels':p.level,
                          'public_exception':p.building in PUBLIC})
    if any(original.values()):errors.append('A building placement was removed')
    current_raws = {p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in sorted((ROOT/'common/history/military_formations').glob('*.txt'))}
    before, after = fleets(base['naval_raws']), fleets(current_raws)
    if len(before) != len(after): errors.append('Formation count changed')
    rows = []
    for old, new in zip(before, after):
        target = [tuple(s) for s in base['targets'][old['name']+'@'+old['owner']]]
        if new['ships'] != target: errors.append(f'Unexpected ships: {new["name"]}')
        if normalized(new['text']) != normalized(replace_ships(old['text'],target)): errors.append(f'Formation metadata changed: {new["name"]}')
        rows.append({'country':new['owner'],'name':new['name'], 'before':sum(n for _,n in old['ships']),
                     'after':sum(n for _,n in target),'ships':target})
    for path, raw in base['naval_raws'].items():
        def strip_ships(text):
            clean = text
            _, pairs = catalog.brace_maps(catalog.clean_comments(text))
            matches = list(re.finditer(r'(?m)^\s*ship\s*=\s*\{',catalog.clean_comments(text)))
            for m in reversed(matches):
                a = text.find('{',m.start(),m.end()); clean=clean[:m.start()]+clean[pairs[a]+1:]
            return normalized(clean)
        if strip_ships(raw)!=strip_ships(current_raws[path]): errors.append(f'Non-ship history changed: {path}')
    objects = catalog.effective_objects('common/ship_types',r'ship_type_[A-Za-z0-9_]+')
    for old,new in CHEAP.items():
        if new not in objects: errors.append(f'Missing class: {new}');continue
        text=objects[new].text
        if catalog.braced_tokens(text,'unlocking_technologies'): errors.append(f'Locked cheap class: {new}')
        for prop in ('ship_crew_max_add','ship_hull_damage_add','ship_hit_points_max_add'):
            if infra.number(text,prop)>=infra.number(objects[old].text,prop): errors.append(f'Not a lower class: {new}:{prop}')
        for prop in ('icon','profile_texture'):
            p=catalog.scalar(text,prop)
            if not (ROOT/p).exists() and not (world.VANILLA/p).exists():errors.append(f'Missing graphic {p}')
        for lang in ('english','french'):
            lp=ROOT/f'localization/{lang}/1776_early_ships_l_{lang}.yml'
            if not lp.exists() or f'{new}:0' not in lp.read_text(encoding='utf-8-sig'):errors.append(f'Missing localization {new}:{lang}')
        old_text=objects[old].text
        for prop in ('goods_input_hardwood_add','goods_input_fabric_add'):
            if infra.number(text,prop)>=infra.number(old_text,prop):errors.append(f'Not cheaper construction: {new}:{prop}')
        if infra.number(text,'goods_input_grain_add')>=infra.number(old_text,'goods_input_grain_add'):
            errors.append(f'Not cheaper maintenance: {new}')
    # A class must be visible in the naval diorama as well as the menu.
    fleet_path=ROOT/'gfx/map/fleet_entities/10_1776_early_ships.txt'
    fleet_defs={b.object_id:b.text for b in catalog.named_blocks(fleet_path,r'ship_type_[A-Za-z0-9_]+',0)}
    entity_sources=[world.VANILLA/'gfx/models/military/units/military_units_ships.asset',
                    world.VANILLA/'gfx/models/infrastructure/ships/sail_transport_ship_01.asset']
    entity_text='\n'.join(p.read_text(encoding='utf-8-sig') for p in entity_sources)
    for key in CHEAP.values():
        if key not in fleet_defs:errors.append(f'Missing fleet graphic {key}');continue
        entity=catalog.scalar(fleet_defs[key],'entity')
        if f'name = "{entity}"' not in entity_text:errors.append(f'Unknown entity {entity}')
    name_defs=catalog.effective_objects('common/ship_name_definitions',r'[A-Za-z0-9_]+')
    if 'shipname_prefixes_clone_template' not in name_defs:errors.append('Missing native naming prefix template')
    for key in CHEAP.values():
        if not any(key in catalog.tokens_flat(catalog.braced_tokens(b.text,'allowed_ship_types')) for b in name_defs.values()):
            errors.append(f'Missing ship naming rule {key}')
    levels,pms,_=infra.actual_semantics()
    checks,_,_,_=infra.infrastructure_plan(infra.read_csv(infra.STATE_CATALOG),levels,pms)
    bic_checks=[r for r in checks if r['Owner_TAG']=='BIC']
    for r in bic_checks:
        if float(r['Infrastructure_Available'])<float(r['Infrastructure_Used']):errors.append(f'BIC infrastructure gap {r["State_ID"]}')
    allowed = {p['path'] for p in base['buildings'] if p['owner']=='BIC' or (p['owner']=='GBR' and p['building'] in (ADMIN,'building_naval_administration'))}
    allowed |= set(base['naval_raws'])
    for p,sha in base['runtime_hashes'].items():
        if p not in allowed and hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=sha:errors.append(f'Unrelated runtime changed: {p}')
    result={'status':'PASS_STATIC_BRITISH_COLONIAL_START' if not errors else 'FAIL',
            'engine_tested':False, 'errors':errors,
            'administrations':{'GBR_removed':18,'BIC_added':140,'BIC_capacity_added_full_workforce':2100},
            'british_required_base_crew':base['british_required_base_crew'],
            'british_naval_administration_levels':base['naval_administration_target'],
            'ownership':ownership,'fleets':rows,'BIC_infrastructure':bic_checks}
    (CACHE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('ownership','fleets','BIC_infrastructure')},indent=2))
    return 0 if not errors else 1

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true')
    args=parser.parse_args()
    if args.prepare:prepare()
    else:raise SystemExit(validate())
