"""Install the four bounded North African territorial resolutions.

Siwa stays Egyptian per explicit user correction; its existing passable route
is verified. Nine native Fezzan provinces connect the oasis core to Tripoli.
No bitmap, technology graph, production recipe, building or Git writes.
"""
import argparse
import json
import shutil
from collections import Counter, defaultdict, deque

import numpy as np
from PIL import Image, ImageDraw
import world1776_balkans03 as b
import world1776_balkans04 as b4

ROOT = b.ROOT
LOT = b.OUT / 'MAGHREB-03'
ST = 'common/history/states/00_states.txt'
POP = 'common/history/pops/03_north_africa.txt'
DIP = 'common/history/diplomacy/1776_world_m03_fezzan.txt'
CHAR = 'common/history/characters/fzn - fezzan.txt'
COUNTRY = 'common/history/countries/fzn - fezzan.txt'
LAW = 'common/laws/1776_world_m03_fezzan.txt'
EFFECT = 'common/scripted_effects/1776_world_m03_fezzan.txt'
FR = 'localization/french/1776_world_m03_fezzan_l_french.yml'
EN = 'localization/english/1776_world_m03_fezzan_l_english.yml'
EDIT = [ST, POP, COUNTRY]
NEW = [DIP, CHAR, LAW, EFFECT, FR, EN]
CORE = ['xCA4E6B', 'x009F47', 'xE6917C', 'xC724C8', 'x3B68A8', 'x92D93F', 'x7DEA64']
LINK = ['x522D29', 'xCD6775']
MOR = 'x0FA44F x4DE76B x53C5EF x88C527 x8ACEDE x8DCD09 x9E582E xE80E2E xF414B2'.split()
TRI = ['xAFD438', 'xD5C61D']
SID_PLAN = [('STATE_LIBYAN_DESERT', CORE), ('STATE_TRIPOLI', LINK)]


