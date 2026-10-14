"""MAP-0 static inventory. Writes reports only, never game/history/map assets.

Run with the bundled Python (Pillow required). The engine, startup effects and
geographical connectivity are deliberately not simulated by this parser.
"""
from __future__ import annotations
import argparse
import collections as C
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
from PIL import Image
from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized

ROOT = Path(__file__).resolve().parents[1]
REGIONS = [
    'R1_WESTERN_EUROPE', 'R2_NORTHERN_CENTRAL_EASTERN_EUROPE',
    'R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA', 'R4_SOUTH_ASIA',
    'R5_EAST_ASIA', 'R6_SOUTHEAST_ASIA_OCEANIA', 'R7_SUBSAHARAN_AFRICA',
    'R8_NORTH_AMERICA_CARIBBEAN', 'R9_SOUTH_AMERICA',
]
R2_WEST = set(('SVEALAND GOTALAND SCANIA NORRLAND GOTLAND JUTLAND ZEALAND WESTERN_NORWAY NORTHERN_NORWAY EASTERN_NORWAY ICELAND AUSTRIA BOHEMIA MORAVIA STYRIA TYROL SOUTH_TYROL POMERANIA ELBE EAST_SWITZERLAND WEST_SWITZERLAND WESTPHALIA ANHALT RHINELAND NORTH_RHINE BRANDENBURG SCHLESWIG_HOLSTEIN WURTTEMBERG BADEN HANNOVER BRUNSWICK BAVARIA FRANCONIA SAXONY HESSE MECKLENBURG RUHR').split())
R2_SOUTH = set(('EASTERN_THRACE DOBRUDJA ALBANIA BOSNIA NORTHERN_THRACE BULGARIA SLOVENIA DALMATIA CROATIA SLAVONIA ISTRIA MONTENEGRO WESTERN_SERBIA EASTERN_SERBIA KOSOVO CRETE WEST_AEGEAN_ISLANDS EAST_AEGEAN_ISLANDS ATTICA THESSALIA SKOPIA MACEDONIA WESTERN_THRACE IONIAN_ISLANDS PELOPONNESE').split())
PRIOR_WORK = {'STATE_'+s for s in 'DOBRUDJA NUNAVUT EAST_SWITZERLAND GREATER_CAUCASUS BESSARABIA ISTRIA LOMBARDY SOUTH_TYROL'.split()}

def prov(v):
    s = scalar(v)
    return 'x'+s[1:].upper() if re.fullmatch(r'[xX][0-9a-fA-F]{6}', s) else s

def values(n, key):
    return [scalar(v.value) for b in n.children(key) for v in b.children() if not isinstance(v.value, list)]

def effective(root, game, folder):
    files = {p.name: p for p in (game/folder).glob('*.txt')}
    files.update({p.name: p for p in (root/folder).glob('*.txt')})
    return [files[k] for k in sorted(files)]

def label(p, root, game):
    if p.is_relative_to(root):
        return 'MOD:'+p.relative_to(root).as_posix()
    return 'VANILLA:'+p.relative_to(game).as_posix()

def trees(root, game, folder):
    for p in effective(root, game, folder):
        raw = p.read_text(encoding='utf-8-sig')
        yield p, raw, parse(raw)

def own_inventory(root, game):
    owners, pairs, odd = C.defaultdict(list), {}, []
    for p, raw, ns in trees(root, game, 'common/history/states'):
        for state in walk(ns):
            if not state.key.startswith('s:STATE_'):
                continue
            sid = state.key[2:]
            for create in state.children('create_state'):
                tag = scalar(create.one('country')).removeprefix('c:')
                ps = [prov(v) for v in values(create, 'owned_provinces')]
                pairs[sid, tag] = ps
                for v in ps:
                    owners[v].append((sid, tag))
                for bare in create.children(''):
                    odd.append((sid, tag, label(p, root, game), raw[:bare.start].count('\n')+1, scalar(bare.value)))
    return owners, pairs, odd

