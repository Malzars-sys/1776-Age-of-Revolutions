"""Install bounded Senegambian, Mali and Hausa territorial reforms.

Explicit native RGB lists, current-file node patches, exact population/asset
conservation. No bitmap, common technology graph, recipe, Git or vanilla writes.
"""
import argparse
import json
import shutil
from collections import Counter, defaultdict, deque
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import world1776_sahel0205_plan as planmod
import world1776_sahel01 as s

ROOT, LOT, PREFIX = planmod.ROOT, planmod.LOT, planmod.PREFIX
ST = s.ST
OVERRIDES = ['CAY','JLF','BND','SRR','KBU','SGU','MSN','GAO']
COAST_COUNTRIES = ['CAY','JLF','BND','SRR','KBU']
PATCH_COUNTRIES = COAST_COUNTRIES + ['HAU']
ARMY = 'common/history/military_formations/07_military_formations_subsaharan_africa.txt'


def dump(name, obj):
    (LOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def load(name):
    return json.loads((LOT/name).read_text('utf8'))


def raw(p): return s.b.a.raw(p)


def external_review():
    path=LOT/'EXTERNAL_COMPOSITION_REVIEW.json'
    return load(path.name) if path.exists() else None


def reviewed_external(rel,current_hash):
    review=external_review()
    return bool(review and review['status']=='VERIFIED_PRESERVED' and review['outputs'].get(rel)==current_hash)


def state_owners(text):
    result=defaultdict(list)
    for node in s.b.walk(s.b.parse(text)):
        if node.key.startswith('s:STATE_'):
            for part in node.children('create_state'):
                for color in s.ids(part,'owned_provinces'):result[color].append([node.key[2:],part.one('country')[2:]])
    return dict(result)


def save_text(path, text, bom=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'')+text.encode('utf8'))


def scope_text(text, key):
    n=s.b.one(text,key)
    return text[n.start:n.end]


def allocations(states, plan):
    """Per-source portion counts after the explicit territorial decisions."""
    grouped=defaultdict(dict)
    for row in plan:
        key=row['state'],row['source']
        for color in row['RGBs']:
            assert color not in grouped[key],(key,color)
            grouped[key][color]=row['target']
    result={}
    for (sid,source),changes in grouped.items():
        node=s.b.one(states,'s:'+sid)
        original=s.ids(s.part(node,source),'owned_provinces')
        assert set(changes)<=set(original)
        result[sid,source]=dict(Counter(changes.get(c,source) for c in original))
    return result


def changed_files(plan):
    wanted={r['state'] for r in plan}
    result={ST:set('s:'+x for x in wanted),ARMY:{'c:MSN'}}
    for folder in ['common/history/pops','common/history/buildings']:
        for p in s.b.tech.effective(folder):
            text=raw(p)
            touched={n.key for n in s.b.walk(s.b.parse(text)) if n.key in {'s:'+v for v in wanted}}
            if not touched:continue
            # Only include files which actually contain a source portion moved.
            meaningful=set()
            for key in touched:
                n=s.b.one(text,key)
                if any(n.children('region_state:'+r['source']) for r in plan if r['state']==key[2:]):meaningful.add(key)
            if meaningful:
                assert p.is_relative_to(ROOT), 'Native filename must be copied explicitly before an overlay edit.'
                result[p.relative_to(ROOT).as_posix()]=meaningful
    for tag in PATCH_COUNTRIES:
        paths=list((ROOT/'common/history/countries').glob(tag.lower()+' - *.txt'))
        assert len(paths)==1,(tag,paths)
        result[paths[0].relative_to(ROOT).as_posix()]={'c:'+tag}
    return result


def politics_effect():
    text=raw(s.b.a.GAME/'common/scripted_effects/00_political_setup.txt')
    n=s.b.one(text,'effect_starting_politics_traditional')
    return text[n.start:n.end].replace('effect_starting_politics_traditional','effect_aor1776_sahel_starting_politics',1).replace('law_type:law_mercantilism','law_type:law_aor1776_sahel_trade_customs')+'\n'


