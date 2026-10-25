"""Format the supplied cultural illustrations for native unit panels.

Retain each original PNG. Export a centered square crop at the native 512px
unit size, BGRA8 with all ten mipmaps. No generative image changes.
Default is read-only; --export writes this unit's new assets only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import struct
from PIL import Image, ImageOps
from building_dds_compat import BGRA, assert_export_layout

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'docs/reports/military/ENGINEER_CORPS'
SOURCE = ROOT/'workshop_assets/source/engineer_corps'
ATTACHMENTS = {
    'generic': 'a42ef6f7-904a-4fcb-b508-6368b71d8f9b',
    'european': 'f3ed7f48-d352-4eb4-b31f-83677b562406',
    'east_asian': '577907c5-dd55-4d1f-91c8-7621fb8ca4e8',
    'american': 'c7df8ec0-25b3-48d9-8e6f-f945ec6e4aff',
    'african': 'cfbe8a7c-2e36-45c3-9bbb-9ee705e6bc30',
    'arabic': '00c8ed82-06b0-4ce3-b2b5-6f9b80450dfb',
    'south_asian': '8b046f8b-fd3b-4089-9b73-1c718f936709',
}


def encode(path):
    source = Image.open(path).convert('RGBA')
    base = ImageOps.fit(source, (512,512), Image.Resampling.LANCZOS, centering=(.5,.5))
    header=bytearray(128); header[:4]=b'DDS '
    for offset,value in [(4,124),(8,0x2100f),(12,512),(16,512),(20,2048),(28,10),
                         (76,32),(80,0x41),(88,32),(92,BGRA[0]),(96,BGRA[1]),
                         (100,BGRA[2]),(104,BGRA[3]),(108,0x401008)]:
        struct.pack_into('<I',header,offset,value)
    payload=bytes(header)+b''.join(base.resize((512>>i,512>>i),Image.Resampling.LANCZOS).tobytes('raw','BGRA') for i in range(10))
    assert_export_layout(payload, path.name)
    assert len(payload)==1398228
    return payload,base


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--export',action='store_true'); args=ap.parse_args()
    rows=[]
    for region,attachment in ATTACHMENTS.items():
        master=SOURCE/(region+'.png')
        if args.export and not master.exists():
            master.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(Path('C:/Users/simeo/AppData/Local/Temp')/('codex-clipboard-'+attachment+'.png'),master)
        payload,preview=encode(master)
        suffix='' if region=='generic' else '_'+region
        target=ROOT/f'gfx/unit_illustrations/1776_engineer_corps{suffix}.dds'
        if args.export:
            assert not target.exists() or target.read_bytes()==payload,'Concurrent illustration edit: '+str(target)
            target.write_bytes(payload)
            preview.save(REPORT/(region+'_preview.png'))
        assert target.read_bytes()==payload
        rows.append(dict(region=region,source=master.relative_to(ROOT).as_posix(),
                         original_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),
                         target=target.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(payload).hexdigest(),
                         size=[512,512],mips=10,format='BGRA8',conversion='Centered square crop and resize only'))
    result=dict(art=rows,generic='USER_IMAGE_a42ef6f7-904a-4fcb-b508-6368b71d8f9b',runtime='NOT_RUN')
    if args.export: (REPORT/'ART.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(exported=len(rows),generic=result['generic']),indent=2))


if __name__=='__main__': main()
