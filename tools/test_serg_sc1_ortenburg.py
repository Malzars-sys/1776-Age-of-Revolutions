"""Exact Ortenburg installation, negative scope and independently bounded receipts."""
import copy, json, unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc1_ortenburg as a

class OrtenburgContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=a.load(a.OUT/'BASELINE.json');cls.g=a.load(a.OUT/'GEOMETRY.json')
        cls.old=a.core.packed(a.OUT/'provinces_before.png');cls.now=a.core.packed(a.ROOT/'map_data/provinces.png')
        cls.state=a.load(a.rm.OUT/'ROADMAP_STATE.json')
    def test_only_four_exact_pixels_change(self):
        ys,xs=a.np.where(self.old!=self.now);self.assertEqual(sorted([[int(x),int(y)] for x,y in zip(xs,ys)]),a.CELLS)
    def test_no_unapproved_parent_or_neighbor_transfer(self):
        for x,y in a.CELLS:self.assertEqual(int(self.old[y,x]),int(a.PARENT[1:],16));self.assertEqual(int(self.now[y,x]),int(a.RGB[1:],16))
        for rgb in ['xEDBA00','xEDBA11','xEDBA12','xEDBA13','xEDBA14','xEDBB00','xEDBF00','xEDC000']:
            self.assertTrue(a.np.array_equal(self.old==int(rgb[1:],16),self.now==int(rgb[1:],16)),rgb)
    def test_donor_not_disconnected(self):
        import serg_sc4_piombino as physical
        y,x=a.np.where(self.now==int(a.PARENT[1:],16));self.assertEqual(len(x),272);self.assertEqual(len(physical.components(x,y)),1)
    def test_compact_orthogonal_child(self):
        import serg_sc4_piombino as physical
        y,x=a.np.where(self.now==int(a.RGB[1:],16));self.assertEqual(len(x),4);self.assertEqual(len(physical.components(x,y)),1)
    def test_only_reviewed_new_registry_title(self):
        rows=a.load(a.reg.active_registry_path());self.assertEqual(len(rows),580)
        self.assertEqual([r for r in rows if r['rgb']!=a.RGB],self.b['registry'])
        self.assertEqual(next(r['beneficiary'] for r in rows if r['rgb']==a.RGB),'ORT')
    def test_tail_guard_rejects_wrong_country_or_coordinate(self):
        m=a.load(a.OUT/'REGISTRY_MIGRATION.json');self.assertEqual(m,a.reg.approved_territorial_migrations()[-1]);self.assertEqual(m['new_members'],['ORT']);self.assertFalse(m['free_cities'])
        original=Path.read_text
        bad_holder=copy.deepcopy(m);next(r for r in bad_holder['updated'] if r['rgb']==a.RGB)['beneficiary']='BAV'
        bad_geometry=copy.deepcopy(self.g);next(r for r in bad_geometry['assignments'] if r['owner']=='ORT')['cells'][0]=[4391,901]
        for target,fake in [(a.OUT/'REGISTRY_MIGRATION.json',bad_holder),(a.OUT/'GEOMETRY.json',bad_geometry)]:
            def guarded(path,*args,**kwargs):
                return json.dumps(fake) if path==target else original(path,*args,**kwargs)
            with patch.object(Path,'read_text',guarded):
                with self.assertRaises(AssertionError):a.reg.approved_territorial_migrations()
    def test_demographic_transfer_is_confession_preserving(self):
        d=a.load(a.OUT/'DEMOGRAPHY.json');self.assertEqual(d['selected_donor_before']-d['selected_donor_after'],1000);self.assertEqual(d['religion'],'protestant');self.assertEqual(d['world_delta'],0)
    def test_ruler_is_karl_three_not_son(self):
        text=(a.ROOT/'common/history/characters/1776_sc1_ortenburg.txt').read_text(encoding='utf8');self.assertIn('aor1776_ort_karl',text);self.assertIn('age = 60',text);self.assertNotIn('birth_date',text);self.assertNotIn('Albrecht',text)
    def test_no_new_military_or_diplomatic_pact_file(self):
        self.assertFalse(any(p.startswith(('common/history/military','common/history/diplomacy','common/history/treaties')) for p in a.load(a.OUT/'EXPECTED_TEXT.json')))
    def test_no_macro_bavarian_technology_copy(self):
        self.assertEqual(len(a.TECHS),9);self.assertFalse(set(a.TECHS)&{'centralization','coke_smelting','alloysworking','standardized_field_artillery','permanent_engineer_services','scientific_fortification_siegecraft'})
    def test_live_technology_validator_has_no_capability_failure(self):
        s=a.load(a.OUT/'STARTING_TECH_CHECK.json');self.assertEqual(s['technologies'],sorted(a.TECHS));self.assertFalse([r for r in s['findings'] if r['priority'] in ['P0','P1']])
    def test_ratisbonne_receipt_bounded_and_real_quote(self):
        r=a.load(a.previous.OUT/'RUNTIME_USER_ATTESTATION_2026_10_25.json');self.assertEqual(r['sub_lot_ids'],['RG-D-CITY']);self.assertEqual(r['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertFalse(r['regional_closure_approved']);self.assertEqual(r['points_awarded'],0);self.assertIsNone(r['actual_test_date']);self.assertFalse(r['extra_observations_invented'])
    def test_previous_region_remains_blocked(self):
        t=next(t for t in self.state['tasks'] if t['id']==a.previous.TASK);self.assertEqual(t['status'],'BLOCKED');self.assertEqual(t['installed_delivery_status'],'PASS_RUNTIME_USER_VALIDATED')
    def test_ortenburg_not_human_validated(self):
        self.assertFalse(list(a.OUT.glob('RUNTIME_USER_ATTESTATION*')));self.assertIsNone(a.load(a.OUT/'FILES_MODIFIED.json')['human_validation'])
    def test_progress_and_no_second_task(self):
        p=a.rm.progress(self.state);self.assertEqual((p['earned_weight'],p['total_weight'],p['qualified_tasks']),(82,235,24));self.assertEqual(p['next_task'],a.TASK)
        candidate=self.state['runtime_validation_hold']['next_implementation_candidate'];self.assertNotEqual(candidate,a.TASK);self.assertEqual(next(t['status'] for t in self.state['tasks'] if t['id']==candidate),'NOT_STARTED')
    def test_canonical_validator_passes(self):self.assertEqual(a.rm.check()['status'],'PASS')

if __name__=='__main__':unittest.main()
