"""MAP-1C diagnostic calculations and report tables; NEVER writes runtime files."""
from pathlib import Path
import csv, json, zipfile, math, re, subprocess, difflib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from map1_prepare import protected, digest, table, GAME
from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/MAP1C'; E=OUT/'MAP1C_GEOGRAPHIC_EVIDENCE'
B=ROOT/'docs/reports/map/MAP1B'; OLD=ROOT/'docs/reports/map/MAP1'
before=json.loads((OUT/'MAP1C_PROTECTED_BEFORE.json').read_text())
assert protected()==before['runtime']
def save(name,rows):
    assert rows
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def jsonout(name,data):
    (E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

# Real contemporary gazetteer coordinates are NOT historical boundaries or game locators.
rows=[r.split('\t') for r in zipfile.ZipFile(E/'cities1000.zip').read('cities1000.txt').decode('utf-8').splitlines()]
ids={'Luxembourg':2960316,'Namur':2790471,'Liège':2792413,'Charleroi':2800481,'Brussels':2800866,'Trier':2821164,'Reims':2984114,
     'Milan':3173435,'Como':3178229,'Genoa':3176219,'Parma':3171457,'Piacenza':3171058,'Verona':3164527,
     'Brescia (game label)':3181554,'Bergamo (game label)':3182164,
     'Breslau':3081368,'Liegnitz':3093692,'Oppeln':3090048,'Ratibor':3087584,'Glogau':3099213,'Görlitz':2918987,'Olomouc':3069011}
gaz={int(r[0]):r for r in rows}
controls=table(B/'MAP1B_GEOGRAPHIC_EVIDENCE/GCP_AND_CONTROLS.csv')
metrics=[]; obs=[]
def fit(X,Y,method):
    # X are centered east/north km; affine and similarity are distinct local models.
    if method=='AFFINE':
        D=np.column_stack([X,np.ones(len(X))]); T=np.linalg.lstsq(D,Y,rcond=None)[0]
        return lambda x:np.column_stack([x,np.ones(len(x))])@T, float(np.linalg.cond(D)), int(np.linalg.matrix_rank(D))
    # Raster Y is downward, geographical north is upward: allow this reflection.
    X=X.copy(); X[:,1]*=-1
    D=[]; y=[]
    for (x,z),(u,v) in zip(X,Y): D.extend([[x,-z,1,0],[z,x,0,1]]); y.extend([u,v])
    D=np.array(D); a,b,c,d=np.linalg.lstsq(D,y,rcond=None)[0]
    return lambda x:np.column_stack([a*x[:,0]+b*x[:,1]+c,b*x[:,0]-a*x[:,1]+d]),float(np.linalg.cond(D)),int(np.linalg.matrix_rank(D))
for case in ['lux','lombardy','silesia']:
    cc=[p for p in controls if p['Case']==case]
    lat0=np.mean([float(gaz[ids[p['Name']]][4]) for p in cc]); lon0=np.mean([float(gaz[ids[p['Name']]][5]) for p in cc])
    X=np.array([[(float(gaz[ids[p['Name']]][5])-lon0)*111.32*math.cos(math.radians(lat0)),(float(gaz[ids[p['Name']]][4])-lat0)*111.32] for p in cc])
    scan=np.array([[float(p['Source_X']),float(p['Source_Y'])] for p in cc]); game=np.array([[float(p['Game_X']),float(p['Game_Y'])] for p in cc])
    ii=[i for i,p in enumerate(cc) if p['Role']=='FIT']; check=[i for i,p in enumerate(cc) if p['Role']=='CHECK']
    for target,Y in [('HISTORICAL_SCAN',scan),('GAME_LOCATORS_DIAGNOSTIC_ONLY',game)]:
        for method in ['AFFINE','SIMILARITY']:
            predict,cond,rank=fit(X[ii],Y[ii],method); errors=np.linalg.norm(predict(X)-Y,axis=1)
            loo=[]
            for i in range(len(cc)):
                keep=[j for j in range(len(cc)) if j!=i]
                model,_,_=fit(X[keep],Y[keep],method); loo.append(float(np.linalg.norm(model(X[i:i+1])-Y[i])))
            metrics.append(dict(Case=case,Target=target,Method=method,Fit_Count=len(ii),Independent_Check_Count=len(check),Fit_RMS_Px=float(np.sqrt(np.mean(errors[ii]**2))),Check_RMS_Px=float(np.sqrt(np.mean(errors[check]**2))),Check_Max_Px=float(max(errors[check])),All_Points_LOOCV_Max_Px=max(loo),Design_Condition=cond,Design_Rank=rank,Use_For_Sovereignty='NO'))
            for i,p in enumerate(cc):
                r=gaz[ids[p['Name']]]
                obs.append(dict(Case=case,Name=p['Name'],GeoNames_ID=r[0],Modern_Name=r[1],Latitude_WGS84=r[4],Longitude_WGS84=r[5],Modern_Record_Modified=r[18],Historical_Scan_X=p['Source_X'],Historical_Scan_Y=p['Source_Y'],Historical_Observation_Status='INHERITED_NOT_RECONFIRMED_REJECTED_FOR_SOVEREIGNTY',Game_Locator_X=p['Game_X'],Game_Locator_Y=p['Game_Y'],Role=p['Role'],Method=method,Target=target,Residual_Px=float(errors[i]),LOOCV_Residual_Px=loo[i]))
    # Visual QA: independent city location to historical scan; no game polygon implied.
    config=json.loads((B/'MAP1B_GEOGRAPHIC_EVIDENCE/anchor_observations.json').read_text())[case]
    im=Image.open(B/'MAP1B_GEOGRAPHIC_EVIDENCE'/config['image']).convert('RGB'); d=ImageDraw.Draw(im); font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    pred,_,_=fit(X[ii],scan[ii],'AFFINE'); yy=pred(X)
    for i,p in enumerate(cc):
        x,y=scan[i]; u,v=yy[i]; color=(20,140,50) if i in ii else (225,70,10)
        d.line((x,y,u,v),fill=color,width=3); d.ellipse((x-5,y-5,x+5,y+5),outline=color,width=2)
        d.text((x+8,y-18),p['Name'],font=font,fill=color,stroke_width=1,stroke_fill='white')
    im.save(E/(case+'_independent_geodetic_scan.png'))
jsonout('GEODETIC_CONTROL_OBSERVATIONS.json',obs); jsonout('LOCAL_MODEL_COMPARISON.json',metrics)

base=table(OLD/'MAP1_BASELINE_PROVINCE_INDEX.csv'); geom=json.loads((OLD/'MAP1_GEOGRAPHIC_EVIDENCE/geometry_index.json').read_text())
pops=table(OLD/'MAP1_POP_INVENTORY.csv'); buildings=table(OLD/'MAP1_BUILDING_INVENTORY.csv')
focus=['xD001A0','x5180A0','x3A5FB9','xEF2040','x867A90','x9AC196','x4713EE','xA40CE9','x70B8A9','x50C060','x71E080','xF0E080','x9061E0']
decisions=[]
notes={
'xD001A0':('LUX-POL-01','DOCUMENTED_GAMEPLAY_APPROXIMATION','LUX under AUS personal_union','Duché habsbourgeois; conserver TAG LUX est un compromis politique, pas une certification du contour RGB.','LUX-02 pp.2-3; LUX-03; R1-0001/-0004','Proposer un pacte seulement; aucun transfert provincial; approbation explicite.'),
'x5180A0':('LUX-GEO-02','UNRESOLVED','NOT_SELECTED','Arlon/Bastogne et secteurs luxembourgeois possibles; contour entier non démontré.','LUX-01; LUX-02; R1-0001','Ne pas convertir une proximité urbaine en attribution du polygone.'),
'x3A5FB9':('LUX-GEO-03','UNRESOLVED','NOT_SELECTED','Secteurs Chiny/Bouillon; distinguer duché et principauté/enclaves.','LUX-01; LUX-02; R1-0035','Obtenir listes de villages et feuillets locaux Ferraris.'),
'xEF2040':('LUX-GEO-04','UNRESOLVED','NOT_SELECTED','Voisin nord: Liège et juridictions distinctes; pas de transfert global au duché.','LUX-01; R1-0004','Contrôle de la Meuse et enclaves requis.'),
'x867A90':('LOM-GEO-01','UNRESOLVED','NOT_SELECTED','Bergame relève de Venise, mais la province dépasse la seule ville vers les Alpes.','LOM-01/-04; LOM-05','Ni Milan ni Grisons sans preuve polygonale entière.'),
'x9AC196':('LOM-GEO-02','UNRESOLVED','NOT_SELECTED','Bormio/Valtellina relèvent des Trois Ligues en 1776; identité de tout ce RGB non démontrée.','LOM-01; LOM-05','Piste réelle VEN -> Trois Ligues, pas transfert automatique à SWI.'),
'x4713EE':('LOM-GEO-03','UNRESOLVED','NOT_SELECTED','Brescia/Crema vénitiennes et Crémone autrichienne doivent être séparées; possible polygone mixte.','LOM-01/-03/-04','Ne pas suivre le locator forestier nommé Bergamo.'),
'xA40CE9':('LOM-GEO-04','UNRESOLVED','NOT_SELECTED','Como milanaise contre Chiavenna/Valtellina grisonnes au nord.','LOM-01/-03/-05','Calage lacustre et juridictions nécessaires.'),
'x70B8A9':('LOM-GEO-05','UNRESOLVED','NOT_SELECTED','Mantoue habsbourgeoise; ne pas projeter ses droits sur toute la forme.','LOM-02/-03','Vérifier limites mantouanes et Pô.'),
'x50C060':('LOM-GEO-06','UNRESOLVED','NOT_SELECTED','Secteur Crema/Mantoue à préciser: autorité de la ville ne suffit pas.','LOM-02/-03/-04','Ne pas transférer à VEN par ressemblance du centre.'),
'x71E080':('SIL-GEO-01','UNRESOLVED','NOT_SELECTED','Partage de 1742 confirmé en 1763; Troppau/Teschen autrichiens, limites RGB incertaines.','SIL-01; SIL-02 p.19','Corriger scope MORAVIA indépendamment; arbitrage AUS/PRU toujours nécessaire.'),
'xF0E080':('SIL-GEO-02','UNRESOLVED','NOT_SELECTED','Province méridionale mixte possible Nysa/Troppau; double propriété écrite.','SIL-01; SIL-02 p.19','Ne pas choisir AUS ou PRU pour simplement supprimer le doublon.'),
'x9061E0':('SIL-TECH-01','UNRESOLVED','AUS (technical retention only)','AUS seul propriétaire écrit; la définition range ce RGB en WEST_GALICIA, pas UPPER_SILESIA.','Définition 02_east_europe.txt:184; historique 00_states.txt UPPER_SILESIA; SIL-02','Correction de référence envisageable sans changement de souveraineté; création du split AUS à contrôler.')}
for pid in focus:
    rr=[r for r in base if r['Province_ID']==pid]; owners=sorted({r['Owner_TAG'] for r in rr}); states=sorted({r['State_ID'] for r in rr}); bb=geom['bboxes'][pid]; ident,status,proposed,fact,source,action=notes[pid]
    affected=[r for r in pops if r['State_ID'] in states and r['Owner_TAG'] in owners]
    deps=[r for r in buildings if r['State_ID'] in states and r['Owner_TAG'] in owners]
    case='lux' if pid.startswith('x') and ident.startswith('LUX') else ('lombardy' if ident.startswith('LOM') else 'silesia')
    err=max(float(r['Residual_Game_Px']) for r in controls if r['Case']==case and r['Role']=='CHECK')
    decisions.append(dict(Decision_ID=ident,Province_RGB=pid,Geometry_State='|'.join(states),Current_Written_Owner='|'.join(owners),Proposed_Owner_Or_Relationship=proposed,Decision_Status=status,Change_Type='POLITICAL_RELATION' if ident=='LUX-POL-01' else ('TECHNICAL_SCOPE_ONLY' if pid=='x9061E0' else 'TERRITORIAL_INVESTIGATION'),Pixel_Area=int(rr[0]['Province_Pixels']),Pixel_BBox=json.dumps(bb),BBox_Width_Px=bb[2]-bb[0],BBox_Height_Px=bb[3]-bb[1],MAP1B_Check_Max_Error_Px=err,Error_Over_Small_BBox_Dimension=err/min(bb[2]-bb[0],bb[3]-bb[1]),Historical_Facts_1776_01_01=fact,Documents_And_Limits=source+'; voir METHOD_AND_EVIDENCE.md',Cartographic_Method='WGS84 audit of inherited scan points (not reconfirmed) affine/similarity + game physical-reference review; bitmap alignment not certified',State_Owner_Population_Written=sum(int(r['Size']) for r in affected),Population_On_RGB='NOT_DETERMINABLE_FROM_STATE_LEVEL_POPS',Building_Commands_In_Geometry_State=len(deps),Population_Buildings_Units_Impact='No application. Preserve all records; projected transfer allocations unknown. See DEPENDENCY_IMPACTS.json.',Diplomacy_Impact='AUS-LUX pact changes subject status and potentially bloc/markets' if ident=='LUX-POL-01' else 'No diplomatic change authorized',Risk_And_Fallback=action,User_Approved='NO',Auto_Transfer='FORBIDDEN'))
save('MAP1C_MAPPING_DECISIONS.csv',decisions)

luxpop=[r for r in pops if r['Owner_TAG']=='LUX']; luxbuild=[r for r in buildings if r['Owner_TAG']=='LUX']
assert sum(int(r['Size']) for r in luxpop)==137881
approx=[dict(Approval_ID='APP-LUX-01',Decision_ID='LUX-POL-01',Province_RGB='xD001A0',Category='DOCUMENTED_GAMEPLAY_APPROXIMATION',Proposal='Keep LUX as separate country; add AUS -> LUX personal_union; no RGB transfer',Historical_Authority='Habsburg duchy, not sovereign modern Luxembourg',Compromise='Existing LUX tag retained as dynastic territorial proxy, not a claim that current 47-pixel boundary is the whole historical duchy',Affected_Pops=137881,Buildings='All LUX written building commands preserved; no ownership reassignment',Units='Preserve LUX formation/recruitment records; check subject participation in engine',Diplomacy='Changes independence; verify market/bloc effects and current ruler before applying',Alternative='Direct AUS integration needs explicit reassignment of pops/buildings/units and remains unapproved; unchanged LUX avoids new gameplay effects but retains political mismatch',Technical_Precondition='personal_union identifier exists; use established AUS country scope; preserve existing pacts; verify ruling dynasty/regime rather than silently changing them',Approval='PENDING_EXPLICIT_USER_APPROVAL',Applied='NO')]
save('MAP1C_APPROXIMATIONS_FOR_APPROVAL.csv',approx)

# Candidate worktree only: simulate removing accidental Git words, preserving AST meaning.
work=Path('C:/Users/simeo/.codex/worktrees/map-0-collaborator-integration/1776_Age_of_Revolutions_fork'); candidate=work/'common/history/states/00_states.txt'; raw=candidate.read_text(encoding='utf-8-sig')
needle='create_state = {git status\ngit fetch origin'; assert raw.count(needle)==1
clean=raw.replace(needle,'create_state = {',1)
def bare(ns): return [scalar(n.value) for n in walk(ns) if n.key=='' and scalar(n.value) in {'git','status','fetch','origin'}]
assert bare(parse(raw))==['git','status','git','fetch','origin']; assert not bare(parse(clean))
def stripped(ns):
    return [(n.key,n.op, stripped(n.value) if isinstance(n.value,list) else n.value) for n in ns if not(n.key=='' and not isinstance(n.value,list) and scalar(n.value) in {'git','status','fetch','origin'})]
assert stripped(parse(raw))==stripped(parse(clean))
(E/'BESSARABIA_CANDIDATE_ONLY_UNAPPLIED.patch').write_text(''.join(difflib.unified_diff(raw.splitlines(True),clean.splitlines(True),fromfile='candidate/common/history/states/00_states.txt',tofile='candidate/common/history/states/00_states.txt')),encoding='utf-8')
tech=[dict(Fix_ID='TECH-BESS-01',Target='Collaborator candidate ONLY',File=str(candidate),Province_RGB='Bessarabia RGBs unchanged',Current_Defect='Five bare tokens git status git fetch origin at lines 7679-7680',Proposed_Fix='Delete only accidental Git words; leave create_state braces, MOL owner, claim and homelands unchanged',Sovereignty_Change='NO',Readiness='READY_FOR_APPROVAL',Dependencies='No population/building/unit edit',Validation='In-memory AST equality after removing exact five tokens; primary file has no matching defect',Risk_Fallback='Patch restricted to candidate file hash; refuse if source changed; do not copy whole candidate over main',Approved='NO',Applied='NO'),
dict(Fix_ID='TECH-SIL-01',Target='Main working mod',File='common/history/states/00_states.txt',Province_RGB='x9061E0',Current_Defect='AUS ownership command under UPPER_SILESIA; physical definition WEST_GALICIA',Proposed_Fix='Move the existing AUS ownership reference to an AUS split under WEST_GALICIA; keep AUS. Do not replace GAL scope or move bitmap/state definition',Sovereignty_Change='NO',Readiness='CONDITIONAL_DEPENDENCY_AND_ENGINE_TEST',Dependencies='WEST_GALICIA currently GAL only; AUS split requires population/recruitment/ownership compatibility review; UPPER_SILESIA AUS remains with two disputed RGBs',Validation='Definition/history mismatch verified; future patch must retain multiset (RGB,owner), pops and all building/formation selectors',Risk_Fallback='Do not create an empty-populated split silently; alternative region-definition change itself changes gameplay and needs separate approval',Approved='NO',Applied='NO'),
dict(Fix_ID='TECH-SIL-02',Target='Main working mod',File='common/history/states/00_states.txt',Province_RGB='x71E080|xF0E080',Current_Defect='Both AUS and PRU references under UPPER_SILESIA but definition MORAVIA',Proposed_Fix='Prepare scope relocation independently; do NOT choose an owner or delete duplicate references until historical arbitration',Sovereignty_Change='NOT_ALLOWED_IN_TECHNICAL_FIX',Readiness='BLOCKED_BY_DUPLICATE_OWNER_AND_DEPENDENCIES',Dependencies='MORAVIA AUS exists but PRU split absent; contested populations cannot be derived from area',Validation='Both owners and wrong scope separately confirmed',Risk_Fallback='Leave unchanged until agreed owner and conservation manifest; scope fix alone would retain duplicate',Approved='NO',Applied='NO')]
save('MAP1C_TECHNICAL_FIXES.csv',tech)
candidates=[dict(Candidate_ID='IMPL-001',Linked_Decision='TECH-BESS-01',Type='SYNTAX_REPAIR_CANDIDATE_ONLY',Ready='YES_AFTER_USER_APPROVAL',Files='Collaborator candidate common/history/states/00_states.txt only',Owner_Change='NO',Exact_Action='Apply BESSARABIA_CANDIDATE_ONLY_UNAPPLIED.patch against recorded hash',Preconditions='Candidate hash matches; 5 tokens present; primary remains clean',Required_Test='AST semantic equality; no owner/pop/building delta; validate candidate parsing; no merge',Approval='PENDING',Applied='NO'),
dict(Candidate_ID='IMPL-002',Linked_Decision='LUX-POL-01',Type='POLITICAL_APPROXIMATION',Ready='CONDITIONAL_APPROVAL_AND_RULER_CHECK',Files='common/history/diplomacy/00_subject_relationships.txt',Owner_Change='NO_RGB_OWNER_CHANGE',Exact_Action='Add AUS -> LUX personal_union only, preserving all LUX records',Preconditions='Explicit APP-LUX-01 approval; review LUX ruler/regime and competing pacts',Required_Test='New game LUX subject; 137881 written population conserved; buildings and formations conserved; market/bloc behavior',Approval='PENDING',Applied='NO'),
dict(Candidate_ID='IMPL-003',Linked_Decision='TECH-SIL-01',Type='SCOPE_REPAIR_WITH_DEPENDENCY_RISK',Ready='NO_UNTIL_SPLIT_VALIDATION',Files='common/history/states/00_states.txt',Owner_Change='NO',Exact_Action='Relocate x9061E0 AUS reference without moving geography or assigning another owner',Preconditions='Approval + AUS WEST_GALICIA population/units/buildings selector compatibility',Required_Test='Same (RGB,owner) multiset; all state-country selectors still valid; new-game state not empty/orphaned',Approval='PENDING',Applied='NO')]
save('MAP1C_IMPLEMENTATION_CANDIDATES.csv',candidates)

impact={}
for sid in ['STATE_WALLONIA','STATE_LOMBARDY','STATE_UPPER_SILESIA','STATE_MORAVIA','STATE_WEST_GALICIA']:
    impact[sid]={'pops_written':[r for r in pops if r['State_ID']==sid], 'buildings_written':[r for r in buildings if r['State_ID']==sid], 'warning':'State-country data, NOT per-province allocations; duplicate building commands are not engine-effective level totals.'}
impact['LUX_COUNTRY']={'pops':luxpop,'buildings':luxbuild,'country_history':(ROOT/'common/history/countries/lux - luxemburg.txt').read_text(encoding='utf-8-sig'),'military_context':'common/history/military_formations/00_military_formations_europe.txt:2901; preserve complete LUX block','dependency_references':'../MAP1/MAP1_DEPENDENCY_REFERENCES.csv and STATE_WALLONIA.json'}
jsonout('DEPENDENCY_IMPACTS.json',impact)
urls={'cities1000.zip':'https://download.geonames.org/export/dump/cities1000.zip','geonames_readme.txt':'https://download.geonames.org/export/dump/readme.txt','ne_10m_lakes.geojson':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes.geojson','ne_10m_rivers.geojson':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines_scale_rank.geojson','naturalearth_lakes_notice.html':'https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-lakes/','lbc_grigioni.html':'https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.04'}
jsonout('SOURCE_LEDGER.json',[{'file':f,'url':u,'sha256':digest(E/f),'access_date':'2026-10-10','interpretation':'Modern geodetic reference only' if not f.startswith('lbc') else 'LOM-05 institutional history; not a game-province boundary'} for f,u in urls.items()])
gd=ROOT/'.git/worktrees/1776_Age_of_Revolutions_fork'
assert (ROOT/'.git/refs/heads/codex/map-0-collaborator-integration').read_text().strip()==before['HEAD']
assert (gd/'MERGE_HEAD').read_text().strip()=='0e018d9b292ec263d424500a47279d895cf1020a'
jsonout('BESSARABIA_SIMULATION_CHECK.json',{'candidate_sha256':digest(candidate),'tokens_removed':5,'ast_equal_except_exact_parasites':True,'runtime_applied':False,'patch':'BESSARABIA_CANDIDATE_ONLY_UNAPPLIED.patch','main_contains_parasites':needle in (ROOT/'common/history/states/00_states.txt').read_text(encoding='utf-8-sig'),'candidate_head':before['HEAD'],'candidate_merge_head':(gd/'MERGE_HEAD').read_text().strip(),'git_verification_method':'Read-only worktree HEAD pointer, branch ref and MERGE_HEAD; Git -C sandbox denied, no mutation'})
# Preserve all 1220 original MAP1 manifest entries and entire MAP1B as well as runtime.
original=table(OLD/'MAP1_DELIVERABLE_HASHES.csv')
for r in original: assert digest(OLD/r['File'])==r['SHA256'],r['File']
for f,sha in before['MAP1B'].items(): assert digest(ROOT/f)==sha,f
assert protected()==before['runtime']
assert digest(GAME/'map_data/provinces.png')==json.loads((OLD/'MAP1_GEOGRAPHIC_EVIDENCE/GEOMETRY_METADATA.json').read_text())['bitmap_sha256']
assert (ROOT/'.git/refs/heads/main').read_text().strip()==before['HEAD']
assert digest(candidate)=='d5a676c5bdc879bfe21e58536438691e1c7c320e7b79cb66fac034beeacc30a6'
assert (OUT/'MAP1C_EXECUTIVE_SUMMARY.md').exists()
assert (E/'METHOD_AND_EVIDENCE.md').exists()
assert len({r['Decision_ID'] for r in decisions})==len(decisions)
assert {r['Decision_Status'] for r in decisions}<={'HISTORICALLY_VERIFIED','DOCUMENTED_GAMEPLAY_APPROXIMATION','UNRESOLVED'}
for name in ['MAP1C_MAPPING_DECISIONS.csv','MAP1C_APPROXIMATIONS_FOR_APPROVAL.csv','MAP1C_TECHNICAL_FIXES.csv','MAP1C_IMPLEMENTATION_CANDIDATES.csv']:
    rr=table(OUT/name); assert all(r.get('Applied','NO')=='NO' for r in rr)
jsonout('VALIDATION.json',{'runtime_files_hash_equal':len(before['runtime']),'MAP1B_files_hash_equal':len(before['MAP1B']),'MAP1_manifest_hash_equal':len(original),'HEAD_unchanged':True,'candidate_file_HEAD_and_MERGE_HEAD_unchanged':True,'game_province_bitmap_hash_equal':True,'required_deliverables_present':True,'mapping_rows':len(decisions),'territorial_transfers_admitted':0,'historically_verified_province_transfers':0,'political_approximations_for_approval':len(approx),'technical_fixes_prepared':len(tech),'runtime_changes_applied':0,'game_engine_tests':'NOT_RUN_NO_RUNTIME_CHANGE','all_unfavorable_controls_retained':True})
print(json.dumps({'models':metrics,'decisions':len(decisions),'validation':'PASS'},ensure_ascii=False,indent=2))
