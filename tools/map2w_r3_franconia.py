"""MAP2W-R3-A: targeted Franconian continuation, preserving previous installs."""
import collections as C
import json,re,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2w_r2b_completion as prior
core=prior.core;q=prior.q;ROOT=prior.ROOT;OUT=prior.a.r1.OUT/'R3'
REGIONS=['STATE_FRANCONIA','STATE_WURTTEMBERG','STATE_BADEN','STATE_BAVARIA']
def dump(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def capture():
    assert not (OUT/'BASELINE.json').exists(),'Immutable capture already exists'
    backup=prior.OUT/'provinces_candidate.png';assert core.sha(backup)==core.sha(ROOT/'map_data/provinces.png')
    originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if any(s in raw for s in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    inv=core.qa.inventory();registry=json.loads(core.active_registry_path().read_text());assert len(registry)==567;assert sum(r['count'] for r in inv['pops'])==835801255
    dump('BASELINE.json',dict(inventory=inv,originals=originals,hashes=q.economy.runtime_hashes(),registry=registry,bitmap_backup=backup.relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(backup),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=core.sha(ROOT/'.git/index'),registry_tool=(ROOT/'tools/map2l_registry.py').read_text(encoding='utf8')))
    print('Current baseline: 567 imperial RGB, world 835801255. R2-B bitmap retained.',flush=True)
def diagnostic():
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup']);owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    cities=[('Oehringen',9.503,49.201),('Neuenstein',9.58,49.204),('Langenburg',9.856,49.253),('Ingelfingen',9.652,49.3),('Bartenstein',9.881,49.359),('Kirchberg_Jagst',9.981,49.205),('Waldenburg',9.64,49.184),('Schillingsfuerst',10.26,49.287),('Castell',10.349,49.74),('Wertheim',9.517,49.759),('Rothenburg',10.18,49.377),('Schweinfurt',10.232,50.046),('Windsheim',10.415,49.504),('Weissenburg',10.972,49.03)]
    target=forward(model,[[lo,la] for _,lo,la in cities]);rows=[]
    for (name,lo,la),p in zip(cities,target):
        rgb='x'+format(int(before[round(p[1]),round(p[0])]),'06X');rows.append(dict(name=name,geo=[lo,la],diagnostic_pixel=p.tolist(),rgb=rgb,owner=owners.get(rgb)))
    dump('CITY_DIAGNOSTIC.json',rows);print(json.dumps(rows,ensure_ascii=False),flush=True)
    print('Available tags',{t:t in b['inventory']['countries'] for t in ['HLA','HIN','HKI','HBA','HSC','HOE']},flush=True)

def svg_review():
    """Render the retained vector evidence; do not infer sovereignty from pixels."""
    import xml.etree.ElementTree as ET
    tree=ET.parse(OUT/'EVIDENCE/Gerabronn_1800.svg');ns={'s':'http://www.w3.org/2000/svg'}
    symbols=tree.find('.//s:g[@id="symbols"]',ns)
    pts=[(float(n.attrib['x']),float(n.attrib['y'])) for n in symbols if n.tag.endswith('use')]
    labels=[]
    for n in tree.findall('.//s:g[@id="texts"]/s:text',ns):
        name=''.join(n.itertext()).strip();xy=re.search(r'translate\(([-\d.]+),([-\d.]+)\)',n.attrib.get('transform',''))
        if xy:
            p=np.array([float(xy[1])/10,float(xy[2])/10]);near=sorted(pts,key=lambda q:np.linalg.norm(p-q))[:2]
            labels.append(dict(name=name,label=p.tolist(),symbols=near))
    polys=[];im=Image.new('RGB',(1120,1280),'white');d=ImageDraw.Draw(im)
    colors={'HohenloheLa':'#e9b865','HohenloheKi':'#69b6bb','HohenloheBa':'#b38ac7','HohenloheIn':'#82af70','HohenloheOe':'#d4ad94','Brandenburg':'#a6b6c3','Stadt':'#f6e6aa'}
    for n in tree.findall('.//s:path[@id]',ns):
        data=n.attrib.get('d','');cls=n.attrib.get('class','');ident=n.attrib['id']
        if not re.match(r'M\d',data):continue
        assert set(re.findall('[A-Za-z]',data))<={'M','L','Z'},ident
        parts=[]
        for part in re.findall(r'M([^Z]+)Z',data):
            poly=[tuple(map(float,p)) for p in re.findall(r'([-\d.]+),([-\d.]+)',part)];parts.append(poly)
            d.polygon([((x-558)*40,(477-y)*40) for x,y in poly],fill=colors.get(cls,'#eee9dd'),outline='#64696c')
        polys.append(dict(id=ident,cls=cls,polygons=parts))
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for row in labels:
        x,y=row['label'];d.text(((x-558)*40,(477-y)*40),row['name'],fill='black',font=font)
    im.save(OUT/'GERABRONN_SOURCE_REVIEW.png');dump('SOURCE_VECTOR.json',dict(polygons=polys,labels=labels))
    print(json.dumps(labels,ensure_ascii=False));print('Source polygons',[(p['id'],p['cls']) for p in polys])
    from html import unescape
    raw=(OUT/'EVIDENCE/Gerabronn_SOURCE.html').read_text(encoding='utf8')
    for token in ['fileinfotpl_src','fileinfotpl_aut','licensetpl_short','1900','1800','Beschreibung','Bodenschatz']:
        at=raw.find(token)
        if at>=0:print(token,re.sub('<[^>]+>',' ',unescape(raw[max(0,at-100):at+1600])))

def compiler_before():
    old=prior.OUT;prior.OUT=OUT
    try:prior.compiler_before()
    finally:prior.OUT=old

def geometry():
    """Stable Langenburg/Kirchberg cores only, not an 1800 map back-projection."""
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup'])
    assert not {'HLN','HKI'}&set(b['inventory']['countries'])
    source=load('SOURCE_VECTOR.json');cities={r['name']:r for r in load('CITY_DIAGNOSTIC.json')}
    controls=[('Langenburg',561.6,457.7),('Bartenstein',564.1,469.2),('Kirchberg_Jagst',571.6,452.4)]
    X=np.array([[x,y,1] for _,x,y in controls]);Y=np.array([cities[n]['diagnostic_pixel'] for n,_,_ in controls]);tr=np.linalg.solve(X,Y)
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    tests=[('Gerabronn',567.1,457.4,9.92028,49.24944),('Schrozberg',571.3,467.9,9.97944,49.34528)]
    alignment=dict(transform=tr.tolist(),controls=[dict(name=n,source=[x,y],pixel=cities[n]['diagnostic_pixel']) for n,x,y in controls],independent_sheet_checks=[dict(name=n,source=[x,y],geo=[lo,la],residual=float(np.linalg.norm(np.array([x,y,1])@tr-forward(model,[[lo,la]])[0]))) for n,x,y,lo,la in tests],warning='Registration of source geometry to inherited diagnostic model, NOT independent native bitmap calibration. Geographic B generalisation only; no certified subpixel accuracy.')
    dump('SOURCE_ALIGNMENT.json',alignment)
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};labels={};traces=[];excluded=[]
    # Only stable territorial Amts cores; Werdeck acquired 1797 is absent.
    for ident,tag in [('HoLaLangenburg','HLN'),('HoKiKirchberg','HKI')]:
        row=next(p for p in source['polygons'] if p['id']==ident);accepted=[];mapped_parts=[]
        area=lambda p:abs(sum(p[i-1][0]*p[i][1]-p[i][0]*p[i-1][1] for i in range(len(p))))
        # First testable sublot: largest continuous Amts body only. Eastern
        # detached parcels near the later Ansbach regularisations stay C.
        core_poly=max(row['polygons'],key=area)
        for poly in [core_poly]:
            mapped=np.column_stack([poly,np.ones(len(poly))])@tr;mapped_parts.append(mapped.tolist())
            xmin,ymin=np.floor(mapped.min(axis=0)).astype(int);xmax,ymax=np.ceil(mapped.max(axis=0)).astype(int)
            yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx.ravel();yy=yy.ravel();centres=np.column_stack([xx+.5,yy+.5]);chosen=core.inside(centres,mapped)
            # Do not widen a territory to rescue an invisible fragment.
            for x,y in zip(xx[chosen],yy[chosen]):
                rgb='x'+format(int(before[y,x]),'06X');sid,old=owners[rgb]
                reason=None if rgb=='xEDA218' and old=='BAV' and sid=='STATE_FRANCONIA' else 'PROTECTED_CORE_OR_UNREVIEWED_PARENT'
                if reason:excluded.append(dict(source=ident,cell=[int(x),int(y)],rgb=rgb,owner=old,reason=reason));continue
                key=(int(x),int(y));assert key not in labels
                labels[key]=(tag,ident);accepted.append(list(key))
        # Isolated subpixel enclaves are left abstract, not playable one-cell states.
        mask=np.zeros(before.shape,bool)
        for x,y in accepted:mask[y,x]=True
        removed=[]
        for part in core.components(mask):
            if len(part)==1:
                y,x=part[0];del labels[x,y];removed.append([x,y]);excluded.append(dict(source=ident,cell=[x,y],reason='ONE_CELL_FRAGMENT_NOT_ENLARGED'))
        accepted=[p for p in accepted if p not in removed]
        assert len(accepted)>=3,(ident,accepted)
        traces.append(dict(territory=ident,tag=tag,source_polygons=[core_poly],game_polygons=mapped_parts,included=accepted,confidence='B',excluded_late_acquisitions=['HoBaWerdeck','Niedernhall_Mainz_share_1799','Jagstberg_1803'],excluded_condominiums=['KondObersteinach','KondRuppertshofen','KondGaggstatt'],detached_parts_deferred=len(row['polygons'])-1))
    parents=sorted({'x'+format(int(before[y,x]),'06X') for x,y in labels});assert parents==['xEDA218']
    after=before.copy();assignments=[];new=[];color=0xEDB900;used=set(map(int,np.unique(before)))
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
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,traces=traces,excluded=excluded,new_members=['HLN','HKI'],hub_rebindings=[],limits='R3-A1 stable Langenburg and Kirchberg only. B generalised native-cell interiors, no one-cell countries or corridors. Other branches pending; no retrospective 1797/1803 gains. All previously assigned cores protected.'))
    im=Image.open(OUT/'GERABRONN_SOURCE_REVIEW.png');d=ImageDraw.Draw(im);itr=np.linalg.inv(np.vstack([tr.T,[0,0,1]]))
    for x,y in labels:
        corners=[itr@np.array([px,py,1]) for px,py in [(x,y),(x+1,y),(x+1,y+1),(x,y+1),(x,y)]]
        d.line([((p[0]-558)*40,(477-p[1])*40) for p in corners],fill='blue',width=3)
    im.save(OUT/'SOURCE_ACCEPTED_REVIEW.png');print('Transfers',dict(C.Counter(tag for tag,_ in labels.values())),'new RGB',new,'assignments',[(r['rgb'],r['owner'],r['pixels']) for r in assignments],flush=True)

