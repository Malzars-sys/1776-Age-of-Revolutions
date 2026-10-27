"""One existing Elaphite island pixel, Venice -> Ragusa; no new land or RGB.

--apply once, --validate subsequently. No shared history, POP, flavour or Git writes.
"""
import argparse
import io
import json
import shutil
from collections import Counter
from PIL import Image
import numpy as np
import world1776_balkans06 as b6

b=b6.b;ROOT=b.ROOT;OUT=b.OUT;LOT=OUT/'BALKANS-07-CARTOGRAPHY'
BMP='map_data/provinces.png';POINT=(4503,1065);OLD='x11A0E0';NEW='xE8D201'
def rgb(k):return tuple(bytes.fromhex(k[1:]))
def load(n):return json.loads((LOT/n).read_text('utf8'))
def dump(n,v):(LOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed.'
    before=b.a.sha(ROOT/BMP);im=Image.open(ROOT/BMP).convert('RGB');assert im.getpixel(POINT)==rgb(OLD)
    current=__import__('world1776_balkans04').inventory();assert current==load('BASELINE.json')['inventory'],'Review concurrent territorial evolution.'
    dest=LOT/'apply_inputs'/BMP;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/BMP,dest)
    im.putpixel(POINT,rgb(NEW));buf=io.BytesIO();im.save(buf,format='PNG')
    assert b.a.sha(ROOT/BMP)==before,'Concurrent bitmap change: reread.'
    (ROOT/BMP).write_bytes(buf.getvalue())
    dump('FILES_MODIFIED.json',[{'file':BMP,'before':before,'after':b.a.sha(ROOT/BMP),'pixels_changed':1,'new_RGBs':0}])
    dump('PIXEL_PATCH.json',{'point':POINT,'before':OLD,'after':NEW,'interpretation':'Existing isolated Elaphite island cell, in the Sipan/Lopud group; archipelago-level identification, not surveyed individual-island coordinates.','previous_owner':'VEN','new_owner':'RAG','land_added':0,'coastline_changed':False,'new_RGBs':0})
    print('One existing island pixel reassigned to Ragusa; no land, POP or flavour additions.')
def validate():
    base=load('BASELINE.json');checks=[]
    def ck(k,v,detail=None):checks.append({'check':k,'passed':bool(v),'detail':detail})
    old=np.asarray(Image.open(LOT/'apply_inputs'/BMP).convert('RGB'));now=np.asarray(Image.open(ROOT/BMP).convert('RGB'))
    ys,xs=np.where(np.any(old!=now,axis=2));ck('one_authorized_pixel',list(zip(xs.tolist(),ys.tolist()))==[POINT])
    ck('correct_old_new_colors',tuple(old[POINT[1],POINT[0]])==rgb(OLD) and tuple(now[POINT[1],POINT[0]])==rgb(NEW))
    ck('dimensions_unchanged',old.shape==now.shape==(3616,8192,3))
    # Only one pixel changed; old color survives elsewhere and new color already exists.
    ck('color_set_unchanged',len(xs)==1 and np.count_nonzero(np.all(old==rgb(OLD),axis=2))>1 and np.any(np.all(old==rgb(NEW),axis=2)))
    inv=__import__('world1776_balkans04').inventory()
    for key in ['owners','world_population','odd','git']:ck('unchanged.'+key,inv[key]==base['inventory'][key])
    ck('existing_province_ownerships',inv['owners'][NEW]==[['STATE_DALMATIA','RAG']] and inv['owners'][OLD]==[['STATE_DALMATIA','VEN']])
    for key in ['gameplay','SERG_proofs','prior_WORLD_proofs']:
        differences=[r for r,h in base[key].items() if r!=BMP and (not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h)]
        if key=='SERG_proofs' and (LOT/'EXTERNAL_SERG_REVIEW.json').exists():
            reviewed=load('EXTERNAL_SERG_REVIEW.json')['files']
            valid=all(r in reviewed and reviewed[r]['before']==base[key][r] and reviewed[r]['current']==b.a.sha(ROOT/r)==b.a.sha(LOT/reviewed[r]['archive']) for r in differences)
            ck('preserved_or_exact_reviewed_external.'+key,valid,{'external_documentary_changes':differences})
        else:ck('preserved.'+key,not differences,differences)
    # Both sides are already registered land provinces: the sea/land mask is unchanged.
    ck('no_sea_or_land_creation',NEW in inv['owners'] and OLD in inv['owners'] and len(xs)==1)
    ck('heightmaps_untouched',all(b.a.sha(ROOT/r)==base['gameplay'][r] for r in ['map_data/heightmap.png','map_data/packed_heightmap.png']))
    dump('VALIDATION.json',{'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_validation':False})
    print(json.dumps({'passed':sum(c['passed'] for c in checks),'total':len(checks),'failed':[c['check'] for c in checks if not c['passed']]}))
    return all(c['passed'] for c in checks)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true');args=p.parse_args()
    if args.apply:apply()
    if args.validate:raise SystemExit(0 if validate() else 1)
