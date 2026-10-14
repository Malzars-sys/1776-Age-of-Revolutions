"""Regression cases for missing principle bonuses and mismatched demands."""
import re
import validate_diplomacy_ottoman_1776 as cw
from map2k_work import ROOT

def validate_demand_feedback(check,node,textnode):
 wg=node('common/war_goal_types/1776_imperial_war_goals.txt','aor1776_hre_restitution')
 for field in ['possible','valid']:
  raw=textnode(wg.children(field))
  check('restitution_requires_real_land_and_documented_refusal:'+field,all(k in raw for k in ['owner','scope:target_country','aor1776_hre_restitution_state','aor1776_hre_restitution_refusal_valid_tt','aor1776_hre_refusal_holder','aor1776_hre_release_refused']))
  comparisons=[n for n in cw.walk(wg.children(field)) if n.key=='var:aor1776_hre_refusal_holder']
  check('unrecorded_state_refusal_cannot_fetch_unset_variable:'+field,len(comparisons)==1 and comparisons[0].op=='?=')
 # Target-state eligibility still matters; a refusal is not a licence to
 # conquer foreign homelands without registered imperial provinces.
 def allowed(land,owned,state_refusal,country_refusal):return land and owned and (state_refusal or country_refusal)
 fixtures=[(False,True,False,True,False),(True,False,True,True,False),(True,True,False,False,False),(True,True,True,False,True),(True,True,False,True,True)]
 check('refusal_does_not_create_claims_on_nonimperial_homeland_model',all(allowed(*f[:4])==f[4] for f in fixtures))
 for lang in ['english','french']:
  loc={}
  for p in (ROOT/'localization'/lang).glob('1776_imperial*_l_'+lang+'.yml'):
   loc.update(dict(re.findall(r'^ ([^ :]+):0 "(.*)"$',p.read_text(encoding='utf-8-sig'),re.M)))
  keys=[key+'_proposal_'+response+'_'+suffix for key in ['aor1776_hre_request_subject_release','aor1776_hre_request_restitution','aor1776_hre_enforce_internal_restitution'] for response in ['declined','accepted'] for suffix in ['name','desc']]
  check('generic_diplomatic_response_popup_keys_localized:'+lang,all(k in loc for k in keys))
  received=[key+'_proposal_notification_'+suffix for key in ['aor1776_hre_request_subject_release','aor1776_hre_request_restitution','aor1776_hre_enforce_internal_restitution'] for suffix in ['name','desc']]
  check('recipient_proposal_window_title_and_description_localized:'+lang,all(k in loc for k in received) and 'INITIATOR_COUNTRY.GetName' in loc['aor1776_hre_request_subject_release_proposal_notification_desc'])
  check('refusal_messages_distinguish_subject_liberation_and_territory:'+lang,'TARGET_COUNTRY.GetName' in loc['aor1776_hre_request_subject_release_proposal_declined_desc'] and 'aor1776_hre.31.result' in loc and 'aor1776_hre_restitution_refusal_valid_tt' in loc)
