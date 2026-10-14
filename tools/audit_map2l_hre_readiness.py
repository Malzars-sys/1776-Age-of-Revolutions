"""Read-only HRE readiness audit; write a report, never territorial assignments.

Keep MAP1 research status distinct from later applied MAP2K/MAP2L lots.
The old baseline and geographic research artifacts are not rewritten.
"""
from pathlib import Path
import collections
import csv
import json
import subprocess
import sys
import numpy as np
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2l_belgium import packed, sha
from map2l_hre_work import GIT
from map2l_registry import active_registry_path,approved_territorial_extensions,approved_territorial_migrations

ROOT = qa.ROOT
OUT = ROOT / 'docs/reports/map/MAP2L/READINESS'
INDEX_STATE = Path('C:/Users/simeo/AppData/Roaming/colgrep/indices/1776_Age_of_Revolutions_fork-9f9c61cb/state.json')
UNFINISHED = {
    'STATE_FRANCONIA', 'STATE_RHINELAND', 'STATE_RUHR', 'STATE_NORTH_RHINE',
    'STATE_WESTPHALIA', 'STATE_WURTTEMBERG', 'STATE_BADEN', 'STATE_BAVARIA',
    'STATE_ANHALT', 'STATE_BRUNSWICK', 'STATE_HESSE', 'STATE_SAXONY',
}
AGENT_REFS = [
    ('tools/map2l_hre_work.py', 31, 61, 'baseline capture, not an approved transfer'),
    ('tools/map2k_imperial_system.py', 14, 14, 'imperial member roster'),
    ('tools/map2k_imperial_system.py', 37, 43, 'reviewed registry guard'),
    ('tools/map2b_tables.mjs', 11, 19, 'previous southern European transfers, not new Franconia geometry'),
    ('tools/map2l_hre_work.py', 92, 92, 'research filter, not historic border proof'),
    ('docs/reports/map/MAP2L/GEOMETRY/franconia_before.json', 1, 59, 'current native province preview, not a candidate subdivision'),
    ('common/history/countries/lge - imperial estate.txt', 1, 19, 'existing Liege initialization'),
    ('common/history/countries/stm - imperial estate.txt', 1, 19, 'existing Stavelot initialization'),
    ('tools/tech_start_1776_implementation.py', 50, 61, 'unrelated technology graph debt edges; does not explain law setup'),
]


def runtime_hashes():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for folder in ('common', 'map_data', 'gui', 'gfx/FX', 'gfx/map', 'localization', 'events')
            for p in (ROOT / folder).rglob('*') if p.is_file()}


