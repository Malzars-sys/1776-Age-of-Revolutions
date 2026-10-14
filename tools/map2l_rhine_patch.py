"""Stage a source-traced limited Neckar correction; apply text with apply_patch."""
import collections as C
import csv
import json
import re
import shutil
import sys
import numpy as np
from PIL import Image, ImageDraw
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2b_patch import state, region, append
from map_1776_audit import values
from map2l_belgium import allocate, components, packed, sha
from map2l_rhine import ROOT, OUT, render
from map2l_franconia import inside
from map2l_registry import active_registry_path
SID='STATE_BADEN'


def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def emit(files, name):
    import map2l_belgium as emitter
    emitter.LOT=OUT
    return emitter.emit(files, name)


def geometry():
    b=json.loads((OUT/'BASELINE.json').read_text())
    assert sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    config=json.loads((OUT/'TRACING.json').read_text())
    fit=[p for p in config['points'] if p['role']=='FIT']
    X=np.array([[*p['source'],1] for p in fit]);Y=np.array([p['game'] for p in fit])
    T=np.linalg.lstsq(X,Y,rcond=None)[0];inverse=np.linalg.inv(T[:2]);metrics=[]
    for p in config['points']:
        if 'game' not in p:continue
        predicted=np.array([*p['source'],1])@T
        metrics.append(dict(**p,predicted_game=predicted.tolist(),error_game_px=float(np.linalg.norm(predicted-p['game']))))
    source=OUT/config['source'];overlay=Image.open(source).convert('RGB');draw=ImageDraw.Draw(overlay)
    for p in config['polygons']:
        draw.line([tuple(q) for q in p['points']]+[tuple(p['points'][0])],fill='orange' if p['owner']=='KPF' else 'red',width=5)
    for p in metrics:
        x,y=p['source'];draw.ellipse((x-7,y-7,x+7,y+7),fill='blue');draw.text((x+9,y),p['name'],fill='blue',stroke_width=2,stroke_fill='white')
    overlay.save(OUT/'HISTORICAL_OVERLAY.png')
    dump('ALIGNMENT.json',dict(matrix_source_to_game=T.tolist(),points=metrics,
         source_sha256=sha(source),status='LOCAL_GAME_SCALE_APPROXIMATION_REMOTE_CONTROL_LIMITS_EXTRAPOLATION'))
    before=packed(ROOT/'map_data/provinces.png');changed=before.copy()
    parents={int(rgb[1:],16):rgb for rgb in config['parents']}
    mask=np.isin(before,list(parents));ys,xs=np.where(mask);cells=np.column_stack((xs,ys))
    scan=(cells+0.5-T[2])@inverse;owners=np.array(['BAD']*len(cells),dtype='U3')
    for p in config['polygons']:owners[inside(scan,p['points'])]=p['owner']
    lookup={tuple(c):str(t) for c,t in zip(cells,owners)}
    # Never enlarge or force a country around a native name/locator.
    assert lookup.get((4290,887))=='KPF', 'Native Heidelberg hub lies outside traced envelope; review geometry'
    abstracted=[]
    for (x,y),tag in list(lookup.items()):
        if (x,y)==(4290,887):continue
        near=[lookup[q] for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if q in lookup and before[q[1],q[0]]==before[y,x]]
        if near and tag not in near:
            dest=C.Counter(near).most_common(1)[0][0]
            if dest!=tag:lookup[x,y]=dest;abstracted.append(dict(cell=[int(x),int(y)],before=tag,after=dest))
    assert {'KPF','KMZ'}<=set(lookup.values()), 'No representable enclave in source envelope'
    colors=set(np.unique(before).tolist());counter=0;assignments=[];new=[]
    for value,parent in sorted(parents.items()):
        groups=[]
        for tag in sorted(set(lookup.values())):
            local=np.zeros(mask.shape,dtype=bool)
            for (x,y),t in lookup.items():
                if t==tag and before[y,x]==value:local[y,x]=True
            for part in components(local):groups.append(dict(owner=tag,cells=[(x,y) for y,x in part],pixels=len(part)))
        keep=next(g for g in groups if (4290,887) in g['cells']) if parent=='xE0A2B9' else max(groups,key=lambda g:g['pixels'])
        for g in groups:
            rgb=parent
            if g is not keep:
                while 0xEDA300+counter in colors:counter+=1
                v=0xEDA300+counter;counter+=1;colors.add(v);rgb='x'+format(v,'06X');new.append(dict(rgb=rgb,parent_rgb=parent))
            for x,y in g['cells']:changed[y,x]=int(rgb[1:],16)
            assignments.append(dict(rgb=rgb,parent_rgb=parent,state=SID,**g))
    Image.fromarray(np.stack(((changed>>16)&255,(changed>>8)&255,changed&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    scope=[r for r in b['inventory']['owners'] if r['key'][1] in {'STATE_RHINELAND','STATE_HESSE','STATE_BADEN','STATE_FRANCONIA'} and r['key'][0] not in config['parents']]
    scope += [dict(key=[r['rgb'],SID,r['owner']],count=1) for r in assignments]
    render(changed,scope,json.loads((OUT/'NATIVE_ANCHORS.json').read_text()),caption='Applied Neckar sublot / apres : game-scale approximation',filename='AFTER.png')
    render(before,[r for r in b['inventory']['owners'] if r['key'][1] in {'STATE_RHINELAND','STATE_HESSE','STATE_BADEN','STATE_FRANCONIA'}],json.loads((OUT/'NATIVE_ANCHORS.json').read_text()))
    left=Image.open(OUT/'BEFORE.png');right=Image.open(OUT/'AFTER.png');both=Image.new('RGB',(left.width+right.width,left.height),'white');both.paste(left);both.paste(right,(left.width,0));both.save(OUT/'BEFORE_AFTER.png')
    weights=C.Counter()
    for r in b['inventory']['owners']:
        if r['key'][1]==SID and r['key'][0] not in config['parents']:weights[r['key'][2]]+=int((before==int(r['key'][0][1:],16)).sum())
    weights.update(lookup.values())
    dump('GEOMETRY.json',dict(status='LIMITED_SOURCE_TRACED_NECKAR_LOT_NOT_FULL_RHINE',assignments=assignments,
         new_provinces=new,parents=config['parents'],abstracted_pixels=abstracted,
         pixels_by_owner=dict(weights),candidate_sha256=sha(OUT/'provinces_candidate.png'),
         changed_pixels=int((changed!=before).sum()),limitations=config['limitations']))
    print('Candidate',len(new),'new RGBs;',dict(weights),'; residuals',[(p['name'],round(p['error_game_px'],3)) for p in metrics])


def prepare():
    b=json.loads((OUT/'BASELINE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text());files={};allocations=[]
    assert sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    weights=g['pixels_by_owner'];parents=set(g['parents'])
    rel='common/history/states/00_states.txt';raw=b['originals'][rel]
    src=next(n for n in state(raw,SID).children('create_state') if n.one('country')=='c:BAD');owned=src.children('owned_provinces')[0]
    retained=[r for r in values(src,'owned_provinces') if r not in parents]+[r['rgb'] for r in g['assignments'] if r['owner']=='BAD']
    raw=edits(raw,[(owned.start,owned.end,'owned_provinces = { '+' '.join(retained)+' }')])
    s=state(raw,SID);addition='\n'.join('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(r['rgb'] for r in g['assignments'] if r['owner']==tag)+' } }' for tag in ['KPF','KMZ'])
    files[rel]=edits(raw,[(s.end-1,s.end-1,'\n'+addition+'\n')])
    rel='map_data/state_regions/00_west_europe.txt';raw=b['originals'][rel];s=next(n for n in cw.parse(raw) if n.key==SID);ps=s.children('provinces')[0]
    province_list=[r for r in values(s,'provinces') if r not in parents]+[r['rgb'] for r in g['assignments']]
    files[rel]=edits(raw,[(ps.start,ps.end,'provinces = { '+' '.join('"'+r+'"' for r in province_list)+' }')])
    for rel,original in b['originals'].items():
        if '/pops/' not in rel and '/buildings/' not in rel:continue
        try:src=region(original,SID,'BAD')
        except StopIteration:continue
        ops=[];moved=C.defaultdict(list)
        if '/pops/' in rel:
            for pop in src.children('create_pop'):
                n=pop.children('size')[0];count=int(n.value);amounts=allocate(count,weights);piece=original[pop.start:pop.end]
                ops.append((n.start,n.end,'size = '+str(amounts['BAD'])))
                for tag,amount in amounts.items():
                    if tag!='BAD' and amount:moved[tag].append(edits(piece,[(n.start-pop.start,n.end-pop.start,'size = '+str(amount))]))
                allocations.append(dict(kind='population',file=rel,profile=cw.scalar(pop.one('culture'))+'/'+cw.scalar(pop.one('religion','DEFAULT')),before=count,after=amounts))
        else:
            for building in src.children('create_building'):
                levels=[n for n in cw.walk(building.children()) if n.key=='levels' and isinstance(n.value,str)]
                if not levels:continue
                bytag=C.defaultdict(list);counts=C.Counter();piece=original[building.start:building.end]
                for n in levels:
                    amounts=allocate(int(n.value),weights)
                    for tag,amount in amounts.items():bytag[tag].append((n.start-building.start,n.end-building.start,'levels = '+str(amount)));counts[tag]+=amount
                fragments={}
                for tag in weights:
                    if not counts[tag]:continue
                    fragment=edits(piece,bytag[tag]);zeros=[]
                    for own in cw.parse(fragment)[0].children('add_ownership'):
                        for holder in own.children():
                            if holder.one('levels')=='0':zeros.append((holder.start,holder.end,''))
                    fragment=edits(fragment,zeros)
                    if tag!='BAD' and cw.scalar(building.one('building'))=='building_government_administration':fragment=re.sub(r'(country\s*=\s*"?c:)BAD',r'\g<1>'+tag,fragment)
                    fragments[tag]=fragment
                ops.append((building.start,building.end,fragments.get('BAD','')))
                for tag,fragment in fragments.items():
                    if tag!='BAD':moved[tag].append(fragment)
                allocations.append(dict(kind='building',file=rel,profile=cw.scalar(building.one('building')),before=sum(int(n.value) for n in levels),after=dict(counts)))
        raw=edits(original,ops)
        for tag,pieces in moved.items():raw=append(raw,SID,tag,'\n'.join(pieces))
        files[rel]=raw
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tmap={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for r in g['new_provinces']:terrain+='\n'+r['rgb']+'="'+tmap[r['parent_rgb'].upper()]+'"'
    (OUT/'province_terrains_candidate.txt').write_text(terrain+'\n',encoding='utf-8')
    previous=[r for r in b['registry'] if r['state']==SID];updated=[r for r in previous if r['rgb'] not in parents]
    updated += [dict(rgb=r['rgb'],state=SID,beneficiary=r['owner'],basis='MAP2L Neckar: retained unresolved BAD fringe; not certified historical sovereignty.' if r['owner']=='BAD' else 'MAP2L Neckar: conservative source-traced gameplay envelope, chronology corrected; see RHINE_CENTRAL/REPORT.md.') for r in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state']!=SID]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)
    migration=dict(replaced_regions=[SID],previous=previous,updated=updated,new_members=[],free_cities=[],new_provinces=g['new_provinces'],geometry='RHINE_CENTRAL/GEOMETRY.json')
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)
    for rel,raw in files.items():
        if rel.endswith('.txt'):cw.parse(raw)
    changes=emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,allocations=allocations,new_tags=[],registered_RGBs=len(ledger),population_method='Each BAD culture/religion profile area-proportional; exact conserved totals; not a census'))
    rows=[dict(RGB=r['rgb'],Parent_RGB=r['parent_rgb'],State_ID=SID,Previous_Owner='BAD',New_Owner=r['owner'],Pixels=r['pixels']) for r in g['assignments']]
    for name,data in [('TERRITORIAL_CHANGES.csv',rows),('POPULATION_VALIDATION.csv',[dict(File=r['file'],Profile=r['profile'],Before=r['before'],After_Total=sum(r['after'].values()),**r['after']) for r in allocations if r['kind']=='population'])]:
        with (OUT/name).open('w',encoding='utf-8-sig',newline='') as handle:writer=csv.DictWriter(handle,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    print('Prepared',len(changes),'text files;',len(ledger),'registered RGBs')


def install():
    b=json.loads((OUT/'BASELINE.json').read_text());p=json.loads((OUT/'PLAN.json').read_text())
    assert sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert all(sha(ROOT/rel)!=b['hashes'][rel] for rel in p['files'] if rel in b['hashes']), 'Apply reviewed text patch first'
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    shutil.copyfile(OUT/'province_terrains_candidate.txt',ROOT/'map_data/province_terrains.txt')


def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();changes=emit(files,'IMPERIAL.patch')
    dump('IMPERIAL_FILES.json',dict(files=changes,all_compiled_files=list(files)))
    print('Prepared',len(changes),'imperial runtime updates')


def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
    import prototype_map2k_main_map as main
    main.MOD=ROOT;main.PACKAGE=OUT/'MAIN_MAP';main.PACKAGE.mkdir(exist_ok=True);main.build_and_test()


if __name__=='__main__':{'geometry':geometry,'prepare':prepare,'install':install,'imperial':imperial,'maps':maps}[sys.argv[1]]()
