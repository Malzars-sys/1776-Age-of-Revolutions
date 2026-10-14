"""Build a reviewable, narrowly scoped apply_patch from the immutable MAP-2E baseline.
Never write game files directly. Integer apportionment is a technical allocation,
not a historical census. Existing demographic attributes are copied verbatim.
"""
import collections as C, difflib, json, re
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2a_patch import state, edits, append
from map2e_work import ROOT,OUT,BASE,TARGETS

GROUPS={
 'STATE_GREATER_CAUCASUS':{'ABK':['x73A639','x40D001'],'IMR':['x011141','x801000','x85DCE4','xC9B445','xD1A8AF','xD65AC8','xD15CBD'],'TUR':['xC27075','x74A861','xC0CF80']},
 'STATE_ARMENIA':{'ARM':['x805000','xAB3AF1','xDC0812','x005000','x16A02D'],'NAK':['x30DF60','x3161E0']},
 'STATE_ELIZAVETPOL':{'GJA':['xDFB2B0','x9195D4','x80D041'],'SHK':['xB7DDE5','xEE1A87','x404F5B','x8090BF'],'KRB':['x2F7A57','x0E70E4','x747318','x809040']},
 'STATE_AZERBAIJAN':{'AZB':['x69FE0D','xD77566','xBFD159','x6EB08E','x0E8C3E','x008FBF','x0467D5'],'SRV':['x0B74ED','x493F0B','xE7B07C'],'TAL':['x007060']},
 'STATE_DAGESTAN':{'RUS':['x01D041'],'AZB':['xDA5ABE','x9F1D8F']},
 'STATE_STAVROPOL':{'RUS':['x891792']},
}
OLD={'STATE_GREATER_CAUCASUS':'GEO','STATE_ARMENIA':'PER','STATE_ELIZAVETPOL':'PER','STATE_AZERBAIJAN':'PER','STATE_DAGESTAN':'CAUC','STATE_STAVROPOL':'CAUC'}
DUP_REMOVE={'STATE_KUBAN':{'CRI':['xBCF376']},'STATE_NORTH_CAUCASUS':{'CAUC':['x019041','xDA8EF4','x83F33B','x2790A8','x56FD87','x668A47','xC05001','x23F98B']}}
NEW={
 'IMR':('STATE_GREATER_CAUCASUS','georgian','orthodox','kingdom',[181,132,57]),
 'KRB':('STATE_ELIZAVETPOL','azerbaijani','shiite','principality',[167,142,206]),
 'GJA':('STATE_ELIZAVETPOL','azerbaijani','shiite','principality',[126,175,161]),
 'SHK':('STATE_ELIZAVETPOL','azerbaijani','sunni','principality',[151,170,89]),
 'NAK':('STATE_ARMENIA','azerbaijani','shiite','principality',[169,129,69]),
 'TAL':('STATE_AZERBAIJAN','persian','shiite','principality',[180,173,77]),
 'SRV':('STATE_AZERBAIJAN','azerbaijani','sunni','principality',[196,134,83]),
}
NAMES={
 'IMR':('Kingdom of Imereti','Imeretian','Royaume d’Iméréthie','imérétien'),
 'KRB':('Khanate of Karabakh','Karabakhi','Khanat du Karabakh','karabakhi'),
 'GJA':('Khanate of Ganja','Ganjan','Khanat de Gandja','gandjien'),
 'SHK':('Khanate of Sheki','Shekian','Khanat de Chaki','chaki'),
 'NAK':('Khanate of Nakhchivan','Nakhchivani','Khanat de Nakhitchevan','nakhitchevanais'),
 'TAL':('Khanate of Talysh','Talysh','Khanat de Talysh','talysh'),
 'SRV':('Khanate of Shirvan','Shirvani','Khanat de Chirvan','chirvani'),
 'ARM':('Khanate of Erivan','Erivani','Khanat d’Erevan','érevanien'),
 'AZB':('Khanate of Quba','Quban','Khanat de Kouba','koubain'),
 'CHC':('Chechen Communities','Chechen','Communautés tchétchènes','tchétchène'),
}
STATE_NAMES={
 ('STATE_GREATER_CAUCASUS','GEO'):('Kartli-Kakheti','Kartl-Kakhétie'),
 ('STATE_GREATER_CAUCASUS','IMR'):('Imereti and Western Principalities','Iméréthie et principautés occidentales'),
 ('STATE_GREATER_CAUCASUS','ABK'):('Abkhazia','Abkhazie'),
 ('STATE_GREATER_CAUCASUS','TUR'):('Akhaltsikhe','Akhaltsikhé'),
 ('STATE_ARMENIA','ARM'):('Erivan','Erevan'),('STATE_ARMENIA','NAK'):('Nakhchivan','Nakhitchevan'),
 ('STATE_ELIZAVETPOL','KRB'):('Karabakh','Karabakh'),('STATE_ELIZAVETPOL','GJA'):('Ganja','Gandja'),('STATE_ELIZAVETPOL','SHK'):('Sheki','Chaki'),
 ('STATE_AZERBAIJAN','AZB'):('Quba, Baku and Salyan','Kouba, Bakou et Salyan'),('STATE_AZERBAIJAN','SRV'):('Shirvan','Chirvan'),('STATE_AZERBAIJAN','TAL'):('Talysh','Talysh'),
 ('STATE_DAGESTAN','AZB'):('Derbent','Derbent'),('STATE_DAGESTAN','RUS'):('Kizliar','Kizliar'),('STATE_DAGESTAN','CHC'):('Dagestani Communities','Communautés daghestanaises'),
 ('STATE_STAVROPOL','RUS'):('Mozdok','Mozdok'),('STATE_STAVROPOL','CAUC'):('Nogai Steppe','Steppe nogaïe'),('STATE_NORTH_CAUCASUS','CAUC'):('Kabardia and Central Highland Communities','Kabardie et communautés montagnardes centrales'),
}
def body_rewrite(raw,node,field,value):
    fragment=raw[node.start:node.end];v=node.children(field)[0]
    return fragment[:v.start-node.start]+field+' = '+str(value)+fragment[v.end-node.start:]
