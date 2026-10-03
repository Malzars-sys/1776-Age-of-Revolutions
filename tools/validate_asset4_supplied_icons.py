"""Read-only checks for the supplied ASSET4 art integration, not a game launch."""
from io import BytesIO
import json
import re
import struct
import subprocess

from PIL import Image

from asset4_style_reference_audit import ROOT, TOKENS, field, pairs, parse


def main():
    manifest = json.loads((ROOT / "docs/reports/assets/asset4_import_2026-10-01/manifest.json").read_text(encoding="utf-8"))
    rows = []
    for entry in manifest["entries"]:
        definitions = dict(pairs(parse(ROOT / entry["definition"])))
        assert field(definitions[entry["id"]], entry["field"]) == entry["dds"], entry["id"]
        payload = (ROOT / entry["dds"]).read_bytes()
        assert payload[:4] == b"DDS "
        height, width = struct.unpack_from("<II", payload, 12)
        mips = struct.unpack_from("<I", payload, 28)[0]
        assert (width, height) == (entry["size"], entry["size"])
        assert mips == (8 if entry["size"] == 208 else 9)
        decoded = Image.open(BytesIO(payload)).convert("RGBA")
        assert decoded.getchannel("A").getextrema()[0] == 0
        assert decoded.getchannel("A").getextrema()[1] >= 240
        rows.append({"id": entry["id"], "reference": entry["dds"], "size": width,
                     "mips": mips, "true_alpha": True})

    # Prove the integration changes visual fields only in the six consuming files.
    for filename in {entry["definition"] for entry in manifest["entries"]}:
        baseline = subprocess.run(["git", "show", "HEAD:" + filename], cwd=ROOT,
                                  check=True, capture_output=True).stdout.decode("utf-8-sig")
        old = dict(pairs([token for token in TOKENS.findall(baseline) if not token.startswith("#")]))
        new = dict(pairs(parse(ROOT / filename)))
        for entry in manifest["entries"]:
            if entry["definition"] == filename:
                for data in (old, new):
                    data[entry["id"]] = [(k, v) for k, v in pairs(data[entry["id"]]) if k != entry["field"]]
        assert old == new, "Non-visual definition change: " + filename

    cement_works = dict(pairs(parse(ROOT / "common/buildings/11_tech6c1b_cement_works.txt")))
    assert field(cement_works["building_cement_works"], "icon").endswith("unused/foundries.dds")
    for _, tokens in pairs(parse(ROOT / "common/production_methods/11_tech6c1b_cement_production.txt")):
        assert field(tokens, "texture") == "gfx/error_deer.dds"
    print(json.dumps({"status": "PASS_STATIC_AND_DDS", "integrated_count": len(rows),
                      "gameplay_unchanged_in_visual_files": True, "cement_building_and_pms": "PREVIEW_ONLY",
                      "assets": rows, "limitations": "Not tested inside the game."}, indent=2))


if __name__ == "__main__":
    main()
