"""Independent conservation checks against the actual MAP-2E dirty baseline.
These are written-history/static-model checks, never an engine test.
"""
import collections as C, contextlib, io, json, re, subprocess, sys
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2e_work import ROOT,GAME,OUT,BASE,TARGETS,GIT,sha,source_bitmap
from map2e_patch import GROUPS,OLD,DUP_REMOVE,NEW,transform
from map_1776_audit import effective
def attribute_populations(originals):
    result=C.Counter()
    for path,raw in originals.items():
        if not path.startswith(('common/history/pops/','common/history/population/')):continue
        for p in cw.walk(cw.parse(raw)):
            if p.key=='create_pop':
                attrs=[qa.norm(n) for n in p.children() if n.key!='size'];result[json.dumps(attrs,separators=(',',':'))]+=int(p.one('size'))
    return result
def weighted_buildings(rows):
    out=C.Counter()
    for row in rows:
        sid,tag,body=row['key'];tree=json.loads(body)
        def normalize(n):
            key,op,val=n
            if isinstance(val,list):
                if key=='building' and any(v[0]=='country' and v[2]=='c:PER' for v in val):
                    val=[[k,o,'STATE_TABRIZ' if k=='region' and v in {'STATE_ARMENIA','STATE_AZERBAIJAN','STATE_ELIZAVETPOL'} else v] for k,o,v in val]
                return [key,op,[normalize(v) for v in val]]
            return [key,op,'PER_LEVEL' if key=='levels' else val]
        def levels(n):return int(n[2]) if n[0]=='levels' else sum(levels(v) for v in n[2]) if isinstance(n[2],list) else 0
        out[(sid,json.dumps(normalize(tree),separators=(',',':')))]+=levels(tree)*row['count']
    return out
def unit_totals(rows,with_region=False):
    out=C.Counter()
    for r in rows:
        country,formation,sid,body=r['key'];n=json.loads(body)
        attrs=[v for v in n[2] if v[0] not in ('count','state_region')];key=[country,formation,json.dumps(attrs,separators=(',',':'))]
        if with_region:key.append(sid)
        out[tuple(key)]+=int(next(v[2] for v in n[2] if v[0]=='count'))*r['count']
    return out
def regional_totals(inv):
    out=C.Counter()
    for r in inv['regional_pop']:out[r['key'][0]]+=r['count']
    return out
