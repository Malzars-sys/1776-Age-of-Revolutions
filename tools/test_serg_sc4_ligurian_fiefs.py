"""Scope, shared-file preservation and human-receipt guards; no engine execution."""
import copy
import unittest
import serg_sc4_ligurian_fiefs as lot


class LigurianContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=(lot.OUT/'BUILDINGS_BEFORE.txt').read_bytes().decode('utf8')
        cls.state=lot.load(lot.OUT/'BASELINE.json')['roadmap']

    def changed_admin(self,old,new):
        n=lot.gen_admin(self.before)
        return self.before[:n.start]+self.before[n.start:n.end].replace(old,new)+self.before[n.end:]

    def test_priority_after_two_bounded_savoy_nice_receipts(self):
        p=lot.rm.progress(self.state)
        self.assertEqual((p['earned_weight'],p['total_weight'],p['percent'],p['next_task']),(82,235,'34.89',lot.TASK))
        t=next(t for t in self.state['tasks'] if t['id']=='SC4-SAVOY-NICE')
        self.assertTrue(lot.rm.partial_runtime_evidence(t))
        self.assertEqual({s['id'] for s in t['installed_sub_lots']},{'SN-I-SAV','SN-I-NIC'})
        self.assertEqual(t['status'],'BLOCKED')

    def test_two_savoy_nice_receipts_never_close_region(self):
        state=copy.deepcopy(self.state);t=next(t for t in state['tasks'] if t['id']=='SC4-SAVOY-NICE')
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)

    def test_rejects_foreign_or_private_ownership(self):
        for old,new in [('country="c:GEN"','country="c:SAR"'),('country={','building={')]:
            with self.assertRaises(AssertionError):lot.candidate(self.changed_admin(old,new))

    def test_rejects_invented_capacity(self):
        with self.assertRaises(AssertionError):lot.candidate(self.changed_admin('levels=1','levels=2'))

    def test_rejects_replay_and_unrelated_method_replacement(self):
        with self.assertRaises(AssertionError):lot.candidate(lot.candidate(self.before))
        with self.assertRaises(AssertionError):lot.candidate(self.changed_admin('pm_hereditary_bureaucrats','pm_elected_bureaucrats'))

    def test_rejects_embedded_territorial_population_or_diplomatic_edit(self):
        for extra in ['create_pop={ size=1000 culture=north_italian }','set_owner_of_provinces={ country=c:GEN provinces={ xACB500 } }','create_diplomatic_pact={ country=c:AUS type=puppet }']:
            with self.assertRaises(AssertionError):lot.candidate(self.changed_admin('reserves=1','reserves=1\n'+extra))

    def test_shared_file_neighbors_survive_without_restoration(self):
        marker='\n# Concurrent unrelated text: retain it verbatim\n'
        raw=self.before+marker;after=lot.candidate(raw)
        self.assertTrue(after.endswith(marker))
        old=lot.gen_admin(raw);new=lot.gen_admin(after)
        self.assertEqual(raw[:old.start],after[:new.start])
        self.assertEqual(raw[old.end:],after[new.end:])
        # The installer separately refuses changes since the session snapshot.
        self.assertNotEqual(raw.encode('utf8'),self.before.encode('utf8'))

    def test_pending_ligurian_correction_does_not_award_points(self):
        state=copy.deepcopy(self.state);t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=[dict(id=lot.SUB,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')])
        self.assertFalse(lot.rm.partial_runtime_evidence(t))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
        self.assertEqual(lot.rm.progress(state)['next_task'],'SC4-PIOMBINO')
        self.assertIsNone(t['runtime_validation']['attestation'])

    def test_savoy_receipt_cannot_be_reused_for_ligurian_region(self):
        state=copy.deepcopy(self.state);t=next(t for t in state['tasks'] if t['id']==lot.TASK)
        sn=next(t for t in state['tasks'] if t['id']=='SC4-SAVOY-NICE')
        t.update(status='BLOCKED',blocking_reason='Unresolved Ligurian territorial rights',installed_delivery_status='PASS_RUNTIME_USER_VALIDATED',installed_sub_lots=[dict(id=lot.SUB,status='PASS_RUNTIME_USER_VALIDATED')],runtime_validation=copy.deepcopy(sn['runtime_validation']))
        self.assertFalse(lot.rm.partial_runtime_evidence(t))


if __name__=='__main__':unittest.main()
