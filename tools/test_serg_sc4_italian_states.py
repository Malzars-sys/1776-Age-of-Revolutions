"""Institutional scope and partial-receipt safeguards; never engine or Git writes."""
import copy
import unittest
import serg_sc4_italian_states as lot


class ItalianStatesContracts(unittest.TestCase):
    def baseline(self):return copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap'])

    def test_priority_after_bounded_anterior_acceptance(self):
        state=self.baseline();p=lot.rm.progress(state)
        self.assertEqual((p['earned_weight'],p['percent'],p['next_task']),(82,'34.89',lot.TASK))
        self.assertEqual(sum(lot.rm.qualifications(state).values()),24)

    def anterior(self):return next(t for t in self.baseline()['tasks'] if t['id']==lot.prior.TASK)

    def test_explicit_partial_receipt_qualified(self):
        self.assertTrue(lot.rm.partial_runtime_evidence(self.anterior()))

    def test_partial_receipt_cannot_close_region(self):
        state=self.baseline();t=self.anterior();t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        state['tasks']=[t if x['id']==t['id'] else x for x in state['tasks']]
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)

    def test_partial_receipt_requires_each_installation_accepted(self):
        t=self.anterior();t['installed_sub_lots'][0]['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        self.assertFalse(lot.rm.partial_runtime_evidence(t))

    def test_partial_receipt_rejects_extra_scope(self):
        t=self.anterior();t['installed_sub_lots'].append(dict(id='FRICKTAL',status='PASS_RUNTIME_USER_VALIDATED'))
        self.assertFalse(lot.rm.partial_runtime_evidence(t))

    def test_partial_receipt_requires_actual_attestation(self):
        t=self.anterior();t['runtime_validation']['attestation']=None
        self.assertFalse(lot.rm.partial_runtime_evidence(t))

    def test_partial_validation_does_not_remove_block(self):
        t=self.anterior();t['blocking_reason']=''
        self.assertFalse(lot.rm.partial_runtime_evidence(t))

    def test_three_independent_administration_contracts(self):
        for tag in lot.ADMIN_TAGS:self.assertTrue(lot.admin_contract(lot.expected_admin(tag),tag))

    def test_no_artificial_fourth_tuscan_administration(self):
        with self.assertRaises(AssertionError):lot.expected_admin('TUS')

    def test_reject_swapped_owner_or_subdivision(self):
        for tag in lot.ADMIN_TAGS:
            for old,new in [('"c:'+tag+'"','"c:AUS"'),('region_state:'+tag,'region_state:AUS')]:
                with self.subTest(tag=tag,change=old),self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin(tag).replace(old,new),tag)

    def test_reject_extra_capacity_and_other_regions(self):
        for tag in lot.ADMIN_TAGS:
            for old,new in [('levels = 1','levels = 2'),('s:STATE_EMILIA','s:STATE_ROMAGNA')]:
                with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin(tag).replace(old,new),tag)

    def test_reject_future_or_incompatible_methods(self):
        for tag in lot.ADMIN_TAGS:
            for old,new in [('pm_hereditary_bureaucrats','pm_professional_bureaucrats'),('pm_1776_no_organized_data_reporting','pm_1776_administrative_data_reporting')]:
                with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin(tag).replace(old,new),tag)

    def test_reject_population_and_diplomatic_effects(self):
        for tag in lot.ADMIN_TAGS:
            for extra in ['create_pop = { size = 1000 }','create_diplomatic_pact = { country = c:AUS type = puppet }','activate_law = law_type:law_monarchy']:
                with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin(tag).replace('reserves = 1','reserves = 1\n'+extra),tag)

    def test_new_partial_installations_no_credit(self):
        state=self.baseline();t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
        self.assertEqual(lot.rm.progress(state)['next_task'],'SC4-SAVOY-NICE')
        self.assertIsNone(t['runtime_validation']['attestation'])

    def test_no_fake_global_runtime_pass(self):
        state=self.baseline();t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)


if __name__=='__main__':unittest.main()
