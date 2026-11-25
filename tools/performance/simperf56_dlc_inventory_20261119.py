"""Read native startup DLC declarations of completed current trials."""
import hashlib,json,re
from pathlib import Path
from simperf56_ai_cohorts import LAB
labels=('SCORC1','ECNC1','ECNC2','SCORC2','AIOFFC1','VAN_OFFC1','VAN_ONC1','VAN_ONR1','VAN_OFFR1','PROFC1')
rows={}
for label in labels:
    paths=list((LAB/'runs').glob(label+'_*'));assert len(paths)==1
    p=paths[0];assert (p/'EXIT.json').exists()
    declarations=[]
    for log in (p/'logs').glob('debug*.log'):
        text=log.read_text(encoding='utf-8-sig',errors='replace')
        for m in re.finditer(r'\]: DLC:\s*\n(.*?)\nMod:',text,re.S):
            lines=[x.strip() for x in m[1].splitlines() if x.strip()]
            declarations.append(dict(log=str(log),entries=lines))
    assert declarations,label
    signatures={tuple(x['entries']) for x in declarations};assert len(signatures)==1
    entries=list(next(iter(signatures)))
    launch=json.loads((p/'LAUNCH.json').read_text(encoding='utf-8-sig'))
    signature=Path(launch['profile'])/'dlc_signature';assert signature.is_file()
    rows[label]=dict(entries=entries,sha256=hashlib.sha256('\n'.join(entries).encode()).hexdigest(),
        native_signature_file=str(signature),native_signature_sha256=hashlib.sha256(signature.read_bytes()).hexdigest(),evidence=declarations)
same=len({(x['sha256'],x['native_signature_sha256']) for x in rows.values()})==1
with (LAB/'CURRENT_NATIVE_DLC_INVENTORY_20261119.json').open('x',encoding='utf-8') as f:
    json.dump(dict(trials=rows,all_identical=same,scope='Native startup DLC declaration, not an inventory of the separate canonical installation.'),f,indent=2)
print(json.dumps(dict(all_identical=same,trials={k:v['entries'] for k,v in rows.items()}),indent=2));assert same
