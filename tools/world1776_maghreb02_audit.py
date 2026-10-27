"""Read-only territorial screening, Morocco through Egypt; no gameplay writes.

Uses the current WORLD MAGHREB-02 capture, without promoting map hints,
historical uncertainty or a successful conservation check to runtime evidence.
"""
import json
from collections import Counter

import numpy as np
from PIL import Image
import world1776_balkans03 as b
import world1776_balkans04 as b4

ROOT = b.ROOT
LOT = b.OUT / 'MAGHREB-02'
SCOPE = [
    'MARRAKECH', 'FEZ', 'AL_RIF', 'INNER_MOROCCO',
    'ORAN', 'ALGIERS', 'CONSTANTINE', 'TUNISIA',
    'TRIPOLI', 'LIBYA', 'LIBYAN_DESERT',
    'LOWER_EGYPT', 'MIDDLE_EGYPT', 'UPPER_EGYPT', 'MATRUH', 'SINAI', 'EGYPTIAN_DESERT',
    'SAHARA', 'EAST_SAHARA', 'WEST_SAHARA',
]


def dump(name, value):
    (LOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def main():
    base = json.loads((LOT / 'BASELINE.json').read_text('utf8'))
    current = b4.inventory()
    regions = {n.key: n for n in b.parse(b.a.raw(ROOT / 'map_data/state_regions/03_north_africa.txt'))}
    states = b.a.raw(ROOT / 'common/history/states/00_states.txt')
    image = np.asarray(Image.open(ROOT / 'map_data/provinces.png').convert('RGB'), dtype=np.uint32)
    packed = image[:, :, 0] * 65536 + image[:, :, 1] * 256 + image[:, :, 2]
    values, counts = np.unique(packed, return_counts=True)
    areas = {'x' + f'{int(c):06X}': int(n) for c, n in zip(values, counts)}
    rows = []
    for suffix in SCOPE:
        sid = 'STATE_' + suffix
        node = b.one(states, 's:' + sid)
        provinces = [x.strip('"') for x in b.a.ids(regions[sid], 'provinces')]
        parts = []
        for part in node.children('create_state'):
            ids = [x.strip('"') for x in b.a.ids(part, 'owned_provinces')]
            parts.append({'owner': part.one('country'), 'province_entries': len(ids),
                          'unique_provinces': len(set(ids)), 'provinces': ids,
                          'internal_repeats': [x for x, n in Counter(ids).items() if n > 1]})
        dup = {c: current['owners'][c] for c in provinces if len(current['owners'].get(c, [])) > 1}
        rows.append({'state': sid, 'registered_provinces': len(provinces), 'parts': parts,
                     'multiple_assignments': dup,
                     'registered_colors_absent_from_bitmap': [c for c in provinces if c not in areas]})
    dump('TERRITORIAL_INVENTORY.json', rows)
    dup = {}
    for row in rows:
        dup.update(row['multiple_assignments'])
    bounds = []
    for color, owners in dup.items():
        ys, xs = np.where(packed == int(color[1:], 16))
        bounds.append({'RGB': color, 'owners': owners, 'pixels': len(xs),
                       'bbox': [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                       'historical_owner': 'UNRESOLVED_NO_ARBITRARY_TRANSFER'})
    dump('DUPLICATE_ASSIGNMENTS.json', bounds)
    crosswalk = json.loads((LOT / 'NATIVE_PLACE_CROSSWALK.json').read_text('utf8'))
    fzn_owned = [c for c, parts in current['owners'].items() if any(tag == 'FZN' for _, tag in parts)]
    tripoli_dups = {c: parts for c, parts in dup.items() if parts[0][0] == 'STATE_TRIPOLI'}
    morocco_dups = {c: parts for c, parts in dup.items() if parts[0][0] == 'STATE_INNER_MOROCCO'}
    findings = [
        {'id': 'NORTH-AFRICA-T01', 'place': 'Fezzan / Murzuq', 'priority': 'P1',
         'status': 'TERRITORIAL_OMISSION_CONFIRMED_BOUNDARY_MASK_PENDING',
         'current_FZN_provinces': fzn_owned,
         'native_Murzuq_RGB': 'xCA4E6B', 'current_owner': current['owners'].get('xCA4E6B'),
         'action': 'Restore a bounded oasis nucleus for the Awlad Muhammad polity; avoid annexing all Sahara or all Zuwayya land. Existing FZN country needs starting-profile and population checks before activation.'},
        {'id': 'NORTH-AFRICA-T02', 'place': 'Siwa', 'priority': 'P1',
         'status': 'PREMATURE_DIRECT_EGYPTIAN_CONTROL_BOUNDARY_MASK_PENDING',
         'native_Siwa_RGB': 'xE0D021', 'current_owner': current['owners'].get('xE0D021'),
         'action': 'Separate the autonomous oasis from direct Egyptian ownership before its 1820 conquest; do not assign it to the Sudan or Zuwayya merely to avoid creating a country.'},
        {'id': 'NORTH-AFRICA-T03', 'place': 'Tripoli hinterland', 'priority': 'P0',
         'status': 'DUPLICATE_TERRITORIAL_ASSIGNMENTS_CONFIRMED_HISTORICAL_MASK_PENDING',
         'RGBs': sorted(tripoli_dups),
         'action': 'Resolve TRI versus ZWY ownership after geographic/historical matching; repeated ZWY entries are also present. Coastal province names alone do not prove ownership of inland polygons.'},
        {'id': 'NORTH-AFRICA-T04', 'place': 'Morocco / Tekna interface', 'priority': 'P0',
         'status': 'NINE_DUPLICATE_TERRITORIAL_ASSIGNMENTS_HISTORICAL_MASK_PENDING',
         'RGBs': sorted(morocco_dups),
         'action': 'Resolve MOR versus TEK ownership through the Draa / Wadi Nun interface; royal allegiance does not itself prove direct administration. No arbitrary straight border.'},
    ]
    dump('TERRITORIAL_QUEUE.json', findings)
    checks = []
    def ck(name, result, detail=None):
        checks.append({'check': name, 'passed': bool(result), 'detail': detail})
    ck('twenty_regional_definitions_examined', len(rows) == 20)
    ck('Fezzan_absence_reproduced', not fzn_owned)
    ck('Siwa_native_crosswalk_reproduced', any(r['place'] == 'Siwa' and r['declared_province'] == r['sampled_RGB'] == 'xE0D021' and r['owners_at_locator'] == [['STATE_MATRUH', 'EGY']] for r in crosswalk))
    ck('Murzuq_native_crosswalk_reproduced', any(r['place'] == 'Murzuq' and r['declared_province'] == r['sampled_RGB'] == 'xCA4E6B' and r['owners_at_locator'] == [['STATE_LIBYAN_DESERT', 'ZWY']] for r in crosswalk))
    ck('two_existing_Tripoli_conflicts_identified', set(tripoli_dups) == {'xAFD438', 'xD5C61D'}, tripoli_dups)
    ck('Tripoli_conflicts_have_TRI_and_ZWY', all({p[1] for p in parts} == {'TRI', 'ZWY'} for parts in tripoli_dups.values()))
    ck('nine_Morocco_Tekna_conflicts_identified', len(morocco_dups) == 9 and len(dup) == 11, morocco_dups)
    ck('Morocco_conflicts_have_MOR_and_TEK', all({p[1] for p in parts} == {'MOR', 'TEK'} for parts in morocco_dups.values()))
    ck('no_new_missing_RGB_claimed', all(not r['registered_colors_absent_from_bitmap'] for r in rows))
    ck('unchanged_ownership_inventory', current['owners'] == base['inventory']['owners'])
    ck('unchanged_world_population', current['world_population'] == base['inventory']['world_population'], current['world_population'])
    ck('unchanged_Git_identity_and_index', current['git'] == base['inventory']['git'])
    differences = [{'file': rel, 'before': old, 'current': b.a.sha(ROOT / rel) if (ROOT / rel).exists() else None}
                   for rel, old in base['protected'].items()
                   if not (ROOT / rel).exists() or b.a.sha(ROOT / rel) != old]
    reviewed_path = LOT / 'EXTERNAL_REVIEW.json'
    reviewed = json.loads(reviewed_path.read_text('utf8'))['reviewed_differences'] if reviewed_path.exists() else []
    unreviewed = [row for row in differences if row not in reviewed]
    ck('all_unattributed_changes_absent', not unreviewed, unreviewed)
    ck('reviewed_concurrent_changes_archived', all(b.a.sha(LOT / 'external_snapshots' / row['file']) == row['current'] for row in reviewed))
    ck('Gibraltar_endpoint_preserved', b.one(b.a.raw(ROOT / 'common/strait_definitions/strait_definitions.txt'), 'strait_gibraltar').one('second_land_endpoint') == 'xE8D231')
    for color, owner in [('xE8D231', 'SPA'), ('xE8D232', 'SPA'), ('xE8D233', 'SPA'), ('xE8D201', 'RAG')]:
        ck('previous_core_preserved.' + color, {p[1] for p in current['owners'].get(color, [])} == {owner})
    dump('POPULATION_LEDGER.json', {'before': base['inventory']['world_population'], 'after': current['world_population'], 'delta': current['world_population'] - base['inventory']['world_population'], 'POP_files_written': 0})
    dump('CONCURRENT_CHANGES.json', {'protected_files': len(base['protected']), 'differences': differences,
         'reviewed_external_changes': len(reviewed), 'unreviewed_differences': unreviewed,
         'gameplay_writes': 0, 'SERG_writes': 0, 'vanilla_writes': 0, 'Git_writes': 0})
    result = {'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
              'passed': sum(c['passed'] for c in checks), 'total': len(checks), 'checks': checks,
              'meaning': 'Audit reproduction and conservation only; known territorial findings remain open.',
              'runtime': 'NOT_RUN', 'human_validation': False}
    dump('VALIDATION.json', result)
    print(json.dumps({k: result[k] for k in ['status', 'passed', 'total']}))
    return result['status'] == 'PASS'


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
