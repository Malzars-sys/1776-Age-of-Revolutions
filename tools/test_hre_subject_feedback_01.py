"""R1 regression contracts; no claim of executing the game engine."""
import unittest,re,json
import hre_subject_feedback_01 as r
h=r.h

def text(p):return (h.ROOT/p).read_text(encoding='utf-8-sig')
def node(p,k):return next(n for n in h.cw.parse(text(p)) if n.key==k)
def loc(p):return dict(re.findall(r'(?m)^ ([\w.]+):(?:\d+)?[ \t]+"([^\n]*)"$',text(p)))

class FeedbackContracts(unittest.TestCase):
    def test_bidirectional_type_chain(self):
        bond=node('common/subject_types/1776_imperial_reforms.txt',h.LINK)
        self.assertEqual({n.value for n in bond.children('lower_autonomy_subject_type_alternatives')[0].children()},{h.ESTATE,h.ELECTOR})
        for t in [h.ESTATE,h.ELECTOR]:
            n=node('common/subject_types/1776_imperial_centralization.txt',t)
            self.assertEqual([n.value for n in n.children('higher_autonomy_subject_type_alternatives')[0].children()],[h.LINK])
            self.assertEqual(n.children('lower_autonomy_subject_type_alternatives')[0].children(),[])
    def test_both_diplomatic_descriptions_use_same_authority(self):
        for lang in ['french','english']:
            prefix=f'localization/{lang}/1776_imperial_'
            for stem,key in [('constitution','aor1776_imperial_obligation_desc'),('repairs','aor1776_imperial_obligation_pact_desc'),('reforms','aor1776_hre_protectorate_desc')]:
                self.assertEqual(loc(prefix+stem+'_l_'+lang+'.yml')[key],'$concept_aor1776_hre_protectorate_desc$')
    def test_all_bond_display_surfaces_share_title_and_description(self):
        for lang in ['french','english']:
            prefix=f'localization/{lang}/1776_imperial_'
            constitution=loc(prefix+'constitution_l_'+lang+'.yml')
            subjects=loc(prefix+'subjects_l_'+lang+'.yml')
            self.assertEqual(constitution['aor1776_imperial_obligation'],'$concept_aor1776_hre_protectorate$')
            for action in ['aor1776_hre_protectorate','aor1776_hre_crownland']:
                self.assertEqual(subjects[action+'_pact_desc'],'$concept_aor1776_hre_protectorate_desc$')
            for stem in ['constitution','repairs','reforms','subjects']:
                raw=text(prefix+stem+'_l_'+lang+'.yml')
                for stale in ['obligation impériale sans tribut ni suzeraineté native','imperial obligation without tribute or native overlordship','Un lien constitutionnel impérial sans tribut']:self.assertNotIn(stale,raw)
    def test_rates_real_and_displayed(self):
        for kind,rate in [('estate',.15),('elector',.10)]:
            n=node('common/diplomatic_actions/1776_imperial_centralization.txt','aor1776_imperial_'+kind).children('pact')[0]
            self.assertEqual(float(n.one('income_transfer')),rate)
            self.assertEqual(n.one('income_transfer_based_on_second_country'),'yes')
            self.assertEqual(n.one('second_country_gets_income_transfer'),'no')
        for lang,marker in [('french','#v 15 %#!'),('english','#v 15%#!')]:
            self.assertIn(marker,text(f'localization/{lang}/1776_imperial_subjects_l_{lang}.yml'))
    def test_lowering_explicitly_checks_electoral_status(self):
        n=node('common/diplomatic_actions/37_subjects_decrease_autonomy.txt','da_decrease_autonomy').children('accept_effect')[0]
        raw=json.dumps(h.qa.norm(n));self.assertIn('aor1776_hre_elector',raw)
        self.assertIn(h.ESTATE,raw);self.assertIn(h.ELECTOR,raw);self.assertNotIn('annex',raw)
    def test_both_increase_actions_return_to_link(self):
        p='common/diplomatic_actions/38_subjects_increase_autonomy.txt'
        for k in ['da_increase_autonomy_of_subject','da_increase_autonomy_of_self']:
            n=node(p,k).children('accept_effect')[0];raw=json.dumps(h.qa.norm(n))
            self.assertIn(h.LINK,raw);self.assertIn('aor1776_hre_centralized_subject',raw)
            for forbidden in ['make_independent','remove_diplomatic_pact','annex','aor1776_hre_electoral_privilege_revoked']:self.assertNotIn(forbidden,raw)
    def test_native_actions_else_branch_is_unchanged(self):
        def clean(n):
            if n.key=='custom_tooltip' and n.one('text')=='aor1776_hre_autonomy_reduction_allowed_tt':return None
            limits=n.children('limit')
            if n.key=='if' and limits and limits[0].one('is_subject_type')==h.LINK:return ['decrease_autonomy','=','yes']
            if n.key=='else_if' and limits and limits[0].one('aor1776_hre_any_native_bond')=='no':return None
            if n.key=='if' and limits and limits[0].one('aor1776_hre_centralized_subject')=='yes':return ['increase_autonomy','=','yes']
            if n.key=='else' and n.one('increase_autonomy')=='yes':return None
            if isinstance(n.value,list):return [n.key,n.op,[v for c in n.children() if (v:=clean(c)) is not None]]
            return h.qa.norm(n)
        for p in ['common/diplomatic_actions/37_subjects_decrease_autonomy.txt','common/diplomatic_actions/38_subjects_increase_autonomy.txt']:
            self.assertEqual([h.qa.norm(n) for n in h.cw.parse((h.GAME/p).read_text(encoding='utf-8-sig'))],[clean(n) for n in h.cw.parse(text(p))])
    def test_no_global_localization_lie_for_vanilla_subjects(self):
        for lang in ['english','french']:
            rows=loc(f'localization/{lang}/replace/1776_imperial_autonomy_l_{lang}.yml')
            native=(h.GAME/f'localization/{lang}/interfaces_l_{lang}.yml').read_text(encoding='utf-8-sig')
            for k in ['SUBJECT_TYPE_ANNEX_TOOLTIP','SUBJECT_TYPE_DECREASED_AUTONOMY_TOOLTIP','SUBJECT_TYPE_INDEPENDENCE_TOOLTIP','SUBJECT_TYPE_INCREASED_AUTONOMY_TOOLTIP']:
                fallback='aor1776_vanilla_'+k.lower()
                self.assertEqual(rows[fallback],re.search(r'(?m)^ '+k+r':(?:\d+)?[ \t]+"([^\n]*)"$',native).group(1))
                self.assertIn('SubjectType.GetKey',rows[k]);self.assertIn('SelectLocalization',rows[k])
    def test_table_lower_tooltip_covers_both_branches(self):
        rows=loc('localization/french/replace/1776_imperial_autonomy_l_french.yml')
        for k in ['concept_imperial_estate','concept_imperial_elector','dignité électorale','n’est pas annexé']:self.assertIn(k,rows['aor1776_hre_link_lower_tooltip'])
    def test_safe_decrease_no_general_conversion_during_ballot(self):
        n=node('common/diplomatic_actions/37_subjects_decrease_autonomy.txt','da_decrease_autonomy')
        for k in ['potential','possible']:
            raw=json.dumps(h.qa.norm(n.children(k)[0]))
            for flag in ['aor1776_hre_emperor','aor1776_hre_election_open','aor1776_hre_election_pending','aor1776_hre_centralization_native_eligible']:self.assertIn(flag,raw)
    def test_generator_component_is_idempotent(self):
        expected=r.load('EXPECTED_TEXT.json');self.assertEqual(h.autonomy_feedback(expected),expected)
    def test_prerequisite_tokens_not_replaced_as_effects(self):
        for p,k in [('common/diplomatic_actions/37_subjects_decrease_autonomy.txt','can_decrease_autonomy'),('common/diplomatic_actions/38_subjects_increase_autonomy.txt','can_increase_autonomy')]:
            expected=len(re.findall(r'\b'+k+r' = yes',(h.GAME/p).read_text(encoding='utf-8-sig')))
            self.assertEqual(len(re.findall(r'\b'+k+r' = yes',text(p))),expected)

if __name__=='__main__':unittest.main()
