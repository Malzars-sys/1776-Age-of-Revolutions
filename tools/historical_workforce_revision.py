"""Historical workforce follow-up: immutable full mod archive and scoped QA."""
from pathlib import Path
import json, hashlib, zipfile, subprocess, sys, collections as C
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
import map2b_patch as maps
import regional_workforce_population as prior
import validate_wallonia_start_1776 as w
import inspect_oct09_saved_crews as saved
import re, difflib
ROOT=qa.ROOT
OUT=ROOT/'docs/reports/historical_workforce_revision_1776'
GIT='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
def write(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def snapshot():
    archive=OUT/'PRE_REVISION_FULL_MOD.zip'
    assert not archive.exists() and not (OUT/'BASELINE.json').exists(), 'Snapshot is immutable.'
    OUT.mkdir(parents=True,exist_ok=True)
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and not p.is_relative_to(OUT)
                 and not any(part in ('.git','.asset-cache','__pycache__') for part in p.relative_to(ROOT).parts))
    manifest={}
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        for p in files:
            rel=p.relative_to(ROOT).as_posix(); h=hashlib.sha256()
            with p.open('rb') as src, z.open(rel,'w',force_zip64=True) as dst:
                while chunk:=src.read(1024*1024): h.update(chunk); dst.write(chunk)
            manifest[rel]={'sha256':h.hexdigest(),'bytes':p.stat().st_size}
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(manifest)
    write('SNAPSHOT_MANIFEST.json',{'date':'2026-10-11','archive':archive.name,'archive_sha256':qa.sha(archive),
        'files':manifest,'excluded':'.git database, .asset-cache derived data, __pycache__, this new report directory; no mod source or runtime asset excluded',
        'head':subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'branch':subprocess.check_output([GIT,'branch','--show-current'],cwd=ROOT,text=True).strip(),
        'git_status':subprocess.check_output([GIT,'status','--porcelain=v1'],cwd=ROOT,text=True)})
    originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig')
               for folder in ('common/history/pops','common/history/buildings','common/history/military_formations')
               for p in (ROOT/folder).glob('*.txt')}
    write('BASELINE.json',{'originals':originals,'inventory':qa.inventory(),
        'hashes':{p:v['sha256'] for p,v in manifest.items()}})
    print('Verified full archive:',len(files),'files;',archive.stat().st_size,'bytes; SHA256',qa.sha(archive))
DESTINATIONS=[('USA','STATE_NEW_YORK'),('USA','STATE_PENNSYLVANIA'),('USA','STATE_MARYLAND'),
    ('USA','STATE_SOUTH_CAROLINA'),('GBR','STATE_HOME_COUNTIES'),('GBR','STATE_LANCASHIRE'),
    ('NVS','STATE_NOVA_SCOTIA'),('SWE','STATE_SVEALAND'),('SWE','STATE_FINLAND'),
    ('SPA','STATE_LOWER_ANDALUSIA'),('SPA','STATE_CATALONIA'),('SWE','STATE_GOTALAND'),
    ('CHI','STATE_SHANXI'),('CHI','STATE_SHENGJING'),('CHI','STATE_MANCHURIA')]
