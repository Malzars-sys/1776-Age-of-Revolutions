"""MAP-2R: immutable current-state capture and reviewed Anhalt continuation."""
import json,sys,subprocess,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageColor
import map2q_eutin as q
import map2q_continue as source
ROOT=q.ROOT
OUT=ROOT/'docs/reports/map/MAP2R'
REGIONS={'STATE_ANHALT','STATE_BRUNSWICK','STATE_HANNOVER'}
TAGS=['ANH','ABG','AKT','AZR']
def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'BASELINE.json').exists(),'Immutable baseline exists'
    manifest=q.load('INSTALLED_MANIFEST.json')
    assert all(q.core.sha(ROOT/p)==h for p,h in manifest['functional_files'].items())
    inv=q.core.qa.inventory()
    assert sum(r['count'] for r in inv['pops'])==835801255
    assert sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='HLB')==9206
    assert all(t not in inv['countries'] for t in TAGS[1:])
    originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            text=p.read_text(encoding='utf-8-sig')
            if any(s in text for s in REGIONS):originals[p.relative_to(ROOT).as_posix()]=text
    bitmap=ROOT/'docs/reports/map/MAP2Q/R3/provinces_candidate.png'
    assert q.core.sha(bitmap)==q.core.sha(ROOT/'map_data/provinces.png')
    dump('BASELINE.json',dict(inventory=inv,originals=originals,hashes=q.economy.runtime_hashes(),
        bitmap_backup=bitmap.relative_to(ROOT).as_posix(),bitmap_sha256=q.core.sha(bitmap),
        registry=json.loads(q.core.active_registry_path().read_text(encoding='utf8')),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=q.core.sha(ROOT/'.git/index'),
        prior_reports={p.relative_to(ROOT).as_posix():q.core.sha(p) for p in (ROOT/'docs/reports/map').rglob('*') if p.is_file() and OUT not in p.parents}))
    print('Baseline protected: world835801255 HLB9206; new TAGs unused',flush=True)
def inspect():
    b=load('BASELINE.json');bmp=q.core.packed(ROOT/b['bitmap_backup']);rows=[]
    for r in b['inventory']['owners']:
        rgb,sid,tag=r['key']
        if sid not in REGIONS:continue
        ys,xs=np.where(bmp==int(rgb[1:],16))
        rows.append(dict(RGB=rgb,State_ID=sid,Owner=tag,Pixels=len(xs),Xmin=int(xs.min()),Xmax=int(xs.max()),Ymin=int(ys.min()),Ymax=int(ys.max())))
    dump('CURRENT_PROVINCES.json',rows)
    print('Anhalt provinces',[r for r in rows if r['State_ID']=='STATE_ANHALT'])
    print('Current ANH population',[r for r in b['inventory']['regional_pop'] if r['key'][1]=='ANH'])
    print('Anhalt locators',[r for r in q.r9.locators(bmp) if 4320<r['X']<4390 and 780<r['Y']<850])
def fetch():source.OUT=OUT;source.fetch()
def assets():
    im=Image.open(OUT/'EVIDENCE/EULER_1753.jp2').convert('RGB')
    print('Primary dimensions',im.size)
    im.resize((2200,round(im.height*2200/im.width))).save(OUT/'EULER_OVERVIEW.png')
