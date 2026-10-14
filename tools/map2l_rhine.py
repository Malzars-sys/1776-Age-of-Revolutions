"""Capture the next HRE lot without changing gameplay or previous baselines.

Run `capture` once; `verify` checks that this preparation has not changed runtime.
No territorial attribution is inferred from province names or present owners.
"""
from pathlib import Path
import collections
import csv
import json
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
from map2l_belgium import packed, sha
from map2l_hre_work import GIT
from map2l_registry import active_registry_path

ROOT = qa.ROOT
OUT = ROOT / 'docs/reports/map/MAP2L/RHINE_CENTRAL'
REGIONS = {'STATE_RHINELAND', 'STATE_HESSE', 'STATE_BADEN', 'STATE_FRANCONIA'}


def fetch_source():
    # Observed link on the public Rumsey catalogue page, not a guessed image ID.
    url = 'https://www.davidrumsey.com/rumsey/Size2/D0049/00492030.jpg?userid=2&username=rumsey&resolution=2&servertype=JVA&cid=8&iid=RUMSEY&vcid=NA&usergroup=Rumsey3x&profileid=13'
    target = OUT / 'VAUGONDY_READING.jpg'
    assert OUT.exists() and not target.exists(), 'Preserve any previously fetched source'
    with urllib.request.urlopen(url, timeout=25) as response:
        data = response.read(30_000_001)
    assert len(data) <= 30_000_000
    import io
    image = Image.open(io.BytesIO(data))
    image.verify()
    target.write_bytes(data)
    size = Image.open(target).size
    source = dict(catalogue='https://www.davidrumsey.com/maps2294.html', catalogue_number='3353.062',
                  observed_image_url=url, sha256=sha(target), size=list(size),
                  title='Haut, Bas Rhin', map_date=1753,
                  status='FETCHED_FOR_VISUAL_REVIEW_NOT_APPROVED_FOR_TRACING',
                  warning='Image identity, resolution, alignment and political changes through 1776 must be checked')
    (OUT / 'VAUGONDY_SOURCE.json').write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(source, ensure_ascii=False))


def fetch_detail():
    url = 'https://upload.wikimedia.org/wikipedia/commons/2/20/Robert_de_Vaugondy_%2C_Didier._Carte_Des_Cercles_Du_Haut-_Et_Du_Bas-Rhin_%281753%29.jpeg'
    target = OUT / 'VAUGONDY_SANTINI_DETAIL.jpg'
    assert OUT.exists() and not target.exists(), 'Preserve previously fetched source'
    request = urllib.request.Request(url, headers={'User-Agent': 'HistoricalMapResearch/1.0'})
    with urllib.request.urlopen(request, timeout=25) as response:
        data = response.read(30_000_001)
    assert len(data) <= 30_000_000
    import io
    image = Image.open(io.BytesIO(data))
    image.verify()
    target.write_bytes(data)
    source = dict(observed_image_url=url, sha256=sha(target), size=list(Image.open(target).size),
                  catalogue='https://catalogue.bnf.fr/ark:/12148/cb41904894h',
                  hosting_page='https://commons.wikimedia.org/wiki/File:Robert_de_Vaugondy_,_Didier._Carte_Des_Cercles_Du_Haut-_Et_Du_Bas-Rhin_(1753).jpeg',
                  author='Didier Robert de Vaugondy', map_date=1753, edition_date=1777,
                  status='PRIMARY_MAP_REPRODUCTION_PENDING_ALIGNMENT_AND_1776_CHRONOLOGY',
                  license='Public domain mark',
                  warning='Different photographed exemplar than BnF scan; catalogue identifies edition, not custody of this photograph')
    (OUT / 'VAUGONDY_SANTINI_SOURCE.json').write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(source, ensure_ascii=False))


