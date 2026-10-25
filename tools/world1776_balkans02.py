"""BALKANS-02. Local, guarded Ragusan restoration; --apply once, --validate thereafter.

Historical border tracing is an approximation on the existing coarse coastline.
It is not an exact cadastral reconstruction or a native-game validation.
"""
from pathlib import Path
from collections import Counter
import argparse, json, re, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import audit_anzin_regional_infrastructure as a
import audit_starting_tech_1776 as tech
import map_1776_audit as geo
from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized

ROOT=a.ROOT
OUT=ROOT/'docs/reports/map/WORLD_1776_CLOSURE'
LOT=OUT/'BALKANS-02'
SID='STATE_DALMATIA'
ST='common/history/states/00_states.txt'
POP='common/history/pops/01_south_europe.txt'
BLD='common/history/buildings/01_south_europe.txt'
REG='map_data/state_regions/01_south_europe.txt'
BMP='map_data/provinces.png'
TER='map_data/province_terrains.txt'
EDIT=[ST,POP,BLD,REG,BMP,TER]
COLORS={'RAG':'xE8D201','NEUM':'xE8D202','SUTORINA':'xE8D203'}
TECHS='commercial_insurance_markets distillation enclosed_dock_systems improved_husbandry international_relations medical_degrees organized_textile_production periodical_print_networks regulated_small_arms scientific_fortification_siegecraft scientific_naval_architecture state_dockyard_systems centralization traditional_food_processing organized_workshops traditional_papermaking organized_financial_institutions organized_military_establishments institutionalized_scientific_exchange'.split()