def inspect():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8')); inv=base['inventory']
    keys=set(prior.CONFIG)|set(DESTINATIONS); texts=base['originals']
    results=[]
    for tag,sid in sorted(keys):
        if [sid,tag] not in inv['states']: continue
        total=sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[sid,tag])
        written=[]
        for path,raw in texts.items():
            if '/buildings/' not in path or 's:'+sid not in raw: continue
            try: region=maps.region(raw,sid,tag)
            except StopIteration: continue
            for b in region.children('create_building'):
                written.append({'path':path,'kind':cw.scalar(b.one('building')),'levels':maps.levels(b),'pms':maps.methods(b)})
        results.append({'country':tag,'region':sid,'initial_population':total,'written':written})
    saved.SAVE=ROOT/'.asset-cache/observateur_3_readonly.txt'
    countries={}; states={}; builds=C.defaultdict(list); pops=C.defaultdict(list)
    for sec,i,raw in saved.objects():
        if sec=='country_manager': countries[i]=saved.field(raw,'definition')
        elif sec=='states':
            states[i]={'id':i,'country_id':int(saved.field(raw,'country') or -1),'region':saved.field(raw,'region'),
                'infrastructure':float(saved.field(raw,'infrastructure') or 0),'usage':float(saved.field(raw,'infrastructure_usage') or 0)}
        elif sec=='building_manager':
            st=int(saved.field(raw,'state') or -1)
            builds[st].append({'id':i,'kind':saved.field(raw,'building'),'levels':float(saved.field(raw,'levels') or 0),
                'staffing':float(saved.field(raw,'staffing') or 0),'pms':w.pms(raw),'subsidized':saved.field(raw,'subsidized'),
                'inputs':w.goods(raw,'input'),'outputs':w.goods(raw,'output')})
        elif sec=='pops':
            st=int(saved.field(raw,'location') or -1); accept=re.search(r'acceptance_status="([^"]+)"',raw)
            pops[st].append({'type':saved.field(raw,'type'),'workplace':int(saved.field(raw,'workplace') or -1),'workforce':int(saved.field(raw,'workforce') or 0),
                'dependents':int(saved.field(raw,'dependents') or 0),'acceptance':accept.group(1) if accept else None})
    for row in results:
        s=next(s for s in states.values() if s['region']==row['region'] and countries[s['country_id']]==row['country'])
        row['native']=dict(s,buildings=builds[s['id']]); ps=pops[s['id']]
        row['native']['free_workforce']=sum(p['workforce'] for p in ps if p['type']!='slaves')
        row['native']['slave_workforce']=sum(p['workforce'] for p in ps if p['type']=='slaves')
        agrarian={b['id'] for b in builds[s['id']] if b['kind'].endswith(('_farm','_plantation','_ranch')) and not b['kind'].startswith('building_subsistence')}
        row['native']['agricultural_slave_workforce']=sum(p['workforce'] for p in ps if p['type']=='slaves' and p['workplace'] in agrarian)
        row['native']['free_population']=sum(p['workforce']+p['dependents'] for p in ps if p['type']!='slaves')
        row['native']['accepted_clerks']=sum(p['workforce'] for p in ps if p['type']=='clerks' and p['acceptance']=='full_acceptance')
        row['native']['accepted_bureaucrats']=sum(p['workforce'] for p in ps if p['type']=='bureaucrats' and p['acceptance']=='full_acceptance')
        print(row['country'],row['region'],'POP',row['initial_population'],'WF',row['native']['free_workforce'],'INFRA',s['infrastructure'],s['usage'])
        print('NATIVE',[(b['kind'],b['levels'],b['staffing']) for b in builds[s['id']] if 'subsistence' not in b['kind']])
        print('HISTORY',[(b['kind'],b['levels']) for b in row['written'] if b['kind'] in ('building_government_administration','building_railway','building_shipyard','building_naval_administration')])
    write('INSPECTION.json',{'date':'1776.2.1','source':'observateur_3; predates population additions and this revision','states':results})
# Explicit location changes, not historical counts of real-world offices.
BUILDING_TARGETS=[
 ('USA','STATE_DISTRICT_OF_COLUMBIA','building_government_administration',0),
 ('USA','STATE_NEW_YORK','building_government_administration',10),
 ('USA','STATE_PENNSYLVANIA','building_government_administration',14),
 ('USA','STATE_GEORGIA','building_government_administration',1),
 ('USA','STATE_MARYLAND','building_government_administration',8),
 ('GBR','STATE_FLORIDA','building_limestone_quarry',0),
 ('GBR','STATE_LANCASHIRE','building_limestone_quarry',3),
 ('SPA','STATE_WEST_INDIES','building_naval_administration',0),
 ('SPA','STATE_LOWER_ANDALUSIA','building_naval_administration',12),
]
ROAD_TARGETS=[('USA','STATE_DISTRICT_OF_COLUMBIA',1),('USA','STATE_GEORGIA',2),
 ('USA','STATE_MARYLAND',5),('USA','STATE_NEW_YORK',5),('USA','STATE_PENNSYLVANIA',7),('GBR','STATE_FLORIDA',2),('GBR','STATE_BERMUDA',1),
 ('SWE','STATE_ALAND',1),('SWE','STATE_SVEALAND',9),('SPA','STATE_WEST_INDIES',3),
 ('CHI','STATE_ALXA',2)]

