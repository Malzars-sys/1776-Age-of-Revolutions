"""R8: install the player's approved B approximation; audit, never edit Thorn.

Commands are explicit stages. Earlier report generators are never called.
Population allocation reuses MAP-2L's largest-remainder method through R3.
"""
import collections as C
import csv
import difflib
import json
import math
import re
import shutil
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2m_r3 as prior

core=prior.r2.core
economy=prior.economy
ROOT=prior.ROOT
OUT=ROOT/'docs/reports/map/MAP2M/R8'
R7=OUT.parent/'R7'

def dump(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))

def csvout(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'BASELINE.json').exists(),'Never overwrite a captured baseline'
    hashes=economy.runtime_hashes()
    assert hashes==json.loads((R7/'BASELINE.json').read_text())['runtime_hashes'],'Changed workspace: inspect, never restore'
    inv=core.qa.inventory()
    previous={p.relative_to(ROOT).as_posix():core.sha(p) for n in range(1,8) for p in (OUT.parent/f'R{n}').rglob('*') if p.is_file()}
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    dump('BASELINE.json',dict(inventory=inv,hashes=hashes,earlier_proofs=previous,
        bitmap_backup=(OUT/'provinces_before.png').relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),
        registry=json.loads(core.active_registry_path().read_text()),git_head=prior.r2.head(),git_index_sha256=core.sha(ROOT/'.git/index')))
    print('Captured immutable R8 baseline:',len(hashes),'runtime files;',len(previous),'prior evidence files')

