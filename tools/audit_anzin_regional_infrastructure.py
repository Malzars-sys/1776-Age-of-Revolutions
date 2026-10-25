"""Scoped Anzin/road/industrial-transport audit. Never writes gameplay files.

--capture freezes the current sources before the authorized patch. --validate
checks that patch and writes economic estimates, not simulated game outcomes.
All game references use the repository's canonical local installation.
"""
from copy import deepcopy
from decimal import Decimal as D
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import itertools
import json
import re
import shutil
import subprocess

from PIL import Image
from validate_diplomacy_ottoman_1776 import parse, normalized
from localization_duplicate_audit import entries

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Games/Victoria 3/game')
REPORT=ROOT/'docs/reports/economy/ANZIN_REGIONAL_INFRASTRUCTURE_R1'
COMPANY='common/company_types/00_companies_france.txt'
ROADS='common/production_methods/22_tech7a_wave_a_land_transport_production.txt'
FACTORIES=['common/buildings/01_industry.txt',
           'common/buildings/11_tech6c1b_cement_works.txt',
           'common/buildings/12_tech6c4_oil_refinery.txt',
           'common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt']
OWN=[COMPANY,ROADS]+FACTORIES
PMG='pmg_aor1776_industrial_transport'
PG='prestige_good_aor1776_anzin_coking_coal'
NEW_GROUP='common/production_method_groups/1776_industrial_transport.txt'
NEW_GOOD='common/prestige_goods/1776_anzin_coking_coal.txt'
ICON='gfx/interface/icons/goods_icons/prestige_goods/1776_anzin_coking_coal.dds'
MASTER='workshop_assets/source/anzin_coking_coal.png'
ROAD_KEYS=['pm_traditional_road_network','pm_turnpike_road_network',
           'pm_engineered_road_network','pm_paved_road_network']
GROUPS=['pmg_base_building_land_transport_network','pmg_land_transport_canals',
        'pmg_base_building_railway','pmg_passenger_trains']
NEW=[NEW_GROUP,NEW_GOOD,ICON,MASTER]+[
    f'localization/{lang}/1776_anzin_regional_transport_l_{lang}.yml'
    for lang in ['french','english']]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def raw(path): return path.read_bytes().decode('utf-8-sig')
def dump(name,obj):
    (REPORT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def catalog(folder):
    files={p.name:p for p in (GAME/folder).glob('*.txt')}
    files.update({p.name:p for p in (ROOT/folder).glob('*.txt')})
    result={}
    for name,path in sorted(files.items()):
        for node in parse(raw(path)):
            if isinstance(node.value,list):
                result[node.key.removeprefix('REPLACE_OR_CREATE:')]=(node,path)
    return result
def ids(node,key): return [v.value for block in node.children(key) for v in block.children()]
def chain(key,groups):
    result=[]
    while key:
        assert key not in result
        result.append(key);key=groups[key][0].one('parent_group')
    return result
def targets():
    groups=catalog('common/building_groups');result=[]
    for key,(node,path) in catalog('common/buildings').items():
        parents=chain(node.one('building_group'),groups)
        if 'bg_manufacturing' in parents:
            result.append(dict(key=key,file=path.relative_to(ROOT).as_posix(),groups=parents))
    return result
def recipe(node):
    result=dict(jobs={},inputs={},outputs={},state={},country={},gates=ids(node,'unlocking_technologies'))
    for kind in ['building_modifiers','state_modifiers','country_modifiers']:
        for block in node.children(kind):
            for scale in block.children():
                for item in scale.children():
                    try: value=D(item.value)
                    except Exception: continue
                    if kind=='building_modifiers':
                        if item.key.startswith('building_employment_'):
                            result['jobs'][item.key[20:-4]]=str(value)
                        elif item.key.startswith('goods_input_'):
                            result['inputs'][item.key[12:-4]]=str(value)
                        elif item.key.startswith('goods_output_'):
                            result['outputs'][item.key[13:-4]]=str(value)
                    else: result['state' if kind=='state_modifiers' else 'country'][scale.key+':'+item.key]=str(value)
    return result
def recipes():
    methods=catalog('common/production_methods');groups=catalog('common/production_method_groups')
    return {key:dict(group=group,source=str(methods[key][1]),**recipe(methods[key][0]))
            for group in GROUPS for key in ids(groups[group][0],'production_methods')}
def git_state():
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    return dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=sha(ROOT/'.git/index'))


