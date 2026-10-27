"""Ionian possessions / Epirote outposts, 1776: bounded political cores.

No coast, vanilla, Git, SERG tracking, common recipe or technology writes.
Eight outpost pixels are a political approximation; Kythera uses an entire
separate pre-existing island component. Neither is a cadastral reconstruction.
"""
import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import world1776_balkans03 as b

ROOT=b.ROOT;OUT=b.OUT;LOT=OUT/'BALKANS-04'
STATES='common/history/states/00_states.txt'
POPS='common/history/pops/01_south_europe.txt'
REGIONS='map_data/state_regions/01_south_europe.txt'
TERRAIN='map_data/province_terrains.txt'
BMP='map_data/provinces.png'
NEW='common/history/buildings/1776_world_b04_ionian_posts.txt'
EDIT=[STATES,POPS,REGIONS,TERRAIN,BMP]
PLAN=[
 {'name':'Butrinto','rgb':'xE8D211','parent':'x7BE071','state':'STATE_ALBANIA','pixels':[[4553,1147],[4553,1148]],'population':500,'geo_approx':[20.020,39.744]},
 {'name':'Parga','rgb':'xE8D212','parent':'x8050E0','state':'STATE_THESSALIA','pixels':[[4559,1158],[4559,1159]],'population':3000,'geo_approx':[20.399,39.282]},
 {'name':'Preveza','rgb':'xE8D213','parent':'x8050E0','state':'STATE_THESSALIA','pixels':[[4569,1167],[4569,1168]],'population':1700,'geo_approx':[20.752,38.961]},
 {'name':'Vonitsa','rgb':'xE8D214','parent':'x518791','state':'STATE_ATTICA','pixels':[[4571,1169],[4571,1170]],'population':1000,'geo_approx':[20.884,38.920]},
]
if (LOT/'KYTHERA_SELECTION.json').exists():
    PLAN.append({'name':'Cerigo / Kythera','rgb':'xE8D215','parent':'x0055D7','state':'STATE_PELOPONNESE',
                 'pixels':json.loads((LOT/'KYTHERA_SELECTION.json').read_text('utf8'))['pixels'],
                 'population':7500,'geo_approx':[22.986,36.237],'kind':'existing_island'})
SIDS=list(dict.fromkeys(p['state'] for p in PLAN))

