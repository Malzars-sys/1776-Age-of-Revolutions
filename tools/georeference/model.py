"""Reversible diagnostic raster georeferencing. No sovereignty inference."""
import math
import numpy as np

KINDS=('miller_affine','geographic_affine','miller_axes','native_miller_hypothesis')

def project(points,kind):
    p=np.asarray(points,dtype=float).reshape(-1,2)
    if not np.isfinite(p).all() or np.any(np.abs(p[:,0])>180) or np.any(np.abs(p[:,1])>90):
        raise ValueError('Longitude [-180,180], latitude [-90,90], valeurs finies requises.')
    if kind=='geographic_affine':return p
    return np.column_stack((np.radians(p[:,0]),1.25*np.log(np.tan(np.pi/4+.4*np.radians(p[:,1])))))

def unproject(points,kind):
    p=np.asarray(points,dtype=float).reshape(-1,2)
    if kind=='geographic_affine':return p
    if np.any(np.abs(.8*p[:,1])>700):raise ValueError('Point hors domaine numérique.')
    return np.column_stack((np.degrees(p[:,0]),np.degrees(2.5*(np.arctan(np.exp(.8*p[:,1]))-np.pi/4))))

def observed(rows,role):
    return [r for r in rows if r.get('role')==role and r.get('pixel') is not None]

def fit(rows,kind='miller_affine',dimensions=(8192,3616),equator_fraction=.58):
    if kind not in KINDS:raise ValueError('Modèle inconnu.')
    if not isinstance(rows,list) or len(rows)>200:raise ValueError('Liste de 200 repères maximum requise.')
    for r in rows:
        if not isinstance(r,dict) or not isinstance(r.get('name'),str) or r.get('role') not in ['FIT','CHECK','TARGET']:
            raise ValueError('Repère invalide : nom et rôle FIT/CHECK/TARGET requis.')
        if not isinstance(r.get('geo'),list) or len(r['geo'])!=2 or None in r['geo']:raise ValueError('Deux coordonnées géographiques requises.')
        project([r['geo']],kind)
        if r.get('pixel') is not None:
            pixel=r['pixel']
            if not isinstance(pixel,list) or len(pixel)!=2 or None in pixel or not np.isfinite(np.asarray(pixel,float)).all():raise ValueError('Deux coordonnées pixel finies requises.')
    width,height=map(int,dimensions)
    if not 0<width<=16384 or not 0<height<=16384:raise ValueError('Dimensions de diagnostic invalides.')
    selected=observed(rows,'FIT')
    if kind=='native_miller_hypothesis':
        scale=width/(2*math.pi)
        return {'schema_version':1,'kind':kind,'dimensions':[width,height],
            'matrix':[[scale,0],[0,-scale],[width/2,height*equator_fraction]],
            'status':'HYPOTHESIS_NOT_EXACT','fit_count':0,'domain':None,
            'assumptions':['Miller sphérique isotrope non prouvé','Greenwich au centre X non prouvé',
                'Équateur graphique natif : pas une preuve complète de projection'],
            'equator_fraction':equator_fraction,'controls':rows}
    if len(selected)<3:raise ValueError('Au moins trois repères FIT non colinéaires sont nécessaires.')
    coords=[r['geo'] for r in selected];p=project(coords,kind);pixels=np.array([r['pixel'] for r in selected],float)
    if not np.isfinite(pixels).all():raise ValueError('Pixels non finis.')
    center=p.mean(axis=0);scale=p.std(axis=0)
    if np.any(scale<1e-12):raise ValueError('Repères dégénérés.')
    if kind=='miller_axes':
        a=np.linalg.lstsq(np.column_stack((p[:,0],np.ones(len(p)))),pixels[:,0],rcond=None)[0]
        b=np.linalg.lstsq(np.column_stack((p[:,1],np.ones(len(p)))),pixels[:,1],rcond=None)[0]
        matrix=np.array([[a[0],0],[0,b[0]],[a[1],b[1]]]);condition=None
    else:
        design=np.column_stack(((p-center)/scale,np.ones(len(p))))
        if np.linalg.matrix_rank(design)!=3:raise ValueError('Repères colinéaires : calage refusé.')
        coeff=np.linalg.lstsq(design,pixels,rcond=None)[0]
        slopes=coeff[:2]/scale[:,None];matrix=np.vstack((slopes,coeff[2]-center@slopes))
        condition=float(np.linalg.cond(design))
    if abs(np.linalg.det(matrix[:2]))<1e-12:raise ValueError('Calage non inversible.')
    geo=np.array(coords)
    return {'schema_version':1,'kind':kind,'dimensions':[width,height],'matrix':matrix.tolist(),
        'status':'EMPIRICAL_NOT_EXACT','fit_count':len(selected),'condition_normalized':condition,
        'domain':[geo.min(axis=0).tolist(),geo.max(axis=0).tolist()],
        'controls':rows,'assumptions':['Emplacements de hubs non assimilés à des relevés GPS',
            'Domaine FIT rectangulaire indicatif ; extrapolation signalée',
            'RMS et maximum observés ne sont pas des intervalles de confiance']}

