"""Read-only audit of the bounded Canadian, Polish and Northwest outcome fixes.

Untargeted definitions in shared files must remain byte-identical as text bodies.
No eligibility predicates, Polish partition effects or new rewards are introduced.
"""
import argparse
from collections import Counter
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re

import issue27_journal_outcomes_audit as old_audit

SELECTED = {
    "00_canada_australia.txt": {
        "je_canada_can": ("complete", "invalid"),
        "je_canada_gbr": ("complete",),
    },
    "07_poland_lithuania_mod.txt": {
        "je_plc_reform": ("complete",),
        "je_plc_reform_industry": ("complete",),
        "je_plc_reform_trade": ("complete",),
        "je_plc_reform_education": ("complete",),
        "je_plc_reform_railways": ("complete",),
        "je_plc_reform_farming": ("complete",),
        "je_plc_reform_military": ("complete",),
        "je_plc_reform_great_power": ("complete",),
    },
    "07_american_mod_jes.txt": {
        "je_northwest_frontier_mod": ("complete", "timeout"),
    },
}
EXPECTED = {key: kinds for items in SELECTED.values() for key, kinds in items.items()}
ALIASES = {
    "je_canada_can": "$je_canada$",
    "je_canada_can_reason": "$je_canada_reason$",
    "je_canada_gbr": "$je_canada$",
    "je_canada_gbr_reason": "$je_canada_reason$",
}


def verify_pair(before, after):
    rows = old_audit.check_journal(before, after, EXPECTED)
    if before.key.startswith("je_plc_reform"):
        fields = old_audit.fields(after.body)
        old_audit.check(not any(f.key == "timeout" for f in fields), "Polish partition timer reintroduced")
        old_audit.check("set_state_owner" not in old_audit.signature(after.body), "Polish territorial transfer reintroduced")
    return rows


def negative_controls(pairs):
    cases = (
        ("Polish literacy threshold", "je_plc_reform", "literacy_rate > 0.20", "literacy_rate > 0.21"),
        ("Polish GDP target", "je_plc_reform", "add = 9000000", "add = 9000001"),
        ("Polish ideological cleanup", "je_plc_reform", "remove_ideology = ideology_polish_szlachta", "remove_ideology = ideology_magnatial"),
        ("Polish education continuation", "je_plc_reform", "type = je_plc_reform_education", "type = je_plc_reform_trade"),
        ("Canadian territory count", "je_canada_gbr", "amount >= 9", "amount >= 8"),
        ("Canadian country scope", "je_canada_gbr", "any_subject_or_below", "any_country"),
        ("Canadian silent invalidation", "je_canada_can", "hidden invalid_outcome", "hidden"),
        ("Northwest timeout duration", "je_northwest_frontier_mod", "timeout = 2300", "timeout = 2301"),
        ("Northwest timeout flag", "je_northwest_frontier_mod", "flags = { timeout }", "flags = {}"),
    )
    results = []
    for name, key, anchor, replacement in cases:
        before, after = pairs[key]
        old_audit.check(anchor in after.body, "Missing negative control anchor: " + name)
        mutant = replace(after, body=after.body.replace(anchor, replacement, 1))
        try:
            verify_pair(before, mutant)
        except ValueError as exc:
            results.append({"control": name, "detected": True, "reason": str(exc)})
        else:
            raise ValueError("Undetected negative control: " + name)
    before, after = pairs["je_plc_reform"]
    for name, addition in (
        ("Polish timer restored", "\ntimeout = 6000\n"),
        ("Legacy conclusion restored", "\ncomplete = { always = yes }\n"),
    ):
        try:
            verify_pair(before, replace(after, body=after.body + addition))
        except ValueError as exc:
            results.append({"control": name, "detected": True, "reason": str(exc)})
        else:
            raise ValueError("Undetected negative control: " + name)
    return results


