"""R7 proposals only. No function in this module writes runtime files."""
import sys,json,csv,hashlib,math,collections
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent/'R6'))
import pilot as p
w=p.w;r=p.r;ROOT=p.ROOT

def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        out=csv.DictWriter(f,fieldnames=fields or list(rows[0]));out.writeheader();out.writerows(rows)

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Never replace an earlier baseline.'
    current=w.prior.economy.runtime_hashes();ref=p.load('BASELINE.json')
    assert current==ref['runtime_hashes'],'Changed runtime reference: inspect, do not restore.'
    previous={q.relative_to(ROOT).as_posix():w.sha(q) for n in ['R1','R2','R3','R4','R5','R6'] for q in (OUT.parent/n).rglob('*') if q.is_file()}
    dump('BASELINE.json',dict(runtime_hashes=current,prior_hashes=previous,git_head=w.prior.r3.r2.head(),git_index_sha256=w.sha(ROOT/'.git/index'),
        inventory_sha256=ref['inventory_sha256'],bitmap_sha256=w.sha(ROOT/'map_data/provinces.png')))
    dump('OPTION_RULES.json',dict(status='PROPOSAL_ONLY_NOT_APPROVED',decision_category_for_both_options='B',
        local_window_half_open=[4404,732,4412,740],source_RGB='xE1A03A',target_RGB_if_later_approved='x567452',
        political_source='Mayer1763 Swedish mainland west of Peenestrom; not modern water alone',
        drawing_support='Current LUNG kg.52 western water edge, projected with all four frozen R5 native models; this is a drawing aid, not the exact1776 bank',
        variant_A='Inherited18, all inherited polygon variants agree; one cell-layer adjacent to existing SWE; right edge remains3.19px west of every frozen native bank variant.',
        variant_B='Parent PRU land cells in local window; entire cell west of every projected bank; retain only 4-connected proposed components touching existing SWE.',
        protected='All rows>=740 (Anklam/Peendamm approach); all cells outside window; no point-based Peendamm enclave; no Usedom/Wollin east of channel; no Demmin extension.',
        thresholds_are_not_confidence_intervals=True,new_projection_fit=False,third_variant='Not useful: changing RGB province definitions cannot create subpixel space. No resolution overhaul.'))
    print(len(current),'runtime files protected;',len(previous),'prior artifact hashes.')

def west_bank():
    fs=json.loads((OUT.parent/'R3/EVIDENCE/LUNG_PEENESTROM_WATER.geojson').read_text())['features'];feature=next(f for f in fs if f['id']=='kg.52');points=[]
    for lat in np.linspace(54.165,53.88,1500):
        intervals=[]
        for poly in feature['geometry']['coordinates']:
            intersections=[]
            for ring in poly:
                for a,b in zip(ring[:-1],ring[1:]):
                    if (a[1]<=lat<b[1]) or (b[1]<=lat<a[1]):intersections.append(a[0]+(lat-a[1])*(b[0]-a[0])/(b[1]-a[1]))
            intersections.sort()
            intervals.extend((a,b) for a,b in zip(intersections[0::2],intersections[1::2]) if 13.69<a<b<13.95)
        if intervals:points.append([min(v[0] for v in intervals),float(lat)])
    return np.array(points)

def connected_to_existing(cells,existing):
    todo=set(cells);keep=set()
    while todo:
        component={todo.pop()};queue=list(component)
        for x,y in queue:
            for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if n in todo:todo.remove(n);component.add(n);queue.append(n)
        if any(n in existing for x,y in component for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):keep|=component
    return keep

