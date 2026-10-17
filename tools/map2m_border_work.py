"""MAP-2M: independent Peene and Netze candidates; immutable local baselines."""
import csv,json,re,sys,time,urllib.request
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2l_prussian_borders as previous
import map2l_mainz as core

ROOT=core.ROOT
BASE=ROOT/'docs/reports/map/MAP2M'
PREVIOUS=previous.OUT

def configure(sector):
    core.OUT=BASE/sector
    core.OUT.mkdir(parents=True,exist_ok=True)
    core.REGIONS={'STATE_POMERANIA'} if sector=='PEENE' else {'STATE_POSEN'}
    core.REGION_FILE='map_data/state_regions/'+('00_west_europe.txt' if sector=='PEENE' else '02_east_europe.txt')
    # Both independent diagnostic baselines reference the accepted MAP-2L
    # bitmap. An unapproved proposal must never become the next baseline.
    core.BACKUP=PREVIOUS/'provinces_candidate.png'
    for name in ['PREPARE_EXTRA_FILES','POPULATION_ALLOCATION_WEIGHTS','BUILDING_ALLOCATION_WEIGHTS']:
        if hasattr(core,name):delattr(core,name)
    return core.OUT

def audit():
    """Read actual RGB/owner data, not the older atlas's named locators."""
    BASE.mkdir(parents=True,exist_ok=True)
    inv=core.qa.inventory();bmp=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in inv['owners']}
    rows=[]
    for rgb,(sid,tag) in owners.items():
        if sid not in {'STATE_POMERANIA','STATE_WEST_PRUSSIA','STATE_POSEN','STATE_BRANDENBURG'}:continue
        y,x=np.where(bmp==int(rgb[1:],16))
        rows.append(dict(RGB=rgb,State_ID=sid,Owner_TAG=tag,cells=len(x),xmin=int(x.min()),xmax=int(x.max()),ymin=int(y.min()),ymax=int(y.max())))
    with (BASE/'CURRENT_PROVINCES.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    river=np.asarray(Image.open(core.qa.GAME/'map_data/rivers.png').convert('RGB'))
    for sector,box in [('PEENE',(4372,711,4442,775)),('NETZE',(4435,740,4550,812))]:
        out=configure(sector);x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),236,dtype=np.uint8)
        for rgb in np.unique(local):
            key='x'+format(int(rgb),'06X');tag=owners.get(key,('',None))[1]
            arr[local==rgb]={'PRU':(145,190,225),'PLC':(220,160,160),'SWE':(235,205,65),'MEC':(145,185,130),'MST':(145,185,130)}.get(tag,(236,236,236))
        edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];arr[edge]=80
        im=Image.fromarray(arr).resize(((x1-x0)*12,(y1-y0)*12),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
        for rgb in np.unique(local):
            key='x'+format(int(rgb),'06X')
            if key not in owners:continue
            y,x=np.where(local==rgb);d.text((float(x.mean())*12,float(y.mean())*12),key[1:],font=font,fill='black',stroke_width=1,stroke_fill='white')
        for x in range((x0//5+1)*5,x1,5):d.line(((x-x0)*12,0,(x-x0)*12,im.height),fill='#999999');d.text(((x-x0)*12,0),str(x),font=font,fill='black')
        for y in range((y0//5+1)*5,y1,5):d.line((0,(y-y0)*12,im.width,(y-y0)*12),fill='#999999');d.text((0,(y-y0)*12),str(y),font=font,fill='black')
        im.save(out/'CURRENT_OWNERS.png')
        Image.fromarray(river[y0:y1,x0:x1]).resize(im.size,Image.Resampling.NEAREST).save(out/'NATIVE_RIVERS.png')
    print('Audited',len(rows),'actual provinces; bitmap',core.sha(ROOT/'map_data/provinces.png'))

def fetch():
    out=BASE/'EVIDENCE';out.mkdir(parents=True,exist_ok=True)
    sources=[('GRUND_1775_DETAIL.jpg','https://kartenhighlights.staatsbibliothek-berlin.de/wp-content/uploads/SBB_IIIC_Kart_N-10051_Ausschnitt-40000-dpi-scaled.jpg'),('MAYER_BSB_AFTER_1763.jpg','https://api.digitale-sammlungen.de/iiif/image/v2/bsb00074494_00001/full/4000,/0/default.jpg'),('GUESSEFELD_1775.jpg','https://www.e-rara.ch/i3f/v30/29730664/full/4000,/0/default.jpg')]
    results=[]
    for name,url in sources:
        p=out/name
        if not p.exists():
            request=urllib.request.Request(url,headers={'User-Agent':'MAP-2M historical cartography research'})
            content=urllib.request.urlopen(request,timeout=45).read(30000001);assert len(content)<=30000000;p.write_bytes(content)
        results.append(dict(file=name,url=url,sha256=core.sha(p),dimensions=Image.open(p).size))
    (out/'SOURCES.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)

def readings():
    cases=[('GUESSEFELD_1775.jpg','NETZE_1775_READING.png',(180,1790,1850,2560)),('MAYER_BSB_AFTER_1763.jpg','PEENE_BSB_READING.png',(1430,2390,3310,3000))]
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for name,target,box in cases:
        im=Image.open(BASE/'EVIDENCE'/name).convert('RGB').crop(box);d=ImageDraw.Draw(im)
        for x in range((box[0]//100+1)*100,box[2],100):d.line((x-box[0],0,x-box[0],im.height),fill='#6495ed');d.text((x-box[0],2),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):d.line((0,y-box[1],im.width,y-box[1]),fill='#6495ed');d.text((2,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        im.save(BASE/'EVIDENCE'/target)
    Image.open(BASE/'EVIDENCE/GUESSEFELD_1775.jpg').crop((500,2000,1700,2470)).resize((2400,940)).save(BASE/'EVIDENCE/NETZE_TOWNS_DETAIL.png')

def candidates(sector):
    """Unapproved diagnostic only. Does NOT write a runtime/candidate bitmap."""
    out=configure(sector);b=json.loads((out/'BASELINE.json').read_text());bmp=core.packed(ROOT/'map_data/provinces.png')
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    if sector=='PEENE':
        source=PREVIOUS/'EVIDENCE/MAYER_1763_GREIFSWALD.jpg'
        controls=[dict(name='Darss northwestern coastal cape',source=[80,219],target=[4380,724],quality='manually interpreted coastline; not surveyed'),dict(name='Greifswald coastal locality',source=[519,510],target=[4400.235,734.059],quality='native port, not certified historical city centre'),dict(name='Northern Usedom / Peene estuary cape',source=[664,432],target=[4408,732],quality='manual coast identification, not surveyed')]
        polygon=[[0,0],[949,0],[949,420],[664,432],[702,485],[714,530],[701,572],[724,615],[733,674],[722,697],[652,687],[610,673],[570,671],[536,651],[498,619],[458,632],[430,618],[400,619],[378,656],[356,681],[305,690],[270,665],[255,613],[225,595],[190,549],[170,520],[130,452],[105,400],[0,380]]
        parents={'xE1A03A','xA04121'};target='SWE';box=[4372,711,4442,775]
        diagnostic=[dict(name='Northern Ruegen cape: independent coastal interpretation',source=[505,28],reference=[4399,715],quality='manual coastal interpretation, extrapolated; not a surveyed control')]
        issue='Fit triangle lies north of most Peene frontier. Northern Ruegen coast does not agree; Peene/Trebel absent in native hydrography. Peendamm cannot be independently resolved in the bitmap. Do not treat fit residual zero as positional accuracy.'
    else:
        source=BASE/'EVIDENCE/GUESSEFELD_1775.jpg'
        controls=[dict(name='Danzig',source=[1760,1335],target=[4521.545,727.361],quality='native city locator; not independently surveyed'),dict(name='Bromberg',source=[1410,2318],target=[4507.717,767.086],quality='native farm named Bromberg; not certified city centre'),dict(name='Thorn',source=[1680,2395],target=[4519.315,772.105],quality='native farm; read-only alignment control; enclave not altered')]
        polygon=[[490,1930],[600,1955],[800,1965],[900,1920],[1000,1925],[1130,1990],[1170,2095],[1270,2090],[1320,2190],[1410,2195],[1430,2270],[1500,2330],[1510,2400],[1420,2430],[1320,2450],[1220,2430],[1170,2400],[1110,2370],[900,2340],[800,2325],[700,2320],[650,2360],[600,2400],[400,2390],[300,2400],[340,2250],[400,2200],[420,2070]]
        parents={r['key'][0] for r in b['inventory']['owners'] if r['key'][1:]==['STATE_POSEN','PLC']};target='PRU';box=[4435,740,4550,812]
        diagnostic=[]
        issue='Tentative northern district envelope, NOT a verified complete sovereignty boundary. Three eastern locators give no independent western validation; Pila/Walcz extrapolation differs from geographic diagnostic. Southern Inowroclaw county is not justified by the available Grund excerpt or this envelope. Later Toeppen outline not approved as a substitute.'
    matrix=np.linalg.solve(np.array([[*r['source'],1] for r in controls]),np.array([r['target'] for r in controls]))
    for row in diagnostic:
        row['predicted']=(np.array([*row['source'],1])@matrix).tolist();row['difference_px']=float(np.linalg.norm(np.array(row['predicted'])-row['reference']))
    # The native geographic hypothesis is only a cross-model diagnostic,
    # never an independent certified observation of Piła or Wałcz.
    if sector=='NETZE':
        from georeference.model import forward
        model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json').read_text())['model']
        by=forward(model,[[18.008,53.123]])[0];offset=np.array([4507.717,767.086])-by
        for name,point,geo in [('Pila',[819,2180],[16.738,53.151]),('Walcz',[739,2062],[16.475,53.273])]:
            pred=np.array([*point,1])@matrix;reference=forward(model,[geo])[0]+offset
            diagnostic.append(dict(name=name,source=point,predicted=pred.tolist(),reference=reference.tolist(),difference_px=float(np.linalg.norm(pred-reference)),quality='DISAGREEMENT BETWEEN UNVALIDATED MODELS; NOT measured city error'))
    source_sha=core.sha(source)
    cfg=dict(sector=sector,status='NOT_APPROVED_FOR_TERRITORIAL_TRANSFER',source=source.relative_to(ROOT).as_posix(),source_sha256=source_sha,controls=controls,matrix=matrix.tolist(),diagnostics=diagnostic,polygon=polygon,warning=issue,accepted_cells=0)
    core.dump('CANDIDATE_MODEL.json',cfg)
    rows=[];mask=np.zeros(bmp.shape,dtype=bool)
    for own in b['inventory']['owners']:
        rgb,sid,owner=own['key']
        if rgb not in parents:continue
        ys,xs=np.where(bmp==int(rgb[1:],16));cells=np.column_stack((xs,ys));local=(cells+.5-matrix[2])@np.linalg.inv(matrix[:2]);take=core.inside(local,polygon)
        for x,y in cells[take]:
            rows.append(dict(X=int(x),Y=int(y),RGB=rgb,State_ID=sid,Before=owner,Proposed=target,Applied=False,Status='UNVALIDATED_ALIGNMENT_DO_NOT_APPLY',Source=source.relative_to(ROOT).as_posix(),Source_SHA256=source_sha))
            mask[y,x]=True
    with (out/'CANDIDATE_CELLS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['X','Y','RGB','State_ID','Before','Proposed','Applied','Status','Source','Source_SHA256'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    with (out/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerow(['X','Y','RGB_before','RGB_after','State_ID','Owner_before','Owner_after','Source'])
    # Source overlay is explicitly a rejected hypothesis, not an approved trace.
    im=Image.open(source).convert('RGB');d=ImageDraw.Draw(im);d.line([tuple(p) for p in polygon]+[tuple(polygon[0])],fill='red',width=4);d.text((20,20),'UNVALIDATED PROPOSAL - NOT APPLIED',fill='red',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24));im.save(out/'SOURCE_HYPOTHESIS.png')
    x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1];owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};arr=np.full((*local.shape,3),236,dtype=np.uint8)
    for rgb in np.unique(local):
        tag=owners.get('x'+format(int(rgb),'06X'));arr[local==rgb]={'PRU':(145,190,225),'SWE':(235,205,65),'PLC':(220,160,160),'MEC':(145,185,130),'MST':(145,185,130)}.get(tag,(236,236,236))
    edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];arr[edge]=80
    images=[]
    for title,proposal in [('REFERENCE',False),('CANDIDATS NON VALIDES / NON APPLIQUES',True),('APRES EFFECTIF : INCHANGE',False)]:
        view=arr.copy()
        if proposal:view[mask[y0:y1,x0:x1]]=[190,110,220]
        im=Image.fromarray(view).resize(((x1-x0)*8,(y1-y0)*8),Image.Resampling.NEAREST);canvas=Image.new('RGB',(im.width,im.height+40),'white');canvas.paste(im,(0,32));ImageDraw.Draw(canvas).text((8,8),title,fill='black');images.append(canvas)
    combined=Image.new('RGB',(images[0].width*3,images[0].height),'white')
    for i,im in enumerate(images):combined.paste(im,(i*im.width,0))
    combined.save(out/'BEFORE_AFTER.png')
    print(sector,len(rows),'unapproved candidate cells; zero applied;',[(r['name'],round(r['difference_px'],2)) for r in diagnostic])

if __name__=='__main__':
    action=sys.argv[1]
    if action in {'audit','fetch','readings'}:globals()[action]()
    elif action=='capture':configure(sys.argv[2]);core.capture()
    elif action=='candidates':candidates(sys.argv[2])
    else:raise SystemExit('Unknown action')
