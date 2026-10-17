"""Departure-entry visibility contracts, not live engine/UI tests."""
import unittest,json
import hre_secession_lens_01 as s
h=s.h

def nodes(raw):return h.cw.parse(raw)
def current(p):return (s.ROOT/p).read_text(encoding='utf-8-sig')
def one(raw,key):return next(n for n in nodes(raw) if n.key==key)

class DepartureFilter(unittest.TestCase):
    def test_native_other_plays_and_conditions_identical(self):
        native=(h.GAME/s.NATIVE).read_text(encoding='utf-8-sig')
        def clean(n):
            if n.key=='selectable_in_lens' and any(c.key==s.MEMBER for c in n.children()):return None
            if n.key=='custom_tooltip' and n.one('text')=='aor1776_hre_bloc_departure_requires_secession_tt':return None
            if isinstance(n.value,list):return [n.key,n.op,[v for c in n.children() if (v:=clean(c)) is not None]]
            return h.qa.norm(n)
        self.assertEqual([h.qa.norm(n) for n in nodes(native)],[clean(n) for n in nodes(current(s.NATIVE))])
    def test_generic_exit_hidden_and_direct_launch_guarded(self):
        n=one(current(s.NATIVE),'dp_leave_power_bloc')
        self.assertEqual(n.children('selectable_in_lens')[0].one(s.MEMBER),'no')
        guards=[g for g in h.cw.walk(n.children('possible')) if g.key==s.MEMBER]
        self.assertEqual([g.value for g in guards],['no'])
    def test_specialized_entry_requires_current_imperial_bloc(self):
        n=one(current(s.IMPERIAL),'dp_aor1776_hre_secession')
        self.assertEqual(n.children('selectable_in_lens')[0].one(s.MEMBER),'yes')
        self.assertEqual(n.children('selectable_in_lens')[0].one('aor1776_hre_emperor'),'no')
        guards=[g for g in h.cw.walk(n.children('possible')) if g.key==s.MEMBER]
        self.assertEqual([g.value for g in guards],['yes'])
    def test_imperial_play_other_rules_unchanged(self):
        before=s.load('BASELINE.json')['original_imperial']
        def clean(n):
            if n.key==s.MEMBER:return None
            if n.key=='custom_tooltip' and n.one('text')=='aor1776_hre_secession_in_imperial_bloc_tt':return None
            if isinstance(n.value,list):return [n.key,n.op,[v for c in n.children() if (v:=clean(c)) is not None]]
            return h.qa.norm(n)
        self.assertEqual([h.qa.norm(n) for n in nodes(before)],[clean(n) for n in nodes(current(s.IMPERIAL))])
    def test_current_bloc_not_only_roster_tag(self):
        n=one(current(s.TRIGGER),s.MEMBER)
        self.assertEqual(n.one('aor1776_hre_member'),'yes');self.assertEqual(n.one('exists'),'power_bloc')
        self.assertEqual(n.children('power_bloc')[0].one('has_identity'),'identity:identity_aor1776_imperial_federation')
    def test_truth_table_is_not_engine_execution(self):
        # Boolean specification: member outside imperial bloc keeps vanilla exit.
        def imperial(member,bloc):return member and bloc=='imperial'
        for member,bloc,hidden in [(True,'imperial',True),(False,'imperial',False),(True,'foreign',False),(False,'foreign',False),(True,None,False)]:
            self.assertEqual(imperial(member,bloc),hidden)
    def test_idempotent_regeneration(self):
        expected=s.load('EXPECTED_TEXT.json');self.assertEqual(s.augment(expected),expected)
    def test_no_secession_war_goal_or_enforcement_change(self):
        p='common/war_goal_types/1776_imperial_war_goals.txt'
        self.assertEqual(h.qa.sha(s.ROOT/p),s.load('BASELINE.json')['hashes'][p])
    def test_all_validation_messages_localized(self):
        for lang in ['english','french']:
            raw=current(f'localization/{lang}/1776_imperial_constitution_l_{lang}.yml')
            for key in ['aor1776_hre_bloc_departure_requires_secession_tt','aor1776_hre_secession_in_imperial_bloc_tt']:
                self.assertEqual(raw.count(' '+key+':0 '),1)

if __name__=='__main__':unittest.main()
