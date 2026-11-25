"""New-round snapshots, preserving the previous mission's records."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
ROUND=REPORT/'RELOAD_EXPERIMENT_2026_11_17'
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for b in iter(lambda:stream.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('before','after'));args=parser.parse_args()
old=json.loads((REPORT/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
beforepath=ROUND/'PRESERVATION_BEFORE.json'
if args.phase=='before':
    groups={'runtime':{str(ROOT/k) for k in old['runtime']},'normal_profile':set(old['normal_profile']),
        'git_index':{str(ROOT/'.git/index')},'steam_executable':{old['executable']},'protected_diplomacy':set(old['protected_diplomacy'])}
    groups['normal_profile'].update(str(p) for p in (ROOT.parent.parent/'save games').rglob('*') if p.is_file())
    # Protect earlier uncommitted reports/tools as evidence. The plan is the only
    # intentionally appended old report; its exact preceding bytes are archived.
    groups['earlier_evidence']={str(p) for p in REPORT.rglob('*') if p.is_file() and ROUND not in p.parents and 'MATURE1_' not in str(p) and p.name!='PREPARATION.json'}
    record=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),groups={g:{p:sha(Path(p)) for p in paths} for g,paths in groups.items()})
    with beforepath.open('x',encoding='utf-8') as out:json.dump(record,out,indent=2,ensure_ascii=False)
    print(json.dumps({g:len(v) for g,v in record['groups'].items()}))
else:
    original=json.loads(beforepath.read_text(encoding='utf-8'));groups={}
    for g,paths in original['groups'].items():
        changes=[];same=0
        for raw,expected in paths.items():
            p=Path(raw);actual=sha(p) if p.is_file() else None
            if actual==expected:same+=1
            else:changes.append(dict(path=raw,before=expected,after=actual))
        groups[g]=dict(checked=len(paths),unchanged=same,changes=changes)
    record=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),groups=groups)
    with (ROUND/'PRESERVATION_AFTER.json').open('x',encoding='utf-8') as out:json.dump(record,out,indent=2,ensure_ascii=False)
    print(json.dumps(record,indent=2,ensure_ascii=False))
