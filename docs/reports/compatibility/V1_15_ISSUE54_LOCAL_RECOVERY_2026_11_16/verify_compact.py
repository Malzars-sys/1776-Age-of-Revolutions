"""Retain the existing truth-table checker; select compact predicates by content.

The legacy extractor only accepts expressions longer than 2000 characters.
COMPACT's expressions are shorter. No equivalence check is removed or weakened.
"""
from pathlib import Path
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
root = Path.cwd()
spec = importlib.util.spec_from_file_location('fastpath', root / 'tools/compatibility/issue54_verify_fastpath.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def predicates(text):
    values = [s for s in re.findall(r'visible\s*=\s*"\[([^"\r\n]+)\]"', text) if 'GetTechnology(' in s]
    assert len(values) == 2
    return values

module.predicates = predicates
lab = Path('C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111')
result = module.verify(lab / 'A_current/gui/tech_tree.gui', root / 'docs/reports/compatibility/V1_15_ISSUE54_EXPRESSIONS_2026_11_12/variants/COMPACT.gui', lab / 'evidence/MOD_GRAPH.json')
result['extractor_change'] = 'Select the two expressions containing GetTechnology rather than imposing a 2000-character minimum.'
output = Path(__file__).with_name('COMPACT_STATIC_RECHECK.json')
with output.open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
print(json.dumps(result, indent=2))
