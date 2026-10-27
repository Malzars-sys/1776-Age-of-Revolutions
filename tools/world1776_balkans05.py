"""B05: provincial households, bounded reassignment of existing Ottoman troops.

--apply installs once from the current shared file; --validate is repeatable.
No map, POP, technology, vanilla, SERG or Git writes. Historical limits in REPORT.
"""
import argparse
import json
import re
import shutil
from collections import Counter
import world1776_balkans03 as b
import world1776_balkans04 as b4

ROOT=b.ROOT; OUT=b.OUT; LOT=OUT/'BALKANS-05'
ARMY='common/history/military_formations/04_military_formations_middle_east.txt'
NEWARMY='common/history/military_formations/zz_1776_world_b05_albanian_households.txt'
TRAIT='common/character_traits/1776_world_b05_albanian_households.txt'
PREFIX='aor1776_b05_'

def dump(name,obj):
    (LOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((LOT/name).read_text('utf8'))

def transform(text):
    country=b.one(text,'c:TUR')
    formation=next(n for n in country.children('create_military_formation') if n.one('save_scope_as')=='rumeli_ordusu')
    units=formation.children('combat_unit')
    cavalry=next(n for n in units if n.one('type')=='unit_type:combat_unit_type_hussars')
    foot=next(n for n in units if n.one('type')=='unit_type:combat_unit_type_irregular_infantry')
    assert cavalry.one('state_region')==foot.one('state_region')=='s:STATE_ALBANIA'
    assert cavalry.one('count')=='4' and foot.one('count')=='2'
    assert cavalry.one('service_type','regular')==foot.one('service_type','regular')=='regular'
    count=cavalry.children('count')[0]
    return b.edits(text,[(count.start,count.end,'count = 2'),(foot.start,foot.end,'')])

def new_files():
    files={NEWARMY:'''# B05: two provincial households within the existing Ottoman framework.
# Existing regular units moved from Rumelia, not additional troop estimates.
# Gjeli 2018 pp.35-41: Mustafa heads Scutari in 1776, not Mahmud.
# Inbasi 2019 p.149: Kurd Ahmed holds Avlonya during 1774-1778.
MILITARY_FORMATIONS = {
 c:TUR ?= {
  create_military_formation = {
   type = army hq_region = sr:region_balkans
   name = aor1776_b05_scutari_household
   combat_unit = {
    type = unit_type:combat_unit_type_irregular_infantry
    state_region = s:STATE_ALBANIA count = 2
   }
   save_scope_as = aor1776_b05_scutari_formation
  }
  create_military_formation = {
   type = army hq_region = sr:region_balkans
   name = aor1776_b05_avlonya_contingent
   combat_unit = {
    type = unit_type:combat_unit_type_hussars
    state_region = s:STATE_ALBANIA count = 2
   }
   save_scope_as = aor1776_b05_avlonya_formation
  }
  # Ages are technical generation estimates, not verified birth years.
  # IG and ideology are qualitative gameplay representations of household rule.
  create_character = {
   first_name = aor1776_b05_mustafa last_name = aor1776_b05_bushati
   historical = yes culture = albanian religion = rel:sunni age = 40
   is_general = yes commander_rank = commander_rank_1
   interest_group = ig_landowners ideology = ideology_traditionalist
   traits = { aor1776_b05_scutari_head }
   save_scope_as = aor1776_b05_mustafa_character
  }
  scope:aor1776_b05_mustafa_character = {
   transfer_to_formation = scope:aor1776_b05_scutari_formation
  }
  create_character = {
   first_name = aor1776_b05_ahmed last_name = aor1776_b05_kurt
   historical = yes culture = albanian religion = rel:sunni age = 55
   is_general = yes commander_rank = commander_rank_1
   interest_group = ig_landowners ideology = ideology_traditionalist
   traits = { aor1776_b05_avlonya_governor }
   save_scope_as = aor1776_b05_ahmed_character
  }
  scope:aor1776_b05_ahmed_character = {
   transfer_to_formation = scope:aor1776_b05_avlonya_formation
  }
 }
}
''',TRAIT:'''# Office labels only: no random assignment or numerical bonus.
aor1776_b05_scutari_head = {
 type = condition
 texture = "gfx/interface/icons/character_trait_icons/basic_political_operator.dds"
 possible = { always = no }
 character_modifier = {} command_modifier = {} country_modifier = {}
}
aor1776_b05_avlonya_governor = {
 type = condition
 texture = "gfx/interface/icons/character_trait_icons/basic_political_operator.dds"
 possible = { always = no }
 character_modifier = {} command_modifier = {} country_modifier = {}
}
'''}
    loc={
      'french':{
       'mustafa':'Mustafa','bushati':'Bushati','ahmed':'Ahmed','kurt':'Kurt',
       'scutari_household':'Maison de Scutari','avlonya_contingent':'Contingent d’Avlonya',
       'scutari_head':'Chef de la maison de Scutari',
       'scutari_head_desc':'Ce notable dirige la maison de Scutari et rassemble ses hommes. Son autorité repose sur les alliances locales et sur ses rapports avec la Porte.',
       'avlonya_governor':'Mutasarrıf d’Avlonya',
       'avlonya_governor_desc':'Le gouverneur d’Avlonya répond devant la Porte de l’ordre, des recettes et du contingent demandé à sa province.'},
      'english':{
       'mustafa':'Mustafa','bushati':'Bushati','ahmed':'Ahmed','kurt':'Kurt',
       'scutari_household':'Scutari Household','avlonya_contingent':'Avlonya Contingent',
       'scutari_head':'Head of the Scutari Household',
       'scutari_head_desc':'This notable leads the Scutari household and musters its men. His authority rests on local alliances and his dealings with the Porte.',
       'avlonya_governor':'Mutasarrıf of Avlonya',
       'avlonya_governor_desc':'The governor of Avlonya answers to the Porte for order, revenue and the contingent required from his province.'}}
    for lang,strings in loc.items():
        files[f'localization/{lang}/1776_world_b05_albanian_households_l_{lang}.yml']='l_'+lang+':\n'+''.join(' '+PREFIX+k+':0 "'+v+'"\n' for k,v in strings.items())
    return files

def military_snapshot():
    counts=Counter(); formations=[]; characters=[]; bindings=[]
    for p in b.tech.effective('common/history/military_formations'):
        for root in b.parse(b.a.raw(p)):
            for country in root.children():
                if not country.key.startswith('c:'):continue
                for f in country.children('create_military_formation'):
                    formations.append([country.key,f.one('name'),f.one('save_scope_as')])
                    for u in f.children('combat_unit'):
                        counts[(country.key,u.one('state_region'),u.one('type'),u.one('service_type','regular'))]+=int(u.one('count','1'))
                for n in country.children('create_character'):
                    characters.append([country.key,b.normalized([n])])
                for n in country.children():
                    if n.key.startswith('scope:'):bindings.append([country.key,b.normalized([n])])
    # The parser's normalized nodes contain tuples. Compare the same JSON
    # representation as the archived before-snapshot, rather than tuple/list types.
    return json.loads(json.dumps({'counts':[[*key,v] for key,v in sorted(counts.items())],
            'formations':formations,'characters':characters,'bindings':bindings}))

def capture():
    game={}
    for folder in ['common','events','localization','map_data','gfx','gui']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():game[p.relative_to(ROOT).as_posix()]=b.a.sha(p)
    initial=load('BASELINE.json')
    return {'gameplay':game,'military':military_snapshot(),'inventory':b4.inventory(),
            'SERG_proofs':{r:b.a.sha(ROOT/r) for r in initial['SERG_proofs']},
            'prior_WORLD_proofs':{r:b.a.sha(ROOT/r) for r in initial['prior_WORLD_proofs']}}

def apply():
    assert not (LOT/'APPLY_BASELINE.json').exists(),'Already applied; use --validate.'
    files=new_files();assert all(not (ROOT/r).exists() for r in files)
    before=capture();original=b.a.raw(ROOT/ARMY);updated=transform(original)
    p=LOT/'patch_inputs'/ARMY;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/ARMY,p)
    dump('APPLY_BASELINE.json',before)
    assert b.a.sha(ROOT/ARMY)==before['gameplay'][ARMY],'Shared input changed; reread.'
    bom=b'\xef\xbb\xbf' if (ROOT/ARMY).read_bytes().startswith(b'\xef\xbb\xbf') else b''
    (ROOT/ARMY).write_bytes(bom+updated.encode('utf8'))
    for r,text in files.items():
        p=ROOT/r;p.parent.mkdir(parents=True,exist_ok=True)
        assert not p.exists(),'Concurrent new file.'
        p.write_bytes((b'\xef\xbb\xbf' if r.endswith('.yml') else b'')+text.encode('utf8'))
    dump('FILES_MODIFIED.json',[{'file':r,'before':before['gameplay'].get(r),'after':b.a.sha(ROOT/r)} for r in [ARMY,*files]])
    print('B05 installed: four existing battalions reassigned, two historical household leaders; no territorial changes.')

