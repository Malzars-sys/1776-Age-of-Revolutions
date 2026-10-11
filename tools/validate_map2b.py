"""Independent totals/scope checks for the actual dirty-tree MAP-2B baseline."""
import collections as C, json, math
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
import map2b_patch as plan
ROOT=qa.ROOT; OUT=plan.OUT
def weighted_buildings(inv,exclude_rail=False):
    totals=C.Counter()
    for row in inv['buildings']:
        sid,tag,signature=row['key']; node=json.loads(signature)
        kind=next(v[2] for v in node[2] if v[0]=='building')
        if exclude_rail and kind=='building_railway': continue
        pms=tuple(sorted(v[2] for n in node[2] if n[0]=='activate_production_methods' for v in n[2]))
        owners=[v for n in node[2] if n[0]=='add_ownership' for v in n[2]]
        for owner in owners:
            attrs={v[0]:v[2] for v in owner[2]}
            # Economic location can legitimately move from extinct VEN/South Tyrol
            # to VEN/Venetia; country and ownership vehicle/levels must not change.
            totals[(kind,pms,owner[0],attrs.get('type',''),str(attrs.get('country','')),str(next((v[2] for v in node[2] if v[0]=='reserves'),'')))]+=int(attrs['levels'])*row['count']
        for v in node[2]:
            if v[0]=='level': totals[(kind,pms,'root_level','','','')]+=int(v[2])*row['count']
    return totals
def army(inv):
    out=C.Counter()
    for row in inv['units']:
        tag,form,sid,sig=row['key']; n=json.loads(sig); attrs={v[0]:v[2] for v in n[2]}
        out[(tag,attrs['type'],attrs.get('service_type','regular'))]+=int(attrs['count'])*row['count']
    return out
