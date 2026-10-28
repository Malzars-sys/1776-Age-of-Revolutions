"""Current-file survey for Horn territorial work; no functional writes."""
import csv,json
from collections import Counter,defaultdict
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_sahel0607 as prior
ROOT=prior.ROOT
LOT=prior.LOT.parent/'CONGO-01'
ST=prior.ST
SIDS=['STATE_CONGO','STATE_BAS_CONGO','STATE_NORTH_ANGOLA','STATE_SOUTH_ANGOLA','STATE_EAST_ANGOLA','STATE_KASAI','STATE_GABON','STATE_KATANGA','STATE_BENGUELA_COAST']

def dump(name,value):
    (LOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def survey():
    LOT.mkdir(exist_ok=True)
    assert not (LOT/'BASELINE.json').exists(),'Do not replace captured inputs.'
    prior.m.s.g.LOT=LOT
    dump('BASELINE.json',dict(inventory=prior.m.s.b4.inventory(),protected=prior.m.s.g.protection(),source='Actual current workspace after user test and concurrent American changes; not a Git baseline.'))
    own=prior.m.state_owners(prior.raw(ROOT/ST));regioncat=prior.m.s.b.a.catalog('map_data/state_regions');country=prior.m.s.b.a.catalog('common/country_definitions')
    regions=[];tags=set()
    for sid in SIDS:
        if sid not in regioncat:continue
        n,path=regioncat[sid];parts=Counter(v[-1][1] for v in own.values() if v[-1][0]==sid);tags.update(parts)
        regions.append(dict(state=sid,portions=dict(parts),hubs={c.key:c.value for c in n.children() if c.key in ['city','port','farm','wood','mine']}))
    countries=[]
    for t in sorted(tags):
        n,path=country[t]
        countries.append(dict(TAG=t,path=str(path),definition=prior.raw(path)[n.start:n.end],history=[str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else 'VANILLA:'+p.name for p in prior.m.s.b.tech.effective('common/history/countries') if any(x.key=='c:'+t for x in prior.m.s.b.walk(prior.m.s.b.parse(prior.raw(p))))]))
    dump('CURRENT_INVENTORY.json',dict(regions=regions,countries=countries))
    im=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'))
    pack=im[:,:,0].astype('uint32')*65536+im[:,:,1].astype('uint32')*256+im[:,:,2]
    palette={}
    for t,(n,path) in country.items():
        try:palette[t]=tuple(map(int,prior.m.s.ids(n,'color')))
        except ValueError:continue
    box=(4250,2040,4750,2570);x0,y0,x1,y1=box;crop=pack[y0:y1,x0:x1];rgb=np.zeros((*crop.shape,3),'uint8')+210
    rows=[];idx=0
    for sid in SIDS:
        if sid not in regioncat:continue
        n,path=regioncat[sid]
        for c in prior.m.s.ids(n,'provinces'):
            yy,xx=np.where(crop==int(c[1:],16))
            if not xx.size:continue
            tag=own.get(c,[[sid,None]])[-1][1]
            rgb[crop==int(c[1:],16)]=tuple(int(v*.4+255*.6) for v in palette.get(tag,(100,100,100)))
            rows.append(dict(index=idx,state=sid,RGB=c,owner=tag,pixels=int(xx.size),centroid=[round(float(xx.mean())+x0,2),round(float(yy.mean())+y0,2)],bbox=[int(xx.min())+x0,int(yy.min())+y0,int(xx.max())+x0+1,int(yy.max())+y0+1]));idx+=1
    edge=np.zeros(crop.shape,bool);edge[1:]|=crop[1:]!=crop[:-1];edge[:,1:]|=crop[:,1:]!=crop[:,:-1];rgb[edge]=(125,125,125)
    river=np.array(Image.open(ROOT/'map_data/rivers.png').convert('RGB'))[y0:y1,x0:x1].astype('int16')
    rgb[(river[:,:,2]>river[:,:,0]+20)&(river[:,:,2]>river[:,:,1]+10)]=(40,95,210)
    out=Image.fromarray(rgb).resize(((x1-x0)*4,(y1-y0)*4),Image.Resampling.NEAREST);draw=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for r in rows:
        x,y=r['centroid'];draw.text(((x-x0)*4,(y-y0)*4),str(r['index']),font=font,fill='black',stroke_width=1,stroke_fill='white')
    hubs=list(csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')))
    for h in hubs:
        if h['State_ID'] not in SIDS:continue
        x,y=float(h['Locator_X']),float(h['Locator_Y'])
        if x0<=x<x1 and y0<=y<y1:draw.text(((x-x0)*4,(y-y0)*4-16),h['Hub_Name'],font=font,fill='black',stroke_width=2,stroke_fill='white')
    out.save(LOT/'NATIVE_PROVINCES_AND_RIVERS.png');dump('GEOMETRY_CELLS.json',rows)
    print(json.dumps(regions,ensure_ascii=False,indent=2))
    print('Countries:',sorted(tags),'cells:',len(rows))

if __name__=='__main__':survey()
