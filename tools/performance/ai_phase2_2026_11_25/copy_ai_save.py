"""Prepare a separate solo Victoria 3 starting save for the country AI experiment."""

import argparse
from collections import Counter
import csv
from copy import copy
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
from zipfile import ZipFile


TOOLS = Path(__file__).resolve().parents[1]
DATA = TOOLS.parents[1] / "docs/reports/performance/AGGRESSIVE_2026_11_24"
sys.path.insert(0, str(TOOLS))
from simperf56_ai_cohorts import db_chunks
from simperf56_save_state import records, sections, parse


# Signature of the fields verified against the native 1.15.2 text and binary saves.
BINARY_CONTROLLER = re.compile(
    rb"\x01\x00\x03\x00\x40\x28\x01\x00\x14\x00(....)"
    rb"\x05\x03\x01\x00\x0e\x00([\x00\x01])", re.S,
)
BINARY_COUNTRY = re.compile(
    rb"\x14\x00(....)\x01\x00\x03\x00(?:\x8b\x53\x01\x00\x0e\x00[\x00\x01])?"
    rb"\xdd\x07\x01\x00\x0f\x00([\x03-\x08])\x00", re.S,
)
BINARY_PLAYER_START = bytes.fromhex("415901000300ab050100030014000000000001000300e20001000f00")
BINARY_PLAYER_COUNTRY = re.compile(rb"\x40\x28\x01\x00\x14\x00(....)\x04\x00\x04\x00\x04\x00", re.S)
BINARY_START_META = bytes.fromhex("ad55010003008f0501000c004accfd6aee0001000f000600312e31352e32453201000c0040ba8903")
BINARY_SOLO_META = bytes.fromhex("c10501000e00000d5801000c00010000000400")
COHORTS = ("B", "C", "D", "E", "F")
# Preserve autonomous actors in the Hungarian revolution and Chinese unification.
REFINED_EXCEPTIONS = {"TRS", "XIN"}


def cohort(name):
    thresholds = {"B": "100000", "C": "250000", "D": "500000", "E": "500000", "F": "500000"}
    definitions = json.loads((DATA / "COHORTES.json").read_text(encoding="utf-8-sig"))
    tags = {entry["tag"] for entry in definitions[thresholds[name]]["affected"]}
    if name in {"E", "F"}:
        with (DATA / "INVENTAIRE_PAYS.csv").open(encoding="utf-8-sig", newline="") as stream:
            types = {row["tag"]: row["country_type"] for row in csv.DictReader(stream)}
        tags = {tag for tag in tags if types[tag] != "decentralized"}
    if name == "F":
        tags.difference_update(REFINED_EXCEPTIONS)
    return tags


def prepare_text(raw, requested):
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    source = raw.decode("utf-8-sig")
    if not re.match(r"SAV[0-9a-fA-F]+\r?\nmeta_data=\{", source) or not source.startswith("SAV0100"):
        raise ValueError("Expected a native, uncompressed Victoria 3 text save.")
    spans = sections(source)
    meta_start, meta_end = spans["meta_data"]
    meta = parse(source[meta_start:meta_end])[0]
    if (meta.one("version", "").strip('"'), meta.one("game_date"), meta.one("ironman"),
            meta.one("number_of_players")) != ("1.15.2", "1776.1.1", "no", "1"):
        raise ValueError("Expected a non-Ironman, solo 1776 start from Victoria 3 1.15.2.")

    tags_by_id = {ident: str(country.one("definition", "")).strip('"')
                  for ident, country in records(source, spans["country_manager"])}
    humans = [entry.one("country") for _, entry in records(source, spans["player_manager"])
              if entry.one("country") is not None]
    if len(humans) != 1 or not tags_by_id.get(humans[0]):
        raise ValueError("Could not identify the single player country in the save.")
    player_tag = tags_by_id[humans[0]]

    flags = Counter()
    countries_seen = set()
    affected = set()
    edits = []
    for _, start, _, controller in db_chunks(source, spans["ai"]):
        ident = controller.one("country")
        tag = tags_by_id.get(ident)
        fields = controller.children("enabled")
        if not tag or tag in countries_seen or len(fields) != 1 or fields[0].value not in {"yes", "no"}:
            raise ValueError("Unexpected native AI controller layout.")
        countries_seen.add(tag)
        flag = fields[0]
        flags[flag.value] += 1
        if ident == humans[0] and flag.value != "yes":
            raise ValueError("Player country's controller already has a nonstandard state.")
        if tag == player_tag or tag not in requested:
            continue
        a, b = start + flag.start, start + flag.end
        if source[a:b] != "enabled=yes":
            raise ValueError(f"Expected an enabled controller for {tag}.")
        edits.append((a, b))
        affected.add(tag)
    if flags != {"yes": 646} or affected != requested - {player_tag}:
        raise ValueError("The save does not match the original 1776 cohort inventory.")

    chunks = []
    original = []
    previous = 0
    for start, end in edits:
        unchanged = source[previous:start]
        chunks.extend((unchanged, "enabled=no"))
        original.extend((unchanged, "enabled=yes"))
        previous = end
    chunks.append(source[previous:])
    original.append(source[previous:])
    if bom + "".join(original).encode("utf-8") != raw:
        raise ValueError("The field edits did not reproduce the original save when reverted.")
    saved = bom + "".join(chunks).encode("utf-8")
    if len(raw) - len(saved) != len(affected):
        raise ValueError("Unexpected output size for the planned controller edits.")
    return saved, {"format": "text", "played_country": player_tag, "disabled": sorted(affected),
                   "before": flags["yes"], "after": flags["yes"] - len(affected)}


