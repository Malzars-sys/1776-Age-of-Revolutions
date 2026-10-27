"""Player-requested coastal infill of the HBC-02 proposal; diagnostics only."""
import csv
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from audit_hbc_1776 import ROOT, GAME, runtime, sha
from hbc02_map_candidates import pixel_components
from validate_diplomacy_ottoman_1776 import parse, scalar

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-02'


def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    before=runtime()
    expected=next(r['sha256'] for r in load('INPUTS.json') if r['path']=='map_data/provinces.png')
    assert sha(ROOT/'map_data/provinces.png')==expected,'Bitmap changed: refresh the base proposal first.'
    original=load('CORRIDOR_CANDIDATE.json');posts=load('POST_CANDIDATES.json')
    rows=list(csv.DictReader((OUT.parent/'HBC-01/HBC_PROVINCE_REGISTER.csv').open(encoding='utf-8-sig')))
    hbc={int(r['Province_RGB'][1:],16):r for r in rows}
    assert all(r['Distinct_owners']=='HBC' for r in rows)
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
    rel=Path('map_data/state_regions/99_seas.txt')
    sea_path=ROOT/rel if (ROOT/rel).exists() else GAME/rel
    hudson=next(n for n in parse(sea_path.read_text(encoding='utf-8-sig')) if n.key=='STATE_HUDSON_BAY')
    water={int(scalar(v.value)[1:],16) for n in hudson.children('provinces') for v in n.children()}
    base={int(rgb[1:],16) for rgb in original['rgb']}
    # The player's complete line is the inland boundary, including the
    # Cumberland branch: fill its coastward side, never its inland side.
    coastal=set(base)
    spine=np.isin(a,sorted(coastal));owned=np.isin(a,sorted(hbc));bay=np.isin(a,sorted(water))
    selected=set(base);slices=[]
    for y in np.where(np.any(spine,axis=1))[0]:
        left=int(np.flatnonzero(spine[y])[0])
        east=np.flatnonzero(bay[y,left:])
        if not len(east):continue
        right=left+int(east[0])
        if right<=left:continue
        candidates={int(v) for v in np.unique(a[y,left:right][owned[y,left:right]])}
        selected.update(candidates)
        slices.append(dict(y=int(y),corridor_inland_x=left,first_hudson_water_x=right,rgb_count=len(candidates)))
    mask=np.isin(a,sorted(selected));added=selected-base
    root_labels,component_sizes,_=pixel_components(mask,[p['diagnostic_cell'] for p in posts])
    filled=all(np.all(mask[r['y'],r['corridor_inland_x']:r['first_hudson_water_x']][owned[r['y'],r['corridor_inland_x']:r['first_hudson_water_x']]]) for r in slices)
    # Re-read current declarations for the selected provinces: do not rely
    # on the older audit when collaborators may have edited shared files.
    from audit_hbc_1776 import effective,provs
    from validate_diplomacy_ottoman_1776 import walk
    current={}
    for path in effective('common/history/states'):
        for n in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if n.key!='create_state':continue
            tag=scalar(n.one('country','')).removeprefix('c:')
            for rgb in provs(n,'owned_provinces'):
                key=int(rgb[1:],16)
                if key in selected:current.setdefault(key,set()).add(tag)
    checks=dict(base_corridors_retained=base<=selected,all_coastward_land_filled=filled,all_selected_provinces_currently_hbc=all(current.get(v)=={'HBC'} for v in selected),no_water_selected=not bool(selected&water),all_posts_still_connected=len(set(root_labels))==1 and root_labels[0]>0)
    details=dict(date='2026-10-25',authority='Direct player request: fill all land between the coastal side of the line and the shore for a clean coastal band',status='PLAYER_REQUESTED_VISUAL_PROPOSAL_NOT_APPLIED',method='For each original-network raster row, include existing HBC land between the inland edge of the complete line, including Cumberland, and the first Hudson Bay water pixel to its east; retain entire native provinces and do not expand landward of the line',base_provinces=len(base),provinces=len(selected),added_provinces=len(added),pixels=int(mask.sum()),added_pixels=int(mask.sum())-original['pixels'],rgb=sorted(f'x{v:06X}' for v in selected),added_rgb=sorted(f'x{v:06X}' for v in added),coastal_slices=slices,post_components=root_labels,pixel_component_sizes=sorted(component_sizes,reverse=True),historical_boundaries_validated=False,gameplay_files_modified=[],runtime_market_tested=False,water_region=dict(name=hudson.key,file=str(sea_path),rgb=sorted(f'x{v:06X}' for v in water)))
    dump('COASTAL_CANDIDATE.json',details)
    counts={int(k):int(v) for k,v in zip(*np.unique(a,return_counts=True))}
    with (OUT/'COASTAL_PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['RGB','State_ID','Role','Bitmap_pixels','Current_owner','Applied']);w.writeheader()
        for rgb in sorted(selected):w.writerow(dict(RGB=f'x{rgb:06X}',State_ID=hbc[rgb]['State_ID'],Role='ORIGINAL_CORRIDOR' if rgb in base else 'PLAYER_COASTAL_INFILL',Bitmap_pixels=counts[rgb],Current_owner='HBC',Applied=False))
    box=(1600,400,2420,925);x0,y0,x1,y1=box;scale=2
    canvas=np.zeros((*a.shape,3),dtype=np.uint8);canvas[:]=(37,48,58)
    canvas[owned]=(112,101,73);canvas[mask]=(235,183,50)
    edges=np.zeros(a.shape,dtype=bool);edges[:,1:]|=a[:,1:]!=a[:,:-1];edges[1:,:]|=a[1:,:]!=a[:-1,:]
    canvas[edges&owned]=(52,53,51)
    crop=Image.fromarray(canvas[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(crop.width,crop.height+145),'#25303a');sheet.paste(crop,(0,80));d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    d.text((15,8),'HBC — bande côtière remplie jusqu’au littoral',font=font,fill='white')
    d.text((15,40),'Jaune : proposition ajustée ; brun : reste de la HBC actuelle. Aucun transfert appliqué.',font=small,fill='white')
    for i,p in enumerate(posts):
        x,y=p['diagnostic_cell'];cx=(x-x0)*scale;cy=80+(y-y0)*scale
        d.ellipse((cx-6,cy-6,cx+6,cy+6),fill='white',outline='black',width=2)
        dx,dy=[(12,12),(12,12),(12,-28),(12,-28)][i]
        d.text((cx+dx,cy+dy),p['name'],font=small,fill='white',stroke_width=2,stroke_fill='black')
    d.text((15,sheet.height-52),f'{len(selected)} provinces : réseau initial + {len(added)} provinces de remplissage côtier.',font=small,fill='white')
    d.text((15,sheet.height-28),'Toute la terre côté littoral de la ligne est incluse. Accès au marché à vérifier en jeu.',font=small,fill='white')
    sheet.save(OUT/'COASTAL_CANDIDATE.png')
    checks['no_runtime_change']=before==runtime()
    dump('COASTAL_VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),historical_validation=False,runtime_tested=False))
    print(json.dumps(dict(provinces=len(selected),added=len(added),pixels=int(mask.sum()),components=sorted(component_sizes,reverse=True),checks=checks),ensure_ascii=False))
    assert all(checks.values()),checks


if __name__=='__main__':main()
