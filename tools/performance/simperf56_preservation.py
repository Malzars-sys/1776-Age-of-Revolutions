"""Compare current bytes with the mission's pre-benchmark preservation record."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
before=json.loads((REPORT/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8-sig'))
plan=json.loads((REPORT/'PREPARATION.json').read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def check(mapping):
    same=[];different=[];missing=[];unreadable=[]
    for raw,expected in mapping.items():
        path=Path(raw)
        if not path.is_file():missing.append(raw);continue
        try:actual=sha(path)
        except OSError as exc:unreadable.append(dict(path=raw,error=str(exc)));continue
        if actual==expected:same.append(raw)
        else:different.append(dict(path=raw,before_sha256=expected,after_sha256=actual))
    return dict(checked=len(mapping),unchanged_count=len(same),changed=different,missing=missing,unreadable=unreadable)
runtime={str(ROOT/rel):spec['sha256'] for rel,spec in before['runtime'].items()}
normal=check(before['normal_profile'])
frozen=check({str(Path(plan['main_frozen'])/rel):spec['sha256'] for rel,spec in before['runtime'].items()})
diag=check({str(Path(plan['lab'])/'diagnostic_no_hre_daily_guard'/rel):spec['sha256'] for rel,spec in before['runtime'].items()})
head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
result=dict(utc=datetime.now(timezone.utc).isoformat(),reference_head=before['head'],current_head=head,head_unchanged=head==before['head'],
 runtime=check(runtime),normal_profile=normal,protected_diplomacy=check(before['protected_diplomacy']),
 index_unchanged=sha(ROOT/'.git/index')==before['index_sha256'],compact_gui_sha256=sha(ROOT/'gui/tech_tree.gui'),
 executable_unchanged=sha(Path(before['executable']))==before['executable_sha256'],frozen_runtime=frozen,diagnostic_vs_reference=diag,
 no_automatic_restoration=True,
 note='Any changed normal file must be examined, not restored wholesale. This check proves bytes only for the recorded files, not every file in either installed game.')
target=REPORT/'PRESERVATION_AFTER.json'
with target.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,ensure_ascii=False)
print(json.dumps(result,indent=2,ensure_ascii=False))
