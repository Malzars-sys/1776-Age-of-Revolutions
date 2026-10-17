"""Exact requested starting levels: one Rhone arms declaration (5), Canton (10)."""
import collections as C
import json
import os
import subprocess
import sys
import start_buildings_2026_10_15 as b
from map2a_patch import edits

ROOT=b.ROOT
OUT=b.OUT/'RHONE_CANTON_FINAL_LEVELS'

def dump(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def head():
    return subprocess.check_output([b.GIT,'rev-parse','HEAD'],cwd=ROOT,text=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')).strip()

def records(rows):
    return sorted((s,t,b.qa.signature(n)) for s,t,n,p in rows)

def prepare():
    assert not (OUT/'BASELINE.json').exists(), 'Do not replace the pre-edit baseline'
    rows=b.declarations();ops={};originals={};hits=C.Counter()
    for sid,tag,node,path in rows:
        kind=b.cw.scalar(node.one('building'));rel=path.relative_to(ROOT).as_posix()
        if (sid,tag,kind)==('STATE_RHONE','FRA','building_arms_industry'):
            hits['rhone']+=1
            if rel!=b.NEW:ops.setdefault(rel,[]).append((node.start,node.end,''))
            else:
                levels=[v for v in b.cw.walk(node.children()) if v.key=='levels']
                assert len(levels)==1 and b.levels(node)==3
                v=levels[0];ops.setdefault(rel,[]).append((v.start,v.end,'levels = 5'))
        elif (sid,tag,kind)==('STATE_GUANGDONG','CHI','building_trade_center'):
            hits['canton']+=1
            levels=[v for v in b.cw.walk(node.children()) if v.key=='levels']
            assert len(levels)==1 and b.levels(node)==5
            v=levels[0];ops.setdefault(rel,[]).append((v.start,v.end,'levels=10'))
    assert hits=={'rhone':3,'canton':1}
    files={}
    for rel,changes in ops.items():
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');originals[rel]=raw;files[rel]=edits(raw,changes)
    expected=[r for r in rows if r[3].relative_to(ROOT).as_posix() not in files]
    for text in files.values():expected+=b.parse_addon(text)
    dump('BASELINE.json',dict(hashes=b.runtime_hashes(),head=head(),index_sha256=b.sha(ROOT/'.git/index'),originals=originals,expected_text=files,expected_buildings=records(expected)))
    old=b.patchwork.OUT
    try:b.patchwork.OUT=OUT;b.patchwork.emit(files,'CHANGES.patch')
    finally:b.patchwork.OUT=old
    print('Prepared: Rhone three declarations (2+2+3) consolidated to one at 5; Canton 5 -> 10.')

def validate():
    before=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'));rows=b.declarations();totals=b.totals(rows);checks=[]
    def check(name,result):checks.append(dict(name=name,passed=bool(result)))
    check('All worldwide declarations match exact reviewed transformation',records(rows)==[tuple(r) for r in before['expected_buildings']])
    arms=[n for s,t,n,p in rows if (s,t,b.cw.scalar(n.one('building')))==('STATE_RHONE','FRA','building_arms_industry')]
    check('One Rhone arms declaration, exactly five total levels',len(arms)==1 and b.levels(arms[0])==5 and totals['STATE_RHONE','FRA','building_arms_industry']==5)
    trade=[n for s,t,n,p in rows if (s,t,b.cw.scalar(n.one('building')))==('STATE_GUANGDONG','CHI','building_trade_center')]
    check('One Canton trade-centre declaration, exactly ten levels',len(trade)==1 and b.levels(trade[0])==10)
    check('Chinese Guangdong port still level five',totals['STATE_GUANGDONG','CHI','building_port']==5)
    check('No Chinese trade centres outside Canton',not any(t=='CHI' and s!='STATE_GUANGDONG' and k=='building_trade_center' and v for (s,t,k),v in totals.items()))
    for rel,text in before['expected_text'].items():
        actual=(ROOT/rel).read_text(encoding='utf-8-sig')
        check('Exact content and valid syntax '+rel,actual==text and bool(b.cw.parse(actual)))
    hashes=b.runtime_hashes();old=before['hashes']
    check('Only four targeted building-history files changed',{p for p in hashes.keys()|old.keys() if hashes.get(p)!=old.get(p)}==set(before['expected_text']))
    for r in b.forecast(rows):
        if (r['state'],r['owner']) in [('STATE_RHONE','FRA'),('STATE_GUANGDONG','CHI')]:
            check('Non-negative nominal infrastructure margin '+r['state'],r['nominal_margin']>=0)
    check('HEAD unchanged',head()==before['head'])
    check('Index unchanged',b.sha(ROOT/'.git/index')==before['index_sha256'])
    result=dict(status='PASS_STATIC_PENDING_RUNTIME' if all(c['passed'] for c in checks) else 'FAIL',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),rhone_arms_levels=5,canton_trade_levels=10,engine_tested=False)
    dump('VALIDATION.json',result)
    print(result['status'],result['passed'],'/',result['total'])
    for c in checks:
        if not c['passed']:print('FAIL',c['name'])
    assert result['status']!='FAIL'

if __name__=='__main__':{'prepare':prepare,'validate':validate}[sys.argv[1]]()
