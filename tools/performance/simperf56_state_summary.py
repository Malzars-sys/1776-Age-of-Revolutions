"""Compact, explicitly qualified evidence from the completed isolated trials."""
from pathlib import Path
from collections import Counter
import csv, hashlib, io, json, re

ROOT = Path(__file__).resolve().parents[2]
LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117')
REPORT = ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/STATE_INVESTIGATION_2026_11_17'

def read(name):
    return json.loads((LAB/name).read_text(encoding='utf-8-sig'))

def write(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')

rows = []
for trial in ('HMC1', 'HMM1', 'HMM2R', 'HMC2', 'ENG_ON2', 'ENG_OFF2', 'PROF_INIT'):
    result = read(trial+'_RESULTS.json')
    assert result['heartbeat_sequence_consecutive']
    assert result['executable_sha256'] == 'fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15'
    assert result['settings_sha256'] == '49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c'
    for w in result['heartbeat_windows']:
        if not (w['window'].startswith('FIRST_AFTER_LOAD_') or
                trial == 'PROF_INIT' and w['window'].startswith('JULY_')):
            continue
        rows.append(dict(trial=trial, window=w['window'], start_date=w['start']['date_raw'],
                         end_date=w['end']['date_raw'], start_utc=w['start']['utc'], end_utc=w['end']['utc'],
                         days=w['simulated_days'], seconds=w['wall_seconds'],
                         days_per_second=w['days_per_second'], cpu_machine_percent=w['cpu_machine_percent_approx'],
                         working_set_mib=w['working_set_mib_mean'], samples=w['cpu_samples'],
                         max_sample_gap_seconds=w['max_sample_gap_seconds'],
                         legacy_script_profiling=trial == 'PROF_INIT'))
assert len(rows) == 24
csv_text = io.StringIO(newline='')
out = csv.DictWriter(csv_text, fieldnames=list(rows[0]))
out.writeheader(); out.writerows(rows)
csv_path = REPORT/'MEASUREMENTS.csv'
if csv_path.exists():
    assert csv_path.read_bytes() == csv_text.getvalue().encode('utf-8')
else:
    csv_path.write_bytes(csv_text.getvalue().encode('utf-8'))

states = {label: read('STATE_'+label+'.json') for label in ('INITIAL', 'JULY', 'AUGUST', 'MATURE')}
compact = {}
initial = states['INITIAL']
for label, s in states.items():
    assert s['country']['totals']['population'] == s['states']['population']
    b0, b1 = initial['buildings']['by_id'], s['buildings']['by_id']
    shared = [i for i in b0.keys() & b1.keys()
              if (b0[i]['type'], b0[i]['state']) == (b1[i]['type'], b1[i]['state'])]
    pm_changes = sum(set(b0[i]['production_methods']) != set(b1[i]['production_methods']) for i in shared)
    a0, a1 = initial['ai']['by_country'], s['ai']['by_country']
    same_country = [i for i in a0.keys() & a1.keys()
                    if i in initial['country']['by_id'] and i in s['country']['by_id']
                    and initial['country']['by_id'][i]['tag'] == s['country']['by_id'][i]['tag']]
    compact[label] = dict(date=s['date'], path=s['path'], sha256=s['sha256'], bytes=s['bytes'],
        countries_with_population=s['country']['active_with_population'], country=s['country']['totals'],
        states=s['states'], pops=s['pops'], buildings=s['buildings']['totals'], ai=s['ai']['totals'],
        ai_goal_types=s['ai']['goal_types'], ai_strategy_types=s['ai']['strategy_types'],
        ai_strategy_changes_on_same_country=sum(a0[i]['strategies'] != a1[i]['strategies'] for i in same_country),
        same_country_count=len(same_country),
        pm_sets_changed_from_initial=pm_changes, same_building_id_type_state_count=len(shared),
        serialized_records={k:s[k]['records'] for k in ('market_manager','diplomatic_plays','war_manager',
            'military_formation_manager','new_combat_unit_manager','ship_manager','treaty_manager')},
        section_bytes={k:s['section_bytes'][k] for k in ('ai','tasks','market_manager','building_manager')})

cohorts = Counter()
for i, a in initial['ai']['by_country'].items():
    country = initial['country']['by_id'].get(i)
    cohorts[country['country_type'].strip('"') if country else 'not_in_populated_country_table'] += 1

profile_files = ['SCRIPT_PROFILE_INITIAL_PROF_INIT.txt', 'SCRIPT_PROFILE_JULY_PROF_INIT.txt']
profiles = []
for name in profile_files:
    p = LAB/name
    parsed = {}; row_types = Counter(); raw_rows = 0
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('#') or not line.strip(): continue
        m = re.fullmatch(r'(\S+) (.+):(\d+) ([\d.]+) (\d+)', line)
        assert m, repr(line)
        key = (m[1], m[2], int(m[3]))
        row_types[m[1]] += 1; raw_rows += 1
        # Several separately compiled expressions can share a source location.
        # Aggregate only for source-location comparison; retain the raw dump.
        row = parsed.setdefault(key, dict(type=m[1], file=m[2], line=int(m[3]), seconds=0.0, calls=0))
        row['seconds'] += float(m[4]); row['calls'] += int(m[5])
    profiles.append(parsed)
    summary = dict(file=name, sha256=hashlib.sha256(p.read_bytes()).hexdigest(), rows=raw_rows,
                   unique_source_locations=len(parsed), row_types=dict(row_types),
                   raw_row_seconds_sum_not_exclusive_cpu=sum(x['seconds'] for x in parsed.values()),
                   top=sorted(parsed.values(), key=lambda x:x['seconds'], reverse=True)[:12])
    compact['PROFILE_'+('INITIAL' if len(profiles)==1 else 'JULY')] = summary
first, second = profiles
missing = [list(k) for k in first.keys()-second.keys()]
decreases = [list(k) for k in first.keys() & second.keys()
             if second[k]['calls'] < first[k]['calls'] or second[k]['seconds'] < first[k]['seconds']]
deltas = [dict(**{k:v for k,v in second[key].items() if k not in ('seconds','calls')},
               seconds=second[key]['seconds']-first[key]['seconds'],
               calls=second[key]['calls']-first[key]['calls']) for key in first.keys() & second.keys()]
compact['SCRIPT_PROFILE_COMPARISON'] = dict(
    common_rows=len(first.keys() & second.keys()), missing_initial_rows=missing,
    decreasing_common_rows=decreases, cumulative_counts_supported=not missing and not decreases,
    top_deltas=sorted(deltas,key=lambda x:x['seconds'],reverse=True)[:12],
    caveat='Cumulative script VM records only; nesting and coverage incomplete. Not native CPU stacks or exclusive cost.')
compact['INITIAL_AI_COUNTRY_TYPES'] = dict(cohorts)
compact['MEASUREMENTS'] = rows
compact['AI_DIAGNOSTIC'] = read('AI_COMPARISON.json')
compact['QUALITY'] = dict(
    accepted_windows=24, clock_resolution_seconds=1, logical_processors=16,
    partial_first_day_excluded=True, no_fps_measurement=True,
    excluded='All intervals crossing ENG_ON2 March22 pause, PROF_INIT April3 or July1 pauses; incomplete final DAY in immutable raw PROF_INIT log; zero-DAY aborted attempts.',
    profiles='Legacy profiling off for the ENG_ON2/ENG_OFF2 first56 comparison, on throughout PROF_INIT January and July windows.',
    no_statistical_confidence_claim=True, ai_off_pair_count=1,
    baseline_variation='Old 93s, current HRE122-125s, later AI control149s. Compare contemporary controls, not different batches.',
    world_comparison='July and August are separate normal-runtime branches from S0; mature April1777 is the earlier MATURE1 branch. Not one deterministic longitudinal trajectory.',
    state_counter_caveats='POP objects are not persons; serialized records not active counts; failed AI counters not rates or CPU cost; country_goal entries not verified executable queues; datetimes and task cursors not proof of causality.')
write(LAB/'STATE_SYNTHESIS.json', compact)
write(REPORT/'SUMMARY.json', compact)
print(json.dumps({'measurements': len(rows), 'world_dates': {k:v['date'] for k,v in compact.items() if k in states},
                  'cohorts': dict(cohorts), 'script_profile_common_rows': len(first.keys() & second.keys()),
                  'script_profile_missing': len(missing), 'script_profile_decreases': len(decreases)}, indent=2))
