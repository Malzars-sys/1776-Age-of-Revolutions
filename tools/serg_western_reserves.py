"""Bounded western arbitration: Dutch Venlo/Beesel cores, no new HRE member."""
import collections
import difflib
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import serg_prussian_west as prior
from map2l_belgium import packed, components, allocate

ROOT, CANON = prior.ROOT, prior.CANON
OUT = CANON/'WESTERN_RESERVES_ARBITRATION_2026_11_05'
SID, PARENT = 'STATE_GELRE', 'x0000DF'
sha = prior.sha


def load(name):
    return json.loads((OUT/name).read_text(encoding='utf-8-sig'))


def dump(name, value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def geometry():
    assert prior.runtime()==load('BASELINE.json')['runtime']
    a=packed(OUT/'provinces_before.png'); z=a.copy(); t=load('TRACING.json')
    lots=[]; children=[]; rows=[]; moved=np.zeros(a.shape,dtype=bool)
    for i,lot in enumerate(t['sub_lots']):
        mask=np.zeros(a.shape,dtype=bool)
        for x,y in lot['cells']:
            assert a[y,x]==int(PARENT[1:],16) and not moved[y,x]
            mask[y,x]=True
        child='x'+format(0xEEC700+i,'06X')
        assert not (a==int(child[1:],16)).any() and len(components(mask))==1
        z[mask]=int(child[1:],16); moved|=mask
        children.append(dict(rgb=child,parent_rgb=PARENT))
        ys,xs=np.where(mask)
        rows.append(dict(rgb=child,parent_rgb=PARENT,state=SID,previous_owner='BEO',owner='NET',pixels=int(mask.sum()),cells=[[int(x),int(y)] for y,x in zip(ys,xs)]))
        lots.append(dict(id=lot['id'],pixels=int(mask.sum()),cells=rows[-1]['cells'],status='PREPARED_NOT_INSTALLED'))
    assert moved.sum()==8
    keep=(a==int(PARENT[1:],16))&~moved; ys,xs=np.where(keep)
    rows.insert(0,dict(rgb=PARENT,parent_rgb=PARENT,state=SID,previous_owner='BEO',owner='BEO',pixels=int(keep.sum()),cells=[[int(x),int(y)] for y,x in zip(ys,xs)]))
    assert keep.sum()==157 and len(components(keep))==1
    Image.fromarray(np.stack(((z>>16)&255,(z>>8)&255,z&255),axis=-1).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,
        parents=[PARENT],assignments=rows,new_provinces=children,ownership_cells=8,changed_pixels=8,sub_lots=lots,
        candidate_sha256=sha(OUT/'provinces_candidate.png'),hub_rebindings=[],all_other_parent_pixels_immutable=True,
        scope='Only Dutch cores; Prussian B72/B32, Roermond core, Cleves/Mark/Berg borders immutable'))
    render(); print('Prepared Dutch cores: Venlo 4, Beesel 4; BEO retained 157')


def render():
    b=load('BASELINE.json'); g=load('GEOMETRY.json')
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    afterowners=owners|{r['rgb']:r['owner'] for r in g['assignments']}
    colors={'PRU':(112,158,206),'BEO':(220,175,112),'NET':(225,199,75),'KPF':(189,160,208),'LGE':(205,130,130)}
    box=(4226,812,4242,829); scale=30; panels=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for title,path,own in [('AVANT',OUT/'provinces_before.png',owners),('APRES - B POLITIQUE',OUT/'provinces_candidate.png',afterowners)]:
        a=packed(path)[box[1]:box[3],box[0]:box[2]]; rgb=np.full((*a.shape,3),220,dtype=np.uint8)
        for v in np.unique(a):rgb[a==v]=colors.get(own.get('x'+format(int(v),'06X')),(220,220,220))
        im=Image.new('RGB',(480,580),'white'); im.paste(Image.fromarray(rgb).resize((480,510),Image.Resampling.NEAREST),(0,35));d=ImageDraw.Draw(im)
        d.text((8,8),title,font=font,fill='black');d.text((8,552),'Bleu PRU ; jaune NET ; ocre BEO',font=font,fill='black')
        for label,x,y in [('Venlo',4234.72,818.18),('Beesel',4231.74,821.33),('Roermond',4230.55,823.63)]:
            x=(x-box[0])*scale;y=(y-box[1])*scale+35;d.ellipse((x-2,y-2,x+2,y+2),fill='black');d.text((x+5,y+5),label,font=font,fill='black',stroke_width=1,stroke_fill='white')
        panels.append(im)
    im=Image.new('RGB',(960,580),'white');im.paste(panels[0]);im.paste(panels[1],(480,0))
    im.save(OUT/('BEFORE_AFTER.png' if (OUT/'INSTALLATION.json').exists() else 'BEFORE_CANDIDATE.png'))


