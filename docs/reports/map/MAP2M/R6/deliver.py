"""MAP-2M-R6 presentation and preservation tests. Writes R6 artifacts only."""
import sys,json,hashlib,collections
import numpy as np
from PIL import Image,ImageDraw
import pilot as p
w=p.w;r=p.r;OUT=p.OUT;ROOT=p.ROOT

def images():
    bmp,water,river,path=p.physical_masks()
    owners={int(v['key'][0][1:],16):v['key'][2] for v in w.load('BASELINE.json')['inventory']['owners']}
    rows=r.read_csv(OUT/'CANDIDATE_DECISIONS.csv')
    for pilot,sector,box,s in [('A','PEENE',(4402,730,4415,741),42),('B','NETZE',(4503,757,4520,775),32)]:
        x0,y0,x1,y1=box;loc=bmp[y0:y1,x0:x1];arr=np.full((*loc.shape,3),[210,225,240],np.uint8)
        for v in np.unique(loc):
            if int(v) in owners:arr[loc==v]={'SWE':[240,210,110],'PRU':[120,162,205],'PLC':[225,165,180]}.get(owners[int(v)],[205,205,205])
        base=Image.fromarray(arr).resize(((x1-x0)*s,(y1-y0)*s),Image.Resampling.NEAREST);pw,ph=base.size
        canvas=Image.new('RGB',(2*pw+60,ph+310),'white');d=ImageDraw.Draw(canvas)
        for k,label in enumerate(['Reference effective avant R6','Apres R6 : AUCUN TRANSFERT']):
            im=base.copy();dd=ImageDraw.Draw(im)
            for x in range(x0,x1):dd.line(((x-x0)*s,0,(x-x0)*s,ph),fill='#777777')
            for y in range(y0,y1):dd.line((0,(y-y0)*s,pw,(y-y0)*s),fill='#777777')
            for yy,xx in zip(*np.where(river[y0:y1,x0:x1])):
                cx,cy=(xx+.5)*s,(yy+.5)*s;dd.ellipse((cx-2,cy-2,cx+2,cy+2),fill='#0011bb')
            if k:
                for v in rows:
                    x,y=int(v['X']),int(v['Y'])
                    if v['Pilot']==pilot and x0<=x<x1 and y0<=y<y1:dd.rectangle(((x-x0)*s+3,(y-y0)*s+3,(x+1-x0)*s-3,(y+1-y0)*s-3),outline='#df6600' if v['Class']=='B' else '#555555',width=3)
            ox=20+k*(pw+20);canvas.paste(im,(ox,100));d.text((ox,62),label,fill='black',font=w.font(20))
        d.text((20,15),'R6 PILOTE '+pilot+' - proprietaires inchanges / couches diagnostiques',fill='black',font=w.font(24))
        for y,text in enumerate([
          'Fonds identiques : Prusse bleu, Suede jaune, Pologne rose ; aucune cellule A.',
          'Cadres a droite : B orange / C gris. Ce ne sont PAS des transferts installes.',
          'Petits points bleus : rivieres natives, indices 3 a 15 (lecture R6 corrigee).',
          'Aucun trace historique source vers reel accepte : aucune fausse limite georeferencee.',
          'Sources interpretees et hypotheses rejetees : images *_BANK / *_RIM_* separees.',
          'Thorn exclu ; changements fonctionnels = 0.']):d.text((20,ph+125+y*28),text,fill='black',font=w.font(17))
        canvas.save(OUT/(sector+'_BEFORE_AFTER.png'))
    # Independent final diagnostic on a physical river mask, no political labels.
    im=Image.open(OUT/'NATIVE_B_READING.png').convert('RGB');canvas=Image.new('RGB',(max(im.width,1100),im.height+170),'white');canvas.paste(im,(0,120));d=ImageDraw.Draw(canvas)
    row=next(v for v in r.read_csv(OUT/'FINAL_HOLDOUT_CHECKS.csv') if v['ID']=='B_VISTULA_WEST_APEX')
    details=next(v for v in p.load('FINAL_HOLDOUT_DETAIL.json') if v['id']==row['ID'])
    def xy(x,y):return ((x-4497)*32,(y-753)*32+120)
    for x,y in details['native_tied_centres']:
        x,y=xy(x,y);d.ellipse((x-5,y-5,x+5,y+5),outline='#aa0000',width=3)
    x,y=xy(float(row['Pred_X']),float(row['Pred_Y']));d.line((x-9,y,x+9,y),fill='#a000aa',width=3);d.line((x,y-9,x,y+9),fill='#a000aa',width=3)
    d.text((10,10),'Vistule : controle final R6, modele R5 fige',fill='black',font=w.font(25))
    d.text((10,45),'Rouge : 5 cellules ex aequo ; violet : prediction. Ecart au milieu = 0,68 px.',fill='black',font=w.font(20))
    d.text((10,78),'Plateau : rayon de lecture requis 2,5 px ; pas une precision certifiee de 0,68 px.',fill='black',font=w.font(20))
    canvas.save(OUT/'FINAL_HOLDOUT_REVIEW.png')

