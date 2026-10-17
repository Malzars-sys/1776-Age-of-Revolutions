"""MAP-2M-R2: isolated differential map correction; old hypotheses stay immutable."""
import collections as C
import csv
import difflib
import json
import os
import sys
import subprocess
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2l_mainz as core
import map2m_border_work as old
import start_buildings_2026_10_15 as economy

ROOT = core.ROOT
OUT = old.BASE / 'R2'
SECTORS = {'PEENE': (4372,711,4442,775), 'NETZE': (4435,740,4550,812)}
NEW_RGB = 'xEDB010'

def dump(name, value):
    p = OUT/name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def load(name):
    return json.loads((OUT/name).read_text(encoding='utf-8'))

def head():
    return subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')).strip()

def capture():
    assert not (OUT/'BASELINE.json').exists(), 'Never replace an existing reference'
    inv = core.qa.inventory()
    bmp = core.packed(ROOT/'map_data/provinces.png')
    original = old.PREVIOUS/'provinces_candidate.png'
    assert core.sha(original) == core.sha(ROOT/'map_data/provinces.png')
    owners = {r['key'][0]:r['key'][1:] for r in inv['owners']}
    assert owners['x567452'] == ['STATE_POMERANIA','SWE'] and int((bmp==0x567452).sum())==341
    assert sum(r['count'] for r in inv['pops']) == 835804980
    refs = {p.relative_to(ROOT).as_posix():core.sha(p) for p in old.BASE.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json', dict(inventory=inv, hashes=economy.runtime_hashes(), bitmap_backup=original.relative_to(ROOT).as_posix(),
         bitmap_sha256=core.sha(original), registry=json.loads(core.active_registry_path().read_text()),
         git_head=head(), git_index_sha256=core.sha(ROOT/'.git/index'), earlier_proofs=refs))
    print('Captured current dirty workspace, population',sum(r['count'] for r in inv['pops']))

