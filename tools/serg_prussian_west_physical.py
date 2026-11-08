"""Bounded western physical-landmark continuation, no Git or vanilla writes."""
from pathlib import Path
import collections,hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_prussian_west as prior
from georeference.model import forward

ROOT=prior.ROOT;CANON=prior.CANON
OUT=CANON/'PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05'
SOURCE=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))

def anchors():
    # Explicit matching of named junctions/characteristic bends, not nearest
    # points selected retrospectively from the entire unrelated river network.
    rows=[
      dict(name='Rhin–Moselle',role='FIT',river='Mosel',geo=[7.606348,50.363837],pixel=[4266.5,852.5],kind='tributary endpoint / red junction',uncertainty_pixels=1),
      dict(name='Rhin–Main',role='FIT',river='Main',geo=[8.291504,49.99328],pixel=[4284.5,858.5],kind='tributary endpoint / red junction',uncertainty_pixels=1),
      dict(name='Weser : boucle Rehme–Porta/Vlotho',role='FIT',river='Weser',geo=[8.833398,52.220331],pixel=[4298.5,789.5],kind='westernmost knee of the middle-Weser loop; generalized bend',uncertainty_pixels=2),
      dict(name='Weser : coude de Hameln',role='CHECK',river='Weser',geo=[9.343408,52.117621],pixel=[4311.5,795.5],kind='eastern knee downstream of Hameln; generalized bend',uncertainty_pixels=2),
      dict(name='Rhin : coude occidental de Düsseldorf',role='CHECK',river='Rhine',geo=[6.703857,51.270868],pixel=[4243.5,819.5],kind='western elbow of the lower-Rhine channel; generalized bend',uncertainty_pixels=2),
      dict(name='Meuse : saillant oriental Venlo–Arcen',role='CHECK',river='Maas',geo=[6.181152,51.508368],pixel=[4233.5,819.5],kind='easternmost middle-Meuse elbow; coarse identity, not a city point',uncertainty_pixels=3)]
    features=json.loads(SOURCE.read_text())['features']
    for r in rows:
        pts=np.array([p[:2] for f in features if f['properties'].get('name')==r['river'] for p in f['geometry']['coordinates']])
        assert np.linalg.norm(pts-np.array(r['geo']),axis=1).min()<1e-7
    fit=[r for r in rows if r['role']=='FIT'];design=np.array([r['geo']+[1] for r in fit]);target=np.array([r['pixel'] for r in fit])
    matrix=np.linalg.solve(design,target)
    axes=np.array(json.loads((ROOT/'docs/reports/map/MAP2M/R5/TRANSFORMATIONS.json').read_text())['selected_native']['matrix'])
    miller=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    for r in rows:
        p=np.array(r['geo']+[1])@matrix;r['predicted_pixel']=p.tolist();r['residual_pixels']=float(np.linalg.norm(p-r['pixel']))
        r['r5_residual_pixels']=float(np.linalg.norm(np.array(r['geo']+[1])@axes-r['pixel']))
        r['miller_residual_pixels']=float(np.linalg.norm(forward(miller,[r['geo']])[0]-r['pixel']))
    dump('PHYSICAL_ANCHORS.json',dict(rows=rows,source=SOURCE.relative_to(ROOT).as_posix(),source_sha256=sha(SOURCE),mod_rivers_sha256=sha(ROOT/'map_data/rivers.png'),vanilla_rivers_sha256=sha(Path('C:/Games/Victoria 3/game/map_data/rivers.png')),historical_border_source=False,native_points_are_interpretations=True,old_models_modified=False))
    dump('PHYSICAL_MODEL.json',dict(kind='geographic_affine',matrix=matrix.tolist(),dimensions=[8192,3616],status='REJECTED_INDEPENDENT_CHECKS',installed=False,fit_count=3,check_count=3,zero_fit_is_not_accuracy=True,warning='The independent CHECK readings reject this interpolating fit for the present pass. No old projection changed. R5 remains a coarse B hypothesis, not a cadastral or engine validation.'))
    box=(4220,780,4330,875);scale=10;im=Image.open(ROOT/'map_data/rivers.png').convert('RGB').crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for f in features:
        if f['properties'].get('name') not in ['Rhine','Mosel','Main','Weser','Maas']:continue
        pts=np.array(f['geometry']['coordinates'])[:,:2];native=np.c_[pts,np.ones(len(pts))]@matrix
        for p in native:
            if box[0]<=p[0]<box[2] and box[1]<=p[1]<box[3]:x,y=(p[0]-box[0])*scale,(p[1]-box[1])*scale;d.ellipse((x-1,y-1,x+1,y+1),fill='magenta')
    for i,r in enumerate(rows,1):
        x,y=(r['pixel'][0]-box[0])*scale,(r['pixel'][1]-box[1])*scale
        d.ellipse((x-4,y-4,x+4,y+4),outline='black',width=2);d.text((x+6,y-15),str(i)+' '+r['role'],font=font,fill='black',stroke_width=2,stroke_fill='white')
    im.save(OUT/'PHYSICAL_RIVER_OVERLAY.png')
    for r in rows:print(r['role'],r['name'],'new',round(r['residual_pixels'],2),'R5',round(r['r5_residual_pixels'],2),'Miller',round(r['miller_residual_pixels'],2))

