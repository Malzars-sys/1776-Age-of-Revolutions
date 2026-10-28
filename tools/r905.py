"""R9-05: guarded installation of researched Amazonian colonial cores.

Whole existing provinces; no new nation, population, building or bitmap.
See SOURCES.md for the distinction between historical sites and gameplay links.
"""
import collections as C,json,re,sys
import numpy as np
from PIL import Image
from audit_hbc_1776 import ROOT,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,state_nodes,rgb_block,ownership
from validate_diplomacy_ottoman_1776 import parse,scalar,normalized
from central01 import cohorts
from r904 import assigns
from hbc02_map_candidates import graph

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-05'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt'
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def prepare():
 assert not (OUT/'APPLIED.json').exists();g=load('GEOMETRY_PROPOSAL.json');raw=text(ROOT/ST);ns=state_nodes(raw);edits=[];transfers=[]
 for sid,v in g['regions'].items():
  n=ns[sid];old=n.children('create_state');current={r:scalar(z.one('country'))[2:] for z in old for r in provs(z,'owned_provinces')};assert current==v['before']
  target=v['after'];newtags=set(target.values())-set(current.values())
  for z in old:
   tag=scalar(z.one('country'))[2:];rgbs=[r for r,t in target.items() if t==tag]
   if not rgbs:edits.append((z.start,z.end,''))
   else:
    p=z.children('owned_provinces')[0];edits.append((p.start,p.end,'owned_provinces = '+rgb_block(rgbs)))
  additions=[]
  for tag in sorted(newtags):additions.append('create_state = { country = c:'+tag+' owned_provinces = '+rgb_block([r for r,t in target.items() if t==tag])+' state_type = incorporated }')
  # Captaincy pretensions, not control of the forests. A statewide Portuguese
  # claim on Maynas would overstate the Tabatinga post and is deliberately absent.
  claim='SC2' if sid=='STATE_PASTAZA' else 'BRZ'
  if not any(scalar(z.value)=='c:'+claim for z in n.children('add_claim')):additions.append('add_claim = c:'+claim)
  edits.append((n.end-1,n.end-1,'\n\t\t'+'\n\t\t'.join(additions)+'\n\t'))
  transfers.extend(dict(state=sid,rgb=r,before=current[r],after=t) for r,t in target.items() if t!=current[r])
 files={ST:encoded(ROOT/ST,edit(raw,edits))};ledger=[]
 raw=text(ROOT/PP);ns=state_nodes(raw);edits=[]
 for sid,source in [('STATE_AMAZONAS','AP7'),('STATE_MATO_GROSSO','AP7'),('STATE_PARA','BRZ')]:
  n=ns[sid];rs=n.children('region_state:'+source)[0];selected=[]
  for z in rs.children('create_pop'):
   culture=scalar(z.one('culture'));size=int(z.one('size'))
   take=(sid=='STATE_AMAZONAS' and (culture in ['amazonic','afro_brazilian'] or culture=='amazonian' and size==8640)) or (sid=='STATE_MATO_GROSSO' and culture in ['paulista','afro_brazilian']) or (sid=='STATE_PARA' and culture=='amazonian')
   if take:selected.append(z)
  assert selected,sid;dest='AP7' if sid=='STATE_PARA' else 'BRZ';assert not n.children('region_state:'+dest)
  for z in selected:
   edits.append((z.start,z.end,''));ledger.append(dict(state=sid,before=source,after=dest,culture=scalar(z.one('culture')),size=int(z.one('size')),pop_type=scalar(z.one('pop_type')),religion=scalar(z.one('religion'))))
  edits.append((n.end-1,n.end-1,'\n\t\tregion_state:'+dest+' = {\n'+ '\n'.join(raw[z.start:z.end] for z in selected)+'\n\t\t}\n\t'))
 # Maynas: existing Andean cohorts with the mission administration, existing
 # forest cohorts with native autonomy. No religion or culture is rewritten.
 n=ns['STATE_PASTAZA'];rs=n.children('region_state:SC3')[0];groups={'SC2':[],'AP7':[],'BRZ':[]};tabatinga=False
 assert len(n.children())==1
 for z in rs.children('create_pop'):
  s=raw[z.start:z.end];culture=scalar(z.one('culture'));amount=int(z.one('size'));dest='AP7' if culture=='amazonian' else 'SC2'
  if culture=='amazonian' and amount==22455:
   # Tabatinga (74) alone, per Sampaio cited by Coutinho p.48. Javari's 131
   # belong to a separate site whose mapping is not certified by this token.
   # Redistribution proxy includes registered absentees; not a new census.
   size=z.children('size')[0];a=size.start-z.start;b=size.end-z.start
   groups['BRZ'].append(s[:a]+'size = 74'+s[b:]);s=s[:a]+'size = 22381'+s[b:];amount-=74;tabatinga=True
   ledger.append(dict(state='STATE_PASTAZA',before='SC3',after='BRZ',culture=culture,size=74,pop_type=scalar(z.one('pop_type')),religion=scalar(z.one('religion')),basis='1775 Tabatinga registered stock alone; separate Javari excluded; not ethnic census or 1776 exact count'))
  groups[dest].append(s);ledger.append(dict(state='STATE_PASTAZA',before='SC3',after=dest,culture=culture,size=amount,pop_type=scalar(z.one('pop_type')),religion=scalar(z.one('religion'))))
 assert tabatinga
 replacement='\n'.join('region_state:'+tag+' = {\n'+'\n'.join(parts)+'\n}' for tag,parts in groups.items());edits.append((rs.start,rs.end,replacement));files[PP]=encoded(ROOT/PP,edit(raw,edits))
 # The legacy AP7 aggregate includes multiple peoples. Do not retroproject the
 # Kayapo ethnonym over the entire Acre, Negro, Maynas and Mato Grosso.
 for lang,name in [('french','Peuples amazoniens'),('english','Amazonian peoples')]:
  rel=f'localization/{lang}/mod_v2content_l_{lang}.yml';raw=text(ROOT/rel);matches=list(re.finditer(r'(?m)^(\s*AP7:\s*(?:\d+\s*)?)"Kayapo"',raw));assert len(matches)==1
  m=matches[0];files[rel]=encoded(ROOT/rel,raw[:m.start()]+m[1]+'"'+name+'"'+raw[m.end():])
 manifest=dict(input_sha256={},output_sha256={},geometry_sha256=sha(OUT/'GEOMETRY_PROPOSAL.json'))
 for rel,data in files.items():
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  p=ROOT/rel;b=OUT/'before'/rel;q=OUT/'patch'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data);b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(p.read_bytes());manifest['input_sha256'][rel]=sha(p);manifest['output_sha256'][rel]=sha(q)
 dump('PATCH.json',manifest);dump('PREPARE_RUNTIME.json',runtime());dump('TRANSFERS.json',transfers);dump('POPULATION_LEDGER.json',ledger)
 print(json.dumps(dict(files=len(files),province_transfers=len(transfers),population_redistributed=sum(r['size'] for r in ledger),population_added=0)))
