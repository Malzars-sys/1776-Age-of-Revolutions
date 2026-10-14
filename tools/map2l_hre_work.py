"""Immutable starting point for the detailed HRE territorial rework.

Generated audit/evidence only. No runtime, launcher, save, or Git mutations.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import validate_map2a as qa
from map2c_work import source_bitmap

ROOT = qa.ROOT
OUT = ROOT / 'docs/reports/map/MAP2L'
GIT = 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture():
    target = OUT / 'BASELINE.json'
    assert not target.exists(), 'Never overwrite a captured baseline'
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = qa.inventory()
    registry_path = ROOT / 'docs/reports/map/MAP2K/IMPERIAL_DE_JURE_REGISTRY.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    originals = {}
    folders = ['common/history', 'common/country_definitions', 'common/dynamic_country_names',
               'common/scripted_effects', 'common/scripted_triggers', 'common/journal_entries',
               'common/on_actions', 'map_data/state_regions']
    for folder in folders:
        for path in (ROOT / folder).rglob('*.txt'):
            originals[path.relative_to(ROOT).as_posix()] = path.read_text(encoding='utf-8-sig')
    frozen = {}
    for folder in ['common', 'map_data', 'gui', 'gfx/FX', 'gfx/map', 'localization']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file():
                frozen[path.relative_to(ROOT).as_posix()] = sha(path)
    bitmap = source_bitmap()
    bitmap_backup = OUT / 'SOURCE/provinces_before.png'
    bitmap_backup.parent.mkdir(parents=True, exist_ok=True)
    assert not bitmap_backup.exists()
    shutil.copyfile(bitmap, bitmap_backup)
    assert sha(bitmap_backup) == sha(bitmap)
    baseline = dict(historical_date='1776-01-01', scope='Holy Roman Empire only',
                    user_authorized='Redraw provinces for additional small states and enclaves',
                    inventory=inventory, originals=originals, hashes=frozen,
                    de_jure_registry=registry, registry_sha256=sha(registry_path),
                    bitmap_sha256=sha(bitmap), bitmap_backup=bitmap_backup.relative_to(ROOT).as_posix(),
                    git_head=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                    git_index_sha256=sha(ROOT/'.git/index'))
    target.write_text(json.dumps(baseline, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(status='BASELINE_CAPTURED', protected_files=len(frozen),
                         source_files=len(originals), imperial_RGBs=len(registry),
                         bitmap_backup=baseline['bitmap_backup']), ensure_ascii=False))


def fetch_cliopatria():
    """Download the researchers' public vector dataset; not a gameplay authority."""
    assert (OUT / 'BASELINE.json').exists()
    evidence = OUT / 'EVIDENCE'
    evidence.mkdir(exist_ok=True)
    path = evidence / 'cliopatria.geojson.zip'
    url = 'https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/main/cliopatria.geojson.zip'
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read(150_000_001)
        assert len(data) <= 150_000_000, 'Dataset unexpectedly large'
        with zipfile.ZipFile(__import__('io').BytesIO(data)) as z:
            members = [n for n in z.namelist() if n.casefold().endswith('.geojson')]
            assert len(members) == 1, f'Expected one GeoJSON, got {members}'
        path.write_bytes(data)
    with zipfile.ZipFile(path) as z:
        members = [n for n in z.namelist() if n.casefold().endswith('.geojson')]
        assert len(members) == 1
        obj = json.loads(z.read(members[0]))
    features = obj['features']
    print('Features:', len(features), 'Sample properties:', features[0]['properties'])
    candidates = []
    for feature in features:
        p = feature['properties']
        start, end = p.get('FromYear'), p.get('ToYear')
        if start is not None and end is not None and int(start) <= 1776 <= int(end):
            # Bounding box / affiliation is reviewed before any territorial edit.
            if 'Holy Roman Empire' in str(p) or any(word.casefold() in str(p).casefold()
                    for word in ['Bavaria','Palatinate','Ansbach','Bayreuth','Würzburg','Bamberg','Nuremberg','Mainz','Trier','Cologne','Münster','Salzburg']):
                candidates.append(feature)
    subset = evidence / 'cliopatria_hre_1776_candidates.geojson'
    subset.write_text(json.dumps({'type':'FeatureCollection','features':candidates},ensure_ascii=False), encoding='utf-8')
    (evidence/'CLIopatria_SOURCE.json').write_text(json.dumps(dict(url=url,sha256=sha(path),
         features=len(features),candidates=len(candidates),
         status='RESEARCH_INPUT_NOT_VERIFIED_FOR_GAMEPLAY',
         warning='Year bounds, polity level, source maps, coverage and geometric alignment need review.'),indent=2),encoding='utf-8')
    print('1776 candidates:', len(candidates))
    for feature in candidates:
        print(json.dumps(feature['properties'],ensure_ascii=False))


