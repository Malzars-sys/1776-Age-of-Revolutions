"""Independent DDS decode, visual-only AST comparison and whole common/gfx protection checks."""
from io import BytesIO
import hashlib
import json
import struct
import sys
from PIL import Image, ImageDraw, ImageFont
from asset4_style_reference_audit import ROOT, TOKENS, field, pairs, parse
from building_dds_compat import assert_export_layout, matches_export_hash

PACK = ROOT / "docs/reports/assets/asset6_preview_2026-10-02"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    args = sys.argv[1:]
    if args not in ([], ["--assets-only"]):
        raise SystemExit("Usage: validate_asset6_approved_icons.py [--assets-only]")
    manifest = json.loads((PACK / "integration_manifest.json").read_text(encoding="utf-8"))
    exports = json.loads((PACK / "integration_export_validation.json").read_text(encoding="utf-8"))
    baseline = json.loads((PACK / manifest["protected_baseline"]).read_text(encoding="utf-8"))
    assert manifest["approval"]["approved"] and len(manifest["entries"]) in (5, 6)
    refinery_integrated = len(manifest["entries"]) == 6
    if refinery_integrated:
        assert manifest["approval"]["refinery"]["approved"]
    decoded_icons, rows = [], []
    for entry in manifest["entries"]:
        definition = dict(pairs(parse(ROOT / entry["definition"])))
        assert field(definition[entry["id"]], entry["field"]) == entry["dds"]
        assert sum(k == entry["field"] for k, _ in pairs(definition[entry["id"]])) == 1
        source = (PACK / entry["preview"]).read_bytes()
        assert sha(source) == entry["source_sha256"], "Source changed"
        payload = (ROOT / entry["dds"]).read_bytes()
        assert payload[:4] == b"DDS "
        height, width = struct.unpack_from("<II", payload, 12)
        mips = struct.unpack_from("<I", payload, 28)[0]
        assert (height, width, mips) == (entry["size"], entry["size"], entry["mips"])
        assert struct.unpack_from("<II", payload, 76) == (32, 0x41)
        assert_export_layout(payload, entry["dds"])
        offset, size, mip_sizes = 128, width, []
        for _ in range(mips):
            assert len(payload[offset:offset + size * size * 4]) == size * size * 4
            offset += size * size * 4
            mip_sizes.append(size)
            size = max(1, size // 2)
        assert offset == len(payload) and mip_sizes[-1] == 1
        decoded = Image.open(BytesIO(payload)).convert("RGBA")
        export = next(row for row in exports["results"] if row["key"] == entry["key"])
        expected = Image.open(PACK / export["target_png"]).convert("RGBA")
        assert decoded.tobytes() == expected.tobytes() and matches_export_hash(payload, export["dds_sha256"], entry["dds"])
        alpha = decoded.getchannel("A")
        assert alpha.getextrema()[0] == 0 and alpha.getextrema()[1] >= 240
        assert all(alpha.getpixel(p) == 0 for p in [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)])
        if entry["key"] == "oil_refinery":
            assert entry["opacity_note_accepted"] is True
            assert alpha.crop((width*15//100, height*15//100, width*85//100, height*85//100)).getextrema()[0] >= 240, "Unexpected transparent holes in refinery"
        if entry["key"] == "thermal_catalytic_cracking_refinery":
            # Probe clear interior, not the antialiased arch edge after reduction.
            for x, y in [(.30, .70), (.49, .72), (.35, .67)]:
                assert alpha.getpixel((int(x*width), int(y*height))) == 0, "DDS furnace hole not transparent"
            for x, y in [(.407, .729), (.45, .833), (.40, .45), (.88, .80)]:
                assert alpha.getpixel((int(x*width), int(y*height))) >= 240, "Gold subject lost"
        rows.append({"id": entry["id"], "dds": entry["dds"], "sha256": sha(payload), "dimensions": [width, height], "mip_sizes": mip_sizes, "binding_and_decode_valid": True})
        decoded_icons.append((entry, decoded))

    if args == ["--assets-only"]:
        # Preserve the historical lot-wide baseline; the color migration has its own snapshot.
        report = {"status": "PASS_CURRENT_ASSET_BINDINGS_AND_NATIVE_DDS", "assets": rows,
                  "historic_batch_baseline_checked": False, "game_tested": False,
                  "source_alpha_preserved": True, "transparent_furnace_opening_verified": True}
        (PACK / "current_asset_color_validation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return

    # Ignore only requested visual fields; all logical gameplay values must match.
    for filename, old_file in manifest["definition_baseline"].items():
        assert old_file["sha256"] == baseline[filename]
        old = dict(pairs([t for t in TOKENS.findall(old_file["text"]) if not t.startswith("#")]))
        new = dict(pairs(parse(ROOT / filename)))
        for entry in manifest["entries"]:
            if entry["definition"] == filename:
                for definitions in (old, new):
                    definitions[entry["id"]] = [(k, v) for k, v in pairs(definitions[entry["id"]]) if k != entry["field"]]
        assert old == new, "Non-visual change: " + filename

    allowed_changed = set(manifest.get("stage_allowed_changed", manifest["definition_baseline"]))
    allowed_added = {entry["dds"] for entry in manifest["entries"] if entry["dds"] not in baseline}
    changed = []
    for relative, digest in baseline.items():
        assert (ROOT / relative).is_file(), "Protected file removed: " + relative
        if sha((ROOT / relative).read_bytes()) != digest:
            assert relative in allowed_changed, "Unrelated file changed: " + relative
            changed.append(relative)
    current = {p.relative_to(ROOT).as_posix() for folder in ["common", "gfx"] for p in (ROOT / folder).rglob("*") if p.is_file()}
    added = current - baseline.keys()
    assert added == allowed_added and set(changed) == allowed_changed
    if not refinery_integrated:
        refinery_file = "common/buildings/12_tech6c4_oil_refinery.txt"
        assert sha((ROOT / refinery_file).read_bytes()) == baseline[refinery_file]
        assert not (ROOT / "gfx/interface/icons/building_icons/1776_oil_refinery.dds").exists()

    # Contact sheet is layout of independently decoded exports; source artwork is never edited.
    sheet = Image.new("RGB", (1080, 760), "#22282b")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    for i, (entry, icon) in enumerate(decoded_icons):
        x, y = i % 3 * 360, i // 3 * 380
        label = entry["label"]
        if entry["key"] == "thermal_catalytic_cracking_refinery":
            label = "Craquage thermique et catalytique"
        draw.text((x+10, y+8), label, font=font, fill="#eee5d4")
        for dx, bg in [(12, "#443c30"), (186, "#d8d1c1")]:
            thumb = icon.resize((160, 160), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (160, 160), bg)
            tile.paste(thumb, (0, 0), thumb)
            sheet.paste(tile, (x+dx, y+38))
        draw.text((x+12, y+215), f"DDS {entry['size']} px / {entry['mips']} mipmaps", font=font, fill="#eee5d4")
        cursor = x+12
        for size in ([48, 64, 96] if entry["family"] == "BUILDING" else [32, 48, 64]):
            tiny = icon.resize((size, size), Image.Resampling.LANCZOS)
            sheet.paste(tiny, (cursor, y+255), tiny)
            draw.text((cursor, y+332), str(size)+" px", font=font, fill="#eee5d4")
            cursor += size+25
    if not refinery_integrated:
        draw.text((732, 480), "Raffinerie : apercu retouche", font=font, fill="#eee5d4")
        draw.text((732, 515), "Non integree dans ce lot", font=font, fill="#eee5d4")
    sheet.save(PACK / "LOT_3_DDS_INTEGRES_QA.png")
    report = {"status": "PASS_SIX_STATIC_BINDINGS_AND_DDS" if refinery_integrated else "PASS_FIVE_STATIC_BINDINGS_AND_DDS", "integrated_count": len(rows), "gameplay_unchanged": True, "changed_definition_files": sorted(changed), "new_dds_files": sorted(added), "other_protected_files_unchanged": len(baseline)-len(changed), "source_alpha_preserved": True, "transparent_furnace_opening_verified": True, "refinery": "INTEGRATED_APPROVED_V3" if refinery_integrated else "REVISED_PREVIEW_NOT_INTEGRATED", "technical_note": manifest["technical_warning"], "game_tested": False, "assets": rows}
    (PACK / "integration_static_validation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    manifest["status"] = "SIX_ICONS_INTEGRATED_AND_STATICALLY_VALIDATED" if refinery_integrated else "FIVE_ICONS_INTEGRATED_AND_STATICALLY_VALIDATED"
    (PACK / "integration_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    previews = json.loads((PACK / "preview_manifest.json").read_text(encoding="utf-8"))
    previews["status"] = "ALL_SIX_INTEGRATED_STATICALLY_VALIDATED" if refinery_integrated else "PARTIALLY_INTEGRATED_REFINERY_REVISION_PENDING"
    for entry in previews["entries"]:
        if entry["key"] == "oil_refinery" and not refinery_integrated:
            entry["preview"] = "previews/oil_refinery_v3_foreground_contrast.png"
            entry["master_sha256"] = sha((PACK / entry["preview"]).read_bytes())
            entry["status"] = "REVISED_PREVIEW_PENDING_APPROVAL_WITH_OPACITY_NOTE"
        else:
            integrated = next(e for e in manifest["entries"] if e["key"] == entry["key"])
            entry["preview"] = integrated["preview"]
            entry["master_sha256"] = integrated["source_sha256"]
            entry["status"] = "INTEGRATED_STATICALLY_VALIDATED"
    (PACK / "preview_manifest.json").write_text(json.dumps(previews, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