def prepare():
    raise RuntimeError('R3 candidate withdrawn: resolve NATIVE_REFERENCE_CONTRADICTION.json before any future implementation')
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};groups=C.defaultdict(list);bindings=[]
    assert load('COMPILER_BEFORE.json')['passed']==73
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    for r in g['assignments']:groups[r['parent_rgb']].append(r)
    sid='STATE_FRANCONIA';rel='common/history/states/00_states.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');n=core.state(raw,sid);ops=[]
    assert core.qa.signature(n)==core.qa.signature(core.state(b['originals'][rel],sid)),'Concurrent affected-state edit'
    for z in n.children('create_state'):
        tag=z.one('country').removeprefix('c:');f=z.children('owned_provinces')[0];values=[]
        for rgb in core.values(z,'owned_provinces'):values.extend(r['rgb'] for r in groups[rgb] if r['owner']==tag) if rgb in groups else values.append(rgb)
        if values!=core.values(z,'owned_provinces'):ops.append((f.start,f.end,'owned_provinces = { '+' '.join(values)+' }'))
        assert values
    for tag in g['new_members']:
        values=[r['rgb'] for r in g['assignments'] if r['owner']==tag]
        ops.append((n.end-1,n.end-1,'\ncreate_state = { country = c:'+tag+' owned_provinces = { '+' '.join(values)+' } }\n'))
    files[rel]=core.edits(raw,sorted(ops))
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png');locs=q.r9.locators(before)
    for rel,old in b['originals'].items():
        if not rel.startswith('map_data/state_regions/'):continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');nodes={z.key:z for z in core.cw.parse(raw)}
        if sid not in nodes:continue
        n=nodes[sid];assert core.qa.signature(n)==core.qa.signature(next(z for z in core.cw.parse(old) if z.key==sid));ops=[]
        for field in ['provinces','prime_land']:
            for f in n.children(field):
                existing=core.values(n,field);values=[]
                for rgb in existing:values.extend(r['rgb'] for r in groups[rgb]) if rgb in groups else values.append(rgb)
                if values!=existing:
                    ops.append((f.start,f.end,field+' = { '+' '.join('"'+v+'"' for v in values)+' }'))
                    if field=='prime_land':bindings.append(dict(state=sid,field=field,before=existing,after=values))
        for loc in locs:
            if loc['ID']!=int(n.one('id')):continue
            x,y=int(loc['X']),int(loc['Y']);rgb='x'+format(int(after[y,x]),'06X');oldrgb=core.cw.scalar(n.one(loc['Kind']))
            if rgb!=oldrgb:
                f=n.children(loc['Kind'])[0];ops.append((f.start,f.end,loc['Kind']+' = "'+rgb+'"'));bindings.append(dict(state=sid,field=loc['Kind'],before=oldrgb,after=rgb,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
        if ops:files[rel]=core.edits(raw,sorted(ops))
    # Population is conserved per existing culture/religion profile. Pixel
    # shares are a provisional technical allocation, not an historical census.
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};counts_by_rgb=dict(zip(*np.unique(before,return_counts=True)))
    total=sum(int(counts_by_rgb[int(rgb[1:],16)]) for rgb,st in owners.items() if st==[sid,'BAV']);weights=C.Counter({'BAV':total})
    for r in g['assignments']:
        if r['owner']!='BAV':weights['BAV']-=r['pixels'];weights[r['owner']]+=r['pixels']
    allocations=[]
    for rel,old in b['originals'].items():
        if '/pops/' not in rel:continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig')
        try:n=core.region(raw,sid,'BAV')
        except StopIteration:continue
        assert core.qa.signature(n)==core.qa.signature(core.region(old,sid,'BAV')),'Concurrent population edit';ops=[];moved=C.defaultdict(list)
        for p in n.children('create_pop'):
            f=p.children('size')[0];amounts=core.allocate(int(f.value),weights);piece=raw[p.start:p.end];ops.append((f.start,f.end,'size = '+str(amounts['BAV'])))
            for tag,amount in amounts.items():
                if tag!='BAV' and amount:moved[tag].append(core.edits(piece,[(f.start-p.start,f.end-p.start,'size = '+str(amount))]))
            allocations.append(dict(state=sid,source='BAV',culture=p.one('culture'),religion=p.one('religion','DEFAULT:'+p.one('culture')),before=int(f.value),after=amounts))
        raw=core.edits(raw,sorted(ops))
        for tag,parts in moved.items():raw=core.append(raw,sid,tag,'\n'.join(parts))
        for tag in moved:raw=raw.replace('\n\t\n\t\tregion_state:'+tag,'\n\n\t\tregion_state:'+tag)
        files[rel]=raw
    dump('ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_PROFILE_CONSERVATION_NOT_CENSUS',weights={sid+'|BAV':weights},profiles=allocations,historical_population=None,buildings='All existing levels, PMs, ownership and units remain at surviving donor subdivision. No arbitrary new factory or regiment.'))
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw.rstrip()+'\n'+''.join(r['rgb']+'="'+tm[r['parent_rgb'].upper()]+'"\n' for r in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state']==sid];updated=[r for r in previous if r['rgb'] not in g['parents']]+[dict(rgb=r['rgb'],state=sid,beneficiary=r['owner'],basis='MAP2W-R3-A1: stable Langenburg/Kirchberg cores, B generalisation. Other Hohenlohe branches/fringes unchanged; see MAP2W/R3/REPORT.md') for r in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state']!=sid]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    defs='HLN = { color = { 220 170 80 } country_type = recognized tier = principality cultures = { south_german } religion = protestant capital = STATE_FRANCONIA }\nHKI = { color = { 75 160 170 } country_type = recognized tier = principality cultures = { south_german } religion = protestant capital = STATE_FRANCONIA }\n'
    files['common/country_definitions/1776_map2w_r3_hohenlohe.txt']=defs
    for tag,birth,first,last in [('HLN','1726.3.27','Christian Albrecht','zu Hohenlohe-Langenburg'),('HKI','1729.10.19','Christian Friedrich Karl','zu Hohenlohe-Kirchberg')]:
        prefix='aor1776_map2w_r3_'+tag.lower()
        files['common/history/countries/'+tag.lower()+' - map2w_r3.txt']=(ROOT/'common/history/countries/nas - nassau.txt').read_text(encoding='utf-8-sig').replace('c:NAS','c:'+tag)
        files['common/history/characters/'+tag.lower()+' - map2w_r3.txt']='CHARACTERS = { c:'+tag+' ?= { create_character = { first_name = '+prefix+'_first last_name = '+prefix+'_last historical = yes culture = south_german religion = rel:protestant ruler = yes birth_date = '+birth+' interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    # Simplified house arms: native passant leopards, no fabricated full banner.
    files['common/coat_of_arms/coat_of_arms/1776_map2w_r3_hohenlohe.txt']='aor1776_map2w_r3_hohenlohe = { pattern = "pattern_solid.tga" color1 = "white" colored_emblem = { texture = "ce_leopard_passant_guardant.dds" color1 = "black" color2 = "black" instance = { position = { 0.5 0.32 } scale = { 0.75 0.33 } } instance = { position = { 0.5 0.68 } scale = { 0.75 0.33 } } } }\n'
    files['common/flag_definitions/1776_map2w_r3_hohenlohe.txt']=''.join(tag+' = { flag_definition = { coa = aor1776_map2w_r3_hohenlohe priority = 100 allow_overlord_canton = no } }\n' for tag in g['new_members'])
    files['common/government_types/00_1776_map2w_r3_hohenlohe.txt']='gov_aor1776_map2w_r3_hohenlohe = { transfer_of_power = hereditary male_ruler = "RULER_TITLE_PRINCE" female_ruler = "RULER_TITLE_PRINCESS" possible = { OR = { c:HLN ?= this c:HKI ?= this } has_law = law_type:law_monarchy } on_government_type_change = { change_to_hereditary = yes } on_post_government_type_change = { post_change_to_hereditary = yes } }\n'
    for lang in ['french','english']:
        fr=lang=='french';loc={'HLN':'Hohenlohe-Langenbourg' if fr else 'Hohenlohe-Langenburg','HLN_ADJ':'langenbourgeois' if fr else 'Langenburg','HKI':'Hohenlohe-Kirchberg','HKI_ADJ':'kirchbergeois' if fr else 'Kirchberg','aor1776_map2w_r3_hln_first':'Christian Albrecht','aor1776_map2w_r3_hln_last':'zu Hohenlohe-Langenburg','aor1776_map2w_r3_hki_first':'Christian Friedrich Karl','aor1776_map2w_r3_hki_last':'zu Hohenlohe-Kirchberg','gov_aor1776_map2w_r3_hohenlohe':'Principauté' if fr else 'Principality','gov_aor1776_map2w_r3_hohenlohe_desc':('Le [concept_ruler] gouverne les possessions de sa branche de la maison de Hohenlohe, qui conserve ses propres institutions.\\n\\n$TRANSFER_OF_POWER_NAME_DESC$' if fr else 'The [concept_ruler] governs the possessions of their branch of the House of Hohenlohe, which retains its own institutions.\\n\\n$TRANSFER_OF_POWER_NAME_DESC$')}
        files[f'localization/{lang}/1776_map2w_r3_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in loc.items())
    migration=dict(replaced_regions=[sid],previous=previous,updated=updated,new_members=g['new_members'],free_cities=[],new_provinces=g['new_provinces'],geometry='MAP2W/R3/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[],country_additions={n.key:core.qa.signature(n) for n in core.cw.parse(defs)})
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n';files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    dump('EXPECTED_TEXT.json',files);dump('PLAN.json',dict(files=list(files),registered_RGBs=len(ledger),region_reference_changes=bindings,new_subdivisions=[[sid,t] for t in g['new_members']]))
    core.OUT=OUT;patches=[]
    for i,(rel,raw) in enumerate(files.items()):
        name=f'HISTORY_{i}.patch';core.emit({rel:raw},name);patches.append(name)
    dump('HISTORY_PATCHES.json',patches);print('Prepared',len(files),'files,',len(ledger),'registry entries; bindings',bindings,flush=True)

def install():
    raise RuntimeError('Candidate withdrawn; no geographic acceptance for R3-A1')
    old=prior.a.OUT;prior.a.OUT=OUT
    try:prior.a.install()
    finally:prior.a.OUT=old

def imperial():
    old=prior.a.OUT;prior.a.OUT=OUT
    try:prior.a.imperial()
    finally:prior.a.OUT=old

def imperial_patches():
    old=prior.OUT;prior.OUT=OUT
    try:prior.imperial_patches()
    finally:prior.OUT=old

def journal():
    old=prior.a.OUT;prior.a.OUT=OUT
    try:prior.a.journal()
    finally:prior.a.OUT=old

def validate():
    import map2l_registry as reg
    b=load('BASELINE.json');g=load('GEOMETRY.json');m=load('REGISTRY_MIGRATION.json');inv=core.qa.inventory();dump('CURRENT_INVENTORY.json',inv);checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    counter=lambda rows:C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy();owners={r['key'][0]:r['key'][1:] for r in inv['owners']};eo=counter(b['inventory']['owners'])
    for key in list(eo):
        if key[0] in g['parents']:del eo[key]
    for row in g['assignments']:
        for x,y in row['cells']:expected[y,x]=int(row['rgb'][1:],16)
        eo[row['rgb'],row['state'],row['owner']]=1;mask=after==int(row['rgb'][1:],16)
        check('Owner/State '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['owner']])
        check('Exact connected RGB '+row['rgb'],int(mask.sum())==row['pixels'] and len(core.components(mask))==1)
    check('Full world bitmap exact scoped delta',np.array_equal(expected,after));check('Full world ownership exact declared delta',counter(inv['owners'])==eo)
    check('Seven sovereign cells only',sum(r['pixels'] for r in g['assignments'] if r['owner']!='BAV')==7)
    check('Erfurt unmodified',np.array_equal(before[822:837,4342:4359],after[822:837,4342:4359]))
    for key in ['building_levels_written','buildings','duplicates','errors','resolved_demographics','pops','units']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    check('Only two declared countries added',inv['countries']==reg.expected_country_definitions(b['inventory']['countries'],[m]))
    types=dict(b['inventory']['state_types']);types.update({f'STATE_FRANCONIA|{t}':'incorporated_default' for t in g['new_members']});check('Exactly two new economic subdivisions',inv['state_types']==types)
    ep=counter(b['inventory']['regional_pop']);alloc=load('ALLOCATION.json')
    for row in alloc['profiles']:
        ep[row['state'],row['source'],row['culture'],row['religion']]-=row['before']
        for tag,n in row['after'].items():ep[row['state'],tag,row['culture'],row['religion']]+=n
        check('Integer culture/religion profile '+row['culture']+'/'+row['religion'],sum(row['after'].values())==row['before'] and all(isinstance(n,int) and n>=0 for n in row['after'].values()))
    check('Exact regional demography allocation',counter(inv['regional_pop'])==ep)
    world=sum(r['count'] for r in inv['pops']);oldworld=sum(r['count'] for r in b['inventory']['pops']);check('World population not fabricated',world==oldworld==835801255)
    totals={t:sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==t) for t in g['new_members']+['BAV']};check('Both new countries populated',all(totals[t]>0 for t in g['new_members']))
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'));check('571 distinct imperial RGB',len(ledger)==len({r['rgb'] for r in ledger})==571)
    for row in ledger:check('Imperial title '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']])
    check('Exact physical imperial extent preserved',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text())['de_jure_registry'];belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text());regions={r['state'] for r in belgian['assignments']}
    initial=[r for r in initial if r['state'] not in regions]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in belgian['assignments']]+reg.approved_territorial_extensions()
    check('Full chronological registry replay',reg.apply_territorial_migrations(initial)==ledger)
    changed_parents=set(map(int,np.unique(before[before!=after])));check('Only explicitly residual xEDA218 recoloured',changed_parents=={0xEDA218})
    for row in b['registry']:
        if row['rgb'] in g['parents']:continue
        check('Previous registered RGB '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']] and int(row['rgb'][1:],16) not in changed_parents)
    protected=0
    for directory in reg.approved_lot_dirs():
        if directory==OUT:continue
        geometry_path=directory/'GEOMETRY.json'
        if not geometry_path.exists():continue
        oldgeo=json.loads(geometry_path.read_text());basepath=directory/'BASELINE.json';oldowners={}
        if basepath.exists():oldowners={r['key'][0]:r['key'][2] for r in json.loads(basepath.read_text()).get('inventory',{}).get('owners',[])}
        for row in oldgeo.get('assignments',[]):
            previous=row.get('previous_owner',oldowners.get(row['parent_rgb']))
            if row['owner']==previous:continue
            cells=row['cells'];protected+=len(cells);check('Accepted prior cells '+directory.name+'/'+row['rgb'],all(after[y,x]==before[y,x] for x,y in cells))
    files=load('EXPECTED_TEXT.json');compiled=load('IMPERIAL_EXPECTED.json')
    for rel,raw in {**files,**compiled}.items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig');check('Expected text '+rel,actual.rstrip()==raw.lstrip('\ufeff').rstrip())
        if rel.endswith('.txt'):
            try:core.cw.parse(actual);check('Parse '+rel,True)
            except Exception as exc:check('Parse '+rel,False,str(exc))
    for rel,old in b['originals'].items():
        if rel not in files:continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig')
        if '/history/' in rel:
            scope=lambda text:[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(text)) if n.key.startswith('s:STATE_') and n.key!='s:STATE_FRANCONIA']
            check('Unrelated histories '+rel,scope(raw)==scope(old))
        if rel.startswith('map_data/state_regions/'):
            oldnodes={n.key:n for n in core.cw.parse(old)};newnodes={n.key:n for n in core.cw.parse(raw)}
            for sid,n in oldnodes.items():
                excluded={'provinces'} if sid=='STATE_FRANCONIA' else set();check('Unchanged resources, hubs, IDs, arable '+sid,[core.qa.signature(c) for c in n.children() if c.key not in excluded]==[core.qa.signature(c) for c in newnodes[sid].children() if c.key not in excluded])
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for row in g['new_provinces']:
        rgb=row['rgb'];check('New RGB unique '+rgb,not np.any(before==int(rgb[1:],16)) and len(re.findall(r'(?im)^\s*'+rgb+r'\s*=',terrain))==1)
        check('Terrain inherited '+rgb,tm[rgb.upper()]==tm[row['parent_rgb'].upper()]);check('State mapping '+rgb,inv['geometry'].get(rgb)=='STATE_FRANCONIA')
    locsets=[]
    for lang in ['french','english']:
        path=ROOT/f'localization/{lang}/1776_map2w_r3_l_{lang}.yml';raw=path.read_text(encoding='utf-8-sig');keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0\s+"',raw,re.M);locsets.append(set(keys))
        check('BOM/header '+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':'))
        check('Ten unique balanced keys '+lang,len(keys)==len(set(keys))==10 and all(line.count('"')==2 for line in raw.splitlines()[1:] if line.strip()))
        check('Dynamic succession prose '+lang,'$TRANSFER_OF_POWER_NAME_DESC$' in raw)
        collisions=[]
        for p in (ROOT/'localization'/lang).rglob('*.yml'):
            if p==path:continue
            other=p.read_text(encoding='utf-8-sig');collisions.extend(k for k in keys if re.search(r'^\s*'+re.escape(k)+r':',other,re.M))
        check('No new localisation collisions '+lang,not collisions,collisions)
    check('FR/EN key parity',locsets[0]==locsets[1])
    for tag,birth in [('HLN','1726.3.27'),('HKI','1729.10.19')]:
        rel='common/history/characters/'+tag.lower()+' - map2w_r3.txt';rulers=[n for n in core.cw.walk(core.cw.parse((ROOT/rel).read_text())) if n.key=='create_character']
        check('One dated historical ruler '+tag,len(rulers)==1 and rulers[0].one('birth_date')==birth and rulers[0].one('ruler')=='yes')
        check('Owned capital '+tag,any(r['key'][1:]==['STATE_FRANCONIA',tag] for r in inv['owners']))
    check('Native flag assets resolve',(core.qa.GAME/'gfx/coat_of_arms/colored_emblems/ce_leopard_passant_guardant.dds').is_file() and (core.qa.GAME/'gfx/coat_of_arms/patterns/pattern_solid.tga').is_file())
    from map2k_patch import ELECTORS
    check('Nine electors unchanged, new members not electors',len(ELECTORS)==9 and not set(g['new_members'])&set(ELECTORS.values()))
    check('No diplomatic or military files authored',not any('/diplomacy/' in p or '/diplomatic_' in p or '/military_' in p or '/subject_types/' in p for p in files))
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));allowed=set(files)|set(compiled)|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    outside=[p for p in changed if p not in allowed];check('No unexpected external runtime changes',not outside,outside)
    for part in ['buildings','military_formations','character_templates','companies','subject_types','diplomacy','map_object_data','production_methods','production_method_groups']:
        check('Protected '+part+' byte-identical',all(current.get(p)==h for p,h in b['hashes'].items() if '/'+part+'/' in p))
    for p in ['gfx/interface/icons/company_icons/historical_company_icons/france_saint_gobain.dds','common/company_types/00_companies_france.txt']:
        check('Protected French economy '+p,current.get(p)==b['hashes'].get(p))
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head']);check('Index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    result=dict(status='MAP2W_R3_READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2W_R3_BLOCKED',scope='R3-A1 Langenburg and Kirchberg stable cores only',runtime_status='NOT_TESTED_R3',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,world_before=oldworld,world_after=world,country_populations=totals,protected_prior_cells_checked=protected,runtime_files_modified=changed,external_changes=outside,preexisting_duplicate_RGBs=len(inv['duplicates']),preexisting_invalid_references=inv['errors'],new_errors=[r for r in inv['errors'] if r not in b['inventory']['errors']])
    dump('VALIDATION.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2W-R3-A1',functional_files={p:current[p] for p in changed},bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),git_head=b['git_head'],git_index_sha256=b['git_index_sha256']))
    print(result['status'],result['passed'],'/',result['total'],'populations',totals,flush=True)
    if result['passed']!=result['total']:raise SystemExit(1)

