"""Scoped Polish-Prussian frontier continuation. No Git writes or vanilla edits."""
from pathlib import Path
import collections,difflib,hashlib,json,re,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2l_belgium import packed,components

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIA_POLAND_2026_11_05'
CANON=OUT.parent
REGIONS={'STATE_WEST_PRUSSIA','STATE_POSEN'}
PRIOR=[CANON/'PRUSSIA_V1_2026_11_02',CANON/'NORTH_SAXONY_1_2026_11_05']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def runtime_hashes():return {p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','events','map_data','gfx','gui','localization'] for p in (ROOT/folder).rglob('*') if p.is_file()}
def capture():
    import serg_closure_roadmap as roadmap
    from map2l_registry import active_registry_path
    OUT.mkdir(exist_ok=True);(OUT/'EVIDENCE').mkdir(exist_ok=True);assert not (OUT/'BASELINE.json').exists()
    originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_bytes().decode('utf-8')
            if any(s in raw for s in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    git={}
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current']),('git_dir',['rev-parse','--absolute-git-dir']),('status',['status','--porcelain=v1'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],capture_output=True,text=True);assert r.returncode==0;git[name]=r.stdout.strip()
    git['index_sha256']=sha(Path(git['git_dir'])/'index')
    (OUT/'provinces_before.png').write_bytes((ROOT/'map_data/provinces.png').read_bytes());(OUT/'ROADMAP_STATE_BEFORE.json').write_bytes((CANON/'ROADMAP_STATE.json').read_bytes())
    state=roadmap.load_json(CANON/'ROADMAP_STATE.json');h=runtime_hashes()
    dump('BASELINE.json',dict(runtime=h,hashes=h,originals=originals,inventory=qa.inventory(),git=git,bitmap_backup=(OUT/'provinces_before.png').relative_to(ROOT).as_posix(),bitmap_sha256=sha(ROOT/'map_data/provinces.png'),
        registry=json.loads(active_registry_path().read_text()),progress=roadmap.progress(state),canonical_check=roadmap.check(),
        previous_delivery={p.relative_to(ROOT).as_posix():sha(p) for folder in PRIOR for p in folder.rglob('*') if p.is_file()},
        archived_polish_proofs={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'docs/reports/map/MAP2M').rglob('*') if p.is_file()},
        previous_tools={n:sha(ROOT/n) for n in ['tools/serg_prussia_v1.py','tools/serg_north_saxony1.py','tools/map2l_registry.py']}))
    print('Captured',len(h),'runtime files;',roadmap.progress(state)['percent'])

TOWNS=[('Dantzig',18.6466,54.352,'PLC'),('Thorn',18.6048,53.0103,'PLC'),('Bromberg',18.0076,53.1235,'PRU'),('Fordon',18.174,53.149,'PRU'),
 ('Inowroclaw',18.2639,52.7931,'PRU'),('Szubin',17.738,53.009,'PRU'),('Znin',17.719,52.85,'PRU'),('Mogilno',17.956,52.657,'PRU'),
 ('Trzemeszno',17.825,52.562,'PLC'),('Gniezno',17.596,52.535,'PLC'),('Poznan',16.9252,52.4064,'PLC'),('Walcz',16.4712,53.2779,'PRU'),('Pila',16.738,53.151,'PRU'),('Kamin',17.528,53.532,'PRU'),
 ('Elbing',19.409,54.152,'PRU'),('Marienwerder',18.933,53.735,'PRU'),('Olsztyn',20.48,53.778,'PRU'),('Plock',19.7,52.546,'PLC'),('Lipno',19.178,52.845,'PLC'),('Rypin',19.410,53.066,'PLC'),('Brodnica',19.403,53.26,'PRU'),('Gorzno',19.643,53.197,'PRU')]
def diagnostics(candidate=False):
    b=load('BASELINE.json');a=packed(OUT/('provinces_candidate.png' if candidate else 'provinces_before.png'));owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    if candidate:owners.update({r['rgb']:r['owner'] for r in load('GEOMETRY.json')['assignments']})
    # Frozen MAP2M R5 local axes; do not refit old controls.
    m=np.array(json.loads((ROOT/'docs/reports/map/MAP2M/R5/TRANSFORMATIONS.json').read_text())['selected_native']['matrix'])
    rows=[];box=(4460,730,4545,800);local=a[730:800,4460:4545];arr=np.full((*local.shape,3),230,dtype=np.uint8)
    for v in np.unique(local):arr[local==v]={'PRU':(118,155,194),'PLC':(223,162,177)}.get(owners.get('x'+format(int(v),'06X')),(220,220,220))
    im=Image.fromarray(arr).resize((1190,980),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for name,lon,lat,wanted in TOWNS:
        x,y=np.array([lon,lat,1])@m;rgb='x'+format(int(a[int(y),int(x)]),'06X');owner=owners.get(rgb);rows.append(dict(name=name,lon=lon,lat=lat,x=float(x),y=float(y),rgb=rgb,owner=owner,expected=wanted,certified_city_position=False))
        px,py=(x-box[0])*14,(y-box[1])*14
        if 0<=px<1190 and 0<=py<980:d.ellipse((px-3,py-3,px+3,py+3),fill='red');d.text((px+4,py),name,font=font,fill='black',stroke_width=1,stroke_fill='white')
        print(name,round(x,2),round(y,2),rgb,owner,wanted)
    suffix='AFTER' if candidate else 'BEFORE';im.save(OUT/('FRONTIER_'+suffix+'.png'));dump('TOWNS_'+suffix+'.json',rows)
    if not candidate:
        focus={'x41A021','xC02121','xFCC7B7','xEDB010','x0180A0','x945000','x80A0A0'};items=[]
        for r in b['inventory']['owners']:
            if r['key'][0] in focus:
                ys,xs=np.where(a==int(r['key'][0][1:],16));items.append(dict(rgb=r['key'][0],state=r['key'][1],owner=r['key'][2],pixels=len(xs),box=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]))
        dump('CURRENT_INVENTORY.json',items);print(items)

def geometry():
    from map2l_franconia import inside
    b=load('BASELINE.json');assert runtime_hashes()==b['runtime'],'Reassess concurrent runtime changes'
    a=packed(OUT/'provinces_before.png');after=a.copy()
    native=np.array(json.loads((ROOT/'docs/reports/map/MAP2M/R5/TRANSFORMATIONS.json').read_text())['selected_native']['matrix'])
    # New primary-sheet reading; the old Pfau and Guessefeld-1775 controls and
    # rejected southern rim are never refitted. Coordinates are on the 4000px
    # copy of the explicitly dated 1780 revised sheet (Netze inset).
    controls=[('Bromberg',2609,289,18.0076,53.1235),('Fordon',2663,260,18.174,53.149),
              ('Inowroclaw',2753,521,18.2639,52.7931),('Mogilno',2622,533,17.956,52.657),
              ('Znin',2526,459,17.719,52.85),('Gniezno',2491,644,17.596,52.535)]
    checks=[('Labyszyn',2612,420,17.92,52.95),('Pakosc',2695,494,18.08,52.802)]
    design=np.array([[x,y,1] for _,x,y,_,_ in controls]);target=np.array([[lon,lat,1] for _,_,_,lon,lat in controls])@native
    matrix=np.linalg.lstsq(design,target,rcond=None)[0]
    # The top of an inset is not a sovereign border. Close the envelope to
    # the north solely as a working extent; its southern/western edge is the
    # boundary reading. Match the dashed line west of Mogilno, not the town
    # cross itself. No later-map southern fringe is automatically annexed.
    outline=[(2300,100),(2665,100),(3040,100),(3040,450),(2990,495),(2940,530),(2940,570),(2890,605),(2870,645),(2860,680),(2830,721),(2790,733),(2745,724),(2720,699),(2708,665),(2690,628),(2670,591),(2630,590),(2600,560),(2580,530),(2555,512),(2530,495),(2510,480),(2488,448),(2465,430),(2430,410),(2390,395),(2300,350)]
    polygon=np.c_[np.array(outline),np.ones(len(outline))]@matrix
    yy,xx=np.mgrid[753:790,4488:4520];points=np.c_[(xx+.5).ravel(),(yy+.5).ravel()]
    mask=inside(points,polygon).reshape(xx.shape)
    # This is a conservative northern core, not the full 1780 boundary.
    # Preserve the uncertain southern countryside and Polish Trzemeszno and
    # Gniezno, rather than retrojecting an entire later map state into 1776.
    mask &= yy<=780
    netze=np.zeros(a.shape,dtype=bool);netze[753:790,4488:4520]=mask & np.isin(a[753:790,4488:4520],[0xFCC7B7,0xC02121])
    thorn_cells=[[4520,766],[4521,766],[4520,767],[4521,767]]
    thorn=np.zeros(a.shape,dtype=bool)
    for x,y in thorn_cells:assert a[y,x]==0x41A021;thorn[y,x]=True
    # Contemporaneous 1775 sheet: southern Culmland/Dobrzyn boundary. Rypin
    # was annexed only in 1793 (municipal chronology), unlike Brodnica and
    # Gorzno. Read the political line, not the whole shared native province.
    dc=[('Thorn',1658,2390,18.6048,53.0103),('Brodnica',1943,2310,19.403,53.26),
        ('Lidzbark',2173,2320,19.826,53.263),('Culm',1535,2155,18.425,53.348)]
    dd=np.array([[x,y,1] for _,x,y,_,_ in dc]);dt=np.array([[lon,lat,1] for _,_,_,lon,lat in dc])@native;dm=np.linalg.lstsq(dd,dt,rcond=None)[0]
    border=[(1780,2450),(1810,2440),(1850,2438),(1890,2445),(1920,2433),(1955,2417),(1980,2419),(2010,2430),(2027,2443),(2039,2462),(2062,2440),(2100,2427),(2135,2424),(2170,2390),(2195,2355),(2220,2330),(2250,2310),(2280,2305)]
    dpoly=np.c_[np.array(border+[(2300,2650),(1750,2650)]),np.ones(len(border)+2)]@dm
    dy,dx=np.mgrid[750:772,4535:4565];dp=np.c_[(dx+.5).ravel(),(dy+.5).ravel()]
    dobrzyn=np.zeros(a.shape,dtype=bool);dobrzyn[750:772,4535:4565]=inside(dp,dpoly).reshape(dx.shape)&(a[750:772,4535:4565]==0x374AC3)
    # One adjacent boundary cell keeps the known Polish city Rypin on the
    # Polish side despite the coarse sheet/native fit. Explicit B decision,
    # not a native-model optimization or a claim to its municipal cadastre.
    rx,ry=4540,765
    assert not dobrzyn[ry,rx] and a[ry,rx]==0x374AC3 and any(dobrzyn[y,x] for x,y in [(rx-1,ry),(rx+1,ry),(rx,ry-1),(rx,ry+1)])
    dobrzyn[ry,rx]=True
    golub=np.linalg.norm(np.array([1848,2402,1])@dm-np.array([19.053,53.11,1])@native)
    dump('DOBRZYN_TRACING.json',dict(source='Guessefeld 1775, existing MAP2M image; contemporary political border',controls=dc,source_to_native_matrix=dm.tolist(),fit_residuals_px=np.linalg.norm(dd@dm-dt,axis=1).tolist(),golub_check=dict(source=[1848,2402],geographic=[19.053,53.11],residual_px=float(golub)),border_source=border,native_polygon=dpoly.tolist(),classification='B_POLITICAL_GENERALISATION',municipal_chronology='https://rypin.eu/strona-49-historia.html',political_B_boundary_cell=[rx,ry],not_full_dobrzyn_cadastre=True))
    owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']};assignments=[];new=[];parents=[];nextval=0xEEC200
    for parent,selected,tag in [('x41A021',thorn,'PLC'),('xC02121',netze,'PRU'),('xFCC7B7',netze,'PRU'),('x374AC3',dobrzyn,'PLC')]:
        value=int(parent[1:],16);allcells=a==value;moved=allcells&selected;retained=allcells&~selected
        if not moved.any():continue
        sid,src=owners[parent];parents.append(parent)
        assert retained.any(),'Do not annex whole ambiguous parent in this scoped pass'
        assert not (a==nextval).any();child='x'+format(nextval,'06X');after[moved]=nextval;nextval+=1;new.append(dict(rgb=child,parent_rgb=parent))
        for rgb,owner,cells in [(parent,src,retained),(child,tag,moved)]:
            ys,xs=np.where(cells);assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=src,owner=owner,pixels=len(xs),cells=[[int(x),int(y)] for y,x in zip(ys,xs)],components_4=sorted([len(c) for c in components(cells)],reverse=True)))
    rgb=np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=-1).astype(np.uint8);Image.fromarray(rgb).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,parents=parents,assignments=assignments,new_provinces=new,changed_pixels=int((after!=a).sum()),candidate_sha256=sha(OUT/'provinces_candidate.png'),hub_rebindings=[],thorn_core_cells=thorn_cells))
    residual=np.linalg.norm(design@matrix-target,axis=1);checkres=np.linalg.norm(np.array([[x,y,1] for _,x,y,_,_ in checks])@matrix-np.array([[lon,lat,1] for _,_,_,lon,lat in checks])@native,axis=1)
    dump('TRACING.json',dict(source='Guessefeld 1780 revised, Bern e-rara-127551, Netze inset',controls=controls,checks=checks,source_to_native_matrix=matrix.tolist(),fit_residuals_px=residual.tolist(),check_residuals_px=checkres.tolist(),source_outline=outline,native_outline=polygon.tolist(),native_profile='MAP2M/R5/TRANSFORMATIONS.json selected_native, unchanged',imperial_owners=[],core_limit=dict(max_native_y=780,reason='Exclude uncertain southern fringe and protect Trzemeszno/Gniezno; not the whole 1780 border'),thorn=dict(classification='B_URBAN_CORE_NOT_RURAL_TERRITORY',cells=thorn_cells,source='1775 Guessefeld reserved Thorn loop; Pfau45 fortified city on opposite bank to the old farm; 1780 inset reserved Thorn loop',native_city_diagnostic=[4521.48,767.34],not_user_certified=True)))
    image=Image.open(OUT/'EVIDENCE/GUESSEFELD_1780.jpg').convert('RGB');d=ImageDraw.Draw(image);d.line(outline+[outline[0]],fill='blue',width=3)
    for name,x,y,_,_ in controls:d.ellipse((x-4,y-4,x+4,y+4),fill='red');d.text((x+5,y+5),name,fill='blue',stroke_width=1,stroke_fill='white')
    image.crop((2350,170,3210,800)).resize((1290,945)).save(OUT/'SOURCE_TRACE_REVIEW.jpg')
    print('Netze cells',int(netze.sum()),'Thorn',len(thorn_cells),'Dobrzyn',int(dobrzyn.sum()));print('Fit',residual,'Checks',checkres);print('Dobrzyn residuals',np.linalg.norm(dd@dm-dt,axis=1));print([(r['rgb'],r['owner'],r['pixels'],r['components_4']) for r in assignments]);diagnostics(True);review_dobrzyn()

