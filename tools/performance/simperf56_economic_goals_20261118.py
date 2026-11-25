"""One native economic AI goal per diagnostic, with native PRE/POST proofs."""
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, subprocess
from simperf56_ai_cohorts import LAB, ROOT, PARENT, PREVIOUS, SOURCE, prior, sha, write, db_chunks
from simperf56_save_state import sections

REPORT=PARENT/'ECONOMIC_GOALS_2026_11_18'
VANILLA=Path('C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117/profiles/VANILLA1/save games/france_1836_01_01.v3')
CACHE=LAB/'ECONOMIC_SOURCE_GOALS_20261118.json'
SOURCE_HASH='387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2'
GOALS=('expand_production_buildings','change_production_methods','handle_money_spending','handle_ongoing_constructions')

def goal_state(text):
    out={}
    for rid,a,b,n in db_chunks(text,sections(text)['ai']):
        entries=n.children('ai_goal');counts=Counter(str(g.one('type')) for g in entries)
        payload={}
        for g in entries:
            typ=str(g.one('type'));payload.setdefault(typ,[]).append(hashlib.sha256(text[a+g.start:a+g.end].encode('utf-8')).hexdigest())
        out[str(n.one('country'))]=dict(controller_id=rid,enabled=n.one('enabled'),goals=dict(counts),payload=payload)
    return out

def snapshot():
    old=json.loads((LAB/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
    groups={k:{p:sha(p) for p in old['groups'][k]} for k in ('runtime','normal_profile','git_index','steam_executable','protected_diplomacy')}
    groups['prior_reports']={str(p):sha(p) for p in PARENT.rglob('*') if p.is_file() and REPORT not in p.parents}
    groups['prior_tools']={str(p):sha(p) for p in (ROOT/'tools/performance').iterdir() if p.is_file()}
    frozen=Path(json.loads((LAB/'SOURCE_PLAN.json').read_text(encoding='utf-8'))['main_frozen'])
    groups['frozen_runtime']={str(p):sha(p) for p in frozen.rglob('*') if p.is_file()}
    groups['reference_files']={str(p):sha(p) for p in (SOURCE,VANILLA,LAB/'S0_WITHOUT_EXPAND_GOAL.v3',PREVIOUS/'telemetry_profile/gui/frontend/frontend_ingame_menu.gui')}
    return dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),groups=groups)

def init():
    assert not REPORT.exists() and not CACHE.exists()
    assert sha(SOURCE)==SOURCE_HASH
    REPORT.mkdir()
    state=snapshot();write(LAB/'ECONOMIC_PRESERVATION_BEFORE_20261118.json',state)
    source=goal_state(SOURCE.read_text(encoding='utf-8-sig'))
    assert len(source)==646 and all(x['enabled']=='yes' for x in source.values())
    write(CACHE,dict(source_sha256=SOURCE_HASH,controllers=source))
    write(REPORT/'LAB_LOCATION.json',dict(lab=str(LAB),profiles=str(LAB/'profiles'),runs=str(LAB/'runs'),frozen_runtime=json.loads((LAB/'SOURCE_PLAN.json').read_text(encoding='utf-8'))['main_frozen'],bulky_files_outside_repository=True))
    print(json.dumps(dict(groups={k:len(v) for k,v in state['groups'].items()},controllers=len(source),vanilla_sha256=sha(VANILLA)),indent=2))

