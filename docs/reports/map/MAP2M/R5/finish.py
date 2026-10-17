"""R5 presentation and differential tests, never writes functional files."""
import sys,json,csv,collections,subprocess,os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import work as w
import review as r

def images():
    bmp,water,rivers,_=w.physical_masks();owners={int(v['key'][0][1:],16):v['key'][2] for v in w.load('BASELINE.json')['inventory']['owners']}
    points=w.load('REVISED_CONTROL_OBSERVATIONS.json')['points'];model=w.load('TRANSFORMATIONS.json')['selected_native']
    # Physical observations with no political colours. Errors remain readable.
    controls=Image.new('RGB',(1900,1080),'white');d=ImageDraw.Draw(controls)
    panels=[((4340,706,4532,741),8,(20,80)),((4415,772,4435,790),22,(20,510)),((4550,775,4590,803),16,(650,510))]
    for bbox,s,origin in panels:
        x0,y0,x1,y1=bbox;loc=water[y0:y1,x0:x1];arr=np.where(loc[:,:,None],[202,223,245],[239,231,212]).astype(np.uint8);arr[rivers[y0:y1,x0:x1]]=[30,90,220]
        im=Image.fromarray(arr).resize(((x1-x0)*s,(y1-y0)*s),Image.Resampling.NEAREST);draw=ImageDraw.Draw(im)
        for v in points:
            if not(x0<=v['X']<x1 and y0<=v['Y']<y1):continue
            x=(v['X']-x0)*s;y=(v['Y']-y0)*s;c='#0055cc' if v['Role']=='FIT' else '#a000c0' if v['Role']=='REVISED_CHECK' else '#c00000'
            draw.ellipse((x-5,y-5,x+5,y+5),outline=c,width=3);draw.text((x+7,y+3),v['ID'],fill=c,font=w.font(15))
            pred=r.forward(model,[[v['Longitude'],v['Latitude']]])[0];px=(pred[0]-x0)*s;py=(pred[1]-y0)*s
            draw.line((x,y,px,py),fill=c,width=2);draw.line((px-4,py,px+4,py),fill=c,width=2);draw.line((px,py-4,px,py+4),fill=c,width=2)
        controls.paste(im,origin)
    d.text((20,15),'R5 - observations physiques natives et predictions du modele empirique',fill='black',font=w.font(28))
    d.text((20,420),'Bleu : FIT. Rouge : CHECK reserve. Violet : Usedom corrige, hors statistique pristine.',fill='black',font=w.font(22))
    d.text((20,455),'Cercle : observation. Croix : prediction. Pas de plus-proche-rivage ajuste pour ces controles.',fill='black',font=w.font(20))
    d.text((20,1010),'4 controles originaux : moyenne 2,08 px ; maximum 3,19 px. Ni precision mondiale, ni frontiere validee.',fill='black',font=w.font(22))
    controls.save(w.OUT/'NATIVE_CONTROL_REVIEW.png')
    candidates=r.read_csv(w.OUT/'CANDIDATE_CELLS.csv');source=w.prior.r3.load('GEOMETRY_REVIEW.json')['PEENE']['historical_polygon'];mp=w.load('MAYER_PHYSICAL_CALIBRATION.json')['similarity']
    for sector,bbox,s in [('PEENE',(4385,730,4414,748),24),('NETZE',(4460,749,4530,785),12)]:
        x0,y0,x1,y1=bbox;loc=bmp[y0:y1,x0:x1];arr=np.full((*loc.shape,3),[205,225,246],np.uint8)
        for val in np.unique(loc):
            if int(val) in owners:arr[loc==val]={'PRU':[120,161,205],'SWE':[240,210,110],'PLC':[223,162,179]}.get(owners[int(val)],[208,208,208])
        base=Image.fromarray(arr).resize(((x1-x0)*s,(y1-y0)*s),Image.Resampling.NEAREST);pw,ph=base.size;canvas=Image.new('RGB',(pw*2+60,ph+260),'white');draw=ImageDraw.Draw(canvas)
        for i,title in enumerate(['Avant : reference R3','R5 installe : AUCUN TRANSFERT']):
            im=base.copy();d=ImageDraw.Draw(im)
            for x in range(x0,x1):d.line(((x-x0)*s,0,(x-x0)*s,ph),fill='#777777')
            for y in range(y0,y1):d.line((0,(y-y0)*s,pw,(y-y0)*s),fill='#777777')
            if i==1:
                for row in candidates:
                    x,y=int(row['X']),int(row['Y'])
                    if row['Sector']==sector and x0<=x<x1 and y0<=y<y1:d.rectangle(((x-x0)*s+2,(y-y0)*s+2,(x+1-x0)*s-2,(y+1-y0)*s-2),outline='#e05a00' if row['Class']=='B' else '#555555',width=2)
                if sector=='PEENE':
                    geo=w.old.unmetric(w.old.apply(np.array(source),mp['matrix']),mp['origin_lon_lat']);p=r.forward(model,geo)[3:]
                    d.line([((x-x0)*s,(y-y0)*s) for x,y in p],fill='#a000b0',width=3)
                    fs=json.loads((w.OUT.parent/'R3/EVIDENCE/LUNG_PEENE_LAWA.geojson').read_text())['features']
                    for f in fs:
                        if f['properties'].get('LA_GN')!='Peene':continue
                        parts=f['geometry']['coordinates'];parts=[parts] if f['geometry']['type']=='LineString' else parts
                        for part in parts:
                            p=r.forward(model,part);d.line([((x-x0)*s,(y-y0)*s) for x,y in p],fill='#0033ff',width=2)
            ox=20+i*(pw+20);canvas.paste(im,(ox,100));draw.text((ox,65),title,fill='black',font=w.font(22))
        draw.text((20,15),sector+' - avant/apres des proprietaires (fonds strictement identiques)',fill='black',font=w.font(25))
        draw.text((20,ph+125),'Fond: PRU bleu / SWE jaune / PLC rose. Cadres orange: B ; gris: C. Aucun A.',fill='black',font=w.font(19))
        if sector=='PEENE':
            draw.text((20,ph+160),'Violet: hypothese Mayer reprojetee, pas une nouvelle limite installee.',fill='#8a008a',font=w.font(19))
            draw.text((20,ph+195),'Bleu vif: Peene moderne LUNG reprojetee, pas preuve de souverainete 1776.',fill='#0033aa',font=w.font(19))
        else:
            draw.text((20,ph+160),'Gris: hypotheses heritees, sans conversion politique source vers reel validee.',fill='#555555',font=w.font(19))
            draw.text((20,ph+195),'Aucun trace politique nouvellement valide, aucun transfert installe.',fill='black',font=w.font(19))
        draw.text((20,ph+228),'Les divergences geometriques restent ouvertes. Thorn exclu.',fill='black',font=w.font(19))
        canvas.save(w.OUT/(sector+'_BEFORE_AFTER.png'))
    # Annotated source controls, not a new historical map or changed bitmap.
    p=w.ROOT/'docs/reports/map/MAP2L/PRUSSIAN_BORDERS/EVIDENCE/MAYER_1763_GREIFSWALD.jpg';im=Image.open(p).convert('RGB').resize((1898,1536));d=ImageDraw.Draw(im)
    for row in mp['source_points']:
        x,y=np.array(row['xy'])*2;c='blue' if row['role']=='FIT' else 'red';d.ellipse((x-6,y-6,x+6,y+6),outline=c,width=4);d.text((x+8,y+8),row['ID']+' '+row['role'],fill=c,font=w.font(20))
    im.save(w.OUT/'MAYER_SOURCE_CONTROLS.png')

