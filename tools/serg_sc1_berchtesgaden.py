"""One guarded Berchtesgaden pass; no fabricated human validation."""
import collections as C,contextlib,copy,csv,io,json,os,re,shutil,subprocess,sys,unittest
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc1_brixen as prior
import serg_sc4_italian_states as italian
import serg_sc4_piombino as physical
ROOT=prior.ROOT;rm=prior.rm;core=prior.core;reg=prior.reg;sha=prior.sha
TASK='SC1-BERCHTESGADEN';OUT=rm.OUT/TASK;PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
TAG='BGT';RGB='xEDBF00';PARENT='xAB7EB0';SID='STATE_TYROL';POP=1000
CELLS=[[4384,930],[4384,931],[4385,930],[4385,931]]
TEST_SUMMARY='Nouvelle partie au 1er janvier 1776 : BG-I-CORE, Berchtesgaden (BGT), quatre cellules B et 1000 habitants ; capitale Berchtesgaden dans la portion BGT, Franz Anton Josef von Hausen-Gleichenstorff prince-prévôt, théocratie, chancellerie de 100 postes et petite saline de 100 postes. Vérifier sel, financement, relations, droits impériaux sans dixième électeur et tous les voisins, notamment les douze cellules SLZ. Simuler un mois, sauvegarder puis recharger ; rapporter les résultats réels.'
SCOPE_NOTE='BG-I-CORE couvre la résidence et une petite activité saline, pas toutes les Gnotschaften, Schellenberg, Ramsau ou Königssee. SC1-BERCHTESGADEN reste BLOCKED P1 pour leur attribution et démographie ; aucun reçu humain nouveau. BR-I-CORE et TR-I-CORE sont validés dans leurs seuls noyaux, leurs régions restent bloquées et le Tyrol demeure dépendant. SC1-PASSAU-OUTLIERS est identifiée sans commencement.'
MISSION=Path('C:/Users/simeo/.codex/attachments/1e4e02a3-f955-41a1-bae1-adb66732e090/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def load(p):return rm.load_json(p)
def dump(n,o):rm.write_json(OUT/n,o)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    state=load(rm.OUT/'ROADMAP_STATE.json');checked=rm.check()
    assert checked['status']=='PASS' and rm.progress(state)['next_task']==TASK and state['events'][-1]['id']=='SERG-RM-0031'
    OUT.mkdir(exist_ok=True);hashes=italian.runtime_hashes();inv=core.qa.inventory();git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json',dict(roadmap=state,inventory=inv,hashes=hashes,registry=load(reg.active_registry_path()),reports=proofs,tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=sha(ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal'))))
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png');shutil.copyfile(MISSION,OUT/'USER_MISSION.txt');dump('ENTRY_TRACKER_VALIDATION.json',checked);print('Berchtesgaden selected P1 after real partial BRX receipt; 82/235',flush=True)

