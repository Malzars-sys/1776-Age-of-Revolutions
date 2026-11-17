"""Consolidate existing UI captures; no process inspection or game input."""
from pathlib import Path
import csv
import json
import math

HERE = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def number(value):
    # The PowerShell sampler used the French locale. Fields are CSV-quoted.
    return float(value.replace(',', '.'))

def main():
    observations = {item['id']: item for item in read(HERE / 'FPS_OBSERVATIONS.json')}
    result = []
    for directory in sorted(HERE.glob('[AB][12]_*/measurements')):
        for meta_path in sorted(directory.glob('*_metadata.json')):
            meta = read(meta_path)
            with (directory / (meta['id'] + '_cpu.csv')).open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream))
            seconds = sum(number(row['interval_s']) for row in rows)
            cpu = 100 * sum(number(row['cpu_delta_ms']) for row in rows) / (1000 * seconds * meta['logical_processors'])
            assert seconds > 0 and math.isfinite(cpu)
            result.append(dict(meta, source=meta_path.relative_to(HERE).as_posix(),
                               cpu_machine_weighted_percent=cpu,
                               cpu_one_core_equivalent_percent=cpu*meta['logical_processors'],
                               fps=observations.get(meta['id']),
                               fps_is_approximate_visual_snapshot=True,
                               controlled='_fixed_' in meta['id']))
    # This regenerable summary never overwrites raw CSVs or metadata.
    (HERE / 'CAPTURE_SUMMARIES.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    controlled = [row for row in result if row['controlled']]
    for trial in ['A1', 'B1', 'B2', 'A2']:
        print(trial, [(row['phase'], row['category'], round(row['cpu_machine_weighted_percent'], 3), row['fps'])
                      for row in controlled if row['trial'] == trial])

if __name__ == '__main__':
    main()