def anklam_chain():
    model=w.load('TRANSFORMATIONS.json')['selected_native'];rows=r.read_csv(w.R4/'CONTROL_POINTS.csv');transform=json.loads((w.R4/'TRANSFORMATIONS.json').read_text())['source_to_real']['ANKLAM_1773']['similarity'];results=[]
    for v in rows:
        if v['source']!='ANKLAM_1773':continue
        g=w.old.unmetric(w.old.apply([[float(v['source_x']),float(v['source_y'])]],transform['matrix_source_xy1_to_local_EN_m']),transform['origin_lon_lat'])[0];p=r.forward(model,[g])[0]
        results.append(dict(id=v['id'],role=v['role'],source_estimated_geo=g.tolist(),native_estimate=p.tolist(),reference_geo=[float(v['longitude']),float(v['latitude'])],native_observation=None,
            warning='No native historical-building homologue. This is a chained estimate, not a new independent city control.'))
    p=np.array([v['native_estimate'] for v in results]);w.dump('ANKLAM_CHAIN.json',dict(points=results,point_extent_px=(p.max(axis=0)-p.min(axis=0)).tolist(),
        conclusion='Town and Peendamm mill occupy less than one native pixel of separation; cannot allocate a large province based on urban point position.',source_controls_unchanged=True,new_fit_points=0,
        excluded_extra_control='Heilig-Geist historic church not uniquely homologated to a surviving footprint in retained XML; modern bridge replaced repeatedly. Neither added by guesswork.'))

