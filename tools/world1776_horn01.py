"""Bounded Horn restoration. --preflight writes proofs only; --apply once."""
import argparse,json,shutil
from collections import defaultdict,deque,Counter
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_horn01_plan as p
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
                assert path.is_relative_to(ROOT),'Review new filename overlay.'
                assert n.key[2:] not in result,'Multiple active histories.'
                result[n.key[2:]]=(path.relative_to(ROOT).as_posix(),n.key)
    return result

def scopes():
    plan=load('PLAN.json');regions={'s:'+r['state'] for r in plan};sources=defaultdict(set)
    for r in plan:sources['s:'+r['state']].add(r['source'])
    result={ST:regions,ARMY:{'c:ETH'}}
    for folder in ['common/history/pops','common/history/buildings']:
        for path in b.tech.effective(folder):
            selected=set()
            for n in b.walk(b.parse(raw(path))):
                if n.key in regions and any(n.children('region_state:'+t) for t in sources[n.key]):selected.add(n.key)
            if selected:
                assert path.is_relative_to(ROOT)
                result[path.relative_to(ROOT).as_posix()]=selected
    for rel,key in histories().values():result[rel]={key}
    return result

def country_body(tag):
    r=p.COUNTRIES[tag];effect='effect_aor1776_horn01_'+('decentralised' if r['kind']=='decentralized' else 'politics')
    return 'c:'+tag+' ?= {\n'+''.join(' add_technology_researched = '+t+'\n' for t in r['tech'])+' '+effect+' = yes\n'+(' effect_native_conscription_3 = yes\n' if r['kind']=='decentralized' else ' activate_law = law_type:law_oligarchy\n activate_law = law_type:law_slave_trade\n')+'}\n'

def transform(original):
    plan=load('PLAN.json');allocation=prior.m.allocations(original[ST],plan)
    # The inherited repeated Majeerteen token is not a second geographic cell.
    somalia=b.one(original[ST],'s:STATE_SOMALILAND')
    mjt=next(n for n in somalia.children('create_state') if n.one('country')=='c:MJT')
    targets={c:r['target'] for r in plan if r['state']=='STATE_SOMALILAND' and r['source']=='MJT' for c in r['RGBs']}
    allocation['STATE_SOMALILAND','MJT']=dict(Counter(targets.get(c,'MJT') for c in dict.fromkeys(prior.m.s.ids(mjt,'owned_provinces'))))
    out={ST:prior.m.transform({ST:original[ST]},plan)[ST]}
    node=b.one(out[ST],'s:STATE_SOMALILAND');ops=[]
    for part in node.children('create_state'):
        colors=prior.m.s.ids(part,'owned_provinces')
        if 'x2D75F4' in colors:
            assert colors.count('x2D75F4')==2,'Review inherited duplicate before rewriting.'
            field=part.children('owned_provinces')[0]
            ops.append((field.start,field.end,'owned_provinces = { '+' '.join(dict.fromkeys(colors))+' }'))
    assert len(ops)==1
    out[ST]=b.edits(out[ST],ops)
    # Keep existing imperial government offices at the surviving Gondarine
    # court. No levels/recipes are created; this is required by territorial loss.
    for rel,text in original.items():
        if rel==ST:continue
        if rel==ARMY:
            node=b.one(text,'c:ETH');ops=[]
            for n in b.walk([node]):
                if n.key=='combat_unit' and n.one('state_region')=='s:STATE_AMHARA':
                    f=n.children('state_region')[0];ops.append((f.start,f.end,'state_region = s:STATE_GONDER'))
            assert len(ops)==3,'Four dragoons, twelve irregulars, twenty-three conscripts: references only.'
            out[rel]=b.edits(text,ops);continue
        if '/history/countries/' in rel:
            owned=[n for n in b.walk(b.parse(text)) if n.key[2:] in p.COUNTRIES and n.key.startswith('c:')]
            assert len(owned)==1
            n=owned[0];out[rel]=b.edits(text,[(n.start,n.end,country_body(n.key[2:]).rstrip('\n'))]);continue
        if '/history/pops/' in rel:out[rel]=prior.m.transform_portions(text,allocation,False);continue
        assert '/history/buildings/' in rel,rel
        offices=[];remove=[]
        for n in b.walk(b.parse(text)):
            if not n.key.startswith('s:STATE_'):continue
            for part in n.children('region_state:ETH'):
                for item in part.children('create_building'):
                    if item.one('building','').strip('"')=='building_government_administration':
                        assert n.key in ['s:STATE_AMHARA','s:STATE_GONDER']
                        offices.append(text[item.start:item.end]);remove.append((item.start,item.end,''))
        stripped=b.edits(text,remove)
        updated=prior.m.transform_portions(stripped,allocation,True)
        if offices:
            state=b.one(updated,'s:STATE_GONDER');part=state.children('region_state:ETH')
            if part:where=part[0].end-1;insert='\n'+'\n'.join(offices)+'\n'
            else:where=state.end-1;insert='\nregion_state:ETH = {\n'+'\n'.join(offices)+'\n}\n'
            updated=b.edits(updated,[(where,where,insert)])
        out[rel]=updated
    return out

