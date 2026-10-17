"""Reproducible research-only source calibration. No runtime output paths."""
import sys, json, re, math, urllib.parse, xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import research as r

class Links(HTMLParser):
    def __init__(self,raw):
        super().__init__();self.links=[];self.feed(raw)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='a' and d.get('href'):self.links.append(d['href'])

def catalogue():
    links=Links((r.OUT/'EVIDENCE/SBB_1772_BOUNDARY_SEARCH.html').read_text()).links
    nxt=next(v for v in links if v.endswith('/NXT'))
    url=urllib.parse.urljoin('https://lbssbb.gbv.de',nxt.rsplit('/',1)[0]+'/SHW?FRST=1')
    r.fetch('SBB_1772_ONLINE_WITH_CONTEXT.html',url)

def inspect(name):
    raw=(r.OUT/'EVIDENCE'/name).read_text(errors='replace')
    print('\n'.join(Links(raw).links))
    text=re.sub('<[^>]+>',' ',raw);text=re.sub(r'\s+',' ',text)
    print(text[-13000:])

def metric(geo,origin):
    """Local equirectangular work plane in metres, not a source projection claim."""
    p=np.asarray(geo,float);lon,lat=origin
    return (p-[lon,lat])*[111319.49079327358*math.cos(math.radians(lat)),111319.49079327358]

def unmetric(p,origin):
    lon,lat=origin
    return np.asarray(p)/[111319.49079327358*math.cos(math.radians(lat)),111319.49079327358]+origin

def fit(x,y,kind):
    x=np.asarray(x,float);y=np.asarray(y,float)
    if kind=='affine':return np.linalg.lstsq(np.c_[x,np.ones(len(x))],y,rcond=None)[0]
    if kind=='similarity':
        # Raster y is down, metric north is up: include the fixed axis reflection.
        x=x.copy();x[:,1]*=-1
        a=[];b=[]
        for (u,v),(e,n) in zip(x,y):a.extend([[u,-v,1,0],[v,u,0,1]]);b.extend([e,n])
        u,v,e,n=np.linalg.lstsq(a,b,rcond=None)[0]
        return np.array([[u,v],[v,-u],[e,n]])
    raise ValueError(kind)

def apply(p,m):return np.c_[np.asarray(p),np.ones(len(p))]@np.asarray(m)

def polygon_center(points):
    p=np.asarray(points);q=np.roll(p,-1,axis=0);c=p[:,0]*q[:,1]-q[:,0]*p[:,1]
    return np.sum((p+q)*c[:,None],axis=0)/(3*c.sum())

