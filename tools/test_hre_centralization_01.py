"""Static contracts and explicit Python transition models, NOT engine tests."""
import unittest,copy,re,json
import hre_centralization_01 as h

def node(path,key):
    return next(n for n in h.cw.parse((h.ROOT/path).read_text(encoding='utf-8-sig')) if n.key==key)

def transition_model(countries,old,new):
    """Small independent state-graph spec; does not execute Clausewitz code."""
    before=copy.deepcopy(countries);result=copy.deepcopy(countries)
    if old==new or result[old]['overlord'] is not None:return before,False
    candidate=result[new]
    if candidate['overlord'] is not None and not(candidate['overlord']==old and candidate['kind'] in {'estate','elector'}):return before,False
    subjects=[k for k,v in result.items() if v['overlord']==old and v['kind'] in {'estate','elector'}]
    candidate['overlord']=None;candidate['kind']=None
    for tag in subjects:
        if tag!=new:result[tag]['overlord']=new
    if result[old]['pure']:
        result[old]['overlord']=new;result[old]['kind']='elector' if result[old]['electoral'] else 'estate'
    return result,True

class SubjectContracts(unittest.TestCase):
    def test_exactly_three_imperial_types(self):
        from map_1776_audit import effective
        keys=[n.key for p in effective(h.ROOT,h.GAME,'common/subject_types') for n in h.cw.parse(p.read_text(encoding='utf-8-sig'))]
        self.assertEqual([keys.count(k) for k in [h.LINK,h.ESTATE,h.ELECTOR]],[1,1,1]);self.assertNotIn('subject_type_aor1776_hre_crownland',keys)
    def test_native_subjects_untouched(self):
        p='common/subject_types/00_subject_types.txt';self.assertFalse((h.ROOT/p).exists())
        self.assertEqual(h.qa.sha(h.GAME/p),h.load('BASELINE.json')['native_hashes'][p])
    def test_localization_name_description_and_links(self):
        for lang in ['english','french']:
            s=(h.ROOT/f'localization/{lang}/1776_imperial_subjects_l_{lang}.yml').read_text(encoding='utf-8-sig')
            for k in [h.LINK,h.ESTATE,h.ELECTOR]:self.assertIn(k+'_no_icon:0',s)
            for k in ['concept_aor1776_hre_protectorate','concept_imperial_estate','concept_imperial_elector']:
                self.assertRegex(s,re.escape(k)+r'_desc:0 "[^\n]*\[concept_subject_type')
            for bad in ['native dependency','gameplay','prototype','dépendance impériale native','centralization journal','journal de centralisation']:self.assertNotIn(bad,s)
    def test_no_annex_or_non_imperial_alternative_type_escape(self):
        for t in [h.ESTATE,h.ELECTOR]:
            n=node('common/subject_types/1776_imperial_centralization.txt',t)
            self.assertEqual(n.one('annex_on_country_formation'),'no')
            self.assertTrue(all(not n.children(k)[0].children() for k in ['lower_autonomy_subject_type_alternatives','same_autonomy_subject_type_alternatives']))
            self.assertEqual([c.value for c in n.children('higher_autonomy_subject_type_alternatives')[0].children()],[h.LINK])
    def test_tribute_direction_and_single_payment(self):
        for t,rate in [('estate',.15),('elector',.10)]:
            n=node('common/diplomatic_actions/1776_imperial_centralization.txt','aor1776_imperial_'+t).children('pact')[0]
            self.assertEqual(len(n.children('income_transfer')),1);self.assertEqual(float(n.one('income_transfer')),rate)
            self.assertEqual(n.one('income_transfer_based_on_second_country'),'yes');self.assertEqual(n.one('second_country_gets_income_transfer'),'no')
            self.assertEqual(float(n.one('cost')),0)
    def test_changed_balance_is_reflected_in_localization(self):
        old=h.CONFIG['estate_tribute']
        try:
            h.CONFIG['estate_tribute']=.125
            texts=h.localizations(h.load('EXPECTED_TEXT.json'))
            self.assertIn('#v 12.5%#!',texts['localization/english/1776_imperial_subjects_l_english.yml'])
            self.assertIn('#v 12,5 %#!',texts['localization/french/1776_imperial_subjects_l_french.yml'])
        finally:h.CONFIG['estate_tribute']=old
    def test_old_whole_empire_annexation_removed(self):
        for stage in [1,2,3]:
            n=node(h.RF,'aor1776_hre_stage_'+str(stage));self.assertFalse(any(n.key in {'annex','create_diplomatic_pact','change_subject_type'} for n in h.cw.walk([n])))
            n=node('common/scripted_buttons/1776_imperial_centralization.txt','aor1776_hre_centralize_'+str(stage))
            self.assertEqual(n.children('possible')[0].children('custom_tooltip')[0].one('always'),'no')
    def test_native_annex_and_unification_validation_guards(self):
        for p,k,f in [('common/war_goal_types/00_annex_country.txt','annex_country','valid'),('common/war_goal_types/27_unification.txt','unification','valid'),('common/diplomatic_actions/37_subjects_decrease_autonomy.txt','da_decrease_autonomy','possible')]:
            n=node(p,k).children(f)[0];self.assertTrue(any(n.key=='aor1776_hre_any_native_bond' and n.value=='no' for n in h.cw.walk([n])))
    def test_native_guard_overrides_change_no_other_content(self):
        def without_our_guard(n):
            if n.key=='custom_tooltip' and n.one('text')=='aor1776_hre_no_direct_annexation_tt':return None
            if isinstance(n.value,list):return [n.key,n.op,[value for c in n.children() if (value:=without_our_guard(c)) is not None]]
            return h.qa.norm(n)
        # The autonomy action now intentionally has electoral conversion logic;
        # R1 separately proves that its ordinary-country branch remains native.
        for p in ['common/war_goal_types/00_annex_country.txt','common/war_goal_types/27_unification.txt']:
            original=h.cw.parse((h.GAME/p).read_text(encoding='utf-8-sig'));new=h.cw.parse((h.ROOT/p).read_text(encoding='utf-8-sig'))
            self.assertEqual([h.qa.norm(n) for n in original],[without_our_guard(n) for n in new])
    def test_electoral_status_is_not_only_a_tag_list(self):
        n=node(h.TRIG,'aor1776_hre_elector');raw=json.dumps(h.qa.norm(n))
        self.assertIn('aor1776_hre_electoral_privilege_granted',raw);self.assertIn('aor1776_hre_electoral_privilege_revoked',raw)
    def test_privilege_changes_are_authorized_and_not_mid_ballot(self):
        for v in ['grant','revoke']:
            n=node('common/scripted_effects/1776_imperial_centralization.txt','aor1776_hre_'+v+'_electoral_privilege')
            raw=json.dumps(h.qa.norm(n));self.assertIn('aor1776_hre_constitutional_privilege_change_authorized',raw);self.assertIn('aor1776_hre_election_open',raw);self.assertIn('aor1776_hre_election_pending',raw)
    def test_sync_preserves_liberty_and_has_no_daily_hook(self):
        n=node('common/scripted_effects/1776_imperial_centralization.txt','aor1776_hre_sync_imperial_subject_status');raw=json.dumps(h.qa.norm(n))
        self.assertIn('c01_status_previous_liberty',raw);self.assertIn('add_liberty_desire',raw)
        oa=(h.ROOT/'common/on_actions/1776_imperial_constitution.txt').read_text(encoding='utf8');self.assertNotIn('aor1776_hre_sync_imperial_subject_status',oa)
    def test_advanced_constitution_does_not_disable_elections(self):
        n=node('common/on_actions/1776_imperial_constitution.txt','aor1776_hre_death_hook');self.assertNotIn('aor1776_hre_unified',json.dumps(h.qa.norm(n)))
    def test_mixed_powers_not_native_candidates(self):
        n=node('common/scripted_triggers/1776_imperial_centralization.txt','aor1776_hre_centralization_native_eligible');s=json.dumps(h.qa.norm(n))
        for t in ['c:PRU','c:AUS','c:SWE','c:SAR']:self.assertNotIn('"'+t+'"',s)
        self.assertIn('c:ANH',s);self.assertIn('c:KPF',s)
    def test_production_succession_fails_closed(self):
        n=node(h.EF,h.INSTALL);s=json.dumps(h.qa.norm(n));self.assertIn('aor1776_hre_centralized_transfer_pending',s)
        self.assertNotIn('make_independent',s);self.assertNotIn('create_diplomatic_pact',s)
    def test_companion_not_activated_and_console_armed(self):
        self.assertFalse((h.ROOT/'common/scripted_effects/zz_hre_centralization_01_test.txt').exists())
        p=h.COMPANION/'mod/common/scripted_effects/zz_hre_centralization_01_test.txt';s=p.read_text(encoding='utf8');self.assertIn('aor1776_hre_c01_dev_armed',s)
        self.assertNotIn('annex =',s)

