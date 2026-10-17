"""Guarded MAP-2Q-R3 continuation; never rewrites previous baselines."""
import sys, json, subprocess
from pathlib import Path
import map2q_eutin as q
import map2q_continue as previous
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor

ROOT=q.ROOT
OUT=q.OUT/'R3'
SID=q.REGION
POP='common/history/pops/00_west_europe.txt'
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'BASELINE.json').exists()
    m=q.load('INSTALLED_MANIFEST.json')
    assert all(q.core.sha(ROOT/p)==h for p,h in m['functional_files'].items())
    inv=q.core.qa.inventory()
    assert sum(r['count'] for r in inv['pops'])==835801255
    raw=(ROOT/POP).read_text(encoding='utf-8-sig')
    pops=q.core.region(raw,SID,'HLB').children('create_pop')
    assert [int(p.one('size')) for p in pops]==[2298,12,49,123,4997,121]
    originals={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in [POP,
        'common/history/states/00_states.txt','map_data/state_regions/00_west_europe.txt','map_data/province_terrains.txt']}
    dump('BASELINE.json',dict(inventory=inv,hashes=q.economy.runtime_hashes(),originals=originals,
        registry=json.loads(q.core.active_registry_path().read_text(encoding='utf8')),
        bitmap_backup='docs/reports/map/MAP2Q/provinces_candidate.png',
        bitmap_sha256=q.core.sha(ROOT/'map_data/provinces.png'),
        eutin_pop_blocks=[raw[p.start:p.end] for p in pops],
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_index_sha256=q.core.sha(ROOT/'.git/index'),
        prior_artifacts={p.relative_to(ROOT).as_posix():q.core.sha(p) for p in (ROOT/'docs/reports/map').rglob('*') if p.is_file() and OUT not in p.parents},
        independent_hashes={p.relative_to(ROOT).as_posix():q.core.sha(p) for folder in ['docs/prototypes/REGIONAL_INFRASTRUCTURE/mod','tools/vic3-diagnostic-bridge'] for p in (ROOT/folder).rglob('*') if p.is_file()}))
    assert q.core.sha(ROOT/'map_data/provinces.png')==q.core.sha(q.OUT/'provinces_candidate.png')
    print('R3 baseline frozen. World 835801255; six accepted Eutin blocks intact.')
def fetch():
    previous.OUT=OUT;previous.fetch()
def inspect():
    b=load('BASELINE.json');bmp=q.core.packed(ROOT/b['bitmap_backup'])
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    box=(4330,733,4354,752);x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1]
    pal={'HOL':'#98bd98','LUB':'#ba9bd2','HLB':'#eea16c','MEC':'#b4c8db','SCH':'#e5cc7f'}
    arr=np.full((*local.shape,3),(143,186,214),dtype=np.uint8)
    for c in np.unique(local):
        tag=owners.get('x'+format(int(c),'06X'),['',''])[1]
        if tag:arr[local==c]=ImageColor.getrgb(pal.get(tag,'#aaa'))
    im=Image.fromarray(arr).resize(((x1-x0)*40,(y1-y0)*40),Image.Resampling.NEAREST)
    d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for x in range(x0,x1):
        for y in range(y0,y1):
            d.rectangle(((x-x0)*40,(y-y0)*40,(x-x0+1)*40,(y-y0+1)*40),outline='#888')
            d.text(((x-x0)*40+2,(y-y0)*40+2),str(x)[-2:]+','+str(y)[-2:],font=f,fill='black')
    im.save(OUT/'CURRENT_CELL_GRID.png')
    print('Local RGBs',[(hex(int(c)),owners.get('x'+format(int(c),'06X'))) for c in np.unique(local)])
    print('Locators',[r for r in q.r9.locators(bmp) if x0<=r['X']<x1 and y0<=r['Y']<y1])
    print('Region populations',[r for r in b['inventory']['regional_pop'] if r['key'][0]==SID])
