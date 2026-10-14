"""MAP-2L local physical calibration, using the georeference prototype.

All generated files stay in the Erfurt-Eichsfeld diagnostic directory.
No runtime bitmap, owner, population or historical source is written.
"""
import argparse
import hashlib
import json
import heapq
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from georeference.model import fit,forward,inverse,evaluate
from map_georeference import ROOT,GAME,DEFAULT,load,digest

OUT=ROOT/'docs/reports/map/MAP2L/ERFURT_EICHSFELD/LOCAL_RECALIBRATION'
RIVER_SOURCE=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'
BOX=(4260,735,4430,865)

def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def nearest(points,route):
    squares=((np.asarray(points)[:,None,:]-route[None,:,:])**2).sum(axis=2)
    ix=squares.argmin(axis=1)
    return np.sqrt(squares[np.arange(len(ix)),ix]),ix

def robust_translation(fixed,route):
    """Translation-only robust ICP. Fixed multistart, never using CHECK data."""
    solutions=[]
    for initial in [[0,0],[-6,-6],[-6,6],[6,-6],[6,6],[0,-7],[0,7]]:
        offset=np.array(initial,float)
        for iteration in range(100):
            errors,ix=nearest(fixed+offset,route);weights=1/np.sqrt(1+(errors/2)**2)
            new=np.clip(np.average(route[ix]-fixed,axis=0,weights=weights),-15,15)
            if np.linalg.norm(offset-new)<1e-7:break
            offset=new
        errors,_=nearest(fixed+offset,route);cost=float(np.mean(np.sqrt(1+(errors/2)**2)-1))
        solutions.append((cost,offset.copy(),iteration+1))
    return min(solutions,key=lambda value:value[0])

def robust_similarity(fixed,route,translation):
    """Four parameters, with rotation/scale constrained; CHECK never accessed."""
    rotation=np.eye(2);scale=1.;offset=np.array(translation)
    for iteration in range(100):
        predicted=fixed@(scale*rotation)+offset;errors,ix=nearest(predicted,route)
        target=route[ix];weights=1/np.sqrt(1+(errors/2)**2)
        a=np.average(fixed,axis=0,weights=weights);b=np.average(target,axis=0,weights=weights)
        x=fixed-a;y=target-b
        u,s,vt=np.linalg.svd(x.T@(y*weights[:,None]));new_rotation=u@vt
        angle=np.clip(np.arctan2(new_rotation[0,1],new_rotation[0,0]),-np.radians(3),np.radians(3))
        new_rotation=np.array([[np.cos(angle),np.sin(angle)],[-np.sin(angle),np.cos(angle)]])
        new_scale=np.clip(float(np.sum(weights*np.sum((x@new_rotation)*y,axis=1))/np.sum(weights*np.sum(x*x,axis=1))),.95,1.05)
        new_offset=b-a@(new_scale*new_rotation)
        change=np.max(np.abs((fixed@(new_scale*new_rotation)+new_offset)-predicted))
        scale,rotation,offset=new_scale,new_rotation,new_offset
        if change<1e-7:break
    errors,_=nearest(fixed@(scale*rotation)+offset,route)
    return scale*rotation,offset,{'scale':float(scale),'rotation_degrees':float(np.degrees(angle)),
        'iterations':iteration+1,'limits':'scale 0.95..1.05, rotation -3..3 degrees'}

