"""MAP-2M-R3 continuation: preserve accepted R2 and current economic changes."""
import json
import os
import sys
import subprocess
import urllib.request
import collections as C
import csv
import difflib
import time
import unittest
import io
from pathlib import Path
import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont
import map2m_r2 as r2
import start_buildings_2026_10_15 as economy

ROOT=r2.ROOT
OUT=ROOT/'docs/reports/map/MAP2M/R3'

def dump(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))

def capture():
    assert not (OUT/'BASELINE.json').exists(), 'Immutable continuation reference exists'
    inv=r2.core.qa.inventory();bmp=r2.core.packed(ROOT/'map_data/provinces.png')
    reference=r2.OUT/'provinces_candidate.png'
    assert r2.core.sha(reference)==r2.core.sha(ROOT/'map_data/provinces.png')
    assert int((bmp==0x567452).sum())==347 and int((bmp==0xEDB010).sum())==85 and int((bmp==0xFCC7B7).sum())==142
    assert sum(r['count'] for r in inv['pops'])==835804980
    old={p.relative_to(ROOT).as_posix():r2.core.sha(p) for p in r2.old.BASE.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json',dict(inventory=inv,hashes=economy.runtime_hashes(),earlier_proofs=old,bitmap_backup=reference.relative_to(ROOT).as_posix(),
         bitmap_sha256=r2.core.sha(reference),git_head=r2.head(),git_index_sha256=r2.core.sha(ROOT/'.git/index'),
         registry=json.loads(r2.core.active_registry_path().read_text())))
    print('R3 baseline: accepted 347 Swedish cells / 85 Bromberg cells / 142 Polish residual cells. Population 835804980.')

def fetch(name,url):
    """Bounded public-source retrieval. Never reuse this to bypass access controls."""
    p=OUT/'EVIDENCE'/name;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():print('Existing source',name,p.stat().st_size);return
    request=urllib.request.Request(url,headers={'User-Agent':'MAP-2M-R3 historical-geography research'})
    with urllib.request.urlopen(request,timeout=30) as response:
        data=response.read(22000001);content_type=response.headers.get('Content-Type','')
    assert len(data)<=22000000, 'Source-size bound exceeded'
    p.write_bytes(data)
    dump('EVIDENCE/'+name+'.source.json',dict(url=url,bytes=len(data),sha256=r2.core.sha(p),content_type=content_type))
    print('Saved',name,len(data),'bytes',content_type)

def physical():
    """Read-only diagnostic, independent of political ownership in the fit."""
    from georeference.model import forward
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json').read_text())['model']
    native=r2.core.packed(ROOT/load('BASELINE.json')['bitmap_backup'])
    owners={int(r['key'][0][1:],16):r['key'][2] for r in load('BASELINE.json')['inventory']['owners']}
    coast=json.loads((OUT/'EVIDENCE/NE_COASTLINE.geojson').read_text())['features']
    hydro=json.loads((OUT/'EVIDENCE/LUNG_PEENE_LAWA.geojson').read_text())['features']
    bbox=(4370,708,4434,755);x0,y0,x1,y1=bbox;scale=20
    loc=native[y0:y1,x0:x1];arr=np.full((*loc.shape,3),(240,245,250),dtype=np.uint8)
    for value in np.unique(loc):
        if int(value) in owners:arr[loc==value]=(205,205,205)
    base=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
    d=ImageDraw.Draw(base);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    offset=np.array(r2.load('PHYSICAL_DIAGNOSTIC.json')['offset'])
    def lines(geo,color):
        p=forward(model,geo)+offset
        if len(p)>1:d.line([((x-x0)*scale,(y-y0)*scale) for x,y in p],fill=color,width=2)
    for f in coast:
        for geo in [f['geometry']['coordinates']] if f['geometry']['type']=='LineString' else f['geometry']['coordinates']:
            g=np.array(geo);mask=(g[:,0]>11.8)&(g[:,0]<15)&(g[:,1]>53.5)&(g[:,1]<55)
            if mask.any():lines(g[mask],(0,135,0))
    hs=[]
    for f in hydro:
        if f['properties'].get('LA_GN') in ['Peene','Trebel','Ryck']:
            geo=f['geometry']['coordinates'];parts=[geo] if f['geometry']['type']=='LineString' else geo
            for g in parts:lines(g,(0,100,230))
            hs.append(dict(name=f['properties']['LA_GN'],bbox=f['bbox'],fid=f['properties']['fid']))
    for f in json.loads((OUT/'EVIDENCE/LUNG_PEENESTROM_WATER.geojson').read_text())['features']:
        if f['properties'].get('GN2')=='Peenestrom':
            for polygon in f['geometry']['coordinates']:
                for ring in polygon:lines(ring,(190,0,210))
    towns=[('Demmin',13.036,53.907),('Anklam',13.692,53.856),('Wolgast',13.776,54.052),('Greifswald',13.381,54.095)]
    for name,lon,lat in towns:
        x,y=forward(model,[[lon,lat]])[0]+offset;x=(x-x0)*scale;y=(y-y0)*scale
        d.ellipse((x-4,y-4,x+4,y+4),fill='red');d.text((x+6,y+3),name,fill='red',font=font)
    for x in range(x0,x1,5):d.line(((x-x0)*scale,0,(x-x0)*scale,base.height),fill='#999999');d.text(((x-x0)*scale+1,1),str(x),font=font,fill='black')
    for y in range(y0+2,y1,5):d.line((0,(y-y0)*scale,base.width,(y-y0)*scale),fill='#999999');d.text((1,(y-y0)*scale),str(y),font=font,fill='black')
    base.save(OUT/'PEENE_PHYSICAL_READING.png')
    dump('PHYSICAL_SOURCE_READING.json',dict(rivers=hs,offset=offset.tolist(),warning='Diagnostic only: coast and river positions not accepted controls yet.'))
    print('Named physical routes:',hs)