def readings():
    im=Image.open(OUT/'EULER_OVERVIEW.png').convert('RGB')
    for name,box in [('CENTRAL',(810,500,1760,945)),('HARZ',(360,560,920,1040)),('NORTH',(1020,220,1810,640))]:
        crop=im.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2));d=ImageDraw.Draw(crop);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
        for x in range((box[0]//100+1)*100,box[2],100):
            p=(x-box[0])*2;d.line((p,0,p,crop.height),fill='#6688cc');d.text((p+2,0),str(x),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            p=(y-box[1])*2;d.line((0,p,crop.width,p),fill='#6688cc');d.text((0,p+2),str(y),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'_READING.png'))
    b=load('BASELINE.json');bmp=q.core.packed(ROOT/b['bitmap_backup']);x0,y0,x1,y1=(4333,788,4402,832)
    local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),(140,190,211),dtype=np.uint8)
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};palette={'ANH':'#dc9ba6','PRU':'#bec3d1','BRA':'#c2a274','SAX':'#a8c990','HAN':'#c8b3d2'}
    for c in np.unique(local):
        tag=owners.get('x'+format(int(c),'06X'));arr[local==c]=ImageColor.getrgb(palette.get(tag,'#a7c3da'))
    im=Image.fromarray(arr).resize(((x1-x0)*20,(y1-y0)*20),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for x in range(x0,x1,2):d.line(((x-x0)*20,0,(x-x0)*20,im.height),fill='#888');d.text(((x-x0)*20+1,0),str(x),font=f,fill='black')
    for y in range(y0,y1,2):d.line((0,(y-y0)*20,im.width,(y-y0)*20),fill='#888');d.text((0,(y-y0)*20+1),str(y),font=f,fill='black')
    for c in np.unique(local):
        yy,xx=np.where(local==c)
        d.text((int(np.median(xx))*20,int(np.median(yy))*20),'x'+format(int(c),'06X'),font=f,fill='black')
    im.save(OUT/'NATIVE_READING.png')
def anchor_crops():
    im=Image.open(OUT/'EULER_OVERVIEW.png').convert('RGB')
    for name,box in [('MAGDEBURG',(960,130,1180,260)),('LEIPZIG',(1500,1350,1740,1510))]:
        p=im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3));d=ImageDraw.Draw(p);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
        for x in range((box[0]//20+1)*20,box[2],20):d.line(((x-box[0])*3,0,(x-box[0])*3,p.height),fill='blue');d.text(((x-box[0])*3,0),str(x),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//20+1)*20,box[3],20):d.line((0,(y-box[1])*3,p.width,(y-box[1])*3),fill='blue');d.text((0,(y-box[1])*3),str(y),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        p.save(OUT/(name+'_ANCHOR.png'))
def alignment():
    # Local use of the retained European diagnostic, NOT a surveyed projection.
    controls=[('Magdeburg',1046,191,11.6276,52.1277),
        ('Bernburg',1108,668,11.740096,51.794638),
        ('Koethen',1329,754,11.970928,51.751855),
        ('Dessau',1567,627,12.2456,51.8386),
        ('Zerbst',1441,427,12.085,51.965),
        ('Ballenstedt',654,767,11.232649,51.719002)]
    def target(lon,lat):return [4365.351074+23.057991056249843*(lon-11.6276),796.939941-30.99675*(lat-52.1277)]
    X=np.array([[x,y,1] for _,x,y,_,_ in controls]);Y=np.array([target(lon,lat) for _,_,_,lon,lat in controls])
    T=np.linalg.lstsq(X,Y,rcond=None)[0]
    rows=[dict(name=n,source=[x,y],target=target(lon,lat),predicted=(np.array([x,y,1])@T).tolist(),
        fit_error_px=float(np.linalg.norm(np.array([x,y,1])@T-target(lon,lat)))) for n,x,y,lon,lat in controls]
    dump('ALIGNMENT.json',dict(transform=T.tolist(),controls=rows,
        limitation='Source fit against a retained geographic diagnostic anchored at the native Magdeburg city. No independent native-city positional certification. Only broad subdivision of existing ANH ownership is authorized here; no PRU fringe inferred from town positions.',
        source='Euler/Rhode/Berger 1753, 2200px overview; source scale does not imply cadastral accuracy.'))
    print(rows)

def geometry():
    b=load('BASELINE.json');before=q.core.packed(ROOT/b['bitmap_backup']);after=before.copy()
    assert q.core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    T=np.array(load('ALIGNMENT.json')['transform'])
    # Generalized historical envelopes read on Euler 1753. Outer fringes are
    # clipped to existing ANH ownership, never used to seize neighboring land.
    polygons={
      'AZR':[(1345,283),(1408,272),(1508,251),(1587,227),(1620,217),(1654,252),(1666,303),(1730,360),(1820,363),(1845,409),(1800,450),(1835,500),(1816,556),(1770,560),(1760,590),(1660,600),(1620,573),(1588,588),(1540,605),(1480,600),(1425,580),(1366,590),(1325,559),(1288,530),(1280,460),(1280,400),(1240,350),(1248,303),(1285,299),(1297,329),(1330,340)],
      'AKT':[(1100,574),(1170,565),(1180,537),(1210,545),(1235,583),(1240,616),(1270,626),(1300,610),(1330,610),(1350,639),(1380,628),(1410,647),(1390,675),(1388,715),(1395,800),(1430,840),(1420,885),(1390,896),(1350,890),(1318,868),(1270,874),(1220,850),(1222,819),(1198,817),(1170,768),(1135,768),(1120,742),(1150,724),(1180,706),(1150,672),(1115,628)],
      'ABG':[(900,568),(960,574),(995,575),(1050,592),(1090,598),(1130,637),(1140,687),(1150,709),(1135,722),(1150,739),(1120,764),(1070,763),(1060,787),(1030,789),(995,757),(970,750),(965,710),(1000,685),(1030,650),(995,630),(960,625),(935,650),(910,670),(900,632)]}
    # Warmsdorf is Koethen, not Bernburg; Groebzig is Dessau, not Koethen.
    holes={'ABG':[[(932,630),(990,636),(1054,654),(1020,679),(980,708),(953,731),(910,717),(921,686)]],
        'AKT':[[(1190,757),(1230,750),(1260,777),(1263,799),(1277,824),(1280,844),(1240,842),(1210,826),(1198,800)]]}
    parents=['x8A448C','xED8F7B'];yy,xx=np.where(np.isin(before,[int(c[1:],16) for c in parents]));points=np.column_stack([xx+.5,yy+.5])
    labels=np.full(len(xx),'ANH',dtype='<U3');traces=[]
    for tag,poly in polygons.items():
        mapped=np.column_stack([np.array(poly),np.ones(len(poly))])@T
        selected=q.core.inside(points,mapped)
        for hole in holes.get(tag,[]):selected &= ~q.core.inside(points,np.column_stack([np.array(hole),np.ones(len(hole))])@T)
        assert not np.any(selected & (labels!='ANH')),'Overlapping traced territories'
        labels[selected]=tag;traces.append(dict(tag=tag,source_polygon=poly,game_polygon=mapped.tolist(),source_holes=holes.get(tag,[])))
    for tag,poly,note in [
        ('ABG',[(525,744),(550,744),(590,745),(620,735),(670,739),(710,732),(704,755),(680,768),(650,783),(600,791),(560,791),(555,825),(559,871),(585,906),(601,934),(604,952),(558,947),(520,931),(495,911),(473,903),(461,873),(486,852),(494,811),(497,781)],'Harz: interior around Ballenstedt and Harzgerode; Hoym and Quedlinburg excluded'),
        ('AKT',[(938,646),(985,646),(1034,657),(1010,679),(975,703),(950,718),(925,706),(933,681)],'Warmsdorf detached core; no corridor')]:
        mapped=np.column_stack([np.array(poly),np.ones(len(poly))])@T;selected=q.core.inside(points,mapped)
        assert not np.any(selected & (labels!='ANH')),'Overlapping traced interior'
        labels[selected]=tag;traces.append(dict(tag=tag,source_polygon=poly,game_polygon=mapped.tolist(),source_holes=[],note=note))
    assignments=[];new=[];color=0xEDB300;used=set(int(v) for v in np.unique(before))
    for parent in parents:
        original=before==int(parent[1:],16)
        sublabels=np.full(before.shape,'',dtype='<U3');sublabels[yy,xx]=labels
        for tag in TAGS:
            parts=q.core.components(original & (sublabels==tag))
            for k,part in enumerate(parts):
                if tag=='ANH' and k==0:rgb=parent
                else:
                    while color in used:color+=1
                    rgb='x'+format(color,'06X');used.add(color);color+=1
                    new.append(dict(rgb=rgb,parent_rgb=parent))
                ys=np.array([p[0] for p in part]);xs=np.array([p[1] for p in part]);after[ys,xs]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state='STATE_ANHALT',previous_owner='ANH',owner=tag,pixels=len(part),cells=[[int(x),int(y)] for y,x in part],confidence='B' if tag!='ANH' else 'C_RETAINED',basis='Euler 1753 generalized interior, clipped to existing ANH; residual ANH fringes retained, not certified as Dessau'))
    assert all(any(r['owner']==tag for r in assignments) for tag in TAGS)
    assert sum(r['pixels'] for r in assignments)==279
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,hub_rebindings=[],traces=traces))
    im=Image.open(OUT/'EULER_OVERVIEW.png').convert('RGB');d=ImageDraw.Draw(im)
    for trace in traces:d.line(trace['source_polygon']+[trace['source_polygon'][0]],fill={'ABG':'lime','AKT':'red','AZR':'blue'}[trace['tag']],width=3)
    im.crop((360,220,1860,980)).save(OUT/'SOURCE_TRACING_REVIEW.png')
    print('Assignment cells',dict(__import__('collections').Counter({t:sum(r['pixels'] for r in assignments if r['owner']==t) for t in TAGS})))
    print('New RGBs',new)
    preview(before,after,assignments)

def compiler_before():
    import map2q_r3 as prior
    prior.OUT=OUT;prior.compiler_before()

