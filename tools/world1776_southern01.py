"""Southern Africa bounded installation from immediate preimages; never restores a baseline."""
import argparse,json,shutil
from collections import defaultdict,deque,Counter
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_southern01_plan as p
import world1776_sahel0607 as prior
import validate_starting_technology_1776 as contract
ROOT,LOT,ST,PREFIX=p.ROOT,p.LOT,p.ST,p.PREFIX
raw,save=prior.raw,prior.save
b=prior.m.s.b
ARMY=prior.m.ARMY
RELATIONS='common/history/diplomacy/00_relations.txt'
def dump(n,v):p.h.dump(n,v)
def load(n):return json.loads((LOT/n).read_text('utf8'))
def histories():return load('HISTORY_INPUTS.json')
def prepare():
 if (LOT/'PREPARED.json').exists():return
 dump('PLAN.json',p.make_plan());dump('COUNTRY_PROFILES.json',p.COUNTRIES)
 cat=b.a.catalog('common/country_definitions');assert all(t not in cat for t,r in p.COUNTRIES.items() if r['new'])
 dump('DEFINITION_INPUTS.json',{t:raw(path)[n.start:n.end] for t,(n,path) in cat.items() if t in p.COUNTRIES and not p.COUNTRIES[t]['new']})
 hist={};native={};bodies={}
 for path in b.tech.effective('common/history/countries'):
  text=raw(path)
  for n in b.walk(b.parse(text)):
   t=n.key[2:] if n.key.startswith('c:') else ''
   if t not in p.COUNTRIES:continue
   assert t not in bodies
   bodies[t]=text[n.start:n.end]
   if path.is_relative_to(ROOT):hist[t]=[path.relative_to(ROOT).as_posix(),n.key]
   else:native[t]=dict(file='common/history/countries/'+path.name,text=text)
 dump('HISTORY_INPUTS.json',hist);dump('NATIVE_HISTORY_INPUTS.json',native);dump('COUNTRY_HISTORY_INPUTS.json',bodies)
 chars=[]
 for path in b.tech.effective('common/history/characters'):
  text=raw(path);keys=[n.key for n in b.walk(b.parse(text)) if n.key in ['c:BST','c:MTB','c:MSH']]
  if keys:chars.append(dict(file='common/history/characters/'+path.name,text=text,keys=keys,native=not path.is_relative_to(ROOT)))
 dump('CHARACTER_INPUTS.json',chars)
 snap=contract.collect_snapshot();before=[contract.audit_country(t,snap) for t in p.WITNESSES];dump('STARTING_TECH_BEFORE.json',before)
 dump('PREPARED.json',dict(historical_date='1776-01-01',no_installation_yet=True))
def country_body(t):
 r=p.COUNTRIES[t]
 if r.get('preserve_knowledge'):
  old=next(v for v in load('STARTING_TECH_BEFORE.json') if v['TAG']==t)
  tech=sorted(set(old['technologies'])|set(r.get('targeted_grants',[])))
 else:tech=r['tech']
 effect='effect_aor1776_southern01_'+('decentralised' if r['kind']=='decentralized' else 'politics')
 oldbody=load('COUNTRY_HISTORY_INPUTS.json').get(t,'')
 cons=[n.key for n in b.walk(b.parse(oldbody)) if n.key.startswith('effect_native_conscription_')]
 if r['new'] and r['kind']=='decentralized':cons=['effect_native_conscription_3']
 return 'c:'+t+' ?= {\n'+''.join(' add_technology_researched = '+x+'\n' for x in tech)+' '+effect+' = yes\n'+''.join(' '+x+' = yes\n' for x in cons)+'}\n'
