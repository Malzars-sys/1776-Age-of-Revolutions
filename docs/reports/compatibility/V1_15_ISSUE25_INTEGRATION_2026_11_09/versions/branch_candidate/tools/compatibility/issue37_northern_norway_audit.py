"""Read-only bounded province audit for issue #37; not an engine pathfinding test.

Compare the installed mod with an exact pre-edit map-file backup. Outputs JSON.
Requires the sibling journal audit's field reader, Pillow and NumPy.
"""
import argparse
from collections import defaultdict, deque
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from issue27_journal_outcomes_audit import fields

STATE = "STATE_NORTHERN_NORWAY"
REL = Path("map_data/state_regions/00_west_europe.txt")
TARGETS = frozenset(("x2495FE", "xFEC50D", "x7005BB", "x6480A4"))
RGB = re.compile(r"x[0-9A-Fa-f]{6}")


def one(items, key):
    matches = [f for f in items if f.key == key]
    if len(matches) != 1:
        raise ValueError("Expected exactly one field: " + key)
    return matches[0]


def colors(field):
    return RGB.findall(field.body)


def correction(text):
    """Compute the sole authorized edit, without writing anything."""
    state = one(fields(text), STATE)
    impassable = one(fields(state.body), "impassable")
    if not TARGETS.issubset(colors(impassable)):
        raise ValueError("Expected all four original impassable provinces")
    result = impassable.value
    for province in sorted(TARGETS):
        result, count = re.subn('"' + province + r'"[ \t]*', "", result)
        if count != 1:
            raise ValueError("Province must occur exactly once: " + province)
    new_state = state.value.replace(impassable.value, result, 1)
    if text.count(state.value) != 1:
        raise ValueError("Ambiguous state source span")
    return text.replace(state.value, new_state, 1)


def effective_files(mod, vanilla, folder):
    files = {p.name: p for p in (vanilla / folder).glob("*.txt")}
    files.update({p.name: p for p in (mod / folder).glob("*.txt")})
    return [files[name] for name in sorted(files)]


