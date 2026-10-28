"""Bounded Malagasy restoration; --apply once only."""
import argparse,json,shutil
from collections import defaultdict,deque,Counter
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_madagascar02_plan as p
import world1776_sahel0607 as prior
import validate_starting_technology_1776 as contract
ROOT,LOT,ST,PREFIX=p.ROOT,p.LOT,p.ST,p.PREFIX
raw=prior.raw;save=prior.save
b=prior.m.s.b
ARMY=prior.m.ARMY

def dump(name,data):p.h.dump(name,data)

def load(name):return json.loads((LOT/name).read_text('utf8'))

def histories():
    if (LOT/'HISTORY_INPUTS.json').exists():return {t:tuple(v) for t,v in load('HISTORY_INPUTS.json').items()}
    result={}
    for path in b.tech.effective('common/history/countries'):
        text=raw(path)
        for n in b.walk(b.parse(text)):
            if n.key in ['c:'+t for t in p.COUNTRIES]:
                if not path.is_relative_to(ROOT):continue
                assert n.key[2:] not in result,'Multiple active histories.'
                result[n.key[2:]]=(path.relative_to(ROOT).as_posix(),n.key)
    return result

def raw_country_node(text,tag):
 n=b.one(text,'c:'+tag);return text[n.start:n.end]

def country_body(tag):
 r=p.COUNTRIES[tag]
 if r.get('preserve_knowledge'):
  cached=load('COUNTRY_HISTORY_INPUTS.json');native=load('NATIVE_HISTORY_INPUTS.json')
  text=cached[tag] if tag in cached else raw_country_node(native[tag]['text'],tag)
  assert text.count('effect_starting_politics_traditional = yes')==1,(tag,'review native political call')
  text=text.replace('effect_starting_politics_traditional = yes','effect_aor1776_madagascar02_politics = yes').replace('activate_law = law_type:law_mercantilism','activate_law = law_type:law_aor1776_madagascar02_trade_customs')
  if r.get('targeted_grants'):
   call='effect_aor1776_madagascar02_politics = yes'
   text=text.replace(call,''.join('add_technology_researched = '+t+'\n\t\t' for t in r['targeted_grants'])+call,1)
  return text
 effect='effect_aor1776_madagascar02_'+('decentralised' if r['kind']=='decentralized' else 'politics')
 return 'c:'+tag+' ?= {\n'+''.join(' add_technology_researched = '+t+'\n' for t in r['tech'])+' '+effect+' = yes\n'+(' effect_native_conscription_3 = yes\n' if r['kind']=='decentralized' else ' activate_law = law_type:law_slave_trade\n')+'}\n'

