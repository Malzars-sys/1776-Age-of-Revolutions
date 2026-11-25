"""One serialized native AI goal ablation; reject if the engine recreates it.

Diagnostic only. No mod files, controller flags, countries or economic state
are edited. Native PRE and POST saves decide whether treatment is persistent.
"""
from collections import Counter
from pathlib import Path
import argparse, json, re
from simperf56_ai_cohorts import LAB, REPORT, PREVIOUS, SOURCE, prior, sha, write, db_chunks
from simperf56_save_state import sections

GOAL='expand_production_buildings'
LABEL='GOAL_EXPAND1'

def goals(text):
    return {str(n.one('country')):dict(enabled=n.one('enabled'),
        goals=Counter(str(g.one('type')) for g in n.children('ai_goal')))
        for rid,a,b,n in db_chunks(text,sections(text)['ai'])}

def prepare():
    assert sha(SOURCE)=='387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2'
    raw=SOURCE.read_bytes();text=raw.decode('utf-8-sig');spans=sections(text)
    original=goals(text);edits=[]
    for rid,a,b,n in db_chunks(text,spans['ai']):
        for g in n.children('ai_goal'):
            if g.one('type')==GOAL:edits.append((a+g.start,a+g.end))
    assert len(edits)==400
    changed=text
    for a,b in sorted(edits,reverse=True):changed=changed[:a]+changed[b:]
    modified=goals(changed);assert set(modified)==set(original)
    for country,v in original.items():
        want=v['goals'].copy();want.pop(GOAL,None)
        assert modified[country]==dict(enabled=v['enabled'],goals=want)
    ai_a,ai_b=spans['ai'];removed=sum(b-a for a,b in edits)
    assert changed[:ai_a]==text[:ai_a] and changed[ai_b-removed:]==text[ai_b:]
    variant=LAB/'S0_WITHOUT_EXPAND_GOAL.v3'
    with variant.open('xb') as f:f.write((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+changed.encode('utf-8'))
    write(LAB/'ONE_GOAL_VARIANT.json',dict(goal=GOAL,removed_blocks=len(edits),
        path=str(variant),source_sha256=sha(SOURCE),variant_sha256=sha(variant),
        outside_ai_byte_identical=True,all_other_goals_and_enabled_flags_equal=True,
        runtime_validated=False,gameplay_preserving=False))
    prior.LAB=LAB;prior.REPORT=REPORT;prior.profile(LABEL,save=variant)
    pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before)
    spec=plan['profiles'][LABEL];spec['mods'][1]=(PREVIOUS/'telemetry_profile').as_posix()
    spec['diagnostic_goal_removed']=GOAL
    cp=Path(spec['path'])/'content_load.json';old=cp.read_bytes();content=json.loads(old)
    content['enabledMods'][1]['path']=spec['mods'][1]
    write(LAB/'PLAN_BEFORE_GOAL_CONTROLS.json',json.loads(before))
    assert pp.read_bytes()==before and cp.read_bytes()==old
    cp.write_text(json.dumps(content,indent=2),encoding='utf-8')
    pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
    write(LAB/'PROFILE_CONTROLS_GOAL_EXPAND1.json',spec)

def verify(path,phase):
    original=goals(SOURCE.read_text(encoding='utf-8-sig'))
    text=path.read_text(encoding='utf-8-sig');actual=goals(text)
    target_present={c:v['goals'][GOAL] for c,v in actual.items() if v['goals'][GOAL]}
    other_diff={}
    for c in set(actual)&set(original):
        want=original[c]['goals'].copy();want.pop(GOAL,None)
        got=actual[c]['goals'].copy();got.pop(GOAL,None)
        if got!=want or actual[c]['enabled']!='yes':
            other_diff[c]=dict(expected=want,actual=got,enabled=actual[c]['enabled'])
    out=dict(trial=LABEL,phase=phase,save=str(path),sha256=sha(path),
        date=re.search(r'\bgame_date=([\d.]+)',text[:4096])[1],controllers=len(actual),
        enabled_counts=dict(Counter(v['enabled'] for v in actual.values())),
        target_goal_remaining=target_present,other_goal_or_flag_differences=other_diff,
        missing_controllers=sorted(set(original)-set(actual)),new_controllers=sorted(set(actual)-set(original)))
    out['treatment_verified']=not target_present and not other_diff and not out['new_controllers'] and (phase!='PRE' or not out['missing_controllers'])
    write(LAB/(LABEL+'_'+phase+'_GOAL_PROOF.json'),out)
    print(json.dumps(out,indent=2))
    if not out['treatment_verified']:raise SystemExit('Treatment not verified: do not interpret this as an ablation benchmark.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=('prepare','verify'))
    ap.add_argument('--save',type=Path);ap.add_argument('--phase',choices=('PRE','POST'));a=ap.parse_args()
    if a.action=='prepare':prepare()
    else:verify(a.save,a.phase)
