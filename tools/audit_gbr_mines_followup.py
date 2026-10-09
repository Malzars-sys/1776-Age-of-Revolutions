"""Plan/check British starting mine pumps and eight additional iron levels."""
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
import build_start_1776_runtime_wave1 as numbers

ROOT=world.ROOT
CACHE=ROOT/'.asset-cache/oct09_balance_revision'
RECORD=CACHE/'gbr_mines_followup.json'
ADDED={'STATE_YORKSHIRE':4,'STATE_MIDLANDS':4}
KINDS={'building_iron_mine','building_coal_mine'}

def prepare():
    assert not RECORD.exists(), 'Preserve the existing follow-up reference'
    raws,placements=world.all_placements(world.HISTORY)
    rows=[p for p in placements if p.owner=='GBR' and p.building in KINDS]
    last={p.key:p for p in rows}
    changes=collections.defaultdict(list);report=[]
    for p in rows:
        family='iron' if p.building=='building_iron_mine' else 'coal'
        equipment='pm_atmospheric_engine_pump_building_'+family+'_mine'
        pms=[equipment if re.fullmatch(r'pm_(picks_and_shovels|atmospheric_engine_pump|condensing_engine_pump|diesel_pump)_building_'+family+'_mine',pm) else pm for pm in p.pms]
        assert equipment in pms, ('Base mine equipment not recognized',p.key,p.pms)
        updated=world.replace_active_pms(p.text,pms)
        n=ADDED.get(p.state,0) if p.building=='building_iron_mine' and last[p.key] is p else 0
        if n:
            updated=world.rescale_ownership(updated,p.level+n)
            report.append({'state':p.state,'before':p.level,'after':p.level+n,'added':n})
        if updated!=p.text:changes[p.path].append((p.start,p.end,updated))
    assert sum(r['added'] for r in report)==8
    previous=json.loads((CACHE/'crew_ceiling.json').read_text(encoding='utf-8'))['expected']
    before={};expected={};hashes={}
    for path,edits in changes.items():
        rel=path.relative_to(ROOT).as_posix()
        raw=raws[path]
        assert raw==previous[rel], 'Pre-mine revision differs from the validated preceding revision'
        before[rel]=raw;hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
        for a,b,t in sorted(edits,reverse=True):raw=raw[:a]+t+raw[b:]
        expected[rel]=raw
    record={'before':before,'before_sha256':hashes,'expected':expected,'iron_levels':report,
            'deficit_seen':278,'base_extra_iron':320,'base_extra_tools':80,'base_extra_coal':80,
            'request':'British iron/coal mines start with atmospheric pumps; add eight iron levels in valid resource states.'}
    RECORD.write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    patch='*** Begin Patch\n'
    for rel,new in expected.items():
        actual=(ROOT/rel).read_text(encoding='utf-8')
        desired=('\ufeff' if actual.startswith('\ufeff') else '')+new
        patch+='*** Update File: '+rel+'\n'
        for line in list(difflib.unified_diff(actual.splitlines(),desired.splitlines(),n=40))[2:]:
            patch+=('@@' if line.startswith('@@') else line.rstrip('\n'))+'\n'
    print(json.dumps({'patch':patch+'*** End Patch','report':report},ensure_ascii=True))

def check(quiet=False):
    record=json.loads(RECORD.read_text(encoding='utf-8'))
    expected_current=record['expected'].copy()
    successor=CACHE/'gbr_agriculture_followup.json'
    approved=None
    if successor.exists():
        import audit_gbr_agriculture_followup as agriculture
        approved=agriculture.check(quiet=True)
        for rel,expected in record['expected'].items():
            if rel in approved['before']:
                assert approved['before'][rel]==expected, 'Agriculture preceding mine reference mismatch '+rel
                expected_current[rel]=approved['expected'][rel]
    for rel,expected in expected_current.items():
        assert (ROOT/rel).read_text(encoding='utf-8-sig')==expected, 'Unexpected edit '+rel
        cat.brace_maps(cat.clean_comments(expected))
    _,placements=world.all_placements(world.HISTORY)
    rows=[p for p in placements if p.owner=='GBR' and p.building in KINDS]
    for p in rows:
        family='iron' if p.building=='building_iron_mine' else 'coal'
        assert 'pm_atmospheric_engine_pump_building_'+family+'_mine' in p.pms, p.key
    assert 'atmospheric_engine' in naval.technology_sets()['GBR']
    states=cat.effective_objects('map_data/state_regions',r'STATE_[A-Za-z0-9_]+')
    last={p.key:p for p in rows}
    for item in record['iron_levels']:
        p=last['GBR',item['state'],'building_iron_mine']
        after=item['after']
        if approved:
            change=next((r for r in approved['levels'] if r['key']==['GBR',item['state'],'building_iron_mine']),None)
            if change:
                assert change['before']==after
                after=change['after']
        assert p.level==after
        resources=dict(re.findall(r'(building_\w+)\s*=\s*(\d+)',states[p.state].text))
        assert p.level<=int(resources.get('building_iron_mine',0)), 'Iron resource cap exceeded'
    pms=cat.effective_objects('common/production_methods',r'[A-Za-z0-9_]+')
    assert numbers.number(pms['pm_atmospheric_engine_pump_building_iron_mine'].text,'goods_output_iron_add')==40
    result={'status':'PASS_GBR_MINE_FOLLOWUP','iron_levels_added':8,'extra_base_iron':320,
            'extra_base_tools':80,'extra_base_coal':80,'engine_tested':False,
            'subsequent_agricultural_rebalancing':approved is not None}
    if not quiet:print(json.dumps(result))
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');args=parser.parse_args()
    prepare() if args.prepare else check()
