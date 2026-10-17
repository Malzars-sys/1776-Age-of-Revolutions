"""Scoped R9 correction and read-only imperial progress census.

Imports previous readers without running their generators. No Git mutations.
"""
import collections as C
import csv
import difflib
import json
import math
import re
import shutil
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import map2m_r8 as old

ROOT=old.ROOT;core=old.core;economy=old.economy
OUT=ROOT/'docs/reports/map/MAP2M/R9'
sys.path.insert(0,str(OUT.parent/'R7'))
import arbitration as seven

def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def capture():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'BASELINE.json').exists()
    previous=old.load('BASELINE.json');reference=dict(previous['hashes']);reference.update(old.load('MANIFEST.json')['installed_runtime'])
    hashes=economy.runtime_hashes();assert hashes==reference,'Workspace changed since R8: inspect, never restore'
    bmp=core.packed(ROOT/'map_data/provinces.png');inv=core.qa.inventory()
    assert [int((bmp==v).sum()) for v in [0x567452,0xE1A03A,0xEDB010,0xFCC7B7,0x41A021]]==[398,292,85,142,153]
    assert sum(r['count'] for r in inv['pops'])==835804980
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    prior_files={p.relative_to(ROOT).as_posix():core.sha(p) for p in (ROOT/'docs/reports/map').rglob('*') if p.is_file() and OUT not in p.parents}
    for rel in ['tools/map2m_r8.py','tools/test_map2m_r8.py']:prior_files[rel]=core.sha(ROOT/rel)
    dump('BASELINE.json',dict(inventory=inv,hashes=hashes,earlier_proofs=prior_files,registry=json.loads(core.active_registry_path().read_text()),
        git_head=old.prior.r2.head(),git_index_sha256=core.sha(ROOT/'.git/index'),bitmap_sha256=core.sha(ROOT/'map_data/provinces.png')))
    print('R9 captured current R8:',len(hashes),'runtime files;',len(prior_files),'old map artifacts protected')

def locators(bmp):
    folder='gfx/map/map_object_data';paths={p.name:p for p in (core.qa.GAME/folder).glob('generated_map_object_locators_*.txt')}
    paths.update({p.name:p for p in (ROOT/folder).glob('generated_map_object_locators_*.txt')})
    rows=[]
    for path in paths.values():
        raw=path.read_text(encoding='utf-8-sig')
        for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\}',raw):
            x=float(m[2]);y=bmp.shape[0]-float(m[4]);cx,cy=math.floor(x),math.floor(y)
            if 0<=cy<bmp.shape[0] and 0<=cx<bmp.shape[1]:
                rows.append(dict(Kind=path.stem.removeprefix('generated_map_object_locators_'),ID=int(m[1]),X=x,Y=y,RGB='x'+format(int(bmp[cy,cx]),'06X'),File=path.as_posix(),Line=raw.count('\n',0,m.start())+1))
    return rows

