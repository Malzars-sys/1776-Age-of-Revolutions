"""Independent native DDS/color checks and visual-only definition protection."""
from io import BytesIO
from collections import Counter
import hashlib
import json
import struct
from PIL import Image, ImageDraw, ImageFont
from asset4_style_reference_audit import ROOT, TOKENS, field, pairs, parse
from building_dds_compat import assert_export_layout

PACK = ROOT / "docs/reports/assets/asset26_preview_2026-10-05/revision_v3"
def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest = json.loads((PACK / "integration_manifest.json").read_text(encoding="utf-8"))
    exports = json.loads((PACK / "integration_export_validation.json").read_text(encoding="utf-8"))
    baseline = json.loads((PACK / manifest["protected_baseline"]).read_text(encoding="utf-8"))
    assert manifest["approval"]["approved"] and len(manifest["entries"]) == 3
    rows, icons = [], []
    (PACK / "decoded_dds_png").mkdir(exist_ok=True)
    for entry in manifest["entries"]:
        definitions = dict(pairs(parse(ROOT / entry["definition"])))
        assert field(definitions[entry["id"]], "texture") == entry["dds"]
        assert sum(k == "texture" for k, _ in pairs(definitions[entry["id"]])) == 1
        assert sha((PACK / entry["preview"]).read_bytes()) == entry["source_sha256"]
        payload = (ROOT / entry["dds"]).read_bytes()
        assert payload[:4] == b"DDS " and len(payload) == 349652
        assert struct.unpack_from("<II", payload, 12) == (256, 256)
        assert struct.unpack_from("<I", payload, 28)[0] == 9
        assert_export_layout(payload, entry["dds"])
        export = next(r for r in exports["results"] if r["key"] == entry["key"])
        assert sha(payload) == export["dds_sha256"]
        offset, checked = 128, []
        for mip in export["mip_hashes"]:
            size = mip["size"]
            native = payload[offset:offset + size*size*4]
            rgba = bytearray(native)
            rgba[0::4], rgba[2::4] = native[2::4], native[0::4]
            assert sha(rgba) == mip["rgba_sha256"], "Native colors/alpha changed"
            offset += size*size*4
            checked.append(size)
        assert offset == len(payload) and checked == [256,128,64,32,16,8,4,2,1]
        decoded = Image.open(BytesIO(payload)).convert("RGBA")
        expected = Image.open(PACK / export["target_png"]).convert("RGBA")
        assert decoded.tobytes() == expected.tobytes()
        alpha = decoded.getchannel("A")
        assert alpha.getextrema()[0] == 0 and alpha.getextrema()[1] >= 240
        assert all(alpha.getpixel(p) == 0 for p in [(0,0),(255,0),(0,255),(255,255)])
        decoded.save(PACK / "decoded_dds_png" / (entry["key"] + ".png"))
        icons.append((entry, decoded))
        rows.append({"id":entry["id"],"dds":entry["dds"],"dimensions":[256,256],"mip_sizes":checked,"all_mip_colors_and_alpha_match":True,"native_layout":True,"binding_valid":True})
    for filename, previous in manifest["definition_baseline"].items():
        assert previous["sha256"] == baseline[filename]
        old = dict(pairs([t for t in TOKENS.findall(previous["text"]) if not t.startswith("#")]))
        new = dict(pairs(parse(ROOT / filename)))
        for entry in manifest["entries"]:
            if entry["definition"] == filename:
                assert field(old[entry["id"]], "texture") == entry["previous_texture"]
                for definitions in (old, new):
                    definitions[entry["id"]] = [(k,v) for k,v in pairs(definitions[entry["id"]]) if k != "texture"]
        assert old == new, "Non-visual gameplay edit"
        old_lines = previous["text"].splitlines()
        new_lines = (ROOT / filename).read_text(encoding="utf-8").splitlines()
        assert len(old_lines) == len(new_lines), "Unexpected definition line count"
        actual_changes = Counter((a.strip(), b.strip()) for a, b in zip(old_lines, new_lines) if a != b)
        assert all(a[:len(a)-len(a.lstrip())] == b[:len(b)-len(b.lstrip())] for a,b in zip(old_lines,new_lines)), "Indentation changed"
        expected_changes = Counter(
            ('texture = "' + e["previous_texture"] + '"', 'texture = "' + e["dds"] + '"')
            for e in manifest["entries"] if e["definition"] == filename
        )
        assert actual_changes == expected_changes, "Changes exceed exact approved texture lines"
    changed = {p for p,h in baseline.items() if not (ROOT / p).is_file() or sha((ROOT / p).read_bytes()) != h}
    allowed_changed = set(manifest["definition_baseline"])
    assert changed == allowed_changed, "Unrelated protected game file changed"
    current = {p.relative_to(ROOT).as_posix() for d in ["common","gfx"] for p in (ROOT/d).rglob("*") if p.is_file()}
    added = current - baseline.keys()
    assert added == {e["dds"] for e in manifest["entries"]}
    sheet = Image.new("RGB", (1080,350), "#22282b")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",16)
    for i,(entry,icon) in enumerate(icons):
        x = i*360
        draw.text((x+10,8),entry["label"],font=font,fill="#eee5d4")
        for dx,bg in [(12,"#443c30"),(186,"#d8d1c1")]:
            thumb = icon.resize((160,160),Image.Resampling.LANCZOS)
            tile = Image.new("RGB",(160,160),bg)
            tile.paste(thumb,(0,0),thumb)
            sheet.paste(tile,(x+dx,40))
        draw.text((x+12,212),"DDS natif 256 px / 9 mipmaps",font=font,fill="#eee5d4")
        for j,size in enumerate([32,48,64]):
            thumb = icon.resize((size,size),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(x+12+j*100,254),thumb)
    sheet.save(PACK / "LOT_23_DDS_INTEGRES_QA.png")
    report = {"status":"PASS_THREE_INTEGRATED_NATIVE_TECHNOLOGY_ICONS","integrated_count":3,"gameplay_unchanged":True,"changed_definition_files":sorted(changed),"new_dds_files":sorted(added),"other_protected_files_unchanged":len(baseline)-len(changed),"game_tested":False,"assets":rows}
    (PACK / "integration_static_validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    manifest["status"] = "THREE_ICONS_INTEGRATED_STATICALLY_VALIDATED"
    (PACK / "integration_manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    main()