def validate():
    before=load('APPLY_BASELINE.json');entry=load('BASELINE.json');checks=[]
    def check(k,v,detail=None):checks.append({'check':k,'passed':bool(v),'detail':detail})
    original=b.a.raw(LOT/'patch_inputs'/ARMY);current=b.a.raw(ROOT/ARMY)
    expected={ARMY:transform(original),**new_files()}
    for r,t in expected.items():
        check('exact_scoped_output.'+r,b.a.raw(ROOT/r)==t)
        if r.endswith('.txt'):check('parse.'+r,bool(b.parse(t)))
    def outside(t,n):return t[:n.start]+'<TUR>'+t[n.end:]
    check('all_other_countries_byte_identical',outside(original,b.one(original,'c:TUR'))==outside(current,b.one(current,'c:TUR')))
    now=military_snapshot()
    check('world_units_conserved_by_country_state_type_service',now['counts']==before['military']['counts'])
    for key in ['formations','characters','bindings']:
        check('all_existing_'+key+'_preserved',all(e in now[key] for e in before['military'][key]))
    check('exactly_two_formations_added',len(now['formations'])==len(before['military']['formations'])+2)
    check('exactly_two_characters_added',len(now['characters'])==len(before['military']['characters'])+2)
    check('exactly_two_bindings_added',len(now['bindings'])==len(before['military']['bindings'])+2)
    newcountry=b.one(expected[NEWARMY],'c:TUR')
    scopes=[n.one('save_scope_as') for n in b.walk(b.parse(expected[NEWARMY])) if n.children('save_scope_as')]
    check('new_scopes_unique',len(scopes)==len(set(scopes))==4)
    oldscopes=set()
    for p in (ROOT/'common/history').rglob('*.txt'):
        if p==ROOT/NEWARMY:continue
        oldscopes.update(n.value for n in b.walk(b.parse(b.a.raw(p))) if n.key=='save_scope_as' and isinstance(n.value,str))
    check('new_scopes_do_not_collide',not (set(scopes)&oldscopes))
    types=b.a.catalog('common/combat_unit_types');cultures=b.a.catalog('common/cultures');religions=b.a.catalog('common/religions')
    for f in newcountry.children('create_military_formation'):
        check('HQ.'+f.one('save_scope_as'),f.one('hq_region')=='sr:region_balkans')
        for u in f.children('combat_unit'):
            check('unit_reference.'+u.one('type'),u.one('type').split(':')[-1] in types)
            check('state_and_regular_service.'+f.one('save_scope_as'),u.one('state_region')=='s:STATE_ALBANIA' and u.one('service_type','regular')=='regular')
    check('albanian_culture_exists','albanian' in cultures);check('sunni_religion_exists','sunni' in religions)
    check('landowners_IG_exists','ig_landowners' in b.a.catalog('common/interest_groups'))
    check('traditionalist_ideology_exists','ideology_traditionalist' in b.a.catalog('common/ideologies'))
    for n in b.parse(expected[TRAIT]):
        check('nonrandom_office.'+n.key,n.children('possible')[0].one('always')=='no')
        check('no_office_stat_bonuses.'+n.key,all(not n.children(k)[0].children() for k in ['character_modifier','command_modifier','country_modifier']))
        check('native_texture.'+n.key,(b.a.GAME/n.one('texture').strip('"')).exists())
    for lang in ['french','english']:
        r=f'localization/{lang}/1776_world_b05_albanian_households_l_{lang}.yml'
        check('BOM.'+lang,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
        keys=re.findall(r'^\s+('+PREFIX+r'\w+):',expected[r],re.M)
        check('ten_unique_localized_keys.'+lang,len(keys)==len(set(keys))==10)
        duplicates=[]
        for p in (ROOT/'localization'/lang).rglob('*.yml'):
            if p==ROOT/r:continue
            found=re.findall(r'^\s*('+PREFIX+r'\w+):',b.a.raw(p),re.M)
            if found:duplicates.append(str(p))
        check('no_other_localization_definitions.'+lang,not duplicates,duplicates)
    owners=b4.inventory()
    for k in ['world_population','owners','odd','git']:check('unchanged.'+k,owners[k]==before['inventory'][k])
    check('world_population_834936539',owners['world_population']==834936539)
    changed={}
    for category,key in [('gameplay','gameplay'),('SERG_proofs','SERG_proofs'),('prior_WORLD_proofs','prior_WORLD_proofs')]:
        differences=[{'file':r,'before':h,'current':b.a.sha(ROOT/r) if (ROOT/r).exists() else None} for r,h in before[key].items() if r!=ARMY and (not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h)]
        changed[category]=differences
        check('all_preapply_'+category+'_preserved',not differences,differences)
    # Entry-to-apply changes are observations, never overwritten or attributed to B05.
    entry_delta={k:[{'file':r,'before':h,'at_apply':before[k].get(r)} for r,h in entry[k].items() if before[k].get(r)!=h] for k in ['gameplay','SERG_proofs']}
    check('previous_WORLD_archives_unchanged_since_entry',all(b.a.sha(ROOT/r)==h for r,h in entry['prior_WORLD_proofs'].items()))
    beforetech=load('TECH_BEFORE.json')[0];aftertech=load('TECH_AFTER.json')[0]
    check('technology_findings_not_increased',aftertech['findings']==beforetech['findings'])
    check('technology_grants_unchanged',aftertech['technologies']==beforetech['technologies'])
    check('technology_unit_types_unchanged',aftertech['unit_types']==beforetech['unit_types'])
    dump('CONCURRENT_CHANGES.json',{'entry_to_apply_observed':entry_delta,'after_apply_differences':changed,'Git_writes':0,'SERG_writes':0,'vanilla_writes':0,'baseline_restored':False})
    dump('POPULATION_LEDGER.json',{'world_before':before['inventory']['world_population'],'world_after':owners['world_population'],'delta':0,'all_POP_files_sha256_unchanged':all(b.a.sha(ROOT/r)==h for r,h in before['gameplay'].items() if r.startswith('common/history/pops/')),'transfers':[]})
    dump('MILITARY_LEDGER.json',{'before':before['military'],'after':now,'units_added':0,'units_removed':0,'existing_units_reassigned':4,'new_generals':2,'type_state_service_counts_conserved':now['counts']==before['military']['counts']})
    dump('STARTING_TECH_CHECK.json',{'status':'PREEXISTING_DEBT_NO_NEW_FINDINGS','T_criterion':'PARTIAL_NO_CREDIT','empire_before_status':beforetech['status'],'empire_after_status':aftertech['status'],'identical_findings':aftertech['findings']==beforetech['findings'],'unit_gates':{k:b.a.ids(types[k][0],'unlocking_technologies') for k in ['combat_unit_type_hussars','combat_unit_type_irregular_infantry']},'technologies_unchanged':aftertech['technologies']==beforetech['technologies'],'new_technologies':[],'engine_tested':False})
    passed=sum(c['passed'] for c in checks)
    dump('VALIDATION.json',{'status':'PASS' if passed==len(checks) else 'FAIL','passed':passed,'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_validation':False})
    print(json.dumps({'passed':passed,'total':len(checks),'failed':[c['check'] for c in checks if not c['passed']]}))
    return passed==len(checks)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true');args=p.parse_args()
    if args.apply:apply()
    elif args.validate:raise SystemExit(0 if validate() else 1)
    else:p.print_help()
