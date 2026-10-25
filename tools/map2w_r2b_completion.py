"""MAP2W-R2-B: current-state continuation, never replay a previous install."""
import collections as C
import json,re,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2w_r2_hesse_nassau as a
core=a.core;q=a.q;ROOT=a.ROOT;OUT=a.r1.OUT/'R2B'
def dump(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def capture():
    assert not (OUT/'BASELINE.json').exists(),'Immutable capture already exists'
    backup=a.OUT/'provinces_candidate.png';assert core.sha(backup)==core.sha(ROOT/'map_data/provinces.png')
    inv=core.qa.inventory();originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if any(s in raw for s in ['STATE_HESSE','STATE_RHINELAND','STATE_SAXONY','STATE_NORTH_RHINE']):originals[p.relative_to(ROOT).as_posix()]=raw
    registry=json.loads(core.active_registry_path().read_text(encoding='utf8'))
    assert len(registry)==554 and sum(r['count'] for r in inv['pops'])==835801255
    dump('BASELINE.json',dict(inventory=inv,originals=originals,hashes=q.economy.runtime_hashes(),registry=registry,bitmap_backup=backup.relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(backup),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=core.sha(ROOT/'.git/index'),registry_tool=(ROOT/'tools/map2l_registry.py').read_text(encoding='utf8')))
    print('Fresh baseline: world 835801255; 554 imperial RGB; prior R2-A bitmap verified',flush=True)
def source_previews():
    im=Image.open(a.r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB')
    for name,box in [('NASSAU',(500,2600,2000,4000)),('FULDA',(2450,1950,3850,3150))]:
        crop=im.crop(box);d=ImageDraw.Draw(crop);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
        for x in range((box[0]//100+1)*100,box[2],100):d.line((x-box[0],0,x-box[0],crop.height),fill='#296bba',width=1);d.text((x-box[0]+2,0),str(x),font=font,fill='blue',stroke_width=2,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):d.line((0,y-box[1],crop.width,y-box[1]),fill='#296bba',width=1);d.text((0,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=2,stroke_fill='white')
        crop.thumbnail((1500,1400));crop.save(OUT/(name+'_SOURCE.png'))
    from georeference.model import forward
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    cities=[('Saarbruecken',6.9969,49.2326),('Ottweiler',7.1646,49.401),('StJohann',6.997,49.234),('Diez',8.008,50.37),('Hadamar',8.043,50.445),('Usingen',8.537,50.336),('Wiesbaden',8.241,50.083),('Homburg',8.61,50.23),('Herbstein',9.35,50.56),('Geisa',9.95,50.716),('Dermbach',10.12,50.714)]
    pix=forward(model,[[lo,la] for _,lo,la in cities]);im=core.packed(ROOT/'map_data/provinces.png');own={r['key'][0]:r['key'][1:] for r in load('BASELINE.json')['inventory']['owners']}
    rows=[]
    for (n,lo,la),p in zip(cities,pix):
        rgb='x'+format(int(im[round(p[1]),round(p[0])]),'06X');rows.append(dict(name=n,geo=[lo,la],diagnostic_pixel=p.tolist(),rgb=rgb,owner=own.get(rgb)))
    dump('CITY_DIAGNOSTIC_BEFORE.json',rows);print(json.dumps(rows),flush=True)
def geometry():
    """Interior jurisdiction traces; no previous accepted RGB is eligible."""
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup']);owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    nassau=np.array(json.loads((a.OUT/'SOURCE_ALIGNMENT.json').read_text())['transform'])
    fulda=np.array(json.loads((a.r1.OUT/'SOURCE_ALIGNMENT.json').read_text())['transform'])
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    controls=[('Saarbruecken',2636,2818,6.9969,49.2326),('Ottweiler',3558,1312,7.1646,49.4010),('Saarlouis',1547,2068,6.7511,49.3135),('Neunkirchen',3710,1874,7.1806,49.3470),('Homburg_Saar',4790,2033,7.338,49.3225),('StWendel',3840,816,7.168,49.467)]
    X=np.array([[x,y,1] for _,x,y,_,_ in controls]);Y=forward(model,[[lo,la] for _,_,_,lo,la in controls]);saar=np.linalg.lstsq(X,Y,rcond=None)[0]
    dump('SAAR_SOURCE_ALIGNMENT.json',dict(transform=saar.tolist(),controls=[dict(name=n,source=[x,y],geo=[lo,la],diagnostic_pixel=p.tolist(),sheet_residual=float(np.linalg.norm(np.array([x,y,1])@saar-p))) for (n,x,y,lo,la),p in zip(controls,Y)],warning='Sheet registration to inherited diagnostic projection; NOT independent native pixel validation. Interior B generalisation; not cadastral accuracy.'))
    specs=[
      ('Saarbruecken_Ottweiler','NSB','SAAR',[(2000,2200),(2500,2000),(2900,1600),(3200,1500),(3400,1150),(3900,1000),(4250,1300),(4100,1750),(4250,1930),(3900,2050),(3600,2100),(3260,2350),(3180,2700),(3250,2850),(3100,3000),(2850,2950),(2600,2860),(2350,2890),(2100,2700)],{'x11C021'}),
      ('Hadamar_Ellar','NOU','NASSAU',[(830,2790),(970,2780),(990,2840),(940,2895),(930,2945),(1000,2955),(990,2995),(940,2990),(900,3030),(870,3010),(820,3000),(800,2950)],{'x1357DB','x90C0A0'}),
      ('Diez','NOU','NASSAU',[(710,3110),(790,3110),(820,3155),(890,3170),(875,3190),(820,3190),(800,3220),(770,3190),(755,3160),(700,3160)],{'x90C0A0','x1357DB'}),
      ('Loehnberg_Merenberg','NWB','NASSAU',[(1010,2735),(1070,2780),(1150,2775),(1170,2820),(1275,2850),(1280,2875),(1190,2875),(1140,2900),(1120,2875),(1080,2870),(1040,2850),(1020,2810)],{'x1357DB','x90C0A0'}),
      ('Usingen_centre','NAS','NASSAU',[(1390,3120),(1485,3135),(1530,3155),(1580,3175),(1570,3250),(1500,3290),(1460,3315),(1410,3280),(1380,3230)],{'x8B7C67','x11C0A0','x1357DB'}),
      ('Wiesbaden','NAS','NASSAU',[(1000,3670),(1130,3650),(1220,3670),(1210,3750),(1230,3800),(1200,3830),(1200,3860),(1170,3850),(1155,3875),(1070,3850),(1060,3820),(1010,3820)],{'x11C0A0','x8B7C67','x1357DB'}),
      ('Geisa_Rasdorf','FUL','FULDA',[(3400,2295),(3480,2310),(3570,2320),(3600,2380),(3600,2440),(3530,2450),(3470,2440),(3440,2465),(3370,2445),(3340,2390)],{'xD0C021','xD04121'}),
      ('Dermbach','FUL','FULDA',[(3710,2300),(3740,2320),(3770,2325),(3770,2395),(3760,2440),(3730,2480),(3700,2470),(3680,2450),(3700,2410)],{'xD0C021'}),
      ('Herbstein','FUL','FULDA',[(2570,2710),(2665,2705),(2715,2725),(2710,2755),(2675,2760),(2645,2780),(2610,2770),(2590,2780),(2570,2740)],{'xD04121'})]
    sources={'NASSAU':(Image.open(a.r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB'),nassau),'FULDA':(Image.open(a.r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB'),fulda),'SAAR':(Image.open(OUT/'EVIDENCE/Saarbruecken_1789_Fabricius_1909.jpg').convert('RGB'),saar)}
    labels={};traces=[];excluded=[]
    for name,tag,source,poly,allowed in specs:
        im,tr=sources[source];sheet=np.asarray(im);itr=np.linalg.inv(np.vstack([tr.T,[0,0,1]]));mapped=np.column_stack([poly,np.ones(len(poly))])@tr
        xmin,ymin=np.floor(mapped.min(axis=0)).astype(int);xmax,ymax=np.ceil(mapped.max(axis=0)).astype(int)
        yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx.ravel();yy=yy.ravel();chosen=core.inside(np.column_stack([xx+.5,yy+.5]),mapped);accepted=[]
        for x,y in zip(xx[chosen],yy[chosen]):
            rgb='x'+format(int(before[y,x]),'06X');sid,old=owners[rgb];sx,sy,_=itr@np.array([x+.5,y+.5,1]);sx=int(round(sx));sy=int(round(sy));sample=sheet[sy-15:sy+16,sx-15:sx+16].astype(int);rr,gg,bb=sample[...,0],sample[...,1],sample[...,2]
            if source=='NASSAU':fraction=float(np.mean((gg>rr+7)&(gg>bb+3)&(rr<185)&(bb>80)))
            elif source=='FULDA':fraction=float(np.mean((rr>gg+5)&(bb>gg+3)&(rr<250)&(gg>60)))
            else:fraction=float(np.mean((rr>bb+35)&(gg>bb+28)&(bb<175)&(np.abs(rr-gg)<35)))
            reason='SOURCE_FILL_OR_EDGE' if fraction<0.50 else 'PRIOR_CORE_OR_UNREVIEWED_PARENT' if rgb not in allowed else None
            if reason:excluded.append(dict(territory=name,cell=[int(x),int(y)],rgb=rgb,owner=old,reason=reason,source_pixel=[sx,sy],fraction=fraction));continue
            if old==tag:continue
            assert (int(x),int(y)) not in labels
            labels[int(x),int(y)]=(tag,name);accepted.append([int(x),int(y)])
        traces.append(dict(territory=name,tag=tag,source=source,source_polygon=poly,game_polygon=mapped.tolist(),included=accepted))
    parents=sorted({'x'+format(int(before[y,x]),'06X') for x,y in labels});after=before.copy();assignments=[];new=[];used=set(map(int,np.unique(before)));color=0xEDB800
    for parent in parents:
        sid,old=owners[parent];ys,xs=np.where(before==int(parent[1:],16));tags=np.array([labels.get((int(x),int(y)),(old,''))[0] for x,y in zip(xs,ys)])
        for tag in sorted(set(tags)):
            mask=np.zeros(before.shape,bool);mask[ys[tags==tag],xs[tags==tag]]=True
            for i,part in enumerate(core.components(mask)):
                if tag==old and i==0:rgb=parent
                else:
                    while color in used:color+=1
                    rgb='x'+format(color,'06X');used.add(color);color+=1;new.append(dict(rgb=rgb,parent_rgb=parent))
                py=np.array([p[0] for p in part]);px=np.array([p[1] for p in part]);after[py,px]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=old,owner=tag,pixels=len(part),cells=[[int(x),int(y)] for y,x in part],territories=sorted({labels[x,y][1] for y,x in part if (x,y) in labels}),confidence='B' if tag!=old else 'C_RETAINED'))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,traces=traces,excluded=excluded,new_members=['NSB'],hub_rebindings=[],limits='Inward B traces only; unchanged remnants do not certify surrounding ownership. No Homburg independence, no Hanau native subject, no condominium or post-1776 acquisitions.'))
    # Inspect actual accepted cell footprints against the retained source sheets.
    for source,(im,tr) in sources.items():
        im=im.copy();d=ImageDraw.Draw(im);itr=np.linalg.inv(np.vstack([tr.T,[0,0,1]]))
        for t in traces:
            if t['source']!=source:continue
            for x,y in t['included']:
                corners=[tuple((itr@np.array([px,py,1]))[:2]) for px,py in [(x,y),(x+1,y),(x+1,y+1),(x,y+1),(x,y)]];d.line(corners,fill='blue',width=5)
        box={'NASSAU':(500,2600,2000,4000),'FULDA':(2450,1950,3850,3150),'SAAR':(1600,850,4400,3300)}[source];crop=im.crop(box);crop.thumbnail((1500,1400));crop.save(OUT/(source+'_ACCEPTED_REVIEW.png'))
    print('Transfers',dict(C.Counter(tag for tag,_ in labels.values())),'newRGB',len(new),'parents',parents,flush=True)
    print('Sectors',dict(C.Counter(name for _,name in labels.values())),flush=True)
