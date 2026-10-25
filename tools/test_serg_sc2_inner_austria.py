"""Reject scope leaks and unsupported acceptance of the two regional additions."""
import copy
import unittest
import serg_sc2_inner_austria as lot
import serg_closure_roadmap as rm


class InnerAustriaContracts(unittest.TestCase):
    def reject(self, old, new):
        for sid in lot.SIDS:
            with self.subTest(region=sid), self.assertRaises(AssertionError):
                lot.admin_contract(lot.expected_admin(sid).replace(old,new,1),sid)

    def test_independent_regional_contracts(self):
        for sid in lot.SIDS:
            self.assertTrue(lot.admin_contract(lot.expected_admin(sid),sid))

    def test_reject_extra_level(self):
        self.reject('levels = 1','levels = 2')

    def test_reject_foreign_owner(self):
        self.reject('country = "c:AUS"','country = "c:VEN"')

    def test_reject_foreign_selector(self):
        self.reject('region_state:AUS','region_state:PRU')

    def test_reject_other_region(self):
        for sid in lot.SIDS:
            with self.assertRaises(AssertionError):
                lot.admin_contract(lot.expected_admin(sid).replace('s:'+sid,'s:STATE_CROATIA'),sid)

    def test_reject_swapped_regional_files(self):
        with self.assertRaises(AssertionError):
            lot.admin_contract(lot.expected_admin('STATE_STYRIA'),'STATE_SLOVENIA')

    def test_reject_incompatible_professional_pm(self):
        self.reject('pm_hereditary_bureaucrats','pm_professional_bureaucrats')

    def test_reject_future_reporting_pm(self):
        self.reject('pm_1776_no_organized_data_reporting','pm_1776_administrative_data_reporting')

    def test_reject_extra_pop_effect(self):
        self.reject('reserves = 1','reserves = 1\n create_pop = { culture = south_german size = 1000 }')

    def test_reject_other_building(self):
        self.reject('building_government_administration','building_barracks')

    def test_reject_missing_public_ownership(self):
        self.reject('add_ownership','unused_ownership')

    def baseline(self):
        return copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap'])

    def ready(self):
        state=self.baseline()
        task=next(t for t in state['tasks'] if t['id']==lot.TASK)
        task['status']='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
        state['runtime_validation_hold']={'task_id':lot.TASK}
        return state,task

    def test_initial_priority_and_78_points(self):
        p=rm.progress(self.baseline())
        self.assertEqual((p['earned_weight'],p['total_weight'],p['percent'],p['next_task']),(78,235,'33.19',lot.TASK))

    def test_new_installation_no_credit_or_receipt(self):
        state,task=self.ready()
        self.assertEqual(rm.progress(state)['earned_weight'],78)
        self.assertIsNone(task['runtime_validation']['attestation'])
        self.assertFalse(rm.terminal_evidence(task,state))

    def test_runtime_hold_stops_next_implementation(self):
        state,_=self.ready()
        self.assertEqual(rm.progress(state)['next_task'],lot.TASK)
        state.pop('runtime_validation_hold')
        self.assertEqual(rm.progress(state)['next_task'],'SC2-ANTERIOR-AUSTRIA')
        self.assertEqual(next(t for t in state['tasks'] if t['id']=='SC2-ANTERIOR-AUSTRIA')['status'],'NOT_STARTED')

    def test_no_fake_terminal_pass(self):
        state,task=self.ready()
        task['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(rm.terminal_evidence(task,state))
        self.assertEqual(rm.progress(state)['earned_weight'],78)

    def test_innviertel_block_not_retention_approval(self):
        state=self.baseline()
        task=next(t for t in state['tasks'] if t['id']=='SC2-AUSTRIA')
        self.assertEqual(task['status'],'BLOCKED')
        ack=lot.load(rm.file_ref(task['user_acknowledgment']))
        self.assertFalse(ack['retention_approved'])
        self.assertEqual(ack['points_awarded'],0)
        self.assertFalse(ack['runtime_user_validation'])

    def test_no_automatic_neighbor_or_teschen_acceptance(self):
        state=self.baseline()
        self.assertEqual(next(t for t in state['tasks'] if t['id']=='SC2-TESCHEN')['status'],'NOT_STARTED')
        self.assertEqual(next(t for t in state['tasks'] if t['id']=='SC2-AUSTRIAN-SILESIA')['status'],'NOT_APPLICABLE_VERIFIED')
        self.assertFalse(rm.qualifications(state)['SC2-MAP2A-VALIDATION'])

    def maritime_before(self):
        record=lot.load(lot.OUT/'MARITIME_CLEANUP.json')['files'][0]
        return (lot.OUT/record['before_file']).read_bytes().decode('utf8')

    def test_maritime_cleanup_exact_scoped_candidate(self):
        before=self.maritime_before()
        candidate,nodes=lot.inland_cleanup(before)
        self.assertEqual(len(nodes),2)
        self.assertTrue(lot.maritime_contract(before,candidate))
        region=lot.shared.core.region(candidate,'STATE_SLOVENIA','AUS')
        self.assertEqual([lot.shared.core.cw.scalar(n.one('building')) for n in region.children('create_building')],['building_railway','building_trade_center'])

    def test_maritime_reject_altered_concurrent_owner(self):
        before=self.maritime_before()
        _,nodes=lot.inland_cleanup(before)
        node=next(n for n in nodes if 'building_port' in lot.shared.core.qa.signature(n))
        changed=before[:node.start]+before[node.start:node.end].replace('c:AUS','c:VEN')+before[node.end:]
        with self.assertRaises(AssertionError):
            lot.inland_cleanup(changed)

    def test_maritime_reject_outside_region_edit(self):
        before=self.maritime_before();candidate,_=lot.inland_cleanup(before)
        with self.assertRaises(AssertionError):
            lot.maritime_contract(before,candidate.replace('s:STATE_DALMATIA','s:STATE_DALMATIA_CHANGED',1))

    def test_maritime_reject_second_cleanup(self):
        candidate,_=lot.inland_cleanup(self.maritime_before())
        with self.assertRaises(AssertionError):
            lot.inland_cleanup(candidate)


if __name__=='__main__':
    unittest.main()