def ravensberg():
    from map2l_belgium import packed,components
    from map2l_franconia import inside
    source=CANON/'PRUSSIAN_WEST_2026_11_05/RAVENSBERG_1772.jpg'
    locations={r['name']:r for r in load('CITY_GEO_REFERENCES.json')['rows']}
    readings=[('Herford',1845,1177,'FIT'),('Bielefeld',1391,1643,'FIT'),('Bünde',1742,786,'FIT'),('Borgholzhausen',783,1036,'FIT'),('Versmold',260,1340,'FIT'),('Vlotho',2586,1083,'FIT'),('Halle',961,1258,'CHECK'),('Werther',1093,1265,'CHECK'),('Preußisch Oldendorf',1687,243,'CHECK')]
    fit=[r for r in readings if r[3]=='FIT'];matrix=np.linalg.lstsq(np.array([[x,y,1] for _,x,y,_ in fit]),np.array([locations[n]['geo'] for n,_,_,_ in fit]),rcond=None)[0]
    axes=np.array(json.loads((ROOT/'docs/reports/map/MAP2M/R5/TRANSFORMATIONS.json').read_text())['selected_native']['matrix'])
    outline=[(1525,75),(1645,65),(1700,100),(1760,210),(1810,275),(1890,325),(1890,430),(1860,480),(1800,620),(1795,740),(1830,800),(1960,780),(2020,750),(2080,770),(2200,800),(2310,860),(2350,950),(2450,1000),(2630,1020),(2690,1090),(2680,1130),(2560,1160),(2460,1155),(2440,1190),(2370,1230),(2260,1235),(2200,1250),(2100,1250),(2010,1300),(1960,1400),(1950,1510),(1850,1690),(1800,1810),(1720,1930),(1590,1975),(1390,2010),(1220,2000),(1000,1980),(900,1970),(830,1880),(790,1820),(760,1730),(700,1660),(630,1560),(600,1530),(520,1515),(440,1490),(340,1470),(230,1460),(110,1445),(100,1390),(110,1290),(185,1185),(350,1100),(485,1060),(600,1000),(710,975),(1000,945),(1210,900),(1335,925),(1440,880),(1530,840),(1540,790),(1480,760),(1400,700),(1425,585),(1480,500),(1510,420),(1460,370),(1430,320),(1450,250),(1480,170)]
    geo=np.c_[outline,np.ones(len(outline))]@matrix;poly=np.c_[geo,np.ones(len(geo))]@axes
    b=load('BASELINE.json');a=packed(OUT/'provinces_before.png');yy,xx=np.mgrid[780:815,4270:4310]
    mask=inside(np.c_[(xx+.5).ravel(),(yy+.5).ravel()],poly).reshape(xx.shape)
    interior=mask.copy()
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:interior &= np.roll(np.roll(mask,dy,axis=0),dx,axis=1)
    owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    rows=[]
    for value in np.unique(a[780:815,4270:4310][interior]):
        rgb='x'+format(int(value),'06X');sid,tag=owners[rgb]
        rows.append(dict(rgb=rgb,state=sid,owner=tag,cells=int(((a[780:815,4270:4310]==value)&interior).sum()),newer_coloured_parcel=int(value)>=0xED0000))
    dump('RAVENSBERG_INTERSECTIONS.json',rows)
    metrics=[]
    for name,x,y,role in readings:
        predicted=np.array([x,y,1])@matrix;reference=np.array(locations[name]['geo']);error=(predicted-reference)@axes[:2]
        metrics.append(dict(name=name,source_pixel=[x,y],role=role,geo_reference=reference.tolist(),geonames_id=locations[name]['id'],source_fit_residual_native_pixels=float(np.linalg.norm(error)),native_pixel=(np.r_[predicted,1]@axes).tolist()))
    dump('RAVENSBERG_TRACING.json',dict(source=source.relative_to(ROOT).as_posix(),source_sha256=sha(source),source_to_geo_matrix=matrix.tolist(),source_outline=outline,native_outline=poly.tolist(),readings=metrics,selected_native='MAP2M/R5 geographic_axes, retained unchanged',reason='Independent physical readings favour this coarse model over Miller; new interpolating physical affine rejected on CHECK points',boundary_erosion_pixels=1,political_approximation='B',cadastral_certification=False))
    im=Image.open(source).convert('RGB');d=ImageDraw.Draw(im);d.line(outline+[outline[0]],fill='blue',width=4)
    for name,x,y,role in readings:d.ellipse((x-5,y-5,x+5,y+5),fill='red' if role=='FIT' else 'green');d.text((x+6,y),name,fill='black',stroke_width=1,stroke_fill='white')
    im.resize((1800,1342)).save(OUT/'RAVENSBERG_TRACE_REVIEW.jpg')
    print('Interior intersections',rows);print('Source CHECK residuals',[(r['name'],round(r['source_fit_residual_native_pixels'],2)) for r in metrics if r['role']=='CHECK'])

