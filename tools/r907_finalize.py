"""R9-07 final safety amendment and combined current-workspace verification."""
import json,collections as C,sys
from audit_hbc_1776 import ROOT,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,ownership
from validate_diplomacy_ottoman_1776 import parse,scalar,normalized
from central01 import cohorts
from r904 import assigns
import r907,r907_pampas
OUT=r907.OUT;ST=r907.ST;PP=r907.PP
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def hub_names():
 assert not (OUT/'HUB_NAMES_AMENDMENT.json').exists();files={}
 for l in ['french','english']:
  rel=f'localization/{l}/replace/1776_r907_chaco_malvinas_l_{l}.yml';p=ROOT/rel
  old=text(p);assert old.count('HUB_NAME_STATE_SOUTH_ATLANTIC_ISLANDS_')==5
  files[rel]=encoded(p,old.replace('HUB_NAME_STATE_SOUTH_ATLANTIC_ISLANDS_','aor1776_r907_malvinas_'))
 files['common/scripted_effects/1776_r907_malvinas_names.txt']=('''# State scope: only the Spanish-owned split portion. No global hub override.
aor1776_r907_malvinas_names = {
 if = { limit = { state_region = s:STATE_SOUTH_ATLANTIC_ISLANDS owner = { c:SC4 ?= this } }
'''+''.join('  set_hub_name = { type = '+k+' name = aor1776_r907_malvinas_'+k+' }\n' for k in ['city','port','farm','mine','wood'])+''' }
}
''').encode()
 files['common/on_actions/17_1776_r907_malvinas_names.txt']=('''on_game_started = { on_actions = { aor1776_r907_malvinas_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_r907_malvinas_initialize } }
on_state_created = { on_actions = { aor1776_r907_malvinas_update } }
on_state_owner_change = { on_actions = { aor1776_r907_malvinas_update } }
aor1776_r907_malvinas_initialize = { effect = { every_state = { aor1776_r907_malvinas_names = yes } } }
aor1776_r907_malvinas_update = { effect = { aor1776_r907_malvinas_names = yes } }
''').encode()
 manifest={'input_sha256':{},'output_sha256':{}}
 for rel,b in files.items():
  p=ROOT/rel;manifest['input_sha256'][rel]=sha(p) if p.exists() else None
  if rel.endswith('.txt'):assert not p.exists();parse(b.decode())
  if p.exists():q=OUT/'hub_names_before'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
 for rel,b in files.items():
  p=ROOT/rel;assert (sha(p) if p.exists() else None)==manifest['input_sha256'][rel];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);manifest['output_sha256'][rel]=sha(p)
 dump('HUB_NAMES_AMENDMENT.json',manifest)
def amend():
 assert not (OUT/'SAFETY_AMENDMENT.json').exists()
 # Only undo our own transfer of this token; preserve all other current blocks.
 own=ownership();rgb='x5E9DB3';sid='STATE_SOUTH_ATLANTIC_ISLANDS';assert own[rgb]=={(sid,'SC4')}
 p=ROOT/ST;before=p.read_bytes();raw=text(p);n=state_nodes(raw)[sid];ed=[]
 for z in n.children('create_state'):
  t=scalar(z.one('country'))[2:];rr=set(provs(z,'owned_provinces'));b=z.children('owned_provinces')[0]
  if t=='SC4':rr.remove(rgb)
  elif t=='GBR':rr.add(rgb)
  else:raise AssertionError(t)
  ed.append((b.start,b.end,'owned_provinces = '+rgb_block(rr)))
 out=encoded(p,edit(raw,ed));parse(out.decode('utf-8-sig'));q=OUT/'safety_before'/ST;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(before)
 expected=sha(p);assert p.read_bytes()==before;p.write_bytes(out)
 dump('SAFETY_AMENDMENT.json',{'date':'2026-10-28','rgb':rgb,'from':'SC4','to':'GBR','reason':'Retain a passable province for the preexisting British composite-region population. Fine chronology of Port Egmont is also unresolved. This is a provisional retained western sector, not historical certification of continued British administration. No irreversible choice/new State Region or fabricated compensatory population transfer.','input_sha256':expected,'output_sha256':sha(p),'earlier_validation_results':'Pre-amendment observations retained; final combined check supersedes only installed ownership count.'})
