"""HBC: protected demographic/economic baseline and Eastmain arc proposal.

Writes reports only. --check-conservation checks current histories against the
frozen gameplay baseline without replacing it. No ownership patch is applied.
"""
import collections as C
import csv
import heapq
import json
import math
from pathlib import Path
import sys

import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from validate_diplomacy_ottoman_1776 import parse,walk,scalar
from hbc02_map_candidates import graph,pixel_components
from georeference.model import forward

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-03'
PRIOR=OUT.parent/'HBC-02'


def dump(name,o):(OUT/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))


def canonical(n,sid):
    value=[canonical(v,sid) for v in n.children()] if isinstance(n.value,list) else scalar(n.value)
    if n.key=='region' and value==sid:value='$BUILDING_LOCATION'
    return [n.key,n.op,value]


def economic_inventory():
    pops=[];buildings=[];sources={}
    for kind,rows in [('pops',pops),('buildings',buildings)]:
        for path in effective('common/history/'+kind):
            raw=path.read_text(encoding='utf-8-sig')
            if 'region_state:HBC' not in raw:continue
            for s in walk(parse(raw)):
                if not s.key.startswith('s:STATE_'):continue
                sid=s.key[2:]
                for region in s.children('region_state:HBC'):
                    for n in region.children('create_pop' if kind=='pops' else 'create_building'):
                        rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else 'VANILLA:'+path.relative_to(GAME).as_posix()
                        sources[rel]=sha(path)
                        common=dict(state=sid,file=rel,line=raw.count('\n',0,n.start)+1)
                        if kind=='pops':rows.append(dict(**common,culture=scalar(n.one('culture')),religion=scalar(n.one('religion','DEFAULT')),size=int(n.one('size',0))))
                        else:rows.append(dict(**common,building=scalar(n.one('building')),normalized_command=canonical(n,sid)))
    population=C.Counter()
    for r in pops:population[(r['culture'],r['religion'])]+=r['size']
    groups=C.defaultdict(list)
    for r in buildings:groups[r['building']].append(r['normalized_command'])
    existing=set()
    for path in effective('common/history/states'):
        for s in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            for n in s.children('create_state'):
                if scalar(n.one('country',''))=='c:HBC' and provs(n,'owned_provinces'):existing.add(s.key[2:])
    return dict(population=sum(r['size'] for r in pops),population_by_culture_religion=[dict(culture=c,religion=r,size=n) for (c,r),n in sorted(population.items())],pops=pops,building_commands=buildings,ordered_building_commands_by_type=dict(groups),source_hashes=sources,hbc_owned_states=sorted(existing))


def conservation(baseline,current):
    existing=set(current['hbc_owned_states'])
    return dict(total_population_preserved=current['population']==baseline['population'],cultures_religions_preserved=current['population_by_culture_religion']==baseline['population_by_culture_religion'],building_commands_levels_pms_owners_preserved=current['ordered_building_commands_by_type']==baseline['ordered_building_commands_by_type'],all_pop_states_exist_under_hbc=all(r['state'] in existing for r in current['pops']),all_building_states_exist_under_hbc=all(r['state'] in existing for r in current['building_commands']))


