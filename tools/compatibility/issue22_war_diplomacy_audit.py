"""Read-only 1.15 war/diplomacy review, including the remaining support calibration.

Checks targeted payloads against canonical native data, preserves every other
byte, inventories inherited goals/plays and checks two declared 1776 wars.
These checks do not simulate fronts, peace, AI or engine enforcement.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE22_WAR_DIPLOMACY/REVIEW_2026_11_09'
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk


def read(p):
    return p.read_bytes().decode('utf-8-sig')


def digest(b):
    return hashlib.sha256(b).hexdigest()


def tokens(text):
    return [m.group() for m in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[?<>!=]+|[^\s{}?<>!=#]+', text)
            if not m.group().startswith('#')]


def signature(node):
    return (node.key, node.op, [signature(n) for n in node.children()]
            if isinstance(node.value, list) else node.value)


def effective_files(folder, native_only=False):
    files = {p.relative_to(GAME).as_posix().casefold(): p for p in (GAME / folder).rglob('*.txt')}
    if not native_only:
        files.update({p.relative_to(ROOT).as_posix().casefold(): p for p in (ROOT / folder).rglob('*.txt')})
    return sorted(files.values(), key=lambda p: str(p).casefold())


def catalog(folder, native_only=False):
    result, pending, ordinary = {}, [], {}
    for p in effective_files(folder, native_only):
        for node in parse(read(p)):
            if not isinstance(node.value, list):
                continue
            prefix, _, key = node.key.partition(':')
            if prefix in ('INJECT', 'REPLACE', 'REPLACE_OR_CREATE'):
                pending.append((prefix, key, node, p))
            else:
                ordinary.setdefault(node.key, []).append(str(p))
                result[node.key] = (node, str(p))
    for prefix, key, node, p in pending:
        new = copy.deepcopy(node)
        new.key = key
        if prefix == 'INJECT' and key in result:
            old = copy.deepcopy(result[key][0])
            replacing = {n.key for n in new.children()}
            old.value = [n for n in old.children() if n.key not in replacing] + new.children()
            new = old
        result[key] = (new, str(p))
    return result, {k: v for k, v in ordinary.items() if len(v) > 1}


def bare(node):
    return [n.value.strip('"') for n in node.children() if not n.key and isinstance(n.value, str)]


def selected(text, spec):
    top = next(n for n in parse(text) if n.key == spec['root'])
    return [n for n in walk(top.children()) if n.key == spec['command']][spec['occurrence']]


def replace_value(text, node, value):
    old = text[node.start:node.end]
    new, count = re.subn(r'(value\s*(?:=|<=|>=|<|>)\s*)[^\s{}]+', lambda m: m.group(1) + value, old)
    if count != 1:
        raise ValueError('Expected exactly one value token')
    return text[:node.start] + new + text[node.end:]


def audit(replacements=None, full=True):
    replacements = replacements or {}
    contract = json.loads(read(LOT / 'CONTRACT.json'))
    checks, details = [], {}

    def check(name, ok):
        checks.append({'check': name, 'passed': bool(ok)})

    for rel, spec in contract['files'].items():
        text = replacements.get(rel, read(ROOT / rel))
        native = read(GAME / rel)
        restored = text
        check(rel + '.canonical_source_unchanged', digest((GAME / rel).read_bytes()) == spec['native_sha256'])
        try:
            parse(text)
            check(rel + '.syntax', True)
            for i, site in enumerate(spec['sites']):
                node = selected(text, site)
                fields = [(n.key, n.op, n.value) for n in node.children()]
                expected = [tuple(row) for row in site['native_payload']]
                check(rel + '.site_' + str(i) + '.native_payload_and_scope', fields == expected)
                reference = dict(site, occurrence=site['native_occurrence'])
                check(rel + '.site_' + str(i) + '.live_native_reference',
                      signature(selected(native, reference))[2] == signature(node)[2])
            for site in reversed(spec['sites']):
                node = selected(restored, site)
                restored = replace_value(restored, node.children('value')[0], site['old_value'])
            original = (LOT / 'before' / rel).read_bytes()
            encoded = (b'\xef\xbb\xbf' if spec['bom_preserved'] else b'') + restored.encode('utf-8')
            check(rel + '.all_other_bytes_preserved', encoded == original and digest(original) == spec['before_sha256'])
        except (ValueError, StopIteration, IndexError, KeyError) as exc:
            check(rel + '.structure:' + str(exc), False)

    # Strict boundary checks use the installed values/operators, not a second
    # implementation of the intended patch.
    for rel, spec in contract['files'].items():
        for i, site in enumerate(spec['sites']):
            if site['command'] != 'has_war_support':
                continue
            node = selected(replacements.get(rel, read(ROOT / rel)), site).children('value')[0]
            expected_threshold = float(site['expected_value'])
            threshold = float(node.value)
            compare = {'<': lambda a, b: a < b, '>': lambda a, b: a > b, '<=': lambda a, b: a <= b}
            for delta in (-0.01, 0, 0.01):
                value = expected_threshold + delta
                actual = compare.get(node.op, lambda *_: None)(value, threshold)
                expected = compare[site['operator']](value, expected_threshold)
                check(rel + '.site_' + str(i) + '.boundary_' + str(delta), actual == expected)

    restored = contract['restored_plays']
    text = replacements.get(restored['file'], read(ROOT / restored['file']))
    native_nodes = {n.key: n for n in parse(read(GAME / restored['native_file']))}
    check('restored_plays.canonical_source_unchanged',
          digest((GAME / restored['native_file']).read_bytes()) == restored['native_sha256'])
    try:
        current = {n.key: n for n in parse(text)}
        check('restored_plays.exact_key_set', set(current) == set(restored['keys']))
        for key in restored['keys']:
            check(key + '.exact_native_object', key in current and signature(current[key]) == signature(native_nodes[key]))
    except ValueError:
        check('restored_plays.syntax', False)

    if full:
        goals, duplicate_goals = catalog('common/war_goal_types')
        plays, duplicate_plays = catalog('common/diplomatic_plays')
        native_plays, _ = catalog('common/diplomatic_plays', True)
        native_goals, _ = catalog('common/war_goal_types', True)
        countries, _ = catalog('common/country_definitions')
        check('goals.no_ordinary_duplicates', not duplicate_goals)
        check('plays.no_ordinary_duplicates', not duplicate_plays)
        check('plays.no_native_play_hidden', set(native_plays) <= set(plays))
        check('goals.no_native_goal_hidden', set(native_goals) <= set(goals))
        triggers, _ = catalog('common/scripted_triggers')
        for dependency in ['diplomatic_play_has_no_relations_blockers', 'is_russia_unification_pair']:
            check('restored_plays.' + dependency + '.resolves', dependency in triggers)
        for rel in restored['dependencies_inherited']:
            check('restored_plays.' + rel + '.inherited_not_masked',
                  (GAME / rel).is_file() and not (ROOT / rel).exists())
        kinds = {n.one('kind') for n, _ in native_goals.values()} | {'custom'}
        settings = {v for n, _ in native_goals.values() for group in n.children('settings') for v in bare(group)}
        mirrors = []
        for key, (node, source) in goals.items():
            check(key + '.native_kind', node.one('kind') in kinds)
            for group in node.children('settings'):
                check(key + '.native_settings', set(bare(group)) <= settings)
            for block in node.children('mirrored_wargoal'):
                for target in block.children('type'):
                    check(key + '.mirror_goal_resolves', target.value in goals)
                mirrors.append({'goal': key, 'method': block.one('method')})
        for key, (node, _) in plays.items():
            for field in ['war_goal', 'target_war_goal']:
                target = node.one(field)
                if target:
                    check(key + '.' + field + '.resolves', target in goals)

        before = json.loads(read(LOT / 'BEFORE.json'))['sources']
        warfiles = ['common/history/diplomatic_plays/00_american_revolution.txt',
                    'common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt']
        starts = []
        for rel in warfiles:
            check(rel + '.starting_setup_preserved', digest((ROOT / rel).read_bytes()) == before[rel])
            raw = read(ROOT / rel)
            for country in parse(raw)[0].children():
                actor = country.key.removeprefix('c:')
                check(rel + '.actor_defined', actor in countries)
                for play in country.children('create_diplomatic_play'):
                    target = play.one('target_country').removeprefix('c:')
                    kind = play.one('type')
                    check(rel + '.target_defined', target in countries)
                    check(rel + '.play_defined', kind in plays)
                    check(rel + '.ongoing_war', play.one('war') == 'yes')
                    for field in play.children('add_initiator_backers') + play.children('add_target_backers'):
                        for backer in bare(field):
                            check(rel + '.backer_' + backer + '.defined', backer.removeprefix('c:') in countries)
                    for goal in play.children('add_war_goal'):
                        check(rel + '.goal_' + goal.one('type') + '.defined', goal.one('type') in goals)
                        check(rel + '.holder_' + goal.one('holder') + '.defined', goal.one('holder').removeprefix('c:') in countries)
                    starts.append({'file': rel, 'initiator': actor, 'target': target, 'type': kind,
                                   'explicit_goals': [signature(n) for n in play.children('add_war_goal')],
                                   'runtime_fronts_not_validated': True})
        usa = starts[0]
        check('usa.initial_independence_war', usa['initiator'] == 'USA' and usa['target'] == 'GBR' and usa['type'] == 'dp_independence')
        check('usa.spain_starts_neutral_in_this_declaration', 'c:SPA' not in tokens(read(ROOT / warfiles[0])))
        check('independence.native_restore_subject_mirror', goals['independence'][0].children('mirrored_wargoal')[0].one('method') == 'restore_subject')
        hooks = {n.key for p in effective_files('common/on_actions') for n in parse(read(p))}
        for hook in ['on_wargoal_enforced', 'on_war_end', 'on_capitulation',
                     'on_peace_agreement_signed_war_leader', 'on_peace_agreement_signed_war_participant']:
            check(hook + '.effective_hook_declared', hook in hooks)
        forbidden = re.compile(r'\b(?:add_war_exhaustion|has_war_exhaustion|additional_war_exhaustion|war_exhaustion_from_acceptance_of_dead)\b')
        removed = []
        for folder in ['common', 'events']:
            for p in effective_files(folder):
                if forbidden.search(' '.join(tokens(read(p)))):
                    removed.append(str(p))
        mod_removed = [p for p in removed if Path(p).is_relative_to(ROOT)]
        inherited_removed = [p for p in removed if Path(p).is_relative_to(GAME)]
        check('no_removed_exhaustion_commands_in_mod_scripts', not mod_removed)
        # The current canonical game still ships this old script-value file.
        # Record that upstream residue explicitly, rather than claiming a clean
        # effective graph or changing vanilla. Unknown upstream residues fail.
        inherited_contract = contract['inherited_legacy_reference']
        check('inherited_legacy_reference.exact_recorded_source',
              inherited_removed == [str(GAME / inherited_contract['file'])]
              and digest((GAME / inherited_contract['file']).read_bytes()) == inherited_contract['sha256'])
        details = {'goals': len(goals), 'plays': len(plays), 'native_goals': len(native_goals),
                   'native_plays': len(native_plays), 'mirrors': mirrors, 'initial_wars': starts,
                   'duplicate_goals': duplicate_goals, 'duplicate_plays': duplicate_plays,
                   'removed_command_files': removed,
                   'inherited_legacy_reference': inherited_contract,
                   'scope_limit': 'Declared references and exact payloads only; no engine load order, territorial ownership, fronts, war simulation or peace acceptance inferred.'}
    failed = [c for c in checks if not c['passed']]
    return {'status': 'FAIL_STATIC' if failed else 'PASS_STATIC_ONLY', 'passed': len(checks) - len(failed),
            'total': len(checks), 'errors': failed, 'checks': checks, 'inventory': details,
            'engine_tested': False, 'human_runtime_accepted': False}


def negative_controls():
    contract = json.loads(read(LOT / 'CONTRACT.json'))
    result = []
    for rel, spec in contract['files'].items():
        for i, site in enumerate(spec['sites']):
            raw = read(ROOT / rel)
            changed = replace_value(raw, selected(raw, site).children('value')[0], site['old_value'])
            result.append({'case': rel + '.legacy_value_' + str(i),
                           'detected': audit({rel: changed}, full=False)['status'] == 'FAIL_STATIC'})
    rel = contract['restored_plays']['file']
    raw = read(ROOT / rel)
    for key in contract['restored_plays']['keys']:
        node = next(n for n in parse(raw) if n.key == key)
        changed = raw[:node.start] + raw[node.end:]
        result.append({'case': key + '.missing', 'detected': audit({rel: changed}, full=False)['status'] == 'FAIL_STATIC'})
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    result = audit()
    if args.negative_controls:
        result['negative_controls'] = negative_controls()
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['status', 'passed', 'total', 'errors']}))
    if args.negative_controls:
        print(json.dumps({'negative_controls_detected': sum(c['detected'] for c in result['negative_controls']),
                          'negative_controls_total': len(result['negative_controls'])}))
    sys.exit(result['status'] != 'PASS_STATIC_ONLY' or any(not c['detected'] for c in result.get('negative_controls', [])))
