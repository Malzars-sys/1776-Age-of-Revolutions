"""Analyze the completed profiling run without changing its raw evidence.

The bounded launcher stops its own test process after the requested stop file.
A final native log write may therefore be incomplete. Reject every malformed
DAY except the final, unterminated DAY line; preserve and hash the original.
"""
from pathlib import Path
import hashlib, json, shutil
from simperf56_analyze import analyze, game_date

LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117')
SOURCE = LAB/'runs/PROF_INIT_20261117T184238701Z'
DEST = LAB/'analysis/PROF_INIT'
assert not DEST.exists()
DEST.mkdir(parents=True)
(DEST/'logs').mkdir()
manifest = {'source': str(SOURCE), 'excluded_tail': [], 'files': {}}
for name in ('LAUNCH.json', 'OBSERVER.json', 'CONTINUOUS_CPU_RAM.csv'):
    shutil.copyfile(SOURCE/name, DEST/name)
for p in (SOURCE/'logs').glob('debug*.log'):
    raw = p.read_bytes()
    lines = raw.splitlines(keepends=True)
    kept = []
    for i, line in enumerate(lines):
        text = line.decode('utf-8-sig', errors='replace')
        if 'SIM56|DAY|date=' in text:
            date = text.split('SIM56|DAY|date=', 1)[1].strip()
            if game_date(date) is None:
                assert p.name == 'debug.log' and i == len(lines)-1
                assert not line.endswith((b'\r', b'\n'))
                manifest['excluded_tail'].append({'file': p.name, 'line': text})
                continue
        kept.append(line)
    (DEST/'logs'/p.name).write_bytes(b''.join(kept))
    manifest['files'][p.name] = {'source_sha256': hashlib.sha256(raw).hexdigest(),
                               'analysis_sha256': hashlib.sha256(b''.join(kept)).hexdigest()}
with (LAB/'PROF_INIT_ANALYSIS_INPUT.json').open('x', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
result = analyze(DEST)
assert result['heartbeat_sequence_consecutive']
result['raw_run'] = str(SOURCE)
result['analysis_input_manifest'] = str(LAB/'PROF_INIT_ANALYSIS_INPUT.json')
accepted = [r for r in result['heartbeat_windows']
            if r['window'].startswith(('FIRST_AFTER_LOAD_', 'JULY_'))]
assert len(accepted) == 6
result['accepted_windows'] = [r['window'] for r in accepted]
result['quality_note'] = ('Only first-after-load and July DAY windows accepted. '
    'April 3 and July 1 setup/save pauses invalidate crossing intervals. '
    'Legacy script profiling enabled throughout both accepted groups. '
    'Raw final unterminated DAY line excluded in a separate analysis copy only.')
with (LAB/'PROF_INIT_RESULTS.json').open('x', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(json.dumps({'days': result['daily_heartbeats'], 'accepted': [
    {k: r[k] for k in ('window', 'wall_seconds', 'days_per_second',
                      'cpu_machine_percent_approx', 'working_set_mib_mean')}
    for r in accepted]}, indent=2))
