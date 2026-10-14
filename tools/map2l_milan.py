"""Scoped Milan/Cremonese bitmap correction, with immutable review stages."""
import json
import sys
import csv
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/MILAN_CREMONESE'
core.OUT=OUT
core.BACKUP=OUT.parent/'MAINZ_COMPLETION/provinces_candidate.png'
core.REGIONS={'STATE_LOMBARDY'}
core.REGION_FILE='map_data/state_regions/01_south_europe.txt'

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    source=core.ROOT/'docs/reports/map/MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/lombardy_west_1750_1600.png'
    im=Image.open(source).convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for name,box in [('SOURCE_BORDER',(1130,450,1480,650)),('SOURCE_CITIES',(990,380,1440,990))]:
        crop=im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3));d=ImageDraw.Draw(crop)
        for x in range((box[0]//20+1)*20,box[2],20):
            d.line(((x-box[0])*3,0,(x-box[0])*3,crop.height),fill='#3085df');d.text(((x-box[0])*3+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//20+1)*20,box[3],20):
            d.line((0,(y-box[1])*3,crop.width,(y-box[1])*3),fill='#3085df');d.text((0,(y-box[1])*3+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=[r for r in csv.DictReader(f) if r['State_ID'] in {'STATE_LOMBARDY','STATE_VENETIA','STATE_EMILIA','STATE_PIEDMONT'}]
    core.dump('NATIVE_ANCHORS.json',rows)
    print(json.dumps([{k:r[k] for k in ['Hub_Name','Hub_Type','Locator_X','Locator_Y','Locator_Sampled_RGB']} for r in rows],ensure_ascii=False))

def presentation():
    """Technical political preview of actual reviewed pixels, not an AI map."""
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    geometry=json.loads((OUT/'GEOMETRY.json').read_text())
    before=core.packed(core.ROOT/baseline['bitmap_backup'])
    after=core.packed(core.ROOT/'map_data/provinces.png')
    assert core.sha(core.ROOT/'map_data/provinces.png')==geometry['candidate_sha256']
    old={int(r['key'][0][1:],16):r['key'][2] for r in baseline['inventory']['owners']}
    new={**old,**{int(r['rgb'][1:],16):r['owner'] for r in geometry['assignments']}}
    palette={'AUS':'#b5b0d7','VEN':'#69b9ac','SWI':'#bd6861','SAR':'#809bac','PAR':'#acd19e','MOD':'#dec788'}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    views=[]
    for title,bmp,owners in [('Avant : deux morceaux',before,old),('Après : territoire continu',after,new)]:
        local=bmp[960:1014,4284:4360];tags=np.array([owners.get(int(v),'?') for v in local.ravel()]).reshape(local.shape)
        arr=np.full((*local.shape,3),190,dtype=np.uint8)
        for tag,color in palette.items():arr[tags==tag]=ImageColor.getrgb(color)
        im=Image.fromarray(arr).resize((760,540),Image.Resampling.NEAREST)
        border=ImageDraw.Draw(im)
        # Draw on pixel boundaries, never replace a complete owned pixel.
        # Otherwise a narrow but genuinely connected territory looks severed.
        for y,x in zip(*np.where(tags[1:]!=tags[:-1])):
            border.line((x*10,(y+1)*10,(x+1)*10,(y+1)*10),fill='#282828',width=2)
        for y,x in zip(*np.where(tags[:,1:]!=tags[:,:-1])):
            border.line(((x+1)*10,y*10,(x+1)*10,(y+1)*10),fill='#282828',width=2)
        canvas=Image.new('RGB',(760,620),'white');canvas.paste(im,(0,40));d=ImageDraw.Draw(canvas)
        d.text((15,8),title,font=font,fill='black')
        for label,x,y in [('Milan',4304,991),('Venise',4320,977),('Crémonais',4318,998),('Mantoue',4336,1003)]:
            d.text(((x-4284)*10,(y-960)*10+40),label,font=font,fill='black',stroke_width=2,stroke_fill='white')
        d.text((10,584),'Violet : possessions autrichiennes / vert : Venise',font=font,fill='black')
        views.append(canvas)
    combined=Image.new('RGB',(1520,660),'white');combined.paste(views[0]);combined.paste(views[1],(760,0))
    ImageDraw.Draw(combined).text((10,629),'Aperçu des pixels appliqués ; approximation à la résolution du jeu, pas un tracé cadastral.',font=font,fill='black')
    combined.save(OUT/'POLITICAL_BEFORE_AFTER.png')
    print('Political before/after generated from immutable baseline and applied bitmap')

def audit_summary():
    reports={name:json.loads((OUT.parent/name/'VALIDATION.json').read_text()) for name in ['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE']}
    rows=[dict(lot=name,status=r['status'],passed=sum(bool(c['passed']) for c in r['checks']),checks=len(r['checks']),engine_tested=r['engine_tested']) for name,r in reports.items()]
    assert all(r['passed']==r['checks'] and r['status'].startswith('PASS') and not r['engine_tested'] for r in rows)
    core.dump('NON_REGRESSION.json',dict(status='PASS_STATIC_ENGINE_DEFERRED',suites=rows,
        applied_bitmap_sha256=core.sha(core.ROOT/'map_data/provinces.png'),registry_sha256=core.sha(core.active_registry_path()),
        inherited_format_warning='common/history/pops/01_south_europe.txt:846, whitespace-only line in unchanged Istrian scope; present in immutable baseline before this lot. Git diff --check against HEAD is therefore not globally clean.',
        game_policy='Do not launch until all HRE lots complete, as requested'))
    print(json.dumps(rows,ensure_ascii=False))

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'geometry':core.geometry,'prepare':core.prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps,'presentation':presentation,'audit-summary':audit_summary}[sys.argv[1]]()
