"""Bounded Chad/Nile restoration with immutable inputs and conservation checks."""
import argparse,json,shutil
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_sahel0205 as m
import world1776_sahel0607_plan as p
ROOT,LOT,ST,PREFIX=p.ROOT,p.LOT,p.ST,p.PREFIX

def dump(name,obj):p.q.dump(name,obj)
def load(name):return json.loads((LOT/name).read_text('utf8'))
def raw(path):return m.raw(path)
def save(path,text,bom=False):m.save_text(path,text,bom)

def additional():
    cat=m.s.b.a.catalog('common/country_definitions');data={};defs=[]
    for tag,record in p.COUNTRIES.items():
        if tag in cat:assert tag=='SRA' or cat[tag][1]==ROOT/'common/country_definitions'/f'{PREFIX}.txt',tag
        defs.append(tag+' = {\n color = { '+' '.join(map(str,record['color']))+' }\n country_type = '+record.get('kind','unrecognized')+'\n tier = principality\n cultures = { '+' '.join(record['culture'])+' }\n religion = '+record['religion']+'\n capital = '+record['capital']+'\n}\n')
        effect='effect_aor1776_sahel0607_decentralised' if record.get('kind')=='decentralized' else 'effect_aor1776_sahel0607_politics'
        data['common/history/countries/'+tag.lower()+' - 1776 chad nile.txt']='COUNTRIES = { c:'+tag+' ?= {\n'+''.join(' add_technology_researched = '+v+'\n' for v in record['tech'])+' '+effect+' = yes\n'+(' effect_native_conscription_3 = yes\n' if record.get('kind')=='decentralized' else ' activate_law = law_type:law_oligarchy\n activate_law = law_type:law_slave_trade\n')+'} }\n'
    # Wadai's regional capital must contain its own Wara/Abeche nucleus.
    n,path=cat['WAD'];fragment=raw(path)[n.start:n.end];f=n.children('capital')[0]
    defs.append(m.s.b.edits(fragment,[(f.start-n.start,f.end-n.start,'capital = STATE_CHAD')]))
    data['common/country_definitions/'+PREFIX+'.txt']='\n'.join(defs)
    effect=m.additions(False)['common/scripted_effects/1776_world_sahel0205.txt']
    effect=effect.replace('effect_aor1776_sahel_starting_politics','effect_aor1776_sahel0607_politics').replace('effect_aor1776_sahel_decentralised_starting_politics','effect_aor1776_sahel0607_decentralised').replace('law_aor1776_sahel_trade_customs','law_aor1776_sahel0607_trade_customs')
    data['common/scripted_effects/'+PREFIX+'.txt']=effect
    native,path=m.s.b.a.catalog('common/laws')['law_mercantilism'];modifier=native.children('modifier')[0]
    allowed=[t for t,r in p.COUNTRIES.items() if r.get('kind')!='decentralized']
    data['common/laws/'+PREFIX+'.txt']='''law_aor1776_sahel0607_trade_customs = {
 group = lawgroup_trade_policy
 parent = law_mercantilism
 icon = "gfx/interface/icons/law_icons/mercantilism.dds"
 progressiveness = 0
 unlocking_technologies = { international_relations }
 is_visible = { OR = { '''+' '.join('c:'+t+' ?= this' for t in allowed)+''' } }
 can_enact = { OR = { '''+' '.join('c:'+t+' ?= this' for t in allowed)+' } }\n '+raw(path)[modifier.start:modifier.end]+'\n}\n'
    data['common/history/diplomacy/'+PREFIX+'.txt']='''DIPLOMACY = {
 # Local autonomy under Funj suzerainty, not annexation of every northern village.
 c:SNR ?= { create_diplomatic_pact = { country = c:ABD type = tributary } }
 # Mandara revolt circa 1781 is not pre-installed on 1 January 1776.
 c:BOR ?= { create_diplomatic_pact = { country = c:MDR type = tributary } }
 # Nominal Ottoman-Egyptian link of the Nubian kashifs and frontier garrisons.
 c:EGY ?= { create_diplomatic_pact = { country = c:NUB type = tributary } }
}
'''
    for lang in ['french','english']:
        strings={}
        for tag,r in p.COUNTRIES.items():strings[tag]=r['fr' if lang=='french' else 'en'];strings[tag+'_ADJ']=r['adj_fr' if lang=='french' else 'adj_en']
        strings.update(law_aor1776_sahel0607_trade_customs='Coutumes commerciales' if lang=='french' else 'Trade Customs',law_aor1776_sahel0607_trade_customs_desc='Les marchés et les caravanes acquittent des droits auprès des autorités locales.' if lang=='french' else 'Markets and caravans pay dues to the local authorities.')
        data[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
    return data

def scopes(plan):
    states={'s:'+r['state'] for r in plan};source_by_state=defaultdict(set)
    for r in plan:source_by_state['s:'+r['state']].add(r['source'])
    result={ST:states,m.ARMY:{'c:WAD'}}
    for folder in ['common/history/pops','common/history/buildings']:
        for path in m.s.b.tech.effective(folder):
            text=raw(path);selected=set()
            for n in m.s.b.walk(m.s.b.parse(text)):
                if n.key not in states:continue
                if any(n.children('region_state:'+t) for t in source_by_state[n.key]):selected.add(n.key)
            if selected:
                assert path.is_relative_to(ROOT),'Review native filename overlay before editing.'
                result[path.relative_to(ROOT).as_posix()]=selected
    return result

def transform(original,plan):
    out={ST:m.transform({ST:original[ST]},plan)[ST]}
    allocation=m.allocations(original[ST],plan)
    for rel,text in original.items():
        if rel==ST:continue
        if rel==m.ARMY:
            n=m.s.b.one(text,'c:WAD');ops=[]
            for unit in m.s.b.walk([n]):
                if unit.key=='combat_unit' and unit.one('state_region')=='s:STATE_WADDAI':
                    assert unit.one('service_type')=='conscript' and unit.one('count')=='1'
                    f=unit.children('state_region')[0];ops.append((f.start,f.end,'state_region = s:STATE_CHAD'))
            assert len(ops)==1
            out[rel]=m.s.b.edits(text,ops);continue
        assert '/history/pops/' in rel or '/history/buildings/' in rel,rel
        out[rel]=m.transform_portions(text,allocation,'/history/buildings/' in rel)
    return out

def geometry(states,render=True):
    own=m.state_owners(states)
    im=np.array(Image.open(ROOT/m.s.BMP).convert('RGB'))
    pack=im[:,:,0].astype('uint32')*65536+im[:,:,1].astype('uint32')*256+im[:,:,2]
    crop=pack[1300:1990,4300:5100]
    result=[]
    target_tags=list(p.COUNTRIES)+['WAD','BGI','BOR']
    adjacency=defaultdict(set)
    # Map native province numbers to country codes once, then derive actual
    # land border contact without a distance-to-capital partition.
    table={int(c[1:],16):v[-1][1] for c,v in own.items()}
    ids={t:i+1 for i,t in enumerate(sorted(set(table.values())))}
    tagmap=np.zeros(crop.shape,dtype='int32')
    for color in np.unique(crop):
        if int(color) in table:tagmap[crop==color]=ids[table[int(color)]]
    inv={v:k for k,v in ids.items()}
    for left,right in [(tagmap[:,:-1],tagmap[:,1:]),(tagmap[:-1,:],tagmap[1:,:])]:
        pairs=np.unique(np.stack([left.ravel(),right.ravel()],axis=1),axis=0)
        for a,b in pairs:
            if a and b and a!=b:adjacency[inv[a]].add(inv[b]);adjacency[inv[b]].add(inv[a])
    for tag in target_tags:
        ys,xs=np.where(tagmap==ids.get(tag,-1));points=set(zip(xs.tolist(),ys.tolist()));sizes=[]
        while points:
            x=next(iter(points));points.remove(x);queue=deque([x]);count=0
            while queue:
                x,y=queue.popleft();count+=1
                for xy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if xy in points:points.remove(xy);queue.append(xy)
            sizes.append(count)
        result.append(dict(TAG=tag,components=sorted(sizes,reverse=True),neighbors=sorted(adjacency[tag]),centralised=p.COUNTRIES.get(tag,{}).get('kind')!='decentralized'))
    # Every newly Egyptian pixel must have a land path to pre-existing Egypt
    # inside this survey window, including the Kharga corridor.
    egypt=tagmap==ids['EGY'];seen=np.zeros(egypt.shape,bool)
    before=load('APPLY_BEFORE.json')['inventory']['owners'] if (LOT/'APPLY_BEFORE.json').exists() else load('BASELINE.json')['inventory']['owners']
    old_colors=[int(c[1:],16) for c,v in before.items() if v[-1][1]=='EGY']
    yy,xx=np.where(egypt & np.isin(crop,old_colors));queue=deque(zip(xx.tolist(),yy.tolist()))
    for x,y in queue:seen[y,x]=True
    while queue:
        x,y=queue.popleft()
        for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if 0<=ny<egypt.shape[0] and 0<=nx<egypt.shape[1] and egypt[ny,nx] and not seen[ny,nx]:
                seen[ny,nx]=True;queue.append((nx,ny))
    transfers=[c for r in load('PLAN.json') if r['target']=='EGY' for c in r['RGBs']]
    corridor=[dict(RGB=c,pixels_in_survey=int((crop==int(c[1:],16)).sum()),connected_to_existing_Egypt=bool(np.all(seen[crop==int(c[1:],16)]))) for c in transfers]
    dump('EGYPT_CORRIDOR_CHECK.json',corridor)
    if render:
        palette={tag:tuple(v['color']) for tag,v in p.COUNTRIES.items()}
        for tag in ['BOR','BGI','WAD','DFR','SD1','EGY','TUR','TBI']:
            n,path=m.s.b.a.catalog('common/country_definitions')[tag];palette[tag]=tuple(map(int,m.s.ids(n,'color')))
        for name,box in [('CHAD',(4330,1670,4740,1950)),('NILE',(4700,1490,5020,1920))]:
            x0,y0,x1,y1=box;a=pack[y0:y1,x0:x1];rgb=np.zeros((*a.shape,3),dtype='uint8')+60
            for color in np.unique(a):
                tag=table.get(int(color));rgb[a==color]=palette.get(tag,(210,210,210))
            edge=np.zeros(a.shape,bool);country=np.zeros(a.shape,'int32')
            for color in np.unique(a):country[a==color]=ids.get(table.get(int(color)),0)
            edge[1:,:]|=country[1:,:]!=country[:-1,:];edge[:,1:]|=country[:,1:]!=country[:,:-1];rgb[edge]=(25,30,35)
            out=Image.fromarray(rgb).resize(((x1-x0)*4,(y1-y0)*4),Image.Resampling.NEAREST);d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
            for tag in sorted(set(table.get(int(c)) for c in np.unique(a))-{None}):
                if tag not in palette:continue
                mask=np.isin(a,[int(c[1:],16) for c,v in own.items() if v[-1][1]==tag]);yy,xx=np.where(mask)
                if xx.size<10:continue
                cx,cy=xx.mean(),yy.mean();i=np.argmin((xx-cx)**2+(yy-cy)**2)
                d.text((int(xx[i])*4,int(yy[i])*4),tag,font=font,fill='white',stroke_width=2,stroke_fill='black')
            out.save(LOT/(name+'_PROPOSED.png'))
    dump('GEOMETRY_PREFLIGHT.json',result)
    print('Disconnected:',[(r['TAG'],r['components']) for r in result if len(r['components'])!=1])
    print('Central neighbors:',[(r['TAG'],r['neighbors']) for r in result if r['centralised']])
    return result

def preflight():
    plan=load('PLAN.json');current=raw(ROOT/ST)
    original={rel:raw(ROOT/rel) for rel in scopes(plan)};updated=transform(original,plan)
    for rel,text in updated.items():
        path=LOT/'staged'/rel;save(path,text,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    for rel,text in additional().items():save(LOT/'staged'/rel,text,rel.endswith('.yml'))
    dump('PROPOSED_SCOPES.json',{r:sorted(v) for r,v in scopes(plan).items()})
    geometry(updated[ST])


def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed; do not replay.'
    plan=load('PLAN.json')
    assert p.make_plan(raw(ROOT/ST))==plan,'Ownership changed since review.'
    scope=scopes(plan);new=additional()
    assert all(not (ROOT/r).exists() for r in new),'New-file collision.'
    original={r:raw(ROOT/r) for r in scope};updated=transform(original,plan)
    hashes={r:m.s.b.a.sha(ROOT/r) for r in scope}
    for rel in scope:
        dest=LOT/'apply_inputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/rel,dest)
    m.s.g.LOT=LOT
    protected=m.s.g.protection()
    for f in (ROOT/'gfx/map/map_object_data').glob('*.txt'):protected[f.relative_to(ROOT).as_posix()]=m.s.b.a.sha(f)
    dump('APPLY_BEFORE.json',dict(inventory=m.s.b4.inventory(),protected=protected,
         scope={r:sorted(v) for r,v in scope.items()},new_files=list(new)))
    assert all(m.s.b.a.sha(ROOT/r)==h for r,h in hashes.items()),'Concurrent input update.'
    for rel,text in updated.items():
        assert m.s.b.a.sha(ROOT/rel)==hashes[rel],rel
        save(ROOT/rel,text,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    for rel,text in new.items():
        assert not (ROOT/rel).exists(),rel
        save(ROOT/rel,text,rel.endswith('.yml'))
    dump('FILES_MODIFIED.json',[dict(file=r,before=hashes.get(r),after=m.s.b.a.sha(ROOT/r)) for r in list(scope)+list(new)])
    print('Installed:',len(scope),'existing files,',len(new),'new files;',sum(len(r['RGBs']) for r in plan),'native province transfers.')


def validate():
    before=load('APPLY_BEFORE.json');plan=load('PLAN.json');checks=[]
    def ck(k,v,detail=None):checks.append(dict(check=k,passed=bool(v),detail=detail))
    original={r:raw(LOT/'apply_inputs'/r) for r in before['scope']}
    expected=transform(original,plan)
    for rel,text in expected.items():
        current=raw(ROOT/rel)
        ck('exact_declared_patch.'+rel,current==text)
        def outside(t):
            nodes=[m.s.b.one(t,k) for k in before['scope'][rel]]
            return m.s.b.edits(t,[(n.start,n.end,'<OWNED_NODE>') for n in nodes])
        ck('outside_owned_nodes_unchanged.'+rel,outside(current)==outside(original[rel]))
        if '/history/pops/' in rel:ck('cohort_conservation.'+rel,m.pop_cohorts(current)==m.pop_cohorts(original[rel]))
        if '/history/buildings/' in rel:ck('building_levels_and_recipes_conserved.'+rel,m.building_inventory(current)==m.building_inventory(original[rel]))
    now=m.s.b4.inventory();owners=dict(before['inventory']['owners'])
    for row in plan:
        for color in row['RGBs']:
            ck('single_original_owner.'+color,owners.get(color)==[[row['state'],row['source']]])
            owners[color]=[[row['state'],row['target']]]
    ck('exact_global_owner_delta',owners==now['owners'])
    ck('world_population_conserved',now['world_population']==before['inventory']['world_population'])
    ck('Git_identity_and_index_unchanged',now['git']==before['inventory']['git'])
    ck('no_new_duplicate_owner',{c for c,v in now['owners'].items() if len(v)>1}<={c for c,v in before['inventory']['owners'].items() if len(v)>1})
    cat=m.s.b.a.catalog('common/country_definitions');cultures=m.s.b.a.catalog('common/cultures')
    religions=m.s.b.a.catalog('common/religions')
    for tag,data in p.COUNTRIES.items():
        n,path=cat[tag]
        ck('own_effective_definition.'+tag,path==ROOT/'common/country_definitions'/f'{PREFIX}.txt')
        ck('one_known_culture_list.'+tag,len(n.children('cultures'))==1 and m.s.ids(n,'cultures')==data['culture'] and set(data['culture'])<=set(cultures))
        ck('known_religion.'+tag,n.one('religion') in religions)
        ck('capital_region_owned.'+tag,any([n.one('capital'),tag] in v for v in now['owners'].values()))
        ck('political_type.'+tag,n.one('country_type')==data.get('kind','unrecognized'))
        ck('definition_schema.'+tag,set(c.key for c in n.children())<={'color','country_type','tier','cultures','religion','capital'})
    ck('Wadai_capital_region_restored',cat['WAD'][0].one('capital')=='STATE_CHAD')
    ck('Wara_core_in_Wadai',now['owners']['xB08124']==[['STATE_CHAD','WAD']])
    edited={r['file'] for r in load('FILES_MODIFIED.json')}
    delta=[dict(file=r,before=h,after=m.s.b.a.sha(ROOT/r) if (ROOT/r).exists() else None) for r,h in before['protected'].items() if r not in edited and (not (ROOT/r).exists() or m.s.b.a.sha(ROOT/r)!=h)]
    ck('all_other_existing_functional_and_protected_files_unchanged',not delta,delta)
    for rel,text in additional().items():
        ck('generated_file_exact.'+rel,raw(ROOT/rel)==text)
        if rel.endswith('.yml'):
            ck('localization_BOM.'+rel,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
            ck('localization_header.'+rel,text.startswith('l_'+('french' if '/french/' in rel else 'english')+':'))
    records=geometry(raw(ROOT/ST))
    central={t for t,(n,path) in cat.items() if n.one('country_type')!='decentralized'}
    for r in records:
        ck('country_contiguous.'+r['TAG'],len(r['components'])==1,r['components'])
        if r['centralised']:ck('no_central_enclave_amid_decentralised_territories.'+r['TAG'],bool(set(r['neighbors'])&central),r['neighbors'])
    for r in load('EGYPT_CORRIDOR_CHECK.json'):ck('new_Egyptian_cell_connected_to_existing_Egypt.'+r['RGB'],r['pixels_in_survey']>0 and r['connected_to_existing_Egypt'])
    dump('CONCURRENT_CHANGES.json',dict(outside_scope_changes=delta,all_preexisting_versions_preserved=not delta,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime='NOT_RUN',human_validation=False)
    dump('VALIDATION.json',result)
    ledger=load('POPULATION_LEDGER.json') if (LOT/'POPULATION_LEDGER.json').exists() else {}
    ledger.update(world_before=before['inventory']['world_population'],world_after=now['world_population'],delta=now['world_population']-before['inventory']['world_population'],method='Conservative cohort split by enumerated native-province counts. Technical redistribution only, not a census or density estimate; all cohort attributes conserved.')
    dump('POPULATION_LEDGER.json',ledger)
    print('Static:',result['status'],result['passed'],'/',result['total']);print('FAIL:',[c for c in checks if not c['passed']])
    return result['status']=='PASS'

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for key in ['preflight','apply','validate']:a.add_argument('--'+key,action='store_true')
    args=a.parse_args()
    if args.preflight:preflight()
    if args.apply:apply()
    if args.validate:raise SystemExit(0 if validate() else 1)
