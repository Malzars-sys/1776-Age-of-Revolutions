"""TECH-R3: scoped R2 acceptance, then ports/trade/arms availability. No territorial writes."""
import collections as C,contextlib,copy,csv,io,json,os,re,subprocess,sys,unittest
from pathlib import Path
import audit_starting_tech_1776_r2 as r2
import validate_starting_technology_1776 as contract
r1=r2.r1;ROOT=r1.ROOT;GAME=r1.GAME;qa=r1.qa;cw=r1.cw;sha=r1.sha;load=r1.load
OUT=ROOT/'docs/reports/technology/STARTING_TECH_AUDIT_1776_R3'
SOURCE=Path('C:/Users/simeo/.codex/attachments/25b8866a-9822-43fd-9d6a-4a9630c06f64/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def dump(name,obj,base=None):((OUT if base is None else base)/name).write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def proof_hashes(folder):return {p.relative_to(ROOT).as_posix():sha(p) for p in folder.rglob('*') if p.is_file()}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def receive():
    assert not OUT.exists();OUT.mkdir()
    files=load(r2.OUT/'FILES_MODIFIED.json');manifest=load(r2.OUT/'DELIVERY_MANIFEST.json');oldstate=load(r2.OUT/'AUDIT_STATE.json');assert oldstate['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'
    previous=proof_hashes(r2.OUT);r1proofs=proof_hashes(r1.OUT);serg=proof_hashes(r1.rm.OUT);runtime=r1.runtime.runtime_hashes()
    scope={p:dict(delivered=h,current=sha(ROOT/p),exact=sha(ROOT/p)==h) for p,h in files['sha256'].items()}
    differences={p:dict(delivered=h,current=sha(ROOT/p) if (ROOT/p).is_file() else None) for p,h in manifest['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h}
    dump('ENTRY.json',dict(recorded_on='2026-10-24',R2_state=oldstate,R2_proofs=previous,R1_proofs=r1proofs,SERG_proofs=serg,runtime_hashes=runtime,R2_functional_comparison=scope,R2_manifest_differences=differences,git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    assert load(r1.OUT/'AUDIT_STATE.json')['status']=='PASS_RUNTIME_USER_VALIDATED'
    r1receipt=load(r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json');assert r1receipt['status']=='PASS_RUNTIME_USER_VALIDATED'
    (OUT/'USER_MISSION.txt').write_bytes(SOURCE.read_bytes());source_name='USER_VALIDATION_TECH_R2_2026_10_24.txt';(r2.OUT/source_name).write_bytes(SOURCE.read_bytes())
    receipt_name='RUNTIME_USER_ATTESTATION_2026_10_24.json';assert not (r2.OUT/receipt_name).exists()
    receipt=dict(status='PASS_RUNTIME_USER_VALIDATED',delivery='STARTING_TECH_AUDIT_1776_R2',scope='R2-A/B/C/D actually delivered and covered by PLAYER_TEST_PROTOCOL.md only',recorded_on='2026-10-24',actual_test_date=None,user_source=source_name,source_sha256=sha(SOURCE),protocol='PLAYER_TEST_PROTOCOL.md',protocol_sha256=sha(r2.OUT/'PLAYER_TEST_PROTOCOL.md'),delivery_manifest_sha256=sha(r2.OUT/'DELIVERY_MANIFEST.json'),tested_functional_files=files['sha256'],current_functional_comparison=scope,PM_selections=12,history_tokens=14,functional_files=5,PM_tags=['BIK','CAR','GEN','KND','RUS','VEN'],technology_grants=0,technology_removals=0,alloy_parents=['shaft_mining','organized_workshops'],sub_lots=['R2-A','R2-B','R2-C','R2-D'],new_game_date='1776-01-01',simulation_months=1,save_and_reload=True,protocol_confirmed_as_whole=True,explicitly_reported=['Fonctionnement des PM, administrations, centres commerciaux, bâtiments forestiers, manufactures, ateliers et autres bâtiments du protocole','Fonctionnement du graphe de prérequis des alliages','Aucune attribution nationale inattendue ou déblocage industriel anachronique constaté','Conservation des territoires et modifications concurrentes vérifiés','Aucune anomalie économique ou fonctionnelle bloquante lors des contrôles','Un mois complet réussi','Sauvegarde et rechargement réussis'],automated_engine_test=False,extra_measurements_invented=False,world_audit_complete=False,excludes=['Toute correction TECH-R3 ou postérieure','Toute révision ultérieure des fichiers ou recettes, notamment ECON-ALLOYS','Certification historique des 470 profils','Clôture SERG ou WORLD','Validation territoriale RG-D-CITY'])
    dump(receipt_name,receipt,r2.OUT)
    raw=(r2.OUT/'AUDIT_STATE.json').read_bytes();state=copy.deepcopy(oldstate);state['status']='PASS_RUNTIME_USER_VALIDATED';state['runtime_validation']=dict(status='PASS_RUNTIME_USER_VALIDATED',attestation=receipt_name,protocol='PLAYER_TEST_PROTOCOL.md',scope='Exact R2 delivery only; subsequent revisions excluded');state['next_action']='TECH-R3 separately authorized by player; R2 receipt does not cover its corrections.';assert (r2.OUT/'AUDIT_STATE.json').read_bytes()==raw;dump('AUDIT_STATE.json',state,r2.OUT)
    (r2.OUT/'ACCEPTANCE_2026_10_24.md').write_bytes(('# Réception humaine de TECH-R2\n\nPASS_RUNTIME_USER_VALIDATED pour les douze sélections, quatorze tokens dans quatre historiques, et les parents des alliages dans un cinquième fichier. Le joueur confirme le protocole intégral, un mois et la sauvegarde/rechargement. Pas de date effective ni de mesure inventée. La version est liée au manifeste original, sans héritage automatique pour R3 ou les recettes ECON-ALLOYS. Les rapports, tests et manifestes initiaux sont conservés ; AUDIT_STATE est la seule vue antérieure actualisée. Comparaison détaillée dans le reçu JSON et TECH-R3/R2_ACCEPTANCE.json.\n').encode('utf8'))
    checks=dict(real_user_source_preserved=sha(r2.OUT/source_name)==sha(SOURCE),exact_5_file_delivery_scope=len(scope)==5,receipt_is_PASS=receipt['status']=='PASS_RUNTIME_USER_VALIDATED',no_R3_inheritance=receipt['excludes'][0]=='Toute correction TECH-R3 ou postérieure',original_R2_proofs_preserved_except_state=all(sha(ROOT/p)==h for p,h in previous.items() if p!=(r2.OUT/'AUDIT_STATE.json').relative_to(ROOT).as_posix()),all_R1_proofs_preserved=all(sha(ROOT/p)==h for p,h in r1proofs.items()),R1_still_PASS=load(r1.OUT/'AUDIT_STATE.json')['status']=='PASS_RUNTIME_USER_VALIDATED',no_effective_test_date_invented=receipt['actual_test_date'] is None,no_new_engine_test=not receipt['automated_engine_test'])
    dump('R2_ACCEPTANCE.json',dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,functional_comparison=scope,manifest_differences=differences,R1_attestation_sha256=sha(r1.OUT/'RUNTIME_USER_ATTESTATION_2026_10_24.json'),receipt=(r2.OUT/receipt_name).relative_to(ROOT).as_posix(),subsequent_revisions_not_validated=True));assert all(checks.values())
    print('R2 human receipt recorded; exact functional hashes:',sum(r['exact'] for r in scope.values()),'/5; R1 preserved; delivery differences',list(differences),flush=True)

def capture():
    assert load(OUT/'R2_ACCEPTANCE.json')['status']=='PASS' and not (OUT/'BASELINE.json').exists()
    runtime=r1.runtime.runtime_hashes();inv=qa.inventory()
    dump('BASELINE.json',dict(hashes=runtime,inventory=inv,R1_proofs=proof_hashes(r1.OUT),R2_proofs=proof_hashes(r2.OUT),SERG_proofs=proof_hashes(r1.rm.OUT),WORLD_proofs=proof_hashes(ROOT/'docs/reports/map/WORLD_1776_CLOSURE'),SERG_state=load(r1.rm.OUT/'ROADMAP_STATE.json'),tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    (OUT/'PROFILE_DECISIONS.json').write_bytes((r2.OUT/'PROFILE_DECISIONS.json').read_bytes())
    old=r1.OUT
    try:
        r1.OUT=OUT
        with contextlib.redirect_stdout(io.StringIO()):r1.inspect()
    finally:r1.OUT=old
    (OUT/'CURRENT_BEFORE.json').write_bytes((OUT/'RESOLVED_AFTER.json').read_bytes())
    print('Fresh current snapshot captured:',len(load(OUT/'CURRENT_BEFORE.json')['active_tags']),'active countries',flush=True)

FOCUS={'PORT':{'building_port'},'TRADE':{'building_trade_center'},'ARMS':{'building_arms_industry','building_artillery_foundry','building_munition_plant'}}
PORT_PM='pm_aor1776_traditional_commercial_harbor'
PORT_TARGETS={('JAP','STATE_KYUSHU'),('KOR','STATE_BUSAN'),('SUL','STATE_MINDANAO')}
FINANCIAL_TAGS={'PRU','TUS'}
PORT_SOURCES={'JAP':'https://www.city.nagasaki.lg.jp/uploaded/attachment/4724.pdf','KOR':'https://customs.go.kr/busan/cm/cntnts/cntntsView.do?cntntsId=2386&mi=7394','SUL':'https://archium.ateneo.edu/phstudies/vol25/iss1/4/'}
def numbers(n):return r2.pm_numbers(n)
def numeric_sum(methods,pms):
    result=C.defaultdict(float)
    for pm in methods:
        if pm in pms:
            for path,value in numbers(pms[pm]).items():
                if '/workforce_scaled/' in path or '/level_scaled/' in path or '/unscaled/' in path:result[path]+=value
    return dict(result)
def flows(params):
    inputs={};outputs={};jobs={}
    for key,v in params.items():
        tail=key.rsplit('/',1)[-1]
        if tail.startswith('goods_input_') and tail.endswith('_add'):inputs[tail[12:-4]]=v
        elif tail.startswith('goods_output_') and tail.endswith('_add'):outputs[tail[13:-4]]=v
        elif tail.startswith('building_employment_') and tail.endswith('_add'):jobs[tail[20:-4]]=v
    return inputs,outputs,jobs
def last_levels(r):
    total=0
    for n in contract.walk(r['node'].children('add_ownership')):
        if n.key=='levels':total+=int(cw.scalar(n.value))
    return total or 1
def audit():
    s=contract.collect_snapshot();histories=r2.placements();bykey=C.defaultdict(list)
    for r in histories:bykey[(r['state'],r['tag'],r['building'])].append(r)
    goods,_,_=r1.objects('common/goods');prices={g:float(r1.val(n,'cost','0')) for g,n in goods.items()};matrix=[];categories={};unknown=set()
    for category,kinds in FOCUS.items():
        rows=[]
        for key,selection in sorted(s['selected'].items()):
            state,tag,kind=key
            if kind not in kinds:continue
            techs=set(s['starts'][tag]['technologies']);decls=bykey[key];base=s['buildings'][kind];chosen=list(selection.values())
            missing={pm:sorted(set(r1.values(s['pms'][pm],'unlocking_technologies'))-techs) for pm in chosen if pm in s['pms'] and set(r1.values(s['pms'][pm],'unlocking_technologies'))-techs}
            missing_building=sorted(set(r1.values(base,'unlocking_technologies'))-techs)
            params=numeric_sum(chosen,s['pms']);ins,outs,jobs=flows(params);unknown.update((set(ins)|set(outs))-set(goods))
            alternatives={g:[pm for pm in r1.values(s['groups'][g],'production_methods') if pm in s['pms'] and not(set(r1.values(s['pms'][pm],'unlocking_technologies'))-techs)] for g in selection}
            action='OPEN_RESEARCH_NOT_ENGINE_FAILURE' if missing or missing_building else 'NO_GATE_CONFLICT_HISTORICAL_AND_MARKET_REVIEW'
            if category=='PORT' and missing and (tag,state) in PORT_TARGETS:action='R3-P_TRADITIONAL_HARBOR_PM'
            elif category=='TRADE' and missing and tag in FINANCIAL_TAGS:action='R3-T_EVIDENCED_FINANCIAL_FOUNDATION'
            elif category=='ARMS' and 'pm_cannons' in missing:action='R3-A_TRADITIONAL_CASTING_GATE_ONLY_ECON_RECIPE_RESERVED'
            row=dict(TAG=tag,State=state,Building=kind,Selected_PM=';'.join(chosen),Missing_PM_Gates=json.dumps(missing,sort_keys=True),Missing_Construction_Gates=';'.join(missing_building),Priority='P0' if missing else 'P1' if missing_building else 'P3',Action=action,Explicit_History_Declarations=len(decls),Last_Declaration_Levels=last_levels(decls[-1]),All_Declaration_Levels=';'.join(str(last_levels(r)) for r in decls),Sources=';'.join(r['file']+':'+str(r['line']) for r in decls),Compatible_Alternatives=json.dumps(alternatives,sort_keys=True),Selected_Recipe_Inputs=json.dumps(ins,sort_keys=True),Selected_Recipe_Outputs=json.dumps(outs,sort_keys=True),Selected_Recipe_Jobs=json.dumps(jobs,sort_keys=True),Selected_Recipe_Base_Price_Margin_Before_Wages=sum(prices.get(g,0)*v for g,v in outs.items())-sum(prices.get(g,0)*v for g,v in ins.items()),Market_Input_Availability='NOT_CERTIFIED_BY_STATIC_DECLARATIONS',Omitted_Groups=';'.join(g for g in r1.values(base,'production_method_groups') if g not in selection),Historical_Source=PORT_SOURCES.get(tag,'') if category=='PORT' else '',Engine_Failure_Observed=False,Scope_Note='Last explicit PM per group; levels and values are declarative, not an engine execution or price/route simulation.')
            rows.append(row)
            if missing or missing_building:matrix.append(dict(ID=category+'-'+str(len(matrix)+1).zfill(3),Category=category,TAG=tag,State=state,Building=kind,Priority=row['Priority'],Missing_PM_Gates=row['Missing_PM_Gates'],Missing_Construction_Gates=row['Missing_Construction_Gates'],Action=action,Status='OPEN',Engine_Failure_Observed=False))
        csvout({'PORT':'PORT_TECH_AUDIT.csv','TRADE':'TRADE_CENTER_TECH_AUDIT.csv','ARMS':'ARMS_INDUSTRY_TECH_AUDIT.csv'}[category],rows);categories[category]=dict(assets=len(rows),PM_conflicts=sum(r['Missing_PM_Gates']!='{}' for r in rows),construction_conflicts=sum(bool(r['Missing_Construction_Gates']) for r in rows))
    csvout('PRIORITY_MATRIX.csv',matrix)
    selected={t:contract.audit_country(t,s) for t in sorted(FINANCIAL_TAGS|{x[0] for x in PORT_TARGETS}|{'MUG','MARATH'})};dump('TAG_CONTRACTS_BEFORE.json',selected)
    dump('FOCUS_BEFORE.json',dict(categories=categories,priority_rows=len(matrix),priorities=dict(C.Counter(r['Priority'] for r in matrix)),unknown_selected_goods=sorted(unknown),current_country_count=len(s['starts']),all_knowledge={t:v['technologies'] for t,v in s['starts'].items()},selection_model='Last explicit method per group; declaration level/count is not a certified engine merge result.'))
    print(json.dumps(load(OUT/'FOCUS_BEFORE.json')['categories']),'; focus conflict rows',len(matrix),flush=True)

def write_patch(path,old,new,edits,phase):
    assert path.is_relative_to(ROOT) and path.read_bytes()==old,'Concurrent modification: '+str(path)
    rel=path.relative_to(ROOT).as_posix();p=OUT/'PATCH_PREIMAGES'/phase/rel;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old)
    assert path.read_bytes()==old;path.write_bytes(new);assert path.read_bytes()==new
    return dict(file=rel,before_sha256=sha(p),after_sha256=sha(path),preimage=p.relative_to(ROOT).as_posix(),edits=edits,phase=phase)
def create_file(rel,data,phase):
    p=ROOT/rel;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);assert p.read_bytes()==data
    return dict(file=rel,before_sha256=None,after_sha256=sha(p),phase=phase,created=True)
def encode_like(raw,data):return (b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b'')+raw.encode('utf8')
def install_ports():
    assert (OUT/'FOCUS_BEFORE.json').exists() and not (OUT/'PORT_PATCHES.json').exists()
    pms,_,_=r1.objects('common/production_methods');assert PORT_PM not in pms
    pm='''# Commercial harbor services without a naval dockyard system.
pm_aor1776_traditional_commercial_harbor = {
 texture = "gfx/interface/icons/production_method_icons/anchorage.dds"
 building_modifiers = {
  workforce_scaled = {
   goods_input_wood_add = 9
   goods_input_fabric_add = 3
   goods_output_merchant_marine_add = 6
  }
  level_scaled = {
   building_employment_laborers_add = 490
   building_employment_clerks_add = 140
   building_employment_bureaucrats_add = 70
  }
 }
 state_modifiers = {
  workforce_scaled = { state_infrastructure_add = 2 }
 }
}
'''
    cw.parse(pm);pending=C.defaultdict(list)
    for r in r2.placements():
        if r['building']!='building_port' or (r['tag'],r['state']) not in PORT_TARGETS:continue
        data=r['path'].read_bytes();raw=data.decode('utf-8-sig')
        matches=[n for root in cw.parse(raw) for state in root.children() if state.key=='s:'+r['state'] for country in state.children() if country.key=='region_state:'+r['tag'] for n in country.children('create_building') if r1.val(n,'building')=='building_port']
        assert len(matches)==1
        token=[x for n in matches[0].children('activate_production_methods') for x in n.children() if cw.scalar(x.value)=='pm_basic_port'];assert len(token)==1
        x=token[0];pending[r['path']].append(dict(start=x.start,end=x.end,old=raw[x.start:x.end],new='"'+PORT_PM+'" "pm_1776_no_raw_data_reporting"',tag=r['tag'],state=r['state']))
    assert sum(len(v) for v in pending.values())==3
    group,source,_=r1.objects('common/production_method_groups');p=(ROOT if source['pmg_base_building_port'].startswith('MOD:') else GAME)/source['pmg_base_building_port'].split(':',1)[1];assert p.is_relative_to(ROOT)
    data=p.read_bytes();raw=data.decode('utf-8-sig');g=next(n for n in cw.parse(raw) if n.key=='pmg_base_building_port');tokens=g.children('production_methods')[0].children();x=next(x for x in tokens if cw.scalar(x.value)=='pm_basic_port');old=raw[x.start:x.start];nl='\r\n' if '\r\n' in raw[g.start:g.end] else '\n';new=PORT_PM+nl+'\t\t';pending[p].append(dict(start=x.start,end=x.start,old=old,new=new,group='pmg_base_building_port'))
    patches=[create_file('common/production_methods/1776_tech_r3_commercial_harbor.txt',pm.encode('utf8'),'R3-P')]
    for path,edits in pending.items():
        old=path.read_bytes();raw=old.decode('utf-8-sig')
        for e in sorted(edits,key=lambda x:x['start'],reverse=True):assert raw[e['start']:e['end']]==e['old'];raw=raw[:e['start']]+e['new']+raw[e['end']:]
        cw.parse(raw);patches.append(write_patch(path,old,encode_like(raw,old),edits,'R3-P'))
    for lang,name in [('french','Services portuaires traditionnels'),('english','Traditional Harbor Services')]:
        raw='l_'+lang+':\n '+PORT_PM+':0 "'+name+'"\n';patches.append(create_file('localization/'+lang+'/1776_tech_r3_harbor_l_'+lang+'.yml',b'\xef\xbb\xbf'+raw.encode('utf8'),'R3-P'))
    dump('PORT_PATCHES.json',patches);print('R3-P: three historical ports use commercial harbor PM; no naval technology grant, levels retained',flush=True)

def install_trade():
    assert (OUT/'PORT_PATCHES.json').exists() and not (OUT/'TRADE_PATCHES.json').exists()
    s=contract.collect_snapshot();assert all('organized_financial_institutions' not in s['starts'][t]['technologies'] for t in FINANCIAL_TAGS)
    raw='# Evidenced credit institutions by 1776; no law or political changes.\nCOUNTRIES = {\n c:PRU ?= { add_technology_researched = organized_financial_institutions }\n c:TUS ?= { add_technology_researched = organized_financial_institutions }\n}\n';cw.parse(raw)
    dump('TRADE_PATCHES.json',[create_file('common/history/countries/zz_1776_tech_r3_financial_foundations.txt',raw.encode('utf8'),'R3-T')]);print('R3-T: one financial foundation each to PRU and TUS; four initial trade centers become compatible without capacity cut',flush=True)

def install_arms_gate():
    assert (OUT/'TRADE_PATCHES.json').exists() and not (OUT/'ARMS_PATCHES.json').exists()
    # Re-read the live shared file. ECON owns recipes and PM groups; only this
    # technology-gate child belongs to TECH. All other current bytes are retained.
    p=ROOT/'common/production_methods/01_industry.txt';old=p.read_bytes();raw=old.decode('utf-8-sig');pm=next(n for n in cw.parse(raw) if n.key=='pm_cannons');parents=pm.children('unlocking_technologies');assert len(parents)==1
    assert r1.values(pm,'unlocking_technologies')==['standardized_field_artillery']
    x=parents[0].children()[0];oldtoken=raw[x.start:x.end];assert oldtoken=='standardized_field_artillery';newtoken='organized_military_establishments';updated=raw[:x.start]+newtoken+raw[x.end:];cw.parse(updated)
    non_gate=lambda n:[qa.signature(x) for x in n.children() if x.key!='unlocking_technologies'];newnode=next(n for n in cw.parse(updated) if n.key=='pm_cannons');assert non_gate(pm)==non_gate(newnode)
    dump('ARMS_PATCHES.json',[write_patch(p,old,encode_like(updated,old),[dict(start=x.start,end=x.end,old=oldtoken,new=newtoken,PM='pm_cannons',scope='UNLOCK_GATE_ONLY_NO_RECIPE_OR_GROUP_EDIT')],'R3-A')]);print('R3-A: traditional cannon PM gate corrected; live ECON recipe and groups untouched. Construction gate remains separate.',flush=True)

def owned_patches():return load(OUT/'PORT_PATCHES.json')+load(OUT/'TRADE_PATCHES.json')+load(OUT/'ARMS_PATCHES.json')
def rescan():
    old=r1.OUT
    try:
        r1.OUT=OUT
        with contextlib.redirect_stdout(io.StringIO()):r1.inspect()
    finally:r1.OUT=old
    b=load(OUT/'CURRENT_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json');s=contract.collect_snapshot()
    technology=[]
    for tag in sorted(set(b['starts'])|set(after['starts'])):
        before=set(b['starts'].get(tag,{}).get('technologies',[]));now=set(after['starts'].get(tag,{}).get('technologies',[]))
        technology.append(dict(TAG=tag,Before=len(before),After=len(now),Added=';'.join(sorted(now-before)),Removed=';'.join(sorted(before-now)),R3_Own_Grant=tag in FINANCIAL_TAGS,New_Concurrent_Tag=tag not in b['starts'],Before_Technologies=';'.join(sorted(before)),After_Technologies=';'.join(sorted(now))))
    csvout('TECH_BEFORE_AFTER.csv',technology)
    with (OUT/'PRIORITY_MATRIX.csv').open(encoding='utf-8-sig',newline='') as f:matrix=list(csv.DictReader(f))
    pmchanges=[]
    for m in matrix:
        key=(m['State'],m['TAG'],m['Building']);selection=s['selected'].get(key,{})
        knowledge=set(s['starts'].get(m['TAG'],{}).get('technologies',[]));missing={pm:sorted(set(r1.values(s['pms'][pm],'unlocking_technologies'))-knowledge) for pm in selection.values() if pm in s['pms'] and set(r1.values(s['pms'][pm],'unlocking_technologies'))-knowledge};construction=sorted(set(r1.values(s['buildings'][m['Building']],'unlocking_technologies'))-knowledge)
        own=m['Action'].startswith(('R3-P','R3-T','R3-A'))
        m.update(After_Missing_PM=json.dumps(missing,sort_keys=True),After_Missing_Construction=';'.join(construction),After_Priority='P0' if missing else 'P1' if construction else '',Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if own and not missing else 'OPEN',Remaining_Limit='CONSTRUCTION_GATE_STILL_OPEN' if own and construction else 'RUNTIME_OPERATION_NOT_CERTIFIED' if own else 'RESEARCH_AND_RUNTIME_REVIEW')
        if own:
            audit_name={'PORT':'PORT_TECH_AUDIT.csv','TRADE':'TRADE_CENTER_TECH_AUDIT.csv','ARMS':'ARMS_INDUSTRY_TECH_AUDIT.csv'}[m['Category']];source=OUT/audit_name.replace('.csv','_BEFORE.csv') if (OUT/audit_name.replace('.csv','_BEFORE.csv')).exists() else OUT/audit_name
            with source.open(encoding='utf-8-sig',newline='') as f:original=next(r for r in csv.DictReader(f) if (r['State'],r['TAG'],r['Building'])==key)
            pmchanges.append(dict(Sub_Lot=m['Action'].split('_')[0],TAG=m['TAG'],State=m['State'],Building=m['Building'],PM_Before=original['Selected_PM'],PM_After=';'.join(selection.values()),PM_Gates_Before=original['Missing_PM_Gates'],PM_Gates_After=json.dumps(missing),Construction_Gate_Remains=';'.join(construction),Last_Declaration_Levels_Before=original['Last_Declaration_Levels'],Status=m['Status']))
    csvout('PRIORITY_MATRIX.csv',matrix);csvout('BUILDING_PM_BEFORE_AFTER.csv',pmchanges)
    impacts=[]
    for tag in sorted(s['starts']):
        known=set(s['starts'][tag]['technologies']);impacts.append(dict(TAG=tag,Cannon_Old_Gate_Met='standardized_field_artillery' in known,Cannon_New_Gates_Met=set(r1.values(s['pms']['pm_cannons'],'unlocking_technologies'))<=known,Port_New_PM_Tech_Eligible=True,Port_Basic_Gate_Met='enclosed_dock_systems' in known,Initial_Port_Scopes=sum(k[1]==tag and k[2]=='building_port' for k in s['selected']),Initial_Cannon_Foundry_Scopes=sum(k[1]==tag and k[2]=='building_artillery_foundry' for k in s['selected']),No_Automatic_Country_Tech_Grant=tag not in FINANCIAL_TAGS))
    csvout('GLOBAL_AVAILABILITY_IMPACT.csv',impacts)
    consumers={}
    for folder in ['common/technology/technologies','common/buildings','common/production_methods','common/laws','common/combat_unit_types']:
        objects,_,_=r1.objects(folder);consumers[folder]=[key for key,n in objects.items() if 'organized_financial_institutions' in r1.values(n,'unlocking_technologies')]
    dump('FINANCIAL_UNLOCK_IMPACT.json',dict(grant_tags=sorted(FINANCIAL_TAGS),technology='organized_financial_institutions',direct_consumers=consumers,descendants_not_automatically_granted=True,laws_or_institutions_not_explicitly_changed=True))
    dump('TAG_CONTRACTS_AFTER.json',{tag:contract.audit_country(tag,s) for tag in sorted(FINANCIAL_TAGS|{t for t,_ in PORT_TARGETS}|{'MUG','MARATH'})})
    # Explicitly recheck the three human-tested R2 trade choices, not a fresh grant.
    witnesses={}
    for state,tag in [('STATE_CEYLON','KND'),('STATE_CIRCARS','CAR'),('STATE_MADRAS','CAR')]:witnesses[tag+'/'+state]=s['selected'][(state,tag,'building_trade_center')]
    dump('R2_TRADE_WITNESSES.json',dict(selected=witnesses,unchanged_and_compatible=all('pm_trade_center_trade_quantity_limited' in p.values() for p in witnesses.values())))
    dump('CURRENT_AFTER.json',dict(inventory=s['inventory'],starts=s['starts'],selected=[dict(state=k[0],tag=k[1],building=k[2],groups=v) for k,v in s['selected'].items()],graph=s['graph']))
    summary=dict(countries=len(after['active_tags']),new_tags=sum(r['Tag_Origin']=='NEW_MOD_TAG' for r in after['rows']),categories_before=dict(C.Counter(r['Status'] for r in b['rows'])),categories_after=dict(C.Counter(r['Status'] for r in after['rows'])),before_declaration_conflicts=len(b['conflicts']),after_declaration_conflicts=len(after['conflicts']),PM_conflicts_after=sum(r['Scope']=='INITIAL_SELECTED_PM' for r in after['conflicts']),construction_conflicts_after=sum(r['Scope']=='INITIAL_BUILDING_CONSTRUCTION_GATE' for r in after['conflicts']),focus_assets_changed=len(pmchanges),focus_priorities_before=dict(C.Counter(r['Priority'] for r in matrix)),focus_priorities_after=dict(C.Counter(r['After_Priority'] for r in matrix if r['After_Priority'])),country_technology_additions=sum(len(r['Added'].split(';')) for r in technology if r['Added'] and r['R3_Own_Grant']),technology_changes=[r for r in technology if r['Added'] or r['Removed']],cannon_parent_eligible_before=sum(r['Cannon_Old_Gate_Met'] for r in impacts),cannon_parent_eligible_after=sum(r['Cannon_New_Gates_Met'] for r in impacts),automated_engine_test=False)
    dump('SUMMARY.json',summary);print(json.dumps({k:v for k,v in summary.items() if k!='technology_changes'}),flush=True)

def refresh_focus_tables():
    global OUT
    original=OUT
    for name in ['PORT_TECH_AUDIT.csv','TRADE_CENTER_TECH_AUDIT.csv','ARMS_INDUSTRY_TECH_AUDIT.csv']:
        before=original/name.replace('.csv','_BEFORE.csv')
        if not before.exists():before.write_bytes((original/name).read_bytes())
    stage=original/'AFTER_FOCUS';stage.mkdir(exist_ok=True)
    try:
        OUT=stage;audit()
    finally:OUT=original
    for name in ['PORT_TECH_AUDIT.csv','TRADE_CENTER_TECH_AUDIT.csv','ARMS_INDUSTRY_TECH_AUDIT.csv']:
        with (original/name.replace('.csv','_BEFORE.csv')).open(encoding='utf-8-sig',newline='') as f:before={(r['State'],r['TAG'],r['Building']):r for r in csv.DictReader(f)}
        with (stage/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        for r in rows:
            b=before.get((r['State'],r['TAG'],r['Building']));r.update(Original_PM=b['Selected_PM'] if b else '',Original_Missing_PM_Gates=b['Missing_PM_Gates'] if b else '',New_Independent_World_Scope=b is None,Snapshot='CURRENT_AFTER_R3')
        csvout(name,rows)
    (OUT/'FOCUS_AFTER.json').write_bytes((stage/'FOCUS_BEFORE.json').read_bytes());(OUT/'CURRENT_FOCUS_PRIORITY_MATRIX.csv').write_bytes((stage/'PRIORITY_MATRIX.csv').read_bytes())
    summary=load(OUT/'SUMMARY.json');summary['focus_assets_after']=load(OUT/'FOCUS_AFTER.json')['categories'];dump('SUMMARY.json',summary)
    print('Complete focus tables refreshed, including independent new Ragusa; original tables retained',flush=True)

def economics():
    pms,src,_=r1.objects('common/production_methods');goods,gs,_=r1.objects('common/goods');prices={g:float(r1.val(n,'cost','0')) for g,n in goods.items()};rows=[]
    for pm in ['pm_anchorage','pm_basic_port',PORT_PM,'pm_trade_center','pm_trade_center_trade_quantity_normal','pm_trade_center_trade_quantity_limited','pm_cannons']:
        params=numeric_sum([pm],pms);ins,outs,jobs=flows(params);gross=sum(prices[g]*q for g,q in outs.items())-sum(prices[g]*q for g,q in ins.items());rows.append(dict(PM=pm,Source=src[pm],Inputs=json.dumps(ins,sort_keys=True),Outputs=json.dumps(outs,sort_keys=True),Nominal_Jobs=sum(jobs.values()),Job_Mix=json.dumps(jobs,sort_keys=True),Base_Price_Input_Cost=sum(prices[g]*q for g,q in ins.items()),Base_Price_Output_Value=sum(prices[g]*q for g,q in outs.items()),Gross_Before_Wages=gross,Parameters=json.dumps(params,sort_keys=True),Limitation='Per-level full-workforce parameters; trade service fees, throughput, wages, market prices and actual operation are not simulated.'))
    csvout('ECONOMIC_PARAMETERS.csv',rows);sensitivity=[]
    for pm in ['pm_basic_port',PORT_PM]:
        params=numeric_sum([pm],pms);ins,outs,jobs=flows(params);employment=sum(jobs.values())
        for im,om in [(1,1),(1.25,1),(1,.75),(.75,1),(1,1.25)]:
            for wage in [0,.05,.10,.15]:
                revenue=sum(prices[g]*q*om for g,q in outs.items());cost=sum(prices[g]*q*im for g,q in ins.items());sensitivity.append(dict(PM=pm,Input_Price_Multiplier=im,Output_Price_Multiplier=om,Assumed_Weekly_Blended_Wage_Per_Worker=wage,Revenue=revenue,Goods_Cost=cost,Assumed_Wages=employment*wage,Illustrative_Net=revenue-cost-employment*wage,Not_Engine_Income=True))
    csvout('PORT_COST_SENSITIVITY.csv',sensitivity)
    s=contract.collect_snapshot();supply=[]
    for tag,state in sorted(PORT_TARGETS):
        candidates=[]
        for key,selection in s['selected'].items():
            if key[1]!=tag:continue
            ins,outs,jobs=flows(numeric_sum(selection.values(),s['pms']))
            relevant={g:v for g,v in outs.items() if g in {'wood','fabric'} and v>0}
            if relevant:candidates.append(dict(state=key[0],building=key[2],output_per_level=relevant))
        subsistence=[pm for pm in pms if 'subsistence' in pm and set(flows(numeric_sum([pm],pms))[1])&{'wood','fabric'}]
        supply.append(dict(TAG=tag,State=state,Required_Goods='wood;fabric',New_Inputs_Per_Level='wood:9;fabric:3',Old_Nominal_Input_Per_Level='clippers:6',Own_Explicit_Producer_Sources=json.dumps(candidates,sort_keys=True),Existing_Subsistence_Recipe_Sources=';'.join(subsistence),Industrial_Shipyard_Required=False,Imports_Market_Stock_Workforce_Unknown=True,Input_Access_Guaranteed=False))
    csvout('PORT_INPUT_ACCESS_REVIEW.csv',supply)
    dump('ECONOMIC_RECIPE_SNAPSHOT.json',{pm:dict(source=src[pm],signature=qa.signature(pms[pm])) for pm in ['pm_cannons','pm_muskets',PORT_PM,'pm_basic_port','pm_trade_center_trade_quantity_normal']})
    print('Current recipes, port wage/price sensitivity and conditional clipper supply recorded; no invented runtime profit',flush=True)

def concurrent_review(current):
    baseline=load(OUT/'BASELINE.json');owned={r['file'] for r in owned_patches()};external={p:dict(before=baseline['hashes'].get(p),after=current.get(p)) for p in set(baseline['hashes'])|set(current) if baseline['hashes'].get(p)!=current.get(p) and p not in owned}
    world_source=ROOT/'docs/reports/map/WORLD_1776_CLOSURE/BALKANS-02/FILES_MODIFIED.json';world={r['file']:r for r in load(world_source)} if world_source.exists() else {};world_ok={p:dict(source=world_source.relative_to(ROOT).as_posix(),before_matches=baseline['hashes'].get(p)==row['before'],after_matches=current.get(p)==row['after']) for p,row in world.items() if p in external}
    econ_source=ROOT/'docs/reports/economy/ALLOYS_1776_REBALANCE/FILES_MODIFIED.json';econ_scope=set();econ_info=None
    if (ROOT/'tools/econ_alloys_1776.py').exists():
        import econ_alloys_1776 as econ
        econ_scope=set(econ.OWNED)
        if (OUT/'POST_TEST_CONCURRENT_REVIEW.json').exists():econ_scope.update(load(OUT/'POST_TEST_CONCURRENT_REVIEW.json')['reviewed_additional_ECON_paths'])
        econ_info=dict(tool='tools/econ_alloys_1776.py',tool_sha256=sha(ROOT/'tools/econ_alloys_1776.py'),report_directory=econ.OUT.relative_to(ROOT).as_posix(),receipt_exists=econ_source.exists(),receipt_sha256=sha(econ_source) if econ_source.exists() else None,owned_paths=sorted(econ_scope),our_cannon_gate_file_not_in_ECON_owned='common/production_methods/01_industry.txt' not in econ_scope)
    unreviewed=set(external)-set(world_ok)-econ_scope
    unknown_technology_country_changes=[]
    before=load(OUT/'CURRENT_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json')
    for tag in set(before['starts'])&set(after['starts'])-FINANCIAL_TAGS:
        if before['starts'][tag]['technologies']!=after['starts'][tag]['technologies']:unknown_technology_country_changes.append(tag)
    result=dict(external_runtime=external,WORLD_verified_files=world_ok,ECON=econ_info,ECON_external_files=sorted(set(external)&econ_scope),unreviewed_external_paths=sorted(unreviewed),new_independent_tags=sorted(set(after['starts'])-set(before['starts'])),unexpected_existing_country_knowledge_changes=unknown_technology_country_changes,R2_current_file_drift={p:dict(delivered=h,current=current.get(p)) for p,h in load(r2.OUT/'FILES_MODIFIED.json')['sha256'].items() if current.get(p)!=h},policy='Current bytes retained. TECH writes only paths and edits listed in its own patch receipts. WORLD/ECON delivery and documentation remain independent; no baseline restore.',territorial_tracking_written_by_TECH=False)
    if world_source.exists():
        (OUT/'WORLD_BALKANS02_MANIFEST_READ_ONLY_COPY.json').write_bytes(world_source.read_bytes());p=world_source.parent/'VALIDATION.json'
        result['WORLD_validation_observed']=dict(sha256=sha(p),status=load(p).get('status'),passed=load(p).get('passed'),total=load(p).get('total')) if p.exists() else None
    dump('CONCURRENT_CHANGES.json',result);return result

def static():
    b=load(OUT/'BASELINE.json');after=load(OUT/'RESOLVED_AFTER.json');before=load(OUT/'CURRENT_BEFORE.json');data=load(OUT/'CURRENT_AFTER.json');current=r1.runtime.runtime_hashes();concurrency=concurrent_review(current);checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    owned=owned_patches();ck('Eight authorized functional paths only',len(owned)==8 and not any(r['file'].startswith(('map_data/','common/history/states/','common/history/pops/','common/country_definitions/','common/laws/','common/history/diplomacy/')) for r in owned))
    ck('Every external functional delta belongs to observed WORLD or ECON scope',not concurrency['unreviewed_external_paths'])
    ck('WORLD files match both baseline and its own delivered changes',all(r['before_matches'] and r['after_matches'] for r in concurrency['WORLD_verified_files'].values()))
    ck('ECON has a distinct recipe and group scope',concurrency['ECON'] is not None and concurrency['ECON']['our_cannon_gate_file_not_in_ECON_owned'])
    for r in owned:
        p=ROOT/r['file'];ck('Own delivered SHA '+r['file'],sha(p)==r['after_sha256'])
        if r.get('created'):ck('New path was absent at entry '+r['file'],r['file'] not in b['hashes'])
        else:
            old=(ROOT/r['preimage']).read_bytes();text=old.decode('utf-8-sig')
            for e in sorted(r['edits'],key=lambda e:e['start'],reverse=True):assert text[e['start']:e['end']]==e['old'];text=text[:e['start']]+e['new']+text[e['end']:]
            ck('Only reviewed current-byte edits '+r['file'],sha(ROOT/r['preimage'])==r['before_sha256'] and p.read_bytes()==encode_like(text,old))
        if p.suffix=='.txt':cw.parse(p.read_text(encoding='utf-8-sig'));ck('Paradox syntax '+r['file'],True)
        elif p.suffix=='.yml':
            lang='french' if '/french/' in r['file'] else 'english';raw=p.read_bytes();ck('Localization BOM header unique '+lang,raw.startswith(b'\xef\xbb\xbf') and raw.decode('utf-8-sig').startswith('l_'+lang+':') and sum(len(re.findall(r'^\s*'+PORT_PM+r':',q.read_text(encoding='utf-8-sig',errors='replace'),re.M)) for q in (ROOT/'localization'/lang).rglob('*.yml'))==1)
    s=contract.collect_snapshot();pms=s['pms'];groups=s['groups']
    ck('Current knowledge equals surveyed snapshot',all(v['technologies']==after['starts'][t]['technologies'] for t,v in s['starts'].items()) and set(s['starts'])==set(after['starts']))
    ck('Only PRU TUS receive one financial root',not concurrency['unexpected_existing_country_knowledge_changes'] and all(set(after['starts'][t]['technologies'])==set(before['starts'][t]['technologies'])|{'organized_financial_institutions'} for t in FINANCIAL_TAGS))
    ck('Only new country RAG comes from independent WORLD',concurrency['new_independent_tags']==['RAG'] and 'common/history/countries/1776_world_b02_ragusa.txt' in concurrency['WORLD_verified_files'])
    ck('No unknown technology unresolved effect or prerequisite debt',all(set(v['technologies'])<=set(s['graph']) and not v['unresolved'] for v in s['starts'].values()) and not r1.graph_debts(after))
    ck('Technology graph and eras unchanged by R3',before['graph']==after['graph'] and before['tech_eras']==after['tech_eras'])
    def cyclic(k,trail=()):return k in trail or any(cyclic(p,trail+(k,)) for p in s['graph'][k])
    ck('Graph has known parents and no cycle',all(p in s['graph'] for parents in s['graph'].values() for p in parents) and not any(cyclic(k) for k in s['graph']))
    ck('Accepted alloy parents intact',set(s['graph']['alloysworking'])=={'shaft_mining','organized_workshops'})
    ck('New port PM in exactly its intended group',[g for g,n in groups.items() if PORT_PM in r1.values(n,'production_methods')]==['pmg_base_building_port'])
    ck('Port group old relative order and default choices retained',r1.values(groups['pmg_base_building_port'],'production_methods')==['pm_anchorage',PORT_PM,'pm_basic_port','pm_industrial_port','pm_modern_port'] and r1.val(pms[PORT_PM],'is_default') is None and not r1.values(pms[PORT_PM],'unlocking_technologies'))
    for tag,state in sorted(PORT_TARGETS):
        selected=s['selected'][(state,tag,'building_port')];known=set(s['starts'][tag]['technologies'])
        ck('Both commercial and neutral-data PM selected '+tag,selected.get('pmg_base_building_port')==PORT_PM and selected.get('pmg_1776_raw_data_reporting')=='pm_1776_no_raw_data_reporting' and all(not(set(r1.values(pms[pm],'unlocking_technologies'))-known) for pm in selected.values()))
        ck('No naval root or enclosed docks gifted '+tag,s['starts'][tag]['technologies']==before['starts'][tag]['technologies'])
    oldgate=(ROOT/load(OUT/'ARMS_PATCHES.json')[0]['preimage']).read_text(encoding='utf-8-sig');oldpm=next(n for n in cw.parse(oldgate) if n.key=='pm_cannons');newpm=pms['pm_cannons'];non_gate=lambda n:[qa.signature(x) for x in n.children() if x.key!='unlocking_technologies']
    ck('Cannon economic recipe identical to exact live preimage',non_gate(oldpm)==non_gate(newpm))
    ck('Cannon PM only needs military organization',r1.values(newpm,'unlocking_technologies')==['organized_military_establishments'])
    ck('No previous cannon technology eligibility lost anywhere',all('standardized_field_artillery' not in set(v['technologies']) or set(r1.values(newpm,'unlocking_technologies'))<=set(v['technologies']) for v in s['starts'].values()))
    for tag,state in [('MUG','STATE_DELHI'),('MARATH','STATE_AGRA')]:
        ck('Existing traditional foundry can select current cannon PM '+tag,'pm_cannons' in s['selected'][(state,tag,'building_artillery_foundry')].values() and set(r1.values(newpm,'unlocking_technologies'))<=set(s['starts'][tag]['technologies']))
        ck('No standardized artillery or industrial knowledge gifted '+tag,s['starts'][tag]['technologies']==before['starts'][tag]['technologies'] and 'standardized_field_artillery' not in s['starts'][tag]['technologies'])
    ck('Foundry construction retains separate standardization gate',r1.values(s['buildings']['building_artillery_foundry'],'unlocking_technologies')==['standardized_field_artillery'])
    ck('Three human-tested R2 trade choices compatible and unchanged',load(OUT/'R2_TRADE_WITNESSES.json')['unchanged_and_compatible'])
    ck('Original R1 and accepted R2 proofs unchanged',all(sha(ROOT/p)==h for field in ['R1_proofs','R2_proofs'] for p,h in b[field].items()))
    ck('R1 R2 human receipts PASS and version bounded',all(load(folder/'AUDIT_STATE.json')['status']=='PASS_RUNTIME_USER_VALIDATED' for folder in [r1.OUT,r2.OUT]) and load(OUT/'R2_ACCEPTANCE.json')['subsequent_revisions_not_validated'])
    ck('All SERG proof and state bytes preserved',all(sha(ROOT/p)==h for p,h in b['SERG_proofs'].items()) and load(r1.rm.OUT/'ROADMAP_STATE.json')==b['SERG_state'])
    ck('SERG canonical validator PASS',r1.rm.check()['status']=='PASS')
    ck('Military unit declarations unchanged',s['inventory']['units']==b['inventory']['units'])
    ck('World total written population conserved despite independent transfer',sum(x['count'] for x in s['inventory']['pops'])==sum(x['count'] for x in b['inventory']['pops']))
    goods,_,_=r1.objects('common/goods');unknown=set()
    for pm in [PORT_PM,'pm_cannons','pm_basic_port','pm_trade_center_trade_quantity_normal']:
        ins,outs,_=flows(numeric_sum([pm],pms));unknown|=(set(ins)|set(outs))-set(goods)
    ck('Affected recipe goods exist in effective catalog',not unknown)
    ins,outs,jobs=flows(numeric_sum([PORT_PM],pms));ck('Port uses existing basic materials and positive service output',ins=={'wood':9,'fabric':3} and outs=={'merchant_marine':6} and sum(jobs.values())==700)
    ck('Old ports and modern alternatives not deleted',all(k in pms for k in ['pm_anchorage','pm_basic_port','pm_industrial_port','pm_modern_port']))
    ck('Reused port texture exists',(GAME/'gfx/interface/icons/production_method_icons/anchorage.dds').exists() or (ROOT/'gfx/interface/icons/production_method_icons/anchorage.dds').exists())
    ck('Version executable target corroborated',load(OUT/'VERSION_EVIDENCE.json')['product_version']=='1.13.11' and '1.13.*' in load(OUT/'VERSION_EVIDENCE.json')['target'])
    ck('Git HEAD branch index preserved',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    ck('Old core audits and their tests preserved',all(sha(ROOT/p)==b['tools'][p] for p in ['tools/audit_starting_tech_1776.py','tools/audit_starting_tech_1776_r2.py','tools/validate_starting_technology_1776.py','tools/test_starting_tech_audit_1776.py','tools/test_starting_tech_audit_1776_r2.py']))
    ck('No fabricated R3 human receipt',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    current=r1.runtime.runtime_hashes();dump('SESSION_AFTER_STATIC.json',dict(hashes=current,inventory=s['inventory'],git=b['git'],WORLD_new_tag='RAG',static_only=True))
    vanilla={str(p):sha(p) for folder in ['common/goods','common/pop_types','common/production_methods','common/buildings','common/production_method_groups'] for p in r1.effective(folder) if p.is_relative_to(GAME)};dump('VANILLA_INPUTS.json',vanilla)
    dump('FILES_MODIFIED.json',dict(runtime_files=[r['file'] for r in owned],sha256={r['file']:current[r['file']] for r in owned},own_country_technology_additions=dict(PRU=['organized_financial_institutions'],TUS=['organized_financial_institutions']),history_port_base_PM_replacements=3,explicit_neutral_data_selections=3,artillery_gate_change=True,artillery_recipe_or_group_change=False,territory_or_population_write=False,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',human_validation=None))
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),failed=[r['name'] for r in checks if not r['passed']],checks=checks,automated_engine_test=False,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',human_validation=None);dump('TEST_RESULTS.json',result);print(result['passed'],'/',result['total'],result['failed'],flush=True);assert not result['failed']

def tests():
    import serg_sc4_ligurian_fiefs as lig
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden','test_serg_sc1_passau_outliers','test_serg_versioned_receipts','test_serg_sc1_regensburg_demography','test_start_economy_2026_10_15','test_starting_tech_audit_1776','test_starting_tech_audit_1776_r2','test_starting_tech_audit_1776_r3']
    for label,names in [('TARGETED_TESTS',['test_starting_tech_audit_1776_r3']),('CUMULATIVE_TESTS',modules)]:
        stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names));failed=[dict(id=t.id(),traceback=trace) for t,trace in result.failures+result.errors];(OUT/(label+'.log')).write_bytes(stream.getvalue().encode('utf8'));dump(label+'.json',dict(total=result.testsRun,passed=result.testsRun-len(failed)-len(result.skipped),failed=failed,skipped=[dict(id=t.id(),reason=reason) for t,reason in result.skipped],automated_engine_test=False));print(label,result.testsRun-len(failed)-len(result.skipped),'/',result.testsRun,'failures',len(failed),flush=True)

def repair_report_routing():
    assert not (OUT/'REPORT_ROUTING_REPAIR.json').exists()
    for n in ['FOCUS_BEFORE.json','TAG_CONTRACTS_BEFORE.json']:(OUT/('MISROUTED_AFTER_'+n)).write_bytes((OUT/n).read_bytes())
    b=load(OUT/'CURRENT_BEFORE.json');matrix=[];categories={};unknown=set();goods,_,_=r1.objects('common/goods')
    for category,name in [('PORT','PORT_TECH_AUDIT_BEFORE.csv'),('TRADE','TRADE_CENTER_TECH_AUDIT_BEFORE.csv'),('ARMS','ARMS_INDUSTRY_TECH_AUDIT_BEFORE.csv')]:
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        categories[category]=dict(assets=len(rows),PM_conflicts=sum(r['Missing_PM_Gates']!='{}' for r in rows),construction_conflicts=sum(bool(r['Missing_Construction_Gates']) for r in rows))
        for r in rows:
            unknown|=(set(json.loads(r['Selected_Recipe_Inputs']))|set(json.loads(r['Selected_Recipe_Outputs'])))-set(goods)
            if r['Missing_PM_Gates']!='{}' or r['Missing_Construction_Gates']:matrix.append(r)
    dump('FOCUS_BEFORE.json',dict(categories=categories,priority_rows=len(matrix),priorities=dict(C.Counter(r['Priority'] for r in matrix)),unknown_selected_goods=sorted(unknown),current_country_count=len(b['starts']),all_knowledge={t:v['technologies'] for t,v in b['starts'].items()},selection_model='Last explicit method per group; declaration level/count is not a certified engine merge result.',reconstructed_from_frozen_before_CSV_and_country_snapshot=True))
    s=contract.collect_snapshot();s['inventory']=load(OUT/'BASELINE.json')['inventory'];s['pms']['pm_cannons']=next(n for n in cw.parse((ROOT/load(OUT/'ARMS_PATCHES.json')[0]['preimage']).read_text(encoding='utf-8-sig')) if n.key=='pm_cannons')
    for t in FINANCIAL_TAGS|{x[0] for x in PORT_TARGETS}|{'MUG','MARATH'}:
        s['starts'][t]=copy.deepcopy(b['starts'][t]);s['starts'][t]['history']=[x['file'] for x in b['starts'][t]['history']]
    for tag,state in PORT_TARGETS:s['selected'][(state,tag,'building_port')]={'pmg_base_building_port':'pm_basic_port'}
    dump('TAG_CONTRACTS_BEFORE.json',{t:contract.audit_country(t,s) for t in sorted(FINANCIAL_TAGS|{x[0] for x in PORT_TARGETS}|{'MUG','MARATH'})})
    dump('REPORT_ROUTING_REPAIR.json',dict(problem='Python default argument captured initial report directory during AFTER_FOCUS redirection. Two derived BEFORE JSON views were overwritten; original CSV and CURRENT_BEFORE/BASELINE snapshots stayed intact.',corrected='dump resolves OUT at call time. Reconstructed both derived before views from frozen original CSV, country snapshot and exact preimage of cannon PM. Misrouted after views preserved separately.',gameplay_files_affected=False,R1_R2_or_territorial_proofs_affected=False,sources=['CURRENT_BEFORE.json','BASELINE.json','PORT_TECH_AUDIT_BEFORE.csv','TRADE_CENTER_TECH_AUDIT_BEFORE.csv','ARMS_INDUSTRY_TECH_AUDIT_BEFORE.csv','ARMS_PATCHES.json']))
    print('Derived report routing repaired from frozen source proofs; no gameplay or protected proof change',flush=True)

def refine_port_input_access():
    assert not (OUT/'PORT_INPUT_REFINEMENT.json').exists()
    (OUT/'PORT_PATCHES_BEFORE_INPUT_REVIEW.json').write_bytes((OUT/'PORT_PATCHES.json').read_bytes())
    for n in ['ECONOMIC_PARAMETERS.csv','PORT_COST_SENSITIVITY.csv','PORT_INPUT_ACCESS_REVIEW.csv','ECONOMIC_RECIPE_SNAPSHOT.json']:
        if (OUT/n).exists():(OUT/('FIRST_PORT_RECIPE_'+n)).write_bytes((OUT/n).read_bytes())
    p=ROOT/'common/production_methods/1776_tech_r3_commercial_harbor.txt';old=p.read_bytes();raw=old.decode('utf8');needle='goods_input_clippers_add = 4';assert raw.count(needle)==1;start=raw.index(needle);replacement='goods_input_wood_add = 9\n   goods_input_fabric_add = 3';updated=raw[:start]+replacement+raw[start+len(needle):];cw.parse(updated)
    change=write_patch(p,old,updated.encode('utf8'),[dict(start=start,end=start+len(needle),old=needle,new=replacement,reason='KOR/SUL have no declared industrial shipyard and isolationism requests. Use local wood/fabric subsistence inputs; no law, market or shipyard creation. Base-price input cost stays 240.')],'R3-P_INPUT_REVIEW');dump('PORT_INPUT_REFINEMENT.json',change)
    patches=load(OUT/'PORT_PATCHES.json');item=next(r for r in patches if r['file']==p.relative_to(ROOT).as_posix());item['after_sha256']=sha(p);item['input_review']='PORT_INPUT_REFINEMENT.json';dump('PORT_PATCHES.json',patches)
    print('Traditional port inputs refined to wood9/fabric3; same base cost, no industrial clipper dependency. Previous recipe evidence archived.',flush=True)

def refine_cannon_global_review():
    assert not (OUT/'ARMS_GATE_REFINEMENT.json').exists()
    for n in ['TARGETED_TESTS.json','TARGETED_TESTS.log','CUMULATIVE_TESTS.json','CUMULATIVE_TESTS.log','TEST_RESULTS.json','GLOBAL_AVAILABILITY_IMPACT.csv','SUMMARY.json']:
        p=OUT/n
        if p.exists():(OUT/('FIRST_GATE_'+n)).write_bytes(p.read_bytes())
    (OUT/'ARMS_PATCHES_FIRST_GATE.json').write_bytes((OUT/'ARMS_PATCHES.json').read_bytes())
    p=ROOT/'common/production_methods/01_industry.txt';old=p.read_bytes();raw=old.decode('utf-8-sig');pm=next(n for n in cw.parse(raw) if n.key=='pm_cannons');assert r1.values(pm,'unlocking_technologies')==['organized_military_establishments','organized_workshops'];tokens=pm.children('unlocking_technologies')[0].children();start=tokens[0].end;end=tokens[1].end;removed=raw[start:end];assert removed.strip()=='organized_workshops';new=raw[:start]+raw[end:];cw.parse(new)
    refinement=write_patch(p,old,encode_like(new,old),[dict(start=start,end=end,old=removed,new='',reason='Avoid withdrawing prior availability from GAL and MLT; workshops not a universal necessary condition for this traditional existing-foundry PM.')],'R3-A_GLOBAL_REVIEW');dump('ARMS_GATE_REFINEMENT.json',refinement)
    original=load(OUT/'ARMS_PATCHES.json');original[0]['edits'][0]['new']='organized_military_establishments';original[0]['after_sha256']=sha(p);original[0]['global_review']='ARMS_GATE_REFINEMENT.json';dump('ARMS_PATCHES.json',original)
    print('Cannon gate refined after exhaustive impact review: military organization only; no prior country eligibility withdrawn. First results archived.',flush=True)

def review_post_test_ECON():
    assert not (OUT/'POST_TEST_CONCURRENT_REVIEW.json').exists()
    (OUT/'FINAL_PRE_CONCURRENT_CHECK.json').write_bytes((OUT/'FINAL_CHECKS.json').read_bytes())
    before=load(OUT/'SESSION_AFTER_STATIC.json')['hashes'];current=r1.runtime.runtime_hashes();d={p:dict(before=before.get(p),after=current.get(p)) for p in set(before)|set(current) if before.get(p)!=current.get(p)}
    import econ_alloys_1776 as econ
    extra={'common/goods/1776_hardware.txt','common/modifier_type_definitions/1776_hardware.txt','gui/1776_hardware_texticons.gui','gfx/interface/icons/goods_icons/aor1776_hardware.dds'}
    assert set(d)<=set(econ.OWNED)|extra and not(set(d)&{p['file'] for p in owned_patches()})
    pms,_,_=r1.objects('common/production_methods');snap=load(OUT/'ECONOMIC_RECIPE_SNAPSHOT.json');preserved={pm:qa.signature(pms[pm])==r['signature'] for pm,r in snap.items()};assert all(preserved.values())
    for rel in d:
        p=ROOT/rel
        if p.suffix in {'.txt','.gui'}:cw.parse(p.read_text(encoding='utf-8-sig'))
    goods,_,_=r1.objects('common/goods');assert 'aor1776_hardware' in goods
    # This is evidence of the peer's evolving scope, not an instruction to do its work.
    dump('POST_TEST_CONCURRENT_REVIEW.json',dict(status='COMPATIBLE_WITH_UNCHANGED_TECH_R3_PATCHES',functional_delta=d,reviewed_additional_ECON_paths=sorted(extra),context_source=dict(thread_id='01a080b1-616e-71b2-85c3-0d7759724725',thread_title='Fix cement technology chain',observed_request='New basic hardware good, larger utensil recipes, alloy input at first tier, transparent supplied icon'),economic_PM_signatures_preserved=preserved,R3_functional_files_unchanged=True,cumulative_suite_reexecuted_for_this_revision=False,peer_delivery_not_approved_by_TECH=True,peer_runtime_validation_not_invented=True))
    print('Post-test ECON hardware evolution reviewed; all R3 economic PMs and eight own files unchanged',flush=True)

def retest_current_composition():
    for name in ['TEST_RESULTS.json','SESSION_AFTER_STATIC.json','TARGETED_TESTS.json','TARGETED_TESTS.log']:(OUT/('PRE_HARDWARE_'+name)).write_bytes((OUT/name).read_bytes())
    static()
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_starting_tech_audit_1776_r3'));failed=[dict(id=t.id(),traceback=trace) for t,trace in result.failures+result.errors];(OUT/'TARGETED_TESTS.log').write_bytes(stream.getvalue().encode('utf8'));dump('TARGETED_TESTS.json',dict(total=result.testsRun,passed=result.testsRun-len(failed)-len(result.skipped),failed=failed,skipped=[dict(id=t.id(),reason=reason) for t,reason in result.skipped],automated_engine_test=False,current_ECON_composition_rechecked=True));assert not failed
    reports()
    p=OUT/'REPORT.md';raw=p.read_bytes();text=raw.decode('utf8');text+='\nUne évolution indépendante postérieure d’ECON ajoute la quincaillerie, son icône et ses recettes. Les huit fichiers TECH et les signatures de nos procédés économiques restent identiques. POST_TEST_CONCURRENT_REVIEW.json documente les huit évolutions observées et le périmètre supplémentaire ; aucun de ces fichiers n’est écrit par TECH. Les 66 contrôles statiques et 41 tests ciblés ont été réexécutés sur cette composition. La suite cumulative 596/609 reste celle de PRE_HARDWARE_SESSION_AFTER_STATIC.json : elle n’est pas présentée comme réexécutée après cette évolution externe. Les douze assertions classées et l’exclusion demeurent visibles.\n';p.write_bytes(text.encode('utf8'))
    with (OUT/'PROGRESS_HISTORY.md').open('ab') as f:f.write('- 2026-10-24 — R3-007 : évolution externe Quincaillerie d’ECON conservée ; aucun fichier TECH modifié. Contrôle de coexistence, 66 statiques et 41 ciblés réexécutés ; suite cumulative précédente conservée avec son instantané, sans nouvelle prétention d’exécution.\n'.encode('utf8'))
    print('Current composition: static and targeted tests rerun; prior cumulative snapshot explicitly distinguished',flush=True)

def doc(name,text):(OUT/name).write_bytes(text.encode('utf8'))
def reports():
    summary=load(OUT/'SUMMARY.json');v=load(OUT/'TEST_RESULTS.json');target=load(OUT/'TARGETED_TESTS.json');cumulative=load(OUT/'CUMULATIVE_TESTS.json')
    old={r['id'] for r in load(r2.OUT/'CUMULATIVE_TESTS.json')['failed']};receipt_assertion='test_starting_tech_audit_1776_r2.R2Delivery.test_r2_still_awaits_user_and_has_no_new_receipt';allowed=old|{receipt_assertion};new=[r for r in cumulative['failed'] if r['id'] not in allowed]
    review=[dict(id=r['id'],classification='OBSOLETE_AFTER_GENUINE_R2_ATTESTATION' if r['id']==receipt_assertion else 'PREEXISTING_R2_CLASSIFIED_ASSERTION' if r['id'] in old else 'NEW_FAILURE_REQUIRES_INVESTIGATION') for r in cumulative['failed']]
    dump('CUMULATIVE_TEST_REVIEW.json',dict(failed=review,new_unexplained_failures=[r['id'] for r in new],old_tests_modified=False,R2_real_attestation_causes_one_obsolete_absence_assertion=any(r['id']==receipt_assertion for r in cumulative['failed'])));assert not target['failed'] and not new
    contracts=load(OUT/'TAG_CONTRACTS_AFTER.json')
    csvout('P3_RESEARCH_HANDOFFS.csv',[dict(TAG=t,Priority='P3',Question='Verify actual active commercial regime and runtime market access; requests alone do not certify active law.',Requested_Laws=';'.join(contracts[t]['law_requests']),Source='TAG_CONTRACTS_AFTER.json',Owner='POLITICAL_OR_MARKET_REVIEW',Direct_TECH_Law_Change=False,Runtime_Validated=False) for t in ['JAP','KOR','SUL']])
    v.update(targeted=dict(passed=target['passed'],total=target['total'],failed=len(target['failed'])),cumulative=dict(passed=cumulative['passed'],total=cumulative['total'],classified_assertions=len(cumulative['failed']),skipped=len(cumulative['skipped']),new_unexplained_failures=0));dump('TEST_RESULTS.json',v)
    with (OUT/'BUILDING_PM_BEFORE_AFTER.csv').open(encoding='utf-8-sig',newline='') as f:changes=list(csv.DictReader(f))
    table='\n'.join('| '+r['TAG']+' | '+r['State'].removeprefix('STATE_')+' | '+r['Building'].removeprefix('building_')+' | '+('Port traditionnel + données désactivées' if r['Sub_Lot']=='R3-P' else 'Commerce normal conservé ; socle financier ajouté' if r['Sub_Lot']=='R3-T' else 'Canons conservés ; gate organisation militaire')+' |' for r in changes)
    before=load(OUT/'CURRENT_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json');tech_table='\n'.join('| '+t+' | '+str(len(before['starts'][t]['technologies']))+' | '+str(len(after['starts'][t]['technologies']))+' | organized_financial_institutions |' for t in sorted(FINANCIAL_TAGS))
    counts=load(OUT/'FOCUS_AFTER.json')['categories'];concurrency=load(OUT/'CONCURRENT_CHANGES.json');global_count=summary['cannon_parent_eligible_after']
    doc('HISTORICAL_DECISIONS.md','''# TECH-R3 — décisions et limites historiques

Référence : 1er janvier 1776. Aucun contrôle statique ne certifie une rentabilité, un marché ou une production effectivement observés. Les sources établissent des capacités qualitatives ; les coefficients de recettes sont des approximations de jeu B.

## Ports commerciaux et établissements navals

Les 18 déclarations initiales en conflit utilisent `pm_basic_port`, qui exige `enclosed_dock_systems`, lui-même enfant de `state_dockyard_systems`. Cela ne prouve ni l’absence d’un port historique ni une production nulle en jeu. Les noms et descriptions du mod associent ce dernier ensemble à des établissements navals et des bassins protégés. Un commerce maritime ancien ne justifie pas automatiquement tout cet appareil militaire.

Trois cas sont installés : JAP/Kyushu, KOR/Busan, SUL/Mindanao. Les niveaux existants 2/1/1, les propriétaires économiques, les emplacements et les réserves sont conservés. La source concernant Jolo étaye le rôle commercial du sultanat SUL, sans prétendre établir le pixel ou le hub exact du port de Mindanao.

- [Ville de Nagasaki : port international](https://www.city.nagasaki.lg.jp/uploaded/attachment/4724.pdf), texte municipal indexé : activité internationale depuis le XVIe siècle, contacts chinois et néerlandais encadrés au XVIIIe. Ces restrictions ne signifient pas une absence de commerce. Aucun débit réel de 1776 n’est déduit du nombre de navires.
- [Douane de Busan : commerce du waegwan](https://customs.go.kr/busan/cm/cntnts/cntntsView.do?cntntsId=2386&mi=7394), page officielle consultée : site de Choryang à partir de 1678, échanges réglementés antérieurs à l’ouverture de 1876. La source ne justifie pas un chantier naval industriel national.
- [Poggio, Lopez et Tremml-Werner, recherche originale](https://onlinelibrary.wiley.com/doi/10.1111/aehr.70030), introduction et contexte consultés : réseau maritime de Sulu déjà établi au début du XVIIIe siècle. L’objet principal de l’étude est 1836 : aucune clause de ce traité, frontière ou quantité du XIXe n’est rétroprojetée en 1776. La notice [Warren 1977](https://archium.ateneo.edu/phstudies/vol25/iss1/4/) est une piste bibliographique, pas une lecture intégrale de son PDF.

Le nouveau procédé `pm_aor1776_traditional_commercial_harbor` utilise bois 9 + tissu 3 → marine marchande 6, avec 700 emplois (490 ouvriers, 140 employés et 70 bureaucrates), infrastructure 2. Les navires et petits services côtiers sont une abstraction de l’entretien et de la manutention avec des matériaux courants ; aucune nouvelle industrie ni aucun bien n’est créé. La collecte de données est explicitement désactivée dans les trois ports pour éviter une dépendance implicite à la métrologie.

Comparateur écrit : le port spécialisé utilise 6 clippers → 9 marine marchande, 1000 emplois et infrastructure 3. Ce n’est pas une baisse de production réelle déjà mesurée : l’ancien procédé avait un gate absent. Le nouveau procédé ne devient pas le défaut global ; mouillage, port de base et variantes ultérieures sont conservés. Il devient une alternative mondiale, mais seuls les trois historiques sélectionnent explicitement ce nouveau procédé.

Un premier modèle utilisait quatre clippers. Le contrôle des intrants a montré l’absence de chantier naval explicite chez KOR/SUL et des demandes d’isolationnisme. Ce modèle est archivé et remplacé par bois/tissu, qui existent dans les recettes de subsistance. Au prix de référence, les deux propositions coûtent 240 et donnent une valeur de service 300 : marge brute 60 avant salaires. Le procédé final reste légèrement moins efficace par emploi que le port spécialisé (60/700 contre 90/1000). PORT_COST_SENSITIVITY.csv contient aussi des pertes : aucune viabilité moteur garantie.

KOR demande l’isolationnisme ; SUL contient des demandes concurrentes d’isolationnisme et de mercantilisme dont certaines ont des gates absents. JAP conserve le sakoku. Les lois réellement actives et les marchés demandent un contrôle en jeu. TECH ne modifie aucune loi ni pacte pour ouvrir artificiellement le commerce. Les quinze autres sélections portuaires restent signalées, même si la nouvelle alternative est désormais disponible.

## Crédit et commerce ordinaire : deux attributions ciblées

`organized_financial_institutions` est un socle d’ère I sans parent. Sa description actuelle couvre comptabilité, crédit et intermédiation, sans exiger banque centrale ou bourse modernes. L’omettre pour toute une nation peut être incohérent sans justifier une baisse uniforme de son commerce.

PRU : la [notice du Münzkabinett de Berlin](https://ikmk.smb.museum/object?id=18230184), consultée via son texte indexé (ouverture directe indisponible), décrit la Banque royale fondée en 1765 et le bankotaler frappé en 1766 avec date 1765. Cette preuve antérieure à 1776 justifie le socle financier, pas un ensemble industriel supplémentaire.

TUS : l’[histoire institutionnelle de Monte dei Paschi](https://www.gruppomps.it/en/about-us/history.html) atteste les structures bancaires de 1624 et le contrôle gouvernemental renforcé en 1759. Le crédit siennois appartient alors au contexte toscan ; aucun territoire n’est ajouté. Une seule technologie est accordée à chacun des deux TAGs.

Les quatre centres existants restent en commerce normal : PRU/Brandenburg, Prusse orientale et Poméranie ; TUS/Toscane. Aucune capacité haute ou maximale, aucun emploi ni intrant de recette n’est augmenté. L’effet réel peut cependant différer d’un éventuel repli moteur antérieur vers le commerce limité. Le coût de marine marchande est un intrant, les recettes proviennent des échanges : l’absence de sortie de biens dans un PM de service ne prouve pas un déficit. Ne pas assimiler le solde de biens à la rentabilité commerciale.

Les consommateurs directs du socle sont le commerce normal et les recherches de crédit public, bourse et assurance. Ces descendants ne sont pas attribués. Les choix R2 de KND/Ceylan et CAR/Circars/Madras restent limités et compatibles ; aucune répétition ni extension de leurs corrections.

## Artillerie traditionnelle et normalisation de campagne

Le procédé `pm_cannons` ne décrit pas à lui seul une standardisation complète des calibres, affûts et unités. Les [données patrimoniales scientifiques indiennes](https://indiascienceheritage.gov.in/WarTechnology5.html) distinguent l’artillerie de bronze et de fer antérieure au XVIIIe siècle ; l’[objet de 1541 étudié par Durham](https://stories.durham.ac.uk/VRM_25-objects-19/) confirme des capacités de fabrication anciennes. Ces sources motivent la distinction conceptuelle, sans certifier la localisation, les effectifs ou le rendement précis des arsenaux MUG et MARATH en 1776.

Décision minimale : `pm_cannons` exige désormais seulement `organized_military_establishments`, déjà possédé par MUG et MARATH. Aucun `standardized_field_artillery`, acier industriel, coke, vapeur ou alliages national ajouté. La recette économique du fichier courant est intégralement conservée ; les nouveaux procédés de bronze et groupes d’ECON-ALLOYS sont réservés à cet agent.

La construction de nouvelles fonderies reste conditionnée à `standardized_field_artillery`. Deux arsenaux historiques peuvent sélectionner leur procédé ancien sans que l’on prétende leur donner les capacités d’extension d’une fonderie normalisée. Les unités et formations restent inchangées.

Le premier essai ajoutait aussi `organized_workshops` : le contrôle des 471 pays a révélé une perte de disponibilité pour GAL et MLT. Ce second parent est retiré avant livraison finale. Le modèle final ne retire aucune disponibilité existante ; les preuves du premier essai sont archivées. GLOBAL_AVAILABILITY_IMPACT.csv décrit les implications mondiales, sans construire de nouvelles fonderies.

## Dossiers laissés ouverts

132 sélections explicites ont encore un gate absent : 15 ports et 117 centres commerciaux. Les 54 gates de construction restent distincts, dont cinq bâtiments militaires. Les huit historiques absents et les alertes régionales de ressources demeurent dans leur file indépendante. Les groupes omis dans les historiques ne sont pas certifiés par une reconstruction de sélection explicite ; ils figurent dans les CSV et dans le protocole.

TECH ne valide pas les évolutions de Raguse ni les recettes ECON. Leurs versions courantes sont conservées et signalées séparément ; le reçu R2 reste attaché à sa livraison historique, sans couverture automatique de ces révisions.
''')
    doc('PLAYER_TEST_PROTOCOL.md','''# TECH-R3 — protocole joueur groupé

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Aucun test moteur effectué par l’agent.** R1/R2 sont validés dans leurs périmètres exacts ; cette nouvelle passe attend votre confirmation. Utiliser une nouvelle partie au **1er janvier 1776**.

## R3-P — ports traditionnels

Inspecter JAP/Kyushu, KOR/Busan et SUL/Mindanao. Le port existe au même endroit avec les mêmes niveaux : 2, 1 et 1. Procédé visible : **Services portuaires traditionnels**. Collecte de données désactivée. Aucune technologie navale nouvelle.

Valeurs écrites par niveau à plein fonctionnement : bois 9 + tissu 3 → marine marchande 6 ; emplois 700 ; infrastructure 2. Ce sont des capacités, pas des valeurs de production ou d’emploi déjà observées. Vérifier que le procédé reste sélectionné, que les matériaux sont disponibles, que des employés sont recrutés et que le service est produit. Un recrutement partiel n’est pas à lui seul une anomalie.

Le procédé n’exige aucun clipper industriel ni nouveau chantier naval. Contrôler néanmoins les prix du bois/tissu et la demande locale de marine marchande. Si la demande ou le régime commercial laisse le port en difficulté, relever le pays, les PM actifs, les intrants, l’emploi et le résultat. Ne pas ouvrir artificiellement le marché pour masquer le constat.

Les lois commerciales préexistantes sont conservées : sakoku japonais, demande d’isolationnisme coréenne et demandes commerciales à vérifier chez Sulu. La capacité portuaire ne signifie pas une ouverture diplomatique ou juridique. Quelques ports témoins, notamment GBR, VEN et un port non corrigé, doivent garder leurs procédés attendus ; le mouillage et les variantes spécialisées restent disponibles.

## R3-T — commerce de Prusse et Toscane

PRU doit conserver ses 36 anciennes technologies et posséder uniquement le nouveau socle financier (37 au total). TUS passe de 20 à 21. Aucun crédit public, bourse, assurance, vapeur, rail ou procédé industriel supplémentaire automatiquement attribué. Vérifier les listes dans TECH_BEFORE_AFTER.csv.

Les centres de Brandenburg, Prusse orientale, Poméranie et Toscane gardent le commerce normal. Vérifier sa disponibilité, son maintien, les employés, l’approvisionnement en marine marchande, les échanges, frais et finances. Les paramètres du procédé restent inchangés ; l’effet réel d’un éventuel ancien repli vers le commerce limité reste à observer. Aucune promesse de rentabilité ni de doublement d’échanges.

Témoins R2 : KND/Ceylan et CAR/Circars/Madras gardent le commerce limité. Les pays commerçants non corrigés ne doivent recevoir aucun paquet financier. Contrôler les lois et l’amendement prussien préexistant sans les modifier pour le test.

## R3-A — deux fonderies historiques

Inspecter MUG/Delhi et MARATH/Agra : procédé de canons traditionnels initial conservé et disponible avec l’organisation militaire déjà possédée. Aucun octroi de normalisation de l’artillerie, acier, coke ou alliages. Vérifier recrutement, matériaux de la recette réellement affichée, production de canons, demande et résultat économique.

Le gate de construction des nouvelles fonderies reste distinct : ne pas considérer son absence comme une panne de l’arsenal déjà installé. GAL/MLT et une grande puissance avec artillerie normalisée servent de témoins de disponibilité conservée.

ECON-ALLOYS introduit ses propres recettes et choix de bronze : ils doivent être présents dans leur version courante, sans être confondus avec la modification de gate TECH-R3. Le présent test ne certifie pas automatiquement la rentabilité de toute sa chaîne ou ses ustensiles ; son protocole garde son périmètre propre.

## Contrôles communs et durée

Vérifier les témoins R1/R2, dont la mine native BGT inchangée. Les territoires SERG et leurs validations restent conservés. Raguse et les changements balkaniques viennent de WORLD et gardent leurs propres preuves et calendrier de validation : les observer n’étend pas automatiquement votre attestation TECH.

Laisser tourner **un mois complet**, surveiller recrutement, intrants, accès au marché, pénuries, prix, dépenses et échanges. Signaler tout PM remplacé ou indisponible, arrêt de production ou déficit bloquant avec le contexte observé. Une capacité écrite et une estimation statique ne valent pas production réelle.

Sauvegarder puis recharger ; retrouver technologies, bâtiments et choix de procédés sans crash ni anomalie bloquante. Confirmer séparément R3-P, R3-T et R3-A, en ne rapportant que les vérifications réellement effectuées. Aucun reçu R3 ne sera enregistré avant votre réponse explicite.
''')
    inventory='\n'.join('| '+k+' | '+str(summary['categories_before'].get(k,0))+' | '+str(summary['categories_after'].get(k,0))+' |' for k in ['PASS','REQUIRES_HISTORICAL_REVIEW','BUILDING_TECH_CONFLICT','MISSING_HISTORY'])
    report='''**AUDIT TECHNOLOGIQUE 1776 — TECH-R3**

R2 : **PASS_RUNTIME_USER_VALIDATED**, version exacte réceptionnée. R3 : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Audit mondial et dossiers territoriaux toujours distincts.

## Réception R2 et état R1

Le joueur confirme le protocole intégral, un mois et sauvegarde/rechargement. Les cinq empreintes fonctionnelles R2 correspondent à la livraison lors de la réception, sans différence dans son manifeste. Reçu ajouté dans R2, source utilisateur copiée, seul AUDIT_STATE actualisé ; rapports, manifestes et tests originaux conservés. R2_ACCEPTANCE.json contient les contrôles d’acceptation et les versions. R1 reste PASS_RUNTIME_USER_VALIDATED dans son périmètre, avec ses preuves intactes.

Le reçu R2 couvre douze sélections, quatorze remplacements dans quatre historiques et les parents des alliages dans un cinquième fichier ; six TAGs, aucun grant national. Aucun test à recommencer, aucune date effective, mesure économique ou capture inventée. R3, ECON et les évolutions territoriales postérieures sont exclus. Le fichier sud-européen a ensuite évolué pour Raguse : cette révision n’hérite pas du PASS historique R2, qui reste valide.

## Inventaire courant et diagnostic

Entrée : 470 pays et 93 nouveaux TAGs. État courant : '''+str(summary['countries'])+' pays et '+str(summary['new_tags'])+''' nouveaux TAGs, du fait de la création indépendante de RAG par WORLD. TECH ne crée aucun pays.

| Catégorie principale exclusive | Entrée R3 | État courant |
| --- | ---: | ---: |
'''+inventory+'''

Ces catégories sont des vues de profil statique, pas des validations historiques ou moteur. Le nouvel inventaire conserve les décisions documentaires antérieures. Huit historiques restent absents.

Les CSV couvrent tous les scopes actuels : '''+str(counts['PORT']['assets'])+' ports, '+str(counts['TRADE']['assets'])+' centres commerciaux et '+str(counts['ARMS']['assets'])+''' bâtiments militaires déclarés. Ce ne sont pas des ports cartographiés individuellement ni des niveaux additionnés. Les déclarations superposées, leurs niveaux et les groupes omis sont séparés des choix explicites. Aucune usine de munitions initiale n’est créée pour compléter artificiellement une chaîne.

Au départ, 195 gates de déclarations, dont 141 PM et 54 constructions. Le focus compte 144 cas d’actifs : **141 P0 de sélection incompatible dans les scripts et trois P1 exclusifs de construction** ; deux autres constructions se superposent aux P0 des fonderies. Aucun dysfonctionnement moteur observé, aucun faux positif démontré, aucune nouvelle erreur de capacité P2 quantifiée. Trois dossiers P3 juridiques (JAP/KOR/SUL) sont renvoyés dans P3_RESEARCH_HANDOFFS.csv ; ils recoupent les pays étudiés et ne sont pas trois nouveaux bâtiments en panne. Les autres incertitudes de marché, groupes omis et histoire restent explicites.

Après installation : **132 sélections explicites incompatibles** (15 ports, 117 centres), **54 gates de construction**, soit **186 signalements de gates**. Dans le focus, 132 P0 et cinq P1 de construction restent ouverts. La nouvelle alternative portuaire ne certifie pas le repli réel du moteur dans les quinze historiques restants. Les ressources et huit absences conservent leur file indépendante.

## Corrections installées

Huit fichiers fonctionnels TECH : nouveau PM, groupe portuaire étendu, deux historiques asiatiques, deux localisations, historique financier additionnel et seul gate des canons dans le fichier courant d’industrie. Trois substitutions de PM portuaire, trois sélections explicites de données neutres, deux grants ciblés et un gate partagé corrigé. Neuf incompatibilités de disponibilité disparaissent du relevé ; cela ne clôture pas les restrictions de construction ni les dossiers territoriaux.

| Pays | État technique | Bâtiment | Correction |
| --- | --- | --- | --- |
'''+table+'''

| Pays | Technologies avant | Après | Seul ajout |
| --- | ---: | ---: | --- |
'''+tech_table+'''

Les autres pays préexistants conservent leurs technologies ; les 19 savoirs initiaux de RAG viennent de WORLD et ne sont pas crédités à TECH. Les choix R2 KND/CAR sont conservés et recontrôlés.

Le port traditionnel emploie bois/tissu, pas des navires industriels : 9/3 → marine marchande 6, 700 postes, infrastructure 2 par niveau. Le port spécialisé reste 6 clippers→9, 1000 postes et infrastructure 3. Aux prix de référence, marge brute 60 contre 90 avant salaires ; le modèle conserve des cas déficitaires selon prix/salaires. Les sources de subsistance fournissent les matériaux de base, sans garantie d’emploi, de stocks ou d’accès effectif. Les lois commerciales restent inchangées et peuvent limiter les échanges.

Le commerce ordinaire des quatre centres PRU/TUS conserve ses paramètres ; aucun niveau maximal offert ni descendant financier automatiquement donné. Les recettes de service ne se jugent pas comme une simple vente de biens : prix, frais, routes et recettes demandent le moteur.

`pm_cannons` demande maintenant seulement `organized_military_establishments`. Recette, emplois, autres procédés et groupes économiques préservés. La normalisation demeure requise pour construire une nouvelle fonderie. L’éligibilité technologique à ce PM passe de 97 à '''+str(global_count)+''' pays, sans aucune perte d’éligibilité ancienne ni nouvelle usine construite. L’essai à deux parents affectait GAL/MLT : cette condition supplémentaire a été retirée avant livraison finale.

HISTORICAL_DECISIONS.md fournit sources, niveaux de preuve, arbitrages et limites. Les effets mondiaux des gates et consommateurs du socle financier sont détaillés sans supposer d’octroi automatique.

## Tests, version et concurrence

'''+f"**{v['passed']}/{v['total']} contrôles statiques**, **{target['passed']}/{target['total']} tests ciblés** ; **{cumulative['passed']}/{cumulative['total']} cumulatifs réussis**, {len(cumulative['failed'])} assertions classées et {len(cumulative['skipped'])} exclusion héritée. Aucun nouvel échec inexpliqué. Les onze anciennes assertions R2 restent classées ; une assertion supplémentaire attendait l’absence de reçu R2, désormais contredite par l’attestation réelle. Aucun ancien test supprimé ou réécrit.\n"+'''
Syntaxe, localisation, références, sélection, gates, intrants, effectifs théoriques, effets mondiaux, absence de perte de disponibilité, conservation des choix R2, preuves et protections sont contrôlés. La première passe de tests est archivée : les révisions issues des contrôles globaux et des intrants justifient la nouvelle exécution finale. Une erreur de routage de deux vues JSON dérivées a aussi été réparée depuis les CSV et snapshots gelés, sans impact sur le jeu ou les preuves R1/R2 ; les vues mal routées et les sources sont conservées.

Exécutable et journal disponibles : **1.13.11** ; descriptor **1.13.***, revérifiés. Aucun lancement moteur par l’agent, aucune écriture vanilla. HEAD, branche et index Git conservés ; aucune opération Git d’écriture.

WORLD BALKANS-02 et ECON-ALLOYS sont actifs indépendamment. Les fichiers de Raguse, transferts, populations, bitmap et institutions restent ceux de WORLD. Les recettes d’alliages, ustensiles et bronze, groupes, besoins domestiques et localisations restent ceux d’ECON. Le fichier du gate de canons est distinct de ses fichiers économiques déclarés ; sa recette courante est identique à la préimage. CONCURRENT_CHANGES.json expose tous les écarts hors TECH et leur rattachement. Aucune restauration depuis une ancienne baseline.

Les fortifications/génie, Anzin, drainage, mines/sel, Saint-Gobain, France/USA et témoins R1/R2 sont conservés. Les 873 preuves SERG et son état sont identiques : **82/235 = 34,89 %, 24/81 tâches qualifiées**. Aucun fichier de suivi SERG/WORLD écrit par TECH, aucune clôture ou attestation territoriale étendue.

## Validation et suite

PLAYER_TEST_PROTOCOL.md regroupe R3-P, R3-T et R3-A : nouvelle partie en 1776, pays/procédés, matériaux et recrutement, économie et marchés, témoins R1/R2, un mois puis sauvegarde/rechargement. Les restrictions légales de commerce, les groupes historiques omis, les quinze ports et 117 centres restants, les cinq constructions militaires et les autres 49 gates de construction restent ouverts.

Prochaine action recommandée : validation humaine R3, puis recherche ciblée sur les ports et réseaux marchands restants avec leurs lois et intrants. Aucun R4 commencé et aucun reçu humain R3 créé. Les chantiers WORLD/ECON gardent leurs propres protocoles et calendrier ; leurs états ne sont pas modifiés ici.
'''
    doc('REPORT.md',report)
    dump('AUDIT_STATE.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',R1_status='PASS_RUNTIME_USER_VALIDATED',R2_status='PASS_RUNTIME_USER_VALIDATED',R2_acceptance='R2_ACCEPTANCE.json',sub_lots=['R3-P','R3-T','R3-A'],corrected_asset_gates=9,technology_grants=dict(PRU=['organized_financial_institutions'],TUS=['organized_financial_institutions']),runtime_validation=dict(status='NOT_RUN_BY_AGENT',attestation=None,protocol='PLAYER_TEST_PROTOCOL.md'),global_audit_status='OPEN_FINDINGS_REMAIN',territorial_tracking_written=False,R4_started=False,next_action='Player validation of TECH-R3; remaining port/trade research documented, not automatically started.'))
    doc('PROGRESS_HISTORY.md','# Historique TECH-R3\n\n- 2026-10-24 — R3-001 : reçu humain R2 enregistré après comparaison 5/5 ; R1 et preuves originales conservés.\n- 2026-10-24 — R3-002 : inventaire exhaustif ports/commerce/armureries, source des conflits et économie conditionnelle.\n- 2026-10-24 — R3-003 : trois ports traditionnels et données neutres ; socle financier PRU/TUS ; gate des canons traditionnel distinct de leur construction.\n- 2026-10-24 — R3-004 : examen mondial : condition artisanale retirée pour conserver GAL/MLT. Intrants portuaires révisés vers bois/tissu pour éviter un chantier naval ou des importations imposées à KOR/SUL. Essais et preuves intermédiaires conservés.\n- 2026-10-24 — R3-005 : WORLD/Raguse et ECON/alliages-ustensiles conservés ; aucune écriture territoriale. Réparation documentée de vues dérivées, sources gelées préservées.\n'+f"- 2026-10-24 — R3-006 : {v['passed']}/{v['total']} statiques, {target['passed']}/{target['total']} ciblés, {cumulative['passed']}/{cumulative['total']} cumulatifs ; {len(cumulative['failed'])} assertions classées, {len(cumulative['skipped'])} exclusion. Protocole prêt ; R3 attend le joueur.\n")
    print('R3 report, historical decisions, protocol and bounded state prepared',flush=True)

def finalize():
    b=load(OUT/'BASELINE.json');v=load(OUT/'TEST_RESULTS.json');current=r1.runtime.runtime_hashes();checks={}
    checks['Functional workspace identical to statically checked snapshot']=current==load(OUT/'SESSION_AFTER_STATIC.json')['hashes']
    checks['Eight owned functional files match reviewed patches']=all(current[r['file']]==r['after_sha256'] for r in owned_patches())
    checks['R1 accepted R2 proof hashes preserved']=all(sha(ROOT/p)==h for field in ['R1_proofs','R2_proofs'] for p,h in b[field].items())
    checks['873 SERG proofs and current state preserved']=len(b['SERG_proofs'])==873 and all(sha(ROOT/p)==h for p,h in b['SERG_proofs'].items()) and load(r1.rm.OUT/'ROADMAP_STATE.json')==b['SERG_state']
    checks['Vanilla referenced goods and templates unchanged']=all(sha(p)==h for p,h in load(OUT/'VANILLA_INPUTS.json').items())
    checks['Final static and targeted checks pass']=v['status']=='PASS' and v['passed']==v['total'] and v['targeted']['passed']==v['targeted']['total']
    checks['Cumulative failures individually classified']=not load(OUT/'CUMULATIVE_TEST_REVIEW.json')['new_unexplained_failures']
    checks['R3 awaits user without a human receipt']=load(OUT/'AUDIT_STATE.json')['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and not list(OUT.glob('RUNTIME_USER_ATTESTATION*'))
    checks['Mandatory R3 files exist']=all((OUT/n).is_file() for n in ['REPORT.md','R2_ACCEPTANCE.json','PRIORITY_MATRIX.csv','PORT_TECH_AUDIT.csv','TRADE_CENTER_TECH_AUDIT.csv','ARMS_INDUSTRY_TECH_AUDIT.csv','TECH_BEFORE_AFTER.csv','BUILDING_PM_BEFORE_AFTER.csv','HISTORICAL_DECISIONS.md','FILES_MODIFIED.json','CONCURRENT_CHANGES.json','TEST_RESULTS.json','PLAYER_TEST_PROTOCOL.md'])
    checks['Git HEAD branch index unchanged']=git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index']
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);own={r['file'] for r in owned_patches()};errors=[l for l in diff.stdout.splitlines() if any(l.startswith(p+':') for p in own)];checks['No own whitespace error']=not errors;dump('DIFF_CHECK.json',dict(returncode=diff.returncode,stdout=diff.stdout,stderr=diff.stderr,own_errors=errors,unrelated_whitespace_not_modified=True))
    result=dict(status='PASS' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),checks=checks,failed=[k for k,ok in checks.items() if not ok],automated_engine_test=False);dump('FINAL_CHECKS.json',result);assert not result['failed'],result
    dump('SESSION_AFTER.json',dict(hashes=current,git=b['git'],SERG_state=load(r1.rm.OUT/'ROADMAP_STATE.json'),concurrent_sources='CONCURRENT_CHANGES.json',human_validation_R3=None,static_only=True))
    manifest={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'};manifest.update({r['file']:sha(ROOT/r['file']) for r in owned_patches()})
    for name in ['audit_starting_tech_1776_r3.py','test_starting_tech_audit_1776_r3.py']:manifest['tools/'+name]=sha(ROOT/'tools'/name)
    dump('DELIVERY_MANIFEST.json',dict(scope='TECH-R3 own files and proofs only; independent WORLD/ECON changes recorded, not approved',files=manifest,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',human_validation=None));print('Final checks',result['passed'],'/',result['total'],'; manifest',len(manifest),'files; R3 awaits player',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