def survey():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(OUT/'provinces_before.png');targets={'STATE_BAVARIA','STATE_TYROL','STATE_AUSTRIA','STATE_STYRIA'};rows=[]
    for r in inv['owners']:
        rgb,sid,tag=r['key']
        if sid not in targets:continue
        yy,xx=np.where(a==int(rgb[1:],16));rows.append(dict(rgb=rgb,state=sid,owner=tag,cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    tags=['BGT','BCH','BRG','BCG'];use={t:[] for t in tags}
    for folder in ['common/country_definitions','common/flag_definitions']:
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            raw=p.read_text(encoding='utf-8-sig')
            for t in tags:
                if re.search(r'\b'+t+r'\b',raw):use[t].append(str(p))
    import serg_sc1_salzburg as slz
    hubs=slz.prior.pas.prior.q.r9.locators(a);dump('LOCATORS_BEFORE.json',hubs)
    dump('NATIVE_INVENTORY.json',dict(provinces=rows,candidate_tags=use,countries={t:inv['countries'].get(t) for t in ['BAV','SLZ','AUS']+tags},populations=[r for r in inv['regional_pop'] if r['key'][0] in targets],buildings=[r for r in inv['buildings'] if r['key'][0] in targets],units=[r for r in inv['units'] if r['key'][0] in {'BAV','SLZ','AUS'}],nearby_hubs=[r for r in hubs if 4360<r['X']<4420 and 900<r['Y']<960]))
    print('Tags',json.dumps(use),flush=True)
    for r in rows:
        if 4365<r['bounds'][2] and r['bounds'][0]<4420 and 905<r['bounds'][3] and r['bounds'][1]<950:print(r,flush=True)
    for r in inv['regional_pop']:
        if r['key'][0] in {'STATE_BAVARIA','STATE_TYROL'}:print('population',r,flush=True)
    for r in hubs:
        if 4360<r['X']<4420 and 910<r['Y']<950:print('hub',r,flush=True)

def compiler_before():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();actual={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in files};diff=[p for p,raw in files.items() if raw.lstrip('\ufeff')!=actual[p]]
    dump('COMPILER_BEFORE.json',dict(actual=actual,differences=diff));print('Compiler preflight',diff,flush=True);assert not diff

def prepare():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png');assert italian.runtime_hashes()==b['hashes']
    assert TAG not in b['inventory']['countries'] and RGB not in b['inventory']['geometry'] and not np.any(a==int(RGB[1:],16)) and not load(OUT/'NATIVE_INVENTORY.json')['candidate_tags'][TAG]
    after=a.copy()
    for x,y in CELLS:assert a[y,x]==int(PARENT[1:],16);after[y,x]=int(RGB[1:],16)
    yy,xx=np.where(after==int(PARENT[1:],16));assert len(physical.components(xx,yy))==1
    rows=[]
    for rgb,tag in [(PARENT,'AUS'),(RGB,TAG)]:
        yy,xx=np.where(after==int(rgb[1:],16));points=sorted([[int(x),int(y)] for x,y in zip(xx,yy)]);rows.append(dict(rgb=rgb,parent_rgb=PARENT,state=SID,previous_owner='AUS',owner=tag,pixels=len(points),cells=points,confidence='B_POLITICAL_APPROXIMATION' if tag==TAG else 'RETAINED_NOT_CERTIFIED'))
    geo=dict(parents=[PARENT],assignments=rows,new_provinces=[dict(rgb=RGB,parent_rgb=PARENT)],new_members=[TAG],free_cities=[],selected_option='BERCHTESGADEN_RESIDENCE_CORE',classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,hub_rebindings=[])
    files={};originals={}
    def old(p):
        assert sha(ROOT/p)==b['hashes'][p];raw=(ROOT/p).read_bytes().decode('utf8');originals[p]=raw;return raw
    p='common/history/states/00_states.txt';raw=old(p);n=core.state(raw,SID);files[p]=core.edits(raw,[(n.end-1,n.end-1,'\n\t\t# SC1-BERCHTESGADEN: sovereign residence B, technical region is not sovereignty.\n\t\tcreate_state = { country = c:BGT owned_provinces = { xEDBF00 } }\n\t')]).replace('\t\n\t\t# SC1-BERCHTESGADEN:','\n\t\t# SC1-BERCHTESGADEN:')
    p='map_data/state_regions/00_west_europe.txt';raw=old(p);off=int(raw.startswith('\ufeff'));n=next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID);f=n.children('provinces')[0];frag=raw[f.start+off:f.end+off];assert frag.count('"'+PARENT+'"')==1
    files[p]=core.edits(raw,[(f.start+off,f.end+off,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    p='map_data/province_terrains.txt';raw=old(p);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)};assert RGB.upper() not in terrain;files[p]=raw+'\n'+RGB+'="'+terrain[PARENT.upper()]+'"\n'
    p='common/history/pops/00_west_europe.txt';raw=old(p);n=core.region(raw,SID,'AUS');donors=[pop for pop in n.children('create_pop') if pop.one('culture')=='south_german' and pop.one('religion') is None and pop.one('pop_type') is None];assert donors
    donor=next(pop for pop in donors if int(pop.one('size'))>=POP);f=donor.children('size')[0];amount=int(f.value);raw=core.edits(raw,[(f.start,f.end,'size = '+str(amount-POP))]);files[p]=core.append(raw,SID,TAG,'\n\t\t\tcreate_pop = { culture = south_german size = 1000 }\n').replace('\t\n\t\tregion_state:BGT','\n\t\tregion_state:BGT')
    defs='BGT = { color = { 113 73 139 } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = STATE_TYROL }\n';files['common/country_definitions/1776_sc1_berchtesgaden.txt']=defs
    files['common/history/countries/bgt - berchtesgaden.txt']='''COUNTRIES = {
 c:BGT ?= {
  effect_starting_politics_reactionary = yes
  activate_law = law_type:law_theocracy
  activate_law = law_type:law_autocracy
  activate_law = law_type:law_state_religion
  activate_law = law_type:law_religious_schools
  activate_law = law_type:law_hereditary_bureaucrats
  activate_law = law_type:law_serfdom
  activate_law = law_type:law_land_based_taxation
  activate_law = law_type:law_aor1776_imperial_customs
  activate_law = law_type:law_aor1776_imperial_no_slavery
 }
}
'''
    files['common/history/characters/1776_sc1_berchtesgaden.txt']='''CHARACTERS = { c:BGT ?= { create_character = {
 first_name = aor1776_bgt_first last_name = aor1776_bgt_last
 historical = yes culture = south_german religion = rel:catholic ruler = yes
 # Approximate engine age only; no unverified exact birth date is asserted.
 age = 60 interest_group = ig_devout ideology = ideology_traditionalist
} } }
'''
    files['common/government_types/00_1776_sc1_berchtesgaden.txt']='gov_aor1776_berchtesgaden = { transfer_of_power = dictatorial male_ruler = "aor1776_bgt_ruler" female_ruler = "aor1776_bgt_ruler_female" possible = { c:BGT ?= this has_law = law_type:law_theocracy } on_government_type_change = { change_to_dictatorial = yes } on_post_government_type_change = { post_change_to_dictatorial = yes } }\n'
    files['common/buildings/1776_sc1_berchtesgaden.txt']='''# Fixed small existing institutions. No standard 1500-job administration or 5000-job mine.
building_aor1776_berchtesgaden_chancery = {
 building_group = bg_bureaucracy city_type = city levels_per_mesh = 50
 expandable = no buildable = no downsizeable = no
 potential = { state_region = s:STATE_TYROL owner = { c:BGT ?= this } }
 production_method_groups = { pmg_aor1776_berchtesgaden_chancery }
 icon = "gfx/interface/icons/building_icons/building_government_administration.dds"
 required_construction = construction_cost_very_low
 background = "gfx/interface/icons/building_icons/backgrounds/building_panel_bg_monuments.dds"
}
# Inland wood-fired brine boiling, not a coastal pan or a new mining concession.
building_aor1776_berchtesgaden_saline = {
 building_group = bg_light_industry city_type = city levels_per_mesh = 50
 expandable = no buildable = no downsizeable = no ownership_type = self
 potential = { state_region = s:STATE_TYROL owner = { c:BGT ?= this } }
 production_method_groups = { pmg_aor1776_berchtesgaden_saline }
 icon = "gfx/interface/icons/building_icons/building_salt_mine.dds"
 required_construction = construction_cost_very_low
 background = "gfx/interface/icons/building_icons/backgrounds/building_panel_bg_mining.dds"
}
'''
    files['common/production_method_groups/1776_sc1_berchtesgaden.txt']='pmg_aor1776_berchtesgaden_chancery = { texture = "gfx/interface/icons/generic_icons/mixed_icon_ownership.dds" ai_selection = most_productive production_methods = { pm_aor1776_berchtesgaden_chancery } }\npmg_aor1776_berchtesgaden_saline = { texture = "gfx/interface/icons/generic_icons/1776_mixed_icon_production_yellow.dds" ai_selection = most_productive production_methods = { pm_aor1776_berchtesgaden_saline } }\n'
    files['common/production_methods/1776_sc1_berchtesgaden.txt']='''# Technical modest capacity; not reconstructed staffing or tonnage.
pm_aor1776_berchtesgaden_chancery = {
 texture = "gfx/interface/icons/production_method_icons/simple_organization.dds"
 country_modifiers = { workforce_scaled = { country_bureaucracy_add = 1 } }
 state_modifiers = { workforce_scaled = { state_tax_capacity_add = 1 } }
 building_modifiers = {
  workforce_scaled = { goods_input_paper_add = 0.5 }
  level_scaled = { building_employment_clerks_add = 25 building_employment_bureaucrats_add = 25 building_employment_clergymen_add = 25 building_employment_aristocrats_add = 25 }
 }
}
pm_aor1776_berchtesgaden_saline = {
 texture = "gfx/interface/icons/production_method_icons/picks_and_shovels.dds"
 building_modifiers = {
  workforce_scaled = { goods_input_wood_add = 1 goods_input_tools_add = 0.1 goods_output_salt_add = 1 }
  level_scaled = { building_employment_laborers_add = 95 building_employment_shopkeepers_add = 5 }
 }
}
'''
    files['common/history/buildings/1776_sc1_berchtesgaden.txt']='''BUILDINGS = { s:STATE_TYROL = { region_state:BGT = {
 create_building = { building = "building_aor1776_berchtesgaden_chancery" add_ownership = { country = { country = "c:BGT" levels = 1 } } reserves = 1 activate_production_methods = { "pm_aor1776_berchtesgaden_chancery" } }
 create_building = { building = "building_aor1776_berchtesgaden_saline" add_ownership = { country = { country = "c:BGT" levels = 1 } } reserves = 1 activate_production_methods = { "pm_aor1776_berchtesgaden_saline" } }
} } }
'''
    files['common/scripted_effects/1776_sc1_berchtesgaden.txt']='''assign_aor1776_berchtesgaden_names = {
 if = {
  limit = { state_region = s:STATE_TYROL owner = { c:BGT ?= this } }
  set_state_name = aor1776_state_berchtesgaden
  set_hub_name = { type = city name = aor1776_hub_berchtesgaden }
 }
}
'''
    files['common/on_actions/99_1776_sc1_berchtesgaden.txt']='''on_game_started = { on_actions = { aor1776_berchtesgaden_names_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_berchtesgaden_names_initialize } }
on_state_created = { on_actions = { aor1776_berchtesgaden_state_name_changed } }
on_state_owner_change = { on_actions = { aor1776_berchtesgaden_state_name_changed } }
on_become_subject = { on_actions = { aor1776_berchtesgaden_country_names_changed } }
on_become_independent = { on_actions = { aor1776_berchtesgaden_country_names_changed } }
aor1776_berchtesgaden_names_initialize = { effect = { every_state = { assign_aor1776_berchtesgaden_names = yes } } }
aor1776_berchtesgaden_state_name_changed = { effect = { assign_aor1776_berchtesgaden_names = yes } }
aor1776_berchtesgaden_country_names_changed = { effect = { every_scope_state = { assign_aor1776_berchtesgaden_names = yes } } }
'''
    files['common/coat_of_arms/coat_of_arms/1776_sc1_berchtesgaden.txt']='aor1776_berchtesgaden = { pattern = "pattern_solid.tga" color1 = "red" colored_emblem = { texture = "ce_keys_st_peter.dds" color1 = "yellow" color2 = "white" instance = { scale = { 0.8 0.8 } } } }\n';files['common/flag_definitions/1776_sc1_berchtesgaden.txt']='BGT = { flag_definition = { coa = aor1776_berchtesgaden priority = 100 allow_overlord_canton = no } }\n'
    # No diplomatic pact, union, vassalage or 1795 salt monopoly projected into 1776.
    for lang in ['french','english']:
        fr=lang=='french';pairs={'BGT':'Berchtesgaden','BGT_ADJ':'berchtesgadenois' if fr else 'Berchtesgadener','aor1776_bgt_first':'Franz Anton Josef','aor1776_bgt_last':'von Hausen-Gleichenstorff','aor1776_bgt_ruler':'Prince-prévôt' if fr else 'Prince-Provost','aor1776_bgt_ruler_female':'Princesse-prévôte' if fr else 'Princess-Provost','gov_aor1776_berchtesgaden':'Prévôté princière de Berchtesgaden' if fr else 'Prince-Provostry of Berchtesgaden','gov_aor1776_berchtesgaden_desc':('Le prince-prévôt gouverne avec le chapitre des chanoines. La chancellerie administre les affaires temporelles de cette petite principauté impériale, dont les salines et les ateliers alimentent les échanges avec les pays voisins.' if fr else 'The prince-provost governs with the chapter of canons. The chancery administers the temporal affairs of this small imperial principality, whose saltworks and workshops supply trade with neighboring lands.')+r'\n\n$TRANSFER_OF_POWER_NAME_DESC$','aor1776_state_berchtesgaden':'Berchtesgaden','aor1776_hub_berchtesgaden':'Berchtesgaden','building_aor1776_berchtesgaden_chancery':'Chancellerie de la prévôté' if fr else 'Provostry Chancery','building_aor1776_berchtesgaden_chancery_desc':'Les officiers du prince-prévôt et les chanoines règlent les affaires du territoire et du chapitre.' if fr else 'The prince-provost’s officers and canons administer the territory and chapter.','pmg_aor1776_berchtesgaden_chancery':'Administration capitulaire' if fr else 'Chapter Administration','pm_aor1776_berchtesgaden_chancery':'Officiers de la prévôté' if fr else 'Provostry Officers','building_aor1776_berchtesgaden_saline':'Saline de Frauenreuth' if fr else 'Frauenreuth Saltworks','building_aor1776_berchtesgaden_saline_desc':'La saumure des salines est chauffée au bois dans des poêles pour en recueillir le sel.' if fr else 'Brine is heated with wood in boiling pans to recover its salt.','pmg_aor1776_berchtesgaden_saline':'Ébullition de la saumure' if fr else 'Brine Boiling','pm_aor1776_berchtesgaden_saline':'Poêles à sel chauffées au bois' if fr else 'Wood-fired Salt Pans'}
        files['localization/'+lang+'/1776_sc1_berchtesgaden_l_'+lang+'.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    previous=[r for r in b['registry'] if r['state']==SID];assert any(r['rgb']==PARENT and r['beneficiary']=='AUS' for r in previous)
    addition=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC1-BERCHTESGADEN: four-cell sovereign residence B south-west of Salzburg; not whole gnotschaften or landholding rights')
    migration=dict(replaced_regions=[SID],previous=previous,updated=sorted(previous+[addition],key=lambda r:r['rgb']),new_members=[TAG],free_cities=[],new_provinces=geo['new_provinces'],geometry='SERG_CLOSURE/'+TASK+'/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],country_additions={TAG:core.qa.signature(core.cw.parse(defs)[0])})
    rel=reg.active_registry_path().relative_to(ROOT).as_posix();originals[rel]=(ROOT/rel).read_text(encoding='utf-8-sig');assert load(ROOT/rel)==b['registry'];files[rel]=json.dumps(sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    for p,raw in files.items():
        if p not in originals:assert not (ROOT/p).exists(),p
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration);dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(transferred=POP,donor='AUS',recipient=TAG,donor_before=454812,donor_after=453812,donor_south_german_before=349084,donor_south_german_after=348084,alemannic_unchanged=105728,donor_group_before=amount,donor_group_after=amount-POP,culture='south_german',religion='DEFAULT:south_german',profession='not declared',historical_basis='Rounded residence B estimate 1000, uncertainty 700-1500; OeAW 1698 Markt 97 fiscal properties among 957 for whole principality, not a household census. Whole territory approx 9000 before 1733 emigration and approx 10000 in 1803; no full-country total transferred. Not an exact 1776 census or a per-pixel allocation.',court_capacity=100,saline_capacity=100,capacities_are_technical=True))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png');print('Prepared BGT, 4 AUS cells, 1000 transferred residents; SLZ untouched',flush=True)

def review_concurrent():
    b=load(OUT/'BASELINE.json');cur=italian.runtime_hashes();planned=set(load(OUT/'EXPECTED_TEXT.json'))|{'map_data/provinces.png'};changes=sorted(k for k in set(cur)|set(b['hashes']) if cur.get(k)!=b['hashes'].get(k));overlap=sorted(set(changes)&planned);same=core.qa.inventory()==b['inventory']
    dump('CONCURRENT_BEFORE_INSTALL.json',dict(changes=changes,files={p:cur.get(p) for p in changes},hashes=cur,overlap_with_planned_files=overlap,inventory_unchanged=same));print('Concurrent runtime',changes,'overlap',overlap,'inventory unchanged',same,flush=True);assert not overlap and same

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');originals=load(OUT/'TEXT_BEFORE.json');review=load(OUT/'CONCURRENT_BEFORE_INSTALL.json')
    assert review['inventory_unchanged'] and not review['overlap_with_planned_files'] and italian.runtime_hashes()==review['hashes'];assert sha(ROOT/'.git/index')==b['git']['index_sha256'] and not load(OUT/'COMPILER_BEFORE.json')['differences']
    for p,raw in originals.items():assert (ROOT/p).read_bytes().decode('utf8').lstrip('\ufeff')==raw.lstrip('\ufeff'),p
    for p,raw in files.items():
        dest=ROOT/p
        if p not in originals:assert not dest.exists(),p
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw.encode('utf8'))
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png');print('Berchtesgaden core installed, pending checks',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;before=load(OUT/'COMPILER_BEFORE.json');files=compiler.compile_system();changed=[]
    for p,raw in files.items():
        if raw.lstrip('\ufeff')==before['actual'][p]:continue
        assert (ROOT/p).read_text(encoding='utf-8-sig')==before['actual'][p],p
        bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf');(ROOT/p).write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'));changed.append(p)
    dump('IMPERIAL_EXPECTED.json',files);dump('IMPERIAL_FILES.json',changed);print('Imperial compiler changed',len(changed),'files',flush=True)

