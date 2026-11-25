"""Compare exact serialized sections at the same date; no save edits or melting."""
import argparse, hashlib, json
from pathlib import Path
from simperf56_ai_cohorts import LAB
from simperf56_save_state import sections

ap=argparse.ArgumentParser();ap.add_argument('normal');ap.add_argument('diagnostic');a=ap.parse_args()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def get(label):
    r=read(LAB/(label+'_RESULTS.json'));p=read(r['native_proof']);save=Path(p['save'])
    raw=save.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['sha256']
    text=raw.decode('utf-8-sig').replace('\r\n','\n');spans=sections(text)
    return r,p,{k:dict(characters=b-c,sha256=hashlib.sha256(text[c:b].encode('utf-8')).hexdigest()) for k,(c,b) in spans.items()}
nr,np,ns=get(a.normal);dr,dp,ds=get(a.diagnostic)
assert np['date']==dp['date']
assert read(nr['source_proof'])['sha256']==read(dr['source_proof'])['sha256']
common=sorted(set(ns)&set(ds));changed={k:dict(normal=ns[k],diagnostic=ds[k]) for k in common if ns[k]!=ds[k]}
equal=[k for k in common if ns[k]==ds[k]]
out=dict(normal=a.normal,diagnostic=a.diagnostic,date=np['date'],normal_save=np['save'],diagnostic_save=dp['save'],
    source_hash_equal=True,normal_sections=ns,diagnostic_sections=ds,equal_sections=equal,changed_sections=changed,
    added=sorted(set(ds)-set(ns)),removed=sorted(set(ns)-set(ds)),
    scope='Exact text-section equality at one matched save date, not a proof of identical intermediate decisions, callback execution, CPU causality or future gameplay equivalence.')
dest=LAB/(a.normal+'_'+a.diagnostic+'_MATCHED_POST_SECTIONS.json')
with dest.open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps(dict(normal=a.normal,diagnostic=a.diagnostic,date=out['date'],equal=len(equal),changed=list(changed),added=out['added'],removed=out['removed']),indent=2))