def additional():
 out={};defs=[];cache=load('DEFINITION_INPUTS.json')
 for t,r in p.COUNTRIES.items():
  if r['new']:
   text=t+' = { color = { '+' '.join(map(str,r['color']))+' } country_type = '+r['kind']+' tier = principality religion = animist cultures = { '+' '.join(r['culture'])+' } capital = '+r['capital']+' }'
  else:
   text=cache[t];n=b.parse(text)[0];ops=[]
   for field,value in [('country_type',r['kind']),('capital',r['capital']),('tier','kingdom' if r['kind']=='unrecognized' else 'principality'),('cultures','{ '+' '.join(r['culture'])+' }')]:
    f=n.children(field);assert len(f)==1;ops.append((f[0].start,f[0].end,field+' = '+value))
   text=b.edits(text,ops)
  defs.append(text)
 out['common/country_definitions/'+PREFIX+'.txt']='\n\n'.join(defs)+'\n'
 native=load('NATIVE_HISTORY_INPUTS.json')
 for t in p.COUNTRIES:
  if t in histories():continue
  if t in native:
   rec=native[t];n=b.one(rec['text'],'c:'+t);out[rec['file']]=b.edits(rec['text'],[(n.start,n.end,country_body(t).rstrip('\n'))])
  else:out['common/history/countries/'+t.lower()+' - 1776 southern.txt']='COUNTRIES = { '+country_body(t)+'}\n'
 effect=raw(ROOT/'common/scripted_effects/1776_world_madagascar02.txt').replace('madagascar02','southern01')
 out['common/scripted_effects/'+PREFIX+'.txt']=effect
 law,path=b.a.catalog('common/laws')['law_mercantilism'];f=law.children('modifier')[0];allowed=' '.join('c:'+t+' ?= this' for t,r in p.COUNTRIES.items() if r['kind']=='unrecognized')
 out['common/laws/'+PREFIX+'.txt']='law_aor1776_southern01_trade_customs = { group = lawgroup_trade_policy parent = law_mercantilism icon = "gfx/interface/icons/law_icons/mercantilism.dds" progressiveness = 0 unlocking_technologies = { international_relations } is_visible = { OR = { '+allowed+' } } can_enact = { OR = { '+allowed+' } } '+raw(path)[f.start:f.end]+' }\n'
 out['common/history/diplomacy/'+PREFIX+'.txt']='DIPLOMACY = { c:MSH ?= { if = { limit = { exists = c:MNC } create_diplomatic_pact = { country = c:MNC type = tributary } } } }\n'
 for row in load('CHARACTER_INPUTS.json'):
  if row['native']:
   out[row['file']]=b.edits(row['text'],[(b.one(row['text'],key).start,b.one(row['text'],key).end,key+' ?= { }') for key in row['keys']])
 for lang in ['french','english']:
  strings={}
  for t,r in p.COUNTRIES.items():strings[t]=r['fr' if lang=='french' else 'en'];strings[t+'_ADJ']=r['adj_fr' if lang=='french' else 'adj_en']
  strings.update(law_aor1776_southern01_trade_customs='Coutumes commerciales' if lang=='french' else 'Trade Customs',law_aor1776_southern01_trade_customs_desc='Les autorités locales prélèvent les droits des marchés et des caravanes.' if lang=='french' else 'Local authorities collect dues on markets and caravans.')
  out[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
 return out
def scopes():
 plan=load('PLAN.json');states={'s:'+r['state'] for r in plan};result={ST:states,RELATIONS:{'c:GBR'}}
 for folder in ['common/history/pops','common/history/buildings']:
  for path in b.tech.effective(folder):
   selected={n.key for n in b.walk(b.parse(raw(path))) if n.key in states}
   if selected:assert path.is_relative_to(ROOT);result[path.relative_to(ROOT).as_posix()]=selected
 for rel,key in histories().values():result.setdefault(rel,set()).add(key)
 for row in load('CHARACTER_INPUTS.json'):
  if not row['native']:result.setdefault(row['file'],set()).update(row['keys'])
 # Only extant nodes from superseded nineteenth-century territorial governments.
 for path in b.tech.effective('common/history/military_formations'):
  keys={n.key for n in b.walk(b.parse(raw(path))) if n.key in ['c:'+t for t in p.DEACTIVATED]}
  if keys:assert path.is_relative_to(ROOT);result[path.relative_to(ROOT).as_posix()]=keys
 return result
def transform(old):
 plan=load('PLAN.json');alloc=prior.m.allocations(old[ST],plan);out={ST:prior.m.transform({ST:old[ST]},plan)[ST]}
 for rel,text in old.items():
  if rel==ST:continue
  ops=[]
  if '/history/pops/' in rel or '/history/buildings/' in rel:out[rel]=prior.m.transform_portions(text,alloc,'/history/buildings/' in rel);continue
  if rel==RELATIONS:
   n=b.one(text,'c:GBR')
   for f in n.children('set_relations'):
    if f.one('country')=='c:ORA':ops.append((f.start,f.end,'# SOUTHERN-01: no Orange republic in1776.'))
   assert len(ops)==1
  elif '/history/countries/' in rel:
   for t,(path,key) in histories().items():
    if path==rel:n=b.one(text,key);ops.append((n.start,n.end,country_body(t).rstrip('\n')))
  elif '/history/characters/' in rel:
   rec=next(r for r in load('CHARACTER_INPUTS.json') if r['file']==rel)
   for key in rec['keys']:n=b.one(text,key);ops.append((n.start,n.end,key+' ?= { }'))
  elif '/history/military_formations/' in rel:
   for t in p.DEACTIVATED:
    nn=[n for n in b.walk(b.parse(text)) if n.key=='c:'+t]
    for n in nn:ops.append((n.start,n.end,n.key+' ?= { }'))
  else:raise AssertionError(rel)
  out[rel]=b.edits(text,ops)
 return out
def geometry(text,render=True):
 own=prior.m.state_owners(text);im=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'))[2430:3000,4370:4950];pack=im[:,:,0].astype('uint32')*65536+im[:,:,1].astype('uint32')*256+im[:,:,2]
 table={int(c[1:],16):v[-1][1] for c,v in own.items()};ids={t:i+1 for i,t in enumerate(sorted(set(table.values())))};inverse={v:k for k,v in ids.items()};code=np.zeros(pack.shape,'int32')
 for c in np.unique(pack):code[pack==c]=ids.get(table.get(int(c)),0)
 adj=defaultdict(set)
 for left,right in [(code[:,:-1],code[:,1:]),(code[:-1],code[1:])]:
  for a,z in np.unique(np.stack([left.ravel(),right.ravel()],axis=1),axis=0):
   if a and z and a!=z:adj[inverse[a]].add(inverse[z]);adj[inverse[z]].add(inverse[a])
 result=[]
 for t in list(p.COUNTRIES)+['SAN','TSW','TMP','MNC','MTP']:
  yy,xx=np.where(code==ids.get(t,-1));points=set(zip(xx.tolist(),yy.tolist()));sizes=[]
  while points:
   start=points.pop();q=deque([start]);size=0
   while q:
    x,y=q.popleft();size+=1
    for xy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if xy in points:points.remove(xy);q.append(xy)
   sizes.append(size)
  result.append(dict(TAG=t,components=sorted(sizes,reverse=True),neighbors=sorted(adj[t])))
 dump('GEOMETRY_CHECK.json',result)
 if render:
  colors={}
  for t,(n,path) in b.a.catalog('common/country_definitions').items():
   try:colors[t]=tuple(map(int,prior.m.s.ids(n,'color')))
   except ValueError:pass
  for t,r in p.COUNTRIES.items():colors[t]=tuple(r['color'])
  rgb=np.zeros((*code.shape,3),'uint8')+210
  for t,i in ids.items():rgb[code==i]=colors.get(t,(120,120,120))
  edge=np.zeros(code.shape,bool);edge[1:]|=code[1:]!=code[:-1];edge[:,1:]|=code[:,1:]!=code[:,:-1];rgb[edge]=(30,30,30)
  out=Image.fromarray(rgb).resize((1740,1710),Image.Resampling.NEAREST);d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
  for t in list(p.COUNTRIES)+['SAN','TSW','DEI','NAM','PDI','VND','XHO','TMP','MNC','MTP']:
   yy,xx=np.where(code==ids.get(t,-1))
   if len(xx):j=np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2);d.text((int(xx[j])*3,int(yy[j])*3),t,font=font,fill='white',stroke_width=2,stroke_fill='black')
  out.save(LOT/'PROPOSED.png')
 return result
