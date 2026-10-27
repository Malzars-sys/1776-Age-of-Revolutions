"""Conservative whole-province correction of documented colonial overextensions.

Category B, not a survey of every 1776 frontier. Known settlements and the
player's HBC/Quebec/USA land witness are protected. No bitmap or Git writes.
"""
import collections as C
import csv,heapq,json,sys,zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,ownership,rgb_block,NATIVE_LAWS
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from hbc03_quebec_arc import economic_inventory,conservation
from hbc02_map_candidates import graph
from georeference.model import fit,evaluate,forward,inverse
from r8_south_geometry import bitmap,norm
from r8_south_correct import allocate,pop_signature,components
from hbc04_land_links import flood,path,contacts,pair
import colonies01_core as core

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/COLONIES-01/FRONTIER'
ST=core.ST;PP=core.PP
TARGET={'STATE_NEW_YORK','STATE_GEORGIA','STATE_NORTH_CAROLINA','STATE_SOUTH_CAROLINA'}
ADMIN={'STATE_NEW_YORK':'NY','STATE_GEORGIA':'GA','STATE_NORTH_CAROLINA':'NC','STATE_SOUTH_CAROLINA':'SC','STATE_VIRGINIA':'VA','STATE_PENNSYLVANIA':'PA','STATE_MARYLAND':'MD','STATE_MASSACHUSETTS':'MA','STATE_NEW_JERSEY':'NJ'}


