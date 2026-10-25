"""Current cumulative contracts, separate from archived earlier-stage tests."""
import json,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import map2w_r4bc as w
import map2l_registry as reg

class FreisingRegensburg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=w.load(w.OUT/'BASELINE.json');cls.v=w.load(w.OUT/'VALIDATION.json');cls.a=w.load(w.OUT/'ALLOCATION.json')
        cls.g={s:w.load(w.OUT/s/'GEOMETRY.json') for s in ['R4B','R4C']};cls.m={s:w.load(w.OUT/s/'REGISTRY_MIGRATION.json') for s in cls.g};cls.bitmap=w.core.packed(w.ROOT/'map_data/provinces.png')
    def test_all_live_checks_pass(self):self.assertEqual(self.v['passed'],self.v['total'])
    def test_r4b_ready(self):self.assertEqual(w.load(w.OUT/'R4B/VALIDATION.json')['status'],'MAP2W_R4B_READY_FOR_SCOPED_RUNTIME_VALIDATION')
    def test_r4c_ready(self):self.assertEqual(w.load(w.OUT/'R4C/VALIDATION.json')['status'],'MAP2W_R4C_READY_FOR_SCOPED_RUNTIME_VALIDATION')
    def test_no_new_runtime_claim(self):self.assertFalse(self.v['engine_executed']);self.assertEqual(self.v['runtime_status'],'NOT_TESTED_NEW_FREISING_REGENSBURG_CHANGES')
    def test_passau_manual_attestation(self):
        r=w.load(w.pas.OUT/'RUNTIME_USER_ATTESTATION.json');self.assertEqual(r['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertEqual(r['successful_checks_reported'],8);self.assertFalse(r['automated_engine_test'] or r['historical_boundary_certification'] or r['future_Freising_Regensburg_changes_covered'])
    def test_passau_unchanged(self):
        original=w.core.packed(w.ROOT/self.b['bitmap_backup']);self.assertTrue(np.array_equal(original==0xEDBA00,self.bitmap==0xEDBA00));self.assertEqual(int((self.bitmap==0xEDBA00).sum()),40)
    def test_class_b_no_cadastral_claim(self):
        for g in self.g.values():self.assertEqual(g['classification'],'B_POLITICAL_APPROXIMATION');self.assertFalse(g['historical_cadastral_precision'])
    def test_only_bavaria_state_71(self):
        for m in self.m.values():self.assertEqual(m['replaced_regions'],['STATE_BAVARIA'])
    def test_freising_fourteen_cells(self):self.assertEqual(int((self.bitmap==0xEDBA10).sum()),14)
    def test_two_bishop_nuclei(self):
        self.assertEqual(int((self.bitmap==0xEDBA11).sum()),5);self.assertEqual(int((self.bitmap==0xEDBA12).sum()),9)
    def test_city_two_adjacent_cells_not_diocese(self):
        mask=np.isin(self.bitmap,[0xEDBA13,0xEDBA14]);self.assertEqual(int(mask.sum()),2);self.assertEqual([len(c) for c in w.core.components(mask)],[2])
    def test_no_core_parent(self):
        for g in self.g.values():self.assertTrue(all(not rgb.startswith('xED') for rgb in g['parents']))
    def test_only_three_new_countries(self):self.assertEqual(self.m['R4B']['new_members']+self.m['R4C']['new_members'],['FSI','RBI','RCI'])
    def test_city_free_bishops_not_free(self):self.assertEqual(self.m['R4B']['free_cities'],[]);self.assertEqual(self.m['R4C']['free_cities'],['RCI'])
    def test_nine_electors(self):
        from map2k_patch import ELECTORS
        self.assertEqual(len(ELECTORS),9);self.assertFalse(set(ELECTORS.values())&{'FSI','RBI','RCI'})
    def test_no_extent_or_hub_migration(self):
        for m in self.m.values():self.assertFalse(m['extent_added_cells'] or m['extent_removed_cells'] or m['region_reference_changes'])
    def test_573_registry_rgb(self):self.assertEqual(self.v['registered_RGBs'],573)
    def test_world_population_conserved(self):self.assertEqual((self.v['world_before'],self.v['world_after']),(835801255,835801255))
    def test_technical_population_no_census(self):self.assertIsNone(self.a['historical_population']);self.assertEqual(self.a['populations'],dict(FSI=4994,RBI=4993,RCI=713))
    def test_every_profile_preserved(self):
        for r in self.a['profiles']:self.assertEqual(sum(r['after'].values()),r['before'])
    def test_no_injected_industries_or_troops(self):self.assertFalse(any('/buildings/' in p or '/military' in p or '/diplomacy/' in p for p in w.load(w.OUT/'EXPECTED_TEXT.json')))
    def test_real_bishops_no_fake_city_biography(self):
        raw=(w.ROOT/'common/history/characters/1776_map2w_r4bc.txt').read_text();self.assertIn('1727.5.11',raw);self.assertIn('aor1776_sew_first',raw);self.assertNotIn('c:RCI',raw)
    def test_republic_separate_theocracies(self):
        for tag,law in [('FSI','law_theocracy'),('RBI','law_theocracy'),('RCI','law_presidential_republic')]:self.assertIn('law_type:'+law,(w.ROOT/f'common/history/countries/{tag.lower()} - map2w_r4bc.txt').read_text())
    def test_distinct_city_bishop_flags(self):
        raw=(w.ROOT/'common/flag_definitions/1776_map2w_r4bc.txt').read_text();self.assertIn('coa = aor1776_regensburg_city',raw);self.assertIn('coa = aor1776_regensburg_bishop',raw)
    def test_no_new_duplicate_or_invalid_references(self):self.assertEqual(self.v['preexisting_duplicate_RGBs'],44);self.assertEqual(len(self.v['preexisting_invalid_references']),12);self.assertFalse(self.v['new_errors'])
    def test_current_cumulative_tail_not_previous_last(self):self.assertEqual(reg.approved_lot_dirs()[-3:],[w.pas.OUT,w.OUT/'R4B',w.OUT/'R4C'])
    def test_older_tests_not_rewritten(self):
        for p,h in self.b['protected_tool_hashes'].items():self.assertEqual(w.pas.sha(w.ROOT/p),h)
    def mutate(self,sector,name,change):
        target=w.OUT/sector/name;data=w.load(target);change(data);original=Path.read_text
        def reader(p,*args,**kwargs):return json.dumps(data) if p==target else original(p,*args,**kwargs)
        with patch.object(Path,'read_text',autospec=True,side_effect=reader):
            with self.assertRaises(AssertionError):reg.approved_lot_dirs()
    def test_guard_rejects_freising_translation(self):self.mutate('R4B','GEOMETRY.json',lambda g:g['assignments'][1]['cells'][0].__setitem__(0,4350))
    def test_guard_rejects_regensburg_city_to_bishop(self):self.mutate('R4C','GEOMETRY.json',lambda g:g['assignments'][4].update(owner='RBI'))
    def test_guard_rejects_freising_to_bavaria(self):self.mutate('R4B','GEOMETRY.json',lambda g:g['assignments'][1].update(owner='BAV'))
    def test_guard_rejects_protected_parent(self):self.mutate('R4C','GEOMETRY.json',lambda g:g['parents'].append('xEDBA00'))
    def test_guard_rejects_extent_growth(self):self.mutate('R4B','REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4355,905]))
    def test_guard_rejects_extra_country(self):self.mutate('R4C','REGISTRY_MIGRATION.json',lambda m:m['new_members'].append('RGA'))
    def test_guard_rejects_electoral_or_free_bishop(self):self.mutate('R4B','REGISTRY_MIGRATION.json',lambda m:m['free_cities'].append('FSI'))
    def test_guard_rejects_duplicate_cell(self):self.mutate('R4C','GEOMETRY.json',lambda g:g['assignments'][1]['cells'].__setitem__(0,g['assignments'][1]['cells'][1]))
    def test_guard_rejects_edited_retained_parent(self):self.mutate('R4B','GEOMETRY.json',lambda g:g['assignments'][0]['cells'][0].__setitem__(0,4359))
    def test_guard_rejects_hub_rebinding(self):self.mutate('R4C','REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'].append({'state':'STATE_BAVARIA','field':'farm'}))

if __name__=='__main__':unittest.main()
