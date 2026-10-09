"""Snapshot/check the small early-ship role correction; no game or runtime writes.

Preparation derives a colour-only caravel candidate in ignored cache. Its
approved master is exported by rebuild_asset_icons.cjs, not this validator.
"""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import recolour_pm_icons as colour
import preview_pm_group_bindings as bindings
import asset4_style_reference_audit as art

ROOT = colour.ROOT
CACHE = ROOT/'.asset-cache/early_ship_roles_2026-10-08'
SHIP = 'common/ship_types/10_1776_early_ships.txt'
FR = 'localization/french/1776_early_ships_l_french.yml'
EN = 'localization/english/1776_early_ships_l_english.yml'
DDS = 'gfx/interface/icons/ships/ship_types/1776_silhouette_caravel.dds'
SOURCE = 'docs/reports/assets/early_ship_sources_2026-10-08/caravel.png'
REFERENCE = Path('C:/Games/Victoria 3/game/gfx/interface/icons/ships/ship_types/silhouette_ship_of_the_line.dds')
MANIFEST = 'docs/reports/assets/early_ship_sources_2026-10-08/capital_colour_revision.json'

def expected_roles(raw):
    def transform(match):
        block = match.group()
        if block.startswith('ship_type_caravel'):
            block = block.replace('ship_group_cruisers', 'ship_group_capital_ships')
        elif block.startswith('ship_type_galley'):
            block = block.replace('ship_group_capital_ships', 'ship_group_cruisers')
            block = block.replace('ship_blockade_strength_add = 50', 'ship_blockade_strength_add = 50\n        ship_max_distance_to_port_add = 1')
            block = block.replace('    construction_goods = {', '    distance_to_port_modifier = {\n        ship_hull_damage_mult = -0.8\n        ship_crew_damage_mult = -0.8\n    }\n    construction_goods = {')
        return block
    return re.sub(r'(?ms)^ship_type_\w+ = \{.*?^\}', transform, raw)

