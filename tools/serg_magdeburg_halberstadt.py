"""Bounded Magdeburg/Saale continuation; no Git or vanilla writes."""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import serg_prussian_west as prior
from georeference.model import forward
from map2l_belgium import packed, components, allocate
from map2l_franconia import inside

ROOT = prior.ROOT
CANON = prior.CANON
OUT = CANON / 'MAGDEBURG_HALBERSTADT_2026_11_05'
REGIONS = {'STATE_ANHALT'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def trace():
    """New western reading of the source; the native Miller model stays frozen."""
    model_path = ROOT / 'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json'
    model = json.loads(model_path.read_text())['model']
    towns = {r['name']: r for r in load('TOWN_DIAGNOSTICS.json')['rows']}
    # Source coordinates use the existing 3000-pixel reproduction's scale.
    # The new 6000-pixel reproduction is inspected at twice those coordinates.
    readings = [
        ('Magdeburg', 710, 216, 'FIT'), ('Bernburg', 873, 510, 'FIT'),
        ('Dessau', 1086, 476, 'FIT'), ('Halle (Saale)', 980, 731, 'FIT'),
        ('Querfurt', 766, 879, 'FIT'), ('Naumburg', 870, 1050, 'FIT'),
        ('Merseburg', 974, 850, 'CHECK'), ('Weißenfels', 990, 975, 'CHECK'),
        ('Gommern', 874, 240, 'CHECK'), ('Barby', 852, 350, 'CHECK')]
    fitted = [r for r in readings if r[3] == 'FIT']
    design = np.array([[x, y, 1] for _, x, y, _ in fitted])
    target = forward(model, [towns[n]['geo'] for n, _, _, _ in fitted])
    matrix = np.linalg.lstsq(design, target, rcond=None)[0]
    rows = []
    for name, x, y, role in readings:
        native = np.array([x, y, 1]) @ matrix
        reference = forward(model, [towns[name]['geo']])[0]
        rows.append(dict(name=name, source_pixel=[x, y], role=role, native_pixel=native.tolist(),
            reference_native=reference.tolist(), residual_pixels=float(np.linalg.norm(native-reference)),
            native_city_position_certified=False, geonames_id=towns[name]['geonames_id']))
    # A regional political core: Merseburg/Querfurt/Weissenfels/Naumburg.
    # The north edge excludes Halle and the unarbitrated Mansfeld county.
    saale = [(748,863),(794,852),(830,849),(854,839),(870,819),(893,800),
        (927,792),(954,804),(977,814),(1008,815),(1035,808),(1060,815),
        (1150,815),(1150,1110),(946,1110),(916,1098),(899,1077),(872,1056),
        (868,1031),(879,1009),(853,984),(829,963),(806,940),(778,917),(753,899)]
    gommern = [(785,211),(815,205),(843,208),(864,218),(900,227),(940,239),
        (974,242),(994,239),(992,270),(971,281),(953,296),(929,300),
        (910,284),(885,274),(861,265),(838,269),(813,263),(801,252),(782,248)]
    polys = {name: (np.c_[poly, np.ones(len(poly))] @ matrix).tolist()
             for name, poly in [('MH-SAALE-CORE', saale), ('MH-GOMMERN-CORE', gommern)]}
    dump('TRACING.json', dict(source='Schenk 1758, Bern MUE Ryh 5301:30; e-rara-124790',
        source_image='EVIDENCE/SCHENK_1758_6000.jpg', source_sha256=sha(OUT/'EVIDENCE/SCHENK_1758_6000.jpg'),
        source_coordinate_scale=[3000,2376], actual_reproduction=[6000,4753],
        source_to_native_matrix=matrix.tolist(), readings=rows,
        source_outlines={'MH-SAALE-CORE':saale,'MH-GOMMERN-CORE':gommern}, native_outlines=polys,
        native_model=model_path.relative_to(ROOT).as_posix(), native_model_sha256=sha(model_path),
        native_model_unchanged=True, previous_north_saxony_trace_unchanged=True,
        classification='B_POLITICAL_GENERALISATION', historical_cadastral_precision=False,
        controls_are_source_readings_not_ground_truth=True,
        scope='Only current PRU cells in the reviewed parents; Anhalt and all other non-PRU cells immutable.'))
    im=Image.open(OUT/'EVIDENCE/SCHENK_1758_6000.jpg').convert('RGB')
    draw=ImageDraw.Draw(im)
    for poly, color in [(saale,'blue'),(gommern,'red')]:
        draw.line([(x*2,y*2) for x,y in poly+[poly[0]]], fill=color, width=5)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    for row in rows:
        x,y=row['source_pixel'];x*=2;y*=2
        draw.ellipse((x-5,y-5,x+5,y+5),fill='red' if row['role']=='FIT' else 'green')
        draw.text((x+7,y+5),row['name']+' '+row['role'],font=font,fill='black',stroke_width=2,stroke_fill='white')
    im.crop((1300,300,2360,2270)).resize((954,1773)).save(OUT/'SOURCE_TRACE_REVIEW.jpg')
    for row in rows:print(row['name'],row['role'],round(row['residual_pixels'],2))


def geometry():
    b=load('BASELINE.json');assert prior.runtime()==b['runtime'], 'Reassess concurrent functional changes'
    a=packed(OUT/'provinces_before.png');g=load('TRACING.json')
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    yy,xx=np.mgrid[790:835,4345:4390]
    selected=np.zeros(a.shape,dtype=bool);lots=[]
    for name,poly in g['native_outlines'].items():
        mask=inside(np.c_[(xx+.5).ravel(),(yy+.5).ravel()],np.array(poly)).reshape(xx.shape)
        permitted={'x618061','xCF5D8E'} if name=='MH-SAALE-CORE' else {'xA080E0'}
        local=mask & np.isin(a[790:835,4345:4390],[int(rgb[1:],16) for rgb in permitted])
        chosen=np.zeros(a.shape,dtype=bool);chosen[790:835,4345:4390]=local
        assert not (selected&chosen).any()
        selected|=chosen
        ys,xs=np.where(chosen);lots.append(dict(id=name,cells=[[int(x),int(y)] for y,x in zip(ys,xs)],pixels=int(chosen.sum()),status='PREPARED_NOT_INSTALLED'))
    after=a.copy();assignments=[];children=[]
    for idx,value in enumerate(sorted(np.unique(a[selected]))):
        parent='x'+format(int(value),'06X');sid,tag=owners[parent]
        assert sid=='STATE_ANHALT' and tag=='PRU'
        moved=(a==value)&selected;retained=(a==value)&~selected
        assert retained.any() and moved.any(), 'Review whole-parent transfers separately'
        child='x'+format(0xEEC500+idx,'06X');assert not (a==int(child[1:],16)).any()
        after[moved]=int(child[1:],16);children.append(dict(rgb=child,parent_rgb=parent))
        for rgb,owner,mask in [(parent,'PRU',retained),(child,'SAX',moved)]:
            ys,xs=np.where(mask);assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=tag,owner=owner,
                pixels=int(mask.sum()),cells=[[int(x),int(y)] for y,x in zip(ys,xs)],components_4=sorted([len(z) for z in components(mask)],reverse=True)))
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=-1).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,
        parents=sorted({r['parent_rgb'] for r in assignments}),assignments=assignments,new_provinces=children,
        hub_rebindings=[],ownership_cells=int(selected.sum()),changed_pixels=int((a!=after).sum()),
        candidate_sha256=sha(OUT/'provinces_candidate.png'),sub_lots=lots,all_non_prussian_cells_immutable=True,
        excluded=['Barby portions already held in approved Anhalt cores','Mansfeld county sovereignty and 1780 succession','Quedlinburg and other microstates','Erfurt/Eichsfeld','Glatz/Silesia','Other Prussian frontiers']))
    render()
    print('Candidate',int(selected.sum()),'PRU -> SAX;',[(z['id'],z['pixels']) for z in lots])


