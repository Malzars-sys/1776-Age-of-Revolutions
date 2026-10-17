import unittest
import numpy as np
import map2m_r9 as w

class R9Guards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=w.load('PLAN.json');cls.before=w.core.packed(w.OUT/'provinces_before.png');cls.after=w.core.packed(w.ROOT/'map_data/provinces.png')

    def test_exact_two_cells_and_no_elsewhere_edit(self):
        self.assertEqual({(r['X'],r['Y']) for r in self.plan['changes']},{(4409,735),(4410,735)})
        self.assertTrue(np.array_equal(self.after,w.old.prior.r2.expected_raster(self.before,self.plan['changes'])))
        changed=self.after.copy();changed[740,4410]^=1
        self.assertFalse(np.array_equal(changed,w.old.prior.r2.expected_raster(self.before,self.plan['changes'])))

    def test_prior398_and_all41_r8_cells_preserved(self):
        self.assertEqual(int((self.before==0x567452).sum()),398)
        self.assertTrue(np.all(self.after[self.before==0x567452]==0x567452))
        self.assertTrue(all(self.after[r['Y'],r['X']]==0x567452 for r in w.old.load('PLAN.json')['changes']))

    def test_no_fake_wolgast_city_or_moved_locator(self):
        rows=w.old.readcsv(w.OUT/'PEENE_NATIVE_LOCATORS.csv')
        self.assertEqual([(r['Kind'],r['ID']) for r in rows if r['ID']=='57'],[('city','57'),('mine','57'),('port','57')])
        b=w.load('BASELINE.json');self.assertTrue(all(w.core.sha(w.ROOT/p)==h for p,h in b['hashes'].items() if p.startswith('gfx/map/map_object_data/')))

    def test_demographic_conservation_and_negative_guard(self):
        self.assertEqual(sum(r['after']['SWE'] for r in self.plan['allocations']),235)
        for r in self.plan['allocations']:self.assertEqual(r['after'],w.core.allocate(r['before'],self.plan['weights']))
        for rel,new in w.load('EXPECTED_TEXT.json').items():
            old=w.load('ORIGINAL_TEXT.json')[rel]
            self.assertEqual(w.old.profiles(old),w.old.profiles(new))
            self.assertNotEqual(w.old.profiles(old),w.old.profiles(new.replace('size = 209','size = 210')))

    def test_no_unapplied_proposal_in_change_csvs(self):
        for name in ['PRUSSIA_POLAND_CHANGES.csv','PRUSSIAN_HRE_BORDER_CHANGES.csv']:self.assertEqual(w.old.readcsv(w.OUT/name),[])
        self.assertEqual(len(w.old.readcsv(w.OUT/'TERRITORIAL_CHANGES.csv')),2)

    def test_thorn_really_unchanged_and_proposals_separate(self):
        self.assertTrue(np.array_equal(self.before==0x41A021,self.after==0x41A021))
        self.assertEqual(int((self.after==0x41A021).sum()),153)
        self.assertTrue(all(r['Applied']=='False' for r in w.old.readcsv(w.OUT/'THORN_ARBITRATION_PROPOSALS.csv')))

    def test_progress_covers_registry_without_starting_next_lot(self):
        summary=w.load('PROGRESS_SUMMARY.json');self.assertTrue(summary['all_registered_states_covered']);self.assertFalse(summary['next_lot_started'])
        rows=w.old.readcsv(w.OUT/'HRE_REGIONS_INVENTORY.csv')
        self.assertTrue(all(r['Status'] in {'VALIDATED','IMPLEMENTED','PARTIAL','RESEARCHED_ONLY','AUDITED_ONLY','NOT_STARTED','UNKNOWN'} for r in rows))
        self.assertEqual(next(r for r in rows if r['Region']=='Wismar–Poel–Neukloster')['Status'],'RESEARCHED_ONLY')

    def test_no_fake_runtime_or_full_historical_completion(self):
        v=w.load('VALIDATION.json');self.assertEqual(v['status'],'MAP-2M-R9_PARTIAL');self.assertFalse(v['engine_tested']);self.assertFalse(v['R8_runtime_user_validated']);self.assertFalse(v['historical_boundary_certified'])
        self.assertEqual(v['peene_status'],'PEENE_GAMEPLAY_COMPLETE')

if __name__=='__main__':unittest.main()
