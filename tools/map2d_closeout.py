"""Generate final review artifacts and independently verify the three MAP-2D CSVs."""
import collections as C
import csv
import difflib
import json
import re
from pathlib import Path

from map2d_work import ROOT, GAME, OUT, BASE, sha
from validate_map2d import ALLOWED


def closeout():
    baseline = json.loads(BASE.read_text(encoding='utf-8'))
    data = json.loads((OUT / 'TABLE_DATA.json').read_text(encoding='utf-8'))
    validation = data['validation']
    assert validation['status'] == 'PASS_STATIC'
    manifest = []
    whitespace = []
    diff = []
    for name in sorted(ALLOWED):
        current = ROOT / name
        old = baseline['originals'].get(name, '')
        new = current.read_text(encoding='utf-8-sig')
        before_hash = baseline['hashes'].get(name)
        for i, line in enumerate(new.splitlines(), 1):
            trailing = line.rstrip(' \t') != line
            mixed_indent = bool(re.match(r'^[ \t]* \t', line))
            if trailing or mixed_indent:
                whitespace.append({'path': name, 'line': i,
                                   'kind': 'trailing_whitespace' if trailing else 'space_before_tab',
                                   'identical_line_exists_in_baseline': line in old.splitlines()})
        record = {
            'path': name,
            'before_sha256': before_hash,
            'after_sha256': sha(current),
            'created_by_map2d': before_hash is None,
            'utf8_bom': current.read_bytes().startswith(b'\xef\xbb\xbf'),
        }
        if name == 'common/diplomatic_actions/28_invite_to_power_bloc.txt':
            native = GAME / name
            record['native_base_sha256'] = sha(native)
            record['native_base_version'] = 'Victoria 3 1.13.11 installed locally'
            native_text = native.read_text(encoding='utf-8-sig')
            (OUT / 'INVITATION_NATIVE_DELTA.patch').write_text(
                ''.join(difflib.unified_diff(native_text.splitlines(True), new.splitlines(True),
                                             fromfile='native/' + name, tofile='mod/' + name)),
                encoding='utf-8')
        manifest.append(record)
        diff.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                        fromfile='a/' + name if before_hash else '/dev/null',
                                        tofile='b/' + name))
    (OUT / 'MAP2D_FINAL.patch').write_text(''.join(diff), encoding='utf-8')
    (OUT / 'PATCH_MANIFEST.json').write_text(json.dumps({
        'purpose': 'Review against the preserved dirty-workspace baseline; not an instruction to reapply.',
        'patch_note': 'Text diff omits BOM markers; final file hashes and BOM fields are authoritative.',
        'files': manifest,
    }, ensure_ascii=False, indent=2), encoding='utf-8')

    def read_csv(name):
        with (OUT / name).open(encoding='utf-8', newline='') as stream:
            return list(csv.DictReader(stream))
    territorial = read_csv('MAP2D_TERRITORIAL_CHANGES.csv')
    population = read_csv('MAP2D_POPULATION_VALIDATION.csv')
    unresolved = read_csv('MAP2D_UNRESOLVED.csv')
    assert len(territorial) == 28
    assert len({r['Province_RGB'] for r in territorial}) == 28
    assert len(population) == len(data['population']) == 86
    assert len(unresolved) == 11
    numeric_fields = ['Land_Pixels', 'Min_X', 'Min_Y', 'Max_X', 'Max_Y']
    expected = {r[0]: r for r in data['territorial']}
    for row in territorial:
        original = expected[row['Province_RGB']]
        for field, index in zip(['State_Region', 'Before_Owner', 'After_Owner', 'Decision_Class'], range(1, 5)):
            assert row[field] == original[index]
        assert [int(row[k]) for k in numeric_fields] == original[5:10]
    sums = C.defaultdict(lambda: [0, 0, 0])
    for row, original in zip(population, data['population']):
        assert [row[k] for k in ['State_Region', 'Owner', 'Culture', 'Religion_Explicit_Or_Default']] == original[:4]
        nums = [int(row[k]) for k in ['Before_People', 'After_People', 'Delta_People']]
        assert nums == original[4:]
        assert nums[2] == nums[1] - nums[0]
        key = row['State_Region']
        for i, n in enumerate(nums):
            sums[key][i] += n
    assert all(a == b and d == 0 for a, b, d in sums.values())
    assert sums['WORLD'] == [835804980, 835804980, 0]
    result = {
        'status': 'PASS',
        'files_checked': 3,
        'territorial_rows': len(territorial),
        'population_rows': len(population),
        'unresolved_rows': len(unresolved),
        'csv_matches_validated_inventory': True,
        'each_delta_matches_after_minus_before': True,
        'every_region_delta_zero': True,
        'region_totals': dict(sums),
        'required_deliverables_exist': all((OUT / name).exists() for name in [
            'MAP2D_EXECUTIVE_SUMMARY.md', 'MAP2D_TERRITORIAL_CHANGES.csv',
            'MAP2D_POPULATION_VALIDATION.csv', 'MAP2D_UNRESOLVED.csv', 'MAP2D_VALIDATION.json']),
        'visual_review': 'Three previews inspected; Unresolved wrapping corrected and reinspected.',
        'native_engine_test': 'NOT_RUN',
        'whitespace_diagnostics': {
            'status': 'NON_BLOCKING',
            'line_count': len(whitespace),
            'new_whitespace_line_patterns': [r for r in whitespace if not r['identical_line_exists_in_baseline']],
            'note': 'Dirty checkout has existing Git whitespace warnings; no global formatting rewrite.',
        },
    }
    assert result['required_deliverables_exist']
    (OUT / 'QA' / 'CSV_VALIDATION.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    closeout()