def compiler_before():
    previous=a.r1.prior.t.OUT;a.r1.prior.t.OUT=OUT
    try:a.r1.prior.t.compiler_before()
    finally:a.r1.prior.t.OUT=previous
def prepare():
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};bindings=[];regions=sorted({r['state'] for r in g['assignments']});groups=C.defaultdict(list)
    assert load('COMPILER_BEFORE.json')['passed']==73
    assert not set(g['new_members'])&set(b['inventory']['countries'])
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png')
    for row in g['assignments']:groups[row['parent_rgb']].append(row)
    rel='common/history/states/00_states.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');ops=[];new_subdivisions=[]
    for sid in regions:
        node=core.state(raw,sid);assert core.qa.signature(node)==core.qa.signature(core.state(b['originals'][rel],sid)),'Concurrent state edit '+sid
        existing=set()
        for n in node.children('create_state'):
            tag=n.one('country').removeprefix('c:');existing.add(tag);f=n.children('owned_provinces')[0];owned=[]
            for rgb in core.values(n,'owned_provinces'):owned.extend(r['rgb'] for r in groups[rgb] if r['owner']==tag) if rgb in groups else owned.append(rgb)
            owned.extend(r['rgb'] for r in g['assignments'] if r['state']==sid and r['owner']==tag and r['previous_owner']!=tag)
            assert owned,'Do not silently delete subdivision '+sid+'/'+tag
            if owned!=core.values(n,'owned_provinces'):ops.append((f.start,f.end,'owned_provinces = { '+' '.join(owned)+' }'))
        for tag in sorted({r['owner'] for r in g['assignments'] if r['state']==sid}-existing):
            owned=[r['rgb'] for r in g['assignments'] if r['state']==sid and r['owner']==tag];ops.append((node.end-1,node.end-1,'\ncreate_state = { country = c:'+tag+' owned_provinces = { '+' '.join(owned)+' } }\n'));new_subdivisions.append([sid,tag])
    files[rel]=core.edits(raw,sorted(ops))
    # Preserve all economic geography and scalar resources; split province lists only.
    locs=q.r9.locators(before)
    for rel,old in b['originals'].items():
        if not rel.startswith('map_data/state_regions/'):continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');nodes={n.key:n for n in core.cw.parse(raw)};ops=[]
        for sid in regions:
            if sid not in nodes:continue
            n=nodes[sid];assert core.qa.signature(n)==core.qa.signature(next(z for z in core.cw.parse(old) if z.key==sid))
            for field in ['provinces','prime_land']:
                for f in n.children(field):
                    existing=core.values(n,field);updated=[]
                    for rgb in existing:updated.extend(r['rgb'] for r in groups[rgb]) if rgb in groups else updated.append(rgb)
                    if existing!=updated:
                        ops.append((f.start,f.end,field+' = { '+' '.join('"'+v+'"' for v in updated)+' }'))
                        if field=='prime_land':bindings.append(dict(state=sid,field=field,before=existing,after=updated))
            for loc in locs:
                if loc['ID']!=int(n.one('id')):continue
                x,y=int(loc['X']),int(loc['Y']);rgb='x'+format(int(after[y,x]),'06X');old_rgb=core.cw.scalar(n.one(loc['Kind']))
                if rgb!=old_rgb:
                    f=n.children(loc['Kind'])[0];ops.append((f.start,f.end,loc['Kind']+' = "'+rgb+'"'));bindings.append(dict(state=sid,field=loc['Kind'],before=old_rgb,after=rgb,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
        if ops:files[rel]=core.edits(raw,sorted(ops))
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};weights={};allocations=[]
    counts_by_rgb=dict(zip(*np.unique(before,return_counts=True)))
    for sid,src in sorted({(r['state'],r['previous_owner']) for r in g['assignments']}):
        total=sum(int(counts_by_rgb[int(rgb[1:],16)]) for rgb,st in owners.items() if st==[sid,src]);counts=C.Counter({src:total})
        for r in g['assignments']:
            if r['state']==sid and r['previous_owner']==src and r['owner']!=src:counts[src]-=r['pixels'];counts[r['owner']]+=r['pixels']
        assert counts[src]>0;weights[sid+'|'+src]=dict(counts)
    for rel,old in b['originals'].items():
        if '/pops/' not in rel:continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');ops=[];moved=C.defaultdict(list)
        for key,counts in weights.items():
            sid,src=key.split('|')
            try:n=core.region(raw,sid,src)
            except StopIteration:continue
            assert core.qa.signature(n)==core.qa.signature(core.region(old,sid,src)),('Concurrent population edit',rel,sid,src)
            for pop in n.children('create_pop'):
                f=pop.children('size')[0];amounts=core.allocate(int(f.value),counts);piece=raw[pop.start:pop.end];ops.append((f.start,f.end,'size = '+str(amounts[src])))
                for tag,amount in amounts.items():
                    if tag!=src and amount:moved[sid,tag].append(core.edits(piece,[(f.start-pop.start,f.end-pop.start,'size = '+str(amount))]))
                allocations.append(dict(state=sid,source=src,culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:'+pop.one('culture')),before=int(f.value),after=amounts))
        if ops:
            text=core.edits(raw,sorted(ops))
            for (sid,tag),parts in moved.items():text=core.append(text,sid,tag,'\n'.join(parts))
            files[rel]=text
    dump('ALLOCATION.json',dict(method='TECHNICAL_PROFILE_CONSERVATION_NOT_HISTORICAL_CENSUS',weights=weights,profiles=allocations,buildings='Unchanged at surviving donor subdivisions, no industrial geography inferred from pixel shares',historical_population=None))
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw.rstrip()+'\n'+''.join(r['rgb']+'="'+tm[r['parent_rgb'].upper()]+'"\n' for r in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state'] in regions];updated=[r for r in previous if r['rgb'] not in g['parents']]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2W-R2-B: inward jurisdiction generalisation B; C remnants unchanged, not certified; see MAP2W/R2B/REPORT.md') for r in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state'] not in regions]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    defs='NSB = { color = { 56 118 171 } country_type = recognized tier = principality cultures = { south_german } religion = protestant capital = STATE_RHINELAND }\n'
    files['common/country_definitions/1776_map2w_r2b_saarbruecken.txt']=defs
    files['common/history/countries/nsb - map2w_r2b.txt']=(ROOT/'common/history/countries/nas - nassau.txt').read_text(encoding='utf-8-sig').replace('c:NAS','c:NSB')
    files['common/history/characters/nsb - map2w_r2b.txt']='CHARACTERS = { c:NSB ?= { create_character = { first_name = aor1776_map2w_r2b_nsb_first last_name = aor1776_map2w_r2b_nsb_last historical = yes culture = south_german religion = rel:protestant ruler = yes birth_date = 1745.1.3 interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    # Reuse the existing explicitly simplified dynastic arms, not a new raster asset.
    files['common/flag_definitions/1776_map2w_r2b_saarbruecken.txt']='NSB = { flag_definition = { coa = aor1776_map2w_r2_nassau priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french';files[f'localization/{lang}/1776_map2w_r2b_l_{lang}.yml']='\ufeffl_'+lang+':\n NSB:0 "'+('Nassau-Sarrebruck' if fr else 'Nassau-Saarbrücken')+'"\n NSB_ADJ:0 "'+('sarrebruckois' if fr else 'Saarbrücken')+'"\n aor1776_map2w_r2b_nsb_first:0 "Ludwig"\n aor1776_map2w_r2b_nsb_last:0 "von Nassau-Saarbrücken"\n'
    migration=dict(replaced_regions=regions,previous=previous,updated=updated,new_members=['NSB'],free_cities=[],new_provinces=g['new_provinces'],geometry='MAP2W/R2B/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[],country_additions={n.key:core.qa.signature(n) for n in core.cw.parse(defs)})
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n';files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    dump('EXPECTED_TEXT.json',files);core.OUT=OUT;changes=core.emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,registered_RGBs=len(ledger),region_reference_changes=bindings,new_subdivisions=new_subdivisions))
    print('Prepared',len(changes),'files; imperial RGB',len(ledger),'new subdivisions',new_subdivisions,flush=True)
def install():
    previous=a.OUT;a.OUT=OUT
    try:a.install()
    finally:a.OUT=previous
def imperial():
    previous=a.OUT;a.OUT=OUT
    try:a.imperial()
    finally:a.OUT=previous
def imperial_patches():
    core.OUT=OUT;files=load('IMPERIAL_EXPECTED.json');patches=[]
    for i,(rel,raw) in enumerate(files.items()):
        if (ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'):continue
        name='IMPERIAL_'+str(i)+'.patch';core.emit({rel:raw},name);patches.append(name)
    dump('IMPERIAL_PATCHES.json',patches);print(patches,flush=True)
def journal():
    previous=a.OUT;a.OUT=OUT
    try:a.journal()
    finally:a.OUT=previous
def concurrency():
    """Read-only receipt, not authorization or implementation of external work."""
    b=load('BASELINE.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();rel='common/company_types/00_companies_france.txt'
    assert head.startswith('9b1764e') and subprocess.check_output(['git','diff','--name-only',b['git_head'],head],cwd=ROOT,text=True).splitlines()==[rel]
    old=subprocess.check_output(['git','show',b['git_head']+':'+rel],cwd=ROOT).decode('utf-8-sig');raw=(ROOT/rel).read_text(encoding='utf-8-sig');oldnodes={n.key:n for n in core.cw.parse(old)};newnodes={n.key:n for n in core.cw.parse(raw)}
    assert set(oldnodes)==set(newnodes) and {k for k in oldnodes if core.qa.signature(oldnodes[k])!=core.qa.signature(newnodes[k])}=={'company_dmc'}
    n=oldnodes['company_dmc'];z=newnodes['company_dmc'];assert [core.qa.signature(x) for x in n.children() if x.key!='prosperity_modifier']==[core.qa.signature(x) for x in z.children() if x.key!='prosperity_modifier']
    assert n.children('prosperity_modifier')[0].one('state_assimilation_mult')=='0.1'
    prosperity=z.children('prosperity_modifier')[0];assert {c.key:c.value for c in prosperity.children()}=={'state_assimilation_mult':'0.2','state_conversion_mult':'0.2'}
    paths=[rel,'common/decisions/1776_usa_french_support.txt','common/history/countries/zz_1776_usa_revolution_r2.txt','common/history/diplomatic_plays/00_american_revolution.txt','common/journal_entries/06_usa_independence_mod.txt','common/journal_entries/1776_usa_french_support.txt','common/on_actions/1776_usa_revolution_r2.txt','common/scripted_effects/1776_usa_french_support.txt','common/scripted_triggers/1776_usa_french_support.txt','common/treaty_articles/1776_usa_french_support.txt','events/1776_usa_french_support.txt','events/french_revolution_mod_events.txt','localization/english/1776_usa_revolution_r2_l_english.yml','localization/french/1776_usa_revolution_r2_l_french.yml']
    planned=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_EXPECTED.json'));assert not set(paths)&planned
    for p in paths:
        raw=(ROOT/p).read_text(encoding='utf-8-sig')
        if p.endswith('.txt'):core.cw.parse(raw)
        if p=='common/history/diplomatic_plays/00_american_revolution.txt':assert 'c:USA' in raw and 'dp_independence' in raw
        elif p!=rel:assert 'aor1776_support' in raw or 'aor1776_french_support' in raw or 'aor1776_legacy_debt' in raw,p
        assert 'aor1776_hre_' not in raw and 'c:NSB' not in raw,p
    dump('CONCURRENT_WORK_OBSERVED.json',dict(head_before=b['git_head'],head_after=head,index_sha256=core.sha(ROOT/'.git/index'),hashes={p:core.sha(ROOT/p) for p in paths},files=paths,company_scope='Only company_dmc prosperity: assimilation 0.1 -> 0.2, conversion 0.2 added. Saint-Gobain and Anzin ASTs identical.',usa_scope='USA/FRA American-war/support files assigned to the concurrent agent; receipt is preservation only, not certification of their functionality.',git_cause='External pull --ff-only origin main at 21:50:15 +0200 observed in reflog. No Git mutation by this MAP agent.',historical_baseline_unchanged=True))
    print('External PR8 and 13 USA-support files preserved; no MAP overlap',flush=True)
def princely_government():
    """Vanilla European principality tier selects a duchy; constrain NSB only."""
    files=load('EXPECTED_TEXT.json');changed={}
    rel='common/government_types/00_1776_map2w_r2b_saarbruecken.txt'
    changed[rel]='gov_aor1776_map2w_r2b_saarbruecken = { transfer_of_power = hereditary male_ruler = "RULER_TITLE_PRINCE" female_ruler = "RULER_TITLE_PRINCESS" possible = { c:NSB ?= this has_law = law_type:law_monarchy } on_government_type_change = { change_to_hereditary = yes } on_post_government_type_change = { post_change_to_hereditary = yes } }\n'
    for lang in ['french','english']:
        rel=f'localization/{lang}/1776_map2w_r2b_l_{lang}.yml';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert raw==files[rel].lstrip('\ufeff');fr=lang=='french'
        changed[rel]='\ufeff'+raw+' gov_aor1776_map2w_r2b_saarbruecken:0 "'+('Principauté de Nassau-Sarrebruck' if fr else 'Principality of Nassau-Saarbrücken')+'"\n gov_aor1776_map2w_r2b_saarbruecken_desc:0 "'+('Le [concept_ruler] héréditaire gouverne les possessions de Nassau-Sarrebruck, demeurées distinctes de celles de Nassau-Usingen.' if fr else 'The hereditary [concept_ruler] governs the possessions of Nassau-Saarbrücken, which remain distinct from those of Nassau-Usingen.')+'"\n'
    files.update(changed);dump('EXPECTED_TEXT.json',files);core.OUT=OUT;core.emit(changed,'PRINCELY_GOVERNMENT.patch')
def usa_concurrency():
    """Explicit continuation of the user-assigned USA chantier, never a glob waiver."""
    receipt=load('CONCURRENT_WORK_OBSERVED.json');extra=['common/character_templates/1776_usa_founders.txt','common/decisions/1776_usa_content_r1.txt','common/decisions/1776_usa_founders.txt','common/history/characters/zz_1776_usa_founders.txt','common/history/military_formations/01_military_formations_north_america.txt','common/journal_entries/1776_usa_revolutionary_spirit.txt','common/laws/1776_usa_minutemen.txt','common/on_actions/1776_usa_content_r1.txt','common/scripted_effects/1776_usa_content_r1.txt','common/scripted_effects/1776_usa_echoes.txt','common/scripted_triggers/1776_usa_founders.txt','common/ship_modifications/1776_usa_armed_merchantman.txt','common/ship_types/1776_usa_armed_merchantman.txt','common/static_modifiers/1776_usa_revolution_r2.txt','events/1776_usa_content_r1.txt','events/1776_usa_echoes.txt','events/1776_usa_founders.txt']
    planned=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_EXPECTED.json'));assert not planned&set(extra)
    for rel in extra:
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');core.cw.parse(raw);assert 'aor1776_' in raw,rel
        assert 'c:NSB' not in raw and 'aor1776_hre_' not in raw,rel
    rel='common/history/military_formations/01_military_formations_north_america.txt';old=subprocess.check_output(['git','show',receipt['head_after']+':'+rel],cwd=ROOT).decode('utf-8-sig');raw=(ROOT/rel).read_text(encoding='utf-8-sig')
    previous={n.key:core.qa.signature(n) for n in core.cw.parse(old)[0].children()};current={n.key:core.qa.signature(n) for n in core.cw.parse(raw)[0].children()};assert set(previous)==set(current) and {k for k in previous if previous[k]!=current[k]}=={'c:USA'}
    receipt['files']=sorted(set(receipt['files'])|set(extra));receipt['hashes']={p:core.sha(ROOT/p) for p in receipt['files']};receipt['usa_military_scope']='North-American formation file: only c:USA differs from observed HEAD; includes commanders and merchant-ship type. No non-USA block changed. MAP does not certify USA ship design.'
    receipt['external_activity_policy']='These exact files belong to the concurrently assigned task and may continue changing. Hashes are observed fingerprints, not a lock. MAP validation protects its own expected outputs and all non-USA combat units; no external bytes are restored.'
    receipt['non_usa_north_america_country_AST']={k:v for k,v in current.items() if k!='c:USA'};dump('CONCURRENT_WORK_OBSERVED.json',receipt);print('Protected explicit USA continuation; no non-USA military block changed',flush=True)
def validate():
    from map2l_registry import expected_country_definitions,apply_territorial_migrations,approved_territorial_extensions,approved_lot_dirs
    b=load('BASELINE.json');g=load('GEOMETRY.json');m=load('REGISTRY_MIGRATION.json');inv=core.qa.inventory();checks=[];dump('CURRENT_INVENTORY.json',inv)
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy();eo=counter(b['inventory']['owners']);owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    for k in list(eo):
        if k[0] in g['parents']:del eo[k]
    for row in g['assignments']:
        for x,y in row['cells']:expected[y,x]=int(row['rgb'][1:],16)
        eo[row['rgb'],row['state'],row['owner']]=1
        check('Owner and State_ID '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['owner']])
        mask=after==int(row['rgb'][1:],16);check('Exact connected RGB '+row['rgb'],int(mask.sum())==row['pixels'] and len(core.components(mask))==1)
    check('Full world bitmap exact scoped delta',np.array_equal(expected,after));check('Full world ownership exact delta',counter(inv['owners'])==eo)
    check('45 sovereign transfers',sum(r['pixels'] for r in g['assignments'] if r['owner']!=r['previous_owner'])==45)
    check('Erfurt unchanged',np.array_equal(before[822:837,4342:4359],after[822:837,4342:4359]))
    for key in ['building_levels_written','buildings','duplicates','errors','resolved_demographics','pops']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    concurrent=load('CONCURRENT_WORK_OBSERVED.json') if (OUT/'CONCURRENT_WORK_OBSERVED.json').exists() else None
    if concurrent and 'usa_military_scope' in concurrent:
        check('Non-USA combat units conserved; USA externally assigned',counter([r for r in inv['units'] if r['key'][0]!='USA'])==counter([r for r in b['inventory']['units'] if r['key'][0]!='USA']))
    else:check('Global invariant units',inv['units']==b['inventory']['units'])
    check('Only NSB country added',inv['countries']==expected_country_definitions(b['inventory']['countries'],[m]))
    types=dict(b['inventory']['state_types']);types['STATE_RHINELAND|NSB']='incorporated_default';check('Only one new economic subdivision',inv['state_types']==types)
    ep=counter(b['inventory']['regional_pop'])
    for row in load('ALLOCATION.json')['profiles']:
        ep[row['state'],row['source'],row['culture'],row['religion']]-=row['before']
        for tag,n in row['after'].items():ep[row['state'],tag,row['culture'],row['religion']]+=n
        check('Integer profile '+row['state']+'/'+row['source']+'/'+row['culture']+'/'+row['religion'],sum(row['after'].values())==row['before'] and all(isinstance(n,int) and n>=0 for n in row['after'].values()))
    check('Exact regional population reassignment',counter(inv['regional_pop'])==ep)
    world=sum(r['count'] for r in inv['pops']);oldworld=sum(r['count'] for r in b['inventory']['pops']);check('World total conserved, no fabricated census',world==oldworld==835801255)
    totals={tag:sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag) for tag in ['NSB','NAS','NOU','NWB','FUL','KPF','FRM','HES','HEK','MEI']}
    check('New country has conserved population',totals['NSB']>0)
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'));check('567 unique imperial RGB',len(ledger)==len({r['rgb'] for r in ledger})==567)
    for row in ledger:check('De jure title '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']])
    check('Imperial physical extent conserved',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry'];belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'));regions={r['state'] for r in belgian['assignments']}
    initial=[r for r in initial if r['state'] not in regions]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in belgian['assignments']]+approved_territorial_extensions()
    check('Chronological cumulative registry replay',apply_territorial_migrations(initial)==ledger)
    changed_parents=set(map(int,np.unique(before[before!=after])));check('Only reviewed residual parents recoloured',changed_parents<={int(r[1:],16) for r in g['parents']})
    for row in b['registry']:
        if row['rgb'] in g['parents']:continue
        check('Protected previous RGB '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']] and int(row['rgb'][1:],16) not in changed_parents)
    # Previously accepted territorial cells must remain byte-exact, including
    # all R1 / R2-A cores; no later-core exception is introduced in this lot.
    protected=0
    for directory in approved_lot_dirs():
        if directory==OUT:continue
        geo=json.loads((directory/'GEOMETRY.json').read_text())
        for row in geo['assignments']:
            if row['owner']==row.get('previous_owner'):continue
            cells=row['cells'];ok=all(after[y,x]==before[y,x] for x,y in cells);protected+=len(cells);check('Accepted prior cells '+directory.name+'/'+row['rgb'],ok)
    files=load('EXPECTED_TEXT.json');compiled=load('IMPERIAL_EXPECTED.json')
    for rel,raw in {**files,**compiled}.items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig');check('Planned text '+rel,actual.rstrip()==raw.lstrip('\ufeff').rstrip())
        if rel.endswith('.txt'):
            try:core.cw.parse(actual);check('Clausewitz parse '+rel,True)
            except Exception as exc:check('Clausewitz parse '+rel,False,str(exc))
    affected=set(m['replaced_regions'])
    for rel in files:
        if rel not in b['originals']:continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');old=b['originals'][rel]
        if '/history/' in rel:
            scope=lambda text:[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(text)) if n.key.startswith('s:STATE_') and n.key[2:] not in affected]
            check('Unrelated state histories '+rel,scope(raw)==scope(old))
        if rel.startswith('map_data/state_regions/'):
            # Province and explicitly declared reference deltas only.
            from map2l_registry import rebind_state_definitions
            rebound=rebind_state_definitions(old,[m]);oldnodes={n.key:n for n in core.cw.parse(rebound)};newnodes={n.key:n for n in core.cw.parse(raw)}
            for sid,node in oldnodes.items():
                exclude={'provinces'} if sid in affected else set();check('All resources/IDs/traits/hubs '+sid,[core.qa.signature(n) for n in node.children() if n.key not in exclude]==[core.qa.signature(n) for n in newnodes[sid].children() if n.key not in exclude])
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for r in g['new_provinces']:
        check('Unique new RGB '+r['rgb'],not np.any(before==int(r['rgb'][1:],16)) and len(re.findall(r'(?im)^\s*'+r['rgb']+r'\s*=',terrain))==1)
        check('Inherited terrain '+r['rgb'],tm[r['rgb'].upper()]==tm[r['parent_rgb'].upper()])
        check('New region mapping '+r['rgb'],inv['geometry'].get(r['rgb'])==next(z['state'] for z in g['assignments'] if z['rgb']==r['rgb']))
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_map2w_r2b_l_{lang}.yml';raw=p.read_text(encoding='utf-8-sig');keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0\s+"',raw,re.M)
        check('BOM/header '+lang,p.read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':'))
        check('Six matching unique localisation keys '+lang,len(keys)==len(set(keys))==6 and all(line.count('"')==2 for line in raw.splitlines()[1:] if line.strip()))
        collisions=[]
        for p in (ROOT/'localization'/lang).rglob('*.yml'):
            if p.name.startswith('1776_map2w_r2b_'):continue
            text=p.read_text(encoding='utf-8-sig');collisions.extend(k for k in keys if re.search(r'^\s*'+re.escape(k)+r':',text,re.M))
        check('No localisation collision '+lang,not collisions,collisions)
    ruler=[n for n in core.cw.walk(core.cw.parse((ROOT/'common/history/characters/nsb - map2w_r2b.txt').read_text())) if n.key=='create_character'];check('Dated unique NSB ruler',len(ruler)==1 and ruler[0].one('birth_date')=='1745.1.3' and ruler[0].one('ruler')=='yes')
    check('NSB capital region owned',any(r['key'][1:]==['STATE_RHINELAND','NSB'] for r in inv['owners']))
    check('No new native subject or electoral status',m['new_members']==['NSB'] and not m['free_cities'] and not any('/diplomacy/' in p or '/subject_types/' in p for p in files))
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));allowed=set(files)|set(compiled)|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    external=set(concurrent['files']) if concurrent else set()
    outside=[p for p in changed if p not in allowed|external];check('No unexpected runtime delta, collaborators protected',not outside,outside)
    if concurrent:
        # Other agent is actively writing these exact user-assigned files.
        # Enforce semantic non-overlap, not a false promise of a global lock.
        check('External files remain present and outside MAP writes',all((ROOT/p).is_file() and p not in files and p not in compiled for p in external))
        check('External work does not overlap MAP planned files',not external&(set(files)|set(compiled)))
    for part in ['buildings','military_formations','character_templates','companies','subject_types','diplomacy','map_object_data','production_methods','production_method_groups']:
        check('All MAP-protected '+part+' files byte-identical',all(current.get(p)==h for p,h in b['hashes'].items() if '/'+part+'/' in p and p not in external))
    if concurrent and 'non_usa_north_america_country_AST' in concurrent:
        rel='common/history/military_formations/01_military_formations_north_america.txt';now={n.key:core.qa.signature(n) for n in core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))[0].children() if n.key!='c:USA'}
        check('Non-USA North-American military country AST protected',now==concurrent['non_usa_north_america_country_AST'])
    check('Saint-Gobain icon protected',current.get('gfx/interface/icons/company_icons/historical_company_icons/france_saint_gobain.dds')==b['hashes'].get('gfx/interface/icons/company_icons/historical_company_icons/france_saint_gobain.dds'))
    git_ref=concurrent or dict(head_after=b['git_head'],index_sha256=b['git_index_sha256'])
    check('Observed HEAD preserved',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==git_ref['head_after']);check('Observed index preserved',core.sha(ROOT/'.git/index')==git_ref['index_sha256'])
    result=dict(status='MAP2W_R2B_READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2W_R2B_BLOCKED',scope='New inward B cores only; C peripheries and institutions remain unchanged',runtime_status='NOT_TESTED_R2B',prior_user_validation='../RUNTIME_USER_ATTESTATION_R2B.json',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,world_before=oldworld,world_after=world,country_populations=totals,protected_prior_accepted_cells_checked=protected,runtime_files_modified=[p for p in changed if p not in external],external_files=sorted(external),preexisting_duplicate_RGBs=len(inv['duplicates']),preexisting_invalid_references=inv['errors'],new_errors=[r for r in inv['errors'] if r not in b['inventory']['errors']])
    dump('VALIDATION_R2B.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2W-R2-B',functional_files={p:current[p] for p in changed if p not in external},protected_external_files={p:current[p] for p in external},bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),git_head=git_ref['head_after'],git_index_sha256=git_ref['index_sha256']))
    print(result['status'],result['passed'],'/',len(checks),'populations',totals,flush=True)
    if result['passed']!=len(checks):raise SystemExit(1)
