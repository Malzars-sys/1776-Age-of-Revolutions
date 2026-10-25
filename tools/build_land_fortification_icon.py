"""Format-only export of the user's icon after built-in background extraction.

No illustration or alpha mask is drawn here. The retained transparent master
is encoded to the canonical building-icon layout: 256px BGRA8 with nine mips.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import struct

from PIL import Image
from building_dds_compat import BGRA, assert_export_layout

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / 'workshop_assets/source/aor1776_land_fortification_transparent.png'
ICON = ROOT / 'gfx/interface/icons/building_icons/building_aor1776_land_fortification.dds'
SIZE = 256


def resized(image, size):
    return image.convert('RGBa').resize((size, size), Image.Resampling.LANCZOS).convert('RGBA')


def expected_dds():
    source = Image.open(MASTER).convert('RGBA')
    assert source.size == (1254, 1254) and source.getchannel('A').getextrema() == (0, 255)
    target = resized(source, SIZE)
    header = bytearray(128)
    header[:4] = b'DDS '
    for offset, value in ((4, 124), (8, 0x2100f), (12, SIZE), (16, SIZE),
                          (20, SIZE * 4), (28, 9), (76, 32), (80, 0x41), (88, 32),
                          (92, BGRA[0]), (96, BGRA[1]), (100, BGRA[2]),
                          (104, BGRA[3]), (108, 0x401008)):
        struct.pack_into('<I', header, offset, value)
    sizes = [SIZE >> i for i in range(9)]
    payload = bytes(header) + b''.join((target if n == SIZE else resized(target, n)).tobytes('raw', 'BGRA') for n in sizes)
    assert len(payload) == 349652
    assert_export_layout(payload, ICON.relative_to(ROOT).as_posix())
    return payload, target


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--export', action='store_true')
    args = ap.parse_args()
    expected, target = expected_dds()
    if args.export:
        assert not ICON.exists() or ICON.read_bytes() == expected, 'Concurrent icon edit: refusing replacement'
        ICON.parent.mkdir(parents=True, exist_ok=True)
        ICON.write_bytes(expected)
    actual = ICON.read_bytes()
    assert actual == expected
    decoded = Image.open(io.BytesIO(actual)).convert('RGBA')
    assert decoded.tobytes() == target.tobytes()
    assert all(decoded.getpixel(p)[3] == 0 for p in [(0, 0), (255, 0), (0, 255), (255, 255)])
    # The built-in cutout retains near-opaque painting pixels (251-254 alpha).
    # Preserve that returned alpha rather than repainting its interior mask.
    assert decoded.getpixel((128, 128))[3] >= 250
    print(json.dumps(dict(icon=ICON.relative_to(ROOT).as_posix(), size=[256, 256],
                          format='BGRA8', mips=9, alpha=decoded.getchannel('A').getextrema(),
                          sha256=hashlib.sha256(actual).hexdigest(), white_background_removed=True,
                          illustration_editing='Built-in image_gen; this exporter changes format only.'), indent=2))


if __name__ == '__main__':
    main()
