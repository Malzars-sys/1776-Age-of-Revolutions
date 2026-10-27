"""Campaign preserves points, scope, old receipts and truthful missing controls."""
import ast, copy, json, unittest
from pathlib import Path
import serg_closure_campaign_20261026 as a

class ClosureCampaignContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=a.load(a.OUT/'BASELINE.json');cls.s=a.load(a.rm.OUT/'ROADMAP_STATE.json')
        cls.audit=a.load(a.OUT/'INSTALLED_VALIDATION_AUDIT.json')
        cls.obs=a.load(a.OUT/'TESCHEN_USER_OBSERVATION.json')

    def test_scope_weights_and_qualifications_unchanged(self):
        p=a.rm.progress(self.s)
        self.assertEqual((p['earned_weight'],p['total_weight'],p['qualified_tasks'],p['total_tasks']),(82,235,24,81))
        self.assertEqual([(t['id'],t['weight']) for t in self.s['tasks']],[(t['id'],t['weight']) for t in self.b['roadmap']['tasks']])
        self.assertEqual(a.rm.qualifications(self.s),a.rm.qualifications(self.b['roadmap']))

    def test_all_eight_installations_audited_without_automatic_credit(self):
        self.assertEqual([r['task_id'] for r in self.audit['rows']],a.TASKS)
        self.assertEqual(self.audit['total_potential_points'],11)
        self.assertEqual(self.audit['qualified_new_points'],0)
        self.assertFalse(any(r['can_close'] for r in self.audit['rows']))

    def test_two_luxembourg_scope_differences_not_hidden(self):
        self.assertEqual((self.audit['passed'],self.audit['total']),(133,135))
        self.assertEqual(self.audit['status'],'FAIL')
        self.assertEqual({c['task_id'] for c in self.audit['failed']},{'SC2-LUXEMBOURG-VALIDATION'})
        reconciliation=a.load(a.OUT/'LUXEMBOURG_SCOPE_RECONCILIATION.json')
        self.assertFalse(reconciliation['restoration_performed'])
        self.assertEqual(reconciliation['current_admin_declarations'],dict(BEO_STATE_WALLONIA=0,BEO_STATE_FLANDERS=3))
        for row in reconciliation['calibration_rows']:
            self.assertEqual(int(row['Final_Target_Level']),0 if row['State_ID']=='STATE_WALLONIA' else 3)

    def test_old_runtime_receipts_not_edited(self):
        for rel,h in self.b['prior_proofs'].items():
            if 'ATTESTATION' in Path(rel).name or 'RUNTIME_USER' in Path(rel).name:
                self.assertEqual(a.sha(a.ROOT/rel),h,rel)

    def test_human_observation_preserves_unknowns(self):
        self.assertEqual(self.obs['status'],'USER_REPORTED_IN_GAME_OBSERVATION')
        for key in ['actual_test_date','new_game_date','simulation_months','save_reload','tested_file_hashes_supplied_by_user']:
            self.assertIsNone(self.obs[key])
        self.assertFalse(self.obs['grants_terminal_status'])

    def test_visual_observation_cannot_be_repurposed_as_terminal_receipt(self):
        s=copy.deepcopy(self.s);t=next(t for t in s['tasks'] if t['id']=='SC2-TESCHEN')
        t['status']='PASS_RUNTIME_USER_VALIDATED';t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation=a.PREFIX+'TESCHEN_USER_OBSERVATION.json')
        self.assertFalse(a.rm.terminal_evidence(t,s))

    def test_proposal_is_not_an_approved_na_decision(self):
        decision=a.load(a.OUT/'TESCHEN_PROPOSED_CLOSURE_DECISION.json')
        self.assertIsNone(decision['approved_by']);self.assertIsNone(decision['terminal_status_recommended_now'])
        self.assertFalse(decision['no_correction_required']);self.assertEqual(decision['points_awarded'],0)
        s=copy.deepcopy(self.s);t=next(t for t in s['tasks'] if t['id']=='SC2-TESCHEN')
        t.update(status='NOT_APPLICABLE_VERIFIED',decision=decision)
        self.assertFalse(a.rm.terminal_evidence(t,s))

    def test_selected_task_and_all_other_blocked_statuses_retained(self):
        for t in self.s['tasks']:
            old=next(x for x in self.b['roadmap']['tasks'] if x['id']==t['id'])
            expected='BLOCKED' if t['id']=='SC2-LUXEMBOURG-VALIDATION' else old['status']
            self.assertEqual(t['status'],expected,t['id'])
        lux=next(t for t in self.s['tasks'] if t['id']=='SC2-LUXEMBOURG-VALIDATION')
        self.assertEqual(lux['static_tests']['status'],'SCOPE_REVIEW_REQUIRED')
        self.assertTrue(lux['blocking_reason'])
        self.assertEqual(self.s['closure_campaign']['selected_blocked_task'],'SC2-TESCHEN')

    def test_no_holstein_or_new_task_started(self):
        t=next(t for t in self.s['tasks'] if t['id']=='SC3-HOLSTEIN')
        old=next(t for t in self.b['roadmap']['tasks'] if t['id']=='SC3-HOLSTEIN')
        self.assertEqual(t,old);self.assertEqual(t['status'],'NOT_STARTED')
        self.assertTrue(self.s['closure_campaign']['suspend_new_territories'])

    def test_matrix_covers_exact_old_blocked_set(self):
        matrix=a.load(a.OUT/'BLOCKED_MATRIX.json')
        expected={t['id'] for t in self.b['roadmap']['tasks'] if t['status']=='BLOCKED'}|{'SC2-LUXEMBOURG-VALIDATION'}
        self.assertEqual({r['task_id'] for r in matrix['rows']},expected)
        self.assertEqual(len(expected),24)
        self.assertTrue(all(r['sources'] and r['human_remaining'] and r['conflict_risk'] and r['next_concrete_action'] for r in matrix['rows']))

    def test_missing_human_controls_explicit_for_each_scope(self):
        for row in self.audit['rows']:
            self.assertTrue(row['missing_human']);self.assertFalse(row['new_human_attestation_created'])
        self.assertFalse(list(a.OUT.glob('RUNTIME_USER_ATTESTATION*')))

    def test_additive_event_history(self):
        old=self.b['roadmap']['events'];self.assertEqual(self.s['events'][:len(old)],old)
        self.assertEqual(len({e['id'] for e in self.s['events']}),len(self.s['events']))

    def test_no_acceptance_gate_or_progress_formula_changed(self):
        before=ast.parse((a.OUT/'TRACKER_TOOL_BEFORE.py').read_text(encoding='utf-8-sig'))
        after=ast.parse((a.ROOT/'tools/serg_closure_roadmap.py').read_text(encoding='utf-8-sig'))
        def functions(tree):return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
        old,new=functions(before),functions(after)
        for name in ['terminal_evidence','partial_runtime_evidence','mixed_partial_runtime_evidence','qualifications','progress','structural_errors']:
            self.assertEqual(old[name],new[name],name)

    def test_next_action_routes_campaign_not_expansion(self):
        text=(a.rm.OUT/'NEXT_ACTION.md').read_text(encoding='utf-8')
        self.assertIn('campagne de levée des blocages',text)
        self.assertIn('PLAYER_TEST_PROTOCOL_GROUPED.md',text)
        self.assertNotIn('Prochain candidat territorial préparé',text)

    def test_all_prior_nested_serg_proofs_retained(self):
        for rel,h in self.b['prior_proofs'].items():
            if Path(rel).parent!=a.rm.OUT.relative_to(a.ROOT):self.assertEqual(a.sha(a.ROOT/rel),h,rel)

    def test_canonical_tracker_validator(self):self.assertEqual(a.rm.check()['status'],'PASS')

if __name__=='__main__':unittest.main()
