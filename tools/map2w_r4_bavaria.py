"""R4 evidence and read-only native audit. Never writes runtime or Git files."""
import collections as C
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2w_r2b_completion as prior

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reports/map/MAP2W/R4'
GAME = Path('C:/Games/Victoria 3/game')
BOX = (4310, 875, 4455, 985)
NE = ROOT / 'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def dump(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf8')

def require_captured_map():
    """Do not regenerate an old R4 diagnostic from a future functional map."""
    b=load(OUT/'BASELINE.json')
    for path in ['map_data/provinces.png','map_data/rivers.png','map_data/state_regions/00_west_europe.txt','common/history/states/00_states.txt']:
        assert sha(ROOT/path)==b['hashes'][path], 'Map has advanced since R4 capture: '+path

def snapshot():
    assert not (OUT/'BASELINE.json').exists(), 'Do not overwrite capture'
    data = dict(hashes=prior.q.economy.runtime_hashes(),
                git_head=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                git_index_sha256=sha(ROOT/'.git/index'),
                registry_sha256=sha(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),
                registry_tool_sha256=sha(ROOT/'tools/map2l_registry.py'),
                inventory=prior.core.qa.inventory())
    dump('BASELINE.json', data)
    print('Captured',len(data['hashes']),'runtime files',flush=True)

def inspect():
    require_captured_map()
    inv=load(OUT/'BASELINE.json')['inventory']
    rows=[r for r in inv['owners'] if r['key'][1] in ['STATE_BAVARIA','STATE_FRANCONIA','STATE_AUSTRIA','STATE_TIROL']]
    dump('CURRENT_OWNERS.json', rows)
    rivers=Image.open(ROOT/'map_data/rivers.png');a=np.array(rivers)
    x0,y0,x1,y1=BOX;crop=a[y0:y1,x0:x1];s=8
    color=rivers.convert('RGB').crop(BOX).resize(((x1-x0)*s,(y1-y0)*s),Image.Resampling.NEAREST)
    d=ImageDraw.Draw(color);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    for x in range(x0,x1,10):
        d.line(((x-x0)*s,0,(x-x0)*s,color.height),fill='#bcbcbc');d.text(((x-x0)*s+1,1),str(x),font=f,fill='black',stroke_width=1,stroke_fill='white')
    for y in range(y0,y1,10):
        d.line((0,(y-y0)*s,color.width,(y-y0)*s),fill='#bcbcbc');d.text((1,(y-y0)*s),str(y),font=f,fill='black',stroke_width=1,stroke_fill='white')
    color.save(OUT/'NATIVE_RIVERS.png')
    Image.open(ROOT/'map_data/provinces.png').crop(BOX).resize(color.size,Image.Resampling.NEAREST).save(OUT/'NATIVE_PROVINCES.png')
    doc=load(NE);features=[]
    canvas=Image.new('RGB',color.size,'#fafaf4');d=ImageDraw.Draw(canvas)
    bounds=(9.5,47.2,15.5,50)
    def xy(p):return ((p[0]-bounds[0])/(bounds[2]-bounds[0])*canvas.width,(bounds[3]-p[1])/(bounds[3]-bounds[1])*canvas.height)
    for r in doc['features']:
        if r['geometry']['type']!='LineString':continue
        p=np.array(r['geometry']['coordinates'])[:,:2]
        hit=(p[:,0]>bounds[0])&(p[:,0]<bounds[2])&(p[:,1]>bounds[1])&(p[:,1]<bounds[3])
        if not hit.any():continue
        features.append(dict(name=r['properties'].get('name'),id=r['properties'].get('ne_id'),source_vertices=int(hit.sum())))
        if hit.sum()<2:continue
        q=[xy(v) for v in p[hit]];d.line(q,fill='#1679b1',width=2)
        ix=len(q)//2;d.text(q[ix],str(r['properties'].get('name')),font=f,fill='black',stroke_width=1,stroke_fill='white')
    for name,p in [('Freising',(11.745,48.402)),('Passau',(13.464,48.574)),('Regensburg',(12.097,49.019)),('Werdenfels',(11.096,47.496))]:
        x,y=xy(p);d.ellipse((x-3,y-3,x+3,y+3),fill='red');d.text((x+5,y),name,font=f,fill='black')
    canvas.save(OUT/'GEOGRAPHIC_RIVERS.png')
    dump('NATIVE_INSPECTION.json',dict(box=BOX,size=rivers.size,palette_mode=rivers.mode,
         palette_counts=dict(sorted(C.Counter(map(int,crop.ravel())).items())),
         width_indices=list(range(3,16)),marker_indices=[0,1,2],
         local_mod_matches_vanilla=bool(np.array_equal(crop,np.array(Image.open(GAME/'map_data/rivers.png'))[y0:y1,x0:x1])),
         retained_geographic_source=str(NE.relative_to(ROOT)),source_sha256=sha(NE),source_features=features,
         warning='Separate geographic/native panels; no correspondence, projection or city pixel inferred by this rendering. Geographic city labels are orientation only.'))
    print('Native inspection',features,flush=True)

