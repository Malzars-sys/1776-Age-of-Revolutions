"""Verify the bounded issue-23 duplicate-provider fix without writing live data.

--candidate reads the preserved economic snapshot. --controls writes deliberate
mutations only inside that snapshot and restores it, retaining control inputs.
All JSON outputs are confined to a new compatibility-evidence filename.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(Path(__file__).resolve().parent))
import issue23_economy_reference_audit as economy

TARGETS = {
    'common/production_method_groups/09_misc_resource.txt': (
        'pmg_base_building_logging_camp',
        'pmg_train_automation_building_rubber_plantation',
    ),
    'common/production_methods/12_subsistence.txt': tuple(
        'pm_home_workshops_building_subsistence_' + suffix
        for suffix in ('farm', 'orchard', 'pasture', 'fishing_village', 'rice_farm')
    ),
}
CUSTOM = (
    'common/production_method_groups/99_tech_tree_wood_rework_pmgs.txt',
    'common/production_method_groups/99_tech_tree_wave3_causality_pmgs.txt',
    'common/production_methods/99_tech_start_1776_subsistence_tools.txt',
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def native_remainder(raw, targets):
    text = raw.decode('utf-8-sig')
    nodes = economy.parse(text)
    removed = [node for node in nodes if node.key in targets]
    if {node.key for node in removed} != set(targets) or len(removed) != len(targets):
        raise ValueError('Native target set differs; repeat source review.')
    for node in sorted(removed, key=lambda x: x.start, reverse=True):
        text = text[:node.start] + text[node.end:]
    return (b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.encode('utf-8')


def verify(evidence, mod):
    baseline = json.loads((evidence / 'BASELINE.json').read_text(encoding='utf-8'))
    plan = json.loads((evidence / 'PLAN.json').read_text(encoding='utf-8'))
    before = json.loads((evidence / 'REFERENCES_BEFORE.json').read_text(encoding='utf-8'))
    checks = []

    def check(name, condition):
        checks.append({'check': name, 'pass': bool(condition)})

    for rel in CUSTOM:
        check(rel + ' authored bytes preserved',
              digest((mod / rel).read_bytes()) == baseline['source_hashes'][rel])
    for rel, targets in TARGETS.items():
        original = (evidence / 'native' / rel).read_bytes()
        active = (mod / rel).read_bytes()
        check(rel + ' current canonical source unchanged',
              digest((GAME / rel).read_bytes()) == digest(original))
        check(rel + ' only conflicting native objects removed', active == native_remainder(original, targets))
        old_nodes = economy.parse(original.decode('utf-8-sig'))
        new_nodes = economy.parse(active.decode('utf-8-sig'))
        check(rel + ' all unrelated object IDs/order preserved',
              [n.key for n in new_nodes] == [n.key for n in old_nodes if n.key not in targets])
        for target in targets:
            check(target + ' absent from native remainder', not any(n.key == target for n in new_nodes))
    result = economy.audit(mod=mod, game=GAME)
    check('all economic references resolve', not result['unresolved'])
    check('no ambiguous effective reference', not result['ambiguous_references'])
    check('no duplicated effective definition', not any(result['duplicate_definitions'][c] for c in result['duplicate_definitions']))
    check('no parser failure', not result['parse_errors'])
    check('initial PM selections remain supported', not result['unsupported_initial_methods'])
    check('same-building PM prerequisites remain supported', not result['incompatible_pm_prerequisites'])
    check('all unique category inventories preserved', result['counts'] == before['counts'])
    check('exactly the two intended new masks',
          set(result['same_path_masks']) - set(before['same_path_masks']) == set(TARGETS))
    check('no prior same-path mask removed', set(before['same_path_masks']) <= set(result['same_path_masks']))
    check('plan matches the seven reviewed IDs',
          {target for row in plan['files'] for target in row['removed_native_ids']} ==
          {target for values in TARGETS.values() for target in values})
    return {'status': 'PASS_STATIC_ONLY' if all(c['pass'] for c in checks) else 'FAIL_STATIC',
            'passed': sum(c['pass'] for c in checks), 'total': len(checks), 'checks': checks,
            'economic_references': result, 'engine_tested': False}


def controls(evidence):
    mod = (evidence / 'candidate_mod').resolve()
    if mod == ROOT or not mod.is_relative_to(evidence.resolve()):
        raise ValueError('Controls may only touch the evidence candidate snapshot.')
    rows = []
    cases = [('forestry_duplicate', 'common/production_method_groups/09_misc_resource.txt',
              [TARGETS['common/production_method_groups/09_misc_resource.txt'][0]]),
             ('rubber_duplicate', 'common/production_method_groups/09_misc_resource.txt',
              [TARGETS['common/production_method_groups/09_misc_resource.txt'][1]]),
             ('five_subsistence_duplicates', 'common/production_methods/12_subsistence.txt',
              list(TARGETS['common/production_methods/12_subsistence.txt']))]
    for name, rel, targets in cases:
        native = (evidence / 'native' / rel).read_bytes().decode('utf-8-sig')
        injected = '\n\n'.join(native[n.start:n.end] for n in economy.parse(native) if n.key in targets).encode('utf-8')
        archive = evidence / 'control_inputs' / (name + '.txt')
        archive.parent.mkdir(exist_ok=True)
        if archive.exists():
            raise ValueError('Preserve previous controls; choose a new evidence directory.')
        archive.write_bytes(injected)
        control_file = mod / Path(rel).parent / 'zz_issue23_deliberate_duplicate_control.txt'
        if control_file.exists():
            raise ValueError('A control file already exists.')
        control_file.write_bytes(injected)
        try:
            result = verify(evidence, mod)
            category = 'groups' if 'production_method_groups' in rel else 'methods'
            detected = all(target in result['economic_references']['duplicate_definitions'][category] for target in targets)
            rows.append({'case': name, 'expected_ids': targets, 'detected': detected,
                         'validator_status': result['status']})
        finally:
            # Only our exact, derived control file is removed; its bytes remain archived.
            if control_file.read_bytes() != injected:
                raise ValueError('Control input changed unexpectedly; preserve it for review.')
            control_file.unlink()
    rel = CUSTOM[2]
    target = mod / rel
    original = target.read_bytes()
    mutated = original.replace(b'goods_output_tools_add = 0.10', b'goods_output_tools_add = 0.90', 1)
    if mutated == original:
        raise ValueError('Tools-coefficient control failed to construct.')
    (evidence / 'control_inputs/tools_coefficient_drift.txt').write_bytes(mutated)
    target.write_bytes(mutated)
    try:
        result = verify(evidence, mod)
        found = next(c for c in result['checks'] if c['check'] == rel + ' authored bytes preserved')
        rows.append({'case': 'authored_tools_coefficient_drift', 'detected': not found['pass'],
                     'validator_status': result['status']})
    finally:
        if target.read_bytes() != mutated:
            raise ValueError('Mutated fixture changed unexpectedly; preserve for review.')
        target.write_bytes(original)
    restored = verify(evidence, mod)
    return {'status': 'PASS_NEGATIVE_CONTROLS' if all(r['detected'] and r['validator_status'] == 'FAIL_STATIC' for r in rows)
            and restored['status'] == 'PASS_STATIC_ONLY' else 'FAIL_CONTROLS',
            'cases': rows, 'candidate_restored': restored['status'] == 'PASS_STATIC_ONLY',
            'live_gameplay_written': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    evidence, output = args.evidence.resolve(), args.output.resolve()
    if not evidence.is_relative_to(ROOT / 'docs/reports/compatibility') or not output.is_relative_to(evidence):
        parser.error('All derived output must remain in this compatibility evidence directory.')
    if output.exists():
        parser.error('Use a new output filename; preserve earlier results.')
    result = controls(evidence) if args.controls else verify(evidence, evidence / 'candidate_mod' if args.candidate else ROOT)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'passed', 'total', 'cases', 'candidate_restored') if k in result}))


if __name__ == '__main__':
    main()
