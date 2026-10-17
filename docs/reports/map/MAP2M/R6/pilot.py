"""Read-only runtime investigation of two MAP-2M-R6 pilots.

All generated artifacts are confined to this folder. R1-R5 are imported only
for pure readers/math; their generation commands are never invoked.
"""
import sys,json,csv,hashlib,math,collections
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parent
R5=OUT.parent/'R5'
sys.path.insert(0,str(R5))
import work as w
import review as r
ROOT=w.ROOT
# Verified source scans have 124,653,588 pixels; retain a bounded safety limit.
Image.MAX_IMAGE_PIXELS=150_000_000

def dump(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))

def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields or list(rows[0]));writer.writeheader();writer.writerows(rows)

def physical_masks():
    bmp,water,oldmask,path=w.physical_masks()
    river=Image.open(path);indices=np.asarray(river)
    # Installed NRivers.NUM_WIDTH_PIXEL_VALUES=13, palette widths 3..15.
    # Green width 15 is NOT the source marker at index 0.
    mask=(indices>=3)&(indices<=15)
    return bmp,water,mask,path

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Never overwrite a reference.'
    reference=w.load('BASELINE.json');current=w.prior.economy.runtime_hashes()
    assert current==reference['runtime_hashes'],'Runtime differs from R5: inspect without restoring.'
    prior={p.relative_to(ROOT).as_posix():w.sha(p) for name in ['R1','R2','R3','R4','R5'] for p in (OUT.parent/name).rglob('*') if p.is_file()}
    dump('BASELINE.json',dict(runtime_hashes=current,prior_files=prior,inventory_sha256=hashlib.sha256(json.dumps(reference['inventory'],sort_keys=True).encode()).hexdigest(),
        git_head=w.prior.r3.r2.head(),git_index_sha256=w.sha(ROOT/'.git/index'),bitmap_sha256=w.sha(ROOT/'map_data/provinces.png')))
    print(len(current),'functional files and',len(prior),'prior evidence files protected.')

