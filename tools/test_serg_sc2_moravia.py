"""Negative scope/PM/ownership guards and genuine receipt boundaries."""
import copy,unittest
import serg_sc2_moravia as lot
import serg_closure_roadmap as rm

class MoraviaContracts(unittest.TestCase):
    def reject(self,old,new):
        with self.assertRaises(AssertionError):lot.admin_contract(lot.expected_admin().replace(old,new,1))
    def test_expected_scope(self):self.assertTrue(lot.admin_contract(lot.expected_admin()))
    def test_reject_second_level(self):self.reject('levels = 1','levels = 2')
    def test_reject_wrong_region(self):self.reject('s:STATE_MORAVIA','s:STATE_BOHEMIA')
    def test_reject_wrong_country_selector(self):self.reject('region_state:AUS','region_state:PRU')
    def test_reject_wrong_public_owner(self):self.reject('country = "c:AUS"','country = "c:PRU"')
    def test_reject_incompatible_professional_pm(self):self.reject('pm_hereditary_bureaucrats','pm_professional_bureaucrats')
    def test_reject_research_data_creation(self):self.reject('pm_1776_no_organized_data_reporting','pm_1776_administrative_data_reporting')
    def test_reject_added_effect(self):self.reject('reserves = 1','reserves = 1\n create_pop = { culture = czech size = 1000 }')
    def test_reject_another_building(self):self.reject('building_government_administration','building_barracks')
    def test_reject_no_ownership(self):self.reject('add_ownership','unused_ownership')
    def baseline(self):return copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap'])
    def test_bohemia_credit_72_of_235(self):
        p=rm.progress(self.baseline());self.assertEqual((p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks']),(72,235,'30.64',21))
    def test_new_ready_installation_has_zero_credit(self):
        s=self.baseline();t=next(t for t in s['tasks'] if t['id']=='SC2-MORAVIA');t['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        s['runtime_validation_hold']={'task_id':t['id']};p=rm.progress(s)
        self.assertEqual((p['earned_weight'],p['next_task']),(72,'SC2-MORAVIA'));self.assertIsNone(t['runtime_validation']['attestation'])
    def test_next_candidate_silesia_not_started(self):
        s=self.baseline();next(t for t in s['tasks'] if t['id']=='SC2-MORAVIA')['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        self.assertEqual(rm.progress(s)['next_task'],'SC2-AUSTRIAN-SILESIA')
        self.assertEqual(next(t for t in s['tasks'] if t['id']=='SC2-AUSTRIAN-SILESIA')['status'],'NOT_STARTED')
    def test_confirmation_does_not_spread_to_map2a(self):
        s=self.baseline();done=rm.qualifications(s)
        self.assertTrue(done['SC2-BOHEMIA']);self.assertTrue(done['SC1-SALZBURG']);self.assertFalse(done['SC2-MAP2A-VALIDATION'])
        r=lot.load(lot.prior.OUT/'RUNTIME_USER_ATTESTATION_2026_10_19.json')
        self.assertEqual(r['task_ids'],['SC2-BOHEMIA']);self.assertEqual(r['simulation_months'],1)
        self.assertTrue(r['save_and_reload']);self.assertIsNone(r['actual_test_date']);self.assertIsNone(r['language_tested'])
    def test_preserved_map2a_ids(self):
        b=lot.load(lot.OUT/'BOUNDARY_AUDIT.json');p=[r for r in b['provinces'] if r['protected_map2a']]
        self.assertEqual({r['rgb'] for r in p},{'x71E080','xF0E080'});self.assertEqual(sum(r['cells_before'] for r in p),311)
        self.assertTrue(all(r['owner_before']==r['owner_after']=='AUS' and r['cells_before']==r['cells_after'] for r in p))

if __name__=='__main__':unittest.main()