def controls():
    root=ET.parse(r.OUT/'EVIDENCE/OSM_ANKLAM.xml').getroot()
    nodes={e.get('id'):[float(e.get('lon')),float(e.get('lat'))] for e in root.findall('node')}
    ways={e.get('id'):e for e in root.findall('way')}
    # Pixel centres manually read on the acquired 4000-pixel original. No locator used.
    # CHECK selection fixed before fitting, including a point across the Peene.
    entries=[('A_MAR','Marienkirche',143255838,2076,1376,'FIT',12,'1773 legend 2; medieval church footprint, rebuilt walls not exact original centre'),
        ('A_NIK','Nikolaikirche',143255843,1666,1414,'FIT',12,'1773 legend 3; surviving footprint, postwar reconstruction'),
        ('A_PUL','Pulverturm',309987590,1840,1060,'FIT',10,'1773 legend 7, circular tower on southern city wall'),
        ('A_STE','Steintor',143255854,1504,1206,'CHECK',15,'1773 legend 13, eastern city gate; reserved independent check'),
        ('A_WES','Wesselsche Muehle',143245232,1582,2033,'CHECK',18,'Single mill north of bridge in 1773; identification provisional; municipality dates mill to 1728')]
    rows=[]
    for ident,name,way,x,y,role,err,note in entries:
        e=ways[str(way)];pts=[nodes[n.get('ref')] for n in e.findall('nd')]
        if pts[0]==pts[-1]:pts=pts[:-1]
        geo=polygon_center(pts);rows.append(dict(id=ident,sector='PEENE',source='ANKLAM_1773',name=name,
            source_x=x,source_y=y,source_space='Original 4000x2259; x east on raster, y down; not north-up',
            longitude=float(geo[0]),latitude=float(geo[1]),role=role,reading_radius_source_px=err,
            coordinate_source=f'https://www.openstreetmap.org/way/{way}',
            coordinate_derivation='Polygon area centroid of public OSM footprint; unsurveyed, not certified precision',
            correspondence_status='PROVISIONAL_PHYSICAL_HOMOLOGUE',stability=note,native_x='',native_y='',
            native_status='NO_IDENTIFIED_NATIVE_BUILDING_HOMOLOGUE'))
    # Church sites supplied by NID. The map cross is used, not the text label.
    # Inowroclaw and Pakosc remain excluded from FIT: exact church identity ambiguous.
    pfau=[('N_GNI','GNIEWKOWO','Gniewkowo parish church',2276,367,'FIT',15,'Cross in town; NID medieval parish site; symbol-scale identification provisional'),
        ('N_KRU','KRUSZWICA','Kruszwica collegiate church',1718,1828,'FIT',20,'Cross in Polnisch Kruschwitz east of Goplo; NID 1120-1130 site; provisional symbol identification'),
        ('N_STR','STRZELNO','Strzelno convent churches',1018,1967,'FIT',25,'Church cross on east of town; NID former Norbertine complex; two nearby churches unresolved'),
        ('N_INO','INOWROCLAW','Inowroclaw St Nicholas',1785,1015,'CHECK',35,'Urban core church hypothesis; exact church block not secure, CHECK_DIAGNOSTIC_ONLY'),
        ('N_PAK','PAKOSC','Pakosc St Bonaventure convent',925,523,'CHECK',40,'Town/convent reading uncertain near multiple river arms; CHECK_DIAGNOSTIC_ONLY')]
    for ident,key,name,x,y,role,err,note in pfau:
        html=(r.OUT/f'EVIDENCE/NID_{key}.html').read_text()
        lat,lon=map(float,re.search(r'destination=([0-9.]+),([0-9.]+)',html).groups())
        url=r.load(f'EVIDENCE/NID_{key}.html.source.json')['url']
        rows.append(dict(id=ident,sector='NETZE',source='PFAU_39',name=name,source_x=x,source_y=y,
            source_space='4000x2822 raster after exact 180 degree rotation: u=3999-original_x;v=2821-original_y; approximate north-up only',
            longitude=lon,latitude=lat,role=role,reading_radius_source_px=err,coordinate_source=url,
            coordinate_derivation='NID site location linked by destination and GPX; not a surveyed church centroid',
            correspondence_status='PROVISIONAL_PHYSICAL_HOMOLOGUE' if role=='FIT' else 'AMBIGUOUS_CHECK_NOT_CERTIFIED',
            stability=note,native_x='',native_y='',native_status='NO_IDENTIFIED_NATIVE_BUILDING_HOMOLOGUE'))
    r.csvout('CONTROL_POINTS.csv',rows)
    return rows

