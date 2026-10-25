"""BALKANS-03: bounded Montenegrin initial institutions and military correction.

--apply once; --validate subsequently. No map, POP, vanilla or Git writes.
All historical uncertainty and gameplay calibrations are documented in the lot.
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
LOT=OUT/'BALKANS-03'
COUNTRY='common/history/countries/mon - montenegro.txt'
ARMY='common/history/military_formations/00_military_formations_europe.txt'
STATES='common/history/states/00_states.txt'
GOV='common/government_types/04_theocracies.txt'
OWN=[COUNTRY,ARMY,STATES]
SID='STATE_MONTENEGRO'
PREFIX='1776_world_b03_montenegro'

def dump(name,value):
    (LOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def one(text,key):
    ns=[n for n in walk(parse(text)) if n.key==key]
    assert len(ns)==1,(key,len(ns))
    return ns[0]

def edits(text,ops):
    for lo,hi,new in sorted(ops,reverse=True):text=text[:lo]+new+text[hi:]
    return text

def new_files():
    files={}
    def add(folder,text,filename=None):files[folder+'/'+(filename or PREFIX+'.txt')]=text.strip()+'\n'
    # Override the canonical file by filename, preserving every other government.
    text=a.raw(a.GAME/GOV);n=one(text,'gov_prince_bishopric');block=text[n.start:n.end]
    block=block.replace('male_ruler = "RULER_TITLE_PRINCE_BISHOP"','male_ruler = "aor1776_mon_vladika"')
    block=block.replace('male_heir = "RULER_TITLE_HEIR_APPARENT"','male_heir = "aor1776_mon_coadjutor"')
    block=re.sub(r'# Oddball political system[^\r\n]*','# Montenegrin vladika and appointed coadjutor; the 1776 successor belongs to the Plamenac family.',block)
    files[GOV]=edits(text,[(n.start,n.end,block)])
    add('common/history/characters','''# The sources date Arsenije's birth only to the early eighteenth century.
# Age 65 is a generation estimate, not a claimed archival birth date.
CHARACTERS = { c:MON ?= { create_character = {
 first_name = aor1776_mon_arsenije last_name = aor1776_mon_plamenac
 historical = yes culture = serb religion = rel:orthodox
 heir = yes age = 65 interest_group = ig_devout ideology = ideology_traditionalist
} } }''',filename='zz_'+PREFIX+'.txt')
    add('common/character_traits','''# Office marker only. Not randomly assigned and gives no numerical modifiers.
aor1776_mon_guvernadur = {
 type = condition
 texture = "gfx/interface/icons/character_trait_icons/basic_political_operator.dds"
 possible = { always = no }
 character_modifier = {} command_modifier = {} country_modifier = {}
}''')
    add('common/buildings','''# Existing metropolitan household; capacity abstraction, not an archival staff list.
building_aor1776_cetinje_metropolitan_house = {
 building_group = bg_bureaucracy city_type = city levels_per_mesh = 50
 expandable = no buildable = no downsizeable = no
 potential = { state_region = s:STATE_MONTENEGRO owner = { c:MON ?= this } }
 production_method_groups = { pmg_aor1776_cetinje_metropolitan_house }
 icon = "gfx/interface/icons/building_icons/building_government_administration.dds"
 required_construction = construction_cost_very_low
 background = "gfx/interface/icons/building_icons/backgrounds/building_panel_bg_monuments.dds"
}''')
    add('common/production_method_groups','''pmg_aor1776_cetinje_metropolitan_house = {
 production_methods = { pm_aor1776_cetinje_metropolitan_house }
}''')
    add('common/production_methods','''pm_aor1776_cetinje_metropolitan_house = {
 texture = "gfx/interface/icons/production_method_icons/simple_organization.dds"
 country_modifiers = { workforce_scaled = { country_bureaucracy_add = 2 } }
 state_modifiers = { workforce_scaled = { state_tax_capacity_add = 1 } }
 building_modifiers = {
  workforce_scaled = { goods_input_paper_add = 1 }
  level_scaled = {
   building_employment_clergymen_add = 100 building_employment_clerks_add = 50
   building_employment_bureaucrats_add = 25 building_employment_aristocrats_add = 25
  }
 }
}''')
    add('common/history/buildings','''BUILDINGS = { s:STATE_MONTENEGRO = { region_state:MON = {
 create_building = { building = "building_aor1776_cetinje_metropolitan_house"
  add_ownership = { country = { country = "c:MON" levels = 1 } }
  reserves = 1 activate_production_methods = { "pm_aor1776_cetinje_metropolitan_house" }
 }
} } }''')
    add('common/history/diplomacy','''# Qualitative calibration of continuing border mediation, not a formal alliance.
DIPLOMACY = { c:MON ?= { set_relations = { country = c:VEN value = 20 } } }''',filename='zz_'+PREFIX+'.txt')
    loc={
      'french':{
       'gov_prince_bishopric':'Gouvernement du vladika',
       'gov_prince_bishopric_desc':'Le vladika dirige la métropole et partage les affaires du pays avec le guvernadur et les chefs des clans. Les assemblées locales conservent leur autorité ; le coadjuteur est le successeur désigné du métropolite.',
       'aor1776_mon_vladika':'Vladika','aor1776_mon_coadjutor':'Coadjuteur',
       'aor1776_mon_jovan':'Jovan','aor1776_mon_radonjic':'Radonjić',
       'aor1776_mon_arsenije':'Arsenije','aor1776_mon_plamenac':'Plamenac',
       'aor1776_mon_guvernadur':'Guvernadur',
       'aor1776_mon_guvernadur_desc':'Le guvernadur représente les chefs laïcs et participe à la conduite des affaires et des levées du pays. Il entretient les contacts avec les autorités voisines.',
       'aor1776_mon_clan_muster':'Levée des clans',
       'building_aor1776_cetinje_metropolitan_house':'Maison de la métropole de Cetinje',
       'pmg_aor1776_cetinje_metropolitan_house':'Administration de la métropole',
       'pm_aor1776_cetinje_metropolitan_house':'Offices monastiques'},
      'english':{
       'gov_prince_bishopric':'Government of the Vladika',
       'gov_prince_bishopric_desc':'The vladika heads the metropolitanate and shares public affairs with the guvernadur and the clan chiefs. Local assemblies retain their authority; the coadjutor is the metropolitan’s designated successor.',
       'aor1776_mon_vladika':'Vladika','aor1776_mon_coadjutor':'Coadjutor',
       'aor1776_mon_jovan':'Jovan','aor1776_mon_radonjic':'Radonjić',
       'aor1776_mon_arsenije':'Arsenije','aor1776_mon_plamenac':'Plamenac',
       'aor1776_mon_guvernadur':'Guvernadur',
       'aor1776_mon_guvernadur_desc':'The guvernadur represents the lay chiefs and takes part in the country’s public affairs and musters. He maintains contacts with neighbouring authorities.',
       'aor1776_mon_clan_muster':'Clan Muster',
       'building_aor1776_cetinje_metropolitan_house':'Cetinje Metropolitan Household',
       'pmg_aor1776_cetinje_metropolitan_house':'Metropolitan Administration',
       'pm_aor1776_cetinje_metropolitan_house':'Monastic Offices'}}
    for lang,strings in loc.items():
        files[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in strings.items())
    return files

def transform(originals):
    out=dict(originals)
    text=originals[COUNTRY];n=one(text,'c:MON');rule=n.children('set_ruling_interest_groups')[0]
    assert a.ids(n,'set_ruling_interest_groups')==['ig_landowners']
    law=next(x for x in n.children('activate_law') if x.value=='law_type:law_theocracy')
    out[COUNTRY]=edits(text,[(rule.end-1,rule.end-1,' ig_devout '),
        (law.end,law.end,'\n\t\tactivate_law = law_type:law_oligarchy\n\t\tactivate_law = law_type:law_peasant_levies')])
    text=originals[STATES];n=one(text,'s:'+SID)
    claims=[x for x in n.children('add_claim') if x.value=='c:MON'];assert len(claims)==1
    out[STATES]=edits(text,[(claims[0].start,claims[0].end,'# No blanket Montenegrin political claim on Venetian Cattaro or Ottoman districts.')])
    text=originals[ARMY];n=one(text,'c:MON');formation=n.children('create_military_formation')[0]
    units=formation.children('combat_unit');regular=[u for u in units if u.one('service_type')!='conscript']
    reserve=[u for u in units if u.one('service_type')=='conscript']
    assert sorted((u.one('type'),u.one('count')) for u in regular)==[
        ('unit_type:combat_unit_type_hussars','1'),('unit_type:combat_unit_type_line_infantry','5')]
    assert len(reserve)==1 and reserve[0].one('count')=='1' and reserve[0].one('type')=='unit_type:combat_unit_type_irregular_infantry'
    ops=[(u.start,u.end,'') for u in regular]
    name=formation.children('name')[0];ops.append((name.start,name.end,'name = aor1776_mon_clan_muster'))
    character=n.children('create_character')[0]
    assert character.one('template')=='default' and character.one('is_general')=='yes'
    ops.append((character.start,character.end,'''create_character = {
            first_name = aor1776_mon_jovan last_name = aor1776_mon_radonjic
            historical = yes culture = serb religion = rel:orthodox age = 29
            is_general = yes ig_leader = yes interest_group = ig_landowners
            ideology = ideology_traditionalist traits = { aor1776_mon_guvernadur }
            save_scope_as = cleanup2d4_general_052
        }'''))
    out[ARMY]=edits(text,ops)
    out[ARMY]=out[ARMY].replace('GEN1776-052 — Montengrin_Raiders — PROCEDURAL_ALLOWED','GEN1776-052 — Clan muster — HISTORICAL_JOVAN_RADONJIC')
    return out

def inventory():
    owners,pairs,odd=geo.own_inventory(ROOT,a.GAME)
    total=0;pops=[];assets=[]
    for p in tech.effective('common/history/pops'):
        for n in walk(parse(a.raw(p))):
            if n.key=='create_pop':total+=int(n.one('size'))
            if n.key=='s:'+SID:pops.append(normalized([n]))
    for p in tech.effective('common/history/buildings'):
        for n in walk(parse(a.raw(p))):
            if n.key=='s:'+SID:assets.append(normalized([n]))
    n=one(a.raw(ROOT/COUNTRY),'c:MON')
    grants=[x.value for x in n.children('add_technology_researched')]
    army=one(a.raw(ROOT/ARMY),'c:MON')
    units=[{'type':u.one('type'),'count':int(u.one('count')),'service':u.one('service_type','regular')} for u in walk([army]) if u.key=='combat_unit']
    return {'world_population':total,'pops':pops,'assets':assets,'technologies':grants,'units':units,
        'owners':{k:[list(x) for x in v] for k,v in owners.items()},'odd':odd,'git':a.git_state()}

def apply():
    LOT.mkdir(parents=True,exist_ok=True)
    assert not (LOT/'BASELINE.json').exists(),'Already installed; use --validate.'
    news=new_files();assert all(not (ROOT/r).exists() for r in news)
    original={r:a.raw(ROOT/r) for r in OWN};updated=transform(original)
    baseline={'owned':{r:a.sha(ROOT/r) for r in OWN},'protected':{},'serg':{},'new':list(news),
              'before':inventory(),'vanilla_government_sha256':a.sha(a.GAME/GOV)}
    for folder in ['common','events','gui','gfx','localization','map_data']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():
                r=p.relative_to(ROOT).as_posix()
                if r not in OWN:baseline['protected'][r]=a.sha(p)
    for p in (ROOT/'docs/reports/map/SERG_CLOSURE').rglob('*'):
        if p.is_file():baseline['serg'][p.relative_to(ROOT).as_posix()]=a.sha(p)
    for r in OWN:
        dest=LOT/'patch_inputs'/r;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,dest)
    source=LOT/'native_reference'/GOV;source.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a.GAME/GOV,source)
    dump('BASELINE.json',baseline)
    assert all(a.sha(ROOT/r)==h for r,h in baseline['owned'].items()),'Concurrent shared edit: reread and adapt.'
    for r,t in updated.items():
        p=ROOT/r;bom=b'\xef\xbb\xbf' if p.read_bytes().startswith(b'\xef\xbb\xbf') else b''
        p.write_bytes(bom+t.encode('utf8'))
    for r,t in news.items():
        p=ROOT/r;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((b'\xef\xbb\xbf' if r.endswith('.yml') else b'')+t.encode('utf8'))
    dump('AFTER.json',inventory())
    dump('FILES_MODIFIED.json',[{'file':r,'before':baseline['owned'].get(r),'after':a.sha(ROOT/r)} for r in OWN+list(news)])
    print('Installed: Montenegrin institutions, appointed coadjutor, guvernadur, existing reserve; no bitmap/POP edits.')

def validate():
    base=json.loads((LOT/'BASELINE.json').read_text(encoding='utf8'));after=inventory();checks=[]
    def check(key,value,details=None):checks.append({'check':key,'passed':bool(value),'detail':details})
    old={r:a.raw(LOT/'patch_inputs'/r) for r in OWN};expected=transform(old);news=new_files()
    for r,t in {**expected,**news}.items():
        check('exact_scoped_text.'+r,a.raw(ROOT/r)==t)
        if r.endswith('.txt'):check('parse.'+r,bool(parse(t)))
    for r in OWN:
        key='s:'+SID if r==STATES else 'c:MON'
        before_node=one(old[r],key);after_node=one(a.raw(ROOT/r),key)
        def exterior(t,n):return t[:n.start]+'<SCOPED_NODE>'+t[n.end:]
        check('outside_MON_block_identical.'+r,exterior(old[r],before_node)==exterior(a.raw(ROOT/r),after_node))
    check('vanilla_reference_unchanged',a.sha(a.GAME/GOV)==base['vanilla_government_sha256'])
    orig_gov=parse(a.raw(a.GAME/GOV));new_gov=parse(a.raw(ROOT/GOV))
    for n in orig_gov:
        if n.key!='gov_prince_bishopric':check('other_government_unchanged.'+n.key,normalized([n])==normalized([one(a.raw(ROOT/GOV),n.key)]))
    gov=one(a.raw(ROOT/GOV),'gov_prince_bishopric')
    check('government_still_hereditary',gov.one('transfer_of_power')=='hereditary')
    check('MON_only_government_scope','c:MON = ROOT' in a.raw(ROOT/GOV)[gov.start:gov.end])
    check('no_ownership_changes',after['owners']==base['before']['owners'])
    check('population_world_conserved',after['world_population']==base['before']['world_population'],after['world_population'])
    check('local_POPs_cultures_religions_professions_identical',after['pops']==base['before']['pops'])
    check('nine_technologies_preserved',after['technologies']==base['before']['technologies'] and len(after['technologies'])==9)
    objects,_,_=tech.objects('common/technology/technologies');grants=set(after['technologies'])
    check('technology_ids_resolve',grants<=set(objects))
    check('technology_prerequisites_closed',all(set(a.ids(objects[k],'unlocking_technologies'))<=grants for k in grants))
    country=one(a.raw(ROOT/COUNTRY),'c:MON')
    check('clergy_and_chiefs_in_government',set(a.ids(country,'set_ruling_interest_groups'))=={'ig_landowners','ig_devout'})
    laws=[x.value for x in country.children('activate_law')]
    for key in ['law_theocracy','law_oligarchy','law_peasant_levies']:check('law_active.'+key,'law_type:'+key in laws)
    lawkeys={k.split(':')[-1] for k in a.catalog('common/laws')}
    check('law_ids_resolve',all(l.split(':')[-1] in lawkeys for l in laws))
    check('no_regular_units',all(u['service']=='conscript' for u in after['units']))
    check('single_existing_reserve_preserved',after['units']==[u for u in base['before']['units'] if u['service']=='conscript'])
    types=a.catalog('common/combat_unit_types')
    for u in after['units']:
        key=u['type'].split(':')[-1];un,_=types[key]
        check('unit_tech_eligible.'+key,set(a.ids(un,'unlocking_technologies'))<=grants)
        check('unit_levy_eligible.'+key,un.one('conscript_peasant_levies')=='yes')
    regional=one(a.raw(ROOT/STATES),'s:'+SID)
    check('blanket_MON_claim_removed',not any(n.value=='c:MON' for n in regional.children('add_claim')))
    check('Cattaro_remains_Venetian',after['owners'].get('x90A0E0')==[[SID,'VEN']])
    check('core_MON_preserved',after['owners'].get('x8C6292')==[[SID,'MON']])
    military=one(a.raw(ROOT/ARMY),'c:MON');j=military.children('create_character')[0]
    for k,v in [('historical','yes'),('first_name','aor1776_mon_jovan'),('last_name','aor1776_mon_radonjic'),('ig_leader','yes'),('is_general','yes'),('interest_group','ig_landowners')]:check('Jovan.'+k,j.one(k)==v)
    heir=one(news['common/history/characters/zz_'+PREFIX+'.txt'],'create_character')
    check('Arsenije_named_coadjutor',heir.one('heir')=='yes' and heir.one('first_name')=='aor1776_mon_arsenije' and heir.one('ruler')!='yes')
    existing=ROOT/'common/history/characters/cleanup2b1 - major rulers 1776.txt'
    sava=one(a.raw(existing),'c:MON').children('create_character')[0]
    check('Sava_ruler_preserved',sava.one('first_name')=='Sava_II' and sava.one('ruler')=='yes')
    trait=one(news['common/character_traits/'+PREFIX+'.txt'],'aor1776_mon_guvernadur')
    check('office_trait_has_no_bonuses',all(not n.children() for n in trait.children() if n.key.endswith('_modifier')))
    check('office_not_random',trait.children('possible')[0].one('always')=='no')
    jobs=a.recipe(a.catalog('common/production_methods')['pm_aor1776_cetinje_metropolitan_house'][0])
    check('administration_positive_jobs',all(float(x)>=0 for x in jobs['jobs'].values()) and sum(map(float,jobs['jobs'].values()))==200)
    pmg=a.catalog('common/production_method_groups')['pmg_aor1776_cetinje_metropolitan_house'][0]
    check('new_PM_registered',a.ids(pmg,'production_methods')==['pm_aor1776_cetinje_metropolitan_house'])
    check('new_PM_no_unmet_gate',not jobs['gates'])
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml'
        check('BOM.'+lang,p.read_bytes().startswith(b'\xef\xbb\xbf'))
        defined=set(re.findall(r'^\s+(\w+):\d',a.raw(p),re.M))
        for k in ['aor1776_mon_jovan','aor1776_mon_radonjic','aor1776_mon_arsenije','aor1776_mon_plamenac','aor1776_mon_vladika','aor1776_mon_coadjutor','aor1776_mon_guvernadur','aor1776_mon_clan_muster']:
            check('localization.'+lang+'.'+k,k in defined)
    check('icon_exists',(a.GAME/'gfx/interface/icons/character_trait_icons/basic_political_operator.dds').exists())
    external={r:{'before':h,'observed_now':a.sha(ROOT/r) if (ROOT/r).exists() else None} for r,h in base['protected'].items() if not (ROOT/r).exists() or a.sha(ROOT/r)!=h}
    serg=[r for r,h in base['serg'].items() if not (ROOT/r).exists() or a.sha(ROOT/r)!=h]
    check('protected_gameplay_unchanged',not external,list(external))
    check('SERG_proofs_unchanged',not serg,serg)
    check('git_unchanged',after['git']==base['before']['git'])
    for lot in ['BALKANS-01','BALKANS-02']:
        manifest=json.loads((OUT/lot/'FILES_MODIFIED.json').read_text(encoding='utf8'))
        # Shared state history intentionally changes; other owned files must survive.
        for e in manifest:
            r=e['file']
            if r in OWN:continue
            check('prior_lot_preserved.'+lot+'.'+r,a.sha(ROOT/r)==e['after'])
    dump('CONCURRENT_CHANGES.json',{'external_gameplay':external,'SERG_proofs':serg,'shared_files':'Three current MON scopes only; no restoration from old lot baselines.'})
    dump('STARTING_TECH_CHECK.json',{'tag':'MON','technologies':after['technologies'],'count':9,'units_before':base['before']['units'],'units_after':after['units'],'new_PM':jobs,'runtime':'NOT_RUN'})
    result={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','historical_boundaries':'NOT_CERTIFIED_NO_PIXEL_TRANSFER'}
    dump('VALIDATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}));print([c for c in checks if not c['passed']])
    return result

def render_map():
    data=inventory();im=Image.open(ROOT/'map_data/provinces.png').convert('RGB');arr=np.array(im)[1045:1095,4495:4560]
    colors={'MON':(168,103,154),'VEN':(103,164,204),'TUR':(197,171,113),'RAG':(169,59,67)}
    panel=np.zeros_like(arr);panel[:]=(32,58,78)
    for c,owners in data['owners'].items():
        color=tuple(bytes.fromhex(c[1:]))
        panel[np.all(arr==color,axis=2)]=colors.get(owners[0][1],(125,128,129))
    canvas=Image.new('RGB',(1120,890),(21,30,40));canvas.paste(Image.fromarray(panel).resize((1040,800),Image.Resampling.NEAREST),(40,50));draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    draw.text((40,14),'BALKANS-03 : répartition politique conservée, aucune province transférée',font=font,fill='white')
    draw.text((40,858),'Mauve : MON · Bleu : VEN · Ocre : TUR · Rouge : RAG — les hubs natifs ne prouvent pas une frontière historique.',font=font,fill='white')
    canvas.save(LOT/'MONTENEGRO_CATTARO_CURRENT.png')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--map',action='store_true');args=p.parse_args()
    if args.apply:apply()
    if args.validate:validate()
    if args.map:render_map()
    if not any(vars(args).values()):print('Use --apply once, then --validate / --map.')