def dump(name, value):
    (LOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def load(name):
    return json.loads((LOT / name).read_text('utf8'))


def part(node, tag):
    return next(n for n in node.children('create_state') if n.one('country') == 'c:' + tag)


def ids(node, key):
    return [c.strip('"') for c in b.a.ids(node, key)]


def transformed(old):
    text = old[ST]
    ops = []
    inner = b.one(text, 's:STATE_INNER_MOROCCO')
    p = part(inner, 'MOR')
    owned = ids(p, 'owned_provinces')
    assert set(MOR).issubset(owned) and set(ids(part(inner, 'TEK'), 'owned_provinces')) == set(MOR)
    field = p.children('owned_provinces')[0]
    ops.append((field.start, field.end, 'owned_provinces = { ' + ' '.join(c for c in owned if c not in MOR) + ' }'))
    for sid, colors in SID_PLAN:
        state = b.one(text, 's:' + sid)
        p = part(state, 'ZWY')
        owned = ids(p, 'owned_provinces')
        assert set(colors).issubset(owned) and not any(n.one('country') == 'c:FZN' for n in state.children('create_state'))
        remove = set(colors) | (set(TRI) if sid == 'STATE_TRIPOLI' else set())
        field = p.children('owned_provinces')[0]
        ops.append((field.start, field.end, 'owned_provinces = { ' + ' '.join('"' + c + '"' for c in owned if c not in remove) + ' }'))
        # A native subdivision is retained; no new region/resources/hub is invented.
        ops.append((state.end - 1, state.end - 1, '\n\t\tcreate_state = { country = c:FZN owned_provinces = { ' + ' '.join(colors) + ' } }\n\t'))
    output = {ST: b.edits(text, ops)}
    text = old[POP]
    ops = []
    ledger = []
    for sid, colors in SID_PLAN:
        state = b.one(text, 's:' + sid)
        source = state.children('region_state:ZWY')[0]
        assert not state.children('region_state:FZN')
        source_state = b.one(old[ST], 's:' + sid)
        denominator = len(set(ids(part(source_state, 'ZWY'), 'owned_provinces')))
        fragments = []
        for pop in source.children('create_pop'):
            size = pop.children('size')[0]
            before = int(size.value)
            moved = (before * len(colors) + denominator // 2) // denominator
            assert 0 < moved < before
            ops.append((size.start, size.end, 'size = ' + str(before - moved)))
            frag = text[pop.start:pop.end]
            fragments.append(b.edits(frag, [(size.start - pop.start, size.end - pop.start, 'size = ' + str(moved))]))
            ledger.append({'state': sid, 'source': 'ZWY', 'recipient': 'FZN',
                           'culture': pop.one('culture'), 'religion': pop.one('religion'),
                           'pop_type': pop.one('pop_type'), 'before': before,
                           'after_ZWY': before - moved, 'after_FZN': moved,
                           'technical_fraction': [len(colors), denominator],
                           'historical_census_estimate': False})
        ops.append((state.end - 1, state.end - 1, '\n\t\tregion_state:FZN = {\n\t\t\t' + '\n\t\t\t'.join(fragments) + '\n\t\t}\n\t'))
    output[POP] = b.edits(text, ops)
    assert old[COUNTRY].count('effect_starting_politics_traditional = yes') == 1
    output[COUNTRY] = old[COUNTRY].replace('effect_starting_politics_traditional = yes', 'effect_aor1776_fezzan_starting_politics = yes')
    return output, ledger


def new_files():
    native = b.a.raw(b.a.GAME / 'common/scripted_effects/00_political_setup.txt')
    node = b.one(native, 'effect_starting_politics_traditional')
    politics = native[node.start:node.end].replace('effect_starting_politics_traditional', 'effect_aor1776_fezzan_starting_politics', 1)
    assert politics.count('law_type:law_mercantilism') == 1
    politics = politics.replace('law_type:law_mercantilism', 'law_type:law_aor1776_fezzan_caravan_tolls')
    return {
        DIP: '''# Awlad Muhammad autonomy and the tribute relationship to Tripoli.
DIPLOMACY = {
 c:TRI ?= { create_diplomatic_pact = { country = c:FZN type = tributary } }
}
''',
        CHAR: '''# Native FZN templates describe nineteenth-century Awlad Sulayman leaders.
# The 1776 restoration uses the engine's ordinary ruler generation; no invented
# historical Awlad Muhammad ruler or additional general is scripted here.
CHARACTERS = { }
''',
        LAW: '''# Existing customs effects, without granting maritime insurance to an oasis.
law_aor1776_fezzan_caravan_tolls = {
 group = lawgroup_trade_policy
 parent = law_mercantilism
 icon = "gfx/interface/icons/law_icons/mercantilism.dds"
 progressiveness = 0
 unlocking_technologies = { international_relations }
 is_visible = { c:FZN ?= this }
 can_enact = { c:FZN ?= this }
 modifier = {
  state_tariff_import_add = 0.50
  state_tariff_export_add = 0.20
  state_subvention_export_add = 0.50
  state_subvention_import_add = 0.20
  state_import_advantage_mult = -0.25
  state_export_advantage_mult = 0.25
 }
}
''',
        EFFECT: '# FZN-only copy of native initial politics; one trade-law substitution.\n' + politics + '\n',
        FR: 'l_french:\n law_aor1776_fezzan_caravan_tolls:0 "Péages caravaniers"\n law_aor1776_fezzan_caravan_tolls_desc:0 "Le pouvoir prélève des droits sur les caravanes et les marchandises qui traversent les oasis."\n',
        EN: 'l_english:\n law_aor1776_fezzan_caravan_tolls:0 "Caravan Tolls"\n law_aor1776_fezzan_caravan_tolls_desc:0 "The government collects duties on caravans and goods passing through the oases."\n',
    }


def apply():
    assert not (LOT / 'FILES_MODIFIED.json').exists(), 'Already installed; validate only.'
    assert all(not (ROOT / r).exists() for r in NEW), 'Review current file, never overwrite.'
    before = b4.inventory()
    old = {r: b.a.raw(ROOT / r) for r in EDIT}
    expected_hashes = {r: b.a.sha(ROOT / r) for r in EDIT}
    out, ledger = transformed(old)
    for r in EDIT:
        target = LOT / 'apply_inputs' / r
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / r, target)
    dump('APPLY_BEFORE.json', before)
    dump('POP_ALLOCATION.json', ledger)
    assert all(b.a.sha(ROOT / r) == h for r, h in expected_hashes.items()), 'Shared input changed; reread.'
    for r, text in out.items():
        bom = b'\xef\xbb\xbf' if (ROOT / r).read_bytes().startswith(b'\xef\xbb\xbf') else b''
        (ROOT / r).write_bytes(bom + text.encode('utf8'))
    for r, text in new_files().items():
        path = ROOT / r
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write((b'\xef\xbb\xbf' if r.endswith('.yml') else b'') + text.encode('utf8'))
    dump('FILES_MODIFIED.json', [{'file': r, 'before': expected_hashes.get(r), 'after': b.a.sha(ROOT / r)} for r in EDIT + NEW])
    print('Installed: Fezzan core and link, 11 duplicate owners removed; Siwa remains Egyptian.')


def province_graph():
    regions = {n.key: n for p in b.tech.effective('map_data/state_regions') for n in b.parse(b.a.raw(p))}
    impassable = {c for n in regions.values() for c in ids(n, 'impassable')}
    arr = np.asarray(Image.open(ROOT / 'map_data/provinces.png').convert('RGB'), dtype=np.uint32)
    packed = arr[:, :, 0] * 65536 + arr[:, :, 1] * 256 + arr[:, :, 2]
    # All changed territories and the complete Egyptian connection lie here.
    crop = packed[1200:1650, 3780:4900]
    adj = defaultdict(set)
    for a, c in [(crop[:, :-1], crop[:, 1:]), (crop[:-1, :], crop[1:, :])]:
        mask = a != c
        pairs = np.unique(np.column_stack((a[mask], c[mask])), axis=0)
        for x, y in pairs:
            x, y = 'x' + f'{int(x):06X}', 'x' + f'{int(y):06X}'
            if x not in impassable and y not in impassable:
                adj[x].add(y)
                adj[y].add(x)
    return adj, impassable


def find_path(adj, start, goal, allowed):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        if goal(path[-1]):
            return path
        for nxt in sorted(adj[path[-1]]):
            if nxt not in seen and allowed(nxt):
                seen.add(nxt)
                queue.append(path + [nxt])
    return None


def validate():
    base = load('BASELINE.json')
    before = load('APPLY_BEFORE.json')
    current = b4.inventory()
    checks = []
    def ck(name, result, detail=None):
        checks.append({'check': name, 'passed': bool(result), 'detail': detail})
    old = {r: b.a.raw(LOT / 'apply_inputs' / r) for r in EDIT}
    output, ledger = transformed(old)
    peer_path = LOT / 'EXTERNAL_REVIEW.json'
    peer = load('EXTERNAL_REVIEW.json') if peer_path.exists() else {}
    def with_peer_states(text):
        if not peer:
            return text
        snapshot = b.a.raw(LOT / peer['state_snapshot'])
        ops = []
        for key in peer['state_regions']:
            original = b.one(text, key)
            external = b.one(snapshot, key)
            ops.append((original.start, original.end, snapshot[external.start:external.end]))
        return b.edits(text, ops)
    output[ST] = with_peer_states(output[ST])
    for r, text in output.items():
        ck('exact_current_version_targeted_patch.' + r, b.a.raw(ROOT / r) == text)
    for r, text in new_files().items():
        ck('exact_new_file.' + r, b.a.raw(ROOT / r) == text)
    expected = dict(before['owners'])
    for color in MOR:
        expected[color] = [['STATE_INNER_MOROCCO', 'TEK']]
    for color in TRI:
        expected[color] = [['STATE_TRIPOLI', 'TRI']]
    for sid, colors in SID_PLAN:
        for color in colors:
            expected[color] = [[sid, 'FZN']]
    expected.update(peer.get('state_owner_updates', {}))
    ck('only_twenty_declared_RGB_owner_resolutions', current['owners'] == expected)
    owners = current['owners']
    for color in MOR + TRI + CORE + LINK:
        ck('one_owner.' + color, len(owners.get(color, [])) == 1, owners.get(color))
    scopes = {'STATE_INNER_MOROCCO', 'STATE_TRIPOLI', 'STATE_LIBYAN_DESERT', 'STATE_MATRUH'}
    ck('no_remaining_duplicate_in_corrected_regions', not any(len(v) > 1 and any(s in scopes for s, _ in v) for v in owners.values()))
    inherited = {c: v for c, v in before['owners'].items() if len(v) > 1 and not any(s in scopes for s, _ in v)}
    ck('inherited_duplicates_elsewhere_unchanged', {c: v for c, v in owners.items() if len(v) > 1} == inherited, inherited)
    adj, impassable = province_graph()
    def own(c, tag):
        return owners.get(c, []) and all(t == tag for _, t in owners[c])
    fzn = set(CORE + LINK)
    route = find_path(adj, CORE[0], lambda c: own(c, 'TRI'), lambda c: c in fzn or own(c, 'TRI'))
    ck('Fezzan_passable_link_to_centralized_Tripoli', bool(route), route)
    ck('every_Fezzan_province_connected_to_capital', all(find_path(adj, CORE[0], lambda c, target=target: c == target, lambda c: c in fzn) for target in fzn))
    ck('no_Fezzan_impassable_province', not (fzn & impassable))
    for color in TRI:
        ck('Tripoli_resolved_polygon_not_enclave.' + color, bool(find_path(adj, color, lambda c: c == 'x84D04D', lambda c: own(c, 'TRI'))))
    egypt_route = find_path(adj, 'xE0D021', lambda c: owners.get(c) == [['STATE_LOWER_EGYPT', 'EGY']], lambda c: own(c, 'EGY'))
    ck('Siwa_Egyptian_passable_route_to_Nile', bool(egypt_route), egypt_route)
    ck('Siwa_all_Egyptian_owners_unchanged', all(owners[c] == value for c, value in before['owners'].items() if any(tag == 'EGY' for _, tag in value)))
    dump('CORRIDORS.json', {'Fezzan_to_Tripoli': route, 'Siwa_to_Egypt': egypt_route,
         'adjacency': 'Four-neighbour shared land edge; impassable provinces excluded.',
         'user_rule_location': 'This lot only; AGENTS.md and .agents not modified.'})
    ck('population_transfer_records_conserved', all(r['before'] == r['after_ZWY'] + r['after_FZN'] for r in ledger))
    ck('world_population_conserved', before['world_population'] == current['world_population'], current['world_population'])
    ck('Git_identity_and_index_conserved', before['git'] == current['git'])
    # Preserve everything outside the declared state/pop nodes byte for byte.
    for rel, scoped in [(ST, ['STATE_INNER_MOROCCO', 'STATE_TRIPOLI', 'STATE_LIBYAN_DESERT']), (POP, [x[0] for x in SID_PLAN])]:
        def outside(text):
            nodes = [b.one(text, 's:' + sid) for sid in scoped]
            return b.edits(text, [(n.start, n.end, '<SCOPED>') for n in nodes])
        reference = with_peer_states(old[rel]) if rel == ST else old[rel]
        ck('all_other_regions_identical_with_reviewed_peer_nodes.' + rel, outside(reference) == outside(b.a.raw(ROOT / rel)))
    for r in ['map_data/provinces.png', 'map_data/state_regions/03_north_africa.txt', 'map_data/province_terrains.txt', 'common/strait_definitions/strait_definitions.txt']:
        ck('protected.' + r, b.a.sha(ROOT / r) == base['protected'][r])
    differences = [{'file': r, 'before': h, 'current': b.a.sha(ROOT / r) if (ROOT / r).exists() else None}
                   for r, h in base['protected'].items() if r not in EDIT and (not (ROOT / r).exists() or b.a.sha(ROOT / r) != h)]
    admitted = peer.get('reviewed_differences', [])
    unreviewed = [row for row in differences if row not in admitted]
    dump('CONCURRENT_CHANGES.json', {'differences_outside_scope': differences, 'unreviewed': unreviewed,
         'external_shared_state_regions': peer.get('state_regions', []),
         'SERG_writes': 0, 'Git_writes': 0, 'vanilla_writes': 0, 'restored_old_baseline': False})
    ck('all_unattributed_changes_absent', not unreviewed, unreviewed)
    ck('external_shared_snapshot_preserved', not peer or b.a.sha(LOT / peer['state_snapshot']) == peer['state_snapshot_sha256'])
    dump('POPULATION_LEDGER.json', {'world_before': before['world_population'], 'world_after': current['world_population'],
         'delta': current['world_population'] - before['world_population'], 'transferred_to_FZN': sum(r['after_FZN'] for r in ledger),
         'allocation_method': 'Technical split of existing cohorts, 7/53 and 2/53 native provinces; no historical population per pixel or new census inferred.', 'cohort_ledger': ledger})
    result = {'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL', 'passed': sum(c['passed'] for c in checks),
              'total': len(checks), 'checks': checks, 'runtime': 'NOT_RUN', 'human_validation': False}
    dump('VALIDATION.json', result)
    print(json.dumps({k: result[k] for k in ['status', 'passed', 'total']}))
    return result['status'] == 'PASS'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    if args.apply:
        apply()
    if args.validate:
        raise SystemExit(0 if validate() else 1)
