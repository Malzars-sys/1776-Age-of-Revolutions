"""MAP2T exact scoped-delta and negative authorization tests."""
import copy
import unittest
import numpy as np
import map2t_saxony as t
from map2l_registry import expected_country_definitions

class SaxonDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=t.load('BASELINE.json');cls.g=t.load('GEOMETRY.json');cls.m=t.load('REGISTRY_MIGRATION.json')
        cls.before=t.core.packed(t.ROOT/cls.b['bitmap_backup']);cls.after=t.core.packed(t.ROOT/'map_data/provinces.png');cls.inv=t.core.qa.inventory()

    def test_exact_declared_bitmap(self):
        expected=self.before.copy()
        for r in self.g['assignments']:
            for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after))

    def test_every_protected_erfurt_cell_unchanged(self):
        self.assertTrue(np.array_equal(self.before[822:837,4342:4359],self.after[822:837,4342:4359]))

    def test_no_other_state_touched(self):
        colors=[int(r['key'][0][1:],16) for r in self.b['inventory']['owners'] if r['key'][1]!=t.SID]
        mask=np.isin(self.before,colors)
        self.assertTrue(np.array_equal(self.before[mask],self.after[mask]))

    def test_only_six_approved_new_tags(self):
        self.assertEqual(set(self.inv['countries'])-set(self.b['inventory']['countries']),set(t.NEW_TAGS))

    def test_all_economic_and_military_data_unchanged(self):
        for key in ['buildings','building_levels_written','units']:self.assertEqual(self.inv[key],self.b['inventory'][key])

    def test_all_world_culture_and_religion_profiles_preserved(self):
        self.assertEqual(self.inv['pops'],self.b['inventory']['pops'])

    def test_no_new_inherited_anomalies(self):
        for key in ['duplicates','errors']:self.assertEqual(self.inv[key],self.b['inventory'][key])

    def test_country_changes_exact(self):
        self.assertEqual(self.inv['countries'],expected_country_definitions(self.b['inventory']['countries'],[self.m]))

    def test_tier_does_not_authorize_capital_change(self):
        m=copy.deepcopy(self.m);m['country_tier_corrections'][0]['after_signature']=m['country_tier_corrections'][0]['after_signature'].replace('STATE_SAXONY','STATE_BRANDENBURG')
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_tier_does_not_authorize_a_foreign_country(self):
        m=copy.deepcopy(self.m);m['country_tier_corrections'][0]['tag']='PRU'
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_tier_does_not_authorize_other_members(self):
        m=copy.deepcopy(self.m);m['new_members'].append('FRA')
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_new_colours_unique_and_connected(self):
        self.assertEqual(len({r['rgb'] for r in self.g['new_provinces']}),16)
        for r in self.g['assignments']:self.assertEqual(len(t.core.components(self.after==int(r['rgb'][1:],16))),1)

    def test_no_post1776_reuss_unification(self):
        self.assertTrue({'RGZ','RGE','RSL'}<=set(self.inv['countries']))
        self.assertFalse({'RLO','REB'}&set(self.m['new_members']))

    def test_sax_is_still_an_elector(self):
        from map2k_patch import ELECTORS
        self.assertIn('SAX',ELECTORS.values());self.assertFalse(set(t.NEW_TAGS)&set(ELECTORS.values()))

    def test_population_allocations_are_integer_and_conservative(self):
        for row in t.load('POPULATION_ALLOCATION.json')['profiles']:
            self.assertEqual(row['before'],sum(row['after'].values()))
            self.assertTrue(all(isinstance(v,int) and v>=0 for v in row['after'].values()))

    def test_native_projection_not_refitted(self):
        self.assertFalse(t.load('ALIGNMENT.json')['native_model_refitted'])
        self.assertIsNone(t.load('ALIGNMENT.json')['native_position_error_bound'])

    def test_initial_states_are_not_native_imperial_subjects(self):
        for tag in t.NEW_TAGS:
            text=(t.ROOT/('common/history/countries/'+tag.lower()+' - map2t.txt')).read_text(encoding='utf8')
            self.assertNotIn('create_diplomatic_pact',text)

if __name__=='__main__':unittest.main()
