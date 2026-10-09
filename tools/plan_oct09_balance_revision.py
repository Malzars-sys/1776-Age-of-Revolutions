"""Plan authorized October 9 balance changes; runtime writes use apply_patch only.

The ignored baseline is immutable. --check validates that exact patch, preserved
art/populations, technology references and initial formations. Not an engine test.
"""
from __future__ import annotations
import argparse
import collections
import difflib
import hashlib
import json
import math
import re
from pathlib import Path
import audit_british_colonial_start as old
import build_start_1776_research_input_pack as cat
import build_start_1776_world_apply as world
import build_start_1776_runtime_wave1 as infra

ROOT = world.ROOT
CACHE = ROOT / '.asset-cache/oct09_balance_revision'
ADVANCED = {'GBR','FRA','SPA','RUS','POR','NET','DEN','DENNOR','NOR','SWE'}
COASTAL = {'TUR','VEN','GEN','SAR','SIC','PAP','TUS','AUS','TUN','TRI'}
TECH_MAP = {
    'aor_cog_construction': 'state_dockyard_systems',
    'aor_galley_construction': 'state_dockyard_systems',
    'aor_caravel_construction': 'enclosed_dock_systems',
    'aor_frigate_construction': 'marine_chronometry',
    'aor_line_ship_construction': 'standardized_naval_signals',
    'aor_carronade_mountings': 'copper_sheathing',
    'aor_diagonal_ship_framing': 'diagonal_ship_framing',
}
COLONIES = {'ONT': ('STATE_ONTARIO',5), 'QUE': ('STATE_QUEBEC',5),
            'NBS': ('STATE_NEW_BRUNSWICK',2), 'NVS': ('STATE_NEW_BRUNSWICK',3),
            'HBC': ('STATE_MANITOBA',2)}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def set_number(text,key,value):
    text,n = re.subn(r'(\b'+re.escape(key)+r'\s*=\s*)-?[0-9.]+',
                    lambda m:m[1]+str(value),text,count=1)
    if n != 1: raise ValueError('Missing field '+key)
    return text

def replace_block(text,key,new):
    spans = world.block_spans(text,key,1)
    if len(spans)!=1: raise ValueError('Missing/duplicate block '+key)
    _,a,b=spans[0]
    indent=re.match(r'[ \t]*',text[a:b])[0]
    return text[:a]+indent+key+' = {\n'+''.join(indent+'    '+k+' = '+str(v)+'\n' for k,v in new.items())+indent+'}'+text[b:]

def edit_object(raw,key,fn):
    spans=world.block_spans(raw,re.escape(key),0)
    if len(spans)!=1: raise ValueError('Missing/duplicate object '+key)
    _,a,b=spans[0]
    return raw[:a]+fn(raw[a:b])+raw[b:]

def unit(kind,state,count,service='regular'):
    return ('\n\t\t\tcombat_unit = {\n\t\t\t\ttype = unit_type:'+kind+'\n'
            +(f'\t\t\t\tservice_type = {service}\n' if service!='regular' else '')
            +f'\t\t\t\tstate_region = s:{state}\n\t\t\t\tcount = {count}\n\t\t\t}}\n')

def infantry(tag,tech,units):
    order=['irregular_infantry','musket_infantry','line_infantry','skirmish_infantry',
           'trench_infantry','squad_infantry','mechanized_infantry']
    valid=[]
    for name in order:
        key='combat_unit_type_'+name
        req=cat.tokens_flat(cat.braced_tokens(units[key].text,'unlocking_technologies'))
        if not req or any(t in tech.get(tag,set()) for t in req): valid.append(key)
    return valid[-1]

