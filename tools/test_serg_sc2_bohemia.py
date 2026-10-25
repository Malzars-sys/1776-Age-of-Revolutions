"""Regression contracts for the population correction and bounded player handoff."""
import copy,unittest
import serg_sc2_bohemia as lot
import serg_closure_roadmap as rm

class BohemiaContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=(lot.OUT/'POPS_BEFORE.txt').read_bytes().decode('utf8')
        cls.new=(lot.OUT/'POPS_CANDIDATE.txt').read_bytes().decode('utf8')
        cls.baseline=lot.load(lot.OUT/'BASELINE.json')['roadmap']

    def test_exact_scoped_candidate(self):self.assertTrue(lot.validate_scope(self.old,self.new))
    def test_reject_another_region_change(self):
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,self.new.replace('s:STATE_MORAVIA','s:STATE_MORAVIA_TEST',1))
    def test_reject_cultural_reassignment(self):
        n=lot.pop_nodes(self.new)[0];a=self.new[:n.start];b=self.new[n.start:].replace('south_german','czech',1)
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,a+b)
    def test_reject_religion_edit(self):
        n=lot.pop_nodes(self.new)[1];a=self.new[:n.start];b=self.new[n.start:].replace('catholic','protestant',1)
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,a+b)
    def test_reject_wrong_total(self):
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,self.new.replace('903287','903288',1))
    def test_reject_profession_change(self):
        n=lot.pop_nodes(self.new)[1];a=self.new[:n.start];b=self.new[n.start:].replace('shopkeepers','aristocrats',1)
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,a+b)
    def test_reject_extra_pop(self):
        n=lot.pop_nodes(self.new)[0];bad=self.new[:n.start]+self.new[n.start:n.end]+self.new[n.start:]
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,bad)
    def test_reject_comment_or_formatting_change(self):
        n=lot.pop_nodes(self.new)[0];bad=self.new[:n.start]+'# extra\n'+self.new[n.start:]
        with self.assertRaises(AssertionError):lot.validate_scope(self.old,bad)
    def test_largest_remainder_exact_and_stable_tie(self):self.assertEqual(lot.allocate_counts([1,1,1],5),[2,2,1])
    def test_positive_values_required(self):
        for ns,total in [([0,1],10),([1],0),([],1),([-1,2],3)]:
            with self.assertRaises(AssertionError):lot.allocate_counts(ns,total)
    def test_extreme_rounding_does_not_delete_small_group(self):
        with self.assertRaises(AssertionError):lot.allocate_counts([1,10000],1)
    def test_receipt_stays_at_twelve_cells(self):
        r=lot.load(lot.prior.OUT/'RUNTIME_USER_ATTESTATION_2026_10_19.json')
        self.assertEqual(r['task_ids'],['SC1-SALZBURG'])
        self.assertEqual(r['scope']['cells'],[[x,y] for x in range(4385,4389) for y in range(924,927)])
        self.assertEqual(r['scope']['classification'],'B_POLITICAL_APPROXIMATION')
        self.assertIsNone(r['actual_test_date']);self.assertIsNone(r['language_tested'])
    def ready(self):
        state=copy.deepcopy(self.baseline);t=next(t for t in state['tasks'] if t['id']=='SC2-BOHEMIA')
        t['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        state['runtime_validation_hold']={'task_id':t['id']}
        return state,t
    def test_salzburg_credit_is_66_of_235(self):
        p=rm.progress(self.baseline);self.assertEqual((p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks']),(66,235,'28.09',20))
    def test_new_installation_has_zero_credit(self):
        state,t=self.ready();p=rm.progress(state)
        self.assertEqual(p['earned_weight'],66);self.assertFalse(rm.terminal_evidence(t,state))
    def test_player_handoff_blocks_automatic_next_start(self):
        state,t=self.ready();self.assertEqual(rm.progress(state)['next_task'],'SC2-BOHEMIA')
        self.assertEqual(next(t for t in state['tasks'] if t['id']=='SC2-MORAVIA')['status'],'NOT_STARTED')
    def test_next_eligible_candidate_is_moravia(self):
        state,t=self.ready();state.pop('runtime_validation_hold')
        self.assertEqual(rm.progress(state)['next_task'],'SC2-MORAVIA')
    def test_fake_pass_without_receipt_is_not_credited(self):
        state,t=self.ready();t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(rm.terminal_evidence(t,state));self.assertEqual(rm.progress(state)['earned_weight'],66)

if __name__=='__main__':unittest.main()
