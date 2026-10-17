"""Prussian borders in 1776: staged, immutable actual-workspace baseline."""
import csv,json,sys,re,urllib.request
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2l_mainz as core
import map2l_swabia_completion as previous

OUT=core.ROOT/'docs/reports/map/MAP2L/PRUSSIAN_BORDERS'
core.OUT=OUT
core.BACKUP=previous.OUT/'provinces_candidate.png'
CAPTURE_REGIONS={'STATE_POMERANIA','STATE_WEST_PRUSSIA','STATE_EAST_PRUSSIA','STATE_POSEN','STATE_BRANDENBURG','STATE_ANHALT','STATE_BRUNSWICK','STATE_LOWER_SILESIA','STATE_UPPER_SILESIA'}
core.REGIONS={'STATE_POMERANIA'}
if hasattr(core,'PREPARE_EXTRA_FILES'):del core.PREPARE_EXTRA_FILES

def fetch():
    folder=OUT/'EVIDENCE';folder.mkdir(exist_ok=True)
    url='https://www.uni-greifswald.de/storages/uni-greifswald/1_Universitaet/1.3_Einrichtungen/1.3.4._Kustodie/Sammlungsobjekt_des_Quartals/2015_April_Juni_Mayersche_Karte_949x768_300dpi.jpg'
    path=folder/'MAYER_1763_GREIFSWALD.jpg';assert not path.exists()
    data=urllib.request.urlopen(url,timeout=40).read(20000000);path.write_bytes(data)
    core.dump('MAYER_SOURCE.json',dict(url=url,institution='Universitaet Greifswald',author='Andreas Mayer / Tobias Conrad Lotter',date=1763,sha256=core.sha(path),dimensions=Image.open(path).size,catalogue='https://www.uni-greifswald.de/universitaet/einrichtungen/kustodie/wissenschaftliche-sammlungen/sammlungsobjekt-des-quartals/geographische-kartensammlung-die-mayersche-karte/',warning='Municipal internal boundaries omitted; use external jurisdiction and physical coastline/river evidence, not old maps with incorrectly coloured 1720 border'))
    print('Saved',len(data),'bytes',Image.open(path).size)

def fetch_poland():
    sources=[('SCHMETTAU_PRUSSIA.jpg','https://westpreussische-gesellschaft.de/Downloads/Historische_Karten/04-OF_Das-neue-Gebiet-Westpreussen-und-seine-erste-Gliederung_SBB_IIIC_Kart_N-1020_Index.jpg'),('TOEPPEN_NETZE_1772.jpg','https://upload.wikimedia.org/wikipedia/commons/6/66/Netzedistrikt_mit_Kreiseinteilung_1772.jpg')]
    results=[]
    for name,url in sources:
        path=OUT/'EVIDENCE'/name
        if not path.exists():
            req=urllib.request.Request(url,headers={'User-Agent':'MAP2L historical cartography research'})
            data=urllib.request.urlopen(req,timeout=60).read(30000000);path.write_bytes(data)
        results.append(dict(path='EVIDENCE/'+name,url=url,sha256=core.sha(path),size=path.stat().st_size,dimensions=Image.open(path).size))
        print(results[-1])
    core.dump('POLAND_SOURCES.json',results)

