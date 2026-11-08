"""Read-only live-mod checks; writes a new evidence result, never gameplay."""
from pathlib import Path
import sys,json,hashlib,re,collections as C,subprocess
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'AGENTS.md').exists())
sys.path.insert(0,str(ROOT/'tools'))
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
import map2l_registry as reg
from map2l_belgium import packed,components
from map_1776_audit import values
from map2b_patch import state
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((OUT/'BASELINE.json').read_text());old=json.loads((OUT/'INVENTORY_BEFORE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text());plan=json.loads((OUT/'PLAN.json').read_text());install=json.loads((OUT/'INSTALLATION.json').read_text())
now=qa.inventory();a=packed(OUT/'provinces_before.png');z=packed(ROOT/'map_data/provinces.png')
checks=[]
def ck(id,yes,detail=None):checks.append(dict(id=id,passed=bool(yes),detail=detail))
changed={r['file']:r for r in install['changes']}
ck('installed_version_matches_reviewed_manifest',all(sha(ROOT/p)==v['after'] for p,v in changed.items()),list(changed))
unrelated=[p for p,h in b['runtime_hashes'].items() if p not in changed and (not(ROOT/p).is_file() or sha(ROOT/p)!=h)]
ck('all_other_runtime_files_preserved',not unrelated,unrelated)
ck('all_old_archives_and_attestations_preserved',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in b['archive_hashes'].items()),len(b['archive_hashes']))
ck('originals_backed_up_exactly',all(sha(OUT/'backups'/p)==v['before'] for p,v in changed.items()))
ck('bitmap_equals_exact_reviewed_candidate',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
ck('native_bitmap_dimensions_unchanged',a.shape==z.shape)
oldown={r['key'][0]:(r['key'][1],r['key'][2]) for r in old['owners']};newown={r['key'][0]:(r['key'][1],r['key'][2]) for r in now['owners']}
expected=oldown|{r['rgb']:(r['state'],r['owner']) for r in g['assignments']}
ck('world_ownership_exactly_declared',newown==expected)
changes=set()
for rgb,(sid,owner) in oldown.items():
 if rgb in g['parents']:continue
 if sid.startswith('STATE_') and (owner!='BAV' or sid not in ('STATE_BAVARIA','STATE_FRANCONIA')):
  pass
# Compare every changed physical cell; unchanged pixels keep their old owner.
yy,xx=np.where(a!=z)
for y,x in zip(yy,xx):
 before='x'+format(int(a[y,x]),'06X');after='x'+format(int(z[y,x]),'06X')
 if oldown[before][1]!=newown[after][1]:
  changes.add((int(x),int(y)))
ck('exact_156_owner_changes',changes=={tuple(c) for s in g['sub_lots'] for c in s['cells']} and len(changes)==156)
ck('only_BAV_to_KPF_changes',all(oldown['x'+format(int(a[y,x]),'06X')][1]=='BAV' and newown['x'+format(int(z[y,x]),'06X')][1]=='KPF' for x,y in changes))
ck('all_non_BAV_physical_cores_unchanged',all(oldown['x'+format(int(a[y,x]),'06X')][1]=='BAV' for y,x in zip(yy,xx)))
ck('all_old_RGBs_retained',set(np.unique(a))<=set(np.unique(z)))
ck('exact_new_RGB_set',set(np.unique(z))-set(np.unique(a))=={int(r['rgb'][1:],16) for r in g['new_provinces']})
ck('all_affected_RGBs_connected',all(len(components(z==int(r['rgb'][1:],16)))==1 for r in g['assignments']))
ck('all_affected_RGBs_exact_cells',all({(int(x),int(y)) for y,x in zip(*np.where(z==int(r['rgb'][1:],16)))}=={tuple(c) for c in r['cells']} for r in g['assignments']))
ck('new_RGBs_owned_once',all(sum(r['count'] for r in now['owners'] if r['key'][0]==n['rgb'])==1 for n in g['new_provinces']))
ck('new_RGBs_in_original_economic_region',all(now['geometry'][n['rgb']]==old['geometry'][n['parent_rgb']] for n in g['new_provinces']))
ck('original_region_assignments_preserved',all(now['geometry'].get(k)==v for k,v in old['geometry'].items()))
ck('only_KPF_Bavaria_state_added',set(map(tuple,now['states']))-set(map(tuple,old['states']))=={('STATE_BAVARIA','KPF')})
ck('all_previous_states_retained',set(map(tuple,old['states']))<=set(map(tuple,now['states'])))
terr={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))}
ck('new_terrains_inherited_from_parents',all(terr[n['rgb'].upper()]==terr[n['parent_rgb'].upper()] for n in g['new_provinces']))
oldraw=(OUT/'backups/map_data/state_regions/00_west_europe.txt').read_text(encoding='utf-8-sig');raw=(ROOT/'map_data/state_regions/00_west_europe.txt').read_text(encoding='utf-8-sig')
def nonref(text):return {n.key:[qa.norm(c) for c in n.children() if c.key not in ('provinces','prime_land')] for n in cw.parse(text)}
ck('hubs_resources_terrain_arable_region_fields_preserved',nonref(oldraw)==nonref(raw))
ck('no_hub_reference_or_physical_locator_move',g['hub_rebindings']==[] and all(sha(ROOT/p)==h for p,h in b['runtime_hashes'].items() if 'locator' in p))
ck('world_raw_demographics_conserved',old['pops']==now['pops'])
ck('world_resolved_demographics_conserved',old['resolved_demographics']==now['resolved_demographics'])
expected_pop=C.Counter({tuple(r['key']):r['count'] for r in old['regional_pop']})
for row in plan['population_allocations']:
 religion=row['religion'] if row['religion']!='DEFAULT' else 'DEFAULT:'+row['culture']
 expected_pop[(row['state'],'BAV',row['culture'],religion)]-=row['after']['KPF']
 expected_pop[(row['state'],'KPF',row['culture'],religion)]+=row['after']['KPF']
