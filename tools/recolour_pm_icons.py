"""Preview-only, deterministic PM recolouring. Never generates or installs art.

Only hue and saturation change; dimensions, alpha and HSV value are preserved.
Sources (including installed vanilla) are read-only. Outputs belong in the
ignored .asset-cache. A fixed manifest records inputs and colour parameters.
"""
import argparse
import colorsys
import hashlib
import json
import struct
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_hashes():
    return {path.relative_to(ROOT).as_posix(): digest(path)
            for folder in ("common", "gfx", "gui")
            for path in (ROOT / folder).rglob("*") if path.is_file()}


def decode(path):
    data = bytearray(path.read_bytes())
    if data[:4] == b"DDS " and data[84:88] == b"DX10":
        dxgi = struct.unpack_from("<I", data, 128)[0]
        if dxgi in (87, 91):
            height, width = struct.unpack_from("<II", data, 12)
            return Image.frombytes("RGBA", (width, height),
                                   bytes(data[148:148 + width * height * 4]),
                                   "raw", "BGRA")
        aliases = {99: 98, 72: 71, 75: 74, 78: 77, 29: 28}
        if dxgi in aliases:
            struct.pack_into("<I", data, 128, aliases[dxgi])
    return Image.open(BytesIO(data)).convert("RGBA")


def colour_measure(image):
    samples = []
    for red, green, blue, alpha in image.get_flattened_data():
        hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        if alpha >= 160 and value >= 0.25 and saturation >= 0.18:
            samples.append((hue, saturation, value * alpha / 255))
    assert samples, "Source has no measurable coloured field"
    weight = sum(row[2] for row in samples)
    # These PMs each have a single non-wrapping field palette.
    return {"hue_degrees": sum(h * w for h, _, w in samples) / weight * 360,
            "saturation": sum(s * w for _, s, w in samples) / weight}


def recolour(source, hue_delta, saturation_scale, saturation_floor=0,
             achromatic_hue_degrees=None):
    pixels = []
    for red, green, blue, alpha in source.get_flattened_data():
        if alpha == 0:
            pixels.append((red, green, blue, alpha))
            continue
        hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        output_hue = ((achromatic_hue_degrees / 360) % 1
                      if achromatic_hue_degrees is not None and saturation < 0.18
                      else (hue + hue_delta / 360) % 1)
        rgb = colorsys.hsv_to_rgb(output_hue,
                                 min(1, max(saturation_floor, saturation * saturation_scale)), value)
        pixels.append(tuple(round(channel * 255) for channel in rgb) + (alpha,))
    result = Image.new("RGBA", source.size)
    result.putdata(pixels)
    assert result.size == source.size
    assert result.getchannel("A").tobytes() == source.getchannel("A").tobytes()
    assert all(max(before[:3]) == max(after[:3])
               for before, after in zip(source.get_flattened_data(), result.get_flattened_data()))
    return result