def source_crops():
    for name,path,box in [('LAS',OUT/'EVIDENCE/LAS_402_A36_183_1819.jpg',(420,920,730,1130)),
                          ('REILLY',q.OUT/'EVIDENCE/REILLY_WAGRIEN_300.jpg',(580,715,830,925))]:
        im=Image.open(path).convert('RGB').crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3))
        d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
        for x in range((box[0]//20+1)*20,box[2],20):
            p=(x-box[0])*3;d.line((p,0,p,im.height),fill='#5555cc');d.text((p+2,0),str(x),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//20+1)*20,box[3],20):
            p=(y-box[1])*3;d.line((0,p,im.width,p),fill='#5555cc');d.text((0,p+2),str(y),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        im.save(OUT/(name+'_LOCAL_READING.png'))
def kohli_pages():
    import shutil
    src=q.OUT/'CONTINUATION_R1/EVIDENCE/KOHLI_MANIFEST.json'
    dest=OUT/'EVIDENCE/KOHLI_MANIFEST.json'
    if not dest.exists():shutil.copyfile(src,dest)
    previous.OUT=OUT;previous.kohli_pages()
def alignment():
    # Same geographic diagnostic and measured Kiel technical anchor as Q.
    # This is not an independently surveyed native projection.
    def target(lon,lat):
        return np.array([4325.842285+23.057991056249843*(lon-10.13489),
                         726.857910-30.99674943247102*(lat-54.32133)])
    controls=[('Eutin',[461,600],[10.61148,54.13503]),
              ('Ploen',[180,563],[10.42765,54.16202]),
              ('Neustadt',[709,658],[10.81450,54.10707]),
              ('Luebeck',[535,1204],[10.68729,53.86893]),
              ('Travemuende',[784,985],[10.8768,53.9599])]
    src=np.array([[*p,1] for _,p,_ in controls]);dst=np.array([target(*ll) for _,_,ll in controls])
    mat=np.linalg.lstsq(src,dst,rcond=None)[0]
    markers=[('Schwartau',[542,1097]),('Rensefeld',[516,1091]),('Kaltenhof',[576,1088]),
             ('Ratekau',[549,1005]),('Sereetz',[586,1066]),('Offendorf',[624,1020]),
             ('Ovendorf',[658,1057]),('Ruppersdorf',[513,974])]
    rows=[dict(name=n,source=p,pixel=(np.array([*p,1])@mat).tolist()) for n,p in markers]
    dump('ALIGNMENT.json',dict(controls=controls,matrix=mat.tolist(),residuals=(np.linalg.norm(src@mat-dst,axis=1)).tolist(),
        markers=rows,warning='Diagnostic source fit only; native geographic accuracy not independently certified. B interior envelopes, not cadastral limits. No arbitrary translation.'))
    print('Markers',rows)
    print('Fit residuals',np.linalg.norm(src@mat-dst,axis=1).tolist())
def geometry():
    b=load('BASELINE.json');a=load('ALIGNMENT.json');mat=np.array(a['matrix'])
    before=q.core.packed(ROOT/b['bitmap_backup'])
    assert q.core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    # Interior game-scale envelopes, not the whole post-1803 red territory.
    zones=[dict(name='Schwartau-Rensefeld-Kaltenhof',category='B',points=[[498,1074],[520,1065],[538,1070],[555,1075],[580,1062],[598,1074],[598,1093],[574,1110],[544,1111],[523,1106],[509,1119],[492,1118],[490,1098]]),
           dict(name='Ratekau-Ruppersdorf',category='B',points=[[490,947],[525,947],[535,980],[573,984],[577,1020],[557,1037],[525,1035],[516,990],[492,987]]),
           dict(name='Offendorf-Ovendorf',category='B',points=[[605,993],[641,996],[664,1030],[674,1058],[655,1064],[632,1040],[609,1035]])]
    x0,y0,x1,y1=(4335,735,4345,742);yy,xx=np.mgrid[y0:y1,x0:x1]
    src=(np.column_stack((xx.ravel()+.5,yy.ravel()+.5))-mat[2])@np.linalg.inv(mat[:2])
    selected=np.zeros(before.shape,bool);cellzones={}
    for i,z in enumerate(zones):
        take=q.core.inside(src,z['points']).reshape(xx.shape)
        for y,x in zip(*np.where(take)):
            point=(int(x+x0),int(y+y0));selected[point[1],point[0]]=True;cellzones[str(point)]=z['name']
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    parents=sorted('x'+format(int(c),'06X') for c in np.unique(before[selected]))
    assert parents and all(owners.get(p)==[SID,'LUB'] for p in parents),parents
    after=before.copy();assignments=[];new=[];used=set(np.unique(before).tolist());counter=0xEDB204
    for parent in parents:
        native=before==int(parent[1:],16)
        for take,tag in [(native&~selected,'LUB'),(native&selected,'HLB')]:
            parts=q.core.components(take)
            biggest=max(range(len(parts)),key=lambda i:len(parts[i]))
            for i,part in enumerate(parts):
                rgb=parent
                if tag=='HLB' or i!=biggest:
                    assert counter not in used
                    rgb='x'+format(counter,'06X');used.add(counter);counter+=1;new.append(dict(rgb=rgb,parent_rgb=parent))
                cells=[[int(x),int(y)] for y,x in part]
                for x,y in cells:after[y,x]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state=SID,previous_owner='LUB',owner=tag,pixels=len(cells),cells=cells,category='B' if tag=='HLB' else 'UNCHANGED_SOVEREIGNTY'))
    for r in q.load('GEOMETRY.json')['assignments']:
        if r['owner']=='HLB':
            assert all(after[y,x]==before[y,x] for x,y in r['cells'])
    for r in q.r9.locators(before):
        x,y=int(r['X']),int(r['Y'])
        assert after[y,x]==before[y,x],r
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('TRACING.json',dict(source='EVIDENCE/LAS_402_A36_183_1819.jpg',zones=zones,source_to_bitmap_matrix=a['matrix'],imperial_owners=['LUB','HOL','HLB'],
        warning='B modest interior envelopes of documented direct Amt villages; chapter properties and Wilmsdorf excluded. No whole 1819 outline imported; no certified native city error bound.'))
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,hub_rebindings=[],candidate_sha256=q.core.sha(OUT/'provinces_candidate.png'),
        tracing_sha256=q.core.sha(OUT/'TRACING.json'),changed_pixels=int((after!=before).sum())))
    im=Image.open(OUT/'EVIDENCE/LAS_402_A36_183_1819.jpg').convert('RGB');d=ImageDraw.Draw(im)
    for z in zones:d.line([tuple(p) for p in z['points']]+[tuple(z['points'][0])],fill='blue',width=2)
    for r in assignments:
        if r['owner']!='HLB':continue
        for x,y in r['cells']:
            pts=(np.array([[x,y],[x+1,y],[x+1,y+1],[x,y+1],[x,y]])-mat[2])@np.linalg.inv(mat[:2])
            d.line([tuple(p) for p in pts],fill='#00dd00',width=2)
    im.save(OUT/'SOURCE_SELECTION.png')
    print('Transfers',[(r['rgb'],r['pixels'],r['cells']) for r in assignments if r['owner']=='HLB'])
