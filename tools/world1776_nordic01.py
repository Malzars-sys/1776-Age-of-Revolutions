"""NORDIC-01: current Scandinavian/Finnish border survey; explicit bounded patches.

No Git/vanilla writes. Survey captures are immutable; reports are separate from
the historic WORLD 320-point denominator. Run --survey once, then --inspect.
"""
import argparse, json, re, shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import world1776_balkans03 as b
import world1776_balkans04 as b4

ROOT=b.ROOT; WORLD=b.OUT; LOT=WORLD/'NORDIC-01'
STATES='common/history/states/00_states.txt'
SIDS=['SVEALAND','GOTALAND','NORRLAND','GOTLAND','SCANIA','JUTLAND','ZEALAND',
      'WESTERN_NORWAY','NORTHERN_NORWAY','EASTERN_NORWAY','ICELAND',
      'UUSIMAA','KUOPIO','WEST_KARELIA','ALAND','OSTROBOTHNIA','OULU',
      'EAST_KARELIA','KOLA']
def save(name,value):
    p=LOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((LOT/name).read_text('utf8'))
def hashes():
    folders=['common','events','gui','gfx','localization','map_data','docs/reports/map/SERG_CLOSURE']
    return {p.relative_to(ROOT).as_posix():b.a.sha(p) for f in folders for p in (ROOT/f).rglob('*') if p.is_file()}
def survey():
    LOT.mkdir(parents=True,exist_ok=True)
    assert not (LOT/'BEFORE.json').exists(),'Survey already captured; do not replace its baseline.'
    inv=b4.inventory()
    save('BEFORE.json',dict(captured_utc=datetime.now(timezone.utc).isoformat(),historical_date='1776-01-01',
                           inventory=inv,protected=hashes()))
    for rel in [STATES,'common/history/pops/00_west_europe.txt','common/history/pops/02_east_europe.txt',
                'map_data/state_regions/00_west_europe.txt','map_data/state_regions/02_east_europe.txt',
                'map_data/state_regions/15_russia.txt']:
        p=LOT/'survey_inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
    print('Captured current workspace, owners and population:',inv['world_population'])
def inspect():
    regions=b.a.catalog('map_data/state_regions');text=b.a.raw(ROOT/STATES)
    image=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=image[:,:,0]*65536+image[:,:,1]*256+image[:,:,2]
    owners=b4.inventory()['owners'];rows=[]
    pops=Counter()
    for path in b.tech.effective('common/history/pops'):
        for n in b.walk(b.parse(b.a.raw(path))):
            if n.key.startswith('s:STATE_'):
                for part in n.children():
                    for pop in part.children('create_pop'):pops[n.key[2:],part.key.split(':',1)[-1]]+=int(pop.one('size'))
    for suffix in SIDS:
        sid='STATE_'+suffix
        if sid not in regions:continue
        n,path=regions[sid];st=b.one(text,'s:'+sid);ids=[x.strip('"') for x in b.a.ids(n,'provinces')]
        cells=[]
        for c in ids:
            yy,xx=np.where(packed==int(c[1:],16))
            cells.append(dict(rgb=c,owners=owners.get(c,[]),pixels=len(xx),
                bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())] if len(xx) else None,
                center=[float(xx.mean()),float(yy.mean())] if len(xx) else None))
        rows.append(dict(state=sid,file=str(path.relative_to(ROOT)),
            parts=[dict(owner=p.one('country'),province_count=len(b.a.ids(p,'owned_provinces')),
                        population=pops[sid,p.one('country')[2:]]) for p in st.children('create_state')],
            hubs={k:n.one(k) for k in ['city','port','farm','mine','wood']},provinces=cells))
    save('TERRITORIAL_INVENTORY.json',rows)
    for r in rows:print(r['state'],r['parts'])
    # Data map: real province geometry, equal pixel crop, no cosmetic smoothing.
    lut=np.zeros((1<<24,3),dtype=np.uint8);lut[:]=[208,224,232]
    colors={'SWE':[233,190,77],'DENNOR':[194,89,83],'RUS':[115,169,109]}
    for c,parts in owners.items():lut[int(c[1:],16)]=colors.get(parts[0][1],[200,196,182]) if parts else [220,220,220]
    for name,box in [('overview',(4140,0,4950,600)),('finland',(4550,250,4900,570)),('north',(4530,0,4910,280))]:
        x0,y0,x1,y1=box;data=packed[y0:y1,x0:x1];pic=Image.fromarray(lut[data]);d=ImageDraw.Draw(pic)
        edge=np.zeros(data.shape,dtype=bool);edge[1:,:]|=data[1:,:]!=data[:-1,:];edge[:,1:]|=data[:,1:]!=data[:,:-1]
        ar=np.asarray(pic).copy();ar[edge]=(80,85,80);pic=Image.fromarray(ar).resize(((x1-x0)*3,(y1-y0)*3));d=ImageDraw.Draw(pic)
        font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
        for r in rows:
            for p in r['provinces']:
                if not p['center']:continue
                x,y=p['center']
                if x0<=x<x1 and y0<=y<y1 and name!='overview':d.text(((x-x0)*3,(y-y0)*3),p['rgb'][1:],font=font,fill='black',stroke_width=1,stroke_fill='white')
        pic.save(LOT/(name+'.png'))
    print('Survey maps written.')

