"""Read-back checks for final MAP-2E deliverables. Does not change gameplay."""
import csv,json
from pathlib import Path
from map2e_work import OUT

def run():
    checks=[]
    def check(name,ok):checks.append({'test':name,'status':'PASS' if ok else 'FAIL'})
    data=json.loads((OUT/'TABLE_DATA.json').read_text(encoding='utf-8'))
    def rows(name):
        with (OUT/name).open(encoding='utf-8',newline='') as f:return list(csv.reader(f))
    t=rows('MAP2E_TERRITORIAL_CHANGES.csv');p=rows('MAP2E_POPULATION_VALIDATION.csv');u=rows('MAP2E_UNRESOLVED.csv')
    check('54 territorial records, each with 14 columns',len(t)==55 and all(len(r)==14 for r in t))
    check('Territorial CSV matches planned RGB/owners and numeric geometry',all([*r[:5],*map(int,r[5:10])]==d for r,d in zip(t[1:],data['territorial'])))
    check('Exactly 45 transfers and nine duplicate resolutions',sum(r[4]=='DOCUMENTED_GAMEPLAY_APPROXIMATION' for r in t[1:])==45 and sum(r[4]=='DUPLICATE_RESOLVED' for r in t[1:])==9)
    check('191 population records plus total',len(p)==193 and all(len(r)==7 for r in p))
    check('Population CSV matches source groups, counts and deltas',all([*r[:4],*map(int,r[4:])]==d for r,d in zip(p[1:-1],data['population'])))
    check('Population totals 3749856, no change',list(map(int,p[-1][4:]))==[3749856,3749856,0] and sum(int(r[4]) for r in p[1:-1])==sum(int(r[5]) for r in p[1:-1])==3749856)
    check('13 unresolved/approximation records',len(u)==14 and all(len(r)==5 for r in u))
    check('Five required outputs exist',all((OUT/f).is_file() for f in ['MAP2E_EXECUTIVE_SUMMARY.md','MAP2E_TERRITORIAL_CHANGES.csv','MAP2E_POPULATION_VALIDATION.csv','MAP2E_UNRESOLVED.csv','MAP2E_VALIDATION.json']))
    v=json.loads((OUT/'MAP2E_VALIDATION.json').read_text(encoding='utf-8'))
    check('Latest runtime validation passes 32 tests, native pending',v['status']=='PASS_STATIC' and len(v['checks'])==32 and all(r['status']=='PASS' for r in v['checks']) and v['native_engine']=='NOT_RUN')
    backup=json.loads((OUT/'MAP2E_BACKUP_AND_CLEANUP.json').read_text(encoding='utf-8'))
    check('Only verified temporary copies removed; sums reconcile',all(not(Path(backup['removed_base'])/r['path']).exists() for r in backup['removed']) and sum(r['bytes'] for r in backup['removed'])==backup['reclaimed_logical_bytes'] and sum(r['files'] for r in backup['removed'])==backup['removed_files'])
    result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','checks':checks}
    (OUT/'QA/DELIVERABLE_VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(result['status'],len(checks),'deliverable read-back checks')
    for c in checks:
        if c['status']=='FAIL':print(c)
    return result['status']=='PASS'
if __name__=='__main__':raise SystemExit(0 if run() else 1)