def dump(name,obj):
    (LOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def node(t,key):
    hits=[n for n in walk(parse(t)) if n.key==key]
    assert len(hits)==1,(key,len(hits))
    return hits[0]

def replace(t,ops):
    for lo,hi,s in sorted(ops,reverse=True):t=t[:lo]+s+t[hi:]
    return t

def rgb(key):return tuple(bytes.fromhex(key[1:]))

def masks(arr):
    """Pixel trace reviewed against Carter map 2 and Marinkovic p17.

    Existing sea/land and all non-x11A0E0 pixels remain immutable.
    Peljesac is merged with the mainland in the source bitmap; Korcula's
    western body, Hvar and Vis remain Venetian. Lastovo has no source land.
    """
    yy,xx=np.indices(arr.shape[:2]);base=np.all(arr==rgb('x11A0E0'),axis=2)
    peninsula=(xx>=4490)&(xx<=4503)&(yy>=1061)&(yy<=1064)
    mainland=(xx>=4504)&(yy>=1063)
    mljet=(xx>=4491)&(xx<=4500)&(yy>=1065)&(yy<=1068)
    rag=base&(peninsula|mainland|mljet)
    neum=np.zeros(base.shape,dtype=bool)
    for x,y in [(4504,1061),(4504,1062),(4505,1062),(4503,1062),(4503,1063),(4502,1063),(4502,1064)]:neum[y,x]=True
    sut=np.zeros(base.shape,dtype=bool)
    for x,y in [(4515,1070),(4515,1071),(4515,1072),(4514,1073),(4515,1073),(4516,1073)]:sut[y,x]=True
    assert np.all(base[neum]) and np.all(base[sut])
    rag&=~(neum|sut)
    return {'RAG':rag,'NEUM':neum,'SUTORINA':sut}

def new_files():
    files={}
    def add(folder,text):files[folder+'/1776_world_b02_ragusa.txt']=text.strip()+'\n'
    add('common/country_definitions','''RAG = {
 color = { 157 49 55 }
 country_type = recognized
 tier = city_state
 cultures = { croat }
 capital = STATE_DALMATIA
}''')
    laws='presidential_republic oligarchy state_religion land_based_taxation hereditary_bureaucrats religious_schools no_colonial_affairs no_health_system local_police peasant_levies merchant_navy tenant_farmers migration_controls slavery_banned merchant_banking'.split()
    add('common/history/countries','COUNTRIES = { c:RAG ?= {\n'+''.join(' add_technology_researched = '+x+'\n' for x in TECHS)+
        ' effect_starting_politics_reactionary = yes\n'+''.join(' activate_law = law_type:law_'+x+'\n' for x in laws)+' set_tax_level = medium\n} }')
    # Do not assign an unverified historical person to the January rectorship.
    add('common/history/characters','''# Procedural placeholder: monthly rector for 1776-01 has not been identified.
# The birth date is a generation parameter, not a historical assertion.
CHARACTERS = { c:RAG ?= { create_character = {
 historical = no culture = croat religion = rel:catholic ruler = yes
 birth_date = 1726.1.1 interest_group = ig_landowners ideology = ideology_traditionalist
} } }''')
    add('common/government_types','''gov_aor1776_ragusan_republic = {
 transfer_of_power = presidential_elective
 new_leader_on_reform_government = no
 male_ruler = "aor1776_rag_recteur" female_ruler = "aor1776_rag_rectrice"
 possible = { c:RAG ?= this has_law = law_type:law_presidential_republic has_law = law_type:law_oligarchy }
 on_government_type_change = { change_to_presidential_elective = yes }
 on_post_government_type_change = { post_change_to_presidential_elective = yes }
}''')
    subject=a.raw(ROOT/'common/subject_types/1776_imperial_reforms.txt')
    subject=subject.replace('subject_type_aor1776_hre_protectorate','subject_type_aor1776_ragusan_tribute').replace('aor1776_hre_protectorate','aor1776_ragusan_tribute')
    subject=re.sub(r'lower_autonomy_subject_type_alternatives\s*=\s*\{[^}]*\}','lower_autonomy_subject_type_alternatives = {}',subject)
    subject=subject.replace('can_offer_to_become_in_sway_offers = yes','can_offer_to_become_in_sway_offers = no')
    # Serialize an independent copy; never modify the SERG template.
    add('common/subject_types',subject)
    add('common/diplomatic_actions','''# Budget abstraction of the triennial tribute, not a ducat/sterling conversion.
aor1776_ragusan_tribute = {
 groups = { general power_bloc }
 texture = "gfx/interface/icons/diplomatic_action_icons/tributary_15.dds"
 show_in_lens = no potential = { always = no }
 pact = {
  cost = 0 has_junior_participant = yes subject_type = subject_type_aor1776_ragusan_tribute
  income_transfer = 0.05 second_country_gets_income_transfer = no
  income_transfer_based_on_second_country = yes
  actor_can_break = { always = yes } target_can_break = { always = yes }
 }
 ai = { will_break = { always = no } will_propose = { always = no } }
}''')
    add('common/history/diplomacy','''DIPLOMACY = { c:TUR ?= {
 create_diplomatic_pact = { country = c:RAG type = aor1776_ragusan_tribute }
 create_diplomatic_pact = { country = c:RAG type = grant_own_market }
} }''')
    add('common/buildings','''# Existing small republican administration, not a new scalable building.
building_aor1776_ragusan_chancery = {
 building_group = bg_bureaucracy city_type = city levels_per_mesh = 50
 expandable = no buildable = no downsizeable = no
 potential = { state_region = s:STATE_DALMATIA owner = { c:RAG ?= this } }
 production_method_groups = { pmg_aor1776_ragusan_chancery }
 icon = "gfx/interface/icons/building_icons/building_government_administration.dds"
 required_construction = construction_cost_very_low
 background = "gfx/interface/icons/building_icons/backgrounds/building_panel_bg_monuments.dds"
}''')
    add('common/production_method_groups','''pmg_aor1776_ragusan_chancery = { production_methods = { pm_aor1776_ragusan_chancery } }''')
    add('common/production_methods','''# 200 jobs is a capacity abstraction, not an archival headcount.
pm_aor1776_ragusan_chancery = {
 texture = "gfx/interface/icons/production_method_icons/simple_organization.dds"
 country_modifiers = { workforce_scaled = { country_bureaucracy_add = 2 } }
 state_modifiers = { workforce_scaled = { state_tax_capacity_add = 1 } }
 building_modifiers = {
  workforce_scaled = { goods_input_paper_add = 1 }
  level_scaled = {
   building_employment_clerks_add = 50 building_employment_bureaucrats_add = 75
   building_employment_clergymen_add = 50 building_employment_aristocrats_add = 25
  }
 }
}''')
    add('common/history/buildings','''BUILDINGS = { s:STATE_DALMATIA = { region_state:RAG = {
 # One existing Dalmatian fishing level is reassigned; Venetian levels 3 -> 2.
 create_building = {
  building = "building_fishing_wharf"
  add_ownership = { building = { type = "building_fishing_wharf" country = "c:RAG" levels = 1 region = "STATE_DALMATIA" } }
  reserves = 1 activate_production_methods = { "pm_simple_fishing" "pm_unrefrigerated" }
 }
 # Independent harbour; the Venetian Zadar port is preserved.
 create_building = { building = "building_port"
  add_ownership = { country = { country = "c:RAG" levels = 1 } }
  reserves = 1 activate_production_methods = { "pm_basic_port" }
 }
 create_building = { building = "building_aor1776_ragusan_chancery"
  add_ownership = { country = { country = "c:RAG" levels = 1 } }
  reserves = 1 activate_production_methods = { "pm_aor1776_ragusan_chancery" }
 }
} } }''')
    # Armorial flag: historical silver/red bars, not an asserted St Blaise ensign.
    add('common/coat_of_arms/coat_of_arms','''aor1776_ragusan_arms = {
 pattern = "pattern_solid.tga" color1 = "white"
 colored_emblem = { texture = "ce_stripes_08.dds" color1 = "red" color2 = "white" instance = { scale = { 1 1 } } }
}''')
    add('common/flag_definitions','''RAG = { flag_definition = { coa = aor1776_ragusan_arms priority = 100 allow_overlord_canton = no } }''')
    loc={
      'french':{
       'RAG':'Raguse','RAG_ADJ':'ragusaine','RAG_ADJ_MS':'ragusain','RAG_ADJ_FS':'ragusaine','RAG_ADJ_MP':'ragusains','RAG_ADJ_FP':'ragusaines',
       'gov_aor1776_ragusan_republic':'République patricienne de Raguse',
       'gov_aor1776_ragusan_republic_desc':'Les familles patriciennes réunies au Grand Conseil élisent les magistrats de la République. Le Sénat conduit les affaires et le recteur représente la cité.',
       'aor1776_rag_recteur':'Recteur','aor1776_rag_rectrice':'Rectrice',
       'subject_type_aor1776_ragusan_tribute':'République tributaire',
       'subject_type_aor1776_ragusan_tribute_desc':'Une république tributaire conserve son gouvernement, sa diplomatie et son marché. Elle ne participe pas automatiquement aux guerres de son suzerain.',
       'aor1776_ragusan_tribute':'Tribut de Raguse',
       'aor1776_ragusan_tribute_desc':'Raguse verse 5 % de ses revenus à la Porte et conserve sa neutralité, son gouvernement et son marché.',
       'building_aor1776_ragusan_chancery':'Chancellerie de la République',
       'pmg_aor1776_ragusan_chancery':'Administration de la République',
       'pm_aor1776_ragusan_chancery':'Offices du Grand Conseil'},
      'english':{
       'RAG':'Ragusa','RAG_ADJ':'Ragusan','gov_aor1776_ragusan_republic':'Patrician Republic of Ragusa',
       'gov_aor1776_ragusan_republic_desc':'The patrician families assembled in the Major Council elect the Republic’s magistrates. The Senate conducts its affairs and the rector represents the city.',
       'aor1776_rag_recteur':'Rector','aor1776_rag_rectrice':'Rector',
       'subject_type_aor1776_ragusan_tribute':'Tributary Republic',
       'subject_type_aor1776_ragusan_tribute_desc':'A tributary republic retains its government, diplomacy and market. It does not automatically join its overlord’s wars.',
       'aor1776_ragusan_tribute':'Ragusan Tribute',
       'aor1776_ragusan_tribute_desc':'Ragusa pays 5% of its income to the Porte while retaining its neutrality, government and market.',
       'building_aor1776_ragusan_chancery':'Republican Chancery',
       'pmg_aor1776_ragusan_chancery':'Republican Administration',
       'pm_aor1776_ragusan_chancery':'Offices of the Major Council'}}
    for lang,data in loc.items():
        files[f'localization/{lang}/1776_world_b02_ragusa_l_{lang}.yml']='l_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in data.items())
    return files

def transformations(old):
    result=dict(old)
    # New RGBs remain in the existing state region; no hub/locator is moved.
    n=node(old[REG],SID);p=n.children('provinces')[0]
    result[REG]=replace(old[REG],[(p.end-1,p.end-1,' '+' '.join('"'+v+'"' for v in COLORS.values())+' ')])
    n=node(old[ST],'s:'+SID)
    insertion='\n\t\tcreate_state = { country = c:RAG owned_provinces = { '+COLORS['RAG']+' } }\n\t\tcreate_state = { country = c:TUR owned_provinces = { '+COLORS['NEUM']+' '+COLORS['SUTORINA']+' } }\n'
    result[ST]=replace(old[ST],[(n.end-1,n.end-1,insertion)])
    n=node(old[POP],'s:'+SID);v=n.children('region_state:VEN')[0]
    p=next(x for x in v.children('create_pop') if x.one('culture')=='croat').children('size')[0]
    assert p.value=='297796'
    sub=old[POP][p.start:p.end];sub=sub.replace('297796','267796')
    insertion='\n\t\tregion_state:RAG = { create_pop = { culture = croat size = 30000 } }\n'
    result[POP]=replace(old[POP],[(p.start,p.end,sub),(n.end-1,n.end-1,insertion)])
    n=node(old[BLD],'s:'+SID)
    b=next(x for x in walk([n]) if x.key=='create_building' and scalar(x.one('building'))=='building_fishing_wharf')
    lev=next(x for x in walk([b]) if x.key=='levels');assert lev.value=='3'
    result[BLD]=replace(old[BLD],[(lev.start,lev.end,old[BLD][lev.start:lev.end].replace('3','2'))])
    assert all(v not in old[TER] for v in COLORS.values())
    terrain=scalar(node(old[TER],'x11A0E0').value)
    result[TER]=old[TER].rstrip()+'\n# BALKANS-02: terrain inherited from the split Dalmatian parent.\n'+''.join(k+'="'+terrain+'"\n' for k in COLORS.values())
    return result

def inv():
    owners,pairs,odd=geo.own_inventory(ROOT,a.GAME);pop=[];total=0
    for path in tech.effective('common/history/pops'):
        for n in walk(parse(a.raw(path))):
            if n.key=='create_pop':total+=int(n.one('size'))
            if n.key=='s:'+SID:pop.append(normalized([n]))
    return {'owners':{k:[list(x) for x in v] for k,v in owners.items()},'world_population':total,'pop_dalmatia':pop,'odd':odd,'git':a.git_state()}

def apply():
    assert not (LOT/'BASELINE.json').exists(),'Patch already captured: use --validate.'
    news=new_files();assert all(not (ROOT/r).exists() for r in news)
    for folder in ['common/country_definitions','common/history/countries','common/flag_definitions']:
        assert 'RAG' not in a.catalog(folder),folder
    old={r:a.raw(ROOT/r) for r in EDIT if r!=BMP};result=transformations(old)
    arr=np.array(Image.open(ROOT/BMP).convert('RGB'));ms=masks(arr)
    packed=(arr[:,:,0].astype(np.uint32)<<16)|(arr[:,:,1].astype(np.uint32)<<8)|arr[:,:,2]
    unique=set(map(int,np.unique(packed)))
    assert all(int(c[1:],16) not in unique for c in COLORS.values())
    baseline={'owned':{r:a.sha(ROOT/r) for r in EDIT},'new':list(news),'protected':{},'serg':{},'before':inv()}
    for folder in ['common','events','localization','map_data','gfx']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():
                r=p.relative_to(ROOT).as_posix()
                if r not in EDIT:baseline['protected'][r]=a.sha(p)
    for p in (ROOT/'docs/reports/map/SERG_CLOSURE').rglob('*'):
        if p.is_file():baseline['serg'][p.relative_to(ROOT).as_posix()]=a.sha(p)
    for r in EDIT:
        p=LOT/'patch_inputs'/r;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,p)
    dump('BASELINE.json',baseline)
    # Refuse to write if any shared input changed while preparing the patch.
    assert all(a.sha(ROOT/r)==h for r,h in baseline['owned'].items())
    for r,t in result.items():
        p=ROOT/r;bom=b'\xef\xbb\xbf' if p.read_bytes().startswith(b'\xef\xbb\xbf') else b''
        p.write_bytes(bom+t.encode('utf8'))
    pixels={}
    for key,mask in ms.items():
        arr[mask]=rgb(COLORS[key]);ys,xs=np.where(mask)
        pixels[key]={'rgb':COLORS[key],'count':int(mask.sum()),'pixels':list(map(list,zip(map(int,xs),map(int,ys))))}
    Image.fromarray(arr).save(ROOT/BMP)
    for r,t in news.items():
        p=ROOT/r;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8-sig' if r.endswith('.yml') else 'utf8',newline='\n')
    dump('PIXEL_PATCH.json',pixels);dump('AFTER.json',inv())
    dump('FILES_MODIFIED.json',[{'file':r,'before':baseline['owned'].get(r),'after':a.sha(ROOT/r)} for r in EDIT+list(news)])
    print('Applied local Ragusan restoration:',{k:v['count'] for k,v in pixels.items()})

