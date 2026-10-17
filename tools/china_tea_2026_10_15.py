"""Only twenty Chinese tea-plantation levels, with existing-infrastructure checks."""
import collections as C
import json
import os
import subprocess
import sys
import start_buildings_2026_10_15 as b

ROOT=b.ROOT
OUT=b.OUT/'CHINA_TEA'
NEW='common/history/buildings/99_1776_china_tea_addon.txt'
STATES=['STATE_HUNAN','STATE_SICHUAN','STATE_NANJING','STATE_SUZHOU']
KIND='building_tea_plantation'

def dump(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')

def head():
    return subprocess.check_output([b.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')).strip()

def prepare():
    assert not (OUT/'BASELINE.json').exists(), 'Do not replace the pre-edit snapshot'
    assert not (ROOT/NEW).exists(), 'Do not add these twenty levels twice'
    methods=b.new_recipes(KIND,'CHI')
    text='# Twenty requested Chinese tea levels only; no roads, technology or other industry changes.\nBUILDINGS = {\n'
    for sid in STATES:
        text+='\ts:'+sid+' = {\n\t\tregion_state:CHI = {\n\t\t\tcreate_building = {\n\t\t\t\tbuilding = "'+KIND+'"\n\t\t\t\tadd_ownership = { building = { type = "building_manor_house" country = "c:CHI" levels = 5 region = "'+sid+'" } }\n\t\t\t\treserves = 1\n\t\t\t\tactivate_production_methods = { '+' '.join('"'+pm+'"' for pm in methods)+' }\n\t\t\t}\n\t\t}\n\t}\n'
    text+='}\n'
    rows=b.declarations();inventory=b.qa.inventory()
    after=b.forecast(rows+b.parse_addon(text))
    chosen=[r for r in after if r['owner']=='CHI' and r['state'] in STATES]
    assert len(chosen)==4
    for row in chosen:
        assert row['nominal_margin']>=0 and row['free_arable']>=0 and KIND in row['arable_resources']
        assert [row['state'],'CHI'] in inventory['states']
    dump('BASELINE.json',dict(hashes=b.runtime_hashes(),inventory=inventory,head=head(),index_sha256=b.sha(ROOT/'.git/index'),expected_text=text))
    dump('INFRASTRUCTURE_BEFORE.json',[r for r in b.forecast(rows) if r['owner']=='CHI' and r['state'] in STATES])
    dump('INFRASTRUCTURE_AFTER.json',chosen)
    previous=b.patchwork.OUT
    try:b.patchwork.OUT=OUT;b.patchwork.emit({NEW:text},'CHANGES.patch')
    finally:b.patchwork.OUT=previous
    print('Prepared exactly 5 levels in each of',', '.join(STATES))

def validate():
    baseline=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    inv=b.qa.inventory();rows=b.declarations();checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value)))
    check('Exact reviewed tea history',(ROOT/NEW).read_text(encoding='utf-8-sig')==baseline['expected_text'])
    current=b.runtime_hashes();old=baseline['hashes']
    check('Only functional change is the new tea file',{p for p in current.keys()|old.keys() if current.get(p)!=old.get(p)}=={NEW})
    added=b.parse_addon(baseline['expected_text'])
    expected=b.qa.counter(baseline['inventory']['buildings'])
    for sid,tag,node,path in added:expected[(sid,tag,b.qa.signature(node))]+=1
    check('Exact worldwide building delta, no other additions',b.qa.counter(inv['buildings'])==expected)
    check('Exactly four declarations, five levels each',len(added)==4 and all(b.levels(n)==5 for s,t,n,p in added))
    totals=b.totals(rows);added_rows=[r for r in rows if r[3]==ROOT/NEW]
    check('Twenty tea levels, no other building kind',sum(b.levels(n) for s,t,n,p in added_rows)==20 and all(b.cw.scalar(n.one('building'))==KIND for s,t,n,p in added_rows))
    for field in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','units','errors','duplicates']:
        check('Preserved inventory '+field,inv[field]==baseline['inventory'][field])
    for sid,tag,node,path in added_rows:
        check('Valid state and tea resource '+sid,[sid,tag] in inv['states'] and KIND in b.values(b.catalog('map_data/state_regions')[sid],'arable_resources'))
        check('Unlocked tea building '+sid,set(b.values(b.catalog('common/buildings')[KIND],'unlocking_technologies'))<=b.starting_tech('CHI'))
        for pm in b.recipes(node):
            check('Unlocked selected method '+sid+' '+pm,set(b.values(b.catalog('common/production_methods')[pm],'unlocking_technologies'))<=b.starting_tech('CHI'))
    after=[r for r in b.forecast(rows) if r['owner']=='CHI' and r['state'] in STATES]
    for row in after:
        check('Existing infrastructure sufficient '+row['state'],row['nominal_margin']>=0)
        check('Existing arable land sufficient '+row['state'],row['free_arable']>=0)
    check('No Chinese arms technology granted','regulated_small_arms' not in b.starting_tech('CHI'))
    check('Population remains 835804980',sum(r['count'] for r in inv['pops'])==835804980)
    check('HEAD unchanged',head()==baseline['head'])
    check('Git index unchanged',b.sha(ROOT/'.git/index')==baseline['index_sha256'])
    result=dict(status='PASS_STATIC_PENDING_RUNTIME' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                added_levels=20,states={s:5 for s in STATES},infra_after={r['state']:r['nominal_margin'] for r in after},engine_tested=False)
    dump('VALIDATION.json',result)
    print(result['status'],result['passed'],'/',result['total'],'checks; margins:',result['infra_after'])
    for row in checks:
        if not row['passed']:print('FAIL',row['name'])
    assert result['status']!='FAIL'

if __name__=='__main__':{'prepare':prepare,'validate':validate}[sys.argv[1]]()