def apportion(number,weights):
    total=sum(weights.values());out={k:number*v//total for k,v in weights.items()}
    for k in sorted(weights,key=lambda k:(-(number*weights[k]%total),k))[:number-sum(out.values())]:out[k]+=1
    assert sum(out.values())==number
    return out
def transform(base):
    result=dict(base['originals']); geo=json.loads((OUT/'GEOGRAPHY_before.json').read_text(encoding='utf-8'))['provinces']
    raw=result['common/history/states/00_states.txt']; moves=[]
    for sid,groups in GROUPS.items():
        s=state(raw,sid);cr=next(n for n in s.children('create_state') if n.one('country')=='c:'+OLD[sid]);ps=cr.children('owned_provinces')[0]
        oldprovs=[cw.scalar(v.value) for v in ps.children()];newprovs={v for vv in groups.values() for v in vv}; assert newprovs<=set(oldprovs)
        kept=[v for v in oldprovs if v not in newprovs]
        new=''
        if kept:new='create_state = { country = c:'+OLD[sid]+' owned_provinces = { '+' '.join(kept)+' } state_type = '+cw.scalar(cr.one('state_type','unincorporated'))+' }'
        for tag,vs in groups.items():
            new+='\n\t\t# MAP-2E: whole-RGB historical/gameplay approximation; see decision manifest.\n\t\tcreate_state = { country = c:'+tag+' owned_provinces = { '+' '.join(vs)+' } state_type = '+('incorporated' if tag in ('GEO','IMR','ABK','ARM','NAK','AZB','GJA','SHK','KRB','SRV','TAL') else 'unincorporated')+' }'
            for v in vs:moves.append([v,sid,OLD[sid],tag,'DOCUMENTED_GAMEPLAY_APPROXIMATION',geo[v]['pixels'],*geo[v]['bbox']])
        raw=edits(raw,[(cr.start,cr.end,new)])
    for sid,tags in DUP_REMOVE.items():
        for tag,vs in tags.items():
            cr=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+tag);ps=cr.children('owned_provinces')[0];frag=raw[ps.start:ps.end]
            for v in vs:
                frag=frag.replace(v,'');winner=next(t for t in geo[v]['owners'] if t!=tag)
                moves.append([v,sid,tag+'|'+winner,winner,'DUPLICATE_RESOLVED',geo[v]['pixels'],*geo[v]['bbox']])
            raw=edits(raw,[(ps.start,ps.end,frag)])
    result['common/history/states/00_states.txt']=raw
    # Territory remains in the original State Region: only historical owner subdivisions change.
    owners=C.defaultdict(dict)
    for r in base['inventory']['owners']:
        v,s,t=r['key'];owners[s][v]=t
    weights={}
    for sid,groups in GROUPS.items():
        old=OLD[sid]; pool=[r['key'][0] for r in base['inventory']['owners'] if r['key'][1:]==[sid,old]]
        ww=C.Counter()
        for v in pool:ww[next((t for t,vs in groups.items() if v in vs),old)]+=geo[v]['pixels']
        weights[sid]=dict(ww)
    # Retain every create_pop field except its size: religion, status, literacy etc.
    for path,original in base['originals'].items():
        if not path.startswith(('common/history/pops/','common/history/population/')):continue
        operations=[]
        for s in cw.walk(cw.parse(original)):
            sid=s.key.removeprefix('s:')
            if sid not in GROUPS:continue
            rr=s.children('region_state:'+OLD[sid])
            if not rr:continue
            r=rr[0];assert all(n.key=='create_pop' for n in r.children()),'Unexpected extra population command'
            pools={t:[] for t in weights[sid]}
            for p in r.children('create_pop'):
                for tag,n in apportion(int(p.one('size')),weights[sid]).items():
                    if n:pools[tag].append(body_rewrite(original,p,'size',n))
            new='\n'.join('region_state:'+tag+' = {\n\t\t\t# MAP-2E integer land-area allocation, not a census.\n\t\t\t'+'\n\t\t\t'.join(pp)+'\n\t\t}' for tag,pp in sorted(pools.items()) if pp)
            operations.append((r.start,r.end,new))
        if operations:result[path]=edits(original,operations)
    # Only two regions lose all PER territory. Economic ownership remains PER;
    # the holder's headquarters is relocated to an existing, populated PER region.
    lost_per={'STATE_ARMENIA','STATE_AZERBAIJAN','STATE_ELIZAVETPOL'}
    building_transfers=[]
    for path,original in base['originals'].items():
        if not path.startswith('common/history/buildings/'):continue
        ops=[]
        for s in cw.walk(cw.parse(original)):
            sid=s.key.removeprefix('s:')
            if sid not in ['STATE_ARMENIA','STATE_AZERBAIJAN','STATE_GREATER_CAUCASUS']:continue
            tag=OLD[sid];rs=s.children('region_state:'+tag)
            if not rs:continue
            r=rs[0];pools=C.defaultdict(list)
            assert all(n.key=='create_building' for n in r.children())
            for b in r.children('create_building'):
                kind=cw.scalar(b.one('building'));frag=original[b.start:b.end];dest=tag
                if sid=='STATE_ARMENIA':dest='NAK' if kind=='building_vineyard' else 'ARM'
                if sid=='STATE_AZERBAIJAN':dest='AZB'
                if sid=='STATE_GREATER_CAUCASUS' and kind in ['building_textile_mill','building_wheat_farm']:dest='IMR'
                holders=[n for n in cw.walk([b]) if n.key=='building' and n.children('country')]
                if sid in lost_per:
                    changes=[]
                    for h in holders:
                        if cw.scalar(h.one('country'))=='c:PER':
                            node=h.children('region')[0];changes.append((node.start-b.start,node.end-b.start,'region = "STATE_TABRIZ"'))
                    frag=edits(frag,changes)
                if kind=='building_railway' and sid in ['STATE_ARMENIA','STATE_GREATER_CAUCASUS']:
                    # Split road levels, not technology or recipes. Same owner, PMs and reserves.
                    oldlevel=int(holders[0].one('levels'));expected=4 if sid=='STATE_ARMENIA' else 2;assert oldlevel==expected
                    h=next(n for n in cw.walk(cw.parse(frag)) if n.key=='levels');levels=[('ARM',3),('NAK',1)] if sid=='STATE_ARMENIA' else [('GEO',1),('IMR',1)]
                    for d,n in levels:pools[d].append(edits(frag,[(h.start,h.end,'levels = '+str(n))]));building_transfers.append([path,sid,tag,d,kind,n])
                else:pools[dest].append(frag);building_transfers.append([path,sid,tag,dest,kind,sum(int(n.value) for n in cw.walk([b]) if n.key=='levels')])
            new='\n'.join('region_state:'+t+' = {\n\t\t\t'+'\n\t\t\t'.join(bb)+'\n\t\t}' for t,bb in pools.items())
            ops.append((r.start,r.end,new))
        raw=edits(original,ops)
        # Any other ownership headquarters that point to newly non-PER subdivisions.
        ops=[]
        for h in cw.walk(cw.parse(raw)):
            if h.key=='building' and cw.scalar(h.one('country',''))=='c:PER' and cw.scalar(h.one('region','')) in lost_per:
                n=h.children('region')[0];ops.append((n.start,n.end,'region = "STATE_TABRIZ"'))
        result[path]=edits(raw,ops)
    for path,original in base['originals'].items():
        if not path.startswith('common/history/military_formations/'):continue
        ops=[]
        for c in cw.walk(cw.parse(original)):
            if c.key=='c:PER':
                for u in cw.walk([c]):
                    if u.key=='combat_unit' and u.one('state_region')=='s:STATE_ARMENIA':
                        n=u.children('state_region')[0];ops.append((n.start,n.end,'state_region = s:STATE_TABRIZ'))
        if ops:result[path]=edits(original,ops)
    # Fix real native locator/hub mismatches, not the sovereignty of their RGBs.
    for path,original in base['originals'].items():
        if not path.startswith('map_data/state_regions/'):continue
        raw=original;ops=[]
        for s in cw.parse(original):
            replacements={'STATE_GREATER_CAUCASUS':{'wood':'x4A4DF9','mine':'xD62036'},'STATE_KUBAN':{'wood':'x9A01E0'},'STATE_STAVROPOL':{'wood':'xA4B654'}}.get(s.key,{})
            for kind,rgb in replacements.items():
                n=s.children(kind)[0];ops.append((n.start,n.end,kind+' = "'+rgb+'"'))
        if ops:result[path]=edits(raw,ops)
    path='common/country_definitions/00_countries.txt';raw=result[path];ops=[]
    for n in cw.parse(raw):
        if n.key in ['ARM','AZB']:
            frag=raw[n.start:n.end].replace('country_type = recognized','country_type = unrecognized').replace('tier = kingdom','tier = principality').replace('is_named_from_capital = yes','religion = shiite')
            if n.key=='ARM':frag=frag.replace('cultures = { armenian }','cultures = { azerbaijani armenian }')
            ops.append((n.start,n.end,frag))
    result[path]=edits(raw,ops)
    path='common/history/countries/arm - armenia.txt';result[path]=result[path].replace('law_type:law_organic_regulation','law_type:law_monarchy')
    # These are major regional authorities, not one tag for every village or melik.
    definitions='# MAP-2E: major local authorities in 1776. Minor principalities remain documented abstractions.\n'
    countries='COUNTRIES = {\n'
    tech=['distillation','improved_husbandry','international_relations','light_infantry_tactics','organized_textile_production','regulated_small_arms','shaft_mining','traditional_food_processing','organized_workshops','organized_military_establishments']
    laws=['monarchy','autocracy','mercantilism','traditionalism','manorialism','hereditary_bureaucrats','land_based_taxation','peasant_levies','no_schools','racial_segregation']
    for t,(cap,cu,rel,tier,color) in NEW.items():
        definitions+=f'{t} = {{ color = {{ {" ".join(map(str,color))} }} country_type = '+('recognized' if t=='IMR' else 'unrecognized')+f' tier = {tier} cultures = {{ {cu} }} religion = {rel} capital = {cap} }}\n'
    for t in [*NEW,'AZB','ABK']:
        countries+='\tc:'+t+' ?= {\n'+''.join('\t\tadd_technology_researched = '+v+'\n' for v in tech)+''.join('\t\tactivate_law = law_type:law_'+v+'\n' for v in laws)+('\t\tactivate_law = law_type:law_slavery_banned\n' if t=='IMR' else '')+'\t\tset_tax_level = medium\n\t}\n'
    result['common/country_definitions/03_1776_caucasus.txt']=definitions
    result['common/history/countries/1776_caucasus_local_authorities.txt']=countries+'}\n'
    # Targeted early-period country names; do not replace the existing naming trees.
    path='common/dynamic_country_names/00_dynamic_country_names.txt';raw=result[path]
    for t in ['AZB','CHC']:
        node=next(n for n in cw.parse(raw) if n.key==t);at=node.end-1
        raw=edits(raw,[(at,at,'\n\tdynamic_country_name = { name = aor1776_'+t.lower()+' adjective = aor1776_'+t.lower()+'_adj is_main_tag_only = yes priority = 100 trigger = { exists = scope:actor scope:actor ?= { current_date < 1828.1.1 } } }\n')])
    raw+='\nARM = { dynamic_country_name = { name = aor1776_arm adjective = aor1776_arm_adj is_main_tag_only = yes priority = 100 trigger = { exists = scope:actor scope:actor ?= { current_date < 1828.1.1 } } } }\n';result[path]=raw
    eff='aor1776_caucasus_state_names = {\n'
    for (sid,t),names in STATE_NAMES.items():
        key='aor1776_'+sid.lower()+'_'+t.lower();eff+=f'\tif = {{ limit = {{ state_region = s:{sid} owner = {{ c:{t} ?= this }} }} set_state_name = {key} }}\n'
    result['common/scripted_effects/1776_caucasus_state_names.txt']=eff+'}\n'
    result['common/on_actions/13_1776_caucasus_state_names.txt']='''# Add child actions; never replace other MAP naming actions.
on_game_started = { on_actions = { aor1776_caucasus_names_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_caucasus_names_initialize } }
on_state_created = { on_actions = { aor1776_caucasus_state_name_changed } }
on_state_owner_change = { on_actions = { aor1776_caucasus_state_name_changed } }
aor1776_caucasus_names_initialize = { effect = { every_state = { aor1776_caucasus_state_names = yes } } }
aor1776_caucasus_state_name_changed = { effect = { aor1776_caucasus_state_names = yes } }
'''
    flags='# Generic identification flags assembled from native assets; not reconstructed historical banners.\n'
    for t in NEW:
        flags+=t+' = { pattern = "pattern_solid.tga" color1 = '+('"white"' if t=='IMR' else 'rgb { '+ ' '.join(str(v/255) for v in NEW[t][4])+' }')+' color2 = "white" colored_emblem = { texture = "'+('ce_cross_couped.dds' if t=='IMR' else 'ce_crescent.dds')+'" color1 = '+('"red"' if t=='IMR' else '"white"')+' instance = { scale = { 0.45 0.45 } position = { 0.5 0.5 } } } }\n'
    result['common/coat_of_arms/coat_of_arms/04_1776_caucasus.txt']=flags
    for language,ni,si in [('english',0,0),('french',2,1)]:
        loc='\ufeffl_'+language+':\n'
        for t,nn in NAMES.items():
            if t in NEW:loc+=' '+t+':0 "'+nn[ni]+'"\n '+t+'_ADJ:0 "'+nn[ni+1]+'"\n'
            else:loc+=' aor1776_'+t.lower()+':0 "'+nn[ni]+'"\n aor1776_'+t.lower()+'_adj:0 "'+nn[ni+1]+'"\n'
        for (sid,t),nn in STATE_NAMES.items():loc+=' aor1776_'+sid.lower()+'_'+t.lower()+':0 "'+nn[si]+'"\n'
        result[f'localization/{language}/1776_caucasus_l_{language}.yml']=loc
    changed={p:v for p,v in result.items() if v!=base['originals'].get(p)}
    return changed,moves,weights,building_transfers