def compiler_before():
    import map2k_imperial_system as compiler
    b=load('BASELINE.json');compiler.OUT=OUT
    compiler.qa.inventory=lambda:b['inventory']
    files=compiler.compile_system()
    results=[]
    for rel,raw in files.items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig')
        results.append(dict(file=rel,passed=actual==raw.lstrip('\ufeff')))
    dump('COMPILER_BEFORE.json',dict(results=results,passed=sum(r['passed'] for r in results),total=len(results)))
    assert all(r['passed'] for r in results),[r for r in results if not r['passed']]
    print('Pre-R3 constitutional reproduction',len(results),'/',len(results))
def prepare():
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};allocations=[]
    assert q.economy.runtime_hashes()==b['hashes']
    before=q.core.packed(ROOT/b['bitmap_backup'])
    assert load('COMPILER_BEFORE.json')['passed']==57
    rel='common/history/states/00_states.txt';raw=b['originals'][rel]
    state=q.core.state(raw,SID);ops=[]
    for tag in ['LUB','HLB']:
        n=next(n for n in state.children('create_state') if n.one('country')=='c:'+tag)
        field=n.children('owned_provinces')[0]
        rgbs=[]
        for c in q.core.values(n,'owned_provinces'):
            rgbs += [r['rgb'] for r in g['assignments'] if r['owner']==tag and r['parent_rgb']==c] if c in g['parents'] else [c]
        rgbs += [r['rgb'] for r in g['assignments'] if r['owner']==tag and r['rgb'] not in rgbs]
        ops.append((field.start,field.end,'owned_provinces = { '+' '.join(rgbs)+' }'))
    files[rel]=q.core.edits(raw,ops)
    rel='map_data/state_regions/00_west_europe.txt';raw=b['originals'][rel]
    state=next(n for n in q.core.cw.parse(raw) if n.key==SID);f=state.children('provinces')[0]
    values=q.core.values(state,'provinces')
    newvalues=[]
    for c in values:
        newvalues += [r['rgb'] for r in g['assignments'] if r['parent_rgb']==c] if c in g['parents'] else [c]
    ops=[(f.start,f.end,'provinces = { '+' '.join('"'+c+'"' for c in newvalues)+' }')]
    # Inherit any prime-land classifications without moving hub references.
    for f in state.children('prime_land'):
        old=q.core.values(state,'prime_land');new=[]
        for c in old:new += [r['rgb'] for r in g['assignments'] if r['parent_rgb']==c] if c in g['parents'] else [c]
        if old!=new:ops.append((f.start,f.end,'prime_land = { '+' '.join('"'+c+'"' for c in new)+' }'))
    files[rel]=q.core.edits(raw,ops)
    source_rgbs=[r['key'][0] for r in b['inventory']['owners'] if r['key'][1:]==[SID,'LUB']]
    total=sum(int((before==int(c[1:],16)).sum()) for c in source_rgbs)
    moved=sum(r['pixels'] for r in g['assignments'] if r['owner']=='HLB')
    counts={'LUB':total-moved,'HLB':moved}
    raw=b['originals'][POP];n=q.core.region(raw,SID,'LUB');ops=[];pieces=[]
    for p in n.children('create_pop'):
        size=p.children('size')[0];amounts=q.core.allocate(int(size.value),counts)
        ops.append((size.start,size.end,'size = '+str(amounts['LUB'])))
        if amounts['HLB']:
            piece=raw[p.start:p.end]
            pieces.append(q.core.edits(piece,[(size.start-p.start,size.end-p.start,'size = '+str(amounts['HLB']))]))
        allocations.append(dict(culture=p.one('culture'),religion=p.one('religion','DEFAULT'),before=int(size.value),after=amounts))
    raw=q.core.edits(raw,ops);files[POP]=q.core.append(raw,SID,'HLB','\n'.join(pieces))
    assert [files[POP][p.start:p.end] for p in q.core.region(files[POP],SID,'HLB').children('create_pop')[:6]]==b['eutin_pop_blocks']
    import re
    terrain=b['originals']['map_data/province_terrains.txt']
    tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    terrain+='\n'+''.join(r['rgb']+'="'+tm[r['parent_rgb'].upper()]+'"\n' for r in g['new_provinces'])
    files['map_data/province_terrains.txt']=terrain
    previous=[r for r in b['registry'] if r['state']==SID]
    updated=list(previous)+[dict(rgb=r['rgb'],state=SID,beneficiary='HLB',basis='MAP2Q R3: modest B envelope of direct Amt Kaltenhof; no post-1803 chapter annexation. See R3/HISTORICAL_EVIDENCE.md.') for r in g['assignments'] if r['owner']=='HLB']
    ledger=sorted([r for r in b['registry'] if r['state']!=SID]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    registry=q.core.active_registry_path().relative_to(ROOT).as_posix();files[registry]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    migration=dict(replaced_regions=[SID],previous=previous,updated=updated,new_members=[],free_cities=[],
        new_provinces=g['new_provinces'],geometry='MAP2Q/R3/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[])
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):q.core.cw.parse(raw)
    dump('EXPECTED_TEXT.json',files);dump('POPULATION_ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_AREA_REDISTRIBUTION_NOT_HISTORICAL_ESTIMATE',source_cells=total,moved_cells=moved,profiles=allocations))
    q.core.OUT=OUT;changes=q.core.emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,allocations=allocations,registered_RGBs=len(ledger)))
    print('Prepared',len(changes),'text files; population transferred',sum(r['after']['HLB'] for r in allocations),'from',total,'source cells; registry',len(ledger))
