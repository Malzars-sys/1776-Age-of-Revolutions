"""Create one local launcher playset, with backup and exact membership checks.

Run only with the launcher closed. Does not change the selected playset,
content_load.json, existing playsets, cloud IDs or game saves.
"""
from pathlib import Path
import datetime
import hashlib
import json
import sqlite3
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT.parent.parent
DB = PROFILE / 'launcher-v2.sqlite'
PROTOTYPE = ROOT.parent / 'aor1776_hre_map_prototype'
NAME = '1776 — Test carte impériale'
OUT = ROOT / 'docs/reports/map/MAP2K/PROTOTYPES/hre_main_map'


def normalized(path):
    return str(Path(path).resolve()).replace('\\', '/').casefold()


def rows(connection, table):
    return [dict(r) for r in connection.execute('SELECT * FROM ' + table)]


def run(apply):
    required = ['.metadata/metadata.json', 'descriptor.mod',
                'gfx/FX/coloroverlay.fxh', 'gfx/FX/aor1776_hre_prototype.fxh',
                'gfx/map/map_modes/aor1776_hre_prototype.txt',
                'gfx/map/map_painting/aor1776_hre_mask.dds',
                'gfx/map/map_painting/aor1776_hre_sentinel.dds']
    source = OUT / 'mod'
    for relative in required:
        assert (PROTOTYPE / relative).is_file(), f'Missing deployed file: {relative}'
        assert (PROTOTYPE / relative).read_bytes() == (source / relative).read_bytes(), relative
    c = sqlite3.connect(DB if apply else DB.as_uri() + '?mode=ro', uri=not apply, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    assert c.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
    main = [r for r in rows(c, 'mods') if r['dirPath'] and normalized(r['dirPath']) == normalized(ROOT)]
    assert len(main) == 1 and main[0]['status'] == 'ready_to_play', 'Main local mod not unique/ready'
    matching = [r for r in rows(c, 'mods') if r['dirPath'] and normalized(r['dirPath']) == normalized(PROTOTYPE)]
    assert len(matching) <= 1
    existing = [r for r in rows(c, 'playsets') if r['name'] == NAME and not r['isRemoved']]
    assert len(existing) <= 1, 'Ambiguous existing playset'
    if apply:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup = OUT / 'launcher_backups' / f'{stamp}-{uuid.uuid4().hex[:8]}.sqlite'
        backup.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(backup) as b:
            c.backup(b)
        before_sets = rows(c, 'playsets')
        before_links = rows(c, 'playsets_mods')
        before_mods = rows(c, 'mods')
        before_values = rows(c, 'key_value_pairs')
        content_hash = hashlib.sha256((PROFILE / 'content_load.json').read_bytes()).hexdigest()
        now = int(time.time() * 1000)
        c.execute('BEGIN IMMEDIATE')
        try:
            if matching:
                mod_id = matching[0]['id']
                assert matching[0]['source'] == 'local' and matching[0]['status'] == 'ready_to_play'
            else:
                mod_id = str(uuid.uuid4())
                metadata = json.loads((PROTOTYPE / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))
                c.execute('''INSERT INTO mods
                  (id,name,displayName,dirPath,status,source,requiredVersion,tags,
                   createdDate,size,metadataId,metadataVersion,metadataStatus,isMetadataApplied,isNew)
                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (mod_id, PROTOTYPE.name, metadata['name'], str(PROTOTYPE), 'ready_to_play', 'local',
                   metadata['supported_game_version'], json.dumps(metadata['tags']), now // 1000,
                   sum(p.stat().st_size for p in PROTOTYPE.rglob('*') if p.is_file()),
                   metadata['id'], metadata['version'], 'applied', 0, 1))
            if existing:
                playset_id = existing[0]['id']
                actual = [tuple(r) for r in c.execute('SELECT modId,enabled,position FROM playsets_mods WHERE playsetId=? ORDER BY position', (playset_id,))]
                assert actual == [(main[0]['id'], 1, 0), (mod_id, 1, 1)], 'Existing same-named playset differs; no overwrite'
            else:
                playset_id = str(uuid.uuid4())
                c.execute('''INSERT INTO playsets
                  (id,name,isActive,loadOrder,createdOn,updatedOn,syncState,state,description)
                  VALUES (?,?,?,?,?,?,?,?,?)''',
                  (playset_id, NAME, 0, 'custom', now, now, 'NOT_ELIGIBLE', 'private',
                   'Mod principal local + prototype de carte impériale, sans autres mods.'))
                c.executemany('INSERT INTO playsets_mods (playsetId,modId,enabled,position) VALUES (?,?,1,?)',
                              [(playset_id, main[0]['id'], 0), (playset_id, mod_id, 1)])
                # Preserve the DLC choices of the currently selected playset.
                active = [r for r in before_sets if r['isActive']]
                if len(active) == 1:
                    c.execute('''INSERT INTO playsets_dlcs (playsetId,dlcId,enabled)
                      SELECT ?,dlcId,enabled FROM playsets_dlcs WHERE playsetId=?''',
                      (playset_id, active[0]['id']))
            after_sets = {r['id']: r for r in rows(c, 'playsets')}
            after_mods = {r['id']: r for r in rows(c, 'mods')}
            after_links = rows(c, 'playsets_mods')
            assert all(after_sets[r['id']] == r for r in before_sets), 'Existing playset changed'
            assert all(after_mods[r['id']] == r for r in before_mods), 'Existing mod changed'
            assert all(r in after_links for r in before_links), 'Existing membership changed'
            assert rows(c, 'key_value_pairs') == before_values, 'Launcher settings changed'
            assert not c.execute('PRAGMA foreign_key_check').fetchall()
            c.commit()
        except BaseException:
            c.rollback()
            raise
        assert hashlib.sha256((PROFILE / 'content_load.json').read_bytes()).hexdigest() == content_hash
        report = {'playset_name': NAME, 'playset_id': playset_id, 'backup': str(backup),
                  'old_playsets_preserved': True, 'selected_playset_unchanged': True,
                  'content_load_unchanged': True, 'cloud_publication': False}
    else:
        assert len(existing) == len(matching) == 1, 'Requested playset/prototype is missing'
        playset_id = existing[0]['id']
        report = {'playset_name': NAME, 'playset_id': playset_id}
    members = [dict(r) for r in c.execute('''SELECT m.id,m.displayName,m.dirPath,m.status,pm.enabled,pm.position
       FROM playsets_mods pm JOIN mods m ON m.id=pm.modId
       WHERE pm.playsetId=? ORDER BY pm.position''', (playset_id,))]
    assert len(members) == 2
    assert [normalized(r['dirPath']) for r in members] == [normalized(ROOT), normalized(PROTOTYPE)]
    assert all(r['enabled'] == 1 and r['status'] == 'ready_to_play' for r in members)
    assert [r['position'] for r in members] == [0, 1]
    assert c.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
    report.update(status='PASS_LOCAL_PLAYSET_CONFIGURATION', mods=members)
    if apply:
        (OUT / 'PLAYSET_CREATED.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    c.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    assert sys.argv[1:] in [['--apply'], ['--verify']], 'Use --apply or --verify'
    run(sys.argv[1:] == ['--apply'])
