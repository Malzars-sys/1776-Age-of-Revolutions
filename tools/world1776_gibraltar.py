"""Reattach Gibraltar's African endpoint to the installed Spanish Ceuta core.

No map, POP, mission, building, vanilla or Git writes. Native same-filename
override preserves every other strait definition from the current game.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image
import world1776_balkans03 as b
import world1776_balkans04 as b4

ROOT = b.ROOT
LOT = b.OUT / 'MAGHREB-01-GIBRALTAR'
REL = 'common/strait_definitions/strait_definitions.txt'
SOURCE = b.a.GAME / REL
TARGET = ROOT / REL


def dump(name, value):
    (LOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def hashes(paths):
    return {p.relative_to(ROOT).as_posix(): b.a.sha(p) for p in sorted(set(paths)) if p.is_file()}


def protection():
    paths = []
    for folder in ['common', 'events', 'gui', 'localization', 'map_data']:
        paths.extend(p for p in (ROOT / folder).rglob('*') if p.suffix in ['.txt', '.yml', '.gui', '.json'])
    paths.extend(ROOT / p for p in ['map_data/provinces.png', 'map_data/heightmap.png', 'map_data/packed_heightmap.png', 'descriptor.mod'])
    for folder in ['docs/reports/map/SERG_CLOSURE']:
        paths.extend((ROOT / folder).rglob('*'))
    for folder in b.OUT.iterdir():
        if folder.is_dir() and folder != LOT:
            paths.extend(folder.rglob('*'))
    return hashes(paths)


def transformed(source):
    text = source.decode('utf-8-sig')
    node = b.one(text, 'strait_gibraltar')
    field = node.children('second_land_endpoint')[0]
    assert field.value == 'xA0B0C0'
    part = text[field.start:field.end]
    assert part.count('xA0B0C0') == 1
    result = b.edits(text, [(field.start, field.end, part.replace('xA0B0C0', 'xE8D231'))])
    return (b'\xef\xbb\xbf' if source.startswith(b'\xef\xbb\xbf') else b'') + result.encode('utf8')


def apply():
    assert not TARGET.exists(), 'Existing strait override must be reviewed, never overwritten.'
    assert not (LOT / 'BASELINE.json').exists(), 'Already captured; use --validate.'
    source = SOURCE.read_bytes()
    output = transformed(source)
    # Parsing and exact byte comparison are done before the sole functional write.
    assert output.replace(b'xE8D231', b'xA0B0C0') == source
    LOT.mkdir(parents=True, exist_ok=True)
    base = {'captured_utc': datetime.now(timezone.utc).isoformat(),
            'inventory': b4.inventory(), 'protected': protection(),
            'vanilla_sha256': b.a.sha(SOURCE), 'target_existed': False}
    dump('BASELINE.json', base)
    (LOT / 'VANILLA_STRAITS_REFERENCE.txt').write_bytes(source)
    assert SOURCE.read_bytes() == source and not TARGET.exists(), 'Source or target changed; reread.'
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open('xb') as stream:
        stream.write(output)
    dump('FILES_MODIFIED.json', [{'file': REL, 'before': None, 'after': b.a.sha(TARGET),
         'reference_sha256': base['vanilla_sha256'], 'only_semantic_change':
         'strait_gibraltar.second_land_endpoint: xA0B0C0 -> xE8D231'}])
    print('Installed: African Gibraltar endpoint on Spanish Ceuta; all other straits preserved.')


def validate():
    base = json.loads((LOT / 'BASELINE.json').read_text('utf8'))
    current = b4.inventory()
    reference = (LOT / 'VANILLA_STRAITS_REFERENCE.txt').read_bytes()
    checks = []
    def ck(name, result, detail=None):
        checks.append({'check': name, 'passed': bool(result), 'detail': detail})
    ck('exact_one_field_patch_in_current_native_file', TARGET.read_bytes() == transformed(reference))
    ck('vanilla_reference_unchanged', b.a.sha(SOURCE) == base['vanilla_sha256'])
    original = b.parse(reference.decode('utf-8-sig'))
    installed = b.parse(b.a.raw(TARGET))
    ck('same_twelve_unique_strait_definitions', len(installed) == len(original) == 12 and len({n.key for n in installed}) == 12)
    for old in original:
        if old.key != 'strait_gibraltar':
            ck('other_strait_unchanged.' + old.key, b.normalized([old]) == b.normalized([next(n for n in installed if n.key == old.key)]))
    g = next(n for n in installed if n.key == 'strait_gibraltar')
    for key, expected in [('first_land_endpoint', 'xBC6ED3'), ('second_land_endpoint', 'xE8D231'),
                          ('first_sea_endpoint', 'x5FDDFB'), ('second_sea_endpoint', 'x40D9DB'),
                          ('type', 'natural'), ('total_block_requires_full_control', 'yes'),
                          ('military_block_requires_full_control', 'yes'), ('tolls_require_full_control', 'yes')]:
        ck('Gibraltar.' + key, g.one(key) == expected)
    owners = current['owners']
    for color, expected in [('xE8D231', [['STATE_AL_RIF', 'SPA']]), ('xE8D232', [['STATE_AL_RIF', 'SPA']]),
                            ('xE8D233', [['STATE_ORAN', 'SPA']]), ('xA0B0C0', [['STATE_AL_RIF', 'MOR']]),
                            ('xBC6ED3', [['STATE_UPPER_ANDALUSIA', 'GBR']])]:
        ck('owner.' + color, owners.get(color) == expected, owners.get(color))
    image = np.asarray(Image.open(ROOT / 'map_data/provinces.png').convert('RGB'))
    ceuta = np.all(image == tuple(bytes.fromhex('E8D231')), axis=2)
    ys, xs = np.where(ceuta)
    ck('Ceuta_one_existing_pixel', list(zip(xs.tolist(), ys.tolist())) == [(3973, 1252)])
    terrain = b.one(b.a.raw(ROOT / 'map_data/province_terrains.txt'), 'xE8D231').value
    ck('Ceuta_registered_land', terrain not in ['ocean', 'lakes'] and 'xE8D231' in b.a.raw(ROOT / 'map_data/state_regions/03_north_africa.txt'))
    for sea in ['x5FDDFB', 'x40D9DB']:
        ck('sea_endpoint_exists_and_not_land.' + sea, sea not in owners and np.any(np.all(image == tuple(bytes.fromhex(sea[1:])), axis=2)))
    ck('all_territorial_ownership_unchanged', owners == base['inventory']['owners'])
    ck('world_population_unchanged', current['world_population'] == base['inventory']['world_population'], current['world_population'])
    ck('Git_identity_and_index_unchanged', current['git'] == base['inventory']['git'])
    differences = [{'file': rel, 'before': h, 'after': b.a.sha(ROOT / rel) if (ROOT / rel).exists() else None}
                   for rel, h in base['protected'].items() if not (ROOT / rel).exists() or b.a.sha(ROOT / rel) != h]
    ck('all_existing_functional_and_prior_proof_files_preserved', not differences, differences)
    overrides = list((ROOT / 'common/strait_definitions').glob('*.txt'))
    ck('one_native_filename_override', overrides == [TARGET])
    dump('CONCURRENT_CHANGES.json', {'protected_files': len(base['protected']), 'differences': differences,
         'Git_writes': 0, 'SERG_writes': 0, 'vanilla_writes': 0})
    dump('POPULATION_LEDGER.json', {'before': base['inventory']['world_population'], 'after': current['world_population'],
         'delta': current['world_population'] - base['inventory']['world_population'], 'POP_files_written': 0})
    result = {'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
              'passed': sum(c['passed'] for c in checks), 'total': len(checks), 'checks': checks,
              'runtime': 'NOT_RUN', 'human_validation': False}
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
