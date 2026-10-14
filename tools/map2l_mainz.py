"""Mainz/Rheingau/Aschaffenburg and western Palatinate: explicit staged lot."""
from pathlib import Path
import collections as C
import csv
import json
import subprocess
import sys
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
from map2l_belgium import packed, sha
from map2l_hre_work import GIT
from map2l_registry import active_registry_path
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2b_patch import state, region, append
from map_1776_audit import values
from map2l_belgium import allocate, components
from map2l_franconia import inside
import re
import shutil

ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2L/MAINZ_PALATINATE'
SOURCE=OUT.parent/'RHINE_CENTRAL'
REGIONS={'STATE_HESSE','STATE_RHINELAND','STATE_FRANCONIA'}

def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'BASELINE.json').exists(),'Immutable lot baseline'
    backup=globals().get('BACKUP',SOURCE/'provinces_candidate.png')
    assert sha(backup)==sha(ROOT/'map_data/provinces.png')
    hashes={p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if any(sid in raw for sid in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    inventory=qa.inventory()
    dump('BASELINE.json',dict(inventory=inventory,hashes=hashes,originals=originals,
         bitmap_backup=backup.relative_to(ROOT).as_posix(),bitmap_sha256=sha(backup),
         registry=json.loads(active_registry_path().read_text()),
         git_head=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         git_index_sha256=sha(ROOT/'.git/index')))
    bmp=packed(backup);rows=[]
    for r in inventory['owners']:
        rgb,sid,tag=r['key']
        if sid not in REGIONS:continue
        ys,xs=np.where(bmp==int(rgb[1:],16))
        rows.append(dict(RGB=rgb,State=sid,Owner=tag,Pixels=len(xs),X_min=int(xs.min()),X_max=int(xs.max()),Y_min=int(ys.min()),Y_max=int(ys.max())))
    with (OUT/'CURRENT.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('Baseline captured;',len(rows),'province references;',len(originals),'source snapshots; runtime unchanged')

def crops():
    OUT.mkdir(parents=True,exist_ok=True)
    image=Image.open(SOURCE/'DE_WIT_MAINZ_3500.jpg').convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for name,box in [('RHEINGAU',(190,1020,1430,1610)),('ASCHAFFENBURG',(2110,1050,3330,1940)),('MAIN_CORE',(1350,1060,2400,1770)),('MAIN_TOWN',(2700,1260,2970,1460))]:
        im=image.crop(box);d=ImageDraw.Draw(im)
        for x in range((box[0]//100+1)*100,box[2],100):
            d.line((x-box[0],0,x-box[0],im.height),fill='blue');d.text((x-box[0]+1,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            d.line((0,y-box[1],im.width,y-box[1]),fill='blue');d.text((1,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        im.save(OUT/(name+'_READING.png'))
    west=OUT/'SCHENK_PALATINATE.jpg'
    if west.exists():
        image=Image.open(west).convert('RGB')
        for name,box in [('WEST_PALATINATE',(570,750,2310,1920)),('WEST_ANCHORS',(220,550,2410,1920))]:
            im=image.crop(box);d=ImageDraw.Draw(im)
            for x in range((box[0]//100+1)*100,box[2],100):
                d.line((x-box[0],0,x-box[0],im.height),fill='blue');d.text((x-box[0]+1,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
            for y in range((box[1]//100+1)*100,box[3],100):
                d.line((0,y-box[1],im.width,y-box[1]),fill='blue');d.text((1,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
            im.save(OUT/(name+'_READING.png'))
        for name,box in [('SCHENK_MAINZ',(1790,740,1990,930)),('SCHENK_FRANKFURT',(2170,580,2390,710)),('SCHENK_NECKAR',(2130,1620,2730,1930))]:
            image.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2)).save(OUT/(name+'.png'))
    image=Image.open(SOURCE/'VAUGONDY_SANTINI_DETAIL.jpg').convert('RGB')
    box=(1200,860,2200,1500);im=image.crop(box).resize((1500,960));d=ImageDraw.Draw(im)
    for x in range(1200,2200,100):
        d.line(((x-1200)*1.5,0,(x-1200)*1.5,im.height),fill='blue');d.text(((x-1200)*1.5+2,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
    for y in range(900,1500,100):
        d.line((0,(y-860)*1.5,im.width,(y-860)*1.5),fill='blue');d.text((1,(y-860)*1.5+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
    im.save(OUT/'VAUGONDY_NORTH_READING.png')

def fetch_west():
    # A narrowly targeted readable substitute for blocked Vaugondy scans.
    url='https://www.e-rara.ch/i3f/v20/29042527/manifest'
    assert not (OUT/'SCHENK_PALATINATE.jpg').exists()
    with urllib.request.urlopen(url,timeout=25) as r:manifest=json.load(r)
    service=manifest['sequences'][0]['canvases'][0]['images'][0]['resource']['service']['@id']
    with urllib.request.urlopen(service+'/full/3500,/0/default.jpg',timeout=25) as r:data=r.read(30_000_001)
    assert len(data)<=30_000_000
    import io
    Image.open(io.BytesIO(data)).verify()
    (OUT/'SCHENK_PALATINATE.jpg').write_bytes(data)
    dump('SCHENK_SOURCE.json',dict(catalogue='https://www.e-rara.ch/doi/10.3931/e-rara-112447',
        manifest_url=url,manifest=manifest,image_service=service,sha256=sha(OUT/'SCHENK_PALATINATE.jpg'),
        date='after 1695',institution='Universitätsbibliothek Bern, MUE Ryh 3002:28',
        license='Public Domain Mark',warning='Older geographical envelope, not automatic evidence of 1776 ownership'))
    print(service,Image.open(OUT/'SCHENK_PALATINATE.jpg').size)

def emit(files,name):
    import map2l_belgium as emitter
    emitter.LOT=OUT
    return emitter.emit(files,name)

def preview(bmp,rows,name):
    cfg=json.loads((OUT/'TRACING.json').read_text())
    box=cfg.get('preview_box',(4255,846,4329,889));x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1]
    colors={'KMZ':'#bd3e32','KPF':'#d7aa32','HES':'#609ab6','BAV':'#aaaabb','PRU':'#607d76','FRM':'#ec8a43','WZB':'#9975bb','AUS':'#b5b0d7','VEN':'#69b9ac','SWI':'#bd6861','SAR':'#809bac','PAR':'#acd19e','MOD':'#dec788'}
    image=Image.new('RGB',(local.shape[1],local.shape[0]),'#ececec');arr=np.array(image)
    from PIL import ImageColor
    for r in rows:
        rgb,sid,tag=r['key'];arr[local==int(rgb[1:],16)]=ImageColor.getrgb(colors.get(tag,'#c8c8c0'))
    edge=np.zeros(local.shape,dtype=bool);edge[1:]|=local[1:]!=local[:-1];edge[:,1:]|=local[:,1:]!=local[:,:-1];arr[edge]=50
    image=Image.fromarray(arr).resize((local.shape[1]*14,local.shape[0]*14),Image.Resampling.NEAREST)
    out=Image.new('RGB',(image.width,image.height+65),'white');out.paste(image);d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for tag,x,y in cfg.get('preview_labels',[('Rheingau',4283,861),('Mainz (hub)',4291,866),('Frankfurt',4300,856),('Aschaffenburg core',4312,862),('Otterberg raccord',4270,873),('Kaiserslautern',4268,879)]):
        point=((x-x0)*14,(y-y0)*14);d.text(point,tag,font=font,fill='black',stroke_width=2,stroke_fill='white')
    d.text((10,image.height+5),name+' | source-traced core approximations; unchanged fringes NOT certified',font=font,fill='black')
    d.text((10,image.height+30),cfg.get('preview_legend','KMZ red / KPF gold / HES blue / BAV gray / PRU green / FRM orange'),font=font,fill='black')
    out.save(OUT/(name+'.png'))

def geometry():
    b=json.loads((OUT/'BASELINE.json').read_text());c=json.loads((OUT/'TRACING.json').read_text())
    assert sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    if 'calibrated_sources' in c:return geometry_layers(b,c)
    X=np.array([[*p['source'],1] for p in c['points']]);Y=np.array([p['game'] for p in c['points']]);T=np.linalg.lstsq(X,Y,rcond=None)[0]
    fit=[p for p in c['cross_points'] if p['role']=='FIT'];U=np.linalg.solve(np.array([[*p['source'],1] for p in fit]),np.array([p['target'] for p in fit]))
    crossT=np.vstack((np.column_stack((U[:2],np.zeros(2))),[*U[2],1]))@T
    metrics=[dict(**p,predicted_game=(np.array([*p['source'],1])@T).tolist(),error_game_px=float(np.linalg.norm(np.array([*p['source'],1])@T-p['game']))) for p in c['points']]
    cross=[]
    for p in c['cross_points']:
        predicted=np.array([*p['source'],1])@crossT
        cross.append(dict(**p,predicted_game=predicted.tolist(),error_game_px=float(np.linalg.norm(predicted-p['game'])) if 'game' in p else None))
    assert max(p['error_game_px'] for p in metrics)<4.3
    dump('ALIGNMENT.json',dict(matrix_source_to_game=T.tolist(),matrix_de_wit_to_schenk=U.tolist(),matrix_de_wit_to_game=crossT.tolist(),
         points=metrics,cross_points=cross,source_sha256=sha(OUT/c['source']),cross_source_sha256=sha(OUT/c['cross_source']),
         warning='Fit residuals are not independent validation. Remote Giessen fails extrapolation; only explicit conservative local parents approved.'))
    for source,matrix,filename in [('SCHENK',T,'SCHENK_OVERLAY.png'),('DE_WIT',crossT,'DE_WIT_OVERLAY.png')]:
        image=Image.open(OUT/c['source'] if source=='SCHENK' else OUT/c['cross_source']).convert('RGB');d=ImageDraw.Draw(image)
        for p in c['polygons']:
            if p['source']==source:d.line([tuple(q) for q in p['points']]+[tuple(p['points'][0])],fill='red' if p['owner']=='KMZ' else 'blue',width=5)
        image.save(OUT/filename)
    before=packed(ROOT/'map_data/provinces.png');after=before.copy();oldowners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    colors=set(np.unique(before).tolist());new=[];assignments=[];counter=0
    for parent in c['parents']:
        value=int(parent[1:],16);sid,oldowner=oldowners[parent];ys,xs=np.where(before==value);cells=np.column_stack((xs,ys));tags=np.array([oldowner]*len(cells),dtype='U3');zones=np.zeros(len(cells),dtype=int)
        for i,p in enumerate(c['polygons'],1):
            if parent not in p['parents']:continue
            matrix=T if p['source']=='SCHENK' else crossT
            points=(cells+0.5-matrix[2])@np.linalg.inv(matrix[:2]);selected=inside(points,p['points']);tags[selected]=p['owner'];zones[selected]=i
        groups=[]
        for zone in sorted(set(zones)):
            mask=np.zeros(before.shape,dtype=bool);mask[ys[zones==zone],xs[zones==zone]]=True
            tag=str(tags[zones==zone][0])
            for part in components(mask):groups.append(dict(owner=tag,state=sid,source_zone=int(zone),pixels=len(part),cells=[(x,y) for y,x in part]))
        assert any(g['source_zone'] for g in groups),'Envelope does not intersect '+parent
        keep=next(g for g in groups if (4268,879) in g['cells']) if parent=='x11C021' else max(groups,key=lambda g:g['pixels'])
        for g in groups:
            rgb=parent
            if g is not keep:
                while 0xEDA400+counter in colors:counter+=1
                color=0xEDA400+counter;counter+=1;colors.add(color);rgb='x'+format(color,'06X');new.append(dict(rgb=rgb,parent_rgb=parent))
            for x,y in g['cells']:after[y,x]=int(rgb[1:],16)
            assignments.append(dict(rgb=rgb,parent_rgb=parent,previous_owner=oldowner,**g))
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    scope=[r for r in b['inventory']['owners'] if r['key'][1] in REGIONS and r['key'][0] not in c['parents']]+[dict(key=[r['rgb'],r['state'],r['owner']],count=1) for r in assignments]
    preview(before,b['inventory']['owners'],'BEFORE');preview(after,scope,'AFTER')
    left=Image.open(OUT/'BEFORE.png');right=Image.open(OUT/'AFTER.png');both=Image.new('RGB',(left.width*2,left.height),'white');both.paste(left);both.paste(right,(left.width,0));both.save(OUT/'BEFORE_AFTER.png')
    transfers=C.Counter()
    for r in assignments:
        if r['owner']!=r['previous_owner']:transfers[r['state']+'/'+r['previous_owner']+'->'+r['owner']]+=r['pixels']
    dump('GEOMETRY.json',dict(status='SOURCE_TRACED_CORE_SUBLOT_NOT_COMPLETE_RHINE',parents=c['parents'],assignments=assignments,new_provinces=new,
         transfers=dict(transfers),candidate_sha256=sha(OUT/'provinces_candidate.png'),changed_pixels=int((before!=after).sum()),limitations=c['limitations']))
    print('Candidate:',len(new),'new RGBs;',dict(transfers),'; residuals',[(p['name'],round(p['error_game_px'],3)) for p in metrics])

def geometry_layers(b,c):
    """Explicit pre-reviewed local matrices, independently auditable sources."""
    sources={s['key']:s for s in c['calibrated_sources']};matrices={k:np.array(s['matrix']) for k,s in sources.items()}
    dump('ALIGNMENT.json',dict(sources=[dict(**s,sha256=sha(OUT/s['path'])) for s in sources.values()],
         method=c['method'],warning=c['limitations']))
    for key,s in sources.items():
        image=Image.open(OUT/s['path']).convert('RGB');d=ImageDraw.Draw(image)
        for p in c['polygons']:
            if p['source']==key:d.line([tuple(q) for q in p['points']]+[tuple(p['points'][0])],fill='red',width=2 if key=='HL' else 5)
        for q in s.get('controls',[]):
            x,y=q['source'];d.ellipse((x-3,y-3,x+3,y+3),fill='blue')
        image.save(OUT/(key+'_OVERLAY.png'))
    before=packed(ROOT/'map_data/provinces.png');after=before.copy();owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    colors=set(np.unique(before).tolist());new=[];assignments=[];counter=0
    anchors=json.loads((OUT/c.get('native_anchors','../RHINE_CENTRAL/NATIVE_ANCHORS.json')).read_text())
    for parent in c['parents']:
        value=int(parent[1:],16);sid,oldowner=owners[parent];ys,xs=np.where(before==value);cells=np.column_stack((xs,ys));tags=np.array([c.get('default_owners',{}).get(parent,oldowner)]*len(cells),dtype='U3');zones=np.zeros(len(cells),dtype=int)
        for i,p in enumerate(c['polygons'],1):
            if parent not in p['parents']:continue
            t=matrices[p['source']];src=(cells+0.5-t[2])@np.linalg.inv(t[:2]);take=inside(src,p['points'])
            for hole in p.get('exclusions',[]):take&=~inside(src,hole['points'])
            tags[take]=p['owner'];zones[take]=i
        if c.get('discover_only'):continue
        groups=[]
        for zone in sorted(set(zones)):
            mask=np.zeros(before.shape,dtype=bool);mask[ys[zones==zone],xs[zones==zone]]=True
            for part in components(mask):groups.append(dict(owner=str(tags[zones==zone][0]),state=sid,source_zone=int(zone),pixels=len(part),cells=[(x,y) for y,x in part]))
        assert any(r['source_zone'] for r in groups),'No source envelope intersects '+parent
        hubs={(int(float(r['Locator_X'])),int(float(r['Locator_Y']))) for r in anchors if before[int(float(r['Locator_Y'])),int(float(r['Locator_X']))]==value}
        hubgroups=[r for r in groups if hubs&set(r['cells'])]
        assert len(hubgroups)<=1,'Review multiple hubs in split '+parent
        keep=hubgroups[0] if hubgroups else max(groups,key=lambda r:r['pixels'])
        for r in groups:
            rgb=parent
            if r is not keep:
                while c['rgb_start']+counter in colors:counter+=1
                color=c['rgb_start']+counter;counter+=1;colors.add(color);rgb='x'+format(color,'06X');new.append(dict(rgb=rgb,parent_rgb=parent))
            for x,y in r['cells']:after[y,x]=int(rgb[1:],16)
            assignments.append(dict(rgb=rgb,parent_rgb=parent,previous_owner=oldowner,**r))
    if c.get('discover_only'):
        findings=[]
        for parent in c['parents']:
            sid,owner=owners[parent];ys,xs=np.where(before==int(parent[1:],16));cells=np.column_stack((xs,ys))
            for p in c['polygons']:
                if parent not in p['parents']:continue
                t=matrices[p['source']];src=(cells+0.5-t[2])@np.linalg.inv(t[:2]);take=inside(src,p['points'])
                for hole in p.get('exclusions',[]):take&=~inside(src,hole['points'])
                count=int(take.sum())
                if count:findings.append(dict(parent=parent,state=sid,owner=owner,source=p['territory'],pixels=count))
        dump('CANDIDATE_INTERSECTIONS.json',findings);print(json.dumps(findings,ensure_ascii=False));return
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    scope=[r for r in b['inventory']['owners'] if r['key'][0] not in c['parents']]+[dict(key=[r['rgb'],r['state'],r['owner']],count=1) for r in assignments]
    preview(before,b['inventory']['owners'],'BEFORE');preview(after,scope,'AFTER');left=Image.open(OUT/'BEFORE.png');right=Image.open(OUT/'AFTER.png');both=Image.new('RGB',(left.width*2,left.height),'white');both.paste(left);both.paste(right,(left.width,0));both.save(OUT/'BEFORE_AFTER.png')
    transfers=C.Counter()
    for r in assignments:
        if r['owner']!=r['previous_owner']:transfers[r['state']+'/'+r['previous_owner']+'->'+r['owner']]+=r['pixels']
    dump('GEOMETRY.json',dict(status='SOURCE_TRACED_MAINZ_ESTATES_GAME_SCALE',parents=c['parents'],assignments=assignments,new_provinces=new,transfers=dict(transfers),
        candidate_sha256=sha(OUT/'provinces_candidate.png'),tracing_sha256=sha(OUT/'TRACING.json'),changed_pixels=int((before!=after).sum()),limitations=c['limitations']))
    print('Candidate',len(new),'new RGBs;',dict(transfers))

def prepare():
    b=json.loads((OUT/'BASELINE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text());files={};allocations=[];bmp=packed(ROOT/b['bitmap_backup'])
    assert sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    if 'tracing_sha256' in g:assert sha(OUT/'TRACING.json')==g['tracing_sha256'],'Regenerate candidate after tracing changes'
    oldowners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']};affected={oldowners[rgb] for rgb in g['parents']};weights={}
    for sid,src in sorted(affected):
        counts=C.Counter()
        for r in b['inventory']['owners']:
            if r['key'][1:]==[sid,src] and r['key'][0] not in g['parents']:counts[src]+=int((bmp==int(r['key'][0][1:],16)).sum())
        for r in g['assignments']:
            if (r['state'],r['previous_owner'])==(sid,src):counts[r['owner']]+=r['pixels']
        assert counts[src]>0 or any(r['state']==sid and r['owner']==src for r in g['assignments']),'Do not invalidate private economic holders or recruitment subdivisions'
        weights[sid,src]=counts
    rel='common/history/states/00_states.txt';raw=b['originals'][rel]
    for sid in sorted(REGIONS):
        parents={r for r in g['parents'] if oldowners[r][0]==sid}
        if not parents:continue
        assigns=[r for r in g['assignments'] if r['state']==sid];existing={n.one('country').split(':')[-1]:n for n in state(raw,sid).children('create_state')};ops=[];added=[]
        for tag in sorted({r['owner'] for r in assigns}|{oldowners[r][1] for r in parents}):
            rgbs=[r['rgb'] for r in assigns if r['owner']==tag]
            if tag in existing:
                n=existing[tag];owned=n.children('owned_provinces')[0];rgbs=[r for r in values(n,'owned_provinces') if r not in parents]+rgbs
                ops.append((owned.start,owned.end,'owned_provinces = { '+' '.join(rgbs)+' }'))
            else:added.append('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(rgbs)+' } }')
        if added:s=state(raw,sid);ops.append((s.end-1,s.end-1,'\n'+'\n'.join(added)+'\n'))
        raw=edits(raw,ops)
    files[rel]=raw
    rel=globals().get('REGION_FILE','map_data/state_regions/00_west_europe.txt');raw=b['originals'][rel]
    for sid in sorted(REGIONS):
        parents={r for r in g['parents'] if oldowners[r][0]==sid}
        if not parents:continue
        s=next(n for n in cw.parse(raw) if n.key==sid);ps=s.children('provinces')[0];rgbs=[r for r in values(s,'provinces') if r not in parents]+[r['rgb'] for r in g['assignments'] if r['state']==sid]
        raw=edits(raw,[(ps.start,ps.end,'provinces = { '+' '.join('"'+r+'"' for r in rgbs)+' }')])
    files[rel]=raw
    for rel,original in b['originals'].items():
        if '/pops/' not in rel and '/buildings/' not in rel:continue
        raw=original;all_ops=[];all_moved=C.defaultdict(list)
        for (sid,src),counts in weights.items():
            # Always allocate from the immutable source, never process a
            # population/building newly appended by another transfer again.
            try:n=region(original,sid,src)
            except StopIteration:continue
            ops=[];moved=C.defaultdict(list)
            if '/pops/' in rel:
                for pop in n.children('create_pop'):
                    size=pop.children('size')[0];amounts=allocate(int(size.value),counts);piece=raw[pop.start:pop.end]
                    ops.append((size.start,size.end,'size = '+str(amounts[src]))) if amounts[src] else ops.append((pop.start,pop.end,''))
                    for tag,amount in amounts.items():
                        if tag!=src and amount:moved[tag].append(edits(piece,[(size.start-pop.start,size.end-pop.start,'size = '+str(amount))]))
                    allocations.append(dict(kind='population',file=rel,state=sid,source=src,profile=cw.scalar(pop.one('culture'))+'/'+cw.scalar(pop.one('religion','DEFAULT')),before=int(size.value),after=amounts))
            else:
                for building in n.children('create_building'):
                    levels=[v for v in cw.walk(building.children()) if v.key=='levels' and isinstance(v.value,str)]
                    if not levels:continue
                    piece=raw[building.start:building.end];bytag=C.defaultdict(list);totals=C.Counter()
                    for v in levels:
                        amounts=allocate(int(v.value),counts)
                        for tag,amount in amounts.items():bytag[tag].append((v.start-building.start,v.end-building.start,'levels = '+str(amount)));totals[tag]+=amount
                    if not any(amount for tag,amount in totals.items() if tag!=src):
                        allocations.append(dict(kind='building',file=rel,state=sid,source=src,profile=cw.scalar(building.one('building')),before=sum(int(v.value) for v in levels),after=dict(totals)))
                        continue
                    fragments={}
                    for tag in counts:
                        if not totals[tag]:continue
                        fragment=edits(piece,bytag[tag]);zeros=[]
                        for own in cw.parse(fragment)[0].children('add_ownership'):
                            for holder in own.children():
                                if holder.one('levels')=='0':zeros.append((holder.start,holder.end,''))
                        fragment=edits(fragment,zeros)
                        if tag!=src and cw.scalar(building.one('building'))=='building_government_administration':fragment=re.sub(r'(country\s*=\s*"?c:)'+src,r'\g<1>'+tag,fragment)
                        fragments[tag]=fragment
                    ops.append((building.start,building.end,fragments.get(src,'')))
                    for tag,fragment in fragments.items():
                        if tag!=src:moved[tag].append(fragment)
                    allocations.append(dict(kind='building',file=rel,state=sid,source=src,profile=cw.scalar(building.one('building')),before=sum(int(v.value) for v in levels),after=dict(totals)))
            all_ops.extend(ops)
            for tag,pieces in moved.items():all_moved[sid,tag].extend(pieces)
        raw=edits(original,all_ops)
        for (sid,tag),pieces in all_moved.items():raw=append(raw,sid,tag,'\n'.join(pieces))
        if raw!=original:files[rel]=raw
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tmap={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for r in g['new_provinces']:terrain+='\n'+r['rgb']+'="'+tmap[r['parent_rgb'].upper()]+'"'
    (OUT/'province_terrains_candidate.txt').write_text(terrain+'\n',encoding='utf-8')
    previous=[r for r in b['registry'] if r['state'] in REGIONS];updated=[r for r in previous if r['rgb'] not in g['parents']]
    registered_owners=json.loads((OUT/'TRACING.json').read_text()).get('imperial_owners')
    updated += [dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L '+OUT.name+': source-traced game-scale territory; retained fringe not historically certified; see REPORT.md.') for r in g['assignments'] if registered_owners is None or r['owner'] in registered_owners]
    ledger=sorted([r for r in b['registry'] if r['state'] not in REGIONS]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)
    migration=dict(replaced_regions=sorted(REGIONS),previous=previous,updated=updated,new_members=[],free_cities=[],new_provinces=g['new_provinces'],geometry=OUT.name+'/GEOMETRY.json')
    if registered_owners is not None:
        migration['ownership_previous']=[dict(rgb=r['key'][0],state=r['key'][1],beneficiary=r['key'][2]) for r in b['inventory']['owners'] if r['key'][1] in REGIONS]
        migration['ownership_updated']=[r for r in migration['ownership_previous'] if r['rgb'] not in g['parents']]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner']) for r in g['assignments']]
        after=packed(OUT/'provinces_candidate.png')
        before_mask=np.isin(bmp,[int(r['rgb'][1:],16) for r in b['registry']])
        after_mask=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
        migration['extent_added_cells']=[[int(x),int(y)] for y,x in zip(*np.where(after_mask&~before_mask))]
        migration['extent_removed_cells']=[[int(x),int(y)] for y,x in zip(*np.where(before_mask&~after_mask))]
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)
    for rel,raw in files.items():
        if rel.endswith('.txt'):cw.parse(raw)
    changes=emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,allocations=allocations,new_tags=[],registered_RGBs=len(ledger),method='Exact integer culture/religion and building profile conservation; weights by complete source state subdivision, not pixels as a census'))
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        keys=['rgb','parent_rgb','state','previous_owner','owner','pixels'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(g['assignments'])
    print('Prepared',len(changes),'text files;',len(ledger),'registered RGBs;',len(allocations),'allocation profiles')

def install():
    b=json.loads((OUT/'BASELINE.json').read_text());p=json.loads((OUT/'PLAN.json').read_text())
    assert sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert all(sha(ROOT/rel)!=b['hashes'][rel] for rel in p['files'] if rel in b['hashes'])
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png');shutil.copyfile(OUT/'province_terrains_candidate.txt',ROOT/'map_data/province_terrains.txt')

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();changes=emit(files,'IMPERIAL.patch');dump('IMPERIAL_FILES.json',dict(files=changes,all_compiled_files=list(files)))
    print('Prepared',len(changes),'imperial runtime updates')

def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
    import prototype_map2k_main_map as main
    main.MOD=ROOT;main.PACKAGE=OUT/'MAIN_MAP';main.PACKAGE.mkdir(exist_ok=True);main.build_and_test()

if __name__=='__main__':{'capture':capture,'crops':crops,'fetch-west':fetch_west,'geometry':geometry,'prepare':prepare,'install':install,'imperial':imperial,'maps':maps}[sys.argv[1]]()
