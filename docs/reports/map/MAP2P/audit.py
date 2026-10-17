"""Read-only MAP2P investigation. All generated files remain beside this script."""
from pathlib import Path
import sys,json,csv,math,hashlib,subprocess,collections as C
import urllib.request
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'tools'))
import map2o_east_frisia as previous
import numpy as np
from PIL import Image,ImageDraw,ImageFont
core=previous.core;OUT=Path(__file__).resolve().parent
BOX=(4236,739,4294,775)
SOUTH='x784B8E';WEST='xC0C021';EAST=['xECC3B4','xC00161']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def old_report_metadata():
    return {p.relative_to(ROOT).as_posix():[p.stat().st_size,p.stat().st_mtime_ns] for p in (ROOT/'docs/reports/map').rglob('*') if p.is_file() and OUT not in p.parents}

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Do not replace original audit reference'
    inv=core.qa.inventory();hashes=previous.economy.runtime_hashes()
    manifest=previous.load('INSTALLED_MANIFEST.json')
    assert all(hashes.get(p)==h for p,h in manifest['functional_files'].items())
    assert sha(core.active_registry_path())==manifest['imperial_registry_sha256']
    dump('BASELINE.json',dict(inventory=inv,runtime_hashes=hashes,old_report_metadata=old_report_metadata(),
        registry_sha256=sha(core.active_registry_path()),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=sha(ROOT/'.git/index'),
        historical_date='1776-01-01',date='2026-10-16'))
    dump('MAP2O_RUNTIME_USER_VALIDATION.json',dict(lot='MAP2O',status='PASS_RUNTIME_USER_VALIDATED',date_recorded='2026-10-16',
        method='Manual user confirmation in supplied MAP2P instruction',source='C:/Users/simeo/.codex/attachments/4753fc32-5d1b-4872-bd52-c2c0af654f06/Texte collé.txt',
        user_statement='Validation manuelle en jeu confirmée par le joueur.',coverage='MAP2O accepted as described by user; individual checklist items not supplied',
        duration='Not provided; no one-month simulation inferred',automated_engine_test=False,engine_logs_provided=False,historical_boundary_certification=False,
        prior_proofs_rewritten=False,new_MAP2P_territorial_changes_authorized=False))
    print('Reference captured; MAP2O receipt recorded here only. No game/history/registry writes.')

def inventory():
    b=load('BASELINE.json');bmp=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    rows=[];cells=[];x0,y0,x1,y1=BOX
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf-8'));rights={r['rgb']:r['beneficiary'] for r in ledger}
    for color in np.unique(bmp[y0:y1,x0:x1]):
        rgb='x'+format(int(color),'06X');who=owners.get(rgb)
        if not who:continue
        yy,xx=np.where(bmp==color);mask=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)
        neighbors=C.Counter()
        for y,x in zip(yy[mask],xx[mask]):
            for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                c=int(bmp[y+dy,x+dx])
                if c!=color:neighbors['x'+format(c,'06X')]+=1
            if rgb=='xF9DCA2':
                sector=('NORTH_COAST' if y<=749 else 'CENTRAL_INTERIOR' if y<=756 else 'SOUTHERN_FRINGE')
                cells.append(dict(X=int(x),Y=int(y),RGB=rgb,Owner_TAG=who[1],State_ID=who[0],Sector=sector,
                    Historical_geometry='B_MACRO_ONLY; no certified town containment',Proposed_change='NONE'))
        rows.append(dict(RGB=rgb,State_ID=who[0],Owner_TAG=who[1],Total_cells=len(xx),Cells_in_audit_box=int(mask.sum()),X_min=int(xx.min()),X_max=int(xx.max()),Y_min=int(yy.min()),Y_max=int(yy.max()),
            Registered_holder=rights.get(rgb,''),Adjacent_RGBs=';'.join(sorted(neighbors)),Proposed_installed_changes=0))
    csvout('CURRENT_TERRITORIES.csv',rows);csvout('MAP2O_319_CELL_AUDIT.csv',cells)
    dump('COASTAL_SUBSECTORS.json',dict(counts=dict(C.Counter(r['Sector'] for r in cells)),
        segmentation='Raster review bands, NOT historical boundaries',cells=sum(1 for r in cells),
        physical_land_water_checked=False))
    previous.panel(bmp,owners,BOX,'MAP2P : situation installee ; aucune correction appliquee',scale=18).save(OUT/'CURRENT_BORDER_MAP.png')
    print('Inventoried',len(rows),'RGB envelopes;',len(cells),'accepted PRU cells')

