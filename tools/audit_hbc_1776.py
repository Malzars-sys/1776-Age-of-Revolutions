"""Current-workspace HBC audit. Writes diagnostics only; never game data."""
import collections as C
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from validate_diplomacy_ottoman_1776 import parse,walk,scalar

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Games/Victoria 3/game')
OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-01'
STATES=['STATE_NUNAVUT','STATE_SASKATCHEWAN','STATE_MANITOBA','STATE_ONTARIO','STATE_QUEBEC']


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def effective(folder):
    paths={p.relative_to(GAME/folder).as_posix():p for p in (GAME/folder).rglob('*.txt')}
    paths.update({p.relative_to(ROOT/folder).as_posix():p for p in (ROOT/folder).rglob('*.txt')})
    return sorted(paths.values(),key=lambda p:p.name)
def runtime():return {p.relative_to(ROOT).as_posix():sha(p) for folder in ['common','map_data','localization','gfx','gui','events'] for p in (ROOT/folder).rglob('*') if p.is_file()}
def provs(n,key):return [scalar(v.value) for b in n.children(key) for v in b.children()]


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    initial=runtime()
    if not (OUT/'BASELINE.json').exists():dump('BASELINE.json',dict(date='2026-10-25',runtime_sha256=initial,scope='Read-only HBC diagnosis and historical decisions; no territory reassigned'))
    ownership=C.defaultdict(list);raw_states={};declarations=[]
    for path in effective('common/history/states'):
        raw=path.read_text(encoding='utf-8-sig')
        for s in walk(parse(raw)):
            if not s.key.startswith('s:STATE_'):continue
            sid=s.key[2:]
            for n in s.children('create_state'):
                tag=scalar(n.one('country','')).removeprefix('c:')
                for rgb in provs(n,'owned_provinces'):ownership[rgb].append((sid,tag))
                if tag=='HBC':
                    declarations.append(dict(state=sid,rgb_list=provs(n,'owned_provinces'),file=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else 'VANILLA:'+str(path.relative_to(GAME)),line=raw.count('\n',0,n.start)+1))
                    raw_states[sid]=raw[s.start:s.end]
    hbc={rgb for rgb,pairs in ownership.items() if any(t=='HBC' for s,t in pairs)}
    definitions={};all_land=set()
    for path in effective('map_data/state_regions'):
        for n in parse(path.read_text(encoding='utf-8-sig')):
            if n.key.startswith('STATE_'):
                all_land.update(provs(n,'provinces'))
                if n.key in STATES:definitions[n.key]=(set(provs(n,'provinces')),scalar(n.one('id','UNKNOWN')))
    pops=[];buildings=[]
    for kind,rows in [('pops',pops),('buildings',buildings)]:
        for path in effective('common/history/'+kind):
            raw=path.read_text(encoding='utf-8-sig')
            if 'region_state:HBC' not in raw:continue
            for s in walk(parse(raw)):
                if not s.key.startswith('s:STATE_'):continue
                for rs in s.children('region_state:HBC'):
                    for n in rs.children('create_pop' if kind=='pops' else 'create_building'):
                        common=dict(state=s.key[2:],file=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else 'VANILLA:'+str(path.relative_to(GAME)),line=raw.count('\n',0,n.start)+1)
                        if kind=='pops':rows.append(dict(**common,culture=scalar(n.one('culture')),religion=scalar(n.one('religion','DEFAULT')),size=int(n.one('size',0))))
                        else:
                            levels=[int(v.value) for v in walk(n.children('add_ownership')) if v.key=='levels' and isinstance(v.value,str) and v.value.isdigit()]
                            rows.append(dict(**common,building=scalar(n.one('building')),declared_ownership_levels=sum(levels),production_methods=';'.join(provs(n,'activate_production_methods')),interpretation='Creation/ownership command, not certified final engine level'))
    csvout('POPULATION_CURRENT.csv',pops);csvout('BUILDING_COMMANDS_CURRENT.csv',buildings)
    summary=[]
    for sid in STATES:
        items=[d for d in declarations if d['state']==sid];rgbs={rgb for d in items for rgb in d['rgb_list']}
        ps=[p for p in pops if p['state']==sid]
        summary.append(dict(State_ID=sid,Numeric_State_ID=definitions[sid][1],Province_declarations=sum(len(d['rgb_list']) for d in items),Unique_HBC_RGB=len(rgbs),Population=sum(p['size'] for p in ps),Cultures=json.dumps(dict(C.Counter({c:sum(p['size'] for p in ps if p['culture']==c) for c in {p['culture'] for p in ps}})),ensure_ascii=False),State_region_fully_HBC=rgbs==definitions[sid][0],History_file=items[0]['file'],Declaration_line=items[0]['line']))
    csvout('CURRENT_BY_STATE.csv',summary)
    # Current bitmap only: old MAP1 geometry is not silently used as a baseline.
    bmp=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=(bmp[:,:,0]<<16)|(bmp[:,:,1]<<8)|bmp[:,:,2]
    rgb,count=np.unique(packed,return_counts=True);counts={f'x{int(v):06X}':int(c) for v,c in zip(rgb,count)}
    rows=[]
    for key in sorted(hbc):
        pairs=ownership[key];sids=sorted({s for s,t in pairs if t=='HBC'})
        rows.append(dict(Province_RGB=key,State_ID=';'.join(sids),Numeric_State_ID=';'.join(definitions[s][1] for s in sids),Bitmap_pixels=counts.get(key,0),Ownership_declarations=len(pairs),Distinct_owners=';'.join(sorted({t for s,t in pairs})),State_definition_matches=all(key in definitions[s][0] for s in sids),Historical_control='NOT_VALIDATED_FROM_CURRENT_OWNER',Target_owner='UNRESOLVED_PENDING_HISTORICAL_MAPPING',Write_allowed=False))
    csvout('HBC_PROVINCE_REGISTER.csv',rows)
    mask=np.isin(packed,np.asarray([int(k[1:],16) for k in hbc],dtype=np.uint32))
    ys,xs=np.where(mask);bbox=[max(0,int(xs.min())-50),max(0,int(ys.min())-40),min(packed.shape[1],int(xs.max())+51),min(packed.shape[0],int(ys.max())+41)]
    x0,y0,x1,y1=bbox
    land=np.isin(packed,np.asarray([int(k[1:],16) for k in all_land],dtype=np.uint32))
    canvas=np.empty((*packed.shape,3),dtype=np.uint8);canvas[:]=(28,49,63);canvas[land]=(97,111,111);canvas[mask]=(222,179,61)
    cropped=Image.fromarray(canvas[y0:y1,x0:x1]);cropped.thumbnail((1450,1000))
    sheet=Image.new('RGB',(max(1000,cropped.width),cropped.height+165),'#1c313f');sheet.paste(cropped,((sheet.width-cropped.width)//2,65))
    draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    draw.text((18,12),'HBC : territoire actuellement affiché dans le mod',font=font,fill='white')
    draw.text((18,40),'Jaune = propriétaire HBC dans les scripts ; pas une frontière historique validée',font=small,fill='white')
    draw.text((18,cropped.height+82),f"{len(hbc)} RGB distincts ; {sum(p['size'] for p in pops):,} habitants déclarés ; cinq State Regions",font=small,fill='white')
    draw.text((18,cropped.height+109),'Aucun poste placé par conversion GPS approximative. Aucun transfert appliqué.',font=small,fill='white')
    sheet.save(OUT/'CURRENT_HBC_EXTENT.png')
    sources=ROOT/'docs/reports/map/MAP1/inputs/regional_originals'
    reused=[sources/f'R8_NORTH_AMERICA_CARIBBEAN_{n}' for n in ['UNCERTAINTIES.md','SOURCES.csv','RECOMMENDATIONS.csv','COVERAGE.csv']]
    reused += [ROOT/f'docs/reports/map/MAP1/MAP1_CASE_DOSSIERS/R8_NORTH_AMERICA_CARIBBEAN-{n}.md' for n in ['0048','0079','0083','0089','0095']]
    dump('REUSED_WORK.json',[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),status='Existing evidence reused; mapping not assumed valid') for p in reused])
    total=sum(p['size'] for p in pops);cultures={c:sum(p['size'] for p in pops if p['culture']==c) for c in sorted({p['culture'] for p in pops})}
    dump('INVENTORY.json',dict(population=total,cultures=cultures,unique_rgb=len(hbc),province_declarations=sum(len(d['rgb_list']) for d in declarations),HBC_pixels=int(mask.sum()),bitmap_bbox=bbox,bitmap_sha256=sha(ROOT/'map_data/provinces.png'),coordinate_system='Game pixels; no established North America historical georeferencing',duplicates=[r for r in rows if r['Ownership_declarations']>1],building_commands=len(buildings),scope_note='Declared histories, not employee count or a historical census; command order/effects may affect final engine values'))
    final=runtime();external=[k for k in initial.keys()|final.keys() if initial.get(k)!=final.get(k)]
    checks=[('five_current_states',set(d['state'] for d in declarations)==set(STATES)),('all_RGB_in_bitmap',all(r['Bitmap_pixels']>0 for r in rows)),('state_memberships_match',all(r['State_definition_matches'] for r in rows)),('no_conflicting_HBC_owner',all(r['Distinct_owners']=='HBC' for r in rows)),('population_partition',total==sum(r['Population'] for r in summary)),('cultures_partition',sum(cultures.values())==total),('reused_files_exist',all(p.exists() for p in reused)),('no_runtime_file_changed_during_audit',not external)]
    dump('VALIDATION.json',dict(status='AUDITED_HISTORICAL_CLASSIFICATION_READY_GEOMETRY_PENDING',checks=[dict(name=n,passed=bool(v)) for n,v in checks],new_runtime_writes=[],external_runtime_changes=external,human_validated=False,runtime_tested=False,ownership_changes_applied=0))
    print(json.dumps(dict(states=summary,total_population=total,cultures=cultures,unique_rgb=len(hbc),province_declarations=sum(len(d['rgb_list']) for d in declarations),duplicates=len([r for r in rows if r['Ownership_declarations']>1]),checks=checks),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
