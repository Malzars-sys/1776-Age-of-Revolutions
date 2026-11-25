"""Read country activity from an isolated Victoria 3 native text save."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simperf56_save_state import child, num, records, sections


def items(node, group):
    return node.children(group) if node is not None else []


def sum_values(node, group):
    return sum(float(field.value) for block in items(node, group) for field in block.children())


def queued(country, name):
    return sum(order.one("type") is not None for queue in country.children(name)
               for elements in queue.children("construction_elements") for order in elements.children())


def inspect(path, tags):
    text = path.read_text(encoding="utf-8-sig")
    spans = sections(text)
    country_ids = {}
    snapshot = {}
    for ident, country in records(text, spans["country_manager"]):
        tag = str(country.one("definition", "")).strip('"')
        if tag not in tags or country.one("dead") == "yes":
            continue
        budget = child(country, "budget")
        buildings = child(budget, "country_building_budget") if budget else None
        incomes = child(buildings, "incomes") if buildings else None
        expenses = child(buildings, "expenses") if buildings else None
        pop = child(country, "pop_statistics")
        country_ids[ident] = tag
        snapshot[tag] = {
            "country_id": ident,
            "country_type": country.one("country_type"),
            "government": country.one("government"),
            "market": country.one("market"),
            "treasury": num(budget, "money") if budget else None,
            "weekly_income": sum_values(budget, "weekly_income") if budget else None,
            "weekly_expense": sum_values(budget, "weekly_expenses") if budget else None,
            "building_taxes": {key: sum(sum_values(source, "values") for source in items(incomes, key))
                               for key in ("income_taxes", "poll_taxes", "dividends_taxes")},
            "military_expenses": sum(sum(sum_values(source, "values") for source in items(expenses, key))
                                     for key in ("military_goods", "military_slaves", "military_wages")),
            "population": round(sum(num(pop, f"population_{stratum}_strata") for stratum in
                                    ("upper", "middle", "lower"))) if pop else None,
            "private_queue": queued(country, "private_queue"),
            "government_queue": queued(country, "government_queue"),
        }

    states = {ident: node.one("country") for ident, node in records(text, spans["states"])
              if node.one("country") in country_ids}
    counts = defaultdict(Counter)
    for _, building in records(text, spans["building_manager"]):
        ident = states.get(building.one("state"))
        if ident is None:
            continue
        counts[ident]["building_records"] += 1
        counts[ident]["building_levels"] += num(building, "levels")
        counts[ident]["active_buildings"] += building.one("active") == "yes"
        output = child(building, "output_goods")
        goods = child(output, "goods") if output else None
        counts[ident]["producing_buildings"] += bool(goods and any(num(good, "value") > 0 for good in goods.children()))

    journals = defaultdict(list)
    for manager, key in (("military_formation_manager", "formations"),
                         ("new_combat_unit_manager", "units"),
                         ("journal_entry_manager", "journal_entries"), ("ai", "controller")):
        for _, entry in records(text, spans[manager]):
            ident = entry.one("country")
            if ident not in country_ids:
                continue
            if key == "controller":
                snapshot[country_ids[ident]][key] = entry.one("enabled")
                continue
            counts[ident][key] += 1
            if key == "journal_entries":
                journals[ident].append(entry.one("type"))
            if key == "units":
                counts[ident]["manpower"] += num(entry, "current_manpower")

    for ident, tag in country_ids.items():
        snapshot[tag].update({field: counts[ident][field] for field in (
            "building_records", "building_levels", "active_buildings", "producing_buildings", "formations", "units", "manpower",
        )})
        snapshot[tag]["journal_entries"] = sorted(set(journals[ident]))
    return {"save": path.name, "countries": snapshot, "absent": sorted(tags - snapshot.keys())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("tags", nargs="+")
    args = parser.parse_args()
    result = inspect(args.save, set(args.tags))
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)


if __name__ == "__main__":
    main()
