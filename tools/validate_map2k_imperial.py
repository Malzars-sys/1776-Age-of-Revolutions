"""Differential MAP2K validation. Static checks/models are not engine tests."""
import csv,json,collections as C,re,subprocess,os
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective,values
from map2k_work import ROOT,GAME,OUT,BASE,GIT,sha
from map2k_patch import MOVES,NEW,ELECTORS
from map2k_imperial_system import compile_system
def node(path,key):return next(n for n in cw.parse((ROOT/path).read_text(encoding='utf-8-sig')) if n.key==key)
def textnode(n):return json.dumps([qa.norm(x) for x in n] if isinstance(n,list) else qa.norm(n),ensure_ascii=False)
def profiles(base,folder):
 out=C.Counter()
 for p in effective(ROOT,GAME,'common/history/'+folder):
  rel=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else None
  raw=base['originals'].get(rel,p.read_text(encoding='utf-8-sig')) if base else p.read_text(encoding='utf-8-sig')
  for s in cw.walk(cw.parse(raw)):
   if not s.key.startswith('s:STATE_'):continue
   for r in s.children():
    if not r.key.startswith('region_state:'):continue
    for b in r.children('create_pop' if folder=='pops' else 'create_building'):
     omitted={'size'} if folder=='pops' else {'add_ownership'}
     sig=json.dumps([qa.norm(n) for n in b.children() if n.key not in omitted],ensure_ascii=False,sort_keys=True)
     count=int(b.one('size')) if folder=='pops' else sum(int(n.value) for n in cw.walk(b.children()) if n.key=='levels' and not isinstance(n.value,list))
     out[(s.key,sig)]+=count
 return out
