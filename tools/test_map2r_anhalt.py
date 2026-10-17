"""MAP2R delta guards; old snapshot expectations are deliberately not rewritten."""
import unittest,json,collections
import numpy as np
import map2r_anhalt as r

class AnhaltDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=r.load('BASELINE.json');cls.g=r.load('GEOMETRY.json')
        cls.before=r.q.core.packed(r.ROOT/cls.b['bitmap_backup'])
        cls.after=r.q.core.packed(r.ROOT/'map_data/provinces.png')
        cls.inv=r.q.core.qa.inventory()
    def test_exact_bitmap_and_no_external_change(self):
        expected=self.before.copy()
        for a in self.g['assignments']:
            self.assertEqual(a['previous_owner'],'ANH');self.assertEqual(a['state'],'STATE_ANHALT')
            for x,y in a['cells']:expected[y,x]=int(a['rgb'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after))
    def test_four_tags_and_only_three_new_countries(self):
        self.assertEqual(set(self.inv['countries'])-set(self.b['inventory']['countries']),{'ABG','AKT','AZR'})
        owners={a['owner'] for a in self.g['assignments']};self.assertEqual(owners,set(r.TAGS))
    def test_all_economy_and_units_preserved(self):
        for key in ['buildings','building_levels_written','units']:
            self.assertEqual(self.inv[key],self.b['inventory'][key],key)
    def test_no_population_fabrication(self):
        self.assertEqual(self.inv['pops'],self.b['inventory']['pops'])
        self.assertEqual(sum(p['count'] for p in self.inv['regional_pop'] if p['key'][1]=='HLB'),9206)
    def test_registry_and_non_electoral_members(self):
        m=r.load('REGISTRY_MIGRATION.json');self.assertEqual(m['new_members'],['ABG','AKT','AZR']);self.assertEqual(m['free_cities'],[])
        self.assertEqual(m['extent_added_cells'],[]);self.assertEqual(m['extent_removed_cells'],[])
        from map2k_patch import ELECTORS
        self.assertFalse(set(ELECTORS)&{'ABG','AKT','AZR'})
    def test_jever_and_all_prussian_cells_unchanged(self):
        colors=[int(p['key'][0][1:],16) for p in self.b['inventory']['owners'] if p['key'][2]=='PRU' or p['key'][1]=='STATE_HANNOVER']
        mask=np.isin(self.before,colors);self.assertTrue(np.array_equal(self.before[mask],self.after[mask]))
    def test_preexisting_anomalies_not_excused_or_increased(self):
        self.assertEqual(self.inv['duplicates'],self.b['inventory']['duplicates']);self.assertEqual(self.inv['errors'],self.b['inventory']['errors'])
    def test_1776_rulers_not_1836_templates(self):
        for tag in r.TAGS:
            p='common/history/characters/'+('anh - anhalt.txt' if tag=='ANH' else tag.lower()+' - map2r anhalt.txt')
            text=(r.ROOT/p).read_text(encoding='utf-8-sig')
            self.assertIn('ruler = yes',text);self.assertNotIn('template = ANH_',text)
    def test_parent_cells_and_connectivity(self):
        self.assertEqual(sum(a['pixels'] for a in self.g['assignments']),279)
        for a in self.g['assignments']:
            self.assertEqual(len(r.q.core.components(self.after==int(a['rgb'][1:],16))),1)
    def test_name_correction_rejects_capital_change(self):
        import copy
        from map2l_registry import expected_country_definitions
        m=copy.deepcopy(r.load('REGISTRY_MIGRATION.json'))
        m['anhalt_name_correction']['after_signature']=m['anhalt_name_correction']['after_signature'].replace('STATE_ANHALT','STATE_BRANDENBURG')
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])
    def test_name_correction_rejects_other_country(self):
        import copy
        from map2l_registry import expected_country_definitions
        m=copy.deepcopy(r.load('REGISTRY_MIGRATION.json'));m['anhalt_name_correction']['tag']='PRU'
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

if __name__=='__main__':unittest.main()