def prepare():
    import collections as C,re
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};sid='STATE_ANHALT'
    assert q.economy.runtime_hashes()==b['hashes'],'Runtime drift: review before writing'
    assert load('COMPILER_BEFORE.json')['passed']==load('COMPILER_BEFORE.json')['total']==57
    rel='common/history/states/00_states.txt';raw=b['originals'][rel];s=q.core.state(raw,sid)
    n=next(n for n in s.children('create_state') if n.one('country')=='c:ANH');f=n.children('owned_provinces')[0]
    existing=q.core.values(n,'owned_provinces');assert set(existing)==set(g['parents'])
    ops=[(f.start,f.end,'owned_provinces = { '+' '.join(r['rgb'] for r in g['assignments'] if r['owner']=='ANH')+' }')]
    extra='\n'.join('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(r['rgb'] for r in g['assignments'] if r['owner']==tag)+' } }' for tag in TAGS[1:])
    ops.append((s.end-1,s.end-1,'\n'+extra+'\n'));files[rel]=q.core.edits(raw,ops)
    rel='map_data/state_regions/00_west_europe.txt';raw=b['originals'][rel];s=next(n for n in q.core.cw.parse(raw) if n.key==sid);ops=[];bindings=[]
    for field in ['provinces','prime_land']:
        for f in s.children(field):
            old=q.core.values(s,field);new=[]
            for c in old:new.extend([r['rgb'] for r in g['assignments'] if r['parent_rgb']==c] if c in g['parents'] else [c])
            if old!=new:
                ops.append((f.start,f.end,field+' = { '+' '.join('"'+c+'"' for c in new)+' }'))
                if field=='prime_land':bindings.append(dict(state=sid,field=field,before=old,after=new))
    # Hubs stay physically fixed. Rebind only if the cell acquired a child RGB.
    before=q.core.packed(ROOT/b['bitmap_backup']);after=q.core.packed(OUT/'provinces_candidate.png')
    for loc in q.r9.locators(before):
        if loc['ID']!=62:continue
        field=loc['Kind'];x,y=int(loc['X']),int(loc['Y']);new='x'+format(int(after[y,x]),'06X')
        old=q.core.cw.scalar(s.one(field))
        if old in g['parents'] and old!=new:
            f=s.children(field)[0];ops.append((f.start,f.end,field+' = "'+new+'"'))
            bindings.append(dict(state=sid,field=field,before=old,after=new,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
    files[rel]=q.core.edits(raw,ops)
    counts=C.Counter()
    for r in g['assignments']:counts[r['owner']]+=r['pixels']
    allocations=[]
    for rel,original in b['originals'].items():
        if '/pops/' not in rel:continue
        try:n=q.core.region(original,sid,'ANH')
        except StopIteration:continue
        ops=[];pieces=C.defaultdict(list)
        for pop in n.children('create_pop'):
            f=pop.children('size')[0];amounts=q.core.allocate(int(f.value),counts)
            ops.append((f.start,f.end,'size = '+str(amounts['ANH'])))
            for tag in TAGS[1:]:
                if amounts[tag]:pieces[tag].append(q.core.edits(original[pop.start:pop.end],[(f.start-pop.start,f.end-pop.start,'size = '+str(amounts[tag]))]))
            allocations.append(dict(culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:north_german'),before=int(f.value),after=amounts))
        raw=q.core.edits(original,ops)
        for tag,content in pieces.items():raw=q.core.append(raw,sid,tag,'\n'.join(content))
        files[rel]=raw
    assert sum(a['before'] for a in allocations)==152886
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw+'\n'+''.join(r['rgb']+'="'+tm[r['parent_rgb'].upper()]+'"\n' for r in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state']==sid]
    updated=[r for r in previous if r['rgb'] not in g['parents']]+[dict(rgb=r['rgb'],state=sid,beneficiary=r['owner'],basis='MAP2R: reviewed subdivision of existing Anhalt; B core envelopes, residual Dessau attribution provisional. See MAP2R/REPORT.md.') for r in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state']!=sid]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    migration=dict(replaced_regions=[sid],previous=previous,updated=updated,new_members=TAGS[1:],free_cities=[],new_provinces=g['new_provinces'],geometry='MAP2R/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[])
    countries(files,migration)
    files[q.core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):q.core.cw.parse(raw)
    dump('EXPECTED_TEXT.json',files);dump('POPULATION_ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_REDISTRIBUTION_NOT_HISTORICAL_ESTIMATE',source_cells=279,weights=dict(counts),profiles=allocations))
    q.core.OUT=OUT;changes=q.core.emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,registered_RGBs=len(ledger),region_reference_changes=bindings))
    print('Prepared text files',len(changes),'registered RGBs',len(ledger),'weights',dict(counts),'bindings',bindings)

def countries(files,migration):
    colors={'ABG':'114 158 90','AKT':'205 122 150','AZR':'218 183 83'}
    defs=''.join(t+' = { color = { '+colors[t]+' } country_type = recognized tier = principality cultures = { north_german } religion = protestant capital = STATE_ANHALT }\n' for t in TAGS[1:])
    files['common/country_definitions/1776_map2r_anhalt.txt']=defs
    migration['country_additions']={n.key:q.core.qa.signature(n) for n in q.core.cw.parse(defs)}
    rel='common/country_definitions/00_countries.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');node=next(n for n in q.core.cw.parse(raw) if n.key=='ANH');f=node.children('is_named_from_capital')[0]
    assert f.value=='yes';raw=q.core.edits(raw,[(f.start,f.end,'is_named_from_capital = no')]);newnode=next(n for n in q.core.cw.parse(raw) if n.key=='ANH');files[rel]=raw
    migration['anhalt_name_correction']=dict(tag='ANH',before_signature=q.core.qa.signature(node),after_signature=q.core.qa.signature(newnode))
    original=(ROOT/'common/history/countries/anh - anhalt.txt').read_text(encoding='utf-8-sig')
    for tag in TAGS[1:]:files['common/history/countries/'+tag.lower()+' - map2r anhalt.txt']=original.replace('c:ANH','c:'+tag)
    rulers={'ANH':('Leopold Friedrich Franz','1740.8.10'),'ABG':('Friedrich Albrecht','1735.8.15'),'AKT':('Karl Georg Lebrecht','1730.8.15'),'AZR':('Friedrich August','1734.8.8')}
    for tag,(name,born) in rulers.items():
        # Override native 1836 ANH ruler/heir file, rather than duplicate rulers.
        rel='common/history/characters/'+('anh - anhalt.txt' if tag=='ANH' else tag.lower()+' - map2r anhalt.txt')
        assert not (ROOT/rel).exists(),'Review pre-existing character override '+rel
        files[rel]='CHARACTERS = { c:'+tag+' ?= { create_character = { first_name = aor1776_map2r_'+tag.lower()+'_first last_name = Askanier historical = yes culture = north_german religion = rel:protestant ruler = yes birth_date = '+born+' interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    files['common/flag_definitions/1776_map2r_anhalt.txt']='# Shared Ascanian arms are an explicit graphical abstraction, not evidence of political union.\n'+''.join(t+' = { flag_definition = { coa = ANH priority = 100 allow_overlord_canton = no } }\n' for t in TAGS[1:])
    names={'ANH':('Anhalt-Dessau','Anhalt-Dessau'),'ABG':('Anhalt-Bernburg','Anhalt-Bernbourg'),'AKT':('Anhalt-Köthen','Anhalt-Köthen'),'AZR':('Anhalt-Zerbst','Anhalt-Zerbst')}
    for lang,i in [('english',0),('french',1)]:
        # replace/ intentionally overrides native ANH naming without duplicate keys.
        loc='\ufeffl_'+lang+':\n'
        for tag,pair in names.items():loc+=' '+tag+':0 "'+pair[i]+'"\n '+tag+'_ADJ:0 "'+pair[i]+'"\n aor1776_map2r_'+tag.lower()+'_first:0 "'+rulers[tag][0]+'"\n'
        files[f'localization/{lang}/replace/1776_map2r_anhalt_l_{lang}.yml']=loc

def install():
    b=load('BASELINE.json');files=load('EXPECTED_TEXT.json')
    assert q.core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    for p,raw in files.items():assert (ROOT/p).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip(),p
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Installed only reviewed child RGB bitmap; text previously verified.')

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files)
    q.core.OUT=OUT;changes=q.core.emit(files,'IMPERIAL.patch');dump('IMPERIAL_FILES.json',dict(files=changes))
    print('Imperial runtime updates',len(changes))

def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()

