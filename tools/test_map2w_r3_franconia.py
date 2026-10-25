"""Final R3 protection checks after withdrawing unaccepted geometry."""
import json,unittest
import map2w_r3_franconia as w
class WithdrawnR3Tests(unittest.TestCase):
    def test_final_blocked_status(self):self.assertEqual(w.load('VALIDATION.json')['status'],'MAP2W_R3_BLOCKED')
    def test_all_protection_checks(self):
        v=w.load('VALIDATION.json');self.assertEqual(v['passed'],v['total'])
    def test_no_country_or_colour_installed(self):
        v=w.load('VALIDATION.json');self.assertFalse(v['new_countries_installed']);self.assertFalse(v['new_RGBs_installed']);self.assertEqual(v['territorial_transfers_applied'],0)
    def test_no_active_migration(self):self.assertFalse((w.OUT/'REGISTRY_MIGRATION.json').exists())
    def test_proposed_migration_is_not_approved(self):
        import map2l_registry as r
        self.assertNotIn(w.OUT,r.approved_lot_dirs())
    def test_population_conserved(self):self.assertEqual(w.load('VALIDATION.json')['world_after'],835801255)
    def test_no_r3_runtime_claim(self):self.assertFalse(w.load('VALIDATION.json')['manual_R3_validation'])
    def test_r2b_attestation_preserved(self):
        r=json.loads((w.OUT.parent/'R2B/RUNTIME_USER_ATTESTATION.json').read_text());self.assertEqual(r['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertFalse(r['R3_changes_covered'])
    def test_no_install_without_new_evidence(self):
        with self.assertRaises(RuntimeError):w.install()
    def test_no_prepare_without_new_evidence(self):
        with self.assertRaises(RuntimeError):w.prepare()
    def test_contradiction_not_certified_city_error(self):self.assertEqual(w.load('NATIVE_REFERENCE_CONTRADICTION.json')['status'],'UNRESOLVED_REFERENCE_DISAGREEMENT_NOT_CERTIFIED_CITY_ERROR')
    def test_candidate_archived_not_accepted(self):self.assertEqual(w.load('CANDIDATE_STATIC_VALIDATION.json')['geographic_acceptance'],'WITHDRAWN_LOCAL_REFERENCE_CONTRADICTION')
if __name__=='__main__':unittest.main()
