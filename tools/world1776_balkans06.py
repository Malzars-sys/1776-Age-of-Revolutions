"""B06 mainland Greece / Morea: bounded initial coastal defence and civil office.

New files only, no map/POP/shared recipe/technology/Git/vanilla/SERG writes.
Crete remains outside this authorization. --apply once; --validate thereafter.
"""
import argparse
import json
import re
from collections import defaultdict
import world1776_balkans05 as prev

b=prev.b; ROOT=b.ROOT; OUT=b.OUT; LOT=OUT/'BALKANS-06'
BUILD='common/history/buildings/1776_world_b06_greek_coastal_defences.txt'
CHAR='common/history/characters/zz_1776_world_b06_athens.txt'
TRAIT='common/character_traits/1776_world_b06_athens.txt'
SIDS=['STATE_ATTICA','STATE_PELOPONNESE']
PM='pm_naval_fortification_basic';KIND='building_naval_fortification';PREFIX='aor1776_b06_'

def load(n):return json.loads((LOT/n).read_text('utf8'))
def dump(n,v):(LOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def files():
    buildings=['# B06: regional capacity for attested Ottoman coastal fortifications, not exact site meshes.',
               '# ATTICA: Lepanto/Antirrio; PELOPONNESE: Nauplia/Palamidi. One aggregate level each.',
               '# No later Haseki wall (1778), Ali Pasha works, or modern inland-fort building.', 'BUILDINGS = {']
    for sid in SIDS:
        buildings.append(f''' s:{sid} = {{ region_state:TUR = {{
  create_building = {{
   building = "{KIND}"
   add_ownership = {{ country = {{ country = "c:TUR" levels = 1 }} }}
   reserves = 1
   activate_production_methods = {{ "{PM}" }}
  }}
 }} }}''')
    buildings.append('}')
    out={BUILD:'\n'.join(buildings)+'\n',CHAR:'''# Kupeli 2020, pp.464-465: first Athenian voivodate in 1775-1776.
# Politician pool only: no general, national IG leadership, or state-governor mechanic.
# Age 45 is a technical adult-generation calibration, not an archival birth year.
CHARACTERS = { c:TUR ?= {
 create_character = {
  first_name = aor1776_b06_haci_ali last_name = aor1776_b06_haseki
  historical = yes culture = turkish religion = rel:sunni age = 45
  role = politician interest_group = ig_landowners ideology = ideology_traditionalist
  traits = { aor1776_b06_athens_voivode }
  trait_generation = { }
 }
} }
''',TRAIT:'''# Dated civil office label, never randomly assigned and no numerical modifier.
aor1776_b06_athens_voivode = {
 type = condition
 texture = "gfx/interface/icons/character_trait_icons/basic_political_operator.dds"
 possible = { always = no }
 character_modifier = {} command_modifier = {} country_modifier = {}
}
'''}
    for lang,strings in {
        'french':{'haci_ali':'Hacı Ali','haseki':'Haseki','athens_voivode':'Voïvode d’Athènes','athens_voivode_desc':'Le voïvode administre Athènes et ses dépendances et intervient dans la collecte des recettes. Il traite avec les autorités ottomanes, les notables et les représentants des communautés.'},
        'english':{'haci_ali':'Hacı Ali','haseki':'Haseki','athens_voivode':'Voivode of Athens','athens_voivode_desc':'The voivode administers Athens and its dependencies and takes part in revenue collection. He deals with Ottoman officials, local notables and community representatives.'}}.items():
        out[f'localization/{lang}/1776_world_b06_athens_l_{lang}.yml']='l_'+lang+':\n'+''.join(' '+PREFIX+k+':0 "'+v+'"\n' for k,v in strings.items())
    return out

def population():
    rows=defaultdict(lambda:defaultdict(int))
    for p in b.tech.effective('common/history/pops'):
        for root in b.parse(b.a.raw(p)):
            for s in root.children():
                if s.key.removeprefix('s:') not in SIDS+['STATE_THESSALIA']:continue
                for c in s.children():
                    for n in c.children('create_pop'):rows[s.key][c.key]+=int(n.one('size'))
    return dict(rows)

def existing_forts():
    found=[]
    for p in b.tech.effective('common/history/buildings'):
        for root in b.parse(b.a.raw(p)):
            for s in root.children():
                if s.key.removeprefix('s:') not in SIDS:continue
                for c in s.children():
                    if c.key!='region_state:TUR':continue
                    for n in c.children('create_building'):
                        if n.one('building','').strip('"')==KIND:found.append([p.relative_to(ROOT).as_posix(),s.key,n])
    return found

def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed; use --validate.'
    new=files();assert all(not (ROOT/r).exists() for r in new)
    assert not existing_forts(),'Review existing capacity before adding levels.'
    # Independent additions are composed on the current workspace; no old file is restored.
    current={r:b.a.sha(ROOT/r) for r in load('BASELINE.json')['gameplay']}
    before={'gameplay':current,'inventory':prev.b4.inventory(),'military':prev.military_snapshot(),'population':population(),
            'SERG_proofs':{r:b.a.sha(ROOT/r) for r in load('BASELINE.json')['SERG_proofs']},
            'prior_WORLD_proofs':{r:b.a.sha(ROOT/r) for r in load('BASELINE.json')['prior_WORLD_proofs']}}
    dump('APPLY_BASELINE.json',before)
    for r,t in new.items():
        p=ROOT/r;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists()
        p.write_bytes((b'\xef\xbb\xbf' if r.endswith('.yml') else b'')+t.encode('utf8'))
    dump('FILES_MODIFIED.json',[{'file':r,'before':None,'after':b.a.sha(ROOT/r)} for r in new])
    print('B06 installed: two existing-site coastal capacities; one civil historical politician; no shared gameplay edits.')

def validate():
    before=load('APPLY_BASELINE.json');entry=load('BASELINE.json');checks=[]
    def ck(k,v,detail=None):checks.append({'check':k,'passed':bool(v),'detail':detail})
    for r,t in files().items():
        ck('exact_new_file.'+r,b.a.raw(ROOT/r)==t)
        if r.endswith('.txt'):ck('parse.'+r,bool(b.parse(t)))
    found=existing_forts();ck('two_defence_declarations',len(found)==2)
    buildings=b.a.catalog('common/buildings');pms=b.a.catalog('common/production_methods');groups=b.a.catalog('common/production_method_groups')
    fort=buildings[KIND][0];pm=pms[PM][0];recipe=b.a.recipe(pm)
    known=set(load('TECH_AFTER.json')[0]['technologies'])
    ck('building_gate_satisfied',set(b.a.ids(fort,'unlocking_technologies'))<=known)
    ck('PM_gate_satisfied',set(b.a.ids(pm,'unlocking_technologies'))<=known)
    ck('PM_belongs_to_building_group',any(PM in b.a.ids(groups[g][0],'production_methods') for g in b.a.ids(fort,'production_method_groups')))
    ck('existing_recipe_exact',recipe['jobs']=={'soldiers':'900','officers':'100'} and recipe['inputs']=={'small_arms':'5','iron':'5'})
    state_text=b.a.raw(ROOT/'common/history/states/00_states.txt');terrain=b.a.raw(ROOT/'map_data/province_terrains.txt')
    regions=b.a.raw(ROOT/'map_data/state_regions/01_south_europe.txt')
    for path,sid,node in found:
        state=b.one(state_text,sid);ck('TUR_portion.'+sid,any(n.one('country')=='c:TUR' for n in state.children('create_state')))
        ck('only_one_level.'+sid,sum(int(n.value) for n in b.walk([node]) if n.key=='levels')==1)
        ck('only_basic_PM.'+sid,[v.strip('"') for v in b.a.ids(node,'activate_production_methods')]==[PM])
        ck('TUR_country_ownership.'+sid,any(n.key=='country' and n.value=='"c:TUR"' for n in b.walk([node])))
        region=b.one(regions,sid.removeprefix('s:'));provs=[x.strip('"') for x in b.a.ids(region,'provinces')]
        # Verify the installed state already has a native sea exit; runtime province/hub assignment remains separate.
        ck('coastal_native_region.'+sid,region.one('naval_exit_id') is not None and bool(provs))
    char=b.one(files()[CHAR],'create_character')
    ck('civil_politician',char.one('role')=='politician' and not char.children('is_general') and not char.children('is_admiral'))
    ck('no_national_leadership',not char.children('ig_leader') and not char.children('ruler') and not char.children('heir'))
    ck('birth_region_not_inferred_from_office',not char.children('home_region'))
    for cat,key in [('common/cultures','turkish'),('common/religions','sunni'),('common/interest_groups','ig_landowners'),('common/ideologies','ideology_traditionalist')]:ck('reference.'+key,key in b.a.catalog(cat))
    ck('politician_role_native','character_role_politician' in b.a.catalog('common/character_roles'))
    trait=b.one(files()[TRAIT],PREFIX+'athens_voivode')
    ck('office_not_random',trait.children('possible')[0].one('always')=='no')
    ck('office_no_bonuses',all(not trait.children(k)[0].children() for k in ['character_modifier','command_modifier','country_modifier']))
    ck('native_trait_texture',(b.a.GAME/trait.one('texture').strip('"')).exists())
    for lang in ['french','english']:
        r=f'localization/{lang}/1776_world_b06_athens_l_{lang}.yml';text=b.a.raw(ROOT/r)
        ck('BOM.'+lang,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
        keys=re.findall(r'^\s+('+PREFIX+r'\w+):',text,re.M)
        ck('four_unique_keys.'+lang,len(keys)==len(set(keys))==4)
        duplicates=[]
        for p in (ROOT/'localization'/lang).rglob('*.yml'):
            if p==ROOT/r:continue
            if re.search(r'^\s*'+PREFIX+r'\w+:',b.a.raw(p),re.M):duplicates.append(str(p))
        ck('no_localization_collisions.'+lang,not duplicates,duplicates)
    ck('military_entirely_identical',prev.military_snapshot()==before['military'])
    now=prev.b4.inventory()
    for key in ['world_population','owners','odd','git']:ck('unchanged.'+key,now[key]==before['inventory'][key])
    ck('regional_populations_identical',population()==before['population'])
    changes={}
    for group in ['gameplay','SERG_proofs','prior_WORLD_proofs']:
        delta=[{'file':r,'before':h,'after':b.a.sha(ROOT/r) if (ROOT/r).exists() else None} for r,h in before[group].items() if not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h]
        changes[group]=delta;ck('all_old_'+group+'_preserved',not delta,delta)
    entry_changes={k:[{'file':r,'entry':h,'at_apply':before[k].get(r)} for r,h in entry[k].items() if before[k].get(r)!=h] for k in ['gameplay','SERG_proofs','prior_WORLD_proofs']}
    oldtech=load('TECH_BEFORE.json')[0];newtech=load('TECH_AFTER.json')[0]
    ck('no_new_technology_findings',oldtech['findings']==newtech['findings'])
    ck('all_technology_grants_identical',oldtech['technologies']==newtech['technologies'])
    for sid in SIDS:
        recs=[r for r in newtech['buildings'] if r['state']==sid and r['building']==KIND]
        ck('new_fort_compatible.'+sid,len(recs)==1 and not recs[0]['construction_missing'] and all(not v for v in recs[0]['PM_missing'].values()))
    # Explicit exclusions: no world-map patch, future walls, standing regional armies, or Crete additions.
    ck('all_functional_outputs_are_new_files',all(e['before'] is None for e in load('FILES_MODIFIED.json')))
    ck('Crete_not_referenced',all('STATE_CRETE' not in t for t in files().values()))
    dump('CONCURRENT_CHANGES.json',{'entry_to_apply_observed':entry_changes,'postapply_changes':changes,'Git_writes':0,'SERG_writes':0,'vanilla_writes':0,'old_baseline_restored':False})
    dump('POPULATION_LEDGER.json',{'world_before':before['inventory']['world_population'],'world_after':now['world_population'],'world_delta':now['world_population']-before['inventory']['world_population'],'regional_before':before['population'],'regional_after':population(),'transfers':[]})
    dump('CAPACITY.json',{'levels':2,'employment_capacity':{'soldiers':1800,'officers':200},'weekly_goods_at_full_employment':{'small_arms':10,'iron':10},'recipe_per_level':recipe,'actual_employment_observed':False,'two_PMs_unscaled_strait_control':'Existing native regional effect; no new strait connection or physical site placement','new_civil_politicians':1,'new_combat_units':0})
    dump('STARTING_TECH_CHECK.json',{'TUR_before':oldtech['status'],'TUR_after':newtech['status'],'unchanged_findings':newtech['findings']==oldtech['findings'],'technologies':newtech['technologies'],'installed_fortifications_gates_satisfied':True,'regional_T_criterion':'PARTIAL_NO_CREDIT_CRETE_OUTSIDE_SCOPE','engine_tested':False})
    passed=sum(c['passed'] for c in checks);dump('VALIDATION.json',{'status':'PASS' if passed==len(checks) else 'FAIL','passed':passed,'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_validation':False})
    print(json.dumps({'passed':passed,'total':len(checks),'failed':[c['check'] for c in checks if not c['passed']]}));return passed==len(checks)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true');args=p.parse_args()
    if args.apply:apply()
    elif args.validate:raise SystemExit(0 if validate() else 1)
    else:p.print_help()
