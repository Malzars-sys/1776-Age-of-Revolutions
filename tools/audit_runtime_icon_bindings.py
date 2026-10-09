"""Audit actual icon bindings, including inline goods glyphs and all local PMs.

Read-only by default. --patch emits an apply_patch-compatible repair, never
edits gameplay. --snapshot records small provenance/baseline data (no previews).
Use --check --baseline <snapshot> after applying to verify non-visual identity.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re

import asset4_style_reference_audit as art

ROOT = art.ROOT
PM_DIR = 'gfx/interface/icons/production_method_icons/'
EXACT_PM_ICONS = {
    'default_building_salt_pan': '1776_salt_pan_pm',
    'pm_spice_cultivation': '1776_spice_cultivation_pm',
    'pm_mechanized_spice_cultivation': '1776_mechanized_spice_cultivation_pm',
    'pm_no_explosives_production': 'no_explosives',
    'pm_leblanc_process': '1776_black_powder_pm',
    'pm_ammonia-soda_process': 'nitroglycerin',
    'pm_vacuum_evaporation': 'dynamite',
    'pm_brine_electrolysis': 'vaccum_brine_electrolysis',
    'pm_coke_blast_furnaces': '1776_coke_blast_furnaces_pm',
    'pm_blister_steel_process': '1776_puddling_and_rolling_pm',
    'pm_thomas_process': '1776_thomas_process_pm',
    'pm_no_rail_network': 'no_rail_transport',
    'pm_early_trains': '1776_experimental_locomotive_green',
    'pm_steam_trains': '1776_steam_locomotive_green',
    'pm_steam_trains_principle_transport_3': '1776_steam_locomotive_green',
    'pm_electric_trains': '1776_electric_locomotive_green',
    'pm_electric_trains_principle_transport_3': '1776_electric_locomotive_green',
    'pm_diesel_trains': '1776_diesel_locomotive_green',
    'pm_diesel_trains_principle_transport_3': '1776_diesel_locomotive_green',
    'pm_natural_cement_process': '1776_natural_cement_process',
    'pm_hydraulic_cement_process': '1776_hydraulic_cement_process',
    'pm_portland_cement_process': '1776_portland_cement_process',
    'pm_chemical_bleaching_textile_mill': '1776_textile_bleaching',
    'pm_solvay_process_building_chemical_works': '1776_solvay_process',
    'pm_all_metal_aircraft': '1776_all_metal_aircraft_yellow',
    'pm_aluminium_housewares': '1776_aluminium_housewares_yellow',
    'pm_aluminium_conductors_building_power_plant': 'electric_streetlights',
    'pm_wohler_deville_process': '1776_wohler_deville_process',
    'pm_no_precision_machinery': '1776_no_precision_machinery_purple',
    'pm_precision_machine_tools': '1776_precision_machine_tools',
    'pm_electrical_precision_machinery': '1776_electrical_precision_machinery',
    'pm_no_salt_processing_building_salt_mine': '1776_manual_ore_sorting',
    'pm_salt_purification_building_salt_mine': '1776_salt_purification',
    'pm_no_organized_medical_supply': 'no_pharmaceuticals',
    'pm_confessional_hospitals': '1776_confessional_hospitals',
    'pm_private_pharmacies': '1776_private_pharmacies',
    'pm_public_health_services': '1776_public_health_services',
    'pm_pressed_glass': '1776_pressed_glass_pm',
    'pm_no_mine_ventilation': 'disabled',
    'pm_steam_mine_ventilation': '1776_steam_mine_ventilation',
    'pm_electric_mine_ventilation': '1776_electric_mine_ventilation',
    'pm_cylinder_flour_milling': '1776_cylinder_flour_milling',
    'pm_no_scientific_management': 'no_org',
    'pm_scientific_management': '1776_scientific_management',
    'pm_scientific_management_automotive_industry': '1776_scientific_management',
    'pm_scientific_management_electrics_industry': '1776_scientific_management',
    'pm_tabulating_offices': 'census',
    'pm_no_printing_services': 'disabled',
    'pm_mechanized_typesetting': 'printing_presses',
    'pm_rotary_press': 'newspapers',
    'pm_no_canal_network': 'disabled',
    'pm_industrial_canals': '1776_industrial_canals_pm',
    'pm_engineered_canals': '1776_engineered_canals_pm',
}


def excluded(key, path):
    # Consumer methods outside the copper-specific chain remain in scope.
    return 'copper' in key or 'copper' in path.name


def pm_icon(key):
    name = EXACT_PM_ICONS.get(key)
    if key.startswith('pm_no_ore_concentration_building_'):
        name = '1776_manual_ore_sorting'
    elif key.startswith('pm_ore_concentration_building_'):
        name = '1776_ore_concentration'
    elif key.startswith('pm_steam_mine_ventilation_building_'):
        name = '1776_steam_mine_ventilation'
    elif key.startswith('pm_electric_mine_ventilation_building_'):
        name = '1776_electric_mine_ventilation'
    elif key.startswith('pm_vapor_compression_refrigeration_building_'):
        name = 'refrigerated_storage'
    elif key.startswith('pm_unit_electric_drive_building_'):
        name = '1776_unit_electric_drive'
    elif key.startswith('field_drainage_building_') or key == 'pm_field_drainage_spice_cultivation':
        name = 'maintained_sewers'
    if name is None:
        raise ValueError('PM requires semantic review: ' + key)
    # Some shipped native symbols are under unused/, but still loadable assets.
    for relative in (PM_DIR + name + '.dds', PM_DIR + 'unused/' + name + '.dds'):
        if art.resolve(relative):
            return relative
    raise FileNotFoundError(name)


def tokens_digest(tokens, ignore_texture=False):
    tokens = list(tokens)
    if ignore_texture:
        for i in range(len(tokens)-2):
            if tokens[i] in ('texture', 'icon') and tokens[i+1] == '=':
                tokens[i+2] = 'ARTWORK_REFERENCE'
    return hashlib.sha256(json.dumps(tokens, separators=(',', ':')).encode()).hexdigest()


def blocks(path, name):
    """Find complete named blocks without treating comments/braces as syntax."""
    import build_start_1776_research_input_pack as history
    return history.named_blocks(path, name, 0)


def audit():
    goods = art.catalog('common/goods')
    pms = art.catalog('common/production_methods')
    fixes, excluded_pms, missing = [], [], []
    glyphs = {}
    for path in sorted((ROOT/'gui').rglob('*.gui')):
        if 'texticon' not in path.read_text(encoding='utf-8-sig'):
            continue
        for key, t in art.pairs(art.parse(path)):
            if key != 'texticon' or not isinstance(t, list):
                continue
            name = art.field(t, 'icon')
            sizes = [v for k,v in art.pairs(t) if k == 'iconsize' and isinstance(v,list)]
            glyphs.setdefault(name, []).extend((path,art.field(s,'texture')) for s in sizes)
    for name,(t,path) in goods.items():
        if not path.is_relative_to(ROOT) or excluded(name,path):
            continue
        texture = art.field(t,'texture')
        if not texture or 'error_' in texture or not art.resolve(texture):
            missing.append({'kind':'GOOD','id':name,'texture':texture})
        if name not in glyphs:
            missing.append({'kind':'TEXTICON','id':name,'texture':'NO_OVERRIDE'})
        for gui,actual in glyphs.get(name,[]):
            if actual != texture:
                fixes.append({'kind':'TEXTICON','id':name,'file':gui.relative_to(ROOT).as_posix(),
                              'before':actual,'after':texture})
    for name,(t,path) in pms.items():
        texture = art.field(t,'texture')
        if excluded(name,path):
            if 'error_' in texture:
                excluded_pms.append(name)
            continue
        if 'error_' in texture:
            fixes.append({'kind':'PM','id':name,'file':path.relative_to(ROOT).as_posix(),
                          'before':texture,'after':pm_icon(name)})
        elif texture and not art.resolve(texture):
            missing.append({'kind':'PM','id':name,'texture':texture})
    for folder,kind,visual in [('common/buildings','BUILDING','icon'),
                               ('common/technology/technologies','TECH','texture')]:
        for name,(t,path) in art.catalog(folder).items():
            if excluded(name,path) or (kind == 'TECH' and art.field(t,'can_research') == 'no'):
                continue
            texture = art.field(t,visual)
            if texture and ('error_' in texture or not art.resolve(texture)):
                missing.append({'kind':kind,'id':name,'texture':texture})
    return fixes, excluded_pms, missing, goods, pms


def patch(fixes):
    by_file = {}
    for fix in fixes:
        by_file.setdefault(fix['file'], []).append(fix)
    output = ['*** Begin Patch\n']
    for relative, changes in sorted(by_file.items()):
        path = ROOT/relative
        old = path.read_text(encoding='utf-8-sig')
        new = old
        # Replace in complete identified blocks, never a global error_* match.
        for fix in changes:
            if fix['kind'] == 'PM':
                candidates = blocks(path, re.escape(fix['id']))
            else:
                candidates = [b for b in blocks(path,'texticon')
                              if art.field([t for t in art.TOKENS.findall(b.text)
                                            if not t.startswith('#')][2:-1], 'icon') == fix['id']]
            if len(candidates) != 1:
                raise ValueError('Ambiguous binding: ' + str(fix))
            before = candidates[0].text
            after, count = re.subn(r'(\btexture\s*=\s*)"' + re.escape(fix['before']) + '"',
                                   lambda m:m[1]+'"'+fix['after']+'"', before)
            if count != 1 or new.count(before) != 1:
                raise ValueError('Ambiguous texture in ' + fix['id'])
            new = new.replace(before, after, 1)
        output.append('*** Update File: ' + str(path) + '\n')
        diff = list(difflib.unified_diff(old.splitlines(True),new.splitlines(True),n=8))
        output.extend('@@\n' if line.startswith('@@') else line for line in diff[2:])
    output.append('*** End Patch\n')
    return ''.join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path,default=Path('C:/Games/Victoria 3/game'))
    parser.add_argument('--patch',action='store_true')
    parser.add_argument('--snapshot',type=Path)
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    art.GAME = args.game.resolve()
    if not (art.GAME/'common/goods').is_dir():
        raise FileNotFoundError('Installed game directory required')
    fixes, excluded_pms, missing, goods, pms = audit()
    hashes = {f:tokens_digest(art.parse(ROOT/f), True) for f in sorted({r['file'] for r in fixes})}
    protected = {name:tokens_digest(t) for name,(t,p) in pms.items()
                 if excluded(name,p) or 'laboratory' in p.name}
    protected.update({'FILE:'+p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ROOT/'gfx/interface/icons/production_method_icons').glob('1776_laboratory*.dds')})
    protected.update({'GOOD:'+name:tokens_digest(t) for name,(t,p) in goods.items() if excluded(name,p)})
    report = {'scope':'all local goods inline glyphs and all PM icon references; copper excluded; laboratory preserved',
              'fix_count':len(fixes),'fixes':fixes,'missing':missing,'excluded_copper_pms':excluded_pms,
              'nonvisual_file_hashes':hashes,'protected_hashes':protected,'game_tested':False}
    if args.snapshot:
        path = args.snapshot.resolve()
        if not path.is_relative_to(ROOT/'docs/reports') and not path.is_relative_to(ROOT/'.asset-cache'):
            raise ValueError('Snapshot must stay in reports or asset cache')
        if path.exists():
            raise FileExistsError('Refusing to overwrite the pre-change baseline')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if args.baseline:
        baseline = json.loads(args.baseline.read_text(encoding='utf-8-sig'))
        for relative,digest in baseline['nonvisual_file_hashes'].items():
            assert tokens_digest(art.parse(ROOT/relative),True) == digest, 'Non-visual change: '+relative
        assert protected == baseline['protected_hashes'], 'Copper/laboratory changes'
        for fix in baseline['fixes']:
            assert art.resolve(fix['after']), 'Missing mapped asset: '+fix['after']
        # A valid-looking path must not conceal a copied error texture, an
        # unreadable DDS or an entirely invisible image.
        errors = {(image.size,hashlib.sha256(image.tobytes()).hexdigest())
                  for p in (art.GAME/'gfx').glob('error_*.dds')
                  for image in [art.decode(p)]}
        textures = sorted({fix['after'] for fix in baseline['fixes']})
        for texture in textures:
            path = art.resolve(texture)
            assert path.read_bytes()[:4] == b'DDS ', 'Not a DDS: '+texture
            image = art.decode(path)
            assert image.getchannel('A').getbbox(), 'Invisible texture: '+texture
            assert (image.size,hashlib.sha256(image.tobytes()).hexdigest()) not in errors, 'Copied error art: '+texture
        report['mapped_textures_decoded'] = len(textures)
        report['nonvisual_identity_verified'] = True
    if args.check:
        assert not fixes and not missing, report
    if args.patch:
        assert not missing, missing
        print(patch(fixes),end='')
    else:
        print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