def unresolved():
    rows=[
      ('A_LOCAL_NATIVE','A','PHYSICAL_HOMOLOGUE_MISSING','No opposed shores of Wolgast narrows identified in native masks, including corrected widths','A political cell border remains possible in principle; it would be an explicit generalization, not a bank-resolved reconstruction.'),
      ('A_SOURCE_REAL','A','GEOREFERENCE_NOT_ACCEPTED','New western bank reading exists in source pixels; no new distributed, securely identified source-real controls','No refit of failed northern Mayer capes. Either provide homologated local anchors or authorize a separately reviewed generalized political line.'),
      ('PEENDAMM','A','RESOLUTION_AND_POLYGON','Urban references span0.152x0.203px; historical enclave polygon/area still not established','Do not infer whole enclave extent from the mill. No minimum-cell enclave installed; any enlargement requires explicit user approval.'),
      ('B_SOURCE_LINE','B','POLITICAL_LINE_AND_DATE','1772 manuscript rim is not automatically international; private red text explicitly excluded; southern1775 segment not matched to1772 state','Identify dated sovereign segment and new source-real controls for this one segment; do not reopen all four districts.'),
      ('B_FINAL_PLATEAU','B','GENERALIZED_PHYSICAL_CHECK','Vistula apex centroid residual0.679px, but5 tied native cells require2.5px reading radius','Retain final check, do not fit it or use it to select a new model. One schematic bend does not certify every adjacent cell.'),
      ('B_SUPPORT','B','EXTRAPOLATION','Some investigated cell centres lie outside frozen R5 support; individually flagged','Do not extend validated domain silently; maintain C where full chain is absent.'),
      ('PFAU','B','NO_NEW_IDENTIFICATION','No new proof for Inowroclaw/Pakosc crosses','Do not reoptimize the old ambiguous points or use1778 borders automatically for Jan1776.'),
      ('INHERITED','BOTH','PREEXISTING_ANOMALIES','44 duplicate RGBs and12 invalid references persist without new runtime edits','Keep separate from R6 regressions; not repaired in this local pilot.'),
      ('THORN','B','OUT_OF_SCOPE','x41A021 unchanged','Separate task only.')]
    p.csvout('UNRESOLVED.csv',[dict(ID=i,Pilot=a,Category=c,Obstacle=o,Next_action=n) for i,a,c,o,n in rows])

