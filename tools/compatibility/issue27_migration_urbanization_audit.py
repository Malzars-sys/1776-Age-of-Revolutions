"""Read-only preservation audit for the migration/urbanization journal batch.

The only predicate syntax exception is the three explicitly checked peasant
comparisons in je_urbanization_events_1. No thresholds or iterator percentages
are normalized. This is not the Paradox parser or an engine acceptance test.
"""
import argparse
from collections import Counter
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re

import issue27_journal_outcomes_audit as original

FILES = ("00_urbanization.txt", "02_south_america_migration.txt")
EXPECTED = {
    "je_urbanization_events_1": ("complete",),
    "je_urbanization_events_2": ("complete",),
    "je_south_america_migration": ("complete", "invalid"),
    "je_central_america_migration": ("complete", "invalid"),
    "je_american_west_migration": ("complete", "invalid"),
}
PEASANT_BLOCK = re.compile(
    r"\bpop_type_percent_country\s*=\s*\{\s*(?:#[^\n]*\n\s*)?"
    r"pop_type\s*=\s*peasants\s+percent\s*(>|<)\s*(0\.6|0\.35)\s*\}"
)


def normalize_urbanization(journal):
    """Apply exactly the documented 1.15 argument renames to the old source."""
    if journal.key != "je_urbanization_events_1":
        return journal
    matches = list(PEASANT_BLOCK.finditer(journal.body))
    original.check([(m[1], m[2]) for m in matches] ==
                   [(">", "0.6"), (">", "0.6"), ("<", "0.35")],
                   "Expected exactly the three original peasant comparisons")

    def rewrite(match):
        text = re.sub(r"\bpop_type\s*=\s*peasants\b",
                      "target = pop_type:peasants", match[0])
        return re.sub(r"\bpercent\b", "value", text)

    return replace(journal, body=PEASANT_BLOCK.sub(rewrite, journal.body))


def verify_journal(before, after):
    return original.check_journal(normalize_urbanization(before), after, EXPECTED)


def negative_controls(pairs):
    """Confirm that gameplay-changing regressions are rejected in memory."""
    controls = (
        ("peasant threshold", "je_urbanization_events_1", "value < 0.35", "value < 0.36"),
        ("typed peasant target", "je_urbanization_events_1", "target = pop_type:peasants", "target = peasants"),
        ("state iterator threshold", "je_urbanization_events_2", "percent >= 0.75", "percent >= 0.70"),
        ("completion event", "je_urbanization_events_2", "urbanization_events.5", "urbanization_events.1"),
        ("annual event weight", "je_urbanization_events_2", "30 = 0", "31 = 0"),
        ("migration goal", "je_central_america_migration", "multiply = 1000000", "multiply = 1500000"),
        ("country scope", "je_south_america_migration", "ROOT = {", "PREV = {"),
        ("silent cancellation", "je_south_america_migration", "hidden invalid_outcome", "hidden"),
        ("cancellation predicate", "je_american_west_migration", "has_variable = cancel_sa_migration_var", "always = yes"),
    )
    results = []
    for name, key, old, new in controls:
        before, after = pairs[key]
        original.check(old in after.body, "Negative control anchor missing: " + name)
        mutated = replace(after, body=after.body.replace(old, new, 1))
        try:
            verify_journal(before, mutated)
        except ValueError as exc:
            results.append({"control": name, "detected": True, "reason": str(exc)})
        else:
            raise ValueError("Undetected negative control: " + name)
    before, after = pairs["je_south_america_migration"]
    mutated = replace(after, body=after.body + "\ncomplete = { always = yes }\n")
    try:
        verify_journal(before, mutated)
    except ValueError as exc:
        results.append({"control": "legacy field reintroduced", "detected": True, "reason": str(exc)})
    else:
        raise ValueError("Undetected legacy-field negative control")
    return results


def audit(mod, baseline, vanilla, self_test=False):
    rows, errors, pairs, seen = [], [], {}, []
    old_fields = 0
    for filename in FILES:
        relative = Path("common/journal_entries") / filename
        try:
            before_bytes = (baseline / relative).read_bytes()
            after_bytes = (mod / relative).read_bytes()
            before_text = before_bytes.decode("utf-8-sig")
            after_text = after_bytes.decode("utf-8-sig")
            before = original.fields(before_text)
            after = original.fields(after_text)
            original.check([j.key for j in before] == [j.key for j in after],
                           "Journal definitions or order changed")
            for old, new in zip(before, after):
                original.check(old.key in EXPECTED, "Unexpected journal: " + old.key)
                seen.append(old.key)
                old_fields += sum(f.key in original.LEGACY for f in original.fields(old.body))
                mapping = verify_journal(old, new)
                pairs[old.key] = (old, new)
                rows.append({"file": relative.as_posix(), "journal": old.key,
                             "outcomes": mapping,
                             "new_line": after_text.count("\n", 0, new.start) + 1,
                             "before_sha256": hashlib.sha256(before_bytes).hexdigest(),
                             "after_sha256": hashlib.sha256(after_bytes).hexdigest(),
                             "population_argument_renames": 3 if old.key == "je_urbanization_events_1" else 0})
        except (OSError, ValueError) as exc:
            errors.append({"file": relative.as_posix(), "error": str(exc)})
    if Counter(seen) != Counter(EXPECTED.keys()):
        errors.append({"error": "Expected exactly the five selected journal definitions"})
    keys = ("je_standard_completion_header", "je_standard_on_completion_header",
            "je_standard_completion_conclusion_desc", "je_standard_failure_conclusion_desc")
    sources = {}
    for language in ("english", "french"):
        relative = Path("localization") / language / ("journal_entries_l_" + language + ".yml")
        source = mod / relative if (mod / relative).is_file() else vanilla / relative
        sources[language] = str(source)
        text = source.read_text(encoding="utf-8-sig")
        for key in keys:
            if not re.search(r"^\s*" + re.escape(key) + r":", text, re.M):
                errors.append({"error": "Missing localization", "language": language, "key": key})
        for file in (mod / "localization" / language).rglob("*.yml"):
            text = file.read_text(encoding="utf-8-sig")
            for key in keys:
                if file != source and re.search(r"^\s*" + re.escape(key) + r":", text, re.M):
                    errors.append({"error": "Unexpected standard-key override", "file": str(file), "key": key})
    controls = []
    if self_test and not errors:
        try:
            controls = negative_controls(pairs)
        except ValueError as exc:
            errors.append({"error": str(exc)})
    return {"status": "PASS_STATIC_ONLY" if not errors else "FAIL_STATIC",
            "runtime_tested": False, "files": len(FILES), "journals": len(rows),
            "legacy_fields_replaced": old_fields,
            "outcomes": sum(len(row["outcomes"]) for row in rows),
            "mapping": rows, "localization_sources": sources,
            "negative_controls": controls, "errors": errors,
            "limits": ["No Paradox parser or game simulation executed.",
                       "Original predicates, effects and ordered non-conclusion fields preserved except the three documented argument renames.",
                       "No cleanup helpers or changes to migration goals imported from vanilla.",
                       "Simultaneous outcomes, active modifiers, cancellation and save/reload require engine acceptance."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod-root", type=Path, required=True)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--vanilla-root", type=Path, required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = audit(args.mod_root, args.baseline_root, args.vanilla_root, args.self_test)
    print(json.dumps(result, indent=2))
    return bool(result["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
