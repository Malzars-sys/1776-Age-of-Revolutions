"""Read-only territorial research; the only permitted runtime edit is trade-centre GUI."""
import csv, hashlib, json, re, sys, urllib.request
from html import unescape
import map2m_border_work as previous
from PIL import Image, ImageDraw, ImageFont

ROOT = previous.ROOT
OUT = previous.BASE / 'R1'
GUI = 'gui/building_details_panel.gui'

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def capture():
    path = OUT / 'BASELINE.json'
    if path.exists():
        raise SystemExit('Baseline already exists; never overwrite it.')
    source = previous.BASE / 'PEENE/BASELINE.json'
    baseline = json.loads(source.read_text())
    assert all(previous.core.sha(ROOT / name) == digest for name, digest in baseline['hashes'].items())
    dump(path, baseline)
    (OUT / 'building_details_panel.before.gui').write_bytes((ROOT / GUI).read_bytes())
    print('Captured immutable runtime reference, including GUI before fix.')

def fetch(name, url):
    path = OUT / 'EVIDENCE' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'MAP-2M-R1 private historical research'})
        with urllib.request.urlopen(req, timeout=35) as response:
            content = response.read(35_000_001)
        if len(content) > 35_000_000:
            raise ValueError('Research size limit exceeded')
        path.write_bytes(content)
    print(name, len(path.read_bytes()), hashlib.sha256(path.read_bytes()).hexdigest())
    return path

def links(name):
    text = (OUT / 'EVIDENCE' / name).read_text(encoding='utf-8', errors='replace')
    for href, title in re.findall(r'<a[^>]+href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</a>', text, re.S):
        title = re.sub('<[^>]*>', ' ', title)
        if re.search('Tabula geographica|CIIIa[12]|[Mm]anifest|[Dd]igital|[Vv]iew|[Ss]can|wbc.poznan', title + href):
            print(unescape(href), unescape(title).strip()[:240])
    for tag in re.findall(r'<iframe[^>]+>', text):
        print(tag[:600])

def inspect(name):
    text = (OUT / 'EVIDENCE' / name).read_text(encoding='utf-8', errors='replace')
    for tag in ['script', 'style']:
        text = re.sub(fr'<{tag}\b.*?</{tag}>', '', text, flags=re.S)
    text = unescape(re.sub('<[^>]*>', '\n', text))
    lines = [re.sub(r'\s+', ' ', s).strip() for s in text.splitlines() if s.strip()]
    print('\n'.join(lines[-200:]))

def readings():
    cases = [
        ('HOMANN_NETZE_FULL.jpg', 'NETZE_INSET.png', (320, 330, 2140, 1570)),
        ('ANKLAM_1694_CIIIa1.jpg', 'ANKLAM_BRIDGE.png', (3100, 1680, 4310, 2590)),
    ]
    for name, target, box in cases:
        image = Image.open(OUT / 'EVIDENCE' / name).convert('RGB').crop(box)
        image.save(OUT / 'EVIDENCE' / target)
        print(target, box, image.size)

