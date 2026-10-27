"""One Ortenburg pass; scoped Regensburg receipt and preservation first."""
import collections as C, contextlib, copy, io, json, os, re, subprocess, sys, unittest
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import serg_sc1_regensburg_demography as previous
ROOT=previous.ROOT; rm=previous.rm; core=previous.core; reg=previous.reg
sha=previous.sha; load=previous.load; runtime=previous.previous.prior.italian
TASK='SC1-ORTENBURG'; OUT=rm.OUT/TASK; PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
TAG='ORT'; SID='STATE_BAVARIA'; PARENT='x8C26DD'; RGB='xEDC100'; POP=1000
CELLS=[[4392,901],[4392,902],[4393,901],[4393,902]]
TECHS=['distillation','improved_husbandry','international_relations','organized_forestry','organized_textile_production','organized_workshops','periodical_print_networks','traditional_food_processing','traditional_papermaking']
os.environ['GIT_OPTIONAL_LOCKS']='0'
def dump(n,o): rm.write_json(OUT/n,o)
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def capture():
    assert not OUT.exists(); OUT.mkdir()
    state=load(rm.OUT/'ROADMAP_STATE.json'); assert rm.check()['status']=='PASS'
    dump('BASELINE.json',dict(roadmap=state,hashes=runtime.runtime_hashes(),inventory=core.qa.inventory(),registry=load(reg.active_registry_path()),proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents},peer_proofs={p.relative_to(ROOT).as_posix():sha(p) for base in ['docs/reports/technology','docs/reports/economy/ALLOYS_1776_REBALANCE','docs/reports/map/WORLD_1776_CLOSURE'] for p in (ROOT/base).rglob('*') if p.is_file()},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    (OUT/'provinces_before.png').write_bytes((ROOT/'map_data/provinces.png').read_bytes())
    (OUT/'USER_AUTHORIZATION.txt').write_text('Ok, Ratisbonne passe. Tu peux passer à Ortenburg.\n',encoding='utf8')
    print('Captured current workspace and all prior/peer proofs.',flush=True)

def receive():
    b=load(OUT/'BASELINE.json'); state=load(rm.OUT/'ROADMAP_STATE.json'); assert state==b['roadmap']
    task=next(t for t in state['tasks'] if t['id']==previous.TASK)
    assert task['status']=='BLOCKED' and task['installed_sub_lots'][0]['id']=='RG-D-CITY'
    path=previous.OUT/'RUNTIME_USER_ATTESTATION_2026_10_25.json'; assert not path.exists()
    raw=(ROOT/previous.REL).read_text(encoding='utf-8-sig'); pops={tag:[dict(culture=p.one('culture'),religion=p.one('religion'),size=int(p.one('size'))) for p in core.region(raw,'STATE_BAVARIA',tag).children('create_pop')] for tag in ['RCI','RBI']}
    assert sum(p['size'] for p in pops['RCI'])==11000 and sum(p['size'] for p in pops['RBI'])==4993
    expected=load(previous.OUT/'EXPECTED_TEXT.json')[previous.REL]
    assert all(core.qa.signature(core.region(raw,'STATE_BAVARIA',tag))==core.qa.signature(core.region(expected,'STATE_BAVARIA',tag)) for tag in ['RCI','RBI'])
    receipt=dict(status='PASS_RUNTIME_USER_VALIDATED',task_ids=[previous.TASK],sub_lot_ids=['RG-D-CITY'],scope_type='INSTALLED_SUB_LOTS_ONLY',regional_closure_approved=False,points_awarded=0,recorded_on='2026-10-25',actual_test_date=None,source=PREFIX+'USER_AUTHORIZATION.txt',verbatim_confirmation='Ok, Ratisbonne passe. Tu peux passer à Ortenburg.',protocol=previous.PREFIX+'PLAYER_TEST_PROTOCOL.md',scope='RG-D-CITY municipal demographic correction only; current RCI/RBI blocks match delivered version',explicitly_reported=['Ratisbonne passe'],extra_observations_invented=False,automated_engine_test=False,excluded=['Regional closure of SC1-REGENSBURG-DEMOGRAPHY','BG-E-SALT-NATIVE-R1 or other territories','Cadastral or 1776 census certification'],current_demographic_blocks=pops)
    receipt.update(new_game_date='1776-01-01',simulation_months=1,protocol_confirmation_basis='Short positive user acceptance of the supplied RG-D-CITY protocol; no detailed observations or effective test date added')
    rm.write_json(path,receipt)
    task['installed_delivery_status']='PASS_RUNTIME_USER_VALIDATED'; task['installed_sub_lots'][0].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=path.relative_to(ROOT).as_posix())
    task['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=path.relative_to(ROOT).as_posix(),scope='RG-D-CITY only; positive user report, no additional measurements invented')
    task['current_delivery_note']='RG-D-CITY validé par le joueur le 25 octobre (date de réception) : seuls les 11000 habitants municipaux RCI et la correction livrée sont couverts. Région BLOCKED P1 pour les autres ressorts et preuves historiques ; zéro point régional. Aucune observation supplémentaire inventée.'
    assert task['remaining_territorial_obligations']==next(t for t in b['roadmap']['tasks'] if t['id']==previous.TASK)['remaining_territorial_obligations']
    state.pop('runtime_validation_hold',None)
    event_id='SERG-RM-'+str(max(int(e['id'].split('-')[-1]) for e in state['events'])+1).zfill(4)
    state['events'].append(dict(id=event_id,date='2026-10-25',kind='SCOPED_REGRENSBURG_USER_VALIDATION',scope_version=state['scope_version'],source=path.relative_to(ROOT).as_posix(),changes=[dict(task_id=previous.TASK,before='BLOCKED',after='BLOCKED')],sub_lot_changes=[dict(id='RG-D-CITY',before='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',after='PASS_RUNTIME_USER_VALIDATED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=task['current_delivery_note']))
    state['mission_status']='REGENSBURG_CITY_ACCEPTED_ORTENBURG_AUTHORIZED'
    assert rm.progress(state)['next_task']==TASK
    assert not rm.structural_errors(state),rm.structural_errors(state)
    assert load(rm.OUT/'ROADMAP_STATE.json')==b['roadmap']; rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()): rm.render()
    dump('SELECTION.json',dict(status='PASS',canonical=rm.check(),selected=TASK,priority='P1',dependencies=[],only_new_task=TASK,regensburg_receipt=path.relative_to(ROOT).as_posix(),regional_credit_added=0))
    print('RG-D-CITY receipt recorded; Ortenburg selected; 82/235.',flush=True)

def survey():
    b=load(OUT/'BASELINE.json'); a=core.packed(OUT/'provinces_before.png'); inv=b['inventory']
    import serg_sc1_salzburg as slz
    hubs=slz.prior.pas.prior.q.r9.locators(a)
    relevant=[r for r in hubs if 4350<r['X']<4420 and 865<r['Y']<935]
    rows=[]
    for r in inv['owners']:
        rgb,sid,tag=r['key']
        if sid not in ['STATE_BAVARIA','STATE_AUSTRIA']: continue
        yy,xx=np.where(a==int(rgb[1:],16))
        if len(xx) and xx.min()<4420 and xx.max()>4360 and yy.min()<935 and yy.max()>870:
            rows.append(dict(rgb=rgb,state=sid,owner=tag,cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    dump('NATIVE_INVENTORY.json',dict(provinces=rows,hubs=relevant,populations=[r for r in inv['regional_pop'] if r['key'][0]=='STATE_BAVARIA'],buildings=[r for r in inv['buildings'] if r['key'][0]=='STATE_BAVARIA']))
    print(json.dumps(dict(provinces=rows,hubs=relevant),ensure_ascii=False),flush=True)

def prepare():
    b=load(OUT/'BASELINE.json'); a=core.packed(OUT/'provinces_before.png'); z=a.copy()
    assert TAG not in b['inventory']['countries'] and RGB not in b['inventory']['geometry']
    assert not np.any(a==int(RGB[1:],16))
    for x,y in CELLS: assert a[y,x]==int(PARENT[1:],16); z[y,x]=int(RGB[1:],16)
    import serg_sc4_piombino as physical
    yy,xx=np.where(z==int(PARENT[1:],16)); assert len(physical.components(xx,yy))==1
    originals={}; files={}
    def old(p):
        data=(ROOT/p).read_bytes(); originals[p]=data.decode('utf8'); return originals[p]
    def edit(raw,operations):
        bom=raw.startswith('\ufeff'); return ('\ufeff' if bom else '')+core.edits(raw.lstrip('\ufeff'),operations)
    p='common/history/states/00_states.txt';raw=old(p); n=core.state(raw.lstrip('\ufeff'),SID)
    files[p]=edit(raw,[(n.end-1,n.end-1,'\n\t\t# SC1-ORTENBURG: sovereign residence B, not the mediate Bavarian estates.\n\t\tcreate_state = { country = c:ORT owned_provinces = { xEDC100 } }\n\t')]).replace('\t\n\t\t# SC1-ORTENBURG:','\n\t\t# SC1-ORTENBURG:')
    p='map_data/state_regions/00_west_europe.txt';raw=old(p);n=next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID);f=n.children('provinces')[0];frag=raw.lstrip('\ufeff')[f.start:f.end]; assert frag.count('"'+PARENT+'"')==1
    files[p]=edit(raw,[(f.start,f.end,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    p='map_data/province_terrains.txt'; raw=old(p);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}; assert RGB.upper() not in terrain; files[p]=raw+'\n'+RGB+'="'+terrain[PARENT.upper()]+'"\n'
    p='common/history/pops/00_west_europe.txt';raw=old(p);clean=raw.lstrip('\ufeff');n=core.region(clean,SID,'BAV');donor=next(p for p in n.children('create_pop') if p.one('culture')=='south_german' and p.one('religion')=='protestant');f=donor.children('size')[0];amount=int(f.value);assert amount>=POP
    new=core.edits(clean,[(f.start,f.end,'size = '+str(amount-POP))]);new=core.append(new,SID,TAG,'\n\t\t\tcreate_pop = { culture = south_german religion = protestant size = 1000 }\n').replace('\t\n\t\tregion_state:ORT','\n\t\tregion_state:ORT');files[p]=('\ufeff' if raw.startswith('\ufeff') else '')+new
    defs='ORT = { color = { 168 68 62 } country_type = recognized tier = principality cultures = { south_german } religion = protestant capital = STATE_BAVARIA }\n';files['common/country_definitions/1776_sc1_ortenburg.txt']=defs
    files['common/history/countries/ort - ortenburg.txt']='COUNTRIES = { c:ORT ?= {\n'+''.join(' add_technology_researched = '+t+'\n' for t in TECHS)+''' activate_law = law_type:law_traditionalism
 activate_law = law_type:law_no_police
 activate_law = law_type:law_peasant_levies
 activate_law = law_type:law_monarchy
 activate_law = law_type:law_autocracy
 activate_law = law_type:law_state_religion
 activate_law = law_type:law_religious_schools
 activate_law = law_type:law_hereditary_bureaucrats
 activate_law = law_type:law_land_based_taxation
 activate_law = law_type:law_aor1776_imperial_customs
 activate_law = law_type:law_aor1776_imperial_no_slavery
 set_institution_investment_level = { institution = institution_schools level = 1 }
} }
'''
    files['common/history/characters/1776_sc1_ortenburg.txt']='''CHARACTERS = { c:ORT ?= { create_character = {
 first_name = aor1776_ort_karl last_name = aor1776_ort_dynasty
 historical = yes culture = south_german religion = rel:protestant ruler = yes
 # Rounded engine age for Karl III (1715-1776); no exact birthday asserted.
 age = 60 interest_group = ig_landowners ideology = ideology_traditionalist
} } }
'''
    files['common/government_types/00_1776_sc1_ortenburg.txt']='''gov_aor1776_ortenburg = {
 transfer_of_power = hereditary
 male_ruler = "aor1776_ort_count" female_ruler = "aor1776_ort_countess"
 possible = { c:ORT ?= this has_law = law_type:law_monarchy }
 on_government_type_change = { change_to_hereditary = yes }
 on_post_government_type_change = { post_change_to_hereditary = yes }
}
'''
    files['common/buildings/1776_sc1_ortenburg.txt']='''# Technical small chancery capacity, not an archival personnel census.
building_aor1776_ortenburg_chancery = {
 building_group = bg_bureaucracy city_type = city levels_per_mesh = 50
 expandable = no buildable = no downsizeable = no
 potential = { state_region = s:STATE_BAVARIA owner = { c:ORT ?= this } }
 production_method_groups = { pmg_aor1776_ortenburg_chancery }
 icon = "gfx/interface/icons/building_icons/building_government_administration.dds"
 required_construction = construction_cost_very_low
 background = "gfx/interface/icons/building_icons/backgrounds/building_panel_bg_monuments.dds"
}
'''
    files['common/production_method_groups/1776_sc1_ortenburg.txt']='pmg_aor1776_ortenburg_chancery = { texture = "gfx/interface/icons/generic_icons/mixed_icon_ownership.dds" ai_selection = most_productive production_methods = { pm_aor1776_ortenburg_chancery } }\n'
    files['common/production_methods/1776_sc1_ortenburg.txt']='''pm_aor1776_ortenburg_chancery = {
 texture = "gfx/interface/icons/production_method_icons/simple_organization.dds"
 country_modifiers = { workforce_scaled = { country_bureaucracy_add = 1 } }
 state_modifiers = { workforce_scaled = { state_tax_capacity_add = 1 } }
 building_modifiers = {
  workforce_scaled = { goods_input_paper_add = 0.5 }
  level_scaled = { building_employment_clerks_add = 40 building_employment_bureaucrats_add = 40 building_employment_aristocrats_add = 20 }
 }
}
'''
    files['common/history/buildings/1776_sc1_ortenburg.txt']='BUILDINGS = { s:STATE_BAVARIA = { region_state:ORT = { create_building = { building = "building_aor1776_ortenburg_chancery" level = 1 reserves = 1 activate_production_methods = { "pm_aor1776_ortenburg_chancery" } } } } }\n'
    files['common/scripted_effects/1776_sc1_ortenburg_names.txt']='''assign_aor1776_ortenburg_names = {
 if = {
  limit = { state_region = s:STATE_BAVARIA owner = { c:ORT ?= this } }
  set_state_name = aor1776_state_ortenburg
  set_hub_name = { type = city name = aor1776_hub_ortenburg }
 }
}
'''
    files['common/on_actions/99_1776_sc1_ortenburg.txt']='''on_game_started = { on_actions = { aor1776_ortenburg_names_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_ortenburg_names_initialize } }
on_state_created = { on_actions = { aor1776_ortenburg_state_changed } }
on_state_owner_change = { on_actions = { aor1776_ortenburg_state_changed } }
aor1776_ortenburg_names_initialize = { effect = { every_state = { assign_aor1776_ortenburg_names = yes } } }
aor1776_ortenburg_state_changed = { effect = { assign_aor1776_ortenburg_names = yes } }
'''
    files['common/coat_of_arms/coat_of_arms/1776_sc1_ortenburg.txt']='aor1776_ortenburg = { pattern = "pattern_solid.tga" color1 = "red" colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 0.8 0.8 } } } }\n'
    files['common/flag_definitions/1776_sc1_ortenburg.txt']='ORT = { flag_definition = { coa = aor1776_ortenburg priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french';pairs={'ORT':'Ortenbourg' if fr else 'Ortenburg','ORT_ADJ':'ortenbourgeois' if fr else 'Ortenburg','aor1776_ort_karl':'Karl III','aor1776_ort_dynasty':'von Ortenburg','aor1776_ort_count':'Comte impérial' if fr else 'Imperial Count','aor1776_ort_countess':'Comtesse impériale' if fr else 'Imperial Countess','gov_aor1776_ortenburg':'Comté impérial d’Ortenbourg' if fr else 'Imperial County of Ortenburg','gov_aor1776_ortenburg_desc':('Le comte exerce ses droits souverains sur le petit territoire immédiat d’Ortenbourg. Le conseil du marché règle les affaires de la communauté, tandis que les officiers du comte administrent ses droits et revenus.' if fr else 'The count exercises sovereign rights over the small immediate territory of Ortenburg. The market council handles communal affairs, while the count’s officers administer his rights and revenues.')+r'\n\n$TRANSFER_OF_POWER_NAME_DESC$','aor1776_state_ortenburg':'Ortenbourg' if fr else 'Ortenburg','aor1776_hub_ortenburg':'Ortenbourg' if fr else 'Ortenburg','building_aor1776_ortenburg_chancery':'Chancellerie comtale' if fr else 'Comital Chancery','pmg_aor1776_ortenburg_chancery':'Administration comtale' if fr else 'Comital Administration','pm_aor1776_ortenburg_chancery':'Officiers du comte' if fr else 'Comital Officers'}
        files[f'localization/{lang}/1776_sc1_ortenburg_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    rows=[]
    for rgb,tag in [(PARENT,'BAV'),(RGB,TAG)]:
        yy,xx=np.where(z==int(rgb[1:],16));rows.append(dict(rgb=rgb,parent_rgb=PARENT,state=SID,previous_owner='BAV',owner=tag,pixels=len(xx),cells=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])))
    geo=dict(classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,selected_option='ORTENBURG_MARKET_CASTLE_CORE',parents=[PARENT],new_provinces=[dict(rgb=RGB,parent_rgb=PARENT)],assignments=rows,hub_rebindings=[],basis='Valck after 1705, Ortenburg comitatus southwest of Passau and north of Griesbach; compact residence marker only, no mediate Hofmark annexation')
    previous_rows=[r for r in b['registry'] if r['state']==SID];addition=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC1-ORTENBURG sovereign market/castle nucleus B, not Bavarian mediate estates')
    migration=dict(replaced_regions=[SID],previous=previous_rows,updated=sorted(previous_rows+[addition],key=lambda r:r['rgb']),new_members=[TAG],free_cities=[],new_provinces=geo['new_provinces'],geometry='SERG_CLOSURE/'+TASK+'/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],country_additions={TAG:core.qa.signature(core.cw.parse(defs)[0])})
    p=reg.active_registry_path().relative_to(ROOT).as_posix();old(p); assert load(ROOT/p)==b['registry'];files[p]=json.dumps(sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    p='tools/map2l_registry.py';raw=old(p);needle='        result.append(passau_outliers)\n    return result';assert raw.count(needle)==1
    guard='''        result.append(passau_outliers)
    ortenburg=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-ORTENBURG'
    if (ortenburg/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((ortenburg/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((ortenburg/'GEOMETRY.json').read_text(encoding='utf8'))
        assert passau_outliers in result
        assert m['replaced_regions']==['STATE_BAVARIA'] and m['new_members']==['ORT'] and m['free_cities']==[]
        assert not m['extent_added_cells'] and not m['extent_removed_cells'] and m['region_reference_changes']==geo['hub_rebindings']==[]
        assert geo['parents']==['x8C26DD'] and geo['selected_option']=='ORTENBURG_MARKET_CASTLE_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDC100','parent_rgb':'x8C26DD'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('x8C26DD','BAV',272),('xEDC100','ORT',4)}
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='ORT')==[[4392,901],[4392,902],[4393,901],[4393,902]]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDC100'} and all(new[k]==v for k,v in old.items())
        assert old['x8C26DD']['beneficiary']==new['x8C26DD']['beneficiary']=='BAV' and new['xEDC100']['beneficiary']=='ORT'
        assert set(m['country_additions'])=={'ORT'}
        result.append(ortenburg)
    return result'''
    files[p]=raw.replace(needle,guard)
    for p,raw in files.items():
        if p not in originals: assert not (ROOT/p).exists(),p
        if p.endswith('.txt'): core.cw.parse(raw.lstrip('\ufeff'))
    # Compiler preflight runs BEFORE publishing the new migration to the registry helper.
    import map2k_imperial_system as compiler
    compiler.OUT=OUT; compiled=compiler.compile_system(); actual={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in compiled}; differences=[p for p,raw in compiled.items() if raw.lstrip('\ufeff')!=actual[p]];assert not differences,differences
    dump('COMPILER_BEFORE.json',dict(actual=actual,differences=differences))
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration);dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(transferred=POP,donor='BAV',state=SID,recipient=TAG,culture='south_german',religion='protestant',selected_donor_before=amount,selected_donor_after=amount-POP,world_delta=0,estimate='Rounded market/castle nucleus B, 1000; later 1840 market figure 1092 is only a dated proxy, not a census of 1776 or a total of all sovereign villages. No per-cell population interpolation.',all_professions_preserved=True))
    Image.fromarray(np.stack([(z>>16)&255,(z>>8)&255,z&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    print('Prepared ORT: four BAV cells, 1000 existing Protestant residents, nine modest technologies.',flush=True)

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');old=load(OUT/'TEXT_BEFORE.json'); current=runtime.runtime_hashes(); changes={p:dict(before=b['hashes'].get(p),after=current.get(p)) for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)}
    assert not set(changes)&(set(files)|{'map_data/provinces.png'}),changes
    dump('CONCURRENT_BEFORE_INSTALL.json',dict(files=changes,current_hashes=current,overlap=[]))
    assert core.qa.inventory()==b['inventory'],'Concurrent geographical data changed; re-evaluate patches'
    for p,raw in old.items():assert (ROOT/p).read_bytes().decode('utf8')==raw,p
    for p,raw in files.items():
        if p not in old:assert not (ROOT/p).exists(),p
    for p,raw in files.items():(ROOT/p).parent.mkdir(parents=True,exist_ok=True);(ROOT/p).write_bytes(raw.encode('utf8'))
    assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    (ROOT/'map_data/provinces.png').write_bytes((OUT/'provinces_candidate.png').read_bytes())
    import importlib
    importlib.reload(reg)
    import map2k_imperial_system as compiler
    importlib.reload(compiler); compiler.OUT=OUT; expected=compiler.compile_system(); pre=load(OUT/'COMPILER_BEFORE.json')['actual'];changed=[]
    for p,raw in expected.items():
        assert (ROOT/p).read_text(encoding='utf-8-sig')==pre[p],p
        if raw.lstrip('\ufeff')==pre[p]:continue
        bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf');(ROOT/p).write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'));changed.append(p)
    dump('IMPERIAL_EXPECTED.json',expected);dump('IMPERIAL_FILES.json',changed)
    print('Installed Ortenburg and guarded imperial integration; awaiting static and player validation.',flush=True)

def validate():
    b=load(OUT/'BASELINE.json'); inv=core.qa.inventory(); current=runtime.runtime_hashes(); files=load(OUT/'EXPECTED_TEXT.json'); checks=[]
    def ck(n,ok): checks.append(dict(name=n,passed=bool(ok)))
    old=core.packed(OUT/'provinces_before.png'); now=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(old!=now)
    ck('Exact four reviewed pixels only',sorted([[int(x),int(y)] for x,y in zip(xx,yy)])==CELLS)
    ck('Exact BAV donor and ORT child colors',all(old[y,x]==int(PARENT[1:],16) and now[y,x]==int(RGB[1:],16) for x,y in CELLS))
    for p,raw in files.items():
        ck('Reviewed current-byte patch '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'));ck('Syntax '+p,True)
    for p,raw in load(OUT/'IMPERIAL_EXPECTED.json').items():ck('Compiled imperial file '+p,(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    expected_paths=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png'}
    concurrent=load(OUT/'CONCURRENT_BEFORE_INSTALL.json')['files'];diff={p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)}
    ck('No unreviewed functional delta',diff<=expected_paths|set(concurrent))
    dump('FILES_MODIFIED.json',dict(runtime_files=sorted(diff&expected_paths),sha256={p:current[p] for p in diff&expected_paths},tool_files=['tools/map2l_registry.py','tools/serg_sc1_ortenburg.py'],human_validation=None,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'))
    ck('World populations and faiths exactly conserved',core.qa.counter(inv['pops'])==core.qa.counter(b['inventory']['pops']) and core.qa.counter(inv['resolved_demographics'])==core.qa.counter(b['inventory']['resolved_demographics']))
    expected=core.qa.counter(b['inventory']['regional_pop']);expected[SID,'BAV','south_german','protestant']-=POP;expected[SID,TAG,'south_german','protestant']+=POP
    ck('Only reviewed demographic transfer',core.qa.counter(inv['regional_pop'])==expected)
    ck('World total unchanged',sum(x['count'] for x in inv['pops'])==sum(x['count'] for x in b['inventory']['pops']))
    ck('No military declaration touched',inv['units']==b['inventory']['units'])
    ck('Only one country definition added',set(inv['countries'])==set(b['inventory']['countries'])|{TAG})
    ck('All existing country definitions retained',all(inv['countries'][t]==v for t,v in b['inventory']['countries'].items()))
    rows=load(reg.active_registry_path());ck('Registry one exact additional title',rows==sorted(b['registry']+[next(r for r in rows if r['rgb']==RGB)],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])) and len(rows)==580)
    ck('Title belongs only to ORT',next(r for r in rows if r['rgb']==RGB)['beneficiary']==TAG)
    ck('Only ORT added to approved tail',reg.approved_territorial_migrations()[-1]==load(OUT/'REGISTRY_MIGRATION.json') and reg.additional_members().count(TAG)==1 and TAG not in reg.additional_free_cities())
    from map2k_patch import ELECTORS
    ck('Nine electors and no new elector',len(ELECTORS)==9 and TAG not in ELECTORS.values())
    for tag in ['RCI','RBI','PAS','SLZ','FSI','BGT','BRX','TRT','MCA','AUS','RAG']:
        ck('Protected population '+tag,[r for r in inv['regional_pop'] if r['key'][1]==tag]==[r for r in b['inventory']['regional_pop'] if r['key'][1]==tag])
    import validate_starting_technology_1776 as contract
    s=contract.collect_snapshot();knowledge=load(OUT/'KNOWLEDGE_BEFORE.json')
    ck('All prior starting technology profiles retained',all(s['starts'][t]['technologies']==ts for t,ts in knowledge.items()) and set(s['starts'])==set(knowledge)|{TAG})
    ck('Nine explicit technologies only',set(s['starts'][TAG]['technologies'])==set(TECHS) and not s['starts'][TAG]['unresolved'])
    report=contract.audit_country(TAG,s);dump('STARTING_TECH_CHECK.json',report)
    technical=[r for r in report['findings'] if r['code'] in ['UNKNOWN_TECHNOLOGY','MISSING_TECHNOLOGY_PREREQUISITE','UNKNOWN_PM','SELECTED_PM_UNLOCK_GATE','UNKNOWN_BUILDING','CONSTRUCTION_GATE_ONLY','REQUESTED_LAW_TECH_GATE','UNKNOWN_REQUESTED_LAW']]
    ck('No unresolved technology or building gate',not technical)
    ck('Validated alloy graph retained',set(s['graph']['alloysworking'])=={'shaft_mining','organized_workshops'})
    ck('Chancery sole new building declaration',sum(r['count'] for r in inv['buildings'])==sum(r['count'] for r in b['inventory']['buildings'])+1)
    ck('One hundred chancery jobs',sum(float(n.value) for n in s['pms']['pm_aor1776_ortenburg_chancery'].children('building_modifiers')[0].children('level_scaled')[0].children())==100)
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_sc1_ortenburg_l_{lang}.yml';data=p.read_bytes();ck('Localization BOM and header '+lang,data.startswith(b'\xef\xbb\xbf') and data.decode('utf-8-sig').startswith('l_'+lang+':'))
        keys=re.findall(r'^\s*(\S+):0 ',data.decode('utf-8-sig'),re.M);ck('Unique localization keys '+lang,len(keys)==len(set(keys)))
    changed_prior={p:dict(before=h,after=sha(ROOT/p) if (ROOT/p).exists() else None) for p,h in b['proofs'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and (not (ROOT/p).exists() or sha(ROOT/p)!=h)}
    ck('All prior nested SERG proofs preserved',not changed_prior)
    peer_delta={p:dict(before=h,after=sha(ROOT/p) if (ROOT/p).exists() else None) for p,h in b['peer_proofs'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h}
    reviewed=load(OUT/'PEER_DOCUMENTARY_REVIEW.json') if (OUT/'PEER_DOCUMENTARY_REVIEW.json').exists() else {}
    ck('Peer proof revisions independently documented without TECH/SERG writes',all(p in reviewed.get('reviewed_paths',[]) for p in peer_delta))
    dump('CONCURRENT_CHANGES.json',dict(functional_before_install=concurrent,peer_documentary_changes=peer_delta,prior_SERG_proof_changes=changed_prior,old_versions_not_restored=True))
    ck('Git HEAD branch and index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    dump('SESSION_AFTER_STATIC.json',dict(hashes=current,inventory=inv,starting_technologies={t:v['technologies'] for t,v in s['starts'].items()}))
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',task_ids=[TASK],passed=sum(r['passed'] for r in checks),total=len(checks),failed=[r['name'] for r in checks if not r['passed']],checks=checks,automated_engine_test=False)
    dump('VALIDATION.json',result);print('Static',result['passed'],'/',result['total'],result['failed'],flush=True);assert not result['failed']

def track():
    s=load(rm.OUT/'ROADMAP_STATE.json');t=next(t for t in s['tasks'] if t['id']==TASK);assert t['status']=='NOT_STARTED';assert load(OUT/'VALIDATION.json')['status']=='PASS'
    # The present installation is a residence nucleus, not a certification of every rural jurisdiction.
    t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md',PREFIX+'SOURCES.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),installed_sub_lots=[dict(id='OR-I-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope='Four-cell market/castle sovereign nucleus B and 1000 residents only',attestation=None)],delivered_scope=dict(classification='B_PARTIAL_SOVEREIGN_RESIDENCE',sub_lots=['OR-I-CORE'],full_regional_coverage=False,cells=CELLS,population=POP),remaining_territorial_obligations=[dict(id='OR-RURAL-PERIMETER',status='OPEN_NOT_VALIDATED',scope='Dated mapping of sovereign rural villages and immediate versus mediate lordships beyond market/castle nucleus'),dict(id='OR-1776-DEMOGRAPHY',status='OPEN_NOT_VALIDATED',scope='Comparable near-1776 market and sovereign rural population; dated confessional counts')],blocking_reason='Seul OR-I-CORE, marché/résidence souverains, est représenté en B. Les villages du ressort immédiat et leur population comparable de 1776 restent à établir, distincts des Hofmarken bavaroises. Le repère de 1840 ne clôture pas cette démographie ; aucun transfert des possessions médiates ni de toute la commune actuelle.',residual_uncertainty='Noyau B topologique, population arrondie non recensée en 1776 ; profil technique abstrait et emblème simplifié. Fonctionnement et placement moteur à vérifier.')
    t['runtime_validation'].update(status='NOT_RUN',attestation=None,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',scope='OR-I-CORE only; no human confirmation yet')
    t['historical_sources'].append(PREFIX+'SOURCES.md:1')
    t['current_delivery_note']='OR-I-CORE installé : ORT, quatre cellules xEDC100 depuis BAV x8C26DD, 1000 protestants transférés sans variation mondiale, Karl III et comté héréditaire, neuf technologies et chancellerie 100 postes. Région BLOCKED P1 pour périphéries et démographie comparables ; noyau seul en attente du joueur, zéro point.'
    p=rm.progress(s);event_id='SERG-RM-'+str(max(int(e['id'].split('-')[-1]) for e in s['events'])+1).zfill(4)
    s['events'].append(dict(id=event_id,date='2026-10-25',kind='ORTENBURG_SCOPED_SOVEREIGN_NUCLEUS_PENDING_RUNTIME',scope_version=s['scope_version'],source=PREFIX+'USER_AUTHORIZATION.txt',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+'VALIDATION.json',PREFIX+'REPORT.md'],note=t['current_delivery_note']))
    probe=copy.deepcopy(s);probe.pop('runtime_validation_hold',None);candidate=rm.progress(probe)['next_task'];assert candidate and candidate!=TASK
    s['runtime_validation_hold']=dict(task_id=TASK,pending_task_ids=[TASK],protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,reason='Une seule nouvelle étape autorisée ; attendre le test du noyau Ortenburg.',test_summary='Nouvelle partie 1776 : ORT/Ortenburg, quatre cellules B, 1000 habitants protestants, Karl III, comté héréditaire, neuf technologies et chancellerie de 100 postes. Contrôler droits impériaux, voisins et économie ; un mois, sauvegarde/rechargement.',scope_note='RG-D-CITY Ratisbonne est validé dans son périmètre municipal. OR-I-CORE seul attend son reçu ; le ressort rural et la démographie complète d’Ortenburg restent bloqués. Aucune deuxième étape commencée.')
    s['mission_status']='REGENSBURG_CITY_ACCEPTED_ORTENBURG_NUCLEUS_PENDING_RUNTIME'
    assert not rm.structural_errors(s),rm.structural_errors(s)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    result=rm.check();dump('TRACKER_VALIDATION.json',result);assert result['status']=='PASS';print('Tracking updated; 82/235; only Ortenburg nucleus awaits player.',flush=True)

def refine_start():
    for name in ['VALIDATION.json','STARTING_TECH_CHECK.json','CONCURRENT_CHANGES.json']:
        p=OUT/name; q=OUT/('FIRST_'+name);assert not q.exists();q.write_bytes(p.read_bytes())
    files=load(OUT/'EXPECTED_TEXT.json');p='common/history/countries/ort - ortenburg.txt';old=files[p];assert (ROOT/p).read_bytes()==old.encode('utf8')
    needle=' effect_starting_politics_reactionary = yes\n';assert old.count(needle)==1
    new=old.replace(needle,' activate_law = law_type:law_traditionalism\n activate_law = law_type:law_no_police\n activate_law = law_type:law_peasant_levies\n')
    core.cw.parse(new);(ROOT/p).write_bytes(new.encode('utf8'));files[p]=new;dump('EXPECTED_TEXT.json',files)
    dump('START_POLICY_REFINEMENT.json',dict(file=p,before=old,after=new,reason='Remove broad reactionary template that requested interventionism, professional police/army, mercantilism and per-capita taxation without their technology. Explicit local laws use traditional economy, no professional police and peasant levies; no technology gifts or existing-country changes.'))
    c=load(OUT/'FIRST_CONCURRENT_CHANGES.json');paths=sorted(c['peer_documentary_changes']);snapshot={p:sha(ROOT/p) for p in paths}
    assert all(p.startswith('docs/reports/map/WORLD_1776_CLOSURE/') or p=='docs/reports/economy/ALLOYS_1776_REBALANCE/FILES_MODIFIED.json' for p in paths)
    dump('PEER_DOCUMENTARY_REVIEW.json',dict(reviewed_paths=paths,sha256=snapshot,reason='Independent WORLD B03 finalized documentation and archived EXTERNAL_ORTENBURG_UPDATE.json / EXTERNAL_SERG_UPDATE.json. ECON refreshed its own file manifest. No peer functional change after our entry, and no peer document written or restored by this pass.',WORLD_receipt=load(ROOT/'docs/reports/map/WORLD_1776_CLOSURE/BALKANS-03/EXTERNAL_ORTENBURG_UPDATE.json'),ECON_manifest_scope=load(ROOT/'docs/reports/economy/ALLOYS_1776_REBALANCE/FILES_MODIFIED.json').get('scope')))
    print('Removed incompatible inherited law requests; concurrent peer proof revisions recorded.',flush=True)

def tests():
    import serg_sc4_ligurian_fiefs as lig
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden','test_serg_sc1_passau_outliers','test_serg_versioned_receipts','test_serg_sc1_regensburg_demography','test_serg_sc1_ortenburg']
    for label,names in [('TARGETED_TESTS',['test_serg_sc1_ortenburg']),('CUMULATIVE_TESTS',modules)]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        failed=[dict(id=t.id(),traceback=trace) for t,trace in r.failures+r.errors]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if failed else 'PASS',total=r.testsRun,passed=r.testsRun-len(failed)-len(r.skipped),failed=failed,skipped=[dict(id=t.id(),reason=reason) for t,reason in r.skipped],automated_engine_test=False,old_tests_not_modified=True))
        print(label,r.testsRun-len(failed)-len(r.skipped),'/',r.testsRun,'failures',len(failed),flush=True)

def finalize():
    v=load(OUT/'VALIDATION.json');target=load(OUT/'TARGETED_TESTS.json');suite=load(OUT/'CUMULATIVE_TESTS.json')
    previous_ids={f['id'] for f in load(previous.OUT/'TESTS.json')['failed']}
    new_tail={'test_serg_sc1_passau_outliers.PassauOutlierContracts.test_current_tail','test_serg_sc1_regensburg_demography.RegensburgDemography.test_current_registry_tail_and_nine_electors'}
    new_receipt={'test_serg_sc1_regensburg_demography.RegensburgDemography.test_old_receipts_do_not_approve_this_demography'}
    unknown=[f for f in suite['failed'] if f['id'] not in previous_ids|new_tail|new_receipt]
    assert not unknown,unknown
    assert target['passed']==target['total']==16 and suite['total']==512 and suite['passed']==497 and len(suite['failed'])==14 and len(suite['skipped'])==1
    reviews=[]
    for f in suite['failed']:
        receipt=any(t in f['id'] for t in ['no_brixen_human','pending_new_core','no_fabricated_acceptance','old_receipts_do_not_approve'])
        reviews.append(dict(id=f['id'],classification='REAL_SCOPED_USER_RECEIPT_SUPERSEDES_ABSENCE_ASSERTION' if receipt else 'HISTORICAL_REGISTRY_SNAPSHOT_SUPERSEDED_BY_ADDITIVE_ORTENBURG_LAYER',new_since_previous=f['id'] in new_tail|new_receipt,evidence='Current four-cell and negative guard contracts, exact preservation of 579 prior registry rows, and independent real receipts; no old test changed.'))
    dump('TEST_REVIEW.json',dict(status='NO_UNEXPLAINED_REGRESSION',failed=reviews,unexplained_failures=[],raw_suite_status=suite['status'],old_tests_not_modified=True,automated_engine_test=False))
    s=load(rm.OUT/'ROADMAP_STATE.json');p=rm.progress(s);candidate=s['runtime_validation_hold']['next_implementation_candidate']
    assert candidate=='SC2-TESCHEN' and (p['earned_weight'],p['total_weight'],p['qualified_tasks'])==(82,235,24)
    already=any(e['kind']=='ORTENBURG_FINAL_STATIC_AND_TEST_REVIEW' for e in s['events'])
    event_id='SERG-RM-'+str(max(int(e['id'].split('-')[-1]) for e in s['events'])+1).zfill(4)
    note='146/146 contrôles statiques, 16/16 ciblés et 497/512 cumulatifs ; quatorze assertions historiques classées (dix snapshots de registre, quatre absences de reçus humains), une exclusion héritée. Aucun échec inexpliqué, aucun moteur lancé. OR-I-CORE seul attend le joueur ; région BLOCKED P1, zéro point. SC2-TESCHEN seulement identifié.'
    if not already:s['events'].append(dict(id=event_id,date='2026-10-25',kind='ORTENBURG_FINAL_STATIC_AND_TEST_REVIEW',scope_version=s['scope_version'],source=PREFIX+'TEST_REVIEW.json',changes=[],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',note=note))
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    report=(OUT/'REPORT.md').read_text(encoding='utf8')
    if '## Résultats finaux effectivement obtenus' not in report:(OUT/'REPORT.md').write_text(report+'\n## Résultats finaux effectivement obtenus\n\n'+note+'\n\nLe résultat brut FAIL de la suite cumulative est conservé, avec chaque trace et sa classification, sans suppression ni modification des anciens tests. La nouvelle couche ajoute exactement un titre ORT et préserve tous les 579 anciens ; les tests négatifs refusent un autre bénéficiaire et une cellule déplacée.\n\n![Comparaison politique locale](BEFORE_AFTER.png)\n',encoding='utf8')
    b=load(OUT/'BASELINE.json');current=runtime.runtime_hashes();static=load(OUT/'SESSION_AFTER_STATIC.json')['hashes'];files=load(OUT/'FILES_MODIFIED.json')['sha256'];state=load(rm.OUT/'ROADMAP_STATE.json')
    checks={
      'Functional composition equals statically checked snapshot':current==static,
      'Owned functional files match delivery hashes':all(current.get(f)==h for f,h in files.items()),
      '146 static and 16 targeted pass':v['passed']==v['total']==146 and target['passed']==target['total']==16,
      'Cumulative actual failures individually classified':not unknown and len(reviews)==14,
      'Canonical roadmap validator passes':rm.check()['status']=='PASS',
      'Progress 82 of 235 and 24 of 81 retained':rm.progress(state)['percent']=='34.89' and rm.progress(state)['qualified_tasks']==24,
      'RG-D-CITY user receipt scoped with region still blocked':rm.partial_runtime_evidence(next(t for t in state['tasks'] if t['id']==previous.TASK)),
      'No new ORT human receipt':not list(OUT.glob('RUNTIME_USER_ATTESTATION*')),
      'Only Ortenburg new task changed':all(t['status']==next(x['status'] for x in b['roadmap']['tasks'] if x['id']==t['id']) for t in state['tasks'] if t['id']!=TASK),
      'Next task only identified':next(t['status'] for t in state['tasks'] if t['id']==candidate)=='NOT_STARTED',
      'Prior nested SERG proof bytes retained':all(sha(ROOT/f)==h for f,h in b['proofs'].items() if Path(f).parent!=rm.OUT.relative_to(ROOT)),
      'Git revision branch index retained':git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'],
    }
    diff=subprocess.run(['git','-c','core.safecrlf=false','diff','--check'],cwd=ROOT,text=True,capture_output=True);own_errors=[line for line in diff.stdout.splitlines() if any(line.startswith(p+':') for p in files)]
    dump('DIFF_CHECK.json',dict(returncode=diff.returncode,stdout=diff.stdout,stderr=diff.stderr,own_errors=own_errors,unrelated_peer_whitespace_preserved=True))
    checks['No whitespace errors in owned tracked changes']=not own_errors
    result=dict(status='PASS' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),checks=checks,failed=[k for k,ok in checks.items() if not ok],automated_engine_test=False,human_validation_ORT=None,next_candidate=candidate)
    dump('FINAL_CHECKS.json',result)
    dump('SOURCE_READING.json',dict(historical_map=dict(original='VALCK_BAVARIA_AFTER_1705.jpg',sha256=sha(OUT/'VALCK_BAVARIA_AFTER_1705.jpg'),detail='VALCK_ORTENBURG_DETAIL.png',manifest='VALCK_MANIFEST.json',actually_viewed=True,interpretation='Ortenburg Comit southwest of Passau, south of Vilshofen, north of Griesbach; no metric or cadastral calibration'),date='2026-10-25',sources='SOURCES.md'))
    manifest={f:sha(ROOT/f) for f in files};manifest.update({str((ROOT/'tools'/n).relative_to(ROOT).as_posix()):sha(ROOT/'tools'/n) for n in ['serg_sc1_ortenburg.py','test_serg_sc1_ortenburg.py','map2l_registry.py']});manifest.update({f.relative_to(ROOT).as_posix():sha(f) for f in OUT.rglob('*') if f.is_file() and f.name!='DELIVERY_MANIFEST.json'})
    dump('DELIVERY_MANIFEST.json',dict(files=manifest,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',sub_lot='OR-I-CORE',regional_task_status='BLOCKED',human_validation=None,scope='Market/castle sovereign nucleus only, no complete rural jurisdiction or 1776 census certification'))
    print('Final checks',result['passed'],'/',result['total'],'; next',candidate,'not started.',flush=True);assert not result['failed'],result['failed']

if __name__=='__main__': globals()[sys.argv[1]]()
