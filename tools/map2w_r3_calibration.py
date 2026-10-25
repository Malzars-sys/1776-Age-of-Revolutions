"""Read-only physical investigation, independent of the withdrawn R3 installer."""
import collections as C
import hashlib,json,math,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from georeference.model import forward,fit,evaluate
import map2w_r2b_completion as prior
ROOT=Path(__file__).resolve().parents[1];GAME=Path('C:/Games/Victoria 3/game')
OUT=ROOT/'docs/reports/map/MAP2W/R3/CALIBRATION'
NE=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson'
BOX=(4260,845,4370,925)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def snapshot():
    dest=OUT/'BASELINE.json';assert not dest.exists(),'Never overwrite calibration capture'
    data=dict(hashes=prior.q.economy.runtime_hashes(),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=sha(ROOT/'.git/index'),rivers_mod=sha(ROOT/'map_data/rivers.png'),rivers_vanilla=sha(GAME/'map_data/rivers.png'),provinces=sha(ROOT/'map_data/provinces.png'))
    dump(dest.name,data);print('Read-only capture',len(data['hashes']),'runtime files',flush=True)
def model():return load(ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json')['model']
def inspect():
    palette=Image.open(ROOT/'map_data/rivers.png');a=np.array(palette);assert palette.mode=='P'
    definitions=(GAME/'common/defines/jomini/rivers.txt').read_text(encoding='utf-8-sig');print(definitions)
    original=Image.open(GAME/'map_data/rivers.png');print('Rivers',palette.mode,palette.size,'mod==vanilla',sha(ROOT/'map_data/rivers.png')==sha(GAME/'map_data/rivers.png'))
    width=np.isin(a,np.arange(3,16));markers=np.isin(a,[0,1,2]);x0,y0,x1,y1=BOX;local=a[y0:y1,x0:x1];colors=palette.getpalette();counts=C.Counter(map(int,local.ravel()))
    dump('NATIVE_PALETTE.json',dict(mode=palette.mode,size=list(palette.size),box=BOX,indices=[dict(index=i,rgb=colors[i*3:i*3+3],count=n,river_width=3<=i<=15,marker=i in [0,1,2]) for i,n in sorted(counts.items())],definition=definitions,mod_matches_vanilla=sha(ROOT/'map_data/rivers.png')==sha(GAME/'map_data/rivers.png')))
    scale=9;im=Image.new('RGB',((x1-x0)*scale,(y1-y0)*scale),'#fbfaf7');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    for y,x in zip(*np.where(width[y0:y1,x0:x1])):d.rectangle((x*scale,y*scale,(x+1)*scale-1,(y+1)*scale-1),fill='#2173b8')
    for y,x in zip(*np.where(markers[y0:y1,x0:x1])):d.rectangle((x*scale,y*scale,(x+1)*scale-1,(y+1)*scale-1),fill=['#22a43b','#df3b31','#d4ab33'][int(local[y,x])])
    for x in range(x0,x1,5):d.line(((x-x0)*scale,0,(x-x0)*scale,im.height),fill='#dddddd');d.text(((x-x0)*scale+2,1),str(x),font=font,fill='black')
    for y in range(y0,y1,5):d.text((1,(y-y0)*scale),str(y),font=font,fill='black',stroke_width=1,stroke_fill='white')
    rivers=[];m=model()
    for r in load(NE)['features']:
        if r['geometry']['type']!='LineString':continue
        p=np.array(r['geometry']['coordinates'])[:,:2];take=(p[:,0]>=7.5)&(p[:,0]<=12)&(p[:,1]>=48.3)&(p[:,1]<=50.5)
        if not np.any(take):continue
        name=r['properties'].get('name');rivers.append(dict(name=name,id=r['properties'].get('ne_id'),vertices=int(take.sum()),bounds=[p[take].min(axis=0).tolist(),p[take].max(axis=0).tolist()]))
        q=forward(m,p[take]);points=[((u-x0)*scale,(v-y0)*scale) for u,v in q]
        if len(q)>1:d.line(points,fill='#b949a1',width=2)
        for u,v in points:
            if 10<u<im.width-60 and 10<v<im.height-20:d.text((u+3,v),str(name),font=font,fill='#9b287a',stroke_width=1,stroke_fill='white');break
    dump('RETAINED_HYDROGRAPHY.json',dict(source=str(NE.relative_to(ROOT)),sha256=sha(NE),rivers=rivers))
    for row in load(OUT.parent/'CITY_DIAGNOSTIC.json')[:7]:
        u,v=row['diagnostic_pixel'];u=(u-x0)*scale;v=(v-y0)*scale;d.ellipse((u-3,v-3,u+3,v+3),fill='black');d.text((u+5,v),row['name'],font=font,fill='black',stroke_width=1,stroke_fill='white')
    im.save(OUT/'NATIVE_NE_DIAGNOSTIC.png');print(json.dumps(rivers,ensure_ascii=False),flush=True)
    # A separate unannotated reference for careful manual feature reading.
    Image.open(ROOT/'map_data/rivers.png').convert('RGB').crop(BOX).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST).save(OUT/'NATIVE_RIVERS_RAW.png')