def csvout(name,rows):
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def validate():
 b=json.loads(BASE.read_text());a=qa.inventory();tests=[]
 def check(k,result,detail=''):
  tests.append(dict(test=k,status='PASS' if result else 'FAIL',detail=detail))
 check('world_population',sum(r['count'] for r in a['pops'])==835804980)
 check('culture_religion_counts',a['pops']==b['inventory']['pops'] and a['resolved_demographics']==b['inventory']['resolved_demographics'])
 check('every_population_attribute_by_region',profiles(None,'pops')==profiles(b,'pops'),'Counts, religion, culture, wealth/status and all other written create_pop attributes')
 check('building_levels',a['building_levels_written']==b['inventory']['building_levels_written'])
 check('PM_reserves_and_other_building_attributes_weighted_by_level',profiles(None,'buildings')==profiles(b,'buildings'))
 check('military_formations_and_units',a['units']==b['inventory']['units'])
 check('no_new_history_reference_errors',not [e for e in a['errors'] if e not in b['inventory']['errors']],f"Inherited errors: {len(b['inventory']['errors'])}")
 check('no_new_duplicate_RGBs',a['duplicates']==b['inventory']['duplicates'],f"Inherited duplicate RGBs: {len(a['duplicates'])}")
 owners=qa.counter(a['owners']);before=qa.counter(b['inventory']['owners']);expected=before.copy()
 for sid,old,new,rgb in MOVES:expected[(rgb,sid,old)]-=1;expected[(rgb,sid,new)]+=1
 check('exactly_five_approved_RGB_transfers',+expected==owners)
 check('four_capitals_owned',all([data[0],tag] in a['states'] for tag,data in NEW.items()))
 compiled=compile_system();parses=[];asset_errors=[]
 for rel,raw in compiled.items():
  if rel.endswith('.txt'):
   try:ns=cw.parse(raw);parses.append(rel)
   except Exception as e:check('syntax:'+rel,False,str(e));continue
   for n in cw.walk(ns):
    if n.key in {'icon','texture','background','video','pattern'} and isinstance(n.value,str):
     path=cw.scalar(n.value)
     if path.startswith('gfx/') and not (ROOT/path).exists() and not (GAME/path).exists():asset_errors.append((rel,path))
  stored=(ROOT/rel).read_text(encoding='utf-8-sig')
  check('compiler_matches_runtime:'+rel,stored==raw.lstrip('\ufeff'))
 check('all_generated_scripts_parse',len(parses)==sum(rel.endswith('.txt') for rel in compiled),f'{len(parses)} script files')
 check('referenced_icons_and_event_images_exist',not asset_errors,str(asset_errors))
 for p in effective(ROOT,GAME,'common/history/power_blocs'):
  if p.name!='00_power_blocs.txt':continue
  aus=next(n for n in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))) if n.key=='c:AUS')
  members=[cw.scalar(n.value) for n in cw.walk(aus.children()) if n.key=='member']
  check('imperial_members_not_duplicated',len(members)==len(set(members)))
  check('four_electorates_in_starting_bloc',all('c:'+t in members for t in NEW))
 ef='common/scripted_effects/1776_imperial_constitution.txt'
 install=node(ef,'aor1776_hre_install_elected_country');reuse=install.children('if')[0]
 check('same_leader_branch_has_no_bloc_reset',not any(n.key in {'create_power_bloc','join_power_bloc','leave_power_bloc','add_principle','remove_principle'} for n in cw.walk(reuse.children())) and bool(reuse.children('aor1776_hre_finish_investiture')))
 check('no_unverified_leave_or_destroy_effects',not any(n.key in {'leave_power_bloc','destroy_power_bloc','disband_power_bloc'} for n in cw.walk(install.children())))
 snapshot=node(ef,'aor1776_hre_snapshot_principles');restore=node(ef,'aor1776_hre_restore_principles')
 registered=json.loads((OUT/'PRINCIPLE_SNAPSHOT_SCHEMA.json').read_text());all_levels={x for g,ls in registered for x in ls}
 saved={cw.scalar(n.value).removeprefix('principle:') for n in cw.walk(snapshot.children()) if n.key=='has_principle'}
 restored={cw.scalar(n.value) for n in cw.walk(restore.children()) if n.key=='add_principle'}
 check('all_registered_principle_levels_snapshot_and_restore',saved==restored==all_levels,f'{len(registered)} groups, {len(all_levels)} levels')
 for g,levels in registered:
  for level in levels:
   # Execute the actual compiled ordered if/else_if tests against one active tier.
   selected=[]
   for n in snapshot.children():
    tested=[cw.scalar(q.value).removeprefix('principle:') for q in cw.walk(n.children()) if q.key=='has_principle']
    if tested==[level]:selected+=[cw.scalar(q.value) for q in cw.walk(n.children()) if q.key=='set_variable']
   recovered=[cw.scalar(q.value) for n in restore.children() if any(cw.scalar(q.value) in selected for q in cw.walk(n.children()) if q.key=='has_variable') for q in cw.walk(n.children()) if q.key=='add_principle']
   check('principle_roundtrip:'+level,recovered==[level])
 electorate=node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_elector')
 title_refs={n.key[2:] for n in cw.walk(electorate.children()) if n.key.startswith('c:')}
 check('nine_legal_electoral_titles_no_GDP_award',title_refs==set(ELECTORS.values()) and len(title_refs)==9 and 'gdp' not in textnode(electorate) and 'country_rank' not in textnode(electorate))
 hook=node('common/on_actions/1776_imperial_constitution.txt','aor1776_hre_death_hook')
 check('Joseph_death_not_Maria_theresa_death', 'global_var:aor1776_hre_emperor_person' in textnode(hook) and 'aor1776_hre_emperor_character' in textnode(hook) and 'aor1776_hre.2' in textnode(hook))
 check('Maria_character_history_unchanged',b['originals']['common/history/characters/aus.txt'].split('first_name = "Joseph"')[0]==(ROOT/'common/history/characters/aus.txt').read_text(encoding='utf-8-sig').split('first_name = "Joseph"')[0])
 tally=node(ef,'aor1776_hre_tally_ballot');cast=node(ef,'aor1776_hre_cast_vote')
 check('strict_majority_and_runoff_not_plurality','aor1776_hre_twice_votes' in textnode(tally) and any(n.key=='var:aor1776_hre_twice_votes' and n.op=='>' for n in cw.walk(tally.children())) and 'aor1776_hre_election_deadlocked' in textnode(tally))
 check('duplicate_votes_guarded','aor1776_hre_voted' in textnode(cast.children('if')[0].children('limit')[0]))
 action=node('common/diplomatic_actions/1776_imperial_actions.txt','aor1776_hre_request_restitution');pact=node('common/diplomatic_actions/1776_imperial_actions.txt','aor1776_imperial_obligation')
 forced=action.children('ai')[0].children('accept_score')[0].children('if')[0]
 check('obligation_direction_emperor_owes_holder','owes_obligation_to' in textnode(forced) and 'scope:actor' in textnode(forced) and 'root' in textnode(forced))
 check('pact_zero_cost_zero_tribute_no_native_overlord',pact.children('pact')[0].one('cost')=='0' and pact.children('pact')[0].one('income_transfer')=='0' and not any(n.key in {'subject_type','subject_relation'} for n in cw.walk(pact.children())))
 check('pact_does_not_bypass_filtered_military_calls',not pact.children('pact')[0].children('auto_support_type'))
 defend=node(ef,'aor1776_hre_defend_external_attack')
 check('external_defense_internal_exclusion','remove_target_backers' in textnode(defend) and 'remove_initiator_backers' in textnode(defend) and 'add_target_backers' in textnode(defend))
 check('eligible_estates_called_for_liberation_play','dp_aor1776_hre_subject_release' in textnode(defend) and 'aor1776_hre_called_initiator_PRU' in textnode(defend) and 'add_initiator_backers' in textnode(defend) and 'is_subject_of' in textnode(defend))
 release=node(ef,'aor1776_hre_release_imperial_subjects')
 capture=release.children('every_subject_or_below')[0]
 check('liberation_snapshot_only_legal_imperial_subjects',capture.children('limit')[0].one('aor1776_hre_member')=='yes' and capture.one('set_variable')=='aor1776_hre_release_selected')
 release_pass=next(n for n in release.children('every_country') if n.children('make_independent'))
 check('liberation_independent_not_transferred_to_emperor',release_pass.children('limit')[0].one('has_variable')=='aor1776_hre_release_selected' and release_pass.one('make_independent')=='yes' and not any(n.key in {'annex','create_diplomatic_pact'} for n in cw.walk(release.children())))
 check('subjects_snapshot_before_mutating_dependencies',release.children().index(capture)<release.children().index(release_pass))
 init=node(ef,'aor1776_hre_initialize')
 check('no_automatic_starting_subject_release','aor1776_hre_release_imperial_subjects' not in textnode(init) and 'make_independent' not in textnode(init))
 request_release=node('common/diplomatic_actions/1776_imperial_actions.txt','aor1776_hre_request_subject_release')
 check('imperial_liberation_action_external_targets_only','aor1776_hre_external_imperial_overlord' in textnode(request_release) and 'aor1776_hre_emperor' in textnode(request_release))
 goal_release=node('common/war_goal_types/1776_imperial_war_goals.txt','aor1776_hre_subject_release')
 check('liberation_goal_calls_same_release_effect',goal_release.one('kind')=='custom' and goal_release.one('target_type')=='country' and 'aor1776_hre_release_imperial_subjects' in textnode(goal_release.children('on_enforced')))
 newgoal=node('common/war_goal_types/1776_imperial_war_goals.txt','aor1776_hre_liberate_estate')
 check('legacy_goal_hidden_new_goal_requires_refusal',goal_release.children('possible')[0].one('always')=='no' and 'aor1776_hre_release_refused' in textnode(newgoal.children('possible')) and 'is_subject' in textnode(newgoal.children('possible')))
 release_penalty=node(ef,'aor1776_hre_record_release_refusal')
 check('release_refusal_infamy_antispam','aor1776_hre_release_penalty' in textnode(release_penalty.children('if')[0].children('limit')) and [n.value for n in cw.walk(release_penalty.children()) if n.key=='change_infamy']==['5'] and '3650' in textnode(release_penalty))
 member=node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_member')
 legal_tags={n.key[2:] for n in cw.walk(member.children()) if n.key.startswith('c:')}
 # Dependency fixture: a nested estate must survive emancipation of its
 # parent; non-imperial possessions and seceded estates must remain untouched.
 graph={'LUB':'SWE','MEC':'SWE','MST':'MEC','FIN':'SWE','HAN':'GBR','HOH':'PRU','HOL':'DENNOR'}
 original_graph=graph.copy();seceded={'MST'}
 def descendant(tag,holder):
  seen=set()
  while tag in original_graph and tag not in seen:
   seen.add(tag);tag=original_graph[tag]
   if tag==holder:return True
  return False
 chosen={t for t in graph if t in legal_tags and t not in seceded and descendant(t,'SWE')}
 for t in chosen:graph.pop(t)
 check('release_fixture_excludes_colonies_other_overlords_and_secession',chosen=={'LUB','MEC'} and graph=={'MST':'MEC','FIN':'SWE','HAN':'GBR','HOH':'PRU','HOL':'DENNOR'})
 chosen_all={t for t in original_graph if t in legal_tags and descendant(t,'SWE')}
 check('release_fixture_snapshots_indirect_subjects',chosen_all=={'LUB','MEC','MST'})
 ledger=json.loads((OUT/'IMPERIAL_DE_JURE_REGISTRY.json').read_text());rights={r['rgb']:r for r in ledger}
 returned=node(ef,'aor1776_hre_return_requested_provinces');instructions=[]
 for n in cw.walk(returned.children()):
  if n.key=='set_owner_of_provinces':instructions.append((cw.scalar(n.one('country')).removeprefix('c:'),values(n,'provinces')))
 check('restitution_RGBs_and_recipients_match_frozen_registry',len(instructions)==len(rights) and all(len(rs)==1 and rights[rs[0]]['beneficiary']==t for t,rs in instructions))
 released_returns=node(ef,'aor1776_hre_return_released_subject_provinces')
 release_instructions=[(cw.scalar(n.one('country')).removeprefix('c:'),values(n,'provinces')) for n in cw.walk(released_returns.children()) if n.key=='set_owner_of_provinces']
 check('released_subject_returns_match_territorial_registry',C.Counter((t,tuple(rs)) for t,rs in release_instructions)==C.Counter((t,tuple(rs)) for t,rs in instructions) and 'scope:hre_request_state' not in textnode(released_returns))
 sample={r['rgb']:r['beneficiary'] for r in ledger};misheld=[r['rgb'] for r in ledger if r['beneficiary']=='PRU'][:2]
 for rgb in misheld:sample[rgb]='LUB'
 sample['UNREGISTERED']='LUB'
 for target,rgbs in release_instructions:
  for rgb in rgbs:
   if sample[rgb]=='LUB' and target!='LUB':sample[rgb]=target
 check('liberation_returns_wrong_lands_without_emperor_annexation',all(sample[rgb]=='PRU' for rgb in misheld) and sample['UNREGISTERED']=='LUB' and all(sample[r['rgb']]==r['beneficiary'] for r in ledger))
 # Independent territory fixtures using the ACTUAL compiled transfer list.
 for holder,region in [('BAV','STATE_LOWER_SILESIA'),('FRA','STATE_LOWER_SILESIA'),('PRU','STATE_RHINELAND')]:
  sample={r['rgb']:r['beneficiary'] for r in ledger};selected=[r['rgb'] for r in ledger if r['state']==region]
  for rgb in selected:sample[rgb]=holder
  sample['UNREGISTERED_PROVINCE']=holder;before_fixture=sample.copy()
  for target,rgbs in instructions:
   for rgb in rgbs:
    if rights[rgb]['state']==region and sample[rgb]==holder and target!=holder:sample[rgb]=target
  check('restitution_fixture:'+holder+':'+region,all(sample[x]==rights[x]['beneficiary'] for x in selected) and sample['UNREGISTERED_PROVINCE']==holder and all(sample[x]==v for x,v in before_fixture.items() if x not in selected))
 penalty=node(ef,'aor1776_hre_record_external_refusal')
 check('refusal_penalty_5_per_country_region_not_spammable',all(n.value=='5' for n in cw.walk(penalty.children()) if n.key=='change_infamy') and any(n.key=='NOT' for n in cw.walk(penalty.children())) and '3650' in textnode(penalty))
 statecheck=node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_restitution_state')
 check('AI_state_prefilter_requires_no_target_scope','scope:target_country' not in textnode(statecheck))
 for lang in ['english','french']:
  raw=(ROOT/f'localization/{lang}/1776_imperial_constitution_l_{lang}.yml').read_text(encoding='utf-8-sig')
  keys=re.findall(r'^ ([^ :]+):0 ',raw,re.M)
  check('localization_unique:'+lang,len(keys)==len(set(keys)))
  check('localized_electoral_countries_and_choices:'+lang,all(t in keys and 'aor1776_hre.vote_'+t in keys for t in NEW))
 diplomacy={p:h for p,h in b['hashes'].items() if p.startswith('common/history/diplomacy/')}
 check('all_historical_diplomatic_pacts_including_Hanover_unchanged',bool(diplomacy) and all((ROOT/p).exists() and sha(ROOT/p)==h for p,h in diplomacy.items()))
 warrel='common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt'
 oldwar=cw.parse(b['originals'][warrel]);newwar=cw.parse((ROOT/warrel).read_text(encoding='utf-8-sig'))
 def goals(tree):return C.Counter((cw.scalar(n.one('holder')),cw.scalar(n.one('type')),cw.scalar(n.one('target_state'))) for n in cw.walk(tree) if n.key=='add_war_goal')
 added=C.Counter({('c:IR1','conquer_state','s:STATE_KHUZESTAN.region_state:ARB'):1,('c:OMA','take_treaty_port','s:STATE_FARS.region_state:PER'):1})
 check('Iraq_Zand_exactly_two_restored_goals',goals(newwar)==goals(oldwar)+added)
 check('Iraq_Zand_counteroffensive_and_no_explicit_TUR_intervention',any(n.key=='c:IR1' for n in newwar[0].children()) and 'c:TUR' not in (ROOT/warrel).read_text(encoding='utf-8-sig') and 'c:ARB' in textnode(newwar))
 changed=[p for p,h in b['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
 allowed=set(json.loads((OUT/'PLAN.json').read_text())['files'])|set(compiled)
 check('all_other_protected_runtime_and_MAP_reports_unchanged',set(changed)<=allowed,str(sorted(set(changed)-allowed)))
 git={k:subprocess.check_output([GIT,*args],cwd=ROOT,text=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}).strip() for k,args in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
 check('main_HEAD_refs_index_unchanged',git==b['git'])
 check('province_bitmap_unchanged',sha(__import__('map2c_work').source_bitmap())==b['bitmap_sha256'])
 from validate_map2k_feedback import validate_feedback
 validate_feedback(check,node,textnode,ledger)
 from validate_map2k_reforms import validate_reforms
 validate_reforms(check,node,textnode)
 from validate_map2k_repairs import validate_repairs
 validate_repairs(check,node,textnode,ledger)
 from validate_map2k_dashboard import validate_dashboard
 validate_dashboard(check,node,textnode)
 from validate_map2k_demand_feedback import validate_demand_feedback
 validate_demand_feedback(check,node,textnode)
 from validate_map2k_atlas_access import validate_atlas_access
 validate_atlas_access(check,node,textnode)
 from validate_map2k_electoral_choices import validate_electoral_choices
 validate_electoral_choices(check,node,textnode)
 status='PASS_STATIC_ENGINE_PENDING' if all(t['status']=='PASS' for t in tests) else 'FAIL_STATIC'
 report=dict(status=status,tests=tests,world_population=835804980,territorial_RGB_changes=len(MOVES),de_jure_registered_provinces=len(ledger),engine_tested=False,native_version_observed='1.13.11',engine_limitations=['create_power_bloc and join_power_bloc with an already-member founder must be tested; a failure preserves the old bloc and raises a pending marker','Hanover/GBR, Holstein/DENNOR and Swedish imperial subjects: war participation against an external overlord, custom liberation enforcement and bloc rejoining require engine tests; failed bloc rejoining is marked and retried monthly','Prestige-driven native leadership contests cannot be disabled per identity with a verified API; monthly constitutional restoration is a guarded fallback','Deadlocked election remains open; no plurality is installed','Extinct beneficiary countries are not recreated automatically'],inherited_history_errors=b['inventory']['errors'],changed_protected_files=changed,git=git,checkpoint_commit='adfa30da1cf497470322036d4a8b5e6db49ea32b')
 report['engine_limitations'] += ['Imperial expulsion catalyst interception, daily rejoining and the native six-month join cooldown require engine testing; the native AI kick decision is not absolutely disabled by a verified per-identity API', 'New journal widgets, dynamic demand lists, response popups, electoral treaty and thirty-day deliberation require a restarted engine test', 'Yellow imperial geography is a journal map; no verified main-map filter for arbitrary state modifiers was found']
 (OUT/'MAP2K_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 csvout('MAP2K_TERRITORIAL_CHANGES.csv',[dict(province_RGB=rgb,state=sid,previous_owner=old,new_owner=new,status='DOCUMENTED_GAMEPLAY_APPROXIMATION_USER_APPROVED',population_method='Exact conservation; geometric proportional subdivision, NOT a historical census') for sid,old,new,rgb in MOVES])
 csvout('MAP2K_POPULATION_VALIDATION.csv',[dict(state=r['state'],previous_owner=r['before_owner'],new_owner=r['after_owner'],culture=r['culture'],religion=r['religion'],before=r['before'],remaining=r['remaining'],transferred=r['transferred'],delta=r['delta'],method=r['method']) for r in json.loads((OUT/'PLAN.json').read_text())['population']])
 unresolved=[dict(topic='Native succession transfer',status='REQUIRES_ENGINE_TEST',action=report['engine_limitations'][0]),dict(topic='Personal unions',status='REQUIRES_ENGINE_TEST',action=report['engine_limitations'][1]),dict(topic='Native leadership contests',status='DOCUMENTED_ENGINE_LIMIT',action=report['engine_limitations'][2]),dict(topic='Detailed electoral boundaries and urban locators',status='GAMEPLAY_APPROXIMATION',action='Approved existing RGBs approximate historical territories; no new historical polygon certainty is claimed'),dict(topic='Annexed claimant',status='FUTURE_FLAVOR',action=report['engine_limitations'][4]),dict(topic='MAP2J local report',status='DOCUMENTED_MISSING_REPORT',action='User validated MAP2J in game; no separate local MAP2J folder was present at baseline capture')]
 csvout('MAP2K_UNRESOLVED.csv',unresolved)
 print(status,len(tests),'checks;',len(ledger),'registered provinces')
 for t in tests:
  if t['status']=='FAIL':print('FAIL',t['test'],t['detail'])
 return 0 if status.startswith('PASS') else 1
if __name__=='__main__':raise SystemExit(validate())
