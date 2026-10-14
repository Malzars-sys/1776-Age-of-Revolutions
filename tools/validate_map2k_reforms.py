"""Execute the limited arithmetic/snapshot scripts as models, not the game."""
import itertools,math
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2k_work import ROOT,GAME
from map2k_imperial_principles import GROUPS,PRINCIPLE_FILE,GROUP_FILE,VALUES_FILE,REFORM_EFFECTS

def execute_loss(nodes,variables,globals_):
 def val(x):
  if x.startswith('var:'):return variables.get(x[4:])
  if x.startswith('global_var:'):return globals_.get(x[11:])
  return float(x)
 def match(nodes):
  def one(n):
   if n.key=='OR':return any(one(x) for x in n.children())
   if n.key=='AND':return all(one(x) for x in n.children())
   if n.key=='NOT':return not all(one(x) for x in n.children())
   if n.key=='has_variable':return n.value in variables
   if n.key=='has_global_variable':return n.value in globals_
   a,b=val(n.key),val(n.value)
   if a is None or b is None:return False
   return {'=':lambda:a==b,'?=':lambda:a==b,'>':lambda:a>b,'>=':lambda:a>=b}[n.op]()
  return all(one(n) for n in nodes)
 took=False
 for n in nodes:
  if n.key in ['if','else_if']:
   allowed=(not took) if n.key=='else_if' else True
   passed=allowed and match(n.children('limit')[0].children())
   if passed:execute_loss([x for x in n.children() if x.key!='limit'],variables,globals_)
   took=took or passed if n.key=='else_if' else passed
  elif n.key=='set_variable':
   if isinstance(n.value,list):variables[n.one('name')]=val(n.one('value'))
   else:variables[n.value]=1
  elif n.key=='remove_variable':variables.pop(n.value,None)
  elif n.key=='change_variable':variables[n.one('name')]+=val(n.one('add'))
  else:raise ValueError('Unmodeled instruction '+n.key)
 return variables

