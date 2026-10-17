"""MAP-2O: bounded East Frisian correction, immutable current-worktree baseline."""
from pathlib import Path
import collections as C
import csv
import json
import math
import re
import shutil
import subprocess
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2l_mainz as core
import start_buildings_2026_10_15 as economy
import map2m_r9 as r9

ROOT = core.ROOT
OUT = ROOT / 'docs/reports/map/MAP2O'
BOX = (4238, 728, 4310, 785)
FONT = 'C:/Windows/Fonts/arial.ttf'
PARENT = 'xF9DCA2'
REGION = 'STATE_HANNOVER'


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def csvout(name, rows, fields=None):
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def capture():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'BASELINE.json').exists(), 'Never replace an immutable baseline'
    inv = core.qa.inventory()
    assert sum(r['count'] for r in inv['pops']) == 835804980
    assert len(inv['duplicates']) == 44 and len(inv['errors']) == 12
    reference = ROOT / 'docs/reports/map/MAP2N/COMPLETION/INSTALLED_MANIFEST.json'
    installed = json.loads(reference.read_text(encoding='utf-8'))
    assert all(core.sha(ROOT / p) == h for p, h in installed['functional_files'].items())
    shutil.copy2(ROOT / 'map_data/provinces.png', OUT / 'provinces_before.png')
    originals = {p: (ROOT / p).read_text(encoding='utf-8-sig') for p in
        ['common/history/states/00_states.txt', 'common/history/pops/00_west_europe.txt',
         'map_data/state_regions/00_west_europe.txt', 'map_data/province_terrains.txt']}
    dump('BASELINE.json', {'inventory': inv, 'hashes': economy.runtime_hashes(), 'originals': originals,
        'registry': json.loads(core.active_registry_path().read_text(encoding='utf-8')),
        'bitmap_sha256': core.sha(ROOT / 'map_data/provinces.png'),
        'git_head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'git_index_sha256': core.sha(ROOT / '.git/index'), 'map2n_manifest': installed,
        'bridge_and_prototype_hashes': {p.relative_to(ROOT).as_posix(): core.sha(p)
            for folder in ['docs/prototypes/REGIONAL_INFRASTRUCTURE/mod','tools/vic3-diagnostic-bridge']
            for p in (ROOT / folder).rglob('*') if p.is_file() and '.tmp' not in p.parts},
        'registry_tool_sha256': core.sha(ROOT / 'tools/map2l_registry.py')})
    print('Captured current MAP2N-accepted workspace; no old baseline or Git mutation')


def panel(bitmap, owners, box, title, scale=15, labels=True):
    x0,y0,x1,y1=box; local=bitmap[y0:y1,x0:x1]
    palette={'HAN':'#c7c6ac','PRU':'#599dc6','OLD':'#e7ad79','NET':'#e2ca66','WPM':'#8cb389',
             'WPO':'#dfb661','ANH':'#a6d4c6','BRU':'#d798a5'}
    from PIL import ImageColor
    rgb=np.full((*local.shape,3),(198,221,230),dtype=np.uint8)
    for color in np.unique(local):
        tag=owners.get('x'+format(int(color),'06X'),['',''])[1]
        if tag: rgb[local==color]=ImageColor.getrgb(palette.get(tag,'#c9b6d9'))
    edges=np.zeros(local.shape,bool);edges[1:]|=local[1:]!=local[:-1];edges[:,1:]|=local[:,1:]!=local[:,:-1]
    rgb[edges]=(65,65,65)
    image=Image.new('RGB',((x1-x0)*scale,(y1-y0)*scale+55),'white')
    image.paste(Image.fromarray(rgb).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST),(0,40))
    d=ImageDraw.Draw(image);font=ImageFont.truetype(FONT,12)
    d.text((5,8),title,font=ImageFont.truetype(FONT,17),fill='black')
    if labels:
        for color in np.unique(local):
            key='x'+format(int(color),'06X'); identity=owners.get(key)
            if not identity: continue
            yy,xx=np.where(local==color)
            d.text((int(np.median(xx))*scale,int(np.median(yy))*scale+40),key[1:]+' '+identity[1],font=font,fill='black',stroke_width=2,stroke_fill='white')
    for x in range(math.ceil(x0/5)*5,x1,5):
        d.line(((x-x0)*scale,40,(x-x0)*scale,image.height-15),fill='#a5a5a5')
        d.text(((x-x0)*scale,25),str(x),font=font,fill='black')
    for y in range(math.ceil(y0/5)*5,y1,5):
        d.line((0,(y-y0)*scale+40,image.width,(y-y0)*scale+40),fill='#a5a5a5')
        d.text((0,(y-y0)*scale+40),str(y),font=font,fill='black',stroke_width=1,stroke_fill='white')
    return image


