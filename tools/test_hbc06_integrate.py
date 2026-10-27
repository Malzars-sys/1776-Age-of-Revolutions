"""Negative guards for politically wrong, missing, conflicting or wrong-State RGBs."""
import unittest
from hbc06_integrate import targets_match


class OwnershipGuard(unittest.TestCase):
    def check(self,actual):
        return targets_match(actual,{'x123456':'H01'},lambda _: {('STATE_MANITOBA','HBC')})

    def test_correct_transfer(self):self.assertTrue(self.check({'x123456':{('STATE_MANITOBA','H01')}}))
    def test_missing_owner(self):self.assertFalse(self.check({}))
    def test_wrong_country(self):self.assertFalse(self.check({'x123456':{('STATE_MANITOBA','HBC')}}))
    def test_two_owners(self):self.assertFalse(self.check({'x123456':{('STATE_MANITOBA','H01'),('STATE_MANITOBA','HBC')}}))
    def test_wrong_state(self):self.assertFalse(self.check({'x123456':{('STATE_ONTARIO','H01')}}))


if __name__=='__main__':unittest.main()