def geometry():
    from map2l_belgium import packed,components
    from map2l_franconia import inside
    b=load('BASELINE.json');assert prior.runtime()==b['runtime'],'Reassess concurrent functional changes'
    a=packed(OUT/'provinces_before.png');poly=np.array(load('RAVENSBERG_TRACING.json')['native_outline'])
    yy,xx=np.mgrid[780:815,4270:4310];mask=inside(np.c_[(xx+.5).ravel(),(yy+.5).ravel()],poly).reshape(xx.shape);interior=mask.copy()
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:interior &= np.roll(np.roll(mask,dy,axis=0),dx,axis=1)
    parents={'x1BA4F6','x910095','xEDAC00'}
    interior &= np.isin(a[780:815,4270:4310],[int(r[1:],16) for r in parents])
    selected=np.zeros(a.shape,dtype=bool);selected[780:815,4270:4310]=interior
    assert selected.sum()==32,'Re-review exact authorized political B candidate'
    after=a.copy();owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']};assignments=[];new=[]
    for idx,parent in enumerate(sorted(parents)):
        sid,tag=owners[parent];moved=(a==int(parent[1:],16))&selected;retained=(a==int(parent[1:],16))&~selected
        assert retained.any() and moved.any() and tag in {'SCM','WPM','HAN'}
        child='x'+format(0xEEC400+idx,'06X');assert not (a==int(child[1:],16)).any();after[moved]=int(child[1:],16);new.append(dict(rgb=child,parent_rgb=parent))
        for rgb,owner,part in [(parent,tag,retained),(child,'PRU',moved)]:
            ys,xs=np.where(part);assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=tag,owner=owner,pixels=len(xs),cells=[[int(x),int(y)] for y,x in zip(ys,xs)]))
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=-1).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,parents=sorted(parents),assignments=assignments,new_provinces=new,hub_rebindings=[],ownership_cells=32,changed_pixels=int((a!=after).sum()),candidate_sha256=sha(OUT/'provinces_candidate.png'),preserve_all_existing_prussian_cells=True,protected_owner='WPO',source='RAVENSBERG_TRACING.json',scope='Conservative partial Ravensberg core only; no exact boundary or full regional completion'))
    render()
    print('Prepared 32 cells: SCM 9, WPM 6, HAN 17 -> PRU; no installation')

