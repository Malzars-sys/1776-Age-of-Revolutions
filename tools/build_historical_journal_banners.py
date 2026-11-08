"""Build or verify the two approved-scope historical journal banner exports.

Sources stay unchanged. Default is read-only verification; --write installs
only the two named DDS derivatives. Native banner dimensions/header/mips are
retained. This is asset validation, not an in-game rendering test.
"""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import struct

from PIL import Image, ImageOps

JOURNAL = Path("gfx/interface/illustrations/journal")
SOURCES = (
    ("aor1776_american_destiny.dds",
     Path("gfx/interface/illustrations/frontend/age_of_revolution_frontend_bg.dds"), (0.5, 0.30)),
    ("aor1776_state_and_revolution.dds",
     Path("assets/journal_groups/masters/state_and_revolution_adapted.png"), (0.5, 0.42)),
)


def build(mod, vanilla, write=False):
    reference = (vanilla / JOURNAL / "je_group_illu_great_game.dds").read_bytes()
    if reference[:4] != b"DDS " or reference[84:88] != b"DXT5":
        raise ValueError("Expected the native 128-byte DXT5 banner header")
    height, width = struct.unpack_from("<II", reference, 12)
    mip_count = struct.unpack_from("<I", reference, 28)[0]
    if (width, height, mip_count) != (1108, 200, 11):
        raise ValueError("Native banner contract changed; re-examine exports")
    rows = []
    for name, source, centering in SOURCES:
        source_bytes = (mod / source).read_bytes()
        image = Image.open(BytesIO(source_bytes)).convert("RGBA")
        top = ImageOps.fit(image, (width, height), Image.Resampling.LANCZOS, centering=centering)
        payload, level_sizes = [], []
        w, h = width, height
        for index in range(mip_count):
            level = top if index == 0 else top.resize((w, h), Image.Resampling.LANCZOS)
            encoded = BytesIO()
            level.save(encoded, format="DDS", pixel_format="DXT5")
            data = encoded.getvalue()
            expected = ((w + 3) // 4) * ((h + 3) // 4) * 16
            if data[84:88] != b"DXT5" or len(data) - 128 != expected:
                raise ValueError("Unexpected compressed mip layout")
            payload.append(data[128:])
            level_sizes.append([w, h, expected])
            w, h = max(1, w // 2), max(1, h // 2)
        exported = reference[:128] + b"".join(payload)
        if len(exported) != len(reference):
            raise ValueError("Mip payload differs from native dimensions")
        destination = mod / JOURNAL / name
        previous = destination.read_bytes() if destination.exists() else None
        if write and previous != exported:
            if (destination.read_bytes() if destination.exists() else None) != previous:
                raise ValueError("Destination changed concurrently")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(exported)
        actual = destination.read_bytes() if destination.exists() else None
        if actual is not None:
            with Image.open(BytesIO(actual)) as decoded:
                if decoded.size != (width, height):
                    raise ValueError("DDS readback dimensions differ")
        rows.append({"file": (JOURNAL / name).as_posix(), "source": source.as_posix(),
                     "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                     "source_size": list(image.size), "size": [width, height],
                     "centering": list(centering), "format": "DXT5", "mipmap_count": mip_count,
                     "mip_levels": level_sizes, "bytes": len(exported),
                     "sha256": hashlib.sha256(exported).hexdigest(), "matches": actual == exported})
    return {"status": "PASS_ASSET_STATIC_ONLY" if all(r["matches"] for r in rows) else "FAIL_ASSET_STATIC",
            "runtime_tested": False, "write_requested": write, "artwork": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod-root", type=Path, required=True)
    parser.add_argument("--vanilla-root", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build(args.mod_root, args.vanilla_root, args.write)
    print(json.dumps(result, indent=2))
    return result["status"] != "PASS_ASSET_STATIC_ONLY"


if __name__ == "__main__":
    raise SystemExit(main())
