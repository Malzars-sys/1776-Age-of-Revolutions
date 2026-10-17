"""Read-only MAP2N regression and negative tests. Never rewrite prior reports."""
import unittest,json
from unittest.mock import patch
import numpy as np
import map2n_island as m
import map2l_registry as registry

class PoelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=m.load('ISLAND_PLAN.json');cls.b=m.load('BASELINE.json')
        cls.before=m.core.packed(m.OUT.parent/'MAP2M/R9/provinces_candidate.png')
        cls.after=m.core.packed(m.ROOT/'map_data/provinces.png')

    def test_exact_scoped_edits_and_negative_guard(self):
        expected=self.before.copy()
        for row in self.plan['changes']:expected[row['Y'],row['X']]=int(row['RGB_after'][1:],16)
        # Later, explicitly approved mainland cells do not waive any other edit.
        later=m.OUT/'COMPLETION/PLAN.json'
        if later.exists():
            for row in json.loads(later.read_text())['changes']:expected[row['Y'],row['X']]=int(row['RGB_after'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after))
        expected[740,4410]^=1
        self.assertFalse(np.array_equal(expected,self.after))

    def test_historical_partition_is_explicit_not_all_island_swedish(self):
        geo=m.load('GEOMETRY.json');new={r['owner']:r for r in geo['new_provinces']}
        self.assertEqual(set(new),{'SWE','LUB'});self.assertEqual(new['LUB']['cells'],[[4355,737]])
        self.assertTrue(all(r['state']=='STATE_POMERANIA' for r in new.values()))

    def test_pixel_centre_rasterization_is_reproducible(self):
        d=m.load('POEL_DIAGNOSTIC.json');ring=np.array(d['projected_ring']);x0,y0,x1,y1=m.BOX
        cells=[[x,y] for y in range(y0,y1) for x in range(x0,x1) if m.polygon_contains(ring,(x+.5,y+.5))]
        self.assertEqual(cells,d['island_cells'])

    def test_no_diagonal_or_edge_bridge(self):
        h=m.load('RELIEF_PLAN.json');island={tuple(v) for v in h['island_cells']}
        buffer={(x+dx,y+dy) for x,y in island for dx in [-1,0,1] for dy in [-1,0,1]}-island
        self.assertEqual(buffer,{tuple(v) for v in h['moat_cells']})
        self.assertTrue(all(self.after[y,x]==int(m.SEA[1:],16) for x,y in buffer))
        mutant=self.after.copy();mutant[737,4357]=0xD8F441
        self.assertFalse(all(mutant[y,x]==int(m.SEA[1:],16) for x,y in buffer))

    def test_integer_population_conservation_and_no_artificial_addition(self):
        for row in self.plan['allocations']:
            self.assertEqual(sum(row['after'].values()),row['before'])
            self.assertEqual(row['after'],m.core.allocate(row['before'],self.plan['weights']))
        self.assertEqual(sum(r['after']['SWE']+r['after']['LUB'] for r in self.plan['allocations']),1192)
        self.assertEqual(sum(r['after']['SWE'] for r in self.plan['allocations']),894)

    def test_no_move_of_hubs_or_old_pomeranian_provinces(self):
        rows=m.prior.locators(self.before)
        self.assertTrue(all(self.before[int(r['Y']),int(r['X'])]==self.after[int(r['Y']),int(r['X'])] for r in rows))
        for rgb in [0x567452,0xE1A03A,0xEDB010,0xFCC7B7,0x41A021]:
            self.assertTrue(np.array_equal(self.before==rgb,self.after==rgb))

    def test_ledger_migration_replays_exactly(self):
        migration=m.load('REGISTRY_MIGRATION.json')
        lots=registry.approved_lot_dirs();later=lots[lots.index(m.OUT)+1:]
        migrations=[migration]+[json.loads((p/'REGISTRY_MIGRATION.json').read_text()) for p in later]
        with patch.object(registry,'approved_territorial_migrations',return_value=migrations):
            expected=registry.apply_territorial_migrations(self.plan['registry_before'])
        self.assertEqual(expected,json.loads(m.core.active_registry_path().read_text()))

    def test_no_broad_sweden_exemption(self):
        expected={'STATE_POMERANIA'}
        if (m.OUT/'COMPLETION/REGISTRY_MIGRATION.json').exists():expected.add('STATE_MECKLENBURG')
        self.assertEqual(registry.territorial_holder_overrides()['SWE'],expected)
        self.assertNotIn('SWE',registry.additional_members())
        self.assertEqual(registry.rightful_holder_condition(dict(beneficiary='SWE',state='STATE_POMERANIA')),'exists = c:SWE')
        self.assertNotEqual(registry.rightful_holder_condition(dict(beneficiary='SWE',state='STATE_UPPLAND')),'exists = c:SWE')

    def test_relief_must_be_below_and_above_actual_sea_level(self):
        h=m.load('RELIEF_PLAN.json');self.assertLess(h['sea_height'],h['sea_threshold_16bit']);self.assertGreater(h['land_height'],h['sea_threshold_16bit'])
        self.assertTrue(all(t['native_source_mean_difference']<1 for t in h['tiles']))
        self.assertEqual({tuple(t['source_origin']) for t in h['tiles']},{(8704,1407),(8704,1471)})
        self.assertEqual(len(h['samples']),64);self.assertEqual(len(h['packed_samples']),32)

    def test_no_false_runtime_completion(self):
        archive=m.OUT/'COMPLETION/POEL_STAGE_VALIDATION.json'
        v=json.loads(archive.read_text()) if archive.exists() else m.load('VALIDATION.json');self.assertFalse(v['runtime_tested'])
        self.assertEqual(v['overall_lot'],'MAP2N_PARTIAL_WISMAR_NEUKLOSTER_OPEN')
        self.assertEqual(v['R8_R9_runtime_status'],'PASS_RUNTIME_USER_VALIDATED')

if __name__=='__main__':unittest.main()
