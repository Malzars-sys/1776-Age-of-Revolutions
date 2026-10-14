"""Explicit MAP-2B transforms. Produces an apply_patch payload, not gameplay writes."""
import json, difflib, math, collections, re
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2a_patch import edits
from map_1776_audit import effective, values
ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2B'
MOVES=[('STATE_SOUTH_TYROL','VEN','AUS','xD0BF60'),('STATE_SOUTH_TYROL','VEN','AUS','x1120FF'),
       ('STATE_ISTRIA','VEN','AUS','x3060BF'),('STATE_ISTRIA','VEN','AUS','xF0A040'),
       ('STATE_LOMBARDY','AUS','VEN','x4713EE'),('STATE_PROVENCE','FRA','PAP','xB0C0E0')]
def state(raw,sid):
    match=re.search(r'\bs:'+re.escape(sid)+r'\s*=\s*\{',raw)
    if not match: raise StopIteration(sid)
    start=match.start(); pos=match.end(); depth=1; quote=False; comment=False
    while depth:
        char=raw[pos]; pos+=1
        if char=='\n': comment=False
        if comment: continue
        if char=='"': quote=not quote
        if quote: continue
        if char=='#': comment=True
        elif char=='{': depth+=1
        elif char=='}': depth-=1
    node=cw.parse(raw[start:pos])[0]
    for n in cw.walk([node]): n.start+=start; n.end+=start
    return node
def region(raw,sid,tag): return next(n for n in state(raw,sid).children() if n.key=='region_state:'+tag)
def append(raw,sid,tag,content):
    try: s=state(raw,sid)
    except StopIteration:
        at=raw.rfind('}'); return edits(raw,[(at,at,'\n\ts:'+sid+' = {\n\t\tregion_state:'+tag+' = {\n'+content+'\n\t\t}\n\t}\n')])
    rs=s.children('region_state:'+tag)
    if rs: return edits(raw,[(rs[0].end-1,rs[0].end-1,'\n'+content+'\n\t\t')])
    return edits(raw,[(s.end-1,s.end-1,'\n\t\tregion_state:'+tag+' = {\n'+content+'\n\t\t}\n\t')])
def relocate_owners(raw):
    for sid,old,new,rgb in MOVES:
        s=state(raw,sid)
        src=next(n for n in s.children('create_state') if n.one('country')=='c:'+old)
        own=src.children('owned_provinces')[0]
        assert rgb in values(src,'owned_provinces')
        raw=edits(raw,[(own.start,own.end,raw[own.start:own.end].replace(' '+rgb,''))])
        s=state(raw,sid)
        targets=[n for n in s.children('create_state') if n.one('country')=='c:'+new]
        if targets:
            own=targets[0].children('owned_provinces')[0]
            raw=edits(raw,[(own.end-1,own.end-1,rgb+' ')])
        else:
            raw=edits(raw,[(s.end-1,s.end-1,'\n\t\t# MAP-2B: existing-province approximation; see report.\n\t\tcreate_state = { country = c:'+new+' owned_provinces = { '+rgb+' } }\n\t')])
    s=state(raw,'STATE_SOUTH_TYROL')
    old=next(n for n in s.children('create_state') if n.one('country')=='c:VEN')
    assert not values(old,'owned_provinces')
    return edits(raw,[(old.start,old.end,'')])
def transfer_pops(raw,sid,old,new,amounts=None):
    src=region(raw,sid,old); operations=[]; moved=[]
    for p in src.children('create_pop'):
        amount=int(p.one('size')) if amounts is None else amounts.get((p.one('culture'),p.one('religion')),0)
        if not amount: continue
        count=int(p.one('size')); assert 0<amount<=count
        sn=p.children('size')[0]; frag=raw[p.start:p.end]
        moved.append('\t\t\t'+edits(frag,[(sn.start-p.start,sn.end-p.start,'size = '+str(amount))]))
        operations.append((p.start,p.end,'') if amount==count else (sn.start,sn.end,'size = '+str(count-amount)))
    raw=edits(raw,operations)
    raw=append(raw,sid,new,'\n'.join(moved))
    if amounts is None:
        src=region(raw,sid,old); assert not src.children('create_pop')
        raw=edits(raw,[(src.start,src.end,'')])
    return raw