def survey():
    """Named physical source junctions; no city or game prediction involved."""
    import xml.etree.ElementTree as ET
    ns={'a':'http://www.adv-online.de/namespaces/adv/gid/7.1','g':'http://www.opengis.net/gml/3.2'}
    specs=[('ILLER','Iller','Donau'),('LECH','Lech','Donau'),('ISAR','Isar','Donau'),('INN','Inn','Donau'),('SALZACH','Salzach','Inn')]
    rows=[];canvas=Image.new('RGB',(1500,1000),'#fafaf6');d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for k,(ident,tributary,main) in enumerate(specs):
        p=OUT/'EVIDENCE'/(ident+'_STATION_4326.gml');root=ET.parse(p).getroot();routes=[]
        for e in root.findall('.//a:AX_Gewaesserstationierungsachse',ns):
            name=e.findtext('a:name',None,ns)
            if name not in [tributary,main]:continue
            for geom in e.findall('.//g:posList',ns):
                # EPSG:4326 formal axis order latitude, longitude verified in GML.
                coords=np.array(list(map(float,geom.text.split()))).reshape(-1,2)[:,::-1]
                routes.append(dict(name=name,id=e.get('{'+ns['g']+'}id'),points=coords))
        joins=[]
        for a in [r for r in routes if r['name']==tributary]:
            for b in [r for r in routes if r['name']==main]:
                for ai in [0,-1]:
                    for bi in [0,-1]:
                        if np.linalg.norm(a['points'][ai]-b['points'][bi])<1e-8:
                            point=a['points'][ai]
                            if not any(np.linalg.norm(np.array(j['geo'])-point)<1e-8 for j in joins):joins.append(dict(geo=point.tolist(),tributary_feature=a['id'],main_feature=b['id']))
        rows.append(dict(id=ident,name=tributary+'–'+main,source=str(p.relative_to(ROOT)),sha256=sha(p),endpoint_junctions=joins,role='UNASSIGNED_CANDIDATE',native_pixel=None))
        ox=(k%3)*500;oy=(k//3)*490;allp=np.concatenate([r['points'] for r in routes]);lo=allp.min(axis=0);hi=allp.max(axis=0)
        def xy(v):return (ox+20+(v[0]-lo[0])/(hi[0]-lo[0])*450,oy+450-(v[1]-lo[1])/(hi[1]-lo[1])*400)
        d.text((ox+15,oy+10),ident+' : axes nommés officiels',font=font,fill='black')
        for r in routes:
            col='#2478a8' if r['name']==main else '#b56b22';d.line([xy(v) for v in r['points']],fill=col,width=2)
        for j in joins:
            x,y=xy(j['geo']);d.ellipse((x-5,y-5,x+5,y+5),fill='red');d.text((ox+10,oy+465),str(j['geo']),font=font,fill='black')
    dump('SOURCE_JUNCTIONS.json',rows);canvas.save(OUT/'SOURCE_JUNCTIONS.png');print(json.dumps(rows,ensure_ascii=False),flush=True)

def context_map():
    import xml.etree.ElementTree as ET
    ns={'a':'http://www.adv-online.de/namespaces/adv/gid/7.1','g':'http://www.opengis.net/gml/3.2'}
    root=ET.parse(OUT/'EVIDENCE/MAJOR_RIVERS_CONTEXT.gml').getroot()
    colors={'Donau':'#155cbd','Inn':'#387f48','Isar':'#ae6724','Lech':'#a63991','Salzach':'#ac3926','Iller':'#21a5a5','Regen':'#6f6f6f','Naab':'#635a9a'}
    im=Image.new('RGB',(1300,900),'#fafaf5');d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    def xy(p):return ((p[0]-9.7)/4.3*1300,(49.3-p[1])/2.3*900)
    for e in root.findall('.//a:AX_Gewaesserstationierungsachse',ns):
        name=e.findtext('a:name',None,ns)
        for geom in e.findall('.//g:posList',ns):
            a=np.array(list(map(float,geom.text.split()))).reshape(-1,2)[:,::-1];q=[xy(v) for v in a];d.line(q,fill=colors[name],width=2)
    for k,name in enumerate(colors):d.text((20+k%4*310,20+k//4*25),name,font=f,fill=colors[name])
    for row in load(OUT/'SOURCE_JUNCTIONS.json'):
        for j in row['endpoint_junctions'][:1]:
            x,y=xy(j['geo']);d.ellipse((x-4,y-4,x+4,y+4),fill='black');d.text((x+5,y),row['id'],font=f,fill='black',stroke_width=1,stroke_fill='white')
    for lon in range(10,15):
        x,_=xy((lon,49));d.line((x,75,x,im.height),fill='#cccccc');d.text((x+3,80),str(lon)+' E',font=f,fill='#777777')
    for lat in [47.5,48,48.5,49]:
        _,y=xy((10,lat));d.line((0,y,im.width,y),fill='#cccccc');d.text((3,y),str(lat)+' N',font=f,fill='#777777')
    im.save(OUT/'OFFICIAL_CONTEXT.png')

def calibration():
    require_captured_map()
    import itertools
    protocol=load(OUT/'CONTROL_PROTOCOL.json');sources={r['id']:r for r in load(OUT/'SOURCE_JUNCTIONS.json')}
    raster=np.array(Image.open(ROOT/'map_data/rivers.png'));rows=[]
    for c in protocol['controls']:
        x,y=c['native_marker'];assert raster[y,x]==1
        src=sources[c['id']];points=np.array([j['geo'] for j in src['endpoint_junctions']]);assert len(points)>0
        rows.append(dict(**c,geo=points.mean(axis=0).tolist(),source_junction_alternatives=points.tolist(),native_pixel=[x+.5,y+.5],source_sha256=src['sha256']))
    fitrows=[r for r in rows if r['role']=='FIT'];checks=[r for r in rows if r['role']=='CHECK']
    X=np.array([[*r['geo'],1] for r in fitrows]);Y=np.array([r['native_pixel'] for r in fitrows]);matrix=np.linalg.solve(X,Y)
    for r in rows:
        r['predicted_pixel']=(np.r_[r['geo'],1]@matrix).tolist();r['residual_px']=float(np.linalg.norm(np.array(r['predicted_pixel'])-r['native_pixel']))
    # Only observation quantisation sensitivity. Does NOT cover modelling,
    # geographical generalisation, source-date or historical-boundary error.
    targets=[('Freising',[11.745,48.402]),('Passau',[13.464,48.574]),('Werdenfels',[11.096,47.496]),('Regensburg',[12.097,49.019])]
    sensitivity={name:[] for name,g in targets}
    holdout_sensitivity=[]
    for offsets in itertools.product([[-.5,-.5],[-.5,.5],[.5,-.5],[.5,.5]],repeat=3):
        trial=np.linalg.solve(X,Y+np.array(offsets))
        for name,g in targets:sensitivity[name].append(float(np.linalg.norm(np.r_[g,1]@(trial-matrix))))
        c=checks[0];holdout_sensitivity.append(float(np.linalg.norm(np.r_[c['geo'],1]@trial-c['native_pixel'])))
    points=[]
    for name,g in targets:
        weights=np.linalg.solve(X.T,np.r_[g,1]);p=np.r_[g,1]@matrix
        points.append(dict(name=name,geo=g,diagnostic_pixel=p.tolist(),interpolation_weights=weights.tolist(),inside_fit_triangle=bool(np.all(weights>=0)),quantisation_sensitivity_max_px=max(sensitivity[name]),actual_total_position_uncertainty_px=None,not_accepted_city_location=True))
    data=dict(status='DIAGNOSTIC_NOT_INSTALLATION_PROFILE',formula='[longitude_deg,latitude_deg,1] @ matrix = [bitmap_x,bitmap_y]',matrix=matrix.tolist(),parameters=6,fit_count=3,independent_check_count=len(checks),controls=rows,independent_mean_px=float(np.mean([r['residual_px'] for r in checks])),independent_max_px=max(r['residual_px'] for r in checks),check_fit_quantisation_sensitivity_residual_range=[min(holdout_sensitivity),max(holdout_sensitivity)],city_diagnostics=points,certified_error_bound_px=None,protocol_sha256=sha(OUT/'CONTROL_PROTOCOL.json'),no_hub_or_inherited_model_used=True,no_second_optimisation=True)
    dump('CALIBRATION.json',data);print(json.dumps(data,ensure_ascii=False),flush=True)

def assessment():
    require_captured_map()
    inv=load(OUT/'BASELINE.json')['inventory'];cal=load(OUT/'CALIBRATION.json')
    image=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=(image[:,:,0]<<16)|(image[:,:,1]<<8)|image[:,:,2]
    owner={r['key'][0]:r['key'][2] for r in inv['owners']};regions=inv['geometry']
    region_raw=(ROOT/'map_data/state_regions/00_west_europe.txt').read_text(encoding='utf-8-sig')
    ids={n.key:n.one('id') for n in prior.core.cw.parse(region_raw) if n.key.startswith('STATE_')}
    diagnostics=[]
    for row in cal['city_diagnostics']:
        x,y=np.floor(row['diagnostic_pixel']).astype(int);rgb='x'+format(int(packed[y,x]),'06X');s=regions.get(rgb)
        crop=packed[y-8:y+9,x-8:x+9];values,counts=np.unique(crop,return_counts=True)
        diagnostics.append(dict(name=row['name'],diagnostic_only=True,not_city_or_sovereignty_validation=True,
          diagnostic_pixel=row['diagnostic_pixel'],sampled_RGB=rgb,State=s,State_ID=ids.get(s),Owner_TAG=owner.get(rgb),
          search_window=[int(x-8),int(y-8),int(x+9),int(y+9)],
          intersecting_RGBs=[dict(rgb='x'+format(int(v),'06X'),window_cells=int(c),state=regions.get('x'+format(int(v),'06X')),owner=owner.get('x'+format(int(v),'06X'))) for v,c in zip(values,counts)]))
    vals,cnts=np.unique(packed,return_counts=True);counts={'x'+format(int(v),'06X'):int(c) for v,c in zip(vals,cnts)}
    eic=[dict(rgb=r['key'][0],state=r['key'][1],owner=r['key'][2],pixels=counts.get(r['key'][0],0)) for r in inv['owners'] if r['key'][2]=='EIC']
    det=abs(float(np.linalg.det(np.array(cal['matrix'])[:2,:])));cell_km2=111.32**2*np.cos(np.radians(48.7))/det
    screening=dict(source_area_km2_approx=900,source='HLB Passau territorial history, early-modern immediate total including detached possessions; not a precise 1776 census of area',candidate_affine_cell_area_km2=float(cell_km2),area_equivalent_pixels=float(900/cell_km2),maximum_possible_inscribed_disk_radius_px_under_area_assumption=float(np.sqrt(900/cell_km2/np.pi)),measured_single_holdout_residual_px=cal['independent_max_px'],limitation='Area-only upper-bound screening, NOT an accepted territorial polygon, local error bound or uniform scale certificate. Observed error is comparable to even the theoretical best-case interior radius; no locally verified northern core margin. No arbitrary erosion/transfer.')
    dump('GEOGRAPHIC_ASSESSMENT.json',dict(status='NO_ACCEPTED_TERRITORIAL_GEOMETRY',diagnostic_windows=diagnostics,installed_eichstaett=eic,passau_area_screening=screening,certainty='Sovereignty established for principal entities; bitmap allocation unresolved',accepted_polygons=[],accepted_RGB_transfers=[]))
    dump('TERRITORIAL_CHANGES.json',dict(status='MAP2W_R4_BLOCKED',transfers=[],new_countries=[],new_RGBs=[],changed_cells=0,reason='Independent physical test fails to support territorial margin; see CALIBRATION.json and GEOGRAPHIC_ASSESSMENT.json'))
    print('Preserved Eichstaett',eic,'area screening',screening,flush=True)

def comparison():
    require_captured_map()
    import xml.etree.ElementTree as ET
    cal=load(OUT/'CALIBRATION.json');M=np.array(cal['matrix']);x0,y0,x1,y1=BOX;s=7
    # Left native panel: no smoothing, palette includes all 13 river widths.
    a=np.array(Image.open(ROOT/'map_data/rivers.png'));im=Image.new('RGB',(1530,1050),'#faf9f4');d=ImageDraw.Draw(im)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13);title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',22)
    d.text((20,15),'R4 — contrôle physique indépendant : écart de 4,67 pixels, aucun transfert',font=title,fill='#203544')
    base=(25,100)
    def native(p):return (base[0]+(p[0]-x0)*s,base[1]+(p[1]-y0)*s)
    d.rectangle((base[0],base[1],base[0]+(x1-x0)*s,base[1]+(y1-y0)*s),fill='white')
    yy,xx=np.where(np.isin(a[y0:y1,x0:x1],range(3,16))|np.isin(a[y0:y1,x0:x1],[0,1,2]))
    for y,x in zip(yy,xx):
        u,v=native((x+x0,y+y0));d.rectangle((u,v,u+s-1,v+s-1),fill='#3184b0')
    # Red outline = independent geographic source sent through the REJECTED
    # diagnostic affine. Not a new river or boundary proposal.
    ns={'a':'http://www.adv-online.de/namespaces/adv/gid/7.1','g':'http://www.opengis.net/gml/3.2'}
    for e in ET.parse(OUT/'EVIDENCE/MAJOR_RIVERS_CONTEXT.gml').findall('.//a:AX_Gewaesserstationierungsachse',ns):
        if e.findtext('a:name',None,ns) not in ['Donau','Inn','Salzach','Lech','Isar']:continue
        for geom in e.findall('.//g:posList',ns):
            p=np.array(list(map(float,geom.text.split()))).reshape(-1,2)[:,::-1];q=np.column_stack([p,np.ones(len(p))])@M
            if not ((q[:,0]>=x0)&(q[:,0]<x1)&(q[:,1]>=y0)&(q[:,1]<y1)).all():continue
            d.line([native(v) for v in q],fill='#c785a4',width=1)
    for r in cal['controls']:
        u,v=native(r['native_pixel']);color='#215b29' if r['role']=='FIT' else '#b23422';d.ellipse((u-6,v-6,u+6,v+6),outline=color,width=3);d.text((u+8,v-23),r['id']+' '+r['role'],font=f,fill=color,stroke_width=1,stroke_fill='white')
        if r['role']=='CHECK':
            p=native(r['predicted_pixel']);d.line((u,v,*p),fill=color,width=3);d.line((p[0]-5,p[1]-5,p[0]+5,p[1]+5),fill=color,width=2);d.line((p[0]-5,p[1]+5,p[0]+5,p[1]-5),fill=color,width=2)
    for x in range(x0,x1,20):
        u,v=native((x,y0));d.text((u,v-20),str(x),font=small,fill='#444444')
    for y in range(y0,y1,10):
        u,v=native((x0,y));d.text((u,v),str(y),font=small,fill='#444444')
    # Source scan is deliberately NOT overlaid on the game.
    scan=Image.open(OUT/'EVIDENCE/BSB_1791_READING.jpg');scan.thumbnail((450,420));im.paste(scan,(1060,115));d=ImageDraw.Draw(im)
    lines=['Carte historique BSB, 1791','Passau / Freising / Werdenfels','Non calée sur le bitmap.','Variations 1765–1782 à distinguer.','','Bleu : rivières natives actives','Rose : source physique projetée','dans le modèle diagnostique rejeté','Vert : 3 points FIT (interpolation)','Rouge : Isar, contrôle hors calcul','','4,67 px : résidu observé sur 1 point','Pas une erreur maximale certifiée.','Aucun ancien hub utilisé.','Aucune frontière modifiée.']
    for i,line in enumerate(lines):d.text((1065,535+i*24),line,font=f,fill='#333333')
    d.text((25,925),'Les sources réelles et le raster n’ont pas la même généralisation. Aucun nouveau profil territorial accepté.',font=f,fill='#333333')
    d.text((25,955),'Les diagnostics urbains, sans contrôle local propre, ne sont pas des positions validées des villes.',font=f,fill='#333333')
    im.save(OUT/'CALIBRATION_COMPARISON.png')
    # Honest before/after map: identical functional state. No invented polygons.
    box=(4325,880,4425,950);sx=6;w=(box[2]-box[0])*sx;h=(box[3]-box[1])*sx
    arr=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);p=(arr[:,:,0]<<16)|(arr[:,:,1]<<8)|arr[:,:,2];inv=load(OUT/'BASELINE.json')['inventory'];owners={int(r['key'][0][1:],16):r['key'][2] for r in inv['owners']}
    colours={'BAV':(202,191,150),'AUS':(204,213,220),'EIC':(87,175,146),'ANS':(127,169,210),'FBM':(181,145,186),'NUR':(161,189,170),'WZB':(219,182,166),'SAG':(184,159,118)}
    crop=p[box[1]:box[3],box[0]:box[2]];paint=np.zeros((*crop.shape,3),dtype=np.uint8)
    for val in np.unique(crop):paint[crop==val]=colours.get(owners.get(int(val)),(175,175,175))
    edges=np.zeros(crop.shape,dtype=bool);edges[1:]|=crop[1:]!=crop[:-1];edges[:,1:]|=crop[:,1:]!=crop[:,:-1];paint[edges]=(103,103,103)
    water=np.isin(a[box[1]:box[3],box[0]:box[2]],range(3,16))|np.isin(a[box[1]:box[3],box[0]:box[2]],[0,1,2]);paint[water]=(45,120,175)
    panel=Image.fromarray(paint).resize((w,h),Image.Resampling.NEAREST);both=Image.new('RGB',(2*w+60,h+180),'#faf9f4');bd=ImageDraw.Draw(both)
    both.paste(panel,(20,65));both.paste(panel,(40+w,65));bd.text((20,20),'AVANT R4 — état actif capturé',font=title,fill='#203544');bd.text((40+w,20),'APRÈS R4 — identique (0 cellule modifiée)',font=title,fill='#203544')
    bd.text((20,h+85),'Souverainetés historiques manquantes : non installées. Ne pas lire les propriétaires actuels comme une certification de 1776.',font=f,fill='#333333')
    bd.text((20,h+115),'Bavière : beige | Autriche : gris clair | Eichstätt : vert. Contours internes : RGB actuels. Aucun centre urbain validé ici.',font=f,fill='#333333')
    both.save(OUT/'BEFORE_AFTER.png')

def verify():
    b=load(OUT/'BASELINE.json');inv=prior.core.qa.inventory();current=prior.q.economy.runtime_hashes()
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    # Explicit paths actually observed during this turn, not a folder waiver.
    external={
      'common/decisions/1776_usa_minutemen_reform.txt',
      'common/journal_entries/06_usa_independence_mod.txt',
      'common/laws/1776_usa_reorganized_militia.txt',
      'common/scripted_effects/1776_usa_content_r1.txt',
      'common/scripted_effects/1776_usa_minutemen_reform.txt',
      'common/scripted_triggers/1776_usa_minutemen_reform.txt',
      'events/1776_usa_minutemen_reform.txt',
      'localization/english/1776_usa_minutemen_reform_l_english.yml',
      'localization/french/1776_usa_minutemen_reform_l_french.yml',
    }
    observed=[]
    for path in sorted(set(changed)&external):
        p=ROOT/path;raw=p.read_text(encoding='utf-8-sig') if p.exists() else ''
        if path.endswith('.txt') and raw:prior.core.cw.parse(raw)
        observed.append(dict(path=path,captured_sha256=b['hashes'].get(path),observed_sha256=current.get(path),contains_MAP_R4_identifier='map2w_r4' in raw.lower(),scope='Concurrent USA/FRA work observed, never written/restored by R4; not functionally certified by this protection check'))
    dump('CONCURRENT_OBSERVATION.json',dict(files=observed,unexpected_paths=sorted(set(changed)-external),baseline_not_rewritten=True))
    checks=[]
    def check(name,passed,detail=None):checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('Every runtime path outside explicit observed concurrent list unchanged',not(set(changed)-external),sorted(set(changed)-external))
    check('No MAP R4 identifier introduced in concurrent files',not any(r['contains_MAP_R4_identifier'] for r in observed))
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('Imperial registry unchanged',sha(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json')==b['registry_sha256'])
    check('Registry compiler unchanged',sha(ROOT/'tools/map2l_registry.py')==b['registry_tool_sha256'])
    for key in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','buildings','building_levels_written','units']:
        check('Effective inventory preserved: '+key,inv[key]==b['inventory'][key])
    check('Preexisting duplicate RGBs exactly preserved',inv['duplicates']==b['inventory']['duplicates'] and len(inv['duplicates'])==44)
    check('Preexisting invalid references exactly preserved',inv['errors']==b['inventory']['errors'] and len(inv['errors'])==12)
    registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json');check('567 registry RGBs retained',len(registry)==567)
    from map2k_patch import ELECTORS
    check('Nine electors retained',len(ELECTORS)==9)
    check('R3 still withdrawn',not (OUT.parent/'R3/REGISTRY_MIGRATION.json').exists() and not({'HLN','HKI'}&set(inv['countries'])) and not any('xEDB9'+format(i,'02X') in inv['geometry'] for i in range(4)))
    transfers=load(OUT/'TERRITORIAL_CHANGES.json');check('No territorial implementation falsely claimed',not transfers['transfers'] and transfers['changed_cells']==0 and not (OUT/'REGISTRY_MIGRATION.json').exists())
    check('No installation calibration accepted',load(OUT/'CALIBRATION.json')['certified_error_bound_px'] is None)
    before=sum(r['count'] for r in b['inventory']['pops']);after=sum(r['count'] for r in inv['pops'])
    dump('POPULATION_VALIDATION.json',dict(status='PASS_UNCHANGED' if inv['regional_pop']==b['inventory']['regional_pop'] and before==after else 'FAIL',world_before=before,world_after=after,population_profiles_unchanged=inv['pops']==b['inventory']['pops'],regional_profiles_unchanged=inv['regional_pop']==b['inventory']['regional_pop'],new_people=0,transferred_people=0,building_profiles_unchanged=inv['buildings']==b['inventory']['buildings'],units_unchanged=inv['units']==b['inventory']['units'],reason='No R4 territorial modification, no artificial population. Concurrent reform scripts are not evaluated as runtime execution.'))
    dump('EVIDENCE_MANIFEST.json',dict(files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted((OUT/'EVIDENCE').iterdir()) if p.is_file()],no_vanilla_write=True))
    data=dict(status='PASS_READ_ONLY_R4_PROTECTION' if all(r['passed'] for r in checks) else 'PROTECTION_REVIEW_REQUIRED',territorial_status='MAP2W_R4_BLOCKED',checks=checks,passed=sum(r['passed'] for r in checks),total=len(checks),current_runtime_file_count=len(current),concurrent_paths_observed=len(observed),runtime_union_paths=len(set(current)|set(b['hashes'])),preexisting_duplicate_RGB_count=len(inv['duplicates']),preexisting_invalid_reference_count=len(inv['errors']),engine_test_executed=False,new_territorial_runtime_validation='NOT_APPLICABLE_NO_INSTALL',historical_geometry_validated=False,new_regressions_detected=not all(r['passed'] for r in checks),baseline_immutable=True)
    dump('VALIDATION.json',data);print('Protection',data['passed'],'/',data['total'],'concurrent observed',len(observed),flush=True)
    assert all(r['passed'] for r in checks),[r for r in checks if not r['passed']]

def tests():
    import io,unittest
    modules=['test_map2w_r4_bavaria','test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration']
    suite=unittest.defaultTestLoader.loadTestsFromNames(modules);stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=1).run(suite)
    dump('TESTS.json',dict(status='PASS' if result.wasSuccessful() else 'FAIL',modules=modules,run=result.testsRun,failures=[dict(test=str(t),traceback=s) for t,s in result.failures],errors=[dict(test=str(t),traceback=s) for t,s in result.errors],skipped=[dict(test=str(t),reason=s) for t,s in result.skipped],output=stream.getvalue(),engine_execution=False))
    print(stream.getvalue(),flush=True);assert result.wasSuccessful()

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
