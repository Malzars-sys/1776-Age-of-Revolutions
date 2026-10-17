"""MAP2N evidence/audit stages. No runtime writer in the preparatory stage."""
import csv,json,sys,math,time,urllib.request,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import map2m_r9 as prior

ROOT=prior.ROOT;OUT=ROOT/'docs/reports/map/MAP2N';core=prior.core

def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def csvout(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def capture():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'EVIDENCE').mkdir(exist_ok=True)
    assert not (OUT/'BASELINE.json').exists(),'Never overwrite a reference'
    receipt=json.loads((OUT.parent/'MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json').read_text())
    assert receipt['MAP2N_gate']=='SATISFIED' and not receipt['automated_engine_test']
    current=prior.economy.runtime_hashes();ref=prior.load('BASELINE.json')['hashes'].copy();ref.update(prior.load('MANIFEST.json')['functional_files'])
    assert current==ref,'Workspace changed since accepted R9: inspect without restoring'
    inv=core.qa.inventory()
    previous={p.relative_to(ROOT).as_posix():core.sha(p) for name in ['R8','R9'] for p in (OUT.parent/'MAP2M'/name).rglob('*') if p.is_file()}
    for rel in ['tools/map2m_r8.py','tools/map2m_r9.py','docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json']:previous[rel]=core.sha(ROOT/rel)
    dump('BASELINE.json',dict(inventory=inv,hashes=current,earlier_proofs=previous,git_head=prior.old.prior.r2.head(),git_index_sha256=core.sha(ROOT/'.git/index'),
        bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),runtime_receipt='docs/reports/map/MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json'))
    print('Captured accepted R9, manual prerequisite satisfied;',len(current),'functional files protected')

def fetch():
    sources=[('ATLAS_1720.png','https://www.landesmuseum-mv.de/data/bilder/karten-mecklenburg-pommern/map-mecklenburg-pomerania-1720-01-891.png'),
        ('WISMAR_COMPARISON_2022.svg','https://upload.wikimedia.org/wikipedia/commons/0/06/Swedish_Wismar_map.svg'),
        ('WISMAR_COMPARISON_2022.png','https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Swedish_Wismar_map.svg/960px-Swedish_Wismar_map.svg.png')]
    records=[]
    for name,url in sources:
        path=OUT/'EVIDENCE'/name;start=time.perf_counter()
        try:
            if not path.exists():
                req=urllib.request.Request(url,headers={'User-Agent':'MAP2N historical map research, local analysis'})
                with urllib.request.urlopen(req,timeout=30) as response:data=response.read(12_000_001)
                assert len(data)<=12_000_000
                path.write_bytes(data)
            records.append(dict(name=name,url=url,sha256=core.sha(path),bytes=path.stat().st_size,seconds=time.perf_counter()-start))
            print('Acquired',name,path.stat().st_size)
        except Exception as e:records.append(dict(name=name,url=url,error=str(e)));print('Unavailable',name,str(e))
    dump('FETCHED_SOURCES.json',records)