def dump(name,value):
    (LOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((LOT/name).read_text('utf8'))
def rgb(c):return tuple(bytes.fromhex(c[1:]))
def read(p):return b.a.raw(p)
def total_pop():
    total=0
    for p in b.tech.effective('common/history/pops'):
        total+=sum(int(n.one('size')) for n in b.walk(b.parse(read(p))) if n.key=='create_pop')
    return total

def grouped_plan(plan=None):
    rows=PLAN if plan is None else plan
    return {sid:[p for p in rows if p['state']==sid] for sid in dict.fromkeys(p['state'] for p in rows)}

def added_buildings():
    text=['# Existing Venetian maritime outposts; anchorage capacity is a game abstraction.','BUILDINGS = {']
    for sid in SIDS:
        text.append(f''' s:{sid} = {{ region_state:VEN = {{
  create_building = {{ building = "building_port"
   add_ownership = {{ country = {{ country = "c:VEN" levels = 1 }} }}
   reserves = 1 activate_production_methods = {{ "pm_anchorage" }}
  }}
 }} }}''')
    text.append(''' # One level represents the existing Corfiot defensive complex, not a count of buildings.
 s:STATE_IONIAN_ISLANDS = { region_state:VEN = {
  create_building = { building = "building_naval_fortification"
   add_ownership = { country = { country = "c:VEN" levels = 1 } }
   reserves = 1 activate_production_methods = { "pm_naval_fortification_basic" }
  }
 } }
}''')
    return '\n'.join(text)+'\n'

def transform(old,plan=None):
    selected=PLAN if plan is None else plan
    new={}
    text=old[STATES];ops=[]
    for sid,posts in grouped_plan(selected).items():
        n=b.one(text,'s:'+sid)
        assert all(c.one('country')!='c:VEN' for c in n.children('create_state'))
        values=' '.join(p['rgb'] for p in posts)
        add=f'\n\t\t# BALKANS-04: fortified Venetian coastal cores, not their Ottoman hinterland.\n\t\tcreate_state = {{ country = c:VEN owned_provinces = {{ {values} }} }}\n\t'
        ops.append((n.end-1,n.end-1,add))
    new[STATES]=b.edits(text,ops)
    text=old[REGIONS];ops=[]
    for sid,posts in grouped_plan(selected).items():
        n=b.one(text,sid);provinces=n.children('provinces')[0]
        ops.append((provinces.end-1,provinces.end-1,' '+' '.join('"'+p['rgb']+'"' for p in posts)+' '))
    new[REGIONS]=b.edits(text,ops)
    terrain={n.key:n.value for n in b.parse(old[TERRAIN])}
    new[TERRAIN]=old[TERRAIN].rstrip()+'\n\n# BALKANS-04: terrains inherited from the unchanged land parents.\n'+''.join(p['rgb']+' = '+terrain[p['parent']]+'\n' for p in selected)
    text=old[POPS];ops=[]
    for sid,posts in grouped_plan(selected).items():
        n=b.one(text,'s:'+sid);tur=n.children('region_state:TUR')[0]
        pools=[p for p in tur.children('create_pop') if p.one('culture')=='greek']
        assert len(pools)==1
        pop=pools[0];size=pop.children('size')[0];amount=sum(p['population'] for p in posts)
        assert int(size.value)>amount
        ops.append((size.start,size.end,'size = '+str(int(size.value)-amount)))
        # Copy every demographic attribute, including implicit religion/profession.
        copied=text[pop.start:pop.end];relative=(size.start-pop.start,size.end-pop.start)
        copied=copied[:relative[0]]+'size = '+str(amount)+copied[relative[1]:]
        ops.append((n.end-1,n.end-1,'\n\t\tregion_state:VEN = {\n\t\t\t'+copied+'\n\t\t}\n\t'))
    new[POPS]=b.edits(text,ops)
    return new

def inventory():
    owners,_,odd=b.geo.own_inventory(ROOT,b.a.GAME)
    return {'world_population':total_pop(),'owners':{k:[list(x) for x in v] for k,v in owners.items()},'odd':odd,'git':b.a.git_state()}

def review_external_serg():
    """Record a reviewed peer-tracking update in WORLD, never in SERG."""
    base=load('APPLY_BASELINE.json')
    changed={r:{'before':h,'observed':b.a.sha(ROOT/r)} for r,h in base['SERG_proofs'].items() if b.a.sha(ROOT/r)!=h}
    assert {Path(r).name for r in changed}=={'BLOCKERS.md','NEXT_ACTION.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json','ROADMAP_STATE.json'}
    sources=['docs/reports/map/SERG_CLOSURE/SC1-ORTENBURG/TEST_REVIEW.json',
             'docs/reports/map/SERG_CLOSURE/SC1-ORTENBURG/RUNTIME_USER_ATTESTATION_2026_10_25.json']
    assert all((ROOT/r).exists() for r in sources)
    history=read(ROOT/'docs/reports/map/SERG_CLOSURE/PROGRESS_HISTORY.md')
    assert 'SERG-RM-0042' in history and 'SCOPED_ORTENBURG_RUNTIME_USER_VALIDATION' in history
    snapshots={}
    for r in list(changed)+sources:
        dest=LOT/'external_snapshots'/r;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,dest)
        snapshots[dest.relative_to(LOT).as_posix()]=b.a.sha(dest)
    dump('EXTERNAL_SERG_UPDATE.json',{'date':'2026-10-25','event':'SERG-RM-0040/0041/0042; separate Ortenburg installation, tests and scoped user acceptance',
        'files':changed,'snapshots':snapshots,'sources':{r:b.a.sha(ROOT/r) for r in sources},
        'WORLD_human_validation_added':False,'SERG_writes_by_this_task':0})
    print('Five external SERG tracking updates preserved and archived in WORLD only.')

