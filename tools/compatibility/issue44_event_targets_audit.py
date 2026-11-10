"""Read-only event-provider inventory and scoped restoration checks for #44.

Writes one new evidence JSON. Candidate overlays and negative controls remain
in memory; this tool has no runtime installer or Git operation.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, walk, plain, with_ancestors

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_ISSUE44_EVENT_TARGETS_2026_11_09'
SPEC = {
    'russia_monarchy.12': ('events/russia_events.txt', 'events/zz_1776_v115_event44_russian_accession.txt'),
    'ip4_coup.11': ('events/iberia_events/ip4_coup_events.txt', 'events/zz_1776_v115_event44_foreign_coup.txt'),
    'set_hierarchy_event.3': ('events/india_events/set_hierarchy_events.txt', 'events/zz_1776_v115_event44_edo_hierarchy.txt'),
}
FOLDERS = {'journals': 'common/journal_entries', 'effects': 'common/scripted_effects',
           'triggers': 'common/scripted_triggers', 'modifiers': 'common/static_modifiers',
           'lobbies': 'common/political_lobbies', 'hierarchies': 'common/social_hierarchies',
           'messages': 'common/messages'}


def payload(nodes):
    return [(n.key, n.op, payload(n.value) if isinstance(n.value, list) else n.value) for n in nodes]


def references(audit, events):
    rows, dynamic = [], []
    for folder in ('events', 'common/on_actions', 'common/scripted_effects', 'common/scripted_buttons', 'common/decisions'):
        for path in audit.paths(folder):
            nodes, raw, source = audit.read(path)
            for node, ancestors in with_ancestors(nodes):
                if node.key != 'trigger_event':
                    continue
                target = plain(node.one('id')) if isinstance(node.value, list) else plain(node.value)
                row = {'target': target, 'source': source, 'line': raw.count('\n', 0, node.start) + 1,
                       'ancestors': [n.key for n in ancestors]}
                (dynamic if not target or any(c in target for c in '$[]@') else rows).append(row)
    return {'event_count': len(events), 'literal_count': len(rows), 'literal_references': rows,
            'missing': [r for r in rows if r['target'] not in events], 'dynamic': dynamic,
            'parse_errors': audit.errors,
            'limits': 'Only explicit trigger_event calls in five script families; not on_action event lists, '
                      'dynamic expansion, journal outcomes or runtime reachability.'}


def localization_catalogue(lang):
    local = {p.relative_to(ROOT).as_posix().casefold(): p for p in (ROOT / 'localization' / lang).rglob('*.yml')}
    paths = [p for p in (GAME / 'localization' / lang).rglob('*.yml')
             if p.relative_to(GAME).as_posix().casefold() not in local] + list(local.values())
    rows = {}
    for path in paths:
        raw = path.read_text(encoding='utf-8-sig')
        for match in re.finditer(r'^\s*([\w.]+):\d*\s+"(.*)"[ \t]*(?:#[^\r\n]*)?$', raw, re.MULTILINE):
            rows.setdefault(match.group(1), []).append({'value': match.group(2), 'source': str(path)})
    return rows


def verify(events, native_nodes, objects, native_helpers, locs, literal_rows):
    checks, dependencies, localization = [], [], []

    def check(name, value):
        checks.append({'name': name, 'pass': bool(value)})

    check('all_literal_event_targets_resolve', all(r['target'] in events for r in literal_rows))
    gui = ROOT / 'gui/eventwindow.gui'
    if not gui.exists():
        gui = GAME / 'gui/eventwindow.gui'
    gui_text = gui.read_text(encoding='utf-8-sig')
    for key in SPEC:
        entries = events.get(key, [])
        check(key + '.unique_provider', len(entries) == 1)
        if len(entries) != 1:
            continue
        node = entries[0][0]
        check(key + '.exact_native_payload', payload([node]) == payload([native_nodes[key]]))
        required_names = []
        for field in ('title', 'desc', 'flavor'):
            value = plain(node.one(field))
            if value:
                required_names.append(value)
        required_names.extend(plain(n.one('name')) for n in node.children('option'))
        for child in walk([node]):
            category, target = None, None
            if child.key in ('has_journal_entry', 'add_journal_entry'):
                category = 'journals'
                target = plain(child.one('type')) if isinstance(child.value, list) else plain(child.value)
            elif child.key == 'add_modifier':
                category, target = 'modifiers', plain(child.one('name'))
            elif child.key == 'is_political_lobby_type':
                category, target = 'lobbies', plain(child.value)
            elif child.key == 'set_social_hierarchy':
                category, target = 'hierarchies', plain(child.value)
            elif child.key == 'post_notification':
                category, target = 'messages', plain(child.value)
                if target:
                    required_names.extend(['notification_' + target + '_name',
                                           'notification_' + target + '_desc'])
            elif child.key in native_helpers:
                category, target = native_helpers[child.key][0], child.key
            if category and target:
                providers = objects[category].get(target, [])
                check(key + '.' + category + '.' + target, len(providers) == 1)
                row = {'event': key, 'category': category, 'target': target,
                       'providers': [r[1] for r in providers]}
                if category in ('effects', 'triggers') and len(providers) == 1:
                    same = payload([providers[0][0]]) == payload([native_helpers[target][1]])
                    row['native_payload_equal'] = same
                    check(key + '.native_helper_payload.' + target, same)
                dependencies.append(row)
                if category == 'messages' and len(providers) == 1:
                    texture = plain(providers[0][0].one('texture'))
                    check(key + '.notification_texture', bool(texture) and
                          ((ROOT / texture).exists() or (GAME / texture).exists()))
            if child.key == 'custom_tooltip':
                value = plain(child.one('text')) if isinstance(child.value, list) else plain(child.value)
                if value:
                    required_names.append(value)
        window = plain(node.one('gui_window'))
        if window:
            check(key + '.gui_window', bool(re.search(r'name\s*=\s*"' + re.escape(window) + '"', gui_text)))
        icon = plain(node.one('icon'))
        if icon:
            check(key + '.icon', (ROOT / icon).exists() or (GAME / icon).exists())
        for lang, catalogue in locs.items():
            pending, visited = list(filter(None, required_names)), set()
            while pending:
                name = pending.pop()
                if name in visited:
                    continue
                visited.add(name)
                rows = catalogue.get(name, [])
                check(key + '.' + lang + '.' + name, len(rows) == 1)
                localization.append({'event': key, 'language': lang, 'key': name, 'providers': rows})
                if len(rows) == 1:
                    pending.extend(re.findall(r'\$([a-zA-Z0-9_.]+)\$', rows[0]['value']))
    return checks, dependencies, localization


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--native', action='store_true')
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        parser.error('Use a new output path within the issue 44 evidence directory.')
    if args.native and (not args.inventory or args.candidate):
        parser.error('--native is an inventory-only control.')
    audit = Audit(ROOT, GAME, args.native)
    events = audit.load('events', 'events')
    if args.candidate:
        for key, (_, dst) in SPEC.items():
            for node in parse((EVIDENCE / 'candidate' / dst).read_text(encoding='utf-8-sig')):
                if isinstance(node.value, list):
                    events.setdefault(node.key, []).append((node, 'candidate/' + dst, ''))
    inventory = references(audit, events)
    result = {'inventory': inventory, 'engine_tested': False}
    if not args.inventory:
        objects = {category: audit.load(category, folder) for category, folder in FOLDERS.items()}
        native_audit = Audit(ROOT, GAME, True)
        native_events = native_audit.load('events', 'events')
        native_nodes = {key: native_events[key][0][0] for key in SPEC}
        native_helpers = {}
        for category in ('effects', 'triggers'):
            for key, entries in native_audit.load(category, FOLDERS[category]).items():
                if len(entries) == 1:
                    native_helpers[key] = (category, entries[0][0])
        locs = {lang: localization_catalogue(lang) for lang in ('english', 'french')}
        checks, deps, loc_rows = verify(events, native_nodes, objects, native_helpers, locs, inventory['literal_references'])
        checks.append({'name': 'parsed_inputs_valid', 'pass': not audit.errors})
        controls = []
        if args.controls:
            for key in SPEC:
                missing = dict(events)
                missing.pop(key)
                found, _, _ = verify(missing, native_nodes, objects, native_helpers, locs, inventory['literal_references'])
                failed = [r['name'] for r in found if not r['pass']]
                controls.append({'name': 'missing.' + key, 'detected_by': failed, 'pass': bool(failed)})
            corrupt = copy.deepcopy(events)
            corrupt['russia_monarchy.12'][0][0].children('duration')[0].value = '99'
            found, _, _ = verify(corrupt, native_nodes, objects, native_helpers, locs, inventory['literal_references'])
            failed = [r['name'] for r in found if not r['pass']]
            controls.append({'name': 'changed_russian_payload', 'detected_by': failed,
                             'pass': 'russia_monarchy.12.exact_native_payload' in failed})
            missing_message = dict(objects)
            missing_message['messages'] = dict(objects['messages'])
            missing_message['messages'].pop('edo_system_disappears', None)
            found, _, _ = verify(events, native_nodes, missing_message, native_helpers, locs, inventory['literal_references'])
            failed = [r['name'] for r in found if not r['pass']]
            controls.append({'name': 'missing_edo_notification', 'detected_by': failed,
                             'pass': 'set_hierarchy_event.3.messages.edo_system_disappears' in failed})
            missing_alias = dict(locs)
            missing_alias['french'] = dict(locs['french'])
            missing_alias['french'].pop('russia_monarchy.9.f', None)
            found, _, _ = verify(events, native_nodes, objects, native_helpers, missing_alias, inventory['literal_references'])
            failed = [r['name'] for r in found if not r['pass']]
            controls.append({'name': 'missing_russian_flavor_alias', 'detected_by': failed,
                             'pass': 'russia_monarchy.12.french.russia_monarchy.9.f' in failed})
            missing_lobby = dict(objects)
            missing_lobby['lobbies'] = dict(objects['lobbies'])
            missing_lobby['lobbies'].pop('lobby_pro_overlord', None)
            found, _, _ = verify(events, native_nodes, missing_lobby, native_helpers, locs, inventory['literal_references'])
            failed = [r['name'] for r in found if not r['pass']]
            controls.append({'name': 'missing_coup_lobby_type', 'detected_by': failed,
                             'pass': 'ip4_coup.11.lobbies.lobby_pro_overlord' in failed})
        presentation = {Path(p['source']) for row in loc_rows for p in row['providers']}
        gui = ROOT / 'gui/eventwindow.gui'
        presentation.add(gui if gui.exists() else GAME / 'gui/eventwindow.gui')
        for key in SPEC:
            if len(events.get(key, [])) == 1:
                icon = plain(events[key][0][0].one('icon'))
                if icon:
                    presentation.add(ROOT / icon if (ROOT / icon).exists() else GAME / icon)
        for row in deps:
            if row['category'] == 'messages':
                entries = objects['messages'].get(row['target'], [])
                if len(entries) == 1:
                    texture = plain(entries[0][0].one('texture'))
                    if texture:
                        presentation.add(ROOT / texture if (ROOT / texture).exists() else GAME / texture)
        result.update({'checks': checks, 'dependencies': deps, 'localization': loc_rows, 'controls': controls,
                       'presentation_source_hashes': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                                      for p in presentation},
                       'native_reference_hashes': native_audit.hashes,
                       'status': 'PASS_STATIC_ONLY' if all(r['pass'] for r in checks + controls) else 'FAIL_STATIC'})
    else:
        result['status'] = 'FINDINGS_STATIC_ONLY' if inventory['missing'] or inventory['parse_errors'] else 'PASS_STATIC_ONLY'
    result['source_hashes'] = audit.hashes
    with output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'events': inventory['event_count'],
                      'literal_calls': inventory['literal_count'], 'missing': inventory['missing'],
                      'dynamic_calls': len(inventory['dynamic']),
                      'checks': [sum(r['pass'] for r in result.get('checks', [])), len(result.get('checks', []))],
                      'controls': [sum(r['pass'] for r in result.get('controls', [])), len(result.get('controls', []))],
                      'failed': [r['name'] for r in result.get('checks', []) if not r['pass']]}))
    return 1 if result['status'] == 'FAIL_STATIC' else 0


if __name__ == '__main__':
    raise SystemExit(main())
