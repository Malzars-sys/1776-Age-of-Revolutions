"""Differential R8 guards; none of these tests launches Victoria 3."""
import json
import unittest
import numpy as np
import map2m_r8 as w


class InstalledBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=w.load('BASELINE.json');cls.plan=w.load('PLAN.json')
        cls.before=w.core.packed(w.OUT/'provinces_before.png');cls.after=w.core.packed(w.ROOT/'map_data/provinces.png')

    def test_exact_b_not_a_plus_b(self):
        changes=self.plan['changes'];self.assertEqual(len(changes),41)
        self.assertEqual(len({(r['X'],r['Y']) for r in changes}),41)
        rows=[r for r in w.readcsv(w.R7/'PEENE_PROPOSED_CELLS.csv') if r['Variant']=='B']
        self.assertEqual({(r['X'],r['Y']) for r in changes},{(int(r['X']),int(r['Y'])) for r in rows})
        self.assertTrue(np.array_equal(self.after,w.prior.r2.expected_raster(self.before,changes)))

    def test_outside_edit_is_rejected(self):
        altered=self.after.copy();altered[740,4407]^=1
        self.assertFalse(np.array_equal(altered,w.prior.r2.expected_raster(self.before,self.plan['changes'])))

    def test_exact_population_and_no_artificial_attributes(self):
        self.assertEqual(self.plan['source_area'],3629)
        self.assertEqual(self.plan['weights'],{'PRU':3588,'SWE':41})
        self.assertEqual(sum(r['after']['SWE'] for r in self.plan['allocations']),4820)
        for r in self.plan['allocations']:
            self.assertEqual(r['before'],sum(r['after'].values()))
            self.assertEqual(r['after'],w.core.allocate(r['before'],self.plan['weights']))
        originals=w.load('ORIGINAL_TEXT.json')
        for rel,new in w.load('EXPECTED_TEXT.json').items():
            self.assertEqual(w.profiles(originals[rel]),w.profiles(new))
            self.assertNotEqual(w.profiles(originals[rel]),w.profiles(new.replace('size = 4278','size = 4279')))

    def test_all_building_levels_remain_with_existing_owners(self):
        self.assertTrue(self.plan['building_review'])
        self.assertTrue(all(r['allocation']['SWE']==0 and r['allocation']['PRU']==r['levels'] for r in self.plan['building_review']))

    def test_wolgast_and_protected_rows_not_shifted(self):
        self.assertEqual(int(self.after[735,4410]),0xE1A03A)
        self.assertTrue(np.array_equal(self.before[740:],self.after[740:]))
        self.assertTrue(all(r['Y']<740 and r['Decision']=='B_APPROVED_APPROXIMATION' for r in self.plan['changes']))

    def test_thorn_is_only_a_conditional_plan(self):
        a=w.load('THORN_INVENTORY.json');rows=w.readcsv(w.OUT/'THORN_PROPOSED_CORRECTION.csv')
        self.assertEqual(a['pixels'],153);self.assertEqual(a['applied_cells'],0)
        self.assertTrue(np.array_equal(self.before==0x41A021,self.after==0x41A021))
        self.assertEqual(len(rows),153)
        self.assertTrue(all(r['Applied']=='False' and r['Approval']=='NOT_APPROVED' for r in rows))
        self.assertEqual(sum(r['Owner_in_minimal_technical_scenario']=='PLC' for r in rows),1)

    def test_no_engine_or_complete_historical_claim(self):
        v=w.load('VALIDATION.json')
        self.assertFalse(v['engine_tested']);self.assertFalse(v['historical_boundary_complete'])
        self.assertEqual(v['runtime_status'],'PENDING_USER_NEW_GAME_AND_ONE_MONTH')
        self.assertEqual(v['new_RGBs'],[])

    def test_earlier_artifacts_and_git_immutable(self):
        self.assertTrue(all(w.core.sha(w.ROOT/p)==h for p,h in self.b['earlier_proofs'].items()))
        self.assertEqual(w.prior.r2.head(),self.b['git_head'])
        self.assertEqual(w.core.sha(w.ROOT/'.git/index'),self.b['git_index_sha256'])


if __name__=='__main__':unittest.main()
