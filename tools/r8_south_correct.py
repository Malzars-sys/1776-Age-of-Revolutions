"""Bounded 1776 P0/P1 correction. Prepare, inspect, apply, independently validate.

Whole-province category-B regional fronts, never a claim of surveyed boundaries.
Unresolved Kentucky/Missouri, Gulf Texas, Florida and Apache fronts stay open.
No Git writes; no vanilla writes; current hashes guard shared-file mutations.
"""
import collections as C
import csv,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from hbc06_integrate import text,encoded,edit,ownership,state_nodes,rgb_block,NATIVE_LAWS
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from hbc03_quebec_arc import economic_inventory,conservation
from hbc02_map_candidates import graph
from r8_south_geometry import OUT,bitmap,load
from georeference.model import inverse

ST='common/history/states/00_states.txt'
PP='common/history/pops/05_north_america.txt'
CD='common/country_definitions/00_countries.txt'
PREFIX='1776_r8_southern_nations'
SCOPE={'STATE_'+s for s in ['ALABAMA','MISSISSIPPI','TENNESSEE','ARKANSAS','OKLAHOMA','TEXAS','MISSOURI','KENTUCKY']}
# Reused broad vanilla culture families are explicitly documented in REPORT.md.
GROUPS=[
 ('CHE','Cherokees','Cherokee','cherokee','STATE_TENNESSEE',[105,145,40]),
 ('MSC','Muscogees','Muscogee','muskogean','STATE_ALABAMA',[108,139,208]),
 ('CTW','Choctaws','Choctaw','muskogean','STATE_MISSISSIPPI',[184,118,63]),
 ('CKS','Chickasaws','Chickasaw','muskogean','STATE_MISSISSIPPI',[207,169,68]),
 ('CAD','Caddos','Caddo','caddoan','STATE_ARKANSAS',[71,156,140]),
 ('QPW','Quapaws','Quapaw','siouan','STATE_ARKANSAS',[148,104,164]),
 ('OSG','Osages','Osage','siouan','STATE_MISSOURI',[167,78,87]),
 ('WCH','Wichitas et Taovayas','Wichita and Taovaya','caddoan','STATE_OKLAHOMA',[113,157,164]),
]
COLORS={g[0]:g[5] for g in GROUPS}|{'COM':[219,124,56],'GBR':[184,69,78],'SC1':[198,183,98]}


def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def choose(state,lon,lat):
    """Explicit regional arbitration, not historical latitude/longitude borders.

    S1 contemporary SE map catalogue + S2/S3 homelands; S4/S5 Arkansas;
    S6 1770-72 Caddo records; S7 1759/1772 Taovaya. See SOURCES.md.
    Only old COM cells are eligible. Every output row retains its rule/source.
    """
    if state=='STATE_ALABAMA':
        if lat<31.05:return 'GBR','S2: Mobile coastal district, whole-cell approximation'
        if lat>34.4 and lon< -87.3:return 'CKS','S1/S3: northwest Alabama'
        if lat>34.4 and lon> -86.5:return 'CHE','S1/S8: northeast Alabama Cherokee margin'
        if lon< -87.8:return 'CTW','S1/S2: Tombigbee/Black Warrior western sector'
        return 'MSC','S1: Coosa/Tallapoosa Creek sector'
    if state=='STATE_MISSISSIPPI':
        if lat<31.05:return 'GBR','S2: Mobile treaty coastal strip, not all West Florida claims'
        return ('CKS','S1/S3: northern Mississippi') if lat>33.55 else ('CTW','S1/S2: central/southern Choctaw region')
    if state=='STATE_TENNESSEE':
        return ('CKS','S1/S3: western Tennessee hunting region') if lon< -87.6 else ('CHE','S1/S8/S9: eastern towns and contested Cumberland hunting region')
    if state=='STATE_ARKANSAS':
        if lat>35.05:return 'OSG','S4: northwest Arkansas seasonal Osage region'
        return ('QPW','S5: lower Arkansas regional Quapaw abstraction; Spanish post unresolved') if lon> -93.1 else ('CAD','S6: southwest Arkansas Red River Caddo region')
    if state=='STATE_OKLAHOMA':
        if lon< -98.7:return 'COM','S7/S10: western Southern Plains retained'
        if lat>35.65 and lon> -96:return 'OSG','S4: northeastern Osage margin, category B'
        if lat<34.45 and lon> -95.4:return 'CAD','S6: Red River eastern Caddo margin'
        return 'WCH','S7: Wichita/Canadian/upper Red River regional aggregate'
    if state=='STATE_TEXAS':
        if lat>33.4 and -99<lon< -95.4:return 'WCH','S7: upper Red River Taovaya/Wichita'
        if lon> -96.7 and lat>31.6:return 'CAD','S6: Hasinai/Kadohadacho East Texas'
    if state=='STATE_MISSOURI' and lon< -91.5 and 36.2<lat<38.9:
        return 'OSG','S4: western Missouri Osage; other Missouri fronts unresolved'
    if state=='STATE_KENTUCKY' and lon< -88.4:
        return 'CKS','S3: southwest Kentucky Chickasaw margin; other Kentucky fronts unresolved'
    return 'COM','RESEARCH_REQUIRED: unchanged pending beneficiary/post localization'