def geometry():
    """Restrict transfers to the common interior of dated map and new hydrography."""
    from georeference.model import forward
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json').read_text())['model']
    before=r2.core.packed(ROOT/load('BASELINE.json')['bitmap_backup'])
    offset=np.array(r2.load('PHYSICAL_DIAGNOSTIC.json')['offset'])
    hydro=json.loads((OUT/'EVIDENCE/LUNG_PEENE_LAWA.geojson').read_text())['features']
    peene=next(f for f in hydro if f['properties'].get('LA_GN')=='Peene')
    parts=peene['geometry']['coordinates'];parts=[parts] if peene['geometry']['type']=='LineString' else parts
    river=np.vstack([forward(model,p)+offset for p in parts])
    # The eastern mainland Peene is broadly west-east. Take the northernmost
    # latitude for each X bin: a conservative envelope, not a smoothed boundary.
    river=river[(river[:,0]>=4391)&(river[:,0]<=4410)]
    ys,xs=np.where(before==0xE1A03A);cells=np.column_stack((xs+.5,ys+.5))
    source=r2.load('GEOMETRY_REVIEW.json')['PEENE']
    poly=np.array(source['historical_polygon']);m=np.array(source['new_matrix'])
    historical=np.column_stack((poly,np.ones(len(poly))))@m
    def margin(points,polygon):
        dist=np.full(len(points),np.inf)
        for a,z in zip(polygon,np.roll(polygon,-1,axis=0)):
            ab=z-a;den=float(ab@ab)
            if den:
                u=np.clip(((points-a)@ab)/den,0,1)
                dist=np.minimum(dist,np.linalg.norm(points-a-u[:,None]*ab,axis=1))
        return dist
    historical_dist=margin(cells,historical)
    inside=r2.core.inside(cells,historical)
    older=np.column_stack((poly,np.ones(len(poly))))@np.array(source['old_matrix'])
    river_limit=np.array([min(river[abs(river[:,0]-x)<=1,1],default=-np.inf) for x in cells[:,0]])
    strait=[]
    for f in json.loads((OUT/'EVIDENCE/LUNG_PEENESTROM_WATER.geojson').read_text())['features']:
        if f['properties'].get('GN2')=='Peenestrom':
            for polygon in f['geometry']['coordinates']:
                strait.extend(forward(model,polygon[0])+offset)
    strait=np.asarray(strait)
    west_limit=np.array([min(strait[abs(strait[:,1]-y)<=1,0],default=-np.inf) for y in cells[:,1]])
    # Three-pixel physical precaution and 1.5-pixel historical precaution are
    # sensitivity buffers, NOT measured confidence limits. X<=4407 excludes the
    # entire unresolved Peenestrom/northern Usedom approach and Wolgast centre.
    screened=inside&r2.core.inside(cells,older)&(historical_dist>=1.5)&(cells[:,1]<=river_limit-3)&(cells[:,0]>=4392)&(cells[:,0]<4408)
    take=screened&(cells[:,0]<=west_limit-3)
    mask=np.zeros(before.shape,bool);mask[ys[take],xs[take]]=True
    near=before==0x567452
    for _ in range(30):
        spread=np.roll(near,1,0)|np.roll(near,-1,0)|np.roll(near,1,1)|np.roll(near,-1,1)
        near|=spread&mask
    mask&=near
    chosen=[[int(x),int(y)] for y,x in zip(*np.where(mask))]
    # Independent coastal silhouette checks; not homologous surveyed city points.
    coast=json.loads((OUT/'EVIDENCE/NE_COASTLINE.geojson').read_text())['features']
    allcoast=[]
    for f in coast:
        for p in [f['geometry']['coordinates']] if f['geometry']['type']=='LineString' else f['geometry']['coordinates']:
            p=np.array(p);p=p[(p[:,0]>12)&(p[:,0]<15)&(p[:,1]>53.5)&(p[:,1]<55)]
            if len(p):allcoast.append(p)
    allcoast=np.vstack(allcoast)
    owner={int(r['key'][0][1:],16):r['key'][2] for r in load('BASELINE.json')['inventory']['owners']}
    local=before[709:754,4370:4435];land=np.isin(local,list(owner));shore=np.zeros(land.shape,bool)
    shore[:,1:]|=land[:,1:]!=land[:,:-1];shore[1:]|=land[1:]!=land[:-1];shore&=land
    cy,cx=np.where(shore);native=np.column_stack((cx+4370+.5,cy+709+.5))
    checks=[]
    for name,geo,window in [('Darss outer cape',[12.505,54.477],2.5),('Arkona',[13.435,54.679],3),('Nordperd',[13.744,54.276],3),('Northern Usedom cape',[13.768,54.166],3),('Koserow outer coast',[14.016,54.057],3)]:
        g=allcoast[np.argmin(((allcoast-geo)**2).sum(axis=1))];p=forward(model,[g])[0]+offset
        near=native[np.linalg.norm(native-p,axis=1)<window]
        q=near[np.argmin(np.linalg.norm(near-p,axis=1))] if len(near) else [None,None]
        checks.append(dict(name=name,geo=g.tolist(),predicted=p.tolist(),nearest_native_shore=list(q),distance_px=float(np.linalg.norm(q-p)) if q[0] is not None else None,role='CHECK_NOT_USED_IN_FIT',quality='Generalized coastal silhouette, not a certified city homologue'))
    dump('GEOMETRY_REVIEW.json',dict(PEENE=dict(cells=chosen,pixels=len(chosen),parent='xE1A03A',destination='x567452',
        source_matrix=m.tolist(),historical_polygon=source['historical_polygon'],river_pixels=river.tolist(),strait_pixels=strait.tolist(),physical_buffer_px=3,historical_buffer_px=1.5,
        rejected_near_peenestrom=[[int(x),int(y)] for x,y in zip(xs[screened&~take],ys[screened&~take])],
        working_extent=[4392,4408],warning='Working extent and buffers are NOT the historical frontier or confidence intervals; Wolgast and Peenestrom remain open.'),
        NETZE=dict(cells=[],pixels=0,reason='No additional dated pre-1776 boundary with independently controlled western/southern placement obtained.'),coastal_checks=checks))
    print('Selected new Peene cells',len(chosen),chosen)
    print('Independent coastal silhouette distances',[(v['name'],v['distance_px']) for v in checks])

