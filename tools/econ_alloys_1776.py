"""Read-only gameplay inventory and generated reports for ECON-ALLOYS-1776.

Only writes inside this mission's report directory. Never rewrites gameplay.
"""
from __future__ import annotations
import collections as C
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from validate_diplomacy_ottoman_1776 import parse, walk, scalar

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Games/Victoria 3/game')
OUT=ROOT/'docs/reports/economy/ALLOYS_1776_REBALANCE'
GIT=Path('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe')
GROUP='pmg_aor1776_utensils'
UTENSILS=['pm_aor1776_no_utensils','pm_aor1776_wrought_iron_utensils','pm_aor1776_copper_brass_utensils','pm_aor1776_machined_utensils','pm_aor1776_industrial_utensils']
BRONZE='pm_aor1776_bronze_artillery'
HARDWARE='aor1776_hardware'
NEW_PM='common/production_methods/1776_alloys_utensils.txt'
NEW_GROUP='common/production_method_groups/1776_alloys_utensils.txt'
ALLOY_PM='common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt'
LOCS=[f'localization/{lang}/1776_alloys_utensils_l_{lang}.yml' for lang in ['french','english']]
OWNED=[ALLOY_PM,'common/buildings/01_industry.txt','common/production_method_groups/01_industry.txt','common/pop_needs/00_pop_needs.txt',
       *[f'localization/{lang}/tech6c5c_aluminium_l_{lang}.yml' for lang in ['french','english']],NEW_PM,NEW_GROUP,*LOCS,'tools/tech6c5c_validate.py',
       'common/goods/1776_hardware.txt','common/modifier_type_definitions/1776_hardware.txt','gui/1776_hardware_texticons.gui',
       'gfx/interface/icons/goods_icons/aor1776_hardware.dds','workshop_assets/source/aor1776_hardware_transparent.png','tools/build_hardware_icon.py']


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def vals(n,k):return [scalar(v.value) for b in n.children(k) for v in b.children() if isinstance(v.value,str)]
def canonical(n):return [n.key,n.op,[canonical(v) for v in n.children()] if isinstance(n.value,list) else n.value]
def fingerprint(n):return hashlib.sha256(json.dumps(canonical(n),ensure_ascii=False).encode()).hexdigest()
def definitions(folder):
    files={p.relative_to(GAME/folder).as_posix():p for p in (GAME/folder).rglob('*.txt')}
    files.update({p.relative_to(ROOT/folder).as_posix():p for p in (ROOT/folder).rglob('*.txt')})
    result={};duplicates=C.defaultdict(list)
    for p in sorted(files.values(),key=lambda p:p.name):
        raw=p.read_text(encoding='utf-8-sig')
        for n in parse(raw):
            if n.key and isinstance(n.value,list):
                result[n.key]=(n,p);duplicates[n.key].append(str(p))
    return result,{k:v for k,v in duplicates.items() if len(v)>1}
def recipe(n):
    inputs=C.Counter();outputs=C.Counter();jobs=C.Counter()
    for b in n.children('building_modifiers'):
        for field in b.children():
            for v in field.children():
                if not isinstance(v.value,str):continue
                for prefix,target in [('goods_input_',inputs),('goods_output_',outputs),('building_employment_',jobs)]:
                    if v.key.startswith(prefix) and v.key.endswith('_add'):target[v.key[len(prefix):-4]]+=float(v.value)
    return dict(inputs=dict(inputs),outputs=dict(outputs),jobs=dict(jobs))
def prices_and_wages():
    goods,_=definitions('common/goods');pops,_=definitions('common/pop_types')
    return {k:float(n.one('cost',0)) for k,(n,p) in goods.items()},{k:float(n.one('wage_weight',1)) for k,(n,p) in pops.items()}
