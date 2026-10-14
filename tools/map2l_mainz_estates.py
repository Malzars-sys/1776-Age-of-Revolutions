"""Scoped continuation: Bergstrasse/Starkenburg and Main-Spessart Mainz estates."""
import json
import sys
import urllib.request
from PIL import Image,ImageDraw,ImageFont
import map2l_mainz as core
OUT=core.ROOT/'docs/reports/map/MAP2L/MAINZ_ESTATES'
core.OUT=OUT
core.REGIONS={'STATE_HESSE','STATE_BADEN','STATE_FRANCONIA'}
core.BACKUP=OUT.parent/'MAINZ_PALATINATE/provinces_candidate.png'

def fetch_comparison():
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'OBERSTIFT_1789_COMPARISON.jpg'
    assert not target.exists(),'Preserve source'
    url='https://www.historisches-lexikon-bayerns.de/images/7/79/Artikel_45154_bilder_value_4_oberstift2.jpg'
    with urllib.request.urlopen(url,timeout=25) as r:data=r.read(20_000_001)
    assert len(data)<20_000_000
    import io
    Image.open(io.BytesIO(data)).verify();target.write_bytes(data)
    core.dump('COMPARISON_SOURCE.json',dict(catalogue='https://www.historisches-lexikon-bayerns.de/Lexikon/Mainzer_Oberstift',
        observed_image_page='https://www.historisches-lexikon-bayerns.de/Lexikon/Datei:Artikel_45154_bilder_value_4_oberstift2.jpg',
        url=url,sha256=core.sha(target),size=list(Image.open(target).size),historical_date=1789,publication='Spindler/Diepolder, Bayerischer Geschichtsatlas, 1969, p.30',
        license='Copyright Bayerischer Schulbuchverlag, retained research comparison only; not shipped as gameplay artwork',
        warning='Not automatically 1776 borders; apply only corroborated continuity and inspect omitted micro-estates'))
    print(Image.open(target).size,core.sha(target))

def crops():
    OUT.mkdir(parents=True,exist_ok=True)
    im=Image.open(OUT.parent/'RHINE_CENTRAL/DE_WIT_MAINZ_3500.jpg').convert('RGB');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for name,box in [('BERGSTRASSE',(1430,1530,2400,2260)),('ORB_LOHR',(2130,490,3330,1210)),('KLINGENBERG_MILTENBERG',(2110,1410,2810,2070))]:
        image=im.crop(box);d=ImageDraw.Draw(image)
        for x in range((box[0]//100+1)*100,box[2],100):
            d.line((x-box[0],0,x-box[0],image.height),fill='blue');d.text((x-box[0]+1,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            d.line((0,y-box[1],image.width,y-box[1]),fill='blue');d.text((1,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        image.save(OUT/(name+'_READING.png'))
    path=OUT/'OBERSTIFT_1789_COMPARISON.jpg'
    if path.exists():
        source=Image.open(path).convert('RGB')
        for name,box in [('HL_TOWNS',(200,200,490,500)),('HL_FRANKFURT',(0,95,100,165))]:
            source.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3)).save(OUT/(name+'.png'))
        image=source.resize((1200,1508));d=ImageDraw.Draw(image)
        for x in range(0,600,50):
            d.line((x*2,0,x*2,1508),fill='blue');d.text((x*2+1,1),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range(0,754,50):
            d.line((0,y*2,1200,y*2),fill='blue');d.text((1,y*2+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        image.save(OUT/'OBERSTIFT_READING.png')

if __name__=='__main__':({'fetch-comparison':fetch_comparison,'crops':crops}.get(sys.argv[1]) or getattr(core,sys.argv[1]))()
