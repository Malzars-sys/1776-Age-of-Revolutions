"""R1 scoped human receipt, then a separate current-workspace technical wave."""
import collections as C,contextlib,copy,csv,io,json,os,re,subprocess,sys,unittest
from pathlib import Path
import audit_starting_tech_1776 as r1
ROOT=r1.ROOT;GAME=r1.GAME;qa=r1.qa;cw=r1.cw;rm=r1.rm;sha=r1.sha;load=r1.load
OUT=ROOT/'docs/reports/technology/STARTING_TECH_AUDIT_1776_R2'
SOURCE=Path('C:/Users/simeo/.codex/attachments/cb669bee-a6ca-48c5-9821-21990ceb90d9/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def dump(n,o):r1path=OUT/n;r1path.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def csvout(n,rows,fields=None):
    with (OUT/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def receipt():
    assert not (OUT/'ENTRY.json').exists();OUT.mkdir(exist_ok=True)
    files=load(r1.OUT/'FILES_MODIFIED.json');cur=r1.runtime.runtime_hashes();old=load(r1.OUT/'DELIVERY_MANIFEST.json')['files']
    changed=[p for p,h in old.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    scope={rel:dict(delivered=h,current=sha(ROOT/rel),matches=sha(ROOT/rel)==h) for rel,h in files['sha256'].items()}
    assert all(d['matches'] for d in scope.values()),scope
    originalproofs={p.relative_to(ROOT).as_posix():sha(p) for p in r1.OUT.rglob('*') if p.is_file()}
    state=load(r1.OUT/'AUDIT_STATE.json');assert state['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    dump('ENTRY.json',dict(runtime_hashes=cur,r1_proofs=originalproofs,r1_state=state,r1_manifest_changes=changed,r1_scope_comparison=scope,territorial_state=load(rm.OUT/'ROADMAP_STATE.json'),date_recorded='2026-10-24'))
    (OUT/'USER_MISSION.txt').write_bytes(SOURCE.read_bytes())
    (r1.OUT/'USER_VALIDATION_TECH_R1_2026_10_24.txt').write_bytes(SOURCE.read_bytes())
    receiptname='RUNTIME_USER_ATTESTATION_2026_10_24.json';assert not (r1.OUT/receiptname).exists()
    r=dict(status='PASS_RUNTIME_USER_VALIDATED',scope_type='TECH_R1_CORRECTIONS_AND_BGT_MINE_ONLY',delivery='STARTING_TECH_AUDIT_1776_R1',recorded_on='2026-10-24',actual_test_date=None,source=(r1.OUT/'USER_VALIDATION_TECH_R1_2026_10_24.txt').relative_to(ROOT).as_posix(),protocol=(r1.OUT/'PLAYER_TEST_PROTOCOL.md').relative_to(ROOT).as_posix(),protocol_confirmed_as_whole=True,corrected_tags=list(r1.ASSIGNMENTS),counts={row['TAG']:[int(row['Before_Count']),int(row['After_Count'])] for row in csv.DictReader((r1.OUT/'STARTING_TECH_BEFORE_AFTER.csv').open(encoding='utf-8-sig',newline=''))},country_tech_additions=28,tested_functional_files=files['sha256'],delivery_manifest_sha256=sha(r1.OUT/'DELIVERY_MANIFEST.json'),explicitly_reported=['Nouvelle partie au 1er janvier 1776','Huit corrections et technologies attendues fonctionnelles','Technologies et méthodes contrôlées fonctionnelles','Mine native de sel BGT fonctionnelle','Recrutement, intrants, production et finances sans anomalie bloquante pendant le protocole','Pays témoins contrôlés sans anomalie','Aucun octroi technologique supplémentaire inattendu constaté','Un mois complet réussi','Sauvegarde et rechargement réussis'],new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,bgt_mine=dict(building='building_salt_mine',level=1,nominal_jobs=5000,ownership='public',data_reporting='pm_1776_no_raw_data_reporting',version='TECH_R1_NATIVE_MINE_CONFIGURATION'),automated_engine_test=False,additional_observations_invented=False,world_audit_complete=False,serg_closure_approved=False,excludes=['Toute modification R2 ou postérieure','Exactitude historique des 470 profils','Résolution des 207 signalements et 16 avertissements','Validation RG-D-CITY','Clôture territoriale SERG ou WORLD'])
    (r1.OUT/receiptname).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    state.update(status='PASS_RUNTIME_USER_VALIDATED',runtime_validation=dict(status='PASS_RUNTIME_USER_VALIDATED',attestation=receiptname,protocol='PLAYER_TEST_PROTOCOL.md',scope='Eight TECH-R1 corrections and exact TECH-R1 BGT native mine only; all later revisions excluded'),global_audit_status='OPEN_FINDINGS_REMAIN')
    (r1.OUT/'AUDIT_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (r1.OUT/'ACCEPTANCE_2026_10_24.md').write_text('# R1 — validation humaine bornée\n\nPASS_RUNTIME_USER_VALIDATED pour les huit corrections (28 ajouts) et la configuration TECH-R1 de la mine native BGT. Le joueur confirme le protocole complet, un mois et la sauvegarde/rechargement. Aucune date effective de test, capture, valeur d’emploi ou mesure économique inventée. Trois fichiers fonctionnels identiques à la livraison R1 lors de l’enregistrement. Audit mondial encore ouvert ; aucune couverture de R2, de RG-D-CITY ou des régions SERG/WORLD. Rapports originaux et manifestes de livraison conservés comme preuves datées ; seule la vue AUDIT_STATE est actualisée.\n',encoding='utf8')
    dump('R1_ACCEPTANCE_CHECK.json',dict(status='PASS',functional_files=scope,original_delivery_manifest_changes=changed,all_old_r1_proofs_preserved_except_state=all(sha(ROOT/p)==h for p,h in originalproofs.items() if p!=(r1.OUT/'AUDIT_STATE.json').relative_to(ROOT).as_posix()),receipt=receiptname,serg_unchanged=load(rm.OUT/'ROADMAP_STATE.json')==load(OUT/'ENTRY.json')['territorial_state'],automated_engine_test=False))
    print('R1 receipt recorded for eight corrections and exact BGT mine; three functional hashes match. Prior delivery differences:',changed,flush=True)

def capture():
    assert load(OUT/'R1_ACCEPTANCE_CHECK.json')['status']=='PASS' and not (OUT/'BASELINE.json').exists()
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    proofs={p.relative_to(ROOT).as_posix():sha(p) for p in r1.OUT.rglob('*') if p.is_file()}
    protected={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file()}
    # WORLD report names are not assumed; all existing map-report text/JSON/CSV
    # tracking is captured read-only and can only be changed by its own agent.
    world={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'docs/reports/map').rglob('*') if p.is_file() and ('WORLD' in p.as_posix().upper()) and p.suffix.lower() in {'.json','.md','.csv','.txt'}}
    inv=qa.inventory();current=r1.runtime.runtime_hashes()
    dump('BASELINE.json',dict(inventory=inv,hashes=current,r1_proofs=proofs,serg_proofs=protected,world_tracking=world,serg_state=load(rm.OUT/'ROADMAP_STATE.json'),tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    old=r1.OUT
    try:
        r1.OUT=OUT
        with contextlib.redirect_stdout(io.StringIO()):r1.inspect()
    finally:r1.OUT=old
    finish_capture()

def finish_capture():
    assert (OUT/'BASELINE.json').exists() and not (OUT/'CURRENT_BEFORE.json').exists()
    (OUT/'CURRENT_BEFORE.json').write_bytes((OUT/'RESOLVED_AFTER.json').read_bytes())
    evidence=[]
    for name in ['STARTING_TECH_AUDIT_1776.csv','STARTING_TECH_BEFORE_AFTER.csv','BUILDING_TECH_CONFLICTS.csv','COUNTRIES_REQUIRING_REVIEW.csv']:
        with (r1.OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        evidence.append(dict(file=name,rows=len(rows),sha256=sha(r1.OUT/name)))
    dump('MANDATORY_R1_READING.json',dict(csv_files=evidence,documents=[dict(file=n,sha256=sha(r1.OUT/n)) for n in ['TECH_VALIDATION.json','SOURCES_AND_DECISIONS.md','REPORT.md','PLAYER_TEST_PROTOCOL.md']],scripts_read=['tools/audit_starting_tech_1776.py','tools/test_starting_tech_audit_1776.py']))
    print('Current baseline captured after R1 acceptance:',len(load(OUT/'CURRENT_BEFORE.json')['active_tags']),'countries; SERG/WORLD read only',flush=True)

def placements():
    result=[]
    for order,p in enumerate(r1.effective('common/history/buildings')):
        raw=p.read_text(encoding='utf-8-sig')
        for root in cw.parse(raw):
            for state in root.children():
                if not state.key.startswith('s:STATE_'):continue
                for country in state.children():
                    if not country.key.startswith('region_state:'):continue
                    for n in country.children('create_building'):
                        kind=r1.val(n,'building');result.append(dict(state=state.key[2:],tag=country.key.split(':',1)[1],building=kind,methods=r1.values(n,'activate_production_methods'),file=r1.ref(p),line=raw[:n.start].count('\n')+1,order=order,node=n,raw=raw,path=p))
    return result

def reconcile():
    current=load(OUT/'CURRENT_BEFORE.json');techs={tag:set(s['technologies']) for tag,s in current['starts'].items()};buildings,_,_=r1.objects('common/buildings');pms,_,_=r1.objects('common/production_methods');groups,_,_=r1.objects('common/production_method_groups');rows=placements();final={};bykey=C.defaultdict(list)
    for row in rows:
        key=(row['state'],row['tag'],row['building']);bykey[key].append(row)
        selection=final.setdefault(key,{})
        for pm in row['methods']:
            if row['building'] not in buildings:continue
            matching=[g for g in r1.values(buildings[row['building']],'production_method_groups') if g in groups and pm in r1.values(groups[g],'production_methods')]
            for group in matching:selection[group]=dict(pm=pm,file=row['file'],line=row['line'])
    with (r1.OUT/'BUILDING_TECH_CONFLICTS.csv').open(encoding='utf-8-sig',newline='') as f:old=list(csv.DictReader(f))
    matrix=[]
    for i,c in enumerate(old,1):
        key=(c['State'],c['TAG'],c['Building']);selected=final.get(key,{})
        row=dict(ID='TECH-R2-'+str(i).zfill(3),TAG=c['TAG'],State=c['State'],Building=c['Building'],Object=c['Object'],R1_Kind=c['Kind'],R1_Missing=c['Missing'],Priority='',Conclusion='',Evidence='',Engine_Run=False,Selected_PM='',Current_Missing='',Compatible_Alternatives='',Action='')
        if c['Kind']=='RESOURCE_OR_PM_CONFLICT':row.update(Priority='P3',Conclusion='RESOURCE_ALLOCATION_REQUIRES_OWNING_TERRITORIAL_AGENT',Evidence='Regional template warning is not proof of missing owner-portion resource; no resource or territory edits allowed.',Action='DOCUMENT_HANDOFF_ONLY')
        elif c['Scope']=='INITIAL_BUILDING_CONSTRUCTION_GATE':
            missing=set(r1.values(buildings[c['Building']],'unlocking_technologies'))-techs.get(c['TAG'],set())
            row.update(Current_Missing=';'.join(sorted(missing)),Priority='P1' if missing else 'P4',Conclusion='CONSTRUCTION_GATE_ONLY_NOT_PROOF_OF_NO_PRODUCTION' if missing else 'ALREADY_SATISFIED',Evidence='Existing historical building declaration; rebuilding gate differs from operation. '+str(len(bykey[key]))+' declaration(s).',Action='REVIEW_HISTORICAL_BUILDING_OR_GATE' if missing else 'NO_CHANGE')
        else:
            owning_groups=[g for g in r1.values(buildings[c['Building']],'production_method_groups') if g in groups and c['Object'] in r1.values(groups[g],'production_methods')]
            active=[selected[g] for g in owning_groups if g in selected]
            row['Selected_PM']=';'.join(a['pm'] for a in active)
            missing=set(r1.values(pms[c['Object']],'unlocking_technologies'))-techs.get(c['TAG'],set()) if c['Object'] in pms else {'UNKNOWN_PM'}
            alternatives=sorted({pm for group in owning_groups for pm in r1.values(groups[group],'production_methods') if pm in pms and not(set(r1.values(pms[pm],'unlocking_technologies'))-techs.get(c['TAG'],set()))})
            row.update(Current_Missing=';'.join(sorted(missing)),Compatible_Alternatives=';'.join(alternatives))
            if not missing:row.update(Priority='P4',Conclusion='ALREADY_SATISFIED',Evidence='Current country knowledge satisfies this PM.',Action='NO_CHANGE')
            elif c['Object'] not in [a['pm'] for a in active]:row.update(Priority='P4',Conclusion='SUPERSEDED_DECLARATION_IN_ORDERED_HISTORY_MODEL',Evidence=json.dumps(active,ensure_ascii=False),Action='NO_CHANGE; final engine selection remains a runtime observation')
            else:row.update(Priority='P0',Conclusion='SELECTED_PM_WITH_UNSATISFIED_UNLOCK_GATE',Evidence=json.dumps(active,ensure_ascii=False)+'; construction/PM gates read from current definitions, not assumed from GDP.',Action='SELECT_EVIDENCED_OLDER_COMPATIBLE_PM' if alternatives else 'REVIEW_NO_COMPATIBLE_METHOD')
        matrix.append(row)
    csvout('PRIORITY_MATRIX.csv',matrix);csvout('CONFIRMED_TECH_CONFLICTS.csv',[r for r in matrix if r['Conclusion']=='SELECTED_PM_WITH_UNSATISFIED_UNLOCK_GATE'])
    dump('ORDERED_PM_MODEL.json',dict(assumption='Effective history files by filename; last explicit method per production group. Static reconstruction, not a certified engine execution trace.',selected=[dict(state=k[0],tag=k[1],building=k[2],groups=v) for k,v in final.items()]))
    print('Reevaluated',len(matrix),'signals; priorities',dict(C.Counter(r['Priority'] for r in matrix)),'conclusions',dict(C.Counter(r['Conclusion'] for r in matrix)),flush=True)
    print('Selected PM conflicts:',dict(C.Counter(r['Object'] for r in matrix if r['Priority']=='P0')),flush=True)

PM_PLAN=[
 ('R2-A','RUS','STATE_BREST','building_logging_camp','pm_saw_mills','pm_simple_forestry'),
 ('R2-A','GEN','STATE_PIEDMONT','building_furniture_manufactory','pm_lathe','pm_handcrafted_furniture'),
 ('R2-A','GEN','STATE_PIEDMONT','building_logging_camp','pm_saw_mills','pm_simple_forestry'),
 ('R2-A','GEN','STATE_PIEDMONT','building_tooling_workshop','pm_pig_iron','pm_crude_tools'),
 ('R2-A','VEN','STATE_ISTRIA','building_tooling_workshop','pm_pig_iron','pm_crude_tools'),
 ('R2-B','KND','STATE_CEYLON','building_government_administration','pm_horizontal_drawer_cabinets','pm_simple_organization'),
 ('R2-B','VEN','STATE_VENETIA','building_government_administration','pm_horizontal_drawer_cabinets','pm_simple_organization'),
 ('R2-B','KND','STATE_CEYLON','building_railway','pm_industrial_canals','pm_no_canal_network'),
 ('R2-B','BIK','STATE_RAJPUTANA','building_textile_mill','pm_craftsman_sewing','pm_no_luxury_clothes'),
 ('R2-C','KND','STATE_CEYLON','building_trade_center','pm_trade_center_trade_quantity_normal','pm_trade_center_trade_quantity_limited'),
 ('R2-C','CAR','STATE_CIRCARS','building_trade_center','pm_trade_center_trade_quantity_normal','pm_trade_center_trade_quantity_limited'),
 ('R2-C','CAR','STATE_MADRAS','building_trade_center','pm_trade_center_trade_quantity_normal','pm_trade_center_trade_quantity_limited'),
]
ALLOY_FILE='common/technology/technologies/95_tech6r1_aluminium_metallurgy.txt'
def guarded_write(path,old,new,edits,phase):
    assert path.is_relative_to(ROOT) and path.read_bytes()==old,'Concurrent edit: '+str(path)
    rel=path.relative_to(ROOT).as_posix();dest=OUT/'PATCH_PREIMAGES'/phase/rel
    assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(old)
    # Only current bytes were read and patched; never reconstruct from a delivery baseline.
    assert path.read_bytes()==old,'Concurrent edit before write: '+rel
    path.write_bytes(new);assert path.read_bytes()==new
    return dict(file=rel,before_sha256=sha(dest),after_sha256=sha(path),preimage=dest.relative_to(ROOT).as_posix(),edits=edits,phase=phase)
def pm_numbers(n):
    out={}
    def walk(nodes,prefix=''):
        for x in nodes:
            key=prefix+'/'+x.key
            if isinstance(x.value,list):walk(x.children(),key)
            else:
                try:out[key]=float(x.value)
                except (ValueError,TypeError):pass
    walk(n.children());return out
def install_pm():
    assert not (OUT/'PM_PATCHES.json').exists()
    current=load(OUT/'CURRENT_BEFORE.json');pms,_,_=r1.objects('common/production_methods');buildings,_,_=r1.objects('common/buildings');groups,_,_=r1.objects('common/production_method_groups')
    allrows=placements();pending=C.defaultdict(list);fixes=[]
    for cohort,tag,state,kind,old,new in PM_PLAN:
        found=[r for r in allrows if (r['tag'],r['state'],r['building'])==(tag,state,kind) and old in r['methods']]
        assert found,(tag,state,kind,old)
        knowledge=set(current['starts'][tag]['technologies']);assert set(r1.values(pms[old],'unlocking_technologies'))-knowledge
        assert not(set(r1.values(pms[new],'unlocking_technologies'))-knowledge)
        assert any(old in r1.values(groups[g],'production_methods') and new in r1.values(groups[g],'production_methods') for g in r1.values(buildings[kind],'production_method_groups'))
        # Read current bytes, preserving BOM and mixed newlines. Parser offsets refer to this exact text.
        for r in found:
            p=r['path'];data=p.read_bytes();raw=data.decode('utf-8-sig');root=cw.parse(raw)
            selected=[n for n in root for s in n.children() if s.key=='s:'+state for c in s.children() if c.key=='region_state:'+tag for n in c.children('create_building') if r1.val(n,'building')==kind and old in r1.values(n,'activate_production_methods')]
            assert len(selected)==1,(p,tag,state,kind)
            pm=selected[0].children('activate_production_methods')[0];token=[x for x in pm.children() if cw.scalar(x.value)==old];assert len(token)==1
            x=token[0];oldraw=raw[x.start:x.end];assert oldraw.strip('"')==old,repr(oldraw)
            newraw=oldraw.replace(old,new);pending[p].append(dict(start=x.start,end=x.end,old=oldraw,new=newraw,tag=tag,state=state,building=kind,cohort=cohort))
        bef=pm_numbers(pms[old]);aft=pm_numbers(pms[new]);delta={k:aft.get(k,0)-bef.get(k,0) for k in bef.keys()|aft.keys() if aft.get(k,0)!=bef.get(k,0)}
        fixes.append(dict(Cohort=cohort,TAG=tag,State=state,Building=kind,Before_PM=old,After_PM=new,History_Declarations=len(found),Sources=';'.join(r['file']+':'+str(r['line']) for r in found),Missing_Old_Gates=';'.join(sorted(set(r1.values(pms[old],'unlocking_technologies'))-knowledge)),New_Gates=';'.join(r1.values(pms[new],'unlocking_technologies')),Written_Parameter_Delta=json.dumps(delta,ensure_ascii=False,sort_keys=True),Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'))
    # Review the complete plan before the first functional write.
    csvout('BUILDING_TECH_FIXES.csv',fixes)
    patches=[]
    for p,edits in pending.items():
        old=p.read_bytes();raw=old.decode('utf-8-sig')
        for e in sorted(edits,key=lambda x:x['start'],reverse=True):
            assert raw[e['start']:e['end']]==e['old'];raw=raw[:e['start']]+e['new']+raw[e['end']:]
        new=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+raw.encode('utf8')
        cw.parse(raw);patches.append(guarded_write(p,old,new,edits,'P0_PM'))
    dump('PM_PATCHES.json',patches)
    print('P0 installed:',len(fixes),'building selections;',sum(len(p['edits']) for p in patches),'tokens in',len(patches),'current files',flush=True)

def install_alloys():
    assert (OUT/'PM_PATCHES.json').exists() and not (OUT/'ALLOYS_PATCH.json').exists()
    p=ROOT/ALLOY_FILE;old=p.read_bytes();raw=old.decode('utf-8-sig');tech=next(n for n in cw.parse(raw) if n.key=='alloysworking');parents=tech.children('unlocking_technologies')[0];assert r1.values(tech,'unlocking_technologies')==['coke_smelting']
    token=parents.children()[0];assert raw[token.start:token.end]=='coke_smelting'
    nl='\r\n' if '\r\n' in raw[parents.start:parents.end] else '\n';replacement='shaft_mining'+nl+'\t\torganized_workshops'
    changed=raw[:token.start]+replacement+raw[token.end:];cw.parse(changed)
    new=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+changed.encode('utf8')
    patch=guarded_write(p,old,new,[dict(start=token.start,end=token.end,old='coke_smelting',new=replacement)],'P1_ALLOYS');dump('ALLOYS_PATCH.json',patch)
    print('P1 installed: alloysworking requires shaft_mining + organized_workshops; no country technology grant',flush=True)

def rescan():
    assert (OUT/'ALLOYS_PATCH.json').exists()
    old=r1.OUT
    try:
        r1.OUT=OUT
        with contextlib.redirect_stdout(io.StringIO()):r1.inspect()
    finally:r1.OUT=old
    b=load(OUT/'CURRENT_BEFORE.json');a=load(OUT/'RESOLVED_AFTER.json');csvout('TECH_BEFORE_AFTER.csv',[dict(TAG=t,Before_Count=len(b['starts'][t]['technologies']),After_Count=len(a['starts'][t]['technologies']),Added=';'.join(sorted(set(a['starts'][t]['technologies'])-set(b['starts'][t]['technologies']))),Removed=';'.join(sorted(set(b['starts'][t]['technologies'])-set(a['starts'][t]['technologies']))),Direct_PM_Change=t in {p[1] for p in PM_PLAN},Alloy_Holder='alloysworking' in a['starts'][t]['technologies'],Runtime_Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if t in {p[1] for p in PM_PLAN} or 'alloysworking' in a['starts'][t]['technologies'] else 'NO_NEW_COUNTRY_GRANT') for t in a['active_tags']])
    impact=[]
    for t in a['active_tags']:
        k=set(a['starts'][t]['technologies']);impact.append(dict(TAG=t,Alloys_Held='alloysworking' in k,Coke_Held='coke_smelting' in k,Before_Parent_Gates_Met=set(b['graph']['alloysworking'])<=k,After_Parent_Gates_Met=set(a['graph']['alloysworking'])<=k,Before_Parents=';'.join(b['graph']['alloysworking']),After_Parents=';'.join(a['graph']['alloysworking']),New_Grant=False))
    csvout('ALLOYS_GLOBAL_IMPACT.csv',impact)
    with (OUT/'PRIORITY_MATRIX.csv').open(encoding='utf-8-sig',newline='') as f:matrix=[r for r in csv.DictReader(f) if r['ID'].startswith('TECH-R2-')]
    fixes={(t,s,k,old):new for _,t,s,k,old,new in PM_PLAN}
    for r in matrix:
        new=fixes.get((r['TAG'],r['State'],r['Building'],r['Object']));r.update(After_Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if new else 'OPEN',After_PM=new or r['Selected_PM'],After_Missing='' if new else r['Current_Missing'])
    for tag in ['AUS','BEO','FRA','PRU','RUS','SAX','SWE']:
        row={k:'' for k in matrix[0]};row.update(ID='ALLOY-'+tag,TAG=tag,Object='alloysworking',R1_Kind='TECH_GRAPH_PREREQUISITE',R1_Missing='coke_smelting',Priority='P1',Conclusion='OVERRESTRICTIVE_COKE_PARENT_FOR_NONFERROUS_ALLOYS',Evidence='Current base alloy PM consumes raw coal, not coke; Saltford charcoal/isolated coal annealing in C18; graph-wide impact examined.',Engine_Run=False,Current_Missing='coke_smelting',Action='REPLACE_SHARED_PARENT_NOT_COUNTRY_GRANT',After_Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION');matrix.append(row)
    for tag in ['AP7','CKC','FRS','GR7','HWA','INDOP','PLW','TTI']:
        row={k:'' for k in matrix[0]};row.update(ID='HISTORY-'+tag,TAG=tag,R1_Kind='MISSING_HISTORY',Priority='P3',Conclusion='DOCUMENTARY_REVIEW_NO_EUROPEAN_TEMPLATE',Evidence='Individual review in MISSING_HISTORY_REVIEW.csv; not certified intentional absence.',Engine_Run=False,Action='RESEARCH_WITH_OWNING_WORLD_AGENT',After_Status='OPEN');matrix.append(row)
    # Historical profile review is a different population, with country overlap.
    for r in b['rows']:
        if r['Status']!='REQUIRES_HISTORICAL_REVIEW':continue
        row={k:'' for k in matrix[0]};row.update(ID='PROFILE-'+r['TAG'],TAG=r['TAG'],R1_Kind='HISTORICAL_PROFILE_REVIEW',Priority='P2',Conclusion='HISTORICAL_PROFILE_NOT_CERTIFIED',Evidence='COUNTRIES_REQUIRING_REVIEW.csv and current 470-country inventory',Engine_Run=False,Action='SPECIALIST_REVIEW_NO_MASS_PROFILE_COPY',After_Status='OPEN');matrix.append(row)
    csvout('PRIORITY_MATRIX.csv',matrix)
    csvout('CONFIRMED_TECH_CONFLICTS.csv',[r for r in matrix if r['Conclusion']=='SELECTED_PM_WITH_UNSATISFIED_UNLOCK_GATE'])
    dump('RESCAN_SUMMARY.json',dict(countries=len(a['active_tags']),country_knowledge_changes=[t for t in a['active_tags'] if b['starts'][t]['technologies']!=a['starts'][t]['technologies']],before_categories=dict(C.Counter(r['Status'] for r in b['rows'])),after_categories=dict(C.Counter(r['Status'] for r in a['rows'])),alloy_holders=[r['TAG'] for r in impact if r['Alloys_Held']],parent_eligible_before=sum(r['Before_Parent_Gates_Met'] for r in impact),parent_eligible_after=sum(r['After_Parent_Gates_Met'] for r in impact),graph_debts_before=sorted(r1.graph_debts(b)),graph_debts_after=sorted(r1.graph_debts(a)),original_signals=223,pm_selected_incompatible_before=153,pm_selections_corrected=len(PM_PLAN),false_positives_proved=0,remaining_declared_tech_conflicts=len(a['conflicts']),matrix_priorities=dict(C.Counter(r['Priority'] for r in matrix)),matrix_open_priorities=dict(C.Counter(r['Priority'] for r in matrix if r['After_Status']=='OPEN')),automated_engine_test=False))
    print(json.dumps(load(OUT/'RESCAN_SUMMARY.json'),ensure_ascii=False),flush=True)

def reconcile_classification():
    """Retain the prior reviewed profile decisions, rather than reverting to stale plans."""
    b=load(OUT/'CURRENT_BEFORE.json');previous=load(r1.OUT/'RESOLVED_AFTER.json')
    assert b['starts']==previous['starts'] and b['graph']==previous['graph']
    assert load(OUT/'ENTRY.json')['r1_manifest_changes']==[]
    assert not (OUT/'RAW_CURRENT_BEFORE_WITHOUT_REVIEWED_PROFILE_OVERRIDES.json').exists()
    (OUT/'RAW_CURRENT_BEFORE_WITHOUT_REVIEWED_PROFILE_OVERRIDES.json').write_bytes((OUT/'CURRENT_BEFORE.json').read_bytes())
    changed=[r['TAG'] for r,p in zip(b['rows'],previous['rows']) if r['Status']!=p['Status']]
    b['rows']=previous['rows'];dump('CURRENT_BEFORE.json',b)
    (OUT/'PROFILE_DECISIONS.json').write_bytes((r1.OUT/'PROFILE_DECISIONS.json').read_bytes())
    dump('AUDIT_CLASSIFICATION_RECONCILIATION.json',dict(reason='Fresh resolution of all histories and graph matched R1 exactly, but the first R2 view omitted the 36 previously reviewed profile overrides, affecting 24 classification labels. Restore these documentary expectations, without any functional write or revised historical claim.',fresh_starts_equal_r1=True,fresh_graph_equal_r1=True,entry_manifest_equal_r1=True,country_rows_reclassified=changed,profile_decisions_source=(r1.OUT/'PROFILE_DECISIONS.json').relative_to(ROOT).as_posix(),profile_decisions_sha256=sha(r1.OUT/'PROFILE_DECISIONS.json'),raw_initial_view_preserved=True))
    print('Reused',len(load(OUT/'PROFILE_DECISIONS.json')),'reviewed profiles; preserved raw scan and classification explanation',flush=True)

MISSING=['AP7','CKC','FRS','GR7','HWA','INDOP','PLW','TTI']
MISSING_RESEARCH={
 'AP7':('Kayapó / agrégat amazonien','Cultures vivrières, chasse, pêche, collecte ; villages et réseaux de parenté. La source communautaire contemporaine ne date pas ces pratiques au 1er janvier 1776 et ne valide pas les cinq régions attribuées au TAG.','https://institutoraoni.org.br/atuacao/atividades-economicas-sustentaveis/','Source communautaire actuelle ; attribution de techniques 1776 encore ouverte.'),
 'CKC':('Communautés tchouktches','Élevage du renne, chasse maritime, bateaux de peau et échanges ; cultures moteur siberian/inuit trop larges pour un profil unique. Collections ethnographiques surtout XIXe–XXe : ne pas rétroprojeter armes à feu ou harpons explosifs en 1776.','https://www.amnh.org/research/anthropology/collections/collections-history/asian-ethnography','Pratiques matérielles documentées ; chronologie et équivalence technologique 1776 ouvertes.'),
 'FRS':('Communautés autochtones de Taïwan','Agriculture, chasse, filage/tissage et travail du rotin attestés chez les Truku ; yuanzhumin agrège plusieurs peuples. Ne pas transformer cet exemple en monarchie industrielle commune à toute l’île.','https://www.taroko.gov.tw/en/sglarticle/cultural-heritage','Source officielle locale, portée truku et non ensemble du TAG en 1776.'),
 'GR7':('Inuit du Groenland','Kayak, travail du bois/os/peau et chasse maritime : savoirs spécialisés distincts des manufactures du jeu. Collections de kayak XIXe ne prouvent pas une technologie industrielle XVIIIe. Capitale écrite STATE_BLUE_NILE sans portion possédée : signalement WORLD séparé, aucune correction ici.','https://invention.si.edu/invention-stories/inventing-outdoors','Équivalences 1776 ouvertes ; capitale manifestement hors des régions possédées signalée.'),
 'HWA':('Chefferies hawaïennes sous le vent','Hiérarchie aliʻi/kahuna/makaʻāinana, lois kapu, agriculture, pêche et construction de pirogues. Décentralisé dans le moteur ne signifie pas sans institutions ni savoirs. Pas de régime européen ni de techniques post-contact attribués.','https://www.nps.gov/hale/learn/historyculture/early-hawaiians.htm','Source NPS ; datation avant contact 1778 complétée par histoire agricole officielle.'),
 'INDOP':('Communautés de Sumatra / Batak','Cultures sumatran/batak ; réseaux de parenté et textiles rituels complexes, traditions dynamiques. Une plantation d’épices existe déjà, PM de culture et charrettes sans gate technologique ; ne pas créer une industrie ni attribuer la métallurgie pour ce seul motif.','https://australian.museum/learn/cultures/international-collection/indonesia/social-fabrics-of-the-batak-people/','Tissage et structures sociales documentés, correspondance au TAG composite et à 1776 encore ouverte.'),
 'PLW':('Palawa','Outils de pierre spécialisés, carrières et échanges ; savoirs non assimilables à une absence de technique. Population écrite 200 : donnée territoriale conservée et renvoyée à WORLD, aucune réparation démographique TECH.','https://nre.tas.gov.au/aboriginal-heritage-tasmania/cultural-heritage/aboriginal-stone-artefacts','Source officielle tasmanienne ; technologies nationales et démographie 1776 restent à étudier.'),
 'TTI':('Te Tau Ihu / Māori','Iwi/hapū, échanges, pêche, horticulture adaptée au climat, fibres et tissage ; techniques du harakeke antérieures au remplacement par des matériaux européens. Un savoir local textile ne prouve pas une manufacture mécanisée ou les institutions européennes du graphe.','https://collections.tepapa.govt.nz/topic/3613','Source Te Papa ; application régionale au nord de l’île du Sud encore ouverte.'),
}
def reviews():
    import validate_starting_technology_1776 as contract
    s=contract.collect_snapshot();inv=s['inventory'];rows=[];expectations={}
    for tag in MISSING:
        name,note,url,limit=MISSING_RESEARCH[tag];definition=s['definitions'][tag]
        expectations[tag]=dict(absence_policy='OPEN_DOCUMENTED_REVIEW',absence_evidence='MISSING_HISTORY_REVIEW.csv#'+tag)
        rows.append(dict(TAG=tag,Name=name,Country_Type=r1.val(definition,'country_type'),Cultures=';'.join(r1.values(definition,'cultures')),Religion=r1.val(definition,'religion') or 'NOT_EXPLICIT_IN_DEFINITION',Capital_Read_Only=r1.val(definition,'capital'),Owned_Regions=';'.join(x[0] for x in inv['states'] if x[1]==tag),Population_Written=sum(x['count'] for x in inv['regional_pop'] if x['key'][1]==tag),Initial_Building_Declarations=sum(x['count'] for x in inv['buildings'] if x['key'][1]==tag),Initial_Unit_Declarations=sum(x['count'] for x in inv['units'] if x['key'][0]==tag),History_Found=bool(s['starts'][tag]['history']),Technologies=len(s['starts'][tag]['technologies']),Research=note,Source=url,Limit=limit,Decision='OPEN_P3_NO_FUNCTIONAL_CHANGE',Intentional_Absence_Verified=False,Runtime_Validated=False))
    csvout('MISSING_HISTORY_REVIEW.csv',rows);dump('MISSING_HISTORY_EXPECTATIONS.json',expectations)
    allrows=load(OUT/'RESOLVED_AFTER.json')['rows'];newtags=[r['TAG'] for r in allrows if r['Tag_Origin']=='NEW_MOD_TAG']
    results=[contract.audit_country(t,s,expectations.get(t,{})) for t in newtags];dump('NEW_TAG_TECH_REVIEW.json',results)
    dump('NEW_TAG_TECH_REVIEW_SUMMARY.json',dict(total=len(results),statuses=dict(C.Counter(r['status'] for r in results)),finding_codes=dict(C.Counter(f['code'] for r in results for f in r['findings'])),note='Supplemental read-only scan of all 93 new tags, including initial law requests and units. These findings are not added as new confirmed runtime bugs to the original 223-signal matrix. Active laws, defaults and production remain runtime questions.'))
    # Hand-offs only; this technical pass cannot change capitals, population or laws.
    handoffs=[dict(TAG='GR7',Priority='P0',Owner='WORLD',Observation='Definition capital STATE_BLUE_NILE is not among owned regions (STATE_GREENLAND).',Action='Verify capital with territorial owner; TECH did not change it.'),dict(TAG='PLW',Priority='P3',Owner='WORLD',Observation='200 people in current effective written demographics; chronology and geography require specialist review.',Action='Demographic review; TECH preserved bytes.'),dict(TAG='BGT',Priority='P1',Owner='POLITICAL_LAWS',Observation='Preexisting political effect and imperial law variants have separate law compatibility issues, already documented in R1.',Action='No law, governor or technology gift as a workaround.')]
    csvout('OUT_OF_SCOPE_HANDOFFS.csv',handoffs)
    (OUT/'REUSABLE_TAG_CHECK.md').write_text('''# Contrôle par TAG — lecture seule

`tools/validate_starting_technology_1776.py --tag ABC --tag DEF --expectations fichier.json --output rapport.json`

Depuis Python : `snapshot = collect_snapshot()` une seule fois, puis `audit_country("ABC", snapshot, attentes_locales)` ; retourne un dictionnaire sans écrire. La commande retourne 1 si P0/P1, sinon 0 ; lire aussi REVIEW, qui ne vaut pas approbation.

Le fichier d’attentes associe chaque TAG à `required`, `forbidden`, éventuellement `allowed`, `historical_evidence`. Ce sont des attentes propres au pays, jamais un palier uniforme. Pour une absence d’historique, fournir `absence_policy` et `absence_evidence` : `OPEN_DOCUMENTED_REVIEW` conserve une revue P3, `INTENTIONAL_VERIFIED` exige une preuve et ne crée aucune validation humaine. Sans preuve, l’absence est signalée P0.

Vérifie les effets partagés, grants conditionnels séparés, références inconnues, parents, alertes chronologiques existantes, historiques, bâtiments, PM par groupe, gates de construction séparés des PM, ressources régionales, demandes de lois et types d’unités initiales. Les lois demandées ne sont pas certifiées actives ; l’allocation de ressource à la portion du propriétaire, les groupes omis et les choix par défaut du moteur exigent un contrôle en jeu. Les conditions non technologiques complètes des lois/PM ne sont pas simulées. Une alerte chronologique demande une source ; elle ne retire pas automatiquement un savoir.

Exemples d’attentes d’absence dans MISSING_HISTORY_EXPECTATIONS.json. Huit dossiers restent ouverts ; ce document n’affirme pas que leur omission était intentionnelle et fonctionnelle. Le rapport NEW_TAG_TECH_REVIEW.json couvre les 93 nouveaux TAGs, y compris les noyaux politiques approuvés, sans aucune intervention territoriale.
''',encoding='utf8')
    print('Individual missing-history reviews:',len(rows),'; new-tag read-only contracts:',len(results),flush=True)

def patches():return load(OUT/'PM_PATCHES.json')+[load(OUT/'ALLOYS_PATCH.json')]
def review_concurrent():
    assert not (OUT/'REVIEWED_CONCURRENT_STATE.json').exists()
    (OUT/'STATIC_FIRST_RUN.json').write_bytes((OUT/'TECH_VALIDATION.json').read_bytes())
    (OUT/'SESSION_FIRST_STATIC.json').write_bytes((OUT/'SESSION_AFTER_STATIC.json').read_bytes())
    source=ROOT/'docs/reports/map/WORLD_1776_CLOSURE/BALKANS-01/FILES_MODIFIED.json';w=load(source);b=load(OUT/'BASELINE.json');current=r1.runtime.runtime_hashes();owned={r['file']:r for r in patches()}
    comparisons={}
    for path,change in w['files'].items():
        assert b['hashes'][path]==change['before']
        actual=owned[path]['before_sha256'] if path in owned else current[path]
        assert actual==change['after'],path
        comparisons[path]=dict(world_before=change['before'],world_after=change['after'],verified_pre_TECH_patch=path in owned,current=current[path])
    (OUT/'WORLD_BALKANS01_FILES_MODIFIED_READ_ONLY_COPY.json').write_bytes(source.read_bytes())
    proof_files={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'docs/reports/map/WORLD_1776_CLOSURE').rglob('*') if p.is_file()}
    dump('REVIEWED_CONCURRENT_STATE.json',dict(source=source.relative_to(ROOT).as_posix(),source_sha256=sha(source),files=comparisons,tracking_proofs_after_independent_delivery=proof_files,expected_external_files=sorted(set(w['files'])-set(owned)),expected_owner_transfer=dict(state='STATE_WEST_AEGEAN_ISLANDS',RGBs=['x6090A0','x6960A0'],from_owner='VEN',to_owner='TUR',population=80404,buildings=['building_fishing_wharf','building_port']),political_requests_removed=['MOL/WAL law_organic_regulation','MOL/WAL law_elected_bureaucrats'],TECH_did_not_write_territorial_files=True,reviewed_report='docs/reports/map/WORLD_1776_CLOSURE/BALKANS-01/REPORT.md',first_static_failure_explained=True,independent_human_validation_not_created=True))
    print('Five independently delivered WORLD files reviewed; shared-file preimage exactly matches WORLD after-hash. No restoration.',flush=True)

def static():
    b=load(OUT/'BASELINE.json');before=load(OUT/'CURRENT_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json');inv=qa.inventory();current=r1.runtime.runtime_hashes();checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    owned={p['file'] for p in patches()};changed={p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)};external=changed-owned
    dump('CONCURRENT_CHANGES.json',dict(entry_r1_delivery_differences=load(OUT/'ENTRY.json')['r1_manifest_changes'],outside_owned_files={p:dict(before=b['hashes'].get(p),after=current.get(p)) for p in sorted(external)},owned_current_patches=sorted(owned),all_original_r1_functional_files_preserved=all(sha(ROOT/p)==h for p,h in load(r1.OUT/'FILES_MODIFIED.json')['sha256'].items()),policy='Read current bytes; exact token patch with preimage/hash guard; no old baseline restored. External changes retained.'))
    ck('Exactly five owned functional files',len(owned)==5)
    concurrent=load(OUT/'REVIEWED_CONCURRENT_STATE.json') if (OUT/'REVIEWED_CONCURRENT_STATE.json').exists() else None
    ck('All concurrent external deltas match independently reviewed WORLD delivery',external==set(concurrent['expected_external_files']) and all(current[p]==r['world_after'] for p,r in concurrent['files'].items() if p in external) if concurrent else not external)
    c=load(OUT/'CONCURRENT_CHANGES.json');c.update(review='REVIEWED_CONCURRENT_STATE.json' if concurrent else None,shared_preimage_matches_independent_WORLD_delivery=bool(concurrent),scope='TECH modifies five files by 15 reviewed token edits. WORLD separately transfers two Cycladic RGBs, 80404 people and existing assets, removes two law requests each in MOL/WAL.');dump('CONCURRENT_CHANGES.json',c)
    for patch in patches():
        path=ROOT/patch['file'];data=path.read_bytes();old=(ROOT/patch['preimage']).read_bytes();raw=old.decode('utf-8-sig')
        for e in sorted(patch['edits'],key=lambda x:x['start'],reverse=True):
            assert raw[e['start']:e['end']]==e['old'];raw=raw[:e['start']]+e['new']+raw[e['end']:]
        expected=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+raw.encode('utf8')
        ck('Only reviewed token edits '+patch['file'],data==expected and sha(path)==patch['after_sha256'] and sha(ROOT/patch['preimage'])==patch['before_sha256'])
        cw.parse(data.decode('utf-8-sig'));ck('Paradox syntax '+patch['file'],True)
    ck('470 countries same unconditional and conditional knowledge/history/effects',before['starts']==after['starts'] and len(after['active_tags'])==470)
    ck('No unknown technology or unresolved shared effect anywhere',all(set(v['technologies'])<=set(after['graph']) and not v['unresolved'] for v in after['starts'].values()))
    ck('Seven exact graph debts before and zero after',r1.graph_debts(before)=={(t,'alloysworking','coke_smelting') for t in ['AUS','BEO','FRA','PRU','RUS','SAX','SWE']} and not r1.graph_debts(after))
    ck('Only alloysworking parents changed',{k for k in before['graph'] if before['graph'][k]!=after['graph'][k]}=={'alloysworking'} and set(after['graph']['alloysworking'])=={'shaft_mining','organized_workshops'})
    ck('Late aluminium descendants and all other gates retained',all(before['graph'][k]==after['graph'][k] for k in before['graph'] if k!='alloysworking'))
    ck('No unknown graph parent',all(p in after['graph'] for v in after['graph'].values() for p in v))
    def cyclic(k,trail=()):return k in trail or any(cyclic(p,trail+(k,)) for p in after['graph'][k])
    ck('Graph acyclic',not any(cyclic(k) for k in after['graph']))
    ck('Technology era/category/inactive markers unchanged',all(before[k]==after[k] for k in ['tech_eras','tech_categories','tech_inactive']))
    pms,_,_=r1.objects('common/production_methods');buildings,_,_=r1.objects('common/buildings');groups,_,_=r1.objects('common/production_method_groups');rows=placements()
    for _,tag,state,kind,old,new in PM_PLAN:
        found=[r for r in rows if (r['tag'],r['state'],r['building'])==(tag,state,kind)];knowledge=set(after['starts'][tag]['technologies'])
        ck('PM compatible and selected '+tag+'/'+state+'/'+kind,found and all(new in r['methods'] and old not in r['methods'] for r in found) and not(set(r1.values(pms[new],'unlocking_technologies'))-knowledge) and any(new in r1.values(groups[g],'production_methods') for g in r1.values(buildings[kind],'production_method_groups')))
    ck('No new explicit building or PM gate conflict',{json.dumps(r,sort_keys=True) for r in after['conflicts']}<={json.dumps(r,sort_keys=True) for r in before['conflicts']})
    ck('207 declaration gates reduced to 195',len(before['conflicts'])==207 and len(after['conflicts'])==195)
    normalized=copy.deepcopy(inv)
    if concurrent:
        for row in normalized['owners']:
            if row['key'][0] in ['x6090A0','x6960A0'] and row['key'][1:] == ['STATE_WEST_AEGEAN_ISLANDS','TUR']:row['key'][2]='VEN'
        normalized['owners']=sorted(normalized['owners'],key=lambda x:x['key'])
        normalized['states']=[['STATE_WEST_AEGEAN_ISLANDS','VEN'] if x==['STATE_WEST_AEGEAN_ISLANDS','TUR'] else x for x in normalized['states']];normalized['states'].sort()
        typ=normalized['state_types'];typ['STATE_WEST_AEGEAN_ISLANDS|VEN']=typ.pop('STATE_WEST_AEGEAN_ISLANDS|TUR')
        for key in ['regional_pop','buildings']:
            for row in normalized[key]:
                if row['key'][:2]==['STATE_WEST_AEGEAN_ISLANDS','TUR']:row['key'][1]='VEN'
            normalized[key].sort(key=lambda x:x['key'])
        # Exact inverse solely in a comparison copy; never write this data to the game.
    for key in ['owners','states','geometry','state_types','countries','pops','resolved_demographics','regional_pop','building_levels_written','units','errors','duplicates']:ck('Effective '+key+' unchanged outside reviewed independent transfer',normalized[key]==b['inventory'][key])
    def strip_methods(body):
        n=json.loads(body);n[2]=[x for x in n[2] if x[0]!='activate_production_methods'];return json.dumps(n,sort_keys=True)
    def non_pm_counter(inventory):
        result=C.Counter()
        for r in inventory['buildings']:result[(r['key'][0],r['key'][1],strip_methods(r['key'][2]))]+=r['count']
        return result
    ck('Building non-PM content retained outside exact reviewed WORLD scope move',non_pm_counter(normalized)==non_pm_counter(b['inventory']))
    for rel,h in load(r1.OUT/'FILES_MODIFIED.json')['sha256'].items():ck('Exact human-tested R1 file preserved '+rel,sha(ROOT/rel)==h)
    ck('All R1 original and additive acceptance proofs preserved since receipt',all((ROOT/rel).is_file() and sha(ROOT/rel)==h for rel,h in b['r1_proofs'].items()))
    ck('R1 human receipt strictly scoped and excludes R2',load(r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json')['status']=='PASS_RUNTIME_USER_VALIDATED' and not load(r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json')['world_audit_complete'])
    ck('Every SERG file unchanged',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in b['serg_proofs'].items()))
    ck('Every existing WORLD tracking file unchanged',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in b['world_tracking'].items()))
    checked=rm.check();ck('Canonical territorial validator PASS and state byte-equivalent',checked['status']=='PASS' and load(rm.OUT/'ROADMAP_STATE.json')==b['serg_state'])
    ck('All prior tools and tests unchanged',all(sha(ROOT/p)==h for p,h in b['tools'].items()))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    version=load(OUT/'VERSION_EVIDENCE.json');ck('Executable and prior log 1.13.11 target 1.13.*',version['product_version']=='1.13.11' and '1.13.*' in version['target'] and any('release/1.13.11' in x for x in version['previous_log']))
    ck('Eight missing histories unchanged, individually open, no invented absence approval',{t for t,v in after['starts'].items() if not v['history']}==set(MISSING) and all(not after['starts'][t]['technologies'] for t in MISSING))
    ck('No R2 runtime attestation created',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    # All effective vanilla inputs used by the reusable validator are read-only and hashed.
    folders=['common/technology/technologies','common/scripted_effects','common/country_definitions','common/history/countries','common/history/buildings','common/buildings','common/production_methods','common/production_method_groups','common/laws','common/combat_unit_types','map_data/state_regions']
    vanilla={str(p):sha(p) for folder in folders for p in r1.effective(folder) if p.is_relative_to(GAME)}
    dump('VANILLA_READ_ONLY_INPUTS.json',vanilla)
    dump('FILES_MODIFIED.json',dict(runtime_files=sorted(owned),sha256={p:current[p] for p in sorted(owned)},country_PM_changes=sorted({p[1] for p in PM_PLAN}),PM_selections=12,history_tokens=14,graph_changed='alloysworking',technology_grants=0,technology_removals=0,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',human_validation=None,patches=['PM_PATCHES.json','ALLOYS_PATCH.json']))
    dump('SESSION_AFTER_STATIC.json',dict(hashes=current,inventory=inv,serg_check=checked,git=b['git']))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',new_human_attestation=None)
    dump('TECH_VALIDATION.json',result);print(result['passed'],'/',result['total'],result['failed'],flush=True);assert not result['failed']

def tests():
    import serg_sc4_ligurian_fiefs as lig
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden','test_serg_sc1_passau_outliers','test_serg_versioned_receipts','test_serg_sc1_regensburg_demography','test_start_economy_2026_10_15','test_starting_tech_audit_1776','test_starting_tech_audit_1776_r2']
    for label,names in [('TARGETED_TESTS',['test_starting_tech_audit_1776_r2']),('CUMULATIVE_TESTS',modules)]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names));failed=[dict(id=t.id(),traceback=trace) for t,trace in r.failures+r.errors]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8');dump(label+'.json',dict(status='FAIL' if failed else 'PASS',total=r.testsRun,passed=r.testsRun-len(failed)-len(r.skipped),failed=failed,skipped=[dict(id=t.id(),reason=reason) for t,reason in r.skipped],automated_engine_test=False))
        print(label,r.testsRun-len(failed)-len(r.skipped),'/',r.testsRun,'failures',len(failed),flush=True)

def resource_review():
    regions,sources,_=r1.objects('map_data/state_regions');rows=[];present={(r['state'],r['tag'],r['building']) for r in placements()}
    with (OUT/'PRIORITY_MATRIX.csv').open(encoding='utf-8-sig',newline='') as f:matrix=list(csv.DictReader(f))
    for m in matrix:
        if m['R1_Kind']!='RESOURCE_OR_PM_CONFLICT':continue
        region=regions[m['State']];kind=m['Building'];quantity=sum(float(n.value) for cap in region.children('capped_resources') for n in cap.children() if n.key==kind)
        quantity+=sum(float(r1.val(n,'discovered_amount','0')) for n in region.children('resource') if r1.val(n,'type')==kind)
        found=(m['State'],m['TAG'],kind) in present
        rows.append(dict(ID=m['ID'],TAG=m['TAG'],State=m['State'],Building=kind,Currently_Declared=found,Current_Regional_Discovered_Quantity=quantity,Source=sources[m['State']],Disposition='OPEN_REGION_TEMPLATE_NOT_OWNER_ALLOCATION' if found and quantity<=0 else 'REQUIRES_RECLASSIFICATION',Engine_Checked=False,Owner_Portion_Capacity_Certified=False))
    assert len(rows)==16 and all(r['Disposition']=='OPEN_REGION_TEMPLATE_NOT_OWNER_ALLOCATION' for r in rows)
    csvout('RESOURCE_REEVALUATION.csv',rows);print('16 regional resource warnings recomputed from current definitions; still open, not certified owner shortages',flush=True)

def reports():
    before=load(OUT/'CURRENT_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json');summary=load(OUT/'RESCAN_SUMMARY.json');v=load(OUT/'TECH_VALIDATION.json');target=load(OUT/'TARGETED_TESTS.json');cumulative=load(OUT/'CUMULATIVE_TESTS.json')
    known={r['id'] for r in load(r1.OUT/'CUMULATIVE_TESTS.json')['failed']};actual={r['id'] for r in cumulative['failed']};unknown=actual-known
    classified=[dict(id=r['id'],classification='Previously recorded snapshot/final-layer or genuine-receipt absence assertion' if r['id'] in known else 'NEW_FAILURE_REQUIRES_INVESTIGATION',previously_recorded=r['id'] in known) for r in cumulative['failed']]
    dump('CUMULATIVE_TEST_REVIEW.json',dict(status='NO_NEW_UNEXPLAINED_FAILURE' if not unknown else 'INVESTIGATION_REQUIRED',failed=classified,new_failures=sorted(unknown),previous_r1_failure_ids=sorted(known),old_tests_not_modified=True))
    assert not target['failed'] and not unknown
    cumulative.update(status='OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY' if cumulative['failed'] else 'PASS',new_unexplained_failures=[],classification_evidence='CUMULATIVE_TEST_REVIEW.json');dump('CUMULATIVE_TESTS.json',cumulative)
    v.update(targeted_tests=dict(passed=target['passed'],total=target['total'],failed=len(target['failed'])),cumulative_tests=dict(passed=cumulative['passed'],total=cumulative['total'],known_old_failures=len(cumulative['failed']),skipped=len(cumulative['skipped']),new_unexplained_failures=0),global_audit_status='OPEN_FINDINGS_REMAIN',complete_world_profile_certification=False,first_static_run='STATIC_FIRST_RUN.json',concurrent_review='REVIEWED_CONCURRENT_STATE.json');dump('TECH_VALIDATION.json',v)
    table='\n'.join('| '+tag+' | '+str(len(before['starts'][tag]['technologies']))+' | '+str(len(after['starts'][tag]['technologies']))+' | 0 / 0 |' for tag in sorted({p[1] for p in PM_PLAN}))
    pm_table='\n'.join('| '+cohort+' | '+tag+' | '+state.removeprefix('STATE_')+' | '+kind.removeprefix('building_')+' | `'+old+'` → `'+new+'` |' for cohort,tag,state,kind,old,new in PM_PLAN)
    priorities=summary['matrix_priorities'];openpriorities=summary['matrix_open_priorities']
    priority_table='\n'.join('| '+p+' | '+str(priorities.get(p,0))+' | '+str(openpriorities.get(p,0))+' |' for p in ['P0','P1','P2','P3','P4'])
    historical='''# Décisions historiques et limites de TECH-R2

Référence : 1er janvier 1776. Les choix de PM sont des approximations techniques bornées, soumises au joueur ; ils ne certifient pas l’absence de tous les savoirs correspondants dans chaque pays. Les profils historiques nationaux ne sont pas élargis sans preuve.

## Alliages : correction de la dépendance, sans cadeau national

Le nœud `alloysworking` représente, selon la note préexistante du mod, une production régulière et contrôlée d’alliages, et non toute pratique artisanale du bronze. L’usine `building_alloys_plant` et sa recette `pm_basic_smelting_process` sont relues : fer 25, cuivre 15, plomb 10 et charbon 10 donnent alliages 60 à pleine activité écrite ; la recette ne requiert pas de coke. Ces valeurs ne sont pas des observations moteur.

La notice archéologique de [Saltford, Historic England](https://historicengland.org.uk/listing/the-list/list-entry/1004607) décrit les ateliers de laiton du XVIIIe siècle, leurs marteaux hydrauliques, le recuit au charbon de bois puis les fours isolant le métal des fumées de houille. Elle permet de distinguer ces opérations de la fonte au coke. [Ironbridge Gorge Museum Trust](https://www.ironbridge.org.uk/about-us/key-figures-in-the-history-of-the-ironbridge-gorge/) situe en 1709 le procédé de Darby pour la fonte au coke. L’existence de ce procédé ne le rend pas nécessaire à toutes les productions d’alliages.

Décision de modèle, explicitement inférée de ces sources et du contenu de la recette : parents `shaft_mining` + `organized_workshops`. Le premier représente le socle minier, le second l’organisation des ateliers ; cela ne prétend pas que chaque établissement devait exploiter son propre puits. Aucun nœud intermédiaire nouveau, aucune généralisation du coke à AUS/BEO/FRA/PRU/RUS/SAX/SWE, aucun changement de leur savoir acquis. Les douze détenteurs actuels possèdent déjà les deux parents.

La note ancienne en énumérait neuf ; le résolveur actuel retrouve aussi MGL, XIN et YUN, déjà détenteurs avant R2. Ce constat ne valide pas historiquement ces extensions. Le relevé Git en lecture seule montre `shaft_mining` lors de l’introduction du nœud le 16 septembre (`bf0b53a`), puis son remplacement par `coke_smelting` le 17 octobre (`73877cf`). La correction s’applique au fichier courant et conserve les révisions ultérieures de l’aluminium : aucune restauration du fichier ancien.

Impact global exhaustif : cinq pays remplissaient les seuls parents directs de recherche, contre 93 après. C’est une modification réelle de l’accès futur, **pas 88 attributions**, ni une preuve que tous les autres critères de recherche sont remplis. Le coût, l’ère, la catégorie, les recettes, le nombre de détenteurs et tous les autres parents sont conservés. Bauxite, Bayer, chimie et électricité gardent leurs gates tardifs. ALLOYS_GLOBAL_IMPACT.csv contient les 470 pays.

## Ateliers : procédés compatibles avec le profil conservé

RUS/Brest et GEN : exploitation forestière simple plutôt que la recette de scierie exigeant `mechanical_tools`. GEN : meubles artisanaux et outils simples ; VEN/Istrie : outils simples. La recette d’outils avancée consommait acier et demandait `precision_boring`. Les anciens PM existent déjà dans les mêmes groupes ; aucune machine ou industrie n’est créée.

Les tours existaient avant 1776 : les [collections Dominy de Winterthur](https://dominycollections.winterthur.org/tools-of-the-trade/woodworking/lathe/) conservent notamment un tour à perche daté 1750–1775. Le repli de GEN ne signifie donc pas « aucun tour à Gênes ». Il évite d’assimiler un artisanat local à toute la capacité industrielle du nœud partagé `mechanical_tools`. Une future preuve locale pourrait justifier une autre solution ; aucune suppression mondiale de cette recette.

## Administration, transport et textile

VEN/Venetia et KND/Ceylan : organisation simple en l’absence de la technologie précise de registre systématique. On ne nie pas leurs archives ou leur administration. Ce repli retire le papier et ramène, par niveau et à activité comparable, bureaucratie 50→10 et capacité fiscale 10→2. Il peut créer une difficulté économique : le test joueur doit la mesurer. Aucune bureaucratie compensatoire ni nouveau registre national n’est inventé.

KND : la couche de canaux industriels est désactivée, tout en conservant routes traditionnelles, absence de rail et absence de train voyageurs. Ce choix ne supprime pas l’irrigation ancienne : les canaux représentés par ce PM sont un réseau industriel de transport avec intrants et métiers spécialisés. Les deux déclarations historiques sont corrigées sans les compter comme deux nouvelles constructions.

BIK : désactiver la conversion en vêtements de luxe incompatible avec le savoir textile écrit, tout en conservant vêtements cousus à la main et métiers traditionnels. Il ne s’agit pas de nier les traditions textiles du Rajasthan. Le gate de construction de la manufacture demeure un dossier P1 indépendant ; aucun profil textile complet n’est certifié.

## Commerce limité : trois centres, deux pays

KND et CAR conservent leurs centres et la propriété économique existante, avec `pm_trade_center_trade_quantity_limited` sans gate financier. Le commerce normal exige `organized_financial_institutions`. Les [papiers d’Arcot conservés au London Museum, 1750–1780](https://www.londonmuseum.org.uk/collections/v/object-779416/document/) attestent des relations financières et commerciales complexes dans le Carnatic. Cela ne prouve ni l’absence d’institutions, ni l’équivalence de toutes ces pratiques au nœud bancaire du mod. Le choix conservateur corrige la sélection incompatible sans attribuer un appareil financier complet ; ses effets, quantité commerciale −50 % et demande de marine marchande 4→3, restent à tester. CAR a deux centres, Circars et Madras.

## Huit absences d’historique : aucun faux succès

MISSING_HISTORY_REVIEW.csv donne pour chaque TAG cultures, religion écrite ou absente, capitales lues sans les modifier, régions, population effective écrite, bâtiments, unités, source et limites chronologiques. Les huit absences restent **OPEN_P3_NO_FUNCTIONAL_CHANGE** ; leur intention et leur innocuité moteur ne sont pas démontrées par le seul statut décentralisé. Sept n’ont aucun bâtiment explicite, INDOP possède sa plantation d’épices avec deux PM compatibles sans gate. Aucun profil européen, industrie, loi ou technologie n’est créé.

Sources individuelles : Institut Raoni pour AP7 (pratiques actuelles, sans rétroprojection certaine en 1776) ; AMNH pour CKC (collections tardives, sans projection des armes à feu) ; parc national Taroko pour FRS (exemple truku, pas l’ensemble de Taïwan) ; Smithsonian pour GR7 (kayaks, chronologie limitée) ; NPS et histoire agricole officielle hawaïenne pour HWA ; Australian Museum pour INDOP (textiles et parenté, sans couvrir tout Sumatra) ; patrimoine autochtone de Tasmanie pour PLW ; Te Papa pour TTI (fibres, tissage et adaptations). Les liens précis et restrictions sont conservés dans le CSV.

GR7 porte une capitale hors de sa région possédée ; PLW a une population écrite de 200. Ces constats sont des renvois documentaires à WORLD, jamais une permission TECH de modifier la carte ou les POP. La décision demeure ouverte pour chacun, y compris les pratiques agricoles, institutions locales et équivalences techniques qui demandent des recherches spécialisées.

## Signaux laissés ouverts et protections

Les 121 choix de commerce normal restants et les 18 ports ne sont pas tous rétrogradés en bloc : leur rôle économique et leurs capacités locales demandent une décision propre. Deux recettes d’artillerie sans alternative compatible restent P0. Les 54 gates de construction ne prouvent pas à eux seuls une production nulle d’un bâtiment déjà installé. Les 16 alertes régionales de ressource ne certifient pas l’allocation à la portion nationale. Aucun faux positif n’est déclaré sans preuve.

Lois et unités des 93 nouveaux TAGs sont signalées séparément par le nouveau contrat en lecture seule. Les demandes conditionnelles de lois ne sont pas des lois actives certifiées. Les incompatibilités politiques BGT préexistantes restent hors périmètre ; la validation humaine réelle de sa mine n’est ni annulée ni étendue.
'''
    (OUT/'HISTORICAL_DECISIONS.md').write_text(historical,encoding='utf8')
    protocol='''# TECH-R2 — protocole joueur groupé

**INSTALLÉ — EN ATTENTE DE VALIDATION HUMAINE.** R1 est validé dans sa version exacte ; son reçu ne couvre pas R2. Le moteur n’a pas été lancé par l’agent. Utiliser une **nouvelle partie au 1er janvier 1776**, avec le mod courant, et observer les pays par changement de pays/observateur si nécessaire. Une ancienne sauvegarde peut conserver les anciens choix.

## 1. Technologies et témoins, avant de laisser passer du temps

Aucun savoir initial ajouté ou retiré pour les 470 pays. Pour les six pays dont les procédés changent :

| TAG | Technologies avant R2 | Après R2 | Ajouts / retraits |
| --- | ---: | ---: | --- |
'''+table+'''

Contrôler les listes, pas seulement les nombres : TECH_BEFORE_AFTER.csv et STARTING_TECH_AUDIT_1776_AFTER.csv. Vérifier quelques témoins : BGT, BRX, TRT et LGE conservent leurs corrections R1 ; BGT garde sa mine native publique niveau 1 et son PM sans collecte de données. Conserver aussi les noyaux SERG et des témoins FRA/GBR/USA/CHI. Aucun effet au premier jour ne doit attribuer un paquet de technologies supplémentaire.

## 2. Sous-lots indépendants : bâtiments et procédés

Une seule partie permet ces contrôles ; chaque groupe peut être rapporté séparément. Les noms internes ci-dessous servent uniquement à identifier sans ambiguïté les recettes. Examiner leur infobulle et la liste réelle de PM du bâtiment.

| Sous-lot | Pays | État technique | Bâtiment | Ancien → nouveau PM |
| --- | --- | --- | --- | --- |
'''+pm_table+'''

R2-A : production et recrutement des ateliers/forêts, accès au bois, aux tissus et aux outils. Les flux écrits diminuent pour bois/meubles/outils ; cela ne doit pas être masqué par des subventions ou des technologies ajoutées. Vérifier les approvisionnements voisins et les qualifications.

R2-B : administration de VEN et KND, recrutement des employés, bureaucratie et capacité fiscale. **Bureaucratie 50→10 et capacité fiscale 10→2 par niveau à activité comparable**, papier 10→0 : relever tout déficit bloquant. À Ceylan, routes traditionnelles conservées, canaux industriels désactivés, aucun rail/train actif. Le PM supprimé représentait 800 postes et 1 infrastructure par niveau à plein fonctionnement ; ne pas exiger leur maintien. À Bikaner, vêtements de base conservés, conversion en luxe désactivée, aucun nouvel artisanat inventé.

R2-C : commerce limité à Kandy et dans les deux centres CAR. Le mod applique **−50 % à la quantité commerciale** et la demande de marine marchande du PM passe de 4 à 3 par niveau à plein fonctionnement. Vérifier échanges, accès au marché et absence de blocage économique excessif. Les titres de propriété et les niveaux des centres sont conservés. Aucun résultat de prix, revenu ou emploi n’est annoncé à l’avance.

BUILDING_TECH_FIXES.csv contient tous les écarts de paramètres, y compris changement des métiers, des intrants et des sorties. Les valeurs décrivent les scripts, pas une économie déjà observée. Une méthode visible mais impossible à garder sélectionnée, un arrêt de recrutement, un déficit administratif rédhibitoire ou une pénurie persistante doivent être rapportés comme anomalie avec pays/état/bâtiment.

## 3. R2-D : alliages et absence de déblocages tardifs

Dans l’arbre, `alloysworking` doit dépendre de `shaft_mining` et `organized_workshops`, plus de `coke_smelting`. AUS/BEO/FRA/PRU/RUS/SAX/SWE gardent les alliages déjà acquis sans recevoir le coke. Les autres détenteurs CHI/GBR/MGL/XIN/YUN restent inchangés.

Comparer un témoin possédant les nouveaux parents sans avoir encore les alliages : il peut remplir leurs parents directs sans obtenir la technologie gratuitement. L’étude globale recense 93 pays dans ce cas de prérequis satisfaits, dont les détenteurs ; cela ne certifie pas les autres critères du bouton de recherche. Vérifier que bauxite/Bayer, électricité, procédés électrolytiques, vapeur et rail ne sont pas débloqués artificiellement. La recette initiale de l’usine d’alliages reste identique ; si une usine existe, inspecter intrants, recrutement et sortie, sans en construire une gratuitement pour le test.

## 4. Un mois puis sauvegarde/rechargement

Laisser tourner un mois complet. Surveiller les six pays, l’administration, le commerce et les chaînes ateliers/forêts ; noter les pénuries, déficits ou PM remplacés par défaut par le moteur. Le recrutement peut être partiel ; l’absence de plein emploi n’est pas à elle seule un échec. Vérifier les ressources réellement disponibles dans les portions nationales concernées.

Sauvegarder puis recharger. Retrouver technologies, bâtiments, PM et économie sans crash ni anomalie bloquante. Rendre un résultat par sous-lot R2-A/B/C/D avec les seules observations réellement faites. Ne pas étendre une réussite à tout l’audit mondial, aux huit historiques absents ou aux tâches territoriales SERG/WORLD.

Le lot concurrent BALKANS-01 a son propre protocole et son propre suivi. Le tester éventuellement dans la même partie ne le valide pas automatiquement : son attestation doit préciser ce périmètre distinct. RG-D-CITY reste également indépendant.
'''
    (OUT/'PLAYER_TEST_PROTOCOL.md').write_text(protocol,encoding='utf8')
    report='''**AUDIT TECHNOLOGIQUE 1776 — R2**

R1 : **PASS_RUNTIME_USER_VALIDATED**, périmètre exact conservé. R2 : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, sans nouveau reçu humain. Audit mondial encore incomplet.

## 1. Attestation R1 et comparaison de livraison

Le joueur confirme le protocole complet des huit corrections BGT/BRX/TRT/LGE/PAP/CAR/ARK/VIE (28 ajouts), la mine native publique BGT niveau 1, un mois et la sauvegarde/rechargement. Les trois fichiers fonctionnels correspondent exactement à leurs empreintes de livraison. Aucune différence dans le manifeste R1 à l’entrée, aucune date effective de test ni mesure économique inventée. RUNTIME_USER_ATTESTATION_2026_10_24.json et la copie du message sont ajoutés au dossier R1 ; les rapports et manifestes originaux sont conservés. Seul AUDIT_STATE.json est actualisé pour le reçu. Le reçu exclut R2, l’exactitude des 470 profils, RG-D-CITY et toute clôture SERG/WORLD. R1_ACCEPTANCE_CHECK.json contient les comparaisons.

## 2. Inventaire courant et version

470 pays actifs, dont 93 nouveaux TAGs ; 462 avec historique, 442 avec au moins une technologie, 28 ensembles vides. Huit historiques absents, toujours ouverts. Les premières classifications de la recapture avaient omis les décisions documentaires R1 ; les connaissances et le graphe correspondaient pourtant exactement. Les 36 décisions existantes ont été réutilisées sans changement fonctionnel, corrigeant 24 étiquettes. Le relevé brut est conservé dans RAW_CURRENT_BEFORE_WITHOUT_REVIEWED_PROFILE_OVERRIDES.json et l’explication dans AUDIT_CLASSIFICATION_RECONCILIATION.json.

| Catégorie principale exclusive | Entrée R2 | Après R2 |
| --- | ---: | ---: |
'''
    report+='\n'.join('| '+key+' | '+str(summary['before_categories'].get(key,0))+' | '+str(summary['after_categories'].get(key,0))+' |' for key in ['PASS','REQUIRES_HISTORICAL_REVIEW','BUILDING_TECH_CONFLICT','INCORRECT_TECH_PROFILE','MISSING_HISTORY'])
    report+='''

Les sept profils aux parents incohérents passent à revue historique, pas à validation historique automatique. Ces catégories exclusives diffèrent des lignes de conflits : plusieurs problèmes peuvent concerner le même pays. Les décisions de profil conservées, le détail des 470 pays et le delta technologique exhaustif sont fournis.

Exécutable local et dernier journal disponible : **1.13.11** ; descriptor : **1.13.***. Les définitions et effets réellement présents sont utilisés. VERSION_EVIDENCE.json distingue le journal préexistant d’un test nouveau. Aucune incompatibilité de version supplémentaire démontrée dans le périmètre ; aucune prétendue exécution moteur ni modification vanilla.

## 3. 223 signalements réévalués et priorités

Les 207 lignes de gates se répartissent en **153 sélections explicites de PM dont le gate manque** et **54 restrictions de construction** ; les **16 alertes de ressources** concernent le modèle régional et non une allocation nationale certifiée. **Zéro faux positif démontré**. Les 153 incompatibilités sont confirmées dans les scripts, **zéro panne de production observée par l’agent en jeu**. Le dernier choix explicite par groupe et l’ordre des couches sont reconstruits ; ce modèle ne remplace pas une trace du moteur et ne certifie pas les groupes omis.

La matrice étendue ajoute les sept dettes de graphe, les huit dossiers d’historiques et les 158 revues de profils existantes : 396 lignes, qui ne sont pas 396 bugs ni 396 pays distincts. P4 est explicitement vide. Douze PM et les sept dettes sont traités statiquement et attendent le joueur.

| Priorité | Lignes à l’examen | Encore ouvertes après installation |
| --- | ---: | ---: |
'''+priority_table+'''

CONFIRMED_TECH_CONFLICTS.csv conserve les 153 lignes initiales avec leur statut après correction. PRIORITY_MATRIX.csv conserve cause, gate, alternatives compatibles, source, action et limite moteur pour chaque signalement. 195 gates de déclarations restent après, dont 141 PM et 54 constructions ; les 16 alertes de ressources restent ouvertes. Les sept pays libérés de l’incohérence de graphe doivent encore être appréciés historiquement : cela explique les 165 profils de la vue actuelle sans inventer sept nouvelles corrections de pays.

## 4. Corrections installées, pays et technologies

**Douze sélections de PM**, **quatorze remplacements** dans quatre historiques, car Ceylan possède deux couches identiques pour deux bâtiments. Puis une seule correction de graphe dans un cinquième fichier. Aucun bâtiment, niveau, subvention, ressource, population ou technologie nationale créé par TECH-R2. Aucun PM commun modifié.

| Sous-lot | Pays | État technique | Bâtiment | Avant → après |
| --- | --- | --- | --- | --- |
'''+pm_table+'''

| Pays avec PM corrigé | Technologies avant | Après | Ajouts / retraits |
| --- | ---: | ---: | --- |
'''+table+'''

Les 470 ensembles restent identiques, soit **zéro ajout et zéro retrait**. Le fichier TECH_BEFORE_AFTER.csv le prouve pays par pays. Les titres étrangers, réserves et niveaux sont conservés. Les paramètres réduits et leurs conséquences à tester sont dans BUILDING_TECH_FIXES.csv et le protocole : notamment administration 50→10, commerce −50 %, production artisanale moins intensive. Aucune rentabilité n’est inventée.

## 5. Sept incohérences des alliages

`alloysworking` dépend désormais de **shaft_mining + organized_workshops**. Le coke n’est offert à personne. Le contenu de l’usine ne nécessite pas ce procédé spécifique de fonte ; les sources sur le laiton et le recuit du XVIIIe siècle soutiennent cette séparation. Les douze détenteurs actuels, y compris MGL/XIN/YUN absents de l’ancienne liste de neuf, restent détenteurs. Tous ont les nouveaux parents ; sept dettes→zéro. L’accès aux seuls parents de recherche passe de 5 à 93 pays ; aucun octroi automatique, coût/ère et descendants tardifs inchangés. Décision historique, lecture Git et impacts exhaustifs dans HISTORICAL_DECISIONS.md et ALLOYS_GLOBAL_IMPACT.csv.

## 6. Historiques absents et futurs TAGs

AP7, CKC, FRS, GR7, HWA, INDOP, PLW et TTI sont examinés séparément : cultures, institutions/pratiques, source, limites, actifs et données écrites. Sept n’ont pas de bâtiment explicite ; INDOP a une plantation d’épices dont les PM n’exigent pas de technologie manquante. Aucune absence intentionnelle et fonctionnelle n’est certifiée sans preuve, aucun profil occidental forcé. MISSING_HISTORY_REVIEW.csv et OUT_OF_SCOPE_HANDOFFS.csv gardent les cas ouverts. Capitale GR7 hors région et population PLW sont renvoyées à WORLD sans écriture.

Le nouveau contrat `tools/validate_starting_technology_1776.py` est réutilisable par les agents territoriaux pour un ou plusieurs TAGs et leurs attentes historiques locales. Il contrôle historique, effets, technologies, parents, alertes chronologiques, bâtiments, PM, ressources, demandes de lois et unités ; il n’impose aucun palier uniforme. NEW_TAG_TECH_REVIEW.json couvre les **93 nouveaux TAGs**. Les alertes supplémentaires de lois demandées et de recrutement ne sont pas des lois actives ni des pannes moteur certifiées, et ne sont pas fondues artificiellement dans les 223 lignes originales.

## 7. Tests effectivement exécutés

'''+f"**{v['passed']}/{v['total']} contrôles statiques**, **{target['passed']}/{target['total']} tests ciblés**. **{cumulative['passed']}/{cumulative['total']} cumulatifs réussis**, {len(cumulative['failed'])} anciennes assertions et {len(cumulative['skipped'])} exclusion héritée ; zéro nouvel échec inexpliqué. Les anciens tests sont conservés. Traces dans TARGETED_TESTS.log et CUMULATIVE_TESTS.log ; classement dans CUMULATIVE_TEST_REVIEW.json.\n"+'''
Syntaxe des cinq fichiers, PM dans leur groupe et gates satisfaits, 470 ensembles initiaux identiques, graphe sans cycle/ID inconnu/dette restante, descendants tardifs, contraintes négatives du nouveau contrat, ressources et actifs, empreintes R1, données nationales protégées et Git sont contrôlés. Aucun mois ni sauvegarde n’est simulé par ces tests.

## 8. Concurrence et conservation

La première passe statique (54/60) a détecté six écarts liés aux modifications concurrentes WORLD BALKANS-01. Son résultat est gardé, pas effacé. Les cinq fichiers de ce lot et ses preuves ont été lus : deux RGB cycladiques VEN→TUR, 80 404 habitants transférés sans variation mondiale, pêche et port déplacés de scope, deux demandes de lois retirées dans chacun de MOL/WAL. Le fichier de bâtiments partagé correspondait **exactement** à l’empreinte de sortie WORLD avant mon patch. Les quatre autres fichiers correspondent toujours à sa livraison. Une copie de comparaison inverse existe seulement en mémoire pour vérifier tous les autres champs ; aucune donnée territoriale n’est réécrite par TECH.

Les corrections concurrentes sont conservées ; les statuts et le protocole WORLD demeurent de sa responsabilité. Les fichiers, POP, propriétaires et demandes de lois extérieurs à ce delta documenté sont inchangés. Tous les bâtiments/PM communs, fortifications, génie, Anzin, sel, drainage, Saint-Gobain, France, USA/Minutemen et noyaux SERG restent protégés. Aucun fichier restauré depuis une baseline, aucun Git d’écriture, aucun vanilla écrit.

## 9. Validation joueur et suite

PLAYER_TEST_PROTOCOL.md regroupe les quatre sous-lots : nouvelle partie en 1776 ; six pays et 12 PM ; alliages et témoins ; ressources, recrutement, administration, commerce et économie ; un mois puis sauvegarde/rechargement. R2 reste **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** jusqu’à une confirmation explicite. Les huit absences, les 141 PM ouverts, 54 constructions, 16 ressources et revues historiques restent à traiter ; les difficultés politiques BGT relèvent d’un chantier distinct.

**SERG inchangé : 82/235 = 34,89 %, 24/81 tâches qualifiées**, 873 fichiers de preuves/suivi identiques. MC-I-CORE, TR-I-CORE, BR-I-CORE, BG-I-CORE et PS-OB-CORE conservés ; RG-D-CITY garde son statut indépendant. Aucune tâche territoriale commencée par TECH. Prochaine action : validation joueur R2 ; préparer ensuite une vague ciblée sur les ports/centres commerciaux et armureries encore ouverts, sans la commencer automatiquement.
'''
    (OUT/'REPORT.md').write_text(report,encoding='utf8')
    dump('AUDIT_STATE.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',R1_status='PASS_RUNTIME_USER_VALIDATED',R1_attestation=(r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json').relative_to(ROOT).as_posix(),country_PM_tags=sorted({p[1] for p in PM_PLAN}),country_technology_grants=0,graph_change='alloysworking',runtime_validation=dict(status='NOT_RUN_BY_AGENT',attestation=None,protocol='PLAYER_TEST_PROTOCOL.md'),global_audit_status='OPEN_FINDINGS_REMAIN',serg_tracking_written=False,territorial_task_started=False,next_action='Player validation of R2-A/B/C/D; no automatic R3 or territorial mission.'))
    (OUT/'PROGRESS_HISTORY.md').write_text('# Historique TECH-R2\n\n- 2026-10-24 — R2-001 : reçu humain R1 borné aux huit corrections et à la mine BGT exacte ; aucun écart fonctionnel à la livraison lors de l’enregistrement.\n- 2026-10-24 — R2-002 : réévaluation des 207 gates et 16 alertes régionales ; distinction construction, PM sélectionné et activité moteur.\n- 2026-10-24 — R2-003 : 12 choix de PM dans six pays, 14 tokens dans quatre fichiers courants ; sous-lots A/B/C.\n- 2026-10-24 — R2-004 : parent alliages remplacé par extraction en puits et ateliers organisés ; analyse des 470 pays, zéro grant ; sous-lot D.\n- 2026-10-24 — R2-005 : huit absences examinées et conservées ouvertes ; contrat réutilisable et lecture des 93 nouveaux TAGs.\n- 2026-10-24 — R2-006 : concurrence WORLD BALKANS-01 identifiée par empreintes, conservée ; premier diagnostic statique maintenu comme preuve.\n'+f"- 2026-10-24 — R2-007 : {v['passed']}/{v['total']} contrôles statiques, {target['passed']}/{target['total']} ciblés, {cumulative['passed']}/{cumulative['total']} cumulatifs ; {len(cumulative['failed'])} assertions anciennes, {len(cumulative['skipped'])} exclusion, aucun nouvel échec inexpliqué. Protocole joueur prêt ; aucun reçu R2.\n",encoding='utf8')
    print('R2 reports, protocol and scoped state written; no R2 human validation',flush=True)

def review_world_followup():
    assert not (OUT/'WORLD_TRACKING_FINAL_REVIEW.json').exists()
    (OUT/'FINAL_FIRST_RUN.json').write_bytes((OUT/'FINAL_CHECKS.json').read_bytes())
    first=load(OUT/'REVIEWED_CONCURRENT_STATE.json');old=load(OUT/'WORLD_BALKANS01_FILES_MODIFIED_READ_ONLY_COPY.json');world=ROOT/'docs/reports/map/WORLD_1776_CLOSURE';current_manifest=load(world/'BALKANS-01/FILES_MODIFIED.json')
    assert load(world/'BALKANS-01/FILES_MODIFIED_OWN_PATCH_ONLY.json')==old
    own={r['file']:r for r in patches()}
    for p,row in current_manifest['files'].items():
        assert row['before']==old['files'][p]['before']
        assert row['after']==(own[p]['after_sha256'] if p in own else old['files'][p]['after'])
        assert sha(ROOT/p)==row['after']
    changed={p:dict(before=h,after=sha(ROOT/p)) for p,h in first['tracking_proofs_after_independent_delivery'].items() if sha(ROOT/p)!=h}
    expected={'CONCURRENT_CHANGES.json','NEXT_ACTION.md','PROGRESS_HISTORY.md','ROADMAP.md','ROADMAP_STATE.json','BALKANS-01/FILES_MODIFIED.json','BALKANS-01/REPORT.md','BALKANS-01/VALIDATION.json'}
    assert set(changed)=={(world/p).relative_to(ROOT).as_posix() for p in expected}
    check=load(world/'BALKANS-01/VALIDATION.json');assert check['status']=='PASS_STATIC' and check['passed']==check['total'] and check['runtime']=='NOT_RUN'
    concurrence=load(world/'CONCURRENT_CHANGES.json');shared=concurrence['shared_file_composition'];assert shared['before']==own['common/history/buildings/01_south_europe.txt']['before_sha256'] and shared['after']==own['common/history/buildings/01_south_europe.txt']['after_sha256']
    tracking={p.relative_to(ROOT).as_posix():sha(p) for p in world.rglob('*') if p.is_file()}
    dump('WORLD_TRACKING_FINAL_REVIEW.json',dict(status='VERIFIED_INDEPENDENT_DOCUMENTARY_UPDATE_ONLY',files=changed,original_WORLD_own_patch_manifest_preserved=True,combined_functional_hashes_match=True,shared_composition_matches_our_exact_patch=True,world_static_checks_observed=dict(passed=check['passed'],total=check['total']),new_human_attestation=False,TECH_world_writes=False,tracking_current=tracking,reason='WORLD independently recognized our exact TECH-R2 changes, archived its original manifest, and updated its documentation, research state and test timing. Runtime is identical to our tested snapshot. First final check retained in FINAL_FIRST_RUN.json. Documentary hashes are a point-in-time observation, not a freeze on the independently active agent.'))
    c=load(OUT/'CONCURRENT_CHANGES.json');c['subsequent_WORLD_documentary_review']='WORLD_TRACKING_FINAL_REVIEW.json';dump('CONCURRENT_CHANGES.json',c)
    v=load(OUT/'TECH_VALIDATION.json');v['final_documentary_concurrency_review']='WORLD_TRACKING_FINAL_REVIEW.json';dump('TECH_VALIDATION.json',v)
    p=OUT/'REPORT.md';oldbytes=p.read_bytes();s=oldbytes.decode('utf8');s+='\nRevue finale de concurrence : WORLD a actualisé huit fichiers documentaires pour reconnaître exactement les patches TECH-R2, archiver son manifeste propre initial et consigner sa recherche balkanique ainsi que le calendrier de ses tests. Les cinq empreintes fonctionnelles composées concordent et aucun fichier du jeu n’a évolué depuis nos tests. Son contrôle documentaire affiche 53/53 sans test moteur. Le premier contrôle final (13/14) a détecté ces changements de preuves ; il est conservé dans FINAL_FIRST_RUN.json. WORLD_TRACKING_FINAL_REVIEW.json explique et vérifie cette évolution indépendante. Ses empreintes documentaires sont un relevé ponctuel, pas un gel de son agent actif. Aucun suivi WORLD n’a été écrit par TECH.\n';assert p.read_bytes()==oldbytes;p.write_text(s,encoding='utf8')
    with (OUT/'PROGRESS_HISTORY.md').open('a',encoding='utf8') as f:f.write('- 2026-10-24 — R2-008 : huit mises à jour documentaires indépendantes WORLD examinées ; son manifeste propre initial est conservé, les patches composés concordent exactement, aucun changement fonctionnel depuis les tests. Aucune validation humaine ajoutée.\n')
    print('Eight independent WORLD documentary updates verified; original own-patch manifest preserved; no runtime drift',flush=True)

def finalize():
    b=load(OUT/'BASELINE.json');v=load(OUT/'TECH_VALIDATION.json');checks={};current=r1.runtime.runtime_hashes();concurrent=load(OUT/'REVIEWED_CONCURRENT_STATE.json')
    checks['Runtime unchanged since static snapshot']=current==load(OUT/'SESSION_AFTER_STATIC.json')['hashes']
    checks['Five functional files match patch delivery']=all(sha(ROOT/p)==h for p,h in load(OUT/'FILES_MODIFIED.json')['sha256'].items())
    checks['873 SERG proofs byte preserved']=len(b['serg_proofs'])==873 and all(sha(ROOT/p)==h for p,h in b['serg_proofs'].items())
    checks['R1 accepted proofs byte preserved']=all(sha(ROOT/p)==h for p,h in b['r1_proofs'].items())
    world_review=load(OUT/'WORLD_TRACKING_FINAL_REVIEW.json') if (OUT/'WORLD_TRACKING_FINAL_REVIEW.json').exists() else None
    archived_world=ROOT/'docs/reports/map/WORLD_1776_CLOSURE/BALKANS-01/FILES_MODIFIED_OWN_PATCH_ONLY.json'
    checks['Independent WORLD own-patch proof preserved and documentary evolution reviewed']=bool(world_review) and world_review['combined_functional_hashes_match'] and sha(archived_world)==sha(OUT/'WORLD_BALKANS01_FILES_MODIFIED_READ_ONLY_COPY.json')
    checks['Vanilla effective input hashes unchanged']=all(sha(p)==h for p,h in load(OUT/'VANILLA_READ_ONLY_INPUTS.json').items())
    checks['Old tools and tests unchanged']=all(sha(ROOT/p)==h for p,h in b['tools'].items())
    checks['Real static and targeted checks pass']=v['status']=='PASS' and v['passed']==v['total'] and v['targeted_tests']['passed']==v['targeted_tests']['total']
    checks['No new unexplained cumulative failure']=not load(OUT/'CUMULATIVE_TEST_REVIEW.json')['new_failures']
    checks['R2 has no human receipt']=load(OUT/'AUDIT_STATE.json')['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and not list(OUT.glob('RUNTIME_USER_ATTESTATION*'))
    checks['Mandatory documents exist']=all((OUT/n).is_file() for n in ['REPORT.md','PRIORITY_MATRIX.csv','CONFIRMED_TECH_CONFLICTS.csv','BUILDING_TECH_FIXES.csv','TECH_BEFORE_AFTER.csv','HISTORICAL_DECISIONS.md','FILES_MODIFIED.json','CONCURRENT_CHANGES.json','TECH_VALIDATION.json','PLAYER_TEST_PROTOCOL.md'])
    with (OUT/'RESOURCE_REEVALUATION.csv').open(encoding='utf-8-sig',newline='') as f:resources=list(csv.DictReader(f))
    checks['16 resource warnings recomputed from current definitions']=len(resources)==16 and all(r['Currently_Declared']=='True' and float(r['Current_Regional_Discovered_Quantity'])<=0 and r['Engine_Checked']=='False' for r in resources)
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    checks['Git HEAD branch index unchanged']=git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index']
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);lines=diff.stdout.splitlines();own=set(load(OUT/'FILES_MODIFIED.json')['runtime_files']);own_errors=[x for x in lines if any(x.startswith(p+':') for p in own)]
    checks['No owned whitespace error']=not own_errors;dump('DIFF_CHECK.json',dict(returncode=diff.returncode,stdout=diff.stdout,stderr=diff.stderr,owned_errors=own_errors,old_findings_retained=True))
    result=dict(status='PASS' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),failed=[n for n,p in checks.items() if not p],checks=checks,automated_engine_test=False);dump('FINAL_CHECKS.json',result);assert not result['failed'],result
    dump('SESSION_AFTER.json',dict(hashes=current,git=b['git'],SERG_state=load(rm.OUT/'ROADMAP_STATE.json'),independent_WORLD_delivery='REVIEWED_CONCURRENT_STATE.json',static_only=True))
    manifest={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'}
    manifest.update({p:sha(ROOT/p) for p in load(OUT/'FILES_MODIFIED.json')['runtime_files']})
    for name in ['audit_starting_tech_1776_r2.py','validate_starting_technology_1776.py','test_starting_tech_audit_1776_r2.py']:manifest['tools/'+name]=sha(ROOT/'tools'/name)
    dump('DELIVERY_MANIFEST.json',dict(scope='R2 own functional edits and technical proofs; includes read-only copies but no territorial claim',files=manifest,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',human_validation=None))
    print('Final checks',result['passed'],'/',result['total'],'; delivery manifest',len(manifest),'files; R2 awaits user',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
