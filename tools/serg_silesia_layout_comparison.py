"""Read-only Silesian layout comparison; writes documentation evidence only."""
from pathlib import Path
import collections, hashlib, json, subprocess, sys
import numpy as np
from PIL import Image
import validate_map2a as qa
import map2b_patch as patch
import serg_closure_roadmap as roadmap

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT/'docs/reports/map/SERG_CLOSURE'
OUT = CANON/'SILESIA_STATE_LAYOUT_COMPARISON_2026_11_05'
REGIONS = ['STATE_UPPER_SILESIA','STATE_LOWER_SILESIA','STATE_MORAVIA','STATE_WEST_GALICIA']
AUSTRIAN = ['x71E080','xF0E080','x9061E0']
PRIOR = ['PRUSSIA_V1_2026_11_02','NORTH_SAXONY_1_2026_11_05','PRUSSIA_POLAND_2026_11_05','SC2-AUSTRIAN-SILESIA']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(name): return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def runtime():
    return {p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','events','map_data','gfx','gui','localization'] for p in (ROOT/folder).rglob('*') if p.is_file()}
def protected():
    paths=[p for name in PRIOR for p in (CANON/name).rglob('*') if p.is_file()]
    paths += [ROOT/'tools/map2l_registry.py']
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}
def git():
    ans={}
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current']),('git_dir',['rev-parse','--absolute-git-dir'])]:
        p=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True)
        ans[name]=p.stdout.strip()
    ans['index_sha256']=sha(Path(ans['git_dir'])/'index')
    return ans

def capture():
    assert not (OUT/'BASELINE.json').exists(), 'Never replace a baseline'
    OUT.mkdir(exist_ok=True)
    check=roadmap.check(); assert check['status']=='PASS',check
    state=roadmap.load_json(CANON/'ROADMAP_STATE.json')
    dump('BASELINE.json',dict(runtime=runtime(),protected=protected(),git=git(),canonical=check))
    for name in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']:
        (OUT/('BEFORE_'+name)).write_bytes((CANON/name).read_bytes())
    inv=qa.inventory()
    image=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=(image[:,:,0]<<16)|(image[:,:,1]<<8)|image[:,:,2]
    vals,counts=np.unique(packed,return_counts=True); sizes=dict(zip(vals.tolist(),counts.tolist()))
    rows=[]
    raw=(ROOT/'common/history/states/00_states.txt').read_text(encoding='utf-8-sig')
    for sid in REGIONS:
        owners=[dict(rgb=r['key'][0],owner=r['key'][2],declarations=r['count'],pixels=sizes.get(int(r['key'][0][1:],16),0)) for r in inv['owners'] if r['key'][1]==sid]
        pops=collections.Counter()
        for r in inv['regional_pop']:
            if r['key'][0]==sid:pops[r['key'][1]]+=r['count']
        buildings=[r for r in inv['buildings'] if r['key'][0]==sid]
        n=patch.state(raw,sid)
        rows.append(dict(state=sid,provinces=owners,populations_written=dict(pops),building_declarations=buildings,state_history=raw[n.start:n.end]))
    dump('CURRENT_INVENTORY.json',dict(regions=rows,austrian_candidate_rgb=AUSTRIAN,global_written_population=sum(r['count'] for r in inv['pops']),inventory_errors=inv['errors'],interpretation='Written declarations only; no engine overlay or cadastral certification'))
    ai=ROOT/'common/ai_strategies/00_default_strategy.txt'
    lines=ai.read_text(encoding='utf-8-sig').splitlines()
    assert all(t in '\n'.join(lines[1390:1407]) for t in ['is_split_state = yes','owner = ROOT','has_claim_by = root','multiply = 2.0'])
    dump('AI_EVIDENCE.json',dict(path=ai.relative_to(ROOT).as_posix(),sha256=sha(ai),block='ai_strategy_default/state_value/foreign-state branch',start_line=1390,end_line=1407,lines=[dict(line=i+1,text=lines[i]) for i in range(1389,1407)],factor=2.0,condition='Foreign target; either a split region with a non-treaty-port portion owned by ROOT, or a claim by ROOT. Outer reachability and other valuation conditions still apply.',not_a_war_probability=True,claim_does_not_stack_with_split=True,engine_test=False))
    print('Captured',len(runtime()),'runtime files;',check['progress']['percent'],'%; no gameplay writes')

def verify():
    before=load('BASELINE.json'); state=roadmap.load_json(CANON/'ROADMAP_STATE.json'); old=load('BEFORE_ROADMAP_STATE.json')
    checks=[]
    def add(name,ok):checks.append(dict(name=name,status='PASS' if ok else 'FAIL'))
    add('all_runtime_files_identical',runtime()==before['runtime'])
    add('previous_deliveries_and_approved_silesia_evidence_identical',protected()==before['protected'])
    add('git_head_branch_index_identical',git()==before['git'])
    add('all_81_task_records_identical',state['tasks']==old['tasks'] and len(state['tasks'])==81)
    add('all_previous_events_identical',state['events'][:-1]==old['events'])
    add('only_one_documentary_event_added',state['events'][-1]['id']=='SERG-RM-0064' and len(state['events'])==len(old['events'])+1)
    add('runtime_hold_and_external_deliveries_identical',all(state[k]==old[k] for k in ['runtime_validation_hold','external_prussian_deliveries']))
    add('scope_and_approval_unchanged',all(state[k]==old[k] for k in ['scope_version','closure_approval','source_manifest']))
    add('progress_identical',roadmap.progress(state)==before['canonical']['progress'])
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        new=(CANON/name).read_bytes(); prior=(OUT/('BEFORE_'+name)).read_bytes()
        add(name+'_previous_body_preserved',new.endswith(prior.split(b'\n',1)[1]))
    add('progress_history_additive',(CANON/'PROGRESS_HISTORY.md').read_bytes().startswith((OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()))
    canonical=roadmap.check();add('canonical_validator',canonical['status']=='PASS')
    dump('CANONICAL_CHECK.json',canonical)
    dump('FINAL_CHECKS.json',dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),functional_changes=0,new_human_receipts=0,engine_test=False))
    print(json.dumps(load('FINAL_CHECKS.json'),ensure_ascii=False,indent=2))
    assert all(c['status']=='PASS' for c in checks)

if __name__=='__main__':
    {'capture':capture,'verify':verify}[sys.argv[1]]()
