"""Brixen: guarded territorial implementation; never manufactures a human receipt."""
import collections as C
import contextlib, copy, csv, io, json, os, re, shutil, subprocess, sys, unittest
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc1_trento as prior
ROOT=prior.ROOT;rm=prior.rm;core=prior.core;reg=prior.reg;sha=prior.sha
TASK='SC1-BRIXEN';OUT=rm.OUT/TASK;PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
TAG='BRX';RGB='xEDBE00';PARENT='xD040E0';SID='STATE_SOUTH_TYROL';POP=3000
CELLS=[[x,y] for x in range(4362,4365) for y in range(948,951)]
TEST_SUMMARY='Nouvelle partie au 1er janvier 1776 : BR-I-CORE, Brixen (BRX), neuf cellules B, capitale dans la portion BRX et nom Brixen, Leopold Maria Joseph von Spaur catholique, théocratie, 3 000 habitants et une chancellerie publique de 200 postes au maximum. Vérifier le pacte défensif AUS, les droits impériaux sans nouvel électeur et tous les voisins, notamment TR-I-CORE. Simuler un mois, sauvegarder puis recharger ; communiquer les résultats réels.'
SCOPE_NOTE='BR-I-CORE représente seulement la résidence politique de Brixen. Bruneck/Puster, Klausen/Feldthurns et autres possessions restent ouverts ; aucune clôture régionale ni validation cadastrale. Le placement automatique de la capitale du nouvel État partagé doit être contrôlé en jeu. Trente reste BLOCKED malgré son noyau humainement validé ; le Tyrol dépend encore des deux principautés. SC1-BERCHTESGADEN est identifiée sans commencement.'
MISSION=Path('C:/Users/simeo/.codex/attachments/48d13c37-0556-446d-867a-f7442a0f7efa/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def load(p):return rm.load_json(p)
def dump(n,o):rm.write_json(OUT/n,o)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    s=load(rm.OUT/'ROADMAP_STATE.json');checked=rm.check()
    assert checked['status']=='PASS' and rm.progress(s)['next_task']==TASK and s['events'][-1]['id']=='SERG-RM-0029'
    OUT.mkdir(exist_ok=True);hashes=prior.prior.italian.runtime_hashes();inv=core.qa.inventory()
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json',dict(roadmap=s,inventory=inv,hashes=hashes,registry=load(reg.active_registry_path()),reports=proofs,
        tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},
        git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=sha(ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal'))))
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png');shutil.copyfile(MISSION,OUT/'USER_MISSION.txt')
    dump('ENTRY_TRACKER_VALIDATION.json',checked);print('Brixen baseline: 82/235, P1, Salzburg dependency satisfied; Trento region BLOCKED',flush=True)

def survey():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(OUT/'provinces_before.png')
    targets={'STATE_SOUTH_TYROL','STATE_TYROL','STATE_BAVARIA','STATE_STYRIA','STATE_VENETIA'};rows=[]
    for r in inv['owners']:
        rgb,sid,tag=r['key']
        if sid not in targets:continue
        yy,xx=np.where(a==int(rgb[1:],16));rows.append(dict(rgb=rgb,state=sid,owner=tag,cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    tags=['BRX','BRI','BRN','BXN'];use={t:[] for t in tags}
    for folder in ['common/country_definitions','common/flag_definitions']:
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            raw=p.read_text(encoding='utf-8-sig')
            for t in tags:
                if re.search(r'\b'+t+r'\b',raw):use[t].append(str(p))
    import serg_sc1_salzburg as slz
    hubs=slz.prior.pas.prior.q.r9.locators(a);dump('LOCATORS_BEFORE.json',hubs)
    dump('NATIVE_INVENTORY.json',dict(provinces=rows,candidate_tags=use,countries={t:inv['countries'].get(t) for t in ['AUS','TRT','SLZ','VEN']+tags},
        populations=[r for r in inv['regional_pop'] if r['key'][0] in targets],buildings=[r for r in inv['buildings'] if r['key'][0] in targets],
        units=[r for r in inv['units'] if r['key'][0] in {'AUS','VEN','TRT','SLZ'}],native_hubs=[r for r in hubs if r['ID'] in [55,56,71]]))
    print('Tags',json.dumps(use),flush=True)
    for r in rows:
        if r['state'] in {'STATE_TYROL','STATE_SOUTH_TYROL'}:print(r,flush=True)
    for r in inv['regional_pop']:
        if r['key'][0] in {'STATE_TYROL','STATE_SOUTH_TYROL'}:print('population',r,flush=True)
    for r in hubs:
        if r['ID'] in [55,56]:print('hub',r,flush=True)

def compiler_before():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();actual={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in files}
    diff=[p for p,raw in files.items() if raw.lstrip('\ufeff')!=actual[p]]
    dump('COMPILER_BEFORE.json',dict(actual=actual,differences=diff));print('Compiler preflight',diff,flush=True);assert not diff

def prepare():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png')
    assert prior.prior.italian.runtime_hashes()==b['hashes'],'Concurrent changes require review'
    assert TAG not in b['inventory']['countries'] and RGB not in b['inventory']['geometry'] and not np.any(a==int(RGB[1:],16))
    assert not load(OUT/'NATIVE_INVENTORY.json')['candidate_tags'][TAG]
    after=a.copy()
    for x,y in CELLS:
        assert a[y,x]==int(PARENT[1:],16)
        after[y,x]=int(RGB[1:],16)
    yy,xx=np.where(after==int(PARENT[1:],16));assert len(prior.prior.prior.components(xx,yy))==1
    rows=[]
    for rgb,tag in [(PARENT,'AUS'),(RGB,TAG)]:
        yy,xx=np.where(after==int(rgb[1:],16));points=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
        rows.append(dict(rgb=rgb,parent_rgb=PARENT,state=SID,previous_owner='AUS',owner=tag,pixels=len(points),cells=points,confidence='B_POLITICAL_APPROXIMATION' if tag==TAG else 'RETAINED_NOT_CERTIFIED'))
    geo=dict(parents=[PARENT],assignments=rows,new_provinces=[dict(rgb=RGB,parent_rgb=PARENT)],new_members=[TAG],free_cities=[],selected_option='BRIXEN_RESIDENCE_CORE',classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,hub_rebindings=[])
    files={};originals={}
    def old(p):
        assert sha(ROOT/p)==b['hashes'][p]
        raw=(ROOT/p).read_bytes().decode('utf8');originals[p]=raw;return raw
    p='common/history/states/00_states.txt';raw=old(p);n=core.state(raw,SID)
    files[p]=core.edits(raw,[(n.end-1,n.end-1,'\n\t\t# SC1-BRIXEN: political residence, not the diocese or all Puster/Isarco.\n\t\tcreate_state = { country = c:BRX owned_provinces = { xEDBE00 } }\n\t')]).replace('\t\n\t\t# SC1-BRIXEN:','\n\t\t# SC1-BRIXEN:')
    p='map_data/state_regions/00_west_europe.txt';raw=old(p);off=int(raw.startswith('\ufeff'));n=next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID);f=n.children('provinces')[0]
    frag=raw[f.start+off:f.end+off];assert frag.count('"'+PARENT+'"')==1
    files[p]=core.edits(raw,[(f.start+off,f.end+off,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    p='map_data/province_terrains.txt';raw=old(p);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    assert RGB.upper() not in terrain;files[p]=raw+'\n'+RGB+'="'+terrain[PARENT.upper()]+'"\n'
    p='common/history/pops/00_west_europe.txt';raw=old(p);n=core.region(raw,SID,'AUS');donors=[pop for pop in n.children('create_pop') if pop.one('culture')=='south_german']
    assert len(donors)==2 and all(pop.one('religion') is None and pop.one('pop_type') is None for pop in donors)
    f=donors[0].children('size')[0];assert int(f.value)==91500
    raw=core.edits(raw,[(f.start,f.end,'size = '+str(91500-POP))]);files[p]=core.append(raw,SID,TAG,'\n\t\t\tcreate_pop = { culture = south_german size = '+str(POP)+' }\n').replace('\t\n\t\tregion_state:BRX','\n\t\tregion_state:BRX')
    defs='BRX = { color = { 169 67 85 } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = STATE_SOUTH_TYROL }\n'
    files['common/country_definitions/1776_sc1_brixen.txt']=defs
    files['common/history/countries/brx - brixen.txt']='''COUNTRIES = {
 c:BRX ?= {
  add_technology_researched = international_relations
  effect_starting_politics_reactionary = yes
  activate_law = law_type:law_theocracy
  activate_law = law_type:law_autocracy
  activate_law = law_type:law_state_religion
  activate_law = law_type:law_religious_schools
  activate_law = law_type:law_hereditary_bureaucrats
  activate_law = law_type:law_land_based_taxation
  activate_law = law_type:law_aor1776_imperial_customs
  activate_law = law_type:law_aor1776_imperial_no_slavery
 }
}
'''
    files['common/history/characters/1776_sc1_brixen.txt']='CHARACTERS = { c:BRX ?= { create_character = { first_name = aor1776_brx_first last_name = aor1776_brx_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1696.5.10 interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    files['common/government_types/00_1776_sc1_brixen.txt']='gov_aor1776_brixen = { transfer_of_power = dictatorial male_ruler = "aor1776_brx_ruler" female_ruler = "aor1776_brx_ruler_female" possible = { c:BRX ?= this has_law = law_type:law_theocracy } on_government_type_change = { change_to_dictatorial = yes } on_post_government_type_change = { post_change_to_dictatorial = yes } }\n'
    files['common/buildings/1776_sc1_brixen.txt']='''# Existing episcopal chancery: small public court, no scalable bureaucracy farm.
building_aor1776_brixen_chancery = {
 building_group = bg_bureaucracy
 city_type = city
 levels_per_mesh = 50
 expandable = no
 buildable = no
 downsizeable = no
 potential = { state_region = s:STATE_SOUTH_TYROL owner = { c:BRX ?= this } }
 production_method_groups = { pmg_aor1776_brixen_chancery }
 icon = "gfx/interface/icons/building_icons/building_government_administration.dds"
 required_construction = construction_cost_very_low
 background = "gfx/interface/icons/building_icons/backgrounds/building_panel_bg_monuments.dds"
}
'''
    files['common/production_method_groups/1776_sc1_brixen.txt']='pmg_aor1776_brixen_chancery = { texture = "gfx/interface/icons/generic_icons/mixed_icon_ownership.dds" ai_selection = most_productive production_methods = { pm_aor1776_brixen_chancery } }\n'
    files['common/production_methods/1776_sc1_brixen.txt']='''# Technical capacity, not a reconstructed personnel register.
pm_aor1776_brixen_chancery = {
 texture = "gfx/interface/icons/production_method_icons/simple_organization.dds"
 country_modifiers = { workforce_scaled = { country_bureaucracy_add = 2 } }
 state_modifiers = { workforce_scaled = { state_tax_capacity_add = 1 } }
 building_modifiers = {
  workforce_scaled = { goods_input_paper_add = 1 }
  level_scaled = {
   building_employment_clerks_add = 50
   building_employment_bureaucrats_add = 50
   building_employment_clergymen_add = 75
   building_employment_aristocrats_add = 25
  }
 }
}
'''
    files['common/history/buildings/1776_sc1_brixen.txt']='BUILDINGS = { s:STATE_SOUTH_TYROL = { region_state:BRX = { create_building = { building = "building_aor1776_brixen_chancery" add_ownership = { country = { country = "c:BRX" levels = 1 } } reserves = 1 activate_production_methods = { "pm_aor1776_brixen_chancery" } } } } }\n'
    files['common/history/treaties/1776_sc1_brixen.txt']='''TREATIES = {
 # Political approximation B: country-wide native pact, not a literal Landlibell.
 # Regional fiscal quotas and limited military service are not reproduced.
 create_treaty = {
  name = treaty_aor1776_landlibell_brixen
  first_country = c:AUS
  second_country = c:BRX
  is_draft = no
  entered_into_force_on = 1511.6.23
  binding_period = { years = 5 }
  articles_to_create = { { article = defensive_pact } }
 }
}
'''
    files['common/scripted_effects/1776_sc1_brixen.txt']='''# State-owner scope only. Do not rename the TRT or AUS portions or move a locator.
assign_aor1776_brixen_names = {
 if = {
  limit = { state_region = s:STATE_SOUTH_TYROL owner = { c:BRX ?= this } }
  set_state_name = aor1776_state_brixen
  set_hub_name = { type = city name = aor1776_hub_brixen }
 }
}
'''
    files['common/on_actions/99_1776_sc1_brixen.txt']='''on_game_started = { on_actions = { aor1776_brixen_names_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_brixen_names_initialize } }
on_state_created = { on_actions = { aor1776_brixen_state_name_changed } }
on_state_owner_change = { on_actions = { aor1776_brixen_state_name_changed } }
on_become_subject = { on_actions = { aor1776_brixen_country_names_changed } }
on_become_independent = { on_actions = { aor1776_brixen_country_names_changed } }
aor1776_brixen_names_initialize = { effect = { every_state = { assign_aor1776_brixen_names = yes } } }
aor1776_brixen_state_name_changed = { effect = { assign_aor1776_brixen_names = yes } }
aor1776_brixen_country_names_changed = { effect = { every_scope_state = { assign_aor1776_brixen_names = yes } } }
'''
    # Red cross is a neutral engine emblem, explicitly not the historical Paschal lamb.
    files['common/coat_of_arms/coat_of_arms/1776_sc1_brixen.txt']='aor1776_brixen = { pattern = "pattern_solid.tga" color1 = "white" colored_emblem = { texture = "ce_cross_couped.dds" color1 = "red" instance = { scale = { 0.7 0.7 } } } }\n'
    files['common/flag_definitions/1776_sc1_brixen.txt']='BRX = { flag_definition = { coa = aor1776_brixen priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french';pairs={'BRX':'Brixen','BRX_ADJ':'brixinois' if fr else 'Brixenian','aor1776_brx_first':'Leopold Maria Joseph','aor1776_brx_last':'von Spaur','aor1776_brx_ruler':'Prince-évêque' if fr else 'Prince-Bishop','aor1776_brx_ruler_female':'Princesse-évêque' if fr else 'Princess-Bishop','gov_aor1776_brixen':'Principauté épiscopale de Brixen' if fr else 'Prince-Bishopric of Brixen','gov_aor1776_brixen_desc':('Le prince-évêque exerce son pouvoir temporel depuis la Hofburg avec le conseil aulique et le chapitre. La défense commune avec le Tyrol accompagne les droits du principat dans le Saint-Empire.' if fr else 'The prince-bishop exercises temporal authority from the Hofburg with the aulic council and cathedral chapter. Common defence with Tyrol accompanies the principality’s rights within the Holy Roman Empire.')+r'\n\n$TRANSFER_OF_POWER_NAME_DESC$','treaty_aor1776_landlibell_brixen':'Accord de défense du Landlibell' if fr else 'Landlibell Defence Agreement','aor1776_state_brixen':'Brixen','aor1776_hub_brixen':'Brixen','building_aor1776_brixen_chancery':'Chancellerie de la Hofburg' if fr else 'Hofburg Chancery','building_aor1776_brixen_chancery_desc':'Le conseil aulique et les officiers du prince-évêque administrent les affaires temporelles du principat.' if fr else 'The aulic council and the prince-bishop’s officers administer the temporal affairs of the principality.','pmg_aor1776_brixen_chancery':'Conseil aulique' if fr else 'Aulic Council','pm_aor1776_brixen_chancery':'Officiers de la cour épiscopale' if fr else 'Episcopal Court Officers'}
        files['localization/'+lang+'/1776_sc1_brixen_l_'+lang+'.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    previous=[r for r in b['registry'] if r['state']==SID];assert any(r['rgb']==PARENT and r['beneficiary']=='AUS' for r in previous)
    addition=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC1-BRIXEN: nine-cell residence nucleus B, relative historic topology; not complete temporal or diocesan boundaries')
    migration=dict(replaced_regions=[SID],previous=previous,updated=sorted(previous+[addition],key=lambda r:r['rgb']),new_members=[TAG],free_cities=[],new_provinces=geo['new_provinces'],geometry='SERG_CLOSURE/'+TASK+'/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],country_additions={TAG:core.qa.signature(core.cw.parse(defs)[0])})
    rel=reg.active_registry_path().relative_to(ROOT).as_posix();originals[rel]=(ROOT/rel).read_text(encoding='utf-8-sig');assert load(ROOT/rel)==b['registry']
    files[rel]=json.dumps(sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    for p,raw in files.items():
        if p not in originals:assert not (ROOT/p).exists(),p
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration);dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(transferred=POP,donor='AUS',recipient=TAG,donor_before=482000,donor_after=479000,donor_south_german_before=183000,donor_south_german_after=180000,north_italian_unchanged=299000,culture='south_german',religion='DEFAULT:south_german',profession='unchanged: not declared',historical_basis='OeAW Ortslexikon Suedtirol p5: Brixen Stadtgericht 1697 approx 2000, 1798 3629 including Pfeffersberg. Rounded 3000 residence estimate, not a 1776 census, whole principality 26759 (1785) or diocese 230164 (1770).',court_capacity=200,capacity_is_technical_approximation=True))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    print('Prepared BRX: 9 cells, 3000 donor residents, no physical locator or Trento reference changed',flush=True)

def review_concurrent():
    b=load(OUT/'BASELINE.json');cur=prior.prior.italian.runtime_hashes();planned=set(load(OUT/'EXPECTED_TEXT.json'))|{'map_data/provinces.png'}
    changes=sorted(k for k in set(cur)|set(b['hashes']) if cur.get(k)!=b['hashes'].get(k))
    overlap=sorted(set(changes)&planned);same=core.qa.inventory()==b['inventory']
    dump('CONCURRENT_BEFORE_INSTALL.json',dict(changes=changes,files={p:cur.get(p) for p in changes},hashes=cur,overlap_with_planned_files=overlap,inventory_unchanged=same))
    print('Concurrent runtime',changes,'overlap',overlap,'inventory unchanged',same,flush=True)
    assert not overlap and same

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');originals=load(OUT/'TEXT_BEFORE.json');review=load(OUT/'CONCURRENT_BEFORE_INSTALL.json')
    assert review['inventory_unchanged'] and not review['overlap_with_planned_files'] and prior.prior.italian.runtime_hashes()==review['hashes']
    assert sha(ROOT/'.git/index')==b['git']['index_sha256'] and not load(OUT/'COMPILER_BEFORE.json')['differences']
    for p,raw in originals.items():assert (ROOT/p).read_bytes().decode('utf8').lstrip('\ufeff')==raw.lstrip('\ufeff'),p
    for p,raw in files.items():
        dest=ROOT/p
        if p not in originals:assert not dest.exists(),p
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw.encode('utf8'))
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png');print('Brixen core installed, pending compiler and static tests',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;before=load(OUT/'COMPILER_BEFORE.json');files=compiler.compile_system();changed=[]
    for p,raw in files.items():
        if raw.lstrip('\ufeff')==before['actual'][p]:continue
        assert (ROOT/p).read_text(encoding='utf-8-sig')==before['actual'][p],p
        bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf');(ROOT/p).write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'));changed.append(p)
    dump('IMPERIAL_EXPECTED.json',files);dump('IMPERIAL_FILES.json',changed);print('Imperial compiler changed',len(changed),'files',flush=True)

def validate():
    b=load(OUT/'BASELINE.json');old=b['inventory'];inv=core.qa.inventory();current=prior.prior.italian.runtime_hashes();files=load(OUT/'EXPECTED_TEXT.json');imperial=load(OUT/'IMPERIAL_EXPECTED.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(a!=z)
    ck('Exactly nine declared AUS to BRX pixels',sorted(zip(map(int,xx),map(int,yy)))==sorted(map(tuple,CELLS)) and all(int(a[y,x])==int(PARENT[1:],16) and int(z[y,x])==int(RGB[1:],16) for x,y in CELLS))
    ck('Native map size retained',a.shape==z.shape==(3616,8192))
    for rgb,count in [(PARENT,453),(RGB,9)]:
        yy,xx=np.where(z==int(rgb[1:],16));ck('Connected '+rgb,len(xx)==count and len(prior.prior.prior.components(xx,yy))==1)
    eo=core.qa.counter(old['owners']);eo[RGB,SID,TAG]=1;ck('Only one new sovereign owner',core.qa.counter(inv['owners'])==eo)
    eg=dict(old['geometry']);eg[RGB]=SID;ck('Only one new province',inv['geometry']==eg)
    ck('Only one new incorporated state portion',inv['states']==sorted(old['states']+[[SID,TAG]]))
    et=dict(old['state_types']);et[SID+'|'+TAG]='incorporated_default';ck('All old state types retained',inv['state_types']==et)
    defs=core.cw.parse(files['common/country_definitions/1776_sc1_brixen.txt'])[0];ec=dict(old['countries']);ec[TAG]=core.qa.signature(defs);ck('All old country definitions retained',inv['countries']==ec)
    for field in ['pops','resolved_demographics','units','errors','duplicates']:ck('World conservation '+field,inv[field]==old[field])
    ep=core.qa.counter(old['regional_pop']);ep[SID,'AUS','south_german','DEFAULT:south_german']-=POP;ep[SID,TAG,'south_german','DEFAULT:south_german']=POP
    ck('Exact 3000 south German transfer only',core.qa.counter(inv['regional_pop'])==ep)
    popnode=core.region(files['common/history/pops/00_west_europe.txt'],SID,TAG).children('create_pop')[0]
    ck('No invented religious or professional census',[(n.key,n.value) for n in popnode.children()]==[('culture','south_german'),('size','3000')])
    admin=core.region(files['common/history/buildings/1776_sc1_brixen.txt'],SID,TAG).children('create_building')[0];eb=core.qa.counter(old['buildings']);eb[SID,TAG,core.qa.signature(admin)]+=1
    ck('All old buildings economic ownership retained',core.qa.counter(inv['buildings'])==eb)
    el=core.qa.counter(old['building_levels_written']);el['building_aor1776_brixen_chancery']+=1;ck('Only one small public court level added',core.qa.counter(inv['building_levels_written'])==el)
    ck('Episcopal court nationally owned',admin.children('add_ownership')[0].children('country')[0].one('country')=='"c:BRX"')
    pm=core.cw.parse(files['common/production_methods/1776_sc1_brixen.txt'])[0];employment=pm.children('building_modifiers')[0].children('level_scaled')[0].children()
    types=prior.prior.italian.definitions('common/pop_types');ck('Court jobs reference actual professions',all(n.key.removeprefix('building_employment_').removesuffix('_add') in types for n in employment))
    jobs=sum(int(n.value) for n in employment);ck('Court capacity 200 and below conservative 25 percent workforce',jobs==200 and jobs<POP*0.25)
    building=core.cw.parse(files['common/buildings/1776_sc1_brixen.txt'])[0]
    ck('Court public group and no arbitrary expansion',building.one('building_group')=='bg_bureaucracy' and building.one('expandable')=='no' and building.one('buildable')=='no' and building.one('downsizeable')=='no')
    ck('Court scoped only BRX portion','state_region = s:STATE_SOUTH_TYROL owner = { c:BRX ?= this }' in files['common/buildings/1776_sc1_brixen.txt'])
    ledger=load(reg.active_registry_path());m=load(OUT/'REGISTRY_MIGRATION.json');addition=next(r for r in m['updated'] if r['rgb']==RGB)
    ck('Exact additive registry 576 to 577',ledger==sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])) and len(ledger)==len({r['rgb'] for r in ledger})==577)
    ck('Exact prior migration input',m['previous']==[r for r in b['registry'] if r['state']==SID])
    ck('Current cumulative Salzburg Massa Trento Brixen tail',reg.approved_lot_dirs()[-4:]==[rm.OUT/'SC1-SALZBURG',prior.prior.OUT,prior.OUT,OUT])
    ck('Imperial physical extent unchanged',np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    from map2k_patch import ELECTORS
    ck('BRX member neither free city nor tenth elector',TAG in reg.additional_members() and TAG not in reg.additional_free_cities() and TAG not in ELECTORS.values() and len(ELECTORS)==9)
    ck('Piedmont bounded rights retained',reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}} and [r for r in ledger if r['beneficiary']=='SAR']==[r for r in b['registry'] if r['beneficiary']=='SAR'])
    import serg_sc1_salzburg as slz
    loc_after=slz.prior.pas.prior.q.r9.locators(z);ck('Every physical locator and locator RGB unchanged',loc_after==load(OUT/'LOCATORS_BEFORE.json'))
    oldst=next(n for n in core.cw.parse(load(OUT/'TEXT_BEFORE.json')['map_data/state_regions/00_west_europe.txt'].lstrip('\ufeff')) if n.key==SID);newst=next(n for n in core.cw.parse(files['map_data/state_regions/00_west_europe.txt'].lstrip('\ufeff')) if n.key==SID)
    ck('All regional hubs resources arables and traits unchanged',[core.qa.signature(n) for n in oldst.children() if n.key!='provinces']==[core.qa.signature(n) for n in newst.children() if n.key!='provinces'])
    ck('Trento city reference still TRT',core.cw.scalar(newst.one('city'))==prior.RGB and int(z[973,4352])==int(prior.RGB[1:],16))
    ck('Brixen capital has owned state portion, actual automatic point pending engine',defs.one('capital')==SID and [SID,TAG] in inv['states'])
    name=files['common/scripted_effects/1776_sc1_brixen.txt'];ck('Naming effect only BRX in correct state','limit = { state_region = s:STATE_SOUTH_TYROL owner = { c:BRX ?= this } }' in name and 'set_state_name = aor1776_state_brixen' in name and 'set_hub_name = { type = city name = aor1776_hub_brixen }' in name)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))};ck('Child terrain matches parent',terrain[PARENT.upper()]==terrain[RGB.upper()])
    import serg_sc4_ligurian_fiefs as lig
    policy=lig.initial_policy(TAG,prior.prior.italian.definitions('common/scripted_effects'),prior.prior.italian.definitions('common/laws'));dump('INITIAL_POLICY.json',policy)
    ck('Effective theocracy state religion bureaucracy customs no slavery',{'law_theocracy','law_state_religion','law_hereditary_bureaucrats','law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery'}<=set(policy['laws'].values()))
    ck('Defensive pact technology active','international_relations' in policy['technologies'])
    char=files['common/history/characters/1776_sc1_brixen.txt'];ck('Leopold 1696 starts, coadjutor not substituted',all(s in char for s in ['aor1776_brx_first','aor1776_brx_last','birth_date = 1696.5.10','ruler = yes','ig_devout','rel:catholic']) and 'Ignaz' not in char)
    pact=files['common/history/treaties/1776_sc1_brixen.txt'];ck('AUS BRX defensive pact, not annexation or puppet',all(s in pact for s in ['first_country = c:AUS','second_country = c:BRX','1511.6.23','article = defensive_pact']) and 'puppet' not in pact and 'personal_union' not in pact)
    ck('No army fort unit or standard 1500-job admin added',not any(p.startswith('common/history/military_formations/') or p.startswith('common/combat_unit_types/') for p in files) and 'building_government_administration' not in core.qa.signature(admin))
    for p,raw in files.items():
        ck('Exact installed candidate '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
        if p.endswith('.txt'):
            try:core.cw.parse(raw.lstrip('\ufeff'));ok=True
            except Exception:ok=False
            ck('Syntax '+p,ok)
        if p.endswith('.yml'):
            ck('Localization BOM '+p,(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'))
            pairs=re.findall(r'^ ([A-Za-z0-9_]+):0 "(.*)"$',raw,re.M);ck('Localization well formed '+p,len(pairs)==len(raw.splitlines())-1 and len(pairs)==len({k for k,v in pairs}))
    for p,raw in imperial.items():ck('Exact imperial compiled file '+p,(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    # Assets already shipped with the game; no copy or write into vanilla.
    for path in re.findall(r'(?:icon|texture|background) = "([^"]+)"','\n'.join(raw for p,raw in files.items() if p.startswith(('common/buildings/','common/production_methods/','common/production_method_groups/')))):
        ck('Existing engine icon '+path,(ROOT/path).is_file() or (core.qa.GAME/path).is_file())
    currentchanges=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));con=load(OUT/'CONCURRENT_BEFORE_INSTALL.json');allowed=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png'}
    ck('All other functional and concurrent files preserved',set(currentchanges)<=allowed|set(con['changes']) and all(current.get(p)==h for p,h in con['files'].items()),currentchanges)
    proofchanges=[p for p,h in b['reports'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)];ck('All old nested evidence and receipts immutable',not proofchanges,proofchanges)
    toolchanges=[p for p,h in b['tools'].items() if sha(ROOT/p)!=h];ck('Only bounded registry guard and tracker display wording changed',set(toolchanges)=={'tools/map2l_registry.py','tools/serg_closure_roadmap.py'},toolchanges)
    protected=[];overlaps=[]
    for d in reg.approved_lot_dirs():
        if d==OUT:continue
        for r in load(d/'GEOMETRY.json')['assignments']:
            if 'cells' not in r:continue
            hit=set(map(tuple,r['cells']))&set(map(tuple,CELLS))
            if hit:overlaps.append(dict(lot=d.name,rgb=r['rgb'],cells=sorted(hit)))
            protected.append(dict(lot=d.name,rgb=r['rgb'],owner=r['owner'],pixels=r['pixels']))
    ck('No prior approved core overlaps Brixen',not overlaps,overlaps)
    ca=dict(zip(*np.unique(a,return_counts=True)));cz=dict(zip(*np.unique(z,return_counts=True)));ck('Every old RGB cell count unchanged except parent',all(ca.get(int(rgb[1:],16))==cz.get(int(rgb[1:],16)) for rgb in old['geometry'] if rgb!=PARENT))
    dump('PROTECTED_CORE_CHECK.json',dict(rows=protected,old_geometry_rows=len(protected),overlaps=overlaps,only_changed_pixels=CELLS))
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip();ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    ck('No Brixen human receipt',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    state=load(rm.OUT/'ROADMAP_STATE.json');tr=next(t for t in state['tasks'] if t['id']=='SC1-TRENTO');ck('Trento receipt partial and whole region BLOCKED',tr['status']=='BLOCKED' and tr['installed_delivery_status']=='PASS_RUNTIME_USER_VALIDATED' and rm.partial_runtime_evidence(tr))
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,engine_executed=False,automated_engine_test=False)
    dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current));owned=sorted(set(currentchanges)-set(con['changes']))
    dump('FILES_MODIFIED.json',dict(task_ids=[TASK],runtime_files=owned,sha256={p:current[p] for p in owned},old_tools_changed=['tools/map2l_registry.py','tools/serg_closure_roadmap.py'],concurrent_changes_preserved_not_written=con['files']))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'],v['failed']

def tests():
    import serg_sc4_ligurian_fiefs as lig
    review=load(prior.OUT/'TEST_REVIEW.json');inherited=set(review['historical_final_layer_assertions']);obsolete=set(review['obsolete_snapshot_assertions'])|{'test_serg_sc1_trento.TrentoContracts.test_current_chain_retains_both_user_validated_nuclei'}
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen']
    for label,names in [('TESTS',modules),('SCOPED_TESTS',['test_serg_sc1_brixen'])]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names));failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors];unknown=[f for f in failures if f['id'] not in inherited|obsolete]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8');dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if unknown else 'OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY' if failures else 'PASS',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unknown,automated_engine_test=False))
        print(label,r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,'unexplained',len(unknown),flush=True);assert not unknown,unknown
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),obsolete_snapshot_assertions=sorted(obsolete),old_tests_not_modified=True,unexplained_failures=[],replacement='Current cumulative Salzburg -> Massa -> Trento -> Brixen plus negative guard contracts. Earlier fixed-last-layer assertions preserved unchanged.'))