def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists();assert sha(OUT/'GEOMETRY_PROPOSAL.json')==m['geometry_sha256']
 assert all(sha(ROOT/r)==h for r,h in m['input_sha256'].items()),'Shared content changed; re-examine before installing'
 assert all(sha(OUT/'patch'/r)==h for r,h in m['output_sha256'].items())
 for r in m['output_sha256']:(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
def verify():
 m=load('PATCH.json');base=load('PREPARE_RUNTIME.json');now=runtime();checks={};old=assigns(text(OUT/'before'/ST));new=assigns(text(ROOT/ST));desired=old.copy();transfers=load('TRANSFERS.json');g=load('GEOMETRY_PROPOSAL.json')
 checks['installed_manifest_exact']=all(sha(ROOT/r)==h for r,h in m['output_sha256'].items())
 checks['modified_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'] if r.endswith('.txt'))
 for row in transfers:
  r,s,b,t=[row[k] for k in ['rgb','state','before','after']];assert desired[r,s,b]==1;desired[r,s,b]-=1;desired[r,s,t]+=1
 checks['exact_authorized_province_transfers']=+desired==new
 before=C.Counter();after=C.Counter()
 for (r,s,t),c in old.items():before[r]+=c
 for (r,s,t),c in new.items():after[r]+=c
 checks['no_new_duplicate_or_unowned_province']=before==after
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};own=ownership();ns=state_nodes(text(ROOT/ST));pop=state_nodes(text(ROOT/PP))
 checks['changed_rgb_belongs_to_declared_region']=all(r['rgb'] in provs(regs[r['state']],'provinces') for r in transfers)
 checks['no_empty_owner_portion']=all(provs(z,'owned_provinces') for sid in g['regions'] for z in ns[sid].children('create_state'))
 oldns=state_nodes(text(OUT/'before'/ST));oldpops=state_nodes(text(OUT/'before'/PP))
 checks['all_other_state_blocks_identical']=all(normalized([n])==normalized([oldns[s]]) for s,n in ns.items() if s not in g['regions'])
 checks['all_other_population_blocks_identical']=all(normalized([n])==normalized([oldpops[s]]) for s,n in pop.items() if s not in g['regions'])
 shares={(sid,scalar(z.one('country'))[2:]) for sid,n in ns.items() for z in n.children('create_state')}
 checks['population_scopes_have_land']=all((sid,rs.key.split(':')[1]) in shares for sid in g['regions'] for rs in pop[sid].children() if rs.children('create_pop'))
 checks['same_regional_population_culture_religion_and_status']=cohorts(text(OUT/'before'/PP))==cohorts(text(ROOT/PP))
 def totals(raw):return C.Counter({(sid,rs.key.split(':')[1]):sum(int(z.one('size')) for z in rs.children('create_pop')) for sid,n in state_nodes(raw).items() for rs in n.children()})
 prior=totals(text(OUT/'before'/PP));expected=prior.copy()
 for r in load('POPULATION_LEDGER.json'):expected[r['state'],r['before']]-=r['size'];expected[r['state'],r['after']]+=r['size']
 checks['population_owner_deltas_match_ledger']=+expected==+totals(text(ROOT/PP))
 checks['no_existing_building_or_country_profile_changed']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/countries/','common/country_definitions/','common/history/diplomacy/','common/history/military_formations/')))
 checks['bitmap_regions_terrain_and_locators_identical']=all(now.get(r)==h for r,h in base.items() if r.startswith(('map_data/','gfx/map/')))
 definitions={n.key:n for p in effective('common/country_definitions') for n in parse(text(p))}
 checks['all_affected_capitals_still_owned']=all((scalar(definitions[t].one('capital')),t) in shares for t in ['BRZ','SC2','SC3','AP7'])
 checks['no_new_country']=all(now.get(r)==h for r,h in base.items() if r.startswith('common/country_definitions/')) and not any(r.startswith('common/country_definitions/') and r not in base for r in now)
 checks['old_spanish_pastaza_portion_removed_without_orphan_pop']=('STATE_PASTAZA','SC3') not in shares and not pop['STATE_PASTAZA'].children('region_state:SC3')
 checks['tabatinga_has_74_existing_people']=totals(text(ROOT/PP))['STATE_PASTAZA','BRZ']==74
 checks['all_new_colonial_portions_incorporated']=all(any(z.one('country')=='c:'+t and z.one('state_type')=='incorporated' for z in ns[s].children('create_state')) for s,t in [('STATE_AMAZONAS','BRZ'),('STATE_MATO_GROSSO','BRZ'),('STATE_PASTAZA','BRZ'),('STATE_PASTAZA','SC2')])
 checks['para_hubs_keep_portuguese_owner']=all(own[scalar(regs['STATE_PARA'].one(k))]=={('STATE_PARA','BRZ')} for k in ['city','port','farm','mine','wood'])
 checks['no_blanket_portuguese_claim_on_maynas']=not any(scalar(z.value)=='c:BRZ' for z in ns['STATE_PASTAZA'].children('add_claim'))
 checks['captaincy_claims_and_quito_claim_present']=all(any(scalar(z.value)=='c:'+t for z in ns[s].children('add_claim')) for s,t in [('STATE_AMAZONAS','BRZ'),('STATE_MATO_GROSSO','BRZ'),('STATE_PARA','BRZ'),('STATE_PASTAZA','SC2')])
 # Passability: side contacts >=2 raster pixels, exclude declared impassables
 # and special adjacency barriers. This is topology, not engine market access.
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2];imp={int(r[1:],16) for n in regs.values() for r in provs(n,'impassable')}
 import csv
 from audit_hbc_1776 import GAME
 rel='map_data/adjacencies.csv';p=ROOT/rel if (ROOT/rel).exists() else GAME/rel;blocked=set()
 for row in csv.DictReader(p.open(encoding='utf-8-sig'),delimiter=';'):
  if all(row.get(k,'').startswith('x') for k in ['From','To']) and (row.get('Type') in ['sea','impassable'] or row.get('adjacency_rule_name','').strip()):blocked.add(frozenset(int(row[k][1:],16) for k in ['From','To']))
 all_brz={int(r[1:],16) for r,v in own.items() if len(v)==1 and next(iter(v))[1]=='BRZ'}-imp
 adj=graph(a,np.array(sorted(all_brz),dtype=np.uint32));start=int(scalar(regs['STATE_PARA'].one('city'))[1:],16);seen={start};stack=[start]
 while stack:
  u=stack.pop()
  for v,w in adj[u].items():
   if v not in seen and w>=2 and frozenset([u,v]) not in blocked:seen.add(v);stack.append(v)
 changed_brz={int(r['rgb'][1:],16) for r in transfers if r['after']=='BRZ'};checks['new_portuguese_land_passably_connected_to_belem']=changed_brz<=seen
 # A mission network needs a colonial land exit, not an invented jungle road
 # all the way to Quito. Check its contacts with the preserved Spanish cores.
 spanish={int(r[1:],16) for r,v in own.items() if len(v)==1 and next(iter(v))[1] in ['SC2','SC3']}-imp;sa=graph(a,np.array(sorted(spanish),dtype=np.uint32));mission={int(r[1:],16) for r,t in g['regions']['STATE_PASTAZA']['after'].items() if t=='SC2'};border={r for r in spanish if any(s!='STATE_PASTAZA' for s,t in own[f'x{r:06X}'])};reached=set(border);stack=list(border)
 while stack:
  u=stack.pop()
  for v,w in sa[u].items():
   if v not in reached and w>=2 and frozenset([u,v]) not in blocked:reached.add(v);stack.append(v)
 checks['maynas_missions_have_passable_spanish_land_exit']=mission<=reached
 checks['no_new_portuguese_corridor_uses_impassable']=not (changed_brz&imp)
 # Stronger witness than a province graph: actual side-adjacent raster land,
 # respecting the same special barriers. No diagonal or sea connection.
 from hbc04_land_links import flood,path,pair
 blocked_bits={pair(*tuple(v)) for v in blocked};seed=int(np.flatnonzero(a.ravel()==start)[0]);parents,_=flood(a,np.isin(a,list(all_brz)),[seed],blocked_bits)
 reachable_tokens={int(a.ravel()[v]) for v in parents};checks['actual_raster_land_reaches_every_new_portuguese_province']=changed_brz<=reachable_tokens
 witnesses={}
 for row in load('SITES.json'):
  if row['name'] not in ['Vila Bela','Cuiaba','Barcelos','Sao Gabriel','Marabitanas','Sao Joaquim','Tabatinga']:continue
  token=int(row['rgb'][1:],16);x,y=map(lambda v:int(round(v)),row['pixel']);candidate=y*a.shape[1]+x;end=candidate if candidate in parents and int(a.ravel()[candidate])==token else None
  if end is not None:witnesses[row['name']]=dict(rgb=row['rgb'],pixels=[[int(v%a.shape[1]),int(v//a.shape[1])] for v in path(parents,end)])
 checks['all_seven_named_post_witnesses_reach_belem']=len(witnesses)==7
 dump('PIXEL_PATH_WITNESSES.json',witnesses)
 dump('LAND_CONNECTIONS.json',dict(new_portuguese_provinces=len(changed_brz),reaching_belem=len(changed_brz&seen),maynas_mission_provinces=len(mission),missions_with_spanish_land_exit=len(mission&reached),excluded_impassable=len(imp),blocked_special_adjacencies=len(blocked),engine_market_or_military_access_tested=False))
 for lang,name in [('french','Peuples amazoniens'),('english','Amazonian peoples')]:
  rel=f'localization/{lang}/mod_v2content_l_{lang}.yml';oldloc=text(OUT/'before'/rel);newloc=text(ROOT/rel)
  checks['only_AP7_name_changed.'+lang]=newloc==re.sub(r'(?m)^(\s*AP7:\s*(?:\d+\s*)?)"Kayapo"',lambda m:m[1]+'"'+name+'"',oldloc) and (ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf')
 checks['R9_04_and_sacramento_and_CENTRAL_witnesses_preserved']=all(own[r]=={(s,t)} for r,s,t in [('x144683','STATE_ARAUCANIA','H91'),('xF2263F','STATE_LOS_RIOS','PAT'),('x4E1443','STATE_URUGUAY','BRZ'),('xB0243F','STATE_COSTA_RICA','G81'),('xBB820B','STATE_PANAMA','K81'),('x446C64','STATE_WEST_INDIES','C81')])
 external={r:dict(before=base.get(r),after=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change']=not external
 checks={k:bool(v) for k,v in checks.items()};dump('VALIDATION.json',dict(date='2026-10-28',checks=checks,passed=sum(checks.values()),total=len(checks),engine_tested=False,human_validated=False));print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
