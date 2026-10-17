"""Player-requested starting industry/agriculture changes; no territorial edits."""
import collections as C
import csv, json, subprocess, sys
from functools import lru_cache
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective, values
from map2l_belgium import sha
from map2l_hre_work import GIT
import map2l_mainz as patchwork

ROOT = qa.ROOT
OUT = ROOT/'docs/reports/economy/START_BUILDINGS_2026_10_15'
NEW = 'common/history/buildings/99_1776_player_industry_agriculture_addon.txt'
KINDS = ['building_arms_industry','building_salt_mine','building_silk_plantation','building_rice_farm','building_livestock_ranch','building_glassworks']
PLAN = [
    ('STATE_RHONE','FRA','building_arms_industry',3),
    ('STATE_AUSTRIA','AUS','building_arms_industry',3),
    ('STATE_ANHALT','PRU','building_salt_mine',2),
    ('STATE_JIANGXI','CHI','building_arms_industry',2),
    ('STATE_SUZHOU','CHI','building_silk_plantation',10),
    ('STATE_JIANGSU','CHI','building_silk_plantation',8),
    ('STATE_NANJING','CHI','building_silk_plantation',6),
    ('STATE_EASTERN_HUBEI','CHI','building_silk_plantation',3),
    ('STATE_GUANGDONG','CHI','building_silk_plantation',3),
    ('STATE_JIANGSU','CHI','building_rice_farm',3),
    ('STATE_HUNAN','CHI','building_rice_farm',3),
    ('STATE_JIANGXI','CHI','building_rice_farm',2),
    ('STATE_EASTERN_HUBEI','CHI','building_rice_farm',2),
    ('STATE_ZHILI','CHI','building_livestock_ranch',6),
    ('STATE_SHANDONG','CHI','building_livestock_ranch',5),
    ('STATE_HENAN','CHI','building_livestock_ranch',4),
    ('STATE_SICHUAN','CHI','building_livestock_ranch',3),
    ('STATE_SHANXI','CHI','building_livestock_ranch',2),
    ('STATE_JIANGXI','CHI','building_glassworks',4),
    ('STATE_NANJING','CHI','building_glassworks',3),
    ('STATE_SUZHOU','CHI','building_glassworks',3),
]
DELTAS = dict(zip(KINDS,[8,2,30,10,20,10]))

