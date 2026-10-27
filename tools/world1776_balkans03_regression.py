"""Read-only replay of B02 tests, plus current B01/B03 cross-checks.

Writes only B03 evidence. Historical B01/B02 receipts are never rewritten.
The raw B02 result retains its two obsolete-baseline failures; adjudication
requires exact B03 receipts for MON scopes and unchanged current Git identity.
"""
import contextlib
import io
import json
import re
import sys
from collections import Counter

import world1776_balkans02 as old
import world1776_balkans03 as b
import localization_duplicate_audit as loc


def main():
    checks=[]
    def check(k,v,detail=None):checks.append({'check':k,'passed':bool(v),'detail':detail})
    base=json.loads((b.LOT/'BASELINE.json').read_text('utf8'))
    replay=b.LOT/'prior_lot_replay';replay.mkdir(exist_ok=True)
    original_dump=old.dump
    old.dump=lambda n,v:(replay/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    try:
        with contextlib.redirect_stdout(io.StringIO()) as log:raw=old.validate()
        (replay/'B02_RAW_OUTPUT.txt').write_text(log.getvalue(),encoding='utf8')
    finally:old.dump=original_dump
    failures=[c for c in raw['checks'] if not c['passed']]
    expected_failures={'git_unchanged','protected_differences_have_independent_peer_receipts','SERG_receipts_unchanged'}
    territorial=b.LOT/'EXTERNAL_ORTENBURG_UPDATE.json'
    peer=json.loads(territorial.read_text('utf8')) if territorial.exists() else {}
    if peer:
        expected_failures.update({'exact_scoped_text.common/history/states/00_states.txt','bitmap_only_authorized_pixels','only_three_new_ownership_keys','exact_scoped_text.map_data/province_terrains.txt'})
    check('B02_raw_replay_has_only_dated_baseline_and_external_SERG_drift',
          {c['check'] for c in failures}==expected_failures,
          [{'check':c['check'],'passed':False} for c in failures])
    check('current_git_identity_matches_B03_entry',b.a.git_state()==base['before']['git'])
    b03=json.loads((b.LOT/'VALIDATION.json').read_text('utf8'))
    check('B03_all_scoped_and_protection_checks_pass',b03['status']=='PASS')
    oldexternal=json.loads((b.OUT/'BALKANS-02/CONCURRENT_CHANGES.json').read_text('utf8'))['external_gameplay']
    nowexternal=json.loads((replay/'CONCURRENT_CHANGES.json').read_text('utf8'))['external_gameplay']
    observed_file=b.LOT/'EXTERNAL_GAMEPLAY_OBSERVATIONS.json'
    observed=json.loads(observed_file.read_text('utf8')).get('files',{}) if observed_file.exists() else {}
    expected_extra=set(b.OWN)| (set(observed) & set(json.loads((old.LOT/'BASELINE.json').read_text('utf8'))['protected']))
    check('only_MON_and_recorded_external_additional_B02_protected_differences',set(nowexternal)-set(oldexternal)==expected_extra,sorted(set(nowexternal)-set(oldexternal)))
    check('preexisting_external_changes_preserved_since_B03_entry',all(nowexternal[r]['observed_now']==base['protected'][r] for r in oldexternal))
    for r in b.OWN:
        check('MON_preimage_matches_old_protection.'+r,b.a.sha(b.LOT/'patch_inputs'/r)==nowexternal[r]['before'])
    inv=b.inventory()
    for c in ['x6090A0','x6960A0']:
        check('B01_Cyclades_owner.'+c,inv['owners'].get(c)==[['STATE_WEST_AEGEAN_ISLANDS','TUR']])
    for tag in ['mol - moldavia','wal - wallachia']:
        text=b.a.raw(b.ROOT/f'common/history/countries/{tag}.txt')
        check('B01_Danubian_laws.'+tag,not re.search(r'activate_law\s*=\s*law_type:(law_organic_regulation|law_elected_bureaucrats)\b',text))
    chars=[]
    for p in b.tech.effective('common/history/characters'):
        for n in b.walk(b.parse(b.a.raw(p))):
            if n.key=='c:MON':chars.extend(n.children('create_character'))
    check('one_initial_MON_ruler',sum(n.one('ruler')=='yes' for n in chars)==1)
    check('one_initial_MON_heir',sum(n.one('heir')=='yes' for n in chars)==1)
    for language in ['french','english']:
        entries=loc.entries(language)
        own=b.ROOT/f'localization/{language}/replace/{b.PREFIX}_l_{language}.yml'
        keys=set(re.findall(r'^\s+(\w+):\d',b.a.raw(own),re.M))
        for key in sorted(keys):
            check('unique_mod_localization.'+language+'.'+key,len(entries[key])==1,
                  [str(e[0].relative_to(b.ROOT)) for e in entries[key]])
    laws=b.a.catalog('common/laws')
    check('theocracy_does_not_disallow_oligarchy',
          'law_oligarchy' not in b.a.ids(laws['law_theocracy'][0],'disallowing_laws'))
    result={'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL',
            'passed':sum(x['passed'] for x in checks),'total':len(checks),
            'B02_raw':{k:raw[k] for k in ['status','passed','total','runtime']},
            'B02_raw_interpretation':str(raw['passed'])+' checks pass; dated baseline and concurrent Ortenburg differences retained as raw failures and separately reconciled. No historical proof was rewritten.',
            'runtime':'NOT_RUN','checks':checks}
    b.dump('REGRESSION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
    print([x for x in checks if not x['passed']])
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
