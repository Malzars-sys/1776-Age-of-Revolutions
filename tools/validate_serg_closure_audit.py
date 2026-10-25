"""Read-only checks of the audit deliverables, not a Victoria 3 engine test."""
from pathlib import Path
import collections,csv,hashlib,json,re
from PIL import Image
from serg_global_closure_audit import ROOT,OUT,save

def run():
    checks=[]
    def check(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
    required=['REPORT.md','REGIONAL_COVERAGE.csv','IMPERIAL_STATES_INVENTORY.csv','COMPLETED_LOTS.csv','REMAINING_WORK.csv','UNCOVERED_REGIONS.csv','ABSTRACTIONS_AND_DEFERRED.csv','CLOSURE_ROADMAP.md','CLOSURE_CRITERIA.md','SOURCE_AND_REPORT_INDEX.md','SERG_COVERAGE_MAP.png']
    for n in required:check('deliverable_'+n,(OUT/n).exists() and (OUT/n).stat().st_size>100)
    tables=json.loads((OUT/'TABLE_DATA.json').read_text())
    cv=json.loads((OUT/'CSV_VALIDATION.json').read_text())
    for n,expected in tables.items():
        with (OUT/(n+'.csv')).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        check('csv_rows_'+n,len(rows)==len(expected),len(rows))
        headers=list(expected[0])
        def text(v):
            if v is None:return ''
            if isinstance(v,bool):return str(v).lower()
            return str(v)
        check('csv_exact_values_'+n,all({k:text(v) for k,v in record.items()}==actual for record,actual in zip(expected,rows)))
        receipt=next(x for x in cv['checks'] if x['file']==n+'.csv')
        check('artifact_roundtrip_'+n,receipt['range_verified'] and receipt['csv_roundtrip_verified'])
        check('csv_hash_'+n,hashlib.sha256((OUT/(n+'.csv')).read_bytes()).hexdigest()==receipt['sha256'])
        for r in rows:
            for column in ('Preuve','Rapport','Attestation','Lot_ou_date','Inventaire_ancien'):
                value=r.get(column,'')
                if value.startswith('docs/') and re.match(r'.+:\d+$',value):
                    path,num=value.rsplit(':',1);p=ROOT/path
                    check('reference_'+n+'_'+column+'_'+r.get('ID',r.get('Lot','')),p.exists() and 0<int(num)<=len(p.read_text(encoding='utf-8-sig').splitlines()),value)
        check('no_missing_path_marker_'+n,all('NON RETROUVÉ' not in str(r) for r in rows))
    regions=tables['REGIONAL_COVERAGE'];ent=tables['IMPERIAL_STATES_INVENTORY'];lots=tables['COMPLETED_LOTS'];issues=tables['REMAINING_WORK']
    statuses={'VALIDÉ EN JEU','INSTALLÉ — NON VALIDÉ','AUDITÉ — CONFORME','PARTIELLEMENT TRAITÉ','AUDITÉ — BLOQUÉ OU DIFFÉRÉ','NON AUDITÉ'}
    check('eleven_macro_groups',{r['Macro_region'] for r in regions}==set('ABCDEFGHIJK'))
    check('statuses_valid',all(r['Statut'] in statuses for r in regions))
    check('unique_sector_ids',len({r['ID'] for r in regions})==len(regions))
    check('unique_inventory_ids',len({r['ID'] for r in ent})==len(ent))
    check('map_numbering',set(r['Repere_carte'] for r in regions)==set(range(1,len(regions)+1)))
    labels=json.loads((OUT/'MAP_LABELS.json').read_text())
    check('map_csv_correspondence',{r['ID']:r['Repere_carte'] for r in regions}=={r['sector_id']:r['number'] for r in labels})
    inv=json.loads((OUT/'CURRENT_INVENTORY.json').read_text())
    owner={r['key'][0]:r['key'][2] for r in inv['owners']}
    for r in ent:
        if r['TAG_actuel']:check('country_definition_'+r['ID'],r['TAG_actuel'] in inv['countries'])
        check('RGB_actual_owner_'+r['ID'],all(owner.get(rgb)==r['TAG_actuel'] for rgb in r['RGB_identifies'].split(';') if rgb))
    check('chronological_dates',[r['Date_documentee'] for r in lots]==sorted(r['Date_documentee'] for r in lots))
    check('thirty_explicit_layers',sorted(r['Ordre_chaine_registre'] for r in lots if r['Ordre_chaine_registre'] is not None)==list(range(1,31)))
    check('R3_not_completed',not any('MAP2W/R3' in r['Lot'] for r in lots))
    for r in lots:
        if r['Statut']=='VALIDÉ EN JEU':
            path=r['Attestation'].rsplit(':',1)[0];j=json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
            check('manual_receipt_'+r['Lot'],j.get('status')=='PASS_RUNTIME_USER_VALIDATED' and not j.get('automated_engine_test',False))
    att=json.loads((OUT/'RUNTIME_USER_ATTESTATION.json').read_text())
    check('new_attestation_scoped',len(att['lots'])==4 and att['historical_boundary_certification'] is False and att['automated_engine_test'] is False)
    m=json.loads((OUT/'COVERAGE_METRICS.json').read_text())
    check('subsector_metrics',m['subsector_status_counts']==dict(collections.Counter(r['Statut'] for r in regions)))
    check('issue_metrics',m['issues_by_priority']==dict(collections.Counter(r['Priorite'] for r in issues)))
    check('no_fake_global_percentage',m['overall_percentage'] is None and m['closure_1_0'] is False)
    reg=json.loads((OUT/'REGISTRY_CHECKS.json').read_text());geo=json.loads((OUT/'EFFECTIVE_GEOMETRY_CHECKS.json').read_text())
    check('registry_current_573',len(reg)==573 and all(r['match'] and r['bitmap_cells']>0 for r in reg))
    check('final_geometry_326',len(geo)==326 and all(not r['bad_cells'] and r['owner_match'] for r in geo))
    supplemental=json.loads((OUT/'SUPPLEMENTAL_CHECKS.json').read_text())
    check('supplemental_all_pass',supplemental['passed']==supplemental['total'],supplemental['total'])
    protection=json.loads((OUT/'PROTECTION_CHECK.json').read_text())
    check('protected_runtime_unchanged',not protection['runtime_changes'],protection['runtime_changes'])
    check('git_untouched',protection['head_unchanged'] and protection['index_unchanged'])
    check('coverage_map_readable_dimensions',Image.open(OUT/'SERG_COVERAGE_MAP.png').size==(2160,1780))
    # Check older tests honestly: these are dated receipts, not reruns or PASS overrides.
    old=json.loads((ROOT/'docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/TESTS.json').read_text())
    check('old_failures_preserved',old['run']==260 and old['passed_count']==258 and old['all_passed'] is False)
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='VALIDATION.json'}
    result=dict(status='SERG_GLOBAL_CLOSURE_AUDIT_COMPLETE' if all(c['passed'] for c in checks) else 'AUDIT_DELIVERY_CHECK_FAILED',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c for c in checks if not c['passed']],checks=checks,output_hashes=files,engine_run_by_agent=False,territorial_changes=0,new_countries=0,git_writes=0)
    save('VALIDATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('checks','output_hashes')},ensure_ascii=False))
    if result['failed']:raise SystemExit(1)
if __name__=='__main__':run()
