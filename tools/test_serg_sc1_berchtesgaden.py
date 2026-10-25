"""Bound the new sovereign core and preserve genuine partial receipts."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc1_berchtesgaden as lot

class BerchtesgadenContracts(unittest.TestCase):
    def reject(self,name,mutate):
        p=lot.OUT/name;data=lot.load(p);mutate(data);reader=Path.read_text
        def read(fp,*a,**kw):return json.dumps(data) if fp==p else reader(fp,*a,**kw)
        with patch.object(Path,'read_text',autospec=True,side_effect=read):
            with self.assertRaises(AssertionError):lot.reg.approved_lot_dirs()
    def test_reject_salzburg_absorption(self):
        self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='BGT')['cells'].append([4386,925]))
    def test_reject_bavarian_parent_substitution(self):
        self.reject('GEOMETRY.json',lambda g:g.update(parents=['x6EA29B']))
    def test_reject_entire_tyrolean_parent_title(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']==lot.PARENT).update(beneficiary='BGT'))
    def test_reject_free_city(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m.update(free_cities=['BGT']))
    def test_reject_hub_rebinding(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'].append(dict(state=lot.SID,field='farm',before='x5D4166',after=lot.RGB,pixel=[4395,928])))
    def test_reject_added_imperial_extent(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4384,930]))
    def test_reject_cadastral_claim(self):
        self.reject('GEOMETRY.json',lambda g:g.update(historical_cadastral_precision=True))
    def test_reject_wrong_member(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['new_members'].append('BRG'))
    def test_current_cumulative_tail(self):
        self.assertEqual(lot.reg.approved_lot_dirs()[-5:],[lot.rm.OUT/'SC1-SALZBURG',lot.rm.OUT/'SC4-MASSA-CARRARA',lot.rm.OUT/'SC1-TRENTO',lot.prior.OUT,lot.OUT])
    def test_brixen_receipt_is_real_and_partial(self):
        s=lot.load(lot.OUT/'BASELINE.json')['roadmap'];t=next(t for t in s['tasks'] if t['id']=='SC1-BRIXEN');r=lot.load(lot.prior.OUT/'RUNTIME_USER_ATTESTATION_2026_10_23.json')
        self.assertEqual(t['status'],'BLOCKED');self.assertEqual(t['priority'],'P1');self.assertTrue(lot.rm.partial_runtime_evidence(t));self.assertFalse(lot.rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),s));self.assertEqual(r['sub_lot_ids'],['BR-I-CORE']);self.assertIsNone(r['actual_test_date']);self.assertFalse(r['regional_closure_approved']);self.assertEqual(len(t['remaining_territorial_obligations']),5)
    def test_pending_new_core_gains_no_credit(self):
        s=copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap']);t=next(t for t in s['tasks'] if t['id']==lot.TASK);t['status']='PASS_RUNTIME_USER_VALIDATED';self.assertFalse(lot.rm.terminal_evidence(t,s));self.assertEqual(lot.rm.progress(s)['earned_weight'],82);self.assertFalse(list(lot.OUT.glob('RUNTIME_USER_ATTESTATION*')))
    def test_small_inland_saline_not_full_mine_or_port(self):
        f=lot.load(lot.OUT/'EXPECTED_TEXT.json');nodes=lot.core.cw.parse(f['common/buildings/1776_sc1_berchtesgaden.txt']);self.assertEqual(nodes[1].one('city_type'),'city');self.assertEqual(nodes[1].one('building_group'),'bg_light_industry');self.assertEqual(nodes[1].one('expandable'),'no')
        pms=lot.core.cw.parse(f['common/production_methods/1776_sc1_berchtesgaden.txt']);jobs=[sum(int(v.value) for v in p.children('building_modifiers')[0].children('level_scaled')[0].children()) for p in pms];self.assertEqual(jobs,[100,100]);self.assertLess(sum(jobs),lot.POP*.25)
    def test_no_copied_pact_or_artificial_technology(self):
        f=lot.load(lot.OUT/'EXPECTED_TEXT.json');self.assertFalse(any(p.startswith('common/history/treaties/') for p in f));self.assertNotIn('add_technology_researched',f['common/history/countries/bgt - berchtesgaden.txt'])
    def test_names_scoped_to_berchtesgaden_only(self):
        f=lot.load(lot.OUT/'EXPECTED_TEXT.json');n=lot.core.cw.parse(f['common/scripted_effects/1776_sc1_berchtesgaden.txt'])[0].children('if')[0].children('limit')[0];self.assertEqual(n.one('state_region'),'s:STATE_TYROL');self.assertEqual(n.children('owner')[0].children()[0].key,'c:BGT')
    def test_no_earlier_capital_or_resource_reference_changed(self):
        p='map_data/state_regions/00_west_europe.txt';old=lot.load(lot.OUT/'TEXT_BEFORE.json')[p];new=lot.load(lot.OUT/'EXPECTED_TEXT.json')[p];node=lambda r:next(n for n in lot.core.cw.parse(r.lstrip('\ufeff')) if n.key==lot.SID)
        self.assertEqual([lot.core.qa.signature(n) for n in node(old).children() if n.key!='provinces'],[lot.core.qa.signature(n) for n in node(new).children() if n.key!='provinces'])
    def test_tyrol_still_depends_on_both_unclosed_regions(self):
        s=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');t=next(t for t in s['tasks'] if t['id']=='SC2-TYROL');self.assertEqual(set(t['depends_on']),{'SC1-TRENTO','SC1-BRIXEN'});self.assertEqual(t['status'],'NOT_STARTED')

if __name__=='__main__':unittest.main()
