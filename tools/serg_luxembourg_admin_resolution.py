"""Luxembourg-only administrative repair. No old audit/report is rewritten.

capture is recorded separately in ADMIN_R1_2026_10_26/BASELINE.json.
install patches one existing building region and two active BUILD target rows.
validate is read-only unless --write-report is explicitly supplied.
"""
import collections
import csv
import io
import json
import sys
from pathlib import Path
import serg_closure_campaign_20261026 as shared

ROOT=shared.ROOT; rm=shared.rm; core=shared.core; cw=core.cw
sha=shared.sha; load=shared.load
OUT=rm.OUT/'SC2-LUXEMBOURG-VALIDATION/ADMIN_R1_2026_10_26'
PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
TASK='SC2-LUXEMBOURG-VALIDATION'
HISTORY='common/history/buildings/00_west_europe.txt'
MATRIX='docs/reports/buildings/BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_RUNTIME_V1.csv'
PMS=['pm_simple_organization','pm_hereditary_bureaucrats','pm_religious_bureaucrats','pm_1776_no_organized_data_reporting']
BLOCK='''\t\t\tcreate_building = {
\t\t\t\tbuilding = "building_government_administration"
\t\t\t\tadd_ownership = {
\t\t\t\t\tcountry = { country = "c:BEO" levels = 1 }
\t\t\t\t}
\t\t\t\treserves = 1
\t\t\t\tactivate_production_methods = {
\t\t\t\t\t"pm_simple_organization" "pm_hereditary_bureaucrats"
\t\t\t\t\t"pm_religious_bureaucrats" "pm_1776_no_organized_data_reporting"
\t\t\t\t}
\t\t\t}
'''

def dump(name,data):rm.write_json(OUT/name,data)
def scalar(n,key,default=None):
    x=n.one(key)
    return cw.scalar(x) if x is not None else default
def records(raw):return list(csv.DictReader(io.StringIO(raw.lstrip('\ufeff'),newline='')))
def key(r):return r['Owner_TAG'],r['State_ID'],r['Building_ID']
def admin_row(r,owner):return key(r)==(owner,'STATE_WALLONIA','building_government_administration')

def building_patch(raw):
    clean=raw.lstrip('\ufeff');offset=len(raw)-len(clean)
    region=core.region(clean,'STATE_WALLONIA','BEO')
    assert not any(scalar(n,'building')=='building_government_administration' for n in region.children('create_building'))
    closing=offset+region.end-1
    assert raw[closing]=='}'
    pos=raw.rfind('\n',0,closing)+1
    assert not raw[pos:closing].strip()
    newline='\r\n' if '\r\n' in raw else '\n'
    return raw[:pos]+BLOCK.replace('\n',newline)+raw[pos:]

def matrix_patch(raw):
    """Preserve every byte of unrelated CSV records, including their quoting."""
    lines=raw.splitlines(keepends=True)
    reader=csv.DictReader(io.StringIO(raw.lstrip('\ufeff'),newline=''))
    edits=[];amendments=[];previous=1
    for row in reader:
        start,end=previous,reader.line_num;previous=end
        if not any(admin_row(row,tag) for tag in ['BEO','LUX']):continue
        before=dict(row);level=1 if row['Owner_TAG']=='BEO' else 0
        row.update(Target_Level=str(level),Delta=str(level-int(row['Current_Level'])),Decision='KEEP' if level else 'REMOVE',Base_Historical_Target_Level=str(level),Runtime_Base_Target_Level=str(level),Runtime_Level_Delta='0',Runtime_Final_Target_Level=str(level),Runtime_Overlay_Type='SERG_LUX_OWNER_RECONCILIATION',Runtime_Overlay_Reason='ADMIN_R1_2026_10_26: one provincial administration assigned to active BEO/Wallonia; inactive LUX has no starting state.')
        row['Notes']+=' | SERG_ADMIN_R1_2026_10_26: effective target owner reconciled; preimage and rationale in '+PREFIX+'BUILD_TARGET_AMENDMENT.json'
        buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=reader.fieldnames,lineterminator='\r\n' if lines[start].endswith('\r\n') else '\n');writer.writerow(row)
        edits.append((start,end,buf.getvalue()));amendments.append(dict(before=before,after=row))
    assert len(edits)==2 and {r['after']['Owner_TAG'] for r in amendments}=={'BEO','LUX'}
    for start,end,replacement in reversed(edits):lines[start:end]=[replacement]
    return ''.join(lines),amendments

