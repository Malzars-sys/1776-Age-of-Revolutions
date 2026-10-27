"""Broaden the player-marked connectors into compact provincial blocks.

Proposal data and derived map only; no runtime map or history edits.
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
from hbc03_quebec_arc import conservation,economic_inventory
from hbc04_land_links import flood,pair

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-05'
PRIOR=OUT.parent/'HBC-04'


def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def dump(name,o):(OUT/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def in_polygon(point,vertices):
    x,y=point;inside=False
    for (x1,y1),(x2,y2) in zip(vertices,vertices[1:]+vertices[:1]):
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:inside=not inside
    return inside


def main():
    OUT.mkdir(parents=True,exist_ok=True);before=runtime()
    old_proposal=OUT/'COMPACT_BLOCKS.json';saved=OUT/'BEFORE_NOTCH_INFILL.json'
    if old_proposal.exists() and not saved.exists():
        saved.write_bytes(old_proposal.read_bytes())
    previous=load(PRIOR/'LAND_LINK_CANDIDATE.json');base={int(v[1:],16) for v in previous['rgb']}
    bitmap=ROOT/'map_data/provinces.png'
    assert sha(bitmap)==previous['inputs']['bitmap_sha256'],'Revalidate the previous witness after a bitmap change.'
    b=np.asarray(Image.open(bitmap).convert('RGB'),dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2];height,width=a.shape
    owners=C.defaultdict(set)
    for source in effective('common/history/states'):
        for s in walk(parse(source.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            for n in s.children('create_state'):
                tag=scalar(n.one('country','')).removeprefix('c:')
                for rgb in provs(n,'owned_provinces'):owners[int(rgb[1:],16)].add((s.key[2:],tag))
    tags={tag:{rgb for rgb,values in owners.items() if any(t==tag for sid,t in values)} for tag in ['HBC','ONT','USA']}
    assert base<=tags['HBC'] and all(len(owners[v])==1 for t in tags.values() for v in t)
    # Gameplay envelopes taken from the player's annotated overview, in the
    # diagnostic's native pixel frame (x0=1600,y0=400,scale=2,header=90).
    # These are NOT historical or geographic squares. Whole provinces with
    # centres inside the envelopes are selected; original countries/posts
    # and protected routes have precedence at the shared boundary.
    boxes={'HBC':[2210,775,2325,904],'ONT':[2140,904,2345,995]}
    relevant=tags['HBC']|tags['ONT'];yy,xx=np.where(np.isin(a,sorted(relevant)))
    ids,inverse,count=np.unique(a[yy,xx],return_inverse=True,return_counts=True)
    mx=np.bincount(inverse,weights=xx)/count;my=np.bincount(inverse,weights=yy)/count
    centres={int(rgb):(float(x),float(y)) for rgb,x,y in zip(ids,mx,my)}
    def inside(rgb,box):
        x,y=centres[rgb];x0,y0,x1,y1=box
        return x0<=x<x1 and y0<=y<y1
    # Additional wedge explicitly marked by the player in red, immediately
    # west of the James Bay connector. Pixel frame as above; visual gameplay
    # envelope only, not a reconstructed historical border.
    notch=[[2130,754],[2205,754],[2209,801],[2229,850],[2225,876],
           [2208,847],[2190,835],[2174,812],[2157,790],[2135,776]]
    infill={rgb for rgb in tags['HBC'] if in_polygon(centres[rgb],notch)}
    hbc=base|{rgb for rgb in tags['HBC'] if inside(rgb,boxes['HBC'])}|infill
    ont_added={rgb for rgb in tags['HBC']-hbc if inside(rgb,boxes['ONT'])}
    ont=tags['ONT']|ont_added
    assert hbc.isdisjoint(ont)
    # New ONT block can use only former HBC provinces already omitted from
    # the old proposal. It cannot take the protected HBC base or another
    # country's land. This remains a future ownership change, not applied.
    proposals={'HBC':hbc,'ONT':ont};additions={'HBC':hbc-base,'ONT':ont_added}
    rel=Path('map_data/adjacencies.csv');adjfile=ROOT/rel if (ROOT/rel).exists() else GAME/rel
    blocked=set()
    for row in csv.DictReader(adjfile.open(encoding='utf-8-sig'),delimiter=';'):
        if not all(row.get(k,'').startswith('x') for k in ['From','To']):continue
        if row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip():
            blocked.add(pair(int(row['From'][1:],16),int(row['To'][1:],16)))
    impassable=set()
    for source in effective('map_data/state_regions'):
        for n in parse(source.read_text(encoding='utf-8-sig')):impassable.update(int(v[1:],16) for v in provs(n,'impassable'))
    # Reject newly selected detached pieces instead of painting an unlinked
    # new province as if it broadened the block. Keep every older selection.
    connectivity={}
    old_witness=load(PRIOR/'PIXEL_PATH_WITNESS.json')
    for tag in ['HBC','ONT']:
        seed_row=next(r for r in old_witness if r['owner']==tag);x,y=seed_row['pixel'];seed=y*width+x
        mask=np.isin(a,sorted(proposals[tag]-impassable));reachable,_=flood(a,mask,[seed],blocked)
        connected_rgb={int(a.ravel()[v]) for v in reachable}
        disconnected_new=additions[tag]-connected_rgb
        proposals[tag]-=disconnected_new;additions[tag]-=disconnected_new
        connectivity[tag]=dict(new_provinces_discarded_as_detached=sorted(f'x{v:06X}' for v in disconnected_new),reachable_province_rgb=sorted(f'x{v:06X}' for v in connected_rgb))
    hbc,ont=proposals['HBC'],proposals['ONT']
    previous_compact=load(saved) if saved.exists() else None
    previous_hbc={int(v[1:],16) for v in previous_compact['hbc_rgb']} if previous_compact else base
    previous_ont={int(v[1:],16) for v in previous_compact['ont_rgb']} if previous_compact else tags['ONT']
    notch_added=hbc-previous_hbc
    dump('USER_NOTCH_INFILL.json',dict(authority='Player red annotation: add this area too',bitmap_vertices=notch,selection='Whole current-HBC provinces whose raster centroids fall inside the visual envelope; detached additions rejected',previous_hbc_provinces=len(previous_hbc),added_provinces=len(notch_added),added_rgb=sorted(f'x{v:06X}' for v in notch_added),historic_boundary_claim=False,gameplay_files_modified=[]))
    def future_owner(rgb):
        if rgb in hbc:return 'HBC'
        if rgb in ont:return 'ONT'
        return next(iter(owners[rgb]))[1] if rgb in owners else 'UNOWNED'
    witness_ok=all(f'x{int(a[r["pixel"][1],r["pixel"][0]]):06X}'==r['rgb'] and future_owner(int(r['rgb'][1:],16))==r['owner'] for r in old_witness)
    passable_witness=all(int(r['rgb'][1:],16) not in impassable for r in old_witness)
    valid_steps=all(sum(abs(u-v) for u,v in zip(first['pixel'],second['pixel']))==1 and pair(int(first['rgb'][1:],16),int(second['rgb'][1:],16)) not in blocked for first,second in zip(old_witness,old_witness[1:]))
    retained_ont={int(v[1:],16) for v in previous['protected_ont_rgb']}
    population=conservation(load(OUT.parent/'HBC-03/CONSERVATION_BASELINE.json'),economic_inventory())
    target_states={sid for rgb in hbc for sid,t in owners[rgb]}
    conservation_plan=load(OUT.parent/'HBC-03/CONSERVATION_PLAN.json')
    hbc_plan_valid=all(r['target_state'] in target_states for r in conservation_plan['pop_commands']+conservation_plan['building_commands'])
    checks={**population,'all_old_hbc_provinces_retained':base<=hbc,'all_current_ont_provinces_retained':tags['ONT']<=ont,'previous_compact_hbc_retained':previous_hbc<=hbc,'previous_compact_ont_unchanged':previous_ont==ont,'player_notch_expansion_present':bool(notch_added),'protected_ont_path_retained':retained_ont<=ont,'no_double_proposed_owner':hbc.isdisjoint(ont),'only_current_hbc_or_ont_land_changed':(hbc|ont)<=relevant,'old_land_path_still_valid_under_proposed_owners':witness_ok,'witness_has_no_current_impassable_province':passable_witness,'witness_has_only_current_allowed_land_steps':valid_steps,'hbc_conservation_plan_still_has_all_target_states':hbc_plan_valid,'new_hbc_block_added':bool(additions['HBC']),'new_ont_block_added':bool(additions['ONT'])}
    dump('COMPACT_BLOCKS.json',dict(date='2026-10-25',status='PLAYER_DRAWN_COMPACT_BLOCKS_PREPARED_NOT_APPLIED',authority='Player asks for broader square-like territorial blocks in the annotated connectors',envelopes_pixel=boxes,selection='Whole provinces whose raster centroids fall in the player-marked envelopes; earlier HBC selection and existing ONT ownership preserved; detached new provinces rejected',hbc_rgb=sorted(f'x{v:06X}' for v in hbc),ont_rgb=sorted(f'x{v:06X}' for v in ont),hbc_provinces=len(hbc),ont_provinces=len(ont),hbc_added_provinces=len(additions['HBC']),ont_added_provinces=len(additions['ONT']),ont_added_source='Existing HBC land omitted from the earlier retained-HBC proposal; future transfer to ONT for the player-requested shape',additions={tag:sorted(f'x{v:06X}' for v in additions[tag]) for tag in additions},connectivity=connectivity,prior_land_witness='../HBC-04/PIXEL_PATH_WITNESS.json',historic_boundary_claim=False,gameplay_files_modified=[],bitmap_sha256=sha(bitmap),military_movement_tested=False,population_baseline=108626,economic_plan='../HBC-03/CONSERVATION_PLAN.json'))
    with (OUT/'PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['RGB','State_ID','Current_owner','Proposed_owner','Role']);w.writeheader()
        for rgb in sorted(hbc|ont):
            sid,tag=next(iter(owners[rgb]));future=future_owner(rgb)
            role='BROADENED_BLOCK' if rgb in additions[future] else 'RETAINED_PROPOSAL' if future=='HBC' else 'EXISTING_UPPER_CANADA'
            w.writerow(dict(RGB=f'x{rgb:06X}',State_ID=sid,Current_owner=tag,Proposed_owner=future,Role=role))
    x0,y0,x1,y1=1600,400,2490,1100;scale=2
    canvas=np.zeros((*a.shape,3),dtype=np.uint8);canvas[:]=(37,48,58)
    land=np.isin(a,np.asarray(sorted(owners),dtype=np.uint32));canvas[land]=(97,104,100)
    canvas[np.isin(a,sorted(tags['HBC']))]=(112,101,73);canvas[np.isin(a,sorted(tags['USA']))]=(62,101,128)
    canvas[np.isin(a,sorted(hbc))]=(235,183,50);canvas[np.isin(a,sorted(ont))]=(175,111,158)
    borders=np.zeros(a.shape,dtype=bool);borders[:,1:]|=a[:,1:]!=a[:,:-1];borders[1:,:]|=a[1:,:]!=a[:-1,:]
    # Only outline land cells, keeping water visually quiet.
    canvas[borders&land]=(49,47,44)
    crop=Image.fromarray(canvas[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(crop.width,crop.height+170),'#25303a');sheet.paste(crop,(0,90));d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    d.text((15,8),'Raccords élargis : blocs territoriaux plus compacts',font=font,fill='white')
    d.text((15,44),'Jaune : HBC proposée ; rose : tout le Haut-Canada proposé ; bleu : Treize Colonies.',font=small,fill='white')
    posts=load(OUT.parent/'HBC-02/POST_CANDIDATES.json')+[dict(name='Eastmain House',diagnostic_cell=load(OUT.parent/'HBC-03/EASTMAIN_CANDIDATE.json')['post']['diagnostic_cell'])]
    for i,p in enumerate(posts):
        x,y=p['diagnostic_cell'];cx=(x-x0)*scale;cy=90+(y-y0)*scale;d.ellipse((cx-5,cy-5,cx+5,cy+5),fill='white',outline='black',width=2)
        dx,dy=[(12,12),(12,12),(12,-28),(12,-28),(-160,-28)][i];d.text((cx+dx,cy+dy),p['name'],font=small,fill='white',stroke_width=2,stroke_fill='black')
    d.text((1220,1230),'Haut-Canada',font=font,fill='white',stroke_width=2,stroke_fill='black')
    # Contact markers remain, but the old pale-pink route strip and white
    # line are omitted: neither was a separate territorial ownership strip.
    for edge in previous['borders']:
        if edge['to_country']=='USA':
            x,y=edge['from_pixel'];cx=(x-x0)*scale;cy=90+(y-y0)*scale;d.ellipse((cx-6,cy-6,cx+6,cy+6),fill='#ee766b',outline='white',width=2)
            d.text((cx-190,cy+15),'Frontière américaine',font=small,fill='white',stroke_width=2,stroke_fill='black')
    d.text((15,sheet.height-65),f'HBC : {len(hbc)} provinces ; Haut-Canada : {len(ont)} provinces. Liaison terrestre maintenue.',font=small,fill='white')
    d.text((15,sheet.height-36),'Proposition non appliquée ; 108 626 habitants HBC et tous les bâtiments protégés.',font=small,fill='white');sheet.save(OUT/'COMPACT_BLOCKS.png')
    checks['no_runtime_change']=before==runtime();dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),engine_tested=False,gameplay_files_modified=[]))
    print(json.dumps(dict(checks=checks,hbc_provinces=len(hbc),ont_provinces=len(ont),added_hbc=len(additions['HBC']),added_ont=len(additions['ONT'])),ensure_ascii=False));assert all(checks.values()),checks


if __name__=='__main__':main()
