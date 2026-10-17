"""MAP2Q continuation: independent evidence and population-policy delta.

Does not recapture, overwrite or reinterpret an earlier immutable baseline.
"""
from pathlib import Path
import json,sys,urllib.request,subprocess,hashlib
from html.parser import HTMLParser
import map2q_eutin as q

ROOT=q.ROOT
OUT=q.OUT/'CONTINUATION_R1'

def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'BASELINE.json').exists()
    manifest=q.load('INSTALLED_MANIFEST.json')
    assert all(q.core.sha(ROOT/p)==h for p,h in manifest['functional_files'].items())
    inventory=q.core.qa.inventory()
    dump('BASELINE.json',dict(inventory=inventory,runtime_hashes=q.economy.runtime_hashes(),
        original_pops=(ROOT/'common/history/pops/00_west_europe.txt').read_text(encoding='utf-8-sig'),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_index_sha256=q.core.sha(ROOT/'.git/index'),
        installed_manifest=manifest,
        earlier_q_artifacts={p.relative_to(ROOT).as_posix():q.core.sha(p) for p in q.OUT.rglob('*')
            if p.is_file() and OUT not in p.parents}))
    print('Continuation baseline captured; installed Q delta verified intact')

class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in {'a','link','img'}:
            value=d.get('href',d.get('src',''))
            if value and any(s in value.lower() for s in ['pdf','iiif','manifest','fulltext','alto','gct','epub','book','download']):print(tag,value)

def fetch():
    url=sys.argv[2];filename=sys.argv[3]
    assert '/' not in filename and '\\' not in filename
    folder=OUT/'EVIDENCE';folder.mkdir(parents=True,exist_ok=True)
    target=folder/filename;assert not target.exists()
    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 historical map research'})
    with urllib.request.urlopen(request,timeout=40) as r:
        data=r.read(30000001);ctype=r.headers.get('Content-Type','');final=r.url
    assert len(data)<30000000,'Source exceeds bounded evidence size'
    target.write_bytes(data)
    dump(filename+'.source.json',dict(url=url,final_url=final,bytes=len(data),sha256=q.core.sha(target),content_type=ctype))
    print(filename,len(data),ctype)
    if 'html' in ctype:Links().feed(data.decode('utf8',errors='replace'))

def pdf_extract():
    from pypdf import PdfReader
    path=OUT/'EVIDENCE'/sys.argv[2];reader=PdfReader(path)
    print('PAGES',len(reader.pages))
    texts=[p.extract_text() for p in reader.pages]
    (OUT/'EVIDENCE'/(path.stem+'_TEXT.txt')).write_text('\n\f\n'.join(texts),encoding='utf8')
    for i,t in enumerate(texts):
        if any(s in t.lower() for s in ['1776','1769','1775','bevölkerung','volksmenge']):
            print('PAGE',i+1,t[:300].replace('\n',' '))

def kohli_pages():
    """Fetch only explicitly selected canvases using URLs published in the manifest."""
    import re
    folder=OUT/'EVIDENCE'
    manifest=json.loads((folder/'KOHLI_MANIFEST.json').read_text(encoding='utf8'))
    pages=[int(s) for s in sys.argv[2:]]
    assert len(pages)<=20
    class Plain(HTMLParser):
        def __init__(self):super().__init__();self.text=[]
        def handle_data(self,data):self.text.append(data)
    for number in pages:
        canvas=manifest['items'][number-1]
        url=canvas['seeAlso'][0]['id'];target=folder/f'KOHLI_{number:03d}.html'
        if not target.exists():
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 historical research'})
            with urllib.request.urlopen(req,timeout=40) as response:data=response.read(2000000)
            target.write_bytes(data)
            dump(target.name+'.source.json',dict(url=url,sha256=q.core.sha(target)))
        p=Plain();p.feed(target.read_text(encoding='utf8'))
        text=' '.join(' '.join(p.text).split())
        (folder/f'KOHLI_{number:03d}.txt').write_text(text,encoding='utf8')
        print('CANVAS',number,canvas['label'],text)

def recheck():
    """Replay installed Q without overwriting any earlier validation artifact."""
    q.dump=lambda name,obj:dump('RECHECK_'+name,obj)
    q.validate()

def verify():
    import os
    baseline=json.loads((OUT/'BASELINE.json').read_text(encoding='utf8'))
    current=q.economy.runtime_hashes()
    checks=[]
    def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    check('All runtime files unchanged during demographic investigation',current==baseline['runtime_hashes'])
    check('Imperial register unchanged',q.core.sha(q.core.active_registry_path())==baseline['installed_manifest']['registry_sha256'])
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==baseline['git_head'])
    check('Git index unchanged',q.core.sha(ROOT/'.git/index')==baseline['git_index_sha256'])
    allowed={'docs/reports/map/MAP2Q/REPORT.md','docs/reports/map/MAP2Q/NEXT_STEPS.md',
             'docs/reports/map/MAP2Q/HISTORICAL_EVIDENCE.md'}
    changed=[p for p,h in baseline['earlier_q_artifacts'].items() if not (ROOT/p).exists() or q.core.sha(ROOT/p)!=h]
    check('Earlier evidence and baselines preserved; only three narrative reports may be annotated',set(changed)<=allowed,changed)
    evidence=json.loads((OUT/'POPULATION_EVIDENCE.json').read_text(encoding='utf8'))
    check('No 1819 census relabelled as 1776',evidence['installed_1776_target'] is None and all(r['reference_year']==1819 for r in evidence['read_counts']))
    check('Source totals remain distinct',[(r['territory'],r['people']) for r in evidence['read_counts']]==[('Eutin city',2652),('Amt Eutin',6824)])
    env={**os.environ,'PYTHONPATH':str(ROOT/'tools'),'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}
    command=[sys.executable,'-B','-X','utf8','-m','unittest','test_map2q_eutin']
    test=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf8',errors='replace')
    check('Five targeted Q replay/unit tests',test.returncode==0,test.stdout+test.stderr)
    dump('VERIFICATION.json',dict(status='MAP2Q_PARTIAL_HISTORICAL_POPULATION_UNRESOLVED',
        passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,unit_command=command,
        runtime_test='NOT_RUN',new_runtime_changes=[],population_adjustment_people=0,
        explanation='No defensible 1776 target for the installed nucleus. World total is not a policy constraint; it is unchanged because no correction was invented.'))
    print(test.stdout+test.stderr)
    print(sum(c['passed'] for c in checks),'/',len(checks),'checks; historical population unresolved')
    if not all(c['passed'] for c in checks):raise SystemExit(1)

if __name__=='__main__':globals()[sys.argv[1]]()