def install():
    b=load(OUT/'BASELINE.json');expected={HISTORY:building_patch(b['originals'][HISTORY])}
    expected[MATRIX],amendments=matrix_patch(b['originals'][MATRIX])
    assert not (OUT/'INSTALLATION.json').exists(), 'Installation is not automatically repeated'
    for rel in expected:
        assert (ROOT/rel).read_bytes()==b['originals'][rel].encode('utf-8'), 'Concurrent change: reread and review '+rel
    dump('BUILD_TARGET_AMENDMENT.json',dict(status='INSTALLED_TARGET_RECONCILIATION_NOT_HUMAN_VALIDATION',task_ids=[TASK],reason='The positive provincial target was left on inactive LUX while active BEO/Wallonia was removed. One level is reassigned to BEO; Flanders and all other targets unchanged.',scope='One ordinary level serves the BEO portion of technical Wallonia, including Luxembourg; no separate municipality or country created.',rows=amendments,original_target_total=sum(int(r['Target_Level']) for r in records(b['originals'][MATRIX])),historical_building_count_claim=False,old_reports_and_baselines_rewritten=False))
    for rel,text in expected.items():
        assert (ROOT/rel).read_bytes()==b['originals'][rel].encode('utf-8')
        (ROOT/rel).write_bytes(text.encode('utf-8'))
    dump('INSTALLATION.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',task_ids=[TASK],functional_files=[HISTORY],active_contract_files=[MATRIX],sha256={r:sha(ROOT/r) for r in expected},population_added=0,new_territory=False,production_methods=PMS,attestation=None))
    print('Installed one BEO/Wallonia administration and two BUILD target-row corrections; no other building changed.',flush=True)

