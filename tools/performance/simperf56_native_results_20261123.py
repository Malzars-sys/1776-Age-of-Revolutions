"""Validate native timing and post-run evidence for the 1.15.2 trials."""
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import json
import re
import shutil

from simperf56_analyze import analyze, game_date
from simperf56_economic_goals_20261118 import goal_state
from simperf56_native_categories_20261123 import LAB, PREVIOUS, read, sha, write
from simperf56_save_state import records, sections


def queue_counts(save, country_span):
    """Report orders present on the snapshot date; completed orders are absent."""
    families = {'government_queue': Counter(), 'private_queue': Counter()}
    for _, country in records(save, country_span):
        for name, counts in families.items():
            for queue in country.children(name):
                for elements in queue.children('construction_elements'):
                    for order in elements.children():
                        kind = order.one('type')
                        if kind is not None:
                            counts[str(kind)] += 1
    return {name: dict(total=sum(counts.values()), by_type=dict(counts)) for name, counts in families.items()}


def collect(trial):
    plan = read(LAB/'PREPARATION.json')
    spec = plan['profiles'][trial]
    (run,) = (LAB/'runs').glob(trial+'_*')
    launch = read(run/'LAUNCH.json')
    end = read(run/'EXIT.json')
    assert launch['executable_sha256'] == plan['executable_sha256']
    assert sha(run/'SETTINGS.json') == spec['settings_sha256']
    assert sha(spec['seed_path']) == spec['common_save_sha256']
    assert sha(spec['native_define_file']) == spec['native_define_sha256']
    mods = [x['path'] for x in read(run/'CONTENT_LOAD.json')['enabledMods']]
    assert mods == spec['mods']

    automatic = spec.get('native_ui_autostart', False)
    evidence_name = '_WINDOW.json' if automatic else '_UNPAUSE.json'
    action = read(LAB/'evidence'/(trial+evidence_name))
    assert action['process_id'] == launch['process_id']
    assert action['secondary'].endswith('DISPLAY2') and action['client']['x'] < 0
    if not automatic:
        assert action['action'] == 'click'
    start = datetime.fromisoformat(launch['started_utc'] if automatic else action['utc'])
    stopped = datetime.fromisoformat(end['ended_utc'])
    witness_dir = LAB/'autosave_witnesses'/trial
    watcher = read(witness_dir/'WATCHER_READY.json')
    watcher_ready = datetime.fromisoformat(watcher['utc'])
    events = [json.loads(line) for line in (witness_dir/'FILE_EVENTS.jsonl').read_text(encoding='utf-8').splitlines()]
    observed = [tuple(map(int, e['game_date'].split('.')))[:3] for e in events
                if e['event'] == 'native_autosave_file_observed' and e['game_date']]
    assert not any((1776, 1, 2) <= d <= (1776, 2, 27) for d in observed)
    witnesses = [e for e in events if e['event'] == 'native_autosave_preserved'
                 and e['stable_copy_verified'] and tuple(map(int, e['game_date'].split('.')))[:3] == (1776, 4, 1)]
    assert witnesses, 'Missing verified April 1 autosave.'
    witness = witnesses[0]
    assert sha(witness['preserved']) == witness['sha256']

    input_dir = LAB/'analysis'/trial
    (input_dir/'logs').mkdir(parents=True)
    for name in ('LAUNCH.json', 'OBSERVER.json', 'CONTINUOUS_CPU_RAM.csv'):
        shutil.copyfile(run/name, input_dir/name)
    truncated = []
    for path in (run/'logs').glob('debug*.log'):
        raw = path.read_bytes()
        if not raw.endswith(b'\n'):
            prefix, sep, tail = raw.rpartition(b'\n')
            if b'SIM56|DAY|date=' in tail and not game_date(tail.decode('utf-8', errors='replace').split('SIM56|DAY|date=', 1)[1]):
                truncated.append(dict(file=path.name, line=tail.decode('utf-8', errors='replace')))
                raw = prefix + sep
        (input_dir/'logs'/path.name).write_bytes(raw)
    archive = LAB/'evidence'/(trial+'_NATIVE_LOG_ARCHIVE.log')
    if archive.is_file():
        shutil.copyfile(archive, input_dir/'logs/debug.99.log')
    result = analyze(input_dir)
    assert result['heartbeat_sequence_consecutive']
    windows = [w for w in result['heartbeat_windows'] if w['window'].startswith('FIRST_AFTER_LOAD_')]
    assert [w['simulated_days'] for w in windows] == [14, 28, 56]
    for window in windows:
        assert game_date(window['start']['date_raw']).isoformat() == '1776-01-02'
        assert start-timedelta(seconds=1) <= datetime.fromisoformat(window['start']['utc'])
        assert watcher_ready <= datetime.fromisoformat(window['start']['utc'])
        assert datetime.fromisoformat(window['end']['utc']) <= stopped

    save = Path(witness['preserved']).read_text(encoding='utf-8-sig')
    assert re.search(r'(?m)^speed=(\d+)', save)[1] == '4'
    controllers = goal_state(save)
    expected = read(PREVIOUS/'ECONOMIC_SOURCE_GOALS_20261118.json')['controllers']
    expected_enabled = spec.get('expected_enabled', 'yes')
    flags = Counter(c['enabled'] for c in controllers.values())
    assert controllers and flags == {expected_enabled: len(controllers)}, flags
    goal_counts = Counter()
    for controller in controllers.values(): goal_counts.update(controller['goals'])
    save_sections = sections(save)
    queues = queue_counts(save, save_sections['country_manager'])
    result.update(windows_14_28_56=windows, raw_run=str(run), excluded_log_tail=truncated,
                  native_disabled_define=spec['native_disabled_define'], native_override=spec.get('native_override', {}),
                  post_autosave=witness,
                  post_controllers=len(controllers), post_controller_flags=dict(flags), post_goals=dict(goal_counts),
                  post_missing_controllers=sorted(set(expected)-set(controllers)),
                  post_new_controllers=sorted(set(controllers)-set(expected)),
                  post_save_sections=sorted(save_sections), post_queue_counts=queues,
                  native_ui_autostart=automatic, input_timestamp=None if automatic else action['utc'],
                  initial_seed_verified=True,
                  native_switch_effect_requires_independent_evidence=True)
    write(LAB/(trial+'_RESULTS.json'), result)
    print(json.dumps(dict(trial=trial, post_controllers=len(controllers), post_date=witness['game_date'],
                          queues={name: counts['total'] for name, counts in queues.items()},
                          seconds=[w['wall_seconds'] for w in windows])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trial')
    parser.add_argument('--lab', type=Path, default=LAB)
    args = parser.parse_args()
    LAB = args.lab
    collect(args.trial)