def documentation():
    source=OUT/'HOMANN_1716_TIROL.jpg';v=load(OUT/'VALIDATION.json');tests=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    dump('SOURCE_READING.json',dict(date='2026-10-23',historical_date='1776-01-01',historical_map_actually_viewed=dict(path=source.relative_to(ROOT).as_posix(),sha256=sha(source),detail=PREFIX+'HOMANN_1716_BRIXEN_DETAIL.png',method='browser image and local cropped detail visually inspected',geodetic_overlay=False,cadastral_boundary_read=False),archival_inventories_read=True,original_1776_acts_transcribed=False,old_R4_alignment_reused=False,modern_administrative_borders_used=False,bishop_source_access='Full indexed institutional biography; direct page cache miss',population_source=dict(url='https://www.oeaw.ac.at/fileadmin/subsites/Institute/VID/PDF/Publications/diverse_Publications/Historisches_Ortslexikon/Ortslexikon_Suedtirol.pdf',pages=[3,4,5,6,7],read='PDF text',rounded_residence_estimate=3000,exact_1776_census=False)))
    rows=[['Brixen résidence','Temporalité du prince-évêque et conseil aulique distincte du diocèse','BRX xEDBE00, neuf cellules B ; 3000 résidents','Hofarchiv ; Homann 1716 ; ÖAW','Position relative, pas limite cadastrale'],['Bruneck / Puster','Ressorts épiscopaux distincts des juridictions tyroliennes voisines','Aucune extension ; obligation ouverte','ÖAW ; Tiroler Landesarchiv','Ne pas annexer tout le Puster ou Lienz'],['Klausen / Feldthurns','Juridictions et droits temporels à cartographier séparément','AUS inchangé hors noyau ; obligation ouverte','ÖAW ; Tiroler Landesarchiv','Pas une conservation définitivement approuvée'],['Hofgericht / Albeins / Pfeffersberg / Lüsen','Possessions autour de la résidence et ressorts propres','Neuf cellules ne les certifient pas ; obligation ouverte','ÖAW ; inventaire Hofarchiv','Carte juridictionnelle datée et démographie nécessaires'],['Buchenstein / Enneberg / Antholz et autres enclaves','Temporalité, seigneuries foncières et diocèse à distinguer','Aucun transfert sans attribution ; obligation ouverte','Inventaires à approfondir','Ne pas déduire les frontières de la seule coloration Homann'],['Veldes / Bled et droits éloignés','Possession foncière ne signifie pas automatiquement souveraineté impériale','Aucune nouvelle terre hors Tyrol ; obligation ouverte','Fonds juridictionnels à rechercher','Statut et limites en 1776 non établis dans cette passe'],['Tyrol / Habsbourg','Défense et fiscalité communes ne suppriment pas la principauté','Pacte AUS–BRX natif national B ; aucune armée nouvelle','Landlibell, Tiroler Landesarchiv','Quotas et restrictions régionales non entièrement simulés'],['Trente / Salzbourg / Venise / voisins','Principautés et possessions voisines distinctes','Tous noyaux et localisateurs antérieurs conservés','Reçus et géométries cumulatives','Aucune deuxième tâche ou réparation Tyrol automatique']]
    with (OUT/'JURISDICTION_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['jurisdiction','historical_distinction_1776','implementation','source','limit']);w.writerows(rows)
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['rgb','state','previous_owner','owner','cells_after','category'])
        for r in load(OUT/'GEOMETRY.json')['assignments']:w.writerow([r['rgb'],r['state'],r['previous_owner'],r['owner'],r['pixels'],r['confidence']])
    sub=dict(id='BR-I-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',tag=TAG,state=SID,category='B',cells=CELLS,new_rgb=RGB,previous_owner='AUS',population_transferred=POP,scope='Brixen residence nucleus only; Leopold, small public court, temporal imperial title and Austrian defensive bond. Automatic capital point pending player test; not whole principality, diocese or peripheral jurisdictions.')
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',regional_status='BLOCKED',sub_lots=[sub],independently_testable_components=[dict(id='BR-T-CORE',test='9 cells, 3000 transfer, neighbors and automatic capital point'),dict(id='BR-I-COURT',test='Leopold, theocracy, laws and 200-job public chancery'),dict(id='BR-P-DEFENCE',test='imperial rights and AUS defensive pact')],no_runtime_attestation=True,regional_cadastral_closure=False,points_awarded=0,political_approximation='B'))
    report=f'''**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# SC1-BRIXEN — noyau B de résidence

**82/235 = 34,89 % avant/après**, 24 tâches qualifiées sur 81, périmètre 1.0.0 et poids inchangés. Le reçu réel **TR-I-CORE PASS_RUNTIME_USER_VALIDATED** est enregistré pour les douze cellules et le protocole rapporté dans USER_MISSION.txt, sans date de test inventée. Contrôle d'acceptation Trente 9/9 et 103 empreintes de livraison exactes. **SC1-TRENTO reste BLOCKED P1**, zéro point : Non/Sole, Giudicarie, Riva/Ledro, Pergine, Fiemme et autres possessions restent ouverts. Aucune extension de l'attestation.

Après cette acceptation, le validateur confirme **SC1-BRIXEN P1**, dépendance Salzbourg satisfaite. Une seule nouvelle tâche exécutée. Le Tyrol ne devient pas admissible : il dépend des deux principautés non closes.

## Recherche et choix

Les sources institutionnelles distinguent principauté temporelle, diocèse, dépendances et défense tyrolienne. **Leopold Maria Joseph von Spaur** règne en janvier 1776 ; le coadjuteur Ignaz Joseph n'est pas substitué. Homann 1716 et son détail sont réellement lus ; le positionnement est relatif aux villes voisines, sans vieux recalage R4 ni frontière contemporaine. SOURCES.md précise les accès réussis et infructueux ; SOURCE_READING.json et JURISDICTION_MATRIX.csv bornent chaque conclusion. B_PROPOSAL.md compare A (juridictions complètes), B (résidence installée) et C (absence de représentation).

## Installation limitée

**BR-I-CORE : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** ; région **BLOCKED P1**. TAG libre **BRX**, nouveau RGB **xEDBE00**, **neuf cellules AUS→BRX** dans STATE_SOUTH_TYROL ; parent xD040E0 **462→453**, connecté. Tous les autres RGB, notamment TRT, intacts. Aucun localisateur physique ni référence urbaine ancienne changé. La capitale nationale possède sa portion ; une action enfant nomme seulement cette portion et son city Brixen. **Le placement automatique de sa capitale à l'intérieur du noyau reste à vérifier en jeu** : aucun point urbain Brixen existant n'est présenté comme une preuve acquise.

**3 000 habitants transférés** depuis le groupe south_german AUS de 91 500→88 500 ; portion AUS 482 000→479 000, germanophones 183 000→180 000. Nord-italiens 299 000 et TRT 9 000 inchangés. Population mondiale **834 926 252**, professions et religion par défaut conservées. Estimation arrondie de résidence, pas recensement 1776 ou total diocésain ; aucune population créée pour remplir une administration.

Leopold, théocratie catholique, lois impériales, capitale et **une chancellerie publique non extensible de 200 postes** (paramètres de jeu modestes, pas effectifs historiques certifiés). Aucun bâtiment, ressource, caserne, fort ou régiment pris au voisin ; pas d'armée fictive. Pacte **AUS–BRX** : approximation nationale du lien défensif du Landlibell, sans quotas régionaux ni union personnelle. Succession capitulaire abstraite. Croix rouge moteur provisoire, ni aigle à crosse temporel ni Agneau pascal diocésain de la source cathédrale ; amélioration visuelle P2 distincte.

Registre impérial **576→577**, tous les titres antérieurs conservés, même emprise physique ; BRX membre sans ville libre et **neuf électeurs**. Aucun transfert de Bolzano, Merano, Rovereto, Innsbruck ou Lienz. La région n'est pas close : Bruneck/Puster, Klausen/Feldthurns, ressorts ruraux, enclaves et possessions éloignées demandent attribution détaillée et démographie. Leur absence actuelle n'est pas approuvée définitivement.

## Contrôles et suite

**{v['passed']}/{v['total']} contrôles statiques**. **{tests['passed']}/{tests['total']} tests cumulatifs réussis**, {len(tests['failed'])} anciennes assertions de dernière couche conservées et explicitement classées, {len(tests['skipped'])} test ignoré hérité ; aucun échec inexpliqué. **{scoped['passed']}/{scoped['total']} tests Brixen ciblés** : refus d'extension Bolzano/Puster, de reprise de Trente, de ville libre et d'emprise ajoutée ; contrôles des reçus limités. Les tests antérieurs n'ont pas été modifiés. Contrats finaux de suivi et conservation dans FINAL_TESTS.json / FINAL_CHECKS.json.

Tous les anciens fichiers fonctionnels hors périmètre déclaré, preuves imbriquées et reçus sont contrôlés par empreintes. Le contrôle juste avant installation ne détecte aucun changement concurrent fonctionnel depuis l'entrée ; les travaux fortifications/génie, France/Anzin/Saint-Gobain/drainage et États-Unis déjà présents sont conservés. HEAD, branche et index inchangés ; aucune écriture Git ou vanilla. Quatre blancs en fin de ligne hérités, non nettoyés, restent classés séparément. Un libellé P0 figé du générateur de BLOCKERS est remplacé par « blocage régional », pour représenter correctement Brixen P1 sans changer les règles de progression (TRACKER_RENDER_FIX.json).

**Prochaine action : test joueur de BR-I-CORE**, nouvelle partie 1776, capitale et noms, institutions, défense, voisins, un mois, sauvegarde/rechargement : PLAYER_TEST_PROTOCOL.md. Aucun moteur exécuté par l'agent, aucun reçu humain Brixen ni point ajouté. Candidate indépendante **SC1-BERCHTESGADEN P1**, sélection recalculée après blocage régional ; elle reste NOT_STARTED et n'est pas commencée. Innviertel/SC2-AUSTRIA, Teschen, Trente et autres blocages antérieurs restent inchangés.
'''
    (OUT/'REPORT.md').write_text(report,encoding='utf8')