def fetch_bsb():
    evidence = OUT / 'EVIDENCE'
    evidence.mkdir(exist_ok=True)
    url='https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb00090735/manifest'
    path=evidence/'bsb00090735_manifest.json'
    if not path.exists():
        with urllib.request.urlopen(url,timeout=30) as response:
            data=response.read()
        json.loads(data)
        path.write_bytes(data)
    obj=json.loads(path.read_bytes())
    canvases=obj['sequences'][0]['canvases']
    for number, canvas in enumerate(canvases,1):
        image=canvas['images'][0]['resource']
        service=image['service']['@id']
        preview_url=service+'/full/2400,/0/default.jpg'
        target=evidence/f'bsb00090735_{number:04d}_2400.jpg'
        if not target.exists():
            with urllib.request.urlopen(preview_url,timeout=30) as response:
                target.write_bytes(response.read())
        print(number,canvas['label'],image['width'],image['height'],str(target),sha(target))
    (evidence/'BSB_SOURCE.json').write_text(json.dumps(dict(manifest=url,
        source_date='1743 [published after 1764]',
        institution='Bayerische Staatsbibliothek',public_domain='PDM per bavarikon record',
        status='SOURCE_MAP_NOT_YET_ALIGNED_OR_CORROBORATED_FOR_1776'),indent=2),encoding='utf-8')


def fetch_comparison_svg():
    # Reference only, never copy 1789 boundaries to the 1776 runtime blindly.
    evidence=OUT/'EVIDENCE'
    evidence.mkdir(exist_ok=True)
    url='https://upload.wikimedia.org/wikipedia/commons/e/ee/Holy_Roman_Empire_1789.svg'
    target=evidence/'Holy_Roman_Empire_1789_comparison.svg'
    if not target.exists():
        request=urllib.request.Request(url,headers={'User-Agent':'HistoricalMapResearch/1.0 (local Victoria 3 mod research; public source comparison)'})
        with urllib.request.urlopen(request,timeout=30) as response:
            target.write_bytes(response.read())
    import xml.etree.ElementTree as ET
    obj=ET.fromstring(target.read_bytes())
    inkscape='{http://www.inkscape.org/namespaces/inkscape}'
    labels=[(n.tag.rsplit('}',1)[-1],n.attrib.get('id'),n.attrib.get(inkscape+'label'))
            for n in obj.iter() if n.attrib.get(inkscape+'label')]
    print('Bytes',target.stat().st_size,'labels',len(labels))
    print(json.dumps(labels[:90],ensure_ascii=False))
    (evidence/'COMPARISON_SVG_SOURCE.json').write_text(json.dumps(dict(url=url,
        page='https://commons.wikimedia.org/wiki/File:Holy_Roman_Empire_1789.svg',
        sha256=sha(target),authors=['Trasamundo','ziegelbrenner','Rosenzweig'],
        license='CC BY-SA 3.0',historical_date=1789,
        use='Comparison/inventory only; not yet a source for runtime tracing',
        warning='1777 Palatinate/Bavaria union and 1779 Innviertel changes must not be back-projected'),indent=2),encoding='utf-8')


def preview_region(name, regions):
    import numpy as np
    from PIL import Image,ImageDraw,ImageFont
    baseline=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    owned=[r for r in baseline['inventory']['owners'] if r['key'][1] in regions]
    bitmap=Image.open(OUT/'SOURCE/provinces_before.png').convert('RGB')
    colors=np.array(bitmap,dtype=np.uint32)
    packed=(colors[:,:,0]<<16)|(colors[:,:,1]<<8)|colors[:,:,2]
    wanted=[int(r['key'][0][1:],16) for r in owned]
    selected=np.isin(packed,wanted)
    ys,xs=np.nonzero(selected)
    box=(int(xs.min())-12,int(ys.min())-12,int(xs.max())+13,int(ys.max())+13)
    x0,y0,x1,y1=box
    local=packed[y0:y1,x0:x1]
    shade=np.full((*local.shape,3),225,dtype=np.uint8)
    palette=[(158,204,241),(227,187,243),(247,190,124),(201,225,149),(252,232,134),(247,175,185),(156,222,202),(194,194,246)]
    names={}
    for number,r in enumerate(sorted(owned,key=lambda r:r['key'][0]),1):
        color=int(r['key'][0][1:],16)
        shade[local==color]=palette[(number-1)%len(palette)]
        ly,lx=np.nonzero(local==color)
        names[number]=(r['key'][0],r['key'][2],float(lx.mean()),float(ly.mean()))
    edge=np.zeros(local.shape,dtype=bool)
    edge[:,1:]|=local[:,1:]!=local[:,:-1]
    edge[1:,:]|=local[1:,:]!=local[:-1,:]
    shade[edge]=[100,100,100]
    scale=10
    preview=Image.fromarray(shade).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(preview.width,preview.height+len(names)*24+60),'white')
    canvas.paste(preview)
    draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    for number,(rgb,owner,x,y) in names.items():
        draw.text((x*scale,y*scale),str(number),fill='black',font=font,stroke_width=2,stroke_fill='white')
        draw.text((10,preview.height+10+(number-1)*24),f'{number}: {rgb} — {owner}',font=font,fill='black')
    folder=OUT/'GEOMETRY'
    folder.mkdir(exist_ok=True)
    canvas.save(folder/f'{name}_before.png')
    (folder/f'{name}_before.json').write_text(json.dumps(dict(crop=box,scale=scale,labels=names),indent=2),encoding='utf-8')
    print('Native crop',box,'provinces',len(owned))