def unresolved():
    rows=[('NATIVE_SCOPE','B','Coarse regional model verified only on sparse schematic physical landmarks','2.08px mean/3.19px max across four original reserved points, not a universal error bound; reserve a new final test set before further model selection'),
      ('USEDOM_REVIEW','B','Original extrema window selected Ruegen, not Usedom; corrected observation is not pristine','Keep original and revised measurements, use component-specific cape definitions; do not count correction as independent validation'),
      ('MAYER_SOUTH','B','Northern physical capes do not validate extrapolated southern political boundary','Add distributed physical source-to-real controls near Demmin/Anklam/Wolgast; no river-nearest-distance substitute'),
      ('PEENESTROM18','B','18 inherited candidates not defensibly A after source/native uncertainty','Keep raster unchanged; use water-arm morphology and historical east-bank boundary separately; do not enlarge Peendamm'),
      ('PFAU_IDENTITIES','C','Inowroclaw/Pakosc church identities not demonstrated; global frame change cannot explain affine residuals','Identify individual church symbols by street/water configurations with dated site plans, then fix new independent controls before fitting'),
      ('PFAU_SEAMS','C','No homologated seam network between five acquired sheets','Read identical physical features at a common edge or use independently controlled per-sheet model; no visual geographic collage'),
      ('NETZE_POLITICAL_LINE','C','1772 draft coloured line state and later modifications unresolved in source-to-real space','Trace identified political line separately from private estate annotations, resolve dated1776/1777 states; do not use1778 automatically'),
      ('INOWROCLAW_SOUTH','C','1772 manuscript does not show whole southern district; native fit support weaker here','Add a source dated byJan1776 and physical anchors bracketing southern extent; do not colour entire xC02121 from city estimate'),
      ('THORN','C','x41A021 known anomaly excluded','Leave unchanged; separate future task'),
      ('INHERITED_ANOMALIES','C','44 duplicate RGBs and12 unresolved references are preexisting','Preserve and report separately, not silently repair out of scope')]
    w.csvout('UNRESOLVED.csv',[dict(ID=i,Class=c,Issue=p,Concrete_action=n) for i,c,p,n in rows])