def load(p):return core.load(p)
def dump(n,o):(OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def owners():
    out=C.defaultdict(set)
    for r,v in ownership().items():out['x'+r[1:].upper()].update(v)
    return out


def calibration(a,regs):
    loc={}
    for kind in ['city','farm','mine','wood','port']:
        rel='gfx/map/map_object_data/generated_map_object_locators_'+kind+'.txt';p=ROOT/rel if (ROOT/rel).exists() else GAME/rel
        for n in parse(text(p))[0].children('instances')[0].children():
            if n.one('id') is not None:
                pos=[float(v.value) for v in n.children('position')[0].children()];loc[int(n.one('id')),kind]=[pos[0],a.shape[0]-pos[2]]
    with zipfile.ZipFile(ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip') as z:
        records=[r for line in z.read('cities1000.txt').decode().splitlines() if (r:=line.split('\t'))[8]=='US']
    rows=[];aliases={'New York':'New York City','Washington':'Washington, D.C.','Virginia Beach':'Virginia Beach','Pittsburgh':'Pittsburgh'}
    for row in csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')):
        sid,kind,name=row['State_ID'],row['Hub_Type'],row['Hub_Name']
        if sid not in ADMIN:continue
        matches=[r for r in records if r[10]==ADMIN[sid] and norm(r[1]) in {norm(name),norm(aliases.get(name,name))}]
        if not matches:continue
        rec=max(matches,key=lambda r:int(r[14] or 0));px=loc[int(regs[sid].one('id')),kind];rgb=f'x{int(a[int(px[1]),int(px[0])]):06X}'
        if rgb not in provs(regs[sid],'provinces'):continue
        rows.append(dict(name=name,state=sid,kind=kind,role='FIT' if kind=='city' else 'CHECK',geo=[float(rec[5]),float(rec[4])],pixel=px,rgb=rgb))
    assert len([r for r in rows if r['role']=='FIT'])>=6
    model=fit(rows,'miller_affine',a.shape[::-1]);dump('GEODETIC_CONTROLS.json',rows);dump('GEODETIC_MODEL.json',model);dump('GEODETIC_EVALUATION.json',evaluate(model));return model


def choose(s,lon,lat):
    if s=='STATE_GEORGIA' and lon< -83.2:return 'CHE' if lat>34.3 else 'MSC'
    if s=='STATE_NORTH_CAROLINA':
        # Reedy River/Tryon Mountain/Chiswell line, approximated at province scale.
        boundary=float(np.interp(lat,[34.95,35.22,36.94],[-82.35,-82.23,-80.95]))
        if lon<boundary:return 'CHE'
    if s=='STATE_SOUTH_CAROLINA' and lon< -82.65 and lat>34.2:return 'CHE'
    if s=='STATE_NEW_YORK' and lon< -75.5:return 'IRO'
    return 'USA'


def land_witness(a,own,desired):
    """Keep direct Upper Canada access by the eastern NY border, not a strip
    artificially cutting the Haudenosaunee homeland into disconnected pockets.
    The approved HBC and Quebec ownership/geometry is entirely unchanged.
    """
    current={r:set(v) for r,v in own.items()}
    for r,(sid,t) in desired.items():current[r]={(sid,t)}
    impassable={int(r[1:],16) for pp in effective('map_data/state_regions') for n in parse(text(pp)) for r in provs(n,'impassable')}
    blocked=set();rel='map_data/adjacencies.csv';pp=ROOT/rel if (ROOT/rel).exists() else GAME/rel
    for row in csv.DictReader(pp.open(encoding='utf-8-sig'),delimiter=';'):
        if all(row.get(k,'').startswith('x') for k in ['From','To']) and (row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip()):blocked.add(pair(int(row['From'][1:],16),int(row['To'][1:],16)))
    colors={t:{int(r[1:],16) for r,v in current.items() if any(tt==t for s,tt in v)}-impassable for t in ['HBC','QUE','USA']}
    masks={t:np.isin(a,sorted(v)) for t,v in colors.items()}
    ont=np.isin(a,[int(r[1:],16) for r,v in current.items() if ('STATE_ONTARIO','QUE') in v])
    links=contacts(a,ont,masks['USA'],blocked);assert links,'Upper Canada no longer directly touches the colonies'
    usa_by_seed=dict(links);qparents,_=flood(a,masks['QUE'],usa_by_seed,blocked)
    goals={u:v for u,v in contacts(a,masks['HBC'],masks['QUE'],blocked) if v in qparents};assert goals
    old=load(OUT.parent.parent/'HBC-04/PIXEL_PATH_WITNESS.json');x,y=old[0]['pixel'];start=y*a.shape[1]+x
    parents,end=flood(a,masks['HBC'],[start],blocked,goals=set(goals));assert end is not None
    qp=path(qparents,goals[end])[::-1];route=path(parents,end)+qp+[usa_by_seed[qp[-1]]]
    witness=[]
    for u in route:
        y,x=divmod(u,a.shape[1]);r=f'x{int(a[y,x]):06X}';sid,t=next(iter(current[r]));witness.append(dict(pixel=[x,y],rgb=r,state=sid,owner=t))
    assert list(dict.fromkeys(r['owner'] for r in witness))==['HBC','QUE','USA']
    assert witness[-2]['state']=='STATE_ONTARIO'
    dump('UPDATED_LAND_WITNESS.json',witness)
    return dict(pixel_steps=len(route),old_endpoint=old[-1]['rgb'],new_endpoint=witness[-1]['rgb'],old_endpoint_replaced_not_mandated_by_player=True,native_passability_respected=True,engine_military_access_observed=False)


def prepare():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'APPLIED.json').exists();before=runtime();own=owners();a=bitmap()
    regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};model=calibration(a,regs)
    selected={r:s for r,v in own.items() for s,t in v if s in TARGET and t=='USA'};centers={}
    for r in selected:
        y,x=np.where(a==int(r[1:],16));assert len(x);centers[r]=[float(x.mean()),float(y.mean())]
    desired={};rows=[]
    for r,s in selected.items():
        lon,lat=map(float,inverse(model,[centers[r]])[0]);desired[r]=choose(s,lon,lat)
        rows.append(dict(rgb=r,state=s,before='USA',after=desired[r],geo_proxy=[lon,lat],policy='CONSERVATIVE_REGIONAL_ARBITRATION_NOT_SURVEYED_BOUNDARY'))
    # Preserve documented early colonial towns and the 1773 Georgia ceded core.
    sites={'Savannah':('STATE_GEORGIA',[-81.0998,32.0835]),'Augusta':('STATE_GEORGIA',[-81.9748,33.4735]),'Washington_1773_cession':('STATE_GEORGIA',[-82.7393,33.7368]),'Albany':('STATE_NEW_YORK',[-73.7562,42.6526]),'New_York':('STATE_NEW_YORK',[-74.006,40.7128]),'Ninety_Six':('STATE_SOUTH_CAROLINA',[-82.0224,34.1751]),'Charleston':('STATE_SOUTH_CAROLINA',[-79.9311,32.7765]),'New_Bern':('STATE_NORTH_CAROLINA',[-77.0441,35.1085]),'Wilmington':('STATE_NORTH_CAROLINA',[-77.9447,34.2257])}
    protected=[]
    for name,(sid,geo) in sites.items():
        p=forward(model,[geo])[0];r=min((r for r,s in selected.items() if s==sid),key=lambda r:np.linalg.norm(np.array(centers[r])-p));desired[r]='USA';protected.append(dict(name=name,state=sid,geo=geo,rgb=r))
    connection=land_witness(a,own,{r:(selected[r],t) for r,t in desired.items()})
    for r in rows:r['after']=desired[r['rgb']]
    changes={r:t for r,t in desired.items() if t!='USA'};assert {'CHE','MSC','IRO'}<=set(changes.values())
    by=C.defaultdict(set)
    for r,t in desired.items():by[selected[r],t].add(r)
    files={};raw=text(ROOT/ST);patch=[]
    for sid,s in state_nodes(raw).items():
        if sid not in TARGET:continue
        src=[n for n in s.children('create_state') if n.one('country')=='c:USA'];assert len(src)==1;n=src[0]
        node=n.children('owned_provinces')[0];patch.append((node.start,node.end,'owned_provinces = '+rgb_block(by[sid,'USA'])))
        for (ss,t),cells in by.items():
            if ss==sid and t!='USA':patch.append((s.end-1,s.end-1,'\n create_state = { country = c:'+t+' owned_provinces = '+rgb_block(cells)+' }\n'))
        cultures={'CHE':'cherokee','MSC':'muskogean','IRO':'iroquoian'}
        present={scalar(n.value) for n in s.children('add_homeland')}
        for t,cu in cultures.items():
            if (sid,t) in by and 'cu:'+cu not in present:patch.append((s.end-1,s.end-1,'\n add_homeland = cu:'+cu+'\n'))
    files[ST]=encoded(ROOT/ST,edit(raw,patch))
    # Keep settlers/jobs on retained colonial territory. Transfer only existing
    # Cherokee/Iroquoian cohorts; no people are converted or created.
    raw=text(ROOT/PP);ns=state_nodes(raw);patch=[];native=C.defaultdict(list)
    for sid in TARGET:
        rs=ns[sid].children('region_state:USA')[0]
        for n in rs.children('create_pop'):
            cu=scalar(n.one('culture'));t='IRO' if cu=='iroquoian' else 'CHE' if cu=='cherokee' else None
            if t and (sid,t) in by:native[sid,t].append(raw[n.start:n.end]);patch.append((n.start,n.end,''))
    # Existing Muscogee cohorts are shared between their Alabama and Georgia
    # portions. This is a documented technical relocation, not a new census.
    old=ns['STATE_ALABAMA'].children('region_state:MSC')[0]
    weights={'STATE_ALABAMA':sum((s,'MSC') in v for v in own.values() for s in ['STATE_ALABAMA']),'STATE_GEORGIA':len(by['STATE_GEORGIA','MSC'])}
    for n in old.children('create_pop'):
        size=n.children('size')[0];counts=allocate(int(size.value),weights)
        patch.append((size.start,size.end,'size = '+str(counts['STATE_ALABAMA'])))
        part=raw[n.start:n.end];part=part[:size.start-n.start]+'size = '+str(counts['STATE_GEORGIA'])+part[size.end-n.start:];native['STATE_GEORGIA','MSC'].append(part)
    for (sid,t),bodies in native.items():patch.append((ns[sid].end-1,ns[sid].end-1,'\n region_state:'+t+' = {\n'+'\n'.join(bodies)+'\n }\n'))
    assert all((s,t) in native for (s,t) in by if t!='USA'),'Every new native portion needs existing, identified population'
    files[PP]=encoded(ROOT/PP,edit(raw,patch))
    # Colonial administrative seats: Atlanta/Raleigh are later foundations.
    # Keep the old State_IDs and all assets, but put their city hubs at the
    # existing 1776 seats Savannah/New Bern in retained colonial territory.
    regrel='map_data/state_regions/05_north_america.txt';raw=text(ROOT/regrel);patch=[];hubproof=[]
    cityrel='gfx/map/map_object_data/generated_map_object_locators_city.txt';cityraw=text(ROOT/cityrel);citypatch=[]
    for sid,name,geo in [('STATE_GEORGIA','Savannah',[-81.0998,32.0835]),('STATE_NORTH_CAROLINA','New Bern',[-77.0441,35.1085])]:
        pred=forward(model,[geo])[0];yy,xx=np.where(np.isin(a,[int(r[1:],16) for r in by[sid,'USA']]))
        i=int(np.argmin((xx-pred[0])**2+(yy-pred[1])**2));x,y=int(xx[i]),int(yy[i]);r=f'x{int(a[y,x]):06X}'
        node=next(n for n in parse(raw) if n.key==sid).children('city')[0];patch.append((node.start,node.end,'city = "'+r+'"'))
        n=next(n for n in parse(cityraw)[0].children('instances')[0].children() if n.one('id')==regs[sid].one('id'));node=n.children('position')[0]
        citypatch.append((node.start,node.end,f'position = {{ {x} 0.0 {a.shape[0]-y} }}'))
        hubproof.append(dict(state=sid,name=name,rgb=r,pixel=[x,y],geo=geo,kind='city',precision='EMPIRICAL_SNAP_NOT_SURVEYED'))
    files[regrel]=encoded(ROOT/regrel,edit(raw,patch));files[cityrel]=encoded(ROOT/cityrel,edit(cityraw,citypatch))
    for lang in ['french','english']:
        files[f'localization/{lang}/replace/1776_colonial_seats_l_{lang}.yml']=b'\xef\xbb\xbf'+('l_'+lang+':\n HUB_NAME_STATE_GEORGIA_city:0 "Savannah"\n HUB_NAME_STATE_NORTH_CAROLINA_city:0 "New Bern"\n').encode('utf8')
    # Activate the already defined Haudenosaunee country with a local profile.
    rel='common/country_definitions/00_countries.txt';raw=text(ROOT/rel);n=next(n for n in parse(raw) if n.key=='IRO');typ=n.children('country_type')[0]
    files[rel]=encoded(ROOT/rel,edit(raw,[(typ.start,typ.end,'country_type = decentralized'),(n.end-1,n.end-1,'\n religion = animist\n')]))
    rel='common/history/countries/1776_haudenosaunee.txt';assert not (ROOT/rel).exists()
    files[rel]=('COUNTRIES = { c:IRO ?= { add_technology_researched = traditional_food_processing\n'+''.join('activate_law = law_type:law_'+law+'\n' for law in NATIVE_LAWS)+'effect_native_conscription_10 = yes\n} }\n').encode()
    # No built assets follow the transferred Native countryside: all prior
    # colonial buildings retain their owner, level, PM, reserve and State share.
    assert runtime()==before
    dump('BASELINE_RUNTIME.json',before);dump('BASELINE_OWNERS.json',{r:sorted(v) for r,v in own.items()});dump('BASELINE_HBC.json',economic_inventory())
    for rel,data in files.items():
        parse(data.decode('utf-8-sig'));p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    dump('PATCH.json',dict(input_sha256={r:before.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files}))
    dump('PLAN.json',dict(rows=rows,transfers=len(changes),protected_sites=protected,land_connection=connection,hubs=hubproof,muscogee_population_allocation_weights=weights,sovereignty_precision='CATEGORY_B_REGIONAL_APPROXIMATION',all_frontiers_complete=False))
    with (OUT/'PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps(dict(transfers=len(changes),after={s:dict(C.Counter(desired[r] for r,ss in selected.items() if ss==s)) for s in sorted(TARGET)},land_connection=connection)))


def apply():
    core.OUT=OUT;core.apply()


def totals(raw):
    out=C.Counter()
    for s in state_nodes(raw).values():
        for rs in s.children():
            if rs.key.startswith('region_state:'):
                for n in rs.children('create_pop'):out[pop_signature(n)]+=int(n.one('size'))
    return out


def validate():
    p=load(OUT/'PATCH.json');plan=load(OUT/'PLAN.json');own=owners();old=load(OUT/'BASELINE_OWNERS.json');checks={}
    checks['installed_hashes']=all(sha(ROOT/r)==d for r,d in p['output_sha256'].items())
    desired={r['rgb']:(r['state'],r['after']) for r in plan['rows']};checks['every_planned_owner']=all(own[r]=={v} for r,v in desired.items())
    checks['no_other_territorial_change']=set(old)==set(own) and all(own[r]==set(map(tuple,v)) for r,v in old.items() if r not in desired)
    checks['world_population_and_every_identity_preserved']=totals(text(ROOT/PP))==totals(text(OUT/'before'/PP))
    base=load(OUT/'BASELINE_RUNTIME.json');now=runtime();checks['all_buildings_and_units_preserved']=all(now.get(r)==d for r,d in base.items() if r.startswith(('common/history/buildings/','common/history/military_formations/')))
    checks['protected_sites_retained']=all(own[r['rgb']]=={(r['state'],'USA')} for r in plan['protected_sites'])
    witness=load(OUT/'UPDATED_LAND_WITNESS.json')
    checks['hbc_upper_canada_usa_pixel_route']=all(own[r['rgb']]=={(r['state'],r['owner'])} for r in witness) and list(dict.fromkeys(r['owner'] for r in witness))==['HBC','QUE','USA'] and witness[-2]['state']=='STATE_ONTARIO'
    checks['land_route_side_adjacent']=all(abs(u['pixel'][0]-v['pixel'][0])+abs(u['pixel'][1]-v['pixel'][1])==1 for u,v in zip(witness,witness[1:]))
    checks['no_new_province_without_population']=all(state_nodes(text(ROOT/PP))[s].children('region_state:'+t) for s,t in set(desired.values()) if t!='USA')
    checks.update({'hbc_'+k:v for k,v in conservation(load(OUT/'BASELINE_HBC.json'),economic_inventory()).items()})
    checks['other_map_data_preserved']=all(now.get(r)==d for r,d in base.items() if r.startswith(('map_data/','gfx/map/')) and r not in p['output_sha256'])
    for row in plan['hubs']:checks['colonial_city_hub_owned.'+row['state']]=own[row['rgb']]=={(row['state'],'USA')}
    approved_core=load(OUT.parent/'CORE/PATCH.json')['output_sha256']
    checks['no_unlisted_changes']=not any(base.get(r)!=now.get(r) and approved_core.get(r)!=now.get(r) for r in base.keys()|now.keys() if r not in p['output_sha256'])
    # Record connectivity, including inherited islands; never bridge them blindly.
    a=bitmap();cells={int(r['rgb'][1:],16) for r in plan['rows']};cells|={int(r[1:],16) for r,v in own.items() if any(t in {'CHE','MSC'} for s,t in v)}
    adj=graph(a,np.array(sorted(cells),dtype=np.uint32));conn={}
    for t in ['CHE','MSC','IRO']:
        rs={int(r[1:],16) for r,v in own.items() if any(tt==t for s,tt in v)};conn[t]=[len(c) for c in components(adj,rs)]
    checks['native_countries_connected']=all(len(v)==1 for v in conn.values())
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),connectivity=conn,engine_tested=False));render(own,a)
    print(json.dumps(dict(checks=checks,connectivity=conn),indent=2));return all(checks.values())


