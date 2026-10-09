"""Read-only review of all Victoria 3 logs, including rotated files.

The last run starts at the mtime of code_revisions.log. Rotated logs from that
run are included. Historical logs are compared, not mistaken for new failures.
No files, saves or logs are changed. --save also examines the exit autosave.
"""
from pathlib import Path
import argparse
import collections
import datetime
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOGS = Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/logs')
SAVE = LOGS.parent / 'save games/autosave_exit.v3'
HEADER = re.compile(r'^\[[\d:.]+\]\[([^\]]+)\]:\s*(.*)')


def messages(raw):
    current = None
    for number, line in enumerate(raw.splitlines(), 1):
        match = HEADER.match(line)
        if match:
            if current:
                yield current
            current = [number, match[1].split(':')[0], match[2]]
        elif current and line.strip():
            current[2] += '\n' + line.strip()
    if current:
        yield current


def signature(component, message):
    # Country tooltip IDs/pointers differ every launch; compare the actual
    # script error and source, not the transient GUI payload.
    message = re.sub(r'\x15tooltip:\S+\s*', '', message)
    message = message.replace('\x15tooltippable_name ', '').replace('\x15!', '')
    message = re.sub(r'\x16([A-Z]{2,6})\d+!', r'\1 ', message)
    message = re.sub(r'\x16[a-z_]+!', '', message).replace('\xa0', ' ')
    message = re.sub(r'0x[0-9a-fA-F]+', 'ADDRESS', message)
    message = re.sub(r':\d+', ':LINE', message)
    message = re.sub(r'near line: \d+', 'near line: LINE', message)
    return component + ': ' + message


def logs():
    start = (LOGS / 'code_revisions.log').stat().st_mtime
    touched = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, stderr=subprocess.DEVNULL).decode().splitlines()
    touched += subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT).decode().splitlines()
    previous = set()
    current = collections.Counter()
    locations = {}
    related = {}
    inventory = []
    components = collections.Counter()
    texts = {}
    for path in sorted(LOGS.glob('*.log')):
        raw = path.read_text(encoding='utf-8-sig', errors='replace')
        texts[path.name] = raw
        latest = path.stat().st_mtime >= start - 2
        inventory.append({'file': path.name, 'bytes': path.stat().st_size,
                          'last_run': latest, 'lines': len(raw.splitlines())})
        for line, component, message in messages(raw):
            key = signature(component, message)
            if not latest:
                previous.add(key)
                continue
            # debug logs duplicate error messages; count them but preserve origin.
            components[component] += 1
            current[key] += 1
            locations.setdefault(key, []).append(f'{path.name}:{line}')
            matching = [p for p in touched if p in message.replace('\\', '/')]
            if matching or 'ottoman_1776' in message or 'je_1776_' in message:
                related.setdefault(key, {'files': matching, 'message': message})
    actionable = {key: count for key, count in current.items()
                  if any(word in key.lower() for word in ('error', 'invalid', 'failed', 'cannot', 'not valid',
                     'not found', 'already has', 'wrong type', 'unlocalized', 'missing', 'never', 'orphan',
                     'not in code', 'defined twice', 'duplicate', 'does not match', 'should be',
                     'unknown', 'unexpected', 'unsupported', 'will not', 'no ai_weight'))}
    return {'run_start_local': datetime.datetime.fromtimestamp(start).isoformat(),
            'files_read': inventory, 'message_components': dict(components),
            'changed_file_messages': [{'count': current[key], 'seen_in_older_logs': key in previous,
                                      'locations': locations[key][:4], **value} for key, value in related.items()],
            'diagnostic_messages': [{'count': count, 'seen_in_older_logs': key in previous,
                                    'locations': locations[key][:3], 'message': key}
                                   for key, count in sorted(actionable.items(), key=lambda x: (-x[1], x[0]))]}


def section(raw, name):
    match = re.search(r'^' + re.escape(name) + r'=\{', raw, re.M)
    if not match:
        return ''
    depth = 1
    # Managers contain unindented database blocks: indentation alone cannot
    # delimit them. Count braces, ignoring braces inside quoted strings.
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|[{}]', raw[match.end():]):
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return raw[match.start():match.end() + token.end()]
    raise ValueError('Unclosed save manager: ' + name)


def records(raw):
    for match in re.finditer(r'^(\d+)=\{\n(.*?)^\}', raw, re.M | re.S):
        yield int(match[1]), match[2]


def field(raw, name):
    match = re.search(r'^\t' + name + r'=(.*)', raw, re.M)
    return match[1].strip('"') if match else None


