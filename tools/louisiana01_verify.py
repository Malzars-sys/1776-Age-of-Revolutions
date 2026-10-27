"""Independent staged/installed checks; preserves previous passes as dated evidence."""
from louisiana01 import *

def region_capacity(n):
 result=C.Counter(arable_land=int(n.one('arable_land')))
 for z in n.children('capped_resources'):
  for v in z.children():result['capped:'+v.key]+=int(v.value)
 for z in n.children('resource'):
  for v in z.children():
   if v.key in ['discovered_amount','undiscovered_amount']:result[scalar(z.one('type'))+':'+v.key]+=int(v.value)
 return result

def country_cohorts(raw):
 out=C.Counter()
 for sid,n in state_nodes(raw).items():
  for rs in n.children():
   if not rs.key.startswith('region_state:'):continue
   for p in rs.children('create_pop'):out[rs.key,pop_signature(p)]+=int(p.one('size'))
 return out

def main(staged=False):
 plan=load(OUT/'PLAN.json');patch=load(OUT/'PATCH.json');base=load(OUT/'BASELINE_RUNTIME.json');now=runtime();checks={}
 concurrent=load(OUT/'CONCURRENT_SHARED_CHANGES.json') if (OUT/'CONCURRENT_SHARED_CHANGES.json').exists() else None
 external=load(OUT/'CONCURRENT_FILES.json') if (OUT/'CONCURRENT_FILES.json').exists() else {}
 def get(rel):return text(OUT/'patch'/rel) if staged and rel in patch['output_sha256'] else text(ROOT/rel)
 def before(rel):return text(ROOT/rel) if staged else text(OUT/'before'/rel)
 checks['inputs_current' if staged else 'installed_hashes_current']=all(now.get(r)==h for r,h in patch['input_sha256' if staged else 'output_sha256'].items())
 checks['patch_hashes_intact']=all(sha(OUT/'patch'/r)==h for r,h in patch['output_sha256'].items())
 checks['no_unlisted_runtime_change']=all(now.get(r)==base.get(r) or (r in external and now.get(r)==external[r]['observed_sha256']) for r in now.keys()|base.keys() if r not in patch['output_sha256'])
 global_bitmap_unchanged=sha(ROOT/'map_data/provinces.png')==patch['bitmap_sha256']
 if not global_bitmap_unchanged and (OUT/'CONCURRENT_BITMAP_CHANGE.json').exists():
  proof=load(OUT/'CONCURRENT_BITMAP_CHANGE.json');source=ROOT/proof['baseline_path']
  old_pixels=np.asarray(Image.open(source).convert('RGB'));new_pixels=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'));x0,y0,x1,y1=proof['protected_roi']
  checks['bitmap_scope_unmodified_external_change_proved']=sha(source)==patch['bitmap_sha256'] and sha(ROOT/'map_data/provinces.png')==proof['current_sha256'] and np.array_equal(old_pixels[y0:y1,x0:x1],new_pixels[y0:y1,x0:x1])
 else:checks['bitmap_unmodified']=global_bitmap_unchanged
 own={r:set(map(tuple,v)) for r,v in load(OUT/'BASELINE_OWNERS.json').items()}
 if concurrent:
  source=text(OUT/'concurrent_snapshot'/ST);nodes=state_nodes(source);current_nodes=state_nodes(get(ST))
  checks['concurrent_shared_state_blocks_preserved']=all(normalized([current_nodes[s]])==normalized([nodes[s]]) for s in concurrent['states'])
  for r,v in list(own.items()):
   remaining={(s,t) for s,t in v if s not in concurrent['states']}
   if remaining:own[r]=remaining
   else:del own[r]
  for s in concurrent['states']:
   for cs in nodes[s].children('create_state'):
    for r in provs(cs,'owned_provinces'):own.setdefault('x'+r[1:].upper(),set()).add((s,scalar(cs.one('country'))[2:]))
 actual=C.defaultdict(set)
 for p in effective('common/history/states'):
  for sid,n in state_nodes(get(p.relative_to(ROOT).as_posix())).items():
   for cs in n.children('create_state'):
    for r in provs(cs,'owned_provinces'):actual['x'+r[1:].upper()].add((sid,scalar(cs.one('country'))[2:]))
 changed={v['rgb']:tuple(v['after']) for v in plan['transfers']}
 checks['every_planned_owner']=all(actual.get(r)=={v} for r,v in changed.items())
 checks['ownership_unchanged_elsewhere']=set(actual)==set(own) and all(actual[r]==v for r,v in own.items() if r not in changed)
 checks['no_new_ownerless_or_double_owner']=all(len(actual[r])==1 for r in changed) and {r for r,v in actual.items() if len(v)>1}=={r for r,v in own.items() if len(v)>1}
 regions={}
 for p in effective('map_data/state_regions'):
  contents=get(p.relative_to(ROOT).as_posix()) if p.is_relative_to(ROOT) else text(p)
  for n in parse(contents):regions[n.key]=n
 regs_before={n.key:n for n in parse(before(REG))}
 memberships=C.defaultdict(set)
 for sid,n in regions.items():
  for r in provs(n,'provinces'):memberships['x'+r[1:].upper()].add(sid)
 checks['moved_rgb_region_refs_unique']=all(memberships[r]=={s} for r,(s,t) in changed.items())
 checks['region_rgb_universe_conserved']=set().union(*(set(provs(n,'provinces')) for n in parse(get(REG))))==set().union(*(set(provs(n,'provinces')) for n in regs_before.values()))
 checks['all_state_ids_unique']=len({n.one('id') for n in regions.values()})==len(regions)
 checks['capacities_conserved']=region_capacity(regions[LA])+region_capacity(regions[WF])==region_capacity(regs_before[LA])+region_capacity(regs_before[WF])
 checks['region_fields_unchanged_elsewhere']=all(normalized([n])==normalized([regs_before[s]]) for s,n in regions.items() if s in regs_before and s not in {LA,WF,AR})
 for sid in [LA,AR,MO,WF]:
  cells=set(provs(regions[sid],'provinces'))
  checks['valid_hubs.'+sid]=all(not regions[sid].one(k) or scalar(regions[sid].one(k)) in cells for k in ['city','port','farm','mine','wood'])
 history=state_nodes(get(ST));oldhist=state_nodes(before(ST));claimchanges={r['state']:r for r in plan['claims']}
 checks['claims_match_plan']=all(sorted(scalar(v.value) for v in history[s].children('add_claim'))==r['after'] for s,r in claimchanges.items())
 checks['claims_outside_scope_unchanged']=all(normalized(n.children('add_claim'))==normalized(oldhist[s].children('add_claim')) for s,n in history.items() if s not in claimchanges)
 checks['western_claims_no_anachronistic_usa']=all('c:USA' not in [v.value for v in history[s].children('add_claim')] for s in LOU_CLAIMS|{'STATE_TEXAS'})
 checks['new_spain_texas_claim_preserved']='c:SC1' in [v.value for v in history['STATE_TEXAS'].children('add_claim')]
 checks['mountain_overlap_preserved']=set(v.value for v in history['STATE_COLORADO'].children('add_claim'))=={'c:LOU','c:SC1'}
 checks['no_population_or_identity_loss']=totals(get(PP))==totals(before(PP))
 checks['every_country_cohort_total_preserved']=country_cohorts(get(PP))==country_cohorts(before(PP))
 pp=state_nodes(get(PP))
 def pop(s,t):return sum(int(p.one('size')) for n in pp[s].children('region_state:'+t) for p in n.children('create_pop'))
 checks['posts_have_colonial_population']=pop(AR,'LOU')==400 and pop(MO,'LOU')==1600
 checks['restored_caddo_share_populated']=pop(LA,'CAD')==500
 shares={(s,cs.one('country')[2:]) for s,n in history.items() for cs in n.children('create_state')}
 checks['all_added_pop_scopes_exist']=all((s,t) in shares for s,t in [(LA,'CAD'),(AR,'LOU'),(MO,'LOU')])
 checks['buildings_units_and_country_profiles_unchanged']=all(now.get(r)==h or (r in external and now.get(r)==external[r]['observed_sha256']) for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/military_formations/','common/history/countries/','common/country_definitions/')))
 checks['lou_shares_explicitly_incorporated']=all(cs.one('state_type')=='incorporated' for sid,n in history.items() for cs in n.children('create_state') if cs.one('country')=='c:LOU')
 checks['british_parishes_in_west_florida']=all(actual[r]=={(WF,'GBR')} for r in BRIT) and len(provs(regions[WF],'provinces'))==12
 checks['all_modified_scripts_parse']=all(parse(get(r)) is not None for r in patch['output_sha256'] if r.endswith('.txt'))
 checks['localized_seats_utf8_bom']=all((OUT/'patch'/f'localization/{lang}/replace/1776_louisiana_seats_l_{lang}.yml').read_bytes().startswith(b'\xef\xbb\xbf') for lang in ['french','english'])
 a=bitmap();centers,adj,blocked=geometry(a,actual,{LA,AR,MO,WF,MS});lou={int(r[1:],16) for r,v in actual.items() if any(t=='LOU' for s,t in v)}
 checks['province_corridor_single_component']=len(components(adj,lou))==1
 for tag in ['QPW','CAD','GBR']:
  cells={int(r[1:],16) for r,v in actual.items() if any(t==tag and s in {LA,AR,MO,WF,MS} for s,t in v)}
  checks['no_stranded_regional_pocket.'+tag]=len(components(adj,cells))==1
 mask=np.isin(a,sorted(lou));start=next(v for v in plan['hubs'] if v['state']==LA)['pixel'];x,y=start
 parents,_=flood(a,mask,[y*a.shape[1]+x],blocked)
 reached={int(a[divmod(v,a.shape[1])]) for v in parents};checks['every_lou_province_land_reachable']=lou<=reached
 witnesses=[]
 for site in plan['sites']:
  r=site['rgb'];pixels=[u for u in parents if int(a[divmod(u,a.shape[1])])==int(r[1:],16)]
  checks['site_connected.'+site['name']]=bool(pixels) and actual[r]=={(site['state'],'LOU')}
  if pixels:
   u=min(pixels,key=lambda u:np.linalg.norm(np.array([u%a.shape[1],u//a.shape[1]])-site['projection']))
   witnesses.append(dict(site=site['name'],pixels=[[v%a.shape[1],v//a.shape[1]] for v in path(parents,u)],rgb=r))
 checks['lou_national_capital_owned']=any((LA,'LOU') in v for v in actual.values())
 for h in plan['hubs']:
  n=next(n for n in parse(get(LOC))[0].children('instances')[0].children() if n.one('id')==str(h['id']));v=[float(z.value) for z in n.children('position')[0].children()];r=f'x{int(a[int(a.shape[0]-v[2]),int(v[0])]):06X}'
  checks['locator_samples_its_hub.'+h['state']]=r==h['rgb']==scalar(regions[h['state']].one('city'))
 # Preserve exact footprints of approved earlier lots, independent of hashes.
 for tag in ['HBC','QUE','USA','IRO','CHE','MSC','NVS','SML','SC1']:
  checks['protected_footprint.'+tag]={r for r,v in own.items() if any(t==tag for s,t in v)}=={r for r,v in actual.items() if any(t==tag for s,t in v)}
 previous_path=load(OUT.parent/'COLONIES-01/FRONTIER/UPDATED_LAND_WITNESS.json')
 checks['hbc_quebec_colonies_land_witness_preserved']=all(f'x{int(a[v["pixel"][1],v["pixel"][0]]):06X}'==v['rgb'] and actual[v['rgb']]=={(v['state'],v['owner'])} for v in previous_path)
 dump(('STAGED_' if staged else '')+'VALIDATION.json',dict(date='2026-10-27',checks=checks,all_pass=all(checks.values()),global_bitmap_unchanged=global_bitmap_unchanged,external_bitmap_change_proof='CONCURRENT_BITMAP_CHANGE.json' if not global_bitmap_unchanged else None,engine_tested=False,status='PREPARED' if staged else 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',preexisting_double_owner_count=sum(len(v)>1 for v in own.values())))
 dump(('STAGED_' if staged else '')+'LAND_WITNESSES.json',witnesses)
 print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])))
 return all(checks.values())

if __name__=='__main__':sys.exit(0 if main('--staged' in sys.argv) else 1)
