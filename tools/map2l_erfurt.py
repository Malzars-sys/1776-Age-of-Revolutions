"""Erfurt/Eichsfeld: staged source and native physical calibration review."""
import csv
import json
import sys
import io
import struct
import urllib.request
import re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/ERFURT_EICHSFELD'
core.OUT=OUT
core.BACKUP=OUT.parent/'MILAN_CREMONESE/provinces_candidate.png'
core.REGIONS={'STATE_HESSE','STATE_HANNOVER','STATE_BRUNSWICK','STATE_ANHALT','STATE_SAXONY'}

def catalogue():
    url=sys.argv[2];name=sys.argv[3]
    assert re.fullmatch(r'[A-Z0-9_]+',name)
    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (historical cartographic research)'})
    with urllib.request.urlopen(request,timeout=30) as response:data=response.read(4_000_001)
    assert len(data)<=4_000_000
    target=OUT/(name+'.html')
    if target.exists():assert target.read_bytes()==data,'Retained source changed; do not overwrite'
    else:target.write_bytes(data)
    core.dump(name+'.METADATA.json',dict(url=url,sha256=core.sha(target),bytes=len(data)))
    raw=data.decode('utf-8','replace')
    for match in re.finditer(r'iiif|manifest|14659|1789|[.]jpg|tile|canvas|e-rara|image-server|image_server|ryh_\d+',raw,re.I):
        print(re.sub(r'\s+',' ',raw[max(0,match.start()-180):match.end()+220]))

