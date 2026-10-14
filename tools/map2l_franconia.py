"""Stage the authorised Franconia lot; no runtime text edits by this generator."""
from pathlib import Path
import collections as C
import csv
import json
import re
import shutil
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2b_patch import state, region, append
from map2l_belgium import packed, sha, allocate
from map2l_belgium import components
from map2l_hre_work import GIT
from map2l_registry import active_registry_path
ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2L/FRANCONIA'
MAP2L=OUT.parent
SID='STATE_FRANCONIA'
SOURCE=MAP2L/'GEOMETRY/Homann_reading.jpg'
TAGS=['ANS','FBM','WZB','NUR','EIC']
PALETTE={'BAV':(170,170,170),'ANS':(229,147,65),'FBM':(87,151,207),'WZB':(179,86,165),'NUR':(194,56,56),'EIC':(87,175,146),'COB':(126,108,185)}


def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')


def baseline():
    return json.loads((OUT/'BASELINE_AFTER_PIEDMONT.json').read_text(encoding='utf-8'))


def capture(continuation=False):
    name='BASELINE_AFTER_PIEDMONT.json' if continuation else 'BASELINE.json'
    target=OUT/name
    assert not target.exists(),'Do not replace a lot baseline'
    # Reuse the already saved, identical post-Belgium candidate; no new full map copy.
    bitmap=MAP2L/'BELGIUM/provinces_candidate.png'
    assert sha(bitmap)==sha(ROOT/'map_data/provinces.png')
    inv=qa.inventory();originals={};hashes={}
    for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():hashes[p.relative_to(ROOT).as_posix()]=sha(p)
    for folder in ['common/history','common/country_definitions','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if SID in raw or p.name=='lge - imperial estate.txt':originals[p.relative_to(ROOT).as_posix()]=raw
    registry=MAP2L/'IMPERIAL_DE_JURE_REGISTRY.json'
    if continuation:
        import map2k_imperial_system as compiler
        compiler.OUT=OUT
        compiled=compiler.compile_system()
        assert all((ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff') for p,raw in compiled.items()),'Manual compiler drift: do not overwrite'
    dump(name,dict(inventory=inv,originals=originals,hashes=hashes,
        bitmap_backup=bitmap.relative_to(ROOT).as_posix(),bitmap_sha256=sha(bitmap),
        de_jure_registry=json.loads(registry.read_text()),registry_sha256=sha(registry),
        git_head=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_index_sha256=sha(ROOT/'.git/index')))
    print('FRANCONIA',name,'captured; existing bitmap reused;',len(originals),'relevant text snapshots')


def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    im=Image.open(SOURCE).convert('RGB');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for label,box in [('NW',(0,500,1150,1650)),('NE',(1050,500,2263,1650)),('SW',(0,1500,1150,2600)),('SE',(1050,1500,2263,2600))]:
        crop=im.crop(box);d=ImageDraw.Draw(crop)
        for x in range((box[0]//100+1)*100,box[2],100):
            d.line([(x-box[0],0),(x-box[0],crop.height)],fill=(160,50,50),width=1)
            d.text((x-box[0]+2,4),str(x),font=font,fill='red',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            d.line([(0,y-box[1]),(crop.width,y-box[1])],fill=(160,50,50),width=1)
            d.text((4,y-box[1]+2),str(y),font=font,fill='red',stroke_width=1,stroke_fill='white')
        crop.save(OUT/('HOMANN_'+label+'.png'))
    for label,box in [('NUREMBERG',(1050,1450,1360,1650)),('WURZBURG',(150,1100,450,1350)),('BAYREUTH',(1500,850,1740,1090)),('BAMBERG',(970,980,1220,1210))]:
        im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3),Image.Resampling.LANCZOS).save(OUT/('CITY_'+label+'.png'))
    rows=[]
    with (ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            if r['State_ID'] in {SID,'STATE_BAVARIA','STATE_HESSE','STATE_SAXONY','STATE_WURTTEMBERG'}:
                rows.append({k:r[k] for k in ['State_ID','Hub_Type','Hub_Name','Locator_X','Locator_Y','Locator_Sampled_RGB']})
    dump('NATIVE_ANCHORS.json',rows)
    print(json.dumps(rows,ensure_ascii=False,indent=2))


def align():
    config=json.loads((OUT/'TRACING.json').read_text(encoding='utf-8'))
    fit=[p for p in config['points'] if p['role']=='FIT']
    X=np.array([[*p['source'],1] for p in fit]);Y=np.array([p['game'] for p in fit])
    T=np.linalg.lstsq(X,Y,rcond=None)[0]
    inv=np.linalg.inv(T[:2]);metrics=[]
    for p in config['points']:
        predicted=np.array([*p['source'],1])@T
        metrics.append(dict(**p,predicted_game=predicted.tolist(),error_game_px=float(np.linalg.norm(predicted-p['game']))))
    dump('ALIGNMENT.json',dict(source=SOURCE.relative_to(ROOT).as_posix(),source_sha256=sha(SOURCE),
         matrix_source_to_game=T.tolist(),points=metrics,method='Local affine scan to three surveyed native hubs; independent Regensburg control. Coburg hub is a rejected label/position control.',
         precision='Game-scale envelope approximation, not cadastral reconstruction'))
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    image=Image.open(SOURCE).convert('RGB');d=ImageDraw.Draw(image)
    palette={'ANS':(235,110,40),'FBM':(50,110,220),'WZB':(210,50,170),'NUR':(230,40,40),'EIC':(30,150,120),'COB':(100,30,160)}
    for polygon in config['polygons']:
        d.line([tuple(p) for p in polygon['points']]+[tuple(polygon['points'][0])],fill=palette[polygon['owner']],width=5)
    old=packed(ROOT/'map_data/provinces.png');selected={int(r['key'][0][1:],16) for r in baseline()['inventory']['owners'] if r['key'][1]==SID}
    ys,xs=np.where(np.isin(old,list(selected)))
    cells=set(zip(xs.tolist(),ys.tolist()))
    def source(x,y):return tuple((np.array([x,y])-T[2])@inv)
    for x,y in cells:
        for dx,dy,edge in [(0,-1,[(x,y),(x+1,y)]),(0,1,[(x,y+1),(x+1,y+1)]),(-1,0,[(x,y),(x,y+1)]),(1,0,[(x+1,y),(x+1,y+1)])]:
            if (x+dx,y+dy) not in cells:d.line([source(*v) for v in edge],fill=(255,0,255),width=3)
    for p in config['points']:
        u,v=p['source'];d.ellipse((u-7,v-7,u+7,v+7),fill='red');d.text((u+10,v-10),p['name'],fill='red',stroke_width=2,stroke_fill='white')
    image.save(OUT/'HISTORICAL_OVERLAY.png')


def inside(points,polygon):
    hit=np.zeros(len(points),dtype=bool);x,y=points.T
    for i,a in enumerate(polygon):
        b=polygon[i-1];ax,ay=a;bx,by=b
        if ay==by:continue
        hit ^= ((ay>y)!=(by>y)) & (x<(bx-ax)*(y-ay)/(by-ay)+ax)
    return hit


def preview(path,owners,original,box):
    x0,y0,x1,y1=box;local=original[y0:y1,x0:x1]
    a=np.full((*local.shape,3),235,dtype=np.uint8)
    for (x,y),tag in owners.items():a[y-y0,x-x0]=PALETTE[tag]
    edge=np.zeros(local.shape,dtype=bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:,:]|=local[1:,:]!=local[:-1,:]
    a[edge]=[95,95,95]
    im=Image.fromarray(a).resize((a.shape[1]*10,a.shape[0]*10),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(im.width,im.height+180),'white');canvas.paste(im)
    d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for i,(tag,color) in enumerate(PALETTE.items()):
        pts=[(x,y) for (x,y),t in owners.items() if t==tag]
        if not pts:continue
        x,y=np.mean(pts,axis=0);d.text(((x-x0)*10,(y-y0)*10),tag,font=font,fill='black',stroke_width=2,stroke_fill='white')
        d.rectangle((10,im.height+7+i*23,26,im.height+22+i*23),fill=color)
        d.text((34,im.height+5+i*23),tag,font=font,fill='black')
    canvas.save(path)


def geometry():
    base=baseline();assert sha(ROOT/'map_data/provinces.png')==base['bitmap_sha256']
    before=packed(ROOT/'map_data/provinces.png');changed=before.copy()
    rows=[r for r in base['inventory']['owners'] if r['key'][1]==SID]
    parents={int(r['key'][0][1:],16):r['key'][0] for r in rows}
    mask=np.isin(before,list(parents));ys,xs=np.where(mask);cells=np.column_stack((xs,ys))
    align=json.loads((OUT/'ALIGNMENT.json').read_text());T=np.array(align['matrix_source_to_game']);inverse=np.linalg.inv(T[:2])
    scan=(cells+0.5-T[2])@inverse
    owners=np.array(['BAV']*len(cells),dtype='U3');config=json.loads((OUT/'TRACING.json').read_text())
    for polygon in config['polygons']:owners[inside(scan,polygon['points'])]=polygon['owner']
    # No enlarged enclaves: only abstract isolated one-pixel fragments into a
    # neighbour inside the same parent, except protected engine hub cells.
    hubs={'xD0C0A0':(4351,877,'NUR'),'xF91154':(4362,862,'ANS'),
          'x51C0A0':(4322,861,'WZB'),'x648AD1':(4347,862,'FBM')}
    lookup={tuple(c):str(t) for c,t in zip(cells,owners)};abstracted=[]
    for rgb,(x,y,tag) in hubs.items():assert lookup[x,y]==tag,(rgb,lookup[x,y],tag,'Review source outline, never force nearest-city ownership')
    protected={(x,y) for x,y,t in hubs.values()}
    for coord,tag in list(lookup.items()):
        x,y=coord
        if coord in protected:continue
        near=[lookup[q] for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if q in lookup and before[q[1],q[0]]==before[y,x]]
        if near and tag not in near:
            neighbour=C.Counter(near).most_common(1)[0][0]
            if neighbour!=tag:abstracted.append(dict(cell=[int(x),int(y)],from_owner=tag,to_owner=neighbour,reason='Isolated native pixel, no territorial dilation'));lookup[coord]=neighbour
    colors=set(np.unique(before).tolist());counter=0;assignments=[];new=[]
    for value,parent in sorted(parents.items()):
        groups=[]
        for tag in sorted(set(lookup.values())):
            local=np.zeros(mask.shape,dtype=bool)
            for (x,y),t in lookup.items():
                if t==tag and int(before[y,x])==value:local[y,x]=True
            for part in components(local):groups.append(dict(owner=tag,cells=[(x,y) for y,x in part],pixels=len(part)))
        if parent in hubs:
            x,y,t=hubs[parent];keep=next(g for g in groups if (x,y) in g['cells'])
        else:keep=max(groups,key=lambda g:g['pixels'])
        for g in groups:
            rgb=parent
            if g is not keep:
                while 0xEDA200+counter in colors:counter+=1
                value_new=0xEDA200+counter;counter+=1;colors.add(value_new);rgb='x'+format(value_new,'06X')
                new.append(dict(rgb=rgb,parent_rgb=parent))
            for x,y in g['cells']:changed[y,x]=int(rgb[1:],16)
            assignments.append(dict(rgb=rgb,parent_rgb=parent,state=SID,**g))
    assert set(TAGS)<=set(lookup.values())
    a=np.stack(((changed>>16)&255,(changed>>8)&255,changed&255),axis=2).astype(np.uint8)
    Image.fromarray(a).save(OUT/'provinces_candidate.png')
    box=(int(xs.min())-12,int(ys.min())-12,int(xs.max())+13,int(ys.max())+13)
    preview(OUT/'before.png',{tuple(c):'BAV' for c in cells},before,box)
    preview(OUT/'after.png',lookup,changed,box)
    left=Image.open(OUT/'before.png');right=Image.open(OUT/'after.png')
    both=Image.new('RGB',(left.width+right.width,left.height),'white');both.paste(left);both.paste(right,(left.width,0));both.save(OUT/'BEFORE_AFTER.png')
    dump('GEOMETRY.json',dict(status='SOURCE_TRACED_GAME_SCALE_APPROXIMATION_NOT_CADASTRAL',
        assignments=assignments,new_provinces=new,abstracted_pixels=abstracted,
        pixels_by_owner=dict(C.Counter(lookup.values())),crop=box,
        candidate_sha256=sha(OUT/'provinces_candidate.png'),changed_pixels=int((changed!=before).sum()),
        source=SOURCE.relative_to(ROOT).as_posix(),source_sha256=sha(SOURCE),
        limitations=['Homann dating unresolved; major jurisdictions corroborated by Le Rouge and existing research, not exact cadastral borders at 1776.',
        'Local affine independent Regensburg residual approximately five game pixels; outer fringes remain approximate.',
        'Small secondary jurisdictions abstracted; remaining undocumented fringe retains BAV pending targeted review.',
        'Native Coburg farm lies near historical Bamberg; no locator displaced or pixel enlarged.']))
    print('Candidate:',len(assignments),'province identities;',len(new),'new RGBs;',dict(C.Counter(lookup.values())))


def csvout(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def emit(files,name):
    import map2l_belgium as e
    e.LOT=OUT
    return e.emit(files,name)


def prepare():
    base=baseline();geo=json.loads((OUT/'GEOMETRY.json').read_text());inv=qa.inventory()
    assert sha(ROOT/'map_data/provinces.png')==base['bitmap_sha256']
    assert not set(TAGS)&set(inv['countries'])
    weights=geo['pixels_by_owner'];files={};allocation=[]
    rel='common/history/states/00_states.txt';raw=base['originals'][rel]
    source=next(n for n in state(raw,SID).children('create_state') if n.one('country')=='c:BAV')
    parts=[]
    for tag in sorted(weights):
        rgb=[r['rgb'] for r in geo['assignments'] if r['owner']==tag]
        parts.append('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(rgb)+' } }')
    files[rel]=edits(raw,[(source.start,source.end,'\n\t\t'.join(parts))])
    rel='map_data/state_regions/00_west_europe.txt';raw=base['originals'][rel]
    node=next(n for n in cw.parse(raw) if n.key==SID);provs=node.children('provinces')[0]
    files[rel]=edits(raw,[(provs.start,provs.end,'provinces = { '+' '.join('"'+r['rgb']+'"' for r in geo['assignments'])+' }')])
    for rel,original in base['originals'].items():
        if '/pops/' not in rel and '/buildings/' not in rel:continue
        try:src=region(original,SID,'BAV')
        except StopIteration:continue
        raw=original;ops=[];moved=C.defaultdict(list)
        if '/pops/' in rel:
            for pop in src.children('create_pop'):
                n=pop.children('size')[0];count=int(n.value);amounts=allocate(count,weights);fragment=raw[pop.start:pop.end]
                ops.append((n.start,n.end,'size = '+str(amounts['BAV'])))
                for tag,amount in amounts.items():
                    if tag!='BAV' and amount:moved[tag].append(edits(fragment,[(n.start-pop.start,n.end-pop.start,'size = '+str(amount))]))
                allocation.append(dict(kind='population',file=rel,profile=cw.scalar(pop.one('culture'))+'/'+cw.scalar(pop.one('religion','DEFAULT')),before=count,after=amounts))
        else:
            for building in src.children('create_building'):
                levels=[n for n in cw.walk(building.children()) if n.key=='levels' and isinstance(n.value,str)]
                if not levels:continue
                bytag=C.defaultdict(list);counts=C.Counter();piece=raw[building.start:building.end]
                for n in levels:
                    amounts=allocate(int(n.value),weights)
                    for tag,amount in amounts.items():bytag[tag].append((n.start-building.start,n.end-building.start,'levels = '+str(amount)));counts[tag]+=amount
                fragments={}
                for tag in weights:
                    if not counts[tag]:continue
                    fragment=edits(piece,bytag[tag]);root=cw.parse(fragment)[0];zeros=[]
                    for own in root.children('add_ownership'):
                        for holder in own.children():
                            if holder.one('levels')=='0':zeros.append((holder.start,holder.end,''))
                    fragment=edits(fragment,zeros)
                    kind=cw.scalar(building.one('building'))
                    # Public offices follow political control; private holders
                    # remain BAV investors in the retained Franconia subdivision.
                    if tag!='BAV' and kind=='building_government_administration':fragment=re.sub(r'(country\s*=\s*"?c:)BAV',r'\g<1>'+tag,fragment)
                    fragments[tag]=fragment
                ops.append((building.start,building.end,fragments.get('BAV','')))
                for tag,fragment in fragments.items():
                    if tag!='BAV':moved[tag].append(fragment)
                allocation.append(dict(kind='building',file=rel,profile=cw.scalar(building.one('building')),before=sum(int(n.value) for n in levels),after=dict(counts)))
        raw=edits(raw,ops)
        for tag,pieces in moved.items():raw=append(raw,SID,tag,'\n'.join(pieces))
        files[rel]=raw
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')
    terrains={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for r in geo['new_provinces']:terrain+='\n'+r['rgb']+'="'+terrains[r['parent_rgb'].upper()]+'"'
    (OUT/'province_terrains_candidate.txt').write_text(terrain+'\n',encoding='utf-8')
    names={'ANS':('Brandenburg-Ansbach-Bayreuth','Brandebourg-Ansbach-Bayreuth','Ansbachian','Ansbachois'),
        'FBM':('Prince-Bishopric of Bamberg','Principauté épiscopale de Bamberg','Bambergian','Bambergeois'),
        'WZB':('Prince-Bishopric of Würzburg','Principauté épiscopale de Wurtzbourg','Würzburgian','Wurtzbourgeois'),
        'NUR':('Imperial City of Nuremberg','Ville impériale de Nuremberg','Nurembergian','Nurembergeois'),
        'EIC':('Prince-Bishopric of Eichstätt','Principauté épiscopale d’Eichstätt','Eichstättian','Eichstättois')}
    countries='';coas='';flags=''
    for tag in TAGS:
        rgb=PALETTE[tag];religion='protestant' if tag in {'ANS','NUR'} else 'catholic'
        countries+=tag+' = { color = { '+' '.join(str(v) for v in rgb)+' } country_type = recognized tier = '+('city_state' if tag=='NUR' else 'principality')+' cultures = { south_german } religion = '+religion+' capital = '+SID+' }\n'
        ground={'ANS':'white','FBM':'blue','WZB':'red','NUR':'red','EIC':'green'}[tag]
        emblem='ce_eagle.dds' if tag in {'ANS','NUR'} else 'ce_cross_couped.dds'
        ink='black' if tag=='ANS' else 'white' if tag in {'WZB','EIC'} else 'yellow'
        coas+='AOR1776_'+tag+' = { pattern = "pattern_solid.tga" color1 = '+ground+' colored_emblem = { texture = "'+emblem+'" color1 = '+ink+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
        flags+=tag+' = { flag_definition = { coa = AOR1776_'+tag+' priority = 100 allow_overlord_canton = no } }\n'
    files['common/country_definitions/1776_map2l_franconian_estates.txt']=countries
    files['common/coat_of_arms/coat_of_arms/1776_map2l_franconian_flags.txt']=coas
    files['common/flag_definitions/1776_map2l_franconian_flags.txt']=flags
    # Use country-scoped early-modern variants, not era-4 research grants.
    scoped='OR = { '+' '.join('c:'+t+' ?= this' for t in TAGS)+' }'
    laws=''
    for key,parent,group,icon,possible in [
        ('law_aor1776_imperial_city_republic','law_presidential_republic','lawgroup_governance_principles','presidential_republic','c:NUR ?= this'),
        ('law_aor1776_imperial_customs','law_mercantilism','lawgroup_trade_policy','mercantilism',scoped),
        ('law_aor1776_imperial_no_slavery','law_slavery_banned','lawgroup_slavery','slavery_banned',scoped)]:
        modifier=''
        filename={'law_presidential_republic':'00_governance_principles.txt','law_mercantilism':'01_trade_policy.txt','law_slavery_banned':'02_slavery.txt'}[parent]
        raw=(ROOT/'common/laws'/filename).read_text(encoding='utf-8-sig');p=next(n for n in cw.parse(raw) if n.key==parent)
        mods=p.children('modifier')
        if mods:modifier=raw[mods[0].start:mods[0].end]
        laws+=key+' = { group = '+group+' parent = '+parent+' icon = "gfx/interface/icons/law_icons/'+icon+'.dds" progressiveness = 0 is_visible = { '+possible+' } can_enact = { '+possible+' } '+modifier+' }\n'
    files['common/laws/1776_map2l_franconian_start_variants.txt']=laws
    files['common/government_types/00_1776_map2l_nuremberg.txt']='''gov_aor1776_nuremberg_council = {
 transfer_of_power = presidential_elective
 new_leader_on_reform_government = no
 male_ruler = "aor1776_city_councillor_title"
 female_ruler = "aor1776_city_councillor_title"
 possible = { c:NUR ?= this has_law = law_type:law_aor1776_imperial_city_republic }
 on_government_type_change = { change_to_presidential_elective = yes }
 on_post_government_type_change = { post_change_to_presidential_elective = yes }
}
'''
    bv=(ROOT/'common/history/countries/bav - bavaria.txt').read_text(encoding='utf-8-sig')
    techs=re.findall(r'add_technology_researched\s*=\s*(\w+)',bv)
    core=['law_land_based_taxation','law_hereditary_bureaucrats','law_peasant_levies','law_no_police','law_guild_system','law_tenant_farmers','law_no_workers_rights']
    for tag in TAGS:
        initial=['law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery',*core,
            'law_oligarchy' if tag=='NUR' else 'law_autocracy','law_state_religion',
            'law_monarchy' if tag=='ANS' else 'law_aor1776_imperial_city_republic' if tag=='NUR' else 'law_theocracy']
        files[f'common/history/countries/{tag.lower()} - franconian estate.txt']='COUNTRIES = { c:'+tag+' ?= {\n'+''.join(' add_technology_researched = '+t+'\n' for t in techs)+''.join(' activate_law = law_type:'+l+'\n' for l in initial)+'} }\n'
    rulers='CHARACTERS = {\n'
    for tag,first,last,age in [('ANS','Alexander','Hohenzollern',39),('FBM','Adam Friedrich','von Seinsheim',67),('WZB','Adam Friedrich','von Seinsheim',67),('EIC','Raymund Anton','von Strasoldo',57)]:
        rulers+='c:'+tag+' ?= { create_character = { first_name = aor1776_'+tag.lower()+'_first last_name = aor1776_'+tag.lower()+'_last historical = yes culture = south_german religion = rel:'+('protestant' if tag=='ANS' else 'catholic')+' ruler = yes age = '+str(age)+' interest_group = '+('ig_landowners' if tag=='ANS' else 'ig_devout')+' ideology = ideology_traditionalist } }\n'
    files['common/history/characters/1776_map2l_franconian_rulers.txt']=rulers+'}\n'
    for lang,i in [('english',0),('french',1)]:
        loc='\ufeffl_'+lang+':\n'
        for tag,v in names.items():loc+=' '+tag+':0 "'+v[i]+'"\n '+tag+'_ADJ:0 "'+v[2+i]+'"\n'
        for tag,first,last in [('ANS','Alexander','Hohenzollern'),('FBM','Adam Friedrich','von Seinsheim'),('WZB','Adam Friedrich','von Seinsheim'),('EIC','Raymund Anton','von Strasoldo')]:loc+=' aor1776_'+tag.lower()+'_first:0 "'+first+'"\n aor1776_'+tag.lower()+'_last:0 "'+last+'"\n'
        translations={'law_aor1776_imperial_city_republic':('Patrician imperial republic','République impériale patricienne'),
            'law_aor1776_imperial_customs':('Early-modern imperial customs','Douanes impériales d’Ancien Régime'),
            'law_aor1776_imperial_no_slavery':('Free status in the imperial estates','Statut libre des habitants impériaux'),
            'gov_aor1776_nuremberg_council':('Patrician city council','Conseil urbain patricien'),
            'aor1776_city_councillor_title':('First Councillor','Premier conseiller')}
        for k,v in translations.items():loc+=' '+k+':0 "'+v[i]+'"\n'
        descriptions={'law_aor1776_imperial_city_republic':('An established imperial city governed by its patrician council, not a modern national republic.','Une ville impériale gouvernée par son conseil patricien, non une république nationale moderne.'),
            'law_aor1776_imperial_customs':('Local tariffs and regulated commerce; no modern commercial-insurance technology is granted.','Tarifs locaux et commerce réglementé ; aucune technologie moderne d’assurance commerciale n’est accordée.'),
            'law_aor1776_imperial_no_slavery':('The starting population retains free status without granting a later abolitionist-movement technology. Serfdom is a separate land-tenure law.','La population initiale conserve son statut libre sans recevoir une technologie tardive de mobilisation abolitionniste. Le servage relève séparément du régime foncier.'),
            'gov_aor1776_nuremberg_council':('The city is represented by its oligarchic council.','La ville est représentée par son conseil oligarchique.')}
        for k,v in descriptions.items():loc+=' '+k+'_desc:0 "'+v[i]+'"\n'
        loc+=' HUB_NAME_STATE_FRANCONIA_farm:0 "Bamberg"\n'
        files[f'localization/{lang}/1776_map2l_franconia_l_{lang}.yml']=loc
    for rel,raw in files.items():
        if rel.endswith('.txt'):cw.parse(raw)
    ledger=[r for r in base['de_jure_registry'] if r['state']!=SID]
    ledger+= [dict(rgb=r['rgb'],state=SID,beneficiary=r['owner'],basis='MAP2L Franconia: unchanged unresolved BAV fringe, NOT certified Bavarian sovereignty; see FRANCONIA/UNRESOLVED.csv.' if r['owner']=='BAV' else 'MAP2L Franconia: explicitly reviewed source-traced game-scale envelope; see FRANCONIA/GEOGRAPHIC_EVIDENCE.md, dating/outer-fringe limitations retained.') for r in geo['assignments']]
    ledger.sort(key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)
    migration=dict(replaced_regions=[SID],previous=[r for r in base['de_jure_registry'] if r['state']==SID],updated=[r for r in ledger if r['state']==SID],new_members=TAGS,free_cities=['NUR'],new_provinces=geo['new_provinces'])
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)
    changes=emit(files,'HISTORY.patch')
    dump('PLAN.json',dict(files=changes,allocations=allocation,new_tags=TAGS,technology_initializations=techs,law_variants_scoped_to_new_countries=True,
        personal_union_representation='Ansbach/Bayreuth one tag, distinct traced parts. Bamberg/Wurzburg distinct estates with two native instances of the same historical bishop; no invented Austrian subjection.',
        population_method='Area-proportional allocation of each existing culture/religion profile; not a historical census.',flags='Procedural identifying banners, not certified territorial flags.'))
    csvout('TERRITORIAL_CHANGES.csv',[dict(RGB=r['rgb'],Parent_RGB=r['parent_rgb'],State_ID=SID,Previous_Owner='BAV',New_Owner=r['owner'],Pixels=r['pixels'],Created=r['rgb']!=r['parent_rgb'],Confidence='UNRESOLVED_RETAINED_OWNER' if r['owner']=='BAV' else 'DOCUMENTED_GAMEPLAY_APPROXIMATION') for r in geo['assignments']])
    csvout('POPULATION_VALIDATION.csv',[dict(File=r['file'],Profile=r['profile'],Before=r['before'],After_Total=sum(r['after'].values()),**r['after']) for r in allocation if r['kind']=='population'])
    print('Prepared',len(changes),'text files;',len(ledger),'imperial RGBs; populations conserved')


def install_generated():
    base=baseline();geo=json.loads((OUT/'GEOMETRY.json').read_text())
    assert sha(ROOT/'map_data/provinces.png')==base['bitmap_sha256']
    assert sha(OUT/'provinces_candidate.png')==geo['candidate_sha256']
    inv=qa.inventory();assert set(TAGS)<=set(inv['countries'])
    assert {r['rgb'] for r in json.loads(active_registry_path().read_text()) if r['state']==SID}=={r['rgb'] for r in geo['assignments']}
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    shutil.copyfile(OUT/'province_terrains_candidate.txt',ROOT/'map_data/province_terrains.txt')
    print('Reviewed Franconia bitmap and inherited terrain data installed')


def compile_imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system()
    changes=emit(files,'IMPERIAL.patch')
    dump('IMPERIAL_FILES.json',dict(files=changes,all_compiled_files=list(files)))
    print('Prepared',len(changes),'imperial runtime changes')


def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()
    import prototype_map2k_main_map as main
    main.MOD=ROOT;main.PACKAGE=OUT/'MAIN_MAP';main.PACKAGE.mkdir(parents=True,exist_ok=True)
    main.build_and_test()


def finish_metadata():
    # Small explicit post-review adjustments; no new territorial geometry.
    files={};coas=''
    for tag in TAGS:
        ground={'ANS':'white','FBM':'blue','WZB':'red','NUR':'red','EIC':'green'}[tag]
        emblem='ce_eagle.dds' if tag in {'ANS','NUR'} else 'ce_cross_couped.dds'
        ink='black' if tag=='ANS' else 'white' if tag in {'WZB','EIC'} else 'yellow'
        coas+='AOR1776_'+tag+' = { pattern = "pattern_solid.tga" color1 = '+ground+' colored_emblem = { texture = "'+emblem+'" color1 = '+ink+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_franconian_flags.txt']=coas
    for lang in ['english','french']:
        rel=f'localization/{lang}/1776_map2l_franconia_l_{lang}.yml';raw=(ROOT/rel).read_text(encoding='utf-8')
        if 'HUB_NAME_STATE_FRANCONIA_farm:' not in raw:raw+=' HUB_NAME_STATE_FRANCONIA_farm:0 "Bamberg"\n'
        files[rel]=raw
    ledger=json.loads(active_registry_path().read_text());migration=json.loads((OUT/'REGISTRY_MIGRATION.json').read_text())
    for row in ledger+migration['updated']:
        if row['state']==SID and row['beneficiary']=='BAV':row['basis']='MAP2L Franconia: unchanged unresolved BAV fringe, NOT certified Bavarian sovereignty; see FRANCONIA/UNRESOLVED.csv.'
    files[active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)
    emit(files,'METADATA.patch')


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    {'capture':capture,'capture-continuation':lambda:capture(True),'inspect':inspect,'align':align,'geometry':geometry,'prepare':prepare,'install-generated':install_generated,'compile-imperial':compile_imperial,'maps':maps,'finish-metadata':finish_metadata}[sys.argv[1]]()
