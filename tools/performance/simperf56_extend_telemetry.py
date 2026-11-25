"""Complete the not-yet-launched common telemetry, retaining exact old bytes."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
plan=json.loads((REPORT/'PREPARATION.json').read_text(encoding='utf-8'))
folder=Path(plan['telemetry'])
assert not (REPORT/'runtime').exists(),'Do not change instrumentation after launching a series.'
hook=folder/'common/on_actions/zz_aor56_telemetry.txt'
events=folder/'events/aor56_telemetry.txt'
a,b=hook.read_bytes(),events.read_bytes()
old=' c:FRA ?= {\n'
text=a.decode('utf-8-sig')
assert text.count(old)==1 and 'COUNTRY_DONE' not in text
updated=text.replace(old,' debug_log = "SIM56|COUNTRY_DONE"\n c:FRA ?= { trigger_event = { id = aor56.100 days = 1 }\n',1)
extra='aor56.100 = { type = country_event hidden = yes immediate = { debug_log = "SIM56|DAY|date=[TimeKeeper.GetCurrentDate.GetString]" trigger_event = { id = aor56.100 days = 1 } } }\n'
assert b'aor56.100' not in b
archive=REPORT/'telemetry_pre_launch_archive';archive.mkdir()
(archive/hook.name).write_bytes(a);(archive/events.name).write_bytes(b)
assert hook.read_bytes()==a and events.read_bytes()==b
hook.write_bytes(b'\xef\xbb\xbf'+updated.encode('utf-8'))
events.write_bytes(b+extra.encode('utf-8'))
result={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (hook,events)}
with (REPORT/'TELEMETRY_HASHES.json').open('x',encoding='utf-8') as out:json.dump(result,out,indent=2)
print(json.dumps(result,indent=2))