def forward(model,geo):
    p=project(geo,model['kind']);m=np.asarray(model['matrix'],float)
    return p@m[:2]+m[2]

def inverse(model,pixels):
    p=np.asarray(pixels,float).reshape(-1,2);m=np.asarray(model['matrix'],float)
    if not np.isfinite(p).all():raise ValueError('Pixels non finis.')
    return unproject((p-m[2])@np.linalg.inv(m[:2]),model['kind'])

def in_domain(model,geo):
    if model.get('domain') is None:return False
    p=np.asarray(geo,float);low,high=np.array(model['domain'])
    return bool(np.all(p>=low)&np.all(p<=high))

def stats(values):
    return {'count':len(values),'rms_px':float(np.sqrt(np.mean(np.square(values)))) if values else None,
        'max_px':max(values) if values else None,'median_px':float(np.median(values)) if values else None}

def evaluate(model,rows=None):
    rows=model.get('controls',[]) if rows is None else rows;results=[];errors={'FIT':[],'CHECK':[]}
    for r in rows:
        p=forward(model,[r['geo']])[0]
        error=float(np.linalg.norm(p-r['pixel'])) if r.get('pixel') is not None else None
        result={**r,'predicted_pixel':p.tolist(),'residual_px':error,'extrapolated':not in_domain(model,r['geo'])}
        if error is not None and r.get('role') in errors:errors[r['role']].append(error)
        results.append(result)
    local=[r['residual_px'] for r in results if r['role']=='CHECK' and r['residual_px'] is not None and not r['extrapolated']]
    trusted=[r['residual_px'] for r in results if r['role']=='CHECK' and r.get('quality')=='surveyed_landmark' and r['residual_px'] is not None and not r['extrapolated']]
    loo=[];fitted=observed(rows,'FIT')
    if len(fitted)>=4 and model['kind']!='native_miller_hypothesis':
        for r in fitted:
            remaining=[v for v in rows if v is not r]
            try:
                held=fit(remaining,model['kind'],model['dimensions'])
                loo.append({'name':r['name'],'error_px':float(np.linalg.norm(forward(held,[r['geo']])[0]-r['pixel']))})
            except ValueError:loo.append({'name':r['name'],'error_px':None})
    return {'points':results,'fit':stats(errors['FIT']),'check':stats(errors['CHECK']),
        'local_check':stats(local),'local_surveyed_check':stats(trusted),'leave_one_out':loo,
        'accuracy_status':'NOT_ESTABLISHED' if len(trusted)<3 else 'EMPIRICALLY_CHECKED_NOT_EXACT',
        'confidence_interval_px':None,
        'warning':'Les écarts aux hubs sont des écarts à des emplacements du jeu, pas une mesure certaine de la position historique. Aucun contrôle pixel indépendant pour les TARGET sans observation.'}

def grid_lines(model,spacing=1,clip_domain=True):
    if not math.isfinite(spacing) or not .05<=spacing<=30:raise ValueError('Espacement de 0,05° à 30° requis.')
    if clip_domain and model.get('domain') is not None:
        low,high=model['domain'];lon0,lat0=low;lon1,lat1=high
    elif clip_domain:
        raise ValueError('Modèle sans domaine vérifié : autoriser explicitement l’extrapolation.')
    else:lon0,lat0,lon1,lat1=-180,-85,180,85
    if not clip_domain and spacing<.5:raise ValueError('Grille mondiale : espacement minimal 0,5°. Utiliser un domaine local pour une grille plus fine.')
    lines=[]
    for axis,start,end,other0,other1 in [('lon',lon0,lon1,lat0,lat1),('lat',lat0,lat1,lon0,lon1)]:
        for value in np.arange(math.ceil(start/spacing)*spacing,end+1e-9,spacing):
            samples=np.linspace(other0,other1,181)
            geo=np.column_stack((np.full(len(samples),value),samples)) if axis=='lon' else np.column_stack((samples,np.full(len(samples),value)))
            lines.append({'axis':axis,'value':float(value),'pixels':forward(model,geo).tolist()})
    return lines
