"""Reject unreviewed expansion and fictitious closure of the coastal core."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc4_massa_carrara as lot

class MassaCarraraContracts(unittest.TestCase):
    def reject(self,name,mutate):
        p=lot.OUT/name;data=lot.load(p);mutate(data);reader=Path.read_text
        def read(fp,*a,**kw):return json.dumps(data) if fp==p else reader(fp,*a,**kw)
        with patch.object(Path,'read_text',autospec=True,side_effect=read):
            with self.assertRaises(AssertionError):lot.reg.approved_lot_dirs()
    def test_reject_occupation_of_lucca(self):
        self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='MCA')['cells'].append([4328,1033]))
    def test_reject_shifted_coastal_core(self):
        self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='MCA')['cells'][0].__setitem__(0,4324))
    def test_reject_whole_parent_transfer(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']==lot.PARENT).update(beneficiary='MCA'))
    def test_reject_undeclared_imperial_extent(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4328,1033]))
    def test_reject_free_city_status(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m.update(free_cities=['MCA']))
    def test_reject_cadastral_certification(self):
        self.reject('GEOMETRY.json',lambda g:g.update(historical_cadastral_precision=True))
    def test_reject_rebinding_parma_hub(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'].append(dict(state=lot.SID,field='city',before='x0B3B43',after=lot.RGB)))
    def test_current_chain_retains_salzburg_before_massa(self):
        self.assertEqual(lot.reg.approved_lot_dirs()[-2:],[lot.rm.OUT/'SC1-SALZBURG',lot.OUT])
    def test_no_human_receipt_no_points_even_after_static_success(self):
        state=copy.deepcopy(lot.load(lot.OUT/'STATE_AFTER_PIOMBINO_ACK.json'))
        task=next(t for t in state['tasks'] if t['id']==lot.TASK)
        task['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
        task['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(task,state))
        self.assertEqual(lot.rm.progress(state)['earned_weight'],82)
    def test_piombino_acknowledgment_is_not_a_runtime_receipt(self):
        ack=lot.load(lot.prior.OUT/'USER_ACKNOWLEDGMENT_2026_10_23.json')
        self.assertFalse(ack['runtime_validation_granted'])
        self.assertFalse(ack['retention_approved'])
        self.assertEqual(ack['points_awarded'],0)
    def test_partial_installation_hold_preserves_regional_block_and_credit(self):
        state=copy.deepcopy(lot.load(lot.OUT/'STATE_AFTER_PIOMBINO_ACK.json'))
        task=next(t for t in state['tasks'] if t['id']==lot.TASK)
        task.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
        self.assertEqual(lot.rm.progress(state)['next_task'],'SC1-TRENTO')
        state['runtime_validation_hold']={'task_id':lot.TASK}
        p=lot.rm.progress(state)
        self.assertEqual(p['next_task'],lot.TASK)
        self.assertEqual((p['earned_weight'],p['percent']),(82,'34.89'))
        self.assertEqual(task['status'],'BLOCKED')

if __name__=='__main__':unittest.main()
