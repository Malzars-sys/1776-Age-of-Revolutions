"""Issue 56: isolated AI cohort lab, exact save edits, immutable source evidence."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import argparse, hashlib, json, re, shutil, subprocess, sys
import simperf56_state_lab as prior
from simperf56_save_state import sections, records, block_end, parse

ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
REPORT = PARENT/'AI_COHORTS_2026_11_17'
PREVIOUS = Path('C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117')
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor56_ai_20261117')
SOURCE = Path('C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117/profiles/MAIN3/save games/royaume de france_1776_01_01.v3')

def sha(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def write(p, data):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f: json.dump(data,f,indent=2,ensure_ascii=False)

def db_chunks(text, span):
    a,b=span; m=re.search(r'\bdatabase=\{', text[a:b]); assert m
    start=a+m.end()-1; end=block_end(text,start); pos=start+1
    while True:
        hit=re.search(r'(\d+)=\{', text[pos:end])
        if not hit: break
        left=pos+hit.start(); right=block_end(text,pos+hit.end()-1)
        yield hit[1],left,right,parse(text[left:right])[0]
        pos=right

def init():
    assert not LAB.exists() and not REPORT.exists()
    LAB.mkdir(); REPORT.mkdir(); (LAB/'requests').mkdir()
    base=json.loads((PREVIOUS/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
    groups={k:{p:sha(p) for p in base['groups'][k]} for k in (
        'runtime','normal_profile','git_index','steam_executable','protected_diplomacy')}
    groups['previous_reports']={str(p):sha(p) for p in PARENT.rglob('*') if p.is_file() and REPORT not in p.parents}
    groups['previous_tools']={str(p):sha(p) for p in (ROOT/'tools/performance').iterdir() if p.is_file()}
    write(LAB/'PRESERVATION_BEFORE.json',dict(utc=datetime.now(timezone.utc).isoformat(),
        head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),groups=groups))
    normal=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/launcher-v2.sqlite')
    raw=normal.read_bytes(); (LAB/'launcher_current_before.sqlite').write_bytes(raw)
    assert normal.read_bytes()==raw and not Path(str(normal)+'-wal').exists()
    write(LAB/'LAUNCHER_BASELINE.json',dict(path=str(normal),sha256=sha(normal),bytes=len(raw),
        current_state_preserved=True,historical_restore=False))
    plan=json.loads((PREVIOUS/'SOURCE_PLAN.json').read_text(encoding='utf-8'))
    write(LAB/'SOURCE_PLAN.json',plan)
    plan['lab']=str(LAB); plan['profiles']={}; write(LAB/'PREPARATION.json',plan)
    shutil.copyfile(PREVIOUS/'run_profile_trial.ps1',LAB/'run_profile_trial.ps1')
    write(REPORT/'LAB_LOCATION.json',dict(lab=str(LAB),frozen_runtime=plan['main_frozen'],
        instrumentation=str(PREVIOUS/'telemetry_profile'),bulky_evidence_outside_repository=True))
    print(json.dumps({'lab':str(LAB),'preservation_groups':{k:len(v) for k,v in groups.items()},'launcher_sha256':sha(normal)}))

def inventory():
    assert sha(SOURCE)=='387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2'
    raw=SOURCE.read_bytes(); text=raw.decode('utf-8-sig'); ss=sections(text)
    populated=json.loads((PREVIOUS/'STATE_INITIAL.json').read_text(encoding='utf-8'))['country']['by_id']
    countries={i:n for i,n in records(text,ss['country_manager'])}
    found=[]; edits={'DEC':[], 'OTHER':[]}
    for rid,left,right,n in db_chunks(text,ss['ai']):
        country=str(n.one('country')); assert country in countries
        c=countries[country]; flags=n.children('enabled'); assert len(flags)==1 and flags[0].value=='yes'
        kind=str(c.one('country_type','')).strip('"'); assert kind
        entry=dict(controller_id=rid,country_id=country,tag=str(c.one('definition','')).strip('"'),
            country_type=kind,populated=country in populated,dead=c.one('dead','no'),
            enabled=n.one('enabled'),country_goal_entries=len(n.children('country_goal')[0].children()) if n.children('country_goal') else 0)
        found.append(entry)
        flag=flags[0]; before=text[left+flag.start:left+flag.end]; assert before=='enabled=yes'
        # Complement includes EVERY controller outside the exact DEC cohort.
        group='DEC' if kind=='decentralized' else 'OTHER'
        edits[group].append((left+flag.start,left+flag.end,'enabled=no'))
    assert len(found)==646 and len({x['country_id'] for x in found})==646
    bytype=Counter((x['country_type'],x['populated']) for x in found)
    for group,changes in edits.items():
        changed=text
        for a,b,value in sorted(changes,reverse=True): changed=changed[:a]+value+changed[b:]
        # Restoring only these exact fields must reconstruct the source bytes.
        ai_start,ai_end=ss['ai']; new_ai_end=ai_end-len(changes)
        assert changed[:ai_start]==text[:ai_start] and changed[new_ai_end:]==text[ai_end:]
        out=LAB/('S0_'+group+'_AI_OFF.v3')
        out.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+changed.encode('utf-8'))
        assert out.stat().st_size==len(raw)-len(changes)
        write(LAB/('VARIANT_'+group+'.json'),dict(path=str(out),sha256=sha(out),source_sha256=sha(SOURCE),
            changed_fields=len(changes),only_change='Selected AI.enabled yes -> no inside ai database',
            outside_ai_section_byte_identical=True,intended_disabled_country_ids=sorted(x['country_id'] for x in found if (x['country_type']=='decentralized')==(group=='DEC')),
            runtime_loaded=False))
    data=dict(source=str(SOURCE),source_sha256=sha(SOURCE),controllers=found,
        counts=[dict(country_type=k[0],populated=k[1],controllers=v) for k,v in sorted(bytype.items())],
        total_controllers=len(found),nonpopulated=[x for x in found if not x['populated']],
        cohorts={k:len(v) for k,v in edits.items()},classification_covers_every_controller=True)
    write(LAB/'CONTROLLER_INVENTORY.json',data); write(REPORT/'CONTROLLER_INVENTORY.json',data)
    print(json.dumps({k:v for k,v in data.items() if k!='controllers'},indent=2))

def profile(label,cohort):
    source=SOURCE if cohort in ('ON','OFF') else LAB/('S0_'+cohort+'_AI_OFF.v3')
    prior.LAB=LAB; prior.REPORT=REPORT
    prior.profile(label,save=source)
    pp=LAB/'PREPARATION.json'; raw=pp.read_bytes(); plan=json.loads(raw); spec=plan['profiles'][label]
    overlay=PREVIOUS/'telemetry_profile'; controls=json.loads((PREVIOUS/'PROFILE_CONTROLS.json').read_text(encoding='utf-8'))
    assert sha(overlay/controls['new_file'])==controls['override_sha256']
    spec['mods'][1]=overlay.as_posix(); spec['diagnostic_cohort']=cohort
    cp=Path(spec['path'])/'content_load.json'; old=cp.read_bytes(); obj=json.loads(old); obj['enabledMods'][1]['path']=overlay.as_posix()
    (LAB/('PLAN_BEFORE_CONTROLS_'+label+'.json')).write_bytes(raw)
    assert pp.read_bytes()==raw and cp.read_bytes()==old
    cp.write_text(json.dumps(obj,indent=2),encoding='utf-8')
    pp.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
    write(LAB/('PROFILE_CONTROLS_'+label+'.json'),spec)

def verify(label,save,phase):
    plan=json.loads((LAB/'PREPARATION.json').read_text(encoding='utf-8')); cohort=plan['profiles'][label]['diagnostic_cohort']
    inv=json.loads((LAB/'CONTROLLER_INVENTORY.json').read_text(encoding='utf-8'))
    initial={r['country_id']:r for r in inv['controllers']}
    raw=save.read_bytes(); text=raw.decode('utf-8-sig'); ss=sections(text)
    actual={str(n.one('country')):dict(controller_id=rid,enabled=n.one('enabled')) for rid,a,b,n in db_chunks(text,ss['ai']) if n.one('country') is not None}
    assert set(actual)<=set(initial), 'New controllers require explicit review'
    expected_off={i for i,r in initial.items() if cohort=='OFF' or cohort=='DEC' and r['country_type']=='decentralized' or cohort=='OTHER' and r['country_type']!='decentralized'}
    differences={i:dict(actual=r['enabled'],expected='no' if i in expected_off else 'yes') for i,r in actual.items() if r['enabled']!=('no' if i in expected_off else 'yes')}
    missing=sorted(set(initial)-set(actual))
    if phase=='PRE': assert not missing
    assert not differences,differences
    out=dict(trial=label,phase=phase,save=str(save),date=re.search(r'\bgame_date=([\d.]+)',text[:4096])[1],sha256=sha(save),
        controllers=len(actual),enabled_counts=dict(Counter(r['enabled'] for r in actual.values())),
        intended_initial_disabled=len(expected_off),missing_initial_controllers=[initial[i] for i in missing],
        unexpected_flags=differences,all_present_controllers_match_expected=True,actual=actual)
    write(LAB/(label+'_'+phase+'_AI_PROOF.json'),out)
    print(json.dumps({k:v for k,v in out.items() if k!='actual'},indent=2))

def audit():
    before=json.loads((LAB/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
    result=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),groups={})
    for k,paths in before['groups'].items():
        changed=[p for p,h in paths.items() if not Path(p).exists() or sha(p)!=h]
        result['groups'][k]=dict(checked=len(paths),unchanged=len(paths)-len(changed),changes=changed)
    write(LAB/'PRESERVATION_AFTER.json',result); write(REPORT/'PRESERVATION_AFTER.json',result); print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('action',choices=('init','inventory','profile','verify','audit')); ap.add_argument('--label');ap.add_argument('--cohort',choices=('ON','OFF','DEC','OTHER'));ap.add_argument('--save',type=Path);ap.add_argument('--phase',choices=('PRE','POST'));a=ap.parse_args()
    if a.action=='init':init()
    elif a.action=='inventory':inventory()
    elif a.action=='profile':profile(a.label,a.cohort)
    elif a.action=='verify':verify(a.label,a.save,a.phase)
    else:audit()