def audit():
    assert not (OUT/'ISLAND_PLAN.json').exists(),'Preparatory audit obsolete; preserve installed Poel reports'
    b=load('BASELINE.json');bmp=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    model=prior.seven.w.load('TRANSFORMATIONS.json')['selected_native'];rows=[]
    for r in b['inventory']['owners']:
        rgb,sid,tag=r['key']
        if sid!='STATE_MECKLENBURG':continue
        ys,xs=np.where(bmp==int(rgb[1:],16));rows.append(dict(RGB=rgb,State_ID=sid,Owner=tag,Pixels=len(xs),X_min=int(xs.min()),Y_min=int(ys.min()),X_max=int(xs.max()),Y_max=int(ys.max()),References=r['count']))
    csvout('CURRENT_PROVINCES.csv',rows)
    hubs=[r for r in prior.locators(bmp) if r['ID']==75];csvout('NATIVE_LOCATORS.csv',hubs)
    diagnostics=[]
    for name,geo in [('WISMAR',[11.466,53.893]),('POEL',[11.433,54.0]),('NEUKLOSTER',[11.683,53.867])]:
        point=prior.seven.r.forward(model,[geo])[0];x,y=map(math.floor,point);rgb='x'+format(int(bmp[y,x]),'06X')
        diagnostics.append(dict(Name=name,Longitude=geo[0],Latitude=geo[1],X=float(point[0]),Y=float(point[1]),RGB=rgb,Owner_State=owners.get(rgb),
            Certified_position=False,Source='Reused R2 approximate geographic targets and frozen R5 native model; not a city homologue'))
    dump('POSITION_DIAGNOSTICS.json',diagnostics)
    for name,box in [('WISMAR',(4349,733,4365,746)),('POEL',(4349,730,4364,741)),('NEUKLOSTER',(4354,735,4370,748))]:
        panels=[prior.old.panel(bmp,box,title,owners,scale=28) for title in ['ETAT ACTUEL : aucun transfert MAP2N','APRES AUDIT : identique, aucune installation']]
        for im in panels:
            d=ImageDraw.Draw(im);v=next(r for r in diagnostics if r['Name']==name);x=(v['X']-box[0])*28;y=(v['Y']-box[1])*28+42
            d.ellipse((x-5,y-5,x+5,y+5),fill='#c83a7c');d.text((10,im.height-24),'Point rose : diagnostic NON CERTIFIE',font=prior.old.font(14),fill='black')
        out=Image.new('RGB',(panels[0].width*2,panels[0].height+55),'white')
        for i,im in enumerate(panels):out.paste(im,(i*im.width,0))
        ImageDraw.Draw(out).text((8,out.height-42),'Avant/apres reels identiques. Gris : eau ; terre : proprietaires actuels.',font=prior.old.font(15),fill='black')
        out.save(OUT/(name+'_BEFORE_AFTER.png'))
    csvout('TERRITORIAL_CHANGES.csv',[],['Sector','X','Y','State_ID','RGB_before','RGB_after','Owner_before','Owner_after','Source','Applied'])
    pops=[dict(State_ID=r['key'][0],Owner=r['key'][1],Culture=r['key'][2],Religion=r['key'][3],Before=r['count'],After=r['count'],Difference=0) for r in b['inventory']['regional_pop'] if r['key'][0]=='STATE_MECKLENBURG']
    csvout('POPULATION_VALIDATION.csv',pops)
    print('Mecklenburg:',rows,'diagnostics:',diagnostics)

def validate():
    assert not (OUT/'ISLAND_PLAN.json').exists(),'Preparatory audit obsolete; run map2n_island.py validate'
    b=load('BASELINE.json');inv=core.qa.inventory();checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value)))
    check('Functional files byte-for-byte unchanged',prior.economy.runtime_hashes()==b['hashes'])
    check('Effective complete inventory unchanged',inv==b['inventory'])
    check('World population835804980',sum(r['count'] for r in inv['pops'])==835804980)
    bmp=core.packed(ROOT/'map_data/provinces.png')
    for rgb,n in [(0x567452,400),(0xE1A03A,290),(0xEDB010,85),(0xFCC7B7,142),(0x41A021,153)]:check('Protected footprint count '+hex(rgb),int((bmp==rgb).sum())==n)
    check('Exact accepted R9 bitmap',core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256'])
    check('Earlier R8 R9 proofs immutable',all(core.sha(ROOT/p)==h for p,h in b['earlier_proofs'].items()))
    check('Inherited44duplicates12badrefs unchanged',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('HEAD and index unchanged',prior.old.prior.r2.head()==b['git_head'] and core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    result=dict(status='MAP2N_AUDITED_NOT_IMPLEMENTED',static_preservation='PASS' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,
        passed=sum(r['passed'] for r in checks),total=len(checks),applied_cells=0,new_RGBs=[],world_population=835804980,engine_tested=False,
        R8_R9_manual_gate='SATISFIED',MAP2N_runtime_status='NOT_IMPLEMENTED_NOT_TESTED',functional_files_changed=[])
    dump('VALIDATION.json',result);print(result['static_preservation'],result['passed'],'/',result['total']);assert result['static_preservation']=='PASS'

if __name__=='__main__':globals()[sys.argv[1]]()