def allocation(sid, origin):
    s = sid.removeprefix('STATE_')
    filename = origin.split('/')[-1]
    if filename == '00_west_europe.txt':
        ix = 7 if s == 'GREENLAND' else (1 if s in R2_WEST else 0)
    elif filename == '01_south_europe.txt':
        ix = 6 if s == 'CAPE_VERDE' else (2 if s in {'CANARY_ISLANDS', 'MADEIRA'} else (1 if s in R2_SOUTH else 0))
    elif filename == '02_east_europe.txt' or filename == '15_russia.txt':
        ix = 2 if s in {'KUBAN', 'DAGESTAN', 'GREATER_CAUCASUS', 'ARMENIA', 'AZERBAIJAN'} else 1
    elif filename in {'05_north_america.txt', '06_central_america.txt'}:
        ix = 7
    elif filename == '07_south_america.txt': ix = 8
    elif filename == '03_north_africa.txt': ix = 2
    elif filename == '04_subsaharan_africa.txt': ix = 6
    elif filename == '08_middle_east.txt': ix = 2
    elif filename == '09_central_asia.txt':
        ix = 1 if s in {'SAMARA', 'TARTARIA', 'ASTRAKHAN'} else (4 if s in {'LHASA', 'NGARI'} else (3 if s in {'QUETTA', 'BALUCHISTAN', 'HIMALAYAS', 'EASTERN_HIMALAYAS'} else 2))
    elif filename == '10_india.txt': ix = 3
    elif filename == '11_east_asia.txt': ix = 4
    elif filename in {'12_indonesia.txt', '13_australasia.txt'}: ix = 5
    elif filename == '14_siberia.txt': ix = 1 if s == 'URAL' else 4
    else: raise ValueError('Unallocated region: '+sid+' '+origin)
    # Geography overrides: archive filenames mix several continents/subregions.
    if s in {'CAMBODIA','BANGKOK','TONKIN','ANNAM','MEKONG','LAOS','CHIANG_MAI','NAKHON_RATCHASIMA','HAWAIIAN_ISLANDS','BURMA','MANDALAY','ARAKAN','PEGU','TENASSERIM','SHAN_STATES','KACHIN'}: ix=5
    if s == 'INDIAN_OCEAN_TERRITORY': ix=6
    if s in {'URALSK','KHIVA','SEMIRECHE','JETISY','AKMOLINSK','FERGANA','MERZ','SYRDARYA','AKTOBE','NORTH_CAUCASUS','ELIZAVETPOL','STAVROPOL'}: ix=2
    if s in {'SURGUT','KRASNOYARSK','ALTAI','BURYATIA','KOLYMA','AMUR','CHELYABINSK'}: ix=4
    if s in {'ERITREA','KORDOFAN','DARFUR','BLUE_NILE','EASTERN_MALI','WESTERN_MALI','TIMBUKTU','NIGER','CHAD'}: ix=6
    secondary, note = '', ''
    if s in {'EASTERN_THRACE', 'NORTHERN_THRACE', 'DOBRUDJA', 'CRETE', 'WEST_AEGEAN_ISLANDS', 'EAST_AEGEAN_ISLANDS'}:
        secondary = REGIONS[2]; note = 'Interface ottomane Europe/Anatolie; responsabilité géographique européenne.'
    if s in {'KUBAN', 'DAGESTAN', 'GREATER_CAUCASUS', 'ARMENIA', 'AZERBAIJAN'}:
        secondary = REGIONS[1]; note = 'Interface Caucase/Russie européenne.'
    if s in {'URAL', 'TOBOLSK', 'OB', 'TOMSK'}:
        secondary = REGIONS[4 if ix == 1 else 1]; note = 'Interface Europe/Sibérie; découpage de mission, pas conclusion historique.'
    if s in {'PASHTUNISTAN', 'CENTRAL_HIGHLANDS', 'NORTHERN_BALUCHISTAN', 'HERAT', 'BALKH', 'QUETTA', 'KANDAHAR', 'KABUL', 'BALUCHISTAN'}:
        secondary = REGIONS[3 if ix == 2 else 2]; note = 'Interface Afghanistan/Baloutchistan; coordonner sans dupliquer les recommandations.'
    if s in {'LHASA', 'NGARI', 'HIMALAYAS', 'EASTERN_HIMALAYAS', 'ASSAM'}:
        secondary = REGIONS[3 if ix == 4 else 4]; note = 'Interface himalayenne; rattachement géographique à confirmer lors du mapping fin.'
    if s in {'DONGOLA','MAURITANIA','INNER_MAURITANIA','EAST_SAHARA','WEST_SAHARA','ERITREA','KORDOFAN','DARFUR','BLUE_NILE','TIMBUKTU','NIGER','CHAD'}:
        secondary=REGIONS[6 if ix==2 else 2]; note='Interface Sahara/Sahel/Nil; responsable géographique unique, frontière de mission conventionnelle.'
    if s in {'KACHIN','BURMA','PEGU','TENASSERIM','SHAN_STATES','TONKIN','YUNNAN','GUANGXI'}:
        secondary=REGIONS[3 if s in {'KACHIN','BURMA'} else (4 if ix==5 else 5)]; note='Interface Asie du Sud/Asie orientale/Asie du Sud-Est.'
    if s in {'LOMBARDY','PIEDMONT','SAVOY','LIGURIA','ISTRIA','SOUTH_TYROL'}:
        secondary=REGIONS[1 if ix==0 else 0]; note='Interface alpine/adriatique R1-R2; VEN/GEN restent inclus et leurs historiques protégés.'
    if s in {'DZUNGARIA','TIANSHAN'}:
        secondary=REGIONS[2]; note='Interface Asie orientale/Asie centrale; responsabilité principale R5, contrôle historique à rechercher.'
    if s == 'CYPRUS':
        secondary=REGIONS[1]; note='Interface Méditerranée orientale; responsabilité principale R3.'
    if s in {'PANAMA','MAGDALENA'}:
        secondary=REGIONS[8 if ix==7 else 7]; note='Interface de l’isthme R8-R9; une seule mission principale.'
    return REGIONS[ix], secondary, note