def maps():
    from PIL import ImageColor
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};now=dict(old)
    for r in g['assignments']:now[r['rgb']]=r['owner']
    colors={'BAV':'#bdc6d3','WUR':'#a8c19a','ANS':'#d6ab85','FBM':'#c8919c','WZB':'#ceadbd','HLN':'#dcaa50','HKI':'#4ba0aa','NUR':'#dfc780'}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',25);box=(4321,874,4338,891);scale=30
    def tile(bitmap,owners,outline):
        x0,y0,x1,y1=box;local=bitmap[y0:y1,x0:x1];arr=np.zeros((*local.shape,3),dtype='uint8')
        for c in np.unique(local):arr[local==c]=ImageColor.getrgb(colors.get(owners.get('x'+format(int(c),'06X')),'#eeebe5'))
        im=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        if outline:
            for row in g['assignments']:
                if row['owner']=='BAV':continue
                for x,y in row['cells']:d.rectangle(((x-x0)*scale,(y-y0)*scale,(x-x0+1)*scale-1,(y-y0+1)*scale-1),outline='white',width=3)
        for t,x,y in [('1 HLN',4326.5,881),('2 HKI',4328.5,883),('ANS',4334,878),('WUR',4322,885)]:
            px=(x-x0)*scale;py=(y-y0)*scale;d.text((max(2,min(px-30,im.width-90)),py-35),t,font=font,fill='#183444',stroke_width=2,stroke_fill='white')
        return im
    im=Image.new('RGB',(1140,780),'#fcfaf5');d=ImageDraw.Draw(im);d.text((25,18),'MAP2W-R3-A1 — noyaux Hohenlohe : 7 cellules B',font=bold,fill='#233849');d.text((25,75),'AVANT',font=bold,fill='#233849');d.text((600,75),'APRÈS — ajouts encadrés en blanc',font=bold,fill='#233849');im.paste(tile(before,old,False),(25,115));im.paste(tile(after,now,True),(600,115))
    d.text((25,655),'1 : Langenbourg (HLN), 3 cellules ; 2 : Kirchberg (HKI), 4 cellules.',font=font,fill='#233849');d.text((25,690),'Gris : résidus bavarois non certifiés. Les autres branches ne sont pas reconstruites.',font=font,fill='#233849');d.text((25,725),'Contours généralisés ; ni cadastre de 1776, ni positions GPS garanties dans le jeu.',font=font,fill='#233849');im.save(OUT/'BEFORE_AFTER.png')
    guide=Image.new('RGB',(1150,1020),'#fcfaf5');d=ImageDraw.Draw(guide);d.text((25,18),'Où vérifier R3-A1 — nouvelle partie, 1er janvier 1776',font=bold,fill='#233849');guide.paste(tile(after,now,True),(25,80));v=load('VALIDATION.json')
    notes=['À l’ouest d’Ansbach, au nord-est du Wurtemberg ; région économique Franconie / ID 72.',f"1. HLN — xEDB903 : Christian Albrecht ; {v['country_populations']['HLN']:,} habitants techniques.",f"2. HKI — xEDB902 : Christian Friedrich Karl ; {v['country_populations']['HKI']:,} habitants techniques.",'Les noms des pays sont sélectionnables ; aucun locator de ville ou de bâtiment n’est déplacé.','Les deux princes restent des membres impériaux non électeurs, sans sujétion dynastique inventée.','Contrôler drapeaux, titres, lois, marché, subsistance, profils et droits du journal impérial.','Aucun nouveau bâtiment, PM, régiment, plafond de ressource ou corridor.','Ne pas attendre les autres branches Hohenlohe, Castell, Wertheim ou les villes encore absentes.','Puis laisser passer un mois : surveiller erreurs, bloc impérial, neuf électeurs et contributions.','R2-B est validé manuellement ; les ajouts R3-A1 ne le sont pas encore.']
    for i,n in enumerate(notes):d.text((25,625+i*34),n,font=font,fill='#233849')
    guide.save(OUT/'PLAYER_LOCATION_GUIDE.png');print('Two maps rendered',flush=True)

