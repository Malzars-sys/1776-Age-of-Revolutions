"""Size metropolitan GBR roads at full employment, with zero canal credit."""
import collections as C
import csv, json, math, re, subprocess, sys
import start_buildings_2026_10_15 as base
from map2a_patch import edits

ROOT=base.ROOT
OUT=base.OUT/'BRITISH_ROADS_AND_SALT'
HOME={'STATE_HOME_COUNTIES','STATE_EAST_ANGLIA','STATE_WEST_COUNTRY','STATE_WALES','STATE_MIDLANDS','STATE_YORKSHIRE','STATE_LANCASHIRE','STATE_LOWLANDS','STATE_HIGHLANDS','STATE_ULSTER','STATE_LEINSTER','STATE_MUNSTER','STATE_CONNAUGHT'}
ROAD='pm_turnpike_road_network'
KEYS=['state_infrastructure_add','state_infrastructure_from_population_add','state_infrastructure_from_population_max_add','state_infrastructure_mult']
SALT='common/production_methods/10_tech6a1b_salt_producers.txt'
CANALS={'STATE_LANCASHIRE','STATE_MIDLANDS','STATE_YORKSHIRE'}
IRISH_ADD={'STATE_LEINSTER':10,'STATE_ULSTER':3,'STATE_MUNSTER':2}
IRISH_FILE='common/history/buildings/99_1776_irish_bureaucracy_addon.txt'

def network_pms(sid):
    return [ROAD,'pm_industrial_canals' if sid in CANALS else 'pm_no_canal_network','pm_no_rail_network','pm_no_passenger_trains']

def irish_pms():
    methods=base.new_recipes('building_government_administration','IREK')
    return ['pm_professional_bureaucrats' if p=='pm_hereditary_bureaucrats' else p for p in methods]

def irish_text():
    return '# Cover observed -128 Irish bureaucracy: +150 nominal at full employment.\nBUILDINGS = {\n'+''.join('\ts:'+sid+' = {\n\t\tregion_state:IREK = {\n\t\t\tcreate_building = {\n\t\t\t\tbuilding = "building_government_administration"\n\t\t\t\tadd_ownership = { country = { country = "c:IREK" levels = '+str(n)+' } }\n\t\t\t\treserves = 1\n\t\t\t\tactivate_production_methods = { '+' '.join('"'+pm+'"' for pm in irish_pms())+' }\n\t\t\t}\n\t\t}\n\t}\n' for sid,n in IRISH_ADD.items())+'}\n'