def diagnose():
    b=load('BASELINE.json');bmp,water,river,_=seven.p.physical_masks();owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    models=seven.w.load('TRANSFORMATIONS.json');cities=[]
    coordinates=[('Stralsund',13.082,54.309,'SWE'),('Greifswald',13.381,54.095,'SWE'),('Rugen interior',13.4,54.4,'SWE'),
        ('Wolgast',13.776,54.052,'SWE'),('Demmin',13.04,53.905,'PRU'),('Anklam',13.692,53.856,'PRU'),('Usedom interior',14.0,53.9,'PRU'),('Wollin interior',14.61,53.91,'PRU'),
        ('Walcz',16.47,53.27,'PRU'),('Kamin',17.52,53.53,'PRU'),('Bromberg',18.0,53.13,'PRU'),('Inowroclaw',18.26,52.795,'PRU'),
        ('Thorn diagnostic only',18.605,53.01,'PLC'),('Pila',16.738,53.151,'PRU'),('Gniezno',17.60,52.535,'PLC')]
    selected=models['selected_native']
    for name,lon,lat,wanted in coordinates:
        p=seven.r.forward(selected,[[lon,lat]])[0];x,y=map(math.floor,p);rgb='x'+format(int(bmp[y,x]),'06X')
        variants={k:seven.r.forward(dict(v,name=k),[[lon,lat]])[0].tolist() for k,v in models['tested_native'].items()}
        cities.append(dict(Name=name,Longitude=lon,Latitude=lat,X=float(p[0]),Y=float(p[1]),RGB=rgb,State_Owner=owners.get(rgb),Expected_owner=wanted,
            Native_locator=False,Certified_city_position=False,Variants=variants))
    hubs=locators(bmp);local=[r for r in hubs if 4380<r['X']<4445 and 710<r['Y']<780]
    csvout('PEENE_NATIVE_LOCATORS.csv',local)
    csvout('CITY_DIAGNOSTICS.csv',[{k:v for k,v in r.items() if k!='Variants'} for r in cities])
    dump('CITY_DIAGNOSTICS.json',cities)
    print('Actual local locators:',[(r['Kind'],r['ID'],round(r['X'],2),round(r['Y'],2),r['RGB']) for r in local])
    for r in cities:print(r['Name'],round(r['X'],2),round(r['Y'],2),r['RGB'],r['State_Owner'],'wanted',r['Expected_owner'])
    before=bmp
    for x,y in [(4409,735),(4410,735)]:print('Wolgast cell',x,y,hex(int(bmp[y,x])),'water',bool(water[y,x]),'river',bool(river[y,x]))
    # Thorn's actual native river layer alongside the province; no fitting.
    box=(4504,755,4532,782);im=old.panel(bmp,box,'THORN : RGB actuels, hydrographie native en cyan',owners,scale=24);d=ImageDraw.Draw(im)
    for y in range(box[1],box[3]):
        for x in range(box[0],box[2]):
            if river[y,x]:
                px,py=(x-box[0])*24,(y-box[1])*24+42;d.rectangle((px+7,py+7,px+16,py+16),fill='#00b5c7')
    for name,x,y in [('farm natif',4519.314941,772.104736),('diagnostic geo',cities[12]['X'],cities[12]['Y'])]:
        px,py=(x-box[0])*24,(y-box[1])*24+42;d.ellipse((px-5,py-5,px+5,py+5),fill='#b20e82');d.text((px+6,py),name,font=old.font(14),fill='black',stroke_width=2,stroke_fill='white')
    im.save(OUT/'THORN_NATIVE_REVIEW.png')
    for sid in sorted({r['key'][1] for r in b['inventory']['owners'] if r['key'][2]=='PRU'}):
        refs=[r['key'][0] for r in b['inventory']['owners'] if r['key'][1:]==[sid,'PRU']]
        registered={r['rgb'] for r in b['registry']}
        print('Prussia',sid,len(refs),'RGB;',sum(r in registered for r in refs),'registered')

