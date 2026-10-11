"""MAP-2C: immutable baseline, local native-map previews and focused checks."""
from pathlib import Path
import collections as C
import hashlib, json, re, sys
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective, values, prov

ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2C'
GAME=qa.GAME
E=OUT/'MAP2C_GEOGRAPHIC_EVIDENCE'
BASE=OUT/'MAP2C_BASELINE.json'
BOXES={'provence':(4180,995,4250,1060), 'venice':(4290,935,4425,1030)}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def source_bitmap():
    p=ROOT/'map_data/provinces.png'
    return p if p.exists() else GAME/'map_data/provinces.png'
def packed(p):
    a=np.array(Image.open(p).convert('RGB'), dtype=np.uint32)
    return (a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]
def snapshot():
    assert not BASE.exists(), 'Do not replace the actual dirty-tree baseline'
    OUT.mkdir(parents=True,exist_ok=True); E.mkdir(exist_ok=True)
    folders=['common','map_data','gfx','localization','events','.metadata',
             'docs/reports/map/MAP1C','docs/reports/map/MAP2A','docs/reports/map/MAP2B',
             'docs/reports/historical_workforce_revision_1776']
    hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
    paths=['common/scripted_effects/1776_alpine_state_names.txt',
           'common/on_actions/12_1776_alpine_state_names.txt',
           'common/dynamic_country_names/00_dynamic_country_names.txt',
           'localization/french/1776_alpine_state_names_l_french.yml',
           'localization/english/1776_alpine_state_names_l_english.yml']
    original={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in paths}
    # Byte-exact snapshot of the effective map, even when it is inherited vanilla.
    bmp=source_bitmap(); data=bmp.read_bytes(); (E/'provinces_before.png').write_bytes(data)
    BASE.write_text(json.dumps({'hashes':hashes,'originals':original,'inventory':qa.inventory(),
        'bitmap_source':str(bmp),'bitmap_hash':sha(bmp),'native_test':'NOT_RUN'},ensure_ascii=False),encoding='utf-8')
    print('Baseline:',len(hashes),'protected files; effective bitmap',sha(bmp))

def geo_data():
    defs={}; hubs={}; names={}
    for p in effective(ROOT,GAME,'map_data/state_regions'):
        for s in cw.parse(p.read_text(encoding='utf-8-sig')):
            defs[s.key]=[prov(v) for v in values(s,'provinces')]
            hubs[s.key]={k:prov(s.one(k)) for k in ['city','port','farm','wood','mine'] if s.children(k)}
    for p in [GAME/'localization/english/hub_names_l_english.yml']:
        for key,val in re.findall(r'^\s*(HUB_NAME_STATE_\w+):\d*\s*"([^"]*)"',p.read_text(encoding='utf-8-sig'),re.M): names[key]=val
    return defs,hubs,names

