"""Two administrative Floridas, preserving current sovereignty and all old assets.

Whole-province Apalachicola approximation; British MS/AL coast joins West Florida.
--prepare stages a bounded patch; --apply guards current hashes; --validate rereads.
No new country, Git operation, vanilla mutation or automatic annexation.
"""
import collections as C
import json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,ownership,state_nodes,rgb_block
from hbc03_quebec_arc import economic_inventory,conservation,canonical
from hbc02_map_candidates import graph
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from r8_south_geometry import bitmap,load
from r8_south_correct import allocate,pop_signature,components
from georeference.model import forward,inverse

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/FLORIDA-01'
PRIOR=OUT.parent/'R8-CORRECTIONS-01'
EAST='STATE_FLORIDA';WEST='STATE_WEST_FLORIDA'
SOURCES={EAST,'STATE_ALABAMA','STATE_MISSISSIPPI'}
ST='common/history/states/00_states.txt';PP='common/history/pops/05_north_america.txt'
REG='map_data/state_regions/05_north_america.txt'


def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def source(rel):return ROOT/rel if (ROOT/rel).exists() else GAME/rel
def values(raw):return {n.key:n for n in parse(raw) if n.key.startswith('STATE_')}


def cohort_totals(raw,regions):
    out=C.Counter()
    for sid,s in state_nodes(raw).items():
        if sid in regions:
            for rs in s.children():
                if rs.key.startswith('region_state:'):
                    for p in rs.children('create_pop'):out[rs.key,pop_signature(p)]+=int(p.one('size'))
    return sorted([[t,k,v] for (t,k),v in out.items()])


def capacities(regions):
    counts=C.Counter()
    for s in regions:
        counts['arable_land']+=int(s.one('arable_land',0))
        for c in s.children('capped_resources'):
            for n in c.children():counts['capped:'+n.key]+=int(n.value)
        for r in s.children('resource'):
            for key in ['discovered_amount','undiscovered_amount']:
                counts['resource:'+scalar(r.one('type'))+':'+key]+=int(r.one(key,0))
    return dict(counts)


def broaden(raw):
    """Widen Florida predicates/effects, retaining representative saved scopes.

    A sale transfers every seller-owned share in either Florida, never natives.
    Seminole-specific journal intentionally remains East-Florida-specific.
    """
    def rewrite(n):
        part=raw[n.start:n.end]
        changes=[(c.start-n.start,c.end-n.start,rewrite(c)) for c in n.children()]
        for a,b,s in sorted(changes,reverse=True):part=part[:a]+s+part[b:]
        if not isinstance(n.value,list):
            if n.key=='state_region' and scalar(n.value)=='s:'+EAST:
                return 'OR = { state_region = s:'+EAST+' state_region = s:'+WEST+' }'
            if n.key=='has_state_in_state_region' and scalar(n.value)==EAST:
                return 'OR = { has_state_in_state_region = '+EAST+' has_state_in_state_region = '+WEST+' }'
            if n.key=='owns_entire_state_region' and scalar(n.value)==EAST:
                return 'AND = { owns_entire_state_region = '+EAST+' owns_entire_state_region = '+WEST+' }'
        elif n.key=='s:'+EAST:
            sibling=part.replace('s:'+EAST,'s:'+WEST,1)
            if n.children('add_claim') or n.children('remove_claim'):return part+'\n'+sibling
            if n.children('any_scope_state'):
                all_states=any(scalar(v.value)=='all' for v in walk(n.children()) if v.key=='count')
                return ('AND' if all_states else 'OR')+' = {\n'+part+'\n'+sibling+'\n}'
        if n.key=='random_state' and any(v.key=='set_state_owner' for v in walk(n.children())):
            part=part.replace('random_state','every_state',1)
        return part
    return edit(raw,[(n.start,n.end,rewrite(n)) for n in parse(raw)])


def exclude_buyer(raw,object_key):
    obj=next(n for n in parse(raw) if n.key==object_key)
    owner=obj.children('immediate')[0].children('random_state')[0].children('limit')[0].children('owner')[0]
    return edit(raw,[(owner.end-1,owner.end-1,'\n NOT = { this = root }\n NOT = { is_subject_of = root }\n')])


