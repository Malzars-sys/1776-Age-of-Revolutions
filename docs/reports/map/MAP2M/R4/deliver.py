"""Build R4 research deliverables. All writes are confined to this directory."""
import sys, json, csv, math, collections, re
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import research as r
import analysis as a

Image.MAX_IMAGE_PIXELS=150000000
FONT='C:/Windows/Fonts/arial.ttf'
def font(n=17):return ImageFont.truetype(FONT,n)
def read_csv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))

def evidence():
    files=[]
    for p in sorted((r.OUT/'EVIDENCE').iterdir()):
        if p.name.endswith(('.source.json','.failure.json')):continue
        m=p.with_name(p.name+'.source.json')
        v=dict(path=p.relative_to(r.ROOT).as_posix(),bytes=p.stat().st_size,sha256=r.sha(p))
        if m.exists():v.update(r.load('EVIDENCE/'+m.name))
        if p.suffix.lower() in ['.png','.jpg']:
            with Image.open(p) as im:v['dimensions_px']=list(im.size)
        files.append(v)
    specs=[dict(id='SBB_N1146_1',title='Carte von der neugemachten Grentze zwischen der acquirirten Provintz und dem Koenigreich Pohlen ...',
        author='Not stated in consulted catalogue',publisher='Manuscript, not a printed edition',survey_date=None,production_date='[1772], inferred catalogue date',publication_date=None,
        edition='Brouillon oder fluechtige Kopie; digitized 2025',scale='circa 1:136000',orientation='Approximately north at top; physical graticule not observed',projection='Not identified',
        institution='Staatsbibliothek zu Berlin',shelfmark='Kart. N 1146/1',notice='https://stabikat.de/DB=1/XMLPRS=N/PPN?PPN=1936716976',
        image_access='https://resolver.staatsbibliothek-berlin.de/SBB000396D400000000',rights='Public Domain Mark 1.0 in catalogue and manifest',access_status='ACQUIRED_FULL_SCAN',
        image_structure='1 western recto + 2 eastern recto, overlapping scan; 3 and 4 versos; 5 colour target, NOT five independent maps',
        coverage='Driesen, Deutsch Krone, Pila, Kamin, Bromberg, Netze and Vistula approach. Inowroclaw city and southern district not fully represented.',
        use='Dated frontier drawing with coloured lines; date of individual annotations and exact colour semantics still to establish; no automatic Jan 1776 polygon',file_prefixes=['BOUNDARY_1772_','SBB_1772_']),
      dict(id='PFAU_1778',title='Special Carte von Pohlen in 35 Sektionen',author='Theodor Philipp von Pfau',publisher='[Berlin], no publisher identified; plates directed by A. le Claire; Schleuten engraver per catalogue',
        survey_date='1772-1773 per catalogue',production_date='Engraving 1775-1778 per catalogue',publication_date='[1778]',edition='First engraved edition per WBC catalogue, not the 1772 original survey',
        scale='circa 1:87500',orientation='South-up approximate; R4 reading raster is rotated exactly 180 degrees, not assumed exact geographic north-up',projection='Not identified',
        institution='Biblioteka Uniwersytecka w Poznaniu / Mirabilia UAM',shelfmark='Edition 588634; shelfmark not independently transcribed',
        notice='https://www.wbc.poznan.pl/dlibra/publication/773069/edition/588634?language=pl',image_access='https://mirabilia.amu.edu.pl/iiif/manifest/588634.json',
        rights='Public domain and unrestricted access stated by catalogue; public IIIF viewer permits download',access_status='SELECTED_FULL_SHEETS_ACQUIRED',
        image_structure='35 manifest canvases; selected index 0001, backing 0002, sheets XXXIX XLV XLVI XLVII XLVIII at width 4000',
        coverage='Detailed Inowroclaw/Goplo, Znin, Czarnkow, Drezdenko, Torun environs. No confirmed Walcz/Kamin full coverage in acquired detailed sheets.',
        use='Physical topography; engraved boundaries not automatically pre-1776',file_prefixes=['PFAU_']),
      dict(id='AGAD_PFAU_COPY',title="Mapa Pfau'a",author='Attributed to Pfau in inventory title; copyist not identified',publisher='Manuscript copy',
        survey_date='Not established for this physical copy',production_date='1800-1815 in official temporary inventory, unit 580',publication_date=None,
        edition='Date conflicts with treating this as the original 1772-1773 field manuscript; unresolved',scale='Not given in consulted inventory',orientation='Not observed on original',projection='Not identified',
        institution='Archiwum Glowne Akt Dawnych, Warsaw',shelfmark='fonds 447, unit 580; AK.103,104,105,106,107,107A',
        notice='https://www.agad.gov.pl/inwentarze/kart447InOd.html',image_access=None,rights='Catalogue consulted only; no manuscript raster acquired',access_status='CATALOGUE_ONLY_DATE_CONFLICT',
        coverage='Cannot certify sheet coverage without original',use='Dating contradiction. The scan-gallery snippet in HTML is commented-out boilerplate, not an active image link.',file_prefixes=['AGAD_']),
      dict(id='GRUND_1775',title='Carte von der neu acquirirten Provintz West-Preussen benebst dem gantzen Netz-Fluss und einem Stueck vom Warthe-Bruch und deren Situation',
        author='[I. A.] Grund [d. Aelteren] in SBB notice; often cited J.A. Grund',publisher='o.O., manuscript coloured',survey_date=None,production_date='1775',publication_date=None,
        edition='Original manuscript; full public scan not located in inspected records',scale='circa 1:222000',orientation='N unten stated in SBB catalogue (south-up)',projection='Not identified',
        institution='Staatsbibliothek zu Berlin',shelfmark='Kart. N 10051; PPN428487513',notice='https://stabikat.de/DB=1/XMLPRS=N/PPN?PPN=428487513',
        image_access='Existing western excerpt retained in MAP2M/EVIDENCE/GRUND_1775_DETAIL.jpg',rights='Full reproduction terms to confirm with institution; no order placed',access_status='WESTERN_EXCERPT_REUSED_FULL_NOT_OBTAINED',
        coverage='Original titled Netze basin; acquired excerpt Driesen-Landsberg only. Catalogue explicitly excludes northern Pomerellen.',
        use='Priority alternative now complemented by public N1146/1. Official reproduction service available; no paid request sent.',file_prefixes=['GRUND_','SBB_REPRODUCTIONS']),
      dict(id='ANKLAM_1773',title='Grund Riss von der Stadt Anklam, folded plate in Topographische und Chronologische Beschreibung ...',author='Carl Friedrich Stavenhagen (book); plate draughtsman not identified',
        publisher='Greifswald: Roese',survey_date='Not identified separately',production_date='No independent plate date identified',publication_date='1773',edition='BSB bsb10001079, scan 35 of 658',scale='No geodetic scale certified',
        orientation='North approximately at bottom; no assumption about exact bearing',projection='Local town plan, no geographic projection established',institution='Bayerische Staatsbibliothek',shelfmark='4 Bor.46u; BSB-ID991042738029707356',
        notice='https://www.digitale-sammlungen.de/de/details/bsb10001079',image_access='https://api.digitale-sammlungen.de/iiif/image/v2/bsb10001079_00035/full/4000,/0/default.jpg',rights='Manifest: NoC-NC1.0; use here for non-commercial research, not a blanket licence for redistribution',
        access_status='ACQUIRED_FOLDED_PLAN',coverage='Anklam old town, Peene bridge and north-bank mill, not whole Demmin-Wolgast frontier',
        use='Physical homologues; legend identifies two churches, gate and powder tower. Contains no complete 1776 political boundary.',file_prefixes=['ANKLAM_1773_']),
      dict(id='MODERN_CONTROL_METADATA',title='Physical reference objects: OSM Anklam footprints, NID Polish historic sites, Anklam municipal history',author='OSM contributors; Narodowy Instytut Dziedzictwa; Hansestadt Anklam',publisher='Respective data holders',
        survey_date='Mixed modern dates, not geodetically certified here',production_date='Retrieved 2026-10-15',publication_date='Various',edition='Read-only public data snapshot',scale='Building-scale reference, not political boundary data',orientation='WGS84 longitude/latitude',projection='EPSG4326 for coordinate fields',institution='OSM / NID / City of Anklam',shelfmark=None,
        notice='See per-file URLs',image_access=None,rights='OSM ODbL attribution required; NID descriptions may be CC BY-NC-ND, no site photos downloaded; city metadata reference only',
        access_status='ACQUIRED_METADATA',coverage='Anklam and five Inowroclaw-area church sites',use='Stability and coordinate checks, not sovereignty evidence; no addresses of individual persons used in reports',file_prefixes=['OSM_ANKLAM','NID_','ANKLAM_CITY_'])]
    for s in specs:
        prefixes=s.pop('file_prefixes')
        s['files']=[v for v in files if any(Path(v['path']).name.startswith(p) for p in prefixes)]
    # Retained originals retain their independent rights and original hashes; no re-download.
    r.dump('SOURCES.json',dict(retrieved_on='2026-10-15',sources=specs,all_new_acquired_files=files,
        retained_sources_inventory='EXISTING_ASSETS.json',retained_model_provenance='PRIOR_TRANSFORMATIONS.json',
        retained_catalogue_note='GStA Tit50 Nr1a=1772 boundary boards; Nr1=1776 Thorn posts (not dated Jan1); Nr2=1777 regulation; Nr10=1776-1780 Kruszwice estates. Metadata only, no manuscript examined.',
        independence='Pfau sheets are one survey family. Two copies of Mayer or Homann are not independent political proofs. SBB N1146 rectos/versos are one object.',
        archive_research_lead='Kart.N1163 (Behm 1778, 1777 regulation) is a literature lead only, not acquired or used as a Jan1776 boundary.'))
    coverage=[]
    for ident,areas,limits in [
        ('SBB_N1146_1','Krone;Pila;Kamin;Bromberg;Netze-Vistula','Inowroclaw southern district outside full detailed extent; coloured-line interpretation not yet a certified Jan1776 perimeter'),
        ('PFAU_39','Inowroclaw;Goplo;Gniewkowo;Strzelno;Pakosc','Provisional source calibration rejected for political tracing; edition1778'),
        ('PFAU_45','Torun and Vistula physical context','Thorn explicitly excluded from political proposals'),
        ('PFAU_46','Znin and southern Netze environs','No full four-district perimeter certified'),
        ('PFAU_47','Czarnkow middle Netze','No confirmed Walcz/Kamin extent in this detailed sheet'),
        ('PFAU_48','Drezdenko western Netze','Not a full Krone district sheet'),
        ('PFAU_0001','Series index','Coverage index only, not a detailed frontier source'),
        ('PFAU_0002','Backing and handwritten sheet list','Not geographic map coverage'),
        ('GRUND_1775','Driesen-Landsberg acquired excerpt','Full sheet still absent; do not extrapolate excerpt to Kamin/Inowroclaw'),
        ('ANKLAM_1773','Town;bridge;Peendamm mill','No whole Peene or Wolgast coverage'),
        ('MAYER_RETAINED','Demmin-Anklam-Wolgast regional','General map and unresolved native alignment'),
        ('GEOGREIF_RETAINED','Anklam CIIIa1/a2,1694','Local-research-only images; predates1720 treaty, not sovereignty1776'),
        ('GUESSEFELD_RETAINED','Regional Netze district1775','Generalized geography; inherited locator fit unvalidated'),
        ('HOMANN_INSET_RETAINED','Four administrative districts schematic','Plate state/date unresolved; atlas binding date is not plate publication proof')]:
        coverage.append(dict(Source_ID=ident,Observed_coverage=areas,Limitations=limits,Political_perimeter_certified='NO'))
    r.csvout('SOURCE_COVERAGE.csv',coverage)

