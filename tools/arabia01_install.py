"""ARABIA-01: guarded, bounded installation and independent current-file audit.

No Git writes, vanilla writes, bitmap changes, or global baseline restoration.
"""
import collections as C, json, re, sys
from pathlib import Path
from arabia01 import ROOT, GAME, OUT, ST, PP, SCOPE, dump, load, preview
from audit_hbc_1776 import effective, provs, sha, runtime
from hbc06_integrate import text, state_nodes, ownership, encoded, edit, rgb_block
from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized

BP=['common/history/buildings/08_middle_east.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']
TAGS=['NEJ','NBB','A91','A92','BHN','ZAI','HDJ']
PROFILE=['improved_husbandry','international_relations','organized_textile_production',
         'regulated_small_arms','organized_military_establishments','traditional_food_processing']
LAWS=['monarchy','autocracy','state_religion','hereditary_bureaucrats','no_police',
      'peasant_levies','traditionalism','land_based_taxation','mercantilism','serfdom',
      'no_schools','no_health_system','no_workers_rights','migration_controls','slave_trade',
      'legal_guardianship','child_labor_allowed','outlawed_dissent']

def compact(n): return json.dumps(normalized([n]),ensure_ascii=False,sort_keys=True)
def rgbkey(r): return 'x'+r[1:].upper()
def owners():
    d=C.defaultdict(set)
    for r,vs in ownership().items():d[rgbkey(r)].update(vs)
    return d
def popstock(raw,owner=False):
    d=C.Counter()
    for sid,s in state_nodes(raw).items():
        for rs in s.children():
            for p in rs.children('create_pop'):
                sig=tuple((n.key,str(n.value)) for n in p.children() if n.key!='size')
                d[(sid,rs.key if owner else '',sig)]+=int(p.one('size'))
    return d
def stock_rows(d):return [dict(key=list(k),amount=v) for k,v in sorted(d.items())]
def buildingstock(raw):
    d=C.Counter()
    for sid,s in state_nodes(raw).items():
        for rs in s.children():
            for b in rs.children('create_building'):
                # Sum ownership levels within each declaration, not every nested levels field twice.
                levels=sum(int(n.value) for own in b.children('add_ownership') for n in walk(own.children()) if n.key=='levels')
                if not levels:levels=int(b.one('level',b.one('levels','1')))
                d[(sid,scalar(b.one('building')))]+=levels
    return d
def counterjson(d):return {'|'.join(k):v for k,v in sorted(d.items())}
def renamed(raw,old,new):return raw.replace('region_state:'+old,'region_state:'+new).replace('c:'+old,'c:'+new)
def inside(raw,node):return raw[raw.index('{',node.start)+1:node.end-1]
def popsplit(raw,node,alloc):
    ps=node.children('create_pop');total=[sum(v[i] for v in alloc.values()) for i in range(len(ps))]
    assert total==[int(p.one('size')) for p in ps]
    rows=[];ledger=[]
    for tag,amounts in alloc.items():
        bodies=[]
        for p,n in zip(ps,amounts):
            if not n:continue
            body=raw[p.start:p.end];size=p.children('size')[0]
            body=body[:size.start-p.start]+'size = '+str(n)+body[size.end-p.start:]
            bodies.append(body)
        rows.append('region_state:'+tag+' = {\n'+ '\n'.join(bodies)+'\n\t\t}')
        ledger.append(dict(owner=tag,total=sum(amounts),cohort_sizes=amounts))
    return '\n\t\t'.join(rows),ledger

def tech_audit(name):
    from validate_starting_technology_1776 import collect_snapshot,audit_country
    s=collect_snapshot();exp={t:dict(historical_evidence='SOURCES.md and REPORT.md: inherited capabilities checked separately from historical certainty; no industrial tier.') for t in TAGS}
    results=[audit_country(t,s,exp[t]) for t in TAGS]
    dump(name,results)
    return results

