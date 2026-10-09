#!/usr/bin/env python3
"""Plan and validate the approved naval/administrative revision, without runtime writes.

--prepare captures an immutable, ignored baseline and prints an apply_patch plan.
--check verifies the exact planned edits, population conservation, recruitment
capacity, fleet technology and native entity/graphic bindings. No engine claim.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import math
import re
from pathlib import Path
import audit_british_colonial_start as previous
import build_start_1776_research_input_pack as catalog
import build_start_1776_runtime_wave1 as infra
import build_start_1776_world_apply as world

ROOT = world.ROOT
CACHE = ROOT / '.asset-cache/naval_admin_revision_2026-10-08'
POP_PATH = 'common/history/pops/10_india.txt'
# Leave a reserve from the reported +283, including possible national bonuses.
GBR_REMOVE = {'STATE_HOME_COUNTIES': 11, 'STATE_LANCASHIRE': 4,
              'STATE_YORKSHIRE': 2, 'STATE_MIDLANDS': 3}
STATES = ('STATE_WEST_BENGAL', 'STATE_EAST_BENGAL', 'STATE_BIHAR',
          'STATE_CIRCARS', 'STATE_AWADH')
CREWS = {'ship_type_caravel': 150, 'ship_type_galley': 240, 'ship_type_cog': 60}
COUNTERPARTS = previous.CHEAP

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pop_regions(raw):
    states = world.block_spans(raw, r's:STATE_[A-Za-z0-9_]+', 1)
    return {(owner.split(':')[1], next(s.split(':')[1] for s,x,y in states if x<a<y)): (a,b,raw[a:b])
            for owner,a,b in world.block_spans(raw, r'region_state:[A-Za-z0-9_]+', 2)}

def pop_rows(raw):
    return [raw[a:b] for _,a,b in world.block_spans(raw, 'create_pop', 1)]

def pop_size(raw):
    return sum(int(catalog.scalar(p, 'size')) for p in pop_rows(raw))

def fleet_targets(rows, tech):
    """Preserve counts; keep ~1/8 advanced hulls per country/category, not per fleet."""
    totals = collections.Counter()
    reverse = {v:k for k,v in COUNTERPARTS.items()}
    for r in rows:
        for kind,n in r['ships']:
            totals[r['owner'],reverse.get(kind,kind)] += n
    quotas = {key: (max(1,n//8) if key[1] != 'ship_type_troop_ship'
                    and 'scientific_naval_architecture' in tech.get(key[0],set()) else 0)
              for key,n in totals.items() if key[1] in COUNTERPARTS}
    assigned = collections.defaultdict(collections.Counter)
    # Assign modern ships to the largest formations first, preserving flagships.
    for key,n in totals.items():
        if key[1] not in COUNTERPARTS: continue
        candidates = []
        for index,r in enumerate(rows):
            if r['owner'] != key[0]: continue
            count = sum(c for k,c in r['ships'] if reverse.get(k,k)==key[1])
            if count: candidates.append((index,count))
        left = quotas[key]
        for index,count in sorted(candidates,key=lambda x:(-x[1],x[0])):
            take = min(left,max(1,count//8)) if left else 0
            assigned[index][key[1]] = take
            left -= take
        # Very small categories can concentrate their only modern hull in one fleet.
        if left:
            index,count = max(candidates,key=lambda x:x[1])
            assigned[index][key[1]] += left
    result = {}
    for index,r in enumerate(rows):
        counts = collections.Counter()
        for kind,n in r['ships']: counts[reverse.get(kind,kind)] += n
        out = []
        for kind,n in counts.items():
            if kind not in COUNTERPARTS: out.append((kind,n)); continue
            keep = assigned[index][kind]
            if keep: out.append((kind,keep))
            if n>keep: out.append((COUNTERPARTS[kind],n-keep))
        result[r['owner']+'@'+r['name']] = out
    return result

def demographic_target(raw, levels, pms):
    regions = pop_regions(raw)
    methods = catalog.effective_objects('common/production_methods', r'pm_[A-Za-z0-9_]+')
    cultures = catalog.effective_objects('common/cultures', r'[A-Za-z0-9_]+')
    ratio = infra.number((ROOT/'common/defines/00_defines.txt').read_text(), 'WORKING_ADULT_RATIO_BASE')
    if not 0<ratio<1: raise ValueError('Invalid workforce ratio')
    changes, report = [], []
    for state in STATES:
        key = 'BIC',state,previous.ADMIN
        count = levels[key]
        active = [p.replace('pm_hereditary_bureaucrats','pm_professional_bureaucrats') for p in pms[key]]
        jobs = {role:int(sum(infra.number(methods[pm].text, f'building_employment_{role}_add') for pm in active)*count)
                for role in ('bureaucrats','clerks')}
        a,b,region = regions['BIC',state]
        pops = pop_rows(region)
        additions = {}
        for role,required in jobs.items():
            # Credit only English/Protestant pools, which are unambiguously accepted.
            existing = sum(int(catalog.scalar(p,'size')) for p in pops
                           if catalog.scalar(p,'culture')=='british'
                           and catalog.scalar(p,'religion','protestant')=='protestant'
                           and catalog.scalar(p,'pop_type')==role)
            additions[role] = max(0,math.ceil(required*1.2/ratio)-existing)
        amount = sum(additions.values())
        donors = []
        for _,x,y in world.block_spans(region,'create_pop',1):
            p=region[x:y]; culture=catalog.scalar(p,'culture')
            religion=catalog.scalar(p,'religion',catalog.scalar(cultures[culture].text,'religion'))
            if religion=='hindu' and not catalog.scalar(p,'pop_type'):
                donors.append((int(catalog.scalar(p,'size')),x,y,p))
        size,x,y,donor=max(donors)
        if amount>size//10: raise ValueError(f'Excessive conversion {state}')
        updated=re.sub(r'(\bsize\s*=\s*)\d+',lambda m:m[1]+str(size-amount),donor,count=1)
        new=region[:x]+updated+region[y:]
        insert='\n\t\t\t# Accepted qualified administrative families; split from local Hindu population.\n'
        for role,n in additions.items():
            if n:
                insert+=('\t\t\tcreate_pop = {\n\t\t\t\tculture = british\n'
                         '\t\t\t\treligion = protestant\n'
                         f'\t\t\t\tpop_type = {role}\n\t\t\t\tsize = {n}\n\t\t\t}}\n')
        closing=new.rfind('}')
        new=new[:closing].rstrip()+insert+'\t\t'+new[closing:]
        if pop_size(new)!=pop_size(region): raise ValueError('Population changed')
        changes.append((a,b,new))
        report.append({'state':state,'admin_levels':count,'jobs':jobs,'working_adult_ratio':ratio,
                       'reserve':0.2,'converted_population':amount,'new_families':additions,
                       'donor_culture':catalog.scalar(donor,'culture'), 'donor_before':size,
                       'donor_after':size-amount,'state_total':pop_size(region)})
    for a,b,new in sorted(changes,reverse=True): raw=raw[:a]+new+raw[b:]
    return raw,report

def prepare():
    CACHE.mkdir(parents=True,exist_ok=True)
    baseline=CACHE/'baseline.json'
    if baseline.exists(): raise ValueError('Baseline exists; use --check, never replace it')
    raws,placements=world.all_placements(world.HISTORY)
    levels,pms,_=infra.actual_semantics()
    naval={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig')
           for p in sorted((ROOT/'common/history/military_formations').glob('*.txt'))}
    rows=previous.fleets(naval)
    targets=fleet_targets(rows,previous.technology_sets())
    objects=catalog.effective_objects('common/ship_types',r'ship_type_[A-Za-z0-9_]+')
    crew=sum(n*(CREWS[k] if k in CREWS else infra.number(objects[k].text,'ship_crew_max_add'))
             for r in rows if r['owner']=='GBR' for k,n in targets[r['owner']+'@'+r['name']])
    naval_level=math.ceil(crew*1.2/1000)
    edits=collections.defaultdict(list)
    grouped=collections.defaultdict(list)
    for p in placements: grouped[p.key].append(p)
    for state,remove in GBR_REMOVE.items():
        ps=grouped['GBR',state,previous.ADMIN]
        for p,n in zip(ps,world.allocate([p.level for p in ps],sum(p.level for p in ps)-remove)):
            edits[p.path].append((p.start,p.end,world.rescale_ownership(p.text,n)))
    naval_ps=[p for p in placements if p.owner=='GBR' and p.building=='building_naval_administration']
    for p,n in zip(naval_ps,world.allocate([p.level for p in naval_ps],naval_level)):
        edits[p.path].append((p.start,p.end,world.rescale_ownership(p.text,n)))
    for p in placements:
        if p.owner=='BIC' and p.building==previous.ADMIN:
            text=p.text.replace('pm_hereditary_bureaucrats','pm_professional_bureaucrats')
            edits[p.path].append((p.start,p.end,text))
    expected={}
    before={}
    for path,changes in edits.items():
        raw=raws[path]; before[path.relative_to(ROOT).as_posix()]=raw
        for a,b,new in sorted(changes,reverse=True): raw=raw[:a]+new+raw[b:]
        expected[path.relative_to(ROOT).as_posix()]=raw
    for path,raw in naval.items():
        before[path]=raw
        for r in sorted((r for r in rows if r['path']==path),key=lambda r:r['start'],reverse=True):
            raw=raw[:r['start']]+previous.replace_ships(r['text'],targets[r['owner']+'@'+r['name']])+raw[r['end']:]
        expected[path]=raw
    before[POP_PATH]=(ROOT/POP_PATH).read_text(encoding='utf-8-sig')
    expected[POP_PATH],demographics=demographic_target(before[POP_PATH],levels,pms)
    graphics=[e['proposed_dds'] for e in json.loads((ROOT/'.asset-cache/early_ship_graphics_2026-10-08/candidates.json').read_text())['candidates']]
    permitted=set(expected)|set(graphics)|{'common/ship_types/10_1776_early_ships.txt'}
    base={'before':before,'expected':expected,'targets':targets,'demographics':demographics,
          'gbr_base_crew':crew,'gbr_naval_levels':naval_level,'allowed_runtime':sorted(permitted),
          'protected':{p.relative_to(ROOT).as_posix():hash_file(p) for folder in ('common','gui','gfx')
                       for p in (ROOT/folder).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in permitted}}
    baseline.write_text(json.dumps(base,indent=2),encoding='utf-8')
    patch='*** Begin Patch\n'+''.join(previous.patch_file(p,before[p],raw) for p,raw in expected.items())+'*** End Patch'
    (CACHE/'planned.patch').write_text(patch,encoding='utf-8')
    print(json.dumps({'patch':patch,'gbr_crew':crew,'gbr_naval_levels':naval_level,
                      'converted':sum(r['converted_population'] for r in demographics),'demographics':demographics}))

def check():
    base=json.loads((CACHE/'baseline.json').read_text())
    errors=[]
    for path,expected in base['expected'].items():
        # Allow whitespace-only cleanup of the generated patch, not data drift.
        current=(ROOT/path).read_text(encoding='utf-8-sig')
        if [s.rstrip() for s in current.splitlines()]!=[s.rstrip() for s in expected.splitlines()]:
            errors.append('Unexpected edit: '+path)
        catalog.brace_maps(catalog.clean_comments(expected))
    for path,digest in base['protected'].items():
        if not (ROOT/path).exists() or hash_file(ROOT/path)!=digest: errors.append('Protected changed: '+path)
    for folder in ('common','gui','gfx'):
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and p.relative_to(ROOT).as_posix() not in set(base['protected'])|set(base['allowed_runtime']):
                errors.append('Unexpected new runtime: '+str(p))
    before,after=pop_regions(base['before'][POP_PATH]),pop_regions((ROOT/POP_PATH).read_text(encoding='utf-8-sig'))
    if before.keys()!=after.keys(): errors.append('Population regions changed')
    for key,(a,b,text) in before.items():
        current=after[key][2]
        if pop_size(text)!=pop_size(current): errors.append('Population total changed: '+str(key))
        if not (key[0]=='BIC' and key[1] in STATES) and text!=current: errors.append('Unrelated pops changed: '+str(key))
    for r in base['demographics']:
        pops=pop_rows(after['BIC',r['state']][2])
        for role,jobs in r['jobs'].items():
            available=sum(int(catalog.scalar(p,'size')) for p in pops if catalog.scalar(p,'culture')=='british'
                          and catalog.scalar(p,'religion','protestant')=='protestant' and catalog.scalar(p,'pop_type')==role)*r['working_adult_ratio']
            if available<jobs*1.2:errors.append('Insufficient accepted pool: '+r['state']+':'+role)
    tech=previous.technology_sets()
    objects=catalog.effective_objects('common/ship_types',r'ship_type_[A-Za-z0-9_]+')
    navy=[]
    for row in previous.fleets({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in base['before'] if 'military_formations/' in p}):
        key=row['owner']+'@'+row['name']
        if row['ships']!=[tuple(s) for s in base['targets'][key]]:errors.append('Fleet differs: '+key)
        old=next(r for r in previous.fleets({p:raw for p,raw in base['before'].items() if 'military_formations/' in p}) if r['owner']+'@'+r['name']==key)
        if sum(n for _,n in old['ships'])!=sum(n for _,n in row['ships']):errors.append('Fleet count changed: '+key)
        for kind,n in row['ships']:
            required=catalog.tokens_flat(catalog.braced_tokens(objects[kind].text,'unlocking_technologies'))
            if any(t not in tech.get(row['owner'],set()) for t in required):errors.append('Unavailable ship: '+key+':'+kind)
        navy.append({'country':row['owner'],'name':row['name'],'ships':row['ships']})
    for modern,cheap in COUNTERPARTS.items():
        obj=objects[cheap].text; original=objects[modern].text
        for prop in ('ship_hit_points_max_add','ship_hull_damage_add','ship_crew_max_add'):
            if infra.number(obj,prop)>=infra.number(original,prop):errors.append('Not weaker: '+cheap+':'+prop)
        for prop in ('goods_input_hardwood_add','goods_input_fabric_add'):
            # First occurrence is construction goods, independent of materiel.
            if infra.number(obj,prop)>infra.number(original,prop)*0.21:errors.append('Not inexpensive: '+cheap+':'+prop)
        for prop in ('profile_texture','icon'):
            path=catalog.scalar(obj,prop)
            if not (ROOT/path).exists() and not (world.VANILLA/path).exists():errors.append('Graphic missing: '+path)
    native='\n'.join(p.read_text(encoding='utf-8-sig') for p in (world.VANILLA/'gfx/models').rglob('*.asset'))
    entities=(ROOT/'gfx/map/fleet_entities/10_1776_early_ships.txt').read_text()
    for name in re.findall(r'\bentity\s*=\s*"([^"]+)"',entities):
        if not re.search(r'\bname\s*=\s*"'+re.escape(name)+r'"',native):errors.append('Native entity missing: '+name)
    result={'status':'FAIL' if errors else 'PASS_STATIC_NAVAL_ADMIN_REVISION','engine_tested':False,
            'errors':errors,'gbr_removed_admin':sum(GBR_REMOVE.values()),'gbr_base_crew':base['gbr_base_crew'],
            'gbr_naval_levels':base['gbr_naval_levels'],'converted_population':sum(r['converted_population'] for r in base['demographics']),
            'demographics':base['demographics'],'fleets':navy,'protected_files':len(base['protected'])}
    (CACHE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('demographics','fleets')}))
    if errors:raise SystemExit(1)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare',action='store_true');parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.prepare==args.check:parser.error('Choose exactly --prepare or --check')
    prepare() if args.prepare else check()
