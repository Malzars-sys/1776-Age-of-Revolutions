"""Read-only workforce diagnosis and explicit population-only startup repair."""
from pathlib import Path
import json, re, math, collections as C, sys, hashlib, difflib, subprocess
import inspect_oct09_saved_crews as saved
import validate_wallonia_start_1776 as w
import validate_diplomacy_ottoman_1776 as cw
import map2b_patch as maps
import validate_map2a as qa
from map_1776_audit import effective, values
ROOT=maps.ROOT
OUT=ROOT/'docs/reports/regional_workforce_population_1776'
MONTH=ROOT/'docs/reports/map/MAP2B/OBSERVATEUR_3_COMPARISON.json'
TARGETS=[('USA','STATE_DISTRICT_OF_COLUMBIA'),('USA','STATE_GEORGIA'),('GBR','STATE_FLORIDA'),('GBR','STATE_BERMUDA'),('GBR','STATE_JAMAICA'),('SPA','STATE_WEST_INDIES'),('CHI','STATE_ALXA'),('CHI','STATE_AMUR'),('SWE','STATE_ALAND'),('NVS','STATE_NEW_BRUNSWICK'),('FRA','STATE_GUYENNE')]
GIT='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
CONFIG={
    ('USA','STATE_DISTRICT_OF_COLUMBIA'):('05_north_america.txt','dixie',.30),
    ('USA','STATE_GEORGIA'):('05_north_america.txt','dixie',.30),
    ('GBR','STATE_FLORIDA'):('05_north_america.txt','british',.30),
    ('GBR','STATE_BERMUDA'):('05_north_america.txt','british',.30),
    ('NVS','STATE_NEW_BRUNSWICK'):('05_north_america.txt','anglo_canadian',.30),
    ('SPA','STATE_WEST_INDIES'):('06_central_america.txt','spanish',.30),
    ('GBR','STATE_JAMAICA'):('06_central_america.txt','british',.30),
    ('CHI','STATE_ALXA'):('11_east_asia.txt','manchu',.30),
    ('CHI','STATE_AMUR'):('14_siberia.txt','manchu',.30),
    ('SWE','STATE_ALAND'):('15_russia.txt','swedish',.35),
}
def protected_paths():
    return sorted({p.relative_to(ROOT).as_posix() for folder in ('common','map_data','localization','docs/reports/map')
                   for p in (ROOT/folder).rglob('*') if p.is_file()})
def capture():
    assert not (OUT/'BASELINE.json').exists(), 'Never replace the pre-population baseline.'
    originals={('common/history/pops/'+name):(ROOT/'common/history/pops'/name).read_text(encoding='utf-8-sig')
               for name,_,_ in CONFIG.values()}
    paths=protected_paths()
    write('BASELINE.json',{'head':subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'hashes':{p:qa.sha(ROOT/p) for p in paths},'originals':originals,'inventory':qa.inventory()})
    print('Captured',len(paths),'protected files; five population histories.')
def rounded_people(workers,ratio):
    return int(math.ceil(max(0,workers)/ratio/100)*100)