def prepare_wolgast():
    b=load('BASELINE.json');assert economy.runtime_hashes()==b['hashes']
    before=core.packed(OUT/'provinces_before.png');_,water,_,_=seven.p.physical_masks()
    changes=[dict(Sector='WOLGAST',X=x,Y=735,RGB_before='xE1A03A',RGB_after='x567452',State_ID='STATE_POMERANIA',Owner_before='PRU',Owner_after='SWE',
        Decision='R9_GAME_SCALE_POLITICAL_APPROXIMATION',Basis='Wolgast Swedish1776; existing mainland corridor; frozen diagnostic models cover city vicinity; no native Wolgast hub',Applied=True) for x in [4409,4410]]
    assert all(before[r['Y'],r['X']]==0xE1A03A and not water[r['Y'],r['X']] for r in changes)
    after=old.prior.r2.expected_raster(before,changes)
    assert len(core.components(after==0x567452))==1 and len(core.components(after==0xE1A03A))==1
    # Fixed R5 models are only sensitivity diagnostics, not a new calibration.
    city=next(r for r in load('CITY_DIAGNOSTICS.json') if r['Name']=='Wolgast')
    assert all(after[math.floor(p[1]),math.floor(p[0])]==0x567452 for p in city['Variants'].values())
    source_area=sum(int((before==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_POMERANIA','PRU'])
    weights={'PRU':source_area-2,'SWE':2};allocations=[];originals={};files={}
    for path in economy.effective(ROOT,core.qa.GAME,'common/history/pops'):
        raw=path.read_text(encoding='utf-8-sig')
        try:region=core.region(raw,'STATE_POMERANIA','PRU')
        except StopIteration:continue
        edits=[];moved=[]
        for pop in region.children('create_pop'):
            size=pop.children('size')[0];counts=core.allocate(int(size.value),weights)
            edits.append((size.start,size.end,'size = '+str(counts['PRU'])))
            if counts['SWE']:moved.append(core.edits(raw[pop.start:pop.end],[(size.start-pop.start,size.end-pop.start,'size = '+str(counts['SWE']))]))
            allocations.append(dict(state='STATE_POMERANIA',culture=core.cw.scalar(pop.one('culture')),religion=core.cw.scalar(pop.one('religion','DEFAULT')),before=int(size.value),after=counts))
        updated=core.edits(raw,edits)
        for fragment in moved:updated=core.append(updated,'STATE_POMERANIA','SWE',fragment)
        a=raw.splitlines(True);z=updated.splitlines(True)
        for kind,a0,a1,z0,z1 in difflib.SequenceMatcher(a=a,b=z,autojunk=False).get_opcodes():
            if kind in ['insert','replace']:
                for i in range(z0,z1):
                    if not z[i].strip():z[i]='\n'
        updated=''.join(z);core.cw.parse(updated);assert path.is_relative_to(ROOT)
        rel=path.relative_to(ROOT).as_posix();originals[rel]=raw;files[rel]=updated
    buildings=[]
    for sid,tag,node,path in economy.declarations():
        if (sid,tag)!=('STATE_POMERANIA','PRU'):continue
        for n in core.cw.walk(node.children()):
            if n.key=='levels':
                split=core.allocate(int(n.value),weights);assert split['SWE']==0
                buildings.append(dict(building=node.one('building'),levels=int(n.value),allocation=split))
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('PLAN.json',dict(changes=changes,source_area=source_area,weights=weights,allocations=allocations,building_review=buildings,files=list(files),candidate_sha256=core.sha(OUT/'provinces_candidate.png')))
    dump('ORIGINAL_TEXT.json',originals);dump('EXPECTED_TEXT.json',files)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'HISTORY.patch')
    finally:core.OUT=oldout
    csvout('TERRITORIAL_CHANGES.csv',changes)
    fields=list(changes[0]);csvout('PRUSSIA_POLAND_CHANGES.csv',[],fields);csvout('PRUSSIAN_HRE_BORDER_CHANGES.csv',[],fields)
    print('Prepared2 Wolgast cells; population transferred',sum(r['after']['SWE'] for r in allocations),'weights',weights)

def install():
    b=load('BASELINE.json');plan=load('PLAN.json')
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    for rel,text in load('EXPECTED_TEXT.json').items():assert (ROOT/rel).read_text(encoding='utf-8-sig')==text
    hashes=economy.runtime_hashes();assert {p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}==set(plan['files'])
    assert core.sha(OUT/'provinces_candidate.png')==plan['candidate_sha256']
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png');print('Installed',plan['candidate_sha256'])

def validate():
    b=load('BASELINE.json');plan=load('PLAN.json');before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png');inv=core.qa.inventory();checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value)))
    check('Exact two authorized local cells only',np.array_equal(after,old.prior.r2.expected_raster(before,plan['changes'])) and int((before!=after).sum())==2)
    check('Installed candidate hash',core.sha(ROOT/'map_data/provinces.png')==plan['candidate_sha256'])
    check('Swedish400 / Prussian290 cells',int((after==0x567452).sum())==400 and int((after==0xE1A03A).sum())==290)
    check('All398 prior Swedish pixels retained',int((before==0x567452).sum())==398 and np.all(after[before==0x567452]==0x567452))
    check('All41 R8 transfers retained',all(after[r['Y'],r['X']]==0x567452 for r in old.load('PLAN.json')['changes']))
    for value in [0x567452,0xE1A03A]:check('Single four-connected component '+hex(value),len(core.components(after==value))==1)
    check('Rows740plus untouched',np.array_equal(before[740:],after[740:]))
    check('Usedom Wollin east approach untouched',np.array_equal(before[710:790,4411:4455],after[710:790,4411:4455]))
    check('No RGB added or removed',np.array_equal(np.unique(before),np.unique(after)))
    for rgb in [0xEDB010,0xFCC7B7,0x41A021,0x80A0A0,0x999CEE]:check('Unchanged protected footprint '+hex(rgb),np.array_equal(before==rgb,after==rgb))
    for name in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:
        check('Cumulative inventory preserved '+name,inv[name]==b['inventory'][name])
    check('World population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    expected=core.qa.counter(b['inventory']['regional_pop'])
    for r in plan['allocations']:
        rel='DEFAULT:'+r['culture'] if r['religion']=='DEFAULT' else r['religion'];n=r['after']['SWE']
        expected['STATE_POMERANIA','PRU',r['culture'],rel]-=n;expected['STATE_POMERANIA','SWE',r['culture'],rel]+=n
    check('Exact regional demographic delta',+expected==core.qa.counter(inv['regional_pop']))
    for rel,text in load('EXPECTED_TEXT.json').items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig')
        check('Exact parsed history '+rel,actual==text and bool(core.cw.parse(actual)))
        check('All demographic attributes and totals '+rel,old.profiles(actual)==old.profiles(load('ORIGINAL_TEXT.json')[rel]))
    hashes=economy.runtime_hashes();changed={p for p in hashes.keys()|b['hashes'].keys() if hashes.get(p)!=b['hashes'].get(p)}
    check('Only bitmap and Pomeranian pop history changed',changed==set(plan['files'])|{'map_data/provinces.png'})
    check('Imperial registry unchanged',json.loads(core.active_registry_path().read_text())==b['registry'])
    check('Inherited44 duplicates and12 badrefs unchanged',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('Brandenburg arms6',economy.totals(economy.declarations())['STATE_BRANDENBURG','PRU','building_arms_industry']==6)
    check('All old map evidence immutable',all(core.sha(ROOT/p)==h for p,h in b['earlier_proofs'].items()))
    check('HEAD unchanged',old.prior.r2.head()==b['git_head']);check('Index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    cityrows=[];owners={r['key'][0]:r['key'][2] for r in inv['owners']}
    for row in load('CITY_DIAGNOSTICS.json')[:8]:
        x,y=math.floor(row['X']),math.floor(row['Y']);rgb='x'+format(int(after[y,x]),'06X');observed=owners.get(rgb)
        cityrows.append(dict(Name=row['Name'],X=row['X'],Y=row['Y'],RGB=rgb,Owner=observed,Expected=row['Expected_owner'],Evidence='FROZEN_COARSE_DIAGNOSTIC_NOT_CERTIFIED_CITY_HOMOLOGUE'))
        check('Gameplay ownership diagnostic '+row['Name'],observed==row['Expected_owner'])
    wolgast=next(r for r in load('CITY_DIAGNOSTICS.json') if r['Name']=='Wolgast')
    check('All four frozen Wolgast estimates fall in SWE',all(after[math.floor(v[1]),math.floor(v[0])]==0x567452 for v in wolgast['Variants'].values()))
    csvout('PEENE_OWNERSHIP_CHECKS.csv',cityrows)
    a=core.qa.counter(b['inventory']['regional_pop']);z=core.qa.counter(inv['regional_pop']);rows=[]
    for k in sorted(a.keys()|z.keys()):
        if k[0] in ['STATE_POMERANIA','STATE_POSEN','STATE_WEST_PRUSSIA']:
            rows.append(dict(State_ID=k[0],Owner=k[1],Culture=k[2],Religion=k[3],Before=a[k],After=z[k],Difference=z[k]-a[k]))
    csvout('POPULATION_VALIDATION.csv',rows)
    result=dict(status='MAP-2M-R9_PARTIAL',static_validation='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
        peene_status='PEENE_GAMEPLAY_COMPLETE' if all(c['passed'] for c in checks) else 'PARTIAL',peene_completion_meaning='Practical political approximation; Wolgast area Swedish, no native Wolgast hub added; Peendamm omitted by resolution decision',
        engine_tested=False,runtime_status='PENDING_USER_NEW_GAME_AND_ONE_MONTH',R8_runtime_user_validated=False,historical_boundary_certified=False,
        changes=dict(wolgast=2,prussia_poland=0,thorn=0,other_prussian_hre_borders=0),population_transferred=235,world_population=835804980,
        functional_files=sorted(changed),new_RGBs=[],inherited_duplicate_RGBs=44,inherited_invalid_refs=12)
    dump('VALIDATION.json',result)
    print('R9',result['static_validation'],result['passed'],'/',result['total'],result['peene_status'])
    for c in checks:
        if not c['passed']:print('FAIL',c['name'])
    assert result['static_validation']=='PASS'

def previews():
    b=load('BASELINE.json');before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    for filename,box,cells,titles in [('PEENE_BEFORE_AFTER.png',(4392,726,4423,748),{(4409,735),(4410,735)},['AVANT R9 : 398 cellules SWE','APRES R9 : 400 cellules SWE, +2']),
        ('THORN_BEFORE_AFTER.png',(4506,758,4531,779),set(),['THORN AVANT R9 : PRU153','THORN APRES R9 : IDENTIQUE, aucun transfert'])]:
        panels=[]
        for bmp,title in zip([before,after],titles):panels.append(old.panel(bmp,box,title,owners,cells,22))
        out=Image.new('RGB',(panels[0].width*2,panels[0].height+75),'white')
        for i,im in enumerate(panels):out.paste(im,(i*im.width,0))
        d=ImageDraw.Draw(out)
        text='SWE jaune / PRU bleu / PLC rose. Orange : deux cellules contigues. Aucun hub Wolgast ajoute.' if filename.startswith('PEENE') else 'Avant et apres reels identiques. Ferme Torun non utilisee pour attribuer une province entiere.'
        d.text((8,out.height-65),text,font=old.font(16),fill='black')
        d.text((8,out.height-35),'Approximation de jeu, pas une limite geodesique certifiee.' if filename.startswith('PEENE') else 'La proposition historique de Thorn reste a arbitrer separement ; voir le diagnostic hydrographique.',font=old.font(16),fill='black')
        out.save(OUT/filename)

def audit_data():
    b=load('BASELINE.json');bmp=core.packed(ROOT/'map_data/provinces.png');owners=C.defaultdict(list)
    for r in b['inventory']['owners']:owners[r['key'][0]].append(r['key'][1:])
    registered={r['rgb']:r for r in b['registry']};values,counts=np.unique(bmp,return_counts=True);sizes=dict(zip(map(int,values),map(int,counts)))
    # Exact files and neighbouring ownerships, not inferred historical counties.
    rgbrows=[]
    for r in b['inventory']['owners']:
        rgb,sid,tag=r['key']
        if tag!='PRU':continue
        mask=bmp==int(rgb[1:],16);ys,xs=np.where(mask);adj=C.Counter()
        for x,y in zip(xs.tolist(),ys.tolist()):
            for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if 0<=ny<bmp.shape[0] and 0<=nx<bmp.shape[1] and not mask[ny,nx]:adj['x'+format(int(bmp[ny,nx]),'06X')]+=1
        rgbrows.append(dict(RGB=rgb,State_ID=sid,Owner=tag,Pixel_count=len(xs),Registered=rgb in registered,Registered_beneficiary=registered.get(rgb,{}).get('beneficiary',''),
            Registry_basis=registered.get(rgb,{}).get('basis',''),Actual_geometry_state=b['inventory']['geometry'].get(rgb,''),
            Adjacent_RGBs=';'.join(sorted(adj)),Adjacent_owners=';'.join(sorted({p[1] for v in adj for p in owners[v]})),
            Owner_reference_count=r['count']))
    csvout('PRUSSIAN_RGB_INVENTORY.csv',rgbrows)
    receipts=[]
    for path in (ROOT/'docs/reports/map/MAP2L').glob('RUNTIME_USER_VALIDATION*.json'):
        data=json.loads(path.read_text(encoding='utf-8'));receipts.append(dict(File=path.relative_to(ROOT).as_posix(),**data))
    dump('MANUAL_RECEIPTS_INDEX.json',receipts)
    import subprocess,os
    history=subprocess.check_output([core.GIT,'log','-8','--format=%h %s','--','docs/reports/map','map_data'],cwd=ROOT,text=True,encoding='utf-8',env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    (OUT/'GIT_READ_ONLY_HISTORY.txt').write_text(history,encoding='utf-8')
    # Preserve relevant original R2 conclusions verbatim in a compact audit.
    source=ROOT/'docs/reports/map/MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'
    r2rows=old.readcsv(source)
    audit_sids={r['State_ID'] for r in rgbrows}|{'STATE_SAXONY','STATE_HESSE','STATE_BAVARIA','STATE_BOHEMIA','STATE_MECKLENBURG','STATE_SCHLESWIG_HOLSTEIN'}
    selected=[{k:r.get(k,'') for k in ['Change_ID','State_ID','Historical_Polity_Name','Historical_Conclusion','Geographic_Location','Mapping_Status','Source_IDs','Unresolved_Uncertainty']} for r in r2rows if r.get('State_ID') in audit_sids]
    if selected:csvout('R2_REUSED_FINDINGS.csv',selected)
    totals=C.Counter()
    for r in b['inventory']['owners']:totals[r['key'][1],r['key'][2]]+=sizes.get(int(r['key'][0][1:],16),0)
    csvout('STATE_OWNER_PIXEL_INVENTORY.csv',[dict(State_ID=k[0],Owner=k[1],Pixels_in_declared_RGBs=v,Warning='Duplicate references retained, not unique sovereignty if inherited conflict') for k,v in sorted(totals.items()) if any(s['state']==k[0] for s in b['registry'])])
    print('Prussian',len(rgbrows),'RGB references;',len(selected),'R2 findings;',len(receipts),'manual receipts. Git log read only.')

def progress():
    b=load('BASELINE.json');catalog=load('REGION_CLASSIFICATION.json');rows=[]
    source=ROOT/'docs/reports/map/MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'
    r2=old.readcsv(source);covered={sid for r in catalog for sid in r['States']}
    for sid in sorted({r['state'] for r in b['registry']}-covered):
        findings=[r for r in r2 if r.get('State_ID')==sid]
        catalog.append(dict(Region='Autre secteur enregistré : '+sid,States=[sid],Reports=['MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'] if findings else [],
            Status='RESEARCHED_ONLY' if findings else 'UNKNOWN',Installed='Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9',Receipt='Aucune attestation régionale retrouvée',
            Open='Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction',Importance='À qualifier',Complexity='À qualifier',Dependencies='Délimiter le périmètre avant un futur lot ; pas de modification R9'))
    for r in catalog:
        refs=[v for v in b['inventory']['owners'] if v['key'][1] in r['States']]
        reports=r['Reports']
        assert all((ROOT/'docs/reports/map'/p).exists() for p in reports)
        rows.append(dict(Region=r['Region'],State_IDs=';'.join(r['States']),Current_owners=';'.join(sorted({v['key'][2] for v in refs})),
            Reports=';'.join(reports),Installed_corrections=r['Installed'],Manual_validation=r['Receipt'],Open_issues=r['Open'],Status=r['Status'],
            Historical_importance=r['Importance'],Estimated_complexity=r['Complexity'],Dependencies=r['Dependencies'],
            Caveat='Status covers named scope only; economic State_ID and registry membership are not historical border proof'))
    csvout('HRE_REGIONS_INVENTORY.csv',rows)
    counts=C.Counter(r['Status'] for r in rows)
    text=['# Avancement territorial du SERG — inventaire R9','',
        'Les statuts portent sur les sous-secteurs nommés, pas sur des régions entières implicitement certifiées. VALIDATED signifie seulement validation manuelle des modifications inspectées, sans test moteur automatisé ni certification historique. IMPLEMENTED signifie installé et statiquement contrôlé, sans reçu manuel spécifique suffisant. PARTIAL conserve les portions non résolues. RESEARCHED_ONLY ne signifie pas NOT_STARTED : une recherche existe, mais pas une véritable correction dédiée. AUDITED_ONLY décrit le contrôle R9 sans transfert. UNKNOWN signale les limites du corpus.','',
        'Le CSV couvre tous les State_ID du registre impérial actif, les sous-lots différenciés et le contexte extérieur prusso-polonais. Une ligne automatique « autre secteur enregistré » est volontairement prudente : elle ne transforme pas une attribution gelée de gameplay en travail cartographique achevé. Les territoires institutionnellement mixtes ne sont pas déclarés intégralement impériaux du seul fait de leur State_ID.','',
        '## Comptage des lignes, non des provinces','',*['- '+k+' : '+str(v) for k,v in sorted(counts.items())],'',
        '## Sous-secteurs et preuves','']
    for r in rows:text+=['### '+r['Region'],'',r['Status']+' — '+r['Installed_corrections']+'.',
        '', 'Validation : '+r['Manual_validation']+'.','', 'Reste ouvert : '+r['Open_issues']+'.','', 'Rapports : '+r['Reports']+'.','']
    text+=['## Prochain lot recommandé','',
        'Wismar–Poel–Neukloster, STATE_MECKLENBURG (75), exclusivement. La recherche R2-0132 établit le problème, et la propriété actuelle ne comporte aucun SWE (MEC1295, MST329). Aucun lot territorial dédié à ces possessions suédoises n’a été identifié. Ce choix ne signifie ni reprise de toute la Poméranie ni refonte de tout le Mecklembourg. Voir NEXT_HRE_REGION_RECOMMENDATION.md. Aucun travail de ce prochain lot n’est lancé.','',
        'Les acquisitions postérieures, les approximations restées ouvertes en Silésie, la Frise orientale et Thorn ne sont pas masquées par cette recommandation. Elles restent au registre des anomalies R9.']
    (OUT/'HRE_REGIONS_PROGRESS.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    dump('PROGRESS_SUMMARY.json',dict(rows=len(rows),statuses=dict(counts),all_registered_states_covered={r['state'] for r in b['registry']}<={s for r in rows for s in r['State_IDs'].split(';')},recommended='Wismar-Poel-Neukloster',next_lot_started=False))
    print('Progress:',len(rows),'scope rows;',dict(counts))

def thorn_arbitration():
    bmp=core.packed(ROOT/'map_data/provinces.png');rows=[]
    # Proposals only: R9 has no authority to pretend the uncertain point is exact.
    variants={'U1_URBAN_ABSTRACTION':[(4521,767)],'U2_TWO_CELL_ABSTRACTION':[(4520,767),(4521,767)]}
    for name,cells in variants.items():
        for x,y in cells:
            assert bmp[y,x]==0x41A021
            rows.append(dict(Variant=name,X=x,Y=y,RGB_before='x41A021',Proposed_owner='PLC',State_ID='STATE_WEST_PRUSSIA',
                Proposed_RGB='NOT_RESERVED',Evidence='Northern-bank city vicinity from frozen geographic diagnostic and Pfau city/riverside configuration; exact cell choice not certified',
                Status='PLAYER_ARBITRATION_REQUIRED_NOT_HISTORICAL_CADASTRE',Applied=False))
    csvout('THORN_ARBITRATION_PROPOSALS.csv',rows)
    b=load('BASELINE.json');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};box=(4512,762,4526,775);panels=[]
    for name,cells in variants.items():
        im=old.panel(bmp,box,name+' : NON APPLIQUE',owners,cells,30);d=ImageDraw.Draw(im)
        for x,y in cells:
            px,py=(x-box[0])*30,(y-box[1])*30+42;d.rectangle((px+3,py+3,px+26,py+26),fill='#e5a6a6',outline='#dc7015',width=2)
        panels.append(im)
    out=Image.new('RGB',(panels[0].width*2,panels[0].height+100),'white')
    for i,im in enumerate(panels):out.paste(im,(i*im.width,0))
    d=ImageDraw.Draw(out)
    for i,s in enumerate(['Propositions urbaines conditionnelles :1 ou2 cellules, pas les153.',
        'Pas de RGB reserve, ni population/batiment transfere. Farm Torun reste intact.',
        'Emplacement au pixel et possessions rurales non certifies : arbitrage requis.']):d.text((6,out.height-90+i*27),s,font=old.font(15),fill='black')
    out.save(OUT/'THORN_ARBITRATION.png')

def tests():
    import unittest,io,time
    suite=unittest.defaultTestLoader.loadTestsFromNames(['test_map2m_r9','test_map2l_registry']);stream=io.StringIO();start=time.perf_counter()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    (OUT/'UNIT_TESTS.log').write_text(stream.getvalue(),encoding='utf-8')
    dump('UNIT_TESTS.json',dict(tests=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors),failures=len(result.failures),errors=len(result.errors),elapsed_seconds=time.perf_counter()-start,engine_tests=False))
    print(stream.getvalue());assert result.wasSuccessful()

def finalize():
    required=['REPORT.md','WOLGAST_CORRECTION.md','PEENE_BEFORE_AFTER.png','PRUSSIA_POLAND_AUDIT.md','PRUSSIA_POLAND_CHANGES.csv',
        'THORN_CORRECTION.md','THORN_BEFORE_AFTER.png','PRUSSIAN_HRE_BORDERS_AUDIT.md','PRUSSIAN_HRE_BORDER_CHANGES.csv',
        'HRE_REGIONS_INVENTORY.csv','HRE_REGIONS_PROGRESS.md','NEXT_HRE_REGION_RECOMMENDATION.md','TERRITORIAL_CHANGES.csv',
        'POPULATION_VALIDATION.csv','VALIDATION.json','UNRESOLVED.csv','RUNTIME_TEST_PLAN.md']
    assert all((OUT/p).is_file() for p in required)
    v=load('VALIDATION.json');u=load('UNIT_TESTS.json');assert v['static_validation']=='PASS' and u['errors']==u['failures']==0
    v['unit_tests']=u;v['deliverables']=required;v['inventory']=load('PROGRESS_SUMMARY.json')
    v['colgrep']=dict(attempts=2,successful_agent_commands=1,first_failure='Sandbox index lock access denied',verified_returned_locations=5,
        telemetry='Successful agent-mode output returned paths; no captured GGUF/GPU loading banner, no independent GPU proof',
        repository_queries='One semantic question; retry for sandbox access, no redundant comparison search',elapsed_seconds=None,codex_task_tokens=None,quota_savings='Not measurable')
    dump('VALIDATION.json',v)
    b=load('BASELINE.json');assert old.prior.r2.head()==b['git_head'] and core.sha(ROOT/'.git/index')==b['git_index_sha256']
    assert all(core.sha(ROOT/p)==h for p,h in b['earlier_proofs'].items())
    for name in ['PEENE_BEFORE_AFTER.png','THORN_BEFORE_AFTER.png','THORN_NATIVE_REVIEW.png','THORN_ARBITRATION.png']:
        with Image.open(OUT/name) as im:im.verify()
    files={p.relative_to(ROOT).as_posix():core.sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    for rel in ['tools/map2m_r9.py','tools/test_map2m_r9.py']:files[rel]=core.sha(ROOT/rel)
    dump('MANIFEST.json',dict(algorithm='SHA256',files=files,functional_files={rel:core.sha(ROOT/rel) for rel in v['functional_files']},git_head=b['git_head'],git_index_sha256=b['git_index_sha256']))
    print('R9 complete delivery:',v['passed'],'static checks;',u['passed'],'unit tests. Overall PARTIAL; no engine validation.')

if __name__=='__main__':globals()[sys.argv[1]]()
