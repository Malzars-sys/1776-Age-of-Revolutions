"""Independent decode of every mipmap for every migrated asset family."""
from io import BytesIO
import hashlib
import json
from pathlib import Path
import struct

from PIL import Image
from building_dds_compat import assert_export_layout, matches_export_hash

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs/reports/assets/all_asset_color_layout_2026-10-03"


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def mip_images(payload):
    size = struct.unpack_from("<I", payload, 16)[0]
    count = struct.unpack_from("<I", payload, 28)[0]
    offset = 128
    for _ in range(count):
        length = size * size * 4
        single = bytearray(payload[:128])
        struct.pack_into("<II", single, 12, size, size)
        struct.pack_into("<I", single, 20, size * 4)
        struct.pack_into("<I", single, 28, 1)
        yield Image.open(BytesIO(bytes(single) + payload[offset:offset + length])).convert("RGBA")
        offset += length
        size = max(1, size // 2)
    assert offset == len(payload)


def main():
    diagnosis = json.loads((PACK / "diagnosis.json").read_text(encoding="utf-8"))
    baseline = json.loads((PACK / "baseline.json").read_text(encoding="utf-8"))
    rows = []
    for entry in diagnosis["entries"]:
        new = (ROOT / entry["dds"]).read_bytes()
        old = (PACK / "backups" / f"{entry['key']}_{entry['before']}.dds").read_bytes() if entry["changed"] else new
        assert digest(old) == entry["before"] and digest(new) == entry["after"]
        assert_export_layout(new, entry["dds"])
        assert matches_export_hash(new, entry["before"], entry["dds"])
        if entry.get("export_hash"):
            assert matches_export_hash(new, entry["export_hash"], entry["dds"])
        for source in entry["pinned_sources"]:
            assert digest((ROOT / source["path"]).read_bytes()) == source["sha256"].lower()
        count = 0
        for before, after in zip(mip_images(old), mip_images(new), strict=True):
            assert before.size == after.size and before.tobytes() == after.tobytes(), entry["dds"]
            count += 1
        assert count == entry["mips"]
        image = Image.open(BytesIO(new)).convert("RGBA")
        native_preview = Image.open(PACK / f"{entry['key']}_native_decoded.png").convert("RGBA")
        assert image.tobytes() == native_preview.tobytes()
        # A separate decoder explicitly ignores masks and uses native BGRA storage.
        size = entry["size"]
        native = Image.frombytes("RGBA", (size, size), new[128:128 + size * size * 4], "raw", "BGRA")
        assert native.tobytes() == image.tobytes()
        rows.append({"key": entry["key"], "family": entry["family"], "mips_identical": count,
                     "native_storage_verified": True, "converted_this_pass": entry["changed"]})
    changed = []
    for relative, expected in baseline.items():
        if digest((ROOT / relative).read_bytes()) != expected:
            changed.append(relative)
    assert sorted(changed) == sorted(e["dds"] for e in diagnosis["entries"] if e["changed"])
    report = {"status": "PASS_INDEPENDENT_PILLOW_ALL_FAMILIES_ALL_MIPS", "game_tested": False,
              "verified_assets": len(rows), "verified_mips": sum(r["mips_identical"] for r in rows),
              "converted": len(changed), "other_game_files_unchanged": len(baseline) - len(changed),
              "source_colors_and_alpha_unchanged": True, "assets": rows}
    (PACK / "independent_validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "assets"}, indent=2))


if __name__ == "__main__":
    main()