def build(validate_clean=True):
    base=json.loads(BASE.read_text(encoding='utf-8'));changed,moves,weights,bt=transform(base)
    patch='*** Begin Patch\n'
    for p,new in changed.items():
        if validate_clean:assert not (ROOT/p).exists() or (ROOT/p).read_text(encoding='utf-8-sig')==base['originals'].get(p),'Concurrent edits: '+p
        if p not in base['originals']:patch+='*** Add File: '+str(ROOT/p).replace('\\','/')+'\n'+''.join('+'+l+'\n' for l in new.splitlines())
        else:
            old=base['originals'][p]
            if (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'):old='\ufeff'+old
            if old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
            diff=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=12))
            patch+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
            for l in diff[2:]:patch+=('@@' if l.startswith('@@') else l)+'\n'
    patch+='*** End Patch\n'
    (OUT/'INTEGRATION.patch').write_text(patch,encoding='utf-8')
    (OUT/'PLAN.json').write_text(json.dumps({'files':list(changed),'territorial':moves,'weights':weights,'building_transfers':bt,'new_tags':list(NEW)},ensure_ascii=False,indent=2),encoding='utf-8')
    print('Prepared',len(changed),'files;',len(moves),'territorial records;',len(NEW),'major new tags')
def repair():
    base=json.loads(BASE.read_text(encoding='utf-8'));changed,*_=transform(base)
    patch='*** Begin Patch\n'
    for p,new in changed.items():
        old=(ROOT/p).read_text(encoding='utf-8')
        if old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
        if old==new:continue
        patch+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
        for l in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=12))[2:]:patch+=('@@' if l.startswith('@@') else l)+'\n'
    print(patch+'*** End Patch')
if __name__=='__main__':
    import sys
    if '--repair' in sys.argv:repair()
    else:build('--final-plan' not in sys.argv)
