"""Passau's scoped static contracts; these are not engine tests."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import map2w_r4_political as w
import map2l_registry as reg

class PassauPoliticalPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=w.load(w.OUT/'GEOMETRY.json');cls.m=w.load(w.OUT/'REGISTRY_MIGRATION.json')
        cls.v=w.load(w.OUT/'VALIDATION.json');cls.b=w.load(w.OUT/'BASELINE.json')
        cls.c=w.load(w.OUT/'CANDIDATES.json');cls.a=w.load(w.OUT/'ALLOCATION.json')
        cls.bitmap=w.packed()
    def test_static_receipt(self):self.assertEqual(self.v['passed'],self.v['total'])
    def test_runtime_not_claimed(self):self.assertFalse(self.v['engine_test_executed']);self.assertEqual(self.v['manual_validation_status'],'NOT_TESTED_NEW_PASSAU_CORE')
    def test_class_b_not_geodesy(self):self.assertEqual(self.g['classification'],'B_POLITICAL_APPROXIMATION');self.assertFalse(self.g['historical_cadastral_precision'])
    def test_only_bavaria(self):self.assertEqual(self.m['replaced_regions'],['STATE_BAVARIA'])
    def test_single_new_country(self):self.assertEqual(self.m['new_members'],['PAS']);self.assertEqual(set(self.m['country_additions']),{'PAS'})
    def test_one_new_rgb(self):self.assertEqual(self.g['new_provinces'],[{'rgb':'xEDBA00','parent_rgb':'xB08021'}])
    def test_no_old_core_split(self):self.assertEqual(self.g['parents'],['xB08021'])
    def test_exact_raster_cells(self):
        actual={(int(x),int(y)) for y,x in np.argwhere(self.bitmap==0xEDBA00)}
        proposed={(r['x'],r['y']) for r in self.c['options'][0]['cells']}
        self.assertEqual(actual,proposed);self.assertEqual(len(actual),40)
    def test_parent_residual(self):self.assertEqual(int((self.bitmap==0xB08021).sum()),212)
    def test_both_rgb_connected(self):
        for rgb in [0xEDBA00,0xB08021]:self.assertEqual(len(w.prior.core.components(self.bitmap==rgb)),1)
    def test_option_two_rejected_fragmentation(self):
        p=self.c['options'][1];self.assertEqual(p['cell_count'],83)
        self.assertEqual(p['donor_state_components_after'],[3306,52,5,3,1,1,1])
    def test_no_extent_or_hub_changes(self):self.assertFalse(self.m['extent_added_cells'] or self.m['extent_removed_cells'] or self.m['region_reference_changes'])
    def test_nine_electors_no_free_city(self):
        from map2k_patch import ELECTORS
        self.assertEqual(len(ELECTORS),9);self.assertNotIn('PAS',ELECTORS.values());self.assertFalse(self.m['free_cities'])
    def test_world_population_conserved(self):self.assertEqual((self.v['world_before'],self.v['world_after']),(835801255,835801255))
    def test_population_not_census(self):self.assertIsNone(self.a['historical_population']);self.assertEqual(self.a['PAS_population'],14267)
    def test_every_profile_conserved(self):
        for r in self.a['profiles']:self.assertEqual(sum(r['after'].values()),r['before'])
    def test_207_scope_guards(self):self.assertEqual(self.v['total'],207);self.assertFalse(self.v['new_errors'])
    def test_preexisting_debt_separate(self):self.assertEqual(self.v['preexisting_duplicate_RGBs'],44);self.assertEqual(len(self.v['preexisting_invalid_references']),12)
    def test_no_native_subject_or_building_rewrite(self):
        paths=w.load(w.OUT/'EXPECTED_TEXT.json')
        self.assertFalse(any('/diplomacy/' in p or '/buildings/' in p or '/military' in p for p in paths))
    def test_current_country_and_government(self):
        cw=w.prior.core.cw
        n=cw.parse((w.ROOT/'common/country_definitions/1776_map2w_r4_passau.txt').read_text())[0]
        self.assertEqual(n.key,'PAS');self.assertEqual(n.one('capital'),'STATE_BAVARIA');self.assertEqual(n.one('religion'),'catholic')
        g=cw.parse((w.ROOT/'common/government_types/00_1776_map2w_r4_passau.txt').read_text())[0]
        self.assertEqual(g.one('male_ruler'),'"RULER_TITLE_PRINCE_BISHOP"')
    def test_historical_ruler(self):
        raw=(w.ROOT/'common/history/characters/pas - map2w_r4.txt').read_text()
        self.assertIn('age = 67',raw);self.assertIn('historical = yes',raw)
    def mutate(self,filename,change):
        original=Path.read_text;target=w.OUT/filename;data=w.load(target);change(data)
        def reader(p,*args,**kwargs):return json.dumps(data) if p==target else original(p,*args,**kwargs)
        with patch.object(Path,'read_text',autospec=True,side_effect=reader):
            with self.assertRaises(AssertionError):reg.approved_lot_dirs()
    def test_guard_rejects_wrong_owner(self):self.mutate('GEOMETRY.json',lambda g:g['assignments'][1].update(owner='PRU'))
    def test_guard_rejects_translation(self):self.mutate('GEOMETRY.json',lambda g:g['assignments'][1]['cells'][0].__setitem__(0,4408))
    def test_guard_rejects_duplicate_cell(self):self.mutate('GEOMETRY.json',lambda g:g['assignments'][1]['cells'].__setitem__(0,g['assignments'][1]['cells'][1]))
    def test_guard_rejects_extent_growth(self):self.mutate('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4400,902]))
    def test_guard_rejects_hub_movement(self):self.mutate('REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'].append({'state':'STATE_BAVARIA','field':'city'}))
    def test_guard_rejects_new_elector_alias(self):self.mutate('REGISTRY_MIGRATION.json',lambda m:m['new_members'].append('ELP'))
    def test_registry_current_layer(self):self.assertEqual(reg.approved_lot_dirs()[-1],w.OUT)
    def test_r3_not_reinstalled(self):self.assertNotIn(w.R4.parent/'R3',reg.approved_lot_dirs());self.assertNotIn('HLN',self.b['inventory']['countries'])
    def test_original_evidence_preserved(self):
        for p,h in self.b['source_hashes'].items():self.assertEqual(w.sha(w.ROOT/p),h)

if __name__=='__main__':unittest.main()