def capture():
    assert not (REPORT/'BASELINE.json').exists(),'Use the existing baseline; never overwrite it.'
    REPORT.mkdir(parents=True,exist_ok=True)
    for rel in OWN:
        dest=REPORT/'baseline'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
    folders=['common','events','gui','gfx','localization','map_data','history']
    existing={p.relative_to(ROOT).as_posix():sha(p) for folder in folders for p in (ROOT/folder).rglob('*') if p.is_file()}
    native={str(path.relative_to(GAME)):sha(path) for folder in [
        'common/company_types','common/production_methods','common/production_method_groups',
        'common/buildings','common/building_groups','common/goods','common/pop_types','common/defines']
        for path in (GAME/folder).glob('*') if path.is_file()}
    assert all(not (ROOT/rel).exists() for rel in NEW),'New path already exists.'
    source=Path('C:/Users/simeo/.codex/attachments/bf201119-67b1-4b29-a997-79ec95aadd37/Texte collé.txt')
    shutil.copy2(source,REPORT/'USER_MISSION.txt')
    before=recipes()
    dump('BASELINE.json',dict(utc=datetime.now(timezone.utc).isoformat(),git=git_state(),owned={p:existing[p] for p in OWN},
        protected={p:h for p,h in existing.items() if p not in OWN},native=native,new=NEW,targets=targets()))
    dump('PM_BEFORE.json',before)
    dump('COMPANY_BEFORE.json',dict(key='company_mines_anzin',
        main=ids(catalog('common/company_types')['company_mines_anzin'][0],'building_types'),
        extension=ids(catalog('common/company_types')['company_mines_anzin'][0],'extension_building_types')))
    print(json.dumps(dict(status='CAPTURED_BEFORE_PATCH',infrastructure_methods=len(before),industries=len(targets()),protected=len(existing)-len(OWN)),indent=2))


def economic():
    before=json.loads((REPORT/'PM_BEFORE.json').read_text(encoding='utf-8'));after=recipes()
    goods=catalog('common/goods');pops=catalog('common/pop_types')
    prices={k:D(n.one('cost')) for k,(n,p) in goods.items() if n.one('cost')}
    weights={k:D(n.one('wage_weight','0')) for k,(n,p) in pops.items()}
    def balance(r,wage=D(500),price=D(1),staff=D(1),throughput=D(1),input_price=D(1)):
        wage_bill=sum(D(v)*weights[k] for k,v in r['jobs'].items())*wage/D(10000)*staff
        inputs=sum(D(v)*prices[k]*input_price for k,v in r['inputs'].items())*staff*throughput
        revenue=sum(D(v)*prices[k]*(price if k=='transportation' else 1) for k,v in r['outputs'].items())*staff*throughput
        return dict(employees=float(sum(map(D,r['jobs'].values()))*staff),wages=float(wage_bill),
            inputs_cost=float(inputs),revenue=float(revenue),balance=float(revenue-inputs-wage_bill),
            operating_deficit_proxy=float(max(D(0),inputs+wage_bill-revenue)))
    pm_rows=[]
    for key in before:
        for version,data in [('before',before),('after',after)]:
            r=data[key];row=dict(method=key,group=r['group'],version=version,**balance(r),
                jobs=json.dumps(r['jobs'],ensure_ascii=False),inputs=json.dumps(r['inputs'],ensure_ascii=False),
                transportation=float(D(r['outputs'].get('transportation','0'))),other_effects=json.dumps(r['state'],ensure_ascii=False))
            pm_rows.append(row)
    # Reference scenarios, explicitly not measured saves or equilibrium forecasts.
    scenarios=[('reference',0,500,1,1),('dense_region_high_wages',3000000,900,1,1),
               ('rural_region',200000,300,1,1),('high_transport_demand',1500000,500,1.5,1),
               ('low_transport_demand',200000,300,.5,1),('high_demand_cheap_inputs',1500000,500,1.5,.75)]
    rows=[]
    for name,population,wage,price,input_price in scenarios:
        for staffing in [D(1),D('.5')]:
            for throughput in [D(1),D('1.1')]:
                for key in ROAD_KEYS:
                    for version,data in [('before',before),('after',after)]:
                        rows.append(dict(scenario=name,population=population,wage_per_10000=wage,transport_price_factor=price,
                            input_price_factor=input_price,staffing=float(staffing),throughput=float(throughput),method=key,version=version,
                            **balance(data[key],D(str(wage)),D(str(price)),staffing,throughput,D(str(input_price)))))
    # Demand cannot be inferred from recipe quantities: stress test a price fall.
    sensitivity=[]
    for drop in [D(0),D('.1'),D('.25'),D('.375'),D('.5')]:
        key=ROAD_KEYS[1];a=balance(before[key]);b=balance(after[key],price=1-drop)
        sensitivity.append(dict(price_drop_after_extra_supply=float(drop),before=a,after=b))
    dump('PM_AFTER.json',after)
    dump('ECONOMICS.json',dict(reference_prices={k:str(prices[k]) for k in ['transportation','wood','tools','limestone','cement','heavy_petroleum_products']},
        wage_weights={k:str(weights[k]) for k in ['laborers','clerks','bureaucrats','machinists','engineers']},
        wage_formula='sum(employees * native wage_weight) * weekly wage_rate_per_10000 / 10000',
        pm_modules=pm_rows,scenarios=rows,price_sensitivity=sensitivity,observed_market_prices=None,
        limitations='Operating deficit proxy only, before reserves, profits, wage adjustment, native hiring, subsidies, taxes or market equilibrium. Population labels do not compute market prices.'))
    for name,data in [('PM_COMPARISON.csv',pm_rows),('SCENARIOS.csv',rows)]:
        with (REPORT/name).open('w',newline='',encoding='utf-8-sig') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    return before,after,pm_rows,rows