def physics():
    """Inventory physical candidates; never turn a nearest pixel into a GCP."""
    p=OUT/'AWGN_JAGST_KOCHER_NECKAR.geojson';doc=load(p)
    routes={r['properties']['GEW_NAME']:np.array(r['geometry']['coordinates'])[:,:2] for r in doc['features']}
    assert set(routes)=={'Jagst','Kocher','Neckar'} and len(doc['features'])==3
    specifications=[
      ('P1','Confluent Jagst–Neckar','Jagst','FIT_CANDIDATE',None,'first_endpoint'),
      ('P2','Confluent Kocher–Neckar','Kocher','FIT_CANDIDATE',None,'first_endpoint'),
      ('P3','Boucle Jagst près de Bächlingen','Jagst','FIT_CANDIDATE',(9.82,49.23,9.89,49.27),'maximum_turn_over_700m_in_window'),
      ('P4','Boucle Kocher près de Künzelsau','Kocher','FIT_CANDIDATE',(9.67,49.26,9.73,49.31),'maximum_turn_over_700m_in_window'),
      ('P5','Coude Jagst près de Kirchberg','Jagst','CHECK_RESERVED',(9.95,49.185,10.01,49.22),'maximum_turn_over_700m_in_window'),
      ('P6','Coude Kocher près de Schwäbisch Hall','Kocher','CHECK_RESERVED',(9.72,49.095,9.77,49.13),'maximum_turn_over_700m_in_window')]
    a=np.array(Image.open(ROOT/'map_data/rivers.png'));vanilla=np.array(Image.open(GAME/'map_data/rivers.png'));markers=np.isin(a,[0,1,2]);width=np.isin(a,np.arange(3,16));mask=markers|width
    x0,y0,x1,y1=BOX;yy,xx=np.where(mask[y0:y1,x0:x1]);native=np.column_stack([xx+x0+.5,yy+y0+.5]);m=model();hyp=load(ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json')['model'];rows=[]
    for ident,name,river,role,bounds,rule in specifications:
        route=routes[river]
        if bounds:
            lo,la,hi,ha=bounds;inside=(route[:,0]>=lo)&(route[:,0]<=hi)&(route[:,1]>=la)&(route[:,1]<=ha);assert np.any(inside)
            # Physical curve candidate selected from geography alone. Angles
            # use points 350 m along the river on either side, never a game
            # prediction, a city locator or an edge of the sampling window.
            km=route*np.array([111.32*math.cos(math.radians(49.25)),111.32]);s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(km,axis=0),axis=1))]
            left=np.column_stack([np.interp(s-.35,s,km[:,k]) for k in [0,1]]);right=np.column_stack([np.interp(s+.35,s,km[:,k]) for k in [0,1]])
            u=left-km;v=right-km;cos=np.sum(u*v,axis=1)/(np.linalg.norm(u,axis=1)*np.linalg.norm(v,axis=1)+1e-15);eligible=np.where(inside)[0];ix=eligible[np.argmax(cos[eligible])];geo=route[ix];vertex_count=len(eligible)
        else:geo=route[0];vertex_count=1
        predicted=forward(m,[geo])[0];other=forward(hyp,[geo])[0]
        distances=np.linalg.norm(native-predicted,axis=1)
        feature=next(r for r in doc['features'] if r['properties']['GEW_NAME']==river)
        rows.append(dict(id=ident,name=name,river=river,role=role,source='AWGN LUBW modern physical network, NOT 1776 political boundary',object_id=feature['properties']['OBJECTID'],source_selection_rule=rule,source_window=bounds,source_vertices_examined=vertex_count,geo=geo.tolist(),diagnostic_miller_pixel=predicted.tolist(),unfitted_native_hypothesis_pixel=other.tolist(),candidate_models_disagreement_px=float(np.linalg.norm(predicted-other)),nearest_any_native_river_distance_px=float(distances.min()),native_homolog_pixel=None,used_for_fit=False,used_for_independent_validation=False,matched_residual_px=None,rejection='No identifiable Jagst/Kocher/Neckar river branch in the inspected native local network; neither nearest blue pixel nor projected coordinate is a correspondence.'))
    source_summary=[dict(name=n,vertices=len(r),first=r[0].tolist(),last=r[-1].tolist()) for n,r in routes.items()]
    # Full local palette audit, not just blue shades. Expanded corridor covers
    # both former proposals and their plausible several-pixel disagreement.
    corridor=(4300,870,4340,892);cx0,cy0,cx1,cy1=corridor;crop=a[cy0:cy1,cx0:cx1]
    unknown=[int(i) for i in np.unique(crop) if int(i) not in [0,1,2,254,255] and not 3<=i<=15]
    source_confluence_separation=float(np.linalg.norm(forward(m,[routes['Jagst'][0]])[0]-forward(m,[routes['Kocher'][0]])[0]))
    dump('PHYSICAL_LANDMARKS.json',dict(status='NO_NATIVE_LOCAL_HOMOLOGUES_ACCEPTED',landmarks=rows,source_geometry=source_summary,source_sha256=sha(p),requested_output_crs='EPSG:4326',service_native_crs='EPSG:25832',actual_fit_pairs=0,actual_independent_check_pairs=0,planned_fit_candidates=4,reserved_check_candidates=2,model_fitted=False,accepted_profile=None,local_independent_mean_px=None,local_independent_max_px=None,local_error_bound_px=None,confidence_interval=None,quantisation_component_only='For a uniquely identified cell observation, using its centre introduces up to +/-0.5 pixel per axis. Does not bound identification, source age, generalisation or model errors.',corridor_box=corridor,corridor_native_river_pixels=int(mask[cy0:cy1,cx0:cx1].sum()),corridor_all_nonbackground_pixels=int(np.count_nonzero(~np.isin(crop,[254,255]))),corridor_unknown_palette_indices=unknown,local_mod_equals_vanilla=bool(np.array_equal(a[y0:y1,x0:x1],vanilla[y0:y1,x0:x1])),mouths_separation_in_diagnostic_pixels=source_confluence_separation,warning='Modern hydrography is an independent physical source, not an independent native pixel observation. Nearest-river distances and model disagreements are diagnostics, not positional residuals or accuracy bounds.'))
    # Read-only local relief inspection; packed runtime height is sampled with
    # the existing verified Poel tile convention, not a guessed PNG flip.
    Image.MAX_IMAGE_PIXELS=150_000_000
    height=np.array(Image.open(ROOT/'map_data/heightmap.png'));packed=np.array(Image.open(ROOT/'map_data/packed_heightmap.png'));ind=np.array(Image.open(GAME/'map_data/indirection_heightmap.png'));samples=[]
    for hy in range(2*cy0,2*cy1,4):
        for hx in range(2*cx0,2*cx1,4):
            tx,ty=hx//64,(hy+1)//64;r,g,step,level=map(int,ind[ty,tx]);n=64//step+1
            if (hx-tx*64)%step or (hy-(ty*64-1))%step:continue
            px=r*n+(hx-tx*64)//step;py=packed.shape[0]-[0,6695,7569,7662,7680][level]-(g+1)*n+(hy-(ty*64-1))//step
            samples.append(dict(source=[hx,hy],packed=[px,py],source_height=int(height[hy,hx]),packed_height=int(packed[py,px]),step=step,level=level))
    box=(2*cx0,2*cy0,2*cx1,2*cy1);raster=height[box[1]:box[3],box[0]:box[2]].astype(float);normalized=np.uint8(np.round((raster-raster.min())/(raster.max()-raster.min())*255));relief=Image.fromarray(normalized).convert('RGB').resize((800,440),Image.Resampling.NEAREST);relief.save(OUT/'LOCAL_RELIEF_DIAGNOSTIC.png')
    dump('RELIEF_INSPECTION.json',dict(box_native=corridor,heightmap_size=list(height.shape[::-1]),packed_size=list(packed.shape[::-1]),sample_count=len(samples),sampled_mean_abs_difference=float(np.mean([abs(r['source_height']-r['packed_height']) for r in samples])) if samples else None,sampled_max_abs_difference=max([abs(r['source_height']-r['packed_height']) for r in samples],default=None),samples=samples,accepted_geographic_summits_or_valley_controls=0,source_min=int(raster.min()),source_max=int(raster.max()),limitation='Relative grayscale range, not metres. Relief has no self-identifying geographic point here. No geographic DEM tied to a native homologous summit/valley; no FIT or CHECK created from raster extrema.'))
    print('Physical candidates',len(rows),'accepted FIT 0, CHECK 0; corridor river pixels',int(mask[cy0:cy1,cx0:cx1].sum()),'mouths separation',source_confluence_separation,flush=True)

