"""Distinguish static preservation PASS from incomplete historical geometry."""
import csv,json,subprocess
import numpy as np
import map2m_border_work as w
from map2l_registry import active_registry_path
from map2l_hre_work import GIT

def validate():
    inv=w.core.qa.inventory();bmp=w.core.packed(w.ROOT/'map_data/provinces.png');checks=[];owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in inv['owners']}
    def check(name,value,detail=''):checks.append(dict(name=name,passed=bool(value),detail=detail))
    check('Accepted northern core is still 341 cells under Sweden',int((bmp==0x567452).sum())==341 and owners['x567452']==('STATE_POMERANIA','SWE'))
    check('Unchanged inherited reference anomalies',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('Danzig remains Polish and Thorn province is not changed',owners['x80A0A0'][1]=='PLC' and owners['x41A021'][1]=='PRU')
    def levels(n):return int(n[2]) if n[0]=='levels' else sum(levels(c) for c in n[2]) if isinstance(n[2],list) else 0
    arms=0
    for row in inv['buildings']:
        if row['key'][:2]!=['STATE_BRANDENBURG','PRU']:continue
        n=json.loads(row['key'][2])
        if next(c[2] for c in n[2] if c[0]=='building')=='building_arms_industry':arms+=levels(n)*row['count']
    check('Exactly six Prussian arms-industry levels remain in Brandenburg',arms==6)
    for sector in ['PEENE','NETZE']:
        out=w.configure(sector);b=json.loads((out/'BASELINE.json').read_text());model=json.loads((out/'CANDIDATE_MODEL.json').read_text());rows=list(csv.DictReader((out/'CANDIDATE_CELLS.csv').open(encoding='utf-8-sig')))
        check(sector+' entire inventory remains exactly the accepted reference',inv==b['inventory'])
        check(sector+' all runtime bytes unchanged',all(w.core.sha(w.ROOT/rel)==digest for rel,digest in b['hashes'].items()))
        current={p.relative_to(w.ROOT).as_posix() for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for p in (w.ROOT/folder).rglob('*') if p.is_file()}
        check(sector+' no new or removed runtime files',current==set(b['hashes']))
        check(sector+' baseline bitmap and registry immutable',w.core.sha(w.ROOT/b['bitmap_backup'])==b['bitmap_sha256']==w.core.sha(w.ROOT/'map_data/provinces.png') and json.loads(active_registry_path().read_text())==b['registry'])
        check(sector+' no unapproved raster staged for installation',not (out/'provinces_candidate.png').exists())
        check(sector+' every candidate resolves to its actual RGB and unique owner',all('x'+format(int(bmp[int(r['Y']),int(r['X'])]),'06X')==r['RGB'] and owners[r['RGB']]==(r['State_ID'],r['Before']) for r in rows))
        check(sector+' protected Swedish core excluded',not any(r['RGB']=='x567452' for r in rows))
        check(sector+' all candidates explicitly unapplied',all(r['Applied']=='False' and r['Status']=='UNVALIDATED_ALIGNMENT_DO_NOT_APPLY' for r in rows) and model['accepted_cells']==0)
        check(sector+' historical source unchanged',w.core.sha(w.ROOT/model['source'])==model['source_sha256'])
        check(sector+' world population conserved',sum(r['count'] for r in inv['pops'])==835804980)
        check(sector+' Git HEAD/index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=w.ROOT,text=True).strip()==b['git_head'] and w.core.sha(w.ROOT/'.git/index')==b['git_index_sha256'])
        total=[]
        before=w.core.qa.counter(b['inventory']['regional_pop']);after=w.core.qa.counter(inv['regional_pop'])
        for key,value in sorted(before.items()):
            if key[0] in w.core.REGIONS:total.append(dict(State_ID=key[0],Owner=key[1],Culture=key[2],Religion=key[3],Before=value,After=after[key],Difference=after[key]-value))
        with (out/'POPULATION_VALIDATION.csv').open('w',encoding='utf-8-sig',newline='') as f:
            d=csv.DictWriter(f,fieldnames=list(total[0]));d.writeheader();d.writerows(total)
        sector_checks=[c for c in checks if c['name'].startswith(sector+' ') or not c['name'].startswith(('PEENE ','NETZE '))]
        report=dict(status='MAP-2M_PARTIAL',static_preservation='PASS' if all(c['passed'] for c in sector_checks) else 'FAIL',sector=sector,geometry_complete=False,historical_attribution_complete=False,candidate_cells=len(rows),applied_cells=0,new_RGBs=0,engine_tested=False,runtime_status='NO_NEW_TERRITORIAL_CHANGE_NOT_USER_VALIDATED',checks=sector_checks,blocker=model['warning'])
        (out/'VALIDATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    report=dict(status='MAP-2M_PARTIAL',static_preservation='PASS' if all(c['passed'] for c in checks) else 'FAIL',ready_for_runtime_validation=False,sectors={s:json.loads((w.BASE/s/'VALIDATION.json').read_text()) for s in ['PEENE','NETZE']},checks=checks,world_population=835804980,accepted_swedish_core_cells=341,applied_cells=0,engine_tested=False)
    (w.BASE/'VALIDATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(report['status'],report['static_preservation'],sum(c['passed'] for c in checks),'/',len(checks),'preservation checks. Historical completion gates remain FALSE.')
    return int(not all(c['passed'] for c in checks))

if __name__=='__main__':raise SystemExit(validate())