def route_to_existing(adj,sizes,distance,start,goal):
    q=[(0.,start)];best={start:0.};previous={}
    while q:
        cost,u=heapq.heappop(q)
        if best[u]!=cost:continue
        if u in goal:
            path=[u]
            while path[-1]!=start:path.append(previous[path[-1]])
            return path[::-1]
        for v in sorted(adj[u]):
            nxt=cost+1+math.sqrt(sizes[v])/20+8*distance.get(v,1000)
            if nxt<best.get(v,float('inf')):best[v]=nxt;previous[v]=u;heapq.heappush(q,(nxt,v))
    return []


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    current=economic_inventory();baseline_file=OUT/'CONSERVATION_BASELINE.json'
    if not baseline_file.exists():
        assert '--check-conservation' not in sys.argv,'No frozen baseline exists.'
        assert current['population']==108626,'Reconcile starting population with HBC-01 before freezing a new baseline.'
        dump('CONSERVATION_BASELINE.json',dict(date='2026-10-25',authority='Player: keep all current HBC population and buildings despite territorial decentralization',**current))
    baseline=load(baseline_file);economy_checks=conservation(baseline,current)
    assert all(economy_checks.values()),economy_checks
    if '--check-conservation' in sys.argv:
        dump('CONSERVATION_CHECK.json',dict(checks=economy_checks,all_pass=True,scope='Declared country population and ordered building history commands; engine not run'))
        print(json.dumps(economy_checks));return
    before=runtime();base_data=load(PRIOR/'COASTAL_CANDIDATE.json');posts=load(PRIOR/'POST_CANDIDATES.json')
    expected=next(v['sha256'] for v in load(PRIOR/'INPUTS.json') if v['path']=='map_data/provinces.png')
    assert sha(ROOT/'map_data/provinces.png')==expected,'Base bitmap changed.'
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
    owners=C.defaultdict(set)
    for path in effective('common/history/states'):
        for s in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            for n in s.children('create_state'):
                tag=scalar(n.one('country','')).removeprefix('c:')
                for rgb in provs(n,'owned_provinces'):owners[int(rgb[1:],16)].add((s.key[2:],tag))
    hbc={rgb for rgb,values in owners.items() if any(t=='HBC' for sid,t in values)}
    assert all(len(owners[rgb])==1 for rgb in hbc)
    base={int(v[1:],16) for v in base_data['rgb']};assert base<=hbc
    bay={int(v[1:],16) for v in base_data['water_region']['rgb']}
    full=graph(a,np.asarray(sorted(hbc|bay),dtype=np.uint32))
    adjacency={u:{v:n for v,n in neighbours.items() if v in hbc} for u,neighbours in full.items() if u in hbc}
    coastal={v for water in bay for v in full[water] if v in hbc}
    distance={v:0 for v in coastal};q=C.deque(sorted(coastal))
    while q:
        u=q.popleft()
        for v in adjacency[u]:
            if v not in distance:distance[v]=distance[u]+1;q.append(v)
    # Modern river-mouth proxy from Canadian Hydrographic Service directions.
    # Do not describe this as a surveyed position of the 1776 buildings.
    geo=[-78.5,52.25];model=load(PRIOR/'MODELS.json')['miller_affine'];predicted=forward(model,[geo])[0]
    quebec={rgb for rgb in hbc if ('STATE_QUEBEC','HBC') in owners[rgb]}
    yy,xx=np.where(np.isin(a,sorted(quebec)));nearest=int(np.argmin((xx-predicted[0])**2+(yy-predicted[1])**2))
    point=[int(xx[nearest]),int(yy[nearest])];start=int(a[point[1],point[0]])
    route=route_to_existing(adjacency,dict(zip(*np.unique(a,return_counts=True))),distance,start,base)
    assert route,'No continuous existing-HBC route to Eastmain; cannot add an isolated post.'
    selected=base|set(route);baymask=np.isin(a,sorted(bay));owned=np.isin(a,sorted(hbc));spine=np.isin(a,route);slices=[]
    # East bank: fill the land WEST of the new line toward James Bay.
    # The existing west-bank infill is retained rather than recomputed.
    for y in np.where(np.any(spine,axis=1))[0]:
        right=int(np.flatnonzero(spine[y])[-1]);west=np.flatnonzero(baymask[y,:right])
        if not len(west):continue
        left=int(west[-1])+1
        selected.update(int(v) for v in np.unique(a[y,left:right+1][owned[y,left:right+1]]))
        slices.append(dict(y=int(y),bay_edge=left,inland_edge=right))
    east=dict(name='Eastmain House',geo_proxy=geo,predicted_pixel=predicted.tolist(),diagnostic_cell=point,diagnostic_rgb=f'x{start:06X}',state='STATE_QUEBEC',geo_proxy_source='https://publications.gc.ca/collections/collection_2022/mpo-dfo/Fs74-6-2021-12-eng.pdf',site_position_historically_certified=False,date_status='SUPPORTED_PRE_1776_YEAR_ROUND_FROM_1771',history_source='https://www.collectionscanada.gc.ca/obj/s4/f2/dsk3/MWU/TC-MWU-230.pdf#page=163')
    points=[p['diagnostic_cell'] for p in posts]+[point];mask=np.isin(a,sorted(selected));roots,parts,_=pixel_components(mask,points)
    proposed_states={sid for rgb in selected for sid,tag in owners[rgb] if tag=='HBC'}
    pop_plan=[];by_state=C.Counter()
    for p in baseline['pops']:
        target=p['state'] if p['state'] in proposed_states else 'STATE_MANITOBA'
        assert target in proposed_states
        by_state[target]+=p['size'];pop_plan.append(dict(**p,target_state=target,action='KEEP' if target==p['state'] else 'RELOCATE_WITHIN_HBC_FOR_GAMEPLAY'))
    building_plan=[]
    for r in baseline['building_commands']:
        target=r['state'] if r['state'] in proposed_states else 'STATE_MANITOBA'
        building_plan.append(dict(source_state=r['state'],target_state=target,building=r['building'],source_file=r['file'],source_line=r['line'],action='KEEP' if target==r['state'] else 'RELOCATE_WITHIN_HBC_FOR_GAMEPLAY',preserve_full_command=True))
    dump('CONSERVATION_PLAN.json',dict(status='PREPARED_NOT_APPLIED',population=baseline['population'],population_by_target_state=dict(by_state),pop_commands=pop_plan,building_history_commands=len(building_plan),building_commands=building_plan,preserve_pms_levels_reserves_and_economic_owners=True,keep_transferred_people_under_hbc=True,duplicate_population_for_new_decentralized_holders=False,gameplay_abstraction_not_historical_migration=True))
    checks={**economy_checks,'old_proposal_retained':base<=selected,'all_five_posts_connected':len(set(roots))==1 and roots[0]>0,'route_only_shared_edges':all(adjacency[u].get(v,0)>0 for u,v in zip(route,route[1:])),'all_selected_still_hbc':selected<=hbc,'no_sea_selected':not bool(selected&bay),'population_plan_conserves_total':sum(by_state.values())==baseline['population'],'building_plan_conserves_all_commands':len(building_plan)==len(baseline['building_commands'])}
    dump('EASTMAIN_CANDIDATE.json',dict(status='COASTAL_ARC_PROPOSAL_NOT_APPLIED',post=east,route=[f'x{v:06X}' for v in route],route_cost='1+sqrt(province pixels)/20+8*minimum land-province hops from Hudson Bay coast',rgb=sorted(f'x{v:06X}' for v in selected),provinces=len(selected),added_to_coastal_proposal=len(selected-base),pixels=int(mask.sum()),coastal_slices=slices,post_pixel_components=roots,pixel_component_sizes=sorted(parts,reverse=True),historical_route_certified=False,runtime_market_tested=False,gameplay_files_modified=[]))
    with (OUT/'PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['RGB','State_ID','Owner_current','Role']);w.writeheader()
        for rgb in sorted(selected):w.writerow(dict(RGB=f'x{rgb:06X}',State_ID=next(iter(owners[rgb]))[0],Owner_current='HBC',Role='EXISTING_COASTAL_PROPOSAL' if rgb in base else 'EASTMAIN_ARC'))
    x0,y0,x1,y1=1600,400,2420,925;scale=2
    canvas=np.zeros((*a.shape,3),dtype=np.uint8);canvas[:]=(37,48,58);canvas[owned]=(112,101,73);canvas[mask]=(235,183,50)
    edges=np.zeros(a.shape,dtype=bool);edges[:,1:]|=a[:,1:]!=a[:,:-1];edges[1:,:]|=a[1:,:]!=a[:-1,:];canvas[edges&owned]=(52,53,51)
    crop=Image.fromarray(canvas[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(crop.width,crop.height+145),'#25303a');sheet.paste(crop,(0,80));d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    d.text((15,8),'HBC — arc côtier prolongé jusqu’à Eastmain, côté Québec',font=font,fill='white')
    d.text((15,40),'Jaune : proposition ; brun : reste de la HBC actuelle. Aucun transfert appliqué au jeu.',font=small,fill='white')
    all_posts=[dict(name=p['name'],point=p['diagnostic_cell']) for p in posts]+[dict(name='Eastmain House',point=point)]
    for i,p in enumerate(all_posts):
        x,y=p['point'];cx=(x-x0)*scale;cy=80+(y-y0)*scale;d.ellipse((cx-6,cy-6,cx+6,cy+6),fill='white',outline='black',width=2)
        dx,dy=[(12,12),(12,12),(12,-28),(12,-28),(-155,-28)][i];d.text((cx+dx,cy+dy),p['name'],font=small,fill='white',stroke_width=2,stroke_fill='black')
    d.text((15,sheet.height-52),f'{len(selected)} provinces candidates ; cinq postes reliés ; remplissage jusqu’au littoral.',font=small,fill='white')
    d.text((15,sheet.height-28),'Conservation prévue : 108 626 habitants et tous les bâtiments existants. Test moteur à faire.',font=small,fill='white')
    sheet.save(OUT/'EASTMAIN_ARC.png')
    checks['no_runtime_file_modified']=before==runtime()
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),gameplay_files_modified=[],engine_tested=False))
    print(json.dumps(dict(checks=checks,provinces=len(selected),eastmain_rgb=east['diagnostic_rgb'],population_plan=dict(by_state),build_commands=len(building_plan)),ensure_ascii=False))
    assert all(checks.values()),checks


if __name__=='__main__':main()