def set_building(raw,sid,tag,kind,total):
    try: rs=maps.region(raw,sid,tag)
    except StopIteration: return raw,0
    bs=[b for b in rs.children('create_building') if cw.scalar(b.one('building'))==kind]
    ops=[]
    for b in bs:
        if total==0: ops.append((raw.rfind('\n',0,b.start)+1,b.end,'')); continue
        lv=[n for n in cw.walk(b.children()) if n.key in ('levels','level')]
        assert len(lv)==1, (sid,kind,'multiple economic owners require explicit allocation')
        ops.append((lv[0].start,lv[0].end,lv[0].key+' = '+str(total)))
    return maps.edits(raw,ops),len(bs)

def transformed():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    result=dict(base['originals'])
    old=json.loads((prior.OUT/'BASELINE.json').read_text(encoding='utf-8'))
    plans=json.loads((prior.OUT/'PLAN.json').read_text(encoding='utf-8'))['states']
    previous=prior.transform(old['originals'],plans)
    for path,raw in old['originals'].items():
        # No selective historical group is lost: reverse precisely the previous additions.
        assert result[path]==previous[path], 'Concurrent population edit: '+path
        result[path]=raw
    for tag,sid,kind,total in BUILDING_TARGETS:
        matches=0
        for path in result:
            if '/buildings/' not in path: continue
            result[path],n=set_building(result[path],sid,tag,kind,total); matches+=n
        assert matches, (tag,sid,kind)
    for tag,sid,total in ROAD_TARGETS:
        for path in result:
            if '/buildings/' in path:
                # Retain the PMs, economic owner and subsidies; do not undo the AI controller.
                result[path],_=set_building(result[path],sid,tag,'building_railway',total)
    path='common/history/buildings/05_north_america.txt';raw=result[path]
    # The DLC landmark is also anachronistic in 1776; retain the surrounding DLC check.
    ns=[n for n in cw.walk(cw.parse(raw)) if n.key=='create_building' and cw.scalar(n.one('building'))=='building_capitol_hill']
    assert len(ns)==1
    result[path]=maps.edits(raw,[(ns[0].start,ns[0].end,'# The federal Capitol is not present in the 1776 start.')])
    path='common/history/military_formations/00_military_formations_europe.txt';raw=result[path];ops=[]
    for country in cw.walk(cw.parse(raw)):
        if country.key not in ('c:SWE','c:GBR'): continue
        for form in country.children('create_military_formation'):
            for unit in form.children('combat_unit'):
                sid=cw.scalar(unit.one('state_region'));loc=unit.children('state_region')[0]
                assert unit.one('count') is not None
                if country.key=='c:GBR' and sid=='s:STATE_BERMUDA':
                    assert unit.one('service_type','regular')=='regular'
                    ops.append((loc.start,loc.end,'state_region = s:STATE_HOME_COUNTIES'))
                if country.key=='c:SWE' and sid=='s:STATE_ALAND':
                    assert unit.one('service_type','regular')=='regular'
                    if int(unit.one('count'))==23:
                        # Twenty recruits in Svealand, ten in Gotaland; same formation/types/count.
                        frag=raw[unit.start:unit.end];cnt=unit.children('count')[0]
                        def relocated(n,target):
                            return maps.edits(frag,[(loc.start-unit.start,loc.end-unit.start,'state_region = s:'+target),
                                (cnt.start-unit.start,cnt.end-unit.start,'count = '+str(n))])
                        ops.append((unit.start,unit.end,relocated(13,'STATE_SVEALAND')+'\n\t\t\t'+relocated(10,'STATE_GOTALAND')))
                    else: ops.append((loc.start,loc.end,'state_region = s:STATE_SVEALAND'))
    assert len(ops)==7, len(ops)
    result[path]=maps.edits(raw,ops)
    path='common/country_definitions/00_countries.txt'
    with zipfile.ZipFile(OUT/'PRE_REVISION_FULL_MOD.zip') as z: raw=z.read(path).decode('utf-8-sig').replace('\r\n','\n')
    usa=next(n for n in cw.parse(raw) if n.key=='USA');cap=usa.children('capital')[0]
    assert cw.scalar(cap.value)=='STATE_DISTRICT_OF_COLUMBIA'
    result[path]=maps.edits(raw,[(cap.start,cap.end,'capital = STATE_PENNSYLVANIA')])
    return {p:raw for p,raw in result.items() if p not in base['originals'] or raw!=base['originals'][p]}