def validate():
    b=p.load('BASELINE.json');current=w.prior.economy.runtime_hashes();inventory=w.prior.r3.r2.core.qa.inventory();bmp,water,river,rp=p.physical_masks();tests=[]
    def check(name,ok):tests.append(dict(name=name,passed=bool(ok)))
    check('2169 functional files byte-identical to R6 start',current==b['runtime_hashes'] and len(current)==2169)
    check('Runtime also byte-identical to R5 start',current==w.load('BASELINE.json')['runtime_hashes'])
    check('All264 R1-R5 evidence/artifact files unchanged',len(b['prior_files'])==264 and all((ROOT/name).is_file() and w.sha(ROOT/name)==sha for name,sha in b['prior_files'].items()))
    check('HEAD unchanged',w.prior.r3.r2.head()==b['git_head']);check('Git index unchanged',w.sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('provinces.png unchanged',w.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256'])
    check('Inventory including pops/cultures/religions/buildings/PM/owners/military unchanged',hashlib.sha256(json.dumps(inventory,sort_keys=True).encode()).hexdigest()==b['inventory_sha256'])
    check('World population835804980',sum(v['count'] for v in inventory['pops'])==835804980)
    owner={int(v['key'][0][1:],16):(v['key'][1],v['key'][2]) for v in inventory['owners']}
    for rgb,n,tag in [(0x567452,357,'SWE'),(0xEDB010,85,'PRU'),(0xFCC7B7,142,'PLC')]:
        check(f'x{rgb:06X} retains{n} cells and owner{tag}',int((bmp==rgb).sum())==n and owner[rgb][1]==tag)
    check('44 inherited duplicate RGBs unchanged',len(inventory['duplicates'])==44 and inventory['duplicates']==w.load('BASELINE.json')['inventory']['duplicates'])
    check('12 inherited invalid references unchanged',len(inventory['errors'])==12 and inventory['errors']==w.load('BASELINE.json')['inventory']['errors'])
    rows=r.read_csv(OUT/'CANDIDATE_DECISIONS.csv');check('Every cell resolves to actual RGB State_ID owner',all(int(v['Current_RGB'][1:],16)==int(bmp[int(v['Y']),int(v['X'])]) and owner[int(v['Current_RGB'][1:],16)]==(v['State_ID'],v['Current_owner']) for v in rows))
    check('No duplicate candidate coordinate',len(rows)==len({(v['X'],v['Y']) for v in rows}))
    check('No A, no applied transfer, no invented RGB',all(v['Class'] in ['B','C'] and v['Applied']=='False' and not v['Proposed_RGB'] for v in rows))
    check('18 inherited Peene candidates only',sum(v['Pilot']=='A' for v in rows)==18)
    ys,xs=np.where(bmp==0xEDB010);core=np.c_[xs,ys]
    check('B candidates directly adjacent to core and inside pilot',all(4501<=int(v['X'])<4520 and 758<=int(v['Y'])<775 and np.min(np.abs(core-[int(v['X']),int(v['Y'])]).sum(axis=1))==1 for v in rows if v['Pilot']=='B'))
    inherited={(v['X'],v['Y']) for v in r.read_csv(p.R5/'CANDIDATE_CELLS.csv') if v['Origin']=='R4_INHERITED'}
    check('No automatic import of R5 additional149',all((v['X'],v['Y']) in inherited for v in rows))
    check('Thorn excluded',all(v['Current_RGB']!='x41A021' for v in rows))
    check('Zero territorial ledger entries',not r.read_csv(OUT/'TERRITORIAL_CHANGES.csv'))
    model=p.load('LOCAL_TRANSFORMATIONS.json');check('Native parameters frozen, no refit',model['frozen_native']==w.load('TRANSFORMATIONS.json')['selected_native'] and model['new_native_fit_points']==0 and model['new_source_fits']==0)
    protocol=p.load('FROZEN_PROTOCOL.json');check('Frozen model hash matches',protocol['native_model_sha256']==w.sha(p.R5/'TRANSFORMATIONS.json'))
    checks=r.read_csv(OUT/'FINAL_HOLDOUT_CHECKS.csv');check('Both final checks kept separate from fitting and selection',len(checks)==2 and all(v['Used_for_fit']=='False' and v['Used_for_selection']=='False' for v in checks))
    a=next(v for v in checks if v['ID']=='A_WOLGAST_NARROWS');check('Unobservable channel has no fabricated residual',not a['Residual_px'] and a['Status']=='UNMEASURABLE_NO_NATIVE_CHANNEL')
    bb=next(v for v in checks if v['ID']=='B_VISTULA_WEST_APEX');check('New bend diagnostic inside R5 support',bb['Outside_R5_support']=='False')
    detail=next(v for v in p.load('FINAL_HOLDOUT_DETAIL.json') if v['id']==bb['ID']);check('Five-cell ambiguity explicitly retained',len(detail['native_tied_centres'])==5 and detail['observed_plateau_radius_including_half_cell_px']==2.5 and detail['reading_ambiguity_exceeds_preregistered_radius'])
    check('Forward inverse math roundtrip',np.allclose(r.inverse(model['frozen_native'],r.forward(model['frozen_native'],[[13.78,54.05],[18.14,53.115]])),[[13.78,54.05],[18.14,53.115]],atol=1e-10))
    raw=np.asarray(Image.open(rp))
    check('Corrected width15 included; special and background indices excluded',river[raw==15].all() and not river[np.isin(raw,[0,1,2,254,255])].any())
    check('Pilot B recovers17 omitted width15 pixels',int((raw[753:777,4497:4525]==15).sum())==17 and int(river[753:777,4497:4525].sum())==45)
    for t in p.load('SOURCE_LINE_OBSERVATIONS.json'):
        path=ROOT/t['Source'];im=Image.open(path);pts=np.asarray(t['points'])
        check('Source hash and pixel bounds '+t['ID'],w.sha(path)==t['sha256'] and (pts>=0).all() and (pts[:,0]<im.width).all() and (pts[:,1]<im.height).all())
    check('No invented geographic coordinates for unqualified source traces',all(not v['Longitude_A'] and not v['Latitude_A'] and v['Applied']=='False' for v in r.read_csv(OUT/'HISTORICAL_BORDER_EVIDENCE.csv')))
    for name in ['REPORT.md','PILOT_A_PEENE.md','PILOT_B_BROMBERG.md','HISTORICAL_BORDER_EVIDENCE.csv','CONTROL_POINTS.csv','FINAL_HOLDOUT_CHECKS.csv','LOCAL_TRANSFORMATIONS.json','CANDIDATE_DECISIONS.csv','TERRITORIAL_CHANGES.csv','PEENE_BEFORE_AFTER.png','NETZE_BEFORE_AFTER.png','UNRESOLVED.csv','NEXT_STEPS.md']:
        check('Deliverable '+name,(OUT/name).is_file())
    for name in ['pilot.py','deliver.py']:compile((OUT/name).read_text(encoding='utf-8'),name,'exec');check('Python syntax '+name,True)
    result=dict(status='MAP-2M-R6_PARTIAL',method_demonstrated_for_political_cell_transfer=False,static_integrity_status='PASS' if all(t['passed'] for t in tests) else 'FAIL',passed=sum(t['passed'] for t in tests),total=len(tests),tests=tests,
      functional_file_count=len(current),prior_files_protected=len(b['prior_files']),functional_changes=[],territorial_transfers=0,new_RGBs=0,world_population=835804980,
      candidate_classes=dict(collections.Counter(v['Class'] for v in rows)),extrapolated_candidate_count=sum(v['Outside_frozen_R5_support']=='True' for v in rows),
      final_holdout_count=2,final_numerically_measurable=1,bend_midpoint_disagreement_px=float(bb['Residual_px']),bend_reading_ambiguity_px=2.5,new_model_fits=0,
      corrected_diagnostic_filter='River width indices3..15, not3..11. No runtime edits. Old R5 reports preserved.',inherited_anomalies=dict(duplicate_RGBs=44,invalid_references=12),runtime_test_R6=False,automated_engine_test=False,
      ColGrep=dict(invocations=2,successful_agent_searches=1,first='Index lock denied',second='Exit0; returned R1/NETZE/REPORT.md lines5 and9; verified by reading lines1-24',new_relevant_asset_discovered=False,model_GPU_telemetry_captured=False,exact_token_savings=None))
    p.dump('VALIDATION.json',result)
    p.dump('MANIFEST.json',{file.relative_to(OUT).as_posix():dict(sha256=w.sha(file),bytes=file.stat().st_size) for file in OUT.rglob('*') if file.is_file() and file.name!='MANIFEST.json'})
    print(result['static_integrity_status'],result['passed'],'/',result['total'],'; R6 PARTIAL;0 runtime edits')
    if not all(t['passed'] for t in tests):raise SystemExit('Validation failure')

if __name__=='__main__':{'images':images,'unresolved':unresolved,'validate':validate}[sys.argv[1]]()
