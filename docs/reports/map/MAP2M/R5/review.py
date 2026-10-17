"""R5 local-model review, source checks and conservative candidate screening."""
import sys,json,csv,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import work as w
from georeference.model import project,unproject

def forward(model,geo):
    kind='geographic_affine' if model['name'].startswith('geographic') else 'miller_affine'
    return w.old.apply(project(geo,kind),model['matrix'])
def inverse(model,pixels):
    m=np.array(model['matrix']);basis=(np.asarray(pixels)-m[2])@np.linalg.inv(m[:2])
    return unproject(basis,'geographic_affine' if model['name'].startswith('geographic') else 'miller_affine')
def read_csv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def hull(points):
    p=sorted(set(map(tuple,points)))
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower=[];upper=[]
    for v in p:
        while len(lower)>=2 and cross(lower[-2],lower[-1],v)<=0:lower.pop()
        lower.append(v)
    for v in reversed(p):
        while len(upper)>=2 and cross(upper[-2],upper[-1],v)<=0:upper.pop()
        upper.append(v)
    return lower[:-1]+upper[:-1]
def in_support(model,point):
    polygon=np.asarray(model['fit_support_convex_hull_lon_lat']);p=np.asarray(point);v=np.roll(polygon,-1,axis=0)-polygon;u=p-polygon
    cross=v[:,0]*u[:,1]-v[:,1]*u[:,0];return bool(np.all(cross>=-1e-10) or np.all(cross<=1e-10))
def fit_axes(geo,pix,kind):
    p=project(geo,'geographic_affine' if kind.startswith('geographic') else 'miller_affine');pix=np.asarray(pix)
    ab=np.linalg.lstsq(np.c_[p[:,0],np.ones(len(p))],pix[:,0],rcond=None)[0];cd=np.linalg.lstsq(np.c_[p[:,1],np.ones(len(p))],pix[:,1],rcond=None)[0]
    return np.array([[ab[0],0],[0,cd[0]],[ab[1],cd[1]]])