def audit():
    frozen = runtime_hashes()
    head = subprocess.check_output([GIT, 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    index_sha = sha(ROOT / '.git/index')
    inv = qa.inventory()
    base = json.loads((ROOT / 'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf-8'))
    ledger = json.loads(active_registry_path().read_text(encoding='utf-8'))
    bmp_colors = set(np.unique(packed(ROOT / 'map_data/provinces.png')).tolist())
    owner_rows = collections.defaultdict(list)
    for row in inv['owners']:
        owner_rows[row['key'][0]].append(row)
    checks = []

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))

    expected_count=315+len(approved_territorial_extensions())+sum(len(m['updated'])-len(m['previous']) for m in approved_territorial_migrations())
    check('Distinct registered RGBs', len({r['rgb'] for r in ledger}) == len(ledger) == expected_count)
    for row in ledger:
        rgb, state, holder = row['rgb'], row['state'], row['beneficiary']
        check('Registered territorial identity ' + rgb,
              int(rgb[1:], 16) in bmp_colors and inv['geometry'].get(rgb) == state
              and owner_rows[rgb] == [dict(key=[rgb, state, holder], count=1)], row)
    check('No new inventory errors since MAP2L baseline', inv['errors'] == base['inventory']['errors'])
    check('No new multiple assignments since MAP2L baseline', inv['duplicates'] == base['inventory']['duplicates'])
    check('Conserved raw and resolved demographic totals', inv['pops'] == base['inventory']['pops']
          and inv['resolved_demographics'] == base['inventory']['resolved_demographics'])
    check('Conserved written building levels', inv['building_levels_written'] == base['inventory']['building_levels_written'])
    check('Conserved military recruitment and units', inv['units'] == base['inventory']['units'])
    belgian = json.loads((ROOT / 'docs/reports/map/MAP2L/BELGIUM/VALIDATION.json').read_text(encoding='utf-8'))
    check('Belgian regression suite', all(c['passed'] for c in belgian['checks']), len(belgian['checks']))
    with (ROOT / 'docs/reports/map/MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv').open(encoding='utf-8-sig', newline='') as f:
        queued = [r for r in csv.DictReader(f) if r['State_ID'] in UNFINISHED]
    fields = ('Change_ID', 'State_ID', 'Historical_Polity_Name', 'De_Jure_Sovereign',
              'Effective_Controller', 'Historical_Conclusion', 'Mapping_Status',
              'Geographic_Correspondence', 'Unresolved_Uncertainty', 'Source_IDs')
    queue = [{k: r[k] for k in fields} for r in queued]
    regions = {}
    for sid in sorted(UNFINISHED):
        rows = [r for r in inv['owners'] if r['key'][1] == sid]
        regions[sid] = dict(owners=rows,
            populations=[r for r in inv['regional_pop'] if r['key'][0] == sid],
            native_geometry_RGBs=sorted(rgb for rgb, state in inv['geometry'].items() if state == sid))
    refs = []
    for rel, start, end, relevance in AGENT_REFS:
        lines = (ROOT / rel).read_text(encoding='utf-8-sig').splitlines()
        valid = 1 <= start <= end <= len(lines)
        check('Local agent reference bounds ' + rel + ':' + str(start), valid)
        refs.append(dict(path=rel, start=start, end=end, file_lines=len(lines), valid=valid,
                         relevance=relevance, excerpt=lines[start-1:end]))
    bad_ref = 'docs/reports/map/MAP1_CASE_DOSSIERS/R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0031.md'
    check('Incorrect local agent dossier path explicitly rejected', not (ROOT / bad_ref).exists())
    coverage = {}
    if INDEX_STATE.exists():
        indexed = json.loads(INDEX_STATE.read_text(encoding='utf-8'))['files']
        indexed_paths = {p.replace('\\', '/').casefold(): row for p, row in indexed.items()}
        for suffix in ('.csv', '.gui', '.asset', '.mod', '.geojson'):
            files = [p for p in ROOT.rglob('*' + suffix) if not any(x in p.parts for x in ('.git', 'node_modules', '.venv', '__pycache__'))]
            coverage[suffix] = dict(on_disk=len(files), indexed=sum(p.relative_to(ROOT).as_posix().casefold() in indexed_paths for p in files))
        coverage['key_files'] = {}
        for rel in ('tools/map2l_hre_work.py', 'tools/map2l_belgium.py',
                    'common/history/countries/lge - imperial estate.txt',
                    'common/history/countries/stm - imperial estate.txt'):
            entry = indexed_paths.get(rel.casefold())
            actual = (ROOT / rel).stat()
            coverage['key_files'][rel] = dict(indexed=entry is not None,
                stored_size=None if entry is None else entry['size'], actual_size=actual.st_size,
                stored_mtime_ns=None if entry is None else entry['mtime'], actual_mtime_ns=actual.st_mtime_ns)
    check('Audit leaves every runtime file unchanged', runtime_hashes() == frozen)
    check('Audit leaves HEAD and Git index unchanged',
          subprocess.check_output([GIT, 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == head
          and sha(ROOT / '.git/index') == index_sha)
    result = dict(status='PASS_STATIC_READINESS_BLOCKED' if all(c['passed'] for c in checks) else 'FAIL',
        historical_date='1776-01-01', runtime_changes_applied_this_pass=[],
        new_ready_territorial_assignments=[], checks=checks, imperial_registry_count=len(ledger),
        world_population=sum(r['count'] for r in inv['pops']),
        inherited_inventory_errors=inv['errors'], inherited_duplicate_RGBs=inv['duplicates'],
        previous_belgian_validation=belgian['status'], queued_research=queue, current_regions=regions,
        queue_warning='MAP1 status is historical research metadata, not a rollback of later MAP2K/MAP2L applied lots. Current owners above come from live files.',
        verified_local_agent_refs=refs, rejected_agent_path=bad_ref, index_coverage=coverage,
        engine_test_this_pass=False, engine_warning='Prior logs contain unavailable starting laws for LGE/STM and older electors. Static tests do not clear these warnings.',
        git_head=head, git_index_sha256=index_sha, protected_runtime_files=len(frozen))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'AUDIT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(result['status'], len(checks), 'checks;', len(queue), 'historical queue records;', len(inv['errors']), 'inherited inventory errors')
    print(json.dumps(coverage, ensure_ascii=False, indent=2))
    return 0 if result['status'].startswith('PASS') else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(audit())
