"""Bounded Brixen core, cumulative preservation and genuine receipt scope."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import serg_sc1_brixen as lot

class BrixenContracts(unittest.TestCase):
    def reject(self,name,mutate):
        path=lot.OUT/name;data=lot.load(path);mutate(data);reader=Path.read_text
        def read(fp,*a,**kw):return json.dumps(data) if fp==path else reader(fp,*a,**kw)
        with patch.object(Path,'read_text',autospec=True,side_effect=read):
            with self.assertRaises(AssertionError):lot.reg.approved_lot_dirs()

    def test_reject_bolzano_annexation(self):
        self.reject('GEOMETRY.json',lambda g:next(r for r in g['assignments'] if r['owner']=='BRX')['cells'].append([4358,957]))
    def test_reject_puster_or_lienz_parent(self):
        self.reject('GEOMETRY.json',lambda g:g.update(parents=['xF0E0C0']))
    def test_reject_whole_austrian_parent_right(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']==lot.PARENT).update(beneficiary='BRX'))
    def test_reject_trento_title_reassignment(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:next(r for r in m['updated'] if r['rgb']==lot.prior.RGB).update(beneficiary='BRX'))
    def test_reject_trento_hub_rebinding(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['region_reference_changes'].append(dict(state=lot.SID,field='city',before=lot.prior.RGB,after=lot.RGB,pixel=[4352,973])))
    def test_reject_cadastral_claim(self):
        self.reject('GEOMETRY.json',lambda g:g.update(historical_cadastral_precision=True))
    def test_reject_free_city(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m.update(free_cities=['BRX']))
    def test_reject_added_imperial_extent(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['extent_added_cells'].append([4363,949]))
    def test_reject_other_member(self):
        self.reject('REGISTRY_MIGRATION.json',lambda m:m['new_members'].append('BRI'))
    def test_current_cumulative_tail(self):
        self.assertEqual(lot.reg.approved_lot_dirs()[-4:],[lot.rm.OUT/'SC1-SALZBURG',lot.prior.prior.OUT,lot.prior.OUT,lot.OUT])
    def test_trento_user_receipt_is_partial(self):
        s=lot.load(lot.OUT/'BASELINE.json')['roadmap'];t=next(t for t in s['tasks'] if t['id']=='SC1-TRENTO')
        self.assertEqual(t['status'],'BLOCKED');self.assertTrue(lot.rm.partial_runtime_evidence(t))
        self.assertFalse(lot.rm.terminal_evidence(dict(t,status='PASS_RUNTIME_USER_VALIDATED'),s))
        r=lot.load(lot.prior.OUT/'RUNTIME_USER_ATTESTATION_2026_10_23.json')
        self.assertEqual(r['sub_lot_ids'],['TR-I-CORE']);self.assertIsNone(r['actual_test_date']);self.assertFalse(r['regional_closure_approved'])
        self.assertEqual(lot.rm.progress(s)['earned_weight'],82)
    def test_no_brixen_human_receipt_no_credit(self):
        s=copy.deepcopy(lot.load(lot.OUT/'BASELINE.json')['roadmap']);t=next(t for t in s['tasks'] if t['id']==lot.TASK);t['status']='PASS_RUNTIME_USER_VALIDATED'
        self.assertFalse(lot.rm.terminal_evidence(t,s));self.assertFalse(list(lot.OUT.glob('RUNTIME_USER_ATTESTATION*')));self.assertEqual(lot.rm.progress(s)['earned_weight'],82)
    def test_all_old_hubs_and_trento_city_reference_retained(self):
        f=lot.load(lot.OUT/'EXPECTED_TEXT.json')['map_data/state_regions/00_west_europe.txt'];old=lot.load(lot.OUT/'TEXT_BEFORE.json')['map_data/state_regions/00_west_europe.txt']
        nodes=lambda r:next(n for n in lot.core.cw.parse(r.lstrip('\ufeff')) if n.key==lot.SID)
        self.assertEqual([lot.core.qa.signature(n) for n in nodes(f).children() if n.key!='provinces'],[lot.core.qa.signature(n) for n in nodes(old).children() if n.key!='provinces'])
        self.assertEqual(lot.core.cw.scalar(nodes(f).one('city')),lot.prior.RGB)
    def test_small_court_does_not_inflate_population(self):
        d=lot.load(lot.OUT/'DEMOGRAPHY.json');self.assertEqual(d['transferred'],3000);self.assertEqual(d['court_capacity'],200)
        pm=lot.load(lot.OUT/'EXPECTED_TEXT.json')['common/production_methods/1776_sc1_brixen.txt'];n=lot.core.cw.parse(pm)[0].children('building_modifiers')[0].children('level_scaled')[0]
        self.assertEqual(sum(int(v.value) for v in n.children()),200)
        self.assertLess(200,3000*.25)
    def test_names_only_brixen_state_owner_scope(self):
        names=lot.load(lot.OUT/'EXPECTED_TEXT.json')['common/scripted_effects/1776_sc1_brixen.txt'];n=lot.core.cw.parse(names)[0].children('if')[0];limit=n.children('limit')[0]
        self.assertEqual(limit.one('state_region'),'s:STATE_SOUTH_TYROL');self.assertEqual(limit.children('owner')[0].children()[0].key,'c:BRX');self.assertEqual(limit.children('owner')[0].children()[0].op,'?=')
    def test_tyrol_remains_dependent_and_unstarted(self):
        s=lot.load(lot.rm.OUT/'ROADMAP_STATE.json');tyrol=next(t for t in s['tasks'] if t['id']=='SC2-TYROL')
        self.assertEqual(set(tyrol['depends_on']),{'SC1-TRENTO','SC1-BRIXEN'});self.assertEqual(tyrol['status'],'NOT_STARTED')

if __name__=='__main__':unittest.main()
