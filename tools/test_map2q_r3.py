"""Read-only R3 guards; old snapshot tests remain unmodified and report failures."""
import unittest,json
import numpy as np
import map2q_r3 as r

class Kaltenhof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=r.load('BASELINE.json');cls.g=r.load('GEOMETRY.json')
        cls.before=r.q.core.packed(r.ROOT/cls.b['bitmap_backup'])
        cls.after=r.q.core.packed(r.ROOT/'map_data/provinces.png')
    def test_exact_delta_and_negative_guard(self):
        expected=self.before.copy()
        for row in self.g['assignments']:
            for x,y in row['cells']:expected[y,x]=int(row['rgb'][1:],16)
        self.assertTrue(np.array_equal(expected,self.after))
        self.assertEqual(int((self.before!=self.after).sum()),4)
        expected[738,4341]^=1
        self.assertFalse(np.array_equal(expected,self.after))
    def test_no_new_territory_corridor(self):
        changed={(x,y) for row in self.g['assignments'] if row['owner']=='HLB' for x,y in row['cells']}
        self.assertEqual(changed,{(4338,738),(4338,739),(4339,739),(4340,738)})
        self.assertEqual(self.after[738,4339],self.before[738,4339])
    def test_no_eutin_or_offscope_change(self):
        self.assertTrue(np.array_equal(self.before[:737],self.after[:737]))
        for row in r.q.load('GEOMETRY.json')['assignments']:
            if row['owner']=='HLB':
                for x,y in row['cells']:self.assertEqual(self.before[y,x],self.after[y,x])
    def test_accepted_eutin_blocks_untouched(self):
        raw=(r.ROOT/r.POP).read_text(encoding='utf-8-sig')
        pops=r.q.core.region(raw,r.SID,'HLB').children('create_pop')
        self.assertEqual([raw[p.start:p.end] for p in pops[:6]],self.b['eutin_pop_blocks'])
        self.assertEqual([int(p.one('size')) for p in pops[6:]],[1568,38])
    def test_distinct_new_rgb_and_no_membership_expansion(self):
        self.assertEqual({row['rgb'] for row in self.g['new_provinces']},{'xEDB204','xEDB205'})
        m=r.load('REGISTRY_MIGRATION.json')
        self.assertFalse(m['new_members']);self.assertFalse(m['extent_added_cells']);self.assertFalse(m['extent_removed_cells'])
    def test_technical_population_not_1776_census(self):
        a=r.load('POPULATION_ALLOCATION.json')
        self.assertIn('NOT_HISTORICAL_ESTIMATE',a['method'])
        self.assertEqual(sum(p['after']['HLB'] for p in a['profiles']),1606)
        self.assertTrue(all(sum(p['after'].values())==p['before'] for p in a['profiles']))
    def test_native_union_remains_exact_pair(self):
        u=r.q.load('PERSONAL_UNION_EXCEPTION.json')
        raw=(r.ROOT/'common/diplomatic_actions/22_subject_personal_union.txt').read_text(encoding='utf-8-sig')
        self.assertEqual(raw.replace(u['new'],u['old']),r.Path(u['native_file']).read_text(encoding='utf-8-sig'))
    def test_geo_accuracy_not_certified_from_fitting(self):
        a=r.load('ALIGNMENT.json')
        self.assertIn('not independently certified',a['warning'])
        self.assertEqual(len(a['controls']),5)

if __name__=='__main__':unittest.main()