def verify():
 ma=load('PATCH.json');mb=r907_pampas.load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();own=ownership();checks={}
 for r in [ST,PP]:assert ma['output_sha256'][r]==mb['input_sha256'][r]
 checks['two_preparations_form_exact_hash_chain']=True
 targets=[v for v in r907.MOVES if v[1]!='x5E9DB3']+[(s,r,'SC4','PAT') for s,rr in r907_pampas.MOVES.items() for r in rr]
 old=assigns(text(OUT/'before'/ST));expected=old.copy()
 for s,r,b,t in targets:assert expected[r,s,b]==1;expected[r,s,b]-=1;expected[r,s,t]+=1
 actual=assigns(text(ROOT/ST));checks['exactly_30_authorized_final_transfers']=+expected==actual
 def cnt(c):
  z=C.Counter()
  for (r,s,t),v in c.items():z[r]+=v
  return z
 checks['no_new_duplicate_or_unowned_RGB']=cnt(old)==cnt(actual)
 expectedhash={**ma['output_sha256'],**mb['output_sha256'],**load('HUB_NAMES_AMENDMENT.json')['output_sha256']};modified=set(expectedhash);expectedhash[ST]=load('SAFETY_AMENDMENT.json')['output_sha256']
 checks['nine_final_runtime_file_hashes_match']=len(modified)==9 and all(now.get(r)==h for r,h in expectedhash.items())
 checks['all_changed_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in modified if r.endswith('.txt'))
 oldns=state_nodes(text(OUT/'before'/ST));ns=state_nodes(text(ROOT/ST));changed={'STATE_SANTA_FE','STATE_SOUTH_ATLANTIC_ISLANDS','STATE_LA_PAMPA','STATE_RIO_NEGRO'}
 checks['all_other_state_blocks_preserved']=all(normalized([n])==normalized([oldns[s]]) for s,n in ns.items() if s not in changed)
 oldp=state_nodes(text(OUT/'before'/PP));newp=state_nodes(text(ROOT/PP));popchanged={'STATE_SOUTH_ATLANTIC_ISLANDS','STATE_LA_PAMPA','STATE_RIO_NEGRO'}
 checks['all_other_population_blocks_preserved']=all(normalized([n])==normalized([oldp[s]]) for s,n in newp.items() if s not in popchanged)
 oc=cohorts(text(OUT/'before'/PP));nc=cohorts(text(ROOT/PP));checks['world_population_delta_115_only']=sum(nc.values())-sum(oc.values())==115 and not (oc-nc)
 for s,size in [('STATE_LA_PAMPA','8871'),('STATE_RIO_NEGRO','3815')]:
  before=oldp[s].children('region_state:SC4')[0].children('create_pop');native=[z for z in before if z.one('culture')=='patagonian'];after=newp[s].children('region_state:PAT')[0].children('create_pop');other=newp[s].children('region_state:SC4')[0].children('create_pop');checks['intact_native_cohort_'+size]=len(native)==1 and native[0].one('size')==size and any(normalized([z])==normalized(native) for z in after) and normalized([z for z in before if z not in native])==normalized(other)
 checks['old_British_stock_unchanged']=normalized(oldp['STATE_SOUTH_ATLANTIC_ISLANDS'].children('region_state:GBR'))==normalized(newp['STATE_SOUTH_ATLANTIC_ISLANDS'].children('region_state:GBR'))
 pp=newp['STATE_SOUTH_ATLANTIC_ISLANDS'].children('region_state:SC4')[0].children('create_pop');checks['only_new_115_catholic_spanish_proxy']=len(pp)==1 and pp[0].one('size')=='115' and pp[0].one('culture')=='spanish' and pp[0].one('religion')=='catholic'
 regs={n.key:n for f in effective('map_data/state_regions') for n in parse(text(f))}
 checks['all_transferred_RGBs_valid_and_passable']=all(r in provs(regs[s],'provinces') and r not in provs(regs[s],'impassable') for s,r,b,t in targets)
 imp={r for n in regs.values() for r in provs(n,'impassable')}
 checks['every_affected_population_scope_has_passable_land']=all(any((s,rs.key.split(':')[1]) in v and r not in imp for r,v in own.items()) for s in popchanged|{'STATE_SANTA_FE'} for rs in newp[s].children() if rs.children('create_pop'))
 checks['western_reserve_and_other_islands_preserved']=all(own[r]=={('STATE_SOUTH_ATLANTIC_ISLANDS','GBR')} for r in ['x5E9DB3','x0CB556','xB0BDDF','xB5100C','xB5760C'])
 checks['SC4_insular_city_port_hubs_owned']=all(own[scalar(regs['STATE_SOUTH_ATLANTIC_ISLANDS'].one(k))]=={('STATE_SOUTH_ATLANTIC_ISLANDS','SC4')} for k in ['city','port'])
 checks['continental_donor_hubs_preserved']=all(own[scalar(regs[s].one(k))]=={(s,'SC4')} for s in r907_pampas.MOVES for k in ['city','mine','wood']) and own['x700090']=={('STATE_LA_PAMPA','SC4')}
 checks['colonial_guards_and_abandoned_SanFernando_preserved']=all(own[r]=={(s,t)} for r,s,t in [('xB63BAD','STATE_BAJO_PARAGUAY','SC4'),('xCCC385','STATE_BAJO_PARAGUAY','SC4'),('xE0C49E','STATE_CHACO','SC4'),('xB0C011','STATE_CHACO','GNI')])
 checks['all_existing_buildings_profiles_units_pacts_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/countries/','common/country_definitions/','common/history/military_formations/','common/history/diplomacy/')))
 checks['only_one_new_port_file']=set(r for r in now if r.startswith('common/history/buildings/') and r not in base)=={r907.PORT}
 checks['geometry_terrain_locators_unchanged']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/')))
 checks['all_prior_R9_CENTRAL_witnesses_preserved']=all(own[r]=={(s,t)} for r,s,t in [('xC564C3','STATE_ANTIOQUIA','WYU'),('x7B4B5E','STATE_GUAYANA','NET'),('x439BC2','STATE_GUAYANA','FRA'),('x6C6251','STATE_GUAYANA','NET'),('x3C0D20','STATE_PASTAZA','BRZ'),('x144683','STATE_ARAUCANIA','H91'),('xF2263F','STATE_LOS_RIOS','PAT'),('x4E1443','STATE_URUGUAY','BRZ'),('xB0243F','STATE_COSTA_RICA','G81'),('xBB820B','STATE_PANAMA','K81'),('x446C64','STATE_WEST_INDIES','C81')])
 checks['claims_retained']=all(any(scalar(z.value)==t for z in ns[s].children('add_claim')) for s,t in [('STATE_LA_PAMPA','c:SC4'),('STATE_RIO_NEGRO','c:SC4'),('STATE_SOUTH_ATLANTIC_ISLANDS','c:GBR')])
 for l in ['french','english']:
  for suffix,count in [('chaco_malvinas',7),('pampas',2)]:
   p=ROOT/f'localization/{l}/replace/1776_r907_{suffix}_l_{l}.yml';s=text(p);checks['localization_'+l+'_'+suffix]=p.read_bytes().startswith(b'\xef\xbb\xbf') and s.startswith('l_'+l+':') and len(__import__('re').findall(r'(?m)^\s+\w+:0 ',s))==count
 effects=text(ROOT/'common/scripted_effects/1776_r907_malvinas_names.txt');actions=text(ROOT/'common/on_actions/17_1776_r907_malvinas_names.txt')
 checks['hub_names_effect_restricted_to_region_and_SC4_owner']='state_region = s:STATE_SOUTH_ATLANTIC_ISLANDS owner = { c:SC4 ?= this }' in effects
 checks['hub_names_initialized_and_updated_without_monthly_loop']=all(k in actions for k in ['on_game_started','on_game_started_after_lobby','on_state_created','on_state_owner_change']) and 'monthly' not in actions
 checks['no_global_hub_names_override']=all('HUB_NAME_STATE_SOUTH_ATLANTIC_ISLANDS_' not in text(ROOT/f'localization/{l}/replace/1776_r907_chaco_malvinas_l_{l}.yml') for l in ['french','english'])
 checks['all_five_custom_hub_keys_in_both_languages']=all('aor1776_r907_malvinas_'+k+':0 ' in text(ROOT/f'localization/{l}/replace/1776_r907_chaco_malvinas_l_{l}.yml') for l in ['french','english'] for k in ['city','port','farm','mine','wood'])
 comparison=load('TECH_FINAL_COMPARISON.json');checks['no_added_or_removed_technology_findings']=all(not z['added'] and not z['removed'] for z in comparison.values())
 # The final safety amendment does not change any PM or building.
 checks['tech_final_snapshot_still_matches_buildings_and_profiles']=all(now.get(r)==h for r,h in r907_pampas.load('PREPARE_RUNTIME.json').items() if r.startswith(('common/history/buildings/','common/history/countries/','common/technology/','common/production_methods/')))
 external={r:{'before':base.get(r),'after':now.get(r)} for r in base.keys()|now.keys() if r not in modified and base.get(r)!=now.get(r)};dump('FINAL_CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change_since_first_prepare']=not external
 checks={k:bool(v) for k,v in checks.items()};dump('FINAL_VALIDATION.json',{'date':'2026-10-28','status':'PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL_STATIC','checks':checks,'passed':sum(checks.values()),'total':len(checks),'final_transfers':30,'engine_tested':False,'human_validated':False});dump('FINAL_PATCH_MANIFEST.json',expectedhash);dump('FINAL_RUNTIME_MANIFEST.json',now);print(json.dumps({'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v]}));assert all(checks.values())
if __name__=='__main__':
 if '--amend' in sys.argv:amend()
 elif '--hub-names' in sys.argv:hub_names()
 elif '--verify' in sys.argv:verify()