def preview(label='before',bitmap=None):
    OUT.mkdir(parents=True,exist_ok=True); E.mkdir(exist_ok=True)
    rgb=packed(bitmap or source_bitmap()); inv=qa.inventory(); defs,hubs,names=geo_data()
    owners={r['key'][0]:r['key'][2] for r in inv['owners']}
    byrgb={v:s for s,vs in defs.items() for v in vs}
    colors={'FRA':(78,130,192),'PAP':(240,210,96),'SAR':(85,181,164),
            'VEN':(192,86,85),'AUS':(190,180,203),'SWI':(165,182,116),'MOD':(140,167,94),'PAR':(125,156,94)}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    for case,box in BOXES.items():
        x0,y0,x1,y1=box; crop=rgb[y0:y1,x0:x1]; canvas=np.zeros((*crop.shape,3),dtype=np.uint8)
        locs=[]
        for c in np.unique(crop):
            v='x%06X'%int(c); tag=owners.get(v,'SEA'); sid=byrgb.get(v,'')
            mask=crop==c; canvas[mask]=colors.get(tag,(52,65,74) if tag=='SEA' else (110,116,95))
            ys,xs=np.where(mask)
            if len(xs)>=8: locs.append((v,tag,sid,float(xs.mean()),float(ys.mean()),int(len(xs))))
        # Province boundaries are technical subdivisions, not all sovereign boundaries.
        bd=np.zeros(crop.shape,dtype=bool); bd[1:]|=crop[1:]!=crop[:-1]; bd[:,1:]|=crop[:,1:]!=crop[:,:-1]
        canvas[bd]=(35,40,45)
        scale=9; im=Image.fromarray(canvas).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
        d=ImageDraw.Draw(im)
        for v,tag,sid,x,y,count in locs:
            if sid in (['STATE_PROVENCE','STATE_RHONE','STATE_LANGUEDOC'] if case=='provence' else ['STATE_VENETIA','STATE_LOMBARDY','STATE_ISTRIA','STATE_SOUTH_TYROL']):
                d.text((x*scale,y*scale),v+' '+tag,fill='white',stroke_width=1,stroke_fill='black',font=font,anchor='mm')
        # Physical locator positions, never province centroids labelled as cities.
        for kind in ['city','port','farm','wood','mine']:
            path=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
            pos={ident:(float(x),3616-float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',path.read_text(encoding='utf-8-sig'))}
            for sid,hh in hubs.items():
                if kind not in hh: continue
                sid_id=next((str(s.one('id')) for p in effective(ROOT,GAME,'map_data/state_regions') for s in cw.parse(p.read_text(encoding='utf-8-sig')) if s.key==sid),None) if sid in ['STATE_PROVENCE','STATE_VENETIA','STATE_ISTRIA','STATE_LOMBARDY','STATE_SOUTH_TYROL'] else None
                if sid_id not in pos: continue
                x,y=pos[sid_id]
                if not (x0<=x<x1 and y0<=y<y1): continue
                xx,yy=(x-x0)*scale,(y-y0)*scale
                txt=names.get('HUB_NAME_'+sid+'_'+kind,kind)
                d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=(255,245,150))
                d.text((xx,yy+15),txt,fill=(255,245,150),stroke_width=1,stroke_fill='black',font=font,anchor='mm')
        im.save(E/(case+'_'+label+'.png'))
        (E/(case+'_'+label+'_rgb.json')).write_text(json.dumps(locs,ensure_ascii=False,indent=2),encoding='utf-8')
        print(case,label,len(locs),'RGB')

def physical():
    E.mkdir(parents=True,exist_ok=True)
    river=Image.open(GAME/'map_data/rivers.png').convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for case,box in BOXES.items():
        x0,y0,x1,y1=box; scale=9
        im=river.crop(box).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        for x in range(x0,x1,5):
            xx=(x-x0)*scale;d.line((xx,0,xx,im.height),fill=(190,190,190));d.text((xx+2,0),str(x),font=font,fill='black')
        for y in range(y0,y1,5):
            yy=(y-y0)*scale;d.line((0,yy,im.width,yy),fill=(190,190,190));d.text((0,yy+2),str(y),font=font,fill='black')
        im.save(E/(case+'_physical_grid.png'))

def propose():
    before=packed(E/'provinces_before.png'); after=before.copy(); changes=[]
    # Reuse existing province identities. No new RGB, owner selector, State Region or TAG.
    x0,y0,x1,y1=BOXES['provence']; local=before[y0:y1,x0:x1]; cut=after[y0:y1,x0:x1]
    pap=int('B0C0E0',16); north=int('C03918',16)
    polygon=[(4205,1029),(4205,1027),(4208,1026),(4210,1024),(4211,1021),
             (4214,1020),(4217,1022),(4219,1025),(4219,1029),(4217,1032),
             (4215,1034),(4212,1036),(4209,1036),(4206,1034)]
    image=Image.new('1',(x1-x0,y1-y0)); ImageDraw.Draw(image).polygon([(x-x0,y-y0) for x,y in polygon],fill=1)
    wanted=np.array(image,dtype=bool)&np.isin(local,[pap,north])
    # A trimmed part joins the nearest adjacent original French province in Provence.
    french=[int(v,16) for v in ['31C0DF','C03918','B040E0']]
    seed=np.isin(local,french)
    retired=(local==pap)&~wanted
    points=np.argwhere(seed)
    for y,x in np.argwhere(retired):
        sy,sx=points[np.argmin(((points-[y,x])**2).sum(axis=1))]
        cut[y,x]=local[sy,sx]
    cut[wanted]=pap
    # Keep the French subdivisions contiguous after clipping the Comtat perimeter.
    # Small detached pieces of the northern French RGB join an adjacent French RGB.
    points=set(map(tuple,np.argwhere(cut==north))); groups=[]
    while points:
        p=points.pop(); group={p}; todo=[p]
        while todo:
            y,x=todo.pop()
            for q in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if q in points: points.remove(q);group.add(q);todo.append(q)
        groups.append(group)
    groups.sort(key=len,reverse=True)
    for group in groups[1:]:
        adjacent=C.Counter()
        for y,x in group:
            for sy,sx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if 0<=sy<cut.shape[0] and 0<=sx<cut.shape[1] and int(cut[sy,sx]) in [french[0],french[2]]:
                    adjacent[int(cut[sy,sx])]+=1
        # A tiny enclosed remnant inside the new papal outline joins that outline.
        if not adjacent:
            assert any(cut[sy,sx]==pap for y,x in group for sy,sx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)])
        target=adjacent.most_common(1)[0][0] if adjacent else pap
        for y,x in group: cut[y,x]=target
    # The first clipping can also detach another French RGB. Regrow detached
    # pieces only from the retained connected cores, instead of Euclidean jumps.
    for color in french:
        points=set(map(tuple,np.argwhere(cut==color))); groups=[]
        while points:
            p=points.pop(); group={p}; todo=[p]
            while todo:
                y,x=todo.pop()
                for q in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                    if q in points: points.remove(q);group.add(q);todo.append(q)
            groups.append(group)
        groups.sort(key=len,reverse=True)
        for group in groups[1:]:
            for y,x in group: cut[y,x]=0
    todo=C.deque(map(tuple,np.argwhere(np.isin(cut,french))))
    while todo:
        y,x=todo.popleft()
        for sy,sx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
            if 0<=sy<cut.shape[0] and 0<=sx<cut.shape[1] and cut[sy,sx]==0:
                cut[sy,sx]=cut[y,x];todo.append((sy,sx))
    cut[cut==0]=pap
    x0,y0,x1,y1=BOXES['venice']; local=before[y0:y1,x0:x1]; cut=after[y0:y1,x0:x1]
    # Udine west of the simplified border; Gorizia/Gradisca and Trieste remain AUS.
    yy,xx=np.indices(local.shape); xx+=x0; yy+=y0
    border=np.where(yy<970,4410,np.where(yy<975,4411,np.where(yy<979,4410,4408)))
    mask=(local==int('56C78A',16))&(xx<border)
    cut[mask]=int('108021',16)
    delta=before!=after
    for old,new in sorted(set(zip(before[delta].tolist(),after[delta].tolist()))):
        ys,xs=np.where((before==old)&(after==new))
        changes.append({'old_rgb':'x%06X'%old,'new_rgb':'x%06X'%new,'pixels':int(len(xs)),
                        'bbox':[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]})
    a=np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=2).astype(np.uint8)
    Image.fromarray(a).save(E/'provinces_proposed.png')
    data={'changes':changes,'changed_pixels':int(delta.sum()),'comtat_polygon_game_pixels':polygon,
          'method':'Documented game-scale simplification; physical river and locality review, not a cadastral georeferencing',
          'no_population_by_pixel':'Populations are keyed by owner/State Region and stay exactly unchanged.'}
    (E/'GEOMETRY_CHANGES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    preview('proposed',E/'provinces_proposed.png')
    print(json.dumps(data,ensure_ascii=False))

def patch_inputs():
    baseline=json.loads(BASE.read_text(encoding='utf-8'))
    target=OUT/'MAP2C_PATCH_INPUTS.json'
    assert not target.exists(), 'Keep original patch inputs'
    paths=['common/country_definitions/00_countries.txt','map_data/state_regions/01_south_europe.txt']
    for p in paths: assert sha(ROOT/p)==baseline['hashes'][p], p
    target.write_text(json.dumps({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in paths},ensure_ascii=False),encoding='utf-8')
    print('Additional original inputs preserved')

def components(array,color):
    yy,xx=np.where(array==color)
    points=set(zip(yy.tolist(),xx.tolist())); sizes=[]
    while points:
        first=points.pop(); todo=[first]; size=1
        while todo:
            y,x=todo.pop()
            for nextp in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if nextp in points: points.remove(nextp);todo.append(nextp);size+=1
        sizes.append(size)
    return sorted(sizes,reverse=True)

def geometry_check():
    before=packed(E/'provinces_before.png'); after=packed(E/'provinces_proposed.png')
    assert before.shape==after.shape==(3616,8192)
    assert np.array_equal(np.unique(before),np.unique(after)), 'Province identities changed'
    delta=before!=after
    expected=json.loads((E/'GEOMETRY_CHANGES.json').read_text(encoding='utf-8'))
    assert int(delta.sum())==expected['changed_pixels']
    defs,_,_=geo_data(); byrgb={int(v[1:],16):s for s,vs in defs.items() for v in vs}
    changes=json.loads((E/'GEOMETRY_CHANGES.json').read_text(encoding='utf-8'))['changes']
    for r in changes:
        old,new=int(r['old_rgb'][1:],16),int(r['new_rgb'][1:],16)
        assert byrgb[old]==byrgb[new] in ['STATE_PROVENCE','STATE_ISTRIA']
    topology={}
    for c in set(before[delta].tolist()+after[delta].tolist()):
        a,b=components(before,c),components(after,c)
        topology['x%06X'%c]={'before_components':a,'after_components':b}
        assert len(b)<=len(a), ('New disconnected fragment',c,a,b)
    assert int(after[1034,4209])==int('B0C0E0',16), 'Avignon lost'
    assert int(after[968,4405])==int('108021',16), 'Udine not Venetian'
    assert int(after[977,4414])==int('56C78A',16), 'Gorizia lost'
    return {'dimensions':[8192,3616],'province_colors':int(len(np.unique(after))),
            'changed_pixels':int(delta.sum()),'connectivity':topology,'changes':changes}

def apply_bitmap():
    result=geometry_check()
    assert sha(source_bitmap())==json.loads(BASE.read_text(encoding='utf-8'))['bitmap_hash']
    shutil.copyfile(E/'provinces_proposed.png',ROOT/'map_data/provinces.png')
    print('Native semantic map applied:',result['changed_pixels'],'pixels')

def validate():
    baseline=json.loads(BASE.read_text(encoding='utf-8')); before=baseline['inventory']; after=qa.inventory()
    allowed={
        'common/country_definitions/00_countries.txt','map_data/state_regions/01_south_europe.txt',
        'common/scripted_effects/1776_alpine_state_names.txt',
        'localization/french/1776_alpine_state_names_l_french.yml',
        'localization/english/1776_alpine_state_names_l_english.yml',
        'localization/french/replace/1776_map2c_l_french.yml',
        'localization/english/replace/1776_map2c_l_english.yml','map_data/provinces.png',
        'common/history/treaties/1776_avignon_transit_rights.txt'}
    changed=[]
    for p,h in baseline['hashes'].items():
        if not (ROOT/p).exists() or sha(ROOT/p)!=h:
            assert p in allowed, 'Unrelated file changed: '+p
            changed.append(p)
    new=[]
    for f in ['common','map_data','gfx','localization','events','.metadata']:
        for p in (ROOT/f).rglob('*'):
            if p.is_file() and p.relative_to(ROOT).as_posix() not in baseline['hashes']:
                rel=p.relative_to(ROOT).as_posix(); assert rel in allowed, 'Unexpected new runtime file: '+rel
                new.append(rel)
    for k in before:
        if k!='countries': assert before[k]==after[k], 'Inventory changed: '+k
    oldcountries=before['countries']; newcountries=after['countries']
    assert set(oldcountries)==set(newcountries)
    assert all(oldcountries[c]==newcountries[c] for c in oldcountries if c!='VEN')
    ven=json.loads(oldcountries['VEN'])
    for n in ven[2]:
        if n[0]=='is_named_from_capital': assert n[2]=='yes';n[2]='no'
    assert json.dumps(ven,ensure_ascii=False,separators=(',',':'))==newcountries['VEN']
    inputs=json.loads((OUT/'MAP2C_PATCH_INPUTS.json').read_text(encoding='utf-8'))
    original=cw.parse(inputs['map_data/state_regions/01_south_europe.txt'])
    current=cw.parse((ROOT/'map_data/state_regions/01_south_europe.txt').read_text(encoding='utf-8-sig'))
    oldnorm=[qa.norm(n) for n in original]; newnorm=[qa.norm(n) for n in current]
    for n in oldnorm:
        if n[0]=='STATE_ISTRIA':
            for child in n[2]:
                if child[0]=='mine': assert child[2]=='x56C78A';child[2]='x108021'
    assert oldnorm==newnorm, 'State definition changed beyond mine RGB'
    script=(ROOT/'common/scripted_effects/1776_alpine_state_names.txt').read_text(encoding='utf-8-sig')
    cw.parse(script)
    oldscript=cw.parse(baseline['originals']['common/scripted_effects/1776_alpine_state_names.txt'])[0]
    currentscript=cw.parse(script)[0]
    # Existing Lombardy, Tyrol and Istria logic remains byte-independent AST-identical.
    oldbranches=oldscript.children('if')[0].children()
    newbranches=currentscript.children('if')[1].children()
    assert [qa.norm(n) for n in oldbranches]==[qa.norm(n) for n in newbranches[:-1]]
    names=set(re.findall(r'set_state_name\s*=\s*(\w+)',script))
    for lang in ['french','english']:
        loc=ROOT/f'localization/{lang}/1776_alpine_state_names_l_{lang}.yml'
        assert loc.read_bytes().startswith(b'\xef\xbb\xbf'), 'Localization BOM missing: '+str(loc)
        text=loc.read_text(encoding='utf-8-sig')
        keys=set(re.findall(r'^\s*(\w+):\d+',text,re.M)); assert names<=keys
        replace=ROOT/f'localization/{lang}/replace/1776_map2c_l_{lang}.yml'
        assert replace.read_bytes().startswith(b'\xef\xbb\xbf')
        assert len(re.findall(r'^\s*dyn_c_venice_republic:',replace.read_text(encoding='utf-8-sig'),re.M))==1
        assert 'treaty_1776_avignon_transit_rights:' in replace.read_text(encoding='utf-8-sig')
    treaty_path=ROOT/'common/history/treaties/1776_avignon_transit_rights.txt'
    treaty=cw.parse(treaty_path.read_text(encoding='utf-8-sig'))[0].children('create_treaty')
    assert len(treaty)==1
    treaty=treaty[0]
    assert treaty.one('first_country')=='c:FRA' and treaty.one('second_country')=='c:PAP'
    assert treaty.one('entered_into_force_on')=='1776.1.1' and treaty.one('is_draft')=='no'
    articles=treaty.children('articles_to_create')[0].children()
    assert len(articles)==1 and articles[0].one('article')=='transit_rights'
    assert articles[0].one('source_country')=='c:FRA' and articles[0].one('target_country')=='c:PAP'
    all_transit=[]
    for p in effective(ROOT,GAME,'common/history/treaties'):
        for n in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))):
            if n.children('article') and n.one('article')=='transit_rights':
                if n.one('source_country')=='c:FRA' and n.one('target_country')=='c:PAP': all_transit.append(str(p))
    assert len(all_transit)==1, 'Duplicate FRA -> PAP transit article'
    article_text=(GAME/'common/treaty_articles/24_transit_rights.txt').read_text(encoding='utf-8-sig')
    assert 'is_transit_rights' in article_text and 'maintenance_paid_by = target_country' in article_text
    assert sha(ROOT/'map_data/provinces.png')==sha(E/'provinces_proposed.png')
    geometry=geometry_check()
    # Inspect the actual engine locator, not a labelled province centroid.
    locator_rows=[]; a=packed(E/'provinces_before.png'); b=packed(ROOT/'map_data/provinces.png')
    defs,hubs,_=geo_data(); ids={'STATE_PROVENCE':'29','STATE_ISTRIA':'118','STATE_VENETIA':'114'}
    # Venetia's actual ID is read from effective definitions rather than assumed.
    for p in effective(ROOT,GAME,'map_data/state_regions'):
        for n in cw.parse(p.read_text(encoding='utf-8-sig')):
            if n.key in ids: ids[n.key]=str(n.one('id'))
    for kind in ['city','port','farm','wood','mine']:
        path=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        pos={ident:(float(x),3616-float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',path.read_text(encoding='utf-8-sig'))}
        for sid,ident in ids.items():
            if ident not in pos or kind not in hubs[sid]: continue
            x,y=pos[ident]; old='x%06X'%int(a[int(y),int(x)]); newrgb='x%06X'%int(b[int(y),int(x)])
            if old!=newrgb: assert (sid,kind,old,newrgb)==('STATE_ISTRIA','mine','x56C78A','x108021')
            locator_rows.append({'region':sid,'kind':kind,'pixel':[x,y],'before_rgb':old,'after_rgb':newrgb,
                'definition_rgb':hubs[sid][kind],'matches':newrgb==hubs[sid][kind]})
    (E/'ENGINE_LOCATOR_CHECK.json').write_text(json.dumps(locator_rows,ensure_ascii=False,indent=2),encoding='utf-8')
    world_before=sum(r['count'] for r in before['pops']);world_after=sum(r['count'] for r in after['pops'])
    region_totals=C.Counter()
    targets={'STATE_PROVENCE','STATE_ISTRIA','STATE_VENETIA','STATE_LOMBARDY','STATE_SOUTH_TYROL'}
    pop_rows=[]
    for r in before['regional_pop']:
        sid,tag,cu,rel=r['key']
        if sid in targets:
            pop_rows.append([sid,tag,cu,rel,r['count'],r['count'],0])
            region_totals[sid+'|'+tag]+=r['count']
    data={'population':pop_rows,'region_totals':dict(region_totals),'geometry':geometry}
    (OUT/'TABLE_DATA.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    result={'phase':'MAP-2C','static_status':'PASS','native_game_test':'NOT_RUN',
        'runtime_files_changed':sorted(changed+new),'protected_files_checked':len(baseline['hashes']),
        'protected_files_unchanged':len(baseline['hashes'])-len(changed),
        'global_population_before':world_before,'global_population_after':world_after,'population_delta':world_after-world_before,
        'all_culture_religion_owner_region_groups_exactly_preserved':True,
        'all_building_commands_and_written_levels_exactly_preserved':True,'all_units_and_recruitment_exactly_preserved':True,
        'all_owner_rgb_selectors_and_state_regions_preserved':True,'unrelated_country_definitions_preserved':True,
        'all_previous_report_files_and_unrelated_runtime_hashes_preserved':True,
        'no_new_reference_errors':True,'preexisting_reference_errors':before['errors'],
        'preexisting_duplicate_province_assignments':len(before['duplicates']),
        'geometry':geometry,'engine_locators':locator_rows,'no_commit_merge_push_executed':True,
        'map_before_sha256':baseline['bitmap_hash'],'map_after_sha256':sha(ROOT/'map_data/provinces.png'),
        'transit_treaty':{'source':'FRA','target':'PAP','article':'transit_rights','starts':'1776.1.1',
            'duplicate_articles':0,'military_access_added':False,'binding_years':5,
            'effect':'Access to French world-market hubs; direct connection to the Latium domestic market is NOT guaranteed',
            'native_market_access_test':'NOT_RUN','vanilla_influence_maintenance':50}}
    (OUT/'MAP2C_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['static_status','native_game_test','runtime_files_changed','global_population_before','global_population_after','population_delta']}))

def comparisons():
    preview('before',E/'provinces_before.png')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for case in BOXES:
        a=Image.open(E/(case+'_before.png')); b=Image.open(E/(case+'_proposed.png'))
        image=Image.new('RGB',(a.width+b.width,a.height+95),(245,246,247));d=ImageDraw.Draw(image)
        d.text((12,8),'Avant MAP-2C',font=font,fill='black')
        d.text((a.width+12,8),'Apres MAP-2C',font=font,fill='black')
        image.paste(a,(0,40));image.paste(b,(a.width,40))
        legend='FRA bleu | PAP or | SAR turquoise' if case=='provence' else 'VEN rouge | AUS mauve | SWI vert | SAR turquoise'
        d.text((12,a.height+48),legend,font=small,fill='black')
        d.text((12,a.height+71),'Contours RGB techniques. Points = locators du jeu. Apercu hors jeu, pas une capture native.',font=small,fill='black')
        image.save(E/(case+'_comparison.png'))

if __name__=='__main__':
    if '--snapshot' in sys.argv: snapshot()
    if '--preview' in sys.argv: preview('before',E/'provinces_before.png')
    if '--physical' in sys.argv: physical()
    if '--propose' in sys.argv: propose()
    if '--patch-inputs' in sys.argv: patch_inputs()
    if '--check-geometry' in sys.argv: print(json.dumps(geometry_check()))
    if '--apply-bitmap' in sys.argv: apply_bitmap()
    if '--validate' in sys.argv: validate()
    if '--comparisons' in sys.argv: comparisons()
