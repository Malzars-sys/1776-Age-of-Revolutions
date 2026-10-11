"""Read-only map-derived previews and crops; source files remain intact."""
from pathlib import Path
from PIL import Image
import sys
E=Path(__file__).resolve().parents[1]/'docs/reports/map/MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE'
Image.MAX_IMAGE_PIXELS=200000000
for name in (['lux_1771','lombardy_1750','lombardy_west_1750','silesia_1758'] if len(sys.argv)==1 else []):
    im=Image.open(E/(name+'.jpg')).convert('RGB')
    im.resize((1600,round(im.height*1600/im.width))).save(E/(name+'_1600.png'))
if len(sys.argv)>1:
    name=sys.argv[1]; box=tuple(map(int,sys.argv[2:6]))
    im=Image.open(E/name)
    im.crop(box).save(E/(Path(name).stem+'_crop_'+ '_'.join(map(str,box))+'.png'))