def validate():
    b=load(OUT/'BASELINE.json');old=b['inventory'];inv=core.qa.inventory();current=italian.runtime_hashes();files=load(OUT/'EXPECTED_TEXT.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(a!=z)
    ck('Exactly four declared AUS to BGT cells',sorted(zip(map(int,xx),map(int,yy)))==sorted(map(tuple,CELLS)) and all(int(a[y,x])==int(PARENT[1:],16) and int(z[y,x])==int(RGB[1:],16) for x,y in CELLS));ck('Native map dimensions unchanged',a.shape==z.shape==(3616,8192))
    for rgb,count in [(PARENT,304),(RGB,4)]:
        yy,xx=np.where(z==int(rgb[1:],16));ck('Connected '+rgb,len(xx)==count and len(physical.components(xx,yy))==1)
    eo=core.qa.counter(old['owners']);eo[RGB,SID,TAG]=1;ck('Only one new sovereign owner',core.qa.counter(inv['owners'])==eo)
    eg=dict(old['geometry']);eg[RGB]=SID;ck('Only one new province',inv['geometry']==eg);ck('Only one new state portion',inv['states']==sorted(old['states']+[[SID,TAG]]))
    et=dict(old['state_types']);et[SID+'|'+TAG]='incorporated_default';ck('All old state types retained',inv['state_types']==et)
    defs=core.cw.parse(files['common/country_definitions/1776_sc1_berchtesgaden.txt'])[0];ec=dict(old['countries']);ec[TAG]=core.qa.signature(defs);ck('All old country definitions retained',inv['countries']==ec)
    for field in ['pops','resolved_demographics','units','errors','duplicates']:ck('World conservation '+field,inv[field]==old[field])
    ep=core.qa.counter(old['regional_pop']);ep[SID,'AUS','south_german','DEFAULT:south_german']-=POP;ep[SID,TAG,'south_german','DEFAULT:south_german']=POP;ck('Exact 1000 German donor transfer only',core.qa.counter(inv['regional_pop'])==ep)
    pop=core.region(files['common/history/pops/00_west_europe.txt'],SID,TAG).children('create_pop')[0];ck('No invented profession or confessional split',[(n.key,n.value) for n in pop.children()]==[('culture','south_german'),('size','1000')])
    nodes=core.region(files['common/history/buildings/1776_sc1_berchtesgaden.txt'],SID,TAG).children('create_building');eb=core.qa.counter(old['buildings']);el=core.qa.counter(old['building_levels_written'])
    for n in nodes:
        eb[SID,TAG,core.qa.signature(n)]+=1;el[core.cw.scalar(n.one('building'))]+=1;ck('Public national ownership '+core.cw.scalar(n.one('building')),n.children('add_ownership')[0].children('country')[0].one('country')=='"c:BGT"')
    ck('Only two bounded buildings added',len(nodes)==2 and core.qa.counter(inv['buildings'])==eb and core.qa.counter(inv['building_levels_written'])==el)
    pms={n.key:n for n in core.cw.parse(files['common/production_methods/1776_sc1_berchtesgaden.txt'])};jobs={};types=italian.definitions('common/pop_types')
    for key,n in pms.items():
        employ=n.children('building_modifiers')[0].children('level_scaled')[0].children();jobs[key]=sum(int(e.value) for e in employ);ck('Existing professions '+key,all(e.key.removeprefix('building_employment_').removesuffix('_add') in types for e in employ));ck('No added technology requirement '+key,not n.children('unlocking_technologies'))
    ck('100 court plus 100 saline jobs below conservative workforce',sorted(jobs.values())==[100,100] and sum(jobs.values())<POP*.25)
    builds=core.cw.parse(files['common/buildings/1776_sc1_berchtesgaden.txt']);ck('Both existing institutions nonexpandable',len(builds)==2 and all(n.one('expandable')==n.one('buildable')==n.one('downsizeable')=='no' for n in builds))
    ck('Saltworks inland processing not coastal port or mining concession',builds[1].one('building_group')=='bg_light_industry' and builds[1].one('city_type')=='city')
    salt=pms['pm_aor1776_berchtesgaden_saline'].children('building_modifiers')[0].children('workforce_scaled')[0];ck('Small salt output from wood and tools',[(n.key,n.value) for n in salt.children()]==[('goods_input_wood_add','1'),('goods_input_tools_add','0.1'),('goods_output_salt_add','1')] and 'salt' in italian.definitions('common/goods'))
    ck('Existing salt resource capacities unchanged',all('resource' not in n.key for n in builds))
    ledger=load(reg.active_registry_path());m=load(OUT/'REGISTRY_MIGRATION.json');addition=next(r for r in m['updated'] if r['rgb']==RGB)
    ck('Exact additive registry 577 to 578',ledger==sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])) and len(ledger)==len({r['rgb'] for r in ledger})==578)
    ck('Exact migration previous layer',m['previous']==[r for r in b['registry'] if r['state']==SID]);ck('Current Salzburg Massa Trento Brixen Berchtesgaden tail',reg.approved_lot_dirs()[-5:]==[rm.OUT/'SC1-SALZBURG',rm.OUT/'SC4-MASSA-CARRARA',rm.OUT/'SC1-TRENTO',prior.OUT,OUT])
    ck('Physical imperial extent unchanged',np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    from map2k_patch import ELECTORS
    ck('BGT ordinary member no tenth elector or free city',TAG in reg.additional_members() and TAG not in reg.additional_free_cities() and TAG not in ELECTORS.values() and len(ELECTORS)==9)
    ck('Bounded Piedmont rights intact',reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}} and [r for r in ledger if r['beneficiary']=='SAR']==[r for r in b['registry'] if r['beneficiary']=='SAR'])
    import serg_sc1_salzburg as slz
    ck('All physical locators and their RGBs unchanged',slz.prior.pas.prior.q.r9.locators(z)==load(OUT/'LOCATORS_BEFORE.json'))
    sp='map_data/state_regions/00_west_europe.txt';oldst=next(n for n in core.cw.parse(load(OUT/'TEXT_BEFORE.json')[sp].lstrip('\ufeff')) if n.key==SID);newst=next(n for n in core.cw.parse(files[sp].lstrip('\ufeff')) if n.key==SID)
    ck('All hubs arables resources traits unchanged',[core.qa.signature(n) for n in oldst.children() if n.key!='provinces']==[core.qa.signature(n) for n in newst.children() if n.key!='provinces']);ck('Capital in owned portion, automatic point pending user',defs.one('capital')==SID and [SID,TAG] in inv['states'])
    names=files['common/scripted_effects/1776_sc1_berchtesgaden.txt'];ck('Naming scoped to BGT portion only','limit = { state_region = s:STATE_TYROL owner = { c:BGT ?= this } }' in names and 'set_hub_name = { type = city name = aor1776_hub_berchtesgaden }' in names)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))};ck('Child keeps parent terrain',terrain[PARENT.upper()]==terrain[RGB.upper()])
    import serg_sc4_ligurian_fiefs as lig
    policy=lig.initial_policy(TAG,italian.definitions('common/scripted_effects'),italian.definitions('common/laws'));dump('INITIAL_POLICY.json',policy);ck('Effective Catholic theocracy serfdom customs and no slavery',{'law_theocracy','law_state_religion','law_hereditary_bureaucrats','law_serfdom','law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery'}<=set(policy['laws'].values()))
    char=files['common/history/characters/1776_sc1_berchtesgaden.txt'];ck('Hausen starts without anticipated Schroffenberg or invented birthday','aor1776_bgt_first' in char and 'aor1776_bgt_last' in char and 'age = 60' in char and 'birth_date' not in char and 'Schroffenberg' not in char and 'ruler = yes' in char)
    ck('No automatically copied defensive pact union puppet or new army',not any(p.startswith(('common/history/treaties/','common/history/diplomacy/','common/history/military_formations/','common/combat_unit_types/')) for p in files))
    for p,raw in files.items():
        ck('Exact installed candidate '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
        if p.endswith('.txt'):
            try:core.cw.parse(raw.lstrip('\ufeff'));ok=True
            except Exception:ok=False
            ck('Syntax '+p,ok)
        if p.endswith('.yml'):ck('UTF8 BOM '+p,(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'))
    for p,raw in load(OUT/'IMPERIAL_EXPECTED.json').items():ck('Exact imperial generated file '+p,(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    for path in re.findall(r'(?:icon|texture|background) = "([^"]+)"','\n'.join(raw for p,raw in files.items() if p.startswith(('common/buildings/','common/production_methods/','common/production_method_groups/')))):ck('Existing icon '+path,(ROOT/path).is_file() or (core.qa.GAME/path).is_file())
    con=load(OUT/'CONCURRENT_BEFORE_INSTALL.json');changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));allowed=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png'}
    ck('Other functional and concurrent work preserved',set(changed)<=allowed|set(con['changes']) and all(current.get(p)==h for p,h in con['files'].items()),changed)
    proofchanges=[p for p,h in b['reports'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)];ck('All prior nested proofs and attestations unchanged',not proofchanges,proofchanges)
    tools=[p for p,h in b['tools'].items() if sha(ROOT/p)!=h];ck('Only old registry guard tool changed',tools==['tools/map2l_registry.py'],tools)
    overlaps=[]
    for d in reg.approved_lot_dirs():
        if d==OUT:continue
        for r in load(d/'GEOMETRY.json')['assignments']:
            if set(map(tuple,r.get('cells',[])))&set(map(tuple,CELLS)):overlaps.append([d.name,r['rgb'],r['owner']])
    ck('No overlap with any old approved geometry row',not overlaps,overlaps);ca=dict(zip(*np.unique(a,return_counts=True)));cz=dict(zip(*np.unique(z,return_counts=True)));ck('All old RGB counts unchanged except declared AUS parent',all(ca.get(int(rgb[1:],16))==cz.get(int(rgb[1:],16)) for rgb in old['geometry'] if rgb!=PARENT))
    ck('SLZ twelve exact cells and entire Bavarian residual unchanged',all(int(z[y,x])==int('EDBB00',16) for x in range(4385,4389) for y in range(924,927)) and int((z==int('EDBB00',16)).sum())==12 and np.array_equal(a==int('6EA29B',16),z==int('6EA29B',16)))
    for id in ['SC1-BRIXEN','SC1-TRENTO']:
        t=next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']==id);ck('Real bounded receipt '+id,t['status']=='BLOCKED' and t['installed_delivery_status']=='PASS_RUNTIME_USER_VALIDATED' and rm.partial_runtime_evidence(t))
    ck('No Berchtesgaden human receipt',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')));git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip();ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False);dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current));owned=sorted(set(changed)-set(con['changes']));dump('FILES_MODIFIED.json',dict(task_ids=[TASK],runtime_files=owned,sha256={p:current[p] for p in owned},old_tools_changed=['tools/map2l_registry.py'],concurrent_changes_preserved_not_written=con['files']));print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'],v['failed']

def tests():
    import serg_sc4_ligurian_fiefs as lig
    r=load(prior.OUT/'TEST_REVIEW.json');inherited=set(r['historical_final_layer_assertions']);obsolete=set(r['obsolete_snapshot_assertions'])|{'test_serg_sc1_brixen.BrixenContracts.test_current_cumulative_tail','test_serg_sc1_brixen.BrixenContracts.test_no_brixen_human_receipt_no_credit'}
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden']
    for label,names in [('TESTS',modules),('SCOPED_TESTS',['test_serg_sc1_berchtesgaden'])]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names));failed=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors];unknown=[f for f in failed if f['id'] not in inherited|obsolete];(OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8');dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if unknown else 'OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY' if failed else 'PASS',total=r.testsRun,passed=r.testsRun-len(failed)-len(r.skipped),failed=failed,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unknown,automated_engine_test=False));print(label,r.testsRun-len(failed)-len(r.skipped),'/',r.testsRun,'unexplained',len(unknown),flush=True);assert not unknown,unknown
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),obsolete_snapshot_assertions=sorted(obsolete),old_tests_not_modified=True,unexplained_failures=[],classification='Seven fixed-final-layer expectations plus one pre-acceptance absence-of-Brixen-receipt expectation; genuine user receipt now replaces that old lifecycle snapshot.',replacement='Current cumulative tail and genuine partial BRX receipt checked by Berchtesgaden contracts.'))