def candidates():
    b=r.load('BASELINE.json');bmp=r.r3.r2.core.packed(r.ROOT/'map_data/provinces.png')
    lookup={int(v['key'][0][1:],16):(v['key'][1],v['key'][2]) for v in b['inventory']['owners']}
    sets={}
    sets['PEENE']=[(x,y,'SWE','B','MAYER_RETAINED;LUNG_R3','R3 rejected Peenestrom band: shore and channel unresolved') for x,y in r.r3.load('GEOMETRY_REVIEW.json')['PEENE']['rejected_near_peenestrom']]
    sets['NETZE']=[]
    for v in read_csv(r.OUT.parent/'NETZE/CANDIDATE_CELLS.csv'):
        x,y=int(v['X']),int(v['Y']);val=int(bmp[y,x]);owner=lookup.get(val,('',''))[1]
        if owner=='PRU':continue  # Already accepted R3 core is NOT a new transfer proposal.
        assert val!=0x41A021
        sets['NETZE'].append((x,y,'PRU','B','GUESSEFELD_RETAINED;SBB_N1146_1','Inherited regional hypothesis, not recomputed from new scan; exact district/boundary unvalidated'))
    out={}
    for sector,values in sets.items():
        coords={(x,y) for x,y,*_ in values};group={};i=0
        for start in sorted(coords):
            if start in group:continue
            i+=1;todo=[start];group[start]=i
            while todo:
                x,y=todo.pop()
                for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if q in coords and q not in group:group[q]=i;todo.append(q)
        rows=[]
        for x,y,want,cl,source,why in values:
            rgb=int(bmp[y,x]);state,owner=lookup[rgb]
            rows.append(dict(X=x,Y=y,Pixel_center_X=x+.5,Pixel_center_Y=y+.5,State_ID=state,Current_RGB=f'x{rgb:06X}',Proposed_RGB='',Current_owner=owner,
                Historical_owner_hypothesis=want,Sector=sector,District='UNASSIGNED_SUBDISTRICT' if sector=='NETZE' else 'Peenestrom approach',
                Contiguous_group=f'{sector}_B_{group[x,y]:02}',Class=cl,Sources=source,
                Source_boundary_reading='Inherited candidate; new dated map NOT silently substituted',Geographic_model='Prior unvalidated alignment; see PRIOR_TRANSFORMATIONS.json',
                Validation='DO_NOT_APPLY_R4',Uncertainty=why,Applied='False'))
        r.csvout(sector+'_CANDIDATE_CELLS.csv',rows,fields=list(rows[0]) if rows else ['X','Y','Class','Validation']);out[sector]=rows
    # Unlocated documentary gaps must not be assigned invented pixels or RGBs.
    unresolved=[('PEENE_NATIVE','Peene','C','Anklam plan source-to-real fit improves local town position, but native Peene/bridge not homologated','Identify physical game-raster anchors independently; retain mainland and Usedom masks'),
        ('PEENE_CHANNEL','Wolgast-Peenestrom','B','18 rejected R3 cells remain ambiguous; narrow channel schematized','Dedicated shore correspondence; avoid converting islands into mainland'),
        ('GRUND_FULL','Netze','C','Full Grund1775 reproduction not found in inspected access records','Official SBB reproduction quote/request requires user authorisation; use N1146 as free complement'),
        ('AGAD_DATE','Netze','C','Official unit580 dates AK103-107A to1800-1815; not proven original1772 survey','Obtain actual manuscript images and resolve copy/annotation dating; no external request sent'),
        ('KRONE','Deutsch Krone','B','New1772 manuscript covers region; current Wałcz assignment cannot delimit full district','Read border on full panel1 and establish physical source-real/native controls'),
        ('KAMIN','Kamin','B','New1772 manuscript contains Kamin; no independent native calibration','Do not allocate whole current RGB from city location'),
        ('BROMBERG','Bromberg','B','85-cell R3 core accepted; outer fringe line still not independently registered','Preserve xEDB010 and treat eastern/western fringes separately'),
        ('INOWROCLAW','Inowroclaw','C','New1772 sheet does not cover entire southern district; Pfau1778 dating and calibration unresolved','Reject present Pfau fit for border work; secure dated southern boundary and certified homologues'),
        ('THORN','Torun','C','x41A021 known out-of-scope anomaly;1776 boundary-post file not specifically datedJan1','Leave unchanged; separate future task'),
        ('PLATE_DATE','Netze','C','Homann inset plate state undated; not independent of reused engraving','Do not use atlas1793 binding date or title1752 as actual plate state date'),
        ('COLOUR_SEMANTICS','Netze','C','N1146 labelled draft/copy; coloured lines and red private-estate names require separate interpretation','Do not equate every coloured line or red name with a sovereign boundary')]
    r.csvout('UNRESOLVED.csv',[dict(ID=i,Sector=s,Class=c,Issue=p,Required_evidence=n) for i,s,c,p,n in unresolved])
    r.dump('CANDIDATE_SUMMARY.json',{s:dict(rows=len(rows),classes=dict(collections.Counter(v['Class'] for v in rows)),groups=len(set(v['Contiguous_group'] for v in rows)),applied=0) for s,rows in out.items()})
    return out