def tables():
    g=load('GEOMETRY.json');v=load('VALIDATION.json');inventory=[]
    atlas='https://www.leo-bw.de/media/kgl_atlas/current/delivered/pdf/HABW_6_6.pdf'
    vector='https://commons.wikimedia.org/wiki/File:HkDE-wt_Gerabronn_1800.svg'
    def add(name,tag,ruler,status,government,notes,source,cls='C_GEOMETRIE',rgb=None):
        inventory.append(dict(Juridiction=name,TAG=tag,Souverain_1776=ruler,Gouvernement=government,Statut=status,Certitude=cls,Population_technique=v['country_populations'].get(tag),RGB=rgb,Observations=notes,Source=source))
    for name,tag,ruler,rgb in [('Hohenlohe-Langenbourg','HLN','Christian Albrecht, né 1726-03-27','xEDB903'),('Hohenlohe-Kirchberg','HKI','Christian Friedrich Karl, né 1729-10-19','xEDB902')]:
        add(name,tag,ruler,'NOYAU_INSTALLE_R3_A1_FRANGES_OUVERTES','Principauté héréditaire impériale autonome, non électorale','Seul noyau central installé ; possessions détachées et franges restent à tracer. Aucune vassalité native ou union personnelle entre branches. Capitale technique STATE_FRANCONIA/72 ; démographie provisoire.',atlas+'; '+vector+'; https://www.deutsche-biographie.de/'+('gnd104194847.html' if tag=='HLN' else 'pnd102556490.html'),'A_INSTITUTION_B_GEOMETRIE',rgb)
    add('Hohenlohe-Öhringen',None,'Ludwig Friedrich Karl','DIFFERE','Principauté','Öhringen-ville encore partagée avant la vente de 1782 ; ne pas appliquer la ville unifiée de 1800. Résidu WUR x100060 non transféré.',atlas)
    add('Hohenlohe-Ingelfingen',None,'Heinrich August','DIFFERE','Principauté, titre recoupé 1764','Ne pas utiliser le successeur Friedrich Ludwig en 1776. Schrozberg et propriétés dispersées demandent un tracé distinct ; part de Niedernhall acquise en 1799 exclue.',atlas+'; https://www.deutsche-biographie.de/pnd13760162X.html')
    add('Hohenlohe-Bartenstein',None,'Ludwig Leopold','DIFFERE','Principauté catholique, sujets de confessions diverses','Noyau identifié, mais non ajouté pour isoler le premier test. Werdeck 1797 et Jagstberg 1803 exclus. Pfedelbach/Mainhardt et Untergröningen ne sont pas automatiquement ajoutés.',atlas)
    add('Hohenlohe-Schillingsfürst',None,'Karl Albrecht I','DIFFERE','Principauté catholique','Noyau diagnostique sous ANS xEDA217 déjà traité. Pas de prélèvement automatique dans un noyau accepté. Possessions de Waldenburg à distinguer du siège de Schillingsfürst.',atlas)
    add('Hohenlohe-Waldenburg',None,'Pas de souverain distinct de la branche de Schillingsfürst démontré','PAS_DE_TAG_AUTOMATIQUE','Ancienne lignée éteinte ; possession dynastique/administration','Ancienne lignée éteinte 1679 ; branche jeune de Waldenburg 1807 hors période. Les Ämter de Waldenburg ne prouvent pas un septième État indépendant en 1776.',atlas,'A_EXCLUSION_ANACHRONISME')
    add('Castell-Remlingen',None,'Albrecht Friedrich Carl mineur ; tutelle à préciser','R3_B_EN_ATTENTE','Comté, pas principauté de 1901','Continuité du comté recoupée ; ne pas importer Gleißenberg/Burghaslach 1778 ni Breitenlohe 1782/83. Diagnostic Castell sous WZB x0B0DBA ; noyau antérieur protégé.','https://www.deutsche-biographie.de/sfz8048.html; https://castell.de/media/56/da/d5/1703236788/Casteller_Nachrichten_53_2023_web_.pdf')
    add('Castell-Rüdenhausen, ancienne lignée',None,'Règne et régence à dater avant installation','R3_B_EN_ATTENTE','Comté','Ne pas confondre ancienne lignée avec la nouvelle branche issue de Remlingen en 1803. Condominiums à délimiter, pas de nouveau pays par simple nom.','https://www.deutsche-biographie.de/sfz8048.html')
    add('Löwenstein-Wertheim-Virneburg',None,'Pluralité des titulaires à vérifier','R3_B_EN_ATTENTE','Branche comtale protestante','Souveraineté, coseigneuries et juridictions communes à séparer. Freudenberg comme nom de branche de 1813 exclu.','https://www.landesarchiv-bw.de/de/themen/praesentationen---themenzugaenge/71708')
    add('Löwenstein-Wertheim-Rochefort',None,'Souverain de 1776 à vérifier avant installation','R3_B_EN_ATTENTE','Branche princière catholique, élévation 1711','Rosenberg comme nom de branche de 1813 exclu. Ne pas accorder les compensations de 1803. Diagnostic Wertheim sous BAV xEDA206 ; pas de transfert aveugle du RGB.','https://www.landesarchiv-bw.de/de/themen/praesentationen---themenzugaenge/71708; https://www.historisches-lexikon-bayerns.de/Lexikon/Wertheim%2C_Grafschaft')
    for name,owner,rgb in [('Rothenburg ob der Tauber','ANS','xEDA217'),('Schweinfurt','WZB','xA55FB1'),('Windsheim','ANS','xEDA217'),('Weißenburg','BAV','x010AD7')]:
        add(name,None,'Conseil urbain ; titulaires non nécessaires sans nouveau pays','R3_C_EN_ATTENTE','Ville impériale','Pas de pays distinct trouvé dans les définitions effectives. Point géographique diagnostique sous '+owner+' / '+rgb+' ; position de ville ≠ souveraineté du RGB entier. Ne pas défaire les anciens noyaux.','MAP2L/FRANCONIA/EVIDENCE; MAP2L/GEOMETRY/Homann_reading.jpg; https://www.historisches-lexikon-bayerns.de/Lexikon/Staatsgebiet_%2819./20._Jahrhundert%29',rgb=rgb)
    for name,notes in [('Limpurg et successions','Droits partagés, parts de Bartenstein et autres coseigneurs à distinguer ; pas de pays agrégé automatique.'),('Schwarzenberg / Seinsheim','Possessions fragmentées non délimitées dans cette première installation.'),('Comburg et autres prévôtés','Immédiateté, tutelle épiscopale et contrôle territorial à recouper ; abbaye ou chapitre ne prouve pas un État autonome.')]:add(name,None,'Non vérifié pour création','R3_C_EN_ATTENTE','Statut territorial non finalisé',notes,atlas+'; anciens dossiers FRANCONIA')
    add('Ansbach, Bayreuth, Bamberg, Würzburg, Nuremberg, Eichstätt, Cobourg','ANS/FBM/WZB/NUR/EIC/COB','Conservés dans les historiques existants','DEJA_TRAITES_PRESERVES','Institutions antérieures conservées','Anciennes passes et propriétaires effectifs relus ; aucun nouveau partage de leurs noyaux acceptés. Nuremberg a déjà un pays distinct, pas de doublon.','MAP2L/FRANCONIA/REPORT.md; MAP2L/FRANCONIA_CONTINUATION/REPORT.md','HERITE_SANS_NOUVELLE_CERTIFICATION')
    discrepancies=[dict(Juridiction=r['Juridiction'],Probleme=('Noyau autonome absent, auparavant résidu BAV' if r['TAG'] in g['new_members'] else r['Observations']),Action=r['Statut'],Certitude=r['Certitude'],Source=r['Source']) for r in inventory]
    unresolved=[dict(Juridiction=r['Juridiction'],Probleme=r['Observations'],Etape=r['Statut'],Source=r['Source']) for r in inventory if r['Statut'] not in {'DEJA_TRAITES_PRESERVES','PAS_DE_TAG_AUTOMATIQUE'}]
    unresolved.extend([dict(Juridiction='Géoréférencement et frontière de cellule',Probleme='Contrôles de feuille contre modèle hérité : pas une mesure indépendante de la position réelle dans le bitmap. Les cellules de bord peuvent empiéter ; catégorie B, pas A cadastrale.',Etape='GENERALISATION_DOCUMENTEE',Source='SOURCE_ALIGNMENT.json; SOURCE_ACCEPTED_REVIEW.png'),dict(Juridiction='Démographie, économie et drapeaux',Probleme='Populations techniques et armes dynastiques simplifiées communes. Aucun recensement 1776 validé ; bâtiments et emplois non redistribués par aire. Tester subsistance et accès au marché.',Etape='A_VERIFIER_EN_JEU',Source='ALLOCATION.json; RUNTIME_PROTOCOL.md')])
    changes=[]
    for r in g['assignments']:
        changes.append(dict(Type='TRANSFERT' if r['owner']!='BAV' else 'RESIDU_TECHNIQUE',Territoire=';'.join(r['territories']) or 'Résidu bavarois non certifié',Avant='BAV',Apres=r['owner'],State_ID='STATE_FRANCONIA',ID_numerique=72,RGB_avant=r['parent_rgb'],RGB_apres=r['rgb'],Cellules=r['pixels'],Population=v['country_populations'].get(r['owner']) if r['owner']!='BAV' else None,Certitude=r['confidence'],Source=vector+'; '+atlas))
    for row in load('ALLOCATION.json')['profiles']:
        for tag,n in row['after'].items():
            if tag=='BAV' or not n:continue
            changes.append(dict(Type='POPULATION_PAR_PROFIL',Territoire=row['culture']+' / '+row['religion'],Avant='BAV',Apres=tag,State_ID='STATE_FRANCONIA',ID_numerique=72,RGB_avant=None,RGB_apres=None,Cellules=None,Population=n,Certitude='TECHNIQUE_NON_RECENSEMENT',Source='ALLOCATION.json'))
    changes.sort(key=lambda r:({'TRANSFERT':0,'POPULATION_PAR_PROFIL':1,'RESIDU_TECHNIQUE':2}[r['Type']],r['Apres'],r['RGB_apres'] or ''))
    datasets={}
    for name,rows in [('INVENTORY_1776.csv',inventory),('DISCREPANCIES.csv',discrepancies),('UNRESOLVED.csv',unresolved),('TERRITORIAL_CHANGES.csv',changes)]:datasets[name]=dict(fields=list(rows[0]),rows=rows)
    dump('CSV_TABLES.json',datasets);print({k:len(t['rows']) for k,t in datasets.items()},flush=True)