def audit(mod, baseline, vanilla, self_test=False):
    errors, rows, pairs, untouched, seen = [], [], {}, [], []
    legacy_count = 0
    for name, selected in SELECTED.items():
        rel = Path("common/journal_entries") / name
        try:
            before_bytes = (baseline / rel).read_bytes()
            after_bytes = (mod / rel).read_bytes()
            before_text = before_bytes.decode("utf-8-sig")
            after_text = after_bytes.decode("utf-8-sig")
            before = old_audit.fields(before_text)
            after = old_audit.fields(after_text)
            old_audit.check([f.key for f in before] == [f.key for f in after], "Definition inventory/order changed")
            for first, last in zip(before, after):
                if first.key not in selected:
                    old_audit.check(first.body == last.body, "Untargeted definition changed: " + first.key)
                    untouched.append(first.key)
                    continue
                seen.append(first.key)
                legacy_count += sum(f.key in old_audit.LEGACY for f in old_audit.fields(first.body))
                mapping = verify_pair(first, last)
                pairs[first.key] = (first, last)
                rows.append({"file": rel.as_posix(), "journal": first.key, "outcomes": mapping,
                             "new_line": after_text.count("\n", 0, last.start) + 1,
                             "before_sha256": hashlib.sha256(before_bytes).hexdigest(),
                             "after_sha256": hashlib.sha256(after_bytes).hexdigest()})
        except (OSError, ValueError) as exc:
            errors.append({"file": rel.as_posix(), "error": str(exc)})
    if Counter(seen) != Counter(EXPECTED.keys()):
        errors.append({"error": "Expected exactly the eleven selected journals"})
    loc_checks = []
    for language in ("french", "english"):
        rel = Path("localization") / language / ("1776_canadian_journals_l_" + language + ".yml")
        try:
            data = (mod / rel).read_bytes()
            old_audit.check(data.startswith(b"\xef\xbb\xbf"), "Missing localization BOM")
            text = data.decode("utf-8-sig")
            old_audit.check(text.splitlines()[0] == "l_" + language + ":", "Wrong language header")
            actual = dict(re.findall(r'^\s*(\w+):0\s+"([^"\r\n]*)"\s*$', text, re.M))
            old_audit.check(actual == ALIASES, "Canadian aliases differ from the bounded mapping")
            for key in ALIASES:
                definitions = []
                for path in (mod / "localization" / language).rglob("*.yml"):
                    count = len(re.findall(r"^\s*" + re.escape(key) + r":", path.read_text(encoding="utf-8-sig"), re.M))
                    definitions.extend([path.as_posix()] * count)
                old_audit.check(len(definitions) == 1, "Duplicate or missing Canadian key: " + key)
            native_rel = Path("localization") / language / ("content_1_l_" + language + ".yml")
            native = mod / native_rel if (mod / native_rel).exists() else vanilla / native_rel
            native_text = native.read_text(encoding="utf-8-sig")
            for key in ("je_canada", "je_canada_reason"):
                old_audit.check(re.search(r"^\s*" + key + r":", native_text, re.M), "Missing native alias target: " + key)
            standard_rel = Path("localization") / language / ("journal_entries_l_" + language + ".yml")
            standard = mod / standard_rel if (mod / standard_rel).exists() else vanilla / standard_rel
            standard_text = standard.read_text(encoding="utf-8-sig")
            for key in ("je_standard_completion_header", "je_standard_on_completion_header",
                        "je_standard_completion_conclusion_desc", "je_standard_failure_conclusion_desc",
                        "JOURNAL_ENTRY_TIMEOUT", "JOURNAL_ENTRY_ON_TIMEOUT",
                        "JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC"):
                old_audit.check(re.search(r"^\s*" + key + r":", standard_text, re.M), "Missing standard outcome text: " + key)
            loc_checks.append({"language": language, "file": rel.as_posix(), "native_source": str(native), "unique_keys": 4})
        except (OSError, ValueError) as exc:
            errors.append({"language": language, "error": str(exc)})
    controls = []
    if self_test and not errors:
        try:
            controls = negative_controls(pairs)
        except ValueError as exc:
            errors.append({"error": str(exc)})
    return {"status": "PASS_STATIC_ONLY" if not errors else "FAIL_STATIC", "runtime_tested": False,
            "files": len(SELECTED), "journals": len(rows), "legacy_fields_replaced": legacy_count,
            "outcomes": sum(len(r["outcomes"]) for r in rows), "mapping": rows,
            "untargeted_definitions_unchanged": untouched, "localization": loc_checks,
            "negative_controls": controls, "errors": errors,
            "limits": ["No engine acceptance of the newly installed fixes.",
                       "All predicates, effects and ordered non-conclusion fields compare equal to the immediate baseline.",
                       "Native Canadian button/event semantics and conclusion precedence remain runtime gates."]}


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