def source():
    url='https://upload.wikimedia.org/wikipedia/commons/9/98/Coldewey-Ostfriesland-1730.png'
    target=OUT/'COLDEWEY_1730.png';assert not target.exists()
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HistoricalMapResearch/1.0'}),timeout=30) as r:
        data=r.read(20_000_001);assert len(data)<20_000_000
    target.write_bytes(data)
    dump('COLDEWEY_SOURCE.json',dict(url=url,primary_map='Coldewey/Homann1730',sha256=sha(target),
        reproduction_host='Wikimedia Commons',institutional_commentary='LGLN Ostfrieslandkarte_1730; Schlossmuseum Jever Ka225b',
        license_note='Historical engraving; original author died1773; inspect image independently of Commons metadata',date_accessed='2026-10-16'))
    print('Saved one targeted historical source',len(data))

def proposals():
    b=load('BASELINE.json');bmp=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    # These are exact carrier envelopes to investigate, NOT source-derived
    # historical polygons. In particular no row authorizes their wholesale transfer.
    bands=[('C_SOUTH',SOUTH,'Leer/southern interface'),('C_WEST',WEST,'Rheiderland/Dollard interface'),
           ('C_EAST_NORTH',EAST[0],'Wittmund/Jever interface'),('C_EAST_SOUTH',EAST[1],'Friedeburg/Oldenburg/Varel interface'),
           ('C_FAR_SOUTH','x8080E0','Southern limit exclusion check')]
    candidates=[];summary=[]
    for ident,rgb,sector in bands:
        yy,xx=np.where(bmp==int(rgb[1:],16));sid,tag=owners[rgb]
        for y,x in zip(yy,xx):candidates.append(dict(Candidate_ID=ident,X=int(x),Y=int(y),RGB=rgb,State_ID=sid,Owner_current=tag,Owner_proposed='',Class='C',Action='DO_NOT_APPLY',Meaning='Carrier envelope only; wrong-cell subset undetermined'))
        summary.append(dict(ID=ident,Sector=sector,Historical_sovereignty='PRU inside East Frisian jurisdiction; neighboring jurisdiction excluded',Owner_current=tag,State_ID=sid,RGB=rgb,
            Carrier_cells=len(xx),Confirmed_wrong_cells='',Wrong_cells_lower_bound=0,Wrong_cells_upper_bound=len(xx),Class='C',Source_IDs='S1;S3;S4',
            Proposed_correction='SUBDIVIDE_ONLY_AFTER_SOURCE_MATCH; no whole-province transfer',Installed=False))
    # Southern part of accepted province gets a separate review band. It is not
    # inferred to belong to HAN or OLD merely because it lies at a raster edge.
    yy,xx=np.where(bmp==int(previous.PARENT[1:],16));keep=yy>=757;yy,xx=yy[keep],xx[keep]
    for y,x in zip(yy,xx):candidates.append(dict(Candidate_ID='C_ACCEPTED_SOUTH_EDGE',X=int(x),Y=int(y),RGB=previous.PARENT,State_ID=previous.REGION,Owner_current='PRU',Owner_proposed='',Class='C',Action='DO_NOT_APPLY',Meaning='Accepted southern review band; not a historical boundary or confirmed foreign land'))
    summary.append(dict(ID='C_ACCEPTED_SOUTH_EDGE',Sector='Possible absorbed neighboring land; not demonstrated',Historical_sovereignty='Unassigned at individual-cell level',Owner_current='PRU',State_ID=previous.REGION,RGB=previous.PARENT,
        Carrier_cells=len(xx),Confirmed_wrong_cells='',Wrong_cells_lower_bound=0,Wrong_cells_upper_bound=len(xx),Class='C',Source_IDs='S3;S4',
        Proposed_correction='KEEP_ACCEPTED_MAP2O; no reverse transfer justified',Installed=False))
    csvout('BORDER_ANOMALIES.csv',summary);csvout('CANDIDATE_CELLS_NOT_AUTHORIZED.csv',candidates)
    csvout('PROPOSED_CHANGES.csv',[],['Proposal_ID','X','Y','RGB_current','RGB_proposed','State_ID','Owner_current','Owner_proposed','Class','Source_IDs','Installed'])
    dump('DECISIONS.json',dict(new_transfer_proposals_A=0,new_transfer_proposals_B=0,proposed_transfer_cells=0,proposed_new_RGBs=0,
        accepted_core_retained_cells=319,accepted_core_class='B',candidate_envelope_cells=len(candidates),confirmed_foreign_cells_absorbed=None,
        confirmed_Prussian_cells_still_wrong=None,candidate_envelopes_are_not_union_of_wrong_cells=True,
        research_stop='One new decisive regional engraving inspected; native-source homologous boundary remains missing. No further generalized recalibration or source campaign justified in this audit.'))
    local=Image.open(OUT/'COLDEWEY_1730.png')
    local.crop((265,625,980,1130)).resize((1430,1010),Image.Resampling.NEAREST).save(OUT/'COLDEWEY_SOUTH_DETAIL.png')
    panels=[previous.panel(bmp,owners,BOX,'ACTUEL : MAP2O accepte, noyau cotier PRU (B)',scale=18),
            previous.panel(bmp,owners,BOX,'PROPOSITION : conserver ; zones C a delimiter, NON a transferer',scale=18,labels=False)]
    d=ImageDraw.Draw(panels[1]);x0,y0,x1,y1=BOX;font=ImageFont.truetype(previous.FONT,14)
    local=bmp[y0:y1,x0:x1];candidate_colors={int(r[1][1:],16) for r in bands}
    for y in range(y0,y1):
        for x in range(x0,x1):
            color=int(bmp[y,x]);accepted=color==int(previous.PARENT[1:],16)
            if color in candidate_colors or (accepted and y>=757):
                px,py=(x-x0)*18,(y-y0)*18+40
                d.line((px,py+17,px+17,py),fill='#bb236c',width=2)
            elif accepted:
                px,py=(x-x0)*18,(y-y0)*18+40;d.rectangle((px+6,py+6,px+11,py+11),fill='#19724a')
    width=panels[0].width;height=panels[0].height
    canvas=Image.new('RGB',(width*2,height+108),'white')
    for i,p in enumerate(panels):canvas.paste(p,(i*width,0))
    d=ImageDraw.Draw(canvas)
    notes=['Couleurs = proprietaires actuels. Points verts = maintien du noyau B, pas une limite historique certifiee.',
        'Hachures roses = enveloppes C examinees ; aucune attribution nouvelle proposee. La bande sud PRU n\'est pas une annexion etablie.',
        '0 cellule de transfert A/B prete ; 0 nouveau RGB. Carte d\'arbitrage, NON un nouveau trace de frontiere.']
    for i,note in enumerate(notes):d.text((9,height+8+i*30),note,font=ImageFont.truetype(previous.FONT,18),fill='#242424')
    canvas.save(OUT/'PROPOSED_BORDER_MAP.png')
    print('Prepared0 executable transfers;',len(candidates),'carrier cells explicitly C/not authorized')