def make_plan():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    diag=json.loads((OUT/'DIAGNOSIS.json').read_text(encoding='utf-8'))
    inv=base['inventory']; unitdefs=w.catalog('common/combat_unit_types')
    military=C.Counter()
    for r in inv['units']:
        tag,form,sid,signature=r['key']; attrs={n[0]:n[2] for n in json.loads(signature)[2]}
        if attrs.get('service_type','regular')=='conscript': continue
        kind=attrs['type'].removeprefix('unit_type:')
        military[(tag,sid)]+=int(attrs['count'])*r['count']*int(unitdefs[kind].one('max_manpower',0))
    countries=w.catalog('common/country_definitions'); culturedefs=w.catalog('common/cultures')
    plans=[]
    for s in diag['states']:
        key=(s['country'],s['region'])
        if key not in CONFIG: continue  # Guyenne has ample labour: no population change.
        filename,culture,ratio=CONFIG[key]; path='common/history/pops/'+filename
        original_groups=maps.region(base['originals'][path],s['region'],s['country']).children('create_pop')
        initial=sum(int(n.one('size')) for n in original_groups)
        initial_free=sum(int(n.one('size')) for n in original_groups if n.one('pop_type')!='slaves')
        baseline_workforce=min(s['free_workforce'],initial_free*ratio)
        primary=values(countries[s['country']],'cultures')
        assert culture in primary, (key,culture,primary)
        assert culture in culturedefs
        jobtypes=C.Counter()
        for b in s['buildings']:
            for t,n in b['jobs_per_level'].items(): jobtypes[t]+=n*b['levels']
        # Slave labour can cover some existing agricultural labourer jobs, not roads
        # or qualified government posts. Do not count it as free labour or add slaves.
        slaves=sum(p['workforce'] for p in s['pops'] if p['type']=='slaves')
        agricultural=sum(b['jobs_per_level'].get('laborers',0)*b['levels'] for b in s['buildings']
            if b['building'].endswith(('_farm','_plantation','_ranch')))
        slave_credit=min(slaves,agricultural)
        jobs=sum(jobtypes.values())+military[key]-slave_credit
        qualified={t:sum(p['workforce'] for p in s['pops'] if p['type']==t and p['acceptance']=='full_acceptance')
                   for t in ('clerks','bureaucrats')}
        if s['region']=='STATE_JAMAICA':
            total=rounded_people(jobtypes['clerks']*1.05-qualified['clerks'],ratio)
            groups=[{'culture':culture,'religion':s['religion_of_owner'],'pop_type':'clerks','size':total}]
            reason='Qualified/accepted clerks, not a shortage of total free workforce.'
        else:
            total=rounded_people(jobs*1.05-baseline_workforce,ratio)
            assert total>0, (key,'No numerical labour deficit')
            groups=[]; remaining=total
            for t in ('bureaucrats','clerks'):
                n=min(remaining,rounded_people(jobtypes[t]-qualified[t],ratio))
                if n: groups.append({'culture':culture,'religion':s['religion_of_owner'],'pop_type':t,'size':n}); remaining-=n
            if remaining: groups.append({'culture':culture,'religion':s['religion_of_owner'],'pop_type':'laborers','size':remaining})
            reason='Free workforce below civilian job capacity plus existing permanent military manpower.'
        # Washington keeps the existing Yankee/Dixie free-population proportions.
        if s['region']=='STATE_DISTRICT_OF_COLUMBIA':
            split=[]
            for g in groups:
                y=int(round(g['size']*1133/(1133+3545)))
                split.extend([dict(g,culture='yankee',size=y),dict(g,culture='dixie',size=g['size']-y)])
            groups=split
        plans.append({'country':s['country'],'region':s['region'],'path':path,'initial_population':initial,
            'added_population':total,'new_initial_population':initial+total,'groups':groups,'reason':reason,
            'observed_free_workforce':s['free_workforce'],'observed_free_population':s['free_population'],
            'initial_free_population':initial_free,'planning_free_workforce':baseline_workforce,
            'observed_infrastructure':s['infrastructure'],'observed_usage':s['usage'],
            'civilian_job_capacity':sum(jobtypes.values()),'permanent_military_manpower_capacity':military[key],
            'existing_agricultural_slave_workforce_credit':slave_credit,'free_job_capacity_estimate':jobs,
            'workforce_ratio_model':ratio,'estimated_added_workforce':round(total*ratio,2),
            'estimated_total_free_workforce':round(baseline_workforce+total*ratio,2)})
    assert len(plans)==10
    write('PLAN.json',{'source':diag['source'],'date':diag['game_date'],'source_sha256':diag['source_sha256'],
        'world_population_added':sum(p['added_population'] for p in plans),'states':plans,
        'limitations':'Gameplay workforce calibration, not a historical census. 5% capacity margin. Recruitment, qualifications, wages and market access require a fresh native game. Military capacity excludes conscripts.'})
    for p in plans: print(p['country'],p['region'],p['initial_population'],'+',p['added_population'],'=',p['new_initial_population'],p['groups'])
def transform(originals,plans):
    result=dict(originals)
    for p in plans:
        content='\t\t\t# Workforce repair after observateur_3: gameplay calibration, not a historical census.\n'
        for g in p['groups']:
            assert g['size']>0 and g['pop_type']!='slaves'
            content+='\t\t\tcreate_pop = { culture = '+g['culture']+' religion = '+g['religion']+' pop_type = '+g['pop_type']+' size = '+str(g['size'])+' }\n'
        result[p['path']]=maps.append(result[p['path']],p['region'],p['country'],content.rstrip())
        result[p['path']]=result[p['path']].replace('\n\t\t\n\t\t\t# Workforce repair', '\n\n\t\t\t# Workforce repair')
    return result
