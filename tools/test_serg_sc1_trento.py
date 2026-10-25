"""Reject overreach in the reviewed episcopal core and receipt scope."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc1_trento as lot


class TrentoContracts(unittest.TestCase):
    def reject(self,name,mutate):
        p=lot.OUT/name;data=lot.load(p);mutate(data);reader=Path.read_text
        def read(fp,*a,**kw):return json.dumps(data) if fp==p else reader(fp,*a,**kw)
        with patch.object(Path,'read_text',autospec=True,side_effect=read):
            with self.assertRaises(AssertionError):lot.reg.approved_lot_dirs()

    def test_reject_rovereto_expansion(self):
        self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='TRT')['cells'].append([4347,981]))

    def test_reject_whole_austrian_parent_title(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']==lot.PARENT).update(beneficiary='TRT'))

    def test_reject_bolzano_or_brixen_color(self):
        self.reject('GEOMETRY.json',lambda g:g.update(parents=['xD040E0']))

    def test_reject_farm_rebinding(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'][0].update(field='farm',pixel=[4347,981]))

    def test_reject_cadastral_claim(self):
        self.reject('GEOMETRY.json',lambda g:g.update(historical_cadastral_precision=True))

    def test_reject_free_city(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m.update(free_cities=['TRT']))

    def test_reject_added_imperial_extent(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4352,973]))

    def test_current_chain_retains_both_user_validated_nuclei(self):
        self.assertEqual(lot.reg.approved_lot_dirs()[-3:],[lot.rm.OUT/'SC1-SALZBURG',lot.prior.OUT,lot.OUT])

    def test_no_human_receipt_no_credit(self):
        state=copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap'])
        t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)

    def test_massa_receipt_does_not_close_region(self):
        state=lot.load(lot.OUT/'BASELINE.json')['roadmap']
        t=next(t for t in state['tasks'] if t['id']=='SC4-MASSA-CARRARA')
        self.assertEqual(t['status'],'BLOCKED')
        self.assertTrue(lot.rm.partial_runtime_evidence(t))
        self.assertFalse(lot.rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),state))
        receipt=lot.load(lot.prior.OUT/'RUNTIME_USER_ATTESTATION_2026_10_23.json')
        self.assertEqual(receipt['sub_lot_ids'],['MC-I-CORE'])
        self.assertIsNone(receipt['actual_test_date'])
        self.assertFalse(receipt['regional_closure_approved'])

    def test_tyrol_stays_dependent_on_both_bishoprics(self):
        state=lot.load(lot.OUT/'BASELINE.json')['roadmap']
        t=next(t for t in state['tasks'] if t['id']=='SC2-TYROL')
        self.assertEqual(set(t['depends_on']),{'SC1-TRENTO','SC1-BRIXEN'})
        self.assertEqual(next(t for t in state['tasks'] if t['id']=='SC1-BRIXEN')['status'],'NOT_STARTED')


if __name__=='__main__':unittest.main()
