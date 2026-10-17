"""Static safeguards for starting customary landowner preferences, not engine QA."""
from pathlib import Path
import re
import unittest
import validate_diplomacy_ottoman_1776 as cw
from start_buildings_2026_10_15 import catalog

ROOT=Path(__file__).resolve().parents[1]
IDEOLOGY='ideology_aor1776_customary_landowners'
IDEOLOGY_PATH=ROOT/'common/ideologies/16_1776_customary_landowners.txt'
ACTION_PATH=ROOT/'common/on_actions/15_1776_customary_law_support.txt'


class CustomarySupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ideology=cw.parse(IDEOLOGY_PATH.read_text(encoding='utf-8-sig'))[0]
        cls.actions=cw.parse(ACTION_PATH.read_text(encoding='utf-8-sig'))

    def test_single_ig_ideology_not_leader_replacement(self):
        self.assertEqual(self.ideology.key,IDEOLOGY)
        self.assertEqual(len(cw.parse(IDEOLOGY_PATH.read_text(encoding='utf-8-sig'))),1)
        self.assertEqual(self.ideology.one('priority'),'100')
        self.assertNotEqual(self.ideology.one('character_ideology'),'yes')
        self.assertEqual({n.key for n in self.ideology.children() if n.key.startswith('lawgroup_')},
            {'lawgroup_governance_principles','lawgroup_distribution_of_power'})

    def test_strict_preference_for_each_customary_law(self):
        scores={'strongly_disapprove':-2,'disapprove':-1,'neutral':0,'approve':1,'strongly_approve':2}
        for group,favourite in [('lawgroup_governance_principles','law_chiefdom'),('lawgroup_distribution_of_power','law_elder_council')]:
            block=self.ideology.children(group)[0]
            self.assertEqual(block.one(favourite),'strongly_approve')
            self.assertTrue(all(scores[cw.scalar(n.value)]<2 for n in block.children() if n.key!=favourite))

    def test_all_law_references_exist_in_correct_group(self):
        laws=catalog('common/laws')
        for block in self.ideology.children():
            if not block.key.startswith('lawgroup_'):continue
            names=[n.key for n in block.children()]
            self.assertEqual(len(names),len(set(names)))
            for name in names:
                self.assertIn(name,laws)
                self.assertEqual(laws[name].one('group'),block.key)

    def test_only_actual_customary_starting_countries(self):
        init=next(n for n in self.actions if n.key=='aor1776_customary_landowners_initialize')
        countries=init.children('effect')[0].children('every_country')[0]
        gate=countries.children('limit')[0].children('OR')[0]
        self.assertEqual([cw.scalar(n.value) for n in gate.children()],['law_type:law_chiefdom','law_type:law_elder_council'])
        self.assertTrue(all(n.key=='has_law' for n in gate.children()))
        self.assertEqual({n.key for n in countries.children()},{'limit','ig:ig_landowners'})
        # Representative country-history cases, not a simulated engine result.
        for filename,expected in [('kau - kaurna.txt',True),('kki - kuki.txt',True),('chi - china.txt',False),('pru - prussia.txt',False)]:
            nodes=cw.parse((ROOT/'common/history/countries'/filename).read_text(encoding='utf-8-sig'))
            starting={cw.scalar(n.value) for n in cw.walk(nodes) if n.key=='activate_law'}
            self.assertEqual(bool(starting & {'law_type:law_chiefdom','law_type:law_elder_council'}),expected)

    def test_only_startup_child_action_not_monthly_or_global_effect_override(self):
        self.assertEqual({n.key for n in self.actions},{'on_game_started','aor1776_customary_landowners_initialize'})
        hook=next(n for n in self.actions if n.key=='on_game_started')
        self.assertEqual([n.key for n in hook.children()],['on_actions'])
        self.assertEqual([cw.scalar(n.value) for n in hook.children('on_actions')[0].children()],['aor1776_customary_landowners_initialize'])

    def test_idempotent_addition_preserves_existing_ideologies_and_laws(self):
        nodes=list(cw.walk(self.actions))
        adds=[n for n in nodes if n.key=='add_ideology']
        self.assertEqual(len(adds),1)
        self.assertEqual(cw.scalar(adds[0].value),IDEOLOGY)
        self.assertTrue(any(n.key=='has_ideology' and cw.scalar(n.value)=='ideology:'+IDEOLOGY for n in nodes))
        self.assertFalse(any(n.key in ['remove_ideology','activate_law','deactivate_law','set_ideology','set_ig_trait'] for n in nodes))

    def test_localizations_have_bom_name_and_description(self):
        for lang in ['french','english']:
            path=ROOT/f'localization/{lang}/1776_customary_landowners_l_{lang}.yml'
            self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
            raw=path.read_text(encoding='utf-8-sig')
            self.assertTrue(raw.startswith('l_'+lang+':'))
            for suffix in ['', '_desc']:
                self.assertRegex(raw,r'(?m)^ '+re.escape(IDEOLOGY+suffix)+r': ".+"$')

    def test_icon_exists(self):
        icon=cw.scalar(self.ideology.one('icon'))
        self.assertTrue((ROOT/icon).is_file() or (Path('C:/Games/Victoria 3/game')/icon).is_file())


if __name__=='__main__':unittest.main(verbosity=2)
