"""Conservation and honest unresolved-state guards for MAP-2S."""
import unittest,json
import map2s_jever as s

class JeverGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=s.load('BASELINE.json');cls.d=s.load('DECISIONS.json');cls.data=s.load('CSV_TABLES.json')
    def test_no_fabricated_geometry(self):
        self.assertIsNone(self.d['native_town_pixel']);self.assertFalse(self.d['changed_cells']);self.assertFalse(self.d['new_RGBs'])
    def test_sovreignty_does_not_authorize_entire_carrier(self):
        self.assertEqual(self.d['historical_sovereignty'],'AZR');self.assertEqual(self.d['classification'],'C_GEOMETRY_A_SOVEREIGNTY')
        self.assertTrue(all(r['Owner_before']==r['Owner_after']=='OLD' for r in self.data['JEVER_TERRITORIAL_AUDIT.csv']['rows']))
    def test_empty_installed_territorial_delta(self):self.assertEqual(self.data['TERRITORIAL_CHANGES.csv']['rows'],[])
    def test_population_no_compensation_or_estimate(self):
        self.assertTrue(all(p['Before']==p['After'] and p['Delta']==0 and not p['Historical_estimate'] for p in self.data['POPULATION_BEFORE_AFTER.csv']['rows']))
    def test_player_receipt_not_engine(self):
        v=s.load('MAP2R_RUNTIME_USER_VALIDATION.json');self.assertEqual(v['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertFalse(v['automated_engine_test']);self.assertIsNone(v['simulation_duration']);self.assertFalse(v['historical_boundary_certification'])
    def test_core_counts(self):
        self.assertEqual({t:sum(a['pixels'] for a in s.r.load('GEOMETRY.json')['assignments'] if a['owner']==t) for t in s.r.TAGS},{'ANH':167,'ABG':23,'AKT':33,'AZR':56})
    def test_all_runtime_hashes_identical(self):self.assertEqual(s.q.economy.runtime_hashes(),self.b['hashes'])
    def test_registry_identical(self):self.assertEqual(json.loads(s.core.active_registry_path().read_text(encoding='utf8')),self.b['registry'])
    def test_centralization_inputs_protected(self):
        protected=[p for p in self.b['hashes'] if 'imperial_centralization' in p or 'imperial_subjects' in p]
        self.assertTrue(protected)
        for p in protected:self.assertEqual(s.core.sha(s.ROOT/p),self.b['hashes'][p])
    def test_all_anomalies_unresolved_not_silently_fixed(self):self.assertTrue(all(p['Installed_cells']==0 for p in self.data['ANHALT_REMAINING_ANOMALIES.csv']['rows']))
    def test_next_region_not_started(self):self.assertEqual(self.d['next_region'],'STATE_SAXONY');self.assertFalse(self.d['next_region_started'])
    def test_new_source_images_real_and_bounded(self):
        for p in s.load('MAP_SOURCES.json'):
            self.assertEqual(s.core.sha(s.OUT/p['name']),p['sha256']);self.assertEqual(len(p['size']),2)

if __name__=='__main__':unittest.main()
