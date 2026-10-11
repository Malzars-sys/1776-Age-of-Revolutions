"""Read-only existing AST fixture suites, recorded under MAP-2D only."""
import json,contextlib,io
from map2d_work import OUT
import validate_diplomacy_ottoman_1776 as ottoman
import validate_regional_infrastructure_shortage as infrastructure

def run():
    result={'kind':'EXISTING_ACTUAL_SCRIPT_AST_FIXTURES_NOT_NATIVE_ENGINE','suites':{}}
    for name,fn in [('ottoman_journal_models',ottoman.model_tests),('regional_infrastructure_shortage_models',infrastructure.model_tests)]:
        log=io.StringIO()
        try:
            with contextlib.redirect_stdout(log):data=fn()
            result['suites'][name]={'status':'PASS','scenario_count':len(data) if isinstance(data,(dict,list)) else None,'output':log.getvalue()}
        except Exception as e:result['suites'][name]={'status':'FAIL','error':str(e),'output':log.getvalue()}
    result['legacy_baseline_guards']='Not rerun against old pre-MAP inventories: the independent MAP2D baseline validates authorized territorial deltas and preserved systems.'
    (OUT/'REGRESSION_TESTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return all(s['status']=='PASS' for s in result['suites'].values())
if __name__=='__main__':raise SystemExit(0 if run() else 1)