def prepare(label,goal):
    assert re.fullmatch('[A-Z][A-Z0-9_]{2,30}',label)
    cache=json.loads(CACHE.read_text(encoding='utf-8'));assert cache['source_sha256']==sha(SOURCE)==SOURCE_HASH
    source=SOURCE
    if goal=='expand_production_buildings':
        manifest=json.loads((LAB/'ONE_GOAL_VARIANT.json').read_text(encoding='utf-8'))
        source=Path(manifest['path']);assert sha(source)==manifest['variant_sha256'] and manifest['source_sha256']==SOURCE_HASH and manifest['removed_blocks']==400
    elif goal:
        raw=SOURCE.read_bytes();text=raw.decode('utf-8-sig');spans=sections(text);edits=[]
        for rid,a,b,n in db_chunks(text,spans['ai']):
            for g in n.children('ai_goal'):
                if g.one('type')==goal:edits.append((a+g.start,a+g.end))
        assert len(edits)==sum(x['goals'].get(goal,0) for x in cache['controllers'].values())==400
        changed=text
        for a,b in sorted(edits,reverse=True):changed=changed[:a]+changed[b:]
        ai_a,ai_b=spans['ai'];removed=sum(b-a for a,b in edits)
        assert changed[:ai_a]==text[:ai_a] and changed[ai_b-removed:]==text[ai_b:]
        source=LAB/('S0_WITHOUT_'+goal.upper()+'.v3')
        with source.open('xb') as f:f.write((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+changed.encode('utf-8'))
        write(LAB/(label+'_VARIANT.json'),dict(goal=goal,removed_blocks=len(edits),source_sha256=SOURCE_HASH,variant_sha256=sha(source),path=str(source),outside_ai_byte_identical=True,only_change='Remove the matching ai_goal blocks; every remaining source byte retained',gameplay_preserving=False))
    prior.LAB=LAB;prior.REPORT=REPORT;prior.profile(label,save=source)
    pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before);spec=plan['profiles'][label]
    spec['mods'][1]=(PREVIOUS/'telemetry_profile').as_posix();spec['diagnostic_goal_removed']=goal
    cp=Path(spec['path'])/'content_load.json';old=cp.read_bytes();content=json.loads(old)
    content['enabledMods'][1]['path']=spec['mods'][1]
    with (LAB/('ECON_PLAN_BEFORE_CONTROLS_'+label+'.json')).open('xb') as f:f.write(before)
    assert pp.read_bytes()==before and cp.read_bytes()==old
    cp.write_text(json.dumps(content,indent=2),encoding='utf-8')
    pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
    write(LAB/('ECON_PROFILE_'+label+'.json'),spec)

def verify(label,path,phase,goal):
    cache=json.loads(CACHE.read_text(encoding='utf-8'));original=cache['controllers']
    text=path.read_text(encoding='utf-8-sig');actual=goal_state(text)
    wrong={};payload_diff=[];remaining={}
    for country,v in actual.items():
        if country not in original:continue
        expected=original[country]['goals'].copy();expected.pop(goal,None)
        if v['goals']!=expected or v['enabled']!='yes':wrong[country]=dict(expected=expected,actual=v['goals'],enabled=v['enabled'])
        payload=original[country]['payload'].copy();payload.pop(goal,None)
        if v['payload']!=payload:payload_diff.append(country)
        if goal and v['goals'].get(goal):remaining[country]=v['goals'][goal]
    missing=sorted(set(original)-set(actual));new=sorted(set(actual)-set(original))
    out=dict(trial=label,phase=phase,goal_removed=goal,date=re.search(r'\bgame_date=([\d.]+)',text[:4096])[1],save=str(path),sha256=sha(path),controllers=len(actual),enabled_counts=dict(Counter(x['enabled'] for x in actual.values())),target_goal_remaining=remaining,other_goal_or_flag_differences=wrong,payload_changed_countries=payload_diff,missing_controllers=missing,new_controllers=new,expected_removed_objectives=sum(x['goals'].get(goal,0) for x in original.values()) if goal else 0)
    out['treatment_verified']=not wrong and not remaining and not new and (phase!='PRE' or not missing and not payload_diff)
    write(LAB/(label+'_'+phase+'_GOAL_PROOF.json'),out)
    print(json.dumps({k:v for k,v in out.items() if k!='other_goal_or_flag_differences'},indent=2))
    if not out['treatment_verified']:raise SystemExit('Native treatment validation failed; inspect before benchmarking or interpreting.')

def audit():
    before=json.loads((LAB/'ECONOMIC_PRESERVATION_BEFORE_20261118.json').read_text(encoding='utf-8'));now=snapshot();out=dict(utc=now['utc'],head=now['head'],groups={})
    for k,paths in before['groups'].items():
        changed=[p for p,h in paths.items() if not Path(p).is_file() or sha(p)!=h]
        out['groups'][k]=dict(checked=len(paths),unchanged=len(paths)-len(changed),changes=changed)
    write(LAB/'ECONOMIC_PRESERVATION_AFTER_20261118.json',out);write(REPORT/'PRESERVATION_AFTER.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=('init','prepare','verify','audit'));ap.add_argument('--label');ap.add_argument('--goal',choices=GOALS);ap.add_argument('--save',type=Path);ap.add_argument('--phase',choices=('PRE','POST'));args=ap.parse_args()
    if args.action=='init':init()
    elif args.action=='prepare':prepare(args.label,args.goal)
    elif args.action=='verify':verify(args.label,args.save,args.phase,args.goal)
    else:audit()