def models():
    tested=w.load('REVISED_NATIVE_MODELS.json');selected=dict(tested['geographic_axes'],name='geographic_axes')
    rows=w.load('REVISED_CONTROL_OBSERVATIONS.json')['points'];fit=[v for v in rows if v['Role']=='FIT'];check=[v for v in rows if v['Role']=='CHECK']
    geo=np.array([[r['Longitude'],r['Latitude']] for r in fit]);pix=np.array([[r['X'],r['Y']] for r in fit]);checkgeo=[[r['Longitude'],r['Latitude']] for r in check]
    selected.update(status='LOCAL_EMPIRICAL_COARSE_VALIDATION_NOT_EXACT',selection='Axis-separated 4 parameters; simpler than 6-parameter shear from sparse coastal geometry. Selection informed by reserved checks; no untouched final external test exists.',
        fit_domain_bbox_lon_lat=[geo.min(axis=0).tolist(),geo.max(axis=0).tolist()],
        domain_warning='Bounding rectangle is not convex-hull support. Inowroclaw south and western Warta control may be extrapolated. No guaranteed error bound between landmarks.',
        pristine_holdout_count=len(check),pristine_holdout_mean_px=float(np.linalg.norm(forward(selected,checkgeo)-np.array([[r['X'],r['Y']] for r in check]),axis=1).mean()),
        pristine_holdout_max_px=float(np.linalg.norm(forward(selected,checkgeo)-np.array([[r['X'],r['Y']] for r in check]),axis=1).max()),
        revised_usedom_not_in_pristine_statistics=True)
    selected['fit_support_convex_hull_lon_lat']=hull(geo.tolist())
    checks=read_csv(w.OUT/'INDEPENDENT_VALIDATION.csv');lookup={v['ID']:v for v in rows}
    for v in checks:
        z=lookup[v['ID']];v['Outside_fit_convex_hull']=not in_support(selected,[z['Longitude'],z['Latitude']])
    w.csvout('INDEPENDENT_VALIDATION.csv',checks)
    targets=[('Anklam',[13.692,53.856]),('Wolgast',[13.776,54.052]),('Walcz',[16.47,53.27]),('Kamin',[17.52,53.53]),('Bromberg',[18.00,53.13]),('Inowroclaw',[18.26,52.795])]
    tgeo=np.array([v[1] for v in targets]);centre=forward(selected,tgeo);loo=[];ensemble=[]
    for i,row in enumerate(fit):
        keep=[j for j in range(len(fit)) if j!=i];m=fit_axes(geo[keep],pix[keep],'geographic_axes');pred=forward(dict(name='geographic_axes',matrix=m.tolist()),tgeo);ensemble.append(pred)
        loo.append(dict(omitted_id=row['ID'],target_displacements_px=np.linalg.norm(pred-centre,axis=1).tolist()))
    rng=np.random.default_rng(1776);perturb=[]
    for _ in range(300):
        rad=np.sqrt(rng.uniform(0,1,len(fit)))*[v['Reading_radius_px'] for v in fit];ang=rng.uniform(0,2*np.pi,len(fit));pp=pix+np.c_[np.cos(ang)*rad,np.sin(ang)*rad]
        m=fit_axes(geo,pp,'geographic_axes');perturb.append(forward(dict(name='geographic_axes',matrix=m.tolist()),tgeo))
    alltested=[]
    for name,model in tested.items():alltested.append(forward(dict(model,name=name),tgeo))
    pert=np.array(perturb);en=np.array(ensemble+alltested+[centre]);sens=[]
    for i,(name,g) in enumerate(targets):sens.append(dict(name=name,geo=g,predicted_pixel=centre[i].tolist(),
        reading_perturbation_max_px=float(np.max(np.linalg.norm(pert[:,i]-centre[i],axis=1))),
        leave_one_out_max_px=float(np.max(np.linalg.norm(np.array(ensemble)[:,i]-centre[i],axis=1))),
        alternative_models_max_px=float(np.max(np.linalg.norm(np.array(alltested)[:,i]-centre[i],axis=1))),
        envelope_min_xy=en[:,i].min(axis=0).tolist(),envelope_max_xy=en[:,i].max(axis=0).tolist(),
        uncertainty_is_not_confidence_interval=True))
    selected['sensitivity_targets']=sens;selected['leave_one_out']=loo;selected['reading_sensitivity_trials']=300
    w.dump('TRANSFORMATIONS.json',dict(selected_native=selected,tested_native=tested,first_round='NATIVE_MODELS_DIAGNOSTIC.json',
        source_to_real_R4_retained='R4/TRANSFORMATIONS.json, unchanged; Anklam similarity usable only as local source diagnostic; Pfau39 rejected',
        historical_frontier_authorization=False))
    # Export all observations; provenance and roles remain explicit.
    flat=[]
    for r in rows:
        v=dict(r)
        for k,value in v.items():
            if isinstance(value,(list,dict)):v[k]=json.dumps(value,separators=(',',':'))
        flat.append(v)
    fields=list(dict.fromkeys(k for v in flat for k in v));w.csvout('CONTROL_POINTS.csv',flat,fields)
    print('Pristine independent native checks',selected['pristine_holdout_mean_px'],selected['pristine_holdout_max_px']);print(json.dumps(sens,indent=2))