def write_csv(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields or list(rows[0]));writer.writeheader();writer.writerows(rows)

def prepare():
    b=load('BASELINE.json');review=load('GEOMETRY_REVIEW.json');core=r2.core
    assert economy.runtime_hashes()==b['hashes'], 'Workspace changed: re-review, never overwrite'
    before=core.packed(ROOT/b['bitmap_backup']);changes=[]
    for x,y in review['PEENE']['cells']:
        changes.append(dict(Sector='PEENE',X=x,Y=y,RGB_before='xE1A03A',RGB_after='x567452',State_ID='STATE_POMERANIA',
            Owner_before='PRU',Owner_after='SWE',Source='Mayer/Lotter 1763; existing two source readings; LUNG Peene and Peenestrom physical envelope',
            Approximation='Conservative mainland interior, not the complete river frontier'))
    assert len(changes)==10
    after=r2.expected_raster(before,changes)
    for value in [0xE1A03A,0x567452]:assert len(core.components(after==value))==1
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    area=sum(int((before==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_POMERANIA','PRU'])
    weights={'PRU':area-len(changes),'SWE':len(changes)}
    allocations=[];files={};originals={}
    for path in economy.effective(ROOT,core.qa.GAME,'common/history/pops'):
        raw=path.read_text(encoding='utf-8-sig')
        try:region=core.region(raw,'STATE_POMERANIA','PRU')
        except StopIteration:continue
        edits=[];moved=[]
        for pop in region.children('create_pop'):
            size=pop.children('size')[0];counts=core.allocate(int(size.value),weights)
            edits.append((size.start,size.end,'size = '+str(counts['PRU'])))
            if counts['SWE']:
                moved.append(core.edits(raw[pop.start:pop.end],[(size.start-pop.start,size.end-pop.start,'size = '+str(counts['SWE']))]))
            allocations.append(dict(state='STATE_POMERANIA',source='PRU',target='SWE',culture=core.cw.scalar(pop.one('culture')),
                religion=core.cw.scalar(pop.one('religion','DEFAULT')),before=int(size.value),after=counts))
        updated=core.edits(raw,edits)
        for fragment in moved:updated=core.append(updated,'STATE_POMERANIA','SWE',fragment)
        # Do not introduce blank indentation lines in a previously dirty file.
        a=raw.splitlines(True);z=updated.splitlines(True)
        for kind,a0,a1,z0,z1 in difflib.SequenceMatcher(a=a,b=z,autojunk=False).get_opcodes():
            if kind in ['insert','replace']:
                for i in range(z0,z1):
                    if not z[i].strip():z[i]='\n'
        updated=''.join(z);core.cw.parse(updated)
        assert path.is_relative_to(ROOT)
        rel=path.relative_to(ROOT).as_posix();originals[rel]=raw;files[rel]=updated
    assert allocations and files
    building_review=[]
    for sid,tag,node,path in economy.declarations():
        if (sid,tag)!=('STATE_POMERANIA','PRU'):continue
        for child in core.cw.walk(node.children()):
            if child.key=='levels':
                allocation=core.allocate(int(child.value),weights)
                assert allocation['SWE']==0, 'Nonzero building transfer requires explicit ownership review'
                building_review.append(dict(building=node.one('building'),levels=int(child.value),allocation=allocation,path=path.relative_to(ROOT).as_posix()))
    plan=dict(changes=changes,allocations=allocations,weights=weights,source_area=area,files=sorted(files),building_review=building_review,
        new_provinces=[],candidate_sha256=core.sha(OUT/'provinces_candidate.png'),status='MAP-2M-R3_PARTIAL',
        netze_applied_cells=0,reason='New physical geometry supports only the mainland Peene core; no dated independent Netze refinement.')
    dump('PLAN.json',plan);dump('ORIGINAL_TEXT.json',originals);dump('EXPECTED_TEXT.json',files)
    write_csv('TERRITORIAL_CHANGES.csv',changes)
    old_out=core.OUT
    try:core.OUT=OUT;core.emit(files,'HISTORY.patch')
    finally:core.OUT=old_out
    print('Prepared ten Peene cells; population moved',sum(v['after']['SWE'] for v in allocations),'; no building levels or RGB definitions changed.')

def install_raster():
    b=load('BASELINE.json');plan=load('PLAN.json');core=r2.core
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert core.sha(OUT/'provinces_candidate.png')==plan['candidate_sha256']
    for rel,text in load('EXPECTED_TEXT.json').items():assert (ROOT/rel).read_text(encoding='utf-8-sig')==text
    core.shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Installed reviewed R3 raster',plan['candidate_sha256'])

def previews():
    b=load('BASELINE.json');plan=load('PLAN.json');core=r2.core
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png')
    owners={int(r['key'][0][1:],16):r['key'][2] for r in b['inventory']['owners']}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for sector,box in r2.SECTORS.items():
        x0,y0,x1,y1=box;scale=10;panels=[]
        for title,bmp in [('REFERENCE R2 VALIDEE PAR LE JOUEUR',before),('APRES R3 : PARTIEL',after)]:
            local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),235,np.uint8)
            for v in np.unique(local):arr[local==v]={'PRU':(145,190,225),'SWE':(235,205,65),'PLC':(220,160,160)}.get(owners.get(int(v)),(235,235,235))
            im=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
            canvas=Image.new('RGB',(im.width,im.height+145),'white');canvas.paste(im,(0,40));d=ImageDraw.Draw(canvas)
            d.text((8,9),title,font=font,fill='black')
            # Province boundary lines, without replacing entire one-pixel cells.
            for yy in range(local.shape[0]):
                for xx in range(local.shape[1]):
                    x=xx*scale;y=yy*scale+40
                    if xx and local[yy,xx]!=local[yy,xx-1]:d.line((x,y,x,y+scale),fill='#555555')
                    if yy and local[yy,xx]!=local[yy-1,xx]:d.line((x,y,x+scale,y),fill='#555555')
            for row in r2.load('PLAN.json')['changes']:
                if row['Sector']!=sector:continue
                x=(row['X']-x0)*scale;y=(row['Y']-y0)*scale+40
                d.rectangle((x,y,x+scale-1,y+scale-1),outline='#006d70',width=1)
            if title.startswith('APRES'):
                for row in plan['changes']:
                    if row['Sector']!=sector:continue
                    x=(row['X']-x0)*scale;y=(row['Y']-y0)*scale+40
                    d.rectangle((x,y,x+scale-1,y+scale-1),outline='#d00000',width=2)
            def open_box(a,z,label):
                xa=(a[0]-x0)*scale;ya=(a[1]-y0)*scale+40;xb=(z[0]-x0)*scale;yb=(z[1]-y0)*scale+40
                d.rectangle((xa,ya,xb,yb),outline='#a000b0',width=2)
                for q in range(int(xa),int(xb)-4,10):d.line((q,ya,q+4,ya+4),fill='#a000b0',width=2)
                d.text((xa+3,ya+5),label,font=font,fill='#800090',stroke_width=1,stroke_fill='white')
            if sector=='PEENE':
                open_box((4406,731),(4418,744),'Peenestrom')
                open_box((4388,739),(4406,747),'Peene / Peendamm ouverts')
            else:
                open_box((4452,750),(4487,774),'Krone / Kamin : non clos')
                open_box((4497,771),(4525,790),'Inowroclaw : non clos')
                d.text((8,im.height+115),'Aucun nouveau transfert Netze en R3. Thorn strictement gelee.',font=font,fill='#800090')
            y=im.height+50
            for i,line in enumerate(['Bleu : Prusse | Jaune : Suede | Rose : Pologne',
                'Contour turquoise : 91 cellules R2 conservees | Rouge : ajouts R3',
                'Cadres violets : zones ouvertes indicatives, PAS des frontieres historiques']):
                d.text((8,y+21*i),line,font=font,fill='black')
            panels.append(canvas)
        out=Image.new('RGB',(panels[0].width*2,panels[0].height),'white');out.paste(panels[0]);out.paste(panels[1],(panels[0].width,0));out.save(OUT/(sector+'_BEFORE_AFTER.png'))

def validate():
    core=r2.core;b=load('BASELINE.json');plan=load('PLAN.json');inv=core.qa.inventory();checks=[]
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png')
    def check(name,ok,detail=''):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    check('Exact ten reviewed RGB edits and no other pixels',np.array_equal(after,r2.expected_raster(before,plan['changes'])) and int((before!=after).sum())==10)
    check('Installed bitmap hash',core.sha(ROOT/'map_data/provinces.png')==plan['candidate_sha256'])
    check('Accepted 347 Swedish cells retained',int((before==0x567452).sum())==347 and np.all(after[before==0x567452]==0x567452))
    check('Swedish province now 357 cells; Prussian parent 333',int((after==0x567452).sum())==357 and int((after==0xE1A03A).sum())==333)
    for rgb in ['xEDB010','xFCC7B7','xA04121','x41A021','x80A0A0','x999CEE']:
        v=int(rgb[1:],16);check('Exact frozen footprint '+rgb,np.array_equal(before==v,after==v))
    accepted=r2.load('PLAN.json')['changes']
    check('All 91 accepted R2 pixels retain exact RGB',len(accepted)==91 and all(after[v['Y'],v['X']]==int(v['RGB_after'][1:],16) for v in accepted))
    check('Netze window entirely unchanged',np.array_equal(before[740:812,4435:4550],after[740:812,4435:4550]))
    check('Wolgast, Peenestrom, Usedom east approach unchanged',np.array_equal(before[711:775,4405:4442],after[711:775,4405:4442]))
    check('Demmin and Anklam southern river approach unchanged',np.array_equal(before[739:754,4385:4418],after[739:754,4385:4418]))
    for rgb in [0xE1A03A,0x567452]:check('Single four-connected component '+hex(rgb),len(core.components(after==rgb))==1)
    check('No RGB created or removed',np.array_equal(np.unique(before),np.unique(after)))
    for rgb,owner in [('xE1A03A','PRU'),('x567452','SWE')]:
        refs=[v for v in inv['owners'] if v['key'][0]==rgb]
        check('Single correct owner and State_ID '+rgb,len(refs)==1 and refs[0]['count']==1 and refs[0]['key'][1:]==['STATE_POMERANIA',owner] and inv['geometry'][rgb]=='STATE_POMERANIA')
    for field in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:
        check('Preserved effective inventory '+field,inv[field]==b['inventory'][field])
    check('Population world 835804980 exactly',sum(v['count'] for v in inv['pops'])==835804980)
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for row in plan['allocations']:
        religion='DEFAULT:'+row['culture'] if row['religion']=='DEFAULT' else row['religion'];amount=row['after']['SWE']
        regional[(row['state'],'PRU',row['culture'],religion)]-=amount;regional[(row['state'],'SWE',row['culture'],religion)]+=amount
    check('Exact regional cultures/religions after deterministic allocation',+regional==core.qa.counter(inv['regional_pop']))
    def profiles(raw):
        result=C.Counter()
        for s in core.cw.walk(core.cw.parse(raw)):
            if s.key.startswith('s:STATE_'):
                for rs in s.children():
                    for p in rs.children('create_pop'):
                        profile=[core.qa.norm(n) for n in p.children() if n.key!='size']
                        result[s.key,json.dumps(profile,sort_keys=True)]+=int(p.one('size'))
        return result
    files=load('EXPECTED_TEXT.json');originals=load('ORIGINAL_TEXT.json')
    for rel,text in files.items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig')
        check('Exact reviewed text '+rel,actual==text)
        check('Parse changed text '+rel,bool(core.cw.parse(actual)))
        check('All pop attributes and per-state totals '+rel,profiles(actual)==profiles(originals[rel]))
    hashes=economy.runtime_hashes();changed={p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}
    check('Only bitmap and one population file changed',changed==set(files)|{'map_data/provinces.png'})
    check('Full imperial registry unchanged; only existing registered RGB expanded',json.loads(core.active_registry_path().read_text())==b['registry'])
    check('All earlier MAP2M evidence immutable',all((ROOT/p).is_file() and core.sha(ROOT/p)==digest for p,digest in b['earlier_proofs'].items()))
    check('Inherited 44 duplicate RGB and 12 invalid references unchanged',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    totals=economy.totals(economy.declarations())
    check('Brandenburg six arms levels',totals['STATE_BRANDENBURG','PRU','building_arms_industry']==6)
    check('Rhone five arms levels',totals['STATE_RHONE','FRA','building_arms_industry']==5)
    check('Canton ten trade levels and five port levels',totals['STATE_GUANGDONG','CHI','building_trade_center']==10 and totals['STATE_GUANGDONG','CHI','building_port']==5)
    check('No Chinese trade centre outside Canton',not any(sid!='STATE_GUANGDONG' and tag=='CHI' and kind=='building_trade_center' and count for (sid,tag,kind),count in totals.items()))
    check('HEAD unchanged',r2.head()==b['git_head'])
    check('Git index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    receipt=load('R2_USER_RUNTIME_VALIDATION.json')
    check('R2 manual receipt distinct from automated engine test',receipt.get('status')=='PASS_RUNTIME_USER_VALIDATED' and not receipt.get('automated_engine_test',False))
    prior=core.qa.counter(b['inventory']['regional_pop']);now=core.qa.counter(inv['regional_pop'])
    for sector,sids in [('PEENE',{'STATE_POMERANIA'}),('NETZE',{'STATE_POSEN','STATE_WEST_PRUSSIA'})]:
        rows=[]
        for key in sorted(prior.keys()|now.keys()):
            if key[0] in sids:rows.append(dict(State_ID=key[0],Owner=key[1],Culture=key[2],Religion=key[3],Before=prior[key],After=now[key],Difference=now[key]-prior[key]))
        write_csv(sector+'_POPULATION_VALIDATION.csv',rows)
        check('Sector population conserved '+sector,sum(v['Before'] for v in rows)==sum(v['After'] for v in rows))
    result=dict(status='MAP-2M-R3_PARTIAL',static_validation='PASS' if all(v['passed'] for v in checks) else 'FAIL',passed=sum(v['passed'] for v in checks),total=len(checks),checks=checks,
        sectors=dict(PEENE=dict(applied_cells=10,historical_geometry_complete=False),NETZE=dict(applied_cells=0,historical_geometry_complete=False)),
        world_population=835804980,population_transferred_pru_swe=1175,functional_files=sorted(changed),new_RGBs=[],
        inherited_duplicates=44,inherited_invalid_references=12,engine_tested=False,runtime_status='PENDING_USER_NEW_GAME_AND_ONE_MONTH',
        colgrep=dict(calls=1,successful_model_runs=0,elapsed_seconds=1.02,error='Access denied before local agent execution; exact-location fallback',codex_task_tokens=None,classic_search_count=None,economy_estimate='Not measurable without a successful comparative run'))
    dump('VALIDATION.json',result);previews()
    print(result['status'],result['static_validation'],result['passed'],'/',result['total'])
    for v in checks:
        if not v['passed']:print('FAIL',v['name'])
    assert result['static_validation']=='PASS'

def evidence():
    base='https://umweltkarten.lung-mv.de/dienste/wg_gewaesser?'
    params='SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&SRSNAME=EPSG:4326&OUTPUTFORMAT=application%2Fvnd.geo%2Bjson'
    files=[('LUNG_WATER_CAPABILITIES.xml',base+'SERVICE=WFS&REQUEST=GetCapabilities','Official LUNG MV; advertises Lizenz CC BY-SA',True),
        ('LUNG_PEENE.geojson',base+params+'&TYPENAME=fg&BBOX=53.75,12.8,54.25,14.0,EPSG:4326&MAXFEATURES=10000','LUNG MV; CC BY-SA as advertised',False),
        ('LUNG_PEENE_LONLAT.geojson',base+params+'&TYPENAME=fg&BBOX=12.8,53.75,14.0,54.25,EPSG:4326&MAXFEATURES=10000','LUNG MV; CC BY-SA as advertised',False),
        ('LUNG_PEENE_FEDERAL.geojson',base+params+'&TYPENAME=kul_fg__1o-bund&BBOX=12.8,53.75,14.0,54.25,EPSG:4326&MAXFEATURES=2000','LUNG MV; CC BY-SA as advertised',False),
        ('LUNG_PEENE_LAWA.geojson',base+params+'&TYPENAME=lawa&BBOX=12.8,53.75,14.0,54.25,EPSG:4326&MAXFEATURES=1000','LUNG MV; CC BY-SA as advertised',True),
        ('LUNG_PEENESTROM_WATER.geojson',base+params+'&TYPENAME=kg&BBOX=13.5,53.75,14.1,54.25,EPSG:4326&MAXFEATURES=100','LUNG MV; CC BY-SA as advertised',True),
        ('NE_COASTLINE.geojson','https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_coastline.geojson','Natural Earth, public-domain cartographic dataset',True),
        ('GSTA_NETZE_BOUNDARIES.html','https://archivdatenbank.gsta.spk-berlin.de/midosasearch-gsta/MidosaSEARCH/ii_ha_gd_abt_9/xml/inhalt/GStA_ii_ha_gd_abt_9_2_42.htm','GStA PK; catalogue metadata, not underlying manuscripts',True)]
    rows=[]
    for name,url,attribution,used in files:
        p=OUT/'EVIDENCE'/name;row=dict(file=p.relative_to(ROOT).as_posix(),url=url,attribution=attribution,used_in_decision=used,
            sha256=r2.core.sha(p),bytes=p.stat().st_size,accessed='2026-10-15')
        if name.endswith('geojson'):row['feature_count']=len(json.loads(p.read_text())['features'])
        rows.append(row)
    dump('SOURCES.json',dict(sources=rows,geometry_note='Contemporary hydrography supplies physical geometry only, not 1776 political borders. Modern dredging or schematic raster coast is not silently declared historical.',
        retrieval_notes=['Normal TLS validation retained. Python CA failure on LUNG was not bypassed; Windows Invoke-WebRequest trust store succeeded.',
            'WFS 1.1 server expects lon/lat BBOX despite EPSG:4326; lat/lon request returned zero features and was rejected.',
            'fg hit the 10000-feature cap, so its completeness is NOT assumed. LAWA named routes (284 features) and coastal water polygons (14) used instead.',
            'Raw downloads are retained with hashes; no re-download required to reproduce diagnostics. CC BY-SA version not specified by the service; retain attribution and inspect terms before external republication.'],
        reused_sources=['docs/reports/map/MAP2L/PRUSSIAN_BORDERS/MAYER_SOURCE.json','docs/reports/map/MAP2M/R1/SOURCES.json','docs/reports/map/MAP2M/R2/GEOMETRY_REVIEW.json','docs/reports/map/MAP2M/R2/PHYSICAL_DIAGNOSTIC.json'],
        archive_notices=[dict(reference='II. HA GD Abt. 9 Polizeiverwaltung Tit. 50 Nr. 1 a',date='1772',topic='Boundary boards for acquired province, September 1772; table',manuscript_consulted=False),
            dict(reference='Tit. 50 Nr. 2',date='1777',topic='Boundary regulation instructions by von Stach',manuscript_consulted=False),
            dict(reference='Tit. 50 Nr. 10',date='1776-1780',topic='Ostroveck/Skotnicki, Amt Kruszwice; note',manuscript_consulted=False)],
        schmettau=dict(status='NO_INDIVIDUALLY_DATED_TARGET_SHEET_OBTAINED',collection_span='1767-1787, not a uniform 1776 snapshot',
            consulted_catalogue='https://geobasis-bb.de/lgb/de/presse/pressemitteilungen/~13-02-2026-zeitreise-per-karte',territorial_use=False)))
    ds=[v['distance_px'] for v in load('GEOMETRY_REVIEW.json')['coastal_checks']]
    print('Coastal silhouette check mean/max',float(np.mean(ds)),max(ds),'NOT certified town errors')

def tests():
    names=['test_map2m_r3','test_map2m_r2','test_map2m_r1','test_map2l_registry','test_map2l_runtime_receipt','test_trade_center_pm_layout','test_start_economy_2026_10_15']
    stream=io.StringIO();start=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromNames(names)
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    dump('TESTS.json',dict(modules=names,tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),seconds=time.monotonic()-start,
        passed=result.wasSuccessful(),output=stream.getvalue(),automated_engine_test=False))
    print(stream.getvalue());assert result.wasSuccessful()

def delivery():
    """Cross-check delivered artifacts against the already validated live state."""
    v=load('VALIDATION.json');p=load('PLAN.json');b=load('BASELINE.json');checks={}
    required=['REPORT.md','UNRESOLVED.csv','TERRITORIAL_CHANGES.csv','PEENE_BEFORE_AFTER.png','NETZE_BEFORE_AFTER.png',
        'PEENE_POPULATION_VALIDATION.csv','NETZE_POPULATION_VALIDATION.csv','R2_USER_RUNTIME_VALIDATION.json',
        'SOURCES.json','TESTS.json','NETZE_POSITION_DIAGNOSTICS.csv','COLGREP.json']
    checks['All requested delivery artifacts exist']=all((OUT/n).is_file() for n in required)
    rows=list(csv.DictReader((OUT/'TERRITORIAL_CHANGES.csv').open(encoding='utf-8-sig')))
    expected=[{k:str(z) for k,z in row.items()} for row in p['changes']]
    checks['CSV equals complete applied plan']=rows==expected
    checks['Source provenance hashes match retained files']=all(r2.core.sha(ROOT/s['file'])==s['sha256'] for s in load('SOURCES.json')['sources'])
    checks['Installed raster remains validated']=r2.core.sha(ROOT/'map_data/provinces.png')==p['candidate_sha256']
    checks['49 static checks all pass']=v['static_validation']=='PASS' and v['passed']==v['total']==49 and all(z['passed'] for z in v['checks'])
    t=load('TESTS.json');checks['62 real tool tests pass']=t['passed'] and t['tests_run']==62 and t['errors']==t['failures']==0
    checks['No automated runtime claim']=not v['engine_tested'] and v['status']=='MAP-2M-R3_PARTIAL'
    native=r2.core.packed(ROOT/b['bitmap_backup']);owner={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    rows=list(csv.DictReader((OUT/'NETZE_POSITION_DIAGNOSTICS.csv').open(encoding='utf-8-sig')))
    checks['Diagnostic town CSV reflects actual R2 colours, not invented references']=all(
        int(native[int(float(z['Pixel_Y'])),int(float(z['Pixel_X']))])==int(z['RGB_at_floor_XY'][1:],16)
        and owner[z['RGB_at_floor_XY']]==[z['State_ID'],z['Owner']] for z in rows)
    for name in ['PEENE_BEFORE_AFTER.png','NETZE_BEFORE_AFTER.png']:Image.open(OUT/name).verify()
    checks['Both generated comparison PNGs decode']=True
    checks['HEAD and index remain unchanged']=r2.head()==b['git_head'] and r2.core.sha(ROOT/'.git/index')==b['git_index_sha256']
    dump('DELIVERY_CHECK.json',dict(passed=all(checks.values()),checks=checks))
    print('Delivery checks',sum(checks.values()),'/',len(checks));assert all(checks.values())

if __name__=='__main__':
    if sys.argv[1]=='fetch':fetch(sys.argv[2],sys.argv[3])
    else:{'capture':capture,'physical':physical,'geometry':geometry,'prepare':prepare,'install-raster':install_raster,'previews':previews,'validate':validate,'evidence':evidence,'tests':tests,'delivery':delivery}[sys.argv[1]]()