ck('regional_population_transfer_exact_by_profile',expected_pop==C.Counter({tuple(r['key']):r['count'] for r in now['regional_pop']}))
ck('transferred_population_55115',sum(r['after']['KPF'] for r in plan['population_allocations'])==55115)
ck('buildings_levels_PM_and_economic_holders_preserved',old['buildings']==now['buildings'] and old['building_levels_written']==now['building_levels_written'])
ck('military_units_and_recruitment_preserved',old['units']==now['units'] and all(sha(ROOT/p)==h for p,h in b['runtime_hashes'].items() if 'military_formations' in p))
ck('country_definitions_and_technology_profiles_preserved',old['countries']==now['countries'] and all(sha(ROOT/p)==h for p,h in b['runtime_hashes'].items() if '/countries/' in p or '/technolog' in p))
ck('inherited_errors_unchanged',old['errors']==now['errors'],len(now['errors']))
ck('inherited_duplicate_assignments_unchanged',old['duplicates']==now['duplicates'],len(now['duplicates']))
ck('prior_Innbaiern_175_conserved',newown['xFDA6CB']==('STATE_AUSTRIA','BAV') and int((z==0xFDA6CB).sum())==175)
ck('Obernberg_and_Passau_cores_conserved',newown['xEDC000'][1]=='PAS' and int((z==0xEDC000).sum())==4 and int((z==0xEDBA00).sum())==40)
ck('Salzburg_core_conserved',newown['xEDBB00'][1]=='SLZ' and int((z==0xEDBB00).sum())==12)
ledger=json.loads(reg.active_registry_path().read_text());previous=json.loads((OUT/'REGISTRY_BEFORE.json').read_text());m=json.loads((OUT/'REGISTRY_MIGRATION.json').read_text());oldledger={r['rgb']:r for r in previous};newledger={r['rgb']:r for r in ledger}
ck('611_unique_imperial_titles',len(ledger)==len(newledger)==611)
ck('all_599_old_title_records_preserved',all(newledger[k]==v for k,v in oldledger.items()))
ck('only_12_subdivision_titles_added',set(newledger)-set(oldledger)=={r['rgb'] for r in g['new_provinces']})
ck('all_titles_follow_current_owners',all(newown[r['rgb']]==(r['state'],r['beneficiary']) for r in ledger))
ck('new_migration_is_last_in_approved_chain',reg.approved_lot_dirs()[-1]==OUT)
ck('imperial_footprint_unchanged',all(r in oldledger for r in g['parents']) and all(r['rgb'] in newledger for r in g['assignments']) and m['extent_added_cells']==m['extent_removed_cells']==[])
ck('no_new_country_elector_or_free_city',m['new_members']==m['free_cities']==[] and m['country_additions']=={})
# Full live registry membership and registration branches must be emitted for all titles.
triggers=(ROOT/'common/scripted_triggers/1776_imperial_constitution.txt').read_text(encoding='utf-8-sig')
missing=[r['rgb'] for r in ledger if 'p:'+r['rgb'] not in triggers]
ck('every_title_has_live_compiler_reference',not missing,missing)
ck('compiled_derivatives_installed_exactly',all((ROOT/p).read_bytes().decode('utf-8')==v for p,v in json.loads((OUT/'EXPECTED_TEXT.json').read_text()).items()))
parse_errors=[]
for row in install['changes']:
 p=ROOT/row['file']
 if p.suffix=='.txt':
  try:cw.parse(p.read_text(encoding='utf-8-sig'))
  except Exception as e:parse_errors.append([row['file'],str(e)])
ck('all_installed_scripts_parse',not parse_errors,parse_errors)
ck('all_touched_localizations_have_BOM',all((ROOT/r['file']).read_bytes().startswith(b'\xef\xbb\xbf') for r in install['changes'] if r['file'].endswith('.yml')))
ck('Git_HEAD_and_index_preserved',(ROOT/'.git/HEAD').read_text()==b['git_branch'] and sha(ROOT/'.git/index')==b['git_index'])
ck('no_human_runtime_receipt_created',install['human_runtime_receipts']==0 and all(s['attestation'] is None for s in install['sub_lots']))
ck('grouped_player_protocol_prepared',(OUT/'PLAYER_TEST_PROTOCOL_GROUPED.md').is_file())
result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',task_ids=['SC6-SWABIAN-ARBITRATIONS'],passed=sum(r['passed'] for r in checks),total=len(checks),failed=[r for r in checks if not r['passed']],checks=checks,engine_test=False,human_attestation=None,provisional_demographic_redistribution=True)
p=OUT/'VALIDATION.json';assert not p.exists();p.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
(OUT/'INVENTORY_AFTER.json').write_bytes((json.dumps(now,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({k:result[k] for k in ['status','passed','total','failed']},ensure_ascii=False))
assert result['status']=='PASS'