def texture_mip():
    """Decode a native DDS reduced-resolution mip, avoiding full 8k decode."""
    for name in ['flatmap','flatmap_overlay']:
        path=core.qa.GAME/f'gfx/map/textures/{name}.dds'
        with path.open('rb') as source:
            header=bytearray(source.read(128));assert header[:4]==b'DDS '
            height,width=struct.unpack_from('<II',header,12);mips=struct.unpack_from('<I',header,28)[0]
            fourcc=bytes(header[84:88]);extra=source.read(20) if fourcc==b'DX10' else b''
            if fourcc==b'\x00\x00\x00\x00':
                bits,*masks=struct.unpack_from('<5I',header,88)
                assert bits==32 and masks==[0xff0000,0xff00,0xff,0xff000000],(bits,masks)
                offset=128;w,h=width,height;level=0
                while w>2048 and level+1<mips:
                    offset+=w*h*4;w=max(1,w//2);h=max(1,h//2);level+=1
                assert w<=2048
                source.seek(offset);data=np.frombuffer(source.read(w*h*4),dtype=np.uint8).reshape(h,w,4)
                Image.fromarray(data[:,:, [2,1,0]]).save(OUT/(name+'_MIP.png'))
                print(name,'uncompressed BGRA source',width,height,'mip',level,'derived',w,h)
                continue
            block=8 if fourcc==b'DXT1' else 16
            if fourcc==b'DX10':
                dxgi=struct.unpack_from('<I',extra)[0]
                assert dxgi in [71,72,74,75,77,78,98,99],dxgi
                block=8 if dxgi in [71,72] else 16
            else:assert fourcc in [b'DXT1',b'DXT3',b'DXT5'],fourcc
            offset=128+len(extra);w,h=width,height;level=0
            while w>2048 and level+1<mips:
                offset+=max(1,(w+3)//4)*max(1,(h+3)//4)*block;w=max(1,w//2);h=max(1,h//2);level+=1
            assert w<=2048,'No safely small mip; use a dedicated decoder instead'
            source.seek(offset);data=source.read(max(1,(w+3)//4)*max(1,(h+3)//4)*block)
        struct.pack_into('<II',header,12,h,w);struct.pack_into('<I',header,28,1)
        image=Image.open(io.BytesIO(bytes(header)+extra+data)).convert('RGB')
        image.save(OUT/(name+'_MIP.png'))
        print(name,'source',width,height,'fourcc',fourcc,'mip',level,'derived',w,h)

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=[r for r in csv.DictReader(f) if r['State_ID'] in core.REGIONS|{'STATE_ELBE','STATE_WESTPHALIA'}]
    core.dump('NATIVE_ANCHORS.json',rows)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    bbox=(4288,785,4383,850)
    for name,path in [('RIVERS',core.qa.GAME/'map_data/rivers.png'),('RGB',core.ROOT/'map_data/provinces.png')]:
        image=Image.open(path).convert('RGB').crop(bbox).resize(((bbox[2]-bbox[0])*14,(bbox[3]-bbox[1])*14),Image.Resampling.NEAREST)
        draw=ImageDraw.Draw(image)
        for x in range(4290,bbox[2],5):
            draw.line(((x-bbox[0])*14,0,(x-bbox[0])*14,image.height),fill='#777777');draw.text(((x-bbox[0])*14+2,0),str(x),font=font,fill='black',stroke_width=1,stroke_fill='white')
        for y in range(785,bbox[3],5):
            draw.line((0,(y-bbox[1])*14,image.width,(y-bbox[1])*14),fill='#777777');draw.text((0,(y-bbox[1])*14+2),str(y),font=font,fill='black',stroke_width=1,stroke_fill='white')
        image.save(OUT/(name+'_GRID.png'))
    assessment=json.loads((OUT.parent/'MAINZ_COMPLETION/NORTHERN_CALIBRATION_ASSESSMENT.json').read_text())
    points=assessment['city_fit']+assessment['city_checks'][:2]
    # Empirical cylindrical/Miller hypothesis; not asserted as the engine's CRS.
    coords=np.array([r['geo'] for r in points]);native=np.array([r['native'] for r in points])
    projected=np.column_stack((np.radians(coords[:,0]),1.25*np.log(np.tan(np.pi/4+.4*np.radians(coords[:,1])))))
    matrix=np.linalg.lstsq(np.column_stack((projected,np.ones(len(points)))),native,rcond=None)[0]
    core.dump('MILLER_HYPOTHESIS.json',dict(status='DIAGNOSTIC_NOT_APPROVED',controls=points,matrix=matrix.tolist(),residuals=np.linalg.norm(np.column_stack((projected,np.ones(len(points))))@matrix-native,axis=1).tolist()))
    print(json.dumps(dict(matrix=matrix.tolist(),controls=[dict(name=r['name'],residual=float(e)) for r,e in zip(points,np.linalg.norm(np.column_stack((projected,np.ones(len(points))))@matrix-native,axis=1))]),ensure_ascii=False))

def rivers():
    source=core.ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'
    matrix=np.array(json.loads((OUT/'MILLER_HYPOTHESIS.json').read_text())['matrix'])
    native=Image.open(core.qa.GAME/'map_data/rivers.png').convert('RGB')
    bbox=(4280,760,4420,860);scale=9
    arr=np.array(native)[bbox[1]:bbox[3],bbox[0]:bbox[2]]
    river=np.any(arr<250,axis=2)&~np.all(arr==[128,128,128],axis=2)
    yy,xx=np.where(river);pixels=np.column_stack((xx+bbox[0]+.5,yy+bbox[1]+.5))
    image=native.crop(bbox).resize((140*scale,100*scale),Image.Resampling.NEAREST);draw=ImageDraw.Draw(image)
    metrics=[]
    for name in ['Weser','Elbe']:
        segments=[r['geometry']['coordinates'] for r in json.loads(source.read_text())['features'] if r['properties'].get('name')==name]
        coords=np.array([p[:2] for seg in segments for p in seg]);coords=coords[(coords[:,0]>=8)&(coords[:,0]<=14)&(coords[:,1]>=50)&(coords[:,1]<=53)]
        projected=np.column_stack((np.radians(coords[:,0]),1.25*np.log(np.tan(np.pi/4+.4*np.radians(coords[:,1]))),np.ones(len(coords))))@matrix
        take=(projected[:,0]>=bbox[0])&(projected[:,0]<bbox[2])&(projected[:,1]>=bbox[1])&(projected[:,1]<bbox[3]);coords=coords[take];projected=projected[take]
        distances=np.sqrt(((projected[:,None,:]-pixels[None,:,:])**2).sum(axis=2)).min(axis=1)
        metrics.append(dict(name=name,vertices=len(coords),median_distance_px=float(np.median(distances)),p90_distance_px=float(np.percentile(distances,90)),max_distance_px=float(distances.max()),geo_bounds=[coords.min(axis=0).tolist(),coords.max(axis=0).tolist()]))
        points=[((p[0]-bbox[0])*scale,(p[1]-bbox[1])*scale) for p in projected]
        for x,y in points:draw.ellipse((x-2,y-2,x+2,y+2),fill='magenta')
    image.save(OUT/'MILLER_RIVERS_DIAGNOSTIC.png')
    core.dump('MILLER_PHYSICAL_CHECKS.json',dict(status='DIAGNOSTIC_NOT_APPROVED',matrix_fitted_to_rivers=False,source_sha256=core.sha(source),native_sha256=core.sha(core.qa.GAME/'map_data/rivers.png'),checks=metrics,
        warning='Nearest-network distances are NOT unique landmark matches; generalized/missing river branches and possible false correspondence must be reviewed visually.'))
    print(json.dumps(metrics,ensure_ascii=False))

def locator_preview():
    """Actual current ownership with explicitly UNVALIDATED locator hypotheses."""
    inventory=core.qa.inventory();bmp=core.packed(core.ROOT/'map_data/provinces.png')
    x0,y0,x1,y1=4280,780,4420,865;scale=8;local=bmp[y0:y1,x0:x1]
    owners={int(r['key'][0][1:],16):r['key'][2] for r in inventory['owners']}
    tags=np.array([owners.get(int(v),'?') for v in local.ravel()]).reshape(local.shape)
    palette={'PRU':(113,151,186),'HAN':(133,181,160),'HEK':(152,147,190),'HES':(182,142,188),'SAX':(197,179,143),'COB':(187,143,100),'KMZ':(189,78,75)}
    pixels=np.full((*local.shape,3),205,dtype=np.uint8)
    for tag,color in palette.items():pixels[tags==tag]=color
    im=Image.fromarray(pixels).resize((1120,680),Image.Resampling.NEAREST);draw=ImageDraw.Draw(im)
    for y,x in zip(*np.where(tags[1:]!=tags[:-1])):draw.line((x*scale,(y+1)*scale,(x+1)*scale,(y+1)*scale),fill='#444444',width=1)
    for y,x in zip(*np.where(tags[:,1:]!=tags[:,:-1])):draw.line(((x+1)*scale,y*scale,(x+1)*scale,(y+1)*scale),fill='#444444',width=1)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    anchors=json.loads((OUT/'NATIVE_ANCHORS.json').read_text())
    for r in anchors:
        if r['Hub_Type']!='city':continue
        x,y=float(r['Locator_X']),float(r['Locator_Y'])
        if not (x0<=x<x1 and y0<=y<y1):continue
        u,v=(x-x0)*scale,(y-y0)*scale;draw.ellipse((u-3,v-3,u+3,v+3),fill='black');draw.text((u+6,v),r['Hub_Name'],font=font,fill='black',stroke_width=2,stroke_fill='white')
    matrix=np.array(json.loads((OUT/'MILLER_HYPOTHESIS.json').read_text())['matrix'])
    points=[]
    for name,geo in [('Erfurt (projection non validée)',[11.03536353,50.97734161]),('Duderstadt (projection non validée)',[10.2595,51.5131]),('Heiligenstadt (projection non validée)',[10.1386,51.3782])]:
        p=np.array([np.radians(geo[0]),1.25*np.log(np.tan(np.pi/4+.4*np.radians(geo[1]))),1])@matrix
        u,v=(p[0]-x0)*scale,(p[1]-y0)*scale;draw.ellipse((u-5,v-5,u+5,v+5),outline='blue',width=2);draw.text((u+7,v-14),name,font=font,fill='blue',stroke_width=2,stroke_fill='white');points.append(dict(name=name,game=p.tolist()))
    r=next(r for r in anchors if r['Hub_Name']=='Erfurt');u,v=(float(r['Locator_X'])-x0)*scale,(float(r['Locator_Y'])-y0)*scale
    draw.ellipse((u-5,v-5,u+5,v+5),outline='#a85800',width=2);draw.text((u-45,v+12),'Ferme nommée Erfurt dans le jeu',font=font,fill='#a85800',stroke_width=2,stroke_fill='white')
    canvas=Image.new('RGB',(1120,750),'white');canvas.paste(im,(0,45));d=ImageDraw.Draw(canvas)
    d.text((12,10),'Placement à résoudre — territoires actuels INCHANGÉS',font=font,fill='black')
    d.text((12,721),'Bleu : hypothèses rejetées, PAS de nouvelles frontières. Orange : repère rural du jeu.',font=font,fill='black')
    canvas.save(OUT/'PLACEMENT_A_RESoudre.png')
    core.dump('UNAPPLIED_LOCATOR_HYPOTHESES.json',dict(status='REJECTED_NO_OWNER_CHANGE',points=points))
    expected=json.loads((OUT.parent/'MILAN_CREMONESE/NON_REGRESSION.json').read_text())
    checks=[dict(name='Last approved bitmap unchanged',passed=core.sha(core.ROOT/'map_data/provinces.png')==expected['applied_bitmap_sha256']),
        dict(name='Last approved imperial registry unchanged',passed=core.sha(core.active_registry_path())==expected['registry_sha256'])]
    for name in ['EICHSFELD_FULL_SOURCE.jpg','ERFURT_SOURCE.jpg']:
        metadata=json.loads((OUT.parent/'MAINZ_COMPLETION'/(name+'.SOURCE.json')).read_text())
        checks.append(dict(name='Retained historical source immutable '+name,passed=core.sha(OUT.parent/'MAINZ_COMPLETION'/name)==metadata['sha256']))
    core.dump('READ_ONLY_VALIDATION.json',dict(status='PASS_READ_ONLY_NOT_IMPLEMENTED' if all(r['passed'] for r in checks) else 'FAIL',checks=checks))
    assert all(r['passed'] for r in checks)
    print('Read-only checks',len(checks),'passed; no gameplay implementation')

def source_controls():
    """Review crops of the supplied Bern source; no raster boundary edits."""
    path=OUT.parent/'MAINZ_COMPLETION/BERN_ERFURT_1789.jpg'
    image=Image.open(path).convert('RGB');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    for name,box in [('BERN_EICHSFELD',(140,280,1600,1900)),('BERN_ERFURT',(1720,1570,3210,2790)),('BERN_TICKS',(90,220,3350,355))]:
        crop=image.crop(box);d=ImageDraw.Draw(crop)
        for x in range((box[0]//100+1)*100,box[2],100):
            d.line((x-box[0],0,x-box[0],crop.height),fill='#5599bb');d.text((x-box[0]+1,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            d.line((0,y-box[1],crop.width,y-box[1]),fill='#5599bb');d.text((1,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'_GRID.png'))
    print('New historical source review crops; no gameplay files touched')

if __name__=='__main__':
    {'inspect':inspect,'rivers':rivers,'capture':core.capture,'locator-preview':locator_preview,'catalogue':catalogue,'texture-mip':texture_mip,'source-controls':source_controls}[sys.argv[1]]()
