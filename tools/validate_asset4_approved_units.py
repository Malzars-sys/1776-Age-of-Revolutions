"""Read-only checks: approved regional images, DDS, branches and unchanged gameplay."""
from io import BytesIO
import hashlib
import json
import struct
import subprocess

from PIL import Image
from asset4_style_reference_audit import ROOT, TOKENS, catalog, field, pairs, parse


def without_images(tokens):
    return [(key, value) for key, value in pairs(tokens) if key != "combat_unit_image"]


def branches(tokens):
    return [(field(field(value, "trigger", []), "has_culture_graphics", "FALLBACK"),
             field(value, "texture")) for key, value in pairs(tokens) if key == "combat_unit_image"]


def main():
    pack = ROOT / "docs/reports/assets/asset4_import_2026-10-01"
    approval = json.loads((pack / "unit_art_approval.json").read_text(encoding="utf-8"))
    exports = json.loads((pack / "approved_unit_export_validation.json").read_text(encoding="utf-8"))["results"]
    assert len(exports) == 5 * len(approval["approved_units"])
    assert len({item["target_dds"] for item in exports}) == len(exports)
    filename = "common/combat_unit_types/00_land_combat_unit_types.txt"
    current = dict(pairs(parse(ROOT / filename)))
    native = catalog("common/combat_unit_types", native_only=True)
    rows = []
    for unit in approval["approved_units"]:
        native_key = "combat_unit_type_line_infantry" if unit.endswith("musket_infantry") else "combat_unit_type_cannon_artillery"
        order = [region for region, _ in branches(native[native_key][0])]
        assert order == ["east_asian", "south_asian", "african", "arabic", "FALLBACK"]
        expected = []
        for region in order:
            item = next(x for x in exports if x["unit"] == unit and x["region"] == region)
            expected.append((region, item["target_dds"]))
            image = ROOT / item["preview"]
            assert hashlib.sha256(image.read_bytes()).hexdigest().upper() == item["sha256"]
            payload = (ROOT / item["target_dds"]).read_bytes()
            assert payload[:4] == b"DDS " and len(payload) == 1398228
            assert hashlib.sha256(payload).hexdigest().upper() == item["export_sha256"]
            assert struct.unpack_from("<II", payload, 12) == (512, 512)
            assert struct.unpack_from("<I", payload, 28)[0] == 10
            assert all(value == 255 for value in payload[131::4]), item["key"]
            decoded = Image.open(BytesIO(payload)).convert("RGBA")
            assert decoded.size == (512, 512)
            assert decoded.getchannel("A").getextrema() == (255, 255)
            rows.append({"unit": unit, "region": region, "texture": item["target_dds"], "mips": 10})
        assert branches(current[unit]) == expected
    baseline = subprocess.run(["git", "show", "HEAD:" + filename], cwd=ROOT,
                              check=True, capture_output=True).stdout.decode("utf-8-sig")
    old = dict(pairs([token for token in TOKENS.findall(baseline) if not token.startswith("#")]))
    assert old.keys() == current.keys()
    for unit in old:
        if unit in approval["approved_units"]:
            assert without_images(old[unit]) == without_images(current[unit]), unit
        else:
            assert old[unit] == current[unit], "Unapproved definition change: " + unit
    if "combat_unit_type_cannon_artillery" in approval["approved_units"]:
        approved_revision = approval["approved_revisions"]["combat_unit_type_cannon_artillery"]
        assert approved_revision["revision"] == 3
        pinned = json.loads((pack / approved_revision["checks"]).read_text(encoding="utf-8"))["images"]
        bombard_exports = [item for item in exports if item["unit"] == "combat_unit_type_cannon_artillery"]
        assert len(bombard_exports) == len(pinned) == 5
        for item in bombard_exports:
            source = next(check for check in pinned if check["key"] == item["key"])
            assert item["preview"] == source["preview"] and item["sha256"] == source["sha256"]
        bombard_status = "APPROVED_V3_INTEGRATED"
    else:
        assert branches(current["combat_unit_type_cannon_artillery"]) == [("FALLBACK", "gfx/error_deer.dds")]
        bombard_status = "UNINTEGRATED_PENDING_USER_APPROVAL"
    print(json.dumps({"status": "PASS_STATIC_AND_DDS", "integrated_illustrations": len(rows),
                      "native_cultural_branch_order": True, "gameplay_unchanged": True,
                      "bombard": bombard_status, "assets": rows,
                      "limitation": "Not verified in a running game."}, indent=2))


if __name__ == "__main__":
    main()
