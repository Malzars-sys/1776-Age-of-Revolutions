"""Scope and evidence safeguards for a partial installation under a regional P0 block."""
import copy
import unittest
import serg_sc2_anterior_austria as lot


class AnteriorAustriaContracts(unittest.TestCase):
    def baseline(self):return copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap'])

    def test_priority_after_explicit_inner_receipt(self):
        state=self.baseline();p=lot.rm.progress(state)
        self.assertEqual((p['earned_weight'],p['percent'],p['next_task']),(82,'34.89',lot.TASK))
        self.assertTrue(lot.rm.qualifications(state)[lot.prior.TASK])

    def test_blocked_region_with_partial_installations_has_no_credit(self):
        state=self.baseline();t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
        self.assertEqual(lot.rm.progress(state)['next_task'],'SC4-EXISTING-ITALIAN-STATES')
        self.assertIsNone(t['runtime_validation']['attestation'])

    def test_no_fictitious_terminal_receipt(self):
        state=self.baseline();t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)

    def test_regional_admin_contracts(self):
        for sid in lot.ADMIN_FILES:self.assertTrue(lot.admin_contract(lot.expected_admin(sid),sid))

    def test_reject_administration_scope_leaks(self):
        for sid in lot.ADMIN_FILES:
            for old,new in [('levels = 1','levels = 2'),('country = "c:AUS"','country = "c:VEN"'),
                    ('region_state:AUS','region_state:VEN'),('pm_hereditary_bureaucrats','pm_professional_bureaucrats'),
                    ('reserves = 1','reserves = 1\n create_pop = { size = 500 }')]:
                with self.subTest(state=sid,change=new), self.assertRaises(AssertionError):
                    lot.admin_contract(lot.expected_admin(sid).replace(old,new,1),sid)

    def test_reject_swapped_administrations(self):
        with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin('STATE_BADEN'),'STATE_ISTRIA')

    def before(self):return (lot.OUT/'PUBLIC_PORT_BEFORE.txt').read_bytes().decode('utf8')

    def test_exact_public_port_change_keeps_all_other_bytes(self):
        before=self.before();after,node=lot.port_candidate(before)
        self.assertTrue(lot.port_contract(before,after))
        self.assertEqual(len(before),len(after))
        self.assertEqual(before.count('c:VEN')-after.count('c:VEN'),1)
        self.assertIn('building_port',lot.core.qa.signature(node))

    def test_reject_public_shipyard_nationalization(self):
        before=self.before();after,_=lot.port_candidate(before)
        region=lot.core.region(after,'STATE_ISTRIA','AUS')
        node=next(n for n in region.children('create_building') if lot.core.cw.scalar(n.one('building'))=='building_shipyard')
        changed=after[:node.start]+after[node.start:node.end].replace('c:VEN','c:AUS')+after[node.end:]
        with self.assertRaises(AssertionError):lot.port_contract(before,changed)

    def test_reject_private_property_expropriation(self):
        before=self.before();after,_=lot.port_candidate(before)
        region=lot.core.region(after,'STATE_ISTRIA','AUS')
        node=next(n for n in region.children('create_building') if lot.core.cw.scalar(n.one('building'))=='building_fishing_wharf')
        changed=after[:node.start]+after[node.start:node.end].replace('c:VEN','c:AUS')+after[node.end:]
        with self.assertRaises(AssertionError):lot.port_contract(before,changed)

    def test_reject_other_region_edit(self):
        before=self.before();after,_=lot.port_candidate(before)
        with self.assertRaises(AssertionError):lot.port_contract(before,after.replace('s:STATE_DALMATIA','s:STATE_DALMATIA_CHANGED',1))

    def test_reject_port_capacity_or_pm_change(self):
        before=self.before();after,_=lot.port_candidate(before)
        region=lot.core.region(after,'STATE_ISTRIA','AUS')
        node=next(n for n in region.children('create_building') if lot.core.cw.scalar(n.one('building'))=='building_port')
        for old,new in [('levels = 2','levels = 3'),('pm_basic_port','pm_cargo_port')]:
            changed=after[:node.start]+after[node.start:node.end].replace(old,new,1)+after[node.end:]
            with self.assertRaises(AssertionError):lot.port_contract(before,changed)

    def test_reject_concurrent_preimage_change(self):
        before=self.before();_,node=lot.port_candidate(before)
        changed=before[:node.start]+before[node.start:node.end].replace('levels = 2','levels = 3')+before[node.end:]
        with self.assertRaises(AssertionError):lot.port_candidate(changed)

    def test_reject_replay(self):
        after,_=lot.port_candidate(self.before())
        with self.assertRaises(AssertionError):lot.port_candidate(after)


if __name__=='__main__':unittest.main()