def review_dobrzyn():
    b=load('BASELINE.json');g=load('GEOMETRY.json');a=packed(OUT/'provinces_candidate.png');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners.update({r['rgb']:r['owner'] for r in g['assignments']})
    local=a[751:777,4528:4565];arr=np.full((*local.shape,3),220,dtype=np.uint8)
    for v in np.unique(local):arr[local==v]={'PRU':(118,155,194),'PLC':(223,162,177)}.get(owners.get('x'+format(int(v),'06X')),(220,220,220))
    im=Image.fromarray(arr).resize((1295,910),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for name,x,y in [('Rypin',4540.05,765.61),('Brodnica',4539.89,759.6),('Gorzno',4545.4,761.55),('wood hub',4540.2085,762.7424)]:
        xx,yy=(x-4528)*35,(y-751)*35;d.ellipse((xx-4,yy-4,xx+4,yy+4),fill='red');d.text((xx+4,yy),name,font=f,fill='black',stroke_width=1,stroke_fill='white')
    im.save(OUT/'DOBRZYN_AFTER.png')
    s=load('DOBRZYN_TRACING.json');im=Image.open(ROOT/'docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg');d=ImageDraw.Draw(im);d.line([tuple(r) for r in s['border_source']],fill='blue',width=3)
    for name,x,y,_,_ in s['controls']:d.ellipse((x-4,y-4,x+4,y+4),fill='red');d.text((x+5,y+5),name,fill='blue',stroke_width=1,stroke_fill='white')
    im.crop((1480,2040,2310,2540)).resize((1245,750)).save(OUT/'DOBRZYN_SOURCE_TRACE.jpg')

def prepare():
    import map2l_mainz as core
    from map2l_registry import active_registry_path
    b=load('BASELINE.json');g=load('GEOMETRY.json');assert runtime_hashes()==b['runtime']
    assert not any(r['state'] in REGIONS for r in b['registry']),'Do not silently remove imperial rights'
    new_thorn=next(r['rgb'] for r in g['assignments'] if r['parent_rgb']=='x41A021' and r['owner']=='PLC')
    rel='gfx/map/map_object_data/generated_map_object_locators_farm.txt';oldfarm=(ROOT/rel).read_bytes().decode('utf-8')
    # Read the actual mod file, not an old vanilla baseline. Only ID 158's
    # position changes, by about five native cells; rotation/scale unchanged.
    pattern=r'(id\s*=\s*158\s+position\s*=\s*\{\s*)([^}]+)(\})';matches=list(re.finditer(pattern,oldfarm));assert len(matches)==1
    position=[float(x) for x in matches[0].group(2).split()];assert position==[4519.314941,0.,2843.895264]
    newfarm=re.sub(pattern,lambda m:m.group(1)+'4521.500000 0.000000 2848.500000 '+m.group(3),oldfarm,count=1)
    relocation=dict(state='STATE_WEST_PRUSSIA',kind='farm',id=158,file=rel,before_position=position,after_position=[4521.5,0.,2848.5],before_bitmap_point=[4519.314941,772.104736],after_bitmap_point=[4521.5,767.5],reason='Thorn fortified city is on the north bank in Pfau; frozen R5 geographic diagnostic and native river give a coarse B placement, not an exact city locator',classification='B_POLITICAL_GENERALISATION')
    g['locator_relocations']=[relocation]
    g['hub_rebindings']=[dict(state='STATE_WEST_PRUSSIA',field='farm',before='x41A021',bitmap_before='x41A021',after=new_thorn,point=[4521.5,767.5],pixel=[4521,767],locator_moved=True)]
    dump('GEOMETRY.json',g);dump('LOCATOR_RELOCATION.json',relocation)
    core.OUT=OUT;core.REGIONS=REGIONS;core.REGION_FILE='map_data/state_regions/02_east_europe.txt'
    civil={'building_logging_camp','building_livestock_ranch','building_rye_farm','building_coal_mine','building_iron_mine','building_lead_mine','building_paper_mill','building_railway'}
    core.BUILDING_ALLOCATION_WEIGHTS={}
    for rel,text in b['originals'].items():
        if '/buildings/' not in rel:continue
        for sid,src in [('STATE_WEST_PRUSSIA','PRU'),('STATE_POSEN','PLC')]:
            try:n=core.region(text,sid,src)
            except StopIteration:continue
            for build in n.children('create_building'):
                kind=cw.scalar(build.one('building'))
                if kind not in civil:core.BUILDING_ALLOCATION_WEIGHTS[rel,sid,src,kind]={src:1,('PLC' if src=='PRU' else 'PRU'):0}
    before={};expected={}
    def extra(files,migration):
        migration.update(country_additions={},external_to_hre=True,locator_relocations=[relocation])
        assert migration['previous']==migration['updated']==[]
        assert migration['extent_added_cells']==migration['extent_removed_cells']==[]
        rel='tools/map2l_registry.py';raw=(ROOT/rel).read_bytes().decode('utf-8');anchor='    return result\n\ndef provincial_membership_overrides'
        if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
        assert raw.count(anchor)==1
        guard='''    polish_frontier=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIA_POLAND_2026_11_05'
    if (polish_frontier/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((polish_frontier/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((polish_frontier/'GEOMETRY.json').read_text(encoding='utf8'))
        assert north_saxony in result
        assert m['replaced_regions']==['STATE_POSEN','STATE_WEST_PRUSSIA']
        assert m['previous']==m['updated']==m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['external_to_hre'] is True
        assert m['new_provinces']==g['new_provinces'] and len(g['new_provinces'])==4
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert set(g['parents'])=={'x41A021','xC02121','xFCC7B7','x374AC3'}
        assert sum(r['pixels'] for r in g['assignments'] if r['owner']!=r['previous_owner'])==285
        assert all(r['state'] in m['replaced_regions'] and {r['owner'],r['previous_owner']}<={'PRU','PLC'} for r in g['assignments'])
        assert len(m['locator_relocations'])==1 and m['locator_relocations']==g['locator_relocations']
        loc=m['locator_relocations'][0]
        assert (loc['state'],loc['kind'],loc['id'])==('STATE_WEST_PRUSSIA','farm',158)
        assert loc['before_position']==[4519.314941,0.,2843.895264] and loc['after_position']==[4521.5,0.,2848.5]
        result.append(polish_frontier)
'''
        files[rel]=raw.replace(anchor,guard+anchor)
        files['gfx/map/map_object_data/generated_map_object_locators_farm.txt']=newfarm
        files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    core.PREPARE_EXTRA_FILES=extra
    def emit(files,name):
        for rel,text in files.items():
            if rel.startswith(OUT.relative_to(ROOT).as_posix()+'/'):(ROOT/rel).write_text(text,encoding='utf-8');continue
            old=(ROOT/rel).read_bytes().decode('utf-8');before[rel]=old
            if old.startswith('\ufeff') and not text.startswith('\ufeff'):text='\ufeff'+text
            if '\r\n' in old and old.count('\n')==old.count('\r\n'):text=text.replace('\r\n','\n').replace('\n','\r\n')
            if text!=old:expected[rel]=text
        return sorted(expected)
    core.emit=emit;core.prepare()
    rel='map_data/province_terrains.txt';old=(ROOT/rel).read_bytes().decode('utf-8');text=(OUT/'province_terrains_candidate.txt').read_text(encoding='utf-8')
    # Do not propagate inherited tundra into a Lower Vistula urban plain.
    text,n=re.subn(r'(?m)^'+new_thorn+r'\s*=\s*"tundra"',new_thorn+'="plains"',text);assert n==1
    if old.startswith('\ufeff'):text='\ufeff'+text.lstrip('\ufeff')
    if '\r\n' in old and old.count('\n')==old.count('\r\n'):text=text.replace('\r\n','\n').replace('\n','\r\n')
    before[rel]=old;expected[rel]=text
    for rel,text in list(expected.items()):
        a=before[rel].splitlines(True);c=text.splitlines(True);parts=[]
        for tag,i,j,k,l in difflib.SequenceMatcher(None,a,c,autojunk=False).get_opcodes():
            lines=c[k:l]
            if tag!='equal':lines=[line if line.strip() else ('\r\n' if line.endswith('\r\n') else '\n') for line in lines]
            parts.extend(lines)
        expected[rel]=''.join(parts)
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',expected)
    lines=[]
    for rel,text in expected.items():lines.extend(difflib.unified_diff(before[rel].splitlines(True),text.splitlines(True),fromfile=rel,tofile=rel,n=3))
    (OUT/'REVIEW.diff').write_text(''.join(lines),encoding='utf-8')
    plan=load('PLAN.json');plan.update(files=sorted(expected),imperial_registry_unchanged=True,source_date_caveat='1780 inset corroborates core towns controlled by Prussia before 1776; not a full 1776 boundary certificate',runtime_installed=False);dump('PLAN.json',plan)
    print('Prepared',len(expected),'text files; imperial titles unchanged')

def install():
    import serg_prussia_v1 as core
    core.OUT=OUT;core.install()

def verify():
    import map2l_registry as registry
    import serg_closure_roadmap as roadmap
    import map2m_r9 as old
    b=load('BASELINE.json');g=load('GEOMETRY.json');i=load('INSTALLATION.json');inv=qa.inventory();dump('INVENTORY_AFTER.json',inv)
    before=packed(OUT/'provinces_before.png');after=packed(ROOT/'map_data/provinces.png');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
    ck('Installed bitmap exact',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
    moved=[r for r in g['assignments'] if r['owner']!=r['previous_owner']]
    ck('Exact 285 changed cells',len(g['new_provinces'])==4 and sum(r['pixels'] for r in moved)==285 and int((before!=after).sum())==285)
    ck('Netze PLC to PRU 222',sum(r['pixels'] for r in moved if r['owner']=='PRU')==222)
    ck('Thorn and Dobrzyn PRU to PLC 4 plus 59',[(r['parent_rgb'],r['pixels']) for r in moved if r['owner']=='PLC']==[('x41A021',4),('x374AC3',59)])
    wanted=qa.counter(b['inventory']['owners']).copy()
    for r in b['inventory']['owners']:
        if r['key'][0] in g['parents']:del wanted[tuple(r['key'])]
    for r in g['assignments']:wanted[r['rgb'],r['state'],r['owner']]+=1
    ck('Worldwide ownership delta exact',qa.counter(inv['owners'])==wanted)
    ck('Duplicate debt unchanged',inv['duplicates']==b['inventory']['duplicates'])
    ck('No new orphan or wrong-state reference',inv['errors']==b['inventory']['errors'])
    ck('Four new single-state RGBs',all(inv['geometry'][r['rgb']]==inv['geometry'][r['parent_rgb']] for r in g['new_provinces']))
    allowed=np.isin(before,[int(x[1:],16) for x in g['parents']]);ck('All pixels outside four parents exact',np.array_equal(after[~allowed],before[~allowed]))
    for r in g['assignments']:
        ys,xs=np.where(after==int(r['rgb'][1:],16));ck('Exact cell set '+r['rgb'],set(zip(xs.tolist(),ys.tolist()))=={tuple(c) for c in r['cells']} and len(xs)==r['pixels'])
    ck('All new subdivisions connected',all(len(r['components_4'])==1 for r in moved))
    oldcore=before==0xEDB010;owners={r['key'][0]:r['key'][2] for r in inv['owners']}
    ck('Accepted Bromberg 85 cells exact',int(oldcore.sum())==85 and np.all(after[oldcore]==0xEDB010) and owners['xEDB010']=='PRU')
    ck('Dantzig 185 PLC cells exact',int((before==0x80A0A0).sum())==185 and np.all(after[before==0x80A0A0]==0x80A0A0) and owners['x80A0A0']=='PLC')
    ck('Native Poznan PLC province exact',np.all(after[before==0x999CEE]==0x999CEE) and owners['x999CEE']=='PLC')
    ck('Twenty-two coarse town diagnostics consistent',len(load('TOWNS_AFTER.json'))==22 and all(r['owner']==r['expected'] for r in load('TOWNS_AFTER.json')),'Not independently certified city positions')
    for folder in PRIOR:
        pg=json.loads((folder/'GEOMETRY.json').read_text());cells=[c for r in pg['assignments'] if r['owner']=='SAX' for c in r['cells']]
        ck('Protected Saxon core '+folder.name,all(after[y,x]==before[y,x] and owners['x'+format(int(after[y,x]),'06X')]=='SAX' for x,y in cells),len(cells))
    ck('Previous Saxon delivery evidence exact',all(sha(ROOT/rel)==h for rel,h in b['previous_delivery'].items()))
    ck('Archived MAP2M proofs and results exact',all(sha(ROOT/rel)==h for rel,h in b['archived_polish_proofs'].items()))
    ck('Previous delivery tools exact',all(sha(ROOT/n)==h for n,h in b['previous_tools'].items() if n!='tools/map2l_registry.py'))
    ck('Global written and resolved population profiles exact',inv['pops']==b['inventory']['pops'] and inv['resolved_demographics']==b['inventory']['resolved_demographics'])
    ck('Global total population exact',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in b['inventory']['pops']))
    regional=qa.counter(inv['regional_pop']);prior=qa.counter(b['inventory']['regional_pop']);p=load('PLAN.json')
    ck('Population outside two states exact',{k:v for k,v in regional.items() if k[0] not in REGIONS}=={k:v for k,v in prior.items() if k[0] not in REGIONS})
    for sid,src,dst in [('STATE_POSEN','PLC','PRU'),('STATE_WEST_PRUSSIA','PRU','PLC')]:
        delta=sum(r['after'].get(dst,0) for r in p['allocations'] if r['kind']=='population' and r['state']==sid)
        ck('Population addition '+sid,sum(v for k,v in regional.items() if k[:2]==(sid,dst))==sum(v for k,v in prior.items() if k[:2]==(sid,dst))+delta,delta)
    ck('All buildings PMs levels holders exact',inv['buildings']==b['inventory']['buildings'] and inv['building_levels_written']==b['inventory']['building_levels_written'])
    ck('All units and recruitment exact',inv['units']==b['inventory']['units'])
    ck('All country definitions exact',inv['countries']==b['inventory']['countries'])
    ledger=json.loads(registry.active_registry_path().read_text());ck('592 imperial titles unchanged',ledger==b['registry'] and len(ledger)==592)
    texts=load('TEXT_BEFORE.json');regrel=registry.active_registry_path().relative_to(ROOT).as_posix();ck('Imperial registry bytes exact',(ROOT/regrel).read_bytes().decode('utf-8')==texts[regrel])
    ck('Imperial physical extent unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in ledger]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    migration=load('REGISTRY_MIGRATION.json');ck('New geometry chain external to HRE',registry.approved_lot_dirs()[-1]==OUT and migration['previous']==migration['updated']==[] and migration['external_to_hre'])
    rel='gfx/map/map_object_data/generated_map_object_locators_farm.txt';raw=(ROOT/rel).read_bytes().decode('utf-8');original=texts[rel]
    expected=re.sub(r'(id\s*=\s*158\s+position\s*=\s*\{\s*)([^}]+)(\})',lambda m:m.group(1)+'4521.500000 0.000000 2848.500000 '+m.group(3),original,count=1)
    ck('Only farm locator 158 position changed',raw==expected)
    locs=old.locators(after);farm=next(r for r in locs if r['Kind']=='farm' and r['ID']==158)
    ck('Thorn farm reference contains relocated locator',farm['RGB']=='xEEC200' and farm['X']==4521.5 and farm['Y']==767.5)
    ck('Bromberg farm unchanged',next(r for r in locs if r['Kind']=='farm' and r['ID']==160)['RGB']=='xEDB010')
    ck('Brodnica wood hub remains PRU',next(r for r in locs if r['Kind']=='wood' and r['ID']==158)['RGB']=='x374AC3' and owners['x374AC3']=='PRU')
    from map2b_patch import state
    definitions=cw.parse((ROOT/'map_data/state_regions/02_east_europe.txt').read_text(encoding='utf-8-sig'));west=next(n for n in definitions if n.key=='STATE_WEST_PRUSSIA')
    ck('State farm reference now Thorn PLC',cw.scalar(west.one('farm'))=='xEEC200')
    river=ROOT/'map_data/rivers.png';river=river if river.exists() else Path('C:/Games/Victoria 3/game/map_data/rivers.png');r=np.array(Image.open(river))
    ys1=np.where((r[764:771,4519]>=3)&(r[764:771,4519]<=15))[0]+764;ys2=np.where((r[764:771,4521]>=3)&(r[764:771,4521]<=15))[0]+764
    ck('Old farm south and relocated town north of local native Vistula',len(ys1)>0 and len(ys2)>0 and 772.104736>max(ys1) and 767.5<min(ys2) and r[767,4521]==255,dict(old_crossings=ys1.tolist(),new_crossings=ys2.tolist()))
    terrain=(ROOT/'map_data/province_terrains.txt').read_text();ck('New Thorn urban terrain plains',bool(re.search(r'(?m)^xEEC200\s*=\s*"plains"',terrain)))
    ck('Thorn rural parent retained 149 PRU cells',int((after==0x41A021).sum())==149 and owners['x41A021']=='PRU')
    for row in i['changes']:ck('Installed hash '+row['file'],sha(ROOT/row['file'])==row['after'])
    changed={r['file'] for r in i['changes']};now=runtime_hashes();drift=[n for n in set(now)|set(b['runtime']) if now.get(n)!=b['runtime'].get(n) and n not in changed]
    ck('All other runtime files and concurrent work exact',not drift,drift)
    ck('No imperial script or localisation modified',not any('/scripted_' in n or '/power_bloc_' in n or n.startswith('localization/') for n in changed))
    for rel in changed:
        if rel.endswith('.txt'):cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    ck('Changed game scripts parse',True)
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],capture_output=True,text=True);ck('Git '+name+' exact',r.returncode==0 and r.stdout.strip()==b['git'][name])
    ck('Git index exact',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    canonical=roadmap.check();dump('CANONICAL_AFTER.json',canonical);ck('Canonical validator PASS',canonical['status']=='PASS',canonical['errors'])
    ck('No HRE progress credit 93/235',canonical['progress']['earned_weight']==93 and canonical['progress']['total_weight']==235 and canonical['progress']['percent']=='39.57')
    current=roadmap.load_json(CANON/'ROADMAP_STATE.json');previous=load('ROADMAP_STATE_BEFORE.json');ck('All 81 SERG task records exact',current['tasks']==previous['tasks']);ck('Old event history prefix exact',current['events'][:len(previous['events'])]==previous['events'])
    failed=[r for r in checks if not r['passed']];dump('VALIDATION.json',dict(status='FAIL' if failed else 'PASS',passed=len(checks)-len(failed),total=len(checks),failed=failed,checks=checks,engine_test=False,human_attestation=None,external_to_hre=True))
    print('Static',len(checks)-len(failed),'/',len(checks));print(json.dumps(failed,ensure_ascii=False));assert not failed

def legacy(phase):
    import unittest,io,time
    stream=io.StringIO();start=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromName('test_map2m_r9');result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    dump('LEGACY_'+phase+'.json',dict(total=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),failures=[dict(test=str(test),traceback=body) for test,body in result.failures],errors=[dict(test=str(test),traceback=body) for test,body in result.errors],skipped=len(result.skipped),elapsed_seconds=time.monotonic()-start,engine_test=False))
    (OUT/('LEGACY_'+phase+'_RAW.txt')).write_text(stream.getvalue(),encoding='utf-8');print('Legacy',phase,result.testsRun,'tests',len(result.failures),'failures',len(result.errors),'errors')