def origins():
    old=load(ROOT/'docs/reports/map/MAP2L/FRANCONIA/ALIGNMENT.json');m=model();sheet=load(OUT.parent/'SOURCE_ALIGNMENT.json');cities=load(OUT.parent/'CITY_DIAGNOSTIC.json');M=np.array(old['matrix_source_to_game']);fits=[r for r in old['points'] if r['role']=='FIT'];T=np.linalg.lstsq(np.array([[*r['source'],1] for r in fits]),np.array([r['game'] for r in fits]),rcond=None)[0];assert np.allclose(T,M)
    anchors=load(ROOT/'docs/reports/map/MAP2L/FRANCONIA/NATIVE_ANCHORS.json');old_roles=[]
    for r in old['points']:
        native=next((a for a in anchors if np.linalg.norm(np.array([float(a['Locator_X']),float(a['Locator_Y'])])-r['game'])<.001),None)
        old_roles.append(dict(name=r['name'],role=r['role'],source=r['source'],game=r['game'],native_hub_type=native['Hub_Type'] if native else None,native_hub_label=native['Hub_Name'] if native else None,geodetic_ground_truth=False,residual_px=r['error_game_px']))
    mfit=[r for r in m['controls'] if r['role']=='FIT'];target_rows=[]
    for r in cities[:7]:target_rows.append(dict(name=r['name'],geo=r['geo'],pixel=r['diagnostic_pixel'],outside_fit_latitude=not(m['domain'][0][1]<=r['geo'][1]<=m['domain'][1][1]),south_of_fit_domain_degrees=max(0,m['domain'][0][1]-r['geo'][1])))
    ev=evaluate(m)
    dump('REFERENCE_ORIGINS.json',dict(status='NEITHER_FRAME_IS_LOCAL_PHYSICAL_GROUND_TRUTH',old_scan=dict(source=old['source'],source_sha256=old['source_sha256'],formula='[scan_x,scan_y,1] @ matrix = [bitmap_x,bitmap_y]',matrix=M.tolist(),parameters=6,fit_points=3,unique_affine_exactly_reproduced=True,anchors=old_roles,source_projection='Historical engraved scan; no exact geographical projection established. Paper/engraving distortions not removed.',warning='"surveyed native hubs" in the old method field means read positions in the game, NOT geodetically surveyed cities. Leave previous work unchanged.'),miller=dict(formula='p=[radians(lon),1.25*log(tan(pi/4+0.4*radians(lat)))]; pixel=p@A+b',matrix=m['matrix'],parameters=6,fit_points=5,anchors=mfit,domain=m['domain'],evaluation={'fit':ev['fit'],'check':ev['check'],'leave_one_out':ev['leave_one_out']},warning='Five unsurveyed city locators fitted north of Hohenlohe; affine cross-terms and extrapolation can propagate hub displacement. Miller is an empirical basis, not proof of engine projection.'),r3_sheet=dict(matrix=sheet['transform'],fit_points=sheet['controls'],checks=sheet['independent_sheet_checks'],warning='SVG -> three pixels PREDICTED by the inherited Miller model. No new native observation; tiny sheet residuals are correlated with the same parent model.'),targets=target_rows,source_svg_crs='Undeclared in SVG metadata; source coordinates have nominal map units, not asserted to be EPSG:25832 or GK3.',no_global_model_modified=True))
    print('Frame origins and exact transforms recorded',flush=True)

