"""MAP-1 read-only research intake and geographic reports, never runtime writes."""
from pathlib import Path
import csv, hashlib, json, zipfile, collections, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reports/map/MAP1'
INPUT = OUT / 'inputs'
ARCHIVE = Path('C:/Users/simeo/Downloads/MAP1_WORLD_1776_HANDOFF.zip')
GAME = Path('C:/Games/Victoria 3/game')
EXPECTED = 'e3911fd80a40c6b297a68f66e898d9b187863b64483a9608123606143ee2ea78'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def table(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def savecsv(name, rows, fields=None):
    rows = list(rows)
    with (OUT/name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fields or list(rows[0]), extrasaction='raise')
        w.writeheader(); w.writerows(rows)

def protected():
    folders = ['common', 'map_data', 'gfx', 'localization', 'events', '.metadata']
    return {p.relative_to(ROOT).as_posix():digest(p) for folder in folders
            for p in (ROOT/folder).rglob('*') if p.is_file()}

def intake():
    OUT.mkdir(parents=True, exist_ok=True)
    before = protected()
    (OUT/'MAP1_RUNTIME_BEFORE.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
    assert digest(GAME/'map_data/provinces.png') == EXPECTED, 'STOP: bitmap changed'
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.infolist()
        assert len({e.filename for e in entries}) == len(entries)
        for e in entries:
            target = (INPUT/e.filename).resolve()
            assert target.is_relative_to(INPUT.resolve()), 'ZIP path escape'
            assert not e.filename.startswith('/') and '\\' not in e.filename
            if not e.is_dir():
                target.parent.mkdir(parents=True, exist_ok=True)
                content = z.read(e)
                if target.exists(): assert target.read_bytes() == content, 'Existing input differs'
                else: target.write_bytes(content)
    original_checks = []
    manifest = table(INPUT/'map1_outputs/MAP1_INPUT_MANIFEST.csv')
    for r in manifest:
        p = INPUT/'regional_originals'/r['Filename']
        assert digest(p) == r['SHA256'] and p.stat().st_size == int(r['Bytes']), p
        original_checks.append(dict(r, Check='PASS'))
    assert len(original_checks)==36
    savecsv('MAP1_ORIGINAL_SHA256_CHECKS.csv', original_checks)
    for name in ['MAP_1776_BASELINE.csv','MAP_1776_9_REGIONS.csv','MAP_1776_KNOWN_ISSUES.csv']:
        a,b = INPUT/'map0_reference'/name, ROOT/'docs/reports/map'/name
        assert digest(a)==digest(b), 'STOP: MAP0 baseline changed: '+name
    rows = []
    for p in sorted(INPUT.rglob('*.csv')):
        raw=p.read_bytes(); data=table(p)
        with p.open(encoding='utf-8-sig', newline='') as f:
            parsed=list(csv.reader(f)); width=len(parsed[0])
        assert all(len(row)==width for row in parsed), 'Ragged CSV: '+str(p)
        rows.append(dict(File=p.relative_to(INPUT).as_posix(), Rows=len(data), Columns=width,
                         UTF8_BOM=raw.startswith(b'\xef\xbb\xbf'), Separator=',', SHA256=digest(p)))
    savecsv('MAP1_CSV_INTAKE.csv', rows)
    main=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_MASTER.csv')
    sources=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_SOURCES.csv')
    coverage=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_COVERAGE.csv')
    queue=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_MAPPING_QUEUE.csv')
    for records,key,n in [(main,'Change_ID',1005),(sources,'Source_ID',374),(queue,'Change_ID',410)]:
        assert len(records)==n and len({r[key] for r in records})==n
    print(json.dumps({'archive_entries':len(entries),'coverage_rows':len(coverage),
                      'master_fields':list(main[0]),'source_fields':list(sources[0]),
                      'coverage_fields':list(coverage[0]),'queue_first':queue[0],
                      'baseline_first':table(INPUT/'map0_reference/MAP_1776_BASELINE.csv')[0]},indent=2,ensure_ascii=False))
    assert before == protected(), 'Runtime changed'

if __name__=='__main__': intake()
