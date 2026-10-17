"""Negative tests: cumulative approvals must not waive unrelated preservation."""
import unittest
import json
from map2l_registry import expected_country_definitions,rebind_state_definitions,expected_locator_rgb,reviewed_core_exception_owner
from pathlib import Path
from unittest.mock import patch

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

    def tier_case(self):
        before=json.dumps(['WUR','=',[['tier','=','kingdom'],['capital','=','STATE_WURTTEMBERG']]],separators=(',',':'))
        after=before.replace('kingdom','principality')
        change=dict(tag='WUR',before='kingdom',after='principality',before_signature=before,after_signature=after)
        return before,after,dict(new_members=[],country_tier_corrections=[change])

    def test_exact_wur_duchy_tier_correction(self):
        before,after,migration=self.tier_case()
        self.assertEqual(expected_country_definitions({'WUR':before},[migration]),{'WUR':after})

    def test_tier_correction_cannot_change_capital(self):
        before,_,migration=self.tier_case()
        migration['country_tier_corrections'][0]['after_signature']=migration['country_tier_corrections'][0]['after_signature'].replace('STATE_WURTTEMBERG','STATE_BAVARIA')
        with self.assertRaises(AssertionError):expected_country_definitions({'WUR':before},[migration])

    def test_tier_correction_cannot_target_another_country(self):
        before,_,migration=self.tier_case();migration['country_tier_corrections'][0]['tag']='PRU'
        with self.assertRaises(AssertionError):expected_country_definitions({'WUR':before},[migration])

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

    def test_exact_locator_binding_not_global_waiver(self):
        folder=Path('test-migration');migration=self.migration();migration['region_reference_changes'][0]['pixel']=[20,30]
        with patch.object(Path,'read_text',return_value=json.dumps(migration)):
            self.assertEqual(expected_locator_rgb(0x1DD141,(20,30),[folder]),0xEDA900)
            self.assertEqual(expected_locator_rgb(0x1DD141,(20,31),[folder]),0x1DD141)
            with self.assertRaises(AssertionError):expected_locator_rgb(0x218061,(20,30),[folder])

    def test_locator_rebinding_chain_requires_exact_prior_bitmap_rgb(self):
        first=Path('first');second=Path('second');a=self.migration();a['region_reference_changes'][0]['pixel']=[20,30]
        b=self.migration(before='xEDA900',after='xEDAF00');b['region_reference_changes'][0]['pixel']=[20,30]
        contents={first/'REGISTRY_MIGRATION.json':json.dumps(a),second/'REGISTRY_MIGRATION.json':json.dumps(b)}
        with patch.object(Path,'read_text',autospec=True,side_effect=lambda path:contents[path]):
            self.assertEqual(expected_locator_rgb(0x1DD141,(20,30),[first,second]),0xEDAF00)
            with self.assertRaises(AssertionError):expected_locator_rgb(0x1DD141,(20,30),[second,first])

    def test_core_exception_cannot_move_to_a_different_pixel(self):
        folder=Path('SWABIA_COMPLETION');data={'core_exceptions':[dict(preceding_lot='SWABIA',rgb='xEDAD0D',previous_owner='SKE',new_owner='SKI',cells=[[4324,929]])]}
        with patch.object(Path,'read_text',return_value=json.dumps(data)):
            with self.assertRaises(AssertionError):reviewed_core_exception_owner((4324,929),'SKE',[folder])

    def test_core_exception_cannot_replace_another_country(self):
        folder=Path('SWABIA_COMPLETION');data={'core_exceptions':[dict(preceding_lot='SWABIA',rgb='xEDAD0D',previous_owner='SKE',new_owner='SAC',cells=[[4324,928]])]}
        with patch.object(Path,'read_text',return_value=json.dumps(data)):
            with self.assertRaises(AssertionError):reviewed_core_exception_owner((4324,928),'SKE',[folder])

    def test_exact_core_exception_is_not_a_whole_abbey_waiver(self):
        folder=Path('SWABIA_COMPLETION');data={'core_exceptions':[dict(preceding_lot='SWABIA',rgb='xEDAD0D',previous_owner='SKE',new_owner='SKI',cells=[[4324,928]])]};geo={'assignments':[dict(owner='SKI',parent_rgb='xEDAD0D',previous_owner='SKE',pixels=1,cells=[[4324,928]])]}
        contents={folder/'REGISTRY_MIGRATION.json':json.dumps(data),folder/'GEOMETRY.json':json.dumps(geo)}
        with patch.object(Path,'read_text',autospec=True,side_effect=lambda path:contents[path]):
            self.assertEqual(reviewed_core_exception_owner((4324,928),'SKE',[folder]),'SKI')
            self.assertEqual(reviewed_core_exception_owner((4324,929),'SKE',[folder]),'SKE')
            with self.assertRaises(AssertionError):reviewed_core_exception_owner((4324,928),'SAG',[folder])


if __name__=='__main__':unittest.main()