def validate():
    baseline=json.loads((LOT/'BASELINE.json').read_text(encoding='utf8'));checks=[]
    def check(k,v,detail=None):checks.append({'check':k,'passed':bool(v),'detail':detail})
    expected=transformations({r:a.raw(LOT/'patch_inputs'/r) for r in EDIT if r!=BMP})
    news=new_files();after=inv()
    for r,t in {**expected,**news}.items():
        check('exact_scoped_text.'+r,a.raw(ROOT/r)==t)
        if r.endswith('.txt'):check('parse.'+r,bool(parse(t)))
    before=np.array(Image.open(LOT/'patch_inputs'/BMP).convert('RGB'));now=np.array(Image.open(ROOT/BMP).convert('RGB'))
    ms=masks(before);planned=before.copy()
    for k,m in ms.items():planned[m]=rgb(COLORS[k])
    check('bitmap_only_authorized_pixels',np.array_equal(planned,now))
    check('dimensions_mode_preserved',Image.open(ROOT/BMP).size==Image.open(LOT/'patch_inputs'/BMP).size and Image.open(ROOT/BMP).mode=='RGB')
    check('no_coastline_land_sea_change',all(np.all(before[m]==rgb('x11A0E0')) for m in ms.values()))
    changed={k for k in set(after['owners'])|set(baseline['before']['owners']) if after['owners'].get(k)!=baseline['before']['owners'].get(k)}
    check('only_three_new_ownership_keys',changed==set(COLORS.values()),sorted(changed))
    check('RAG_owner',after['owners'].get(COLORS['RAG'])==[[SID,'RAG']])
    for k in ['NEUM','SUTORINA']:check(k+'_owner',after['owners'].get(COLORS[k])==[[SID,'TUR']])
    check('world_population_conserved',after['world_population']==baseline['before']['world_population'],after['world_population'])
    check('git_unchanged',after['git']==baseline['before']['git'])
    regions=a.catalog('map_data/state_regions');members={}
    for sid,(n,p) in regions.items():
        for c in geo.values(n,'provinces'):members.setdefault(geo.prov(c),[]).append(sid)
    for c in COLORS.values():check('unique_state_membership.'+c,members.get(c)==[SID])
    terrains={n.key for n in parse(a.raw(ROOT/TER))}
    for c in COLORS.values():check('terrain.'+c,c in terrains)
    # All existing areas, subjects, countries and other lots remain byte-identical.
    external=[]
    for r,h in baseline['protected'].items():
        if not (ROOT/r).exists() or a.sha(ROOT/r)!=h:external.append(r)
    # Concurrent alloy work is independently identified by its own BEFORE hashes.
    # This accounts for its provenance; it does not validate the alloy mechanics.
    peer_path=ROOT/'docs/reports/economy/ALLOYS_1776_REBALANCE/CONCURRENT_CHANGES.json'
    peer=json.loads(peer_path.read_text(encoding='utf8')) if peer_path.exists() else {}
    accounted={r:{'before':baseline['protected'][r],'observed_now':a.sha(ROOT/r),
                  'peer_receipt':peer_path.relative_to(ROOT).as_posix(),
                  'peer_before_matches':peer.get('owned_file_hashes',{}).get(r)==baseline['protected'][r]}
               for r in external if (ROOT/r).exists()}
    # Reconstruct the separately issued technology patches when available.
    r3=ROOT/'docs/reports/technology/STARTING_TECH_AUDIT_1776_R3'
    for pf in ['ARMS_PATCHES.json','PORT_PATCHES.json','TRADE_PATCHES.json']:
        if not (r3/pf).exists():continue
        for e in json.loads((r3/pf).read_text(encoding='utf8')):
            r=e['file']
            if r not in accounted or accounted[r]['peer_before_matches']:continue
            if e.get('before_sha256')!=baseline['protected'][r] or e.get('after_sha256')!=a.sha(ROOT/r):continue
            valid=True
            if e.get('preimage') and e.get('edits'):
                p=ROOT/e['preimage'];valid=a.sha(p)==e['before_sha256'];t=a.raw(p)
                for op in sorted(e['edits'],key=lambda x:x['start'],reverse=True):
                    valid=valid and t[op['start']:op['end']]==op['old']
                    t=t[:op['start']]+op['new']+t[op['end']:]
                valid=valid and t==a.raw(ROOT/r)
            accounted[r].update(peer_receipt=(r3/pf).relative_to(ROOT).as_posix(),peer_before_matches=valid,
                                peer_after_matches=True)
    check('protected_differences_have_independent_peer_receipts',
          len(accounted)==len(external) and all(x['peer_before_matches'] for x in accounted.values()),accounted)
    serg=[r for r,h in baseline['serg'].items() if not (ROOT/r).exists() or a.sha(ROOT/r)!=h]
    check('SERG_receipts_unchanged',not serg,serg)
    check('B01_Cyclades_preserved',all(after['owners'].get(c)==[['STATE_WEST_AEGEAN_ISLANDS','TUR']] for c in ['x6090A0','x6960A0']))
    obj,_,_=tech.objects('common/technology/technologies')
    check('new_technology_ids_resolve',all(x in obj for x in TECHS))
    check('new_technology_prerequisites_closed',all(set(a.ids(obj[x],'unlocking_technologies'))<=set(TECHS) for x in TECHS))
    # Cross-references and PM legality for the three starting assets.
    methods=a.catalog('common/production_methods');groups=a.catalog('common/production_method_groups');buildings=a.catalog('common/buildings')
    for b,ps in [('building_port',['pm_basic_port']),('building_fishing_wharf',['pm_simple_fishing','pm_unrefrigerated']),('building_aor1776_ragusan_chancery',['pm_aor1776_ragusan_chancery'])]:
        bn,_=buildings[b];available=set()
        for g in a.ids(bn,'production_method_groups'):
            check('PMG_resolves.'+g,g in groups)
            if g in groups:available.update(a.ids(groups[g][0],'production_methods'))
        for pm in ps:
            check('PM_legal.'+pm,pm in methods and pm in available)
            if pm in methods:check('PM_technology.'+pm,set(a.ids(methods[pm][0],'unlocking_technologies'))<=set(TECHS))
    check('market_pact_exists','grant_own_market' in a.catalog('common/diplomatic_actions'))
    check('tribute_texture_exists',(a.GAME/'gfx/interface/icons/diplomatic_action_icons/tributary_15.dds').exists())
    check('armorial_texture_exists',(a.GAME/'gfx/coat_of_arms/colored_emblems/ce_stripes_08.dds').exists())
    check('no_automatic_wars','join_overlord_wars = no' in news['common/subject_types/1776_world_b02_ragusa.txt'])
    for lang in ['french','english']:check('loc_BOM.'+lang,(ROOT/f'localization/{lang}/1776_world_b02_ragusa_l_{lang}.yml').read_bytes().startswith(b'\xef\xbb\xbf'))
    # A passage must have a 4-neighbour link to the Ottoman hinterland and the sea.
    for name in ['NEUM','SUTORINA']:
        neighbours=set()
        for y,x in zip(*np.where(ms[name])):
            for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:neighbours.add('x%02X%02X%02X'%tuple(now[yy,xx]))
        check(name+'_joins_Ottoman_Bosnia','x9021E0' in neighbours)
        check(name+'_reaches_Adriatic','x2861CB' in neighbours)
    # Check the mainland only: the source bitmap already merges islands farther NW.
    contact=[]
    for y,x in zip(*np.where(ms['RAG'])):
        if x<4505:continue
        for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            c='x%02X%02X%02X'%tuple(now[yy,xx])
            if any(p[1]=='VEN' for p in after['owners'].get(c,[])):contact.append([int(x),int(y),c])
    check('Sutorina_separates_mainland_Ragusa_from_Cattaro',not contact,contact)
    lawkeys={k.split(':')[-1] for k in a.catalog('common/laws')}
    for law in re.findall(r'activate_law\s*=\s*law_type:(\w+)',news['common/history/countries/1776_world_b02_ragusa.txt']):
        check('law_resolves.'+law,law in lawkeys)
    check('RAG_culture_exists','croat' in a.catalog('common/cultures'))
    check('RAG_religion_exists','catholic' in a.catalog('common/religions'))
    foreign_new={}
    for folder in ['common','events','localization','map_data','gfx']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():
                r=p.relative_to(ROOT).as_posix()
                if r not in baseline['protected'] and r not in EDIT and r not in news:foreign_new[r]=a.sha(p)
    dump('CONCURRENT_CHANGES.json',{'external_gameplay':accounted,'foreign_new_files':foreign_new,'serg_proofs':serg,'external_mechanics_validated_here':False})
    result={'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','geometry_precision':'APPROXIMATION_REQUIRES_PLAYER_REVIEW','historical_rector':'UNRESOLVED_PROCEDURAL_PLACEHOLDER'}
    dump('VALIDATION.json',result);print(json.dumps({k:v for k,v in result.items() if k!='checks'}));print([x for x in checks if not x['passed']])
    return result

