"""Independent decoded DDS validation and visual-only changes against pre-integration state."""
from io import BytesIO
import hashlib
import json
import struct
import sys

from PIL import Image, ImageDraw, ImageFont
from asset4_style_reference_audit import ROOT, TOKENS, field, pairs, parse

PACK = ROOT / "docs/reports/assets/asset5_preview_2026-10-02"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tokens(text):
    return [t for t in TOKENS.findall(text) if not t.startswith("#")]


def main():
    args = sys.argv[1:]
    if args and (len(args) != 1 or not args[0].startswith("--only=")):
        raise SystemExit("Usage: validate_asset5_approved_icons.py [--only=asset_key]")
    only = args[0].split("=", 1)[1] if args else None
    manifest = json.loads((PACK / "integration_manifest.json").read_text(encoding="utf-8"))
    exports = json.loads((PACK / "integration_export_validation.json").read_text(encoding="utf-8"))
    baseline = json.loads((PACK / manifest["protected_baseline"]).read_text(encoding="utf-8"))
    assert manifest["approval"]["approved"] is True
    assert len(manifest["entries"]) == 6
    selected = [entry for entry in manifest["entries"] if not only or entry["key"] == only]
    assert not only or len(selected) == 1, "Unknown single-asset validation target"
    rows, decoded_icons = [], []
    for entry in selected:
        definitions = dict(pairs(parse(ROOT / entry["definition"])))
        assert field(definitions[entry["id"]], entry["field"]) == entry["dds"], entry["id"]
        assert sum(k == entry["field"] for k, _ in pairs(definitions[entry["id"]])) == 1
        source = (PACK / entry["preview"]).read_bytes()
        assert sha(source) == entry["source_sha256"], "Approved source modified"
        payload = (ROOT / entry["dds"]).read_bytes()
        assert payload[:4] == b"DDS "
        height, width = struct.unpack_from("<II", payload, 12)
        mips = struct.unpack_from("<I", payload, 28)[0]
        assert (width, height) == (entry["size"], entry["size"])
        assert mips == entry["mips"]
        assert struct.unpack_from("<II", payload, 76) == (32, 0x41)
        assert struct.unpack_from("<IIIII", payload, 88) == (32, 0xff, 0xff00, 0xff0000, 0xff000000)
        offset, level = 128, entry["size"]
        mip_sizes = []
        for _ in range(mips):
            size = level * level * 4
            assert len(payload[offset:offset+size]) == size
            mip_sizes.append(level)
            offset += size
            level = max(1, level // 2)
        assert mip_sizes[-1] == 1 and offset == len(payload), "Invalid full mip chain"
        decoded = Image.open(BytesIO(payload)).convert("RGBA")
        export = next(row for row in exports["results"] if row["key"] == entry["key"])
        expected = Image.open(PACK / export["target_png"]).convert("RGBA")
        assert decoded.tobytes() == expected.tobytes(), "DDS differs from native-size PNG"
        assert sha(payload) == export["dds_sha256"]
        alpha = decoded.getchannel("A")
        assert alpha.getextrema()[0] == 0 and alpha.getextrema()[1] >= 240
        assert all(alpha.getpixel(p) == 0 for p in [(0,0),(width-1,0),(0,height-1),(width-1,height-1)])
        interior_alpha = alpha.crop((width*15//100,height*15//100,width*85//100,height*85//100)).getextrema() if entry["family"] == "BUILDING" else None
        rows.append({"id":entry["id"],"dds":entry["dds"],"size":width,"mips":mips,"mip_sizes":mip_sizes,
                     "sha256":sha(payload),"true_exterior_alpha":True,"interior_alpha":interior_alpha})
        decoded_icons.append((entry, decoded))

    if only:
        # Deliberately scoped: retain the historic lot-wide baseline report.
        decoded_icons[0][1].save(PACK / f"{only}_dds_decoded_current.png")
        report = {"status":"PASS_TARGET_ASSET_BINDING_AND_DECODED_DDS",
                  "asset":only,"assets":rows,"source_alpha_preserved":True,
                  "historic_batch_baseline_checked":False,"game_tested":False}
        (PACK / f"{only}_replacement_validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(report,indent=2))
        return

    # Compare the actual working-tree state before integration, not HEAD; preserve earlier user edits.
    for filename, previous in manifest["definition_baseline"].items():
        assert previous["sha256"] == baseline[filename]
        old = dict(pairs(tokens(previous["text"])))
        new = dict(pairs(parse(ROOT / filename)))
        for entry in manifest["entries"]:
            if entry["definition"] == filename:
                for definitions in (old,new):
                    definitions[entry["id"]] = [(k,v) for k,v in pairs(definitions[entry["id"]]) if k != entry["field"]]
        assert old == new, "Non-visual definition change: " + filename

    allowed_changed = set(manifest["definition_baseline"])
    allowed_added = {entry["dds"] for entry in manifest["entries"]}
    changed = []
    for relative, digest in baseline.items():
        assert (ROOT / relative).is_file(), "Protected file removed: " + relative
        if sha((ROOT / relative).read_bytes()) != digest:
            changed.append(relative)
            assert relative in allowed_changed, "Unrelated file changed: " + relative
    current_files = {str(p.relative_to(ROOT)).replace("\\","/") for folder in ["common","gfx"] for p in (ROOT / folder).rglob("*") if p.is_file()}
    added = current_files - baseline.keys()
    assert added == allowed_added, "Unexpected additions / missing exports: " + str(added ^ allowed_added)
    assert set(changed) == allowed_changed

    # Preserve the still-unapproved cement building and its production-method previews.
    cement = dict(pairs(parse(ROOT / "common/buildings/11_tech6c1b_cement_works.txt")))
    assert field(cement["building_cement_works"],"icon").endswith("unused/foundries.dds")
    for _, pm in pairs(parse(ROOT / "common/production_methods/11_tech6c1b_cement_production.txt")):
        assert field(pm,"texture") == "gfx/error_deer.dds"

    # Only layout/reduction of the independently decoded exports for visual inspection.
    sheet = Image.new("RGB",(1080,780),"#22282b")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",17)
    small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",13)
    for index,(entry,icon) in enumerate(decoded_icons):
        x, y = index%3*360, index//3*390
        draw.text((x+10,y+7),entry["label"],font=font,fill="#eee5d4")
        for dx,bg in [(12,"#443c30"),(186,"#d8d1c1")]:
            thumb=icon.resize((160,160),Image.Resampling.LANCZOS)
            tile=Image.new("RGB",(160,160),bg); tile.paste(thumb,(0,0),thumb)
            sheet.paste(tile,(x+dx,y+40))
        draw.text((x+12,y+212),f"DDS {entry['size']} px / {entry['mips']} mipmaps",font=small,fill="#eee5d4")
        sizes = [48,64,96] if entry["family"] == "BUILDING" else [32,48,64]
        cursor=x+12
        for size in sizes:
            tiny=icon.resize((size,size),Image.Resampling.LANCZOS)
            sheet.paste(tiny,(cursor,y+250),tiny)
            draw.text((cursor,y+350),str(size)+" px",font=small,fill="#eee5d4")
            cursor+=size+25
    sheet.save(PACK / "LOT_2_DDS_INTEGRES_QA.png")
    report={"status":"PASS_STATIC_AND_DDS_WITH_OPACITY_WARNING","integrated_count":len(rows),
            "gameplay_unchanged":True,"changed_definition_files":sorted(changed),"new_dds_files":sorted(added),
            "other_protected_files_unchanged":len(baseline)-len(changed),"source_alpha_preserved":True,
            "warnings":[manifest["technical_warning"]],"cement_previews":"NOT_INTEGRATED",
            "game_tested":False,"assets":rows}
    (PACK / "integration_static_validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
