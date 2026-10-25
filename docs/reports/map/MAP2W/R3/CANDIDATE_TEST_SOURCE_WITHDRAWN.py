"""R3-A1 current and negative contracts; these are not engine tests."""
import copy,json,re,unittest
from pathlib import Path
from unittest.mock import patch
import map2w_r3_franconia as w
import map2l_registry as reg

class HohenloheCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=w.load('GEOMETRY.json');cls.m=w.load('REGISTRY_MIGRATION.json');cls.v=w.load('VALIDATION.json');cls.b=w.load('BASELINE.json')
    def test_static_checks(self):self.assertEqual(self.v['passed'],self.v['total'])
    def test_scoped_status(self):self.assertEqual(self.v['status'],'MAP2W_R3_READY_FOR_SCOPED_RUNTIME_VALIDATION')
    def test_no_engine_claim(self):self.assertEqual(self.v['runtime_status'],'NOT_TESTED_R3')
    def test_manual_r2b_attestation_only(self):
        r=json.loads((w.OUT.parent/'R2B/RUNTIME_USER_ATTESTATION.json').read_text());self.assertEqual(r['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertFalse(r['R3_changes_covered']);self.assertEqual(r['confirmed_by_user']['protocol_checks_confirmed'],9)
    def test_exact_members(self):self.assertEqual(self.m['new_members'],['HLN','HKI'])
    def test_only_one_state(self):self.assertEqual(self.m['replaced_regions'],['STATE_FRANCONIA'])
    def test_exact_parent_residual(self):self.assertEqual(self.g['parents'],['xEDA218'])
    def test_seven_transfers(self):self.assertEqual(sum(r['pixels'] for r in self.g['assignments'] if r['owner']!='BAV'),7)
    def test_no_one_cell_country(self):self.assertTrue(all(r['pixels']>=3 for r in self.g['assignments'] if r['owner']!='BAV'))
    def test_new_colours(self):self.assertEqual([r['rgb'] for r in self.g['new_provinces']],['xEDB900','xEDB901','xEDB902','xEDB903'])
    def test_no_historical_population_invention(self):self.assertIsNone(w.load('ALLOCATION.json')['historical_population'])
    def test_population_conserved(self):self.assertEqual(self.v['world_after'],835801255)
    def test_no_invented_subject(self):self.assertFalse(any('/diplomacy/' in p for p in w.load('EXPECTED_TEXT.json')))
    def test_no_new_factories_or_army(self):self.assertFalse(any('/buildings/' in p or '/military_formations/' in p for p in w.load('EXPECTED_TEXT.json')))
    def test_no_locator_motion_or_resource_change(self):self.assertFalse(self.m['region_reference_changes'])
    def test_no_new_elector_or_city(self):
        from map2k_patch import ELECTORS
        self.assertEqual(len(ELECTORS),9);self.assertFalse(set(self.m['new_members'])&set(ELECTORS.values()));self.assertFalse(self.m['free_cities'])
    def test_unchanged_imperial_extent(self):self.assertFalse(self.m['extent_added_cells'] or self.m['extent_removed_cells'])
    def test_old_anomalies_not_hidden(self):self.assertEqual(self.v['preexisting_duplicate_RGBs'],44);self.assertEqual(len(self.v['preexisting_invalid_references']),12);self.assertFalse(self.v['new_errors'])
    def test_lineage_not_one_tag_per_name(self):self.assertNotIn('HWA',self.m['new_members']);self.assertNotIn('HLA',self.m['new_members'])
    def test_prince_government_scoped(self):
        n=w.core.cw.parse((w.ROOT/'common/government_types/00_1776_map2w_r3_hohenlohe.txt').read_text())[0]
        self.assertEqual(n.one('male_ruler'),'"RULER_TITLE_PRINCE"');self.assertEqual({z.key for z in n.children('possible')[0].children('OR')[0].children()},{'c:HLN','c:HKI'})
    def test_localisation_pair(self):
        sets=[set(re.findall(r'^\s*([A-Za-z0-9_.-]+):0', (w.ROOT/f'localization/{l}/1776_map2w_r3_l_{l}.yml').read_text(encoding='utf-8-sig'),re.M)) for l in ['french','english']];self.assertEqual(sets[0],sets[1]);self.assertEqual(len(sets[0]),10)
    def test_not_false_native_calibration(self):self.assertIn('NOT independent native',w.load('SOURCE_ALIGNMENT.json')['warning'])
    def test_1800_enclaves_not_all_imported(self):self.assertTrue(all(t['detached_parts_deferred']>0 for t in self.g['traces']))
    def mutate_geometry(self,change):
        original=Path.read_text;data=copy.deepcopy(self.g);change(data)
        def reader(p,*args,**kwargs):return json.dumps(data) if p==w.OUT/'GEOMETRY.json' else original(p,*args,**kwargs)
        with patch.object(Path,'read_text',autospec=True,side_effect=reader):
            with self.assertRaises(AssertionError):reg.approved_lot_dirs()
    def test_guard_rejects_ansbach_parent(self):self.mutate_geometry(lambda g:g['parents'].append('xEDA217'))
    def test_guard_rejects_bartenstein_substitution(self):self.mutate_geometry(lambda g:g['assignments'][-1].update(owner='HBA'))
    def test_guard_rejects_different_cell_even_in_box(self):self.mutate_geometry(lambda g:g['assignments'][-1]['cells'].__setitem__(0,[4326,880]))
    def test_guard_rejects_thuringia(self):self.mutate_geometry(lambda g:g['assignments'][-1].update(state='STATE_SAXONY'))
    def test_guard_accepts_reviewed_layer(self):self.assertEqual(reg.approved_lot_dirs()[-1],w.OUT)

if __name__=='__main__':unittest.main()
