"""Belgian HRE territorial lot. Stage data, emit text patches, audit before apply.

Boundaries are a declared game-resolution approximation of the historical atlas,
not a cadastral reconstruction. The frozen world bitmap is never overwritten.
"""
from pathlib import Path
import collections as C
import difflib
import json
import re
import shutil
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2b_patch import state, region, append
from map_1776_audit import values, effective
from map2l_hre_work import ROOT, OUT, sha

LOT=OUT/'BELGIUM'
REGIONS=['STATE_FLANDERS','STATE_WALLONIA']
TAGS=['LGE','STM']
COLORS={'BEO':(235,200,127),'LGE':(173,55,80),'STM':(99,141,160)}


def dump(name,obj):
    LOT.mkdir(parents=True,exist_ok=True)
    (LOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')


def packed(path):
    a=np.array(Image.open(path).convert('RGB'),dtype=np.uint32)
    return (a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]


def components(mask):
    ys,xs=np.where(mask)
    cells=set(zip(ys.tolist(),xs.tolist()));out=[]
    while cells:
        first=cells.pop();part=[first];todo=[first]
        while todo:
            y,x=todo.pop()
            for q in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if q in cells:cells.remove(q);todo.append(q);part.append(q)
        out.append(part)
    return sorted(out,key=lambda p:(-len(p),min(p)))


def geometry():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    assert sha(ROOT/'map_data/provinces.png')==base['bitmap_sha256'],'Live bitmap changed since baseline'
    before=packed(OUT/'SOURCE/provinces_before.png')
    atlas=Image.open(OUT/'EVIDENCE/1789_0160c_v2.jpg').convert('RGB')
    # Surveyed game locators matched to the two square capital symbols, read
    # on the ORIGINAL 3509 x 2481 atlas, not the UI-resized preview.
    game=np.array([[4200.894,831.743],[4223.577,839.778]])
    source=np.array([[1733.5,1096.0],[2370.5,1258.0]])
    dg=game[1]-game[0];ds=source[1]-source[0]
    a=float(ds@dg/(dg@dg));b=float((ds[1]*dg[0]-ds[0]*dg[1])/(dg@dg))
    transform=np.array([[a,b],[-b,a]])
    offset=source[0]-game[0]@transform
    # Similarity transform preserves the source's area ratios and proportions.
    # No radial buffer, dilation, snapping-to-city or minimum-size enlargement.
    box=(4142,804,4256,889);x0,y0,x1,y1=box
    yy,xx=np.indices((y1-y0,x1-x0));xy=np.stack([xx+x0+.5,yy+y0+.5],axis=-1)
    uv=xy@transform+offset
    src=np.asarray(atlas);u=np.floor(uv[:,:,0]).astype(int);v=np.floor(uv[:,:,1]).astype(int)
    valid=(u>=0)&(u<atlas.width)&(v>=0)&(v<atlas.height)
    samples=np.zeros((*xx.shape,3),dtype=np.int16);samples[valid]=src[v[valid],u[valid]].astype(np.int16)
    # Explicit atlas colour keys. Small-letter artefacts are suppressed by
    # a local source-space majority only; native pixels are never expanded.
    def colour_mask(center,tolerance):
        hits=np.zeros(xx.shape,dtype=np.int16)
        for du in [-14,0,14]:
          for dv in [-14,0,14]:
            uu=u+du;vv=v+dv;ok=(uu>=0)&(uu<atlas.width)&(vv>=0)&(vv<atlas.height)
            delta=np.full((*xx.shape,3),300,dtype=np.int16)
            delta[ok]=src[vv[ok],uu[ok]].astype(np.int16)-np.array(center,dtype=np.int16)
            hits+=(np.max(np.abs(delta),axis=2)<tolerance)
        return hits>=5
    liege=colour_mask([253,70,128],32)
    # Its pink-grey ink is close to France's: the polity's explicitly read
    # eastern atlas window excludes the unrelated French/Bouillon colour.
    stavelot=colour_mask([228,131,150],20)&(u>=2470)&(u<2780)&(v>=1310)&(v<1580)
    rows=[r for r in base['inventory']['owners'] if r['key'][1] in REGIONS]
    original={int(r['key'][0][1:],16):r for r in rows}
    local=before[y0:y1,x0:x1];scope=np.isin(local,list(original))
    owner=np.zeros(local.shape,dtype=np.uint8)
    owner[liege&scope]=1;owner[stavelot&scope]=2
    # The black capital square hides the territorial ink beneath the Liège
    # mine locator. The atlas explicitly names this point as Liège: do not
    # turn a printed symbol into an artificial Austrian enclave.
    owner[int(839.778)-y0,int(4223.577)-x0]=1
    abstracted=[]
    # One-pixel artefacts have no reliable extent at this resolution: keep the
    # neighbour's representation. Larger enclaves retain their actual size.
    for code in [1,2]:
        for part in components(owner==code):
            if len(part)<2:
                for y,x in part:owner[y,x]=0
                abstracted.append(dict(owner=TAGS[code-1],native_pixels=len(part),cells=[[x+x0,y+y0] for y,x in part]))
    after=before.copy();cut=after[y0:y1,x0:x1]
    used=set(np.unique(before).tolist());next_rgb=0xEDA100;assignments=[];children=[]
    # Preserve a province's native identity at its existing engine hub, if it
    # has one. Thus existing locators stay on their declared colour.
    import csv
    with (ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:
        hubs=[r for r in csv.DictReader(f) if r['State_ID'] in REGIONS]
    for old,row in sorted(original.items()):
        mask=local==old;groups=[]
        for code in [0,1,2]:
            for part in components(mask&(owner==code)):groups.append((code,part))
        old_hubs=[r for r in hubs if r['Defined_Hub_RGB']==row['key'][0]]
        preferred=None
        for h in old_hubs:
            p=(int(float(h['Locator_Y']))-y0,int(float(h['Locator_X']))-x0)
            for i,(code,part) in enumerate(groups):
                if p in part:
                    assert preferred is None or preferred==i,'Multiple hubs assigned to separate children'
                    preferred=i
        if preferred is None:preferred=max(range(len(groups)),key=lambda i:len(groups[i][1]))
        for i,(code,part) in enumerate(groups):
            rgb=old
            if i!=preferred:
                while next_rgb in used:next_rgb+=1
                rgb=next_rgb;next_rgb+=1;used.add(rgb)
                children.append(dict(rgb='x%06X'%rgb,parent_rgb=row['key'][0],terrain='INHERIT_PARENT'))
            tag='BEO' if code==0 else TAGS[code-1]
            for y,x in part:cut[y,x]=rgb
            assignments.append(dict(rgb='x%06X'%rgb,parent_rgb=row['key'][0],state=row['key'][1],
                before_owner='BEO',owner=tag,pixels=len(part),cells=[[x+x0,y+y0] for y,x in part]))
    assert all(any(r['owner']==tag for r in assignments) for tag in ['BEO',*TAGS])
    assert np.array_equal(after[~np.isin(before,list(original))],before[~np.isin(before,list(original))])
    assert not set(original)-set(np.unique(after).tolist()),'Original colour deleted'
    arr=np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=2).astype(np.uint8)
    LOT.mkdir(parents=True,exist_ok=True);Image.fromarray(arr).save(LOT/'provinces_candidate.png')
    summary=C.Counter()
    for r in assignments:summary[(r['state'],r['owner'])]+=r['pixels']
    # Namur's confluence is an independent rough reading, not a fitted point.
    check_game=np.array([4210.085,847.315]);check_source=np.array([1998,1483])
    err=float(np.linalg.norm((check_game@transform+offset-check_source)@np.linalg.inv(transform)))
    report=dict(status='GAME_RESOLUTION_APPROXIMATION_NOT_CADASTRAL',
        historical_target='1776-01-01',atlas_date=1789,atlas_url='https://connaitrelawallonie.wallonie.be/sites/default/files/maps/1789_0160c_v2.jpg',
        period_cross_check='Ferraris 1770-1778: separate Liège and Stavelot jurisdictions, not retrospective Belgian national ownership',
        fitted_anchors=[dict(name=n,game=g.tolist(),source=s.tolist()) for n,g,s in zip(['Brussels','Liège'],game,source)],
        transform=transform.tolist(),offset=offset.tolist(),namur_rough_independent_error_game_pixels=err,
        limitations=['Native city locators and region envelope are coarse; village-level accuracy is not claimed.',
            'No transfers outside the frozen BEO envelope: Maastricht condominium and other foreign-held fragments are not adjudicated.',
            'Bouillon and Saint-Hubert retain their current representation pending separate legal and geometric review.',
            'Existing State Regions remain shared economic regions; sovereign borders are independently redrawn.'],
        crop=box,assignments=assignments,new_provinces=children,abstracted=abstracted,
        pixels_by_state_owner=[dict(state=s,owner=t,pixels=c) for (s,t),c in sorted(summary.items())],
        candidate_sha256=sha(LOT/'provinces_candidate.png'))
    dump('GEOMETRY.json',report)
    preview(report,after)
    print(json.dumps(dict(new_RGBs=len(children),assignments=len(assignments),pixels=report['pixels_by_state_owner'],independent_error=err),ensure_ascii=False))


def preview(report,array):
    x0,y0,x1,y1=report['crop'];local=array[y0:y1,x0:x1];canvas=np.full((*local.shape,3),230,dtype=np.uint8)
    for r in report['assignments']:canvas[local==int(r['rgb'][1:],16)]=COLORS[r['owner']]
    edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1]
    canvas[edge]=[70,70,70]
    im=Image.fromarray(canvas).resize((canvas.shape[1]*10,canvas.shape[0]*10),Image.Resampling.NEAREST)
    out=Image.new('RGB',(im.width,im.height+110),'white');out.paste(im)
    d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    for i,(tag,title) in enumerate([('BEO','Pays-Bas autrichiens'),('LGE','Principauté de Liège'),('STM','Stavelot-Malmedy')]):
        d.rectangle((12,im.height+10+i*30,35,im.height+30+i*30),fill=COLORS[tag]);d.text((45,im.height+10+i*30),title,font=font,fill='black')
    out.save(LOT/'belgium_candidate.png')


