"""R2 population model and scope guards; no runtime writes."""
import unittest
import map2q_r2 as r

class Demography(unittest.TestCase):
    def test_largest_remainders(self):
        self.assertEqual(r.apportion([10870,18,254,183],7600),[7295,12,170,123])
        self.assertEqual(sum(r.apportion([1,2,3],17)),17)

    def test_six_tokens_and_unchanged_context(self):
        original=r.read('BASELINE.json')['original_pops'];after,rows=r.transformed(original)
        before_region=r.q.core.region(original,r.q.REGION,'HLB')
        new_region=r.q.core.region(after,r.q.REGION,'HLB')
        self.assertEqual(original[:before_region.start],after[:new_region.start])
        self.assertEqual(original[before_region.end:],after[new_region.end:])
        self.assertEqual(len(new_region.children('create_pop')),6)
        self.assertEqual(sum(int(n.one('size')) for n in new_region.children('create_pop')),7600)

    def test_nonzero_world_delta_is_valid(self):
        before=[dict(key=[r.q.REGION,'HLB','north_german','DEFAULT:north_german'],count=100)]
        after=[dict(key=[r.q.REGION,'HLB','north_german','DEFAULT:north_german'],count=80)]
        profiles=[dict(culture='north_german',religion='DEFAULT',delta=-20)]
        self.assertTrue(r.population_delta_ok(before,after,profiles))

    def test_compensation_and_extra_people_are_rejected(self):
        before=[dict(key=[r.q.REGION,'HLB','north_german','DEFAULT:north_german'],count=100)]
        after=[dict(key=[r.q.REGION,'HLB','north_german','DEFAULT:north_german'],count=80),
               dict(key=[r.q.REGION,'HOL','north_german','DEFAULT:north_german'],count=20)]
        profiles=[dict(culture='north_german',religion='DEFAULT',delta=-20)]
        self.assertFalse(r.population_delta_ok(before,after,profiles))
        after[0]['count']=81;after.pop()
        self.assertFalse(r.population_delta_ok(before,after,profiles))

    def test_sources_not_mixed(self):
        m=r.read('ESTIMATE_CALCULATIONS.json')
        self.assertEqual(m['aggsh_amt_1819'],7070);self.assertEqual(m['kohli_amt_1819'],6824)
        self.assertEqual(m['aggsh_city_1819'],2686);self.assertEqual(m['kohli_city_1819'],2652)
        self.assertAlmostEqual(m['city_linear'],2165.0833333333335)
        self.assertAlmostEqual(m['rural_geometric'],5444.678271951813)
        self.assertEqual(sum(m['modeled_rural_districts'])+m['city_rounded'],7600)

    def test_snapshot_guards_reject_repeated_application(self):
        new,_=r.transformed(r.read('BASELINE.json')['original_pops'])
        with self.assertRaises(AssertionError):r.transformed(new)

if __name__=='__main__':unittest.main()
