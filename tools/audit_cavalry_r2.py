"""Read-only inventory and static comparison for the UNAPPLIED cavalry proposal.

No battle outcomes are predicted. Outputs JSON; never modifies the unit file.
"""
from pathlib import Path
import collections
import hashlib
import json
import subprocess

from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized
from map_1776_audit import effective, values
import start_buildings_2026_10_15 as economy

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Games/Victoria 3/game')
REPORT=ROOT/'docs/reports/military/AMERICAN_REVOLUTION_R2'
UNIT_FILE='common/combat_unit_types/00_land_combat_unit_types.txt'

def audit():
    original=json.loads((ROOT/'docs/reports/military/MIL_CAVALRY_AUDIT/STATS.json').read_text())
    proposal=json.loads((ROOT/'docs/reports/military/MIL_CAVALRY_AUDIT/PROPOSAL.json').read_text())['values']
    types=economy.catalog('common/combat_unit_types')
    rows=[]
    for p in effective(ROOT,GAME,'common/history/military_formations'):
        for country in walk(parse(p.read_text(encoding='utf-8-sig'))):
            if not country.key.startswith('c:'):continue
            for f in country.children('create_military_formation'):
                for unit in f.children('combat_unit'):
                    key=scalar(unit.one('type')).split(':')[-1]
                    if key not in original:continue
                    rows.append(dict(tag=country.key[2:],formation=scalar(f.one('name',f.one('save_scope_as','unnamed'))),
                                     state=unit.one('state_region'),type=key,service=unit.one('service_type','regular'),
                                     count=int(unit.one('count')),source=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)))
    counts=collections.Counter();countries=collections.Counter()
    for row in rows:counts[row['type']]+=row['count'];countries[row['tag']]+=row['count']
    current={}
    unchanged={}
    for key,before in original.items():
        n=types[key]
        data={k:n.one(k) for k in ['max_manpower','supply_capacity']}
        for k in ['upkeep_modifier','battle_modifier','formation_modifier']:
            data[k]={x.key:scalar(x.value) for b in n.children(k) for x in b.children()}
        data.update(unlocking_technologies=values(n,'unlocking_technologies'),upgrades=values(n,'upgrades'))
        unchanged[key]=all(data[k]==before[k] for k in data)
        current[key]=data
    checks={
        'current_stats_equal_R1_audit':all(unchanged.values()),
        'regular_battalions_505':sum(row['count'] for row in rows if row['service']=='regular')==505,
        'countries_117':len(countries)==117,
        'no_proposal_installed':all(unchanged.values()),
        'all_unit_definitions_parse':bool(parse((ROOT/UNIT_FILE).read_text(encoding='utf-8-sig'))),
    }
    aggregate={}
    for field in ['unit_offense_add','unit_defense_add']:
        b=sum(counts[key]*float(current[key]['battle_modifier'].get(field,0)) for key in counts)
        a=sum(counts[key]*proposal[key][field] for key in counts)
        aggregate[field]=dict(before=b,after=a,delta=a-b)
    costs={k:original[k]['nominal_base_goods_cost'] for k in counts}
    checks['nominal_goods_cost_unchanged']=sum(counts[k]*costs[k] for k in counts)==32540
    candidate=REPORT/'proposal/00_land_combat_unit_types.txt'
    patch=REPORT/'CAVALRY_P1_ISOLATED.patch'
    if candidate.exists() and patch.exists():
        proposed={n.key:n for n in parse(candidate.read_text(encoding='utf-8-sig'))}
        loaded={n.key:n for n in parse((ROOT/UNIT_FILE).read_text(encoding='utf-8-sig'))}
        checks['proposal.same_unit_identifiers']=set(proposed)==set(loaded)
        checks['proposal.other_units_unchanged']=all(normalized([n])==normalized([proposed[k]]) for k,n in loaded.items() if k not in original)
        checks['proposal.lancers_unchanged']=normalized([loaded['combat_unit_type_lancers']])==normalized([proposed['combat_unit_type_lancers']])
        for key,n in proposed.items():
            if key not in original:continue
            ignore={'battle_modifier','supply_capacity'}
            checks['proposal.'+key+'.cost_tech_mobility_unchanged']=normalized([x for x in n.children() if x.key not in ignore])==normalized([x for x in loaded[key].children() if x.key not in ignore])
            expected=proposal[key]
            bm={x.key:float(x.value) for b in n.children('battle_modifier') for x in b.children()}
            checks['proposal.'+key+'.exact_P1_stats']=all((float(n.one('supply_capacity')) if f=='supply_capacity' else bm.get(f,0))==v for f,v in expected.items())
            untouched=set(original[key]['battle_modifier'])-set(expected)
            checks['proposal.'+key+'.other_combat_effects_unchanged']=all(bm[k]==float(original[key]['battle_modifier'][k]) for k in untouched)
        result=subprocess.run(['git','apply','--check',str(patch)],cwd=ROOT,capture_output=True,text=True)
        checks['proposal.patch_applies_cleanly_without_applying']=result.returncode==0
    return dict(status='DESIGN_ONLY',patch_applied=False,runtime_executed=False,
                unit_file=UNIT_FILE,unit_file_sha256=hashlib.sha256((ROOT/UNIT_FILE).read_bytes()).hexdigest(),
                checks=checks,passed=sum(checks.values()),failed=[k for k,v in checks.items() if not v],
                countries=len(countries),battalions=sum(counts.values()),contingents=len(rows),
                formations=len({(r['source'],r['tag'],r['formation']) for r in rows}),
                counts=dict(counts),top_countries=countries.most_common(12),current=current,
                proposal=proposal,aggregate_metrics_not_battle_results=aggregate,
                nominal_goods_cost=sum(counts[k]*costs[k] for k in counts),exposure=rows)

if __name__=='__main__':
    data=audit()
    print(json.dumps(data,ensure_ascii=False,indent=2))
    raise SystemExit(0 if not data['failed'] else 1)
