"""Read-only save diagnosis and narrowly scoped startup regression checks.

Save infrastructure is a serialized cache, not a refreshed UI calculation.
Reports never claim that a static PM projection is a post-fix engine test.
"""
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
import inspect_oct09_saved_crews as saved
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
OUT = ROOT/'docs/reports/wallonia_start_1776_2026-10-10'
SAVE = ROOT/'.asset-cache/wallonia_start_2026-10-10/observateur_2_readonly.txt'
SOURCE_SAVE = Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/save games/observateur_2.v3')
HISTORIES = ('common/history/buildings/00_west_europe.txt',
             'common/history/buildings/98_build_start_1776_world_redistribution.txt')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def strict(nodes):
    return [[n.key, n.op, strict(n.value) if isinstance(n.value,list) else cw.scalar(n.value)] for n in nodes]

def snapshot():
    paths = []
    for directory in ('common', 'map_data', 'docs/reports/map/MAP1C', 'docs/reports/map/MAP2A'):
        paths.extend(p for p in (ROOT/directory).rglob('*') if p.is_file())
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}

def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def catalog(directory):
    return {n.key:n for p in effective(ROOT, GAME, directory)
            for n in cw.parse(p.read_text(encoding='utf-8-sig'))}

def pms(raw):
    match = re.search(r'^\t{3}production_methods=\{(.*?)^\t{3}\}', raw, re.M|re.S)
    return re.findall(r'"([^"]+)"', match.group(1)) if match else []

def goods(raw, direction):
    match = re.search(r'^\t{3}'+direction+r'_goods=\{(.*?)^\t{3}\}', raw, re.M|re.S)
    if not match:
        return {}
    return {int(k):float(v) for k,v in re.findall(r'^\t{5}(\d+)=\{\n\t{6}value=([\d.-]+)', match.group(1), re.M)}

def infrastructure_per_pm(node):
    state = node.children('state_modifiers')
    return sum(float(n.value) for root in state for n in cw.walk(root.children())
               if n.key == 'state_infrastructure_add')

def diagnose():
    saved.SAVE = SAVE
    states, countries, buildings = {}, {}, collections.defaultdict(list)
    for section, ident, raw in saved.objects():
        if section == 'country_manager':
            countries[ident] = saved.field(raw, 'definition')
        elif section == 'states':
            states[ident] = {
                'id':ident, 'country_id':int(saved.field(raw,'country') or -1),
                'region':saved.field(raw,'region'),
                'serialized_infrastructure_cache':float(saved.field(raw,'infrastructure') or 0),
                'serialized_usage':float(saved.field(raw,'infrastructure_usage') or 0),
                'controller_changed_pm_at_start':'flag="aor1776_ai_regional_changed_this_pulse"' in raw,
            }
        elif section == 'building_manager':
            row = {k:saved.field(raw,k) for k in ('building','levels','staffing','throughput','subsidized','goods_cost','goods_sales')}
            row.update(id=ident, pms=pms(raw), inputs=goods(raw,'input'), outputs=goods(raw,'output'))
            row['levels'] = float(row['levels'] or 0)
            row['staffing'] = float(row['staffing'] or 0)
            buildings[int(saved.field(raw,'state') or -1)].append(row)
    pm_defs = catalog('common/production_methods')
    building_defs = catalog('common/buildings')
    groups = catalog('common/building_groups')
    def usage(group):
        node = groups[group]
        own = node.one('infrastructure_usage_per_level')
        if own is not None: return float(own)
        parent = node.one('parent_group')
        return usage(cw.scalar(parent)) if parent else 0
    for ident, state in states.items():
        state['country'] = countries.get(state['country_id'])
        state['cache_delta'] = round(state['serialized_infrastructure_cache']-state['serialized_usage'],5)
        rail = [b for b in buildings[ident] if b['building']=='building_railway']
        state['regional_infrastructure'] = rail
        state['regional_fixed_output_at_saved_staffing'] = sum(b['staffing']*sum(infrastructure_per_pm(pm_defs[p]) for p in b['pms']) for b in rail)
    wallonia = next(s for s in states.values() if s['country']=='BEO' and s['region']=='STATE_WALLONIA')
    rows = buildings[wallonia['id']]
    totals = {'inputs':collections.Counter(), 'outputs':collections.Counter()}
    for b in rows:
        group = cw.scalar(building_defs[b['building']].one('building_group'))
        # Subsistence levels do not consume infrastructure like constructed farms.
        # Other figures are group-only estimates; saved state usage is authoritative.
        if 'subsistence' in b['building']:
            b['base_infrastructure_usage_per_level'] = 0
        else:
            b['base_infrastructure_usage_per_level'] = usage(group)
        b['base_infrastructure_usage'] = round(b['levels']*b['base_infrastructure_usage_per_level'],5)
        for direction in totals: totals[direction].update(b[direction])
    deficits = sorted((s for s in states.values() if s['cache_delta']<0), key=lambda s:s['cache_delta'])
    plan_path = ROOT/'docs/reports/buildings/BUILD_START_1776_RUNTIME_INFRASTRUCTURE_AUDIT.csv'
    with plan_path.open(encoding='utf-8-sig', newline='') as stream:
        plan = {(r['Owner_TAG'],r['State_ID']):r for r in csv.DictReader(stream)}
    for state in deficits:
        planned = plan.get((state['country'],state['region']))
        if planned:
            state['old_static_plan_usage'] = float(planned['Infrastructure_Used'])
            state['usage_above_old_plan'] = round(state['serialized_usage']-state['old_static_plan_usage'],5)
            state['old_static_plan_road_pm'] = planned['Road_PM']
            state['old_static_plan_canal_pm'] = planned['Canal_PM']
    start = SAVE.open(encoding='utf-8').read(1200)
    assert 'game_date=1776.1.1' in start
    result = {
        'source_save':str(SOURCE_SAVE), 'source_sha256':digest(SOURCE_SAVE),
        'game_date':'1776.1.1', 'game_version':'1.13.11',
        'warning':'Serialized infrastructure can precede startup scripted PM changes. Cache deltas are not current UI observations; household demand and current local shortages are not serialized in these building goods fields.',
        'wallonia':wallonia, 'wallonia_buildings':rows,
        'wallonia_building_goods_totals':{d:dict(v) for d,v in totals.items()},
        'states_inspected':len(states), 'states_with_negative_serialized_cache_delta':len(deficits),
        'deficit_states':deficits,
    }
    write('SAVE_DIAGNOSIS.json', result)
    print(json.dumps({'wallonia':wallonia,'building_goods':result['wallonia_building_goods_totals'],
                      'consumers':[(b['building'],b['levels'],b['base_infrastructure_usage']) for b in rows],
                      'states':len(states),'cache_deficit_states':len(deficits),
                      'largest_cache_deficits':[(s['country'],s['region'],s['cache_delta']) for s in deficits[:20]]}, ensure_ascii=False,indent=2))

