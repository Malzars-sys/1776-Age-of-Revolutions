"""MAP-1B evidence acquisition only. Never writes runtime or MAP1 files."""
from pathlib import Path
import hashlib, json, urllib.request, re, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/MAP1B'
E=OUT/'MAP1B_GEOGRAPHIC_EVIDENCE'
E.mkdir(parents=True,exist_ok=True)
def fetch(name,url):
    import urllib.parse
    url=urllib.parse.quote(url,safe=':/?=&%')
    p=E/name
    if p.exists(): return p
    req=urllib.request.Request(url,headers={'User-Agent':'HistoricalMapResearch/1.0 (noncommercial research)'})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(); meta={'url':url,'resolved_url':r.url,'content_type':r.headers.get('Content-Type'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'access_date':'2026-10-10'}
    p.write_bytes(b)
    p.with_suffix(p.suffix+'.metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(name,len(b),meta['content_type'])
    return p
if __name__=='__main__':
    if len(sys.argv)>2:
        p=fetch(sys.argv[1],sys.argv[2])
        if '--commons' in sys.argv:
            import html
            url=html.unescape(re.search(r'<div class="fullImageLink"[^>]*><a href="([^"]+)',p.read_text(encoding='utf-8')).group(1)).split('?')[0]
            fetch(p.stem+'.jpg',url)
        if '--preview' in sys.argv:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS=200000000
            im=Image.open(p); im.thumbnail((2200,1800)); im.save(E/(p.stem+'_overview.png'))
