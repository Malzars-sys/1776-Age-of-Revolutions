"""Independent MAP2H finishing invariants; native game tests remain player-owned."""
import collections as C,contextlib,io,json,re,subprocess
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from validate_map2f import population_profiles
from map_1776_audit import effective
from map2h_finishing import ROOT,GAME,OUT,BASE,GIT,sha,dump
import map2h_finishing_patch as patcher
def economic(inv):
 out=C.Counter()
 for row in inv['buildings']:
  sid,tag,body=row['key'];n=json.loads(body);rest=[v for v in n[2] if v[0]!='add_ownership']
  for own in [v for v in n[2] if v[0]=='add_ownership']:
   for h in own[2]:
    fields=[v for v in h[2] if v[0]!='levels'];holder=next((v[2] for v in fields if v[0]=='country'),'c:'+tag)
    for f in fields:
     if f[0]=='region' and holder=='c:INDOP' and f[2] in patcher.WHOLE:f[2]='STATE_NORTH_SUMATRA'
    out[json.dumps([sid,rest,h[0],fields],ensure_ascii=False,sort_keys=True)]+=row['count']*int(next(v[2] for v in h[2] if v[0]=='levels'))
 return out
def logical_allowed(n,tag,kind,present):
 if n.key=='OR':return any(logical_allowed(v,tag,kind,present) for v in n.children())
 if n.key=='AND':return all(logical_allowed(v,tag,kind,present) for v in n.children())
 if n.key=='is_country_type':return n.value==kind
 if n.key=='exists':assert n.value=='c:KAU';return present
 if n.key=='c:KAU':assert n.op=='=' and n.value=='ROOT';return present and tag=='KAU'
 raise AssertionError('Unexpected law eligibility token '+n.key)
