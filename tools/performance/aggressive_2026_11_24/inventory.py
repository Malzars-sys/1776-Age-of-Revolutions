"""Read the effective 1776 cultures, territorial states and native POP records."""
import argparse
from collections import Counter, defaultdict
import csv
import json
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path.cwd() / "tools/performance"))
from simperf56_save_state import child, num, records, sections
from validate_diplomacy_ottoman_1776 import parse, walk

STEAM = Path("C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game")
BASE = Path(os.environ.get("AOR56_FROZEN_BASE", Path.cwd())).resolve()


def objects(folder, mod):
    paths = {p.name: p for p in (STEAM / folder).glob("*.txt")}
    for layer in dict.fromkeys((BASE, mod)):
        paths.update({p.name: p for p in (layer / folder).glob("*.txt")})
    return {node.key: node for name in sorted(paths)
            for node in parse(paths[name].read_text(encoding="utf-8-sig")) if node.key}


def atom(node, key, default=""):
    return str(node.one(key, default)).strip('"')


def values(node):
    return [str(n.value).strip('"') for n in node.children() if not isinstance(n.value, list)] if node else []


def population(stats):
    return round(sum(num(stats, "population_" + group + "_strata")
                     for group in ("upper", "middle", "lower"))) if stats else 0


def gdp_sample(country):
    gdp = child(country, "gdp")
    channels = child(gdp, "channels") if gdp else None
    for channel in channels.children() if channels else []:
        samples = values(child(channel, "values"))
        if samples:
            return float(samples[-1])
    return None


def write_csv(path, rows):
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def inspect(save, output, mod):
    raw = save.read_text(encoding="utf-8-sig")
    spans = sections(raw)
    countries = dict(records(raw, spans["country_manager"]))
    states = dict(records(raw, spans["states"]))
    states_by_owner = defaultdict(list)
    for ident, state in states.items():
        if state.one("country") is not None:
            states_by_owner[atom(state, "country")].append(state)
    controllers = {atom(obj, "country"): atom(obj, "enabled")
                   for _, obj in records(raw, spans["ai"]) if obj.one("country") is not None}
    region_by_state = {state: region for region, node in objects("common/strategic_regions", mod).items()
                       for state in values(child(node, "states"))}
    names = {}
    for folder in (layer / "localization/french" for layer in dict.fromkeys((STEAM, BASE, mod))):
        for path in sorted(folder.rglob("*.yml")):
            names.update(re.findall(r'(?m)^\s+([A-Z0-9]{3,}):(?:\d+)?\s+"([^"]+)"',
                                    path.read_text(encoding="utf-8-sig", errors="replace")))
    pacts_by_target = defaultdict(set)
    for _, pact in records(raw, spans["pacts"]):
        targets = child(pact, "targets")
        if targets:
            pacts_by_target[atom(targets, "second")].add(atom(pact, "action"))
    country_rows = []
    for ident, country in countries.items():
        owned = states_by_owner[ident]
        if ident not in controllers and (country.one("dead") == "yes" or not owned):
            continue
        tag = atom(country, "definition")
        capital = states.get(atom(country, "capital"))
        owned_regions = {atom(state, "region") for state in owned}
        provinces = 0
        for state in owned:
            packed = child(state, "provinces")
            if packed:
                runs = [int(value) for value in values(child(packed, "provinces"))]
                assert len(runs) % 2 == 0 and all(n >= 0 for n in runs)
                provinces += sum(length + 1 for length in runs[1::2])
        country_rows.append(dict(tag=tag, name=names.get(tag, tag), country_id=ident,
            controller=controllers.get(ident, ""), population=population(child(country, "pop_statistics")),
            province_count=provinces, state_fragments=len(owned),
            capital_region=region_by_state.get(atom(capital, "region"), "") if capital else "",
            regions=" ".join(sorted({region_by_state.get(s, "") for s in owned_regions} - {""})),
            state_regions=" ".join(sorted(owned_regions)), country_type=atom(country, "country_type"),
            incoming_pacts=" ".join(sorted(pacts_by_target[ident])), recorded_gdp=gdp_sample(country)))
    definitions = objects("common/cultures", mod)
    culture_ids = {i: atom(obj, "type") for i, obj in records(raw, spans["cultures"])}
    observed = Counter()
    attributes = Counter()
    groups = set()
    workplaces = set()
    for _, pop in records(raw, spans["pops"]):
        if pop.one("type") is not None:
            culture = culture_ids[atom(pop, "culture")]
            observed[culture] += 1
            attributes.update(n.key for n in pop.children())
            identity = culture, atom(pop, "religion"), atom(pop, "type"), atom(pop, "location")
            groups.add(identity)
            workplaces.add(identity + (atom(pop, "workplace"),))
    source_sizes = Counter()
    source_rows = Counter()
    source_fields = Counter()
    candidates = {}
    for layer in dict.fromkeys((STEAM, BASE, mod)):
        candidates.update({p.name: p for p in (layer / "common/history/pops").glob("*.txt")})
    for path in candidates.values():
        for node in walk(parse(path.read_text(encoding="utf-8-sig"))):
            if node.key == "create_pop":
                key = atom(node, "culture")
                source_rows[key] += 1
                source_sizes[key] += int(atom(node, "size"))
                source_fields.update(n.key for n in node.children())
    culture_rows = []
    for key in sorted(definitions.keys() | observed.keys() | source_rows.keys()):
        definition = definitions.get(key)
        fields = {field: atom(definition, field) if definition else ""
                  for field in ("language", "heritage", "religion")}
        culture_rows.append(dict(culture=key, **fields, history_entries=source_rows[key],
            history_population=source_sizes[key], serialized_pops=observed[key]))
    output.mkdir(parents=True)
    write_csv(output / "COUNTRIES.csv", sorted(country_rows, key=lambda row: row["tag"]))
    write_csv(output / "CULTURES.csv", culture_rows)
    metrics = dict(date=re.search(r'\bgame_date=([\d.]+)', raw[:4096])[1],
        country_rows=len(country_rows), controllers=Counter(controllers.values()),
        total_population=sum(r["population"] for r in country_rows),
        state_population=sum(population(child(state, "pop_statistics")) for state in states.values()),
        culture_definitions=len(definitions), runtime_registered_cultures=len(culture_ids), represented_cultures=len(observed),
        runtime_pops=sum(observed.values()), history_pop_entries=sum(source_rows.values()),
        history_total=sum(source_sizes.values()), province_count=sum(r["province_count"] for r in country_rows),
        possible_pop_groups_by_type_culture_religion_location=len(groups),
        same_key_including_workplace=len(workplaces),
        pop_fields=attributes, history_fields=source_fields)
    (output / "METRICS.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics))


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("save", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument("--mod", type=Path, default=BASE)
    args = cli.parse_args()
    inspect(args.save, args.output, args.mod)




