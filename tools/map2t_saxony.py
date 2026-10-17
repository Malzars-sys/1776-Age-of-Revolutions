"""MAP-2T: bounded Saxon/Thuringian reconstruction with immutable capture."""
import collections as C
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
import map2r_anhalt as prior

q = prior.q
core = q.core
ROOT = prior.ROOT
OUT = ROOT / 'docs/reports/map/MAP2T'
SID = 'STATE_SAXONY'
OLD_TAGS = ['SAX', 'WEI', 'MEI', 'COB', 'SCW']
NEW_TAGS = ['GOT','HIL','SSO','RGZ','RGE','RSL']
NAMES = {
 'SAX':('Electorate of Saxony','Électorat de Saxe'),
 'WEI':('Saxe-Weimar-Eisenach','Saxe-Weimar-Eisenach'),
 'MEI':('Saxe-Meiningen','Saxe-Meiningen'),
 'COB':('Saxe-Coburg-Saalfeld','Saxe-Cobourg-Saalfeld'),
 'SCW':('Schwarzburg-Rudolstadt','Schwarzbourg-Rudolstadt'),
 'GOT':('Saxe-Gotha-Altenburg','Saxe-Gotha-Altenbourg'),
 'HIL':('Saxe-Hildburghausen','Saxe-Hildburghausen'),
 'SSO':('Schwarzburg-Sondershausen','Schwarzbourg-Sondershausen'),
 'RGZ':('County of Reuss-Greiz','Comté de Reuss-Greiz'),
 'RGE':('County of Reuss-Gera','Comté de Reuss-Gera'),
 'RSL':('County of Reuss-Schleiz','Comté de Reuss-Schleiz')}

# Deliberately inward, generalized cores on SOURCE_OVERVIEW.png (1800px wide).
# Not a complete polygon census and not 1905 red administrative boundaries.
TRACES = [
 ('GOT','Gotha',[(370,483),(421,477),(461,487),(503,487),(553,492),(568,524),(540,545),(526,570),(548,600),(544,630),(520,650),(489,685),(471,725),(494,760),(506,777),(483,790),(451,773),(429,739),(391,724),(373,684),(368,635)]),
 ('GOT','Altenburg',[(1213,489),(1267,481),(1310,502),(1327,537),(1297,573),(1260,585),(1224,569),(1198,539)]),
 ('GOT','Roda',[(893,597),(938,596),(966,610),(996,607),(998,638),(1020,657),(1001,670),(957,666),(941,688),(915,684),(906,670),(878,665),(875,638)]),
 ('HIL','Hildburghausen',[(423,897),(478,899),(490,884),(514,897),(548,889),(562,906),(581,911),(587,930),(577,961),(554,972),(504,962),(465,946),(438,941),(425,925)]),
 ('SSO','Arnstadt',[(584,654),(615,653),(638,674),(627,694),(589,700),(575,686)]),
 ('SSO','Gehren',[(585,785),(598,771),(610,775),(621,789),(636,789),(656,808),(643,830),(646,847),(633,867),(622,885),(603,891),(590,878),(587,850),(590,827)]),
 ('RGZ','Greiz',[(1139,730),(1176,729),(1193,755),(1220,754),(1227,772),(1209,785),(1181,779),(1159,795),(1139,785),(1117,791),(1111,779),(1129,757)]),
 ('RGE','Gera',[(1038,565),(1073,571),(1097,566),(1128,579),(1132,605),(1119,624),(1080,631),(1048,619),(1016,622),(1005,605)]),
 ('RSL','Schleiz',[(1031,797),(1066,802),(1073,822),(1058,841),(1040,858),(1027,859),(1024,837),(1011,826),(1017,811)]),
 ('RSL','Schleiz south',[(1042,876),(1076,889),(1074,913),(1054,922),(1024,914),(1016,898)])]

def protected_cells(x,y):
    # Union of rejected old/translated Erfurt neighbourhoods, generously padded.
    # Eichsfeld is outside SID, as are all Anhalt corrections.
    return (x>=4342)&(x<=4358)&(y>=822)&(y<=836)

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

def load(name):
    return json.loads((OUT / name).read_text(encoding='utf8'))

def capture():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'BASELINE.json').exists(), 'Immutable baseline already exists'
    inv = core.qa.inventory()
    originals = {}
    for folder in ['common/history', 'map_data/state_regions']:
        for p in (ROOT / folder).rglob('*.txt'):
            raw = p.read_text(encoding='utf-8-sig')
            if SID in raw:
                originals[p.relative_to(ROOT).as_posix()] = raw
    bitmap = ROOT / 'docs/reports/map/MAP2R/provinces_candidate.png'
    assert core.sha(bitmap) == core.sha(ROOT / 'map_data/provinces.png')
    protected = ['tools/map2l_registry.py', 'tools/map2k_imperial_system.py',
                 'tools/hre_centralization_01.py', 'tools/hre_subject_feedback_01.py',
                 'tools/hre_secession_lens_01.py']
    dump('BASELINE.json', dict(inventory=inv, originals=originals,
        hashes=q.economy.runtime_hashes(), bitmap_backup=bitmap.relative_to(ROOT).as_posix(),
        bitmap_sha256=core.sha(bitmap),
        registry=json.loads(core.active_registry_path().read_text(encoding='utf8')),
        git_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        git_index_sha256=core.sha(ROOT / '.git/index'),
        tool_originals={p:(ROOT/p).read_text(encoding='utf8') for p in protected},
        prior_records={p.relative_to(ROOT).as_posix():core.sha(p)
          for folder in ['MAP2R','MAP2S'] for p in (ROOT/'docs/reports/map'/folder).rglob('*')
          if p.is_file() and p.suffix in {'.json','.md','.csv'}}))
    print('Immutable capture: world', sum(r['count'] for r in inv['pops']), flush=True)

