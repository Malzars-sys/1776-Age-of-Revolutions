"""MAP-2U: reviewed Reuss cores and northern Sondershausen, additive to MAP2T."""
import collections as C
import json
import re
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
import map2t_saxony as t

core=t.core; q=t.q; ROOT=t.ROOT
OUT=ROOT/'docs/reports/map/MAP2U'
NEW_TAGS=['RLO','REB']
REGIONS=['STATE_SAXONY','STATE_ANHALT']
NAMES={'RLO':('County of Reuss-Lobenstein','Comté de Reuss-Lobenstein'),
       'REB':('County of Reuss-Ebersdorf','Comté de Reuss-Ebersdorf'),
       'SSO':('Schwarzburg-Sondershausen','Schwarzbourg-Sondershausen')}

def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):
    return json.loads((OUT/name).read_text(encoding='utf8'))

EXTERNAL_BUILDINGS=[
 'common/history/buildings/99_1776_econ_paper_forestry_livestock.txt',
 'common/history/buildings/99_1776_prussian_forestry_addon.txt',
 'common/history/buildings/99_1776_prussian_start_micro_adjustment.txt']

def row_counter(rows):
    return C.Counter({json.dumps(r['key'],ensure_ascii=False):r['count'] for r in rows})

def expected_field(b,key):
    """Replay only the separately witnessed external building deltas."""
    base=row_counter(b['inventory'][key])
    if (OUT/'EXTERNAL_BUILDINGS_OBSERVED.json').exists() and key in ['buildings','building_levels_written']:
        observation=load('EXTERNAL_BUILDINGS_OBSERVED.json')
        assert set(observation['files'])==set(EXTERNAL_BUILDINGS)
        for row in observation['deltas'][key]:base[row['key']]+=row['delta']
    return base

def observe_external_buildings():
    assert not (OUT/'EXTERNAL_BUILDINGS_OBSERVED.json').exists(),'Observation is immutable'
    b=load('BASELINE.json');inv=core.qa.inventory();deltas={}
    for key in ['buildings','building_levels_written']:
        old=row_counter(b['inventory'][key]);now=row_counter(inv[key]);deltas[key]=[dict(key=k,delta=now[k]-old[k]) for k in sorted(set(old)|set(now)) if old[k]!=now[k]]
    levels={json.loads(r['key']):r['delta'] for r in deltas['building_levels_written']}
    assert levels=={'building_livestock_ranch':5,'building_logging_camp':2,'building_paper_mill':8},levels
    authorized_pairs={('STATE_AUSTRIA','AUS'),('STATE_BRANDENBURG','PRU'),('STATE_SAXONY','SAX'),('STATE_LOWER_SILESIA','PRU'),('STATE_UPPER_SILESIA','PRU'),('STATE_BAVARIA','BAV'),('STATE_POMERANIA','PRU'),('STATE_BRUNSWICK','PRU'),('STATE_WEST_PRUSSIA','PRU')}
    for row in deltas['buildings']:assert tuple(json.loads(row['key'])[:2]) in authorized_pairs,row
    hashes=q.economy.runtime_hashes();reference=load('PREINSTALL_CONCURRENT_SNAPSHOT.json')['hashes']
    own=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_FILES.json')['files'])|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    outside={p for p in set(hashes)|set(reference) if hashes.get(p)!=reference.get(p) and p not in own}
    assert outside==set(EXTERNAL_BUILDINGS),outside
    dump('EXTERNAL_BUILDINGS_OBSERVED.json',dict(provenance='Observed concurrent workspace edits after MAP2U installation; not authored or reverted by this lot',files={p:dict(before=reference.get(p),observed=hashes[p],text=(ROOT/p).read_text(encoding='utf-8-sig')) for p in EXTERNAL_BUILDINGS},deltas=deltas,level_delta=levels,MAP2U_building_changes=False))
    print('Recorded three external building edits; exact deltas',levels,flush=True)

def capture():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'BASELINE.json').exists(),'Immutable capture exists'
    inv=core.qa.inventory(); originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if any(sid in raw for sid in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    bitmap=t.OUT/'provinces_candidate.png'
    assert core.sha(bitmap)==core.sha(ROOT/'map_data/provinces.png')
    protected=['tools/map2l_registry.py','tools/map2k_imperial_system.py','tools/hre_centralization_01.py','tools/hre_subject_feedback_01.py','tools/hre_secession_lens_01.py']
    dump('BASELINE.json',dict(inventory=inv,originals=originals,hashes=q.economy.runtime_hashes(),
      bitmap_backup=bitmap.relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(bitmap),
      registry=json.loads(core.active_registry_path().read_text(encoding='utf8')),
      git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      git_index_sha256=core.sha(ROOT/'.git/index'),
      tool_originals={p:(ROOT/p).read_text(encoding='utf8') for p in protected},
      prior_records={p.relative_to(ROOT).as_posix():core.sha(p) for folder in ['MAP2R','MAP2S','MAP2T'] for p in (ROOT/'docs/reports/map'/folder).rglob('*') if p.is_file()}))
    print('Captured world',sum(r['count'] for r in inv['pops']),'; imperial RGBs',len(load('BASELINE.json')['registry']),flush=True)

def inspect():
    b=load('BASELINE.json');a=core.packed(ROOT/b['bitmap_backup']);rows=[]
    owner={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    for color in np.unique(a[813:852,4335:4380]):
        rgb='x'+format(int(color),'06X');ys,xs=np.where(a==color)
        rows.append(dict(rgb=rgb,region_owner=owner.get(rgb),pixels=len(xs),box=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]))
    dump('CURRENT_PROVINCES.json',rows)
    locators=q.r9.locators(a);dump('LOCATORS_BEFORE.json',[r for r in locators if r['ID'] in [62,70,73]])
    from map2o_east_frisia import panel
    panel(a,owner,(4335,813,4383,855),'MAP-2U avant / limites techniques',scale=20).save(OUT/'NATIVE_BEFORE.png')
    print(json.dumps(rows,ensure_ascii=False,indent=2),flush=True)

def compiler_before():
    old=t.OUT;t.OUT=OUT
    try:t.compiler_before()
    finally:t.OUT=old

def fetch():
    import urllib.request,urllib.parse
    from html.parser import HTMLParser
    class Links(HTMLParser):
        def handle_starttag(self,tag,attrs):
            for k,v in attrs:
                if k in ['src','href']:self.links.append(v)
    evidence=OUT/'EVIDENCE';evidence.mkdir(exist_ok=True)
    for title,url in [('Ebersdorf','https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_RjL_Eb_Vw.htm'),
                      ('Lobenstein','https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_RjL_Lo_Vw.htm'),
                      ('Sondershausen','https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_SS_Vw.htm')]:
        p=evidence/(title+'.html')
        raw=p.read_bytes() if p.exists() and title=='Ebersdorf' else urllib.request.urlopen(url,timeout=30).read();p.write_bytes(raw)
        parser=Links();parser.links=[];parser.feed(raw.decode('latin1'))
        print(title,parser.links,flush=True)
        for link in parser.links:
            if link.startswith('../gif/vSK820Th') and link.endswith(('.gif','.GIF')):
                imageurl=urllib.parse.urljoin(url,link);p=evidence/Path(link).name
                if not p.exists():p.write_bytes(urllib.request.urlopen(imageurl,timeout=30).read())
                print(p.name,imageurl,flush=True)

def source_grids():
    for label,name,box in [('EB','vSK820Th_RjL_Eb_Vw.gif',(0,350,270,530)),('LO','vSK820Th_RjL_Lo_Vw.gif',(0,350,270,530)),('SS','vSK820Th_SS_Vw.gif',(0,20,210,155))]:
        im=Image.open(OUT/'EVIDENCE'/name).convert('RGB').crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4))
        d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
        for x in range(box[0],box[2],20):
            px=(x-box[0])*4;d.line((px,0,px,im.height),fill='#6e84bd');d.text((px+1,0),str(x),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//20+1)*20,box[3],20):
            py=(y-box[1])*4;d.line((0,py,im.width,py),fill='#6e84bd');d.text((0,py+1),str(y),font=f,fill='blue',stroke_width=1,stroke_fill='white')
        im.save(OUT/(label+'_SOURCE_GRID.png'))

def geometry():
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup'])
    profile=ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json'
    model=json.loads(profile.read_text(encoding='utf8'))['model']
    controls_reuss=[('Gera',340,99,12.0833,50.8772),('Lobenstein',117,456,11.6396,50.4512),
        ('Ebersdorf',114,427,11.6525,50.4883),('Hirschberg',221,485,11.8211,50.4054),('Wurzbach',48,444,11.5389,50.4617)]
    controls_ss=[('Sondershausen',142,60,10.8643,51.3696),('Ebeleben',100,102,10.7296,51.2826),
        ('Keula',37,78,10.5318,51.3316),('Clingen',174,132,10.9327,51.2313),('Arnstadt',172,341,10.945,50.834)]
    transforms={};alignments={}
    for label,controls in [('REUSS',controls_reuss),('SS',controls_ss)]:
        source=np.array([[x,y,1] for _,x,y,_,_ in controls]);target=forward(model,[[lon,lat] for _,_,_,lon,lat in controls])
        tr=np.linalg.lstsq(source,target,rcond=None)[0];transforms[label]=tr
        alignments[label]=dict(transform=tr.tolist(),controls=[dict(name=n,source=[x,y],geo=[lon,lat],diagnostic_target=p.tolist(),sheet_residual=float(np.linalg.norm(np.array([x,y,1])@tr-p))) for (n,x,y,lon,lat),p in zip(controls,target)])
    traces=[
      ('RLO','Lobenstein main core','REUSS',[(106,443),(114,447),(120,453),(135,447),(164,448),(170,457),(149,462),(149,473),(128,478),(133,489),(122,499),(100,500),(94,504),(80,496),(72,491),(64,493),(58,488),(72,478),(83,475),(89,466),(94,459),(93,455),(102,449)]),
      ('REB','Ebersdorf-Wurzbach core','REUSS',[(23,441),(43,440),(49,432),(53,442),(60,447),(76,437),(96,432),(105,435),(109,423),(116,420),(120,434),(116,437),(108,437),(105,444),(95,448),(88,448),(81,457),(83,462),(71,469),(52,474),(42,477),(35,490),(29,492),(22,487),(24,471),(22,461),(18,455)]),
      ('REB','Hirschberg core','REUSS',[(198,472),(206,474),(215,467),(224,469),(230,477),(226,485),(212,490),(205,496),(202,486)]),
      ('SSO','Unterherrschaft northern core','SS',[(28,70),(40,63),(46,58),(55,65),(63,59),(73,69),(83,74),(93,70),(102,75),(110,71),(111,61),(119,56),(118,47),(125,41),(135,35),(147,42),(160,47),(171,43),(184,38),(189,47),(186,58),(194,65),(184,70),(178,82),(172,84),(177,98),(174,109),(184,116),(174,120),(167,116),(163,112),(155,111),(155,118),(163,125),(159,136),(144,135),(130,130),(124,129),(119,118),(106,123),(107,131),(97,135),(92,125),(88,118),(85,113),(85,103),(77,99),(72,106),(71,114),(64,114),(65,98),(56,92),(56,84),(49,83),(45,87),(36,84),(28,82),(31,77)])]
    owner={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    labels={};trace_rows=[]
    for tag,name,key,poly in traces:
        mapped=np.column_stack([poly,np.ones(len(poly))])@transforms[key]
        xmin,ymin=np.floor(mapped.min(axis=0)).astype(int);xmax,ymax=np.ceil(mapped.max(axis=0)).astype(int)
        yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx.ravel();yy=yy.ravel()
        mask=core.inside(np.column_stack([xx+.5,yy+.5]),mapped)&~t.protected_cells(xx,yy)
        included=[];excluded=[]
        for x,y in zip(xx[mask],yy[mask]):
            rgb='x'+format(int(before[y,x]),'06X');sid,old=owner[rgb]
            allowed=(tag=='SSO' and sid=='STATE_ANHALT' and old=='PRU' and rgb=='x3C9B93') or (tag in NEW_TAGS and sid=='STATE_SAXONY' and old in ['WEI','SAX'] and not rgb.startswith('xEDB4'))
            if not allowed:excluded.append([int(x),int(y),sid,old]);continue
            assert (int(x),int(y)) not in labels,'Overlapping claims'
            labels[int(x),int(y)]=tag;included.append([int(x),int(y)])
        trace_rows.append(dict(tag=tag,name=name,source=key,source_polygon=poly,game_polygon=mapped.tolist(),included=included,excluded=excluded,confidence='B',basis='Inward IEG 1820 core, corroborated by pre-1776 dynastic continuity and Putzger 1789; residual boundaries not certified'))
    # The narrow Ebersdorf residence territory is sub-pixel across its width.
    # Quantize its mapped core to one cell, not the whole surrounding province.
    # The source polygon genuinely intersects the cell; no corridor is added.
    x,y=4365,845
    assert owner['x'+format(int(before[y,x]),'06X')]==['STATE_SAXONY','WEI']
    sample_y,sample_x=np.mgrid[0:64,0:64]
    points=np.column_stack([x+(sample_x.ravel()+.5)/64,y+(sample_y.ravel()+.5)/64])
    overlap=float(core.inside(points,np.array(trace_rows[1]['game_polygon'])).mean())
    assert overlap>.1 and (x,y) not in labels
    labels[x,y]='REB';trace_rows[1]['included'].append([x,y])
    trace_rows[1]['one_cell_quantization']=dict(cell=[x,y],inward_polygon_coverage=overlap,reason='Sub-pixel residence core generalized to one playable cell; not a surveyed border or entire neighboring province')
    parents=sorted({'x'+format(int(before[y,x]),'06X') for x,y in labels})
    after=before.copy();assignments=[];new=[];used=set(map(int,np.unique(before)));color=0xEDB500
    for parent in parents:
        sid,old=owner[parent];ys,xs=np.where(before==int(parent[1:],16));tags=np.array([labels.get((int(x),int(y)),old) for x,y in zip(xs,ys)])
        for tag in sorted(set(tags)):
            mask=np.zeros(before.shape,bool);mask[ys[tags==tag],xs[tags==tag]]=True
            for i,part in enumerate(core.components(mask)):
                if tag==old and i==0:rgb=parent
                else:
                    while color in used:color+=1
                    rgb='x'+format(color,'06X');used.add(color);color+=1;new.append(dict(rgb=rgb,parent_rgb=parent))
                py=np.array([p[0] for p in part]);px=np.array([p[1] for p in part]);after[py,px]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=old,owner=tag,pixels=len(part),cells=[[int(x),int(y)] for y,x in part],confidence='B' if tag!=old else 'C_RETAINED'))
    assert all(any(a['owner']==tag for a in assignments) for tag in NEW_TAGS+['SSO'])
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,traces=trace_rows,new_members=NEW_TAGS,hub_rebindings=[]))
    dump('SOURCE_ALIGNMENT.json',dict(sources=alignments,native_profile=str(profile.relative_to(ROOT)),native_profile_sha256=core.sha(profile),native_model_refitted=False,independent_error_bound_px=None,warning='Source-sheet alignment only. No regional recalibration or rejected 7.20px translation.'))
    for label in ['EB','LO','SS']:
        name={'EB':'vSK820Th_RjL_Eb_Vw.gif','LO':'vSK820Th_RjL_Lo_Vw.gif','SS':'vSK820Th_SS_Vw.gif'}[label]
        image=Image.open(OUT/'EVIDENCE'/name).convert('RGB');d=ImageDraw.Draw(image)
        for a in trace_rows:
            if (label=='LO' and a['tag']=='RLO') or (label=='EB' and a['tag']=='REB') or (label=='SS' and a['tag']=='SSO'):d.line(a['source_polygon']+[a['source_polygon'][0]],fill='blue',width=1)
        image.resize((image.width*3,image.height*3)).save(OUT/(label+'_TRACING_REVIEW.png'))
    print('Transfers',dict(C.Counter(labels.values())),'new RGBs',len(new),'parents',parents,flush=True)

