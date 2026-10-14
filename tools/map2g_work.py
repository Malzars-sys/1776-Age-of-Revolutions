"""Focused R5 baseline: exact dirty histories and hashes, not a full archive."""
import collections as C,csv,json,subprocess,sys
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2c_work import ROOT,GAME,sha,source_bitmap,geo_data
from map2e_work import GIT
OUT=ROOT/'docs/reports/map/MAP2G';BASE=OUT/'MAP2G_BASELINE.json'
CONTROL=Path('C:/Users/simeo/.codex/visualizations/2026/09/08/01a080b1-616e-71b2-85c3-0d7759724725')
TARGETS={r['State_ID'] for r in csv.DictReader((ROOT/'docs/reports/map/MAP_1776_9_REGIONS.csv').open(encoding='utf-8-sig')) if r['Region_ID']=='R5_EAST_ASIA'}
def dump(name,data):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def snapshot():
 assert not BASE.exists(),'Never overwrite baseline'
 receipt=json.loads((CONTROL/'checkpoint_map2f_validated_before_map2g/REMOTE_VALIDATION.json').read_text())
 assert receipt['status']=='PASS_REMOTE_EXACT_RESTORATION' and receipt['sha256_all_files']=='MATCH'
 folders=['common','map_data','gfx','gui','events','localization','music','.metadata']+[f'docs/reports/map/MAP2{x}' for x in 'ABCDEF']+['docs/reports/map/MAP1C','docs/reports/historical_workforce_revision_1776']
 hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
 originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names','map_data/state_regions'] for p in (ROOT/f).rglob('*.txt')}
 inv=qa.inventory();assert sum(r['count'] for r in inv['pops'])==835804980 and len(inv['duplicates'])==50
 git={k:subprocess.check_output([GIT,*args],cwd=ROOT,text=True).strip() for k,args in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 dump('MAP2G_BASELINE.json',{'inventory':inv,'originals':originals,'hashes':hashes,'bitmap_sha256':sha(source_bitmap()),'git':git,'scope':sorted(TARGETS),'backup':receipt})
 dump('GEOGRAPHY.json',json.loads((CONTROL/'R5_GEOGRAPHY.json').read_text()))
 dump('BACKUP_MAP2F_VERIFICATION.json',receipt)
 raw=subprocess.check_output([GIT,'show','georg3mx-map-rework:common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
 now=originals['common/history/states/00_states.txt'];current={n.key:qa.norm(n) for n in cw.walk(cw.parse(now)) if n.key.removeprefix('s:') in TARGETS}
 differences=[{'state':n.key,'collaborator':qa.norm(n),'current':current[n.key]} for n in cw.walk(cw.parse(raw)) if n.key in current and qa.norm(n)!=current[n.key]]
 dump('COLLABORATOR_COMPARISON.json',differences)
 print('Baseline:',len(TARGETS),'regions, population835804980, 50 inherited duplicates;',len(differences),'different collaborator state scopes')
if __name__=='__main__':snapshot()