def employment_sensitivity():
    methods=catalog('common/production_methods');groups=catalog('common/production_method_groups');buildings=catalog('common/buildings')
    rows=[]
    for target in targets():
        node=buildings[target['key']][0]
        choices=[ids(groups[g][0],'production_methods') for g in ids(node,'production_method_groups') if g!=PMG]
        needed={pm:set(ids(methods[pm][0],'unlocking_production_methods')) for group in choices for pm in group}
        labor={pm:D(recipe(methods[pm][0])['jobs'].get('laborers','0')) for group in choices for pm in group}
        best=None;count=0
        for combo in itertools.product(*choices):
            selected=set(combo)
            if any(not needed[pm]<=selected for pm in combo):continue
            val=sum(labor[pm] for pm in combo);count+=1
            if best is None or val<best[0]:best=(val,combo)
        assert best is not None
        rows.append(dict(building=target['key'],minimum_raw_laborer_coefficient_before=str(best[0]),
            after_rail=str(best[0]-1000),negative_before=best[0]<0,negative_after=best[0]<1000,
            combination=list(best[1]),combinations_checked=count,
            caveat='All technologies presumed available; PM dependencies checked, laws and native employment flooring not executed.'))
    dump('INDUSTRIAL_EMPLOYMENT_SENSITIVITY.json',rows)
    return rows