def countries(files,migration):
    defs=''.join(tag+' = { color = { '+color+' } country_type = recognized tier = principality cultures = { north_german } religion = protestant capital = STATE_SAXONY }\n' for tag,color in [('RLO','190 137 178'),('REB','134 184 132')])
    files['common/country_definitions/1776_map2u_reuss.txt']=defs
    migration['country_additions']={n.key:core.qa.signature(n) for n in core.cw.parse(defs)}
    # Engine has no native county tier; the government and ruler title are comital.
    template=(ROOT/'common/history/countries/cob - saxe-coburg-gotha.txt').read_text(encoding='utf-8-sig')
    for tag in NEW_TAGS:files['common/history/countries/'+tag.lower()+' - map2u.txt']=template.replace('c:COB','c:'+tag)
    rulers={'RLO':('Heinrich II.','Reuss-Lobenstein','1702.7.19'),'REB':('Heinrich XXIV.','Reuss-Ebersdorf','1724.1.22')}
    for tag,(_,_,born) in rulers.items():
        files['common/history/characters/'+tag.lower()+' - map2u.txt']='CHARACTERS = { c:'+tag+' ?= { create_character = { first_name = aor1776_map2u_'+tag.lower()+'_first last_name = aor1776_map2u_'+tag.lower()+'_last historical = yes culture = north_german religion = rel:protestant ruler = yes birth_date = '+born+' interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    files['common/flag_definitions/1776_map2u.txt']='# Shared Reuss dynastic arms are temporary graphical approximations, not political union.\n'+''.join(tag+' = { flag_definition = { coa = aor1776_map2t_reuss priority = 100 allow_overlord_canton = no } }\n' for tag in NEW_TAGS)
    files['common/government_types/00_1776_map2u.txt']='gov_aor1776_map2u_county = { transfer_of_power = hereditary male_ruler = "RULER_TITLE_COUNT" female_ruler = "RULER_TITLE_COUNTESS" possible = { OR = { c:RLO ?= this c:REB ?= this } has_law = law_type:law_monarchy } on_government_type_change = { change_to_hereditary = yes } on_post_government_type_change = { post_change_to_hereditary = yes } }\n'
    for lang,index in [('english',0),('french',1)]:
        loc='\ufeffl_'+lang+':\n'
        for tag in NEW_TAGS:
            adjective=('Reuss-Lobenstein' if tag=='RLO' else 'Reuss-Ebersdorf') if lang=='english' else 'reussien'
            loc+=' '+tag+':0 "'+NAMES[tag][index]+'"\n '+tag+'_ADJ:0 "'+adjective+'"\n'
            first,last,_=rulers[tag]
            loc+=' aor1776_map2u_'+tag.lower()+'_first:0 "'+first+'"\n aor1776_map2u_'+tag.lower()+'_last:0 "'+last+'"\n'
        loc+=' gov_aor1776_map2u_county:0 "'+('Imperial county' if lang=='english' else 'Comté impérial')+'"\n'
        desc=('The count or countess governs this hereditary county of the Empire according to the succession of the ruling house.' if lang=='english' else 'Le comte ou la comtesse gouverne ce comté de l’Empire selon la succession héréditaire de la maison régnante.')
        loc+=' gov_aor1776_map2u_county_desc:0 "'+desc+'\\n\\n$TRANSFER_OF_POWER_NAME_DESC$"\n'
        files[f'localization/{lang}/1776_map2u_l_{lang}.yml']=loc
    rel='common/country_definitions/1776_map2t_saxony.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig')
    node=next(n for n in core.cw.parse(raw) if n.key=='SSO');f=node.children('capital')[0];assert f.value=='STATE_SAXONY'
    edited=core.edits(raw,[(f.start,f.end,'capital = STATE_ANHALT')]);files[rel]=edited
    new=next(n for n in core.cw.parse(edited) if n.key=='SSO')
    migration['country_capital_corrections']=[dict(tag='SSO',before='STATE_SAXONY',after='STATE_ANHALT',before_signature=core.qa.signature(node),after_signature=core.qa.signature(new))]

