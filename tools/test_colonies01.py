"""Actual-file regression guards for the requested independence law lock."""
import unittest
from colonies01_core import ROOT,TRIGGER,LAW,text,parse,walk


def locked(country,overlord,independence_war=False):
    node=parse(text(ROOT/'common/scripted_triggers/1776_usa_colonial_expansion.txt'))[0]
    values={'this':'c:'+country,'is_subject':'yes' if overlord else 'no','aor1776_usa_independence_war_active':'yes' if independence_war else 'no'}
    def check(n):
        if n.key=='OR':return any(check(v) for v in n.children())
        if n.key not in values:raise AssertionError('Unreviewed trigger syntax')
        return values[n.key]==n.value
    return all(check(n) for n in node.children())


class ColonialRestriction(unittest.TestCase):
    def test_colonies_still_in_rebellion_remain_locked(self):self.assertTrue(locked('USA','GBR'))
    def test_independence_unlocks_without_a_fixed_date(self):self.assertFalse(locked('USA',None))
    def test_changing_overlord_does_not_fake_independence(self):self.assertTrue(locked('USA','FRA'))
    def test_subject_pact_ending_during_war_is_not_yet_victory(self):self.assertTrue(locked('USA',None,independence_war=True))
    def test_other_british_subjects_unchanged(self):
        for country in ['HBC','NVS','QUE','IREK']:self.assertFalse(locked(country,'GBR'))
    def test_britain_itself_unchanged(self):self.assertFalse(locked('GBR',None))
    def test_enactment_and_imposition_have_the_target_guard(self):
        laws=[n for n in parse(text(ROOT/LAW)) if n.key!='law_no_colonial_affairs']
        self.assertEqual(len(laws),3)
        for law in laws:
            self.assertTrue(any(n.key==TRIGGER for n in walk(law.children('can_enact'))))
            target=law.children('can_impose')[0].children('scope:target_country')
            self.assertEqual(len(target),1)
            self.assertTrue(any(n.key==TRIGGER for n in walk(target)))
    def test_no_initial_colonial_institution(self):
        raw=text(ROOT/'common/history/countries/usa - usa.txt')
        self.assertIn('law_type:law_no_colonial_affairs',raw)
        self.assertNotIn('law_type:law_frontier_colonization',raw)
        self.assertNotIn('institution_colonial_affairs',raw)


if __name__=='__main__':unittest.main()
