"""Decode local Tech & Res DDS candidates for visual inspection only."""

from io import BytesIO
import json
from pathlib import Path
import struct
import sys
from tempfile import gettempdir

from PIL import Image, ImageDraw


SOURCE = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\529340\3472248460\gfx\interface\icons\production_method_icons")
NAMES = [
    "pm_manual_data_reporting.dds",
    "pm_manual_data_reporting_2.dds",
    "pm_manual_data_optimization.dds",
    "pm_basic_data_analysis.dds",
    "pm_digital_data_on_premises.dds",
    "disabled.dds",
    "disabled_green.dds",
    "pm_research_center_basic.dds",
    "pm_research_center_medium.dds",
    "pm_research_center_advanced.dds",
]


def decode(path: Path) -> Image.Image:
    data = bytearray(path.read_bytes())
    if data[84:88] == b"DX10":
        # BC7 sRGB and BC7 UNORM share the same compressed pixel layout.
        if struct.unpack_from("<I", data, 128)[0] == 99:
            struct.pack_into("<I", data, 128, 98)
    return Image.open(BytesIO(data)).convert("RGBA")


if __name__ == "__main__":
    cell = 260
    sheet = Image.new("RGB", (cell * 5, cell * 2), "#28282b")
    draw = ImageDraw.Draw(sheet)
    for index, name in enumerate(NAMES):
        icon = decode(SOURCE / name)
        icon = icon.resize((208, 208), Image.Resampling.NEAREST)
        x, y = (index % 5) * cell + 26, (index // 5) * cell + 6
        sheet.paste(icon, (x, y), icon)
        draw.text((x - 20, y + 215), name.removesuffix(".dds"), fill="white")
    output = Path(gettempdir()) / "1776_tech8c_pm_asset_candidates.png"
    sheet.save(output)
    print(output)
    laboratory = Path(__file__).resolve().parents[1] / "gfx/interface/icons/building_icons/1776_research_laboratory.dds"
    if laboratory.exists():
        decoded = decode(laboratory)
        if decoded.size != (256, 256):
            raise ValueError("Laboratory DDS has an unexpected size")
        output_lab = Path(gettempdir()) / "1776_tech8c_laboratory_decoded_dds.png"
        decoded.save(output_lab)
        print(output_lab)
    # Independent decode of the actual seven DDS files referenced by the PMs.
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "docs/reports/assets/tech8c_laboratory_pm_icons.json"
    if manifest_path.exists():
        entries = json.loads(manifest_path.read_text(encoding="utf-8"))["entries"]
        labels = ["Instrumental", "Electrifie", "Haute precision", "General", "Production", "Societe", "Militaire"]
        sheet = Image.new("RGB", (4 * 228, 2 * 290), "#28282b")
        draw = ImageDraw.Draw(sheet)
        for index, (entry, label) in enumerate(zip(entries, labels, strict=True)):
            if "--cutouts" in sys.argv:
                icon = Image.open(root / entry["cutout"]).convert("RGBA")
                icon = icon.resize((208, 208), Image.Resampling.LANCZOS)
            else:
                icon = decode(root / entry["output"])
            if icon.size != (208, 208):
                raise ValueError("Unexpected PM DDS dimensions: " + entry["pm"])
            # Leave the fourth equipment slot blank; four orientations below.
            slot = index if index < 3 else index + 1
            x, y = (slot % 4) * 228 + 10, (slot // 4) * 290 + 10
            for cy in range(0, 208, 16):
                for cx in range(0, 208, 16):
                    color = "#6a655b" if ((cx // 16 + cy // 16) % 2) else "#99938a"
                    draw.rectangle((x + cx, y + cy, x + min(cx + 15, 207), y + min(cy + 15, 207)), fill=color)
            sheet.paste(icon, (x, y), icon)
            draw.text((x, y + 216), label, fill="white")
            thumbnail = icon.resize((32, 32), Image.Resampling.LANCZOS)
            for offset, color in [(0, "#423b2e"), (48, "#dad4c9")]:
                draw.rectangle((x + offset, y + 242, x + offset + 31, y + 273), fill=color)
                sheet.paste(thumbnail, (x + offset, y + 242), thumbnail)
        filename = "tech8c_laboratory_pm_cutout_preview.png" if "--cutouts" in sys.argv else "tech8c_laboratory_pm_preview.png"
        output_pm = root / "docs/reports/assets" / filename
        sheet.save(output_pm)
        print(output_pm)