def prepare():
    CACHE.mkdir(parents=True,exist_ok=True)
    basepath=CACHE/'baseline.json'
    if basepath.exists(): raise ValueError('Baseline already exists; do not overwrite it')
    expected={}; before={}; report={'engine_tested':False,'rye':[], 'colonies':[], 'naval_admin':[]}
    def read(path):
        if path not in before: before[path]=(ROOT/path).read_text(encoding='utf-8-sig') if (ROOT/path).exists() else None
        return expected.get(path,before[path])
    def save(path,raw):
        if path not in before: read(path)
        expected[path]=raw

    path='common/production_methods/01_industry.txt';raw=read(path)
    raw=edit_object(raw,'pm_thomas_process',lambda t:set_number(t,'goods_input_iron_add',55))
    raw=edit_object(raw,'pm_bessemer_process',lambda t:t)  # Guard this neighboring PM.
    def coke(t):
        for k,n in {'goods_input_iron_add':25,'goods_input_coal_add':25,'goods_output_steel_add':40}.items(): t=set_number(t,k,n)
        return t
    raw=edit_object(raw,'pm_coke_blast_furnaces',coke)
    def tools(t):
        t=set_number(t,'goods_input_iron_add',15)
        return re.sub(r'(goods_input_iron_add\s*=\s*15)',r'\1\n\t\t\tgoods_input_steel_add = 3',t,count=1)
    raw=edit_object(raw,'pm_pig_iron',tools);save(path,raw)
    report['recipes']={'thomas_iron':55,'coke':{'iron':25,'coal':25,'steel':40},'wrought_tools':{'iron':15,'steel':3}}

    raws,ps=world.all_placements(world.HISTORY)
    edits=collections.defaultdict(list)
    rye=collections.defaultdict(list)
    for p in ps:
        if p.owner=='GBR' and p.building in {'building_tooling_workshop','building_tooling_workshops'}:
            new=world.replace_active_pms(p.text,[('pm_pig_iron' if k in {'pm_crude_tools','pm_steel','pm_steel_tools','pm_pig_iron'} else k) for k in p.pms])
            edits[p.path].append((p.start,p.end,new))
        if p.owner=='GBR' and p.building=='building_rye_farm': rye[p.state].append(p)
    for state,rows in rye.items():
        # Change one placement per state, not each repeated create_building.
        p=rows[-1];remove=min(5,max(1,math.ceil(p.level/4)),sum(x.level for x in rows)-1)
        if remove:
            edits[p.path].append((p.start,p.end,world.rescale_ownership(p.text,p.level-remove)))
        report['rye'].append({'state':state,'removed':remove,'edited_placement_before':p.level,'after':p.level-remove})

    tech=old.technology_sets()
    units=cat.effective_objects('common/combat_unit_types',r'combat_unit_type_[A-Za-z0-9_]+')
    add_buildings=[]
    def building(owner,state,kind,n,pms):
        add_buildings.append((owner,state,kind,n,pms))
    for tag,(state,n) in COLONIES.items():
        kind=infantry(tag,tech,units)
        report['colonies'].append({'tag':tag,'state':state,'regiments':n,'infantry':kind})
        existing=sum(p.level for p in ps if p.key==(tag,state,'building_barrack'))
        if existing<n: building(tag,state,'building_barrack',n-existing,['pm_no_organization'])
    building('GBR','STATE_BERMUDA','building_barrack',2,['pm_no_organization'])
    building('USA','STATE_RHODE_ISLAND','building_naval_administration',1,['pm_simple_sailor_recruitment'])

    # Fleet revisions preserve total counts and all commanders.
    naval={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/history/military_formations').glob('*.txt')}
    fleets=old.fleets(naval)
    fleet_report=[]
    for path,raw in naval.items():
        changes=[]
        for row in [r for r in fleets if r['path']==path]:
            t=row['text'];ships=row['ships']
            if row['owner'] in COASTAL:
                counts=collections.Counter()
                for k,n in ships: counts['ship_type_galley' if k in {'ship_type_caravel','ship_type_ship_of_the_line','ship_type_frigate','ship_type_galley'} else k]+=n
                t=old.replace_ships(t,list(counts.items()))
            if row['owner']=='GBR' and row['name']=='cleanup2d3b_gbr_naval_2':
                counts=collections.Counter(dict(ships))
                if counts['ship_type_galley']<5:raise ValueError('Not enough galleys')
                counts['ship_type_galley']-=5;counts['ship_type_frigate']+=5
                t=old.replace_ships(t,[(k,n) for k,n in counts.items() if n])
                t=t.replace('hq_region = sr:region_western_europe','hq_region = sr:region_atlantic_coast\n\t\t\tsupply_hub = s:STATE_BERMUDA')
            fleet_report.append({'owner':row['owner'],'name':row['name'],'before':ships,'after':old.ships(t)})
            if t!=row['text']: changes.append((row['start'],row['end'],t))
        # Armies: change headquarters, not recruitment origin of regular units.
        for owner,a,b in old.country_spans(raw):
            if owner.split()[0]!='c:GBR':continue
            country=raw[a:b]
            for _,x,y in world.block_spans(country,'create_military_formation',1):
                t=country[x:y];name=cat.scalar(t,'name')
                if name not in {'cleanup2d3b_gbr_land_2','cleanup2d3b_gbr_land_3'}:continue
                t=re.sub(r'hq_region\s*=\s*sr:\w+','hq_region = sr:region_canada',t,count=1)
                t=re.sub(r'(hq_region = sr:region_canada)',r'\1\n\t\t\tsupply_hub = s:STATE_NEWFOUNDLAND',t,count=1)
                if name=='cleanup2d3b_gbr_land_2':
                    spans=world.block_spans(t,'combat_unit',1)
                    for _,u,v in reversed(spans):
                        if cat.scalar(t[u:v],'service_type')=='conscript': t=t[:u]+t[v:]
                    insertion=unit('combat_unit_type_line_infantry','STATE_HOME_COUNTIES',5,'conscript')+unit('combat_unit_type_line_infantry','STATE_LANCASHIRE',5,'conscript')+unit('combat_unit_type_improved_cannon_artillery','STATE_BERMUDA',2)
                    pos=t.rfind('save_scope_as');t=t[:pos]+insertion+'\t\t\t'+t[pos:]
                changes.append((a+x,a+y,t))
        for x,y,t in sorted(changes,reverse=True):raw=raw[:x]+t+raw[y:]
        if raw!=naval[path]:save(path,raw)
    report['fleets']=fleet_report

    path='common/history/military_formations/01_military_formations_north_america.txt';raw=read(path)
    # HBC already has a formation/commander; upgrade it rather than creating a duplicate.
    for _,a,b in old.country_spans(raw):
        if not raw[a:b].lstrip().startswith('c:HBC'):continue
        chunk=raw[a:b];row=next(r for r in report['colonies'] if r['tag']=='HBC')
        chunk=chunk.replace('combat_unit_type_irregular_infantry',row['infantry'])
        chunk=set_number(chunk,'count',2);raw=raw[:a]+chunk+raw[b:];break
    pos=raw.rfind('}')
    addition=''
    for row in report['colonies']:
        if row['tag']=='HBC':continue
        addition+=f"\n\tc:{row['tag']} ?= {{\n\t\tcreate_military_formation = {{\n\t\t\ttype = army\n\t\t\thq_region = sr:region_canada\n\t\t\tsupply_hub = s:{row['state']}\n\t\t\tname = aor_{row['tag'].lower()}_garrison\n"+unit(row['infantry'],row['state'],row['regiments'])+'\t\t}\n\t}\n'
    save(path,raw[:pos]+addition+raw[pos:])
    save('common/history/military_deployments/10_1776_north_american_mobilization.txt',
         '# Mobilization occurs after formation creation. Native supported effect.\nMILITARY_DEPLOYMENTS = {\n\tc:GBR ?= {\n\t\tscope:cleanup2d4_formation_019 ?= {\n\t\t\tfully_mobilize_army = yes\n\t\t}\n\t}\n}\n')

    # Naval manpower audit includes the native default middle equipment for slots
    # not explicitly overridden (SHIP_TEMPLATE_DEFAULT_MODIFICATION_LEVEL = 2).
    ships=cat.effective_objects('common/ship_types',r'ship_type_[A-Za-z0-9_]+')
    mods=cat.effective_objects('common/ship_modifications',r'[A-Za-z0-9_]+')
    crew=collections.Counter()
    for row in fleet_report:
        for key,n in row['after']:
            t=ships[key].text
            explicit=cat.tokens_flat(cat.braced_tokens(t,'default_modifications'))
            extra=sum(infra.number(mods[m].text,'ship_crew_max_add') for m in explicit if m in mods)
            # Early galley defaults gain five rowers in this revision.
            if key=='ship_type_galley':extra+=5
            crew[row['owner']]+=n*(infra.number(t,'ship_crew_max_add')+extra)
    for tag in sorted(ADVANCED|COASTAL|{'USA'}):
        rows=[p for p in ps if p.owner==tag and p.building=='building_naval_administration']
        levels=sum(p.level for p in rows)
        # Existing large excesses are kept; only insufficient capacity is expanded.
        required=math.ceil(crew[tag]*1.2/1000)
        extra=max(0,required-levels)
        if extra and rows:
            p=max(rows,key=lambda p:p.level)
            edits[p.path].append((p.start,p.end,world.rescale_ownership(p.text,p.level+extra)))
        report['naval_admin'].append({'country':tag,'crew_estimate':crew[tag],'levels_before':levels,'minimum_with_20_percent_reserve':required,'added':extra if rows else 0})
    for p,changes in edits.items():
        path=p.relative_to(ROOT).as_posix();raw=read(path)
        for a,b,t in sorted(changes,reverse=True):raw=raw[:a]+t+raw[b:]
        save(path,raw)
    grouped=collections.defaultdict(list)
    for tag,state,kind,n,pms in add_buildings:
        grouped[state,tag].append((kind,n,pms))
    text='# Authorized additional Canadian support and Rhode Island naval administration.\nBUILDINGS = {\n'
    for (state,tag),rows in grouped.items():
        text+=f'\ts:{state} = {{\n\t\tregion_state:{tag} = {{\n'
        for kind,n,pms in rows:
            text+=f'\t\t\tcreate_building = {{\n\t\t\t\tbuilding = "{kind}"\n\t\t\t\tadd_ownership = {{ country = {{ country = "c:{tag}" levels = {n} }} }}\n\t\t\t\treserves = 1\n\t\t\t\tactivate_production_methods = {{ '+ ' '.join('"'+k+'"' for k in pms)+' }\n\t\t\t}\n'
        text+='\t\t}\n\t}\n'
    save('common/history/buildings/99_1776_oct09_balance.txt',text+'}\n')

    path='common/history/countries/gbr - great britain.txt';raw=read(path)
    raw=raw.replace('\t\tset_export_tariff_level = {\n\t\t\tgoods = g:opium', '\t\tset_export_tariff_level = {\n\t\t\tgoods = g:tools\n\t\t\tlevel = low_subventions\n\t\t}\n\t\tset_export_tariff_level = {\n\t\t\tgoods = g:opium',1)
    save(path,raw)

    # Existing naval technologies only; no new tree nodes or changed tech effects.
    for path in ['common/ship_types/10_1776_early_ships.txt','common/ship_types/00_ship_types.txt','common/ship_modifications/10_1776_early_equipment.txt']:
        raw=read(path)
        for a,b in TECH_MAP.items():raw=re.sub(r'\b'+a+r'\b',b,raw)
        if path.endswith('10_1776_early_ships.txt'):
            for hull,one,two in [('caravel','aor_caravel_blockade','aor_caravel_landing'),('galley','aor_galley_coastal_battery','aor_galley_boarding_spur')]:
                raw=raw.replace(f'ship_mod_slot_utility_1 = {{ {one} }}\n        ship_mod_slot_utility_2 = {{ {two} }}',f'ship_mod_slot_utility_1 = {{ {one} {two} }}')
                raw=raw.replace(f'\n        ship_mod_slot_utility_2 = {two}','')
            raw=raw.replace('modification_construction_cost = 0.5','modification_construction_cost = 1')
        if path.endswith('10_1776_early_equipment.txt'):
            raw=raw.replace('# Default low levels add no cost; optional utilities are intentionally inexpensive.','# Every equipment tier adds goods, useful statistics and construction complexity.')
            for hull in ('caravel','galley','cog'):
                for slot in ('armor','guns','propulsion','range'):
                    key=f'aor_{hull}_{slot}_low'
                    stats={'armor':{'ship_hit_points_max_add':30,'ship_armor_add':0.5},
                           'guns':{'ship_hull_damage_add':1,'ship_crew_damage_add':0.5},
                           'propulsion':{'ship_movement_speed_add':0.2},
                           'range':{'ship_supply_capacity_add':2}}[slot].copy()
                    if hull=='galley' and slot=='propulsion':stats['ship_crew_max_add']=5
                    if hull=='cog' and slot=='range':stats['ship_carrying_capacity_add']=0.05
                    stats['ship_construction_progress_max_add']=1
                    goods={'armor':{'goods_input_hardwood_add':2,'goods_input_tools_add':0.25},
                           'guns':{'goods_input_iron_add':0.25,'goods_input_tools_add':0.1},
                           'propulsion':{'goods_input_fabric_add':1,'goods_input_hardwood_add':0.5},
                           'range':{'goods_input_hardwood_add':1,'goods_input_fabric_add':0.5}}[slot]
                    raw=edit_object(raw,key,lambda t,s=stats,g=goods:replace_block(replace_block(t,'modifier',s),'construction_goods',g))
            # Keep second and third tiers genuinely better than the first.
            for hull in ('caravel','galley','cog'):
                raw=edit_object(raw,f'aor_{hull}_propulsion_mid',lambda t:set_number(t,'ship_movement_speed_add',0.4))
                raw=edit_object(raw,f'aor_{hull}_propulsion_high',lambda t:set_number(t,'ship_movement_speed_add',0.8))
            # Naval, already-existing gates for batteries rather than a new node.
            raw=raw.replace('armament_standardization_inspection','scientific_naval_architecture')
            raw=edit_object(raw,'aor_galley_guns_high',lambda t:t.replace('scientific_naval_architecture','ship_classification_surveying'))
        save(path,raw)
    path='common/technology/technologies/26_1776_early_ship_construction.txt';read(path);expected[path]=None
    path='common/history/countries/99_1776_ship_construction_grants.txt';raw=read(path)
    tags=[o.split()[0].removeprefix('c:') for o,a,b in old.country_spans(raw)]
    raw='# Existing naval technology grants; no dedicated ship-construction nodes.\nCOUNTRIES = {\n'
    for tag in sorted(tags):
        keys={'state_dockyard_systems','enclosed_dock_systems'}
        if tag in ADVANCED:keys|={'scientific_naval_architecture','ship_classification_surveying','marine_chronometry','standardized_naval_signals'}
        raw+=f'    c:{tag} ?= {{\n'+''.join(f'        add_technology_researched = {k}\n' for k in sorted(keys))+'    }\n'
    save(path,raw+'}\n')
    for lang in ('english','french'):
        path=f'localization/{lang}/1776_early_ship_equipment_l_{lang}.yml';raw=read(path)
        raw='\n'.join(line for line in raw.splitlines() if not any(re.match(r'\s*'+k+r'(?:_desc)?:',line) for k in TECH_MAP))+'\n'
        raw=raw.replace('compatible with blockade organization.','dedicated to landing troops. Only one function modification can be fitted.').replace("compatibles avec l'organisation du blocus.","destinées au débarquement des troupes. Une seule modification de fonction peut être montée.")
        save(path,raw)
        names={'ONT':('Ontario Garrison','Garnison de l’Ontario'),'QUE':('Quebec Garrison','Garnison du Québec'),'NBS':('New Brunswick Garrison','Garnison du Nouveau-Brunswick'),'NVS':('Nova Scotia Garrison','Garnison de Nouvelle-Écosse')}
        save(f'localization/{lang}/1776_canadian_garrisons_l_{lang}.yml','l_'+lang+':\n'+''.join(f' aor_{tag.lower()}_garrison: "{n[lang=="french"]}"\n' for tag,n in names.items()))
        path=f'localization/{lang}/1776_early_ships_l_{lang}.yml';raw=read(path)
        desc={
          'french': {
            'caravel': "Développées dans la péninsule Ibérique, les caravelles ont accompagné les explorations atlantiques des XVe et XVIe siècles. Leur gréement à voile permet les longues traversées. Dans la flotte, elles assurent la projection navale, le blocus et le soutien des débarquements.",
            'galley': "Longues et étroites, les galères associent rames et voiles. Elles ont longtemps servi les marines de Méditerranée, où leur propulsion à rames facilite les manœuvres près des côtes. Leur batterie de proue et leurs soldats d'abordage défendent ports et détroits ; l'éloignement des bases réduit leur efficacité.",
            'cog': "Navire marchand des mers du Nord et de la Baltique, la cogue a accompagné l'essor du commerce hanséatique au Moyen Âge. Sa coque et sa cale accueillent des cargaisons importantes. Réquisitionnée par la marine, elle transporte troupes, vivres et matériel et soutient les débarquements."},
          'english': {
            'caravel': "Developed in Iberia, caravels accompanied Atlantic exploration during the fifteenth and sixteenth centuries. Their sailing rigs supported long voyages. In the fleet, they provide naval power projection, blockade and support for landings.",
            'galley': "Long and narrow, galleys combine oars and sails. They served Mediterranean navies for centuries, using rowing power to maneuver near the coast. Bow batteries and boarding troops defend ports and straits; operating far from their bases reduces their effectiveness.",
            'cog': "A merchant vessel of the North and Baltic seas, the cog accompanied the growth of Hanseatic trade during the Middle Ages. Its hull and hold carry substantial cargoes. Requisitioned for naval service, it transports troops, provisions and equipment and supports landings."}}
        for hull,d in desc[lang].items(): raw=re.sub(r'( ship_type_'+hull+r'_desc:[^\"]*)\"[^\"]*\"',lambda m:m[1]+'"'+d+'"',raw)
        save(path,raw)

    # Do not modify definitions outside the planned scope, or any approved artwork.
    protected={p.relative_to(ROOT).as_posix():digest(p) for folder in ('common','gfx','gui','localization') for p in (ROOT/folder).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in expected}
    baseline={'before':before,'expected':expected,'protected':protected,'report':report}
    basepath.write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
    patch='*** Begin Patch\n'
    for path,new in expected.items():
        prev=before[path]
        if new is None:patch+='*** Delete File: '+path+'\n'
        elif prev is None:patch+='*** Add File: '+path+'\n'+''.join('+'+line+'\n' for line in new.splitlines())
        else:patch+=old.patch_file(path,prev,new)
    patch+='*** End Patch'
    print(json.dumps({'patch':patch,'report':report},ensure_ascii=False))

def prepare_crew_amendment():
    """Preserve the original baseline; record the evidence-backed crew correction."""
    base=json.loads((CACHE/'baseline.json').read_text(encoding='utf-8'))
    expected=base['expected'].copy()
    path='common/ship_types/10_1776_early_ships.txt'
    raw=expected[path]
    for hull,n in [('caravel',100),('galley',200),('cog',100)]:
        raw=edit_object(raw,'ship_type_'+hull,lambda t,n=n:set_number(t,'ship_crew_max_add',n))
    raw=raw.replace('# crew 30% of the corresponding class. Combat capability remains lower.',
                    '# Crew uses whole 100-sailor assignment slots. Combat capability remains lower.')
    expected[path]=raw
    path='common/ship_modifications/10_1776_early_equipment.txt'
    raw=expected[path]
    for tier in ('low','mid','high'):
        raw=edit_object(raw,'aor_galley_propulsion_'+tier,lambda t:set_number(t,'ship_crew_max_add',0))
    expected[path]=raw
    # Relocate existing capacity, do not enlarge the British salary bill.
    raws,placements=world.all_placements(world.HISTORY)
    path='common/history/buildings/00_west_europe.txt'
    home=next(p for p in placements if p.key==('GBR','STATE_HOME_COUNTIES','building_naval_administration'))
    original=base['before'][path]
    assert home.level==11
    expected[path]=expected[path].replace(world.rescale_ownership(home.text,13),world.rescale_ownership(home.text,14),1)
    path='common/history/buildings/10_india.txt'
    ceylon=next(p for p in placements if p.key==('GBR','STATE_CEYLON','building_naval_administration'))
    assert ceylon.level==3
    previous=(ROOT/path).read_text(encoding='utf-8-sig')
    expected[path]=previous[:ceylon.start]+previous[ceylon.end:]
    amendment={'expected':expected,'new_before':{path:previous},
               'crew_slots':{'caravel':100,'galley':200,'cog':100},
               'naval_admin_transfer':{'from':'STATE_CEYLON','to':'STATE_HOME_COUNTIES','levels':3,'total_unchanged':31},
               'evidence':'Local save dated 1776.1.31: slots of 100; Ceylon failed officer hires, qualifying_workforce=0, staffing=0.95898/3.'}
    target=CACHE/'crew_amendment.json'
    if target.exists():raise ValueError('Crew amendment already exists; preserve it')
    target.write_text(json.dumps(amendment,indent=2,ensure_ascii=False),encoding='utf-8')
    patch='*** Begin Patch\n'
    for path,new in expected.items():
        oldtext=base['before'].get(path,previous if path in amendment['new_before'] else None)
        if new is None:patch+='*** Delete File: '+path+'\n'
        elif oldtext is None:patch+='*** Add File: '+path+'\n'+''.join('+'+l+'\n' for l in new.splitlines())
        elif oldtext!=new:
            patch+='*** Update File: '+path+'\n'
            # Zero-context hunks avoid BOM/header normalization and unrelated text.
            for l in list(difflib.unified_diff(oldtext.splitlines(),new.splitlines(),n=0))[2:]:
                patch+=('@@' if l.startswith('@@') else l.rstrip('\n'))+'\n'
    patch+='*** End Patch'
    print(json.dumps({'patch':patch},ensure_ascii=True))

def prepare_crew_ceiling():
    """Latest user choice: round sailor demand upward, not downward."""
    base=json.loads((CACHE/'baseline.json').read_text(encoding='utf-8'))
    previous=json.loads((CACHE/'crew_amendment.json').read_text(encoding='utf-8'))
    expected=previous['expected'].copy()
    path='common/ship_types/10_1776_early_ships.txt'
    raw=expected[path]
    for hull,n in [('caravel',200),('galley',300),('cog',100)]:
        raw=edit_object(raw,'ship_type_'+hull,lambda t,n=n:set_number(t,'ship_crew_max_add',n))
    expected[path]=raw
    path='common/history/buildings/00_west_europe.txt'
    _,placements=world.all_placements(world.HISTORY)
    home=next(p for p in placements if p.key==('GBR','STATE_HOME_COUNTIES','building_naval_administration'))
    expected[path]=expected[path].replace(world.rescale_ownership(home.text,14),world.rescale_ownership(home.text,15),1)
    amendment={**previous,'expected':expected,'crew_slots':{'caravel':200,'galley':300,'cog':100},
               'naval_admin_transfer':{'from':'STATE_CEYLON','to':'STATE_HOME_COUNTIES','levels':3,'added_in_metropole':1,'total_after':32},
               'gbr_crew_after':31400,'user_choice':'Round up to 200 / 300 sailors; 32,000 capacity suffices without the former automatic 20% surplus.'}
    target=CACHE/'crew_ceiling.json'
    if target.exists():raise ValueError('Ceiling amendment already exists')
    target.write_text(json.dumps(amendment,indent=2,ensure_ascii=False),encoding='utf-8')
    patch='*** Begin Patch\n'
    for path,new in expected.items():
        oldtext=base['before'].get(path,previous['new_before'].get(path))
        if new is None:patch+='*** Delete File: '+path+'\n'
        elif oldtext is None:patch+='*** Add File: '+path+'\n'+''.join('+'+l+'\n' for l in new.splitlines())
        elif oldtext!=new:
            patch+='*** Update File: '+path+'\n'
            for l in list(difflib.unified_diff(oldtext.splitlines(),new.splitlines(),n=0))[2:]:
                patch+=('@@' if l.startswith('@@') else l.rstrip('\n'))+'\n'
    print(json.dumps({'patch':patch+'*** End Patch'},ensure_ascii=True))

def check():
    base=json.loads((CACHE/'baseline.json').read_text(encoding='utf-8'));errors=[]
    amendment_path=CACHE/'crew_ceiling.json'
    if amendment_path.exists():
        amendment=json.loads(amendment_path.read_text(encoding='utf-8'))
        base['expected'].update(amendment['expected'])
        for path in amendment['new_before']:base['protected'].pop(path,None)
        base['report']['crew_correction']=amendment['crew_slots']
        base['report']['naval_admin_transfer']=amendment['naval_admin_transfer']
        for row in base['report']['naval_admin']:
            if row['country']=='GBR':
                row['added']=1
                row['crew_estimate']=amendment['gbr_crew_after']
                row.pop('minimum_with_20_percent_reserve',None)
    if (CACHE/'gbr_mines_followup.json').exists():
        import audit_gbr_mines_followup as mines
        record=mines.check(quiet=True)
        for path,before in record['before'].items():
            if before!=base['expected'].get(path):errors.append('Mine follow-up preceding reference mismatch '+path)
        base['expected'].update(record['expected'])
        base['report']['gbr_iron_mines_followup']=record['iron_levels']
    if (CACHE/'gbr_agriculture_followup.json').exists():
        import audit_gbr_agriculture_followup as agriculture
        record=agriculture.check(quiet=True)
        for path,before in record['before'].items():
            if path in base['expected'] and [l.rstrip() for l in before.strip().splitlines()]!=[l.rstrip() for l in base['expected'][path].strip().splitlines()]:
                errors.append('Agriculture preceding reference mismatch '+path)
            base['protected'].pop(path,None)
        base['expected'].update(record['expected'])
        base['report']['gbr_agriculture_followup']={'levels':record['levels'],'populations':record['populations']}
    for path,expected in base['expected'].items():
        p=ROOT/path
        if expected is None:
            if p.exists():errors.append('Deleted node file still present')
        elif not p.exists() or [l.rstrip() for l in p.read_text(encoding='utf-8-sig').strip().splitlines()]!=[l.rstrip() for l in expected.strip().splitlines()]:errors.append('Unexpected edit '+path)
        elif p.suffix=='.txt':cat.brace_maps(cat.clean_comments(expected))
    for path,h in base['protected'].items():
        followup=CACHE/'naval_signals_followup.json'
        if path=='common/technology/technologies/25_tech3a_naval.txt' and followup.exists():
            import audit_naval_signals_followup as signals
            record=signals.check()
            if record['prior_protected_sha256']!=h:errors.append('Naval follow-up reference does not match original protection')
            continue
        if not (ROOT/path).exists() or digest(ROOT/path)!=h:errors.append('Protected changed '+path)
    tech=cat.effective_objects('common/technology/technologies',r'[A-Za-z0-9_]+')
    for path in ('common/ship_types/10_1776_early_ships.txt','common/ship_types/00_ship_types.txt','common/ship_modifications/10_1776_early_equipment.txt'):
        text=(ROOT/path).read_text(encoding='utf-8-sig')
        if any(re.search(r'\b'+k+r'\b',text) for k in TECH_MAP):errors.append('Obsolete gate '+path)
        for m in re.finditer(r'unlocking_technologies\s*=\s*\{([^}]+)\}',text):
            for k in m[1].split():
                if k not in tech:errors.append('Invalid technology '+k)
    ship_types=cat.effective_objects('common/ship_types',r'ship_type_[A-Za-z0-9_]+')
    for hull in ('caravel','galley','cog'):
        text=ship_types['ship_type_'+hull].text
        if infra.number(text,'ship_crew_max_add')%100:errors.append('Partial sailor slot '+hull)
        if 'ship_mod_slot_utility_2' in text or 'ship_mod_slot_utility_3' in text:errors.append('Extra utility slot '+hull)
    researched=old.technology_sets()
    # Semantic checks, independent of matching the approved text patch.
    pm=cat.effective_objects('common/production_methods',r'[A-Za-z0-9_]+')
    for key,field,n in [('pm_thomas_process','goods_input_iron_add',55),
                        ('pm_coke_blast_furnaces','goods_input_iron_add',25),
                        ('pm_coke_blast_furnaces','goods_input_coal_add',25),
                        ('pm_coke_blast_furnaces','goods_output_steel_add',40),
                        ('pm_pig_iron','goods_input_iron_add',15),
                        ('pm_pig_iron','goods_input_steel_add',3)]:
        if key not in pm or infra.number(pm[key].text,field)!=n:errors.append('Recipe mismatch '+key+':'+field)
    equipment=cat.effective_objects('common/ship_modifications',r'[A-Za-z0-9_]+')
    for hull in ('caravel','galley','cog'):
        for slot in ('armor','guns','propulsion','range'):
            item=equipment['aor_'+hull+'_'+slot+'_low'].text
            goods=[float(n) for n in re.findall(r'goods_input_\w+_add\s*=\s*([0-9.]+)',item)]
            if not goods or not any(n>0 for n in goods):errors.append('Free equipment '+hull+':'+slot)
            if infra.number(item,'ship_construction_progress_max_add')<1:errors.append('No added construction complexity '+hull+':'+slot)
        for tier in ('low','mid','high'):
            if infra.number(equipment['aor_galley_propulsion_'+tier].text,'ship_crew_max_add')%100:errors.append('Partial equipment crew slot '+tier)
    _,placements=world.all_placements(world.HISTORY)
    for p in placements:
        if p.owner=='GBR' and p.building in {'building_tooling_workshop','building_tooling_workshops'} and 'pm_pig_iron' not in p.pms:errors.append('Wrong British tools PM '+p.state)
    gbr_admin=sum(p.level for p in placements if p.owner=='GBR' and p.building=='building_naval_administration')
    if gbr_admin!=32:errors.append('British naval capacity '+str(gbr_admin))
    if any(p.key==('GBR','STATE_CEYLON','building_naval_administration') for p in placements):errors.append('Ceylon transfer incomplete')
    military=(ROOT/'common/history/military_formations/00_military_formations_europe.txt').read_text(encoding='utf-8-sig')
    formations=[]
    for owner,a,b in old.country_spans(military):
        if owner.split()[0]!='c:GBR':continue
        formations=[military[a:b][x:y] for _,x,y in world.block_spans(military[a:b],'create_military_formation',1)]
    north=next(t for t in formations if cat.scalar(t,'name')=='cleanup2d3b_gbr_land_2')
    conscripts=regular_artillery=0
    for _,a,b in world.block_spans(north,'combat_unit',1):
        item=north[a:b];n=infra.number(item,'count')
        if cat.scalar(item,'service_type')=='conscript':conscripts+=n
        elif 'combat_unit_type_improved_cannon_artillery' in item:regular_artillery+=n
    if conscripts!=10 or regular_artillery!=3:errors.append('North American units mismatch')
    for name in ('cleanup2d3b_gbr_land_2','cleanup2d3b_gbr_land_3'):
        t=next(t for t in formations if cat.scalar(t,'name')==name)
        if 'hq_region = sr:region_canada' not in t:errors.append('Canadian HQ missing '+name)
    base['report']['naval_admin']=[]
    crew_totals=collections.Counter()
    for key in ('marine_chronometry','standardized_naval_signals'):
        # The grants explicitly enumerate the approved advanced maritime powers.
        holders={t for t,s in researched.items() if key in s}
        if holders!=ADVANCED:errors.append('Advanced technology whitelist '+key+':'+str(holders))
    for r in old.fleets({p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/history/military_formations').glob('*.txt')}):
        for kind,n in r['ships']:
            crew_totals[r['owner']]+=n*infra.number(ship_types[kind].text,'ship_crew_max_add')
            req=cat.tokens_flat(cat.braced_tokens(ship_types[kind].text,'unlocking_technologies'))
            if req and not any(t in researched[r['owner']] for t in req):errors.append('Unavailable hull '+r['owner']+':'+kind)
        if r['owner'] in COASTAL and any(k!='ship_type_galley' for k,n in r['ships']):errors.append('Non-coastal hull '+r['owner'])
        if r['owner']=='GBR' and r['name']=='cleanup2d3b_gbr_naval_2':
            if dict(r['ships']).get('ship_type_frigate')!=6 or 'supply_hub = s:STATE_BERMUDA' not in r['text']:errors.append('Western Approaches location/count')
    for tag in sorted(ADVANCED|COASTAL|{'USA'}):
        levels=sum(p.level for p in placements if p.owner==tag and p.building=='building_naval_administration')
        base['report']['naval_admin'].append({'country':tag,'crew_estimate':crew_totals[tag],'levels_after':levels,'theoretical_capacity':levels*1000})
        if crew_totals[tag]>levels*1000:errors.append('Naval manpower capacity '+tag)
    result={'status':'FAIL' if errors else 'PASS_STATIC_OCT09_BALANCE','engine_tested':False,'errors':errors,'protected_files':len(base['protected']),'report':base['report']}
    (CACHE/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if errors:raise SystemExit(1)

def repair_patch():
    """Anchor corrections with full surrounding context, including actual BOMs."""
    expected=json.loads((CACHE/'crew_ceiling.json').read_text(encoding='utf-8'))['expected']
    patch='*** Begin Patch\n';files=[]
    for path,new in expected.items():
        if new is None:continue
        actual=(ROOT/path).read_text(encoding='utf-8')
        desired=('\ufeff' if path.endswith('.yml') else '')+new
        if actual==desired:continue
        files.append(path)
        patch+='*** Update File: '+path+'\n'
        for line in list(difflib.unified_diff(actual.splitlines(),desired.splitlines(),n=35))[2:]:
            patch+=('@@' if line.startswith('@@') else line.rstrip('\n'))+'\n'
    print(json.dumps({'patch':patch+'*** End Patch','files':files},ensure_ascii=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--check',action='store_true');parser.add_argument('--amend-prepare',action='store_true');parser.add_argument('--ceiling-prepare',action='store_true');parser.add_argument('--repair-patch',action='store_true');args=parser.parse_args()
    if sum((args.prepare,args.check,args.amend_prepare,args.ceiling_prepare,args.repair_patch))!=1:parser.error('Choose exactly one action')
    repair_patch() if args.repair_patch else (prepare_crew_ceiling() if args.ceiling_prepare else (prepare_crew_amendment() if args.amend_prepare else (prepare() if args.prepare else check())))
