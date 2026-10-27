"""HBC-02: current-raster localization and connected corridor candidates.

Diagnostic only. Never modifies runtime files or imports SERG roadmaps.
Native hub calibration is approximate; computed corridors are gameplay
candidates, not a historical boundary reconstruction or an approved patch.
"""
import collections as C
import csv
import hashlib
import heapq
import json
import math
from pathlib import Path
import re
import unicodedata
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from audit_hbc_1776 import ROOT, GAME, effective, provs, runtime, sha
from validate_diplomacy_ottoman_1776 import parse, walk, scalar
from georeference.model import fit, evaluate, forward

OUT = ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-02'
GEO = ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE'
HUBS = ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv'
SIDES = ('city','port','farm','mine','wood')


def dump(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def norm(s):
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()


def geo_records():
    with zipfile.ZipFile(GEO/'cities1000.zip') as z:
        return [r for line in z.read('cities1000.txt').decode().splitlines()
                if (r := line.split('\t'))[8] == 'CA']


def controls(a, definitions):
    # Retain the catalogue's human-readable names, but re-read effective
    # locators and sample this run's bitmap rather than trust old MAP1 RGBs.
    current = {}
    for kind in SIDES:
        rel = Path(f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt')
        path = ROOT/rel if (ROOT/rel).exists() else GAME/rel
        raw = path.read_text(encoding='utf-8-sig')
        for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\}', raw):
            current[(int(m[1]),kind)] = ([float(m[2]), a.shape[0]-float(m[4])], str(path), raw.count('\n',0,m.start())+1)
    geos = geo_records()
    # Fixed FIT/CHECK roles chosen before evaluating residuals. These are
    # native named anchors, not independently surveyed historical landmarks.
    roles = {'York Factory':'FIT','Moose Factory':'FIT','Rankin Inlet':'FIT',
             'Regina':'FIT','Hay River':'FIT','Quebec':'FIT',
             'Arviat':'CHECK','Thompson':'CHECK','Fort Smith':'CHECK',
             'Saskatoon':'CHECK','Bytown':'CHECK','Montreal':'CHECK',
             'Toronto':'CHECK','Portage la Prairie':'CHECK','Sherbrooke':'CHECK',
             'Yorkton':'CHECK','Sudbury':'CHECK'}
    aliases = {'Quebec':'Québec','Bytown':'Ottawa','Montreal':'Montréal','Sudbury':'Greater Sudbury'}
    result=[]
    for old in csv.DictReader(HUBS.open(encoding='utf-8-sig')):
        name=old['Hub_Name'];sid=old['State_ID'];kind=old['Hub_Type']
        if name not in roles or sid not in {'STATE_ONTARIO','STATE_QUEBEC','STATE_SASKATCHEWAN','STATE_MANITOBA','STATE_NUNAVUT','STATE_NORTHWEST_TERRITORIES'}:continue
        if name=='York Factory':
            geo=[-92.30443,57.00271];ref='https://www.mhs.mb.ca/docs/sites/yorkfactory.shtml';note='Modern York III proxy; York II was about 1 km downstream (Parks Canada).'
        else:
            candidates=[r for r in geos if norm(r[1])==norm(aliases.get(name,name))]
            if name=='Thompson':candidates=[r for r in candidates if float(r[4])>54]
            if name=='Sherbrooke':candidates=[r for r in candidates if float(r[5])>-80]
            assert len(candidates)==1,(name,len(candidates))
            r=candidates[0];geo=[float(r[5]),float(r[4])];ref=f'GeoNames {r[0]} in retained cities1000.zip';note='Modern place reference; native locator is not a survey.'
        pos,path,line=current[(int(scalar(definitions[sid].one('id'))),kind)]
        rgb=f'x{int(a[math.floor(pos[1]),math.floor(pos[0])]):06X}'
        declared=scalar(definitions[sid].one(kind))
        valid=rgb==declared
        result.append(dict(name=name,geo=geo,pixel=pos if valid else None,observed_locator_pixel=pos,role=roles[name],quality='native_locator_not_surveyed',geo_source=ref,note=note,locator_file=path,locator_line=line,current_rgb=rgb,defined_rgb=declared,usable=valid,exclusion_reason=None if valid else 'Effective locator does not sample the current hub definition RGB; excluded before fitting/evaluation'))
    assert len(result)==len(roles)
    return result


def graph(a, allowed):
    adjacency=C.defaultdict(dict)
    for left,right in [(a[:,:-1],a[:,1:]),(a[:-1,:],a[1:,:])]:
        mask=(left!=right)&np.isin(left,allowed)&np.isin(right,allowed)
        lo=np.minimum(left[mask],right[mask]).astype(np.uint64)
        hi=np.maximum(left[mask],right[mask]).astype(np.uint64)
        pairs,counts=np.unique((lo<<24)|hi,return_counts=True)
        for p,count in zip(pairs,counts):
            x=int(p)>>24;y=int(p)&0xffffff
            adjacency[x][y]=adjacency[x].get(y,0)+int(count)
            adjacency[y][x]=adjacency[y].get(x,0)+int(count)
    return adjacency


def shortest(adj, sizes, start, destinations):
    q=[(0.,start)];distance={start:0.};previous={}
    target=None
    while q:
        cost,u=heapq.heappop(q)
        if cost!=distance[u]:continue
        if u in destinations:target=u;break
        for v in sorted(adj[u]):
            nxt=cost+1+math.sqrt(sizes[v])/20
            if nxt<distance.get(v,float('inf')):
                distance[v]=nxt;previous[v]=u;heapq.heappush(q,(nxt,v))
    if target is None:return []
    route=[target]
    while route[-1]!=start:route.append(previous[route[-1]])
    return route[::-1]


def pixel_components(mask, points):
    yy,xx=np.where(mask);remaining=set(zip(xx.tolist(),yy.tolist()))
    labels={};sizes=[]
    while remaining:
        seed=remaining.pop();number=len(sizes)+1;stack=[seed];count=0
        while stack:
            x,y=stack.pop();labels[(x,y)]=number;count+=1
            for point in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if point in remaining:remaining.remove(point);stack.append(point)
        sizes.append(count)
    return [labels.get(tuple(map(math.floor,p)),0) for p in points],sizes,labels


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    before=runtime()
    dump('BASELINE_RUNTIME.json',before)
    image=Image.open(ROOT/'map_data/provinces.png').convert('RGB')
    b=np.asarray(image,dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
    owners=C.defaultdict(set);definitions={}
    for path in effective('common/history/states'):
        for s in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            for n in s.children('create_state'):
                tag=scalar(n.one('country','')).removeprefix('c:')
                for rgb in provs(n,'owned_provinces'):owners[int(rgb[1:],16)].add((s.key[2:],tag))
    for path in effective('map_data/state_regions'):
        for n in parse(path.read_text(encoding='utf-8-sig')):
            if n.key.startswith('STATE_'):definitions[n.key]=n
    hbc=sorted(rgb for rgb,values in owners.items() if any(tag=='HBC' for sid,tag in values))
    assert all(len(owners[rgb])==1 for rgb in hbc)
    rows=controls(a,definitions)
    models={kind:fit(rows,kind,a.shape[::-1]) for kind in ['miller_affine','miller_axes','geographic_affine']}
    evaluations={kind:evaluate(model) for kind,model in models.items()}
    model=models['miller_affine']
    dump('CONTROLS.json',dict(schema_version=1,dimensions=list(a.shape[::-1]),controls=rows))
    dump('MODELS.json',models)
    dump('CALIBRATION.json',evaluations)
    dump('INPUTS.json',[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in [ROOT/'map_data/provinces.png',HUBS,GEO/'cities1000.zip',GEO/'ne_10m_lakes.geojson',GEO/'ne_10m_rivers.geojson']])
    ids,counts=np.unique(a,return_counts=True);sizes=dict(zip(map(int,ids),map(int,counts)))
    adj=graph(a,np.asarray(hbc,dtype=np.uint32))
    # Use native, RGB-verified York/Moose anchors for the geometry test;
    # geographic predictions are kept separately to expose native offsets.
    posts=[dict(name='York Factory II',geo=[-92.30443,57.00271],proxy_km=1.,source='https://www.parks.canada.ca/lhn-nhs/mb/yorkfactory/info/commemoration',native_anchor='York Factory',date_status='SUPPORTED_1715_TO_1788'),
           dict(name='Moose Factory',geo=[-80.61624,51.26689],proxy_km=0.,source='GeoNames 6077991; Parks Canada Moose Factory designation',native_anchor='Moose Factory',date_status='SUPPORTED'),
           dict(name='Prince of Wales / Churchill',geo=[-94.2134278,58.7971583],proxy_km=0.1,source='https://en.wikipedia.org/wiki/Prince_of_Wales_Fort; photographed fort https://commons.wikimedia.org/wiki/File:Prince_of_Wales_Fort,_Churchill,_MB.jpg',date_status='SUPPORTED_POST_GEODETIC_PROXY'),
           dict(name='Cumberland House 1774',geo=[-102.2567,53.95804],proxy_km=2.,source='https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=736; https://www.tourismsaskatchewan.com/listings/1421/cumberland-house-provincial-historic-park',date_status='SUPPORTED_1774_POST_MOVED_1793')]
    tree=set();routes=[]
    # Retain all uncertainty candidates; choosing the nearest existing HBC
    # cell is an explicit diagnostic, never a historical decision.
    hy,hx=np.where(np.isin(a,hbc))
    for p in posts:
        predictions={kind:forward(m,[p['geo']])[0].tolist() for kind,m in models.items()}
        predicted=predictions['miller_affine'];p['model_predictions']=predictions
        p['model_spread_px']=max(math.dist(v,predicted) for v in predictions.values())
        # A sensitivity envelope, NOT a statistical confidence interval.
        local_checks=[q['residual_px'] for q in evaluations['miller_affine']['points'] if q['role']=='CHECK' and not q['extrapolated']]
        radius=max(local_checks,default=15.)+p['model_spread_px']+2.
        x,y=predicted;left=max(0,math.floor(x-radius));top=max(0,math.floor(y-radius));right=min(a.shape[1],math.ceil(x+radius)+1);bottom=min(a.shape[0],math.ceil(y+radius)+1)
        p['sensitivity_radius_px_not_confidence']=radius
        p['nearby_hbc_rgb']=[f'x{int(v):06X}' for v in sorted(set(np.unique(a[top:bottom,left:right]))&set(hbc))]
        if p.get('native_anchor'):
            anchor=next(r for r in rows if r['name']==p['native_anchor']);point=anchor['pixel'];rgb=int(anchor['current_rgb'][1:],16)
            p['native_vs_geographic_px']=math.dist(point,predicted);method='CURRENT_NATIVE_NAMED_ANCHOR'
        else:
            nearest=int(np.argmin((hx-x)**2+(hy-y)**2));point=[int(hx[nearest]),int(hy[nearest])];rgb=int(a[point[1],point[0]]);method='NEAREST_CURRENT_HBC_CELL_TO_UNCERTIFIED_PREDICTION'
        p.update(diagnostic_cell=point,diagnostic_rgb=f'x{rgb:06X}',selection_method=method,distance_to_prediction_px=math.dist(point,predicted),state_owner=[list(v) for v in sorted(owners[rgb])],historical_rgb_validated=False)
        if not tree:tree.add(rgb);route=[rgb]
        else:
            route=shortest(adj,sizes,rgb,tree);tree.update(route)
        routes.append(dict(post=p['name'],rgb_path=[f'x{v:06X}' for v in route],reachable=bool(route),consecutive_shared_edge_counts=[adj[u][v] for u,v in zip(route,route[1:])],historical_route_validated=False))
    selected=np.isin(a,sorted(tree))
    roots,component_sizes,labels=pixel_components(selected,[p['diagnostic_cell'] for p in posts])
    initial_defects=[];excluded=set();mandatory={int(p['diagnostic_rgb'][1:],16) for p in posts}
    # Whole-province ownership may retain tiny detached fragments. Do not
    # hide them or silently edit the bitmap: reroute around such RGBs.
    while len(component_sizes)>1:
        by_rgb=C.defaultdict(set)
        for (x,y),label in labels.items():by_rgb[int(a[y,x])].add(label)
        bad={rgb for rgb,parts in by_rgb.items() if len(parts)>1}
        if not bad or bad&mandatory:break
        initial_defects.append(dict(component_sizes=sorted(component_sizes,reverse=True),excluded_rgb=sorted(f'x{r:06X}' for r in bad)))
        excluded.update(bad)
        clean={u:{v:n for v,n in neighbours.items() if v not in excluded} for u,neighbours in adj.items() if u not in excluded}
        tree=set();routes=[]
        for p in posts:
            start=int(p['diagnostic_rgb'][1:],16)
            route=shortest(clean,sizes,start,tree) if tree else [start]
            tree.update(route)
            routes.append(dict(post=p['name'],rgb_path=[f'x{v:06X}' for v in route],reachable=bool(route),consecutive_shared_edge_counts=[adj[u][v] for u,v in zip(route,route[1:])],historical_route_validated=False))
        selected=np.isin(a,sorted(tree))
        roots,component_sizes,labels=pixel_components(selected,[p['diagnostic_cell'] for p in posts])
        if not all(r['reachable'] for r in routes):break
    n=len(component_sizes)
    dump('POST_CANDIDATES.json',posts)
    with (OUT/'PROVINCE_CANDIDATES.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['RGB','State_ID','Owner_current','Bitmap_pixels','Corridor_neighbours','Historical_owner_after','Applied'])
        writer.writeheader()
        for rgb in sorted(tree):
            sid,tag=next(iter(owners[rgb]))
            writer.writerow(dict(RGB=f'x{rgb:06X}',State_ID=sid,Owner_current=tag,Bitmap_pixels=sizes[rgb],Corridor_neighbours=';'.join(f'x{v:06X}' for v in sorted(adj[rgb]) if v in tree),Historical_owner_after='UNRESOLVED_CANDIDATE_ONLY',Applied=False))
    dump('CORRIDOR_CANDIDATE.json',dict(status='TECHNICAL_SENSITIVITY_SCENARIO_NOT_APPLIED',root='York Factory II',algorithm='Sequential minimum-cost paths in existing HBC province adjacency; cost 1+sqrt(province_pixels)/20, no historical route inference; reroute around detached-fragment RGBs',initial_geometry_defects=initial_defects,routes=routes,rgb=sorted(f'x{v:06X}' for v in tree),provinces=len(tree),pixels=int(selected.sum()),current_hbc_provinces=len(hbc),current_hbc_pixels=sum(sizes[r] for r in hbc),target_pixel_components=roots,pixel_component_sizes=sorted(component_sizes,reverse=True),all_post_cells_in_one_component=len(set(roots))==1 and roots[0]>0,all_selected_pixels_connected=n==1,historical_boundaries_validated=False,market_access_runtime_tested=False,incorporation_changed=False))
    # A neutral current-owner backdrop. Preview never assigns Indigenous
    # ownership or claims to grey areas and never edits the source raster.
    box=(1600,400,2420,925);x0,y0,x1,y1=box;scale=2
    canvas=np.zeros((*a.shape,3),dtype=np.uint8);canvas[:]=(37,48,58)
    canvas[np.isin(a,hbc)]=(112,101,73);canvas[selected]=(235,183,50)
    coast=np.zeros(a.shape,dtype=bool)
    coast[:,1:]|=a[:,1:]!=a[:,:-1];coast[1:,:]|=a[1:,:]!=a[:-1,:]
    canvas[coast&np.isin(a,hbc)]=(52,53,51)
    crop=Image.fromarray(canvas[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(crop.width,crop.height+145),'#25303a');sheet.paste(crop,(0,80));d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    d.text((15,8),'HBC — essai de réseau continu sur les provinces actuelles',font=font,fill='white')
    d.text((15,40),'Jaune : scénario technique ; brun : HBC actuelle. Aucun transfert appliqué.',font=small,fill='white')
    for i,p in enumerate(posts):
        x,y=p['diagnostic_cell'];cx=(x-x0)*scale;cy=80+(y-y0)*scale
        d.ellipse((cx-6,cy-6,cx+6,cy+6),fill='white',outline='black',width=2)
        label=p['name'];offsets=[(12,12),(12,12),(12,-28),(12,-28)];dx,dy=offsets[i]
        d.text((cx+dx,cy+dy),label,font=small,fill='white',stroke_width=2,stroke_fill='black')
        px,py=p['model_predictions']['miller_affine'];px=(px-x0)*scale;py=80+(py-y0)*scale
        d.line((px-5,py-5,px+5,py+5),fill='#63e5f3',width=2);d.line((px+5,py-5,px-5,py+5),fill='#63e5f3',width=2)
    d.text((15,sheet.height-52),f'{len(tree)} provinces candidates ; croix cyan = prédictions géographiques approximatives.',font=small,fill='white')
    d.text((15,sheet.height-28),'Tracé non historique ; postes incertains exclus. Accès au marché non testé dans le moteur.',font=small,fill='white')
    sheet.save(OUT/'CONNECTED_CANDIDATE.png')
    after=runtime()
    checks=dict(current_native_rgb_checks=all((r['pixel'] is not None)==(r['current_rgb']==r['defined_rgb']) for r in rows),four_targets=len(posts)==4,all_routes_reachable=all(r['reachable'] for r in routes),no_corner_only_route=all(all(n>0 for n in r['consecutive_shared_edge_counts']) for r in routes),post_cells_continuous=len(set(roots))==1 and roots[0]>0,all_selected_pixels_connected=n==1,no_runtime_change=before==after)
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),runtime_tested=False,historical_rgb_validated=False,gameplay_files_modified=[]))
    print(json.dumps(dict(checks=checks,fit=evaluations['miller_affine']['fit'],check=evaluations['miller_affine']['check'],local_check=evaluations['miller_affine']['local_check'],posts=[dict(name=p['name'],rgb=p['diagnostic_rgb'],native_offset=p.get('native_vs_geographic_px'),prediction_distance=p['distance_to_prediction_px']) for p in posts],candidate_provinces=len(tree)),ensure_ascii=False))


if __name__=='__main__':main()