def preflight():
 prepare();old={r:raw(ROOT/r) for r in scopes()};out=transform(old)
 for r,t in out.items():save(LOT/'staged'/r,t,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
 for r,t in additional().items():save(LOT/'staged'/r,t,r.endswith('.yml'))
 dump('SCOPES.json',{r:sorted(v) for r,v in scopes().items()});print('GEOMETRY',geometry(out[ST]))
def apply():
 prepare();assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed'
 scope=scopes();new=additional();assert all(not (ROOT/r).exists() for r in new),'New-file collision'
 own=prior.m.state_owners(raw(ROOT/ST))
 for r in load('PLAN.json'):
  for c in r['RGBs']:assert own[c]==[[r['state'],r['source']]],(c,own[c])
 old={r:raw(ROOT/r) for r in scope};hashes={r:b.a.sha(ROOT/r) for r in scope};out=transform(old)
 prior.m.s.g.LOT=LOT;before=dict(inventory=prior.m.s.b4.inventory(),protected=prior.m.s.g.protection(),scope={r:sorted(v) for r,v in scope.items()},new_files=list(new))
 dump('APPLY_BEFORE.json',before)
 for r in scope:dest=LOT/'apply_inputs'/r;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,dest)
 assert all(b.a.sha(ROOT/r)==v for r,v in hashes.items()),'Concurrent mutation'
 for r,t in out.items():
  assert b.a.sha(ROOT/r)==hashes[r];save(ROOT/r,t,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
 for r,t in new.items():assert not (ROOT/r).exists();save(ROOT/r,t,r.endswith('.yml'))
 dump('FILES_MODIFIED.json',[dict(file=r,before=hashes.get(r),after=b.a.sha(ROOT/r)) for r in list(scope)+list(new)])
 print('Installed',len(scope),'existing +',len(new),'new;',sum(len(r['RGBs']) for r in load('PLAN.json')),'cells')
def audit_tech():
 snap=contract.collect_snapshot();new=[contract.audit_country(t,snap,dict(required=r['tech'],allowed=r['tech'],historical_evidence=r['basis'])) for t,r in p.COUNTRIES.items() if r['new']];old={r['TAG']:r for r in load('STARTING_TECH_BEFORE.json')};after=[contract.audit_country(t,snap) for t in old];comparison=[]
 for r in after:
  a={json.dumps(f,sort_keys=True) for f in old[r['TAG']]['findings'] if f['priority'] in ['P0','P1']};z={json.dumps(f,sort_keys=True) for f in r['findings'] if f['priority'] in ['P0','P1']}
  comparison.append(dict(TAG=r['TAG'],introduced=[json.loads(x) for x in sorted(z-a)],inherited_remaining=[json.loads(x) for x in sorted(a&z)],resolved=[json.loads(x) for x in sorted(a-z)],knowledge_removed=sorted(set(old[r['TAG']]['technologies'])-set(r['technologies'])),knowledge_added=sorted(set(r['technologies'])-set(old[r['TAG']]['technologies']))))
 dump('STARTING_TECH_NEW_COUNTRIES.json',new);dump('STARTING_TECH_EXISTING_AFTER.json',after);dump('TECH_NON_REGRESSION.json',dict(new_profiles=len(new),all_new_profiles_pass=all(r['status']=='PASS_STATIC_ONLY' for r in new),existing_country_comparison=comparison,shared_graph_changes=0,shared_recipe_changes=0,human_validated=False))
 print('New profiles',[(r['TAG'],r['status'],r['findings']) for r in new]);print('Introduced',[(r['TAG'],r['introduced']) for r in comparison if r['introduced']])
def validate():
 before=load('APPLY_BEFORE.json');checks=[]
 def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
 old={r:raw(LOT/'apply_inputs'/r) for r in before['scope']};expected=transform(old)
 for rel,t in expected.items():
  current=raw(ROOT/rel);ck('exact_patch.'+rel,current==t)
  def outside(text):return b.edits(text,[(n.start,n.end,'<OWNED_NODE>') for n in [b.one(text,k) for k in before['scope'][rel]]])
  ck('outside_owned_nodes_preserved.'+rel,outside(current)==outside(old[rel]))
  if '/history/pops/' in rel:ck('all_population_cohorts_conserved.'+rel,prior.m.pop_cohorts(current)==prior.m.pop_cohorts(old[rel]))
  if '/history/buildings/' in rel:ck('all_levels_PM_conserved.'+rel,prior.m.building_inventory(current)==prior.m.building_inventory(old[rel]))
 now=prior.m.s.b4.inventory();owners=dict(before['inventory']['owners'])
 for r in load('PLAN.json'):
  for c in r['RGBs']:ck('expected_original_owner.'+c,owners.get(c)==[[r['state'],r['source']]]);owners[c]=[[r['state'],r['target']]]
 ck('exact_global_owner_delta',owners==now['owners']);ck('world_population_conserved',now['world_population']==before['inventory']['world_population']);ck('Git_identity_index_unchanged',now['git']==before['inventory']['git'])
 ck('no_new_duplicate',{c for c,v in now['owners'].items() if len(v)>1}<={c for c,v in before['inventory']['owners'].items() if len(v)>1})
 for t in p.DEACTIVATED:ck('anachronistic_state_absent.'+t,not any(v[-1][1]==t for v in now['owners'].values()))
 cat=b.a.catalog('common/country_definitions');central={t for t,(n,path) in cat.items() if n.one('country_type')!='decentralized'}
 for t,r in p.COUNTRIES.items():
  n,path=cat[t];ck('effective_own_definition.'+t,path==ROOT/'common/country_definitions'/f'{PREFIX}.txt');ck('capital_owned.'+t,any([r['capital'],t] in v for v in now['owners'].values()));ck('political_type.'+t,n.one('country_type')==r['kind'])
 for r in geometry(raw(ROOT/ST)):
  if r['TAG'] not in p.COUNTRIES or p.COUNTRIES[r['TAG']]['kind']=='decentralized':continue
  ck('no_central_enclave_in_decentralised_land.'+r['TAG'],bool(set(r['neighbors'])&central),r['neighbors']);ck('central_contiguous.'+r['TAG'],len([v for v in r['components'] if v>=max(r['components'],default=1)*.05])==1,r['components'])
 for r,t in additional().items():ck('generated_file_exact.'+r,raw(ROOT/r)==t)
 edited={r['file'] for r in load('FILES_MODIFIED.json')}
 repairs={}
 for name in ['COMPATIBILITY_REPAIR.json','COMPATIBILITY_REPAIR_R2.json']:
  if (LOT/name).exists():repairs.update({r['file']:r for r in load(name)['files']})
 if repairs:
  for rec in repairs.values():
   edited.add(rec['file']);ck('reviewed_repair_hash.'+rec['file'],b.a.sha(ROOT/rec['file'])==rec['after'])
   if rec.get('extra_scoped_key'):
    a=raw(LOT/'repair_inputs'/rec['file']);z=raw(ROOT/rec['file']);key=rec['extra_scoped_key'];an=b.one(a,key);zn=b.one(z,key)
    ck('repair_outside_owned_node.'+rec['file'],b.edits(a,[(an.start,an.end,'<OWNED_NODE>')])==b.edits(z,[(zn.start,zn.end,'<OWNED_NODE>')]))
 outside=[dict(file=r,before=v,after=b.a.sha(ROOT/r) if (ROOT/r).exists() else None) for r,v in before['protected'].items() if r not in edited and (not (ROOT/r).exists() or b.a.sha(ROOT/r)!=v)]
 ck('other_protected_files_preserved',not outside,outside);dump('CONCURRENT_CHANGES.json',dict(outside_scope_changes=outside,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False))
 result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False);dump('VALIDATION.json',result);print('Static',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']]);return result['status']=='PASS'
if __name__=='__main__':
 parser=argparse.ArgumentParser()
 for k in ['preflight','apply','tech','validate']:parser.add_argument('--'+k,action='store_true')
 a=parser.parse_args()
 if a.preflight:preflight()
 if a.apply:apply()
 if a.tech:audit_tech()
 if a.validate:raise SystemExit(0 if validate() else 1)