def prepare():
    assert not (OUT/'APPLIED.json').exists(),'Already installed; audit instead.'
    plan=load('PLAN.json');ow=owners();files={};before=runtime();hashes={};ledger=[]
    # No hidden stale baseline: collect current hashes and snapshots immediately before preparation.
    for z in plan['transfers']:assert ow[z['rgb']]=={(z['state'],z['before'])},z
    existing={n.key for p in effective('common/country_definitions') for n in parse(text(p))}
    assert not {'A91','A92'}&existing
    raw=text(ROOT/ST);patch=[];ns=state_nodes(raw)
    for sid in sorted({z['state'] for z in plan['transfers']}):
        s=ns[sid];by=C.defaultdict(set);original={}
        for n in s.children('create_state'):
            t=scalar(n.one('country'))[2:];by[t]|=set(provs(n,'owned_provinces'));original[t]=n
        for z in plan['transfers']:
            if z['state']==sid:by[z['before']].remove(z['rgb']);by[z['after']].add(z['rgb'])
        for t,n in original.items():
            if not by[t]:patch.append((n.start,n.end,''))
            elif set(provs(n,'owned_provinces'))!=by[t]:
                p=n.children('owned_provinces')[0];patch.append((p.start,p.end,'owned_provinces = '+rgb_block(by[t])))
        added=''.join('\n\t\tcreate_state = {\n\t\t\tcountry = c:'+t+'\n\t\t\towned_provinces = '+rgb_block(by[t])+'\n\t\t}\n' for t in sorted(by) if t not in original and by[t])
        if added:patch.append((s.end-1,s.end-1,added))
    files[ST]=encoded(ROOT/ST,edit(raw,patch))
    raw=text(ROOT/PP);ns=state_nodes(raw);patch=[]
    n=ns['STATE_NEJD'].children('region_state:NBB')[0]
    body,led=popsplit(raw,n,{'NEJ':[50000,0,3000],'A91':[10000,18700,1000],'NBB':[19896,0,1951]})
    patch.append((n.start,n.end,body));ledger.append(dict(state='STATE_NEJD',policy='Redistribution of inherited stock; NOT a historical census or pixel-derived estimate.',allocations=led))
    n=ns['STATE_HAIL'].children('region_state:NBB')[0];patch.append((n.start,n.end,renamed(raw[n.start:n.end],'NBB','A91')))
    n=ns['STATE_ABU_DHABI'].children('region_state:BHN')[0]
    body,led=popsplit(raw,n,{'BHN':[10199,0,4420,1000,0],'A92':[0,7989,0,1066,231]})
    patch.append((n.start,n.end,body));ledger.append(dict(state='STATE_ABU_DHABI',policy='Redistribution of inherited stock; minority categories retained, not certified as a local 1776 census.',allocations=led))
    src=ns['STATE_YEMEN'].children('region_state:HDJ')[0];dst=ns['STATE_YEMEN'].children('region_state:ZAI')[0]
    patch.extend([(src.start,src.end,''),(dst.end-1,dst.end-1,'\n'+inside(raw,src)+'\n\t\t')])
    files[PP]=encoded(ROOT/PP,edit(raw,patch));assert popstock(raw)==popstock(files[PP].decode('utf-8-sig'))
    dump('POP_REDISTRIBUTION_LEDGER.json',ledger)
    # Existing civil buildings are moved, not recreated. Duplicate world declarations stay aligned.
    for rel in BP:
        raw=text(ROOT/rel);ns=state_nodes(raw);patch=[]
        for sid,old,new in [('STATE_NEJD','NBB','NEJ'),('STATE_HAIL','NBB','A91')]:
            if sid not in ns:continue
            for n in ns[sid].children('region_state:'+old):patch.append((n.start,n.end,renamed(raw[n.start:n.end],old,new)))
        if 'STATE_ABU_DHABI' in ns:
            for n in ns['STATE_ABU_DHABI'].children('region_state:BHN'):
                fs=[b for b in n.children('create_building') if scalar(b.one('building'))=='building_fishing_wharf']
                for b in fs:patch.append((b.start,b.end,''))
                if fs:patch.append((ns['STATE_ABU_DHABI'].end-1,ns['STATE_ABU_DHABI'].end-1,'\n region_state:A92 = {\n'+'\n'.join(renamed(raw[b.start:b.end],'BHN','A92') for b in fs)+'\n }\n'))
        if 'STATE_YEMEN' in ns:
            s=ns['STATE_YEMEN'];src=s.children('region_state:HDJ');dst=s.children('region_state:ZAI')
            if src:
                assert len(src)==len(dst)==1
                src,dst=src[0],dst[0];moved=[]
                for b in src.children('create_building'):
                    kind=scalar(b.one('building'));same=[z for z in dst.children('create_building') if scalar(z.one('building'))==kind]
                    if same:
                        assert kind=='building_coffee_plantation' and len(same)==1
                        old=same[0];assert provs(b,'activate_production_methods')==provs(old,'activate_production_methods')
                        ls=[z for z in walk(old.children()) if z.key=='levels'];assert len(ls)==1
                        extra=sum(int(z.value) for z in walk(b.children()) if z.key=='levels')
                        z=ls[0];patch.append((z.start,z.end,'levels='+str(int(z.value)+extra)))
                    else:moved.append(renamed(raw[b.start:b.end],'HDJ','ZAI'))
                patch.append((src.start,src.end,''))
                if moved:patch.append((dst.end-1,dst.end-1,'\n'+'\n'.join(moved)+'\n'))
        new=edit(raw,patch);assert buildingstock(raw)==buildingstock(new),rel
        files[rel]=encoded(ROOT/rel,new)
    # Local capability profiles: a Sunni oasis/coastal emirate and a decentralised aggregate.
    files['common/country_definitions/1776_arabia01.txt']=('''# ARABIA-01. A92 is a collective representation, not an Al Thani state.
A91 = { color = { 189 154 83 } country_type = unrecognized tier = principality cultures = { bedouin } religion = sunni capital = STATE_NEJD }
A92 = { color = { 172 117 140 } country_type = decentralized tier = principality cultures = { bedouin } religion = sunni capital = STATE_ABU_DHABI }
''').encode()
    hist='COUNTRIES = {\n'
    for tag in ['A91','A92']:
        tech=PROFILE if tag=='A91' else ['improved_husbandry','international_relations','organized_textile_production','traditional_food_processing','organized_military_establishments']
        laws=LAWS if tag=='A91' else [v for v in LAWS if v not in ['monarchy','autocracy']]+['chiefdom','elder_council']
        hist+=' c:'+tag+' ?= {\n'+''.join('  add_technology_researched = '+t+'\n' for t in tech)+''.join('  activate_law = law_type:law_'+l+'\n' for l in laws)+' }\n'
    hist+='}\n';files['common/history/countries/1776_arabia01.txt']=hist.encode()
    files['common/history/diplomacy/1776_arabia01.txt']=('''# Persian governorate represented by the existing puppet relation, not an 1783 Khalifa state.
DIPLOMACY = { c:PER ?= { create_diplomatic_pact = { country = c:BHN type = puppet } } }
''').encode()
    files['common/history/characters/nej - nejd.txt']=('''# Overrides the vanilla 1836 Faisal/Saud templates only for the reactivated NEJ.
CHARACTERS = { c:NEJ ?= { create_character = {
 first_name = aor1776_abdulaziz_bin_muhammad_bin_saud
 last_name = aor1776_arabia_empty_name
 historical = yes ruler = yes age = 55 culture = cu:bedouin religion = rel:sunni
 interest_group = ig_devout ideology = ideology_traditionalist
} } }
''').encode()
    # Decorative banners: no claim these are attested 1776 national flags.
    files['common/flag_definitions/1776_arabia01.txt']='\n'.join(t+' = { flag_definition = { coa = aor1776_arabia_'+t.lower()+' priority = 100 allow_overlord_canton = no } }' for t in ['NEJ','A91','A92']).encode()
    files['common/coat_of_arms/coat_of_arms/1776_arabia01.txt']='\n'.join('aor1776_arabia_'+t.lower()+' = { pattern = "pattern_solid.tga" color1 = "'+col+'" }' for t,col in [('NEJ','green'),('A91','brown'),('A92','red')]).encode()
    # Maritime access is an engine test, not certified by the presence of a port.
    port=lambda s,t:' s:'+s+' = { region_state:'+t+' = { create_building = { building = "building_port" add_ownership = { country = { country = "c:'+t+'" levels = 1 } } reserves = 1 activate_production_methods = { "pm_aor1776_traditional_commercial_harbor" "pm_1776_no_raw_data_reporting" } } } }\n'
    files['common/history/buildings/1776_arabia01.txt']=('BUILDINGS = {\n'+port('STATE_HAIL','A91')+port('STATE_ABU_DHABI','BHN')+'}\n').encode()
    # Units initialize their recruitment buildings natively. Avoid duplicate explicit barracks.
    files['common/history/military_formations/1776_arabia01.txt']=('MILITARY_FORMATIONS = {\n'+''.join(' c:'+t+' ?= { create_military_formation = { type = army hq_region = sr:region_arabia name = aor1776_arabia_'+t.lower()+'_levies combat_unit = { type = unit_type:combat_unit_type_irregular_infantry service_type = conscript state_region = s:STATE_NEJD count = 1 } } }\n' for t in ['NEJ','A91'])+'}\n').encode()
    for lang in ['french','english']:
        fr=lang=='french';names={'NEJ':('Émirat de Diriyah','Emirate of Diriyah'),'NEJ_ADJ':('de Diriyah','Diriyah'),'A91':('Banu Khalid','Banu Khalid'),'A91_ADJ':('khalidi','Khalidi'),'A92':('Communautés du Qatar','Qatari communities'),'A92_ADJ':('qatari','Qatari'),'aor1776_abdulaziz_bin_muhammad_bin_saud':('Abdulaziz ben Muhammad ben Saoud','Abdulaziz bin Muhammad bin Saud'),'aor1776_arabia_empty_name':('',''),'aor1776_arabia_nej_levies':('Levée de Diriyah','Diriyah levy'),'aor1776_arabia_a91_levies':('Levée des Banu Khalid','Banu Khalid levy')}
        files['localization/'+lang+'/replace/1776_arabia01_l_'+lang+'.yml']=b'\xef\xbb\xbf'+('l_'+lang+':\n'+''.join(' '+k+':0 "'+v[0 if fr else 1]+'"\n' for k,v in names.items())).encode('utf8')
    # Disable capital-derived naming for NEJ only. Preserve the country definition otherwise.
    rel='common/country_definitions/00_countries.txt';raw=text(ROOT/rel);nej=next(n for n in parse(raw) if n.key=='NEJ');n=nej.children('is_named_from_capital')
    if n:
        z=n[0];files[rel]=encoded(ROOT/rel,edit(raw,[(z.start,z.end,'is_named_from_capital = no')]))
    # Prepare all files before any runtime mutation; record exact current preimages.
    stage=OUT/'staged';pre=OUT/'preimages';manifest=[]
    for rel,data in files.items():
        p=ROOT/rel;old=p.read_bytes() if p.exists() else None
        if old==data:continue
        if not rel.endswith('.yml'):parse(data.decode('utf-8-sig'))
        q=stage/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
        if old is not None:
            q=pre/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
        manifest.append(dict(file=rel,before_sha256=sha(p) if p.exists() else None,after_sha256=sha(stage/rel)))
    dump('PREPARED.json',dict(files=manifest,world_before=before,ownership_before={r:sorted(v) for r,v in ow.items()},scope=SCOPE))
    print(json.dumps({'prepared_files':len(manifest),'transfers':len(plan['transfers']),'population_stock_conserved':True,'existing_civil_buildings_conserved':True}))