def render_map():
    b=json.loads((LOT/'BASELINE.json').read_text(encoding='utf8'))['before'];aft=inv()
    colors={'VEN':(96,162,207),'RAG':(175,58,66),'TUR':(194,164,105),'MON':(169,105,157),'AUS':(210,210,210)}
    canvas=Image.new('RGB',(1520,720),(23,31,40));d=ImageDraw.Draw(canvas)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    for i,(file,info,title) in enumerate([(LOT/'patch_inputs'/BMP,b,'Avant'),(ROOT/BMP,aft,'Après : Raguse et les deux passages ottomans')]):
        arr=np.array(Image.open(file).convert('RGB'))[1035:1085,4470:4540];sub=np.zeros_like(arr);sub[:]=(33,59,79)
        for c,where in info['owners'].items():
            if c.startswith('x') and where:sub[np.all(arr==rgb(c),axis=2)]=colors.get(where[0][1],(115,126,132))
        canvas.paste(Image.fromarray(sub).resize((700,500),Image.Resampling.NEAREST),(30+i*760,100))
        d.text((30+i*760,55),title,font=f,fill='white')
    d.text((30,625),'Rouge : Raguse · Bleu : Venise · Ocre : Porte · Mauve : Monténégro',font=f,fill='white')
    d.text((30,660),'Tracé local approximatif ; côtes conservées ; Lastovo absent du bitmap initial.',font=f,fill='white')
    canvas.save(LOT/'ADRIATIC_BEFORE_AFTER.png')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--map',action='store_true');args=p.parse_args()
    if args.apply:apply()
    if args.validate:validate()
    if args.map:render_map()
    if not any(vars(args).values()):print('Use --apply once or --validate / --map.')
