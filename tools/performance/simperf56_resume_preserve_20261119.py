"""Read current protected state and preserve changed normal files, never restore them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess
from simperf56_ai_cohorts import LAB, ROOT
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
baseline=json.loads((LAB/'ECONOMIC_PRESERVATION_BEFORE_20261118.json').read_text(encoding='utf-8'))
target=LAB/'resume_preservation_20261119';assert not target.exists();target.mkdir()
normal=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3')
out=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    compared_to='ECONOMIC_PRESERVATION_BEFORE_20261118.json',restored_files=0,groups={})
for key in ('normal_profile','protected_diplomacy','git_index','steam_executable','reference_files'):
    current={};changed=[];copies=[]
    for name,previous in baseline['groups'][key].items():
        p=Path(name);actual=sha(p) if p.is_file() else None;current[name]=actual
        if actual==previous:continue
        changed.append(dict(path=name,previous_sha256=previous,current_sha256=actual))
        if actual is not None and key in ('normal_profile','protected_diplomacy'):
            relative=p.relative_to(normal) if p.is_relative_to(normal) else Path('other')/hashlib.sha256(name.encode()).hexdigest()[:16]/p.name
            dest=target/'current_changed_files'/relative;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists()
            shutil.copy2(p,dest);assert sha(dest)==sha(p)==actual
            copies.append(dict(source=name,preserved=str(dest),sha256=actual))
    out['groups'][key]=dict(checked=len(current),current_hashes=current,changes=changed,preserved_copies=copies)
with (target/'RESUME_BEFORE.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps(dict(utc=out['utc'],head=out['head'],groups={k:dict(checked=v['checked'],changed=len(v['changes']),copied=len(v['preserved_copies'])) for k,v in out['groups'].items()}),indent=2))
