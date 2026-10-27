"""Format-only export and icon-binding checks; never changes PM recipes."""
import copy
import json
import math
from pathlib import Path
import struct
import sys
from PIL import Image, ImageDraw, ImageFont
import econ_alloys_1776 as econ
from building_dds_compat import BGRA, assert_export_layout

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/assets/HARDWARE_PM_ICONS'
MASTERS='workshop_assets/source/hardware_pm_icons'
ICONS='gfx/interface/icons/production_method_icons'
ITEMS=[
 ('pm_aor1776_wrought_iron_utensils','01_forged_cast_red.png','1776_hardware_forged_cast_red.dds','Forge et moulage'),
 ('pm_aor1776_copper_brass_utensils','02_copper_brass_red.png','1776_hardware_copper_brass_red.dds','Cuivre et laiton'),
 ('pm_aor1776_machined_utensils','03_machined_red.png','1776_hardware_machined_red.dds','Usinage'),
 ('pm_aor1776_industrial_utensils','04_industrial_red.png','1776_hardware_industrial_red.dds','Industrialisée'),
]
DISABLED='gfx/interface/icons/production_method_icons/unused/disabled.dds'
SIZE=208


def resized(im,size):return im.convert('RGBa').resize((size,size),Image.Resampling.LANCZOS).convert('RGBA')


def expected(master):
    image=Image.open(master).convert('RGBA')
    assert image.width==image.height and image.getchannel('A').getextrema()==(0,255)
    for pt in [(0,0),(image.width-1,0),(0,image.height-1),(image.width-1,image.height-1)]:assert image.getpixel(pt)[3]==0
    icon=resized(image,SIZE)
    header=bytearray(128);header[:4]=b'DDS '
    count=int(math.log2(SIZE))+1
    for offset,value in [(4,124),(8,0x2100f),(12,SIZE),(16,SIZE),(20,SIZE*4),(28,count),(76,32),(80,0x41),(88,32),(92,BGRA[0]),(96,BGRA[1]),(100,BGRA[2]),(104,BGRA[3]),(108,0x401008)]:struct.pack_into('<I',header,offset,value)
    levels=[icon];size=SIZE
    while size>1:
        size=max(1,size//2);levels.append(resized(icon,size))
    assert len(levels)==count
    return icon,bytes(header)+b''.join(im.tobytes('raw','BGRA') for im in levels),count


def normalized(raw):
    nodes=copy.deepcopy(econ.parse(raw))
    for node in nodes:
        if node.key in econ.UTENSILS:node.value=[v for v in node.children() if v.key!='texture']
    return [econ.canonical(n) for n in nodes]


def build(export=False):
    baseline=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    pmfile=ROOT/econ.NEW_PM
    rows=[];previews=[]
    for key,source,dest,label in ITEMS:
        path=ROOT/ICONS/dest;master=ROOT/MASTERS/source
        icon,payload,mips=expected(master)
        if export:
            assert not path.exists() or path.read_bytes()==payload,'Refuse to replace unrelated artwork'
            path.write_bytes(payload)
        assert path.read_bytes()==payload
        assert_export_layout(payload,path.relative_to(ROOT).as_posix())
        assert Image.open(path).convert('RGBA').tobytes()==icon.tobytes()
        icon.save(OUT/(dest[:-4]+'.png'))
        coloured=[(r,g,b) for r,g,b,a in icon.get_flattened_data() if a>180 and max(r,g,b)-min(r,g,b)>40]
        assert coloured and sum(r>g and r>b for r,g,b in coloured)/len(coloured)>.97,'Expected red icon family'
        rows.append(dict(id=key,dds=path.relative_to(ROOT).as_posix(),source=master.relative_to(ROOT).as_posix(),size=SIZE,mips=mips,source_sha256=econ.sha(master),dds_sha256=econ.sha(path),provenance='docs/reports/assets/HARDWARE_PM_ICONS/VALIDATION.json'))
        previews.append((label,icon))
    methods=econ.definitions('common/production_methods')[0]
    for row in rows:assert econ.scalar(methods[row['id']][0].one('texture'))==row['dds']
    assert econ.scalar(methods['pm_aor1776_no_utensils'][0].one('texture'))==DISABLED
    assert econ.scalar(methods['pm_no_canal_network'][0].one('texture'))==DISABLED
    assert (econ.GAME/DISABLED).exists()
    assert normalized(pmfile.read_text(encoding='utf-8-sig'))==normalized(baseline['pm_text']),'Non-texture PM change'
    assert econ.sha(ROOT/'gfx/interface/icons/goods_icons/aor1776_hardware.dds')==baseline['goods_icon_sha256']
    for rel,sha in baseline['references'].items():assert econ.sha(Path(rel))==sha,'Reference modified'
    registry_path=ROOT/'docs/reports/assets/source_registry.json'
    registry=json.loads(registry_path.read_text(encoding='utf-8-sig'))
    before_path=OUT/'REGISTRY_BEFORE.json'
    if export and not before_path.exists():before_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
    old=json.loads(before_path.read_text(encoding='utf-8'))
    by_dds={v['dds']:v for v in registry['entries']}
    for row in rows:
        entry={k:v for k,v in row.items() if k!='id'}
        if export and row['dds'] not in by_dds:registry['entries'].append(entry)
        else:assert by_dds[row['dds']]==entry
    if export:registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    current=json.loads(registry_path.read_text(encoding='utf-8-sig'))
    new_dds={r['dds'] for r in rows}
    assert [v for v in current['entries'] if v['dds'] not in new_dds]==old['entries'],'Unrelated registry entries changed'
    assert len({v['dds'] for v in current['entries']})==len(current['entries'])
    # Contact sheet checks large and actual UI scales on two contrasting grounds.
    sheet=Image.new('RGB',(1000,470),'#292e33');draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for i,(label,icon) in enumerate(previews):
        x=i*250;draw.text((x+12,10),label,font=font,fill='white')
        sheet.paste(icon,(x+21,45),icon)
        for row,bg in enumerate(['#292e33','#d3cec2']):
            y=275+row*85;draw.rectangle((x+8,y,x+242,y+75),fill=bg)
            for dx,size in [(18,32),(83,48),(165,64)]:
                thumb=resized(icon,size);sheet.paste(thumb,(x+dx,y+5),thumb)
    sheet.save(OUT/'PREVIEW.png')
    result=dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',icons=rows,neutral_texture=DISABLED,neutral_matches_canals=True,alpha_and_native_layout_valid=True,only_PM_textures_changed=True,other_registry_entries_preserved=True,goods_icon_preserved=True,reference_art_preserved=True,runtime_tested=False)
    (OUT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS: four red PM icons, canal disabled icon reused, native BGRA8/mips/alpha, recipes and other artwork preserved.')


if __name__=='__main__':build('--export' in sys.argv)
