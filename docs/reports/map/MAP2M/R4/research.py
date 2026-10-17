"""MAP-2M-R4: research-only tools; never writes any runtime game file."""
import sys, json, csv, hashlib, time, urllib.request, re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from html.parser import HTMLParser

OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'map_data/provinces.png').is_file())
sys.path.insert(0,str(ROOT/'tools'))
import map2m_r3 as r3
import start_buildings_2026_10_15 as economy

def dump(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def sha(p):return r3.r2.core.sha(p)
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Do not replace the immutable R4 reference'
    b=r3.r2.core.qa.inventory();bmp=r3.r2.core.packed(ROOT/'map_data/provinces.png')
    assert sha(ROOT/'map_data/provinces.png')==r3.load('PLAN.json')['candidate_sha256']
    counts={f'x{v:06X}':int((bmp==v).sum()) for v in [0x567452,0xEDB010,0xFCC7B7]}
    assert list(counts.values())==[357,85,142]
    assert sum(v['count'] for v in b['pops'])==835804980
    earlier={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.parent.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json',dict(hashes=economy.runtime_hashes(),inventory=b,counts=counts,earlier_proofs=earlier,
        bitmap_sha256=sha(ROOT/'map_data/provinces.png'),git_head=r3.r2.head(),git_index_sha256=sha(ROOT/'.git/index')))
    dump('R3_USER_RUNTIME_VALIDATION.json',dict(status='PASS_RUNTIME_USER_VALIDATED',recorded_on='2026-10-15',
        evidence='User MAP-2M-R4 instructions: R3 checked manually in game, no new anomaly reported',
        automated_engine_test=False,simulation_duration=None,engine_logs_provided=False,historical_frontier_certification=False,
        scope=dict(swedish_RGB='x567452',swedish_cells=357,bromberg_RGB='xEDB010',bromberg_cells=85,polish_residual_cells=142),
        R4_research_not_runtime_validated=True))
    print('Captured R3 accepted geometry and all current functional changes; population 835804980.')

def audit():
    inventory=[]
    for p in sorted(OUT.parent.rglob('*')):
        if not p.is_file() or OUT in p.parents:continue
        if p.suffix.lower() in ['.png','.jpg','.jpeg','.geojson']:
            row=dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
            if p.suffix.lower()!='.geojson':
                with Image.open(p) as im:row['dimensions']=list(im.size)
            inventory.append(row)
    dump('EXISTING_ASSETS.json',inventory)
    records={}
    for name in ['PEENE/CANDIDATE_MODEL.json','NETZE/CANDIDATE_MODEL.json','R1/PEENE/CALIBRATION.json','R1/NETZE/CALIBRATION.json',
        'R2/GEOMETRY_REVIEW.json','R2/PHYSICAL_DIAGNOSTIC.json','R3/GEOMETRY_REVIEW.json']:
        p=OUT.parent/name;value=json.loads(p.read_text());records[name]=dict(sha256=sha(p),data=value)
    dump('PRIOR_TRANSFORMATIONS.json',records)
    print('Audited',len(inventory),'retained raster/vector assets; no downloads or old report rewrites.')

def fetch(name,url,timeout=35):
    p=OUT/'EVIDENCE'/name;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():print('Retained',name,p.stat().st_size);return
    t=time.monotonic()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'MAP-2M-R4 public historical map research'})
        with urllib.request.urlopen(req,timeout=timeout) as response:
            data=response.read(45000001);ctype=response.headers.get('Content-Type');final=response.url
        assert len(data)<=45000000,'Bounded acquisition exceeded'
        p.write_bytes(data)
        dump('EVIDENCE/'+name+'.source.json',dict(url=url,final_url=final,bytes=len(data),sha256=sha(p),content_type=ctype,seconds=time.monotonic()-t))
        print(name,len(data),ctype)
    except Exception as e:
        dump('EVIDENCE/'+name+'.failure.json',dict(url=url,error=str(e),seconds=time.monotonic()-t,
            retry_after=getattr(e,'headers',{}).get('Retry-After')));print('FAILED',name,str(e));raise

def links(name):
    class Parser(HTMLParser):
        def handle_starttag(self,tag,attrs):
            d=dict(attrs)
            for key in ['href','src','data-src']:
                if key in d and any(s in d[key].lower() for s in ['content','stabikat','digital','repro','mirabili','iiif','manifest','agad','viewer']):print(key,d[key])
    raw=(OUT/'EVIDENCE'/name).read_text(encoding='utf-8-sig');Parser().feed(raw)
    for line in raw.splitlines():
        if any(s in line.lower() for s in ['imageproperties','dzi','manifesturl','iiif','jp2','djvu','location.replace']):print(line.strip()[:1000])

def pfau():
    manifest=load('EVIDENCE/PFAU_MANIFEST.json');jobs=[]
    for canvas in manifest['items']:
        number=canvas['label']['none'][0].removeprefix('/').removesuffix('.jp2')
        if number not in ['0001','0002','39','45','46','47','48']:continue
        service=canvas['items'][0]['items'][0]['body']['service'][0]['id']
        jobs.append((f'PFAU_{number}.jpg',service+'/full/4000,/0/default.jpg'))
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda job:fetch(*job),jobs))

def contact():
    files=sorted((OUT/'EVIDENCE').glob('PFAU_*.jpg'));w=900;h=710
    canvas=Image.new('RGB',(w*2,h*((len(files)+1)//2)),'white');d=ImageDraw.Draw(canvas)
    for i,p in enumerate(files):
        im=Image.open(p).convert('RGB');im.thumbnail((w-20,h-40));x=(i%2)*w;y=(i//2)*h
        canvas.paste(im,(x,y+25));d.text((x+5,y+5),p.name+' | SOURCE orientation unchanged',fill='black')
    canvas.save(OUT/'PFAU_CONTACT.png')

if __name__=='__main__':
    if sys.argv[1]=='fetch':fetch(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='links':links(sys.argv[2])
    else:{'capture':capture,'audit':audit,'pfau':pfau,'contact':contact}[sys.argv[1]]()