def validate():
    base=json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'));checks={}
    def check(name,ok):checks[name]=bool(ok)
    companies=catalog('common/company_types');company=companies['company_mines_anzin'][0]
    old_companies=parse(raw(REPORT/'baseline'/COMPANY));now_companies=parse(raw(ROOT/COMPANY))
    old=next(n for n in old_companies if n.key=='company_mines_anzin')
    old_text=raw(REPORT/'baseline'/COMPANY);new_text=raw(ROOT/COMPANY)
    check('anzin.all_bytes_outside_company_block_preserved',
          old_text[:old.start]==new_text[:company.start] and old_text[old.end:]==new_text[company.end:])
    check('anzin.main_coal_and_regional_infrastructure',ids(company,'building_types')==['building_coal_mine','building_railway'])
    check('anzin.iron_remains_extension',ids(company,'extension_building_types')==['building_iron_mine'])
    check('anzin.prestige_good_link',ids(company,'possible_prestige_goods')==[PG])
    restored=deepcopy(now_companies);restored_anzin=next(n for n in restored if n.key==company.key)
    restored_anzin.value[:]=[n for n in restored_anzin.children() if n.key not in ['building_types','possible_prestige_goods']]
    old.value[:]=[n for n in old.children() if n.key not in ['building_types','possible_prestige_goods']]
    check('anzin.other_characteristics_and_all_other_companies_preserved',normalized(restored)==normalized(old_companies))
    check('anzin.no_new_railway_gate_in_company',not company.children('prestige_goods_trigger') and normalized(company.children('possible'))==normalized(old.children('possible')))
    roads=parse(raw(ROOT/ROADS));oldroads=parse(raw(REPORT/'baseline'/ROADS))
    data={n.key:recipe(n) for n in roads}
    check('roads.dirt_60_percent_jobs_reduction',data[ROAD_KEYS[0]]['jobs']=={'laborers':'360','clerks':'40'})
    check('roads.dirt_no_new_tickets_or_inputs',not data[ROAD_KEYS[0]]['outputs'] and not data[ROAD_KEYS[0]]['inputs'])
    check('roads.turnpike_output_60_percent_increase',D(data[ROAD_KEYS[1]]['outputs']['transportation'])==D('3.2'))
    restored=deepcopy(roads)
    for n in restored:
        if n.key==ROAD_KEYS[0]:
            for job in n.children('building_modifiers')[0].children('level_scaled')[0].children():
                job.value={'building_employment_laborers_add':'900','building_employment_clerks_add':'100'}[job.key]
        elif n.key==ROAD_KEYS[1]:
            n.children('building_modifiers')[0].children('workforce_scaled')[0].children('goods_output_transportation_add')[0].value='2'
    check('roads.only_three_numeric_tokens_changed',normalized(restored)==normalized(oldroads))
    groups=catalog('common/building_groups');buildings=catalog('common/buildings');pmgs=catalog('common/production_method_groups');pms=catalog('common/production_methods')
    check('transport.same_exact_methods_as_mines',ids(pmgs[PMG][0],'production_methods')==ids(pmgs['pmg_train_automation_building_coal_mine'][0],'production_methods'))
    check('transport.mine_pm_sources_untouched',sha(ROOT/'common/production_methods/03_mines.txt')==base['protected']['common/production_methods/03_mines.txt'])
    check('transport.same_railway_technology',ids(pms['pm_rail_transport_mine'][0],'unlocking_technologies')==['railways'])
    check('transport.cart_default_is_neutral',not pms['pm_road_carts'][0].children('building_modifiers') and ids(pmgs[PMG][0],'production_methods')[0]=='pm_road_carts')
    current_targets=targets();check('transport.twenty_manufacturing_buildings',len(current_targets)==20)
    for target in current_targets:
        n=buildings[target['key']][0];check('transport.single_group.'+n.key,ids(n,'production_method_groups').count(PMG)==1)
        check('transport.not_government_funded.'+n.key,all(groups[k][0].one('is_government_funded')!='yes' for k in target['groups']))
    for rel in FACTORIES:
        current=parse(raw(ROOT/rel));previous=parse(raw(REPORT/'baseline'/rel))
        for n in current:
            for block in n.children('production_method_groups'):block.value[:]=[x for x in block.children() if x.value!=PMG]
        check('transport.only_group_added_to_factory_file.'+rel,normalized(current)==normalized(previous))
        stripped=re.sub(r'(?m)^[\t ]*'+re.escape(PMG)+r'\r?\n','',raw(ROOT/rel))
        check('transport.factory_bytes_outside_added_line_preserved.'+rel,stripped==raw(REPORT/'baseline'/rel))
    for key,(n,path) in buildings.items():
        c=chain(n.one('building_group'),groups)
        if any(groups[g][0].one('is_government_funded')=='yes' for g in c):
            check('transport.government_excluded.'+key,PMG not in ids(n,'production_method_groups'))
    regional=buildings['building_railway'][0]
    check('regional.same_single_building',ids(regional,'aliases')==['building_land_transport_network'] and not regional.children('unlocking_technologies'))
    check('regional.private_funding_model_preserved',groups['bg_land_transport_network'][0].one('parent_group')=='bg_private_infrastructure')
    prior_recipes=json.loads((REPORT/'PM_BEFORE.json').read_text(encoding='utf-8'))
    # The installed railway methods have different gates: railways, steel
    # railway cars, electric railway, or compression ignition. Do not assume
    # every method repeats the same key; preserve the actual technology gates.
    rail_gates=set()
    for key in ids(pmgs['pmg_base_building_railway'][0],'production_methods')[1:]:
        gates=ids(pms[key][0],'unlocking_technologies');rail_gates.update(gates)
        check('regional.operational_rail_remains_gated.'+key,bool(gates) and gates==prior_recipes[key]['gates'])
    inventions={n.key:n for n in parse(raw(ROOT/'common/scripted_effects/00_starting_inventions.txt'))}
    def starting_techs(nodes):
        result=set()
        for n in nodes:
            if n.key=='add_technology_researched':result.add(n.value)
            elif n.key in inventions:result.update(starting_techs(inventions[n.key].children()))
            elif isinstance(n.value,list):result.update(starting_techs(n.children()))
        return result
    french_techs=starting_techs(parse(raw(ROOT/'common/history/countries/fra - france.txt')))
    check('anzin.france_cannot_activate_modern_rail_in_1776',not rail_gates&french_techs)
    prestige=catalog('common/prestige_goods')[PG][0]
    check('prestige.coal_native_bonus',prestige.one('base_good')=='coal' and prestige.one('prestige_bonus')=='0.1')
    check('prestige.supplied_icon_referenced',prestige.one('texture')=='"'+ICON+'"')
    source=Image.open(ROOT/MASTER);icon=Image.open(ROOT/ICON)
    check('prestige.native_size_alpha_mips',icon.size==(256,256) and icon.mode=='RGBA' and int.from_bytes((ROOT/ICON).read_bytes()[28:32],'little')==9)
    check('prestige.transparent_corners',all(icon.getpixel(p)[3]==0 for p in [(0,0),(255,0),(0,255),(255,255)]))
    check('prestige.original_preserved',source.size==(1254,1254) and sha(ROOT/MASTER)==sha(Path('C:/Users/simeo/AppData/Local/Temp/codex-clipboard-b11ec85a-194a-4c70-b507-9acf17e08643.png')))
    locsets=[]
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_anzin_regional_transport_l_{lang}.yml';text=raw(p);catalogue=entries(lang)
        keys=set(re.findall(r'(?m)^ ([A-Za-z0-9_]+):0 "[^"\n]*"',text));locsets.append(keys)
        check('localization.complete_unique_BOM.'+lang,keys=={PMG,PG} and all(len(catalogue[k])==1 for k in keys) and p.read_bytes().startswith(b'\xef\xbb\xbf'))
    check('localization.FR_EN_same_keys',locsets[0]==locsets[1])
    changed=[rel for rel,h in base['protected'].items() if sha(ROOT/rel)!=h]
    # Accept only separately evidenced changes from the concurrent territorial
    # task, with its exact current hashes. Never restore those files or quietly
    # exclude paths from preservation checks.
    concurrent_path=REPORT/'CONCURRENT_WORK_OBSERVED.json'
    concurrent=json.loads(concurrent_path.read_text(encoding='utf-8')) if concurrent_path.exists() else {}
    recognized=concurrent.get('files',{})
    unexpected=[rel for rel in changed if rel not in recognized
                or recognized[rel]['baseline_sha256']!=base['protected'][rel]
                or recognized[rel]['observed_sha256']!=sha(ROOT/rel)]
    check('preservation.no_unexplained_external_edits',not unexpected)
    check('preservation.native_read_only',all(sha(GAME/rel)==h for rel,h in base['native'].items()))
    check('preservation.git_no_write',git_state()==base['git'])
    before,after,pmrows,scenarios=economic();employment=employment_sensitivity()
    for key in before:
        if key not in ROAD_KEYS[:2]:check('economic.all_other_pm_modules_unchanged.'+key,before[key]==after[key])
    check('economic.full_and_half_staffing_tested',{r['staffing'] for r in scenarios}=={.5,1})
    check('economic.anzin_throughput_tested',{r['throughput'] for r in scenarios}=={1,1.1})
    result=dict(status='PASS_STATIC_WITH_RUNTIME_OPEN_ITEMS' if all(checks.values()) else 'FAIL_STATIC',
        passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v],checks=checks,
        protected_file_count=len(base['protected']),changed_protected=changed,
        concurrent_changes_evidenced=[rel for rel in changed if rel not in unexpected],unexplained_changes=unexpected,
        industries=current_targets,
        economic_scenarios=len(scenarios),native_methods_audited=len(before),runtime='NOT_RUN',
        industrial_employment_raw_coefficient_risks=dict(negative_before=sum(r['negative_before'] for r in employment),negative_after=sum(r['negative_after'] for r in employment)),
        observed_market_prices='UNAVAILABLE_BINARY_SAVE',subsidies='MODELED_OPERATING_DEFICIT_ONLY',
        source_sha256={rel:sha(ROOT/rel) for rel in OWN+NEW})
    dump('VALIDATION.json',result)
    print(json.dumps({k:result[k] for k in ['status','passed','total','failed','protected_file_count','changed_protected','economic_scenarios','native_methods_audited','industrial_employment_raw_coefficient_risks','runtime']},indent=2))
    return 0 if all(checks.values()) else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--capture',action='store_true');parser.add_argument('--validate',action='store_true');args=parser.parse_args()
    if args.capture:capture()
    elif args.validate:raise SystemExit(validate())
    else:print(json.dumps(recipes(),ensure_ascii=False,indent=2))
