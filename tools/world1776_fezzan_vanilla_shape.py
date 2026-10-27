"""Restore only Fezzan's vanilla political outline on explicit player request.

No raster, POP, country setup, vanilla, Git, or SERG writes. Two ambiguous
vanilla Tripoli RGBs retain their current unique TRI owner. Old M03 evidence
and its oasis-core tests remain archived, not rewritten to fit this revision.
"""
import collections
import datetime
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import world1776_maghreb03 as m
import serg_luxembourg_admin_resolution as shared

ROOT=m.ROOT; OUT=m.LOT/'FEZZAN_VANILLA_SHAPE_2026_10_27'
VANILLA=Path(r'C:/Games/Victoria 3/game')
ST=m.ST
SIDS=['STATE_TRIPOLI','STATE_LIBYAN_DESERT']
sha=shared.sha
def dump(name,obj):shared.rm.write_json(OUT/name,obj)
def load(name):return shared.load(OUT/name)
def owners(raw):
    result=collections.Counter()
    for state in shared.cw.parse(raw.lstrip('\ufeff'))[0].children():
        for country in state.children('create_state'):
            for rgb in m.ids(country,'owned_provinces'):
                result[rgb,state.key.removeprefix('s:'),country.one('country').removeprefix('c:')]+=1
    return result

def planned(raw,native):
    prefix='\ufeff' if raw.startswith('\ufeff') else '';clean=raw.lstrip('\ufeff');ops=[];targets={};conflicts=[]
    for sid in SIDS:
        state=m.b.one(clean,'s:'+sid);base=m.b.one(native.lstrip('\ufeff'),'s:'+sid)
        native_fzn=m.ids(m.part(base,'FZN'),'owned_provinces')
        tri=set(m.ids(m.part(state,'TRI'),'owned_provinces')) if sid=='STATE_TRIPOLI' else set()
        shared_rgb=set(native_fzn)&tri
        for rgb in sorted(shared_rgb):conflicts.append(dict(rgb=rgb,state=sid,kept_owner='TRI',reason='Ambiguous vanilla ownership already resolved under MAGHREB-03; retain unique TRI assignment.'))
        target=[rgb for rgb in native_fzn if rgb not in shared_rgb];targets[sid]=target
        fzn=m.part(state,'FZN');zwy=m.part(state,'ZWY')
        source=m.ids(zwy,'owned_provinces')
        result=[rgb for rgb in source if rgb not in target]
        result += [rgb for rgb in m.ids(fzn,'owned_provinces') if rgb not in target and rgb not in result]
        for part,colors in [(fzn,target),(zwy,result)]:
            field=part.children('owned_provinces')[0]
            ops.append((field.start,field.end,'owned_provinces = { '+' '.join('"'+rgb+'"' for rgb in colors)+' }'))
    assert [len(targets[sid]) for sid in SIDS]==[48,30]
    assert {r['rgb'] for r in conflicts}=={'xAFD438','xD5C61D'}
    return prefix+m.b.edits(clean,ops),targets,conflicts

