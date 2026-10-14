"""Continue corroborated Franconian envelopes into adjacent Bavarian provinces.

Erfurt calibration and all its pending territories are explicitly out of scope.
The retained Homann tracing and its imperfect but documented game-scale affine
are reused; no city-distance partition or new projection optimization.
"""
import csv
import json
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2l_mainz as core
from map2l_franconia import inside,PALETTE

OUT=core.ROOT/'docs/reports/map/MAP2L/FRANCONIA_CONTINUATION'
core.OUT=OUT
core.BACKUP=OUT.parent/'MILAN_CREMONESE/provinces_candidate.png'
core.REGIONS={'STATE_FRANCONIA','STATE_BAVARIA'}

def preview(bmp,rows,name):
    cfg=json.loads((OUT/'TRACING.json').read_text())
    x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1]
    arr=np.full((*local.shape,3),235,dtype=np.uint8)
    for row in rows:
        rgb,_,tag=row['key'];arr[local==int(rgb[1:],16)]=PALETTE.get(tag,(200,200,192))
    edge=np.zeros(local.shape,dtype=bool);edge[1:]|=local[1:]!=local[:-1];edge[:,1:]|=local[:,1:]!=local[:,:-1]
    arr[edge]=50
    image=Image.fromarray(arr).resize((local.shape[1]*16,local.shape[0]*16),Image.Resampling.NEAREST)
    out=Image.new('RGB',(image.width,image.height+90),'white');out.paste(image)
    draw=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    draw.text((10,image.height+5),name+' | Franconian envelopes across economic region border',font=font,fill='black')
    draw.text((10,image.height+30),'ANS orange / FBM blue / NUR red / EIC green / BAV grey',font=font,fill='black')
    draw.text((10,image.height+55),'Game-scale approximation; unchanged fringes remain unresolved.',font=font,fill='black')
    out.save(OUT/(name+'.png'))

core.preview=preview

def geometry():
    core.geometry()
    result=json.loads((OUT/'GEOMETRY.json').read_text())
    result['status']='RETAINED_FRANCONIAN_ENVELOPES_CONTINUED_ACROSS_ECONOMIC_BORDER'
    core.dump('GEOMETRY.json',result)

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    before=core.packed(core.ROOT/'map_data/provinces.png')
    t=np.array(json.loads((OUT.parent/'FRANCONIA/ALIGNMENT.json').read_text())['matrix_source_to_game'])
    polygons=json.loads((OUT.parent/'FRANCONIA/TRACING.json').read_text())['polygons']
    findings=[]
    for row in baseline['inventory']['owners']:
        rgb,sid,tag=row['key']
        if sid not in core.REGIONS or tag!='BAV':continue
        y,x=np.where(before==int(rgb[1:],16));cells=np.column_stack((x,y))
        source=(cells+.5-t[2])@np.linalg.inv(t[:2])
        for polygon in polygons:
            if polygon['owner']=='COB':continue
            selected=inside(source,polygon['points'])
            if np.any(selected):findings.append({'rgb':rgb,'state':sid,'previous_owner':tag,
                'owner':polygon['owner'],'territory':polygon['jurisdiction'],'pixels':int(selected.sum()),
                'cells':cells[selected].tolist(),'source_bounds':[source[selected].min(axis=0).tolist(),source[selected].max(axis=0).tolist()]})
    core.dump('CONTINUATION_INTERSECTIONS.json',findings)
    print(json.dumps([{k:v for k,v in r.items() if k!='cells'} for r in findings],ensure_ascii=False,indent=2))

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'geometry':geometry,'prepare':core.prepare,
        'install':core.install,'imperial':core.imperial,'maps':core.maps}[sys.argv[1]]()
