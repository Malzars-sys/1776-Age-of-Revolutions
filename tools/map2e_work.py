"""MAP-2E: differential baseline and focused native-grid evidence, not a world atlas."""
from pathlib import Path
import hashlib, json, re, sys, subprocess, collections as C
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective
from map2c_work import packed, source_bitmap, geo_data

ROOT=qa.ROOT; GAME=qa.GAME
OUT=ROOT/'docs/reports/map/MAP2E'; BASE=OUT/'MAP2E_BASELINE.json'
TARGETS={'STATE_KUBAN','STATE_NORTH_CAUCASUS','STATE_STAVROPOL','STATE_DAGESTAN','STATE_GREATER_CAUCASUS','STATE_ARMENIA','STATE_ELIZAVETPOL','STATE_AZERBAIJAN','STATE_KARS'}
CHECKPOINT='cb401334bc58f2aa0747fa1a45567f3ab54a14fe'
GIT='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    assert not BASE.exists(), 'Never overwrite the actual dirty-tree baseline'
    OUT.mkdir(parents=True,exist_ok=True)
    folders=['common','map_data','gfx','events','localization','.metadata','docs/reports/map/MAP1C','docs/reports/map/MAP2A','docs/reports/map/MAP2B','docs/reports/map/MAP2C','docs/reports/map/MAP2D','docs/reports/historical_workforce_revision_1776']
    hashes={p.relative_to(ROOT).as_posix():sha(p) for folder in folders for p in (ROOT/folder).rglob('*') if p.is_file()}
    originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for folder in ['common/history','common/country_definitions','common/dynamic_country_names','map_data/state_regions'] for p in (ROOT/folder).rglob('*.txt')}
    git={k:subprocess.check_output([GIT,*args],cwd=ROOT).decode().strip() for k,args in {'head':['rev-parse','HEAD'],'status':['status','--porcelain=v1','--untracked-files=all'],'refs':['show-ref']}.items()}
    git['index_sha256']=sha(ROOT/'.git/index')
    inv=qa.inventory()
    BASE.write_text(json.dumps({'checkpoint':CHECKPOINT,'hashes':hashes,'originals':originals,'inventory':inv,'bitmap_sha256':sha(source_bitmap()),'git':git},ensure_ascii=False),encoding='utf-8')
    assert sum(r['count'] for r in inv['pops'])==835804980
    print('Baseline: world 835804980; protected files',len(hashes),'duplicates',len(inv['duplicates']),'errors',len(inv['errors']))