def prepare():
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};bindings=[]
    observed=load('CONCURRENT_WORK_OBSERVED.json')
    current=q.economy.runtime_hashes()
    touched_old=set(b['originals'])|{'map_data/provinces.png','map_data/province_terrains.txt','common/country_definitions/1776_map2t_saxony.txt'}
    drift={p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)}
    assert not drift&touched_old,'Concurrent edits overlap MAP2U targets: '+str(drift&touched_old)
    # Additive collaborator snapshot, never rewrite the immutable MAP2U capture.
    if not (OUT/'PREINSTALL_CONCURRENT_SNAPSHOT.json').exists():
        dump('PREINSTALL_CONCURRENT_SNAPSHOT.json',dict(hashes=current,inventory=core.qa.inventory(),files=sorted(drift),not_map2u_changes=True))
    assert load('COMPILER_BEFORE.json')['passed']==73
    assert not set(NEW_TAGS)&set(b['inventory']['countries'])
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png')
    byparent=C.defaultdict(list)
    for a in g['assignments']:byparent[a['parent_rgb']].append(a)
    rel='common/history/states/00_states.txt';raw=b['originals'][rel];ops=[]
    for sid in REGIONS:
        s=core.state(raw,sid);existing=set()
        for n in s.children('create_state'):
            tag=n.one('country').removeprefix('c:');existing.add(tag);f=n.children('owned_provinces')[0];old=core.values(n,'owned_provinces');new=[]
            for rgb in old:new.extend(a['rgb'] for a in byparent[rgb] if a['owner']==tag) if rgb in byparent else new.append(rgb)
            # Include incoming fragments when a receiver already owns part of this region.
            new.extend(a['rgb'] for a in g['assignments'] if a['state']==sid and a['owner']==tag and a['previous_owner']!=tag)
            if old!=new:ops.append((f.start,f.end,'owned_provinces = { '+' '.join(new)+' }'))
        added=[tag for tag in NEW_TAGS+['SSO'] if tag not in existing and any(a['state']==sid and a['owner']==tag for a in g['assignments'])]
        if added:ops.append((s.end-1,s.end-1,'\n'+''.join('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(a['rgb'] for a in g['assignments'] if a['state']==sid and a['owner']==tag)+' } }\n' for tag in added)))
    files[rel]=core.edits(raw,sorted(ops))
    for rel,raw in b['originals'].items():
        if not rel.startswith('map_data/state_regions/'):continue
        ops=[]
        for s in core.cw.parse(raw):
            if s.key not in REGIONS:continue
            sid=s.key
            for field in ['provinces','prime_land']:
                for f in s.children(field):
                    old=core.values(s,field);new=[]
                    for rgb in old:new.extend(a['rgb'] for a in byparent[rgb]) if rgb in byparent else new.append(rgb)
                    if old!=new:
                        ops.append((f.start,f.end,field+' = { '+' '.join('"'+c+'"' for c in new)+' }'))
                        if field=='prime_land':bindings.append(dict(state=sid,field=field,before=old,after=new))
            for loc in load('LOCATORS_BEFORE.json'):
                if loc['ID']!={'STATE_SAXONY':73,'STATE_ANHALT':62}[sid]:continue
                x,y=int(loc['X']),int(loc['Y']);rgb='x'+format(int(after[y,x]),'06X');old=core.cw.scalar(s.one(loc['Kind']))
                if old!=rgb:
                    f=s.children(loc['Kind'])[0];ops.append((f.start,f.end,loc['Kind']+' = "'+rgb+'"'))
                    bindings.append(dict(state=sid,field=loc['Kind'],before=old,after=rgb,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
        if ops:files[rel]=core.edits(raw,sorted(ops))
    owner={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};weights={};allocations=[]
    for sid,donor in sorted({(a['state'],a['previous_owner']) for a in g['assignments']}):
        total=sum(int(np.sum(before==int(rgb[1:],16))) for rgb,(s,tag) in owner.items() if (s,tag)==(sid,donor))
        transfers=C.Counter()
        for a in g['assignments']:
            if (a['state'],a['previous_owner'])==(sid,donor) and a['owner']!=donor:transfers[a['owner']]+=a['pixels']
        weights[sid+'|'+donor]={donor:total-sum(transfers.values()),**dict(transfers)}
    for rel,raw in b['originals'].items():
        if '/pops/' not in rel:continue
        text=raw;ops=[];pieces=C.defaultdict(list)
        for sid in REGIONS:
            try:s=core.state(raw,sid)
            except (StopIteration,IndexError):continue
            for node in s.children():
                if not node.key.startswith('region_state:'):continue
                donor=node.key.split(':')[1];w=weights.get(sid+'|'+donor)
                if not w:continue
                for pop in node.children('create_pop'):
                    f=pop.children('size')[0];amounts=core.allocate(int(f.value),w)
                    ops.append((f.start,f.end,'size = '+str(amounts.get(donor,0))))
                    for tag,amount in amounts.items():
                        if tag!=donor and amount:pieces[sid,tag].append(core.edits(raw[pop.start:pop.end],[(f.start-pop.start,f.end-pop.start,'size = '+str(amount))]))
                    allocations.append(dict(state=sid,donor=donor,culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:'+pop.one('culture')),before=int(f.value),after=amounts))
        if ops:
            text=core.edits(raw,sorted(ops))
            for (sid,tag),parts in pieces.items():text=core.append(text,sid,tag,'\n'.join(parts))
            files[rel]=text
    dump('POPULATION_ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_REDISTRIBUTION_NOT_HISTORICAL_CENSUS',weights=weights,profiles=allocations,reason='No close dated count matches the installed clipped nuclei. The 1820 approximate Ebersdorf total and 1800 urban count are not 1776 country populations.'))
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw+'\n'+''.join(a['rgb']+'="'+terrain[a['parent_rgb'].upper()]+'"\n' for a in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state'] in REGIONS]
    updated=[r for r in previous if r['rgb'] not in g['parents']]+[dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2U B core/quantization, C residual retained; see GEOMETRY.json and HISTORICAL_EVIDENCE.md.') for a in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state'] not in REGIONS]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    migration=dict(replaced_regions=REGIONS,previous=previous,updated=updated,new_members=NEW_TAGS,free_cities=[],new_provinces=g['new_provinces'],geometry='MAP2U/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[])
    countries(files,migration)
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
        if rel in b['originals']:assert (ROOT/rel).read_text(encoding='utf-8-sig')==b['originals'][rel],rel
    dump('EXPECTED_TEXT.json',files);core.OUT=OUT;changes=core.emit(files,'HISTORY.patch')
    dump('PLAN.json',dict(files=changes,registered_RGBs=len(ledger),region_reference_changes=bindings))
    print('Prepared',len(changes),'files; registry',len(ledger),flush=True)

def install():
    old=t.OUT;t.OUT=OUT
    try:t.install()
    finally:t.OUT=old

def imperial():
    old=t.OUT;t.OUT=OUT
    try:t.imperial()
    finally:t.OUT=old

def maps():
    from georeference.model import forward,inverse
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png')
    old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};new=dict(old)
    for a in g['assignments']:new[a['rgb']]=a['owner']
    palette={'SSO':'#a886c2','RLO':'#c789b3','REB':'#8ac08e','PRU':'#879eb5','WEI':'#b9c47f','SAX':'#d9ca94','SCW':'#bdb3cd','GOT':'#edd389','RSL':'#99938c','RGZ':'#82becb','RGE':'#d99a61','COB':'#c5ac8c','MEI':'#94ac9a','HIL':'#78c3aa'}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
    towns=[('Sondershausen',10.8643,51.3696),('Ebeleben',10.7296,51.2826),('Erfurt',11.0328,50.9787),('Gera',12.0833,50.8772),('Bad Lobenstein',11.6396,50.4512),('Ebersdorf',11.6525,50.4883),('Hirschberg',11.8211,50.4054),('Schleiz',11.8148,50.5798),('Weimar',11.3290,50.9803),('Leipzig',12.3731,51.3397)]
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text(encoding='utf8'))['model']
    pixels=forward(model,[[lon,lat] for _,lon,lat in towns]);box=(4338,815,4385,852);x0,y0,x1,y1=box;scale=18
    def panel(array,owners,title):
        local=array[y0:y1,x0:x1];rgb=np.zeros((*local.shape,3),dtype='uint8')
        for color in np.unique(local):rgb[local==color]=ImageColor.getrgb(palette.get(owners.get('x'+format(int(color),'06X')),'#c1c8cc'))
        edges=np.zeros(local.shape,bool);edges[:,1:]|=local[:,1:]!=local[:,:-1];edges[1:,:]|=local[1:,:]!=local[:-1,:]
        im=Image.fromarray(rgb).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST)
        p=Image.new('RGB',(im.width,im.height+165),'#fcfaf5');p.paste(im,(0,42));d=ImageDraw.Draw(p);d.text((14,9),title,font=bold,fill='#202d3a')
        for a in g['assignments']:
            if a['owner']==a['previous_owner']:continue
            for x,y in a['cells']:
                if x0<=x<x1 and y0<=y<y1:d.rectangle(((x-x0)*scale,(y-y0)*scale+42,(x-x0+1)*scale-1,(y-y0+1)*scale+41),outline='#263c36',width=2)
        offsets={'Sondershausen':(20,-28),'Ebeleben':(-110,12),'Erfurt':(-5,-25),'Gera':(15,-10),'Bad Lobenstein':(-180,30),'Ebersdorf':(-155,-38),'Hirschberg':(22,30),'Schleiz':(20,-20),'Weimar':(12,-30),'Leipzig':(-40,-28)}
        for (name,_,_),point in zip(towns,pixels):
            x,y=(point-[x0,y0])*scale;y+=42
            if not 0<x<p.width or not 42<y<im.height+42:continue
            dx,dy=offsets[name];d.ellipse((x-3,y-3,x+3,y+3),fill='#212121',outline='white');d.line((x,y,x+dx,y+dy+8),fill='#333333');d.text((x+dx,y+dy),name,font=small,fill='#101010',stroke_width=2,stroke_fill='#fffdf7')
        d.rectangle(((4342-x0)*scale,(822-y0)*scale+42,(4359-x0)*scale,(837-y0)*scale+42),outline='#c35451',width=2)
        for i,(tag,color) in enumerate(palette.items()):
            xx=12+(i%7)*118;yy=im.height+54+(i//7)*25;d.rectangle((xx,yy,xx+13,yy+13),fill=color);d.text((xx+19,yy-2),tag,font=small,fill='black')
        d.text((12,im.height+111),'Contours B généralisés. Cadre rouge : Erfurt exclu.',font=small,fill='#343434')
        d.text((12,im.height+135),'Points de villes : projection diagnostique, pas des locators certifiés.',font=small,fill='#343434')
        return p
    a=panel(before,old,'AVANT MAP-2U');z=panel(after,new,'APRÈS MAP-2U : territoires installés')
    comparison=Image.new('RGB',(a.width+z.width+20,a.height),'#fcfaf5');comparison.paste(a,(0,0));comparison.paste(z,(a.width+20,0));comparison.save(OUT/'THURINGIA_BEFORE_AFTER.png')
    # Geographic companion: real modern town coordinates plus inverse-projected
    # installed cell footprints. These are two explicit layers, not a GPS claim.
    geo=Image.new('RGB',(900,873),'#fcfaf5');d=ImageDraw.Draw(geo)
    d.text((20,14),'Repères modernes et noyaux modifiés',font=bold,fill='#202d3a')
    limits=(10.2,50.2,12.6,51.6)
    def plot(lon,lat):return (65+(lon-limits[0])/(limits[2]-limits[0])*760,65+(limits[3]-lat)/(limits[3]-limits[1])*620)
    for lon in np.arange(10.25,12.6,.25):
        x,_=plot(lon,51.6);d.line((x,65,x,685),fill='#dedfdc');d.text((x-15,688),f'{lon:.2f}°E',font=small,fill='#65717a')
    for lat in np.arange(50.25,51.61,.25):
        _,y=plot(10.2,lat);d.line((65,y,825,y),fill='#dedfdc');d.text((4,y-9),f'{lat:.2f}°N',font=small,fill='#65717a')
    for a in g['assignments']:
        if a['owner']==a['previous_owner']:continue
        for x,y in a['cells']:
            corners=inverse(model,[[x,y],[x+1,y],[x+1,y+1],[x,y+1]])
            d.polygon([plot(lon,lat) for lon,lat in corners],fill=palette[a['owner']],outline='#3f534c')
    placements={'Sondershausen':(10,-30),'Ebeleben':(-105,16),'Erfurt':(-65,10),'Gera':(12,0),'Bad Lobenstein':(-145,25),'Ebersdorf':(-120,-30),'Hirschberg':(16,24),'Schleiz':(20,-20),'Weimar':(0,-28),'Leipzig':(-15,-26)}
    for name,lon,lat in towns:
        x,y=plot(lon,lat);dx,dy=placements[name];d.ellipse((x-4,y-4,x+4,y+4),fill='#172b35');d.line((x,y,x+dx,y+dy+8),fill='#56656b');d.text((x+dx,y+dy),name,font=font,fill='#10212c',stroke_width=2,stroke_fill='#fcfaf5')
    for i,tag in enumerate(['SSO','RLO','REB']):
        y=736+i*28;d.rectangle((24,y,40,y+16),fill=palette[tag]);d.text((49,y-1),tag+' — '+NAMES[tag][1],font=font,fill='#172b35')
    d.text((24,828),'Empreintes du jeu reprojetées approximativement ; frontières B, pas un cadastre.',font=small,fill='#5c3333')
    d.text((24,851),'Ebeleben et Clingen partiellement différés pour préserver le secteur d’Erfurt.',font=small,fill='#5c3333')
    player=Image.new('RGB',(geo.width+z.width+20,873),'#fcfaf5');player.paste(geo,(0,0));player.paste(z,(geo.width+20,0));player.save(OUT/'PLAYER_LOCATION_GUIDE.png')
    dump('MODERN_REFERENCE_POINTS.json',[dict(name=name,longitude=lon,latitude=lat,diagnostic_pixel=p.tolist(),not_certified_native_locator=True) for (name,lon,lat),p in zip(towns,pixels)])
    print('Before/after and geographic player guide generated.',flush=True)

def journal():
    import render_map2k_imperial_map as render
    render.OUT=OUT;render.render()

def validate():
    from map2l_registry import expected_country_definitions,apply_territorial_migrations,approved_territorial_extensions,protected_core_preserved
    b=load('BASELINE.json');g=load('GEOMETRY.json');m=load('REGISTRY_MIGRATION.json');inv=core.qa.inventory();dump('CURRENT_INVENTORY.json',inv)
    checks=[]
    def check(name,passed,detail=None):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
        if not passed:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy()
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']};eo=counter(b['inventory']['owners'])
    for key in list(eo):
        if key[0] in g['parents']:del eo[key]
    for a in g['assignments']:
        for x,y in a['cells']:expected[y,x]=int(a['rgb'][1:],16)
        eo[a['rgb'],a['state'],a['owner']]=1
        check('Owner/state '+a['rgb'],owners.get(a['rgb'])==[a['state'],a['owner']])
        check('Exact cells '+a['rgb'],int(np.sum(after==int(a['rgb'][1:],16)))==a['pixels'])
        check('Connected RGB '+a['rgb'],len(core.components(after==int(a['rgb'][1:],16)))==1)
    check('Exact world bitmap delta',np.array_equal(expected,after))
    check('Exact world owners delta',counter(inv['owners'])==eo)
    check('Erfurt guard unchanged',np.array_equal(before[822:837,4342:4359],after[822:837,4342:4359]))
    prior=t.load('GEOMETRY.json');simple_owner={rgb:row[1] for rgb,row in owners.items()}
    for a in prior['assignments']:
        if a['owner']!=a['previous_owner'] or a['rgb']!=a['parent_rgb']:
            check('MAP2T frozen core/RGB '+a['rgb'],protected_core_preserved(a,after,simple_owner,[]))
    check('All 121 prior transfers remain protected',sum(a['pixels'] for a in prior['assignments'] if a['owner']!=a['previous_owner'])==121)
    for a in t.prior.load('GEOMETRY.json')['assignments']:
        check('Anhalt principality cells '+a['rgb'],protected_core_preserved(a,after,simple_owner,[]))
    for key in ['units','duplicates','errors','resolved_demographics','pops']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    for key in ['buildings','building_levels_written']:
        check('Building data plus exact witnessed external delta '+key,row_counter(inv[key])==expected_field(b,key))
    state_types=dict(b['inventory']['state_types']);state_types.update({'STATE_SAXONY|RLO':'incorporated_default','STATE_SAXONY|REB':'incorporated_default','STATE_ANHALT|SSO':'incorporated_default'})
    check('Only three new state subdivisions',inv['state_types']==state_types)
    check('Only authorized country definitions',inv['countries']==expected_country_definitions(b['inventory']['countries'],[m]))
    ep=counter(b['inventory']['regional_pop'])
    for row in load('POPULATION_ALLOCATION.json')['profiles']:
        ep[row['state'],row['donor'],row['culture'],row['religion']]-=row['before']
        for tag,amount in row['after'].items():ep[row['state'],tag,row['culture'],row['religion']]+=amount
        check('Integer conservation '+row['state']+' '+row['donor']+' '+row['culture']+' '+row['religion'],sum(row['after'].values())==row['before'] and all(isinstance(n,int) and n>=0 for n in row['after'].values()))
    check('Exact regional demographic delta',counter(inv['regional_pop'])==ep)
    world=sum(r['count'] for r in inv['pops']);oldworld=sum(r['count'] for r in b['inventory']['pops'])
    check('Reference world verified',oldworld==835801255)
    check('No artificial population added',world==oldworld)
    check('HLB population unchanged',sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='HLB')==9206)
    check('Existing SSO southern population unchanged',[r for r in inv['regional_pop'] if r['key'][:2]==['STATE_SAXONY','SSO']]==[r for r in b['inventory']['regional_pop'] if r['key'][:2]==['STATE_SAXONY','SSO']])
    for tag in NEW_TAGS:
        check('New country populated '+tag,sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag)>0)
        check('New capital has territory '+tag,any(r['key'][1:]==['STATE_SAXONY',tag] for r in inv['owners']))
        history=(ROOT/('common/history/countries/'+tag.lower()+' - map2u.txt')).read_text(encoding='utf8')
        check('No imperial native subjection '+tag,'create_diplomatic_pact' not in history)
        check('Declared country template preserved '+tag,'effect_starting_politics_conservative' in history)
    check('Sondershausen diagnostic point lies in SSO',owners.get('x'+format(int(after[819,4348]),'06X'))==['STATE_ANHALT','SSO'])
    check('No arbitrary urban locator added',all(core.sha(ROOT/p)==h for p,h in b['hashes'].items() if p.startswith('gfx/map/map_object_data/')))
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'))
    om=np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]);nm=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
    check('Imperial physical extent unchanged',np.array_equal(om,nm))
    check('Unique registry and count',len(ledger)==len({r['rgb'] for r in ledger})==541)
    for row in ledger:check('Imperial title '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']])
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry']
    belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'));regions={a['state'] for a in belgian['assignments']}
    frozen=[r for r in initial if r['state'] not in regions]+[dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for a in belgian['assignments']]+approved_territorial_extensions()
    replay=apply_territorial_migrations(frozen);check('Cumulative registry replay',replay==ledger)
    import prototype_map2k_main_map as main_map
    mask=np.array(Image.open(ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds').convert('RGBA'))[:,:,0]==255
    x0,y0=main_map.ORIGIN;check('Main imperial map mask unchanged and correct',np.array_equal(mask,nm[y0:y0+main_map.TILE,x0:x0+main_map.TILE]))
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={rgb.upper():v for rgb,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for a in g['new_provinces']:
        check('New RGB absent before '+a['rgb'],not np.any(before==int(a['rgb'][1:],16)))
        check('Terrain once/inherited '+a['rgb'],len(re.findall(r'(?im)^\s*'+a['rgb']+r'\s*=',terrain))==1 and tm[a['rgb'].upper()]==tm[a['parent_rgb'].upper()])
        check('New RGB state defined '+a['rgb'],inv['geometry'].get(a['rgb'])==next(r['state'] for r in g['assignments'] if r['rgb']==a['rgb']))
    for rel,raw in load('EXPECTED_TEXT.json').items():
        check('Exact reviewed file '+rel,(ROOT/rel).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip())
        if rel.endswith('.txt'):
            try:core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'));check('Parse '+rel,True)
            except Exception as exc:check('Parse '+rel,False,str(exc))
        if rel in b['originals'] and '/history/' in rel:
            previous=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(b['originals'][rel])) if n.key.startswith('s:STATE_') and n.key[2:] not in REGIONS]
            now=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(raw)) if n.key.startswith('s:STATE_') and n.key[2:] not in REGIONS]
            check('Other state history unchanged '+rel,previous==now)
        if rel.startswith('map_data/state_regions/'):
            old={n.key:n for n in core.cw.parse(b['originals'][rel])};new={n.key:n for n in core.cw.parse(raw)}
            for sid,node in old.items():
                exclude={'provinces'}|{r['field'] for r in m['region_reference_changes'] if r['state']==sid}
                check('Resources ID arable traits '+sid,[core.qa.signature(n) for n in node.children() if n.key not in exclude]==[core.qa.signature(n) for n in new[sid].children() if n.key not in exclude])
        if rel.endswith('.yml'):
            check('Localization BOM '+rel,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
            check('Localization header '+rel,raw.lstrip('\ufeff').startswith('l_'+('french' if '/french/' in rel else 'english')+':'))
    for rel,raw in load('IMPERIAL_EXPECTED.json').items():check('Compiled imperial '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    from map2k_patch import ELECTORS
    check('SAX only existing electoral rights','SAX' in ELECTORS.values() and not set(NEW_TAGS)&set(ELECTORS.values()))
    current=q.economy.runtime_hashes();reference=load('PREINSTALL_CONCURRENT_SNAPSHOT.json');changed=sorted(p for p in set(current)|set(reference['hashes']) if current.get(p)!=reference['hashes'].get(p))
    allowed=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_FILES.json')['files'])|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    external=load('EXTERNAL_BUILDINGS_OBSERVED.json') if (OUT/'EXTERNAL_BUILDINGS_OBSERVED.json').exists() else dict(files={})
    outside=[p for p in changed if p not in allowed and p not in external['files']]
    check('No undocumented runtime changes after collaborator snapshot',not outside,outside)
    for p,record in external['files'].items():check('Witnessed external file preserved '+p,current.get(p)==record['observed'])
    for folder in ['buildings','military_formations','diplomacy','subject_types']:
        check('Original '+folder+' files preserved except witnessed external edits',all(current.get(p)==external['files'].get(p,{}).get('observed',h) for p,h in reference['hashes'].items() if '/'+folder+'/' in p))
    for p in ['tools/map2k_imperial_system.py','tools/hre_centralization_01.py','tools/hre_subject_feedback_01.py','tools/hre_secession_lens_01.py']:
        check('Independent imperial mechanics tool '+p,(ROOT/p).read_text(encoding='utf8')==b['tool_originals'][p])
    from localization_duplicate_audit import entries
    for lang in ['english','french']:
        entries_by_key=entries(lang)
        rel=f'localization/{lang}/1776_map2u_l_{lang}.yml'
        keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0\s+"',load('EXPECTED_TEXT.json')[rel],re.M)
        for key in keys:check('Unique localization '+lang+' '+key,len(entries_by_key.get(key,[]))==1)
        check('Complete matching localization keys '+lang,len(keys)==10)
        native=(core.GAME/f'localization/{lang}/government_l_{lang}.yml').read_text(encoding='utf-8-sig') if hasattr(core,'GAME') else (Path('C:/Games/Victoria 3/game')/f'localization/{lang}/government_l_{lang}.yml').read_text(encoding='utf-8-sig')
        check('Native count titles exist '+lang,all(re.search(r'^\s*'+key+r':',native,re.M) for key in ['RULER_TITLE_COUNT','RULER_TITLE_COUNTESS']))
    coa=(ROOT/'common/coat_of_arms/coat_of_arms/1776_map2t.txt').read_text(encoding='utf8')
    check('Referenced Reuss arms defined','aor1776_map2t_reuss' in coa)
    check('Old SSO government/ruler untouched',all(current.get(p)==h for p,h in b['hashes'].items() if p in ['common/government_types/00_1776_map2t.txt','common/history/characters/sso - map2t.txt']))
    check('Prior reports/baselines unchanged',all((ROOT/p).exists() and core.sha(ROOT/p)==h for p,h in b['prior_records'].items()))
    check('Native diagnostic projection unchanged',core.sha(ROOT/load('SOURCE_ALIGNMENT.json')['native_profile'])==load('SOURCE_ALIGNMENT.json')['native_profile_sha256'])
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    dump('WORLD_POPULATION_DELTA.json',dict(before=oldworld,after=world,delta=world-oldworld,historical_estimate_applied=False,method=load('POPULATION_ALLOCATION.json')['method'],world_population_not_a_historical_invariant=True))
    dump('IMPERIAL_REGISTRY_VALIDATION.json',dict(before=len(b['registry']),after=len(ledger),extent_unchanged=bool(np.array_equal(om,nm)),cumulative_replay=replay==ledger,new_members=NEW_TAGS,new_electors=[],native_subjects_added=False))
    result=dict(status='MAP2U_READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2U_STATIC_FAILURE',runtime_status='NOT_TESTED_MAP2U',MAP2T_runtime_status='PASS_RUNTIME_USER_VALIDATED',historical_scope='Generalized political nuclei, incomplete dispersed estates',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,transferred_cells=21,new_RGBs=4,world_population=world,runtime_files_modified=[p for p in changed if p in allowed],concurrent_files_observed=reference['files'],concurrent_building_edits_after_install=sorted(external['files']),preexisting_anomalies=dict(duplicate_RGBs=len(inv['duplicates']),invalid_references=len(inv['errors'])),independent_geographic_error_bound_px=None)
    if (OUT/'UNIT_TESTS.json').exists():result['unit_tests']=load('UNIT_TESTS.json')
    if (OUT/'CSV_VALIDATION.json').exists():result['tables']=load('CSV_VALIDATION.json')
    dump('VALIDATION.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2U',status=result['status'],functional_files={p:current[p] for p in result['runtime_files_modified']},bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),previous_manifest='docs/reports/map/MAP2T/INSTALLED_MANIFEST.json'))
    print(result['status'],result['passed'],'/',result['total'],flush=True)
    if result['passed']!=result['total']:raise SystemExit(1)

