"""MAP2Q source/delta/union negative guards. Never writes runtime data."""
import unittest
import numpy as np
import map2q_eutin as q


class EutinGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=q.load('GEOMETRY.json');cls.before=q.core.packed(q.OUT/'provinces_before.png');cls.after=q.core.packed(q.ROOT/'map_data/provinces.png')

    def test_exact_bitmap_and_negative_outside_edit(self):
        expected=self.before.copy()
        for r in self.g['assignments']:
            for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after))
        expected[735,4410]^=1
        self.assertFalse(np.array_equal(expected,self.after))

    def test_only_authorized_owners_and_region(self):
        transfers=[r for r in self.g['assignments'] if r['owner']=='HLB']
        self.assertEqual(sum(r['pixels'] for r in transfers),31)
        self.assertEqual({r['previous_owner'] for r in transfers},{'LUB','HOL'})
        self.assertTrue(all(r['state']=='STATE_SCHLESWIG_HOLSTEIN' for r in self.g['assignments']))

    def test_native_union_exception_is_one_exact_pair(self):
        u=q.load('PERSONAL_UNION_EXCEPTION.json')
        raw=(q.ROOT/'common/diplomatic_actions/22_subject_personal_union.txt').read_text(encoding='utf-8-sig')
        self.assertEqual(raw.count(u['new']),1)
        self.assertEqual(raw.replace(u['new'],u['old']),q.Path(u['native_file']).read_text(encoding='utf-8-sig'))
        self.assertIn('c:HLB ?= this has_law = law_type:law_theocracy overlord ?= { c:OLD ?= this }',u['new'])
        self.assertNotEqual(raw.replace('c:HLB ?= this','c:LUB ?= this'),raw)

    def test_historical_population_not_claimed_for_area_allocation(self):
        text=(q.ROOT/'docs/reports/map/MAP_POPULATION_POLICY.md').read_text(encoding='utf8')
        self.assertIn('11 325',text);self.assertIn('pas une donnée historique',text)
        self.assertIn('prime sur la conservation',text)

    def test_no_schwartau_or_oldenburg_corridor(self):
        self.assertTrue(np.array_equal(self.before[738:745,4337:4347],self.after[738:745,4337:4347]))
        self.assertEqual({r['rgb'] for r in self.g['new_provinces']},{'xEDB200','xEDB201','xEDB202','xEDB203'})


if __name__=='__main__':unittest.main()
