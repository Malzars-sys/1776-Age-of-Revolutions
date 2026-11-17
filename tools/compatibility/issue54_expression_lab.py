"""Prepare bounded GUI-expression experiments, never UI automation or startup sampling."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111')
REPORT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE54_EXPRESSIONS_2026_11_12'
PREVIOUS = ROOT / 'docs/reports/compatibility/V1_15_ISSUE54_INTERACTIVE_2026_11_11'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert not REPORT.exists() or not any(p.is_file() for p in REPORT.rglob('*')), 'Retain existing experiment evidence.'
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'images').mkdir(exist_ok=True)
    (REPORT / 'variants').mkdir(exist_ok=True)
    plan = json.loads((PREVIOUS / 'AUTHORIZED_RETRY_2026_11_12/PLAN.json').read_text(encoding='utf-8-sig'))
    source = LAB / 'A_current'
    probe = LAB / 'expression_probe'
    assert not probe.exists() or not any(p.is_file() for p in probe.rglob('*'))
    # Independent copies keep all normal and frozen inputs untouched. This
    # intentionally avoids hardlinks after the host rejected their creation.
    count = 0
    for path in source.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        target = probe / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        count += 1
    original = (source / 'gui/tech_tree.gui').read_bytes()
    raw = original.decode('utf-8-sig')
    matches = list(re.finditer(r'(?m)^(\s*visible\s*=\s*)("[^"\r\n]{2000,}")', raw))
    assert len(matches) == 2
    edge = next(m for m in matches if 'TechTreeLine.GetTargetTech.Self' in m[2])
    card = next(m for m in matches if 'Technology.ShouldShow' in m[2])
    variants = {}
    for label, edge_value, card_value in [
        ('CONTROL', None, None),
        ('EDGE_OFF', 'yes', None),
        ('CARD_OFF', None, '"[Technology.ShouldShow(GetPlayer.Self)]"'),
        ('BOTH_OFF', 'yes', '"[Technology.ShouldShow(GetPlayer.Self)]"'),
    ]:
        changed = raw
        for match, value in sorted([(edge, edge_value), (card, card_value)], key=lambda x: x[0].start(), reverse=True):
            if value is not None:
                changed = changed[:match.start(2)] + value + changed[match.end(2):]
        payload = (b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'') + changed.encode('utf-8')
        path = REPORT / 'variants' / (label + '.gui')
        path.write_bytes(payload)
        variants[label] = dict(path=str(path), sha256=sha(path), diagnostic_only=label!='CONTROL',
                               edge_filter_removed=edge_value is not None, card_filter_removed=card_value is not None)
    plan.update(date='2026-11-12', started_utc=datetime.now(timezone.utc).isoformat(),
                report=str(REPORT), probe=str(probe), variants=variants,
                immutable_files=count-1, base_gui_sha256=sha(source/'gui/tech_tree.gui'),
                order=['EDGE_OFF','CARD_OFF','BOTH_OFF','OPTIMIZED_1','CONTROL_REPEAT','OPTIMIZED_2'],
                diagnostic_only=True, no_technology_definition_changes=True,
                user_authorized_pr=True, user_authorized_merge=False)
    (REPORT / 'PLAN.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')
    (REPORT / 'FPS_OBSERVATIONS.json').write_text('[]', encoding='utf-8')
    print(json.dumps(dict(report=str(REPORT), probe=str(probe), files=count, variants=list(variants)), indent=2))

if __name__ == '__main__':
    main()