def source_manifest():
    sources=[('Ebersdorf','vSK820Th_RjL_Eb_Vw.gif','650'),('Lobenstein','vSK820Th_RjL_Lo_Vw.gif','653'),('Sondershausen','vSK820Th_SS_Vw.gif','673')]
    dump('SOURCE_FILES.json',[dict(title=title,file='EVIDENCE/'+name,sha256=core.sha(OUT/'EVIDENCE'/name),url='https://www.ieg-maps.uni-mainz.de/gif/'+name,doi='10.25359/ISSN.1614-6352.MAP'+number,authors='Andreas Kunz / Joachim Robert Moeschl; IEG Mainz 2006',license='CC BY-NC 4.0 as stated on the source page',date_represented=1820,use='Comparative diagnostic source, NOT asserted as a direct 1776 boundary survey') for title,name,number in sources])

def reports():
    b=load('BASELINE.json');g=load('GEOMETRY.json');v=load('VALIDATION.json');tests=load('UNIT_TESTS.json');inv=load('CURRENT_INVENTORY.json');files={};prefix=OUT.relative_to(ROOT).as_posix()+'/'
    totals={tag:sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag) for tag in NEW_TAGS+['SSO']}
    north=sum(r['count'] for r in inv['regional_pop'] if r['key'][:2]==['STATE_ANHALT','SSO'])
    runtime_files='\n'.join('- `'+p+'`' for p in v['runtime_files_modified'])
    legacy=tests['prior_stage_snapshots'];failures='\n'.join('- `'+name+'`' for name in legacy['failures'])
    files[prefix+'REPORT.md']=f'''# MAP-2U — Noyaux complémentaires de Thuringe installés

Situation visée : 1er janvier 1776. **{v['status']}**.

Le lot installe les deux comtés distincts et un noyau septentrional de SSO. Il ne certifie pas les limites de toutes les possessions dispersées. Aucun test moteur MAP2U n’est revendiqué.

## Avant / après

| Secteur | Avant | Après | Cellules transférées | Population technique du pays |
|---|---|---|---:|---:|
| Lobenstein | WEI, xC00A37 | RLO, xEDB503 | 3 | {totals['RLO']} |
| Résidence d’Ebersdorf | WEI, xC00A37 | REB, xEDB502 | 1 | {totals['REB']} au total |
| Noyau de Hirschberg | SAX, x31E0C0 | REB, xEDB500 | 1 | inclus ci-dessus |
| Sondershausen nord | PRU, x3C9B93 | SSO, xEDB501 | 16 | {totals['SSO']} dont {north} au nord |

**21 cellules**, quatre RGB nouveaux xEDB500–xEDB503. Région73 STATE_SAXONY pour les Reuss; région62 STATE_ANHALT pour Sondershausen. Le nom technique de cette dernière région ne signifie pas une annexion des principautés d’Anhalt: leurs pixels, propriétaires et populations sont inchangés. Le registre passe de537 à541 RGB, sans extension physique de l’Empire.

RLO est un comté sous Heinrich II, REB sous Heinrich XXIV. Le rang technique natif « principality » ne dispose pas d’un équivalent « county »: le gouvernement et les titres affichés sont bien comtaux. Pas d’élévation princière de1790 ou1806 appliquée d’avance, ni d’union de1824. Drapeaux temporaires: mêmes armes dynastiques simplifiées que les autres Reuss, sans union politique. Les lois et technologies de départ reprennent le modèle existant COB, non un audit institutionnel complet.

SSO reste un seul pays, avec ses12 cellules méridionales intactes et16 cellules au nord. Sa région capitale technique est désormais STATE_ANHALT, où se trouve le point diagnostique de Sondershausen; aucun locator n’est créé ou déplacé. La région capitale du jeu ne certifie pas l’emplacement d’une ville physique.

## Portée géographique

Toutes les attributions installées sont des **généralisations B**. Les sources institutionnelles établissent les souverainetés; les cartes comparatives guident les contours intérieurs. Aucune borne indépendante d’erreur locale n’est établie. Le profil diagnostique est conservé, sans nouvelle optimisation ni translation7,20pixels. Les ajustements des nouvelles feuilles ne constituent pas un recalage de la projection du jeu.

Le territoire résidentiel d’Ebersdorf est étroit: sa trace intérieure n’occupe qu’environ12,6% de la cellule4365/845. Une seule cellule est retenue pour représenter ce noyau, abstraction explicite de résolution, pas l’attribution de toute la province voisine. Hirschberg est séparé; aucun corridor ne les relie. Le point géographique diagnostique de Hirschberg est proche d’une limite de cellule: son noyau n’est pas une position urbaine certifiée.

Les prolongements Wurzbach/Oßla tombant sur SCW sont laissés inchangés, faute de séparation locale assez sûre pour rouvrir Rudolstadt. Les franges vers Keula/STATE_BRUNSWICK et les prolongements Ebeleben–Clingen sont différés. Ces derniers rencontrent le rectangle de protection d’Erfurt, qui couvre aussi des terrains bien au-delà de la ville. Ce rectangle n’est pas une frontière historique d’Erfurt. Toutes ses cellules restent identiques.

Voir [carte avant/après](THURINGIA_BEFORE_AFTER.png), [repérage moderne et dans le jeu](PLAYER_LOCATION_GUIDE.png), les trois audits et UNRESOLVED.csv. Les résidus inchangés ne sont pas validés comme historiquement corrects. Les petites enclaves ne prolongent pas ce lot.

## Population et économie

Population mondiale mesurée avant/après: **835801255**, delta0. Ce total n’est pas une obligation historique; il résulte ici d’une redistribution technique provisoire. Les chiffres du tableau ne sont pas des recensements1776. Des inventaires démographiques sont repérés, mais sans valeurs consultables au périmètre de ces noyaux, aucune estimation historique n’est appliquée. Pas de compensation ailleurs ni d’ajout artificiel.

MAP2U conserve les profils culture/religion, bâtiments, niveaux, PM écrits, propriétaires économiques, ressources, capacités agraires, unités et recrutements. Trois fichiers de bâtiments ont toutefois été modifiés en parallèle par un autre travail du workspace: leur différentiel exact est enregistré dans EXTERNAL_BUILDINGS_OBSERVED.json et conservé, sans être attribué à ce lot. HLB reste à9206 habitants. Les six pays MAP2T et leurs noyaux sont conservés. Aucun bâtiment ni formation n’est fabriqué pour les nouveaux comtés; leur viabilité en nouvelle partie doit être contrôlée.

## Validation et coexistence

**{v['passed']}/{v['total']}** contrôles statiques. **22/22** tests ciblés et **60/60** tests de contrats impériaux. Les73 sorties du compilateur impérial sont vérifiées avant puis après;17 reçoivent seulement les membres et droits supplémentaires. Les44 doublons RGB et12 références invalides préexistants restent inchangés. Aucun nouvel électeur ni sujet natif de l’empereur. Les mécanismes HRE-CENTRALIZATION, icônes et prototypes sont préservés.

Les{legacy['tests']} tests d’étapes anciennes donnent{legacy['tests']-len(legacy['failures'])-len(legacy['errors'])} succès et{len(legacy['failures'])} échecs, détaillés dans LEGACY_TEST_TRIAGE.md. Sept étaient déjà signalés lors de MAP2T; quatre attentes globales de MAP2T deviennent dépassées, ainsi que l’ancienne assertion qui exigeait tous les pixels prussiens immuables. Deux comparaisons économiques anciennes rencontrent aussi les changements de bâtiments parallèles. Les principautés d’Anhalt et les121 transferts/16RGB de MAP2T sont vérifiés directement et restent intacts. Aucune ancienne baseline ou assertion n’est réécrite.

Des modifications concurrentes de141 fichiers ont été observées avant installation, sans chevauchement des cibles territoriales. Elles sont conservées dans un constat additif PREINSTALL_CONCURRENT_SNAPSHOT.json, séparé de la baseline initiale immuable. Trois changements supplémentaires de bâtiments sont apparus après installation: papier, exploitation forestière et élevage, avec un delta global observé de+8/+2/+5 niveaux respectivement. Ces trois fichiers ont été lus et leurs empreintes, contenus et différences canoniques sont conservés dans EXTERNAL_BUILDINGS_OBSERVED.json. Il ne s’agit ni de modifications MAP2U ni d’une validation historique de cet équilibrage. Le contrôle final rejoue exclusivement ces deltas explicitement observés et les modifications territoriales déclarées; les autres données restent strictement protégées.

La validation manuelle MAP2T est enregistrée dans MAP2T/RUNTIME_USER_ATTESTATION_MAP2U.json: six nouveaux États, dignité saxonne, mécanismes, économies et un mois sans erreur signalée. Il s’agit du test du joueur, pas d’un test moteur automatisé ni d’une certification de toutes les frontières. MAP2U reste **NOT_TESTED_MAP2U**.

## Fichiers fonctionnels modifiés

{runtime_files}

Outils nouveaux: map2u_thuringia.py, test_map2u_thuringia.py, map2u_tables.mjs. L’extension de map2l_registry.py est explicitement limitée aux trois parents de ce lot et au seul changement de région capitale de SSO. Les rapports antérieurs restent intacts; seule une attestation additive est ajoutée pour MAP2T.

HEAD et index Git inchangés. Aucun commit, merge, reset, push, changement de branche ou écriture dans l’installation du jeu. Aucune autre région commencée.

## Recherche locale

Aucun appel ColGrep redondant: les fichiers, identifiants et outils nécessaires étaient déjà localisés par MAP2T et par le prompt. Les lectures exactes ont été vérifiées localement. Cette passe ne mesure donc ni une exécution2B ni une économie de quota. Les compteurs de tokens Codex ne sont pas accessibles.
'''
    files[prefix+'HISTORICAL_EVIDENCE.md']='''# Preuves et méthode MAP-2U

## Souverainetés avant1776

[Landeszentrale für politische Bildung Thüringen, résidences des Reuss](https://www.politische-bildung-thueringen.de/informieren/dossiers/dossier/2/residenzen-der-reussen/), auteur Marco Kreutzmann: branches distinctes de Lobenstein et Ebersdorf issues du partage1678; dignités princières seulement1790 et1806. Les deux résidences sont antérieures à1776. Cela établit l’identité des deux comtés, pas une frontière pixel par pixel.

[Archives de Thuringe, gouvernement de Sondershausen, fonds5-14-1130](https://www.archive-in-thueringen.de/de/bestand/view/id/25954): depuis1716, Unterherrschaft et Oberherrschaft relèvent du même État tout en conservant des gouvernements distincts. Les réorganisations de1842–1847 ne sont pas appliquées au départ.

## Séparation territoriale et cartes comparatives

Les cartes IEG-MAPS650,653 et673, Andreas Kunz / Joachim Robert Moeschl,2006, représentent1820 et sont conservées avec empreintes dans SOURCE_FILES.json. Liens: [Ebersdorf](https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_RjL_Eb_Vw.htm), [Lobenstein](https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_RjL_Lo_Vw.htm), [Sondershausen](https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_SS_Vw.htm). Les traces bleues sont conservées dans les images TRACING_REVIEW et leurs sommets exacts dans GEOMETRY.json.

La reconstruction1789 de Putzger et son ALIGNMENT.json restent disponibles dans MAP2T. Les contours Reuss y sont regroupés à une échelle qui ne sépare pas correctement Ebersdorf: ils ne suffisent pas à attribuer chaque enclave. Les feuilles IEG apportent cette distinction, sous contrôle de la chronologie; les contours intérieurs demeurent B, pas des levés1776.

[IEG, notice Reuss-Ebersdorf](https://www.hgisg-ekompendium.ieg-mainz.de/Dokumentation_Datensaetze/Multimedia/Staaten/Reuss-Ebersdorf.php): le partage consécutif à l’extinction de Hirschberg en1711 donne à Ebersdorf les environs de cette résidence. L’union de1824 est écartée. Les zones hachurées de Gera/Saalburg, condominium seulement après1802, sont exclues des nouveaux tracés. Les possessions devenues prussiennes en1815 ne sont pas importées comme telles dans les comtés. Les éventuelles petites rectifications entre1776 et1820 ne sont pas toutes résolues: seuls des noyaux sont retenus.

## Souverains

Lobenstein: Heinrich II,1702–1782, né le19juillet1702. Le catalogue historique de la société des sciences naturelles de Gera relève sa prédication funèbre de1782, entrée2173, sous le titre comtal: [bibliographie conservée par ZOBODAT](https://www.zobodat.at/pdf/Jber-Ges-Freunden-Naturwiss-Gera_39-42_0147-0228.pdf), repérage par le numéro de l’entrée. Heinrich XXXV ne lui succède qu’en1782; il n’est pas installé en1776.

Ebersdorf: Heinrich XXIV,1724–1779, identité comtale [Deutsche Biographie, GND143309773](https://www.deutsche-biographie.de/gnd143309773.html). Date de naissance22janvier1724 corroborée par [LAGIS, registre familial](https://www.lagis-hessen.de/de/subjects/rsrec/current/1/entry/heinrich%2Bx.%252C%2Breuss-ebersdorf%252C%2Bgraf/sn/bio/register/person). Aucun successeur1779 ni titre princier1806 anticipé. SSO conserve le souverain contemporain déjà vérifié et installé par MAP2T.

## Démographie et limites documentaires

[Archives, Landesdirektion Ebersdorf, rubrique démographique](https://www.archive-in-thueringen.de/de/findbuch/view/bestand/21761/systematik/83870): dossier0992, fonds3-12-2500, annonce des comparaisons1714/1784 dans un dossier1811; dossier0990 signale aussi des données Lobenstein1794. Les notices ne donnent pas les tableaux eux-mêmes: aucune population1776 n’en est inventée. La notice IEG donne des ordres de grandeur postérieurs qui ne correspondent ni à la date ni aux noyaux installés; ils ne deviennent pas une estimation1776.

L’accès à la rubrique de frontières83834 fournie dans le prompt n’a pas livré de contenu exploitable. Aucune de ses limites n’est prétendue lue ou appliquée. Le document institutionnel accessible de Sondershausen et les cartes comparatives sont distingués de cette lacune.

## Précision et traçabilité

SOURCE_ALIGNMENT.json aligne les nouvelles feuilles sur le profil diagnostique conservé. Les faibles résidus des points d’ajustement ne sont pas des erreurs géographiques indépendantes. Ni refonte régionale de projection, ni translation7,20pixels, ni rivières assimilées à des centres urbains certifiés. Les villes modernes sont des repères explicites du guide; les limites politiques proviennent des polygones, et non de la seule position d’une ville.

Les zones A concernent les identités et filiations politiques établies. Les cellules effectivement transférées sont B. Les secteurs C sont conservés sans transfert, avec les réserves d’UNRESOLVED.csv. La quantification d’Ebersdorf à une cellule reste visible comme approximation.
'''
    files[prefix+'REUSS_LOBENSTEIN_AUDIT.md']=f'''# Reuss-Lobenstein

TAG RLO libre à la capture; comté distinct installé, sous Heinrich II (1702.7.19), et non Heinrich XXXV. Aucun titre princier de1790, aucune union de1824.

Trois cellules du parent xC00A37, précédemment WEI dans STATE_SAXONY73, composent xEDB503. Population provisoire: {totals['RLO']}. Le tracé intérieur est lu sur la feuille IEG653 puis confronté aux branches de la carte1789 et à leur chronologie; il ne réunit pas artificiellement les possessions détachées. Altengeß et Heberndorf restent exclus. Les parties hachurées de Gera/Saalburg ne sont pas annexées.

Le tiers natif principality n’est qu’une contrainte technique: le gouvernement spécifique donne Comté impérial et Comte/Comtesse. Capital technique STATE_SAXONY, sans nouveau locator. Drapeau temporaire aux armes dynastiques reussiennes simplifiées; lois/technologies du modèle COB. Aucun lien de sujétion natif, nouvel électorat, bâtiment ou unité.

Le contour est B, non une frontière complète de1776. Les chiffres techniques ne sont pas des habitants historiques certifiés. Voir HISTORICAL_EVIDENCE.md, GEOMETRY.json et le plan de test pour les sources, sommets, limites et vérifications.
'''
    files[prefix+'REUSS_EBERSDORF_AUDIT.md']=f'''# Reuss-Ebersdorf

TAG REB libre à la capture; comté distinct installé sous Heinrich XXIV (1724.1.22). Pas de rang princier1806 ou d’union Lobenstein–Ebersdorf1824.

Deux noyaux disjoints, sans corridor: xEDB502 pour la résidence d’Ebersdorf (une cellule WEI) et xEDB500 pour Hirschberg (une cellule SAX), tous deux dans STATE_SAXONY73. Les principaux noyaux de RGZ, RGE et RSL restent intacts. Les droits Gera/Saalburg ne sont pas transférés.

La juridiction résidentielle étroite ne contient aucun centre de cellule dans sa trace intérieure: elle est quantifiée à la cellule4365/845. GEOMETRY.json conserve son recouvrement échantillonné d’environ12,6%. C’est une abstraction B explicitement plus large que le noyau intérieur, sans attribution de toute la province. Le noyau de Hirschberg découle du polygone et non du nom d’un bâtiment; sa ville diagnostique se trouve près du bord inférieur du pixel, sans précision urbaine certifiée.

Les quatre cellules candidates Wurzbach/Oßla qui recoupent le territoire technique SCW sont différées. Aucun élargissement de REB pour donner une continuité factice. Population technique totale: {totals['REB']}, répartie depuis WEI et SAX, tous profils conservés. La résidence technique partage la région capitale73; aucun locator, bâtiment ou unité créé.

Les preuves politiques, dates et limites cartographiques sont référencées dans HISTORICAL_EVIDENCE.md. Les futurs chiffres d’archives doivent être lus et ramenés au périmètre réellement installé avant tout remplacement de la population technique.
'''
    files[prefix+'SONDERSHAUSEN_AUDIT.md']=f'''# Schwarzbourg-Sondershausen

SSO existait déjà avec12 cellules et6734 habitants dans le noyau méridional. Ceux-ci sont préservés intégralement. Le lot ajoute16 cellules prussiennes du parent x3C9B93 dans STATE_ANHALT62, sous xEDB501; {north} habitants techniques sont transférés, soit {totals['SSO']} au total pour le même pays.

La région capitale devient STATE_ANHALT, et non une nouvelle entité politique Anhalt. Les quatre principautés ANH/ABG/AKT/AZR et leur découpage restent inchangés. Aucun second pays SSO, corridor vers Arnstadt/Gehren ou annexion générale de la région62.

Le point moderne de référence Sondershausen10.8643E/51.3696N donne le diagnostic X4348.711/Y819.877; la cellule4348/819 appartient désormais à SSO. La lecture de la feuille IEG673 et la présence de l’Unterherrschaft avant1776 soutiennent ce noyau B. Il ne s’agit pas d’une validation indépendante de précision subpixel.

Les locators urbains présents pour les régions62 et73 correspondent à d’autres centres partagés; aucun locator autonome Sondershausen n’est trouvé. LOCATORS_BEFORE.json conserve leurs chemins et lignes. Aucun de leurs X/Y n’est déplacé. La capitale technique ne fabrique pas une ville historique dans le paysage.

Ebeleben donne X4345.762/Y822.456 et rencontre la zone de protection d’Erfurt: sa cellule de référence reste inchangée. Clingen et les prolongements méridionaux restent également différés. Quatre cellules occidentales candidates de STATE_BRUNSWICK ne sont pas transférées. SCW et sa partie de Frankenhausen sont préservés.

Le souverain et le gouvernement SSO existants sont conservés. Aucune population historique nouvelle n’est présumée; les profils prussiens de la seule région62 sont redistribués techniquement. Les deux ensembles restent discontinus comme demandé.
'''
    files[prefix+'LEGACY_TEST_TRIAGE.md']=f'''# Tests figés d’étapes antérieures

22/22 tests MAP2U et60/60 contrats cumulatifs passent. Les{legacy['tests']} tests antérieurs donnent{legacy['tests']-len(legacy['failures'])-len(legacy['errors'])} succès,{len(legacy['failures'])} échecs,{len(legacy['errors'])} erreur. Aucun ancien test ou baseline n’est modifié.

Sept échecs étaient déjà consignés par MAP2T. Quatre assertions MAP2T attendaient le monde entier avant MAP2U, exactement six pays supplémentaires depuis leur capture, aucune modification d’une autre région ou les seules définitions de pays de ce stade. Une assertion MAP2R supplémentaire exigeait que toutes les cellules prussiennes mondiales restent inchangées: elle rencontre les16 cellules PRU→SSO autorisées, sans altération des quatre Anhalt. Ce ne sont pas de nouvelles pertes silencieuses: le bitmap mondial est vérifié exactement contre la transformation MAP2U, et les noyaux antérieurs sont contrôlés séparément.

L’attente ancienne à Wolgast et les anciennes photographies de registre restent signalées, pas réécrites. Les44 doublons RGB et12 références invalides hérités ne sont pas corrigés ni augmentés ici.

Deux échecs économiques supplémentaires proviennent des trois fichiers de bâtiments modifiés parallèlement dans le workspace. Leurs deltas observés figurent dans EXTERNAL_BUILDINGS_OBSERVED.json: aucune ancienne baseline n’est modifiée pour les masquer. Le nouveau contrôle économique conserve exactement la baseline plus ces seuls deltas attestés par les empreintes des trois fichiers, sans autorisation générale de modifier l’économie.

## Échecs effectivement observés

{failures}

Traces complètes et durées: UNIT_TESTS.json. Statique différentiel: VALIDATION.json.
'''
    files[prefix+'RUNTIME_TEST_PLAN.md']='''# Contrôle manuel MAP-2U à effectuer

Statut NOT_TESTED_MAP2U. La validation du joueur de MAP2T reste limitée à MAP2T. Démarrer une nouvelle partie1776; une sauvegarde antérieure ne teste pas ces historiques.

1. Reuss-Lobenstein/RLO: retrouver Bad Lobenstein au sud de Schleiz, près de la frontière franconienne; vérifier les trois cellules, Comté impérial, Heinrich II, absence d’union1824, population et fonctionnement du marché.
2. Reuss-Ebersdorf/REB: vérifier la cellule juste au nord de Lobenstein, puis le noyau détaché de Hirschberg vers l’est. Même pays, Heinrich XXIV, aucun corridor et aucune annexion des noyaux Greiz/Gera/Schleiz. La cellule d’Ebersdorf est une abstraction, pas une frontière certifiée.
3. Sondershausen/SSO: au nord-ouest d’Erfurt et au sud de Nordhausen, retrouver xEDB501 dans la région technique Anhalt. SSO doit aussi conserver son noyau méridional Gehren, sans corridor. Vérifier la région capitale et l’absence de nouvelle ville physique présumée. Ebeleben/Clingen et les franges occidentales sont des réserves, pas des territoires livrés.
4. Pays antérieurs: inspecter les six pays MAP2T, les quatre Anhalt, la dignité électorale de SAX et HLB. La zone d’Erfurt–Eichsfeld doit rester inchangée.
5. Mécanismes: RLO et REB membres ordinaires du bloc impérial, pas électeurs ni nouveaux sujets natifs. Vérifier titres de restitution, interface, liens impériaux et les deux types centralisés sans changement de contribution.
6. Économies: comparer les populations techniques et les profils, la subsistance, budgets, emploi, infrastructures et accès aux marchés. Aucun bâtiment ni unité n’est ajouté pour les comtés. Ne pas interpréter des chiffres techniques comme un recensement1776.
7. Laisser passer un mois. Vérifier absence de crash, erreurs nouvelles, disparition de pays ou anomalie des hooks impériaux. Fournir les noms des territoires réellement inspectés avant un futur PASS_RUNTIME_USER_VALIDATED.

PLAYER_LOCATION_GUIDE.png montre les villes modernes et les cellules du jeu, avec avertissement sur le calage. THURINGIA_BEFORE_AFTER.png facilite la comparaison. Aucune validation moteur automatisée n’est annoncée.
'''
    files[prefix+'NEXT_HRE_REGION_RECOMMENDATION.md']='''# Prochain lot conseillé, non commencé

Une passe ciblée de Hesse: Hesse-Cassel, Hesse-Darmstadt, Waldeck et raccords des branches de Nassau hors lots rhénans. Cette recommandation reprend MAP2T/NEXT_HRE_REGION_RECOMMENDATION.md et l’inventaire MAP2Q/R3/HRE_REGIONS_INVENTORY_UPDATED.csv, ligne28: le secteur y reste PARTIAL, sans certification de tous les bailliages.

Protéger les corrections de Mayence, du Palatinat et du Rhin–Westphalie; ne pas importer un Nassau unifié de1806. Demander un périmètre précis avant toute installation. Aucun nouveau chantier n’est lancé dans cette passe.

Thuringe: clôture pratique des noyaux de cette mission, pas clôture historique intégrale. Les petites possessions Reuss et les franges SSO restent explicites dans UNRESOLVED.csv. Erfurt–Eichsfeld conserve son blocage documenté; les autres grandes franges ernestines restent ouvertes, sans prolonger MAP2U pour des micro-enclaves.
'''
    for rel,raw in files.items():
        raw=re.sub(r'\b(le|de|en|à|ses|et|[Ll]es|des|dont|vers|depuis|seulement|après|avant|environ|[Rr]égion|cellules?|translation|recensements|dossier|fonds|entrée|comparaisons)(?=\d)',r'\1 ',raw)
        raw=re.sub(r'(?<=\d)(?=cellules|pixels|RGB|juillet|janvier)', ' ',raw)
        raw=raw.replace('juillet1702','juillet 1702').replace('janvier1724','janvier 1724').replace('delta0','delta 0').replace('835801255','835 801 255').replace('12,6%','12,6 %')
        assert '\ufffd' not in raw;files[rel]=raw
    dump('REPORTS_EXPECTED.json',files);core.OUT=OUT;core.emit(files,'REPORTS.patch')
    print(len(files),'authored reports prepared.',flush=True)

