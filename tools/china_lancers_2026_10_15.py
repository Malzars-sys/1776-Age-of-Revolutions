"""Replace Chinese starting cavalry types only; preserve every formation detail."""
import collections as C
import json
import os
import subprocess
import sys
import start_buildings_2026_10_15 as b
from map2a_patch import edits

ROOT=b.ROOT
OUT=ROOT/'docs/reports/military/CHINA_LANCERS_2026_10_15'
TARGET='unit_type:combat_unit_type_lancers'

def dump(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def head():
    return subprocess.check_output([b.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')).strip()

def cavalry():
    result=C.Counter();types=b.catalog('common/combat_unit_types')
    for path in b.effective(ROOT,b.qa.GAME,'common/history/military_formations'):
        for country in b.cw.walk(b.cw.parse(path.read_text(encoding='utf-8-sig'))):
            if country.key!='c:CHI':continue
            for formation in country.children('create_military_formation'):
                for unit in formation.children('combat_unit'):
                    kind=b.cw.scalar(unit.one('type')).removeprefix('unit_type:')
                    if types[kind].one('group')=='combat_unit_group_cavalry':result[kind]+=int(unit.one('count'))
    return dict(result)

def prepare():
    assert not (OUT/'BASELINE.json').exists(), 'Never replace the pre-edit reference'
    originals={};expected={};changes=[];types=b.catalog('common/combat_unit_types')
    for path in b.effective(ROOT,b.qa.GAME,'common/history/military_formations'):
        raw=path.read_text(encoding='utf-8-sig');ops=[]
        for country in b.cw.walk(b.cw.parse(raw)):
            if country.key!='c:CHI':continue
            for formation in country.children('create_military_formation'):
                for unit in formation.children('combat_unit'):
                    field=unit.children('type')[0];kind=b.cw.scalar(field.value).removeprefix('unit_type:')
                    if types[kind].one('group')!='combat_unit_group_cavalry' or field.value==TARGET:continue
                    ops.append((field.start,field.end,'type = '+TARGET))
                    changes.append(dict(file=path.relative_to(ROOT).as_posix(),line=raw[:field.start].count('\n')+1,
                         formation=formation.one('name'),state=unit.one('state_region'),service_type=unit.one('service_type','regular'),
                         before=kind,after='combat_unit_type_lancers',battalions=int(unit.one('count'))))
        if ops:
            assert path.is_relative_to(ROOT)
            rel=path.relative_to(ROOT).as_posix();originals[rel]=raw;expected[rel]=edits(raw,ops)
    assert changes
    dump('BASELINE.json',dict(originals=originals,expected=expected,hashes=b.runtime_hashes(),head=head(),index_sha256=b.sha(ROOT/'.git/index'),
                              cavalry_before=cavalry(),changes=changes))
    previous=b.patchwork.OUT
    try:b.patchwork.OUT=OUT;b.patchwork.emit(expected,'CHANGES.patch')
    finally:b.patchwork.OUT=previous
    print('Prepared',sum(r['battalions'] for r in changes),'battalions in',len(changes),'recruitment entries')

def validate():
    before=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'));checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value)))
    for rel,expected in before['expected'].items():
        raw=(ROOT/rel).read_text(encoding='utf-8-sig')
        check('Exact type-only change; counts, service, states, names and commands preserved: '+rel,raw==expected)
        check('Valid syntax '+rel,bool(b.cw.parse(raw)))
    hashes=b.runtime_hashes()
    check('No other functional files changed',{p for p in hashes.keys()|before['hashes'].keys() if hashes.get(p)!=before['hashes'].get(p)}==set(before['expected']))
    total=sum(before['cavalry_before'].values());now=cavalry()
    check('All starting Chinese cavalry are lancers',now=={'combat_unit_type_lancers':total})
    check('All 60 cavalry battalions retained',total==60)
    definition=b.catalog('common/combat_unit_types')['combat_unit_type_lancers']
    check('Lancers already unlocked for China',set(b.values(definition,'unlocking_technologies'))<=b.starting_tech('CHI'))
    check('Lancer upkeep has no small-arms input',not any(n.key=='goods_input_small_arms_add' for n in b.cw.walk(definition.children('upkeep_modifier'))))
    check('No arms technology granted','regulated_small_arms' not in b.starting_tech('CHI'))
    check('HEAD unchanged',head()==before['head'])
    check('Git index unchanged',b.sha(ROOT/'.git/index')==before['index_sha256'])
    result=dict(status='PASS_STATIC_PENDING_RUNTIME' if all(c['passed'] for c in checks) else 'FAIL',checks=checks,
                passed=sum(c['passed'] for c in checks),total=len(checks),cavalry_before=before['cavalry_before'],cavalry_after=now,
                functional_files=list(before['expected']),engine_tested=False)
    dump('VALIDATION.json',result)
    print(result['status'],result['passed'],'/',result['total'],'checks;',now)
    for c in checks:
        if not c['passed']:print('FAIL',c['name'])
    assert result['status']!='FAIL'

if __name__=='__main__':{'prepare':prepare,'validate':validate}[sys.argv[1]]()
