"""Current 26 October user mission, section 2: audit eight installed SERG lots.

Read gameplay only. Write new audit evidence only in CLOSURE_CAMPAIGN_2026_10_26.
This is separate from the completed documentation-consolidation mission.
"""
import collections, json, sys
from pathlib import Path
import numpy as np
import serg_sc2_teschen as previous
ROOT=previous.ROOT; rm=previous.rm; core=previous.core; reg=previous.reg
sha=previous.sha; load=previous.load
OUT=rm.OUT/'CLOSURE_CAMPAIGN_2026_10_26'; PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
TASKS=['SC2-MAP2A-VALIDATION','SC2-LUXEMBOURG-VALIDATION','SC4-MILAN-VALIDATION','SC4-PIEDMONT-VALIDATION','SC5-MINDEN-VALIDATION','SC5-COLOGNE-VALIDATION','SC5-MAINZ-VALIDATION','SC6-SWABIA-CONTINUATION-VALIDATION']
def dump(name,obj):rm.write_json(OUT/name,obj)

def audit_installed():
    b=load(OUT/'BASELINE.json'); inv=core.qa.inventory(); bitmap=core.packed(ROOT/'map_data/provinces.png')
    owners=collections.Counter({tuple(r['key']):r['count'] for r in inv['owners']}); registry=load(reg.active_registry_path())
    rows=[]; checks=[]
    def ck(task,name,ok):checks.append(dict(task_id=task,name=name,passed=bool(ok)))
    def geometry(task,folders,tags):
        gs=[load(ROOT/'docs/reports/map'/p/'GEOMETRY.json') for p in folders]
        selected=[r for r in reg.effective_assignments(gs) if r['owner'] in tags]
        for r in selected:
            rgb,sid,tag=r['rgb'],r['state'],r['owner']
            ck(task,'Unique current owner '+rgb,owners[rgb,sid,tag]==1 and sum(v for k,v in owners.items() if k[0]==rgb)==1)
            ck(task,'Reviewed cells retained '+rgb,all(int(bitmap[y,x])==int(rgb[1:],16) for x,y in r['cells']))
            ck(task,'Registered beneficiary '+rgb,any(x['rgb']==rgb and x['state']==sid and x['beneficiary']==tag for x in registry))
        return selected
    task=TASKS[0]
    for rgb,sid,tag in [('x9AC196','STATE_LOMBARDY','SWI'),('x71E080','STATE_MORAVIA','AUS'),('xF0E080','STATE_MORAVIA','AUS'),('x9061E0','STATE_WEST_GALICIA','AUS')]:
        ck(task,'MAP2A assignment '+rgb,owners[rgb,sid,tag]==1 and sum(v for k,v in owners.items() if k[0]==rgb)==1)
    ck(task,'Bergamo remains VEN',owners['x867A90','STATE_LOMBARDY','VEN']==1)
    ck(task,'Teschen technical population retained',sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==['STATE_WEST_GALICIA','AUS'])==135753)
    ck(task,'Teschen recruitment region',any(r['key'][0]=='AUS' and r['key'][2]=='STATE_WEST_GALICIA' for r in inv['units']))
    ck(task,'Teschen buildings present',any(r['key'][:2]==['STATE_WEST_GALICIA','AUS'] for r in inv['buildings']))
    rows.append(dict(task_id=task,scope='Four original MAP2A RGBs and related histories; TE-R-CORE is separate',observed_rgb=['x9AC196','x71E080','xF0E080','x9061E0'],receipt_coverage='Anciennes missions A–E/A–H testés en jeu ; aucun mois ou détail individuel MAP2A ajouté.',missing_human=['périmètre des quatre RGB en nouvelle partie 1776','bâtiments et recrutement associés','un mois complet sur ce périmètre']))
    task=TASKS[1];ck(task,'Luxembourg BEO and no initial LUX state',owners['xD001A0','STATE_WALLONIA','BEO']==1 and not any(k[2]=='LUX' for k in owners))
    source=load(ROOT/'docs/reports/map/LUX_BEO_INTEGRATION_2026-10-10/BASELINE.json')['originals']
    signatures=lambda ns:collections.Counter(core.qa.signature(n) for n in ns)
    rel='common/history/pops/00_west_europe.txt';old=core.region(source[rel],'STATE_WALLONIA','LUX');now=core.region((ROOT/rel).read_text(encoding='utf-8-sig'),'STATE_WALLONIA','BEO')
    expected=signatures(old.children('create_pop'));actual=signatures(now.children('create_pop'))
    ck(task,'Four original Luxembourg POP groups retained',all(actual[k]>=v for k,v in expected.items()) and sum(int(n.one('size')) for n in old.children('create_pop'))==137881)
    for rel in ['common/history/buildings/00_west_europe.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']:
        old=core.region(source[rel],'STATE_WALLONIA','LUX');now=core.region((ROOT/rel).read_text(encoding='utf-8-sig'),'STATE_WALLONIA','BEO')
        expected=collections.Counter({k.replace('c:LUX','c:BEO'):v for k,v in signatures(old.children('create_building')).items()});actual=signatures(now.children('create_building'))
        ck(task,'Luxembourg building declarations '+rel,all(actual[k]>=v for k,v in expected.items()))
    rel='common/history/military_formations/00_military_formations_europe.txt'
    old=next(n for n in core.cw.walk(core.cw.parse(source[rel])) if n.key=='c:LUX')
    now=next(n for n in core.cw.walk(core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))) if n.key=='c:BEO')
    expected=signatures(old.children());actual=signatures(now.children())
    ck(task,'Luxembourg formation commander and scopes',all(actual[k]>=v for k,v in expected.items()))
    nodes=core.cw.parse((ROOT/'common/history/diplomacy/00_subject_relationships.txt').read_text(encoding='utf-8-sig'));aus=next(n for n in core.cw.walk(nodes) if n.key=='c:AUS')
    ck(task,'BEO remains AUS crown land',any(n.one('country')=='c:BEO' and n.one('type')=='crown_land' for n in aus.children('create_diplomatic_pact')))
    rows.append(dict(task_id=task,scope='xD001A0 BEO, original POPs, administration, formation/commander and crown_land',receipt_coverage='Intégration approuvée et inspection belge ancienne ; pas de reçu spécifique complet.',missing_human=['Luxembourg BEO et LUX absent en nouvelle partie 1776','administration et formation de trois unités','un mois sur ce périmètre']))
    selected=geometry(TASKS[2],['MAP2L/MILAN_CREMONESE'],{'AUS'})
    rows.append(dict(task_id=TASKS[2],scope='64-cell Austrian connection xEDA701',observed_rgb=[r['rgb'] for r in selected],receipt_coverage='Reçu ancien Belgique/Franconie/Rhénanie, pas MILAN_CREMONESE.',missing_human=['raccord AUS de 64 cellules et voisins VEN/SWI','nouvelle partie et un mois']))
    ext=load(ROOT/'docs/reports/map/MAP2L/PIEDMONT/EXTENSION.json')
    for r in ext['provinces']:ck(TASKS[3],'Exact Piedmont title '+r['rgb'],any(x==r for x in registry) and owners[r['rgb'],r['state'],'SAR']==1)
    ck(TASKS[3],'Sardinia excluded',not any(r['beneficiary']=='SAR' and r['state']=='STATE_SARDINIA' for r in registry))
    rows.append(dict(task_id=TASKS[3],scope='Nine Piedmont SAR titles, Sardinia excluded',observed_rgb=[r['rgb'] for r in ext['provinces']],receipt_coverage='Autorisation d’inclusion précise, distincte d’un test attesté.',missing_human=['SAR membre, neuf RGB piémontais reconnus et Sardaigne exclue','nouvelle partie et un mois']))
    cases={TASKS[4]:(['MAP2L/MINDEN_RAVENSBERG'],{'PRU'},'Minden 76 cellules, Ravensberg séparé','Exclusion explicite de Minden dans RUNTIME_USER_VALIDATION.json.'),TASKS[5]:(['MAP2L/DUCHY_WESTPHALIA'],{'KCL'},'Duché et Vest, 84 cellules KCL','Aucun reçu nommant ce lot ultérieur.'),TASKS[6]:(['MAP2L/MAINZ_PALATINATE','MAP2L/MAINZ_ESTATES','MAP2L/MAINZ_COMPLETION'],{'KMZ'},'Trois couches Mayence ; Erfurt exclue','Aucun reçu couvrant explicitement les trois couches.'),TASKS[7]:(['MAP2L/SWABIA_CONTINUATION'],{'SFU','SEW'},'Noyaux Fürstenberg/Ellwangen','SWABIA_FINISH exclut la validation automatique de la continuation.')}
    for task,(folders,tags,scope,coverage) in cases.items():
        selected=geometry(task,folders,tags)
        rows.append(dict(task_id=task,scope=scope,observed_rgb=[r['rgb'] for r in selected],reviewed_cells=sum(r['pixels'] for r in selected),receipt_coverage=coverage,missing_human=['propriétaires, noyaux et mécanismes impériaux du lot nommé','nouvelle partie et un mois']))
    for row in rows:
        task=next(t for t in b['roadmap']['tasks'] if t['id']==row['task_id']);scopechecks=[c for c in checks if c['task_id']==row['task_id']]
        current_task=next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']==row['task_id'])
        row.update(weight=task['weight'],static_present=all(c['passed'] for c in scopechecks),static_checks=len(scopechecks),failed=[c['name'] for c in scopechecks if not c['passed']],baseline_status=task['status'],current_status=current_task['status'],can_close=False,new_human_attestation_created=False)
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',task_ids=TASKS,passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c for c in checks if not c['passed']],checks=checks,rows=rows,total_potential_points=sum(r['weight'] for r in rows),qualified_new_points=0,automated_engine_test=False)
    dump('INSTALLED_VALIDATION_AUDIT.json',result)
    print(json.dumps({k:result[k] for k in ['status','passed','total','failed','total_potential_points','qualified_new_points']},ensure_ascii=False),flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
