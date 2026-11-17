"""Recalculate archived UI CPU observations from primary CSVs; never rewrite them."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import json

root = Path.cwd()
base = root / 'docs/reports/compatibility'
sources = {
    'AB': base / 'V1_15_ISSUE54_INTERACTIVE_2026_11_11/AUTHORIZED_RETRY_2026_11_12',
    'expressions': base / 'V1_15_ISSUE54_EXPRESSIONS_2026_11_12',
}
number = lambda s: float(s.replace(',', '.'))
result = {'utc': datetime.now(timezone.utc).isoformat(), 'new_measurements': False, 'sources': {}}
for family, folder in sources.items():
    fps = {item['id']: item for item in json.loads((folder / 'FPS_OBSERVATIONS.json').read_text(encoding='utf-8-sig'))}
    records = []
    for metadata in sorted(folder.glob('*/measurements/*_metadata.json')):
        item = json.loads(metadata.read_text(encoding='utf-8-sig'))
        if family == 'AB' and '_fixed_' not in item['id']:
            continue
        csv_path = metadata.with_name(item['id'] + '_cpu.csv')
        with csv_path.open(encoding='utf-8-sig', newline='') as stream:
            samples = list(csv.DictReader(stream))
        elapsed = sum(number(s['interval_s']) for s in samples)
        cpu = 100 * sum(number(s['cpu_delta_ms']) for s in samples) / (1000 * elapsed * item['logical_processors'])
        evidence = folder / item['ui_state_evidence']
        records.append(dict(item, cpu_recalculated_percent=cpu, raw_samples=len(samples),
                            raw_elapsed_seconds=elapsed, evidence_exists=evidence.is_file(),
                            fps_observation=fps.get(item['id']), metadata_source=str(metadata),
                            sample_count_matches=len(samples)==item['samples']))
    trials = sorted(p for p in folder.iterdir() if p.is_dir() and (p / 'LAUNCH.json').is_file())
    run_states = []
    for trial in trials:
        launch = json.loads((trial / 'LAUNCH.json').read_text(encoding='utf-8-sig'))
        run_states.append({'directory': trial.name, 'trial': launch['trial'],
                           'exit_record': (trial / 'EXIT.json').is_file(),
                           'cpu_captures': len(list(trial.glob('measurements/*_metadata.json')))})
    result['sources'][family] = {'records': records, 'runs': run_states}
with Path(__file__).with_name('ARCHIVE_MEASUREMENTS.json').open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
for family, data in result['sources'].items():
    print(family, 'captures:', len(data['records']), 'missing evidence:', sum(not r['evidence_exists'] for r in data['records']))
    for r in data['runs']:
        print(r)
