"""MAP-2D baseline and focused inspection. Never overwrite the dirty-tree baseline."""
from pathlib import Path
import hashlib, json, sys, subprocess, collections as C
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective, values, prov
from map2c_work import packed, source_bitmap, geo_data

ROOT=qa.ROOT
GAME=qa.GAME
OUT=ROOT/'docs/reports/map/MAP2D'
BASE=OUT/'MAP2D_BASELINE.json'
TARGETS={'STATE_BESSARABIA','STATE_MOLDAVIA','STATE_BUKOVINA','STATE_DOBRUDJA','STATE_CRIMEA','STATE_CHERSON','STATE_TAURIDA','STATE_KUBAN'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    assert not BASE.exists(), 'Baseline already exists: never replace it'
    OUT.mkdir(parents=True,exist_ok=True)
    folders=['common','map_data','gfx','localization','events','.metadata','docs/reports/map/MAP2A','docs/reports/map/MAP2B','docs/reports/map/MAP2C','docs/reports/historical_workforce_revision_1776']
    hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
    originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/diplomatic_actions','common/treaty_articles','common/ai_strategies','map_data/state_regions'] for p in (ROOT/f).rglob('*.txt')}
    (OUT/'provinces_before.png').write_bytes(source_bitmap().read_bytes())
    inv=qa.inventory()
    BASE.write_text(json.dumps({'hashes':hashes,'originals':originals,'inventory':inv,'bitmap_hash':sha(source_bitmap())},ensure_ascii=False),encoding='utf-8')
    print('Baseline saved',len(hashes),'files; population',sum(x['count'] for x in inv['pops']))
def inspect():
    inv=qa.inventory()
    for field in ['owners','regional_pop','buildings','units']:
        print('\n'+field)
        for r in inv[field]:
            k=r['key']
            if (k[1] if field in ['owners','units'] else k[0]) in TARGETS or (field=='units' and k[2] in TARGETS): print(r)
    for folder in ['states','pops','buildings']:
        for p in effective(ROOT,GAME,'common/history/'+folder):
            hits=[s for s in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))) if s.key.removeprefix('s:') in TARGETS]
            if hits: print(folder,p.relative_to(ROOT) if p.is_relative_to(ROOT) else p,len(hits))
def brief():
    inv=json.loads(BASE.read_text(encoding='utf-8'))['inventory']
    for s in sorted(TARGETS):
        pp=[r for r in inv['regional_pop'] if r['key'][0]==s]
        bb=[r for r in inv['buildings'] if r['key'][0]==s]
        print(s,'population',sum(r['count'] for r in pp))
        for r in bb:
            n=json.loads(r['key'][2]);kind=next(v[2] for v in n[2] if v[0]=='building')
            print(' ',r['key'][1],kind,'records',r['count'])
    git='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
    raw=subprocess.check_output([git,'show','georg3mx-map-rework:common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
    selected={s.key:qa.norm(s) for s in cw.walk(cw.parse(raw)) if s.key.removeprefix('s:') in TARGETS}
    (OUT/'COLLABORATOR_COMPARISON.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
    for k,s in selected.items():print('Collaborator',k,[n for n in s[2] if n[0]=='create_state'])
    # Physical river grid: inspect Bug/Dnieper and northern Bessarabia without fitting town centroids.
    river=Image.open(GAME/'map_data/rivers.png').convert('RGB')
    for name,box in {'estuaries':(4780,915,4865,992),'north_bessarabia':(4680,887,4760,945)}.items():
        x0,y0,x1,y1=box;scale=10;im=river.crop(box).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
        for x in range(x0,x1,5):d.line(((x-x0)*scale,0,(x-x0)*scale,im.height),fill=(190,190,190));d.text(((x-x0)*scale,0),str(x),fill='black',font=font)
        for y in range(y0,y1,5):d.line((0,(y-y0)*scale,im.width,(y-y0)*scale),fill=(190,190,190));d.text((0,(y-y0)*scale),str(y),fill='black',font=font)
        im.save(OUT/(name+'_rivers.png'))
def preview(label):
    inv=qa.inventory(); rgb=packed(source_bitmap()); defs,hubs,names=geo_data()
    owner={r['key'][0]:r['key'][2] for r in inv['owners']}
    regions={v:s for s,vs in defs.items() for v in vs}
    colors={'MOL':(92,177,115),'TUR':(207,94,89),'CRI':(224,180,82),'RUS':(98,133,208),'AUS':(169,137,195),'PLC':(181,178,154),'WAL':(113,193,183)}
    for name,box in {'bessarabia':(4660,860,4820,1045),'black_sea':(4765,875,4960,1045)}.items():
        x0,y0,x1,y1=box; crop=rgb[y0:y1,x0:x1]; canvas=np.zeros((*crop.shape,3),np.uint8); rows=[]
        for c in np.unique(crop):
            v='x%06X'%int(c); tag=owner.get(v,'SEA'); mask=crop==c
            canvas[mask]=colors.get(tag,(47,63,73)); ys,xs=np.where(mask)
            rows.append([v,regions.get(v,''),tag,len(xs),float(xs.mean()+x0),float(ys.mean()+y0)])
        bd=np.zeros(crop.shape,bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];canvas[bd]=(28,30,35)
        scale=7;im=Image.fromarray(canvas).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
        for v,s,tag,n,x,y in rows:
            if s in TARGETS and n>=15:d.text(((x-x0)*scale,(y-y0)*scale),v+' '+tag,fill='white',stroke_width=1,stroke_fill='black',anchor='mm',font=font)
        im.save(OUT/(name+'_'+label+'.png'))
        (OUT/(name+'_'+label+'_rgb.json')).write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print('Previews',label)
if __name__=='__main__':
    if sys.argv[1]=='snapshot': snapshot()
    elif sys.argv[1]=='inspect': inspect()
    elif sys.argv[1]=='preview': preview(sys.argv[2])
    elif sys.argv[1]=='brief': brief()
