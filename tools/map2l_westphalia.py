"""Bounded Rhine/Westphalia implementation using retained map evidence.

Immutable source stage; no projection refitting of Erfurt or earlier Mainz lots.
Runtime text changes are emitted as apply_patch payloads, not installed silently.
"""
import csv
import json
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageColor
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/RHINE_WESTPHALIA'
core.OUT=OUT
core.BACKUP=OUT.parent/'FRANCONIA_CONTINUATION/provinces_candidate.png'
core.REGIONS={'STATE_NORTH_RHINE','STATE_RUHR','STATE_WESTPHALIA'}

def inspect():
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as stream:
        anchors=[row for row in csv.DictReader(stream) if row['State_ID'] in core.REGIONS|{'STATE_HANNOVER','STATE_HESSE','STATE_GELRE','STATE_RHINELAND'}]
    core.dump('NATIVE_ANCHORS.json',anchors)
    print(json.dumps([{k:row[k] for k in ['State_ID','Hub_Type','Hub_Name','Locator_X','Locator_Y','Locator_Sampled_RGB']} for row in anchors],ensure_ascii=False))
    source=OUT.parent/'RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg'
    image=Image.open(source).convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for name,box in [('VAUGONDY_NORTH',(440,70,1690,880))]:
        crop=image.crop(box);draw=ImageDraw.Draw(crop)
        for x in range((box[0]//50+1)*50,box[2],50):
            draw.line((x-box[0],0,x-box[0],crop.height),fill='#618fee');draw.text((x-box[0]+1,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//50+1)*50,box[3],50):
            draw.line((0,y-box[1],crop.width,y-box[1]),fill='#618fee');draw.text((0,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'.png'))

def preview(bmp,rows,name):
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1]
    owners={int(r['key'][0][1:],16):r['key'][2] for r in rows}
    tags=np.array([owners.get(int(value),'?') for value in local.ravel()]).reshape(local.shape)
    colors={'PRU':'#609ab6','KPF':'#d7aa32','KCL':'#737db9','WPM':'#87b468','WPD':'#e09070','LIP':'#bb8aab','SCM':'#dec588','HAN':'#bbc0b2','NAS':'#df9468','BEO':'#d4bf97','LGE':'#bd6389','STM':'#6bac78','NET':'#d8945d'}
    arr=np.full((*local.shape,3),220,dtype=np.uint8)
    for tag,color in colors.items():arr[tags==tag]=ImageColor.getrgb(color)
    scale=8;image=Image.fromarray(arr).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST);draw=ImageDraw.Draw(image)
    for y,x in zip(*np.where(tags[1:]!=tags[:-1])):draw.line((x*scale,(y+1)*scale,(x+1)*scale,(y+1)*scale),fill='#282828',width=1)
    for y,x in zip(*np.where(tags[:,1:]!=tags[:,:-1])):draw.line(((x+1)*scale,y*scale,(x+1)*scale,(y+1)*scale),fill='#282828',width=1)
    canvas=Image.new('RGB',(image.width,image.height+70),'white');canvas.paste(image)
    draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    draw.text((8,image.height+4),name+' | Rhin-Westphalie: retained sources / game-scale approximation',font=font,fill='black')
    draw.text((8,image.height+25),'Prusse bleu / Palatinat or / Cologne violet / Munster vert / Paderborn saumon',font=font,fill='black')
    draw.text((8,image.height+46),'No cadastral or sub-two-pixel precision claimed.',font=font,fill='black')
    canvas.save(OUT/(name+'.png'))

core.preview=preview

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'geometry':core.geometry,'prepare':core.prepare,
     'install':core.install,'imperial':core.imperial,'maps':core.maps}[sys.argv[1]]()
