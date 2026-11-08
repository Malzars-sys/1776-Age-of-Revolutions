"""Read-only game-data audit; --output writes evidence only into a new directory.

Models same-path file masking and top-level object directives. Starting laws are
script requests, not a claim about engine acceptance. Only two simple political
macros are expanded; other conditional initialization remains explicitly unknown.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

FOCUS = [
    'law_military_bureaucrats', 'law_caesaropapism',
    'law_official_nationality', 'law_third_section', 'law_okhrana',
    'law_internal_colonization', 'law_communal_administration',
    'law_labour_suffrage', 'law_revolutionary_guard',
    'law_extraordinary_commission',
]
TAGS = ['RUS', 'PLC', 'UBD', 'ALK', 'KZH', 'CRI']
PROFILE = {
    'RUS': 'rus - russia.txt', 'PLC': 'plc - polish-lithuania.txt',
    'UBD': 'ubd - baltic.txt', 'ALK': 'alk - alyaska.txt',
    'KZH': 'kzh - kishi zhuz.txt', 'CRI': 'cri - crimean khanate.txt',
}
INPUTS: dict[Path, bytes] = {}


def read(path):
    path = Path(path)
    if path not in INPUTS:
        INPUTS[path] = path.read_bytes()
    return INPUTS[path].decode('utf-8-sig')


def source(path):
    base = ROOT if path.is_relative_to(ROOT) else GAME
    return ('mod/' if base == ROOT else 'vanilla/') + path.relative_to(base).as_posix()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def effective_files(folder):
    """The descriptor currently replaces technology directories, not laws."""
    mod = {p.name: p for p in (ROOT / folder).glob('*.txt')}
    replacements = re.findall(r'replace_path\s*=\s*"([^"]+)"', read(ROOT / 'descriptor.mod'))
    replaced = any(folder == p or folder.startswith(p + '/') for p in replacements)
    files = {} if replaced else {p.name: p for p in (GAME / folder).glob('*.txt')}
    files.update(mod)
    return [files[k] for k in sorted(files)]


def catalog(files):
    result, directives, duplicates = {}, [], []
    for path in files:
        raw = read(path)
        for node in parse(raw):
            if not node.key or not isinstance(node.value, list):
                continue
            key = node.key
            if ':' in key:
                directive, key = key.split(':', 1)
                directives.append({'directive': directive, 'id': key, 'source': source(path)})
                if directive == 'INJECT_OR_CREATE' and key in result:
                    continue  # Existing object's identity/group stays in place.
                if directive not in ('INJECT_OR_CREATE', 'REPLACE_OR_CREATE'):
                    continue
            elif key in result:
                duplicates.append({'id': key, 'sources': [source(result[key][0]), source(path)]})
            result[key] = path, node
    return result, directives, duplicates


def fields(path, node, wanted):
    raw = read(path)
    return {c.key: raw[c.start:c.end] for c in node.children() if c.key in wanted}


def atoms(node, key):
    found = node.children(key)
    return [str(c.value) for c in found[0].children() if not c.key] if found else []


def main(output=None):
    native, _, _ = catalog(sorted((GAME / 'common/laws').glob('*.txt')))
    laws, directives, duplicates = catalog(effective_files('common/laws'))
    effects, _, _ = catalog(effective_files('common/scripted_effects'))
    definitions, _, _ = catalog(effective_files('common/country_definitions'))
    cultures, _, _ = catalog(effective_files('common/cultures'))
    techs, _, _ = catalog(effective_files('common/technology/technologies'))
    amendments, _, _ = catalog(effective_files('common/amendments'))
    loc = dict(re.findall(r'^\s+(law_[\w]+):(?:\d+)?\s*"([^"\n]*)"',
                         read(GAME / 'localization/french/laws_l_french.yml'), re.M))
    focus = []
    for law in FOCUS:
        path, node = native[law]
        required = atoms(node, 'unlocking_technologies')
        gates = {}
        for tech in required:
            tp, tn = techs[tech]
            gates[tech] = {'source': source(tp), 'era': tn.one('era'),
                           'can_research': tn.one('can_research', 'not_explicitly_disabled'),
                           'prerequisites': atoms(tn, 'unlocking_technologies')}
        focus.append({
            'id': law, 'french': loc.get(law), 'group': node.one('group'),
            'parent': node.one('parent'), 'native_source': source(path),
            'effective_source': source(laws[law][0]) if law in laws else None,
            'status': 'DEFINED' if law in laws else 'MISSING_MASKED',
            'masked_by': source(ROOT / path.relative_to(GAME))
                         if law not in laws and (ROOT / path.relative_to(GAME)).exists() else None,
            'native_conditions': fields(path, node, {'is_visible', 'can_enact',
                                                       'unlocking_laws', 'unlocking_technologies'}),
            'technology_gates': gates,
        })

    # All subject-pact candidates are recorded, with branch ancestry. This does
    # not evaluate conditional startup effects or determine sovereign history.
    pacts = []
    for path in effective_files('common/history/diplomacy'):
        def visit(nodes, owner=None, ancestry=()):
            for n in nodes:
                country = n.key[2:] if n.key.startswith('c:') else owner
                if n.key == 'create_diplomatic_pact' and country:
                    pacts.append({'overlord_candidate': country,
                                  'country': n.one('country'), 'type': n.one('type'),
                                  'source': source(path), 'ancestry': list(ancestry)})
                visit(n.children(), country, ancestry + (n.key,))
        visit(parse(read(path)))
    subject_types, _, _ = catalog(effective_files('common/subject_types'))
    russian_pacts = []
    reached = {'RUS'}
    while True:
        added = []
        for p in pacts:
            typ = p['type']
            if p['overlord_candidate'] in reached and typ and (
                typ in subject_types or 'subject_type_' + typ in subject_types
            ):
                target = str(p['country']).removeprefix('c:')
                if p not in russian_pacts:
                    russian_pacts.append(p)
                if target not in reached:
                    added.append(target)
        if not added:
            break
        reached.update(added)

    profiles = {}
    for tag in TAGS:
        path = ROOT / 'common/history/countries' / PROFILE[tag]
        raw = read(path)
        country = next(n for n in walk(parse(raw)) if n.key == 'c:' + tag)
        dp, definition = definitions[tag]
        primary = atoms(definition, 'cultures')
        # Initial religion is an inference from the first defined primary
        # culture; no runtime state-religion claim is made.
        religion = cultures[primary[0]][1].one('religion') if primary else None
        country_type = definition.one('country_type')
        requested, trace, unresolved = {}, [], []

        def expand(nodes, origin):
            last_condition = None
            for n in nodes:
                if n.key == 'activate_law':
                    law = str(n.value).removeprefix('law_type:')
                    if law not in laws:
                        unresolved.append({'missing_law': law, 'origin': origin})
                        continue
                    group = laws[law][1].one('group')
                    requested[group] = law
                    trace.append({'group': group, 'law': law, 'origin': origin})
                elif n.key.startswith('effect_starting_politics_'):
                    if n.key not in ('effect_starting_politics_conservative',
                                      'effect_starting_politics_traditional'):
                        unresolved.append({'unexpanded_macro': n.key})
                    else:
                        ep, en = effects[n.key]
                        expand(en.children(), source(ep) + ':' + n.key)
                elif n.key == 'if':
                    limit = n.children('limit')[0]
                    if limit.one('country_is_islamic') == 'yes':
                        last_condition = religion in ('sunni', 'shiite', 'ibadi')
                    elif limit.one('is_country_type') == 'decentralized':
                        last_condition = country_type == 'decentralized'
                    else:
                        last_condition = None
                        if any(c.key == 'activate_law' for c in walk(n.children())):
                            unresolved.append({'conditional_law_initialization': raw[n.start:n.end]
                                               if origin == source(path) else origin})
                    if last_condition is True:
                        expand([c for c in n.children() if c.key != 'limit'], origin)
                elif n.key == 'else' and last_condition is False:
                    expand(n.children(), origin)

        expand(country.children(), source(path))
        initial_amendments = []
        for active in country.children():
            if not active.key.startswith('active_law:'):
                continue
            for amend in active.children('add_amendment'):
                aid = amend.one('type')
                ap, an = amendments[aid]
                initial_amendments.append({'id': aid, 'group': active.key.split(':', 1)[1],
                                          'source': source(ap), 'allowed_laws': atoms(an, 'allowed_laws'),
                                          'possible': fields(ap, an, {'possible'})})
        profiles[tag] = {
            'source': source(path), 'country_type': country_type,
            'definition_source': source(dp), 'initial_primary_cultures_in_definition': primary,
            'religion_inferred_from_first_defined_primary_culture': religion,
            'requested_laws_after_two_supported_macros': requested,
            'activation_trace': trace, 'initial_amendments': initial_amendments,
            'directly_researched_technologies': [n.value for n in country.children('add_technology_researched')],
            'technology_macros_not_expanded': [n.key for n in country.children()
                                               if n.key.startswith('effect_starting_technology_')],
            'unknowns': unresolved,
            'limitation': 'Script requests only. Unmentioned groups and engine defaults are unknown; '
                          'technology macros, events and runtime acceptance are not simulated.',
        }

    ip5path = GAME / 'common/amendments/00_amendments_ip5_04.txt'
    ip5 = [{'id': n.key, 'effective_source': source(amendments[n.key][0])
            if n.key in amendments else None} for n in parse(read(ip5path)) if n.key]
    triggers, _, _ = catalog(effective_files('common/scripted_triggers'))
    tp, tn = triggers['country_is_subject_type_valid_for_caesaropapism']
    helper = read(tp)[tn.start:tn.end]
    blocpath = ROOT / 'common/history/power_blocs/00_power_blocs.txt'
    blocraw = read(blocpath)
    bloc = next(n for n in walk(parse(blocraw)) if n.key == 'c:RUS')
    # Retain the actual RUS bloc source, rather than inferring subjecthood.
    read(ROOT / 'common/defines/zz_1776_world_russia01.txt') if (ROOT / 'common/defines/zz_1776_world_russia01.txt').exists() else None
    version_candidates = [GAME.parent / 'binaries/victoria3.exe', GAME / 'version.txt']
    version = {str(p): p.stat().st_mtime for p in version_candidates if p.exists()}
    changed = [source(p) for p, data in INPUTS.items() if digest(p.read_bytes()) != digest(data)]
    report = {
        'status': 'AUDIT_ONLY_NO_GAMEPLAY_EDITS_RUNTIME_NOT_TESTED',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'canonical_game': str(GAME), 'version_file_metadata': version,
        'catalog_size': {'effective_laws': len(laws), 'native_laws': len(native)},
        'missing_native_laws_all': sorted(set(native) - set(laws)),
        'focus_laws': focus, 'law_directives': directives, 'duplicate_law_ids': duplicates,
        'countries': profiles, 'russian_subject_pact_candidates': russian_pacts,
        'russian_subject_closure_including_RUS': sorted(reached),
        'russian_bloc_source': blocraw[bloc.start:bloc.end],
        'caesaropapism_subject_helper': {'source': source(tp), 'script': helper},
        'native_ip5_amendments': ip5,
        'input_hashes': {source(p): digest(data) for p, data in sorted(INPUTS.items())},
        'changed_during_audit': changed,
        'snapshot_limit': 'Not an atomic engine snapshot; concurrent changes detected by final hashes are listed.',
    }
    if output:
        output = Path(output).resolve()
        if output.exists():
            raise SystemExit('Evidence directory must be new; previous evidence is never overwritten.')
        output.mkdir(parents=True)
        for p, data in INPUTS.items():
            target = output / 'inputs' / source(p)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (output / 'AUDIT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'status': report['status'], 'focus_missing': [f['id'] for f in focus if f['status'] == 'MISSING_MASKED'],
        'all_missing_native_laws': report['missing_native_laws_all'],
        'russian_subject_closure': sorted(reached), 'duplicate_laws': duplicates,
        'disabled_technology_gates': {f['id']: [k for k, v in f['technology_gates'].items()
                                                if v['can_research'] == 'no'] for f in focus
                                      if any(v['can_research'] == 'no' for v in f['technology_gates'].values())},
        'input_count': len(INPUTS), 'changed_during_audit': changed,
        'output': str(output) if output else None,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New evidence directory, never game-data files')
    main(parser.parse_args().output)