def prepare():
    import validate_diplomacy_ottoman_1776 as cw
    import map2m_r9 as locators
    from map2b_patch import state,region,append
    from map2a_patch import edits
    from map_1776_audit import values
    from map2l_registry import active_registry_path
    b=load('BASELINE.json');g=load('GEOMETRY.json');assert prior.runtime()==b['runtime']
    before={};files={};allocations=[]
    def read(rel):
        raw=(ROOT/rel).read_bytes().decode('utf8')
        if rel in b['runtime']:assert sha(ROOT/rel)==b['runtime'][rel]
        before[rel]=raw;return raw.lstrip('\ufeff')
    children=[r['rgb'] for r in g['new_provinces']]
    rel='common/history/states/00_states.txt';raw=read(rel);n=state(raw,SID)
    net=next(z for z in n.children('create_state') if cw.scalar(z.one('country'))=='c:NET')
    beo=next(z for z in n.children('create_state') if cw.scalar(z.one('country'))=='c:BEO')
    assert values(beo,'owned_provinces')==[PARENT]
    f=net.children('owned_provinces')[0];files[rel]=edits(raw,[(f.end-1,f.end-1,' '+' '.join(children)+' ')])
    rel='map_data/state_regions/00_west_europe.txt';raw=read(rel);n=next(z for z in cw.parse(raw) if z.key==SID)
    f=n.children('provinces')[0];ops=[(f.end-1,f.end-1,' '+' '.join('"'+c+'"' for c in children)+' ')]
    a,z=packed(OUT/'provinces_before.png'),packed(OUT/'provinces_candidate.png')
    for kind in ['city','farm','mine','wood','port']:
        if not n.children(kind) or cw.scalar(n.one(kind))!=PARENT:continue
        loc=next(r for r in locators.locators(a) if r['Kind']==kind and r['ID']==int(n.one('id')))
        x,y=loc['X'],loc['Y'];assert a[int(y),int(x)]==z[int(y),int(x)],'Review a hub change separately'
    if PARENT in values(n,'prime_land'):
        f=n.children('prime_land')[0];ops.append((f.end-1,f.end-1,' '+' '.join('"'+c+'"' for c in children)+' '))
    files[rel]=edits(raw,ops)
    weights={'BEO':157,'NET':8}
    for rel in b['originals']:
        if '/pops/' not in rel:continue
        original=read(rel)
        try:n=region(original,SID,'BEO')
        except StopIteration:continue
        ops=[];pieces=[]
        for pop in n.children('create_pop'):
            f=pop.children('size')[0];count=int(f.value);amounts=allocate(count,weights)
            ops.append((f.start,f.end,'size = '+str(amounts['BEO'])))
            if amounts['NET']:pieces.append(edits(original[pop.start:pop.end],[(f.start-pop.start,f.end-pop.start,'size = '+str(amounts['NET']))]))
            allocations.append(dict(state=SID,file=rel,source='BEO',target='NET',profile=[pop.one('culture'),pop.one('religion','DEFAULT')],before=count,after=amounts))
        files[rel]=append(edits(original,ops),SID,'NET','\n'.join(pieces))
    assert sum(r['before'] for r in allocations)==24173
    assert not [r for r in b['inventory']['buildings'] if r['key'][:2]==[SID,'BEO']]
    rel='map_data/province_terrains.txt';raw=read(rel);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw+'\n'+'\n'.join(c+' = "'+terrain[PARENT.upper()]+'"' for c in children)+'\n'
    ledger=json.loads(active_registry_path().read_text(encoding='utf-8-sig'));dump('REGISTRY_BEFORE.json',ledger)
    previous=[r for r in ledger if r['state']==SID];removed=[c for lot in g['sub_lots'] for c in lot['cells']]
    dump('REGISTRY_MIGRATION.json',dict(replaced_regions=[SID],previous=previous,updated=previous,
        new_members=[],free_cities=[],country_additions={},new_provinces=g['new_provinces'],region_reference_changes=[],
        extent_added_cells=[],extent_removed_cells=removed,dutch_sovereign_cores_excluded_from_BEO_restitution=True,
        institutional_arbitration='Full Dutch sovereignty/generaliteitsland; omit these NET cores from the BEO restitution domain. No country-wide NET membership or doctrine about all Burgundian lands inferred.'))
    rel='tools/map2l_registry.py';raw=read(rel);anchor='    return result\n\ndef provincial_membership_overrides'
    if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
    assert raw.count(anchor)==1
    guard="""    western_reserves=ROOT/'docs/reports/map/SERG_CLOSURE/WESTERN_RESERVES_ARBITRATION_2026_11_05'
    if (western_reserves/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((western_reserves/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((western_reserves/'GEOMETRY.json').read_text(encoding='utf8'))
        assert gueldre in result
        assert m['replaced_regions']==['STATE_GELRE'] and m['previous']==m['updated']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==[] and m['country_additions']=={}
        assert m['dutch_sovereign_cores_excluded_from_BEO_restitution'] is True
        assert m['new_provinces']==g['new_provinces']==[{'rgb':'xEEC700','parent_rgb':'x0000DF'},{'rgb':'xEEC701','parent_rgb':'x0000DF'}]
        assert g['parents']==['x0000DF'] and g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==8
        assert [(z['id'],z['pixels']) for z in g['sub_lots']]==[('PW-VENLO-NET-B4',4),('PW-BEESEL-NET-B4',4)]
        removed=[c for z in g['sub_lots'] for c in z['cells']]
        assert sorted(m['extent_removed_cells'])==sorted(removed) and len({tuple(c) for c in removed})==8
        assert {(z['owner'],z['previous_owner'],z['state']) for z in g['assignments']}=={('BEO','BEO','STATE_GELRE'),('NET','BEO','STATE_GELRE')}
        assert not {'xEEC700','xEEC701'} & {z['rgb'] for z in m['updated']}
        result.append(western_reserves)
"""
    if '\r\n' in raw:guard=guard.replace('\n','\r\n')
    files[rel]=raw.replace(anchor,guard+anchor)
    for rel,text in list(files.items()):
        old=before[rel]
        if old.startswith('\ufeff'):text='\ufeff'+text.lstrip('\ufeff')
        if '\r\n' in old and old.count('\n')==old.count('\r\n'):text=text.replace('\r\n','\n').replace('\n','\r\n')
        oldlines,newlines,parts=old.splitlines(True),text.splitlines(True),[]
        for op,i,j,k,l in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
            lines=newlines[k:l]
            if op!='equal':lines=[line if line.strip() else ('\r\n' if line.endswith('\r\n') else '\n') for line in lines]
            parts.extend(lines)
        files[rel]=''.join(parts)
        if rel.endswith('.txt'):cw.parse(files[rel].lstrip('\ufeff'))
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files)
    dump('PLAN.json',dict(files=sorted(files),population_allocations=allocations,weights=weights,moved_population=sum(r['after']['NET'] for r in allocations),
        population_method='Technical exact-integer redistribution of existing BEO/Gelre profiles, not a census',buildings_units_technologies_unchanged=True,runtime_installed=False))
    print('Prepared',len(files),'text files; population to NET',sum(r['after']['NET'] for r in allocations))


