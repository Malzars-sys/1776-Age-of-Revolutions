"""Verify actual engine-resolved score override files using native load checksums."""
import argparse, json, re
from simperf56_ai_cohorts import LAB
ap=argparse.ArgumentParser();ap.add_argument('normal');ap.add_argument('diagnostic');ap.add_argument('--load-only',action='store_true');a=ap.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
setup=read(LAB/'SCORE_BASES_SETUP_20261118.json')
expected={r['file'].replace('\\','/').lower() for r in setup['changes']};assert len(expected)==9
def run(label):
    dirs=list((LAB/'runs').glob(label+'_*'));assert len(dirs)==1
    p=dirs[0]
    if not a.load_only:assert (p/'EXIT.json').exists()
    launch=read(p/'LAUNCH.json');text=(p/'stdout.txt').read_text(encoding='utf-8-sig',errors='replace')
    matches=re.findall(r'\[Checksum Builder\] \[[^\]]+\] (.+?) \[Contents Checksum\]: ([0-9a-fA-F]+)',text)
    hashes={k.replace('\\','/').lower():v.lower() for k,v in matches};assert len(hashes)>1000
    return launch,hashes
normal,nh=run(a.normal);diag,dh=run(a.diagnostic)
assert normal['executable_sha256']==diag['executable_sha256']
if not a.load_only:assert normal['settings_sha256']==diag['settings_sha256']
assert diag['mods']==normal['mods']+[setup['overlay'].replace('\\','/')]
changed={k:dict(normal=nh[k],diagnostic=dh[k]) for k in set(nh)&set(dh) if nh[k]!=dh[k]}
added=sorted(set(dh)-set(nh));removed=sorted(set(nh)-set(dh))
out=dict(normal=a.normal,diagnostic=a.diagnostic,expected_building_files=sorted(expected),
    load_only_preflight=a.load_only,not_a_performance_comparison=a.load_only,
    native_checksum_files_normal=len(nh),native_checksum_files_diagnostic=len(dh),changed=changed,
    added=added,removed=removed,actual_engine_loaded_changes_verified=set(changed)==expected and not added and not removed,
    scope='Actual engine-resolved virtual-file content hashes; not a CPU profile or proof of callback call frequency')
with (LAB/(a.diagnostic+('_RUNTIME_SCORE_PREFLIGHT.json' if a.load_only else '_RUNTIME_SCORE_PROOF.json'))).open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps({k:v for k,v in out.items() if k!='changed'},indent=2))
assert out['actual_engine_loaded_changes_verified'],'Do not interpret score performance before verifying the actual overrides'
