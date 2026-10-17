"""MAP2M R5: reproducible diagnostics; no runtime writes in this script."""
import sys,json,csv,hashlib,math,time
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'map_data/provinces.png').is_file())
R4=OUT.parent/'R4';GAME=Path('C:/Games/Victoria 3/game')
sys.path.insert(0,str(R4));import research as prior
import analysis as old

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def font(n=17):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)

def capture():
    assert not (OUT/'BASELINE.json').exists()
    ref=json.loads((R4/'BASELINE.json').read_text());current=prior.economy.runtime_hashes()
    changes=[p for p,h in ref['hashes'].items() if current.get(p)!=h]
    assert not changes and set(current)==set(ref['hashes']),changes
    dump('BASELINE.json',dict(runtime_hashes=current,inventory=ref['inventory'],bitmap_sha256=sha(ROOT/'map_data/provinces.png'),
        R4_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in R4.rglob('*') if p.is_file()},git_head=prior.r3.r2.head(),git_index_sha256=sha(ROOT/'.git/index')))
    print('R3/R4 reference intact;',len(current),'functional files protected.')

def physical_masks():
    import re
    bmp=prior.r3.r2.core.packed(ROOT/'map_data/provinces.png')
    default=GAME/'map_data/default.map';raw=default.read_text(encoding='utf-8-sig')
    sea=re.search(r'sea_starts\s*=\s*\{([^}]+)',raw).group(1);lake=re.search(r'lakes\s*=\s*\{([^}]+)',raw).group(1)
    water=np.isin(bmp,[int(v[1:],16) for v in re.findall(r'x[0-9a-fA-F]{6}',sea+' '+lake)])
    riverpath=ROOT/'map_data/rivers.png'
    if not riverpath.exists():riverpath=GAME/'map_data/rivers.png'
    river=Image.open(riverpath)
    assert river.mode=='P','Review palette before changing extraction'
    indices=np.array(river);mask=(indices>=3)&(indices<=11)
    return bmp,water,mask,riverpath