def legacy_before():legacy('BEFORE')
def legacy_after():legacy('AFTER')

def tests():
    import unittest,io,time
    modules=['test_serg_closure_roadmap','test_map2l_registry','test_map2m_r2'];stream=io.StringIO();start=time.monotonic();suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(m) for m in modules);result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    dump('TEST_RESULTS.json',dict(total=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),elapsed_seconds=time.monotonic()-start,modules=modules,engine_test=False,bitmap_sha256=sha(ROOT/'map_data/provinces.png')))
    (OUT/'TEST_RESULTS_RAW.txt').write_text(stream.getvalue(),encoding='utf-8');print(load('TEST_RESULTS.json'));assert result.wasSuccessful(),stream.getvalue()

def tracker():
    import serg_closure_roadmap as roadmap
    assert load('VALIDATION.json')['status']=='PASS'
    raw=(CANON/'ROADMAP_STATE.json').read_bytes();s=json.loads(raw);previous=load('ROADMAP_STATE_BEFORE.json');assert s==previous,'Reconcile any concurrent tracker changes'
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    delivery=dict(id='PRUSSIA-POLAND-2026-11-05',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',external_to_hre=True,management_points=0,report=prefix+'REPORT.md',sources=prefix+'SOURCES.md',static_tests=prefix+'VALIDATION.json',protocol=prefix+'PLAYER_TEST_PROTOCOL.md',human_attestation=None,
        sub_lots=[dict(id='PP-NETZE-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',direction='PLC_TO_PRU',cells=222,attestation=None),dict(id='PP-THORN-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',direction='PRU_TO_PLC',cells=4,attestation=None),dict(id='PP-DOBRZYN-FRINGE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',direction='PRU_TO_PLC',cells=59,attestation=None)],
        residual_uncertainty='Catégorie B ; contour complet des quatre districts de la Netze et possessions rurales de Thorn non certifiés. Encarts 1780 confrontés aux contrôles antérieurs à 1776, sans rétroprojection de 1793.')
    s.setdefault('external_prussian_deliveries',[]).append(delivery)
    s['release_focus'].update(current_pass='PRUSSIA_POLISH_FRONTIER',current_delivery=prefix+'REPORT.md',next_requested_pass=None,next_pass_started=False,
        continuation_authority='Instruction explicite utilisateur : Passe aux frontières polonaises prussiennes.',polish_frontier_delivery=delivery['id'])
    s['runtime_validation_hold'].update(protocol=prefix+'PLAYER_TEST_PROTOCOL.md',reason='Test joueur groupé des trois sous-lots polono-prussiens et des installations saxonnes encore en attente.',next_implementation_candidate=None,
        scope_note='Les trois nouveaux sous-lots sont extérieurs au SERG ; aucun point supplémentaire, aucune modification des 81 fiches. Anciennes attestations et attentes saxonnes conservées. Aucun nouveau chantier automatique.')
    s['mission_status']='PRUSSIA_POLAND_CORE_AND_DOBRZYN_INSTALLED_PENDING_RUNTIME'
    before=roadmap.progress(previous);after=roadmap.progress(s);eid='SERG-RM-'+format(max(int(e['id'].rsplit('-',1)[1]) for e in s['events'])+1,'04d')
    s['events'].append(dict(id=eid,date='2026-11-05',kind='PRUSSIA_POLAND_FRONTIER_INSTALLED_EXTERNAL_TO_HRE',scope_version=s['scope_version'],source=prefix+'REPORT.md',changes=[],before_weight=before['earned_weight'],after_weight=after['earned_weight'],total_weight=after['total_weight'],before_percent=before['percent'],after_percent=after['percent'],
        note='285 cellules modifiées : 222 PLC→PRU dans la Netze, 4 PRU→PLC à Thorn et 59 PRU→PLC en Dobrzyń. Seul le repère farm158 est déplacé vers le noyau polonais de rive nord. Catégorie B, hors SERG ; 592 titres et toutes les 81 fiches inchangés, aucun reçu humain ni point. Test groupé proposé ; aucune autre passe commencée.',
        evidence=[prefix+'INSTALLATION.json',prefix+'VALIDATION.json',prefix+'PLAYER_TEST_PROTOCOL.md']))
    names=['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md'];texts={n:(CANON/n).read_bytes().decode('utf-8') for n in names};dump('TRACKER_BEFORE.json',texts)
    header='''## Livraison courante — frontière polono-prussienne, 5 novembre 2026

**285 cellules corrigées, catégorie B** : 222 PLC→PRU dans le noyau Netze (Bromberg/Żnin/Mogilno/Inowrocław), 4 PRU→PLC pour Thorn et 59 PRU→PLC dans la frange de Dobrzyń/Rypin. Le seul repère rural Toruń est raccordé à son noyau polonais de rive nord. Dantzig, Poznań, Gniezno et Trzemeszno restent polonaises ; Brodnica et Górzno restent prussiennes. [Rapport](PRUSSIA_POLAND_2026_11_05/REPORT.md), [sources et limites](PRUSSIA_POLAND_2026_11_05/SOURCES.md), [protocole joueur groupé](PRUSSIA_POLAND_2026_11_05/PLAYER_TEST_PROTOCOL.md).

Trois sous-lots `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`, **aucune réception humaine**. Cette livraison est **extérieure au Saint-Empire** : les 592 titres impériaux, les 81 fiches et les 235 points sont inchangés. **93/235 = 39,57 %, 32/81**. Les corrections saxonnes de 811 + 606 cellules et toutes leurs preuves sont préservées ; leurs attentes de validation demeurent.

**Prochaine action : test joueur groupé de cette livraison et des sous-lots saxons en attente. Aucun autre territoire commencé.** Le contour intégral des quatre districts de la Netze, les possessions rurales de Thorn et les franges non datées ne sont pas clôturés. Les anciens blocages SERG restent tels quels ; aucun micro-État ou lot bavarois relancé. Les encadrés précédents ci-dessous sont des archives de priorité.

'''
    updated={}
    for name in names[:3]:
        text=texts[name];idx=text.index('\n');new=text[:idx+1]+'\n'+header+text[idx+1:]
        if name=='NEXT_ACTION.md':new=new.replace(new.splitlines()[0],'# Prochaine action — test joueur groupé des frontières prussiennes',1)
        updated[name]=new
    updated['PROGRESS_HISTORY.md']=texts['PROGRESS_HISTORY.md']+'\n\n## '+eid+' — 5 novembre 2026 — Frontière polono-prussienne, livraison hors SERG\n\n285 cellules installées : PP-NETZE-CORE, 222 PLC→PRU ; PP-THORN-CORE, 4 PRU→PLC ; PP-DOBRZYN-FRINGE, 59 PRU→PLC. Farm158/Toruń déplacé vers la rive nord, autres repères et tous les bâtiments/PM/unités préservés. Approximation B ; limites complètes de la Netze et possessions rurales de Thorn non certifiées. Les preuves MAP2M, les 811 + 606 cellules saxonnes et les 81 tâches sont inchangées. Livraison extérieure au SERG, 592 titres impériaux inchangés ; aucun reçu humain ou point : 93/235, 39,57 %, 32/81. Prochaine action limitée au test joueur groupé, aucune autre passe commencée. [Rapport](PRUSSIA_POLAND_2026_11_05/REPORT.md).\n'
    assert (CANON/'ROADMAP_STATE.json').read_bytes()==raw
    (CANON/'ROADMAP_STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,text in updated.items():
        assert (CANON/name).read_bytes().decode('utf-8')==texts[name]
        (CANON/name).write_bytes(text.encode('utf-8'))
    roadmap.write_json(CANON/'PROGRESS_SNAPSHOT.json',roadmap.progress(s));dump('TRACKER_CHANGE.json',dict(event=eid,before=before,after=roadmap.progress(s),changed_task_ids=[],human_receipts_added=0,external_delivery=delivery))
    result=roadmap.check();dump('CANONICAL_AFTER.json',result);assert result['status']=='PASS',result['errors'];print(eid,result['progress']['percent'])

def report():
    b=load('BASELINE.json');g=load('GEOMETRY.json');p=load('PLAN.json');v=load('VALIDATION.json');i=load('INSTALLATION.json');t=load('TEST_RESULTS.json') if (OUT/'TEST_RESULTS.json').exists() else None
    movements={sid:sum(r['after'].get(dst,0) for r in p['allocations'] if r['kind']=='population' and r['state']==sid) for sid,dst in [('STATE_POSEN','PRU'),('STATE_WEST_PRUSSIA','PLC')]}
    rows=['| Parent | Transfert | Cellules transférées | Résidu conservé |','| --- | --- | ---: | ---: |']
    for parent in g['parents']:
        a=[r for r in g['assignments'] if r['parent_rgb']==parent];changed=next(r for r in a if r['owner']!=r['previous_owner']);retained=next(r for r in a if r['owner']==r['previous_owner']);rows.append('| '+parent+' | '+changed['previous_owner']+' → '+changed['owner']+' | '+str(changed['pixels'])+' | '+str(retained['pixels'])+' |')
    testline=f"{t['total']} tests ciblés exécutés : **{t['passed']} réussites, {t['skipped']} exclusion, {t['failures']} échec et {t['errors']} erreur**." if t else 'Suite ciblée à exécuter après actualisation du suivi ; aucun chiffre antérieur présenté comme nouveau.'
    text=f'''# SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %

**Frontière polono-prussienne : trois sous-lots installés le 5 novembre 2026, en attente du test joueur.** Mission centrée sur la Prusse ; aucune Bavière, aucun micro-État ou autre chantier commencé.

## Installation concrète

**PP-NETZE-CORE : 222 cellules PLC → PRU**, autour de Bromberg/Bydgoszcz, Żnin, Mogilno et Inowrocław. Les 85 cellules reçues antérieurement restent exactes ; Trzemeszno, Gniezno et Poznań restent polonaises. **PP-THORN-CORE : 4 cellules PRU → PLC**, noyau urbain sur la rive nord de la Vistule ; 149 cellules rurales restent PRU. **PP-DOBRZYN-FRINGE : 59 cellules PRU → PLC**, secteur de Rypin, tandis que Brodnica/Górzno et le repère forestier restent prussiens.

{chr(10).join(rows)}

**285 cellules recolorées**, quatre RGB nouveaux `xEEC200` à `xEEC203`, mêmes deux régions économiques et mêmes pays. Les nouveaux noyaux sont connexes ; les deux fragments du résidu RGB de Dobrzyń restent reliés par les provinces prussiennes voisines. Le manifeste [INSTALLATION.json](INSTALLATION.json) décrit les **{len(i['changes'])} fichiers installés** et leurs empreintes exactes.

![Netze et Thorn après installation](FRONTIER_AFTER.png)

![Frange de Dobrzyń après installation](DOBRZYN_AFTER.png)

Le seul repère **farm158/Toruń** est déplacé d'environ cinq cellules, de la rive sud vers le noyau PLC de rive nord. La référence provinciale suit réellement son nouveau point ; aucun autre repère, rotation ou échelle n'est modifié. Le nouveau terrain de Thorn est `plains` ; l'ancien `tundra` du parent rural n'est pas corrigé ou recopié sur le noyau urbain. Les noms de ville préexistants sont conservés ; aucune nouvelle ville nommée n'est créée à Inowrocław ou Rypin.

## Sources et portée historique

La livraison est une **généralisation politique B**, pas une frontière cadastrale certifiée. Les scans antérieurs sont réutilisés, les anciens recalages rejetés ne sont pas relancés. L'encart **révisé de 1780** est confronté aux chronologies institutionnelles : Żnin et Mogilno sous contrôle prussien dès 1774, Trzemeszno demeurant polonaise jusqu'en 1793. L'édition de 1780, postérieure à la cible, n'est pas appliquée intégralement à janvier 1776. Le liseré méridional de 1775 dont la date d'effet était contestée reste exclu.

La frontière orientale de Dobrzyń est lue sur la feuille **contemporaine de 1775**, avec Rypin polonaise jusqu'en 1793. Thorn est distinguée de ses campagnes ; les cartes politiques et la configuration riveraine de Pfau justifient le noyau B, sans inventer une approbation des anciennes variantes U1/U2 ou une validation du nouveau choix. [Sources, lectures, points et limites](SOURCES.md).

**Le contour complet des quatre districts de la Netze, les possessions rurales de Thorn et les rectifications non datées restent ouverts.** Les diagnostics de villes sont grossiers, pas des locators homologués. Les résidus des nouvelles lectures de feuilles ne démontrent pas une précision uniforme des frontières. L'effet sur le rendu des repères, les accès au marché et le fonctionnement économique doit être observé en jeu ; aucune panne moteur n'a été constatée par l'agent, qui n'a pas lancé le jeu.

## Conservation

Les **811 + 606 cellules saxonnes précédentes**, leurs preuves et leurs outils sont préservés. Leurs attentes de réception demeurent. Anhalt, Cottbus/Peitz, les réparations MAP2A et les autres noyaux validés sont hors des quatre parents et restent exacts. Tous les rapports/reçus/résultats bruts MAP2M sont conservés sans réécriture.

Redistribution technique des populations existantes : **{movements['STATE_POSEN']}** habitants PLC → PRU dans Posen, **{movements['STATE_WEST_PRUSSIA']}** PRU → PLC dans Prusse occidentale. Ces nombres portent sur les portions État/propriétaire ; aucun n'est un recensement de Thorn ou de Rypin. Les profils culturels/religieux explicites et résolus et le total mondial écrit, **{sum(r['count'] for r in b['inventory']['pops'])}**, restent identiques.

**Tous les bâtiments, PM, niveaux, détenteurs économiques, armements, formations et recrutements sont inchangés.** Aucun nouveau pays, technologie ou recette. Les fortifications, le Corps du génie et les travaux économiques/concurrents restent protégés par empreintes et comparaison d'inventaire.

Ces territoires sont **extérieurs au Saint-Empire** : les **592 titres impériaux**, leur étendue, les membres et les électeurs restent inchangés ; aucun script impérial ou texte de localisation n'est régénéré. Seul un manifeste géométrique extérieur est ajouté à la chaîne technique. Les **81 fiches SERG restent intégralement identiques** ; la livraison est suivie séparément sans point ni changement du dénominateur.

## Contrôles réellement exécutés

- **{v['passed']}/{v['total']} contrôles différentiels PASS** sur le workspace installé : [VALIDATION.json](VALIDATION.json).
- {testline} [Résultats](TEST_RESULTS.json), [sortie brute](TEST_RESULTS_RAW.txt).
- La suite photographique R9 a aussi été exécutée avant et après : **8 tests, 2 échecs avant, 3 après, aucune erreur**. Les deux premiers portent sur un raster limité aux seules deux cellules de R9 et l'identité de tous les anciens repères, déjà dépassés avant cette mission. Le nouvel écart est l'assertion « Thorn inchangée, 153 cellules », volontairement remplacée par le correctif autorisé (149 + 4) et son contrôle différentiel exact. Aucun test ancien, résultat brut ou baseline n'est modifié pour masquer ces écarts. [Avant](LEGACY_BEFORE.json), [après](LEGACY_AFTER.json), [interprétation](LEGACY_EXPECTATIONS.md).
- Aucun reçu humain nouveau, aucune exécution moteur automatisée. Git HEAD/branche/index inchangés ; aucune opération Git d'écriture, aucune modification du vanilla. Les contrôles finaux, manifestes et protections se trouvent dans `FINAL_CHECKS.json`, `FILES_MODIFIED.json` et `CONCURRENT_CHANGES.json`.

## Suivi et prochaine action

Les trois sous-lots sont **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun `PASS_RUNTIME_USER_VALIDATED` créé. Leurs incertitudes ne sont pas effacées par les tests statiques.

**Progression SERG avant/après : 93/235 → 93/235 points, 39,57 % → 39,57 %, 32/81 tâches qualifiées**, périmètre 1.0.0 inchangé. Aucun crédit pour une correction extérieure au SERG.

**Prochaine action : [test joueur groupé](PLAYER_TEST_PROTOCOL.md)** des trois sous-lots polono-prussiens et, dans la même partie si souhaité, des installations saxonnes encore en attente. Aucun autre territoire commencé automatiquement.

La livraison est dans **{ROOT.as_posix()}**. Les autres copies du mod et le hotfix ne sont pas synchronisés automatiquement ; vérifier le chemin chargé dans le lanceur.
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')

def finalize():
    import serg_closure_roadmap as roadmap
    b=load('BASELINE.json');i=load('INSTALLATION.json');v=load('VALIDATION.json');t=load('TEST_RESULTS.json');beforelegacy=load('LEGACY_BEFORE.json');afterlegacy=load('LEGACY_AFTER.json')
    allowed={r['file'] for r in i['changes']};now=runtime_hashes();drift=[n for n in set(now)|set(b['runtime']) if now.get(n)!=b['runtime'].get(n) and n not in allowed]
    oldproofdrift=[n for n,h in {**b['previous_delivery'],**b['archived_polish_proofs']}.items() if sha(ROOT/n)!=h]
    state=roadmap.load_json(CANON/'ROADMAP_STATE.json');previous=load('ROADMAP_STATE_BEFORE.json');p=roadmap.progress(state);canonical=roadmap.check();dump('CANONICAL_AFTER.json',canonical)
    diff=subprocess.run(['git','--no-optional-locks','diff','--check'],capture_output=True,text=True);(OUT/'DIFF_CHECK_RAW.txt').write_text(diff.stdout+diff.stderr,encoding='utf-8')
    checks=[]
    def ck(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
    ck('Current static checks PASS',v['status']=='PASS' and v['passed']==v['total'] and not v['failed'])
    ck('Targeted tests PASS',t['failures']==t['errors']==0 and t['passed']>0)
    oldset={r['test'] for r in beforelegacy['failures']};newset={r['test'] for r in afterlegacy['failures']}
    ck('Legacy expectations precisely classified',beforelegacy['total']==afterlegacy['total']==8 and len(oldset)==2 and len(newset)==3 and oldset<=newset and all('thorn_really_unchanged' in n for n in newset-oldset) and not beforelegacy['errors'] and not afterlegacy['errors'])
    ck('Installed files exact',all(sha(ROOT/r['file'])==r['after'] for r in i['changes']))
    ck('Other concurrent runtime files exact',not drift,drift)
    ck('Historical and previous delivery proofs exact',not oldproofdrift,oldproofdrift)
    ck('Old delivery tools exact',all(sha(ROOT/n)==h for n,h in b['previous_tools'].items() if n!='tools/map2l_registry.py'))
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],capture_output=True,text=True);ck('Git '+name+' exact',r.returncode==0 and r.stdout.strip()==b['git'][name])
    ck('Git index exact',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    ck('Canonical validator PASS',canonical['status']=='PASS',canonical['errors'])
    ck('81 tasks 235 points scope 1.0.0 exact',state['tasks']==previous['tasks'] and len(state['tasks'])==81 and p['total_weight']==235 and state['scope_version']=='1.0.0')
    ck('93 points 39.57 percent 32 qualified unchanged',p['earned_weight']==93 and p['percent']=='39.57' and p['qualified_tasks']==32)
    ck('Event history prefix exact',state['events'][:len(previous['events'])]==previous['events'])
    ck('Progress history additive',(CANON/'PROGRESS_HISTORY.md').read_bytes().decode('utf-8').startswith(load('TRACKER_BEFORE.json')['PROGRESS_HISTORY.md']))
    delivery=state['external_prussian_deliveries'][-1]
    ck('External delivery pending player without points',delivery['external_to_hre'] and delivery['management_points']==0 and delivery['human_attestation'] is None and delivery['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and all(l['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and l['attestation'] is None for l in delivery['sub_lots']))
    ck('No new human receipt',not any('RECEIPT' in p.name.upper() or 'ATTESTATION' in p.name.upper() for p in OUT.rglob('*') if p.is_file()))
    ck('No next territory or Bavaria started',state['release_focus']['next_pass_started'] is False and state['release_focus']['bavaria_started'] is False)
    ck('Diff check clean',diff.returncode==0,dict(returncode=diff.returncode,raw='DIFF_CHECK_RAW.txt'))
    ck('Required delivery documents present',all((OUT/n).exists() for n in ['REPORT.md','SOURCES.md','PLAYER_TEST_PROTOCOL.md','VALIDATION.json','TEST_RESULTS.json','LEGACY_EXPECTATIONS.md','LOCATOR_RELOCATION.json']))
    failed=[r for r in checks if not r['passed']]
    dump('CONCURRENT_CHANGES.json',dict(runtime_files_captured=len(b['runtime']),runtime_files_changed=[r for r in i['changes'] if r['file'] in now],protected_runtime_drift=drift,protected_document_count=len(b['previous_delivery'])+len(b['archived_polish_proofs']),protected_document_drift=oldproofdrift,preexisting_git_status=b['git']['status'],policy='Current workspace only; no restore, no Git mutation, no vanilla write, no cross-checkout synchronization'))
    dump('FINAL_CHECKS.json',dict(status='FAIL' if failed else 'PASS',passed=len(checks)-len(failed),total=len(checks),failed=failed,checks=checks,progress_before=b['progress'],progress_after=p,external_to_hre=True,engine_test=False,human_receipts_added=0))
    tracking=[dict(file=(CANON/n).relative_to(ROOT).as_posix(),after=sha(CANON/n)) for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]
    dump('FILES_MODIFIED.json',dict(installed_files=i['changes'],tracking_updates=tracking,new_tool=dict(file='tools/serg_prussia_poland.py',sha256=sha(ROOT/'tools/serg_prussia_poland.py')),new_evidence=[dict(file=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in OUT.rglob('*') if p.is_file() and p.name!='FILES_MODIFIED.json']))
    print('Final',len(checks)-len(failed),'/',len(checks),'; diff',diff.returncode);assert not failed,failed

if __name__=='__main__':globals()[sys.argv[1]]()
