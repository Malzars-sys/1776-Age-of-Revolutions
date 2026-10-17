"""Cumulative read-only MAP2N regression tests, including the preserved Poel stage."""
import json,unittest
from unittest.mock import patch
import numpy as np
import map2n_completion as m
import map2l_registry as registry

class CompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=m.load('PLAN.json');cls.base=m.load('BASELINE.json');cls.after=m.core.packed(m.ROOT/'map_data/provinces.png')
        cls.before=m.core.packed(m.ROOT/cls.base['bitmap_reference'])

    def test_exact_mainland_patch_and_negative_out_of_scope_edit(self):
        expected=self.before.copy()
        for r in self.plan['changes']:expected[r['Y'],r['X']]=int(r['RGB_after'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after));expected[750,4400]^=1
        self.assertFalse(np.array_equal(expected,self.after))

    def test_historical_sectors_and_no_city_only_neukloster(self):
        rows=self.plan['assignments'];self.assertEqual({r['rgb']:r['pixels'] for r in rows},{m.WISMAR:1,m.WISMAR_EAST:3,m.BENZ:1,m.NEUKLOSTER:8})
        self.assertTrue(all(r['state']=='STATE_MECKLENBURG' and r['owner']=='SWE' for r in rows))
        amt=next(r for r in rows if r['rgb']==m.NEUKLOSTER)
        self.assertEqual({y for x,y in amt['cells']},{739,740,741})

    def test_parent_provenance_is_not_invented(self):
        for r in self.plan['assignments']:
            self.assertTrue(all(self.before[y,x]==int(r['parent_rgb'][1:],16) for x,y in r['cells']))
            self.assertEqual(len(m.core.components(self.after==int(r['rgb'][1:],16))),1)

    def test_no_artificial_benz_neukloster_corridors(self):
        for x in [4358,4360]:self.assertTrue(np.array_equal(self.before[738:743,x],self.after[738:743,x]))
        self.assertEqual(self.after[739,4358],0xD8F441);self.assertEqual(self.after[739,4360],0xD8F441)

    def test_poel_and_strait_exactly_preserved(self):
        plan=m.island.load('ISLAND_PLAN.json');h=m.island.load('RELIEF_PLAN.json')
        for r in plan['changes']:self.assertEqual(int(self.after[r['Y'],r['X']]),int(r['RGB_after'][1:],16))
        for x,y in h['moat_cells']:self.assertEqual(int(self.after[y,x]),int(m.island.SEA[1:],16))
        for rel in ['map_data/heightmap.png','map_data/packed_heightmap.png','map_data/rivers.png']:self.assertEqual(m.core.sha(m.ROOT/rel),self.base['hashes'][rel])

    def test_reserved_source_controls_not_native_accuracy_claim(self):
        t=m.load('SOURCE_TRACING.json');fit=[r for r in t['controls'] if r['role']=='FIT'];held=[r for r in t['controls'] if r['role']=='CHECK']
        self.assertEqual((len(fit),len(held)),(3,4));self.assertLess(max(r['source_alignment_error_native_px'] for r in held),.2)
        self.assertIn('not certified',t['native_projection'])

    def test_only_source_majorities_and_no_sea_reclamation(self):
        t=m.load('SOURCE_TRACING.json');self.assertEqual(len(t['candidates']),13);self.assertEqual(len(t['rejected']),2)
        self.assertTrue(all(r['Coverage']>=.5 and r['Owner_before']==['STATE_MECKLENBURG','MEC'] for r in t['candidates']))
        for r in t['rejected']:self.assertEqual(self.after[r['Y'],r['X']],self.before[r['Y'],r['X']])

    def test_integer_population_no_creation(self):
        self.assertEqual(sum(r['after']['SWE'] for r in self.plan['allocations']),3874)
        for r in self.plan['allocations']:
            self.assertEqual(sum(r['after'].values()),r['before']);self.assertEqual(r['after'],m.core.allocate(r['before'],self.plan['weights']))

    def test_exact_ledger_replay_after_poel(self):
        migration=m.load('REGISTRY_MIGRATION.json')
        lots=registry.approved_lot_dirs();later=lots[lots.index(m.OUT)+1:]
        migrations=[migration]+[json.loads((p/'REGISTRY_MIGRATION.json').read_text()) for p in later]
        with patch.object(registry,'approved_territorial_migrations',return_value=migrations):result=registry.apply_territorial_migrations(self.base['registry'])
        self.assertEqual(result,json.loads(m.core.active_registry_path().read_text()))

    def test_cumulative_poel_then_mainland_ledger_replay(self):
        migrations=[m.island.load('REGISTRY_MIGRATION.json'),m.load('REGISTRY_MIGRATION.json')]
        lots=registry.approved_lot_dirs();later=lots[lots.index(m.OUT)+1:]
        migrations += [json.loads((p/'REGISTRY_MIGRATION.json').read_text()) for p in later]
        original=m.island.load('ISLAND_PLAN.json')['registry_before']
        with patch.object(registry,'approved_territorial_migrations',return_value=migrations):result=registry.apply_territorial_migrations(original)
        self.assertEqual(result,json.loads(m.core.active_registry_path().read_text()))

    def test_undeclared_registry_input_rejected(self):
        bad=list(self.base['registry']);bad=[dict(r) for r in bad];next(r for r in bad if r['state']=='STATE_MECKLENBURG')['beneficiary']='PRU'
        with patch.object(registry,'approved_territorial_migrations',return_value=[m.load('REGISTRY_MIGRATION.json')]):
            with self.assertRaises(AssertionError):registry.apply_territorial_migrations(bad)

    def test_no_sweden_membership_or_worldwide_exception(self):
        self.assertNotIn('SWE',registry.additional_members());self.assertEqual(registry.territorial_holder_overrides()['SWE'],{'STATE_POMERANIA','STATE_MECKLENBURG'})
        for state in ['STATE_UPPLAND','STATE_SKANIA','STATE_RHINELAND']:
            self.assertNotEqual(registry.rightful_holder_condition(dict(beneficiary='SWE',state=state)),'exists = c:SWE')

    def test_external_holder_manifest_is_strict(self):
        target=m.OUT/'REGISTRY_MIGRATION.json';original=registry.Path.read_text;bad=m.load('REGISTRY_MIGRATION.json');bad['external_holder_RGBs'].append('xFFFFFF')
        def read(path,*args,**kwargs):return json.dumps(bad) if path==target else original(path,*args,**kwargs)
        with patch.object(registry.Path,'read_text',new=read):
            with self.assertRaises(AssertionError):registry.territorial_holder_overrides()

    def test_native_hubs_are_not_moved_to_make_territory_fit(self):
        for r in m.prior.locators(self.before):
            if r['ID'] in [57,75]:self.assertEqual(self.before[int(r['Y']),int(r['X'])],self.after[int(r['Y']),int(r['X'])])

    def test_prior_prussian_frontiers_untouched(self):
        for rgb in [0x567452,0xE1A03A,0xEDB010,0xFCC7B7,0x41A021]:self.assertTrue(np.array_equal(self.before==rgb,self.after==rgb))

    def test_all_sectors_ready_but_not_fake_engine_validation(self):
        v=m.load('VALIDATION.json');self.assertEqual(v['status'],'MAP2N_READY_FOR_RUNTIME_VALIDATION');self.assertEqual(set(v['sectors']),{'WISMAR','POEL','NEUKLOSTER'})
        self.assertFalse(v['engine_tested']);self.assertFalse(v['historical_boundary_certified'])
        receipt=m.PARENT/'RUNTIME_USER_VALIDATION_2026_10_15.json'
        if receipt.exists():
            human=json.loads(receipt.read_text(encoding='utf-8'))
            self.assertEqual(human['lot'],'MAP2N');self.assertEqual(human['status'],'PASS_RUNTIME_USER_VALIDATED')
            self.assertFalse(human['automated_engine_test']);self.assertFalse(human['historical_boundary_certification'])
            self.assertFalse(human['prototype_included']);self.assertTrue(v['runtime_user_validated'])
            self.assertEqual(v['runtime_status'],human['status'])
        else:self.assertFalse(v['runtime_user_validated'])

if __name__=='__main__':unittest.main()
