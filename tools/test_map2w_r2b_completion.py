"""Scoped current-state and negative contracts, not Victoria 3 engine tests."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import map2w_r2b_completion as w
import map2l_registry as reg

class HesseNassauCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=w.load('GEOMETRY.json');cls.m=w.load('REGISTRY_MIGRATION.json');cls.v=w.load('VALIDATION_R2B.json');cls.b=w.load('BASELINE.json')
    def test_static_checks(self):self.assertEqual(self.v['passed'],self.v['total'])
    def test_scoped_status(self):self.assertEqual(self.v['status'],'MAP2W_R2B_READY_FOR_SCOPED_RUNTIME_VALIDATION')
    def test_no_runtime_claim(self):self.assertEqual(self.v['runtime_status'],'NOT_TESTED_R2B')
    def test_exact_receivers(self):
        totals={tag:sum(r['pixels'] for r in self.g['assignments'] if r['owner']==tag and r['owner']!=r['previous_owner']) for tag in ['NSB','NOU','NWB','NAS','FUL']}
        self.assertEqual(totals,dict(NSB=15,NOU=8,NWB=2,NAS=11,FUL=9))
    def test_saar_distinct_not_merged_usingen(self):self.assertEqual(self.m['new_members'],['NSB'])
    def test_exact_new_rgb(self):self.assertEqual([r['rgb'] for r in self.g['new_provinces']],['xEDB8'+format(i,'02X') for i in range(13)])
    def test_no_previous_new_rgb_parent(self):self.assertTrue(all(not p.startswith('xED') for p in self.g['parents']))
    def test_only_three_regions(self):self.assertEqual(self.m['replaced_regions'],['STATE_HESSE','STATE_RHINELAND','STATE_SAXONY'])
    def test_no_new_electors_or_free_cities(self):self.assertFalse(self.m['free_cities'])
    def test_nine_electors_retained(self):
        from map2k_patch import ELECTORS
        self.assertEqual(len(ELECTORS),9);self.assertNotIn('NSB',ELECTORS.values())
    def test_imperial_extent_frozen(self):self.assertFalse(self.m['extent_added_cells'] or self.m['extent_removed_cells'])
    def test_only_one_new_country(self):
        result=reg.expected_country_definitions(self.b['inventory']['countries'],[self.m]);self.assertEqual(set(result)-set(self.b['inventory']['countries']),{'NSB'})
        self.assertTrue(all(result[k]==s for k,s in self.b['inventory']['countries'].items()))
    def test_no_historical_population_invention(self):self.assertIsNone(w.load('ALLOCATION.json')['historical_population'])
    def test_world_conserved(self):self.assertEqual(self.v['world_before'],835801255);self.assertEqual(self.v['world_after'],835801255)
    def test_16814_conserved_saar_population(self):self.assertEqual(self.v['country_populations']['NSB'],16814)
    def test_prior_general_attestation_not_extrapolated(self):
        receipt=json.loads((w.a.r1.OUT/'RUNTIME_USER_ATTESTATION_R2B.json').read_text());self.assertFalse(receipt['future_R2B_changes_covered']);self.assertIsNone(receipt['simulation_duration'])
    def test_44_old_duplicates(self):self.assertEqual(self.v['preexisting_duplicate_RGBs'],44)
    def test_12_old_references_no_new_errors(self):self.assertEqual(len(self.v['preexisting_invalid_references']),12);self.assertFalse(self.v['new_errors'])
    def test_flag_uses_existing_dynastic_arms(self):self.assertIn('coa = aor1776_map2w_r2_nassau',(w.ROOT/'common/flag_definitions/1776_map2w_r2b_saarbruecken.txt').read_text())
    def test_nsbs_princely_title_is_explicit(self):
        n=w.core.cw.parse((w.ROOT/'common/government_types/00_1776_map2w_r2b_saarbruecken.txt').read_text())[0]
        self.assertEqual(n.one('male_ruler'),'"RULER_TITLE_PRINCE"');self.assertEqual(n.children('possible')[0].children()[0].key,'c:NSB')
    def test_localisations_match(self):
        import re
        sets=[set(re.findall(r'^\s*([A-Za-z0-9_.-]+):0', (w.ROOT/f'localization/{lang}/1776_map2w_r2b_l_{lang}.yml').read_text(encoding='utf-8-sig'),re.M)) for lang in ['french','english']]
        self.assertEqual(sets[0],sets[1]);self.assertEqual(len(sets[0]),6)
    def mutate_geometry(self,change):
        original=Path.read_text;data=copy.deepcopy(self.g);change(data)
        def reader(p,*args,**kwargs):return json.dumps(data) if p==w.OUT/'GEOMETRY.json' else original(p,*args,**kwargs)
        with patch.object(Path,'read_text',autospec=True,side_effect=reader):
            with self.assertRaises(AssertionError):reg.approved_lot_dirs()
    def test_guard_rejects_new_prussian_saar(self):self.mutate_geometry(lambda g:g['assignments'][1].update(owner='PRU'))
    def test_guard_rejects_out_of_scope_cell(self):self.mutate_geometry(lambda g:g['assignments'][1]['cells'].__setitem__(0,[4345,830]))
    def test_guard_rejects_prior_core_parent(self):self.mutate_geometry(lambda g:g['parents'].append('xEDB701'))
    def test_no_unsupported_native_union(self):self.assertFalse(any('/diplomacy/' in p for p in w.load('EXPECTED_TEXT.json')))
    def test_registry_guard_accepts_current_layer(self):
        layers=reg.approved_lot_dirs();self.assertIn(w.OUT,layers)
        passau=w.OUT.parent/'R4/POLITICAL_REPRESENTATION/PASSAU'
        expected=[passau] if (passau/'REGISTRY_MIGRATION.json').exists() else []
        self.assertEqual(layers[layers.index(w.OUT)+1:],expected)

if __name__=='__main__':unittest.main()