def patch():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'));out=['*** Begin Patch']
    for path,new in transformed().items():
        assert qa.sha(ROOT/path)==base['hashes'][path], 'Edited since snapshot: '+path
        raw=(ROOT/path).read_text(encoding='utf-8-sig')
        diff=list(difflib.unified_diff(raw.splitlines(),new.splitlines(),n=5))
        assert diff
        out.append('*** Update File: '+path)
        for line in diff[2:]: out.append('@@' if line.startswith('@@') else line)
    out.append('*** End Patch');print('\n'.join(out))

def repair():
    # Rich context avoids matching repeated vanilla building templates in the wrong state.
    out=['*** Begin Patch']
    for path,new in transformed().items():
        raw=(ROOT/path).read_text(encoding='utf-8-sig')
        diff=list(difflib.unified_diff(raw.splitlines(),new.splitlines(),n=65))
        if not diff: continue
        out.append('*** Update File: '+path)
        for line in diff[2:]: out.append('@@' if line.startswith('@@') else line)
    out.append('*** End Patch');print('\n'.join(out))

def unit_totals(rows):
    counts=C.Counter()
    for row in rows:
        tag,formation,sid,signature=row['key'];attrs={n[0]:n[2] for n in json.loads(signature)[2]}
        counts[(tag,formation,attrs['type'],attrs.get('service_type','regular'))]+=int(attrs['count'])*row['count']
    return counts

