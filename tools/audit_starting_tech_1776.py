"""Effective 1776 country technology audit; no inferred engine execution or territorial writes."""
import collections as C,copy,csv,hashlib,io,json,os,re,subprocess,sys,unittest
from pathlib import Path
import validate_map2a as qa
import tech_start_1776_implementation as historical
import serg_closure_roadmap as rm
import serg_sc4_italian_states as runtime
ROOT=qa.ROOT;GAME=qa.GAME;cw=qa.cw
OUT=ROOT/'docs/reports/technology/STARTING_TECH_AUDIT_1776_R1'
PROFILE_FILE='common/scripted_effects/1776_restored_starting_technology_profiles.txt'
OVERLAY_FILE='common/history/countries/zz_1776_restored_starting_technologies.txt'
SALT_HISTORY='common/history/buildings/1776_sc1_berchtesgaden.txt'
CRAFTS={'distillation','improved_husbandry','international_relations','organized_textile_production','traditional_food_processing','organized_workshops','traditional_papermaking','periodical_print_networks'}
PROFILE_TECHS={
    'aor1776_start_ecclesiastical_crafts':CRAFTS,
    'aor1776_start_salt_provostry':CRAFTS|{'shaft_mining','organized_forestry'},
    'aor1776_start_trento_crafts':CRAFTS|{'institutionalized_scientific_exchange'},
    'aor1776_start_military_administration_foundation':{'organized_military_establishments'},
    'aor1776_start_husbandry_foundation':{'improved_husbandry'},
    'aor1776_start_shaft_mining_foundation':{'shaft_mining'},
}
ASSIGNMENTS={'BGT':'aor1776_start_salt_provostry','BRX':'aor1776_start_ecclesiastical_crafts','TRT':'aor1776_start_trento_crafts','PAP':'aor1776_start_military_administration_foundation','CAR':'aor1776_start_military_administration_foundation','ARK':'aor1776_start_husbandry_foundation','VIE':'aor1776_start_husbandry_foundation','LGE':'aor1776_start_shaft_mining_foundation'}
SOURCE=Path('C:/Users/simeo/.codex/attachments/df8e856e-0d05-49dc-8609-441ba9118afa/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(n,o):(OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def csvout(n,rows,fields=None):
    with (OUT/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def ref(p):return ('MOD:' if p.is_relative_to(ROOT) else 'VANILLA:')+p.relative_to(ROOT if p.is_relative_to(ROOT) else GAME).as_posix()
def val(n,k,d=None):return cw.scalar(n.one(k,d)) if n.one(k,d) is not None else None
def values(n,k):return [cw.scalar(c.value) for b in n.children(k) for c in b.children() if isinstance(c.value,str)]
def effective(folder):
    replaces=re.findall(r'replace_path\s*=\s*"([^"]+)"',(ROOT/'descriptor.mod').read_text(encoding='utf8'))
    files={}
    if not any(folder==p or folder.startswith(p+'/') for p in replaces):
        files.update({p.relative_to(GAME/folder).as_posix().casefold():p for p in (GAME/folder).rglob('*.txt')})
    files.update({p.relative_to(ROOT/folder).as_posix().casefold():p for p in (ROOT/folder).rglob('*.txt')})
    return [files[k] for k in sorted(files)]
def objects(folder):
    result={};sources={};collisions=[]
    for p in effective(folder):
        for n in cw.parse(p.read_text(encoding='utf-8-sig')):
            key=n.key.removeprefix('REPLACE_OR_CREATE:').removeprefix('REPLACE:')
            if key in result:collisions.append(dict(id=key,before=sources[key],after=ref(p)))
            result[key]=n;sources[key]=ref(p)
    return result,sources,collisions

def capture():
    assert not (OUT/'BASELINE.json').exists();OUT.mkdir(exist_ok=True)
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    inv=qa.inventory();hashes=runtime.runtime_hashes();check=rm.check();assert check['status']=='PASS'
    dump('BASELINE.json',dict(inventory=inv,hashes=hashes,serg_state=load(rm.OUT/'ROADMAP_STATE.json'),serg_proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file()},tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index')),vanilla_inputs={},current_date='2026-10-24'))
    (OUT/'USER_MISSION.txt').write_bytes(SOURCE.read_bytes());dump('SERG_ENTRY_CHECK.json',check)
    print('Baseline captured; SERG read only; active countries',len({r[1] for r in inv['states']}),flush=True)

def resolve(nodes,effects,techs,trail=()):
    """Separate unconditional grants from branches that cannot be proven statically."""
    grants=set();conditional=set();calls=[];unresolved=[]
    for n in nodes:
        if n.key=='add_technology_researched' and isinstance(n.value,str):grants.add(cw.scalar(n.value))
        elif n.key=='add_era_researched':grants|={k for k,t in techs.items() if val(t,'era')==cw.scalar(n.value)}
        elif n.key in effects:
            calls.append(n.key)
            if n.key in trail:unresolved.append('CYCLE:'+n.key);continue
            g,c,cc,u=resolve(effects[n.key].children(),effects,techs,trail+(n.key,));grants|=g;conditional|=c;calls+=cc;unresolved+=u
        elif isinstance(n.value,list) and n.key not in {'limit','modifier','trigger'}:
            g,c,cc,u=resolve(n.children(),effects,techs,trail);conditional|=g|c;calls+=cc;unresolved+=u
        elif n.key.startswith(('effect_starting_technology_','aor1776_start_')):unresolved.append('UNKNOWN_EFFECT:'+n.key)
    return grants,conditional,sorted(set(calls)),sorted(set(unresolved))

def ancestors(keys,graph):
    result=set(keys);pending=list(keys)
    while pending:
        for parent in graph.get(pending.pop(),set()):
            if parent not in result:result.add(parent);pending.append(parent)
    return result

def country_names(tags):
    names={};pattern=re.compile(r'^\s*([A-Z][A-Z0-9_]+):\d*\s+"(.*)"\s*$',re.M)
    for base in [GAME,ROOT]:
        for p in sorted((base/'localization/french').rglob('*.yml')):
            for k,v in pattern.findall(p.read_text(encoding='utf-8-sig',errors='replace')):
                if k in tags:names[k]=v
    return names

def inspect():
    b=load(OUT/'BASELINE.json');inv=qa.inventory();active=sorted({r[1] for r in inv['states']})
    techs,ts,tc=objects('common/technology/technologies');effects,es,ec=objects('common/scripted_effects');defs,ds,dc=objects('common/country_definitions')
    vanilla_tags=set()
    for p in (GAME/'common/country_definitions').glob('*.txt'):
        vanilla_tags.update(n.key for n in cw.parse(p.read_text(encoding='utf-8-sig')) if n.children('country_type'))
    graph={k:set(values(n,'unlocking_technologies')) for k,n in techs.items()}
    plan=historical.read_csv(historical.COUNTRY_PLAN);planby={r['TAG']:r for r in plan}
    known_targets,researched=historical.final_targets(plan,{r['TAG']:[] for r in plan},graph)
    _,classifications=historical.parse_graph_and_classifications()
    histories=C.defaultdict(list);histnodes=C.defaultdict(list)
    for p in effective('common/history/countries'):
        raw=p.read_text(encoding='utf-8-sig')
        for root in cw.parse(raw):
            for n in root.children():
                if n.key.startswith('c:'):
                    tag=n.key[2:];histories[tag].append(dict(file=ref(p),line=raw[:n.start].count('\n')+1));histnodes[tag]+=n.children()
    decisions=load(OUT/'PROFILE_DECISIONS.json') if (OUT/'PROFILE_DECISIONS.json').exists() else {}
    names=country_names(active);starts={};rows=[]
    for tag in active:
        granted,conditional,calls,unresolved=resolve(histnodes[tag],effects,techs)
        starts[tag]=dict(technologies=sorted(granted),conditional_technologies=sorted(conditional),effects=calls,unresolved=unresolved,history=histories[tag])
        missing={f'{k}->{p}' for k in granted for p in graph.get(k,set()) if p not in granted};unknown=granted-set(techs)
        # Sericulture is an intentional regional starting-knowledge marker with
        # a live silk modifier, not an obsolete alias merely because research is disabled.
        inactive={k for k in granted if k in techs and val(techs[k],'can_research')=='no' and k!='sericulture'}
        advanced={k for k in granted if classifications.get(k) in {'C','D'}}|set(historical.FORBIDDEN_START_TECHS)&granted
        expected=set(known_targets[tag]) if tag in researched else None
        if tag in decisions:expected=set(decisions[tag]['target'])
        stale={k for k in expected or [] if k not in techs}
        if expected is not None:expected-=stale
        missingtarget=expected-granted if expected is not None else set();extra=granted-expected if expected is not None else set()
        dtype=val(defs[tag],'country_type') if tag in defs else 'UNKNOWN'
        intentional_empty=expected==set() and bool(histories[tag]) and not granted
        status='MISSING_HISTORY' if not histories[tag] else 'MISSING_TECH_INITIALIZATION' if not granted and not intentional_empty and dtype!='decentralized' else 'INCORRECT_TECH_PROFILE' if unknown or missing or inactive else 'REQUIRES_HISTORICAL_REVIEW' if expected is None or extra or missingtarget else 'PASS'
        rows.append(dict(TAG=tag,Name=names.get(tag,planby.get(tag,{}).get('Country',tag)),Region=planby.get(tag,{}).get('Region',';'.join(sorted({r[0] for r in inv['states'] if r[1]==tag}))),Status=status,Country_Type=dtype,Tag_Origin='NEW_MOD_TAG' if tag not in vanilla_tags else 'VANILLA_TAG_MODIFIED' if ds.get(tag,'').startswith('MOD:') or any(r['file'].startswith('MOD:') for r in histories[tag]) else 'VANILLA_REUSED',Definition_Source=ds.get(tag,''),History_Sources=';'.join(r['file']+':'+str(r['line']) for r in histories[tag]),Starting_Effects=';'.join(calls),Tech_Count=len(granted),Technologies=';'.join(sorted(granted)),Conditional_Technologies=';'.join(sorted(conditional)),Expected_Profile=decisions[tag]['profile'] if tag in decisions else 'EXISTING_RESEARCHED_1776_PLAN' if expected is not None else 'REQUIRES_COUNTRY_SPECIFIC_REVIEW',Missing_Historical_Tech=';'.join(sorted(missingtarget)),Additional_vs_Old_Plan=';'.join(sorted(extra)),Obsolete_Reference_Plan_IDs=';'.join(sorted(stale)),Intentional_Empty_Profile=intentional_empty,Unknown_Tech=';'.join(sorted(unknown)),Inactive_Aliases=';'.join(sorted(inactive)),Missing_Prerequisites=';'.join(sorted(missing)),Unresolved_Effects=';'.join(unresolved),Blocked_Buildings='',Blocked_PMs='',Correction=decisions.get(tag,{}).get('decision','REVIEW_REMAINING_EVIDENCE')))
        rows[-1]['Potentially_Advanced_Tech']=';'.join(sorted(advanced))
        if advanced and rows[-1]['Status']=='PASS':rows[-1]['Status']='REQUIRES_HISTORICAL_REVIEW'
    # Compare explicit initial building commands to the effective building and PM definitions.
    buildings,bs,bc=objects('common/buildings');pms,ms,mc=objects('common/production_methods');pmgs,gs,gc=objects('common/production_method_groups');conflicts=[]
    for r in inv['buildings']:
        sid,tag,body=r['key'];node=json.loads(body);kind=next((n[2].strip('"') for n in node[2] if n[0]=='building'),None)
        if tag not in starts or kind not in buildings:continue
        techset=set(starts[tag]['technologies']);missing=set(values(buildings[kind],'unlocking_technologies'))-techset
        if missing:conflicts.append(dict(TAG=tag,State=sid,Building=kind,Object=kind,Kind='BUILDING_TECH_CONFLICT',Missing=';'.join(sorted(missing)),Source=bs[kind],Scope='INITIAL_BUILDING_CONSTRUCTION_GATE'))
        for n in node[2]:
            if n[0]!='activate_production_methods':continue
            for pmnode in n[2]:
                pm=pmnode[2].strip('"')
                if pm not in pms:conflicts.append(dict(TAG=tag,State=sid,Building=kind,Object=pm,Kind='RESOURCE_OR_PM_CONFLICT',Missing='UNKNOWN_PM',Source='',Scope='INITIAL_SELECTED_PM'));continue
                missing=set(values(pms[pm],'unlocking_technologies'))-techset
                if missing:conflicts.append(dict(TAG=tag,State=sid,Building=kind,Object=pm,Kind='BUILDING_TECH_CONFLICT',Missing=';'.join(sorted(missing)),Source=ms[pm],Scope='INITIAL_SELECTED_PM'))
    for row in rows:
        cs=[c for c in conflicts if c['TAG']==row['TAG']]
        row['Blocked_Buildings']=';'.join(sorted({c['Building'] for c in cs if c['Scope']=='INITIAL_BUILDING_CONSTRUCTION_GATE'}));row['Blocked_PMs']=';'.join(sorted({c['Object'] for c in cs if c['Scope']=='INITIAL_SELECTED_PM'}))
        if row['Status']=='PASS' and cs:row['Status']='BUILDING_TECH_CONFLICT'
    stage='AFTER' if (ROOT/OVERLAY_FILE).exists() else 'BEFORE'
    dump('RESOLVED_'+stage+'.json',dict(active_tags=active,starts=starts,graph={k:sorted(v) for k,v in graph.items()},tech_sources=ts,tech_eras={k:val(n,'era') for k,n in techs.items()},tech_categories={k:val(n,'category') for k,n in techs.items()},tech_inactive=[k for k,n in techs.items() if val(n,'can_research')=='no'],tech_collisions=tc,country_collisions=dc,effect_collisions=ec,profiles={tag:sorted(v) for tag,v in known_targets.items() if tag in researched},conflicts=conflicts,rows=rows))
    csvout('STARTING_TECH_AUDIT_1776_'+stage+'.csv',rows)
    csvout('BUILDING_TECH_CONFLICTS_'+stage+'.csv',conflicts,['TAG','State','Building','Object','Kind','Missing','Source','Scope'])
    print(stage,'countries',len(active),'categories',dict(C.Counter(r['Status'] for r in rows)),'conflicts',len(conflicts),flush=True)
    print('No-tech countries:',sum(r['Tech_Count']==0 for r in rows),'missing histories:',[r['TAG'] for r in rows if r['Status']=='MISSING_HISTORY'],flush=True)
    print('New mod tags audited:',sum(r['Tag_Origin']=='NEW_MOD_TAG' for r in rows),'priority cases:',[(r['TAG'],r['Tech_Count'],r['Status']) for r in rows if r['TAG'] in {'BGT','BRX','TRT','MCA','SLZ','PAS','RBI','RCI','FSI'}],flush=True)
    print('Dependency debts:',[(r['TAG'],r['Missing_Prerequisites']) for r in rows if r['Missing_Prerequisites']],flush=True)

def plan():
    r=load(OUT/'RESOLVED_BEFORE.json');decisions={}
    for tag,profile in ASSIGNMENTS.items():
        old=set(r['starts'][tag]['technologies']);target=old|PROFILE_TECHS[profile]
        assert not (ancestors(target,r['graph'])-target),(tag,ancestors(target,r['graph'])-target)
        decisions[tag]=dict(profile=profile,before=sorted(old),target=sorted(target),added=sorted(target-old),removed=[],decision='ADD_REVIEWED_PROFILE_IN_NEW_HISTORY_OVERLAY',historical_confidence='MEDIUM_REGION_AND_EXISTING_CAPACITY' if tag in ['BGT','BRX','TRT'] else 'TECHNICAL_PARENT_OF_EXISTING_DOCUMENTED_CAPACITY',note='No nineteenth-century industrial, coke, steam, rail, finance or professional corps grant added.')
    decisions['MCA']=dict(profile='EXISTING_MASSA_RESIDENCE_CRAFTS_MEDICINE',target=r['starts']['MCA']['technologies'],decision='NO_CHANGE; already 10 coherent craft/medical technologies; no Carrara mine invented for unrepresented territory')
    # The five common craft/commercial nodes are already researched for ANH.
    # Recognise matching small German profiles, without adding agriculture or
    # state industrial capacities merely because another neighbour owns them.
    simple=set(r['profiles']['ANH']);assert len(simple)==5
    for row in r['rows']:
        if row['Country_Type']=='recognized' and (row['Region'].startswith('STATE_') or row['Region']=='CENTRAL_EUROPE_GERMAN_ITALY') and set(row['Technologies'].split(';'))==simple and all(region in {'STATE_ANHALT','STATE_SAXONY','STATE_HESSE','STATE_HANNOVER','STATE_FRANCONIA','STATE_WURTTEMBERG','STATE_WESTPHALIA','STATE_BRUNSWICK','STATE_NORTH_RHINE','STATE_RHINELAND','STATE_SCHLESWIG_HOLSTEIN'} for region,owner in load(OUT/'BASELINE.json')['inventory']['states'] if owner==row['TAG']):
            decisions[row['TAG']]=dict(profile='EXISTING_ANHALT_FIVE_COMMON_CRAFTS',target=sorted(simple),decision='NO_CHANGE; five common craft/commercial capacities consistent with reviewed ANH profile, no blanket Austrian or Bavarian grant')
    dump('PROFILE_DECISIONS.json',decisions)
    print('Plan:',{t:len(decisions[t]['added']) for t in ASSIGNMENTS},'unchanged reviewed profiles',len(decisions)-len(ASSIGNMENTS),flush=True)

def install():
    b=load(OUT/'BASELINE.json');decisions=load(OUT/'PROFILE_DECISIONS.json')
    assert not (ROOT/PROFILE_FILE).exists() and not (ROOT/OVERLAY_FILE).exists()
    assert sha(ROOT/SALT_HISTORY)==b['hashes'][SALT_HISTORY]
    # Shared, unconditional country-scoped effects; the existing tier system is
    # intentionally left unchanged because its 1836-style bundles are too broad.
    lines=['# Reviewed 1776 starting knowledge for restored states. Country history only.','']
    for key,techset in PROFILE_TECHS.items():
        inherit=key in {'aor1776_start_salt_provostry','aor1776_start_trento_crafts'}
        lines += [key+' = {']+([' aor1776_start_ecclesiastical_crafts = yes'] if inherit else [])+[' add_technology_researched = '+tech for tech in sorted(techset-CRAFTS if inherit else techset)]+['}','']
    history=['# Additive setup only: existing laws, rulers, diplomacy and country files retained.','COUNTRIES = {']
    for tag,profile in ASSIGNMENTS.items():history+=[' c:'+tag+' ?= { '+profile+' = yes }']
    history+=['}','']
    current=(ROOT/SALT_HISTORY).read_bytes();needle=b'"pm_1776_raw_data_reporting"';assert current.count(needle)==1
    updated=current.replace(needle,b'"pm_1776_no_raw_data_reporting"')
    (OUT/'BGT_BUILDING_HISTORY_BEFORE.txt').write_bytes(current)
    files={PROFILE_FILE:'\n'.join(lines).encode('utf8'),OVERLAY_FILE:'\n'.join(history).encode('utf8'),SALT_HISTORY:updated}
    for rel,data in files.items():cw.parse(data.decode('utf-8-sig'))
    assert sha(ROOT/SALT_HISTORY)==b['hashes'][SALT_HISTORY]
    for rel,data in files.items():(ROOT/rel).write_bytes(data)
    dump('FILES_MODIFIED.json',dict(runtime_files=list(files),sha256={rel:sha(ROOT/rel) for rel in files},country_tags=list(ASSIGNMENTS),new_profiles=PROFILE_FILE,additive_history=OVERLAY_FILE,no_on_action_or_first_tick_grants=True,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',human_validation=None))
    csvout('STARTING_TECH_BEFORE_AFTER.csv',[dict(TAG=t,Profile=ASSIGNMENTS[t],Before_Count=len(decisions[t]['before']),After_Count=len(decisions[t]['target']),Before=';'.join(decisions[t]['before']),Added=';'.join(decisions[t]['added']),Removed='',After=';'.join(decisions[t]['target']),Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION') for t in ASSIGNMENTS])
    print('Installed',len(ASSIGNMENTS),'additive country profiles and BGT no-data fallback; no SERG writes',flush=True)

def extend_liege():
    """One additional evidenced omission found by the exhaustive building audit."""
    files=load(OUT/'FILES_MODIFIED.json');assert files['country_tags']==list(ASSIGNMENTS)[:-1]
    assert all(sha(ROOT/rel)==h for rel,h in files['sha256'].items())
    before=load(OUT/'RESOLVED_BEFORE.json');old=set(before['starts']['LGE']['technologies']);assert 'shaft_mining' not in old
    decisions=load(OUT/'PROFILE_DECISIONS.json');decisions['LGE']=dict(profile=ASSIGNMENTS['LGE'],before=sorted(old),target=sorted(old|{'shaft_mining'}),added=['shaft_mining'],removed=[],decision='ADD_REVIEWED_MINING_FOUNDATION',historical_confidence='HIGH; pre-1776 coal extraction documented in Liege; existing installed coal mine currently gated')
    effect=(ROOT/PROFILE_FILE).read_text(encoding='utf8');assert ASSIGNMENTS['LGE'] not in effect
    (ROOT/PROFILE_FILE).write_text(effect+'\n'+ASSIGNMENTS['LGE']+' = { add_technology_researched = shaft_mining }\n',encoding='utf8')
    raw=(ROOT/OVERLAY_FILE).read_text(encoding='utf8');root=cw.parse(raw)[0];at=root.end-1
    (ROOT/OVERLAY_FILE).write_text(raw[:at]+' c:LGE ?= { '+ASSIGNMENTS['LGE']+' = yes }\n'+raw[at:],encoding='utf8')
    dump('PROFILE_DECISIONS.json',decisions)
    files.update(country_tags=list(ASSIGNMENTS),sha256={rel:sha(ROOT/rel) for rel in files['runtime_files']});dump('FILES_MODIFIED.json',files)
    csvout('STARTING_TECH_BEFORE_AFTER.csv',[dict(TAG=t,Profile=ASSIGNMENTS[t],Before_Count=len(decisions[t]['before']),After_Count=len(decisions[t]['target']),Before=';'.join(decisions[t]['before']),Added=';'.join(decisions[t]['added']),Removed='',After=';'.join(decisions[t]['target']),Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION') for t in ASSIGNMENTS])
    print('Liege coal mining omission corrected separately: 12 -> 13 technologies',flush=True)

def graph_debts(r):
    return {(tag,k,p) for tag,s in r['starts'].items() for k in s['technologies'] for p in r['graph'].get(k,[]) if p not in s['technologies']}

def validate():
    b=load(OUT/'BASELINE.json');before=load(OUT/'RESOLVED_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json');decisions=load(OUT/'PROFILE_DECISIONS.json');files=load(OUT/'FILES_MODIFIED.json');checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    current=runtime.runtime_hashes();inv=qa.inventory();effects,es,_=objects('common/scripted_effects');techs,_,_=objects('common/technology/technologies')
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));concurrent=[p for p in changed if p not in files['runtime_files']]
    dump('CONCURRENT_CHANGES.json',dict(files={p:dict(before=b['hashes'].get(p),after=current.get(p)) for p in concurrent},own_writes=files['runtime_files'],policy='Observed current bytes kept. No restoration from old baseline.'))
    ck('Exactly the three scoped functional files changed',set(changed)==set(files['runtime_files']))
    ck('All installed bytes match reviewed manifest',all(current[rel]==h for rel,h in files['sha256'].items()))
    ck('All 470 starting countries audited including 93 new mod tags',len(after['active_tags'])==470 and after['active_tags']==before['active_tags']==sorted({r[1] for r in b['inventory']['states']}) and sum(r['Tag_Origin']=='NEW_MOD_TAG' for r in after['rows'])==93)
    ck('Country names and sources fully populated',all(r['Name'] and r['Region'] and r['Definition_Source'] for r in after['rows']))
    ck('Only eight reviewed country knowledge sets changed',{tag for tag in after['active_tags'] if before['starts'][tag]['technologies']!=after['starts'][tag]['technologies']}==set(ASSIGNMENTS))
    additions=0
    for tag,profile in ASSIGNMENTS.items():
        a=set(after['starts'][tag]['technologies']);z=set(before['starts'][tag]['technologies']);additions+=len(a-z)
        ck('Exact additions without removal '+tag,a==set(decisions[tag]['target']) and a-z==set(decisions[tag]['added']) and z<=a)
        ck('No dangling prerequisite on corrected country '+tag,ancestors(a,after['graph'])==a)
        ck('Reviewed profile executed unconditionally in country history '+tag,profile in after['starts'][tag]['effects'] and not after['starts'][tag]['conditional_technologies'] and not after['starts'][tag]['unresolved'])
    ck('Exactly 28 reviewed country technology additions',additions==28)
    for profile,expected in PROFILE_TECHS.items():
        g,c,calls,u=resolve(effects[profile].children(),effects,techs,(profile,))
        ck('Shared profile exact known closed set '+profile,g==expected and not c and not u and g<=set(techs) and ancestors(g,after['graph'])==g)
    forbidden={'coke_smelting','atmospheric_engine','mechanical_tools','precision_boring','railways','scientific_metrology','permanent_engineer_services','specialized_technical_academies'}
    ck('No advanced industrial or professional corps knowledge added',not forbidden&set().union(*(set(decisions[tag]['added']) for tag in ASSIGNMENTS)))
    ck('No unknown researched technology anywhere',all(set(s['technologies'])<=set(after['graph']) and not s['unresolved'] for s in after['starts'].values()))
    unknown_parents={(k,p) for k,parents in after['graph'].items() for p in parents if p not in after['graph']}
    ck('Graph has no unknown parent',not unknown_parents)
    def cycle(k,trail=(),done=None):
        if k in trail:return True
        return any(cycle(p,trail+(k,)) for p in after['graph'][k])
    ck('Graph acyclic',not any(cycle(k) for k in after['graph']))
    allowed={(tag,'alloysworking','coke_smelting') for tag in ['AUS','BEO','FRA','PRU','RUS','SAX','SWE']}
    ck('Only seven explicitly documented preexisting alloy debts remain',graph_debts(after)==allowed and allowed<=graph_debts(before))
    empty={t for t,s in after['starts'].items() if not s['technologies']};beforeempty={t for t,s in before['starts'].items() if not s['technologies']}
    ck('No country becomes empty and BGT no longer empty',empty==beforeempty-{'BGT'} and len(empty)==28)
    missing={r['TAG'] for r in after['rows'] if r['Status']=='MISSING_HISTORY'}
    ck('Eight missing histories explicitly retained as open cases',missing=={'AP7','CKC','FRS','GR7','HWA','INDOP','PLW','TTI'} and all(r['Country_Type']=='decentralized' for r in after['rows'] if r['TAG'] in missing))
    ck('No Western profile imposed on intentionally empty starts',all(before['starts'][t]['technologies']==after['starts'][t]['technologies'] for t in empty))
    ck('Regional sericulture retained as functioning starting knowledge',all('sericulture' in after['starts'][t]['technologies'] for t in ['CHI','JAP','KOR','MGL','XIN','YUN']))
    for key in ['pops','resolved_demographics','regional_pop','owners','geometry','states','state_types','countries','building_levels_written','units','errors','duplicates']:ck('Unchanged effective '+key,inv[key]==b['inventory'][key])
    old=qa.counter(b['inventory']['buildings']);new=qa.counter(inv['buildings'])
    removed=list((old-new).elements());added=list((new-old).elements())
    ck('Only one BGT salt recipe changes',len(removed)==len(added)==1 and removed[0][:2]==added[0][:2]==('STATE_TYROL','BGT') and added[0][2]==removed[0][2].replace('pm_1776_raw_data_reporting','pm_1776_no_raw_data_reporting'))
    ck('BGT old building bytes differ by one PM token only',(ROOT/SALT_HISTORY).read_bytes()==(OUT/'BGT_BUILDING_HISTORY_BEFORE.txt').read_bytes().replace(b'"pm_1776_raw_data_reporting"',b'"pm_1776_no_raw_data_reporting"'))
    buildings,_,_=objects('common/buildings');pms,_,_=objects('common/production_methods');groups,_,_=objects('common/production_method_groups')
    root=cw.parse((ROOT/SALT_HISTORY).read_text(encoding='utf-8-sig'))[0];region=root.children()[0].children()[0];mine=next(n for n in region.children('create_building') if val(n,'building')=='building_salt_mine');methods=values(mine,'activate_production_methods');knowledge=set(after['starts']['BGT']['technologies'])
    ck('Mine construction is unlocked now and was locked before',set(values(buildings['building_salt_mine'],'unlocking_technologies'))<=knowledge and 'shaft_mining' not in before['starts']['BGT']['technologies'])
    ck('All six mine PM gates satisfied',len(methods)==6 and all(pm in pms and set(values(pms[pm],'unlocking_technologies'))<=knowledge for pm in methods))
    ck('All selected mine PMs belong to its defined groups',all(any(pm in values(groups[g],'production_methods') for g in values(buildings['building_salt_mine'],'production_method_groups')) for pm in methods))
    jobs=sum(float(n.value) for pm in methods for block in pms[pm].children('building_modifiers') for level in block.children('level_scaled') for n in level.children() if n.key.startswith('building_employment_') and n.key.endswith('_add'))
    ck('Mine total job capacity 5000 with neutral data reporting',jobs==5000 and 'pm_1776_no_raw_data_reporting' in methods and 'pm_1776_raw_data_reporting' not in methods)
    ck('No salt special building or arbitrary subsidy reintroduced','saline' not in (ROOT/SALT_HISTORY).read_text().lower() and 'subsid' not in (ROOT/SALT_HISTORY).read_text().lower())
    ck('Liege existing coal mine access corrected',any(c['TAG']=='LGE' and c['Building']=='building_coal_mine' for c in before['conflicts']) and not any(c['TAG']=='LGE' and c['Building']=='building_coal_mine' for c in after['conflicts']))
    ck('No new building or PM conflict introduced',{json.dumps(c,sort_keys=True) for c in after['conflicts']}<={json.dumps(c,sort_keys=True) for c in before['conflicts']})
    ck('Profile references are country-history-only',all(not p.startswith('common/on_actions') for p in changed) and all(not re.search(r'\b(on_game_started|on_daily_pulse|trigger_event|every_country)\b',(ROOT/rel).read_text(encoding='utf-8-sig')) for rel in [PROFILE_FILE,OVERLAY_FILE]))
    ck('Every previous country history and political setup preserved',all(current.get(rel)==h for rel,h in b['hashes'].items() if rel.startswith('common/history/countries/')))
    ck('All SERG tracking evidence and human receipts byte preserved',all(sha(ROOT/rel)==h for rel,h in b['serg_proofs'].items()))
    checked=rm.check();ck('SERG remains 82/235 24/81 and same pending tasks',checked['status']=='PASS' and load(rm.OUT/'ROADMAP_STATE.json')==b['serg_state'])
    ck('All earlier tools preserved',all(sha(ROOT/rel)==h for rel,h in b['tools'].items()))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    ck('Git head branch index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    v=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',new_human_attestation=None,world_population=sum(r['count'] for r in inv['pops']),known_global_debts=dict(missing_histories=sorted(missing),prerequisite_debts=sorted(allowed),unresolved_initial_building_declarations=len(after['conflicts'])));dump('TECH_VALIDATION.json',v)
    dump('SESSION_AFTER_STATIC.json',dict(hashes=current,inventory=inv,serg_check=checked));print(v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']

def reports():
    before=load(OUT/'RESOLVED_BEFORE.json');after=load(OUT/'RESOLVED_AFTER.json');decisions=load(OUT/'PROFILE_DECISIONS.json');old={r['TAG']:r for r in before['rows']};rows=[]
    regions,_,_=objects('map_data/state_regions');resource_review=[]
    for entry in load(OUT/'SESSION_AFTER_STATIC.json')['inventory']['buildings']:
        sid,tag,body=entry['key'];definition=json.loads(body);kind=next((n[2].strip('"') for n in definition[2] if n[0]=='building'),'')
        if not (kind.endswith('_mine') or kind.endswith('_quarry') or kind=='building_gold_fields') or sid not in regions:continue
        region=regions[sid];quantity=sum(float(n.value) for cap in region.children('capped_resources') for n in cap.children() if n.key==kind)
        quantity+=sum(float(val(n,'discovered_amount','0')) for n in region.children('resource') if val(n,'type')==kind)
        if quantity<=0:resource_review.append(dict(TAG=tag,State=sid,Building=kind,Kind='RESOURCE_OR_PM_CONFLICT',Detail='No positive discovered resource in regional template; province-share, historical scripts and final engine allocation require review',Engine_Confirmed=False))
    csvout('RESOURCE_AVAILABILITY_REVIEW.csv',resource_review,['TAG','State','Building','Kind','Detail','Engine_Confirmed'])
    for row in after['rows']:
        r=dict(row,Before_Status=old[row['TAG']]['Status'],Before_Tech_Count=old[row['TAG']]['Tech_Count'],Validation_Mode='STATIC_PROFILE_CHECK_NOT_ENGINE_EXECUTION',Runtime_Status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if row['TAG'] in ASSIGNMENTS else 'RETAINED_NOT_REVALIDATED')
        expected=set(decisions[row['TAG']]['target']) if row['TAG'] in decisions else set(after['profiles'].get(row['TAG'],[]))
        r['Expected_Technologies']=';'.join(sorted(expected&set(after['graph']))) if expected else 'INTENTIONALLY_EMPTY' if r['Intentional_Empty_Profile'] else 'UNRESOLVED'
        r['Resource_Review']=';'.join(sorted({c['State']+':'+c['Building'] for c in resource_review if c['TAG']==r['TAG']}))
        if r['Resource_Review'] and r['Status']=='PASS':r['Status']='RESOURCE_OR_PM_CONFLICT'
        if row['Status']=='PASS' and row['TAG'] not in decisions:r['Correction']='NO_CHANGE_REQUIRED_IN_REVIEWED_STATIC_PROFILE'
        rows.append(r)
    csvout('STARTING_TECH_AUDIT_1776.csv',rows)
    conf=[dict(c,Disposition='OPEN_DECLARATION_RECONCILIATION; no advanced technology granted automatically',Engine_Confirmed=False) for c in after['conflicts']]
    conf += [dict(TAG=c['TAG'],State=c['State'],Building=c['Building'],Object=c['Building'],Kind=c['Kind'],Missing='POSITIVE_DISCOVERED_RESOURCE_IN_REGION_TEMPLATE',Source='map_data/state_regions',Scope='REGIONAL_TEMPLATE_ONLY_NOT_FINAL_ENGINE_ALLOCATION',Disposition=c['Detail'],Engine_Confirmed=False) for c in resource_review]
    csvout('BUILDING_TECH_CONFLICTS.csv',conf,['TAG','State','Building','Object','Kind','Missing','Source','Scope','Disposition','Engine_Confirmed'])
    review=[r for r in rows if r['Status']!='PASS'];csvout('COUNTRIES_REQUIRING_REVIEW.csv',review)
    zeros=[dict(TAG=r['TAG'],Name=r['Name'],Country_Type=r['Country_Type'],Intentional_Empty_Profile=r['Intentional_Empty_Profile'],Status=r['Status'],Evidence='Existing 1776 country research and tier choice' if r['Intentional_Empty_Profile'] else 'No historical technology conclusion; retained open without Western grant') for r in rows if r['Tech_Count']==0];csvout('EMPTY_PROFILE_EXCEPTIONS.csv',zeros)
    log=Path.home()/'Documents/Paradox Interactive/Victoria 3/logs/error.log'
    if log.exists():
        relevant=[line for line in log.read_text(encoding='utf-8-sig',errors='replace').splitlines() if 'Country BGT is not permitted to retain law' in line]
        dump('PREEXISTING_PLAYER_LOG_EXCERPT.json',dict(source=str(log),source_sha256=sha(log),existing_log_not_new_agent_engine_run=True,actual_game_test_date_unknown=True,lines=relevant,interpretation='Distinct politics/law compatibility issues; no technology is added to force modern army/interventionism. Prior human receipts are not revoked or extended.'))
    v=load(OUT/'TECH_VALIDATION.json');v.update(global_audit_status='OPEN_FINDINGS_REMAIN',complete_world_profile_certification=False,scope='72 current static guards for eight scoped country corrections, one neutral mine PM correction, exhaustive coverage and preservation; open findings explicitly enumerated.')
    dump('TECH_VALIDATION.json',v)
    stats=dict(total_countries=len(rows),new_mod_tags=sum(r['Tag_Origin']=='NEW_MOD_TAG' for r in rows),countries_with_history=sum(bool(r['History_Sources']) for r in rows),countries_with_positive_tech_count=sum(r['Tech_Count']>0 for r in rows),before_categories=dict(C.Counter(r['Status'] for r in before['rows'])),after_categories=dict(C.Counter(r['Status'] for r in rows)),changed_tags=list(ASSIGNMENTS),country_technology_additions=sum(len(decisions[t]['added']) for t in ASSIGNMENTS),missing_history_tags=[r['TAG'] for r in rows if r['Status']=='MISSING_HISTORY'],empty_profile_count=len(zeros),intentional_empty_profiles=sum(r['Intentional_Empty_Profile'] for r in zeros),building_declarations_with_conflicts_before=len(before['conflicts']),building_declarations_with_conflicts_after=len(after['conflicts']),countries_with_building_or_pm_conflicts=len({c['TAG'] for c in conf}),regional_resource_template_warnings=len(resource_review),conflict_csv_rows=len(conf),historic_or_profile_review_count=len(review),serg=dict(earned_weight=82,total_weight=235,qualified_tasks=24,total_tasks=81,percent='34.89',tracking_files_modified=False),runtime_validation='NOT_RUN_BY_AGENT')
    dump('SUMMARY.json',stats)
    print(json.dumps(stats,ensure_ascii=False),flush=True)

def tests():
    import serg_sc4_ligurian_fiefs as lig
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden','test_serg_sc1_passau_outliers','test_serg_versioned_receipts','test_serg_sc1_regensburg_demography','test_start_economy_2026_10_15','test_starting_tech_audit_1776']
    for label,names in [('TARGETED_TESTS',['test_starting_tech_audit_1776']),('CUMULATIVE_TESTS',modules)]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names));fail=[dict(id=t.id(),traceback=trace) for t,trace in r.failures+r.errors]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8');dump(label+'.json',dict(status='FAIL' if fail else 'PASS',total=r.testsRun,passed=r.testsRun-len(fail)-len(r.skipped),failed=fail,skipped=[dict(id=t.id(),reason=reason) for t,reason in r.skipped],automated_engine_test=False))
        print(label,r.testsRun-len(fail)-len(r.skipped),'/',r.testsRun,'failures',len(fail),flush=True)

def finalize():
    b=load(OUT/'BASELINE.json');v=load(OUT/'TECH_VALIDATION.json');s=load(OUT/'SUMMARY.json');targeted=load(OUT/'TARGETED_TESTS.json');cum=load(OUT/'CUMULATIVE_TESTS.json')
    previous=load(rm.OUT/'SC1-REGENSBURG-DEMOGRAPHY/TESTS.json');known={f['id'] for f in previous['failed']};unknown=[f for f in cum['failed'] if f['id'] not in known]
    assert not unknown,unknown
    review=load(rm.OUT/'SC1-REGENSBURG-DEMOGRAPHY/TEST_REVIEW.json')
    classified=[dict(id=f['id'],classification=next(r['classification'] for r in review['failed'] if r['id']==f['id']),previously_recorded=True) for f in cum['failed']]
    dump('CUMULATIVE_TEST_REVIEW.json',dict(status='NO_NEW_UNEXPLAINED_FAILURE',failed=classified,unexplained_failures=[],old_tests_not_modified=True,source='SERG_CLOSURE/SC1-REGENSBURG-DEMOGRAPHY/TEST_REVIEW.json',note='Eight old final-layer expectations, three old absence-of-genuine-receipt assertions; all retained. One inherited skip.'))
    cum.update(status='OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY',unexplained_failures=[],classification_evidence='CUMULATIVE_TEST_REVIEW.json');dump('CUMULATIVE_TESTS.json',cum)
    v['targeted_tests']=dict(passed=targeted['passed'],total=targeted['total'],failed=len(targeted['failed']));v['cumulative_tests']=dict(passed=cum['passed'],total=cum['total'],known_old_failures=len(cum['failed']),skipped=len(cum['skipped']),new_unexplained_failures=0);dump('TECH_VALIDATION.json',v)
    s['tests']=dict(static_checks=v['passed'],targeted=targeted['passed'],cumulative_passed=cum['passed'],cumulative_total=cum['total'],old_assertions=len(cum['failed']),inherited_skips=len(cum['skipped']));dump('SUMMARY.json',s)
    link=lambda name:'['+name+'](<'+(OUT/name).as_posix()+'>)'
    categories='\n'.join('| '+key+' | '+str(s['before_categories'].get(key,0))+' | '+str(s['after_categories'].get(key,0))+' |' for key in ['PASS','MISSING_HISTORY','MISSING_TECH_INITIALIZATION','INCORRECT_TECH_PROFILE','BUILDING_TECH_CONFLICT','RESOURCE_OR_PM_CONFLICT','REQUIRES_HISTORICAL_REVIEW'])
    changes=load(OUT/'PROFILE_DECISIONS.json');table='\n'.join('| '+tag+' | '+str(len(changes[tag]['before']))+' | '+str(len(changes[tag]['target']))+' | '+', '.join(changes[tag]['added'])+' |' for tag in ASSIGNMENTS)
    report='''**AUDIT TECHNOLOGIQUE 1776 — MICRO-ÉTATS ET PAYS RESTAURÉS**

Audit complet des pays présents, correction fonctionnelle partielle installée ; le monde entier n'est pas déclaré conforme. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** pour les huit corrections, aucun reçu humain nouveau.

## 1. Cause racine et moteur

BGT avait un historique, un gouvernement et un souverain, mais aucun grant de technologie : son effet politique vanilla ne donne aucun savoir. Le nouveau TAG n'hérite pas des technologies AUS. BRX et TRT n'avaient que des grants ponctuels. Syntaxe et effets contrôlés sur le vanilla local **1.13.11**, avec arbre et paliers 1776 du mod. Aucun effet vanilla 1836 copié et aucun problème d'exécution moteur prétendument observé par l'agent.

La mine BGT exige `shaft_mining` pour sa construction ; l'absence de ce gate ne prouve pas à elle seule qu'un bâtiment forcé par l'historique n'avait aucune production. La méthode additionnelle de données exigeait aussi `scientific_metrology`, sans rapport nécessaire avec l'extraction traditionnelle. Ces deux problèmes sont traités séparément.

## 2. Inventaire exhaustif et catégories

**470 pays présents**, dont **93 nouveaux TAGs du mod**. **462** ont au moins un historique retrouvé ; **442** ont un ensemble technologique non vide après correction. **252 PASS** de cohérence statique de profil, sans validation moteur. Les 28 ensembles vides restants comprennent 17 choix explicites de la recherche existante, trois cas à revoir et huit historiques absents ; ils ne sont pas assimilés à l'omission BGT.

| Catégorie principale, exclusive | Avant | Après |
| --- | ---: | ---: |
'''+categories+'''

Les colonnes détaillées conservent les anomalies simultanées. Ainsi les 45 lignes de catégorie principale bâtiments ne sont pas tous les pays ayant un conflit : **114 pays** portent au moins un signalement bâtiment/PM/ressource. Un profil en revue historique reste classé en revue même s'il porte aussi un tel signalement. Les écarts aux vieux plans ne sont pas tous des erreurs actuelles : IDs supprimés et évolutions ultérieures sont visibles.

## 3. Corrections installées

**28 ajouts ciblés**, sans suppression technologique, dans **huit pays**. Un socle commun partagé et cinq extensions étroites remplacent les listes copiées. Aucun coke, vapeur, rail, métrologie ou génie professionnel supplémentaire n'est accordé.

| TAG | Avant | Après | Ajouts |
| --- | ---: | ---: | --- |
'''+table+'''

BGT et BRX restent sans technologie militaire nouvelle. TRT reçoit notamment le parent scientifique de sa médecine déjà attribuée. PAP et CAR reçoivent seulement le parent administratif de leurs capacités militaires existantes. ARK/VIE reçoivent un socle sous leurs techniques agricoles existantes, sans certification générale de leurs profils. Liège reçoit le savoir d'extraction attesté pour sa houille, sans importer tout le profil belge. MCA conserve ses dix nœuds : pas de mine de Carrare créée pour un territoire absent du noyau.

## 4. Mine de Berchtesgaden et économie

Mine native publique **niveau 1**, capacité écrite de **5000 postes**, pioches/pelles, sans explosif ni vapeur ; **collecte de données désactivée**, sans nouvelle définition de PM. Les 10 postes de données et l'intrant papier de la recette auparavant sélectionnée disparaissent ; l'extraction conserve outils **2** → sel **20** par niveau à plein fonctionnement. Ces flux sont des paramètres écrits, pas des résultats observés. Aucune saline spéciale réintroduite, aucune subvention ou population ajoutée.

La région technique Tyrol contient **18** niveaux de sel découverts ; ce n'est pas la capacité propre à BGT. La portion locale et l'accès effectif au marché restent à vérifier. Avec **1000 habitants**, qui ne sont pas tous des actifs, et une chancellerie de 100 postes, le recrutement partiel est attendu. Aucun revenu, prix, emploi réel ou rentabilité n'est inventé ; aucun marché ou accord ajouté artificiellement.

## 5. Questions ouvertes précises

- **Huit historiques absents** : AP7, CKC, FRS, GR7, HWA, INDOP, PLW, TTI, tous décentralisés. Pas de profil occidental forcé ; recherches par communauté nécessaires.
- **Sept dettes de prérequis** : AUS, BEO, FRA, PRU, RUS, SAX et SWE possèdent `alloysworking` sans le `coke_smelting` actuellement exigé. La note historique des alliages et le graphe doivent être arbitrés ; le coke n'est pas offert pour masquer la contradiction.
- **158 profils en revue historique** et d'autres cas techniques portent notamment des différences avec les plans anciens, des profils régionaux copiés, ou les huit distributions de signaux navals classées tardives par une ancienne matrice. Les listes de 21 nœuds PAS/FSI/RBI/RCI/SLZ sont techniquement présentes et fermées, mais ne sont pas automatiquement certifiées dans toutes leurs spécialisations.
- **207 conflits de gates dans les déclarations initiales**, contre 210 avant, et **16 avertissements de ressource régionale**, soit **223 lignes** dans le CSV complet. Ports, universités, baleinières, armureries, centres commerciaux et recettes industrielles exigent une réconciliation par procédé. Certains historiques complètent d'autres couches : ce sont des signalements statiques, pas 223 blocages moteur certifiés. Aucune flotte, finance ou machine avancée attribuée en masse.
- BGT a aussi des incompatibilités politiques **préexistantes et distinctes** : variantes impériales réservées à certains TAGs n'incluant pas BGT ; écoles religieuses incompatibles avec le servage. L'effet politique vanilla demande également des lois dont les gates 1776 sont différents. Le journal existant du joueur en donne des avertissements, conservés comme extrait antérieur, sans prétendre à un nouveau test moteur. Les lois et déclencheurs restent inchangés conformément au périmètre de protection.

La liste exhaustive est dans COUNTRIES_REQUIRING_REVIEW.csv, pas dans une liste limitée aux micro-États européens. `sericulture` reste un marqueur régional ancien fonctionnel ; `can_research = no` ne suffit pas à le traiter comme obsolète.

## 6. Vérifications et conservation

**72/72 contrôles statiques**, **29/29 tests ciblés**. **521/533 tests cumulatifs réussis**, onze anciennes assertions de snapshots/reçus classées, une exclusion héritée, **aucun nouvel échec inexpliqué**. Traces et classements sont conservés ; aucun ancien test supprimé ou modifié.

Seuls trois fichiers fonctionnels appartiennent à cette passe : un nouvel effet partagé, un nouvel historique additionnel et le seul choix de PM de données dans l'historique du bâtiment BGT. Tous les anciens historiques nationaux sont identiques ; définitions de pays, souverains, lois écrites, populations, diplomaties, frontières, bâtiments/PM globaux, fortifications/génie, Anzin, drainage, infrastructures, Saint-Gobain et États-Unis sont préservés. Le marché et l'équilibre réel ne sont pas simulés par ce contrôle.

Les profils sont appelés dans l'historique national uniquement : aucune attribution au premier tick ajoutée. Le chargement réel et la sauvegarde/rechargement relèvent du protocole joueur.

## 7. Suivi et prochaine action

**SERG inchangé : 82/235, 34,89 %, 24/81 tâches qualifiées**. Tous les fichiers de suivi, événements et reçus ont gardé leurs octets. RG-D-CITY demeure distinct et en attente ; aucun nouveau PASS_RUNTIME_USER_VALIDATED, aucune tâche territoriale commencée, notamment Ortenburg. Aucun Git d'écriture ni fichier vanilla modifié.

Prochaine action : nouvelle partie, vérifier BGT et les huit profils corrigés, quelques témoins dont MCA/SLZ/PAS/Anhalt et l'échantillon asiatique, absence de paquet supplémentaire au premier jour, un mois, sauvegarde/rechargement. Le test ne clôturera pas automatiquement les régions ou les autres signalements.

'''
    report+='\nFichiers : '+', '.join(link(n) for n in ['STARTING_TECH_AUDIT_1776.csv','STARTING_TECH_BEFORE_AFTER.csv','BUILDING_TECH_CONFLICTS.csv','TECH_VALIDATION.json','SOURCES_AND_DECISIONS.md','PLAYER_TEST_PROTOCOL.md'])+'.\n'
    (OUT/'REPORT.md').write_text(report,encoding='utf8')
    dump('AUDIT_STATE.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',global_audit_status='OPEN_FINDINGS_REMAIN',changed_tags=list(ASSIGNMENTS),runtime_validation=dict(status='NOT_RUN_BY_AGENT',attestation=None,protocol='PLAYER_TEST_PROTOCOL.md'),serg_tracking_unchanged=True,territorial_task_started=False,remaining_findings='COUNTRIES_REQUIRING_REVIEW.csv',next_action='Player validation of this technical delivery; no territorial continuation automatically.'))
    (OUT/'PROGRESS_HISTORY.md').write_text('# Historique propre à l’audit technologique\n\n- 2026-10-24 — TECH-AUDIT-001 : inventaire des 470 pays actifs, diagnostic BGT, comparaison des historiques effectifs et des recherches antérieures. Suivi SERG conservé.\n- 2026-10-24 — TECH-AUDIT-002 : huit pays corrigés, 28 grants supplémentaires ; méthode neutre de données pour la mine native BGT. Aucune nouvelle validation humaine.\n- 2026-10-24 — TECH-AUDIT-003 : 72 contrôles statiques, 29 tests ciblés, 521/533 cumulatifs réussis ; onze assertions anciennes classées et une exclusion héritée. Protocole joueur prêt ; audit mondial encore ouvert pour les cas détaillés.\n',encoding='utf8')
    current=runtime.runtime_hashes();post=load(OUT/'SESSION_AFTER_STATIC.json')['hashes'];checks={}
    checks['Current runtime equals checked and tested snapshot']=current==post
    checks['Three installed functional files match reviewed bytes']=all(sha(ROOT/rel)==h for rel,h in load(OUT/'FILES_MODIFIED.json')['sha256'].items())
    checks['All SERG tracking proofs and human receipts byte preserved']=all(sha(ROOT/rel)==h for rel,h in b['serg_proofs'].items())
    checks['All earlier tools preserved']=all(sha(ROOT/rel)==h for rel,h in b['tools'].items())
    checks['72 actual static guards and 29 targeted tests pass']=v['passed']==v['total']==72 and targeted['passed']==targeted['total']==29
    checks['533 cumulative tests only same eleven old failures']=cum['total']==533 and cum['passed']==521 and {f['id'] for f in cum['failed']}==known and len(cum['skipped'])==1
    check=rm.check();checks['Canonical SERG unchanged at 82/235 24/81']=check['status']=='PASS' and load(rm.OUT/'ROADMAP_STATE.json')==b['serg_state']
    with (OUT/'STARTING_TECH_AUDIT_1776.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    checks['Complete 470-row unique named country CSV']=len(rows)==len({r['TAG'] for r in rows})==470 and all(r['Name'] for r in rows)
    with (OUT/'STARTING_TECH_BEFORE_AFTER.csv').open(encoding='utf-8-sig',newline='') as f:delta=list(csv.DictReader(f))
    checks['Eight complete before after rows']=len(delta)==8 and {r['TAG'] for r in delta}==set(ASSIGNMENTS)
    with (OUT/'BUILDING_TECH_CONFLICTS.csv').open(encoding='utf-8-sig',newline='') as f:conflicts=list(csv.DictReader(f))
    checks['223 conflict rows distinguish 207 tech gates and 16 resource warnings']=len(conflicts)==223 and sum(c['Kind']=='RESOURCE_OR_PM_CONFLICT' for c in conflicts)==16
    checks['Every new correction awaits human validation']=all(r['Status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' for r in delta) and not list(OUT.glob('RUNTIME_USER_ATTESTATION*'))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    checks['Git head branch and index unchanged']=git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index']
    checks['Required deliverables present']=all((OUT/n).is_file() for n in ['STARTING_TECH_AUDIT_1776.csv','STARTING_TECH_BEFORE_AFTER.csv','BUILDING_TECH_CONFLICTS.csv','TECH_VALIDATION.json','PLAYER_TEST_PROTOCOL.md','REPORT.md'])
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);findings=[l for l in diff.stdout.splitlines() if 'trailing whitespace.' in l];checks['Only four inherited whitespace findings']=len(findings)==4 and all(l.startswith('common/history/pops/00_west_europe.txt:') for l in findings)
    dump('DIFF_CHECK.json',dict(returncode=diff.returncode,existing_whitespace_findings=findings,own_new_files_syntax_checked=True))
    final=dict(status='PASS' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),failed=[k for k,ok in checks.items() if not ok],checks=checks,automated_engine_test=False);dump('FINAL_CHECKS.json',final);assert not final['failed'],final
    dump('SESSION_AFTER.json',dict(hashes=current,serg_check=check,git=b['git'],functional_changes=load(OUT/'FILES_MODIFIED.json'),static_only=True))
    manifest=dict(current)
    for p in OUT.rglob('*'):
        if p.is_file() and p.name!='DELIVERY_MANIFEST.json':manifest[p.relative_to(ROOT).as_posix()]=sha(p)
    for rel in ['tools/audit_starting_tech_1776.py','tools/test_starting_tech_audit_1776.py']:manifest[rel]=sha(ROOT/rel)
    dump('DELIVERY_MANIFEST.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files=manifest,global_findings_open=True,serg_untouched=True,human_attestation=None,automated_engine_test=False))
    assert all(sha(ROOT/rel)==h for rel,h in manifest.items())
    print('Final',final['passed'],'/',final['total'],'PASS; manifest',len(manifest),'files; audit worldwide findings remain open',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