def contact_sheet(config, originals, candidates, target):
    sheet = Image.new("RGB", (350 * len(config["candidates"]), 650), "#292b2e")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
    small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    for index, entry in enumerate(config["candidates"]):
        left = index * 350
        draw.text((left + 12, 12), entry["label"], fill="#eee8db", font=font)
        for row, im in enumerate((originals[index], candidates[index])):
            y = 60 + row * 225
            display = im.copy()
            display.thumbnail((168, 168), Image.Resampling.LANCZOS)
            sheet.paste(display, (left + (350 - display.width) // 2, y), display)
            draw.text((left + 12, y + 175), "Avant" if row == 0 else config.get("colour_label", "Couleur violette uniquement"),
                      fill="#eee8db", font=small)
        for bg_index, background in enumerate(("#292b2e", "#d8d1c5")):
            y = 495 + bg_index * 65
            draw.rectangle((left + 12, y, left + 337, y + 62), fill=background)
            for size_index, size in enumerate((32, 48, 64)):
                im = candidates[index].resize((size, size), Image.Resampling.LANCZOS)
                sheet.paste(im, (left + 48 + 95 * size_index, y), im)
    draw.text((12, 628), config.get("sheet_footer", "Proposition non intégrée — dessins et alpha inchangés — aucune génération IA"),
              fill="#eee8db", font=small)
    sheet.save(target)

def check_integration(manifest_path):
    """Check approved colour-only installation; never write runtime files."""
    import audit_pm_group_palette as art
    import preview_pm_group_bindings as bindings
    config = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert config['status'] == 'APPROVED_AND_INTEGRATED'
    baseline = json.loads((ROOT/config['qa']['runtime_baseline']).read_text())
    files = json.loads((ROOT/config['qa']['pm_baseline']).read_text())
    registry_before = json.loads((ROOT/config['qa']['registry_baseline']).read_text())
    registry = json.loads((ROOT/'docs/reports/assets/source_registry.json').read_text())
    entries = {e['dds']:e for e in registry['entries']}
    assert len(entries) == len(registry['entries']), 'Duplicate registered DDS'
    approved = {item['entry']['dds'] for item in config['candidates']}
    assert set(entries) == {e['dds'] for e in registry_before['entries']} | approved
    for entry in registry_before['entries']:
        if entry['dds'] not in approved:
            assert entries[entry['dds']] == entry, 'Unrelated registry entry changed'
    methods = art.catalog('common/production_methods')
    for path,raw in files.items():
        edits = [{'id':item['id'],'texture':item['entry']['dds']} for item in config['candidates'] if item['file']==path]
        assert bindings.normal((ROOT/path).read_text(encoding='utf-8-sig')) == bindings.normal(bindings.expected_file(raw,edits)), 'Non-visual PM change: '+path
    for item in config['candidates']:
        entry = item['entry']
        assert entries[entry['dds']] == entry
        assert art.art.field(methods[item['id']][0],'texture') == entry['dds']
        source = Path(item['source'])
        if not source.is_absolute(): source = ROOT/source
        assert digest(source) == item['source_sha256']
        master = ROOT/entry['source'];dds = ROOT/entry['dds']
        assert digest(master) == entry['source_sha256']
        assert digest(dds) == entry['dds_sha256']
        original,final = decode(source),decode(master)
        assert original.size == final.size
        assert original.getchannel('A').tobytes() == final.getchannel('A').tobytes()
        expected = recolour(original, item['hue_delta_degrees'], item['saturation_scale'],
                            item.get('saturation_floor', 0), item.get('achromatic_hue_degrees'))
        assert final.tobytes() == expected.tobytes(), 'Master is not the recorded colour-only transform'
        def value(im):
            red,green,blue,_ = im.split()
            return ImageChops.lighter(ImageChops.lighter(red,green),blue).tobytes()
        assert value(original) == value(final), 'HSV value changed'
        assert decode(dds).tobytes() == final.tobytes(), 'DDS top mip differs from the colour-only master'
        header = art.art.header(dds)
        assert (header['width'],header['height'],header['mips']) == (entry['size'],entry['size'],entry['mips'])
        assert art.palette(dds).get(item['palette'],0)>.8
    allowed = set(files) | approved
    current = runtime_hashes()
    assert not [p for p in set(baseline)|set(current) if p not in allowed and baseline.get(p)!=current.get(p)], 'Unrelated runtime change'
    report = {'status':'PASS_COLOUR_ONLY_INTEGRATION','batch':config['batch'],'approved_assets':len(approved),
              'recipes_unchanged':True,'groups_unchanged':True,'alpha_and_value_unchanged':True,
              'protected_runtime_files':len(set(baseline)-allowed),'generated':False,'engine_tested':False}
    ((ROOT/config['qa']['runtime_baseline']).parent/'integration_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--check-integration", action="store_true")
    parser.add_argument("--snapshot", action="store_true", help="Record machine-generated integration baselines in the ignored preview cache")
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    if args.check_integration:
        check_integration(manifest_path)
        return
    out = manifest_path.parent
    assert out.is_relative_to(ROOT / ".asset-cache"), "Preview output must remain in ignored cache"
    config = json.loads(manifest_path.read_text(encoding="utf-8"))
    baseline = runtime_hashes()
    if args.snapshot:
        assert not args.inspect, 'Inspection must not replace integration baselines'
        snapshots = {
            'integration_baseline.json': baseline,
            'integration_pm_baseline.json': {entry['file']: (ROOT/entry['file']).read_text(encoding='utf-8-sig') for entry in config['candidates']},
            'integration_registry_baseline.json': json.loads((ROOT/'docs/reports/assets/source_registry.json').read_text()),
        }
        for name, contents in snapshots.items():
            destination = out/name
            assert not destination.exists(), 'Refusing to overwrite an existing integration baseline'
            destination.write_text(json.dumps(contents, indent=2), encoding='utf-8')
    originals = []
    outputs = []
    metrics = []
    for entry in config["candidates"]:
        path = Path(entry["source"])
        assert digest(path) == entry["source_sha256"], "Source changed since proposal"
        original = decode(path)
        originals.append(original)
        if args.inspect:
            candidate = original
        else:
            candidate = recolour(original, entry["hue_delta_degrees"], entry["saturation_scale"],
                                 entry.get("saturation_floor", 0), entry.get("achromatic_hue_degrees"))
            target = out / (entry["id"] + ".png")
            candidate.save(target)
        outputs.append(candidate)
        metrics.append({"id": entry["id"], "dimensions": list(original.size),
                        "source_palette": colour_measure(original),
                        "candidate_palette": colour_measure(candidate),
                        "alpha_identical": candidate.getchannel("A").tobytes() == original.getchannel("A").tobytes(),
                        "value_identical": all(max(a[:3]) == max(b[:3]) for a, b in
                                               zip(original.get_flattened_data(), candidate.get_flattened_data())),
                        "source_signature": path.read_bytes()[:8].hex(),
                        "candidate_sha256": None if args.inspect else digest(target)})
    assert len(originals) == 3 or (config.get('final_harmonisation') is True and len(originals) == 2), "PM proposals use batches of three; the explicitly requested final harmonisation contains two remaining icons"
    contact_sheet(config, originals, outputs, out / ("inspection.png" if args.inspect else f"lot_{config.get('batch',6)}.png"))
    assert baseline == runtime_hashes(), "Runtime changed during preview"
    report = {"status": "READ_ONLY_INSPECTION" if args.inspect else "PASS_COLOUR_ONLY_PREVIEW",
              "generated": False, "runtime_unchanged": True, "engine_tested": False,
              "candidates": metrics}
    if not args.inspect:
        (out / "validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