def measures():
    """Scenario, not an engine forecast: retained February non-road capacity, 80% road staffing.

    Qualifications, input shortages and AI PM changes can invalidate this scenario.
    All road destinations must also pass the occupied-workforce budget check.
    """
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    rows=json.loads((OUT/'INSPECTION.json').read_text(encoding='utf-8'))['states']
    pmdefs=w.catalog('common/production_methods'); regions=w.catalog('map_data/state_regions');traits=w.catalog('common/state_traits')
    from map_1776_audit import values
    targets={(tag,sid,kind):n for tag,sid,kind,n in BUILDING_TARGETS}
    roads={(tag,sid):n for tag,sid,n in ROAD_TARGETS}
    newmil={('GBR','STATE_HOME_COUNTIES'):13,('SWE','STATE_SVEALAND'):20,('SWE','STATE_GOTALAND'):10}
    removedmil={('GBR','STATE_BERMUDA'):15,('SWE','STATE_ALAND'):29} # observed native levels, not written counts
    destinations=set(newmil)|{('USA','STATE_NEW_YORK'),('USA','STATE_PENNSYLVANIA'),('USA','STATE_MARYLAND'),('GBR','STATE_LANCASHIRE'),('SPA','STATE_LOWER_ANDALUSIA')}
    oldpop=json.loads((prior.OUT/'PLAN.json').read_text(encoding='utf-8'))['states']
    def jobs(pms):
        return sum(float(n.value) for p in pms for n in cw.walk(pmdefs[p].children()) if n.key.startswith('building_employment_') and n.key.endswith('_add'))
    results=[]
    for row in rows:
        key=(row['country'],row['region'])
        if key not in prior.CONFIG and key not in destinations: continue
        tag,sid=key;native=row['native'];bs=native['buildings']
        net=next(b for b in bs if b['kind']=='building_railway')
        commands=maps.rail_commands(base['originals'],sid,tag)
        # Latest filename wins for these overlays; confirm the road tier against effective history.
        pms=maps.methods(commands[-1][1]);new=roads.get(key,net['levels'])
        active=sum(maps.pm_fixed(p,pmdefs) for p in net['pms'])
        fixed=sum(maps.pm_fixed(p,pmdefs) for p in pms)
        terrain=sum(float(n.value) for t in values(regions[sid],'traits') if t in traits for n in cw.walk(traits[t].children()) if n.key=='state_infrastructure_mult')
        factor=min(1,native['infrastructure']/(3+active*net['staffing']),max(.05,1+terrain))
        nonroad=native['infrastructure']-active*net['staffing']*factor
        supply=nonroad+fixed*new*.8*factor
        usage=native['usage']+.1*(new-net['levels']) # retain the old cache's road overhead conservatively
        job_delta=0;level_changes=[]
        for b in bs:
            k=(tag,sid,b['kind'])
            if k not in targets: continue
            dest=targets[k];delta=dest-b['levels'];level_changes.append([b['kind'],b['levels'],dest])
            per={'building_government_administration':1,'building_naval_administration':.2,'building_limestone_quarry':2}[b['kind']]
            usage+=delta*per
            # Do not pretend empty removed buildings free already-employed people.
            job_delta+=jobs(b['pms'])*(delta if delta>0 else dest-b['staffing'])
        usage+=.2*(newmil.get(key,0)-removedmil.get(key,0))
        civilian=sum(jobs(b['pms'])*b['staffing'] for b in bs if not b['kind'].startswith('building_subsistence'))
        agri=sum(jobs(b['pms'])*b['staffing'] for b in bs if b['kind'].endswith(('_farm','_plantation','_ranch')))
        credit=min(native['agricultural_slave_workforce'],agri)
        # Receiver budget retains observed other employment, fully staffs its new roads and new critical jobs.
        barrack_staff=sum(b['staffing'] for b in bs if b['kind']=='building_barrack')
        retained_military=0 if key in removedmil else barrack_staff*1000
        occupied=civilian-credit+job_delta+jobs(pms)*new-jobs(net['pms'])*net['staffing']+1000*newmil.get(key,0)+retained_military
        destination=key in destinations
        if destination:
            assert supply-usage>=1, (key,'destination infrastructure',supply,usage)
            assert occupied<=native['free_workforce'], (key,'destination workers',occupied,native['free_workforce'])
        pop=next((p for p in oldpop if (p['country'],p['region'])==key),None)
        results.append({'country':tag,'region':sid,'population_pre_calibration':pop['initial_population'] if pop else row['initial_population'],
            'population_calibrated':row['initial_population'],'population_revised':pop['initial_population'] if pop else row['initial_population'],
            'native_observed_infrastructure':native['infrastructure'],'native_observed_usage':native['usage'],
            'native_observed_balance':round(native['infrastructure']-native['usage'],5),
            'road_levels_before':net['levels'],'road_levels_after':new,'road_jobs_after':jobs(pms)*new,
            'road_qualified_slots_after':sum(float(n.value)*new for p in pms for n in cw.walk(pmdefs[p].children()) if n.key in ('building_employment_clerks_add','building_employment_bureaucrats_add','building_employment_machinists_add')),
            'observed_accepted_clerks':native['accepted_clerks'],'observed_accepted_bureaucrats':native['accepted_bureaucrats'],
            'marginal_multiplier':factor,'native_nonroad_supply_retained':nonroad,'scenario_supply_80_percent':round(supply,5),
            'scenario_usage':round(usage,5),'scenario_balance_80_percent':round(supply-usage,5),
            'receiver':destination,'receiver_free_workforce':native['free_workforce'],
            'occupied_free_civilian_jobs_before':round(civilian-credit,3),'scenario_free_jobs_with_full_new_critical_jobs':round(occupied,3),
            'slave_credit_only_in_existing_agricultural_jobs':credit,'building_level_changes':level_changes,
            'new_regular_recruits':1000*newmil.get(key,0),'military_removed_native_levels':removedmil.get(key,0)})
    write('REVISION_MEASURES.json',{'method':'Conditional capacity scenario, not a post-patch native result. 80% roads; other observed staffed infrastructure retained; current history PMs; receiver full critical jobs plus observed other jobs, agricultural slave credit only.',
        'states':results,'world_unsupported_population_removed':882400,'USA_administration_levels_retired':14,'USA_administration_levels_relocated':10,
        'population_redistribution':'NONE: no adequately evidenced 1776 regional migration/census-scope correction; neighbour populations are unchanged.'})
    for r in results: print(r['country'],r['region'],'roads',r['road_levels_before'],r['road_levels_after'],'scenario margin',r['scenario_balance_80_percent'],'receiver workers',r['scenario_free_jobs_with_full_new_critical_jobs'],r['receiver_free_workforce'])

