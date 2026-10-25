"""Deterministic format-only export of the approved Saint-Gobain artwork.

Read-only by default. --export replaces only the company DDS; the illustration,
company definition and prestige-good icon are not redrawn or changed.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct

from PIL import Image, ImageDraw, ImageFont

from building_dds_compat import BGRA, assert_export_layout

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / 'workshop_assets/source/saint_gobain_company_original.png'
ICON = ROOT / 'gfx/interface/icons/company_icons/historical_company_icons/france_saint_gobain.dds'
SOURCE_SHA256 = '8f2d4dc0ead7e524a0ecb33bacf3a40749dc752b30dbafa273e9b44981ef0cf5'
LOW_RES_SHA256 = 'a9e9b7307de51f3e53226e43a3cb9543dba3d0655bdbd5503a975513f515d57d'
SIZE = 256


def sha(data):
    return hashlib.sha256(data).hexdigest()


def resized(image, size):
    # Premultiplied-alpha filtering avoids dark fringes at transparent edges.
    return image.convert('RGBa').resize((size, size), Image.Resampling.LANCZOS).convert('RGBA')


def prepared_icon():
    data = MASTER.read_bytes()
    assert sha(data) == SOURCE_SHA256, 'Retained original differs from approved attachment'
    source = Image.open(io.BytesIO(data)).convert('RGBA')
    assert source.size == (1254, 1254)
    assert source.getchannel('A').getextrema() == (0, 255)
    # Keep the whole approved composition: no crop, padding, sharpening or repaint.
    return resized(source, SIZE)


def dds_bytes(target):
    assert target.mode == 'RGBA' and target.size == (SIZE, SIZE)
    header = bytearray(128)
    header[:4] = b'DDS '
    for offset, value in ((4, 124), (8, 0x2100f), (12, SIZE), (16, SIZE),
                          (20, SIZE * 4), (28, 9), (76, 32), (80, 0x41), (88, 32),
                          (92, BGRA[0]), (96, BGRA[1]), (100, BGRA[2]),
                          (104, BGRA[3]), (108, 0x401008)):
        struct.pack_into('<I', header, offset, value)
    levels = []
    size = SIZE
    while size:
        mip = target if size == SIZE else resized(target, size)
        levels.append(mip.tobytes('raw', 'BGRA'))
        size >>= 1
    payload = bytes(header) + b''.join(levels)
    assert len(levels) == 9 and len(payload) == 349652
    assert_export_layout(payload, ICON.relative_to(ROOT).as_posix())
    return payload


def preview(before, after, destination):
    canvas = Image.new('RGB', (820, 540), '#30363c')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
    draw.text((20, 12), 'Saint-Gobain : reconversion depuis le PNG original', font=font, fill='white')
    for x, image, label in [(25, before, 'Avant : DDS 64 x 64 / DXT5'),
                            (435, after, 'Après : DDS 256 x 256 / BGRA8')]:
        draw.text((x, 58), label, font=font, fill='white')
        display = resized(image, 190)
        canvas.paste(display, (x + 85, 100), display)
        draw.text((x, 315), 'Aperçu à 190 x 190 (panneau vanilla)', font=font, fill='white')
        thumb = resized(image, 64)
        canvas.paste(thumb, (x + 145, 360), thumb)
        draw.text((x + 100, 443), 'Petite icône : 64 x 64', font=font, fill='white')
    draw.text((25, 496), 'Même illustration, même transparence. Aucun redessin ni agrandissement du vieux DDS.',
              font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16), fill='white')
    canvas.save(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', action='store_true')
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    expected = dds_bytes(prepared_icon())
    previous = ICON.read_bytes()
    if args.export:
        assert sha(previous) in {LOW_RES_SHA256, sha(expected)}, 'Concurrent icon edit: refusing replacement'
        ICON.write_bytes(expected)
    actual = ICON.read_bytes()
    assert actual == expected, 'Runtime DDS differs from original-derived export'
    decoded = Image.open(io.BytesIO(actual)).convert('RGBA')
    assert decoded.tobytes() == prepared_icon().tobytes(), 'Top mip is not lossless BGRA8'
    assert decoded.getchannel('A').getextrema() == (0, 255)
    assert all(decoded.getpixel(point)[3] == 0 for point in [(0, 0), (255, 0), (0, 255), (255, 255)])
    if args.preview:
        preview(Image.open(io.BytesIO(previous)).convert('RGBA'), decoded, args.preview)
    print(json.dumps(dict(status='PASS_STATIC_SAINT_GOBAIN_ICON',
                          icon=ICON.relative_to(ROOT).as_posix(), master=MASTER.relative_to(ROOT).as_posix(),
                          source_sha256=SOURCE_SHA256, dds_sha256=sha(actual), dimensions=[SIZE, SIZE],
                          format='Uncompressed native BGRA8', mip_levels=9, bytes=len(actual),
                          alpha_preserved=True, top_mip_lossless=True, illustration_redrawn=False,
                          game_tested=False), indent=2))


if __name__ == '__main__':
    main()
