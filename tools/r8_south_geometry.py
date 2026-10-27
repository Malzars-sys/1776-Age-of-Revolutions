"""Current-bitmap localization for the authorized 1776 southern North America pass.

Modern place coordinates are geodetic proxies only, not sovereignty evidence.
Writes diagnostic data; never game files.
"""
import csv,json,re,unicodedata,zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha
from validate_diplomacy_ottoman_1776 import parse
from georeference.model import fit,evaluate,forward,inverse

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/R8-CORRECTIONS-01'
GEO=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE'
SIDES=['city','port','farm','mine','wood']
REGIONS={'STATE_'+s for s in ['LOUISIANA','KANSAS','OKLAHOMA','ARKANSAS','MISSOURI','KENTUCKY','TENNESSEE','MISSISSIPPI','ALABAMA','FLORIDA','TEXAS','NEW_MEXICO','ARIZONA','SONORA','CHIHUAHUA']}


def norm(s):return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace(' ','').replace('.','')
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def bitmap():
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    return (b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]


def main():
    OUT.mkdir(parents=True,exist_ok=True);a=bitmap();loc={}
    for k in SIDES:
        rel=Path('gfx/map/map_object_data/generated_map_object_locators_'+k+'.txt');p=ROOT/rel if (ROOT/rel).exists() else GAME/rel
        raw=p.read_text(encoding='utf-8-sig')
        for m in re.finditer(r'\{\s*id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([-\d.]+)\s+([-\d.]+)\s*([-\d.]+)\s*\}',raw):
            loc[int(m[1]),k]=([float(m[2]),a.shape[0]-float(m[4])],str(p),raw.count('\n',0,m.start())+1)
    defs={n.key:n for p in effective('map_data/state_regions') for n in parse(p.read_text(encoding='utf-8-sig')) if n.key in REGIONS}
    with zipfile.ZipFile(GEO/'cities1000.zip') as z:
        records=[r for l in z.read('cities1000.txt').decode().splitlines() if (r:=l.split('\t'))[8] in ['US','MX']]
    aliases={'Santa fe':'Santa Fe','St Louis':'St. Louis','Pine bluff':'Pine Bluff','Las Cruces':'Las Cruces','Ruidose':'Ruidoso'}
    admin={'STATE_LOUISIANA':'LA','STATE_KANSAS':'KS','STATE_OKLAHOMA':'OK','STATE_ARKANSAS':'AR','STATE_MISSOURI':'MO','STATE_KENTUCKY':'KY','STATE_TENNESSEE':'TN','STATE_MISSISSIPPI':'MS','STATE_ALABAMA':'AL','STATE_FLORIDA':'FL','STATE_TEXAS':'TX','STATE_NEW_MEXICO':'NM'}
    controls=[]
    for row in csv.DictReader((ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig')):
        sid,k,name=row['State_ID'],row['Hub_Type'],row['Hub_Name']
        if sid not in admin:continue
        candidates=[r for r in records if r[8]=='US' and r[10]==admin[sid] and norm(r[1])==norm(aliases.get(name,name))]
        if not candidates:continue
        record=max(candidates,key=lambda r:int(r[14] or 0));px,path,line=loc[int(defs[sid].one('id')),k];rgb=f'x{int(a[int(px[1]),int(px[0])]):06X}'
        if rgb not in provs(defs[sid],'provinces'):continue
        controls.append(dict(name=name,role='FIT' if k=='city' else 'CHECK',geo=[float(record[5]),float(record[4])],pixel=px,state=sid,kind=k,rgb=rgb,geonames_id=record[0],locator_file=path,locator_line=line))
    model=fit(controls,'miller_affine',a.shape[::-1]);evaluation=evaluate(model)
    dump('GEODETIC_CONTROLS.json',controls);dump('GEODETIC_MODEL.json',model);dump('GEODETIC_EVALUATION.json',evaluation)
    dump('GEOMETRY_INPUTS.json',dict(bitmap_sha256=sha(ROOT/'map_data/provinces.png'),geonames_sha256=sha(GEO/'cities1000.zip'),note='Empirical hub fit; historical territorial precision is not established.'))
    print(json.dumps(dict(controls=len(controls),fit=len([r for r in controls if r['role']=='FIT']),evaluation=evaluation),ensure_ascii=False))


if __name__=='__main__':main()
