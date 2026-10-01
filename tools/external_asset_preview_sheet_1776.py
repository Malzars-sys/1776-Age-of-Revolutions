"""Make a contact sheet of external icon candidates for visual review only."""

from pathlib import Path
from tempfile import gettempdir
from io import BytesIO
import struct

from PIL import Image, ImageDraw


WORKSHOP = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\529340")
CANDIDATES = [
    ("Basileia", "Ateliers", "2880120246", "invention_icons/br_tech_artisan_manufacturing.dds"),
    ("Basileia", "Sciences", "2880120246", "invention_icons/br_tech_early_modern_universities.dds"),
    ("Basileia", "Papier", "2880120246", "invention_icons/br_tech_paper_manufacturies.dds"),
    ("Basileia", "Semoir", "2880120246", "invention_icons/br_tech_seed_drill.dds"),
    ("Morgenroete", "Geologie", "2889925770", "invention_icons/agassiz_geology_tech.dds"),
    ("Morgenroete", "Vaccination", "2889925770", "invention_icons/panum_vaccination_tech.dds"),
    ("Morgenroete", "Presse", "2889925770", "invention_icons/manzoni_rotary_press_tech.dds"),
    ("E&F", "Pharmacie", "3143591632", "production_method_icons/unuse/pharmacies.dds"),
    ("E&F", "Apothicaire", "3143591632", "production_method_icons/unuse/apothecaries.dds"),
    ("E&F", "Pharmacie 2", "3143591632", "production_method_icons/unuse/pharmacy.dds"),
]

CELL = 215
sheet = Image.new("RGB", (CELL * 4, CELL * ((len(CANDIDATES) + 3) // 4)), "#26282b")
draw = ImageDraw.Draw(sheet)
for index, (mod, label, workshop_id, relative) in enumerate(CANDIDATES):
    source = WORKSHOP / workshop_id / "gfx/interface/icons" / relative
    try:
        icon = Image.open(source).convert("RGBA")
    except NotImplementedError:
        # Pillow lacks some sRGB DXGI aliases; their pixel layout is unchanged.
        data = bytearray(source.read_bytes())
        dxgi = struct.unpack_from("<I", data, 128)[0]
        if dxgi not in (29, 91):
            raise
        if dxgi == 91:
            height, width = struct.unpack_from("<II", data, 12)
            icon = Image.frombytes("RGBA", (width, height), bytes(data[148:148 + width * height * 4]), "raw", "BGRA")
        else:
            struct.pack_into("<I", data, 128, 28)
            icon = Image.open(BytesIO(data)).convert("RGBA")
    icon.thumbnail((175, 175), Image.Resampling.LANCZOS)
    x = (index % 4) * CELL + (CELL - icon.width) // 2
    y = (index // 4) * CELL + 5
    sheet.paste(icon, (x, y), icon)
    draw.text(((index % 4) * CELL + 8, (index // 4) * CELL + 182), f"{mod}: {label}", fill="white")

destination = Path(gettempdir()) / "1776_external_asset_candidates.png"
sheet.save(destination)
print(destination)
