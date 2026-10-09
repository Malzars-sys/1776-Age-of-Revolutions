"""Export the retained scientific-management master; check its three PM variants.

Read-only by default. --export rebuilds only the named runtime DDS from its
retained PNG master, never modifies definitions or regenerates native unused art.
Requires Pillow; uses the same native BGRA8 layout as other fork UI assets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from PIL import Image

import asset4_style_reference_audit as art
from building_dds_compat import BGRA, assert_export_layout

ROOT = Path(__file__).resolve().parents[1]
ICON = 'gfx/interface/icons/production_method_icons/1776_scientific_management.dds'
MASTER = 'gfx/interface/icons/production_method_icons/1776_scientific_management_source.png'
OFF = 'gfx/interface/icons/production_method_icons/unused/no_org.dds'
PM_FILE = ROOT / 'common/production_methods/20_tech6d_wave_d_production.txt'
PMG_FILE = ROOT / 'common/production_method_groups/20_tech6d_wave_d_pmgs.txt'
VARIANTS = {
    'pm_scientific_management': 'pmg_scientific_management',
    'pm_scientific_management_automotive_industry': 'pmg_scientific_management_automotive_industry',
    'pm_scientific_management_electrics_industry': 'pmg_scientific_management_electrics_industry',
}


def prepared_icon():
    source = Image.open(ROOT / MASTER).convert('RGBA')
    assert source.width == source.height and source.width >= 1024
    alpha = source.getchannel('A')
    assert alpha.getextrema() == (0, 255), 'Master needs real transparency'
    # Format-only fit: retain the source, remove empty margins and pad for UI.
    bounds = alpha.point(lambda value: 255 if value >= 16 else 0).getbbox()
    assert bounds, 'Empty master'
    subject = source.crop(bounds)
    subject.thumbnail((176, 176), Image.Resampling.LANCZOS)
    target = Image.new('RGBA', (208, 208))
    target.paste(subject, ((208 - subject.width) // 2, (208 - subject.height) // 2))
    return target


def dds_bytes(target):
    header = bytearray(128)
    header[:4] = b'DDS '
    for offset, value in ((4, 124), (8, 0x2100f), (12, 208), (16, 208),
                          (20, 832), (28, 8), (76, 32), (80, 0x41), (88, 32),
                          (92, BGRA[0]), (96, BGRA[1]), (100, BGRA[2]),
                          (104, BGRA[3]), (108, 0x401008)):
        struct.pack_into('<I', header, offset, value)
    levels = []
    size = 208
    while size:
        mip = target.resize((size, size), Image.Resampling.LANCZOS)
        levels.append(mip.tobytes('raw', 'BGRA'))
        size >>= 1
    payload = bytes(header) + b''.join(levels)
    assert len(levels) == 8 and len(payload) == 230828
    assert_export_layout(payload, ICON)
    return payload


def validate_definitions():
    pms = dict(art.pairs(art.parse(PM_FILE)))
    pmgs = dict(art.pairs(art.parse(PMG_FILE)))
    assert art.field(pms['pm_no_scientific_management'], 'texture') == OFF
    assert art.resolve(OFF), 'Missing installed native disabled symbol'
    assert art.field(pms['pm_no_scientific_management'], 'building_modifiers', []) == []
    buildings = art.catalog('common/buildings')
    used_groups = {group for tokens, _ in buildings.values()
                   for group in art.field(tokens, 'production_method_groups', [])}
    for pm, pmg in VARIANTS.items():
        tokens = pms[pm]
        assert art.field(tokens, 'texture') == ICON, pm
        assert art.field(pmgs[pmg], 'texture') == ICON, pmg
        assert art.field(pmgs[pmg], 'production_methods') == ['pm_no_scientific_management', pm]
        assert pmg in used_groups, pmg
        assert art.field(tokens, 'unlocking_technologies') == ['corporate_management']
        modifiers = art.field(tokens, 'building_modifiers')
        workforce = dict(art.pairs(art.field(modifiers, 'workforce_scaled')))
        assert workforce == {'goods_input_paper_add': '5', 'goods_input_services_add': '10',
                             'goods_input_organized_research_data_add': '1'}, pm
        per_level = dict(art.pairs(art.field(modifiers, 'level_scaled')))
        assert per_level == {'building_employment_laborers_add': '-500',
                             'building_employment_machinists_add': '-250',
                             'building_employment_clerks_add': '500',
                             'building_employment_engineers_add': '250',
                             'building_throughput_add': '0.005'}, pm
        assert art.field(modifiers, 'unscaled', []) == [], pm
    goods = art.catalog('common/goods')
    assert 'organized_research_data' in goods
    modifiers = art.catalog('common/modifier_type_definitions')
    assert 'goods_input_organized_research_data_add' in modifiers
    assert 'building_throughput_add' in modifiers
    return [{'level': level, 'throughput_bonus_percent': level * 0.5,
             'organized_data_recipe_input_before_throughput': level}
            for level in (1, 10, 20, 50)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', action='store_true')
    parser.add_argument('--game', type=Path, default=Path('C:/Games/Victoria 3/game'))
    args = parser.parse_args()
    art.GAME = args.game.resolve()
    expected = dds_bytes(prepared_icon())
    if args.export:
        (ROOT / ICON).write_bytes(expected)
    actual = (ROOT / ICON).read_bytes()
    assert actual == expected, 'Runtime DDS differs from reproducible master export'
    icon = art.decode(ROOT / ICON)
    assert icon.size == (208, 208)
    alpha = icon.getchannel('A')
    assert 0.1 < sum(value > 128 for value in alpha.tobytes()) / (208 * 208) < 0.75
    assert not any(alpha.crop((0, 0, 208, 1)).tobytes())
    assert not any(alpha.crop((0, 207, 208, 208)).tobytes())
    assert not any(alpha.crop((0, 0, 1, 208)).tobytes())
    assert not any(alpha.crop((207, 0, 208, 208)).tobytes())
    assert art.header(ROOT / ICON)['mips'] == 8
    scenarios = validate_definitions()
    print(json.dumps({'status': 'PASS_STATIC_SCIENTIFIC_MANAGEMENT', 'variants': len(VARIANTS),
                      'icon': ICON, 'source': MASTER, 'dimensions': [208, 208], 'mips': 8,
                      'format': 'native BGRA8', 'dds_sha256': hashlib.sha256(actual).hexdigest(),
                      'level_examples': scenarios, 'game_tested': False}, indent=2))


if __name__ == '__main__':
    main()