def install():
    import shutil
    b=load('BASELINE.json');files=load('EXPECTED_TEXT.json')
    assert q.core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    for p,raw in files.items():assert (ROOT/p).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip(),p
    assert q.core.sha(OUT/'provinces_candidate.png')==load('GEOMETRY.json')['candidate_sha256']
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Installed guarded four-cell sovereignty correction; two new RGBs.')
def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files)
    q.core.OUT=OUT;changes=q.core.emit(files,'IMPERIAL.patch');dump('IMPERIAL_FILES.json',dict(files=changes))
    print('Imperial runtime changes',len(changes))
def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
def validate():
    import re,collections as C
    from map2l_registry import apply_territorial_migrations,approved_territorial_extensions
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=q.core.qa.inventory();dump('CURRENT_INVENTORY.json',inv)
    checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=q.core.packed(ROOT/b['bitmap_backup']);after=q.core.packed(ROOT/'map_data/provinces.png')
    expected=before.copy();owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    for r in g['assignments']:
        for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
        check('Connected province '+r['rgb'],len(q.core.components(after==int(r['rgb'][1:],16)))==1)
        check('Exact owner/state '+r['rgb'],owners.get(r['rgb'])==[SID,r['owner']])
    check('Exact four-cell RGB delta; all other world pixels protected',np.array_equal(after,expected) and int((after!=before).sum())==4)
    oldowners=counter(b['inventory']['owners']);expectedowners=oldowners.copy()
    for r in b['inventory']['owners']:
        if r['key'][0] in g['parents']:del expectedowners[tuple(r['key'])]
    for r in g['assignments']:expectedowners[r['rgb'],r['state'],r['owner']]=1
    check('All world territorial owners exact expected delta',counter(inv['owners'])==expectedowners)
    for r in q.load('GEOMETRY.json')['assignments']:
        if r['owner']=='HLB':check('Accepted Eutin RGB '+r['rgb'],all(after[y,x]==before[y,x] for x,y in r['cells']) and int((after==int(r['rgb'][1:],16)).sum())==r['pixels'])
    for row in g['new_provinces']:
        check('New RGB absent from old bitmap '+row['rgb'],not np.any(before==int(row['rgb'][1:],16)))
    locs=q.r9.locators(before)
    check('All native locator cells unchanged',all(after[int(r['Y']),int(r['X'])]==before[int(r['Y']),int(r['X'])] for r in locs))
    for key in ['state_types','countries','buildings','building_levels_written','units','errors','duplicates']:
        check('Unchanged global inventory '+key,inv[key]==b['inventory'][key])
    expectedpop=counter(b['inventory']['regional_pop']);alloc=load('POPULATION_ALLOCATION.json')
    for r in alloc['profiles']:
        religion=r['religion'] if r['religion']!='DEFAULT' else 'DEFAULT:'+r['culture']
        key=(SID,'LUB',r['culture'],religion);target=(SID,'HLB',r['culture'],religion)
        expectedpop[key]-=r['after']['HLB'];expectedpop[target]+=r['after']['HLB']
    check('All world population profiles exact declared transfer',counter(inv['regional_pop'])==expectedpop)
    check('Global culture/religion totals unchanged by technical redistribution',inv['pops']==b['inventory']['pops'])
    raw=(ROOT/POP).read_text(encoding='utf-8-sig');pops=q.core.region(raw,SID,'HLB').children('create_pop')
    check('Six accepted Eutin blocks byte-identical',[raw[p.start:p.end] for p in pops[:6]]==b['eutin_pop_blocks'])
    check('Separate new territory population blocks only',len(pops)==8 and [int(p.one('size')) for p in pops[6:]]==[1568,38])
    world=sum(r['count'] for r in inv['pops']);check('Actual world total',world==835801255)
    ledger=json.loads(q.core.active_registry_path().read_text(encoding='utf8'))
    oldmask=np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]);newmask=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
    check('Imperial extent pixel-identical',np.array_equal(oldmask,newmask))
    # Reuse the actual MAP2L starting ledger, Belgian replacement and separate
    # Piedmont extension; MAP2K alone predates these and is not a valid root.
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry']
    belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'))
    regions={r['state'] for r in belgian['assignments']}
    frozen=[r for r in initial if r['state'] not in regions]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in belgian['assignments']]+approved_territorial_extensions()
    check('Cumulative explicit registry migrations replay exactly',apply_territorial_migrations(frozen)==ledger)
    check('Registry 508 to 510; no duplicate RGB',len(ledger)==510 and len({r['rgb'] for r in ledger})==510)
    for r in ledger:check('Registered title '+r['rgb'],owners.get(r['rgb'])==[r['state'],r['beneficiary']])
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')
    for r in g['new_provinces']:
        check('Exactly one inherited terrain '+r['rgb'],len(re.findall(r'(?im)^\s*'+r['rgb']+r'\s*=',terrain))==1)
    for p,text in load('EXPECTED_TEXT.json').items():check('Reviewed history text '+p,(ROOT/p).read_text(encoding='utf-8-sig').rstrip()==text.lstrip('\ufeff').rstrip())
    for p,text in load('IMPERIAL_EXPECTED.json').items():check('Reviewed compiled imperial text '+p,(ROOT/p).read_text(encoding='utf-8-sig')==text.lstrip('\ufeff'))
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    allowed=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_FILES.json')['files'])|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    check('All runtime changes explicitly in scope',set(changed)<=allowed,changed)
    check('Native OLD-HLB union and exception unchanged',all(current[p]==b['hashes'][p] for p in ['common/history/diplomacy/99_1776_map2q_eutin_union.txt','common/diplomatic_actions/22_subject_personal_union.txt','common/history/countries/hlb - eutin.txt']))
    check('Independent bridge/prototype preserved',all((ROOT/p).exists() and q.core.sha(ROOT/p)==h for p,h in b['independent_hashes'].items()))
    allowed_reports={'docs/reports/map/MAP2Q/INSTALLED_MANIFEST.json','docs/reports/map/MAP2Q/REPORT.md','docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'}
    drift=[p for p,h in b['prior_artifacts'].items() if not (ROOT/p).exists() or q.core.sha(ROOT/p)!=h]
    check('All earlier baselines and reports preserved except additive current pointers',set(drift)<=allowed_reports,drift)
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',q.core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    dump('WORLD_POPULATION_DELTA.json',dict(before=sum(r['count'] for r in b['inventory']['pops']),after=world,delta=world-835801255,eutin_preserved=7600,new_territory_provisional=1606,HLB_total=9206,historical_population_estimate_for_new_cells=None,method=alloc['method'],not_a_census=True))
    dump('IMPERIAL_REGISTRY_VALIDATION.json',dict(before=508,after=len(ledger),extent_unchanged=bool(np.array_equal(oldmask,newmask)),cumulative_migration_replay=apply_territorial_migrations(frozen)==ledger,new_RGBs=g['new_provinces'],country_membership_unchanged=True,OLD_HLB_union_unchanged=True))
    tests=load('UNIT_TESTS.json') if (OUT/'UNIT_TESTS.json').exists() else None
    result=dict(status='MAP2Q_R3_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST' if all(c['passed'] for c in checks) else 'FAILED',
        historical_core_status='BISHOPRIC_CORE_GAMEPLAY_PARTIAL',ecclesiastical_status='ECCLESIASTICAL_POSSESSIONS_PARTIAL',runtime_status='NOT_TESTED_R3',
        prior_R2_runtime='PASS_RUNTIME_USER_VALIDATED_MANUAL_ONLY',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
        runtime_files_modified=changed,world_population=world,HLB_population=9206,unit_tests=tests,
        preexisting_anomalies=dict(duplicates=len(inv['duplicates']),errors=len(inv['errors'])),
        native_geographic_error_bound=None,limitations=['Approximation B, not cadastral boundaries.','Ruppersdorf/Neuhof not independently resolved at cell scale.','Domkapitel/Collegiatstift not absorbed.'])
    dump('VALIDATION.json',result)
    print(result['status'],result['passed'],'/',result['total'],'world',world,'changed runtime files',len(changed),flush=True)
    if not all(c['passed'] for c in checks):raise SystemExit(1)