def render(own,a):
    cut=a[990:1410,2090:2540];pic=np.full((*cut.shape,3),[36,49,59],dtype=np.uint8);colors={'USA':[99,153,199],'IRO':[113,179,91],'CHE':[177,151,69],'MSC':[173,101,149],'QUE':[192,157,113],'NVS':[188,118,81]};present=set(map(int,np.unique(cut)))
    for r,v in own.items():
        val=int(r[1:],16)
        if val in present:pic[cut==val]=colors.get(next(iter(v))[1],[107,118,108])
    edge=np.zeros(cut.shape,bool);edge[1:]|=cut[1:]!=cut[:-1];edge[:,1:]|=cut[:,1:]!=cut[:,:-1];pic[edge&np.any(pic!=[36,49,59],axis=2)]=[42,47,43]
    crop=Image.fromarray(pic).resize((1350,1260),Image.Resampling.NEAREST);sheet=Image.new('RGB',(1350,1370),'#24313b');sheet.paste(crop,(0,80));d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    d.text((12,10),'1776 — frontières coloniales corrigées par provinces existantes',font=font,fill='white');d.text((12,43),'Bleu : Treize Colonies ; vert : Haudenosaunee ; or : Cherokees ; mauve : Muscogees.',font=font,fill='white');d.text((12,1342),'Arbitrages régionaux ; passage militaire du joueur conservé ; marges non homologuées.',font=font,fill='white');sheet.save(OUT/'FRONTIERS_1776.png')


if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--validate' in sys.argv:sys.exit(0 if validate() else 1)
