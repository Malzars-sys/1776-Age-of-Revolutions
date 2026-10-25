"""Read-only negative checks for genuine receipts scoped to superseded deliveries."""
import copy,unittest
import serg_closure_roadmap as rm

class VersionedReceipts(unittest.TestCase):
    def setUp(self):
        self.s=rm.load_json(rm.OUT/'ROADMAP_STATE.json')
        self.t=copy.deepcopy(next(t for t in self.s['tasks'] if t['id']=='SC1-BERCHTESGADEN'))
    def test_historical_core_and_pending_revision_are_valid_structure(self):
        self.assertTrue(rm.mixed_partial_runtime_evidence(self.t))
        self.assertFalse(rm.qualifications(self.s)[self.t['id']])
    def test_missing_human_receipt_rejected(self):
        self.t['historical_runtime_validation']['attestation']=None
        self.assertFalse(rm.mixed_partial_runtime_evidence(self.t))
    def test_wrong_version_rejected(self):
        self.t['historical_validated_delivery_version']='NATIVE_MINE_NOT_TESTED'
        self.assertFalse(rm.mixed_partial_runtime_evidence(self.t))
    def test_missing_revision_exclusion_rejected(self):
        self.t['runtime_validation']['pending_revision_ids']=[]
        self.assertFalse(rm.mixed_partial_runtime_evidence(self.t))
    def test_current_mine_cannot_inherit_original_receipt(self):
        self.t['installed_sub_lots'][1]['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(rm.mixed_partial_runtime_evidence(self.t))
    def test_wrong_superseded_version_rejected(self):
        self.t['installed_sub_lots'][1]['supersedes_delivery_version']='OTHER'
        self.assertFalse(rm.mixed_partial_runtime_evidence(self.t))
    def test_receipt_does_not_close_region(self):
        self.t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(rm.terminal_evidence(self.t,self.s))

if __name__=='__main__':unittest.main()