def allocate(count,weights):
    total=sum(weights.values());amounts={t:count*w//total for t,w in weights.items()}
    rest=count-sum(amounts.values())
    order=sorted(weights,key=lambda t:(-(count*weights[t]%total),t))
    for t in order[:rest]:amounts[t]+=1
    assert sum(amounts.values())==count
    return amounts


def emit(files,name):
    patch=['*** Begin Patch'];changes=[]
    for rel,new in files.items():
        path=ROOT/rel;old=path.read_text(encoding='utf-8') if path.exists() else None
        if old is not None and old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
        if old==new:continue
        changes.append(rel)
        if old is None:patch+=['*** Add File: '+str(path)]+['+'+line for line in new.splitlines()]
        else:
            # Repeated native buttons have identical closing lines. Include
            # their unique identifiers so additions cannot match the first one.
            diff=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=15))
            patch+=['*** Update File: '+str(path)]+['@@' if l.startswith('@@') else l for l in diff[2:]]
    patch+=['*** End Patch'];(LOT/name).write_text('\n'.join(patch)+'\n',encoding='utf-8')
    return changes


def prepare():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'));geo=json.loads((LOT/'GEOMETRY.json').read_text(encoding='utf-8'))
    assert sha(ROOT/'map_data/provinces.png')==base['bitmap_sha256']
    inv=qa.inventory();assert not set(TAGS)&set(inv['countries'])
    files={};allocations=[]
    weights={s:{r['owner']:r['pixels'] for r in geo['pixels_by_state_owner'] if r['state']==s} for s in REGIONS}
    rel='common/history/states/00_states.txt';raw=base['originals'][rel]
    for sid in REGIONS:
        src=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:BEO')
        sections=[]
        for tag in ['BEO',*TAGS]:
            rgbs=[r['rgb'] for r in geo['assignments'] if r['state']==sid and r['owner']==tag]
            if rgbs:sections.append('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(rgbs)+' } }')
        raw=edits(raw,[(src.start,src.end,'\n\t\t'.join(sections))])
    files[rel]=raw
    rel='map_data/state_regions/00_west_europe.txt';raw=base['originals'][rel]
    for sid in REGIONS:
        node=next(n for n in cw.parse(raw) if n.key==sid);provs=node.children('provinces')[0]
        rgbs=sorted(r['rgb'] for r in geo['assignments'] if r['state']==sid)
        raw=edits(raw,[(provs.start,provs.end,'provinces = { '+' '.join('"'+r+'"' for r in rgbs)+' }')])
    files[rel]=raw
    for rel,original in base['originals'].items():
        if '/pops/' not in rel and '/buildings/' not in rel:continue
        raw=original
        for sid in REGIONS:
            try:src=region(raw,sid,'BEO')
            except StopIteration:continue
            ops=[];moved=C.defaultdict(list)
            if '/pops/' in rel:
                pops=src.children('create_pop')
                for i,pop in enumerate(pops):
                    count=int(pop.one('size'))
                    # First four Wallonia profiles are the previously restored
                    # Luxembourg pool: keep their entire 137,881 under BEO.
                    preserve=sid=='STATE_WALLONIA' and i<4 and rel.endswith('00_west_europe.txt')
                    amounts={'BEO':count} if preserve else allocate(count,weights[sid])
                    n=pop.children('size')[0];piece=raw[pop.start:pop.end]
                    remaining=amounts.get('BEO',0)
                    ops.append((pop.start,pop.end,'') if not remaining else (n.start,n.end,'size = '+str(remaining)))
                    for tag in TAGS:
                        amount=amounts.get(tag,0)
                        if amount:moved[tag].append(edits(piece,[(n.start-pop.start,n.end-pop.start,'size = '+str(amount))]))
                    allocations.append(dict(file=rel,state=sid,kind='population',before=count,after=amounts,luxembourg_preserved=preserve))
            else:
                for building in src.children('create_building'):
                    lv=[n for n in cw.walk(building.children()) if n.key=='levels' and not isinstance(n.value,list)]
                    if not lv:continue
                    piece=raw[building.start:building.end];bytag=C.defaultdict(list);counts=C.Counter()
                    for n in lv:
                        count=int(n.value);amounts=allocate(count,weights[sid])
                        # Existing Wallonian civil administration becomes the
                        # Liège administration. Flanders' BEO office is kept.
                        if cw.scalar(building.one('building'))=='building_government_administration' and sid=='STATE_WALLONIA':
                            amounts={t:count if t=='LGE' else 0 for t in weights[sid]}
                        for t,amount in amounts.items():
                            bytag[t].append((n.start-building.start,n.end-building.start,'levels = '+str(amount)));counts[t]+=amount
                    fragments={}
                    for tag in weights[sid]:
                        if not counts[tag]:continue
                        fragment=edits(piece,bytag[tag]);root=cw.parse(fragment)[0];zeros=[]
                        for ownership in root.children('add_ownership'):
                            for holder in ownership.children():
                                if holder.one('levels')=='0':zeros.append((holder.start,holder.end,''))
                        fragment=edits(fragment,zeros)
                        if tag!='BEO' and cw.scalar(building.one('building'))=='building_government_administration':
                            fragment=re.sub(r'(country\s*=\s*"?c:)BEO',r'\g<1>'+tag,fragment)
                        fragments[tag]=fragment
                    ops.append((building.start,building.end,fragments.get('BEO','')))
                    for tag in TAGS:
                        if tag in fragments:moved[tag].append(fragments[tag])
                    allocations.append(dict(file=rel,state=sid,kind='building',type=cw.scalar(building.one('building')),before=sum(int(n.value) for n in lv),after=dict(counts)))
            raw=edits(raw,ops)
            for tag,pieces in moved.items():raw=append(raw,sid,tag,'\n'.join(pieces))
        if raw!=original:files[rel]=raw
    # Native terrain file is generated province data. Every child inherits its
    # parent's exact type; full native mapping preserved in the staged override.
    terrain_path=ROOT/'map_data/province_terrains.txt'
    assert not terrain_path.exists(),'Review existing terrain override before overwriting'
    terrain=(qa.GAME/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')
    terrains=dict(re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain))
    terrains={k.upper():v for k,v in terrains.items()}
    for child in geo['new_provinces']:
        child['terrain']=terrains[child['parent_rgb'].upper()]
        terrain+='\n'+child['rgb']+'="'+child['terrain']+'"'
    (LOT/'province_terrains_candidate.txt').write_text(terrain+'\n',encoding='utf-8')
    countries='';rulers='CHARACTERS = {\n';flags='';coas=''
    names={'LGE':('Prince-Bishopric of Liège','Principauté de Liège','Liégeois','Liégeois'),
           'STM':('Stavelot-Malmedy','Stavelot-Malmedy','Stavelotian','Stavelotain')}
    for tag in TAGS:
        rgb=COLORS[tag]
        cultures='wallonian flemish' if tag=='LGE' else 'wallonian north_german'
        countries+=f'{tag} = {{ color = {{ {rgb[0]} {rgb[1]} {rgb[2]} }} country_type = recognized tier = principality cultures = {{ {cultures} }} religion = catholic capital = STATE_WALLONIA }}\n'
        template=base['originals']['common/history/countries/ktr - imperial electorate.txt']
        files[f'common/history/countries/{tag.lower()} - imperial estate.txt']=template.replace('c:KTR','c:'+tag)
        first,last,age=('aor1776_lge_francois_charles','aor1776_lge_velbruck',56) if tag=='LGE' else ('aor1776_stm_jacques','aor1776_stm_hubin',68)
        rulers+=f' c:{tag} ?= {{ create_character = {{ first_name = {first} last_name = {last} historical = yes culture = '+('north_german' if tag=='LGE' else 'primary_culture')+f' religion = rel:catholic ruler = yes age = {age} interest_group = ig_devout ideology = ideology_traditionalist }} }}\n'
        # Identifying native-engine banners, not claimed as archival flags.
        coas+=f'AOR1776_{tag} = {{ pattern = "pattern_solid.tga" color1 = '+('red' if tag=='LGE' else 'blue')+' colored_emblem = { texture = "ce_cross_couped.dds" color1 = '+('yellow' if tag=='LGE' else 'white')+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
        flags+=f'{tag} = {{ flag_definition = {{ coa = AOR1776_{tag} priority = 100 allow_overlord_canton = no }} }}\n'
    files['common/country_definitions/1776_map2l_imperial_estates.txt']=countries
    files['common/history/characters/1776_map2l_belgian_rulers.txt']=rulers+'}\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_belgian_flags.txt']=coas
    files['common/flag_definitions/1776_map2l_belgian_flags.txt']=flags
    for lang,index in [('english',0),('french',1)]:
        loc='\ufeffl_'+lang+':\n'
        for tag,ns in names.items():loc+=' '+tag+':0 "'+ns[index]+'"\n '+tag+'_ADJ:0 "'+ns[2+index]+'"\n'
        loc+=' aor1776_lge_francois_charles:0 "François-Charles"\n aor1776_lge_velbruck:0 "de Velbrück"\n aor1776_stm_jacques:0 "Jacques"\n aor1776_stm_hubin:0 "de Hubin"\n'
        files[f'localization/{lang}/1776_map2l_belgian_estates_l_{lang}.yml']=loc
    for rel,raw in files.items():
        if rel.endswith('.txt'):cw.parse(raw)
    old={r['rgb']:r for r in base['de_jure_registry']};ledger=[]
    assignment={r['rgb']:r for r in geo['assignments']}
    for row in base['inventory']['owners']:
        rgb,sid,tag=row['key']
        if rgb not in old:continue
        if sid not in REGIONS:ledger.append(old[rgb]);continue
        for a in sorted((r for r in geo['assignments'] if r['parent_rgb']==rgb),key=lambda r:r['rgb']):
            ledger.append(dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json'))
    ledger.sort(key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    (LOT/'registry_candidate.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
    changes=emit(files,'HISTORY.patch')
    dump('PLAN.json',dict(files=changes,allocations=allocations,new_tags=TAGS,new_provinces=geo['new_provinces'],
        world_population_before=sum(r['count'] for r in base['inventory']['pops']),
        preserves_military_formations=True,preserves_historical_subject_relationships=True,
        ruler_notes='Velbrück age based on known 1719 birth year. Hubin age 68 is an explicit gameplay estimate, not a verified birth date.',
        flag_notes='Native ecclesiastical identifying banners; not asserted to be the historical territorial flags.',
        historical_sources=['https://donum.uliege.be/handle/2268.1/2513','https://orbi.uliege.be/bitstream/2268/101442/1/bcrh_0001-415x_1987_num_153_3_1290.pdf']))
    print('PREPARED',len(changes),'text files;',len(ledger),'registered province identities')


def install_generated():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    geo=json.loads((LOT/'GEOMETRY.json').read_text(encoding='utf-8'))
    assert sha(ROOT/'map_data/provinces.png')==base['bitmap_sha256'],'Unrelated bitmap edit'
    assert sha(LOT/'provinces_candidate.png')==geo['candidate_sha256']
    assert 'c:LGE' in (ROOT/'common/history/states/00_states.txt').read_text(encoding='utf-8-sig')
    assert not (ROOT/'map_data/province_terrains.txt').exists()
    assert not (OUT/'IMPERIAL_DE_JURE_REGISTRY.json').exists()
    # Mechanical generated map/terrain/registry installation, with the exact
    # prior bitmap already saved and verified. Never touch user save files.
    shutil.copyfile(LOT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    shutil.copyfile(LOT/'province_terrains_candidate.txt',ROOT/'map_data/province_terrains.txt')
    shutil.copyfile(LOT/'registry_candidate.json',OUT/'IMPERIAL_DE_JURE_REGISTRY.json')
    print('Generated bitmap, inherited terrains and versioned registry installed')


def compile_imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=LOT
    files=compiler.compile_system()
    changes=emit(files,'IMPERIAL.patch')
    baseline=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    touched=[rel for rel in files if rel not in baseline['hashes'] or not (ROOT/rel).exists() or sha(ROOT/rel)!=baseline['hashes'][rel]]
    dump('IMPERIAL_FILES.json',dict(files=sorted(set(touched)|set(changes)),all_compiled_files=list(files)))
    print('Imperial integration:',len(changes),'changed files')


if __name__=='__main__':
    if sys.argv[1:]==['geometry']:geometry()
    elif sys.argv[1:]==['prepare']:prepare()
    elif sys.argv[1:]==['install-generated']:install_generated()
    elif sys.argv[1:]==['compile-imperial']:compile_imperial()
    else:raise SystemExit('Use geometry, prepare, install-generated or compile-imperial')