def run():
    b=json.loads(BASE.read_text(encoding='utf-8'));before=b['inventory'];after=qa.inventory();checks=[]
    def check(name,condition,detail=None):
        checks.append({'test':name,'status':'PASS' if condition else 'FAIL','detail':detail})
    expected=qa.counter(before['owners'])
    for sid,groups in GROUPS.items():
        for t,vs in groups.items():
            for v in vs:expected[(v,sid,OLD[sid])]-=1;expected[(v,sid,t)]+=1
    for sid,tags in DUP_REMOVE.items():
        for t,vs in tags.items():
            for v in vs:expected[(v,sid,t)]-=1
    check('Exact authorized owner changes',+expected==qa.counter(after['owners']))
    check('No lost or new province IDs',{r['key'][0] for r in before['owners']}=={r['key'][0] for r in after['owners']})
    check('State Region province geometry unchanged',before['geometry']==after['geometry'])
    check('Bitmap byte-exact including MAP2C and Budjak',b['bitmap_sha256']==sha(source_bitmap()),b['bitmap_sha256'])
    check('Nine Caucasus duplicates resolved',len(before['duplicates'])-len(after['duplicates'])==9)
    check('No new duplicates',all(before['duplicates'].get(k,0)>=v for k,v in after['duplicates'].items()),len(after['duplicates']))
    check('No new orphan/invalid RGB selectors',set(map(str,after['errors']))<=set(map(str,before['errors'])),after['errors'])
    check('World population exactly 835804980',sum(r['count'] for r in after['pops'])==835804980)
    check('All global cultures/religions unchanged',before['pops']==after['pops'] and before['resolved_demographics']==after['resolved_demographics'])
    check('All State Region populations unchanged',regional_totals(before)==regional_totals(after))
    current={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in b['originals']}
    check('Every pop attribute and free/slave status conserved',attribute_populations(b['originals'])==attribute_populations(current))
    check('All declared building levels unchanged',before['building_levels_written']==after['building_levels_written'])
    check('Per-region building levels, PMs, reserves and economic owners conserved',weighted_buildings(before['buildings'])==weighted_buildings(after['buildings']))
    check('National units, formations and service types conserved',unit_totals(before['units'])==unit_totals(after['units']))
    expected_units=qa.counter(before['units']);ee=C.Counter()
    for (t,f,s,body),n in expected_units.items():
        if t=='PER' and s=='STATE_ARMENIA':s='STATE_TABRIZ';body=body.replace('s:STATE_ARMENIA','s:STATE_TABRIZ')
        ee[(t,f,s,body)]+=n
    check('Only authorized Persian recruitment relocation',ee==qa.counter(after['units']))
    changes,moves,weights,bt=transform(b)
    mismatched=[p for p,v in changes.items() if (ROOT/p).read_text(encoding='utf-8-sig')!=v.removeprefix('\ufeff')]
    check('Every patched text matches baseline-derived plan',not mismatched,mismatched)
    changed_existing=[p for p,h in b['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    check('No protected out-of-scope file changed',set(changed_existing)==set(changes)&set(b['hashes']),changed_existing)
    allowed_new={p for p in changes if p not in b['hashes']};new_runtime={p.relative_to(ROOT).as_posix() for f in ['common','map_data','gfx','events','localization','.metadata'] for p in (ROOT/f).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in b['hashes']}
    check('Only planned new runtime files',new_runtime==allowed_new,sorted(new_runtime))
    check('Existing nations retained',set(before['countries'])<=set(after['countries']))
    check('Only Erivan/Quba reused country definitions adjusted',{k for k in before['countries'] if before['countries'][k]!=after['countries'][k]}=={'ARM','AZB'})
    check('Exactly seven major new TAGs',set(after['countries'])-set(before['countries'])==set(NEW))
    check('All new/reused countries have owned capitals',all((cw.scalar(next(n[2] for n in json.loads(after['countries'][t])[2] if n[0]=='capital')),t) in {tuple(s) for s in after['states']} for t in [*NEW,'ARM','AZB','ABK']))
    # Validate native symbols without treating the parser as an engine executor.
    technologies={s.key for p in effective(ROOT,GAME,'common/technology/technologies') for s in cw.parse(p.read_text(encoding='utf-8-sig'))}
    laws={s.key for p in effective(ROOT,GAME,'common/laws') for s in cw.parse(p.read_text(encoding='utf-8-sig'))}
    countries=cw.parse((ROOT/'common/history/countries/1776_caucasus_local_authorities.txt').read_text(encoding='utf-8-sig'))
    check('All new-country technologies exist',all(cw.scalar(n.value) in technologies for n in cw.walk(countries) if n.key=='add_technology_researched'))
    check('All new-country laws exist',all(cw.scalar(n.value).removeprefix('law_type:') in laws for n in cw.walk(countries) if n.key=='activate_law'))
    coa=cw.parse((ROOT/'common/coat_of_arms/coat_of_arms/04_1776_caucasus.txt').read_text(encoding='utf-8-sig'))
    check('All seven new flags have valid native textures',set(n.key for n in coa)==set(NEW) and all((GAME/('gfx/coat_of_arms/'+('patterns/' if n.key=='pattern' else 'colored_emblems/')+cw.scalar(n.value))).exists() for n in cw.walk(coa) if n.key in ('texture','pattern')))
    locales={}
    for lang in ['french','english']:
        pp=ROOT/f'localization/{lang}/1776_caucasus_l_{lang}.yml';raw=pp.read_bytes();locales[lang]=set(re.findall(r'^\s*([\w_]+):0',raw.decode('utf-8-sig'),re.M));check('Localization BOM '+lang,raw.startswith(b'\xef\xbb\xbf'))
    check('French/English keys identical',locales['french']==locales['english'])
    effect=cw.parse((ROOT/'common/scripted_effects/1776_caucasus_state_names.txt').read_text(encoding='utf-8-sig'))
    used={cw.scalar(n.value) for n in cw.walk(effect) if n.key=='set_state_name'}|{'aor1776_'+t.lower()+s for t in ['ARM','AZB','CHC'] for s in ['', '_adj']}
    check('All targeted state/name references localized',used<=locales['english'])
    check('Primary Git HEAD, index and refs untouched',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT).decode().strip()==b['git']['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT).decode().strip()==b['git']['refs'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    suites={}
    import validate_regional_infrastructure_shortage as infr
    for name,fn in [('Ottoman journals',cw.model_tests),('Infrastructure AI',infr.model_tests)]:
        log=io.StringIO()
        try:
            with contextlib.redirect_stdout(log):answer=fn()
            suites[name]={'status':'PASS','result':answer,'output':log.getvalue()};check(name+' existing AST fixtures',True)
        except Exception as e:suites[name]={'status':'FAIL','error':str(e)};check(name+' existing AST fixtures',False,str(e))
    result={'status':'PASS_STATIC' if all(r['status']=='PASS' for r in checks) else 'FAIL_STATIC','native_engine':'NOT_RUN','baseline_checkpoint':b['checkpoint'],'world_population_before':835804980,'world_population_after':sum(r['count'] for r in after['pops']),'ownership_transfers':45,'duplicate_removals':9,'bitmap_edits':0,'duplicates_before':62,'duplicates_after':len(after['duplicates']),'preexisting_reference_errors':after['errors'],'checks':checks,'regression_suites':suites,'modified_runtime_files':list(changes)}
    (OUT/'MAP2E_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    pops=qa.counter(before['regional_pop']);now=qa.counter(after['regional_pop']);keys=sorted(k for k in pops.keys()|now.keys() if k[0] in TARGETS)
    population=[[*k,pops[k],now[k],now[k]-pops[k]] for k in keys]
    (OUT/'TABLE_DATA.json').write_text(json.dumps({'territorial':moves,'population':population,'summary_pop':[[s,t,sum(r['count'] for r in before['regional_pop'] if r['key'][:2]==[s,t]),sum(r['count'] for r in after['regional_pop'] if r['key'][:2]==[s,t])] for s,t in sorted({(k[0],k[1]) for k in keys})],'building_transfers':bt},ensure_ascii=False,indent=2),encoding='utf-8')
    print(result['status'],len(checks),'checks;',len(population),'demographic rows')
    for r in checks:
        if r['status']=='FAIL':print('FAILED',r['test'],r['detail'])
    return result['status']=='PASS_STATIC'
if __name__=='__main__':raise SystemExit(0 if run() else 1)
