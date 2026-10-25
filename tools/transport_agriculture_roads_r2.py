"""Apply/check the authorized 5/10/15 ticket targets and agricultural transport.

Default: read-only gameplay validation and reports. --apply captures the current
workspace first, then edits only the road recipes and farms missing transport.
"""
from copy import deepcopy
from pathlib import Path
import argparse
import json
import re
import shutil

import audit_anzin_regional_infrastructure as prior
from validate_diplomacy_ottoman_1776 import parse, normalized

ROOT,GAME=prior.ROOT,prior.GAME
REPORT=ROOT/'docs/reports/economy/TRANSPORT_AGRICULTURE_ROADS_R2'
ROADS=prior.ROADS
FARMS='common/buildings/02_agro.txt'
OWN=[ROADS,FARMS]
TARGETS={'pm_turnpike_road_network':5,'pm_engineered_road_network':10,'pm_paved_road_network':15}
PMG=prior.PMG


def dump(name,data):
    (REPORT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def raw(rel):return prior.raw(ROOT/rel)
def transport_groups(node,groups):
    result=[]
    for key in prior.ids(node,'production_method_groups'):
        pms=prior.ids(groups[key][0],'production_methods')
        if any(s in key for s in ['transport','train']) or any(
            'transport' in pm or pm=='pm_road_carts' for pm in pms):result.append(key)
    return result
def agriculture():
    groups=prior.catalog('common/building_groups');pmgs=prior.catalog('common/production_method_groups');rows=[]
    for key,(node,path) in prior.catalog('common/buildings').items():
        parents=prior.chain(node.one('building_group'),groups)
        if not set(parents)&{'bg_agriculture','bg_ranching','bg_plantations'}:continue
        if node.one('buildable')=='no':continue
        if any(groups[g][0].one('is_government_funded')=='yes' for g in parents):continue
        rows.append(dict(key=key,file=path.relative_to(ROOT).as_posix(),transport=transport_groups(node,pmgs)))
    return rows


def apply():
    assert not REPORT.exists(),'Baseline exists: do not replace it.'
    rows=agriculture();missing=[r for r in rows if not r['transport']]
    assert len(missing)==6 and {r['file'] for r in missing}=={FARMS}
    REPORT.mkdir(parents=True)
    for rel in OWN:
        dest=REPORT/'baseline'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
    protected={p.relative_to(ROOT).as_posix():prior.sha(p) for folder in ['common','events','gui','gfx','localization','map_data']
               for p in (ROOT/folder).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in OWN}
    base=dict(git=prior.git_state(),owned={rel:prior.sha(ROOT/rel) for rel in OWN},protected=protected,
              agriculture_before=rows,added=[r['key'] for r in missing],road_recipes_before={n.key:prior.recipe(n) for n in parse(raw(ROADS))})
    dump('BASELINE.json',base)
    changes={};text=raw(ROADS);edits=[]
    for node in parse(text):
        if node.key not in TARGETS:continue
        value=node.children('building_modifiers')[0].children('workforce_scaled')[0].children('goods_output_transportation_add')[0]
        match=re.search(re.escape(value.value)+r'$',text[value.start:value.end]);assert match
        edits.append((value.start+match.start(),value.end,str(TARGETS[node.key])))
    assert len(edits)==3
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    changes[ROADS]=text
    text=raw(FARMS);nodes={n.key:n for n in parse(text)};eol='\r\n' if '\r\n' in text else '\n'
    for row in sorted(missing,key=lambda r:nodes[r['key']].start,reverse=True):
        block=nodes[row['key']].children('production_method_groups')[0]
        pos=text.rfind(eol,block.start,block.end)+len(eol)
        indent=re.search(r'(?m)^([ \t]+)\S',text[block.start:block.end]).group(1)
        text=text[:pos]+indent+PMG+eol+text[pos:]
    changes[FARMS]=text
    assert all(prior.sha(ROOT/rel)==h for rel,h in base['owned'].items()),'Concurrent edit in an owned source'
    for rel,text in changes.items():
        bom=b'\xef\xbb\xbf' if (ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf') else b''
        (ROOT/rel).write_bytes(bom+text.encode('utf-8'))


def check():
    base=json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'));checks={}
    def test(name,value):checks[name]=bool(value)
    roads=parse(raw(ROADS));old_roads=parse(prior.raw(REPORT/'baseline'/ROADS))
    road_stats={n.key:prior.recipe(n) for n in roads}
    for key,value in TARGETS.items():test('roads.ticket_target.'+key,road_stats[key]['outputs']['transportation']==str(value))
    restored=deepcopy(roads)
    for node in restored:
        if node.key in TARGETS:
            old=base['road_recipes_before'][node.key]['outputs']['transportation']
            node.children('building_modifiers')[0].children('workforce_scaled')[0].children('goods_output_transportation_add')[0].value=old
    test('roads.only_three_output_values_changed',normalized(restored)==normalized(old_roads))
    test('roads.dirt_keeps_400_jobs_and_no_tickets',road_stats[prior.ROAD_KEYS[0]]['jobs']=={'laborers':'360','clerks':'40'} and not road_stats[prior.ROAD_KEYS[0]]['outputs'])
    current=agriculture();by_key={r['key']:r for r in current}
    for row in base['agriculture_before']:
        test('coverage.transport_available.'+row['key'],bool(by_key[row['key']]['transport']))
        if row['key'] in base['added']:test('coverage.single_new_group.'+row['key'],by_key[row['key']]['transport']==[PMG])
        else:test('coverage.existing_variant_preserved.'+row['key'],by_key[row['key']]['transport']==row['transport'])
    test('coverage.exact_six_missing_farms_completed',set(base['added'])=={'building_rye_farm','building_wheat_farm','building_rice_farm','building_maize_farm','building_millet_farm','building_livestock_ranch'})
    stripped=re.sub(r'(?m)^[ \t]*'+re.escape(PMG)+r'\r?\n','',raw(FARMS))
    test('farms.only_new_group_lines_changed',stripped==prior.raw(REPORT/'baseline'/FARMS))
    # No independent copies of the recipes: existing mine PMs and their gates
    # remain the source of truth for both farms and the previous urban lot.
    groups=prior.catalog('common/production_method_groups');methods=prior.catalog('common/production_methods')
    test('transport.same_mine_pm_list',prior.ids(groups[PMG][0],'production_methods')==prior.ids(groups['pmg_train_automation_building_coal_mine'][0],'production_methods'))
    test('transport.neutral_cart_default',prior.ids(groups[PMG][0],'production_methods')[0]=='pm_road_carts')
    test('transport.railways_gate_preserved',prior.ids(methods['pm_rail_transport_mine'][0],'unlocking_technologies')==['railways'])
    test('transport.native_coefficients',prior.recipe(methods['pm_rail_transport_mine'][0])['inputs']=={'transportation':'5'}
         and prior.recipe(methods['pm_rail_transport_mine'][0])['jobs']=={'laborers':'-1000'})
    buildings=prior.catalog('common/buildings')
    test('urban_center.own_transport_unchanged',PMG not in prior.ids(buildings['building_urban_center'][0],'production_method_groups')
         and 'pmg_public_transport' in prior.ids(buildings['building_urban_center'][0],'production_method_groups'))
    test('ports.excluded',PMG not in prior.ids(buildings['building_port'][0],'production_method_groups'))
    test('industry.existing_twenty_untouched',all(PMG in prior.ids(buildings[r['key']][0],'production_method_groups') for r in prior.targets()))
    changed=[rel for rel,h in base['protected'].items() if prior.sha(ROOT/rel)!=h]
    test('preservation.all_other_gameplay_map_art',not changed)
    test('preservation.git_no_write',base['git']==prior.git_state())
    # The prior reference model, with only the three authorized outputs replaced.
    economics=json.loads((prior.REPORT/'ECONOMICS.json').read_text(encoding='utf-8'))
    reference=[]
    for key in prior.ROAD_KEYS:
        old=next(r for r in economics['pm_modules'] if r['method']==key and r['version']=='after')
        output=float(road_stats[key]['outputs'].get('transportation',0));revenue=output*30
        balance=revenue-old['wages']-old['inputs_cost']
        reference.append(dict(method=key,previous_tickets=old['transportation'],tickets=output,wages=old['wages'],inputs_cost=old['inputs_cost'],
            revenue=revenue,weekly_balance=balance,weekly_deficit_proxy=max(0,-balance)))
    dump('REFERENCE_ECONOMICS.json',dict(reference=reference,live_market_prices=None,
        note='Fixed reference prices/wages from R1; operating balance only, not observed subsidies or a market simulation.'))
    result=dict(status='PASS_STATIC' if all(checks.values()) else 'FAIL_STATIC',passed=sum(checks.values()),total=len(checks),
        failed=[k for k,v in checks.items() if not v],checks=checks,agriculture=current,added=base['added'],
        protected_file_count=len(base['protected']),changed_protected=changed,runtime='NOT_RUN',
        source_sha256={rel:prior.sha(ROOT/rel) for rel in OWN})
    dump('VALIDATION.json',result)
    print(json.dumps({k:result[k] for k in ['status','passed','total','failed','added','protected_file_count','changed_protected','runtime']},indent=2))
    return 0 if all(checks.values()) else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    if args.apply:apply()
    raise SystemExit(check())