class TransitionSpecificationModels(unittest.TestCase):
    def initial(self):
        def c(overlord=None,kind=None,pure=True,electoral=False):return dict(overlord=overlord,kind=kind,pure=pure,electoral=electoral,population=100,buildings=2,liberty=37)
        return {'AUS':c(pure=False,electoral=True),'PRU':c(pure=False,electoral=True),'ANH':c('AUS','estate'),'KPF':c('AUS','elector',electoral=True),'FOREIGN':c('AUS','personal_union'),'HLB':c('OLD','personal_union'),'OLD':c()}
    def test_austria_prussia_only_imperial_subjects_change(self):
        b=self.initial();a,ok=transition_model(b,'AUS','PRU');self.assertTrue(ok)
        for t in ['ANH','KPF']:self.assertEqual(a[t]['overlord'],'PRU')
        for t in ['FOREIGN','HLB','OLD']:self.assertEqual(a[t],b[t])
        self.assertEqual(a['AUS']['overlord'],None)
        for t in b:
            for k in ['population','buildings','liberty']:self.assertEqual(a[t][k],b[t][k])
    def test_elected_subject_freed_before_other_subjects_transferred(self):
        b=self.initial();a,ok=transition_model(b,'AUS','KPF');self.assertTrue(ok);self.assertIsNone(a['KPF']['overlord']);self.assertEqual(a['ANH']['overlord'],'KPF')
    def test_external_subject_candidate_rejected_without_mutation(self):
        b=self.initial();a,ok=transition_model(b,'AUS','HLB');self.assertFalse(ok);self.assertEqual(a,b)
    def test_cycle_candidate_rejected(self):
        b=self.initial();b['AUS']['overlord']='PRU';a,ok=transition_model(b,'AUS','PRU');self.assertFalse(ok);self.assertEqual(a,b)
    def test_previous_pure_emperor_respects_its_electoral_status(self):
        b=self.initial();b['AUS']['pure']=True;a,ok=transition_model(b,'AUS','PRU');self.assertTrue(ok);self.assertEqual(a['AUS']['kind'],'elector')

if __name__=='__main__':unittest.main()
