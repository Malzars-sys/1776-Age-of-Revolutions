"""Exact pixel-space index and review atlas. No latitude/longitude projection."""
from pathlib import Path
import collections as C
import csv, gzip, hashlib, json, re, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from map1_prepare import ROOT, OUT, INPUT, GAME, EXPECTED, table, savecsv, digest, protected
from map_1776_audit import trees, values, prov, own_inventory
from validate_diplomacy_ottoman_1776 import scalar

EVIDENCE=OUT/'MAP1_GEOGRAPHIC_EVIDENCE'

def load_definitions():
    defs={}; hubs={}; countries=set()
    for p,raw,ns in trees(ROOT,GAME,'map_data/state_regions'):
        for n in ns:
            if not n.key.startswith('STATE_'): continue
            defs[n.key]={'provinces':[prov(x) for x in values(n,'provinces')],
                         'numeric_id':scalar(n.one('id')),'source':str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else 'VANILLA:'+str(p.relative_to(GAME))}
            hubs[n.key]={k:prov(n.one(k)) for k in ['city','port','farm','mine','wood'] if n.children(k)}
    for p,raw,ns in trees(ROOT,GAME,'common/country_definitions'):
        for n in ns:
            if n.children('country_type'): countries.add(n.key.removeprefix('REPLACE_OR_CREATE:'))
    names={}
    for p in [GAME/'localization/english/hub_names_l_english.yml']+list((ROOT/'localization/english').rglob('*.yml')):
        for key,val in re.findall(r'^\s*(HUB_NAME_STATE_\w+):\d*\s*"([^"]*)"',p.read_text(encoding='utf-8-sig'),re.M): names[key]=val
    return defs,hubs,names,countries