def additions(assert_new=True):
    files={}
    cat=s.b.a.catalog('common/country_definitions')
    # Reproducible source catalogue excludes this lot's own generated overlay.
    for path in s.b.tech.effective('common/country_definitions'):
        if path == ROOT/'common/country_definitions'/f'{PREFIX}.txt':continue
        for node in s.b.parse(raw(path)):
            if node.key in OVERRIDES:cat[node.key]=(node,path)
    defs=[]
    for tag in OVERRIDES:
        n,p=cat[tag]
        if tag=='GAO':continue
        fragment=raw(p)[n.start:n.end]
        edits=[]
        if tag in COAST_COUNTRIES:
            field=n.children('country_type')[0]
            edits.append((field.start-n.start,field.end-n.start,'country_type = unrecognized'))
        if tag=='SGU':
            field=n.children('capital')[0]
            edits.append((field.start-n.start,field.end-n.start,'capital = STATE_EASTERN_MALI'))
        if tag=='MSN':
            if n.children('religion'):
                f=n.children('religion')[0];edits.append((f.start-n.start,f.end-n.start,'religion = animist'))
            else:edits.append((n.end-n.start-1,n.end-n.start-1,'\n religion = animist\n'))
        if tag=='SRR':
            f=n.children('cultures')[0]
            # Serer is absent from the installed culture catalogue. Use the
            # regional Wolof/Mande IDs, including the Guelwar aristocratic origin.
            edits.append((f.start-n.start,f.end-n.start,'cultures = { mande wolof }'))
        defs.append(s.b.edits(fragment,edits))
    for tag, data in planmod.COUNTRIES.items():
        if assert_new and tag!='GAO':assert tag not in cat, 'TAG collision: '+tag
        defs.append(tag+' = {\n color = { '+' '.join(map(str,data['color']))+' }\n country_type = '+data.get('kind','unrecognized')+'\n tier = principality\n cultures = { '+' '.join(data['culture'])+' }\n religion = '+data['religion']+'\n capital = '+data['capital']+'\n}\n')
        effect='effect_aor1776_sahel_decentralised_starting_politics' if data.get('kind')=='decentralized' else 'effect_aor1776_sahel_starting_politics'
        files['common/history/countries/'+tag.lower()+' - 1776 sahel.txt']='COUNTRIES = { c:'+tag+' ?= {\n'+''.join(' add_technology_researched = '+v+'\n' for v in data['tech'])+' '+effect+' = yes\n'+(' activate_law = law_type:law_oligarchy\n activate_law = law_type:law_slave_trade\n' if data.get('kind')!='decentralized' else ' effect_native_conscription_3 = yes\n')+'} }\n'
    files['common/country_definitions/'+PREFIX+'.txt']='\n\n'.join(defs)+'\n'
    native=raw(s.b.a.GAME/'common/scripted_effects/00_political_setup.txt')
    n=s.b.one(native,'effect_starting_politics_traditional')
    branch=next(c for c in n.children('if') if 'is_country_type = decentralized' in native[c.start:c.end])
    prelude=[c for c in n.children() if c.end<=branch.start]
    body='\n'.join(native[c.start:c.end] for c in prelude+ [c for c in branch.children() if c.key!='limit'])
    files['common/scripted_effects/'+PREFIX+'.txt']=politics_effect()+'\n# Fixed decentralised start branch; no unreachable mercantile-law request.\neffect_aor1776_sahel_decentralised_starting_politics = {\n'+body+'\n}\n'
    law,p=s.b.a.catalog('common/laws')['law_mercantilism']
    mod=law.children('modifier')[0]
    allowed=COAST_COUNTRIES+[k for k,v in planmod.COUNTRIES.items() if v.get('kind')!='decentralized']
    files['common/laws/'+PREFIX+'.txt']='''law_aor1776_sahel_trade_customs = {
 group = lawgroup_trade_policy
 parent = law_mercantilism
 icon = "gfx/interface/icons/law_icons/mercantilism.dds"
 progressiveness = 0
 unlocking_technologies = { international_relations }
 is_visible = { OR = { '''+' '.join('c:'+tag+' ?= this' for tag in allowed)+''' } }
 can_enact = { OR = { '''+' '.join('c:'+tag+' ?= this' for tag in allowed)+' } }\n '+raw(p)[mod.start:mod.end]+'\n}\n'
    files['common/history/diplomacy/'+PREFIX+'.txt']='''# Ardo autonomy under Segou suzerainty, not annexation of the entire Macina.
DIPLOMACY = { c:SGU ?= { create_diplomatic_pact = { country = c:MSN type = tributary } } }
'''
    # Only suppression of native nineteenth-century founders/heirs; no new name.
    path='common/history/characters/msn - massina.txt'
    if assert_new:assert not (ROOT/path).exists(), 'Existing character overlay must be reviewed separately.'
    files[path]='# Pre-Diina Macina: do not instantiate the native nineteenth-century founder and heir templates.\nCHARACTERS = {}\n'
    for lang in ['french','english']:
        strings={}
        for tag,data in planmod.COUNTRIES.items():
            strings[tag]=data['fr' if lang=='french' else 'en']
            strings[tag+'_ADJ']=data['fr' if lang=='french' else 'en']
        strings.update({'SRR':'Sine','SRR_ADJ':'Sine','MSN':'Macina','MSN_ADJ':'Macina',
            'law_aor1776_sahel_trade_customs':'Coutumes commerciales' if lang=='french' else 'Trade Customs',
            'law_aor1776_sahel_trade_customs_desc':'Les marchands acquittent les droits locaux pour fréquenter les marchés et les voies de commerce.' if lang=='french' else 'Merchants pay local dues to use markets and trading routes.'})
        # Existing country names are deliberate native overrides, in replace/.
        files[f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
    return files


def transform_portions(text, allocation, buildings):
    ops=[]
    for sid in sorted({key[0] for key in allocation}):
        nodes=[n for n in s.b.walk(s.b.parse(text)) if n.key=='s:'+sid]
        if not nodes:continue
        assert len(nodes)==1
        state=nodes[0]
        source_tags={source for stateid,source in allocation if stateid==sid}
        by_target=defaultdict(list)
        removed=[]
        for portion in state.children():
            if not portion.key.startswith('region_state:'):continue
            source=portion.key.split(':')[1]
            if source not in source_tags:continue
            weights=allocation[sid,source]
            targets=sorted(weights)
            key='create_building' if buildings else 'create_pop'
            assert all(n.key==key for n in portion.children()),(sid,source)
            for item in portion.children(key):
                fields=[n for n in s.b.walk([item]) if n.key==('levels' if buildings else 'size')]
                assert len(fields)==1,(sid,source,key,len(fields))
                field=fields[0]
                amount=int(field.value)
                if buildings and sid=='STATE_EASTERN_MALI' and source=='MSN':
                    assigned={'MSN':amount}
                elif buildings and sid=='STATE_TIMBUKTU' and source=='MSN' and item.one('building').strip('"') in ['building_trade_center','building_textile_mill','building_salt_mine']:
                    assigned={'TMB':amount}
                else:assigned=dict(zip(targets,s.allocate(amount,[weights[t] for t in targets])))
                for target,value in assigned.items():
                    if not value:continue
                    fragment=text[item.start:item.end]
                    fragment=s.b.edits(fragment,[(field.start-item.start,field.end-item.start,field.key+' = '+str(value))])
                    if buildings:fragment=fragment.replace('c:'+source,'c:'+target)
                    by_target[target].append(fragment)
            removed.append(portion)
        if not removed:continue
        fragment=text[state.start:state.end]
        local=[(p.start-state.start,p.end-state.start,'') for p in removed]
        for target,items in by_target.items():
            existing=[p for p in state.children('region_state:'+target) if p not in removed]
            if existing:
                assert len(existing)==1
                p=existing[0]
                local.append((p.end-state.start-1,p.end-state.start-1,'\n'+'\n'.join(items)+'\n'))
            else:local.append((state.end-state.start-1,state.end-state.start-1,'\nregion_state:'+target+' = {\n'+'\n'.join(items)+'\n}\n'))
        ops.append((state.start,state.end,s.b.edits(fragment,local)))
    return s.b.edits(text,ops)


def transform(old, plan):
    state_source=old[ST]
    allocation=allocations(state_source,plan)
    changed_nodes={}
    for rel,text in old.items():
        if rel==ST:
            changes=defaultdict(dict)
            for r in plan:
                for color in r['RGBs']:changes[r['state']][color]=r['target']
            ops=[]
            for sid, delta in changes.items():
                n=s.b.one(text,'s:'+sid)
                fragment=text[n.start:n.end]
                portions=defaultdict(list)
                extras={}
                for portion in n.children('create_state'):
                    tag=portion.one('country')[2:]
                    extras[tag]=[text[c.start:c.end] for c in portion.children() if c.key not in ['country','owned_provinces']]
                    for color in s.ids(portion,'owned_provinces'):portions[delta.get(color,tag)].append(color)
                parts=[]
                for tag,colors in portions.items():
                    parts.append('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(colors)+' } '+' '.join(extras.get(tag,[]))+' }')
                # Keep all other fields (homelands/claims) from the current state.
                nodes=n.children('create_state')
                frag_ops=[(p.start-n.start,p.end-n.start,'') for p in nodes]
                frag_ops.append((nodes[0].start-n.start,nodes[0].start-n.start,'\n'.join(parts)+'\n'))
                fragment=s.b.edits(fragment,frag_ops)
                ops.append((n.start,n.end,fragment))
            changed_nodes[rel]=s.b.edits(text,ops)
        elif '/history/pops/' in rel or '/history/buildings/' in rel:
            changed_nodes[rel]=transform_portions(text,allocation,'/history/buildings/' in rel)
        elif rel==ARMY:
            n=s.b.one(text,'c:MSN')
            units=[p for p in s.b.walk([n]) if p.key=='combat_unit' and p.one('state_region')=='s:STATE_TIMBUKTU']
            assert len(units)==1 and units[0].one('count')=='1' and units[0].one('service_type')=='conscript'
            field=units[0].children('state_region')[0]
            changed_nodes[rel]=s.b.edits(text,[(field.start,field.end,'state_region = s:STATE_EASTERN_MALI')])
        elif '/history/countries/' in rel:
            if rel.endswith('hau - hausa.txt'):
                assert 'add_technology_researched = organized_military_establishments' not in text
                n=s.b.one(text,'c:HAU');position=text.index('{',n.start)+1
                changed_nodes[rel]=s.b.edits(text,[(position,position,'\n add_technology_researched = organized_military_establishments\n')])
                continue
            assert text.count('effect_starting_politics_traditional')==1,rel
            result=text.replace('effect_starting_politics_traditional','effect_aor1776_sahel_starting_politics',1)
            # Local diplomatic practice independently attested in treaties or
            # confederate relations; no broad tier or science grants are added.
            if 'add_technology_researched = international_relations' not in text:
                n=s.b.one(result,next(k for k in ['c:'+t for t in COAST_COUNTRIES] if k in result))
                result=s.b.edits(result,[(n.start+result[n.start:n.end].index('{')+1,n.start+result[n.start:n.end].index('{')+1,'\n add_technology_researched = international_relations\n')])
            changed_nodes[rel]=result
        else:raise AssertionError(rel)
    return changed_nodes