def render():
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=packed(OUT/'provinces_before.png');after=packed(OUT/'provinces_candidate.png')
    own={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};changed=own|{r['rgb']:r['owner'] for r in g['assignments']}
    box=(4350,790,4386,834);scale=18;panels=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    colors={'PRU':(115,160,205),'SAX':(157,191,113),'ANH':(238,176,108),'ABG':(240,146,80),'AKT':(238,191,150),'AZR':(228,123,102),'WEI':(239,185,197),'SSO':(200,165,185)}
    for title,a,owners in [('AVANT',before,own),('APRES INSTALLE' if (OUT/'INSTALLATION.json').exists() else 'CANDIDAT B - NON INSTALLE',after,changed)]:
        local=a[box[1]:box[3],box[0]:box[2]];rgb=np.full((*local.shape,3),215,np.uint8)
        for val in np.unique(local):rgb[local==val]=colors.get(owners.get('x'+format(int(val),'06X')),(210,210,210))
        im=Image.new('RGB',(648,860),'white');im.paste(Image.fromarray(rgb).resize((648,792),Image.Resampling.NEAREST),(0,38));d=ImageDraw.Draw(im);d.text((8,8),title,font=font,fill='black');d.text((8,836),'Bleu PRU ; vert SAX ; noyaux Anhalt conserves',font=font,fill='black');panels.append(im)
    im=Image.new('RGB',(1296,860),'white');im.paste(panels[0]);im.paste(panels[1],(648,0));im.save(OUT/('BEFORE_AFTER.png' if (OUT/'INSTALLATION.json').exists() else 'BEFORE_CANDIDATE.png'))
    rows=[]
    for row in load('TOWN_DIAGNOSTICS.json')['rows']:
        row=dict(row);x,y=row['Miller']['pixel'];rgb='x'+format(int(after[int(y),int(x)]),'06X');row['candidate_rgb']=rgb;row['candidate_owner']=changed.get(rgb);rows.append(row)
    dump('TOWN_DIAGNOSTICS_CANDIDATE.json',dict(rows=rows,positions_certified=False))
    print('Coarse town readings:',[(r['name'],r['Miller']['state_owner'][1],r['candidate_owner']) for r in rows if r['name'] in ['Halle (Saale)','Magdeburg','Halberstadt','Merseburg','Naumburg','Querfurt','Gommern','Barby']])


