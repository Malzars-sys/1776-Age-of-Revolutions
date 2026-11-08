"""Northern Saxony, one scoped continuation of Prussia V1. No Git writes."""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re
import subprocess
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import values
from map2l_belgium import packed,components

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/SERG_CLOSURE/NORTH_SAXONY_1_2026_11_05'
CANON=OUT.parent
PRIOR=CANON/'PRUSSIA_V1_2026_11_02'
REGIONS={'STATE_ANHALT','STATE_BRANDENBURG'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def runtime_hashes():
    return {p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','events','map_data','gfx','gui','localization'] for p in (ROOT/folder).rglob('*') if p.is_file()}
def capture():
    import serg_closure_roadmap as roadmap
    from map2l_registry import active_registry_path
    OUT.mkdir(exist_ok=True);(OUT/'EVIDENCE').mkdir(exist_ok=True)
    assert not (OUT/'BASELINE.json').exists()
    originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_bytes().decode('utf-8')
            if any(s in raw for s in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    git={}
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current']),('git_dir',['rev-parse','--absolute-git-dir']),('status',['status','--porcelain=v1'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],capture_output=True,text=True);assert r.returncode==0,r.stderr;git[name]=r.stdout.strip()
    git['index_sha256']=sha(Path(git['git_dir'])/'index')
    (OUT/'provinces_before.png').write_bytes((ROOT/'map_data/provinces.png').read_bytes())
    (OUT/'ROADMAP_STATE_BEFORE.json').write_bytes((CANON/'ROADMAP_STATE.json').read_bytes())
    hashes=runtime_hashes();inv=qa.inventory();state=roadmap.load_json(CANON/'ROADMAP_STATE.json')
    dump('BASELINE.json',dict(runtime=hashes,hashes=hashes,inventory=inv,git=git,originals=originals,
         bitmap_backup=(OUT/'provinces_before.png').relative_to(ROOT).as_posix(),bitmap_sha256=sha(ROOT/'map_data/provinces.png'),
         registry=json.loads(active_registry_path().read_text()),progress=roadmap.progress(state),canonical_check=roadmap.check(),
         previous_delivery={p.relative_to(ROOT).as_posix():sha(p) for p in PRIOR.rglob('*') if p.is_file()},
         source_tool_sha256=sha(ROOT/'tools/serg_prussia_v1.py')))
    print('Captured current delivery:',len(hashes),'runtime files; progress',roadmap.progress(state)['percent'])

TOWNS=[('Wittenberg',12.646,51.866,'SAX'),('Torgau',13.,51.561,'SAX'),('Belzig',12.588,52.143,'SAX'),
       ('Juterbog',13.08,51.997,'SAX'),('Dahme',13.428,51.871,'SAX'),('Baruth',13.504,52.049,'SAX'),
       ('Annaburg',13.047,51.733,'SAX'),('Liebenwerda',13.394,51.518,'SAX'),('Elsterwerda',13.519,51.46,'SAX'),
       ('Herzberg',13.22,51.69,'SAX'),('Duben',12.586,51.59,'SAX'),('Bitterfeld',12.325,51.624,'SAX'),
       ('Delitzsch',12.345,51.525,'SAX'),('Eilenburg',12.63,51.46,'SAX'),('Merseburg',12.,51.355,'SAX'),
       ('Halle',11.975,51.48,'PRU'),('Magdeburg',11.635,52.13,'PRU'),('Naumburg',11.809,51.153,'SAX'),
       ('Zeitz',12.136,51.049,'SAX'),('Dessau',12.243,51.831,'ANH'),('Potsdam',13.064,52.398,'PRU')]
def inspect():
    from georeference.model import forward
    b=load('BASELINE.json');a=packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    rows=[];box=(4335,775,4435,845);local=a[775:845,4335:4435];arr=np.full((*local.shape,3),220,dtype=np.uint8)
    colors={'PRU':(118,155,194),'SAX':(150,186,112),'ANH':(235,172,92),'AZR':(230,130,90),'AKT':(210,150,80),'ABG':(220,125,80),'BRA':(180,165,140)}
    for v in np.unique(local):arr[local==v]=colors.get(owners.get('x'+format(int(v),'06X')),(220,220,220))
    im=Image.fromarray(arr).resize((1400,980),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for name,lon,lat,wanted in TOWNS:
        x,y=forward(model,[[lon,lat]])[0];rgb='x'+format(int(a[int(y),int(x)]),'06X');owner=owners.get(rgb)
        rows.append(dict(name=name,lon=lon,lat=lat,x=float(x),y=float(y),rgb=rgb,current_owner=owner,expected=wanted,certified_city_location=False))
        px,py=(x-box[0])*14,(y-box[1])*14;d.ellipse((px-3,py-3,px+3,py+3),fill='red');d.text((px+3,py),name,font=font,fill='black',stroke_width=1,stroke_fill='white')
        print(name,round(x,2),round(y,2),rgb,owner,wanted)
    im.save(OUT/'CURRENT_NORTH_SAXONY.png');dump('TOWN_DIAGNOSTICS_BEFORE.json',rows)

def geometry():
    """Political B reading of Schenk 1758; frozen native georeference."""
    from georeference.model import forward
    from map2l_franconia import inside
    b=load('BASELINE.json');assert runtime_hashes()==b['runtime']
    a=packed(OUT/'provinces_before.png')
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    controls=[('Wittenberg',1318,444,12.646,51.866),('Torgau',1489,726,13.,51.561),
              ('Juterbog',1465,370,13.08,51.997),('Baruth',1636,271,13.504,52.049),
              ('Leipzig',1190,869,12.373,51.34),('Halle',1001,724,11.975,51.48),
              ('Dessau',1086,476,12.243,51.831)]
    design=np.array([[x,y,1] for _,x,y,_,_ in controls]);target=forward(model,[[lon,lat] for _,_,_,lon,lat in controls])
    matrix=np.linalg.lstsq(design,target,rcond=None)[0]
    # One macro envelope: northern Kurkreis and its Meissen/Leipzig raccord.
    # Interior district colours do not imply separate sovereign countries.
    # Anhalt and all non-Prussian pixels remain immutable regardless of this reading.
    outline=[(1197, 166), (1228, 167), (1266, 148), (1305, 146), (1330, 130), (1353, 130), (1370, 141), (1397, 126), (1428, 108), (1442, 109), (1447, 136), (1450, 174), (1410, 181), (1383, 178), (1356, 186), (1343, 213), (1319, 230), (1309, 250), (1311, 267), (1330, 279), (1325, 294), (1350, 307), (1385, 307), (1402, 320), (1408, 346), (1432, 349), (1460, 345), (1481, 349), (1507, 364), (1518, 374), (1518, 393), (1533, 399), (1550, 390), (1570, 382), (1585, 373), (1584, 348), (1578, 319), (1579, 295), (1581, 277), (1595, 254), (1620, 242), (1656, 239), (1684, 228), (1707, 230), (1720, 241), (1723, 266), (1697, 281), (1667, 290), (1647, 304), (1650, 346), (1658, 375), (1667, 387), (1672, 402), (1653, 417), (1646, 439), (1643, 454), (1664, 468), (1690, 466), (1727, 478), (1721, 491), (1700, 500), (1679, 532), (1662, 551), (1642, 579), (1660, 587), (1680, 601), (1697, 625), (1715, 658), (1714, 677), (1696, 692), (1712, 715), (1748, 716), (1770, 738), (1787, 752), (1790, 1000), (1190, 1000), (1148, 830), (1143, 795), (1114, 779), (1092, 754), (1080, 733), (1078, 708), (1080, 675), (1075, 645), (1071, 626), (1104, 614), (1110, 590), (1120, 570), (1155, 560), (1155, 546), (1129, 534), (1100, 529), (1105, 505), (1150, 502), (1173, 490), (1184, 468), (1200, 453), (1206, 432), (1202, 410), (1193, 393), (1177, 389), (1167, 371), (1145, 352), (1120, 343), (1100, 332), (1090, 313), (1060, 304), (1020, 304), (996, 305), (976, 312), (955, 318), (930, 306), (930, 276), (909, 268), (902, 295), (886, 312), (879, 338), (864, 350), (859, 374), (847, 389), (827, 397), (798, 393), (783, 383), (784, 350), (780, 314), (788, 287), (805, 276), (795, 265), (777, 253), (775, 224), (804, 220), (831, 211), (852, 190), (869, 183), (884, 194), (897, 215), (918, 231), (953, 248), (991, 255), (1020, 251), (1051, 242), (1075, 239), (1098, 245), (1101, 217), (1110, 201), (1133, 207), (1153, 193), (1174, 177)]
    poly=np.c_[np.array(outline),np.ones(len(outline))]@matrix
    # Only the two scoped states, and only current PRU. Western outliers are
    # deliberately outside Nord saxon 1: do not reopen Magdeburg/Barby/Mansfeld.
    yy,xx=np.mgrid[775:835,4355:4435];points=np.c_[(xx+.5).ravel(),(yy+.5).ravel()]
    mask=inside(points,poly).reshape(xx.shape)
    oldowners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    scoped_parents={'x34386E','x83B1A8','x9B9076','xA65DA6','xCF5D8E','xDF4020'}
    eligible=[int(rgb[1:],16) for rgb,(sid,owner) in oldowners.items() if sid in REGIONS and owner=='PRU' and rgb in scoped_parents]
    selected=np.zeros(a.shape,dtype=bool);selected[775:835,4355:4435]=mask & np.isin(a[775:835,4355:4435],eligible)
    # Baruth is Saxon in the primary map. The frozen native city's coarse
    # point is one border cell beyond the affine reading (1.55 px residual).
    # Include that adjacent cell as an explicit political B generalisation,
    # never as a refit of the native model or an exact cadastral claim.
    baruth_cell=(4406,799)
    x,y=baruth_cell
    assert int(a[y,x]) in eligible and any(selected[ny,nx] for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
    selected[y,x]=True
    # The new Schenk trace meets the earlier Lotter trace along an internal
    # Saxon district boundary. Close the two reviewed raster seams, not Cottbus
    # or the unresolved Anhalt/Saale fringes.
    seams=load('SEAM_REVIEW.json')['cells'];assert len(seams)==30
    for x,y in seams:
        assert 4405<=x<=4409 and 803<=y<=813 and int(a[y,x]) in eligible and not selected[y,x]
        selected[y,x]=True
    after=a.copy();parents=[];assignments=[];new=[];nextval=0xEEC100
    for v in sorted(np.unique(a[selected])):
        rgb='x'+format(int(v),'06X');sid,owner=oldowners[rgb];parent=a==v;moved=parent&selected
        # Whole parents retain their RGB; partial parents acquire one child.
        retained=parent&~selected;parents.append(rgb)
        if retained.any():
            assert not (a==nextval).any();child='x'+format(nextval,'06X');after[moved]=nextval;nextval+=1
            new.append(dict(rgb=child,parent_rgb=rgb))
            assignments.append(dict(rgb=rgb,parent_rgb=rgb,state=sid,previous_owner=owner,owner='PRU',pixels=int(retained.sum())))
        else:child=rgb
        assignments.append(dict(rgb=child,parent_rgb=rgb,state=sid,previous_owner=owner,owner='SAX',pixels=int(moved.sum())))
    rgb=np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=-1).astype(np.uint8);Image.fromarray(rgb).save(OUT/'provinces_candidate.png')
    g=dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,parents=parents,assignments=assignments,new_provinces=new,hub_rebindings=[],candidate_sha256=sha(OUT/'provinces_candidate.png'),changed_pixels=int((a!=after).sum()),ownership_cells=int(selected.sum()))
    g['saxon_internal_seam_cells']=seams
    dump('GEOMETRY.json',g)
    dump('TRACING.json',dict(source='Schenk 1758, Bern MUE Ryh 5301:30; e-rara-124790',controls=controls,source_to_native_matrix=matrix.tolist(),residuals_px=np.linalg.norm(design@matrix-target,axis=1).tolist(),source_outline=outline,native_outline=poly.tolist(),classification=g['classification'],native_model_unchanged=True,imperial_owners=['PRU','SAX','ANH','AZR','AKT','ABG'],scope=dict(states=sorted(REGIONS),parent_envelope=sorted(scoped_parents),reason='Coherent eastern Kurkreis/Meissen core; western outliers and Saale frontier deferred, not certified'),political_B_border_cell=dict(name='Baruth',pixel=list(baruth_cell),additional_cells=1,reason='Adjacent Saxon border cell; affine source residual 1.55 px'),non_prussian_pixels_immutable=True))
    print('Fit residuals',np.linalg.norm(design@matrix-target,axis=1));print('Transferred',selected.sum(),'cells;',len(new),'new RGBs',parents)
    review=Image.open(OUT/'EVIDENCE/SCHENK_SAXONY.jpg').convert('RGB');d=ImageDraw.Draw(review);d.line(outline+[outline[0]],fill='blue',width=4)
    for name,x,y,_,_ in controls:d.ellipse((x-5,y-5,x+5,y+5),fill='red');d.text((x+7,y+7),name,fill='blue',stroke_width=1,stroke_fill='white')
    review.crop((700,80,1850,1150)).save(OUT/'SOURCE_TRACE_REVIEW.jpg')
    preview()

def preview():
    b=load('BASELINE.json');g=load('GEOMETRY.json');a=packed(OUT/'provinces_candidate.png');old=packed(OUT/'provinces_before.png')
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners.update({r['rgb']:r['owner'] for r in g['assignments']})
    box=(4335,775,4435,845);colors={'PRU':(118,155,194),'SAX':(150,186,112),'ANH':(235,172,92),'AZR':(230,130,90),'AKT':(210,150,80),'ABG':(220,125,80)}
    local=a[775:845,4335:4435];arr=np.full((*local.shape,3),220,dtype=np.uint8)
    for v in np.unique(local):arr[local==v]=colors.get(owners.get('x'+format(int(v),'06X')),(220,220,220))
    im=Image.fromarray(arr).resize((1400,980),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    rows=[]
    for r in load('TOWN_DIAGNOSTICS_BEFORE.json'):
        r=r.copy();x,y=r['x'],r['y'];r['after_rgb']='x'+format(int(a[int(y),int(x)]),'06X');r['after_owner']=owners.get(r['after_rgb']);rows.append(r)
        px,py=(x-box[0])*14,(y-box[1])*14;d.ellipse((px-3,py-3,px+3,py+3),fill='red');d.text((px+3,py),r['name'],font=font,fill='black',stroke_width=1,stroke_fill='white')
    im.save(OUT/'NORTH_SAXONY_CANDIDATE.png');dump('TOWN_DIAGNOSTICS_CANDIDATE.json',rows)
    for r in rows:print(r['name'],r['current_owner'],'->',r['after_owner'])

def prepare():
    import map2l_mainz as core
    import map2m_r9 as old
    from map2l_registry import active_registry_path
    b=load('BASELINE.json');g=load('GEOMETRY.json');a=packed(OUT/'provinces_before.png');candidate=packed(OUT/'provinces_candidate.png')
    locs=old.locators(a)
    raw=b['originals']['map_data/state_regions/00_west_europe.txt']
    for sid in sorted(REGIONS):
        s=next(n for n in cw.parse(raw) if n.key==sid)
        for kind in ['city','farm','mine','wood','port']:
            fields=s.children(kind)
            if not fields:continue
            parent=cw.scalar(fields[0].value)
            if parent not in g['parents']:continue
            actual=[r for r in locs if r['Kind']==kind and r['ID']==int(s.one('id'))]
            assert len(actual)==1
            x,y=actual[0]['X'],actual[0]['Y'];assert 'x'+format(int(a[int(y),int(x)]),'06X')==parent
            rgb='x'+format(int(candidate[int(y),int(x)]),'06X')
            if rgb!=parent:g['hub_rebindings'].append(dict(state=sid,field=kind,before=parent,after=rgb,point=[x,y],pixel=[int(x),int(y)],locator_moved=False))
    for r in g['assignments']:
        ys,xs=np.where(candidate==int(r['rgb'][1:],16));r['cells']=[[int(x),int(y)] for y,x in zip(ys,xs)]
        r['components_4']=sorted([len(c) for c in components(candidate==int(r['rgb'][1:],16))],reverse=True)
    dump('GEOMETRY.json',g)
    core.OUT=OUT;core.REGIONS=REGIONS;core.REGION_FILE='map_data/state_regions/00_west_europe.txt'
    # Retain military, arms and institutional installations. Divide only
    # existing civil production/infrastructure, keeping its PMs and holders.
    civil={'building_logging_camp','building_livestock_ranch','building_rye_farm','building_coal_mine','building_iron_mine','building_lead_mine','building_paper_mill','building_railway'}
    core.BUILDING_ALLOCATION_WEIGHTS={}
    for rel,text in b['originals'].items():
        if '/buildings/' not in rel:continue
        for sid in REGIONS:
            try:n=core.region(text,sid,'PRU')
            except StopIteration:continue
            for build in n.children('create_building'):
                kind=cw.scalar(build.one('building'))
                if kind not in civil:core.BUILDING_ALLOCATION_WEIGHTS[rel,sid,'PRU',kind]={'PRU':1,'SAX':0}
    before={};expected={}
    def extra(files,migration):
        migration['country_additions']={}
        assert migration['extent_added_cells']==migration['extent_removed_cells']==[]
        rel='tools/map2l_registry.py';raw=(ROOT/rel).read_bytes().decode('utf-8')
        anchor='    return result\n\ndef provincial_membership_overrides'
        if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
        assert raw.count(anchor)==1
        guard='''    north_saxony=ROOT/'docs/reports/map/SERG_CLOSURE/NORTH_SAXONY_1_2026_11_05'
    if (north_saxony/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((north_saxony/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((north_saxony/'GEOMETRY.json').read_text(encoding='utf8'))
        assert prussia in result
        assert m['replaced_regions']==['STATE_ANHALT','STATE_BRANDENBURG']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert set(g['parents'])=={'x34386E','x83B1A8','x9B9076','xA65DA6','xCF5D8E','xDF4020'}
        assert g['ownership_cells']==606 and len(g['new_provinces'])==5
        assert all(r['state'] in m['replaced_regions'] and r['previous_owner']=='PRU' and r['owner'] in {'PRU','SAX'} for r in g['assignments'])
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items() if k not in g['parents'])
        assert len(new)==len(old)+len(g['new_provinces'])
        assert {(r['rgb'],r['state'],r['beneficiary']) for r in m['updated'] if r['rgb'] not in old or r['rgb'] in g['parents']}=={(r['rgb'],r['state'],r['owner']) for r in g['assignments']}
        result.append(north_saxony)
'''
        files[rel]=raw.replace(anchor,guard+anchor)
        files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    core.PREPARE_EXTRA_FILES=extra
    def emit(files,name):
        for rel,text in files.items():
            if rel.startswith(OUT.relative_to(ROOT).as_posix()+'/'):
                (ROOT/rel).write_text(text,encoding='utf-8');continue
            previous=(ROOT/rel).read_bytes().decode('utf-8');before[rel]=previous
            if previous.startswith('\ufeff') and not text.startswith('\ufeff'):text='\ufeff'+text
            if '\r\n' in previous and previous.count('\n')==previous.count('\r\n'):text=text.replace('\r\n','\n').replace('\n','\r\n')
            if text!=previous:expected[rel]=text
        return sorted(expected)
    core.emit=emit;core.prepare()
    rel='map_data/province_terrains.txt';previous=(ROOT/rel).read_bytes().decode('utf-8');text=(OUT/'province_terrains_candidate.txt').read_text(encoding='utf-8')
    if previous.startswith('\ufeff'):text='\ufeff'+text.lstrip('\ufeff')
    if '\r\n' in previous and previous.count('\n')==previous.count('\r\n'):text=text.replace('\r\n','\n').replace('\n','\r\n')
    before[rel]=previous;expected[rel]=text
    # Avoid adding whitespace-only lines; retain every original byte outside
    # generated changes and every pre-existing blank line.
    for rel,text in list(expected.items()):
        old_lines=before[rel].splitlines(True);new_lines=text.splitlines(True);parts=[]
        for tag,i,j,k,l in difflib.SequenceMatcher(None,old_lines,new_lines,autojunk=False).get_opcodes():
            lines=new_lines[k:l]
            if tag!='equal':lines=[line if line.strip() else ('\r\n' if line.endswith('\r\n') else '\n') for line in lines]
            parts.extend(lines)
        expected[rel]=''.join(parts)
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',expected)
    plan=load('PLAN.json');plan.update(files=sorted(expected),runtime_installed=False,population_method='Exact integer technical redistribution of current PRU profiles, not a historical census',preserved_PRU_arms_levels=6)
    dump('PLAN.json',plan)
    print('Prepared',len(expected),'text files; no installation')

def compile_prepare():
    import serg_prussia_v1 as prior
    prior.OUT=OUT;prior.compile_prepare()

def install():
    import serg_prussia_v1 as prior
    prior.OUT=OUT;prior.install()

def verify():
    import map2l_registry as registry
    import serg_closure_roadmap as roadmap
    b=load('BASELINE.json');g=load('GEOMETRY.json');installation=load('INSTALLATION.json');inv=qa.inventory();dump('INVENTORY_AFTER.json',inv)
    before=packed(OUT/'provinces_before.png');after=packed(ROOT/'map_data/provinces.png');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
    ck('Bitmap equals final reviewed candidate',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
    ck('Exact 606 PRU to SAX cells',sum(r['pixels'] for r in g['assignments'] if r['owner']=='SAX')==606)
    wanted=qa.counter(b['inventory']['owners']).copy()
    for r in b['inventory']['owners']:
        if r['key'][0] in g['parents']:del wanted[tuple(r['key'])]
    for r in g['assignments']:wanted[r['rgb'],r['state'],r['owner']]+=1
    ck('Exact worldwide ownership delta',qa.counter(inv['owners'])==wanted)
    ck('No additional duplicates',inv['duplicates']==b['inventory']['duplicates'])
    ck('No new wrong-state or orphan references',inv['errors']==b['inventory']['errors'])
    ck('Five new valid RGB references',len(g['new_provinces'])==5 and all(inv['geometry'][r['rgb']]==inv['geometry'][r['parent_rgb']] for r in g['new_provinces']))
    allowed=np.isin(before,[int(rgb[1:],16) for rgb in g['parents']])
    ck('Pixels outside six parents exact',np.array_equal(after[~allowed],before[~allowed]))
    beforeowners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};afterowners={r['key'][0]:r['key'][2] for r in inv['owners']}
    nonpru=np.isin(before,[int(rgb[1:],16) for rgb,tag in beforeowners.items() if tag!='PRU'])
    ck('All non-Prussian cells preserved',np.array_equal(after[nonpru],before[nonpru]))
    for r in g['assignments']:
        ys,xs=np.where(after==int(r['rgb'][1:],16));ck('Exact cell set '+r['rgb'],set(zip(xs.tolist(),ys.tolist()))=={tuple(c) for c in r['cells']} and len(xs)==r['pixels'])
    prior=json.loads((PRIOR/'GEOMETRY.json').read_text());oldcells=[tuple(c) for r in prior['assignments'] if r['owner']=='SAX' for c in r['cells']]
    ck('Previous 811 Lusatian cells exact',len(oldcells)==811 and all(after[y,x]==before[y,x] and afterowners['x'+format(int(after[y,x]),'06X')]=='SAX' for x,y in oldcells))
    ck('Previous delivery evidence untouched',all(sha(ROOT/rel)==digest for rel,digest in b['previous_delivery'].items()))
    ck('Previous delivery tool untouched',sha(ROOT/'tools/serg_prussia_v1.py')==b['source_tool_sha256'])
    towns=load('TOWN_DIAGNOSTICS_CANDIDATE.json')
    ck('Fourteen scoped coarse town diagnostics SAX',all(r['after_owner']=='SAX' for r in towns[:14]),'Coarse native model diagnostics, not independently certified city positions')
    ck('Halle Magdeburg Potsdam and Dessau retained',all(r['after_owner']==r['current_owner'] for r in towns if r['name'] in {'Halle','Magdeburg','Potsdam','Dessau'}))
    pru=np.isin(after,[int(rgb[1:],16) for rgb,tag in afterowners.items() if tag=='PRU']);parts=components(pru)
    enclave=next(c for c in parts if (808,4424) in c)
    ck('Cottbus Peitz remains 86-cell Prussian enclave',len(enclave)==86 and (787,4400) not in enclave)
    ck('Internal Saxon seam has no artificial PRU islands',all(afterowners['x'+format(int(after[y,x]),'06X')]=='SAX' for x,y in load('SEAM_REVIEW.json')['cells']))
    ck('No native locator changes',not any('/map_object_data/' in r['file'] for r in installation['changes']) and all(not r['locator_moved'] for r in g['hub_rebindings']))
    ck('Global population profiles and resolved demographics exact',inv['pops']==b['inventory']['pops'] and inv['resolved_demographics']==b['inventory']['resolved_demographics'])
    ck('Global written population exact',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in b['inventory']['pops']))
    regional=qa.counter(inv['regional_pop']);oldregional=qa.counter(b['inventory']['regional_pop']);plan=load('PLAN.json')
    ck('Populations outside scoped states exact',{k:v for k,v in regional.items() if k[0] not in REGIONS}=={k:v for k,v in oldregional.items() if k[0] not in REGIONS})
    for sid in REGIONS:
        moved=sum(r['after'].get('SAX',0) for r in plan['allocations'] if r['kind']=='population' and r['state']==sid)
        ck('Saxon population addition '+sid,sum(v for k,v in regional.items() if k[:2]==(sid,'SAX'))==sum(v for k,v in oldregional.items() if k[:2]==(sid,'SAX'))+moved)
    ck('All military units and recruitment exact',inv['units']==b['inventory']['units'])
    ck('All country definitions exact',inv['countries']==b['inventory']['countries'])
    ck('All building declarations PMs levels and economic holders exact',inv['buildings']==b['inventory']['buildings'] and inv['building_levels_written']==b['inventory']['building_levels_written'])
    ledger=json.loads(registry.active_registry_path().read_text());migration=load('REGISTRY_MIGRATION.json');oldledger=b['registry']
    ck('592 unique imperial titles from 587',len(ledger)==592 and len({r['rgb'] for r in ledger})==592 and len(oldledger)==587)
    ck('Physical imperial extent unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in oldledger]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    ck('Only reviewed registry rights changed',sorted([r for r in oldledger if r['state'] not in REGIONS]+migration['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))==ledger)
    ck('Ordered migration appended',registry.approved_lot_dirs()[-1]==OUT)
    from map2k_patch import ELECTORS
    ck('Nine electors preserved',len(ELECTORS)==9)
    changed={r['file'] for r in installation['changes']}
    for r in installation['changes']:ck('Installed digest '+r['file'],sha(ROOT/r['file'])==r['after'])
    now=runtime_hashes();drift=[p for p in set(now)|set(b['runtime']) if now.get(p)!=b['runtime'].get(p) and p not in changed]
    ck('Other concurrent runtime files untouched',not drift,drift)
    for rel in changed:
        if rel.endswith('.txt'):cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    ck('Changed game scripts parse',True)
    ck('No new country technology military or building file',not migration['new_members'] and not migration['country_additions'] and not any('/technology/' in p or '/countries/' in p or '/buildings/' in p or '/military' in p for p in changed))
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],capture_output=True,text=True);ck('Git '+name+' unchanged',r.returncode==0 and r.stdout.strip()==b['git'][name])
    ck('Git index exact',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    canonical=roadmap.check();dump('CANONICAL_AFTER.json',canonical)
    ck('Canonical validator PASS',canonical['status']=='PASS',canonical['errors'])
    ck('No unearned credit 93/235',canonical['progress']['earned_weight']==93 and canonical['progress']['total_weight']==235 and canonical['progress']['percent']=='39.57')
    state=roadmap.load_json(CANON/'ROADMAP_STATE.json');previous=load('ROADMAP_STATE_BEFORE.json')
    ck('Other 80 tasks including Silesia exact',[t for t in state['tasks'] if t['id']!='SC3-BRANDENBURG']==[t for t in previous['tasks'] if t['id']!='SC3-BRANDENBURG'])
    ck('Previous events exact',state['events'][:len(previous['events'])]==previous['events'])
    failed=[r for r in checks if not r['passed']];dump('VALIDATION.json',dict(status='FAIL' if failed else 'PASS',task_ids=['SC3-BRANDENBURG'],passed=len(checks)-len(failed),total=len(checks),failed=failed,checks=checks,engine_test=False,human_attestation=None))
    print('Static checks',len(checks)-len(failed),'/',len(checks));print(json.dumps(failed,ensure_ascii=False));assert not failed

def tracker():
    import serg_closure_roadmap as roadmap
    assert load('VALIDATION.json')['status']=='PASS'
    raw=(CANON/'ROADMAP_STATE.json').read_bytes();state=json.loads(raw);previous=load('ROADMAP_STATE_BEFORE.json')
    assert state==previous,'Concurrent tracking update: reconcile before writing'
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    t=next(t for t in state['tasks'] if t['id']=='SC3-BRANDENBURG');assert t['status']=='BLOCKED'
    t['installed_sub_lots'].extend([
        dict(id='NS1-KURKREIS',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope='Wittenberg/Torgau/Annaburg, Bitterfeld/Duben/Delitzsch/Eilenburg, STATE_ANHALT',cells=352,attestation=None),
        dict(id='NS1-FLAMING-MEISSEN',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope='Belzig/Juterbog/Dahme/Baruth, Herzberg/Liebenwerda/Elsterwerda, STATE_BRANDENBURG',cells=254,attestation=None)])
    t['implementation_report'] += [prefix+'REPORT.md',prefix+'SOURCES.md']
    t['installed_lots'].append('SERG_CLOSURE/NORTH_SAXONY_1_2026_11_05')
    t['historical_sources'].append(prefix+'SOURCES.md')
    t['static_tests']['evidence'].append(prefix+'VALIDATION.json')
    t['runtime_validation']['previous_protocol']=t['runtime_validation']['protocol']
    t['runtime_validation'].update(protocol=prefix+'PLAYER_TEST_PROTOCOL.md',scopes=[lot['id'] for lot in t['installed_sub_lots']],attestation=None,status='NOT_RUN')
    t['blocking_reason']='Noyaux lusacien et Nord saxon 1 installés, non reçus ; Magdebourg/Halberstadt, Gommern/Barby, Mansfeld/Saale et les autres limites et obligations régionales ne sont pas clôturés.'
    t['current_delivery_note']='606 cellules PRU→SAX supplémentaires (352 Anhalt technique, 254 Brandebourg), catégorie B ; noyau précédent de 393 cellules conservé et toujours en attente du joueur.'
    t['residual_uncertainty']='Généralisation politique B, pas un cadastre ; raccord interne saxon de 30 cellules et cellule de Baruth documentés. Franges d’Anhalt/Saale hors sous-lot non arbitrées.'
    state['release_focus'].update(current_pass='NORTH_SAXONY_1',current_delivery=prefix+'REPORT.md',next_requested_pass='PRUSSIA_POLISH_FRONTIER',next_pass_started=False,bavaria_started=False,
       continuation_authority='Instruction utilisateur : Passe au Nord saxon 1. Fini le puis après on finira la frontière polonaise.')
    state['runtime_validation_hold'].update(protocol=prefix+'PLAYER_TEST_PROTOCOL.md',reason='Nord saxon 1 installé ; test groupable avec les deux sous-lots lusaciens encore non attestés.',next_implementation_candidate=None,
       scope_note='Prochaine passe demandée : frontière polonaise prussienne, non commencée. Aucun reçu pour les trois sous-lots de SC3-BRANDENBURG ni pour la Haute-Lusace ; autres obligations conservées.')
    state['mission_status']='NORTH_SAXONY_1_INSTALLED_PENDING_RUNTIME_POLISH_FRONTIER_NEXT'
    before=roadmap.progress(previous);after=roadmap.progress(state)
    eid='SERG-RM-'+format(max(int(e['id'].rsplit('-',1)[1]) for e in state['events'])+1,'04d')
    state['events'].append(dict(id=eid,date='2026-11-05',kind='NORTH_SAXONY_1_INSTALLED',scope_version=state['scope_version'],source=prefix+'REPORT.md',
        changes=[dict(task_id='SC3-BRANDENBURG',before='BLOCKED',after='BLOCKED')],before_weight=before['earned_weight'],after_weight=after['earned_weight'],total_weight=after['total_weight'],before_percent=before['percent'],after_percent=after['percent'],
        note='606 cellules PRU→SAX supplémentaires, 352 Anhalt technique et 254 Brandebourg, deux sous-lots indépendamment testables. 811 cellules lusaciennes et preuves antérieures exactes, Cottbus/Peitz PRU conservé. Catégorie B ; aucun reçu humain, aucun point. Prochaine passe demandée : frontière polonaise, non commencée.',
        evidence=[prefix+'INSTALLATION.json',prefix+'VALIDATION.json',prefix+'PLAYER_TEST_PROTOCOL.md']))
    names=['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md'];texts={name:(CANON/name).read_bytes().decode('utf-8') for name in names};dump('TRACKER_BEFORE.json',texts)
    header='''## Livraison courante — Nord saxon 1, 5 novembre 2026

**606 cellules PRU → SAX supplémentaires installées** : 352 dans Anhalt technique, 254 dans le Brandebourg. Wittenberg/Torgau, Belzig/Jüterbog, Dahme/Baruth et raccord septentrional de Meissen ; catégorie B documentée. [Rapport](NORTH_SAXONY_1_2026_11_05/REPORT.md), [sources et limites](NORTH_SAXONY_1_2026_11_05/SOURCES.md), [protocole joueur groupable](NORTH_SAXONY_1_2026_11_05/PLAYER_TEST_PROTOCOL.md).

Deux sous-lots `NS1-KURKREIS` et `NS1-FLAMING-MEISSEN` : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. `SC3-BRANDENBURG` reste **BLOCKED** pour ses obligations régionales. Les 811 cellules lusaciennes précédentes, leurs preuves et les autres tâches sont conservées ; aucune attestation nouvelle. **93/235 = 39,57 %, 32/81** ; 592 titres impériaux, même étendue physique.

**À faire maintenant : test joueur groupé des installations prussiennes. Prochaine passe demandée : frontière polonaise de la Prusse, non commencée.** Les franges de Magdebourg/Halberstadt, Gommern/Barby, Mansfeld/Saale restent ouvertes ; cette passe ne les certifie pas. Aucun lancement de Bavière ou de micro-État. Les sections précédentes ci-dessous gardent leur valeur d'archive ; leur prochaine action historique ne remplace pas cet encadré.

'''
    updated={}
    for name in names[:3]:
        old=texts[name];idx=old.index('\n');new=old[:idx+1]+'\n'+header+old[idx+1:]
        if name=='NEXT_ACTION.md':new=new.replace(new.splitlines()[0],'# Prochaine action — validation Nord saxon 1 et Lusaces ; frontière polonaise ensuite',1)
        if name=='ROADMAP.md':
            anchor='#### SC3-BRANDENBURG —';start=new.index(anchor);end=new.find('\n#### ',start+1);end=len(new) if end<0 else end
            section=new[start:end];section=section.replace('\nRégion/périmètre :','\nNord saxon 1 ajouté aux sous-lots installés, sans clôture régionale ni point ; [livraison](NORTH_SAXONY_1_2026_11_05/REPORT.md).\n\nRégion/périmètre :',1);new=new[:start]+section+new[end:]
        updated[name]=new
    updated['PROGRESS_HISTORY.md']=texts['PROGRESS_HISTORY.md']+'\n\n## '+eid+' — 5 novembre 2026 — Nord saxon 1 installé\n\n606 cellules PRU→SAX supplémentaires : NS1-KURKREIS (352 Anhalt technique), NS1-FLAMING-MEISSEN (254 Brandebourg). Cinq RGB nouveaux, 592 titres impériaux et même étendue ; 811 cellules lusaciennes antérieures préservées. Catégorie B, trente cellules de raccord interne saxon et une cellule adjacente à Baruth explicitement documentées. Aucun bâtiment, unité, PM ou technologie modifié ; redistribution technique des populations existantes. SC3-BRANDENBURG reste BLOCKED, sous-lots prêts au joueur. Aucun reçu humain ni point : 93/235, 39,57 %, 32/81 ; les 80 autres tâches et événements antérieurs sont conservés. Prochaine passe demandée : frontière polonaise prussienne, non commencée. [Rapport](NORTH_SAXONY_1_2026_11_05/REPORT.md).\n'
    assert (CANON/'ROADMAP_STATE.json').read_bytes()==raw
    (CANON/'ROADMAP_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,text in updated.items():
        assert (CANON/name).read_bytes().decode('utf-8')==texts[name],name
        (CANON/name).write_bytes(text.encode('utf-8'))
    roadmap.write_json(CANON/'PROGRESS_SNAPSHOT.json',roadmap.progress(state));dump('TRACKER_CHANGE.json',dict(event=eid,before=before,after=after,human_receipts_added=0,changed_task_ids=['SC3-BRANDENBURG']))
    result=roadmap.check();dump('CANONICAL_AFTER.json',result);assert result['status']=='PASS',result['errors'];print(eid,result['progress']['percent'])

def tests():
    import time,unittest,io
    modules=['test_serg_closure_roadmap','test_map2l_registry'];suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(m) for m in modules);stream=io.StringIO();start= time.monotonic()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    (OUT/'TEST_RESULTS_RAW.txt').write_text(stream.getvalue(),encoding='utf-8')
    data=dict(total=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),elapsed_seconds=time.monotonic()-start,modules=modules,engine_test=False,workspace_digest=sha(ROOT/'map_data/provinces.png'))
    dump('TEST_RESULTS.json',data);print(json.dumps(data));assert result.wasSuccessful(),stream.getvalue()