def audit():
    base=load('BASELINE.json'); bitmap=core.packed(OUT/'provinces_before.png')
    owners={r['key'][0]:r['key'][1:] for r in base['inventory']['owners']}
    rows=[];cells=[];x0,y0,x1,y1=BOX
    for value in np.unique(bitmap[y0:y1,x0:x1]):
        rgb='x'+format(int(value),'06X'); identity=owners.get(rgb)
        if not identity:continue
        yy,xx=np.where(bitmap==value)
        rows.append(dict(RGB=rgb,State_ID=identity[0],Owner_TAG=identity[1],Pixels=len(xx),
            X_min=int(xx.min()),X_max=int(xx.max()),Y_min=int(yy.min()),Y_max=int(yy.max()),
            Registered=any(r['rgb']==rgb for r in base['registry'])))
        if identity[1]=='HAN':
            for y,x in zip(yy,xx):
                if x0<=x<x1 and y0<=y<y1:cells.append(dict(X=int(x),Y=int(y),RGB=rgb,State_ID=identity[0],Owner_TAG='HAN'))
    csvout('PRUSSIAN_TERRITORY_AUDIT.csv',rows)
    csvout('HAN_SECTOR_CELL_INVENTORY.csv',cells)
    locators=[r for r in r9.locators(bitmap) if x0<=r['X']<x1 and y0<=r['Y']<y1]
    dump('NATIVE_LOCATORS.json',locators)
    panel(bitmap,owners,BOX,'AVANT MAP2O : proprietaires et RGB reels').save(OUT/'CURRENT_OWNERS.png')
    for name in ['rivers.png','heightmap.png']:
        paths=[ROOT/'map_data'/name, core.qa.GAME/'map_data'/name]
        p=next((v for v in paths if v.exists()),None)
        if p:
            image=Image.open(p)
            image.crop(BOX).resize(((BOX[2]-BOX[0])*15,(BOX[3]-BOX[1])*15),Image.Resampling.NEAREST).save(OUT/('NATIVE_'+name))
    for name,path,box in [('SCHENK_NORTH','docs/reports/map/MAP2L/RHINE_WESTPHALIA/SCHENK_WESTPHALIA_1710_FULL.jpg',(300,0,1700,780)),
                          ('VAUGONDY_NORTH','docs/reports/map/MAP2L/RHINE_WESTPHALIA/VAUGONDY_NORTH.png',None)]:
        image=Image.open(ROOT/path)
        if box:image=image.crop(box)
        image.thumbnail((1600,1500));image.save(OUT/(name+'_READING.png'))
    print('Provinces',rows)
    print('Locators',locators)
    print('Regional pops',[r for r in base['inventory']['regional_pop'] if r['key'][0]==REGION])


def read(rel):
    return (ROOT/rel).read_text(encoding='utf-8-sig')