def tracking():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');assert s==b['roadmap'];assert load(OUT/'VALIDATION.json')['status']=='PASS' and not load(OUT/'TESTS.json')['unexplained_failures'] and load(OUT/'SCOPED_TESTS.json')['status']=='PASS'
    assert rm.progress(s)['next_task']==TASK;t=next(t for t in s['tasks'] if t['id']==TASK)
    reason=('Noyau de résidence BR-I-CORE installé seulement ; Bruneck/Puster, Klausen/Feldthurns, Hofgericht, Albeins/Pfeffersberg/Lüsen et autres dépendances/enclaves restent à attribuer sur carte juridictionnelle datée et avec démographie correspondante. '
        'Droits éloignés, dont Veldes/Bled, à distinguer de souveraineté impériale ; aucun transfert fondé sur le seul diocèse. Le noyau B ne clôture pas ces obligations et leur représentation actuelle n’est pas approuvée définitivement.')
    note=('Brixen : BR-I-CORE, TAG BRX, neuf cellules xEDBE00 depuis AUS xD040E0 462→453 ; 3000 habitants south_german transférés, monde conservé. '
        'Leopold Maria Joseph von Spaur, théocratie, chancellerie publique de 200 postes et pacte défensif AUS. Aucune armée ou modification de hub existant. '
        'Capitale dans une portion possédée ; placement automatique du centre et nom Brixen à contrôler en jeu. Registre 576→577, même emprise et neuf électeurs. '
        'Seul BR-I-CORE IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; SC1-BRIXEN BLOCKED P1 pour les possessions restantes, zéro point. Trente et autres noyaux/reçus protégés ; aucune validation humaine Brixen.')
    t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=load(OUT/'IMPLEMENTATION.json')['sub_lots'],installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md',PREFIX+'B_PROPOSAL.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope='BR-I-CORE only: nine-cell residence B, 3000 residents transferred, Leopold, chancery, automatic capital placement, imperial rights and defensive bond. Not all temporal possessions or diocese.',new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),blocking_reason=reason,residual_uncertainty=reason+' Pacte national et succession capitulaire abstraits ; paramètres de chancellerie techniques, blason provisoire P2.',current_delivery_note=note,decision=None,delivered_scope=dict(classification='B_EPISCOPAL_RESIDENCE_NUCLEUS',sub_lots=['BR-I-CORE'],new_tag=TAG,new_rgb=RGB,installed_cells=9,transferred_population=POP,cadastral_validation=False,full_principality_coverage=False,world_population_unchanged=True,imperial_physical_extent_unchanged=True),remaining_territorial_obligations=[dict(id=id,status='OPEN_NOT_VALIDATED',scope=scope) for id,scope in [('BR-PUSTER','Bruneck, Oberamt and episcopal rights in Puster, not all neighboring Tyrolean jurisdictions'),('BR-ISARCO','Klausen, Feldthurns, Hofgericht and neighboring rural jurisdictions'),('BR-RURAL','Albeins, Pfeffersberg, Luesen and other rural possessions'),('BR-ENCLAVES','Buchenstein, Enneberg, Antholz and other enclaves, dated temporal attribution required'),('BR-DISTANT','Veldes/Bled and distant rights; property vs imperial temporal sovereignty to establish')]])
    t['historical_sources'].append(PREFIX+'SOURCES.md:1');s['mission_status']='BRIXEN_RESIDENCE_CORE_PENDING_USER_REGION_BLOCKED'
    probe=copy.deepcopy(s);probe.pop('runtime_validation_hold',None);candidate=rm.progress(probe)['next_task'];assert candidate=='SC1-BERCHTESGADEN',candidate
    s['runtime_validation_hold']=dict(task_id=TASK,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,reason='Une seule nouvelle tâche exécutée ; test joueur du noyau Brixen avant toute suite autorisée.',test_summary=TEST_SUMMARY,scope_note=SCOPE_NOTE)
    s['events'].append(dict(id='SERG-RM-0030',date='2026-10-23',kind='SCOPED_EPISCOPAL_IMPLEMENTATION_WITH_TERRITORIAL_BLOCK',scope_version='1.0.0',source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],sub_lot_changes=[dict(id='BR-I-CORE',before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+n for n in ['REPORT.md','VALIDATION.json','TESTS.json','PLAYER_TEST_PROTOCOL.md','IMPLEMENTATION.json']],note=note+' '+reason+' Progression 82/235=34,89 % avant/après. Candidate indépendante Berchtesgaden identifiée seulement ; aucune seconde tâche.'))
    assert s['events'][:-1]==b['roadmap']['events'];assert [x for x in s['tasks'] if x['id']!=TASK]==[x for x in b['roadmap']['tasks'] if x['id']!=TASK]
    p=rm.progress(s);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,TASK),p
    assert not rm.structural_errors(s),rm.structural_errors(s);rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged=True,previous_29_events_unchanged=True,points_awarded=0,scope_version='1.0.0',next_candidate=candidate));print('Tracker PASS; 82/235; Brixen player test pending; Berchtesgaden not started',flush=True)

