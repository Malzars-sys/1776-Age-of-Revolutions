"""Focused, source-driven Budjak review. No game writes in inspect mode."""
import json, hashlib, collections as C, sys, re, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2c_work import packed, source_bitmap, geo_data
from map_1776_audit import effective

ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2D/BUDJAK_REVIEW'
PARENT=OUT.parent
REGIONS={'STATE_BESSARABIA','STATE_MOLDAVIA','STATE_CHERSON','STATE_DOBRUDJA'}
TOUCHED=['common/history/states/00_states.txt','common/history/pops/15_russia.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt','map_data/provinces.png']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def components(mask,conn=4):
    lab=np.zeros(mask.shape,np.int32); remaining=set(map(tuple,np.argwhere(mask)));n=0
    steps=[(-1,0),(1,0),(0,-1),(0,1)]+([(-1,-1),(-1,1),(1,-1),(1,1)] if conn==8 else [])
    while remaining:
        n+=1;p=remaining.pop();todo=[p];lab[p]=n
        while todo:
            y,x=todo.pop()
            for dy,dx in steps:
                q=(y+dy,x+dx)
                if q in remaining:remaining.remove(q);todo.append(q);lab[q]=n
    counts=np.bincount(lab.ravel()); order=sorted(range(1,n+1),key=lambda k:-counts[k])
    return lab,order
def binary_dilation(m):
    out=m.copy();out[1:]|=m[:-1];out[:-1]|=m[1:];out[:,1:]|=m[:,:-1];out[:,:-1]|=m[:,1:]
    return out
