"""Static contracts for the Russian law lot; never writes game data.

An explicit --output writes a new evidence file. Negative controls operate on
in-memory copies, not the workspace. Runtime enactment and IG clout remain untested.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk
from validate_starting_technology_1776 import collect_snapshot, audit_country

EVIDENCE = ROOT / 'docs/reports/compatibility/V1_15_RUSSIAN_LAWS_IMPLEMENTATION_2026_11_07'
RUS = 'common/history/countries/rus - russia.txt'
LAWS = 'common/laws/1776_v115_russian_laws.txt'
IDEOLOGY = 'common/ideologies/17_1776_russian_law_stances.txt'
AMEND = 'common/amendments/17_1776_russian_noble_legacy.txt'
LOC = {lang: f'localization/{lang}/1776_russian_laws_l_{lang}.yml'
       for lang in ('french', 'english')}
AID = 'amendment_aor1776_noble_legacy'


def signature(nodes):
    return [(n.key, n.op, signature(n.value) if isinstance(n.value, list) else n.value)
            for n in nodes]


def obj(raw, key):
    return next(n for n in parse(raw) if n.key == key)


def text(data):
    return data.decode('utf-8-sig')


def values(node, key):
    return [c.value for n in node.children(key) for c in n.children() if not c.key]


def expected_rus(before):
    raw = text(before)
    nl = '\r\n' if b'\r\n' in before else '\n'
    assert raw.count('activate_law = law_type:law_hereditary_bureaucrats') == 1
    raw = raw.replace('activate_law = law_type:law_hereditary_bureaucrats',
                      'activate_law = law_type:law_military_bureaucrats', 1)
    marker = '\t\tactivate_law = law_type:law_censorship' + nl
    block = nl + '\t\tactive_law:lawgroup_bureaucracy ?= {' + nl
    block += '\t\t\tadd_amendment = {' + nl
    block += '\t\t\t\ttype = ' + AID + nl
    block += '\t\t\t\tsponsor = PREV.ig:ig_landowners' + nl
    block += '\t\t\t}' + nl + '\t\t}' + nl
    assert raw.count(marker) == 1
    raw = raw.replace(marker, marker + block, 1)
    return (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + raw.encode('utf-8')


def contracts(payload, before):
    """Assert intended scope, availability, native effects, and transition."""
    law_nodes = parse(text(payload[LAWS]))
    assert {n.key for n in law_nodes} == {'law_third_section', 'law_official_nationality'}
    third = obj(text(payload[LAWS]), 'law_third_section')
    official = obj(text(payload[LAWS]), 'law_official_nationality')
    assert values(third, 'unlocking_technologies') == ['professional_civil_policing']
    assert values(official, 'unlocking_technologies') == [], 'Subjecthood variant must precede nationalism'
    assert third.one('parent') == 'law_secret_police'
    assert official.one('parent') == 'law_subjecthood'
    for law in (third, official):
        visible = law.children('is_visible')[0]
        assert visible.one('c:RUS') == 'this'
        assert not any(n.key in ('OR', 'always') for n in walk(visible.children()))
    assert third.children('is_visible')[0].one('country_has_monarchy_law') == 'yes'
    assert not third.children('is_visible')[0].children('NAND')
    # Compare native payloads after removing only the documented gate changes.
    native = EVIDENCE / 'native_inputs/common/laws'
    native_third = obj((native / '00_internal_security.txt').read_text(encoding='utf-8-sig'),
                       'law_third_section')
    native_official = obj((native / '00_citizenship.txt').read_text(encoding='utf-8-sig'),
                          'law_official_nationality')
    native_third.children('unlocking_technologies')[0].value[0].value = 'professional_civil_policing'
    visible = native_third.children('is_visible')[0]
    visible.value = [n for n in visible.children() if n.key != 'NAND']
    assert signature([third]) == signature([native_third]), 'Native Third Section payload changed'
    assert signature([official]) == signature([native_official]), 'Native nationality payload changed'

    current_tsarist = obj(text(payload[IDEOLOGY]), 'REPLACE:ideology_tsarist')
    assert current_tsarist.children('lawgroup_citizenship')[0].one('law_official_nationality') == 'approve'
    native_tsarist = obj((EVIDENCE / 'native_inputs/common/ideologies/00_ig_ideologies_flavored.txt')
                         .read_text(encoding='utf-8-sig'), 'ideology_tsarist')
    without_preference = copy.deepcopy(current_tsarist)
    without_preference.key = 'ideology_tsarist'
    without_preference.value = [n for n in without_preference.children()
                                if n.key != 'lawgroup_citizenship']
    assert signature([without_preference]) == signature([native_tsarist])

    amendment = obj(text(payload[AMEND]), AID)
    assert set(values(amendment, 'allowed_laws')) == {'law_military_bureaucrats', 'law_hereditary_bureaucrats'}
    assert amendment.one('parent') == 'law_military_bureaucrats'
    assert amendment.children('possible')[0].one('c:RUS') == 'this'
    assert amendment.children('modifier')[0].one('interest_group_ig_landowners_pol_str_mult') == '0.15'
    assert amendment.children('would_sponsor')[0].one('is_interest_group_type') == 'ig_landowners'
    assert amendment.children('can_repeal')[0].children('legitimacy')[0].op == '>='
    assert amendment.children('can_repeal')[0].one('legitimacy') == 'legitimacy_to_repeal_amendment'
    assert payload[RUS] == expected_rus(before), 'Russian changes exceed the two bounded edits'
    country = next(n for n in walk(parse(text(payload[RUS]))) if n.key == 'c:RUS')
    initial = {n.value for n in country.children('activate_law')}
    assert 'law_type:law_military_bureaucrats' in initial
    assert not initial & {'law_type:law_third_section', 'law_type:law_official_nationality'}
    for lang, path in LOC.items():
        assert payload[path].startswith(b'\xef\xbb\xbf')
        raw = text(payload[path])
        assert raw.startswith('l_' + lang + ':\n')
        for key in (AID, AID + '_desc'):
            assert raw.count(' ' + key + ':0 "') == 1
    return True


def main(output=None):
    install = json.loads((EVIDENCE / 'R2/INSTALLATION.json').read_text(encoding='utf-8'))
    baseline = json.loads((EVIDENCE / 'BASELINE.json').read_text(encoding='utf-8'))
    payload = {p: (ROOT / p).read_bytes() for p in install['files']}
    before = (EVIDENCE / 'rus_before.txt').read_bytes()
    contracts(payload, before)
    assert all(hashlib.sha256(data).hexdigest() == install['files'][p]['after']
               for p, data in payload.items())
    protected_missing = [p for p in baseline['files'] if p != RUS and not (ROOT / p).exists()]
    protected_changes = [p for p, sha in baseline['files'].items() if p != RUS and
                         (not (ROOT / p).exists() or
                          hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != sha)]
    # A negative control must fail a semantic contract, not just a file hash.
    controls = [
        ('nationalism_gate_reintroduced', LAWS, b'law_official_nationality = { # For Russia',
         b'law_official_nationality = { # For Russia\n\tunlocking_technologies = { nationalism }'),
        ('disabled_policing_alias', LAWS, b'professional_civil_policing', b'law_enforcement'),
        ('wrong_country_visibility', LAWS, b'c:RUS ?= this', b'c:PLC ?= this'),
        ('changed_native_officer_bonus', LAWS, b'country_officers_pol_str_mult = 0.25', b'country_officers_pol_str_mult = 0.50'),
        ('missing_preference', IDEOLOGY, b'law_official_nationality = approve', b'law_official_nationality = neutral'),
        ('missing_noble_weight', AMEND, b'pol_str_mult = 0.15', b'pol_str_mult = 0.00'),
        ('wrong_initial_bureaucracy', RUS, b'law_type:law_military_bureaucrats', b'law_type:law_hereditary_bureaucrats'),
        ('missing_initial_amendment', RUS, AID.encode(), b'amendment_nonexistent_control'),
        ('wrong_locale', LOC['french'], b'l_french:', b'l_english:'),
    ]
    rejected = []
    for name, path, old, new in controls:
        assert old in payload[path]
        mutated = dict(payload)
        mutated[path] = payload[path].replace(old, new, 1)
        try:
            contracts(mutated, before)
        except (AssertionError, StopIteration, IndexError):
            rejected.append(name)
        else:
            raise AssertionError('Negative control escaped: ' + name)

    snapshot = collect_snapshot()
    earlier = json.loads((EVIDENCE / 'STARTING_TECH_BEFORE.json').read_text(encoding='utf-8'))
    after = [audit_country(row['TAG'], snapshot, {}) for row in earlier]
    comparisons = {}
    for old, new in zip(earlier, after):
        assert old['technologies'] == new['technologies']
        old_findings = {json.dumps(f, sort_keys=True) for f in old['findings']}
        new_findings = {json.dumps(f, sort_keys=True) for f in new['findings']}
        assert not new_findings - old_findings, (new['TAG'], new_findings - old_findings)
        comparisons[new['TAG']] = {'baseline_status': old['status'], 'after_status': new['status'],
                                    'baseline_findings': len(old_findings), 'after_findings': len(new_findings),
                                    'new_findings': 0}
    rus = next(row for row in after if row['TAG'] == 'RUS')
    assert not set(rus['technologies']) & {'nationalism', 'professional_civil_policing'}
    laws = snapshot['laws']
    assert 'law_official_nationality' in laws
    assert not values(laws['law_official_nationality'], 'unlocking_technologies')
    for law_id, tech_id in [('law_third_section', 'professional_civil_policing')]:
        assert law_id in laws
        assert snapshot['techs'][tech_id].one('can_research') != 'no'
    # Duplicate checks include native definitions after file masking, and REPLACE
    # directives for ideologies through the repository's existing object loader.
    import audit_starting_tech_1776 as core
    ideologies, _, _ = core.objects('common/ideologies')
    assert ideologies['ideology_tsarist'].children('lawgroup_citizenship')[0].one('law_official_nationality') == 'approve'
    for lang in LOC:
        for key in (AID, AID + '_desc'):
            count = sum(p.read_text(encoding='utf-8-sig').count(' ' + key + ':')
                        for p in (ROOT / 'localization' / lang).rglob('*.yml'))
            assert count == 1, (lang, key, count)
    for p in (ROOT / 'common/history/countries').glob('*.txt'):
        if p != ROOT / RUS:
            assert AID not in p.read_text(encoding='utf-8-sig')
    result = {
        'status': 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        'contracts': 'PASS_STATIC_ONLY', 'negative_controls_rejected': rejected,
        'protected_files': len(baseline['files']) - 1,
        'concurrent_changes_preserved': protected_changes,
        'concurrent_files_removed_since_R1_baseline': protected_missing,
        'starting_technology_nonregression': comparisons,
        'starting_technology_after': after,
        'runtime_tested': False, 'human_validated': False,
        'limits': 'Script definitions and static requests only; no engine law activation, '
                  'enactment odds, IG government membership or amendment rendering certified.',
    }
    if output:
        output = Path(output)
        assert not output.exists(), 'Existing evidence must not be overwritten'
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'starting_technology_after'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    main(parser.parse_args().output)