def maps_and_localization():
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][2] for r in load(OUT/'BASELINE.json')['inventory']['owners']};owners[RGB]=TAG
    x0,y0,x1,y1,s=4379,919,4399,938,25;panel=(x1-x0)*s+70;im=Image.new('RGB',(panel*2,(y1-y0)*s+140),'#faf8ef');d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    palette={'AUS':'#dbbf90','BAV':'#e4dbaa','SLZ':'#6c93aa',TAG:'#71498b'}
    for k,(arr,title) in enumerate([(a,'AVANT : noyau sous AUS'),(z,'INSTALLE B : BGT, 4 cellules')]):
        ox=k*panel;d.text((ox+10,10),title,font=f,fill='black')
        for y in range(y0,y1):
            for x in range(x0,x1):
                rgb='x'+format(int(arr[y,x]),'06X');u=ox+45+(x-x0)*s;v=53+(y-y0)*s;d.rectangle((u,v,u+s,v+s),fill=palette.get(owners.get(rgb),'#d5d5d5'),outline='#bbb')
                if arr[y,x]!=arr[y,x-1]:d.line((u,v,u,v+s),fill='#333',width=2)
                if arr[y,x]!=arr[y-1,x]:d.line((u,v,u+s,v),fill='#333',width=2)
        for x in range(x0,x1,3):d.text((ox+45+(x-x0)*s,32),str(x),font=f,fill='black')
        for y in range(y0,y1,3):d.text((ox+5,53+(y-y0)*s),str(y),font=f,fill='black')
        for label,x,y in [('SLZ : 12 cellules',4386.5,925),('BGT : residence B',4384.5,930.5),('farm natif TYROL',4395.137,928.734)]:
            u=ox+45+(x-x0)*s;v=53+(y-y0)*s;d.ellipse((u-3,v-3,u+3,v+3),fill='white',outline='black');d.text((u-60,v+8),label,font=f,fill='black',stroke_width=2,stroke_fill='white')
    d.text((10,im.height-58),'SLZ bleu / BGT violet / AUS ocre / BAV jaune. Tous les localisateurs physiques sont conserves.',font=f,fill='black');d.text((10,im.height-35),'Noyau de residence seulement ; placement de la capitale automatique a verifier en jeu.',font=f,fill='black');im.save(OUT/'BEFORE_AFTER.png')
    import localization_duplicate_audit as audit
    rows=[];sets=[]
    for lang in ['english','french']:
        p=ROOT/('localization/'+lang+'/1776_sc1_berchtesgaden_l_'+lang+'.yml');matched=[audit.KEY.match(line) for line in p.read_text('utf-8-sig').splitlines()[1:]];keys={m.group(1) for m in matched if m};sets.append(keys);mod=audit.entries(lang);van=audit.entries(lang,root=audit.VANILLA);rows.append(dict(language=lang,keys=len(keys),all_lines_parse=all(matched),duplicates={k:[str(v[0]) for v in mod[k]] for k in keys if len(mod[k])!=1},vanilla_collisions=sorted(keys&set(van)),bom=p.read_bytes().startswith(b'\xef\xbb\xbf')))
    ok=sets[0]==sets[1] and all(r['all_lines_parse'] and r['bom'] and not r['duplicates'] and not r['vanilla_collisions'] for r in rows);dump('LOCALIZATION_REVIEW.json',dict(status='PASS' if ok else 'FAIL',same_keys_both_languages=sets[0]==sets[1],checks=rows));assert ok,rows;print('Map prepared and localization PASS',flush=True)