def preview_franken():
    from PIL import Image
    preview_region('franconia', ['STATE_FRANCONIA'])
    folder=OUT/'GEOMETRY'
    # Reading crops only; no changes to the source map or gameplay bitmap.
    historical=Image.open(OUT/'EVIDENCE/bsb00090735_0001_2400.jpg')
    historical.crop((200,950,2250,2750)).save(folder/'franconia_historical_detail.jpg')
    print('Historical source size',historical.size)


def belgium_scope():
    """Separate user-approved scope from the immutable original baseline."""
    baseline=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    regions=['STATE_FLANDERS','STATE_WALLONIA']
    rows=[r for r in baseline['inventory']['owners'] if r['key'][1] in regions]
    registered={r['rgb']:r for r in baseline['de_jure_registry']}
    assert len(rows)==14 and all(r['key'][2]=='BEO' for r in rows)
    assert all(r['key'][0] in registered for r in rows)
    report=dict(historical_date='1776-01-01',scope_confirmation='Current Belgian imperial territories are expressly included by the user.',
        tiny_enclave_policy='Keep geographical proportions. Abstract sub-pixel enclaves in neighbouring territory; never inflate their size.',
        territories_to_review=['Austrian Netherlands','Prince-Bishopric of Liège','Imperial Abbey of Stavelot-Malmedy'],
        disputed_separate_review=['Duchy of Bouillon and French-protected/claimed enclaves; no automatic incorporation by modern border'],
        current_native_provinces=[dict(rgb=r['key'][0],state=r['key'][1],owner=r['key'][2],
            current_de_jure_beneficiary=registered[r['key'][0]]['beneficiary']) for r in rows],
        diagnosis='Already in imperial mask, but all fourteen provinces assigned to BEO. Mask membership is NOT proof that the local sovereign or border is correct.',
        implementation_status='SCOPE_AND_BASELINE_AUDITED; territory splits and new polities not yet applied',
        sources=[dict(url='https://opac.kbr.be/BIBFEDERALE/doc/SYRACUSE/16992733/carte-de-cabinet-des-pays-bas-autrichiens-levee-a-l-initiative-du-comte-de-ferraris?_lg=fr-BE',
                      institution='KBR',title='Carte de cabinet des Pays-Bas autrichiens',date='1771-1778'),
                 dict(url='https://geoportail.wallonie.be/catalogue/b8b9e555-a4d1-49bf-940d-31bbbf7613fc.html',
                      institution='Service public de Wallonie',title='Cartes de Ferraris (1770-1778)',
                      limitations='Georeferenced raster; lacks Bouillon and some French enclaves; topography alone does not settle disputed sovereignty')])
    (OUT/'BELGIUM_SCOPE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    preview_region('belgium',regions)
    print(json.dumps(dict(provinces=len(rows),already_registered=len(rows),new_runtime_edits=0),ensure_ascii=False))


def fetch_endres():
    target=OUT/'EVIDENCE/reichskreis1_endres_2003.pdf'
    url='https://www.hdbg.de/basis/pdfs/downloads/reichskreis1.pdf'
    if not target.exists():
        with urllib.request.urlopen(url,timeout=30) as response:
            data=response.read()
        assert data.startswith(b'%PDF-')
        target.write_bytes(data)
    print(str(target),sha(target))


def fetch_belgium_maps():
    evidence=OUT/'EVIDENCE'
    for name in ['1789_0160c_v2','1789_0160b2']:
        url=f'https://connaitrelawallonie.wallonie.be/sites/default/files/maps/{name}.jpg'
        path=evidence/(name+'.jpg')
        if not path.exists():
            with urllib.request.urlopen(url,timeout=30) as response:
                path.write_bytes(response.read())
        from PIL import Image
        print(name,Image.open(path).size,sha(path))
    url='https://geoservices.wallonie.be/arcgis/rest/services/CARTES_ANCIENNES/FERRARIS/MapServer?f=pjson'
    with urllib.request.urlopen(url,timeout=30) as response:
        data=response.read()
    obj=json.loads(data)
    (evidence/'FERRARIS_SERVICE.json').write_bytes(data)
    print('Ferraris',obj.get('spatialReference'),obj.get('fullExtent'),obj.get('copyrightText'))
    from urllib.parse import urlencode
    for name,bbox in [('liege','5.0,50.3,6.2,50.95'),('stavelot','5.55,50.2,6.3,50.6')]:
        params=dict(bbox=bbox,bboxSR=4326,imageSR=4326,size='2048,1600',format='png32',transparent='false',f='image')
        url='https://geoservices.wallonie.be/arcgis/rest/services/CARTES_ANCIENNES/FERRARIS/MapServer/export?'+urlencode(params)
        target=evidence/f'ferraris_{name}_1777.png'
        if not target.exists():
            with urllib.request.urlopen(url,timeout=30) as response:
                data=response.read()
            assert data.startswith(b'\x89PNG'),data[:200]
            target.write_bytes(data)
        (evidence/f'FERRARIS_{name}_SOURCE.json').write_text(json.dumps(dict(url=url,requested_bbox_wgs84=bbox,
            sha256=sha(target),note='Service adjusts extent to requested image aspect ratio; use export JSON extent before georeferencing pixels.'),indent=2),encoding='utf-8')
        print(name,sha(target))


def fetch_franconia_archive():
    """Inspect an archive's own download link; keep reference outside runtime."""
    import re
    evidence=OUT/'EVIDENCE'
    page='https://www.br.de/br-fernsehen/sendungen/1806/circuli-franconiae-fraenkischer-reichskreis-100.html'
    request=urllib.request.Request(page,headers={'User-Agent':'HistoricalMapResearch/1.0'})
    with urllib.request.urlopen(request,timeout=30) as response:
        html=response.read().decode('utf-8')
    links=sorted(set(re.findall(r'[^\s"<>]+\.(?:jpg|jpeg)(?:\?[^"<>]*)?',html)))
    print(json.dumps(links,ensure_ascii=False,indent=2))
    (evidence/'BR_ARCHIVE_LINKS.json').write_text(json.dumps(dict(page=page,links=links),indent=2),encoding='utf-8')
    assert len(links)==1 and links[0].startswith('/br-fernsehen/sendungen/1806/')
    url='https://www.br.de'+links[0]
    target=evidence/'StadtAN_A4_IV_74_Homann.jpg'
    if not target.exists():
        with urllib.request.urlopen(url,timeout=30) as response:
            target.write_bytes(response.read())
    (evidence/'NUREMBERG_ARCHIVE_SOURCE.json').write_text(json.dumps(dict(page=page,url=url,
        sha256=sha(target),archive='Stadtarchiv Nürnberg',signature='StadtAN A4/IV Nr. 74',
        author='Johann Baptist Homann',date='Not specified by hosting catalog; requires dating before runtime tracing',
        use='Historical research reference only'),indent=2),encoding='utf-8')
    from PIL import Image
    img=Image.open(target)
    print('Archive image',img.size)
    img.thumbnail((2600,2600))
    img.save(OUT/'GEOMETRY/Homann_reading.jpg')


if __name__ == '__main__':
    if sys.argv[1:] == ['capture']:
        capture()
    elif sys.argv[1:] == ['fetch-cliopatria']:
        fetch_cliopatria()
    elif sys.argv[1:] == ['fetch-bsb']:
        fetch_bsb()
    elif sys.argv[1:] == ['fetch-comparison-svg']:
        fetch_comparison_svg()
    elif sys.argv[1:] == ['preview-franken']:
        preview_franken()
    elif sys.argv[1:] == ['fetch-endres']:
        fetch_endres()
    elif sys.argv[1:] == ['fetch-franconia-archive']:
        fetch_franconia_archive()
    elif sys.argv[1:] == ['belgium-scope']:
        belgium_scope()
    elif sys.argv[1:] == ['fetch-belgium-maps']:
        fetch_belgium_maps()
    else:
        raise SystemExit('Use capture or fetch-cliopatria; these commands never write gameplay files.')