def audit(mod, vanilla, before_file):
    import numpy as np
    from PIL import Image

    before_bytes, after_bytes = before_file.read_bytes(), (mod / REL).read_bytes()
    before, after = before_bytes.decode("utf-8"), after_bytes.decode("utf-8")
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    check(after == correction(before), "Changes exceed the four authorized flag removals")
    prior = one(fields(one(fields(before), STATE).body), "impassable")
    current_state = one(fields(after), STATE)
    current = one(fields(current_state.body), "impassable")
    provinces = colors(one(fields(current_state.body), "provinces"))
    check(len(provinces) == len(set(provinces)) == 133, "Unexpected province membership")
    check(set(colors(prior)) - set(colors(current)) == TARGETS, "Wrong provinces unblocked")
    check(len(colors(prior)) == 37 and len(colors(current)) == 33, "Other impassable flags changed")

    ownership = defaultdict(set)
    for path in effective_files(mod, vanilla, Path("common/history/states")):
        for top in fields(path.read_text(encoding="utf-8-sig")):
            if not top.block:
                continue
            for state in fields(top.body):
                if state.key != "s:" + STATE:
                    continue
                for entry in fields(state.body):
                    if entry.key == "create_state":
                        fs = fields(entry.body)
                        ownership[one(fs, "country").value].update(colors(one(fs, "owned_provinces")))
    check(ownership["c:RUS"] == TARGETS, "Russian ownership differs from the bounded four provinces")
    check(len(ownership["c:DENNOR"]) == 129, "Danish-Norwegian ownership changed")
    check(ownership["c:RUS"].isdisjoint(ownership["c:DENNOR"]), "Duplicate ownership")
    check(set().union(*ownership.values()) == set(provinces), "Missing ownership")

    membership, blocked, region_sources = {}, set(), []
    for path in effective_files(mod, vanilla, Path("map_data/state_regions")):
        for state in fields(path.read_text(encoding="utf-8-sig")):
            if not state.block:
                continue
            fs = fields(state.body)
            if not any(f.key == "provinces" for f in fs):
                continue
            for province in colors(one(fs, "provinces")):
                if province in TARGETS:
                    check(province not in membership, "Duplicate target state assignment")
                membership[province] = state.key
            for f in fs:
                if f.key == "impassable":
                    blocked.update(colors(f))
    for path in effective_files(mod, vanilla, Path("common/strategic_regions")):
        for region in fields(path.read_text(encoding="utf-8-sig")):
            if region.block and any(f.key == "states" and STATE in f.body.split() for f in fields(region.body)):
                region_sources.append(region.key)
    check(region_sources == ["region_northern_europe"], "Unexpected strategic-region assignment")

    # Read a bounded northern crop; this checks shared pixel edges, not engine routes.
    box = (4350, 100, 5050, 490)
    Image.MAX_IMAGE_PIXELS = None
    raster = np.array(Image.open(mod / "map_data/provinces.png").convert("RGB").crop(box), dtype=np.uint32)
    canonical = np.array(Image.open(vanilla / "map_data/provinces.png").convert("RGB").crop(box), dtype=np.uint32)
    packed = (raster[:, :, 0] << 16) | (raster[:, :, 1] << 8) | raster[:, :, 2]
    numeric = lambda color: int(color[1:], 16)
    target_mask = np.isin(packed, [numeric(p) for p in TARGETS])
    check(np.array_equal(raster[target_mask], canonical[target_mask]), "Target pixels differ from vanilla")
    edges = defaultdict(set)
    for a, b in ((packed[:, :-1], packed[:, 1:]), (packed[:-1, :], packed[1:, :])):
        changed = a != b
        for left, right in np.unique(np.stack((a[changed], b[changed]), axis=1), axis=0):
            left, right = "x%06X" % left, "x%06X" % right
            edges[left].add(right)
            edges[right].add(left)
    rows = []
    for province in sorted(TARGETS):
        ys, xs = np.where(packed == numeric(province))
        check(len(xs) > 0, "Target absent from bounded raster crop: " + province)
        todo, seen = deque([province]), {province}
        while todo:
            for neighbor in edges[todo.popleft()]:
                if neighbor in seen or neighbor in blocked or neighbor not in membership:
                    continue
                if membership[neighbor].endswith("_SEA") or "OCEAN" in membership[neighbor]:
                    continue
                seen.add(neighbor)
                todo.append(neighbor)
        reaches_kola = any(membership.get(p) == "STATE_KOLA" for p in seen)
        check(reaches_kola, "No passable raster-edge path to Kola: " + province)
        rows.append({"province": province, "pixels": len(xs),
                     "bbox": [int(xs.min()) + box[0], int(ys.min()) + box[1],
                              int(xs.max()) + box[0], int(ys.max()) + box[1]],
                     "state": membership.get(province), "owner": "c:RUS",
                     "impassable_before": province in colors(prior),
                     "impassable_after": province in blocked,
                     "raster_edge_path_to_kola": reaches_kola})
    return {"status": "PASS_STATIC_ONLY" if not errors else "FAIL_STATIC", "runtime_tested": False,
            "file": REL.as_posix(), "state": STATE, "provinces": rows,
            "impassable_before": len(colors(prior)), "impassable_after": len(colors(current)),
            "russian_passable_before": 0, "russian_passable_after": len(TARGETS - blocked),
            "danish_norwegian_passable": len(ownership["c:DENNOR"] - blocked),
            "strategic_region": region_sources, "only_authorized_edit": after == correction(before),
            "before_sha256": hashlib.sha256(before_bytes).hexdigest(),
            "after_sha256": hashlib.sha256(after_bytes).hexdigest(), "errors": errors,
            "limits": ["Pixel adjacency does not validate engine pathfinding, access rights, front generation or UI.",
                       "Inherited flags conflict with the mod's Russian split; introduction in 1.15 is not proven."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod-root", type=Path, required=True)
    parser.add_argument("--vanilla-root", type=Path, required=True)
    parser.add_argument("--before-file", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.mod_root, args.vanilla_root, args.before_file)
    print(json.dumps(result, indent=2))
    return bool(result["errors"])


if __name__ == "__main__":
    sys.exit(main())
