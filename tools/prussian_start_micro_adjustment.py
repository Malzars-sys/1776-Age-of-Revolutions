"""Narrow player-authorised start-economy adjustment; no territorial edits."""
import collections as C,json,sys,subprocess
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as parser
from map_1776_audit import effective,values
from map2a_patch import edits
from map2b_patch import region
from map2l_belgium import sha
import map2l_mainz as core

ROOT=qa.ROOT
OUT=ROOT/'docs/reports/economy/PRUSSIA_MICRO_ADJUSTMENT_2026_10_14'
NEW='common/history/buildings/99_1776_prussian_start_micro_adjustment.txt'
WEST='common/history/buildings/00_west_europe.txt'
EAST='common/history/buildings/02_east_europe.txt'
REDISTRIBUTION='common/history/buildings/98_build_start_1776_world_redistribution.txt'
RELEVEL=[(WEST,'STATE_BRANDENBURG','building_government_administration',13,7),(WEST,'STATE_BRANDENBURG','building_arms_industry',4,6),(EAST,'STATE_UPPER_SILESIA','building_iron_mine',1,3),(REDISTRIBUTION,'STATE_BRANDENBURG','building_livestock_ranch',8,4)]
FARMS={'STATE_LOWER_SILESIA':2,'STATE_POMERANIA':2}
DELTAS={'building_government_administration':-6,'building_arms_industry':2,'building_iron_mine':2,'building_lead_mine':1,'building_paper_mill':2}

def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def buildings(raw,sid):
    try:return region(raw,sid,'PRU').children('create_building')
    except StopIteration:return []

def catalog(folder):
    return {n.key:n for path in effective(ROOT,qa.GAME,'common/'+folder) for n in parser.parse(path.read_text(encoding='utf-8-sig'))}

