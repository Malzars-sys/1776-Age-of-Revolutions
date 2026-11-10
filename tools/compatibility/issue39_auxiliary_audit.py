"""Read-only checks for the native objects and localization restored by #39."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import issue39_dependency_audit as dep
from issue27_journal_outcomes_audit import fields, signature


def audit(directory):
    root, game = dep.ROOT, dep.GAME
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    restored = json.loads((directory / 'RESTORATIONS.json').read_text())
    checks = []
    def check(name, value):
        checks.append({'check': name, 'passed': bool(value)})
    laws = dep.catalogue('common/laws')
    modifiers = dep.catalogue('common/static_modifiers')
    native_helpers, helpers = set(), set()
    for folder in ['common/scripted_effects', 'common/scripted_triggers', 'common/script_values']:
        native_helpers.update(dep.catalogue(folder, native_only=True))
        helpers.update(dep.catalogue(folder))
    for key, spec in restored['objects'].items():
        native = game / spec['native_file']
        check(key + '.native_file_pinned', sha(native) == spec['native_sha256'])
        original = next(n for n in fields(dep.read(native)) if n.key == key)
        rel = 'events/zz_1776_v115_five_year_plan.txt' if key.startswith('communism.') else 'common/journal_entries/zz_1776_v115_restored_journals.txt'
        current = next(n for n in fields(dep.read(root / rel)) if n.key == key)
        check(key + '.exact_native_body', original.value == current.value)
        if not key.startswith('communism.'):
            check(key + '.no_autostart_added', not any(f.key == 'is_shown_when_inactive' for f in fields(current.body)))
        for law in sorted(set(re.findall(r'law_type:([a-z_0-9]+)', current.body))):
            check(key + '.law.' + law, law in laws)
        for node in dep.walk(dep.parse(current.value[1:-1])):
            if node.key in native_helpers:
                check(key + '.known_helper.' + node.key, node.key in helpers)
            if node.key == 'add_modifier':
                name = node.one('name') if isinstance(node.value, list) else node.value
                if isinstance(name, str) and not name.startswith(('var:', 'scope:')):
                    check(key + '.modifier.' + name, name in modifiers)
    loc = json.loads((directory / 'LOCALIZATION.json').read_text())
    language_keys = []
    for rel, expected_hash in loc['files'].items():
        path = root / rel
        raw = dep.read(path)
        lang = 'french' if '/french/' in rel else 'english'
        keys = re.findall(r'^ ([\w.]+):0 "(?:[^"\\]|\\.)*"$', raw, re.M)
        language_keys.append(set(keys))
        check(rel + '.BOM', path.read_bytes().startswith(b'\xef\xbb\xbf'))
        check(rel + '.file_pinned', sha(path) == expected_hash)
        check(rel + '.language_header', raw.startswith('l_' + lang + ':\n'))
        check(rel + '.32_unique_valid_lines', len(keys) == len(set(keys)) == 32)
        others = set()
        for base in [game, root]:
            for source in (base / 'localization' / lang).rglob('*.yml'):
                if source == path:
                    continue
                others.update(re.findall(r'^\s*([\w.\-]+):(?:\d+)?\s*"', dep.read(source), re.M))
        check(rel + '.no_existing_key_overridden', not (set(keys) & others))
    check('bilingual_key_parity', language_keys[0] == language_keys[1])
    check('native_journal_entry_GUI_not_masked', (game / 'gui/journal_entry.gui').is_file() and not (root / 'gui/journal_entry.gui').exists())
    manifest = json.loads((directory / 'MANIFEST.json').read_text())
    repro = json.loads((directory / 'REPRO_CHECK/MANIFEST.json').read_text())
    check('captured_source_reproduction_exact', all(repro['files'][k]['candidate_sha256'] == v['candidate_sha256'] for k, v in manifest['files'].items()))
    journals, buttons, events = (dep.catalogue(p) for p in
                                 ['common/journal_entries', 'common/scripted_buttons', 'events'])
    bindings, unresolved = 0, []
    for owner, (node, _) in journals.items():
        for reference in node.children('scripted_button'):
            if reference.value not in buttons:
                continue
            bindings += 1
            for child in dep.walk(buttons[reference.value][0].children()):
                if child.key == 'trigger_event':
                    target = child.one('id') if isinstance(child.value, list) else child.value
                    if isinstance(target, str) and '$' not in target and target not in events:
                        unresolved.append([owner, reference.value, 'event', target])
                elif child.key == 'add_journal_entry':
                    target = child.one('type')
                    if isinstance(target, str) and '$' not in target and target not in journals:
                        unresolved.append([owner, reference.value, 'journal', target])
    check('bound_button_events_and_additions_resolve', not unresolved)
    failures = [c['check'] for c in checks if not c['passed']]
    return {'status': 'FAIL_STATIC' if failures else 'PASS_STATIC_ONLY', 'passed': len(checks) - len(failures),
            'total': len(checks), 'failures': failures, 'checks': checks, 'engine_tested': False,
            'bound_button_bindings': bindings, 'bound_button_findings': unresolved,
            'limits': 'Literal targets and native object identity only; no execution or DLC-chain activation certified.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.directory)
    (args.directory / 'AUXILIARY_FINAL_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}))
    raise SystemExit(bool(result['failures']))