def calibration():
    rows=controls();models={};checks=[];diagnostics={}
    for source in ['ANKLAM_1773','PFAU_39']:
        a=[v for v in rows if v['source']==source];ix=[i for i,v in enumerate(a) if v['role']=='FIT'];cx=[i for i,v in enumerate(a) if v['role']=='CHECK']
        x=np.array([[v['source_x'],v['source_y']] for v in a]);geo=np.array([[v['longitude'],v['latitude']] for v in a]);origin=geo.mean(axis=0).tolist();y=metric(geo,origin)
        models[source]={};ds={}
        for kind in ['similarity','affine']:
            m=fit(x[ix],y[ix],kind);pred=apply(x,m);res=np.linalg.norm(pred-y,axis=1)
            models[source][kind]=dict(matrix_source_xy1_to_local_EN_m=m.tolist(),origin_lon_lat=origin,fit_ids=[a[i]['id'] for i in ix],check_ids=[a[i]['id'] for i in cx],
                fit_mean_m=float(res[ix].mean()),check_mean_m=float(res[cx].mean()),check_max_m=float(res[cx].max()),accepted_for_political_tracing=False)
            for i in cx:
                checks.append(dict(source=source,model=kind,id=a[i]['id'],name=a[i]['name'],predicted_lon=float(unmetric(pred[i],origin)[0]),predicted_lat=float(unmetric(pred[i],origin)[1]),
                    reference_lon=geo[i,0],reference_lat=geo[i,1],residual_m=float(res[i]),status=a[i]['correspondence_status'],game_error_px='',
                    warning='Source-to-real diagnostic only; not certified source accuracy or bitmap error'))
            loo=[]
            # With 3 anchors an affine LOO fit is underdetermined: do not report it.
            if kind=='similarity':
                for i in ix:
                    keep=[j for j in ix if j!=i];lm=fit(x[keep],y[keep],kind)
                    loo.append(dict(omitted_id=a[i]['id'],heldout_error_m=float(np.linalg.norm(apply(x[[i]],lm)[0]-y[i]))))
            rng=np.random.default_rng(1776);spread=[]
            for _ in range(250):
                # Sensitivity range, NOT statistical confidence: uniform disk within assigned reading radii.
                ang=rng.uniform(0,2*np.pi,len(ix));rad=np.sqrt(rng.uniform(0,1,len(ix)))*[a[i]['reading_radius_source_px'] for i in ix]
                xx=x[ix]+np.c_[np.cos(ang)*rad,np.sin(ang)*rad];mm=fit(xx,y[ix],kind)
                spread.append(np.linalg.norm(apply(x[cx],mm)-pred[cx],axis=1))
            ds[kind]=dict(leave_one_fit_out=loo,reading_sensitivity_max_m=float(np.max(spread)),reading_trials=250,
                reading_sensitivity_not_confidence_interval=True,affine_leave_one_out='NOT_IDENTIFIABLE_WITH_ONLY_TWO_REMAINING_ANCHORS' if kind=='affine' else None)
        ds['projective']='NOT_FIT: only 3 candidate fit points, insufficient for 8-parameter model; no polynomial fit'
        ds['model_disagreement_on_checks_m']=np.linalg.norm(apply(x[cx],models[source]['similarity']['matrix_source_xy1_to_local_EN_m'])-apply(x[cx],models[source]['affine']['matrix_source_xy1_to_local_EN_m']),axis=1).tolist()
        ds['status']='DIAGNOSTIC_ONLY: tentative correspondence, sparse extent; no source-to-native physical homologues'
        diagnostics[source]=ds
    r.dump('TRANSFORMATIONS.json',dict(source_to_real=models,coordinate_system=dict(real='WGS84 longitude latitude; metadata NID/OSM, not independently surveyed',
        local='Equirectangular tangent work plane, R=6378137m, no claim about historical map projection',native='8192x3616, x right/y down, integer cell indices; centres x+0.5,y+0.5'),
        real_to_native=dict(status='NOT_NEWLY_CALIBRATED',reason='No independently identified homologous physical landmark in native raster near the frontier',
            retained_hypothesis='../R3 and ../R2; Miller plus offset is diagnostic, not certified exact native projection'),political_boundaries_not_accepted=True))
    r.dump('CALIBRATION_DIAGNOSTIC.json',diagnostics);r.csvout('INDEPENDENT_CHECKS.csv',checks)
    print(json.dumps(models,indent=2));print(json.dumps(diagnostics,indent=2))

if __name__=='__main__':
    if sys.argv[1]=='inspect':inspect(sys.argv[2])
    else:{'catalogue':catalogue,'calibration':calibration}[sys.argv[1]]()
