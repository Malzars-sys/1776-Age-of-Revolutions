"""Independent DDS/mipmap/color verification; protect old laboratory and gameplay."""
from io import BytesIO
import hashlib
import json
import struct
import textwrap
from PIL import Image, ImageDraw, ImageFont
from asset4_style_reference_audit import ROOT, TOKENS, field, pairs, parse
from building_dds_compat import assert_export_layout

PACK = ROOT / 'docs/reports/assets/asset8_pm_grain_revision_2026-10-03'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest = json.loads((PACK / 'integration_manifest.json').read_text(encoding='utf-8'))
    exports = json.loads((PACK / 'integration_export_validation.json').read_text(encoding='utf-8'))
    baseline = json.loads((PACK / manifest['protected_baseline']).read_text(encoding='utf-8'))
    assert len(manifest['entries']) == 10 and len(manifest['retained_laboratory']) == 7
    assert all(not e['key'].startswith('laboratory_') for e in manifest['entries'])
    assert set(manifest['approval']['approved_keys']) == {e['key'] for e in manifest['entries']}
    rows, icons = [], []
    (PACK / 'decoded_dds_png').mkdir(exist_ok=True)
    for entry in manifest['entries']:
        definitions = dict(pairs(parse(ROOT / entry['definition'])))
        assert field(definitions[entry['id']], 'texture') == entry['dds']
        assert sum(k == 'texture' for k, _ in pairs(definitions[entry['id']])) == 1
        assert sha((PACK / entry['preview']).read_bytes()) == entry['source_sha256']
        payload = (ROOT / entry['dds']).read_bytes()
        assert payload[:4] == b'DDS ' and len(payload) == 230828
        assert struct.unpack_from('<II', payload, 12) == (208, 208)
        assert struct.unpack_from('<I', payload, 28)[0] == 8
        assert_export_layout(payload, entry['dds'])
        export = next(r for r in exports['results'] if r['key'] == entry['key'])
        assert sha(payload) == export['dds_sha256']
        offset, checked = 128, []
        for mip in export['mip_hashes']:
            size = mip['size']
            native = payload[offset:offset + size*size*4]
            rgba = bytearray(native)
            rgba[0::4], rgba[2::4] = native[2::4], native[0::4]
            assert sha(rgba) == mip['rgba_sha256'], 'Native colors/alpha changed'
            offset += size*size*4
            checked.append(size)
        assert offset == len(payload) and checked == [208, 104, 52, 26, 13, 6, 3, 1]
        decoded = Image.open(BytesIO(payload)).convert('RGBA')
        expected = Image.open(PACK / export['target_png']).convert('RGBA')
        assert decoded.tobytes() == expected.tobytes(), 'Export colors differ from target PNG'
        alpha = decoded.getchannel('A')
        assert alpha.getextrema()[0] == 0 and alpha.getextrema()[1] >= 240
        assert all(alpha.getpixel(p) == 0 for p in [(0,0),(207,0),(0,207),(207,207)])
        if entry['previous_dds_sha256']:
            assert export['backup'] and sha((PACK / export['backup']).read_bytes()) == entry['previous_dds_sha256']
        decoded.save(PACK / 'decoded_dds_png' / (entry['key'] + '.png'))
        icons.append((entry, decoded))
        rows.append({'id': entry['id'], 'dds': entry['dds'], 'dimensions': [208,208], 'mip_sizes': checked,
                     'all_mip_colors_and_alpha_match': True, 'native_layout': True, 'binding_valid': True})
    for filename, previous in manifest['definition_baseline'].items():
        assert previous['sha256'] == baseline[filename]
        old = dict(pairs([t for t in TOKENS.findall(previous['text']) if not t.startswith('#')]))
        new = dict(pairs(parse(ROOT / filename)))
        for entry in manifest['entries']:
            if entry['definition'] == filename:
                assert field(old[entry['id']], 'texture') == entry['previous_texture']
                for definitions in (old, new):
                    definitions[entry['id']] = [(k,v) for k,v in pairs(definitions[entry['id']]) if k != 'texture']
        assert old == new, 'Non-visual gameplay edit'
    labs = []
    for entry in manifest['retained_laboratory']:
        assert sha((ROOT / entry['dds']).read_bytes()) == entry['sha256'], 'Laboratory artwork changed'
        for binding in entry['bindings']:
            assert sha((ROOT / binding['file']).read_bytes()) == baseline[binding['file']], 'Laboratory methods changed'
            definitions = dict(pairs(parse(ROOT / binding['file'])))
            assert field(definitions[binding['id']], 'texture') == entry['dds']
        labs.append({'key': entry['key'], 'dds_unchanged': True, 'binding_unchanged': True})
    changed = {p for p,h in baseline.items() if not (ROOT / p).is_file() or sha((ROOT / p).read_bytes()) != h}
    changed_dds = {e['dds'] for e in manifest['entries'] if e['previous_dds_sha256']}
    changed_definitions = {e['definition'] for e in manifest['entries'] if e['previous_texture'] != e['dds']}
    assert changed == changed_dds | changed_definitions, 'Unexpected protected file change'
    current = {p.relative_to(ROOT).as_posix() for d in ['common','gfx'] for p in (ROOT/d).rglob('*') if p.is_file()}
    added = current - baseline.keys()
    assert added == {e['dds'] for e in manifest['entries'] if not e['previous_dds_sha256']}
    untouched = json.loads((PACK / 'untouched_other_assets.json').read_text(encoding='utf-8'))
    assert sha((PACK / untouched['technology_preview']).read_bytes()) == untouched['technology_preview_sha256']
    assert sha((ROOT / untouched['building_file']).read_bytes()) == untouched['building_file_sha256']
    sheet = Image.new('RGB', (1020,1210), '#223337')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
    draw.text((12,10), '10 PM intégrés — DDS décodés — laboratoire conservé sans changement', font=font, fill='#eee5d4')
    for i,(entry,icon) in enumerate(icons):
        x, y = (i%3)*340, 60+(i//3)*285
        for line_index, line in enumerate(textwrap.wrap(entry['label'], width=33)):
            draw.text((x+10,y+line_index*21), line, font=font, fill='#eee5d4')
        for dx,bg in [(12,'#15252a'),(176,'#d8d1c1')]:
            thumb = icon.resize((150,150),Image.Resampling.LANCZOS)
            tile = Image.new('RGB',(150,150),bg)
            tile.paste(thumb,(0,0),thumb)
            sheet.paste(tile,(x+dx,y+50))
        for j,size in enumerate([32,48,64]):
            thumb = icon.resize((size,size),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(x+18+j*100,y+211),thumb)
    sheet.save(PACK / 'DIX_PM_DDS_INTEGRES_QA.png')
    report = {'status': 'PASS_TEN_INTEGRATED_PM_LABORATORY_RETAINED', 'integrated_count': 10,
              'retained_laboratory_count': 7, 'gameplay_unchanged': True,
              'changed_definition_files': sorted(changed_definitions), 'replaced_dds_files': sorted(changed_dds),
              'new_dds_files': sorted(added), 'other_protected_files_unchanged': len(baseline)-len(changed),
              'native_building_unchanged': True, 'technology_unchanged': True,
              'game_tested': False, 'assets': rows, 'retained_laboratory': labs}
    (PACK / 'integration_static_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    manifest['status'] = 'TEN_PM_INTEGRATED_STATICALLY_VALIDATED_SEVEN_LABORATORY_RETAINED'
    (PACK / 'integration_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
