"""Controlled local affine diagnostic, using existing MAP1 exact RLE geometry.

No fitted point is treated as an independent validation. No geodetic projection.
Only report outputs are written.
"""
from pathlib import Path
import csv, gzip, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'docs/reports/map/MAP1'
OUT=ROOT/'docs/reports/map/MAP1B'
E=OUT/'MAP1B_GEOGRAPHIC_EVIDENCE'
def table(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def writecsv(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def font(size): return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
cases=json.loads((E/'anchor_observations.json').read_text(encoding='utf-8'))
hubs=table(OLD/'MAP1_HUB_LOCATOR_CHECKS.csv')
baseline=table(OLD/'MAP1_BASELINE_PROVINCE_INDEX.csv')
geom=json.loads((OLD/'MAP1_GEOGRAPHIC_EVIDENCE/geometry_index.json').read_text())
states={'lux':['STATE_WALLONIA'], 'lombardy':['STATE_LOMBARDY'], 'silesia':['STATE_LOWER_SILESIA','STATE_UPPER_SILESIA']}
extras={'lux':[], 'lombardy':[], 'silesia':['x71E080','xF0E080','x9061E0']}
wanted={r['Province_ID'] for r in baseline if any(r['State_ID'] in s for s in states.values())}|set(extras['silesia'])
runs={}
with gzip.open(OLD/'MAP1_GEOGRAPHIC_EVIDENCE/PROVINCE_PIXEL_RUNS.jsonl.gz','rt',encoding='utf-8') as f:
    for line in f:
        obj=json.loads(line)
        if obj['Province_ID'] in wanted: runs[obj['Province_ID']]=obj['runs_y_x0_x1_exclusive']
metrics={}; observations=[]
for name,ss in states.items():
    config=cases[name]; points=[]
    for label,sid,kind,u,v,role in config['points']:
        h=next(h for h in hubs if h['State_ID']==sid and h['Hub_Type']==kind)
        points.append({'Name':label,'State_ID':sid,'Hub_Type':kind,'Game_X':float(h['Locator_X']),'Game_Y':float(h['Locator_Y']),'Source_X':u,'Source_Y':v,'Role':role,'Sampled_RGB':h['Locator_Sampled_RGB']})
    fit=[p for p in points if p['Role']=='FIT']
    X=np.array([[p['Game_X'],p['Game_Y'],1] for p in fit]); Y=np.array([[p['Source_X'],p['Source_Y']] for p in fit])
    assert np.linalg.matrix_rank(X)==3
    T=np.linalg.lstsq(X,Y,rcond=None)[0]
    inv=np.linalg.inv(T[:2])
    for p in points:
        delta=np.array([p['Game_X'],p['Game_Y'],1])@T-np.array([p['Source_X'],p['Source_Y']])
        p.update(Case=name,Residual_Source_Px=round(float(np.linalg.norm(delta)),2),Residual_Game_Px=round(float(np.linalg.norm(delta@inv)),3))
        observations.append(p)
    check=[p for p in points if p['Role']=='CHECK']
    maxerr=max(p['Residual_Game_Px'] for p in check)
    m={'affine_game_to_source':T.tolist(),'fit_rms_source_px':float(np.sqrt(np.mean([p['Residual_Source_Px']**2 for p in points if p['Role']=='FIT']))),'check_rms_game_px':float(np.sqrt(np.mean([p['Residual_Game_Px']**2 for p in check]))),'check_max_game_px':maxerr,'check_count':len(check),'fit_count':len(fit),'mapping_status':'DIAGNOSTIC_NOT_PROJECTION_VALIDATION','manual_reading_source_px':5}
    metrics[name]=m
    im=Image.open(E/config['image']).convert('RGB'); draw=ImageDraw.Draw(im)
    ids=sorted({r['Province_ID'] for r in baseline if r['State_ID'] in ss}|set(extras[name]))
    def trans(x,y): return tuple(np.array([x,y,1.0])@T)
    # Exact polygon is union of pixel squares. Draw only exposed unit edges.
    for i,pid in enumerate(ids):
        cells={(x,y) for y,a,b in runs[pid] for x in range(a,b)}
        color=(20,50,220) if pid not in extras[name] else (235,30,180)
        for x,y in cells:
            for dx,dy,edge in [(0,-1,[(x,y),(x+1,y)]),(0,1,[(x,y+1),(x+1,y+1)]),(-1,0,[(x,y),(x,y+1)]),(1,0,[(x+1,y),(x+1,y+1)])]:
                if (x+dx,y+dy) not in cells: draw.line([trans(*p) for p in edge],fill=color,width=2)
        x,y=trans(*geom['anchors'][pid]); text=str(i+1)
        bb=draw.textbbox((x,y),text,font=font(16)); draw.rectangle((bb[0]-2,bb[1]-2,bb[2]+2,bb[3]+2),fill='white'); draw.text((x,y),text,font=font(16),fill=color)
    for i,p in enumerate(points):
        u,v=p['Source_X'],p['Source_Y']; pu,pv=trans(p['Game_X'],p['Game_Y'])
        color=(10,140,70) if p['Role']=='FIT' else (230,95,0)
        draw.ellipse((u-5,v-5,u+5,v+5),outline=color,width=3)
        draw.line([(u,v),(pu,pv)],fill=color,width=2)
        draw.line([(pu-4,pv),(pu+4,pv)],fill=color,width=2); draw.line([(pu,pv-4),(pu,pv+4)],fill=color,width=2)
        draw.text((u+7,v-16),chr(65+i),font=font(17),fill=color,stroke_width=1,stroke_fill='white')
    im.save(E/(name+'_historical_overlay.png'))
    # A focused crop preserves scan pixels 1:1, with enough context and labels.
    coords=np.array([trans(*geom['anchors'][pid]) for pid in ids]); lo=coords.min(0)-130; hi=coords.max(0)+130
    box=(max(0,int(lo[0])),max(0,int(lo[1])),min(im.width,int(hi[0])),min(im.height,int(hi[1])))
    if box[2]>box[0] and box[3]>box[1]: im.crop(box).save(E/(name+'_detail.png'))
    rows=[]
    for i,pid in enumerate(ids):
        bb=geom['bboxes'][pid]; cen=trans(*geom['anchors'][pid])
        rows.append({'Label':i+1,'Province_ID':pid,'State_ID':'|'.join(sorted({r['State_ID'] for r in baseline if r['Province_ID']==pid})),'Current_Owners':'|'.join(sorted({r['Owner_TAG'] for r in baseline if r['Province_ID']==pid})),'Source_Anchor_X':round(cen[0],2),'Source_Anchor_Y':round(cen[1],2),'Pixel_BBox':str(bb),'Pixel_Area':sum(b-a for y,a,b in runs[pid]),'Historical_Status':'UNASSESSED_AT_RENDER_TIME'})
    writecsv(E/(name+'_overlay_legend.csv'),rows)
    print(name, 'fit RMS scan:',round(m['fit_rms_source_px'],1),'check max game:',maxerr)
writecsv(E/'GCP_AND_CONTROLS.csv',observations)
(E/'ALIGNMENT_METRICS.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
