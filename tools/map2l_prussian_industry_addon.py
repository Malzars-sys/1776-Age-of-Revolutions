"""Explicit player-requested +3 arms / +10 forestry, separate from map conservation."""
import collections as C,json,sys,subprocess
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as parser
from map_1776_audit import effective,values
from map2a_patch import edits
from map2b_patch import region
from map2l_belgium import sha
import map2l_mainz as core

ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2L/SWABIA_COMPLETION/PRUSSIAN_INDUSTRY_ADDON'
ARMS='common/history/buildings/00_west_europe.txt'
LOGGING='common/history/buildings/99_1776_prussian_forestry_addon.txt'
PMS=['pm_organized_forestry','pm_no_hardwood','pm_no_equipment','pm_road_carts']

def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def prepare():
    OUT.mkdir(exist_ok=True);assert not (OUT/'BASELINE.json').exists(),'Immutable addon baseline'
    assert not (ROOT/LOGGING).exists(),'Never replace an existing file'
    raw=(ROOT/ARMS).read_text(encoding='utf-8-sig');state=region(raw,'STATE_BRANDENBURG','PRU');buildings=[n for n in state.children('create_building') if parser.scalar(n.one('building'))=='building_arms_industry'];assert len(buildings)==1
    levels=[n for n in parser.walk(buildings[0].children()) if n.key=='levels'];assert len(levels)==1 and levels[0].value=='1'
    changed=edits(raw,[(levels[0].start,levels[0].end,'levels=4')])
    logging='BUILDINGS = {\n'+''.join(' s:'+sid+' = { region_state:PRU = { create_building = { building = "building_logging_camp" add_ownership = { country = { country = "c:PRU" levels = '+str(count)+' } } reserves = 1 activate_production_methods = { '+ ' '.join('"'+pm+'"' for pm in PMS)+' } } } }\n' for sid,count in [('STATE_BRANDENBURG',6),('STATE_POMERANIA',4)])+'}\n'
    for text in [changed,logging]:parser.parse(text)
    before=qa.inventory();hashes={p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    dump('BASELINE.json',dict(inventory=before,hashes=hashes,arms_before=raw,arms_after=changed,logging_after=logging,HEAD=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_sha256=sha(ROOT/'.git/index'),exception='Human-requested additive industry; NOT territorial population/building redistribution'))
    original_out=core.OUT
    try:core.OUT=OUT;files=core.emit({ARMS:changed,LOGGING:logging},'ADDON.patch')
    finally:core.OUT=original_out
    dump('PLAN.json',dict(files=files,changes=[dict(state='STATE_BRANDENBURG',owner='PRU',building='building_arms_industry',before=1,after=4,delta=3),dict(state='STATE_BRANDENBURG',owner='PRU',building='building_logging_camp',before=0,after=6,delta=6),dict(state='STATE_POMERANIA',owner='PRU',building='building_logging_camp',before=0,after=4,delta=4)],reason='Brandenburg forestry cap=6; remaining four levels placed in Prussian Pomerania cap=11, without altering resources or borders'))
    print('Prepared exactly +3 arms and +10 logging; NOT installed')

def validate():
    b=json.loads((OUT/'BASELINE.json').read_text());a=qa.inventory();checks=[]
    def check(name,passed,detail=''):checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('Exactly intended two file contents',(ROOT/ARMS).read_text(encoding='utf-8-sig')==b['arms_after'] and (ROOT/LOGGING).read_text(encoding='utf-8-sig')==b['logging_after'])
    for key in ['owners','states','state_types','geometry','countries','pops','resolved_demographics','regional_pop','units','errors','duplicates']:
        check('Unchanged '+key,a[key]==b['inventory'][key])
    check('World population remains exact',sum(r['count'] for r in a['pops'])==835804980)
    expected=qa.counter(b['inventory']['building_levels_written']);expected['building_arms_industry']+=3;expected['building_logging_camp']+=10
    check('Exactly requested written building level increases',qa.counter(a['building_levels_written'])==expected)
    old=qa.counter(b['inventory']['buildings']);new=qa.counter(a['buildings']);remove=[];add=[]
    for row in b['inventory']['buildings']:
        if row['key'][:2]==['STATE_BRANDENBURG','PRU'] and next(n[2] for n in json.loads(row['key'][2])[2] if n[0]=='building')=='building_arms_industry':remove.append(row)
    for row in a['buildings']:
        if row['key'][:2] in [['STATE_BRANDENBURG','PRU'],['STATE_POMERANIA','PRU']]:
            node=json.loads(row['key'][2]);kind=next(n[2] for n in node[2] if n[0]=='building')
            if kind in ['building_arms_industry','building_logging_camp']:add.append(row)
    check('Exact three requested building declarations only',len(remove)==1 and len(add)==3 and new-old==qa.counter(add)-qa.counter(remove) and old-new==qa.counter(remove)-qa.counter(add))
    check('Existing arms PM reserves and economic owner unchanged',edits(b['arms_before'],[(n.start,n.end,'levels=4') for st in [region(b['arms_before'],'STATE_BRANDENBURG','PRU')] for build in st.children('create_building') if parser.scalar(build.one('building'))=='building_arms_industry' for n in parser.walk(build.children()) if n.key=='levels'])==b['arms_after'])
    for rel,digest in b['hashes'].items():
        if rel!=ARMS:check('Protected original file '+rel,sha(ROOT/rel)==digest)
    current={p.relative_to(ROOT).as_posix() for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
    check('Only intended new runtime file',current-set(b['hashes'])=={LOGGING})
    definitions={n.key:n for path in effective(ROOT,qa.GAME,'map_data/state_regions') for n in parser.parse(path.read_text(encoding='utf-8-sig'))}
    for sid,required in [('STATE_BRANDENBURG',6),('STATE_POMERANIA',4)]:
        capacity=int(definitions[sid].children('capped_resources')[0].one('building_logging_camp'));check('Logging within unchanged regional capacity '+sid,required<=capacity and [sid,'PRU'] in a['states'],str(capacity))
    pmdefs={n.key:n for path in effective(ROOT,qa.GAME,'common/production_methods') for n in parser.parse(path.read_text(encoding='utf-8-sig'))};techraw=(ROOT/'common/history/countries/pru - prussia.txt').read_text();tech={parser.scalar(n.value) for n in parser.walk(parser.parse(techraw)) if n.key=='add_technology_researched'}
    for pm in PMS:check('Logging method available to Prussia '+pm,pm in pmdefs and set(values(pmdefs[pm],'unlocking_technologies'))<=tech)
    check('HEAD and principal index unchanged',subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['HEAD'] and sha(ROOT/'.git/index')==b['index_sha256'])
    report=dict(status='PASS_STATIC_ENGINE_DEFERRED' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,automatic_engine_test=False,runtime_status='NOT_YET_TESTED',building_delta={'building_arms_industry':3,'building_logging_camp':10},population_added=0,exception_to_map_conservation=True,scope='Additive gameplay request, not a new historical map lot; cumulative map-suite receipts were captured BEFORE this authorised addon')
    dump('VALIDATION.json',report);print(report['status'],sum(r['passed'] for r in checks),'/',len(checks))
    for r in checks:
        if not r['passed']:print('FAIL',r['name'],r['detail'])
    return int(not all(r['passed'] for r in checks))

if __name__=='__main__':
    result={'prepare':prepare,'validate':validate}[sys.argv[1]]();raise SystemExit(result or 0)