def diagnostics():
    """Document missing homologues without inventing a source-to-game fit."""
    records = [
        dict(id='CIIIa1', file='ANKLAM_1694_CIIIa1.jpg', url='https://geogreif.uni-greifswald.de/geogreif-content/jpegMaps/CIIIa1.jpg', catalogue='https://geogreif.uni-greifswald.de/search?coll_id=71Amt&map=overview&signatur=CI+', conception='1694, Peder Wising, catalogue', plate='manuscript, not an engraved plate', exemplar='1694 per catalogue', pre_1776=True, rights='Private research/teaching permitted; reproduction/publication requires written permission. DO NOT PUBLISH SCAN OR DERIVATIVES.'),
        dict(id='CIIIa2', file='ANKLAM_1694_CIIIa2.jpg', url='https://geogreif.uni-greifswald.de/geogreif-content/jpegMaps/CIIIa2.jpg', catalogue='https://geogreif.uni-greifswald.de/search?coll_id=71Amt&map=overview&signatur=CI+', conception='1694, Peder Wising, catalogue', plate='manuscript', exemplar='1694 per catalogue', pre_1776=True, rights='Same GeoGREIF restriction as CIIIa1; local research only.'),
        dict(id='HOMANN_RYHINER', file='HOMANN_NETZE_FULL.jpg', url='https://www.e-rara.ch/i3f/v30/29730682/full/5000,/0/default.jpg', catalogue='https://ryhiner.ub.unibe.ch/de/world/volume/17/image/14614', conception='Not established; represented Netze acquisition implies a post-1772 map state, not a certified printing date', plate='Homann heirs; J. Leitner cartouche; no inspected engraved year', exemplar='Catalogue: [nach 1730]; insufficient to certify pre-1776 printing', pre_1776=None, rights='Consult institution terms before publication.'),
        dict(id='KORNIK', file='KORNIK_CONTENT.html', url='https://platforma.bk.pan.pl/pl/bib_records/195777', catalogue='https://platforma.bk.pan.pl/pl/search_results/195777', conception='A.1752 occurs in atlas title, not proof of Netze plate date', plate='Plate 25 lists the desired title and inset, individual printing date not established', exemplar='1793, Norimbergae, catalogue; A V 018', pre_1776=False, rights='Catalogue only examined. Viewer exposes a multi-page DjVu atlas; not downloaded in full.'),
    ]
    for record in records:
        path = OUT / 'EVIDENCE' / record['file']
        record.update(sha256=previous.core.sha(path), bytes=path.stat().st_size)
    dump(OUT / 'SOURCES.json', records)
    rows = [
        ['PEENE','P1','Anklam Peene bridge','CIIIa1',3785,2010,30,'','','REJECTED_MISSING_GAME_HOMOLOGUE','SOURCE_ONLY','Bridge and divided river bed visible in source; absent from inspected native river raster. A town locator is not the bridge.'],
        ['PEENE','P2','Large Peene meander south of Pinnow','CIIIa2',3507,2733,40,'','','REJECTED_MISSING_GAME_HOMOLOGUE','SOURCE_ONLY','Meander visible; no matching Peene curve in native rivers.png.'],
        ['PEENE','P3','Peenestrom coastal connection','MAYER_1763_GREIFSWALD',664,432,8,4408,732,'OLD_UNVERIFIED_COAST_INTERPRETATION','NOT_CERTIFIED','Inherited manual coast hypothesis only; cadastral sheets do not include this estuary. Not a new independent validation point.'],
        ['PEENE','P4','Demmin confluence','MAYER_BSB_AFTER_1763',1642,2750,15,'','','REJECTED_MISSING_GAME_HOMOLOGUE','SOURCE_ONLY','Confluence readable in Mayer copy, but Peene/Trebel junction not independently identifiable in native raster.'],
        ['NETZE','N1','Deutsch Krone / Walcz town symbol','HOMANN_RYHINER',840,710,12,'','','REJECTED_TOWN_ONLY','SOURCE_ONLY','Town symbol readable; no independently verified native physical point at Walcz.'],
        ['NETZE','N2','Schneidemuhl / Pila town symbol','HOMANN_RYHINER',965,840,12,'','','REJECTED_TOWN_ONLY','SOURCE_ONLY','Previous hypotheses differ by 9.50 game pixels; source icon does not select a unique game province.'],
        ['NETZE','N3','Bromberg town / canal context','HOMANN_RYHINER',1720,950,12,'','','REJECTED_TOWN_ONLY','SOURCE_ONLY','Canal and town improve source context; farm named Bromberg is not a verified physical centre.'],
        ['NETZE','N4','Inowroclaw town symbol','HOMANN_RYHINER',1950,1165,12,'','','REJECTED_TOWN_ONLY','SOURCE_ONLY','Southern district is now visible, but town centre not verified in bitmap and printing date unresolved.'],
        ['NETZE','N5','Uscie: Gwda / Notec junction','HOMANN_RYHINER',950,918,15,'','','REJECTED_MISSING_GAME_HOMOLOGUE','SOURCE_ONLY','Confluence identifiable on source; Gwda tributary absent from inspected native hydrography.'],
        ['NETZE','N6','Vistula bend near Fordon','HOMANN_RYHINER',1790,927,15,'','','UNRESOLVED_COARSE_BEND','RESERVE_NOT_VALIDATED','Broad bend exists in game but cannot identify the precise same point uniquely; not silently promoted to control.'],
    ]
    fields = ['Sector','Point_ID','Feature','Source_ID','Source_X','Source_Y','Manual_reading_uncertainty_source_px','Game_X','Game_Y','Status','Role','Reason']
    for sector in ['PEENE','NETZE']:
        folder = OUT / sector
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / 'HOMOLOGUES.csv').open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f); writer.writerow(fields); writer.writerows(r for r in rows if r[0] == sector)
        model = json.loads((previous.BASE / sector / 'CANDIDATE_MODEL.json').read_text())
        dump(folder / 'CALIBRATION.json', dict(status='NO_JUSTIFIED_NEW_FIT', accepted_game_homologues=0, independent_validation_points=0, independent_mean_error_px=None, independent_max_error_px=None, geometry_complete=False, historical_attribution_complete=False, previous_diagnostics=model['diagnostics'], note='Old numerical discrepancies are preserved, not recertified as independent positional errors. No fit has been rerun from the same unverified points.'))
        with (previous.BASE / sector / 'CANDIDATE_CELLS.csv').open(encoding='utf-8-sig') as f:
            candidates = list(csv.DictReader(f))
        with (folder / 'CELL_CLASSIFICATION.csv').open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['X','Y','RGB','State_ID','Current_owner','Hypothetical_owner','Class','Applied','Reason'])
            writer.writeheader()
            for row in candidates:
                writer.writerow(dict(X=row['X'],Y=row['Y'],RGB=row['RGB'],State_ID=row['State_ID'],Current_owner=row['Before'],Hypothetical_owner=row['Proposed'],Class='UNCERTAIN',Applied=False,Reason='No independently verified source-to-game transform; proposals unchanged.'))
        dump(folder / 'SUMMARY.json', dict(certain_transfer_cells=0, uncertain_candidate_cells=len(candidates), applied_cells=0, new_RGBs=0, unresolved_extent='No invented exhaustive pixel list outside previous hypothesis.', variant_cells_status='No new physically justified transformations available; no claimed certain subset or new numeric variant mask.'))
    reference = {str(path.relative_to(ROOT)):previous.core.sha(path) for sector in ['PEENE','NETZE'] for path in [previous.BASE/sector/'CANDIDATE_CELLS.csv',previous.BASE/sector/'CANDIDATE_MODEL.json']}
    reference_path = OUT / 'HYPOTHESES_REFERENCE.json'
    if reference_path.exists():
        assert json.loads(reference_path.read_text()) == reference, 'Initial hypotheses must not change.'
    else:
        dump(reference_path, reference)
    figures(rows)
    print('Source tables, calibration gates, 79/162 immutable uncertain candidates, and comparison figures generated. Zero applied.')