def map_evidence():
    """Scientific diagnostic panels, no edits to source map assets."""
    evidence=load(OUT/'PHYSICAL_LANDMARKS.json');doc=load(OUT/'AWGN_JAGST_KOCHER_NECKAR.geojson');m=model();hyp=load(ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json')['model']
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',22)
    image=Image.new('RGB',(1550,1050),'#faf9f4');d=ImageDraw.Draw(image)
    d.text((25,15),'R3-CALIBRATION — six repères examinés, aucune homologie locale acceptée',font=bold,fill='#213748')
    d.text((25,58),'Source physique indépendante : AWGN / LUBW, WGS84',font=font,fill='#213748');d.text((815,58),'Raster fluvial natif + hypothèses non validées',font=font,fill='#213748')
    left=(35,110,755,650);lo,la,hi,ha=(9.1,49.07,10.1,49.41)
    def geo_xy(p):return (left[0]+(p[0]-lo)/(hi-lo)*(left[2]-left[0]),left[3]-(p[1]-la)/(ha-la)*(left[3]-left[1]))
    for lon in np.arange(9.1,10.11,.2):
        x,_=geo_xy([lon,la]);d.line((x,left[1],x,left[3]),fill='#deded5');d.text((x-12,left[3]+7),f'{lon:.1f}°E',font=small,fill='#333333')
    for lat in [49.1,49.2,49.3,49.4]:
        _,y=geo_xy([lo,lat]);d.line((left[0],y,left[2],y),fill='#deded5');d.text((left[0],y-17),f'{lat:.1f}°N',font=small,fill='#333333')
    layer=Image.new('RGB',(left[2]-left[0]+1,left[3]-left[1]+1),'#f5f7f0');ld=ImageDraw.Draw(layer)
    for r in doc['features']:
        p=np.array(r['geometry']['coordinates'])[:,:2];pts=[(u-left[0],v-left[1]) for u,v in map(geo_xy,p)];name=r['properties']['GEW_NAME'];color={'Jagst':'#227fad','Kocher':'#168b69','Neckar':'#7899a8'}[name];ld.line(pts,fill=color,width=3)
    image.paste(layer,(left[0],left[1]));d=ImageDraw.Draw(image)
    for lon in np.arange(9.1,10.11,.2):
        x,_=geo_xy([lon,la]);d.line((x,left[1],x,left[3]),fill='#e3e3db')
    for lat in [49.1,49.2,49.3,49.4]:
        _,y=geo_xy([lo,lat]);d.line((left[0],y,left[2],y),fill='#e3e3db');d.text((left[0],y-17),f'{lat:.1f}°N',font=small,fill='#333333')
    for row in evidence['landmarks']:
        x,y=geo_xy(row['geo']);check=row['role']=='CHECK_RESERVED';col='#ad4e1b' if check else '#273a55';d.ellipse((x-5,y-5,x+5,y+5),fill=col);offset=(-5,-25) if row['id']=='P1' else (7,4);d.text((x+offset[0],y+offset[1]),row['id']+(' réservé' if check else ''),font=font,fill=col,stroke_width=2,stroke_fill='white')
    d.text((525,160),'Jagst',font=font,fill='#227fad');d.text((440,540),'Kocher',font=font,fill='#168b69')
    # Integer native cells are shown without an interpolation or photo layer.
    box=(4280,848,4355,908);sx=9;x0,y0,x1,y1=box;top=(820,110);arr=np.array(Image.open(ROOT/'map_data/rivers.png'))[y0:y1,x0:x1];native=Image.new('RGB',((x1-x0)*sx,(y1-y0)*sx),'#f5f4ef');nd=ImageDraw.Draw(native)
    for y,x in zip(*np.where(np.isin(arr,range(3,16)))):nd.rectangle((x*sx,y*sx,(x+1)*sx-1,(y+1)*sx-1),fill='#4686b2')
    for x in range(0,x1-x0,5):nd.line((x*sx,0,x*sx,native.height),fill='#ddddda');nd.text((x*sx+2,1),str(x0+x),font=small,fill='#333333')
    for y in range(0,y1-y0,5):nd.text((1,y*sx),str(y0+y),font=small,fill='#333333')
    def local(p):return ((p[0]-x0)*sx,(p[1]-y0)*sx)
    cx0,cy0,cx1,cy1=evidence['corridor_box'];nd.rectangle((*local([cx0,cy0]),*local([cx1,cy1])),outline='#b5453c',width=2)
    for r in doc['features']:
        p=np.array(r['geometry']['coordinates'])[:,:2]
        for mod,col in [(m,'#b3599f'),(hyp,'#4a9f47')]:nd.line([local(q) for q in forward(mod,p)],fill=col,width=1)
    for row in evidence['landmarks']:
        a=local(row['diagnostic_miller_pixel']);b=local(row['unfitted_native_hypothesis_pixel']);nd.line([a,b],fill='#a15d1e',width=2)
        for x,y in [a,b]:nd.ellipse((x-3,y-3,x+3,y+3),fill='#a15d1e')
        if row['id'] not in ['P2']:nd.text((a[0]+4,a[1]+3),row['id'],font=font,fill='#333333',stroke_width=1,stroke_fill='white')
    for r in load(OUT.parent/'GEOMETRY.json')['assignments']:
        if r['owner']=='BAV':continue
        for x,y in r['cells']:
            px,py=local([x,y]);nd.rectangle((px,py,px+sx-1,py+sx-1),outline='#aa2222',width=2)
    image.paste(native,top);d=ImageDraw.Draw(image)
    lines=['Bleu : rivières natives, indices de largeur 3–15. Rose : AWGN projeté par le Miller hérité.',
           'Vert : AWGN projeté par l’hypothèse Miller théorique ; aucune des deux n’est un calage local validé.',
           'Segments bruns : désaccord entre deux hypothèses. Ce ne sont PAS des résidus ni des intervalles de confiance.',
           'Rectangle rouge : corridor de 40 × 22 cellules, zéro pixel fluvial natif, marqueurs compris.',
           'Petits carrés rouges : ancien candidat retiré ; aucune frontière ou population modifiée.',
           'P5/P6 réservés au contrôle indépendant : aucun homologue natif accepté, donc résidus non mesurables.',
           'Décision B : garder Langenbourg/Kirchberg en C. Incertitude locale non bornée avec ces données.',
           'Données modernes AWGN : repères physiques uniquement, jamais des frontières politiques de 1776.']
    for i,line in enumerate(lines):d.text((35,715+i*35),line,font=font,fill='#263d4c')
    image.save(OUT/'CORRESPONDENCES_AND_UNCERTAINTY.png');print('Physical diagnostic and uncertainty map rendered',flush=True)

def decision():
    p=load(OUT/'PHYSICAL_LANDMARKS.json');assert p['actual_fit_pairs']==p['actual_independent_check_pairs']==0
    alternatives=[
      dict(sector='Castell',physical_context='Main present regionally, but no uniquely paired local landmark accepted; county branches/condominiums need their own source geometry.',independent_calibration_ready=False,testable_territorial_sublot_prepared=False,decision='Defer: do not transfer whole WZB RGB from a city point or reuse failed calibration.'),
      dict(sector='Wertheim',physical_context='Main is drawn, so an independent Main-bend pilot is a plausible later research route. Tauber confluence not identified in the native network; continuity of branch rights also needs its own tracing.',independent_calibration_ready=False,testable_territorial_sublot_prepared=False,decision='No validated local mapping in this pass. Keep as future documented lead, not a ready country or transfer.'),
      dict(sector='Rothenburg / Windsheim / Weissenburg',physical_context='Tauber, Aisch and Rezat local watercourses not available as accepted native controls. Earlier sovereign cores are protected.',independent_calibration_ready=False,testable_territorial_sublot_prepared=False,decision='Defer. No synthetic one-cell country or automatic core exception.'),
      dict(sector='Schweinfurt',physical_context='Main could support a separate physical pilot, but a diagnostic town point and the coarse regional river shape do not establish the city territory or independent local accuracy.',independent_calibration_ready=False,testable_territorial_sublot_prepared=False,decision='No ready sublot demonstrated. Do not recast a WZB core automatically.')]
    dump('DECISION.json',dict(status='MAP2W_R3_CALIBRATION_CASE_B',territorial_delivery_status='MAP2W_R3_BLOCKED',install=False,category='C_GEOGRAPHIC_MATCHING_NOT_VALIDATED',new_functional_modifications=[],new_RGBs=[],new_countries=[],actual_fit_pairs=0,actual_independent_check_pairs=0,local_error_mean_px=None,local_error_max_px=None,local_error_bound_px=None,no_fit_or_translation_performed=True,no_old_profile_changed=True,alternatives=alternatives,recommendation='Defer R3 and move next to MAP2W-R4 (Bavarian and ecclesiastical jurisdictions), only after the user supplies or authorizes that mission. No automatic territorial work outside this calibration task.',no_runtime_validation_requested=True))
    print('Case B; no territory installed; recommend deferring R3 for MAP2W-R4',flush=True)

def verify():
    b=load(OUT/'BASELINE.json');current=prior.q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    external={'common/decisions/1776_usa_french_support.txt','common/on_actions/1776_usa_revolution_r2.txt','common/scripted_effects/1776_usa_french_support.txt','common/scripted_triggers/1776_usa_french_support.txt','events/1776_american_diplomacy.txt','localization/english/1776_american_diplomacy_r3_l_english.yml','localization/french/1776_american_diplomacy_r3_l_french.yml','common/laws/00_army_model.txt','common/laws/1776_usa_minutemen.txt'}
    unexpected=sorted(set(changed)-external);observations=[]
    for p in sorted(set(changed)&external):
        if (ROOT/p).exists():
            raw=(ROOT/p).read_text(encoding='utf-8-sig')
            assert not any(s in raw for s in ['aor1776_map2w_r3','c:HLN','c:HKI','xEDB903','xEDB902']),p
            if p.endswith('.txt'):prior.core.cw.parse(raw)
            if p=='common/laws/00_army_model.txt':
                old=subprocess.check_output(['git','show',b['git_head']+':'+p],cwd=ROOT).decode('utf-8-sig').replace('\r\n','\n')
                variants=[(prefix+text).encode('utf8') for prefix in ['', '\ufeff'] for text in [old,old.replace('\n','\r\n')]]
                assert b['hashes'][p] in [hashlib.sha256(v).hexdigest() for v in variants],'Cannot anchor old law source'
                oldnodes={n.key:n for n in prior.core.cw.parse(old)};newnodes={n.key:n for n in prior.core.cw.parse(raw)};sig=prior.core.qa.signature
                assert set(newnodes)-set(oldnodes)=={'law_aor1776_minutemen'} and set(oldnodes)<=set(newnodes)
                assert all(sig(n)==sig(newnodes[k]) for k,n in oldnodes.items() if k!='law_national_militia')
                n=oldnodes['law_national_militia'];z=newnodes['law_national_militia'];assert not n.children('is_visible')
                assert [sig(c) for c in n.children()]==[sig(c) for c in z.children() if c.key!='is_visible']
                condition=z.children('is_visible')[0].children('NOT')[0].children()[0];assert condition.key=='c:USA' and condition.value=='this'
                condition=newnodes['law_aor1776_minutemen'].children('is_visible')[0].children()[0];assert condition.key=='c:USA' and condition.value=='this'
        observations.append(dict(path=p,sha256_at_capture=b['hashes'].get(p),sha256_observed_now=current.get(p),scope='User-assigned concurrent USA/FRA support chantier; observed, never written or restored by this calibration tool'))
    dump('CONCURRENT_OBSERVATION.json',dict(status='EXTERNAL_ASSIGNED_EVOLUTION_OBSERVED',files=observations,not_a_functional_test_of_USA=True,read_only_map_calibration=True,baseline_not_rewritten=True,unexpected_paths=unexpected))
    old_r3=load(OUT.parent/'BASELINE.json')
    checks=[dict(name='Every non-concurrent runtime path and SHA256 preserved',passed=not unexpected,detail=unexpected),dict(name='Only explicit user-assigned concurrent paths observed, no MAP overlap',passed=set(changed)<=external,detail=changed),dict(name='HEAD preserved',passed=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head']),dict(name='Index preserved',passed=sha(ROOT/'.git/index')==b['git_index_sha256']),dict(name='Native rivers preserved',passed=sha(ROOT/'map_data/rivers.png')==b['rivers_mod'] and sha(GAME/'map_data/rivers.png')==b['rivers_vanilla']),dict(name='Province bitmap preserved',passed=sha(ROOT/'map_data/provinces.png')==b['provinces']),dict(name='Reviewed imperial registry preserved',passed=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json')==old_r3['registry']),dict(name='Existing registry tool preserved',passed=(ROOT/'tools/map2l_registry.py').read_text(encoding='utf8')==old_r3['registry_tool']),dict(name='No active R3 migration',passed=not (OUT.parent/'REGISTRY_MIGRATION.json').exists()),dict(name='No accepted calibration invented',passed=load(OUT/'PHYSICAL_LANDMARKS.json')['accepted_profile'] is None),dict(name='No functional correction installed',passed=load(OUT/'DECISION.json')['new_functional_modifications']==[])]
    dump('VALIDATION.json',dict(status='PASS_READ_ONLY_DIAGNOSTIC_PROTECTION' if all(r['passed'] for r in checks) else 'PROTECTION_REVIEW_REQUIRED',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,engine_execution=False,geographic_accuracy_validated=False,territorial_delivery_status='MAP2W_R3_BLOCKED',static_territorial_validation='NOT_APPLICABLE_NO_FUNCTIONAL_CHANGE',runtime_paths_compared_union=len(set(current)|set(b['hashes'])),current_runtime_file_count=len(current),runtime_paths_changed_externally=len(observations),no_external_changes_overwritten=True))
    print('Protection',sum(r['passed'] for r in checks),'/',len(checks),changed,flush=True);assert all(r['passed'] for r in checks)