def physical_diagnostic():
    heights=Image.open(ROOT/'map_data/heightmap.png');provinces=Image.open(ROOT/'map_data/provinces.png');rivers=Image.open(ROOT/'map_data/rivers.png')
    sx,sy=heights.width/provinces.width,heights.height/provinces.height
    assert (sx,sy)==(2,2) and rivers.size==provinces.size
    values=np.asarray(heights.crop(tuple(int(v*2) for v in BOX)),dtype=float)
    low,high=np.percentile(values,[1,99]);gray=np.clip((values-low)*255/max(high-low,1),0,255).astype(np.uint8)
    base=Image.fromarray(gray).convert('RGB').resize(((BOX[2]-BOX[0])*18,(BOX[3]-BOX[1])*18),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(base.width,base.height+90),'white');canvas.paste(base,(0,35));d=ImageDraw.Draw(canvas)
    d.text((8,8),'RELIEF : recadrage multiplie par2 ; contraste local, pas une frontiere politique',font=ImageFont.truetype(previous.FONT,16),fill='black')
    d.text((8,base.height+47),'Coordonnees provinces : '+str(BOX)+' | aucune ville geolocalisee par ce contraste.',font=ImageFont.truetype(previous.FONT,15),fill='black')
    canvas.save(OUT/'ALIGNED_HEIGHTMAP_DIAGNOSTIC.png')
    dump('PHYSICAL_LAYER_DIAGNOSTIC.json',dict(provinces_dimensions=provinces.size,heightmap_dimensions=heights.size,rivers_dimensions=rivers.size,
        raster_scale=[sx,sy],province_crop=BOX,heightmap_crop=[v*2 for v in BOX],contrast_percentiles=[1,99],contrast_values=[float(low),float(high)],
        prior_MAP2O_crop_method='Same unscaled BOX for heightmap and provinces',prior_crop_geometrically_aligned=False,
        changes_to_native_data=False,certified_city_locations=False,certified_historical_boundary=False,
        interpretation='Correct image-index scaling only. No geographic projection fit or political boundary inferred.'))
    print('Heightmap diagnostic corrected locally; no runtime data changed')