def delivery_check():
    import csv
    required=['REPORT.md','HISTORICAL_EVIDENCE.md','REUSS_LOBENSTEIN_AUDIT.md','REUSS_EBERSDORF_AUDIT.md','SONDERSHAUSEN_AUDIT.md',
      'TERRITORIAL_CHANGES.csv','THURINGIA_BEFORE_AFTER.png','POPULATION_BEFORE_AFTER.csv','WORLD_POPULATION_DELTA.json','IMPERIAL_REGISTRY_VALIDATION.json',
      'VALIDATION.json','UNIT_TESTS.json','UNRESOLVED.csv','RUNTIME_TEST_PLAN.md','NEXT_HRE_REGION_RECOMMENDATION.md','PLAYER_LOCATION_GUIDE.png']
    checks=[]
    for name in required:checks.append(dict(name='Deliverable '+name,passed=(OUT/name).is_file() and (OUT/name).stat().st_size>0))
    for name,table in load('CSV_TABLES.json').items():
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        check=bool(len(rows)==len(table['rows']) and all(list(row)==table['fields'] for row in rows))
        checks.append(dict(name='CSV records '+name,passed=check))
    for rel,raw in load('REPORTS_EXPECTED.json').items():checks.append(dict(name='Reviewed report '+rel,passed=(ROOT/rel).read_text(encoding='utf8')==raw))
    v=load('VALIDATION.json');tests=load('UNIT_TESTS.json')
    checks.append(dict(name='All scoped static checks pass',passed=v['passed']==v['total']))
    checks.append(dict(name='Strict unit groups pass',passed=all(not tests[key]['failures'] and not tests[key]['errors'] for key in ['MAP2U_targeted','cumulative_contracts'])))
    checks.append(dict(name='Runtime not falsely certified',passed=v['runtime_status']=='NOT_TESTED_MAP2U'))
    checks.append(dict(name='Manual receipt present',passed=json.loads((t.OUT/'RUNTIME_USER_ATTESTATION_MAP2U.json').read_text(encoding='utf8'))['status']=='PASS_RUNTIME_USER_VALIDATED'))
    checks.append(dict(name='Git HEAD unchanged',passed=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==load('BASELINE.json')['git_head']))
    checks.append(dict(name='Git index unchanged',passed=core.sha(ROOT/'.git/index')==load('BASELINE.json')['git_index_sha256']))
    dump('DELIVERY_CHECK.json',dict(passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks))
    assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
    print('All',len(checks),'delivery checks pass; 16 requested files present.',flush=True)

