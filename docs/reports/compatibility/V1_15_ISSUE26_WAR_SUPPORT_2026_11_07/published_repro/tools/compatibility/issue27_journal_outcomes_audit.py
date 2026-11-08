"""Read-only audit of bounded issue #27 journal-outcome migrations.

Usage: python issue27_journal_outcomes_audit.py --mod-root CANDIDATE
       --baseline-root BEFORE --vanilla-root GAME [--inventory-root FULL_MOD]
       [--batch first|sick-man]
Outputs JSON; never writes game files. Token equivalence is not engine validation.
"""
import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys

FILES = (
    "1776_usa_french_support.txt", "1776_usa_revolutionary_spirit.txt",
    "1776_ottoman_reforms.txt", "1776_imperial_centralization.txt",
    "1776_imperial_situation.txt", "10_1776_birth_quota_trial.txt",
)
EXPECTED = {
    "je_aor1776_french_support": ("complete",),
    "je_aor1776_revolutionary_spirit": ("complete",),
    "je_1776_porte_burden": ("complete", "invalid"),
    "je_1776_many_masters": ("complete", "fail", "invalid"),
    "je_aor1776_hre_centralization": ("invalid", "complete"),
    "je_aor1776_hre_situation": ("invalid", "complete"),
    "je_aor1776_hre_vote": ("complete", "invalid"),
    "je_birth_quota_trial": ("complete", "fail"),
}
SICK_MAN_EXPECTED = {
    "je_sick_man_main": ("complete", "timeout"),
    "je_sick_man_syria": ("complete", "invalid"),
    "je_sick_man_egypt": ("complete", "invalid"),
    "je_sick_man_economy": ("complete", "invalid"),
    "je_sick_man_education": ("complete", "invalid"),
    "je_sick_man_separatism": ("complete", "fail", "invalid"),
    "je_sick_man_army": ("complete", "invalid"),
    "je_sick_man_bureaucracy": ("complete", "invalid"),
}
BATCHES = {"first": (FILES, EXPECTED),
           "sick-man": (("00_sick_man.txt",), SICK_MAN_EXPECTED)}
LEGACY = {"complete", "on_complete", "fail", "on_fail", "invalid", "on_invalid",
          "on_timeout", "on_complete_all_involved", "on_fail_all_involved",
          "on_invalid_all_involved", "on_timeout_all_involved"}
LEX = re.compile(r'"(?:\\.|[^"\\])*"|\x23[^\n]*|[{}]|>=|<=|!=|\?=|=|>|<|[^\s{}=<>!#]+')

def tokens(text):
    return [m for m in LEX.finditer(text.lstrip("\ufeff")) if not m[0].startswith("#")]

def signature(text):
    return tuple(m[0] for m in tokens(text))

@dataclass
class Field:
    key: str
    value: str
    body: str
    start: int
    end: int
    block: bool

def fields(text):
    """Read direct fields, keeping duplicate keys, order and source spans."""
    text = text.lstrip("\ufeff")
    ts, result, i = tokens(text), [], 0
    while i < len(ts):
        if ts[i][0] in ("{", "}"):
            raise ValueError("Unexpected brace at direct-field level")
        if i+2 >= len(ts) or ts[i+1][0] != "=":
            i += 1
            continue
        key, start = ts[i][0], ts[i].start()
        if ts[i+2][0] != "{":
            if ts[i+2][0] == "}":
                raise ValueError("Missing field value")
            result.append(Field(key, ts[i+2][0], "", start, ts[i+2].end(), False))
            i += 3
            continue
        j, depth = i+3, 1
        while j < len(ts) and depth:
            depth += (ts[j][0] == "{") - (ts[j][0] == "}")
            j += 1
        if depth:
            raise ValueError("Unclosed block: " + key)
        end = ts[j-1].end()
        result.append(Field(key, text[ts[i+2].start():end],
                            text[ts[i+2].end():ts[j-1].start()], start, end, True))
        i = j
    return result

def one(items, key, optional=False):
    found = [f for f in items if f.key == key]
    if len(found) != 1 and not (optional and not found):
        raise ValueError(f"Expected one {key}, found {len(found)}")
    return found[0] if found else None