def run():
    base=json.loads((OUT/'MAP2B_BASELINE.json').read_text(encoding='utf-8'))
    before=base['inventory']; after=qa.inventory()
    plans=json.loads((OUT/'INFRASTRUCTURE_PLAN.json').read_text(encoding='utf-8'))
    intended=plan.all_transform(base['originals'],plans)
    changed=[]
    for path,raw in base['originals'].items():
        actual=(ROOT/path).read_text(encoding='utf-8-sig')
        assert [qa.norm(n) for n in cw.parse(actual)]==[qa.norm(n) for n in cw.parse(intended[path])], 'Unplanned edit: '+path
        if qa.sha(ROOT/path)!=base['hashes'][path]: changed.append(path)
    assert len(changed)==18
    assert all(qa.sha(ROOT/p)==sha for p,sha in base['hashes'].items() if p not in changed), 'Unrelated protected file changed'
    a,b=qa.counter(before['owners']),qa.counter(after['owners']); expected=a.copy()
    for sid,old,new,rgb in plan.MOVES:
        assert expected[(rgb,sid,old)]==1
        del expected[(rgb,sid,old)]; expected[(rgb,sid,new)]+=1
    assert +expected==b
    assert {r[0] for r in a}=={r[0] for r in b}
    assert before['geometry']==after['geometry']
    assert before['duplicates']==after['duplicates']
    assert before['pops']==after['pops']
    assert before['resolved_demographics']==after['resolved_demographics']
    rp_before=qa.counter(before['regional_pop']); rp_after=qa.counter(after['regional_pop'])
    def regional(counter):
        totals=C.Counter()
        for (sid,owner,cu,rel),n in counter.items(): totals[(sid,cu,rel)]+=n
        return totals
    assert regional(rp_before)==regional(rp_after)
    assert weighted_buildings(before,True)==weighted_buildings(after,True), 'Non-infrastructure levels/PMs/economic owners changed'
    assert army(before)==army(after)
    assert before['countries']==after['countries']
    assert not set(map(str,after['errors']))-set(map(str,before['errors']))
    pairs=set(map(tuple,before['states'])); pairs.remove(('STATE_SOUTH_TYROL','VEN')); pairs.add(('STATE_PROVENCE','PAP'))
    assert pairs==set(map(tuple,after['states']))
    for k,v in before['state_types'].items():
        if k!='STATE_SOUTH_TYROL|VEN': assert after['state_types'][k]==v
    for rgb,sid,tag in [('xD001A0','STATE_WALLONIA','BEO'),('x9AC196','STATE_LOMBARDY','SWI'),('x867A90','STATE_LOMBARDY','VEN'),('x71E080','STATE_MORAVIA','AUS'),('xF0E080','STATE_MORAVIA','AUS'),('x9061E0','STATE_WEST_GALICIA','AUS')]:
        assert b[(rgb,sid,tag)]==1
    # Wallonia's complete demographic and non-rail content is unchanged.
    assert {k:v for k,v in rp_before.items() if k[0]=='STATE_WALLONIA'}=={k:v for k,v in rp_after.items() if k[0]=='STATE_WALLONIA'}
    assert sum(v for k,v in rp_after.items() if k[0]=='STATE_WALLONIA' and k[1]=='BEO')==1099399
    pmdefs=cw.effective('common/production_methods')
    gbr=next(n for n in cw.walk(cw.parse((ROOT/'common/history/countries/gbr - great britain.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:GBR')
    assert 'turnpike_road_networks' in [n.value for n in gbr.children('add_technology_researched')]
    for row in plans:
        bs=plan.rail_commands({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in changed if '/buildings/' in p},row['region'],row['country'])
        assert bs and all(plan.levels(b)==row['new_levels'] and plan.methods(b)==[row['road_pm'],'pm_no_canal_network','pm_no_rail_network','pm_no_passenger_trains'] for _,b in bs)
        assert row['new_levels']>=row['current_written_levels']
        assert row['reserve_estimate']>=2-1e-5
        if row['road_pm']!='pm_traditional_road_network': assert row['country']=='GBR'
    assert len(plans)==69
    old_levels=qa.counter(before['building_levels_written']); new_levels=qa.counter(after['building_levels_written'])
    delta=new_levels-old_levels
    assert set(k[0] if isinstance(k,tuple) else k for k in delta)=={'building_railway'}
    population=[]
    target={x[0] for x in plan.MOVES}
    for key in sorted(set(rp_before)|set(rp_after)):
        if key[0] in target:
            population.append(list(key)+[rp_before[key],rp_after[key],rp_after[key]-rp_before[key]])
    # Existing fixtures execute parsed scripts, not the native game.
    import validate_regional_infrastructure_shortage as infra
    scenario=infra.model_tests()
    cw.implementation_checks(); cw.model_tests()
    # The old administration test freezes entire building files against a62be0b,
    # including unrelated Lombardy. Run it, record its scope conflict explicitly,
    # then check Ottoman administration commands against the actual turn baseline.
    try:
        cw.ottoman_admin_building_checks()
        legacy_admin='PASS'
    except AssertionError as exc:
        assert str(exc).startswith('Other buildings, owners, reserves or PM changed:')
        legacy_admin='OLD_WHOLE_FILE_GUARD_NOT_APPLICABLE: '+str(exc)
    admin_before=[]; admin_after=[]
    for path in base['originals']:
        if '/buildings/' not in path: continue
        for dest,raw in [(admin_before,base['originals'][path]),(admin_after,(ROOT/path).read_text(encoding='utf-8-sig'))]:
            for s in cw.walk(cw.parse(raw)):
                if not s.key.startswith('s:STATE_'): continue
                for r in s.children('region_state:TUR'):
                    for n in r.children('create_building'):
                        if cw.scalar(n.one('building'))=='building_government_administration': dest.append((path,s.key,qa.signature(n)))
    assert admin_before==admin_after
    extra=sum(s['new_levels']-s['current_written_levels'] for s in plans)
    result={'result':'PASS_STATIC','territorial_provinces_changed':len(plan.MOVES),'territorial_state_regions':sorted(target),'countries_territorial':['AUS','VEN','FRA','PAP'],
            'population_before':sum(r['count'] for r in before['pops']),'population_after':sum(r['count'] for r in after['pops']),
            'culture_religion_totals':'EXACTLY_CONSERVED','regional_culture_religion_totals':'EXACTLY_CONSERVED',
            'non_infrastructure_building_levels_pms_owners':'EXACTLY_CONSERVED','military_units_before':sum(army(before).values()),'military_units_after':sum(army(after).values()),
            'military_recruitment_selectors_relocated':1,'duplicates_before':len(before['duplicates']),'duplicates_after':len(after['duplicates']),'new_duplicates':0,'duplicates_in_MAP2B_scope':0,
            'old_critical_reference_errors':before['errors'],'new_critical_reference_errors':[],
            'MAP2A_and_LUX':'PRESERVED','geometry_and_country_definitions':'UNCHANGED','protected_files_unchanged':len(base['hashes'])-len(changed),
            'changed_gameplay_files':sorted(changed),'infrastructure_states_adjusted':69,'infrastructure_levels_added_to_69_current_histories':extra,
            'territorial_dependency_infrastructure_levels_added':7,'additional_railway_levels_written_including_overlays':sum(delta.values()),
            'projected_full_staffing_minimum_reserve':min(s['reserve_estimate'] for s in plans),'understaffed_saved_networks':sum(s['employment_warning'] for s in plans),
            'retained_turnpike_networks':[(s['country'],s['region']) for s in plans if s['road_pm']=='pm_turnpike_road_network'],
            'infra_AST_scenarios_passed':len(scenario),'ottoman_AST_checks':'PASS','ottoman_administrations_against_actual_MAP2B_baseline':'PASS',
            'old_ottoman_administration_guard':legacy_admin,'commit_merge_push':'NOT_PERFORMED',
            'native_new_game':'USER_TESTED; observed via observateur_3 dated 1776.2.1, not an independently operated UI session',
            'native_one_month':'OBSERVED_USER_SAVE; 59/69 original deficits now nonnegative, 10 remain; 17 negative states worldwide',
            'projection_limits':'Saved caches can precede startup PM changes. Marginal multipliers are conservative estimates, not newly measured engine modifiers. Full staffing is assumed; eight saved networks were under-employed. No guarantee of day-one access or budget.'}
    month=json.loads((OUT/'OBSERVATEUR_3_COMPARISON.json').read_text(encoding='utf-8'))
    assert month['game_date']=='1776.2.1' and month['contains_MAP2B_history']
    result['native_save_evidence']={k:month[k] for k in ['source_save','source_sha256','game_date','patch_markers','original_69_history_level_matches','preliminary_69_history_level_matches','original_69_still_negative','negative_month_cache_balances','wallonia']}
    result['native_validation_limit']='68 of 69 preliminary infrastructure targets load at the planned level; East Prussia is 1 instead of 3. Rio was subsequently reduced from 33 to the original 8 using native port/road measurements; this final refinement is not tested in this save. Nine remaining original deficit networks are understaffed; none of the ten has full staffed target capacity loaded.'
    (OUT/'MAP2B_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'TABLE_DATA.json').write_text(json.dumps({'population':population,'infrastructure':plans},ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': run()