def move_building(raw,sid,old,new,kind,amount=None,choose=0):
    if 's:'+sid not in raw: return raw
    try: src=region(raw,sid,old)
    except StopIteration: return raw
    matches=[b for b in src.children('create_building') if cw.scalar(b.one('building'))==kind]
    if not matches: return raw
    b=matches[choose]; fragment=raw[b.start:b.end]
    levels=[n for n in cw.walk(b.children()) if n.key=='levels']
    if amount is None:
        raw=edits(raw,[(b.start,b.end,'')])
    else:
        assert len(levels)==1
        count=int(levels[0].value); assert 0<amount<count
        lv=levels[0]
        fragment=edits(fragment,[(lv.start-b.start,lv.end-b.start,'levels = '+str(amount))])
        raw=edits(raw,[(lv.start,lv.end,'levels = '+str(count-amount))])
    # Preserve economic owners (including foreign governments/investors) and PMs.
    return append(raw,sid,new,'\t\t\t'+fragment)
def map_transform(originals):
    result=dict(originals)
    p='common/history/states/00_states.txt'; result[p]=relocate_owners(result[p])
    p='common/history/pops/00_west_europe.txt'; raw=result[p]
    raw=transfer_pops(raw,'STATE_SOUTH_TYROL','VEN','AUS')
    raw=raw.replace('# Temporary split by owned provinces (AUS 2/4); regional totals unchanged.',
                    '# MAP-2B: retained regional population; AUS is also the gameplay proxy for the imperial bishoprics.')
    raw=transfer_pops(raw,'STATE_PROVENCE','FRA','PAP',{('occitan',None):96000,('french',None):2000,('sephardic',None):1500})
    result[p]=raw
    p='common/history/pops/01_south_europe.txt'; raw=result[p]
    raw=transfer_pops(raw,'STATE_ISTRIA','VEN','AUS',{('north_italian',None):40000,('hungarian',None):500,('slovene',None):140000,('south_german',None):6000,('croat',None):40000})
    raw=raw.replace('# Temporary split by owned provinces (AUS 1/6); regional totals unchanged.',
                    '# MAP-2B: qualitative littoral/interior allocation, not a 1776 census or province-count apportionment.')
    raw=transfer_pops(raw,'STATE_LOMBARDY','AUS','VEN',{('north_italian',None):350000,('north_italian','jewish'):58})
    result[p]=raw
    for p in result:
        if '/buildings/' not in p: continue
        raw=result[p]
        if 's:STATE_SOUTH_TYROL' in raw:
            try:
                r=region(raw,'STATE_SOUTH_TYROL','VEN')
                raw=edits(raw,[(r.start,r.start+len(r.key),'region_state:AUS')])
                # VEN no longer has a state here; retain foreign owners in Venetia.
                s=state(raw,'STATE_SOUTH_TYROL'); ops=[]
                for b in cw.walk(s.children()):
                    if b.key=='building' and isinstance(b.value,list) and cw.scalar(b.one('country'))=='c:VEN':
                        q=b.children('region')[0]; ops.append((q.start,q.end,'region = "STATE_VENETIA"'))
                raw=edits(raw,ops)
            except StopIteration: pass
        raw=move_building(raw,'STATE_LOMBARDY','AUS','VEN','building_vineyard')
        raw=move_building(raw,'STATE_LOMBARDY','AUS','VEN','building_silk_plantation',1)
        raw=move_building(raw,'STATE_PROVENCE','FRA','PAP','building_food_industry')
        # Northern Adriatic port and fishing activity: no new levels, not a nationalisation.
        raw=move_building(raw,'STATE_ISTRIA','VEN','AUS','building_port',2)
        raw=move_building(raw,'STATE_ISTRIA','VEN','AUS','building_fishing_wharf',2)
        raw=move_building(raw,'STATE_ISTRIA','VEN','AUS','building_trade_center',1)
        # Move the government-owned shipyard, not the privately-owned one.
        try:
            rs=region(raw,'STATE_ISTRIA','VEN')
            bs=[b for b in rs.children('create_building') if cw.scalar(b.one('building'))=='building_shipyard']
            chosen=next((i for i,b in enumerate(bs) if b.children('add_ownership')[0].children('country')),None)
            if chosen is not None: raw=move_building(raw,'STATE_ISTRIA','VEN','AUS','building_shipyard',choose=chosen)
        except StopIteration: pass
        result[p]=raw
    p='common/history/military_formations/00_military_formations_europe.txt'; raw=result[p]
    ven=next(n for n in cw.walk(cw.parse(raw)) if n.key=='c:VEN')
    ops=[(n.start,n.end,'state_region = s:STATE_LOMBARDY') for n in cw.walk(ven.children()) if n.key=='state_region' and cw.scalar(n.value)=='s:STATE_SOUTH_TYROL']
    assert len(ops)==1
    result[p]=edits(raw,ops)
    return result