def apply():
    assert not OUT.exists(), 'Never overwrite an earlier pass'
    runtime=shared.shared.previous.runtime.runtime_hashes()
    world=shared.load(m.b.OUT/'ROADMAP_STATE.json')
    protected={p.relative_to(ROOT).as_posix():sha(p) for folder in [m.LOT,ROOT/'docs/reports/map/SERG_CLOSURE'] for p in folder.rglob('*') if p.is_file() and (folder==m.LOT or p.parent==folder or 'ATTESTATION' in p.name)}
    native=(VANILLA/ST).read_bytes().decode('utf-8');raw=(ROOT/ST).read_bytes().decode('utf-8')
    expected,targets,conflicts=planned(raw,native)
    runtime[ST]=hashlib.sha256(raw.encode('utf-8')).hexdigest()
    before=owners(raw);after=owners(expected)
    changes=[dict(rgb=key[0],state=key[1],owner=key[2],count=v) for key,v in (after-before).items()]
    assert len(changes)==71 and {r['owner'] for r in changes}=={'FZN','ZWY'}
    OUT.mkdir()
    dump('BASELINE.json',dict(date='2026-10-27',original_state_text=raw,runtime_sha256=runtime,vanilla_state_sha256=sha(VANILLA/ST),vanilla_bitmap_sha256=sha(VANILLA/'map_data/provinces.png'),protected_proofs=protected,world=world,world_sources={p:(m.b.OUT/p).read_bytes().decode('utf-8') for p in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md']},git=dict(head=shared.shared.previous.git('rev-parse','HEAD'),branch=shared.shared.previous.git('branch','--show-current'),index=sha(ROOT/'.git/index'))))
    dump('GEOMETRY.json',dict(targets=targets,excluded_ambiguous_native_entries=conflicts,before_FZN={sid:[k[0] for k in before if k[1:]==(sid,'FZN')] for sid in SIDS},new_owner_assignments=changes,raw_vanilla_province_entries=80,resolved_vanilla_provinces=78,new_rgb=0,pixels_recolored=0,historical_cadastral_accuracy_claimed=False,authority='Explicit player request: restore the vanilla outline for appearance, even if less historical.'))
    assert (ROOT/ST).read_bytes()==raw.encode('utf-8'), 'Concurrent state change: reread before patching'
    (ROOT/ST).write_bytes(expected.encode('utf-8'))
    dump('FILES_MODIFIED.json',dict(functional_files=[ST],after_sha256={ST:sha(ROOT/ST)},status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',new_human_receipt=None,POP_files_changed=[],bitmap_changed=False))
    print('Fezzan restored to 78 unambiguous native provinces; two TRI assignments preserved. Only existing province ownership lists written.',flush=True)

def packed(path):
    rgb=np.asarray(Image.open(path).convert('RGB'),dtype=np.uint32)
    return (rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2]

def validate():
    b=load('BASELINE.json');g=load('GEOMETRY.json');raw=(ROOT/ST).read_bytes().decode('utf-8');native=(VANILLA/ST).read_bytes().decode('utf-8')
    expected,targets,conflicts=planned(b['original_state_text'],native);old=owners(b['original_state_text']);now=owners(raw);checks=[]
    def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    ck('Exact bounded patch of four owned_provinces fields',raw==expected)
    ck('Both vanilla province sets restored after explicit duplicate resolution',all({k[0] for k in now if k[1:]==(sid,'FZN')}==set(targets[sid]) for sid in SIDS))
    ck('FZN now has 78 unique province assignments',sum(v for k,v in now.items() if k[2]=='FZN')==78)
    affected={r['rgb'] for r in g['new_owner_assignments']}
    ck('All affected provinces have exactly one current owner',all(sum(v for k,v in now.items() if k[0]==rgb)==1 for rgb in affected))
    old_counts=collections.Counter();new_counts=collections.Counter()
    for (rgb,_,_),count in old.items():old_counts[rgb]+=count
    for (rgb,_,_),count in now.items():new_counts[rgb]+=count
    ck('No province added removed or duplicated globally',old_counts==new_counts)
    ck('Only FZN and ZWY change in the two authorized states',all(k[1] in SIDS and k[2] in ['FZN','ZWY'] for k in set(now-old)|set(old-now)))
    ck('Other owners and states exactly preserved',{k:v for k,v in old.items() if not (k[1] in SIDS and k[2] in ['FZN','ZWY'])}=={k:v for k,v in now.items() if not (k[1] in SIDS and k[2] in ['FZN','ZWY'])})
    ck('Prior Tripoli conflict fixes retained',all(now[rgb,'STATE_TRIPOLI','TRI']==1 and sum(v for k,v in now.items() if k[0]==rgb)==1 for rgb in m.TRI))
    ck('Prior Morocco Tekna conflict fixes retained',all(now[rgb,'STATE_INNER_MOROCCO','TEK']==1 and sum(v for k,v in now.items() if k[0]==rgb)==1 for rgb in m.MOR))
    ck('Native state reference unchanged',sha(VANILLA/ST)==b['vanilla_state_sha256'])
    ck('Vanilla bitmap reference unchanged',sha(VANILLA/'map_data/provinces.png')==b['vanilla_bitmap_sha256'])
    ck('All North African POP declarations unchanged',sha(ROOT/m.POP)==b['runtime_sha256'][m.POP])
    ck('Fezzan setup laws relations characters and technologies unchanged',all(sha(ROOT/p)==b['runtime_sha256'][p] for p in [m.COUNTRY,*m.NEW]))
    ck('No regional geography terrain or resource changes',all(sha(ROOT/p)==b['runtime_sha256'][p] for p in ['map_data/state_regions/03_north_africa.txt','map_data/province_terrains.txt']))
    ck('Old MAGHREB and SERG proofs and receipts immutable',all(sha(ROOT/p)==h for p,h in b['protected_proofs'].items()))
    arr=packed(ROOT/'map_data/provinces.png');base=packed(VANILLA/'map_data/provinces.png');values=[int(rgb[1:],16) for colors in targets.values() for rgb in colors]
    mask=np.isin(arr,values);native_mask=np.isin(base,values)
    ck('Restored political mask exactly matches deconflicted vanilla pixels',np.array_equal(mask,native_mask))
    ck('No target province missing from current bitmap',all(np.any(arr==v) for v in values))
    ys,xs=np.where(mask);x0,x1=max(0,int(xs.min())-25),min(arr.shape[1],int(xs.max())+26);y0,y1=max(0,int(ys.min())-25),min(arr.shape[0],int(ys.max())+26)
    crop=arr[y0:y1,x0:x1];canvas=Image.new('RGB',((x1-x0)*2,(y1-y0)+28),'#eee8da');draw=ImageDraw.Draw(canvas)
    palette={'FZN':(186,65,72),'TRI':(196,209,166),'ZWY':(234,204,161),'AJJ':(201,169,184),'TBI':(183,202,190)}
    for panel,data,label in [(0,old,'Avant : neuf provinces'),(1,now,'Apres : contour vanilla')]:
        colored=np.full((*crop.shape,3),210,dtype=np.uint8)
        for tag,color in palette.items():
            rgbs=[int(k[0][1:],16) for k in data if k[1] in SIDS and k[2]==tag]
            colored[np.isin(crop,rgbs)]=color
        image=Image.fromarray(colored);canvas.paste(image,(panel*(x1-x0),28));draw.text((panel*(x1-x0)+6,6),label,fill='black')
    canvas.save(OUT/'BEFORE_AFTER.png')
    current=shared.shared.previous.runtime.runtime_hashes();external={p:dict(before=b['runtime_sha256'].get(p),after=current.get(p)) for p in set(current)|set(b['runtime_sha256']) if p!=ST and current.get(p)!=b['runtime_sha256'].get(p)}
    dump('CONCURRENT_CHANGES.json',dict(external_runtime_changes=external,functional_files_written_by_this_patch=[ST],restorations=[],old_proofs_changed=[]))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c for c in checks if not c['passed']],checks=checks,runtime_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',automated_engine_test=False,command='python -B -X utf8 tools/world1776_fezzan_vanilla_shape.py validate',state_sha256=sha(ROOT/ST),vanilla_state_sha256=b['vanilla_state_sha256'])
    dump('VALIDATION.json',result);print(json.dumps({k:result[k] for k in ['status','passed','total','failed']},ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':
    if sys.argv[1:] and sys.argv[1]=='apply':apply()
    elif sys.argv[1:] and sys.argv[1]=='validate':raise SystemExit(validate()['status']!='PASS')
    else:raise SystemExit('Use apply or validate.')