def cost(r,prices,wages,labor_wage=10,input_factor=1,output_factor=1):
    i=sum(v*prices[g] for g,v in r['inputs'].items())*input_factor
    o=sum(v*prices[g] for g,v in r['outputs'].items())*output_factor
    weight=sum(v*wages.get(g,1) for g,v in r['jobs'].items());pay=weight*labor_wage/52
    return dict(input_cost=i,output_value=o,gross_margin=o-i,employees=sum(r['jobs'].values()),wage_units=weight,
                annual_labor_wage=labor_wage,weekly_wage_bill=pay,net_before_taxes_subsidies=o-i-pay,
                value_ratio=o/i if i else None,break_even_annual_labor_wage=(o-i)*52/weight if weight else None)
def environment():
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PATH']=str(GIT.parent)+os.pathsep+env.get('PATH','');return env
def legacy_test():
    r=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/tech6c5c_validate.py')],cwd=ROOT,env=environment(),capture_output=True,text=True,timeout=120)
    return dict(command='python -X utf8 tools/tech6c5c_validate.py',exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)


def capture():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'BASELINE.json').exists(),'Never replace baseline'
    models={};raws={};recipes={}
    for kind,folder in [('pms','common/production_methods'),('groups','common/production_method_groups'),('buildings','common/buildings'),('needs','common/pop_needs'),('techs','common/technology/technologies'),('goods','common/goods')]:
        defs,dups=definitions(folder);models[kind]={k:fingerprint(n) for k,(n,p) in defs.items()}
        if kind=='pms':recipes={k:recipe(n) for k,(n,p) in defs.items()}
        if kind in {'buildings','needs','groups'}:raws[kind]={k:canonical(n) for k,(n,p) in defs.items() if k in {'building_furniture_manufactory','popneed_household_items','pmg_foundries'}}
    files={}
    for folder in ['common','map_data','localization','gfx','gui','events']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():files[p.relative_to(ROOT).as_posix()]=sha(p)
    prices,wages=prices_and_wages()
    originals={rel:(ROOT/rel).read_text(encoding='utf-8-sig') for rel in OWNED if (ROOT/rel).exists()}
    dump('BASELINE.json',dict(status='PRE_IMPLEMENTATION',files=files,models=models,raws=raws,recipes=recipes,prices=prices,wages=wages,
         originals=originals,git_head=subprocess.check_output([str(GIT),'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index=sha(ROOT/'.git/index')))
    dump('LEGACY_TEST_BEFORE.json',legacy_test())
    dump('CONCURRENT_CHANGES.json',dict(policy='Never restore baselines; tightly patch current shared blocks. Technology files and starting profiles remain untouched.',
         initial_git_status=subprocess.check_output([str(GIT),'status','--short','--',*OWNED,'common/technology/technologies/95_tech6r1_aluminium_metallurgy.txt'],cwd=ROOT,text=True),
         owned_file_hashes={rel:sha(ROOT/rel) for rel in OWNED},technology_sha256=sha(ROOT/'common/technology/technologies/95_tech6r1_aluminium_metallurgy.txt'),human_validations_changed=False))
    print('Baseline captured; legacy test recorded; protected runtime files',len(files))


def report_tables():
    b=json.loads((OUT/'BASELINE.json').read_text());pms,_=definitions('common/production_methods');tech,_=definitions('common/technology/technologies');prices,wages=prices_and_wages()
    rows=[]
    for k in ['pm_basic_smelting_process','pm_electric_arc_process_alloying']:
        for state,r in [('before',b['recipes'][k]),('after',recipe(pms[k][0]))]:
            rows.append(dict(PM=k,State=state,Inputs=json.dumps(r['inputs']),Output=json.dumps(r['outputs']),Jobs=json.dumps(r['jobs']),**cost(r,prices,wages)))
    csvout('ALLOY_PRODUCTION_BEFORE_AFTER.csv',rows)
    rows=[]
    for k in UTENSILS:
        n=pms[k][0];r=recipe(n);gates=vals(n,'unlocking_technologies');economics=cost(r,prices,wages)
        rows.append(dict(PM=k,Technologies=';'.join(gates),Eras=';'.join(str(tech[t][0].one('era')) for t in gates),
                         Inputs=json.dumps(r['inputs']),Hardware=r['outputs'].get(HARDWARE,0),Furniture=r['outputs'].get('furniture',0),Jobs=json.dumps(r['jobs']),**economics))
    csvout('FURNITURE_UTENSILS_PM_MATRIX.csv',rows)
    csvout('HARDWARE_PM_MATRIX.csv',rows)
    h=json.loads((OUT/'HARDWARE_BASELINE.json').read_text(encoding='utf-8'))
    csvout('HARDWARE_BEFORE_AFTER.csv',[dict(PM=k,Previous_furniture=h['recipes'][k]['outputs'].get('furniture',0),New_hardware=recipe(pms[k][0])['outputs'].get(HARDWARE,0),Previous_inputs=json.dumps(h['recipes'][k]['inputs']),New_inputs=json.dumps(recipe(pms[k][0])['inputs'])) for k in UTENSILS])
    rows=[]
    for k,(n,p) in pms.items():
        r=recipe(n)
        if r['inputs'].get('alloys',0)>0:
            gates=vals(n,'unlocking_technologies');rows.append(dict(Consumer=k,Before_Alloys=b['recipes'].get(k,{}).get('inputs',{}).get('alloys',0),After_Alloys=r['inputs']['alloys'],Technologies=';'.join(gates),Eras=';'.join(str(tech[t][0].one('era')) for t in gates),Scope='per fully staffed level per week'))
    rows.append(dict(Consumer='popneed_household_items',Before_Alloys=0,After_Alloys='bounded substitution, not fixed quantity',Technologies='none; wealth package',Eras='wealth 10+',Scope='weight=.02; min_supply_share=.01; max_supply_share=.05'))
    csvout('ALLOY_DEMAND_BEFORE_AFTER.csv',rows)
    # Explicit scenarios, not estimates of an unobserved in-game equilibrium.
    scenarios=[]
    for name,alloy_levels,bronze_levels,utensil_levels in [('weakly_industrialized',0,0,1),('metallurgical_country',2,3,4),('military_power',4,10,5),('hardware_exporter',6,2,20),('industrial_V_VI',20,10,40)]:
        pm=UTENSILS[3] if name=='industrial_V_VI' else UTENSILS[2]
        if name=='weakly_industrialized':pm=UTENSILS[1]
        demand=bronze_levels*recipe(pms[BRONZE][0])['inputs']['alloys']+utensil_levels*recipe(pms[pm][0])['inputs'].get('alloys',0)
        scenarios.append(dict(name=name,alloy_factory_levels=alloy_levels,bronze_foundry_levels=bronze_levels,utensil_levels=utensil_levels,utensil_pm=pm,
                              alloy_supply=alloy_levels*20,industrial_alloy_demand=demand,hardware_supply=utensil_levels*recipe(pms[pm][0])['outputs'].get(HARDWARE,0),residual_before_POPs_and_trade=alloy_levels*20-demand))
    dump('REFERENCE_SCENARIOS.json',dict(kind='Illustrative explicit levels, not measured national demand',scenarios=scenarios))
    dump('BASE_PRICE_STRESS.json',[dict(pm=k,scenario=label,**cost(recipe(pms[k][0]),prices,wages,w,fi,fo)) for k in ['pm_basic_smelting_process',*UTENSILS[1:],BRONZE,'pm_electric_arc_process_alloying'] for label,w,fi,fo in [('wage_5',5,1,1),('wage_10',10,1,1),('wage_12',12,1,1),('inputs_plus_25_wage_10',10,1.25,1),('combined_adverse',10,1.25,.75)]])
    print('Economic CSVs and explicit reference scenarios generated')


if __name__=='__main__':{'capture':capture,'tables':report_tables}[sys.argv[1]]()
