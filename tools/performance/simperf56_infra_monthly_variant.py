"""One diagnostic variable: regional infrastructure MONTHLY child only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from validate_diplomacy_ottoman_1776 import parse
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
ROUND=REPORT/'RELOAD_EXPERIMENT_2026_11_17'
plan=json.loads((REPORT/'PREPARATION.json').read_text(encoding='utf-8'))
base=Path(plan['main_frozen']);diag=Path(plan['lab'])/'diagnostic_no_regional_monthly'
assert not diag.exists(),'Preserve existing diagnostic.'
manifest=json.loads((Path(plan['lab'])/'FROZEN_MANIFEST.json').read_text(encoding='utf-8'))['files']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(base/r)==v['sha256'] for r,v in manifest.items())
shutil.copytree(base,diag)
rel='common/on_actions/13_1776_ai_regional_infrastructure.txt';path=diag/rel;old=path.read_bytes();text=old.decode('utf-8-sig')
nodes=[n for n in parse(text) if n.key=='aor1776_ai_regional_infrastructure_monthly'];assert len(nodes)==1
node=nodes[0]
body='''aor1776_ai_regional_infrastructure_monthly = {
 # ISSUE56 diagnostic only. Native country pulse and initialization remain.
 effect = {
  if = { limit = { this = c:FRA }
   debug_log = "SIM56|DIAG|INFRA_MONTHLY_BYPASSED|date=[TimeKeeper.GetCurrentDate.GetString]"
  }
 }
}'''
new=text[:node.start]+body+text[node.end:];assert len(parse(new))==len(parse(text))
path.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+new.encode('utf-8'))
diff=[r for r,v in manifest.items() if sha(diag/r)!=v['sha256']];assert diff==[rel]
record=dict(utc=datetime.now(timezone.utc).isoformat(),changed_files=diff,source_sha256=hashlib.sha256(old).hexdigest(),diagnostic_sha256=sha(path),runtime=str(diag),
 scope='Only aor1776_ai_regional_infrastructure_monthly is bypassed. Initialization and all HRE/native/other monthly routines remain unchanged.',
 semantics='Gameplay-changing diagnostic, not an equivalent optimization. Single trace per French country pulse; overhead included.',
 causal_limit='Net effect may include downstream economic/AI state changes, not just script execution cost.')
with (ROUND/'INFRA_MONTHLY_VARIANT.json').open('x',encoding='utf-8') as out:json.dump(record,out,indent=2,ensure_ascii=False)
with (ROUND/'INFRA_MONTHLY_BEFORE.txt').open('xb') as out:out.write(old)
print(json.dumps(record,indent=2))
