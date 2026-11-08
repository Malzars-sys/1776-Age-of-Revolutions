"""Scoped western Prussian frontier pass; preserve older immutable evidence."""
from pathlib import Path
import collections,hashlib,json,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import serg_closure_roadmap as roadmap

ROOT=Path(__file__).resolve().parents[1]
CANON=ROOT/'docs/reports/map/SERG_CLOSURE'
OUT=CANON/'PRUSSIAN_WEST_2026_11_05'
REGIONS={'STATE_RHINELAND','STATE_NORTH_RHINE','STATE_RUHR','STATE_WESTPHALIA','STATE_HANNOVER','STATE_GELRE','STATE_LIMBURG'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def runtime():return {p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','events','map_data','gfx','gui','localization'] for p in (ROOT/folder).rglob('*') if p.is_file()}
def capture():
    OUT.mkdir(exist_ok=True);assert not (OUT/'BASELINE.json').exists()
    assert roadmap.check()['status']=='PASS'
    git={}
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current']),('git_dir',['rev-parse','--absolute-git-dir']),('status',['status','--porcelain=v1'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True);git[name]=r.stdout.strip()
    git['index_sha256']=sha(Path(git['git_dir'])/'index')
    originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_bytes().decode('utf-8')
            if any(s in raw for s in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    names=['PRUSSIA_V1_2026_11_02','NORTH_SAXONY_1_2026_11_05','PRUSSIA_POLAND_2026_11_05','SILESIA_STATE_LAYOUT_COMPARISON_2026_11_05']
    protected={p.relative_to(ROOT).as_posix():sha(p) for name in names for p in (CANON/name).rglob('*') if p.is_file()}
    for folder in ['MINDEN_RAVENSBERG','RHINE_WESTPHALIA','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION']:
        for p in (ROOT/'docs/reports/map/MAP2L'/folder).rglob('*'):
            if p.is_file():protected[p.relative_to(ROOT).as_posix()]=sha(p)
    for name in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']:(OUT/('BEFORE_'+name)).write_bytes((CANON/name).read_bytes())
    (OUT/'provinces_before.png').write_bytes((ROOT/'map_data/provinces.png').read_bytes())
    dump('BASELINE.json',dict(runtime=runtime(),originals=originals,git=git,protected=protected,progress=roadmap.progress(roadmap.load_json(CANON/'ROADMAP_STATE.json')),inventory=qa.inventory()))
    print('Baseline captured; no functional writes')

def berg_geometry():
    """Conservative Berg interior agreed by both retained coarse native models."""
    from georeference.model import forward
    from map2l_franconia import inside
    from map2l_belgium import packed,components
    b=load('BASELINE.json');a=packed(OUT/'provinces_before.png')
    assert runtime()==b['runtime'],'Concurrent functional changes require reassessment'
    controls=[('Dusseldorf',668,420,6.773,51.227),('Cologne',782,600,6.96,50.938),('Bonn',828,755,7.099,50.738),('Julich',571,587,6.355,50.922)]
    source_to_geo=np.linalg.lstsq(np.array([[x,y,1] for _,x,y,_,_ in controls]),np.array([[lon,lat] for _,_,_,lon,lat in controls]),rcond=None)[0]
    # Interior of the named duchy, not a claim to its entire outer boundary.
    # Homburg/Gimborn and the eastern Windeck fringe are deliberately excluded.
    outline=[(730,400),(790,410),(830,430),(880,470),(930,515),(975,570),(985,615),(967,652),(975,690),(950,717),(905,719),(865,686),(840,650),(825,610),(805,565),(760,525),(735,475),(700,430)]
    geo=np.c_[outline,np.ones(len(outline))]@source_to_geo
    axes=np.array(json.loads((ROOT/'docs/reports/map/MAP2M/R5/TRANSFORMATIONS.json').read_text())['selected_native']['matrix'])
    miller=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    polygons=[np.c_[geo,np.ones(len(geo))]@axes,forward(miller,geo)]
    yy,xx=np.mgrid[795:850,4230:4295];pts=np.c_[(xx+.5).ravel(),(yy+.5).ravel()]
    masks=[inside(pts,poly).reshape(xx.shape) for poly in polygons]
    agreed=masks[0]&masks[1]
    scoped={r['key'][0] for r in b['inventory']['owners'] if r['key'][1] in {'STATE_RUHR','STATE_NORTH_RHINE'} and r['key'][2]=='PRU'}
    agreed &= np.isin(a[795:850,4230:4295],[int(s[1:],16) for s in scoped])
    for part in components(agreed):
        if len(part)<3:
            for y,x in part:agreed[y,x]=False
    selected=np.zeros(a.shape,dtype=bool);selected[795:850,4230:4295]=agreed
    tracing=dict(source='docs/reports/map/MAP2L/RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg',source_sha256=sha(ROOT/'docs/reports/map/MAP2L/RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg'),controls=controls,source_to_geo_matrix=source_to_geo.tolist(),source_outline=outline,native_outlines=[poly.tolist() for poly in polygons],models=['MAP2M/R5 geographic_axes','MAP2L/GEOREFERENCE_PROTOTYPE miller_affine'],source_to_geo_residual_degrees=np.linalg.norm(np.array([[x,y,1] for _,x,y,_,_ in controls])@source_to_geo-np.array([[lon,lat] for _,_,_,lon,lat in controls]),axis=1).tolist(),native_models_refitted=False,source_edition=1777,underlying_map_date=1753,classification='UNINSTALLED_BERG_INTERIOR_HYPOTHESES',warning='Both native models are empirical and extrapolated here. Their agreement would not itself prove a cadastral frontier. No Homburg/Gimborn, imperial-city or 1815 expansion inferred.')
    dump('TRACING.json',tracing)
    im=Image.open(ROOT/tracing['source']).convert('RGB');d=ImageDraw.Draw(im);d.line(outline+[outline[0]],fill='blue',width=4)
    for name,x,y,_,_ in controls:d.ellipse((x-4,y-4,x+4,y+4),fill='red');d.text((x+5,y),name,fill='black',stroke_width=1,stroke_fill='white')
    im.crop((500,300,1120,850)).resize((1240,1100)).save(OUT/'BERG_SOURCE_REVIEW.jpg')
    ownership={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    hypotheses=[];panels=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for title,mask in zip(['R5_GEOGRAPHIC_AXES','MILLER_AFFINE'],masks):
        eligible=mask&np.isin(a[795:850,4230:4295],[int(s[1:],16) for s in scoped])
        ys,xs=np.where(eligible);cells=[[int(x+4230),int(y+795)] for y,x in zip(ys,xs)]
        occupants=collections.Counter()
        for value in np.unique(a[795:850,4230:4295][mask]):
            occupants[ownership.get('x'+format(int(value),'06X'),'?')]+=int(((a[795:850,4230:4295]==value)&mask).sum())
        hypotheses.append(dict(model=title,proposed_pru_to_kpf_cells=cells,count=len(cells),all_interior_owners=dict(occupants),installed=False))
        local=a[795:850,4230:4295];canvas=np.full((*local.shape,3),225,dtype=np.uint8)
        colors={'PRU':(100,150,205),'KPF':(190,180,100),'KCL':(205,145,185),'WPM':(105,175,105),'WPD':(220,150,105),'BEO':(245,210,90),'NET':(240,175,90)}
        for v in np.unique(local):canvas[local==v]=colors.get(ownership.get('x'+format(int(v),'06X')),(200,200,200))
        canvas[eligible]=(245,40,80);im=Image.fromarray(canvas).resize((780,660),Image.Resampling.NEAREST)
        panel=Image.new('RGB',(780,720),'white');panel.paste(im,(0,45));dd=ImageDraw.Draw(panel);dd.text((8,10),title+' : HYPOTHESE NON INSTALLEE',font=font,fill='black');dd.text((8,703),'Rose vif : portion PRU proposee vers KPF ; autres couleurs : actuel.',font=font,fill='black');panels.append(panel)
    joined=Image.new('RGB',(1560,720),'white');joined.paste(panels[0]);joined.paste(panels[1],(780,0));joined.save(OUT/'HYPOTHESES_NOT_INSTALLED.png')
    dump('BERG_HYPOTHESES.json',dict(status='NO_GO_NATIVE_CORRESPONDENCE',hypotheses=hypotheses,common_eligible_cells=int(selected.sum()),territory_complete=False,functional_changes=0,decision='Do not choose a native projection solely to force an installation; no cadastral conclusion. A user-approved political B layout with concrete cells would be a separate scoped decision.'))
    if not selected.any():
        print('NO-GO: no common eligible core;',[(r['model'],r['count']) for r in hypotheses]);return
    current_owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    after=a.copy();assignments=[];new=[];idx=0xEEC300
    for value in sorted(np.unique(a[selected])):
        parent='x'+format(int(value),'06X');sid,owner=current_owners[parent]
        moved=(a==value)&selected;remaining=(a==value)&~selected
        assert owner=='PRU' and remaining.any()
        assert not (a==idx).any();child='x'+format(idx,'06X');after[moved]=idx;idx+=1
        new.append(dict(rgb=child,parent_rgb=parent))
        for rgb,tag,mask in [(parent,'PRU',remaining),(child,'KPF',moved)]:
            ys,xs=np.where(mask)
            assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=owner,owner=tag,pixels=len(xs),cells=[[int(x),int(y)] for y,x in zip(ys,xs)]))
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=-1).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(classification='B_CONSERVATIVE_BERG_INTERIOR',historical_cadastral_precision=False,parents=sorted({r['parent_rgb'] for r in assignments}),assignments=assignments,new_provinces=new,hub_rebindings=[],candidate_sha256=sha(OUT/'provinces_candidate.png'),ownership_cells=int(selected.sum()),changed_pixels=int((a!=after).sum()),selected_option='INTERSECTION_OF_TWO_RETAINED_NATIVE_MODELS',not_a_complete_western_frontier=True))
    dump('TRACING.json',dict(source='docs/reports/map/MAP2L/RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg',source_sha256=sha(ROOT/'docs/reports/map/MAP2L/RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg'),controls=controls,source_to_geo_matrix=source_to_geo.tolist(),source_outline=outline,native_outlines=[poly.tolist() for poly in polygons],models=['MAP2M/R5 geographic_axes','MAP2L/GEOREFERENCE_PROTOTYPE miller_affine'],source_to_geo_residual_degrees=np.linalg.norm(np.array([[x,y,1] for _,x,y,_,_ in controls])@source_to_geo-np.array([[lon,lat] for _,_,_,lon,lat in controls]),axis=1).tolist(),native_models_refitted=False,source_edition=1777,underlying_map_date=1753,classification='B_CONSERVATIVE_BERG_INTERIOR',warning='Both native models are empirical and extrapolated here. Their intersection is a conservative choice, not an independent accuracy certificate or a cadastral frontier. Only the named Berg mainland interior changes; no Homburg/Gimborn, imperial-city or 1815 expansion inferred.'))
    im=Image.open(ROOT/'docs/reports/map/MAP2L/RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg').convert('RGB');d=ImageDraw.Draw(im);d.line(outline+[outline[0]],fill='blue',width=4)
    for name,x,y,_,_ in controls:d.ellipse((x-4,y-4,x+4,y+4),fill='red');d.text((x+5,y),name,fill='black',stroke_width=1,stroke_fill='white')
    im.crop((500,300,1120,850)).resize((1240,1100)).save(OUT/'BERG_SOURCE_REVIEW.jpg')
    print('Berg common interior:',selected.sum(),'cells;',[(r['rgb'],r['pixels']) for r in assignments if r['owner']=='KPF'])