def validate():
    baseline = json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    current = snapshot()
    assert set(current)==set(baseline['hashes']), 'Protected files added or deleted'
    changed = sorted(p for p in baseline['hashes'] if baseline['hashes'][p] != current.get(p))
    assert changed == sorted(HISTORIES), changed
    rows = []
    for path in HISTORIES:
        before = cw.parse(baseline['originals'][path])
        after = cw.parse((ROOT/path).read_text(encoding='utf-8-sig'))
        expected = 0
        for node in cw.walk(before):
            if node.key!='s:STATE_WALLONIA': continue
            for region in node.children('region_state:BEO'):
                for building in region.children('create_building'):
                    if cw.scalar(building.one('building'))!='building_railway': continue
                    # These histories derive size from ownership, not a root level field.
                    ownership = next(n for n in cw.walk(building.children()) if n.key=='levels')
                    assert ownership.value=='6'
                    ownership.value='13'
                    methods = building.children('activate_production_methods')[0]
                    canal = next(n for n in methods.children() if cw.scalar(n.value)=='pm_industrial_canals')
                    canal.value='"pm_no_canal_network"'
                    expected+=1
        assert expected == 1, (path,expected)
        assert strict(before)==strict(after), 'Unexpected history edit: '+path
        rows.append({'file':path,'written_command_level_before':6,'written_command_level_after':13,
                     'initial_canal_pm_before':'pm_industrial_canals','initial_canal_pm_after':'pm_no_canal_network'})
    observed = json.loads((OUT/'SAVE_DIAGNOSIS.json').read_text(encoding='utf-8'))
    rail = observed['wallonia']['regional_infrastructure']
    assert len(rail)==1 and rail[0]['levels']==6 and rail[0]['staffing']==6
    assert 'pm_traditional_road_network' in rail[0]['pms'] and 'pm_no_canal_network' in rail[0]['pms']
    # Conservative floor excludes canals, trains, population bonuses and the bloc.
    # Retain the saved usage, plus automatic ownership infrastructure for 7 levels.
    projected_usage = observed['wallonia']['serialized_usage'] + 7*0.1
    floor_supply = 3 + 13*3
    bloc_supply = floor_supply*1.1
    assert floor_supply > projected_usage
    write('VALIDATION.json', {'result':'PASS_STATIC','changed_gameplay_files':changed,'changes':rows,
          'protected_files_identical':len(baseline['hashes'])-len(changed),
          'explicit_other_building_commands_modified':0,
          'derived_financial_district_additional_levels':7,
          'projection_full_staffing_no_canals':{
              'usage_estimate':projected_usage,'supply_no_bloc_bonus':floor_supply,
              'reserve_no_bloc_bonus':round(floor_supply-projected_usage,5),
              'supply_with_existing_internal_trade_principle':bloc_supply,
              'reserve_with_existing_internal_trade_principle':round(bloc_supply-projected_usage,5)},
          'populations_and_map2a_unchanged':True,
          'new_game_after_fix':'NOT_RUN','save_observation_before_fix':observed['source_sha256']})
    print('PASS: exactly two Wallonia railway declarations 6 -> 13, startup canals disabled; every other history node, map file, PM definition and protected report unchanged. Post-fix new game NOT RUN.')

if __name__=='__main__':
    if '--capture' in sys.argv:
        assert not (OUT/'BASELINE.json').exists(), 'Never overwrite the pre-fix baseline'
        write('BASELINE.json', {'hashes':snapshot(),'originals':{p:(ROOT/p).read_text(encoding='utf-8-sig') for p in HISTORIES}})
        print('Pre-fix snapshot captured')
    elif '--diagnose' in sys.argv: diagnose()
    elif '--validate' in sys.argv: validate()
    else: raise SystemExit('Use --capture, --diagnose, or --validate')
