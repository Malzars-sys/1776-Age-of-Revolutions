"""Read-only tracker tests; --report writes ONLY SERG_CLOSURE test evidence.

Synthetic positive/negative cases never persist simulated statuses or receipts.
No game engine, installer, Git write or network command is invoked.
"""
import copy,hashlib,json,sys,unittest
from unittest.mock import patch
import serg_closure_roadmap as rm


class RoadmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.initial=rm.load_json(rm.OUT/'INITIAL_STATE.json')
        # Golden and synthetic tests use the immutable import, not future work.
        cls.state=copy.deepcopy(cls.initial)
        cls.live=rm.load_json(rm.OUT/'ROADMAP_STATE.json')
        cls.current=rm.progress(cls.state)

    def task(self,id,state=None):
        return next(t for t in (state or self.state)['tasks'] if t['id']==id)

    def decision(self,field):
        # Synthetic decision data, confined to memory and marked as such.
        return {field:True,'approved_by':'user','reason':'SYNTHETIC TEST ONLY',
                'evidence':[rm.G+'/REPORT.md']}

    def test_initial_fraction_and_denominator(self):
        p=self.current
        self.assertEqual((p['earned_weight'],p['total_weight'],p['percent']),(60,235,'25.53'))
        self.assertEqual(p['exact_fraction'],'1200/47')
        self.assertEqual((p['qualified_tasks'],p['total_tasks']),(19,81))

    def test_seven_phases_reconcile_without_extra_credit(self):
        self.assertEqual([p['id'] for p in self.current['phases']],list(range(1,8)))
        self.assertEqual(sum(p['earned_weight'] for p in self.current['phases']),60)
        self.assertEqual(sum(p['total_weight'] for p in self.current['phases']),235)

    def test_next_is_salzburg_not_started(self):
        self.assertEqual(self.current['next_task'],'SC1-SALZBURG')
        self.assertEqual(self.task('SC1-SALZBURG')['status'],'NOT_STARTED')
        self.assertEqual(self.state['initialization']['territorial_changes'],0)

    def test_all_eight_pending_receipts_remain_open(self):
        pending=self.current['awaiting_runtime']
        self.assertEqual(len(pending),8)
        self.assertTrue(all(not rm.terminal_evidence(self.task(id),self.state) for id in pending))

    def test_research_ready_and_blocked_never_earn_points(self):
        for status in ('NOT_STARTED','IN_PROGRESS','RESEARCH_COMPLETE','IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','BLOCKED'):
            state=copy.deepcopy(self.state);self.task('SC1-SALZBURG',state)['status']=status
            self.assertEqual(rm.progress(state)['earned_weight'],60,status)

    def test_imported_manual_receipts_are_real_scoped_files(self):
        legacy=[t for t in self.state['tasks'] if t['kind']=='legacy_core']
        self.assertEqual(len(legacy),19)
        self.assertTrue(all(rm.terminal_evidence(t,self.state) for t in legacy))
        self.assertEqual(self.task('BASE-REGENSBURG')['installed_lots'],['MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/R4C'])
        self.assertEqual(self.task('BASE-PEENE')['weight'],3)

    def test_existing_scopes_not_expanded_by_same_receipt(self):
        t=copy.deepcopy(self.task('BASE-PASSAU'));t['title']='Uninspected peripheral possessions'
        self.assertFalse(rm.terminal_evidence(t,self.state))

    def test_pass_without_receipt_is_rejected(self):
        t=copy.deepcopy(self.task('SC1-SALZBURG'));t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(rm.terminal_evidence(t,self.state))

    def test_old_receipt_cannot_validate_new_sublot(self):
        t=copy.deepcopy(self.task('SC1-SALZBURG'));old=self.task('BASE-PASSAU')
        for k in ('runtime_validation','static_tests','implementation_report'):t[k]=copy.deepcopy(old[k])
        t['status']='PASS_RUNTIME_USER_VALIDATED';t['static_tests']['status']='PASS'
        self.assertFalse(rm.terminal_evidence(t,self.state))

    def test_p0_cannot_be_deferred_even_with_decision(self):
        t=copy.deepcopy(self.task('SC1-SALZBURG'));t['status']='DEFERRED_APPROVED'
        t['decision']=self.decision('nonblocking_1_0')
        self.assertFalse(rm.terminal_evidence(t,self.state))

    def test_p1_deferral_requires_explicit_authority(self):
        t=copy.deepcopy(self.task('SC5-JEVER'));t['status']='DEFERRED_APPROVED'
        self.assertFalse(rm.terminal_evidence(t,self.state))
        t['decision']=self.decision('nonblocking_1_0')
        self.assertTrue(rm.terminal_evidence(t,self.state))
        t['decision']['approved_by']='agent'
        self.assertFalse(rm.terminal_evidence(t,self.state))

    def test_verified_no_change_requires_evidence_and_decision(self):
        t=copy.deepcopy(self.task('SC7-MEMBERS-ELECTORS'));t['status']='NOT_APPLICABLE_VERIFIED'
        self.assertFalse(rm.terminal_evidence(t,self.state))
        t['decision']=self.decision('no_correction_required')
        t['static_tests']={'status':'PASS','evidence':[rm.G+'/REGISTRY_CHECKS.json']}
        self.assertTrue(rm.terminal_evidence(t,self.state))

    def test_pending_runtime_cannot_be_bypassed_by_na(self):
        t=copy.deepcopy(self.task('SC5-MINDEN-VALIDATION'));t['status']='NOT_APPLICABLE_VERIFIED'
        t['decision']=self.decision('no_correction_required')
        self.assertFalse(rm.terminal_evidence(t,self.state))

    def test_final_cannot_be_waived_or_declared_complete(self):
        for status in ('DEFERRED_APPROVED','NOT_APPLICABLE_VERIFIED','PASS_RUNTIME_USER_VALIDATED'):
            t=copy.deepcopy(self.task('SC7-FINAL-APPROVAL'));t['status']=status
            t['decision']=self.decision('nonblocking_1_0')
            self.assertFalse(rm.terminal_evidence(t,self.state))
        self.assertFalse(self.current['complete'])
        self.assertFalse(self.state['closure_approval']['approved'])

    def test_rounding_guard_never_displays_premature_100(self):
        with patch.object(rm,'qualifications',return_value={t['id']:True for t in self.state['tasks']}):
            p=rm.progress(self.state)
        self.assertEqual(p['percent'],'99.99');self.assertFalse(p['complete'])

    def test_synthetic_final_receipt_requires_explicit_approval(self):
        state=copy.deepcopy(self.state);t=self.task('SC7-FINAL-APPROVAL',state)
        t['status']='PASS_RUNTIME_USER_VALIDATED'
        t['static_tests']={'status':'PASS','evidence':['synthetic-static.json']}
        t['runtime_validation'].update(status='PASS_RUNTIME_USER_VALIDATED',attestation='synthetic-human.json')
        t['implementation_report']=['synthetic-report.md']
        human={'status':'PASS_RUNTIME_USER_VALIDATED','automated_engine_test':False,'task_ids':[t['id']],
               'new_game_date':'1776-01-01','simulation_months':1,'source':'SYNTHETIC TEST ONLY'}
        static={'task_ids':[t['id']],'total':1,'passed':1,'failed':[]}
        def fake_load(path):return human if path.name=='synthetic-human.json' else static
        with patch.object(rm,'refs_exist',return_value=True),patch.object(rm,'load_json',side_effect=fake_load):
            self.assertFalse(rm.terminal_evidence(t,state))
            state['closure_approval']={'approved':True,'approved_by':'user','scope_version':'1.0.0','source':'synthetic-approval.md'}
            self.assertTrue(rm.terminal_evidence(t,state))
            state['closure_approval']['scope_version']='wrong-version'
            self.assertFalse(rm.terminal_evidence(t,state))

    def test_dependencies_are_checked_and_cycles_rejected(self):
        state=copy.deepcopy(self.state)
        self.task('SC1-SALZBURG',state)['depends_on']=['SC1-TRENTO']
        with self.assertRaisesRegex(ValueError,'Dependency cycle'):rm.progress(state)
        state=copy.deepcopy(self.state);self.task('SC1-SALZBURG',state)['depends_on']=['NONEXISTENT']
        with self.assertRaisesRegex(ValueError,'Missing dependency'):rm.progress(state)

    def test_initial_history_preserved(self):
        self.assertEqual(self.state['events'][:1],self.initial['events'])
        self.assertEqual({t['id']:t['status'] for t in self.state['tasks']},self.initial['events'][0]['initial_statuses'])
        self.assertEqual(self.live['events'][:len(self.initial['events'])],self.initial['events'])

    def test_silent_weight_change_rejected(self):
        state=copy.deepcopy(self.state);self.task('SC1-SALZBURG',state)['weight']=1
        self.assertIn('Scope changed without a new manifest/version',rm.structural_errors(state))

    def test_deleted_task_rejected(self):
        state=copy.deepcopy(self.state);state['tasks']=[t for t in state['tasks'] if t['id']!='SC1-ORTENBURG']
        self.assertIn('Initial tasks must not disappear',rm.structural_errors(state))

    def test_status_edit_without_history_rejected(self):
        state=copy.deepcopy(self.state);self.task('SC1-SALZBURG',state)['status']='IN_PROGRESS'
        self.assertIn('Status change without additive history',rm.structural_errors(state))

    def test_all_original_issues_have_explicit_mapping(self):
        issues=rm.load_json(rm.AUDIT/'ISSUE_DATA.json')
        linked={i for t in self.state['tasks'] for i in t['issues']}|{d['audit_issue'] for d in self.state['deferred_p2']}
        self.assertTrue(linked>={i['ID'] for i in issues})
        self.assertEqual(sum(i['Priorite']=='P0' for i in issues),3)
        self.assertEqual(sum(i['Priorite']=='P1' for i in issues),21)

    def test_p2_proposals_are_not_false_user_approvals(self):
        approved=[d['audit_issue'] for d in self.state['deferred_p2'] if d['status']=='DEFERRED_APPROVED']
        self.assertEqual(approved,['R25','R26'])
        self.assertTrue(all(d['blocking_1_0'] is False for d in self.state['deferred_p2']))

    def test_reference_paths_and_line_numbers_resolve(self):
        refs={r for t in self.state['tasks'] for r in t['historical_sources']}
        for ref in refs:
            p=rm.file_ref(ref);self.assertTrue(p.is_file(),ref)
            raw,sep,last=ref.rpartition(':')
            if sep and last.isdigit():self.assertTrue(1<=int(last)<=len(p.read_text(encoding='utf-8-sig').splitlines()),ref)
        for ref,h in self.state['source_manifest'].items():self.assertEqual(rm.digest(rm.file_ref(ref)),h,ref)

    def test_task_fields_and_acceptance_are_explicit(self):
        required=('id','phase','historical_region','jurisdiction','identified_problem','priority','historical_sources','before','expected','depends_on','acceptance_profile','status','implementation_report','static_tests','runtime_validation','residual_uncertainty')
        for t in self.live['tasks']:
            self.assertTrue(all(k in t for k in required),t['id'])
            self.assertTrue(t['acceptance'] and t['historical_perimeter'],t['id'])

    @unittest.skipUnless('--initial-preservation' in sys.argv,'Initial no-edit check only; future authorized edits must not fail old snapshots')
    def test_protection_runtime_git_and_audit(self):
        observed=rm.observe(self.state)
        self.assertEqual(observed['runtime_files'],2362)
        self.assertEqual(observed['runtime_changed'],[])
        self.assertEqual(observed['source_audit_changed'],[])
        self.assertTrue(all(observed[k] for k in ('head_unchanged','branch_unchanged','index_unchanged','agents_original_preserved')))

    def test_scoped_agents_instruction_and_startup_fallback(self):
        original=rm.load_json(rm.file_ref(self.state['workspace_reference']))['agents_text']
        current=(rm.ROOT/'AGENTS.md').read_text(encoding='utf-8-sig')
        self.assertTrue(current.startswith(original))
        self.assertIn('Passes territoriales du Saint-Empire uniquement',current)
        self.assertIn('SERG_CLOSURE/ROADMAP.md',current)
        self.assertIn('Ligne de démarrage de secours',(rm.OUT/'ROADMAP.md').read_text(encoding='utf-8'))

    def test_generated_views_and_readonly_check(self):
        before={p:rm.digest(p) for p in rm.OUT.rglob('*') if p.is_file()}
        result=rm.check()
        after={p:rm.digest(p) for p in before}
        self.assertEqual(before,after)
        self.assertEqual(result['status'],'PASS',result['errors'])
        self.assertFalse(result['automated_engine_test'])


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(RoadmapTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if '--report' in sys.argv:
        # Report is not a human attestation and never changes roadmap statuses.
        report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',
          total=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
          skipped=[dict(test=str(t),reason=reason) for t,reason in result.skipped],
          failed=[dict(test=str(t),traceback=detail) for t,detail in result.failures+result.errors],
          purpose='Synthetic tracker tests and read-only preservation; no new engine run or historical research',
          automated_engine_test=False)
        rm.write_json(rm.OUT/'TESTS.json',report)
    sys.exit(not result.wasSuccessful())
