"""Scoped, reproducible Poel reconstruction. No game writes in diagnostic stage."""
import collections as C
import json,math,re,sys,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import map2n_work as audit
ROOT=audit.ROOT; OUT=audit.OUT; prior=audit.prior; core=audit.core
GAME=core.qa.GAME
BOX=(4350,731,4365,745)
SWE='xEDB100';LUB='xEDB101';SEA='x807D99'
Image.MAX_IMAGE_PIXELS=None

def dump(name,obj):audit.dump(name,obj)
def load(name):return audit.load(name)
def polygon_contains(poly,point):
    x,y=point;yes=False
    for (a,b),(c,d) in zip(poly,np.roll(poly,-1,axis=0)):
        if (b>y)!=(d>y) and x<(c-a)*(y-b)/(d-b)+a:yes=not yes
    return yes

def diagnose():
    assert prior.economy.runtime_hashes()==load('BASELINE.json')['hashes']
    bmp,water,_,_=prior.seven.p.physical_masks()
    data=json.loads((OUT.parent/'MAP2M/R3/EVIDENCE/NE_COASTLINE.geojson').read_text())
    ring=np.array(data['features'][1283]['geometry']['coordinates'])
    assert np.allclose(ring.min(axis=0),[11.375662,53.961127]) and np.allclose(ring.max(axis=0),[11.497895,54.030951])
    model=prior.seven.w.load('TRANSFORMATIONS.json')['selected_native']
    points=prior.seven.r.forward(model,ring)
    x0,y0,x1,y1=BOX
    cells=[[x,y] for y in range(y0,y1) for x in range(x0,x1) if polygon_contains(points,(x+.5,y+.5))]
    # One complete native-cell sea buffer prevents both edge and diagonal bridges.
    around=sorted({(x+dx,y+dy) for x,y in cells for dx in [-1,0,1] for dy in [-1,0,1]}-{tuple(p) for p in cells})
    edits=[dict(X=x,Y=y,RGB_before='x'+format(int(bmp[y,x]),'06X'),Kind='ISLAND') for x,y in cells]
    edits += [dict(X=x,Y=y,RGB_before='x'+format(int(bmp[y,x]),'06X'),Kind='STRAIT') for x,y in around if not water[y,x]]
    owners={r['key'][0]:r['key'][1:] for r in load('BASELINE.json')['inventory']['owners']}
    im=prior.old.panel(bmp,BOX,'POEL : reconstruction proposee, cote moderne generalisee',owners,scale=36)
    draw=ImageDraw.Draw(im)
    for r in edits:
        x=(r['X']-x0)*36;y=(r['Y']-y0)*36+42
        draw.rectangle((x+2,y+2,x+33,y+33),fill='#e1b52e' if r['Kind']=='ISLAND' else '#3186c4')
    draw.line([((x-x0)*36,(y-y0)*36+42) for x,y in points],fill='black',width=2)
    draw.text((8,im.height-23),'Or : Poel ; bleu : detroit ; trait noir : cote source',font=prior.old.font(13),fill='black')
    im.save(OUT/'POEL_RECONSTRUCTION_PROPOSAL.png')
    dump('POEL_DIAGNOSTIC.json',dict(source='MAP2M/R3/EVIDENCE/NE_COASTLINE.geojson feature1283',
        source_sha256=core.sha(OUT.parent/'MAP2M/R3/EVIDENCE/NE_COASTLINE.geojson'),geographic_ring=ring.tolist(),
        projected_ring=points.tolist(),island_cells=cells,candidate_edits=edits,
        limitation='Generalized modern coastline and reused coarse model; not a measured 1776 cadastral boundary. One-cell strait deliberately exaggerated for robust topology.',
        user_decision='Rebuild island and strait; place Swedish Poel in STATE_POMERANIA'))
    print('island',cells,'coastal edits',edits)

