"""Add a final preservation receipt; preserve drift instead of restoring files."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, shutil, subprocess
from simperf56_ai_cohorts import LAB, ROOT

ap=argparse.ArgumentParser();ap.add_argument('label');args=ap.parse_args()
assert args.label.isalnum()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
before=json.loads((LAB/'ECONOMIC_PRESERVATION_BEFORE_20261118.json').read_text(encoding='utf-8'))
dest=LAB/('final_preservation_'+args.label);assert not dest.exists();dest.mkdir()
out=dict(utc=datetime.now(timezone.utc).isoformat(),baseline='ECONOMIC_PRESERVATION_BEFORE_20261118.json',
         head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         groups={},restored_files=0,git_write_operations=0)
for group,paths in before['groups'].items():
    changes=[];copies=[]
    for name,old in paths.items():
        p=Path(name);current=sha(p) if p.is_file() else None
        if current==old:continue
        changes.append(dict(path=name,previous_sha256=old,current_sha256=current))
        if current and group in ('normal_profile','protected_diplomacy'):
            rel=Path(group)/hashlib.sha256(name.encode()).hexdigest()[:16]/p.name
            saved=dest/'current_changed_files'/rel;saved.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,saved);assert sha(saved)==sha(p)==current
            copies.append(dict(source=name,preserved=str(saved),sha256=current))
    out['groups'][group]=dict(checked=len(paths),unchanged=len(paths)-len(changes),changes=changes,preserved_copies=copies)
status=subprocess.check_output(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=normal'],cwd=ROOT)
with (dest/'GIT_STATUS.txt').open('xb') as f:f.write(status)
out['git_status_sha256']=hashlib.sha256(status).hexdigest()
with (dest/'PRESERVATION_FINAL.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps(dict(utc=out['utc'],head=out['head'],receipt=str(dest/'PRESERVATION_FINAL.json'),
    groups={k:dict(checked=v['checked'],unchanged=v['unchanged'],changed=len(v['changes'])) for k,v in out['groups'].items()}),indent=2))
