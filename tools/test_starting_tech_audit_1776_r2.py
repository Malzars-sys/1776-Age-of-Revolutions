"""R2 current-workspace and reusable per-TAG contracts; no engine simulation."""
import copy,csv,unittest
import audit_starting_tech_1776_r2 as a
import validate_starting_technology_1776 as contract

class R2Delivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=a.load(a.OUT/'CURRENT_BEFORE.json');cls.after=a.load(a.OUT/'RESOLVED_AFTER.json');cls.base=a.load(a.OUT/'BASELINE.json');cls.s=contract.collect_snapshot()
    def test_receipt_really_human_and_exact_r1_scope(self):
        r=a.load(a.r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json');self.assertEqual(r['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertEqual(set(r['corrected_tags']),set(a.r1.ASSIGNMENTS));self.assertEqual(r['country_tech_additions'],28);self.assertIsNone(r['actual_test_date']);self.assertTrue(r['save_and_reload']);self.assertEqual(r['simulation_months'],1)
    def test_receipt_excludes_r2_world_and_territory(self):
        r=a.load(a.r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json');self.assertFalse(r['world_audit_complete'] or r['serg_closure_approved'] or r['automated_engine_test']);self.assertIn('Toute modification R2 ou postérieure',r['excludes'])
    def test_exact_tested_mine_kept(self):
        r=a.load(a.r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json');self.assertEqual(r['bgt_mine']['nominal_jobs'],5000)
        for path,h in r['tested_functional_files'].items():self.assertEqual(a.sha(a.ROOT/path),h,path)
    def test_original_r1_proofs_after_receipt_not_rewritten(self):
        self.assertTrue(all(a.sha(a.ROOT/p)==h for p,h in self.base['r1_proofs'].items()))
    def test_all_470_knowledge_sets_identical(self):
        self.assertEqual(self.before['starts'],self.after['starts']);self.assertEqual(len(self.after['starts']),470)
    def test_no_coke_or_late_grants_to_any_country(self):
        for tag in self.before['starts']:self.assertEqual(self.before['starts'][tag]['technologies'],self.after['starts'][tag]['technologies'],tag)
    def test_all_technology_and_shared_effect_references_resolve(self):
        for tag,v in self.after['starts'].items():self.assertFalse(set(v['technologies'])-set(self.after['graph']),tag);self.assertFalse(v['unresolved'],tag)
    def test_alloy_debts_fixed_without_erasing_knowledge(self):
        self.assertEqual(len(a.r1.graph_debts(self.before)),7);self.assertFalse(a.r1.graph_debts(self.after));self.assertEqual(set(self.after['graph']['alloysworking']),{'shaft_mining','organized_workshops'})
    def test_aluminium_and_electric_descendant_gates_preserved(self):
        for key in ['bauxite_processing','bayer_process','electric_arc_process','electrical_capacitors']:
            if key in self.before['graph']:self.assertEqual(self.before['graph'][key],self.after['graph'][key])
        self.assertIn('industrial_alkalis',self.after['graph']['bauxite_processing']);self.assertIn('electrical_capacitors',self.after['graph']['bayer_process'])
    def test_full_global_alloy_parent_impact_not_automatic_grants(self):
        with (a.OUT/'ALLOYS_GLOBAL_IMPACT.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),470);self.assertEqual(sum(r['Alloys_Held']=='True' for r in rows),12);self.assertEqual(sum(r['Before_Parent_Gates_Met']=='True' for r in rows),5);self.assertEqual(sum(r['After_Parent_Gates_Met']=='True' for r in rows),93);self.assertTrue(all(r['New_Grant']=='False' for r in rows))
    def test_graph_unknown_parent_and_cycle_absent(self):
        graph=self.after['graph']
        def visit(k,trail=()):
            self.assertNotIn(k,trail)
            for p in graph[k]:self.assertIn(p,graph);visit(p,trail+(k,))
        for k in graph:visit(k)
    def test_current_twelve_corrected_pm_gates_satisfied(self):
        for _,tag,state,kind,old,new in a.PM_PLAN:
            selected=self.s['selected'][(state,tag,kind)];self.assertIn(new,selected.values());self.assertNotIn(old,selected.values());self.assertFalse(set(a.r1.values(self.s['pms'][new],'unlocking_technologies'))-set(self.s['starts'][tag]['technologies']))
    def test_both_ceylon_layers_patched_without_duplicate_building_claim(self):
        for kind,new in [('building_railway','pm_no_canal_network'),('building_trade_center','pm_trade_center_trade_quantity_limited')]:
            rows=[r for r in a.placements() if (r['tag'],r['state'],r['building'])==('KND','STATE_CEYLON',kind)];self.assertEqual(len(rows),2);self.assertTrue(all(new in r['methods'] for r in rows))
    def test_pm_deltas_are_explicit_not_promises_of_profit(self):
        with (a.OUT/'BUILDING_TECH_FIXES.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),12);self.assertTrue(all(r['Written_Parameter_Delta'] and r['Status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' for r in rows))
        self.assertEqual(sum(int(r['History_Declarations']) for r in rows),14)
    def test_no_new_initial_declaration_gate_conflict(self):
        key=lambda r:tuple(sorted(r.items()));self.assertLessEqual({key(r) for r in self.after['conflicts']},{key(r) for r in self.before['conflicts']});self.assertEqual(len(self.after['conflicts']),195)
    def test_old_construction_gates_not_called_production_failure(self):
        with (a.OUT/'PRIORITY_MATRIX.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        gates=[r for r in rows if r['R1_Kind']=='BUILDING_TECH_CONFLICT' and r['Object']==r['Building']];self.assertEqual(len(gates),54);self.assertTrue(all(r['Conclusion']=='CONSTRUCTION_GATE_ONLY_NOT_PROOF_OF_NO_PRODUCTION' for r in gates))
    def test_eight_missing_histories_open_individually_not_westernized(self):
        with (a.OUT/'MISSING_HISTORY_REVIEW.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertEqual({r['TAG'] for r in rows},set(a.MISSING));self.assertTrue(all(r['Intentional_Absence_Verified']=='False' and r['Source'] and r['Research'] for r in rows))
        for tag in a.MISSING:self.assertFalse(self.s['starts'][tag]['history'] or self.s['starts'][tag]['technologies'])
    def test_indop_existing_spice_not_missing_tech_industry(self):
        result=contract.audit_country('INDOP',self.s,a.load(a.OUT/'MISSING_HISTORY_EXPECTATIONS.json')['INDOP']);self.assertEqual(len(result['buildings']),1);self.assertEqual(result['buildings'][0]['building'],'building_spice_plantation');self.assertFalse(any(r['code']=='SELECTED_PM_UNLOCK_GATE' for r in result['findings']))
    def test_all_93_new_tags_reviewed_including_political_nuclei(self):
        rows=a.load(a.OUT/'NEW_TAG_TECH_REVIEW.json');self.assertEqual(len(rows),93);self.assertTrue({'BGT','BRX','TRT','MCA'}<={r['TAG'] for r in rows});self.assertTrue(all(not r['human_validated'] for r in rows))
    def test_serg_and_world_tracking_bytes_preserved(self):
        for field in ['serg_proofs','world_tracking']:
            for rel,h in self.base[field].items():self.assertEqual(a.sha(a.ROOT/rel),h,rel)
    def test_r2_still_awaits_user_and_has_no_new_receipt(self):
        files=a.load(a.OUT/'FILES_MODIFIED.json');self.assertEqual(files['installation_status'],'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION');self.assertIsNone(files['human_validation']);self.assertFalse(list(a.OUT.glob('RUNTIME_USER_ATTESTATION*')))

class ReusableTagContract(unittest.TestCase):
    def toy(self):
        node=lambda raw:a.cw.parse(raw)[0]
        return dict(starts={'AAA':dict(technologies=['craft'],conditional_technologies=[],unresolved=[],history=['MOD:local_history'],effects=[])},graph={'craft':[],'advanced':['craft']},late=set(),definitions={},buildings={'shop':node('shop = { production_method_groups = { base } unlocking_technologies = { advanced } }')},pms={'manual':node('manual = { }'),'machine':node('machine = { unlocking_technologies = { advanced } }')},groups={'base':node('base = { production_methods = { manual machine } }')},selected={('STATE_TEST','AAA','shop'):{'base':'manual'}},declarations={('STATE_TEST','AAA','shop'):1},regions={},unassigned=[],law_requests={},laws={},units={},inventory={'units':[]})
    def codes(self,s,e=None):return {f['code'] for f in contract.audit_country('AAA',s,e)['findings']}
    def test_unknown_tag_fails(self):self.assertEqual(contract.audit_country('NOPE',self.toy())['status'],'FAIL_STATIC')
    def test_construction_gate_is_not_pm_or_production_failure(self):
        result=contract.audit_country('AAA',self.toy());gate=next(f for f in result['findings'] if f['code']=='CONSTRUCTION_GATE_ONLY');self.assertFalse(gate['production_failure_proved']);self.assertFalse(any(f['code']=='SELECTED_PM_UNLOCK_GATE' for f in result['findings']))
    def test_incompatible_selected_pm_detected(self):
        s=self.toy();s['selected'][('STATE_TEST','AAA','shop')]['base']='machine';self.assertIn('SELECTED_PM_UNLOCK_GATE',self.codes(s))
    def test_compatible_pm_is_accepted_after_real_technology(self):
        s=self.toy();s['selected'][('STATE_TEST','AAA','shop')]['base']='machine';s['starts']['AAA']['technologies'].append('advanced');self.assertNotIn('SELECTED_PM_UNLOCK_GATE',self.codes(s))
    def test_missing_history_requires_explicit_evidence(self):
        s=self.toy();s['starts']['AAA']['history']=[];self.assertIn('MISSING_HISTORY_WITHOUT_EVIDENCE',self.codes(s));self.assertIn('MISSING_HISTORY_WITHOUT_EVIDENCE',self.codes(s,{'absence_policy':'INTENTIONAL_VERIFIED'}))
    def test_open_absence_exception_stays_review(self):
        s=self.toy();s['starts']['AAA']['history']=[];s['selected']={};r=contract.audit_country('AAA',s,{'absence_policy':'OPEN_DOCUMENTED_REVIEW','absence_evidence':'regional research'});self.assertEqual(r['status'],'REVIEW');self.assertIn('NO_HISTORY_REVIEW_OPEN',{f['code'] for f in r['findings']});self.assertFalse(r['human_validated'])
    def test_unknown_tech_not_hidden_by_absence_policy(self):
        s=self.toy();s['starts']['AAA']['technologies'].append('fake');self.assertIn('UNKNOWN_TECHNOLOGY',self.codes(s,{'absence_policy':'INTENTIONAL_VERIFIED','absence_evidence':'note'}))
    def test_parent_debt_detected_independently(self):
        s=self.toy();s['starts']['AAA']['technologies']=['advanced'];self.assertIn('MISSING_TECH_PARENT',self.codes(s))
    def test_local_required_and_forbidden_not_uniform_tier(self):
        s=self.toy();codes=self.codes(s,{'required':['advanced'],'forbidden':['craft']});self.assertIn('REQUIRED_LOCAL_CAPABILITY_MISSING',codes);self.assertIn('FORBIDDEN_LOCAL_START_TECH',codes);self.assertNotIn('REQUIRED_LOCAL_CAPABILITY_MISSING',self.codes(s,{'required':['craft']}))
    def test_chronological_flags_require_review_not_automatic_removal(self):
        s=self.toy();s['late']={'craft'};self.assertIn('HISTORICAL_ANACHRONISM_FLAG_REQUIRES_SOURCE',self.codes(s));self.assertIn('craft',s['starts']['AAA']['technologies'])
    def test_conditional_grant_never_certified_initial(self):
        s=self.toy();s['starts']['AAA']['conditional_technologies']=['advanced'];self.assertIn('CONDITIONAL_GRANT_NOT_CERTIFIED_INITIAL',self.codes(s));self.assertNotIn('advanced',s['starts']['AAA']['technologies'])
    def test_wrong_group_declaration_reported(self):
        s=self.toy();s['unassigned']=[(('STATE_TEST','AAA','shop'),'machine')];self.assertIn('DECLARED_PM_NOT_IN_BUILDING_GROUP',self.codes(s))
    def test_law_requests_not_claimed_as_active_laws(self):
        s=self.toy();s['law_requests']={'AAA':['law_test']};s['laws']={'law_test':a.cw.parse('law_test = { unlocking_technologies = { advanced } }')[0]};r=contract.audit_country('AAA',s);f=next(f for f in r['findings'] if f['code']=='REQUESTED_LAW_TECH_GATE');self.assertTrue(f['actual_active_law_not_certified'])
    def test_input_contract_is_read_only(self):
        s=self.toy();before=copy.deepcopy(s);contract.audit_country('AAA',s,{'required':['advanced']});self.assertEqual(s,before)

if __name__=='__main__':unittest.main()