def evidence(label):
    OUT.mkdir(parents=True,exist_ok=True)
    rgb=packed(source_bitmap());defs,hubs,names=geo_data(); inv=qa.inventory()
    owner=C.defaultdict(list)
    for r in inv['owners']:owner[r['key'][0]].append(r['key'][2])
    region_ids={s.key:str(s.one('id')) for p in effective(ROOT,GAME,'map_data/state_regions') for s in cw.parse(p.read_text(encoding='utf-8-sig'))}
    locators={}
    for kind in ['city','port','farm','wood','mine']:
        p=ROOT/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        if not p.exists():p=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        pos={ident:(float(x),3616-float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',p.read_text(encoding='utf-8-sig'))}
        for sid in TARGETS:
            if region_ids[sid] not in pos:continue
            x,y=pos[region_ids[sid]]; actual='x%06X'%int(rgb[int(y),int(x)])
            locators[sid+'|'+kind]={'name':names.get('HUB_NAME_'+sid+'_'+kind,''),'x':x,'y':y,'actual_rgb':actual,'hub_rgb':hubs[sid].get(kind),'owners':owner.get(actual,[])}
    rows={}
    for sid in sorted(TARGETS):
        for v in defs[sid]:
            yy,xx=np.where(rgb==int(v[1:],16))
            rows[v]={'state':sid,'owners':owner.get(v,[]),'pixels':int(len(xx)),'bbox':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'centroid':[float(xx.mean()),float(yy.mean())]}
    (OUT/('GEOGRAPHY_'+label+'.json')).write_text(json.dumps({'provinces':rows,'locators':locators},indent=2),encoding='utf-8')
    for case,box in {'north':(4935,950,5215,1110),'south':(4995,1035,5250,1195)}.items():
        x0,y0,x1,y1=box; a=rgb[y0:y1,x0:x1]; canvas=np.zeros((*a.shape,3),np.uint8)
        palette={'RUS':(78,127,190),'GEO':(185,72,65),'IMR':(181,132,57),'ABK':(69,160,110),'AZB':(176,97,170),'ARM':(146,107,67),'KRB':(167,142,206),'SHK':(151,170,89),'GJA':(126,175,161),'TAL':(180,173,77),'NAK':(169,129,69),'SRV':(196,134,83),'PER':(216,195,141),'TUR':(191,91,122),'CIR':(108,167,68),'CHC':(74,114,107),'CAUC':(139,150,155),'CRI':(232,189,83)}
        for c in np.unique(a):
            v='x%06X'%int(c); oo=owner.get(v,[]);canvas[a==c]=(240,50,245) if len(oo)>1 else palette.get(oo[0] if oo else '',(40,53,68))
        bd=np.zeros(a.shape,bool);bd[1:]|=a[1:]!=a[:-1];bd[:,1:]|=a[:,1:]!=a[:,:-1];canvas[bd]=(25,28,32)
        scale=5;im=Image.fromarray(canvas).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',10)
        for v,r in rows.items():
            x,y=r['centroid']
            if x0<=x<x1 and y0<=y<y1:d.text(((x-x0)*scale,(y-y0)*scale),v+' '+'/'.join(r['owners']),fill='white',stroke_width=1,stroke_fill='black',anchor='mm',font=font)
        for k,r in locators.items():
            x,y=r['x'],r['y']
            if x0<=x<x1 and y0<=y<y1:d.ellipse(((x-x0)*scale-2,(y-y0)*scale-2,(x-x0)*scale+2,(y-y0)*scale+2),fill='yellow')
        im.save(OUT/(case+'_'+label+'.png'))
    print('Focused evidence saved',label)
def inspect():
    b=json.loads(BASE.read_text(encoding='utf-8'))
    for field in ['buildings','units']:
        for r in b['inventory'][field]:
            if (r['key'][0] if field=='buildings' else r['key'][2]) in TARGETS: print(field,r)
    for folder in ['countries','characters','military_formations']:
        for p in effective(ROOT,GAME,'common/history/'+folder):
            raw=p.read_text(encoding='utf-8-sig')
            if re.search(r'c:(ARM|AZB|ABK)\b',raw):print(folder,p,raw[:8000])
    raw=subprocess.check_output([GIT,'show','georg3mx-map-rework:common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
    selected={s.key:qa.norm(s) for s in cw.walk(cw.parse(raw)) if s.key.removeprefix('s:') in TARGETS}
    (OUT/'COLLABORATOR_COMPARISON.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Collaborator',json.dumps(selected,ensure_ascii=False)[:15000])
def fit():
    data=json.loads((OUT/'GEOGRAPHY_before.json').read_text(encoding='utf-8')); ll=data['locators']
    # Modern WGS84 centres identify geography, not a claim to 1776 city limits.
    # Retain every control and residual; no exclusion of unfavourable hubs.
    anchors={'STATE_GREATER_CAUCASUS|city':(44.827,41.715),'STATE_KARS|port':(41.641,41.645),'STATE_GREATER_CAUCASUS|port':(41.672,42.146),'STATE_GREATER_CAUCASUS|farm':(41.025,43.002),'STATE_ARMENIA|city':(44.513,40.181),'STATE_ELIZAVETPOL|wood':(46.751,39.758),'STATE_DAGESTAN|mine':(48.291,42.058),'STATE_DAGESTAN|wood':(46.716,43.846),'STATE_AZERBAIJAN|wood':(48.512,41.361),'STATE_AZERBAIJAN|mine':(49.867,40.409),'STATE_NORTH_CAUCASUS|farm':(43.607,43.485)}
    # Local quadratic fit allows the native game's latitude distortion.
    feat=lambda x,y:[1,x,y,x*x,x*y,y*y]
    X=np.array([feat(*a) for a in anchors.values()]); Y=np.array([[ll[k]['x'],ll[k]['y']] for k in anchors]);coef=np.linalg.lstsq(X,Y,rcond=None)[0]
    controls=[]
    for (k,a),y,pr in zip(anchors.items(),Y,X@coef):controls.append({'locator':k,'modern_lon_lat':a,'native_xy':y.tolist(),'fitted_xy':pr.tolist(),'residual_pixels':float(np.linalg.norm(y-pr))})
    rgb=packed(source_bitmap()); tests={}
    for name,a in {'Mozdok':(44.656,43.747),'Akhaltsikhe':(42.987,41.639),'Akhalkalaki':(43.487,41.405),'Lankaran':(48.851,38.754)}.items():
        x,y=np.array(feat(*a))@coef;v='x%06X'%int(rgb[round(y),round(x)]);tests[name]={'modern_lon_lat':a,'native_estimate_xy':[float(x),float(y)],'rgb_at_estimate':v,'geometry':data['provinces'].get(v)}
    result={'method':'All eleven independent geographical city controls; local quadratic least squares. Whole RGB approximation, not a cadastral assertion. Locator identities/modern coordinates are geographically approximate.','controls':controls,'rms_pixels':float(np.sqrt(np.mean(np.sum((X@coef-Y)**2,axis=1)))),'tests':tests}
    (OUT/'LOCAL_GEOGRAPHIC_FIT.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':
    if sys.argv[1]=='snapshot':snapshot()
    elif sys.argv[1]=='evidence':evidence(sys.argv[2])
    elif sys.argv[1]=='inspect':inspect()
    elif sys.argv[1]=='fit':fit()
