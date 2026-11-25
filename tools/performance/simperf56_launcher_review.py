"""Read preserved database copies; never write or restore the normal launcher."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sqlite3

ROOT = Path(__file__).resolve().parents[2]
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117')
REPORT = ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/STATE_INVESTIGATION_2026_11_17'
normal = Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/launcher-v2.sqlite')
current = LAB/'launcher_review/current.sqlite'
reference = Path('C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/B2/user_data/launcher-v2.sqlite')
ref_copy = LAB/'launcher_review/historical_B2.sqlite'
assert current.exists() and not ref_copy.exists()
raw = normal.read_bytes()
assert raw == current.read_bytes(), 'Concurrent launcher change; inspect again'
assert not Path(str(normal)+'-wal').exists()
ref_copy.write_bytes(reference.read_bytes())

def rows(path):
    # Plain Windows filenames work with the bundled SQLite runtime. Query only
    # external copies; URI read-only mode fails on this runtime.
    db = sqlite3.connect(str(path)); db.row_factory = sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    try:
        assert db.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        return {t: [dict(r) for r in db.execute('SELECT * FROM '+t)]
                for t in ('playsets','playsets_mods','playsets_dlcs')}
    finally: db.close()

cur, ref = rows(current), rows(ref_copy)
test_ids = {r['id'] for r in ref['playsets'] if r['name'].startswith('TECHPERF 54 ')}
comparison = []
for table in cur:
    refs = [r for r in ref[table] if r['id' if table=='playsets' else 'playsetId'] not in test_ids]
    def normalized(items, ignore_sync):
        return sorted(json.dumps({k:v for k,v in row.items() if not ignore_sync or k!='lastSyncAttemptAt'},
                                 sort_keys=True, ensure_ascii=True) for row in items)
    changed = []
    if table == 'playsets':
        by_id = {r['id']: r for r in refs}
        for r in cur[table]:
            if r['id'] in by_id:
                changed.extend(k for k,v in r.items() if by_id[r['id']].get(k)!=v)
    comparison.append(dict(table=table,current_rows=len(cur[table]),historical_normal_rows=len(refs),
        exact_equal_to_historical_rows=normalized(cur[table],False)==normalized(refs,False),
        equal_ignoring_sync_timestamp=normalized(cur[table],True)==normalized(refs,True),
        changed_playset_columns=sorted(set(changed))))
before = json.loads((LAB/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
result = dict(utc=datetime.now(timezone.utc).isoformat(), source_unchanged_during_read=normal.read_bytes()==raw,
    source_path=str(normal), last_write_utc=datetime.fromtimestamp(normal.stat().st_mtime,timezone.utc).isoformat(),
    source_sha256=hashlib.sha256(raw).hexdigest(),
    baseline_sha256=before['groups']['normal_profile'][str(normal)],
    historical_reference_path=str(reference), reference_sha256=hashlib.sha256(ref_copy.read_bytes()).hexdigest(),
    comparison=comparison, quick_check='ok', original_database_written=False, restored=False,
    limitation='Binary change since this mission baseline is real. Exact baseline database copy unavailable; comparison uses the preserved historical B2 database, excluding only its named TECHPERF 54 test playsets. Writer and full binary delta not attributable from hashes. No old database restored.')
for p in (LAB/'LAUNCHER_REVIEW.json', REPORT/'LAUNCHER_REVIEW.json'):
    with p.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps(result,indent=2))