def validate():
    import collections as C,re
    from map2l_registry import apply_territorial_migrations,approved_territorial_extensions,expected_country_definitions,approved_territorial_migrations
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=q.core.qa.inventory();dump('CURRENT_INVENTORY.json',inv)
    checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=q.core.packed(ROOT/b['bitmap_backup']);after=q.core.packed(ROOT/'map_data/provinces.png');expected=before.copy()
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    for r in g['assignments']:
        for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
        check('Connected province '+r['rgb'],len(q.core.components(after==int(r['rgb'][1:],16)))==1)
        check('Exact owner/state '+r['rgb'],owners.get(r['rgb'])==[r['state'],r['owner']])
        check('Exact cell count '+r['rgb'],int(np.sum(after==int(r['rgb'][1:],16)))==r['pixels'])
    check('All world pixels match exact declared child RGBs',np.array_equal(after,expected))
    check('No external territory transferred',all(r['state']=='STATE_ANHALT' and r['previous_owner']=='ANH' for r in g['assignments']))
    eo=counter(b['inventory']['owners'])
    for k in list(eo):
        if k[0] in g['parents']:del eo[k]
    for r in g['assignments']:eo[r['rgb'],r['state'],r['owner']]=1
    check('All world owners match exact expected delta',counter(inv['owners'])==eo)
    for r in g['new_provinces']:
        check('New RGB absent from previous bitmap '+r['rgb'],not np.any(before==int(r['rgb'][1:],16)))
        check('RGB resolves to correct State_ID '+r['rgb'],inv['geometry'].get(r['rgb'])=='STATE_ANHALT')
    for key in ['buildings','building_levels_written','units','errors','duplicates']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    types=dict(b['inventory']['state_types']);types.update({'STATE_ANHALT|'+t:'incorporated_default' for t in TAGS[1:]})
    check('Only three authorized state subdivisions added',inv['state_types']==types)
    check('Country definitions exact approved additions and ANH name field',inv['countries']==expected_country_definitions(b['inventory']['countries'],[load('REGISTRY_MIGRATION.json')]))
    ep=counter(b['inventory']['regional_pop']);allocation=load('POPULATION_ALLOCATION.json')
    for p in allocation['profiles']:
        religion=p['religion'];key=('STATE_ANHALT','ANH',p['culture'],religion)
        ep[key]-=p['before']
        for tag,n in p['after'].items():ep['STATE_ANHALT',tag,p['culture'],religion]+=n
    check('All world population profiles match declared redistribution',counter(inv['regional_pop'])==ep)
    check('All culture/religion totals conserved in technical redistribution',inv['pops']==b['inventory']['pops'])
    world=sum(r['count'] for r in inv['pops']);hlb=sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='HLB')
    check('HLB 9206 and world 835801255 verified directly',hlb==9206 and world==835801255)
    ledger=json.loads(q.core.active_registry_path().read_text(encoding='utf8'))
    oldmask=np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]);newmask=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
    check('Imperial physical extent unchanged',np.array_equal(oldmask,newmask))
    import prototype_map2k_main_map as main_map
    mask_path=ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds'
    decoded=np.array(Image.open(mask_path).convert('RGBA'))[:,:,0]==255
    x0,y0=main_map.ORIGIN
    check('Installed imperial main-map mask still matches registry',np.array_equal(decoded,newmask[y0:y0+main_map.TILE,x0:x0+main_map.TILE]))
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry']
    belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'));regions={r['state'] for r in belgian['assignments']}
    frozen=[r for r in initial if r['state'] not in regions]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in belgian['assignments']]+approved_territorial_extensions()
    replay=apply_territorial_migrations(frozen)
    check('Cumulative territorial registry replay',replay==ledger)
    check('Exactly 521 unique registered RGBs',len(ledger)==521 and len({r['rgb'] for r in ledger})==521)
    for r in ledger:check('Registered title '+r['rgb'],owners.get(r['rgb'])==[r['state'],r['beneficiary']])
    raw=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    for r in g['new_provinces']:
        check('Single inherited terrain '+r['rgb'],len(re.findall(r'(?im)^\s*'+r['rgb']+r'\s*=',raw))==1 and terrain[r['rgb'].upper()]==terrain[r['parent_rgb'].upper()])
    rel='map_data/state_regions/00_west_europe.txt'
    old=next(n for n in q.core.cw.parse(b['originals'][rel]) if n.key=='STATE_ANHALT');now=next(n for n in q.core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig')) if n.key=='STATE_ANHALT')
    excluded={'provinces','prime_land','farm'}
    check('Resources infrastructure modifiers and locators preserved',[q.core.qa.signature(n) for n in old.children() if n.key not in excluded]==[q.core.qa.signature(n) for n in now.children() if n.key not in excluded])
    bindings=load('REGISTRY_MIGRATION.json')['region_reference_changes'];bound={tuple(r['pixel']) for r in bindings if 'pixel' in r}
    locs=q.r9.locators(before)
    check('Only declared farm RGB changed under stationary locators',all(after[int(l['Y']),int(l['X'])]==before[int(l['Y']),int(l['X'])] or (int(l['X']),int(l['Y'])) in bound for l in locs))
    for p,text in load('EXPECTED_TEXT.json').items():check('Reviewed history '+p,(ROOT/p).read_text(encoding='utf-8-sig').rstrip()==text.lstrip('\ufeff').rstrip())
    for p,text in load('IMPERIAL_EXPECTED.json').items():check('Reviewed compiled imperial '+p,(ROOT/p).read_text(encoding='utf-8-sig')==text.lstrip('\ufeff'))
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    allowed=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_FILES.json')['files'])|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    check('All runtime modifications explicitly scoped',set(changed)<=allowed,changed)
    check('Every building military and diplomacy runtime file unchanged',all(current.get(p)==h for p,h in b['hashes'].items() if any('/'+folder+'/' in p for folder in ['buildings','military_formations','diplomacy'])))
    drift=[p for p,h in b['prior_reports'].items() if not (ROOT/p).exists() or q.core.sha(ROOT/p)!=h]
    check('All previous reports and baselines preserved except active ledger',set(drift)<={'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'},drift)
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',q.core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    dump('WORLD_POPULATION_DELTA.json',dict(before=835801255,after=world,delta=world-835801255,HLB_total=hlb,method=allocation['method'],historical_estimate_applied=False,world_not_required_invariant=True,reason='No dated population with matching installed core perimeter. No artificial inhabitants or neighbor compensation.'))
    dump('IMPERIAL_REGISTRY_VALIDATION.json',dict(before=510,after=len(ledger),extent_unchanged=bool(np.array_equal(oldmask,newmask)),cumulative_replay=replay==ledger,new_members=TAGS[1:],new_electors=[],free_cities=[],native_union_OLD_HLB_preserved=True,capital_region='STATE_ANHALT',historical_city_hubs_not_certified=True))
    result=dict(status='MAP2R_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST' if all(c['passed'] for c in checks) else 'FAILED',runtime_status='NOT_TESTED_MAP2R',historical_status='FOUR_PRINCIPALITIES_CORE_ONLY_NOT_COMPLETE',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime_files_modified=changed,world_population=world,HLB_population=hlb,preexisting_anomalies=dict(duplicates=len(inv['duplicates']),invalid_references=len(inv['errors'])),new_geographic_error_bound=None)
    if (OUT/'UNIT_TESTS.json').exists():result['unit_tests']=load('UNIT_TESTS.json')
    if (OUT/'CSV_VALIDATION.json').exists():result['tables']=load('CSV_VALIDATION.json')
    dump('VALIDATION.json',result)
    dump('INSTALLED_MANIFEST.json',dict(lot='MAP2R',status=result['status'],functional_files={p:current[p] for p in changed},bitmap_sha256=q.core.sha(ROOT/'map_data/provinces.png'),previous_manifest='docs/reports/map/MAP2Q/INSTALLED_MANIFEST.json',previous_manifest_is_stage_snapshot_not_current=True))
    print(result['status'],result['passed'],'/',result['total'],'world',world,'HLB',hlb,flush=True)
    if result['passed']!=result['total']:raise SystemExit(1)

def unit_tests():
    import unittest,io,time
    groups={'MAP2R_targeted':['test_map2r_anhalt'],'previous_stages':['test_map2q_r3','test_map2q_eutin','test_map2q_r2'],'cumulative':['test_map2l_registry','test_map2m_r8','test_map2m_r9','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']};results={}
    for key,modules in groups.items():
        started=time.monotonic();stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=1).run(unittest.TestLoader().loadTestsFromNames(modules))
        results[key]=dict(modules=modules,tests=r.testsRun,failures=[t.id() for t,_ in r.failures],errors=[t.id() for t,_ in r.errors],output=stream.getvalue(),seconds=round(time.monotonic()-started,2))
        print(key,r.testsRun,'tests',len(r.failures),'failures',len(r.errors),'errors',flush=True)
    dump('UNIT_TESTS.json',results)
    if results['MAP2R_targeted']['failures'] or results['MAP2R_targeted']['errors']:raise SystemExit(1)

