"""Read-only MAP-1C input snapshots and physical-reference crops."""
from pathlib import Path
import json, csv
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from map1_prepare import protected,digest,GAME,table
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/MAP1C'
E=OUT/'MAP1C_GEOGRAPHIC_EVIDENCE'
OUT.mkdir(exist_ok=True); E.mkdir(exist_ok=True)
baseline=protected()
old=json.loads((ROOT/'docs/reports/map/MAP1B/MAP1B_RUNTIME_BEFORE.json').read_text())
assert baseline==old
p=OUT/'MAP1C_PROTECTED_BEFORE.json'
snap={'runtime':baseline,'MAP1B':{f.relative_to(ROOT).as_posix():digest(f) for f in (ROOT/'docs/reports/map/MAP1B').rglob('*') if f.is_file()},'HEAD':'c891b1d9bb2a21bc42409acbdccc268518110260'}
if p.exists(): assert json.loads(p.read_text())==snap
else: p.write_text(json.dumps(snap,indent=2),encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
cropboxes={'lux':(4160,815,4275,915),'lombardy':(4270,940,4380,1040),'silesia':(4420,790,4570,905)}
base=table(ROOT/'docs/reports/map/MAP1/MAP1_BASELINE_PROVINCE_INDEX.csv')
geom=json.loads((ROOT/'docs/reports/map/MAP1/MAP1_GEOGRAPHIC_EVIDENCE/geometry_index.json').read_text())
river=Image.open(GAME/'map_data/rivers.png'); print('rivers',river.size,river.mode)
provinces=Image.open(GAME/'map_data/provinces.png').convert('RGB')
for case,box in cropboxes.items():
    im=river.crop(box).convert('RGB').resize(((box[2]-box[0])*8,(box[3]-box[1])*8),Image.Resampling.NEAREST)
    d=ImageDraw.Draw(im)
    for x in range(box[0],box[2],10):
        xx=(x-box[0])*8; d.line((xx,0,xx,im.height),fill=(180,180,180)); d.text((xx+2,2),str(x),fill='black',font=font)
    for y in range(box[1],box[3],10):
        yy=(y-box[1])*8; d.line((0,yy,im.width,yy),fill=(180,180,180)); d.text((2,yy+2),str(y),fill='black',font=font)
    im.save(E/(case+'_game_rivers_grid.png'))
    pi=provinces.crop(box).resize(im.size,Image.Resampling.NEAREST); dr=ImageDraw.Draw(pi)
    for r in base:
        pid=r['Province_ID']; x,y=geom['anchors'][pid]
        if box[0]<=x<box[2] and box[1]<=y<box[3]:
            dr.text(((x-box[0])*8,(y-box[1])*8),pid,fill='white',stroke_width=1,stroke_fill='black',font=font)
    pi.save(E/(case+'_game_rgb_grid.png'))
assert baseline==protected()