def csv_verify():
    old=prior.OUT;prior.OUT=OUT
    try:prior.csv_verify()
    finally:prior.OUT=old

def references():
    needed={'common/technology/technologies':set(),'common/laws':set(),'common/scripted_effects':{'change_to_hereditary','post_change_to_hereditary'},'common/cultures':{'south_german'},'common/religions':{'protestant'},'common/interest_groups':{'ig_landowners'},'common/ideologies':{'ideology_traditionalist'},'common/government_types':{'gov_aor1776_map2w_r3_hohenlohe'},'common/coat_of_arms/coat_of_arms':{'aor1776_map2w_r3_hohenlohe'}}
    for tag in ['hln','hki']:
        raw=(ROOT/f'common/history/countries/{tag} - map2w_r3.txt').read_text(encoding='utf-8-sig')
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
    dump('REFERENCE_VALIDATION.json',dict(status='PASS',references=found,canonical_game='C:/Games/Victoria 3/game',runtime_execution=False));print('Effective references PASS',flush=True)

def tests():
    import io,time,unittest
    groups={'R3_current':['test_map2w_r3_franconia'],'cumulative_contracts':['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon'],'earlier_delivery_receipts':['test_map2w_west_south','test_map2w_r2_hesse_nassau'],'R2B_stage_receipt':['test_map2w_r2b_completion'],'TU_old_stage_snapshots':['test_map2t_saxony','test_map2u_thuringia']};results={}
    for name,modules in groups.items():
        stream=io.StringIO();start=time.monotonic();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestLoader().loadTestsFromNames(modules));results[name]=dict(modules=modules,tests=r.testsRun,failures=[t.id() for t,_ in r.failures],errors=[t.id() for t,_ in r.errors],seconds=round(time.monotonic()-start,2),output=stream.getvalue());print(name,r.testsRun,'failures',len(r.failures),'errors',len(r.errors),flush=True)
    dump('TESTS.json',results)
    expected=json.loads((prior.OUT/'EARLIER_TEST_COMPARISON.json').read_text())['failure_ids']
    actual=results['TU_old_stage_snapshots']['failures']+results['TU_old_stage_snapshots']['errors'];extra=sorted(set(actual)-set(expected))
    stage_expected=['test_map2w_r2b_completion.HesseNassauCompletion.test_registry_guard_accepts_current_layer'] if (OUT/'REGISTRY_MIGRATION.json').exists() else []
    # That old assertion deliberately pins R2B as the last layer. R3 is now
    # the last layer; no historical baseline or old test is rewritten.
    stage_actual=results['R2B_stage_receipt']['failures']+results['R2B_stage_receipt']['errors']
    dump('EARLIER_TEST_COMPARISON.json',dict(old_TU_failure_identifiers=actual,new_TU_failure_identifiers=extra,R2B_stage_only_expected=stage_expected,R2B_stage_actual=stage_actual,old_baselines_rewritten=False,explanation='After withdrawal R2B is again the last approved layer. Nine retained T/U exact-stage mismatches; no additional failure identifiers.'))
    assert not extra and set(actual)==set(expected) and stage_actual==stage_expected
    assert all(not results[k]['failures'] and not results[k]['errors'] for k in ['R3_current','cumulative_contracts','earlier_delivery_receipts'])