def additional():
    result={};definitions=[];cat=b.a.catalog('common/country_definitions')
    for tag,r in p.COUNTRIES.items():
        if r.get('new'):
            assert tag not in cat or cat[tag][1]==ROOT/'common/country_definitions'/f'{PREFIX}.txt'
            definitions.append(tag+' = { color = { '+' '.join(map(str,r['color']))+' } country_type = '+r['kind']+' tier = principality cultures = { '+' '.join(r['culture'])+' } religion = '+r['religion']+' capital = '+r['capital']+' }')
        else:
            n,path=cat[tag];text=raw(path)[n.start:n.end];ops=[]
            for field,value in [('capital',r['capital']),('country_type',r['kind'])]+([('religion',r['religion'])] if 'religion' in r else []):
                f=n.children(field)
                if f:ops.append((f[0].start-n.start,f[0].end-n.start,field+' = '+value))
                else:ops.append((n.end-n.start-1,n.end-n.start-1,'\n '+field+' = '+value+'\n'))
            definitions.append(b.edits(text,ops))
    result['common/country_definitions/'+PREFIX+'.txt']='\n\n'.join(definitions)+'\n'
    present=histories()
    for t in p.COUNTRIES:
        if t not in present:result['common/history/countries/'+t.lower()+' - 1776 horn.txt']='COUNTRIES = { '+country_body(t)+'}\n'
    result['common/scripted_effects/'+PREFIX+'.txt']=prior.additional()['common/scripted_effects/1776_world_sahel0607.txt'].replace('sahel0607','horn01')
    law,path=b.a.catalog('common/laws')['law_mercantilism'];mod=law.children('modifier')[0]
    allowed=' '.join('c:'+t+' ?= this' for t,r in p.COUNTRIES.items() if r['kind']!='decentralized')
    result['common/laws/'+PREFIX+'.txt']='law_aor1776_horn01_trade_customs = { group = lawgroup_trade_policy parent = law_mercantilism icon = "gfx/interface/icons/law_icons/mercantilism.dds" progressiveness = 0 unlocking_technologies = { international_relations } is_visible = { OR = { '+allowed+' } } can_enact = { OR = { '+allowed+' } } '+raw(path)[mod.start:mod.end]+' }\n'
    result['common/history/diplomacy/'+PREFIX+'.txt']='''DIPLOMACY = {
 # Provincial autonomy under a surviving imperial crown; not direct annexation.
 c:ETH ?= {
  create_diplomatic_pact = { country = c:TGR type = tributary }
  create_diplomatic_pact = { country = c:GJM type = tributary }
  create_diplomatic_pact = { country = c:WLO type = tributary }
 }
 # Shewa, Harar, Awsa and southern kingdoms are not forcibly made imperial subjects.
}
'''
    # Reactivated native templates are dated for 1836. Suppress them rather
    # than adding speculative 1776 rulers in a cartographic pass.
    for path in b.tech.effective('common/history/characters'):
        if any(path.name.startswith(t.lower()+' -') for t in p.COUNTRIES):
            assert not path.is_relative_to(ROOT) or path.name in ['tgr - tigray.txt','gjm - gojjam.txt','shw - shewa.txt','wlt - wolaita.txt','aws - aussa.txt','har - harar.txt','wlg - welega.txt'],str(path)
            rel='common/history/characters/'+path.name
            if (ROOT/rel).exists():assert raw(ROOT/rel).startswith('# HORN-01'), 'Current character overlay requires bounded review.'
            result[rel]='# HORN-01: do not instantiate native 1836 character templates for a reactivated 1776 polity.\nCHARACTERS = {}\n'
    for lang in ['french','english']:
        strings={}
        for t,r in p.COUNTRIES.items():
            if not r.get('new'):continue
            strings[t]=r['fr' if lang=='french' else 'en'];strings[t+'_ADJ']=r['adj_fr' if lang=='french' else 'adj_en']
        # Explicit plural labels: these native tags now aggregate autonomous
        # communities, not later monarchies or a modern ethnic province.
        names={
            'WLG':('Communautés de Wallaga et du Gibe','Wallaga and Gibe Communities','oromo','Oromo'),
            'ARS':('Oromo de l’Est','Eastern Oromo','oromo','Oromo'),
            'BRN':('Borana et Guji','Borana and Guji','borana','Borana'),
            'HDY':('Hadiya et Kambata','Hadiya and Kambata','hadiya','Hadiya'),
            'OGD':('Communautés somalies','Somali Communities','somali','Somali'),
        }
        for t,(fr,en,afr,aen) in names.items():strings[t]=fr if lang=='french' else en;strings[t+'_ADJ']=afr if lang=='french' else aen
        strings.update(law_aor1776_horn01_trade_customs='Coutumes commerciales' if lang=='french' else 'Trade Customs',law_aor1776_horn01_trade_customs_desc='Marchés et caravanes acquittent leurs droits auprès des autorités locales.' if lang=='french' else 'Markets and caravans pay dues to the local authorities.')
        result[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
    return result

def geometry(text,render=True):
    own=prior.m.state_owners(text);image=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'))[1680:2140,4850:5500]
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
    for tag in list(p.COUNTRIES)+['ETH','GLD','MJT','ISQ','WSG']:
        yy,xx=np.where(code==ids.get(tag,-1));points=set(zip(xx.tolist(),yy.tolist()));components=[]
        while points:
            start=points.pop();q=deque([start]);size=0
            while q:
                x,y=q.popleft();size+=1
                for xy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if xy in points:points.remove(xy);q.append(xy)
            components.append(size)
        result.append(dict(TAG=tag,components=sorted(components,reverse=True),neighbors=sorted(adj[tag]),kind=p.COUNTRIES.get(tag,{}).get('kind','unrecognized')))
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
        out=Image.fromarray(rgb).resize((1950,1380),Image.Resampling.NEAREST);d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
        for t in list(p.COUNTRIES)+['ETH','GLD','MJT','ISQ','WSG','TUR','SD1','SNR']:
            yy,xx=np.where(code==ids.get(t,-1))
            if not xx.size:continue
            j=np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2)
            d.text((int(xx[j])*3,int(yy[j])*3),t,font=font,fill='white',stroke_width=2,stroke_fill='black')
        out.save(LOT/'PROPOSED.png')
    print('Disconnected:',[(r['TAG'],r['components']) for r in result if len(r['components'])!=1]);print('Central isolated:',[(r['TAG'],r['neighbors']) for r in result if r['kind']!='decentralized' and not any(n not in p.DECENTRAL and n!='SD1' for n in r['neighbors'])])
    return result

