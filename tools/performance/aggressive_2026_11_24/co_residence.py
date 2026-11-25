"""Screen actual colocated POPs for candidate cultural consolidation."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import json
import sys

from consolidate import replacements
from inventory import BASE, atom, objects, records, sections


def projection(save):
    raw = save.read_text(encoding="utf-8-sig")
    spans = sections(raw)
    declared = objects("common/cultures", BASE)
    cultures = {ident: atom(pop, "type") for ident, pop in records(raw, spans["cultures"])}
    state_ids = {ident for ident, _ in records(raw, spans["states"])}
    mapping = replacements()
    groups = defaultdict(Counter)
    locations = Counter()
    total = 0
    for _, pop in records(raw, spans["pops"]):
        if pop.one("type") is not None:
            culture = cultures[atom(pop, "culture")]
            loc = atom(pop, "location")
            identity = loc, atom(pop, "workplace"), atom(pop, "type"), atom(pop, "religion")
            groups[identity][culture] += 1
            locations.update([loc])
            total += 1
    coexist = Counter()
    conservative = Counter()
    loss = 0
    for counter in groups.values():
        loss += len(counter) - len({mapping.get(key, key) for key in counter})
        for a, b in combinations(sorted(counter), 2):
            left, right = declared.get(a), declared.get(b)
            if not left or not right:
                continue
            mix = (a, b)
            coexist[mix] += 1
            shared = [key for key in ("language", "heritage") if atom(left, key) and atom(left, key) == atom(right, key)]
            if shared and a not in mapping and b not in mapping:
                conservative[mix] += 1
    return dict(runtime_pops=total, states_known=sum(count for key,count in locations.items() if key in state_ids),
                near_duplicate_pop_keys=sum(len(counter) for counter in groups.values()), placed_clusters=len(groups),
                mapping_39_projected_key_reduction=loss, top_pair_same_language_or_heritage=conservative.most_common(75),
                top_pair_any=coexist.most_common(30))


if __name__ == "__main__":
    from sys import argv
    with Path(argv[2]).open("x", encoding="utf-8") as stream:
        json.dump(projection(Path(argv[1])), stream, indent=2)