def scout():
    bmp,water,river,rp=physical_masks()
    for name,bbox,scale in [('BALTIC',(4340,702,4555,755),9),('RIVERS',(4405,758,4540,805),13),('RUGEN',(4374,708,4420,741),25),('WEST',(4340,714,4389,741),25),('POLAND',(4490,700,4555,739),22),('SOUTH_EAST',(4530,763,4600,817),22)]:
        x0,y0,x1,y1=bbox;arr=np.where(water[y0:y1,x0:x1,None],np.array([210,230,248]),np.array([235,231,215])).astype(np.uint8)
        arr[river[y0:y1,x0:x1]]=[20,70,220]
        im=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        for x in range(x0,x1):d.line(((x-x0)*scale,0,(x-x0)*scale,im.height),fill='#aaaaaa')
        for y in range(y0,y1):d.line((0,(y-y0)*scale,im.width,(y-y0)*scale),fill='#aaaaaa')
        step=5
        for x in range((x0//step+1)*step,x1,step):d.text(((x-x0)*scale+1,1),str(x),fill='black',font=font(14))
        for y in range((y0//step+1)*step,y1,step):d.text((1,(y-y0)*scale+1),str(y),fill='black',font=font(14))
        im.save(OUT/('NATIVE_'+name+'_READING.png'))
    dump('NATIVE_RESOURCES.json',dict(dimensions=list(bmp.shape[::-1]),river_path=str(rp),river_sha256=sha(rp),
        game_default_map_sha256=sha(GAME/'map_data/default.map'),heightmap_metadata_sha256=sha(GAME/'map_data/heightmap.heightmap'),
        land_sea_definition='Default.map sea_starts/lakes RGBs; NOT inferred from political owners',
        notes='Physical drawings have no geographic model, no locators and no political colour overlay.'))

def geographic_coast():
    fs=json.loads((OUT.parent/'R3/EVIDENCE/NE_COASTLINE.geojson').read_text())['features'];parts=[]
    for f in fs:
        for part in [f['geometry']['coordinates']] if f['geometry']['type']=='LineString' else f['geometry']['coordinates']:
            p=np.array(part);take=(p[:,0]>10.5)&(p[:,0]<20)&(p[:,1]>53.5)&(p[:,1]<55.4)
            if take.any():
                indices=np.where(take)[0]
                for chunk in np.split(indices,np.where(np.diff(indices)>1)[0]+1):
                    if len(chunk):parts.append(p[chunk])
    return parts

def geo_read():
    im=Image.new('RGB',(1900,650),'#e0eef9');d=ImageDraw.Draw(im)
    def xy(p):return [((lon-10.5)*195,(55.4-lat)*320) for lon,lat in p]
    for p in geographic_coast():
        if len(p)>1:d.line(xy(p),fill='black',width=3)
    places=[('Darss',12.505,54.477),('Arkona',13.435,54.679),('Jasmund',13.677,54.565),('Nordperd',13.744,54.276),('Usedom',13.768,54.166),('Koserow',14.016,54.057),('Rozewie',18.335,54.833),('Hel',18.80,54.60),('Buk',11.696,54.133)]
    for name,lon,lat in places:
        x,y=xy([[lon,lat]])[0];d.ellipse((x-4,y-4,x+4,y+4),fill='red');d.text((x+7,y-4),name,fill='red',font=font(17))
    for lon in np.arange(11,20,.5):
        x=xy([[lon,55.4]])[0][0];d.line((x,0,x,650),fill='#aaaaaa');d.text((x,0),str(lon),fill='black',font=font(16))
    for lat in np.arange(53.5,55.41,.25):
        y=xy([[10.5,lat]])[0][1];d.line((0,y,1900,y),fill='#aaaaaa');d.text((0,y),str(lat),fill='black',font=font(16))
    im.save(OUT/'GEOGRAPHIC_BALTIC_READING.png')

def controls():
    _,water,_,_=physical_masks();coast=np.vstack(geographic_coast());rows=[]
    # Feature boxes fixed by separate physical readings BEFORE any fitting.
    # The target is a geographic cape extremum, never the nearest pixel to a model.
    specs=[
      ('DARSS','Darss northern cape',[12.4,54.43,12.6,54.56],[4377,720,4384,727],'north','FIT',1.2),
      ('ARKONA','Arkona northern cape',[13.3,54.63,13.52,54.73],[4390,713,4403,719],'north','FIT',1.0),
      ('BUK','Buk mainland cape',[11.6,54.10,11.8,54.2],[4359,729,4367,735],'north','FIT',1.5),
      ('HEL','Hel terminal cape',[18.73,54.56,18.86,54.65],[4519,714,4528,721],'east','FIT',1.2),
      ('FEHMARN','Fehmarn northern cape',[10.95,54.4,11.35,54.56],[4347,717,4355,725],'north','CHECK',1.6),
      ('JASMUND','Jasmund eastern cliffs',[13.60,54.49,13.74,54.62],[4403,717,4409,723],'east','CHECK',1.1),
      ('NORDPERD','Nordperd eastern cape',[13.70,54.25,13.80,54.31],[4403,723,4410,728],'east','CHECK',1.2),
      ('USEDOM','Usedom northwest cape',[13.7,54.12,13.82,54.2],[4402,730,4411,737],'north','CHECK',1.7)]
    for ident,name,gb,nb,direction,role,err in specs:
        lon0,lat0,lon1,lat1=gb;p=coast[(coast[:,0]>=lon0)&(coast[:,0]<=lon1)&(coast[:,1]>=lat0)&(coast[:,1]<=lat1)]
        axis=1 if direction=='north' else 0;geo=p[np.argmax(p[:,axis])]
        x0,y0,x1,y1=nb;ys,xs=np.where(~water[y0:y1,x0:x1]);xs=xs+x0;ys=ys+y0
        if direction=='north':take=ys==ys.min();pixel=[float(np.mean(xs[take]+.5)),float(ys.min())]
        else:take=xs==xs.max();pixel=[float(xs.max()+1),float(np.mean(ys[take]+.5))]
        rows.append(dict(ID=ident,Name=name,Role=role,Longitude=float(geo[0]),Latitude=float(geo[1]),X=pixel[0],Y=pixel[1],Reading_radius_px=err,
            Source='R3/EVIDENCE/NE_COASTLINE.geojson',Native_source='map_data/provinces.png; default.map sea_starts/lakes',
            Geographic_feature_box=gb,Native_feature_box=nb,Feature_rule=direction+' extremum of separately identified cape; raster shore edge, not cell centre',
            Stability='Modern generalized coast; cape identity is homologous, shoreline erosion and low-resolution shape included as limitations',Sector='BALTIC_NATIVE'))
    # Southern holdout is a junction topology, not a generic closest-river point.
    river_source=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'
    fs=json.loads(river_source.read_text())['features'];rv=[]
    for f in fs:
        if f['properties'].get('name')=='Warta':
            ps=[f['geometry']['coordinates']] if f['geometry']['type']=='LineString' else f['geometry']['coordinates'];rv.extend(ps)
    p=np.vstack(rv);geo=p[np.argmin(p[:,0])]
    rows.append(dict(ID='WARTA_ODER',Name='Warta Oder confluence',Role='CHECK',Longitude=float(geo[0]),Latitude=float(geo[1]),X=4426.5,Y=781.5,Reading_radius_px=1.2,
        Source=str(river_source.relative_to(ROOT)),Native_source='Vanilla rivers.png junction of east-west Warta and north-south Oder',Geographic_feature_box=[14.5,52.4,14.8,52.7],Native_feature_box=[4424,779,4429,785],
        Feature_rule='Confluence topology identified on native raster; southern extrapolation holdout, not used to fit',Stability='River regulation possible; course geometry generalized at both scales',Sector='SOUTHERN_NATIVE_CHECK'))
    dump('NATIVE_CONTROL_OBSERVATIONS.json',dict(points=rows,roles_fixed_before_fitting=True,geographic_sha256=sha(OUT.parent/'R3/EVIDENCE/NE_COASTLINE.geojson'),native_sha256=sha(ROOT/'map_data/provinces.png')))
    print(json.dumps(rows,indent=2))

def revised_controls():
    observations=load('NATIVE_CONTROL_OBSERVATIONS.json');rows=observations['points']
    # Preserve original observations and first-round errors. Visual topology review
    # shows the first Usedom box clipped Ruegen's southern tip, not Usedom.
    usedom=next(v for v in rows if v['ID']=='USEDOM');usedom['Original_X']=usedom['X'];usedom['Original_Y']=usedom['Y'];usedom['X']=4410.5;usedom['Y']=731.0
    usedom['Role']='REVISED_CHECK';usedom['Native_feature_box']=[4406,730,4413,736]
    usedom['Review']='Wrong landmass in original extrema window; corrected by USEDOM_IDENTIFICATION_REVIEW.png, no fitting to residual. Revised observation is NOT a pristine original holdout.'
    fs=json.loads((ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson').read_text())['features'];parts=[]
    for f in fs:
        if f['properties'].get('name')=='Bug':parts.append(np.array(f['geometry']['coordinates']))
    p=np.vstack(parts);geo=p[np.argmin(p[:,0])]
    rows.append(dict(ID='NAREW_VISTULA',Name='Lower Narew/Bug Vistula confluence',Role='FIT',Longitude=float(geo[0]),Latitude=float(geo[1]),X=4570.5,Y=785.5,Reading_radius_px=1.2,
        Source='MAP1C retained NaturalEarth rivers, Bug named continuous lower course',Native_source='Native river 3-way junction, southern-east reading',
        Geographic_feature_box=[20.5,52.3,20.9,52.6],Native_feature_box=[4568,783,4573,789],
        Feature_rule='Junction topology, new southern anchor; Warta Oder remains an untouched southern CHECK',
        Stability='Modern schematic waterways, not evidence for political borders1776',Sector='SOUTHERN_NATIVE_FIT'))
    dump('REVISED_CONTROL_OBSERVATIONS.json',dict(points=rows,first_round_unchanged='NATIVE_CONTROL_OBSERVATIONS.json',
        change_reason='Add distributed southern anchor to test coastal extrapolation; never promote Warta holdout into FIT. Usedom separately identified correction reported transparently.'))

def native_fit(revised=False):
    from georeference.model import project
    rows=load('REVISED_CONTROL_OBSERVATIONS.json' if revised else 'NATIVE_CONTROL_OBSERVATIONS.json')['points'];geo=np.array([[v['Longitude'],v['Latitude']] for v in rows]);pixels=np.array([[v['X'],v['Y']] for v in rows])
    fit_idx=[i for i,v in enumerate(rows) if v['Role']=='FIT'];check_idx=[i for i,v in enumerate(rows) if v['Role'] in ['CHECK','REVISED_CHECK']];models={};checks=[]
    for kind in ['geographic_affine','miller_affine','geographic_axes','miller_axes']:
        coords=project(geo,'geographic_affine' if kind.startswith('geographic') else 'miller_affine')
        x=coords[fit_idx];y=pixels[fit_idx]
        if kind.endswith('axes'):
            ab=np.linalg.lstsq(np.c_[x[:,0],np.ones(len(x))],y[:,0],rcond=None)[0];cd=np.linalg.lstsq(np.c_[x[:,1],np.ones(len(x))],y[:,1],rcond=None)[0];m=np.array([[ab[0],0],[0,cd[0]],[ab[1],cd[1]]])
        else:m=old.fit(x,y,'affine')
        pred=old.apply(coords,m);err=np.linalg.norm(pred-pixels,axis=1)
        models[kind]=dict(matrix=m.tolist(),fit_mean_px=float(err[fit_idx].mean()),fit_max_px=float(err[fit_idx].max()),
            reserved_mean_px=float(err[check_idx].mean()),reserved_max_px=float(err[check_idx].max()),fit_ids=[rows[i]['ID'] for i in fit_idx],check_ids=[rows[i]['ID'] for i in check_idx],
            forward_input_basis='lon degrees,lat degrees,1' if kind.startswith('geographic') else 'radians lon,1.25log(tan(pi/4+0.4radians(lat))),1',
            status='EMPIRICAL_LOCAL_TEST_NOT_YET_ACCEPTED',native_projection_claim=False)
        for i in check_idx:checks.append(dict(Model=kind,ID=rows[i]['ID'],Role=rows[i]['Role']+'_NEVER_IN_FIT',Observed_X=pixels[i,0],Observed_Y=pixels[i,1],Predicted_X=pred[i,0],Predicted_Y=pred[i,1],Error_px=err[i],Reading_radius_px=rows[i]['Reading_radius_px']))
    dump('REVISED_NATIVE_MODELS.json' if revised else 'NATIVE_MODELS_DIAGNOSTIC.json',models);csvout('INDEPENDENT_VALIDATION.csv' if revised else 'FIRST_ROUND_VALIDATION.csv',checks);print(json.dumps(models,indent=2))

if __name__=='__main__':{'capture':capture,'scout':scout,'geo_read':geo_read,'controls':controls,'native_fit':native_fit,'revised_controls':revised_controls,'revised_fit':lambda:native_fit(True)}[sys.argv[1]]()