def tidy():
    files=load('EXPECTED_TEXT.json');rel='common/history/pops/00_west_europe.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert raw==files[rel]
    # Only the two separators introduced by append; no blanket formatting of
    # earlier or collaborator-authored histories.
    lines=raw.splitlines(keepends=True)
    for i in [3165,3190]:assert lines[i-1].strip()=='';lines[i-1]='\n'
    raw=''.join(lines);files[rel]=raw;dump('EXPECTED_TEXT.json',files);core.OUT=OUT;core.emit({rel:raw},'WHITESPACE.patch')

def close():
    v=load('VALIDATION.json');tests=load('TESTS.json');assert v['passed']==v['total']
    assert load('REFERENCE_VALIDATION.json')['status']=='PASS'
    assert all(not tests[k]['failures'] and not tests[k]['errors'] for k in ['R3_current','cumulative_contracts','earlier_delivery_receipts'])
    assert not load('EARLIER_TEST_COMPARISON.json')['new_TU_failure_identifiers']
    for row in load('CSV_REREAD.json'):assert core.sha(OUT/row['file'])==row['sha256']
    manifest=load('INSTALLED_MANIFEST.json');assert all(core.sha(ROOT/p)==h for p,h in manifest['functional_files'].items())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==manifest['git_head']
    assert core.sha(ROOT/'.git/index')==manifest['git_index_sha256']
    v.update(tests={k:{field:r[field] for field in ['tests','failures','errors']} for k,r in tests.items()},reference_validation='PASS',csv_validation='PASS_EVERY_CELL_REREAD',visual_review='BEFORE_AFTER_PLAYER_GUIDE_SOURCE_FOOTPRINTS_AND_FOUR_TABLE_PREVIEWS_REVIEWED',territorial_transfers={'HLN':3,'HKI':4},new_RGBs=4,registered_RGBs=571,prior_manual_R2B_attestation='R2B/RUNTIME_USER_ATTESTATION.json',new_R3_runtime_accepted=False,final_manifest_hashes='PASS')
    dump('VALIDATION.json',v);print('R3-A1 delivery closed; first sublot ready, no runtime claim',flush=True)

def withdraw_prepare():
    """Revert our candidate only, after checking its exact installed hashes."""
    b=load('BASELINE.json');manifest=load('INSTALLED_MANIFEST.json')
    assert all(core.sha(ROOT/p)==h for p,h in manifest['functional_files'].items()),'Concurrent write: stop, do not overwrite'
    candidate=load('VALIDATION.json');candidate.update(superseded=True,geographic_acceptance='WITHDRAWN_LOCAL_REFERENCE_CONTRADICTION',engine_execution=False)
    dump('CANDIDATE_STATIC_VALIDATION.json',candidate);dump('CANDIDATE_TESTS.json',load('TESTS.json'));dump('CANDIDATE_INSTALLED_MANIFEST.json',manifest)
    dump('PROPOSED_REGISTRY_MIGRATION.json',load('REGISTRY_MIGRATION.json'));files={}
    imperial_previous=json.loads((prior.OUT/'IMPERIAL_EXPECTED.json').read_text(encoding='utf8'))
    planned=load('EXPECTED_TEXT.json');new_paths=[]
    for p in manifest['functional_files']:
        if p.endswith('.png') or p.endswith('.dds'):continue
        if p in imperial_previous:files[p]=imperial_previous[p]
        elif p in b['originals']:files[p]=b['originals'][p]
        elif p==core.active_registry_path().relative_to(ROOT).as_posix():files[p]=json.dumps(b['registry'],ensure_ascii=False,indent=2)+'\n'
        elif p=='map_data/province_terrains.txt':
            raw=(ROOT/p).read_text(encoding='utf-8-sig')
            for row in load('GEOMETRY.json')['new_provinces']:
                pattern=r'(?m)^'+row['rgb']+r'="[^"\n]+"\n';raw,n=re.subn(pattern,'',raw);assert n==1
            files[p]=raw
        elif p not in b['hashes']:
            assert p in planned and (ROOT/p).read_text(encoding='utf-8-sig')==planned[p].lstrip('\ufeff');new_paths.append(p)
        else:raise AssertionError('Missing prior text '+p)
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(b['registry'],ensure_ascii=False,indent=2)+'\n'
    files['tools/map2l_registry.py']=b['registry_tool']
    core.OUT=OUT;patches=[]
    for i,(p,raw) in enumerate(files.items()):
        name=f'WITHDRAW_{i}.patch';core.emit({p:raw},name);patches.append(name)
    for i,p in enumerate(new_paths+[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]):
        name=f'WITHDRAW_DELETE_{i}.patch';(OUT/name).write_text('*** Begin Patch\n*** Delete File: '+str(ROOT/p)+'\n*** End Patch\n',encoding='utf8');patches.append(name)
    dump('WITHDRAW_PATCHES.json',patches);dump('WITHDRAWAL_PLAN.json',dict(preserved_baseline_sha256=core.sha(OUT/'BASELINE.json'),deleted_own_candidate_files=new_paths,patches=patches,reason='Independent reference contradiction exceeds 2–3-cell proposed cores; not a certified city positional error. No previous accepted work is reverted.',only_candidate_hash_verified=True))
    from georeference.model import forward
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    controls=[('Wurzburg',9.9296,49.7913,[4322.24,861.541]),('Nuremberg',11.0767,49.4521,[4351.554,877.18]),('Bayreuth',11.5783,49.9456,[4362.608,862.394]),('Regensburg',12.1011,49.0134,[4373.729,892.864])]
    dump('NATIVE_REFERENCE_CONTRADICTION.json',dict(status='UNRESOLVED_REFERENCE_DISAGREEMENT_NOT_CERTIFIED_CITY_ERROR',source_old='MAP2L/FRANCONIA/ALIGNMENT.json',source_new='MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json',rows=[dict(name=n,geo_diagnostic=[lo,la],old_native_reference=p,new_diagnostic=forward(model,[[lo,la]])[0].tolist(),disagreement_pixels=float(np.linalg.norm(forward(model,[[lo,la]])[0]-p))) for n,lo,la,p in controls],consequence='The tiny proposed cores cannot be assigned B geographic confidence without independent local homologous landmarks. Do not average, translate arbitrarily or treat hub names as exact observations.',no_new_fit_performed=True))
    print('Withdrawal prepared for',len(files),'existing text files and',len(new_paths),'own new runtime files. Baseline and all previous lots preserved.',flush=True)

def withdraw_bitmap():
    b=load('BASELINE.json');candidate=load('CANDIDATE_INSTALLED_MANIFEST.json')
    assert core.sha(ROOT/'map_data/provinces.png')==candidate['bitmap_sha256']
    subprocess.run(['powershell','-NoProfile','-Command',"Copy-Item -LiteralPath '"+str(ROOT/b['bitmap_backup'])+"' -Destination '"+str(ROOT/'map_data/provinces.png')+"' -ErrorAction Stop"],check=True)
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256'];print('Only candidate bitmap delta removed',flush=True)