def render():
    from map2l_belgium import packed
    g=load('GEOMETRY.json');b=load('BASELINE.json');a=packed(OUT/'provinces_before.png');z=packed(OUT/'provinces_candidate.png');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};newowners=owners|{r['rgb']:r['owner'] for r in g['assignments']}
    colors={'PRU':(90,145,205),'WPM':(110,175,100),'WPO':(205,180,105),'HAN':(175,175,175),'LIP':(230,180,180),'SCM':(220,120,130),'WPD':(225,145,100)};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);panels=[]
    for title,bmp,own in [('AVANT',a,owners),('APRES - INSTALLE' if (OUT/'INSTALLATION.json').exists() else 'CANDIDAT B - NON INSTALLE',z,newowners)]:
        local=bmp[780:815,4270:4310];rgb=np.full((*local.shape,3),235,dtype=np.uint8)
        for v in np.unique(local):rgb[local==v]=colors.get(own.get('x'+format(int(v),'06X')),(210,210,210))
        im=Image.fromarray(rgb).resize((640,560),Image.Resampling.NEAREST);canvas=Image.new('RGB',(640,615),'white');canvas.paste(im,(0,35));d=ImageDraw.Draw(canvas);d.text((8,8),title+' ; bleu = Prusse',font=font,fill='black');d.text((8,598),'32 cellules transferees ; limites B, pas un cadastre.',font=font,fill='black');panels.append(canvas)
    im=Image.new('RGB',(1280,615),'white');im.paste(panels[0]);im.paste(panels[1],(640,0));im.save(OUT/('RAVENSBERG_BEFORE_AFTER.png' if (OUT/'INSTALLATION.json').exists() else 'RAVENSBERG_BEFORE_CANDIDATE.png'))
    diagnostics=[]
    for r in load('RAVENSBERG_TRACING.json')['readings']:
        x,y=r['native_pixel'];before='x'+format(int(a[int(y),int(x)]),'06X');after='x'+format(int(z[int(y),int(x)]),'06X')
        diagnostics.append(dict(name=r['name'],native_pixel=[x,y],before_owner=owners.get(before),after_owner=newowners.get(after),independently_certified_city_position=False))
    dump('TOWN_DIAGNOSTICS.json',diagnostics)

