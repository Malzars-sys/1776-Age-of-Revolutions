"""Authorised Mainz southern and remote estates; stage, never invent boundaries."""
import csv
import html
import io
import json
import re
import sys
import urllib.request
import urllib.parse
from PIL import Image,ImageDraw,ImageFont
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/MAINZ_COMPLETION'
core.OUT=OUT
core.BACKUP=OUT.parent/'MAINZ_ESTATES/provinces_candidate.png'
core.REGIONS={'STATE_BADEN','STATE_WURTTEMBERG'}

def links():
    request=urllib.request.Request(sys.argv[2],headers={'User-Agent':'Mozilla/5.0 (historical cartography research)'})
    with urllib.request.urlopen(request,timeout=30) as response:raw=response.read(3_000_001).decode('utf-8')
    assert len(raw)<3_000_000
    urls=[html.unescape(v) for v in re.findall(r'(?:href|src|content)=[\"\']([^\"\']+)',raw)]
    if len(sys.argv)>3 and sys.argv[3]=='original':urls=[v for v in urls if 'upload.wikimedia.org' in v and 'original' in v]
    print('\n'.join(dict.fromkeys(v for v in urls if re.search(r'jpg|jp2|png|tif|iiif|manifest|Content|content/|djvu',v,re.I))))

def fetch():
    OUT.mkdir(parents=True,exist_ok=True)
    url,name,date,catalogue=sys.argv[2:6]
    target=OUT/name
    assert not target.exists(),'Do not replace a retained source'
    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (historical cartography research)'})
    with urllib.request.urlopen(request,timeout=30) as response:data=response.read(40_000_001)
    assert len(data)<=40_000_000
    image=Image.open(io.BytesIO(data));image.verify()
    target.write_bytes(data)
    core.dump(name+'.SOURCE.json',dict(url=url,catalogue=catalogue,date=date,sha256=core.sha(target),size=list(Image.open(target).size),
        use='Retained historical research comparison, not runtime artwork; date and territorial continuity must be checked separately'))
    print(name,Image.open(target).size,core.sha(target))

