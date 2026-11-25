"""Reuse compiled graphics in new vanilla trial profiles; no settings/save edits."""
from pathlib import Path
import argparse, hashlib, json, shutil
from simperf56_ai_cohorts import LAB
ap=argparse.ArgumentParser();ap.add_argument('label',choices=('VAN_ON3','VAN_OFF3'));a=ap.parse_args()
assert len(list((LAB/'runs').glob('VAN_ON2_*/EXIT.json')))==1
src=LAB/'profiles/VAN_ON2/shadercache';dst=LAB/'profiles'/a.label/'shadercache'
assert src.is_dir() and dst.is_dir()
def hashes(folder):return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
before=hashes(dst);source=hashes(src)
receipt=LAB/(a.label+'_GRAPHICS_CACHE_REUSE.json');assert not receipt.exists()
shutil.copytree(src,dst,dirs_exist_ok=True)
after=hashes(dst);assert all(after[k]==h for k,h in source.items())
with receipt.open('x',encoding='utf-8') as f:json.dump(dict(source=str(src),destination=str(dst),before=before,source_hashes=source,
    copied=len(source),deleted=0,source_is_closed_trial=True,only_graphics_cache=True,settings_and_saves_unchanged=True,
    rationale='Reuse completed graphics compilation, excluded from throughput timing; both new trials receive the same compiled cache.'),f,indent=2)
print(json.dumps({'trial':a.label,'copied':len(source),'before_files':len(before),'after_files':len(after)}))