def withdrawn_validate():
    b=load('BASELINE.json');inv=core.qa.inventory();current=q.economy.runtime_hashes();changes=[p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)]
    checks=[dict(name='Full runtime inventory equals pre-R3 capture',passed=inv==b['inventory']),dict(name='All pre-existing runtime file hashes and file set preserved',passed=not changes,detail=changes),dict(name='Exact baseline bitmap',passed=core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']),dict(name='Original registry guard text retained',passed=(ROOT/'tools/map2l_registry.py').read_text(encoding='utf8')==b['registry_tool']),dict(name='HEAD preserved',passed=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head']),dict(name='Index preserved',passed=core.sha(ROOT/'.git/index')==b['git_index_sha256']),dict(name='No active R3 migration',passed=not (OUT/'REGISTRY_MIGRATION.json').exists())]
    result=dict(status='MAP2W_R3_BLOCKED',cause='NATIVE_REFERENCE_CONTRADICTION',runtime_status='NOT_APPLICABLE_NO_R3_INSTALLED',territorial_transfers_applied=0,new_countries_installed=[],new_RGBs_installed=[],retained_candidate_transfers={'HLN':3,'HKI':4},candidate_status='WITHDRAWN_NOT_INSTALLED_NOT_APPROVED',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,world_before=sum(r['count'] for r in b['inventory']['pops']),world_after=sum(r['count'] for r in inv['pops']),preexisting_duplicate_RGBs=len(inv['duplicates']),preexisting_invalid_references=inv['errors'],new_errors=[r for r in inv['errors'] if r not in b['inventory']['errors']],manual_R2B_validation_recorded=True,manual_R3_validation=False,git_head=b['git_head'],git_index_sha256=b['git_index_sha256'])
    dump('VALIDATION.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2W-R3',status='NO_TERRITORIAL_INSTALL',functional_files={},bitmap_sha256=b['bitmap_sha256'],git_head=b['git_head'],git_index_sha256=b['git_index_sha256'],additive_runtime_attestation='../R2B/RUNTIME_USER_ATTESTATION.json'))
    print(result['status'],result['passed'],'/',result['total'],changes,flush=True)
    assert all(c['passed'] for c in checks)

def blocked_tables():
    datasets=load('CSV_TABLES.json');names={'Hohenlohe-Langenbourg','Hohenlohe-Kirchberg'}
    for row in datasets['INVENTORY_1776.csv']['rows']:
        if row['Juridiction'] in names:
            row.update(Statut='CANDIDAT_RETIRE_NON_INSTALLE',Certitude='A_INSTITUTION_C_CALAGE_BITMAP',Population_technique=None,RGB=None,Observations='Noyau proposé retiré : contradiction entre référentiels supérieure à la largeur du territoire proposé. Aucun TAG, RGB ou population supplémentaire installé. Voir NATIVE_REFERENCE_CONTRADICTION.json.')
    for row in datasets['DISCREPANCIES.csv']['rows']:
        if row['Juridiction'] in names:row.update(Probleme='Modèle diagnostique et repères de la passe franconienne antérieure divergent. Position du petit noyau non vérifiée indépendamment.',Action='AUCUN_TRANSFERT_CANDIDAT_RETIRE',Certitude='C_CALAGE')
    for row in datasets['UNRESOLVED.csv']['rows']:
        if row['Juridiction'] in names:row.update(Probleme='Correspondance géographique non résolue ; ancien candidat retiré intégralement. Rechercher des homologues locaux indépendants, sans translation automatique ni confusion erreur de modèle/placement du hub.',Etape='BLOQUE_NON_INSTALLE',Source='NATIVE_REFERENCE_CONTRADICTION.json; SOURCE_ALIGNMENT.json')
        elif row['Juridiction']=='Démographie, économie et drapeaux':row.update(Probleme='Allocations et armoiries du candidat retirées ; population, bâtiments, économie et unités identiques à la capture avant R3.',Etape='AUCUNE_MODIFICATION_ACTIVE')
    row=dict(Type='AUCUN_TRANSFERT_R3',Territoire='Langenbourg et Kirchberg : candidat retiré',Avant='BAV',Apres='BAV',State_ID='STATE_FRANCONIA',ID_numerique=72,RGB_avant='xEDA218',RGB_apres='xEDA218',Cellules=0,Population=0,Certitude='C_CALAGE_NON_INSTALLE',Source='NATIVE_REFERENCE_CONTRADICTION.json; VALIDATION.json')
    datasets['TERRITORIAL_CHANGES.csv']=dict(fields=list(row),rows=[row]);dump('CSV_TABLES.json',datasets);print('Four tables now describe final blocked state; no transfer claimed',flush=True)