def write_csv(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as out:
        w = csv.DictWriter(out, fields, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def audit(root, game, raster, context, issue):
    defs, ids = {}, C.defaultdict(list)
    for p, raw, ns in trees(root, game, 'map_data/state_regions'):
        for n in ns:
            if n.key.startswith('STATE_'):
                sid = n.key
                if sid in defs: issue(context, 'DUPLICATE_STATE', 'ERROR', sid, '', label(p,root,game), 'Plusieurs définitions effectives du même State_ID.')
                defs[sid] = {'node':n, 'provinces':[prov(v) for v in values(n,'provinces')], 'origin':label(p,root,game), 'id':scalar(n.one('id')), 'line':raw[:n.start].count('\n')+1}
                ids[scalar(n.one('id'))].append(sid)
    members = C.defaultdict(list)
    for sid,d in defs.items():
        for v in d['provinces']: members[v].append(sid)
    default = parse((game/'map_data/default.map').read_text(encoding='utf-8-sig'))
    sea = {prov(v.value) for n in default if n.key=='sea_starts' for v in n.children()}
    lakes = {prov(v.value) for n in default if n.key=='lakes' for v in n.children()}
    owners,pairs,odd = own_inventory(root,game)
    for sid,tag,file,line,token in odd:
        issue(context,'BARE_TOKEN_IN_CREATE_STATE','BLOCKER',sid,'',f'{file}:{line}',f'Token inattendu dans create_state: {token!r}; contrôle de syntaxe moteur requis.')
    for v, ss in members.items():
        if len(ss)>1: issue(context,'MULTIPLE_STATE_MEMBERSHIP','BLOCKER','|'.join(ss),v,'map_data/state_regions','Province dans plusieurs State Regions.')
        if v not in raster: issue(context,'PROVINCE_NOT_IN_BITMAP','BLOCKER','|'.join(ss),v,'map_data/state_regions','Identifiant absent du bitmap chargé.')
    for ident, ss in ids.items():
        if len(ss)>1: issue(context,'DUPLICATE_NUMERIC_STATE_ID','BLOCKER','|'.join(ss),'','map_data/state_regions',ident)
    for v, os in owners.items():
        if len(os)>1: issue(context,'DUPLICATE_PROVINCE_OWNER' if len(set(os))>1 else 'REPEATED_SAME_OWNER_PROVINCE','BLOCKER' if len(set(os))>1 else 'REVIEW','|'.join(sorted({s for s,t in os})),v,'common/history/states/00_states.txt','Attributions écrites: '+'|'.join(t for s,t in os))
        if v not in raster: issue(context,'OWNED_PROVINCE_NOT_IN_BITMAP','BLOCKER','|'.join(s for s,t in os),v,'common/history/states/00_states.txt','Identifiant absent du bitmap.')
        for sid,tag in os:
            if sid not in defs or sid not in members.get(v,[]): issue(context,'OWNER_STATE_MISMATCH','BLOCKER',sid,v,'common/history/states/00_states.txt',tag)
    countries = {}
    for p,raw,ns in trees(root,game,'common/country_definitions'):
        for n in ns:
            key = n.key.removeprefix('REPLACE_OR_CREATE:')
            if n.children('country_type'): countries[key]={'type':scalar(n.one('country_type')), 'capital':scalar(n.one('capital'))}
    for sid,tag in pairs:
        if tag not in countries: issue(context,'UNKNOWN_OWNER_TAG','BLOCKER',sid,'','common/history/states/00_states.txt',tag)
    active = {t for s,t in pairs}
    for tag in sorted(active):
        capital = countries.get(tag,{}).get('capital','')
        if capital and not pairs.get((capital,tag)):
            issue(context,'CAPITAL_NOT_OWNED','REVIEW',capital,'','common/country_definitions',f'{tag}: capitale définie non possédée au départ; peut être remplacée par script.')
    strategic = C.defaultdict(list)
    for p,raw,ns in trees(root,game,'common/strategic_regions'):
        for n in ns:
            for s in values(n,'states'): strategic[s].append(n.key)
    for sid,d in defs.items():
        n = d['node']
        for key in ('city','port','farm','mine','wood'):
            if n.children(key) and prov(n.one(key)) not in d['provinces']:
                issue(context,'HUB_OUTSIDE_STATE','ERROR',sid,prov(n.one(key)),d['origin'],key)
        if n.children('naval_exit_id') and scalar(n.one('naval_exit_id')) not in ids:
            issue(context,'UNKNOWN_NAVAL_EXIT','ERROR',sid,'',d['origin'],scalar(n.one('naval_exit_id')))
        if len(strategic[sid]) != 1: issue(context,'STRATEGIC_REGION_COUNT','REVIEW',sid,'','common/strategic_regions',str(strategic[sid]))
    population = C.Counter(); orphan_selectors = C.Counter()
    for folder in ('pops','buildings','population'):
        for p,raw,ns in trees(root,game,'common/history/'+folder):
            for n in walk(ns):
                if not n.key.startswith('s:STATE_'): continue
                sid = n.key[2:]
                if sid not in defs: issue(context,'UNKNOWN_HISTORY_STATE','ERROR',sid,'',label(p,root,game),'Dossier '+folder)
                for child in n.children():
                    if not child.key.startswith('region_state:'): continue
                    tag = child.key.split(':',1)[1]
                    if (sid,tag) not in pairs:
                        orphan_selectors[folder]+=1
                        issue(context,'ORPHAN_HISTORY_SELECTOR','ERROR',sid,'',label(p,root,game)+':'+str(raw[:child.start].count('\n')+1),folder+' / '+tag+' sans territoire correspondant.')
                    if folder=='pops':
                        for pop in child.children('create_pop'): population[sid,tag]+=int(scalar(pop.one('size','0')))
    relations = C.defaultdict(list)
    pact_types = {'puppet','vassal','tributary','personal_union','protectorate','colony','chartered_company','crown_land','dominion'}
    def traverse(ns, current='', conditional=False):
        for n in ns:
            here = n.key[2:] if n.key.startswith('c:') else current
            cond = conditional or n.key in {'if','else_if','else','random','random_list'}
            if n.key=='create_diplomatic_pact' and scalar(n.one('type')) in pact_types:
                relations[scalar(n.one('country')).removeprefix('c:')].append((here,scalar(n.one('type')),cond))
            traverse(n.children(),here,cond)
    for p,raw,ns in trees(root,game,'common/history/diplomacy'): traverse(ns)
    terrain = {}
    for n in parse((game/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')): terrain[prov(n.key)]=scalar(n.value)
    for v in set(terrain)-set(raster):
        issue(context,'TERRAIN_ID_NOT_IN_BITMAP','REVIEW','',v,'VANILLA:map_data/province_terrains.txt','Entrée de terrain sans couleur dans le raster.')
    for v in set(raster)-sea-lakes-set(terrain):
        issue(context,'LAND_TERRAIN_MISSING','REVIEW','|'.join(members.get(v,[])),v,'VANILLA:map_data/province_terrains.txt','Terrain terrestre non défini explicitement.')
    adjacency_rows=list(csv.DictReader((game/'map_data/adjacencies.csv').open(encoding='utf-8-sig'),delimiter=';'))
    for ix,row in enumerate(adjacency_rows,2):
        for field in ('From','To','Through'):
            v=prov(row.get(field,''))
            if not v or v in {'-1','0'}: continue
            if v not in raster: issue(context,'ADJACENCY_ID_NOT_IN_BITMAP','ERROR','',v,f'VANILLA:map_data/adjacencies.csv:{ix}',field)
    loc_missing={}
    for language in ('english','french'):
        folder='localization/'+language
        files={p.name:p for p in (game/folder).rglob('*.yml')}
        files.update({p.name:p for p in (root/folder).rglob('*.yml')})
        keys=set()
        for p in files.values():
            keys.update(re.findall(r'^\s*([A-Za-z0-9_.-]+):\d*\s',p.read_text(encoding='utf-8-sig'),re.M))
        missing=sorted((set(defs)|active)-keys); loc_missing[language]=missing
        for key in missing:
            issue(context,'BASE_LOCALIZATION_KEY_MISSING','REVIEW',key if key.startswith('STATE_') else '','',folder,'Clé de base '+key+' absente; noms dynamiques ou fallback possibles.')
    land = {s:d for s,d in defs.items() if not set(d['provinces']) <= sea|lakes}
    unassigned = set(raster)-set(members)-lakes
    if unassigned: issue(context,'BITMAP_PROVINCES_WITHOUT_REGION','REVIEW','','|'.join(sorted(unassigned)),'VANILLA:map_data/provinces.png','Pixels présents sans State Region ni lac; pas de suppression automatique.')
    missingowners=[]
    for sid,d in land.items():
        impassable={prov(v) for v in values(d['node'],'impassable')}
        for v in d['provinces']:
            if v not in owners and v not in impassable:
                missingowners.append(v); issue(context,'LAND_PROVINCE_WITHOUT_OWNER','REVIEW',sid,v,d['origin'],'Vérifier intention et moteur avant attribution.')
    return {'defs':defs,'land':land,'members':members,'owners':owners,'pairs':pairs,'countries':countries,'relations':relations,'strategic':strategic,'terrain':terrain,'sea':sea,'lakes':lakes,'population':population,'unassigned':unassigned,'missingowners':missingowners,'orphans':dict(orphan_selectors),'loc_missing':loc_missing,'adjacency_rows':len(adjacency_rows)}

def main():
    cli = argparse.ArgumentParser(); cli.add_argument('--game',type=Path,default=Path('C:/Games/Victoria 3/game')); cli.add_argument('--candidate',type=Path); cli.add_argument('--self-test',action='store_true'); cli.add_argument('--strict',action='store_true',help='Exit 2 when ERROR/BLOCKER findings exist; inventory mode exits 0 even with findings.'); args=cli.parse_args()
    if args.self_test:
        bad=parse('STATES={s:STATE_A={create_state={git status git fetch origin country=c:A owned_provinces={x123ABC}}}}')
        assert len(next(n for n in walk(bad) if n.key=='create_state').children(''))==5
        assert prov('xabcdef')=='xABCDEF'
        assert allocation('STATE_GREENLAND','MOD:map_data/state_regions/00_west_europe.txt')[0]==REGIONS[7]
        assert allocation('STATE_ISTRIA','MOD:map_data/state_regions/01_south_europe.txt')[0]==REGIONS[1]
        print('PASS self-tests: malformed tokens / RGB IDs / geographical allocation')
    out=ROOT/'docs/reports/map'; out.mkdir(parents=True,exist_ok=True)
    bitmap=args.game/'map_data/provinces.png'
    with Image.open(bitmap) as im:
        dimensions=im.size
        colors=im.convert('RGB').getcolors(1<<24)
        raster={'x%02X%02X%02X'%color:count for count,color in colors}
    issues=[]
    def issue(context,kind,severity,state,province,source,detail):
        issues.append(dict(Issue_ID=f'MAP0-{len(issues)+1:04}',Context=context,Issue_Type=kind,Severity=severity,State_ID=state,Province_ID=province,Evidence_Source=source,Observed_Fact=detail,Historical_Conclusion='NOT_RESEARCHED',Disposition='DOCUMENT_ONLY'))
    current=audit(ROOT,args.game,raster,'MAIN_WORKING_TREE',issue)
    candidate=audit(args.candidate,args.game,raster,'COLLABORATOR_CANDIDATE',issue) if args.candidate else None
    catalogue=list(csv.DictReader((ROOT/'docs/reports/buildings/BUILD_START_1776_RESEARCH_REGIONS.csv').open(encoding='utf-8-sig')))
    cat={(r['State_ID'],r['Owner_TAG']):r for r in catalogue}
    cat_missing=set(cat)-set(current['pairs']); cat_extra=set(current['pairs'])-set(cat)
    for s,t in sorted(cat_missing|cat_extra): issue('MAIN_WORKING_TREE','CATALOGUE_PAIR_MISMATCH','REVIEW',s,'','BUILD_START_1776_RESEARCH_REGIONS.csv',t)
    pairrows=[]
    for (s,t),ps in sorted(current['pairs'].items()):
        d=current['defs'][s]; reg,secondary,note=allocation(s,d['origin']); cr=cat.get((s,t),{})
        pairrows.append(dict(Region_ID=reg,Secondary_Region_ID=secondary,State_ID=s,State_Display_Name=cr.get('State_Display_Name',s),Owner_TAG=t,Owner_Name=cr.get('Owner_Name',t),Province_Count=len(ps),Province_IDs='|'.join(ps),Research_Included='YES',Protected_Specific_History='YES' if t in {'VEN','GEN'} else 'NO',Previous_Catalogue_Region=cr.get('Research_Region','MISSING'),Geographic_Notes=note))
    row_by_state={r['State_ID']:r for r in pairrows}
    baseline=[]
    for v in sorted(raster):
        ss=current['members'].get(v,[]); os=current['owners'].get(v,[])
        kind='SEA' if v in current['sea'] else ('LAKE' if v in current['lakes'] else ('LAND' if ss else 'UNCLASSIFIED'))
        for sid in ss or ['']:
            d=current['defs'].get(sid,{})
            relevant=sorted({t for s,t in os}) or ['']
            for t in relevant:
                r=row_by_state.get(sid,{})
                rel=current['relations'].get(t,[])
                chain=[]; cursor=t; visited=set(); uncertain=False
                while cursor and cursor not in visited:
                    visited.add(cursor); rs=current['relations'].get(cursor,[])
                    if len(rs)!=1 or rs[0][2]:
                        uncertain=bool(rs); break
                    cursor=rs[0][0]; chain.append(cursor)
                status='MULTIPLE_OR_CONDITIONAL_INITIAL_PACTS' if uncertain else ('STATIC_INITIAL_PACT_CHAIN' if chain else 'NO_INITIAL_SUBJECT_PACT_FOUND')
                findings=[i['Issue_ID'] for i in issues if i['Context']=='MAIN_WORKING_TREE' and ((i['Province_ID']==v) or (i['State_ID']==sid and not i['Province_ID']))]
                baseline.append(dict(Region_ID=r.get('Region_ID',''),Province_ID=v,State_ID=sid,State_Numeric_ID=d.get('id',''),Territory_Type=kind,Owner_TAG=t,Owner_Name=cat.get((sid,t),{}).get('Owner_Name',t),Current_Province_Owners='|'.join(sorted({tag for state,tag in os})),Ownership_History_State_IDs='|'.join(sorted({s for s,tag in os if tag==t})),Owner_State_Key=sid+'|'+t if t else '',Country_Type=current['countries'].get(t,{}).get('type',''),Sovereign_TAG=cursor if not uncertain else '',Initial_Overlord_TAGs='|'.join(x[0] for x in rel),Relationship_Type='|'.join(x[1] for x in rel),Sovereignty_Interpretation=status,Province_Terrain=current['terrain'].get(v,''),Strategic_Regions='|'.join(current['strategic'].get(sid,[])),Province_Pixels=raster[v],Geography_Source=d.get('origin','VANILLA:map_data/default.map'),Ownership_Source='MOD:common/history/states/00_states.txt' if t else '',Collaborator_Preexisting_Edit='YES' if sid in PRIOR_WORK else 'NO',Pending_Collaborator_Edit='YES' if sid in {'STATE_WALLONIA','STATE_LOMBARDY','STATE_BESSARABIA'} else 'NO',Known_Issue_IDs='|'.join(findings),Proposed_Historical_Owner_TAG='',Technical_Notes='Statique; démarrage et souveraineté historique non évalués.'))
    write_csv(out/'MAP_1776_BASELINE.csv',baseline,list(baseline[0]))
    write_csv(out/'MAP_1776_9_REGIONS.csv',pairrows,list(pairrows[0]))
    if candidate:
        loss=sum(candidate['population'].values())-sum(current['population'].values())
        if loss:
            changed_pop_states=sorted({s for s,t in set(current['population'])|set(candidate['population']) if current['population'][s,t]!=candidate['population'][s,t]})
            issue('COLLABORATOR_CANDIDATE','POPULATION_DELTA','BLOCKER','|'.join(changed_pop_states),'','common/history/pops',f'Variation nette de population écrite: {loss}; transfert non conservatif à justifier.')
        if current['pairs'].get(('STATE_WALLONIA','LUX')) and not any(t=='LUX' for s,t in candidate['pairs']):
            issue('COLLABORATOR_CANDIDATE','LUXEMBOURG_STATE_REMOVED','REVIEW','STATE_WALLONIA','xD001A0','common/history/states/00_states.txt','LUX perd sa seule province; vérifier les scopes historiques restants. Décision politique et migration de données requises.')
    write_csv(out/'MAP_1776_KNOWN_ISSUES.csv',issues,['Issue_ID','Context','Issue_Type','Severity','State_ID','Province_ID','Evidence_Source','Observed_Fact','Historical_Conclusion','Disposition'])
    # Compare only province memberships against the installed vanilla, not resources.
    vanilla_defs={n.key:[prov(v) for v in values(n,'provinces')] for p,raw,ns in trees(args.game,args.game,'map_data/state_regions') for n in ns if n.key.startswith('STATE_')}
    different_memberships=[s for s,d in current['defs'].items() if set(d['provinces'])!=set(vanilla_defs.get(s,[]))]
    native_owners,native_pairs,_=own_inventory(args.game,args.game)
    changed_owners=[v for v in raster if current['owners'].get(v,[])!=native_owners.get(v,[])]
    candidate_changes=[v for v in raster if candidate and current['owners'].get(v,[])!=candidate['owners'].get(v,[])]
    def revision_owners(rev):
        raw=subprocess.check_output(['git','show',rev+':common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
        result=C.defaultdict(list)
        for n in walk(parse(raw)):
            if n.key.startswith('s:STATE_'):
                for c in n.children('create_state'):
                    for v in values(c,'owned_provinces'): result[prov(v)].append((n.key[2:],scalar(c.one('country')).removeprefix('c:')))
        return result
    before_collab=revision_owners('d909641^'); after_collab=revision_owners('d5b7421')
    prior_provinces=[v for v in set(before_collab)|set(after_collab) if set(before_collab[v])!=set(after_collab[v])]
    metrics=dict(date='1776-01-01',bitmap_dimensions=dimensions,bitmap_sha256=hashlib.sha256(bitmap.read_bytes()).hexdigest(),bitmap_unique_provinces=len(raster),land_states=len(current['land']),all_state_regions=len(current['defs']),land_provinces=len({v for d in current['land'].values() for v in d['provinces']}),sea_provinces=len(current['sea']),lake_provinces=len(current['lakes']),owner_state_pairs=len(current['pairs']),catalogue_rows=len(catalogue),catalogue_states=len({s for s,t in cat}),catalogue_pair_set_equal=not(cat_missing or cat_extra),baseline_rows=len(baseline),population_written=sum(current['population'].values()),region_pair_counts=dict(C.Counter(r['Region_ID'] for r in pairrows)),region_state_counts={r:len({x['State_ID'] for x in pairrows if x['Region_ID']==r}) for r in REGIONS},region_province_counts={r:sum(x['Province_Count'] for x in pairrows if x['Region_ID']==r) for r in REGIONS},region_country_tags={r:sorted({x['Owner_TAG'] for x in pairrows if x['Region_ID']==r}) for r in REGIONS},protected_pairs=sum(x['Protected_Specific_History']=='YES' for x in pairrows),changed_memberships_vs_vanilla=different_memberships,changed_owners_vs_vanilla_1836=len(changed_owners),changed_owner_states_vs_vanilla_1836=len({s for v in changed_owners for s,t in current['owners'].get(v,[])}),candidate_changed_provinces=candidate_changes,candidate_population_delta=(sum(candidate['population'].values())-sum(current['population'].values())) if candidate else None,issue_counts=dict(C.Counter((i['Context']+'/'+i['Severity']) for i in issues)),unassigned_bitmap_colors=sorted(current['unassigned']),main_orphan_selectors=current['orphans'],candidate_orphan_selectors=candidate['orphans'] if candidate else None)
    metrics['prior_collaborator_changed_owner_provinces']=len(prior_provinces)
    metrics['prior_collaborator_changed_owner_states']=sorted({s for v in prior_provinces for s,t in after_collab[v]})
    metrics['main_unique_incompatible_owner_provinces']=sum(len(set(os))>1 for os in current['owners'].values())
    metrics['main_repeated_same_owner_provinces']=sum(len(os)>1 and len(set(os))==1 for os in current['owners'].values())
    metrics['missing_base_localization_keys']=current['loc_missing']
    metrics['explicit_adjacency_rows']=current['adjacency_rows']
    (out/'MAP_1776_AUDIT_METRICS.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    assert len({(r['Province_ID'],r['State_ID'],r['Owner_TAG']) for r in baseline})==len(baseline)
    assert sum(metrics['region_pair_counts'].values())==len(current['pairs'])
    assert len({r['State_ID']:r['Region_ID'] for r in pairrows})==len(current['land'])
    assert all(len({r['Region_ID'] for r in pairrows if r['State_ID']==s})==1 for s in current['land'])
    assert len({r['Province_ID'] for r in baseline})==len(raster)
    print('PASS: full RGB inventory; unique rows; all actual owner/state pairs allocated; VEN/GEN included. Findings are documented, not repaired.')
    if args.strict and any(i['Severity'] in {'ERROR','BLOCKER'} for i in issues):
        raise SystemExit(2)

if __name__=='__main__': main()