def prepare():
    """Existing-province macro correction; no unverified southern pixel tracing."""
    b=load('BASELINE.json');assert economy.runtime_hashes()==b['hashes']
    before=core.packed(OUT/'provinces_before.png')
    assert int((before==int(PARENT[1:],16)).sum())==319
    originals=dict(b['originals']);files={}
    rel='common/history/states/00_states.txt';raw=originals[rel];s=core.state(raw,REGION)
    src=next(n for n in s.children('create_state') if n.one('country')=='c:HAN')
    dst=next(n for n in s.children('create_state') if n.one('country')=='c:PRU')
    field=src.children('owned_provinces')[0];target=dst.children('owned_provinces')[0]
    assert core.values(src,'owned_provinces').count(PARENT)==1 and PARENT not in core.values(dst,'owned_provinces')
    files[rel]=core.edits(raw,[(field.start,field.end,raw[field.start:field.end].replace(' '+PARENT,'')),
                             (target.end-1,target.end-1,PARENT+' ')])
    # No building, formation or economic owner changes: the existing regional
    # owner states remain alive. Only population changes administrative region.
    rel='common/history/pops/00_west_europe.txt';raw=originals[rel];rs=core.region(raw,REGION,'HAN')
    han_rgbs=[int(v['key'][0][1:],16) for v in b['inventory']['owners'] if v['key'][1:]==[REGION,'HAN']]
    area=int(np.isin(before,han_rgbs).sum());weights={'HAN':area-319,'PRU':319}
    ops=[];moved=[];allocations=[]
    for pop in rs.children('create_pop'):
        sn=pop.children('size')[0];n=int(sn.value);a=core.allocate(n,weights);assert a['HAN']>0
        ops.append((sn.start,sn.end,'size = '+str(a['HAN'])))
        if a['PRU']:
            moved.append(core.edits(raw[pop.start:pop.end],[(sn.start-pop.start,sn.end-pop.start,'size = '+str(a['PRU']))]))
        allocations.append(dict(culture=pop.one('culture'),religion=pop.one('religion','DEFAULT'),before=n,after=a,
            state=REGION,source='HAN',profile=pop.one('culture')+'/'+pop.one('religion','DEFAULT'),kind='population'))
    files[rel]=core.append(core.edits(raw,ops),REGION,'PRU','\n'.join(moved))
    old=b['registry'];assert [r['beneficiary'] for r in old if r['rgb']==PARENT]==['HAN']
    ledger=[dict(r,beneficiary='PRU',basis='MAP2O: Prussian East Frisian coastal core since 1744; existing-province generalization B; southern fringe unresolved, see MAP2O/REPORT.md.') if r['rgb']==PARENT else r for r in old]
    rel=core.active_registry_path().relative_to(ROOT).as_posix();files[rel]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    # Narrow generated-clause edits preserve all unrelated imperial fixes.
    rel='common/scripted_triggers/1776_imperial_constitution.txt';raw=read(rel);originals[rel]=raw
    oldclause='AND = { c:HAN ?= { aor1776_hre_member = yes } NOT = { owner = c:HAN } p:'+PARENT+'.state ?= this }'
    assert raw.count(oldclause)==1
    files[rel]=raw.replace(oldclause,oldclause.replace('c:HAN','c:PRU'))
    rel='common/scripted_effects/1776_imperial_constitution.txt';raw=read(rel);originals[rel]=raw;lines=raw.splitlines(keepends=True);changes=[]
    for i,line in enumerate(lines):
        if PARENT in line and 'c:HAN' in line:
            changes.append(i+1);lines[i]=line.replace('c:HAN','c:PRU')
    # Snapshot owner is on the following line, also keyed by this exact RGB.
    assert len(changes)==5,changes
    effect_lines=changes[:]
    files[rel]=''.join(lines)
    for lang in ['english','french']:
        rel=f'localization/{lang}/1776_imperial_feedback_l_{lang}.yml';raw=read(rel);originals[rel]=raw
        files[rel]=feedback_text(raw)
    migration=dict(geometry='MAP2O/GEOMETRY.json',replaced_regions=[REGION],previous=[r for r in old if r['state']==REGION],updated=[r for r in ledger if r['state']==REGION],
        new_members=[],free_cities=[],new_provinces=[],region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],
        limitation='Only existing xF9DCA2 title changes HAN to PRU. No new imperial land, bloc member, or southern/jurisdictional fringe claimed.')
    dump('REGISTRY_MIGRATION.json',migration)
    yy,xx=np.where(before==int(PARENT[1:],16));cells=[[int(x),int(y)] for y,x in zip(yy,xx)]
    assignments=[dict(rgb=PARENT,parent_rgb=PARENT,state=REGION,owner='PRU',previous_owner='HAN',pixels=319,cells=cells)]
    changes=[dict(X=x,Y=y,RGB_before=PARENT,RGB_after=PARENT,State_ID=REGION,Owner_before='HAN',Owner_after='PRU',Class='B',Source='Schenk1710 territorial envelope + GStA1744-1806 sovereignty') for x,y in cells]
    dump('GEOMETRY.json',dict(parents=[PARENT],assignments=assignments,new_provinces=[],changes=changes,candidate_sha256=b['bitmap_sha256']))
    dump('ORIGINAL_TEXT.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('PLAN.json',dict(files=list(files),text_files=list(files),new_RGBs=[],ownership_cells=319,recolored_cells=0,weights=weights,allocations=allocations,
        changes=changes,imperial_effect_lines=effect_lines,historical_class='B',southern_fringe_status='C_UNCHANGED'))
    csvout('TERRITORIAL_CHANGES.csv',changes)
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'HISTORY.patch')
    finally:core.OUT=oldout
    print('Prepared existing coastal province:319 owner cells,0 recolored cells; population weights',weights,'moved',sum(r['after']['PRU'] for r in allocations))


