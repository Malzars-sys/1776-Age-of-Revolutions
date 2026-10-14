"""Negative tests: cumulative approvals must not waive unrelated preservation."""
import unittest
from map2l_registry import expected_country_definitions,rebind_state_definitions

REGION='STATE_WESTPHALIA = { id = 61 provinces = { "x1DD141" "x218061" } wood = "x1DD141" prime_land = { "x1DD141" } arable_land = 60 }'


class ExplicitMigrationTests(unittest.TestCase):
    def migration(self,field='wood',before='x1DD141',after='xEDA900'):
        return {'replaced_regions':['STATE_WESTPHALIA'],'new_members':[],
                'region_reference_changes':[{'state':'STATE_WESTPHALIA','field':field,'before':before,'after':after}]}

    def test_no_changes_is_identity(self):
        self.assertEqual(expected_country_definitions({'PRU':'frozen'},[]),{'PRU':'frozen'})
        self.assertEqual(rebind_state_definitions(REGION,[]),REGION)

    def test_only_explicit_exact_country_added(self):
        migration={'new_members':['WPM'],'country_additions':{'WPM':'planned'}}
        self.assertEqual(expected_country_definitions({'PRU':'frozen'},[migration]),{'PRU':'frozen','WPM':'planned'})

    def test_existing_country_never_replaced(self):
        with self.assertRaises(AssertionError):expected_country_definitions({'PRU':'frozen'},[{'new_members':['PRU'],'country_additions':{'PRU':'changed'}}])

    def test_undeclared_country_rejected(self):
        with self.assertRaises(AssertionError):expected_country_definitions({},[{'new_members':[],'country_additions':{'WPM':'planned'}}])

    def test_hub_reference_only_changes_declared_field(self):
        result=rebind_state_definitions(REGION,[self.migration()])
        self.assertEqual(result,REGION.replace('wood = "x1DD141"','wood = "xEDA900"'))
        self.assertIn('id = 61',result);self.assertIn('arable_land = 60',result)

    def test_wrong_input_reference_rejected(self):
        with self.assertRaises(AssertionError):rebind_state_definitions(REGION,[self.migration(before='x218061')])

    def test_resource_or_id_changes_rejected(self):
        for field in ['arable_land','id','capped_resources']:
            with self.assertRaises(AssertionError):rebind_state_definitions(REGION,[self.migration(field=field)])

    def test_out_of_scope_reference_rejected(self):
        migration=self.migration();migration['replaced_regions']=[]
        with self.assertRaises(AssertionError):rebind_state_definitions(REGION,[migration])

    def test_different_region_file_untouched(self):
        raw='STATE_LOMBARDY = { id = 121 wood = "x4713EE" }'
        self.assertEqual(rebind_state_definitions(raw,[self.migration()]),raw)

    def test_prime_land_exact_declared_list(self):
        result=rebind_state_definitions(REGION,[self.migration(field='prime_land',before=['x1DD141'],after=['x1DD141','xEDA900'])])
        self.assertEqual(result,REGION.replace('prime_land = { "x1DD141" }','prime_land = { "x1DD141" "xEDA900" }'))


if __name__=='__main__':unittest.main()
