"""Static validation for TECH6C6B phosphate implementation."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def fail(message: str) -> None:
    FAILURES.append(message)


def block(text: str, object_id: str) -> str:
    match = re.search(rf"(?m)^{re.escape(object_id)}\s*=\s*\{{", text)
    if not match:
        fail(f"missing block {object_id}")
        return ""
    depth = 0
    for pos in range(match.end() - 1, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[match.start() : pos + 1]
    fail(f"unclosed block {object_id}")
    return ""


def require(text: str, snippets: list[str], context: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            fail(f"{context}: missing {snippet!r}")


def forbid(text: str, snippets: list[str], context: str) -> None:
    for snippet in snippets:
        if snippet in text:
            fail(f"{context}: forbidden {snippet!r}")


def balanced(text: str, context: str) -> None:
    clean = re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
    clean = re.sub(r"(?m)#.*$", "", clean)
    if clean.count("{") != clean.count("}"):
        fail(f"{context}: unbalanced braces")


def validate_core() -> None:
    good = read("common/goods/15_tech6c6b_phosphates.txt")
    require(good, ['texture = "gfx/error_deer.dds"', "cost = 30", "category = industrial", "tradeable = yes"], "phosphates good")

    building = read("common/buildings/15_tech6c6b_phosphate_mine.txt")
    require(building, [
        "building_group = bg_mining", 'icon = "gfx/error_deer.dds"', "city_type = mine",
        "required_construction = construction_cost_medium", "terrain_manipulator = mining",
        "applied_mineralogy", "pmg_mining_equipment_building_phosphate_mine",
        "ownership_type = self", "ai_value = 1000",
    ], "phosphate mine")

    pmg = read("common/production_method_groups/15_tech6c6b_phosphate_pmgs.txt")
    require(pmg, ['texture = "gfx/error_deer.dds"', "pm_picks_and_shovels_building_phosphate_mine"], "phosphate PMG")
    if len(re.findall(r"(?m)^\s*pm_[a-z0-9_-]+\s*$", pmg)) != 1:
        fail("phosphate PMG must contain exactly one production method")

    pm = read("common/production_methods/15_tech6c6b_phosphate_extraction.txt")
    require(pm, [
        'texture = "gfx/error_deer.dds"', "state_pollution_generation_add = 5",
        "goods_input_tools_add = 5", "goods_output_phosphates_add = 25",
        "building_employment_shopkeepers_add = 500", "building_employment_laborers_add = 4500",
    ], "phosphate extraction PM")
    forbid(pm, ["unlocking_technologies", "goods_input_sulfur", "goods_input_iron", "goods_input_salt"], "phosphate extraction PM")

    modifiers = read("common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt")
    for key in ["goods_input_phosphates_add", "goods_input_phosphates_mult", "goods_output_phosphates_add", "goods_output_phosphates_mult"]:
        if len(re.findall(rf"(?m)^{key}\s*=", modifiers)) != 1:
            fail(f"modifier definition {key} must occur exactly once")

    icons = read("gui/tech6c_goods_texticons.gui")
    icon_block = block(icons.replace("texticon =", "TEXTICON ="), "TEXTICON")
    if icons.count("icon = phosphates") != 1 or 'texture = "gfx/error_deer.dds"' not in icons:
        fail("phosphates texticon missing or duplicated")

    for lang in ("english", "french"):
        base = read(f"localization/{lang}/tech6c6b_phosphates_l_{lang}.yml")
        mod = read(f"localization/{lang}/tech6c_goods_modifiers_l_{lang}.yml")
        for key in ["phosphates", "building_phosphate_mine", "pmg_mining_equipment_building_phosphate_mine", "pm_picks_and_shovels_building_phosphate_mine"]:
            if not re.search(rf"(?m)^\s*{re.escape(key)}:0\s+", base):
                fail(f"{lang} localization missing {key}")
        for key in [
            "modifier_goods_input_phosphates_add", "modifier_goods_input_phosphates_mult",
            "modifier_goods_output_phosphates_add", "modifier_goods_output_phosphates_mult",
            "goods_input_phosphates_add", "goods_input_phosphates_mult",
            "goods_output_phosphates_add", "goods_output_phosphates_mult",
        ]:
            if not re.search(rf"(?m)^\s*{re.escape(key)}:0\s+", mod):
                fail(f"{lang} modifier localization missing {key}")

    for rel in [
        "common/goods/15_tech6c6b_phosphates.txt",
        "common/buildings/15_tech6c6b_phosphate_mine.txt",
        "common/production_method_groups/15_tech6c6b_phosphate_pmgs.txt",
        "common/production_methods/15_tech6c6b_phosphate_extraction.txt",
    ]:
        balanced(read(rel), rel)


def validate_fertilizer() -> None:
    industry = read("common/production_methods/01_industry.txt")
    basic = block(industry, "pm_artificial_fertilizers")
    improved = block(industry, "pm_improved_fertilizer")
    nitrogen = block(industry, "pm_nitrogen_fixation")

    require(basic, [
        "state_pollution_generation_add = 10", "goods_input_phosphates_add = 20",
        "goods_input_industrial_chemicals_add = 20", "goods_input_coal_add = 10",
        "goods_output_fertilizer_add = 80", "building_employment_shopkeepers_add = 500",
        "building_employment_laborers_add = 3000", "building_employment_machinists_add = 1000",
        "building_employment_engineers_add = 500",
    ], "basic phosphate fertilizer")
    forbid(basic, ["goods_input_sulfur_add", "goods_input_iron_add", "goods_input_salt_add", "unlocking_technologies"], "basic phosphate fertilizer")

    require(improved, [
        "state_pollution_generation_add = 15", "improved_fertilizer",
        "goods_input_phosphates_add = 30", "goods_input_industrial_chemicals_add = 25",
        "goods_input_coal_add = 15", "goods_output_fertilizer_add = 120",
        "building_employment_shopkeepers_add = 500", "building_employment_laborers_add = 2000",
        "building_employment_machinists_add = 1500", "building_employment_engineers_add = 1000",
    ], "improved phosphate fertilizer")
    forbid(improved, ["goods_input_sulfur_add", "goods_input_iron_add", "goods_input_salt_add"], "improved phosphate fertilizer")

    require(nitrogen, [
        "state_pollution_generation_add = 15", "nitrogen_fixation", "goods_input_sulfur_add = 40",
        "goods_input_industrial_chemicals_add = 20", "goods_input_iron_add = 30",
        "goods_input_salt_add = 20", "goods_output_fertilizer_add = 200",
        "building_employment_shopkeepers_add = 500", "building_employment_laborers_add = 1000",
        "building_employment_machinists_add = 2000", "building_employment_engineers_add = 1500",
    ], "frozen nitrogen fixation")
    forbid(nitrogen, ["goods_input_phosphates_add", "goods_input_nitrates_add"], "frozen nitrogen fixation")


def parse_state_blocks(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for match in re.finditer(r"(?m)^(STATE_[A-Z0-9_]+)\s*=\s*\{", text):
        depth = 0
        for pos in range(match.end() - 1, len(text)):
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    result[match.group(1)] = text[match.start() : pos + 1]
                    break
    return result


def validate_distribution() -> None:
    matrix_path = ROOT / "docs/reports/industry/TECH6C6B_PHOSPHATE_GLOBAL_RESOURCE_MATRIX.csv"
    with matrix_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 675 or len({r["state_id"] for r in rows}) != 675:
        fail("resource matrix must contain 675 unique states")
        return
    positives = {r["state_id"]: int(r["final_potential"]) for r in rows if int(r["final_potential"]) > 0}
    if len(positives) != 40 or sum(positives.values()) != 1216:
        fail("resource totals must be 40 states and 1216 potential")
    preliminary = [r for r in rows if int(r["preliminary_potential"]) > 0]
    if len(preliminary) != 45 or any(not r["revalidation_result"] for r in preliminary):
        fail("all 45 preliminary candidates must have a revalidation result")
    expected_changes = {
        "STATE_SINAI": 0, "STATE_ALGIERS": 0, "STATE_CAJAMARCA": 24,
        "STATE_NEJD": 0, "STATE_WESTERN_AUSTRALIA": 0, "STATE_WEST_KARELIA": 0,
    }
    for state, final in expected_changes.items():
        row = next(r for r in rows if r["state_id"] == state)
        if int(row["final_potential"]) != final:
            fail(f"reviewed exception mismatch for {state}")

    actual: dict[str, int] = {}
    for path in sorted((ROOT / "map_data/state_regions").glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig")
        balanced(text, path.name)
        for state_id, state_block in parse_state_blocks(text).items():
            matches = re.findall(r"(?m)^\s*building_phosphate_mine\s*=\s*(\d+)\s*$", state_block)
            if len(matches) > 1:
                fail(f"duplicate phosphate resource in {state_id}")
            if matches:
                actual[state_id] = int(matches[0])
    if actual != positives:
        fail(f"map phosphate entries differ from matrix: expected {len(positives)}, actual {len(actual)}")
    print("resource tiers:", dict(Counter(r["final_tier"] for r in rows)))


def validate_scope_and_csv() -> None:
    common_text = "\n".join(p.read_text(encoding="utf-8-sig", errors="replace") for p in (ROOT / "common").rglob("*.txt"))
    if re.search(r"(?m)^nitrates\s*=\s*\{", common_text):
        fail("nitrates good was created inside TECH6C6B")
    if re.search(r"(?m)^building_nitrate_mine\s*=\s*\{", common_text):
        fail("nitrate mine was created inside TECH6C6B")
    if re.search(r"(?m)^guano\s*=\s*\{", common_text):
        fail("guano good was created inside TECH6C6B")
    tech_text = "\n".join(p.read_text(encoding="utf-8-sig", errors="replace") for p in (ROOT / "common/technology").rglob("*.txt"))
    forbid(tech_text, ["phosphates", "building_phosphate_mine"], "technology freeze")
    history_text = "\n".join(p.read_text(encoding="utf-8-sig", errors="replace") for p in (ROOT / "common/history").rglob("*.txt"))
    forbid(history_text, ["building_phosphate_mine", "goods_input_phosphates"], "starting setup freeze")

    expectations = {
        "TECH6C6B_FERTILIZER_ECONOMIC_VALIDATION.csv": 15,
        "TECH6C6B_PHOSPHATE_CONSUMER_IMPLEMENTATION_MATRIX.csv": 12,
    }
    for name, count in expectations.items():
        with (ROOT / "docs/reports/industry" / name).open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        if len(rows) != count:
            fail(f"{name}: expected {count} rows, found {len(rows)}")
        if not rows or any(None in row for row in rows):
            fail(f"{name}: malformed CSV row")


def main() -> int:
    validate_core()
    validate_fertilizer()
    validate_distribution()
    validate_scope_and_csv()
    if FAILURES:
        print("TECH6C6B VALIDATION: FAIL")
        for item in FAILURES:
            print(" -", item)
        return 1
    print("TECH6C6B VALIDATION: PASS")
    print("goods=1 buildings=1 pmgs=1 extraction_pms=1 fertilizer_pms_changed=2")
    print("starting_technology_distribution=UNCHANGED_AND_DEFERRED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