def documentation():
    p=load(OUT/'PHYSICAL_LANDMARKS.json');o=load(OUT/'REFERENCE_ORIGINS.json');decision_data=load(OUT/'DECISION.json');files={};external_count=len(load(OUT/'CONCURRENT_OBSERVATION.json')['files'])
    physical_table='| ID | Repère physique candidat | Longitude / latitude WGS84 | Rôle prévu | Pixel natif homologue | Résidu indépendant | Utilisé |\n| --- | --- | --- | --- | --- | --- | --- |\n'
    for r in p['landmarks']:
        physical_table+=f"| {r['id']} | {r['name']} | {r['geo'][0]:.6f} / {r['geo'][1]:.6f} | {'Contrôle réservé' if r['role']=='CHECK_RESERVED' else 'Ajustement candidat'} | Non identifié | Non mesurable | Non |\n"
    files[(OUT/'PHYSICAL_LANDMARKS.md').relative_to(ROOT).as_posix()]='# Repères examinés — aucun point utilisé dans un calage\n\n'+physical_table+'\nP1/P2 sont les extrémités aval des polylignes AWGN. P3–P6 sont des points de courbure sélectionnés dans des fenêtres géographiques prédéfinies, sans utiliser les prédictions du jeu : angle maximal entre deux positions distantes de 350 m de part et d’autre le long du cours d’eau (approximation métrique locale pour cette sélection seulement). Ce ne sont pas des centres urbains ni des points géodésiques certifiés.\n\nAucun de ces candidats n’est accepté comme homologie. Les champs de coordonnées natives et de résidus restent `null`, jamais zéro. P5/P6 n’ont servi à aucun ajustement. Données détaillées : `PHYSICAL_LANDMARKS.json`.\n'
    oldanchors='\n'.join('- '+r['name']+' : '+str(r['game'])+' ; '+str(r['native_hub_type'])+' / '+str(r['native_hub_label'])+' ; '+r['role']+'.' for r in o['old_scan']['anchors'])
    newanchors='\n'.join('- '+r['name']+' : géographie '+str(r['geo'])+' → locator '+str(r['pixel'])+'.' for r in o['miller']['anchors'])
    sectors='| Secteur | Possibilité indépendante examinée | Décision actuelle |\n| --- | --- | --- |\n'
    sectors+='| Castell | Le Main offre un contexte régional, pas un contrôle local précis déjà accepté. Partages des branches et possessions communes à tracer séparément. | Aucun sous-lot territorial prêt ; ne pas reprendre le RGB WZB entier. |\n'
    sectors+='| Wertheim | Une étude autonome des boucles du Main est une piste réelle. Le confluent de la Tauber n’est pas identifié dans le réseau natif et les droits des branches restent à délimiter. | Piste future, pas un calage indépendant validé dans cette passe. |\n'
    sectors+='| Rothenburg, Windsheim, Weißenburg | Tauber, Aisch et Rezat non disponibles comme homologues natifs acceptés ici. | Différer ; pas de pays artificiel d’une cellule. |\n'
    sectors+='| Schweinfurt | Le Main peut soutenir un futur pilote, mais ni la position de la ville ni son territoire ne se déduisent de la courbe régionale seule. | Aucun transfert automatique du noyau WZB protégé. |\n'
    files[(OUT/'ALTERNATIVES.md').relative_to(ROOT).as_posix()]='# Alternatives à Hohenlohe\n\n'+sectors+'\n**Recommandation : différer R3 et passer ensuite à MAP-2W-R4, juridictions bavaroises et ecclésiastiques**, après consigne du joueur. Ne pas commencer cette autre région automatiquement. L’absence de sous-lot prêt aujourd’hui ne signifie pas que des sources indépendantes n’existent pas ; elle signifie qu’aucune correspondance locale contrôlée n’a été démontrée dans cette passe.\n'
    report=f'''# MAP-2W-R3-CALIBRATION — décision finale

Date : 18 octobre 2026. **Cas B : correspondance locale insuffisante.**

Statut territorial maintenu : **MAP2W_R3_BLOCKED**. Aucun pays, RGB, propriétaire, population, bâtiment, unité ou mécanisme impérial ajouté ou modifié par cette passe. Aucun test moteur effectué ; aucune nouvelle validation en jeu demandée.

## 1. Origines précises des référentiels

### Affine historique franconienne

Ancien document : `MAP2L/FRANCONIA/ALIGNMENT.json`. Le scan Homann de 2263 × 2600 pixels est envoyé vers le bitmap par une affine à six paramètres, calculée avec exactement trois couples de points. Formule : `[sx, sy, 1] @ T = [X, Y]`.

```text
T = {json.dumps(o['old_scan']['matrix'])}
```

Les positions natives proviennent de `FRANCONIA/NATIVE_ANCHORS.json`, lui-même extrait de `MAP1/MAP1_HUB_LOCATOR_CHECKS.csv` :

{oldanchors}

La formule reproduit numériquement les trois FIT, ce qui est attendu pour trois points non colinéaires et six paramètres. Cela ne mesure pas leur justesse géographique. Le mot « surveyed » de l’ancien commentaire signifie une lecture de positions dans les fichiers, pas un relevé géodésique des villes. En particulier, Würzburg est un **hub de bûcherons**, Bayreuth un **hub minier** et le contrôle Ratisbonne un **hub de ferme**. Le contrôle Ratisbonne de 5,121 pixels mêle déformation du scan, affine et placement du hub ; il ne certifie pas le secteur Jagst–Kocher.

### Miller affine hérité

Ancien profil : `MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json`. Base sphérique diagnostique : `u = radians(lon)`, `v = 1,25 × log(tan(π/4 + 0,4 × radians(lat)))`, puis `[X,Y] = [u,v] @ A + b`. Il ne s’agit pas d’une formule de projection moteur prouvée.

```text
[A;b] = {json.dumps(o['miller']['matrix'])}
```

Cinq points FIT, tous des locators non relevés géodésiquement :

{newanchors}

Domaine des points FIT : longitude 8,68417–13,73832°, latitude **50,11552–52,37052° N**. Langenbourg et Kirchberg, vers 49,2° N, sont environ 0,86–0,91° au sud : c’est une extrapolation. RMS FIT 1,716 pixel et RMS CHECK européen 12,082 pixels ne constituent pas une marge locale garantie. Les biais de locators et l’extrapolation peuvent se combiner ; on ne peut attribuer le désaccord à une simple translation ou à la seule formule Miller.

### Calage intermédiaire du candidat retiré

`R3/SOURCE_ALIGNMENT.json` envoie le dessin de Gerabronn vers **trois positions prédites par le Miller hérité**, et non vers trois nouveaux points physiques natifs. Les contrôles de feuille Gerabronn/Schrozberg, 0,079 et 0,222 pixel, partagent ce même référentiel parent. Ils vérifient une cohérence relative, pas la position réelle dans le jeu. Le SVG ne déclare pas de CRS : ses unités nominales ne sont pas assimilées arbitrairement à UTM ou Gauss–Krüger.

Les anciens écarts Würzburg 7,57 / Nuremberg 2,29 / Bayreuth 1,99 / Ratisbonne 4,97 pixels sont des désaccords entre référentiels, pas des erreurs certifiées des villes. Aucun des deux n’est promu comme vérité par défaut. Aucun profil ancien ou frontière validée n’a été réécrit.

Les rasters provinciaux et fluviaux partagent le même repère image 8192 × 3616, origine en haut à gauche, Y vers le bas. Le facteur deux de la hauteur 16384 × 7232 est un facteur de résolution, pas une correction géographique. `default.map` et les defines natifs indiquent le bouclage horizontal et une position graphique d’équateur 0,58 ; ils ne fournissent pas une formule géodésique exacte. Aucun retournement, facteur deux ou translation n’a été introduit pour faire coïncider les hypothèses.

## 2. Nouvelles données physiques indépendantes

Source primaire : [LUBW, réseau hydrographique officiel AWGN](https://www.lubw.baden-wuerttemberg.de/wasser/awgn). Service `Gewaessernetz_AWGN`, couche 0 : système natif EPSG:25832, export demandé en EPSG:4326. Réponse complète : Neckar OBJECTID 18518 (**8 341 sommets**), Jagst 4294 (**9 722**), Kocher 4311 (**7 402**), soit **25 465 sommets**. Métadonnées et réponse GeoJSON conservées avec empreintes.

Le réseau moderne sert à rechercher des formes physiques, pas à définir les frontières de 1776. Rectifications de cours d’eau et écart de date restent des limites. Le réseau Natural Earth 1:10 millions déjà conservé ne contient pas ici la Jagst, le Kocher ou le Neckar ; son seul ajout ou sa meilleure interpolation ne pouvait pas créer ces informations.

Six candidats physiques sont examinés. P1/P2 correspondent aux embouchures ; P3–P6 à des secteurs de boucle, choisis par la géométrie hydrographique seule dans des fenêtres déclarées. Les points réservés ne sont jamais utilisés pour ajuster un modèle.

{physical_table}

## 3. Vérification des données natives et du relief

Le raster fluvial est lu dans le mod actif, palette P, 8192 × 3616. L’extraction comprend **toutes les largeurs 3–15**, conformément aux treize valeurs natives, plus les marqueurs 0–2 ; ce n’est pas un filtre limité aux seuls bleus 3–11. Les fonds 254/255 sont distingués des cours d’eau.

Dans le corridor `[4300,870]–[4340,892]`, couvrant 40 × 22 cellules autour des positions diagnostiques : **zéro pixel de rivière ou de marqueur**, aucun indice inconnu masquant une rivière. Le raster modifié pour les lots antérieurs et le vanilla sont **identiques dans la fenêtre régionale examinée**. Le Rhin, le Main et le Danube sont visibles dans le contexte large, mais pas les branches Jagst–Kocher–Neckar nécessaires aux petites cibles. Les deux confluences P1/P2 ne sont en outre séparées que de 0,507 pixel dans le modèle diagnostique : elles ne fourniraient pas deux ancrages bien séparés à cette résolution.

Le relief est aussi inspecté : source 16384 × 7232, contrôle de **110 échantillons** de la hauteur compactée réellement référencée par l’indirection native. Écart source/packed nul sur ces échantillons. L’image locale montre un modelé lissé, sans sommet ou vallée homologue identifié indépendamment. Les extrema de gris ne deviennent pas des contrôles géographiques, et les valeurs ne sont pas converties en mètres sans preuve.

## 4. Contrôles indépendants et incertitude

**Quatre candidats d’ajustement, deux candidats de contrôle réservés ; zéro couple physique accepté pour le calcul, zéro contrôle natif indépendant mesurable.** Aucun nouveau modèle n’est ajusté. Moyenne des résidus, maximum, borne d’erreur et intervalle de confiance locaux restent `null` / **non établis**, pas zéro.

Les distances aux rivières natives les plus proches sont conservées comme diagnostics de non-correspondance, jamais comme résidus de repères homologues. Les segments entre deux prédictions sur la figure ne représentent ni des barres d’erreur ni une confiance à 95 %. La discrétisation d’une cellule identifiée peut à elle seule représenter jusqu’à ±0,5 pixel par axe ; elle ne borne pas les erreurs de modèle, d’identification ou de source.

L’incertitude totale n’est donc **pas bornable utilement avec les observations disponibles**. On ne peut garantir le choix des noyaux proposés de deux à trois cellules de large. La documentation n’affirme pas que la géographie de ces villes soit impossible à connaître : elle constate l’absence de contrôle physique natif suffisamment discriminant dans ces données.

Carte : `CORRESPONDENCES_AND_UNCERTAINTY.png`. Le panneau gauche est une vue géographique indépendante ; le droit montre les rivières natives et deux hypothèses non validées. Les anciens candidats retirés restent marqués comme tels, sans être installés.

## 5. Décision et alternatives

**Ne rien installer ; Langenbourg/Kirchberg restent en catégorie C pour leur correspondance avec le bitmap.** Leur souveraineté historique n’est pas remise en cause. Leurs sept anciennes cellules ne sont pas réattribuées ; aucun nouveau TAG/RGB, aucun besoin de contrôle en nouvelle partie.

{sectors}

**Recommandation explicite : différer R3 et passer à MAP-2W-R4, juridictions bavaroises et ecclésiastiques**, après consigne du joueur. Les boucles du Main restent une piste de recherche indépendante pour une reprise ultérieure, pas un sous-lot déjà testable. Aucune autre région ne démarre automatiquement.

## 6. Protection, reproductibilité et limites

La capture fraîche `BASELINE.json` conserve les empreintes de **2 328 fichiers fonctionnels** et de Git. Le contrôle final distingue les fichiers inchangés des **{external_count} chemins précis du chantier américain concurrent**, dont l’évolution a été observée sans écriture ou restauration par cette passe. Une modification de visibilité de loi est notamment limitée aux États-Unis, et l’ancien fichier séparé des minutemen a été retiré par ce chantier externe ; les autres lois natives sont comparées à leur source antérieure et conservées. Ces observations ne constituent pas une validation fonctionnelle du chantier américain. La liste et les empreintes observées sont dans `CONCURRENT_OBSERVATION.json` ; la baseline n’est pas réécrite.

Carte provinciale, propriétaires, populations, bâtiments, unités, registre impérial de 567 RGB, compilateur existant, anciens profils, Erfurt–Eichsfeld et lots validés sont préservés. HEAD et index inchangés. Aucun commit, push, merge, reset, rebase, changement de branche ou staging. Installation du jeu en lecture seule.

Le contrôle territorial moteur est **sans objet**, puisqu’aucun correctif fonctionnel n’est installé. **22/22 tests du diagnostic** et **11/11 contrôles de protection** passent. Les tests vérifient notamment le maintien de valeurs nulles en absence de contrôles, les rôles réservés, le refus d’un calage sans couples et les protections de périmètre. Ils ne certifient pas une précision géographique.

Outil indépendant : `tools/map2w_r3_calibration.py` ; commandes de lecture/diagnostic `inspect`, `origins`, `physics`, `map_evidence`, `decision`, `verify`. `snapshot` refuse d’écraser sa capture. Les réponses téléchargées sont conservées ; aucune intégration ou dépendance supplémentaire installée. Les chemins étaient connus ou retrouvables par identifiant/nom exact : aucun appel ColGrep redondant et aucune reconstruction d’index dans cette passe.
'''
    files[(OUT/'REPORT.md').relative_to(ROOT).as_posix()]=report
    dump('INDEPENDENT_CHECKS.json',dict(planned_candidates=['P5','P6'],excluded_from_fit=True,accepted_native_pairs=0,mean_residual_px=None,max_residual_px=None,confidence_interval_px=None,passed_geographic_accuracy=False,result='UNMEASURABLE_NO_NATIVE_HOMOLOGUE_NOT_ZERO_ERROR'))
    url='https://rips-gdi.lubw.baden-wuerttemberg.de/arcgis/rest/services/wfs/Gewaessernetz_AWGN/MapServer/0/query?where=GEW_NAME%20IN%20(%27Jagst%27,%27Kocher%27,%27Neckar%27)&outFields=OBJECTID,GEW_NAME,GEW_KENNZAHL,VOR_GEW_NAME&returnGeometry=true&outSR=4326&f=geojson'
    dump('SOURCES.json',dict(recorded_on='2026-10-18',institution='LUBW Landesanstalt fuer Umwelt Baden-Wuerttemberg',primary_information='https://www.lubw.baden-wuerttemberg.de/wasser/awgn',service='https://rips-gdi.lubw.baden-wuerttemberg.de/arcgis/rest/services/wfs/Gewaessernetz_AWGN/MapServer',layer=0,query=url,files={name:sha(OUT/name) for name in ['AWGN_SERVICE.json','AWGN_LAYER.json','AWGN_JAGST_KOCHER_NECKAR.geojson']},source_epoch='Modern maintained hydrography, not a 1776 political map',licence='No licence inferred from an empty copyrightText. Source and metadata retained; no distribution as a game asset.'))
    core=prior.core;core.OUT=OUT;patches=[]
    for i,(rel,raw) in enumerate(files.items()):
        name=f'DOCUMENT_{i}.patch';core.emit({rel:raw},name);patches.append(name)
    dump('DOCUMENT_PATCHES.json',patches);print('Report, physical landmark table and alternative decision prepared',flush=True)

