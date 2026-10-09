"""Validate the requested 108 extra German ranch levels and emit their patch.

--patch only prints an apply_patch-compatible change to the existing late
history regions. --snapshot freezes pre-change totals and unrelated data.
--baseline checks exactly +108 levels, local ownership, land and unchanged PMs.
This does not model employment, throughput, or fabric lost from subsistence.
"""
import argparse
from collections import Counter
import difflib
import hashlib
import json
from pathlib import Path
import re

import build_start_1776_research_input_pack as history

ROOT = history.ROOT
HISTORY = ROOT/'common/history/buildings'
OVERLAY = HISTORY/'98_build_start_1776_world_redistribution.txt'
RANCH = 'building_livestock_ranch'
PMS = {'pm_open_air_stockyards','pm_simple_ranch','pm_standard_fences','pm_unrefrigerated'}
PLAN = {
    ('PRU','STATE_BRANDENBURG'):8,
    ('PRU','STATE_POMERANIA'):8,
    ('PRU','STATE_EAST_PRUSSIA'):8,
    ('PRU','STATE_WEST_PRUSSIA'):8,
    ('PRU','STATE_LOWER_SILESIA'):8,
    ('BAV','STATE_BAVARIA'):10,
    ('BAV','STATE_FRANCONIA'):10,
    ('WUR','STATE_WURTTEMBERG'):12,
    ('BAD','STATE_BADEN'):10,
    ('SAX','STATE_SAXONY'):10,
    ('HES','STATE_HESSE'):6,
    ('HEK','STATE_HESSE'):6,
    ('MEC','STATE_MECKLENBURG'):4,
}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def structure():
    """Existing history structure stays identical; do not add duplicate states."""
    result = []
    for path in sorted(HISTORY.glob('*.txt')):
        for state in history.named_blocks(path,r's:STATE_[A-Za-z0-9_]+',1):
            regions = [r.object_id for r in history.subblocks(state,r'region_state:[A-Za-z0-9_]+')]
            result.append((path.name,state.object_id,regions))
    return result


def baseline_data():
    rows = history.parse_current_buildings()
    ranches = {}
    other = []
    for row in rows:
        pair = (row['owner'],row['state'])
        value = [row['owner'],row['state'],row['building'],row['level'],sorted(row['pms'])]
        if pair in PLAN and row['building'] == RANCH:
            ranches['|'.join(pair)] = row['level']
        else:
            other.append(value)
    for pair in PLAN:
        ranches.setdefault('|'.join(pair),0)
    protected = {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                 for folder in ['map_data/state_regions','common/history/states',
                                'common/history/power_blocs','common/production_method_groups']
                 for p in sorted((ROOT/folder).glob('*.txt'))}
    protected['common/production_methods/02_agro.txt'] = hashlib.sha256(
        (ROOT/'common/production_methods/02_agro.txt').read_bytes()).hexdigest()
    return {'ranch_levels':ranches,'other_buildings_sha256':digest(other),
            'history_structure_sha256':digest(structure()),'protected_files':protected}


def placements():
    rows = history.parse_current_buildings()
    owners = {(o['owner'],o['state']):o for o in history.parse_state_owners()}
    regions = history.parse_map_regions()
    # All selected non-Prussian owners are explicitly listed in the Austrian HRE.
    aus = next(b for b in history.named_blocks(ROOT/'common/history/power_blocs/00_power_blocs.txt',
                                               'c:AUS',1))
    members = set(re.findall(r'\bmember\s*=\s*c:([A-Z]+)',history.clean_comments(aus.text)))
    assert {tag for tag,_ in PLAN} <= members, 'Country outside the Austrian HRE market'
    output = []
    for (tag,state),added in PLAN.items():
        owner = owners[(tag,state)]
        block = regions[state]['block']
        resources = history.tokens_flat(history.braced_tokens(block.text,'arable_resources'))
        assert RANCH in resources, 'No ranch resource: '+state
        provinces = history.tokens_flat(history.braced_tokens(block.text,'provinces'))
        capacity = int(int(history.scalar(block.text,'arable_land','0')) *
                       len(owner['provinces'])/len(provinces))
        used = sum(r['level'] for r in rows if (r['owner'],r['state']) == (tag,state)
                   and r['building'] in resources)
        assert used <= capacity, (tag,state,used,capacity)
        output.append({'country':tag,'state':state,'added_levels':added,
                       'owned_arable_capacity_floor':capacity,'current_arable_usage':used})
    ranch_pm = next(b for b in history.named_blocks(ROOT/'common/production_methods/02_agro.txt',
                                                   'pm_simple_ranch',0))
    assert int(history.scalar(ranch_pm.text,'goods_output_fabric_add')) == 5
    assert sum(PLAN.values()) == 108
    return output