def pop_signature(node):
    return json.dumps(normalized([n for n in node.children() if n.key!='size']),ensure_ascii=False,sort_keys=True)


def population(raw):
    totals=C.Counter()
    for sid,s in state_nodes(raw).items():
        for rs in s.children():
            if rs.key.startswith('region_state:'):
                for n in rs.children('create_pop'):totals[sid,pop_signature(n)]+=int(n.one('size'))
    return sorted([[s,k,v] for (s,k),v in totals.items()])


def allocate(total,weights):
    """Largest remainders preserve every original cohort exactly, not a census."""
    denominator=sum(weights.values());out={t:total*w//denominator for t,w in weights.items()}
    order=sorted(weights,key=lambda t:(-(total*weights[t]%denominator),t))
    for t in order[:total-sum(out.values())]:out[t]+=1
    return out


def components(adj,cells):
    left=set(cells);out=[]
    while left:
        seed=left.pop();seen={seed};stack=[seed]
        while stack:
            for v in adj.get(stack.pop(),{}):
                if v in left:left.remove(v);seen.add(v);stack.append(v)
        out.append(sorted(seen))
    return sorted(out,key=len,reverse=True)


def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'APPLIED.json').exists(),'Already installed; validate instead.'
    before=runtime();own=ownership();a=bitmap()
    oldcom={r:next(iter(v))[0] for r,v in own.items() if any(t=='COM' for s,t in v)}
    assert all(len(own[r])==1 for r,s in oldcom.items() if s in SCOPE)
    dump('PREEXISTING_COM_OVERLAPS.json',{r:sorted(own[r]) for r in oldcom if len(own[r])!=1})
    mask=np.isin(a,[int(r[1:],16) for r in oldcom]);yy,xx=np.where(mask)
    vals=a[yy,xx];ids,inv,cnt=np.unique(vals,return_inverse=True,return_counts=True)
    sx=np.bincount(inv,weights=xx);sy=np.bincount(inv,weights=yy)
    centers={f'x{int(v):06X}':[float(sx[i]/cnt[i]),float(sy[i]/cnt[i])] for i,v in enumerate(ids)}
    assert set(oldcom)==set(centers)
    model=load(OUT/'GEODETIC_MODEL.json');rows=[];by=C.defaultdict(set)
    for r,sid in sorted(oldcom.items()):
        lon,lat=map(float,inverse(model,[centers[r]])[0])
        t,reason=choose(sid,lon,lat) if sid in SCOPE else ('COM','Outside authorized cell selection; retained')
        rows.append(dict(RGB=r,State_ID=sid,Before='COM',After=t,longitude_proxy=lon,latitude_proxy=lat,rule=reason,precision='CATEGORY_B_NOT_SURVEYED' if t!='COM' else 'UNCHANGED'))
        if sid in SCOPE:by[sid,t].add(r)
    changed=[r for r in rows if r['Before']!=r['After']]
    assert changed and {g[0] for g in GROUPS}<=set(r['After'] for r in changed)
    dump('BASELINE_RUNTIME.json',before)
    dump('BASELINE_OWNERS.json',{r:sorted(v) for r,v in own.items()})
    dump('BASELINE_HBC.json',economic_inventory())
    files={};raw=text(ROOT/ST);patch=[]
    for sid,s in state_nodes(raw).items():
        if sid not in SCOPE:continue
        old=s.children('create_state');source=[n for n in old if scalar(n.one('country'))=='c:COM'];assert len(source)==1
        n=source[0];assert set(provs(n,'owned_provinces'))=={r for r,ss in oldcom.items() if ss==sid}
        # No implicit ownership, incorporation or other source-specific state command is discarded.
        assert {v.key for v in n.children()}=={'country','owned_provinces'}
        additions=[]
        for (ss,t),cells in sorted(by.items()):
            if ss==sid:additions.append('\n\t\tcreate_state = {\n\t\t\tcountry = c:'+t+'\n\t\t\towned_provinces = '+rgb_block(cells)+'\n\t\t}')
        patch.append((n.start,n.end,'\n'.join(additions)))
        # Existing claims are retained; these homeland additions are broad engine abstractions.
        homelands={scalar(n.value) for n in s.children('add_homeland')}
        cultures={g[3] for g in GROUPS if (sid,g[0]) in by}
        addition=''.join('\n\t\tadd_homeland = cu:'+c+'\n' for c in sorted(cultures) if 'cu:'+c not in homelands)
        if addition:patch.append((s.end-1,s.end-1,addition))
    files[ST]=encoded(ROOT/ST,edit(raw,patch))
    # Pure population redistribution: no culture, religion, type or State total is changed.
    raw=text(ROOT/PP);patch=[];allocations=[]
    for sid,s in state_nodes(raw).items():
        if sid not in SCOPE:continue
        original=s.children('region_state:COM');assert len(original)==1
        n=original[0];assert all(v.key=='create_pop' for v in n.children())
        weights={t:len(cells) for (ss,t),cells in by.items() if ss==sid};bodies=C.defaultdict(list)
        for pop in n.children('create_pop'):
            nums=allocate(int(pop.one('size')),weights)
            for t,count in sorted(nums.items()):
                if not count:continue
                # Keep implicit religion implicit: the vanilla culture default remains unchanged.
                size=pop.children('size')[0];body=raw[pop.start:pop.end]
                body=body[:size.start-pop.start]+'size = '+str(count)+body[size.end-pop.start:]
                bodies[t].append(body)
                allocations.append(dict(state=sid,tag=t,size=count,original_size=int(pop.one('size')),cohort=pop_signature(pop),method='TECHNICAL_WHOLE_PROVINCE_COUNT_ALLOCATION_NOT_HISTORICAL_CENSUS'))
        new='\n'.join('\n\t\tregion_state:'+t+' = {\n'+'\n'.join(bodies[t])+'\n\t\t}' for t in sorted(bodies))
        patch.append((n.start,n.end,new))
    files[PP]=encoded(ROOT/PP,edit(raw,patch))
    assert population(raw)==population(files[PP].decode('utf-8-sig'))
    # All removed COM building sections are empty. Refuse to delete assets silently.
    for p in effective('common/history/buildings'):
        raw=text(p);patch=[]
        for sid,s in state_nodes(raw).items():
            if sid not in SCOPE or (sid,'COM') in by:continue
            for n in s.children('region_state:COM'):
                assert not n.children(),'Nonempty building history needs explicit relocation: '+str(p)
                patch.append((n.start,n.end,''))
        if patch:
            assert p.is_relative_to(ROOT),'Would modify vanilla; create a reviewed mod override first.'
            files[p.relative_to(ROOT).as_posix()]=encoded(p,edit(raw,patch))
    # Activate the existing Cherokee/Creek tags, correcting their removal-era capital templates.
    raw=text(ROOT/CD);patch=[];existing={}
    for p in effective('common/country_definitions'):
        for n in parse(text(p)):existing[n.key]=n
    for g in GROUPS[:2]:
        n=next(n for n in parse(raw) if n.key==g[0])
        changes=[(v.start,v.end,'country_type = decentralized') for v in n.children('country_type')]
        changes += [(v.start,v.end,'capital = '+g[4]) for v in n.children('capital')]
        changes += [(n.end-1,n.end-1,'\n\treligion = animist\n')]
        patch.extend(changes)
    files[CD]=encoded(ROOT/CD,edit(raw,patch))
    defs=[];hist=['COUNTRIES = {'];flags=[];coas=[];loc={'french':['l_french:'],'english':['l_english:']}
    for i,g in enumerate(GROUPS):
        t,fr,en,cu,cap,color=g;assert (cap,t) in by
        if i>=2:
            assert t not in existing,t+' collides with an effective definition'
            defs.append(f'{t} = {{ color = {{ {" ".join(map(str,color))} }} country_type = decentralized tier = principality cultures = {{ {cu} }} religion = animist capital = {cap} }}')
            flags.append(f'{t} = {{ flag_definition = {{ coa = aor1776_r8_{t.lower()} priority = 100 allow_overlord_canton = no }} }}')
            coas.append(f'aor1776_r8_{t.lower()} = {{ pattern = "pattern_solid.tga" color1 = "'+['green','blue','brown','yellow','green','purple','red','blue'][i]+'" colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 0.8 0.8 } } } }')
        hist.append(' c:'+t+' ?= {\n  # Regional agricultural knowledge; no European tier copied.\n  add_technology_researched = traditional_food_processing\n'+''.join('  activate_law = law_type:law_'+law+'\n' for law in NATIVE_LAWS)+'  effect_native_conscription_10 = yes\n }')
        for lang,name in [('french',fr),('english',en)]:loc[lang]+=[f' {t}:0 "{name}"',f' {t}_ADJ:0 "{name}"']
    hist.append('}')
    for folder,lines in [('country_definitions',defs),('history/countries',hist),('flag_definitions',flags),('coat_of_arms/coat_of_arms',coas)]:
        files[f'common/{folder}/{PREFIX}.txt']=('\n'.join(lines)+'\n').encode('utf8')
    for lang,lines in loc.items():files[f'localization/{lang}/{PREFIX}_l_{lang}.yml']=b'\xef\xbb\xbf'+('\n'.join(lines)+'\n').encode('utf8')
    for rel,data in files.items():
        if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
        path=OUT/'patch'/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    dump('PATCH.json',dict(input_sha256={r:before.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files},bitmap_sha256=sha(ROOT/'map_data/provinces.png')))
    dump('PLAN.json',dict(date='2026-10-26',status='PREPARED',transfers=len(changed),groups=GROUPS,allocation=allocations,rows=rows,remaining_comanche=C.Counter(r['State_ID'] for r in rows if r['After']=='COM')))
    with (OUT/'PROVINCE_TRANSFERS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    assert runtime()==before,'Concurrent runtime change during preparation.'
    print(json.dumps(dict(transfers=len(changed),by_state={s:dict(C.Counter(r['After'] for r in rows if r['State_ID']==s)) for s in sorted(SCOPE)},files=len(files))))


def apply():
    assert not (OUT/'APPLIED.json').exists()
    p=load(OUT/'PATCH.json');assert sha(ROOT/'map_data/provinces.png')==p['bitmap_sha256']
    for rel,digest in p['input_sha256'].items():
        target=ROOT/rel;assert (sha(target) if target.exists() else None)==digest,rel+' changed; reprepare'
        assert sha(OUT/'patch'/rel)==p['output_sha256'][rel]
    for rel in p['input_sha256']:
        target=ROOT/rel
        if target.exists():
            old=OUT/'before'/rel;old.parent.mkdir(parents=True,exist_ok=True);old.write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((OUT/'patch'/rel).read_bytes())
    dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',date='2026-10-26',files=list(p['input_sha256']),engine_tested=False))
    print('Installed bounded patch; run --validate.')


def validate():
    patch=load(OUT/'PATCH.json');plan=load(OUT/'PLAN.json');old=load(OUT/'BASELINE_OWNERS.json');own=ownership();checks={}
    checks['installed_hashes']=all(sha(ROOT/r)==d for r,d in patch['output_sha256'].items())
    targets={r['RGB']:r for r in plan['rows'] if r['After']!='COM'}
    checks['every_transfer_owner_verified']=all(own.get(r)=={(v['State_ID'],v['After'])} for r,v in targets.items())
    checks['no_ownership_change_outside_manifest']=all(own.get(r)==set(map(tuple,v)) for r,v in old.items() if r not in targets) and set(own)==set(old)
    checks['no_new_double_or_unowned_province']=all(len(own[r])==1 for r in targets)
    checks['no_comanche_in_alabama_mississippi_tennessee_arkansas']=not any(t=='COM' and s in {'STATE_ALABAMA','STATE_MISSISSIPPI','STATE_TENNESSEE','STATE_ARKANSAS'} for v in own.values() for s,t in v)
    before=text(OUT/'before'/PP);after=text(ROOT/PP)
    checks['every_state_cohort_type_culture_religion_and_total_preserved']=population(before)==population(after)
    checks['all_redistributed_pops_have_owned_state']=all(any((s.key[2:],rs.key.split(':')[1]) in v for v in own.values()) for s in state_nodes(after).values() if s.key[2:] in SCOPE for rs in s.children() if rs.key.startswith('region_state:') and rs.children('create_pop'))
    checks['all_building_commands_preserved']=True
    for rel in patch['input_sha256']:
        if '/buildings/' in rel:
            def commands(raw):return [normalized([n]) for n in walk(parse(raw)) if n.key=='create_building']
            checks['all_building_commands_preserved'] &= commands(text(OUT/'before'/rel))==commands(text(ROOT/rel))
    before_runtime=load(OUT/'BASELINE_RUNTIME.json');now=runtime()
    differences=[r for r in before_runtime.keys()|now.keys() if before_runtime.get(r)!=now.get(r)]
    unexpected=[r for r in differences if r not in patch['input_sha256']]
    checks['only_authorized_runtime_files_changed']=not unexpected
    checks['bitmap_terrain_hubs_unchanged']=all(now.get(r)==d for r,d in before_runtime.items() if r.startswith(('map_data/','gfx/map/')))
    hbc_checks=conservation(load(OUT/'BASELINE_HBC.json'),economic_inventory());checks.update({'hbc_'+k:v for k,v in hbc_checks.items()})
    witness=load(OUT.parent/'HBC-04/PIXEL_PATH_WITNESS.json');labels=[next(iter(own[r['rgb']]))[1] for r in witness]
    checks['hbc_quebec_usa_land_witness_preserved']=list(dict.fromkeys(labels))==['HBC','QUE','USA']
    checks['quebec_provinces_and_population_protected']=sum(any(t=='QUE' for s,t in v) for v in own.values())==323 and all(normalized([n])==normalized([state_nodes(before)[s].children('region_state:QUE')[i]]) for s,nodes in state_nodes(after).items() for i,n in enumerate(nodes.children('region_state:QUE')))
    definitions={n.key:n for p in effective('common/country_definitions') for n in parse(text(p))}
    checks['capitals_exist_under_country']=all(any((g[4],g[0]) in v for v in own.values()) and scalar(definitions[g[0]].one('capital'))==g[4] for g in GROUPS)
    checks['decentralized_country_definitions']=all(scalar(definitions[g[0]].one('country_type'))=='decentralized' for g in GROUPS)
    checks['localizations_bom_and_both_languages']=all((ROOT/f'localization/{lang}/{PREFIX}_l_{lang}.yml').read_bytes().startswith(b'\xef\xbb\xbf') and all('\n '+g[0]+':0 ' in text(ROOT/f'localization/{lang}/{PREFIX}_l_{lang}.yml') for g in GROUPS) for lang in ['french','english'])
    a=bitmap();selected=np.array([int(r[1:],16) for r in targets],dtype=np.uint32)
    checks['all_changed_rgb_exist_in_bitmap']=set(map(int,np.unique(a[np.isin(a,selected)])))==set(map(int,selected))
    regions={n.key:set(provs(n,'provinces')) for p in effective('map_data/state_regions') for n in parse(text(p))}
    checks['all_changed_rgb_match_state_definition']=all(r in regions[v['State_ID']] for r,v in targets.items())
    # Record regional connectivity; islands and hunting-ground fragments require review, not silent bridging.
    allcells={int(r[1:],16) for r in targets}|{int(r['RGB'][1:],16) for r in plan['rows']}
    adj=graph(a,np.asarray(sorted(allcells),dtype=np.uint32));conn={}
    for g in GROUPS:
        cells={int(r[1:],16) for r,v in own.items() if any(t==g[0] for s,t in v)}
        conn[g[0]]=[len(c) for c in components(adj,cells)]
    dump('CONNECTIVITY.json',conn)
    checks['no_isolated_new_native_country']=all(v and len(v)==1 for v in conn.values())
    haw={t:sum((s,t) in v for v in own.values()) for t in ['HAW','HMA','HWA'] for s in ['STATE_HAWAIIAN_ISLANDS']}
    checks['hawaii_three_existing_countries_untouched']=all(haw.values()) and all(own[r]==set(map(tuple,v)) for r,v in old.items() if any(s=='STATE_HAWAIIAN_ISLANDS' for s,t in v))
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),unexpected_runtime_changes=unexpected,connectivity=conn,hawaii=haw,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False,human_validated=False))
    render(old,own)
    print(json.dumps(dict(checks=checks,connectivity=conn),ensure_ascii=False,indent=2))
    return all(checks.values())