def final_tests():
    stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_serg_closure_roadmap','test_serg_sc1_brixen']));failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
    (OUT/'FINAL_TESTS.log').write_text(stream.getvalue(),encoding='utf8');dump('FINAL_TESTS.json',dict(task_ids=[TASK],status='PASS' if not failures else 'FAIL',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],automated_engine_test=False));print('Final contracts',r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,flush=True);assert not failures,failures

def maps():
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');b=load(OUT/'BASELINE.json');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners[RGB]=TAG
    x0,y0,x1,y1,s=4343,934,4388,983,14;panel=(x1-x0)*s+60
    im=Image.new('RGB',(2*panel,(y1-y0)*s+150),'#faf8ef');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for k,(arr,title) in enumerate([(a,'AVANT : residence incluse dans AUS'),(z,'INSTALLE B : BRX rouge, neuf cellules')]):
        ox=k*panel;d.text((ox+10,10),title,font=font,fill='black')
        for y in range(y0,y1):
            for x in range(x0,x1):
                rgb='x'+format(int(arr[y,x]),'06X');u=ox+42+(x-x0)*s;v=52+(y-y0)*s
                d.rectangle((u,v,u+s,v+s),fill='#a94355' if rgb==RGB else '#5b7488' if rgb==prior.RGB else '#dcbd87' if owners.get(rgb)=='AUS' else '#d9dfb6',outline='#bbb')
                if arr[y,x]!=arr[y,x-1]:d.line((u,v,u,v+s),fill='#333',width=2)
                if arr[y,x]!=arr[y-1,x]:d.line((u,v,u+s,v),fill='#333',width=2)
        for x in range(x0,x1,5):d.text((ox+42+(x-x0)*s,30),str(x),font=font,fill='black')
        for y in range(y0,y1,5):d.text((ox+5,52+(y-y0)*s),str(y),font=font,fill='black')
        for label,x,y in [('Innsbruck',4352.960,938.379),('Bolzano wood',4358.965,957.048),('Merano mine',4349.286,956.797),('Lienz mine',4381.637,951.180),('Trente TRT city',4352.081,973.938),('Rovereto farm',4347.678,981.101)]:
            u=ox+42+(x-x0)*s;v=52+(y-y0)*s;d.ellipse((u-3,v-3,u+3,v+3),fill='white',outline='black');d.text((u+5,v-14),label,font=font,fill='black',stroke_width=2,stroke_fill='white')
        u=ox+42+(4363-x0)*s;v=52+(949-y0)*s;d.text((u+20,v-10),'Brixen : noyau B',font=font,fill='#8c2233',stroke_width=2,stroke_fill='white')
    d.text((10,im.height-62),'BRX rouge / TRT bleu / AUS ocre. Tous les localisateurs existants restent fixes.',font=font,fill='black')
    d.text((10,im.height-40),'La capitale automatique BRX est a verifier en jeu ; aucune nouvelle coordonnee urbaine native n’est certifiee.',font=font,fill='black')
    d.text((10,im.height-20),'Residence politique seulement ; pas le diocese, tout Isarco/Puster ou les enclaves.',font=font,fill='black');im.save(OUT/'BEFORE_AFTER.png')