def source_panels():
    rows=read_csv(r.OUT/'CONTROL_POINTS.csv')
    for source,file,rot in [('ANKLAM_1773','ANKLAM_1773_PLAN.jpg',False),('PFAU_39','PFAU_39.jpg',True)]:
        im=Image.open(r.OUT/'EVIDENCE'/file).convert('RGB')
        if rot:im=im.transpose(Image.Transpose.ROTATE_180)
        scale=1400/im.width;im=im.resize((1400,round(im.height*scale)))
        d=ImageDraw.Draw(im)
        for row in rows:
            if row['source']!=source:continue
            x,y=float(row['source_x'])*scale,float(row['source_y'])*scale;c='#006bff' if row['role']=='FIT' else '#e00000'
            d.ellipse((x-5,y-5,x+5,y+5),outline=c,width=3);d.text((x+8,y-10),row['id']+' '+row['role'],fill=c,font=font(17))
        canvas=Image.new('RGB',(1400,im.height+90),'white');canvas.paste(im,(0,80));d=ImageDraw.Draw(canvas)
        d.text((20,10),source+' | POINTS PROVISOIRES, pas une frontiere validee',fill='black',font=font(24))
        d.text((20,44),'Bleu: ajustement; rouge: controles reserves. Ambiguites dans CONTROL_POINTS.csv.',fill='black',font=font(19))
        canvas.save(r.OUT/(source+'_CONTROL_READING.png'))

