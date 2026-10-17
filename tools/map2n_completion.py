"""Complete Swedish Mecklenburg after Poel; additive reference, no old baseline writes."""
import collections as C
import json,re,math,sys,zipfile,shutil,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import map2n_island as island
ROOT=island.ROOT;PARENT=island.OUT;OUT=PARENT/'COMPLETION';core=island.core;prior=island.prior
WISMAR='xEDB102';WISMAR_EAST='xEDB103';BENZ='xEDB104';NEUKLOSTER='xEDB105'
NEW=[WISMAR,WISMAR_EAST,BENZ,NEUKLOSTER]

def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def read(rel):return (ROOT/rel).read_text(encoding='utf-8-sig')

def capture():
    OUT.mkdir(exist_ok=True);assert not (OUT/'BASELINE.json').exists()
    b=island.load('BASELINE.json');current=prior.economy.runtime_hashes();ref=dict(b['hashes']);ref.update(island.load('ISLAND_INSTALLED_MANIFEST.json')['functional_files'])
    assert current==ref,'Unrelated workspace edit: inspect and preserve'
    dump('BASELINE.json',dict(hashes=current,inventory=core.qa.inventory(),registry=json.loads(core.active_registry_path().read_text()),
        island_manifest=island.load('ISLAND_INSTALLED_MANIFEST.json'),git_head=prior.old.prior.r2.head(),git_index=core.sha(ROOT/'.git/index'),
        registry_tool_sha256=core.sha(ROOT/'tools/map2l_registry.py'),bitmap_reference='docs/reports/map/MAP2N/island_provinces_candidate.png'))
    print('Frozen current Poel stage; original MAP2N baseline untouched')

def transforms(value):
    result=np.eye(3)
    for kind,args in re.findall(r'(matrix|translate)\(([^)]+)\)',value or ''):
        vals=list(map(float,re.split(r'[,\s]+',args.strip())))
        if kind=='matrix':a,b,c,d,e,f=vals;mat=np.array([[a,c,e],[b,d,f],[0,0,1.]])
        else:mat=np.array([[1,0,vals[0]],[0,1,vals[1] if len(vals)>1 else 0],[0,0,1.]])
        result=result@mat
    return result

