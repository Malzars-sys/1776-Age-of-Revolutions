"""Validate the bounded EUROPE-LAWS-R1 overlay and preserved runtime inputs."""
import copy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import audit_starting_tech_1776 as core

OUT = core.ROOT/'docs/reports/politics/EUROPE_STARTING_LAWS_R1_2026_11_11'
OVERLAY = 'common/history/countries/zzzz_1776_europe_starting_laws_r1.txt'


def contract(before, after, plan):
    checks = {}
    x = {r['tag']:r for r in before['countries']}
    y = {r['tag']:r for r in after['countries']}
    expected = {(r['tag'],r['group']):r['after'] for r in plan['changes']}
    actual = {(t,g):l for t in y for g,l in y[t]['last_unconditional_request_by_group'].items()
              if l != x.get(t,{}).get('last_unconditional_request_by_group',{}).get(g)}
    checks['same_country_scope'] = x.keys() == y.keys()
    checks['only_planned_final_law_requests_changed'] = actual == expected
    checks['unique_targets'] = len(expected) == len(plan['changes']) == 70
    checks['all_law_ids_known'] = all(l in after['laws'] for l in expected.values())
    checks['correct_law_groups'] = all(after['laws'].get(l,{}).get('group')==g
                                      for (_,g),l in expected.items())
    checks['subjecthood_only_monarchies_and_theocracies'] = all(
        x[t]['last_unconditional_request_by_group'].get('lawgroup_governance_principles')
        in {'law_monarchy','law_theocracy'} for (t,g),l in expected.items() if l=='law_subjecthood')
    checks['spain_and_republics_reserved'] = all(
        x[t]['last_unconditional_request_by_group']==y[t]['last_unconditional_request_by_group']
        for t in x if t=='SPA' or (t!='SWI' and x[t]['last_unconditional_request_by_group'].get(
            'lawgroup_governance_principles') not in {'law_monarchy','law_theocracy'}))
    checks['swiss_oligarchy'] = y['SWI']['last_unconditional_request_by_group'][
        'lawgroup_distribution_of_power']=='law_oligarchy'
    checks['ottoman_censorship'] = y['TUR']['last_unconditional_request_by_group'][
        'lawgroup_free_speech']=='law_censorship'
    checks['all_starting_knowledge_preserved'] = all(x[t]['technologies']==y[t]['technologies'] for t in x)
    checks['shared_law_definitions_preserved'] = before['laws']==after['laws']
    checks['all_original_runtime_files_preserved'] = all(
        after['runtime_hashes'].get(p)==h for p,h in before['runtime_hashes'].items())
    checks['single_new_runtime_file'] = set(after['runtime_hashes'])-set(before['runtime_hashes'])=={OVERLAY}
    old = {(r['tag'],f['law'],tuple(f['missing'])) for r in before['countries'] for f in r['law_gate_findings']}
    new = {(r['tag'],f['law'],tuple(f['missing'])) for r in after['countries'] for f in r['law_gate_findings']}
    checks['no_undocumented_new_law_gate'] = new-old == {('TUR','law_censorship',('periodical_print_networks',))}
    return checks, old-new, new-old


def main():
    load = lambda n: json.loads((OUT/n).read_text(encoding='utf-8'))
    before, after, plan = load('BEFORE.json'), load('AFTER.json'), load('PLAN.json')
    checks, removed, added = contract(before,after,plan)
    checks['current_overlay_matches_installation'] = hashlib.sha256((core.ROOT/OVERLAY).read_bytes()).hexdigest()==load('INSTALLATION.json')['sha256']
    checks['snapshot_files_still_current'] = all((core.ROOT/p).is_file() and
        hashlib.sha256((core.ROOT/p).read_bytes()).hexdigest()==h for p,h in after['runtime_hashes'].items())
    roots = core.cw.parse((core.ROOT/OVERLAY).read_text(encoding='utf-8'))
    countries = roots[0].children() if len(roots)==1 and roots[0].key=='COUNTRIES' else []
    checks['overlay_only_country_law_commands'] = len(countries)==70 and all(
        n.key.startswith('c:') and len(n.children())==1 and n.children()[0].key=='activate_law'
        for n in countries)
    negatives = {}
    for name,tag,field,value in [
        ('spain_blanket_subjecthood','SPA','lawgroup_citizenship','law_subjecthood'),
        ('unknown_ottoman_law','TUR','lawgroup_free_speech','law_unknown'),
        ('removed_montenegro_fix','MON','lawgroup_citizenship','law_national_supremacy')]:
        bad = copy.deepcopy(after)
        next(r for r in bad['countries'] if r['tag']==tag)['last_unconditional_request_by_group'][field]=value
        negatives[name] = not all(contract(before,bad,plan)[0].values())
    bad = copy.deepcopy(after)
    next(r for r in bad['countries'] if r['tag']=='SPA')['technologies'].append('nationalism')
    negatives['unrequested_nationalism_grant'] = not all(contract(before,bad,plan)[0].values())
    result = dict(status='PASS_STATIC_WITH_DOCUMENTED_GATE_EXCEPTION' if all(checks.values()) and all(negatives.values()) else 'FAIL_STATIC',
                  checks=checks,negative_controls_rejected=negatives,
                  removed_law_gate_findings=sorted(removed),new_law_gate_findings=sorted(added),
                  new_gate_explanation='TUR: explicit historical censorship request; periodical_print_networks is not granted merely to satisfy a later enactment gate. Initial engine activation remains to be checked.',
                  engine_test=False,human_validation=False)
    (OUT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],checks_passed=sum(checks.values()),checks_total=len(checks),
                         negative_controls_rejected=sum(negatives.values()),law_gate_findings_removed=len(removed),
                         documented_new_gate_findings=len(added))))
    return int(result['status']=='FAIL_STATIC')


if __name__=='__main__':
    sys.exit(main())