def snapshot():
    paths=[p for folder in ['common','map_data','gfx','gui','events','localization'] for p in (ROOT/folder).rglob('*') if p.is_file()]
    result={p.relative_to(ROOT).as_posix():digest(p) for p in paths}
    result['docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json']=digest(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json')
    dest=OUT/'RUNTIME_BASELINE.json'
    if dest.exists():
        assert load(dest)==result,'Runtime changed since this diagnostic baseline.'
    else:save(dest.name,result)
    print('Protected runtime files:',len(result))

def features():
    doc=load(RIVER_SOURCE);out=[]
    for r in doc['features']:
        if r['geometry']['type']!='LineString':continue
        p=np.array(r['geometry']['coordinates'])[:,:2]
        take=(p[:,0]>=7.8)&(p[:,0]<=14.6)&(p[:,1]>=49.8)&(p[:,1]<=54.3)
        if np.any(take):out.append((r,p,take))
    return out

def inspect():
    snapshot()
    records=[]
    for r,p,take in features():
        records.append({'name':r['properties'].get('name'),'ne_id':r['properties'].get('ne_id'),
            'bounds':[p[take].min(axis=0).tolist(),p[take].max(axis=0).tolist()],
            'vertices':int(take.sum()),'first':p[0].tolist(),'last':p[-1].tolist()})
    save('LOCAL_HYDROGRAPHY.json',{'source_sha256':digest(RIVER_SOURCE),'features':records})
    print(json.dumps(records,ensure_ascii=False,indent=2))
    city=load(ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json')['model']
    native=fit([],'native_miller_hypothesis')
    river=Image.open(GAME/'map_data/rivers.png').convert('RGB')
    panels=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for title,model in [('Ancien ajustement sur les villes',city),('Hypothèse Miller + équateur graphique',native)]:
        scale=5;im=river.crop(BOX).resize(((BOX[2]-BOX[0])*scale,(BOX[3]-BOX[1])*scale),Image.Resampling.NEAREST)
        d=ImageDraw.Draw(im)
        for r,p,take in features():
            projected=forward(model,p[take]);q=[((v[0]-BOX[0])*scale,(v[1]-BOX[1])*scale) for v in projected]
            if len(q)>1:d.line(q,fill='#bb3292',width=2)
            if q and 0<q[len(q)//2][0]<im.width and 0<q[len(q)//2][1]<im.height:
                d.text(q[len(q)//2],str(r['properties'].get('name')),font=font,fill='#990066',stroke_width=1,stroke_fill='white')
        for row in load(DEFAULT)['controls'][:3]:
            p=forward(model,[row['geo']])[0];u,v=(p[0]-BOX[0])*scale,(p[1]-BOX[1])*scale
            d.ellipse((u-4,v-4,u+4,v+4),outline='black',width=2);d.text((u+6,v),row['name'],font=font,fill='black',stroke_width=1,stroke_fill='white')
        for x in range(BOX[0],BOX[2],10):
            d.line(((x-BOX[0])*scale,0,(x-BOX[0])*scale,im.height),fill='#dddddd');d.text(((x-BOX[0])*scale+2,0),str(x),font=font,fill='black')
        for y in range(BOX[1],BOX[3],10):d.text((0,(y-BOX[1])*scale),str(y),font=font,fill='black',stroke_width=1,stroke_fill='white')
        panel=Image.new('RGB',(im.width,im.height+45),'white');panel.paste(im,(0,45));ImageDraw.Draw(panel).text((10,10),title,font=font,fill='black');panels.append(panel)
    image=Image.new('RGB',(sum(p.width for p in panels),panels[0].height),'white')
    for i,p in enumerate(panels):image.paste(p,(i*p.width,0))
    image.save(OUT/'HYDROGRAPHY_BEFORE.png')

def native_route(start,end,box):
    """Eight-neighbour route, retaining only the identified main river path.

    Endpoints select the displayed river, not a GPS control point. This removes
    unrelated branches from nearest-path diagnostics; no endpoint is calibrated.
    """
    im=np.array(Image.open(GAME/'map_data/rivers.png').convert('RGB').crop(box))
    mask=np.any(im<250,axis=2)&~np.all(im==[128,128,128],axis=2)
    yy,xx=np.where(mask);points=np.column_stack((xx+box[0],yy+box[1]))
    distances,indices=nearest(np.array([start,end]),points);da,db=distances;ia,ib=indices
    if max(da,db)>3:raise ValueError('Route endpoints not close to river pixels: '+str([(list(start),float(da),points[ia].tolist()),(list(end),float(db),points[ib].tolist())]))
    a=tuple(points[ia]);b=tuple(points[ib]);occupied={tuple(p) for p in points}
    dist={a:0};previous={};todo=[(0,a)]
    while todo:
        cost,p=heapq.heappop(todo)
        if cost!=dist[p]:continue
        if p==b:break
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                q=(p[0]+dx,p[1]+dy)
                if q==p or q not in occupied:continue
                step=np.hypot(dx,dy);new=cost+step
                if new<dist.get(q,float('inf')):dist[q]=new;previous[q]=p;heapq.heappush(todo,(new,q))
    if b not in dist:raise ValueError('Selected river pixels not connected.')
    route=[b]
    while route[-1]!=a:route.append(previous[route[-1]])
    return np.array(route[::-1],float)+.5

def river_geo(name,lat_bounds):
    p=np.vstack([p for r,p,_ in features() if r['properties'].get('name')==name])
    return p[(p[:,1]>=lat_bounds[0])&(p[:,1]<=lat_bounds[1])]

def summary(errors):
    return {'count':len(errors),'mean_px':float(np.mean(errors)),'rms_px':float(np.sqrt(np.mean(errors**2))),
        'max_px':float(np.max(errors)),'p90_px':float(np.percentile(errors,90))}

def physical():
    snapshot();old=load(ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json')['model']
    native=fit([],'native_miller_hypothesis')
    routes={
        'Weser':native_route([4282,741],[4339,843],(4260,735,4355,846)),
        'Elbe':native_route([4288,735],[4429,854],(4260,730,4440,865))}
    # Predefined entire-river holdout: Elbe is never used to optimize parameters.
    geographic={'Weser':river_geo('Weser',(50.6,53)), 'Elbe':river_geo('Elbe',(50.2,53))}
    diagnostics=[];best=[]
    for anchor_name,anchor in [('old_city_fit',old),('native_equator_hypothesis',native)]:
        fixed=forward(anchor,geographic['Weser'])
        # Translation only: no unconstrained warping or six-parameter overfit.
        cost,offset,iterations=robust_translation(fixed,routes['Weser'])
        candidate=json.loads(json.dumps(anchor));candidate['matrix'][2]=(np.array(anchor['matrix'][2])+offset).tolist()
        candidate['kind']='miller_affine'  # Modified matrix is no longer the fixed native hypothesis.
        candidate.update(status='LOCAL_RIVER_DIAGNOSTIC_NOT_APPROVED',fit_count=0,
            controls=load(DEFAULT)['controls'][:3],domain=[geographic['Weser'].min(axis=0).tolist(),geographic['Weser'].max(axis=0).tolist()],
            calibration_method='2-parameter robust translation, Weser-Werra nearest identified route only; not surveyed control pairs',
            independent_check_river='Elbe, excluded from optimization',
            translation_px=offset.tolist(),parent_profile=anchor_name,robust_objective=cost,iterations=iterations,
            use_for_sovereignty=False,geographic_error_bound_px=None)
        comparisons={}
        for river in ['Weser','Elbe']:
            before=nearest(forward(anchor,geographic[river]),routes[river])[0]
            after=nearest(forward(candidate,geographic[river]),routes[river])[0]
            comparisons[river]={'role':'FIT' if river=='Weser' else 'CHECK','before':summary(before),'after':summary(after)}
        doc={'model':candidate,'evaluation':evaluate(candidate),'physical_diagnostics':comparisons,
            'metric_limit':'Distances to an independently selected named river route, NOT residuals of uniquely identified geographic landmark pairs. They may underestimate geographic error.',
            'sources':{'geographic_sha256':digest(RIVER_SOURCE),'native_rivers_sha256':digest(GAME/'map_data/rivers.png')}}
        save(anchor_name+'_river_translation.json',doc);diagnostics.append(doc);best.append(candidate)
    save('PHYSICAL_TRANSLATION_COMPARISON.json',{'status':'NOT_APPROVED_NO_TERRITORY_CHANGE','diagnostics':diagnostics,
        'native_routes':{n:p.tolist() for n,p in routes.items()},'geographic_vertices':{n:p.tolist() for n,p in geographic.items()}})
    print(json.dumps([{'parent':d['model']['parent_profile'],'translation':d['model']['translation_px'],
        'comparisons':d['physical_diagnostics'],'targets':d['evaluation']['points']} for d in diagnostics],ensure_ascii=False,indent=2))

    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);scale=5;panels=[]
    for title,model in [('Avant : villes',old),('Après : translation Weser (NON VALIDÉE)',best[0]),('Autre origine : équateur + translation (NON VALIDÉE)',best[1])]:
        im=Image.open(GAME/'map_data/rivers.png').convert('RGB').crop(BOX).resize((850,650),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        for name,p in geographic.items():
            q=forward(model,p);take=(q[:,0]>=BOX[0])&(q[:,0]<=BOX[2])&(q[:,1]>=BOX[1])&(q[:,1]<=BOX[3])
            for v in q[take]:
                x,y=(v[0]-BOX[0])*scale,(v[1]-BOX[1])*scale;d.ellipse((x-1,y-1,x+1,y+1),fill='#b92a88')
        for r in load(DEFAULT)['controls'][:3]:
            v=forward(model,[r['geo']])[0];x,y=(v[0]-BOX[0])*scale,(v[1]-BOX[1])*scale
            d.ellipse((x-4,y-4,x+4,y+4),outline='black',width=2);d.text((x+6,y),r['name'],font=font,fill='black',stroke_width=1,stroke_fill='white')
        panel=Image.new('RGB',(850,695),'white');panel.paste(im,(0,45));ImageDraw.Draw(panel).text((5,10),title,font=font,fill='black');panels.append(panel)
    im=Image.new('RGB',(2550,695),'white')
    for i,p in enumerate(panels):im.paste(p,(i*850,0))
    im.save(OUT/'HYDROGRAPHY_TRANSLATION.png')
    similarity=[]
    for (name,anchor),translation in zip([('old_city_fit',old),('native_equator_hypothesis',native)],best):
        transform,offset,parameters=robust_similarity(forward(anchor,geographic['Weser']),routes['Weser'],translation['translation_px'])
        model=json.loads(json.dumps(translation));model['matrix']=(np.array(anchor['matrix'])@transform).tolist()
        model['matrix'][2]=(np.array(model['matrix'][2])+offset).tolist();model['kind']='miller_affine'
        model.update(calibration_method='Robust four-parameter similarity matched only to Weser-Werra',similarity=parameters)
        comparison={}
        for river in ['Weser','Elbe']:
            comparison[river]={'role':'FIT' if river=='Weser' else 'CHECK',
                'before':summary(nearest(forward(anchor,geographic[river]),routes[river])[0]),
                'after':summary(nearest(forward(model,geographic[river]),routes[river])[0])}
        result={'model':model,'evaluation':evaluate(model),'physical_diagnostics':comparison,
            'metric_limit':'Nearest identified main river route, NOT unique landmark point pairs; neither GPS city validation nor error bound.'}
        save(name+'_river_similarity.json',result);similarity.append(result)
    save('PHYSICAL_SIMILARITY_COMPARISON.json',{'status':'DIAGNOSTIC_ONLY','diagnostics':similarity})
    print('SIMILARITY',json.dumps([{'parent':r['model']['parent_profile'],'parameters':r['model']['similarity'],
        'fit':r['physical_diagnostics']['Weser']['after'],'check':r['physical_diagnostics']['Elbe']['after']} for r in similarity],ensure_ascii=False,indent=2))

def relief():
    Image.MAX_IMAGE_PIXELS=140000000
    im=Image.open(GAME/'map_data/heightmap.png');sx,sy=im.width/8192,im.height/3616
    box=(4270,790,4390,860);rawbox=tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(box))
    arr=np.array(im.crop(rawbox),float);normalized=((arr-arr.min())/(arr.max()-arr.min())*255).astype(np.uint8)
    image=Image.fromarray(normalized).convert('RGB').resize((1200,700),Image.Resampling.NEAREST);d=ImageDraw.Draw(image)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);peaks=[]
    # Topographically separated maxima, not automatically identified mountains.
    for index in np.argsort(arr,axis=None)[::-1]:
        y,x=np.unravel_index(index,arr.shape);p=np.array([box[0]+(x+.5)/sx,box[1]+(y+.5)/sy])
        if all(np.linalg.norm(p-r['pixel'])>8 for r in peaks):
            peaks.append({'pixel':p.tolist(),'raw_height':float(arr[y,x]),'identity':'NOT_IDENTIFIED'})
            if len(peaks)==8:break
    for i,row in enumerate(peaks):
        x,y=(np.array(row['pixel'])-box[:2])*10;d.ellipse((x-3,y-3,x+3,y+3),outline='red',width=2)
        d.text((x+5,y),str(i),font=font,fill='red',stroke_width=1,stroke_fill='white')
    for x in range(box[0],box[2],10):d.text(((x-box[0])*10,0),str(x),font=font,fill='red',stroke_width=1,stroke_fill='white')
    for y in range(box[1],box[3],10):d.text((0,(y-box[1])*10),str(y),font=font,fill='red',stroke_width=1,stroke_fill='white')
    image.save(OUT/'NATIVE_RELIEF.png');save('RELIEF_PEAKS.json',{'source':str(GAME/'map_data/heightmap.png'),
        'size':list(im.size),'map_to_height_scale':[sx,sy],'peaks':peaks,
        'limit':'Local raster maxima are not automatically identifiable geographic summits. No altitude-to-metres conversion assumed.'})
    print(json.dumps(peaks,ensure_ascii=False,indent=2))

def report():
    snapshot()
    comparison=load(OUT/'PHYSICAL_TRANSLATION_COMPARISON.json');selected=comparison['diagnostics'][0]
    alternate=comparison['diagnostics'][1];model=selected['model'];old=load(ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json')['model']
    # Fixed latitude window based on TARGET coordinates, not error-driven trimming.
    elbe=np.array(comparison['geographic_vertices']['Elbe']);route=np.array(comparison['native_routes']['Elbe'])
    band=(elbe[:,1]>=50.8287)&(elbe[:,1]<=51.6625)
    before,ib=nearest(forward(old,elbe),route);after,ia=nearest(forward(model,elbe),route)
    worst=[]
    for i in np.argsort(after)[-8:][::-1]:
        worst.append({'geo':elbe[i].tolist(),'nearest_native_pixel':route[ia[i]].tolist(),
            'after_px':float(after[i]),'route_endpoint_match':bool(ia[i] in [0,len(route)-1])})
    save('INDEPENDENT_ROUTE_CHECKS.json',{'metric':'Distances to the withheld Elbe route, not uniquely surveyed landmarks.',
        'full_before':summary(before),'full_after':summary(after),
        'target_latitude_band':[50.8287,51.6625],'band_definition':'min/max TARGET latitude plus 0.15 degrees; no residual-based point exclusion',
        'band_before':summary(before[band]),'band_after':summary(after[band]),'largest_errors':worst,
        'warning':'A small cross-track distance cannot exclude tangential displacement. Adjacent vertices are correlated, not hundreds of independent landmarks.'})
    previous_city=evaluate(old,load(DEFAULT)['controls']);new_city=evaluate(model,load(DEFAULT)['controls'])
    save('PREVIOUS_CITY_CHECK_COMPARISON.json',{'status':'LOCATORS_NOT_SURVEYED','before':previous_city['check'],
        'after':new_city['check'],'warning':'Same ten CHECK cities, no recalibration on these. This comparison is distinct from river-distance diagnostics.',
        'points':[{k:r[k] for k in ['name','pixel','predicted_pixel','residual_px','role','quality']} for r in new_city['points'] if r['role']=='CHECK']})
    delta=float(np.linalg.norm(model['translation_px']));target_records=[]
    candidates=[selected,alternate]+load(OUT/'PHYSICAL_SIMILARITY_COMPARISON.json')['diagnostics']
    for row in load(DEFAULT)['controls'][:3]:
        predictions=np.array([forward(c['model'],[row['geo']])[0] for c in candidates])
        p=forward(model,[row['geo']])[0]
        np.testing.assert_allclose(inverse(model,[p])[0],row['geo'],atol=1e-10,rtol=0)
        target_records.append({**row,'old_pixel':forward(old,[row['geo']])[0].tolist(),'candidate_pixel':p.tolist(),
            'candidate_spread_xy':np.ptp(predictions,axis=0).tolist(),
            'extrapolated_from_river_fit':next(r['extrapolated'] for r in selected['evaluation']['points'] if r['name']==row['name']),
            'uncertainty_bound_px':None,'status':'ESTIMATED_NOT_INDEPENDENTLY_OBSERVED_IN_GAME',
            'warning':'Model spread is not a geographic error bound.'})
    sources=[]
    for filename in ['EICHSFELD_FULL_SOURCE.jpg','ERFURT_SOURCE.jpg','BERN_ERFURT_1789.jpg']:
        path=OUT.parent.parent/'MAINZ_COMPLETION'/filename;metadata=load(Path(str(path)+'.SOURCE.json'))
        assert digest(path)==metadata['sha256'];sources.append({'file':filename,**metadata})
    save('PLACEMENT_ESTIMATES.json',{'status':'DIAGNOSTIC_NOT_APPROVED','translation_norm_px':delta,
        'parent_profile':'GEOREFERENCE_PROTOTYPE/miller_affine.json','targets':target_records,
        'independent_city_pixel_observations':0,'source_hashes_verified':sources,
        'applied_territorial_changes':[],'engine_tested':False})
    save('THURINGIA_RIVER_DIAGNOSTIC_PROFILE.json',{**selected,'bitmap_sha256':digest(ROOT/'map_data/provinces.png'),
        'reusable_via':'tools/map_georeference.py convert or grid --profile; not an approved GUI GCP profile',
        'approval':'REJECTED_FOR_TERRITORIAL_APPLICATION','independent_pixel_city_checks':0})
    # Concrete pixel impact, derived from current RGB and current owners.
    import map2l_mainz as core
    inventory=core.qa.inventory();bitmap=core.packed(ROOT/'map_data/provinces.png')
    owners={int(r['key'][0][1:],16):r['key'][2] for r in inventory['owners']}
    x0,y0,x1,y1=4280,780,4420,865;scale=8;local=bitmap[y0:y1,x0:x1]
    tags=np.array([owners.get(int(v),'?') for v in local.ravel()]).reshape(local.shape)
    palette={'PRU':(113,151,186),'HAN':(133,181,160),'HEK':(152,147,190),'HES':(182,142,188),'SAX':(197,179,143),'COB':(187,143,100),'KMZ':(189,78,75),'BRA':(172,156,197),'SCW':(205,165,185)}
    rgb=np.full((*local.shape,3),205,dtype=np.uint8)
    for tag,color in palette.items():rgb[tags==tag]=color
    im=Image.fromarray(rgb).resize((1120,680),Image.Resampling.NEAREST);draw=ImageDraw.Draw(im)
    for y,x in zip(*np.where(tags[1:]!=tags[:-1])):draw.line((x*scale,(y+1)*scale,(x+1)*scale,(y+1)*scale),fill='#444444')
    for y,x in zip(*np.where(tags[:,1:]!=tags[:,:-1])):draw.line(((x+1)*scale,y*scale,(x+1)*scale,(y+1)*scale),fill='#444444')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    impacts=[]
    for row in target_records:
        a=np.array(row['old_pixel']);b=np.array(row['candidate_pixel']);u,v=(a-[x0,y0])*scale;x,y=(b-[x0,y0])*scale
        draw.line((u,v,x,y),fill='#111111',width=2);draw.ellipse((u-5,v-5,u+5,v+5),outline='blue',width=2)
        draw.ellipse((x-5,y-5,x+5,y+5),outline='#006050',width=2);draw.text((x+7,y-18),row['name'],font=font,fill='#006050',stroke_width=2,stroke_fill='white')
        pixels=[]
        for label,p in [('old',a),('candidate',b)]:
            pid=int(bitmap[int(p[1]),int(p[0])]);rgb_id='x%06X'%pid
            assignments=[{'state_id':r['key'][1],'owner':r['key'][2]} for r in inventory['owners'] if r['key'][0]==rgb_id]
            pixels.append({'model':label,'rgb':rgb_id,'owner':owners.get(pid),'attributions':assignments,'pixel':p.tolist()})
        impacts.append({'name':row['name'],'pixels':pixels,'not_a_whole_province_sovereignty_claim':True})
    rural=np.array([4336.258,832.944]);x,y=(rural-[x0,y0])*scale
    draw.rectangle((x-4,y-4,x+4,y+4),outline='#a85800',width=2);draw.text((x-70,y+8),'Ferme « Erfurt » : exclue du calage',font=font,fill='#a85800',stroke_width=2,stroke_fill='white')
    canvas=Image.new('RGB',(1120,780),'white');canvas.paste(im,(0,55));d=ImageDraw.Draw(canvas)
    d.text((12,10),'Erfurt–Eichsfeld : comparaison de placement, frontières INCHANGÉES',font=font,fill='black')
    d.text((12,741),'Bleu : ancien modèle. Vert : translation hydrographique DIAGNOSTIQUE, non validée.',font=font,fill='black')
    canvas.save(OUT/'PLACEMENT_COMPARATIF.png');save('PIXEL_OWNER_COMPARISON.json',impacts)
    save('STATIC_VALIDATION.json',{'status':'PASS_RUNTIME_UNCHANGED_CALIBRATION_NOT_APPROVED',
        'protected_runtime_files':len(load(OUT/'RUNTIME_BASELINE.json')),'runtime_hashes_equal':True,
        'historical_sources_checked':len(sources),'target_roundtrips_passed':len(target_records),
        'independent_city_pixel_checks':0,'applied_provinces':0,'population_building_military_changes':0,
        'engine_tested':False,'approved_for_registry_migration':False})
    print(json.dumps({'translation_norm_px':delta,'independent_band_before':summary(before[band]),
        'independent_band_after':summary(after[band]),'targets':target_records,'pixel_impacts':impacts},ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['inspect','snapshot','physical','relief','report']);args=parser.parse_args()
    {'inspect':inspect,'snapshot':snapshot,'physical':physical,'relief':relief,'report':report}[args.command]()