def prepare():
    import validate_diplomacy_ottoman_1776 as cw
    from map_1776_audit import values
    from map2a_patch import edits
    from map2b_patch import state,region,append
    from map2l_registry import active_registry_path
    import map2m_r9 as locators
    b=load('BASELINE.json');g=load('GEOMETRY.json')
    assert prior.runtime()==b['runtime']
    assert g['ownership_cells']==77 and len(g['new_provinces'])==3
    a=packed(OUT/'provinces_before.png');candidate=packed(OUT/'provinces_candidate.png')
    before={};files={};allocations=[]
    def read(rel):
        raw=(ROOT/rel).read_bytes().decode('utf-8')
        if rel in b['runtime']:assert sha(ROOT/rel)==b['runtime'][rel],rel
        before[rel]=raw
        return raw.lstrip('\ufeff')
    rel='common/history/states/00_states.txt';raw=read(rel)
    n=state(raw,'STATE_ANHALT')
    for tag in ['PRU','SAX']:
        node=next(z for z in n.children('create_state') if cw.scalar(z.one('country'))=='c:'+tag)
        if tag=='PRU':assert set(g['parents'])<=set(values(node,'owned_provinces'))
    sax=next(z for z in n.children('create_state') if cw.scalar(z.one('country'))=='c:SAX')
    field=sax.children('owned_provinces')[0]
    raw=edits(raw,[(field.end-1,field.end-1,' '+' '.join(r['rgb'] for r in g['new_provinces'])+' ')])
    files[rel]=raw
    rel='map_data/state_regions/00_west_europe.txt';raw=read(rel)
    n=next(z for z in cw.parse(raw) if z.key=='STATE_ANHALT');field=n.children('provinces')[0]
    ops=[(field.end-1,field.end-1,' '+' '.join('"'+r['rgb']+'"' for r in g['new_provinces'])+' ')]
    locs=locators.locators(a)
    for kind in ['city','farm','mine','wood','port']:
        fields=n.children(kind)
        if not fields:continue
        parent=cw.scalar(fields[0].value)
        if parent not in g['parents']:continue
        point=next(r for r in locs if r['Kind']==kind and r['ID']==int(n.one('id')))
        x,y=point['X'],point['Y'];actual='x'+format(int(candidate[int(y),int(x)]),'06X')
        assert 'x'+format(int(a[int(y),int(x)]),'06X')==parent
        if actual!=parent:
            ops.append((fields[0].start,fields[0].end,kind+' = "'+actual+'"'))
            g['hub_rebindings'].append(dict(state='STATE_ANHALT',field=kind,before=parent,after=actual,point=[x,y],locator_moved=False))
    if n.children('prime_land'):
        field=n.children('prime_land')[0];primes=set(values(n,'prime_land'))
        added=[r['rgb'] for r in g['new_provinces'] if r['parent_rgb'] in primes]
        if added:ops.append((field.end-1,field.end-1,' '+' '.join('"'+rgb+'"' for rgb in added)+' '))
    files[rel]=edits(raw,ops)
    total=sum(int((a==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_ANHALT','PRU'])
    weights={'PRU':total-g['ownership_cells'],'SAX':g['ownership_cells']}
    for rel in b['originals']:
        if '/pops/' not in rel:continue
        original=read(rel)
        try:n=region(original,'STATE_ANHALT','PRU')
        except StopIteration:continue
        ops=[];pieces=[]
        for pop in n.children('create_pop'):
            size=pop.children('size')[0];count=int(size.value);amounts=allocate(count,weights)
            ops.append((size.start,size.end,'size = '+str(amounts['PRU'])))
            if amounts['SAX']:
                fragment=original[pop.start:pop.end]
                pieces.append(edits(fragment,[(size.start-pop.start,size.end-pop.start,'size = '+str(amounts['SAX']))]))
            allocations.append(dict(file=rel,state='STATE_ANHALT',source='PRU',target='SAX',profile=[pop.one('culture'),pop.one('religion','DEFAULT')],before=count,after=amounts))
        raw=edits(original,ops)
        if pieces:raw=append(raw,'STATE_ANHALT','SAX','\n'.join(pieces))
        if raw!=original:files[rel]=raw
    rel='map_data/province_terrains.txt';raw=read(rel)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    for row in g['new_provinces']:raw+='\n'+row['rgb']+' = "'+terrain[row['parent_rgb'].upper()]+'"'
    files[rel]=raw+'\n'
    rel=active_registry_path().relative_to(ROOT).as_posix();ledger=json.loads(read(rel));previous=[r for r in ledger if r['state']=='STATE_ANHALT']
    assert len(ledger)==595 and set(g['parents'])<={r['rgb'] for r in previous}
    added=[dict(rgb=r['rgb'],state='STATE_ANHALT',beneficiary='SAX',basis='Schenk 1758 and Saxon archival chronology; partial Saale/Gommern political B cores; MAGDEBURG_HALBERSTADT_2026_11_05/REPORT.md') for r in g['new_provinces']]
    files[rel]=json.dumps(sorted(ledger+added,key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    migration=dict(replaced_regions=['STATE_ANHALT'],previous=previous,updated=previous+added,new_members=[],free_cities=[],country_additions={},new_provinces=g['new_provinces'],region_reference_changes=g['hub_rebindings'],extent_added_cells=[],extent_removed_cells=[])
    dump('REGISTRY_MIGRATION.json',migration)
    rel='tools/map2l_registry.py';raw=read(rel);anchor='    return result\n\ndef provincial_membership_overrides'
    if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
    assert raw.count(anchor)==1
    guard="""    magdeburg=ROOT/'docs/reports/map/SERG_CLOSURE/MAGDEBURG_HALBERSTADT_2026_11_05'
    if (magdeburg/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((magdeburg/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((magdeburg/'GEOMETRY.json').read_text(encoding='utf8'))
        assert prussian_west in result
        assert m['replaced_regions']==['STATE_ANHALT']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==77
        assert set(g['parents'])=={'x618061','xA080E0','xCF5D8E'}
        assert len(g['new_provinces'])==3 and sum(z['pixels'] for z in g['sub_lots'])==77
        assert all(z['previous_owner']=='PRU' and z['owner'] in {'PRU','SAX'} and z['state']=='STATE_ANHALT' for z in g['assignments'])
        old={z['rgb']:z for z in m['previous']};new={z['rgb']:z for z in m['updated']}
        assert all(new[k]==v for k,v in old.items()) and len(new)==len(old)+3
        assert {(z['rgb'],z['beneficiary']) for z in m['updated'] if z['rgb'] not in old}=={(z['rgb'],'SAX') for z in g['new_provinces']}
        result.append(magdeburg)
"""
    if '\r\n' in raw:guard=guard.replace('\n','\r\n')
    files[rel]=raw.replace(anchor,guard+anchor)
    # Preserve all old bytes outside edits, UTF-8 BOMs and per-file newlines.
    for rel,text in list(files.items()):
        old=before[rel]
        if old.startswith('\ufeff'):text='\ufeff'+text.lstrip('\ufeff')
        if '\r\n' in old and old.count('\n')==old.count('\r\n'):text=text.replace('\r\n','\n').replace('\n','\r\n')
        oldlines=old.splitlines(True);newlines=text.splitlines(True);parts=[]
        for op,i,j,k,l in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
            lines=newlines[k:l]
            if op!='equal':lines=[line if line.strip() else ('\r\n' if line.endswith('\r\n') else '\n') for line in lines]
            parts.extend(lines)
        text=''.join(parts)
        if rel.endswith('.txt'):cw.parse(text.lstrip('\ufeff'))
        files[rel]=text
    dump('GEOMETRY.json',g);dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files)
    dump('PLAN.json',dict(files=sorted(files),population_allocations=allocations,weights=weights,
        moved_population=sum(z['after']['SAX'] for z in allocations),
        population_method='Technical exact-integer redistribution of existing PRU state profiles, not a historical 1776 census',
        buildings_units_technologies_unchanged=True,runtime_installed=False))
    print('Prepared',len(files),'text files; population moved',sum(z['after']['SAX'] for z in allocations),'hubs',g['hub_rebindings'])


def compile_prepare():
    import serg_prussia_v1 as core
    core.OUT=OUT;core.compile_prepare()


def install():
    import serg_prussia_v1 as core
    assert prior.runtime()==load('BASELINE.json')['runtime'], 'Reassess concurrent functional changes before installation'
    core.OUT=OUT;core.install()


def verify():
    import subprocess
    import validate_map2a as qa
    import map2l_registry as reg
    import validate_diplomacy_ottoman_1776 as cw
    b=load('BASELINE.json');g=load('GEOMETRY.json');installation=load('INSTALLATION.json');expected=load('EXPECTED_TEXT.json')
    a=packed(OUT/'provinces_before.png');z=packed(ROOT/'map_data/provinces.png');inv=qa.inventory();dump('INVENTORY_AFTER.json',inv)
    checks=[]
    def ck(name,value):checks.append(dict(name=name,status='PASS' if value else 'FAIL'))
    changed={row['file'] for row in installation['changes']};runtime=prior.runtime()
    ck('prepared_text_installed_exactly',all((ROOT/p).read_bytes().decode('utf-8')==text for p,text in expected.items()))
    ck('all_other_functional_files_preserved',{p:h for p,h in runtime.items() if p not in changed}=={p:h for p,h in b['runtime'].items() if p not in changed})
    ck('bitmap_exactly_reviewed',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
    ck('exactly_77_changed_cells',int((a!=z).sum())==77)
    wanted={(x,y) for row in g['sub_lots'] for x,y in row['cells']};ys,xs=np.where(a!=z)
    ck('only_documented_cells_changed',set(zip(xs.tolist(),ys.tolist()))==wanted)
    owners={r['key'][0]:r['key'][2] for r in inv['owners']};oldowners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    ck('all_transferred_cells_SAX',all(owners['x'+format(int(z[y,x]),'06X')]=='SAX' for x,y in wanted))
    nonpru=np.isin(a,[int(rgb[1:],16) for rgb,tag in oldowners.items() if tag!='PRU'])
    ck('all_non_prussian_nuclei_preserved',np.array_equal(a[nonpru],z[nonpru]))
    for row in g['assignments']:
        ys,xs=np.where(z==int(row['rgb'][1:],16))
        ck('exact_geometry_'+row['rgb'],set(zip(xs.tolist(),ys.tolist()))=={tuple(v) for v in row['cells']})
    ck('all_three_children_unique',len(g['new_provinces'])==3 and all(next(r['count'] for r in inv['owners'] if r['key'][0]==v['rgb'])==1 for v in g['new_provinces']))
    ownership=qa.counter(b['inventory']['owners']).copy()
    for row in g['new_provinces']:ownership[row['rgb'],'STATE_ANHALT','SAX']+=1
    ck('worldwide_ownership_exact_delta',qa.counter(inv['owners'])==ownership)
    for field in ['pops','resolved_demographics','buildings','building_levels_written','units','countries','states','state_types']:
        ck('inventory_'+field+'_preserved',inv[field]==b['inventory'][field])
    ck('inherited_reference_errors_unchanged',inv['errors']==b['inventory']['errors'])
    ck('inherited_duplicate_debt_unchanged',inv['duplicates']==b['inventory']['duplicates'])
    ck('global_population_preserved',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in b['inventory']['pops']))
    beforepop=qa.counter(b['inventory']['regional_pop']);afterpop=qa.counter(inv['regional_pop'])
    wantedpop=beforepop.copy()
    for row in load('PLAN.json')['population_allocations']:
        culture,religion=row['profile'];religion='DEFAULT:'+culture if religion=='DEFAULT' else religion
        culture=culture.strip('"');religion=religion.strip('"')
        amount=row['after']['SAX'];wantedpop['STATE_ANHALT','PRU',culture,religion]-=amount;wantedpop['STATE_ANHALT','SAX',culture,religion]+=amount
    ck('regional_population_exact_declared_redistribution',+afterpop==+wantedpop)
    oldledger=json.loads(load('TEXT_BEFORE.json')[reg.active_registry_path().relative_to(ROOT).as_posix()]);ledger=json.loads(reg.active_registry_path().read_text(encoding='utf-8-sig'));newrows={r['rgb']:r for r in ledger}
    ck('registry_595_to_598_unique',len(oldledger)==595 and len(ledger)==len(newrows)==598)
    ck('all_previous_imperial_titles_preserved',all(newrows[r['rgb']]==r for r in oldledger))
    ck('new_titles_only_SAX',all(newrows[r['rgb']]['beneficiary']=='SAX' for r in g['new_provinces']))
    ck('imperial_physical_extent_unchanged',np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in oldledger]),np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    ck('explicit_migration_chain_appended',reg.approved_lot_dirs()[-1]==OUT)
    from map2k_patch import ELECTORS
    ck('nine_electors_unchanged',len(ELECTORS)==9)
    for row in g['hub_rebindings']:
        x,y=row['point'];ck('hub_reference_'+row['field'],int(z[int(y),int(x)])==int(row['after'][1:],16) and not row['locator_moved'])
    ck('all_physical_locators_preserved',not any('/map_object_data/' in p for p in changed))
    ck('no_building_country_military_technology_changes',not any(any(s in p for s in ['/buildings/','/countries/','/military','/technology/','/production_methods/']) for p in changed))
    protected=dict(b['protected'])
    for p in OUT.glob('PROTECT_*.json'):protected.update(load(p.name))
    ck('all_prior_evidence_and_Glatz_approval_preserved',all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in protected.items()))
    selected={'Merseburg':'SAX','Querfurt':'SAX','Naumburg':'SAX','Weißenfels':'SAX','Gommern':'SAX','Halle (Saale)':'PRU','Magdeburg':'PRU','Halberstadt':'PRU'}
    towns={r['name']:r for r in load('TOWN_DIAGNOSTICS_CANDIDATE.json')['rows']}
    ck('coarse_town_diagnostics_consistent_not_certified',all(towns[name]['candidate_owner']==tag for name,tag in selected.items()))
    for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        val=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip();ck('git_'+name+'_preserved',val==b['git'][name])
    ck('git_index_preserved',sha(Path(b['git']['git_dir'])/'index')==b['git']['index_sha256'])
    for rel,text in expected.items():
        if rel.endswith('.txt'):cw.parse(text.lstrip('\ufeff'))
    ck('changed_scripts_parse',True)
    dump('VALIDATION.json',dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',checks=checks,passed=sum(c['status']=='PASS' for c in checks),total=len(checks),global_written_population=sum(r['count'] for r in inv['pops']),moved_population=load('PLAN.json')['moved_population'],inherited_errors=inv['errors'],inherited_duplicates=inv['duplicates'],engine_test=False,human_attestation=None))
    print('Validation',len(checks),'checks; failures',[c for c in checks if c['status']!='PASS']);assert all(c['status']=='PASS' for c in checks)


if __name__=='__main__':
    {'trace':trace,'geometry':geometry,'render':render,'prepare':prepare,'compile':compile_prepare,'install':install,'verify':verify}[sys.argv[1]]()
