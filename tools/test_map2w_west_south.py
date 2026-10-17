import json,unittest
import map2w_west_south as w

class MAP2W(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=w.load('GEOMETRY.json');cls.b=w.load('BASELINE.json');cls.v=w.load('VALIDATION.json');cls.m=w.load('REGISTRY_MIGRATION.json')
    def test_no_static_failure(self):self.assertEqual(self.v['passed'],self.v['total'])
    def test_runtime_not_claimed(self):self.assertEqual(self.v['runtime_status'],'NOT_TESTED_MAP2W')
    def test_one_country(self):self.assertEqual(self.m['new_members'],['FUL'])
    def test_only_two_regions(self):self.assertEqual(self.m['replaced_regions'],['STATE_HESSE','STATE_SAXONY'])
    def test_only_two_parents(self):self.assertEqual(self.g['parents'],['xD04121','xD0C021'])
    def test_39_transfers(self):self.assertEqual(sum(a['pixels'] for a in self.g['assignments'] if a['owner']=='FUL'),39)
    def test_four_new_rgb(self):self.assertEqual(len(self.g['new_provinces']),4)
    def test_all_parent_cells(self):self.assertEqual(sum(a['pixels'] for a in self.g['assignments']),345)
    def test_no_extent_change(self):self.assertFalse(self.m['extent_added_cells'] or self.m['extent_removed_cells'])
    def test_no_elector(self):self.assertFalse(self.m['free_cities'])
    def test_real_country_only(self):self.assertEqual(set(self.m['country_additions']),{'FUL'})
    def test_no_hub_fabrication(self):self.assertEqual({r['field'] for r in self.m['region_reference_changes']},{'prime_land'})
    def test_population_technical(self):self.assertIsNone(w.load('POPULATION_ALLOCATION.json')['historical_population'])
    def test_world_stable(self):self.assertEqual(self.v['world_before'],self.v['world_after'])
    def test_independent_precision_not_invented(self):self.assertIsNone(w.load('SOURCE_ALIGNMENT.json')['independent_native_error_bound_px'])
    def test_inventory_first(self):self.assertEqual(w.load('INVENTORY_PHASE.json')['phase'],'BEFORE_FUNCTIONAL_EDITS')
    def test_previous_manual_receipt(self):self.assertEqual(w.load('PREVIOUS_LOTS_RUNTIME_USER_ATTESTATION.json')['status'],'PASS_RUNTIME_USER_VALIDATED')

if __name__=='__main__':unittest.main()
