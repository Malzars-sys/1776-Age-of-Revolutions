"""Bounded continuation, using retained Schenk evidence; no other MAP lot."""
import csv
import json
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2l_mainz as core
import map2l_westphalia as previous

OUT = core.ROOT/'docs/reports/map/MAP2L/MINDEN_RAVENSBERG'
core.OUT = OUT
core.BACKUP = OUT.parent/'RHINE_WESTPHALIA/provinces_candidate.png'
core.REGIONS = {'STATE_HANNOVER'}
# Importing the preceding wrapper must not create countries again.
del core.PREPARE_EXTRA_FILES

def inspect():
    OUT.mkdir(parents=True, exist_ok=True)
    source=OUT.parent/'RHINE_WESTPHALIA/SCHENK_WESTPHALIA_1710_FULL.jpg'
    image=Image.open(source).convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for name,box in [('MINDEN',(1390,980,1800,1250)),('RAVENSBERG',(1260,1170,1570,1430)),('OSNABRUCK',(1030,1020,1240,1240))]:
        crop=image.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3))
        draw=ImageDraw.Draw(crop)
        for x in range((box[0]//20+1)*20,box[2],20):
            draw.line(((x-box[0])*3,0,(x-box[0])*3,crop.height),fill='#5599e9')
            draw.text(((x-box[0])*3+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//20+1)*20,box[3],20):
            draw.line((0,(y-box[1])*3,crop.width,(y-box[1])*3),fill='#5599e9')
            draw.text((0,(y-box[1])*3+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'_READING.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as stream:
        anchors=[r for r in csv.DictReader(stream) if r['State_ID'] in {'STATE_HANNOVER','STATE_WESTPHALIA'}]
    core.dump('NATIVE_ANCHORS.json',anchors)

def preview(bmp,rows,name):
    previous.OUT=OUT
    previous.preview(bmp,rows,name)

core.preview=preview

def patch_parts():
    """Split at file sections, retaining all original 15-line context."""
    raw=(OUT/'IMPERIAL.patch').read_text(encoding='utf-8')
    sections=raw.removeprefix('*** Begin Patch\n').removesuffix('*** End Patch\n').split('*** Update File: ')
    parts=[]
    for section in sections:
        if not section.strip():continue
        header,*hunks=section.split('\n@@')
        pending=[]
        for hunk in hunks:
            if pending and sum(map(len,pending))+len(hunk)>24000:
                parts.append('*** Begin Patch\n*** Update File: '+header+'\n@@'+'\n@@'.join(pending).rstrip('\n')+'\n*** End Patch\n')
                pending=[]
            pending.append(hunk)
        if pending:parts.append('*** Begin Patch\n*** Update File: '+header+'\n@@'+'\n@@'.join(pending).rstrip('\n')+'\n*** End Patch\n')
    original=[l for l in raw.splitlines() if l.startswith(('+','-'))]
    rebuilt=[l for part in parts for l in part.splitlines() if l.startswith(('+','-'))]
    assert rebuilt==original
    core.dump('IMPERIAL_PARTS.json',parts)
    print('Explicit patch parts:',len(parts),'largest:',max(map(len,parts),default=0))

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'geometry':core.geometry,'prepare':core.prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps,'patch-parts':patch_parts}[sys.argv[1]]()