def documentation():
    v=load(OUT/'VALIDATION.json');tests=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    oldmap=rm.OUT/'SC1-SALZBURG/EVIDENCE/REILLY_1.jpg';view=OUT/'HOMANN_1715_BROWSER_VIEW.png'
    dump('SOURCE_READING.json',dict(record_date='2026-10-24',historical_date='1776-01-01',sources=[dict(url='https://www.historisches-lexikon-bayerns.de/Lexikon/Artikel_45401',reading='Full political article and ruler table: Hausen 1768-1780, chapter election, Vogtei, salt contracts and contemporary institutions'),dict(url='https://www.historisches-lexikon-bayerns.de/Lexikon/Berchtesgaden,_F%C3%BCrstpropstei:_Territorium_und_Verwaltung',reading='Territory and administration article: neighboring sovereignties, courts, Gnotschaften and external property distinctions'),dict(url='https://www.heimatkundeverein-berchtesgaden.de/dl/48bcad340dd9b0e4f0dedc2972e8288a/',reading='Two-page PDF, second page confirms Hausen tenure; complete underlying 1986 book not read'),dict(url='https://www.oeaw.ac.at/fileadmin/subsites/Institute/VID/PDF/Publications/diverse_Publications/Historisches_Ortslexikon/Ortslexikon_Salzburg.pdf',reading='Printed pages 14-15, PDF indexes 13-14: fiscal properties and whole-principality estimates, not a 1776 town census'),dict(url='https://www.finanzamt-berchtesgaden-laufen.de/ueber-uns/geschichte',reading='Official local history: Petersberg, Frauenreuth salt activity and later developments; no nineteenth-century conduit projected into 1776')],historical_maps_actually_viewed=[dict(path=view.relative_to(ROOT).as_posix(),sha256=sha(view),source='Homann circa 1715, BSB 2 Mapp. 8-3,1#54, HLB embedded image',method='600px image actually displayed in browser, screenshot retained; not a downloaded original or a reading of full-resolution cadastral details',observed='Salzburg northeast, Reichenhall northwest, Hallein east, Schellenberg between, Berchtesgaden southwest of Salzburg, Koenigssee south'),dict(path=oldmap.relative_to(ROOT).as_posix(),sha256=sha(oldmap),source='Reilly 1791, BSB bsb00090512, reused prior evidence',method='Entire existing local 2500x1869 image visually inspected',limit='After 1776; topological corroboration only, not a dated metric boundary')],access_limits=['BSB high-resolution reader failed; no high-resolution map reading claimed','No original 1776 cadastral act transcribed','No verified exact birth date; engine age 60 is a rounded parameter'],geodetic_overlay=False,old_R4_alignment_reused=False,modern_administrative_borders_used=False,population=dict(rounded_residence=1000,uncertainty=[700,1500],exact_1776_census=False,not_population_per_pixel=True,not_whole_principality=True),visual_delivery_review=dict(path=PREFIX+'BEFORE_AFTER.png',reviewed=True,observation='Four-cell purple BGT core separate from all twelve blue SLZ cells; old physical locators remain fixed.')))
    rows=[['Markt Berchtesgaden / residence','Sovereign prince-provost and chapter, distinct from Salzbourg and religious influence','BGT xEDBF00, four-cell residence B, 1000 transferred residents','HLB political and administration articles; Homann c1715','No cadastral or full-Gnotschaften closure'],['Schellenberg / Ettenberg / Scheffau','Separate market and local jurisdictions within the territorial research perimeter','No broad alpine RGB assigned; open obligation','HLB; OeAW fiscal-property inventory','Attribution and comparable population still needed'],['Ramsau / Bischofswiesen / Gern / Au','Rural Gnotschaften and access zones not interchangeable with the Markt','Outside the four-cell certified implementation scope','HLB; OeAW','No definitive approval of current omission'],['Salzberg / Schoenau / Koenigssee','Valleys and local jurisdictions distinct from one residence point','Open attribution, not a modern district boundary','HLB; Homann; OeAW','BGT core does not represent the entire lake or southern valleys'],['Hallthurm / Reichenhall / Salzbourg','Passages and neighboring Bavarian or Salzbourg sovereignty','All SLZ twelve cells and Bavarian residual unchanged','HLB administration; Homann and Reilly topology','No transfer of underrepresented Salzbourg by default'],['External possessions / Hofmarks / Zinswaelder','Property and lower jurisdiction do not establish independent imperial sovereignty everywhere','No new distant title without dated political evidence','HLB territory and administration','External rights and border jurisdiction remain to classify'],['Habsburg protection / Bavarian salt contracts','Hereditary Vogtei and salt sales distinct from annexation or generic military pact','No copied AUS pact, BAV union, vassality or all-goods treaty','HLB political history; official Finanzamt history','1776 obligations require separate native-mechanism assessment; 1795 excluded'],['Petersberg / Frauenreuth','Existing salt activity before 1776','One small inland saline, 100 technical jobs; no coastal port or new large mine','HLB; official Finanzamt history','No certified historical tonnage or workforce'],['Brixen / Trento / other approved cores','Real user receipts limited to installed cores','All retained; their regions remain blocked','Existing receipts and cumulative geometry','No regional credit and Tyrol dependencies remain unsatisfied']]
    with (OUT/'JURISDICTION_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['jurisdiction','historical_distinction_1776','implementation','source','limit']);w.writerows(rows)
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['rgb','state','previous_owner','owner','cells_before','cells_after','category'])
        for r in load(OUT/'GEOMETRY.json')['assignments']:w.writerow([r['rgb'],r['state'],r['previous_owner'],r['owner'],308 if r['rgb']==PARENT else 0,r['pixels'],r['confidence']])
    sub=dict(id='BG-I-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',tag=TAG,state=SID,category='B',cells=CELLS,new_rgb=RGB,previous_owner='AUS',population_transferred=POP,scope='Four-cell prince-provost residence only: Hausen, Catholic theocracy, 100-job court and 100-job inland saline, bounded imperial rights; automatic capital point and actual economic operation pending player test. Not the whole principality or peripheral jurisdictions.')
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',regional_status='BLOCKED',sub_lots=[sub],independently_testable_components=[dict(id='BG-T-CORE',test='Four cells, 1000-person transfer, automatic capital and neighbors'),dict(id='BG-I-COURT',test='Hausen, prince-provost title, theocracy, laws and 100-job public chancery'),dict(id='BG-E-SALT',test='100-job inland saline, wood/tools inputs, salt output, funding and market access'),dict(id='BG-P-IMPERIAL',test='Bounded imperial rights, nine electors, no copied protection pact or political union')],no_runtime_attestation=True,regional_cadastral_closure=False,points_awarded=0,political_approximation='B'))
    report=f'''**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# SC1-BERCHTESGADEN — BG-I-CORE installé, région bloquée

**82/235 = 34,89 % avant et après**, 24 tâches qualifiées sur 81. Périmètre 1.0.0, poids et qualifications antérieures inchangés. Aucun point régional attribué pour un noyau partiel.

## Reçu précédent et sélection

Le vrai reçu utilisateur **BR-I-CORE PASS_RUNTIME_USER_VALIDATED** est enregistré, limité aux neuf cellules et aux vérifications expressément rapportées dans la mission jointe : nouvelle partie 1776, capitale Brixen intérieure, Leopold, théocratie catholique, 3000 habitants, chancellerie 200 postes, pacte AUS–BRX, droits impériaux, voisins, un mois, sauvegarde et rechargement sans anomalie. Pas de date effective de test, capture ou mesure supplémentaire inventée. Acceptation **9/9**, **111/111 empreintes** de livraison intactes. SC1-BRIXEN reste **BLOCKED P1** avec ses cinq obligations inchangées ; zéro point. L'événement additif SERG-RM-0031 conserve les trente précédents.

Après cette réception, le validateur PASS sélectionne **SC1-BERCHTESGADEN P1**, dépendance SC1-SALZBURG satisfaite. C'est l'unique nouvelle tâche de cette passe. Trente et Brixen restent régionalement bloqués ; SC2-TYROL conserve ses dépendances non closes.

## Recherche au 1er janvier 1776

La principauté temporelle et les juridictions propres sont distinguées du diocèse, des possessions foncières et de la protection. **Franz Anton Josef von Hausen-Gleichenstorff**, prince-prévôt 1768–1780, est le souverain retenu, sans anticipation de Schroffenberg. L'élection capitulaire et la Vogtei habsbourgeoise ne valent pas annexion autrichienne ; les ventes de sel à la Bavière ne valent pas union politique. Le contrat de 1795, les annexions du XIXe siècle et les installations de 1816/1817 sont exclus. Voir SOURCES.md, les deux articles HLB, le PDF du Heimatkundeverein et la notice officielle du Finanzamt ; SOURCE_READING.json borne les lectures réellement réalisées.

Homann vers 1715 a été effectivement affiché dans sa version de consultation de 600 pixels, dont une capture est conservée. Le lecteur BSB haute résolution a échoué : aucune précision cadastrale issue de cet original n'est prétendue. Reilly 1791, déjà conservé dans les preuves Salzbourg, a été relu intégralement comme corroboration topologique postérieure. Les cartes placent la résidence au sud-ouest de Salzbourg et distinguent Reichenhall, Hallein et Schellenberg. Aucun vieux recalage R4, frontière contemporaine ou point de ville isolé ne justifie l'annexion d'un grand RGB. JURISDICTION_MATRIX.csv distingue les ressorts ; B_PROPOSAL.md compare A (territoire complet différé), B (résidence retenue) et C (correction partielle).

## Installation territoriale et démographique

**BG-I-CORE : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. TAG libre **BGT**, nouveau RGB **xEDBF00**, cellules **{CELLS}**. Quatre cellules **AUS→BGT**, parent xAB7EB0 **308→304**, demeurant connecté. Portion technique STATE_TYROL, sans revendication d'appartenance historique tyrolienne. Les douze cellules **SLZ xEDBB00** et les 53 cellules du résidu bavarois **x6EA29B** restent intégralement inchangées. Aucun RGB voisin, ancien hub, localisateur, ressource, arable ou référence de ville n'est déplacé. Le noyau ne reconstitue pas le voisinage complet de la principauté presque entourée par Salzbourg.

**1000 habitants existants** transférés depuis AUS/STATE_TYROL : **454812→453812**, south_german **349084→348084**, alémaniques **105728 conservés**. Population mondiale **834926252**, cultures et confessions globales inchangées ; aucune profession inventée. Estimation arrondie de résidence B, incertitude 700–1500, pas recensement de 1776. Les 97 propriétés fiscales du Markt parmi 957 en 1698 et les estimations de 9000/10000 pour la principauté à d'autres dates ne sont pas converties mécaniquement en population de cette portion.

## Institutions, capitale et économie

Prince-prévôt de Hausen, théocratie catholique, servage et lois impériales ; âge moteur arrondi **60 ans**, sans date de naissance certifiée. L'élection capitulaire reste abstraite par le modèle viager. La capitale nationale appartient à la portion BGT ; une action enfant nomme seulement cette portion et son city **Berchtesgaden**. **Le placement automatique effectif de la capitale reste à vérifier en jeu.** Aucun nouveau localisateur physique n'est présenté comme acquis.

Une **chancellerie publique non extensible de 100 postes**, et une **petite saline intérieure de Frauenreuth non extensible de 100 postes**, à propriété nationale. À plein emploi, paramètres techniques bois 1 et outils 0,1 → sel 1 ; bien sel et icônes existants. Capacité totale 200 postes, sous l'hypothèse prudente de 250 actifs pour 1000 habitants ; ni effectifs réels de 1776 ni tonnage certifié. La préparation de saumure et la cuisson sont regroupées. Aucune technologie ajoutée, grande mine, port côtier, industrie démesurée, nouvelle armée ou fortification. Recrutement, approvisionnement, financement et accès au marché doivent être observés par le joueur.

Registre impérial **577→578**, tous les anciens titres conservés et emprise physique identique, **neuf électeurs** ; BGT membre ordinaire, sans ville libre. Aucun pacte AUS copié de Trente/Brixen, aucune vassalité ou union personnelle BAV/SLZ. Protection, passages et contrats de sel restent à qualifier séparément. L'emblème moteur aux clefs est une évocation, pas un fac-similé de bannière datée.

## Contrôles réels et conservation

**{v['passed']}/{v['total']} contrôles statiques PASS**. **{tests['passed']}/{tests['total']} tests cumulatifs réussis**, **{len(tests['failed'])} échecs classés** : sept attentes figées de dernière couche, plus l'ancienne attente d'absence de reçu Brixen, devenue obsolète après votre véritable attestation. **{len(tests['skipped'])} test ignoré hérité** ; aucun échec inexpliqué. Les anciens tests sont conservés. **{scoped['passed']}/{scoped['total']} tests ciblés PASS**, dont refus d'absorption SLZ, de mauvais parent BAV, d'un titre sur tout le parent AUS, de ville libre, d'extension d'emprise et de certificat cadastral. Les contrats finaux du suivi sont exécutés après actualisation ; résultats exacts dans FINAL_TESTS.json et FINAL_CHECKS.json. Les 18 clés françaises et anglaises sont appariées, avec BOM, sans doublon ni collision vanilla. BEFORE_AFTER.png a été inspecté visuellement.

Les **36 fichiers fonctionnels livrés** sont déclarés dans FILES_MODIFIED.json. Avant installation, aucune nouvelle modification fonctionnelle concurrente depuis l'entrée ; toutes celles déjà présentes sont conservées. Aucun retour depuis une ancienne baseline. Les anciennes preuves imbriquées, reçus, tests et noyaux restent identiques ; seul l'ancien outil map2l_registry.py reçoit un garde strict additionnel après Brixen, sans affaiblissement des précédents. Fortifications/génie, France, Anzin, Saint-Gobain, drainage, États-Unis/Minutemen et accords franco-américains sont protégés par conservation des octets hors périmètre. HEAD, branche main et index conservés ; aucune opération Git d'écriture ni modification vanilla. Les quatre blancs de fin de ligne hérités sont classés séparément, sans nettoyage concurrent.

## Blocages et prochaine action

**SC1-BERCHTESGADEN reste BLOCKED P1**, sans clôture régionale ou validation humaine nouvelle. Gnotschaften périphériques, Schellenberg, Ramsau/Bischofswiesen/Gern/Au, Salzberg/Schönau/Königssee, accès de Hallthurm, droits extérieurs, démographie comparable et qualification des obligations de protection/sel/passages restent ouverts. La représentation actuelle de ces omissions n'est pas approuvée définitivement. Les blocages antérieurs, notamment Innviertel/SC2-AUSTRIA, Teschen, Trente, Brixen et Italie, sont conservés.

**Prochaine action : votre protocole BG-I-CORE**, PLAYER_TEST_PROTOCOL.md : nouvelle partie 1776, capitale, souverain, population, chancellerie/saline et sel, finances, droits et relations, SLZ/voisins, un mois, sauvegarde/rechargement. Aucun moteur exécuté par l'agent, aucun reçu humain BGT créé. Après test et nouvelle autorisation, candidate indépendante recalculée **SC1-PASSAU-OUTLIERS P1**, identifiée seulement ; elle reste NOT_STARTED. Aucune deuxième tâche commencée.
'''
    (OUT/'REPORT.md').write_text(report,encoding='utf8');print('Research, implementation, report and matrices documented',flush=True)

