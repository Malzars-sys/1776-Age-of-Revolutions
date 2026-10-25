"""Negative scope checks and bounded human validation; no game execution."""
import copy
import unittest
import serg_sc4_savoy_nice as lot


class SavoyNiceContracts(unittest.TestCase):
    def baseline(self):return copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap'])

    def test_priority_after_three_explicit_italian_receipts(self):
        state=self.baseline();p=lot.rm.progress(state)
        self.assertEqual((p['earned_weight'],p['total_weight'],p['percent'],p['next_task']),(82,235,'34.89',lot.TASK))
        t=next(t for t in state['tasks'] if t['id']==lot.prior.TASK)
        self.assertTrue(lot.rm.partial_runtime_evidence(t))
        self.assertEqual({s['id'] for s in t['installed_sub_lots']},{'IT-I-MOD','IT-I-PAR','IT-I-LUC'})

    def test_italian_receipt_cannot_credit_or_close_region(self):
        state=self.baseline();t=next(t for t in state['tasks'] if t['id']==lot.prior.TASK)
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)

    def test_nice_rejects_french_or_whole_state_selector(self):
        raw=lot.expected_admin('STATE_PROVENCE')
        for old,new in [('region_state:SAR','region_state:FRA'),('region_state:SAR','region_state:ALL')]:
            with self.assertRaises(AssertionError):lot.admin_contract(raw.replace(old,new),'STATE_PROVENCE')

    def test_rejects_foreign_public_ownership(self):
        for sid in lot.ADMIN_FILES:
            with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin(sid).replace('"c:SAR"','"c:FRA"'),sid)

    def test_rejects_invented_extra_capacity(self):
        for sid in lot.ADMIN_FILES:
            with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin(sid).replace('levels = 1','levels = 2'),sid)

    def test_rejects_island_or_piedmont_addition(self):
        for sid in ['STATE_SARDINIA','STATE_PIEDMONT']:
            with self.assertRaises(AssertionError):lot.expected_admin(sid)

    def test_rejects_embedded_border_population_and_subject_changes(self):
        raw=lot.expected_admin('STATE_SAVOY')
        for extra in ['set_owner_of_provinces = { country = c:SAR provinces = { x5080E0 } }','create_pop = { size = 1000 culture = french }','create_diplomatic_pact = { country = c:AUS type = puppet }','set_variable = aor1776_hre_electoral_privilege_granted']:
            with self.assertRaises(AssertionError):lot.admin_contract(raw.replace('reserves = 1','reserves = 1\n'+extra),'STATE_SAVOY')

    def test_rejects_added_port_or_later_reporting(self):
        raw=lot.expected_admin('STATE_SAVOY')
        for old,new in [('building_government_administration','building_port'),('pm_1776_no_organized_data_reporting','pm_1776_administrative_data_reporting')]:
            with self.assertRaises(AssertionError):lot.admin_contract(raw.replace(old,new),'STATE_SAVOY')

    def test_two_pending_sub_lots_do_not_credit_blocked_region(self):
        state=self.baseline();t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=[dict(id=k,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION') for k in lot.SUB_IDS.values()])
        self.assertFalse(lot.rm.partial_runtime_evidence(t))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
        self.assertEqual(lot.rm.progress(state)['next_task'],'SC4-LIGURIAN-FIEFS')
        self.assertIsNone(t['runtime_validation']['attestation'])


if __name__=='__main__':unittest.main()
