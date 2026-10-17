"""Narrow allocation and full-staff sizing regression tests."""
import collections as C
import unittest
import start_buildings_2026_10_15 as addon
import british_infrastructure_2026_10_15 as roads

class EconomyTests(unittest.TestCase):
    def context(self,**extra):
        row=dict(fixed_add=3,road_add=7,fixed_pop_add=0,road_pop_add=0,fixed_pop_max=0,road_pop_max=0,population=1000000,population_divisor=100000,mult=0,target_capacity=23)
        row.update(extra);return row

    def test_minimum_full_staff_levels(self):
        row=self.context();self.assertEqual(roads.minimum_levels(row),3)
        self.assertEqual(roads.capacity(row,3),24)
        self.assertLess(roads.capacity(row,2),row['target_capacity'])

    def test_population_cap_applies(self):
        row=self.context(population=100000000,road_pop_add=.02,road_pop_max=.5)
        self.assertEqual(roads.capacity(row,2),18)

    def test_negative_regional_modifier_not_dropped(self):
        self.assertAlmostEqual(roads.capacity(self.context(mult=-.1),1),9)

    def test_exact_three_canal_states(self):
        self.assertEqual(roads.CANALS,{'STATE_LANCASHIRE','STATE_MIDLANDS','STATE_YORKSHIRE'})
        for sid in roads.HOME:
            self.assertEqual('pm_industrial_canals' in roads.network_pms(sid),sid in roads.CANALS)
            self.assertEqual('pm_no_canal_network' in roads.network_pms(sid),sid not in roads.CANALS)

    def test_user_building_totals(self):
        counts=C.Counter()
        for sid,tag,kind,n in addon.PLAN:counts[kind]+=n
        self.assertEqual(dict(counts),addon.DELTAS)
        self.assertEqual(sum(counts.values()),80)

    def test_all_chinese_glassworks_have_porcelain_and_unlocked_methods(self):
        for sid,tag,kind,n in addon.PLAN:
            if kind!='building_glassworks':continue
            self.assertEqual(tag,'CHI')
            methods=addon.new_recipes(kind,tag)
            self.assertIn('pm_ceramics',methods)
            self.assertIn('pm_1776_no_raw_data_reporting',methods)
            self.assertNotIn('pm_disabled_ceramics',methods)

    def test_irish_deficit_coverage_without_new_technology(self):
        self.assertEqual(sum(roads.IRISH_ADD.values()),15)
        self.assertGreaterEqual(15*10,128+20)
        self.assertIn('pm_professional_bureaucrats',roads.irish_pms())
        self.assertNotIn('pm_hereditary_bureaucrats',roads.irish_pms())

    def test_scope_excludes_colonies(self):
        self.assertEqual(len(roads.HOME),13)
        self.assertNotIn('STATE_JAMAICA',roads.HOME)
        self.assertNotIn('STATE_NEWFOUNDLAND',roads.HOME)

if __name__=='__main__':unittest.main()
