"""Targeted follow-up: remove only initial Tabriz food factories, including overlays."""
import json, sys, subprocess
from pathlib import Path
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from persian_recruitment_map2e import ROOT,GIT,sha,hashes
from map_1776_audit import effective
from map2e_work import GAME

OUT=ROOT/'docs/reports/map/MAP2E/TABRIZ_FOOD_REMOVAL'
FILES=['common/history/buildings/08_middle_east.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']
def targets(raw):
    return [n for s in cw.walk(cw.parse(raw)) if s.key=='s:STATE_TABRIZ' for r in s.children('region_state:PER') for n in r.children('create_building') if cw.scalar(n.one('building'))=='building_food_industry']
def dump(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def capture():
    assert not (OUT/'BASELINE.json').exists(),'Baseline already exists'
    originals={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in FILES}
    assert all(len(targets(raw))==1 for raw in originals.values())
    dump('BASELINE.json',{'originals':originals,'inventory':qa.inventory(),'hashes':{p:h for p,h in hashes().items() if not p.startswith('docs/reports/map/MAP2E/TABRIZ_FOOD_REMOVAL/')},'head':subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'refs':subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip(),'index':sha(ROOT/'.git/index')})
    print('Captured lightweight baseline; two duplicate startup declarations, each level 1')
def validate():
    b=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'));after=qa.inventory();checks=[]
    def check(name,passed):checks.append({'test':name,'status':'PASS' if passed else 'FAIL'})
    for p,raw in b['originals'].items():
        n=targets(raw)[0];expected=raw[:n.start]+raw[n.end:]
        check('Only food create_building removed: '+p,[qa.norm(n) for n in cw.parse(expected)]==[qa.norm(n) for n in cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))])
    for field in b['inventory']:
        if field not in ('buildings','building_levels_written'):check('Unchanged '+field,b['inventory'][field]==after[field])
    check('No effective Tabriz food declaration remains',not any(targets(p.read_text(encoding='utf-8-sig')) for p in effective(ROOT,GAME,'common/history/buildings')))
    changed={p for p,h in b['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h}
    check('Only the two authorized history files changed',changed==set(FILES))
    check('Git HEAD, refs and index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==b['refs'] and sha(ROOT/'.git/index')==b['index'])
    result={'status':'PASS_STATIC' if all(c['status']=='PASS' for c in checks) else 'FAIL_STATIC','checks':checks,'files':FILES,'native_test':'NOT_RUN','declarations_removed':2,'levels_per_declaration':1,'note':'Two overlapping startup declarations of the same food industry removed. No claim that these represented two distinct native buildings. All other file AST content, units, population, ownership and map preserved.'}
    dump('VALIDATION.json',result)
    print(result['status'],len(checks),'checks')
    for c in checks:
        if c['status']=='FAIL':print(c)
    return result['status']=='PASS_STATIC'
if __name__=='__main__':
    if {'capture':capture,'validate':validate}[sys.argv[1]]() is False:raise SystemExit(1)