def tracking():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');assert s==b['roadmap']
    assert load(OUT/'VALIDATION.json')['status']=='PASS' and not load(OUT/'TESTS.json')['unexplained_failures'] and load(OUT/'SCOPED_TESTS.json')['status']=='PASS'
    assert rm.progress(s)['next_task']==TASK;t=next(t for t in s['tasks'] if t['id']==TASK)
    reason=('Seul le noyau de résidence BG-I-CORE est installé. Gnotschaften périphériques et juridiction de Schellenberg, Ramsau/Bischofswiesen/Gern/Au, Salzberg/Schönau/Königssee, accès de Hallthurm et possessions extérieures exigent attribution politique datée et démographie comparable. '
        'Protection habsbourgeoise, contrats bavarois de sel et passages restent à qualifier sans pacte générique automatique ; droits fonciers et souveraineté ne sont pas confondus. Le noyau B ne clôture pas ces obligations et leur omission actuelle n’est pas approuvée définitivement.')
    note=('BG-I-CORE, TAG BGT, quatre cellules xEDBF00 depuis AUS xAB7EB0 308→304 ; 1000 habitants transférés, monde conservé. '
        'Franz Anton Josef von Hausen-Gleichenstorff, prince-prévôt catholique ; chancellerie et saline intérieure de 100 postes chacune, capacités techniques. '
        'Capitalisation et noms limités à la portion BGT ; placement automatique et fonctionnement économique à tester. Aucun pacte copié, aucune armée nouvelle. '
        'SLZ douze cellules et résidu bavarois intacts ; registre 577→578, même emprise, neuf électeurs. Seul BG-I-CORE IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; région BLOCKED P1, zéro point, aucun reçu humain BGT.')
    obligations=[('BG-SCHELLENBERG','Schellenberg market jurisdiction, Ettenberg and Scheffau; dated boundaries and comparable population'),('BG-RURAL-WEST','Ramsau, Bischofswiesen, Gern, Au and rural Gnotschaften beyond the residence'),('BG-SOUTH','Salzberg, Schoenau and Koenigssee; no whole southern valley assigned from a single town'),('BG-BORDERS','Hallthurm and passages; neighboring Bavarian and Salzbourg sovereignty, no borrowing from SLZ'),('BG-EXTERNAL','External possessions, Hofmarks and Zinswaelder: property and lower jurisdiction versus temporal imperial sovereignty'),('BG-OBLIGATIONS','Habsburg protection, Bavarian salt contracts and passages at 1776-01-01; native mechanism and demographic/economic limits')]
    t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=load(OUT/'IMPLEMENTATION.json')['sub_lots'],installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md',PREFIX+'B_PROPOSAL.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope='BG-I-CORE only: four-cell residence B, 1000 transferred residents, Hausen, 100-job court and 100-job inland saline, automatic capital and bounded imperial rights. Not whole principality, peripheral Gnotschaften or cadastral borders.',new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),blocking_reason=reason,residual_uncertainty=reason+' Succession capitulaire abstraite ; âge, emploi et production paramètres techniques ; emblème provisoire.',current_delivery_note=note,decision=None,delivered_scope=dict(classification='B_PRINCE_PROVOST_RESIDENCE_NUCLEUS',sub_lots=['BG-I-CORE'],new_tag=TAG,new_rgb=RGB,installed_cells=4,transferred_population=POP,cadastral_validation=False,full_principality_coverage=False,world_population_unchanged=True,imperial_physical_extent_unchanged=True),remaining_territorial_obligations=[dict(id=id,status='OPEN_NOT_VALIDATED',scope=scope) for id,scope in obligations],historical_perimeter=['Principauté temporelle de Berchtesgaden au 1er janvier 1776, distincte de Salzbourg et de la Bavière ; juridictions et possessions extérieures à distinguer'])
    t['historical_sources'].append(PREFIX+'SOURCES.md:1');s['mission_status']='BERCHTESGADEN_RESIDENCE_CORE_PENDING_USER_REGION_BLOCKED'
    probe=copy.deepcopy(s);probe.pop('runtime_validation_hold',None);candidate=rm.progress(probe)['next_task'];assert candidate=='SC1-PASSAU-OUTLIERS',candidate
    s['runtime_validation_hold']=dict(task_id=TASK,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,reason='Une seule nouvelle tâche exécutée ; test joueur BG-I-CORE avant toute suite autorisée.',test_summary=TEST_SUMMARY,scope_note=SCOPE_NOTE)
    s['events'].append(dict(id='SERG-RM-0032',date='2026-10-24',kind='SCOPED_PRINCE_PROVOST_IMPLEMENTATION_WITH_TERRITORIAL_BLOCK',scope_version='1.0.0',source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],sub_lot_changes=[dict(id='BG-I-CORE',before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+n for n in ['REPORT.md','VALIDATION.json','TESTS.json','PLAYER_TEST_PROTOCOL.md','IMPLEMENTATION.json']],note=note+' '+reason+' Progression 82/235=34,89 % avant/après. SC1-PASSAU-OUTLIERS identifiée seulement, sans deuxième tâche.'))
    assert s['events'][:-1]==b['roadmap']['events'];assert [x for x in s['tasks'] if x['id']!=TASK]==[x for x in b['roadmap']['tasks'] if x['id']!=TASK]
    p=rm.progress(s);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,TASK),p
    assert not rm.structural_errors(s),rm.structural_errors(s);rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged=True,previous_31_events_unchanged=True,points_awarded=0,scope_version='1.0.0',next_candidate=candidate));print('Tracker PASS; 82/235; BG-I-CORE player test pending; Passau outliers not started',flush=True)