def make_patch():
    original = OVERLAY.read_text(encoding='utf-8-sig')
    updated = original
    found = set()
    for state in history.named_blocks(OVERLAY,r's:STATE_[A-Za-z0-9_]+',1):
        for region in history.subblocks(state,r'region_state:[A-Za-z0-9_]+'):
            pair = (region.object_id.split(':')[1],state.object_id.removeprefix('s:'))
            if pair not in PLAN:
                continue
            assert pair not in found, 'Ambiguous existing overlay region'
            found.add(pair)
            before = region.text
            ranches = [b for b in history.subblocks(region,'create_building')
                       if history.scalar(b.text,'building') == RANCH]
            assert len(ranches) <= 1
            if ranches:
                ranch = ranches[0].text
                assert re.findall(r'\blevels\s*=\s*(\d+)',history.clean_comments(ranch)) == ['1']
                assert history.scalar(ranch,'country') == 'c:'+pair[0]
                after_ranch = re.sub(r'(\blevels\s*=\s*)1\b',lambda m:m[1]+str(1+PLAN[pair]),ranch,count=1)
                after = before.replace(ranch,after_ranch,1)
            else:
                tag,name = pair
                block = ('\n\t\t\t# Fabric balance: additional simple ranching, local manor ownership.\n'
                         '\t\t\tcreate_building = {\n'
                         '\t\t\t\tbuilding = "building_livestock_ranch"\n'
                         '\t\t\t\tadd_ownership = {\n'
                         '\t\t\t\t\tbuilding = {\n'
                         '\t\t\t\t\t\ttype = "building_manor_house"\n'
                         f'\t\t\t\t\t\tcountry = "c:{tag}"\n'
                         f'\t\t\t\t\t\tlevels = {PLAN[pair]}\n'
                         f'\t\t\t\t\t\tregion = "{name}"\n'
                         '\t\t\t\t\t}\n\t\t\t\t}\n'
                         '\t\t\t\treserves = 1\n'
                         '\t\t\t\tactivate_production_methods = { "pm_open_air_stockyards" "pm_simple_ranch" "pm_standard_fences" "pm_unrefrigerated" }\n'
                         '\t\t\t}\n')
                end = before.rfind('}')
                closing_start = before.rfind('\n',0,end)+1
                assert not before[closing_start:end].strip()
                after = before[:closing_start]+block+before[closing_start:]
            assert updated.count(before) == 1
            updated = updated.replace(before,after,1)
    assert found == set(PLAN), 'Missing existing late-history region'
    diff = list(difflib.unified_diff(original.splitlines(True),updated.splitlines(True),n=8))
    body = ''.join('@@\n' if line.startswith('@@') else line for line in diff[2:])
    return '*** Begin Patch\n*** Update File: '+str(OVERLAY)+'\n'+body+'*** End Patch\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot',type=Path)
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--patch',action='store_true')
    args = parser.parse_args()
    current = baseline_data()
    placement = placements()
    if args.snapshot:
        path = args.snapshot.resolve()
        assert path.is_relative_to(ROOT/'docs/reports/buildings') or path.is_relative_to(ROOT/'.asset-cache')
        assert not path.exists(), 'Do not overwrite a pre-change baseline'
        # Extra capacity is checked before patch generation as well as afterward.
        for row in placement:
            assert row['current_arable_usage']+row['added_levels'] <= row['owned_arable_capacity_floor']
        current['placements'] = placement
        current['nominal_additional_fabric'] = 540
        current['note'] = 'Gross output at full staffing, before subsistence replacement, throughput and other market changes; new campaign required.'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(current,indent=2)+'\n',encoding='utf-8')
    if args.baseline:
        before = json.loads(args.baseline.read_text(encoding='utf-8-sig'))
        for field in ['other_buildings_sha256','history_structure_sha256','protected_files']:
            assert current[field] == before[field], 'Unrequested change: '+field
        for pair,added in PLAN.items():
            key = '|'.join(pair)
            assert current['ranch_levels'][key] == before['ranch_levels'][key]+added, 'Wrong ranch delta: '+key
        for path in sorted(HISTORY.glob('*.txt')):
            for state in history.named_blocks(path,r's:STATE_[A-Za-z0-9_]+',1):
                for region in history.subblocks(state,r'region_state:[A-Za-z0-9_]+'):
                    pair = (region.object_id.split(':')[1],state.object_id.removeprefix('s:'))
                    if pair not in PLAN:
                        continue
                    for created in history.subblocks(region,'create_building'):
                        if history.scalar(created.text,'building') != RANCH:
                            continue
                        assert set(history.tokens_flat(history.braced_tokens(created.text,'activate_production_methods'))) == PMS
                        assert history.scalar(created.text,'country') == 'c:'+pair[0]
                        assert history.scalar(created.text,'region') == pair[1]
    if args.patch:
        assert not args.baseline, 'Patch mode is only for the pre-change tree'
        print(make_patch(),end='')
    else:
        countries = Counter()
        for (tag,_),levels in PLAN.items():
            countries[tag] += levels
        print(json.dumps({'status':'PASS_STATIC_RANCH_INTEGRATION' if args.baseline else 'PASS_STATIC_RANCH_PLAN','added_levels':108,
                          'nominal_gross_fabric':540,'countries':countries,
                          'baseline_verified':bool(args.baseline),'game_tested':False,
                          'placements':placement},indent=2))


if __name__ == '__main__':
    main()