def apply():
    assert not (LOT/'APPLY_BASELINE.json').exists(),'Already applied/captured; inspect the receipt instead of replaying.'
    assert not (ROOT/NEW).exists()
    # Read current versions, not an obsolete research-entry snapshot.
    text={r:read(ROOT/r) for r in EDIT if r!=BMP};changed=transform(text)
    before=np.array(Image.open(ROOT/BMP).convert('RGB'));planned=before.copy()
    packed=(before[:,:,0].astype(np.uint32)<<16)|(before[:,:,1].astype(np.uint32)<<8)|before[:,:,2]
    for p in PLAN:
        assert not np.any(packed==int(p['rgb'][1:],16))
        for x,y in p['pixels']:
            assert tuple(before[y,x])==rgb(p['parent']),(p['name'],x,y)
            planned[y,x]=rgb(p['rgb'])
    base={'owned':{r:b.a.sha(ROOT/r) for r in EDIT},'before':inventory(),'protected':{},'SERG_proofs':{},'prior_proofs':{},'new':[NEW]}
    for folder in ['common','events','gui','gfx','localization','map_data']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():
                r=p.relative_to(ROOT).as_posix()
                if r not in EDIT:base['protected'][r]=b.a.sha(p)
    for p in (ROOT/'docs/reports/map/SERG_CLOSURE').rglob('*'):
        if p.is_file():base['SERG_proofs'][p.relative_to(ROOT).as_posix()]=b.a.sha(p)
    for lot in ['BALKANS-01','BALKANS-02','BALKANS-03']:
        for p in (OUT/lot).rglob('*'):
            if p.is_file():base['prior_proofs'][p.relative_to(ROOT).as_posix()]=b.a.sha(p)
    for r in EDIT:
        dest=LOT/'apply_inputs'/r;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,dest)
    dump('APPLY_BASELINE.json',base);dump('PIXEL_PATCH.json',PLAN)
    assert all(b.a.sha(ROOT/r)==h for r,h in base['owned'].items()),'Shared input changed: reread and adapt before writing.'
    for r,t in changed.items():
        p=ROOT/r;prefix=b'\xef\xbb\xbf' if p.read_bytes().startswith(b'\xef\xbb\xbf') else b''
        p.write_bytes(prefix+t.encode('utf8'))
    assert b.a.sha(ROOT/BMP)==base['owned'][BMP],'Bitmap changed concurrently; preserve it and reconcile.'
    Image.fromarray(planned).save(ROOT/BMP)
    p=ROOT/NEW;p.write_text(added_buildings(),encoding='utf8',newline='\n')
    dump('FILES_MODIFIED.json',[{'file':r,'before':base['owned'].get(r),'after':b.a.sha(ROOT/r)} for r in EDIT+[NEW]])
    dump('AFTER.json',inventory())
    print('Installed bounded Ionian corrections; no new country.')

