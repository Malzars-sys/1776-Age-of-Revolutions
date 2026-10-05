"""Read-only validation of the requested unlock changes against a pinned baseline."""
import argparse
import hashlib
import json
import subprocess

from asset4_style_reference_audit import ROOT, TOKENS, field, pairs

PACK = ROOT / "docs/reports/technology/popular_sovereignty_2026-10-03"
BASE_COMMIT = "731d7955c8947d7cbf4d6f661c14e8a7a0593767"
# Git normalizes Windows line endings; only that representation change is allowed.
ARCHIVE_SHA256 = "c387b909036d2007e9ee63491907654ae1ec5f8de68fc4e1f11c1cb523b6be00"
TARGETS = {
    "common/laws/00_governance_principles.txt": ["law_presidential_republic", "law_parliamentary_republic"],
    "common/laws/00_distribution_of_power.txt": ["law_census_voting"],
    "common/technology/technologies/30_tech3a_society.txt": ["liberal_constitutionalism"],
}
PUBLICATION_FILES = set(TARGETS) | {
    "docs/reports/technology/popular_sovereignty_2026-10-03/README.md",
    "docs/reports/technology/popular_sovereignty_2026-10-03/baseline.json",
    "docs/reports/technology/popular_sovereignty_2026-10-03/validation.json",
    "tools/validate_popular_sovereignty_changes.py",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def lines(*args):
    return git(*args).decode("utf-8").splitlines()


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def parse(payload):
    tokens = [t for t in TOKENS.findall(payload.decode("utf-8-sig")) if not t.startswith("#")]
    depth = 0
    for token in tokens:
        depth += (token == "{") - (token == "}")
        assert depth >= 0, "Unexpected closing brace"
    assert depth == 0, "Unbalanced braces"
    entries = list(pairs(tokens))
    assert len({k for k, _ in entries}) == len(entries), "Duplicate top-level definition"
    return dict(entries)


def verify_changes(old_files, read_current):
    for filename, keys in TARGETS.items():
        old, new = parse(old_files[filename]), parse(read_current(filename))
        for key in keys:
            assert key in old and key in new, "Missing definition: " + key
            before = field(old[key], "unlocking_technologies")
            after = field(new[key], "unlocking_technologies")
            assert sum(k == "unlocking_technologies" for k, _ in pairs(new[key])) == 1
            others = ["human_rights", "classical_political_economy"] if key == "liberal_constitutionalism" else []
            assert before == ["constitutional_government", *others], "Unexpected old prerequisites: " + key
            assert after == ["national_sovereignty", *others], "Unexpected new prerequisites: " + key
            for definitions in (old, new):
                definitions[key] = [(k, v) for k, v in pairs(definitions[key]) if k != "unlocking_technologies"]
        assert old == new, "Unrequested change in " + filename


def verify_tree(paths, read_current):
    techs = {}
    for filename in paths:
        for key, tokens in parse(read_current(filename)).items():
            assert key not in techs, "Duplicate technology: " + key
            techs[key] = tokens
    parents = {key: field(tokens, "unlocking_technologies", []) for key, tokens in techs.items()}
    visiting, visited = set(), set()

    def visit(key):
        assert key not in visiting, "Technology dependency cycle: " + key
        if key in visited:
            return
        visiting.add(key)
        for parent in parents[key]:
            assert parent in parents, "Unknown technology parent: " + parent
            visit(parent)
        visiting.remove(key)
        visited.add(key)

    for key in parents:
        visit(key)
    for key in ("national_sovereignty", "human_rights", "classical_political_economy"):
        assert key in techs, "Missing law/technology unlock: " + key
    return parents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--verify", action="store_true", help="Compare with the pinned post-assets commit")
    modes.add_argument("--verify-historical", action="store_true", help="Strictly compare with the immutable October 3 archive")
    parser.add_argument("--staged", action="store_true", help="Verify the exact seven-file Git index before publication")
    args = parser.parse_args()
    assert not (args.staged and args.verify_historical), "Historical mode only reads the working tree"
    read_current = (lambda p: git("show", ":" + p)) if args.staged else (lambda p: (ROOT / p).read_bytes())
    archive_bytes = read_current("docs/reports/technology/popular_sovereignty_2026-10-03/baseline.json")
    assert sha(archive_bytes.replace(b"\r\n", b"\n")) == ARCHIVE_SHA256, "Historical baseline was modified"
    archive = json.loads(archive_bytes)
    if args.verify_historical:
        old_files = {p: text.encode("utf-8") for p, text in archive["definitions"].items()}
        verify_changes(old_files, read_current)
        current = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes())
                   for folder in ("common", "gfx") for p in (ROOT / folder).rglob("*") if p.is_file()}
        assert current.keys() == archive["files"].keys(), "Game file added or deleted since the historical baseline"
        changed = {p for p, h in archive["files"].items() if current[p] != h}
        assert changed == set(TARGETS), "Unrelated game file changed since the historical baseline"
        protected_count = len(current) - len(changed)
        reference = "IMMUTABLE_OCTOBER_3_ARCHIVE"
    else:
        assert git("rev-parse", BASE_COMMIT + "^{commit}").decode().strip() == BASE_COMMIT
        old_files = {p: git("show", BASE_COMMIT + ":" + p) for p in TARGETS}
        verify_changes(old_files, read_current)
        diff_args = ["diff", BASE_COMMIT, *(["--cached"] if args.staged else []), "--name-only"]
        changed = set(lines(*diff_args, "--", "common", "gfx"))
        assert changed == set(TARGETS), "Unrelated game file changed relative to the publication baseline"
        assert not lines("ls-files", "--others", "--exclude-standard", "--", "common", "gfx"), "Untracked game file"
        if args.staged:
            assert set(lines(*diff_args)) == PUBLICATION_FILES, "Publication must contain exactly the seven requested files"
        protected = lines("ls-tree", "-r", "--name-only", BASE_COMMIT, "--", "common", "gfx")
        protected_count = len(protected) - len(changed)
        reference = BASE_COMMIT
    tech_paths = [p for p in lines("ls-files", "--", "common/technology/technologies") if p.endswith(".txt")]
    parents = verify_tree(tech_paths, read_current)
    report = {
        "status": "PASS_REQUESTED_POPULAR_SOVEREIGNTY_CHANGES",
        "validation_mode": "STAGED" if args.staged else "WORKTREE",
        "reference": reference,
        "historical_baseline_preserved": True,
        "historical_baseline_sha256": ARCHIVE_SHA256,
        "historical_baseline_hash_representation": "UTF8_WITH_LF_LINE_ENDINGS",
        "law_unlocks": {key: "national_sovereignty" for key in
                        ("law_presidential_republic", "law_parliamentary_republic", "law_census_voting")},
        "liberal_constitutionalism_parents": parents["liberal_constitutionalism"],
        "law_wealth_voting_unchanged": True,
        "technology_count": len(parents),
        "missing_parents": [], "cycles": [],
        "changed_game_files": sorted(changed),
        "other_tracked_game_files_unchanged": protected_count,
        "publication_file_count": len(PUBLICATION_FILES) if args.staged else None,
        "game_tested": False,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