def previews(inv):
    b=load('BASELINE.json');bitmap=core.packed(ROOT/'map_data/provinces.png')
    old={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    new={r['key'][0]:r['key'][1:] for r in inv['owners']}
    panels=[panel(bitmap,old,BOX,'AVANT : noyau cotier HAN'),panel(bitmap,new,BOX,'APRES : noyau cotier PRU (B)')]
    image=Image.new('RGB',(panels[0].width*2,panels[0].height+65),'white')
    for i,p in enumerate(panels):image.paste(p,(i*p.width,0))
    d=ImageDraw.Draw(image);d.text((8,image.height-50),'Bleu : PRU | gris : HAN | orange : OLD | jaune : NET | vert : Munster. Memes limites RGB.',font=ImageFont.truetype(FONT,18),fill='black')
    d.text((8,image.height-25),'319 cellules changent de souverain ; 0 pixel recolore. Marges meridionales non validees, non transferees.',font=ImageFont.truetype(FONT,17),fill='black')
    image.save(OUT/'EAST_FRISIA_BEFORE_AFTER.png')
    image=panel(bitmap,new,(4249,741,4277,770),'EMDEN : province cotiere prussienne, simplification B',scale=26)
    d=ImageDraw.Draw(image);x,y=4256.644043,748.069336;px,py=(x-4249)*26,(y-741)*26+40
    d.ellipse((px-5,py-5,px+5,py+5),fill='red');d.text((px+8,py+2),'Hub portuaire natif, pas centre historique certifie',font=ImageFont.truetype(FONT,15),fill='black',stroke_width=1,stroke_fill='white')
    image.save(OUT/'EMDEN_DETAIL.png')


def metadata():
    """Add cumulative-schema fields without changing the installed proposal."""
    b=load('BASELINE.json');p=load('PLAN.json');g=load('GEOMETRY.json');m=load('REGISTRY_MIGRATION.json')
    p['files']=p['text_files'];g['candidate_sha256']=b['bitmap_sha256'];m['geometry']='MAP2O/GEOMETRY.json'
    for a in p['allocations']:
        a.update(state=REGION,source='HAN',profile=a['culture']+'/'+a['religion'],kind='population')
    for name,value in [('PLAN.json',p),('GEOMETRY.json',g),('REGISTRY_MIGRATION.json',m)]:dump(name,value)
    shutil.copyfile(ROOT/'map_data/province_terrains.txt',OUT/'province_terrains_candidate.txt')
    receipt=json.loads((ROOT/'docs/reports/map/MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json').read_text(encoding='utf-8'))
    dump('MAP2N_ACCEPTANCE_ACKNOWLEDGMENT.json',dict(date='2026-10-16',lot='MAP2N',status=receipt['status'],source_receipt='docs/reports/map/MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json',
        coverage=receipt['coverage'],duration=receipt['duration'],automated_engine_test=False,engine_logs_provided=False,new_MAP2O_runtime_validated=False))


def feedback_text(raw):
    lines=raw.splitlines(keepends=True);hits=[]
    for i,line in enumerate(lines):
        if 'aor1776_hre_province_'+PARENT+':0 ' in line:
            assert line.count("GetCountry('HAN')")==1
            lines[i]=line.replace("GetCountry('HAN')","GetCountry('PRU')");hits.append(i)
    assert len(hits)==1
    return ''.join(lines)


def feedback_prepare():
    b=load('BASELINE.json');p=load('PLAN.json');originals=load('ORIGINAL_TEXT.json');expected=load('EXPECTED_TEXT.json');files={}
    for lang in ['english','french']:
        rel=f'localization/{lang}/1776_imperial_feedback_l_{lang}.yml'
        assert core.sha(ROOT/rel)==b['hashes'][rel]
        raw=read(rel);originals[rel]=raw;files[rel]=feedback_text(raw);expected[rel]=files[rel]
        assert rel not in p['text_files'];p['text_files'].append(rel)
    p['files']=p['text_files']
    for name,value in [('PLAN.json',p),('ORIGINAL_TEXT.json',originals),('EXPECTED_TEXT.json',expected)]:dump(name,value)
    oldout=core.OUT
    try:core.OUT=OUT;core.emit(files,'FEEDBACK.patch')
    finally:core.OUT=oldout


def compiler_check():
    import map2k_imperial_system as compiler
    folder=OUT/'COMPILER_CHECK';folder.mkdir(exist_ok=True);compiler.OUT=folder
    files=compiler.compile_system();rows=[]
    for rel,text in files.items():
        equal=read(rel).rstrip('\r\n')==text.lstrip('\ufeff').rstrip('\r\n')
        rows.append(dict(file=rel,matches_current_compiler=equal))
    dump('COMPILER_VALIDATION.json',dict(status='PASS' if all(r['matches_current_compiler'] for r in rows) else 'DRIFT_REQUIRES_REVIEW',runtime_files_modified=False,checks=rows))
    print(json.dumps(rows,indent=2))


def unit_tests():
    command=[sys.executable,'-B','-X','utf8','-m','unittest','test_map2l_registry','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']
    started=time.perf_counter();result=subprocess.run(command,cwd=ROOT/'tools',capture_output=True,text=True)
    output=result.stdout+result.stderr;found=re.search(r'Ran (\d+) tests in ([\d.]+)s',output)
    dump('UNIT_TEST_VALIDATION.json',dict(date='2026-10-16',status='PASS' if result.returncode==0 else 'FAIL',kind='STATIC_PYTHON_TESTS_NOT_GAME_ENGINE',command=command,working_directory='tools',
        tests=int(found[1]) if found else None,test_runner_elapsed_seconds=float(found[2]) if found else None,wall_seconds=time.perf_counter()-started,exit_code=result.returncode,result=output,original_baselines_modified=False))
    print(output);assert result.returncode==0


def validate():
    b=load('BASELINE.json');p=load('PLAN.json');inv=core.qa.inventory();checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    check('Bitmap byte-exact and all world pixels unchanged',core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256'] and np.array_equal(before,after))
    check('Existing coastal province319 cells retained',int((after==int(PARENT[1:],16)).sum())==319)
    check('Coastal core is a single connected land province',len(core.components(after==int(PARENT[1:],16)))==1)
    check('No added or removed RGB',set(np.unique(before))==set(np.unique(after)) and p['new_RGBs']==[])
    expected=core.qa.counter(b['inventory']['owners']);expected[PARENT,REGION,'HAN']-=1;expected[PARENT,REGION,'PRU']+=1
    check('Exactly one owner change; all other provinces and State_ID retained',+expected==core.qa.counter(inv['owners']))
    check('Each of319 cells now uniquely Prussian in Hannover',[(r['key'],r['count']) for r in inv['owners'] if r['key'][0]==PARENT]==[([PARENT,REGION,'PRU'],1)])
    for field in ['states','state_types','geometry','countries','pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:
        check('Exact preservation '+field,inv[field]==b['inventory'][field])
    check('World population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for a in p['allocations']:
        religion=a['religion'] if a['religion']!='DEFAULT' else 'DEFAULT:'+a['culture'];n=a['after']['PRU']
        regional[REGION,'HAN',a['culture'],religion]-=n;regional[REGION,'PRU',a['culture'],religion]+=n
        check('Deterministic conserved population '+a['culture']+'/'+religion,a['after']==core.allocate(a['before'],p['weights']) and sum(a['after'].values())==a['before'])
    check('Exact regional culture/religion redistribution; no other populations altered',+regional==core.qa.counter(inv['regional_pop']))
    newreg=json.loads(core.active_registry_path().read_text(encoding='utf-8'))
    check('504 registered provinces; same RGB/state extent',len(newreg)==len(b['registry'])==504 and {(r['rgb'],r['state']) for r in newreg}=={(r['rgb'],r['state']) for r in b['registry']})
    check('Only Emden beneficiary changes to PRU',[(r['rgb'],r['beneficiary']) for r in newreg if r not in b['registry']]==[(PARENT,'PRU')])
    from map2l_registry import approved_lot_dirs,apply_territorial_migrations,territorial_holder_overrides,additional_members,rightful_holder_condition
    check('Explicit MAP2O migration registered last',approved_lot_dirs()[-1]==OUT)
    prior=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf-8'))['de_jure_registry']
    belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf-8'))
    regions={r['state'] for r in belgian['assignments']}
    prior=[r for r in prior if r['state'] not in regions]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in belgian['assignments']]
    # MAP2L also added Piedmont via a separate approved extension.
    from map2l_registry import approved_territorial_extensions
    prior=prior+approved_territorial_extensions()
    check('Cumulative registry migrations reproduce installed ledger',apply_territorial_migrations(prior)==newreg)
    check('Prussian rights require imperial membership; no new member',rightful_holder_condition(next(r for r in newreg if r['rgb']==PARENT))=='c:PRU ?= { aor1776_hre_member = yes }' and 'PRU' not in additional_members())
    check('Swedish limited rights and no membership retained',territorial_holder_overrides()['SWE']=={'STATE_POMERANIA','STATE_MECKLENBURG'} and 'SWE' not in additional_members())
    rights=np.isin(after,[int(r['rgb'][1:],16) for r in newreg])
    mask=np.array(Image.open(ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds').convert('RGBA'))[:,:,0]>0
    check('Imperial map mask still exactly matches registered extent',np.array_equal(mask,rights[708:1220,4152:4664]))
    expected_text=load('EXPECTED_TEXT.json')
    for rel,text in expected_text.items():
        check('Exact reviewed content '+rel,read(rel).rstrip('\r\n')==text.lstrip('\ufeff').rstrip('\r\n'))
        if rel.endswith('.txt'):check('Valid parsed syntax '+rel,bool(core.cw.parse(read(rel))))
    # Native locators and hub definitions are unchanged; only their owner changes.
    locs=r9.locators(after);oldloc=load('NATIVE_LOCATORS.json')
    check('Native locators physically/RGB unchanged',all(r in locs for r in oldloc))
    ports=[r for r in locs if r['Kind']=='port' and r['ID']==69]
    check('Emden port locator on transferred coastal province',len(ports)==1 and 'x'+format(int(after[math.floor(ports[0]['Y']),math.floor(ports[0]['X'])]),'06X')==PARENT)
    current=economy.runtime_hashes();changed={rel for rel,h in current.items() if b['hashes'].get(rel)!=h}
    check('Only six reviewed runtime text files modified',changed==set(p['text_files'])&set(current) and len(changed)==6 and set(current)==set(b['hashes']))
    for rel in ['map_data/state_regions/00_west_europe.txt','map_data/province_terrains.txt','map_data/heightmap.png','map_data/packed_heightmap.png','map_data/rivers.png','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/interface/journal_entries/aor1776_hre_registered_map.dds']:
        check('Preserved physical/resource/map dependency '+rel,current[rel]==b['hashes'][rel])
    for rel,h in b['map2n_manifest']['functional_files'].items():
        if rel not in changed:check('MAP2N file byte-exact '+rel,current.get(rel)==h)
    # Shared files are checked against the new immutable baseline and exact
    # reviewed deltas, not silently substituted in the old MAP2N baseline.
    for region in ['STATE_POMERANIA','STATE_MECKLENBURG','STATE_BRANDENBURG','STATE_WURTTEMBERG','STATE_BAVARIA','STATE_SAXONY']:
        check('Accepted historical state block unchanged '+region,core.qa.norm(core.state(read('common/history/states/00_states.txt'),region))==core.qa.norm(core.state(b['originals']['common/history/states/00_states.txt'],region)))
    for rel,h in b['bridge_and_prototype_hashes'].items():check('Bridge/prototype retained '+rel,core.sha(ROOT/rel)==h)
    check('44 inherited duplicates and12 invalid refs only',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('Git HEAD/index untouched',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    rows=[];oldpop=core.qa.counter(b['inventory']['regional_pop']);newpop=core.qa.counter(inv['regional_pop'])
    for key in sorted(set(oldpop)|set(newpop)):
        if key[0]==REGION:
            rows.append(dict(State_ID=key[0],Owner_TAG=key[1],Culture=key[2],Religion=key[3],Before=oldpop[key],After=newpop[key],Delta=newpop[key]-oldpop[key]))
    csvout('POPULATION_VALIDATION.csv',rows)
    dump('IMPERIAL_REGISTRY_VALIDATION.json',dict(status='PASS' if all(r['passed'] for r in checks if any(w in r['name'] for w in ['registry','registered','rights','beneficiary','member','mask'])) else 'FAIL',before=len(b['registry']),after=len(newreg),changed_beneficiary={PARENT:['HAN','PRU']},new_members=[],extent_changed=False))
    result=dict(status='MAP2O_PARTIAL',static_status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,
        implemented_sectors=['EMDEN_COASTAL_EAST_FRISIA_CORE'],ownership_cells=319,recolored_cells=0,new_RGBs=[],population_world=835804980,population_reallocated=sum(a['after']['PRU'] for a in p['allocations']),
        historical_class='B_EXISTING_PROVINCE_GENERALIZATION',southern_fringe='C_UNCHANGED',engine_tested=False,runtime_user_validated=False,
        prior_MAP2N_status='PASS_RUNTIME_USER_VALIDATED',automated_engine_test=False,functional_files_changed=sorted(changed),preexisting_duplicates=inv['duplicates'],preexisting_invalid_references=inv['errors'],new_errors=[] if inv['errors']==b['inventory']['errors'] else inv['errors'],
        colgrep_agent_calls=1,colgrep_elapsed_seconds=None,codex_token_counter_available=False,exact_quota_savings_measurable=False)
    dump('VALIDATION.json',result);dump('INSTALLED_MANIFEST.json',dict(functional_files={rel:current[rel] for rel in changed},imperial_registry_sha256=core.sha(core.active_registry_path()),baseline='BASELINE.json',status=result['static_status']))
    previews(inv)
    print(json.dumps({k:v for k,v in result.items() if k not in ['checks','preexisting_duplicates','preexisting_invalid_references']},ensure_ascii=False,indent=2))
    for r in checks:
        if not r['passed']:print('FAILED:',r['name'])
    assert all(r['passed'] for r in checks),'MAP2O static validation failed'


if __name__=='__main__':
    {'capture':capture,'audit':audit,'prepare':prepare,'validate':validate,'metadata':metadata,'compiler':compiler_check,'feedback':feedback_prepare,'tests':unit_tests}[sys.argv[1]]()