def conservation():
    b=load('BASELINE.json');checks=[]
    def ck(name,ok):checks.append(dict(name=name,status='PASS' if ok else 'FAIL'))
    ck('all_functional_files_byte_identical',runtime()==b['runtime'])
    ck('all_protected_previous_evidence_identical',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in b['protected'].items()))
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        r=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True)
        ck('git_'+name+'_unchanged',r.stdout.strip()==b['git'][name])
    ck('git_index_unchanged',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    ck('no_gameplay_candidate_or_installation',not (OUT/'provinces_candidate.png').exists() and not (OUT/'INSTALLATION.json').exists())
    hypotheses=load('BERG_HYPOTHESES.json')
    ck('hypotheses_explicitly_rejected',hypotheses['status']=='NO_GO_NATIVE_CORRESPONDENCE' and hypotheses['common_eligible_cells']==0 and all(not x['installed'] for x in hypotheses['hypotheses']))
    ck('r5_core_already_palatin',hypotheses['hypotheses'][0]['all_interior_owners']=={'KPF':151} and hypotheses['hypotheses'][0]['count']==0)
    ck('miller_39_cells_only_hypothetical',hypotheses['hypotheses'][1]['count']==39)
    ck('native_models_not_refitted',load('TRACING.json')['native_models_refitted'] is False)
    result=dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),functional_files=len(b['runtime']),new_runtime_tests=0,new_human_receipts=0,scope='Conservation and truthful diagnostic outputs, not territorial acceptance')
    dump('CONSERVATION_PRE_TRACKING.json',result);assert result['status']=='PASS',result
    print('Conservation',result['passed'],'/',result['total'])