def pfau_audit():
    rows=read_csv(w.R4/'CONTROL_POINTS.csv');a=[v for v in rows if v['source']=='PFAU_39'];x=np.array([[float(v['source_x']),float(v['source_y'])] for v in a]);geo=np.array([[float(v['longitude']),float(v['latitude'])] for v in a]);origin=geo.mean(axis=0);y=w.old.metric(geo,origin)
    fi=[i for i,v in enumerate(a) if v['role']=='FIT'];ci=[i for i,v in enumerate(a) if v['role']=='CHECK'];variants=[]
    baseline=None
    # New precise hypothesis: could the original rotation/frame alone cause the affine discrepancy?
    for name,xx in [('identity',x),('rotate90',np.c_[-x[:,1],x[:,0]]),('rotate180',-x),('rotate270',np.c_[x[:,1],-x[:,0]]),('reflect_y',x*[1,-1])]:
        m=w.old.fit(xx[fi],y[fi],'affine');pred=w.old.apply(xx,m);res=np.linalg.norm(pred[ci]-y[ci],axis=1)
        if baseline is None:baseline=pred
        variants.append(dict(frame=name,check_residuals_m=res.tolist(),max_change_vs_first_frame_m=float(np.max(np.linalg.norm(pred-baseline,axis=1)))))
    distances=[]
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            distances.append(dict(from_id=a[i]['id'],to_id=a[j]['id'],source_distance_px=float(np.linalg.norm(x[i]-x[j])),reference_distance_m=float(np.linalg.norm(y[i]-y[j])),implied_scale_m_per_source_px=float(np.linalg.norm(y[i]-y[j])/np.linalg.norm(x[i]-x[j]))))
    checks=[]
    for file in ['PFAU_39.jpg','PFAU_45.jpg','PFAU_46.jpg','PFAU_47.jpg','PFAU_48.jpg']:
        with Image.open(w.R4/'EVIDENCE'/file) as im:checks.append(dict(file=file,dimensions=list(im.size),sha256=w.sha(w.R4/'EVIDENCE'/file)))
    w.dump('PFAU_FRAME_AUDIT.json',dict(status='NO_ACCEPTED_REPLACEMENT_CALIBRATION',new_hypothesis='Orientation/coordinate-frame error in R4 affine prediction',
        conclusion='Rejected as sole cause: a consistent global rotation/reflection does not alter affine held-out predictions. This does not distinguish wrongly identified church symbols from genuine non-affine local source distortion.',
        controls_never_promoted_to_fit=[a[i]['id'] for i in ci],variants=variants,pairwise_distance_scale=distances,source_frames=checks,
        source_side_issue='The precise building identities at Inowroclaw/Pakosc and three original church crosses are not established by place-name labels alone.',
        intersheet_status='No physically homologated shared seam controls yet; no geographic mosaic accepted.35-section index is not a graticule.',
        grading_marks='No geodetic graticule identified on acquired detailed39; no historical prime-meridian conversion assumed.',political_1776_limit='Engraved1778 vs survey1772-1773 remains separate documentary issue.'))

def mayer():
    rows=w.load('REVISED_CONTROL_OBSERVATIONS.json')['points'];byid={v['ID']:v for v in rows};spec=[('DARSS',[88,211],'FIT'),('ARKONA',[531,24],'FIT'),('NORDPERD',[697,294],'FIT'),('JASMUND',[651,144],'CHECK'),('USEDOM',[712,433],'CHECK')]
    x=np.array([v[1] for v in spec]);geo=np.array([[byid[v[0]]['Longitude'],byid[v[0]]['Latitude']] for v in spec]);origin=geo.mean(axis=0);y=w.old.metric(geo,origin);fi=[i for i,v in enumerate(spec) if v[2]=='FIT'];ci=[i for i,v in enumerate(spec) if v[2]=='CHECK'];models={}
    selected=w.load('TRANSFORMATIONS.json')['selected_native']
    for kind in ['similarity','affine']:
        m=w.old.fit(x[fi],y[fi],kind);pg=w.old.unmetric(w.old.apply(x,m),origin);pn=forward(selected,pg);obs=np.array([[byid[v[0]]['X'],byid[v[0]]['Y']] for v in spec]);res=np.linalg.norm(w.old.apply(x,m)-y,axis=1)
        models[kind]=dict(matrix=m.tolist(),origin_lon_lat=origin.tolist(),source_points=[dict(ID=v[0],xy=v[1],role=v[2],reading_radius_source_px=4) for v in spec],
            source_to_real_check_mean_m=float(res[ci].mean()),source_to_real_check_max_m=float(res[ci].max()),
            full_chain_native_check_errors_px=np.linalg.norm(pn[ci]-obs[ci],axis=1).tolist(),source_sha256=w.sha(w.ROOT/'docs/reports/map/MAP2L/PRUSSIAN_BORDERS/EVIDENCE/MAYER_1763_GREIFSWALD.jpg'),
            status='NEW_PHYSICAL_CAPE_FIT_DIAGNOSTIC_ONLY',limitation='Northern capes constrain the source; southern political frontier remains extrapolated in this source fit. Usedom native observation was revised, not pristine.')
    w.dump('MAYER_PHYSICAL_CALIBRATION.json',models);print(json.dumps(models,indent=2))