def extend_kythera():
    """Add the separately identified island to the installed four-post version.

    Operates on current texts and bitmap; requires their exact current receipts.
    No complete file is restored from the earlier baseline.
    """
    assert len(PLAN)==5 and not (LOT/'KYTHERA_EXTENSION.json').exists()
    receipts=load('FILES_MODIFIED.json')
    assert all(b.a.sha(ROOT/e['file'])==e['after'] for e in receipts),'Current owned files changed: reconcile before extension.'
    old={r:read(ROOT/r) for r in EDIT if r!=BMP};new=transform(old,[PLAN[-1]])
    before_hash={r:b.a.sha(ROOT/r) for r in EDIT+[NEW]}
    for r in EDIT+[NEW]:
        dest=LOT/'kythera_extension_inputs'/r;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,dest)
    image=np.array(Image.open(ROOT/BMP).convert('RGB'))
    for x,y in PLAN[-1]['pixels']:
        assert tuple(image[y,x])==rgb(PLAN[-1]['parent']);image[y,x]=rgb(PLAN[-1]['rgb'])
    assert all(b.a.sha(ROOT/r)==h for r,h in before_hash.items())
    for r,t in new.items():
        p=ROOT/r;prefix=b'\xef\xbb\xbf' if p.read_bytes().startswith(b'\xef\xbb\xbf') else b'';p.write_bytes(prefix+t.encode('utf8'))
    Image.fromarray(image).save(ROOT/BMP)
    (ROOT/NEW).write_text(added_buildings(),encoding='utf8',newline='\n')
    dump('KYTHERA_EXTENSION.json',{'before':before_hash,'after':{r:b.a.sha(ROOT/r) for r in before_hash},'pixels':33,'population':7500,'scope':'Existing Kythera component only; fresh current-version patch.'})
    base=load('APPLY_BASELINE.json')
    dump('FILES_MODIFIED.json',[{'file':r,'before':base['owned'].get(r),'after':b.a.sha(ROOT/r)} for r in EDIT+[NEW]])
    dump('PIXEL_PATCH.json',PLAN);dump('AFTER.json',inventory())
    print('Added the existing separate Kythera island: 33 pixels; 7500 POPs reallocated.')