def apply():
    assert not (OUT/'APPLIED.json').exists()
    m=load('PREPARED.json')
    for z in m['files']:
        p=ROOT/z['file'];assert (sha(p) if p.exists() else None)==z['before_sha256'],('Concurrent change; reprepare first',z['file'])
        assert sha(OUT/'staged'/z['file'])==z['after_sha256']
    tech_audit('TECH_BEFORE.json')
    # Recheck after the read-only audit in case another worker changed a shared file.
    for z in m['files']:
        p=ROOT/z['file'];assert (sha(p) if p.exists() else None)==z['before_sha256'],z['file']
    for z in m['files']:
        p=ROOT/z['file'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((OUT/'staged'/z['file']).read_bytes())
    dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files=m['files'],transfers=len(load('PLAN.json')['transfers']),human_validated=False,game_launched=False))
    print('Installed guarded ARABIA-01; runtime validation pending.')

def repair_profiles():
    """Repair only findings introduced by activation, without gifting later banking/propaganda techs."""
    m=load('APPLIED.json');changes={}
    rel='common/history/countries/1776_arabia01.txt';s=text(ROOT/rel)
    s=s.replace('law_legal_guardianship','law_no_womens_rights').replace('law_outlawed_dissent','law_right_of_assembly').replace('law_mercantilism','law_aor1776_arabia_customs')
    changes[rel]=s.encode()
    rel='common/history/countries/nej - nejd.txt'
    laws=[x.replace('mercantilism','aor1776_arabia_customs').replace('legal_guardianship','no_womens_rights').replace('outlawed_dissent','right_of_assembly') for x in LAWS]+['subjecthood','guild_system']
    changes[rel]=('COUNTRIES = { c:NEJ ?= {\n # Explicit 1776 profile; no generic macro introducing later commercial institutions.\n'+''.join(' add_technology_researched = '+t+'\n' for t in ['distillation']+PROFILE)+''.join(' activate_law = law_type:law_'+l+'\n' for l in laws)+'} }\n').encode()
    changes['common/laws/1776_arabia01.txt']=('''# Early caravan/harbour customs represented by a bounded mercantilism variant.
# No commercial insurance markets are asserted for these polities in 1776.
law_aor1776_arabia_customs = {
 group = lawgroup_trade_policy parent = law_mercantilism
 icon = "gfx/interface/icons/law_icons/mercantilism.dds" progressiveness = 0
 unlocking_technologies = { international_relations }
 is_visible = { OR = { c:NEJ ?= this c:A91 ?= this c:A92 ?= this } }
 can_enact = { OR = { c:NEJ ?= this c:A91 ?= this c:A92 ?= this } }
 modifier = {
  state_tariff_import_add = 0.50 state_tariff_export_add = 0.20
  state_subvention_export_add = 0.50 state_subvention_import_add = 0.20
  state_import_advantage_mult = -0.25 state_export_advantage_mult = 0.25
 }
}
''').encode()
    for lang in ['french','english']:
        rel='localization/'+lang+'/replace/1776_arabia01_l_'+lang+'.yml';raw=text(ROOT/rel)
        names=('Droits de douane traditionnels','Prélèvements sur les échanges caravaniers et portuaires, représentés par une variante du mercantilisme.') if lang=='french' else ('Traditional customs duties','Duties on caravan and harbour trade, represented by a mercantilism variant.')
        raw+=' law_aor1776_arabia_customs:0 "'+names[0]+'"\n law_aor1776_arabia_customs_desc:0 "'+names[1]+'"\n';changes[rel]=b'\xef\xbb\xbf'+raw.encode()
    # Keep first installation records and add an append-only repair receipt.
    repair=[]
    for rel,data in changes.items():
        p=ROOT/rel;old=p.read_bytes() if p.exists() else None;before=sha(p) if p.exists() else None
        known=next((z for z in m['files'] if z['file']==rel),None)
        if known:assert known['after_sha256']==before,('Concurrent edit',rel)
        elif old is not None:
            q=OUT/'preimages'/rel;q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();q.write_bytes(old)
        if p.suffix=='.txt':parse(data.decode('utf-8-sig'))
        q=OUT/'profile_repair_preimages'/rel
        if old is not None:q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        repair.append(dict(file=rel,before_sha256=before,after_sha256=sha(p)))
        if known:known['after_sha256']=sha(p)
        else:m['files'].append(dict(file=rel,before_sha256=before,after_sha256=sha(p)))
    dump('PROFILE_REPAIR.json',dict(reason='Fix invalid law ID and later-tech law requests introduced by the activated/new profiles. Preserve inherited countries outside activation.',files=repair))
    dump('APPLIED.json',m)
    print('Bounded profile repair installed.')