def diagnostics():
    b=load('BASELINE.json'); owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    bmp=core.packed(ROOT/b['bitmap_backup'])
    rivers=np.asarray(Image.open(core.qa.GAME/'map_data/rivers.png').convert('RGB'))
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    for sector,box in SECTORS.items():
        x0,y0,x1,y1=box; local=bmp[y0:y1,x0:x1]
        arr=np.full((*local.shape,3),235,dtype=np.uint8)
        for rgb in np.unique(local):
            tag=owners.get('x'+format(int(rgb),'06X'))
            arr[local==rgb]={'PRU':(145,190,225),'SWE':(235,205,65),'PLC':(220,160,160)}.get(tag,(235,235,235))
        edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];arr[edge]=80
        river=rivers[y0:y1,x0:x1];water=(river.min(axis=2)!=river.max(axis=2))|((river[:,:,0]==0)&(river[:,:,2]>0))
        arr[water]=river[water]
        im=Image.fromarray(arr).resize(((x1-x0)*16,(y1-y0)*16),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        for x in range((x0//5+1)*5,x1,5):
            d.line(((x-x0)*16,0,(x-x0)*16,im.height),fill='#aaaaaa');d.text(((x-x0)*16,0),str(x),font=font,fill='black')
        for y in range((y0//5+1)*5,y1,5):
            d.line((0,(y-y0)*16,im.width,(y-y0)*16),fill='#aaaaaa');d.text((0,(y-y0)*16),str(y),font=font,fill='black')
        im.save(OUT/(sector+'_NATIVE_DIAGNOSTIC.png'))
    # Only a reading grid; not a geometrical correction or an approved transform.
    for name,box in [('PEENE_MAYER',(0,0,949,768)),('NETZE_GUSSE',(1280,2110,1780,2490))]:
        src=old.PREVIOUS/'EVIDENCE/MAYER_1763_GREIFSWALD.jpg' if name.startswith('PEENE') else old.BASE/'EVIDENCE/GUESSEFELD_1775.jpg'
        im=Image.open(src).convert('RGB').crop(box);d=ImageDraw.Draw(im)
        for x in range((box[0]//50+1)*50,box[2],50):d.line((x-box[0],0,x-box[0],im.height),fill='#6495ed');d.text((x-box[0],0),str(x),fill='blue')
        for y in range((box[1]//50+1)*50,box[3],50):d.line((0,y-box[1],im.width,y-box[1]),fill='#6495ed');d.text((0,y-box[1]),str(y),fill='blue')
        im.resize((im.width*2,im.height*2)).save(OUT/(name+'_READING.png'))

def physical():
    """Independent shape diagnostic. Distances to rivers are not city errors."""
    from georeference.model import forward
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json').read_text())['model']
    geo_path=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'
    features=json.loads(geo_path.read_text())['features']
    rivers=np.asarray(Image.open(core.qa.GAME/'map_data/rivers.png').convert('RGB'))
    entries={}
    for name,box,extent in [('Vistula',(4500,710,4540,785),(17,20,52.8,54.5)),('Oder',(4405,730,4438,785),(13,15,52.1,54))]:
        lines=[np.array(f['geometry']['coordinates'])[:,:2] for f in features if f['properties'].get('name')==name and f['geometry']['type']=='LineString']
        geo=np.vstack(lines);lo,hi,south,north=extent;geo=geo[(geo[:,0]>=lo)&(geo[:,0]<=hi)&(geo[:,1]>=south)&(geo[:,1]<=north)]
        x0,y0,x1,y1=box;q=rivers[y0:y1,x0:x1]
        # These windows isolate each named major river; no anonymous nearest tributary.
        mask=(q.min(axis=2)!=q.max(axis=2))|((q[:,:,0]==0)&(q[:,:,2]>0))
        ys,xs=np.where(mask);target=np.column_stack((xs+x0+.5,ys+y0+.5))
        entries[name]=(geo,forward(model,geo),target)
    geo,pred,target=entries['Vistula']
    def distances(points, target):
        return np.sqrt(((points[:,None,:]-target[None,:,:])**2).sum(axis=2).min(axis=1))
    # One rigid offset only. Never fit/check using named game towns.
    # Reserve the Bromberg/Fordon latitude band before fitting the northern route.
    fit_pred=pred[geo[:,1]>=53.30]
    def loss(offset):
        d=distances(fit_pred+offset,target)
        return float((2*(np.sqrt(1+d*d)-1)).sum())
    offsets=[np.array([x,y]) for x in np.arange(-12,12.01,.5) for y in np.arange(-12,12.01,.5)]
    offset=min(offsets,key=loss)
    offsets=[offset+[x,y] for x in np.arange(-.5,.51,.1) for y in np.arange(-.5,.51,.1)]
    offset=min(offsets,key=loss)
    results={}
    for name,(geo,pred,target) in entries.items():
        ds=distances(pred+offset,target)
        results[name]=dict(role='FIT_AND_HELD_OUT_LOCAL_BAND' if name=='Vistula' else 'CHECK',vertices=len(geo),mean_distance=float(ds.mean()),max_distance=float(ds.max()),
                           geo=geo.tolist(),predicted=(pred+offset).tolist(),native_river=target.tolist())
        if name=='Vistula':
            heldout=(geo[:,1]>=53.0)&(geo[:,1]<53.30)
            results[name]['held_out_band']=dict(vertices=int(heldout.sum()),mean_distance=float(ds[heldout].mean()),max_distance=float(ds[heldout].max()),latitudes=[53.0,53.30])
    towns=[('Demmin',[13.036,53.907]),('Anklam',[13.692,53.856]),('Greifswald',[13.381,54.095]),('Wolgast',[13.776,54.052]),
           ('Bromberg',[18.008,53.123]),('Inowroclaw',[18.261,52.799]),('Pila',[16.738,53.151]),('Walcz',[16.475,53.273])]
    dump('PHYSICAL_DIAGNOSTIC.json',dict(offset=offset.tolist(),results=results,targets=[dict(name=n,geo=g,predicted=(forward(model,[g])[0]+offset).tolist()) for n,g in towns],
        warning='Distances to generalized river routes, not certified positional errors of cities; no sovereignty or transfer is authorized by this fit alone.',source_sha256=core.sha(geo_path)))
    print('Physical route diagnostic offset:',offset)
    print({k:{p:v[p] for p in ['vertices','mean_distance','max_distance']} for k,v in results.items()})
    print(load('PHYSICAL_DIAGNOSTIC.json')['targets'])

def geometry():
    """Intersect conservative interiors; never import a candidate CSV as history."""
    from georeference.model import forward
    b=load('BASELINE.json');bmp=core.packed(ROOT/b['bitmap_backup'])
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    native=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json').read_text())['model']
    offset=np.array(load('PHYSICAL_DIAGNOSTIC.json')['offset'])
    sources={s:json.loads((old.BASE/s/'CANDIDATE_MODEL.json').read_text()) for s in SECTORS}
    peene_source=np.array([[80,219,1],[505,28,1],[664,432,1]])
    peene_target=np.array([[4380,724],[4399,715],[4409,732]])
    peene_matrix=np.linalg.solve(peene_source,peene_target)
    # Modern coordinates establish source geometry, not a new sovereignty claim.
    netze_source=np.array([[1760,1335,1],[1410,2318,1],[1680,2395,1]])
    netze_geo=[[18.646,54.352],[18.008,53.123],[18.604,53.010]]
    netze_target=forward(native,netze_geo)+offset
    netze_matrix=np.linalg.solve(netze_source,netze_target)
    def inside_margin(cells, polygon, margin):
        cells=np.asarray(cells,float);poly=np.asarray(polygon,float)
        # Distance to polygon boundary is only a sensitivity buffer, NOT accuracy.
        d=np.full(len(cells),np.inf)
        for a,z in zip(poly,np.roll(poly,-1,axis=0)):
            ab=z-a;den=float(ab@ab)
            if not den:continue
            u=np.clip(((cells-a)@ab)/den,0,1)
            d=np.minimum(d,np.linalg.norm(cells-(a+u[:,None]*ab),axis=1))
        return core.inside(cells,poly)&(d>=margin)
    results={}
    for sector,parent,new_matrix,margin in [('PEENE','xE1A03A',peene_matrix,2.0),('NETZE','xFCC7B7',netze_matrix,1.0)]:
        cfg=sources[sector];old_matrix=np.array(cfg['matrix']);poly=np.array(cfg['polygon'])
        ys,xs=np.where(bmp==int(parent[1:],16));cells=np.column_stack((xs+.5,ys+.5))
        poly_old=np.column_stack((poly,np.ones(len(poly))))@old_matrix
        poly_new=np.column_stack((poly,np.ones(len(poly))))@new_matrix
        take=inside_margin(cells,poly_old,margin)&inside_margin(cells,poly_new,margin)
        # Do not turn a thin inland uncertainty sliver into a disconnected enclave.
        mask=np.zeros(bmp.shape,dtype=bool);mask[ys[take],xs[take]]=True
        if sector=='PEENE':
            # Eastern tip cannot be distinguished safely from northern Usedom.
            # Restrict this PARTIAL extension to the western mainland approach;
            # this cutoff is a retained-uncertainty boundary, not the Peene itself.
            mask[:,4404:]=False
            coremask=bmp==0x567452
            near=coremask.copy()
            for _ in range(20):
                spread=np.roll(near,1,0)|np.roll(near,-1,0)|np.roll(near,1,1)|np.roll(near,-1,1)
                near |= spread & mask
            mask &= near
        results[sector]=dict(parent=parent,cells=[[int(x),int(y)] for y,x in zip(*np.where(mask))],
                             pixels=int(mask.sum()),old_matrix=old_matrix.tolist(),new_matrix=new_matrix.tolist(),
                             historical_polygon=cfg['polygon'],buffer_px=margin,
                             method='Conservative intersection of two differently constrained source readings, not an accuracy certification or a complete frontier')
    dump('GEOMETRY_REVIEW.json',results)
    for sector,row in results.items():
        print(sector,row['pixels'],'cells; bounds', np.min(row['cells'],axis=0) if row['cells'] else None,np.max(row['cells'],axis=0) if row['cells'] else None)
        if len(row['cells'])<25:print(row['cells'])

def prepare():
    """Generate exact text patches and a raster candidate, never overwrite history."""
    b=load('BASELINE.json');review=load('GEOMETRY_REVIEW.json')
    assert economy.runtime_hashes()==b['hashes'], 'Workspace changed after capture'
    before=core.packed(ROOT/b['bitmap_backup']);after=before.copy()
    assert NEW_RGB not in b['inventory']['geometry'] and not np.any(before==int(NEW_RGB[1:],16))
    changes=[]
    for sector,destination,target,sid,source in [('PEENE','x567452','SWE','STATE_POMERANIA','PRU'),('NETZE',NEW_RGB,'PRU','STATE_POSEN','PLC')]:
        row=review[sector]
        assert row['pixels']>0
        for x,y in row['cells']:
            assert before[y,x]==int(row['parent'][1:],16)
            after[y,x]=int(destination[1:],16)
            changes.append(dict(Sector=sector,X=x,Y=y,RGB_before=row['parent'],RGB_after=destination,State_ID=sid,Owner_before=source,Owner_after=target,
                                Source='Mayer/Lotter 1763; conservative western mainland core' if sector=='PEENE' else 'Guessefeld/Homann 1775; Bromberg interior, Homann inset for corroboration only'))
    arrays=np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)
    Image.fromarray(arrays).save(OUT/'provinces_candidate.png')
    assert len(core.components(after==int(NEW_RGB[1:],16)))==1
    assert len(core.components(after==0xFCC7B7))==1
    assert len(core.components(after==0xE1A03A))==1
    assert len(core.components(after==0x567452))==1
    files={}; originals={}; allocations=[]
    def read(rel):
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');originals[rel]=raw;return raw
    rel='common/history/states/00_states.txt';raw=read(rel)
    s=core.state(raw,'STATE_POSEN')
    assert not any(n.one('country')=='c:PRU' for n in s.children('create_state'))
    raw=core.edits(raw,[(s.end-1,s.end-1,'\n\t\tcreate_state = { country = c:PRU owned_provinces = { '+NEW_RGB+' } }\n\t')])
    files[rel]=raw
    rel='map_data/state_regions/02_east_europe.txt';raw=read(rel)
    s=next(n for n in core.cw.parse(raw) if n.key=='STATE_POSEN')
    p=s.children('provinces')[0]
    rgb_list=core.values(s,'provinces')
    assert 'xFCC7B7' in rgb_list and NEW_RGB not in rgb_list
    ops=[(p.start,p.end,'provinces = { '+' '.join('"'+r+'"' for r in rgb_list+[NEW_RGB])+' }')]
    refs=[]
    for field in ['city','port','farm','mine','wood']:
        n=s.children(field)
        if n and core.cw.scalar(n[0].value)=='xFCC7B7':
            assert field=='farm', 'Unexpected province locator dependency'
            assert after[767,4507]==int(NEW_RGB[1:],16), 'Do not move a named locator to force the attribution'
            ops.append((n[0].start,n[0].end,field+' = "'+NEW_RGB+'"'))
            refs.append(dict(state='STATE_POSEN',field=field,before='xFCC7B7',after=NEW_RGB,pixel=[4507,767],locator_moved=False))
    if 'xFCC7B7' in core.values(s,'prime_land'):
        n=s.children('prime_land')[0];ps=core.values(s,'prime_land')
        ops.append((n.start,n.end,'prime_land = { '+' '.join('"'+r+'"' for r in ps+[NEW_RGB])+' }'))
        refs.append(dict(state='STATE_POSEN',field='prime_land',before=ps,after=ps+[NEW_RGB]))
    files[rel]=core.edits(raw,ops)
    rel='map_data/province_terrains.txt';raw=read(rel)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    assert NEW_RGB.upper() not in terrain
    files[rel]=raw.rstrip('\r\n')+'\n'+NEW_RGB+'="'+terrain['XFCC7B7']+'"\n'
    # Exact integer redistribution within each source state-owner subdivision.
    # Area is an explicit gameplay allocation, NOT an inferred historical census.
    weights={}
    for sid,source,target,count in [('STATE_POMERANIA','PRU','SWE',review['PEENE']['pixels']),('STATE_POSEN','PLC','PRU',review['NETZE']['pixels'])]:
        area=sum(int((before==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==[sid,source])
        weights[sid,source]=(target,{source:area-count,target:count})
    for path in economy.effective(ROOT,core.qa.GAME,'common/history/pops'):
        raw=path.read_text(encoding='utf-8-sig');ops=[];moved=[]
        for (sid,source),(target,w) in weights.items():
            try:n=core.region(raw,sid,source)
            except StopIteration:continue
            for pop in n.children('create_pop'):
                size=pop.children('size')[0];counts=core.allocate(int(size.value),w)
                ops.append((size.start,size.end,'size = '+str(counts[source])))
                if counts[target]:
                    fragment=core.edits(raw[pop.start:pop.end],[(size.start-pop.start,size.end-pop.start,'size = '+str(counts[target]))])
                    moved.append((sid,target,fragment))
                allocations.append(dict(state=sid,source=source,target=target,culture=core.cw.scalar(pop.one('culture')),religion=core.cw.scalar(pop.one('religion','DEFAULT')),before=int(size.value),after=counts,weights=w))
        if not ops:continue
        updated=core.edits(raw,ops)
        for sid,target,fragment in moved:updated=core.append(updated,sid,target,fragment)
        assert path.is_relative_to(ROOT), 'Do not copy a vanilla history implicitly'
        rel=path.relative_to(ROOT).as_posix();originals[rel]=raw;files[rel]=updated
    # All existing starting levels round to their source subdivision. Verify this
    # rather than silently deleting or manufacturing infrastructure in the new one.
    for sid,tag,node,path in economy.declarations():
        if (sid,tag) not in weights:continue
        target,w=weights[sid,tag]
        for v in core.cw.walk(node.children()):
            if v.key=='levels':assert core.allocate(int(v.value),w)[target]==0, 'Building redistribution requires explicit review'
    for text in files.values():core.cw.parse(text)
    dump('ORIGINAL_TEXT.json',originals)
    dump('EXPECTED_TEXT.json',files)
    dump('PLAN.json',dict(changes=changes,allocations=allocations,weights={s+'|'+t:w for (s,t),w in weights.items()},files=sorted(files),
         region_reference_changes=refs,new_provinces=[dict(rgb=NEW_RGB,parent_rgb='xFCC7B7',state='STATE_POSEN',owner='PRU',terrain=terrain['XFCC7B7'])],
         candidate_sha256=core.sha(OUT/'provinces_candidate.png'),status='MAP-2M_PARTIAL'))
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(changes[0]));writer.writeheader();writer.writerows(changes)
    old_out=core.OUT
    try:core.OUT=OUT;core.emit(files,'HISTORY.patch')
    finally:core.OUT=old_out
    dump('REGISTRY_MIGRATION.json',dict(replaced_regions=[],previous=[],updated=[],new_members=[],new_provinces=[NEW_RGB],
         reason='Peene extends an existing registered Swedish RGB by six cells; all registry rows are unchanged. New Posen province is NOT de-jure imperial.',
         ownership_changes=changes,region_reference_changes=refs))
    print('Prepared',len(changes),'actual ownership cells;',len(files),'text files; one new RGB',NEW_RGB)
    previews(before,after,changes)

def previews(before,after,changes):
    b=load('BASELINE.json');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    for sector,box in SECTORS.items():
        x0,y0,x1,y1=box;panels=[]
        for title,bmp in [('AVANT',before),('APRES',after)]:
            local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),235,dtype=np.uint8)
            for value in np.unique(local):
                rgb='x'+format(int(value),'06X');tag='PRU' if rgb==NEW_RGB else owners.get(rgb)
                arr[local==value]={'PRU':(145,190,225),'SWE':(235,205,65),'PLC':(220,160,160)}.get(tag,(235,235,235))
            edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];arr[edge]=80
            im=Image.fromarray(arr).resize(((x1-x0)*10,(y1-y0)*10),Image.Resampling.NEAREST)
            canvas=Image.new('RGB',(im.width,im.height+85),'white');canvas.paste(im,(0,40));d=ImageDraw.Draw(canvas)
            d.text((10,10),sector+' / '+title+' / PARTIEL - ne certifie pas toute la frontiere',fill='black')
            for r in changes:
                if r['Sector']==sector:
                    x=(r['X']-x0)*10;y=(r['Y']-y0)*10+40
                    d.rectangle((x,y,x+9,y+9),outline='red',width=1)
            if sector=='NETZE':
                x=(4507.717-x0)*10;y=(767.086-y0)*10+40
                d.ellipse((x-4,y-4,x+4,y+4),outline='black',width=2);d.text((x+6,y),'Bromberg : locator conserve',fill='black')
            d.text((10,im.height+50),'Bleu : Prusse / Jaune : Suede / Rose : Pologne / Rouge : cellules corrigees',fill='black')
            panels.append(canvas)
        output=Image.new('RGB',(panels[0].width*2,panels[0].height),'white')
        output.paste(panels[0]);output.paste(panels[1],(panels[0].width,0));output.save(OUT/(sector+'_BEFORE_AFTER.png'))

def install_raster():
    """Install only the exact reviewed map-data candidate, no generated AI image."""
    b=load('BASELINE.json');plan=load('PLAN.json')
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert core.sha(OUT/'provinces_candidate.png')==plan['candidate_sha256']
    for rel,text in load('EXPECTED_TEXT.json').items():
        assert (ROOT/rel).read_text(encoding='utf-8-sig')==text, 'Install the reviewed text patch first: '+rel
    core.shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Installed exact candidate:',plan['candidate_sha256'])

def tidy_proposal():
    """Remove whitespace-only inserted lines, never clean unrelated dirty work."""
    original=load('ORIGINAL_TEXT.json');expected=load('EXPECTED_TEXT.json');files={}
    for rel,text in expected.items():
        before=original[rel].splitlines(keepends=True);lines=text.splitlines(keepends=True)
        matcher=difflib.SequenceMatcher(a=before,b=lines,autojunk=False)
        for kind,a0,a1,b0,b1 in matcher.get_opcodes():
            if kind in ['insert','replace']:
                for i in range(b0,b1):
                    if not lines[i].strip():lines[i]='\n'
        files[rel]=''.join(lines)
    dump('EXPECTED_TEXT.json',files)
    old_out=core.OUT
    try:core.OUT=OUT;core.emit(files,'WHITESPACE.patch')
    finally:core.OUT=old_out
    print('Generated whitespace-only cleanup of inserted R2 lines; unrelated lines untouched.')

def expected_raster(before,changes):
    expected=before.copy();seen=set()
    for row in changes:
        x,y=row['X'],row['Y']
        if (x,y) in seen:raise ValueError('Repeated territorial cell')
        seen.add((x,y))
        if before[y,x]!=int(row['RGB_before'][1:],16):raise ValueError('Wrong source RGB')
        expected[y,x]=int(row['RGB_after'][1:],16)
    return expected

def validate():
    b=load('BASELINE.json');plan=load('PLAN.json');inv=core.qa.inventory();checks=[]
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png')
    def check(name,passed,detail=''):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('Exact reviewed raster and no outside cell edits',np.array_equal(after,expected_raster(before,plan['changes'])))
    check('91 actual RGB changes',int((before!=after).sum())==91)
    check('Installed reviewed bitmap hash',core.sha(ROOT/'map_data/provinces.png')==plan['candidate_sha256'])
    check('Original 341 Swedish cells never recoloured or removed',np.all(after[before==0x567452]==0x567452) and int((before==0x567452).sum())==341)
    check('Swedish core extended to 347 cells',int((after==0x567452).sum())==347)
    for rgb in ['xA04121','x41A021','x80A0A0','x999CEE']:
        value=int(rgb[1:],16)
        check('Frozen province footprint '+rgb,np.array_equal(before==value,after==value))
    check('Eastern Peene/Usedom approach untouched',np.array_equal(before[711:775,4404:4442],after[711:775,4404:4442]))
    for rgb in [NEW_RGB,'xFCC7B7','xE1A03A','x567452']:
        check('Single connected footprint '+rgb,len(core.components(after==int(rgb[1:],16)))==1)
    expected_owners=core.qa.counter(b['inventory']['owners'])
    expected_owners[(NEW_RGB,'STATE_POSEN','PRU')]+=1
    check('Only new ownership declaration is Bromberg PRU subdivision',core.qa.counter(inv['owners'])==expected_owners)
    expected_geo=dict(b['inventory']['geometry']);expected_geo[NEW_RGB]='STATE_POSEN'
    check('One new RGB in correct State_ID; all others retained',inv['geometry']==expected_geo)
    check('New colour absent from old bitmap',not np.any(before==int(NEW_RGB[1:],16)))
    check('New province exactly 85 cells',int((after==int(NEW_RGB[1:],16)).sum())==85)
    check('Bromberg farm locator remains fixed and now Prussian',after[767,4507]==int(NEW_RGB[1:],16))
    expected_states={tuple(s) for s in b['inventory']['states']}|{('STATE_POSEN','PRU')}
    check('Only one new region_state subdivision',set(map(tuple,inv['states']))==expected_states)
    check('Existing incorporation status unchanged',all(inv['state_types'].get(k)==v for k,v in b['inventory']['state_types'].items()))
    for field in ['pops','resolved_demographics','buildings','building_levels_written','units','countries','errors','duplicates']:
        check('Preserved full inventory: '+field,inv[field]==b['inventory'][field])
    check('835804980 people, no artificial population',sum(r['count'] for r in inv['pops'])==835804980)
    check('Inherited 44 RGB duplicates, 12 invalid references separately retained',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for row in plan['allocations']:
        religion='DEFAULT:'+row['culture'] if row['religion']=='DEFAULT' else row['religion']
        key=(row['state'],row['source'],row['culture'],religion)
        amount=row['after'].get(row['target'],0)
        regional[key]-=amount
        regional[(row['state'],row['target'],row['culture'],religion)]+=amount
    check('Exact deterministic per-culture and religion regional allocations',+regional==core.qa.counter(inv['regional_pop']))
    # All unspecified pop properties, including the explicit aristocrat type,
    # are copied verbatim; validate full population profiles excluding size.
    def profiles(text):
        counts=C.Counter()
        for s in core.cw.walk(core.cw.parse(text)):
            if not s.key.startswith('s:STATE_'):continue
            for rs in s.children():
                for p in rs.children('create_pop'):
                    profile=[core.qa.norm(n) for n in p.children() if n.key!='size']
                    counts[s.key,json.dumps(profile,sort_keys=True)]+=int(p.one('size'))
        return counts
    originals=load('ORIGINAL_TEXT.json');files=load('EXPECTED_TEXT.json')
    for rel,text in files.items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig')
        check('Exact reviewed text '+rel,actual==text)
        check('Parse modified file '+rel,bool(core.cw.parse(actual)))
        if '/pops/' in rel:check('All population attributes and totals per state '+rel,profiles(actual)==profiles(originals[rel]))
    hashes=economy.runtime_hashes();allowed=set(files)|{'map_data/provinces.png'}
    changed={p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}
    check('Only six authorized functional files changed',changed==allowed)
    check('Imperial registry rows unchanged; new Posen territory is not imperial',json.loads(core.active_registry_path().read_text())==b['registry'] and not any(r['rgb']==NEW_RGB for r in b['registry']))
    check('All earlier MAP2M evidence and baselines immutable',all(core.sha(ROOT/p)==digest for p,digest in b['earlier_proofs'].items()))
    current_totals=economy.totals(economy.declarations())
    check('Six Brandenburg arms levels preserved',current_totals['STATE_BRANDENBURG','PRU','building_arms_industry']==6)
    check('Recent Canton correction preserved',current_totals['STATE_GUANGDONG','CHI','building_port']==5 and current_totals['STATE_GUANGDONG','CHI','building_trade_center']==5 and not any(tag=='CHI' and sid!='STATE_GUANGDONG' and kind=='building_trade_center' and n for (sid,tag,kind),n in current_totals.items()))
    check('HEAD unchanged',head()==b['git_head'])
    check('Git index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    # Reuse existing source checks without allowing them to overwrite old reports.
    # A strict old bitmap equality/count of 341 must now fail by design.
    import validate_map2l_prussian_borders as legacy
    legacy_checks=[]
    old_base=json.loads((old.PREVIOUS/'BASELINE.json').read_text())
    def collect(name,value):legacy_checks.append(dict(name=name,passed=bool(value)))
    legacy.source_checks(collect,old.PREVIOUS,inv,old_base,json.loads((old.PREVIOUS/'ALIGNMENT.json').read_text()),
                         json.loads((old.PREVIOUS/'TRACING.json').read_text()),json.loads((old.PREVIOUS/'PLAN.json').read_text()))
    expected_obsolete={'Whole existing province; no manufactured frontier or new RGB','Northern Swedish core unique 341 cells','No other territorial region or historical lot changed'}
    check('Existing Prussian source validator: only expected obsolete assumptions fail',{r['name'] for r in legacy_checks if not r['passed']}==expected_obsolete)
    dump('LEGACY_SOURCE_CHECKS.json',dict(checks=legacy_checks,expected_obsolete=sorted(expected_obsolete),warning='Executed source-check function read-only; old snapshots and validation reports NOT rewritten. R2 differential checks replace only superseded assumptions.'))
    rows=[];prior=core.qa.counter(b['inventory']['regional_pop']);now=core.qa.counter(inv['regional_pop'])
    for k in sorted(prior.keys()|now.keys()):
        if k[0] in ['STATE_POMERANIA','STATE_POSEN']:
            rows.append(dict(State_ID=k[0],Owner=k[1],Culture=k[2],Religion=k[3],Before=prior[k],After=now[k],Difference=now[k]-prior[k]))
    with (OUT/'POPULATION_VALIDATION.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result=dict(status='MAP-2M_PARTIAL',static_validation='PASS' if all(c['passed'] for c in checks) else 'FAIL',
                passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                sectors={s:dict(applied_cells=sum(r['Sector']==s for r in plan['changes']),historical_geometry_complete=False) for s in SECTORS},
                new_RGBs=[NEW_RGB],world_population=835804980,inherited_duplicates=44,inherited_invalid_references=12,
                functional_files=sorted(changed),engine_tested=False,runtime_status='PENDING_USER_NEW_GAME_AND_ONE_MONTH',
                prior_gui='PASS_RUNTIME_USER_VALIDATED per R2 instructions; not an automated engine test',
                colgrep=dict(calls=1,success=False,error='Access denied resolving indexed repository; no local 2B execution confirmed; exact-search fallback'))
    dump('VALIDATION.json',result)
    previews(before,after,plan['changes'])
    print(result['status'],result['static_validation'],result['passed'],'/',result['total'])
    for c in checks:
        if not c['passed']:print('FAIL',c['name'],c['detail'])
    assert result['static_validation']=='PASS'

if __name__=='__main__':
    {'capture':capture,'diagnostics':diagnostics,'physical':physical,'geometry':geometry,'prepare':prepare,'install-raster':install_raster,'validate':validate,'tidy-proposal':tidy_proposal}[sys.argv[1]]()
