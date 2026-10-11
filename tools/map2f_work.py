"""Focused R4 integration support. Immutable dirty-tree baseline and native RGB evidence."""
from pathlib import Path
import collections as C,csv,json,re,sys,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective,values
from map2c_work import ROOT,GAME,sha,packed,source_bitmap,geo_data
from map2e_work import GIT
OUT=ROOT/'docs/reports/map/MAP2F';BASE=OUT/'MAP2F_BASELINE.json'
R4=list(csv.DictReader((ROOT/'docs/reports/map/MAP_1776_9_REGIONS.csv').open(encoding='utf-8-sig')))
TARGETS={r['State_ID'] for r in R4 if r['Region_ID']=='R4_SOUTH_ASIA'}
def dump(name,data):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def snapshot():
    assert not BASE.exists(),'Never overwrite actual baseline'
    inv=qa.inventory();assert sum(r['count'] for r in inv['pops'])==835804980
    folders=['common','map_data','gfx','gui','events','localization','music','.metadata','docs/reports/map/MAP1','docs/reports/map/MAP1C','docs/reports/map/MAP2A','docs/reports/map/MAP2B','docs/reports/map/MAP2C','docs/reports/map/MAP2D','docs/reports/map/MAP2E']
    hashes={p.relative_to(ROOT).as_posix():sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
    originals={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for f in ['common/history','common/country_definitions','common/dynamic_country_names','map_data/state_regions'] for p in (ROOT/f).rglob('*.txt')}
    git={k:subprocess.check_output([GIT,*args],cwd=ROOT,text=True).strip() for k,args in {'head':['rev-parse','HEAD'],'refs':['show-ref']}.items()};git['index']=sha(ROOT/'.git/index')
    dump('MAP2F_BASELINE.json',{'inventory':inv,'originals':originals,'hashes':hashes,'bitmap_sha256':sha(source_bitmap()),'git':git,'scope':sorted(TARGETS)})
    print('Baseline',len(TARGETS),'R4 regions; duplicates',len(inv['duplicates']),'world 835804980',flush=True)
def geography():
    inv=qa.inventory();defs,hubs,names=geo_data();rgb=packed(source_bitmap());crop=rgb[1000:2500,5200:6700]
    owner=C.defaultdict(list)
    for r in inv['owners']:owner[r['key'][0]].append(r['key'][2])
    region_ids={s.key:str(s.one('id')) for p in effective(ROOT,GAME,'map_data/state_regions') for s in cw.parse(p.read_text(encoding='utf-8-sig'))}
    locators={}
    for kind in ['city','port','farm','wood','mine']:
        p=ROOT/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        if not p.exists():p=GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        pos={ident:(float(x),3616-float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',p.read_text(encoding='utf-8-sig'))}
        for sid in TARGETS:
            if region_ids[sid] not in pos:continue
            x,y=pos[region_ids[sid]];v='x%06X'%int(rgb[int(y),int(x)])
            locators[sid+'|'+kind]={'name':names.get('HUB_NAME_'+sid+'_'+kind,''),'x':x,'y':y,'rgb':v,'hub':hubs[sid].get(kind),'owners':owner.get(v,[])}
    rows={}
    for sid in TARGETS:
        for v in defs[sid]:
            yy,xx=np.where(crop==int(v[1:],16))
            if not len(xx):continue
            rows[v]={'state':sid,'owners':owner.get(v,[]),'pixels':len(xx),'bbox':[int(xx.min()+5200),int(yy.min()+1000),int(xx.max()+5200),int(yy.max()+1000)],'centroid':[float(xx.mean()+5200),float(yy.mean()+1000)]}
    dump('GEOGRAPHY.json',{'provinces':rows,'locators':locators,'crop':[5200,1000,6700,2500],'source':'Native RGB bitmap, existing locators identify geography not historical sovereignty'})
    for sid in ['STATE_BOMBAY','STATE_CIRCARS','STATE_MADRAS','STATE_CEYLON','STATE_ASSAM','STATE_GUJARAT','STATE_RAJPUTANA','STATE_BUNDELKHAND','STATE_PUNJAB','STATE_HILL_PUNJAB','STATE_BALUCHISTAN']:
        print(sid,flush=True)
        for k,r in locators.items():
            if k.startswith(sid+'|'):print(k,r)
        for v,r in rows.items():
            if r['state']==sid:print(v,','.join(r['owners']),r['bbox'],r['centroid'],r['pixels'])
def compare_collaborator():
    raw=subprocess.check_output([GIT,'show','georg3mx-map-rework:common/history/states/00_states.txt'],cwd=ROOT).decode('utf-8-sig')
    current=(ROOT/'common/history/states/00_states.txt').read_text(encoding='utf-8-sig');result=[]
    old={s.key:qa.norm(s) for s in cw.walk(cw.parse(current)) if s.key.removeprefix('s:') in TARGETS}
    for s in cw.walk(cw.parse(raw)):
        if s.key in old and qa.norm(s)!=old[s.key]:result.append({'state':s.key,'current':old[s.key],'collaborator':qa.norm(s)})
    dump('COLLABORATOR_COMPARISON.json',result);print('R4 collaborator differing state scopes',len(result))
if __name__=='__main__':{'snapshot':snapshot,'geography':geography,'collaborator':compare_collaborator}[sys.argv[1]]()
