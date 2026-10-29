import unittest
from stabilize_arable_population_1776 import required_land,minimum_region_land,apportion,compatible_communities,canonical_profile
from audit_arable_population_1776 import parse

class StabilizationTests(unittest.TestCase):
 def test_workforce_not_total_population(self):
  self.assertEqual(required_land(300000,50000,10,5000),60)
 def test_rice_and_standard_employment_differ(self):
  self.assertEqual(required_land(100001,0,0,10000),11)
  self.assertEqual(required_land(100001,0,0,5000),21)
 def test_commercial_farms_consume_land_and_provide_jobs(self):
  self.assertEqual(required_land(100000,25000,5,5000),20)
 def test_split_region_floor_safety(self):
  self.assertEqual(minimum_region_land(10,1,3,20),30)
  self.assertIsNone(minimum_region_land(10,0,3,20))
 def test_never_reduce_existing_arable(self):
  self.assertEqual(minimum_region_land(10,1,1,764),764)
 def test_proportional_transfer_conserves_and_cannot_go_negative(self):
  self.assertEqual(apportion(7,[2,3,5]),[1,2,4])
  self.assertEqual(apportion(10,[2,3,5]),[2,3,5])
  with self.assertRaises(ValueError):apportion(11,[2,3,5])
 def test_canadian_population_cannot_leak_to_another_pool(self):
  def r(tag,culture):return dict(owner=tag,country_type='decentralized',profiles={culture})
  self.assertFalse(compatible_communities(r('H06','algonquian'),r('INI','algonquian')))
  self.assertTrue(compatible_communities(r('H06','algonquian'),r('H02','cree')))
  self.assertTrue(compatible_communities(r('X','a'),r('Y','a')))
  self.assertFalse(compatible_communities(r('X','a'),r('Y','b')))
 def test_resolve_implicit_religion_before_cross_country_move(self):
  node=parse('create_pop={culture=cree size=10}')[0]
  self.assertEqual(dict(canonical_profile(node,{'cree':'animist'})),dict(culture='cree',religion='animist'))
  node=parse('create_pop={culture=cree religion=catholic pop_type=slaves size=10}')[0]
  self.assertEqual(dict(canonical_profile(node,{'cree':'animist'}))['religion'],'catholic')

if __name__=='__main__':unittest.main()