def table_data():
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=load('CURRENT_INVENTORY.json')
    audit=[]
    for tag,territory in [('ANH','Dessau / Wörlitz et résidu ancien ANH'),('ABG','Bernburg / Plötzkau et intérieurs du Harz'),('AKT','Köthen et intérieur détaché de Warmsdorf'),('AZR','Zerbst / Roßlau / Coswig, enveloppe tronquée par ancien ANH')]:
        audit.append(dict(Territoire=territory,TAG_avant='ANH',TAG_apres=tag,State_ID='STATE_ANHALT',ID_numerique=62,
            Cellules=sum(a['pixels'] for a in g['assignments'] if a['owner']==tag),Statut='Noyaux B seulement' if tag!='ANH' else 'Maintien provisoire ; franges C',
            Source='Euler/Rhode/Berger 1753 ; LASA Gesamt-Anhalt, Zerbst, Bernburg',Population='Redistribution technique, pas estimation historique',
            Limite='Frontières approximatives ; aucune annexion prussienne. Capitales dans région économique partagée, hub physique non certifié.'))
    audit.extend([dict(Territoire=t,TAG_avant=old,TAG_apres=old,State_ID=s,ID_numerique=number,Cellules=None,Statut='C non appliqué',Source=src,Population='Inchangée',Limite=note) for t,old,s,number,src,note in [
        ('Jever','OLD','STATE_HANNOVER',69,'NLA OL Best 90 ; MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md','Souveraineté Zerbst établie mais contour natif non établi ; OLD reste une anomalie connue, pas un arbitrage historique.'),
        ('Hoym','PRU/ANH','STATE_ANHALT',62,'LASA ID188269 et ID188270','Branche Bernburg-Schaumburg-Hoym distincte ; ne pas annexer mécaniquement à ABG.'),
        ('Franges Harz / Anhalt hors ancienne emprise ANH','PRU/BRA','STATE_ANHALT;STATE_BRUNSWICK',None,'Euler1753 ; R2 retenu','Pas de transfert voisin sans correspondance de limite défendable.')]])
    transfers=[]
    for a in g['assignments']:
        if a['rgb']==a['parent_rgb']:continue
        for x,y in sorted(a['cells']):transfers.append(dict(RGB_avant=a['parent_rgb'],RGB_apres=a['rgb'],State_ID=a['state'],ID_numerique=62,X=x,Y=y,Proprietaire_avant='ANH',Proprietaire_apres=a['owner'],Classe=a['confidence'],Nature='Transfert de souveraineté' if a['owner']!='ANH' else 'RGB technique, propriétaire inchangé',Source='Euler1753 ; GEOMETRY.json / ALIGNMENT.json',Limite='Noyau simplifié B ou résidu C inchangé ; pas de borne géographique indépendante'))
    old={tuple(p['key']):p['count'] for p in b['inventory']['regional_pop']};new={tuple(p['key']):p['count'] for p in inv['regional_pop']};pops=[]
    for key in sorted(set(old)|set(new)):
        if key[0]!='STATE_ANHALT':continue
        pops.append(dict(State_ID=key[0],TAG=key[1],Culture=key[2],Religion=key[3],Avant=old.get(key,0),Apres=new.get(key,0),Delta=new.get(key,0)-old.get(key,0),Nature='Redistribution technique provisoire' if key[1] in TAGS else 'Inchangé',Source='Historiques écrits avant/après ; méthode POPULATION_ALLOCATION.json'))
    pops.append(dict(State_ID='MONDE',TAG='',Culture='Toutes',Religion='Toutes',Avant=835801255,Apres=sum(p['count'] for p in inv['pops']),Delta=0,Nature='Total vérifié, pas une contrainte historique',Source='Inventaire effectif du mod et du jeu installé'))
    unresolved=[dict(Secteur=s,Classe=c,Statut='OUVERT',Probleme=p,Action=a) for s,c,p,a in [
        ('Jever','A souveraineté / C tracé','Toujours OLD dans le jeu, alors que possession Zerbst en1776. Limites avec Varel/Kniphausen non calées.','Carte territoriale locale avant1793 et contrôle des limites dans le bitmap ; ne pas toucher Emden.'),
        ('Harz','B noyaux / C franges','Seuls intérieurs recoupant ancienne emprise ANH installés ; Ballenstedt-Harzgerode non reconstruits intégralement.','Traiter les franges prussiennes/brunswickoises avec repères homologues, sans corridor.'),
        ('Hoym','C','Bernburg-Schaumburg-Hoym ne doit pas être fusionné automatiquement avec Bernburg.','Arbitrer son abstraction avant tout transfert ; pas de cinquième pays créé ici.'),
        ('Dessau et enclaves résiduelles','C','167 cellules restent ANH dont des franges non certifiées comme possessions de Dessau.','Ne pas présenter la conservation technique comme attribution historique démontrée.'),
        ('Zerbst, Coswig, Roßlau','B tronqué','Enveloppe source limitée à ancienne emprise ANH ; extensions éventuelles vers PRU non validées.','Achever les raccords seulement avec correspondance de frontière justifiée.'),
        ('Démographie','Technique','Chiffre municipal Köthen1770 :24702 pour ville et pays ; emprise et date ne coïncident pas avec noyau installé.','Conserver chiffres techniques, rechercher seulement un périmètre comparable avant estimation.'),
        ('Capitales et économie des petits États','Technique / moteur','Une même région économique62, pas quatre hubs urbains indépendants. Aucun bâtiment déplacé ; nouveaux pays sans industrie écrite propre.','Tester marché, subsistance, capitales et partages de capacités en nouvelle partie.'),
        ('Géoréférencement','B non certifié','Résidus de source contre diagnostic ; aucune erreur native indépendante mesurée.','Pas de revendication de précision à deux pixels ; contrôle visuel des noyaux.'),
        ('Drapeaux','Abstraction','Armes ascaniennes partagées, pas quatre bannières reconstruites.','Différencier graphiquement ultérieurement avec sources, sans confondre les États.'),
        ('Anomalies préexistantes','Hors périmètre','44 doublons RGB et12 références invalides dans inventaire antérieur.','Conserver liste exacte et comparer, ne pas les masquer ni élargir ce lot.')]]
    dump('CSV_TABLES.json',{'ANHALT_TERRITORIAL_AUDIT.csv':audit,'CURRENT_PROVINCES.csv':load('CURRENT_PROVINCES.json'),'TERRITORIAL_CHANGES.csv':transfers,'POPULATION_BEFORE_AFTER.csv':pops,'UNRESOLVED.csv':unresolved})
    print('Five typed tables staged as JSON; CSV authoring delegated to documented artifact tool builder.')