def validate_reforms(check,node,textnode):
 pnodes=cw.parse((ROOT/PRINCIPLE_FILE).read_text(encoding='utf-8-sig'));pn={n.key:n for n in pnodes}
 check('twelve_imperial_principle_tiers',set(pn)=={p for levels in GROUPS.values() for p in levels})
 for i in range(1,4):
  diet=pn['aor1776_hre_diet_'+str(i)]
  leader=diet.children('leader_modifier')[0];part=diet.children('member_modifier')[0]
  check('diet_leader_only_resources:'+str(i),leader.one('country_influence_add')==str([50,250,1000][i-1]) and leader.one('country_aor1776_hre_authority_per_estate_add')==str(i*5) and not part.children('country_influence_add') and float(part.one('country_improve_relations_speed_mult'))==i/10)
  admin=pn['aor1776_hre_administration_'+str(i)].children('member_modifier')[0]
  costs=[n for n in admin.children() if n.key.startswith('country_institution_cost_')]
  check('administration_institution_cost_not_tax_capacity:'+str(i),bool(costs) and all(float(n.value)==-i/10 for n in costs) and math.isclose(float(admin.one('country_bureaucracy_mult')),i*.05) and not any(n.key.startswith('state_tax_capacity') for n in admin.children()))
  check('principle_cohesion_gate_and_supplied_icon:'+str(i),all('current_cohesion_number' in textnode(pn[levels[i-1]].children('possible')) and cw.scalar(pn[levels[i-1]].one('icon')).startswith('gfx/interface/icons/principles_icons/aor1776_hre_') and (ROOT/cw.scalar(pn[levels[i-1]].one('icon'))).exists() for levels in GROUPS.values()))
 ident=node('common/power_bloc_identities/1776_imperial_federation.txt','identity_aor1776_imperial_federation')
 check('imperial_mandates_not_rank_or_member_bonus',ident.one('mandate_progress')=='aor1776_hre_authority_progress' and all(float(n.value)==0 for n in ident.children('power_bloc_modifier')[0].children() if n.key.startswith('power_bloc_mandate_progress_per_')))
 lognode=node(VALUES_FILE,'aor1776_hre_log_divisor');lookup={}
 for n in lognode.children('if'):
  limit=n.children('limit')[0].children()[0]
  if limit.op=='=':lookup[int(limit.value)]=float(n.one('add'))
 check('log_lookup_exact_for_every_possible_roster_size',all(abs(1+lookup.get(n,0)-(1+math.log(n)))<1e-9 for n in range(1,38)))
 def progress(c,n):return max(0,c-40)/(1+lookup.get(n,math.log(128) if n>128 else 0))
 check('authority_never_negative_for_0_to_100_cohesion',all(progress(c,n)>=0 for c in range(101) for n in range(1,501)))
 check('authority_zero_below_threshold',all(progress(c,n)==0 for c in range(41) for n in range(1,129)))
 check('log_progress_decreasing_with_member_count_not_subtraction',all(progress(80,n)>progress(80,n+1)>0 for n in range(1,128)))
 check('diminishing_marginal_membership_penalty',all((progress(80,n)-progress(80,n+1))>(progress(80,n+1)-progress(80,n+2)) for n in range(1,127)))
 rawprogress=textnode(node(VALUES_FILE,'aor1776_hre_authority_progress'))
 check('actual_gain_script_uses_positive_divisor','aor1776_hre_log_divisor' in rawprogress and 'divide' in rawprogress and 'power_bloc_rank' not in rawprogress)
 tracker=node(REFORM_EFFECTS,'aor1776_hre_track_principle_order')
 check('acquisition_order_tracks_groups_not_upgrades','has_principle_group' in textnode(tracker) and 'has_principle"' not in textnode(tracker))
 loss=node(REFORM_EFFECTS,'aor1776_hre_apply_succession_loss_to_snapshot')
 groups=list(GROUPS)
 failures=[];fixtures=0
 for levels in itertools.product(range(4),repeat=4):
  active=[i for i,l in enumerate(levels) if l]
  if not active:continue
  for order in itertools.permutations(active):
   globals_={'aor1776_hre_order_'+groups[g]:j+1 for j,g in enumerate(order)}
   flags={'aor1776_hre_saved_'+GROUPS[groups[g]][levels[g]-1]:1 for g in active}
   result=execute_loss(loss.children(),flags.copy(),globals_)
   actual={p for p in result if p.startswith('aor1776_hre_saved_aor1776_hre_')}
   expected=set(flags);last=order[-1]
   if len(active)>1:expected.remove('aor1776_hre_saved_'+GROUPS[groups[last]][levels[last]-1])
   elif levels[last]>1:
    expected.remove('aor1776_hre_saved_'+GROUPS[groups[last]][levels[last]-1]);expected.add('aor1776_hre_saved_'+GROUPS[groups[last]][levels[last]-2])
   fixtures+=1
   if actual!=expected:failures.append((levels,order))
 check('succession_loss_executes_all_tiers_and_acquisition_orders',not failures,f'{fixtures} limited-script fixtures; not engine tests; failures {failures[:4]}')
 check('snapshot_penalty_cannot_change_old_bloc',not any(n.key in {'add_principle','remove_principle','create_power_bloc','join_power_bloc'} for n in cw.walk(loss.children())))
 install=node('common/scripted_effects/1776_imperial_constitution.txt','aor1776_hre_install_elected_country')
 check('same_country_native_leader_branch_preserves_principles','scope:hre_old_imperial_country' in textnode(install.children('if')[0].children('limit')) and 'aor1776_hre_apply_succession_loss_to_snapshot' not in textnode(install.children('if')[0]))
 penalty=next(n for n in cw.walk(install.children()) if n.key=='if' and n.children('aor1776_hre_apply_succession_loss_to_snapshot'))
 check('loss_requires_actual_election_and_country_change','aor1776_hre_election_pending' in textnode(penalty.children('limit')) and 'hre_old_imperial_country' in textnode(penalty.children('limit')))
 defense=textnode(node('common/scripted_effects/1776_imperial_constitution.txt','aor1776_hre_defend_external_attack'))
 check('three_circle_war_obligations_and_internal_neutrality',all(x in defense for x in ['aor1776_hre_group_circles','aor1776_hre_circles_2','aor1776_hre_circles_3','add_target_backers','add_initiator_backers','remove_target_backers','remove_initiator_backers']))
 safe=textnode(node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_reform_safe'))
 check('centralization_requires_peace_cohesion_and_no_external_union',all(k in safe for k in ['is_at_war','75','aor1776_hre_four_pillars_max','top_overlord','is_in_same_power_bloc']))
 maxcheck=textnode(node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_four_pillars_max'))
 check('centralization_exactly_four_max_tiers',all(ls[2] in maxcheck for ls in GROUPS.values()) and 'principle_internal_trade' not in maxcheck)
 for stage in [1,2,3]:
  n=node(REFORM_EFFECTS,'aor1776_hre_stage_'+str(stage));lim=textnode(n.children('if')[0].children('limit'))
  check('reform_effect_rechecks_stage_and_cooldown:'+str(stage),'aor1776_hre_reform_stage' in lim and 'aor1776_hre_reform_cooldown' in lim and 'aor1776_hre_reform_safe' in lim)
 check('centralization_unification_only_on_explicit_final_button','annex' not in textnode(node(REFORM_EFFECTS,'aor1776_hre_reform_controller')) and 'annex' in textnode(node(REFORM_EFFECTS,'aor1776_hre_stage_3')))
 for kind,autonomy in [('protectorate',2),('crownland',1)]:
  n=node('common/subject_types/1776_imperial_reforms.txt','subject_type_aor1776_hre_'+kind)
  check('native_imperial_subject_level_and_no_rank_exclusion:'+kind,n.one('autonomy_level')==str(autonomy) and n.one('overlord_must_be_higher_rank')=='no' and n.one('can_have_subjects')=='yes')
  pact=node('common/diplomatic_actions/1776_imperial_subjects.txt','aor1776_hre_'+kind).children('pact')[0]
  check('centralized_subject_no_tribute_or_free_exit:'+kind,pact.one('income_transfer')=='0' and all(pact.children(k)[0].one('always')=='no' for k in ['actor_can_break','target_can_break']))
 native='common/power_bloc_principle_groups/00_power_bloc_principle_groups.txt'
 old=cw.parse((GAME/native).read_text(encoding='utf-8-sig'));new=cw.parse((ROOT/native).read_text(encoding='utf-8-sig'))
 def normalized(ns):return [(n.key,[qa.norm(x) for x in n.children() if not (x.key=='blocking_identity' and x.value=='identity_aor1776_imperial_federation')]) for n in ns]
 check('all_native_principle_groups_preserved_except_HRE_exclusion',normalized(old)==normalized(new))
 check('all_twenty_three_other_groups_explicitly_block_HRE',len(new)==23 and all(any(cw.scalar(x.value)=='identity_aor1776_imperial_federation' for x in n.children('blocking_identity')) for n in new))
 imperial_groups=cw.parse((ROOT/GROUP_FILE).read_text(encoding='utf-8-sig'))
 check('only_four_groups_not_blocked_for_HRE',set(n.key for n in imperial_groups)==set(GROUPS) and all(n.one('unlocking_identity')=='identity_aor1776_imperial_federation' and not n.children('blocking_identity') for n in imperial_groups))
 rel='common/power_bloc_principles/00_power_bloc_principles.txt'
 base=cw.parse((GAME/rel).read_text(encoding='utf-8-sig'));locked=cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
 guard=qa.norm(cw.parse('NOT = { exists = power_bloc power_bloc ?= { has_identity = identity:identity_aor1776_imperial_federation } }')[0])
 check('native_principle_HRE_guard_uses_optional_missing_bloc_link',guard[2][1][1]=='?=')
 check('all_sixty_nine_native_tiers_hidden_and_unselectable_for_HRE',len(locked)==69 and all(len(n.children(field))==1 and sum(qa.norm(x)==guard for x in n.children(field)[0].children())==1 for n in locked for field in ['visible','possible']))
 originals={n.key:n for n in base}
 def unlocked(n):
  children=[]
  for x in n.children():
   if x.key in ['visible','possible']:
    remainder=[qa.norm(c) for c in x.children() if qa.norm(c)!=guard]
    if remainder or originals[n.key].children(x.key):children.append([x.key,x.op,remainder])
   else:children.append(qa.norm(x))
  return [n.key,n.op,children]
 check('native_principles_all_other_fields_and_conditions_preserved',[unlocked(n) for n in locked]==[qa.norm(n) for n in base])
 check('all_imperial_tiers_use_runtime_member_modifier_not_obsolete_participant_block',all(bool(n.children('member_modifier')) and bool(n.children('member_modifier')[0].children()) and not n.children('participant_modifier') for n in pnodes))
