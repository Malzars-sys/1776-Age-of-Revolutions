"""Add a unique trial using the already prepared common GUI instrumentation."""
import json,sys
from pathlib import Path
from simperf56_state_lab import LAB,profile,write,sha
label=sys.argv[1]
overlay=LAB/'telemetry_profile'
controls=json.loads((LAB/'PROFILE_CONTROLS.json').read_text(encoding='utf-8'))
assert sha(overlay/controls['new_file'])==controls['override_sha256']
profile(label)
pp=LAB/'PREPARATION.json';raw=pp.read_bytes();plan=json.loads(raw);spec=plan['profiles'][label]
spec['mods'][1]=overlay.as_posix()
cp=Path(spec['path'])/'content_load.json';oldc=cp.read_bytes();c=json.loads(oldc)
c['enabledMods'][1]['path']=overlay.as_posix()
assert pp.read_bytes()==raw and cp.read_bytes()==oldc
(LAB/('PLAN_BEFORE_CONTROLS_'+label+'.json')).write_bytes(raw)
(LAB/('CONTENT_BEFORE_CONTROLS_'+label+'.json')).write_bytes(oldc)
cp.write_text(json.dumps(c,indent=2),encoding='utf-8')
pp.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
write(LAB/('PROFILE_CONTROLS_'+label+'.json'),spec)
print(json.dumps(spec,indent=2))
