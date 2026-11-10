"""Bounded issue25 AI diagnostics and two-leaf native-alignment audit.

--prepare writes new local evidence/candidate files only. No gameplay installer,
engine launch, Git writes or native edit. Existing evidence is never overwritten.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE25_AI_SCOPE_TRIAGE_2026_11_09'
LOGS = ROOT / 'docs/reports/compatibility/V1_15_ISSUE25_RELEASE_READINESS_2026_11_09/logs'
REL = 'common/ai_strategies/00_default_strategy.txt'
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/compatibility')]
from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from issue24_map_dlc_audit import Audit, with_ancestors, plain, bare
from audit_1776_runtime_logs import messages, signature


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode('utf-8')).hexdigest()


def write_json(name, data):
    path = LOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def protect():
    hashes = {}
    for folder in ('common', 'events', 'gui', 'localization', 'map_data',
                   'docs/reports/map/SERG_CLOSURE', 'docs/reports/map/WORLD_1776_CLOSURE'):
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and path.suffix.lower() in ('.txt', '.gui', '.yml', '.png', '.json', '.md'):
                hashes[path.relative_to(ROOT).as_posix()] = sha(path.read_bytes())
    for rel in ('descriptor.mod', '.metadata/metadata.json'):
        hashes[rel] = sha((ROOT / rel).read_bytes())
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    return {'hashes': hashes,
            'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, env=env, text=True).strip(),
            'index': sha((ROOT / '.git/index').read_bytes())}


def target(raw, building):
    found = []
    for node, ancestors in with_ancestors(parse(raw)):
        if node.key == 'is_building_type' and node.value == building:
            parent = ancestors[-1]
            path = [a.key for a in ancestors]
            if path[:3] == ['ai_strategy_default', 'secret_goal_scores', 'befriend']:
                levels = parent.children('level')
                if len(levels) != 1:
                    raise ValueError('Expected one level check in target building predicate')
                found.append((node, levels[0], parent, path))
    if len(found) != 1:
        raise ValueError(f'Expected exactly one scoped {building} target, found {len(found)}')
    return found[0]


def logs():
    rows, counts, sources = [], Counter(), {}
    all_entries = 0
    for path in sorted(LOGS.glob('error*.log')):
        sources[path.name] = sha(path.read_bytes())
        for line, component, message in messages(path.read_text(encoding='utf-8-sig', errors='replace')):
            all_entries += 1
            if 'common/ai_strategies/' not in message and 'common/scripted_triggers/00_ai_triggers.txt' not in message:
                continue
            if "Event target link 'region'" in message:
                family = 'region_link_invalid_historical_runtime'
            elif 'building_naval_base' in message:
                family = 'removed_naval_building'
            elif 'ai_strategy_confrontation_agenda' in message or 'ai_strategy_consolidation_agenda' in message:
                family = 'missing_political_strategy'
            elif 'je_state_and_revolution' in message:
                family = 'journal_restored_by_39_awaiting_runtime'
            elif 'je_social_revolution' in message:
                family = 'unported_social_revolution_dependency'
            elif 'law_revolutionary_guard' in message:
                family = 'unported_revolutionary_guard_dependency'
            elif 'PostValidate' in message:
                family = 'postvalidation_secondary_message_no_id'
            elif 'should be in utf8-bom' in message:
                family = 'preexisting_encoding_warning'
            else:
                family = 'unclassified_ai_diagnostic'
            counts[family] += 1
            rows.append({'log': path.name, 'line': line, 'component': component,
                         'family': family, 'message': message, 'signature': signature(component, message)})
    grouped = defaultdict(lambda: {'count': 0, 'examples': []})
    for row in rows:
        item = grouped[row['signature']]
        item['count'] += 1
        item['family'] = row['family']
        item['message'] = row['message']
        if len(item['examples']) < 3:
            item['examples'].append(f"{row['log']}:{row['line']}")
    return {'source': str(LOGS), 'source_hashes': sources, 'all_error_entries': all_entries,
            'selected_ai_entries': len(rows), 'family_counts': dict(counts),
            'signatures': dict(grouped), 'rows': rows,
            'fresh_agent_engine_run': False,
            'limit': 'Preserved rotated logs; message counts are not independent bugs or current runtime observations.'}


def context():
    audit = Audit(ROOT, GAME)
    pools = {}
    for cat, folder in [('strategies', 'common/ai_strategies'), ('buildings', 'common/buildings'),
                        ('laws', 'common/laws'), ('journals', 'common/journal_entries'),
                        ('regions', 'common/strategic_regions'), ('states', 'map_data/state_regions')]:
        pools[cat] = audit.load(cat, folder)
    literal_fields = {'has_strategy': 'strategies', 'is_building_type': 'buildings',
                      'has_journal_entry': 'journals'}
    refs, unresolved = [], []
    paths = audit.paths('common/ai_strategies')
    paths += [GAME / 'common/scripted_triggers/00_ai_triggers.txt']
    for path in paths:
        nodes, raw, source = audit.read(path)
        for node, ancestors in with_ancestors(nodes):
            category = literal_fields.get(node.key)
            value = plain(node.value)
            if category and value:
                row = {'category': category, 'target': value, 'source': source,
                       'line': raw.count('\n', 0, node.start) + 1,
                       'owner': ancestors[0].key if ancestors else None,
                       'providers': [x[1] for x in pools[category].get(value, [])]}
                refs.append(row)
                if not row['providers']:
                    unresolved.append(row)
    lookup = {}
    for cat, keys in [('strategies', ['ai_strategy_confrontation_agenda', 'ai_strategy_consolidation_agenda']),
                      ('buildings', ['building_naval_base', 'building_naval_administration']),
                      ('journals', ['je_state_and_revolution', 'je_social_revolution']),
                      ('laws', ['law_revolutionary_guard'])]:
        lookup[cat] = {key: [x[1] for x in pools[cat].get(key, [])] for key in keys}
    membership = defaultdict(list)
    for key, defs in pools['regions'].items():
        for node, source, raw in defs:
            for group in node.children('states'):
                for state in bare(group):
                    membership[state].append(key)
    land = [key for key, defs in pools['states'].items() if defs[0][0].one('subsistence_building') is not None]
    invalid = {key: membership[key] for key in land if len(membership[key]) != 1}
    return {'counts': {cat: len(pool) for cat, pool in pools.items()},
            'parse_errors': audit.errors, 'lookups': lookup, 'references': refs, 'unresolved': unresolved,
            'land_states': len(land), 'invalid_strategic_memberships': invalid,
            'four_repaired_memberships': {key: membership[key] for key in
                ('STATE_TARTARIA', 'STATE_GALICH', 'STATE_KAUNAS', 'STATE_CHUKOTKA')},
            'input_hashes': audit.hashes,
            'limit': 'AI strategies and one native AI-trigger file only; no full transitive DLC reachability, historical sovereignty or engine execution proof.'}


def prepare():
    LOT.mkdir(parents=True, exist_ok=True)
    before = (ROOT / REL).read_bytes()
    native = (GAME / REL).read_bytes()
    raw, vraw = before.decode('utf-8-sig'), native.decode('utf-8-sig')
    old_b, old_level, parent, path = target(raw, 'building_naval_base')
    new_b, new_level, native_parent, native_path = target(vraw, 'building_naval_administration')
    assert path == native_path and old_level.value == '15' and new_level.value == '3'
    assert old_level.op == new_level.op == '>='
    replacements = []
    for old, new in ((old_b, new_b), (old_level, new_level)):
        start = old.end - len(old.value)
        assert raw[start:old.end] == old.value
        replacements.append({'start': start, 'end': old.end, 'before': old.value, 'after': new.value})
    candidate = raw
    for change in sorted(replacements, key=lambda x: -x['start']):
        candidate = candidate[:change['start']] + change['after'] + candidate[change['end']:]
    candidate_bytes = (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + candidate.encode('utf-8')
    for label, content in [('before', before), ('candidate', candidate_bytes), ('native', native)]:
        p = LOT / label / REL
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as handle:
            handle.write(content)
    contract = {'path': REL, 'replacements': replacements, 'context_path': path,
                'before_sha256': sha(before), 'candidate_sha256': sha(candidate_bytes),
                'native_sha256': sha(native), 'before_line': raw.count('\n', 0, old_b.start) + 1,
                'native_line': vraw.count('\n', 0, new_b.start) + 1,
                'native_predicate': normalized(native_parent.children()),
                'game_version': subprocess.check_output(['powershell', '-NoProfile', '-Command',
                    "(Get-Item -LiteralPath 'C:/Games/Victoria 3/binaries/victoria3.exe').VersionInfo.ProductVersion"], text=True).strip()}
    write_json('BASELINE.json', protect())
    write_json('CONTRACT.json', contract)
    write_json('HISTORICAL_LOG_TRIAGE.json', logs())
    write_json('CONTEXT_BEFORE.json', context())
    print(json.dumps({'prepared': True, 'changes': replacements, 'native_source_line': contract['native_line']}, indent=2))


def audit(content=None):
    contract = json.loads((LOT / 'CONTRACT.json').read_text(encoding='utf-8'))
    before = (LOT / 'before' / REL).read_bytes()
    data = content if content is not None else (ROOT / REL).read_bytes()
    checks = []
    def check(name, passed):
        checks.append({'check': name, 'pass': bool(passed)})
    check('captured_source_unchanged', sha(before) == contract['before_sha256'])
    check('canonical_native_source_unchanged', sha((GAME / REL).read_bytes()) == contract['native_sha256'])
    expected = before.decode('utf-8-sig')
    for change in sorted(contract['replacements'], key=lambda x: -x['start']):
        expected = expected[:change['start']] + change['after'] + expected[change['end']:]
    expected_bytes = (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + expected.encode('utf-8')
    check('only_two_authorized_value_spans', data == expected_bytes)
    check('candidate_hash_matches', sha(data) == contract['candidate_sha256'])
    check('bom_preserved', data.startswith(b'\xef\xbb\xbf') == before.startswith(b'\xef\xbb\xbf'))
    raw = data.decode('utf-8-sig')
    try:
        parse(raw)
        check('syntax', True)
        building, level, parent, path = target(raw, 'building_naval_administration')
        check('building_type', building.value == 'building_naval_administration')
        check('native_threshold_and_operator', level.value == '3' and level.op == '>=')
        check('original_context_preserved', path == contract['context_path'])
        check('native_predicate_equivalence', json.dumps(normalized(parent.children())) == json.dumps(contract['native_predicate']))
    except ValueError as exc:
        check('syntax_or_target: ' + str(exc), False)
    check('no_removed_building_reference', not re.search(r'\bbuilding_naval_base\b', raw))
    # Exact reverse reconstruction proves every unrelated byte, including all
    # geography and the accepted naval-availability rules, is preserved.
    if data == expected_bytes:
        current = raw
        for change in sorted(contract['replacements'], key=lambda x: x['start']):
            current = current[:change['start']] + change['before'] + current[change['start'] + len(change['after']):]
        check('reverse_byte_reconstruction', current == before.decode('utf-8-sig'))
    else:
        check('reverse_byte_reconstruction', False)
    errors = [c for c in checks if not c['pass']]
    return {'status': 'PASS_STATIC_ONLY' if not errors else 'FAIL_STATIC',
            'passed': len(checks) - len(errors), 'total': len(checks), 'checks': checks,
            'errors': errors, 'engine_tested': False}


def negatives():
    good = (LOT / 'candidate' / REL).read_bytes()
    raw = good.decode('utf-8-sig')
    b, level, parent, path = target(raw, 'building_naval_administration')
    def change(node, replacement):
        start = node.end - len(node.value)
        return raw[:start] + replacement + raw[node.end:]
    tests = {
        'old_removed_building': change(b, 'building_naval_base'),
        'old_level_15': change(level, '15'),
        'wrong_new_building': change(b, 'building_port'),
        'zero_level_threshold': change(level, '0'),
        'unrelated_geography_changed': raw.replace('region = sr:region_northeast_asia', 'region = sr:region_russia', 1),
        'unrelated_default_value_changed': raw.replace('value = 100', 'value = 101', 1),
        'broken_syntax': raw + '\n}',
    }
    rows = []
    prefix = b'\xef\xbb\xbf' if good.startswith(b'\xef\xbb\xbf') else b''
    for name, value in tests.items():
        bad = prefix + value.encode('utf-8')
        result = audit(bad)
        rows.append({'case': name, 'input_changed': bad != good,
                     'detected': result['status'] == 'FAIL_STATIC', 'errors': result['errors']})
    return {'detected': sum(r['detected'] and r['input_changed'] for r in rows),
            'total': len(rows), 'cases': rows}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepare', action='store_true')
    p.add_argument('--candidate', action='store_true')
    p.add_argument('--negative-controls', action='store_true')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.prepare:
        prepare()
        return
    result = audit((LOT / 'candidate' / REL).read_bytes() if args.candidate else None)
    if args.negative_controls:
        result['negative_controls'] = negatives()
    if args.output:
        destination = args.output.resolve()
        if not destination.is_relative_to(LOT):
            p.error('Output must remain inside this mission evidence directory')
        write_json(str(destination.relative_to(LOT)), result)
    print(json.dumps(result, indent=2))
    if result['status'] != 'PASS_STATIC_ONLY' or (args.negative_controls and result['negative_controls']['detected'] != result['negative_controls']['total']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
