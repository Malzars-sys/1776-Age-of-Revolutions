"""MAP2K differential baseline and patch preparation, main Git read-only."""
import json,sys,subprocess,hashlib
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2c_work import source_bitmap
ROOT=qa.ROOT; GAME=qa.GAME; OUT=ROOT/'docs/reports/map/MAP2K'; BASE=OUT/'BASELINE.json'
CONTROL=Path('C:/Users/simeo/.codex/visualizations/2026/09/08/01a080b1-616e-71b2-85c3-0d7759724725')
GIT='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,value):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def capture():
 assert not BASE.exists(),'Never replace a pre-edit baseline'
 receipt=json.loads((CONTROL/'checkpoint_map2j_validated_before_map2k/REMOTE_VALIDATION.json').read_text())
 assert receipt['status']=='PASS_REMOTE_EXACT_RESTORATION'
 inv=qa.inventory();assert sum(r['count'] for r in inv['pops'])==835804980
 folders=['common','map_data','gfx','events','localization','gui','music','.metadata']+[f'docs/reports/map/MAP2{x}' for x in 'ABCDEFGHIJ']
 hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
 originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names','map_data/state_regions'] for p in (ROOT/f).rglob('*.txt')}
 git={k:subprocess.check_output([GIT,*args],cwd=ROOT,text=True).strip() for k,args in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 dump('BASELINE.json',dict(inventory=inv,hashes=hashes,originals=originals,git=git,bitmap_sha256=sha(source_bitmap()),backup=receipt,MAP2J_validation='Explicit user confirmation; no local separate MAP2J report found. Preserve current validated workspace.'))
 print('Captured',len(hashes),'protected files;',len(inv['duplicates']),'inherited duplicate RGBs; population 835804980')
if __name__=='__main__':capture()
