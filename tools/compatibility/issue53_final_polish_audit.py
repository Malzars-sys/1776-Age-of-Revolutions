"""Read-only supply tutorial and bilingual tooltip checks for issue 53.

Candidate overlays remain in memory. Writes only a new evidence result.
Threshold fixtures describe the native predicate; they do not execute the engine.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, walk
from issue44_event_targets_audit import payload, localization_catalogue

EVIDENCE = ROOT/'docs/reports/compatibility/V1_15_ISSUE53_FINAL_POLISH_2026_11_10'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(blobs, contract, catalogs, subgoal):
    checks = []
    def check(name, result):
        checks.append({'name': name, 'passed': bool(result)})
    rel = contract['journal_path']
    data = blobs[rel]
    original = (EVIDENCE/'before'/rel).read_bytes()
    before = original.decode('utf-8-sig')
    raw = data.decode('utf-8-sig')
    expected = before[:contract['old_start']] + contract['replacement'] + before[contract['old_end']:]
    check('exact_bounded_patch_and_preserved_other_bytes',
          data == (b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'') + expected.encode())
    check('tutorial_BOM_preserved', data.startswith(b'\xef\xbb\xbf') == original.startswith(b'\xef\xbb\xbf'))
    nodes = parse(raw)
    selected = [n for n in nodes if n.key == contract['journal_id']]
    native = parse((EVIDENCE/'native'/rel).read_text(encoding='utf-8-sig'))
    entry = selected[0]
    check('unique_selected_journal', len(selected) == 1)
    check('matches_current_native_entry', payload(selected) == payload([n for n in native if n.key == contract['journal_id']]))
    check('other_journal_payloads_unchanged',
          payload([n for n in nodes if n.key != contract['journal_id']]) ==
          payload([n for n in parse(before) if n.key != contract['journal_id']]))
    check('obsolete_convoy_value_removed', all(n.key not in ('current_value', 'goal_add_value') and n.value != 'num_convoys_available' for n in walk(entry.children())))
    trigger = entry.children('outcome')[0].children('trigger')[0]
    check('state_goods_target_exists_guard', trigger.one('exists') == 'scope:target')
    target = trigger.children('scope:target')
    check('native_price_boundary', len(target) == 1 and payload(target[0].children()) == [('state_goods_pricier', '<', '0.1')])
    sg = parse(subgoal)[0]
    check('native_subgoal_wiring_preserved', payload([sg]) == payload(parse(contract['subgoal_excerpt'])))
    calls = [n for n in walk(sg.children()) if n.key == 'add_journal_entry']
    check('caller_passes_state_goods_target', len(calls)==1 and calls[0].one('target')=='scope:tut_supply_network' and calls[0].one('type')==contract['journal_id'])
    check('caller_saves_merchant_marine_state_goods', any(n.key=='sg:merchant_marine' and n.one('save_scope_as')=='tut_supply_network' for n in walk(sg.children())))
    for lang, values in contract['localizations'].items():
        rel = 'localization/'+lang+'/1776_v115_final_tooltips_l_'+lang+'.yml'
        content = blobs[rel]
        check(lang+'.UTF8_BOM', content.startswith(b'\xef\xbb\xbf'))
        lines = content.decode('utf-8-sig').splitlines()
        check(lang+'.header', lines[0] == 'l_'+lang+':')
        matches = [re.fullmatch(r' ([\w.]+):0 "([^"\r\n]*)"', line) for line in lines[1:]]
        actual = {m[1]: m[2] for m in matches if m}
        check(lang+'.eight_valid_unique_lines', len(matches)==8 and all(matches) and len(actual)==8)
        check(lang+'.exact_predicate_texts', actual==values)
        for key, value in values.items():
            providers = catalogs[lang].get(key, [])
            check(lang+'.'+key+'.unique_effective_provider', len(providers)==1 and providers[0]['value']==value)
        for key in ('je_tutorial_improve_supply_network', 'je_tutorial_improve_supply_network_reason',
                    'je_tutorial_improve_supply_network_activation_tt', 'je_tutorial_improve_supply_network_activation_2_tt'):
            check(lang+'.'+key+'.inherited_text', len(catalogs[lang].get(key, [])) == 1)
    return checks


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--candidate', action='store_true')
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():
        ap.error('Use a new output under issue53 evidence.')
    contract = json.loads((EVIDENCE/'CONTRACT.json').read_text(encoding='utf-8'))
    source = EVIDENCE/'candidate' if args.candidate else ROOT
    blobs = {f['path']: (source/f['path']).read_bytes() for f in contract['files']}
    catalogs = {lang: localization_catalogue(lang) for lang in contract['localizations']}
    if args.candidate:
        for lang, values in contract['localizations'].items():
            # Only append absent candidate keys; a competing provider must fail uniqueness.
            for key, value in values.items():
                catalogs[lang].setdefault(key, []).append({'value': value, 'source': 'issue53 candidate'})
    audit = Audit(ROOT, GAME)
    pool = audit.load('subgoals', 'common/objective_subgoals')
    providers = pool.get('sg_improve_supply_network', [])
    sg, provider, source_raw = providers[0]
    subgoal = source_raw[sg.start:sg.end]
    checks = verify(blobs, contract, catalogs, subgoal)
    checks += [
        {'name': 'unique_native_caller', 'passed': len(providers)==1 and provider==contract['subgoal_provider']},
        {'name': 'native_tutorial_source_unchanged', 'passed': sha((GAME/contract['journal_path']).read_bytes())==contract['native_tutorial_sha256']},
        {'name': 'native_caller_source_unchanged', 'passed': sha((GAME/provider.removeprefix('native/')).read_bytes())==contract['subgoal_source_sha256']},
        {'name': 'unique_merchant_marine_good', 'passed': len(audit.load('goods', 'common/goods').get('merchant_marine', []))==1},
    ]
    baseline = json.loads((EVIDENCE/'SOURCE_BASELINE.json').read_text(encoding='utf-8'))
    protected = ['common/journal_entries/00_meiji_restoration.txt', 'common/journal_entries/00_player_objectives_great_game.txt',
                 'common/journal_entries/03_russia.txt', 'common/scripted_triggers/00_victoria_scripted_triggers.txt']
    checks.append({'name': 'tooltip_consumers_and_meiji_helper_unchanged',
                   'passed': all(sha((ROOT/p).read_bytes())==baseline[p] for p in protected)})
    # Deliberately small model of only the target-presence and strict-price predicate.
    cases = [{'exists': exists, 'premium': price, 'expected': expected,
              'passed': (exists and price < .1)==expected}
             for exists, price, expected in [(False,0,False),(True,.3,False),(True,.1,False),(True,.099,True)]]
    controls = []
    if args.controls:
        rel = contract['journal_path']
        variants = [
            ('old_convoys', rel, blobs[rel].replace(b'weight = 1018', b'current_value = { value = num_convoys_available }\nweight = 1018'), 'obsolete_convoy_value_removed'),
            ('missing_guard', rel, blobs[rel].replace(b'exists = scope:target', b'exists = root'), 'state_goods_target_exists_guard'),
            ('wrong_boundary', rel, blobs[rel].replace(b'state_goods_pricier < 0.1', b'state_goods_pricier < 0.2'), 'native_price_boundary'),
            ('other_journal_edit', rel, blobs[rel].replace(b'weight = 1001', b'weight = 9999', 1), 'exact_bounded_patch_and_preserved_other_bytes'),
        ]
        for lang in contract['localizations']:
            path = 'localization/'+lang+'/1776_v115_final_tooltips_l_'+lang+'.yml'
            variants += [(lang+'_no_BOM', path, blobs[path][3:], lang+'.UTF8_BOM'),
                         (lang+'_missing_key', path, b'\n'.join(blobs[path].split(b'\n')[:-2])+b'\n', lang+'.eight_valid_unique_lines')]
        for name, rel, altered, target in variants:
            changed = dict(blobs)
            changed[rel] = altered
            tests = verify(changed, contract, catalogs, subgoal)
            controls.append({'name': name, 'passed': any(t['name']==target and not t['passed'] for t in tests)})
        wrong = subgoal.replace('target = scope:tut_supply_network', 'target = root')
        controls.append({'name': 'wrong_caller_target', 'passed': any(t['name']=='caller_passes_state_goods_target' and not t['passed'] for t in verify(blobs,contract,catalogs,wrong))})
    result = {'mode': 'candidate' if args.candidate else 'live', 'checks': checks, 'cases': cases,
              'negative_controls': controls, 'files': {p:sha(b) for p,b in blobs.items()},
              'runtime_tested': False, 'limits': 'Static/native parity and explicit predicate fixtures only; no engine or human acceptance.'}
    result['passed'] = all(row['passed'] for row in checks+cases+controls)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'checks': len(checks), 'cases': len(cases), 'controls': len(controls),
                      'failures': [r for r in checks+cases+controls if not r['passed']]}))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