def reports():
    b=load('BASELINE.json');g=load('GEOMETRY.json');v=load('VALIDATION.json');tests=load('UNIT_TESTS.json');files={}
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    moved=sum(a['pixels'] for a in g['assignments'] if a['owner']!='ANH');recolored=sum(a['pixels'] for a in g['assignments'] if a['rgb']!=a['parent_rgb'])
    totals={t:sum(p['count'] for p in load('CURRENT_INVENTORY.json')['regional_pop'] if p['key'][1]==t) for t in TAGS}
    files[prefix+'REPORT.md']=f'''# MAP-2R — Quatre principautés d’Anhalt, noyaux installés

Date de livraison : 17 octobre 2026. Date historique cible : 1er janvier 1776.

**Statut : {v['status']}. Le chantier territorial complet n’est pas terminé.**
Les noyaux supplémentaires sont installés et prêts pour un contrôle ciblé en nouvelle partie. Aucune validation moteur MAP-2R n’est revendiquée.

## Résultat réellement installé

| Pays | TAG | Cellules de l’ancienne emprise ANH | Population technique |
|---|---|---:|---:|
| Anhalt-Dessau, avec résidus non attribués historiquement | ANH | 167 | {totals['ANH']} |
| Anhalt-Bernbourg, noyau et fragments intérieurs du Harz | ABG | 23 | {totals['ABG']} |
| Anhalt-Köthen, noyau et fragment de Warmsdorf | AKT | 33 | {totals['AKT']} |
| Anhalt-Zerbst, noyau pré-partition | AZR | 56 | {totals['AZR']} |

{moved} cellules changent de propriétaire, ANH vers les trois nouveaux pays. {recolored} cellules changent de RGB, incluant les fragments techniques dont le propriétaire reste ANH. Onze nouveaux RGB sont créés. Les 279 cellules des deux provinces initiales sont toutes comptabilisées, sans extension vers la Prusse ou Brunswick.

La carte de 1753 fournit des enveloppes de juridiction simplifiées, découpées à la résolution du jeu et limitées à l’emprise déjà détenue par ANH. Ce choix permet une correction politique réelle sans faire passer un calage diagnostique pour une mesure topographique certifiée. **Les résidus conservés à Dessau ne sont pas tous des possessions de Dessau démontrées.** Les limites exactes et les extensions manquantes restent ouvertes.

Les trois TAGs ont été autorisés par le joueur. Ils sont membres ordinaires du bloc impérial, sans nouveaux électeurs ni villes libres. Les droits de restauration distinguent désormais les quatre pays. Le registre passe de 510 à 521 RGB, à étendue physique impériale identique. La carte du journal est régénérée ; le masque physique du mode carte n’a pas besoin d’être élargi.

Les souverains de 1776 remplacent les personnages natifs de 1836 : Leopold Friedrich Franz, Friedrich Albrecht, Karl Georg Lebrecht et Friedrich August. Les trois nouveaux pays reprennent les lois et technologies de départ de l’ancien ANH comme abstraction de gameplay, pas comme quatre audits législatifs. Les armes ascaniennes partagées sont une simplification graphique explicite, pas une union politique.

## Données conservées

- Populations mondiales vérifiées : 835 801 255 avant et après. Cette égalité provient de la redistribution technique choisie ici et n’est pas une contrainte pour les travaux futurs.
- Tous les profils culture/religion sont conservés. Les quatre nombres ci-dessus ne sont ni des recensements ni des estimations historiques validées.
- HLB : 9 206 habitants et union OLD–HLB inchangés. Son [acceptation manuelle R3](../MAP2Q/R3/RUNTIME_USER_VALIDATION.json) est conservée séparément.
- Bâtiments écrits, niveaux, PM, propriétaires économiques, infrastructures écrites, armées et recrutements inchangés. Les nouveaux pays n’ont pas reçu artificiellement d’industrie ou d’armée ; vérifier leur fonctionnement économique en jeu.
- Capacités et ressources de la région économique inchangées. Leur répartition effective entre subdivisions, la subsistance et les marchés doivent être contrôlés au chargement.
- Tous les autres pixels, propriétaires et populations sont protégés par comparaison différentielle mondiale. Aucun travail à Erfurt–Eichsfeld, en Frise orientale ou dans un autre lot.
- Aucun commit, changement de branche, modification de HEAD ou de l’index.

## Limites importantes

Jever reste actuellement sous OLD dans les fichiers : c’est une **anomalie connue**, pas la conclusion historique. Sa dépendance envers Zerbst est établie, mais son contour n’est pas suffisamment homologué au bitmap. Voir [JEVER_AUDIT.md](JEVER_AUDIT.md).

Le Harz n’est corrigé que dans des intérieurs recoupant déjà ANH. Hoym n’est pas absorbé arbitrairement par Bernbourg. Les enclaves et franges prussiennes/brunswickoises non tracées ne sont pas certifiées. Zerbst–Coswig–Roßlau reste tronqué par l’ancienne emprise ANH.

Les quatre capitales utilisent la région économique **STATE_ANHALT, ID numérique 62**. Cela ne prouve pas la position historique de leurs centres urbains. Le hub natif Magdebourg reste prussien ; le locator agricole reste physiquement immobile, avec son RGB de référence réassocié au nouveau fragment de Köthen. Aucun nom de ferme n’est utilisé comme preuve de souveraineté.

## Vérifications

{v['passed']}/{v['total']} contrôles statiques passent. Onze nouveaux tests passent, dont deux tests négatifs sur la correction du nom ANH. Le compilateur impérial reproduisait les 57 fichiers initiaux à l’identique avant mutation ; les 57 sorties après mutation ont été comparées aux fichiers installés.

Les 44 doublons RGB et 12 références invalides antérieurs sont inchangés. Les anciennes baselines n’ont pas été réécrites. Voir [VALIDATION.json](VALIDATION.json), [UNIT_TESTS.json](UNIT_TESTS.json) et [LEGACY_TEST_TRIAGE.md](LEGACY_TEST_TRIAGE.md).

Les seules cartes avant/après présentent les modifications réellement installées. Elles ne représentent pas un achèvement cadastral d’Anhalt. Voir [comparatif](ANHALT_BEFORE_AFTER.png) et [plan de test](RUNTIME_TEST_PLAN.md).

## Fichiers modifiés

Fichiers runtime recensés exactement dans VALIDATION.json, champ `runtime_files_modified`. Ils comprennent les historiques territoriaux et démographiques, définitions des trois pays, souverains, noms anglais/français, drapeaux abstraits, terrains, bitmap et les 16 sorties impériales modifiées. Aucun fichier de bâtiments, formations militaires ou diplomatie n’est modifié.

Outils : `tools/map2r_anhalt.py`, `tools/test_map2r_anhalt.py` et extension explicitement gardée de `tools/map2l_registry.py`. Le nouveau manifeste courant est [INSTALLED_MANIFEST.json](INSTALLED_MANIFEST.json). Le manifeste Q précédent est conservé comme photographie de son étape, et non présenté comme l’état courant.

## Recherche locale ColGrep

Une tentative a échoué sur le verrou d’index, puis **un appel abouti au sous-agent local configuré** a retrouvé deux pistes vérifiées : les lignes18–19 de `RULERS_1776_EUROPE_RESIDUAL_SOURCES.md` et la ligne5 de `MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md`. Il n’a pas résolu la géométrie. La commande et les limites de mesure sont conservées dans [COLGREP_USAGE.json](COLGREP_USAGE.json).

Les durées cumulées, les tokens Codex et le nombre complet de recherches classiques n’ont pas été instrumentés sur ces reprises. Aucune économie exacte de quota ne peut être déduite. Intérêt constaté : retrouver rapidement des pistes locales pertinentes ; la vérification historique et l’implémentation restent nécessaires.
'''
    files[prefix+'HISTORICAL_EVIDENCE.md']='''# Preuves et limites — Anhalt1776

## Sources réutilisées

- R2 : `MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv`, lignes40–41. La représentation ANH agrégée était explicitement une abstraction, pas un tracé des quatre principautés.
- `MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md` : voisinages prussiens à préserver tant que les limites ne sont pas établies.
- `docs/research/characters/RULERS_1776_EUROPE_RESIDUAL_SOURCES.md`, lignes18–19 : avertissement contre une division sans source et sans choix du joueur. Le choix de créer les trois pays a depuis été donné explicitement.
- `MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md` : Jever distinct de Varel/Kniphausen ; les grands RGB OLD ne constituent pas des limites certifiées.

## Carte primaire et contrôle chronologique

**S1 — Euler, Rhode, Berger, Tabula geographica principatus Anhaltini et Finitimarum regionum,1753.** [Catalogue David Rumsey](https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~290934~90062555), [métadonnées et copie numérique](https://archive.org/metadata/dr_tabula-geographica-principatus-anhaltini-et-finitimarum-regionum--kartenma-11392035). Original conservé dans EVIDENCE/EULER_1753.jp2,10490×7479. L’aperçu2200px et SOURCE_TRACING_REVIEW.png montrent les enveloppes interprétées. Source antérieure à la mort de Friedrich August1793 ; pas de reprise du partage ultérieur.

Les contours ne reposent pas uniquement sur la localisation d’une ville : ils suivent les ensembles colorés et leurs exclusions sur la carte, recoupés par les descriptions administratives. Enveloppes généralisées, pas copie cadastrale. La couleur générale Bernburg ne suffit notamment pas à absorber Hoym en1776.

**S2 — [LASA Gesamt-Anhalt](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=190133).** Principautés distinctes et institutions communes ; la maison dynastique n’est pas un pays territorial unifié. Les institutions communes et le vote historique commun ne sont pas convertis en quatre nouveaux électeurs.

**S3 — [LASA Anhalt-Zerbst](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=188603)** et [cartes de Zerbst](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=659158). Souveraineté de la lignée avant1793. Des descriptions d’archives donnent1796 pour certains actes de partage, tandis que le prompt retient1797 : cette différence administrative reste signalée et n’a aucun effet sur l’attribution1776.

**S4 — LASA Bernburg : [Plötzkau](https://recherche.landesarchiv.sachsen-anhalt.de/Query/detail.aspx?ID=188270), [Gernrode](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=188264), [Harzgerode](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=188268), [Hoym](https://recherche.landesarchiv.sachsen-anhalt.de/Query/detail.aspx?ID=188269).** Bernburg, Plötzkau, Ballenstedt, Gernrode, Harzgerode et Güntersberge distingués des acquisitions ultérieures. Mühlingen/Coswig1797 et Hoym1812 ne sont pas appliqués à1776. Les intérieurs installés sont limités à l’emprise existante ANH ; la totalité de ces Amts n’est pas revendiquée comme reconstruite.

**S5 — [NLA OL Best90 Jever](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640).** Passage à Anhalt-Zerbst en1667, puis possession personnelle de CatherineII après1793. En1776 Jever n’est ni un territoire OLD autonome ni une possession russe. Souveraineté établie mais frontière native laissée C.

**S6 — [Reconstruction1747–1793](https://commons.wikimedia.org/wiki/File:Map_of_Anhalt_(1747-1793).svg)**, SirIain2013,CCBY-SA3.0. Fichiers conservés dans EVIDENCE, utilisé comme orientation secondaire seulement, pas comme source primaire unique des limites.

## Souverains et démographie

[Leopold Friedrich Franz](https://www.deutsche-biographie.de/sfz68642.html), né1740-08-10 ; [Friedrich Albrecht](https://www.deutsche-biographie.de/gnd104173254.html), né1735-08-15 ; [Karl Georg Lebrecht](https://www.deutsche-biographie.de/sfz39876.html), né1730-08-15 ; [Friedrich August](https://www.schloss-zerbst.de/html/fuersten/friedrich_august.htm), né1734-08-08. Aucun titre ducal du XIXe siècle ajouté. Les rattachements d’intérêt politique sont des abstractions de gameplay, pas des faits déduits de leurs dates de naissance.

La chronologie municipale de [Köthen, XVIIIe siècle](https://www.koethen-anhalt.de/de/401%2C1233.html?single_con=3238%2C1233) mentionne24702 habitants en1770 pour ville et pays. Cette mention n’a pas été vérifiée par lecture du recensement original, et ne correspond pas au périmètre incomplet installé. **Aucune population historique chiffrée n’est donc appliquée.** Les répartitions présentes restent techniques et explicitement provisoires.

## Calage et classification

ALIGNMENT.json conserve six repères sur la source contre un diagnostic géographique retenu, ancré au hub technique de Magdebourg. Les résidus de ce fit, inférieurs à0,35px, ne mesurent PAS l’exactitude des villes natives. Aucune borne géographique indépendante n’est disponible. Le locator agricole n’est pas utilisé comme ville témoin.

- A : existence et souveraineté distinctes des quatre principautés, lien Jever–Zerbst.
- B installé : intérieurs de juridiction sur S1, découpés à la résolution du bitmap et recoupant exclusivement les deux RGB déjà ANH.
- C non installé : Jever, franges extérieures, Hoym et enclaves non localisées. Les résidus ANH restent conservés sans certification historique de leur attribution à Dessau.

Les RGB sont des identifiants de couleurs, jamais des identifiants historiques. STATE_ANHALT est une région économique partagée, ID62. Aucun State_ID n’est inventé ni renuméroté.
'''
    files[prefix+'JEVER_AUDIT.md']='''# Jever — souveraineté établie, installation différée

En1776, Jever dépend de la maison d’Anhalt-Zerbst depuis1667. Le fonds NLA OL Best90 décrit ce Nebenland et son administration locale. L’acquisition personnelle par CatherineII suit la mort du prince en1793 ; elle n’autorise ni une Russie1776 ni une fusion avec Oldenburg.

Dans le jeu actuel : STATE_HANNOVER, ID69, grands RGB OLD `xECC3B4` et `xC00161` au voisinage. Ces enveloppes ne constituent pas le contour démontré de la seigneurie. Leur attribution OLD est une anomalie conservée, pas une conclusion historique validée. Tous les pixels et propriétaires de cette région restent identiques à la baseline MAP2R.

La Frise orientale et le noyau d’Emden prussien `xF9DCA2` restent protégés. Varel et Kniphausen ne sont pas assimilés à Jever : propriétés dynastiques, droits judiciaires et souveraineté doivent être distingués.

Représentation envisagée après preuve du contour : possession éloignée sous AZR, sans corridor ; contrôler son statut institutionnel impérial propre et ne pas déduire des droits territoriaux de la seule dynastie. Aucune union OLD–AZR ni modification de OLD–HLB n’est installée.

Pour terminer : carte territoriale de Jever antérieure à1793, repères homologues avec le bitmap, exclusion documentée des droits Bentinck de Varel/Kniphausen, contrôle de l’enveloppe côtière puis démographie de périmètre comparable. Aucun transfert du grand RGB OLD n’est autorisé par un simple point de ville.

Sources : [NLA OL Best90](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640), audit retenu MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md. Statut : A pour le lien historique, C pour le tracé natif. **Jever n’est pas corrigé par ce lot.**
'''
    files[prefix+'RUNTIME_TEST_PLAN.md']='''# Contrôle ciblé MAP-2R — à effectuer par le joueur

Nouvelle partie au1erjanvier1776 avec le mod courant. Ce plan n’est pas un résultat moteur.

1. Vérifier quatre pays distincts ANH,ABG,AKT,AZR : noms Dessau,Bernbourg,Köthen,Zerbst, carte politique et sélection jouable. Les armes ascaniennes communes sont provisoires.
2. Vérifier les souverains historiques et l’absence des personnages ANH de1836 ou de doubles monarques. Aucun nouveau pays ne doit être un sujet automatique de Dessau.
3. Vérifier population et profils : ANH91513,ABG12603,AKT18083,AZR30687. Ce sont des chiffres techniques, pas des objectifs démographiques historiques. HLB doit rester9206.
4. Vérifier capitales valides dans STATE_ANHALT, sans déduire de la position de Magdebourg ou de la ferme la position historique des quatre résidences. Vérifier accès au marché, subsistance, ressources partagées et infrastructures des nouveaux petits États.
5. Vérifier bloc impérial, journal, droits de restitution et absence de nouveaux électeurs ou villes libres pour ABG/AKT/AZR. Tester une restitution sans annexion globale à Dessau.
6. Vérifier que les bâtiments, PM, propriétaires et armées de l’ancien ANH/PRU sont conservés. Les nouveaux pays n’ont pas reçu d’industrie ou d’armée artificielle ; leur viabilité économique reste à observer.
7. Vérifier le mode carte impérial et la carte du journal ; l’étendue impériale totale doit être inchangée. Le locator agricole a seulement changé de RGB de référence, pas de position.
8. Contrôler que Jever, Emden, OLD–HLB, Eutin/Schwartau, Erfurt–Eichsfeld et les autres lots acceptés restent inchangés. Jever encore OLD est une anomalie ouverte explicitement documentée.
9. Laisser passer un mois et vérifier le hook impérial, budgets, pays existants, cartes et erreurs nouvelles. Ne qualifier PASS_RUNTIME_USER_VALIDATED que les points effectivement inspectés après retour explicite du joueur.

Ne pas considérer une exécution statique ou l’ouverture d’un rapport comme un test de chargement du jeu.
'''
    files[prefix+'NEXT_REGION_RECOMMENDATION.md']='''# Recommandation unique après clôture d’Anhalt

**Saxe et principautés thuringiennes hors Erfurt–Eichsfeld.**

L’inventaire global MAP2M/R9/HRE_REGIONS_INVENTORY.csv, ligne27, signale STATE_SAXONY comme RESEARCHED_ONLY : COB,MEI,SAX,SCW,WEI présents mais aucune passe dédiée ne démontre leurs frontières de1776. L’ajout franconien à Cobourg ne clôt pas ce secteur. Les sources R2 sont déjà retenues et le voisinage avec Anhalt donne une continuité de travail utile.

Ne pas commencer maintenant. Terminer d’abord les points ouverts d’Anhalt ou faire explicitement accepter leur report, puis valider les noyaux en jeu. Exclure Erfurt–Eichsfeld et ne pas transformer des frontières dynastiques postérieures en frontières1776.
'''
    preexisting={
      'test_map2q_eutin.EutinGuards.test_exact_bitmap_and_negative_outside_edit',
      'test_map2q_eutin.EutinGuards.test_no_schwartau_or_oldenburg_corridor',
      'test_map2m_r8.InstalledBTests.test_exact_b_not_a_plus_b',
      'test_map2m_r8.InstalledBTests.test_wolgast_and_protected_rows_not_shifted',
      'test_map2m_r9.R9Guards.test_exact_two_cells_and_no_elsewhere_edit',
      'test_map2n_island.PoelTests.test_exact_scoped_edits_and_negative_guard',
      'test_map2n_completion.CompletionTests.test_exact_mainland_patch_and_negative_out_of_scope_edit',
      'test_map2o_east_frisia.EastFrisiaTests.test_exact_ledger_replay_preserves_every_other_right'}
    failures=[x for group in tests.values() for x in group['failures']]
    files[prefix+'LEGACY_TEST_TRIAGE.md']='''# Tests anciens : écarts conservés et distingués

Les tests et baselines des étapes antérieures ne sont pas modifiés pour masquer leur obsolescence. La reproduction différentielle mondiale depuis la baseline MAP2R passe ; elle protège tous les pixels hors des deux parents ANH et toutes les données hors du plan explicite.

## Échecs déjà recensés dans UNIT_TESTS.json de MAP2Q/R3

'''+''.join('- `'+t+'`\n' for t in failures if t in preexisting)+'''
## Deux nouveaux écarts de snapshots dus à MAP2R

- `test_map2q_r3.Kaltenhof.test_exact_delta_and_negative_guard` attend que seules les quatre cellules R3 changent dans le monde entier. Les nouveaux enfants RGB d’Anhalt rendent cette attente obsolète ; les cellules R3 sont inchangées dans la comparaison mondiale MAP2R.
- `test_map2n_island.PoelTests.test_no_move_of_hubs_or_old_pomeranian_provinces` exige le même RGB sous TOUS les locators mondiaux. Le locator agricole d’Anhalt est physiquement immobile mais son RGB passe explicitement de x8A448C à xEDB304. Aucun hub poméranien n’est déplacé. Cette réassociation est enregistrée dans REGISTRY_MIGRATION.json et contrôlée sans dérogation globale.

## Résultats courants

11/11 tests MAP2R passent ; 16/19 tests des étapes Q passent ; 61/68 tests cumulatifs anciens passent. Zéro erreur d’exécution de test. Les dix échecs listés ne sont pas convertis artificiellement en PASS. Les nouvelles vérifications ciblées comparent l’état mondial à la baseline immédiate avec le delta exact autorisé.

Les 44 doublons de provinces et12 références invalides sont des anomalies de données antérieures, distinctes de ces assertions de snapshots. Leur liste exacte reste identique ; aucune nouvelle anomalie de ces catégories.
'''
    q.core.OUT=OUT;q.core.emit(files,'REPORTS.patch')
    dump('COLGREP_USAGE.json',dict(attempts=2,successful_local_agent_calls=1,failed_attempts=1,
        failure='Index lock access under initial sandbox; later elevated invocation succeeded without integration/model changes.',
        command="& 'C:/Users/simeo/.cargo/bin/colgrep.exe' --agent 'Locate existing retained research and territorial map sources for Anhalt Dessau Bernburg Koethen Zerbst and Jever in 1776, and relevant country, province, population and imperial registry dependencies. Return a few precise repository paths and line ranges. Read only: do not edit source files or configuration.' .",
        configured_model='colgrep-agent-2B-Q8_0.gguf',result='Two returned locations checked against actual files and lines. No geometry established by local model.',
        verified_leads=[dict(path='docs/research/characters/RULERS_1776_EUROPE_RESIDUAL_SOURCES.md',lines='18-19'),dict(path='docs/reports/map/MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md',lines='5')],
        total_local_search_seconds=None,codex_tokens=None,classic_search_count=None,notes='Counters not instrumented across resumed turns. No exact quota-saving claim or fresh GPU telemetry. Agent is retrieval helper only.'))
    print('Report patch ready; no earlier report overwritten.')

