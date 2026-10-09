#!/usr/bin/env python3
"""Reuse existing PMG arrows: cache-only previews and scoped integration checks.

Never draws an asset, recolours a source, writes runtime files or invokes AI.
The contact sheet displays existing textures at native and UI sizes. Previews
use three bindings; an explicit all-groups approval may integrate a larger set.
All unrelated runtime files are protected by hashes.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import audit_pm_group_palette as palette
import build_start_1776_world_apply as world
import recolour_pm_icons as colour

ROOT = world.ROOT
palette.art.GAME = world.VANILLA

def normal(raw):
    return re.sub(r'\s+', '', world.catalog_tools.clean_comments(raw))

def expected_file(raw, bindings):
    changes = []
    for item in bindings:
        spans = world.block_spans(raw, r'(?:REPLACE_OR_CREATE:)?'+re.escape(item['id']), 0)
        if len(spans) != 1:
            raise ValueError('Group does not resolve once: '+item['id'])
        _,a,b = spans[0]
        body = raw[a:b]
        texture = f'texture = "{item["texture"]}"'
        if re.search(r'\btexture\s*=', body):
            body = re.sub(r'\btexture\s*=\s*"[^"]*"', texture, body, count=1)
        else:
            at = body.index('{')+1
            body = body[:at]+'\n    '+texture+body[at:]
        changes.append((a,b,body))
    for a,b,body in sorted(changes,reverse=True):
        raw = raw[:a]+body+raw[b:]
    return raw

def check_coverage(config, groups=None):
    """Validate the approved shared arrows without requiring transient snapshots."""
    assert config['status'] == 'APPROVED_AND_INTEGRATED'
    groups = groups or palette.catalog('common/production_method_groups')
    rules = json.loads((ROOT/'docs/reports/assets/pm_palette_rules.json').read_text())
    variants = rules['group_arrow_policy']['variants']
    local_count, decoded = 0, {}
    for key,(tokens,source) in groups.items():
        if not source.is_relative_to(ROOT):
            continue
        texture = palette.art.field(tokens,'texture')
        family = (rules['group_overrides'].get(key) or
                  next((v for prefix,v in rules['group_prefixes'].items() if key.startswith(prefix)),None) or
                  rules['native_group_textures'].get(Path(texture).name))
        assert family in variants, 'Unknown group colour: '+key
        assert texture == variants[family], 'Unexpected group arrow: '+key
        if texture not in decoded:
            resolved = palette.art.resolve(texture)
            assert resolved and colour.digest(resolved) == config['arrow_textures'][texture], 'Shared arrow changed: '+texture
            im = colour.decode(resolved)
            assert im.getchannel('A').getbbox(), 'Invisible arrow: '+texture
            decoded[texture] = palette.palette(resolved)
        assert decoded[texture].get(rules['families'][family]['palette'],0)>0.8, 'Wrong group colour: '+key
        local_count += 1
    assert local_count == config['local_groups_checked'], 'Local group inventory changed'
    buildings = palette.catalog('common/buildings')
    used = {key for tokens,_ in buildings.values()
            for key in palette.art.field(tokens,'production_method_groups',[])}
    for key in used:
        assert key in groups, 'Missing used group: '+key
        texture = palette.art.field(groups[key][0],'texture')
        if key == 'pmg_dummy':
            # Native city-hub helper, explicitly documented as non-gameplay.
            assert groups[key][1] == world.VANILLA/'common/production_method_groups/00_dummy.txt'
            assert not texture and palette.art.field(groups[key][0],'production_methods',[]) == ['pm_dummy']
            continue
        assert texture and 'error_' not in texture and palette.art.resolve(texture), 'Missing/placeholder used group: '+key
    return {'local_groups_checked':local_count,'active_groups_checked':len(used),
            'visible_active_groups_checked':len(used)-int('pmg_dummy' in used),
            'native_nonvisual_helpers':['pmg_dummy'] if 'pmg_dummy' in used else [],
            'shared_arrow_textures':len(decoded),'group_placeholders':0,'groups_without_texture':0}

def check(manifest_path):
    config = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert config['status'] == 'APPROVED_AND_INTEGRATED'
    baseline = json.loads((ROOT/config['qa']['runtime_baseline']).read_text())
    group_before = json.loads((ROOT/config['qa']['group_baseline']).read_text())
    allowed = set(group_before)
    exports = config.get('shared_exports', [])
    if config.get('shared_export'):
        exports = exports + [config['shared_export']]
    for export in exports:
        allowed.add(export['dds'])
        assert colour.digest(ROOT/export['source']) == export['source_sha256']
        assert colour.digest(ROOT/export['dds']) == export['dds_sha256']
        native = Path(export['native_source'])
        assert colour.digest(native) == export['native_source_sha256']
        # Reproduce the approved hue shift in memory; never edit either image.
        original = colour.decode(native)
        master = colour.decode(ROOT/export['source'])
        recomputed = colour.recolour(original,export['hue_delta_degrees'],export['saturation_scale'])
        assert master.size == original.size and master.tobytes() == recomputed.tobytes()
        header = palette.art.header(ROOT/export['dds'])
        assert (header['width'],header['height'],header['mips']) == (export['size'],export['size'],export['mips'])
    groups = palette.catalog('common/production_method_groups')
    for path,raw in group_before.items():
        expected = expected_file(raw,[b for b in config['bindings'] if b['file']==path])
        assert normal((ROOT/path).read_text(encoding='utf-8-sig')) == normal(expected), 'Unexpected group file edit: '+path
    for item in config['bindings']:
        assert palette.art.field(groups[item['id']][0],'texture') == item['texture']
        resolved = palette.art.resolve(item['texture'])
        assert resolved and palette.palette(resolved).get(item['palette'],0)>0.8
        if item.get('texture_sha256'):
            assert colour.digest(resolved) == item['texture_sha256'], 'Arrow changed: '+item['texture']
    current = colour.runtime_hashes()
    assert not [p for p in set(baseline)|set(current) if p not in allowed and baseline.get(p)!=current.get(p)], 'Unrelated runtime changed'
    report = {'status':'PASS_THREE_GROUP_INTEGRATION' if len(config['bindings']) == 3 else 'PASS_GROUP_BINDING_INTEGRATION','bindings':len(config['bindings']),
              'generated':False,'recipes_unchanged':True,'individual_pm_icons_unchanged':True,
              'protected_runtime_files':len(set(baseline)-allowed),'engine_tested':False}
    if config.get('all_local_groups'):
        report.update(check_coverage(config,groups))
    out = (ROOT/config['qa']['runtime_baseline']).parent/'integration_validation.json'
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

def preview(manifest_path):
    assert manifest_path.is_relative_to(ROOT/'.asset-cache'), 'Preview must be in ignored cache'
    out = manifest_path.parent
    config = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert config['status'] == 'PREVIEW_ONLY_AWAITING_USER_APPROVAL'
    assert len(config['candidates']) == 3
    groups = palette.catalog('common/production_method_groups')
    methods = palette.catalog('common/production_methods')
    before = colour.runtime_hashes()
    baseline = out/'runtime_baseline.json'
    assert not baseline.exists(), 'Preview baseline already exists; use a fresh revision directory'
    baseline.write_text(json.dumps(before),encoding='utf-8')
    sheet = Image.new('RGB',(1050,640),'#292b2e')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
    small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14)
    labels = {'ochre':'Jaune production','green':'Vert automatisation','purple':'Violet preparation'}
    for i,item in enumerate(config['candidates']):
        tokens,path = groups[item['id']]
        current = palette.art.field(tokens,'texture')
        assert current == item['current_texture'], 'Group binding changed: '+item['id']
        source = palette.art.resolve(item['proposed_texture'])
        assert source and colour.digest(source) == item['source_sha256']
        assert palette.palette(source).get(item['palette'],0)>0.8
        arrow = colour.decode(source)
        x = i*350
        draw.text((x+14,14),item['label'],font=font,fill='#eee8db')
        draw.text((x+14,44),labels[item['palette']],font=small,fill='#c6bead')
        if current:
            old = colour.decode(palette.art.resolve(current))
            old.thumbnail((100,100),Image.Resampling.LANCZOS)
            sheet.paste(old,(x+120,82),old)
        else:
            draw.rectangle((x+120,82,x+220,182),outline='#63676b',width=2)
            draw.text((x+129,120),'Sans image',font=small,fill='#a0a3a5')
        draw.text((x+14,193),'Actuel',font=small,fill='#eee8db')
        large = arrow.copy()
        large.thumbnail((120,120),Image.Resampling.LANCZOS)
        sheet.paste(large,(x+115,224),large)
        draw.text((x+14,347),'Double fleche existante reutilisee',font=small,fill='#eee8db')
        for row,bg in enumerate(('#292b2e','#d8d1c5')):
            y = 378+row*73
            draw.rectangle((x+12,y,x+338,y+69),fill=bg)
            for col,size in enumerate((32,48,64)):
                tiny = arrow.copy();tiny.thumbnail((size,size),Image.Resampling.LANCZOS)
                px = x+24+col*105
                sheet.paste(tiny,(px+(64-tiny.width)//2,y+(64-tiny.height)//2),tiny)
        draw.text((x+14,536),'PM du groupe, conserves :',font=small,fill='#eee8db')
        for col,pm in enumerate(palette.art.field(tokens,'production_methods',[])[:4]):
            pmt,_ = methods[pm]
            path = palette.art.resolve(palette.art.field(pmt,'texture'))
            icon = colour.decode(path);icon.thumbnail((48,48),Image.Resampling.LANCZOS)
            sheet.paste(icon,(x+22+col*78,566),icon)
    draw.text((12,620),f'LOT {config["batch"]} NON INTEGRE - fleches reutilisees ; PM et recettes inchanges ; aucune generation IA',font=small,fill='#eee8db')
    target = out/f'lot_{config["batch"]}.png'
    sheet.save(target)
    assert before == colour.runtime_hashes(), 'Runtime changed during preview'
    report = {'status':'PASS_THREE_EXISTING_GROUP_ARROW_PREVIEW','runtime_modified':False,
              'candidate_count':3,'generated':False,'new_dds':0,'engine_tested':False,'preview':str(target)}
    (out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--check-integration',action='store_true')
    parser.add_argument('--check-coverage',action='store_true')
    args = parser.parse_args()
    if args.check_coverage:
        config = json.loads(args.manifest.read_text(encoding='utf-8'))
        print(json.dumps({'status':'PASS_GROUP_ARROW_COVERAGE',**check_coverage(config),'engine_tested':False}))
    elif args.check_integration: check(args.manifest.resolve())
    else: preview(args.manifest.resolve())