def geographic_exports():
    models=r.load('TRANSFORMATIONS.json')['source_to_real'];result={}
    for source,file,rot in [('ANKLAM_1773','ANKLAM_1773_PLAN.jpg',False),('PFAU_39','PFAU_39.jpg',True)]:
        src=Image.open(r.OUT/'EVIDENCE'/file).convert('RGBA')
        if rot:src=src.transpose(Image.Transpose.ROTATE_180)
        model=models[source]['similarity'];m=np.array(model['matrix_source_xy1_to_local_EN_m']);origin=model['origin_lon_lat']
        geo=a.unmetric(a.apply([[0,0],[src.width-1,0],[src.width-1,src.height-1],[0,src.height-1]],m),origin)
        west,south=geo.min(axis=0);east,north=geo.max(axis=0);w=1200;dx=(east-west)/w
        dy=dx*math.cos(math.radians(origin[1]));h=math.ceil((north-south)/dy)
        # Output pixel centre lon/lat -> work-plane EN -> inverse source xy.
        en0=a.metric([[west+dx/2,north-dy/2]],origin)[0];ex=a.metric([[west+dx*1.5,north-dy/2]],origin)[0]-en0;ey=a.metric([[west+dx/2,north-dy*1.5]],origin)[0]-en0
        inv=np.linalg.inv(m[:2]);base=(en0-m[2])@inv;vx=ex@inv;vy=ey@inv
        data=(vx[0],vy[0],base[0],vx[1],vy[1],base[1])
        im=src.transform((w,h),Image.Transform.AFFINE,data,resample=Image.Resampling.BILINEAR)
        name=source+'_WGS84_DIAGNOSTIC';im.save(r.OUT/(name+'.png'))
        (r.OUT/(name+'.pgw')).write_text('\n'.join(map(str,[dx,0,0,-dy,west+dx/2,north-dy/2]))+'\n',encoding='ascii')
        (r.OUT/(name+'.prj')).write_text('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]',encoding='ascii')
        result[source]=dict(path=name+'.png',worldfile=name+'.pgw',crs='EPSG:4326',bounds_W_S_E_N=[west,north-h*dy,east,north],
            dimensions=[w,h],model='similarity',accepted_for_political_tracing=False,warning='Diagnostic georeferenced raster only; no certified geographic accuracy; not a game-native exact overlay')
    r.dump('GEOREFERENCED_EXPORTS.json',result)