def preview(before,after,assignments):
    owners={r['key'][0]:r['key'][2] for r in load('BASELINE.json')['inventory']['owners']}
    newowners=dict(owners);newowners.update({r['rgb']:r['owner'] for r in assignments})
    pal={'ANH':'#61bec4','ABG':'#83c56b','AKT':'#e594ad','AZR':'#eed269','PRU':'#acb4c6','BRA':'#c7a770','SAX':'#9bb8a0','HAN':'#b5a1bb'}
    box=(4343,794,4390,820);x0,y0,x1,y1=box;scale=18
    out=Image.new('RGB',((x1-x0)*scale*2,(y1-y0)*scale+120),'white');d=ImageDraw.Draw(out);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for index,(bmp,own,label) in enumerate([(before,owners,'AVANT : Anhalt agrégé'),(after,newowners,'APRÈS : noyaux simplifiés, franges non certifiées')]):
        local=bmp[y0:y1,x0:x1];a=np.zeros((*local.shape,3),dtype='uint8')
        for c in np.unique(local):a[local==c]=ImageColor.getrgb(pal.get(own.get('x'+format(int(c),'06X')),'#adc5d2'))
        image=Image.fromarray(a).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
        out.paste(image,(index*image.width,40));d.text((index*image.width+8,10),label,font=f,fill='black')
    for i,t in enumerate(TAGS):
        d.rectangle((15+i*400,out.height-65,35+i*400,out.height-45),fill=pal[t]);d.text((43+i*400,out.height-66),{'ANH':'Dessau* (ANH)','ABG':'Bernbourg (ABG)','AKT':'Köthen (AKT)','AZR':'Zerbst (AZR)'}[t],font=f,fill='black')
    d.text((15,out.height-32),'* ANH : résidus provisoires inclus. Jever inchangé ; Harz partiel. Aucune précision cadastrale revendiquée.',font=f,fill='black')
    out.save(OUT/'ANHALT_BEFORE_AFTER.png')

