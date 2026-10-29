"""Independent current-file checks for the bounded DP-01 installation."""
from dp01_install import *
import numpy as np
from PIL import Image
from hbc02_map_candidates import graph
from dp01_geography import draw
def outside(raw):
 return normalized([root for root in parse(raw)]) if not any(n.key.startswith('s:STATE_') for n in walk(parse(raw))) else [(r.key,normalized([n for n in r.children() if n.key not in ['s:'+s for s in SCOPE]])) for r in parse(raw)]
def units(raw,owners=False):
 out=C.Counter()
 for root in parse(raw):
  for country in root.children():
   if not country.key.startswith('c:'):continue
   for f in country.children('create_military_formation'):
    for u in f.children('combat_unit'):
     out[(country.key if owners else '',scalar(u.one('state_region')),scalar(u.one('type')),scalar(u.one('service_type','regular')))]+=int(u.one('count','1'))
 return out
def audit():
 m=load('PREPARED.json');ap=load('APPLIED.json');plan=load('PLAN.json');ow=normalized_owners();before={r:set(map(tuple,v)) for r,v in m['ownership_before'].items()};expected={z['rgb']:{(z['state'],z['after'])} for z in plan['transfers']}
 changed={r for r in set(before)|set(ow) if before.get(r)!=ow.get(r)}
 checks={'exact_planned_changes':changed==set(expected),'planned_owners_correct':all(ow.get(r)==vs for r,vs in expected.items()),'no_new_target_double_owner':all(len(ow.get(r,set()))==1 for r in expected)}
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};scope_rgb={r for s in SCOPE for r in provs(regs[s],'provinces')}
 counts=C.Counter()
 for p in effective('common/history/states'):
  for sid,s in state_nodes(text(p)).items():
   for cs in s.children('create_state'):
    for r in provs(cs,'owned_provinces'):counts['x'+r[1:].upper()]+=1
 checks['every_scope_rgb_one_assignment']=all(counts[r]==1 for r in scope_rgb)
 checks['target_rgb_in_region']=all(z['rgb'] in set(provs(regs[z['state']],'provinces')) for z in plan['transfers'])
 checks['targets_not_impassable']=all(z['rgb'] not in set(provs(regs[z['state']],'impassable')) for z in plan['transfers'])
 poprows=[]
 for rel in POPS:
  old=text(OUT/'preimages'/rel);new=text(ROOT/rel);checks['pop_cohorts_conserved_'+Path(rel).name]=popstock(old)==popstock(new);poprows.append(dict(file=rel,before=sum(popstock(old).values()),after=sum(popstock(new).values())))
 for rel in BUILD:
  if not (OUT/'preimages'/rel).exists():continue
  checks['building_levels_conserved_'+Path(rel).name]=buildingstock(text(ROOT/rel))==buildingstock(text(OUT/'preimages'/rel))
 for rel in [ST]+POPS+BUILD:
  if not (OUT/'preimages'/rel).exists():continue
  checks['outside_scopes_unchanged_'+rel]=outside(text(ROOT/rel))==outside(text(OUT/'preimages'/rel))
 oldunits=C.Counter();newunits=C.Counter();oldown=C.Counter();newown=C.Counter()
 for rel in MIL:
  oldunits+=units(text(OUT/'preimages'/rel));newunits+=units(text(ROOT/rel));oldown+=units(text(OUT/'preimages'/rel),True);newown+=units(text(ROOT/rel),True)
 rel='common/history/military_formations/1776_dp01.txt';newunits+=units(text(ROOT/rel));newown+=units(text(ROOT/rel),True)
 checks['military_counts_types_regions_conserved']=oldunits==newunits
 dump('MILITARY_LEDGER.json',dict(before=[dict(key=k,count=v) for k,v in sorted(oldown.items())],after=[dict(key=k,count=v) for k,v in sorted(newown.items())],note='Existing conscripts reassigned: DUR loses 16, PAN gains 8, KAL/PTA gain 4 each; no added standing units or people.'))
 checks['bitmap_unchanged']=sha(ROOT/'map_data/provinces.png')==m['world_before']['map_data/provinces.png']
 for z in ap['files']:
  checks['hash_'+z['file']]=sha(ROOT/z['file'])==z['after_sha256']
  if z['file'].endswith('.txt'):parse(text(ROOT/z['file']))
 # Compare country definitions/region IDs and resource capacity outside the six hub pointers.
 for rel in ['map_data/state_regions/09_central_asia.txt','map_data/state_regions/10_india.txt']:
  old={n.key:n for n in parse(text(OUT/'preimages'/rel))};new={n.key:n for n in parse(text(ROOT/rel))}
  checks['state_regions_same_keys_'+rel]=set(old)==set(new)
  for sid in old:
   checks['unchanged_region_except_hubs_'+sid]=normalized([n for n in old[sid].children() if n.key not in ['city','farm','wood','mine']])==normalized([n for n in new[sid].children() if n.key not in ['city','farm','wood','mine']])
 hub_expected={'STATE_BALUCHISTAN':{'city':'xBAE3D2','wood':'xF78D0D'},'STATE_PUNJAB':{'city':'xA6DAD0','mine':'x918140'},'STATE_HILL_PUNJAB':{'farm':'x280F05','wood':'x394B7F'}}
 for sid,changes in hub_expected.items():
  for k,r in changes.items():checks['hub_'+sid+'_'+k]=scalar(regs[sid].one(k))==r and r in set(provs(regs[sid],'provinces'))
 im=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),np.uint32);a=(im[:,:,0]<<16)|(im[:,:,1]<<8)|im[:,:,2]
 for tag in ['KAL','PTA']:
  rs={int(r[1:],16) for r,vs in ow.items() if any(t==tag for s,t in vs)};adj=graph(a,np.array(sorted(rs),np.uint32));seen={next(iter(rs))};q=list(seen)
  while q:
   for v,b in adj[q.pop()].items():
    if v in rs and b>=2 and v not in seen:seen.add(v);q.append(v)
  checks['land_connected_'+tag]=seen==rs
  cap='STATE_BALUCHISTAN' if tag=='KAL' else 'STATE_HILL_PUNJAB';checks['capital_owned_'+tag]=any((cap,tag) in vs for vs in ow.values())
 checks['Pishin_remains_DUR']=ow.get('x1910AD')=={('STATE_QUETTA','DUR')}
 checks['Gwadar_MAK_preserved']=ow.get('xB7B2BD')=={('STATE_BALUCHISTAN','MAK')}
 checks['Multan_PAN_preserved']=ow.get('x918140')=={('STATE_PUNJAB','PAN')}
 # Prior Arabia territorial core is not reinstalled or rolled back by the shared state patch.
 arabia=ROOT/'docs/reports/map/ARABIA_1776/ARABIA-01/PLAN.json'
 if arabia.exists():checks['Arabia_prior_transfers_preserved']=all(ow.get(z['rgb'])=={(z['state'],z['after'])} for z in json.loads(arabia.read_text(encoding='utf8'))['transfers'])
 profiles=audit_tech('TECH_AFTER.json');old={z['TAG']:z for z in load('TECH_BEFORE.json')};delta=[]
 for z in profiles:
  before_f={json.dumps(f,sort_keys=True) for f in old[z['TAG']]['findings'] if f['code']!='UNKNOWN_OR_INACTIVE_TAG'};delta.append(dict(tag=z['TAG'],status=z['status'],new_findings=[f for f in z['findings'] if json.dumps(f,sort_keys=True) not in before_f]))
 checks['restored_profiles_pass']=all(z['status']=='PASS_STATIC_ONLY' for z in profiles if z['TAG'] in ['KAL','PTA'])
 checks['no_new_DUR_PAN_tech_findings']=all(not z['new_findings'] for z in delta if z['tag'] in ['DUR','PAN'])
 # Native subject/action pair references and no regular payment, shared with no unrelated TAG.
 n=parse(text(ROOT/'common/subject_types/1776_dp01.txt'))[0];act=parse(text(ROOT/'common/diplomatic_actions/1776_dp01.txt'))[0];pact=act.children('pact')[0]
 checks['suzerainty_action_reference']=scalar(n.one('diplomatic_action'))==act.key and scalar(pact.one('subject_type'))==n.key
 checks['suzerainty_zero_regular_tribute']=float(pact.one('income_transfer'))==0
 checks['suzerainty_retains_diplomacy_and_subjects']=n.one('can_start_own_diplomatic_plays')=='yes' and n.one('can_have_subjects')=='yes'
 # Rulers: named 1776 incumbents; no reactivated vanilla 1836 templates.
 for tag,forbidden in [('KAL',['KAL_mehrab_ahmadzai','KAL_nasir_ahmadzai','KAL_muhammad_hussein_ahmadzai']),('PTA',['PTA_karam_singh_template','PTA_narendra_singh_template']),('PAN',['pan_ranjit_singh','pan_kharak_singh'])]:
  bodies=[text(p)[n.start:n.end] for p in effective('common/history/characters') for n in walk(parse(text(p))) if n.key=='c:'+tag]
  checks['no_1836_character_templates_'+tag]=all(not any(t in b for t in forbidden) for b in bodies)
 for lang in ['french','english']:
  p=ROOT/'localization'/lang/'replace'/('1776_dp01_l_'+lang+'.yml');keys=re.findall(r'^\s*([A-Za-z0-9_]+):0\s+"',text(p),re.M);counts=C.Counter()
  for f in (ROOT/'localization'/lang).rglob('*.yml'):
   counts.update(k for k in re.findall(r'^\s*([A-Za-z0-9_]+):(?:\d+)?\s+"',text(f),re.M) if k in keys)
  checks['loc_BOM_'+lang]=p.read_bytes().startswith(b'\xef\xbb\xbf');checks['loc_unique_'+lang]=all(counts[k]==1 for k in keys)
 draw(a,{r.upper():vs for r,vs in ow.items()},load('SITE_PROXIES.json'),load('VIEW_BOX.json'),'INSTALLED_MAP.png')
 dump('VALIDATION.json',dict(checks=checks,status='PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL_STATIC',runtime_validation=False,transfers=len(changed),scope_rgb=len(scope_rgb),populations=poprows,technology_delta=delta))
 print(json.dumps(dict(checks=len(checks),failed=[k for k,v in checks.items() if not v],tech_delta=delta,POPs=poprows),ensure_ascii=False))
 return all(checks.values())
if __name__=='__main__':sys.exit(0 if audit() else 1)
