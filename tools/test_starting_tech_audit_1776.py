"""Read-only positive and negative country-start contracts, not engine tests."""
import copy,unittest
import audit_starting_tech_1776 as a

class StartingTechAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=a.load(a.OUT/'RESOLVED_BEFORE.json');cls.after=a.load(a.OUT/'RESOLVED_AFTER.json')
        cls.base=a.load(a.OUT/'BASELINE.json');cls.effects,_,_=a.objects('common/scripted_effects');cls.techs,_,_=a.objects('common/technology/technologies')
    def resolve(self,raw,effects=None):return a.resolve(a.cw.parse(raw),self.effects if effects is None else effects,self.techs)
    def test_audit_covers_every_actual_start_tag(self):
        self.assertEqual(set(self.after['active_tags']),{r[1] for r in self.base['inventory']['states']})
        self.assertEqual(len(self.after['rows']),470)
    def test_all_new_start_tags_have_history_or_exact_open_exception(self):
        rows=[r for r in self.after['rows'] if r['Tag_Origin']=='NEW_MOD_TAG'];self.assertEqual(len(rows),93)
        for row in rows:
            if row['TAG'] in {'AP7','GR7','HWA','INDOP','PLW','TTI'}:
                self.assertEqual(row['Status'],'MISSING_HISTORY');self.assertEqual(row['Country_Type'],'decentralized')
            else:self.assertTrue(row['History_Sources'],row['TAG'])
    def test_country_names_not_guessed_from_tags(self):self.assertTrue(all(r['Name']!=r['TAG'] for r in self.after['rows']))
    def test_bgt_root_cause_is_missing_grants_not_history(self):
        self.assertTrue(self.before['starts']['BGT']['history']);self.assertEqual(self.before['starts']['BGT']['technologies'],[])
        self.assertIn('effect_starting_politics_reactionary',self.before['starts']['BGT']['effects'])
    def test_politics_effect_gives_no_technology(self):
        g,c,_,_=self.resolve('effect_starting_politics_reactionary = yes');self.assertFalse(g|c)
    def test_exact_eight_profiles_acquired(self):
        expected={'BGT':10,'BRX':8,'TRT':10,'PAP':16,'CAR':7,'ARK':19,'VIE':19,'LGE':13}
        for tag,n in expected.items():self.assertEqual(len(self.after['starts'][tag]['technologies']),n,tag)
    def test_bgt_has_mining_and_forestry_without_industrial_upgrade(self):
        s=set(self.after['starts']['BGT']['technologies']);self.assertTrue({'shaft_mining','organized_forestry'}<=s)
        self.assertFalse(s&{'coke_smelting','atmospheric_engine','scientific_metrology','permanent_engineer_services','railways'})
    def test_no_blind_austria_copy(self):
        s=set(self.after['starts']['AUS']['technologies'])
        for tag in ['BGT','BRX','TRT']:self.assertNotEqual(set(self.after['starts'][tag]['technologies']),s)
    def test_no_new_military_grants_to_alpine_nuclei(self):
        for tag in ['BGT','BRX','TRT']:
            self.assertFalse(any(self.after['tech_categories'][t]=='military' for t in self.after['starts'][tag]['technologies']))
    def test_all_corrected_prerequisites_closed(self):
        for tag in a.ASSIGNMENTS:
            s=set(self.after['starts'][tag]['technologies']);self.assertEqual(a.ancestors(s,self.after['graph']),s,tag)
    def test_non_corrected_countries_unchanged(self):
        for tag in set(self.after['active_tags'])-set(a.ASSIGNMENTS):self.assertEqual(self.before['starts'][tag]['technologies'],self.after['starts'][tag]['technologies'],tag)
    def test_massa_not_given_unrepresented_carrara_mining(self):self.assertEqual(self.before['starts']['MCA']['technologies'],self.after['starts']['MCA']['technologies'])
    def test_intentional_empty_profiles_not_westernised(self):
        for tag in ['ANK','BNY','BRD','BUG','KRG','LAN','RWD','PPU']:
            self.assertEqual(self.before['starts'][tag]['technologies'],self.after['starts'][tag]['technologies']);self.assertFalse(self.after['starts'][tag]['technologies'])
    def test_sericulture_nonresearchable_marker_preserved(self):
        for tag in ['CHI','JAP','KOR','MGL','XIN','YUN']:self.assertIn('sericulture',self.after['starts'][tag]['technologies'])
    def test_nested_shared_profile_resolves(self):
        g,c,_,u=self.resolve('aor1776_start_salt_provostry = yes');self.assertEqual(g,a.PROFILE_TECHS['aor1776_start_salt_provostry']);self.assertFalse(c or u)
    def test_unknown_profile_reference_rejected(self):
        _,_,_,u=self.resolve('aor1776_start_DOES_NOT_EXIST = yes');self.assertEqual(u,['UNKNOWN_EFFECT:aor1776_start_DOES_NOT_EXIST'])
    def test_cycle_reported_instead_of_recursing_forever(self):
        e={'one':a.cw.parse('one = { two = yes }')[0],'two':a.cw.parse('two = { one = yes }')[0]}
        _,_,_,u=self.resolve('one = yes',e);self.assertIn('CYCLE:one',u)
    def test_conditional_grant_not_certified_as_initial(self):
        g,c,_,_=self.resolve('if = { limit = { is_player = yes } add_technology_researched = shaft_mining }')
        self.assertFalse(g);self.assertEqual(c,{'shaft_mining'})
    def test_comment_cannot_be_mistaken_for_grant(self):
        g,_,_,_=self.resolve('# add_technology_researched = railways\nadd_technology_researched = shaft_mining');self.assertEqual(g,{'shaft_mining'})
    def test_sibling_country_scopes_not_mixed(self):
        root=a.cw.parse('COUNTRIES = { c:AAA ?= { add_technology_researched = shaft_mining } c:BBB ?= { add_technology_researched = railways } }')[0]
        g,_,_,_=a.resolve(root.children()[0].children(),self.effects,self.techs);self.assertEqual(g,{'shaft_mining'})
    def test_descriptor_replaces_vanilla_technology_catalog(self):self.assertTrue(all(p.startswith('MOD:') for p in self.after['tech_sources'].values()))
    def test_only_seven_old_alloy_debts_remain(self):
        self.assertEqual(a.graph_debts(self.after),{(t,'alloysworking','coke_smelting') for t in ['AUS','BEO','FRA','PRU','RUS','SAX','SWE']})
    def test_new_unknown_debt_does_not_fit_exception(self):
        r=copy.deepcopy(self.after);r['starts']['BGT']['technologies'].append('precision_boring')
        self.assertTrue(a.graph_debts(r)-a.graph_debts(self.after))
    def test_eight_country_overlay_changes_only_knowledge(self):
        root=a.cw.parse((a.ROOT/a.OVERLAY_FILE).read_text())[0];self.assertEqual({n.key[2:] for n in root.children()},set(a.ASSIGNMENTS))
        for n in root.children():self.assertEqual([(c.key,c.value) for c in n.children()],[(a.ASSIGNMENTS[n.key[2:]],'yes')])
    def test_current_native_mine_uses_neutral_data_method(self):
        raw=(a.ROOT/a.SALT_HISTORY).read_text();self.assertIn('"pm_1776_no_raw_data_reporting"',raw);self.assertNotIn('"pm_1776_raw_data_reporting"',raw)
        self.assertIn('building = "building_salt_mine"',raw);self.assertNotIn('berchtesgaden_saline',raw)
    def test_no_bgt_or_liege_remaining_mine_gate_conflict(self):self.assertFalse(any(c['TAG'] in ['BGT','LGE'] and c['Building'] in ['building_salt_mine','building_coal_mine'] for c in self.after['conflicts']))
    def test_bgt_has_discovered_salt_resource_without_granting_geology(self):
        regions,_,_=a.objects('map_data/state_regions');r=regions['STATE_TYROL']
        self.assertEqual(sum(int(a.val(n,'discovered_amount','0')) for n in r.children('resource') if a.val(n,'type')=='building_salt_mine'),18)
        self.assertNotIn('geological_surveying',self.after['starts']['BGT']['technologies'])
    def test_no_new_human_or_territorial_approval(self):
        self.assertEqual(a.load(a.rm.OUT/'ROADMAP_STATE.json'),self.base['serg_state']);self.assertEqual(a.rm.check()['status'],'PASS')
        self.assertIsNone(a.load(a.OUT/'FILES_MODIFIED.json')['human_validation'])
    def test_population_and_regensburg_unmodified(self):
        inv=a.load(a.OUT/'SESSION_AFTER_STATIC.json')['inventory'];self.assertEqual(inv['regional_pop'],self.base['inventory']['regional_pop'])
        self.assertEqual(sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='RCI'),11000)

if __name__=='__main__':unittest.main()