def figures(rows):
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
    small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)
    for sector, box, crop in [('PEENE',(4372,711,4442,775),'ANKLAM_BRIDGE.png'),('NETZE',(4435,740,4550,812),'NETZE_INSET.png')]:
        canvas = Image.new('RGB',(1600,1150),'white'); d = ImageDraw.Draw(canvas)
        d.text((20,12),f'{sector} R1 — sources et jeu : juxtaposition, PAS un recalage validé',font=font,fill='black')
        source = Image.open(OUT/'EVIDENCE'/crop).convert('RGB'); source.thumbnail((760,540))
        canvas.paste(source,(20,55)); d.text((20,605),'Nouveaux détails historiques — position native non validée',font=small,fill='black')
        if sector=='PEENE':
            d.text((20,635),'GeoGREIF : recherche locale ; ne pas publier ce scan ni ce dérivé.',font=small,fill='#a00000')
        rivers = Image.open(previous.BASE/sector/'NATIVE_RIVERS.png').convert('RGB'); rivers.thumbnail((760,540))
        canvas.paste(rivers,(820,55)); d.text((820,605),'Hydrographie native : repères locaux manquants ou trop grossiers',font=small,fill='black')
        game = Image.open(previous.BASE/sector/'BEFORE_AFTER.png').convert('RGB')
        width = game.width//3
        panel = game.crop((width,32,width*2,game.height)); panel.thumbnail((760,400))
        canvas.paste(panel,(20,690))
        d.text((820,700),'Violet : hypothèse initiale NON APPLIQUÉE.',font=font,fill='#7b268a')
        d.text((820,745),'Repères homologues natifs acceptés : 0',font=font,fill='black')
        d.text((820,785),'Contrôles indépendants nouveaux : 0',font=font,fill='black')
        d.text((820,825),'Erreur indépendante : NON MESURABLE',font=font,fill='black')
        d.text((820,865),'Aucune transformation supplémentaire forcée.',font=font,fill='black')
        d.text((820,905),'Frontières et données de départ inchangées.',font=font,fill='black')
        d.text((20,1115),f'Fenêtre du jeu X/Y : {box} ; voir HOMOLOGUES.csv pour les lectures source.',font=small,fill='black')
        canvas.save(OUT/sector/'COMPARISON.png')

if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'capture': capture()
    elif action == 'fetch': fetch(sys.argv[2], sys.argv[3])
    elif action == 'links': links(sys.argv[2])
    elif action == 'inspect': inspect(sys.argv[2])
    elif action == 'readings': readings()
    elif action == 'diagnostics': diagnostics()
    else: raise SystemExit('Unknown action')