def maps():
    from PIL import ImageColor
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};now=dict(old)
    for row in g['assignments']:now[row['rgb']]=row['owner']
    colors={'NSB':'#3876ab','NAS':'#8171b5','NOU':'#e19b41','NWB':'#5d9eac','HES':'#c695ba','HEK':'#92bc88','WLD':'#a6bd65','FRM':'#d7c45b','PRU':'#839bb6','KMZ':'#d29065','FUL':'#986bb6','KPF':'#dabb68','MEI':'#baaea7','KTR':'#ae718c'}
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',22)
    specs=[('Sarrebruck–Ottweiler',(4256,871,4277,889),[('1 NSB',4265,879)]),('Nassau : compléments',(4281,839,4302,861),[('2 NOU',4286,846),('3 NWB',4290,844),('4 NAS',4297,850),('5 NAS',4291,857)]),('Fulda : possessions complémentaires',(4311,831,4337,851),[('6 FUL',4327,838),('7 FUL',4332,840),('8 FUL',4315,843)])]
    def tile(bitmap,owners,box,labels,outline):
        x0,y0,x1,y1=box;local=bitmap[y0:y1,x0:x1];arr=np.zeros((*local.shape,3),dtype='uint8');scale=21
        for c in np.unique(local):arr[local==c]=ImageColor.getrgb(colors.get(owners.get('x'+format(int(c),'06X')),'#dfdcd4'))
        im=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        if outline:
            for row in g['assignments']:
                if row['owner']==row['previous_owner']:continue
                for x,y in row['cells']:
                    if x0<=x<x1 and y0<=y<y1:d.rectangle(((x-x0)*scale,(y-y0)*scale,(x-x0+1)*scale-1,(y-y0+1)*scale-1),outline='white',width=2)
        for text,x,y in labels:
            px=(x-x0)*scale;py=(y-y0)*scale;d.text((min(max(px-20,2),im.width-75),max(py-25,1)),text,font=f,fill='#142b3a',stroke_width=2,stroke_fill='white')
        return im
    out=Image.new('RGB',(1250,1750),'#fcfaf5');d=ImageDraw.Draw(out);d.text((25,15),'MAP2W-R2-B — 45 cellules transférées ; seuls les ajouts sont encadrés',font=bold,fill='#243747');y=65
    for title,box,labels in specs:
        d.text((25,y),title+' — AVANT',font=bold,fill='#243747');d.text((655,y),'APRÈS — noyaux B',font=bold,fill='#243747');first=tile(before,old,box,labels,False);last=tile(after,now,box,labels,True);out.paste(first,(25,y+35));out.paste(last,(655,y+35));y+=max(first.height,last.height)+75
    d.text((25,1620),'Blanc : transfert nouveau. Repères schématiques, pas une certification GPS ou cadastrale.',font=f,fill='#243747');d.text((25,1650),'Tous les noyaux MAP antérieurs sont conservés. Les résidus non encadrés ne sont pas certifiés.',font=f,fill='#243747');d.text((25,1680),'NSB bleu / NOU orange / NWB turquoise / NAS violet / FUL mauve / KPF ocre.',font=f,fill='#243747');out.save(OUT/'HESSE_NASSAU_R2B_BEFORE_AFTER.png')
    guide=Image.new('RGB',(1450,970),'#fcfaf5');d=ImageDraw.Draw(guide);d.text((25,18),'Vérification R2-B en nouvelle partie — 1er janvier 1776',font=bold,fill='#243747');x=25
    for title,box,labels in specs:
        im=tile(after,now,box,labels,True);im.thumbnail((440,450));guide.paste(im,(x,100));d.text((x,65),title,font=f,fill='#243747');x+=475
    notes=['1. NSB : Rhénanie, au sud-ouest de KPF ; xEDB800 ; 15 cellules. Ludwig, prince, non sujet natif.',
           '2. NOU : Hadamar–Ellar (6) et Diez (2), au sud des noyaux Siegen–Dillenburg protégés.',
           '3. NWB : deux cellules supplémentaires vers Merenberg–Löhnberg ; pas le condominium de Nassau.',
           '4–5. NAS : Usingen-centre (5) et Wiesbaden (6), sans annexion de Francfort ou de Mayence.',
           '6–8. FUL : Geisa–Rasdorf (6), Dermbach (2), Herbstein (1). Capitales de région non déplacées.',
           'Contrôler noms, drapeaux, souverains, populations, marché et subsistance ; puis simuler un mois.',
           'NSB : 16 814 habitants techniques conservés ; aucun recensement 1776 revendiqué, aucune usine ajoutée.',
           'Vérifier les droits du journal impérial, les neuf électeurs et les contributions : Lien 0 %, État 15 %, Électeur 10 %.',
           'Positions et frontières généralisées : consulter le rapport pour les franges C inchangées.',
           'La validation manuelle antérieure couvre les lots récents déclarés, pas ces ajouts R2-B.']
    for i,text in enumerate(notes):d.text((25,590+i*31),text,font=f,fill='#243747')
    guide.save(OUT/'PLAYER_LOCATION_GUIDE.png');print('Before/after and player guide rendered',flush=True)