def report():
    b=load('BASELINE.json');g=load('GEOMETRY.json');p=load('PLAN.json');v=load('VALIDATION.json');i=load('INSTALLATION.json');tests=load('TEST_RESULTS.json') if (OUT/'TEST_RESULTS.json').exists() else None
    moved={sid:sum(r['after'].get('SAX',0) for r in p['allocations'] if r['kind']=='population' and r['state']==sid) for sid in REGIONS}
    rows=['| Parent | SAX | PRU conservé |','| --- | ---: | ---: |']
    for parent in g['parents']:
        a=[r for r in g['assignments'] if r['parent_rgb']==parent];rows.append('| '+parent+' | '+str(sum(r['pixels'] for r in a if r['owner']=='SAX'))+' | '+str(sum(r['pixels'] for r in a if r['owner']=='PRU'))+' |')
    testline=(f"{tests['total']} tests exécutés : {tests['passed']} réussites, {tests['skipped']} exclusion, {tests['failures']} échec, {tests['errors']} erreur. L'exclusion est le contrôle ancien d'initialisation sans modification ; la conservation du workspace courant est vérifiée séparément.") if tests else 'Tests canoniques à exécuter après actualisation du suivi ; ne pas reprendre les chiffres précédents.'
    text=f'''# SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %

**Nord saxon 1 installé le 5 novembre 2026, en attente du test joueur.** Une seule passe, centrée sur les frontières prussiennes de 1776. Aucun travail sur la frontière polonaise, la Bavière ou les micro-États.

## Changements installés

**606 cellules PRU → SAX supplémentaires** : **NS1-KURKREIS, 352 cellules** dans Anhalt technique (Wittenberg–Torgau–Annaburg et raccord Bitterfeld/Düben/Delitzsch/Eilenburg) ; **NS1-FLAMING-MEISSEN, 254 cellules** dans le Brandebourg (Belzig/Jüterbog, Dahme/Baruth, Herzberg et raccord Liebenwerda/Elsterwerda).

La carte de Schenk de **1758** a été effectivement examinée, avec contrôle chronologique par les notices du Staatsarchiv. [Sources, décision et incertitudes](SOURCES.md). Le résultat est une **approximation politique B**, sans certification cadastrale. Les résidus de transformation de la feuille, 0,73–1,85 cellule, ne constituent pas une précision validée indépendamment.

![Carte de la livraison](NORTH_SAXONY_CANDIDATE.png)

{chr(10).join(rows)}

Cinq RGB nouveaux, `xEEC100` à `xEEC104` ; `x34386E` réattribué entier (**93 cellules**, même couleur). **513 cellules sont recolorées**, les 93 autres changent seulement de propriétaire. Deux ajustements B sont explicités : une cellule adjacente pour Baruth et **30 cellules de raccord interne saxon** entre les feuilles Schenk et Lotter. Les deux poches PRU de 27 et 3 cellules provenaient de ce raccord, pas d'une possession prussienne attestée. Aucun locator ou hub déplacé ; aucune référence de hub ne nécessite de changement.

Le registre passe de **587 à 592 titres** par subdivision, **avec la même étendue impériale**, les mêmes membres et les neuf électeurs. Les titres des portions transférées appartiennent à SAX. Les sept sorties impériales effectivement concernées sont régénérées depuis le workspace courant ; les autres sorties restent identiques. [Précontrôle du générateur](COMPILER_PREFLIGHT.json), [différence révisable](REVIEW.diff).

## Conservation et population

Les **811 cellules lusaciennes de la livraison précédente sont strictement préservées**, ainsi que toutes ses preuves et son outil. Leur attente de validation humaine demeure. Les noyaux d'Anhalt et tous les pixels initialement non prussiens sont inchangés. Cottbus/Peitz conserve son enclave prussienne de **86 cellules** ; Halle, Magdebourg et Potsdam restent prussiennes.

Redistribution technique des populations déjà écrites : **{moved['STATE_ANHALT']}** habitants vers SAX/Anhalt et **{moved['STATE_BRANDENBURG']}** vers SAX/Brandebourg, soit **{sum(moved.values())}** habitants existants. Aucun nouveau recensement, aucune correction historique d'effectif. Les ventilations culturelles/religieuses et le total mondial écrit (**{sum(r['count'] for r in b['inventory']['pops'])}**) sont conservés exactement.

**Aucun bâtiment ni niveau, aucun PM, détenteur économique, armement, recrutement ou unité modifié.** Aucun nouveau pays ou profil technologique. Les limites des régions économiques, ressources, terrains parents, capitales et autres historiques sont préservés. L'initialisation économique réelle des portions saxonnes reste à observer en jeu.

## Vérifications réellement exécutées

- Contrôles différentiels actuels : **{v['passed']}/{v['total']} PASS** ; [résultats](VALIDATION.json).
- {testline} [Résultats](TEST_RESULTS.json), [sortie brute](TEST_RESULTS_RAW.txt).
- Conservation des fichiers concurrents hors des modifications déclarées, des populations, bâtiments, unités, géométrie protégée, preuves et chaîne ordonnée du registre. Les anomalies héritées de références restent identiques, sans nouveau défaut dans le périmètre.
- Liste exacte des **{len(i['changes'])} fichiers installés**, avec empreintes avant/après : [installation](INSTALLATION.json). Contrôle final et état de concurrence dans `FINAL_CHECKS.json` et `CONCURRENT_CHANGES.json`.
- Aucun test moteur effectué par l'agent, aucun résultat humain nouveau, aucune opération Git d'écriture ou modification du vanilla.

Les premières préparations de contour et le précontrôle antérieur au raccord n'ont pas été installés. Seul le candidat final de 606 cellules figure dans le manifeste d'installation. Aucun ancien résultat brut ou ancienne baseline n'est réécrit pour rendre cette passe conforme.

## Statut, limites et prochaine action

Les deux nouveaux sous-lots sont **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. `SC3-BRANDENBURG` reste **BLOCKED** : Magdebourg/Halberstadt, Gommern/Barby, les parts de Mansfeld/Saale et les autres obligations régionales ne sont pas clôturés. Le diagnostic grossier de Mersebourg/Naumbourg et les franges d'Anhalt n'est pas résolu artificiellement. `SC3-SILESIA-LUSATIA` et les 79 autres fiches sont inchangées.

Le noyau Nord saxon 1 de cette passe est livré ; il ne représente pas toutes les corrections saxonnes possibles. Les petites îles de souveraineté et les franges non traitées sont documentées dans les sources ; elles ne sont pas déclarées historiquement exactes par défaut.

**Progression officielle : 93/235 → 93/235 points, 39,57 % → 39,57 %, 32/81 tâches qualifiées**, périmètre 1.0.0. Aucun point pour une installation partielle non reçue. Aucune nouvelle attestation `PASS_RUNTIME_USER_VALIDATED`.

**Prochaine action : [protocole joueur Nord saxon 1](PLAYER_TEST_PROTOCOL.md), groupable avec les Lusaces précédentes. Prochaine passe demandée : frontière polonaise prussienne, non commencée.** Les obligations mises en pause ne sont ni effacées ni créditées.

La livraison fonctionnelle se trouve uniquement dans **{ROOT.as_posix()}**. Les autres copies du mod et le hotfix ne sont pas synchronisés automatiquement.
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')

def finalize():
    import serg_closure_roadmap as roadmap
    b=load('BASELINE.json');i=load('INSTALLATION.json');state=roadmap.load_json(CANON/'ROADMAP_STATE.json');p=roadmap.progress(state);v=load('VALIDATION.json');t=load('TEST_RESULTS.json')
    changes=i['changes'];allowed={r['file'] for r in changes};now=runtime_hashes()
    drift=[rel for rel in set(now)|set(b['runtime']) if now.get(rel)!=b['runtime'].get(rel) and rel not in allowed]
    prior_drift=[rel for rel,digest in b['previous_delivery'].items() if sha(ROOT/rel)!=digest]
    diff=subprocess.run(['git','--no-optional-locks','diff','--check'],capture_output=True,text=True)
    (OUT/'DIFF_CHECK_RAW.txt').write_text(diff.stdout+diff.stderr,encoding='utf-8')
    texts=load('TRACKER_BEFORE.json');previous=load('ROADMAP_STATE_BEFORE.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
    ck('Final static checks PASS',v['status']=='PASS' and v['passed']==v['total'] and not v['failed'])
    ck('Targeted tests pass',t['failures']==t['errors']==0 and t['passed']>0)
    ck('Installed bytes exact',all(sha(ROOT/r['file'])==r['after'] for r in changes))
    ck('Protected runtime hashes exact',not drift,drift)
    ck('Previous delivery proofs exact',not prior_drift,prior_drift)
    ck('Previous delivery source tool exact',sha(ROOT/'tools/serg_prussia_v1.py')==b['source_tool_sha256'])
    ck('Index exact',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],capture_output=True,text=True);ck('Git '+name+' exact',r.returncode==0 and r.stdout.strip()==b['git'][name])
    canonical=roadmap.check();dump('CANONICAL_AFTER.json',canonical);ck('Canonical validator PASS',canonical['status']=='PASS',canonical['errors'])
    ck('Accounting remains 93/235 32/81 39.57',p['earned_weight']==93 and p['total_weight']==235 and p['qualified_tasks']==32 and p['total_tasks']==81 and p['percent']=='39.57' and state['scope_version']=='1.0.0')
    ck('Other 80 tasks exact',[t for t in state['tasks'] if t['id']!='SC3-BRANDENBURG']==[t for t in previous['tasks'] if t['id']!='SC3-BRANDENBURG'])
    ck('Historical events prefix exact',state['events'][:len(previous['events'])]==previous['events'])
    ck('Historical progress text prefix exact',(CANON/'PROGRESS_HISTORY.md').read_bytes().decode('utf-8').startswith(texts['PROGRESS_HISTORY.md']))
    ck('No human receipt created',not any('RECEIPT' in p.name.upper() or 'ATTESTATION' in p.name.upper() for p in OUT.rglob('*') if p.is_file()))
    ck('New sublots pending runtime',all(l['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and l['attestation'] is None for t in state['tasks'] if t['id']=='SC3-BRANDENBURG' for l in t['installed_sub_lots']))
    ck('Polish frontier remains next and unstarted',state['release_focus']['next_requested_pass']=='PRUSSIA_POLISH_FRONTIER' and state['release_focus']['next_pass_started'] is False)
    ck('Bavaria not started',state['release_focus']['bavaria_started'] is False)
    ck('Diff whitespace check clean',diff.returncode==0,dict(returncode=diff.returncode,raw='DIFF_CHECK_RAW.txt'))
    ck('Required delivery documents exist',all((OUT/n).exists() for n in ['REPORT.md','SOURCES.md','PLAYER_TEST_PROTOCOL.md','VALIDATION.json','TEST_RESULTS.json','REGISTRY_MIGRATION.json','GEOMETRY.json']))
    failed=[r for r in checks if not r['passed']]
    dump('CONCURRENT_CHANGES.json',dict(runtime_files_captured=len(b['runtime']),protected_runtime_drift=drift,previous_delivery_files=len(b['previous_delivery']),previous_proof_drift=prior_drift,preexisting_dirty_status=b['git']['status'],new_functional_files=[r for r in changes if r['file'] in now],policy='No restore, no Git writes, no vanilla writes, no cross-checkout synchronization'))
    dump('FINAL_CHECKS.json',dict(status='FAIL' if failed else 'PASS',passed=len(checks)-len(failed),total=len(checks),failed=failed,checks=checks,progress_before=b['progress'],progress_after=p,engine_test=False,human_receipts_added=0))
    modified=changes+[dict(file='tools/serg_north_saxony1.py',before=None,after=sha(ROOT/'tools/serg_north_saxony1.py'),kind='new scoped delivery tool')]
    for name in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']:modified.append(dict(file=(CANON/name).relative_to(ROOT).as_posix(),after=sha(CANON/name),kind='canonical tracking update'))
    dump('FILES_MODIFIED.json',dict(installed_files=changes,tracking_and_tool=modified[len(changes):],new_evidence_directory=OUT.relative_to(ROOT).as_posix(),new_evidence=[dict(file=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in OUT.rglob('*') if p.is_file() and p.name!='FILES_MODIFIED.json']))
    print('Final checks',len(checks)-len(failed),'/',len(checks),'; diff',diff.returncode);assert not failed,failed

if __name__=='__main__':globals()[sys.argv[1]]()