def save():
    raw = SAVE.read_text(encoding='utf-8-sig')
    countries = {}
    important = {}
    for ident, block in records(section(raw, 'country_manager')):
        tag = field(block, 'definition')
        countries[ident] = tag
        if tag in ('TUR', 'EGY', 'PLC', 'CRI', 'GBR', 'HAN', 'FRA', 'AUS', 'SPA', 'POR', 'RUS'):
            important[tag] = {'id': ident, 'government': field(block, 'government'),
                              'ottoman_variables': re.findall(r'flag=(ottoman_1776_\w+)', block),
                              'ottoman_modifiers': re.findall(r'ottoman_1776_\w+', block[block.find('timed_modifiers='):block.find('timed_modifiers=')+2500]),
                              'states': field(block, 'states'),
                              'bloc_join_date': field(block, 'power_bloc_join_date'),
                              'bloc_leave_date': field(block, 'power_bloc_leave_date')}
    journals = []
    for ident, block in records(section(raw, 'journal_entry_manager')):
        key = field(block, 'type') or ''
        country = int(field(block, 'country') or -1)
        if key.startswith('je_1776_') and countries.get(country) == 'TUR':
            journals.append({'id': ident, 'type': key, 'country': countries.get(country),
                             'active': field(block, 'active'), 'goal_value': field(block, 'goal_value')})
    treaties = []
    articles = list(records(section(raw, 'treaty_article_manager')))
    for ident, block in records(section(raw, 'treaty_manager')):
        if any(k in block for k in ('treaty_1776_', 'treaty_name_mod_bourbon')):
            treaties.append({'id': ident, 'name': re.search(r'scripted_name="([^"]+)"', block)[1],
                             'first': countries.get(int(field(block, 'first_country'))),
                             'second': countries.get(int(field(block, 'second_country'))),
                             'date': field(block, 'entered_into_force_on'),
                             'articles': [{'type': field(b, 'article'),
                                           'source': countries.get(int(field(b, 'source_country'))),
                                           'target': countries.get(int(field(b, 'target_country')))}
                                          for _, b in articles if field(b, 'treaty') == str(ident)]})
    blocs = []
    for ident, block in records(section(raw, 'power_bloc_manager')):
        if any(k in block for k in ('ROSSIYSKAYA', 'BRITISH_EMPIRE', 'HOLY_ROMAN')):
            blocs.append({'id': ident, 'leader': countries.get(int(field(block, 'leader'))),
                          'date': field(block, 'founding_date'), 'identity': field(block, 'identity')})
    regions = {'STATE_LOWER_EGYPT', 'STATE_MIDDLE_EGYPT', 'STATE_UPPER_EGYPT', 'STATE_MATRUH', 'STATE_SINAI',
               'STATE_ALEPPO', 'STATE_SYRIA', 'STATE_LEBANON', 'STATE_PALESTINE', 'STATE_TRANSJORDAN'}
    states = [{'id': i, 'region': field(b, 'region'), 'country': countries.get(int(field(b, 'country'))),
               'incorporation': field(b, 'incorporation') or '0'}
              for i, b in records(section(raw, 'states')) if field(b, 'region') in regions]
    egypt_ids = {str(s['id']) for s in states if s['country'] == 'EGY'}
    egypt_buildings = [{'id': i, 'type': field(b, 'building'), 'state': field(b, 'state'),
                       'levels': field(b, 'levels'), 'methods': field(b, 'production_methods')}
                      for i, b in records(section(raw, 'building_manager')) if field(b, 'state') in egypt_ids]
    pacts = []
    for ident, block in records(section(raw, 'pacts')):
        targets = re.search(r'targets=\{\s*first=(\d+)\s*second=(\d+)', block)
        if (targets and targets.groups() in (('95', '465'), ('1', '47'))
                and field(block, 'action') in ('puppet', 'personal_union')):
            pacts.append({'id': ident, 'first': countries.get(int(targets[1])),
                          'second': countries.get(int(targets[2])), 'type': field(block, 'action')})
    metadata = re.search(r'game_date=(.*)', raw)
    return {'save': str(SAVE), 'date': metadata[1] if metadata else None,
            'countries': important, 'ottoman_journals': journals,
            'burden_occurrences': raw.count('ottoman_1776_admin_burden'),
            'treaties': treaties, 'blocs': blocs, 'states': states,
            'egypt_buildings': egypt_buildings, 'subjects': pacts}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()
    print(json.dumps(save() if args.save else logs(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
