"""R3 differential safeguards: not an engine test or historical certification."""
import unittest
import numpy as np
import map2m_r3 as work


class ContinuationTests(unittest.TestCase):
    def test_delta_is_exact_and_all_new_peene_cells(self):
        p=work.load('PLAN.json');g=work.load('GEOMETRY_REVIEW.json')
        self.assertEqual(len(p['changes']),10)
        self.assertEqual({(v['X'],v['Y']) for v in p['changes']},set(map(tuple,g['PEENE']['cells'])))
        self.assertTrue(all((v['Sector'],v['RGB_before'],v['RGB_after'],v['Owner_before'],v['Owner_after'])==
            ('PEENE','xE1A03A','x567452','PRU','SWE') for v in p['changes']))

    def test_no_netze_transfer_or_new_rgb_invented(self):
        p=work.load('PLAN.json')
        self.assertEqual(p['new_provinces'],[])
        self.assertEqual(p['netze_applied_cells'],0)
        self.assertEqual(work.load('GEOMETRY_REVIEW.json')['NETZE']['cells'],[])

    def test_population_exact_and_buildings_all_retained(self):
        p=work.load('PLAN.json')
        self.assertEqual(sum(v['after']['SWE'] for v in p['allocations']),1175)
        for v in p['allocations']:
            self.assertEqual(sum(v['after'].values()),v['before'])
            self.assertTrue(all(n>=0 for n in v['after'].values()))
        self.assertTrue(p['building_review'])
        self.assertTrue(all(v['allocation']['SWE']==0 and v['allocation']['PRU']==v['levels'] for v in p['building_review']))

    def test_frozen_r2_and_no_outside_delta(self):
        core=work.r2.core;b=work.load('BASELINE.json');p=work.load('PLAN.json')
        before=core.packed(work.ROOT/b['bitmap_backup']);after=core.packed(work.ROOT/'map_data/provinces.png')
        self.assertTrue(np.array_equal(after,work.r2.expected_raster(before,p['changes'])))
        for v in work.r2.load('PLAN.json')['changes']:
            self.assertEqual(int(after[v['Y'],v['X']]),int(v['RGB_after'][1:],16))
        altered=after.copy();altered[0,0]^=1
        self.assertFalse(np.array_equal(altered,work.r2.expected_raster(before,p['changes'])))

    def test_manual_receipt_never_promotes_r3(self):
        receipt=work.load('R2_USER_RUNTIME_VALIDATION.json');result=work.load('VALIDATION.json')
        self.assertEqual(receipt['status'],'PASS_RUNTIME_USER_VALIDATED')
        self.assertFalse(receipt['automated_engine_test'])
        self.assertIsNone(receipt['simulation_duration'])
        self.assertFalse(receipt['R3_new_changes_user_validated'])
        self.assertEqual(result['status'],'MAP-2M-R3_PARTIAL')
        self.assertFalse(result['engine_tested'])

    def test_no_claim_of_certified_city_accuracy(self):
        g=work.load('GEOMETRY_REVIEW.json')
        self.assertEqual(len(g['coastal_checks']),5)
        self.assertTrue(all(v['role']=='CHECK_NOT_USED_IN_FIT' and 'not a certified city' in v['quality'] for v in g['coastal_checks']))
        self.assertTrue(all(not v['historical_geometry_complete'] for v in work.load('VALIDATION.json')['sectors'].values()))


if __name__=='__main__':unittest.main()