def render(old,own):
    a=bitmap()[1140:1470,1780:2270];edge=np.zeros(a.shape,bool);edge[1:]|=a[1:]!=a[:-1];edge[:,1:]|=a[:,1:]!=a[:,:-1]
    for label,data in [('BEFORE',old),('AFTER',own)]:
        pic=np.full((*a.shape,3),[37,48,58],dtype=np.uint8)
        present={int(v) for v in np.unique(a)}
        grouped=C.defaultdict(list)
        for r,v in data.items():
            value=int(r[1:],16)
            if value in present:grouped[next(iter(v))[1]].append(value)
        for t,values in grouped.items():pic[np.isin(a,values)]=COLORS.get(t,[101,114,105])
        pic[edge&np.any(pic!=[37,48,58],axis=2)]=[42,47,45]
        crop=Image.fromarray(pic).resize((1470,990),Image.Resampling.NEAREST)
        sheet=Image.new('RGB',(1470,1160),'#25303a');sheet.paste(crop,(0,130));d=ImageDraw.Draw(sheet)
        font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
        d.text((12,8),'1776 — '+('Avant correction' if label=='BEFORE' else 'Corrections installées ; fronts régionaux approximatifs'),font=font,fill='white')
        x=12;y=45
        for tag,col in COLORS.items():
            if x>1300:x=12;y+=35
            d.rectangle((x,y,x+17,y+17),fill=tuple(col));d.text((x+23,y-3),tag,font=font,fill='white');x+=132
        d.text((12,1127),'Limites de provinces conservées. Gris : autres pays. Plusieurs fronts coloniaux et autochtones restent à reprendre.',font=font,fill='white')
        sheet.save(OUT/f'{label}.png')


if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--validate' in sys.argv:sys.exit(0 if validate() else 1)
    else:raise SystemExit('Use --prepare, --apply or --validate')
