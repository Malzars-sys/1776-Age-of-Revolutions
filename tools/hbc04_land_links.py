"""Prepare the player-required HBC -> ONT -> USA land chain, without applying it.

All paths use actual side-adjacent pixels, existing ownership and native
impassability rules. A physical path is not an engine military-access test.
"""
import collections as C
import csv
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from validate_diplomacy_ottoman_1776 import parse,walk,scalar
from hbc03_quebec_arc import economic_inventory,conservation

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-04'
PRIOR=OUT.parent/'HBC-03'


def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pair(u,v):return (min(u,v)<<24)|max(u,v)


def flood(a,mask,seeds,blocked,goals=None):
    """BFS over cell edges, with native province-pair overrides respected."""
    height,width=a.shape;flat=a.ravel();allowed=mask.ravel();parents={int(v):int(v) for v in seeds if allowed[int(v)]}
    queue=C.deque(sorted(parents))
    while queue:
        u=queue.popleft()
        if goals is not None and u in goals:return parents,u
        y,x=divmod(u,width)
        for v in ([u-1] if x else [])+([u+1] if x+1<width else [])+([u-width] if y else [])+([u+width] if y+1<height else []):
            if not allowed[v] or v in parents:continue
            first,second=int(flat[u]),int(flat[v])
            if first!=second and pair(first,second) in blocked:continue
            parents[v]=u;queue.append(v)
    return parents,None


def path(parents,end):
    result=[end]
    while parents[result[-1]]!=result[-1]:result.append(parents[result[-1]])
    return result[::-1]


def contacts(a,first,second,blocked):
    width=a.shape[1];flat=a.ravel();result=[]
    for p,q,off1,off2 in [(first[:,:-1],second[:,1:],0,1),(first[:,1:],second[:,:-1],1,0),(first[:-1,:],second[1:,:],0,width),(first[1:,:],second[:-1,:],width,0)]:
        yy,xx=np.where(p&q)
        for y,x in zip(yy.tolist(),xx.tolist()):
            origin=y*width+x;u=origin+off1;v=origin+off2
            if pair(int(flat[u]),int(flat[v])) not in blocked:result.append((u,v))
    return result


