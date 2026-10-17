"""Regression guards for exact R2 deltas, not engine or historical certification."""
import collections
import unittest
import numpy as np
import map2m_r2 as work


class DeltaTests(unittest.TestCase):
    def test_exact_single_change(self):
        before=np.array([[0x112233,0x445566]],dtype=np.uint32)
        change=dict(X=0,Y=0,RGB_before='x112233',RGB_after='x778899')
        self.assertEqual(work.expected_raster(before,[change]).tolist(),[[0x778899,0x445566]])
        self.assertEqual(before.tolist(),[[0x112233,0x445566]])

    def test_repeated_cell_is_not_silently_accepted(self):
        a=np.array([[0x112233]],dtype=np.uint32)
        c=dict(X=0,Y=0,RGB_before='x112233',RGB_after='x778899')
        with self.assertRaises(ValueError):work.expected_raster(a,[c,c])

    def test_wrong_parent_rejected(self):
        a=np.array([[0x112233]],dtype=np.uint32)
        with self.assertRaises(ValueError):
            work.expected_raster(a,[dict(X=0,Y=0,RGB_before='x123456',RGB_after='x778899')])

    def test_outside_edit_cannot_match_expected_delta(self):
        a=np.array([[0x112233,0x445566]],dtype=np.uint32)
        c=dict(X=0,Y=0,RGB_before='x112233',RGB_after='x778899')
        expected=work.expected_raster(a,[c]);unexpected=expected.copy();unexpected[0,1]=0xAAAAAA
        self.assertFalse(np.array_equal(expected,unexpected))

    def test_reviewed_counts_not_old_hypotheses(self):
        plan=work.load('PLAN.json')
        counts=collections.Counter(c['Sector'] for c in plan['changes'])
        self.assertEqual(counts,{'PEENE':6,'NETZE':85})
        review=work.load('GEOMETRY_REVIEW.json')
        for sector in counts:
            self.assertEqual({(c['X'],c['Y']) for c in plan['changes'] if c['Sector']==sector},set(map(tuple,review[sector]['cells'])))

    def test_no_new_country_or_imperial_netzedistrict(self):
        plan=work.load('PLAN.json');migration=work.load('REGISTRY_MIGRATION.json')
        self.assertEqual(len(plan['new_provinces']),1)
        self.assertEqual(plan['new_provinces'][0]['state'],'STATE_POSEN')
        self.assertEqual(migration['new_members'],[])
        self.assertEqual(migration['updated'],[])

    def test_full_population_profiles_conserved_in_plan(self):
        for row in work.load('PLAN.json')['allocations']:
            self.assertEqual(sum(row['after'].values()),row['before'])
            self.assertTrue(all(v>=0 for v in row['after'].values()))

    def test_only_exact_sources_and_destinations(self):
        for c in work.load('PLAN.json')['changes']:
            self.assertEqual((c['RGB_before'],c['RGB_after'],c['Owner_before'],c['Owner_after']),
                             ('xE1A03A','x567452','PRU','SWE') if c['Sector']=='PEENE' else ('xFCC7B7',work.NEW_RGB,'PLC','PRU'))

    def test_locator_rebound_not_moved(self):
        refs=work.load('PLAN.json')['region_reference_changes']
        ref=next(r for r in refs if r['field']=='farm')
        self.assertFalse(ref['locator_moved'])
        self.assertEqual(ref['pixel'],[4507,767])

    def test_no_false_completion_or_engine_pass(self):
        result=work.load('VALIDATION.json')
        self.assertEqual(result['status'],'MAP-2M_PARTIAL')
        self.assertFalse(result['engine_tested'])
        self.assertTrue(all(not r['historical_geometry_complete'] for r in result['sectors'].values()))


if __name__=='__main__':unittest.main()