def options():
    rules=load('OPTION_RULES.json');bmp,water,river,_=p.physical_masks();geo=west_bank();models=w.load('TRANSFORMATIONS.json')['tested_native'];curves={name:r.forward(dict(mm,name=name),geo) for name,mm in models.items()}
    bankrows=[];bank_at={}
    for y in range(732,740):
        samples=[]
        for name,curve in curves.items():
            hits=[]
            for a,b in zip(curve[:-1],curve[1:]):
                if (a[1]<=y+.5<b[1]) or (b[1]<=y+.5<a[1]):hits.append(float(a[0]+(y+.5-a[1])*(b[0]-a[0])/(b[1]-a[1])))
            assert hits,(name,y,'No extrapolated line replacement permitted')
            samples.append(min(hits))
        bank_at[y]=(min(samples),max(samples));bankrows.append(dict(Y=y,Bank_X_min=min(samples),Bank_X_max=max(samples),Model_values=json.dumps(dict(zip(curves,samples))),Status='MODERN_DRAWING_SUPPORT_NOT_HISTORICAL_ERROR_BOUND'))
    csvout('PEENE_BANK_ENVELOPE.csv',bankrows)
    existing={(x,y) for y in range(728,744) for x in range(4398,4418) if bmp[y,x]==0x567452}
    inherited={tuple([int(v['X']),int(v['Y'])]):v for v in r.read_csv(OUT.parent/'R6/CANDIDATE_DECISIONS.csv') if v['Pilot']=='A'}
    a=set();b=set()
    for y in range(732,740):
        for x in range(4404,4412):
            if bmp[y,x]!=0xE1A03A or water[y,x]:continue
            west=bank_at[y][0]-(x+1)
            if west>=0:b.add((x,y))
            old=inherited.get((x,y))
            if old and all(json.loads(old['Variant_membership_R5'])) and west>=3.19 and any(n in existing for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):a.add((x,y))
    a=connected_to_existing(a,existing);b=connected_to_existing(b,existing)
    assert a and b and a<b,'Need two useful nested options, never invent cells to hit a count.'
    rows=[];summaries={};frontiers=[]
    for variant,cells in [('A',a),('B',b)]:
        area=0
        for x,y in sorted(cells,key=lambda q:(q[1],q[0])):
            ll=r.inverse(w.load('TRANSFORMATIONS.json')['selected_native'],[[x+.5,y+.5]])[0];m=w.load('TRANSFORMATIONS.json')['selected_native']['matrix'];area_cell=111.31949079327358**2*math.cos(math.radians(ll[1]))/(m[0][0]*abs(m[1][1]));area+=area_cell
            rows.append(dict(Variant=variant,Decision_category='B',X=x,Y=y,State_ID='STATE_POMERANIA',RGB_before='xE1A03A',RGB_proposed='x567452',Owner_before='PRU',Owner_proposed='SWE',
                Historical_basis='Swedish mainland west of Peenestrom, Mayer1763; cell geometry deliberately generalized',Historical_bank_certified=False,
                Drawing_bank_X_min=bank_at[y][0],Drawing_bank_X_max=bank_at[y][1],Right_edge_setback_min_px=bank_at[y][0]-(x+1),Approx_cell_km2=area_cell,
                Inside_frozen_R5_support=r.in_support(w.load('TRANSFORMATIONS.json')['selected_native'],ll),
                Prior_status='R6_MAINLAND_B' if (x,y) in inherited else 'NEW_R7_GENERALIZATION_CELL_NOT_IMPORT_OF_C',
                Approval='PENDING_PLAYER',Applied=False))
        values=[v for v in rows if v['Variant']==variant]
        summaries[variant]=dict(proposed_cells=len(cells),approx_added_land_km2=area,prospective_SWE_RGB_cell_count=357+len(cells),
            bbox_inclusive=[min(x for x,y in cells),min(y for x,y in cells),max(x for x,y in cells),max(y for x,y in cells)],
            right_edge_setback_min_px=min(v['Right_edge_setback_min_px'] for v in values),right_edge_setback_max_px=max(v['Right_edge_setback_min_px'] for v in values),
            includes_Wolgast_diagnostic_cell=(4410,735) in cells,extra_vs_A=len(cells-a),new_R7_cells_not_inherited18=len(cells-set(inherited)),
            exact_historical_added_area_km2=None,area_distortion_ratio=None,status='PROPOSED_NOT_INSTALLED',category='B',approval='PENDING_PLAYER')
        for y in sorted({y for x,y in cells}):
            edge=max(x for x,yy in cells if yy==y)+1
            frontiers.append(dict(Variant=variant,Y=y,Proposed_east_edge_X=edge,Distance_to_bank_envelope_west_px=bank_at[y][0]-edge,Distance_to_bank_envelope_east_px=bank_at[y][1]-edge,
                Meaning='Horizontal setback of newly proposed frontier from modern projected drawing support; NOT historical error.'))
        values=[v for v in frontiers if v['Variant']==variant]
        summaries[variant]['new_frontier_setback_min_px']=min(v['Distance_to_bank_envelope_west_px'] for v in values)
        summaries[variant]['new_frontier_setback_max_all_models_px']=max(v['Distance_to_bank_envelope_east_px'] for v in values)
    csvout('PEENE_PROPOSED_CELLS.csv',rows)
    csvout('PEENE_FRONTIER_DEFORMATION.csv',frontiers)
    dump('PEENE_DRAWING_SUPPORT.json',dict(geo_west_bank=geo.tolist(),native_curves={name:v.tolist() for name,v in curves.items()},warning='Modern waterline drawing support, not a georeferenced historical political boundary.'))
    dump('PEENE_OPTION_SUMMARY.json',summaries);print(json.dumps(summaries,indent=2))

