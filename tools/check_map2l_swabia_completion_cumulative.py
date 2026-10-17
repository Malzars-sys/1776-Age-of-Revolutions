"""Cumulative static suites; no automated engine test or Git mutation."""
import json
from concurrent.futures import ThreadPoolExecutor,as_completed
import check_map2l_swabia_finish_cumulative as previous
from map2l_swabia_completion import OUT

if __name__=='__main__':
    records=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending=[pool.submit(previous.run,name) for name in previous.SCRIPTS+['validate_map2l_swabia_completion.py']]
        for future in as_completed(pending):
            record=future.result();records.append(record);print(record['script'],record['exit_code'],record['seconds'],flush=True)
            if record['exit_code']:print(record['output'][-3000:],flush=True)
    (OUT/'CUMULATIVE_RUN.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