def tables():
    g=load('GEOMETRY.json');v=load('VALIDATION_R2B.json');b=load('BASELINE.json');alloc=load('ALLOCATION.json');tables={}
    sources={'Saarbruecken_Ottweiler':'EVIDENCE/Saarbruecken_1789_Fabricius_1909.jpg; https://scopearchiv.saarbruecken.de/detail.aspx?ID=85; https://www.lagis-hessen.de/pnd/12862910X',
      'Hadamar_Ellar':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://arcinsys.hessen.de/arcinsys/showFondsDetails?fondsId=3508',
      'Diez':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://arcinsys.hessen.de/arcinsys/showFondsDetails?fondsId=3508',
      'Loehnberg_Merenberg':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://arcinsys.hessen.de/arcinsys/showFondsDetails.action?fondsId=1992',
      'Usingen_centre':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://www.wiesbaden.de/en/microsite/stadtlexikon/import/a-z/wiesbaden-unter-nassauischer-herrschaft',
      'Wiesbaden':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://www.wiesbaden.de/en/microsite/stadtlexikon/import/a-z/wiesbaden-unter-nassauischer-herrschaft',
      'Geisa_Rasdorf':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; ../HISTORICAL_EVIDENCE.md',
      'Dermbach':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://www.dermbach.de/kultur-freizeit/schloss-dermbach',
      'Herbstein':'../EVIDENCE/Hessen_1789_Uhlhorn.jpg; https://lagis.hessen.de/de/orte/burgen-schloesser-herrenhaeuser/alle-eintraege/14639_burg-herbstein'}
    names={'Saarbruecken_Ottweiler':'Nassau-Sarrebruck : Sarrebruck–Ottweiler','Hadamar_Ellar':'Nassau-Orange : Hadamar–Ellar','Diez':'Nassau-Orange : Diez','Loehnberg_Merenberg':'Nassau-Weilbourg : Merenberg–Löhnberg','Usingen_centre':'Nassau-Usingen : centre','Wiesbaden':'Nassau-Usingen : Wiesbaden','Geisa_Rasdorf':'Fulda : Geisa–Rasdorf','Dermbach':'Fulda : Dermbach','Herbstein':'Fulda : Herbstein'}
    inventory=[]
    for t in g['traces']:
        rows=[r for r in g['assignments'] if t['territory'] in r['territories'] and r['owner']!=r['previous_owner']]
        inventory.append(dict(Territoire=names[t['territory']],TAG=t['tag'],Classe='B',Statut='NOYAU_INSTALLE_FRANGES_OUVERTES',Avant=';'.join(sorted({r['previous_owner'] for r in rows})),Apres=t['tag'],Cellules=len(t['included']),State_ID=';'.join(sorted({r['state'] for r in rows})),RGB=';'.join(r['rgb'] for r in rows),Source=sources[t['territory']]))
    unresolved=[
      ('Nassau-Sarrebruck : périphérie et Sarrewerden','Le noyau de 15 cellules ne reconstitue ni le Warndt ni les possessions de Sarrewerden. Échanges France/Nassau de 1766/1770 et droits alsaciens distincts.','Confronter chaque frange à un état daté de 1776 ; ne pas attribuer les bandes tardives par couleur.','Carte Fabricius 1789 ; Stadtarchiv Saarbrücken'),
      ('Nassau-Orange : franges de Diez–Hadamar','Huit cellules intérieures installées ; communautés, Burbach, Villmar, Camberg et Nassau-ville non certifiées.','Généralisation intérieure seulement ; conserver les cellules voisines.','Fonds 171/172 ; carte Uhlhorn'),
      ('Nassau-Usingen : limites complémentaires','Usingen-centre et Wiesbaden ont des noyaux corrigés ; les résidus NAS ne deviennent pas historiquement certifiés. Burgschwalbach 1777 exclu.','Tracé détaillé des limites et droits de 1776 avant tout nouvel agrandissement.','Wiesbaden Stadtlexikon ; carte Uhlhorn'),
      ('Nassau-Weilbourg : Löhnberg et possessions dispersées','1773 : intégration des trois quarts restants de Löhnberg prouvée ; deux cellules intérieures ajoutées. Limites fines non cadastrales.','Ne pas importer Sayn-Hachenburg 1799, le Nassau partagé échangé en 1781 ou les compensations de 1803.','HHStAW fonds 163 ; Deutsche Biographie Karl Christian'),
      ('Hesse-Hombourg','Autonomie et rapports avec Darmstadt non traduits en souveraineté moteur ; petite enveloppe identifiable mais institution à recouper.','Aucun nouveau pays ou transfert automatique ; exclure Meisenheim 1816.','../R2/HISTORICAL_EVIDENCE_R2.md ; Uhlhorn'),
      ('Hanau-Münzenberg','Administration de Wilhelm depuis 1764 prouvée, pas une preuve suffisante d’État indépendant natif.','Conserver HEK ; résoudre le paragium et les limites avant un éventuel pays.','https://www.hanau.de/stadtentwicklung/geschichte/geschichtsdaten/index.html'),
      ('Hesse-Rotenbourg / branches dispersées / Hanau-Lichtenberg','Droits réservés et possessions éloignées insuffisamment délimités ; aucune indépendance déduite du nom dynastique.','Conserver propriétaires et historiques actuels.','../R2/UNRESOLVED_R2.csv'),
      ('Fulda : franges','Geisa–Rasdorf, Dermbach et Herbstein corrigés par intérieurs B, pas toute la Rhön. Distances aux rivières non prises pour des erreurs GPS de villes.','Ne pas modifier Erfurt–Eichsfeld ni les noyaux T/U ; conserver les autres franges.','GEOMETRY.json ; SOURCE_ALIGNMENT hérités'),
      ('Démographie et économie','Allocations techniques par profils conservés, pas des populations historiques de 1776. NSB ne reçoit aucune usine arbitraire.','Tester subsistance, emploi, accès au marché et localisation visuelle du hub minier de Rhénanie.','ALLOCATION.json ; VALIDATION_R2B.json'),
      ('Drapeau et capitales','NSB réutilise les armes nassoviennes simplifiées ; capitale technique STATE_RHINELAND, pas déplacement des locators communs.','Le drapeau n’est pas une restitution complète du pavillon ; contrôler le prince et les titres en jeu.','common/flag_definitions/1776_map2w_r2b_saarbruecken.txt'),
      ('Titulatures Nassau de R2-A','Les gouvernements antérieurs sont conservés. Le rang principality ne garantit pas le titre prince avec les filtres européens vanilla.','Contrôler NAS/NOU/NWB en jeu avant une correction institutionnelle séparée ; NSB a un gouvernement princier borné.','C:/Games/Victoria 3/game/common/government_types/01_monarchies.txt:2876; R2/REPORT.md')]
    for name,problem,action,source in unresolved[:8]:inventory.append(dict(Territoire=name,TAG=None,Classe='C',Statut='FRANGE_OU_INSTITUTION_DIFFEREE',Avant=None,Apres=None,Cellules=0,State_ID=None,RGB=None,Source=source))
    add=lambda filename,rows:tables.update({filename:dict(fields=list(rows[0]),rows=rows)})
    add('INVENTORY_1776_R2B.csv',inventory)
    add('DISCREPANCIES_R2B.csv',[dict(Territoire=r['Territoire'],Classe=r['Classe'],Avant=r['Avant'],Apres=r['Apres'],Cellules=r['Cellules'],Etat=r['Statut'],Justification='Souveraineté recoupée et intérieur tracé, sans reprendre les noyaux précédents' if r['Classe']=='B' else 'Limite ou institution non résolue ; aucune attribution inventée',Source=r['Source']) for r in inventory])
    add('UNRESOLVED_R2B.csv',[dict(Territoire=n,Probleme=p,Action=act,Source=src) for n,p,act,src in unresolved])
    changes=[];ids={'STATE_HESSE':None,'STATE_RHINELAND':None,'STATE_SAXONY':None};population_by_rgb=C.Counter();allocation_details=[]
    for p in alloc['profiles']:
        for tag,amount in p['after'].items():
            if tag==p['source'] or not amount:continue
            shares={r['rgb']:r['pixels'] for r in g['assignments'] if r['state']==p['state'] and r['previous_owner']==p['source'] and r['owner']==tag}
            parts=core.allocate(amount,shares);population_by_rgb.update(parts);allocation_details.append(dict(state=p['state'],source=p['source'],owner=tag,culture=p['culture'],religion=p['religion'],amount=amount,by_rgb=parts))
    dump('TERRITORY_POPULATION_DETAIL.json',dict(method='Diagnostic subdivision of already conserved profile transfers by accepted cell shares; not a census or separate runtime pop geography',population_by_rgb=dict(population_by_rgb),profiles=allocation_details))
    # Read numerical IDs from effective definitions, never assume the label's number.
    for p in core.qa.effective(ROOT,core.qa.GAME,'map_data/state_regions'):
        for n in core.cw.parse(p.read_text(encoding='utf-8-sig')):
            if n.key in ids:ids[n.key]=int(n.one('id'))
    for r in g['assignments']:
        source='; '.join(sources[t] for t in r['territories']);changes.append(dict(Type='TRANSFERT' if r['owner']!=r['previous_owner'] else 'RESIDU_TECHNIQUE',Territoire='; '.join(names[t] for t in r['territories']) or 'Résidu non certifié',Avant=r['previous_owner'],Apres=r['owner'],State_ID=r['state'],ID_numerique=ids[r['state']],RGB_avant=r['parent_rgb'],RGB_apres=r['rgb'],Cellules=r['pixels'],Population=population_by_rgb[r['rgb']] if r['owner']!=r['previous_owner'] else None,Classe=r['confidence'],Batiments='Aucun transfert : niveaux/PM/propriétaires conservés',Ressources='Aucun changement de plafond ni de type ; terrain hérité',Source=source or 'GEOMETRY.json'))
    for row in alloc['profiles']:
        for tag,n in row['after'].items():
            if tag==row['source'] or not n:continue
            changes.append(dict(Type='POPULATION_PAR_PROFIL',Territoire=row['culture']+' / '+row['religion'],Avant=row['source'],Apres=tag,State_ID=row['state'],ID_numerique=ids[row['state']],RGB_avant=None,RGB_apres=None,Cellules=None,Population=n,Classe='TECHNIQUE_NON_RECENSEMENT',Batiments='Conservés chez le donneur',Ressources='Inchangées',Source='ALLOCATION.json'))
    changes.append(dict(Type='PAYS_ET_INSTITUTION',Territoire='Nassau-Sarrebruck : Ludwig, né le 3 janvier 1745',Avant='Absent',Apres='NSB',State_ID='STATE_RHINELAND',ID_numerique=ids['STATE_RHINELAND'],RGB_avant=None,RGB_apres=None,Cellules=15,Population=v['country_populations']['NSB'],Classe='A_INSTITUTION_B_GEOMETRIE',Batiments='Aucun bâtiment créé',Ressources='Inchangées',Source='HISTORICAL_EVIDENCE_R2B.md'))
    add('CHANGES_R2B.csv',changes);dump('CSV_TABLES.json',tables);dump('INVENTORY_RECEIPT.json',dict(scope='Targeted continuation of current state, not a second German audit',baseline_sha256=core.sha(OUT/'BASELINE.json'),already_installed_checked=['MAP2L Franconia/Rhine/Westphalia/Swabia','MAP2M/N/O/Q/R/S/T/U','MAP2W-R1','MAP2W-R2-A'],entries=len(inventory),census_claimed=False));print({name:len(t['rows']) for name,t in tables.items()},flush=True)