def prepare_binary(raw, requested):
    header, end_of_header, compressed = raw.partition(b"\n")
    if (not re.fullmatch(rb"SAV0105[0-9a-f]{8}00000000", header)
            or end_of_header != b"\n" or not compressed.startswith(b"PK\x03\x04")):
        raise ValueError("Unrecognized compressed Victoria 3 save envelope.")
    with ZipFile(BytesIO(compressed)) as archive:
        if sorted(archive.namelist()) != ["gamestate", "meta"]:
            raise ValueError("Unexpected compressed save members.")
        members = archive.infolist()
        state = archive.read("gamestate")
        meta = archive.read("meta")
    if not (meta.startswith(BINARY_START_META) and meta.endswith(BINARY_SOLO_META) and state.startswith(meta)):
        raise ValueError("Expected a non-Ironman, solo 1776 start from Victoria 3 1.15.2.")

    controllers = list(BINARY_CONTROLLER.finditer(state))
    flags = {int.from_bytes(match[1], "little"): match.start(2) for match in controllers}
    if len(controllers) != 646 or len(flags) != 646 or any(state[offset] != 1 for offset in flags.values()):
        raise ValueError("The original 646 enabled controllers could not all be identified.")

    tags_by_id = {}
    for match in BINARY_COUNTRY.finditer(state):
        ident = int.from_bytes(match[1], "little")
        if ident not in flags:
            continue
        tag = state[match.end():match.end() + match[2][0]]
        if ident in tags_by_id or not re.fullmatch(rb"[A-Z][A-Z0-9]{2,7}", tag):
            raise ValueError("Unexpected country definition in the compressed save.")
        tags_by_id[ident] = tag.decode("ascii")
    if set(tags_by_id) != set(flags) or len(set(tags_by_id.values())) != 646 or not requested <= set(tags_by_id.values()):
        raise ValueError("The country definitions do not match the original cohort inventory.")

    if state.count(BINARY_PLAYER_START) != 1:
        raise ValueError("The single player record could not be identified.")
    start = state.index(BINARY_PLAYER_START) + len(BINARY_PLAYER_START)
    user_length = int.from_bytes(state[start:start + 2], "little")
    played = BINARY_PLAYER_COUNTRY.match(state, start + 2 + user_length)
    if played is None or int.from_bytes(played[1], "little") not in tags_by_id:
        raise ValueError("The single player's country could not be identified.")
    player_id = int.from_bytes(played[1], "little")

    edited = bytearray(state)
    affected = set()
    for ident, tag in tags_by_id.items():
        if ident != player_id and tag in requested:
            edited[flags[ident]] = 0
            affected.add(tag)
    if affected != requested - {tags_by_id[player_id]} or edited[flags[player_id]] != 1:
        raise ValueError("The country edits do not match the requested cohort and player exception.")
    result = BytesIO()
    with ZipFile(result, "w") as archive:
        for member in members:
            archive.writestr(copy(member), edited if member.filename == "gamestate" else meta)
    return header + end_of_header + result.getvalue(), {
        "format": "binary_zip", "played_country": tags_by_id[player_id], "disabled": sorted(affected),
        "before": len(flags), "after": len(flags) - len(affected),
    }


def prepare(raw, requested):
    if raw.startswith(b"SAV0105"):
        return prepare_binary(raw, requested)
    return prepare_text(raw, requested)


def write_copy(source, target, modified):
    if target.suffix.lower() != ".v3" or target.resolve() == source.resolve() or target.exists():
        raise ValueError("Choose a new .v3 destination distinct from the original.")
    with NamedTemporaryFile(dir=target.parent, prefix=".aor56-", delete=False) as handle:
        staged = Path(handle.name)
        try:
            handle.write(modified)
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            handle.close()
            staged.unlink(missing_ok=True)
            raise
    try:
        os.link(staged, target)
    finally:
        staged.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--cohort", choices=COHORTS, required=True)
    args = parser.parse_args()
    if args.target.exists() or args.target.resolve() == args.source.resolve():
        parser.error("Choose a new .v3 destination distinct from the original.")
    original = args.source.read_bytes()
    modified, receipt = prepare(original, cohort(args.cohort))
    write_copy(args.source, args.target, modified)
    receipt["source_sha256"] = hashlib.sha256(original).hexdigest()
    receipt["copy_sha256"] = hashlib.sha256(modified).hexdigest()
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