def native_overlays():
    from georeference.model import forward
    models=r.load('TRANSFORMATIONS.json');native_model=json.loads((r.ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json').read_text())['model'];offset=np.array([-1,5.9])
    bmp=r.r3.r2.core.packed(r.ROOT/'map_data/provinces.png');owners={int(v['key'][0][1:],16):v['key'][2] for v in r.load('BASELINE.json')['inventory']['owners']}
    rows=read_csv(r.OUT/'CONTROL_POINTS.csv');saved={}
    for sector,bbox,scale in [('PEENE',(4378,724,4420,754),28),('NETZE',(4460,750,4530,800),17)]:
        x0,y0,x1,y1=bbox;local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),[190,218,234],np.uint8)
        colors={'PRU':[125,159,202],'PLC':[226,173,185],'SWE':[228,211,125]}
        for val in np.unique(local):
            if int(val) in owners:arr[local==val]=colors.get(owners[int(val)],[195,195,195])
        base=Image.fromarray(arr).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST).convert('RGBA')
        if sector=='PEENE':
            src=Image.open(r.ROOT/'docs/reports/map/MAP2L/PRUSSIAN_BORDERS/EVIDENCE/MAYER_1763_GREIFSWALD.jpg').convert('RGBA')
            m=np.array(r.r3.load('GEOMETRY_REVIEW.json')['PEENE']['source_matrix']);tag='Mayer: ancien recalage non certifie'
        else:
            src=Image.open(r.OUT/'EVIDENCE/PFAU_39.jpg').convert('RGBA').transpose(Image.Transpose.ROTATE_180)
            points=[v for v in rows if v['source']=='PFAU_39' and v['role']=='FIT'];x=np.array([[float(v['source_x']),float(v['source_y'])] for v in points]);g=np.array([[float(v['longitude']),float(v['latitude'])] for v in points])
            # Rendering-only local affine composition. This is not a newly validated native model.
            m=a.fit(x,forward(native_model,g)+offset,'affine');tag='Pfau39: calage diagnostique rejete pour les frontieres'
        inv=np.linalg.inv(m[:2]);o=(np.array([x0,y0])-m[2])@inv;vx=np.array([1/scale,0])@inv;vy=np.array([0,1/scale])@inv
        overlay=src.transform(base.size,Image.Transform.AFFINE,(vx[0],vy[0],o[0],vx[1],vy[1],o[1]),resample=Image.Resampling.BILINEAR)
        alpha=np.array(overlay.getchannel('A'));overlay.putalpha(Image.fromarray((alpha*.38).astype(np.uint8)));base=Image.alpha_composite(base,overlay).convert('RGB');d=ImageDraw.Draw(base)
        for x in range(x0,x1+1):d.line(((x-x0)*scale,0,(x-x0)*scale,base.height),fill='#666666',width=1)
        for y in range(y0,y1+1):d.line((0,(y-y0)*scale,base.width,(y-y0)*scale),fill='#666666',width=1)
        for x in range((x0//5+1)*5,x1,5):d.text(((x-x0)*scale+2,4),str(x),fill='black',font=font(15))
        for y in range((y0//5+1)*5,y1,5):d.text((3,(y-y0)*scale+2),str(y),fill='black',font=font(15))
        for row in read_csv(r.OUT/(sector+'_CANDIDATE_CELLS.csv')):
            x,y=int(row['X']),int(row['Y'])
            if x0<=x<x1 and y0<=y<y1:d.rectangle(((x-x0)*scale+2,(y-y0)*scale+2,(x+1-x0)*scale-2,(y+1-y0)*scale-2),outline='#db5900',width=2)
        if sector=='PEENE':
            hydro=json.loads((r.OUT.parent/'R3/EVIDENCE/LUNG_PEENE_LAWA.geojson').read_text())['features']
            for f in hydro:
                if f['properties'].get('LA_GN')!='Peene':continue
                parts=f['geometry']['coordinates'];parts=[parts] if f['geometry']['type']=='LineString' else parts
                for g in parts:
                    p=forward(native_model,g)+offset;d.line([((x-x0)*scale,(y-y0)*scale) for x,y in p],fill='#0044ee',width=3)
        canvas=Image.new('RGB',(base.width,base.height+160),'white');canvas.paste(base,(0,100));d=ImageDraw.Draw(canvas)
        d.text((15,10),sector+' | R3 installe + superposition DIAGNOSTIQUE',fill='black',font=font(25));d.text((15,48),tag,fill='#9b0000',font=font(19))
        d.text((15,canvas.height-50),'Fond: PRU bleu / PLC rose / SWE jaune. Cadres orange: B, ne pas appliquer.',fill='black',font=font(17))
        d.text((15,canvas.height-26),'Projection native non certifiee; aucun changement de proprietaire dans R4.',fill='#9b0000',font=font(17))
        canvas.save(r.OUT/(sector+'_GEOREFERENCE.png'));saved[sector]=dict(matrix=m.tolist(),purpose='Rendering only, not accepted native calibration',extent=bbox,source_opacity=.38)
    models['native_visualisation_only']=saved;r.dump('TRANSFORMATIONS.json',models)

def validate():
    b=r.load('BASELINE.json');current=r.economy.runtime_hashes();missing=[];changed=[]
    for p,h in b['hashes'].items():
        if p not in current:missing.append(p)
        elif current[p]!=h:changed.append(p)
    new=sorted(set(current)-set(b['hashes']));earlier_changed=[p for p,h in b['earlier_proofs'].items() if not (r.ROOT/p).is_file() or r.sha(r.ROOT/p)!=h]
    inventory=r.r3.r2.core.qa.inventory();bitmap=r.r3.r2.core.packed(r.ROOT/'map_data/provinces.png');tests=[]
    def check(name,ok):tests.append(dict(name=name,pass_=bool(ok)))
    check('All functional file hashes preserved',not missing and not changed and not new)
    check('Earlier MAP2M evidence preserved',not earlier_changed)
    check('HEAD preserved',r.r3.r2.head()==b['git_head']);check('Git index preserved',r.sha(r.ROOT/'.git/index')==b['git_index_sha256'])
    check('Bitmap preserved',r.sha(r.ROOT/'map_data/provinces.png')==b['bitmap_sha256'])
    check('Full effective inventory unchanged',inventory==b['inventory'])
    check('World population 835804980',sum(v['count'] for v in inventory['pops'])==835804980)
    for rgb,count in [(0x567452,357),(0xEDB010,85),(0xFCC7B7,142)]:check(f'x{rgb:06X} retains {count} cells',int((bitmap==rgb).sum())==count)
    check('44 inherited duplicate RGBs unchanged',len(inventory['duplicates'])==44 and inventory['duplicates']==b['inventory']['duplicates'])
    check('12 inherited unresolved references unchanged',len(inventory['errors'])==12 and inventory['errors']==b['inventory']['errors'])
    lookup={v['key'][0]:(v['key'][1],v['key'][2]) for v in inventory['owners']}
    for sector in ['PEENE','NETZE']:
        rows=read_csv(r.OUT/(sector+'_CANDIDATE_CELLS.csv'))
        check(sector+' candidates resolve to current RGB/State_ID/owner',all(f'x{int(bitmap[int(v["Y"]),int(v["X"]) ]):06X}'==v['Current_RGB'] and lookup[v['Current_RGB']]==(v['State_ID'],v['Current_owner']) for v in rows))
        check(sector+' no invented RGB, no A or applied flag',all(not v['Proposed_RGB'] and v['Class']!='A' and v['Applied']=='False' for v in rows))
        check(sector+' excludes Thorn',all(v['Current_RGB']!='x41A021' for v in rows))
        check(sector+' unique cells',len({(v['X'],v['Y']) for v in rows})==len(rows))
    for p in sorted((r.OUT/'EVIDENCE').glob('*.source.json')):
        target=p.with_name(p.name.removesuffix('.source.json'));meta=json.loads(p.read_text());check('Acquired hash '+target.name,target.is_file() and r.sha(target)==meta['sha256'])
    # Mathematical unit check: the raster-y reflection is explicit and tested.
    x=np.array([[0,0],[100,0],[0,100]],float);m=np.array([[2,1],[1,-2],[20,30]]);y=a.apply(x,m)
    check('Similarity reflection and forward transform unit test',np.allclose(a.apply(x,a.fit(x,y,'similarity')),y))
    check('Independent checks excluded from fit IDs',all(not set(v['fit_ids'])&set(v['check_ids']) for models in r.load('TRANSFORMATIONS.json')['source_to_real'].values() for v in models.values()))
    result=dict(status='PASS_RESEARCH_FILE_INTEGRITY' if all(v['pass_'] for v in tests) else 'FAIL',historical_status='MAP_2M_R4_PARTIAL',tests=tests,passed=sum(v['pass_'] for v in tests),total=len(tests),
        functional_files_checked=len(current),functional_missing=missing,functional_changed=changed,functional_new=new,earlier_evidence_changed=earlier_changed,
        world_population=835804980,automated_engine_test=False,R3_runtime_status='PASS_RUNTIME_USER_VALIDATED',R4_runtime_test='NOT_APPLICABLE_RESEARCH_ONLY',
        prior_anomalies=dict(duplicate_RGBs=inventory['duplicates'],invalid_references=inventory['errors']),
        calibration=r.load('CALIBRATION_DIAGNOSTIC.json'),new_accepted_native_control_points=0,new_A_candidates=0,applied_territorial_changes=0,
        colgrep=dict(calls_this_continuation=0,reason='Known paths supplied by preserved context and audited reports; AGENTS rule3 forbids redundant semantic call',exact_token_saving=None))
    r.dump('GEOMETRY_VALIDATION.json',result)
    r.dump('DELIVERABLE_MANIFEST.json',{p.relative_to(r.OUT).as_posix():dict(sha256=r.sha(p),bytes=p.stat().st_size) for p in r.OUT.rglob('*') if p.is_file() and p.name!='DELIVERABLE_MANIFEST.json'})
    print(result['status'],result['passed'],'/',result['total'],'checks;',len(current),'functional files; historical status PARTIAL')
    if not all(v['pass_'] for v in tests):raise SystemExit('Integrity failure; see GEOMETRY_VALIDATION.json')

if __name__=='__main__':
    if sys.argv[1]=='build':evidence();candidates();source_panels();geographic_exports();native_overlays()
    elif sys.argv[1]=='validate':validate()
