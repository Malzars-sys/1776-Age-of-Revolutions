"""Read-only diagnostic contracts, never engine or geodetic accuracy tests."""
import unittest
import numpy as np
import map2w_r3_calibration as c
from georeference.model import fit

class CalibrationCaseBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=c.load(c.OUT/'PHYSICAL_LANDMARKS.json');cls.d=c.load(c.OUT/'DECISION.json');cls.o=c.load(c.OUT/'REFERENCE_ORIGINS.json')
    def test_case_b_no_install(self):self.assertEqual(self.d['status'],'MAP2W_R3_CALIBRATION_CASE_B');self.assertFalse(self.d['install'])
    def test_blocked_not_ready(self):self.assertEqual(self.d['territorial_delivery_status'],'MAP2W_R3_BLOCKED')
    def test_no_new_country_or_rgb(self):self.assertFalse(self.d['new_functional_modifications'] or self.d['new_RGBs'] or self.d['new_countries'])
    def test_no_runtime_claim(self):self.assertTrue(self.d['no_runtime_validation_requested'])
    def test_six_physical_candidates(self):self.assertEqual(len(self.p['landmarks']),6)
    def test_geographic_source_not_city_points(self):
        for r in self.p['landmarks']:self.assertIn(r['source_selection_rule'],['first_endpoint','maximum_turn_over_700m_in_window'])
    def test_four_fit_candidates_not_observations(self):self.assertEqual(sum(r['role']=='FIT_CANDIDATE' for r in self.p['landmarks']),4);self.assertEqual(self.p['actual_fit_pairs'],0)
    def test_two_reserved_checks_not_used(self):
        r=[r for r in self.p['landmarks'] if r['role']=='CHECK_RESERVED'];self.assertEqual(len(r),2);self.assertTrue(all(not p['used_for_fit'] for p in r));self.assertEqual(self.p['actual_independent_check_pairs'],0)
    def test_no_nearest_pixel_promoted_to_control(self):self.assertTrue(all(r['native_homolog_pixel'] is None for r in self.p['landmarks']))
    def test_residuals_unknown_not_zero(self):
        self.assertTrue(all(r['matched_residual_px'] is None for r in self.p['landmarks']));self.assertIsNone(self.p['local_independent_mean_px']);self.assertIsNone(self.p['local_independent_max_px']);self.assertIsNone(self.p['local_error_bound_px'])
    def test_missing_native_pairs_cannot_fit(self):
        rows=[dict(name=r['id'],geo=r['geo'],pixel=None,role='FIT') for r in self.p['landmarks'] if r['role']=='FIT_CANDIDATE']
        with self.assertRaises(ValueError):fit(rows,'miller_affine')
    def test_all_widths_and_markers_accounted_for(self):
        p=c.load(c.OUT/'NATIVE_PALETTE.json');self.assertIn('NUM_WIDTH_PIXEL_VALUES = 13',p['definition']);self.assertTrue(all(r['river_width']==(3<=r['index']<=15) for r in p['indices']))
    def test_local_corridor_truly_blank_not_palette_filter(self):self.assertEqual(self.p['corridor_native_river_pixels'],0);self.assertEqual(self.p['corridor_all_nonbackground_pixels'],0);self.assertFalse(self.p['corridor_unknown_palette_indices'])
    def test_local_mod_vanilla_agree(self):self.assertTrue(self.p['local_mod_equals_vanilla'])
    def test_both_mouths_not_separate_cell_anchors(self):self.assertLess(self.p['mouths_separation_in_diagnostic_pixels'],1)
    def test_official_source_vertices(self):self.assertEqual({r['name'] for r in self.p['source_geometry']},{'Jagst','Kocher','Neckar'});self.assertEqual(sum(r['vertices'] for r in self.p['source_geometry']),25465)
    def test_old_hub_origins_not_surveys(self):
        anchors={r['name']:r for r in self.o['old_scan']['anchors']};self.assertEqual(anchors['Wurzburg']['native_hub_type'],'wood');self.assertEqual(anchors['Bayreuth']['native_hub_type'],'mine');self.assertTrue(all(not r['geodetic_ground_truth'] for r in anchors.values()))
    def test_exact_three_point_affine_not_extra_accuracy(self):self.assertEqual(self.o['old_scan']['fit_points'],3);self.assertEqual(self.o['old_scan']['parameters'],6);self.assertTrue(self.o['old_scan']['unique_affine_exactly_reproduced'])
    def test_miller_is_extrapolated(self):self.assertEqual(self.o['miller']['fit_points'],5);self.assertTrue(all(r['outside_fit_latitude'] for r in self.o['targets']))
    def test_relief_samples_really_match_packed(self):
        p=c.load(c.OUT/'RELIEF_INSPECTION.json');self.assertEqual(p['sample_count'],110);self.assertEqual(p['sampled_max_abs_difference'],0);self.assertEqual(p['accepted_geographic_summits_or_valley_controls'],0)
    def test_recommendation_not_automatic_r4(self):self.assertIn('only after the user',self.d['recommendation']);self.assertTrue(all(not r['testable_territorial_sublot_prepared'] for r in self.d['alternatives']))
    def test_diagnostic_protections(self):
        v=c.load(c.OUT/'VALIDATION.json');self.assertEqual(v['passed'],v['total']);self.assertFalse(v['engine_execution']);self.assertFalse(v['geographic_accuracy_validated'])

if __name__=='__main__':unittest.main()