def tracker():
    import copy
    assert load('CONSERVATION_PRE_TRACKING.json')['status']=='PASS'
    old=load('BEFORE_ROADMAP_STATE.json');current=roadmap.load_json(CANON/'ROADMAP_STATE.json')
    assert current==old,'Concurrent tracking change; reassess'
    state=copy.deepcopy(current);state['mission_status']='PRUSSIAN_WEST_BLOCKED_PREVIOUS_PRUSSIAN_INSTALLATIONS_PENDING_RUNTIME';ref=OUT.relative_to(ROOT).as_posix();task=next(t for t in state['tasks'] if t['id']=='SC5-PRUSSIAN-WEST')
    assert task['status']=='NOT_STARTED' and task['priority']=='P1' and not task['depends_on']
    task.update(status='BLOCKED',implementation_report=[ref+'/REPORT.md'],
        static_tests=dict(status='PASS',evidence=[ref+'/CONSERVATION_PRE_TRACKING.json',ref+'/BERG_HYPOTHESES.json']),
        blocking_reason='Correspondance native non résolue : même intérieur bergien = 151 cellules déjà KPF sous R5, mais 39 cellules PRU proposées sous Miller. Aucun transfert commun et aucune correction indépendante démontrée ; Gueldre et Ravensberg non homologuées.',
        current_delivery_note='Passe documentaire achevée, cartes de Ravensberg 1772 et Clèves/Gueldre/Mark 1793 obtenues et lues ; aucune installation ni validation humaine.',
        residual_uncertainty='Deux modèles empiriques utilisés hors domaine, désaccord d’environ dix cellules ; ni le maintien actuel ni les 39 cellules hypothétiques ne certifient les frontières. Ne pas transformer une étude sans installation en décision NA.',
        investigation_status='COMPLETED_NO_FUNCTIONAL_INSTALLATION',
        next_bounded_action='Résoudre la correspondance locale par repères physiques indépendants ou arbitrage politique B explicite sur un candidat concret ; ne pas répéter les anciens ajustements ni installer les 39 cellules par défaut.')
    task['historical_sources'] += [ref+'/SOURCES.md']
    focus=state['release_focus'];focus.update(current_pass='PRUSSIAN_WEST',current_pass_status='BLOCKED_NO_FUNCTIONAL_INSTALLATION',current_delivery=ref+'/REPORT.md',continuation_authority='Utilisateur : Ok, vas-y après désignation de SC5-PRUSSIAN-WEST ; puis fini.',next_requested_pass=None,next_pass_started=False)
    before=roadmap.progress(current);after=roadmap.progress(state)
    assert (before['earned_weight'],before['percent'],before['qualified_tasks'])==(after['earned_weight'],after['percent'],after['qualified_tasks'])==(93,'39.57',32)
    assert state['events'][-1]['id']=='SERG-RM-0064'
    state['events'].append(dict(id='SERG-RM-0065',date='2026-11-05',kind='PRUSSIAN_WEST_NATIVE_CORRESPONDENCE_BLOCKED',scope_version='1.0.0',source=ref+'/REPORT.md',changes=[dict(task_id=task['id'],before='NOT_STARTED',after='BLOCKED')],before_weight=93,after_weight=93,total_weight=235,before_percent='39.57',after_percent='39.57',note='Sources 1772 et 1793 obtenues, intérieur de Berg comparé sans modifier les modèles. R5 : 151 cellules déjà KPF ; Miller : 39 cellules PRU hypothétiques. Aucun correctif indépendant démontré ; aucune installation, attestation ou point. Minden, Lingen, Tecklenburg et les trois livraisons prussiennes conservés.',evidence=[ref+'/SOURCES.md',ref+'/BERG_HYPOTHESES.json',ref+'/CONSERVATION_PRE_TRACKING.json',ref+'/PLAYER_TEST_PROTOCOL.md']))
    assert (CANON/'ROADMAP_STATE.json').read_bytes()==(OUT/'BEFORE_ROADMAP_STATE.json').read_bytes()
    roadmap.write_json(CANON/'ROADMAP_STATE.json',state)
    intro='''## Prusse occidentale — 5 novembre 2026, passe achevée sans installation

`SC5-PRUSSIAN-WEST` : **BLOCKED P1**. Cartes de Ravensberg 1772 et de Clèves/Gueldre/Mark 1793 obtenues et lues. Le même intérieur de Berg couvre 151 cellules déjà KPF sous l'hypothèse R5, mais propose 39 cellules PRU sous Miller : aucune correction indépendante démontrée, aucun transfert commun. Aucun ancien modèle refait, aucun fichier fonctionnel modifié. [Rapport et preuves](PRUSSIAN_WEST_2026_11_05/REPORT.md).

**93/235 = 39,57 %, 32/81**, aucun reçu ni point nouveau. Les noyaux validés et les installations prussiennes antérieures sont conservés. Action immédiate : [test joueur groupé prussien existant](PRUSSIA_POLAND_2026_11_05/PLAYER_TEST_PROTOCOL.md). L'ouest nécessite une correspondance locale défendable ou un arbitrage politique B concret ; les 39 cellules ne sont pas recommandées pour installation immédiate. Aucun nouveau territoire, micro-État ou lot bavarois commencé. Les encadrés antérieurs ci-dessous restent archivés dans leur contexte.

'''
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        prior=(OUT/('BEFORE_'+name)).read_bytes();assert (CANON/name).read_bytes()==prior,'Concurrent '+name
        head,body=prior.split(b'\n',1)
        if name=='ROADMAP.md':
            text=body.decode('utf-8');start=text.index('#### SC5-PRUSSIAN-WEST');end=text.index('#### SC5-JEVER',start)
            section=text[start:end];assert section.count('`NOT_STARTED`')==1
            text=text[:start]+section.replace('`NOT_STARTED`','`BLOCKED`')+text[end:];body=text.encode('utf-8')
        if name=='BLOCKERS.md':
            text=body.decode('utf-8');assert text.count('Tâches : SC5-PRUSSIAN-WEST `NOT_STARTED`.')==1
            body=text.replace('Tâches : SC5-PRUSSIAN-WEST `NOT_STARTED`.','Tâches : SC5-PRUSSIAN-WEST `BLOCKED`. Correspondance native non résolue ; voir la passe PRUSSIAN_WEST_2026_11_05, aucune correction installée.').encode('utf-8')
        (CANON/name).write_bytes(head+b'\n\n'+intro.encode('utf-8')+body)
    prior=(OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes();assert (CANON/'PROGRESS_HISTORY.md').read_bytes()==prior
    addition='''

## SERG-RM-0065 — 5 novembre 2026 — Prusse occidentale, correspondance bloquée

SC5-PRUSSIAN-WEST NOT_STARTED→BLOCKED P1. Carte primaire Ravensberg 1772 et feuille Clèves/Gueldre/Mark 1793 obtenues et lues. Intérieur de Berg : 151 cellules déjà KPF selon R5, 39 cellules PRU hypothétiques selon Miller ; aucun transfert commun ni correction indépendante démontrée. Première génération arrêtée avant candidat ; export documentaire ultérieur NO-GO, aucun ajustement des anciens modèles. Aucun fichier fonctionnel, reçu ou point nouveau. Toutes les anciennes installations et 80 autres tâches conservées ; 93/235, 39,57 %, 32/81. Test joueur groupé prussien toujours attendu ; aucune Bavière ou autre tâche commencée. [Rapport](PRUSSIAN_WEST_2026_11_05/REPORT.md).
'''
    (CANON/'PROGRESS_HISTORY.md').write_bytes(prior+addition.encode('utf-8'))
    assert (CANON/'PROGRESS_SNAPSHOT.json').read_bytes()==(OUT/'BEFORE_PROGRESS_SNAPSHOT.json').read_bytes()
    roadmap.write_json(CANON/'PROGRESS_SNAPSHOT.json',roadmap.progress(state))
    print('Tracking updated: BLOCKED P1, 93/235 = 39.57%')

def finalize():
    conservation();old=load('BEFORE_ROADMAP_STATE.json');s=roadmap.load_json(CANON/'ROADMAP_STATE.json');checks=[]
    def ck(name,ok):checks.append(dict(name=name,status='PASS' if ok else 'FAIL'))
    ck('functional_conservation',load('CONSERVATION_PRE_TRACKING.json')['status']=='PASS')
    ck('81_tasks_235_points',(len(s['tasks']),sum(t['weight'] for t in s['tasks']))==(81,235))
    target='SC5-PRUSSIAN-WEST';task=next(t for t in s['tasks'] if t['id']==target);prior_task=next(t for t in old['tasks'] if t['id']==target)
    ck('80_other_task_records_unchanged',[t for t in s['tasks'] if t['id']!=target]==[t for t in old['tasks'] if t['id']!=target])
    ck('target_blocked_without_receipt',task['status']=='BLOCKED' and task['runtime_validation']==prior_task['runtime_validation'] and task['decision'] is None and not task['installed_lots'])
    fields=['id','weight','priority','depends_on','acceptance']
    ck('scope_weights_dependencies_acceptance_preserved',all({k:t[k] for k in fields}=={k:o[k] for k in fields} for t,o in zip(s['tasks'],old['tasks'])))
    ck('previous_events_identical',s['events'][:-1]==old['events'] and s['events'][-1]['id']=='SERG-RM-0065')
    ck('runtime_protocol_and_external_deliveries_preserved',all(s[k]==old[k] for k in ['runtime_validation_hold','external_prussian_deliveries','prussian_silesia_comparison','closure_approval','source_manifest']))
    ck('history_additive',(CANON/'PROGRESS_HISTORY.md').read_bytes().startswith((OUT/'BEFORE_PROGRESS_HISTORY.md').read_bytes()))
    p=roadmap.progress(s);ck('no_earned_credit',(p['earned_weight'],p['qualified_tasks'],p['total_weight'],p['percent'])==(93,32,235,'39.57'))
    result=roadmap.check();dump('CANONICAL_CHECK.json',result);ck('canonical_validator',result['status']=='PASS')
    cmd=['git','--no-optional-locks','diff','--check','--','tools/serg_prussian_west.py',*[str((CANON/name).relative_to(ROOT)) for name in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]]
    r=subprocess.run(cmd,capture_output=True,text=True);dump('DIFF_CHECK.json',dict(command=cmd,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr));ck('diff_check',r.returncode==0)
    dump('FINAL_CHECKS.json',dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),functional_changes=0,new_human_receipts=0,engine_test=False,progress=p))
    print('Final checks',len(checks),[c for c in checks if c['status']!='PASS']);assert all(c['status']=='PASS' for c in checks)

if __name__=='__main__':{'capture':capture,'geometry':berg_geometry,'conservation':conservation,'tracker':tracker,'finalize':finalize}[sys.argv[1]]()