def dump(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def modifiers(nodes):
    result=C.Counter()
    for node in base.cw.walk(nodes):
        if node.key in KEYS:
            result[node.key]+=float(node.value)
    return result

def capacity(context,levels):
    flat=context['fixed_add']+levels*context['road_add']
    rate=context['fixed_pop_add']+levels*context['road_pop_add']
    cap=context['fixed_pop_max']+levels*context['road_pop_max']
    pop_part=min(context['population']/context['population_divisor']*rate,cap)
    return (flat+pop_part)*(1+context['mult'])

def minimum_levels(context):
    for n in range(10000):
        if capacity(context,n)+1e-9>=context['target_capacity']:return n
    raise ValueError('No finite road sizing solution')

def old_capacity(row):
    total=C.Counter()
    pms=base.catalog('common/production_methods')
    for declaration,methods in zip(row['road_declarations'],row['previous_road_modes']):
        for pm in methods:
            for sm in pms[pm].children('state_modifiers'):
                for key,value in modifiers(sm.children()).items():total[key]+=declaration['levels']*value
    pop_part=min(row['population']/row['population_divisor']*(row['fixed_pop_add']+total[KEYS[1]]),row['fixed_pop_max']+total[KEYS[2]])
    return (row['fixed_add']+total[KEYS[0]]+pop_part)*(1+row['mult']+total[KEYS[3]])

def staffing_and_inputs(entries):
    result=C.Counter();pms=base.catalog('common/production_methods')
    for count,methods in entries:
        for pm in methods:
            for bm in pms[pm].children('building_modifiers'):
                for node in base.cw.walk(bm.children()):
                    if re.fullmatch('building_employment_.*_add',node.key):result['positions']+=count*float(node.value)
                    elif node.key in ['goods_input_wood_add','goods_input_tools_add','goods_input_iron_add','goods_output_transportation_add']:
                        result[node.key]+=count*float(node.value)
    return dict(result)

def contexts():
    rows=base.declarations();regions=base.catalog('map_data/state_regions');pms=base.catalog('common/production_methods');definitions=base.catalog('common/buildings')
    static=base.catalog('common/static_modifiers');traits=base.catalog('common/state_traits');technologies=base.catalog('common/technology/technologies')
    inv=base.qa.inventory();pop=C.Counter()
    for row in inv['regional_pop']:
        sid,tag,*_=row['key']
        if tag in ['GBR','IREK']:pop[sid]+=row['count']
    common=modifiers(static['base_values'].children());country={};law_ids={}
    for tag in ['GBR','IREK']:
        country[tag]=C.Counter()
        for tech in base.starting_tech(tag):
            if tech in technologies:
                for node in technologies[tech].children('modifier'):country[tag].update(modifiers(node.children()))
        path=next(p for p in base.effective(ROOT,base.qa.GAME,'common/history/countries') if p.name.lower().startswith(tag.lower()+' -'))
        raw=path.read_text(encoding='utf-8-sig')
        law_ids[tag]=[base.cw.scalar(n.value).removeprefix('law_type:') for n in base.cw.walk(base.cw.parse(raw)) if n.key=='activate_law']
        for law in law_ids[tag]:
            if law in base.catalog('common/laws'):
                for node in base.catalog('common/laws')[law].children('modifier'):country[tag].update(modifiers(node.children()))
    # Use the installed game's divisor rather than guessing population units.
    defines='\n'.join(p.read_text(encoding='utf-8-sig') for p in base.effective(ROOT,base.qa.GAME,'common/defines'))
    divisor=int(re.search(r'INDIVIDUALS_PER_POP_INFRASTRUCTURE\s*=\s*(\d+)',defines).group(1))
    data=[]
    for sid in sorted(HOME):
        owners=[tag for state,tag in inv['states'] if state==sid]
        assert len(owners)==1 and owners[0] in ['GBR','IREK'],(sid,owners)
        tag=owners[0]
        regional=[r for r in rows if r[:2]==(sid,tag)]
        m=C.Counter(common);m.update(country[tag])
        for trait in base.values(regions[sid],'traits'):m.update(modifiers(traits[trait].children()))
        # The only capital-specific static modifier is applied when defined.
        capital=base.cw.scalar(base.catalog('common/country_definitions')[tag].one('capital'))
        if sid==capital and 'capital_state' in static:m.update(modifiers(static['capital_state'].children()))
        demand=0;old_roads=0;old_capacity_add=0;road_declarations=[];old_modes=[]
        road=C.Counter()
        for pm in network_pms(sid):
            for sm in pms[pm].children('state_modifiers'):road.update(modifiers(sm.children()))
        for state,tag,node,path in regional:
            kind=base.cw.scalar(node.one('building'));n=base.levels(node);definition=definitions[kind];group=base.cw.scalar(definition.one('building_group'))
            demand+=n*float(definition.one('infrastructure_usage_per_level',base.group_value(group,'infrastructure_usage_per_level')))
            if kind=='building_railway':
                old_roads+=n;road_declarations.append(dict(file=path.relative_to(ROOT).as_posix(),levels=n,signature=base.qa.signature(node)));old_modes.append(base.recipes(node))
                continue
            for pm in base.recipes(node):
                for sm in pms[pm].children('state_modifiers'):
                    for key,value in modifiers(sm.children()).items():m[key]+=n*value
        # Recompute Irish roads AFTER budgeting the requested new offices.
        gov=definitions['building_government_administration'];group=base.cw.scalar(gov.one('building_group'))
        pending_admin=0 if (ROOT/IRISH_FILE).exists() else IRISH_ADD.get(sid,0)
        admin_demand=pending_admin*float(gov.one('infrastructure_usage_per_level',base.group_value(group,'infrastructure_usage_per_level')))
        demand+=admin_demand
        reserve=max(3,demand*.10)
        row=dict(state=sid,owner=tag,population=pop[sid],population_divisor=divisor,demand_full_employment=demand,new_admin_demand=admin_demand,reserve=reserve,target_capacity=demand+reserve,old_levels=old_roads,fixed_add=m[KEYS[0]],fixed_pop_add=m[KEYS[1]],fixed_pop_max=m[KEYS[2]],mult=m[KEYS[3]],road_add=road[KEYS[0]],road_pop_add=road[KEYS[1]],road_pop_max=road[KEYS[2]],canal_capacity_credit=road[KEYS[0]]-7 if sid in CANALS else 0,road_declarations=road_declarations,previous_road_modes=old_modes,selected_methods=network_pms(sid))
        row['required_levels']=minimum_levels(row)
        row['new_levels']=min(old_roads,row['required_levels'])
        row['capacity_before_if_all_turnpikes']=capacity(row,old_roads)
        row['capacity_after']=capacity(row,row['new_levels'])
        row['margin_after']=row['capacity_after']-demand
        row['removed_levels']=old_roads-row['new_levels']
        data.append(row)
    return data,dict(base_infrastructure=dict(common),country_infrastructure={k:dict(v) for k,v in country.items()},canal_states=sorted(CANALS),population_divisor=divisor,laws_examined=law_ids,game_root=str(base.qa.GAME),irish_admin_additions=IRISH_ADD)

def prepare():
    assert not (OUT/'BASELINE.json').exists(),'Immutable baseline exists.'
    assert not (ROOT/IRISH_FILE).exists(),'Do not add Irish offices twice.'
    data,inputs=contexts();before=base.qa.inventory();changes={};originals={};replacements=C.defaultdict(list)
    rows=base.declarations();counter_before=base.totals(rows)
    # Largest remainder allocation preserves ownership profiles and addresses;
    # only their level counts shrink. No other building is touched.
    from map2l_belgium import allocate
    for row in data:
        sid=row['state'];tag=row['owner'];nodes=[r for r in rows if r[:2]==(sid,tag) and base.cw.scalar(r[2].one('building'))=='building_railway']
        allocation=allocate(row['new_levels'],{i:base.levels(r[2]) for i,r in enumerate(nodes)})
        assert row['capacity_after']>=row['demand_full_employment'],sid
        for i,(_,_,node,path) in enumerate(nodes):
            assert path.is_relative_to(ROOT),'Never edit vanilla files.'
            rel=path.relative_to(ROOT).as_posix();originals.setdefault(rel,path.read_text(encoding='utf-8-sig'))
            count=allocation[i]
            if count==0:replacements[rel].append((node.start,node.end,''));continue
            holders=[h for own in node.children('add_ownership') for h in own.children() if h.children('levels')]
            shares=allocate(count,{j:int(h.one('levels')) for j,h in enumerate(holders)})
            for j,h in enumerate(holders):
                if not shares[j]:replacements[rel].append((h.start,h.end,''))
                else:
                    level=h.children('levels')[0];replacements[rel].append((level.start,level.end,'levels = '+str(shares[j])))
            pm=node.children('activate_production_methods')
            assert len(pm)==1
            replacements[rel].append((pm[0].start,pm[0].end,'activate_production_methods = { '+' '.join('"'+p+'"' for p in network_pms(sid))+' }'))
    for rel,items in replacements.items():changes[rel]=edits(originals[rel],items)
    raw=(ROOT/SALT).read_text(encoding='utf-8-sig');originals[SALT]=raw
    salt=next(n for n in base.cw.parse(raw) if n.key=='default_building_salt_pan')
    output=next(n for n in base.cw.walk(salt.children()) if n.key=='goods_output_salt_add')
    assert output.value=='10'
    changes[SALT]=edits(raw,[(output.start,output.end,'goods_output_salt_add = 20')])
    changes[IRISH_FILE]=irish_text()
    dump('BASELINE.json',dict(inventory=before,hashes=base.runtime_hashes(),originals=originals,expected_files=changes,HEAD=subprocess.check_output([base.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_sha256=base.sha(ROOT/'.git/index')))
    dump('PLAN.json',dict(states=data,inputs=inputs,total_before=sum(r['old_levels'] for r in data),total_after=sum(r['new_levels'] for r in data),bureaucracy_added=150,observed_deficit=128,nominal_surplus_after=22,irish_admin_added=15,salt_pan_before=10,salt_pan_after=20))
    old=base.patchwork.OUT
    try:base.patchwork.OUT=OUT;base.patchwork.emit(changes,'CHANGES.patch')
    finally:base.patchwork.OUT=old
    print('Prepared',len(changes),'scoped files; roads',sum(r['old_levels'] for r in data),'->',sum(r['new_levels'] for r in data),'; Irish administration +15; salt pans 10->20')

def validate():
    b=json.loads((OUT/'BASELINE.json').read_text());plan=json.loads((OUT/'PLAN.json').read_text());a=base.qa.inventory();checks=[]
    def check(name,result,detail=''):checks.append(dict(name=name,passed=bool(result),detail=detail))
    for key in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','units','errors','duplicates']:check('Preserved '+key,a[key]==b['inventory'][key])
    hashes=base.runtime_hashes()
    check('Only new Irish administration file',set(hashes)-set(b['hashes'])=={IRISH_FILE} and not(set(b['hashes'])-set(hashes)))
    check('All unrelated runtime bytes including previous addon and GUI preserved',all(hashes.get(p)==digest for p,digest in b['hashes'].items() if p not in b['expected_files']))
    for rel,text in b['expected_files'].items():check('Exact reviewed change '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==text)
    expected=base.qa.counter(b['inventory']['buildings'])
    def sigs(files):
        return C.Counter((sid,tag,base.qa.signature(n)) for text in files.values() for sid,tag,n,path in base.parse_addon(text))
    expected.subtract(sigs({p:t for p,t in b['originals'].items() if p.startswith('common/history/buildings/')}))
    expected.update(sigs({p:t for p,t in b['expected_files'].items() if p.startswith('common/history/buildings/')}))
    check('Exact building/ownership/PM semantic difference',+expected==base.qa.counter(a['buildings']))
    count_before=base.qa.counter(b['inventory']['building_levels_written']);count_before['building_railway']-=plan['total_before']-plan['total_after'];count_before['building_government_administration']+=15
    check('Exact worldwide level delta: roads reduced and 15 offices added',count_before==base.qa.counter(a['building_levels_written']))
    current=base.declarations();totals=base.totals(current)
    csv_rows=[]
    for row in plan['states']:
        sid=row['state'];tag=row['owner'];n=totals[sid,tag,'building_railway']
        road_nodes=[node for s,t,node,p in current if (s,t)==(sid,tag) and base.cw.scalar(node.one('building'))=='building_railway']
        check('Reviewed road total '+sid,n==row['new_levels'])
        check('Exact turnpike/canal/rail choices '+sid,all(base.values(node,'activate_production_methods')==network_pms(sid) for node in road_nodes))
        check('Demand covered at full employment '+sid,capacity(row,n)>=row['demand_full_employment'])
        check('No unnecessary extra level '+sid,n==0 or capacity(row,n-1)<row['target_capacity'])
        check('Existing technology for all selected infrastructure PMs '+sid,all(set(base.values(base.catalog('common/production_methods')[pm],'unlocking_technologies'))<=base.starting_tech(tag) for pm in network_pms(sid)))
        check('Canal credit only in three authorized states '+sid,(row['canal_capacity_credit']>0)==(sid in CANALS))
        csv_rows.append(dict(State_ID=sid,Owner_TAG=tag,Before=row['old_levels'],After=n,Removed=row['old_levels']-n,Canals_Active=sid in CANALS,Demand_after_offices=row['demand_full_employment'],Capacity_before_actual_methods=round(old_capacity(row),3),Capacity_full_employment=round(capacity(row,n),3),Margin=round(capacity(row,n)-row['demand_full_employment'],3)))
    pms=base.catalog('common/production_methods');bureau_per_level=sum(float(n.value) for pm in irish_pms() for n in base.cw.walk(pms[pm].children()) if n.key=='country_bureaucracy_add')
    check('Irish additional nominal bureaucracy covers deficit plus reserve',15*bureau_per_level==150 and 150>=128+20)
    for sid,n in IRISH_ADD.items():
        check('Exact new Irish office levels '+sid,sum(base.levels(node) for s,t,node,p in current if (s,t)==(sid,'IREK') and p==ROOT/IRISH_FILE)==n)
    check('Irish office PMs unlocked',all(set(base.values(pms[pm],'unlocking_technologies'))<=base.starting_tech('IREK') for pm in irish_pms()))
    check('Irish appointed-bureaucrat law respected','pm_professional_bureaucrats' in irish_pms() and 'pm_hereditary_bureaucrats' not in irish_pms())
    pan=pms['default_building_salt_pan'];mine=pms['pm_picks_and_shovels_building_salt_mine']
    check('Salt pans now output 20',next(n.value for n in base.cw.walk(pan.children()) if n.key=='goods_output_salt_add')=='20')
    check('Salt mine output remains 20',next(n.value for n in base.cw.walk(mine.children()) if n.key=='goods_output_salt_add')=='20')
    # Initial requested industry/agriculture must remain exactly as installed.
    check('Previous player building addon untouched',hashes[base.NEW]==b['hashes'][base.NEW])
    with (base.OUT/'BUILDING_CHANGES.csv').open(encoding='utf-8-sig') as f:
        for initial in csv.DictReader(f):
            key=(initial['State_ID'],initial['Owner_TAG'],initial['Building'])
            check('Initial requested final total preserved '+' '.join(key),totals[key]==int(initial['After']))
    check('Previous China/continental infrastructure forecast unchanged',base.forecast(current)==json.loads((base.OUT/'INFRASTRUCTURE_AFTER.json').read_text()))
    check('Six Brandenburg arms levels intact',totals['STATE_BRANDENBURG','PRU','building_arms_industry']==6)
    check('341 Swedish core cells and full map byte-identical',hashes['map_data/provinces.png']==b['hashes']['map_data/provinces.png'])
    check('HEAD and index unchanged',subprocess.check_output([base.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['HEAD'] and base.sha(ROOT/'.git/index')==b['index_sha256'])
    with (OUT/'STATE_REBALANCE.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(csv_rows[0]));writer.writeheader();writer.writerows(csv_rows)
    old_entries=[(decl['levels'],methods) for row in plan['states'] for decl,methods in zip(row['road_declarations'],row['previous_road_modes'])]
    new_entries=[(row['new_levels'],network_pms(row['state'])) for row in plan['states']]
    dump('FULL_STAFF_INPUTS.json',dict(roads_before=staffing_and_inputs(old_entries),roads_after=staffing_and_inputs(new_entries),irish_offices_added=staffing_and_inputs([(15,irish_pms())]),note='Physical full-staff nominal PM quantities, not money or engine hiring measurements. No economy-of-scale or market-price simulation.'))
    report=dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,engine_tested=False,runtime_status='NOT_YET_TESTED',roads_before=plan['total_before'],roads_after=plan['total_after'],canal_states=sorted(CANALS),irish_offices_added=15,irish_bureaucracy_nominal_added=150,irish_observed_deficit=128,salt_pan_output=20,note='Full employment and normal input supply assumptions; no currency deficit, initial hiring level or exact month-one balance is certified. Highlands retains one level with positive coverage but less than the default reserve; no extra level added solely for that buffer.')
    dump('VALIDATION.json',report);print(report['status'],sum(c['passed'] for c in checks),'/',len(checks))
    for c in checks:
        if not c['passed']:print('FAIL',c['name'],c['detail'])
    return int(not all(c['passed'] for c in checks))

def audit():
    data,inputs=contexts();dump('AUDIT.json',dict(states=data,inputs=inputs))
    print(json.dumps(inputs,ensure_ascii=False))
    for r in data:print(r['state'],r['old_levels'],'->',r['new_levels'],'demand',r['demand_full_employment'],'capacity',round(r['capacity_after'],2),'margin',round(r['margin_after'],2),'modes',r['previous_road_modes'])
    print('TOTAL',sum(r['old_levels'] for r in data),'->',sum(r['new_levels'] for r in data))

if __name__=='__main__':
    if sys.argv[1]=='audit':audit()
    elif sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='validate':raise SystemExit(validate())
    else:raise SystemExit('Unknown action')
