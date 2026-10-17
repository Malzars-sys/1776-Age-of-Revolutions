"""MAP2U exact deltas and negative authority tests. Earlier baselines stay frozen."""
import copy
import unittest
import numpy as np
import map2u_thuringia as u
from map2l_registry import expected_country_definitions,protected_core_preserved

class ThuringianDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=u.load('BASELINE.json');cls.g=u.load('GEOMETRY.json');cls.m=u.load('REGISTRY_MIGRATION.json')
        cls.before=u.core.packed(u.ROOT/cls.b['bitmap_backup']);cls.after=u.core.packed(u.ROOT/'map_data/provinces.png')
        cls.inv=u.core.qa.inventory();cls.owners={r['key'][0]:r['key'][2] for r in cls.inv['owners']}

    def test_exact_world_bitmap_delta(self):
        expected=self.before.copy()
        for row in self.g['assignments']:
            for x,y in row['cells']:expected[y,x]=int(row['rgb'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after))

    def test_only_two_new_countries(self):
        self.assertEqual(set(self.inv['countries'])-set(self.b['inventory']['countries']),{'RLO','REB'})

    def test_country_changes_exactly_authorized(self):
        self.assertEqual(self.inv['countries'],expected_country_definitions(self.b['inventory']['countries'],[self.m]))

    def test_capital_change_cannot_target_prussia(self):
        m=copy.deepcopy(self.m);m['country_capital_corrections'][0]['tag']='PRU'
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_capital_change_cannot_change_tier(self):
        m=copy.deepcopy(self.m);row=m['country_capital_corrections'][0];row['after_signature']=row['after_signature'].replace('principality','kingdom')
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_capital_change_cannot_use_foreign_region(self):
        m=copy.deepcopy(self.m);m['country_capital_corrections'][0]['after']='STATE_BRANDENBURG'
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_capital_change_requires_the_exact_lot(self):
        m=copy.deepcopy(self.m);m['new_members'].append('FRA')
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])

    def test_erfurt_protected(self):
        self.assertTrue(np.array_equal(self.before[822:837,4342:4359],self.after[822:837,4342:4359]))

    def test_map2t_121_cells_and_16_rgbs_preserved(self):
        geo=u.t.load('GEOMETRY.json');self.assertEqual(sum(a['pixels'] for a in geo['assignments'] if a['owner']!=a['previous_owner']),121)
        self.assertEqual(len(geo['new_provinces']),16)
        for a in geo['assignments']:
            if a['owner']!=a['previous_owner'] or a['rgb']!=a['parent_rgb']:self.assertTrue(protected_core_preserved(a,self.after,self.owners,[]))

    def test_anhalt_principalities_unchanged(self):
        for a in u.t.prior.load('GEOMETRY.json')['assignments']:self.assertTrue(protected_core_preserved(a,self.after,self.owners,[]))

    def test_new_cells_connected_and_unique(self):
        self.assertEqual(len(self.g['new_provinces']),4)
        for a in self.g['assignments']:
            self.assertEqual(len(u.core.components(self.after==int(a['rgb'][1:],16))),1)
            if a['rgb']!=a['parent_rgb']:self.assertFalse(np.any(self.before==int(a['rgb'][1:],16)))

    def test_sondershausen_city_reference_is_inside_sso(self):
        self.assertEqual(self.owners['x'+format(int(self.after[819,4348]),'06X')],'SSO')

    def test_southern_sso_is_unchanged(self):
        old=[r for r in self.b['inventory']['regional_pop'] if r['key'][:2]==['STATE_SAXONY','SSO']]
        self.assertEqual(old,[r for r in self.inv['regional_pop'] if r['key'][:2]==['STATE_SAXONY','SSO']])

    def test_no_territorial_corridor_between_sso_halves(self):
        sso=[int(rgb[1:],16) for rgb,tag in self.owners.items() if tag=='SSO']
        self.assertGreater(len(u.core.components(np.isin(self.after,sso))),1)

    def test_economic_and_military_invariants(self):
        for key in ['buildings','building_levels_written']:self.assertEqual(u.row_counter(self.inv[key]),u.expected_field(self.b,key))
        self.assertEqual(self.inv['units'],self.b['inventory']['units'])

    def test_world_profiles_and_hlb_preserved(self):
        self.assertEqual(self.inv['pops'],self.b['inventory']['pops'])
        self.assertEqual(sum(r['count'] for r in self.inv['regional_pop'] if r['key'][1]=='HLB'),9206)

    def test_populations_not_fabricated(self):
        for p in u.load('POPULATION_ALLOCATION.json')['profiles']:
            self.assertEqual(sum(p['after'].values()),p['before'])
            self.assertTrue(all(isinstance(v,int) and v>=0 for v in p['after'].values()))

    def test_no_new_electors_or_native_imperial_subjects(self):
        from map2k_patch import ELECTORS
        self.assertTrue('SAX' in ELECTORS.values());self.assertFalse(set(u.NEW_TAGS)&set(ELECTORS.values()))
        for tag in u.NEW_TAGS:self.assertNotIn('create_diplomatic_pact',(u.ROOT/('common/history/countries/'+tag.lower()+' - map2u.txt')).read_text(encoding='utf8'))

    def test_county_not_post1776_princely_title(self):
        gov=(u.ROOT/'common/government_types/00_1776_map2u.txt').read_text(encoding='utf8')
        self.assertIn('RULER_TITLE_COUNT',gov);self.assertNotIn('RULER_TITLE_PRINCE',gov)
        self.assertIn('1702.7.19',(u.ROOT/'common/history/characters/rlo - map2u.txt').read_text(encoding='utf8'))
        self.assertIn('1724.1.22',(u.ROOT/'common/history/characters/reb - map2u.txt').read_text(encoding='utf8'))

    def test_inherited_anomalies_not_increased(self):
        for key in ['duplicates','errors']:self.assertEqual(self.inv[key],self.b['inventory'][key])

    def test_one_cell_ebersdorf_abstraction_is_explicit(self):
        row=self.g['traces'][1]['one_cell_quantization']
        self.assertEqual(row['cell'],[4365,845]);self.assertGreater(row['inward_polygon_coverage'],.1)

    def test_projection_preserved_not_reoptimized(self):
        a=u.load('SOURCE_ALIGNMENT.json');self.assertFalse(a['native_model_refitted']);self.assertIsNone(a['independent_error_bound_px'])

if __name__=='__main__':unittest.main()