def dump(name, value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

@lru_cache(None)
def catalog(folder):
    result = {}
    for path in effective(ROOT,qa.GAME,folder):
        for node in cw.parse(path.read_text(encoding='utf-8-sig')):
            result[node.key.removeprefix('REPLACE_OR_CREATE:')] = node
    return result

def levels(node):
    return sum(int(n.value) for n in cw.walk(node.children()) if n.key=='levels')

def declarations(extra=''):
    result=[]
    for path in effective(ROOT,qa.GAME,'common/history/buildings'):
        raw=path.read_text(encoding='utf-8-sig')
        for state in cw.walk(cw.parse(raw)):
            if not state.key.startswith('s:STATE_'):continue
            for rs in state.children():
                if rs.key.startswith('region_state:'):
                    for b in rs.children('create_building'):
                        result.append((state.key[2:],rs.key.split(':')[1],b,path))
    if extra:
        for state in cw.walk(cw.parse(extra)):
            if state.key.startswith('s:STATE_'):
                for rs in state.children():
                    for b in rs.children('create_building'):
                        result.append((state.key[2:],rs.key.split(':')[1],b,ROOT/NEW))
    return result

def totals(rows):
    counts=C.Counter()
    for sid,tag,node,path in rows:counts[sid,tag,cw.scalar(node.one('building'))]+=levels(node)
    return counts

def group_value(group,key,default=0):
    groups=catalog('common/building_groups')
    node=groups[group]
    if node.children(key):return cw.scalar(node.one(key))
    parent=cw.scalar(node.one('parent_group',''))
    return group_value(parent,key,default) if parent else default

def recipes(node):
    definition=catalog('common/buildings')[cw.scalar(node.one('building'))]
    pmgs=catalog('common/production_method_groups')
    selected=values(node,'activate_production_methods')
    result=[]
    for group in values(definition,'production_method_groups'):
        options=values(pmgs[group],'production_methods')
        matches=[pm for pm in selected if pm in options]
        if len(matches)>1:raise ValueError('Conflicting methods '+str(matches))
        if matches:result+=matches
        elif options:result.append(options[0])
    return result

def forecast(rows):
    definitions=catalog('common/buildings');pms=catalog('common/production_methods')
    regions=catalog('map_data/state_regions');traits=catalog('common/state_traits')
    base=float(catalog('common/static_modifiers')['base_values'].one('state_infrastructure_add'))
    data={}
    for sid,tag,node,path in rows:
        if tag!='CHI' and (sid,tag) not in [('STATE_RHONE','FRA'),('STATE_AUSTRIA','AUS'),('STATE_ANHALT','PRU')]:continue
        row=data.setdefault((sid,tag),dict(state=sid,owner=tag,demand=0,supply=0,rural_levels=0,by_building={}))
        n=levels(node);kind=cw.scalar(node.one('building'));definition=definitions[kind];group=cw.scalar(definition.one('building_group'))
        usage=float(definition.one('infrastructure_usage_per_level',group_value(group,'infrastructure_usage_per_level')))
        row['demand']+=n*usage
        row['by_building'][kind]=row['by_building'].get(kind,0)+n
        if group_value(group,'land_usage','')=='rural':row['rural_levels']+=n
        for pm in recipes(node):
            for sm in pms[pm].children('state_modifiers'):
                row['supply']+=n*sum(float(v.value) for v in cw.walk(sm.children()) if v.key=='state_infrastructure_add')
    for (sid,tag),row in data.items():
        reg=regions[sid]
        fixed=sum(float(v.value) for trait in values(reg,'traits') for v in cw.walk(traits[trait].children()) if v.key=='state_infrastructure_add')
        row.update(base=base,trait_supply=fixed,nominal_capacity=base+fixed+row['supply'],arable=int(reg.one('arable_land',0)),arable_resources=values(reg,'arable_resources'))
        row['nominal_margin']=row['nominal_capacity']-row['demand']
        row['free_arable']=row['arable']-row['rural_levels']
    return sorted(data.values(),key=lambda r:(r['owner'],r['state']))

def audit():
    rows=declarations();counts=totals(rows);data=forecast(rows)
    dump('AUDIT_BEFORE.json',data)
    for tag in ['CHI','FRA','AUS','PRU']:
        print(tag,{kind:sum(n for (sid,owner,k),n in counts.items() if owner==tag and k==kind) for kind in KINDS})
    for row in data:
        if row['owner']=='CHI' or row['state'] in ['STATE_RHONE','STATE_AUSTRIA','STATE_ANHALT']:
            print(row['state'],row['owner'],'infra',row['nominal_margin'],'land',row['free_arable'],'target buildings',{k:v for k,v in row['by_building'].items() if k in KINDS},'resources',','.join(row['arable_resources']))

@lru_cache(None)
def starting_tech(tag):
    result=set()
    effects=catalog('common/scripted_effects')
    for path in effective(ROOT,qa.GAME,'common/history/countries'):
        if not path.name.lower().startswith(tag.lower()+' -'):continue
        nodes=list(cw.walk(cw.parse(path.read_text(encoding='utf-8-sig'))))
        result.update(cw.scalar(n.value) for n in nodes if n.key=='add_technology_researched')
        for node in nodes:
            if node.key.startswith('effect_starting_technology_') and node.value=='yes' and node.key in effects:
                result.update(cw.scalar(n.value) for n in cw.walk(effects[node.key].children()) if n.key=='add_technology_researched')
    return result

def new_recipes(kind,tag):
    definition=catalog('common/buildings')[kind]
    pmgs=catalog('common/production_method_groups')
    selected=[]
    for group in values(definition,'production_method_groups'):
        options=values(pmgs[group],'production_methods')
        assert options,group
        unlocked=[pm for pm in options if set(values(catalog('common/production_methods')[pm],'unlocking_technologies'))<=starting_tech(tag)]
        assert unlocked,(tag,group)
        selected.append('pm_ceramics' if kind=='building_glassworks' and 'pm_ceramics' in options else unlocked[0])
    return selected

def addon_text():
    grouped={}
    for sid,tag,kind,count in PLAN:
        rural=kind in ['building_silk_plantation','building_rice_farm','building_livestock_ranch']
        if kind=='building_arms_industry':
            ownership='country = { country = "c:'+tag+'" levels = '+str(count)+' }'
        else:
            owner='building_manor_house' if rural else 'building_financial_district'
            ownership='building = { type = "'+owner+'" country = "c:'+tag+'" levels = '+str(count)+' region = "'+sid+'" }'
        block='\t\t\tcreate_building = {\n\t\t\t\tbuilding = "'+kind+'"\n\t\t\t\tadd_ownership = { '+ownership+' }\n\t\t\t\treserves = 1\n\t\t\t\tactivate_production_methods = { '+' '.join('"'+p+'"' for p in new_recipes(kind,tag))+' }\n\t\t\t}\n'
        grouped.setdefault((sid,tag),[]).append(block)
    return '# Player-requested additions, 2026-10-15. Existing histories are additive and untouched.\nBUILDINGS = {\n'+''.join('\ts:'+sid+' = {\n\t\tregion_state:'+tag+' = {\n'+''.join(blocks)+'\t\t}\n\t}\n' for (sid,tag),blocks in grouped.items())+'}\n'

def parse_addon(text):
    rows=[]
    for state in cw.walk(cw.parse(text)):
        if not state.key.startswith('s:STATE_'):continue
        for rs in state.children():
            if rs.key.startswith('region_state:'):
                for node in rs.children('create_building'):rows.append((state.key[2:],rs.key.split(':')[1],node,ROOT/NEW))
    return rows

def runtime_hashes():
    return {p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','map_data','gui','gfx','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}

def prepare():
    assert not (OUT/'BASELINE.json').exists(),'Never overwrite baseline; do not repeat additive changes.'
    assert not (ROOT/NEW).exists(),'Addon already exists; inspect it, do not duplicate.'
    before_rows=declarations();text=addon_text();new=parse_addon(text)
    before=qa.inventory();after_forecast=forecast(before_rows+new)
    # Infrastructure requirement is explicit for Chinese glassworks; enforce it
    # for all selected Chinese states without adding unrequested roads/ports.
    chosen={(sid,tag) for sid,tag,kind,count in PLAN}
    for row in after_forecast:
        if (row['state'],row['owner']) not in chosen:continue
        assert [row['state'],row['owner']] in before['states']
        if row['owner']=='CHI':
            assert row['nominal_margin']>=0,(row['state'],row['nominal_margin'])
            assert row['rural_levels']<=row['arable']
        print(row['state'],row['owner'],'margin after',row['nominal_margin'])
    dump('BASELINE.json',dict(inventory=before,hashes=runtime_hashes(),expected_text=text,HEAD=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_sha256=sha(ROOT/'.git/index')))
    dump('INFRASTRUCTURE_BEFORE.json',forecast(before_rows));dump('INFRASTRUCTURE_AFTER.json',after_forecast)
    old=patchwork.OUT
    try:patchwork.OUT=OUT;patchwork.emit({NEW:text},'CHANGES.patch')
    finally:patchwork.OUT=old
    dump('PLAN.json',dict(added=[dict(state=sid,owner=tag,building=kind,levels=count) for sid,tag,kind,count in PLAN],global_deltas=DELTAS,new_file=NEW,glass_interpretation='CHI starts with zero; ten new levels also yield ten total; all use pm_ceramics.'))
    for kind in KINDS:print(kind,new_recipes(kind,'CHI'))

def review():
    """Amend an UNAPPLIED proposal, never overwrite the immutable baseline."""
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    assert not (ROOT/NEW).exists()
    assert runtime_hashes()==baseline['hashes']
    text=addon_text()
    dump('REVIEWED_PLAN.json',dict(expected_text=text,reason='Pre-application PM technology check: choose unlocked reporting-off fallback instead of forcing scientific_metrology. No country technology is granted.'))
    old=patchwork.OUT
    try:patchwork.OUT=OUT;patchwork.emit({NEW:text},'CHANGES.patch')
    finally:patchwork.OUT=old
    dump('INFRASTRUCTURE_AFTER.json',forecast(declarations()+parse_addon(text)))
    print('Reviewed unapplied proposal; baseline preserved.')

def validate():
    baseline=json.loads((OUT/'BASELINE.json').read_text());inventory=qa.inventory();checks=[]
    def check(name,result,detail=''):checks.append(dict(name=name,passed=bool(result),detail=detail))
    for key in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','units','errors','duplicates']:
        check('Preserved '+key,inventory[key]==baseline['inventory'][key])
    reviewed=json.loads((OUT/'REVIEWED_PLAN.json').read_text())['expected_text'] if (OUT/'REVIEWED_PLAN.json').exists() else baseline['expected_text']
    check('Exact reviewed addon and no accidental repeated application',(ROOT/NEW).read_text(encoding='utf-8-sig')==reviewed)
    current=runtime_hashes()
    check('No existing runtime file overwritten',all(current.get(name)==digest for name,digest in baseline['hashes'].items()))
    check('Only one new runtime file',set(current)-set(baseline['hashes'])=={NEW} and not(set(baseline['hashes'])-set(current)))
    check('GUI trade centre fix and bitmap bytes preserved',current['gui/building_details_panel.gui']==baseline['hashes']['gui/building_details_panel.gui'] and current['map_data/provinces.png']==baseline['hashes']['map_data/provinces.png'])
    expected=qa.counter(baseline['inventory']['building_levels_written'])
    expected.update(DELTAS)
    check('Exact worldwide level deltas',qa.counter(inventory['building_levels_written'])==expected)
    expected_declarations=qa.counter(baseline['inventory']['buildings'])
    expected_declarations.update((sid,tag,qa.signature(node)) for sid,tag,node,path in parse_addon(reviewed))
    check('All pre-existing PMs economic owners reserves and declarations retained',qa.counter(inventory['buildings'])==expected_declarations)
    before_rows=[r for r in declarations() if r[3] != ROOT/NEW];after_rows=declarations()
    before_counts=totals(before_rows);after_counts=totals(after_rows)
    changes=[]
    for sid,tag,kind,count in PLAN:
        check('Requested delta '+sid+' '+tag+' '+kind,after_counts[sid,tag,kind]-before_counts[sid,tag,kind]==count)
        changes.append(dict(State_ID=sid,Owner_TAG=tag,Building=kind,Before=before_counts[sid,tag,kind],Added=count,After=after_counts[sid,tag,kind]))
    for kind,delta in [('building_silk_plantation',30),('building_rice_farm',10),('building_livestock_ranch',20),('building_glassworks',10)]:
        total=lambda counter:sum(n for (sid,tag,k),n in counter.items() if tag=='CHI' and k==kind)
        check('China aggregate '+kind,total(after_counts)-total(before_counts)==delta)
    check('China exactly ten glassworks levels',sum(n for (sid,tag,k),n in after_counts.items() if tag=='CHI' and k=='building_glassworks')==10)
    actual=forecast(after_rows);check('Infrastructure forecast reproducible',actual==json.loads((OUT/'INFRASTRUCTURE_AFTER.json').read_text()))
    selected={(sid,tag) for sid,tag,kind,count in PLAN}
    for row in actual:
        if (row['state'],row['owner']) in selected and row['owner']=='CHI':
            check('China nominal infrastructure margin nonnegative '+row['state'],row['nominal_margin']>=0,str(row['nominal_margin']))
            check('China cultivated land within capacity '+row['state'],row['rural_levels']<=row['arable'])
    definitions=catalog('common/buildings');pmgs=catalog('common/production_method_groups');pms=catalog('common/production_methods');regions=catalog('map_data/state_regions')
    tech={tag:starting_tech(tag) for tag in ['FRA','AUS','PRU','CHI']};technology_warnings=[]
    for sid,tag,node,path in parse_addon(reviewed):
        kind=cw.scalar(node.one('building'));definition=definitions[kind];pm_list=values(node,'activate_production_methods')
        missing=set(values(definition,'unlocking_technologies'))-tech[tag]
        precedent=sum(n for (s,t,k),n in before_counts.items() if t==tag and k==kind)
        check('Building gate unlocked or pre-existing historical-building precedent '+sid+' '+kind,not missing or precedent>0)
        if missing:technology_warnings.append(dict(state=sid,owner=tag,building=kind,missing_explicit_grants=sorted(missing),existing_country_levels=precedent,note='Written history already creates this building for this country. No unlock or prerequisite is silently granted; engine expansion availability requires runtime inspection.'))
        permitted={pm for group in values(definition,'production_method_groups') for pm in values(pmgs[group],'production_methods')}
        check('One compatible explicit PM per group '+sid+' '+kind,set(pm_list)<=permitted and len(pm_list)==len(values(definition,'production_method_groups')) and recipes(node)==pm_list)
        for pm in pm_list:check('Unlocked PM '+sid+' '+kind+' '+pm,pm in pms and set(values(pms[pm],'unlocking_technologies'))<=tech[tag])
        if kind in ['building_silk_plantation','building_rice_farm','building_livestock_ranch']:
            check('Arable resource available '+sid+' '+kind,kind in values(regions[sid],'arable_resources'))
        if kind=='building_glassworks':check('Porcelain activated '+sid,'pm_ceramics' in pm_list and 'pm_disabled_ceramics' not in pm_list)
    salt_capacity=sum(int(r.one('discovered_amount',0)) for r in regions['STATE_ANHALT'].children('resource') if cw.scalar(r.one('type'))=='building_salt_mine')
    salt_existing=sum(n for (sid,tag,kind),n in after_counts.items() if sid=='STATE_ANHALT' and kind=='building_salt_mine')
    check('Anhalt discovered salt capacity adequate',salt_existing<=salt_capacity,str(dict(written_levels=salt_existing,regional_discovered=salt_capacity)))
    check('Brandenburg six arms levels preserved',after_counts['STATE_BRANDENBURG','PRU','building_arms_industry']==before_counts['STATE_BRANDENBURG','PRU','building_arms_industry']==6)
    check('Population remains 835804980',sum(r['count'] for r in inventory['pops'])==835804980)
    check('HEAD and Git index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==baseline['HEAD'] and sha(ROOT/'.git/index')==baseline['index_sha256'])
    with (OUT/'BUILDING_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(changes[0]));writer.writeheader();writer.writerows(changes)
    report=dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,global_level_deltas=DELTAS,engine_tested=False,runtime_status='NOT_YET_TESTED',infrastructure_scope='Nominal written-data lower-bound forecast, not a measured in-game infrastructure or market access result. Implicit buildings, population contributions, employment and country modifiers are not simulated.',technology_warnings=technology_warnings,world_population=835804980,inherited_duplicate_RGBs=len(inventory['duplicates']),inherited_invalid_references=len(inventory['errors']))
    dump('VALIDATION.json',report)
    print(report['status'],sum(r['passed'] for r in checks),'/',len(checks))
    for r in checks:
        if not r['passed']:print('FAIL',r['name'],r['detail'])
    return int(not all(r['passed'] for r in checks))

if __name__=='__main__':
    if sys.argv[1]=='audit':audit()
    elif sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='review':review()
    elif sys.argv[1]=='validate':raise SystemExit(validate())
    else:raise SystemExit('Unknown action')
