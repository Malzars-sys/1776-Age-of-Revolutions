"""Install the player-approved HBC contour; regional Indigenous gameplay scenario.

--prepare writes a reviewable patch only. --apply checks every captured hash first.
--validate independently rereads effective histories. No Git or vanilla writes.
"""
import collections as C
import csv
import heapq
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from audit_hbc_1776 import ROOT, GAME, STATES, effective, provs, runtime, sha
from validate_diplomacy_ottoman_1776 import parse, walk, scalar
from hbc03_quebec_arc import economic_inventory, conservation
from hbc02_map_candidates import graph
from hbc04_land_links import flood, pair
from georeference.model import forward

OUT = ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-06'
BASE = OUT.parent
ST = 'common/history/states/00_states.txt'
PP = 'common/history/pops/05_north_america.txt'
PREFIX = '1776_hbc_indigenous'
# Regional ethnolinguistic aggregates, not modern governments projected into 1776.
# Seeds guide approximate whole-province geometry, not surveyed tribal boundaries.
GROUPS = [
 ('H01','Cris des bois','Woods Cree','cree',[-105,55],[96,145,77],['STATE_SASKATCHEWAN']),
 ('H02','Cris des marais','Swampy Cree','cree',[-97,55],[179,116,61],['STATE_MANITOBA']),
 ('H03','Dénésulines','Denesuline','athabaskan',[-103,59],[102,111,167],['STATE_SASKATCHEWAN','STATE_MANITOBA']),
 ('H04','Sayisi Dene','Sayisi Dene','athabaskan',[-96,60.5],[174,121,158],['STATE_NUNAVUT']),
 ('H05','Mushkegowuk','Mushkegowuk','cree',[-85,54],[78,157,137],['STATE_ONTARIO']),
 ('H06','Anishinabeg','Anishinabeg','algonquian',[-88,49.5],[161,154,70],['STATE_ONTARIO']),
 ('H07','Eeyou','Eeyou','cree',[-76,52.5],[185,99,100],['STATE_QUEBEC']),
 ('H08','Naskapis','Naskapi','cree',[-69,56],[128,151,97],['STATE_QUEBEC']),
 ('H09','Inuit du Nunavik','Nunavik Inuit','inuit',[-75,60],[111,167,188],['STATE_QUEBEC']),
 ('H10','Inuit du Kivalliq','Kivalliq Inuit','inuit',[-94,64],[186,155,106],['STATE_NUNAVUT']),
 ('H11','Netsilingmiut','Netsilingmiut','inuit',[-96,69],[100,132,162],['STATE_NUNAVUT']),
 ('H12','Iglulingmiut','Iglulingmiut','inuit',[-83,69],[155,155,189],['STATE_NUNAVUT']),
 ('H13','Inuit de Baffin','Baffin Inuit','inuit',[-68,67],[164,183,171],['STATE_NUNAVUT']),
]
# Explicitly ahistorical player-requested population, not a census or estimate.
ADDED = dict(STATE_NUNAVUT=300000, STATE_MANITOBA=250000,
             STATE_SASKATCHEWAN=250000, STATE_ONTARIO=800000, STATE_QUEBEC=800000)
CLAIMS = set(STATES)-{'STATE_NUNAVUT'}
NATIVE_LAWS = ['chiefdom','state_religion','hereditary_bureaucrats','subjecthood',
               'traditionalism','peasant_levies','closed_borders','guild_system',
               'consumption_based_taxation','isolationism','serfdom','no_workers_rights']


