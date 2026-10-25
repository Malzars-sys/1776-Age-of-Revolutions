"""R4 evidence, holdout discipline and no-installation contracts, not engine tests."""
import json
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import map2w_r4_bavaria as w

class BavariaDiagnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=w.load(w.OUT/'CALIBRATION.json');cls.a=w.load(w.OUT/'GEOGRAPHIC_ASSESSMENT.json');cls.t=w.load(w.OUT/'TERRITORIAL_CHANGES.json');cls.v=w.load(w.OUT/'VALIDATION.json')
    def test_not_ready(self):self.assertEqual(self.t['status'],'MAP2W_R4_BLOCKED')
    def test_zero_functional_changes(self):
        self.assertFalse(self.t['transfers'] or self.t['new_RGBs'] or self.t['new_countries']);self.assertEqual(self.t['changed_cells'],0)
    def test_no_migration(self):self.assertFalse((w.OUT/'REGISTRY_MIGRATION.json').exists())
    def test_frozen_protocol(self):
        self.assertEqual(w.sha(w.OUT/'CONTROL_PROTOCOL.json'),self.c['protocol_sha256']);self.assertTrue(self.c['no_second_optimisation'])
    def test_no_hub_or_inherited_fit(self):self.assertTrue(self.c['no_hub_or_inherited_model_used'])
    def test_native_marker_observations(self):
        a=np.array(Image.open(w.ROOT/'map_data/rivers.png'))
        for r in self.c['controls']:
            x,y=r['native_marker'];self.assertEqual(a[y,x],1);self.assertEqual(r['native_pixel'],[x+.5,y+.5])
    def test_named_geographic_junctions(self):
        for r in self.c['controls']:self.assertTrue(r['source_junction_alternatives'])
    def test_exactly_three_fits(self):self.assertEqual(sum(r['role']=='FIT' for r in self.c['controls']),3)
    def test_real_independent_holdout(self):
        self.assertEqual([r['id'] for r in self.c['controls'] if r['role']=='CHECK'],['ISAR']);self.assertEqual(self.c['independent_check_count'],1)
    def test_recompute_without_holdout(self):
        fit=[r for r in self.c['controls'] if r['role']=='FIT'];X=np.array([[*r['geo'],1] for r in fit]);Y=np.array([r['native_pixel'] for r in fit]);self.assertTrue(np.allclose(np.linalg.solve(X,Y),self.c['matrix']))
    def test_holdout_error_not_zero(self):
        r=next(r for r in self.c['controls'] if r['role']=='CHECK');v=np.r_[r['geo'],1]@np.array(self.c['matrix']);error=float(np.linalg.norm(v-r['native_pixel']));self.assertAlmostEqual(error,self.c['independent_max_px']);self.assertGreater(error,4)
    def test_one_check_not_regional_certificate(self):self.assertIsNone(self.c['certified_error_bound_px'])
    def test_uncertainty_not_quantisation_only(self):
        for r in self.c['city_diagnostics']:self.assertIsNone(r['actual_total_position_uncertainty_px']);self.assertTrue(r['not_accepted_city_location'])
    def test_source_raster_axis_order(self):
        for r in self.c['controls']:self.assertTrue(9<r['geo'][0]<14 and 47<r['geo'][1]<50)
    def test_official_sources_not_truncated_at_count(self):
        for r in w.load(w.OUT/'EVIDENCE/STATION_REQUESTS_4326.json'):
            self.assertFalse(r['error']);self.assertTrue(0<int(r['number_returned'])<1000)
        r=w.load(w.OUT/'EVIDENCE/CONTEXT_REQUEST.json');self.assertFalse(r['error']);self.assertLess(int(r['number_returned']),10000)
    def test_source_integrity(self):
        for r in self.c['controls']:
            p=w.OUT/'EVIDENCE'/(r['id']+'_STATION_4326.gml');self.assertEqual(w.sha(p),r['source_sha256'])
    def test_historical_sheet_not_claimed_1776(self):
        doc=w.load(w.OUT/'EVIDENCE/BSB_1791_MANIFEST.json');self.assertEqual(doc['navDate'],'1791-01-01T00:00:00Z')
    def test_failed_service_calls_not_used_as_evidence(self):
        p=w.OUT/'EVIDENCE/INN_AXES.gml';self.assertTrue(ET.parse(p).getroot().tag.endswith('ExceptionReport'));self.assertNotEqual(w.sha(p),next(r for r in self.c['controls'] if r['id']=='INN')['source_sha256'])
    def test_existing_eichstaett_preserved(self):
        self.assertEqual({r['rgb'] for r in self.a['installed_eichstaett']},{'xEDA21C','xEDA801','xEDA802','xEDA803'});self.assertEqual(sum(r['pixels'] for r in self.a['installed_eichstaett']),103)
    def test_sampled_RGB_not_treated_as_ownership_proof(self):
        for r in self.a['diagnostic_windows']:self.assertTrue(r['not_city_or_sovereignty_validation'])
    def test_no_accepted_polygons(self):self.assertFalse(self.a['accepted_polygons'] or self.a['accepted_RGB_transfers'])
    def test_area_screen_not_accuracy_bound(self):
        a=self.a['passau_area_screening'];self.assertIn('NOT an accepted territorial polygon',a['limitation']);self.assertLess(a['maximum_possible_inscribed_disk_radius_px_under_area_assumption'],5)
    def test_population_conservation(self):
        p=w.load(w.OUT/'POPULATION_VALIDATION.json');self.assertEqual(p['world_before'],p['world_after']);self.assertEqual(p['new_people'],0);self.assertTrue(p['regional_profiles_unchanged'] and p['building_profiles_unchanged'] and p['units_unchanged'])
    def test_before_after_identical_panels(self):
        p=np.array(Image.open(w.OUT/'BEFORE_AFTER.png'));self.assertTrue(np.array_equal(p[65:485,20:620],p[65:485,640:1240]))
    def test_protection_current_receipt(self):self.assertEqual(self.v['passed'],self.v['total']);self.assertFalse(self.v['engine_test_executed'])
    def test_no_runtime_claim(self):self.assertEqual(self.v['new_territorial_runtime_validation'],'NOT_APPLICABLE_NO_INSTALL');self.assertFalse(self.v['historical_geometry_validated'])

if __name__=='__main__':unittest.main()