def preflight():
    prepare()
    if not (LOT/'HISTORY_INPUTS.json').exists():dump('HISTORY_INPUTS.json',histories())
    scope=scopes();old={r:raw(ROOT/r) for r in scope};updated=transform(old)
    for rel,text in updated.items():save(LOT/'staged'/rel,text,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    for rel,text in additional().items():save(LOT/'staged'/rel,text,rel.endswith('.yml'))
    dump('SCOPES.json',{r:sorted(v) for r,v in scope.items()});geometry(updated[ST])

def apply():
    prepare()
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed.'
    if not (LOT/'HISTORY_INPUTS.json').exists():dump('HISTORY_INPUTS.json',histories())
    scope=scopes();new=additional();assert all(not (ROOT/r).exists() for r in new),'Review new-file collision.'
    current=raw(ROOT/ST);owners=prior.m.state_owners(current)
    for r in load('PLAN.json'):
        for color in r['RGBs']:assert owners.get(color) and all(v==[r['state'],r['source']] for v in owners[color]),(color,owners.get(color))
    old={r:raw(ROOT/r) for r in scope};updated=transform(old);hashes={r:b.a.sha(ROOT/r) for r in scope}
    prior.m.s.g.LOT=LOT
    before=dict(inventory=prior.m.s.b4.inventory(),protected=prior.m.s.g.protection(),scope={r:sorted(v) for r,v in scope.items()},new_files=list(new),historical_date='1776-01-01')
    for r in scope:
        dest=LOT/'apply_inputs'/r;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,dest)
    dump('APPLY_BEFORE.json',before)
    assert all(b.a.sha(ROOT/r)==v for r,v in hashes.items()),'Concurrent edit; reread current version.'
    for r,text in updated.items():
        assert b.a.sha(ROOT/r)==hashes[r],r
        save(ROOT/r,text,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
    for r,text in new.items():
        assert not (ROOT/r).exists(),r
        save(ROOT/r,text,r.endswith('.yml'))
    dump('FILES_MODIFIED.json',[dict(file=r,before=hashes.get(r),after=b.a.sha(ROOT/r)) for r in list(scope)+list(new)])
    print('Installed:',len(scope),'existing files,',len(new),'new files,',sum(len(r['RGBs']) for r in load('PLAN.json')),'native cells.')

def audit_tech():
    snap=contract.collect_snapshot()
    new=[contract.audit_country(t,snap,dict(required=r['tech'],allowed=r['tech'],historical_evidence=r['basis'])) for t,r in p.COUNTRIES.items() if not r.get('preserve_knowledge')]
    existing=[contract.audit_country(r['TAG'],snap) for r in load('STARTING_TECH_BEFORE.json')]
    dump('STARTING_TECH_NEW_COUNTRIES.json',new);dump('STARTING_TECH_EXISTING_AFTER.json',existing)
    old={r['TAG']:r for r in load('STARTING_TECH_BEFORE.json')};comparison=[]
    for r in existing:
        a={json.dumps(f,sort_keys=True) for f in old[r['TAG']]['findings'] if f['priority'] in ['P0','P1']};z={json.dumps(f,sort_keys=True) for f in r['findings'] if f['priority'] in ['P0','P1']}
        comparison.append(dict(TAG=r['TAG'],inherited_remaining=[json.loads(f) for f in sorted(a&z)],introduced=[json.loads(f) for f in sorted(z-a)],resolved=[json.loads(f) for f in sorted(a-z)]))
    dump('TECH_NON_REGRESSION.json',dict(new_profiles=len(new),all_new_profiles_pass=all(r['status']=='PASS_STATIC_ONLY' for r in new),existing_country_comparison=comparison,shared_graph_changes=0,shared_recipe_changes=0,human_validated=False))
    print('Profiles:',[(r['TAG'],r['status'],r['findings']) for r in new]);print('New existing P0/P1:',[(r['TAG'],r['introduced']) for r in comparison if r['introduced']])

def base_additional():
 result={};cat=b.a.catalog('common/country_definitions');definitions=[]
 for t,r in p.COUNTRIES.items():
  if r.get('new'):
   if not (LOT/'FILES_MODIFIED.json').exists():assert t not in cat,'New TAG collision: '+t
   definitions.append(t+' = { color = { '+' '.join(map(str,r['color']))+' } country_type = '+r['kind']+' tier = '+('kingdom' if r['kind']=='unrecognized' else 'principality')+' religion = '+r['religion']+' cultures = { '+' '.join(r['culture'])+' } capital = '+r['capital']+' }')
  else:
   # Cache the original definition so later validation never re-sources our overlay.
   cache=load('DEFINITION_INPUTS.json');text=cache[t];n=b.parse(text)[0];ops=[]
   for field,value in [('country_type',r.get('kind',n.one('country_type'))),('capital',r['capital']),('tier',n.one('tier'))]:
    nn=n.children(field)
    if nn:ops.append((nn[0].start,nn[0].end,field+' = '+value))
   definitions.append(b.edits(text,ops))
 result['common/country_definitions/'+PREFIX+'.txt']='\n\n'.join(definitions)+'\n'
 present=histories()
 native=load('NATIVE_HISTORY_INPUTS.json')
 for t in p.COUNTRIES:
  if t in present:continue
  if t in native:
   row=native[t];text=row['text'];node=b.one(text,'c:'+t)
   result[row['file']]=b.edits(text,[(node.start,node.end,country_body(t).rstrip('\n'))])
  else:result['common/history/countries/'+t.lower()+' - 1776 interior.txt']='COUNTRIES = { '+country_body(t)+'}\n'
 result['common/scripted_effects/'+PREFIX+'.txt']=prior.additional()['common/scripted_effects/1776_world_sahel0607.txt'].replace('sahel0607','madagascar02')
 law,path=b.a.catalog('common/laws')['law_mercantilism'];mod=law.children('modifier')[0]
 allowed=' '.join('c:'+t+' ?= this' for t,r in p.COUNTRIES.items() if r['kind']!='decentralized')
 result['common/laws/'+PREFIX+'.txt']='law_aor1776_madagascar02_trade_customs = { group = lawgroup_trade_policy parent = law_mercantilism icon = "gfx/interface/icons/law_icons/mercantilism.dds" progressiveness = 0 unlocking_technologies = { international_relations } is_visible = { OR = { '+allowed+' } } can_enact = { OR = { '+allowed+' } } '+raw(path)[mod.start:mod.end]+' }\n'
 result['common/history/diplomacy/'+PREFIX+'.txt']='DIPLOMACY = { c:LND ?= { create_diplomatic_pact = { country = c:KZM type = tributary } } c:LBA ?= { create_diplomatic_pact = { country = c:KNY type = tributary } } }\n'
 for rel in load('CHARACTER_OVERLAYS.json'):
  result[rel]='# CONGO-01: suppress native1836 characters; cartographic pass adds no ruler.\nCHARACTERS = {}\n'
 for lang in ['french','english']:
  strings={}
  for t,r in p.COUNTRIES.items():
   if r.get('new'):strings[t]=r['fr' if lang=='french' else 'en'];strings[t+'_ADJ']=r['adj_fr' if lang=='french' else 'adj_en']
  pass
  strings.update(law_aor1776_madagascar02_trade_customs='Coutumes commerciales' if lang=='french' else 'Trade Customs',law_aor1776_madagascar02_trade_customs_desc='Les autorités locales prélèvent les droits des marchés et des caravanes.' if lang=='french' else 'Local authorities collect dues on markets and caravans.')
  result[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
 return result

def geometry(text,render=True):
    own=prior.m.state_owners(text);image=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'))[2250:2730,5010:5310]
    packed=image[:,:,0].astype('uint32')*65536+image[:,:,1].astype('uint32')*256+image[:,:,2]
    tags=sorted({v[-1][1] for v in own.values()});ids={t:i+1 for i,t in enumerate(tags)};inverse={v:k for k,v in ids.items()}
    code=np.zeros(packed.shape,'int32');table={int(c[1:],16):v[-1][1] for c,v in own.items()}
    for c in np.unique(packed):
        if int(c) in table:code[packed==c]=ids[table[int(c)]]
    adj=defaultdict(set)
    for a,z in [(code[:,:-1],code[:,1:]),(code[:-1],code[1:])]:
        for x,y in np.unique(np.stack([a.ravel(),z.ravel()],axis=1),axis=0):
            if x and y and x!=y:adj[inverse[x]].add(inverse[y]);adj[inverse[y]].add(inverse[x])
    result=[]
    for tag in p.COUNTRIES:
        yy,xx=np.where(code==ids.get(tag,-1));points=set(zip(xx.tolist(),yy.tolist()));components=[]
        while points:
            start=points.pop();q=deque([start]);size=0
            while q:
                x,y=q.popleft();size+=1
                for xy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if xy in points:points.remove(xy);q.append(xy)
            components.append(size)
        result.append(dict(TAG=tag,components=sorted(components,reverse=True),neighbors=sorted(adj[tag]),kind=p.COUNTRIES[tag]['kind'] if tag in p.COUNTRIES else b.a.catalog('common/country_definitions')[tag][0].one('country_type')))
    dump('GEOMETRY_CHECK.json',result)
    if render:
        cat=b.a.catalog('common/country_definitions');colors={}
        for t,(n,path) in cat.items():
            try:colors[t]=tuple(map(int,prior.m.s.ids(n,'color')))
            except ValueError:continue
        for t,r in p.COUNTRIES.items():
            if r.get('new'):colors[t]=tuple(r['color'])
        rgb=np.zeros((*code.shape,3),'uint8')+200
        for t,i in ids.items():rgb[code==i]=colors.get(t,(100,100,100))
        edge=np.zeros(code.shape,bool);edge[1:]|=code[1:]!=code[:-1];edge[:,1:]|=code[:,1:]!=code[:,:-1];rgb[edge]=(35,35,35)
        out=Image.fromarray(rgb).resize((1200,1920),Image.Resampling.NEAREST);d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
        for t in p.COUNTRIES:
            yy,xx=np.where(code==ids.get(t,-1))
            if not xx.size:continue
            j=np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2)
            d.text((int(xx[j])*4,int(yy[j])*4),t,font=font,fill='white',stroke_width=2,stroke_fill='black')
        out.save(LOT/'PROPOSED.png')
    print('Disconnected:',[(r['TAG'],r['components']) for r in result if len(r['components'])!=1]);print('Central isolated:',[(r['TAG'],r['neighbors']) for r in result if r['kind']!='decentralized' and not any(n not in {t for t,r in p.COUNTRIES.items() if r['kind']=='decentralized'} and n!='SD1' for n in r['neighbors'])])
    return result

def validate():
    before=load('APPLY_BEFORE.json');checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    old={r:raw(LOT/'apply_inputs'/r) for r in before['scope']};expected=transform(old)
    for rel,text in expected.items():
        current=raw(ROOT/rel);ck('exact_current_scoped_patch.'+rel,current==text)
        def outside(t):
            nodes=[b.one(t,k) for k in before['scope'][rel]]
            return b.edits(t,[(n.start,n.end,'<OWNED_NODE>') for n in nodes])
        ck('outside_owned_nodes_preserved.'+rel,outside(current)==outside(old[rel]))
        if '/history/pops/' in rel:ck('all_cohorts_conserved.'+rel,prior.m.pop_cohorts(current)==prior.m.pop_cohorts(old[rel]))
        if '/history/buildings/' in rel:ck('all_levels_and_PM_conserved.'+rel,prior.m.building_inventory(current)==prior.m.building_inventory(old[rel]))
    now=prior.m.s.b4.inventory();owners=dict(before['inventory']['owners'])
    for row in load('PLAN.json'):
        for color in row['RGBs']:
            ck('expected_original_owner.'+color,all(v==[row['state'],row['source']] for v in owners.get(color,[])) and bool(owners.get(color)))
            owners[color]=[[row['state'],row['target']]]
    ck('exact_global_owner_delta',owners==now['owners'])
    ck('no_new_duplicate',{c for c,v in now['owners'].items() if len(v)>1}<={c for c,v in before['inventory']['owners'].items() if len(v)>1})
    ck('world_population_conserved',now['world_population']==before['inventory']['world_population'])
    ck('Git_identity_index_unchanged',now['git']==before['inventory']['git'])
    cat=b.a.catalog('common/country_definitions');cultures=b.a.catalog('common/cultures')
    for t,r in p.COUNTRIES.items():
        n,path=cat[t];ck('own_effective_definition.'+t,path==ROOT/'common/country_definitions'/f'{PREFIX}.txt')
        ck('capital_region_owned.'+t,any([n.one('capital'),t] in v for v in now['owners'].values()))
        ck('political_type.'+t,n.one('country_type')==r['kind']);ck('known_cultures.'+t,set(prior.m.s.ids(n,'cultures'))<=set(cultures))
    for r,text in additional().items():
        ck('generated_file_exact.'+r,raw(ROOT/r)==text)
        if r.endswith('.yml'):ck('localization_BOM.'+r,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
    geometry_rows=geometry(raw(ROOT/ST));central={t for t,(n,path) in cat.items() if n.one('country_type')!='decentralized'}
    for r in geometry_rows:
        if r['kind']=='decentralized':continue
        ck('central_country_contiguous.'+r['TAG'],len([v for v in r['components'] if v>=max(r['components'],default=1)*.05])==1,r['components'])
        ck('no_new_central_enclave_in_decentralised_land.'+r['TAG'],bool(set(r['neighbors'])&central),r['neighbors'])
    edited={r['file'] for r in load('FILES_MODIFIED.json')}
    outside=[dict(file=r,before=v,after=b.a.sha(ROOT/r) if (ROOT/r).exists() else None) for r,v in before['protected'].items() if r not in edited and (not (ROOT/r).exists() or b.a.sha(ROOT/r)!=v)]
    ck('all_other_protected_files_preserved',not outside,outside)
    dump('CONCURRENT_CHANGES.json',dict(outside_scope_changes=outside,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False,all_preexisting_versions_preserved=not outside))
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False)
    dump('VALIDATION.json',result)
    print('Static',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']])
    return result['status']=='PASS'

DYNAMIC='common/dynamic_country_names/00_dynamic_country_names.txt'
REGIONS=['s:STATE_NORTH_MADAGASCAR','s:STATE_SOUTH_MADAGASCAR']

def prepare():
    if (LOT/'DEFINITION_INPUTS.json').exists():return
    p.h.dump('PLAN.json',p.make_plan());p.h.dump('COUNTRY_PROFILES.json',p.COUNTRIES)
    cat=b.a.catalog('common/country_definitions')
    assert all(t not in cat for t,r in p.COUNTRIES.items() if r.get('new')),'New TAG collision'
    definitions={t:raw(path)[n.start:n.end] for t,(n,path) in cat.items() if t in p.COUNTRIES and not p.COUNTRIES[t].get('new')}
    dump('DEFINITION_INPUTS.json',definitions);dump('HISTORY_INPUTS.json',histories())
    dump('COUNTRY_HISTORY_INPUTS.json',{t:raw_country_node(raw(ROOT/rel),t) for t,(rel,key) in histories().items()})
    dump('NATIVE_HISTORY_INPUTS.json',{});dump('CHARACTER_OVERLAYS.json',[])
    candidates=[]
    for path in b.tech.effective('common/history/characters'):
        text=raw(path)
        if any(n.key=='c:MAD' for n in b.walk(b.parse(text))):candidates.append(dict(file='common/history/characters/'+path.name,text=text,native=not path.is_relative_to(ROOT),source=str(path)))
    assert len(candidates)==1;dump('CHARACTER_INPUT.json',candidates[0])
    snap=contract.collect_snapshot();dump('STARTING_TECH_BEFORE.json',[contract.audit_country(t,snap) for t in ['MAD','FRA','POR']])

def scopes():
    result={ST:set(REGIONS),ARMY:{'c:MAD'},DYNAMIC:{'MAD'}}
    for folder in ['common/history/pops','common/history/buildings']:
        for path in b.tech.effective(folder):
            selected={n.key for n in b.walk(b.parse(raw(path))) if n.key in REGIONS and any(part.children('create_pop' if folder.endswith('pops') else 'create_building') for part in n.children('region_state:MAD'))}
            if selected:
                assert path.is_relative_to(ROOT);result[path.relative_to(ROOT).as_posix()]=selected
    for rel,key in histories().values():result[rel]={key}
    char=load('CHARACTER_INPUT.json')
    if not char['native']:result[char['file']]={'c:MAD'}
    return result

def transform(original):
    plan=load('PLAN.json');allocation=prior.m.allocations(original[ST],plan)
    out={ST:prior.m.transform({ST:original[ST]},plan)[ST]}
    char=load('CHARACTER_INPUT.json')
    for rel,text in original.items():
        if rel==ST:continue
        if rel==ARMY:
            n=b.one(text,'c:MAD');body=text[n.start:n.end]
            assert body.count('s:STATE_SOUTH_MADAGASCAR')==1
            out[rel]=b.edits(text,[(n.start,n.end,body.replace('s:STATE_SOUTH_MADAGASCAR','s:STATE_NORTH_MADAGASCAR'))])
        elif rel==DYNAMIC:
            n=b.one(text,'MAD');body=text[n.start:n.end]
            assert body.count('dyn_c_merina_kingdom_adj')==1
            out[rel]=b.edits(text,[(n.start,n.end,body.replace('dyn_c_merina_kingdom_adj','dyn_c_aor1776_antananarivo_adj').replace('dyn_c_merina_kingdom','dyn_c_aor1776_antananarivo'))])
        elif rel==char['file']:
            n=b.one(text,'c:MAD');out[rel]=b.edits(text,[(n.start,n.end,'c:MAD ?= { }')])
        elif '/history/countries/' in rel:
            n=b.one(text,'c:MAD');out[rel]=b.edits(text,[(n.start,n.end,country_body('MAD').rstrip('\n'))])
        else:out[rel]=prior.m.transform_portions(text,allocation,'/history/buildings/' in rel)
    return out

def additional():
    result=base_additional()
    result['common/history/diplomacy/'+PREFIX+'.txt']='DIPLOMACY = { c:BOI ?= { create_diplomatic_pact = { country = c:ATK type = tributary } } }\n'
    char=load('CHARACTER_INPUT.json')
    if char['native']:
        n=b.one(char['text'],'c:MAD');result[char['file']]=b.edits(char['text'],[(n.start,n.end,'c:MAD ?= { }')])
    for lang in ['french','english']:
        rel=f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml';adj='antananarivien' if lang=='french' else 'Antananarivan'
        result[rel]+=' MAD:0 "Antananarivo"\n MAD_ADJ:0 "'+adj+'"\n dyn_c_aor1776_antananarivo:0 "Antananarivo"\n dyn_c_aor1776_antananarivo_adj:0 "'+adj+'"\n'
    return result

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for k in ['preflight','apply','validate','tech']:a.add_argument('--'+k,action='store_true')
    args=a.parse_args()
    if args.preflight:preflight()
    if args.apply:apply()
    if args.tech:audit_tech()
    if args.validate:raise SystemExit(0 if validate() else 1)