def read_detail():
    # Technical reading derivatives only: the downloaded source is immutable.
    im = Image.open(OUT / 'VAUGONDY_SANTINI_DETAIL.jpg').convert('RGB')
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
    for name, box in [('MAINZ_PALATINATE', (900, 1220, 1900, 1940)),
                      ('TRIER', (600, 1150, 1120, 1610))]:
        crop = im.crop(box)
        draw = ImageDraw.Draw(crop)
        for x in range((box[0]//100+1)*100, box[2], 100):
            draw.line((x-box[0], 0, x-box[0], crop.height), fill=(180, 40, 40))
            draw.text((x-box[0]+2, 2), str(x), font=font, fill='red', stroke_width=2, stroke_fill='white')
        for y in range((box[1]//100+1)*100, box[3], 100):
            draw.line((0, y-box[1], crop.width, y-box[1]), fill=(180, 40, 40))
            draw.text((2, y-box[1]+2), str(y), font=font, fill='red', stroke_width=2, stroke_fill='white')
        crop.save(OUT / ('READING_' + name + '.png'))


def fetch_bern():
    manifest_url = 'https://www.e-rara.ch/i3f/v20/29609156/manifest'
    target = OUT / 'DE_WIT_MAINZ_3500.jpg'
    assert not target.exists(), 'Preserve downloaded source'
    with urllib.request.urlopen(manifest_url, timeout=25) as response:
        manifest = json.load(response)
    resource = manifest['sequences'][0]['canvases'][0]['images'][0]['resource']
    service = resource['service']['@id']
    with urllib.request.urlopen(service + '/full/3500,/0/default.jpg', timeout=25) as response:
        data = response.read(30_000_001)
    assert len(data) <= 30_000_000
    import io
    image = Image.open(io.BytesIO(data))
    image.verify()
    target.write_bytes(data)
    (OUT / 'DE_WIT_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    source = dict(catalogue='https://www.e-rara.ch/bes_1/content/titleinfo/29609156', manifest=manifest_url,
                  service=service, requested_width=3500, image_sha256=sha(target),
                  size=list(Image.open(target).size), map_date='after 1688',
                  status='COMPARISON_PRIMARY_MAP_NOT_AUTOMATIC_1776_BOUNDARY',
                  warning='Older than target. Political changes must be checked before any attribution.')
    (OUT / 'DE_WIT_SOURCE.json').write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(source, ensure_ascii=False))


def capture():
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / 'BASELINE.json'
    assert not target.exists(), 'Never replace a lot baseline'
    bitmap = ROOT / 'docs/reports/map/MAP2L/FRANCONIA/provinces_candidate.png'
    assert sha(bitmap) == sha(ROOT / 'map_data/provinces.png'), 'Need current saved bitmap, not a new full-mod copy'
    inventory = qa.inventory()
    hashes = {}
    for folder in ['common', 'map_data', 'gui', 'gfx/FX', 'gfx/map', 'localization', 'events']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file():
                hashes[path.relative_to(ROOT).as_posix()] = sha(path)
    originals = {}
    for folder in ['common/history', 'map_data/state_regions']:
        for path in (ROOT / folder).rglob('*.txt'):
            raw = path.read_text(encoding='utf-8-sig')
            if any(sid in raw for sid in REGIONS):
                originals[path.relative_to(ROOT).as_posix()] = raw
    registry = active_registry_path()
    baseline = dict(status='PRE_IMPLEMENTATION_BASELINE', historical_date='1776-01-01',
                    inventory=inventory, hashes=hashes, originals=originals,
                    bitmap_backup=bitmap.relative_to(ROOT).as_posix(), bitmap_sha256=sha(bitmap),
                    registry=json.loads(registry.read_text()), registry_sha256=sha(registry),
                    git_head=subprocess.check_output([GIT, 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                    git_index_sha256=sha(ROOT / '.git/index'))
    target.write_text(json.dumps(baseline, ensure_ascii=False, indent=2), encoding='utf-8')
    image = packed(bitmap)
    scope = [r for r in inventory['owners'] if r['key'][1] in REGIONS]
    rows = []
    for row in scope:
        rgb, sid, owner = row['key']
        ys, xs = np.where(image == int(rgb[1:], 16))
        assert len(xs), rgb
        rows.append(dict(RGB=rgb, State_ID=sid, Current_Owner=owner,
                         Assignment_Count=row['count'], Pixels=len(xs),
                         X_min=int(xs.min()), X_max=int(xs.max()),
                         Y_min=int(ys.min()), Y_max=int(ys.max()),
                         Historical_Status='CURRENT_RUNTIME_NOT_HISTORICAL_PROOF'))
    with (OUT / 'CURRENT_PROVINCES.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (ROOT / 'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig', newline='') as handle:
        anchors = [{k: r[k] for k in ['State_ID', 'Hub_Type', 'Hub_Name', 'Locator_X', 'Locator_Y', 'Locator_Sampled_RGB']}
                   for r in csv.DictReader(handle) if r['State_ID'] in REGIONS]
    # Keep the legacy locator name visible as a rejected control, not as an owner decision.
    (OUT / 'NATIVE_ANCHORS.json').write_text(json.dumps(anchors, ensure_ascii=False, indent=2), encoding='utf-8')
    render(image, scope, anchors)
    print('Captured current post-Franconia baseline:', len(rows), 'province assignments;', len(originals), 'relevant source snapshots; no gameplay edit')


def render(image, rows, anchors, caption='Current runtime / avant lot : NOT historical boundaries', filename='BEFORE.png'):
    box = (4235, 815, 4395, 928)
    x0, y0, x1, y1 = box
    local = image[y0:y1, x0:x1]
    canvas = np.full((*local.shape, 3), 235, dtype=np.uint8)
    colors = {'KPF': (215, 170, 50), 'KMZ': (190, 58, 48), 'KTR': (160, 85, 115),
              'HES': (90, 150, 180), 'FRM': (225, 125, 60), 'BAD': (210, 195, 95),
              'BAV': (160, 160, 160)}
    for row in rows:
        rgb, sid, owner = row['key']
        canvas[local == int(rgb[1:], 16)] = colors.get(owner, (195, 205, 195))
    edge = np.zeros(local.shape, dtype=bool)
    edge[:, 1:] |= local[:, 1:] != local[:, :-1]
    edge[1:] |= local[1:] != local[:-1]
    canvas[edge] = (70, 70, 70)
    im = Image.fromarray(canvas).resize((local.shape[1]*8, local.shape[0]*8), Image.Resampling.NEAREST)
    result = Image.new('RGB', (im.width, im.height + 75), 'white')
    result.paste(im)
    draw = ImageDraw.Draw(result)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    for row in anchors:
        x, y = float(row['Locator_X']), float(row['Locator_Y'])
        if x0 <= x < x1 and y0 <= y < y1:
            label = 'Bamberg (legacy Coburg)' if row['State_ID']=='STATE_FRANCONIA' and row['Hub_Type']=='farm' else row['Hub_Name']
            point = ((x-x0)*8, (y-y0)*8)
            draw.ellipse((point[0]-2, point[1]-2, point[0]+2, point[1]+2), fill='black')
            draw.text(point, label, font=font, fill='black', stroke_width=2, stroke_fill='white')
    draw.text((10, im.height + 8), caption, font=font, fill='black')
    draw.text((10, im.height + 33), 'KPF gold | KMZ red | KTR purple | HES blue | FRM orange | BAD yellow | BAV gray', font=font, fill='black')
    result.save(OUT / filename)


def verify():
    baseline = json.loads((OUT / 'BASELINE.json').read_text())
    changed = [rel for rel, digest in baseline['hashes'].items() if sha(ROOT / rel) != digest]
    assert not changed, changed
    assert qa.inventory() == baseline['inventory'], 'Runtime inventory changed during preparation'
    assert sha(ROOT / baseline['bitmap_backup']) == baseline['bitmap_sha256']
    assert sha(active_registry_path()) == baseline['registry_sha256']
    assert subprocess.check_output([GIT, 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == baseline['git_head']
    assert sha(ROOT / '.git/index') == baseline['git_index_sha256']
    report = dict(status='PREPARATION_ONLY_NO_RUNTIME_CHANGE', engine_tested=False,
                  engine_test_policy='Deferred by user until all HRE territorial lots are finished',
                  protected_files=len(baseline['hashes']), registry_RGBs=len(baseline['registry']),
                  new_RGBs=0, ownership_transfers=0, runtime_changed_files=changed)
    (OUT / 'PREPARATION_VALIDATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    {'capture': capture, 'verify': verify, 'fetch-source': fetch_source, 'fetch-detail': fetch_detail, 'read-detail': read_detail, 'fetch-bern': fetch_bern}[sys.argv[1]]()