def main():
    OUT.mkdir(parents=True,exist_ok=True);before=runtime()
    previous=load(PRIOR/'EASTMAIN_CANDIDATE.json');base={int(v[1:],16) for v in previous['rgb']}
    expected=next(v['sha256'] for v in load(OUT.parent/'HBC-02/INPUTS.json') if v['path']=='map_data/provinces.png')
    bitmap_sha=sha(ROOT/'map_data/provinces.png')
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2];width=a.shape[1]
    owners=C.defaultdict(set)
    for source in effective('common/history/states'):
        for s in walk(parse(source.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            for n in s.children('create_state'):
                tag=scalar(n.one('country','')).removeprefix('c:')
                for rgb in provs(n,'owned_provinces'):owners[int(rgb[1:],16)].add((s.key[2:],tag))
    countries={tag:{rgb for rgb,values in owners.items() if any(t==tag for sid,t in values)} for tag in ['HBC','ONT','USA']}
    assert base<=countries['HBC']
    assert all(len(owners[v])==1 for values in countries.values() for v in values)
    # Do not restore an old global bitmap when other regional work changed it.
    # Revalidate HBC locally against its frozen 1:1 diagnostic mask, province
    # areas, state ownership and site anchors, then plan on the CURRENT raster.
    audit_folder=OUT.parent/'HBC-01';old_inventory=load(audit_folder/'INVENTORY.json')
    old_rows=list(csv.DictReader((audit_folder/'HBC_PROVINCE_REGISTER.csv').open(encoding='utf-8-sig')))
    old_hbc={int(r['Province_RGB'][1:],16) for r in old_rows}
    values,counts=np.unique(a,return_counts=True);sizes=dict(zip(map(int,values),map(int,counts)))
    x0,y0,x1,y1=old_inventory['bitmap_bbox'];height,box_width=y1-y0,x1-x0
    old_image=np.asarray(Image.open(audit_folder/'CURRENT_HBC_EXTENT.png').convert('RGB'))
    assert old_image.shape[:2]==(height+165,max(1000,box_width)),'Old mask was scaled: independently refresh geography.'
    offset=(old_image.shape[1]-box_width)//2
    old_mask=np.all(old_image[65:65+height,offset:offset+box_width]==[222,179,61],axis=2)
    revalidation=dict(previous_global_bitmap_sha256=expected,current_global_bitmap_sha256=bitmap_sha,global_bitmap_changed=expected!=bitmap_sha,hbc_rgb_set_unchanged=old_hbc==countries['HBC'],all_hbc_province_areas_unchanged=all(sizes.get(int(r['Province_RGB'][1:],16),0)==int(r['Bitmap_pixels']) for r in old_rows),hbc_footprint_changed_cells=int(np.count_nonzero(old_mask!=np.isin(a[y0:y1,x0:x1],sorted(countries['HBC'])))))
    prior_rows=list(csv.DictReader((PRIOR/'PROVINCES.csv').open(encoding='utf-8-sig')))
    revalidation['prior_selection_state_and_owner_unchanged']=all(owners[int(r['RGB'][1:],16)]=={(r['State_ID'],'HBC')} for r in prior_rows)
    assert revalidation['hbc_rgb_set_unchanged'] and revalidation['all_hbc_province_areas_unchanged'] and revalidation['hbc_footprint_changed_cells']==0 and revalidation['prior_selection_state_and_owner_unchanged'],revalidation
    impassable=set()
    for source in effective('map_data/state_regions'):
        for n in parse(source.read_text(encoding='utf-8-sig')):
            impassable.update(int(v[1:],16) for v in provs(n,'impassable'))
    rel=Path('map_data/adjacencies.csv');adjfile=ROOT/rel if (ROOT/rel).exists() else GAME/rel
    blocked=set();overrides=[]
    for row in csv.DictReader(adjfile.open(encoding='utf-8-sig'),delimiter=';'):
        if not all(row.get(k,'').startswith('x') for k in ['From','To']):continue
        u,v=int(row['From'][1:],16),int(row['To'][1:],16)
        if row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip():
            blocked.add(pair(u,v));overrides.append(row)
    masks={tag:np.isin(a,sorted(values-impassable)) for tag,values in countries.items()}
    ont_usa=contacts(a,masks['ONT'],masks['USA'],blocked)
    assert ont_usa,'No unblocked side-adjacent ONT-USA land border: a different territorial dependency must be planned.'
    usa_by_seed={}
    for u,v in ont_usa:usa_by_seed.setdefault(u,v)
    ont_parents,_=flood(a,masks['ONT'],usa_by_seed,blocked)
    hbc_ont=contacts(a,masks['HBC'],masks['ONT'],blocked)
    goals={}
    for u,v in hbc_ont:
        if v in ont_parents:goals.setdefault(u,v)
    assert goals,'No existing-HBC contact to the USA-connected part of ONT.'
    posts=load(OUT.parent/'HBC-02/POST_CANDIDATES.json')+[dict(name='Eastmain House',diagnostic_cell=previous['post']['diagnostic_cell'])]
    points=[math.floor(p['diagnostic_cell'][1])*width+math.floor(p['diagnostic_cell'][0]) for p in posts]
    expected_site_rgb=[p['diagnostic_rgb'] for p in posts[:-1]]+[previous['post']['diagnostic_rgb']]
    revalidation['all_post_rgb_anchors_unchanged']=all(f'x{int(a.ravel()[v]):06X}'==rgb for v,rgb in zip(points,expected_site_rgb))
    assert revalidation['all_post_rgb_anchors_unchanged'],revalidation
    dump('INPUT_REVALIDATION.json',revalidation)
    seed=next(v for p,v in zip(posts,points) if p['name']=='Moose Factory')
    base_mask=np.isin(a,sorted(base))&masks['HBC']
    base_parents,_=flood(a,base_mask,[seed],blocked)
    assert all(v in base_parents for v in points),'An existing post is disconnected under native passability rules; repair that route before proceeding.'
    bridge_parents,end=flood(a,masks['HBC'],base_parents,blocked,goals)
    assert end is not None,'No terrestrial HBC bridge to Upper Canada without another owner.'
    bridge=path(bridge_parents,end);hbc_route=path(base_parents,bridge[0])+bridge[1:]
    ont_entry=goals[end];ont_route=path(ont_parents,ont_entry)[::-1];usa_pixel=usa_by_seed[ont_route[-1]]
    bridge_rgb={int(a.ravel()[v]) for v in bridge};selected=base|bridge_rgb;added=selected-base
    ont_protected={int(a.ravel()[v]) for v in ont_route}
    def point(v):return [v%width,v//width]
    def label(v):return f'x{int(a.ravel()[v]):06X}'
    def country(v):return next(iter(owners[int(a.ravel()[v])]))[1]
    def edge(u,v):return dict(from_country=country(u),to_country=country(v),from_rgb=label(u),to_rgb=label(v),from_pixel=point(u),to_pixel=point(v))
    full_route=hbc_route+ont_route+[usa_pixel]
    def route_row(v):
        sid,tag=next(iter(owners[int(a.ravel()[v])]))
        return dict(pixel=point(v),rgb=label(v),state=sid,owner=tag)
    # Certify the actual witness cell path, not merely a country-level graph.
    valid_steps=all(abs(u%width-v%width)+abs(u//width-v//width)==1 and pair(int(a.ravel()[u]),int(a.ravel()[v])) not in blocked for u,v in zip(full_route,full_route[1:]))
    economy=conservation(load(PRIOR/'CONSERVATION_BASELINE.json'),economic_inventory())
    checks={**economy,'local_hbc_inputs_revalidated_after_global_bitmap_change':all(revalidation[k] for k in ['hbc_rgb_set_unchanged','all_hbc_province_areas_unchanged','prior_selection_state_and_owner_unchanged','all_post_rgb_anchors_unchanged']) and revalidation['hbc_footprint_changed_cells']==0,'old_228_provinces_retained':base<=selected,'bridge_uses_current_hbc_land_only':bridge_rgb<=countries['HBC'],'hbc_ont_border_has_shared_edge':end in goals,'ont_usa_border_has_shared_edge':bool(ont_usa),'same_ont_territory_reaches_both_borders':all(country(v)=='ONT' for v in ont_route),'witness_has_no_diagonal_sea_or_forbidden_step':valid_steps,'witness_country_chain_exact':list(dict.fromkeys(country(v) for v in full_route))==['HBC','ONT','USA'],'all_five_posts_passably_connected':all(v in base_parents for v in points),'no_impassable_province_used':not bool({int(a.ravel()[v]) for v in full_route}&impassable)}
    dump('LAND_LINK_CANDIDATE.json',dict(date='2026-10-25',status='PLAYER_REQUIRED_LAND_CONNECTION_PREPARED_NOT_APPLIED',country_chain=['HBC','ONT','USA'],hbc_provinces=len(selected),hbc_added_provinces=len(added),rgb=sorted(f'x{v:06X}' for v in selected),added_hbc_rgb=sorted(f'x{v:06X}' for v in added),protected_ont_rgb=sorted(f'x{v:06X}' for v in ont_protected),borders=[edge(end,ont_entry),edge(ont_route[-1],usa_pixel)],hbc_route_pixels=len(hbc_route),ont_route_pixels=len(ont_route),usa_contact_pixel=point(usa_pixel),current_hbc_ont_border_edges=len(hbc_ont),current_ont_usa_border_edges=len(ont_usa),gameplay_files_modified=[],military_access_engine_tested=False,historical_claim_for_gameplay_bridge=False,population_baseline_unchanged=108626,prior_conservation_plan='../HBC-03/CONSERVATION_PLAN.json',inputs=dict(bitmap_sha256=sha(ROOT/'map_data/provinces.png'),adjacencies_file=str(adjfile),adjacencies_sha256=sha(adjfile))))
    dump('PIXEL_PATH_WITNESS.json',[route_row(v) for v in full_route])
    dump('NATIVE_PASSABILITY.json',dict(impassable_provinces_count=len(impassable),base_proposal_impassable_rgb=sorted(f'x{v:06X}' for v in base&impassable),excluded_special_adjacencies=overrides,sea_crossings_allowed=False))
    with (OUT/'PROTECTED_PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['RGB','State_ID','Owner_to_preserve','Role']);writer.writeheader()
        for rgb in sorted(selected|ont_protected):
            sid,tag=next(iter(owners[rgb]));role='HBC_EXISTING_PROPOSAL' if rgb in base else 'HBC_SOUTHERN_LINK' if rgb in added else 'ONT_LAND_ROUTE_TO_USA'
            writer.writerow(dict(RGB=f'x{rgb:06X}',State_ID=sid,Owner_to_preserve=tag,Role=role))
    x0,y0,x1,y1=1600,400,2490,1100;scale=2
    canvas=np.zeros((*a.shape,3),dtype=np.uint8);canvas[:]=(37,48,58)
    canvas[np.isin(a,sorted(countries['HBC']))]=(112,101,73);canvas[np.isin(a,sorted(countries['ONT']))]=(128,86,117);canvas[np.isin(a,sorted(countries['USA']))]=(62,101,128)
    canvas[np.isin(a,sorted(selected))]=(235,183,50);canvas[np.isin(a,sorted(added))]=(239,135,58);canvas[np.isin(a,sorted(ont_protected))]=(204,132,186)
    borders=np.zeros(a.shape,dtype=bool);borders[:,1:]|=a[:,1:]!=a[:,:-1];borders[1:,:]|=a[1:,:]!=a[:-1,:];canvas[borders]=(40,48,51)
    crop=Image.fromarray(canvas[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(crop.width,crop.height+170),'#25303a');sheet.paste(crop,(0,90));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    draw.text((15,8),'Continuité terrestre : HBC → Haut-Canada → Treize Colonies',font=font,fill='white')
    draw.text((15,44),'Jaune HBC ; orange raccord ajouté ; rose passage du Haut-Canada ; bleu Treize Colonies.',font=small,fill='white')
    def plot(v):x,y=point(v);return ((x-x0)*scale,90+(y-y0)*scale)
    draw.line([plot(v) for v in full_route],fill='white',width=2)
    for i,p in enumerate(posts):
        x,y=p['diagnostic_cell'];cx=(x-x0)*scale;cy=90+(y-y0)*scale
        draw.ellipse((cx-5,cy-5,cx+5,cy+5),fill='white',outline='black',width=2)
        dx,dy=[(12,12),(12,12),(12,-28),(12,-28),(-160,-28)][i]
        draw.text((cx+dx,cy+dy),p['name'],font=small,fill='white',stroke_width=2,stroke_fill='black')
    for v,text,offset in [(end,'HBC / Haut-Canada',(-205,-27)),(ont_route[-1],'Frontière américaine',(-200,15))]:
        cx,cy=plot(v);draw.ellipse((cx-7,cy-7,cx+7,cy+7),fill='#ef766a',outline='white',width=2);dx,dy=offset;draw.text((cx+dx,cy+dy),text,font=small,fill='white',stroke_width=2,stroke_fill='black')
    draw.text((15,sheet.height-65),f'{len(selected)} provinces HBC proposées, dont {len(added)} pour le raccord. Aucun territoire décentralisé sur le trajet blanc.',font=small,fill='white')
    draw.text((15,sheet.height-36),'Proposition non appliquée. Population et bâtiments protégés ; accès militaire à confirmer en jeu.',font=small,fill='white');sheet.save(OUT/'LAND_LINKS.png')
    checks['no_runtime_change']=before==runtime();dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),engine_tested=False,gameplay_files_modified=[]))
    print(json.dumps(dict(checks=checks,hbc_provinces=len(selected),added_provinces=len(added),protected_ont_provinces=len(ont_protected),borders=[edge(end,ont_entry),edge(ont_route[-1],usa_pixel)]),ensure_ascii=False))
    assert all(checks.values()),checks


if __name__=='__main__':main()
