"""Add a negligible, explicit load-proof trace before launching HRE trials."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
plan=json.loads((REPORT/'PREPARATION.json').read_text())
assert not list((REPORT/'runtime').glob('HRE*')),'Do not mutate a launched diagnostic.'
path=Path(plan['lab'])/'diagnostic_no_hre_daily_guard/common/scripted_effects/1776_imperial_constitution.txt'
before=path.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(before)=='57459627d1ecf16c28a9dba218ef43e8bdf58f3a1e537d1337c6a99965cd8a9e'
old=b'aor1776_hre_schedule_membership_guard = {\n # ISSUE56 DIAGNOSTIC ONLY:'
new=b'aor1776_hre_schedule_membership_guard = {\n debug_log = "SIM56|DIAG|HRE_GUARD_BYPASSED|date=[TimeKeeper.GetCurrentDate.GetString]"\n # ISSUE56 DIAGNOSTIC ONLY:'
assert before.count(old)==1
after=before.replace(old,new,1)
with (REPORT/'diagnostic_before_trace.txt').open('xb') as out:out.write(before)
assert path.read_bytes()==before
path.write_bytes(after)
revision=dict(utc=datetime.now(timezone.utc).isoformat(),file=str(path),before_sha256=sha(before),after_sha256=sha(after),
 purpose='At first pending event and monthly attempts, prove that the no-rescheduling function actually executes. No world loops or scheduled events added; normal source unchanged.',
 expected_frequency='One existing first-day pending event, then monthly calls; incidental HRE callers may also invoke it.',
 note='Diagnostic still deliberately changes gameplay and is not an equivalent optimization. Trace overhead is included in its measured CPU/time.')
with (REPORT/'DIAGNOSTIC_TRACE_REVISION.json').open('x',encoding='utf-8') as out:json.dump(revision,out,indent=2,ensure_ascii=False)
print(json.dumps(revision,indent=2))