def tests():
    import io,time,unittest
    groups={'R2B_current':['test_map2w_r2b_completion'],'cumulative_current_contracts':['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon'],'preserved_delivery_snapshots':['test_map2w_west_south','test_map2w_r2_hesse_nassau'],'earlier_stage_snapshots':['test_map2t_saxony','test_map2u_thuringia']};results={}
    for name,modules in groups.items():
        stream=io.StringIO();start=time.monotonic();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestLoader().loadTestsFromNames(modules));results[name]=dict(modules=modules,tests=r.testsRun,failures=[test.id() for test,_ in r.failures],errors=[test.id() for test,_ in r.errors],seconds=round(time.monotonic()-start,2),output=stream.getvalue());print(name,r.testsRun,'failures',len(r.failures),'errors',len(r.errors),flush=True)
    dump('TESTS_R2B.json',results)
    if any(results[k]['failures'] or results[k]['errors'] for k in ['R2B_current','cumulative_current_contracts','preserved_delivery_snapshots']):raise SystemExit(1)
def csv_verify():
    import csv
    results=[]
    for name,t in load('CSV_TABLES.json').items():
        p=OUT/name;assert p.read_bytes().startswith(b'\xef\xbb\xbf')
        with p.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);rows=list(reader);assert reader.fieldnames==t['fields']
        assert len(rows)==len(t['rows'])
        for got,expected in zip(rows,t['rows']):assert got=={k:'' if expected[k] is None else str(expected[k]) for k in t['fields']}
        results.append(dict(file=name,records=len(rows),status='PASS_EVERY_CELL_REREAD',sha256=core.sha(p)))
    dump('CSV_REREAD.json',results);print(results,flush=True)
