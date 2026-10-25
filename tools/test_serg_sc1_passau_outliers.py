"""Scoped safeguards for the new Obernberg enclave and pending ordinary salt mine."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc1_passau_outliers as lot

class PassauOutlierContracts(unittest.TestCase):
    def reject(self,name,mutate):
        p=lot.OUT/name;data=lot.load(p);mutate(data);reader=Path.read_text
        with patch.object(Path,'read_text',autospec=True,side_effect=lambda fp,*a,**kw:json.dumps(data) if fp==p else reader(fp,*a,**kw)):
            with self.assertRaises(AssertionError):lot.reg.approved_lot_dirs()
    def test_no_new_member_or_second_passau(self):self.reject('REGISTRY_MIGRATION.json',lambda m:m['new_members'].append('PAS'))
    def test_no_entire_innviertel_transfer(self):self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['rgb']==lot.PARENT).update(owner='PAS'))
    def test_no_salzburg_or_old_passau_cell_absorbed(self):self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='PAS')['cells'].append([4400,900]))
    def test_no_alternative_parent(self):self.reject('GEOMETRY.json',lambda g:g.update(parents=['xB08021']))
    def test_no_hub_rebinding(self):self.reject('REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'].append(dict(state=lot.SID,field='city',after=lot.RGB)))
    def test_no_new_extent(self):self.reject('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4393,911]))
    def test_no_free_city(self):self.reject('REGISTRY_MIGRATION.json',lambda m:m.update(free_cities=['PAS']))
    def test_no_cadastral_claim(self):self.reject('GEOMETRY.json',lambda g:g.update(historical_cadastral_precision=True))
    def test_no_whole_parent_imperial_title(self):self.reject('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']==lot.PARENT).update(beneficiary='PAS'))
    def test_current_tail(self):self.assertEqual(lot.reg.approved_lot_dirs()[-2:],[lot.prior.OUT,lot.OUT])
    def test_national_capital_not_moved(self):self.assertEqual(lot.prior.italian.definitions('common/country_definitions')['PAS'].one('capital'),'STATE_BAVARIA')
    def test_ordinary_berchtesgaden_mine_preserved(self):
        raw=(lot.ROOT/'common/history/buildings/1776_sc1_berchtesgaden.txt').read_text('utf8');self.assertIn('building = "building_salt_mine"',raw);self.assertNotIn('berchtesgaden_saline',raw);self.assertFalse((lot.ROOT/'common/building_groups/1776_sc1_berchtesgaden_salt.txt').exists())
    def test_no_fabricated_acceptance_or_regional_credit(self):
        s=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');self.assertEqual(lot.rm.progress(s)['earned_weight'],82)
        for id in [lot.TASK,lot.prior.TASK]:
            t=next(t for t in s['tasks'] if t['id']==id);self.assertIsNone(t['runtime_validation']['attestation'])
        self.assertFalse(list(lot.OUT.glob('RUNTIME_USER_ATTESTATION*')))
    def test_new_population_is_market_not_entire_parish(self):
        demo=lot.load(lot.OUT/'DEMOGRAPHY.json');self.assertEqual(demo['transferred'],1400);self.assertFalse(demo['population_per_pixel']);self.assertEqual(demo['old_passau_core_unchanged'],14267)

if __name__=='__main__':unittest.main()