def source_points():
    root=ET.parse(PARENT/'EVIDENCE/WISMAR_COMPARISON_2022.svg').getroot();circles={}
    def walk(node,parent):
        mat=parent@transforms(node.get('transform'))
        if node.tag.endswith('circle'):
            p=mat@np.array([float(node.get('cx')),float(node.get('cy')),1.]);circles[node.get('id')]=(p[:2]*960/264.58333).tolist()
        for child in node:walk(child,mat)
    walk(root,np.eye(3))
    # Identified black location symbols, not their text-label anchors.
    symbols=[('Schliemannstadt Neubukow',[696,25],'FIT'),('Warin',[756,772],'FIT'),('Neukloster',[720,577],'CHECK'),
             ('Zurow',[586,575],'CHECK'),('Dorf Mecklenburg',[308,642],'FIT'),('Lübow',[410,603],'CHECK'),('Hornstorf',[429,424],'CHECK')]
    z=zipfile.ZipFile(ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip')
    towns={r[1]:r for r in (line.split('\t') for line in z.read('cities1000.txt').decode().splitlines()) if r[8]=='DE' and 11.3<float(r[5])<11.85 and 53.75<float(r[4])<54.15}
    controls=[]
    for name,approx,role in symbols:
        ident,p=min(circles.items(),key=lambda item:np.linalg.norm(np.array(item[1])-approx));assert np.linalg.norm(np.array(p)-approx)<3,(name,ident,p,approx)
        r=towns[name];controls.append(dict(name=name,geonames_id=r[0],longitude=float(r[5]),latitude=float(r[4]),source=p,svg_symbol=ident,role=role))
    return controls

def trace():
    b=load('BASELINE.json');assert prior.economy.runtime_hashes()==b['hashes']
    rows=source_points();fit=[r for r in rows if r['role']=='FIT']
    transform=np.linalg.solve(np.array([[*r['source'],1] for r in fit]),np.array([[r['longitude'],r['latitude']] for r in fit]))
    model=prior.seven.w.load('TRANSFORMATIONS.json')['selected_native'];native=np.array(model['matrix'])
    for r in rows:
        geo=np.array([*r['source'],1])@transform;observed=prior.seven.r.forward(model,[[r['longitude'],r['latitude']]])[0];predicted=prior.seven.r.forward(model,[geo])[0]
        r.update(projected_game=predicted.tolist(),gazetteer_projected_game=observed.tolist(),source_alignment_error_native_px=float(np.linalg.norm(predicted-observed)))
    # This tests source-image georeferencing only, NOT the independent accuracy
    # of the game's frozen projection; do not call these certified city positions.
    inv=np.linalg.inv(np.vstack((transform.T,[0,0,1])))
    source=np.array(Image.open(PARENT/'EVIDENCE/WISMAR_COMPARISON_2022.png').convert('RGB')).astype(int)
    yellow=np.max(np.abs(source-np.array([255,224,170])),axis=2)<25
    bitmap=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};candidates=[];rejected=[]
    for y in range(738,746):
        for x in range(4352,4367):
            g=island.prior.seven.r.inverse(model,[[x+.5,y+.5]])[0]
            p=inv@np.array([*g,1.]);sx,sy=p[:2]
            # Supersample the footprint to avoid basing ownership on a town dot.
            samples=[]
            for dy in np.linspace(.05,.95,15):
                for dx in np.linspace(.05,.95,15):
                    geo=island.prior.seven.r.inverse(model,[[x+dx,y+dy]])[0];a=inv@np.array([*geo,1.]);u,v=map(math.floor,a[:2])
                    samples.append(bool(yellow[v,u]) if 0<=u<960 and 0<=v<960 else False)
            ratio=sum(samples)/len(samples);sector='NEUKLOSTER' if sx>580 else 'WISMAR'
            rgb='x'+format(int(bitmap[y,x]),'06X');owner=owners.get(rgb)
            if ratio>=.5:
                row=dict(Sector=sector,X=x,Y=y,RGB_before=rgb,Owner_before=owner,Source_X=float(sx),Source_Y=float(sy),Coverage=ratio)
                if owner==['STATE_MECKLENBURG','MEC']:candidates.append(row)
                else:rejected.append(dict(**row,Reason='Preserve installed coast: projection mismatch is not sufficient authority to reclaim mainland sea cells.'))
    print('controls',[(r['name'],r['role'],round(r['source_alignment_error_native_px'],3)) for r in rows]);print('candidates',candidates)
    dump('SOURCE_TRACING.json',dict(controls=rows,source_to_lonlat=transform.tolist(),candidates=candidates,rejected=rejected,
        source='WISMAR_COMPARISON_2022.png',source_sha256=core.sha(PARENT/'EVIDENCE/WISMAR_COMPARISON_2022.png'),
        geonames_sha256=core.sha(ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip'),
        threshold=.5,samples_per_cell=225,native_projection='Frozen R5, unchanged; independent native-city accuracy not certified',
        source_license='Fenn-O-maniC, CC BY-SA3.0; derived geographic tracing under same license; no original SVG in runtime assets'))
    scale=36;box=(4351,733,4368,747);im=prior.old.panel(bitmap,box,'WISMAR / NEUKLOSTER : empreintes candidates',owners,scale=scale);d=ImageDraw.Draw(im)
    for r in candidates:
        x=(r['X']-box[0])*scale;y=(r['Y']-box[1])*scale+42;d.rectangle((x+2,y+2,x+scale-3,y+scale-3),fill='#e6b636' if r['Sector']=='WISMAR' else '#8dbce0')
    d.rectangle((0,im.height-24,im.width,im.height),fill='white');d.text((5,im.height-22),'Jaune : Wismar ; bleu : Amt Neukloster ; aucun corridor ajoute',font=prior.old.font(13),fill='black');im.save(OUT/'MAINLAND_PROPOSAL.png')

def prepare():
    b=load('BASELINE.json');assert prior.economy.runtime_hashes()==b['hashes']
    assert not (OUT/'PLAN.json').exists(),'Never repeat a demographic transfer'
    tracing=load('SOURCE_TRACING.json');before=core.packed(ROOT/'map_data/provinces.png');after=before.copy()
    assert not np.isin(before,[int(v[1:],16) for v in NEW]).any()
    expected_w={(4357,739),(4359,739),(4355,740),(4356,740),(4357,740)}
    assert {(r['X'],r['Y']) for r in tracing['candidates'] if r['Sector']=='WISMAR'}==expected_w
    assert len(tracing['candidates'])==13
    changes=[]
    for row in tracing['candidates']:
        x,y=row['X'],row['Y'];parent=row['RGB_before'];assert row['Owner_before']==['STATE_MECKLENBURG','MEC']
        rgb=NEUKLOSTER if row['Sector']=='NEUKLOSTER' else (BENZ if (x,y)==(4359,739) else WISMAR if parent=='xE080A0' else WISMAR_EAST)
        assert before[y,x]==int(parent[1:],16);after[y,x]=int(rgb[1:],16)
        changes.append(dict(Sector='BENZ_DEPENDENCY' if rgb==BENZ else row['Sector'],X=x,Y=y,RGB_before=parent,RGB_after=rgb,
            State_ID='STATE_MECKLENBURG',Owner_before='MEC',Owner_after='SWE',Source_coverage=row['Coverage'],
            Source='Retained Wismar2022 comparative map, historical title corroborated1648/1720/1803; generalized native land cells',Applied=True))
    assignments=[]
    for rgb in NEW:
        rows=[r for r in changes if r['RGB_after']==rgb];parents={r['RGB_before'] for r in rows};assert len(parents)==1
        cells=[[r['X'],r['Y']] for r in rows];assert len(core.components(after==int(rgb[1:],16)))==1
        assignments.append(dict(rgb=rgb,parent_rgb=parents.pop(),state='STATE_MECKLENBURG',owner='SWE',previous_owner='MEC',pixels=len(cells),cells=cells))
    originals={};files={}
    for rel in ['common/history/states/00_states.txt','common/history/pops/00_west_europe.txt','map_data/state_regions/00_west_europe.txt','map_data/province_terrains.txt',core.active_registry_path().relative_to(ROOT).as_posix()]:originals[rel]=read(rel)
    rel='common/history/states/00_states.txt';raw=originals[rel];state=core.state(raw,'STATE_MECKLENBURG');assert not any(n.one('country')=='c:SWE' for n in state.children('create_state'))
    files[rel]=core.edits(raw,[(state.end-1,state.end-1,'\ncreate_state = { country = c:SWE owned_provinces = { '+' '.join(NEW)+' } }\n')])
    rel='map_data/state_regions/00_west_europe.txt';raw=originals[rel];state=next(n for n in core.cw.parse(raw) if n.key=='STATE_MECKLENBURG');field=state.children('provinces')[0];prime=state.children('prime_land')[0]
    files[rel]=core.edits(raw,[(field.end-1,field.end-1,' '+' '.join('"'+v+'"' for v in NEW)+' '),(prime.end-1,prime.end-1,' "'+WISMAR+'" ')])
    rel='common/history/pops/00_west_europe.txt';raw=originals[rel];region=core.region(raw,'STATE_MECKLENBURG','MEC');ops=[];fragments=[];alloc=[]
    source_area=sum(int((before==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_MECKLENBURG','MEC']);weights={'MEC':source_area-13,'SWE':13}
    assert source_area==1289
    for pop in region.children('create_pop'):
        size=pop.children('size')[0];counts=core.allocate(int(size.value),weights);assert counts['MEC']>0
        ops.append((size.start,size.end,'size = '+str(counts['MEC'])))
        if counts['SWE']:fragments.append(core.edits(raw[pop.start:pop.end],[(size.start-pop.start,size.end-pop.start,'size = '+str(counts['SWE']))]))
        alloc.append(dict(culture=pop.one('culture'),religion=pop.one('religion','DEFAULT'),before=int(size.value),after=counts))
    files[rel]=core.append(core.edits(raw,ops),'STATE_MECKLENBURG','SWE','\n'.join(fragments))
    rel='map_data/province_terrains.txt';raw=originals[rel];terrains={rgb.upper():kind for rgb,kind in re.findall(r'(x[0-9A-Fa-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw+'\n'+''.join(r['rgb']+'="'+terrains[r['parent_rgb'].upper()]+'"\n' for r in assignments)
    rel=core.active_registry_path().relative_to(ROOT).as_posix();oldledger=b['registry'];ledger=sorted(oldledger+[
        dict(rgb=r['rgb'],state=r['state'],beneficiary='SWE',basis='MAP2N completion: Wismar/Benz/Neukloster, source-traced native-scale jurisdiction; historical fringes generalized; see MAP2N/REPORT.md.') for r in assignments],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[rel]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    refs=[dict(state='STATE_MECKLENBURG',field='prime_land',before=core.values(state,'prime_land'),after=core.values(state,'prime_land')+[WISMAR])]
    migration=dict(replaced_regions=['STATE_MECKLENBURG'],previous=[r for r in oldledger if r['state']=='STATE_MECKLENBURG'],updated=[r for r in ledger if r['state']=='STATE_MECKLENBURG'],
        new_members=[],free_cities=[],new_provinces=assignments,region_reference_changes=refs,extent_added_cells=[],extent_removed_cells=[],
        external_territorial_holders={'SWE':['STATE_MECKLENBURG']},external_holder_RGBs=NEW,
        limitation='Exact frozen provinces only; Sweden is not an imperial member and no Swedish mainland regions are registered')
    dump('REGISTRY_MIGRATION.json',migration)
    parents=sorted({r['parent_rgb'] for r in assignments});retained=[]
    for rgb in parents:retained.append(dict(rgb=rgb,parent_rgb=rgb,state='STATE_MECKLENBURG',owner='MEC',previous_owner='MEC',pixels=int((after==int(rgb[1:],16)).sum())))
    dump('GEOMETRY.json',dict(parents=parents,assignments=retained+assignments,new_provinces=assignments,changes=changes))
    dump('ORIGINAL_TEXT.json',originals);dump('EXPECTED_TEXT.json',files)
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'HISTORY.patch')
    finally:core.OUT=oldout
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('PLAN.json',dict(changes=changes,assignments=assignments,weights=weights,allocations=alloc,text_files=list(files),new_RGBs=NEW,
        bitmap_sha256=core.sha(OUT/'provinces_candidate.png'),tracing_sha256=core.sha(OUT/'SOURCE_TRACING.json')))
    print('Prepared13 mainland cells,4 RGB, populations',alloc)

def install():
    b=load('BASELINE.json');p=load('PLAN.json');current=prior.economy.runtime_hashes()
    for rel,t in load('EXPECTED_TEXT.json').items():assert read(rel).rstrip('\r\n')==t.rstrip('\r\n'),rel
    changed={rel for rel,h in current.items() if b['hashes'].get(rel)!=h}
    assert changed==set(p['text_files'])&set(current),'Only reviewed text may precede bitmap install'
    assert core.sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    assert core.sha(OUT/'provinces_candidate.png')==p['bitmap_sha256']
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png');print('Installed13 mainland cells; Poel relief untouched')

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'IMPERIAL.patch')
    finally:core.OUT=oldout

def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
    import prototype_map2k_main_map as main
    main.MOD=ROOT;main.PACKAGE=OUT/'MAIN_MAP';main.build_and_test()

def previews():
    from PIL import ImageColor
    before=core.packed(PARENT.parent/'MAP2M/R9/provinces_candidate.png');after=core.packed(ROOT/'map_data/provinces.png')
    inv=core.qa.inventory();owners={r['key'][0]:r['key'][2] for r in inv['owners']}
    oldowners={r['key'][0]:r['key'][2] for r in island.load('BASELINE.json')['inventory']['owners']}
    palette={'SWE':'#e3bc3b','LUB':'#bb775f','MEC':'#9bb79b','MST':'#a2b6bd'}
    box=(4351,733,4368,746);scale=32
    def panel(bmp,own,title):
        x0,y0,x1,y1=box;arr=np.full((y1-y0,x1-x0,3),[216,232,241],dtype=np.uint8);local=bmp[y0:y1,x0:x1]
        for rgb,tag in own.items():
            if tag in palette:arr[local==int(rgb[1:],16)]=ImageColor.getrgb(palette[tag])
        im=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
        canvas=Image.new('RGB',(im.width,im.height+75),'white');canvas.paste(im,(0,35));d=ImageDraw.Draw(canvas);d.text((7,8),title,font=prior.old.font(17),fill='black')
        for x in range(x0,x1):d.line(((x-x0)*scale,35,(x-x0)*scale,35+im.height),fill='#78888a',width=1)
        for y in range(y0,y1):d.line((0,(y-y0)*scale+35,im.width,(y-y0)*scale+35),fill='#78888a',width=1)
        for name,x,y in [('Poel',4354.5,734.2),('Wismar',4353.4,741.6),('Benz',4358.2,737.9),('Amt Neukloster',4360.4,742.6)]:
            anchors={'Poel':(4356,737),'Wismar':(4356.5,740.5),'Benz':(4359.5,739.5),'Amt Neukloster':(4362,740.5)}
            ax,ay=anchors[name];dot=((ax-x0)*scale,(ay-y0)*scale+35);label=((x-x0)*scale,(y-y0)*scale+35)
            d.line((label[0]+15,label[1]+8,dot[0],dot[1]),fill='#384b4c',width=1);d.ellipse((dot[0]-2,dot[1]-2,dot[0]+2,dot[1]+2),fill='#384b4c')
            d.text(((x-x0)*scale,(y-y0)*scale+35),name,font=prior.old.font(14),fill='#172222',stroke_width=1,stroke_fill='white')
        d.text((7,canvas.height-28),'Or : SWE | brun : LUB | vert : MEC | bleu pale : mer',font=prior.old.font(12),fill='black')
        return canvas
    panels=[panel(before,oldowners,'AVANT MAP2N : reference R9 acceptee'),panel(after,owners,'APRES MAP2N : trois possessions integrees')]
    image=Image.new('RGB',(panels[0].width*2,panels[0].height+50),'white')
    for i,p in enumerate(panels):image.paste(p,(i*p.width,0))
    ImageDraw.Draw(image).text((8,image.height-34),'Echelle du jeu : contours generalises ; aucune certification cadastrale.',font=prior.old.font(17),fill='black')
    image.save(PARENT/'MAP2N_BEFORE_AFTER.png')
    for name in ['WISMAR','POEL','NEUKLOSTER']:image.save(PARENT/(name+'_BEFORE_AFTER.png'))

def validate():
    b=load('BASELINE.json');p=load('PLAN.json');initial=island.load('BASELINE.json');ip=island.load('ISLAND_PLAN.json');h=island.load('RELIEF_PLAN.json');inv=core.qa.inventory();checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    before=core.packed(ROOT/b['bitmap_reference']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy()
    for r in p['changes']:expected[r['Y'],r['X']]=int(r['RGB_after'][1:],16)
    check('Exact13 reviewed mainland cells only after Poel',np.array_equal(expected,after) and int((before!=after).sum())==13)
    check('Installed candidate and frozen source tracing',core.sha(ROOT/'map_data/provinces.png')==p['bitmap_sha256'] and core.sha(OUT/'SOURCE_TRACING.json')==p['tracing_sha256'])
    check('All source cells MEC in Mecklenburg',all(r['State_ID']=='STATE_MECKLENBURG' and r['Owner_before']=='MEC' and r['Owner_after']=='SWE' for r in p['changes']))
    for row in p['assignments']:
        rgb=row['rgb'];refs=[r for r in inv['owners'] if r['key'][0]==rgb]
        check('Unique correct owner/State_ID '+rgb,len(refs)==1 and refs[0]['count']==1 and refs[0]['key'][1:]==['STATE_MECKLENBURG','SWE'] and inv['geometry'][rgb]=='STATE_MECKLENBURG')
        check('One connected component and exact footprint '+rgb,len(core.components(after==int(rgb[1:],16)))==1 and int((after==int(rgb[1:],16)).sum())==row['pixels'])
        check('One documented parent and retained parent '+rgb,all(before[y,x]==int(row['parent_rgb'][1:],16) for x,y in row['cells']) and np.any(after==int(row['parent_rgb'][1:],16)))
    core_w={(r['X'],r['Y']) for r in p['changes'] if r['RGB_after'] in [WISMAR,WISMAR_EAST]};benz={(r['X'],r['Y']) for r in p['changes'] if r['RGB_after']==BENZ};amt={(r['X'],r['Y']) for r in p['changes'] if r['RGB_after']==NEUKLOSTER}
    check('Wismar4 Benz1 Neukloster8 cells',len(core_w)==4 and len(benz)==1 and len(amt)==8)
    check('No artificial west-east corridor',all(after[y,4358]==before[y,4358] for y in range(738,743)) and all(after[y,4360]==before[y,4360] for y in range(738,743)))
    check('Poel all4 exact RGB preserved',all(after[r['Y'],r['X']]==int(r['RGB_after'][1:],16) for r in ip['changes']))
    check('Poel full eight-neighbour sea buffer preserved',all(after[y,x]==int(island.SEA[1:],16) for x,y in h['moat_cells']))
    check('All accepted R9 Pomeranian pixels unchanged',np.array_equal(before[:,4380:],after[:,4380:]))
    for rgb,n in [(0x567452,400),(0xE1A03A,290),(0xEDB010,85),(0xFCC7B7,142),(0x41A021,153)]:check('Exact protected R9 footprint '+hex(rgb),np.array_equal(before==rgb,after==rgb) and int((after==rgb).sum())==n)
    world_before=core.packed(PARENT.parent/'MAP2M/R9/provinces_candidate.png')
    check('Cumulative21 province cells changed since acceptedR9',int((world_before!=after).sum())==21)
    original=world_before.copy()
    for r in ip['changes']+p['changes']:original[r['Y'],r['X']]=int(r['RGB_after'][1:],16)
    check('Exact cumulative raster from immutable initial baseline',np.array_equal(original,after))
    check('Exactly six new RGB and no old RGB removed',set(np.unique(after))-set(np.unique(world_before))=={int(rgb[1:],16) for rgb in NEW+[island.SWE,island.LUB]} and not set(np.unique(world_before))-set(np.unique(after)))
    owners=core.qa.counter(b['inventory']['owners'])
    for rgb in NEW:owners[rgb,'STATE_MECKLENBURG','SWE']=1
    check('Exact cumulative ownership references',owners==core.qa.counter(inv['owners']))
    geometry=b['inventory']['geometry'].copy();geometry.update({rgb:'STATE_MECKLENBURG' for rgb in NEW})
    check('Only four new Mecklenburg definitions',geometry==inv['geometry'])
    check('Only additional Swedish Mecklenburg subdivision',{tuple(v) for v in inv['states']}=={tuple(v) for v in b['inventory']['states']}|{('STATE_MECKLENBURG','SWE')})
    check('Old incorporation statuses preserved',all(inv['state_types'][k]==v for k,v in b['inventory']['state_types'].items()))
    for field in ['countries','pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:check('Global cumulative preservation '+field,inv[field]==initial['inventory'][field])
    check('World population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for row in p['allocations']:
        religion=row['religion'] if row['religion']!='DEFAULT' else 'DEFAULT:'+row['culture'];n=row['after']['SWE']
        regional['STATE_MECKLENBURG','MEC',row['culture'],religion]-=n;regional['STATE_MECKLENBURG','SWE',row['culture'],religion]+=n
        check('Deterministic integer allocation '+row['culture'],sum(row['after'].values())==row['before'] and row['after']==core.allocate(row['before'],p['weights']))
    check('Exact culture/religion delta in Mecklenburg only',+regional==core.qa.counter(inv['regional_pop']))
    check('Poel/Pomeranian regional population entirely retained',{k:v for k,v in regional.items() if k[0]=='STATE_POMERANIA'}=={k:v for k,v in core.qa.counter(b['inventory']['regional_pop']).items() if k[0]=='STATE_POMERANIA'})
    for rel,t in load('EXPECTED_TEXT.json').items():
        actual=read(rel);check('Exact reviewed text '+rel,actual.rstrip('\r\n')==t.rstrip('\r\n'))
        if rel.endswith('.txt'):check('Parsed '+rel,bool(core.cw.parse(actual)))
    # Frozen native hubs never moved or silently re-bound to a different owner.
    for r in prior.locators(before):
        if r['ID'] in [57,75]:check('Hub physical/RGB preserved '+r['Kind']+str(r['ID']),before[math.floor(r['Y']),math.floor(r['X'])]==after[math.floor(r['Y']),math.floor(r['X'])])
    for field in ['city','port','farm','mine','wood','arable_land','capped_resources','naval_exit_id']:
        old=next(n for n in core.cw.parse(load('ORIGINAL_TEXT.json')['map_data/state_regions/00_west_europe.txt']) if n.key=='STATE_MECKLENBURG')
        new=next(n for n in core.cw.parse(read('map_data/state_regions/00_west_europe.txt')) if n.key=='STATE_MECKLENBURG')
        check('Mecklenburg resource/hub unchanged '+field,[core.qa.norm(n) for n in old.children(field)]==[core.qa.norm(n) for n in new.children(field)])
    for rel in ['map_data/heightmap.png','map_data/packed_heightmap.png','map_data/rivers.png']:check('Poel physical layer byte-exact retained '+rel,core.sha(ROOT/rel)==b['hashes'][rel])
    for name,sha in h['source_hashes'].items():check('Game source untouched '+name,core.sha(core.qa.GAME/'map_data'/name)==sha)
    check('Native topology/indirection still inherited',not (ROOT/'map_data/heightmap.heightmap').exists() and not (ROOT/'map_data/indirection_heightmap.png').exists())
    ledger=json.loads(core.active_registry_path().read_text());check('504 registry entries, all previous500 byte-value entries retained',len(ledger)==504 and [r for r in ledger if r['rgb'] not in NEW]==b['registry'])
    from map2l_registry import territorial_holder_overrides,additional_members,apply_territorial_migrations,rightful_holder_condition
    check('Swedish external exceptions only explicit two regions',territorial_holder_overrides()['SWE']=={'STATE_POMERANIA','STATE_MECKLENBURG'} and 'SWE' not in additional_members())
    check('Reviewed Swedish new holders accepted without bloc membership',all(rightful_holder_condition(r)=='exists = c:SWE' for r in ledger if r['rgb'] in NEW))
    check('No Swedish mainland claims implied',rightful_holder_condition(dict(beneficiary='SWE',state='STATE_UPPLAND'))!='exists = c:SWE')
    mask=np.array(Image.open(ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds').convert('RGBA'))[:,:,0]>0
    rights=np.isin(after,[int(r['rgb'][1:],16) for r in ledger]);check('Final de-jure DDS exactly matches all504 rights',np.array_equal(mask,rights[708:1220,4152:4664]))
    check('Mainland transfers preserve de-jure land extent',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),rights))
    compiled=load('IMPERIAL_EXPECTED.json')
    for rel,t in compiled.items():check('Exact generated imperial dependency '+rel,read(rel).rstrip('\r\n')==t.lstrip('\ufeff').rstrip('\r\n'))
    mapresults=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text());check('16 overlay checks and compiled helper',len(mapresults['checks'])==16 and all(r['passed'] for r in mapresults['checks']) and mapresults['hlsl_harness']['passed'])
    tracing=load('SOURCE_TRACING.json');held=[r['source_alignment_error_native_px'] for r in tracing['controls'] if r['role']=='CHECK']
    check('Four reserved source-map registration controls',len(held)==4 and max(held)<.2)
    # Validate geographic city diagnostics, not native locator names or fake hubs.
    towns={'Wismar':[11.45563,53.89218],'Neukloster':[11.68779,53.86661]};diagnostics=[]
    model=prior.seven.w.load('TRANSFORMATIONS.json')['selected_native']
    for name,geo in towns.items():
        x,y=prior.seven.r.forward(model,[geo])[0];rgb='x'+format(int(after[math.floor(y),math.floor(x)]),'06X');refs=[r for r in inv['owners'] if r['key'][0]==rgb]
        check('Coarse city ownership diagnostic '+name,refs and refs[0]['key'][1:]==['STATE_MECKLENBURG','SWE']);diagnostics.append(dict(Name=name,X=float(x),Y=float(y),RGB=rgb,Certified_city_position=False))
    dump('CITY_DIAGNOSTICS.json',diagnostics)
    active=core.active_registry_path().relative_to(ROOT).as_posix();check('Earlier R8 R9 artifacts immutable',all(core.sha(ROOT/rel)==sha for rel,sha in initial['earlier_proofs'].items() if rel!=active))
    current=prior.economy.runtime_hashes();changed={rel for rel,sha in current.items() if b['hashes'].get(rel)!=sha}
    allowed=set(p['text_files'])|set(compiled)|{'map_data/provinces.png','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    check('Only reviewed mainland runtime files changed',changed<=allowed and set(current)==set(b['hashes']))
    check('44duplicateRGB12badrefs remain preexisting only',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('HEAD/index unchanged',prior.old.prior.r2.head()==b['git_head'] and core.sha(ROOT/'.git/index')==b['git_index'])
    original_changed={rel for rel,sha in current.items() if initial['hashes'].get(rel)!=sha}
    result=dict(status='MAP2N_READY_FOR_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2N_VALIDATION_FAILED',
        sectors=dict(WISMAR='IMPLEMENTED_STATIC_CHECKED',POEL='IMPLEMENTED_STATIC_CHECKED',NEUKLOSTER='IMPLEMENTED_STATIC_CHECKED'),
        passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,applied_province_cells_total=21,mainland_cells=13,
        new_RGBs=[island.SWE,island.LUB]+NEW,registered_RGBs=504,population_world=835804980,
        mainland_population_reallocated=sum(r['after']['SWE'] for r in p['allocations']),
        engine_tested=False,runtime_user_validated=False,R8_R9_runtime_status='PASS_RUNTIME_USER_VALIDATED',historical_boundary_certified=False,
        functional_files_changed=sorted(original_changed),source_registration_holdout_mean_px=float(np.mean(held)),source_registration_holdout_max_px=max(held),
        source_alignment_not_native_projection_accuracy=True)
    # Human acceptance is additive; do not erase it when rerunning static QA.
    receipt_path=PARENT/'RUNTIME_USER_VALIDATION_2026_10_15.json'
    if receipt_path.exists():
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
        assert receipt['lot']=='MAP2N' and not receipt['automated_engine_test']
        result.update(runtime_status=receipt['status'],runtime_user_validated=True,
            runtime_user_validation_receipt=receipt_path.relative_to(ROOT).as_posix(),
            runtime_validation_method='Manual user report; no automated engine test; duration and individually inspected items unspecified')
    dump('VALIDATION.json',result)
    if not (OUT/'POEL_STAGE_VALIDATION.json').exists():
        old=island.load('VALIDATION.json');assert old['status']=='MAP2N_POEL_READY_FOR_RUNTIME_VALIDATION';shutil.copyfile(PARENT/'VALIDATION.json',OUT/'POEL_STAGE_VALIDATION.json')
    (PARENT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    # Cumulative cell CSV uses the same schema for coastline and mainland stages.
    fields=['Sector','X','Y','State_before','State_after','RGB_before','RGB_after','Owner_before','Owner_after','Source','Applied']
    rows=[dict(Sector='POEL',X=r['X'],Y=r['Y'],State_before=r['State_before'],State_after=r['State_after'],RGB_before=r['RGB_before'],RGB_after=r['RGB_after'],Owner_before=r['Owner_before'],Owner_after=r['Owner_after'],Source='Retained Natural Earth coast and Wismar comparative map; native-scale island',Applied=True) for r in ip['changes']]
    rows += [dict(Sector=r['Sector'],X=r['X'],Y=r['Y'],State_before=r['State_ID'],State_after=r['State_ID'],RGB_before=r['RGB_before'],RGB_after=r['RGB_after'],Owner_before=r['Owner_before'],Owner_after=r['Owner_after'],Source=r['Source'],Applied=True) for r in p['changes']]
    island.audit.csvout('TERRITORIAL_CHANGES.csv',rows,fields)
    a=core.qa.counter(initial['inventory']['regional_pop']);z=core.qa.counter(inv['regional_pop']);island.audit.csvout('POPULATION_VALIDATION.csv',[dict(State_ID=k[0],Owner=k[1],Culture=k[2],Religion=k[3],Before=a[k],After=z[k],Difference=z[k]-a[k]) for k in sorted(a.keys()|z.keys()) if k[0] in ['STATE_MECKLENBURG','STATE_POMERANIA']])
    manifest=dict(functional_files={rel:current[rel] for rel in sorted(original_changed)},registry_sha256=core.sha(core.active_registry_path()),runtime_tested=False)
    dump('INSTALLED_MANIFEST.json',manifest)
    print(result['status'],result['passed'],'/',result['total']);print('Failures',[r['name'] for r in checks if not r['passed']]);assert all(r['passed'] for r in checks)

def tests():
    import unittest
    loader=unittest.TestLoader();suite=unittest.TestSuite([loader.discover(str(ROOT/'tools'),pattern='test_map2n*.py'),loader.discover(str(ROOT/'tools'),pattern='test_map2l_registry.py')])
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    dump('UNIT_TESTS.json',dict(passed=result.wasSuccessful(),tests_run=result.testsRun,failures=[(t.id(),e) for t,e in result.failures],errors=[(t.id(),e) for t,e in result.errors],
        scope='Current cumulative Poel plus mainland tests and territorial registry; read-only static/model tests, not engine validation'))
    assert result.wasSuccessful()

if __name__=='__main__':globals()[sys.argv[1]]()