def finalize():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');p=rm.progress(s);current=prior.prior.italian.runtime_hashes();static=load(OUT/'SESSION_AFTER_STATIC.json');owned=load(OUT/'FILES_MODIFIED.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    changes=sorted(k for k in set(current)|set(static['hashes']) if current.get(k)!=static['hashes'].get(k));ck('No runtime change since successful static validation',not changes,changes)
    ck('Exact delivered functional bytes retained',all(current.get(k)==h for k,h in owned['sha256'].items()));ck('Current history inventory unchanged since static',core.qa.inventory()==static['inventory'])
    checked=rm.check();dump('TRACKER_VALIDATION_FINAL.json',checked);ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    ck('Evidence-based progress unchanged 82/235 34.89 percent',(p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],len(s['tasks']))==(82,235,'34.89',24,81))
    ck('Only Brixen changed after accepted Trento core',[t for t in s['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK])
    ck('Previous 29 events unchanged',s['events'][:-1]==b['roadmap']['events'] and s['events'][-1]['id']=='SERG-RM-0030')
    ck('Player Brixen next, Berchtesgaden not begun',p['next_task']==TASK and s['runtime_validation_hold']['next_implementation_candidate']=='SC1-BERCHTESGADEN' and next(t for t in s['tasks'] if t['id']=='SC1-BERCHTESGADEN')['status']=='NOT_STARTED')
    view=(rm.OUT/'NEXT_ACTION.md').read_text(encoding='utf8');ck('Next action uses actual Brixen test and scope',TEST_SUMMARY in view and SCOPE_NOTE in view and 'Colloredo' not in view)
    br=next(t for t in s['tasks'] if t['id']==TASK);ck('Brixen partial pending, region blocked, no human fiction',br['status']=='BLOCKED' and br['priority']=='P1' and br['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and br['runtime_validation']['attestation'] is None and not list(OUT.glob('RUNTIME_USER_ATTESTATION*')) and len(br['remaining_territorial_obligations'])==5)
    tr=next(t for t in s['tasks'] if t['id']=='SC1-TRENTO');ck('Trento real limited receipt and six open obligations retained',tr['status']=='BLOCKED' and tr['installed_delivery_status']=='PASS_RUNTIME_USER_VALIDATED' and rm.partial_runtime_evidence(tr) and len(tr['remaining_territorial_obligations'])==6)
    ck('All previous terminal qualifications retained',rm.qualifications(s)==rm.qualifications(b['roadmap']))
    canonical={fp.relative_to(ROOT).as_posix() for fp in rm.OUT.iterdir() if fp.is_file()};oldchanges=[rel for rel,h in b['reports'].items() if rel not in canonical and (not (ROOT/rel).is_file() or sha(ROOT/rel)!=h)];ck('All previous nested proofs receipts and tests unchanged',not oldchanges,oldchanges)
    toolchanges=[k for k,h in b['tools'].items() if sha(ROOT/k)!=h];ck('Only declared registry and tracker display tools changed',set(toolchanges)=={'tools/map2l_registry.py','tools/serg_closure_roadmap.py'},toolchanges)
    fix=load(OUT/'TRACKER_RENDER_FIX.json');ck('Tracker edit is exactly the recorded presentation substitution',fix['only_documented_substitution'] and fix['before_sha256']==b['tools'][fix['file']] and sha(ROOT/fix['file'])==fix['after_sha256'] and not fix['progress_rules_changed'])
    ck('Both localizations have same 15 keys without duplicate or vanilla collision',load(OUT/'LOCALIZATION_REVIEW.json')['status']=='PASS')
    con=load(OUT/'CONCURRENT_BEFORE_INSTALL.json');ck('Concurrent runtime preserved since review',all(current.get(k)==h for k,h in con['files'].items()))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');ys,xs=np.where(a!=z);ck('Exactly nine final changed cells',sorted(zip(xs.tolist(),ys.tolist()))==sorted(map(tuple,CELLS)))
    ck('Trento 12 and Massa 8 cells exact',all(int(z[y,x])==int(prior.RGB[1:],16) for x,y in prior.CELLS) and int((z==int(prior.RGB[1:],16)).sum())==12 and all(int(z[y,x])==int(prior.prior.RGB[1:],16) for x,y in prior.prior.CELLS) and int((z==int(prior.prior.RGB[1:],16)).sum())==8)
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);findings=[line for line in diff.stdout.splitlines() if 'trailing whitespace.' in line];ok=len(findings)==4 and all(line.startswith('common/history/pops/00_west_europe.txt:') for line in findings) and diff.returncode==2
    dump('DIFF_CHECK.json',dict(status='INHERITED_WHITESPACE_ONLY' if ok else 'REVIEW_REQUIRED',returncode=diff.returncode,findings=findings,preexisting_findings=4,old_tabs_not_cleaned=True,stderr=diff.stderr));ck('Four inherited whitespace findings only',ok,findings)
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip();ck('Git HEAD branch index never changed',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    ck('All cumulative failures are six preserved historical fixed tails',not load(OUT/'TESTS.json')['unexplained_failures'] and len(load(OUT/'TESTS.json')['failed'])==6)
    ck('All final roadmap and current contracts pass',load(OUT/'FINAL_TESTS.json')['status']=='PASS');ck('Player protocol options and regional obligations documented',all((OUT/n).is_file() for n in ['PLAYER_TEST_PROTOCOL.md','B_PROPOSAL.md','SOURCES.md','JURISDICTION_MATRIX.csv','REPORT.md','BEFORE_AFTER.png']))
    final=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False)
    dump('FINAL_CHECKS.json',final);print('Final checks',final['passed'],'/',final['total'],final['failed'],flush=True);assert not final['failed'],final['failed']
    dump('SESSION_AFTER.json',dict(hashes=current,progress=p,git_head=b['git']['head'],git_branch=b['git']['branch'],git_index_sha256=b['git']['index_sha256'],previous_proofs_checked=len(b['reports'])))
    manifest={rel:sha(ROOT/rel) for rel in owned['runtime_files']}
    for fp in list(OUT.rglob('*'))+list(prior.OUT.glob('*2026_10_23*')):
        if fp.is_file() and fp.name!='DELIVERY_MANIFEST.json':manifest[fp.relative_to(ROOT).as_posix()]=sha(fp)
    for rel in canonical|{reg.active_registry_path().relative_to(ROOT).as_posix(),'tools/serg_sc1_brixen.py','tools/test_serg_sc1_brixen.py','tools/serg_closure_accept_trento.py','tools/map2l_registry.py','tools/serg_closure_roadmap.py'}:manifest[rel]=sha(ROOT/rel)
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK,'SC1-TRENTO'],files=manifest,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',brixen_regional_status='BLOCKED',trento_core_status='PASS_RUNTIME_USER_VALIDATED',trento_regional_status='BLOCKED',concurrent_runtime_observed_not_written=con['files'],automated_engine_test=False));assert all(sha(ROOT/rel)==h for rel,h in manifest.items());print('Delivery manifest verified',len(manifest),'files; no second new task begun',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
