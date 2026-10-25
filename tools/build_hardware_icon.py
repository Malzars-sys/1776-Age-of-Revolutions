"""Format-only native DDS export of the imagegen transparent hardware cutout."""
from pathlib import Path
import struct
from PIL import Image
from building_dds_compat import BGRA, assert_export_layout

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'workshop_assets/source/aor1776_hardware_transparent.png'
ICON=ROOT/'gfx/interface/icons/goods_icons/aor1776_hardware.dds'
PREVIEW=ROOT/'docs/reports/economy/ALLOYS_1776_REBALANCE/HARDWARE_ICON.png'


def resize(im,size):
    return im.convert('RGBa').resize((size,size),Image.Resampling.LANCZOS).convert('RGBA')


def expected():
    im=Image.open(SOURCE).convert('RGBA')
    assert im.getchannel('A').getextrema()==(0,255)
    assert all(im.getpixel(p)[3]==0 for p in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)])
    target=resize(im,256)
    header=bytearray(128);header[:4]=b'DDS '
    for offset,value in [(4,124),(8,0x2100f),(12,256),(16,256),(20,1024),(28,9),(76,32),(80,0x41),(88,32),(92,BGRA[0]),(96,BGRA[1]),(100,BGRA[2]),(104,BGRA[3]),(108,0x401008)]:
        struct.pack_into('<I',header,offset,value)
    payload=bytes(header)+target.tobytes('raw','BGRA')+b''.join(resize(target,256>>i).tobytes('raw','BGRA') for i in range(1,9))
    assert_export_layout(payload,ICON.relative_to(ROOT).as_posix())
    return target,payload


if __name__=='__main__':
    target,payload=expected()
    ICON.parent.mkdir(parents=True,exist_ok=True)
    if ICON.exists() and ICON.read_bytes()!=payload:
        # Recognize only this export's earlier same-size alpha round-trip.
        earlier=payload[:128]+resize(target,256).tobytes('raw','BGRA')+payload[128+256*256*4:]
        assert ICON.read_bytes()==earlier,'Refuse to replace unrelated art'
    ICON.write_bytes(payload)
    target.save(PREVIEW)
    decoded=Image.open(ICON).convert('RGBA')
    assert decoded.tobytes()==target.tobytes()
    print('Transparent hardware icon exported: native BGRA8, 256 x 256, nine mip levels.')