PLAN=[dict(state='STATE_KUOPIO',donor='SWE',recipient='RUS',rgb=['xB81268'],
           description='Nyslott/Savonlinna; 1743 cession, whole native polygon approximation.'),
      dict(state='STATE_NORTHERN_NORWAY',donor='DENNOR',recipient='RUS',
           rgb=['x2495FE','xFEC50D','x7005BB','x6480A4'],
           description='South of Varangerfjord, Neiden/Pasvik common districts; Russian secular and ecclesiastical jurisdiction, overlapping Danish-Norwegian taxation remains a documented limitation.')]
POPS=['common/history/pops/00_west_europe.txt','common/history/pops/15_russia.txt']
def transform(originals):
    out=dict(originals);text=out[STATES];ops=[]
    for row in PLAN:
        n=b.one(text,'s:'+row['state']);donor=next(p for p in n.children('create_state') if p.one('country')=='c:'+row['donor'])
        block=text[n.start:n.end];local=b.one(block,'owned_provinces');items=[c.value for c in local.children()]
        assert set(row['rgb']).issubset({c.strip('"') for c in items})
        remaining=[c for c in items if c.strip('"') not in row['rgb']]
        body='owned_provinces = { '+' '.join(remaining)+' }'
        block=b.edits(block,[(local.start,local.end,body)])
        local_state=b.one(block,'s:'+row['state'])
        added='\n\t\tcreate_state = { country = c:'+row['recipient']+' owned_provinces = { '+' '.join('"'+c+'"' for c in row['rgb'])+' } }\n\t'
        block=b.edits(block,[(local_state.end-1,local_state.end-1,added)])
        ops.append((n.start,n.end,block))
    out[STATES]=b.edits(text,ops)
    ledger=[]
    for rel in POPS:
        text=originals[rel];ops=[]
        for row in PLAN:
            matches=[n for n in b.walk(b.parse(text)) if n.key=='s:'+row['state']]
            if not matches:continue
            n,=matches;part=next(p for p in n.children() if p.key=='region_state:'+row['donor'])
            st=b.one(originals[STATES],'s:'+row['state']);p=next(p for p in st.children('create_state') if p.one('country')=='c:'+row['donor'])
            numerator=len(row['rgb']);denominator=len(set(b.a.ids(p,'owned_provinces')))
            block=text[n.start:n.end];ed=[];new=[]
            for pop in part.children('create_pop'):
                size=pop.children('size')[0];before=int(size.value);moved=(before*numerator+denominator//2)//denominator
                ed.append((size.start-n.start,size.end-n.start,'size = '+str(before-moved)))
                snippet=text[pop.start:pop.end];local_size=b.one(snippet,'size')
                new.append(b.edits(snippet,[(local_size.start,local_size.end,'size = '+str(moved))]))
                ledger.append(dict(state=row['state'],culture=pop.one('culture'),religion=pop.one('religion'),pop_type=pop.one('pop_type'),
                    donor=row['donor'],recipient=row['recipient'],before=before,donor_after=before-moved,recipient_after=moved,
                    allocation=dict(transferred_provinces=numerator,donor_provinces=denominator),historical_population_estimate=False))
            block=b.edits(block,ed);node=b.one(block,'s:'+row['state'])
            block=b.edits(block,[(node.end-1,node.end-1,'\n\t\tregion_state:'+row['recipient']+' = {\n'+'\n'.join(new)+'\n\t\t}\n\t')])
            ops.append((n.start,n.end,block))
        out[rel]=b.edits(text,ops)
    for s in out.values():b.parse(s)
    return out,ledger
def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed; use --validate.'
    paths=[STATES]+POPS;old={r:b.a.raw(ROOT/r) for r in paths};sha={r:b.a.sha(ROOT/r) for r in paths}
    proposed,ledger=transform(old)
    save('PLAN.json',PLAN);save('POPULATION_ALLOCATION.json',ledger)
    for rel in paths:
        dest=LOT/'apply_inputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
    assert all(b.a.sha(ROOT/r)==sha[r] for r in paths),'Concurrent changes: reread.'
    receipts=[]
    for rel,txt in proposed.items():
        assert b.a.sha(ROOT/rel)==sha[rel]
        (ROOT/rel).write_bytes((b'\xef\xbb\xbf' if (ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf') else b'')+txt.encode('utf8'))
        receipts.append(dict(file=rel,before=sha[rel],after=b.a.sha(ROOT/rel)))
    save('FILES_MODIFIED.json',receipts)
    print('Applied',len(receipts),'files, five existing RGBs; population delta 0.')
def demographics():
    total=Counter();parts=Counter()
    for path in b.tech.effective('common/history/pops'):
        for n in b.walk(b.parse(b.a.raw(path))):
            if not n.key.startswith('s:STATE_'):continue
            for p in n.children():
                for pop in p.children('create_pop'):
                    key=(pop.one('culture'),pop.one('religion'),pop.one('pop_type'))
                    total[key]+=int(pop.one('size'));parts[n.key[2:],p.key.split(':',1)[-1]]+=int(pop.one('size'))
    return total,parts
def owner_map(text):
    out={}
    for n in b.walk(b.parse(text)):
        if n.key.startswith('s:STATE_'):
            for p in n.children('create_state'):
                for c in b.a.ids(p,'owned_provinces'):
                    c='x'+c.strip('"')[1:].upper()
                    out.setdefault(c,[]).append([n.key[2:],p.one('country').removeprefix('c:')])
    return out
def review_external():
    """Accept only the exact peer receipt chain, never a general file exemption."""
    peer=ROOT/'docs/reports/map/DURRANI_PUNJAB_1776/DP-02'
    captured=LOT/'external_snapshots/DP-02/CURRENT_RUNTIME_MANIFEST.json'
    manifest=json.loads((captured if captured.exists() else peer/'CURRENT_RUNTIME_MANIFEST.json').read_text('utf8'))
    base=load('BEFORE.json');rows=[]
    for r in manifest['files']:
        rel=r['file'];target=LOT/'apply_inputs'/rel if rel==STATES else ROOT/rel
        assert b.a.sha(target)==r['after_sha256'],('Peer output diverged',rel)
        if rel in base['protected']:assert base['protected'][rel]==r['before_sha256'],('Peer input diverged',rel)
        rows.append(dict(file=rel,before=r['before_sha256'],after=r['after_sha256']))
    # The two Nordic state nodes and all Nordic RGBs are unchanged by the peer.
    survey=b.a.raw(LOT/'survey_inputs'/STATES);immediate=b.a.raw(LOT/'apply_inputs'/STATES)
    for suffix in SIDS:
        sid='s:STATE_'+suffix
        for text in [survey,immediate]:b.one(text,sid)
        x=b.one(survey,sid);y=b.one(immediate,sid)
        assert survey[x.start:x.end]==immediate[y.start:y.end],sid
    sources={}
    for name in ['CURRENT_RUNTIME_MANIFEST.json','APPLIED.json','REPAIR_01.json','PLAN.json','REPORT.md','VALIDATION.json']:
        dest=LOT/'external_snapshots/DP-02'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():shutil.copy2(peer/name,dest)
        sources[name]=b.a.sha(dest)
    before=base['inventory']['owners'];im=owner_map(immediate)
    changes={c:dict(before=before.get(c),after=im.get(c)) for c in set(before)|set(im) if before.get(c)!=im.get(c)}
    assert len(changes)==81 and all(all(s in ['STATE_BALUCHISTAN','STATE_PUNJAB','STATE_HILL_PUNJAB','STATE_KASHMIR','STATE_HIMULAYA'] for s,t in z['after']) for z in changes.values()),'Review external owner scopes'
    save('EXTERNAL_COMPOSITION_REVIEW.json',dict(peer='DURRANI_PUNJAB_1776/DP-02',reviewed=rows,sources=sources,
        owner_changes=changes,shared_state_file_composed_from_current_version=True,functional_writes_by_review=0))
    print('Verified DP-02 outputs and 81 external owner changes; no functional write.')
def validate():
    base=load('BEFORE.json');inv=b4.inventory();old={r:b.a.raw(LOT/'apply_inputs'/r) for r in [STATES]+POPS}
    expected,ledger=transform(old);tests=[]
    def ck(name,ok,detail=None):tests.append(dict(check=name,passed=bool(ok),detail=detail))
    for rel,txt in expected.items():
        ck('exact_current_patch.'+rel,b.a.raw(ROOT/rel)==txt)
        ck('syntax.'+rel,bool(b.parse(b.a.raw(ROOT/rel))))
        def exterior(t):
            ops=[]
            for row in PLAN:
                matches=[n for n in b.walk(b.parse(t)) if n.key=='s:'+row['state']]
                for n in matches:ops.append((n.start,n.end,'<SCOPED_REGION>'))
            return b.edits(t,ops)
        ck('outside_two_scopes_unchanged.'+rel,exterior(old[rel])==exterior(b.a.raw(ROOT/rel)))
    # The immediate preimage includes a verified concurrent Indian installation.
    owners=owner_map(old[STATES])
    for row in PLAN:
        for c in row['rgb']:owners[c]=[[row['state'],row['recipient']]]
    ck('global_owners_exact_five_transfers_from_immediate_preimage',inv['owners']==owners)
    ck('global_population_conserved',inv['world_population']==base['inventory']['world_population'],inv['world_population'])
    ck('Git_identity_and_index_unchanged',inv['git']==base['inventory']['git'])
    ck('five_existing_provinces_no_new_TAG',sum(len(r['rgb']) for r in PLAN)==5)
    # All global demographic cohorts conserved; only two owner keys split.
    def cohorts(text):
        out=Counter()
        for pop in b.walk(b.parse(text)):
            if pop.key=='create_pop':out[pop.one('culture'),pop.one('religion'),pop.one('pop_type')]+=int(pop.one('size'))
        return out
    for rel in POPS:ck('cohort_totals_conserved.'+rel,cohorts(old[rel])==cohorts(b.a.raw(ROOT/rel)))
    cat=b.a.catalog('map_data/state_regions');states=b.a.raw(ROOT/STATES)
    img=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=img[:,:,0]*65536+img[:,:,1]*256+img[:,:,2]
    cells=[]
    for row in PLAN:
        sid=row['state'];reg,_=cat[sid];node=b.one(states,'s:'+sid);ids=[c.strip('"') for c in b.a.ids(reg,'provinces')]
        assigned=[c.strip('"') for p in node.children('create_state') for c in b.a.ids(p,'owned_provinces')]
        ck('unique_regional_assignment.'+sid,Counter(ids)==Counter(assigned))
        recipient=set(row['rgb']);neighbours=set()
        for c in row['rgb']:
            yy,xx=np.where(packed==int(c[1:],16));near=set()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:near.update(f'x{k:06X}' for k in np.unique(packed[yy+dy,xx+dx]))
            near.discard(c);neighbours.update(near)
            ck('registered_RGB_in_bitmap.'+c,bool(len(xx)))
            ck('single_RUS_assignment.'+c,inv['owners'][c]==[[sid,'RUS']])
            cells.append(dict(rgb=c,state=sid,before=row['donor'],after='RUS',pixels=len(xx),bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],adjacent=sorted(near)))
        ck('recipient_directly_touches_existing_Russia.'+sid,any(c not in recipient and any(t=='RUS' for _,t in inv['owners'].get(c,[])) for c in neighbours))
    differences=[]
    allowed={r['file'] for r in load('FILES_MODIFIED.json')}
    for rel,sha in base['protected'].items():
        if rel not in allowed and (not (ROOT/rel).exists() or b.a.sha(ROOT/rel)!=sha):differences.append(dict(file=rel,before=sha,after=b.a.sha(ROOT/rel) if (ROOT/rel).exists() else None))
    review=load('EXTERNAL_COMPOSITION_REVIEW.json') if (LOT/'EXTERNAL_COMPOSITION_REVIEW.json').exists() else dict(reviewed=[])
    reviewed=[dict(file=r['file'],before=r['before'],after=r['after']) for r in review['reviewed']]
    unreviewed=[r for r in differences if r not in reviewed]
    ck('no_unreviewed_external_change',not unreviewed,unreviewed)
    ck('exact_peer_receipt_outputs_still_preserved',all(b.a.sha(ROOT/r['file'])==r['after'] for r in reviewed if r['file']!=STATES))
    ck('peer_shared_state_preimage_preserved',not reviewed or b.a.sha(LOT/'apply_inputs'/STATES)==next(r['after'] for r in reviewed if r['file']==STATES))
    ck('SERG_tracking_and_territorial_files_unchanged',all(not r['file'].startswith('docs/reports/map/SERG_CLOSURE/') for r in differences))
    after,parts=demographics()
    save('POPULATION_LEDGER.json',dict(world_before=base['inventory']['world_population'],world_after=inv['world_population'],delta=0,
        allocation=ledger,portions_after=[dict(state=s,owner=t,population=n) for (s,t),n in parts.items() if s in [r['state'] for r in PLAN]],historical_recalibration=False))
    save('CELL_TRANSFERS.json',cells)
    save('CONCURRENT_CHANGES.json',dict(changes_outside_scope=differences,unreviewed=unreviewed,review='EXTERNAL_COMPOSITION_REVIEW.json',old_baseline_restored=False,Git_writes=0,vanilla_writes=0,SERG_writes=0))
    result=dict(status='PASS' if all(r['passed'] for r in tests) else 'FAIL',passed=sum(r['passed'] for r in tests),total=len(tests),checks=tests,runtime='NOT_RUN',human_validation=False)
    save('VALIDATION.json',result);print(result['status'],result['passed'],result['total']);return result['status']=='PASS'

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for flag in ['survey','inspect','apply','review-external','validate']:p.add_argument('--'+flag,action='store_true')
    a=p.parse_args()
    if a.survey:survey()
    if a.inspect:inspect()
    if a.apply:apply()
    if a.review_external:review_external()
    if a.validate:raise SystemExit(0 if validate() else 1)