def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'GEOMETRY.json').exists(),'Do not replace the pre-review geometry evidence'
    before=json.loads((PARENT/'MAP2D_BASELINE.json').read_text(encoding='utf-8'))['inventory']
    inv=qa.inventory(); rgb=packed(source_bitmap());defs,hubs,names=geo_data()
    owners={r['key'][0]:r['key'][2] for r in inv['owners']}
    old={r['key'][0]:r['key'][2] for r in before['owners']}
    regions={v:s for s,vs in defs.items() for v in vs}
    rows=[]
    # Every Bessarabian province, every CRI province in neighboring sectors,
    # and the Ottoman coastal exceptions. No selection on favorable geometry.
    selected=sorted(v for v,s in regions.items() if s in REGIONS and (s=='STATE_BESSARABIA' or owners.get(v)=='CRI' or (s=='STATE_CHERSON' and owners.get(v)=='TUR')))
    for v in selected:
        ys,xs=np.where(rgb==int(v[1:],16)); x0,y0,x1,y1=int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)
        local=rgb[max(0,y0-1):y1+1,max(0,x0-1):x1+1];mask=local==int(v[1:],16)
        lab,order=components(mask); _,order8=components(mask,8);parts=[]
        for i,k in enumerate(order,1):
            m=lab==k; y,x=np.where(m);nb=binary_dilation(m)&~mask
            neighbors=sorted('x%06X'%int(c) for c in np.unique(local[nb]) if 'x%06X'%int(c) in regions)
            parts.append({'component':i,'pixels':int(m.sum()),'bbox':[int(x.min()+x0-1),int(y.min()+y0-1),int(x.max()+x0-1),int(y.max()+y0-1)],'neighbors':neighbors,'neighbor_owners':sorted({owners.get(n,'UNOWNED') for n in neighbors})})
        hh=[s+'/'+kind+'/'+names.get('HUB_NAME_'+s+'_'+kind,'') for s,h in hubs.items() for kind,p in h.items() if p==v]
        rows.append({'rgb':v,'region':regions[v],'pre_map2d_owner':old.get(v,''),'owner':owners.get(v,''),'pixels':int(len(xs)),'components_4':len(order),'components_8':len(order8),'parts':parts,'hubs':hh})
    # Country connectivity in an ample crop, independently of province components.
    box=(4660,870,4860,1010);x0,y0,x1,y1=box;crop=rgb[y0:y1,x0:x1]
    cri=np.isin(crop,[int(v[1:],16) for v,o in owners.items() if o=='CRI']);lab,order=components(cri)
    cri_groups=[]
    for i,k in enumerate(order,1):
        m=lab==k;y,x=np.where(m);ids=sorted('x%06X'%int(c) for c in np.unique(crop[m]))
        cri_groups.append({'component':i,'pixels':int(m.sum()),'rgb':ids,'bbox':[int(x.min()+x0),int(y.min()+y0),int(x.max()+x0),int(y.max()+y0)],'touches_crop_edge':bool(m[0].any() or m[-1].any() or m[:,0].any() or m[:,-1].any())})
    data={'rows':rows,'cri_groups_crop':cri_groups,'bitmap_same_as_pre_map2d':sha(source_bitmap())==sha(PARENT/'provinces_before.png')}
    (OUT/'GEOMETRY.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    # Hashes only, not a fresh full snapshot. Existing checkpoint holds source bytes.
    baseline=OUT/'REVIEW_BASELINE.json'
    if not baseline.exists():
        paths=[p for folder in ['common','events','gfx','map_data','localization','.metadata'] for p in (ROOT/folder).rglob('*') if p.is_file()]
        baseline.write_text(json.dumps({'hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in paths},'inventory':inv},ensure_ascii=False),encoding='utf-8')
    preview(rgb,owners,'before')
    for r in rows:print(r['rgb'],r['region'],r['pre_map2d_owner']+'>'+r['owner'],r['pixels'],'parts',r['components_4'],r['components_8'],r['parts'],r['hubs'])
    print('CRI country groups',cri_groups)
def preview(rgb,owners,name):
    box=(4670,880,4845,1008);x0,y0,x1,y1=box;crop=rgb[y0:y1,x0:x1]
    colors={'MOL':(92,177,115),'TUR':(207,94,89),'CRI':(224,180,82),'RUS':(98,133,208),'AUS':(169,137,195),'PLC':(181,178,154),'WAL':(113,193,183)}
    canvas=np.zeros((*crop.shape,3),np.uint8)
    for c in np.unique(crop):canvas[crop==c]=colors.get(owners.get('x%06X'%int(c),'SEA'),(47,63,73))
    bd=np.zeros(crop.shape,bool);bd[1:]|=crop[1:]!=crop[:-1];bd[:,1:]|=crop[:,1:]!=crop[:,:-1];canvas[bd]=(28,30,35)
    scale=8;im=Image.fromarray(canvas).resize((crop.shape[1]*scale,crop.shape[0]*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for c in np.unique(crop):
        v='x%06X'%int(c);mask=crop==c;lab,order=components(mask)
        for k in order:
            y,x=np.where(lab==k)
            if len(x)>=15 and owners.get(v) in ['CRI','MOL','TUR']:d.text((x.mean()*scale,y.mean()*scale),v+' '+owners[v],anchor='mm',font=font,fill='white',stroke_width=1,stroke_fill='black')
    im.save(OUT/(name+'.png'))
def prepare():
    backup=OUT/'DIFFERENTIAL_BACKUP';backup.mkdir(exist_ok=True)
    manifest=[]
    for path in TOUCHED:
        p=ROOT/path
        if path=='map_data/provinces.png':
            original=PARENT/'provinces_before.png';assert sha(p)==sha(original)
            dest=original
        else:
            dest=backup/path;dest.parent.mkdir(parents=True,exist_ok=True)
            assert not dest.exists(),'Do not overwrite differential originals'
            shutil.copyfile(p,dest)
        manifest.append({'path':path,'original':dest.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    (backup/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('Differential backup; reuse byte-exact existing bitmap. New source copies bytes:',sum(x['bytes'] for x in manifest if x['path']!='map_data/provinces.png'))
def bitmap_fix():
    # Exact semantic source-map edit, not an AI image transformation.
    path=source_bitmap();im=Image.open(path);assert im.mode=='RGB' and im.size==(8192,3616)
    assert im.getpixel((4768,891))==tuple(bytes.fromhex('DCE378'))
    assert im.getpixel((4768,892))==tuple(bytes.fromhex('FF7D57'))
    im.putpixel((4768,891),tuple(bytes.fromhex('FF7D57')));im.save(path)
    print('Only pixel (4768,891): xDCE378/CRI -> adjacent xFF7D57/PLC')
    inv=qa.inventory();preview(packed(path),{r['key'][0]:r['key'][2] for r in inv['owners']},'after')
def comparison():
    # A legible political preview and a separate exact-pixel inset.
    a=Image.open(OUT/'before.png');b=Image.open(OUT/'after.png')
    pair=Image.new('RGB',(a.width+b.width, a.height+38),'#f3f0e9');pair.paste(a,(0,38));pair.paste(b,(a.width,38))
    d=ImageDraw.Draw(pair);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    d.text((20,6),'AVANT LE CONTROLE',font=font,fill='#222222');d.text((a.width+20,6),'APRES : BUDJAK INTERIEUR OTTOMAN',font=font,fill='#222222')
    pair.save(OUT/'before_after.png')
    old=packed(PARENT/'provinces_before.png');new=packed(source_bitmap());box=(4764,887,4773,896);scale=40
    im=Image.new('RGB',(760,470),'#f3f0e9');d=ImageDraw.Draw(im)
    for i,grid in enumerate([old,new]):
        cut=grid[box[1]:box[3],box[0]:box[2]];canvas=np.zeros((*cut.shape,3),np.uint8)
        for c in np.unique(cut):canvas[cut==c]=(224,180,82) if c==int('DCE378',16) else (181,178,154)
        im.paste(Image.fromarray(canvas).resize((360,360),Image.Resampling.NEAREST),(i*380,55))
        d.text((i*380+10,8),'AVANT' if i==0 else 'APRES',font=font,fill='#222222')
        x=i*380+4*scale;y=55+4*scale;d.rectangle((x,y,x+scale-1,y+scale-1),outline='#bb2222',width=3)
        d.text((i*380+10,425),'CRI : xDCE378' if i==0 else 'PLC : xFF7D57',font=font,fill='#222222')
    im.save(OUT/'isolated_pixel_before_after.png')
def validate():
    base=json.loads((OUT/'REVIEW_BASELINE.json').read_text(encoding='utf-8'));before=base['inventory'];after=qa.inventory();checks={}
    changed=[p for p,h in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    checks['only_four_authorized_runtime_files_changed']=set(changed)==set(TOUCHED)
    current_files={p.relative_to(ROOT).as_posix() for folder in ['common','events','gfx','map_data','localization','.metadata'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    checks['no_runtime_file_added_or_deleted']=current_files==set(base['hashes'])
    own=qa.counter(before['owners']);own[('x5F2259','STATE_BESSARABIA','CRI')]-=1;own[('x5F2259','STATE_BESSARABIA','TUR')]+=1
    checks['only_x5F2259_territorial_owner_changed']=+own==qa.counter(after['owners'])
    states=[s for s in before['states'] if s!=['STATE_BESSARABIA','CRI']]
    checks['only_empty_bessarabia_cri_subdivision_removed']=states==after['states']
    pop=qa.counter(before['regional_pop'])
    for k,n in list(pop.items()):
        if k[:2]==('STATE_BESSARABIA','CRI'):
            pop[(k[0],'TUR',*k[2:])]+=n;del pop[k]
    checks['all_49569_people_transferred_without_other_regional_changes']=pop==qa.counter(after['regional_pop'])
    checks['global_demographics_and_resolved_religions_unchanged']=before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics']
    buildings=qa.counter(before['buildings'])
    moved=[]
    for k,n in list(buildings.items()):
        if k[:2]==('STATE_BESSARABIA','CRI'):
            moved.append([k,n]);buildings[(k[0],'TUR',k[2])]+=n;del buildings[k]
    checks['only_wheat_location_changes_all_building_bodies_owners_preserved']=buildings==qa.counter(after['buildings']) and len(moved)==1
    checks['building_levels_pm_reserves_unchanged']=before['building_levels_written']==after['building_levels_written']
    checks['all_units_formations_and_recruitment_unchanged']=before['units']==after['units']
    checks['countries_types_and_capitals_unchanged']=before['countries']==after['countries']
    checks['state_region_rgb_definitions_unchanged']=before['geometry']==after['geometry']
    checks['duplicates_exactly_unchanged']=before['duplicates']==after['duplicates']
    checks['no_new_orphan_reference']=all(e in before['errors'] for e in after['errors'])
    checks['no_bessarabia_cri_historical_reference_left']=not any(e for e in after['errors'] if 'STATE_BESSARABIA' in e and 'CRI' in e)
    originals=json.loads((OUT/'DIFFERENTIAL_BACKUP/MANIFEST.json').read_text(encoding='utf-8'))
    # Compare ASTs outside the exact state scope, as well as untouched runtime bytes.
    def strip(nodes):
        def walk(n):
            if n.key=='s:STATE_BESSARABIA':return None
            if isinstance(n.value,list):return [n.key,n.op,[v for c in n.children() if (v:=walk(c)) is not None]]
            return qa.norm(n)
        return [walk(n) for n in nodes]
    for path in TOUCHED[:-1]:
        orig=next(r for r in originals if r['path']==path)
        a=cw.parse((ROOT/orig['original']).read_text(encoding='utf-8-sig'));b=cw.parse((ROOT/path).read_text(encoding='utf-8-sig'))
        checks[path+'_outside_bessarabia_ast_unchanged']=strip(a)==strip(b)
    # Attribute counters preserve culture, explicit/implicit religion, slavery and every other pop property.
    def attributes(text):
        out=C.Counter()
        for p in cw.walk(cw.parse(text)):
            if p.key=='create_pop':out[tuple(json.dumps(qa.norm(c),ensure_ascii=False) for c in p.children() if c.key!='size')]+=int(p.one('size'))
        return out
    pp='common/history/pops/15_russia.txt';orig=next(r for r in originals if r['path']==pp)
    checks['all_pop_attributes_including_social_status_preserved']=attributes((ROOT/orig['original']).read_text(encoding='utf-8-sig'))==attributes((ROOT/pp).read_text(encoding='utf-8-sig'))
    old=packed(PARENT/'provinces_before.png');new=packed(source_bitmap());ys,xs=np.where(old!=new)
    edits=[{'x':int(x),'y':int(y),'before':'x%06X'%int(old[y,x]),'after':'x%06X'%int(new[y,x])} for y,x in zip(ys,xs)]
    checks['exactly_one_authorized_pixel_changed']=edits==[{'x':4768,'y':891,'before':'xDCE378','after':'xFF7D57'}]
    checks['bitmap_format_and_dimensions_preserved']=Image.open(source_bitmap()).mode=='RGB' and new.shape==old.shape==(3616,8192)
    checks['no_rgb_created_or_removed']=np.array_equal(np.unique(old),np.unique(new))
    pixel_provinces=[]
    for v in ['xDCE378','xFF7D57']:
        val=int(v[1:],16);yy,xx=np.where((old==val)|(new==val));box=np.s_[yy.min():yy.max()+1,xx.min():xx.max()+1]
        pre=components(old[box]==val)[1];post=components(new[box]==val)[1]
        checks[v+'_no_new_disconnection']=len(post)<=len(pre)
        pre8=components(old[box]==val,8)[1];post8=components(new[box]==val,8)[1]
        pixel_provinces.append({'rgb':v,'region':before['geometry'][v],'owner':next(r['key'][2] for r in before['owners'] if r['key'][0]==v),'pixels_before':int((old[box]==val).sum()),'pixels_after':int((new[box]==val).sum()),'components4_before':len(pre),'components4_after':len(post),'components8_before':len(pre8),'components8_after':len(post8)})
        if v=='xDCE378':checks['cri_detached_pixel_removed']=len(pre)==2 and len(post)==1
    checks['kerch_kinburn_hotin_and_all_other_bitmap_areas_preserved']=all(not ((old==int(v[1:],16))^(new==int(v[1:],16))).any() for v in ['x706060','x8A09FD','x79D62E','xB0C0E0','x76E041'])
    # All registered hubs retain their original physical RGB; no locator file changed.
    defs,hubs,names=geo_data();flat=[v for hh in hubs.values() for v in hh.values()]
    checks['edited_pixel_rgb_not_a_registered_hub']='xDCE378' not in flat and 'xFF7D57' not in flat
    checks['x5F2259_has_no_registered_city_port_farm_wood_mine_hub']='x5F2259' not in flat
    checks['all_diplomacy_journals_infrastructure_techs_previous_maps_byte_preserved']=all(p in TOUCHED for p in changed)
    result={'status':'PASS_STATIC' if all(checks.values()) else 'FAIL_STATIC','checks':checks,'changed_runtime_files':changed,'pixel_changes':edits,'world_population_before':sum(r['count'] for r in before['pops']),'world_population_after':sum(r['count'] for r in after['pops']),'bessarabia_population_before':{o:sum(r['count'] for r in before['regional_pop'] if r['key'][:2]==['STATE_BESSARABIA',o]) for o in ['MOL','TUR','CRI']},'bessarabia_population_after':{o:sum(r['count'] for r in after['regional_pop'] if r['key'][:2]==['STATE_BESSARABIA',o]) for o in ['MOL','TUR','CRI']},'existing_duplicate_rgb':len(after['duplicates']),'reference_errors_before':len(before['errors']),'reference_errors_after':len(after['errors']),'native_engine_after_review':'NOT_RUN','user_native_map2d_observation':{'load':'SUCCESS_REPORTED','PLC_russian_bloc':'REMAINS_REPORTED','CRI_russian_bloc':'REMAINS_REPORTED','CRI_protectorate':'NOT_ESTABLISHED_BY_OBSERVATION'},'git_commit_merge_push':'NOT_PERFORMED'}
    result['pixel_province_geometries']=pixel_provinces
    # Re-run current-source model fixtures without overwriting earlier MAP2D reports.
    import contextlib,io
    import validate_regional_infrastructure_shortage as infrastructure
    model_log=io.StringIO()
    with contextlib.redirect_stdout(model_log):
        cw.model_tests();scenarios=infrastructure.model_tests()
    result['regression_models']={'ottoman':'PASS','administrative_combinations':1024,'political_combinations':192,'infrastructure_scenarios':len(scenarios),'infrastructure_results':[{'scenario':s['scenario'],'result':s['result']} for s in scenarios],'native_engine':False,'log':model_log.getvalue()}
    (OUT/'BUDJAK_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2));print('Failures:',[k for k,v in checks.items() if not v])
    return all(checks.values())
if __name__=='__main__':
    if sys.argv[1]=='validate':sys.exit(0 if validate() else 1)
    {'inspect':inspect,'prepare':prepare,'bitmap_fix':bitmap_fix,'comparison':comparison}[sys.argv[1]]()