def prepare():
    CACHE.mkdir(parents=True, exist_ok=True)
    baseline = CACHE/'baseline.json'
    assert not baseline.exists(), 'Do not overwrite the before-state'
    original, reference = colour.decode(ROOT/SOURCE), colour.decode(REFERENCE)
    assert colour.digest(ROOT/SOURCE) == '3e5ea7d5583fac00a8ac9c69b836ba8fdcdc6211e41333308f503ad3a8ba2570'
    assert colour.digest(REFERENCE) == '963b57e470852576777a011fd3e5fe05e8824f2f4fad5229c1d3ade884e8dfc0'
    old, target = colour.colour_measure(original), colour.colour_measure(reference)
    delta = target['hue_degrees'] - old['hue_degrees']
    scale = target['saturation']/old['saturation']
    candidate = colour.recolour(original, delta, scale)
    candidate.save(CACHE/'caravel_capital_yellow.png')
    captured = {'runtime': colour.runtime_hashes(), 'texts': {p:(ROOT/p).read_text(encoding='utf-8-sig') for p in (SHIP,FR,EN)}, 'registry':json.loads((ROOT/'docs/reports/assets/source_registry.json').read_text()),
                'source':SOURCE,'source_sha256':colour.digest(ROOT/SOURCE),'reference':str(REFERENCE),'reference_sha256':colour.digest(REFERENCE),'reference_palette':target,
                'hue_delta_degrees':delta,'saturation_scale':scale,'candidate_sha256':colour.digest(CACHE/'caravel_capital_yellow.png')}
    baseline.write_text(json.dumps(captured, indent=2), encoding='utf-8')
    sheet = Image.new('RGB', (780, 230), '#24282d')
    draw = ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
    for index,(label,im) in enumerate([('Avant : orange',original),('Caravelle : jaune capital',candidate),('Référence : vaisseau de ligne',reference)]):
        im=im.copy();im.thumbnail((240,160),Image.Resampling.LANCZOS)
        sheet.paste(im,(index*260+(260-im.width)//2,45+(160-im.height)//2),im)
        draw.text((index*260+10,12),label,font=font,fill='white')
    sheet.save(CACHE/'colour_comparison.png')
    print(json.dumps({k:v for k,v in captured.items() if k not in ('runtime','texts','registry')}))

def check():
    baseline=json.loads((CACHE/'baseline.json').read_text())
    current=colour.runtime_hashes();allowed={SHIP,DDS}
    assert not [p for p in set(current)|set(baseline['runtime']) if p not in allowed and current.get(p)!=baseline['runtime'].get(p)], 'Unrelated runtime change'
    assert bindings.normal((ROOT/SHIP).read_text()) == bindings.normal(expected_roles(baseline['texts'][SHIP])), 'Unexpected ship balance/content change'
    descriptions = {
        FR: [("Un navire de guerre à voile économique, à équipage réduit et armement léger, précédant la frégate.", "Un navire capital à voile économique et à équipage réduit, destiné à la projection de puissance et précédant le vaisseau de ligne."),
             ("Une alternative de navire principal moins coûteuse et moins puissante que le vaisseau de ligne.", "Un croiseur de défense côtière primitif, peu coûteux et moins puissant que ses successeurs. Son efficacité au combat chute lorsqu'il s'éloigne des ports.")],
        EN: [("An economical sailing warship with a small crew and light armament, preceding the frigate.", "An economical sailing capital ship with a small crew, intended for power projection and preceding the ship of the line."),
             ("A cheaper, weaker capital ship alternative to a ship of the line.", "An inexpensive primitive coastal-defense cruiser, weaker than its successors. Its combat effectiveness falls sharply when operating far from ports.")],
    }
    for path, changes in descriptions.items():
        expected = baseline['texts'][path]
        for old, new in changes: expected = expected.replace(old, new)
        assert (ROOT/path).read_text(encoding='utf-8-sig') == expected, 'Unexpected localisation change'
    methods=art.catalog('common/ship_types')
    galley=methods['ship_type_galley'][0];caravel=methods['ship_type_caravel'][0]
    assert art.field(galley,'ship_group')=='ship_group_cruisers'
    assert art.field(caravel,'ship_group')=='ship_group_capital_ships'
    registry=json.loads((ROOT/'docs/reports/assets/source_registry.json').read_text())
    before={e['dds']:e for e in baseline['registry']['entries']};after={e['dds']:e for e in registry['entries']}
    assert before.keys()==after.keys()
    assert all(before[p]==after[p] for p in before if p!=DDS), 'Unrelated asset recipe change'
    entry=after[DDS];manifest=json.loads((ROOT/MANIFEST).read_text())
    assert entry==manifest['entry']
    assert colour.digest(ROOT/SOURCE)==baseline['source_sha256']
    assert colour.digest(REFERENCE)==baseline['reference_sha256']
    assert colour.digest(ROOT/entry['source'])==entry['source_sha256']==baseline['candidate_sha256']
    original,final=colour.decode(ROOT/SOURCE),colour.decode(ROOT/entry['source'])
    assert final.tobytes()==colour.recolour(original,baseline['hue_delta_degrees'],baseline['saturation_scale']).tobytes()
    assert colour.digest(ROOT/DDS)==entry['dds_sha256']
    header=art.header(ROOT/DDS)
    assert (header['width'],header['height'],header['mips'])==(240,160,8)
    assert manifest['roles_only_integrated'] is True and manifest['options_and_technology_status']=='PROPOSED_NOT_INTEGRATED'
    result={'status':'PASS_STATIC_EARLY_SHIP_ROLES','capital_caravel':True,'coastal_cruiser_galley':True,'galley_distance_to_port':1,'outside_range_damage_multiplier':0.2,
            'base_combat_and_economic_stats_unchanged':True,'caravel_original_master_preserved':True,'colour_only':True,'technology_and_fleet_files_unchanged':True,'registered_exports':len(after),'protected_runtime_files':len(set(current)-allowed),'engine_tested':False}
    (CACHE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))

if __name__=='__main__':
    parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group(required=True);mode.add_argument('--prepare',action='store_true');mode.add_argument('--check',action='store_true');args=parser.parse_args()
    prepare() if args.prepare else check()
