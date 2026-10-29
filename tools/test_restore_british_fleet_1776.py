import unittest
from collections import Counter
from restore_british_fleet_1776 import allocation,restoration,modernize

class FleetRestorationTests(unittest.TestCase):
 def test_restore_number_without_erasing_later_advanced_ships(self):
  before=[('ship_type_frigate',6),('ship_type_ship_of_the_line',2),('ship_type_caravel',5),('ship_type_galley',9)]
  restored=restoration(before,28)
  self.assertEqual(sum(restored.values()),28)
  self.assertEqual(restored['ship_type_frigate'],6)
  self.assertEqual(restored['ship_type_ship_of_the_line'],2)
 def test_modernization_preserves_total_and_current_roles(self):
  original=[Counter(ship_type_caravel=41,ship_type_galley=63,ship_type_frigate=9,ship_type_ship_of_the_line=7)]
  after,rates=modernize(original)
  self.assertEqual(sum(after[0].values()),120)
  self.assertEqual(after[0]['ship_type_ship_of_the_line'],19)
  self.assertEqual(after[0]['ship_type_frigate'],28)
  self.assertEqual(rates['ship_type_caravel']['converted'],12)
  self.assertEqual(rates['ship_type_galley']['converted'],19)
 def test_small_fleets_do_not_each_round_up_to_excessive_conversion(self):
  original=[Counter(ship_type_caravel=1,ship_type_galley=1) for _ in range(10)]
  after,rates=modernize(original)
  self.assertEqual(sum(r['ship_type_ship_of_the_line'] for r in after),3)
  self.assertEqual(sum(r['ship_type_frigate'] for r in after),3)
  self.assertTrue(all(sum(a.values())==sum(b.values()) for a,b in zip(after,original)))
 def test_restoration_never_reduces_current_ships(self):
  with self.assertRaises(ValueError):restoration([('ship_type_caravel',10)],9)
 def test_allocation_keeps_integer_total(self):
  self.assertEqual(sum(allocation(19,[7,2,2,3,34,13,2])),19)

if __name__=='__main__':unittest.main()