def unit_tests():
    import unittest,io,time
    groups={
        'R3_targeted':['test_map2q_r3'],
        'prior_Q_and_R2_unchanged':['test_map2q_eutin','test_map2q_r2'],
        'cumulative_legacy':['test_map2l_registry','test_map2m_r8','test_map2m_r9','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']}
    results={}
    for key,names in groups.items():
        started=time.monotonic();stream=io.StringIO()
        result=unittest.TextTestRunner(stream=stream,verbosity=1).run(unittest.TestLoader().loadTestsFromNames(names))
        results[key]=dict(modules=names,tests=result.testsRun,failures=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],output=stream.getvalue(),seconds=round(time.monotonic()-started,2))
        print(key,result.testsRun,'tests',len(result.failures),'failures',len(result.errors),'errors',flush=True)
    dump('UNIT_TESTS.json',results)
    if results['R3_targeted']['failures'] or results['R3_targeted']['errors']:raise SystemExit(1)
def previews():
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=load('CURRENT_INVENTORY.json')
    before=q.core.packed(ROOT/b['bitmap_backup']);after=q.core.packed(ROOT/'map_data/provinces.png')
    pal={'LUB':'#b89ccc','HLB':'#e49c55','HOL':'#96b893','MEC':'#b6c9d9','SCH':'#ddc579'}
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    changed={(x,y) for r in g['assignments'] if r['owner']=='HLB' for x,y in r['cells']}
    for filename,box in [('SCHWARTAU_BEFORE_AFTER.png',(4335,736,4344,743)),('KALTENHOF_BEFORE_AFTER.png',(4332,731,4346,744))]:
        x0,y0,x1,y1=box;scale=42;w=(x1-x0)*scale;h=(y1-y0)*scale
        canvas=Image.new('RGB',(2*w+30,h+135),'#ffffff');d=ImageDraw.Draw(canvas)
        for panel,(bmp,inventory,title) in enumerate([(before,b['inventory'],'AVANT R3'),(after,inv,'APRÈS R3 — à tester en jeu')]):
            local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),(173,205,223),dtype=np.uint8)
            owners={r['key'][0]:r['key'][2] for r in inventory['owners']}
            for c in np.unique(local):
                tag=owners.get('x'+format(int(c),'06X'))
                if tag:arr[local==c]=ImageColor.getrgb(pal.get(tag,'#bbbbbb'))
            im=Image.fromarray(arr).resize((w,h),Image.Resampling.NEAREST);dx=panel*(w+30)
            canvas.paste(im,(dx,35));d.text((dx+6,8),title,font=f,fill='#222')
            for x in range(x0,x1):
                for y in range(y0,y1):
                    px=dx+(x-x0)*scale;py=35+(y-y0)*scale
                    d.rectangle((px,py,px+scale,py+scale),outline='#888')
                    if (x,y) in changed:
                        d.rectangle((px+2,py+2,px+scale-2,py+scale-2),outline='#b51626',width=3)
                        d.text((px+3,py+14),'HLB' if panel else 'LUB',font=small,fill='#111')
            for x in range(x0,x1,2):d.text((dx+(x-x0)*scale+1,36),str(x),font=small,fill='#222')
            for y in range(y0+1,y1,2):d.text((dx+2,35+(y-y0)*scale),str(y),font=small,fill='#222')
            # Hollow marker = uninstalled diagnostic hypothesis, not a survey.
            if filename.startswith('KALTENHOF'):
                x,y=load('ALIGNMENT.json')['markers'][-1]['pixel'];px=dx+(x-x0)*scale;py=35+(y-y0)*scale
                d.ellipse((px-5,py-5,px+5,py+5),outline='#2854aa',width=2)
                d.text((dx+3,35+h-22),'Cercle bleu : Ruppersdorf estimé, non installé',font=small,fill='#123c86')
        d.text((6,h+50),'Violet : LUB | orange : HLB | vert : HOL | cadre rouge : les 4 cellules transférées',font=small,fill='#222')
        d.text((6,h+75),'Approximation B : coordonnées bitmap ; pas de certification cadastrale.',font=small,fill='#222')
        d.text((6,h+100),'Eutin inchangé ; aucune liaison artificielle ajoutée.',font=small,fill='#222')
        canvas.save(OUT/filename)