def check(condition, message):
    if not condition:
        raise ValueError(message)

def check_journal(old, new, expected=None):
    expected = EXPECTED if expected is None else expected
    before, after = fields(old.body), fields(new.body)
    check(not any(f.key in LEGACY for f in after), "Legacy conclusion remains")
    unchanged_before = [(f.key, signature(f.value)) for f in before if f.key not in LEGACY]
    unchanged_after = [(f.key, signature(f.value)) for f in after if f.key != "outcome"]
    check(unchanged_before == unchanged_after, "Non-conclusion fields changed")
    outcomes = [f for f in after if f.key == "outcome"]
    check(len(outcomes) == len(expected[old.key]), "Wrong outcome count")
    rows = []
    for kind, outcome in zip(expected[old.key], outcomes):
        fs = fields(outcome.body)
        check(len({f.key for f in fs}) == len(fs), "Duplicate outcome field")
        check({f.key for f in fs} <= {"header", "effect_header", "color", "conclusion_desc",
                                          "flags", "trigger", "effect"}, "Unexpected outcome field")
        predicate = one(before, kind, optional=True) if kind != "timeout" else None
        handler = one(before, "on_"+kind, optional=True)
        target_trigger = one(fs, "trigger", optional=kind == "timeout")
        target_effect = one(fs, "effect")
        check(target_effect.block, "Effect must be a block")
        if kind == "timeout":
            check(target_trigger is None, "Timeout outcome must not have a trigger")
            duration = one(before, "timeout")
            check(not duration.block and float(duration.value) > 0, "Missing positive timeout duration")
        else:
            check(target_trigger.block, "Trigger must be a block")
            expected_trigger = predicate.body if predicate else "always = no"
            check(signature(target_trigger.body) == signature(expected_trigger), "Changed trigger/scope: " + kind)
        check(signature(target_effect.body) == signature(handler.body if handler else ""),
              "Changed effect/order/cleanup: " + kind)
        flags = one(fs, "flags", optional=True)
        flag_values = signature(flags.body) if flags else ()
        desc = one(fs, "conclusion_desc").value
        expected_desc = "je_standard_completion_conclusion_desc" if kind == "complete" else "je_standard_failure_conclusion_desc"
        if kind == "timeout":
            expected_desc = "JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC"
        check(desc == expected_desc, "Unexpected conclusion text")
        if kind == "invalid":
            check(set(flag_values) == {"hidden", "invalid_outcome"}, "Invalidation must be silent")
            check(not any(f.key in {"header", "effect_header", "color"} for f in fs), "Visible invalidation")
        elif kind == "timeout":
            check(flag_values == ("timeout",), "Timeout outcome must have exactly the timeout flag")
            check(one(fs, "header").value == "JOURNAL_ENTRY_TIMEOUT", "Wrong timeout header")
            check(one(fs, "effect_header").value == "JOURNAL_ENTRY_ON_TIMEOUT", "Wrong timeout effect header")
            check(not any(f.key == "color" for f in fs), "Unexpected timeout color")
        else:
            check(not flag_values, "Unexpected visible-outcome flags")
            suffix = "completion" if kind == "complete" else "failure"
            check(one(fs, "header").value == "je_standard_"+suffix+"_header", "Wrong outcome header")
            check(one(fs, "effect_header").value == "je_standard_on_"+suffix+"_header", "Wrong effect header")
            check(one(fs, "color").value == ('"gold_positive"' if kind == "complete" else '"blue_negative"'), "Wrong color")
        rows.append({"kind": kind, "trigger_preserved": predicate is not None,
                     "dormant_handler": predicate is None and kind != "timeout", "effect_preserved": True})
    return rows