def validate():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'));expected=transformed();before=base['inventory'];after=qa.inventory()
    changed=[p for p,h in base['hashes'].items() if qa.sha(ROOT/p)!=h]
    assert set(changed)==set(expected)|{'tools/historical_workforce_revision.py'}, changed
    for path,raw in expected.items():
        assert (ROOT/path).read_text(encoding='utf-8-sig')==raw, 'Unexpected edit: '+path
        original=base['originals'].get(path)
        if original is None:
            with zipfile.ZipFile(OUT/'PRE_REVISION_FULL_MOD.zip') as z: original=z.read(path).decode('utf-8-sig').replace('\r\n','\n')
        assert not [s for s in difflib.ndiff(original.splitlines(),raw.splitlines())
                    if s.startswith('+ ') and s[2:] and s[2:]!=s[2:].rstrip()], 'New trailing whitespace: '+path
    for key in ('owners','states','state_types','geometry','errors','duplicates'):
        assert before[key]==after[key], 'MAP/reference regression: '+key
    old=json.loads((prior.OUT/'BASELINE.json').read_text(encoding='utf-8'))['inventory']
    for key in ('pops','regional_pop','resolved_demographics'):
        assert after[key]==old[key], 'Original population changed: '+key
    assert unit_totals(before['units'])==unit_totals(after['units']), 'Unit counts, types, service or formations changed.'
    new_countries=dict(after['countries']);new_countries['USA']=before['countries']['USA']
    assert new_countries==before['countries'], 'Other country definition changed.'
    # Compare non-target building commands rather than global totals of duplicate overlays.
    targeted={(sid,tag,kind) for tag,sid,kind,_ in BUILDING_TARGETS}|{(sid,tag,'building_railway') for tag,sid,_ in ROAD_TARGETS}|{('STATE_DISTRICT_OF_COLUMBIA','USA','building_capitol_hill')}
    def unrelated(inv):
        return [r for r in inv['buildings'] if (r['key'][0],r['key'][1],next(n[2] for n in json.loads(r['key'][2])[2] if n[0]=='building')) not in targeted]
    assert unrelated(before)==unrelated(after), 'Unrelated building changed.'
    snapshot=json.loads((OUT/'SNAPSHOT_MANIFEST.json').read_text(encoding='utf-8'))
    assert subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==snapshot['head']
    import validate_regional_infrastructure_shortage as infra
    scenarios=infra.model_tests();cw.implementation_checks();cw.model_tests()
    measures()
    write('VALIDATION.json',{'status':'PASS_STATIC','gameplay_files':list(expected),'world_before':sum(r['count'] for r in before['pops']),
        'world_after':sum(r['count'] for r in after['pops']),'population_removed':882400,'original_pop_groups':'Identical to pre-economic-addition histories, including cultures/religions/slave status',
        'territories_and_dependencies':'UNCHANGED; exact province/state ownership and geometry comparisons',
        'military':'Same national counts, types, conscripts and formations; only explicitly authorised SWE/GBR recruitment locations changed',
        'protected_files':len(base['hashes'])-len(changed),'infrastructure_scenarios':scenarios,'ottoman_tests':'PASS',
        'receiver_capacity_and_occupied_workforce_scenarios':'PASS; 8 destinations; conditional 80% road scenario, not engine verification',
        'new_trailing_whitespace':'NONE; existing unrelated whitespace preserved',
        'native_post_revision':'NOT_RUN; observateur_3 is pre-revision evidence, not a test of these changes',
        'snapshot_sha256':snapshot['archive_sha256'],'commit_merge_push':'NONE'})
    print('PASS_STATIC',len(expected),'gameplay files; 882400 unsupported additions retired; original populations and non-target gameplay preserved.')

if __name__=='__main__':
    if '--snapshot' in sys.argv: snapshot()
    if '--inspect' in sys.argv: inspect()
    if '--patch' in sys.argv: patch()
    if '--repair' in sys.argv: repair()
    if '--measures' in sys.argv: measures()
    if '--validate' in sys.argv: validate()