def prepare():
    b=load('BASELINE.json');assert prior.economy.runtime_hashes()==b['hashes']
    assert not (OUT/'ISLAND_PLAN.json').exists(),'Do not repeat an installed allocation'
    before=core.packed(ROOT/'map_data/provinces.png');after=before.copy();d=load('POEL_DIAGNOSTIC.json')
    assert not np.isin(before,[int(SWE[1:],16),int(LUB[1:],16)]).any()
    cells=d['island_cells'];assert cells==[[4355,736],[4356,736],[4355,737],[4356,737]]
    lub=[4355,737] # Southwestern hospital dependencies, a one-cell political abstraction.
    changes=[]
    for row in d['candidate_edits']:
        x,y=row['X'],row['Y'];target=(LUB if [x,y]==lub else SWE) if row['Kind']=='ISLAND' else SEA
        after[y,x]=int(target[1:],16)
        changes.append(dict(**row,RGB_after=target,State_before='STATE_MECKLENBURG' if row['RGB_before']!='x807D99' else 'SEA',
            Owner_before='MEC' if row['RGB_before']!='x807D99' else 'NONE',State_after='STATE_POMERANIA' if row['Kind']=='ISLAND' else 'SEA',
            Owner_after=('LUB' if [x,y]==lub else 'SWE') if row['Kind']=='ISLAND' else 'NONE',Applied=True))
    # Every source terrestrial cell is MEC, no other sovereign is displaced.
    own={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    assert all(own.get(r['RGB_before'])==['STATE_MECKLENBURG','MEC'] for r in changes if r['Owner_before']=='MEC')
    assert len(core.components(np.isin(after,[int(SWE[1:],16),int(LUB[1:],16)])))==1
    rawfiles={};files={}
    for rel in ['common/history/states/00_states.txt','map_data/state_regions/00_west_europe.txt',
                'common/history/pops/00_west_europe.txt','map_data/province_terrains.txt',core.active_registry_path().relative_to(ROOT).as_posix()]:
        rawfiles[rel]=(ROOT/rel).read_text(encoding='utf-8-sig')
    rel='map_data/state_regions/00_west_europe.txt';raw=rawfiles[rel]
    node=next(n for n in core.cw.parse(raw) if n.key=='STATE_POMERANIA');field=node.children('provinces')[0]
    files[rel]=core.edits(raw,[(field.end-1,field.end-1,' "'+SWE+'" "'+LUB+'" ')])
    rel='common/history/states/00_states.txt';raw=rawfiles[rel];node=core.state(raw,'STATE_POMERANIA')
    s=next(n for n in node.children('create_state') if n.one('country')=='c:SWE');field=s.children('owned_provinces')[0]
    files[rel]=core.edits(raw,[(field.end-1,field.end-1,' '+SWE+' '),(node.end-1,node.end-1,'\ncreate_state = { country = c:LUB owned_provinces = { '+LUB+' } }\n')])
    # Reallocate from the complete MEC subdivision, never create inhabitants on new land.
    # Post-reconstruction area weights include the erased coast; buildings stay intact.
    source_area=sum(int((before==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_MECKLENBURG','MEC'])
    lost=sum(r['Owner_before']=='MEC' for r in changes);weights={'MEC':source_area-lost,'SWE':3,'LUB':1}
    rel='common/history/pops/00_west_europe.txt';raw=rawfiles[rel];region=core.region(raw,'STATE_MECKLENBURG','MEC');ops=[];moved=C.defaultdict(list);alloc=[]
    for pop in region.children('create_pop'):
        size=pop.children('size')[0];counts=core.allocate(int(size.value),weights)
        ops.append((size.start,size.end,'size = '+str(counts['MEC'])))
        for tag in ['SWE','LUB']:
            if counts[tag]:moved[tag].append(core.edits(raw[pop.start:pop.end],[(size.start-pop.start,size.end-pop.start,'size = '+str(counts[tag]))]))
        alloc.append(dict(culture=pop.one('culture'),religion=pop.one('religion','DEFAULT'),before=int(size.value),after=counts))
    raw=core.edits(raw,ops)
    for tag,fragments in moved.items():raw=core.append(raw,'STATE_POMERANIA',tag,'\n'.join(fragments))
    files[rel]=raw
    files['map_data/province_terrains.txt']=rawfiles['map_data/province_terrains.txt']+'\n'+SWE+'="plains"\n'+LUB+'="plains"\n'
    rel=core.active_registry_path().relative_to(ROOT).as_posix();oldledger=json.loads(rawfiles[rel]);ledger=sorted(oldledger+[
        dict(rgb=rgb,state='STATE_POMERANIA',beneficiary=tag,basis='MAP2N Poel: island reconstruction; Pomeranian technical grouping explicitly requested; generalized coast and hospital enclave, see REPORT.md.') for rgb,tag in [(SWE,'SWE'),(LUB,'LUB')]],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[rel]=json.dumps(ledger,ensure_ascii=False,indent=2)
    regions=['STATE_MECKLENBURG','STATE_POMERANIA'];previous=[r for r in oldledger if r['state'] in regions];updated=[r for r in ledger if r['state'] in regions]
    a=np.isin(before,[int(r['rgb'][1:],16) for r in oldledger]);z=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
    assignments=[dict(rgb=rgb,parent_rgb='xD8F441',state='STATE_POMERANIA',owner=tag,previous_owner='MEC',pixels=sum(int(after[y,x])==int(rgb[1:],16) for x,y in cells),cells=[[x,y] for x,y in cells if after[y,x]==int(rgb[1:],16)]) for rgb,tag in [(SWE,'SWE'),(LUB,'LUB')]]
    retained=dict(rgb='xD8F441',parent_rgb='xD8F441',state='STATE_MECKLENBURG',owner='MEC',previous_owner='MEC',pixels=int((after==0xD8F441).sum()))
    migration=dict(replaced_regions=regions,previous=previous,updated=updated,new_members=[],free_cities=[],new_provinces=assignments,
        region_reference_changes=[],extent_added_cells=[[int(x),int(y)] for y,x in zip(*np.where(z&~a))],
        extent_removed_cells=[[int(x),int(y)] for y,x in zip(*np.where(a&~z))],
        physical_coastline_change=True,technical_state_grouping='Poel in STATE_POMERANIA, explicitly requested by player')
    dump('REGISTRY_MIGRATION.json',migration);dump('GEOMETRY.json',dict(parents=['xD8F441'],assignments=[retained]+assignments,new_provinces=assignments,changes=changes))
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    dump('ISLAND_ORIGINAL_TEXT.json',rawfiles);dump('ISLAND_EXPECTED_TEXT.json',files)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'ISLAND_HISTORY.patch')
    finally:core.OUT=oldout
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'island_provinces_candidate.png')
    dump('ISLAND_PLAN.json',dict(changes=changes,weights=weights,allocations=alloc,new_RGBs=[SWE,LUB],text_files=list(files),
        bitmap_sha256=core.sha(OUT/'island_provinces_candidate.png'),runtime_base=b['hashes'],registry_before=oldledger,
        registry_tool_before=core.sha(ROOT/'tools/map2l_registry.py'),
        limitations=['Four-cell island; one-cell southwestern Lubeck hospital abstraction, not cadastral precision.','One-cell strait intentionally widened to preserve island topology.','Wismar and Neukloster still not installed.']))
    audit.csvout('TERRITORIAL_CHANGES.csv',changes)
    print('Prepared',len(changes),'cells; allocation',alloc)

def relief():
    assert not (OUT/'RELIEF_PLAN.json').exists()
    plan=load('ISLAND_PLAN.json');d=load('POEL_DIAGNOSTIC.json');height=np.array(Image.open(GAME/'map_data/heightmap.png'))
    packed=np.array(Image.open(GAME/'map_data/packed_heightmap.png'));ind=np.array(Image.open(GAME/'map_data/indirection_heightmap.png'))
    assert height.shape==(7232,16384) and height.dtype==np.uint16 and packed.shape==(8065,3315)
    # Established actual vanilla tile layout; compare orientation against source before writing.
    tiles={}
    for tx,ty in [(136,22),(136,23)]:
        r,g,step,level=map(int,ind[ty,tx]);n=64//step+1;offset=[0,6695,7569,7662,7680][level]
        px=r*n;py=packed.shape[0]-offset-(g+1)*n
        assert np.sum(np.all(ind==ind[ty,tx],axis=2))==1,'Never edit a shared packed tile'
        # Native PNG top row is one full-height sample above ty*64:
        # independently checked versus +/-2 shifts in both axes on both tiles.
        original=packed[py:py+n,px:px+n].copy();reference=height[ty*64-1:ty*64+64:step,tx*64:tx*64+65:step]
        error=float(np.abs(original.astype(float)-reference).mean());assert error<1,(tx,ty,error)
        tiles[tx,ty]=dict(tile=[tx,ty],packed_origin=[px,py],source_origin=[tx*64,ty*64-1],tile_size=n,step=step,level=level,native_source_mean_difference=error)
    # Actual mod sea threshold: 65535 * WATERLEVEL(1.74)/WORLD_EXTENTS_Y(24).
    defines=(ROOT/'common/defines/00_defines.txt').read_text();assert re.search(r'WATERLEVEL\s*=\s*1\.74',defines) and re.search(r'WORLD_EXTENTS_Y\s*=\s*24\b',defines)
    threshold=65535*1.74/24;island={tuple(p) for p in d['island_cells']};moat={(x+dx,y+dy) for x,y in island for dx in [-1,0,1] for dy in [-1,0,1]}-island
    edits=[];packed_edits={}
    for x,y in sorted(island|moat):
        value=5400 if (x,y) in island else 4200
        for hy in [2*y,2*y+1]:
            for hx in [2*x,2*x+1]:
                edits.append(dict(X=hx,Y=hy,Before=int(height[hy,hx]),After=value));height[hy,hx]=value
        for tile in tiles.values():
            tx,ty=tile['tile'];step=tile['step'];n=tile['tile_size'];px,py=tile['packed_origin']
            # Tile borders are duplicated. Update both copies if a changed
            # full-height coordinate lies on their common edge.
            for hy in [2*y,2*y+1]:
                for hx in [2*x,2*x+1]:
                    dx,dy=hx-tx*64,hy-(ty*64-1)
                    if 0<=dx<=64 and 0<=dy<=64 and dx%step==0 and dy%step==0:
                        u,v=px+dx//step,py+dy//step
                        packed_edits.setdefault((u,v),dict(X=u,Y=v,Before=int(packed[v,u]),After=value))
                        packed[v,u]=value
    Image.fromarray(height).save(OUT/'heightmap_candidate.png');Image.fromarray(packed).save(OUT/'packed_heightmap_candidate.png')
    dump('RELIEF_PLAN.json',dict(tiles=list(tiles.values()),sea_threshold_16bit=threshold,land_height=5400,sea_height=4200,
        samples=edits,packed_samples=list(packed_edits.values()),island_cells=[list(p) for p in sorted(island)],moat_cells=[list(p) for p in sorted(moat)],
        source_hashes={n:core.sha(GAME/'map_data'/n) for n in ['heightmap.png','packed_heightmap.png','heightmap.heightmap','indirection_heightmap.png']},
        generated_hashes={n:core.sha(OUT/(n.replace('.png','_candidate.png'))) for n in ['heightmap.png','packed_heightmap.png']},
        encoding='Vanilla metadata and unique tile pointers unchanged; two local tiles patched including their shared border. Existing orientation checked against full height source.',
        limitation='LOD1 has one elevation sample per province pixel; coastline silhouette is necessarily coarse. Native material masks and cached nodes are unchanged; engine refresh must be verified.'))
    print('Relief ready:',len(edits),'source samples;',len(packed_edits),'packed samples; native comparisons',list(tiles.values()))

def install():
    b=load('BASELINE.json');plan=load('ISLAND_PLAN.json');h=load('RELIEF_PLAN.json');current=prior.economy.runtime_hashes()
    for rel,text in load('ISLAND_EXPECTED_TEXT.json').items():assert (ROOT/rel).read_text(encoding='utf-8-sig').rstrip('\r\n')==text.rstrip('\r\n'),rel
    assert {p for p in current.keys()|b['hashes'].keys() if current.get(p)!=b['hashes'].get(p)}==set(plan['text_files'])&(current.keys()|b['hashes'].keys())
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert core.sha(OUT/'island_provinces_candidate.png')==plan['bitmap_sha256']
    for n,sha in h['source_hashes'].items():assert core.sha(GAME/'map_data'/n)==sha
    for n,sha in h['generated_hashes'].items():
        target=ROOT/'map_data'/n;assert not target.exists(),'Do not overwrite collaborator relief'
        assert core.sha(OUT/n.replace('.png','_candidate.png'))==sha
    shutil.copyfile(OUT/'island_provinces_candidate.png',ROOT/'map_data/provinces.png')
    for n in h['generated_hashes']:shutil.copyfile(OUT/n.replace('.png','_candidate.png'),ROOT/'map_data'/n)
    print('Installed scoped bitmap and both coherent heightmaps; native indirection unchanged')

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('ISLAND_IMPERIAL_EXPECTED.json',files)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'ISLAND_IMPERIAL.patch')
    finally:core.OUT=oldout

def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
    import prototype_map2k_main_map as main
    main.MOD=ROOT;main.PACKAGE=OUT/'MAIN_MAP';main.build_and_test()

def rivers():
    target=ROOT/'map_data/rivers.png';assert not target.exists(),'Preserve any collaborator river override'
    source=GAME/'map_data/rivers.png';im=Image.open(source);assert im.mode=='P';a=np.array(im);rows=[]
    for r in load('ISLAND_PLAN.json')['changes']:
        x,y=r['X'],r['Y'];value=255 if r['Kind']=='ISLAND' else 254
        assert a[y,x] in [254,255],'Do not erase a river feature'
        if a[y,x]!=value:rows.append(dict(X=x,Y=y,Before=int(a[y,x]),After=value));a[y,x]=value
    result=Image.fromarray(a);result.putpalette(im.getpalette());result.save(target)
    dump('RIVER_PLAN.json',dict(source_sha256=core.sha(source),changes=rows,output_sha256=core.sha(target),
        basis='Existing native indexed palette:254 sea gray;255 blank land white. No river feature erased.'))

def compare_maps():
    assert not (OUT/'COMPLETION/PLAN.json').exists(),'Use map2n_completion.py previews for the completed lot'
    before=core.packed(OUT.parent/'MAP2M/R9/provinces_candidate.png');after=core.packed(ROOT/'map_data/provinces.png')
    b=load('BASELINE.json');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};owners.update({SWE:['STATE_POMERANIA','SWE'],LUB:['STATE_POMERANIA','LUB']})
    panels=[prior.old.panel(v,BOX,title,owners,scale=34) for v,title in [(before,'AVANT : littoral natif'),(after,'APRES : Poel et detroit reconstruits')]]
    for im,v in zip(panels,[before,after]):
        d=ImageDraw.Draw(im)
        for y in range(BOX[1],BOX[3]):
            for x in range(BOX[0],BOX[2]):
                if v[y,x] in [int(SWE[1:],16),int(LUB[1:],16)]:
                    px=(x-BOX[0])*34;py=(y-BOX[1])*34+42
                    d.rectangle((px+1,py+1,px+32,py+32),fill='#e1b52e' if v[y,x]==int(SWE[1:],16) else '#c2715c')
        d.rectangle((0,im.height-27,im.width,im.height),fill='white');d.text((6,im.height-23),'Or : Suede ; brun : Lubeck ; gris clair : mer',font=prior.old.font(12),fill='black')
    out=Image.new('RGB',(panels[0].width*2,panels[0].height+45),'white')
    for i,im in enumerate(panels):out.paste(im,(i*im.width,0))
    ImageDraw.Draw(out).text((8,out.height-34),'Poel : STATE_POMERANIA. Littoral generalise, pas une restitution cadastrale.',font=prior.old.font(17),fill='black')
    out.save(OUT/'POEL_BEFORE_AFTER.png')
    # Keep the other sector deliverables truthful: their sovereign assignments
    # remain uncorrected, but Poel's actual local coastline must be visible.
    for name,box in [('WISMAR',(4349,733,4365,746)),('NEUKLOSTER',(4354,735,4370,748))]:
        panels=[prior.old.panel(v,box,title,owners,scale=28) for v,title in [(before,'AVANT MAP2N'),(after,'APRES POEL ; '+name+' non termine')]]
        result=Image.new('RGB',(panels[0].width*2,panels[0].height+45),'white')
        for i,im in enumerate(panels):result.paste(im,(i*im.width,0))
        ImageDraw.Draw(result).text((8,result.height-33),'Aucune reattribution de '+name+' installee ; cote de Poel modifiee seulement.',font=prior.old.font(14),fill='black')
        result.save(OUT/(name+'_BEFORE_AFTER.png'))

def validate():
    assert not (OUT/'COMPLETION/PLAN.json').exists(),'Preserve Poel-stage evidence; use map2n_completion.py validate'
    b=load('BASELINE.json');plan=load('ISLAND_PLAN.json');h=load('RELIEF_PLAN.json');rp=load('RIVER_PLAN.json');inv=core.qa.inventory();checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    before=core.packed(OUT.parent/'MAP2M/R9/provinces_candidate.png');after=core.packed(ROOT/'map_data/provinces.png');wanted=before.copy()
    check('Accepted R9 backup matches immutable baseline',core.sha(OUT.parent/'MAP2M/R9/provinces_candidate.png')==b['bitmap_sha256'])
    for r in plan['changes']:wanted[r['Y'],r['X']]=int(r['RGB_after'][1:],16)
    check('Exact eight authorized province pixels only',np.array_equal(after,wanted) and int((before!=after).sum())==8)
    check('Exact installed province candidate',core.sha(ROOT/'map_data/provinces.png')==plan['bitmap_sha256'])
    island=np.isin(after,[int(SWE[1:],16),int(LUB[1:],16)])
    check('One four-cell island',int(island.sum())==4 and len(core.components(island))==1)
    sea_values=[int(v[1:],16) for v in re.findall(r'x[0-9a-fA-F]{6}',re.search(r'sea_starts\s*=\s*\{([^}]+)',(GAME/'map_data/default.map').read_text()).group(1))]
    check('Island separated on all eight-neighbour sides',all(int(after[y,x]) in sea_values for x,y in h['moat_cells']))
    check('Each new RGB one four-connected component',all(len(core.components(after==int(rgb[1:],16)))==1 for rgb in [SWE,LUB]))
    check('Three Swedish and one Lubeck cells',int((after==int(SWE[1:],16)).sum())==3 and int((after==int(LUB[1:],16)).sum())==1)
    check('Every old RGB retained, exactly two new',set(np.unique(after))-set(np.unique(before))=={int(SWE[1:],16),int(LUB[1:],16)} and not set(np.unique(before))-set(np.unique(after)))
    check('Peene and entire eastern approach unchanged',np.array_equal(before[:,4380:],after[:,4380:]))
    for rgb,n in [(0x567452,400),(0xE1A03A,290),(0xEDB010,85),(0xFCC7B7,142),(0x41A021,153)]:
        check('Exact protected footprint '+hex(rgb),np.array_equal(before==rgb,after==rgb) and int((after==rgb).sum())==n)
    expected=core.qa.counter(b['inventory']['owners']);expected[SWE,'STATE_POMERANIA','SWE']=1;expected[LUB,'STATE_POMERANIA','LUB']=1
    check('Only two explicit owner references added',expected==core.qa.counter(inv['owners']))
    geom=b['inventory']['geometry'].copy();geom.update({SWE:'STATE_POMERANIA',LUB:'STATE_POMERANIA'})
    check('Only explicit Pomeranian province definitions added',geom==inv['geometry'])
    check('Only Lubeck Pomeranian subdivision added',{tuple(s) for s in inv['states']}=={tuple(s) for s in b['inventory']['states']}|{('STATE_POMERANIA','LUB')})
    check('All existing incorporation flags preserved',all(inv['state_types'].get(k)==v for k,v in b['inventory']['state_types'].items()))
    for field in ['countries','pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:
        check('Global inventory preserved '+field,inv[field]==b['inventory'][field])
    check('World population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for r in plan['allocations']:
        religion=r['religion'] if r['religion']!='DEFAULT' else 'DEFAULT:'+r['culture']
        moved=r['after']['SWE']+r['after']['LUB'];regional['STATE_MECKLENBURG','MEC',r['culture'],religion]-=moved
        for tag in ['SWE','LUB']:regional['STATE_POMERANIA',tag,r['culture'],religion]+=r['after'][tag]
    check('Exact declared cross-state population allocation',+regional==core.qa.counter(inv['regional_pop']))
    for rel,text in load('ISLAND_EXPECTED_TEXT.json').items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig');check('Exact reviewed text '+rel,actual.rstrip('\r\n')==text.rstrip('\r\n'))
        if rel.endswith('.txt'):check('Parsed '+rel,bool(core.cw.parse(actual)))
    compiled=load('ISLAND_IMPERIAL_EXPECTED.json')
    for rel,text in compiled.items():
        check('Exact compiled imperial dependency '+rel,(ROOT/rel).read_text(encoding='utf-8-sig').rstrip('\r\n')==text.lstrip('\ufeff').rstrip('\r\n'))
    # Full-image equality outside the exact per-sample patches, not just matching counts.
    for name,rows in [('heightmap.png',h['samples']),('packed_heightmap.png',h['packed_samples'])]:
        source=np.array(Image.open(GAME/'map_data'/name));installed=np.array(Image.open(ROOT/'map_data'/name))
        for r in rows:check(name+' original sample '+str((r['X'],r['Y'])),int(source[r['Y'],r['X']])==r['Before']);source[r['Y'],r['X']]=r['After']
        check(name+' exact full-raster delta',np.array_equal(installed,source));check(name+' candidate hash',core.sha(ROOT/'map_data'/name)==h['generated_hashes'][name])
    height=np.array(Image.open(ROOT/'map_data/heightmap.png'));packed=np.array(Image.open(ROOT/'map_data/packed_heightmap.png'))
    check('Every island source sample above actual sea level',all(height[2*y:2*y+2,2*x:2*x+2].min()>h['sea_threshold_16bit'] for x,y in h['island_cells']))
    check('Every moat source sample below actual sea level',all(height[2*y:2*y+2,2*x:2*x+2].max()<h['sea_threshold_16bit'] for x,y in h['moat_cells']))
    for tile in h['tiles']:
        x0,y0=tile['source_origin'];px,py=tile['packed_origin'];n=tile['tile_size'];step=tile['step']
        for r in h['samples']:
            dx,dy=r['X']-x0,r['Y']-y0
            if 0<=dx<=64 and 0<=dy<=64 and dx%step==0 and dy%step==0:check('Packed/source coherence '+str((r['X'],r['Y'],tile['level'])),int(packed[py+dy//step,px+dx//step])==r['After'])
    for name,sha in h['source_hashes'].items():check('Vanilla source untouched '+name,core.sha(GAME/'map_data'/name)==sha)
    check('Native topology and indirection remain inherited',not (ROOT/'map_data/heightmap.heightmap').exists() and not (ROOT/'map_data/indirection_heightmap.png').exists())
    source=Image.open(GAME/'map_data/rivers.png');installed=Image.open(ROOT/'map_data/rivers.png');a=np.array(source)
    for r in rp['changes']:a[r['Y'],r['X']]=r['After']
    check('River indexed palette retained and exact five local deltas',installed.mode=='P' and installed.getpalette()==source.getpalette() and np.array_equal(a,np.array(installed)) and len(rp['changes'])==5)
    check('Native river source unchanged',core.sha(GAME/'map_data/rivers.png')==rp['source_sha256'])
    registry=json.loads(core.active_registry_path().read_text());check('Old registry entries intact plus two explicit rights',registry==sorted(plan['registry_before']+[r for r in registry if r['rgb'] in [SWE,LUB]],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])) and len(registry)==500)
    from map2l_registry import territorial_holder_overrides,additional_members,apply_territorial_migrations
    check('No Swedish bloc membership or broad holder exception','SWE' not in additional_members() and territorial_holder_overrides().get('SWE')=={'STATE_POMERANIA'})
    check('Exact MAP2N ledger migration',load('REGISTRY_MIGRATION.json')['updated']==[r for r in registry if r['state'] in ['STATE_MECKLENBURG','STATE_POMERANIA']])
    mask=np.array(Image.open(ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds').convert('RGBA'))[:,:,0]>0
    rights=np.isin(after,[int(r['rgb'][1:],16) for r in registry]);check('Actual imperial DDS matches all reviewed rights',np.array_equal(mask,rights[708:1220,4152:4664]))
    check('Offline helper shader compilation and16 map checks',all(r['passed'] for r in json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text())['checks']))
    active=core.active_registry_path().relative_to(ROOT).as_posix()
    check('Earlier R8 R9 artifacts untouched',all(core.sha(ROOT/p)==sha for p,sha in b['earlier_proofs'].items() if p!=active))
    changed={p for p,hsh in prior.economy.runtime_hashes().items() if b['hashes'].get(p)!=hsh}
    allowed=set(plan['text_files'])|set(compiled)|{'map_data/provinces.png','map_data/heightmap.png','map_data/packed_heightmap.png','map_data/rivers.png','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    check('No unrelated runtime file changed',changed<=allowed and set(b['hashes'])<=set(prior.economy.runtime_hashes()))
    check('Inherited44 duplicate RGB and12 badrefs only',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('HEAD and index untouched',prior.old.prior.r2.head()==b['git_head'] and core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    result=dict(status='MAP2N_POEL_READY_FOR_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'FAIL',overall_lot='MAP2N_PARTIAL_WISMAR_NEUKLOSTER_OPEN',
        passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,applied_cells=8,new_RGBs=[SWE,LUB],
        population_world=835804980,population_reallocated=sum(r['after']['SWE']+r['after']['LUB'] for r in plan['allocations']),
        runtime_tested=False,R8_R9_runtime_status='PASS_RUNTIME_USER_VALIDATED',functional_files_changed=sorted(changed))
    dump('VALIDATION.json',result)
    a=core.qa.counter(b['inventory']['regional_pop']);z=core.qa.counter(inv['regional_pop'])
    audit.csvout('POPULATION_VALIDATION.csv',[dict(State_ID=k[0],Owner=k[1],Culture=k[2],Religion=k[3],Before=a[k],After=z[k],Difference=z[k]-a[k]) for k in sorted(a.keys()|z.keys()) if k[0] in ['STATE_MECKLENBURG','STATE_POMERANIA']])
    dump('ISLAND_INSTALLED_MANIFEST.json',dict(functional_files={p:core.sha(ROOT/p) for p in sorted(changed)},registry_sha256=core.sha(core.active_registry_path()),runtime_tested=False))
    print(result['status'],result['passed'],'/',result['total']);print('Failures:',[r['name'] for r in checks if not r['passed']]);assert all(r['passed'] for r in checks)

if __name__=='__main__':globals()[sys.argv[1]]()
