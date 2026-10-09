"""Analysis-only function contact sheet: approved masters are never retouched."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'.asset-cache/early_ship_equipment_2026-10-08'
PROPOSAL=ROOT/'docs/reports/naval/naval_functions_art_proposals_2026-10-08.json'

def main(proposal_path=PROPOSAL):
    proposal=json.loads(proposal_path.read_text(encoding='utf-8'))
    sheet=Image.new('RGB',(300*len(proposal['entries']),310),'#213138')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
    stats=[]
    for i,row in enumerate(proposal['entries']):
        source=ROOT/row['proposed_master']
        assert source.read_bytes()==Path(row['generator_source']).read_bytes()
        if row.get('source_sha256'):
            assert hashlib.sha256(source.read_bytes()).hexdigest()==row['source_sha256']
        im=Image.open(source)
        assert im.mode=='RGBA'
        alpha=im.getchannel('A');hist=alpha.histogram();bbox=alpha.getbbox()
        assert hist[0]>0 and bbox
        stats.append(dict(key=row['key'],sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            size=im.size,alpha_zero=hist[0],alpha_opaque=hist[255],alpha_partial=sum(hist[1:255]),bbox=bbox))
        draw.text((i*300+12,10),row['label'],font=font,fill='white')
        for size,y in ((180,42),(64,226),(32,270)):
            # Crops and size variants are solely for this ignored inspection sheet.
            thumb=im.crop(bbox)
            thumb.thumbnail((size,140 if size==180 else size),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(i*300+(300-thumb.width)//2,y),thumb)
    sheet.save(ROOT/proposal['qa']['comparison'])
    (ROOT/proposal['qa']['alpha_report']).write_text(json.dumps(stats,indent=2),encoding='utf-8')
    print(json.dumps(dict(preview=proposal['qa']['comparison'],metrics=stats)))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--proposal',type=Path,default=PROPOSAL)
    args=parser.parse_args()
    main(args.proposal)