def final_tests():
    stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_serg_closure_roadmap','test_serg_sc1_berchtesgaden']));failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
    (OUT/'FINAL_TESTS.log').write_text(stream.getvalue(),encoding='utf8');dump('FINAL_TESTS.json',dict(task_ids=[TASK],status='PASS' if not failures else 'FAIL',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],automated_engine_test=False));print('Final contracts',r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,flush=True);assert not failures,failures

def finalize():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');p=rm.progress(s);current=italian.runtime_hashes();static=load(OUT/'SESSION_AFTER_STATIC.json');owned=load(OUT/'FILES_MODIFIED.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    changes=sorted(k for k in set(current)|set(static['hashes']) if current.get(k)!=static['hashes'].get(k));ck('No runtime change since successful static validation',not changes,changes)
    ck('Exact delivered functional bytes retained',all(current.get(k)==h for k,h in owned['sha256'].items()));ck('Current history inventory unchanged since static',core.qa.inventory()==static['inventory'])
    checked=rm.check();dump('TRACKER_VALIDATION_FINAL.json',checked);ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    ck('Evidence-based progress unchanged 82/235 34.89 percent',(p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],len(s['tasks']))==(82,235,'34.89',24,81))
    ck('Only Berchtesgaden changed after accepted Brixen core',[t for t in s['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK])
    ck('Previous 31 events unchanged',s['events'][:-1]==b['roadmap']['events'] and s['events'][-1]['id']=='SERG-RM-0032')
    ck('Player Berchtesgaden next, Passau outliers not begun',p['next_task']==TASK and s['runtime_validation_hold']['next_implementation_candidate']=='SC1-PASSAU-OUTLIERS' and next(t for t in s['tasks'] if t['id']=='SC1-PASSAU-OUTLIERS')['status']=='NOT_STARTED')
    view=(rm.OUT/'NEXT_ACTION.md').read_text(encoding='utf8');ck('Next action uses actual Berchtesgaden test and scope',TEST_SUMMARY in view and SCOPE_NOTE in view)
    bg=next(t for t in s['tasks'] if t['id']==TASK);ck('BG core pending region blocked no fabricated human receipt',bg['status']=='BLOCKED' and bg['priority']=='P1' and bg['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and bg['runtime_validation']['attestation'] is None and not list(OUT.glob('RUNTIME_USER_ATTESTATION*')) and len(bg['remaining_territorial_obligations'])==6)
    for id,count in [('SC1-BRIXEN',5),('SC1-TRENTO',6)]:
        t=next(t for t in s['tasks'] if t['id']==id);ck('Real limited receipt and obligations retained '+id,t['status']=='BLOCKED' and t['installed_delivery_status']=='PASS_RUNTIME_USER_VALIDATED' and rm.partial_runtime_evidence(t) and len(t['remaining_territorial_obligations'])==count)
    ck('All previous terminal qualifications retained',rm.qualifications(s)==rm.qualifications(b['roadmap']))
    canonical={fp.relative_to(ROOT).as_posix() for fp in rm.OUT.iterdir() if fp.is_file()};oldchanges=[rel for rel,h in b['reports'].items() if rel not in canonical and (not (ROOT/rel).is_file() or sha(ROOT/rel)!=h)];ck('All previous nested proofs and receipts unchanged',not oldchanges,oldchanges)
    toolchanges=[k for k,h in b['tools'].items() if sha(ROOT/k)!=h];ck('Only old registry guard changed all old tests intact',toolchanges==['tools/map2l_registry.py'],toolchanges)
    loc=load(OUT/'LOCALIZATION_REVIEW.json');ck('Both localizations have same 18 keys no duplicate or vanilla collision',loc['status']=='PASS' and all(r['keys']==18 for r in loc['checks']))
    con=load(OUT/'CONCURRENT_BEFORE_INSTALL.json');ck('Concurrent runtime preserved since review',all(current.get(k)==h for k,h in con['files'].items()))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');ys,xs=np.where(a!=z);ck('Exactly four final changed cells',sorted(zip(xs.tolist(),ys.tolist()))==sorted(map(tuple,CELLS)))
    for id,rgb,cells in [('Salzbourg','xEDBB00',12),('Brixen','xEDBE00',9),('Trento','xEDBD00',12),('Massa','xEDBC00',8)]:ck('Old core exact '+id,int((z==int(rgb[1:],16)).sum())==cells and np.array_equal(a==int(rgb[1:],16),z==int(rgb[1:],16)))
    ck('Whole Bavarian residual retained',np.array_equal(a==int('6EA29B',16),z==int('6EA29B',16)))
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);findings=[line for line in diff.stdout.splitlines() if 'trailing whitespace.' in line];ok=len(findings)==4 and all(line.startswith('common/history/pops/00_west_europe.txt:') for line in findings) and diff.returncode==2
    dump('DIFF_CHECK.json',dict(status='INHERITED_WHITESPACE_ONLY' if ok else 'REVIEW_REQUIRED',returncode=diff.returncode,findings=findings,preexisting_findings=4,old_tabs_not_cleaned=True,stderr=diff.stderr));ck('Four inherited whitespace findings only',ok,findings)
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip();ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    tests=load(OUT/'TESTS.json');ck('Eight cumulative failures classified with no unexplained failure',not tests['unexplained_failures'] and len(tests['failed'])==8 and len(tests['skipped'])==1)
    ck('All final roadmap and current contracts pass',load(OUT/'FINAL_TESTS.json')['status']=='PASS');ck('Protocol options research maps and obligations documented',all((OUT/n).is_file() for n in ['PLAYER_TEST_PROTOCOL.md','B_PROPOSAL.md','SOURCES.md','SOURCE_READING.json','JURISDICTION_MATRIX.csv','REPORT.md','BEFORE_AFTER.png']))
    final=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False)
    dump('FINAL_CHECKS.json',final);print('Final checks',final['passed'],'/',final['total'],final['failed'],flush=True);assert not final['failed'],final['failed']
    dump('SESSION_AFTER.json',dict(hashes=current,progress=p,git_head=b['git']['head'],git_branch=b['git']['branch'],git_index_sha256=b['git']['index_sha256'],previous_proofs_checked=len(b['reports'])))
    manifest={rel:sha(ROOT/rel) for rel in owned['runtime_files']}
    for fp in list(OUT.rglob('*'))+list(prior.OUT.glob('*2026_10_23*')):
        if fp.is_file() and fp.name!='DELIVERY_MANIFEST.json':manifest[fp.relative_to(ROOT).as_posix()]=sha(fp)
    for rel in canonical|{reg.active_registry_path().relative_to(ROOT).as_posix(),'tools/serg_sc1_berchtesgaden.py','tools/test_serg_sc1_berchtesgaden.py','tools/serg_closure_accept_brixen.py','tools/map2l_registry.py'}:manifest[rel]=sha(ROOT/rel)
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK,'SC1-BRIXEN'],files=manifest,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',berchtesgaden_regional_status='BLOCKED',brixen_core_status='PASS_RUNTIME_USER_VALIDATED',brixen_regional_status='BLOCKED',concurrent_runtime_observed_not_written=con['files'],automated_engine_test=False));assert all(sha(ROOT/rel)==h for rel,h in manifest.items());print('Delivery manifest verified',len(manifest),'files; no second new task begun',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
