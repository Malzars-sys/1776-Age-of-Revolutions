"""Verify this pinned delivery, preserving historical results (new --output)."""
from pathlib import Path
import argparse
import sys
import json
import hashlib
import re

sys.dont_write_bytecode = True
LOT = Path(__file__).resolve().parent
ROOT = LOT.parents[3]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse


def run():
    load = lambda name: json.loads((LOT / name).read_text(encoding='utf-8'))
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    installation, entry = load('INSTALLATION.json'), load('ENTRY_REVIEW.json')
    view, consumers = load('AFTER_REVIEW_R2.json'), load('CONSUMERS.json')
    scoped, aux, bridge = load('MAPPING_SCOPED_R2.json'), load('AUXILIARY.json'), load('PARIS_BRIDGE.json')
    before, checks = load('BASELINE.json'), []

    def check(label, value):
        checks.append({'check': label, 'passed': bool(value)})

    check('all_494_entries_accounted', entry['counts'] == {
        'journals': 494, 'outcomes': 1045, 'mapped_entries_accounted': 400,
        'authored_no_outcome': 3, 'findings': 0})
    check('outcome_contract_pass', entry['status'] == 'PASS_STATIC_ONLY' and not entry['mapped_ids_absent_from_effective_catalogue'])
    check('transitive_dependencies_and_presentation_pass', view['status'] == 'PASS_STATIC_ONLY')
    check('all_literal_consumers_resolve', consumers['reference_count'] == 2920 and consumers['unresolved_count'] == 0)
    check('mapping_preservation_and_negative_controls', scoped['passed'] == scoped['total'] == 11117 and
          all(r['detected_by_expected_check'] for r in scoped['negative_controls']))
    check('auxiliary_identity_and_dependencies', aux['status'] == 'PASS_STATIC_ONLY' and aux['passed'] == aux['total'] == 65)
    check('paris_bridge_preserved', bridge['status'] == 'PASS_STATIC_ONLY' and bridge['passed'] == bridge['total'] == 13)
    check('new_presentation_regressions_detected', view['self_tests']['checks_passed'] == view['self_tests']['checks_total'] == 5)
    for spec in installation['files']:
        path = ROOT / spec['path']
        data = path.read_bytes()
        language = 'french' if '/french/' in spec['path'] else 'english'
        raw = data.decode('utf-8-sig')
        keys = re.findall(r'^ ([\w.]+):0 "(?:[^"\\]|\\.)*"$', raw, re.M)
        check(language + '_installed_exactly', sha(path) == spec['sha256'])
        check(language + '_BOM_header_and_valid_unique_keys', data.startswith(b'\xef\xbb\xbf') and
              raw.startswith('l_' + language + ':\n') and len(keys) == len(set(keys)) == (1 if language == 'french' else 4))
        collisions = []
        for source in (ROOT / 'localization' / language).rglob('*.yml'):
            if source == path:
                continue
            others = set(re.findall(r'^\s*([\w.\-]+):(?:\d+)?\s*"', source.read_text(encoding='utf-8-sig'), re.M))
            collisions.extend((key, str(source)) for key in set(keys) & others)
        check(language + '_no_mod_key_collision', not collisions)
    for spec in installation['native_localization_repairs']:
        check(spec['key'] + '_native_unchanged_and_bounded_repair',
              sha(Path(spec['native_source'])) == spec['native_sha256'] and
              spec['after'] == spec['before'].replace(spec['replaced'], spec['with'], 1))
    blocks = re.findall(r'```text\n(.*?)\n```', (LOT / 'TESTS_MOTEUR.md').read_text(encoding='utf-8'), re.S)
    check('all_prepared_effect_blocks_parse', len(blocks) == 7 and all(parse(block) for block in blocks))
    changes = [rel for rel, digest in before.items() if not (ROOT / rel).exists() or sha(ROOT / rel) != digest]
    check('all_2988_existing_runtime_data_and_index_inputs_preserved', len(before) == 2988 and not changes)
    native_drift = []
    for name, digest in view['source_hashes'].items():
        if name.startswith('native/') and sha(GAME / name[7:]) != digest:
            native_drift.append(name)
    for name, digest in view['localization_hashes'].items():
        path = Path(name)
        if path.is_relative_to(GAME) and sha(path) != digest:
            native_drift.append(name)
    check('all_consulted_native_inputs_preserved', not native_drift)
    manifest = {**before, **{s['path']: s['sha256'] for s in installation['files']}}
    fingerprint = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'status': 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'FAILED_STATIC_CHECK',
            'passed': sum(c['passed'] for c in checks), 'total': len(checks), 'checks': checks,
            'input_count': len(before), 'existing_inputs_changed': changes, 'native_inputs_changed': native_drift,
            'runtime_files_added': installation['files'], 'runtime_manifest_sha256': fingerprint,
            'runtime_manifest': manifest, 'runtime_tested': False, 'human_acceptance_acquired': False,
            'git_written': False, 'steam_build_updated': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(LOT):
        parser.error('Use a new result in this delivery directory.')
    result = run()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ['checks', 'runtime_manifest', 'runtime_files_added']}))
    print([c for c in result['checks'] if not c['passed']])
    raise SystemExit(result['status'] != 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