def tidy():
    files=load('EXPECTED_TEXT.json');changed={}
    for rel,numbers in {'common/history/pops/00_west_europe.txt':[1930,3521,3611,3709,3752,3804],'common/history/states/00_states.txt':[8057]}.items():
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert raw==files[rel];lines=raw.splitlines(keepends=True)
        for n in numbers:assert lines[n-1].strip()=='';lines[n-1]='\n'
        changed[rel]=''.join(lines)
    files.update(changed);dump('EXPECTED_TEXT.json',files);core.OUT=OUT;core.emit(changed,'WHITESPACE.patch')
def references():
    needed={'common/technology/technologies':set(),'common/laws':set(),'common/scripted_effects':{'change_to_hereditary','post_change_to_hereditary'},'common/cultures':{'south_german'},'common/religions':{'protestant'},'common/interest_groups':{'ig_landowners'},'common/ideologies':{'ideology_traditionalist'},'common/government_types':{'gov_aor1776_map2w_r2b_saarbruecken'},'common/coat_of_arms/coat_of_arms':{'aor1776_map2w_r2_nassau'}}
    raw=(ROOT/'common/history/countries/nsb - map2w_r2b.txt').read_text(encoding='utf-8-sig')
    for n in core.cw.walk(core.cw.parse(raw)):
        if n.key=='add_technology_researched':needed['common/technology/technologies'].add(n.value)
        if n.key=='activate_law':needed['common/laws'].add(n.value.removeprefix('law_type:'))
        if n.key.startswith('effect_starting_'):needed['common/scripted_effects'].add(n.key)
    found={}
    for folder,keys in needed.items():
        hits={}
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            if not p.is_file() or p.suffix!='.txt':continue
            for n in core.cw.parse(p.read_text(encoding='utf-8-sig')):
                if n.key in keys:hits[n.key]=p.as_posix()
        assert set(hits)==keys,(folder,keys-set(hits));found[folder]=hits
    for lang in ['french','english']:
        p=core.qa.GAME/'localization'/lang/('government_l_'+lang+'.yml');assert p.is_file() and 'gov_principality_desc:' in p.read_text(encoding='utf-8-sig')
    dump('REFERENCE_VALIDATION_R2B.json',dict(status='PASS',references=found,canonical_game='C:/Games/Victoria 3/game',installed_executable_version='1.13.11',runtime_execution=False));print('Effective references validated',flush=True)
