"""Northern Senegambia, bounded first Sahel lot. No Git/vanilla writes.

--apply captures the current workspace before patching only Senegal nodes;
--validate checks ownership, demographic conservation and protected data.
Goree is an explicitly documented coastal proxy, not a new physical island.
"""
import argparse
import io
import json
import shutil
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import world1776_balkans03 as b
import world1776_balkans04 as b4
import world1776_gibraltar as g

ROOT = b.ROOT
LOT = b.OUT / 'SAHEL-01'
SID = 'STATE_SENEGAL'
ST = 'common/history/states/00_states.txt'
POP = 'common/history/pops/04_subsaharan_africa.txt'
REG = 'map_data/state_regions/04_subsaharan_africa.txt'
TER = 'map_data/province_terrains.txt'
BMP = 'map_data/provinces.png'
EDIT = [ST, POP, REG, TER, BMP]
TECHS = ['improved_agricultural_implements', 'improved_husbandry',
         'international_relations', 'organized_textile_production',
         'traditional_food_processing', 'organized_workshops']
PREFIX = '1776_world_sahel01_waalo'


def dump(name, obj):
    (LOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def load(name):
    return json.loads((LOT / name).read_text('utf8'))


def rgb(key):
    return tuple(bytes.fromhex(key[1:]))


def ids(node, key):
    return [x.strip('"') for x in b.a.ids(node, key)]


def part(node, tag):
    nodes = [p for p in node.children('create_state') if p.one('country') == 'c:' + tag]
    assert len(nodes) == 1, (tag, len(nodes))
    return nodes[0]


def allocate(total, weights):
    """Largest remainders, deterministic and exactly conservative."""
    den = sum(weights)
    values = [total * w // den for w in weights]
    for i in sorted(range(len(weights)), key=lambda i: (-(total * weights[i] % den), i))[:total-sum(values)]:
        values[i] += 1
    assert sum(values) == total
    return values


def additions():
    files = {}
    files['common/country_definitions/' + PREFIX + '.txt'] = '''WAA = {
 color = { 174 114 73 }
 country_type = unrecognized
 tier = principality
 religion = animist
 cultures = { wolof }
 capital = STATE_SENEGAL
}
'''
    files['common/history/countries/waa - waalo.txt'] = 'COUNTRIES = { c:WAA ?= {\n' + ''.join(
        ' add_technology_researched = ' + t + '\n' for t in TECHS) + ''' effect_aor1776_waalo_starting_politics = yes
 activate_law = law_type:law_oligarchy
 activate_law = law_type:law_slave_trade
} }
'''
    # Native political setup, one scoped law substitution, no extra technology grant.
    source = b.a.GAME / 'common/scripted_effects/00_political_setup.txt'
    text = b.a.raw(source)
    n = b.one(text, 'effect_starting_politics_traditional')
    fragment = text[n.start:n.end]
    assert fragment.count('law_type:law_mercantilism') == 1
    files['common/scripted_effects/' + PREFIX + '.txt'] = (
        '# Native initial setup; trade customs available without maritime insurance.\n' +
        fragment.replace('effect_starting_politics_traditional', 'effect_aor1776_waalo_starting_politics', 1)
        .replace('law_type:law_mercantilism', 'law_type:law_aor1776_waalo_trade_customs') + '\n')
    # Match the current common trade recipe exactly; only availability is local.
    law, path = b.a.catalog('common/laws')['law_mercantilism']
    modifiers = law.children('modifier')[0]
    recipe = b.a.raw(path)[modifiers.start:modifiers.end]
    files['common/laws/' + PREFIX + '.txt'] = '''law_aor1776_waalo_trade_customs = {
 group = lawgroup_trade_policy
 parent = law_mercantilism
 icon = "gfx/interface/icons/law_icons/mercantilism.dds"
 progressiveness = 0
 unlocking_technologies = { international_relations }
 is_visible = { c:WAA ?= this }
 can_enact = { c:WAA ?= this }
 ''' + recipe + '\n}\n'
    translations = {
        'french': {'WAA': 'Waalo', 'WAA_ADJ': 'waalo',
                   'law_aor1776_waalo_trade_customs': 'Coutumes commerciales',
                   'law_aor1776_waalo_trade_customs_desc': 'Les marchands acquittent les droits du royaume pour commercer sur ses terres et ses voies fluviales.'},
        'english': {'WAA': 'Waalo', 'WAA_ADJ': 'Waalo',
                    'law_aor1776_waalo_trade_customs': 'Trade Customs',
                    'law_aor1776_waalo_trade_customs_desc': 'Merchants pay the kingdom’s dues to trade on its lands and waterways.'}}
    for lang, strings in translations.items():
        files[f'localization/{lang}/{PREFIX}_l_{lang}.yml'] = (
            'l_' + lang + ':\n' + ''.join(f' {k}:0 "{v}"\n' for k, v in strings.items()))
    return files


def transform(old):
    plan = load('PLAN.json')
    text = old[ST]
    state = b.one(text, 's:' + SID)
    fra = part(state, 'FRA')
    assert set(ids(fra, 'owned_provinces')) == set(plan['WAA'] + plan['FTR_from_FRA'])
    assert not any(p.one('country') in ['c:WAA', 'c:GBR'] for p in state.children('create_state'))
    field = fra.children('owned_provinces')[0]
    ops = [(field.start, field.end, 'owned_provinces = { xE8D242 }')]
    ftr = part(state, 'FTR').children('owned_provinces')[0]
    ops.append((ftr.end - 1, ftr.end - 1, ' ' + ' '.join(plan['FTR_from_FRA']) + ' '))
    ops.append((state.end - 1, state.end - 1, '''
        create_state = { country = c:WAA owned_provinces = { ''' + ' '.join(plan['WAA']) + ''' } }
        create_state = { country = c:GBR owned_provinces = { xE8D241 } state_type = unincorporated }
    '''))
    result = {ST: b.edits(text, ops)}

    text = old[REG]
    n = b.one(text, SID).children('provinces')[0]
    result[REG] = b.edits(text, [(n.end - 1, n.end - 1, ' "xE8D241" "xE8D242" ')])
    terrain = {n.key: n.value for n in b.parse(old[TER])}
    result[TER] = old[TER].rstrip() + '\n\n# SAHEL-01: inherit existing coastal land terrain.\n' + ''.join(
        p['rgb'] + ' = ' + terrain[p['parent']] + '\n' for p in plan['cores'])

    text = old[POP]
    n = b.one(text, 's:' + SID)
    source = n.children('region_state:FRA')[0]
    source_pops = source.children('create_pop')
    weights = [int(p.one('size')) for p in source_pops]
    source_total = sum(weights)
    # Contemporary settlement totals bound the small coastal portions; preserve
    # existing culture/religion/slave cohorts rather than inventing new populations.
    gb = allocate(4622, weights)
    fr = allocate(1569, [w - v for w, v in zip(weights, gb)])
    remaining = [w - x - y for w, x, y in zip(weights, gb, fr)]
    wa = allocate((sum(remaining) + 1) // 2, remaining)
    ft = [w - x for w, x in zip(remaining, wa)]
    assignments = {'FRA': fr, 'GBR': gb, 'WAA': wa, 'FTR': ft}
    fragments = {}
    for tag, sizes in assignments.items():
        fragments[tag] = []
        for pop, size in zip(source_pops, sizes):
            f = pop.children('size')[0]
            fragment = text[pop.start:pop.end]
            fragments[tag].append(b.edits(fragment, [(f.start-pop.start, f.end-pop.start, 'size = ' + str(size))]))
    ops = [(source.start, source.end, 'region_state:FRA = {\n' + '\n'.join(fragments['FRA']) + '\n}')]
    ftr = n.children('region_state:FTR')[0]
    ops.append((ftr.end - 1, ftr.end - 1, '\n' + '\n'.join(fragments['FTR']) + '\n'))
    ops.append((n.end - 1, n.end - 1, '\n' + '\n'.join(
        'region_state:' + tag + ' = {\n' + '\n'.join(fragments[tag]) + '\n}' for tag in ['WAA', 'GBR']) + '\n'))
    result[POP] = b.edits(text, ops)
    ledger = {'source': 'FRA', 'state': SID, 'source_total': source_total,
              'transfers': {tag: sum(v) for tag, v in assignments.items()},
              'cohort_sizes': assignments, 'method': 'Settlement totals 4622/1569 from 1776 observations; residual divided equally between three Waalo and three upstream Futa provinces. Technical allocation only; not a census or equal historical density assertion. Existing cohort identities conserved.'}
    return result, ledger


def apply():
    assert not (LOT / 'FILES_MODIFIED.json').exists(), 'Already installed; validate only.'
    new = additions()
    assert all(not (ROOT / r).exists() for r in new)
    cat = b.a.catalog('common/country_definitions')
    assert 'WAA' not in cat, 'TAG collision'
    old = {r: b.a.raw(ROOT / r) for r in EDIT if r != BMP}
    patched, ledger = transform(old)
    hashes = {r: b.a.sha(ROOT / r) for r in EDIT}
    before = b4.inventory()
    g.LOT = LOT
    dump('APPLY_BEFORE.json', {'inventory': before, 'protected': g.protection(),
         'vanilla_native_politics_sha256': b.a.sha(b.a.GAME / 'common/scripted_effects/00_political_setup.txt')})
    for rel in EDIT:
        target = LOT / 'apply_inputs' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    image = Image.open(ROOT / BMP).convert('RGB')
    packed = np.asarray(image)
    for p in load('PLAN.json')['cores']:
        assert not np.any(np.all(packed == rgb(p['rgb']), axis=2))
        for xy in p['pixels']:
            assert image.getpixel(tuple(xy)) == rgb(p['parent'])
            image.putpixel(tuple(xy), rgb(p['rgb']))
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    assert all(b.a.sha(ROOT / r) == h for r, h in hashes.items()), 'Concurrent edit: reread before retry.'
    for rel, text in patched.items():
        bom = b'\xef\xbb\xbf' if (ROOT / rel).read_bytes().startswith(b'\xef\xbb\xbf') else b''
        (ROOT / rel).write_bytes(bom + text.encode('utf8'))
    (ROOT / BMP).write_bytes(buf.getvalue())
    for rel, text in new.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((b'\xef\xbb\xbf' if rel.endswith('.yml') else b'') + text.encode('utf8'))
    dump('FILES_MODIFIED.json', [{'file': r, 'before': hashes.get(r), 'after': b.a.sha(ROOT / r)} for r in EDIT + list(new)])
    ledger.update(world_before=before['world_population'], world_after=b4.inventory()['world_population'])
    dump('POPULATION_LEDGER.json', ledger)
    print('Installed Waalo, upstream Futa Toro and two bounded coastal points.')


def cohorts(text):
    result = Counter()
    for p in b.walk(b.parse(text)):
        if p.key == 'create_pop':
            key = tuple((c.key, str(c.value)) for c in p.children() if c.key != 'size')
            result[key] += int(p.one('size'))
    return result


def outside(text, key):
    n = b.one(text, key)
    return b.edits(text, [(n.start, n.end, '<SCOPED_SENEGAL>')])


def validate():
    checks = []
    def ck(name, value, detail=None):
        checks.append(dict(check=name, passed=bool(value), detail=detail))
    before = load('APPLY_BEFORE.json')
    original = {r: b.a.raw(LOT / 'apply_inputs' / r) for r in EDIT if r != BMP}
    external = None
    if (LOT / 'EXTERNAL_COMPOSITION_REVIEW.json').exists():
        external = load('EXTERNAL_COMPOSITION_REVIEW.json')
        # Preserve immutable original inputs. Compose only the two independently
        # reviewed external nodes into the expected current reference in memory.
        ck('external_review_bound_to_two_North_American_nodes', external['reviewed'] and
           {r['state'] for r in external['blocks']} == {'s:STATE_ARKANSAS', 's:STATE_TEXAS'})
        ck('external_review_receipts_unchanged', all(b.a.sha(ROOT / p) == h for p, h in external['evidence'].items()))
        ck('external_review_snapshot_unchanged', b.a.sha(LOT/'external_snapshots/00_states_current.txt') == external['snapshot_sha256'])
        ops = []
        for row in external['blocks']:
            n = b.one(original[ST], row['state'])
            ck('external_input_node_matches_original.' + row['state'], original[ST][n.start:n.end] == row['before'])
            ops.append((n.start, n.end, row['after']))
        original[ST] = b.edits(original[ST], ops)
    transformed, ledger = transform(original)
    for rel, text in transformed.items():
        ck('exact_bounded_text_patch.' + rel, b.a.raw(ROOT / rel) == text)
    for rel, key in [(ST, 's:' + SID), (POP, 's:' + SID), (REG, SID)]:
        ck('outside_Senegal_byte_preserved.' + rel, outside(original[rel], key) == outside(b.a.raw(ROOT / rel), key))
    now = b4.inventory()
    expected = dict(before['inventory']['owners'])
    plan = load('PLAN.json')
    for c in plan['WAA']: expected[c] = [[SID, 'WAA']]
    for c in plan['FTR_from_FRA']: expected[c] = [[SID, 'FTR']]
    for p in plan['cores']: expected[p['rgb']] = [[SID, p['owner']]]
    if external:
        for row in external['owner_delta']:
            ck('external_owner_baseline_matches.' + row['rgb'], expected.get(row['rgb']) == row['before'])
            expected[row['rgb']] = row['after']
    ck('only_declared_Sahel_and_reviewed_external_owner_entries_changed', expected == now['owners'])
    ck('world_population_exactly_conserved', now['world_population'] == before['inventory']['world_population'], now['world_population'])
    ck('all_population_cohort_identities_conserved', cohorts(original[POP]) == cohorts(b.a.raw(ROOT / POP)))
    for tag, size in ledger['transfers'].items():
        n = b.one(b.a.raw(ROOT / POP), 's:' + SID)
        total = sum(int(p.one('size')) for part in n.children('region_state:' + tag) for p in part.children('create_pop'))
        ck('population_portion.' + tag, total == size if tag != 'FTR' else total == size + 94376, total)
    a = np.asarray(Image.open(LOT / 'apply_inputs' / BMP).convert('RGB'))
    z = np.asarray(Image.open(ROOT / BMP).convert('RGB'))
    yy, xx = np.where(np.any(a != z, axis=2))
    wanted = {tuple(xy) for p in plan['cores'] for xy in p['pixels']}
    ck('exact_five_existing_land_pixels_only', set(zip(xx.tolist(), yy.tolist())) == wanted and len(xx) == 5)
    ck('bitmap_dimensions_unchanged', a.shape == z.shape == (3616, 8192, 3))
    for p in plan['cores']:
        ck('pixel_core.' + p['name'], all(tuple(z[y, x]) == rgb(p['rgb']) and tuple(a[y, x]) == rgb(p['parent']) for x, y in p['pixels']))
        ck('whole_RGB_area.' + p['name'], int(np.count_nonzero(np.all(z == rgb(p['rgb']), axis=2))) == len(p['pixels']))
        ck('native_parent_remains.' + p['name'], np.any(np.all(z == rgb(p['parent']), axis=2)))
        ck('registered_land_terrain.' + p['name'], b.one(b.a.raw(ROOT / TER), p['rgb']).value == b.one(original[TER], p['parent']).value)
        ck('coastal.' + p['name'], any('x' + ''.join(f'{v:02X}' for v in a[ny, nx]) not in before['inventory']['owners']
            for x, y in p['pixels'] for nx, ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]))
    # Cardinal land connectivity of the new kingdom and the enlarged existing one.
    from collections import deque
    for tag in ['WAA', 'FTR']:
        colors = [k for k, v in now['owners'].items() if v == [[SID, tag]]]
        packed = z[:,:,0].astype('uint32') * 65536 + z[:,:,1].astype('uint32') * 256 + z[:,:,2]
        mask = np.isin(packed, [int(k[1:], 16) for k in colors])
        ys, xs = np.where(mask)
        left = set(zip(xs.tolist(), ys.tolist()))
        seen = {next(iter(left))}
        q = deque(seen)
        while q:
            x, y = q.popleft()
            for point in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if point in left and point not in seen:
                    seen.add(point)
                    q.append(point)
        ck('connected_country_portion.' + tag, len(left) == len(seen), {'land_pixels': len(left), 'reachable': len(seen)})
    region = b.one(b.a.raw(ROOT / REG), SID)
    region_colors = ids(region, 'provinces')
    all_portions = [c for p in b.one(b.a.raw(ROOT / ST), 's:' + SID).children('create_state') for c in ids(p, 'owned_provinces')]
    ck('every_Senegal_color_owned_exactly_once', len(all_portions) == len(set(all_portions)) and set(region_colors) == set(all_portions))
    ck('no_new_global_duplicate_owner', {k for k,v in now['owners'].items() if len(v)>1} == {k for k,v in before['inventory']['owners'].items() if len(v)>1})
    ck('native_SaintLouis_city_inside_British_core', tuple(z[1734, 3722]) == rgb('xE8D241'))
    for rel, text in additions().items():
        ck('exact_new_file.' + rel, b.a.raw(ROOT / rel) == text)
        if rel.endswith('.yml'):
            ck('localization_BOM.' + rel, (ROOT / rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    new_or_edit = {r['file'] for r in load('FILES_MODIFIED.json')}
    delta = [{'file': rel, 'before': h, 'after': b.a.sha(ROOT / rel) if (ROOT / rel).exists() else None}
             for rel, h in before['protected'].items() if rel not in new_or_edit and (not (ROOT / rel).exists() or b.a.sha(ROOT / rel) != h)]
    ck('other_functional_and_previous_proof_files_preserved', not delta, delta)
    ck('Git_identity_and_index_unchanged', now['git'] == before['inventory']['git'])
    ck('canonical_native_politics_not_modified', b.a.sha(b.a.GAME / 'common/scripted_effects/00_political_setup.txt') == before['vanilla_native_politics_sha256'])
    dump('CONCURRENT_CHANGES.json', {'changes_during_apply_or_checks': delta,
         'external_shared_state_composition': 'EXTERNAL_COMPOSITION_REVIEW.json' if external else None,
         'initial_strict_run': 'VALIDATION_RUN01_CONCURRENT.json' if external else None,
         'Git_writes': 0, 'vanilla_writes': 0, 'SERG_writes': 0})
    result = dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
                  passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                  runtime='NOT_RUN', human_validation=False)
    dump('VALIDATION.json', result)
    print(json.dumps({k: result[k] for k in ['status','passed','total']}))
    print('Failed:', [c['check'] for c in checks if not c['passed']])
    return result['status'] == 'PASS'


def render():
    before = load('APPLY_BEFORE.json')['inventory']['owners']
    after = b4.inventory()['owners']
    box = (3713, 1718, 3800, 1753)
    palette = {'WAA': '#ae7249', 'FTR': '#73cc66', 'FRA': '#4466cc', 'GBR': '#cd5555', 'JLF': '#bfc77a'}
    panels = []
    for image, owners in [(Image.open(LOT/'apply_inputs'/BMP).convert('RGB'), before), (Image.open(ROOT/BMP).convert('RGB'), after)]:
        crop = image.crop(box)
        for y in range(crop.height):
            for x in range(crop.width):
                key = 'x' + ''.join(f'{v:02X}' for v in crop.getpixel((x,y)))
                tag = owners.get(key, [[None,None]])[-1][1]
                crop.putpixel((x,y), tuple(bytes.fromhex(palette.get(tag, '#303b45').lstrip('#'))))
        panels.append(crop.resize((870,350), Image.Resampling.NEAREST))
    out = Image.new('RGB', (900,800), '#1c2229')
    draw = ImageDraw.Draw(out)
    draw.text((15,10), 'SAHEL-01 | Avant', fill='white')
    draw.text((15,395), 'Apres | Waalo brun, Fouta vert, Saint-Louis britannique rouge', fill='white')
    out.paste(panels[0], (15,35)); out.paste(panels[1], (15,420))
    draw.text((15,780), 'Provinces natives : approximation politique. Goree : point cotier hors de ce zoom.', fill='white')
    out.save(LOT/'NORTHERN_SENEGAL_BEFORE_AFTER.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    if args.apply: apply()
    if args.render: render()
    if args.validate: raise SystemExit(0 if validate() else 1)
