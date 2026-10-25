"""Scoped negative guards and player-handoff contracts; no game/Git writes."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc1_salzburg as lot
import serg_closure_roadmap as rm
import map2l_registry as reg

class SalzburgContracts(unittest.TestCase):
    def mutate(self,name,change):
        target=lot.OUT/name;data=lot.load(target);change(data);original=Path.read_text
        def reader(p,*args,**kwargs):return json.dumps(data) if p==target else original(p,*args,**kwargs)
        with patch.object(Path,'read_text',autospec=True,side_effect=reader):
            with self.assertRaises(AssertionError):reg.approved_lot_dirs()

    def test_reject_translated_nucleus(self):
        self.mutate('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='SLZ')['cells'][0].__setitem__(0,4384))
    def test_reject_berchtesgaden_extension(self):
        self.mutate('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='SLZ')['cells'].append([4385,930]))
    def test_reject_protected_parent(self):
        self.mutate('GEOMETRY.json',lambda g:g.update(parents=['xEDBA00']))
    def test_reject_free_city_status(self):
        self.mutate('REGISTRY_MIGRATION.json',lambda m:m.update(free_cities=['SLZ']))
    def test_reject_added_imperial_extent(self):
        self.mutate('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4385,930]))
    def test_reject_changed_ancestral_owner(self):
        self.mutate('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']=='x6EA29B').update(beneficiary='SLZ'))
    def test_reject_cadastral_claim(self):
        self.mutate('GEOMETRY.json',lambda g:g.update(historical_cadastral_precision=True))
    def test_exact_cumulative_tail(self):
        self.assertEqual(reg.approved_lot_dirs()[-4:],[lot.prior.pas.OUT,lot.prior.OUT/'R4B',lot.prior.OUT/'R4C',lot.OUT])
    def ready_state(self):
        state=copy.deepcopy(rm.load_json(rm.OUT/'INITIAL_STATE.json'))
        t=next(t for t in state['tasks'] if t['id']=='SC1-SALZBURG')
        t['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        state['runtime_validation_hold']={'task_id':'SC1-SALZBURG'}
        return state,t
    def test_ready_delivery_has_no_progress_credit(self):
        state,t=self.ready_state();p=rm.progress(state)
        self.assertEqual((p['earned_weight'],p['total_weight'],p['percent']),(60,235,'25.53'))
        self.assertFalse(rm.terminal_evidence(t,state))
    def test_next_action_stays_with_player(self):
        state,t=self.ready_state();p=rm.progress(state)
        self.assertEqual(p['next_task'],'SC1-SALZBURG')
        self.assertIn('SC1-SALZBURG',p['awaiting_runtime'])
        self.assertTrue(all(t['status']=='NOT_STARTED' for t in state['tasks'] if t['id'] in ['SC1-TRENTO','SC1-BRIXEN','SC2-BOHEMIA']))
    def test_hold_does_not_invent_manual_receipt(self):
        state,t=self.ready_state()
        self.assertIsNone(t['runtime_validation']['attestation'])
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(rm.terminal_evidence(t,state))
    def test_without_hold_priority_candidate_is_bohemia(self):
        state,t=self.ready_state();del state['runtime_validation_hold']
        self.assertEqual(rm.progress(state)['next_task'],'SC2-BOHEMIA')

if __name__=='__main__':unittest.main()