def compile_prepare():
    import serg_prussia_v1 as core
    core.OUT=OUT;core.compile_prepare()


def install():
    import serg_prussia_v1 as core
    assert prior.runtime()==load('BASELINE.json')['runtime'],'Reconcile functional concurrency before installation'
    core.OUT=OUT;core.install()


def verify():
    import validate_map2a as qa
    import map2l_registry as reg
    import validate_diplomacy_ottoman_1776 as cw
    reg=importlib.reload(reg)
    b,g=load('BASELINE.json'),load('GEOMETRY.json');inv=qa.inventory();dump('INVENTORY_AFTER.json',inv)
    a,z=packed(OUT/'provinces_before.png'),packed(ROOT/'map_data/provinces.png');checks=[]
    def ck(n,v):checks.append(dict(name=n,status='PASS' if v else 'FAIL'))
    expected=load('EXPECTED_TEXT.json');changed={r['file'] for r in load('INSTALLATION.json')['changes']};now=prior.runtime()
    ck('all_prepared_text_installed',all((ROOT/p).read_bytes().decode('utf8')==raw for p,raw in expected.items()))
    ck('all_other_functional_files_preserved',{p:h for p,h in now.items() if p not in changed}=={p:h for p,h in b['runtime'].items() if p not in changed})
    ck('bitmap_exact',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
    wanted={tuple(c) for lot in g['sub_lots'] for c in lot['cells']};ys,xs=np.where(a!=z)
    ck('exactly_eight_reviewed_cells_changed',len(wanted)==8 and set(zip(xs.tolist(),ys.tolist()))==wanted)
    for row in g['assignments']:
        ys,xs=np.where(z==int(row['rgb'][1:],16));ck('geometry_'+row['rgb'],set(zip(xs.tolist(),ys.tolist()))=={tuple(c) for c in row['cells']})
    ownership=qa.counter(b['inventory']['owners']).copy()
    for r in g['new_provinces']:ownership[r['rgb'],SID,'NET']+=1
    ck('worldwide_ownership_exact_delta',qa.counter(inv['owners'])==ownership)
    ck('all_non_parent_pixels_preserved',np.array_equal(a[a!=int(PARENT[1:],16)],z[a!=int(PARENT[1:],16)]))
    ck('retained_BEO_connected',len(components(z==int(PARENT[1:],16)))==1)
    for rgb in ['xEEC600','xEEC400','xEEC401','xEEC402']:
        mask=a==int(rgb[1:],16);ck('previous_PRU_core_'+rgb,np.array_equal(a[mask],z[mask]) and int((a==int(rgb[1:],16)).sum())==int((z==int(rgb[1:],16)).sum()))
    for field in ['pops','resolved_demographics','buildings','building_levels_written','units','countries','states','state_types','errors','duplicates']:
        ck('inventory_'+field+'_preserved',inv[field]==b['inventory'][field])
    populations=qa.counter(b['inventory']['regional_pop']).copy()
    for r in load('PLAN.json')['population_allocations']:
        culture,religion=r['profile'];religion='DEFAULT:'+culture if religion=='DEFAULT' else religion;culture,religion=culture.strip('"'),religion.strip('"')
        amount=r['after']['NET'];populations[SID,'BEO',culture,religion]-=amount;populations[SID,'NET',culture,religion]+=amount
    ck('regional_population_exact_redistribution',+qa.counter(inv['regional_pop'])==+populations)
    ledger=json.loads(reg.active_registry_path().read_text(encoding='utf-8-sig'));old=load('REGISTRY_BEFORE.json')
    ck('599_imperial_titles_unchanged',ledger==old and len(ledger)==599)
    oldmask=np.isin(a,[int(r['rgb'][1:],16) for r in old]);newmask=np.isin(z,[int(r['rgb'][1:],16) for r in ledger]);ys,xs=np.where(oldmask&~newmask)
    ck('exactly_eight_cells_removed_from_BEO_imperial_domain',set(zip(xs.tolist(),ys.tolist()))==wanted and not (newmask&~oldmask).any())
    ck('no_NET_title_or_national_membership','NET' not in {r['beneficiary'] for r in ledger} and 'NET' not in reg.additional_members() and 'NET' not in reg.territorial_holder_overrides())
    ck('explicit_migration_chain',reg.approved_lot_dirs()[-1]==OUT)
    from map2k_patch import ELECTORS
    ck('nine_electors_unchanged',len(ELECTORS)==9)
    ck('no_hub_or_physical_locator_change',not g['hub_rebindings'] and not any('/map_object_data/' in p for p in changed))
    ck('no_building_country_military_technology_changes',not any(any(s in p for s in ['/buildings/','/countries/','/military','/technology/','/production_methods/']) for p in changed))
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))}
    ck('terrains_inherited',all(terrain[r['rgb'].upper()]==terrain[PARENT.upper()] for r in g['new_provinces']))
    protected=dict(b['protected'])
    for p in OUT.glob('PROTECT_*.json'):protected.update(load(p.name))
    ck('all_prior_proofs_and_approvals_preserved',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in protected.items()))
    for label,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        value=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip();ck('git_'+label+'_unchanged',value==b['git'][label])
    ck('git_index_unchanged',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    for p,raw in expected.items():
        if p.endswith('.txt'):cw.parse(raw.lstrip('\ufeff'))
    ck('changed_scripts_parse',True)
    result=dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),inherited_errors=inv['errors'],inherited_duplicates=inv['duplicates'],moved_population=load('PLAN.json')['moved_population'],engine_test=False,human_attestation=None)
    dump('VALIDATION.json',result);print('Validation',result['passed'],'/',result['total'],[c for c in checks if c['status']!='PASS']);assert result['status']=='PASS'


if __name__=='__main__':
    {'geometry':geometry,'prepare':prepare,'compile':compile_prepare,'install':install,'verify':verify,'render':render}[sys.argv[1]]()
