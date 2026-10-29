"""Regression tests for interpretation, not a synthetic claim of engine validation."""
import unittest
from audit_arable_population_1776 import *

class CapacityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=Catalog()

 def test_agra_split_land(self):
  self.assertEqual(share_land(483,34,37),444)
  self.assertEqual(share_land(483,3,37),39)

 def test_prime_land_and_impassable_are_not_equal_provinces(self):
  region=parse('s={provinces={x000001 x000002 x000003} prime_land={x000002} impassable={x000003}}')[0]
  self.assertEqual(land_weights(region,['x000001'],5),(1,6))
  self.assertEqual(land_weights(region,['x000002'],5),(5,6))
  self.assertEqual(land_weights(region,['x000003'],5),(0,6))
  self.assertEqual(share_land(60,*land_weights(region,['x000002'],5)),50)

 def test_impassable_only_has_zero_land_not_equal_share(self):
  region=parse('s={provinces={a b} impassable={a b}}')[0]
  self.assertEqual(land_weights(region,['a'],5),(0,0))

 def test_inhabitants_are_not_all_workers(self):
  self.assertEqual(pressure(100000,30000,.30),0)
  self.assertEqual(pressure(100000,30000,.35),5000)

 def test_rice_employment_uses_effective_native_definition(self):
  cap=self.c.capacity('building_subsistence_rice_farm',[])
  self.assertEqual(cap['jobs_min'],10000)
  self.assertEqual(cap['jobs_max'],10000)
  self.assertEqual(cap['jobs_max']*444,4440000)

 def test_standard_subsistence_is_not_rice(self):
  self.assertEqual(self.c.capacity('building_subsistence_farm',[])['jobs_max'],5000)

 def test_rural_group_inheritance_and_industry(self):
  self.assertTrue(self.c.is_rural('building_wheat_farm'))
  self.assertTrue(self.c.is_rural('building_cotton_plantation'))
  self.assertFalse(self.c.is_rural('building_logging_camp'))
  self.assertFalse(self.c.is_rural('building_textile_mill'))

 def test_do_not_double_count_ownership_levels(self):
  n=parse('create_building = { level = 2 add_ownership = { country = { levels = 2 } } }')[0]
  self.assertEqual(declared_levels(n),(2,'explicit_level'))
  n=parse('create_building = { add_ownership = { country = { levels = 2 } building = { levels = 3 } } }')[0]
  self.assertEqual(declared_levels(n),(5,'ownership_levels'))

 def test_missing_level_is_not_silently_one(self):
  self.assertIsNone(declared_levels(parse('create_building = { building = x }')[0])[0])

 def test_unknown_pm_is_not_a_known_zero_capacity(self):
  cap=self.c.capacity('building_subsistence_rice_farm',['pm_unknown_test_fixture'])
  self.assertIn('unassigned_pm:pm_unknown_test_fixture',cap['unknown'])

 def test_automation_offsets_base_before_clamping(self):
  c=object.__new__(Catalog)
  c.buildings={'b':parse('b={production_method_groups={g1 g2}}')[0]}
  c.pmgs={n.key:n for n in parse('g1={production_methods={base}} g2={production_methods={auto}}')}
  c.pms={n.key:n for n in parse('base={building_modifiers={level_scaled={building_employment_laborers_add=5000}}} auto={building_modifiers={level_scaled={building_employment_laborers_add=-2000 building_employment_engineers_add=500}}}')}
  self.assertEqual(c.capacity('b',[])['jobs_max'],3500)

 def test_effective_famine_thresholds(self):
  t=food_thresholds()
  self.assertEqual(t['starvation'],.4)
  self.assertEqual(t['severe'],.2)
  self.assertEqual(t['famine_starving_share'],.35)
  self.assertEqual(t['famine_severe_share'],.15)
  self.assertFalse(.98>=t['famine_starving_share'] and .10>=t['famine_severe_share'])
  self.assertTrue(.98>=t['famine_starving_share'] and .36>=t['famine_severe_share'])

 def test_grain_output_and_employment_are_separate(self):
  cap=self.c.capacity('building_wheat_farm',[])
  self.assertGreater(cap['grain_max'],cap['grain_min'])
  self.assertGreater(cap['jobs_max'],0)

 def test_worker_rounding_does_not_hide_wrong_land_measurement(self):
  from types import SimpleNamespace
  n=dict(sha256='test',date='1776.1.1',states=[dict(state='STATE_AGRA',owner='MARATH',arable_land=39,famine_active=False,starving_pct=None,mild_starving_pct=None,severe_starving_pct=None)])
  obs=dict(native_save_sha256='test',date='1776.1.1',observations=[dict(state='STATE_AGRA',owner='MARATH',arable_land=444,rounding_tolerance=5000)])
  p=SimpleNamespace(read_text=lambda **kwargs:json.dumps(obs))
  with self.assertRaises(ValueError):merge_observations(n,p,food_thresholds())

if __name__=='__main__':unittest.main()