def inspect():
    from map2l_belgium import packed
    b=json.loads((OUT/'BASELINE.json').read_text());bmp=packed(core.ROOT/'map_data/provinces.png');rgb=np.asarray(Image.open(core.ROOT/'map_data/provinces.png').convert('RGB'));owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
    rivers=Image.open(core.qa.GAME/'map_data/rivers.png').convert('RGB');river=np.asarray(rivers)
    for name,box in [('POMERANIA',(4370,697,4515,792)),('PRUSSIA_POLAND',(4465,690,4610,825))]:
        x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1];col=rgb[y0:y1,x0:x1];arr=np.full((*local.shape,3),235,dtype=np.uint8)
        colors={'PRU':(146,190,228),'PLC':(221,154,153),'SWE':(235,212,96),'MEC':(149,193,145),'MST':(156,185,137)}
        for val in np.unique(local):
            key='x'+format(int(val),'06X');arr[local==val]=colors.get(owners.get(key,''),(224,224,224))
        edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];arr[edge]=75
        im=Image.fromarray(arr).resize(((x1-x0)*9,(y1-y0)*9),Image.Resampling.NEAREST);draw=ImageDraw.Draw(im)
        for val in np.unique(local):
            key='x'+format(int(val),'06X')
            if key not in owners:continue
            ys,xs=np.where(local==val);point=(int(np.mean(xs)*9),int(np.mean(ys)*9));draw.text(point,key[1:],fill='black',font=font,stroke_width=1,stroke_fill='white')
        for x in range((x0//10+1)*10,x1,10):draw.line(((x-x0)*9,0,(x-x0)*9,im.height),fill=(160,160,160));draw.text(((x-x0)*9,0),str(x),fill='black',font=font)
        for y in range((y0//10+1)*10,y1,10):draw.line((0,(y-y0)*9,im.width,(y-y0)*9),fill=(160,160,160));draw.text((0,(y-y0)*9),str(y),fill='black',font=font)
        im.save(OUT/(name+'_CURRENT.png'))
        Image.fromarray(river[y0:y1,x0:x1]).resize(((x1-x0)*9,(y1-y0)*9),Image.Resampling.NEAREST).save(OUT/(name+'_RIVERS.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:core.dump('NATIVE_ANCHORS.json',[r for r in csv.DictReader(f) if r['State_ID'] in core.REGIONS])
    print('Native river dimensions',rivers.size,'bitmap',bmp.shape)

def reading():
    for name,step in [('MAYER_1763_GREIFSWALD',100),('TOEPPEN_NETZE_1772',100)]:
        im=Image.open(OUT/'EVIDENCE'/(name+'.jpg')).convert('RGB');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
        for x in range(0,im.width,step):
            d.line((x,0,x,im.height),fill=(70,100,220),width=1);d.text((x+2,3),str(x),fill='blue',font=font,stroke_width=1,stroke_fill='white')
        for y in range(0,im.height,step):
            d.line((0,y,im.width,y),fill=(70,100,220),width=1);d.text((2,y+2),str(y),fill='blue',font=font,stroke_width=1,stroke_fill='white')
        im.save(OUT/(name+'_READING.png'))
    Image.open(OUT/'EVIDENCE/MAYER_1763_GREIFSWALD.jpg').crop((270,390,949,752)).resize((2037,1086)).save(OUT/'MAYER_SOUTH_READING.png')

def geometry():
    """Whole existing northern coastal core, not an invented Peene tracing."""
    from map2l_belgium import packed
    b=json.loads((OUT/'BASELINE.json').read_text());bmp=packed(core.ROOT/'map_data/provinces.png')
    assert core.sha(core.ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    ys,xs=np.where(bmp==0x567452);assert len(xs)==341
    assert [r for r in b['inventory']['owners'] if r['key'][0]=='x567452']==[dict(key=['x567452','STATE_POMERANIA','PRU'],count=1)]
    assert len(core.components(bmp==0x567452))==1
    limitations=['Only the existing northern coastal/Ruegen province is reassigned; the remaining mainland frontier to the Peene is NOT completed.','No city locator is used to allocate an entire neighbouring province; source-map jurisdiction, retained R2 evidence and the northern coastal footprint agree on this existing core.','No calibrated historical frontier is asserted. Peene/Trebel are omitted from native hydrography; adjacent xE1A03A and xA04121 remain unchanged pending defensible local source alignment.','Netze district and Thorn are still unresolved and unchanged; Danzig remains Polish.','No new population, building or country; population/older building redistribution is an exact-integer game-scale allocation, not a historical census.']
    tracing=dict(method='Whole existing province jurisdiction correction; no newly drawn historical boundary',calibrated_sources=[dict(key='MAYER_REFERENCE_ONLY',path='EVIDENCE/MAYER_1763_GREIFSWALD.jpg',matrix=[[1,0],[0,1],[0,0]],controls=[],basis='Reference source only. Identity matrix is not a source-to-game calibration and is never used for tracing.')],parents=['x567452'],imperial_owners=['PRU','SWE'],native_anchors='NATIVE_ANCHORS.json',preview_box=[4370,707,4438,775],limitations=limitations)
    core.dump('TRACING.json',tracing)
    core.dump('ALIGNMENT.json',dict(method=tracing['method'],sources=[dict(**s,sha256=core.sha(OUT/s['path'])) for s in tracing['calibrated_sources']],warning=limitations))
    # Binary-identical candidate: ownership is in history, not colour itself.
    core.shutil.copyfile(core.ROOT/'map_data/provinces.png',OUT/'provinces_candidate.png')
    row=dict(rgb='x567452',parent_rgb='x567452',state='STATE_POMERANIA',previous_owner='PRU',owner='SWE',pixels=341,cells=[[int(x),int(y)] for y,x in zip(ys,xs)],source_zone=1)
    core.dump('GEOMETRY.json',dict(status='PARTIAL_SWEDISH_POMERANIA_NORTHERN_CORE',parents=['x567452'],assignments=[row],new_provinces=[],hub_rebindings=[],transfers={'STATE_POMERANIA/PRU->SWE':341},candidate_sha256=core.sha(OUT/'provinces_candidate.png'),tracing_sha256=core.sha(OUT/'TRACING.json'),changed_pixels=0,limitations=limitations))
    previews=[]
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    local=bmp[707:775,4370:4438]
    for title,after in [('BEFORE',False),('AFTER',True)]:
        arr=np.full((*local.shape,3),235,dtype=np.uint8)
        for rgb in np.unique(local):
            key='x'+format(int(rgb),'06X');tag='SWE' if after and key=='x567452' else owners.get(key)
            arr[local==rgb]={'PRU':(130,175,220),'SWE':(235,205,60),'MEC':(150,190,135),'MST':(150,190,135)}.get(tag,(235,235,235))
        edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];arr[edge]=80
        im=Image.fromarray(arr).resize((680,680),Image.Resampling.NEAREST);canvas=Image.new('RGB',(680,730),'white');canvas.paste(im,(0,40));d=ImageDraw.Draw(canvas);d.text((10,8),title+' / x567452: '+('SWE' if after else 'PRU'),fill='black');d.text((10,712),'Blue: Prussia / Gold: Sweden / Green: Mecklenburg. Mainland fringe unchanged.',fill='black');canvas.save(OUT/(title+'.png'));previews.append(canvas)
    both=Image.new('RGB',(1360,730),'white');both.paste(previews[0]);both.paste(previews[1],(680,0));both.save(OUT/'BEFORE_AFTER.png')
    print('Prepared existing coastal core: 341 ownership cells PRU -> SWE; no raster edits')

def extra(files,migration):
    migration['external_territorial_holders']={'SWE':['STATE_POMERANIA']}
    basis='MAP2L PRUSSIAN_BORDERS: R2 and Mayer 1763 support the existing northern coastal core; no new frontier tracing; mainland incomplete; see REPORT.md.'
    for row in migration['updated']:
        if row['rgb']=='x567452':row['basis']=basis
    registry=core.active_registry_path().relative_to(core.ROOT).as_posix()
    rows=json.loads(files[registry])
    for row in rows:
        if row['rgb']=='x567452':row['basis']=basis
    files[registry]=json.dumps(rows,ensure_ascii=False,indent=2)
    for rel,raw in list(files.items()):
        if rel.startswith(('common/history/states/','common/history/buildings/','common/history/pops/')):
            n=core.state(raw,'STATE_POMERANIA')
            clean=re.sub(r'(?m)^[ \t]+$','',raw[n.start:n.end])
            files[rel]=core.edits(raw,[(n.start,n.end,clean)])
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

def prepare():
    core.PREPARE_EXTRA_FILES=extra
    # Preserve the explicitly requested recent Prussian economic tweaks on
    # their remaining Prussian state subdivision, rather than gifting them.
    b=json.loads((OUT/'BASELINE.json').read_text())
    assert core.sha(core.ROOT/'common/history/states/00_states.txt')==b['hashes']['common/history/states/00_states.txt'],'Prepare only against the immutable pre-install history, not an already-applied lot'
    core.BUILDING_ALLOCATION_WEIGHTS={}
    for rel in b['originals']:
        if 'PRUSSIAN_INDUSTRY_ADDON' in rel:continue
        if rel.startswith('common/history/buildings/') and ('prussian' in rel or 'prussia' in rel):
            try:n=core.region(b['originals'][rel],'STATE_POMERANIA','PRU')
            except StopIteration:continue
            for v in n.children('create_building'):
                core.BUILDING_ALLOCATION_WEIGHTS[rel,'STATE_POMERANIA','PRU',core.cw.scalar(v.one('building'))]={'PRU':1}
    core.prepare()
    # With no RGB subdivision, retain terrain bytes exactly, including EOF.
    if not json.loads((OUT/'GEOMETRY.json').read_text())['new_provinces']:
        source=previous.OUT/'province_terrains_candidate.txt'
        assert core.sha(source)==b['hashes']['map_data/province_terrains.txt']
        core.shutil.copyfile(source,OUT/'province_terrains_candidate.txt')

def capture():
    core.REGIONS=CAPTURE_REGIONS
    core.capture()

if __name__=='__main__':{'capture':capture,'fetch':fetch,'fetch-poland':fetch_poland,'inspect':inspect,'reading':reading,'geometry':geometry,'prepare':prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps}[sys.argv[1]]()
