"""Live population boundaries and negative cases; never manufacture engine results."""
import copy,unittest
import serg_sc1_regensburg_demography as lot

class RegensburgDemography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=lot.load(lot.OUT/'BASELINE.json');cls.v=lot.load(lot.OUT/'SESSION_AFTER_STATIC.json')['inventory']
        cls.old=lot.load(lot.OUT/'TEXT_BEFORE.json')[lot.REL]
        cls.raw=(lot.ROOT/lot.REL).read_text(encoding='utf-8-sig')
    def test_city_is_municipal_scope_not_all_urban_population(self):
        self.assertEqual(sum(r['count'] for r in self.v['regional_pop'] if r['key'][1]=='RCI'),11000)
        self.assertNotEqual(11000,22000)
    def test_effective_religions_not_government_conversion(self):
        p=lot.core.region(self.raw,lot.SID,'RCI').children('create_pop')
        self.assertEqual([(n.one('culture'),n.one('religion'),int(n.one('size'))) for n in p],[('south_german',None,4998),('south_german','protestant',6000),('ashkenazi',None,2)])
    def test_bishop_population_untouched_not_city_catholics(self):
        self.assertEqual(lot.core.qa.signature(lot.core.region(self.old,lot.SID,'RBI')),lot.core.qa.signature(lot.core.region(self.raw,lot.SID,'RBI')))
    def test_no_compensation_in_bavaria_or_another_owner(self):
        self.assertEqual([r for r in self.v['regional_pop'] if r['key'][1]!='RCI'],[r for r in self.b['inventory']['regional_pop'] if r['key'][1]!='RCI'])
    def test_world_increase_is_declared(self):
        self.assertEqual(sum(r['count'] for r in self.v['pops'])-sum(r['count'] for r in self.b['inventory']['pops']),10287)
    def test_no_professions_fabricated(self):
        for p in lot.core.region(self.raw,lot.SID,'RCI').children('create_pop'):
            self.assertTrue(set(n.key for n in p.children())<={'culture','religion','size'})
    def test_no_building_or_army_change(self):
        for k in ['buildings','building_levels_written','units']:self.assertEqual(self.v[k],self.b['inventory'][k])
    def test_no_sovereignty_or_capital_change(self):
        for k in ['owners','geometry','states','state_types','countries']:self.assertEqual(self.v[k],self.b['inventory'][k])
    def test_wrong_population_source_rejected(self):
        with self.assertRaises(AssertionError):lot.transform(self.old.replace('size = 696','size = 697'))
    def test_wrong_religion_rejected(self):
        node=lot.core.region(self.old,lot.SID,'RCI');chunk=self.old[node.start:node.end].replace('religion = protestant','religion = catholic')
        with self.assertRaises(AssertionError):lot.transform(self.old[:node.start]+chunk+self.old[node.end:])
    def test_missing_city_owner_rejected(self):
        with self.assertRaises((AssertionError,StopIteration)):lot.transform(self.old.replace('region_state:RCI','region_state:NOT_RCI'))
    def test_extra_population_group_rejected(self):
        node=lot.core.region(self.old,lot.SID,'RCI')
        raw=self.old[:node.end-1]+'create_pop = { culture = french size = 100 }'+self.old[node.end-1:]
        with self.assertRaises(AssertionError):lot.transform(raw)
    def test_shared_file_concurrent_unrelated_change_preserved(self):
        changed=self.old+'\n# unrelated concurrent annotation\n'
        self.assertTrue(lot.transform(changed).endswith('# unrelated concurrent annotation\n'))
    def test_same_update_cannot_be_applied_twice(self):
        with self.assertRaises(AssertionError):lot.transform(self.raw)
    def test_old_receipts_do_not_approve_this_demography(self):
        s=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');t=next(t for t in s['tasks'] if t['id']==lot.TASK)
        self.assertIsNone(t['runtime_validation']['attestation']);self.assertFalse(lot.rm.qualifications(s)[lot.TASK])
    def test_current_registry_tail_and_nine_electors(self):
        from map2k_patch import ELECTORS
        self.assertEqual(lot.load(lot.reg.active_registry_path()),self.b['registry'])
        self.assertEqual(len(ELECTORS),9)

if __name__=='__main__':unittest.main()
