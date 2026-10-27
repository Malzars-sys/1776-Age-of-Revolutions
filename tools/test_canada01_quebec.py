"""Prevent a colonial merger from silently converting different economic assets."""
import unittest
from canada01_quebec import normalized,parse


def building(owner='ONT',pm='pm_no_organization',reserves=1):
    return parse(f'create_building = {{ building = building_barrack add_ownership = {{ country = {{ country = c:{owner} levels = 5 }} }} reserves = {reserves} activate_production_methods = {{ {pm} }} }}')[0]


class ConsolidationGuard(unittest.TestCase):
    def test_successor_public_owner_only(self):self.assertEqual(normalized(building('ONT')),normalized(building('QUE')))
    def test_foreign_economic_owner_is_protected(self):self.assertNotEqual(normalized(building('GBR')),normalized(building('QUE')))
    def test_different_pm_cannot_be_discarded(self):self.assertNotEqual(normalized(building(pm='pm_other')),normalized(building('QUE')))
    def test_different_reserve_cannot_be_discarded(self):self.assertNotEqual(normalized(building(reserves=2)),normalized(building('QUE')))


if __name__=='__main__':unittest.main()