def patch():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    plans=json.loads((OUT/'PLAN.json').read_text(encoding='utf-8'))['states']
    result=transform(base['originals'],plans); out=['*** Begin Patch']
    for p,raw in base['originals'].items():
        assert qa.sha(ROOT/p)==base['hashes'][p], 'Already edited: '+p
        diff=list(difflib.unified_diff(raw.splitlines(),result[p].splitlines(),n=18))
        if diff:
            out.append('*** Update File: '+p)
            for line in diff[2:]: out.append('@@' if line.startswith('@@') else line)
    out.append('*** End Patch'); print('\n'.join(out))
def validate():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    plan=json.loads((OUT/'PLAN.json').read_text(encoding='utf-8')); plans=plan['states']
    before=base['inventory']; after=qa.inventory(); expected=transform(base['originals'],plans)
    assert set(protected_paths())==set(base['hashes']), 'Unexpected protected file added/deleted.'
    changed=[p for p,h in base['hashes'].items() if qa.sha(ROOT/p)!=h]
    assert set(changed)==set(base['originals']), changed
    for path,raw in expected.items():
        assert (ROOT/path).read_text(encoding='utf-8-sig')==raw, 'Unexpected history edit: '+path
    for key in ('owners','states','state_types','geometry','countries','buildings','building_levels_written','units','errors','duplicates'):
        assert before[key]==after[key], 'Unrelated change: '+key
    rp=qa.counter(before['regional_pop']); pp=qa.counter(before['pops']); resolved=qa.counter(before['resolved_demographics'])
    for p in plans:
        assert (p['region'],p['country']) in map(tuple,after['states'])
        assert sum(g['size'] for g in p['groups'])==p['added_population']
        for g in p['groups']:
            key=(p['region'],p['country'],g['culture'],g['religion'])
            rp[key]+=g['size']; pp[(g['culture'],g['religion'])]+=g['size']; resolved[(g['culture'],g['religion'])]+=g['size']
        old=maps.region(base['originals'][p['path']],p['region'],p['country']).children('create_pop')
        new=maps.region(expected[p['path']],p['region'],p['country']).children('create_pop')
        assert [qa.norm(n) for n in old]==[qa.norm(n) for n in new[:len(old)]], 'Existing pop changed.'
        assert all(cw.scalar(n.one('pop_type'))!='slaves' for n in new[len(old):])
    assert rp==qa.counter(after['regional_pop'])
    assert pp==qa.counter(after['pops'])
    assert resolved==qa.counter(after['resolved_demographics'])
    initial=sum(r['count'] for r in before['pops']); final=sum(r['count'] for r in after['pops'])
    assert final-initial==plan['world_population_added']
    assert subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['head']
    import validate_regional_infrastructure_shortage as infra
    scenarios=infra.model_tests()
    cw.implementation_checks(); cw.model_tests()
    write('VALIDATION.json',{'status':'PASS_STATIC','changed_population_files':changed,'world_before':initial,'world_after':final,
        'added_population':final-initial,'states':len(plans),'protected_unchanged_files':len(base['hashes'])-len(changed),
        'existing_population_groups':'UNCHANGED; additions only, no slaves','scope_regressions':'PASS; owners, geometry, all buildings, PMs, diplomacy, military and MAP reports unchanged',
        'infrastructure_script_scenarios':scenarios,'ottoman_scripts':'PASS','native_post_patch_test':'NOT_RUN; new game plus one month required',
        'historical_MAP2B_report':'Preserved as the pre-workforce-patch result. Its exact world-population conservation assertion predates the expressly authorised additions.'})
    print('PASS_STATIC:',final-initial,'added people in',len(plans),'states;',len(changed),'population files; no unrelated gameplay changes.')