def infra(files):
    """Nominal written-data forecast; never an engine/market-access result."""
    definitions=catalog('buildings');groups=catalog('building_groups');pms=catalog('production_methods');traits=catalog('state_traits')
    regions={n.key:n for path in effective(ROOT,qa.GAME,'map_data/state_regions') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    static=catalog('static_modifiers');base=float(static['base_values'].one('state_infrastructure_add'))
    def usage(group):
        node=groups[group]
        if node.children('infrastructure_usage_per_level'):return float(node.one('infrastructure_usage_per_level'))
        parent=node.one('parent_group','');return usage(parent) if parent else 0
    written=[]
    for path in effective(ROOT,qa.GAME,'common/history/buildings'):
        rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        written.append(files.get(rel,path.read_text(encoding='utf-8-sig')))
    if NEW in files and not (ROOT/NEW).exists():written.append(files[NEW])
    rows=[]
    for sid in FARMS:
        demand=supply=arable=0
        for raw in written:
            for b in buildings(raw,sid):
                levels=sum(int(v.value) for v in parser.walk(b.children()) if v.key=='levels');definition=definitions[parser.scalar(b.one('building'))];group=definition.one('building_group')
                per_level=float(definition.one('infrastructure_usage_per_level')) if definition.children('infrastructure_usage_per_level') else usage(group)
                demand+=levels*per_level
                for pm in values(b,'activate_production_methods'):
                    for state_modifier in pms[pm].children('state_modifiers'):
                        supply+=levels*sum(float(v.value) for v in parser.walk(state_modifier.children()) if v.key=='state_infrastructure_add')
                cursor=group
                while cursor:
                    if groups[cursor].one('land_usage','')=='rural':arable+=levels;break
                    cursor=groups[cursor].one('parent_group','')
        fixed_traits=sum(float(v.value) for trait in values(regions[sid],'traits') for v in parser.walk(traits[trait].children()) if v.key=='state_infrastructure_add')
        capacity=base+fixed_traits+supply
        rows.append(dict(state=sid,owner='PRU',written_building_demand=demand,base_infrastructure=base,fixed_trait_infrastructure=fixed_traits,full_staffing_PM_supply=supply,nominal_capacity=capacity,nominal_margin=capacity-demand,written_rural_levels=arable,regional_arable_land=int(regions[sid].one('arable_land')),warning='Written-data forecast only: excludes population/technology/company bonuses, generated urban/military buildings, dynamic modifiers, staffing and input shortages. Actual engine infrastructure remains to be checked.'))
    return rows

def prepare():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'BASELINE.json').exists(),'Immutable actual baseline';assert not (ROOT/NEW).exists()
    originals={rel:(ROOT/rel).read_text(encoding='utf-8-sig') for rel in [WEST,EAST,REDISTRIBUTION]};files={};ops=C.defaultdict(list)
    for rel,sid,kind,before,after in RELEVEL:
        nodes=[n for n in buildings(originals[rel],sid) if parser.scalar(n.one('building'))==kind];assert len(nodes)==1
        levels=[n for n in parser.walk(nodes[0].children()) if n.key=='levels'];assert len(levels)==1 and int(levels[0].value)==before
        ops[rel].append((levels[0].start,levels[0].end,'levels = '+str(after)))
    for rel in originals:files[rel]=edits(originals[rel],ops[rel])
    ranch=next(b for b in buildings(originals[REDISTRIBUTION],'STATE_BRANDENBURG') if parser.scalar(b.one('building'))=='building_livestock_ranch');level=next(n for n in parser.walk(ranch.children()) if n.key=='levels');raw=originals[REDISTRIBUTION][ranch.start:ranch.end]
    # Keep the same Brandenburg manor owner, recipes and reserves; only the
    # producing state's physical location changes for the four moved levels.
    moved={sid:edits(raw,[(level.start-ranch.start,level.end-ranch.start,'levels = '+str(count))]) for sid,count in FARMS.items()}
    def new_building(kind,level,sid,pms):
        return 'create_building = { building = "'+kind+'" add_ownership = { building = { type = "building_financial_district" country = "c:PRU" levels = '+str(level)+' region = "'+sid+'" } } reserves = 1 activate_production_methods = { '+' '.join('"'+pm+'"' for pm in pms)+' } }'
    additions={**moved,'STATE_BRUNSWICK':new_building('building_lead_mine',1,'STATE_BRUNSWICK',['pm_picks_and_shovels_building_lead_mine','pm_no_explosives','pm_no_steam_automation','pm_road_carts','pm_no_ore_concentration_building_lead_mine','pm_no_mine_ventilation']),'STATE_WEST_PRUSSIA':new_building('building_paper_mill',2,'STATE_WEST_PRUSSIA',['pm_pulp_pressing','pm_automation_disabled'])}
    files[NEW]='BUILDINGS = {\n'+''.join(' s:'+sid+' = { region_state:PRU = {\n'+body+'\n } }\n' for sid,body in additions.items())+'}\n'
    for raw in files.values():parser.parse(raw)
    before=qa.inventory();assert all([sid,'PRU'] in before['states'] for sid in additions)
    forecast=infra(files);assert all(r['nominal_margin']>=0 and r['written_rural_levels']<=r['regional_arable_land'] for r in forecast)
    hashes={p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','map_data','gui','gfx','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    dump('BASELINE.json',dict(inventory=before,hashes=hashes,originals=originals,expected_files=files,HEAD=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_sha256=sha(ROOT/'.git/index')))
    dump('INFRASTRUCTURE_FORECAST.json',forecast)
    oldout=core.OUT
    try:core.OUT=OUT;changed=core.emit(files,'CHANGES.patch')
    finally:core.OUT=oldout
    dump('PLAN.json',dict(files=changed,relevels=[dict(file=r[0],state=r[1],owner='PRU',building=r[2],before=r[3],after=r[4]) for r in RELEVEL],moved_ranches=FARMS,ranch_economic_owner_preserved='c:PRU / building_manor_house / STATE_BRANDENBURG',new_lead_mine='STATE_BRUNSWICK / PRU only; BRA and HAN untouched',new_paper_mill='STATE_WEST_PRUSSIA / PRU; confirmed by player',global_level_delta=DELTAS))
    print('Prepared four scoped building files; farm destinations:',json.dumps(forecast,ensure_ascii=False))

def validate():
    b=json.loads((OUT/'BASELINE.json').read_text());a=qa.inventory();checks=[]
    def check(name,result,detail=''):checks.append(dict(name=name,passed=bool(result),detail=detail))
    for key in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','units','errors','duplicates']:check('Unchanged '+key,a[key]==b['inventory'][key])
    check('Population unchanged at 835804980',sum(r['count'] for r in a['pops'])==835804980)
    for rel,expected in b['expected_files'].items():check('Exact reviewed file '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==expected)
    for rel,digest in b['hashes'].items():
        if rel not in b['expected_files']:check('Protected original '+rel,sha(ROOT/rel)==digest)
    current={p.relative_to(ROOT).as_posix() for folder in ['common','map_data','gui','gfx','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    check('Only intended new runtime file',current-set(b['hashes'])=={NEW})
    expected=qa.counter(b['inventory']['building_levels_written'])
    for kind,count in DELTAS.items():expected[kind]+=count
    check('Exact global building-level delta, zero net ranch increase',qa.counter(a['building_levels_written'])==expected)
    # Derive exact expected semantic declaration delta independently from the
    # stored before/after files; all other buildings/holders remain identical.
    def declarations(files):
        result=C.Counter()
        for raw in files.values():
            for st in parser.walk(parser.parse(raw)):
                if not st.key.startswith('s:STATE_'):continue
                for rs in st.children():
                    if rs.key.startswith('region_state:'):
                        for node in rs.children('create_building'):result[st.key[2:],rs.key.split(':')[1],qa.signature(node)]+=1
        return result
    expected_declarations=qa.counter(b['inventory']['buildings']);expected_declarations.subtract(declarations(b['originals']));expected_declarations.update(declarations(b['expected_files']))
    check('All building declarations PMs reserves and economic holders exact',+expected_declarations==qa.counter(a['buildings']))
    data=infra({});check('Ranch forecast reproducible',data==json.loads((OUT/'INFRASTRUCTURE_FORECAST.json').read_text()))
    for row in data:check('Nominal infrastructure and land adequate '+row['state'],row['nominal_margin']>=0 and row['written_rural_levels']<=row['regional_arable_land'],str(row))
    definitions=catalog('buildings');pms=catalog('production_methods');groups=catalog('production_method_groups');tech={parser.scalar(n.value) for n in parser.walk(parser.parse((ROOT/'common/history/countries/pru - prussia.txt').read_text())) if n.key=='add_technology_researched'}
    for sid in ['STATE_BRUNSWICK','STATE_WEST_PRUSSIA',*FARMS]:
        for building in buildings(b['expected_files'][NEW],sid):
            kind=parser.scalar(building.one('building'));check('Building unlocked '+sid+' '+kind,set(values(definitions[kind],'unlocking_technologies'))<=tech)
            valid={pm for group in values(definitions[kind],'production_method_groups') for pm in values(groups[group],'production_methods')}
            for pm in values(building,'activate_production_methods'):check('Compatible unlocked method '+sid+' '+pm,pm in valid and pm in pms and set(values(pms[pm],'unlocking_technologies'))<=tech)
    regions={n.key:n for path in effective(ROOT,qa.GAME,'map_data/state_regions') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for sid,kind,required in [('STATE_BRUNSWICK','building_lead_mine',1),('STATE_UPPER_SILESIA','building_iron_mine',3)]:check('Regional resource cap adequate '+sid,int(regions[sid].children('capped_resources')[0].one(kind))>=required)
    check('HEAD and index unchanged',subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['HEAD'] and sha(ROOT/'.git/index')==b['index_sha256'])
    report=dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,runtime_status='NOT_YET_TESTED',engine_tested=False,global_level_delta=DELTAS,world_population=835804980,inherited_duplicate_RGBs=len(a['duplicates']),inherited_invalid_references=len(a['errors']),infrastructure_scope='Nominal written-data calculation, not measured in-game availability; automatic/implicit buildings and employment effects require a new-game check',past_map_and_industry_receipts_preserved_as_historical_before_this_additional_request=True)
    dump('VALIDATION.json',report);print(report['status'],sum(r['passed'] for r in checks),'/',len(checks))
    for row in checks:
        if not row['passed']:print('FAIL',row['name'],row['detail'])
    return int(not all(r['passed'] for r in checks))

def prepare_textile_removal():
    stage=OUT/'LOWER_SILESIA_TEXTILE_REMOVAL';stage.mkdir(exist_ok=True);assert not (stage/'BASELINE.json').exists()
    raw=(ROOT/EAST).read_text(encoding='utf-8-sig');nodes=[n for n in buildings(raw,'STATE_LOWER_SILESIA') if parser.scalar(n.one('building'))=='building_textile_mill'];assert len(nodes)==1
    node=nodes[0];assert sum(int(v.value) for v in parser.walk(node.children()) if v.key=='levels')==3
    changed=edits(raw,[(node.start,node.end,'')]);before=qa.inventory()
    hashes={p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','map_data','gui','gfx','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    data=dict(inventory=before,hashes=hashes,source_file=EAST,before=raw,after=changed,removed_signature=qa.signature(node),removed_levels=3,HEAD=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_sha256=sha(ROOT/'.git/index'))
    (stage/'BASELINE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    original=core.OUT
    try:core.OUT=stage;core.emit({EAST:changed},'REMOVE.patch')
    finally:core.OUT=original
    print('Prepared removal of exactly three Lower Silesian textile levels; population not removed')

def validate_textile_removal():
    stage=OUT/'LOWER_SILESIA_TEXTILE_REMOVAL';b=json.loads((stage/'BASELINE.json').read_text());a=qa.inventory();checks=[]
    def check(name,result):checks.append(dict(name=name,passed=bool(result)))
    check('Exact one reviewed building deletion',(ROOT/EAST).read_text(encoding='utf-8-sig')==b['after'])
    for key in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','units','errors','duplicates']:check('Unchanged '+key,a[key]==b['inventory'][key])
    expected=qa.counter(b['inventory']['building_levels_written']);expected['building_textile_mill']-=3
    check('Exactly three textile levels removed globally',qa.counter(a['building_levels_written'])==expected)
    declarations=qa.counter(b['inventory']['buildings']);declarations['STATE_LOWER_SILESIA','PRU',b['removed_signature']]-=1
    check('No other declaration or economic holder changed',qa.counter(a['buildings'])==+declarations)
    for rel,digest in b['hashes'].items():
        if rel!=EAST:check('Protected original '+rel,sha(ROOT/rel)==digest)
    current={p.relative_to(ROOT).as_posix() for folder in ['common','map_data','gui','gfx','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    check('No new runtime file',current==set(b['hashes']))
    check('No textile declaration remains in Prussian Lower Silesia',not any(row['key'][:2]==['STATE_LOWER_SILESIA','PRU'] and next(n[2] for n in json.loads(row['key'][2])[2] if n[0]=='building')=='building_textile_mill' for row in a['buildings']))
    check('HEAD and index unchanged',subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['HEAD'] and sha(ROOT/'.git/index')==b['index_sha256'])
    forecast=infra({});(OUT/'FINAL_INFRASTRUCTURE_FORECAST.json').write_text(json.dumps(forecast,ensure_ascii=False,indent=2),encoding='utf-8')
    check('Farm destination nominal infrastructure still adequate',all(row['nominal_margin']>=0 for row in forecast))
    totals=C.Counter()
    for row in a['buildings']:
        sid,owner,body=row['key']
        if owner!='PRU':continue
        n=json.loads(body)
        kind=next(v[2] for v in n[2] if v[0]=='building')
        def levels(v):return int(v[2]) if v[0]=='levels' else sum(levels(child) for child in v[2]) if isinstance(v[2],list) else 0
        totals[sid,kind]+=levels(n)*row['count']
    intended=[('STATE_BRANDENBURG','building_government_administration',7),('STATE_BRANDENBURG','building_arms_industry',6),('STATE_BRANDENBURG','building_livestock_ranch',4),('STATE_UPPER_SILESIA','building_iron_mine',3),('STATE_BRUNSWICK','building_lead_mine',1),('STATE_WEST_PRUSSIA','building_paper_mill',2),('STATE_LOWER_SILESIA','building_livestock_ranch',10),('STATE_POMERANIA','building_livestock_ranch',10),('STATE_LOWER_SILESIA','building_textile_mill',0)]
    for sid,kind,count in intended:check('Final requested total '+sid+' '+kind,totals[sid,kind]==count)
    report=dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,removed_levels=3,removed_state='STATE_LOWER_SILESIA',owner='PRU',population_removed=0,runtime_status='NOT_YET_TESTED',engine_tested=False,phase='After separately validated Prussian micro-adjustment and explicit additional textile deletion')
    (stage/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(report['status'],sum(r['passed'] for r in checks),'/',len(checks))
    for r in checks:
        if not r['passed']:print('FAIL',r['name'])
    return int(not all(r['passed'] for r in checks))

if __name__=='__main__':raise SystemExit({'prepare':prepare,'validate':validate,'prepare-textile-removal':prepare_textile_removal,'validate-textile-removal':validate_textile_removal}[sys.argv[1]]() or 0)