def gazetteer():
    for name in sys.argv[2:]:
        url='https://www.geonames.org/advanced-search.html?'+urllib.parse.urlencode({'q':name,'featureClass':'P','country':'DE'})
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (historical cartography research)'})
        with urllib.request.urlopen(request,timeout=20) as response:raw=response.read(2_000_000).decode('utf-8')
        rows=[re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',row))).strip() for row in re.findall(r'<tr[^>]*>(.*?)</tr>',raw,re.S)]
        rows=[row for row in rows if re.match(r'^\d+\s',row) and 'records found' not in row]
        matched=[row for row in rows if re.match(r'^\d+\s'+re.escape(name)+r'\b',row,re.I)]
        print(url,'\n','\n'.join(row[:450] for row in (matched or rows)[:2]))

def anchors():
    OUT.mkdir(parents=True,exist_ok=True)
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as source:
        rows=[{k:r[k] for k in ['State_ID','Hub_Type','Hub_Name','Locator_X','Locator_Y','Locator_Sampled_RGB']} for r in csv.DictReader(source) if r['State_ID'] in core.REGIONS|{'STATE_HESSE','STATE_SAXONY','STATE_HANNOVER','STATE_BRUNSWICK','STATE_WESTPHALIA','STATE_ANHALT'}]
    core.dump('NATIVE_ANCHORS.json',rows)
    print(json.dumps(rows,ensure_ascii=False))

def crops():
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT.parent/'MAINZ_ESTATES/OBERSTIFT_1789_COMPARISON.jpg'
    image=Image.open(path).convert('RGB');image.crop((180,350,580,754)).resize((1200,1212)).save(OUT/'HL_SOUTH_READING.png')
    image.crop((315,610,475,730)).resize((800,600)).save(OUT/'HL_KRAUTHEIM.png')
    for path in OUT.glob('*_SOURCE.jpg'):
        image=Image.open(path).convert('RGB');overview=image.copy();overview.thumbnail((1800,1500));overview.save(OUT/(path.stem+'_OVERVIEW.png'))
        font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);draw=ImageDraw.Draw(image)
        for x in range(0,image.width,100):draw.line((x,0,x,image.height),fill='blue');draw.text((x+1,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range(0,image.height,100):draw.line((0,y,image.width,y),fill='blue');draw.text((1,y+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        image.save(OUT/(path.stem+'_GRID.png'))
        if path.name=='EICHSFELD_FULL_SOURCE.jpg':image.crop((650,300,2000,1900)).save(OUT/'EICH_CONTROLS_GRID.png')
        if path.name=='ERFURT_SOURCE.jpg':image.resize((2829,2374)).save(OUT/'ERF_HALF_GRID.png')

def controls():
    boxes={'EICHSFELD_FULL_SOURCE.jpg':{'DUDERSTADT':(1000,410,1210,610),'HEILIGENSTADT':(750,1050,970,1220),'WORBIS':(1610,780,1820,980),'MUEHLHAUSEN':(1740,1630,1990,1850),'DINGELSTADT':(1290,1190,1500,1390)},
           'ERFURT_SOURCE.jpg':{'ERFURT':(2600,2130,3100,2630),'GOTHA':(540,2720,930,3020),'TENN':(1100,180,1450,430),'ARNSTADT':(2180,3760,2570,4040)}}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for path,names in boxes.items():
        image=Image.open(OUT/path).convert('RGB')
        for name,box in names.items():
            crop=image.crop(box);draw=ImageDraw.Draw(crop)
            for x in range(((box[0]+24)//25)*25,box[2],25):draw.line((x-box[0],0,x-box[0],crop.height),fill='blue');draw.text((x-box[0],0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
            for y in range(((box[1]+24)//25)*25,box[3],25):draw.line((0,y-box[1],crop.width,y-box[1]),fill='blue');draw.text((0,y-box[1]),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
            crop.resize((crop.width*2,crop.height*2)).save(OUT/(name+'_CONTROL.png'))

def northern_assessment():
    import numpy as np
    fit=[dict(name='Hanover',geo=[9.73322153091431,52.3705162650448],native=[4325.178,788.162],kind='city'),
         dict(name='Magdeburg',geo=[11.63188772,52.13129335],native=[4365.351,796.94],kind='city'),
         dict(name='Erfurt',geo=[11.03536353,50.97734161],native=[4336.258,832.944],kind='farm')]
    checks=[dict(name='Wernigerode',geo=[10.782163,51.836522],native=[4333.256,822.15],kind='farm'),
            dict(name='Leipzig',geo=[12.371292,51.33962],native=[4380.9,821.209],kind='mine')]
    matrix=np.linalg.solve(np.array([r['geo']+[1] for r in fit]),np.array([r['native'] for r in fit]))
    for row in checks:
        row['predicted']=(np.array(row['geo']+[1])@matrix).tolist()
        row['error_px']=float(np.linalg.norm(np.array(row['predicted'])-row['native']))
    # An independently configured city-only model exposes the rural-label problem.
    cityfit=[fit[0],fit[1],dict(name='Frankfurt',geo=[8.683333333,50.116666667],native=[4300.876,856.939],kind='city')]
    citymatrix=np.linalg.solve(np.array([r['geo']+[1] for r in cityfit]),np.array([r['native'] for r in cityfit]))
    citychecks=[dict(name='Brunswick',geo=[10.526726,52.265939],native=[4339.979,795.886],kind='city'),
                dict(name='Dresden',geo=[13.738317489624023,51.05089108097961],native=[4411.987,828.656],kind='city'),fit[2].copy()]
    for row in citychecks:
        row['predicted']=(np.array(row['geo']+[1])@citymatrix).tolist();row['error_px']=float(np.linalg.norm(np.array(row['predicted'])-row['native']))
    core.dump('NORTHERN_CALIBRATION_ASSESSMENT.json',dict(status='REJECTED_NOT_APPLIED',first_fit=fit,first_matrix=matrix.tolist(),first_checks=checks,
        city_fit=cityfit,city_matrix=citymatrix.tolist(),city_checks=citychecks,coordinates_source='GeoNames public gazetteer; exact town queries documented in REPORT.md',
        conclusion='Native farm/mine labels are not established GPS controls. Large discrepancies invalidate blind local affine transfer. City-only extrapolation also lacks sufficiently local independent control. No northern border or owner changed; a reviewed geographic-to-game correspondence is still required.'))
    print(json.dumps(dict(first_checks=checks,city_checks=citychecks),ensure_ascii=False))

def setup_south():
    cfg=OUT/'TRACING.json';assert not cfg.exists(),'Preserve manual tracing; edit it with apply_patch'
    source=json.loads((OUT.parent/'MAINZ_ESTATES/ALIGNMENT.json').read_text())['sources'][1]
    source=dict(source,path='../MAINZ_ESTATES/OBERSTIFT_1789_COMPARISON.jpg')
    source.pop('sha256',None)
    limits=['Southern continuation of the previously reviewed Mainz envelopes at game resolution, not a cadastral map.',
        'HL comparison is dated 1789; Buchen, Tauberbischofsheim and Krautheim sovereignty is separately corroborated for 1776. No 1803 successor principality is projected backwards.',
        'Schontal, Wurzburg, Wertheim, Palatinate and knightly pockets remain excluded; invisible micro-enclaves are not enlarged.',
        'Erfurt and Eichsfeld are not implemented: their independent native geographic controls fail; see NORTHERN_CALIBRATION_ASSESSMENT.json.',
        'Prior HRE lots, coarse Mainz core and other residual owners are not certified or rewritten by this continuation.',
        'Population and building redistribution is an area-weighted gameplay approximation with exact profile conservation; engine test remains deferred.']
    core.dump('TRACING.json',dict(method='Reuse the specific Oberstift local calibration and trace only its southern continuation; northern calage rejected separately.',
        discover_only=True,rgb_start=0xEDA600,native_anchors='NATIVE_ANCHORS.json',parents=['x318061','xEDA302','xEDA511','xEDA206','x100060','x118060','x8F0060','xC541D2'],
        preview_box=[4292,872,4330,898],preview_labels=[['Buchen',4305,880],['Tauberbischofsheim',4314,880],['Krautheim',4310,884],['Heilbronn (native wood hub)',4305,888]],
        calibrated_sources=[source],polygons=[],limitations=limits))

if __name__=='__main__':({'links':links,'fetch':fetch,'gazetteer':gazetteer,'anchors':anchors,'crops':crops,'controls':controls,'northern-assessment':northern_assessment,'setup-south':setup_south}.get(sys.argv[1]) or getattr(core,sys.argv[1]))()