def border_screen():
    models=w.load('TRANSFORMATIONS.json');native=models['selected_native'];tested=[dict(v,name=k) for k,v in models['tested_native'].items()]
    # Reuse the historically read Mayer line. Do not invent a new1772 Netze line.
    original=w.prior.r3.load('GEOMETRY_REVIEW.json')['PEENE'];poly=np.array(original['historical_polygon']);mayers=w.load('MAYER_PHYSICAL_CALIBRATION.json');border_rows=[];polys=[]
    for kind,model in mayers.items():
        pg=w.old.unmetric(w.old.apply(poly,model['matrix']),model['origin_lon_lat'])
        for nm in tested:
            p=forward(nm,pg);polys.append(p)
            for i in range(len(p)-1):border_rows.append(dict(Sector='PEENE',Segment=f'MAYER_{i:02}',Source='MAYER_1763_GREIFSWALD',Source_A_X=poly[i,0],Source_A_Y=poly[i,1],Source_B_X=poly[i+1,0],Source_B_Y=poly[i+1,1],
                Native_model=nm['name'],Source_model=kind,Pred_A_X=p[i,0],Pred_A_Y=p[i,1],Pred_B_X=p[i+1,0],Pred_B_Y=p[i+1,1],
                Line_role='FRAME_OR_WATER_CLIP_NOT_POLITICAL' if i<3 else 'INHERITED_POLITICAL_OR_SHORE_INTERPRETATION',
                Political_proof='NONE: viewport clipping edge' if i<3 else 'Inherited interpretation of Swedish mainland boundary on1763 map; coastline and sovereignty need separate confirmation',
                Class='C' if i<3 else 'B',Status='FRAME_NOT_FRONTIER' if i<3 else 'DIAGNOSTIC_RECONSTRUCTION_NOT_APPROVED',Obstacle='Southern source extrapolation and native shoreline generalization; no confidence bound'))
    fields=list(border_rows[0])
    for district in ['Deutsch Krone','Kamin','Bromberg','Inowroclaw']:
        v={k:'' for k in fields};v.update(Sector='NETZE',Segment=district,Source='SBB Kart.N1146/1 rectos1/2; Pfau39/46/47/48',Line_role='NOT_GEOGRAPHICALLY_RECONSTRUCTED',Political_proof='[1772] draft; individual coloured-line dates/semantics not all established',Class='C' if district=='Inowroclaw' else 'B',Status='NO_ACCEPTED_SOURCE_TO_REAL_POLITICAL_TRACE',Obstacle='No independently validated geographic source line; raw map pixels are not geographic coordinates');border_rows.append(v)
    w.csvout('BORDER_RECONSTRUCTION.csv',border_rows)
    bmp,water,_,_=w.physical_masks();lookup={int(v['key'][0][1:],16):(v['key'][1],v['key'][2]) for v in w.load('BASELINE.json')['inventory']['owners']}
    candidates=[];lung=json.loads((w.OUT.parent/'R3/EVIDENCE/LUNG_PEENESTROM_WATER.geojson').read_text())['features'];shore=[]
    for f in lung:
        if f['properties'].get('GN2')=='Peenestrom':
            for polygon in f['geometry']['coordinates']:shore.extend(polygon[0])
    shore=np.asarray(shore)
    for sector in ['PEENE','NETZE']:
        rows=read_csv(w.R4/(sector+'_CANDIDATE_CELLS.csv'))
        for row in rows:
            x,y=int(row['X']),int(row['Y']);rgb=int(bmp[y,x]);state,owner=lookup[rgb];point=np.array([x+.5,y+.5]);shore_dists=[]
            if sector=='PEENE':
                for model in tested:shore_dists.append(float(np.min(np.linalg.norm(forward(model,shore)-point,axis=1))))
                membership=[bool(w.prior.r3.r2.core.inside(point[None,:],p)[0]) for p in polys]
                cl='B';reason='Political southern source extrapolation remains unvalidated; physical native model has3.19px maximum reserved disagreement'
                if not all(membership):reason+='; alternative source/native models disagree about polygon membership'
            else:cl='C';reason='Inherited candidate has no new validated Pfau/N1146 political source-to-real conversion';membership=[]
            candidates.append(dict(X=x,Y=y,State_ID=state,Current_RGB=f'x{rgb:06X}',Current_owner=owner,Historical_owner_hypothesis=row['Historical_owner_hypothesis'],Sector=sector,
                Origin='R4_INHERITED',Class=cl,Proposed_RGB='',Applied='False',Native_model='geographic_axes empirical; alternatives retained',Historical_source=row['Sources'],
                Contemporary_water_shore_distance_range_px=json.dumps([min(shore_dists),max(shore_dists)]) if shore_dists else '',Alternative_polygon_membership=json.dumps(membership),
                Justification=reason))
    # Search beyond inherited candidates: all remaining PRU mainland pixels in the
    # full historical window, not merely the original18. Never include islands by city name.
    oldset={(v['X'],v['Y']) for v in candidates if v['Sector']=='PEENE'}
    ys,xs=np.where((bmp==0xE1A03A));n=0
    for x,y in zip(xs,ys):
        if (int(x),int(y)) in oldset or not(4384<=x<4412 and 730<=y<748):continue
        pt=np.array([[x+.5,y+.5]]);membership=[bool(w.prior.r3.r2.core.inside(pt,p)[0]) for p in polys]
        if not any(membership):continue
        rgb=int(bmp[y,x]);state,owner=lookup[rgb];n+=1
        candidates.append(dict(X=int(x),Y=int(y),State_ID=state,Current_RGB=f'x{rgb:06X}',Current_owner=owner,Historical_owner_hypothesis='SWE',Sector='PEENE',Origin='NEW_R5_SCREEN_NOT_APPROVED',Class='B',Proposed_RGB='',Applied='False',
            Native_model='geographic_axes and alternatives',Historical_source='New Mayer physical-cape calibration of retained political line',Contemporary_water_shore_distance_range_px='',Alternative_polygon_membership=json.dumps(membership),
            Justification='Additional pixel found by full remaining-parent scan; source southern extrapolation is not independently validated, so not A'))
    w.csvout('CANDIDATE_CELLS.csv',candidates)
    w.csvout('TERRITORIAL_CHANGES.csv',[],['X','Y','State_ID','RGB_before','RGB_after','Owner_before','Owner_after','Historical_evidence','Validation'])
    w.dump('SCREENING_SUMMARY.json',dict(inherited_Peene=18,inherited_Netze=77,additional_Peene_screened=n,new_A_cells=0,applied=0,
        Peene_polygon_models=polys and [v.tolist() for v in polys],Netze_additional_native_screen='Source georeferencing gate not met: no defensible political mask to enumerate new pixels; four districts remain considered, not restricted to77'))
    print('Candidate rows',len(candidates),'additionalPeene',n,'A=0; no runtime changes')

if __name__=='__main__':{'models':models,'pfau_audit':pfau_audit,'mayer':mayer,'border_screen':border_screen}[sys.argv[1]]()