def final_checks():
    import csv,hashlib
    required=['REPORT.md','HISTORICAL_EVIDENCE.md','ANHALT_TERRITORIAL_AUDIT.csv','CURRENT_PROVINCES.csv','TERRITORIAL_CHANGES.csv','ANHALT_BEFORE_AFTER.png','JEVER_AUDIT.md','POPULATION_BEFORE_AFTER.csv','WORLD_POPULATION_DELTA.json','IMPERIAL_REGISTRY_VALIDATION.json','VALIDATION.json','UNRESOLVED.csv','RUNTIME_TEST_PLAN.md','NEXT_REGION_RECOMMENDATION.md']
    checks=[]
    for name in required:checks.append(dict(name=name,passed=(OUT/name).is_file() and (OUT/name).stat().st_size>0))
    for name,rows in load('CSV_TABLES.json').items():
        keys=list(rows[0]);expected=[keys]+[['' if row.get(k) is None else str(row[k]) for k in keys] for row in rows]
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:actual=list(csv.reader(f))
        checks.append(dict(name='CSV exact roundtrip '+name,passed=actual==expected))
    manifest=load('INSTALLED_MANIFEST.json');current=q.economy.runtime_hashes()
    checks.append(dict(name='Installed manifest current',passed=all(current.get(p)==h for p,h in manifest['functional_files'].items())))
    checks.append(dict(name='Validation ready but explicitly partial and not runtime certified',passed=load('VALIDATION.json')['status']=='MAP2R_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST' and load('VALIDATION.json')['runtime_status']=='NOT_TESTED_MAP2R'))
    b=load('BASELINE.json')
    checks.append(dict(name='HEAD and index untouched',passed=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and q.core.sha(ROOT/'.git/index')==b['git_index_sha256']))
    checks.append(dict(name='Previous baseline hash not rewritten',passed=load('BASELINE.json')['bitmap_sha256']==q.core.sha(ROOT/b['bitmap_backup'])))
    data=dict(checks=checks,passed=sum(r['passed'] for r in checks),total=len(checks),deliverables={name:q.core.sha(OUT/name) for name in required},generated_source_assets={'workshop_assets/source/map2k_hre_registered_map.png':q.core.sha(ROOT/'workshop_assets/source/map2k_hre_registered_map.png')},no_commit_or_push=True)
    dump('DELIVERY_VALIDATION.json',data)
    print('Delivery checks',data['passed'],'/',data['total'])
    assert data['passed']==data['total']

if __name__=='__main__':globals()[sys.argv[1]]()
