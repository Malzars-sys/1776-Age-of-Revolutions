"""R3 availability, bounded receipts and preservation contracts; not engine tests."""
import copy,csv,json,unittest
import audit_starting_tech_1776_r3 as a

def csvread(n):
    with (a.OUT/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

class R3Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=a.load(a.OUT/'BASELINE.json');cls.before=a.load(a.OUT/'CURRENT_BEFORE.json');cls.after=a.load(a.OUT/'RESOLVED_AFTER.json');cls.s=a.contract.collect_snapshot();cls.receipt=a.load(a.r2.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json')
    def test_real_explicit_r2_acceptance_bounded(self):
        self.assertEqual(self.receipt['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertEqual(self.receipt['PM_selections'],12);self.assertEqual(self.receipt['history_tokens'],14);self.assertEqual(self.receipt['functional_files'],5);self.assertEqual(self.receipt['simulation_months'],1);self.assertTrue(self.receipt['save_and_reload']);self.assertIsNone(self.receipt['actual_test_date'])
    def test_r2_entry_all_five_hashes_match(self):
        r=a.load(a.OUT/'R2_ACCEPTANCE.json');self.assertEqual(r['status'],'PASS');self.assertEqual(len(r['functional_comparison']),5);self.assertTrue(all(x['exact'] for x in r['functional_comparison'].values()));self.assertFalse(r['manifest_differences'])
    def test_r2_receipt_excludes_new_r3_and_economic_revisions(self):
        self.assertIn('Toute correction TECH-R3 ou postérieure',self.receipt['excludes']);self.assertFalse(self.receipt['automated_engine_test'] or self.receipt['world_audit_complete']);self.assertIn('ECON-ALLOYS',self.receipt['excludes'][1])
    def test_prior_r1_and_r2_proofs_preserved(self):
        for field in ['R1_proofs','R2_proofs']:
            for p,h in self.base[field].items():self.assertEqual(a.sha(a.ROOT/p),h,p)
    def test_both_prior_audit_states_are_human_validated(self):
        self.assertEqual(a.load(a.r1.OUT/'AUDIT_STATE.json')['status'],'PASS_RUNTIME_USER_VALIDATED');self.assertEqual(a.load(a.r2.OUT/'AUDIT_STATE.json')['status'],'PASS_RUNTIME_USER_VALIDATED')
    def test_original_r2_delivery_files_not_relabelled_for_r3(self):
        f=a.load(a.r2.OUT/'FILES_MODIFIED.json');self.assertIsNone(f['human_validation']);self.assertEqual(f['history_tokens'],14)
    def test_only_two_existing_country_knowledge_sets_change(self):
        existing=set(self.before['starts'])&set(self.after['starts']);changed={t for t in existing if self.before['starts'][t]['technologies']!=self.after['starts'][t]['technologies']};self.assertEqual(changed,{'PRU','TUS'})
    def test_precise_root_additions_without_descendant_gift(self):
        for tag in ['PRU','TUS']:
            before=set(self.before['starts'][tag]['technologies']);now=set(self.s['starts'][tag]['technologies']);self.assertEqual(now-before,{'organized_financial_institutions'});self.assertLessEqual(before,now)
    def test_all_country_references_and_parents_valid(self):
        self.assertFalse(a.r1.graph_debts(self.after))
        for t,v in self.s['starts'].items():self.assertLessEqual(set(v['technologies']),set(self.s['graph']),t);self.assertFalse(v['unresolved'],t)
    def test_no_new_modern_technology_for_port_or_cannon_targets(self):
        for tag in ['JAP','KOR','SUL','MUG','MARATH']:self.assertEqual(self.s['starts'][tag]['technologies'],self.before['starts'][tag]['technologies'])
    def test_alloy_graph_from_accepted_r2_preserved(self):self.assertEqual(set(self.s['graph']['alloysworking']),{'shaft_mining','organized_workshops'})
    def test_technology_graph_and_eras_not_reworked(self):self.assertEqual(self.before['graph'],self.after['graph']);self.assertEqual(self.before['tech_eras'],self.after['tech_eras'])
    def test_all_initial_port_trade_and_military_scopes_audited(self):
        for category,name in [('PORT','PORT_TECH_AUDIT.csv'),('TRADE','TRADE_CENTER_TECH_AUDIT.csv'),('ARMS','ARMS_INDUSTRY_TECH_AUDIT.csv')]:
            rows=csvread(name.replace('.csv','_BEFORE.csv'));self.assertEqual(len(rows),a.load(a.OUT/'FOCUS_BEFORE.json')['categories'][category]['assets']);self.assertTrue(all(r['Sources'] and r['Selected_PM'] for r in rows))
    def test_current_focus_tables_cover_new_concurrent_scopes_too(self):
        for category,name in [('PORT','PORT_TECH_AUDIT.csv'),('TRADE','TRADE_CENTER_TECH_AUDIT.csv'),('ARMS','ARMS_INDUSTRY_TECH_AUDIT.csv')]:
            expected={k for k in self.s['selected'] if k[2] in a.FOCUS[category]};actual={(r['State'],r['TAG'],r['Building']) for r in csvread(name)};self.assertEqual(actual,expected)
    def test_no_automatic_global_port_downgrade(self):
        changes=[e for r in a.load(a.OUT/'PORT_PATCHES.json') if r.get('edits') for e in r['edits'] if 'tag' in e];self.assertEqual({(x['tag'],x['state']) for x in changes},a.PORT_TARGETS);self.assertEqual(len(changes),3)
    def test_traditional_ports_have_neutral_data_and_compatible_pm(self):
        for tag,state in a.PORT_TARGETS:
            p=self.s['selected'][(state,tag,'building_port')];self.assertEqual(p['pmg_base_building_port'],a.PORT_PM);self.assertEqual(p['pmg_1776_raw_data_reporting'],'pm_1776_no_raw_data_reporting')
            for pm in p.values():self.assertFalse(set(a.r1.values(self.s['pms'][pm],'unlocking_technologies'))-set(self.s['starts'][tag]['technologies']))
    def test_no_replacement_of_operating_port_by_zero_output_anchorage(self):
        ins,outs,jobs=a.flows(a.numeric_sum([a.PORT_PM],self.s['pms']));self.assertGreater(outs['merchant_marine'],0);self.assertGreater(sum(jobs.values()),100);self.assertEqual(ins,{'wood':9,'fabric':3})
    def test_specialized_port_remains_more_productive_per_worker(self):
        margins={}
        goods,_,_=a.r1.objects('common/goods');prices={g:float(a.r1.val(n,'cost','0')) for g,n in goods.items()}
        for pm in ['pm_basic_port',a.PORT_PM]:
            ins,outs,jobs=a.flows(a.numeric_sum([pm],self.s['pms']));margins[pm]=(sum(prices[g]*v for g,v in outs.items())-sum(prices[g]*v for g,v in ins.items()))/sum(jobs.values())
        self.assertGreater(margins['pm_basic_port'],margins[a.PORT_PM]);self.assertGreater(margins[a.PORT_PM],0)
    def test_old_and_future_port_methods_not_removed(self):
        methods=a.r1.values(self.s['groups']['pmg_base_building_port'],'production_methods');self.assertEqual([p for p in methods if p!=a.PORT_PM],['pm_anchorage','pm_basic_port','pm_industrial_port','pm_modern_port']);self.assertIsNone(a.r1.val(self.s['pms'][a.PORT_PM],'is_default'))
    def test_only_one_group_contains_new_port_pm(self):self.assertEqual([g for g,n in self.s['groups'].items() if a.PORT_PM in a.r1.values(n,'production_methods')],['pmg_base_building_port'])
    def test_port_levels_and_ownership_survive_exact_patch(self):
        for patch in a.load(a.OUT/'PORT_PATCHES.json'):
            if not patch['file'].startswith('common/history/buildings/'):continue
            old=(a.ROOT/patch['preimage']).read_bytes();raw=old.decode('utf-8-sig')
            for e in sorted(patch['edits'],key=lambda e:e['start'],reverse=True):raw=raw[:e['start']]+e['new']+raw[e['end']:]
            self.assertEqual((a.ROOT/patch['file']).read_bytes(),a.encode_like(raw,old))
    def test_all_four_financially_justified_centers_now_compatible(self):
        rows=[r for r in csvread('BUILDING_PM_BEFORE_AFTER.csv') if r['TAG'] in ['PRU','TUS']];self.assertEqual(len(rows),4);self.assertTrue(all(r['PM_Gates_After']=='{}' and r['PM_Before']==r['PM_After'] for r in rows))
    def test_r2_trade_choices_not_repeated(self):
        r=a.load(a.OUT/'R2_TRADE_WITNESSES.json');self.assertTrue(r['unchanged_and_compatible']);self.assertEqual(len(r['selected']),3)
    def test_normal_trade_recipe_and_higher_capacity_gates_not_changed(self):
        pre=a.load(a.OUT/'BASELINE.json')['hashes'];p='common/production_methods/11_private_infrastructure.txt';self.assertEqual(a.sha(a.ROOT/p),pre[p])
    def test_only_cannon_gate_child_changed_in_live_industry_file(self):
        patch=a.load(a.OUT/'ARMS_PATCHES.json')[0];old=(a.ROOT/patch['preimage']).read_text(encoding='utf-8-sig');pm=next(n for n in a.cw.parse(old) if n.key=='pm_cannons');ignore_gate=lambda n:[a.qa.signature(x) for x in n.children() if x.key!='unlocking_technologies'];self.assertEqual(ignore_gate(pm),ignore_gate(self.s['pms']['pm_cannons']))
    def test_no_cannon_recipe_or_economic_group_written(self):
        paths={p['file'] for p in a.owned_patches()};self.assertNotIn('common/production_method_groups/01_industry.txt',paths);self.assertNotIn('common/production_methods/1776_alloys_utensils.txt',paths);self.assertNotIn('common/buildings/01_industry.txt',paths)
    def test_two_traditional_foundries_meet_actual_gate(self):
        for tag,state in [('MUG','STATE_DELHI'),('MARATH','STATE_AGRA')]:
            self.assertIn('pm_cannons',self.s['selected'][(state,tag,'building_artillery_foundry')].values());self.assertLessEqual(set(a.r1.values(self.s['pms']['pm_cannons'],'unlocking_technologies')),set(self.s['starts'][tag]['technologies']))
    def test_foundry_rebuilding_gate_not_confused_with_production(self):
        self.assertEqual(a.r1.values(self.s['buildings']['building_artillery_foundry'],'unlocking_technologies'),['standardized_field_artillery'])
        for tag in ['MUG','MARATH']:self.assertNotIn('standardized_field_artillery',self.s['starts'][tag]['technologies'])
    def test_global_cannon_and_port_availability_impact_exhaustive(self):
        rows=csvread('GLOBAL_AVAILABILITY_IMPACT.csv');self.assertEqual({r['TAG'] for r in rows},set(self.after['starts']));self.assertTrue(all(r['Port_New_PM_Tech_Eligible']=='True' for r in rows));self.assertTrue(any(r['Cannon_Old_Gate_Met']=='False' and r['Cannon_New_Gates_Met']=='True' for r in rows))
    def test_no_country_loses_previously_available_cannon_pm(self):
        rows=csvread('GLOBAL_AVAILABILITY_IMPACT.csv');self.assertFalse([r['TAG'] for r in rows if r['Cannon_Old_Gate_Met']=='True' and r['Cannon_New_Gates_Met']=='False'])
        for tag in ['GAL','MLT']:self.assertLessEqual(set(a.r1.values(self.s['pms']['pm_cannons'],'unlocking_technologies')),set(self.s['starts'][tag]['technologies']))
    def test_no_unknown_goods_in_affected_methods(self):
        goods,_,_=a.r1.objects('common/goods')
        for pm in [a.PORT_PM,'pm_cannons','pm_trade_center_trade_quantity_normal']:
            ins,outs,_=a.flows(a.numeric_sum([pm],self.s['pms']));self.assertLessEqual(set(ins)|set(outs),set(goods))
    def test_port_sensitivity_reports_losses_as_well_as_gains(self):
        rows=csvread('PORT_COST_SENSITIVITY.csv');self.assertTrue(all(r['Not_Engine_Income']=='True' for r in rows));values=[float(r['Illustrative_Net']) for r in rows if r['PM']==a.PORT_PM];self.assertLess(min(values),0);self.assertGreater(max(values),0)
    def test_clipper_market_access_is_not_falsely_guaranteed(self):
        rows=csvread('PORT_INPUT_ACCESS_REVIEW.csv');self.assertEqual(len(rows),3);self.assertTrue(all(r['Input_Access_Guaranteed']=='False' for r in rows))
    def test_traditional_port_does_not_require_missing_shipyard_or_imported_clippers(self):
        ins,_,_=a.flows(a.numeric_sum([a.PORT_PM],self.s['pms']));self.assertNotIn('clippers',ins)
        pms=self.s['pms'];sources=[a.flows(a.numeric_sum([pm],pms))[1] for pm in pms if 'subsistence' in pm];self.assertTrue(any({'wood','fabric'}<=set(row) for row in sources))
    def test_localization_both_languages_bom_and_single_entry(self):
        for lang in ['french','english']:
            data=(a.ROOT/f'localization/{lang}/1776_tech_r3_harbor_l_{lang}.yml').read_bytes();self.assertTrue(data.startswith(b'\xef\xbb\xbf'));self.assertIn(('l_'+lang+':').encode(),data);self.assertEqual(data.count((a.PORT_PM+':0').encode()),1)
    def test_no_territorial_or_population_patch_owned(self):
        for patch in a.owned_patches():self.assertFalse(patch['file'].startswith(('map_data/','common/history/states/','common/history/pops/','common/history/diplomacy/','common/country_definitions/')))
    def test_873_serg_proofs_and_state_retained(self):
        self.assertEqual(len(self.base['SERG_proofs']),873)
        for p,h in self.base['SERG_proofs'].items():self.assertEqual(a.sha(a.ROOT/p),h,p)
        self.assertEqual(a.load(a.r1.rm.OUT/'ROADMAP_STATE.json'),self.base['SERG_state'])
    def test_independent_ragusa_not_attributed_to_our_grants(self):
        rows=csvread('TECH_BEFORE_AFTER.csv');rag=next(r for r in rows if r['TAG']=='RAG');self.assertEqual(rag['R3_Own_Grant'],'False');self.assertEqual(rag['New_Concurrent_Tag'],'True');self.assertNotIn('RAG',a.FINANCIAL_TAGS)
    def test_econ_and_world_external_scopes_are_accounted(self):
        c=a.load(a.OUT/'CONCURRENT_CHANGES.json');self.assertFalse(c['unreviewed_external_paths']);self.assertTrue(c['ECON']['our_cannon_gate_file_not_in_ECON_owned']);self.assertTrue(all(r['after_matches'] for r in c['WORLD_verified_files'].values()))
    def test_r3_has_no_human_attestation(self):
        self.assertFalse(list(a.OUT.glob('RUNTIME_USER_ATTESTATION*')));self.assertIsNone(a.load(a.OUT/'FILES_MODIFIED.json')['human_validation']);self.assertEqual(a.load(a.OUT/'FILES_MODIFIED.json')['installation_status'],'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')
    def test_reusable_validator_separates_remaining_construction_gates(self):
        r=a.contract.audit_country('MUG',self.s);self.assertFalse(any(f['code']=='SELECTED_PM_UNLOCK_GATE' and f.get('PM')=='pm_cannons' for f in r['findings']));self.assertTrue(any(f['code']=='CONSTRUCTION_GATE_ONLY' and f.get('building')=='building_artillery_foundry' for f in r['findings']))

if __name__=='__main__':unittest.main()
