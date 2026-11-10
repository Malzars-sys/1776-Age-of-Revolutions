"""Consolidate preserved release-review evidence; never launch or modify the game.

Reads the explicit evidence directory, including its copied logs. The original
scoped validators and their failed assertions remain unchanged in that directory.
"""
from pathlib import Path
import argparse
import collections
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def leaf_values(nodes, prefix=''):
    result = {}
    counts = collections.Counter()
    for node in nodes:
        occurrence = counts[node.key]
        counts[node.key] += 1
        key = f'{prefix}/{node.key}[{occurrence}]'
        if isinstance(node.value, list):
            result.update(leaf_values(node.children(), key))
        else:
            result[key] = node.value
    return result


def reconcile_copper_drift():
    copper = module('release_copper_audit', ROOT / 'tools/compatibility/issue31_copper_alignment_audit.py')
    prior = {n.key: n for n in copper.parse((copper.LOT / 'before' / copper.PMS).read_text(encoding='utf-8-sig'))}
    current = {n.key: n for n in copper.parse((ROOT / copper.PMS).read_text(encoding='utf-8-sig'))}
    differences = []
    for key in sorted((prior.keys() | current.keys()) - set(copper.METHODS)):
        old = leaf_values(prior[key].children()) if key in prior else {}
        new = leaf_values(current[key].children()) if key in current else {}
        fields = [{'field': field, 'before': old.get(field), 'current': new.get(field)}
                  for field in sorted(old.keys() | new.keys()) if old.get(field) != new.get(field)]
        if fields:
            differences.append({'id': key, 'fields': fields})
    return {
        'file': copper.PMS,
        'changed_nonstandard_methods': differences,
        'all_differences_are_icon_paths': bool(differences) and all(
            re.fullmatch(r'/(texture|icon)\[0\]', field['field'])
            for item in differences for field in item['fields']),
        'original_validator_failure_retained': True,
        'engine_effect_observed': False,
    }


def logs(evidence):
    reader = module('release_runtime_log_reader', ROOT / 'tools/audit_1776_runtime_logs.py')
    manifest = read_json(evidence / 'LOG_SNAPSHOT.json')
    entries = []
    unique = {}
    components = collections.Counter()
    paths = collections.Counter()
    families = collections.Counter()
    for item in manifest:
        if not re.fullmatch(r'error(?:\.[1-5])?\.log', item['name']):
            continue
        raw = (evidence / 'logs' / item['name']).read_text(encoding='utf-8-sig', errors='replace')
        for line, component, message in reader.messages(raw):
            components[component] += 1
            signature = reader.signature(component, message)
            normalized = message.replace('\\', '/')
            sources = sorted(set(re.findall(r'(?:common|events|gui|map_data|localization)/[^\s,:\]"\']+\.(?:txt|gui|yml)', normalized)))
            for path in sources:
                paths[path] += 1
            if 'Duplicate localization key' in message:
                family = 'duplicate_localization'
            elif 'does not match game version' in message:
                family = 'launcher_version_warning'
            elif 'should be in utf8-bom' in message:
                family = 'encoding_warning'
            elif 'common/journal_entries/' in normalized and re.search(r'(?:Unexpected token:|Unknown (?:key|token):|Invalid (?:key|token):)\s*[\'\"]?(?:complete|on_complete|fail|on_fail|on_timeout|invalid|on_invalid)\b', message):
                family = 'legacy_journal_conclusions'
            elif 'Event target link' in message or 'Invalid ' in message or 'is not valid' in message:
                family = 'invalid_scope_or_target'
            elif re.search(r'Unknown|Unexpected|not found|not in code|does not exist', message):
                family = 'unresolved_key_or_reference'
            else:
                family = 'other_engine_diagnostic'
            families[family] += 1
            entry = unique.setdefault(signature, {'count': 0, 'family': family, 'component': component,
                                                   'message': message, 'locations': [], 'source_paths': sources})
            entry['count'] += 1
            if len(entry['locations']) < 4:
                entry['locations'].append(f"{item['name']}:{line}")
            entries.append(signature)
    return {'source': 'explicit copied error logs, not mutable live selection',
            'entries': len(entries), 'distinct_normalized_signatures': len(unique),
            'components': dict(components.most_common()), 'families': dict(families.most_common()),
            'source_paths': dict(paths.most_common()),
            'diagnostics': sorted(unique.values(), key=lambda item: (-item['count'], item['component'], item['message'])),
            'raw_vanilla_baseline_supplied': False,
            'limits': 'Counts are retained diagnostic messages, not distinct bugs or a crash count. Repeated sources and rotated logs are not independent test sessions. Full baseline reduction is not certified.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    if not evidence.is_relative_to(ROOT / 'docs/reports/compatibility'):
        parser.error('Evidence must be in the repository compatibility reports directory.')
    result = {'status': 'RELEASE_REVIEW_FINDINGS_ONLY', 'logs': logs(evidence),
              'copper_drift': reconcile_copper_drift(),
              'agent_engine_run': False, 'release_approved': False}
    destination = evidence / 'INTEGRATED_TRIAGE.json'
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'log_entries': result['logs']['entries'],
                      'distinct_signatures': result['logs']['distinct_normalized_signatures'],
                      'families': result['logs']['families'],
                      'top_sources': dict(list(result['logs']['source_paths'].items())[:8]),
                      'copper_drift': result['copper_drift']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