def unit_tests():
    import unittest,io,time
    groups={'MAP2U_targeted':['test_map2u_thuringia'],'cumulative_contracts':['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01'],
        'prior_stage_snapshots':['test_map2t_saxony','test_map2r_anhalt','test_map2q_r3','test_map2q_r2','test_map2m_r8','test_map2m_r9','test_map2o_east_frisia']}
    results={}
    for name,modules in groups.items():
        start=time.monotonic();stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=1).run(unittest.TestLoader().loadTestsFromNames(modules))
        results[name]=dict(modules=modules,tests=r.testsRun,failures=[test.id() for test,_ in r.failures],errors=[test.id() for test,_ in r.errors],seconds=round(time.monotonic()-start,2),output=stream.getvalue())
        print(name,r.testsRun,'tests',len(r.failures),'failures',len(r.errors),'errors',flush=True)
    dump('UNIT_TESTS.json',results)
    if any(results[name]['failures'] or results[name]['errors'] for name in ['MAP2U_targeted','cumulative_contracts']):raise SystemExit(1)

def table_data():
    b=load('BASELINE.json');g=load('GEOMETRY.json');inv=load('CURRENT_INVENTORY.json');transfers=[];pops=[]
    for a in g['assignments']:
        if a['owner']==a['previous_owner']:continue
        for x,y in sorted(a['cells']):
            transfers.append(dict(State_ID=a['state'],ID_numerique=62 if a['state']=='STATE_ANHALT' else 73,RGB_avant=a['parent_rgb'],RGB_apres=a['rgb'],Avant=a['previous_owner'],Apres=a['owner'],X=x,Y=y,Classe='B',Source='IEG-MAPS 650/653/673; GEOMETRY.json',Limite='Une cellule généralisée pour Ebersdorf' if [x,y]==[4365,845] else 'Noyau généralisé, limites résiduelles non certifiées'))
    old={tuple(r['key']):r['count'] for r in b['inventory']['regional_pop']};new={tuple(r['key']):r['count'] for r in inv['regional_pop']}
    for k in sorted(set(old)|set(new)):
        if k[0] not in REGIONS or old.get(k,0)==new.get(k,0):continue
        pops.append(dict(State_ID=k[0],TAG=k[1],Culture=k[2],Religion=k[3],Avant=old.get(k,0),Apres=new.get(k,0),Delta=new.get(k,0)-old.get(k,0),Methode='Redistribution technique provisoire, non recensement',Source='POPULATION_ALLOCATION.json'))
    pops.append(dict(State_ID='MONDE',TAG=None,Culture='Toutes',Religion='Toutes',Avant=sum(r['count'] for r in b['inventory']['pops']),Apres=sum(r['count'] for r in inv['pops']),Delta=0,Methode='Total effectif, non invariant historique imposé',Source='Inventaire des historiques effectifs'))
    unresolved=[dict(Secteur=s,Classe='C',Probleme=p,Action=a) for s,p,a in [
      ('Ebersdorf–Wurzbach–Oßla','Quatre cellules de la trace intérieure tombent sur SCW; elles restent inchangées pour préserver le territoire antérieur de Rudolstadt. La résidence d’Ebersdorf seule est quantifiée à une cellule.','Comparer une pièce locale antérieure à1776 et le calage existant avant tout transfert SCW.'),
      ('Sondershausen occidental','La trace couvre quatre cellules prussiennes de STATE_BRUNSWICK autour de Keula; elles sont exclues du noyau nord installé.','Documenter les limites occidentales et leur correspondance au bitmap avant extension.'),
      ('Ebeleben–Clingen','Le prolongement méridional recoupe le rectangle de protection d’Erfurt, bien plus large que le territoire de cette ville. Aucun pixel du rectangle ne change.','Maintenir cette réserve tant que la séparation d’Erfurt n’est pas démontrée; aucun corridor vers Gehren.'),
      ('Reuss dispersés','Altengeß, Heberndorf, Thimmendorf–Ruppersdorf, Titschendorf et bois isolés non intégrés; résidus techniques non certifiés.','Ne pas prolonger ce lot pour des micro-enclaves; future passe documentée seulement.'),
      ('Saalburg et Burgk','Les parts de Gera et les possessions de Greiz ne sont pas annexées à Ebersdorf ou Lobenstein. Les limites résiduelles restent incomplètes.','Conserver les droits antérieurs; ne pas importer le condominium de Gera après1802.'),
      ('Démographie','Les archives signalent des comparaisons1714/1784, mais leurs valeurs et périmètres n’ont pas été consultés. Les petites populations installées sont techniques.','Exploiter le dossier0992, fonds3-12-2500, si les images deviennent accessibles; ne pas extrapoler un total1820.'),
      ('Centres urbains et capitales','Aucun locator propre aux trois villes n’existe dans les régions partagées. Le choix d’une région capitale n’ajoute ni ville physique ni population.','Vérifier en nouvelle partie le repérage et l’accès au marché; ne pas déplacer automatiquement les locators natifs.'),
      ('Exactitude des frontières','Les polygones sont des noyaux B, non une restitution cadastrale. L’ajustement des feuilles ne prouve pas une erreur indépendante inférieure à2pixels.','Conserver le profil diagnostique et ses limites; aucune translation7,20pixels.'),
      ('Erfurt–Eichsfeld et autres lots','Problèmes historiques et anciens secteurs incomplets restent ouverts; la validation manuelle de MAP2T n’est pas une certification de toutes leurs limites.','Aucun transfert MAP2U dans les secteurs interdits; lot futur uniquement sur instruction.')]]
    datasets={'TERRITORIAL_CHANGES.csv':transfers,'POPULATION_BEFORE_AFTER.csv':pops,'UNRESOLVED.csv':unresolved}
    dump('CSV_TABLES.json',{name:dict(fields=list(rows[0]),rows=rows) for name,rows in datasets.items()})
    print('Three typed datasets prepared.',flush=True)

if __name__=='__main__':
    globals()[sys.argv[1]]()