def validate():
    b=w.load('BASELINE.json');current=w.prior.economy.runtime_hashes();inventory=w.prior.r3.r2.core.qa.inventory();bmp,_,_,_=w.physical_masks();tests=[]
    def check(name,ok):tests.append(dict(name=name,passed=bool(ok)))
    check('Functional files byte-identical to start R5',current==b['runtime_hashes'])
    check('Functional files also identical to accepted R4/R3 reference',current==json.loads((w.R4/'BASELINE.json').read_text())['hashes'])
    check('All R4 files preserved by hash',all((w.ROOT/p).is_file() and w.sha(w.ROOT/p)==h for p,h in b['R4_hashes'].items()))
    check('Git HEAD unchanged',w.prior.r3.r2.head()==b['git_head']);check('Git index unchanged',w.sha(w.ROOT/'.git/index')==b['git_index_sha256'])
    check('Bitmap unchanged',w.sha(w.ROOT/'map_data/provinces.png')==b['bitmap_sha256'])
    check('Complete effective inventory unchanged',inventory==b['inventory'])
    check('Global population835804980',sum(v['count'] for v in inventory['pops'])==835804980)
    for value,count in [(0x567452,357),(0xEDB010,85),(0xFCC7B7,142)]:check(f'x{value:06X} retains{count}',int((bmp==value).sum())==count)
    check('44 inherited RGB duplicates preserved',len(inventory['duplicates'])==44 and inventory['duplicates']==b['inventory']['duplicates'])
    check('12 inherited invalid references preserved',len(inventory['errors'])==12 and inventory['errors']==b['inventory']['errors'])
    lookup={int(v['key'][0][1:],16):(v['key'][1],v['key'][2]) for v in inventory['owners']};rows=r.read_csv(w.OUT/'CANDIDATE_CELLS.csv')
    check('Every candidate resolves to actual RGB State_ID owner',all(int(v['Current_RGB'][1:],16)==int(bmp[int(v['Y']),int(v['X'])]) and lookup[int(v['Current_RGB'][1:],16)]==(v['State_ID'],v['Current_owner']) for v in rows))
    check('No invented RGBs / no unappproved A / no applied candidates',all(not v['Proposed_RGB'] and v['Class']!='A' and v['Applied']=='False' for v in rows))
    check('Candidates exclude Thorn',all(v['Current_RGB']!='x41A021' for v in rows))
    check('No duplicated candidate coordinates',len({(v['X'],v['Y']) for v in rows})==len(rows))
    check('Empty territorial changes ledger has zero transfers',len(r.read_csv(w.OUT/'TERRITORIAL_CHANGES.csv'))==0)
    for name in ['REPORT.md','NATIVE_PROJECTION_REVIEW.md','CONTROL_POINTS.csv','INDEPENDENT_VALIDATION.csv','TRANSFORMATIONS.json','PFAU_RECALIBRATION.md','PEENE_RECALIBRATION.md','BORDER_RECONSTRUCTION.csv','CANDIDATE_CELLS.csv','TERRITORIAL_CHANGES.csv','PEENE_BEFORE_AFTER.png','NETZE_BEFORE_AFTER.png','UNRESOLVED.csv','NEXT_STEPS.md']:
        check('Deliverable '+name,(w.OUT/name).is_file())
    for name,model in w.load('TRANSFORMATIONS.json')['tested_native'].items():
        check(name+' FIT and CHECK disjoint',not set(model['fit_ids'])&set(model['check_ids']))
        mm=dict(model,name=name);geo=np.array([[13.7,53.9],[18.2,53.1],[16.4,53.3]])
        check(name+' forward inverse roundtrip',np.allclose(r.inverse(mm,r.forward(mm,geo)),geo,atol=1e-10))
    geo=np.array([[10,50],[11,51],[12,49],[13,52]],float);truth=np.array([[23,0],[0,-32],[4000,2400]],float);pix=w.old.apply(geo,truth)
    check('Synthetic axes fit recovery',np.allclose(r.fit_axes(geo,pix,'geographic_axes'),truth,atol=1e-9))
    audit=w.load('PFAU_FRAME_AUDIT.json');check('Pfau global-frame invariance audit',max(v['max_change_vs_first_frame_m'] for v in audit['variants'])<1e-6)
    check('Revised Usedom excluded from pristine statistics',w.load('TRANSFORMATIONS.json')['selected_native']['pristine_holdout_count']==4)
    cli_env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    def query(*args):
        return subprocess.run([sys.executable,'-X','utf8',str(w.OUT/'query.py'),*args],capture_output=True,text=True,encoding='utf-8',env=cli_env,timeout=30)
    inside=query('geo','13.692','53.856')
    check('CLI forward inside support',inside.returncode==0 and not json.loads(inside.stdout)['outside_fit_support'])
    inverse=query('pixel','4408.2025405246095','741.1243418316328')
    check('CLI inverse recovery',inverse.returncode==0 and np.allclose(json.loads(inverse.stdout)['estimate'],[13.692,53.856],atol=1e-9))
    outside=query('geo','11.0328','50.9787')
    check('CLI refuses Erfurt extrapolation by default',outside.returncode!=0 and 'Outside fitted convex-hull support' in outside.stderr)
    diagnostic=query('geo','11.0328','50.9787','--allow-extrapolation')
    check('CLI explicit extrapolation is labelled',diagnostic.returncode==0 and json.loads(diagnostic.stdout)['outside_fit_support'])
    invalid=query('geo','nan','53')
    check('CLI refuses nonfinite geographic input',invalid.returncode!=0 and 'Invalid geographic range' in invalid.stderr)
    for name in ['work.py','review.py','finish.py','query.py']:
        compile((w.OUT/name).read_text(encoding='utf-8'),name,'exec');check('Python syntax '+name,True)
    totals=dict(collections.Counter(v['Class'] for v in rows));model=w.load('TRANSFORMATIONS.json')['selected_native']
    result=dict(status='MAP_2M_R5_PARTIAL',static_integrity_status='PASS' if all(v['passed'] for v in tests) else 'FAIL',tests=tests,passed=sum(v['passed'] for v in tests),total=len(tests),
        functional_file_count=len(current),functional_changes=[],territorial_transfers=0,candidate_classes=totals,global_population=835804980,
        inherited=dict(duplicate_RGB_count=44,invalid_reference_count=12,details=inventory['errors']),
        independent_native=dict(count=4,mean_px=model['pristine_holdout_mean_px'],max_px=model['pristine_holdout_max_px'],revised_check_not_in_statistics='USEDOM',model_selection_used_these_checks=True,new_final_external_test=False),
        R3_runtime_status='PASS_RUNTIME_USER_VALIDATED',R5_runtime_test=False,automated_engine_test=False,
        colgrep=dict(invocations=2,first_result='Index lock denied in sandbox',second_result='Successful local agent search, exit0, returned paths and line ranges manually verified',
            successful_agent_searches=1,model_integration_changed=False,GPU_or_model_telemetry_captured=False,exact_tokens_or_savings=None),
        source_documents_reused_without_acquisition=True)
    w.dump('VALIDATION.json',result)
    w.dump('MANIFEST.json',{p.relative_to(w.OUT).as_posix():dict(sha256=w.sha(p),bytes=p.stat().st_size) for p in w.OUT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'})
    print(result['static_integrity_status'],result['passed'],'/',result['total'],'; R5 PARTIAL; no runtime changes')
    if not all(v['passed'] for v in tests):raise SystemExit('Validation failure')

if __name__=='__main__':{'images':images,'anklam_chain':anklam_chain,'unresolved':unresolved,'validate':validate}[sys.argv[1]]()