def finish_formatting():
    m=load('APPLIED.json');receipt=[]
    for rel in [ST,PP]+BP:
        z=next(z for z in m['files'] if z['file']==rel);p=ROOT/rel
        assert sha(p)==z['after_sha256'],('Concurrent edit',rel)
        raw=text(p);patch=[]
        for sid,n in state_nodes(raw).items():
            if sid in SCOPE:
                a=raw[n.start:n.end];b=re.sub(r'(?m)[\t ]+(?=\r?$)','',a)
                if a!=b:patch.append((n.start,n.end,b))
        if patch:
            before=sha(p);p.write_bytes(encoded(p,edit(raw,patch)))
            receipt.append(dict(file=rel,before_sha256=before,after_sha256=sha(p)));z['after_sha256']=sha(p)
    dump('FORMATTING_FINISH.json',receipt);dump('APPLIED.json',m)
    print('Scoped trailing whitespace cleaned; outside regions untouched.')

def audit():
    m=load('PREPARED.json');before={r:set(map(tuple,v)) for r,v in m['ownership_before'].items()};after=owners();expected={z['rgb']:{(z['state'],z['after'])} for z in load('PLAN.json')['transfers']}
    changed={r for r in set(before)|set(after) if before.get(r)!=after.get(r)}
    checks={'exact_planned_ownership_changes':changed==set(expected),'planned_owners_correct':all(after.get(r)==v for r,v in expected.items()),'no_new_duplicate_or_unowned_assignment':all(len(after[r])==1 for r in expected)}
    raw=text(ROOT/PP);old=text(OUT/'preimages'/PP);checks['all_pop_cohort_stocks_conserved']=popstock(raw)==popstock(old)
    for rel in BP:checks['civil_buildings_preserved_'+Path(rel).name]=buildingstock(text(ROOT/rel))==buildingstock(text(OUT/'preimages'/rel))
    checks['new_capitals_owned']=all(any(t==tag and sid==cap for vs in after.values() for sid,t in vs) for tag,cap in [('NEJ','STATE_NEJD'),('A91','STATE_NEJD'),('A92','STATE_ABU_DHABI')])
    checks['bitmap_unchanged']=sha(ROOT/'map_data/provinces.png')==m['world_before']['map_data/provinces.png']
    for z in load('APPLIED.json')['files']:
        p=ROOT/z['file'];checks['installed_hash_'+z['file']]=sha(p)==z['after_sha256']
        if p.suffix=='.txt':parse(text(p))
    # Independence from RGB letter case; inspect every planned ID against actual region definitions.
    regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))}
    checks['all_target_rgb_in_own_region']=all(z['rgb'] in {rgbkey(r) for r in provs(regs[z['state']],'provinces')} for z in load('PLAN.json')['transfers'])
    checks['no_target_impassable']=all(z['rgb'] not in {rgbkey(r) for r in provs(regs[z['state']],'impassable')} for z in load('PLAN.json')['transfers'])
    scope_rgb={rgbkey(r) for sid in SCOPE for r in provs(regs[sid],'provinces')}
    checks['all_scope_provinces_owned_once']=all(len(after.get(r,set()))==1 for r in scope_rgb)
    # Compare every non-scoped syntax node, not only aggregate totals.
    def outside(raw):
        result=[]
        for root in parse(raw):
            if isinstance(root.value,list):
                result.append((root.key,[(n.key,compact(n)) for n in root.children() if n.key not in {'s:'+s for s in SCOPE}]))
            else:result.append((root.key,compact(root)))
        return result
    for rel in [ST,PP]+BP:checks['outside_scope_nodes_unchanged_'+rel]=outside(text(ROOT/rel))==outside(text(OUT/'preimages'/rel))
    # Side-edge connection of the actual selected provinces, no diagonal-only links.
    from arabia01 import raster
    from hbc02_map_candidates import graph
    import numpy as np
    a=raster()
    for tag in ['NEJ','A91','A92']:
        rs={int(r[1:],16) for r,vs in after.items() if any(t==tag for sid,t in vs)};adj=graph(a,np.array(sorted(rs),np.uint32));seen={next(iter(rs))};q=list(seen)
        while q:
            u=q.pop()
            for v,border in adj[u].items():
                if v in rs and border>=2 and v not in seen:seen.add(v);q.append(v)
        checks['land_connected_'+tag]=seen==rs
    from validate_starting_technology_1776 import collect_snapshot,audit_country
    snap=collect_snapshot();results=[]
    for t in TAGS:
        e=dict(historical_evidence='SOURCES.md and REPORT.md: source-specific local profile, conservative inherited recipe compatibility, no industrial tier.')
        if t in ['NEJ','A91','A92']:e['allowed']=PROFILE+['distillation']
        results.append(audit_country(t,snap,e))
    dump('TECH_AFTER.json',results)
    checks['strategic_region_exists']=any(n.key=='region_arabia' for p in effective('common/strategic_regions') for n in parse(text(p)))
    delta=[];prior={z['TAG']:z for z in load('TECH_BEFORE.json')}
    for z in results:
        pf={json.dumps(f,sort_keys=True) for f in prior[z['TAG']]['findings'] if f['code']!='UNKNOWN_OR_INACTIVE_TAG'}
        new=[f for f in z['findings'] if json.dumps(f,sort_keys=True) not in pf]
        delta.append(dict(tag=z['TAG'],status=z['status'],new_findings=new))
    checks['new_and_reactivated_profiles_pass']=all(z['status']=='PASS_STATIC_ONLY' for z in results if z['TAG'] in ['NEJ','A91','A92'])
    checks['no_new_other_country_tech_findings']=all(not z['new_findings'] for z in delta if z['tag'] not in ['NEJ','A91','A92'])
    # All custom localization keys unique within their mod language, referenced laws exist.
    loc_report=[]
    for lang in ['french','english']:
        p=ROOT/'localization'/lang/'replace'/('1776_arabia01_l_'+lang+'.yml');content=text(p)
        keys=re.findall(r'^\s*([A-Za-z0-9_]+):(?:\d+)?\s+"',content,re.M);counts=C.Counter()
        for lp in (ROOT/'localization'/lang).rglob('*.yml'):
            for k in re.findall(r'^\s*([A-Za-z0-9_]+):(?:\d+)?\s+"',text(lp),re.M):
                if k in keys:counts[k]+=1
        checks['loc_utf8_bom_'+lang]=p.read_bytes().startswith(b'\xef\xbb\xbf')
        checks['custom_loc_keys_unique_'+lang]=all(counts[k]==1 for k in keys)
        loc_report.append(dict(language=lang,key_counts=dict(counts)))
    dump('LOCALIZATION_AUDIT.json',loc_report)
    for t in ['NEJ','A91','A92']:
        known=set(snap['starts'][t]['technologies']);requests=snap['law_requests'][t]
        checks['profile_references_exist_'+t]=all(x in snap['techs'] for x in known) and all(x in snap['laws'] for x in requests)
    dump('TECH_DELTA.json',delta)
    dump('VALIDATION.json',dict(checks=checks,ownership_changes=len(changed),scope_provinces=len(scope_rgb),population_before=sum(popstock(old).values()),population_after=sum(popstock(raw).values()),technical_status='PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL_STATIC',runtime_status='NOT_TESTED',historical_boundaries='Whole-province approximations, not surveyed 1776 borders',tech_delta=delta))
    preview(after,load('SITE_PROXIES.json'),'INSTALLED_ARABIA.png')
    print(json.dumps({'checks':checks,'new_tech_findings':delta},ensure_ascii=False))
    assert all(checks.values())

if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--audit' in sys.argv:audit()
    elif '--repair-profiles' in sys.argv:repair_profiles()
    elif '--finish-formatting' in sys.argv:finish_formatting()
