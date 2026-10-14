"""Attach a human test receipt without changing static checks or exit status."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/'docs/reports/map/MAP2L/RUNTIME_USER_VALIDATION.json'

def annotate(report,lot):
    if not RECEIPT.exists():return report
    receipt=json.loads(RECEIPT.read_text(encoding='utf-8'))
    if Path(lot).name not in receipt['lot_reports']:return report
    report['runtime_status']=receipt['status']
    report['runtime_user_validation']={
        'receipt':RECEIPT.relative_to(ROOT).as_posix(),
        'date':receipt['date'],'method':receipt['method'],
        'coverage':receipt['coverage'],
        'automated_engine_test':False,'historical_boundary_certification':False,
        'new_minden_sublot_included':False,
        'static_results_unchanged':True,
        'legacy_engine_tested_field':'Automated assistant engine testing only; manual user testing is separately recorded here.'}
    return report

def apply_existing():
    receipt=json.loads(RECEIPT.read_text(encoding='utf-8'))
    for name in receipt['lot_reports']:
        path=RECEIPT.parent/name/'VALIDATION.json'
        report=json.loads(path.read_text(encoding='utf-8'))
        annotate(report,name)
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(name,report['runtime_status'],'static:',report['status'])

if __name__=='__main__':apply_existing()