def crop(source,box,name,step=200):
    im=Image.open(ROOT/source).convert('RGB');sub=im.crop(box);d=ImageDraw.Draw(sub)
    for x in range((box[0]//step+1)*step,box[2],step):
        d.line((x-box[0],0,x-box[0],sub.height),fill='#d04040',width=1);d.text((x-box[0]+2,2),str(x),fill='red',font=w.font(19))
    for y in range((box[1]//step+1)*step,box[3],step):
        d.line((0,y-box[1],sub.width,y-box[1]),fill='#d04040',width=1);d.text((2,y-box[1]+2),str(y),fill='red',font=w.font(19))
    sub.save(OUT/name)

def readings():
    sources=[('MAYER_BSB_LOCAL.png','docs/reports/map/MAP2M/EVIDENCE/MAYER_BSB_AFTER_1763.jpg',(2400,1700,3700,2700)),
      ('BOUNDARY_BROMBERG_LOCAL.png','docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL2_FULL.jpg',(6500,4300,8900,6700)),
      ('BOUNDARY_NOTE_LOCAL.png','docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL1_FULL.jpg',(0,0,2500,2500))]
    for name,path,box in sources:crop(path,box,name)
    bmp,water,river,_=physical_masks()
    for name,box,scale in [('A',(4393,724,4418,747),32),('B',(4497,753,4525,777),32)]:
        x0,y0,x1,y1=box;arr=np.where(water[y0:y1,x0:x1,None],[201,228,247],[236,230,207]).astype(np.uint8);arr[river[y0:y1,x0:x1]]=[20,80,220]
        im=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
        for x in range(x0,x1):
            d.line(((x-x0)*scale,0,(x-x0)*scale,im.height),fill='#999999');d.text(((x-x0)*scale+1,2),str(x),fill='black',font=w.font(12))
        for y in range(y0,y1):
            d.line((0,(y-y0)*scale,im.width,(y-y0)*scale),fill='#999999');d.text((1,(y-y0)*scale+1),str(y),fill='black',font=w.font(12))
        im.save(OUT/('NATIVE_'+name+'_READING.png'))
    dump('SOURCE_CROP_FRAMES.json',[dict(file=name,source=path,bbox=box,source_sha256=w.sha(ROOT/path),meaning='Untransformed reading crop; red grid is source pixel coordinates, not longitude/latitude.') for name,path,box in sources])

def palette():
    bmp,water,new,path=physical_masks();river=Image.open(path);a=np.asarray(river);pal=river.getpalette();rows=[]
    for sector,box in [('A',(4393,724,4418,747)),('B',(4497,753,4525,777))]:
        x0,y0,x1,y1=box;loc=a[y0:y1,x0:x1]
        for i,n in zip(*np.unique(loc,return_counts=True)):
            rows.append(dict(Pilot=sector,Index=int(i),RGB=str(pal[3*int(i):3*int(i)+3]),Count=int(n),
                R5_included=3<=i<=11,R6_included=3<=i<=15,Role='WIDTH' if 3<=i<=15 else 'BACKGROUND_OR_SPECIAL'))
    csvout('RIVER_PALETTE_AUDIT.csv',rows)
    dump('RIVER_EXTRACTION_FIX.json',dict(definition_path=str(w.GAME/'common/defines/jomini/rivers.txt'),definition_sha256=w.sha(w.GAME/'common/defines/jomini/rivers.txt'),
        num_width_values=13,width_indices=list(range(3,16)),river_path=str(path),river_sha256=w.sha(path),
        old_filter=[3,11],new_filter=[3,15],R5_files_unchanged=True,note='Corrected diagnostic extraction, not a runtime river edit. Missing blue is not equivalent to missing physical river.'))

def extra_crops():
    for path,box,name in [
      ('docs/reports/map/MAP2M/EVIDENCE/MAYER_BSB_AFTER_1763.jpg',(2600,2030,3040,2470),'WOLGAST_SYMBOLS.png'),
      ('docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL1_FULL.jpg',(400,2600,3300,3700),'BOUNDARY_TITLE_NOTE.png'),
      ('docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL2_FULL.jpg',(7000,4500,8700,5600),'BROMBERG_FORDON_SYMBOLS.png'),
      ('docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg',(500,200,1650,1400),'GUESSEFELD_NETZE_LOCAL.png')]:crop(path,box,name,200)

def protocol():
    assert not (OUT/'FROZEN_PROTOCOL.json').exists(),'Keep preregistered choices.'
    dump('FROZEN_PROTOCOL.json',dict(
        timing='Declared after exploratory source and native reading crops, before any new holdout residual calculation. No R6 transform is fitted or selected.',
        native_model_file='../R5/TRANSFORMATIONS.json',native_model_sha256=w.sha(R5/'TRANSFORMATIONS.json'),native_model='selected_native, geographic_axes, frozen',
        fit_ids=[],selection_after_final_checks=False,
        final_checks=[
          dict(id='A_WOLGAST_NARROWS',role='FINAL_HOLDOUT',object='Opposed mainland/Usedom shores at Wolgast narrows',
               rule='Require distinguishable opposed shores in corrected native water/river masks; otherwise UNMEASURABLE, no fabricated residual.',native_search_box=[4404,731,4416,740],physical_source='LUNG Peenestrom water polygons kg.52; Mayer Wolgast reading'),
          dict(id='B_VISTULA_WEST_APEX',role='FINAL_HOLDOUT',object='Westernmost Vistula elbow south of Fordon, not the urban centre of Fordon',
               real_rule='Minimum longitude among retained Natural Earth Vistula vertices inside fixed geo box. No nearest-point matching.',real_box=[18.04,53.08,18.26,53.22],
               native_rule='Minimum X of width pixels 3..15 in fixed native box; midpoint of tied westmost pixel centres.',native_search_box=[4507,760,4518,770],native_reading_radius_px=1.5,
               limitation='One generalized river bend, not a junction or certified historical bank; keep all tied cells and modern river source limitations.')],
        variant_policy='Compare frozen R5 geographic_axes with all four already retained native models; do not choose a new model using these final checks.',
        political_policy='A requires dated political line and independently checked source-to-real + real-to-native chain, stable assignment under plausible variants. Same colour is insufficient.',
        territories='Pilot A inherited18 only; pilot B inherited Netze candidates inside [4501,758,4520,775] and locally adjacent to validated core. No automatic import of R5 extra149.',
        excluded='Thorn/Torun; other districts, general historical recalibration; no artificial Peendamm enclave.'))

def holdouts():
    protocol=load('FROZEN_PROTOCOL.json');assert w.sha(R5/'TRANSFORMATIONS.json')==protocol['native_model_sha256']
    bmp,water,mask,_=physical_masks();models=w.load('TRANSFORMATIONS.json');model=models['selected_native'];rows=[];controls=[];detail=[]
    for p in w.load('REVISED_CONTROL_OBSERVATIONS.json')['points']:
        if p['Role']=='FIT':controls.append(dict(ID=p['ID'],Role='INHERITED_FROZEN_FIT_NOT_R6_FIT',Source='R5_REVISED_CONTROL_OBSERVATIONS',Longitude=p['Longitude'],Latitude=p['Latitude'],Native_X=p['X'],Native_Y=p['Y'],Native_reading_radius_px=p['Reading_radius_px'] if 'Reading_radius_px' in p else '',Used_for_fit='R5_ONLY',Provenance='Frozen inherited model; no new adjustment or selection in R6.'))
    for spec in protocol['final_checks']:
        x0,y0,x1,y1=spec['native_search_box']
        if spec['id']=='A_WOLGAST_NARROWS':
            rows.append(dict(ID=spec['id'],Role='FINAL_HOLDOUT',Longitude='',Latitude='',Native_X='',Native_Y='',Pred_X='',Pred_Y='',Residual_px='',Outside_R5_support='',
                Status='UNMEASURABLE_NO_NATIVE_CHANNEL',Used_for_fit=False,Used_for_selection=False,
                Reason=f'Native box has {int(water[y0:y1,x0:x1].sum())} water cells and {int(mask[y0:y1,x0:x1].sum())} width cells; no opposed shores/narrows identifiable. Do not measure distance to unrelated sea coast.'))
            detail.append(dict(id=spec['id'],native_box=spec['native_search_box'],water_cells=int(water[y0:y1,x0:x1].sum()),river_width_cells=int(mask[y0:y1,x0:x1].sum())))
            controls.append(dict(ID=spec['id'],Role='FINAL_HOLDOUT_UNMEASURABLE',Source='LUNG_kg52_NATIVE_REVIEW',Longitude='',Latitude='',Native_X='',Native_Y='',Native_reading_radius_px='',Used_for_fit=False,Provenance='Opposed channel shores not identified natively; no point fabricated.'))
            continue
        fs=json.loads((ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/ne_10m_rivers.geojson').read_text())['features'];pts=[]
        lon0,lat0,lon1,lat1=spec['real_box']
        for f in fs:
            if f['properties'].get('name')!='Vistula':continue
            for part in [f['geometry']['coordinates']] if f['geometry']['type']=='LineString' else f['geometry']['coordinates']:
                for p in part:
                    if lon0<=p[0]<=lon1 and lat0<=p[1]<=lat1:pts.append(p[:2])
        assert pts,'No vertices: never move search box to improve score.'
        geo=min(pts,key=lambda p:p[0]);ys,xs=np.where(mask[y0:y1,x0:x1]);assert len(xs)
        tied=xs==xs.min();native=np.array([xs[tied][0]+x0+.5,float(np.mean(ys[tied]))+y0+.5]);pred=r.forward(model,[geo])[0]
        rows.append(dict(ID=spec['id'],Role='FINAL_HOLDOUT',Longitude=geo[0],Latitude=geo[1],Native_X=native[0],Native_Y=native[1],Pred_X=pred[0],Pred_Y=pred[1],Residual_px=float(np.linalg.norm(pred-native)),Outside_R5_support=not r.in_support(model,geo),
            Status='MEASURABLE_SCHEMATIC_APEX_NOT_CERTIFIED',Used_for_fit=False,Used_for_selection=False,Reason=spec['limitation']))
        controls.append(dict(ID=spec['id'],Role='FINAL_HOLDOUT',Source='NE_10M_RIVERS_RETAINED_VISTULA',Longitude=geo[0],Latitude=geo[1],Native_X=native[0],Native_Y=native[1],Native_reading_radius_px=spec['native_reading_radius_px'],Used_for_fit=False,
            Provenance='Extrema rules and boxes fixed in FROZEN_PROTOCOL.json; no locator, urban label, nearest-river residual or adjustment.'))
        tied_centres=np.c_[xs[tied]+x0+.5,ys[tied]+y0+.5];needed=float(np.max(np.linalg.norm(tied_centres-native,axis=1))+.5)
        controls[-1]['Native_reading_radius_px']=max(spec['native_reading_radius_px'],needed)
        controls[-1]['Provenance']+=' Observed plateau requires radius '+str(needed)+'px, exceeding initial protocol1.5px; uncertainty is not hidden by the centroid residual.'
        detail.append(dict(id=spec['id'],geo_candidates=pts,selected_geo=geo,native_tied_centres=tied_centres.tolist(),
            preregistered_radius_px=spec['native_reading_radius_px'],observed_plateau_radius_including_half_cell_px=needed,reading_ambiguity_exceeds_preregistered_radius=needed>spec['native_reading_radius_px'],
            variants=[dict(name=name,prediction=r.forward(dict(mm,name=name),[geo])[0].tolist(),residual_px=float(np.linalg.norm(r.forward(dict(mm,name=name),[geo])[0]-native))) for name,mm in models['tested_native'].items()]))
    for row in rows:
        datum=next(v for v in detail if v['id']==row['ID'])
        row['Protocol_reading_radius_px']=datum.get('preregistered_radius_px','')
        row['Observed_plateau_radius_px']=datum.get('observed_plateau_radius_including_half_cell_px','')
        row['Ambiguity_exceeds_protocol']=datum.get('reading_ambiguity_exceeds_preregistered_radius','')
    csvout('FINAL_HOLDOUT_CHECKS.csv',rows);csvout('CONTROL_POINTS.csv',controls)
    dump('FINAL_HOLDOUT_DETAIL.json',detail)
    print(json.dumps(rows,indent=2))

def source_details():
    for path,box,name,scale in [
      ('docs/reports/map/MAP2L/PRUSSIAN_BORDERS/EVIDENCE/MAYER_1763_GREIFSWALD.jpg',(615,450,770,610),'MAYER1763_WOLGAST_DETAIL.png',6),
      ('docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg',(1160,2140,1550,2460),'GUESSEFELD_BROMBERG_DETAIL.png',3)]:
        im=Image.open(ROOT/path).convert('RGB').crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale));d=ImageDraw.Draw(im)
        for x in range((box[0]//20+1)*20,box[2],20):
            d.line(((x-box[0])*scale,0,(x-box[0])*scale,im.height),fill='#d05555');d.text(((x-box[0])*scale+1,2),str(x),fill='red',font=w.font(17))
        for y in range((box[1]//20+1)*20,box[3],20):
            d.line((0,(y-box[1])*scale,im.width,(y-box[1])*scale),fill='#d05555');d.text((2,(y-box[1])*scale+1),str(y),fill='red',font=w.font(17))
        im.save(OUT/name)

def evidence():
    # Source-image traces are observations, NOT qualified geographic polygons.
    traces=[
      dict(ID='A_MAINLAND_BANK',Pilot='A',Source='docs/reports/map/MAP2L/PRUSSIAN_BORDERS/EVIDENCE/MAYER_1763_GREIFSWALD.jpg',
           points=[[711,501],[712,510],[711,519],[710,528],[707,537],[701,543],[694,549]],reading_radius_source_px=4,
           role='INTERPRETED_WESTERN_PEENESTROM_BANK',political='Swedish mainland side versus Prussian Usedom; bank/thalweg convention not established by this reading',
           date='1763 map state retained; no independent second political source from same Mayer family',status='B_SOURCE_TO_REAL_NOT_VALIDATED'),
      dict(ID='B_VISTULA_RIM_REJECTED',Pilot='B',Source='docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL2_FULL.jpg',
           points=[[8090,4630],[8060,4780],[8008,4930],[7990,5100],[8010,5310],[8040,5500]],reading_radius_source_px=25,
           role='WESTERN_VISTULA_RIM_NOT_ACCEPTED_INTERNATIONAL_BORDER',political='Rim near Fordon must not separate Prussian Bromberg/Fordon from all of Prussian Culm as if Poland; exact administrative purpose not conclusively established',
           date='Catalogue [1772], draft/copy, later additions not individually dated',status='C_REJECT_AS_AUTOMATIC_SOVEREIGNTY_BOUNDARY'),
      dict(ID='B_SOUTHERN_1775_CANDIDATE',Pilot='B',Source='docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg',
           points=[[1190,2367],[1250,2368],[1290,2381],[1330,2408],[1370,2429],[1395,2435],[1440,2428],[1490,2423],[1530,2419]],reading_radius_source_px=8,
           role='INTERPRETED_OUTER_SOUTHERN_RIM_BELOW_BROMBERG',political='Southern acquisition rim against Polish side is a plausible political segment, distinct from Fordon river rim. Same red/yellow colours alone are not sufficient.',
           date='Retained Guessefeld/Homann 1775 state; manuscript-to-1775 equivalence unresolved',status='B_IDENTIFIED_SOURCE_SEGMENT_NO_ACCEPTED_REAL_CALIBRATION')]
    for t in traces:t['sha256']=w.sha(ROOT/t['Source'])
    dump('SOURCE_LINE_OBSERVATIONS.json',traces)
    rows=[]
    for t in traces:
        for i,(a,b) in enumerate(zip(t['points'][:-1],t['points'][1:])):
            rows.append(dict(Pilot=t['Pilot'],Segment=f"{t['ID']}_{i:02}",Source=t['Source'],Source_SHA256=t['sha256'],Source_A_X=a[0],Source_A_Y=a[1],Source_B_X=b[0],Source_B_Y=b[1],Reading_radius_source_px=t['reading_radius_source_px'],
                Line_role=t['role'],Political_evidence=t['political'],Dating=t['date'],Source_to_real='NOT_ACCEPTED',Longitude_A='',Latitude_A='',Longitude_B='',Latitude_B='',Status=t['status'],Applied=False))
    rows.append(dict(Pilot='B',Segment='B_PRIVATE_RED_TEXT',Source='docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL1_FULL.jpg',Source_SHA256=w.sha(ROOT/'docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL1_FULL.jpg'),
        Source_A_X=400,Source_A_Y=2800,Source_B_X=3300,Source_B_Y=3700,Reading_radius_source_px='',Line_role='PRIVATE_OWNERSHIP_NOTE_NOT_SOVEREIGNTY',
        Political_evidence='Red note identifies towns/villages written red as possessions of Generalin von Skorzewska; does not assign them to a sovereign.',Dating='Catalogue [1772]; note ink not independently dated',Source_to_real='NOT_APPLICABLE',Longitude_A='',Latitude_A='',Longitude_B='',Latitude_B='',Status='EXCLUDED_NOT_A_FRONTIER',Applied=False))
    csvout('HISTORICAL_BORDER_EVIDENCE.csv',rows)
    for t in traces:
        im=Image.open(ROOT/t['Source']).convert('RGB');p=np.asarray(t['points']);lo=np.floor(p.min(axis=0)-[70,60]).astype(int);hi=np.ceil(p.max(axis=0)+[100,70]).astype(int)
        lo=np.maximum(lo,0);hi=np.minimum(hi,im.size);sub=im.crop((*lo,*hi));scale=min(5,1500/max(sub.size));sub=sub.resize((int(sub.width*scale),int(sub.height*scale)))
        d=ImageDraw.Draw(sub);pts=[tuple((v-lo)*scale) for v in p];d.line(pts,fill='#b000bf' if t['Pilot']=='A' else '#e00000' if 'REJECTED' in t['ID'] else '#e08000',width=3)
        for i,point in enumerate(pts):d.ellipse((point[0]-3,point[1]-3,point[0]+3,point[1]+3),fill='white');d.text((point[0]+5,point[1]+3),str(i),fill='black',font=w.font(16))
        canvas=Image.new('RGB',(max(sub.width,800),sub.height+100),'white');canvas.paste(sub,(0,100));d=ImageDraw.Draw(canvas)
        d.text((10,10),t['ID']+' - SOURCE PIXELS ONLY',fill='black',font=w.font(20));d.text((10,45),'Lecture interpretee ; non georeferencee, non installee dans le jeu.',fill='black',font=w.font(18));canvas.save(OUT/(t['ID']+'.png'))
    # Quantify a modern cross-section, not a historical boundary or city error.
    water=json.loads((OUT.parent/'R3/EVIDENCE/LUNG_PEENESTROM_WATER.geojson').read_text())['features'];f=next(f for f in water if f['id']=='kg.52');cross=[]
    for lat in [54.04,54.05,54.06,54.07,54.08]:
        for pi,poly in enumerate(f['geometry']['coordinates']):
            xs=[]
            for ring in poly:
                for a,b in zip(ring[:-1],ring[1:]):
                    if (a[1]<=lat<b[1]) or (b[1]<=lat<a[1]):xs.append(a[0]+(lat-a[1])*(b[0]-a[0])/(b[1]-a[1]))
            xs.sort()
            for left,right in zip(xs[0::2],xs[1::2]):
                if 13.75<left<right<13.82:
                    cross.append(dict(Latitude=lat,West_lon=left,East_lon=right,Width_m=(right-left)*111319.49079327358*math.cos(math.radians(lat)),Width_R5_px=(right-left)*w.load('TRANSFORMATIONS.json')['selected_native']['matrix'][0][0],
                        Source='LUNG kg.52 current water; horizontal section, not perpendicular channel width; not a1776 shoreline',Polygon=pi))
    csvout('MODERN_CHANNEL_SECTIONS.csv',cross,fields=['Latitude','West_lon','East_lon','Width_m','Width_R5_px','Source','Polygon'])
    m=w.load('TRANSFORMATIONS.json')['selected_native']['matrix'];lat=54.05
    kmx=111.31949079327358*math.cos(math.radians(lat))/m[0][0];kmy=111.31949079327358/abs(m[1][1])
    _,wm,rm,_=physical_masks();x0,y0,x1,y1=(4404,734,4414,739)
    chain=w.load('ANKLAM_CHAIN.json');points=np.array([v['native_estimate'] for v in chain['points']]);cells=np.floor(points).astype(int).tolist()
    dump('RESOLUTION_LIMITS.json',dict(local_latitude=lat,km_per_pixel_X=kmx,km_per_pixel_Y=kmy,cell_area_km2_approx=kmx*kmy,
        Wolgast_inner_box=[x0,y0,x1,y1],water_cells=int(wm[y0:y1,x0:x1].sum()),river_width_cells=int(rm[y0:y1,x0:x1].sum()),
        Anklam_urban_point_span_px=chain['point_extent_px'],Anklam_projected_point_cells=cells,Peendamm_polygon_area=None,
        warning='Absence of physical channel prevents a local bank-to-bank holdout, NOT drawing a political RGB border in principle. No historical Peendamm polygon/area is established; urban point span is not territorial extent.',
        modern_sections_are_not_historical=True,Peendamm_distinct_robust_representation='NOT_DEMONSTRATED_AT_CURRENT_RESOLUTION',approximations_applied=False))

def decisions():
    bmp,_,_,_=physical_masks();old=r.read_csv(R5/'CANDIDATE_CELLS.csv');ys,xs=np.where(bmp==0xEDB010);core=np.c_[xs,ys];rows=[]
    for v in old:
        x,y=int(v['X']),int(v['Y'])
        if v['Sector']=='PEENE' and v['Origin']=='R4_INHERITED':
            cls='B';pilot='A';distance='';reason='Swedish mainland assignment probable, but no newly accepted source-to-real line and no observable opposed native shores. R5 source/native membership variants are diagnostic only.'
        elif v['Sector']=='NETZE' and 4501<=x<4520 and 758<=y<775:
            dist=int(np.min(np.abs(core-[x,y]).sum(axis=1)))
            if dist!=1:continue
            cls='C';pilot='B';distance=dist;reason='Directly adjacent to validated Bromberg core. Native bend holdout works at one point; source political segment is not converted by a qualified local source-to-real transformation. Do not use Fordon river rim as automatic international border.'
        else:continue
        cellgeo=r.inverse(w.load('TRANSFORMATIONS.json')['selected_native'],[[x+.5,y+.5]])[0]
        rows.append(dict(Pilot=pilot,X=x,Y=y,State_ID=v['State_ID'],Current_RGB=v['Current_RGB'],Current_owner=v['Current_owner'],Owner_hypothesis=v['Historical_owner_hypothesis'],Class=cls,
            Sovereignty_1776='PROBABLE_MAINLAND_SWE' if pilot=='A' else 'CELL_NOT_DEMONSTRATED',Political_source_segment='A_MAINLAND_BANK' if pilot=='A' else 'B_SOUTHERN_1775_CANDIDATE',
            Source_to_real_validated=False,Native_local_control='UNMEASURABLE_NARROWS' if pilot=='A' else 'ONE_SCHEMATIC_HOLDOUT_0.679PX',Independent_full_chain=False,
            Variant_membership_R5=v.get('Alternative_polygon_membership',''),Stable_under_all_qualified_variants='NOT_ESTABLISHED_NO_QUALIFIED_FULL_CHAIN',Core_Manhattan_distance=distance,
            Outside_frozen_R5_support=not r.in_support(w.load('TRANSFORMATIONS.json')['selected_native'],cellgeo),Proposed_RGB='',Applied=False,Reason=reason))
    assert sum(v['Pilot']=='A' for v in rows)==18
    csvout('CANDIDATE_DECISIONS.csv',rows)
    csvout('TERRITORIAL_CHANGES.csv',[],fields=['Pilot','X','Y','State_ID','RGB_before','RGB_after','Owner_before','Owner_after','Evidence','Applied'])
    native=w.load('TRANSFORMATIONS.json');dump('LOCAL_TRANSFORMATIONS.json',dict(native_reference='../R5/TRANSFORMATIONS.json',native_reference_sha256=w.sha(R5/'TRANSFORMATIONS.json'),frozen_native=native['selected_native'],
        native_alternatives=native['tested_native'],new_native_fit_points=0,final_checks_used_for_selection=False,
        source_to_real=dict(A=dict(status='NOT_ACCEPTED',reason='Read new local bank segment, but no new securely homologated distributed source-real controls. Do not refit failed northern caps.'),
                            B=dict(status='NOT_ACCEPTED',reason='Political southern segment distinguished from Vistula rim, but manuscript dating/line equivalence and source-real controls incomplete. Do not reuse ambiguous Pfau39 crosses.')),
        new_source_fits=0,whole_chain_accepted=False))
    dump('DECISION_SUMMARY.json',dict(candidate_count=len(rows),pilot_counts=dict(collections.Counter(v['Pilot'] for v in rows)),classes=dict(collections.Counter(v['Class'] for v in rows)),
        excluded_R5_extra149=True,other_Netze_candidates_outside_local_or_not_directly_adjacent=True,transfers=0))
    print(json.dumps(load('DECISION_SUMMARY.json'),indent=2))

if __name__=='__main__':{'capture':capture,'readings':readings,'palette':palette,'extra_crops':extra_crops,'protocol':protocol,'holdouts':holdouts,'source_details':source_details,'evidence':evidence,'decisions':decisions}[sys.argv[1]]()