def geometry_review(states):
    changes=load('PLAN.json')
    after=transform({ST:states},changes)[ST]
    inv={}
    for n in s.b.walk(s.b.parse(after)):
        if not n.key.startswith('s:STATE_'):continue
        for p in n.children('create_state'):
            for color in s.ids(p,'owned_provinces'):inv[color]=(n.key[2:],p.one('country')[2:])
    image=np.asarray(Image.open(ROOT/s.BMP).convert('RGB'))[1690:2000,3680:4460]
    pack=image[:,:,0].astype('uint32')*65536+image[:,:,1].astype('uint32')*256+image[:,:,2]
    records=[]
    for tag in list(planmod.COUNTRIES)+['HAU','MSN','SGU','CAY','JLF','SRR']:
        colors=[int(c[1:],16) for c,v in inv.items() if v[1]==tag]
        ys,xs=np.where(np.isin(pack,colors))
        points=set(zip(xs.tolist(),ys.tolist()))
        sizes=[]
        while points:
            point=next(iter(points));points.remove(point);q=deque([point]);count=0
            while q:
                x,y=q.popleft();count+=1
                for xy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if xy in points:points.remove(xy);q.append(xy)
            sizes.append(count)
        records.append(dict(TAG=tag,components=sorted(sizes,reverse=True),native_province_count=len(colors)))
    dump('GEOMETRY_PREFLIGHT.json',records)
    print('Proposed disconnected portions:',[(r['TAG'],r['components']) for r in records if len(r['components'])>1])
    return records