def tests():
    import io,time,unittest
    stream=io.StringIO();started=time.monotonic();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestLoader().loadTestsFromName('test_map2w_r3_calibration'))
    dump('TESTS.json',dict(kind='DIAGNOSTIC_CONTRACTS_NOT_ENGINE_OR_GEODETIC_CERTIFICATION',tests=r.testsRun,failures=[t.id() for t,_ in r.failures],errors=[t.id() for t,_ in r.errors],seconds=round(time.monotonic()-started,2),output=stream.getvalue()))
    print(r.testsRun,'tests;',len(r.failures),'failures;',len(r.errors),'errors',flush=True);assert r.wasSuccessful(),stream.getvalue()

def finalize():
    verify();tests();v=load(OUT/'VALIDATION.json');t=load(OUT/'TESTS.json');assert v['passed']==v['total'] and not(t['failures'] or t['errors'])
    v.update(diagnostic_tests={'tests':t['tests'],'failures':t['failures'],'errors':t['errors']},final_visual_review='CORRESPONDENCES_AND_UNCERTAINTY_AND_RELIEF_REVIEWED',calibration_profile_approved=False,case='B',next_recommended_mission='MAP2W-R4_AFTER_USER_DIRECTION')
    dump('VALIDATION.json',v)
    sources=['docs/reports/map/MAP2W/R3/NATIVE_REFERENCE_CONTRADICTION.json','docs/reports/map/MAP2W/R3/SOURCE_ALIGNMENT.json','docs/reports/map/MAP2W/R3/HISTORICAL_EVIDENCE.md','docs/reports/map/MAP2L/FRANCONIA/ALIGNMENT.json','docs/reports/map/MAP2L/FRANCONIA/TRACING.json','docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json','tools/georeference/model.py']
    products=['REPORT.md','PHYSICAL_LANDMARKS.md','ALTERNATIVES.md','DECISION.json','PHYSICAL_LANDMARKS.json','REFERENCE_ORIGINS.json','INDEPENDENT_CHECKS.json','CORRESPONDENCES_AND_UNCERTAINTY.png','NATIVE_RIVERS_RAW.png','LOCAL_RELIEF_DIAGNOSTIC.png','VALIDATION.json','TESTS.json','SOURCES.json','CONCURRENT_OBSERVATION.json']
    dump('DELIVERY_MANIFEST.json',dict(status='CASE_B_NO_TERRITORIAL_INSTALL',recorded_on='2026-10-18',products={p:sha(OUT/p) for p in products},source_hashes_observed={p:sha(ROOT/p) for p in sources},source_epoch_note='Observed source hashes, not a new geodetic certification',runtime_functional_files_written=[],git_operations_written=[],approved_calibration_profile=None))
    print('Delivery complete: Case B; 0 functional writes; 22 diagnostic tests and 11 protections PASS',flush=True)
if __name__=='__main__':globals()[sys.argv[1]]()
