"""Read-only HRE coverage diagnostics. Never executes an installer or writes runtime files.

All outputs are confined to SERG_GLOBAL_CLOSURE_AUDIT. Use Python -B.
"""
from pathlib import Path
import collections, hashlib, json, subprocess, sys, datetime
import numpy as np
from PIL import Image
import validate_map2a as qa
import map2l_registry as registry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT'
RUNTIME=('common','map_data','gfx','gui','events','localization','localisation','music','sound')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8',errors='replace').strip()
def hashes():
    return {p.relative_to(ROOT).as_posix():digest(p) for name in RUNTIME for p in (ROOT/name).rglob('*') if p.is_file()}
def collect():
    if (OUT/'BASELINE.json').exists(): raise RuntimeError('Immutable baseline already exists')
    idx=ROOT/git('rev-parse','--git-path','index')
    save('BASELINE.json',dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_hash=digest(idx),status=git('status','--porcelain=v1','--untracked-files=all').splitlines(),runtime_hashes=hashes()))
    inv=qa.inventory(); save('CURRENT_INVENTORY.json',inv)
    img=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=(img[:,:,0]<<16)|(img[:,:,1]<<8)|img[:,:,2]
    colors,counts=np.unique(packed,return_counts=True)
    cellcount={'x'+format(int(c),'06X'):int(n) for c,n in zip(colors,counts)}
    owners=collections.defaultdict(list)
    for r in inv['owners']: owners[r['key'][0]].append(r['key'][1:])
    reg=json.loads(registry.active_registry_path().read_text(encoding='utf-8-sig'))
    reg_checks=[dict(**r,bitmap_cells=cellcount.get(r['rgb'],0),actual_owners=owners[r['rgb']],match=owners[r['rgb']]==[[r['state'],r['beneficiary']]]) for r in reg]
    save('REGISTRY_CHECKS.json',reg_checks)
    layers=[]; geos=[]
    for order,p in enumerate(registry.approved_lot_dirs(),1):
        m=json.loads((p/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8-sig'))
        gpath=p/'GEOMETRY.json'; geo=json.loads(gpath.read_text(encoding='utf-8-sig')) if gpath.exists() else {}
        if geo.get('assignments'): geos.append(geo)
        layers.append(dict(order=order,path=p.relative_to(ROOT).as_posix(),new_members=m.get('new_members',[]),free_cities=m.get('free_cities',[]),regions=m.get('replaced_regions'),new_rgb_count=len(m.get('new_provinces',[])),classification=geo.get('classification'),geometry_rows=len(geo.get('assignments',[]))))
    effective=registry.effective_assignments(geos)
    checks=[]
    for r in effective:
        bad=[]
        for x,y in r.get('cells',[]):
            if int(packed[y,x])!=int(r['rgb'][1:],16): bad.append([x,y])
        actual=owners[r['rgb']]
        checks.append(dict(rgb=r['rgb'],state=r.get('state'),owner=r.get('owner'),expected_cells=len(r.get('cells',[])),bad_cells=bad,actual_owners=actual,owner_match=actual==[[r.get('state'),r.get('owner')]]))
    save('LAYERS.json',layers);save('EFFECTIVE_GEOMETRY_CHECKS.json',checks)
    save('RGB_COUNTS.json',cellcount)
    # All documentary metadata; includes non-MAP work. Content remains in original files.
    index=[]
    for root in (ROOT/'docs',ROOT/'tools'):
        for p in root.rglob('*'):
            if not p.is_file() or OUT in p.parents or p.suffix.lower() not in {'.md','.csv','.json','.py','.cjs','.js'} or p.stat().st_size>2_000_000: continue
            text=p.read_text(encoding='utf-8-sig',errors='replace')
            if not any(s in text.lower() for s in ('imperial','saint-empire','hre_','franconia','hohenlohe','eichsfeld')): continue
            hits=[dict(line=i,text=line[:500]) for i,line in enumerate(text.splitlines(),1) if any(s in line.lower() for s in ('pass_runtime','user_validat','attestation','not_tested','unresolved','non audité','bloqu','différ','category c','catégorie c','frozen 1776','historical source','https://'))]
            index.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p),lines=len(text.splitlines()),hits=hits[:100]))
    save('DOCUMENT_INDEX.json',index)
    summary=dict(registry_rows=len(reg),registry_mismatches=sum(not r['match'] for r in reg_checks),layers=len(layers),effective_geometry_rows=len(checks),bad_geometry_rows=sum(bool(r['bad_cells']) for r in checks),wrong_owner_rows=sum(not r['owner_match'] for r in checks),world_population=sum(r['count'] for r in inv['pops']),duplicates=inv['duplicates'],errors=inv['errors'],indexed_documents=len(index),bitmap_size=list(packed.shape[::-1]))
    save('DIAGNOSTIC_SUMMARY.json',summary);print(json.dumps(summary,ensure_ascii=False))
def protect():
    b=json.loads((OUT/'BASELINE.json').read_text());now=hashes()
    idx=ROOT/git('rev-parse','--git-path','index')
    changes={k:{'before':b['runtime_hashes'].get(k),'after':now.get(k)} for k in b['runtime_hashes'].keys()|now.keys() if b['runtime_hashes'].get(k)!=now.get(k)}
    obj=dict(head_unchanged=b['head']==git('rev-parse','HEAD'),index_unchanged=b['index_hash']==digest(idx),runtime_changes=changes,runtime_files=len(now),engine_test='NOT_RUN_BY_AGENT',functional_edits_authorized=False)
    save('PROTECTION_CHECK.json',obj);print(json.dumps(obj,ensure_ascii=False))
if __name__=='__main__':
    {'collect':collect,'protect':protect}[sys.argv[1]]()