def audit(mod, baseline, vanilla, inventory=None, batch="first"):
    selected_files, expected = BATCHES[batch]
    errors, rows, seen, legacy_before = [], [], [], 0
    for name in selected_files:
        rel = Path("common/journal_entries")/name
        try:
            old_bytes, new_bytes = (baseline/rel).read_bytes(), (mod/rel).read_bytes()
            old_text, new_text = old_bytes.decode("utf-8-sig"), new_bytes.decode("utf-8-sig")
            old, new = fields(old_text), fields(new_text)
            check([x.key for x in old] == [x.key for x in new], "Journal definitions changed")
            for a, b in zip(old, new):
                check(a.key in expected, "Unexpected journal in bounded batch")
                seen.append(a.key)
                legacy_before += sum(f.key in LEGACY for f in fields(a.body))
                try:
                    mapping = check_journal(a, b, expected)
                except ValueError as exc:
                    errors.append({"file": rel.as_posix(), "journal": a.key, "problem": str(exc)})
                    continue
                rows.append({"file": rel.as_posix(), "journal": a.key,
                             "old_line": old_text.count("\n", 0, a.start)+1,
                             "new_line": new_text.count("\n", 0, b.start)+1,
                             "outcomes": mapping,
                             "before_sha256": hashlib.sha256(old_bytes).hexdigest(),
                             "after_sha256": hashlib.sha256(new_bytes).hexdigest()})
        except (OSError, ValueError) as exc:
            errors.append({"file": rel.as_posix(), "problem": str(exc)})
    if Counter(seen) != Counter(expected.keys()):
        errors.append({"problem": "Expected exactly the eight bounded journal definitions"})
    loc_keys = ("je_standard_completion_header", "je_standard_on_completion_header",
                "je_standard_failure_header", "je_standard_on_failure_header",
                "je_standard_completion_conclusion_desc", "je_standard_failure_conclusion_desc")
    if batch == "sick-man":
        loc_keys += ("JOURNAL_ENTRY_TIMEOUT", "JOURNAL_ENTRY_ON_TIMEOUT", "JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC")
    localization_sources = {}
    for language in ("english", "french"):
        rel = Path("localization")/language/("journal_entries_l_"+language+".yml")
        # A mod with the identical relative file path masks the base-game file.
        source = vanilla/rel
        for layer in (inventory, mod):
            if layer and (layer/rel).is_file():
                source = layer/rel
        localization_sources[language] = str(source)
        text = source.read_text(encoding="utf-8-sig")
        for key in loc_keys:
            if not re.search(r"^\s*"+key+r":", text, re.M):
                errors.append({"problem": "Missing vanilla localization", "language": language, "key": key})
    remaining = []
    if inventory:
        for file in sorted((inventory/"common/journal_entries").glob("*.txt")):
            if file.name in selected_files:
                continue
            try:
                for je in fields(file.read_text(encoding="utf-8-sig")):
                    if not je.block:
                        continue
                    for f in fields(je.body):
                        if f.key in LEGACY:
                            remaining.append({"file": "common/journal_entries/"+file.name,
                                              "journal": je.key, "field": f.key})
            except ValueError as exc:
                remaining.append({"file": str(file), "preexisting_parse_problem": str(exc)})
    return {"status": "PASS_STATIC_ONLY" if not errors else "FAIL_STATIC",
            "runtime_tested": False, "batch": batch, "files": len(selected_files), "journals": len(rows),
            "legacy_fields_before": legacy_before, "outcomes": sum(len(r["outcomes"]) for r in rows),
            "errors": errors, "mapping": rows, "localization_sources": localization_sources,
            "remaining_outside_batch": remaining,
            "limits": ["Token structure only; not the Paradox parser or a game simulation.",
                       "Root/scope and every trigger/effect token preserved; simultaneous outcome precedence needs in-game comparison.",
                       ("The Ottoman administrative invalidation handler has no authored trigger: always=no preserves dormancy."
                        if batch == "first" else "The original JE timeout duration and on_timeout effects are retained; no timeout trigger is introduced."),
                       "Forced external journal removal, active modifiers, callbacks and save/reload need runtime testing."]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mod-root", type=Path, required=True)
    ap.add_argument("--baseline-root", type=Path, required=True)
    ap.add_argument("--vanilla-root", type=Path, required=True)
    ap.add_argument("--inventory-root", type=Path)
    ap.add_argument("--batch", choices=BATCHES, default="first")
    args = ap.parse_args()
    result = audit(args.mod_root, args.baseline_root, args.vanilla_root, args.inventory_root, args.batch)
    print(json.dumps(result, indent=2))
    return bool(result["errors"])

if __name__ == "__main__":
    sys.exit(main())