def write(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def diagnose():
    month=json.loads(MONTH.read_text(encoding='utf-8'))
    rows=[s for s in month['all_negative_states'] if (s['country'],s['region']) in TARGETS]
    wanted={s['id'] for s in rows}; builds=C.defaultdict(list); pops=C.defaultdict(list)
    countries={}; pmdefs=w.catalog('common/production_methods')
    saved.SAVE=ROOT/'.asset-cache/observateur_3_readonly.txt'
    for sec,i,raw in saved.objects():
        if sec=='building_manager' and int(saved.field(raw,'state') or -1) in wanted:
            jobcounts=C.Counter()
            unknown=[]
            for pm in w.pms(raw):
                for n in cw.walk(pmdefs[pm].children()):
                    m=re.fullmatch(r'building_employment_(.+)_add',n.key)
                    if m:
                        try: jobcounts[m[1]]+=float(n.value)
                        except (TypeError,ValueError): unknown.append(n.key)
            kind=saved.field(raw,'building'); level=float(saved.field(raw,'levels') or 0)
            builds[int(saved.field(raw,'state'))].append({'building':kind,'levels':level,'staffing':float(saved.field(raw,'staffing') or 0),
                'pms':w.pms(raw),'jobs_per_level':dict(jobcounts),'jobs_full':round(sum(jobcounts.values())*level,5),'unknown':unknown})
        elif sec=='pops' and int(saved.field(raw,'location') or -1) in wanted:
            accept=re.search(r'acceptance_status="([^"]+)"',raw)
            worker=int(saved.field(raw,'workforce') or 0); dep=int(saved.field(raw,'dependents') or 0)
            qual=re.search(r'^\t{3}qualifications=\{(.*?)^\t{3}\}',raw,re.M|re.S)
            pops[int(saved.field(raw,'location'))].append({'id':i,'type':saved.field(raw,'type'),'culture_id':saved.field(raw,'culture'),
                'religion':saved.field(raw,'religion'),'workforce':worker,'dependents':dep,'employment':saved.field(raw,'employment'),
                'acceptance':accept.group(1) if accept else None,'qualifications_raw':qual.group(1).strip() if qual else ''})
        elif sec=='country_manager' and saved.field(raw,'definition') in {t[0] for t in TARGETS}:
            countries[saved.field(raw,'definition')]={'religion':saved.field(raw,'religion')}
    for s in rows:
        bs=[b for b in builds[s['id']] if not b['building'].startswith('building_subsistence')]
        ps=pops[s['id']]; non_slave=[p for p in ps if p['type']!='slaves']
        s['buildings']=bs; s['pops']=ps
        s['free_population']=sum(p['workforce']+p['dependents'] for p in non_slave)
        s['free_workforce']=sum(p['workforce'] for p in non_slave)
        s['free_workforce_ratio']=round(s['free_workforce']/max(1,s['free_population']),8)
        s['accepted_free_workforce']=sum(p['workforce'] for p in non_slave if p['acceptance']=='full_acceptance')
        s['non_subsistence_max_jobs']=sum(b['jobs_full'] for b in bs)
        s['native_missing_jobs']=round(sum(b['jobs_per_level'].get(t,0)*(b['levels']-b['staffing']) for b in bs for t in b['jobs_per_level']),5)
        s['pop_counts_by_type']=dict(C.Counter({t:sum(p['workforce']+p['dependents'] for p in ps if p['type']==t) for t in set(p['type'] for p in ps)}))
        s['religion_of_owner']=countries[s['country']]['religion']
        print(s['country'],s['region'],'population',s['free_population'],'workforce',s['free_workforce'],'ratio',s['free_workforce_ratio'],'maxJobs',s['non_subsistence_max_jobs'],'missing',s['native_missing_jobs'],'accepted',s['accepted_free_workforce'])
        print('VACANCIES',[(b['building'],b['levels'],b['staffing'],b['jobs_full']) for b in bs if b['staffing']<b['levels']])
    write('DIAGNOSIS.json',{'source':month['source_save'],'source_sha256':month['source_sha256'],'game_date':month['game_date'],'states':rows,
        'method':'Native workforce/dependents and staffing; literal PM job counts sum all production methods, excluding subsistence jobs. Full job capacity is an upper bound; no budget or qualification guarantee.'})
if __name__=='__main__':
    if '--diagnose' in sys.argv: diagnose()
    if '--capture' in sys.argv: capture()
    if '--plan' in sys.argv: make_plan()
    if '--patch' in sys.argv: patch()
    if '--validate' in sys.argv: validate()
