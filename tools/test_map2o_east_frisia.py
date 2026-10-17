"""East Frisian additive correction and negative scope guards; no engine claims."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import map2o_east_frisia as m
import map2l_registry as registry


class EastFrisiaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=m.load('PLAN.json');cls.base=m.load('BASELINE.json');cls.migration=m.load('REGISTRY_MIGRATION.json')

    def test_only_existing_319_cell_province_not_neighboring_tags(self):
        changes=self.plan['changes']
        self.assertEqual(len({(r['X'],r['Y']) for r in changes}),319)
        self.assertTrue(all((r['RGB_before'],r['RGB_after'],r['Owner_before'],r['Owner_after'],r['State_ID'])==(m.PARENT,m.PARENT,'HAN','PRU',m.REGION) for r in changes))
        self.assertEqual(self.plan['new_RGBs'],[]);self.assertEqual(self.plan['recolored_cells'],0)

    def test_deterministic_demographics_without_new_people(self):
        self.assertEqual(self.plan['weights'],{'HAN':1299,'PRU':319})
        self.assertEqual(sum(r['after']['PRU'] for r in self.plan['allocations']),142528)
        for row in self.plan['allocations']:
            self.assertEqual(sum(row['after'].values()),row['before'])
            self.assertEqual(row['after'],m.core.allocate(row['before'],self.plan['weights']))

    def test_exact_ledger_replay_preserves_every_other_right(self):
        with patch.object(registry,'approved_territorial_migrations',return_value=[self.migration]):
            actual=registry.apply_territorial_migrations(self.base['registry'])
        self.assertEqual(actual,json.loads(m.core.active_registry_path().read_text(encoding='utf-8')))
        self.assertEqual([r for r in actual if r['rgb']!=m.PARENT],[r for r in self.base['registry'] if r['rgb']!=m.PARENT])

    def rejected_manifest(self,edit):
        target=m.OUT/'REGISTRY_MIGRATION.json';bad=copy.deepcopy(self.migration);edit(bad);original=Path.read_text
        def read(path,*args,**kwargs):return json.dumps(bad) if path==target else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',new=read):
            with self.assertRaises(AssertionError):registry.approved_lot_dirs()

    def test_cannot_register_all_prussia(self):
        self.rejected_manifest(lambda x:x['new_members'].append('PRU'))

    def test_cannot_extend_registered_land(self):
        self.rejected_manifest(lambda x:x['extent_added_cells'].append([4275,750]))

    def test_cannot_annex_oldenburg(self):
        self.rejected_manifest(lambda x:next(r for r in x['updated'] if r['rgb']=='xECC3B4').update(beneficiary='PRU'))

    def test_cannot_claim_unreviewed_child_rgb(self):
        self.rejected_manifest(lambda x:x['new_provinces'].append({'rgb':'xFFFFFF'}))

    def test_no_false_full_completion_or_runtime_validation(self):
        report=m.load('VALIDATION.json')
        self.assertEqual(report['status'],'MAP2O_PARTIAL');self.assertFalse(report['engine_tested']);self.assertFalse(report['runtime_user_validated'])
        self.assertEqual(report['southern_fringe'],'C_UNCHANGED')


if __name__=='__main__':unittest.main()