def prepare():
    OUT.mkdir(exist_ok=True);assert not (OUT/'APPLIED.json').exists()
    base=runtime();own=ownership();a=bitmap();raw=text(ROOT/REG);regions=values(raw);fl=set(provs(regions[EAST],'provinces'))
    all_defs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))}
    assert WEST not in all_defs
    new_id=max(int(n.one('id',0)) for n in all_defs.values())+1
    model=load(PRIOR/'GEODETIC_MODEL.json')
    # Natural Earth combines the lower Apalachicola with Chattahoochee by name.
    rivers=load(ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson')
    river=np.array([p for f in rivers['features'] if f['properties'].get('name') in ['Apalachicola','Chattahoochee'] and f['geometry']['type']=='LineString' for p in f['geometry']['coordinates'] if 29.7<p[1]<31.1])
    assert len(river)>40;river=river[np.argsort(river[:,1])]
    rows=[];western=set()
    for r in sorted(fl):
        y,x=np.where(a==int(r[1:],16));center=[float(x.mean()),float(y.mean())];lon,lat=map(float,inverse(model,[center])[0])
        limit=float(np.interp(lat,river[:,1],river[:,0]));west=lon<limit
        if west:western.add(r)
        rows.append(dict(rgb=r,before=EAST,after=WEST if west else EAST,owner=next(iter(own[r]))[1],geo_proxy=[lon,lat],river_longitude=limit))
    assert western and western<fl and all(own[r]=={(EAST,'GBR')} for r in western)
    # The new British coast installed by R8 is part of West Florida, not annexed again.
    for r,v in own.items():
        if any(s in SOURCES-{EAST} and t=='GBR' for s,t in v):
            assert len(v)==1;sid,t=next(iter(v));western.add(r);rows.append(dict(rgb=r,before=sid,after=WEST,owner=t,reason='Existing British Mobile/Biloxi coast; owner unchanged'))
    eastern=fl-western
    assert len(western)==9 and len(eastern)==29
    # Snap requested seats to current land, never trust a projected point in the sea.
    hubs={};hproof=[]
    geo={'city':[-87.2169,30.4213],'port':[-87.2169,30.4213],'farm':[-85.4,30.82],'mine':[-87.27,30.75],'wood':[-86.98,30.75]}
    for side,cells in [(WEST,western),(EAST,eastern)]:
        y,x=np.where(np.isin(a,[int(r[1:],16) for r in cells]))
        for kind in (['city','port'] if side==EAST else geo):
            target_geo=[-81.3145,29.8947] if side==EAST else geo[kind]
            p=forward(model,[target_geo])[0];i=int(np.argmin((x-p[0])**2+(y-p[1])**2));px=[int(x[i]),int(y[i])]
            if kind=='city':
                # Place city a little inland in the same province as its port.
                candidate=[px[0] if side==WEST else px[0]-2,px[1]-2 if side==WEST else px[1]]
                if a[candidate[1],candidate[0]]==a[px[1],px[0]]:px=candidate
            rgb=f'x{int(a[px[1],px[0]]):06X}';assert rgb in cells
            hubs[side,kind]=dict(rgb=rgb,pixel=px)
            hproof.append(dict(state=side,kind=kind,geo=target_geo,projected_pixel=p.tolist(),chosen_pixel=px,rgb=rgb,snap_distance_px=float(np.linalg.norm(p-px)),precision='EMPIRICAL_HUB_APPROXIMATION_NOT_SURVEYED'))
    files={};patch=[];new_caps=C.Counter();new_resources=C.Counter();arable=set();moved_counts=C.Counter(r['before'] for r in rows if r['after']==WEST)
    for sid in SOURCES:
        n=regions[sid];cells=set(provs(n,'provinces'));moved=cells&western
        assert moved
        node=n.children('provinces')[0];patch.append((node.start,node.end,'provinces = '+rgb_block(cells-moved)))
        weights={'old':len(cells-moved),'west':len(moved)}
        for key in ['arable_land']:
            node=n.children(key)[0];nums=allocate(int(node.value),weights);new_caps[key]+=nums['west'];patch.append((node.start,node.end,key+' = '+str(nums['old'])))
        arable.update(provs(n,'arable_resources'))
        for group in n.children('capped_resources'):
            for node in group.children():
                # Bone Valley phosphate remains in the peninsula; do not duplicate its field.
                take=0 if sid==EAST and node.key=='building_phosphate_mine' else allocate(int(node.value),weights)['west']
                new_caps[node.key]+=take;patch.append((node.start,node.end,node.key+' = '+str(int(node.value)-take)))
        for res in n.children('resource'):
            kind=scalar(res.one('type'))
            for key in ['discovered_amount','undiscovered_amount']:
                for node in res.children(key):
                    take=0 if sid==EAST and kind=='building_bauxite_mine' else allocate(int(node.value),weights)['west']
                    new_resources[kind,key]+=take;patch.append((node.start,node.end,node.key+' = '+str(int(node.value)-take)))
        if sid==EAST:
            for key in ['city','port','naval_exit_id']:
                node=n.children(key)[0];val='3146' if key=='naval_exit_id' else '"'+hubs[EAST,key]['rgb']+'"';patch.append((node.start,node.end,key+' = '+val))
        else:
            # Their entire British littoral now belongs to West Florida.
            # No built port is removed; these old hub/exit slots become inland.
            assert scalar(n.one('port')) in western
            for key in ['port','naval_exit_id']:
                for node in n.children(key):patch.append((node.start,node.end,''))
    new=[WEST+' = {',f' id = {new_id}',' subsistence_building = "building_subsistence_farm"',' provinces = '+rgb_block(western),' traits = { "state_trait_floridian_wetlands" }']
    new += [f' {k} = "{hubs[WEST,k]["rgb"]}"' for k in geo]
    new += [' arable_land = '+str(new_caps.pop('arable_land')),' arable_resources = { '+' '.join(sorted(arable))+' }',' capped_resources = { '+' '.join(k+' = '+str(v) for k,v in sorted(new_caps.items()) if v)+' }']
    for (kind,key),amount in sorted(new_resources.items()):
        if amount:new.append(f' resource = {{ type = "{kind}" {key} = {amount} }}')
    new+=[' naval_exit_id = 3060','}']
    final=edit(raw,patch)+'\n'+'\n'.join(new)+'\n';files[REG]=encoded(ROOT/REG,final)
    assert capacities([regions[s] for s in SOURCES])==capacities([values(final)[s] for s in SOURCES|{WEST}])
    raw=text(ROOT/ST);patch=[]
    for sid,s in state_nodes(raw).items():
        if sid not in SOURCES:continue
        for n in s.children('create_state'):
            if scalar(n.one('country'))!='c:GBR':continue
            node=n.children('owned_provinces')[0];left=set(provs(n,'owned_provinces'))-western
            if left:patch.append((node.start,node.end,'owned_provinces = '+rgb_block(left)))
            else:patch.append((n.start,n.end,''))
    new='\n s:'+WEST+' = {\n  create_state = { country = c:GBR owned_provinces = '+rgb_block(western)+' state_type = unincorporated }\n  add_claim = c:SPA\n  add_homeland = cu:muskogean\n }\n'
    root=parse(raw)[0];files[ST]=encoded(ROOT/ST,edit(raw,patch+[(root.end-1,root.end-1,new)]))
    raw=text(ROOT/PP);patch=[];bodies=[]
    for sid,s in state_nodes(raw).items():
        if sid not in SOURCES:continue
        rs=s.children('region_state:GBR');assert len(rs)==1
        rs=rs[0]
        if sid!=EAST:
            assert all(n.key=='create_pop' for n in rs.children());bodies += [raw[n.start:n.end] for n in rs.children('create_pop')];patch.append((rs.start,rs.end,''))
        else:
            for n in rs.children('create_pop'):
                east_british=sum(own[r]=={(EAST,'GBR')} for r in eastern)
                size=n.children('size')[0];nums=allocate(int(size.value),{'east':east_british,'west':len(fl-eastern)})
                patch.append((size.start,size.end,'size = '+str(nums['east'])))
                body=raw[n.start:n.end];body=body[:size.start-n.start]+'size = '+str(nums['west'])+body[size.end-n.start:];bodies.append(body)
    root=parse(raw)[0];new='\n s:'+WEST+' = { region_state:GBR = {\n'+'\n'.join(bodies)+'\n } }\n'
    files[PP]=encoded(ROOT/PP,edit(raw,patch+[(root.end-1,root.end-1,new)]))
    assert cohort_totals(raw,SOURCES)==cohort_totals(files[PP].decode('utf-8-sig'),SOURCES|{WEST})
    # Existing East Florida assets stay intact. Add one attested Pensacola port.
    rel='common/history/buildings/1776_florida_west_port.txt';assert not (ROOT/rel).exists()
    files[rel]=('BUILDINGS = { s:'+WEST+' = { region_state:GBR = { create_building = { building = "building_port" add_ownership = { country = { country = c:GBR levels = 1 } } reserves = 1 activate_production_methods = { "pm_basic_port" } } } } }\n').encode()
    # Six localizations and actual hubs, not two names attached to Tallahassee.
    for lang in ['french','english']:
        lines=['l_'+lang+':',f' {EAST}:0 "'+('Floride orientale' if lang=='french' else 'East Florida')+'"',f' {WEST}:0 "'+('Floride occidentale' if lang=='french' else 'West Florida')+'"',f' HUB_NAME_{EAST}_city:0 "'+('Saint Augustine' if lang=='french' else 'St. Augustine')+'"',f' HUB_NAME_{EAST}_port:0 "'+('Saint Augustine' if lang=='french' else 'St. Augustine')+'"']
        for kind,name in {'city':'Pensacola','port':'Pensacola','farm':'Chipola','mine':'Escambia','wood':'Blackwater'}.items():lines.append(f' HUB_NAME_{WEST}_{kind}:0 "{name}"')
        files[f'localization/{lang}/replace/1776_florida_division_l_{lang}.yml']=b'\xef\xbb\xbf'+('\n'.join(lines)+'\n').encode('utf8')
    for kind in geo:
        rel='gfx/map/map_object_data/generated_map_object_locators_'+kind+'.txt';p=source(rel);raw=text(p);nodes=parse(raw);instances=nodes[0].children('instances')[0];patch=[]
        templates=[n for n in instances.children() if n.one('id')=='293'];assert len(templates)==1
        old=templates[0];assert not any(n.one('id')==str(new_id) for n in instances.children())
        def entry(idx,px):
            return '{\n id = '+str(idx)+'\n position = { '+str(px[0])+' 0.0 '+str(a.shape[0]-px[1])+' }\n rotation = { 0 0 0 1 }\n scale = { 1 1 1 }\n}'
        if (EAST,kind) in hubs:
            node=old.children('position')[0];px=hubs[EAST,kind]['pixel'];patch.append((node.start,node.end,'position = { '+str(px[0])+' 0.0 '+str(a.shape[0]-px[1])+' }'))
        if kind=='port':
            for node in instances.children():
                if node.one('id') in {'291','292'}:patch.append((node.start,node.end,''))
        patch.append((instances.end-1,instances.end-1,'\n'+entry(new_id,hubs[WEST,kind]['pixel'])+'\n'))
        files[rel]=encoded(p,edit(raw,patch))
    # Explicit State-list dependencies, using existing mod versions when present.
    for folder in ['common/strategic_regions','common/geographic_regions','common/country_creation']:
        for p in effective(folder):
            raw=text(p)
            if EAST not in raw:continue
            patch=[]
            for n in walk(parse(raw)):
                if n.key in {'states','state_regions'}:
                    for v in n.children():
                        if not v.key and scalar(v.value)==EAST:patch.append((v.start,v.end,raw[v.start:v.end]+' '+WEST))
            if patch:
                rel=p.relative_to(ROOT if p.is_relative_to(ROOT) else GAME).as_posix();files[rel]=encoded(p,edit(raw,patch))
    for rel in ['common/journal_entries/07_american_mod_jes.txt','common/scripted_buttons/00_scripted_buttons_modSX.txt','events/florida_events_mod.txt','common/journal_entries/06_cuba.txt','events/iberia_events/cuba_eventos.txt']:
        raw=text(ROOT/rel);updated=broaden(raw)
        if rel=='common/journal_entries/07_american_mod_jes.txt':updated=exclude_buyer(updated,'je_buying_florida_mod')
        if rel=='events/florida_events_mod.txt':updated=exclude_buyer(updated,'florida.4')
        files[rel]=encoded(ROOT/rel,updated)
    rel='common/scripted_effects/1776_join_ongoing_wars.txt';raw=text(ROOT/rel);roots=parse(raw);effect=next(n for n in roots if n.key=='aor1776_spanish_revolution_goals_effect')
    clause=next(n for n in effect.children('if') if 's:'+EAST in raw[n.start:n.end]);addition='\n'+raw[clause.start:clause.end].replace(EAST,WEST)+'\n'
    files[rel]=encoded(ROOT/rel,edit(raw,[(clause.end,clause.end,addition)]))
    # Check source versions again before writing a stage. Never restore an old shared file.
    assert runtime()==base,'Concurrent runtime mutation during preparation'
    for rel,data in files.items():
        if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
        p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    dump('BASELINE_RUNTIME.json',base);dump('BASELINE_OWNERS.json',{r:sorted(v) for r,v in own.items()});dump('BASELINE_HBC.json',economic_inventory())
    dump('PLAN.json',dict(rows=rows,western=sorted(western),eastern=sorted(eastern),new_state_id=new_id,hubs=hproof,capacities_before=capacities([regions[s] for s in SOURCES]),new_ports=1,province_sovereignty_changed=False,river_dataset_sha256=sha(ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson')))
    dump('PATCH.json',dict(input_sha256={r:base.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files},bitmap_sha256=sha(ROOT/'map_data/provinces.png')))
    print(json.dumps(dict(status='PREPARED',new_id=new_id,west=len(western),east=len(eastern),files=len(files))))


def apply():
    assert not (OUT/'APPLIED.json').exists();p=load(OUT/'PATCH.json')
    assert sha(ROOT/'map_data/provinces.png')==p['bitmap_sha256']
    for r,d in p['input_sha256'].items():assert (sha(ROOT/r) if (ROOT/r).exists() else None)==d,r+' changed; reprepare'
    for r,d in p['output_sha256'].items():assert sha(OUT/'patch'/r)==d
    for r in p['output_sha256']:
        target=ROOT/r
        if target.exists():
            backup=OUT/'before'/r;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((OUT/'patch'/r).read_bytes())
    dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',date='2026-10-26',files=list(p['output_sha256']),engine_tested=False))
    print('Installed; validate next.')


def validate():
    p=load(OUT/'PATCH.json');plan=load(OUT/'PLAN.json');own=ownership();old=load(OUT/'BASELINE_OWNERS.json');checks={}
    checks['installed_hashes']=all(sha(ROOT/r)==d for r,d in p['output_sha256'].items())
    checks['every_province_sovereign_preserved']=set(old)==set(own) and all({t for s,t in v}=={t for s,t in own[r]} for r,v in old.items())
    checks['no_new_duplicate_or_unowned_provinces']=all(len(own[r])==1 for r in plan['western']+plan['eastern'])
    checks['exact_state_migration']=all(own[r]=={(WEST,'GBR')} for r in plan['western']) and all(own[r]==set(map(tuple,old[r])) for r in old if r not in plan['western'])
    before=text(OUT/'before'/PP);after=text(ROOT/PP)
    checks['all_cohorts_totals_types_cultures_religions_preserved']=cohort_totals(before,SOURCES)==cohort_totals(after,SOURCES|{WEST})
    bs=state_nodes(before);ns=state_nodes(after)
    checks['all_other_pop_blocks_preserved']=all(normalized([n])==normalized([ns[s]]) for s,n in bs.items() if s not in SOURCES)
    checks['seminole_population_and_territories_preserved']=normalized(bs[EAST].children('region_state:SML'))==normalized(ns[EAST].children('region_state:SML')) and all(own[r]==set(map(tuple,v)) for r,v in old.items() if any(t=='SML' for s,t in v))
    regs={n.key:n for pp in effective('map_data/state_regions') for n in parse(text(pp))}
    ids=[int(n.one('id',0)) for n in regs.values()];checks['state_id_unique']=ids.count(plan['new_state_id'])==1
    checks['resource_and_arable_budgets_preserved']=capacities([regs[s] for s in SOURCES|{WEST}])==plan['capacities_before']
    checks['new_region_matches_owned_rgb']=set(provs(regs[WEST],'provinces'))==set(plan['western'])
    checks['original_florida_partition_complete']=set(provs(regs[EAST],'provinces'))==set(plan['eastern'])
    region_members=C.defaultdict(list)
    for pp in effective('common/strategic_regions'):
        for n in parse(text(pp)):
            for sid in provs(n,'states'):region_members[sid].append(n.key)
    checks['both_in_same_unique_strategic_region']=region_members[WEST]==region_members[EAST]==['region_atlantic_coast']
    checks['both_in_dixie_geographic_region']=any(n.key=='geographic_region_dixie_old' and {EAST,WEST}<=set(provs(n,'state_regions')) for pp in effective('common/geographic_regions') for n in parse(text(pp)))
    a=bitmap();selected={int(r[1:],16) for r in plan['western']+plan['eastern']};adj=graph(a,np.array(sorted(selected|{0x0D74CA,0x340EED}),dtype=np.uint32));west={int(r[1:],16) for r in plan['western']};east={int(r[1:],16) for r in plan['eastern']}
    checks['west_single_land_component']=len(components(adj,west))==1
    # The Keys were already detached before the split. Prove the exact old
    # island component survives, rather than requiring an invented land bridge.
    original_fl={int(r[1:],16) for r in provs(values(text(OUT/'before'/REG))[EAST],'provinces')}
    old_components=components(adj,original_fl);east_components=components(adj,east)
    checks['east_no_new_land_fragment_and_old_keys_preserved']=east_components[1:]==old_components[1:]
    checks['east_west_land_border_exists']=any(set(adj.get(v,{}))&east for v in west)
    checks['ports_touch_correct_sea']=int(regs[WEST].one('naval_exit_id'))==3060 and int(regs[EAST].one('naval_exit_id'))==3146 and int(scalar(regs[WEST].one('port'))[1:],16) in adj[0x0D74CA] and int(scalar(regs[EAST].one('port'))[1:],16) in adj[0x340EED]
    checks['all_hub_rgb_in_correct_region']=all(scalar(regs[s].one(k)) in set(provs(regs[s],'provinces')) for s in [EAST,WEST] for k in ['city','port','farm','mine','wood'])
    checks['inland_alabama_mississippi_no_stale_ports']=all(not regs[s].children('port') and not regs[s].children('naval_exit_id') for s in SOURCES-{EAST})
    checks['other_neighbor_hubs_match_remaining_regions']=all(scalar(regs[s].one(k)) in set(provs(regs[s],'provinces')) for s in SOURCES-{EAST} for k in ['city','farm','mine','wood'])
    port_entries=[n for n in walk(parse(text(source('gfx/map/map_object_data/generated_map_object_locators_port.txt')))) if n.one('id') is not None]
    checks['no_obsolete_neighbor_port_locators']=not any(n.one('id') in {'291','292'} for n in port_entries)
    for row in plan['hubs']:
        pp=source('gfx/map/map_object_data/generated_map_object_locators_'+row['kind']+'.txt');entries=[n for n in walk(parse(text(pp))) if n.one('id')==str(293 if row['state']==EAST else plan['new_state_id'])];assert len(entries)==1
        pos=[float(n.value) for n in entries[0].children('position')[0].children()];rgb=f'x{int(a[int(a.shape[0]-pos[2]),int(pos[0])]):06X}'
        checks['locator.'+row['state']+'.'+row['kind']]=rgb==row['rgb']
    checks['every_previous_building_history_unchanged']=all((ROOT/r).is_file() and sha(ROOT/r)==d for r,d in load(OUT/'BASELINE_RUNTIME.json').items() if r.startswith('common/history/buildings/'))
    new=text(ROOT/'common/history/buildings/1776_florida_west_port.txt');b=[n for n in walk(parse(new)) if n.key=='create_building']
    checks['one_new_pensacola_port_only']=len(b)==1 and scalar(b[0].one('building'))=='building_port' and sum(int(n.value) for n in walk(b[0].children()) if n.key=='levels')==1
    effect=next(n for n in parse(text(ROOT/'common/scripted_effects/1776_join_ongoing_wars.txt')) if n.key=='aor1776_spanish_revolution_goals_effect');checks['spanish_goals_both_floridas']=sum(n.key=='add_war_goal' and scalar(n.one('type'))=='return_state' and scalar(n.one('target_state')) in {'s:'+s+'.region_state:GBR' for s in [EAST,WEST]} for n in walk(effect.children()))==2
    ev=text(ROOT/'events/florida_events_mod.txt');checks['sale_transfers_all_seller_shares_not_one_random_half']=sum(n.key=='every_state' and any(v.key=='set_state_owner' for v in walk(n.children())) for n in walk(parse(ev)))==2
    for rel,key in [('events/florida_events_mod.txt','florida.4'),('common/journal_entries/07_american_mod_jes.txt','je_buying_florida_mod')]:
        obj=next(n for n in parse(text(ROOT/rel)) if n.key==key)
        owner=obj.children('immediate')[0].children('random_state')[0].children('limit')[0].children('owner')[0]
        checks['purchase_excludes_buyer_and_subjects.'+key]=all(any(n.one(field)=='root' for n in owner.children('NOT')) for field in ['this','is_subject_of'])
    checks.update({'hbc_'+k:v for k,v in conservation(load(OUT/'BASELINE_HBC.json'),economic_inventory()).items()})
    baseline=load(OUT/'BASELINE_RUNTIME.json');now=runtime();unexpected=[r for r in baseline.keys()|now.keys() if baseline.get(r)!=now.get(r) and r not in p['output_sha256']]
    checks['no_unlisted_runtime_change']=not unexpected
    checks['bitmap_and_terrains_unchanged']=all(now.get(r)==d for r,d in baseline.items() if r in ['map_data/provinces.png','map_data/province_terrains.txt'])
    # Prior R8 country ownership is unchanged, even where its coastal cells change State_ID.
    r8=load(PRIOR/'PLAN.json');checks['r8_corrected_countries_preserved']=all({t for s,t in own[r['RGB']]}=={r['After']} for r in r8['rows'] if r['After']!='COM')
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),unexpected=unexpected,engine_tested=False,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'))
    render(own,plan,a);print(json.dumps(checks,indent=2));return all(checks.values())


def render(own,plan,a):
    cut=a[1340:1540,2030:2290];pic=np.full((*cut.shape,3),[35,49,59],dtype=np.uint8)
    present=set(map(int,np.unique(cut)))
    for r,v in own.items():
        val=int(r[1:],16)
        if val not in present:continue
        sid,t=next(iter(v));color=[106,118,104]
        if sid==WEST:color=[222,177,73]
        elif sid==EAST:color=[92,149,199] if t=='GBR' else [103,163,98]
        pic[cut==val]=color
    edge=np.zeros(cut.shape,bool);edge[1:]|=cut[1:]!=cut[:-1];edge[:,1:]|=cut[:,1:]!=cut[:,:-1];pic[edge&np.any(pic!=[35,49,59],axis=2)]=[44,48,44]
    sheet=Image.new('RGB',(1560,1350),'#23313b');sheet.paste(Image.fromarray(pic).resize((1560,1200),Image.Resampling.NEAREST),(0,100));d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    d.text((14,10),'1776 — deux Florides administratives britanniques',font=font,fill='white');d.text((14,49),'Or : Floride occidentale ; bleu : Floride orientale britannique ; vert : Séminoles.',font=font,fill='white')
    for name,sid in [('Pensacola',WEST),('Saint Augustine',EAST)]:
        p=next(r['chosen_pixel'] for r in plan['hubs'] if r['state']==sid and r['kind']=='city');x=(p[0]-2030)*6;y=100+(p[1]-1340)*6;d.ellipse((x-5,y-5,x+5,y+5),fill='white');d.text((x-70,y-34),name,font=font,fill='white',stroke_width=2,stroke_fill='black')
    d.text((14,1312),'Frontière approximative de l’Apalachicola ; souveraineté et populations conservées.',font=font,fill='white');sheet.save(OUT/'FLORIDA_1776.png')


if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--validate' in sys.argv:sys.exit(0 if validate() else 1)
    else:raise SystemExit('Use --prepare, --apply or --validate')