def validate():
    base=load('APPLY_BASELINE.json');after=inventory();checks=[]
    def check(k,v,detail=None):checks.append({'check':k,'passed':bool(v),'detail':detail})
    old={r:read(LOT/'apply_inputs'/r) for r in EDIT if r!=BMP}
    expected=transform(transform(old,PLAN[:-1]),[PLAN[-1]]) if (LOT/'KYTHERA_EXTENSION.json').exists() else transform(old)
    for r,t in {**expected,NEW:added_buildings()}.items():
        check('exact_targeted_patch.'+r,read(ROOT/r)==t)
        check('parse.'+r,bool(b.parse(read(ROOT/r))))
    for r in [STATES,POPS,REGIONS]:
        def exterior(text):
            ops=[]
            for sid in SIDS:
                n=b.one(text,('s:' if r!=REGIONS else '')+sid);ops.append((n.start,n.end,'<SCOPED_REGION>'))
            return b.edits(text,ops)
        check('outside_target_regions_identical.'+r,exterior(old[r])==exterior(read(ROOT/r)))
    before=np.array(Image.open(LOT/'apply_inputs'/BMP).convert('RGB'));now=np.array(Image.open(ROOT/BMP).convert('RGB'));planned=before.copy()
    for p in PLAN:
        for x,y in p['pixels']:planned[y,x]=rgb(p['rgb'])
    check('only_planned_land_pixels_changed',np.array_equal(planned,now))
    check('RGB_dimensions_preserved',Image.open(ROOT/BMP).mode=='RGB' and Image.open(ROOT/BMP).size==(8192,3616))
    expected_owners=dict(base['before']['owners']);expected_owners.update({p['rgb']:[[p['state'],'VEN']] for p in PLAN})
    check('all_old_owners_preserved_only_four_new_VEN_keys',after['owners']==expected_owners)
    check('world_population_conserved',after['world_population']==base['before']['world_population'],after['world_population'])
    def demographic_profile(text):
        out=Counter()
        for n in b.walk(b.parse(text)):
            if n.key=='create_pop':out[(n.one('culture'),n.one('religion'),n.one('pop_type'))]+=int(n.one('size'))
        return out
    check('all_culture_religion_profession_totals_preserved',demographic_profile(old[POPS])==demographic_profile(read(ROOT/POPS)))
    check('git_identity_unchanged',after['git']==base['before']['git'])
    # This coastline's sea colour is present in the pre-existing map and is not recoloured.
    sea_rgb=rgb('x3BDCFA')
    region_objects=b.a.catalog('map_data/state_regions');terrain={n.key:n.value for n in b.parse(read(ROOT/TERRAIN))}
    ledger=[]
    for p in PLAN:
        c=p['rgb'];pixels=p['pixels'];sid=p['state']
        members=[s for s,(n,_) in region_objects.items() if c in [b.geo.prov(x) for x in b.geo.values(n,'provinces')]]
        check('unique_region.'+c,members==[sid])
        check('parent_terrain_inherited.'+c,terrain[c]==terrain[p['parent']])
        check('original_land_parent.'+c,all(tuple(before[y,x])==rgb(p['parent']) for x,y in pixels))
        check('coastal_access.'+c,any(tuple(before[yy,xx])==sea_rgb for x,y in pixels for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]))
        if p.get('kind')=='existing_island':
            todo={tuple(x) for x in pixels};seed=todo.pop();q=[seed]
            while q:
                x,y=q.pop()
                for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if v in todo:todo.remove(v);q.append(v)
            check('whole_connected_Kythera_component.'+c,len(pixels)==33 and not todo)
            # The component is separated from all remaining land of its parent.
            selected={tuple(v) for v in pixels}
            check('Kythera_does_not_transfer_mainland',all(tuple(before[yy,xx])!=rgb(p['parent']) for x,y in pixels for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if (xx,yy) not in selected))
        else:check('two_connected_pixels.'+c,len(pixels)==2 and sum(abs(pixels[0][i]-pixels[1][i]) for i in [0,1])==1)
        check('parent_retains_pixels.'+c,bool(np.any(np.all(now==rgb(p['parent']),axis=2))))
    for sid,posts in grouped_plan().items():
        amount=sum(p['population'] for p in posts)
        was=b.one(old[POPS],'s:'+sid).children('region_state:TUR')[0]
        current=b.one(read(ROOT/POPS),'s:'+sid)
        def popcount(n):return sum(int(p.one('size')) for p in n.children('create_pop'))
        newtur=current.children('region_state:TUR')[0];ven=current.children('region_state:VEN')[0]
        check('local_population_conserved.'+sid,popcount(was)==popcount(newtur)+popcount(ven))
        check('VEN_reallocation.'+sid,popcount(ven)==amount)
        check('TUR_decrease.'+sid,popcount(was)-popcount(newtur)==amount)
        oldgreek=next(p for p in was.children('create_pop') if p.one('culture')=='greek');newgreek=ven.children('create_pop')[0]
        check('demographic_attributes_preserved.'+sid,b.normalized([x for x in oldgreek.children() if x.key!='size'])==b.normalized([x for x in newgreek.children() if x.key!='size']))
        oldother=[p for p in was.children('create_pop') if p.one('culture')!='greek'];newother=[p for p in newtur.children('create_pop') if p.one('culture')!='greek']
        check('all_other_populations_identical.'+sid,b.normalized(oldother)==b.normalized(newother))
        ledger.append({'state':sid,'total_before':popcount(was),'total_after':popcount(newtur)+popcount(ven),'VEN_before':0,'VEN_after':amount,'TUR_after':popcount(newtur),'delta':0})
        # Resources, arable land, traits and native hubs do not change.
        def region_without_provinces(t):return b.normalized([x for x in b.one(t,sid).children() if x.key!='provinces'])
        check('resources_hubs_traits_preserved.'+sid,region_without_provinces(old[REGIONS])==region_without_provinces(read(ROOT/REGIONS)))
    dump('POPULATION_LEDGER.json',{'world_before':base['before']['world_population'],'world_after':after['world_population'],'world_delta':0,'politically_reallocated':sum(p['population'] for p in PLAN),'rows':ledger,'posts':[{'name':p['name'],'population':p['population']} for p in PLAN],'status':'GAME_CALIBRATION_NOT_1776_CENSUS'})
    grants={n.value for n in b.one(read(ROOT/'common/history/countries/ven - venetia.txt'),'c:VEN').children('add_technology_researched')}
    technologies,_,_=b.tech.objects('common/technology/technologies')
    check('VEN_27_initial_technologies_preserved',len(grants)==27)
    check('VEN_technology_ids_resolve',grants<=set(technologies))
    check('VEN_prerequisites_closed',all(set(b.a.ids(technologies[k],'unlocking_technologies'))<=grants for k in grants))
    buildings=b.a.catalog('common/buildings');groups=b.a.catalog('common/production_method_groups');methods=b.a.catalog('common/production_methods')
    recipes={}
    for building,pm in [('building_port','pm_anchorage'),('building_naval_fortification','pm_naval_fortification_basic')]:
        n=buildings[building][0];legal=set()
        check('building_gate.'+building,set(b.a.ids(n,'unlocking_technologies'))<=grants)
        for g in b.a.ids(n,'production_method_groups'):
            check('PMG_exists.'+g,g in groups)
            if g in groups:legal.update(b.a.ids(groups[g][0],'production_methods'))
        check('PM_legal.'+pm,pm in legal and pm in methods)
        check('PM_gate.'+pm,set(b.a.ids(methods[pm][0],'unlocking_technologies'))<=grants)
        recipes[pm]=b.a.recipe(methods[pm][0])
        check('positive_jobs.'+pm,all(float(v)>=0 for v in recipes[pm]['jobs'].values()))
    newassets=[n for n in b.walk(b.parse(added_buildings())) if n.key=='create_building']
    check('one_anchorage_per_new_substate_one_Corfiot_fort',Counter(n.one('building').strip('"') for n in newassets)=={'building_port':len(SIDS),'building_naval_fortification':1})
    check('all_new_levels_one',all(next(n for n in b.walk([p]) if n.key=='levels').value=='1' for p in newassets))
    check('Ionians_existing_cells_remain_VEN',all(after['owners'].get(c)==[['STATE_IONIAN_ISLANDS','VEN']] for c in ['x4B79CA','x405060']))
    check('Ionians_POPs_and_existing_assets_unchanged',b.normalized([b.one(old[POPS],'s:STATE_IONIAN_ISLANDS')])==b.normalized([b.one(read(ROOT/POPS),'s:STATE_IONIAN_ISLANDS')]))
    check('B01_Cyclades_unchanged',all(after['owners'].get(c)==[['STATE_WEST_AEGEAN_ISLANDS','TUR']] for c in ['x6090A0','x6960A0']))
    rag=json.loads((OUT/'BALKANS-02/PIXEL_PATCH.json').read_text('utf8'))
    for label,p in rag.items():check('B02_pixels_preserved.'+label,all(tuple(now[y,x])==rgb(p['rgb']) for x,y in p['pixels']))
    for e in json.loads((OUT/'BALKANS-03/FILES_MODIFIED.json').read_text('utf8')):
        check('B03_functional_receipt.'+e['file'],b.a.sha(ROOT/e['file'])==e['after'])
    externals={r:{'before':h,'observed':b.a.sha(ROOT/r) if (ROOT/r).exists() else None} for r,h in base['protected'].items() if not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h}
    serg={r:{'before':h,'observed':b.a.sha(ROOT/r) if (ROOT/r).exists() else None} for r,h in base['SERG_proofs'].items() if not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h}
    prior=[r for r,h in base['prior_proofs'].items() if not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h]
    check('protected_gameplay_outside_lot_unchanged',not externals,list(externals))
    peer=load('EXTERNAL_SERG_UPDATE.json') if (LOT/'EXTERNAL_SERG_UPDATE.json').exists() else {}
    external_serg_ok=(serg==peer.get('files') and all(b.a.sha(LOT/r)==h for r,h in peer.get('snapshots',{}).items())
                     and all(b.a.sha(ROOT/r)==h for r,h in peer.get('sources',{}).items()))
    check('SERG_proofs_preserved_or_reviewed_peer_update',not serg or external_serg_ok,list(serg))
    check('prior_WORLD_proofs_unchanged',not prior,prior)
    dump('CONCURRENT_CHANGES.json',{'external_gameplay':externals,'SERG_external_updates':serg,'prior_proofs_changed':prior,'scope':'Five shared current files; four coastal cores plus the separate existing Kythera island; no old baseline restored.'})
    dump('STARTING_TECH_CHECK.json',{'tag':'VEN','technologies':sorted(grants),'count':len(grants),'new_country':False,'new_technology_grants':[],'recipes':recipes,'common_recipes_modified':False})
    result={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','geometry':'POLITICAL_CORE_APPROXIMATION_NOT_CADASTRAL'}
    dump('VALIDATION.json',result);print(json.dumps({k:v for k,v in result.items() if k!='checks'}));print([c for c in checks if not c['passed']]);return result

def render():
    before=np.array(Image.open(LOT/'apply_inputs'/BMP).convert('RGB'));after=np.array(Image.open(ROOT/BMP).convert('RGB'))
    old=load('APPLY_BASELINE.json')['before']['owners'];new=inventory()['owners']
    canvas=Image.new('RGB',(1420,930),'#18212a');d=ImageDraw.Draw(canvas);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for j,(a,owners,title) in enumerate([(before,old,'Avant'),(after,new,'Après : quatre noyaux côtiers')]):
        crop=a[1140:1185,4539:4581];panel=np.full_like(crop,(31,56,76))
        for c,who in owners.items():
            if c.startswith('x') and who:panel[np.all(crop==rgb(c),axis=2)]={'VEN':(93,165,206),'TUR':(197,163,103)}.get(who[0][1],(125,128,131))
        canvas.paste(Image.fromarray(panel).resize((672,720),Image.Resampling.NEAREST),(25+710*j,70));d.text((25+710*j,25),title,font=f,fill='white')
        for p in PLAN:
            x,y=p['pixels'][0];px=25+710*j+(x-4539+.5)*16;py=70+(y-1140+.5)*16
            d.ellipse((px-3,py-3,px+3,py+3),fill='white');d.text((px+7,py-8),p['name'],font=f,fill='white',stroke_width=1,stroke_fill='black')
    d.text((25,825),'Bleu : VEN · Ocre : TUR · Huit pixels pour les quatre postes ; côtes et arrière-pays conservés.',font=f,fill='white')
    d.text((25,865),'Approximation politique des places fortifiées ; aucune frontière cadastrale de 1776 certifiée.',font=f,fill='white')
    canvas.save(LOT/'IONIAN_EPIRUS_BEFORE_AFTER.png')
    if len(PLAN)==5:
        canvas=Image.new('RGB',(1400,750),'#18212a');d=ImageDraw.Draw(canvas)
        for j,(a,owners,title) in enumerate([(before,old,'Avant : Cérigo sous TUR'),(after,new,'Après : Cérigo sous VEN')]):
            crop=a[1225:1248,4593:4640];panel=np.full_like(crop,(31,56,76))
            for c,who in owners.items():
                if who:panel[np.all(crop==rgb(c),axis=2)]={'VEN':(93,165,206),'TUR':(197,163,103)}.get(who[0][1],(125,128,131))
            canvas.paste(Image.fromarray(panel).resize((658,460),Image.Resampling.NEAREST),(20+700*j,75));d.text((20+700*j,25),title,font=f,fill='white')
        d.text((25,590),'33 pixels de l’île existante transférés ; continent et îlot oriental non identifié conservés sous TUR.',font=f,fill='white')
        d.text((25,635),'Aucune côte, terre ou liaison maritime créée. Région native : STATE_PELOPONNESE.',font=f,fill='white')
        canvas.save(LOT/'KYTHERA_BEFORE_AFTER.png')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--extend-kythera',action='store_true');p.add_argument('--review-external-serg',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--map',action='store_true');args=p.parse_args()
    if args.apply:apply()
    if args.extend_kythera:extend_kythera()
    if args.review_external_serg:review_external_serg()
    if args.validate:
        result=validate()
        if result['status']!='PASS':raise SystemExit(1)
    if args.map:render()