def rail_commands(originals,sid,tag):
    found=[]
    for p,raw in originals.items():
        if '/buildings/' not in p or 's:'+sid not in raw: continue
        try: r=region(raw,sid,tag)
        except StopIteration: continue
        found.extend((p,b) for b in r.children('create_building') if cw.scalar(b.one('building'))=='building_railway')
    return found
def levels(b): return sum(int(n.value) for n in cw.walk(b.children()) if n.key in ('levels','level'))
def methods(b): return [cw.scalar(n.value) for q in b.children('activate_production_methods') for n in q.children()]
def pm_fixed(pm,defs):
    return sum(float(n.value) for q in defs[pm].children('state_modifiers') for n in cw.walk(q.children()) if n.key=='state_infrastructure_add')
def infrastructure_plan(originals):
    import validate_wallonia_start_1776 as w
    data=json.loads((w.OUT/'SAVE_DIAGNOSIS.json').read_text(encoding='utf-8'))
    pmdefs=w.catalog('common/production_methods')
    traits=w.catalog('common/state_traits'); regions=w.catalog('map_data/state_regions')
    plans=[]
    for s in data['deficit_states']:
        sid=s['region']; tag=s['country']; bs=s['regional_infrastructure']; assert len(bs)<=1
        old=bs[0]['levels'] if bs else 0; staff=bs[0]['staffing'] if bs else 0
        loaded=bs[0]['pms'] if bs else ['pm_traditional_road_network','pm_no_canal_network','pm_no_rail_network','pm_no_passenger_trains']
        road=next(p for p in loaded if p in ('pm_traditional_road_network','pm_turnpike_road_network','pm_engineered_road_network','pm_paved_road_network'))
        commands=rail_commands(originals,sid,tag)
        existing=max([levels(b) for _,b in commands]+[0])
        histfixed=max([sum(pm_fixed(p,pmdefs) for p in methods(b)) for _,b in commands]+[3])
        if tag=='BEO' and sid=='STATE_WALLONIA':
            # The supplied save predates the already-applied Wallonia correction.
            # Its cache includes 6 old canal outputs even though active PMs do not.
            earlier=json.loads((w.OUT/'BASELINE.json').read_text(encoding='utf-8'))['originals']
            histfixed=max(sum(pm_fixed(p,pmdefs) for p in methods(b)) for _,b in rail_commands(earlier,sid,tag))
        activefixed=sum(pm_fixed(p,pmdefs) for p in loaded)
        # Conservative marginal multiplier: retain terrain/unincorporated penalties;
        # never extrapolate positive population/port bonuses into new road levels.
        factor=min(1.0,s['serialized_infrastructure_cache']/(3+histfixed*staff))
        trait_penalty=sum(float(n.value) for t in values(regions[sid],'traits') if t in traits for n in cw.walk(traits[t].children()) if n.key=='state_infrastructure_mult')
        factor=min(factor,max(.05,1+trait_penalty))
        current=s['serialized_infrastructure_cache']-factor*max(0,histfixed-activefixed)*staff
        if tag=='BEO' and sid=='STATE_WALLONIA':
            current=23.1  # Observed initial UI reconstruction, without stale canals.
        # Current canals do not occur in the 69 loaded rows. Never budget unavailable canals.
        assert all(p not in loaded for p in ['pm_industrial_canals','pm_engineered_canals'])
        per=pm_fixed(road,pmdefs)
        reserve=2.0
        new=max(existing,int(math.ceil((s['serialized_usage']+reserve-current+factor*per*staff-.1*old)/(factor*per-.1))))
        usage=s['serialized_usage']+.1*max(0,new-old)
        supply=current+factor*per*(new-staff)
        if tag=='BRZ' and sid=='STATE_RIO_DE_JANEIRO':
            # February native observation supersedes its transient January cache.
            # Three fully staffed basic ports supply 9, base supplies 3; road
            # staffing 19.93299 supplies 59.79897, exactly the observed 71.79897.
            month=json.loads((OUT/'OBSERVATEUR_3_COMPARISON.json').read_text(encoding='utf-8'))
            native=next(r['month'] for r in month['comparison_69'] if r['country']==tag and r['region']==sid)
            assert abs(native['infrastructure']-3*native['networks'][0]['staffing']-12)<1e-5
            new=existing; factor=1.0; current=12+per*staff
            usage=native['usage']-.1*(native['networks'][0]['levels']-new)
            supply=12+per*new
        assert supply>=usage+reserve-1e-6,(tag,sid,new,supply,usage)
        plans.append({'country':tag,'region':sid,'saved_levels':old,'saved_staffing':staff,'current_written_levels':existing,'new_levels':new,'road_pm':road,'saved_cache_delta':s['cache_delta'],'refreshed_baseline_estimate':round(current,5),'marginal_multiplier':round(factor,8),'usage_estimate':round(usage,5),'full_staffing_supply_estimate':round(supply,5),'reserve_estimate':round(supply-usage,5),'employment_warning':staff<old,'changed_startup_pm':s['controller_changed_pm_at_start'],'history_commands':len(commands)})
    assert len(plans)==69
    return plans
