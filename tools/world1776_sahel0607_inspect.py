"""Read-only current territorial survey, before bounded Chad/Nile restoration."""
import json,csv,argparse
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_sahel0205 as previous

ROOT=previous.ROOT
LOT=previous.LOT.parent/'SAHEL-06-07'
ST=previous.ST
TAGS=['BOR','BGI','WAD','DFR','SD1']

def dump(name,value):
    (LOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def overview():
    cells=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'))
    hubs=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')))
    cat=previous.s.b.a.catalog('common/country_definitions')
    palette={t:tuple(int(v) for v in previous.s.ids(n,'color')) for t,(n,p) in cat.items() if previous.s.ids(n,'color') and all(v.isdigit() for v in previous.s.ids(n,'color'))}
    im=Image.open(ROOT/previous.s.BMP).convert('RGB');rivers=Image.open(ROOT/'map_data/rivers.png').convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for label,sids,indexkey in [('CHAD', ['STATE_CHAD','STATE_WADDAI','STATE_BORNU','STATE_DARFUR'],'CHAD_index'),
        ('NILE_NORTH',['STATE_EGYPTIAN_DESERT','STATE_DONGOLA'],'NILE_index'),
        ('NILE_SOUTH',['STATE_BLUE_NILE','STATE_KORDOFAN','STATE_ERITREA'],'NILE_index')]:
        rel=[r for r in cells if r['state'] in sids]
        box=(min(r['bbox'][0] for r in rel)-3,min(r['bbox'][1] for r in rel)-3,max(r['bbox'][2] for r in rel)+3,max(r['bbox'][3] for r in rel)+3)
        raw=np.array(im.crop(box));a=raw[:,:,0].astype('uint32')*65536+raw[:,:,1].astype('uint32')*256+raw[:,:,2]
        country=np.zeros_like(raw)+220
        for r in rel:
            p=palette.get(r['owner'],(120,120,120));country[a==int(r['RGB'][1:],16)]=tuple(int(v*.35+255*.65) for v in p)
        boundary=np.zeros(a.shape,dtype=bool);boundary[1:,:]|=a[1:,:]!=a[:-1,:];boundary[:,1:]|=a[:,1:]!=a[:,:-1]
        country[boundary]=(100,100,100)
        riv=np.array(rivers.crop(box)).astype('int16');water=(riv[:,:,2]>riv[:,:,0]+20)&(riv[:,:,2]>riv[:,:,1]+10)
        country[water]=(30,90,230)
        scale=5;out=Image.fromarray(country).resize((a.shape[1]*scale,a.shape[0]*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(out)
        for r in rel:
            x,y=r['centroid'];d.text(((x-box[0])*scale,(y-box[1])*scale),str(r[indexkey]),fill='#202020',font=font,stroke_width=1,stroke_fill='white')
        for h in hubs:
            if h['State_ID'] not in sids:continue
            x,y=float(h['Locator_X']),float(h['Locator_Y'])
            if not(box[0]<=x<box[2] and box[1]<=y<box[3]):continue
            x=(x-box[0])*scale;y=(y-box[1])*scale;d.ellipse((x-4,y-4,x+4,y+4),fill='black');d.text((x+5,y-16),h['Hub_Name'],fill='black',font=font,stroke_width=2,stroke_fill='white')
        out.save(LOT/(label+'_PROVINCES_AND_RIVERS.png'))

def survey():
    LOT.mkdir(exist_ok=True)
    assert not (LOT/'BASELINE.json').exists(),'Initial survey already captured; do not replace it.'
    previous.s.g.LOT=LOT
    protected=previous.s.g.protection()
    for p in (ROOT/'gfx/map/map_object_data').glob('*.txt'):protected[p.relative_to(ROOT).as_posix()]=previous.s.b.a.sha(p)
    dump('BASELINE.json',dict(inventory=previous.s.b4.inventory(),protected=protected,
        source='Current workspace, including SAHEL-01/02-05 and NORTHWEST-01, not a Git baseline.'))
    text=previous.raw(ROOT/ST);regions=[];owners={}
    for n in previous.s.b.walk(previous.s.b.parse(text)):
        if not n.key.startswith('s:STATE_'):continue
        for p in n.children('create_state'):
            for c in previous.s.ids(p,'owned_provinces'):owners[c]=(n.key[2:],p.one('country')[2:])
        if any(p.one('country')[2:] in TAGS for p in n.children('create_state')):
            regions.append(n.key[2:])
    regions+=['STATE_DARFUR','STATE_SUDAN','STATE_UPPER_NILE','STATE_UBANGI_SHARI']
    regions=list(dict.fromkeys(regions))
    cat=previous.s.b.a.catalog('map_data/state_regions')
    country=previous.s.b.a.catalog('common/country_definitions')
    image=np.asarray(Image.open(ROOT/previous.s.BMP).convert('RGB'))
    # Focused window includes the current Sudan and Chad; no inference of a
    # political frontier from these pixel coordinates.
    image=image[1300:2050,4250:5150]
    packed=image[:,:,0].astype('uint32')*65536+image[:,:,1].astype('uint32')*256+image[:,:,2]
    rows=[]
    for sid in regions:
        if sid not in cat:continue
        n,p=cat[sid]
        for c in previous.s.ids(n,'provinces'):
            yy,xx=np.where(packed==int(c[1:],16))
            if not xx.size:continue
            rows.append(dict(state=sid,RGB=c,owner=owners.get(c,[None,None])[1],
                centroid=[round(float(xx.mean())+4250,2),round(float(yy.mean())+1300,2)],
                bbox=[int(xx.min())+4250,int(yy.min())+1300,int(xx.max()+1)+4250,int(yy.max()+1)+1300],pixels=int(xx.size)))
    dump('GEOMETRY_CELLS.json',rows)
    inventory=[]
    for sid in regions:
        if sid not in cat:continue
        n,p=cat[sid]
        inventory.append(dict(state=sid,portions=dict(Counter(v[1] for v in owners.values() if v[0]==sid)),
            hubs={c.key:c.value for c in n.children() if c.key.startswith('city') or c.key in ['farm','mine','wood','port']}))
    dump('TARGET_INVENTORY.json',inventory)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for label,sids in [('CHAD',['STATE_CHAD','STATE_WADDAI','STATE_BORNU','STATE_DARFUR']),
                       ('NILE',['STATE_DONGOLA','STATE_BLUE_NILE','STATE_KORDOFAN','STATE_ERITREA','STATE_EGYPTIAN_DESERT'])]:
        relevant=[r for r in rows if r['state'] in sids]
        x0=min(r['bbox'][0] for r in relevant)-3;y0=min(r['bbox'][1] for r in relevant)-3
        x1=max(r['bbox'][2] for r in relevant)+3;y1=max(r['bbox'][3] for r in relevant)+3
        crop=Image.fromarray(image).crop((x0-4250,y0-1300,x1-4250,y1-1300)).resize(((x1-x0)*4,(y1-y0)*4),Image.Resampling.NEAREST)
        d=ImageDraw.Draw(crop)
        for i,r in enumerate(relevant):
            x,y=r['centroid'];d.text(((x-x0)*4,(y-y0)*4),str(i),font=font,fill='white',stroke_width=1,stroke_fill='black');r[label+'_index']=i
        crop.save(LOT/(label+'_NATIVE_RGB_INDEX.png'))
    dump('GEOMETRY_CELLS.json',rows)
    print('Survey:',len(regions),'regions;',len(rows),'native RGB records;',len(protected),'protected files.')
    print(json.dumps(inventory,ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');a=p.parse_args()
    if a.render:overview()
    else:survey()