def validate(write=False):
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    raw=(ROOT/HISTORY).read_bytes().decode('utf-8');nodes=cw.parse(raw.lstrip('\ufeff'))
    ck('History syntax accepted by existing parser',bool(nodes))
    ck('Exact bounded insertion only in shared history',raw==building_patch(b['originals'][HISTORY]))
    expected_matrix,amendments=matrix_patch(b['originals'][MATRIX]);current=(ROOT/MATRIX).read_bytes().decode('utf-8')
    ck('Only two authorized CSV records changed',current==expected_matrix)
    oldrows=records(b['originals'][MATRIX]);newrows=records(current)
    ck('No matrix key added deleted or duplicated',[key(r) for r in oldrows]==[key(r) for r in newrows] and len({key(r) for r in newrows})==len(newrows))
    targets={key(r):int(r['Target_Level']) for r in newrows}
    ck('Current active BEO target one and inactive LUX target zero',targets['BEO','STATE_WALLONIA','building_government_administration']==1 and targets['LUX','STATE_WALLONIA','building_government_administration']==0)
    ck('Flanders target three untouched',targets['BEO','STATE_FLANDERS','building_government_administration']==3)
    ck('Total BUILD target levels unchanged',sum(int(r['Target_Level']) for r in oldrows)==sum(int(r['Target_Level']) for r in newrows))
    def counter(data):return collections.Counter({tuple(r['key']):r['count'] for r in data})
    old=counter(b['inventory']['buildings']);new=counter(inv['buildings'])
    block=cw.parse(BLOCK)[0];expected_key=('STATE_WALLONIA','BEO',core.qa.signature(block))
    ck('Global building-record delta is exactly the one new administration',new-old==collections.Counter({expected_key:1}) and not old-new)
    admins=[]
    for path in sorted((ROOT/'common/history/buildings').glob('*.txt')):
        ns=cw.parse(path.read_text(encoding='utf-8-sig'))
        for state in ns[0].children():
            if state.key!='s:STATE_WALLONIA':continue
            for region in state.children():
                for n in region.children('create_building'):
                    if region.key=='region_state:BEO' and scalar(n,'building')=='building_government_administration':admins.append(n)
    ck('Exactly one BEO Wallonia administration across all history layers',len(admins)==1)
    ck('Single government-owned level and reserves',len(admins)==1 and cw.normalized(admins)==cw.normalized([block]))
    for name,index in [('owners',1),('regional_pop',0),('units',2)]:
        oldscope=[r for r in b['inventory'][name] if r['key'][index] in ['STATE_WALLONIA','STATE_FLANDERS']]
        newscope=[r for r in inv[name] if r['key'][index] in ['STATE_WALLONIA','STATE_FLANDERS']]
        ck('Shared-state '+name+' unchanged',oldscope==newscope)
    owners=counter(inv['owners'])
    ck('Luxembourg BEO uniquely owned and LUX has no starting state',owners['xD001A0','STATE_WALLONIA','BEO']==1 and sum(v for k,v in owners.items() if k[0]=='xD001A0')==1 and not any(k[2]=='LUX' for k in owners))
    historical=load(ROOT/'docs/reports/map/LUX_BEO_INTEGRATION_2026-10-10/BASELINE.json')['originals']['common/history/pops/00_west_europe.txt']
    oldpop=core.region(historical,'STATE_WALLONIA','LUX');nowpop=core.region((ROOT/'common/history/pops/00_west_europe.txt').read_text(encoding='utf-8-sig'),'STATE_WALLONIA','BEO')
    popsign=lambda n:collections.Counter(core.qa.signature(p) for p in n.children('create_pop'))
    ck('All four original groups and 137881 residents retained',sum(int(n.one('size')) for n in oldpop.children('create_pop'))==137881 and all(popsign(nowpop)[k]>=v for k,v in popsign(oldpop).items()))
    formationraw=(ROOT/'common/history/military_formations/00_military_formations_europe.txt').read_text(encoding='utf-8-sig')
    beo=next(n for n in cw.walk(cw.parse(formationraw)) if n.key=='c:BEO');formation=next(n for n in beo.children('create_military_formation') if scalar(n,'name')=='Luxemburger_Miliz')
    ck('Luxembourg formation three units in Wallonia retained',sum(int(n.one('count')) for n in formation.children('combat_unit'))==3 and all(n.one('state_region')=='s:STATE_WALLONIA' for n in formation.children('combat_unit')))
    subjects=cw.parse((ROOT/'common/history/diplomacy/00_subject_relationships.txt').read_text(encoding='utf-8-sig'));aus=next(n for n in cw.walk(subjects) if n.key=='c:AUS')
    ck('AUS BEO crown_land retained',any(n.one('country')=='c:BEO' and n.one('type')=='crown_land' for n in aus.children('create_diplomatic_pact')))
    definitions={n.key:n for p in (ROOT/'common/production_methods').glob('*.txt') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
    ck('All four new PMs exist and require no technology grant',all(pm in definitions and not definitions[pm].children('unlocking_technologies') for pm in PMS))
    lawraw=(ROOT/'common/history/countries/beo - belgium old.txt').read_text(encoding='utf-8-sig')
    ck('Hereditary PM admits requested crownland law', 'law_type:law_crownland_diets' in lawraw and 'law_crownland_diets' in [n.value for p in definitions['pm_hereditary_bureaucrats'].children('unlocking_laws') for n in p.children()])
    ck('New PMs do not forbid requested BEO laws',not any(('law_type:'+n.value) in lawraw for pm in PMS for p in definitions[pm].children('disallowing_laws') for n in p.children()))
    ck('State tax and country bureaucracy effects distinct', 'state_tax_capacity_add = 2' in (ROOT/'common/production_methods/07_government.txt').read_text() and 'country_bureaucracy_add = 10' in (ROOT/'common/production_methods/07_government.txt').read_text())
    ck('All old nested SERG proofs unchanged',all(sha(ROOT/r)==h for r,h in b['prior_serg_proofs'].items() if (ROOT/r).parent!=rm.OUT))
    state=load(rm.OUT/'ROADMAP_STATE.json')
    ck('81 tasks 235 points and accepted qualifications preserved',[(t['id'],t['weight']) for t in state['tasks']]==[(t['id'],t['weight']) for t in b['roadmap']['tasks']] and rm.qualifications(state)==rm.qualifications(b['roadmap']))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',task_ids=[TASK],passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c for c in checks if not c['passed']],checks=checks,commands=['python -B -X utf8 tools/serg_luxembourg_admin_resolution.py validate --write-report'],runtime_sha256=shared.previous.runtime.runtime_hashes(),matrix_sha256=sha(ROOT/MATRIX),automated_engine_test=False)
    if write:dump('STATIC_VALIDATION.json',result)
    print(json.dumps({k:result[k] for k in ['status','passed','total','failed']},ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':
    if sys.argv[1:] and sys.argv[1]=='install':install()
    elif sys.argv[1:] and sys.argv[1]=='validate':raise SystemExit(validate('--write-report' in sys.argv)['status']!='PASS')
    else:raise SystemExit('Use install or validate [--write-report].')