def preflight():
    if not (LOT/'HISTORY_INPUTS.json').exists():dump('HISTORY_INPUTS.json',histories())
    scope=scopes();old={r:raw(ROOT/r) for r in scope};updated=transform(old)
    for rel,text in updated.items():save(LOT/'staged'/rel,text,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    for rel,text in additional().items():save(LOT/'staged'/rel,text,rel.endswith('.yml'))
    dump('SCOPES.json',{r:sorted(v) for r,v in scope.items()});geometry(updated[ST])

def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed.'
    if not (LOT/'HISTORY_INPUTS.json').exists():dump('HISTORY_INPUTS.json',histories())
    scope=scopes();new=additional();assert all(not (ROOT/r).exists() for r in new),'Review new-file collision.'
    current=raw(ROOT/ST);owners=prior.m.state_owners(current)
    for r in load('PLAN.json'):
        for color in r['RGBs']:assert owners.get(color) and all(v==[r['state'],r['source']] for v in owners[color]),(color,owners.get(color))
    old={r:raw(ROOT/r) for r in scope};updated=transform(old);hashes={r:b.a.sha(ROOT/r) for r in scope}
    prior.m.s.g.LOT=LOT
    before=dict(inventory=prior.m.s.b4.inventory(),protected=prior.m.s.g.protection(),scope={r:sorted(v) for r,v in scope.items()},new_files=list(new),historical_date='1776-01-01',deduplicated_RGB='x2D75F4')
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
    new=[contract.audit_country(t,snap,dict(required=r['tech'],allowed=r['tech'],historical_evidence=r['basis'])) for t,r in p.COUNTRIES.items()]
    existing=[contract.audit_country(r['TAG'],snap) for r in load('STARTING_TECH_BEFORE.json')]
    dump('STARTING_TECH_NEW_COUNTRIES.json',new);dump('STARTING_TECH_EXISTING_AFTER.json',existing)
    old={r['TAG']:r for r in load('STARTING_TECH_BEFORE.json')};comparison=[]
    for r in existing:
        a={json.dumps(f,sort_keys=True) for f in old[r['TAG']]['findings'] if f['priority'] in ['P0','P1']};z={json.dumps(f,sort_keys=True) for f in r['findings'] if f['priority'] in ['P0','P1']}
        comparison.append(dict(TAG=r['TAG'],inherited_remaining=[json.loads(f) for f in sorted(a&z)],introduced=[json.loads(f) for f in sorted(z-a)],resolved=[json.loads(f) for f in sorted(a-z)]))
    dump('TECH_NON_REGRESSION.json',dict(new_profiles=len(new),all_new_profiles_pass=all(r['status']=='PASS_STATIC_ONLY' for r in new),existing_country_comparison=comparison,shared_graph_changes=0,shared_recipe_changes=0,human_validated=False))
    print('Profiles:',[(r['TAG'],r['status'],r['findings']) for r in new]);print('New existing P0/P1:',[(r['TAG'],r['introduced']) for r in comparison if r['introduced']])

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
    owners['x2D75F4']=list(dict.fromkeys(tuple(v) for v in owners['x2D75F4']));owners['x2D75F4']=[list(v) for v in owners['x2D75F4']]
    ck('exact_global_owner_delta',owners==now['owners'])
    ck('inherited_Majeerteen_duplicate_resolved',len(now['owners']['x2D75F4'])==1)
    ck('no_new_duplicate',{c for c,v in now['owners'].items() if len(v)>1}<={c for c,v in before['inventory']['owners'].items() if len(v)>1})
    ck('world_population_conserved',now['world_population']==before['inventory']['world_population'])
    ck('Git_identity_index_unchanged',now['git']==before['inventory']['git'])
    cat=b.a.catalog('common/country_definitions');cultures=b.a.catalog('common/cultures')
    for t,r in p.COUNTRIES.items():
        n,path=cat[t];ck('own_effective_definition.'+t,path==ROOT/'common/country_definitions'/f'{PREFIX}.txt')
        ck('capital_region_owned.'+t,any([n.one('capital'),t] in v for v in now['owners'].values()))
        ck('political_type.'+t,n.one('country_type')==r['kind']);ck('known_cultures.'+t,set(prior.m.s.ids(n,'cultures'))<=set(cultures))
    ck('imperial_capital_Gondar_preserved',now['owners']['xDF2090']==[['STATE_GONDER','ETH']])
    ck('Asmara_in_highland_Tigray',now['owners']['x64B77C']==[['STATE_ERITREA','TGR']])
    ck('Massawa_Ottoman_port_preserved',now['owners']['x7090A0']==before['inventory']['owners']['x7090A0'])
    ck('Ankober_in_Shewa',now['owners']['xD6B588']==[['STATE_OROMIA','SHW']])
    ck('Mogadishu_in_Hiraab',now['owners']['x894078']==[['STATE_SOMALILAND','HRI']])
    for r,text in additional().items():
        ck('generated_file_exact.'+r,raw(ROOT/r)==text)
        if r.endswith('.yml'):ck('localization_BOM.'+r,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
    geometry_rows=geometry(raw(ROOT/ST));central={t for t,(n,path) in cat.items() if n.one('country_type')!='decentralized'}
    for r in geometry_rows:
        if r['kind']=='decentralized':continue
        ck('central_country_contiguous.'+r['TAG'],len(r['components'])==1,r['components'])
        ck('no_central_enclave_in_decentralised_land.'+r['TAG'],bool(set(r['neighbors'])&central),r['neighbors'])
    edited={r['file'] for r in load('FILES_MODIFIED.json')}
    outside=[dict(file=r,before=v,after=b.a.sha(ROOT/r) if (ROOT/r).exists() else None) for r,v in before['protected'].items() if r not in edited and (not (ROOT/r).exists() or b.a.sha(ROOT/r)!=v)]
    ck('all_other_protected_current_files_preserved',not outside,outside)
    dump('CONCURRENT_CHANGES.json',dict(outside_scope_changes=outside,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False,all_preexisting_versions_preserved=not outside))
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False)
    dump('VALIDATION.json',result)
    print('Static',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']])
    return result['status']=='PASS'

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for k in ['preflight','apply','validate','tech']:a.add_argument('--'+k,action='store_true')
    args=a.parse_args()
    if args.preflight:preflight()
    if args.apply:apply()
    if args.tech:audit_tech()
    if args.validate:raise SystemExit(0 if validate() else 1)