def table_data():
    import csv
    b=load('BASELINE.json');inv=load('CURRENT_INVENTORY.json');g=load('GEOMETRY.json')
    transfers=[]
    for row in g['assignments']:
        if row['owner']!='HLB':continue
        for x,y in row['cells']:transfers.append(dict(RGB_avant=row['parent_rgb'],RGB_apres=row['rgb'],State_ID=SID,X=x,Y=y,Proprietaire_avant='LUB',Proprietaire_apres='HLB',Classe='B',Source='HISTORICAL_EVIDENCE S1-S5',Portee='Schwartau-Rensefeld-Kaltenhof / Ratekau' if row['rgb']=='xEDB204' else 'Offendorf-Ovendorf',Limite='Enveloppe de jeu interpretee; pas cadastre'))
    old={tuple(r['key']):r['count'] for r in b['inventory']['regional_pop']};new={tuple(r['key']):r['count'] for r in inv['regional_pop']}
    pops=[]
    for k in sorted(set(old)|set(new)):
        if k[0]!=SID:continue
        pops.append(dict(Territoire=k[0],TAG=k[1],Culture=k[2],Religion=k[3],Avant=old.get(k,0),Apres=new.get(k,0),Delta=new.get(k,0)-old.get(k,0),Nature='Redistribution technique provisoire' if k[1] in {'LUB','HLB'} else 'Inchange',Note='Six blocs Eutin 7600 preserves; ajout separe 1606' if k[1]=='HLB' else 'Aucun habitant ajoute'))
    pops.append(dict(Territoire='MONDE',TAG='',Culture='Toutes',Religion='Toutes',Avant=835801255,Apres=sum(r['count'] for r in inv['pops']),Delta=0,Nature='Somme des historiques',Note='Conservation par transfert technique; pas contrainte permanente'))
    unresolved=[dict(Secteur='Ruppersdorf',Statut='PARTIAL',Classe='C non installe',Probleme='Titres reperes; enveloppe prudente sans centre de cellule',Suite='Plan local homologue; pas agrandissement force'),
        dict(Secteur='Neuhof',Statut='PARTIAL',Classe='C non installe',Probleme='Domaine identifie; contour propre insuffisant',Suite='Distinguer propriete et juridiction avant subdivision'),
        dict(Secteur='Sereetz / Ratekau franges',Statut='PARTIAL',Classe='B noyau seulement',Probleme='Composition villageoise et droits danois/lubeckois non cadastralement restitues',Suite='Ne pas annexer toute paroisse ni Danischburg'),
        dict(Secteur='Domkapitel / Grossvogtei',Statut='ECCLESIASTICAL_POSSESSIONS_PARTIAL',Classe='C non installe',Probleme='Administration distincte; carte1819 apres secularisation',Suite='Arbitrage institutionnel explicite; pas transfert global'),
        dict(Secteur='Collegiatstift / domaines prives',Statut='PARTIAL',Classe='C non installe',Probleme='Droits fonciers et souverainete non equivalents',Suite='Abstraction des plus petits; pas micro-Etat artificiel'),
        dict(Secteur='Demographie nouveaux territoires',Statut='PROVISIONAL',Classe='Technique',Probleme='1606 redistribues; pas estimation historique de cette emprise',Suite='Donnee datee et perimetre comparable necessaires'),
        dict(Secteur='Georeferencement / limites',Statut='APPROXIMATION_B',Classe='B interpretee',Probleme='Aucune erreur geographique native independante certifiee',Suite='Controle visuel en jeu; ne pas confondre residus et exactitude')]
    with (ROOT/'docs/reports/map/MAP2M/R9/HRE_REGIONS_INVENTORY.csv').open(encoding='utf-8-sig',newline='') as f:regions=list(csv.DictReader(f))
    for row in regions:
        row['R3_update_source']='Inventaire R9 conserve; pas de nouvelle certification'
        if row['Region']=='Frise orientale / Emden':
            row.update(Reports='MAP2O/REPORT.md;MAP2P/REPORT.md',Installed_corrections='319 cellules xF9DCA2 HAN -> PRU; MAP2P aucun transfert nouveau',Manual_validation='MAP2P/MAP2O_RUNTIME_USER_VALIDATION.json',Open_issues='Leer/Rheiderland et marge sud non resolus; noyau Emden seulement',Status='PARTIAL',R3_update_source='MAP2O + MAP2P et attestation manuelle du noyau')
        elif row['Region']=='Wismar–Poel–Neukloster':
            row.update(Current_owners='MEC;MST;SWE',Reports='MAP2N/VALIDATION.json;MAP2N/COMPLETION/VALIDATION.json',Installed_corrections='Poel reconstruite dans STATE_POMERANIA; Wismar-Neukloster quatre RGB SWE',Manual_validation='MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json',Open_issues='Approximations B documentees; pas certification cadastrale',Status='VALIDATED_SCOPED',R3_update_source='MAP2N + COMPLETION et attestation utilisateur')
        elif row['Region']=='Holstein, Schleswig et principauté-évêché de Lübeck':
            row.update(Current_owners='HOL;LUB;SCH;HLB',Reports='MAP2Q/CONTINUATION_R2;MAP2Q/R3',Installed_corrections='Eutin31 cellules + Schwartau-Kaltenhof4 cellules; HLB-OLD union native',Manual_validation='R2 PASS_RUNTIME_USER_VALIDATED; R3 NOT_TESTED',Open_issues='Chapitre; Ruppersdorf; Neuhof; franges; Schleswig non reconstruit',Status='PARTIAL',R3_update_source='Prompt R3 et validation statique R3; pas acceptation moteur R3')
        elif 'Peene' in row['Region'] or 'Netze' in row['Region']:
            row['Manual_validation']='MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json pour seules cellules R8/R9 inspectees'
            row['Reports']+=';MAP2M/R8/REPORT.md;MAP2M/R9/REPORT.md'
            row['R3_update_source']='R8/R9 acceptation manuelle; toutes reserves geometriques anciennes conservees'
            if row['Region']=='Peene R8 et Wolgast R9':
                row['Status']='VALIDATED_SCOPED'
                row['Dependencies']='R8/R9 et transition mensuelle acceptes manuellement; limites historiques non certifiees'
    dump('CSV_TABLES.json',{'TERRITORIAL_CHANGES.csv':transfers,'POPULATION_BEFORE_AFTER.csv':pops,'UNRESOLVED.csv':unresolved,'HRE_REGIONS_INVENTORY_UPDATED.csv':regions})
    print('Prepared four typed table inputs; no CSV authored by Python.')
