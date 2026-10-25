"""Island identification and bounded receipt guards; no game execution."""
import copy
import unittest
import serg_sc4_piombino as lot


class PiombinoEvidence(unittest.TestCase):
    def test_diagonal_contact_does_not_merge_island_and_mainland(self):
        parts=lot.components([0,1],[0,1])
        self.assertEqual([p['cells'] for p in parts],[1,1])

    def test_shared_color_does_not_fill_a_water_gap(self):
        parts=lot.components([0,1,4,5],[0,0,0,0])
        self.assertEqual([p['cells'] for p in parts],[2,2])
        self.assertEqual(sum(p['cells'] for p in parts),4)
        self.assertNotIn([2,0],[q for p in parts for q in p['pixels']])

    def native(self):return lot.load(lot.OUT/'NATIVE_INVENTORY.json')['provinces']

    def test_whole_219_cell_province_cannot_be_treated_as_elba(self):
        rows=self.native();r=next(r for r in rows if r['rgb']=='x6A7662')
        all_points=[p for c in r['components'] for p in c['pixels']]
        r['components']=[dict(cells=219,bounds=r['bounds'],centroid=r['centroid'],pixels=all_points)]
        with self.assertRaises(AssertionError):lot.elba_component(rows)

    def test_rejects_duplicate_or_changed_island_cells(self):
        for mode in ['duplicate','changed_count']:
            rows=self.native();r=next(r for r in rows if r['rgb']=='x6A7662');c=next(c for c in r['components'] if c['cells']==54)
            if mode=='duplicate':c['pixels'][-1]=c['pixels'][0]
            else:c['cells']=55
            with self.assertRaises(AssertionError):lot.elba_component(rows)

    def test_reading_island_does_not_mutate_inventory(self):
        rows=self.native();old=copy.deepcopy(rows);c=lot.elba_component(rows);c['pixels'].pop()
        self.assertEqual(rows,old)

    def test_limited_gen_receipt_cannot_close_piombino_or_liguria(self):
        state=lot.load(lot.OUT/'BASELINE.json')['roadmap']
        t=next(t for t in state['tasks'] if t['id']=='SC4-LIGURIAN-FIEFS')
        self.assertTrue(lot.rm.partial_runtime_evidence(t))
        self.assertEqual([s['id'] for s in t['installed_sub_lots']],['LF-GEN-ADM-PM'])
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
        p=next(t for t in state['tasks'] if t['id']==lot.TASK)
        p['status']='BLOCKED'
        self.assertFalse(lot.rm.terminal_evidence(p,state))
        self.assertEqual(lot.rm.progress(state)['next_task'],'SC4-MASSA-CARRARA')
        self.assertIsNone(p['runtime_validation']['attestation'])


if __name__=='__main__':unittest.main()
