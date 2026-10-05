"""Independent Pillow decode of all nine mip levels, with immutable-art evidence."""
from io import BytesIO
import hashlib
import json
from pathlib import Path
import struct

from PIL import Image
from building_dds_compat import assert_export_layout, matches_export_hash

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs/reports/assets/building_color_layout_2026-10-03"


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
    rows = []
    for entry in diagnosis["entries"]:
        old = (PACK / "backups" / f"{entry['key']}_{entry['before']}.dds").read_bytes()
        new = (ROOT / entry["dds"]).read_bytes()
        assert hashlib.sha256(old).hexdigest() == entry["before"]
        assert hashlib.sha256(new).hexdigest() == entry["after"]
        assert_export_layout(new, entry["dds"])
        assert matches_export_hash(new, entry["before"], entry["dds"])
        compared = 0
        for before, after in zip(mip_images(old), mip_images(new), strict=True):
            assert before.size == after.size and before.tobytes() == after.tobytes()
            compared += 1
        assert compared == 9
        native_preview = Image.open(PACK / f"{entry['key']}_dds_native_decoded.png").convert("RGBA")
        assert native_preview.tobytes() == Image.open(BytesIO(new)).convert("RGBA").tobytes()
        assert hashlib.sha256((ROOT / entry["png"]).read_bytes()).hexdigest() == entry["source_sha256"]
        rows.append({"key": entry["key"], "mips_identical": compared, "native_storage_verified": True})
    report = {"status": "PASS_INDEPENDENT_PILLOW_ALL_MIPS", "game_tested": False, "assets": rows}
    (PACK / "independent_validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