def current_manifest():
    # Small additive archives, not a new full workspace backup.
    import shutil
    for name in ['INSTALLED_MANIFEST.json','REPORT.md']:
        dest=OUT/('PRE_R3_'+name)
        if not dest.exists():
            assert q.core.sha(q.OUT/name)==load('BASELINE.json')['prior_artifacts'][(q.OUT/name).relative_to(ROOT).as_posix()]
            shutil.copyfile(q.OUT/name,dest)
    old=json.loads((OUT/'PRE_R3_INSTALLED_MANIFEST.json').read_text(encoding='utf8'))
    b=load('BASELINE.json');current=q.economy.runtime_hashes()
    paths=set(old['functional_files'])|set(load('VALIDATION.json')['runtime_files_modified'])
    manifest=dict(functional_files={p:current[p] for p in sorted(paths)},registry_sha256=q.core.sha(q.core.active_registry_path()),
        current_validation='R3/VALIDATION.json',previous_manifest='R3/PRE_R3_INSTALLED_MANIFEST.json',
        stage='MAP2Q_R3_PARTIAL',accepted_eutin_population=7600,additional_territory_provisional_population=1606,HLB_population=9206,
        runtime='R2 manually accepted; R3 not tested')
    dump('INSTALLED_MANIFEST.json',manifest)
    q.core.OUT=OUT;q.core.emit({(q.OUT/'INSTALLED_MANIFEST.json').relative_to(ROOT).as_posix():json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'},'CURRENT_MANIFEST.patch')
    tests=load('UNIT_TESTS.json')
    oldtests=q.load('UNIT_TESTS.json')
    dump('TEST_RECONCILIATION.json',dict(
        R3_targeted=dict(tests=8,failures=tests['R3_targeted']['failures'],errors=tests['R3_targeted']['errors']),
        old_Q_and_R2=dict(tests=11,failures=tests['prior_Q_and_R2_unchanged']['failures'],explanation='Two unchanged Q tests require the whole pre-R3 bitmap and Schwartau untouched. They now fail on the exact four authorized cells. Their old baselines were not replaced.'),
        cumulative_legacy=dict(tests=68,failures=tests['cumulative_legacy']['failures'],explanation='Same six failures as the archived pre-R3 Q run; not converted into PASS.',prior_output='MAP2Q/UNIT_TESTS.json',pre_Q_reconciliation='MAP2Q/UNIT_TEST_RECONCILIATION.json'),
        static_R3='All current global-owner, pixel, population, economics and explicit registry-delta guards are separate from those obsolete snapshots.',automated_engine_test=False))
    print('Current manifest patch prepared; original report and manifest archived.')
def delivery():
    import csv
    required=['REPORT.md','SCHWARTAU_KALTENHOF_AUDIT.md','HISTORICAL_EVIDENCE.md','TERRITORIAL_CHANGES.csv',
        'SCHWARTAU_BEFORE_AFTER.png','KALTENHOF_BEFORE_AFTER.png','ECCLESIASTICAL_POSSESSIONS_AUDIT.md',
        'POPULATION_BEFORE_AFTER.csv','WORLD_POPULATION_DELTA.json','IMPERIAL_REGISTRY_VALIDATION.json','VALIDATION.json',
        'UNRESOLVED.csv','RUNTIME_TEST_PLAN.md','NEXT_REGION_RECOMMENDATION.md','HRE_REGIONS_INVENTORY_UPDATED.csv']
    checks=[]
    for name in required:checks.append(dict(name='Deliverable '+name,passed=(OUT/name).is_file() and (OUT/name).stat().st_size>0))
    for name,rows in load('CSV_TABLES.json').items():
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:actual=list(csv.DictReader(f))
        expected=[{k:'' if v is None else str(v) for k,v in row.items()} for row in rows]
        checks.append(dict(name='CSV roundtrip '+name,passed=actual==expected))
    manifest=q.load('INSTALLED_MANIFEST.json')
    checks.append(dict(name='Current functional manifest matches installed files',passed=all(q.core.sha(ROOT/p)==h for p,h in manifest['functional_files'].items())))
    checks.append(dict(name='Current registry hash matches manifest',passed=q.core.sha(q.core.active_registry_path())==manifest['registry_sha256']))
    checks.append(dict(name='Current static guards pass',passed=load('VALIDATION.json')['passed']==load('VALIDATION.json')['total']==609))
    checks.append(dict(name='R3 not labelled runtime validated',passed=load('VALIDATION.json')['runtime_status']=='NOT_TESTED_R3'))
    dump('DELIVERY_VALIDATION.json',dict(passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,git_mutations=False))
    print('Delivery',sum(r['passed'] for r in checks),'/',len(checks))
    assert all(r['passed'] for r in checks)
if __name__=='__main__':globals()[sys.argv[1]]()
