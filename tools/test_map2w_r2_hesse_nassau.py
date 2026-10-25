"""Current scoped contracts; no Victoria 3 engine execution is claimed."""
import json,unittest
import map2w_r2_hesse_nassau as w
from map2l_registry import expected_country_definitions

class NassauContinuation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=w.load('GEOMETRY.json');cls.m=w.load('REGISTRY_MIGRATION.json');cls.v=w.load('VALIDATION_R2.json');cls.b=w.load('BASELINE.json')
    def test_static_checks_pass(self):self.assertEqual(self.v['passed'],self.v['total'])
    def test_runtime_not_claimed(self):self.assertEqual(self.v['runtime_status'],'NOT_TESTED_MAP2W_R1_OR_R2')
    def test_two_distinct_new_countries(self):self.assertEqual(self.m['new_members'],['NOU','NWB'])
    def test_norway_not_reused(self):self.assertNotIn('NOR',self.m['new_members'])
    def test_only_hesse(self):self.assertEqual(self.m['replaced_regions'],['STATE_HESSE'])
    def test_exact_source_parents(self):self.assertEqual(self.g['parents'],['x1357DB','x3E794B','x8B7C67'])
    def test_72_transfers(self):self.assertEqual(sum(a['pixels'] for a in self.g['assignments'] if a['owner']!=a['previous_owner']),72)
    def test_exact_receivers(self):
        self.assertEqual({tag:sum(a['pixels'] for a in self.g['assignments'] if a['owner']==tag and a['owner']!=a['previous_owner']) for tag in ['NOU','NWB','NAS']},{'NOU':43,'NWB':13,'NAS':16})
    def test_561_parent_cells_preserved(self):self.assertEqual(sum(a['pixels'] for a in self.g['assignments']),561)
    def test_nine_real_rgb_additions(self):self.assertEqual([a['rgb'] for a in self.g['new_provinces']],['xEDB70'+str(n) for n in range(9)])
    def test_no_new_rights_outside_empire(self):self.assertFalse(self.m['extent_added_cells'] or self.m['extent_removed_cells'])
    def test_no_electors_or_city_created(self):self.assertFalse(self.m['free_cities'])
    def test_no_locator_move(self):self.assertTrue(all(r['field']=='prime_land' for r in self.m['region_reference_changes']))
    def test_no_fake_independent_pixel_accuracy(self):self.assertIsNone(w.load('SOURCE_ALIGNMENT.json')['independent_native_error_bound_px'])
    def test_no_fake_census(self):self.assertIsNone(w.load('ALLOCATION.json')['historical_population'])
    def test_global_population_unchanged(self):self.assertEqual(self.v['world_before'],self.v['world_after'])
    def test_no_building_fabrication(self):self.assertTrue(all(r['before']==r['after'][r['source']] for r in w.load('ALLOCATION.json')['profiles'] if r['kind']=='building'))
    def test_hes_exact_tier_change_only(self):
        before=self.b['inventory']['countries'];expected=expected_country_definitions(before,[self.m]);self.assertEqual(set(expected)-set(before),{'NOU','NWB'});self.assertEqual({k for k in before if before[k]!=expected[k]},{'HES'})
    def test_hes_guard_rejects_capital_mutation(self):
        m=json.loads(json.dumps(self.m));m['country_tier_corrections'][0]['after_signature']=m['country_tier_corrections'][0]['after_signature'].replace('STATE_HESSE','STATE_BAVARIA')
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])
    def test_hes_guard_rejects_other_lot(self):
        m=json.loads(json.dumps(self.m));m['new_members']=['SOMETHING']
        with self.assertRaises(AssertionError):expected_country_definitions(self.b['inventory']['countries'],[m])
    def test_inventory_precedes_edit(self):self.assertEqual(w.load('INVENTORY_PHASE.json')['phase'],'BEFORE_FUNCTIONAL_EDITS')
    def test_fulda_20047_preserved(self):self.assertEqual(self.v['country_populations']['FUL'],20047)
    def test_sources_filter_other_jurisdictions(self):self.assertTrue(any(r.get('reason')=='Non-Nassau/edge colour on source sheet' for r in self.g['excluded']))

if __name__=='__main__':unittest.main()