def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(n,o): (OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def text(p): return p.read_bytes().decode('utf-8-sig')
def encoded(p,s): return (b'\xef\xbb\xbf' if p.read_bytes().startswith(b'\xef\xbb\xbf') else b'')+s.encode('utf8')
def edit(raw,edits):
    for a,b,s in sorted(edits,reverse=True): raw=raw[:a]+s+raw[b:]
    parse(raw)
    return raw
def ownership():
    result=C.defaultdict(set)
    for p in effective('common/history/states'):
        for s in walk(parse(text(p))):
            if s.key.startswith('s:STATE_'):
                for n in s.children('create_state'):
                    for rgb in provs(n,'owned_provinces'):
                        result[rgb].add((s.key[2:],scalar(n.one('country')).removeprefix('c:')))
    return result
def state_nodes(raw): return {n.key[2:]:n for n in walk(parse(raw)) if n.key.startswith('s:STATE_')}
def rgb_block(values):
    values=sorted(values)
    return '{\n'+''.join('\t\t\t\t'+' '.join(values[i:i+12])+'\n' for i in range(0,len(values),12))+'\t\t\t}'


def targets_match(actual,targets,prior):
    return all(actual.get(r,set())=={(next(iter(prior(r)))[0],t)} for r,t in targets.items())


def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'APPLIED.json').exists(),'Already applied; use --validate.'
    before=runtime();own=ownership()
    assert all(conservation(load(BASE/'HBC-03/CONSERVATION_BASELINE.json'),economic_inventory()).values())
    approved=load(BASE/'HBC-05/COMPACT_BLOCKS.json')
    hbc=set(approved['hbc_rgb']);ont=set(approved['ont_rgb'])
    assert len(hbc)==278 and len(ont)==103 and hbc.isdisjoint(ont)
    old={r for r,v in own.items() if any(t=='HBC' for s,t in v)}
    oldont={r for r,v in own.items() if any(t=='ONT' for s,t in v)}
    assert hbc<=old and oldont<=ont and ont-oldont<=old
    assert all(len(own[r])==1 for r in old|oldont)
    removed=old-hbc-(ont-oldont)
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
    ids,inv,counts=np.unique(a,return_inverse=True,return_counts=True)
    yy,xx=np.indices(a.shape);sx=np.bincount(inv.ravel(),weights=xx.ravel());sy=np.bincount(inv.ravel(),weights=yy.ravel())
    centers={f'x{int(v):06X}':(float(sx[i]/counts[i]),float(sy[i]/counts[i])) for i,v in enumerate(ids)}
    model=load(BASE/'HBC-02/MODELS.json')['miller_affine']
    seeds={g[0]:forward(model,[g[4]])[0] for g in GROUPS}
    # Organic shared-edge fronts; disconnected Arctic islands use nearest regional seed.
    adj=graph(a,np.asarray([int(r[1:],16) for r in removed],dtype=np.uint32))
    assignment={};seed_info=[]
    for sid in STATES:
        cells={r for r in removed if (sid,'HBC') in own[r]}
        groups=[g for g in GROUPS if sid in g[6]]
        dist={};owner={};q=[];used=set()
        for g in groups:
            seed=min(cells-used,key=lambda r:np.linalg.norm(np.array(centers[r])-seeds[g[0]]));used.add(seed)
            dist[seed]=0.;owner[seed]=g[0];heapq.heappush(q,(0.,seed,g[0]))
            seed_info.append(dict(tag=g[0],state=sid,rgb=seed,geo_proxy=g[4],pixel=list(centers[seed])))
        while q:
            d,r,t=heapq.heappop(q)
            if d!=dist[r] or t!=owner[r]:continue
            for v in adj[int(r[1:],16)]:
                rr=f'x{v:06X}'
                if rr not in cells:continue
                cost=d+float(np.linalg.norm(np.array(centers[r])-centers[rr]))
                if cost<dist.get(rr,float('inf')):
                    dist[rr]=cost;owner[rr]=t;heapq.heappush(q,(cost,rr,t))
        for r in cells-owner.keys():
            owner[r]=min(groups,key=lambda g:np.linalg.norm(np.array(centers[r])-seeds[g[0]]))[0]
        assignment.update(owner)
    assert set(assignment)==removed and set(assignment.values())=={g[0] for g in GROUPS}
    targets={r:next(iter(v))[1] for r,v in own.items() if r in old|oldont}
    targets.update(assignment);targets.update({r:'HBC' for r in hbc});targets.update({r:'ONT' for r in ont})
    by=C.defaultdict(set)
    for r,t in targets.items():by[next(iter(own[r]))[0],t].add(r)
    files={};raw=text(ROOT/ST);patch=[]
    for sid,s in state_nodes(raw).items():
        if sid not in STATES:continue
        for n in s.children('create_state'):
            t=scalar(n.one('country')).removeprefix('c:')
            if t not in {'HBC','ONT'}:continue
            values=by.get((sid,t),set())
            if not values:patch.append((n.start,n.end,''))
            else:
                node=n.children('owned_provinces')[0]
                patch.append((node.start,node.end,'owned_provinces = '+rgb_block(values)))
        additions=''
        for g in GROUPS:
            if (sid,g[0]) in by:
                additions+='\n\t\tcreate_state = {\n\t\t\tcountry = c:'+g[0]+'\n\t\t\towned_provinces = '+rgb_block(by[sid,g[0]])+'\n\t\t}\n'
        old_homelands={scalar(n.value) for n in s.children('add_homeland')}
        for cu in sorted({g[3] for g in GROUPS if (sid,g[0]) in by}):
            if 'cu:'+cu not in old_homelands:additions+='\n\t\tadd_homeland = cu:'+cu+'\n'
        # Native claims are State Region-wide. Do not claim the entire Arctic Nunavut.
        if sid in CLAIMS and not any(scalar(n.value)=='c:HBC' for n in s.children('add_claim')):
            additions+='\n\t\tadd_claim = c:HBC\n'
        if sid=='STATE_NUNAVUT':
            for n in s.children('add_claim'):
                if scalar(n.value)=='c:HBC':patch.append((n.start,n.end,''))
        patch.append((s.end-1,s.end-1,additions))
    files[ST]=encoded(ROOT/ST,edit(raw,patch))
    # Move the disappearing HBC Nunavut POP block verbatim to HBC Manitoba.
    raw=text(ROOT/PP);ns=state_nodes(raw);source=ns['STATE_NUNAVUT'].children('region_state:HBC')[0]
    target=ns['STATE_MANITOBA'].children('region_state:HBC')[0]
    bodies='\n'+raw[raw.index('{',source.start)+1:source.end-1]+'\n\t\t'
    files[PP]=encoded(ROOT/PP,edit(raw,[(source.start,source.end,''),(target.end-1,target.end-1,bodies)]))
    defs=[];hist=['COUNTRIES = {'];flags=[];coas=[];loc={'french':['l_french:'],'english':['l_english:']};pop=['POPS = {'];poprows=[]
    culture={'H08':'cree'} # Naskapi/Innu language detail remains aggregated in existing culture.
    for g in GROUPS:
        t,fr,en,cu,geo,color,sids=g
        assert all(t not in [n.key for n in parse(text(p))] for p in effective('common/country_definitions'))
        portions={s:by[s,t] for s in sids if (s,t) in by};capital=max(portions,key=lambda s:len(portions[s]))
        defs.append(f'{t} = {{ color = {{ {" ".join(map(str,color))} }} country_type = decentralized tier = principality cultures = {{ {cu} }} religion = animist capital = {capital} }}')
        tech=['traditional_food_processing'] if cu in {'cree','algonquian'} else []
        hist.append(f' c:{t} ?= {{\n  # Deliberate regional profile; no imported industrial or European military tier.\n'+''.join('  add_technology_researched = '+v+'\n' for v in tech)+''.join('  activate_law = law_type:law_'+v+'\n' for v in NATIVE_LAWS)+'  effect_native_conscription_10 = yes\n }')
        # Decorative scenario banners, not claimed historical national flags.
        flags.append(f'{t} = {{ flag_definition = {{ coa = aor1776_{t.lower()} priority = 100 allow_overlord_canton = no }} }}')
        fc=['green','brown','blue','purple','green','yellow','red','green','blue','brown','blue','purple','black'][GROUPS.index(g)]
        coas.append(f'aor1776_{t.lower()} = {{ pattern = "pattern_solid.tga" color1 = "{fc}" colored_emblem = {{ texture = "ce_bend_dexter.dds" color1 = "white" instance = {{ scale = {{ 0.8 0.8 }} }} }} }}')
        for lang,name in [('french',fr),('english',en)]:
            loc[lang]+=[f' {t}:0 "{name}"',f' {t}_ADJ:0 "'+('autochtone' if lang=='french' else 'Indigenous')+'"']
    hist.append('}')
    # Population quotas are explicit gameplay values by State, never pixel-derived censuses.
    for sid,total in ADDED.items():
        groups=[g for g in GROUPS if (sid,g[0]) in by];weights=[len(by[sid,g[0]]) for g in groups]
        numbers=[total*w//sum(weights) for w in weights];numbers[0]+=total-sum(numbers)
        pop.append(' s:'+sid+' = {')
        for g,n in zip(groups,numbers):
            pop.append(f'  region_state:{g[0]} = {{ create_pop = {{ culture = {g[3]} religion = animist size = {n} }} }}')
            poprows.append(dict(state=sid,tag=g[0],culture=g[3],population=n,policy='PLAYER_AUTHORIZED_AHISTORICAL_GAMEPLAY_ADDITION'))
        pop.append(' }')
    pop.append('}')
    for folder,lines in [('country_definitions',defs),('history/countries',hist),('flag_definitions',flags),('coat_of_arms/coat_of_arms',coas),('history/pops',pop)]:
        files[f'common/{folder}/{PREFIX}.txt']=('\n'.join(lines)+'\n').encode('utf8')
    for lang,lines in loc.items():files[f'localization/{lang}/{PREFIX}_l_{lang}.yml']=b'\xef\xbb\xbf'+('\n'.join(lines)+'\n').encode('utf8')
    for rel,data in files.items():
        if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
        p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    dump('PATCH.json',dict(input_sha256={p:before.get(p) for p in files},patch_sha256={p:sha(OUT/'patch'/p) for p in files},bitmap_sha256=sha(ROOT/'map_data/provinces.png')))
    dump('BASELINE_RUNTIME.json',before)
    dump('PLAN.json',dict(date='2026-10-26',status='PREPARED',groups=[dict(tag=g[0],fr=g[1],en=g[2],culture=g[3],geo_proxy=g[4],color=g[5],allowed_states=g[6]) for g in GROUPS],targets=targets,old_hbc=sorted(old),old_ont=sorted(oldont),by_state={s:{t:len(v) for (ss,t),v in by.items() if ss==s} for s in STATES},seeds=seed_info,populations=poprows,added_population=sum(ADDED.values()),claims=sorted(CLAIMS),historical_boundary_precision='APPROXIMATE_REGIONAL_AGGREGATION',arctic_georeferencing='EXTRAPOLATED_FROM_EXISTING_MODEL_NOT_CADASTRAL',native_Nunavut_claim_omitted='State-wide Arctic claim unsupported; southern watershed claim needs a future finer State split.'))
    with (OUT/'PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['RGB','State_ID','Before','After'])
        for r,t in sorted(targets.items()):s,oldowner=next(iter(own[r]));w.writerow([r,s,oldowner,t])
    assert runtime()==before,'Concurrent runtime write during preparation; inspect before applying.'
    print(json.dumps(dict(status='PREPARED',native_groups=len(GROUPS),new_population=sum(ADDED.values()),ownership=load(OUT/'PLAN.json')['by_state'])))


def apply():
    assert not (OUT/'APPLIED.json').exists(),'Already installed.'
    p=load(OUT/'PATCH.json')
    assert sha(ROOT/'map_data/provinces.png')==p['bitmap_sha256'],'Bitmap changed.'
    for rel,digest in p['input_sha256'].items():
        target=ROOT/rel
        assert (sha(target) if target.exists() else None)==digest,rel+' changed; reprepare.'
        assert sha(OUT/'patch'/rel)==p['patch_sha256'][rel],rel+' staged patch changed.'
    for rel in p['input_sha256']:
        target=ROOT/rel
        if target.exists():
            backup=OUT/'before'/rel;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((OUT/'patch'/rel).read_bytes())
    dump('APPLIED.json',dict(date='2026-10-26',files=p['patch_sha256'],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
    validate()


def validate():
    plan=load(OUT/'PLAN.json');own=ownership();patch=load(OUT/'PATCH.json');checks={}
    checks['patched_files_match_reviewed_bytes']=all(sha(ROOT/r)==v for r,v in patch['patch_sha256'].items())
    checks['all_targets_exactly_one_owner']=targets_match(own,plan['targets'],ownership_before)
    approved=load(BASE/'HBC-05/COMPACT_BLOCKS.json')
    checks['approved_hbc_contour_exact']={r for r,v in own.items() if any(t=='HBC' for s,t in v)}==set(approved['hbc_rgb'])
    checks['approved_ont_contour_exact']={r for r,v in own.items() if any(t=='ONT' for s,t in v)}==set(approved['ont_rgb'])
    before=load(OUT/'BASELINE_RUNTIME.json');after=runtime();changed={r for r in set(before)|set(after) if before.get(r)!=after.get(r)}
    checks['no_other_runtime_file_changed']=changed==set(patch['patch_sha256'])
    checks.update(conservation(load(BASE/'HBC-03/CONSERVATION_BASELINE.json'),economic_inventory()))
    checks['bitmap_unchanged']=sha(ROOT/'map_data/provinces.png')==patch['bitmap_sha256']
    # Compare every non-HBC POP declaration by semantic content with the captured file.
    def pop_rows(raw):
        out=[]
        for s in walk(parse(raw)):
            if not s.key.startswith('s:STATE_'):continue
            for rs in s.children():
                if rs.key.startswith('region_state:') and rs.key!='region_state:HBC':
                    out.append((s.key,rs.key,[(n.key,n.op,scalar(n.value)) for p in rs.children('create_pop') for n in p.children()]))
        return out
    checks['all_other_existing_pops_unchanged']=pop_rows(text(OUT/'before'/PP))==pop_rows(text(ROOT/PP))
    # Existing ownership outside the specific HBC/ONT blocks stays byte-equivalent.
    def other_states(raw):
        from hbc03_quebec_arc import canonical
        result=[]
        for s in walk(parse(raw)):
            if not s.key.startswith('s:STATE_'):continue
            for n in s.children('create_state'):
                t=scalar(n.one('country')).removeprefix('c:')
                if t not in {'HBC','ONT'}|{g[0] for g in GROUPS}:result.append((s.key,canonical(n,s.key[2:])))
        return result
    checks['all_other_territorial_owners_unchanged']=other_states(text(OUT/'before'/ST))==other_states(text(ROOT/ST))
    pops=[n for s in parse(text(ROOT/f'common/history/pops/{PREFIX}.txt')) for st in s.children() for rs in st.children() for n in rs.children('create_pop')]
    checks['new_population_exactly_2400000']=sum(int(n.one('size')) for n in pops)==2400000
    checks['all_thirteen_groups_populated']=all(sum(r['population'] for r in plan['populations'] if r['tag']==g[0])>0 for g in GROUPS)
    checks['new_pop_states_exist']=all(any((r['state'],r['tag']) in v for v in own.values()) for r in plan['populations'])
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
    impass=set();members={}
    for path in effective('map_data/state_regions'):
        for n in parse(text(path)):
            if n.key.startswith('STATE_'):
                members[n.key]=set(provs(n,'provinces'));impass.update(int(r[1:],16) for r in provs(n,'impassable'))
    checks['province_state_references_valid']=all(r in members[s] for r,v in own.items() if r in plan['targets'] for s,t in v)
    adjfile=ROOT/'map_data/adjacencies.csv'
    if not adjfile.exists():adjfile=GAME/'map_data/adjacencies.csv'
    blocked=set()
    for row in csv.DictReader(adjfile.open(encoding='utf-8-sig'),delimiter=';'):
        if all(row.get(k,'').startswith('x') for k in ['From','To']) and (row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip()):blocked.add(pair(int(row['From'][1:],16),int(row['To'][1:],16)))
    witness=load(BASE/'HBC-04/PIXEL_PATH_WITNESS.json');points=[r['pixel'] for r in witness]
    labels=[next(iter(own[f'x{int(a[y,x]):06X}']))[1] for x,y in points]
    checks['actual_land_path_hbc_ont_usa']=list(dict.fromkeys(labels))==['HBC','ONT','USA']
    checks['actual_land_path_passable']=all(int(a[y,x]) not in impass for x,y in points) and all(abs(x-u)+abs(y-v)==1 and pair(int(a[y,x]),int(a[v,u])) not in blocked for (x,y),(u,v) in zip(points,points[1:]))
    posts=load(BASE/'HBC-02/POST_CANDIDATES.json')+[dict(diagnostic_cell=load(BASE/'HBC-03/EASTMAIN_CANDIDATE.json')['post']['diagnostic_cell'])]
    seed=points[0][1]*a.shape[1]+points[0][0];mask=np.isin(a,[int(r[1:],16) for r in approved['hbc_rgb']])&~np.isin(a,sorted(impass))
    reached,_=flood(a,mask,[seed],blocked)
    checks['all_five_posts_still_connected']=all(int(p['diagnostic_cell'][1])*a.shape[1]+int(p['diagnostic_cell'][0]) in reached for p in posts)
    definitions={n.key:n for p in effective('common/country_definitions') for n in parse(text(p))}
    checks['thirteen_decentralized_animist_definitions']=all(definitions[g[0]].one('country_type')=='decentralized' and definitions[g[0]].one('religion')=='animist' for g in GROUPS)
    checks['capitals_owned']=all(any((scalar(definitions[g[0]].one('capital')),g[0]) in v for v in own.values()) for g in GROUPS)
    checks['claims_present_in_four_regions']=all(any(scalar(n.value)=='c:HBC' for n in state_nodes(text(ROOT/ST))[sid].children('add_claim')) for sid in CLAIMS)
    checks['no_blanket_arctic_claim']=not any(scalar(n.value)=='c:HBC' for n in state_nodes(text(ROOT/ST))['STATE_NUNAVUT'].children('add_claim'))
    checks['regional_cultures_have_homelands']=all(any(scalar(n.value)=='cu:'+r['culture'] for n in state_nodes(text(ROOT/ST))[r['state']].children('add_homeland')) for r in plan['populations'])
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),engine_tested=False,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',runtime_files_changed=sorted(changed)))
    print(json.dumps(checks,indent=2));assert all(checks.values()),checks
    preview(a,own,plan)


def ownership_before(r):
    # Frozen CSV has one row per affected existing province.
    if not hasattr(ownership_before,'rows'):
        ownership_before.rows={v['RGB']:{(v['State_ID'],v['Before'])} for v in csv.DictReader((OUT/'PROVINCES.csv').open(encoding='utf-8-sig'))}
    return ownership_before.rows[r]


def preview(a,own,plan):
    colors={g[0]:g[5] for g in GROUPS}|{'HBC':[235,183,50],'ONT':[175,114,163],'USA':[62,101,128]}
    canvas=np.full((*a.shape,3),[37,48,58],dtype=np.uint8)
    all_land={int(r[1:],16) for r in own};canvas[np.isin(a,sorted(all_land))]=[100,112,109]
    for tag,color in colors.items():canvas[np.isin(a,[int(r[1:],16) for r,v in own.items() if any(t==tag for s,t in v)])]=color
    edge=np.zeros(a.shape,bool);edge[1:]|=a[1:]!=a[:-1];edge[:,1:]|=a[:,1:]!=a[:,:-1];canvas[edge&np.isin(a,sorted(all_land))]=[45,49,48]
    x0,y0,x1,y1=1500,0,2820,1120
    crop=Image.fromarray(canvas[y0:y1,x0:x1]);sheet=Image.new('RGB',(crop.width+340,crop.height+115),'#25303a');sheet.paste(crop,(0,80));d=ImageDraw.Draw(sheet)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23);sm=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    d.text((15,10),'HBC — contour intégré et peuples décentralisés',font=f,fill='white')
    d.text((15,45),'13 ensembles régionaux ; 2 400 000 habitants ajoutés pour le gameplay. Frontières approximatives.',font=sm,fill='white')
    for i,(tag,color) in enumerate(colors.items()):
        g=next((g for g in GROUPS if g[0]==tag),None);name=g[1] if g else {'HBC':'Compagnie de la Baie d’Hudson','ONT':'Haut-Canada','USA':'Treize Colonies'}[tag]
        y=95+i*38;d.rectangle((crop.width+10,y,crop.width+28,y+18),fill=tuple(color));d.text((crop.width+37,y-2),name,font=sm,fill='white')
    d.text((15,sheet.height-27),'108 626 habitants HBC et tous ses bâtiments conservés ; chargement moteur à vérifier.',font=sm,fill='white');sheet.save(OUT/'INTEGRATED_MAP.png')


if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--validate' in sys.argv:validate()
    else:raise SystemExit('Use --prepare, --apply or --validate.')
