"""Build and implement the reviewed TECH6C5B global copper distribution."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "map_data" / "state_regions"
OUT = ROOT / "docs" / "reports" / "industry" / "TECH6C5B_COPPER_GLOBAL_RESOURCE_MATRIX.csv"

TIERS = {0: "NONE", 8: "LOW", 16: "MODEST", 24: "MEDIUM", 36: "HIGH", 48: "VERY_HIGH", 60: "WORLD_CLASS"}

# Each entry: (potential, confidence, source category, geological rationale, states).
# The screen uses modern deposit provinces, not merely mines active during 1776-1936.
GROUPS = [
    (24, "HIGH", "NATIONAL_SURVEY_AND_HISTORIC_DISTRICT", "Scandinavian Caledonian and Bergslagen polymetallic copper provinces", "STATE_SVEALAND STATE_EASTERN_NORWAY"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Secondary Scandinavian sulfide districts with game-scale but dispersed copper potential", "STATE_GOTALAND STATE_NORRLAND STATE_WESTERN_NORWAY"),
    (36, "HIGH", "HISTORIC_DISTRICT_AND_GLOBAL_ASSESSMENT", "Cornwall-Devon metallogenic district with major historic copper endowment", "STATE_WEST_COUNTRY"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "British and Irish Caledonian or Variscan copper districts of moderate regional scale", "STATE_WALES STATE_HIGHLANDS STATE_MUNSTER"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized British-Irish copper occurrences below the major district tier", "STATE_LOWLANDS"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "French Variscan and Alpine polymetallic belts with localized exploitable copper", "STATE_AUVERGNE_LIMOUSIN STATE_LANGUEDOC"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Smaller French Alpine or Armorican copper occurrences", "STATE_RHONE STATE_BRITTANY STATE_PROVENCE"),
    (24, "HIGH", "HISTORIC_DISTRICT", "Mansfeld and Bohemian historic copper-polymetallic districts", "STATE_ANHALT STATE_BOHEMIA"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Central European Variscan and Alpine metallogenic zones", "STATE_WALLONIA STATE_MORAVIA STATE_STYRIA STATE_TYROL STATE_SOUTH_TYROL STATE_WESTPHALIA STATE_SAXONY"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized Central European copper occurrences", "STATE_RHINELAND STATE_HESSE"),
    (36, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "Iberian Pyrite Belt with major volcanogenic massive-sulfide copper potential", "STATE_UPPER_ANDALUSIA"),
    (24, "HIGH", "NATIONAL_SURVEY_AND_HISTORIC_DISTRICT", "Southwest Iberian and Portuguese Pyrite Belt continuation", "STATE_ALENTEJO"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Iberian Variscan and Betic copper-polymetallic districts", "STATE_GALICIA STATE_ASTURIAS STATE_CATALONIA STATE_LOWER_ANDALUSIA STATE_EXTREMADURA STATE_BEIRA STATE_LEON STATE_ENTRE_DOURO_E_MINHO"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized Iberian copper occurrences", "STATE_BASQUE_COUNTRY STATE_ARAGON STATE_MURCIA"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Mediterranean Alpine and island copper-polymetallic districts", "STATE_SARDINIA STATE_CALABRIA STATE_SICILY"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized Apennine copper occurrences", "STATE_TUSCANY"),
    (36, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Bor-Timok porphyry and epithermal copper province", "STATE_EASTERN_SERBIA"),
    (24, "HIGH", "REGIONAL_GEOLOGY_AND_HISTORIC_DISTRICT", "Dinaride and Carpathian copper-polymetallic belts", "STATE_BOSNIA STATE_SLOVAKIA STATE_NORTHERN_TRANSYLVANIA STATE_SOUTHERN_TRANSYLVANIA"),
    (16, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Balkan and Carpathian metallogenic belts with moderate copper potential", "STATE_ALBANIA STATE_BULGARIA STATE_KOSOVO STATE_MACEDONIA STATE_SKOPIA STATE_BANAT STATE_WEST_GALICIA STATE_EAST_GALICIA STATE_RUTHENIA STATE_LOWER_SILESIA"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized Balkan-Carpathian copper occurrences", "STATE_SLOVENIA STATE_CROATIA STATE_MONTENEGRO STATE_THESSALIA STATE_PELOPONNESE STATE_BUKOVINA STATE_UPPER_SILESIA"),
    (24, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "Arabian-Nubian Shield volcanogenic and intrusion-related copper province", "STATE_ERITREA"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "Arabian-Nubian Shield and Sinai copper districts", "STATE_SINAI STATE_MAURITANIA STATE_INNER_MAURITANIA"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized North African shield and Atlas copper occurrences", "STATE_UPPER_EGYPT STATE_EGYPTIAN_DESERT STATE_AL_RIF STATE_INNER_MOROCCO STATE_CONSTANTINE STATE_WESTERN_MALI"),
    (60, "HIGH", "USGS_CENTRAL_AFRICAN_COPPERBELT", "World-class Central African sediment-hosted Copperbelt", "STATE_KATANGA STATE_ZAMBIA"),
    (36, "HIGH", "NATIONAL_SURVEY_AND_HISTORIC_DISTRICT", "Namaqualand historic copper province", "STATE_NAMAQUALAND"),
    (24, "HIGH", "USGS_SEDIMENT_HOSTED_ASSESSMENT", "Kalahari Copperbelt and southern African copper provinces", "STATE_BOTSWANA STATE_HEREROLAND STATE_NORTHERN_CAPE STATE_TRANSVAAL STATE_KAZEMBE STATE_SOUTH_ANGOLA"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "African rift, mobile-belt and Copperbelt fringe potential", "STATE_KASAI STATE_CONGO_ORIENTALE STATE_TANGANYIKA STATE_RIFT_VALLEY STATE_ZAMBEZIA STATE_ZAMBEZI STATE_MOCAMBIQUE STATE_EAST_ANGOLA STATE_SOUTH_CAMEROON"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized African greenstone or mobile-belt copper occurrences", "STATE_GUINEA STATE_GOLD_COAST STATE_SIERRA_LEONE STATE_OROMIA STATE_UGANDA STATE_SOUTH_MADAGASCAR STATE_NORTH_MADAGASCAR"),
    (60, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "World-class Basin and Range porphyry copper province", "STATE_ARIZONA"),
    (48, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Major Bingham and British Columbia Cordilleran porphyry provinces", "STATE_UTAH STATE_BRITISH_COLUMBIA"),
    (36, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "Major Cordilleran and native-copper districts", "STATE_MONTANA STATE_IDAHO STATE_NEVADA STATE_MICHIGAN STATE_YUKON_TERRITORY"),
    (24, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "North American Cordilleran or shield copper provinces", "STATE_ALASKA STATE_WASHINGTON STATE_COLORADO STATE_NEW_MEXICO STATE_CALIFORNIA STATE_ONTARIO"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "Secondary Cordilleran and Canadian shield copper potential", "STATE_OREGON STATE_WYOMING STATE_QUEBEC STATE_NORTHWEST_TERRITORIES"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized North American copper districts", "STATE_SOUTH_DAKOTA STATE_MINNESOTA STATE_MAINE STATE_ALBERTA"),
    (48, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Sonoran porphyry copper province including Cananea", "STATE_SONORA"),
    (36, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Sierra Madre porphyry and skarn copper province", "STATE_CHIHUAHUA"),
    (24, "HIGH", "NATIONAL_SURVEY_AND_GLOBAL_ASSESSMENT", "Mexican porphyry, skarn and polymetallic copper districts", "STATE_DURANGO STATE_MEXICO STATE_GUERRERO STATE_JALISCO STATE_ZACATECAS"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Secondary Mexican metallogenic provinces", "STATE_SINALOA STATE_BAJIO STATE_OAXACA STATE_BAJA_CALIFORNIA"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized northeastern Mexican copper occurrences", "STATE_RIO_GRANDE"),
    (24, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Panamanian porphyry copper belt", "STATE_PANAMA"),
    (16, "MEDIUM", "USGS_GLOBAL_PORPHYRY_DATABASE", "Central American volcanic-arc copper systems", "STATE_GUATEMALA STATE_HONDURAS STATE_NICARAGUA STATE_COSTA_RICA STATE_WESTERN_CUBA STATE_EASTERN_CUBA STATE_CENTRAL_CUBA"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized Caribbean island-arc copper occurrences", "STATE_HAITI STATE_SANTO_DOMINGO STATE_PUERTO_RICO STATE_JAMAICA"),
    (60, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "World-class Central Andean porphyry copper belt", "STATE_ANTOFAGASTA"),
    (48, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Major Andean porphyry copper segments", "STATE_TARAPACA STATE_AREQUIPA STATE_SANTIAGO"),
    (36, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Large northern and central Andean copper provinces", "STATE_ECUADOR STATE_POTOSI STATE_CAJAMARCA STATE_PARA"),
    (24, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "Andean and Brazilian shield copper districts", "STATE_ANTIOQUIA STATE_CUNDINAMARCA STATE_CAUCA STATE_LA_PAZ STATE_LIMA STATE_ICA STATE_MINAS_GERAIS"),
    (16, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Secondary Andean, Patagonian and Brazilian copper potential", "STATE_BOLIVAR STATE_JUJUY STATE_TUCUMAN STATE_LOS_RIOS STATE_GOIAS STATE_MATO_GROSSO STATE_BAHIA"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized South American copper occurrences", "STATE_ZULIA STATE_MIRANDA STATE_ARAUCANIA STATE_RIO_GRANDE_DO_SUL"),
    (24, "HIGH", "HISTORIC_DISTRICT_AND_GLOBAL_ASSESSMENT", "Cyprus-type volcanogenic massive-sulfide copper province", "STATE_CYPRUS"),
    (24, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Iranian-Armenian-Tethyan porphyry copper belt", "STATE_TABRIZ STATE_ANKARA"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "Tethyan and Arabian Shield copper provinces", "STATE_OMAN STATE_KERMAN STATE_KHORASAN STATE_ISFAHAN STATE_HUDAVENDIGAR STATE_AYDIN STATE_KONYA STATE_KASTAMONU STATE_ADANA STATE_TRABZON STATE_ERZURUM STATE_KARS"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized Middle Eastern copper occurrences", "STATE_YEMEN STATE_HEDJAZ STATE_ALEPPO STATE_MAZANDARAN STATE_PERSIAN_KURDISTAN"),
    (36, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Tian Shan and Afghan porphyry copper provinces", "STATE_CENTRAL_HIGHLANDS"),
    (24, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "Caucasus, Central Asian and Himalayan copper districts", "STATE_ARMENIA STATE_UZBEKIA STATE_KABUL STATE_LHASA"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "Secondary Central Asian and Afghan metallogenic belts", "STATE_AZERBAIJAN STATE_GREATER_CAUCASUS STATE_TAJIKISTAN STATE_KIRGHIZIA STATE_HERAT STATE_BALKH STATE_PASHTUNISTAN STATE_NGARI"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized Caucasus, Turkmen or Himalayan copper occurrences", "STATE_DAGESTAN STATE_TURKMENIA STATE_HIMALAYAS"),
    (36, "HIGH", "NATIONAL_GEOLOGICAL_SURVEY", "Aravalli-Delhi copper belt of Rajasthan", "STATE_RAJPUTANA"),
    (24, "HIGH", "NATIONAL_GEOLOGICAL_SURVEY", "Indian shield copper belts including Malanjkhand and Singhbhum extensions", "STATE_MALWA STATE_CENTRAL_PROVINCES STATE_ORISSA STATE_KACHIN STATE_SHAN_STATES"),
    (16, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Secondary Indian shield and Burmese copper provinces", "STATE_BUNDELKHAND STATE_MYSORE STATE_HYDERABAD STATE_MANDALAY"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized South Asian copper occurrences", "STATE_GUJARAT STATE_KASHMIR STATE_KURNOOL STATE_BOMBAY STATE_ASSAM STATE_TENASSERIM"),
    (48, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Major Yunnan and Mongolian porphyry copper provinces", "STATE_YUNNAN STATE_URGA"),
    (36, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Tian Shan, Jiangxi and Mongolian copper provinces", "STATE_TIANSHAN STATE_JIANGXI STATE_ULIASTAI"),
    (24, "HIGH", "USGS_GLOBAL_COPPER_ASSESSMENT", "Chinese plateau and southwest polymetallic copper belts", "STATE_SICHUAN STATE_GUIZHOU STATE_GANSU STATE_QINGHAI STATE_HUNAN"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "Secondary Chinese and Indochinese copper districts", "STATE_DZUNGARIA STATE_SHAOZHOU STATE_GUANGXI STATE_SHENGJING STATE_CHONGQING STATE_WESTERN_HUBEI STATE_TONKIN STATE_LAOS"),
    (16, "HIGH", "VANILLA_HISTORY_AND_HISTORIC_DISTRICT", "Ashio and Besshi historic copper mines explicitly represented by vanilla", "STATE_KANTO STATE_SHIKOKU"),
    (8, "MEDIUM", "NATIONAL_GEOLOGICAL_SURVEY", "Localized Japanese and Korean copper districts", "STATE_TOHOKU STATE_HOKUSHINETSU STATE_KYUSHU STATE_BUSAN STATE_YANGHO STATE_FUJIAN"),
    (48, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Major Philippine and Bougainville porphyry copper provinces", "STATE_LUZON STATE_BOUGAINVILLE STATE_EASTERN_NEW_GUINEA"),
    (36, "HIGH", "USGS_GLOBAL_PORPHYRY_DATABASE", "Large southwest Pacific porphyry copper provinces", "STATE_MINDANAO STATE_WESTERN_NEW_GUINEA"),
    (24, "HIGH", "REGIONAL_GEOLOGICAL_SURVEY", "Indonesian and southwest Pacific magmatic-arc copper districts", "STATE_CELEBES STATE_KANAK"),
    (16, "MEDIUM", "USGS_GLOBAL_COPPER_ASSESSMENT", "Secondary Sunda, Borneo and Pacific island-arc copper systems", "STATE_WEST_BORNEO STATE_EAST_BORNEO STATE_MOLUCCAS STATE_SUNDA_ISLANDS STATE_SOLOMON_ISLANDS STATE_VANUATU STATE_FIJI"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized southeast Asian copper occurrences", "STATE_MALAYA STATE_NORTH_BORNEO STATE_NORTH_SUMATRA STATE_SOUTH_SUMATRA STATE_VISAYAS"),
    (60, "HIGH", "GEOSCIENCE_AUSTRALIA", "Olympic Dam province and South Australian copper districts", "STATE_SOUTH_AUSTRALIA"),
    (48, "HIGH", "GEOSCIENCE_AUSTRALIA", "Mount Isa and Queensland copper provinces", "STATE_QUEENSLAND"),
    (36, "HIGH", "GEOSCIENCE_AUSTRALIA", "Lachlan Orogen and Western Australian copper provinces", "STATE_NEW_SOUTH_WALES STATE_WESTERN_AUSTRALIA"),
    (24, "HIGH", "GEOSCIENCE_AUSTRALIA", "Northern Territory Proterozoic copper provinces", "STATE_NORTHERN_TERRITORY"),
    (16, "MEDIUM", "GEOSCIENCE_AUSTRALIA", "Secondary southeast Australian and New Zealand copper districts", "STATE_VICTORIA STATE_SOUTH_ISLAND"),
    (8, "MEDIUM", "GEOSCIENCE_AUSTRALIA", "Localized Tasmanian copper occurrences", "STATE_TASMANIA"),
    (36, "HIGH", "NATIONAL_SURVEY_AND_HISTORIC_DISTRICT", "Ural and Transbaikal copper-polymetallic provinces", "STATE_URAL STATE_TRANS_BAIKAL"),
    (24, "HIGH", "REGIONAL_GEOLOGICAL_SURVEY", "Altai-Sayan and Yenisei copper metallogenic belts", "STATE_TUVA STATE_UPPER_YENISEYSK"),
    (16, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Secondary Siberian copper districts", "STATE_TOMSK STATE_IRKUTSK"),
    (36, "HIGH", "NATIONAL_GEOLOGICAL_SURVEY", "Altai, Kazakh and southern Ural copper provinces", "STATE_CHELYABINSK STATE_ALTAI STATE_SEMIRECHE"),
    (24, "HIGH", "NATIONAL_GEOLOGICAL_SURVEY", "Russian, Kazakh and Caucasus copper-polymetallic districts", "STATE_PERM STATE_UFA STATE_AKTOBE STATE_JETISY STATE_FERGANA STATE_ELIZAVETPOL STATE_BURYATIA"),
    (16, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Secondary Fennoscandian, Kazakh and Far Eastern copper potential", "STATE_KUOPIO STATE_OULU STATE_AKMOLINSK STATE_SYRDARYA STATE_AMUR"),
    (8, "MEDIUM", "REGIONAL_GEOLOGICAL_SURVEY", "Localized Russian and Fennoscandian copper occurrences", "STATE_WEST_KARELIA STATE_EAST_KARELIA STATE_KHARKOV STATE_NORTH_CAUCASUS"),
]


def decode(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), bom


def encode(path: Path, text: str, bom: bool) -> None:
    raw = text.encode("utf-8")
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + raw)


def state_blocks(text: str) -> list[tuple[str, int, int]]:
    starts = list(re.finditer(r"(?m)^(STATE_[A-Z0-9_]+)\s*=\s*\{", text))
    blocks = []
    for match in starts:
        depth = 0
        end = None
        for pos in range(match.end() - 1, len(text)):
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    break
        if end is None:
            raise RuntimeError(f"Unclosed state block: {match.group(1)}")
        blocks.append((match.group(1), match.start(), end))
    return blocks


def insert_copper(text: str, start: int, end: int, value: int) -> str:
    block = text[start:end]
    if "building_copper_mine" in block:
        raise RuntimeError("Copper resource already present before TECH6C5B build")
    match = re.search(r"(?m)^([ \t]*)capped_resources\s*=\s*\{", block)
    if not match:
        raise RuntimeError("State with positive copper has no capped_resources block")
    open_pos = match.end() - 1
    depth = 0
    close_pos = None
    for pos in range(open_pos, len(block)):
        if block[pos] == "{":
            depth += 1
        elif block[pos] == "}":
            depth -= 1
            if depth == 0:
                close_pos = pos
                break
    if close_pos is None:
        raise RuntimeError("Unclosed capped_resources block")
    newline = "\r\n" if "\r\n" in text else "\n"
    close_line_start = block.rfind(newline, 0, close_pos) + len(newline)
    block_indent = match.group(1)
    insertion = f"{block_indent}    building_copper_mine = {value}{newline}{block_indent}"
    return text[: start + close_line_start] + insertion + text[start + close_pos :]


def main() -> None:
    reviewed: dict[str, dict[str, object]] = {}
    for potential, confidence, source, rationale, ids in GROUPS:
        for state_id in ids.split():
            if state_id in reviewed:
                raise RuntimeError(f"Duplicate classification: {state_id}")
            reviewed[state_id] = {
                "potential": potential,
                "tier": TIERS[potential],
                "reason": f"{state_id}: {rationale}.",
                "confidence": confidence,
                "source_category": source,
                "action": "ADD_CAPPED_RESOURCE",
            }

    states: list[tuple[str, Path]] = []
    file_cache: dict[Path, tuple[str, bool, list[tuple[str, int, int]]]] = {}
    for path in sorted(STATE_DIR.glob("*.txt")):
        text, bom = decode(path)
        # Make the build idempotent while preserving every non-copper resource.
        text = re.sub(r"(?m)^[ \t]*building_copper_mine\s*=\s*\d+[ \t]*(?:\r?\n)?", "", text)
        blocks = state_blocks(text)
        file_cache[path] = (text, bom, blocks)
        states.extend((state_id, path) for state_id, _, _ in blocks)

    ids = [state_id for state_id, _ in states]
    if len(ids) != 675 or len(set(ids)) != 675:
        raise RuntimeError(f"Expected 675 unique state regions, found {len(ids)} rows / {len(set(ids))} unique")
    unknown = sorted(set(reviewed) - set(ids))
    if unknown:
        raise RuntimeError(f"Classified state IDs absent from map: {unknown}")

    rows = []
    for state_id, path in states:
        decision = reviewed.get(state_id)
        if decision is None:
            decision = {
                "potential": 0,
                "tier": "NONE",
                "reason": f"{state_id}: global metallogenic screen found no copper province large enough for a separate game-scale potential.",
                "confidence": "MEDIUM",
                "source_category": "GLOBAL_ASSESSMENT_NEGATIVE_SCREEN",
                "action": "KEEP_ZERO",
            }
        rows.append({
            "state_id": state_id,
            "state_region_file": path.relative_to(ROOT).as_posix(),
            **decision,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=[
            "state_id", "state_region_file", "potential", "tier", "reason", "confidence", "source_category", "action"
        ])
        writer.writeheader()
        writer.writerows(rows)

    # Matrix is complete and validated before any map edit begins.
    for path, (text, bom, blocks) in file_cache.items():
        changes = [(start, end, int(reviewed[state_id]["potential"])) for state_id, start, end in blocks if state_id in reviewed]
        if not changes:
            continue
        for start, end, value in reversed(changes):
            text = insert_copper(text, start, end, value)
        encode(path, text, bom)

    counts = Counter(row["tier"] for row in rows)
    total = sum(int(row["potential"]) for row in rows)
    modified_files = len({path for state_id, path in states if state_id in reviewed})
    print(f"states={len(rows)} nonzero={len(reviewed)} zero={len(rows)-len(reviewed)} total={total} files={modified_files}")
    print("tiers=" + ",".join(f"{tier}:{counts[tier]}" for tier in TIERS.values()))


if __name__ == "__main__":
    main()
