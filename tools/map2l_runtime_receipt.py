"""Attach a human test receipt without changing static checks or exit status."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/'docs/reports/map/MAP2L/RUNTIME_USER_VALIDATION.json'
LATER_RECEIPTS=[RECEIPT.parent/'RUNTIME_USER_VALIDATION_RHINE_SWABIA.json',RECEIPT.parent/'RUNTIME_USER_VALIDATION_SWABIA_FINISH.json',RECEIPT.parent/'RUNTIME_USER_VALIDATION_SWABIA_COMPLETION.json',RECEIPT.parent/'RUNTIME_USER_VALIDATION_PRUSSIAN_CORE.json']

def receipts():
    return [(path,json.loads(path.read_text(encoding='utf-8'))) for path in [RECEIPT]+LATER_RECEIPTS if path.exists()]

def annotate(report,lot):
    candidate=Path(lot)
    if candidate.is_absolute():candidate=candidate.relative_to(RECEIPT.parent)
    matched=[(path,r) for path,r in receipts() if candidate.as_posix() in r['lot_reports']]
    if not matched:return report
    path,receipt=matched[-1]
    report['runtime_status']=receipt['status']
    report['runtime_user_validation']={
        'receipt':path.relative_to(ROOT).as_posix(),
        'date':receipt['date'],'method':receipt['method'],
        'coverage':receipt['coverage'],
        'automated_engine_test':False,'historical_boundary_certification':False,
        'new_minden_sublot_included':False,
        'duration':receipt.get('duration','Not enumerated by user'),
        'static_results_unchanged':True,
        'legacy_engine_tested_field':'Automated assistant engine testing only; manual user testing is separately recorded here.'}
    return report

def apply_existing():
    names=list(dict.fromkeys(name for _,receipt in receipts() for name in receipt['lot_reports']))
    for name in names:
        path=RECEIPT.parent/name/'VALIDATION.json'
        report=json.loads(path.read_text(encoding='utf-8'))
        annotate(report,name)
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(name,report['runtime_status'],'static:',report['status'])

if __name__=='__main__':apply_existing()