def set_rail(raw,sid,tag,new,road):
    if 's:'+sid not in raw: return raw,False
    try: r=region(raw,sid,tag)
    except StopIteration: return raw,False
    bs=[b for b in r.children('create_building') if cw.scalar(b.one('building'))=='building_railway']
    if not bs: return raw,False
    assert len(bs)==1
    b=bs[0]; ns=[n for n in cw.walk(b.children()) if n.key in ('level','levels')]; assert len(ns)==1
    pn=b.children('activate_production_methods')[0]
    ps='activate_production_methods = { "'+road+'" "pm_no_canal_network" "pm_no_rail_network" "pm_no_passenger_trains" }'
    return edits(raw,[(ns[0].start,ns[0].end,ns[0].key+' = '+str(new)),(pn.start,pn.end,ps)]),True
def new_rail(new,sid,tag,road):
    return '\t\t\t# MAP-2B: no-input sustainable capacity; wages still apply.\n\t\t\tcreate_building = {\n\t\t\t\tbuilding = "building_railway"\n\t\t\t\tadd_ownership = { country = { country = "c:'+tag+'" levels = '+str(new)+' } }\n\t\t\t\treserves = 1\n\t\t\t\tactivate_production_methods = { "'+road+'" "pm_no_canal_network" "pm_no_rail_network" "pm_no_passenger_trains" }\n\t\t\t}'
def all_transform(originals,plans):
    result=map_transform(originals)
    for row in plans:
        found=0
        for p in result:
            if '/buildings/' not in p: continue
            result[p],ok=set_rail(result[p],row['region'],row['country'],row['new_levels'],row['road_pm']); found+=ok
        if not found:
            p='common/history/buildings/98_build_start_1776_world_redistribution.txt'
            result[p]=append(result[p],row['region'],row['country'],new_rail(row['new_levels'],row['region'],row['country'],row['road_pm']))
    # New territorial subdivisions are outside the saved 69: small no-input road networks.
    p='common/history/buildings/98_build_start_1776_world_redistribution.txt'
    for sid,tag,n in [('STATE_SOUTH_TYROL','AUS',2),('STATE_PROVENCE','PAP',1),('STATE_LOMBARDY','VEN',2),('STATE_ISTRIA','AUS',2)]:
        assert not rail_commands(result,sid,tag)
        result[p]=append(result[p],sid,tag,new_rail(n,sid,tag,'pm_traditional_road_network'))
    return result
def main():
    base=json.loads((OUT/'MAP2B_BASELINE.json').read_text(encoding='utf-8'))
    originals=base['originals']; plans=infrastructure_plan(originals); result=all_transform(originals,plans)
    (OUT/'INFRASTRUCTURE_PLAN.json').write_text(json.dumps(plans,indent=2),encoding='utf-8')
    patch=['*** Begin Patch']; changed=[]
    for p in result:
        if result[p]==originals[p]: continue
        assert (ROOT/p).read_text(encoding='utf-8-sig')==originals[p], 'Concurrent edit: '+p
        changed.append(p); patch.append('*** Update File: '+p)
        for line in list(difflib.unified_diff(originals[p].splitlines(),result[p].splitlines(),n=18))[2:]:
            patch.append('@@' if line.startswith('@@') else line)
    patch.append('*** End Patch')
    print(json.dumps({'patch':'\n'.join(patch),'changed':changed,'states':len(plans),'extra_levels_actual':sum(p['new_levels']-p['current_written_levels'] for p in plans)}))
if __name__=='__main__': main()
