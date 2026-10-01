"""Build a silent left-to-right travelling shot for the birth-quota event.

Usage: python tools/build_birth_quota_event_art.py SOURCE.png OUTPUT.avi
Encode OUTPUT.avi to gfx/event_pictures/birth_quota_scene.bk2 with RAD Video Tools.
The free encoder emits Bink 1, which Victoria 3's bundled Bink DLL can open.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

from PIL import Image, ImageOps


WIDTH = 960
HEIGHT = 540
FPS = 10
FRAMES = 90
TRAVEL_FRAMES = 65


def chunk(tag: bytes, payload: bytes) -> bytes:
    return tag + struct.pack("<I", len(payload)) + payload + (b"\0" if len(payload) % 2 else b"")


def list_chunk(kind: bytes, payload: bytes) -> bytes:
    return chunk(b"LIST", kind + payload)


def build(source: Path, output: Path, icon_root: Path | None = None) -> None:
    with Image.open(source) as input_image:
        image = ImageOps.fit(input_image.convert("RGB"), (1280, 720))
        if icon_root is not None:
            icon_path = icon_root / "event_icons/birth_quota_scene.dds"
            icon_path.parent.mkdir(parents=True, exist_ok=True)
            ImageOps.fit(input_image.convert("RGBA"), (150, 150)).save(icon_path, format="DDS")

    frame_size = WIDTH * HEIGHT * 3
    avih = struct.pack(
        "<14I",
        1_000_000 // FPS,
        frame_size * FPS,
        0,
        0x10,
        FRAMES,
        0,
        1,
        frame_size,
        WIDTH,
        HEIGHT,
        0,
        0,
        0,
        0,
    )
    strh = struct.pack(
        "<4s4sIHHIIIIIIIIhhhh",
        b"vids",
        b"DIB ",
        0,
        0,
        0,
        0,
        1,
        FPS,
        0,
        FRAMES,
        frame_size,
        0xFFFFFFFF,
        0,
        0,
        0,
        WIDTH,
        HEIGHT,
    )
    strf = struct.pack("<IiiHHIIiiII", 40, WIDTH, HEIGHT, 1, 24, 0, frame_size, 0, 0, 0, 0)
    header = list_chunk(b"hdrl", chunk(b"avih", avih) + list_chunk(b"strl", chunk(b"strh", strh) + chunk(b"strf", strf)))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as video:
        video.write(b"RIFF\0\0\0\0AVI ")
        video.write(header)
        movi_start = video.tell()
        video.write(b"LIST\0\0\0\0movi")
        index = []
        for number in range(FRAMES):
            # Travel from the officials on the left to the woman on the right,
            # then hold on her for the final 2.5 seconds.
            t = min(1.0, number / (TRAVEL_FRAMES - 1))
            eased = t * t * (3 - 2 * t)
            zoom = 1.45 + 0.55 * eased
            crop_width = round(image.width / zoom)
            crop_height = round(image.height / zoom)
            center_x = 455 + 335 * eased
            center_y = 300 + 235 * eased
            x = round(center_x - crop_width / 2)
            y = round(center_y - crop_height / 2)
            x = max(0, min(x, image.width - crop_width))
            y = max(0, min(y, image.height - crop_height))
            frame = image.crop((x, y, x + crop_width, y + crop_height)).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
            pixels = frame.transpose(Image.Transpose.FLIP_TOP_BOTTOM).tobytes("raw", "BGR")
            offset = video.tell() - (movi_start + 8)
            video.write(chunk(b"00db", pixels))
            index.append(struct.pack("<4sIII", b"00db", 0x10, offset, len(pixels)))

        end_movi = video.tell()
        video.seek(movi_start + 4)
        video.write(struct.pack("<I", end_movi - movi_start - 8))
        video.seek(end_movi)
        video.write(chunk(b"idx1", b"".join(index)))
        file_end = video.tell()
        video.seek(4)
        video.write(struct.pack("<I", file_end - 8))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--icon-root", type=Path, default=None)
    arguments = parser.parse_args()
    build(arguments.source, arguments.output, arguments.icon_root)