def source_views():
    specs=[
      ('GUESSEFELD_SOUTH_READING.png','docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg',(1050,2300,1510,2580),3,20),
      ('MANUSCRIPT_EAST_SOUTH_READING.png','docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL2_FULL.jpg',(4000,5800,7200,8650),.65,400),
      ('MANUSCRIPT_WEST_OVERLAP_READING.png','docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL1_FULL.jpg',(9700,5500,13000,9000),.6,400),
      ('GUESSEFELD_CARTOUCHE_DATE.png','docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg',(1530,470,1850,620),4,100),
      ('GUESSEFELD_PREFACE_READING.png','docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg',(1150,200,2030,1730),1,200)]
    frames=[]
    for name,path,box,scale,step in specs:
        im=Image.open(ROOT/path).convert('RGB').crop(box).resize((int((box[2]-box[0])*scale),int((box[3]-box[1])*scale)));d=ImageDraw.Draw(im)
        for x in range((box[0]//step+1)*step,box[2],step):d.line(((x-box[0])*scale,0,(x-box[0])*scale,im.height),fill='#b05555');d.text(((x-box[0])*scale+1,2),str(x),fill='red',font=w.font(14))
        for y in range((box[1]//step+1)*step,box[3],step):d.line((0,(y-box[1])*scale,im.width,(y-box[1])*scale),fill='#b05555');d.text((2,(y-box[1])*scale+1),str(y),fill='red',font=w.font(14))
        im.save(OUT/name);frames.append(dict(file=name,source=path,bbox=box,scale=scale,sha256=w.sha(ROOT/path),warning='Source coordinates, no geographic registration. Two manuscript views are one document.'))
    dump('SOURCE_READING_FRAMES.json',frames)

def evidence():
    rows=[
      ('G1775_SOUTH','Guessefeld/Homann retained1775','docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg','R6 southern trace1190,2367 to1530,2419','Red/yellow rim continuous south of Bromberg, matching regional-colour conventions also used elsewhere','A coloured border alone has no certified sovereign meaning; inherited plate/exemplar dating does not date every represented line','1775 attributed to map family; geographic state of this sector not proven Jan1776','C','No conversion or transfer'),
      ('G1775_SZUBIN','Guessefeld/Homann retained1775','docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg','Schubin symbol approx1193,2443, reading radius6sourcepx','Schubin lies south of the interpreted rim, in the side labelled Poland','Official Szubin history reports Prussian incorporation1773: conflict with interpreting whole rim as sovereign Jan1776 line','Municipal1773 is historical context, not a georeferenced1773 boundary deed','C','Reject unqualified use of entire line; some subsegments may still be valid but not identified'),
      ('N1146_EAST','SBB N1146/1 east recto','docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL2_FULL.jpg','Szubin symbol approx4800,6895; Labiszyn near6320,7600','Coloured acquired strip leaves Szubin on its southwest side; private red names also present','Catalogue[1772] draft may precede1773 incorporation; same apparent line does not independently validate1776','[1772] catalogue date; additions not individually dated; exact purpose unresolved','C','Do not read private names as sovereignty'),
      ('N1146_WEST','SBB N1146/1 west recto','docs/reports/map/MAP2M/R4/EVIDENCE/BOUNDARY_1772_PANEL1_FULL.jpg','Eastern overlap near source x9700..13000,y5500..9000','Overlap belongs to same document, not independent geographical or political confirmation','Private ownership note and frame text do not establish legal1776 continuity','Same catalogue[1772] object','C','No automatic source mosaic'),
      ('RECTIFICATIONS','Retained R4 archival metadata','docs/reports/map/MAP2M/R4/SOURCES.json','retained_catalogue_note near end','Tit50 Nr1a1772 boards; Nr11776 Thorn posts; Nr21777 regulation','No original acts examined; catalogue dates do not establish effectiveness by Jan1 1776; Thorn excluded','1776/1777 metadata only; no substitution of1777 state','C','Need dated line/act for this segment, not another same-point fit'),
      ('R6_VISTULA','R6 corrected diagnostic','docs/reports/map/MAP2M/R6/FINAL_HOLDOUT_CHECKS.csv','B_VISTULA_WEST_APEX','Frozen model residual0.6794px to midpoint of five tied native cells; reading ambiguity2.5px','One physical bend cannot certify southern political boundary or its date','Modern river drawing, not sovereign1776 geometry','C','Reuse width indices3..15; do not fit a political line on this point alone')]
    out=[]
    for ident,source,path,location,observation,limitation,date,category,decision in rows:
        out.append(dict(ID=ident,Source=source,Path=path,SHA256=w.sha(ROOT/path),Source_location=location,Observation=observation,Limitation=limitation,Dating=date,Decision_category=category,Decision=decision,Native_segment_accepted=False,Applied=False))
    out.append(dict(ID='SZUBIN_1773',Source='Municipality of Szubin, Historia Gminy',Path='https://szubin.pl/historia-gminy.html',SHA256='',Source_location='History paragraph on1773',
        Observation='Municipal history dates incorporation into Prussian partition to1773',Limitation='Institutional historical summary, not contemporary boundary instrument; no sovereignty extrapolated to whole province',Dating='1773 before Jan1776',Decision_category='C',Decision='Countercheck of rim interpretation, no new pixel assignment',Native_segment_accepted=False,Applied=False))
    csvout('BROMBERG_BORDER_EVIDENCE.csv',out)
    controls=[]
    for v in r.read_csv(OUT.parent/'R6/FINAL_HOLDOUT_CHECKS.csv'):
        controls.append(dict(ID=v['ID'],Origin='R6 retained final check',New_R7=False,Used_for_fit=False,Used_for_model_selection=False,Longitude=v['Longitude'],Latitude=v['Latitude'],Native_X=v['Native_X'],Native_Y=v['Native_Y'],Residual_px=v['Residual_px'],Status=v['Status'],Reading_ambiguity_px=v.get('Observed_plateau_radius_px',''),Use='Retained diagnostic only; no new controls sought because missing evidence is political/date, not a fit residual.'))
    csvout('CONTROL_POINTS.csv',controls)
    decisions=[]
    for v in r.read_csv(OUT/'PEENE_PROPOSED_CELLS.csv'):
        decisions.append(dict(Sector='PEENE',Variant=v['Variant'],X=v['X'],Y=v['Y'],RGB=v['RGB_before'],State_ID=v['State_ID'],Owner_before=v['Owner_before'],Owner_proposed=v['Owner_proposed'],Decision_category='B',
            Basis='Historically Swedish mainland; explicitly proposed raster generalization, NOT a new geometrically certified cell',Approval='PENDING_PLAYER',Applied=False))
    for v in r.read_csv(OUT.parent/'R6/CANDIDATE_DECISIONS.csv'):
        if v['Pilot']=='B':decisions.append(dict(Sector='NETZE',Variant='NONE',X=v['X'],Y=v['Y'],RGB=v['Current_RGB'],State_ID=v['State_ID'],Owner_before=v['Current_owner'],Owner_proposed='',Decision_category='C',Basis='Southern source rim interpretation/dating contradicted or unresolved; no qualified new local source-to-real line',Approval='NOT_ELIGIBLE',Applied=False))
    csvout('CELL_DECISIONS.csv',decisions)
    dump('BROMBERG_CONCLUSION.json',dict(status='C_NON_RESOLU',new_demonstrated_cells=0,new_fits=0,new_control_points=0,
        cause='Political/date identification of southern rim, before geometric fitting',
        countercheck='Szubin municipality dates incorporation1773; retained maps place its town symbol outside coloured acquired rim. This challenges Jan1776 use of whole rim, not proof every segment is wrong.',
        not_established=['Exact meaning of every rim segment','Date of each annotation or revised boundary','Whether this retained1775 exemplar accurately updates all1773 acquisitions','A qualified subset unchanged until Jan1776'],
        next_specific_evidence='Dated pre-Jan1776 boundary act/line including Schubin-Solec sector, or documented revision history of the retained rim; no general archival campaign started.'))

def images():
    bmp,water,river,_=p.physical_masks();proposal=r.read_csv(OUT/'PEENE_PROPOSED_CELLS.csv');x0,y0,x1,y1=4401,730,4415,742;s=34;pw=(x1-x0)*s;ph=(y1-y0)*s
    colors={0x567452:[239,210,100],0xE1A03A:[136,173,209]};owner={int(v['key'][0][1:],16):v['key'][2] for v in w.load('BASELINE.json')['inventory']['owners']}
    a=bmp[y0:y1,x0:x1];arr=np.full((*a.shape,3),[212,231,245],np.uint8)
    for rgb in np.unique(a):
        if int(rgb) in owner:arr[a==rgb]=colors.get(int(rgb),[205,205,205])
    base=Image.fromarray(arr).resize((pw,ph),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(3*pw+100,ph+350),'white');d=ImageDraw.Draw(canvas);summary=load('PEENE_OPTION_SUMMARY.json');banks=r.read_csv(OUT/'PEENE_BANK_ENVELOPE.csv')
    for k,title in enumerate(['Etat installe :357 cellules SWE','Variante A : +3 cellules (proposition)','Variante B : +41 cellules (proposition)']):
        im=base.copy();dd=ImageDraw.Draw(im);variant='A' if k==1 else 'B' if k==2 else None
        chosen={(int(v['X']),int(v['Y'])) for v in proposal if v['Variant']==variant}
        for x,y in chosen:
            dd.rectangle(((x-x0)*s,(y-y0)*s,(x+1-x0)*s,(y+1-y0)*s),fill='#efd264')
            dd.line(((x-x0)*s+4,(y-y0)*s+4,(x+1-x0)*s-4,(y+1-y0)*s-4),fill='#d65000',width=3)
        for x in range(x0,x1):
            dd.line(((x-x0)*s,0,(x-x0)*s,ph),fill='#aaaaaa');dd.text(((x-x0)*s+1,1),str(x),fill='black',font=w.font(11))
        for y in range(y0,y1):
            dd.line((0,(y-y0)*s,pw,(y-y0)*s),fill='#aaaaaa');dd.text((1,(y-y0)*s+1),str(y),fill='black',font=w.font(11))
        for yy in range(y0,y1):
            for xx in range(x0,x1):
                if xx+1<x1 and bmp[yy,xx]!=bmp[yy,xx+1]:dd.line(((xx+1-x0)*s,(yy-y0)*s,(xx+1-x0)*s,(yy+1-y0)*s),fill='#333333',width=2)
                if yy+1<y1 and bmp[yy,xx]!=bmp[yy+1,xx]:dd.line(((xx-x0)*s,(yy+1-y0)*s,(xx+1-x0)*s,(yy+1-y0)*s),fill='#333333',width=2)
        # Left-envelope modern bank is a distinct drawing support, not historical proof.
        points=[((float(v['Bank_X_min'])-x0)*s,(int(v['Y'])+.5-y0)*s) for v in banks];dd.line(points,fill='#8e00b0',width=2)
        # Provisional point retained from R5: explicitly not a native city control.
        tx,ty=(4410.1394-x0)*s,(735.049-y0)*s;dd.ellipse((tx-4,ty-4,tx+4,ty+4),outline='#b00000',width=2)
        ox=20+k*(pw+30);canvas.paste(im,(ox,110));d.text((ox,65),title,fill='black',font=w.font(21))
        if variant:d.text((ox,ph+130),f"~{summary[variant]['approx_added_land_km2']:.1f} km2 / total simule {summary[variant]['prospective_SWE_RGB_cell_count']} cellules SWE",fill='black',font=w.font(20))
    d.text((20,12),'R7 - PEENE : ARBITRAGE UNIQUEMENT / RIEN INSTALLE',fill='black',font=w.font(30))
    for j,text in enumerate([
      'Jaune : Suede ; bleu : Prusse. Hachures orange : ajouts proposes, categorie B, approbation requise.',
      'Trait violet : enveloppe ouest des variantes du rivage moderne LUNG, aide de dessin seulement.',
      'Cercle rouge : point urbain Wolgast provisoire R5, NON valide dans le raster ; aucune cellule forcee sur ce point.',
      'Traits fonces : limites RGB existantes. Grille : pixels natifs entiers, agrandissement sans interpolation.',
      'A et B sont des choix exclusifs. Anklam/Peendamm (Y>=740) hors ajouts. Aucun transfert des ensembles Usedom/Wollin.',
      'Les distances au trait moderne ne sont ni erreurs historiques certifiees ni intervalles de confiance.']):d.text((20,ph+175+j*26),text,fill='black',font=w.font(17))
    canvas.save(OUT/'PEENE_OPTIONS.png')
    # Source comparison: no false geographic registration of an unqualified line.
    sources=[('GUESSEFELD_SOUTH_READING.png','1775 retenue : Szubin au sud du lisere'),('MANUSCRIPT_EAST_SOUTH_READING.png','[1772] : Szubin hors bande coloree')]
    board=Image.new('RGB',(1860,1110),'white');d=ImageDraw.Draw(board);d.text((20,15),'BROMBERG SUD : COMPARAISON DES SOURCES, NON GEOREFERENCEE',fill='black',font=w.font(27))
    for k,(file,label) in enumerate(sources):
        im=Image.open(OUT/file).convert('RGB');im.thumbnail((580,800));ox=20+k*620;board.paste(im,(ox,100));d.text((ox,65),label,fill='black',font=w.font(19))
    nx0,ny0,nx1,ny1=4503,757,4520,775;scale=31;native=bmp[ny0:ny1,nx0:nx1];rgb=np.full((*native.shape,3),[200,220,240],np.uint8)
    for value in np.unique(native):
        if int(value) in owner:rgb[native==value]={'PRU':[136,173,209],'PLC':[225,165,180]}.get(owner[int(value)],[205,205,205])
    im=Image.fromarray(rgb).resize(((nx1-nx0)*scale,(ny1-ny0)*scale),Image.Resampling.NEAREST);dd=ImageDraw.Draw(im)
    for x in range(nx0,nx1):dd.line(((x-nx0)*scale,0,(x-nx0)*scale,im.height),fill='#777777')
    for y in range(ny0,ny1):dd.line((0,(y-ny0)*scale,im.width,(y-ny0)*scale),fill='#777777')
    for row in r.read_csv(OUT/'CELL_DECISIONS.csv'):
        x,y=int(row['X']),int(row['Y'])
        if row['Sector']=='NETZE' and nx0<=x<nx1 and ny0<=y<ny1:dd.rectangle(((x-nx0)*scale+3,(y-ny0)*scale+3,(x+1-nx0)*scale-3,(y+1-ny0)*scale-3),outline='#444444',width=2)
    for yy,xx in zip(*np.where(river[ny0:ny1,nx0:nx1])):dd.ellipse(((xx+.5)*scale-2,(yy+.5)*scale-2,(xx+.5)*scale+2,(yy+.5)*scale+2),fill='#0011bb')
    board.paste(im,(1260,100));d.text((1260,65),'Etat actuel : PRU bleu / PLC rose',fill='black',font=w.font(20))
    d.text((1260,685),'Gris : candidates C, aucun transfert.',fill='black',font=w.font(19))
    d.text((1260,720),'Grille native / RGB existants conserves.',fill='black',font=w.font(19))
    for j,text in enumerate([
      'Contre-controle : la commune de Szubin date son incorporation prussienne de1773, avant la date cible.',
      'Lire le lisere entier comme frontiere souveraine de1776 est donc non etabli. Tous ses troncons ne sont pas prouves faux.',
      'Pas de projection de cette ligne dans le jeu : aucun segment source vers reel accepte.18 cellules locales restent C.',
      'Les pixels actuels de Bromberg restent ceux de R3 :85 PRU /142 PLC. Aucun transfert, Thorn exclu.']):d.text((20,955+j*31),text,fill='black',font=w.font(22))
    board.save(OUT/'BROMBERG_BORDER.png')

def validate():
    baseline=load('BASELINE.json');runtime=w.prior.economy.runtime_hashes();inv=w.prior.r3.r2.core.qa.inventory();bmp,water,rivers,path=p.physical_masks();checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    check('2169 runtime files byte-identical',runtime==baseline['runtime_hashes'] and len(runtime)==2169)
    check('R3/R5 reference retained',runtime==w.load('BASELINE.json')['runtime_hashes'])
    check('All306 R1-R6 files retained by hash',len(baseline['prior_hashes'])==306 and all((ROOT/q).is_file() and w.sha(ROOT/q)==h for q,h in baseline['prior_hashes'].items()))
    check('Bitmap unchanged',w.sha(ROOT/'map_data/provinces.png')==baseline['bitmap_sha256'])
    check('HEAD unchanged',w.prior.r3.r2.head()==baseline['git_head']);check('Index unchanged',w.sha(ROOT/'.git/index')==baseline['git_index_sha256'])
    check('Effective demographic/economic/military inventory unchanged',hashlib.sha256(json.dumps(inv,sort_keys=True).encode()).hexdigest()==baseline['inventory_sha256'])
    check('Global population835804980',sum(v['count'] for v in inv['pops'])==835804980)
    owner={int(v['key'][0][1:],16):(v['key'][1],v['key'][2]) for v in inv['owners']}
    for value,count,tag in [(0x567452,357,'SWE'),(0xEDB010,85,'PRU'),(0xFCC7B7,142,'PLC')]:check(f'x{value:06X} count{count} owner{tag}',int((bmp==value).sum())==count and owner[value][1]==tag)
    check('44 inherited RGB duplicates preserved',len(inv['duplicates'])==44 and inv['duplicates']==w.load('BASELINE.json')['inventory']['duplicates'])
    check('12 inherited invalid references preserved',len(inv['errors'])==12 and inv['errors']==w.load('BASELINE.json')['inventory']['errors'])
    rows=r.read_csv(OUT/'PEENE_PROPOSED_CELLS.csv');sets={v:{(int(q['X']),int(q['Y'])) for q in rows if q['Variant']==v} for v in ['A','B']};rules=load('OPTION_RULES.json')
    check('Exactly two mutually exclusive options with A strict subset of B',sets['A']<sets['B'] and set(q['Variant'] for q in rows)=={'A','B'})
    check('No duplicated pixel within an option',len(rows)==len({(q['Variant'],q['X'],q['Y']) for q in rows}))
    check('All proposals categoryB and pending approval, none applied',all(q['Decision_category']=='B' and q['Approval']=='PENDING_PLAYER' and q['Applied']=='False' for q in rows))
    check('Every proposed RGB State_ID owner is actual',all(int(bmp[int(q['Y']),int(q['X'])])==0xE1A03A and owner[0xE1A03A]==(q['State_ID'],q['Owner_before']) and q['Owner_proposed']=='SWE' and q['RGB_proposed']=='x567452' for q in rows))
    check('No newly invented RGB',0x567452 in owner and owner[0x567452][1]=='SWE')
    check('Proposals local land only, rows740+ protected',all(4404<=int(q['X'])<4412 and 732<=int(q['Y'])<740 and not water[int(q['Y']),int(q['X'])] for q in rows))
    check('Whole proposed cell stays west of all drawing-bank variants',all(float(q['Right_edge_setback_min_px'])>=0 for q in rows))
    check('All proposed cells inside inherited model support',all(q['Inside_frozen_R5_support']=='True' for q in rows))
    existing={(x,y) for y in range(728,744) for x in range(4398,4418) if bmp[y,x]==0x567452}
    for variant,cells in sets.items():check(variant+' new components connect to existing SWE',connected_to_existing(cells,existing)==cells)
    priorC={(q['X'],q['Y']) for q in r.read_csv(OUT.parent/'R5/CANDIDATE_CELLS.csv') if q['Class']=='C'}
    check('No inherited C automatically promoted to proposalB',all((q['X'],q['Y']) not in priorC for q in rows))
    check('Neither proposal creates a Peendamm enclave',all(y<740 for cells in sets.values() for x,y in cells))
    check('Areas are explicit approximations; no invented historical-area ratio',all(v['area_distortion_ratio'] is None and v['exact_historical_added_area_km2'] is None for v in load('PEENE_OPTION_SUMMARY.json').values()))
    decisions=r.read_csv(OUT/'CELL_DECISIONS.csv');check('No demonstratedA; Netze remainsC; all unapplied',not any(q['Decision_category']=='A' for q in decisions) and all(q['Decision_category']=='C' for q in decisions if q['Sector']=='NETZE') and all(q['Applied']=='False' for q in decisions))
    check('18 local Netze candidates only; Thorn excluded',sum(q['Sector']=='NETZE' for q in decisions)==18 and all(q['RGB']!='x41A021' for q in decisions))
    controls=r.read_csv(OUT/'CONTROL_POINTS.csv');check('No new fits or controls invented',all(q['New_R7']=='False' and q['Used_for_fit']=='False' and q['Used_for_model_selection']=='False' for q in controls))
    check('Corrected river width15 retained',rivers[np.asarray(Image.open(path))==15].all())
    for name in ['REPORT.md','PEENE_OPTIONS.md','PEENE_OPTIONS.png','PEENE_PROPOSED_CELLS.csv','BROMBERG_SOUTHERN_BORDER.md','BROMBERG_BORDER_EVIDENCE.csv','BROMBERG_BORDER.png','CONTROL_POINTS.csv','CELL_DECISIONS.csv','PLAYER_DECISION.md','NEXT_STEPS.md']:
        check('Deliverable '+name,(OUT/name).is_file())
    compile((OUT/'arbitration.py').read_text(encoding='utf-8'),'arbitration.py','exec');check('Python syntax',True)
    summary=load('PEENE_OPTION_SUMMARY.json');result=dict(status='MAP-2M-R7_READY_FOR_PLAYER_DECISION',MAP2M_historically_complete=False,static_status='PASS' if all(q['passed'] for q in checks) else 'FAIL',passed=sum(q['passed'] for q in checks),total=len(checks),checks=checks,
      runtime_files_protected=len(runtime),prior_artifacts_protected=len(baseline['prior_hashes']),functional_changes=[],applied_cells=0,new_RGBs=0,world_population=835804980,
      Peene_options=summary,option_categories={'A':'B approximation proposed','B':'B approximation proposed'},Bromberg_status='C_NON_RESOLU_POLITICAL_DATING',demonstrated_A_cells=0,
      manual_R3_runtime_status='PASS_RUNTIME_USER_VALIDATED',R7_engine_test=False,automated_engine_test=False,inherited_anomalies={'duplicate_RGBs':44,'invalid_references':12},
      ColGrep={'calls':0,'reason':'All required source, model and code paths already known; no redundant code-location search.'},new_calibration_points=0,new_model_fits=0)
    dump('VALIDATION.json',result);dump('MANIFEST.json',{q.relative_to(OUT).as_posix():dict(sha256=w.sha(q),bytes=q.stat().st_size) for q in OUT.rglob('*') if q.is_file() and q.name!='MANIFEST.json'})
    print(result['static_status'],result['passed'],'/',result['total'],'; NO RUNTIME CHANGES; OPTIONS REQUIRE PLAYER APPROVAL')
    if not all(q['passed'] for q in checks):raise SystemExit('Validation failed')

if __name__=='__main__':{'capture':capture,'options':options,'source_views':source_views,'evidence':evidence,'images':images,'validate':validate}[sys.argv[1]]()
