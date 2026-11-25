"""Preserve a newly observed launcher state after interruption; never restore."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
from simperf56_ai_cohorts import LAB,write

p=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/launcher-v2.sqlite')
assert not Path(str(p)+'-wal').exists(), 'Use SQLite live backup if a WAL exists'
raw=p.read_bytes();out=LAB/'launcher_resume_20261118.sqlite'
with out.open('xb') as f:f.write(raw)
assert p.read_bytes()==raw
def inspect(path):
    with sqlite3.connect(path.as_uri()+'?mode=ro&immutable=1',uri=True) as c:
        tables=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        return {t:dict(columns=[r[1] for r in c.execute('PRAGMA table_info("'+t.replace('"','""')+'")')],
            rows=c.execute('SELECT * FROM "'+t.replace('"','""')+'"').fetchall()) for t in tables}
old=inspect(LAB/'launcher_current_before.sqlite');new=inspect(out)
changes={}
for t in sorted(set(old)|set(new)):
    a,b=old.get(t),new.get(t)
    if a==b:continue
    # Full private rows remain only in local preserved databases.
    ac=a['rows'] if a else [];bc=b['rows'] if b else []
    changes[t]=dict(before_rows=len(ac),after_rows=len(bc),
        removed_rows=sum(r not in bc for r in ac),added_rows=sum(r not in ac for r in bc),
        columns=b['columns'] if b else a['columns'])
result=dict(observed_utc=datetime.now(timezone.utc).isoformat(),
    before_sha256=hashlib.sha256((LAB/'launcher_current_before.sqlite').read_bytes()).hexdigest(),
    current_sha256=hashlib.sha256(raw).hexdigest(),preserved_copy=str(out),
    changed_tables=changes,restored=False,
    attribution='Observed after an approximately 11.5-hour interruption; writer and cause not established. No historical restoration.')
write(LAB/'LAUNCHER_RESUME_20261118.json',result);print(json.dumps(result,indent=2))