def blocked_docs():
    files={};files[(OUT/'CANDIDATE_REPORT_WITHDRAWN.md').relative_to(ROOT).as_posix()]='# ARCHIVE — CANDIDAT RETIRÉ, NON LIVRÉ\n\nLe texte ci-dessous décrit un candidat installé puis intégralement retiré après découverte d’une contradiction de calage. Il ne décrit pas le mod livré. Le statut courant est MAP2W_R3_BLOCKED ; voir REPORT.md et VALIDATION.json.\n\n'+(OUT/'REPORT.md').read_text(encoding='utf8')
    report='''# MAP-2W-R3 — Livraison bloquée par une contradiction de calage

Date : 18 octobre 2026. Référence historique : 1er janvier 1776.

**Statut final : MAP2W_R3_BLOCKED. Aucun transfert territorial R3 installé.**

## Ce qui a été achevé

La validation manuelle R2-B est enregistrée dans `../R2B/RUNTIME_USER_ATTESTATION.json` : nouvelle partie 1776, neuf points contrôlés, un mois de simulation, aucune anomalie déclarée. Ce n’est pas un test moteur automatisé ni une validation des frontières C ou de R3.

Les anciennes passes franconiennes et les fichiers actuels ont été confrontés avant la préparation : Ansbach, Bayreuth, Bamberg, Würzburg, Nuremberg, Eichstätt et Cobourg sont déjà traités. Aucun de ces noyaux n’est reconstruit depuis zéro. Un inventaire ciblé de 19 entrées distingue les branches de Hohenlohe, Castell, Löwenstein-Wertheim, quatre villes impériales et autres juridictions. Les sources indépendantes et les anachronismes sont documentés dans `HISTORICAL_EVIDENCE.md`.

## Candidat retiré et cause précise

Un premier candidat concernait **Langenbourg (HLN, trois cellules) et Kirchberg (HKI, quatre cellules)**, à partir du résidu bavarois xEDA218 de STATE_FRANCONIA / 72. La préparation avait ajouté les pays, les princes, quatre RGB, leurs profils démographiques et leurs dépendances impériales. **Ces ajouts ont tous été retirés ; HLN/HKI et xEDB900–xEDB903 ne sont pas actifs.**

Les contrôles syntaxiques et de conservation passaient : 1 625 contrôles, 28 tests ciblés, 67 contrats impériaux et 40 tests de livraisons. Cela ne suffisait pas à valider la géographie.

La dernière confrontation a révélé un désaccord entre le modèle Miller diagnostique hérité et les repères natifs utilisés dans l’ancienne passe franconienne : environ **7,57 pixels à Würzburg, 2,29 à Nuremberg, 1,99 à Bayreuth et 4,97 à Ratisbonne**. Ces valeurs mesurent une **contradiction entre référentiels**, pas une erreur certifiée de position des villes : les anciens hubs ne doivent pas davantage être supposés exacts.

Pour un noyau de deux ou trois cellules de large, ce désaccord rend l’attribution géographique insuffisante. Le faible écart de la feuille Gerabronn/Schrozberg contre le même modèle diagnostique (0,079/0,222 pixel) ne prouve pas sa justesse dans le jeu. Aucun déplacement moyen ou translation arbitraire n’a été appliqué. Aucune nouvelle optimisation d’Erfurt–Eichsfeld.

Voir `NATIVE_REFERENCE_CONTRADICTION.json`, `SOURCE_ALIGNMENT.json` et les cartes explicitement marquées **CANDIDAT RETIRÉ / NON INSTALLÉ**. `CANDIDATE_STATIC_VALIDATION.json` et `CANDIDATE_TESTS.json` sont des archives d’un essai retiré, non des attestations de livraison.

## État réellement livré et protections

**Zéro province transférée, zéro nouveau TAG, zéro nouveau RGB, aucun changement démographique ou économique actif.** Total mondial : **835 801 255**. Registre impérial : **567 RGB**, neuf électeurs conservés.

Le retrait a été limité aux fichiers créés ou modifiés par cet essai, après vérification de leurs empreintes. Les dix nouveaux fichiers fonctionnels propres au candidat ont été supprimés ; leurs textes restent récupérables dans `EXPECTED_TEXT.json` et les patches de préparation. La carte et les fichiers partagés ont retrouvé exactement leurs empreintes d’avant R3. Les modifications préexistantes et concurrentes n’ont pas été effacées. `WITHDRAWAL_PLAN.json` décrit cette opération ; `VALIDATION.json` vérifie l’égalité de l’inventaire mondial et de toutes les empreintes fonctionnelles avec la capture R3.

Les 44 doublons RGB et 12 références invalides préexistants restent ouverts, sans nouvelle anomalie. Populations, cultures, religions, bâtiments, propriétaires économiques, unités, papeteries, économie française, Saint-Gobain, Anzin, Saint-Domingue et mécaniques impériales sont conservés. HEAD et index inchangés ; aucun staging, commit, merge, reset, rebase, changement de branche ou push. Aucun fichier de l’installation vanilla modifié.

## Dépendance qui manque pour installer R3-A

Il faut des repères **physiques locaux homologues** dans la région Jagst–Kocher / Langenbourg–Kirchberg, observés à la fois dans une source géographique et dans les données natives du bitmap, puis un contrôle indépendant non ajusté. L’alternative est une correspondance locale documentée entre la source détaillée et un ancien calage dont les ancrages physiques sont eux-mêmes vérifiés. Une simple proximité de ville, un nom de locator ou la moyenne des écarts ne suffit pas.

La souveraineté des deux branches est établie ; leur correspondance exacte avec ces petites cellules ne l’est pas. Castell, Wertheim et les villes impériales ne sont pas installés dans un autre référentiel pour contourner ce problème. Les droits partagés d’Öhringen avant 1782, l’ancienne lignée Waldenburg, les gains de 1797/1799/1803 et les condominiums restent distincts dans l’inventaire.

## Livrables et vérification

`INVENTORY_1776.csv`, `DISCREPANCIES.csv`, `UNRESOLVED.csv`, `TERRITORIAL_CHANGES.csv` décrivent l’état final, sans transfert revendiqué. Le rapport démographique du candidat reste dans `ALLOCATION.json`, non appliqué. Carte comparative et `PLAYER_LOCATION_GUIDE.png` montrent uniquement les propositions retirées, pas des pays à chercher en partie.

**Aucun nouveau test en jeu n’est demandé pour R3 : il n’y a rien d’installé à accepter.** La prochaine action utile est la résolution locale de la contradiction, non un mois de simulation. Le statut ne doit pas être changé en READY ou PASS_RUNTIME_USER_VALIDATED sur la seule base des anciens contrôles statiques.

## Mesure de ColGrep

Un appel local `C:\\Users\\simeo\\.cargo\\bin\\colgrep.exe --agent "Locate retained historical map sources and unimplemented territorial decisions specifically for Hohenlohe branches, Castell and Wertheim, and Rothenburg Schweinfurt Windsheim Weissenburg. Old FRANCONIA/TRACING and FRANCONIA_CONTINUATION are known installed cores; do not return them alone. Return at most five useful paths with line ranges, no edits and no historical decisions." .`

Sortie 0 ; **250,793 secondes**. Les résultats, relus, étaient surtout des fichiers déjà connus et un générateur de rapport trop large : aucune nouvelle source décisive ni recherche évitée démontrée. Le journal ne prouve pas indépendamment quel GGUF/backend a été chargé. Aucun modèle ou paramètre changé, aucune reconstruction forcée d’index. Tokens Codex et nombre exact de recherches classiques non instrumentés ; aucune économie de quota chiffrée revendiquée. L’agent local n’est pas responsable de la décision cartographique : l’insuffisance du premier calage a été détectée et traitée par Codex.
'''
    files[(OUT/'REPORT.md').relative_to(ROOT).as_posix()]=report
    files[(OUT/'RUNTIME_PROTOCOL.md').relative_to(ROOT).as_posix()]='# R3 — Aucun contrôle de nouvelle partie requis\n\nStatut final : **MAP2W_R3_BLOCKED**. Les ajouts de Langenbourg/Kirchberg ont été retirés. Ne pas chercher HLN/HKI dans cette version et ne pas attester leur fonctionnement.\n\nLa validation manuelle R2-B reste enregistrée et valable dans son périmètre. Les anciennes corrections sont conservées.\n\nProchaine étape utile : homologues physiques locaux indépendants pour départager les référentiels autour de la Jagst et du Kocher ; aucune translation arbitraire ni simple confiance dans les noms de hubs. Après une installation future justifiée, créer un nouveau protocole limité à ses changements.\n'
    original=(ROOT/'tools/test_map2w_r3_franconia.py').read_text(encoding='utf8');files[(OUT/'CANDIDATE_TEST_SOURCE_WITHDRAWN.py').relative_to(ROOT).as_posix()]=original
    files['tools/test_map2w_r3_franconia.py']='''"""Final R3 protection checks after withdrawing unaccepted geometry."""
import json,unittest
import map2w_r3_franconia as w
class WithdrawnR3Tests(unittest.TestCase):
    def test_final_blocked_status(self):self.assertEqual(w.load('VALIDATION.json')['status'],'MAP2W_R3_BLOCKED')
    def test_all_protection_checks(self):
        v=w.load('VALIDATION.json');self.assertEqual(v['passed'],v['total'])
    def test_no_country_or_colour_installed(self):
        v=w.load('VALIDATION.json');self.assertFalse(v['new_countries_installed']);self.assertFalse(v['new_RGBs_installed']);self.assertEqual(v['territorial_transfers_applied'],0)
    def test_no_active_migration(self):self.assertFalse((w.OUT/'REGISTRY_MIGRATION.json').exists())
    def test_proposed_migration_is_not_approved(self):
        import map2l_registry as r
        self.assertNotIn(w.OUT,r.approved_lot_dirs())
    def test_population_conserved(self):self.assertEqual(w.load('VALIDATION.json')['world_after'],835801255)
    def test_no_r3_runtime_claim(self):self.assertFalse(w.load('VALIDATION.json')['manual_R3_validation'])
    def test_r2b_attestation_preserved(self):
        r=json.loads((w.OUT.parent/'R2B/RUNTIME_USER_ATTESTATION.json').read_text());self.assertEqual(r['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertFalse(r['R3_changes_covered'])
    def test_no_install_without_new_evidence(self):
        with self.assertRaises(RuntimeError):w.install()
    def test_no_prepare_without_new_evidence(self):
        with self.assertRaises(RuntimeError):w.prepare()
    def test_contradiction_not_certified_city_error(self):self.assertEqual(w.load('NATIVE_REFERENCE_CONTRADICTION.json')['status'],'UNRESOLVED_REFERENCE_DISAGREEMENT_NOT_CERTIFIED_CITY_ERROR')
    def test_candidate_archived_not_accepted(self):self.assertEqual(w.load('CANDIDATE_STATIC_VALIDATION.json')['geographic_acceptance'],'WITHDRAWN_LOCAL_REFERENCE_CONTRADICTION')
if __name__=='__main__':unittest.main()
'''
    core.OUT=OUT;patches=[]
    for i,(rel,raw) in enumerate(files.items()):
        name=f'FINAL_DOC_{i}.patch';core.emit({rel:raw},name);patches.append(name)
    dump('FINAL_DOC_PATCHES.json',patches)

def blocked_maps():
    font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',24)
    for name in ['BEFORE_AFTER.png','PLAYER_LOCATION_GUIDE.png','SOURCE_ACCEPTED_REVIEW.png']:
        im=Image.open(OUT/name).convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,72),fill='#9b2020');d.text((15,9),'CANDIDAT RETIRÉ — NON INSTALLÉ',font=font,fill='white');d.text((15,40),'Calage contradictoire : aucune nouvelle validation en jeu requise',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19),fill='white')
        if name=='PLAYER_LOCATION_GUIDE.png':
            d.rectangle((0,605,im.width,im.height),fill='#fff8f4');d.text((25,640),'Ces deux pays ne sont pas présents dans la livraison R3.',font=font,fill='#9b2020');d.text((25,690),'Tous les ajouts du candidat ont été retirés ; les anciennes passes sont conservées.',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19),fill='black');d.text((25,735),'Voir REPORT.md et NATIVE_REFERENCE_CONTRADICTION.json.',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19),fill='black')
        im.save(OUT/name)

def blocked_close():
    v=load('VALIDATION.json');assert v['status']=='MAP2W_R3_BLOCKED' and v['passed']==v['total']
    b=load('BASELINE.json');assert q.economy.runtime_hashes()==b['hashes']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'];assert core.sha(ROOT/'.git/index')==b['git_index_sha256']
    for row in load('CSV_REREAD.json'):assert core.sha(OUT/row['file'])==row['sha256']
    tests=load('TESTS.json');assert all(not tests[k]['failures'] and not tests[k]['errors'] for k in ['R3_current','cumulative_contracts','earlier_delivery_receipts','R2B_stage_receipt'])
    assert not load('EARLIER_TEST_COMPARISON.json')['new_TU_failure_identifiers']
    oldinv=load('CURRENT_INVENTORY.json')
    if 'HLN' in oldinv['countries']:dump('CANDIDATE_INVENTORY_WITHDRAWN.json',oldinv)
    dump('CURRENT_INVENTORY.json',b['inventory'])
    for name in ['GEOMETRY.json','ALLOCATION.json','PLAN.json','PROPOSED_REGISTRY_MIGRATION.json','SOURCE_ALIGNMENT.json']:
        data=load(name);data.update(status='CANDIDATE_WITHDRAWN_NOT_INSTALLED',approved=False,blocker='NATIVE_REFERENCE_CONTRADICTION.json');dump(name,data)
    v.update(tests={k:{field:r[field] for field in ['tests','failures','errors']} for k,r in tests.items()},candidate_validation_superseded='CANDIDATE_STATIC_VALIDATION.json',csv_validation='PASS_EVERY_CELL_REREAD',final_runtime_hash_comparison='ALL_PRE_R3_FILES_BYTE_IDENTICAL',final_visual_review='WITHDRAWAL_BANNERS_AND_FOUR_FINAL_TABLE_PREVIEWS_REVIEWED',no_new_runtime_test_requested=True)
    dump('VALIDATION.json',v);print('Final blocked delivery: 0 installed transfers; baseline hashes, CSVs, Git protections and live contracts PASS',flush=True)
if __name__=='__main__':globals()[sys.argv[1]]()
