"""Decode installed vanilla regional illustrations for local visual reference.

Format conversion only: these are not replacement assets and no game files are
changed. Keep the source illustrations unedited, including their opaque sky.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from asset4_style_reference_audit import ROOT, GAME, decode, catalog, pairs, field


def main():
    output = ROOT / "docs/reports/assets/asset4_import_2026-10-01/regional_references"
    output.mkdir(parents=True, exist_ok=True)
    regions = ["east_asian", "south_asian", "african", "arabic"]
    expected = regions + ["FALLBACK"]
    native = catalog("common/combat_unit_types", native_only=True)
    for unit in ("combat_unit_type_line_infantry", "combat_unit_type_cannon_artillery"):
        variants = [value for key, value in pairs(native[unit][0]) if key == "combat_unit_image"]
        actual = [field(field(value, "trigger", []), "has_culture_graphics", "FALLBACK") for value in variants]
        if actual != expected:
            raise ValueError(f"Unexpected vanilla branches for {unit}: {actual}")
        print(unit, actual)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    families = ["infantry_{region}_irregular", "infantry_{region}_line", "artillery_{region}_cannon"]
    sheet = Image.new("RGB", (4 * 290, 3 * 330), "#262b30")
    draw = ImageDraw.Draw(sheet)
    for row, pattern in enumerate(families):
        for column, region in enumerate(regions):
            name = pattern.format(region=region)
            source = GAME / f"gfx/unit_illustrations/{name}.dds"
            image = decode(source)
            image.save(output / f"{name}.png")
            thumb = image.copy()
            thumb.thumbnail((270, 270), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (column * 290 + 10, row * 330 + 8), thumb)
            draw.text((column * 290 + 8, row * 330 + 286), name, font=font, fill="#eee6d8")
            print(name, image.size)
    sheet.save(output / "VANILLA_REGIONAL_REFERENCE.png")


if __name__ == "__main__":
    main()
