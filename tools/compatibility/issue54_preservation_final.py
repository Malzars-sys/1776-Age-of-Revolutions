"""Read-only local preservation receipt, never publish its environment paths."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE54_EXPRESSIONS_2026_11_12'
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111')
baseline = json.loads((ROOT / 'docs/reports/compatibility/V1_15_ISSUE54_INTERACTIVE_2026_11_11/NORMAL_INPUTS_BEFORE.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
mod_inputs = {k:v for k,v in baseline.items() if Path(k).is_relative_to(ROOT)}
drift = [k for k,v in mod_inputs.items() if not Path(k).is_file() or sha(Path(k)) != v]
normal_db = ROOT.parent.parent / 'launcher-v2.sqlite'
reference_db = LAB / 'runtime_ui_controlled/B2/user_data/launcher-v2.sqlite'
def connect(path):
    return sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
with connect(normal_db) as current, connect(reference_db) as reference:
    current.row_factory = reference.row_factory = sqlite3.Row
    tables = {}
    for table in ('playsets','playsets_mods','playsets_dlcs'):
        tables[table] = ([dict(r) for r in current.execute('SELECT * FROM ' + table)],
                         [dict(r) for r in reference.execute('SELECT * FROM ' + table)])
    # Explicit dedicated test rows carry these exact prepared names.
    test_rows = [r for r in tables['playsets'][1] if r['name'] in ('ISSUE54 A current GUI','ISSUE54 B vanilla GUI')]
    # Print only local reference metadata if naming differs; do not claim parity.
    identities = [dict(id=r['id'], name=r['name']) for r in tables['playsets'][1]]
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), captured_original_mod_inputs=len(mod_inputs),
               changed_original_mod_inputs=drift, original_gui_sha256=sha(ROOT/'gui/tech_tree.gui'),
               source_index_unchanged=not any(k.endswith('/.git/index') or k.endswith('\\.git\\index') for k in drift),
               normal_playset_counts={t:len(v[0]) for t,v in tables.items()},
               reference_playset_identities_local_only=identities,
               expected_test_rows_found=len(test_rows))
destination=REPORT/'PRESERVATION_FINAL_LOCAL.json'
assert not destination.exists()
destination.write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
