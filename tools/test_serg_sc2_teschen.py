"""Exact province rights, negative widening cases and independently scoped receipts."""
import copy, json, unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc2_teschen as a

class TeschenContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=a.load(a.OUT/'BASELINE.json')
        cls.m=a.load(a.OUT/'REGISTRY_MIGRATION.json')
        cls.rows=a.load(a.reg.active_registry_path())
        cls.state=a.load(a.rm.OUT/'ROADMAP_STATE.json')

    def corrupt_migration(self,mutate):
        fake=copy.deepcopy(self.m);mutate(fake);original=Path.read_text
        def read(path,*args,**kwargs):
            return json.dumps(fake) if path==a.OUT/'REGISTRY_MIGRATION.json' else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            with self.assertRaises(AssertionError):a.reg.approved_territorial_migrations()

    def test_one_new_title_preserves_all_predecessors(self):
        self.assertEqual(len(self.rows),581)
        self.assertEqual([r for r in self.rows if r['rgb']!=a.RGB],self.b['registry'])
        self.assertEqual([(r['state'],r['beneficiary']) for r in self.rows if r['rgb']==a.RGB],[(a.SID,'AUS')])

    def test_other_galician_provinces_excluded(self):
        self.assertEqual([r['rgb'] for r in self.rows if r['state']==a.SID],[a.RGB])
        self.assertEqual(a.reg.provincial_membership_overrides(),{(a.RGB,a.SID,'AUS')})
        import map2k_imperial_system as compiler
        self.assertNotIn(a.SID,compiler.REGIONS)
        self.assertNotIn(('x906060',a.SID,'AUS'),a.reg.provincial_membership_overrides())
        self.assertNotIn((a.RGB,a.SID,'GAL'),a.reg.provincial_membership_overrides())

    def test_wrong_province_rejected(self):self.corrupt_migration(lambda m:m['updated'][0].update(rgb='x906060'))
    def test_wrong_beneficiary_rejected(self):self.corrupt_migration(lambda m:m['updated'][0].update(beneficiary='GAL'))
    def test_whole_region_addition_rejected(self):self.corrupt_migration(lambda m:m['updated'].append(dict(rgb='x906060',state=a.SID,beneficiary='AUS')))
    def test_extra_override_rejected(self):self.corrupt_migration(lambda m:m['province_membership_overrides'].append(dict(rgb='x906060',state=a.SID,owner='AUS')))
    def test_coordinate_change_rejected(self):self.corrupt_migration(lambda m:m['extent_added_cells'].__setitem__(0,[4520,861]))
    def test_duplicate_cell_rejected(self):self.corrupt_migration(lambda m:m['extent_added_cells'].__setitem__(0,m['extent_added_cells'][1]))
    def test_new_member_rejected(self):self.corrupt_migration(lambda m:m.update(new_members=['GAL']))
    def test_fictitious_ownership_transfer_rejected(self):self.corrupt_migration(lambda m:m.update(ownership_updated=m['updated']))

    def test_physical_and_demographic_histories_unchanged(self):
        for p in ['map_data/provinces.png','common/history/states/00_states.txt','common/history/pops/00_west_europe.txt','common/history/pops/01_south_europe.txt']:
            self.assertEqual(a.sha(a.ROOT/p),self.b['hashes'][p],p)
        self.assertEqual(self.m['new_provinces'],[])
        self.assertEqual(a.reg.ownership_rows(self.m,'previous'),a.reg.ownership_rows(self.m,'updated'))

    def test_extent_is_exact_179_existing_cells(self):
        bitmap=a.core.packed(a.ROOT/'map_data/provinces.png');ys,xs=a.np.where(bitmap==int(a.RGB[1:],16))
        self.assertEqual(sorted([[int(x),int(y)] for x,y in zip(xs,ys)]),self.m['extent_added_cells'])
        self.assertEqual(len(xs),179)

    def test_restitution_cannot_take_neighbor_galicia(self):
        text=(a.ROOT/'common/scripted_effects/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
        self.assertIn('country = c:AUS provinces = { '+a.RGB+' }',text)
        self.assertNotIn('p:x906060.state',text)
        self.assertNotIn('p:x1161E0.state',text)

    def test_localization_additions_do_not_replace_old_keys(self):
        expected=a.load(a.OUT/'EXPECTED_TEXT.json');before=a.load(a.OUT/'TEXT_BEFORE.json')
        for p,new in expected.items():
            if p.endswith('.yml'):
                oldlines=before[p].splitlines();newlines=new.splitlines()
                self.assertEqual([l for l in newlines if a.RGB not in l],oldlines)
                self.assertEqual(sum(a.RGB in l for l in newlines),1)

    def test_real_ortenburg_attestation_does_not_close_region(self):
        task=next(t for t in self.state['tasks'] if t['id']=='SC1-ORTENBURG')
        self.assertTrue(a.rm.partial_runtime_evidence(task));self.assertEqual(task['status'],'BLOCKED')
        receipt=a.load(a.ROOT/task['runtime_validation']['attestation'])
        self.assertEqual(receipt['sub_lot_ids'],['OR-I-CORE']);self.assertEqual(receipt['simulation_months'],1)
        self.assertIsNone(receipt['actual_test_date']);self.assertEqual(receipt['points_awarded'],0)

    def test_teschen_has_no_human_receipt_or_regional_credit(self):
        task=next(t for t in self.state['tasks'] if t['id']==a.TASK)
        self.assertEqual(task['status'],'BLOCKED');self.assertEqual(task['installed_delivery_status'],'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
        self.assertEqual([l['id'] for l in task['installed_sub_lots']],['TE-R-CORE'])
        self.assertIsNone(task['runtime_validation']['attestation']);self.assertFalse(list(a.OUT.glob('RUNTIME_USER_ATTESTATION*')))
        self.assertGreaterEqual(len(task['remaining_territorial_obligations']),2)

    def test_progress_scope_and_next_candidate_are_bounded(self):
        p=a.rm.progress(self.state);self.assertEqual((p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['total_tasks']),(82,235,24,81))
        self.assertEqual(p['next_task'],a.TASK)
        candidate=self.state['runtime_validation_hold']['next_implementation_candidate']
        self.assertEqual(candidate,'SC3-HOLSTEIN')
        self.assertEqual(next(t['status'] for t in self.state['tasks'] if t['id']==candidate),'NOT_STARTED')

    def test_canonical_proofs_pass(self):self.assertEqual(a.rm.check()['status'],'PASS')

if __name__=='__main__':unittest.main()