def prepare():
    import re
    import validate_diplomacy_ottoman_1776 as cw
    from map_1776_audit import values
    from map2a_patch import edits
    from map2b_patch import state,region,append
    from map2l_belgium import packed,allocate
    from map2l_registry import active_registry_path
    import map2m_r9 as locators
    b=load('BASELINE.json');g=load('GEOMETRY.json');a=packed(OUT/'provinces_before.png');candidate=packed(OUT/'provinces_candidate.png');before={};files={};weights={};allocations=[]
    def read(rel):
        raw=(ROOT/rel).read_bytes().decode('utf-8');assert rel not in b['runtime'] or sha(ROOT/rel)==b['runtime'][rel],rel
        before[rel]=raw;return raw.lstrip('\ufeff')
    sids=sorted({r['state'] for r in g['assignments']})
    for r in g['assignments']:
        if r['owner']!='PRU':continue
        sid,tag=r['state'],r['previous_owner'];total=sum(int((a==int(v['key'][0][1:],16)).sum()) for v in b['inventory']['owners'] if v['key'][1:]==[sid,tag]);weights[sid,tag]={tag:total-r['pixels'],'PRU':r['pixels']};assert total>r['pixels']
    rel='common/history/states/00_states.txt';raw=read(rel)
    for sid in sids:
        n=state(raw,sid);pru=next(v for v in n.children('create_state') if cw.scalar(v.one('country'))=='c:PRU');field=pru.children('owned_provinces')[0];rgbs=values(pru,'owned_provinces')+[r['rgb'] for r in g['assignments'] if r['state']==sid and r['owner']=='PRU'];raw=edits(raw,[(field.start,field.end,'owned_provinces = { '+' '.join(rgbs)+' }')])
    files[rel]=raw
    rel='map_data/state_regions/00_west_europe.txt';raw=read(rel);locs=locators.locators(a)
    for sid in sids:
        n=next(v for v in cw.parse(raw.lstrip('\ufeff')) if v.key==sid);field=n.children('provinces')[0];rgbs=values(n,'provinces')+[r['rgb'] for r in g['new_provinces'] if next(t for t in g['assignments'] if t['rgb']==r['rgb'])['state']==sid];ops=[(field.start,field.end,'provinces = { '+' '.join('"'+r+'"' for r in rgbs)+' }')]
        for kind in ['city','farm','mine','wood','port']:
            fields=n.children(kind)
            if not fields:continue
            parent=cw.scalar(fields[0].value)
            if parent not in g['parents']:continue
            loc=next(r for r in locs if r['Kind']==kind and r['ID']==int(n.one('id')));x,y=loc['X'],loc['Y'];actual='x'+format(int(candidate[int(y),int(x)]),'06X')
            assert 'x'+format(int(a[int(y),int(x)]),'06X')==parent
            if actual!=parent:ops.append((fields[0].start,fields[0].end,kind+' = "'+actual+'"'));g['hub_rebindings'].append(dict(state=sid,field=kind,before=parent,after=actual,point=[x,y],locator_moved=False))
        if n.children('prime_land'):
            field=n.children('prime_land')[0];old=values(n,'prime_land');new=[]
            for parent in old:new.append(parent);new.extend(r['rgb'] for r in g['new_provinces'] if r['parent_rgb']==parent)
            if old!=new:ops.append((field.start,field.end,'prime_land = { '+' '.join('"'+r+'"' for r in new)+' }'))
        raw=edits(raw,ops)
    files[rel]=raw
    for rel in b['originals']:
        if '/pops/' not in rel:continue
        original=read(rel);ops=[];moved=collections.defaultdict(list)
        for (sid,tag),counts in weights.items():
            try:n=region(original,sid,tag)
            except StopIteration:continue
            for pop in n.children('create_pop'):
                size=pop.children('size')[0];total=int(size.value);amounts=allocate(total,counts);ops.append((size.start,size.end,'size = '+str(amounts[tag])));fragment=original[pop.start:pop.end]
                if amounts['PRU']:moved[sid].append(edits(fragment,[(size.start-pop.start,size.end-pop.start,'size = '+str(amounts['PRU']))]))
                allocations.append(dict(state=sid,source=tag,profile=[pop.one('culture'),pop.one('religion','DEFAULT')],before=total,after=amounts))
        raw=edits(original,ops)
        for sid,pieces in moved.items():raw=append(raw,sid,'PRU','\n'.join(pieces))
        if raw!=original:files[rel]=raw
    rel='map_data/province_terrains.txt';raw=read(rel);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    for r in g['new_provinces']:raw+='\n'+r['rgb']+' = "'+terrain[r['parent_rgb'].upper()]+'"'
    files[rel]=raw+'\n'
    rel=active_registry_path().relative_to(ROOT).as_posix();ledger=json.loads(read(rel));previous=[r for r in ledger if r['state'] in sids];assert set(g['parents'])<={r['rgb'] for r in previous}
    added=[dict(rgb=r['rgb'],state=r['state'],beneficiary='PRU',basis='Ravensberg 1772 conservative political B core; PHYSICAL_ANCHORS_2026_11_05/REPORT.md; no cadastral claim') for r in g['assignments'] if r['owner']=='PRU'];updated=previous+added
    files[rel]=json.dumps(sorted(ledger+added,key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    migration=dict(replaced_regions=sids,previous=previous,updated=updated,new_members=[],free_cities=[],country_additions={},new_provinces=g['new_provinces'],region_reference_changes=g['hub_rebindings'],extent_added_cells=[],extent_removed_cells=[])
    dump('REGISTRY_MIGRATION.json',migration)
    rel='tools/map2l_registry.py';raw=read(rel);anchor='    return result\n\ndef provincial_membership_overrides'
    if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
    assert raw.count(anchor)==1
    guard="""    prussian_west=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05'
    if (prussian_west/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((prussian_west/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((prussian_west/'GEOMETRY.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_HANNOVER','STATE_WESTPHALIA']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==32
        assert set(g['parents'])=={'x1BA4F6','x910095','xEDAC00'}
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items()) and len(new)==len(old)+3
        assert {r['owner'] for r in g['assignments'] if r['owner']!=r['previous_owner']}=={'PRU'}
        result.append(prussian_west)
"""
    files[rel]=raw.replace(anchor,guard+anchor)
    # Preserve BOM, existing newline conventions, and all unchanged content.
    for rel,raw in list(files.items()):
        old=before[rel]
        if old.startswith('\ufeff'):raw='\ufeff'+raw.lstrip('\ufeff')
        if '\r\n' in old and old.count('\n')==old.count('\r\n'):raw=raw.replace('\r\n','\n').replace('\n','\r\n')
        files[rel]=raw
        if rel.endswith('.txt'):cw.parse(raw.lstrip('\ufeff'))
    dump('GEOMETRY.json',g);dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files);dump('PLAN.json',dict(population_allocations=allocations,files=sorted(files),method='Technical integer redistribution of current source profiles; not a historical census',buildings_units_technologies_unchanged=True,runtime_installed=False))
    print('Prepared',len(files),'text files; population moved',sum(r['after']['PRU'] for r in allocations))

def compile_prepare():
    import serg_prussia_v1 as compiler
    compiler.OUT=OUT;compiler.compile_prepare()

def install():
    import serg_prussia_v1 as installer
    installer.OUT=OUT;installer.install()

def verify():
    import subprocess,re
    import validate_map2a as qa
    import validate_diplomacy_ottoman_1776 as cw
    import map2l_registry as reg
    from map2l_belgium import packed
    b=load('BASELINE.json');g=load('GEOMETRY.json');plan=load('INSTALLATION.json');expected=load('EXPECTED_TEXT.json');before=packed(OUT/'provinces_before.png');after=packed(ROOT/'map_data/provinces.png');checks=[]
    def ck(name,ok):checks.append(dict(name=name,status='PASS' if ok else 'FAIL'))
    ck('all_installed_text_exactly_prepared',all((ROOT/p).read_bytes().decode('utf-8')==s for p,s in expected.items()))
    changed={r['file'] for r in plan['changes']};current=prior.runtime();ck('all_other_functional_files_unchanged',{p:h for p,h in current.items() if p not in changed}=={p:h for p,h in b['runtime'].items() if p not in changed})
    ck('bitmap_exactly_reviewed_candidate',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
    ck('exactly_32_changed_cells',int((before!=after).sum())==32)
    expected_cells={(x,y) for r in g['assignments'] if r['owner']=='PRU' for x,y in r['cells']}
    ys,xs=np.where(before!=after);ck('only_documented_cells_changed',set(zip(xs.tolist(),ys.tolist()))==expected_cells)
    for r in g['assignments']:
        cells={(int(x),int(y)) for y,x in zip(*np.where(after==int(r['rgb'][1:],16)))}
        ck('exact_geometry_'+r['rgb'],cells=={tuple(c) for c in r['cells']} and len(cells)==r['pixels'])
    inv=qa.inventory();dump('INVENTORY_AFTER.json',inv)
    oldowners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners={r['key'][0]:r['key'][2] for r in inv['owners']}
    ck('transferred_cells_owned_by_prussia',all(owners['x'+format(int(after[y,x]),'06X')]=='PRU' for x,y in expected_cells))
    for tag in ['PRU','WPO','LIP']:
        mask=np.isin(before,[int(rgb[1:],16) for rgb,owner in oldowners.items() if owner==tag]);ck(tag+'_previous_pixels_preserved',np.array_equal(before[mask],after[mask]))
    for field in ['pops','resolved_demographics','buildings','units','countries','states','state_types']:
        ck('inventory_'+field+'_preserved',inv[field]==b['inventory'][field])
    norm=lambda rows:collections.Counter(json.dumps(r,sort_keys=True) for r in rows)
    ck('no_new_reference_errors',norm(inv['errors'])==norm(b['inventory']['errors']))
    inherited_duplicates=[r for r in b['inventory']['owners'] if r['count']!=1]
    ck('inherited_repeated_owner_declarations_unchanged',norm([r for r in inv['owners'] if r['count']!=1])==norm(inherited_duplicates))
    children={r['rgb'] for r in g['new_provinces']};child_rows=[r for r in inv['owners'] if r['key'][0] in children]
    ck('all_three_new_provinces_have_one_owner_declaration',len(child_rows)==3 and all(r['count']==1 for r in child_rows))
    ck('previous_delivery_evidence_preserved',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in b['protected'].items()))
    ck('previous_western_audit_preserved',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in load('PREVIOUS_WEST_PROTECTION.json').items()))
    rel=reg.active_registry_path().relative_to(ROOT).as_posix();oldledger=json.loads(load('TEXT_BEFORE.json')[rel]);ledger=json.loads((ROOT/rel).read_text(encoding='utf-8-sig'));newmap={r['rgb']:r for r in ledger}
    ck('registry_592_to_595_unique',len(oldledger)==592 and len(ledger)==len(newmap)==595)
    ck('all_old_imperial_titles_preserved',all(newmap[r['rgb']]==r for r in oldledger))
    ck('imperial_physical_extent_unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in oldledger]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    ck('explicit_registry_chain_last_layer',reg.approved_lot_dirs()[-1]==OUT)
    from map2k_patch import ELECTORS
    ck('nine_electors_unchanged',len(ELECTORS)==9)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))}
    ck('child_terrains_inherited',all(terrain[r['rgb'].upper()]==terrain[r['parent_rgb'].upper()] for r in g['new_provinces']))
    ck('all_physical_locators_unchanged',not any('/map_object_data/' in p for p in changed))
    ck('no_building_military_country_technology_files_changed',not any(any(x in p for x in ['/buildings/','/military_formations/','/countries/','/technology/','/production_methods/']) for p in changed))
    ck('new_affine_rejected_not_installed',load('PHYSICAL_MODEL.json')['status']=='REJECTED_INDEPENDENT_CHECKS')
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True);ck('git_'+name+'_unchanged',r.stdout.strip()==b['git'][name])
    ck('git_index_unchanged',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    for rel,raw in expected.items():
        if rel.endswith('.txt'):cw.parse(raw.lstrip('\ufeff'))
    ck('all_installed_scripts_parse',True)
    result=dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),global_written_population=sum(r['count'] for r in inv['pops']),inherited_errors=inv['errors'],inherited_duplicate_declarations=inherited_duplicates,global_uniqueness_status='FAIL_PREEXISTING_UNCHANGED',engine_test=False,human_attestation=None)
    dump('VALIDATION.json',result);print('Validation',result['passed'],'/',result['total'],[c for c in checks if c['status']=='FAIL']);assert result['status']=='PASS'

if __name__=='__main__':{'anchors':anchors,'ravensberg':ravensberg,'geometry':geometry,'prepare':prepare,'compile':compile_prepare,'install':install,'verify':verify}[sys.argv[1]]()