def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed.'
    text=raw(ROOT/ST)
    plan=planmod.make_plan(text)
    assert plan==load('PLAN.json'),'Current ownership differs from reviewed plan.'
    scope=changed_files(plan)
    new=additions()
    assert all(not (ROOT/r).exists() for r in new),'New-file collision; review current workspace.'
    original={r:raw(ROOT/r) for r in scope}
    updated=transform(original,plan)
    hashes={r:s.b.a.sha(ROOT/r) for r in scope}
    for rel in scope:
        target=LOT/'apply_inputs'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/rel,target)
    s.g.LOT=LOT
    dump('APPLY_BEFORE.json',{'inventory':s.b4.inventory(),'protected':s.g.protection(),
         'scope':{r:sorted(k) for r,k in scope.items()},'new_files':list(new)})
    assert all(s.b.a.sha(ROOT/r)==h for r,h in hashes.items()),'Concurrent edit; reread before applying.'
    for rel,t in updated.items():
        save_text(ROOT/rel,t,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    for rel,t in new.items():save_text(ROOT/rel,t,rel.endswith('.yml'))
    dump('FILES_MODIFIED.json',[dict(file=r,before=hashes.get(r),after=s.b.a.sha(ROOT/r)) for r in list(scope)+list(new)])
    dump('COUNTRY_PROFILES.json',planmod.COUNTRIES)
    print('Installed',len(plan),'territorial groups;',sum(len(r['RGBs']) for r in plan),'RGB transfers;',len(new),'new files.')


def pop_cohorts(text):
    result=Counter()
    for n in s.b.walk(s.b.parse(text)):
        if n.key=='create_pop':result[tuple((c.key,str(c.value)) for c in n.children() if c.key!='size')]+=int(n.one('size'))
    return result


def building_inventory(text):
    result=Counter()
    for n in s.b.walk(s.b.parse(text)):
        if n.key!='create_building':continue
        levels=[v for v in s.b.walk([n]) if v.key=='levels']
        pms=tuple(sorted(s.ids(n,'activate_production_methods')))
        # A building may have several ownership parcels; all contribute levels.
        result[n.one('building'),pms]+=sum(int(v.value) for v in levels) if levels else int(n.one('level','1'))
    return result


def repair_compatibility():
    """Bounded follow-up to the first static run; keep its receipts immutable."""
    assert not (LOT/'COMPATIBILITY_REPAIR.json').exists(), 'Repair already applied.'
    before=load('APPLY_BEFORE.json')
    receipt={r['file']:r for r in load('FILES_MODIFIED.json')}
    generated=additions(False)
    updates={r:t for r,t in generated.items() if raw(ROOT/r)!=t}
    hau='common/history/countries/hau - hausa.txt'
    assert s.b.a.sha(ROOT/hau)==before['protected'][hau], 'Concurrent Gobir edit.'
    original={ST:raw(LOT/'apply_inputs'/ST),hau:raw(ROOT/hau)}
    updates[hau]=transform(original,load('PLAN.json'))[hau]
    hashes={r:s.b.a.sha(ROOT/r) for r in updates}
    for rel in updates:
        if rel!=hau:assert hashes[rel]==receipt[rel]['after'], 'Concurrent edit: '+rel
        target=LOT/'repair_inputs'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/rel,target)
    for name in ['VALIDATION.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json']:
        if (LOT/name).exists():shutil.copy2(LOT/name,LOT/name.replace('.json','_RUN01.json'))
    assert all(s.b.a.sha(ROOT/r)==h for r,h in hashes.items())
    for rel,text in updates.items():save_text(ROOT/rel,text,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
    dump('COMPATIBILITY_REPAIR.json',dict(
        reason='Correct Sine field offsets; flatten the five decentralised startup branches; supply Gobir military-site prerequisite only.',
        additional_existing_scope={hau:['c:HAU']},
        files=[dict(file=r,before=h,after=s.b.a.sha(ROOT/r)) for r,h in hashes.items()],
        technology_grant={'HAU':['organized_military_establishments']},
        shared_technology_graph_changes=0,shared_recipe_changes=0))
    print('Compatibility repair:',len(updates),'bounded files.')


def validate():
    before=load('APPLY_BEFORE.json')
    checks=[]
    def ck(name,val,detail=None):checks.append(dict(check=name,passed=bool(val),detail=detail))
    original={r:raw(LOT/'apply_inputs'/r) for r in before['scope']}
    scopes=dict(before['scope'])
    if (LOT/'COMPATIBILITY_REPAIR.json').exists():
        scopes.update(load('COMPATIBILITY_REPAIR.json')['additional_existing_scope'])
        for rel in load('COMPATIBILITY_REPAIR.json')['additional_existing_scope']:
            original[rel]=raw(LOT/'repair_inputs'/rel)
    expected=transform(original,load('PLAN.json'))
    for rel,text in expected.items():
        current=raw(ROOT/rel)
        compare=current
        if rel==ST and external_review():
            review=external_review()
            ck('reviewed_external_shared_state_version',s.b.a.sha(ROOT/rel)==review['outputs'][rel])
            compare=raw(LOT/'external_reference/own_applied_states.txt')
            for key in scopes[rel]:ck('own_state_node_preserved_through_external_composition.'+key,scope_text(current,key)==scope_text(text,key))
        ck('exact_scoped_patch_before_any_reviewed_external_update.'+rel,compare==text)
        keys=scopes[rel]
        def outside(t):
            nodes=[s.b.one(t,k) for k in keys]
            return s.b.edits(t,[(n.start,n.end,'<OWNED_NODE>') for n in nodes])
        ck('outside_owned_nodes_preserved_by_our_patch.'+rel,outside(original[rel])==outside(compare))
        if '/history/pops/' in rel:ck('all_cohorts_conserved.'+rel,pop_cohorts(original[rel])==pop_cohorts(current))
        if '/history/buildings/' in rel:ck('all_building_levels_and_PM_recipes_conserved.'+rel,building_inventory(original[rel])==building_inventory(current))
    now=s.b4.inventory()
    owners=dict(before['inventory']['owners'])
    for row in load('PLAN.json'):
        for color in row['RGBs']:
            ck('old_single_owner.'+color,owners.get(color)==[[row['state'],row['source']]])
            owners[color]=[[row['state'],row['target']]]
    review=external_review()
    if review:
        prior=state_owners(raw(LOT/'external_reference/own_applied_states.txt'))
        later=state_owners(raw(LOT/'external_reference/composed_states.txt'))
        for color in set(prior)|set(later):
            if prior.get(color)==later.get(color):continue
            ck('external_owner_input_matches_own_applied_state.'+color,owners.get(color)==prior.get(color))
            if color in later:owners[color]=later[color]
            else:owners.pop(color,None)
    ck('exact_declared_owner_delta_only',owners==now['owners'])
    ck('world_population_unchanged',now['world_population']==before['inventory']['world_population'],now['world_population'])
    ck('Git_identity_and_index_unchanged',now['git']==before['inventory']['git'])
    old_duplicates={k for k,v in before['inventory']['owners'].items() if len(v)>1}
    current_duplicates={k for k,v in now['owners'].items() if len(v)>1}
    ck('no_new_duplicate_owner',current_duplicates<=old_duplicates,dict(removed_by_reviewed_composition=sorted(old_duplicates-current_duplicates),introduced=sorted(current_duplicates-old_duplicates)))
    ck('no_Sokoto_country_portion_remains',not any(any(p[1]=='SOK' for p in portions) for portions in now['owners'].values()))
    ck('Segou_hub_owned_by_Segou',now['owners']['x2A6A2D']==[['STATE_EASTERN_MALI','SGU']])
    ck('Sikasso_not_a_centralised_future_kingdom',now['owners']['x320EE8']==[['STATE_EASTERN_MALI','SNU']])
    cat=s.b.a.catalog('common/country_definitions')
    cultures=s.b.a.catalog('common/cultures')
    for tag in set(OVERRIDES)|set(planmod.COUNTRIES):
        n,p=cat[tag]
        ck('exact_nonempty_culture_field.'+tag,len(n.children('cultures'))==1 and bool(s.ids(n,'cultures')))
        ck('known_culture_identifiers.'+tag,set(s.ids(n,'cultures'))<=set(cultures))
        ck('definition_field_schema.'+tag,set(c.key for c in n.children())<={'color','country_type','tier','cultures','religion','capital','is_named_from_capital'})
    ck('Sine_culture_proxy_exact',s.ids(cat['SRR'][0],'cultures')==['mande','wolof'])
    for tag,data in planmod.COUNTRIES.items():
        n,p=cat[tag]
        ck('definition_effective.'+tag,p==ROOT/'common/country_definitions'/f'{PREFIX}.txt')
        ck('capital_in_owned_region.'+tag,any(any(v==[n.one('capital'),tag] for v in portions) for portions in now['owners'].values()))
        ck('political_type.'+tag,n.one('country_type')==data.get('kind','unrecognized'))
    for tag in COAST_COUNTRIES:ck('royal_state_not_decentralised.'+tag,cat[tag][0].one('country_type')=='unrecognized')
    edited={r['file'] for r in load('FILES_MODIFIED.json')}
    if (LOT/'COMPATIBILITY_REPAIR.json').exists():edited.update(r['file'] for r in load('COMPATIBILITY_REPAIR.json')['files'])
    delta=[dict(file=r,before=h,after=s.b.a.sha(ROOT/r) if (ROOT/r).exists() else None) for r,h in before['protected'].items() if r not in edited and (not (ROOT/r).exists() or s.b.a.sha(ROOT/r)!=h)]
    ck('all_other_existing_files_preserved_except_verified_external_update',all(reviewed_external(r['file'],r['after']) for r in delta),delta)
    for rel in before['new_files']:
        ck('new_file_exists.'+rel,(ROOT/rel).is_file())
        if rel.endswith('.yml'):ck('BOM_and_header.'+rel,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf') and raw(ROOT/rel).startswith('l_'+('french' if '/french/' in rel else 'english')+':'))
    for rel,text in additions(False).items():ck('generated_file_exact.'+rel,raw(ROOT/rel)==text)
    geometry=geometry_review(original[ST])
    for rec in geometry:
        if rec['TAG'] in planmod.COUNTRIES:ck('new_country_contiguous.'+rec['TAG'],len(rec['components'])==1,rec['components'])
    dump('CONCURRENT_CHANGES.json',dict(outside_scope_changes=delta,external_review='EXTERNAL_COMPOSITION_REVIEW.json' if review else None,all_external_updates_preserved=True,Git_writes=0,vanilla_writes=0,SERG_writes=0))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime='NOT_RUN',human_validation=False)
    dump('VALIDATION.json',result)
    ledger=load('POPULATION_LEDGER.json') if (LOT/'POPULATION_LEDGER.json').exists() else {}
    ledger.update(world_before=before['inventory']['world_population'],world_after=now['world_population'],delta=now['world_population']-before['inventory']['world_population'],method='Conservative cohort split by enumerated native province counts, not a census/density estimate; no conversion of culture/religion/slave status.')
    dump('POPULATION_LEDGER.json',ledger)
    print(json.dumps({k:result[k] for k in ['status','passed','total']}))
    print('FAIL',[(c['check'],c['detail']) for c in checks if not c['passed']])
    return result['status']=='PASS'


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--preflight',action='store_true')
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--validate',action='store_true')
    parser.add_argument('--repair-compatibility',action='store_true')
    args=parser.parse_args()
    if args.preflight:geometry_review(raw(ROOT/ST))
    if args.apply:apply()
    if args.repair_compatibility:repair_compatibility()
    if args.validate:raise SystemExit(0 if validate() else 1)