def run():
 base=json.loads(BASE.read_text());before=base['inventory'];after=qa.inventory();changed,plan,old=patcher.transform(base);dump('PLAN.json',plan);checks=[]
 def check(name,ok,detail=None):
  checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(checks[-1]['status'],name,flush=True)
 expected=qa.counter(before['owners'])
 for r in plan['transfers']:
  k=r['rgb'],r['state'],'INDOP';assert expected[k]==1;expected[k]-=1;expected[r['rgb'],r['state'],r['after']]+=1
 check('exactly_22_RGBs_only_from_INDOP',+expected==qa.counter(after['owners']) and len(plan['transfers'])==22)
 check('all_other_sovereignties_MAP2A_to_H_preserved',qa.counter([r for r in before['owners'] if r['key'][2]!='INDOP'])==qa.counter([r for r in after['owners'] if r['key'][2] not in {'INDOP','TOB','KLT'}]))
 check('no_RGB_added_lost_or_redrawn',before['geometry']==after['geometry'] and {r['key'][0] for r in before['owners']}=={r['key'][0] for r in after['owners']} and sha(ROOT/'map_data/provinces.png')==base['hashes']['map_data/provinces.png'])
 check('44_existing_duplicates_unchanged',before['duplicates']==after['duplicates'] and len(after['duplicates'])==44)
 check('no_new_orphan_history_reference',not set(map(str,after['errors']))-set(map(str,before['errors'])),after['errors'])
 check('world_population_835804980_and_all_religions_cultures',sum(r['count'] for r in after['pops'])==835804980 and before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
 current=dict(old);current.update({p:(ROOT/p).read_text(encoding='utf-8-sig') for p in changed})
 bp,br,bd=population_profiles(old);ap,ar,ad=population_profiles(current)
 check('all_pop_fields_world_and_State_Region_conserved',bp==ap and br==ar)
 check('all_Kaurna_populations_attributes_identical',{k:v for k,v in bd.items() if k[1]=='KAU'}=={k:v for k,v in ad.items() if k[1]=='KAU'})
 check('building_levels_PM_reserves_economic_holders_preserved',before['building_levels_written']==after['building_levels_written'] and economic(before)==economic(after))
 check('only_seven_necessary_INDOP_HQ_references_moved',len(plan['headquarters'])==7 and all(r[1]=='INDOP' and r[3]=='STATE_NORTH_SUMATRA' for r in plan['headquarters']))
 check('all_units_formations_recruitments_identical',before['units']==after['units'])
 actual=[p for p,h in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
 check('only_planned_existing_files_changed',set(actual)=={p for p in changed if p in base['hashes']},actual)
 check('exact_reviewed_source_AST_and_localization',all(([qa.norm(n) for n in cw.parse(txt)]==[qa.norm(n) for n in cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))]) if p.endswith('.txt') else txt.lstrip('\ufeff')==(ROOT/p).read_text(encoding='utf-8-sig') for p,txt in changed.items()))
 check('military_characters_technologies_AI_journals_other_lots_byte_identical',all(sha(ROOT/p)==h for p,h in base['hashes'].items() if p.startswith(('common/history/military_formations/','common/history/characters/','common/technology/','common/production_methods/','common/ai_','common/journal_entries/','common/modifiers/','common/scripted_effects/1776_ai','events/','map_data/','gfx/'))))
 check('Kaurna_definition_stays_unrecognized_playable',before['countries']['KAU']==after['countries']['KAU'] and any(v[:1]==['country_type'] and v[2]=='unrecognized' for v in json.loads(after['countries']['KAU'])[2]))
 exceptions={'TOB','KLT','INDOP'}
 check('every_other_country_definition_unchanged',{k:v for k,v in before['countries'].items() if k not in exceptions}=={k:v for k,v in after['countries'].items() if k not in exceptions})
 for tag in ['TOB','KLT','INDOP','KAU']:
  n=json.loads(after['countries'][tag]);cap=next(v[2] for v in n[2] if v[0]=='capital');check(tag+'_capital_owned',[cap,tag] in after['states'],cap)
 check('two_reused_native_tags_no_new_tag',all(t in before['countries'] and not any(owner==t for _,owner in before['states']) for t in ['TOB','KLT']) and set(after['countries'])==set(before['countries']))
 # The law override must be equivalent to the native rule for every other tag.
 lawraw=cw.parse(changed['common/scripted_triggers/1776_map2h_kaurna_customary_laws.txt'])[0];rules=lawraw.children();eligible=lambda tag,typ,present:all(logical_allowed(n,tag,typ,present) for n in rules)
 identities=list(after['countries'])+['MISSING_COUNTRY'];kinds=['recognized','unrecognized','decentralized','colonial'];cases=0;ok=True
 for present in [False,True]:
  for tag in identities:
   for typ in kinds:
    expected_rule=typ=='decentralized' or (present and tag=='KAU' and typ=='unrecognized');ok &= eligible(tag,typ,present)==expected_rule;cases+=1
 check('country_specific_law_eligibility_model',ok,{'cases':cases,'other_tags_native_decentralized_rule_unchanged':True})
 for p,key,blocks in [('common/laws/00_governance_principles.txt','law_chiefdom',['can_enact','is_visible']),('common/laws/00_distribution_of_power.txt','law_elder_council',['is_visible'])]:
  oldnodes=cw.parse(old[p]);newnodes=cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))
  for n in oldnodes:
   if n.key==key:
    for name in blocks:b=n.children(name)[0];b.value=[cw.Node('aor1776_customary_laws_country_allowed','=','yes',0,0)]
  check('only_'+key+'_visibility_eligibility_extended',[qa.norm(n) for n in oldnodes]==[qa.norm(n) for n in newnodes])
 kau=next(n for n in cw.walk(cw.parse((ROOT/'common/history/countries/kau - kaurna.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:KAU');laws=[cw.scalar(n.value).removeprefix('law_type:') for n in kau.children('activate_law')]
 required={'law_chiefdom','law_elder_council','law_isolationism','law_subjecthood','law_no_womens_rights','law_serfdom','law_consumption_based_taxation','law_censorship','law_debt_slavery'}
 check('exact_user_requested_Kaurna_laws',set(laws)==required and len(laws)==len(required),laws)
 check('Kaurna_initial_technology_identical',[qa.norm(n) for n in kau.children('add_technology_researched')]==[qa.norm(n) for n in next(n for n in cw.walk(cw.parse(old['common/history/countries/kau - kaurna.txt'])) if n.key=='c:KAU').children('add_technology_researched')])
 catalog={n.key:n for p in effective(ROOT,GAME,'common/laws') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
 check('all_requested_laws_defined',required<=set(catalog))
 # Existing native chiefdom government accepts the law without requiring a decentralized country.
 gov=next(n for p in effective(ROOT,GAME,'common/government_types') for n in cw.parse(p.read_text(encoding='utf-8-sig')) if n.key=='gov_chiefdom');poss=gov.children('possible')[0]
 check('native_chiefdom_government_valid_for_playable_Kaurna',len(poss.children())==1 and poss.one('has_law_or_variant')=='law_type:law_chiefdom')
 check('no_authored_Kaurna_ruler_or_european_monarchy',not any(n.key=='create_character' for n in cw.walk(cw.parse(changed['common/history/countries/kau - kaurna.txt']))) and 'law_monarchy' not in laws)
 # Existing other Australian histories are untouched: no broad political overhaul.
 audit=json.loads((OUT/'AUDIT.json').read_text());other={k:v for k,v in audit['Australian_Indigenous'].items() if k!='KAU'}
 check('22_other_Australian_community_histories_unchanged',len(other)==22 and all(not any('republic' in law or 'voting' in law for law in h['explicit_laws']) for v in other.values() for h in v['history']) and all(sha(ROOT/p)==h for p,h in base['hashes'].items() if p.startswith('common/history/countries/') and p!='common/history/countries/kau - kaurna.txt'))
 dip=cw.parse(changed['common/history/diplomacy/1776_map2h_vietnam_rapprochement.txt']);truce=[n for n in cw.walk(dip) if n.key=='create_bidirectional_truce'];pacts=[n for n in cw.walk(dip) if n.key=='create_diplomatic_pact'];relations=[n for n in cw.walk(dip) if n.key=='set_relations']
 check('single_native_24_month_Trinh_TaySon_truce',len(truce)==1 and truce[0].one('country')=='c:TSN' and truce[0].one('months')=='24' and next(n for n in cw.walk(dip) if n.key=='c:DAI').children('create_bidirectional_truce'))
 check('only_Nguyen_TaySon_rivalries_no_permanent_Trinh_alliance',len(pacts)==2 and {(n.one('country'),n.one('type')) for n in pacts}=={('c:NGN','rivalry'),('c:TSN','rivalry')})
 check('temporary_rapprochement_and_Nguyen_hostility',len(relations)==2 and {(n.one('country'),n.one('value')) for n in relations}=={('c:TSN','20'),('c:NGN','-60')})
 check('native_truce_syntax_has_game_history_precedent','create_bidirectional_truce' in (GAME/'common/history/diplomacy/00_truces.txt').read_text())
 check('no_war_event_or_truce_refresh_script',not any(n.key in {'create_war','start_war','start_diplomatic_play','create_diplomatic_play','trigger_event','on_monthly_pulse','on_yearly_pulse'} for n in cw.walk(dip)) and not any('create_bidirectional_truce' in txt for p,txt in changed.items() if p!='common/history/diplomacy/1776_map2h_vietnam_rapprochement.txt'))
 for lang in ['english','french']:
  nm=(ROOT/f'localization/{lang}/NM_Countries_l_{lang}.yml').read_text(encoding='utf-8-sig');loc=(ROOT/f'localization/{lang}/replace/1776_map2h_communities_l_{lang}.yml').read_text(encoding='utf-8');keys=re.findall(r'^ ([A-Za-z0-9_]+):0 "[^"\r\n]*"$',loc,re.M)
  check(lang+'_names_unique_BOM_and_regional',loc.startswith('\ufeffl_'+lang+':') and set(keys)=={'TOB','TOB_ADJ','KLT','KLT_ADJ','aor1776_map2h_tapanuli'} and len(keys)==5 and re.search(r'^ INDOP: "'+('Communautés de Sumatra' if lang=='french' else 'Sumatran Communities')+'"$',nm,re.M) is not None)
  check(lang+'_other_country_names_preserved',re.sub(r'^ INDOP(?:_ADJ)?:.*$','',nm,flags=re.M)==re.sub(r'^ INDOP(?:_ADJ)?:.*$','',old[f'localization/{lang}/NM_Countries_l_{lang}.yml'],flags=re.M))
 check('flags_native_generic_pattern',(GAME/'gfx/coat_of_arms/patterns/pattern_horizontal_split_01.tga').is_file())
 check('no_dynamic_INDOP_TOB_KLT_name_override_conflict',all(n.key not in {'INDOP','TOB','KLT'} for p in effective(ROOT,GAME,'common/dynamic_country_names') for n in cw.parse(p.read_text(encoding='utf-8-sig'))))
 import validate_regional_infrastructure_shortage as infra
 for name,func in [('Ottoman_logical_models',cw.model_tests),('regional_infrastructure_IA_models',infra.model_tests)]:
  try:
   with contextlib.redirect_stdout(io.StringIO()):func()
   check(name,True)
  except Exception as exc:check(name,False,str(exc))
 check('primary_Git_HEAD_refs_index_unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==base['git']['refs'] and sha(ROOT/'.git/index')==base['git']['index'])
 populations=C.Counter()
 for r in after['regional_pop']:
  if r['key'][1] in {'INDOP','TOB','KLT','KAU'}:populations[r['key'][0]+'|'+r['key'][1]]+=r['count']
 status='PASS_STATIC' if all(c['status']=='PASS' for c in checks) else 'FAIL_STATIC'
 dump('VALIDATION.json',{'status':status,'checks':checks,'modified_files':plan['files'],'territorial_changes':plan['transfers'],'population_by_fragment':dict(populations),'population_world':835804980,'owner_transfers':22,'new_tags':0,'reused_tags':['TOB','KLT'],'bitmap_unchanged':True,'military_unchanged':before['units']==after['units'],'all_demographic_profiles_preserved':bp==ap and br==ar,'economic_profiles_preserved':economic(before)==economic(after),'headquarters_relocations':plan['headquarters'],'KAU_country_type':'unrecognized','truce':'DAI–TSN, 24 months; nominal expiration Jan1 1778, not historical treaty duration','native_game_test':'NOT_RUN; initial MAP2H was player-validated, this finish needs a fresh start. Chiefdom ruler UI can auto-generate a native representative; no named historical character invented. Native chiefdom transfer_of_power remains hereditary, an acknowledged engine abstraction.','commit_merge_push':'NOT_PERFORMED'})
 print(status,len(checks),'checks')
 for c in checks:
  if c['status']=='FAIL':print('FAILED',c['name'],c['detail'])
 assert status=='PASS_STATIC'
if __name__=='__main__':run()