def validate():
    b=load('BASELINE.json');current=previous.economy.runtime_hashes();checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    check('All runtime files byte-exact and no additions/deletions',current==b['runtime_hashes'])
    check('All old report files retain original size and modification time',old_report_metadata()==b['old_report_metadata'])
    check('Active imperial registry byte-exact',sha(core.active_registry_path())==b['registry_sha256'])
    check('Git HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index byte-exact',sha(ROOT/'.git/index')==b['git_index_sha256'])
    for rel,digest in previous.load('BASELINE.json')['bridge_and_prototype_hashes'].items():
        check('Bridge/prototype source retained '+rel,sha(ROOT/rel)==digest)
    inv=b['inventory'];check('Inherited anomalies unchanged',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('Preserved world population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    with (OUT/'MAP2O_319_CELL_AUDIT.csv').open(encoding='utf-8-sig') as f:cells=list(csv.DictReader(f))
    check('Every accepted cell individually listed once',len(cells)==len({(r['X'],r['Y']) for r in cells})==319)
    check('All accepted cells remain PRU/Hannover',all((r['RGB'],r['Owner_TAG'],r['State_ID'])==(previous.PARENT,'PRU',previous.REGION) for r in cells))
    # Full bitmap preservation is already proven by file hashes; reconstruct
    # the accepted footprint once, avoiding 319 repeated whole-world decodes.
    bmp=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(bmp==int(previous.PARENT[1:],16))
    check('Accepted319 cell footprint exact',{(int(r['X']),int(r['Y'])) for r in cells}=={(int(x),int(y)) for y,x in zip(yy,xx)})
    with (OUT/'PROPOSED_CHANGES.csv').open(encoding='utf-8-sig') as f:proposals=list(csv.DictReader(f))
    check('No unsupported A/B transfer or invented RGB',len(proposals)==0)
    with (OUT/'CANDIDATE_CELLS_NOT_AUTHORIZED.csv').open(encoding='utf-8-sig') as f:candidates=list(csv.DictReader(f))
    check('Every C candidate explicitly non-executable',len(candidates)==1240 and all(r['Class']=='C' and r['Action']=='DO_NOT_APPLY' and not r['Owner_proposed'] for r in candidates))
    check('All candidate RGB/state/owner claims match inventory',all([r['RGB'],r['State_ID'],r['Owner_current']] in [v['key'] for v in inv['owners']] for r in candidates))
    check('Each candidate footprint is on its named RGB',all(int(bmp[int(r['Y']),int(r['X'])])==int(r['RGB'][1:],16) for r in candidates))
    physical=load('PHYSICAL_LAYER_DIAGNOSTIC.json')
    check('Native raster scaling explicitly2x not same-index crop',physical['provinces_dimensions']==[8192,3616] and physical['heightmap_dimensions']==[16384,7232] and physical['raster_scale']==[2,2] and physical['heightmap_crop']==[v*2 for v in BOX])
    check('Corrected diagnostic does not pretend to validate a political boundary',not physical['prior_crop_geometrically_aligned'] and not physical['certified_city_locations'] and not physical['certified_historical_boundary'] and not physical['changes_to_native_data'])
    receipt=load('MAP2O_RUNTIME_USER_VALIDATION.json')
    check('Manual receipt additive and no invented engine test',receipt['status']=='PASS_RUNTIME_USER_VALIDATED' and not receipt['automated_engine_test'] and not receipt['engine_logs_provided'] and receipt['duration'].startswith('Not provided'))
    required=['REPORT.md','EAST_FRISIA_1776_AUDIT.md','CURRENT_TERRITORIES.csv','BORDER_ANOMALIES.csv','PROPOSED_CHANGES.csv','PROPOSED_BORDER_MAP.png','SOURCE_REGISTER.md','UNRESOLVED.csv','IMPLEMENTATION_PLAN.md','NEXT_REGION_RECOMMENDATION.md']
    check('All requested deliverables present',all((OUT/p).is_file() for p in required))
    for name in ['PROPOSED_BORDER_MAP.png','COLDEWEY_1730.png']:
        im=Image.open(OUT/name);im.verify();check('Readable image '+name,True)
    dump('VALIDATION.json',dict(status='PASS_AUDIT_NO_RUNTIME_MUTATION' if all(r['passed'] for r in checks) else 'FAIL',date='2026-10-16',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,
        runtime_files_checked=len(current),runtime_files_modified=[],old_reports_rewritten=False,proposed_transfer_cells=0,candidate_cells_not_authorized=1240,
        MAP2O_runtime_status='PASS_RUNTIME_USER_VALIDATED',MAP2P_engine_test=False,historical_border_certified=False,colgrep_calls=0,
        colgrep_reason='Required input paths already supplied; no exploratory code localization needed. AGENTS rule3 avoids redundant semantic invocation.',
        source_map_sha256=sha(OUT/'COLDEWEY_1730.png')))
    print('Validation',sum(r['passed'] for r in checks),'/',len(checks))
    for r in checks:
        if not r['passed']:print('FAIL',r['name'])
    assert all(r['passed'] for r in checks)

if __name__=='__main__':{'capture':capture,'inventory':inventory,'source':source,'proposals':proposals,'validate':validate,'physical':physical_diagnostic}[sys.argv[1]]()