def fetch():
    d = OUT / 'EVIDENCE'
    d.mkdir(exist_ok=True)
    name = 'Thüringische Staaten 1789 – F. W. Putzgers Historischer Schul-Atlas 1905 (135770778).jpg'
    digest = hashlib.md5(name.encode()).hexdigest()
    url = f'https://upload.wikimedia.org/wikipedia/commons/{digest[0]}/{digest[:2]}/' + urllib.parse.quote(name.replace(' ', '_'))
    # Wikimedia hashes the normalized (underscored) title.
    digest = hashlib.md5(name.replace(' ', '_').encode()).hexdigest()
    url = f'https://upload.wikimedia.org/wikipedia/commons/{digest[0]}/{digest[:2]}/' + urllib.parse.quote(name.replace(' ', '_'))
    path = d / 'PUTZGER_1789_1905.jpg'
    if not path.exists():
        req = urllib.request.Request(url, headers={'User-Agent':'1776HistoricalMapResearch/1.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            path.write_bytes(response.read())
    image = Image.open(path).convert('RGB')
    image.resize((1800, round(image.height * 1800 / image.width))).save(OUT/'SOURCE_OVERVIEW.png')
    dump('SOURCE_FILE.json', dict(url=url, sha256=core.sha(path), dimensions=image.size,
        date_represented=1789, publication=1905, type='retrospective comparison, not direct proof of 1776'))
    print(url, image.size, flush=True)

def inspect():
    b = load('BASELINE.json')
    a = core.packed(ROOT / b['bitmap_backup'])
    rows = []
    for row in b['inventory']['owners']:
        rgb, sid, tag = row['key']
        if sid != SID: continue
        yy, xx = np.where(a == int(rgb[1:], 16))
        rows.append(dict(RGB=rgb, State_ID=sid, Numeric_ID=73, Owner=tag, Pixels=len(xx),
            Xmin=int(xx.min()), Xmax=int(xx.max()), Ymin=int(yy.min()), Ymax=int(yy.max())))
    dump('CURRENT_PROVINCES.json', rows)
    from map2o_east_frisia import panel
    owners = {r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    panel(a, owners, (4315, 800, 4445, 865), 'MAP-2T AVANT - provinces réellement installées', scale=14).save(OUT/'NATIVE_BEFORE.png')
    print(rows, flush=True)

def source_grid():
    original=Image.open(OUT/'SOURCE_OVERVIEW.png').convert('RGB')
    for name,box in [('WEST',(220,350,850,1060)),('EAST',(780,420,1250,1000)),('NORTH',(100,100,720,500))]:
        image=original.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2))
        draw=ImageDraw.Draw(image);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
        for x in range((box[0]//50+1)*50,box[2],50):
            draw.line(((x-box[0])*2,0,(x-box[0])*2,image.height),fill='#636bb8')
            draw.text(((x-box[0])*2+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//50+1)*50,box[3],50):
            draw.line((0,(y-box[1])*2,image.width,(y-box[1])*2),fill='#636bb8')
            draw.text((0,(y-box[1])*2+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        image.save(OUT/(name+'_SOURCE_GRID.png'))

def geometry():
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup'])
    profile=ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json'
    model=json.loads(profile.read_text(encoding='utf8'))['model']
    # Align the NEW historical sheet; do not refit the native geographic model.
    # Symbol readings are retained as approximate readings, not surveyed pixels.
    controls=[('Gotha',490,571,10.7019,50.9482),
      ('Weimar',800,550,11.3290,50.9803),
      ('Leipzig',1201,254,12.3731,51.3397),
      ('Meiningen',335,858,10.4154,50.5680),
      ('Plauen',1146,880,12.1384,50.4973),
      ('Gera',1091,614,12.0833,50.8772)]
    design=np.array([[x,y,1] for _,x,y,_,_ in controls])
    target=forward(model,[[lon,lat] for _,_,_,lon,lat in controls])
    transform=np.linalg.lstsq(design,target,rcond=None)[0]
    dump('ALIGNMENT.json',dict(source='PUTZGER_1789_1905',transform=transform.tolist(),
      controls=[dict(name=n,source=[x,y],geo=[lon,lat],diagnostic_target=t.tolist(),
        sheet_fit_residual=float(np.linalg.norm(np.array([x,y,1])@transform-t)))
        for (n,x,y,lon,lat),t in zip(controls,target)],
      native_profile=profile.relative_to(ROOT).as_posix(),native_profile_sha256=core.sha(profile),
      native_model_refitted=False,native_position_error_bound=None,
      warning='Historical-sheet fit is not independent native accuracy. B generalization only; no 7.20px translation; Erfurt guard excluded.'))
    relevant=[r for r in b['inventory']['owners'] if r['key'][1]==SID]
    owner={r['key'][0]:r['key'][2] for r in relevant}
    colors=np.array([int(c[1:],16) for c in owner])
    yy,xx=np.where(np.isin(before,colors));points=np.column_stack([xx+.5,yy+.5])
    labels=np.array([owner['x'+format(int(before[y,x]),'06X')] for y,x in zip(yy,xx)])
    claimed=np.zeros(len(xx),bool);traces=[]
    for tag,name,poly in TRACES:
        mapped=np.column_stack([poly,np.ones(len(poly))])@transform
        selected=core.inside(points,mapped)&~protected_cells(xx,yy)
        assert not np.any(claimed&selected),'Overlapping historical cores'
        labels[selected]=tag;claimed|=selected
        traces.append(dict(tag=tag,name=name,source_polygon=poly,game_polygon=mapped.tolist(),
            installed_cells=int(selected.sum()),confidence='B',limitations='Clipped to STATE_SAXONY; Erfurt protected; not complete historical borders'))
    after=before.copy();assignments=[];new=[];used=set(map(int,np.unique(before)));color=0xEDB400
    for parent in owner:
        selected=before[yy,xx]==int(parent[1:],16)
        parent_labels=labels[selected];px=xx[selected];py=yy[selected]
        for tag in sorted(set(parent_labels)):
            mask=np.zeros(before.shape,bool);mask[py[parent_labels==tag],px[parent_labels==tag]]=True
            for index,part in enumerate(core.components(mask)):
                if tag==owner[parent] and index==0:rgb=parent
                else:
                    while color in used:color+=1
                    rgb='x'+format(color,'06X');used.add(color);color+=1
                    new.append(dict(rgb=rgb,parent_rgb=parent))
                ys=np.array([p[0] for p in part]);xs=np.array([p[1] for p in part]);after[ys,xs]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state=SID,previous_owner=owner[parent],owner=tag,
                  pixels=len(part),cells=[[int(x),int(y)] for y,x in part],confidence='B' if tag!=owner[parent] else 'C_RETAINED'))
    present=set(r['owner'] for r in assignments)
    assert set(OLD_TAGS+NEW_TAGS)<=present,('Empty countries',set(OLD_TAGS+NEW_TAGS)-present)
    assert np.all(after[yy[protected_cells(xx,yy)],xx[protected_cells(xx,yy)]]==before[yy[protected_cells(xx,yy)],xx[protected_cells(xx,yy)]]), 'Guard RGBs must stay exactly unchanged'
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(parents=list(owner),assignments=assignments,new_provinces=new,traces=traces,hub_rebindings=[],new_members=NEW_TAGS))
    source_image=Image.open(OUT/'SOURCE_OVERVIEW.png').convert('RGB');d=ImageDraw.Draw(source_image)
    for trace in traces:
        d.line(trace['source_polygon']+[trace['source_polygon'][0]],fill='red',width=3)
    source_image.save(OUT/'SOURCE_TRACING_REVIEW.png')
    print('Territories',C.Counter({t:sum(r['pixels'] for r in assignments if r['owner']==t) for t in present}),flush=True)
    print('New RGBs',len(new),'owner changes',sum(r['pixels'] for r in assignments if r['owner']!=r['previous_owner']),flush=True)

def compiler_before():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();checks=[]
    for p,raw in files.items():checks.append(dict(file=p,passed=(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff')))
    dump('COMPILER_BEFORE.json',dict(passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks))
    assert all(r['passed'] for r in checks),[r for r in checks if not r['passed']]
    print('Full current imperial compiler reproduced',len(files),'files',flush=True)

def fetch_rulers():
    from pypdf import PdfReader
    d=OUT/'EVIDENCE';d.mkdir(exist_ok=True)
    url='https://www.lztthueringen.de/media/egierendef_rsten.pdf';p=d/'HERZ_REGIERENDE_FUERSTEN.pdf'
    if not p.exists():
        with urllib.request.urlopen(url,timeout=60) as response:p.write_bytes(response.read())
    pages=[]
    for i,page in enumerate(PdfReader(p).pages):
        text=page.extract_text()
        if any(s in text for s in ['Gotha-Altenburg','Hildburghausen','Reuß','Reuss','Schwarzburg']):pages.append(dict(page=i+1,text=text))
    dump('RULER_SOURCE_PAGES.json',dict(url=url,sha256=core.sha(p),pages=pages))
    for page in pages:
        for line in page['text'].splitlines():
            if any(s in line for s in ['HEINRICH','CHRISTIAN','LUDWIG','ERNST','1772','1782','1784','1758','1767']):print(page['page'],line,flush=True)

def prepare():
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};bindings=[]
    assert q.economy.runtime_hashes()==b['hashes'],'Workspace runtime drift; inspect before writing'
    assert load('COMPILER_BEFORE.json')['passed']==load('COMPILER_BEFORE.json')['total']
    assert not (set(NEW_TAGS)&set(b['inventory']['countries'])),'New tag collision'
    rel='common/history/states/00_states.txt';raw=b['originals'][rel];s=core.state(raw,SID);ops=[]
    for node in s.children('create_state'):
        tag=node.one('country').removeprefix('c:');f=node.children('owned_provinces')[0]
        ops.append((f.start,f.end,'owned_provinces = { '+' '.join(r['rgb'] for r in g['assignments'] if r['owner']==tag)+' }'))
    extra='\n'.join('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(r['rgb'] for r in g['assignments'] if r['owner']==tag)+' } }' for tag in NEW_TAGS)
    ops.append((s.end-1,s.end-1,'\n'+extra+'\n'));files[rel]=core.edits(raw,ops)
    rel='map_data/state_regions/00_west_europe.txt';raw=b['originals'][rel];s=next(n for n in core.cw.parse(raw) if n.key==SID);ops=[]
    for field in ['provinces','prime_land']:
        for f in s.children(field):
            old=core.values(s,field);new=[]
            for color in old:new.extend(r['rgb'] for r in g['assignments'] if r['parent_rgb']==color)
            if old!=new:
                ops.append((f.start,f.end,field+' = { '+' '.join('"'+c+'"' for c in new)+' }'))
                if field=='prime_land':bindings.append(dict(state=SID,field=field,before=old,after=new))
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png')
    for loc in q.r9.locators(before):
        if loc['ID']!=73:continue
        field=loc['Kind'];x,y=int(loc['X']),int(loc['Y']);new='x'+format(int(after[y,x]),'06X');old=core.cw.scalar(s.one(field))
        if old and old!=new:
            f=s.children(field)[0];ops.append((f.start,f.end,field+' = "'+new+'"'))
            bindings.append(dict(state=SID,field=field,before=old,after=new,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
    files[rel]=core.edits(raw,ops)
    allocations=[];weights={}
    for tag in OLD_TAGS:
        weights[tag]=dict(C.Counter({target:sum(a['pixels'] for a in g['assignments'] if a['previous_owner']==tag and a['owner']==target) for target in OLD_TAGS+NEW_TAGS}))
        weights[tag]={t:n for t,n in weights[tag].items() if n}
    for rel,raw in b['originals'].items():
        if '/pops/' not in rel:continue
        s=core.state(raw,SID);ops=[];pieces=C.defaultdict(list)
        for node in s.children():
            if not node.key.startswith('region_state:'):continue
            tag=node.key.split(':')[1]
            if tag not in OLD_TAGS:continue
            for pop in node.children('create_pop'):
                f=pop.children('size')[0];amounts=core.allocate(int(f.value),weights[tag])
                ops.append((f.start,f.end,'size = '+str(amounts.get(tag,0))))
                for target,amount in amounts.items():
                    if target!=tag and amount:
                        pieces[target].append(core.edits(raw[pop.start:pop.end],[(f.start-pop.start,f.end-pop.start,'size = '+str(amount))]))
                allocations.append(dict(donor=tag,culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:'+pop.one('culture')),before=int(f.value),after=amounts))
        text=core.edits(raw,ops)
        for tag,parts in pieces.items():text=core.append(text,SID,tag,'\n'.join(parts))
        files[rel]=text
    dump('POPULATION_ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_REDISTRIBUTION_NOT_HISTORICAL_CENSUS',weights=weights,profiles=allocations,
        reason='No dated count matches these deliberately clipped cores. Written source populations redistributed, not invented from surface area as a historical estimate. No compensation elsewhere.'))
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw+'\n'+''.join(r['rgb']+'="'+terrain[r['parent_rgb'].upper()]+'"\n' for r in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state']==SID]
    updated=[dict(rgb=r['rgb'],state=SID,beneficiary=r['owner'],basis='MAP2T B historical-sheet core; C residual retained, not a certified 1776 border. See REPORT.md.') for r in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state']!=SID]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    migration=dict(replaced_regions=[SID],previous=previous,updated=updated,new_members=NEW_TAGS,free_cities=[],new_provinces=g['new_provinces'],
        geometry='MAP2T/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[])
    countries(files,migration)
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for p,raw in files.items():
        if p.endswith('.txt'):core.cw.parse(raw)
    dump('EXPECTED_TEXT.json',files);core.OUT=OUT
    changed=core.emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changed,registered_RGBs=len(ledger),region_reference_changes=bindings))
    print('Prepared',len(changed),'files;',len(ledger),'imperial RGBs;',len(bindings),'references rebound',flush=True)

def countries(files,migration):
    colors={'GOT':'221 196 111','HIL':'100 177 133','SSO':'150 124 177','RGZ':'81 171 187','RGE':'218 148 85','RSL':'129 132 142'}
    defs=''.join(t+' = { color = { '+colors[t]+' } country_type = recognized tier = principality cultures = { north_german } religion = protestant capital = STATE_SAXONY }\n' for t in NEW_TAGS)
    files['common/country_definitions/1776_map2t_saxony.txt']=defs
    migration['country_additions']={n.key:core.qa.signature(n) for n in core.cw.parse(defs)}
    rel='common/country_definitions/00_countries.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');ops=[];changes=[]
    for tag,old in [('SAX','kingdom'),('WEI','grand_principality')]:
        node=next(n for n in core.cw.parse(raw) if n.key==tag);f=node.children('tier')[0];assert f.value==old
        new=core.edits(raw[node.start:node.end],[(f.start-node.start,f.end-node.start,'tier = principality')])
        changes.append(dict(tag=tag,before=old,after='principality',before_signature=core.qa.signature(node),after_signature=core.qa.signature(core.cw.parse(new)[0])))
        ops.append((f.start,f.end,'tier = principality'))
    migration['country_tier_corrections']=changes;files[rel]=core.edits(raw,ops)
    template=(ROOT/'common/history/countries/cob - saxe-coburg-gotha.txt').read_text(encoding='utf-8-sig')
    for tag in NEW_TAGS:files['common/history/countries/'+tag.lower()+' - map2t.txt']=template.replace('c:COB','c:'+tag)
    rulers={'GOT':('Ernst II. Ludwig','von Saxe-Gotha-Altenburg','1745.1.30'),
      'HIL':('Ernst Friedrich III. Carl','von Saxe-Hildburghausen','1727.6.10'),
      'SSO':('Christian Günther III.','von Schwarzburg-Sondershausen','1736.6.24'),
      'SCW':('Ludwig Günther II.','von Schwarzburg-Rudolstadt','1708.10.22'),
      'RGZ':('Heinrich XI.','Reuss-Greiz','1722.3.18'),
      'RGE':('Heinrich XXX.','Reuss-Gera','1727.4.24'),
      'RSL':('Heinrich XII.','Reuss-Schleiz','1716.5.15')}
    for tag,(first,last,born) in rulers.items():
        rel='common/history/characters/'+('scw - schwarzburg.txt' if tag=='SCW' else tag.lower()+' - map2t.txt')
        assert not (ROOT/rel).exists(),'Pre-existing character file requires review: '+rel
        files[rel]='CHARACTERS = { c:'+tag+' ?= { create_character = { first_name = aor1776_map2t_'+tag.lower()+'_first last_name = aor1776_map2t_'+tag.lower()+'_last historical = yes culture = north_german religion = rel:protestant ruler = yes birth_date = '+born+' interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    flag='# Shared dynastic arms/colours are a graphical simplification, not a political union.\n'
    for tag in NEW_TAGS:flag+=tag+' = { flag_definition = { coa = '+('aor1776_map2t_reuss' if tag.startswith('R') else 'SCW' if tag=='SSO' else 'COB')+' priority = 100 allow_overlord_canton = no } }\n'
    files['common/flag_definitions/1776_map2t.txt']=flag
    files['common/coat_of_arms/coat_of_arms/1776_map2t.txt']='aor1776_map2t_reuss = { pattern = "pattern_solid.tga" color1 = "black" colored_emblem = { texture = "ce_lion_rampant.dds" color1 = "yellow" color2 = "red" } }\n'
    gov=''
    groups=[('electorate',['SAX'],'ELECTOR','ELECTRESS'),('duchy',['GOT','HIL','WEI','COB'],'DUKE','DUCHESS'),('principality',['SCW','SSO'],'PRINCE','PRINCESS'),('county',['RGZ','RGE','RSL'],'COUNT','COUNTESS')]
    for key,tags,male,female in groups:
        mt='aor1776_map2t_elector_title' if key=='electorate' else 'RULER_TITLE_'+male
        ft='aor1776_map2t_electress_title' if key=='electorate' else 'RULER_TITLE_'+female
        gov+='gov_aor1776_map2t_'+key+' = { transfer_of_power = hereditary male_ruler = "'+mt+'" female_ruler = "'+ft+'" possible = { OR = { '+' '.join('c:'+t+' ?= this' for t in tags)+' } has_law = law_type:law_monarchy } on_government_type_change = { change_to_hereditary = yes } on_post_government_type_change = { post_change_to_hereditary = yes } }\n'
    files['common/government_types/00_1776_map2t.txt']=gov
    desc={'electorate':('Electorate','Électorat'), 'duchy':('Duchy','Duché'),'principality':('Principality','Principauté'),'county':('Imperial county','Comté impérial')}
    for lang,index in [('english',0),('french',1)]:
        loc='\ufeffl_'+lang+':\n'
        for tag,names in NAMES.items():loc+=' '+tag+':0 "'+names[index]+'"\n '+tag+'_ADJ:0 "'+names[index]+'"\n'
        for tag,(first,last,_) in rulers.items():loc+=' aor1776_map2t_'+tag.lower()+'_first:0 "'+first+'"\n aor1776_map2t_'+tag.lower()+'_last:0 "'+last+'"\n'
        loc+=' aor1776_map2t_elector_title:0 "'+('Elector' if lang=='english' else 'Prince-électeur')+'"\n aor1776_map2t_electress_title:0 "'+('Electress' if lang=='english' else 'Princesse-électrice')+'"\n'
        for key,names in desc.items():
            loc+=' gov_aor1776_map2t_'+key+':0 "'+names[index]+'"\n'
            text=('A hereditary imperial government whose ruler maintains the institutions and succession of the ruling house.' if lang=='english' else 'Un gouvernement héréditaire de l’Empire dont le souverain maintient les institutions et la succession de sa maison.')
            loc+=' gov_aor1776_map2t_'+key+'_desc:0 "'+text+'\\n\\n$TRANSFER_OF_POWER_NAME_DESC$"\n'
        files[f'localization/{lang}/replace/1776_map2t_l_{lang}.yml']=loc

def install():
    b=load('BASELINE.json')
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    for p,raw in load('EXPECTED_TEXT.json').items():assert (ROOT/p).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip(),p
    try:
        shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    except OSError as exc:
        if exc.errno!=22:raise
        # Windows sandbox rejects this binary Python handle on some hosts;
        # the native, literal-path copy preserves the reviewed exact bytes.
        subprocess.run(['powershell','-NoProfile','-Command',
            "Copy-Item -LiteralPath '"+str(OUT/'provinces_candidate.png')+"' -Destination '"+str(ROOT/'map_data/provinces.png')+"' -ErrorAction Stop"],check=True)
    assert core.sha(ROOT/'map_data/provinces.png')==core.sha(OUT/'provinces_candidate.png')
    print('Reviewed text verified; installed only declared child RGB bitmap.',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files);core.OUT=OUT
    changes=core.emit(files,'IMPERIAL.patch');dump('IMPERIAL_FILES.json',dict(files=changes))
    print('Prepared cumulative imperial runtime:',len(changes),'changed of',len(files),flush=True)

def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png')
    palette={'SAX':'#b4a6cb','WEI':'#a6c767','MEI':'#7caa86','COB':'#c39c65','SCW':'#bba0c9','GOT':'#ead184','HIL':'#71c19a','SSO':'#9478b4','RGZ':'#58b9cb','RGE':'#df9b66','RSL':'#8f949c'}
    old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};new=dict(old)
    for row in g['assignments']:new[row['rgb']]=row['owner']
    box=(4318,817,4400,858);x0,y0,x1,y1=box;panels=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for array,owners,title in [(before,old,'AVANT'),(after,new,'APRÈS - noyaux B, résidus non certifiés')]:
        local=array[y0:y1,x0:x1];rgb=np.zeros((*local.shape,3),dtype='uint8');rgb[:]=[135,153,165]
        for color in np.unique(local):rgb[local==color]=ImageColor.getrgb(palette.get(owners.get('x'+format(int(color),'06X')),'#8095a4'))
        im=Image.fromarray(rgb).resize(((x1-x0)*13,(y1-y0)*13),Image.Resampling.NEAREST)
        panel=Image.new('RGB',(im.width,im.height+110),'#faf8f0');panel.paste(im,(0,35));d=ImageDraw.Draw(panel);d.text((10,9),title,font=font,fill='black')
        for tag in OLD_TAGS+NEW_TAGS:
            pixels=np.isin(local,[int(c[1:],16) for c,t in owners.items() if t==tag]);ys,xs=np.where(pixels)
            if len(xs):d.text((int(np.median(xs))*13,int(np.median(ys))*13+35),tag,font=font,fill='black',stroke_width=1,stroke_fill='white')
        for i,(tag,color) in enumerate(palette.items()):
            px=(i%6)*175;py=im.height+42+(i//6)*25;d.rectangle((px,py,px+14,py+14),fill=color);d.text((px+19,py),tag,font=font,fill='black')
        # Hatch the explicitly excluded area, without painting it into provinces.
        d.rectangle(((4342-x0)*13,(822-y0)*13+35,(4359-x0)*13,(837-y0)*13+35),outline='red',width=2)
        d.text((5,im.height+88),'Cadre rouge : secteur exclu d’Erfurt. Résidus inchangés non certifiés.',font=font,fill='black')
        panels.append(panel)
    out=Image.new('RGB',(panels[0].width*2+15,panels[0].height),'#faf8f0');out.paste(panels[0],(0,0));out.paste(panels[1],(panels[0].width+15,0));out.save(OUT/'SAXONY_THURINGIA_BEFORE_AFTER.png')

def validate():
    from map2l_registry import expected_country_definitions, apply_territorial_migrations
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=core.qa.inventory();dump('CURRENT_INVENTORY.json',inv)
    checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy()
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']};eo=counter(b['inventory']['owners'])
    for key in list(eo):
        if key[0] in g['parents']:del eo[key]
    for a in g['assignments']:
        for x,y in a['cells']:expected[y,x]=int(a['rgb'][1:],16)
        eo[a['rgb'],a['state'],a['owner']]=1
        check('Owner/state '+a['rgb'],owners.get(a['rgb'])==[SID,a['owner']])
        check('Cell count '+a['rgb'],int(np.sum(after==int(a['rgb'][1:],16)))==a['pixels'])
        check('Connected RGB '+a['rgb'],len(core.components(after==int(a['rgb'][1:],16)))==1)
    check('Every world pixel matches the declared transformation',np.array_equal(after,expected))
    check('Every world owner matches exact expected delta',counter(inv['owners'])==eo)
    guard=(slice(822,837),slice(4342,4359));check('Erfurt old/rejected hypotheses unchanged byte for byte',np.array_equal(before[guard],after[guard]))
    check('Only STATE_SAXONY parent cells split',all(a['state']==SID and a['parent_rgb'] in g['parents'] for a in g['assignments']))
    for key in ['buildings','building_levels_written','units','duplicates','errors','resolved_demographics','pops']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    st=dict(b['inventory']['state_types']);st.update({SID+'|'+t:'incorporated_default' for t in NEW_TAGS})
    check('Only six state subdivisions added',inv['state_types']==st)
    migration=load('REGISTRY_MIGRATION.json')
    check('Country definitions only exact authorized deltas',inv['countries']==expected_country_definitions(b['inventory']['countries'],[migration]))
    ep=counter(b['inventory']['regional_pop'])
    for row in load('POPULATION_ALLOCATION.json')['profiles']:
        ep[SID,row['donor'],row['culture'],row['religion']]-=row['before']
        for tag,amount in row['after'].items():ep[SID,tag,row['culture'],row['religion']]+=amount
    check('All world demographic profiles match declared redistribution',counter(inv['regional_pop'])==ep)
    world=sum(row['count'] for row in inv['pops']);world_before=sum(row['count'] for row in b['inventory']['pops'])
    check('Actual baseline world verified',world_before==835801255)
    check('Technical redistribution has no artificial population',world==world_before)
    for tag in NEW_TAGS:
        total=sum(row['count'] for row in inv['regional_pop'] if row['key'][1]==tag)
        check('New country has territory and population '+tag,total>0 and any(a['owner']==tag for a in g['assignments']))
        check('Capital accessible '+tag,any(row['key'][1:]==[SID,tag] for row in inv['owners']))
        text=(ROOT/('common/history/countries/'+tag.lower()+' - map2t.txt')).read_text(encoding='utf8')
        check('Conservative starting history '+tag,'effect_starting_politics_conservative' in text)
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'))
    oldmask=np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]);newmask=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
    check('Imperial physical extent unchanged',np.array_equal(oldmask,newmask))
    check('Unique registered RGBs',len(ledger)==len({r['rgb'] for r in ledger})==537)
    for row in ledger:check('Imperial title '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']])
    # Replay the existing chronological chain from the frozen MAP2L pre-migration registry.
    from map2l_registry import approved_territorial_extensions
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry']
    belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'));regions={r['state'] for r in belgian['assignments']}
    frozen=[r for r in initial if r['state'] not in regions]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in belgian['assignments']]+approved_territorial_extensions()
    replay=apply_territorial_migrations(frozen);check('Cumulative registry replay',replay==ledger)
    import prototype_map2k_main_map as main_map
    decoded=np.array(Image.open(ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds').convert('RGBA'))[:,:,0]==255
    x0,y0=main_map.ORIGIN;check('Main map physical mask matches new registry',np.array_equal(decoded,newmask[y0:y0+main_map.TILE,x0:x0+main_map.TILE]))
    raw=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    for row in g['new_provinces']:
        check('New RGB absent at baseline '+row['rgb'],not np.any(before==int(row['rgb'][1:],16)))
        check('Terrain inherited once '+row['rgb'],len(re.findall(r'(?im)^\s*'+row['rgb']+r'\s*=',raw))==1 and tm[row['rgb'].upper()]==tm[row['parent_rgb'].upper()])
        check('Defined region '+row['rgb'],inv['geometry'].get(row['rgb'])==SID)
    rel='map_data/state_regions/00_west_europe.txt';old=next(n for n in core.cw.parse(b['originals'][rel]) if n.key==SID);now=next(n for n in core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig')) if n.key==SID)
    bound={row['field'] for row in migration['region_reference_changes']};exclude=bound|{'provinces'}
    check('Resources/arable/infrastructure/state ID preserved',[core.qa.signature(n) for n in old.children() if n.key not in exclude]==[core.qa.signature(n) for n in now.children() if n.key not in exclude])
    # Every old selector outside this state is strictly unchanged in each edited history file.
    for rel,raw in load('EXPECTED_TEXT.json').items():
        check('Exact reviewed runtime '+rel,(ROOT/rel).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip())
        if rel.endswith('.txt'):
            try:core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'));check('Parse '+rel,True)
            except Exception as exc:check('Parse '+rel,False,str(exc))
        if rel in b['originals'] and '/history/' in rel:
            before_nodes=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(b['originals'][rel])) if n.key.startswith('s:STATE_') and n.key!='s:'+SID]
            after_nodes=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(raw)) if n.key.startswith('s:STATE_') and n.key!='s:'+SID]
            check('No other state history edited '+rel,before_nodes==after_nodes)
    for rel,raw in load('IMPERIAL_EXPECTED.json').items():check('Full compiled imperial '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    from map2k_patch import ELECTORS
    check('SAX electoral dignity preserved','SAX' in ELECTORS.values() and not set(NEW_TAGS)&set(ELECTORS.values()))
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    allowed=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_FILES.json')['files'])|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    check('Runtime modifications strictly allowlisted',set(changed)<=allowed,sorted(set(changed)-allowed))
    for folder in ['buildings','military_formations','diplomacy','subject_types']:
        check('All original '+folder+' files preserved',all(current.get(p)==h for p,h in b['hashes'].items() if '/'+folder+'/' in p))
    for p in ['tools/hre_centralization_01.py','tools/hre_subject_feedback_01.py','tools/hre_secession_lens_01.py','tools/map2k_imperial_system.py']:
        check('Separate HRE mechanics/tool preserved '+p,(ROOT/p).read_text(encoding='utf8')==b['tool_originals'][p])
    check('Previous Anhalt/Suspended Jever records untouched',all((ROOT/p).is_file() and core.sha(ROOT/p)==h for p,h in b['prior_records'].items()))
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    dump('WORLD_POPULATION_DELTA.json',dict(before=world_before,after=world,delta=world-world_before,method=load('POPULATION_ALLOCATION.json')['method'],historical_estimate_applied=False,world_total_not_an_invariant_requirement=True))
    dump('IMPERIAL_REGISTRY_VALIDATION.json',dict(before=len(b['registry']),after=len(ledger),extent_unchanged=bool(np.array_equal(oldmask,newmask)),cumulative_replay=replay==ledger,new_members=NEW_TAGS,new_electors=[],existing_elector='SAX',native_subjects_added=False))
    result=dict(status='MAP2T_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST' if all(r['passed'] for r in checks) else 'FAILED',runtime_status='NOT_TESTED_MAP2T',historical_status='SIX_NEW_CORE_COUNTRIES_NOT_FULL_THURINGIA',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,runtime_files_modified=changed,
        transferred_cells=sum(a['pixels'] for a in g['assignments'] if a['owner']!=a['previous_owner']),new_RGBs=len(g['new_provinces']),world_population=world,preexisting_anomalies=dict(duplicate_RGBs=len(inv['duplicates']),invalid_references=len(inv['errors'])),independent_geographic_error_bound_px=None)
    if (OUT/'UNIT_TESTS.json').exists():result['unit_tests']=load('UNIT_TESTS.json')
    if (OUT/'CSV_VALIDATION.json').exists():result['tables']=load('CSV_VALIDATION.json')
    dump('VALIDATION.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2T',status=result['status'],functional_files={p:current[p] for p in changed},bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),previous_manifest='docs/reports/map/MAP2R/INSTALLED_MANIFEST.json',previous_manifest_is_stage_snapshot_not_current=True))
    print(result['status'],result['passed'],'/',result['total'],'world',world,flush=True)
    if result['passed']!=result['total']:raise SystemExit(1)

def unit_tests():
    import unittest,io,time
    groups={'MAP2T_targeted':['test_map2t_saxony'],'cumulative_contracts':['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01'],
      'prior_stage_snapshots':['test_map2r_anhalt','test_map2q_r3','test_map2q_r2','test_map2m_r8','test_map2m_r9','test_map2o_east_frisia']}
    results={}
    for key,modules in groups.items():
        started=__import__('time').monotonic();stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=1).run(unittest.TestLoader().loadTestsFromNames(modules))
        results[key]=dict(modules=modules,tests=r.testsRun,failures=[t.id() for t,_ in r.failures],errors=[t.id() for t,_ in r.errors],output=stream.getvalue(),seconds=round(time.monotonic()-started,2))
        print(key,r.testsRun,'tests;',len(r.failures),'failures;',len(r.errors),'errors',flush=True)
    dump('UNIT_TESTS.json',results)
    if any(results[k]['failures'] or results[k]['errors'] for k in ['MAP2T_targeted','cumulative_contracts']):raise SystemExit(1)

def table_data():
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=load('CURRENT_INVENTORY.json')
    political=[]
    for tag,names in NAMES.items():
        political.append(dict(TAG=tag,Etat=names[1],Situation='Créé, noyaux B' if tag in NEW_TAGS else 'Déjà présent, résidus incomplets',
            Cellules=sum(a['pixels'] for a in g['assignments'] if a['owner']==tag),
            Population_region=sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==[SID,tag]),
            State_ID=SID,ID_numerique=73,Statut_imperial='Électeur conservé' if tag=='SAX' else 'Membre ordinaire autonome',
            Source='HISTORICAL_EVIDENCE.md',Limite='Chiffres démographiques techniques; territoire complet non certifié'))
    political.extend([dict(TAG=None,Etat=label,Situation='Non créé; découpage C',Cellules=None,Population_region=None,State_ID=SID,ID_numerique=73,Statut_imperial='Comté historique, non installé',Source='HISTORICAL_EVIDENCE.md',Limite='Séparation locale Lobenstein/Ebersdorf non établie sur le bitmap') for label in ['Reuss-Lobenstein','Reuss-Ebersdorf']])
    current=[];transfers=[]
    for a in g['assignments']:
        xs=[p[0] for p in a['cells']];ys=[p[1] for p in a['cells']]
        current.append(dict(RGB=a['rgb'],Parent_RGB=a['parent_rgb'],Proprietaire=a['owner'],Ancien_proprietaire=a['previous_owner'],State_ID=SID,ID_numerique=73,Cellules=a['pixels'],Xmin=min(xs),Xmax=max(xs),Ymin=min(ys),Ymax=max(ys),Classe=a['confidence']))
        if a['rgb']==a['parent_rgb']:continue
        for x,y in sorted(a['cells']):
            transfers.append(dict(RGB_avant=a['parent_rgb'],RGB_apres=a['rgb'],Avant=a['previous_owner'],Apres=a['owner'],State_ID=SID,X=x,Y=y,Classe=a['confidence'],Nature='Transfert' if a['owner']!=a['previous_owner'] else 'Subdivision technique',Source='GEOMETRY.json; SOURCE_TRACING_REVIEW.png'))
    old={tuple(r['key']):r['count'] for r in b['inventory']['regional_pop']};new={tuple(r['key']):r['count'] for r in inv['regional_pop']};pops=[]
    for key in sorted(set(old)|set(new)):
        if key[0]!=SID:continue
        pops.append(dict(State_ID=key[0],TAG=key[1],Culture=key[2],Religion=key[3],Avant=old.get(key,0),Apres=new.get(key,0),Delta=new.get(key,0)-old.get(key,0),Methode='Redistribution technique provisoire',Source='POPULATION_ALLOCATION.json'))
    pops.append(dict(State_ID='MONDE',TAG=None,Culture='Toutes',Religion='Toutes',Avant=sum(r['count'] for r in b['inventory']['pops']),Apres=sum(r['count'] for r in inv['pops']),Delta=0,Methode='Total mesuré, non contrainte historique',Source='Inventaire effectif mod et jeu'))
    unresolved=[dict(Secteur=s,Classe='C',Probleme=p,Action=a) for s,p,a in [
      ('Lobenstein et Ebersdorf','Souverainetés distinctes en1776, séparation cartographique non suffisamment identifiée. Aucun de ces pays créé.','Retrouver une carte locale distinguant explicitement les deux juridictions; pas de fusion arbitraire.'),
      ('Schwarzbourg Unterherrschaften','Sondershausen et Frankenhausen hors noyaux installés; possessions septentrionales non reconstruites.','Source locale et accord sur une extension; Anhalt interdit dans le présent lot.'),
      ('Gotha et Erfurt','Le noyau de Gotha est tronqué par le secteur protégé; résidus COB/MEI/SCW non certifiés.','Ne pas modifier Erfurt. Compléter les limites gothaises indépendantes dans une continuation.'),
      ('Weimar et Eisenach','WEI reste une abstraction des deux duchés sous un même souverain; pas une fusion constitutionnelle datée de1776. Eisenach occidental incomplet.','Étudier les possessions nécessaires sans importer la fusion de1809; aucune union native nouvelle ici.'),
      ('Cobourg-Saalfeld et Meiningen','Noms de1776 corrigés, mais grandes franges anciennes conservées; HIL seulement un noyau. Condominiums Themar/Römhild non attribués unilatéralement.','Compléter les enveloppes et les juridictions partagées; préserver les RGB franconiens validés.'),
      ('Électorat de Saxe septentrional','Le lot ne rétablit pas toutes les possessions devenues prussiennes en1815, notamment hors STATE_SAXONY.','Traiter une continuation explicitement autorisée; ne pas interpréter PRU conservé comme verdict historique.'),
      ('Reuss périphérique et Schönburg','Greiz, Gera, Schleiz: seuls noyaux B. Pas de Köstritz souverain ajouté ni de regroupement Reuss du XIXe siècle.','Sources territoriales1776 et examen séparé des droits de Schönburg.'),
      ('Démographie historique','Aucun dénombrement daté au périmètre exact des noyaux ne justifie une estimation historique.','Conserver les chiffres techniques jusqu’à une source comparable; pas de population artificielle.'),
      ('Capitales et économie','Toutes les nouvelles capitales utilisent la région73; Sondershausen physique absent du noyau SSO. Bâtiments et armées non créés.','Contrôler subsistance, marché, budget, accès et identité des petits pays en jeu; pas de centre historique certifié par un locator.'),
      ('Drapeaux','Couleurs/armes communes simplifiées; pas une restitution vexillologique certifiée de1776.','Remplacer ultérieurement par des pavillons historiquement documentés sans changer les souverainetés.'),
      ('Erfurt–Eichsfeld et anciens lots','Secteurs exclus, géométrie et historiques inchangés; la translation7,20px reste rejetée.','Suivi séparé seulement avec preuve nouvelle; ne pas relancer le même recalage.')]]
    data={'1776_POLITICAL_INVENTORY.csv':political,'CURRENT_PROVINCES.csv':current,'TERRITORIAL_CHANGES.csv':transfers,'POPULATION_BEFORE_AFTER.csv':pops,'UNRESOLVED.csv':unresolved}
    dump('CSV_TABLES.json',{name:dict(fields=list(rows[0]),rows=rows) for name,rows in data.items()})
    print('Five typed datasets prepared.',flush=True)

def reports():
    b=load('BASELINE.json');g=load('GEOMETRY.json');v=load('VALIDATION.json');inv=load('CURRENT_INVENTORY.json');tests=load('UNIT_TESTS.json');files={};prefix=OUT.relative_to(ROOT).as_posix()+'/'
    totals={tag:sum(r['count'] for r in inv['regional_pop'] if r['key']==[SID,tag,r['key'][2],r['key'][3]]) for tag in NEW_TAGS}
    rows='\n'.join('| '+NAMES[tag][1]+' | '+tag+' | '+str(sum(a['pixels'] for a in g['assignments'] if a['owner']==tag))+' | '+str(totals[tag])+' |' for tag in NEW_TAGS)
    flows=C.Counter()
    for a in g['assignments']:
        if a['previous_owner']!=a['owner']:flows[a['previous_owner'],a['owner']]+=a['pixels']
    flowrows='\n'.join('| '+x+' | '+y+' | '+str(n)+' |' for (x,y),n in sorted(flows.items()))
    files[prefix+'REPORT.md']=f'''# MAP-2T — Noyaux saxons et thuringiens installés

Date : 17 octobre 2026. Situation historique visée : 1er janvier 1776.

**{v['status']}**. Ce sous-lot est prêt pour un test ciblé, pas pour une certification de toute la Thuringe. Lobenstein, Ebersdorf, les possessions septentrionales et plusieurs enclaves ne sont pas terminés. Aucune validation moteur de MAP-2T n’est revendiquée.

## Modifications réelles

| Nouveau pays | TAG | Cellules du noyau | Population technique |
|---|---|---:|---:|
{rows}

121 cellules changent de propriétaire dans STATE_SAXONY, ID numérique73. Seize RGB nouveaux, xEDB400 à xEDB40F, portent les subdivisions nécessaires, y compris des fragments techniques conservant leur ancien propriétaire. Le registre passe de521 à537 RGB, sans changer l’étendue physique impériale.

| Avant | Après | Cellules transférées |
|---|---|---:|
{flowrows}

Les souverainetés sont distinguées à partir des sources institutionnelles et des trajectoires dynastiques; les contours installés sont des noyaux généralisés B lus sur la reconstruction1789 de Putzger, et non des frontières1776 directement certifiées. Voir [preuves et limites](HISTORICAL_EVIDENCE.md). Les portions non attribuées restent chez leur propriétaire technique antérieur, ce qui n’en fait pas une attribution historique validée.

Gotha–Altenbourg est distinct de Cobourg–Saalfeld. Hildburghausen n’est pas fusionné avec Meiningen. SCW est désormais explicitement Schwarzbourg-Rudolstadt, tandis que SSO représente un noyau méridional de Schwarzbourg-Sondershausen. Greiz, Gera et Schleiz ont trois pays distincts et restent des comtés en1776, sans importer les regroupements ultérieurs. Les noms français/anglais et descriptions de gouvernement sont définis, ainsi que les souverains contemporains. Les modèles législatifs/technologiques des six nouveaux pays sont repris de COB: abstraction de gameplay, pas six audits législatifs historiques.

Les rangs anachroniques de SAX et WEI sont abaissés à principauté au sens technique du jeu. SAX conserve sa dignité et son titre de prince-électeur; WEI reste ducal. Aucun nouvel électeur, aucune nouvelle ville libre, aucune union personnelle ni sujétion impériale native n’est ajouté. Les nouvelles nations rejoignent le bloc et les droits de restitution existants comme membres ordinaires. Les mécanismes HRE-CENTRALIZATION, les deux icônes et les prototypes sont préservés.

## Géométrie et exclusions

Le profil diagnostique natif conservé est réutilisé sans optimisation ni translation7,20px. Le calage effectué concerne uniquement la nouvelle feuille historique. Ses résidus d’ajustement ne prouvent pas l’exactitude géographique du bitmap. Aucune borne indépendante de précision locale n’est revendiquée.

Un rectangle de protection X4342–4358/Y822–836 couvre les hypothèses anciennes et rejetées d’Erfurt avec marge. Tous ses RGB restent identiques. Eichsfeld et tous les pixels hors STATE_SAXONY sont inchangés. Aucun corridor artificiel n’est ajouté entre noyaux détachés. Les RGB franconiens de COB, les quatre Anhalt, Jever, Emden, Eutin, la Peene, la Belgique et la Souabe sont protégés par la comparaison mondiale exacte.

La [carte avant/après](SAXONY_THURINGIA_BEFORE_AFTER.png) représente le découpage réellement installé. Rouge: zone exclue d’Erfurt. La carte du journal est régénérée; le masque physique du mode carte reste identique car l’étendue impériale ne change pas. Les locators ne sont pas déplacés; seuls les RGB de référence nécessaires et les listes prime_land suivent les subdivisions.

## Démographie, économie et armée

Population mondiale directement mesurée avant/après: **835801255**, delta0. Ce total n’est pas imposé comme règle historique; il résulte de la redistribution technique conservatrice retenue ici. Aucun dénombrement proche de1776 avec le périmètre exact des noyaux n’a été établi. Les nombres du tableau ne sont pas des populations historiques certifiées.

Tous les profils culture/religion, bâtiments écrits, niveaux, PM, propriétaires économiques, infrastructures, unités et recrutements sont conservés. Aucun bâtiment ni soldat n’est créé pour les nouveaux pays. Ressources et capacité agraire de la région73 inchangées. Les effets moteur sur la subsistance, les marchés et la viabilité des petits pays restent à tester; leur partage d’une même région économique ne certifie pas les positions de leurs centres historiques. Le noyau SSO n’inclut pas la ville physique de Sondershausen.

## Vérifications

{v['passed']}/{v['total']} contrôles statiques passent. Les17 tests ciblés et60 tests de contrats cumulés passent. Les73 sorties impériales ont été vérifiées avant modification puis après installation. Les44 doublons RGB et12 références invalides hérités sont inchangés.

Les49 tests d’anciennes photographies donnent42 succès et7 échecs, détaillés dans [LEGACY_TEST_TRIAGE.md](LEGACY_TEST_TRIAGE.md). Ces échecs ne sont pas masqués: plusieurs attendent le monde exact d’un ancien lot. Deux assertions Anhalt deviennent obsolètes avec MAP-2T; la préservation effective des cellules Anhalt est vérifiée indépendamment. Les autres comparaisons figées ou l’ancienne attente de Wolgast ne sont pas des nouveaux transferts MAP-2T. Aucune ancienne baseline n’est réécrite.

Le détail complet est dans [VALIDATION.json](VALIDATION.json) et [UNIT_TESTS.json](UNIT_TESTS.json). Le [plan de test](RUNTIME_TEST_PLAN.md) ne concerne que les modifications nouvelles. Les anciens PASS_RUNTIME_USER_VALIDATED restent des attestations manuelles limitées aux inspections précédentes.

## Fichiers

Les fichiers runtime modifiés sont énumérés exactement dans VALIDATION.json, champ runtime_files_modified. Ils comprennent les historiques de propriétaires et populations, définitions de six pays, correction de deux rangs, souverains et gouvernements, noms français/anglais, drapeaux abstraits, RGB/terrains, registre, carte du journal et17 sorties impériales adaptées. Aucun fichier de bâtiments, formations, diplomatie native ou types de sujets n’est changé.

Outils: tools/map2t_saxony.py, tools/test_map2t_saxony.py, tools/map2t_tables.mjs; extension explicitement limitée de tools/map2l_registry.py. HEAD et l’index Git sont inchangés. Aucun commit, merge, reset, push ou fichier de l’installation du jeu modifié.

## ColGrep

La tentative de localisation exploratoire de l’étape précédente n’a livré aucune sortie exploitable avant interruption. L’exécution réelle du modèle2B n’est donc pas certifiée pour cette tentative. Aucun nouvel appel redondant n’a été lancé lorsque les chemins étaient connus. Vérifications exactes effectuées par lecture et rg. Compteurs de tokens Codex et temps d’inférence local non disponibles: aucune économie chiffrée revendiquée.
'''
    files[prefix+'HISTORICAL_EVIDENCE.md']='''# Preuves utilisées et portée

## Sources conservées et réutilisées

R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv, lignes50–54: cinq propriétaires déjà signalés sans frontière microterritoriale démontrée. MAP2Q/R3/HRE_REGIONS_INVENTORY_UPDATED.csv et MAP2S/NEXT_HRE_REGION_RECOMMENDATION.md: secteur encore non reconstruit. Ces pistes ne sont pas transformées en preuves cartographiques.

## Cartographie comparative, pas preuve directe1776

[Putzger, États thuringiens1789, atlas publié1905](https://commons.wikimedia.org/wiki/File:Th%C3%BCringische_Staaten_1789_%E2%80%93_F._W._Putzgers_Historischer_Schul-Atlas_1905_(135770778).jpg). Fichier conservé dans EVIDENCE/PUTZGER_1789_1905.jpg; empreinte et dimensions dans SOURCE_FILE.json. Les remplissages historiques et indications des branches guident les noyaux. Les limites rouges des États et provinces contemporains de l’atlas ne sont pas utilisées comme frontières1776. Les polygones intérieurs sont conservés dans GEOMETRY.json et visibles sur SOURCE_TRACING_REVIEW.png.

## Souverainetés et dates

- [Landesarchiv, engagements des agents d’Altenbourg envers Ernst II en1772–1773](https://www.archive-in-thueringen.de/de/findbuch/view/bestand/21702/systematik/276244): Gotha–Altenbourg relève bien du même duché avant1776. [Biographie académique d’Ernst II](https://www.deutsche-biographie.de/sfz52922.html): règne1772–1804. Pas de création Cobourg–Gotha de1826.
- [Landesarchiv, Geheimes Archiv Hildburghausen](https://www.archive-in-thueringen.de/de/bestand/view/id/23365/bestand/23370): pleine souveraineté en1702, offices d’origine et acquisitions distingués. [Notice d’Ernst Friedrich III](https://www.deutsche-digitale-bibliothek.de/person/gnd/118954776): souverain contemporain. Ne pas importer son remplacement par Altenbourg en1826.
- [Landesarchiv, Amtsarchiv Heldburg](https://www.archive-in-thueringen.de/de/bestand/view/id/23369): filiation Hildburghausen jusqu’au réaménagement1826. [Themar/Römhild](https://www.archive-in-thueringen.de/en/bestand/view/id/23367/bestand/23377): juridictions partagées; elles ne sont pas attribuées unilatéralement dans les noyaux.
- [Inventaire institutionnel du Staatsarchiv Rudolstadt](https://landesarchiv.thueringen.de/media/landesarchiv/5Standorte/Rudolstadt/Veroeffentlichungen/Bestaendeuebersicht_2019_12_09.pdf): Rudolstadt et Sondershausen séparés, Oberherrschaft et Unterherrschaft distinguées. [Heidecksburg, souverains](https://www.heidecksburg.de/historie/regenten/): Ludwig Günther II règne1767–1790. [Stiftung Thüringer Schlösser, Sondershausen](https://www.thueringerschloesser.de/objekt/schloss-sondershausen-mit-park/): Christian Günther III règne1758–1794.
- [Ville de Greiz, chronologie](https://www.greiz.de/tourismus-kultur/tourismus/chronik): union des deux Greiz en1768, dignité princière seulement1778. [Deutsche Biographie, famille Reuss](https://www.deutsche-biographie.de/gnd118744674.html): pas d’unification de la jeune ligne avant1848. RGZ est donc un comté en1776, pas une principauté créée rétroactivement.
- [Heinrich XXX, Reuss-Gera, GND104254211](https://www.deutsche-biographie.de/gnd104254211.html): identité et dates1727–1802; pas d’annexion successorale de Gera en1802 appliquée au départ.
- [Heinrich XII, Reuss-Schleiz, GND104254254](https://www.deutsche-biographie.de/gnd104254254.html):1716–1784. Le souverain retenu n’est pas Heinrich XLII, qui lui succède en1784. Les archives de la [Landesdirektion Ebersdorf](https://www.archive-in-thueringen.de/en/findbuch/view/phrase/Me%C3%9F/exactphrase/1/limit/10/submit/Suche%2Bstarten/page/3/bestand/21761/systematik/83873) distinguent les maisons de Gera, Schleiz, Lobenstein et Ebersdorf et documentent les affaires des années1774–1779.

Ces sources institutionnelles établissent des souverainetés ou une chronologie. Elles ne valident pas séparément chacun des121 pixels transférés. La lecture du fond rétrospectif, sa correspondance au bitmap et la protection d’Erfurt restent des généralisations B explicites.

## Précision et arbitrage

Le profil MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json est conservé sans modification. La feuille nouvelle est ajustée au diagnostic déjà disponible, sans prétendre corriger la projection native. Les écarts de l’ajustement de la feuille ne sont pas des erreurs indépendantes de position des villes. Aucun hub agricole nommé Erfurt, aucune distance à une rivière et aucune translation7,20px ne justifie un transfert.

Les contours conservés sont limités à STATE_SAXONY. Pas de correction du nord prussien de la Saxe en1815, pas d’extension vers Anhalt, pas de nouvelle interprétation du chantier Erfurt. Lobenstein/Ebersdorf restent C: créer deux pays sur une séparation non identifiée serait arbitraire malgré leur existence politique établie. Les franges sont explicitement répertoriées comme incomplètes.

## Population

Aucune valeur de population historique datée au périmètre exact de ces noyaux tronqués n’a été identifiée dans les recherches retenues ou les notices consultées. La redistribution des historiques existants par parts techniques est déterministe, conserve chaque profil écrit et n’est pas présentée comme un recensement. Les surfaces ne produisent aucune nouvelle estimation démographique. Un chiffre territorial total d’une date postérieure ne serait pas applicable automatiquement à un noyau incomplet.

La tentative d’accès au PDF egierendef_rsten.pdf a renvoyé404. Il n’a pas servi à certifier les souverains; les notices accessibles ci-dessus sont utilisées.
'''
    files[prefix+'ERNESTINE_DUCHIES_AUDIT.md']='''# Duchés ernestins

GOT représente des noyaux de Gotha, Altenbourg et Roda; il est distinct de COB, désormais nommé Cobourg–Saalfeld. HIL a un noyau propre, distinct de MEI. WEI représente provisoirement les duchés de Weimar et Eisenach sous le même prince; cela n’affirme ni leur fusion constitutionnelle en1776 ni une nouvelle union personnelle native. Le rang de grand-duché post1815 est retiré.

Les noyaux sont des généralisations B, pas les duchés entiers. Les prolongements et enclaves, Themar/Römhild partagés, les possessions d’Eisenach et les franges du territoire technique COB ne sont pas tous résolus. La portion protégée d’Erfurt reste inchangée. Les deux RGB de COB en Franconie et leurs historiques ne sont pas réouverts.

Le pays électoral albertin SAX reste distinct des branches ernestines. Il conserve son droit électoral, son souverain déjà défini et ses institutions; son rang technique de royaume post1806 est retiré. Les possessions saxonnes devenues prussiennes en1815 hors périmètre ne sont pas restaurées par ce sous-lot.
'''
    files[prefix+'SCHWARZBURG_REUSS_AUDIT.md']='''# Schwarzbourg et Reuss

SCW est nommé Schwarzbourg-Rudolstadt et son souverain natif1836 est remplacé par Ludwig Günther II. SSO constitue un nouveau pays pour un noyau méridional Arnstadt/Gehren, sous Christian Günther III. Les Unterherrschaften autour de Sondershausen et Frankenhausen ne sont pas reconstruites. La capitale technique est la région73; le noyau méridional ne contient pas la ville physique de Sondershausen. Pas d’extension vers Anhalt ni Erfurt pour le compléter artificiellement.

RGZ, RGE et RSL distinguent Greiz, Gera et Schleiz sous leurs comtes de1776. Ils ne sont ni une jeune ligne unifiée en1848, ni des principautés auxquelles une élévation postérieure aurait été appliquée d’avance. La dignité princière de Greiz date1778. Heinrich XII, et non son successeur1784, gouverne Schleiz au départ.

Lobenstein et Ebersdorf sont deux souverainetés identifiées mais non installées: leurs contours respectifs ne sont pas encore suffisamment établis sur le bitmap à partir des pièces utilisées. Aucun couloir, aucune enclave d’un pixel forcée et aucun Köstritz souverain indépendant ne sont inventés. Les nouveaux noyaux ne certifient pas les franges, condominiums, droits de Schönburg ou enclaves militaires/fiscales.

Les lois/technologies de COB, les couleurs dynastiques et un lion reussien générique sont des abstractions techniques explicites, pas une certification des institutions ou pavillons de chaque maison.
'''
    failures=tests['prior_stage_snapshots']['failures']
    files[prefix+'LEGACY_TEST_TRIAGE.md']='''# Tests de photographies anciennes

Les17 tests ciblés et60 tests de contrats cumulatifs passent. Les49 tests historiques supplémentaires donnent42 succès,7 échecs,0 erreur. Aucun test ni baseline ancien n’est modifié pour obtenir un succès.

Deux assertions MAP2R attendent le monde entier de l’étape Anhalt et exactement trois pays supplémentaires depuis leur ancienne baseline. MAP2T ajoute six pays et change121 cellules en Saxe; ces attentes globales ne sont plus applicables. Tous les pixels hors STATE_SAXONY, y compris Anhalt, sont contrôlés identiques à la baseline immédiatement antérieure.

Les tests Q-R3/R8/R9 comparent aussi des bitmaps mondiaux arrêtés avant les lots postérieurs. L’attente R8 de la couleur E1A03A à Wolgast(4410,735) est déjà différente dans la baseline MAP2T et reste identique pendant ce lot. Le test O de registre attend l’ancien registre avant les migrations ultérieures, tandis que le nouveau contrôle effectue la relecture chronologique complète jusqu’à MAP2T. Les secteurs Q/M/O ne changent pas dans le présent bitmap. Ces échecs sont conservés comme diagnostics, pas convertis silencieusement en PASS.

## Identifiants des sept échecs

'''+''.join('- `'+f+'`\n' for f in failures)+'\nLes sorties réelles et traces restent dans UNIT_TESTS.json. Les contrôles différentiels de VALIDATION.json protègent les secteurs antérieurs sans exiger que le monde reste figé à leur date de livraison.\n'
    files[prefix+'RUNTIME_TEST_PLAN.md']='''# Test manuel ciblé MAP-2T

Statut: NOT_TESTED_MAP2T. Nouvelle partie nécessaire; une ancienne sauvegarde ne suffit pas à tester les historiques.

1. Vérifier l’apparition de GOT, HIL, SSO, RGZ, RGE et RSL avec un territoire non vide dans STATE_SAXONY. Comparer à SAXONY_THURINGIA_BEFORE_AFTER.png et aux cellules exactes du CSV.
2. Contrôler noms français, infobulles de gouvernement sans clés brutes, souverains1776 et drapeaux visibles. Greiz, Gera et Schleiz doivent être des comtés; SAX reste électoral, COB s’appelle Cobourg–Saalfeld.
3. Contrôler populations, capitales techniques dans la région73, accès au marché, subsistance, infrastructures, emploi et budget. Les nouveaux pays ne reçoivent ni bâtiments ni unités écrits artificiellement. La capitale physique Sondershausen n’est pas incluse; ne pas confondre capitale de région et centre urbain historique.
4. Confirmer appartenance impériale et droits de restitution des six membres ordinaires. Pas de nouvel électeur, pas de sujétion native automatique, pas de types centralisés activés. Vérifier les interactions électorales existantes sans modifier les icônes ou prototypes.
5. Vérifier visuellement qu’Erfurt–Eichsfeld, Anhalt, Eutin, Jever, la Peene et les anciens lots ne bougent pas. La carte du journal doit correspondre au registre; le mode carte conserve la même étendue.
6. Laisser passer un mois, vérifier absence de crash et diagnostic de chargement; relever les anomalies nouvelles séparément des44 RGB dupliqués/12 références invalides hérités.

Un compte rendu du joueur pourra enregistrer PASS_RUNTIME_USER_VALIDATED uniquement pour les modifications effectivement inspectées. Ni ces contrôles statiques ni l’ancien test MAP2R ne constituent une validation moteur MAP2T ou une certification historique des frontières.
'''
    files[prefix+'NEXT_HRE_REGION_RECOMMENDATION.md']='''# Suite recommandée, non commencée

Priorité: une continuation MAP2T-R1 dans le même secteur, ciblant la séparation documentée Lobenstein/Ebersdorf puis les Unterherrschaften de Schwarzbourg et les prolongements ernestins majeurs, sans rouvrir Erfurt ou Anhalt. Les six noyaux doivent d’abord être contrôlés en jeu.

Après clôture de cette continuation, une passe de Hesse pourrait être envisagée. Aucune autre région n’est commencée automatiquement. Le sous-lot livré n’est pas présenté comme un achèvement de toutes les juridictions thuringiennes.
'''
    dump('REPORTS_EXPECTED.json',files);core.OUT=OUT;print(core.emit(files,'REPORTS.patch'),flush=True)

if __name__ == '__main__':
    globals()[sys.argv[1]]()