def close():
    """Attach delivery checks without rewriting any prior MAP baseline."""
    v=load('VALIDATION_R2B.json');assert v['passed']==v['total'];tests=load('TESTS_R2B.json');refs=load('REFERENCE_VALIDATION_R2B.json');csv=load('CSV_REREAD.json');earlier=load('EARLIER_TEST_COMPARISON.json')
    assert not earlier['new_failure_identifiers'];assert all(not tests[k]['failures'] and not tests[k]['errors'] for k in ['R2B_current','cumulative_current_contracts','preserved_delivery_snapshots']);assert refs['status']=='PASS' and len(csv)==4
    for row in csv:assert core.sha(OUT/row['file'])==row['sha256']
    g=load('GEOMETRY.json');transfers=[r for r in g['assignments'] if r['owner']!=r['previous_owner']];assert sum(r['pixels'] for r in transfers)==45
    v.update(tests={k:{field:r[field] for field in ['tests','failures','errors']} for k,r in tests.items()},prior_stage_failure_comparison=earlier['status'],reference_validation='PASS',csv_validation='PASS_EVERY_CELL_REREAD',cartographic_visual_review='SOURCE_CELL_FOOTPRINTS_AND_OUTPUT_MAPS_REVIEWED_NOT_RUNTIME',csv_preview_review='FOUR_SHEETS_RENDERED_AND_REVIEWED',manifest_note='30 runtime files, plus registry/migration, narrow guard, tools and reports; external USA/DMC files excluded.',territorial_transfers=dict(C.Counter({tag:sum(r['pixels'] for r in transfers if r['owner']==tag) for tag in ['NSB','NOU','NWB','NAS','FUL']})),new_RGBs=len(g['new_provinces']),registered_RGBs=567)
    dump('VALIDATION_R2B.json',v)
    source=OUT/'EVIDENCE/Saarbruecken_1789_Fabricius_1909.jpg';dump('EVIDENCE/SAAR_SOURCE_METADATA.json',dict(title='Die Grafschaft Saarbruecken und ihre Nachbargebiete im Jahre 1789',publisher='F. Wirtz, Darmstadt',publication_year=1909,represented_year=1789,cartographic_authority='W. Fabricius; historical atlas of the Rhine province, maps VI/VII',institution='Bibliotheque nationale de France, GE D-27288',catalogue='https://catalogue.bnf.fr/ark:/12148/cb40574057q',gallica='https://gallica.bnf.fr/ark:/12148/btv1b53079451h',download_source='Wikimedia Commons facsimile from Gallica btv1b53079451h',sha256=core.sha(source),image_size=list(Image.open(source).size),interpretation='Only inward cores with independently corroborated dynastic continuity, not all 1789 borders'))
    print('Delivery checks attached, no runtime validation claimed',flush=True)
if __name__=='__main__':globals()[sys.argv[1]]()