def geometry():
    assert digest(GAME/'map_data/provinces.png')==EXPECTED
    arr=np.array(Image.open(GAME/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    rgb=(arr[:,:,0]<<16)|(arr[:,:,1]<<8)|arr[:,:,2]; del arr
    h,w=rgb.shape; assert (w,h)==(8192,3616)
    colors,inv,counts=np.unique(rgb,return_inverse=True,return_counts=True)
    inv=inv.reshape(h,w).astype(np.int32); assert len(colors)==40875
    ids=['x%06X'%int(x) for x in colors]; index={v:i for i,v in enumerate(ids)}
    runs=C.defaultdict(list)
    for y,row in enumerate(inv):
        starts=np.r_[0,np.flatnonzero(row[1:]!=row[:-1])+1]; ends=np.r_[starts[1:],w]
        for a,b in zip(starts,ends): runs[int(row[a])].append([y,int(a),int(b)])
    bboxes={}; centers={}; anchors={}; wrap={}
    for ix,rs in runs.items():
        rr=np.asarray(rs,dtype=np.int64); sizes=rr[:,2]-rr[:,1]; count=int(sizes.sum())
        assert count==int(counts[ix])
        bboxes[ids[ix]]=[int(rr[:,1].min()),int(rr[:,0].min()),int(rr[:,2].max()),int(rr[:,0].max())+1]
        cx=float(((rr[:,1]+rr[:,2]-1)*sizes).sum()/count/2); cy=float((rr[:,0]*sizes).sum()/count)
        centers[ids[ix]]=[round(cx,3),round(cy,3)]
        crossings=bool((rgb[:,0]==int(colors[ix])).any() and (rgb[:,-1]==int(colors[ix])).any())
        if crossings:
            occupied=np.zeros(w,dtype=bool)
            for _,a,b in rs: occupied[a:b]=True
            empty=np.flatnonzero(~occupied)
            if len(empty):
                cuts=np.r_[0,np.flatnonzero(empty[1:]!=empty[:-1]+1)+1,len(empty)]
                lo,hi=max(zip(cuts[:-1],cuts[1:]),key=lambda pair:pair[1]-pair[0])
                start=int(empty[hi-1])+1; width=w-(hi-lo)
                xmid=((rr[:,1]+rr[:,2]-1)/2-start)%w
                ucx=float((xmid*sizes).sum()/count)
                cx=(start+ucx)%w
                wrap[ids[ix]]={'x_start':start,'width':int(width),'centroid_x':round(cx,3)}
        mids=(rr[:,1]+rr[:,2]-1)/2
        dx=np.minimum(abs(mids-cx),w-abs(mids-cx))
        best=int(np.argmin(dx**2+(rr[:,0]-cy)**2))
        anchors[ids[ix]]=[float(mids[best]),int(rr[best,0])]
    perimeter=np.zeros(len(ids),dtype=np.int64)
    diff=inv!=np.roll(inv,1,axis=1)
    perimeter+=np.bincount(inv[diff],minlength=len(ids))
    perimeter+=np.bincount(np.roll(inv,1,axis=1)[diff],minlength=len(ids))
    diffy=inv[1:]!=inv[:-1]
    perimeter+=np.bincount(inv[1:][diffy],minlength=len(ids))
    perimeter+=np.bincount(inv[:-1][diffy],minlength=len(ids))
    perimeter+=np.bincount(inv[0],minlength=len(ids))+np.bincount(inv[-1],minlength=len(ids))
    baseline=table(INPUT/'map0_reference/MAP_1776_BASELINE.csv')
    owners,pairs,odd=own_inventory(ROOT,GAME)
    old=C.defaultdict(set)
    for r in baseline:
        if r['Owner_TAG']: old[r['Province_ID']].add((r['Ownership_History_State_IDs'],r['Owner_TAG']))
    # Compare ownership as a multiset of state/tag assignments; preserve repeats in separate audit.
    for v in set(owners)|set(old):
        reconstructed={(s,t) for ss,t in old[v] for s in ss.split('|')}
        assert set(owners[v])==reconstructed, 'STOP: current ownership differs from MAP0 '+v
    defs,hubs,names,countries=load_definitions()
    oldmembers=C.defaultdict(set)
    for r in baseline:
        if r['State_ID']: oldmembers[r['Province_ID']].add(r['State_ID'])
    currentmembers=C.defaultdict(set)
    for sid,d in defs.items():
        for v in d['provinces']: currentmembers[v].add(sid)
    for v in currentmembers:
        assert currentmembers[v]==oldmembers[v], 'STOP: State Region baseline changed '+v
    baseline_hubs=C.defaultdict(list)
    for sid,hh in hubs.items():
        for kind,v in hh.items(): baseline_hubs[v].append(sid+':'+kind+':'+names.get('HUB_NAME_'+sid+'_'+kind,'UNNAMED'))
    rows=[]
    for r in baseline:
        v=r['Province_ID']; ix=index[v]; bb=bboxes[v]
        rows.append(dict(r,Pixel_X_Min=bb[0],Pixel_Y_Min=bb[1],Pixel_X_Max_Exclusive=bb[2],Pixel_Y_Max_Exclusive=bb[3],
                         Centroid_X=wrap.get(v,{}).get('centroid_x',centers[v][0]),Centroid_Y=centers[v][1],
                         Label_Interior_X=anchors[v][0],Label_Interior_Y=anchors[v][1],
                         Boundary_Unit_Edges=int(perimeter[ix]),Wrap_X_Crossing='YES' if v in wrap else 'NO',
                         Wrap_Compact_X_Start=wrap.get(v,{}).get('x_start',''),Wrap_Compact_Width=wrap.get(v,{}).get('width',''),
                         Hub_Anchors='|'.join(baseline_hubs[v]),Pixel_Band=f'X{bb[0]//512:02d}_Y{bb[1]//256:02d}',
                         Geographic_Confidence='EXACT_GAME_PIXELS_NOT_HISTORICAL',Geometry_File='MAP1_GEOGRAPHIC_EVIDENCE/PROVINCE_PIXEL_RUNS.jsonl.gz'))
    savecsv('MAP1_BASELINE_PROVINCE_INDEX.csv',rows)
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    with gzip.open(EVIDENCE/'PROVINCE_PIXEL_RUNS.jsonl.gz','wt',encoding='utf-8') as f:
        for v in ids:
            f.write(json.dumps({'Province_ID':v,'bbox':bboxes[v],'runs_y_x0_x1_exclusive':runs[index[v]]},separators=(',',':'))+'\n')
    metadata={'width':w,'height':h,'unique_rgb':len(ids),'bitmap_sha256':EXPECTED,'coordinate_system':'PIXEL_ONLY_TOP_LEFT_ORIGIN',
              'wrap_x':True,'GPS_projection':'NOT_ESTABLISHED','historical_georeferencing':'NOT_ESTABLISHED',
              'geometry':'Lossless row runs; province polygon is union of closed-open unit pixel squares. Contours are their exposed edges. Includes holes and disconnected islands.',
              'read_only_sources':[str(GAME/'map_data/provinces.png'),'map_data/state_regions','common/history/states','localization/english'],
              'hub_limit':'Game hub identifies a locality, not its historical jurisdiction. Names may be anachronistic or relocated by mod.',
              'source_legend':'Solid colors = current technical owner; yellow = issue/reference RGB, not proposed historical boundary.',
              'generated_date':'2026-10-10','defined_country_tags':sorted(countries)}
    (EVIDENCE/'GEOMETRY_METADATA.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    np.savez_compressed(EVIDENCE/'pixel_index.npz',rgb=rgb,inv=inv,colors=colors)
    (EVIDENCE/'geometry_index.json').write_text(json.dumps({'bboxes':bboxes,'centers':centers,'anchors':anchors,'wrap':wrap,'hubs':hubs,'hub_names':names}),encoding='utf-8')
    print('Geometry PASS:',len(ids),'RGB;',len(rows),'baseline attributions')

def locator_check():
    defs,hubs,names,countries=load_definitions()
    rgb=np.load(EVIDENCE/'pixel_index.npz')['rgb']; h,w=rgb.shape
    rows=[]
    for kind in ['city','port','farm','mine','wood']:
        path=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        # Generated locator IDs are State Region numeric IDs. Validate by sampling the bitmap.
        positions={ident:(float(x),float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',path.read_text(encoding='utf-8-sig'))}
        for sid,d in defs.items():
            if kind not in hubs[sid] or d['numeric_id'] not in positions: continue
            x,z=positions[d['numeric_id']]; y=h-z
            if not (0<=x<w and 0<=y<h): continue
            sampled='x%06X'%int(rgb[int(y),int(x)])
            rows.append(dict(State_ID=sid,Hub_Type=kind,Hub_Name=names.get('HUB_NAME_'+sid+'_'+kind,''),
                             Defined_Hub_RGB=hubs[sid][kind],Locator_Sampled_RGB=sampled,
                             Locator_X=round(x,3),Locator_Y=round(y,3),
                             Definition_Matches_Locator='YES' if sampled==hubs[sid][kind] else 'NO',
                             Locator_In_State='YES' if sampled in d['provinces'] else 'NO',
                             Source=str(path),Coordinate_Method='ENGINE_X; PNG_Y=HEIGHT-ENGINE_Z; CHECKED_RGB',
                             Historical_Proof='NONE: vanilla named anchor, not 1776 jurisdiction'))
    savecsv('MAP1_HUB_LOCATOR_CHECKS.csv',rows)
    print('Locator checks',len(rows),'matching',sum(r['Definition_Matches_Locator']=='YES' for r in rows))

if __name__=='__main__':
    if '--locators' in __import__('sys').argv: locator_check()
    else: geometry(); locator_check()