def prepare():
    b=load('BASELINE.json');assert economy.runtime_hashes()==b['hashes']
    bmp=core.packed(ROOT/'map_data/provinces.png')
    proposal=[r for r in readcsv(R7/'PEENE_PROPOSED_CELLS.csv') if r['Variant']=='B']
    cells={(int(r['X']),int(r['Y'])) for r in proposal}
    assert len(proposal)==len(cells)==41
    small={(int(r['X']),int(r['Y'])) for r in readcsv(R7/'PEENE_PROPOSED_CELLS.csv') if r['Variant']=='A'}
    assert len(small)==3 and small<=cells
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    assert owners['xE1A03A']==['STATE_POMERANIA','PRU'] and owners['x567452']==['STATE_POMERANIA','SWE']
    assert int((bmp==0x567452).sum())==357
    sys.path.insert(0,str(R7));import arbitration as seven
    physical,water,river,_=seven.p.physical_masks()
    assert np.array_equal(physical,bmp)
    existing={(x,y) for y in range(728,744) for x in range(4398,4418) if bmp[y,x]==0x567452}
    assert seven.connected_to_existing(cells,existing)==cells
    changes=[]
    for r in proposal:
        x,y=int(r['X']),int(r['Y'])
        assert 4404<=x<4412 and 732<=y<740 and int(bmp[y,x])==0xE1A03A and not water[y,x]
        assert x+1<=float(r['Drawing_bank_X_min']) and r['Inside_frozen_R5_support']=='True'
        changes.append(dict(Sector='PEENE',X=x,Y=y,State_ID='STATE_POMERANIA',RGB_before='xE1A03A',RGB_after='x567452',
            Owner_before='PRU',Owner_after='SWE',Decision='B_APPROVED_APPROXIMATION',Applied=True,
            Basis=r['Historical_basis'],Right_edge_setback_min_px=r['Right_edge_setback_min_px'],Historical_bank_certified=False))
    assert (4410,735) not in cells
    after=prior.r2.expected_raster(bmp,changes)
    assert len(core.components(after==0x567452))==1 and len(core.components(after==0xE1A03A))==1
    area=sum(int((bmp==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_POMERANIA','PRU'])
    weights={'PRU':area-41,'SWE':41};allocations=[];files={};originals={}
    for path in economy.effective(ROOT,core.qa.GAME,'common/history/pops'):
        raw=path.read_text(encoding='utf-8-sig')
        try:region=core.region(raw,'STATE_POMERANIA','PRU')
        except StopIteration:continue
        edits=[];moved=[]
        for pop in region.children('create_pop'):
            size=pop.children('size')[0];counts=core.allocate(int(size.value),weights)
            edits.append((size.start,size.end,'size = '+str(counts['PRU'])))
            if counts['SWE']:
                moved.append(core.edits(raw[pop.start:pop.end],[(size.start-pop.start,size.end-pop.start,'size = '+str(counts['SWE']))]))
            allocations.append(dict(state='STATE_POMERANIA',source='PRU',target='SWE',culture=core.cw.scalar(pop.one('culture')),
                religion=core.cw.scalar(pop.one('religion','DEFAULT')),before=int(size.value),after=counts))
        updated=core.edits(raw,edits)
        for fragment in moved:updated=core.append(updated,'STATE_POMERANIA','SWE',fragment)
        a=raw.splitlines(True);z=updated.splitlines(True)
        for kind,a0,a1,z0,z1 in difflib.SequenceMatcher(a=a,b=z,autojunk=False).get_opcodes():
            if kind in ['insert','replace']:
                for i in range(z0,z1):
                    if not z[i].strip():z[i]='\n'
        updated=''.join(z);core.cw.parse(updated)
        assert path.is_relative_to(ROOT)
        rel=path.relative_to(ROOT).as_posix();originals[rel]=raw;files[rel]=updated
    assert allocations and len(files)==1
    buildings=[]
    for sid,tag,node,path in economy.declarations():
        if (sid,tag)!=('STATE_POMERANIA','PRU'):continue
        for child in core.cw.walk(node.children()):
            if child.key=='levels':
                split=core.allocate(int(child.value),weights)
                assert split['SWE']==0,'Nonzero building transfer requires additional explicit review'
                buildings.append(dict(building=node.one('building'),levels=int(child.value),allocation=split,path=path.relative_to(ROOT).as_posix()))
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('PLAN.json',dict(changes=changes,allocations=allocations,weights=weights,source_area=area,building_review=buildings,
        files=sorted(files),new_provinces=[],netze_applied_cells=0,candidate_sha256=core.sha(OUT/'provinces_candidate.png')))
    dump('ORIGINAL_TEXT.json',originals);dump('EXPECTED_TEXT.json',files)
    csvout('PEENE_TERRITORIAL_CHANGES.csv',changes)
    old=core.OUT
    try:core.OUT=OUT;core.emit(files,'HISTORY.patch')
    finally:core.OUT=old
    print('Preflight PASS: 41 mainland cells; both provinces connected; Wolgast point excluded')
    print('PRU source area',area,'weights',weights,'population PRU -> SWE',sum(r['after']['SWE'] for r in allocations))
    print('Building level redistribution: zero; prepared',list(files))

def install():
    b=load('BASELINE.json');plan=load('PLAN.json')
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert core.sha(OUT/'provinces_candidate.png')==plan['candidate_sha256']
    for rel,text in load('EXPECTED_TEXT.json').items():assert (ROOT/rel).read_text(encoding='utf-8-sig')==text,'Apply reviewed HISTORY.patch first'
    hashes=economy.runtime_hashes()
    assert {p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}==set(plan['files'])
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Installed exact approved B raster:',plan['candidate_sha256'])

def profiles(raw):
    out=C.Counter()
    for s in core.cw.walk(core.cw.parse(raw)):
        if s.key.startswith('s:STATE_'):
            for rs in s.children():
                for p in rs.children('create_pop'):
                    attributes=[core.qa.norm(n) for n in p.children() if n.key!='size']
                    out[s.key,json.dumps(attributes,sort_keys=True)]+=int(p.one('size'))
    return out

def validate():
    b=load('BASELINE.json');plan=load('PLAN.json');inv=core.qa.inventory();checks=[]
    before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    def check(name,ok,detail=''):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    check('Exact 41 approved B pixels, no outside delta',np.array_equal(after,prior.r2.expected_raster(before,plan['changes'])) and int((before!=after).sum())==41)
    proposal=[r for r in readcsv(R7/'PEENE_PROPOSED_CELLS.csv') if r['Variant']=='B']
    cells={(r['X'],r['Y']) for r in plan['changes']}
    check('Exact accepted R7 B list, not A+B',len(proposal)==41 and cells=={(int(r['X']),int(r['Y'])) for r in proposal})
    check('All41 cells were PRU xE1A03A before installation',all(int(before[y,x])==0xE1A03A for x,y in cells))
    check('Every full cell west of all frozen drawing banks',all(int(r['X'])+1<=float(r['Drawing_bank_X_min']) for r in proposal))
    check('All41 in R5 support and rows below740',all(r['Inside_frozen_R5_support']=='True' and int(r['Y'])<740 for r in proposal))
    sys.path.insert(0,str(R7));import arbitration as seven
    _,water,_,_=seven.p.physical_masks()
    check('No sea or lake pixel transferred',not any(water[y,x] for x,y in cells))
    existing={(x,y) for y in range(728,744) for x in range(4398,4418) if before[y,x]==0x567452}
    check('All new components touch previously Swedish mainland',seven.connected_to_existing(cells,existing)==cells)
    for label,rows in [('R2',prior.r2.load('PLAN.json')['changes']),('R3',prior.load('PLAN.json')['changes'])]:
        check('Accepted exact pixel replay '+label,all(after[r['Y'],r['X']]==int(r['RGB_after'][1:],16) for r in rows))
    check('Installed raster hash',core.sha(ROOT/'map_data/provinces.png')==plan['candidate_sha256'])
    with Image.open(ROOT/'map_data/provinces.png') as im:check('RGB 8192x3616 bitmap valid',im.mode=='RGB' and im.size==(8192,3616))
    check('357 accepted Swedish cells preserved and 398 installed',int((before==0x567452).sum())==357 and int((after==0x567452).sum())==398 and np.all(after[before==0x567452]==0x567452))
    check('Prussian source 333 -> 292 pixels',int((before==0xE1A03A).sum())==333 and int((after==0xE1A03A).sum())==292)
    check('No RGB created or removed',np.array_equal(np.unique(before),np.unique(after)))
    for rgb in ['xEDB010','xFCC7B7','xA04121','x41A021','x80A0A0','x999CEE']:
        v=int(rgb[1:],16);check('Frozen footprint '+rgb,np.array_equal(before==v,after==v))
    check('Bromberg85 / Polish residual142',int((after==0xEDB010).sum())==85 and int((after==0xFCC7B7).sum())==142)
    check('All rows740+ untouched including Demmin/Anklam',np.array_equal(before[740:],after[740:]))
    check('Wolgast provisional point not transferred',after[735,4410]==before[735,4410]==0xE1A03A)
    check('Usedom/Wollin east of selected mainland window unchanged',np.array_equal(before[710:790,4412:4455],after[710:790,4412:4455]))
    for value in [0x567452,0xE1A03A]:check('Four-connected province '+hex(value),len(core.components(after==value))==1)
    for rgb,owner in [('xE1A03A','PRU'),('x567452','SWE')]:
        refs=[r for r in inv['owners'] if r['key'][0]==rgb]
        check('Single correct State/owner '+rgb,len(refs)==1 and refs[0]['count']==1 and refs[0]['key'][1:]==['STATE_POMERANIA',owner] and inv['geometry'][rgb]=='STATE_POMERANIA')
    for field in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:
        check('Preserved cumulative inventory '+field,inv[field]==b['inventory'][field])
    check('Exact world population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for row in plan['allocations']:
        religion='DEFAULT:'+row['culture'] if row['religion']=='DEFAULT' else row['religion'];n=row['after']['SWE']
        regional[(row['state'],'PRU',row['culture'],religion)]-=n;regional[(row['state'],'SWE',row['culture'],religion)]+=n
    check('Exact regional deterministic demographic deltas',+regional==core.qa.counter(inv['regional_pop']))
    for rel,text in load('EXPECTED_TEXT.json').items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig')
        check('Reviewed and parsed text '+rel,actual==text and bool(core.cw.parse(actual)))
        check('All pop attributes/types and state totals '+rel,profiles(actual)==profiles(load('ORIGINAL_TEXT.json')[rel]))
    hashes=economy.runtime_hashes();changed={p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}
    check('Only bitmap and reviewed population file changed',changed==set(plan['files'])|{'map_data/provinces.png'})
    check('Imperial registry unchanged',json.loads(core.active_registry_path().read_text())==b['registry'])
    check('R1-R7 artifacts immutable',all((ROOT/p).is_file() and core.sha(ROOT/p)==h for p,h in b['earlier_proofs'].items()))
    check('Inherited44 duplicate RGB and12 invalid refs unchanged',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    totals=economy.totals(economy.declarations())
    for sid,tag,kind,n in [('STATE_BRANDENBURG','PRU','building_arms_industry',6),('STATE_RHONE','FRA','building_arms_industry',5),('STATE_GUANGDONG','CHI','building_trade_center',10),('STATE_GUANGDONG','CHI','building_port',5)]:
        check('Accepted economy '+sid+' '+kind,totals[sid,tag,kind]==n)
    check('No Chinese trade centre outside Canton',not any(sid!='STATE_GUANGDONG' and tag=='CHI' and kind=='building_trade_center' and n for (sid,tag,kind),n in totals.items()))
    check('HEAD unchanged',prior.r2.head()==b['git_head'])
    check('Index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    if (OUT/'THORN_INVENTORY.json').exists():
        thorn=load('THORN_INVENTORY.json');candidate=readcsv(OUT/'THORN_PROPOSED_CORRECTION.csv')
        check('Thorn audit exact153 pixels and single native locator',thorn['pixels']==153 and len(thorn['locators'])==1 and thorn['applied_cells']==0)
        check('Thorn proposal153 uniquely enumerated cells, all unapplied',len(candidate)==153 and len({(r['X'],r['Y']) for r in candidate})==153 and all(r['Applied']=='False' and r['Approval']=='NOT_APPROVED' and after[int(r['Y']),int(r['X'])]==0x41A021 for r in candidate))
    a=core.qa.counter(b['inventory']['regional_pop']);z=core.qa.counter(inv['regional_pop']);rows=[]
    for key in sorted(a.keys()|z.keys()):
        if key[0] in ['STATE_POMERANIA','STATE_WEST_PRUSSIA','STATE_POSEN']:
            rows.append(dict(State_ID=key[0],Owner=key[1],Culture=key[2],Religion=key[3],Before=a[key],After=z[key],Difference=z[key]-a[key]))
    csvout('POPULATION_VALIDATION.csv',rows)
    for sid in ['STATE_POMERANIA','STATE_WEST_PRUSSIA','STATE_POSEN']:
        check('Population conserved '+sid,sum(r['Before'] for r in rows if r['State_ID']==sid)==sum(r['After'] for r in rows if r['State_ID']==sid))
    result=dict(status='MAP-2M-R8_READY_FOR_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'MAP-2M-R8_PARTIAL',
        static_validation='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
        applied_peene_cells=41,decision_category='B_APPROVED_APPROXIMATION',new_RGBs=[],netze_applied_cells=0,thorn_applied_cells=0,
        world_population=835804980,population_transferred_pru_swe=sum(r['after']['SWE'] for r in plan['allocations']),functional_files=sorted(changed),
        inherited_duplicates=44,inherited_invalid_references=12,engine_tested=False,runtime_status='PENDING_USER_NEW_GAME_AND_ONE_MONTH',historical_boundary_complete=False,
        search_metrics=dict(colgrep_calls=0,reason='Known R2/R3/R7 implementation paths reused; exact identifier searches only',codex_task_tokens=None,quota_savings='Not measurable'))
    dump('VALIDATION.json',result)
    print(result['status'],result['static_validation'],result['passed'],'/',result['total'])
    for c in checks:
        if not c['passed']:print('FAIL',c['name'],c['detail'])
    assert result['static_validation']=='PASS'

def font(n=17):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)

def panel(bmp,box,title,owners,selected=(),scale=14):
    from PIL import ImageColor
    x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),225,dtype=np.uint8)
    colors={'PRU':'#87b4dd','SWE':'#ebcb56','PLC':'#e5a6a6'}
    for rgb in np.unique(local):
        refs=owners.get('x'+format(int(rgb),'06X'),[])
        if refs:arr[local==rgb]=ImageColor.getrgb(colors.get(refs[-1],'#a5b2a0'))
    im=Image.fromarray(arr).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST)
    d=ImageDraw.Draw(im)
    for y in range(y0,y1):
        for x in range(x0,x1):
            px,py=(x-x0)*scale,(y-y0)*scale
            if x>x0 and bmp[y,x]!=bmp[y,x-1]:d.line((px,py,px,py+scale),fill='#555555')
            if y>y0 and bmp[y,x]!=bmp[y-1,x]:d.line((px,py,px+scale,py),fill='#555555')
            if (x,y) in selected:d.rectangle((px+1,py+1,px+scale-2,py+scale-2),outline='#ed651a',width=2)
    for x in range((x0//5+1)*5,x1,5):
        px=(x-x0)*scale;d.line((px,0,px,im.height),fill='#7e8890',width=1);d.text((px+2,2),str(x),font=font(12),fill='black')
    for y in range((y0//5+1)*5,y1,5):
        py=(y-y0)*scale;d.line((0,py,im.width,py),fill='#7e8890',width=1);d.text((2,py+2),str(y),font=font(12),fill='black')
    out=Image.new('RGB',(im.width,im.height+42),'white');out.paste(im,(0,42));ImageDraw.Draw(out).text((8,8),title,font=font(),fill='black')
    return out

def previews():
    b=load('BASELINE.json');plan=load('PLAN.json');before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};cells={(v['X'],v['Y']) for v in plan['changes']}
    box=(4388,721,4432,756);panels=[]
    for bmp,title in [(before,'AVANT : x567452 = 357 cellules'),(after,'INSTALLE : 398 cellules, +41 PRU -> SWE')]:
        im=panel(bmp,box,title,owners,cells,16);d=ImageDraw.Draw(im)
        px=(4410.5-box[0])*16;py=(735.5-box[1])*16+42
        d.ellipse((px-5,py-5,px+5,py+5),outline='#bd1875',width=3)
        d.text((px+8,py-21),'Wolgast provisoire\nreste PRU',font=font(13),fill='#84265f',stroke_width=1,stroke_fill='white')
        panels.append(im)
    out=Image.new('RGB',(panels[0].width*2,panels[0].height+65),'white')
    for i,im in enumerate(panels):out.paste(im,(i*im.width,0))
    d=ImageDraw.Draw(out);d.text((8,out.height-58),'SWE jaune | PRU bleu | orange : les 41 cellules exactes. Grille = pixels natifs, origine en haut a gauche.',font=font(),fill='black')
    d.text((8,out.height-30),'Generalisation politique B approuvee ; ni rive historique exacte ni correction complete de Wolgast/Peendamm.',font=font(),fill='black')
    out.save(OUT/'PEENE_BEFORE_AFTER.png')

def thorn():
    """Read-only audit and a conditional minimum technical scenario, not approval."""
    b=load('BASELINE.json');bmp=core.packed(ROOT/'map_data/provinces.png');inv=b['inventory']
    ys,xs=np.where(bmp==0x41A021);cells=set(zip(xs.tolist(),ys.tolist()))
    neighbors=C.Counter()
    for x,y in cells:
        for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if (nx,ny) not in cells:neighbors['x'+format(int(bmp[ny,nx]),'06X')]+=1
    owner_refs=C.defaultdict(list)
    for row in inv['owners']:owner_refs[row['key'][0]].append(dict(State_ID=row['key'][1],Owner=row['key'][2],References=row['count']))
    adjacency=[dict(RGB=rgb,Shared_pixel_edges=n,Owners=owner_refs[rgb],State_ID=inv['geometry'].get(rgb)) for rgb,n in sorted(neighbors.items())]
    # Native locator positions are technical associations, not certified towns.
    folder='gfx/map/map_object_data'
    paths={q.name:q for q in (core.qa.GAME/folder).glob('generated_map_object_locators_*.txt')}
    paths.update({q.name:q for q in (ROOT/folder).glob('generated_map_object_locators_*.txt')})
    locators=[]
    for path in paths.values():
        raw=path.read_text(encoding='utf-8-sig')
        for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\}',raw):
            ident=int(m[1]);x=float(m[2]);y=bmp.shape[0]-float(m[4]);cx,cy=math.floor(x),math.floor(y)
            if (cx,cy) not in cells:continue
            locators.append(dict(Kind=path.stem.removeprefix('generated_map_object_locators_'),ID=ident,X=x,Y=y,Cell_X=cx,Cell_Y=cy,
                File=path.as_posix(),Line=raw.count('\n',0,m.start())+1,Certified_city_position=False))
    farms=[r for r in locators if r['Kind']=='farm' and r['ID']==158]
    assert len(farms)==1
    candidate=(farms[0]['Cell_X'],farms[0]['Cell_Y'])
    sys.path.insert(0,str(R7));import arbitration as seven
    model=seven.w.load('TRANSFORMATIONS.json')['selected_native'];points=np.c_[xs+.5,ys+.5]
    geo=seven.r.inverse(model,points)
    # Approximate spherical cell area from frozen model; not historical acreage.
    corners=np.array([[float(xs.mean()),float(ys.mean())],[float(xs.mean()+1),float(ys.mean())],[float(xs.mean()),float(ys.mean()+1)]])
    g=seven.r.inverse(model,corners);basis=g[1:]-g[0]
    km2=abs(float(np.linalg.det(basis)))*(math.pi*6371.0088/180)**2*math.cos(math.radians(float(g[0,1])))
    poprows=[r for r in inv['regional_pop'] if r['key'][0]=='STATE_WEST_PRUSSIA']
    buildings=[]
    for sid,tag,node,path in economy.declarations():
        if sid=='STATE_WEST_PRUSSIA':
            buildings.append(dict(State_ID=sid,Owner=tag,Building=core.cw.scalar(node.one('building')),Levels=economy.levels(node),
                PMs=core.values(node,'activate_production_methods'),Signature=core.qa.signature(node),File=path.as_posix()))
    units=[r for r in inv['units'] if r['key'][2]=='STATE_WEST_PRUSSIA']
    plan=[]
    for x,y in sorted(cells,key=lambda c:(c[1],c[0])):
        chosen=(x,y)==candidate
        plan.append(dict(X=x,Y=y,RGB_before='x41A021',State_ID='STATE_WEST_PRUSSIA',Owner_before='PRU',
            Owner_in_minimal_technical_scenario='PLC' if chosen else 'PRU',
            RGB_in_scenario='NEW_RGB_TO_RESERVE_LATER' if chosen else 'x41A021',
            Status='CONDITIONAL_NATIVE_HUB_CELL_NOT_HISTORICALLY_VALIDATED' if chosen else 'RETAIN_PENDING_HISTORICAL_BOUNDARY',
            Evidence='Native farm locator named Torun; not an independent city control' if chosen else 'No demonstrated Jan1776 Polish polygon for this cell',
            Approval='NOT_APPROVED',Applied=False))
    csvout('THORN_PROPOSED_CORRECTION.csv',plan)
    csvout('THORN_LOCATORS.csv',locators)
    data=dict(RGB='x41A021',pixels=len(cells),bbox_inclusive=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
        four_connected_component_sizes=list(map(len,core.components(bmp==0x41A021))),owners=owner_refs['x41A021'],State_ID='STATE_WEST_PRUSSIA',numeric_state_id=158,
        approximate_area_km2=km2*len(cells),approximate_cell_area_km2=km2,
        diagnostic_geo_bbox=[geo.min(axis=0).tolist(),geo.max(axis=0).tolist()],area_certified=False,
        adjacency=adjacency,locators=locators,regional_population=poprows,regional_building_declarations=buildings,regional_units=units,
        population_is_not_province_resolved=True,conditional_single_cell=list(candidate),minimal_scenario_is_not_approved=True,
        existing_terrain='tundra (inherited, not changed)',future_files=['map_data/provinces.png','map_data/state_regions/02_east_europe.txt',
            'map_data/province_terrains.txt','common/history/states/00_states.txt','common/history/pops/02_east_europe.txt',
            'common/history/buildings/<only if a justified nonzero allocation requires it>'],applied_cells=0)
    dump('THORN_INVENTORY.json',data)
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']};box=(4496,749,4540,788);panels=[]
    for title,selected in [('ACTUEL : 153 cellules PRU, aucune modifiee',cells),('SCENARIO MINIMAL NON APPLIQUE : 1 cellule a confirmer',{candidate})]:
        im=panel(bmp,box,title,owners,selected,18);d=ImageDraw.Draw(im)
        if len(selected)==1:
            x,y=candidate;px=(x-box[0])*18;py=(y-box[1])*18+42
            d.rectangle((px+2,py+2,px+15,py+15),fill='#ed9c9c',outline='#d66014',width=2)
        for v in locators:
            px=(v['X']-box[0])*18;py=(v['Y']-box[1])*18+42
            d.ellipse((px-4,py-4,px+4,py+4),fill='#a5108a')
            d.text((px+8,py),v['Kind']+' '+str(v['ID']),font=font(14),fill='#8a106d',stroke_width=1,stroke_fill='white')
        panels.append(im)
    out=Image.new('RGB',(panels[0].width*2,panels[0].height+100),'white')
    for i,im in enumerate(panels):out.paste(im,(im.width*i,0))
    d=ImageDraw.Draw(out)
    for i,line in enumerate(['Orange gauche : empreinte complete x41A021. PRU bleu / PLC rose / autres gris.',
        'Droite : minimum technique au hub natif (4519,772), PAS une localisation historique validee ni une frontiere approuvee.',
        'Ne pas transferer les 153 cellules en bloc. Confirmer le noyau urbain et les possessions de 1776 avant tout nouveau dessin.']):
        d.text((10,panels[0].height+8+i*28),line,font=font(),fill='black')
    out.save(OUT/'THORN_BEFORE_PROPOSAL.png')
    # Existing sources, cropped without fitting or altering the originals.
    for name,box2 in [('GUESSEFELD_1775',(1450,2200,1950,2650)),('PFAU_45',(750,700,1450,1200))]:
        path=OUT.parent/'EVIDENCE'/f'{name}.jpg' if name.startswith('GUESSE') else OUT.parent/'R4/EVIDENCE'/f'{name}.jpg'
        Image.open(path).crop(box2).save(OUT/f'THORN_SOURCE_{name}.png')
    print('Thorn audit:',len(cells),'pixels;',round(data['approximate_area_km2'],1),'km2 diagnostic;',len(locators),'locators')
    print('Adjacent',adjacency)
    print('Population by state-owner',poprows)
    print('Technical minimum only:',candidate,'not geographically approved; actual transfers ZERO')

def finalize():
    required=['REPORT.md','PEENE_INSTALLATION.md','PEENE_TERRITORIAL_CHANGES.csv','PEENE_BEFORE_AFTER.png',
        'POPULATION_VALIDATION.csv','VALIDATION.json','THORN_AUDIT.md','THORN_PROPOSED_CORRECTION.csv','THORN_BEFORE_PROPOSAL.png','UNRESOLVED.csv','NEXT_STEPS.md']
    assert all((OUT/name).is_file() and (OUT/name).stat().st_size for name in required)
    result=load('VALIDATION.json');assert result['static_validation']=='PASS' and result['passed']==result['total']==60
    # Results of the already executed unittest commands, recorded without rerunning
    # historical generators or rewriting their proof folders.
    result['unit_tests']=dict(passed=26,total=26,engine_tests=False,suites=[
        dict(command='python -m unittest discover -s tools -p test_map2m_r8.py -v',passed=8,total=8,recorded_run_seconds=2.510),
        dict(command='python -m unittest discover -s tools -p test_map2l_registry.py -v',passed=18,total=18,recorded_run_seconds=.081)])
    result['artifacts_complete']=required
    dump('VALIDATION.json',result)
    b=load('BASELINE.json');hashes=economy.runtime_hashes()
    assert {p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}==set(result['functional_files'])
    assert all(core.sha(ROOT/p)==h for p,h in b['earlier_proofs'].items())
    assert prior.r2.head()==b['git_head'] and core.sha(ROOT/'.git/index')==b['git_index_sha256']
    for name in ['PEENE_BEFORE_AFTER.png','THORN_BEFORE_PROPOSAL.png']:
        with Image.open(OUT/name) as im:im.verify()
    protected={p.relative_to(ROOT).as_posix():core.sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    for rel in ['tools/map2m_r8.py','tools/test_map2m_r8.py']:protected[rel]=core.sha(ROOT/rel)
    dump('MANIFEST.json',dict(algorithm='SHA256',files=protected,installed_runtime={p:hashes[p] for p in result['functional_files']},
        previous_evidence_files=len(b['earlier_proofs']),HEAD=b['git_head'],git_index_sha256=b['git_index_sha256']))
    print('All eleven required deliverables present; PNGs verified; R1-R7 and HEAD/index still unchanged.')

if __name__=='__main__':globals()[sys.argv[1]]()
