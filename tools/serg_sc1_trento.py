"""Guarded, independently evidenced Trento pass; no human receipt generated."""
import collections as C
import contextlib
import copy
import io
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc4_massa_carrara as prior
ROOT=prior.ROOT; rm=prior.rm; core=prior.core; reg=prior.reg; sha=prior.sha
TASK='SC1-TRENTO'; OUT=rm.OUT/TASK; PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
TAG='TRT'; RGB='xEDBD00'; PARENT='xD0BF60'; SID='STATE_SOUTH_TYROL'; POP=9000
CELLS=[[4350,973],[4350,974],[4351,972],[4351,973],[4351,974],[4352,972],[4352,973],[4352,974],[4353,972],[4353,973],[4353,974],[4354,973]]
TEST_SUMMARY='Nouvelle partie au 1er janvier 1776 : Trente (TRT), noyau B de 12 cellules, Cristoforo Sizzo de Noris, capitale, théocratie, 9 000 habitants et administration publique ; contrôler le pacte défensif AUS, les droits impériaux sans dixième électeur et la conservation des voisins/MCA/noyaux alpins. Simuler un mois, sauvegarder puis recharger ; signaler les résultats et anomalies.'
SCOPE_NOTE='TR-I-CORE couvre la seule résidence politique de Trente, pas le diocèse ou l’intégralité des vallées et possessions du principat. Les limites du pacte défensif et de la succession capitulaire sont documentées. Massa-Carrare reste BLOCKED P0 malgré la validation de MC-I-CORE ; les autres blocages régionaux demeurent. Brixen reste NOT_STARTED ; le Tyrol dépend encore des deux principautés.'
MISSION=Path('C:/Users/simeo/.codex/attachments/fa3eb65a-e925-4a80-977a-b93d2d39e32d/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def load(p):return rm.load_json(p)
def dump(n,o):rm.write_json(OUT/n,o)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    state=load(rm.OUT/'ROADMAP_STATE.json'); checked=rm.check()
    assert checked['status']=='PASS' and rm.progress(state)['next_task']==TASK
    assert state['events'][-1]['id']=='SERG-RM-0027'
    hashes=prior.italian.runtime_hashes(); inv=core.qa.inventory()
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    OUT.mkdir(exist_ok=True)
    reports={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json',dict(roadmap=state,inventory=inv,hashes=hashes,registry=load(reg.active_registry_path()),reports=reports,
        tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},
        git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=sha(ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal'))))
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    shutil.copyfile(MISSION,OUT/'USER_MISSION.txt')
    dump('ENTRY_TRACKER_VALIDATION.json',checked)
    print('Trento baseline captured after accepted MCA; 82/235, P1, dependency Salzburg satisfied',flush=True)

def survey():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(OUT/'provinces_before.png')
    targets={'STATE_SOUTH_TYROL','STATE_TYROL','STATE_VENETIA','STATE_LOMBARDY'}
    rows=[]
    for r in inv['owners']:
        rgb,sid,tag=r['key']
        if sid not in targets:continue
        yy,xx=np.where(a==int(rgb[1:],16))
        rows.append(dict(rgb=rgb,state=sid,owner=tag,cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    tags=['TRE','TRN','TRT','TNO','TRI']
    use={t:[] for t in tags}
    for folder in ['common/country_definitions','common/flag_definitions']:
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            raw=p.read_text(encoding='utf-8-sig')
            for t in tags:
                if re.search(r'\b'+t+r'\b',raw):use[t].append(str(p))
    dump('NATIVE_INVENTORY.json',dict(provinces=rows,candidate_tags=use,countries={t:inv['countries'].get(t) for t in ['AUS','SLZ','VEN']+tags},
        populations=[r for r in inv['regional_pop'] if r['key'][0] in targets],buildings=[r for r in inv['buildings'] if r['key'][0] in targets],
        units=[r for r in inv['units'] if r['key'][0] in {'AUS','VEN'}]))
    print('Candidate tags',json.dumps(use),flush=True)
    for r in rows:
        if r['state']=='STATE_SOUTH_TYROL':print(r,flush=True)
    for r in inv['regional_pop']:
        if r['key'][0]=='STATE_SOUTH_TYROL':print('population',r,flush=True)

def prepare():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png')
    assert prior.italian.runtime_hashes()==b['hashes'], 'Review concurrent changes before preparing'
    assert TAG not in b['inventory']['countries'] and RGB not in b['inventory']['geometry'] and not np.any(a==int(RGB[1:],16))
    assert not load(OUT/'NATIVE_INVENTORY.json')['candidate_tags'][TAG]
    after=a.copy()
    for x,y in CELLS:
        assert a[y,x]==int(PARENT[1:],16)
        after[y,x]=int(RGB[1:],16)
    yy,xx=np.where(after==int(PARENT[1:],16));assert len(prior.prior.components(xx,yy))==1
    rows=[]
    for rgb,tag in [(PARENT,'AUS'),(RGB,TAG)]:
        yy,xx=np.where(after==int(rgb[1:],16));points=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
        rows.append(dict(rgb=rgb,parent_rgb=PARENT,state=SID,previous_owner='AUS',owner=tag,pixels=len(points),cells=points,
            confidence='B_POLITICAL_APPROXIMATION' if tag==TAG else 'RETAINED_NOT_CERTIFIED'))
    refs=[dict(state=SID,field='city',before=PARENT,after=RGB,pixel=[4352,973])]
    geo=dict(parents=[PARENT],assignments=rows,new_provinces=[dict(rgb=RGB,parent_rgb=PARENT)],new_members=[TAG],free_cities=[],
        selected_option='TRENT_RESIDENCE_CORE',classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,
        hub_rebindings=refs)
    files={};originals={}
    def old(p):
        assert sha(ROOT/p)==b['hashes'][p]
        raw=(ROOT/p).read_bytes().decode('utf8');originals[p]=raw;return raw
    p='common/history/states/00_states.txt';raw=old(p);n=core.state(raw,SID)
    files[p]=core.edits(raw,[(n.end-1,n.end-1,'\n\t\t# SC1-TRENTO: episcopal residence core, not the diocese or all South Tyrol.\n\t\tcreate_state = { country = c:TRT owned_provinces = { xEDBD00 } }\n\t')]).replace('\t\n\t\t# SC1-TRENTO:','\n\t\t# SC1-TRENTO:')
    p='map_data/state_regions/00_west_europe.txt';raw=old(p);off=int(raw.startswith('\ufeff'))
    n=next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID);f=n.children('provinces')[0]
    frag=raw[f.start+off:f.end+off];assert frag.count('"'+PARENT+'"')==1
    files[p]=core.edits(raw,[(f.start+off,f.end+off,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    n=next(n for n in core.cw.parse(files[p].lstrip('\ufeff')) if n.key==SID);f=n.children('city')[0]
    assert core.cw.scalar(f.value)==PARENT
    files[p]=core.edits(files[p],[(f.start+off,f.end+off,'city = "'+RGB+'"')])
    p='map_data/province_terrains.txt';raw=old(p)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[p]=raw+'\n'+RGB+'="'+terrain[PARENT.upper()]+'"\n'
    p='common/history/pops/00_west_europe.txt';raw=old(p);n=core.region(raw,SID,'AUS')
    donors=[pop for pop in n.children('create_pop') if pop.one('culture')=='north_italian']
    assert len(donors)==2 and all(pop.one('religion') is None and pop.one('pop_type') is None for pop in donors)
    f=donors[0].children('size')[0];amount=int(f.value);assert amount==154000
    raw=core.edits(raw,[(f.start,f.end,'size = '+str(amount-POP))])
    files[p]=core.append(raw,SID,TAG,'\n\t\t\tcreate_pop = { culture = north_italian size = '+str(POP)+' }\n').replace('\t\n\t\tregion_state:TRT','\n\t\tregion_state:TRT')
    defs='TRT = { color = { 91 116 136 } country_type = recognized tier = principality cultures = { north_italian } religion = catholic capital = STATE_SOUTH_TYROL }\n'
    files['common/country_definitions/1776_sc1_trento.txt']=defs
    files['common/history/countries/trt - trento.txt']='''COUNTRIES = {
 c:TRT ?= {
  add_technology_researched = international_relations
  add_technology_researched = medical_degrees
  add_technology_researched = traditional_papermaking
  add_technology_researched = organized_workshops
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
    files['common/history/characters/1776_sc1_trento.txt']='CHARACTERS = { c:TRT ?= { create_character = { first_name = aor1776_trt_first last_name = aor1776_trt_last historical = yes culture = north_italian religion = rel:catholic ruler = yes birth_date = 1706.8.19 interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    files['common/government_types/00_1776_sc1_trento.txt']='gov_aor1776_trento = { transfer_of_power = dictatorial male_ruler = "aor1776_trt_ruler" female_ruler = "aor1776_trt_ruler_female" possible = { c:TRT ?= this has_law = law_type:law_theocracy } on_government_type_change = { change_to_dictatorial = yes } on_post_government_type_change = { post_change_to_dictatorial = yes } }\n'
    files['common/history/buildings/1776_sc1_trento.txt']='BUILDINGS = { s:STATE_SOUTH_TYROL = { region_state:TRT = { create_building = { building = "building_government_administration" add_ownership = { country = { country = "c:TRT" levels = 1 } } reserves = 1 activate_production_methods = { "pm_hereditary_bureaucrats" "pm_religious_bureaucrats" "pm_simple_organization" } } } } }\n'
    files['common/history/treaties/1776_sc1_trento.txt']='''TREATIES = {
 # Limited engine representation of the 1511 territorial defence bond.
 # The native pact covers both countries; it does not reproduce the fiscal
 # contributions, regional service limits or Tyrolean constitutional offices.
 create_treaty = {
  name = treaty_aor1776_landlibell_trento
  first_country = c:AUS
  second_country = c:TRT
  is_draft = no
  entered_into_force_on = 1511.6.23
  binding_period = { years = 5 }
  articles_to_create = { { article = defensive_pact } }
 }
}
'''
    files['common/coat_of_arms/coat_of_arms/1776_sc1_trento.txt']='aor1776_trento = { pattern = "pattern_solid.tga" color1 = "white" colored_emblem = { texture = "ce_eagle.dds" color1 = "black" instance = { scale = { 0.8 0.8 } } } }\n'
    files['common/flag_definitions/1776_sc1_trento.txt']='TRT = { flag_definition = { coa = aor1776_trento priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french';pairs={'TRT':'Trente' if fr else 'Trent','TRT_ADJ':'tridentin' if fr else 'Tridentine',
            'aor1776_trt_first':'Cristoforo','aor1776_trt_last':'Sizzo de Noris',
            'aor1776_trt_ruler':'Prince-évêque' if fr else 'Prince-Bishop','aor1776_trt_ruler_female':'Princesse-évêque' if fr else 'Princess-Bishop',
            'gov_aor1776_trento':'Principauté épiscopale de Trente' if fr else 'Prince-Bishopric of Trent',
            'gov_aor1776_trento_desc':('Le prince-évêque gouverne ses terres avec le conseil aulique, tandis que le chapitre et les magistrats de la ville défendent leurs prérogatives. Les liens de défense avec le Tyrol accompagnent cette autorité temporelle au sein du Saint-Empire.' if fr else 'The prince-bishop governs his lands through the aulic council, while the chapter and city magistrates defend their prerogatives. Defensive ties with Tyrol accompany this temporal authority within the Holy Roman Empire.')+r'\n\n$TRANSFER_OF_POWER_NAME_DESC$',
            'treaty_aor1776_landlibell_trento':'Accord de défense du Landlibell' if fr else 'Landlibell Defence Agreement'}
        files['localization/'+lang+'/1776_sc1_trento_l_'+lang+'.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    previous=[r for r in b['registry'] if r['state']==SID]
    assert any(r['rgb']==PARENT and r['beneficiary']=='AUS' for r in previous)
    addition=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC1-TRENTO: twelve-cell episcopal residence nucleus B; not diocesan or complete princely borders')
    migration=dict(replaced_regions=[SID],previous=previous,updated=sorted(previous+[addition],key=lambda r:r['rgb']),
        new_members=[TAG],free_cities=[],new_provinces=geo['new_provinces'],geometry='SERG_CLOSURE/'+TASK+'/GEOMETRY.json',
        region_reference_changes=refs,extent_added_cells=[],extent_removed_cells=[],country_additions={TAG:core.qa.signature(core.cw.parse(defs)[0])})
    rel=reg.active_registry_path().relative_to(ROOT).as_posix();originals[rel]=(ROOT/rel).read_text(encoding='utf-8-sig')
    assert load(ROOT/rel)==b['registry']
    files[rel]=json.dumps(sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    for p,raw in files.items():
        if p not in originals:assert not (ROOT/p).exists(),p
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration);dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(transferred=POP,donor='AUS',recipient=TAG,donor_before=491000,donor_after=482000,
        donor_north_italian_before=308000,donor_north_italian_after=299000,donor_south_german_unchanged=183000,
        culture='north_italian',religion='DEFAULT:north_italian',profession='unchanged: not declared',
        historical_basis='Carlini 2000 p.358 n.58: around 9000 residents in Trent in 1767, citing Lunelli/Dall’Armi. Rounded residence estimate for 1776, not a census or all-principality population. Garrison mention is not converted into a new unit or ethnic/professional census.'))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    print('Prepared TRT, twelve cells, 9000 transferred residents; city rebind only, Rovereto untouched',flush=True)

def compiler_before():
    import map2k_imperial_system as compiler
    # Exclude this not-yet-installed migration during the preflight; registry
    # guard is added only after this exact comparison succeeds.
    compiler.OUT=OUT;files=compiler.compile_system();actual={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in files}
    diff=[p for p,raw in files.items() if raw.lstrip('\ufeff')!=actual[p]]
    dump('COMPILER_BEFORE.json',dict(actual=actual,differences=diff));print('Compiler preflight',diff,flush=True);assert not diff

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');originals=load(OUT/'TEXT_BEFORE.json')
    reviewed=load(OUT/'CONCURRENT_BEFORE_INSTALL.json')
    assert reviewed['inventory_unchanged'] and not reviewed['overlap_with_planned_files']
    assert prior.italian.runtime_hashes()==reviewed['hashes'],'Review concurrent changes before installation'
    assert sha(ROOT/'.git/index')==b['git']['index_sha256']
    assert not load(OUT/'COMPILER_BEFORE.json')['differences']
    for p,raw in originals.items():assert (ROOT/p).read_bytes().decode('utf8').lstrip('\ufeff')==raw.lstrip('\ufeff'),p
    for p,raw in files.items():
        dest=ROOT/p
        if p not in originals:assert not dest.exists(),p
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw.encode('utf8'))
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Trento functional core installed; imperial compiler update next',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;before=load(OUT/'COMPILER_BEFORE.json');files=compiler.compile_system();changed=[]
    for p,raw in files.items():
        if raw.lstrip('\ufeff')==before['actual'][p]:continue
        assert (ROOT/p).read_text(encoding='utf-8-sig')==before['actual'][p],p
        bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf')
        (ROOT/p).write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'));changed.append(p)
    dump('IMPERIAL_EXPECTED.json',files);dump('IMPERIAL_FILES.json',changed);print('Imperial files updated',len(changed),flush=True)

def validate():
    b=load(OUT/'BASELINE.json');old=b['inventory'];inv=core.qa.inventory();current=prior.italian.runtime_hashes()
    files=load(OUT/'EXPECTED_TEXT.json');imperial=load(OUT/'IMPERIAL_EXPECTED.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(a!=z)
    ck('Exactly twelve declared raster cells changed',sorted(zip(map(int,xx),map(int,yy)))==sorted(map(tuple,CELLS)))
    ck('All changed pixels AUS parent to new TRT color',all(int(a[y,x])==int(PARENT[1:],16) and int(z[y,x])==int(RGB[1:],16) for x,y in CELLS))
    ck('Native map dimensions unchanged',a.shape==z.shape==(3616,8192))
    for rgb,count in [(PARENT,291),(RGB,12)]:
        yy,xx=np.where(z==int(rgb[1:],16));ck('Connected '+rgb,len(xx)==count and len(prior.prior.components(xx,yy))==1)
    eo=core.qa.counter(old['owners']);eo[RGB,SID,TAG]=1
    ck('Only declared new sovereign owner',core.qa.counter(inv['owners'])==eo)
    eg=dict(old['geometry']);eg[RGB]=SID;ck('Only one new province in South Tyrol',inv['geometry']==eg)
    ck('One new incorporated split state',inv['states']==sorted(old['states']+[[SID,TAG]]))
    et=dict(old['state_types']);et[SID+'|'+TAG]='incorporated_default';ck('All old state types retained',inv['state_types']==et)
    defs=core.cw.parse(files['common/country_definitions/1776_sc1_trento.txt'])[0];ec=dict(old['countries']);ec[TAG]=core.qa.signature(defs)
    ck('All old country definitions retained',inv['countries']==ec)
    for field in ['pops','resolved_demographics','units','errors','duplicates']:
        ck('World conservation '+field,inv[field]==old[field])
    ep=core.qa.counter(old['regional_pop']);ep[SID,'AUS','north_italian','DEFAULT:north_italian']-=POP;ep[SID,TAG,'north_italian','DEFAULT:north_italian']=POP
    ck('Exact 9000 population transfer only',core.qa.counter(inv['regional_pop'])==ep)
    popnode=core.region(files['common/history/pops/00_west_europe.txt'],SID,TAG).children('create_pop')[0]
    ck('No invented religion or profession fields',[(n.key,n.value) for n in popnode.children()]==[('culture','north_italian'),('size','9000')])
    admin=core.region(files['common/history/buildings/1776_sc1_trento.txt'],SID,TAG).children('create_building')[0]
    eb=core.qa.counter(old['buildings']);eb[SID,TAG,core.qa.signature(admin)]+=1
    ck('All old buildings and economic ownership retained',core.qa.counter(inv['buildings'])==eb)
    el=core.qa.counter(old['building_levels_written']);el['building_government_administration']+=1
    ck('Only one explicit public court level added',core.qa.counter(inv['building_levels_written'])==el)
    ck('Episcopal court nationally owned',admin.children('add_ownership')[0].children('country')[0].one('country')=='"c:TRT"')
    ledger=load(reg.active_registry_path());migration=load(OUT/'REGISTRY_MIGRATION.json')
    addition=next(r for r in migration['updated'] if r['rgb']==RGB)
    want=sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    ck('Exact additive registry 575 to 576',ledger==want and len(ledger)==len({r['rgb'] for r in ledger})==576)
    ck('Migration exact input',migration['previous']==[r for r in b['registry'] if r['state']==SID])
    ck('Current cumulative Salzburg Massa Trento tail',reg.approved_lot_dirs()[-3:]==[rm.OUT/'SC1-SALZBURG',prior.OUT,OUT])
    ck('Physical imperial extent identical',np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    from map2k_patch import ELECTORS
    ck('TRT member not free city or tenth elector',TAG in reg.additional_members() and TAG not in reg.additional_free_cities() and TAG not in ELECTORS.values() and len(ELECTORS)==9)
    ck('Nine SAR Piedmont rights retained',reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}} and [r for r in ledger if r['beneficiary']=='SAR']==[r for r in b['registry'] if r['beneficiary']=='SAR'])
    import serg_sc1_salzburg as slz
    loc_before=load(OUT/'LOCATORS_BEFORE.json');loc_after=slz.prior.pas.prior.q.r9.locators(z)
    loc_want=copy.deepcopy(loc_before)
    changed_loc=[]
    for r in loc_want:
        if r['Kind']=='city' and r['ID']==56:
            assert [int(r['X']),int(r['Y'])]==[4352,973]
            r['RGB']=RGB;changed_loc.append(r)
    ck('Only Trento city RGB rebound; every physical locator unchanged',len(changed_loc)==1 and loc_want==loc_after)
    ck('Rovereto farm remains AUS parent',all(r['RGB']==PARENT for r in loc_after if r['ID']==56 and r['Kind']=='farm'))
    stp='map_data/state_regions/00_west_europe.txt'
    oldst=next(n for n in core.cw.parse(load(OUT/'TEXT_BEFORE.json')[stp].lstrip('\ufeff')) if n.key==SID)
    newst=next(n for n in core.cw.parse(files[stp].lstrip('\ufeff')) if n.key==SID)
    ck('Regional arables resources traits and other hubs retained',[core.qa.signature(n) for n in oldst.children() if n.key not in {'provinces','city'}]==[core.qa.signature(n) for n in newst.children() if n.key not in {'provinces','city'}])
    ck('Trento capital owns actual city reference',defs.one('capital')==SID and core.cw.scalar(newst.one('city'))==RGB and int(z[973,4352])==int(RGB[1:],16))
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))}
    ck('Child retains parent terrain',terrain[PARENT.upper()]==terrain[RGB.upper()])
    laws=prior.italian.definitions('common/laws');effects=prior.italian.definitions('common/scripted_effects')
    import serg_sc4_ligurian_fiefs as lig
    policy=lig.initial_policy(TAG,effects,laws);dump('INITIAL_POLICY.json',policy)
    ck('Theocracy effective at start',policy['laws']['lawgroup_governance_principles']=='law_theocracy')
    ck('State Catholic religion and inherited bureaucracy',{'law_state_religion','law_hereditary_bureaucrats'}<=set(policy['laws'].values()))
    ck('Imperial no slavery and customs active',{'law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery'}<=set(policy['laws'].values()))
    pmdefs=prior.italian.definitions('common/production_methods');active=set(policy['laws'].values())
    for name in ['pm_simple_organization','pm_hereditary_bureaucrats','pm_religious_bureaucrats']:
        pm=pmdefs[name];unlock=set(core.values(pm,'unlocking_laws'));deny=set(core.values(pm,'disallowing_laws'));tech=set(core.values(pm,'unlocking_technologies'))
        ck('Court method available '+name,(not unlock or bool(unlock&active)) and not deny&active and tech<=set(policy['technologies']))
    char=files['common/history/characters/1776_sc1_trento.txt']
    ck('Sizzo born 1706-08-19 starts, no anticipated Thun',all(s in char for s in ['aor1776_trt_first','aor1776_trt_last','birth_date = 1706.8.19','ruler = yes','ig_devout','rel:catholic']) and 'Thun' not in char)
    chars=prior.italian.definitions('common/ideologies')
    ck('Ruler ideology exists','ideology_traditionalist' in chars)
    pact=files['common/history/treaties/1776_sc1_trento.txt']
    ck('Explicit AUS TRT defensive pact, no puppet or personal union',all(s in pact for s in ['first_country = c:AUS','second_country = c:TRT','1511.6.23','article = defensive_pact']) and 'puppet' not in pact and 'personal_union' not in pact)
    ck('Defensive pact technology available','international_relations' in policy['technologies'])
    ck('No new army regiment or fort copied',not any(p.startswith('common/history/military_formations/') or p.startswith('common/combat_unit_types/') for p in files))
    for p,raw in files.items():
        ck('Exact installed candidate '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
        if p.endswith('.txt'):
            try:core.cw.parse(raw.lstrip('\ufeff'));ok=True
            except Exception:ok=False
            ck('Syntax '+p,ok)
    for p,raw in imperial.items():ck('Exact generated imperial file '+p,(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    allowed=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png'}
    concurrent=load(OUT/'CONCURRENT_BEFORE_INSTALL.json')
    ck('Other functional files and concurrent work preserved',set(changed)<=allowed|set(concurrent['changes']) and all(current.get(p)==h for p,h in concurrent['files'].items()),changed)
    proofchanges=[p for p,h in b['reports'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and (not (ROOT/p).exists() or sha(ROOT/p)!=h)]
    ck('All previous nested proofs and receipts unchanged',not proofchanges,proofchanges)
    toolchanges=[p for p,h in b['tools'].items() if sha(ROOT/p)!=h]
    observed=load(OUT/'CONCURRENT_TOOLS.json')
    ck('Only registry guard changed by this pass; concurrent icon audit retained',set(toolchanges)=={'tools/map2l_registry.py'}|set(observed['files']) and all(sha(ROOT/p)==h for p,h in observed['files'].items()),toolchanges)
    # All earlier geometry rows, including the newly human-tested MCA core.
    olddirs=[d for d in reg.approved_lot_dirs() if d!=OUT];protected=[];overlaps=[]
    for d in olddirs:
        g=load(d/'GEOMETRY.json')
        for r in g['assignments']:
            if 'cells' not in r:continue
            intersection=set(map(tuple,r['cells']))&set(map(tuple,CELLS))
            if intersection:overlaps.append(dict(lot=d.name,rgb=r['rgb'],cells=sorted(intersection)))
            protected.append(dict(lot=d.name,rgb=r['rgb'],owner=r['owner'],pixels=r['pixels']))
    ck('No previous approved geometry overlaps new core',not overlaps,overlaps)
    ca=dict(zip(*np.unique(a,return_counts=True)));cz=dict(zip(*np.unique(z,return_counts=True)))
    ck('Every old province RGB cell count unchanged except declared parent',all(ca.get(int(rgb[1:],16))==cz.get(int(rgb[1:],16)) for rgb in old['geometry'] if rgb!=PARENT))
    dump('PROTECTED_CORE_CHECK.json',dict(rows=protected,old_geometry_rows=len(protected),overlaps=overlaps,only_changed_pixels=CELLS))
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    for p in [p for p in files if p.endswith('.yml')]:ck('Localization UTF8 BOM '+p,(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'))
    ck('No fictitious human Trento receipt',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks']:
        if t['id'] in ['SC2-ANTERIOR-AUSTRIA','SC4-EXISTING-ITALIAN-STATES','SC4-SAVOY-NICE','SC4-LIGURIAN-FIEFS','SC4-MASSA-CARRARA']:
            ck('Previous bounded receipt '+t['id'],t['status']=='BLOCKED' and rm.partial_runtime_evidence(t))
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False)
    dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current))
    owned=sorted(set(changed)-set(concurrent['changes']))
    dump('FILES_MODIFIED.json',dict(task_ids=[TASK],runtime_files=owned,sha256={p:current[p] for p in owned},old_tools_changed=['tools/map2l_registry.py'],concurrent_tools_preserved_not_written=observed['files'],concurrent_changes_preserved_not_written=concurrent['files']))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'],v['failed']

def maps():
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png')
    b=load(OUT/'BASELINE.json');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners[RGB]=TAG
    x0,y0,x1,y1,s=4340,963,4368,986,22;panel=(x1-x0)*s+70
    im=Image.new('RGB',(2*panel,(y1-y0)*s+130),'#faf8ef');d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for k,(arr,title) in enumerate([(a,'AVANT : residence sous AUS'),(z,'INSTALLE B : TRT, 12 cellules')]):
        ox=k*panel;d.text((ox+10,10),title,font=f,fill='black')
        for y in range(y0,y1):
            for x in range(x0,x1):
                rgb='x'+format(int(arr[y,x]),'06X');u=ox+45+(x-x0)*s;v=55+(y-y0)*s
                d.rectangle((u,v,u+s,v+s),fill='#5b7488' if rgb==RGB else '#dcbd87' if owners.get(rgb)=='AUS' else '#d9dfb6',outline='#aaa')
                if arr[y,x]!=arr[y,x-1]:d.line((u,v,u,v+s),fill='#222',width=2)
                if arr[y,x]!=arr[y-1,x]:d.line((u,v,u+s,v),fill='#222',width=2)
        for x in range(x0,x1,3):d.text((ox+45+(x-x0)*s,35),str(x),font=f,fill='black')
        for y in range(y0,y1,3):d.text((ox+5,55+(y-y0)*s),str(y),font=f,fill='black')
        for label,x,y in [('Trente : city',4352.081055,973.937744),('Rovereto : farm',4347.677734,981.100586)]:
            u=ox+45+(x-x0)*s;v=55+(y-y0)*s;d.ellipse((u-4,v-4,u+4,v+4),fill='white',outline='black');d.text((u+6,v-14),label,font=f,fill='black',stroke_width=2,stroke_fill='white')
    d.text((10,im.height-55),'TRT bleu / AUS ocre. Coordonnees des localisateurs inchangées ; seul city est relie au RGB enfant.',font=f,fill='black')
    d.text((10,im.height-32),'Noyau politique de residence. Aucun transfert de Rovereto ni certification des vallees peripheriques.',font=f,fill='black')
    im.save(OUT/'BEFORE_AFTER.png')

def documentation():
    source=ROOT/'docs/reports/map/MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/lombardy_1750.jpg'
    dump('SOURCE_READING.json',dict(date='2026-10-23',historical_date='1776-01-01',
        historical_map_actually_viewed=dict(path=source.relative_to(ROOT).as_posix(),sha256=sha(source),detail=PREFIX+'ROBERT_1750_TRENTO_DETAIL.png',geodetic_overlay=False,cadastral_boundary_read=False),
        archival_inventories_read=True,original_medieval_or_1776_acts_transcribed=False,
        population_source=dict(url='https://heyjoe.fbk.eu/index.php/stusto/article/download/4097/4098',page=358,note=58,read='PDF text page index 13, not successful screenshot',basis_year=1767,rounded_residence_population=9000),
        bishop_birth_source_access='FBK Q49-A p138 indexed passage; complete PDF exceeds web reader size',
        old_R4_alignment_reused=False,modern_administrative_borders_used=False))
    import csv
    rows=[['Trente résidence','Temporalité épiscopale impériale distincte','TRT xEDBD00, 12 cellules B','ASTn Antichi regimi ; Robert 1750','Noyau seul, pas tout diocèse'],
        ['Rovereto / Quattro Vicariati','Juridictions du comté habsbourgeois du Tyrol','AUS, parent xD0BF60 résiduel ; farm conservé','ASTn ; Istituzioni dell’autonomia','Pas de frontière village par village certifiée'],
        ['Bolzano / Merano','Voisinage tyrolien et droits historiques composites','xD040E0 / x039D0F AUS inchangés','Robert 1750 ; inventaire natif','Brixen et droits périphériques non traités'],
        ['Valsugana orientale / Primiero','Dépendances temporelles tyroliennes ; diocèses distincts','Aucun transfert des franges orientales','Istituzioni dell’autonomia ; SAN100900','Pas de projection diocésaine de 1785'],
        ['Val di Non / Sole / Giudicarie','Droits épiscopaux et juridictions féodales à distinguer des enclaves tyroliennes','Aucune extension installée hors résidence','Robert 1750 ; ASTn inventaires juridictionnels','Cartographie juridictionnelle détaillée et démographie requises avant extension'],
        ['Riva / Ledro / Pergine / Fiemme','Ressorts et autonomies propres, spirituel et temporel à séparer','Parent et x1120FF inchangés','Inventaires ASTn ; synthèse provinciale','Aucune annexion intégrale de vallée'],
        ['Brixen / Salzbourg / Tyrol','Principautés et comté distincts au sein du Saint-Empire','Noyau SLZ protégé ; Brixen NOT_STARTED ; Tyrol dépendant','Suivi canonique et reçus','Aucune seconde tâche commencée'],
        ['Venise / Garda','Possessions vénitiennes distinctes des récupérations impériales anciennes','Tous RGB VEN conservés','Robert 1750 ; ancienne réparation MAP2B','Frontières contemporaines ou XIXe siècle exclues']]
    with (OUT/'JURISDICTION_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['jurisdiction','historical_distinction_1776','implementation','source','limit']);w.writerows(rows)
    geo=load(OUT/'GEOMETRY.json')
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['rgb','state','previous_owner','owner','cells_after','category'])
        for r in geo['assignments']:w.writerow([r['rgb'],r['state'],r['previous_owner'],r['owner'],r['pixels'],r['confidence']])
    sub=dict(id='TR-I-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',tag=TAG,state=SID,category='B',
        cells=CELLS,new_rgb=RGB,previous_owner='AUS',population_transferred=POP,
        scope='Episcopal residence nucleus only, Sizzo at 1776-01-01, theocratic court, Trento city hub, bounded imperial title and defensive Tyrolean bond; not entire principality or diocese.')
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',sub_lots=[sub],
        independently_testable_components=[dict(id='TR-T-CORE',test='12 cells, Trento hub, 9000 transfer and neighbors'),dict(id='TR-I-COURT',test='Sizzo, theocracy, laws and single public court'),dict(id='TR-P-DEFENCE',test='imperial rights and AUS defensive pact')],
        no_runtime_attestation=True,regional_cadastral_closure=False,points_awarded=0,political_approximation='B'))
    v=load(OUT/'VALIDATION.json');t=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    report=f'''**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# SC1-TRENTO — noyau politique épiscopal

**82/235 = 34,89 % avant/après**, 81 tâches et périmètre 1.0.0 inchangés. MC-I-CORE est désormais PASS_RUNTIME_USER_VALIDATED selon la confirmation explicite du joueur, limitée aux huit cellules Massa et au protocole livré ; Massa-Carrare reste BLOCKED P0, sans point régional. Rapport et preuves d’origine conservés.

Une seule nouvelle tâche exécutée : **SC1-TRENTO P1**, dépendance Salzbourg satisfaite et sélection confirmée par le validateur après enregistrement du reçu. Brixen et Tyrol ne sont pas commencés. Les sources distinguent le fief temporel impérial, le diocèse et les possessions tyroliennes ; Sizzo règne au 1er janvier 1776, Thun n’est pas anticipé. Carte Robert 1750 intégrale et détail lus ; voir SOURCES.md, SOURCE_READING.json et JURISDICTION_MATRIX.csv.

**TR-I-CORE : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. TAG libre **TRT**, nouveau **xEDBD00**, **12 cellules AUS→TRT**, parent **xD0BF60 303→291** connecté. Trois autres RGB AUS du Sud-Tyrol intacts. Capitale dans la portion TRT, référence city liée à la cellule native de Trente [4352,973] sans déplacement physique. Rovereto conserve son farm et son RGB ; Merano/Bolzano, Venise, Salzbourg et tous les noyaux validés sont préservés.

**9 000 habitants transférés** depuis les nord-italiens AUS existants ; portion AUS **491000→482000**, nord-italiens **308000→299000**, sud-allemands **183000 inchangés** ; TRT 9000. Ordre de grandeur de résidence documenté en 1767, pas recensement exact de 1776 ou total du principat. Population mondiale et composition déclarée conservées ; aucun métier ni effectif militaire inventé.

**Cristoforo Sizzo de Noris**, né le 19 août 1706, prince-évêque catholique, loi théocratique ; un niveau public national pour la chancellerie et le conseil aulique, méthodes compatibles. Le transfert de pouvoir dictatorial du moteur ne reproduit pas intégralement la procédure capitulaire. Aucun ancien bâtiment, investisseur, unité ou fort déplacé ; aucun bonus à l’Autriche ne remplace la souveraineté restituée.

**Pacte défensif AUS–TRT**, représentation B du lien du Landlibell du 23 juin 1511 : pas de marionnette, union personnelle ou annexion. L’article natif s’applique aux pays entiers et ne simule pas les seules obligations régionales, steore et offices historiques ; cette limite est documentée et incluse au contrôle en jeu. **575→576 droits impériaux**, emprise physique identique ; TRT membre, sans ville libre ni dixième électeur. Les 575 titres antérieurs et les droits piémontais restent inchangés.

La résidence est une **approximation politique B**, pas la restitution complète des vallées Non/Sole, Giudicarie, Riva/Ledro, Pergine, Fiemme ou des possessions périphériques. Une extension requiert carte juridictionnelle détaillée antérieure à 1776 et démographie comparable ; ni diocèse, ni limite moderne, ni transfert intégral de SOUTH_TYROL. B_PROPOSAL.md compare A, B et C sans recycler les calages rejetés.

Contrôles exécutés : **{v['passed']}/{v['total']} statiques**, **{t['passed']}/{t['total']} tests cumulatifs**, **{scoped['passed']}/{scoped['total']} ciblés**. Les quatre anciennes assertions de dernière couche sont préservées et classées ; une cinquième assertion Massa devient obsolète après Trente. Nouveau contrôle cumulatif Salzbourg→Massa→Trente et tests négatifs courants ; aucun échec inexpliqué. Aucune exécution du moteur, aucun reçu humain Trente. Le protocole nouveau départ 1776, institutions, défense, droits, conservations, un mois, sauvegarde/rechargement est dans PLAYER_TEST_PROTOCOL.md.

Les modifications concurrentes de drainage apparues avant installation ont été contrôlées et conservées ; les historiques du monde étaient inchangés. Les travaux Anzin/infrastructures, fortifications/génie, France et États-Unis présents à l’entrée sont conservés. Voir CONCURRENT_BEFORE_INSTALL.json, FILES_MODIFIED.json et les contrôles finaux. Aucun Git écrit, aucun vanilla modifié.

**Prochaine action : votre test de TR-I-CORE**. Candidate suivante indépendante : **SC1-BRIXEN P1**, identifiée seulement. Les blocages Massa, Piombino, Ligurie, Savoie/Nice, Italie, Autriche antérieure, Innviertel et Teschen restent distincts et inchangés. Aucun second chantier lancé.
'''
    (OUT/'REPORT.md').write_text(report,encoding='utf8')

def tests():
    import unittest
    import serg_sc4_ligurian_fiefs as lig
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    superseded=set(load(prior.OUT/'TEST_REVIEW.json')['new_obsolete_snapshot_assertions'])|{'test_serg_sc4_massa_carrara.MassaCarraraContracts.test_current_chain_retains_salzburg_before_massa'}
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento']
    for label,names in [('TESTS',modules),('SCOPED_TESTS',['test_serg_sc1_trento'])]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
        unexplained=[f for f in failures if f['id'] not in inherited|superseded]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if unexplained else 'OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY' if failures else 'PASS',
            total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,'unexplained',len(unexplained),flush=True)
        assert not unexplained,[(f['id'],f['traceback']) for f in unexplained]
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),obsolete_snapshot_assertions=sorted(superseded),old_tests_not_modified=True,unexplained_failures=[],replacement='Current Salzburg -> Massa -> Trento tail verified by VALIDATION.json and test_serg_sc1_trento; old fixed-tail assertions retained.'))

def tracking():
    b=load(OUT/'BASELINE.json');state=load(rm.OUT/'ROADMAP_STATE.json');assert state==b['roadmap']
    v=load(OUT/'VALIDATION.json');tested=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert v['status']=='PASS' and not tested['unexplained_failures'] and scoped['status']=='PASS'
    assert rm.progress(state)['next_task']==TASK
    t=next(t for t in state['tasks'] if t['id']==TASK)
    uncertainty=('Noyau de résidence B de 12 cellules uniquement ; pas certification des limites intégrales, du diocèse, des vallées ou de la population totale du principat. '
        'Défense commune traduite par un pacte natif couvrant les pays entiers ; contributions régionales et procédure capitulaire non intégralement simulées. '
        'Toute extension requiert cartographie juridictionnelle détaillée et démographie correspondante, sans déplacer Brixen, Tyrol ou noyaux approuvés.')
    note=('Trente : noyau B installé, TRT, 12 cellules AUS vers xEDBD00, parent xD0BF60 303→291 ; 9000 habitants transférés et total mondial conservé. '
        'Sizzo de Noris au 1er janvier 1776, théocratie, capitale sur le point urbain natif conservé, une administration publique et pacte défensif AUS. '
        'Registre 575→576 sans extension physique ni dixième électeur. Sous-composantes territoire/population, institutions et défense indépendamment vérifiables. '
        'Anciennes preuves et travaux concurrents conservés. Livraison TR-I-CORE IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION, aucun reçu humain ou point. '
        'Limites périphériques, abstraction de défense et succession capitulaire explicitées ; Brixen et Tyrol non commencés.')
    t.update(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        installed_sub_lots=load(OUT/'IMPLEMENTATION.json')['sub_lots'],installed_lots=['SERG_CLOSURE/'+TASK],
        implementation_report=[PREFIX+'REPORT.md',PREFIX+'B_PROPOSAL.md'],
        static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope='TR-I-CORE only: twelve-cell residence B, 9000 transferred residents, Sizzo, court, Trento capital, imperial rights and defensive bond. Not whole principality or diocese.',new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),
        residual_uncertainty=uncertainty,current_delivery_note=note,decision=None,
        delivered_scope=dict(classification='B_EPISCOPAL_RESIDENCE_NUCLEUS',sub_lots=['TR-I-CORE'],new_tag=TAG,new_rgb=RGB,installed_cells=12,transferred_population=POP,cadastral_validation=False,full_principality_coverage=False,world_population_unchanged=True,imperial_physical_extent_unchanged=True))
    t['historical_sources'].append(PREFIX+'SOURCES.md:1')
    state['mission_status']='TRENTO_RESIDENCE_CORE_AWAITING_RUNTIME_USER_VALIDATION'
    state['runtime_validation_hold']=dict(task_id=TASK,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate='SC1-BRIXEN',reason='Une seule tâche exécutée ; test joueur du noyau Trente avant toute suite autorisée.',test_summary=TEST_SUMMARY,scope_note=SCOPE_NOTE)
    state['events'].append(dict(id='SERG-RM-0028',date='2026-10-23',kind='SCOPED_EPISCOPAL_IMPLEMENTATION',scope_version='1.0.0',
        source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],
        sub_lot_changes=[dict(id='TR-I-CORE',before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],
        before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',
        evidence=[PREFIX+n for n in ['REPORT.md','VALIDATION.json','TESTS.json','PLAYER_TEST_PROTOCOL.md','IMPLEMENTATION.json']],note=note+' Progression 82/235=34,89 % avant/après. Prochaine action : test joueur ; SC1-BRIXEN P1 identifiée sans commencement. Aucun Git ou vanilla écrit.'))
    assert state['events'][:-1]==b['roadmap']['events']
    assert [x for x in state['tasks'] if x['id']!=TASK]==[x for x in b['roadmap']['tasks'] if x['id']!=TASK]
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,TASK),p
    probe=copy.deepcopy(state);probe.pop('runtime_validation_hold');next(x for x in probe['tasks'] if x['id']==TASK)['status']='BLOCKED'
    candidate=rm.progress(probe)['next_task'];assert candidate=='SC1-BRIXEN',candidate
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged=True,previous_27_events_unchanged=True,points_awarded=0,scope_version='1.0.0',next_candidate=candidate))
    print('Tracker PASS; 82/235=34.89%; player Trento next, Brixen identified only',flush=True)

def final_tests():
    import unittest
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_serg_closure_roadmap','test_serg_sc1_trento']))
    # No report is written while the read-only validator contracts are running.
    failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
    (OUT/'FINAL_TESTS.log').write_text(stream.getvalue(),encoding='utf8')
    dump('FINAL_TESTS.json',dict(task_ids=[TASK],status='PASS' if not failures else 'FAIL',total=result.testsRun,
        passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,
        skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],automated_engine_test=False))
    print('Final tracker/current contracts',result.testsRun-len(failures)-len(result.skipped),'/',result.testsRun,flush=True)
    assert not failures,failures

def finalize():
    b=load(OUT/'BASELINE.json');state=load(rm.OUT/'ROADMAP_STATE.json');p=rm.progress(state)
    current=prior.italian.runtime_hashes();static=load(OUT/'SESSION_AFTER_STATIC.json');owned=load(OUT/'FILES_MODIFIED.json')
    checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    later=sorted(k for k in set(current)|set(static['hashes']) if current.get(k)!=static['hashes'].get(k))
    ck('Runtime unchanged since successful static validation',not later,later)
    ck('Owned runtime files retain exact delivered bytes',all(current.get(k)==h for k,h in owned['sha256'].items()))
    ck('Current history inventory unchanged since static validation',core.qa.inventory()==static['inventory'])
    checked=rm.check();dump('TRACKER_VALIDATION_FINAL.json',checked)
    ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    ck('Evidence-based progression remains 82/235', (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],len(state['tasks']))==(82,235,'34.89',24,81))
    ck('Only Trento task changed after accepted Massa receipt',[t for t in state['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK])
    ck('Earlier 27 events preserved',state['events'][:-1]==b['roadmap']['events'] and state['events'][-1]['id']=='SERG-RM-0028')
    ck('Trento pending user and Brixen not started',p['next_task']==TASK and state['runtime_validation_hold']['next_implementation_candidate']=='SC1-BRIXEN' and next(t for t in state['tasks'] if t['id']=='SC1-BRIXEN')['status']=='NOT_STARTED')
    nextview=(rm.OUT/'NEXT_ACTION.md').read_text(encoding='utf8')
    ck('Next action names the actual Trento protocol',TEST_SUMMARY in nextview and SCOPE_NOTE in nextview and 'Colloredo' not in nextview)
    trento=next(t for t in state['tasks'] if t['id']==TASK)
    ck('No fictitious Trento validation',trento['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and trento['runtime_validation']['attestation'] is None and not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    mca=next(t for t in state['tasks'] if t['id']=='SC4-MASSA-CARRARA')
    ck('Massa core human validated but region BLOCKED P0',mca['status']=='BLOCKED' and mca['priority']=='P0' and mca['installed_delivery_status']=='PASS_RUNTIME_USER_VALIDATED' and rm.partial_runtime_evidence(mca))
    ck('All accepted task qualifications retained',rm.qualifications(state)==rm.qualifications(b['roadmap']))
    canonical={f.relative_to(ROOT).as_posix() for f in rm.OUT.iterdir() if f.is_file()}
    oldchanges=[rel for rel,h in b['reports'].items() if rel not in canonical and (not (ROOT/rel).is_file() or sha(ROOT/rel)!=h)]
    ck('All old nested evidence and receipts unchanged',not oldchanges,oldchanges)
    concurrent=load(OUT/'CONCURRENT_BEFORE_INSTALL.json')
    ck('Concurrent drainage files unchanged since review',all(current.get(k)==h for k,h in concurrent['files'].items()))
    tools=load(OUT/'CONCURRENT_TOOLS.json')
    ck('Concurrent icon audit unchanged since review',all(sha(ROOT/k)==h for k,h in tools['files'].items()))
    older_tool_changes=[k for k,h in b['tools'].items() if sha(ROOT/k)!=h]
    ck('Old tests unchanged and only declared tools differ',set(older_tool_changes)=={'tools/map2l_registry.py'}|set(tools['files']),older_tool_changes)
    before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    ys,xs=np.where(before!=after)
    ck('Exactly twelve final changed cells',sorted(zip(xs.tolist(),ys.tolist()))==sorted(map(tuple,CELLS)))
    ck('MCA eight cells remain exact original RGB',all(int(after[y,x])==int(prior.RGB[1:],16) for x,y in prior.CELLS) and int((after==int(prior.RGB[1:],16)).sum())==8)
    ck('Nine electors and bounded new member',len(__import__('map2k_patch').ELECTORS)==9 and TAG not in __import__('map2k_patch').ELECTORS.values() and TAG not in reg.additional_free_cities())
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True)
    findings=[s for s in diff.stdout.splitlines() if 'trailing whitespace.' in s]
    diffok=len(findings)==4 and all(s.startswith('common/history/pops/00_west_europe.txt:') for s in findings) and diff.returncode==2
    dump('DIFF_CHECK.json',dict(status='INHERITED_WHITESPACE_ONLY' if diffok else 'REVIEW_REQUIRED',returncode=diff.returncode,findings=findings,
        preexisting_findings=4,line_numbers_shifted_by_new_population_block=True,old_tabs_not_cleaned=True,stderr=diff.stderr))
    ck('No new whitespace finding beyond four inherited tabs',diffok,findings)
    git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    ck('All cumulative failures explicitly classified',not load(OUT/'TESTS.json')['unexplained_failures'] and len(load(OUT/'TESTS.json')['failed'])==5)
    ck('All final tracker and current guards pass',load(OUT/'FINAL_TESTS.json')['status']=='PASS')
    ck('Player protocol and options documented',all((OUT/n).is_file() for n in ['PLAYER_TEST_PROTOCOL.md','B_PROPOSAL.md','SOURCES.md','JURISDICTION_MATRIX.csv','REPORT.md']))
    final=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False)
    dump('FINAL_CHECKS.json',final)
    print('Final',final['passed'],'/',final['total'],final['failed'],flush=True)
    assert not final['failed'],final['failed']
    dump('SESSION_AFTER.json',dict(hashes=current,progress=p,git_head=b['git']['head'],git_branch=b['git']['branch'],git_index_sha256=b['git']['index_sha256'],previous_proofs_checked=len(b['reports'])))
    manifest={rel:sha(ROOT/rel) for rel in owned['runtime_files']}
    for fp in list(OUT.rglob('*'))+list(prior.OUT.glob('*2026_10_23*')):
        if fp.is_file() and fp.name!='DELIVERY_MANIFEST.json':manifest[fp.relative_to(ROOT).as_posix()]=sha(fp)
    for rel in canonical|{reg.active_registry_path().relative_to(ROOT).as_posix(),'tools/serg_sc1_trento.py','tools/test_serg_sc1_trento.py','tools/serg_closure_accept_massa_carrara.py','tools/map2l_registry.py'}:
        manifest[rel]=sha(ROOT/rel)
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK,'SC4-MASSA-CARRARA'],files=manifest,
        installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',massa_core_status='PASS_RUNTIME_USER_VALIDATED',massa_regional_status='BLOCKED',
        concurrent_runtime_observed_not_written=concurrent['files'],concurrent_tools_observed_not_written=tools['files'],automated_engine_test=False))
    assert all(sha(ROOT/rel)==h for rel,h in manifest.items())
    print('Delivery manifest verified',len(manifest),'files; no further task begun',flush=True)

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
