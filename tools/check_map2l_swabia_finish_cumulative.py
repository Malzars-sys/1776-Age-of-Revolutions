"""Read-only runtime QA, bounded parallel independent report processes."""
import os,subprocess,sys,json,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/MAP2L/SWABIA_FINISH'
SCRIPTS=['validate_map2l_belgium.py','validate_map2l_franconia.py','validate_map2l_rhine.py','validate_map2l_mainz.py','validate_map2l_mainz_estates.py','validate_map2l_mainz_completion.py','validate_map2l_milan.py','validate_map2l_franconia_continuation.py','validate_map2l_westphalia.py','validate_map2l_minden_ravensberg.py','validate_map2l_duchy_westphalia.py','validate_map2l_rhine_completion.py','validate_map2l_swabia.py','validate_map2l_swabia_continuation.py','validate_map2l_swabia_finish.py']

def run(name):
    start=time.monotonic();env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}
    result=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/name)],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    return dict(script=name,exit_code=result.returncode,seconds=round(time.monotonic()-start,2),output=result.stdout+result.stderr)

if __name__=='__main__':
    records=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending=[pool.submit(run,name) for name in SCRIPTS]
        for future in as_completed(pending):
            record=future.result();records.append(record);print(record['script'],record['exit_code'],record['seconds'],flush=True)
            if record['exit_code']:print(record['output'][-2500:],flush=True)
    (OUT/'CUMULATIVE_RUN.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
