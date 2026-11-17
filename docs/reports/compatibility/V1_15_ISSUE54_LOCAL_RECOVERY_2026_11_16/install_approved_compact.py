"""Apply only the two measured visibility expressions after explicit approval.

Keeps a byte-for-byte backup, preserves the existing BOM and line endings,
checks current contents immediately before writing, and never writes Git,
the vanilla installations, normal settings, playsets, or saves.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
OUT = HERE / 'INTEGRATION_2026_11_17'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda raw: hashlib.sha256(raw).hexdigest()
sha = lambda p: digest(p.read_bytes()) if p.is_file() else None

def write_json(name, value):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)

def snapshot(reference):
    return dict(
        repository={p: sha(ROOT / p) for p in reference['protectedFiles']},
        normal_profile={p: sha(Path(p)) for p in reference['protectedNormal']},
        git_status=subprocess.check_output(['git', '--no-optional-locks', 'status', '--short'], cwd=ROOT, text=True),
    )

def main():
    if OUT.exists():
        raise SystemExit('Keep previous integration evidence; inspect before retrying.')
    plan = read(HERE / 'PLAN_MANUAL.json')
    reference = read(HERE / 'POST_MANUAL_2026_11_17.json')
    gui = ROOT / 'gui/tech_tree.gui'
    candidate_path = Path(plan['trials']['COMPACT1']['mod']) / 'gui/tech_tree.gui'
    original, candidate = gui.read_bytes(), candidate_path.read_bytes()
    assert digest(original) == plan['trials']['CONTROL1']['gui_sha256'], 'Working GUI changed; review current edits.'
    assert digest(candidate) == plan['trials']['COMPACT1']['gui_sha256'], 'Measured candidate changed.'
    extract = lambda data: [m.group(1) for m in re.finditer(rb'visible\s*=\s*"\[([^"\r\n]+)\]"', data) if b'GetTechnology(' in m.group(1)]
    old, new = extract(original), extract(candidate)
    assert len(old) == len(new) == 2
    assert [s.count(b'GetTechnology(') for s in old] == [42, 43]
    assert [s.count(b'GetTechnology(') for s in new] == [8, 10]
    updated = original
    for before, after in zip(old, new):
        assert updated.count(before) == 1
        updated = updated.replace(before, after, 1)
    restored = updated
    for before, after in zip(old, new):
        assert restored.count(after) == 1
        restored = restored.replace(after, before, 1)
    assert restored == original, 'Unexpected change outside the two expressions.'
    assert updated.decode('utf-8-sig').replace('\r\n', '\n') == candidate.decode('utf-8-sig').replace('\r\n', '\n')
    before_snapshot = snapshot(reference)
    OUT.mkdir()
    with (OUT / 'tech_tree.before.gui').open('xb') as stream:
        stream.write(original)
    write_json('BEFORE.json', dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        approval=dict(quote="Je t'autorise.", source='User reply in this chat to the explicit main-mod application question',
                      scope='Only the two measured GUI visibility expressions; no Git write or native installation change'),
        source_sha256=digest(original), measured_candidate_sha256=digest(candidate), **before_snapshot))
    # Re-read immediately before the only write to product files.
    assert gui.read_bytes() == original, 'Concurrent GUI edit; do not overwrite it.'
    gui.write_bytes(updated)
    assert gui.read_bytes() == updated
    after_snapshot = snapshot(reference)
    changed = [p for p, value in before_snapshot['repository'].items() if after_snapshot['repository'][p] != value]
    changed_normal = [p for p, value in before_snapshot['normal_profile'].items() if after_snapshot['normal_profile'][p] != value]
    expected_changes = ['gui/tech_tree.gui']
    receipt = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION', performance_fix_installed=True,
        source_sha256=digest(original), installed_sha256=sha(gui), measured_candidate_sha256=digest(candidate),
        installed_byte_identical_to_measured_candidate=updated == candidate,
        only_two_expression_spans_changed=True, original_encoding_and_line_endings_preserved=True,
        changed_repository_files=changed, changed_normal_profile_files=changed_normal,
        expected_product_scope_passed=changed == expected_changes and not changed_normal,
        git_index_unchanged=after_snapshot['repository']['.git/index'] == before_snapshot['repository']['.git/index'],
        backup=str(OUT / 'tech_tree.before.gui'),
        candidate_runtime_evidence='MANUAL_RESULTS_2026_11_17/ANALYSIS.json',
        installed_main_mod_runtime_retested=False,
        local_1_15_0_with_gameplay_DLC_tested=False,
        git_write_or_merge_performed=False, normal_profile_restored=False,
        after_snapshot=after_snapshot)
    write_json('APPLICATION_RECEIPT.json', receipt)
    assert receipt['expected_product_scope_passed'], 'Unexpected concurrent drift retained in receipt; inspect without restoring.'
    print(json.dumps({k: v for k, v in receipt.items() if k != 'after_snapshot'}, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
