"""MAP-2Q: isolated, guarded Eutin dossier and approved territorial patch.

Never writes earlier baselines or Git metadata. Run with Python -B.
"""
from pathlib import Path
import collections as C
import json
import shutil
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2l_mainz as core
import start_buildings_2026_10_15 as economy
import map2m_r9 as r9

ROOT = core.ROOT
OUT = ROOT / 'docs/reports/map/MAP2Q'
REGION = 'STATE_SCHLESWIG_HOLSTEIN'
BOX = (4304, 714, 4360, 760)


def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def load(name):
    return json.loads((OUT/name).read_text(encoding='utf-8'))


def capture():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT/'BASELINE.json').exists(), 'Immutable baseline already exists'
    inventory = core.qa.inventory()
    shutil.copy2(ROOT/'map_data/provinces.png', OUT/'provinces_before.png')
    originals = {p:(ROOT/p).read_text(encoding='utf-8-sig') for p in [
        'common/history/states/00_states.txt', 'common/history/pops/00_west_europe.txt',
        'map_data/state_regions/00_west_europe.txt', 'map_data/province_terrains.txt']}
    dump('BASELINE.json', dict(inventory=inventory, hashes=economy.runtime_hashes(), originals=originals,
        registry=json.loads(core.active_registry_path().read_text(encoding='utf-8')),
        bitmap_sha256=core.sha(ROOT/'map_data/provinces.png'),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_index_sha256=core.sha(ROOT/'.git/index'),
        prior_report_hashes={p.relative_to(ROOT).as_posix():core.sha(p)
            for p in (ROOT/'docs/reports/map').rglob('*') if p.is_file() and OUT not in p.parents},
        bridge_and_prototype_hashes={p.relative_to(ROOT).as_posix():core.sha(p)
            for folder in ['docs/prototypes/REGIONAL_INFRASTRUCTURE/mod','tools/vic3-diagnostic-bridge']
            for p in (ROOT/folder).rglob('*') if p.is_file()}))
    print('Captured current dirty workspace without Git mutation')


class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in {'a','img'}:
            u=attrs.get('href',attrs.get('src',''))
            if any(x in u for x in ['jpg','jpeg','png','10496','464','download']):print(tag,u)


def source_links():
    url='https://www.vintage-maps.com/en/antique-maps/europe/germany/von-reilly-germany-schleswig-holstein-wagrien-1795::464'
    text=urllib.request.urlopen(url,timeout=25).read().decode()
    Links().feed(text)


def fetch_source():
    import io
    url='https://www.vintage-maps.com/589-extra_large/von-reilly-germany-schleswig-holstein-wagrien-1795.jpg'
    evidence=OUT/'EVIDENCE';evidence.mkdir(parents=True,exist_ok=True)
    path=evidence/'REILLY_WAGRIEN_300.jpg'
    assert not path.exists()
    data=urllib.request.urlopen(url,timeout=30).read(15000001)
    assert len(data)<15000000
    Image.open(io.BytesIO(data)).verify()
    path.write_bytes(data)
    dump('REILLY_PROVENANCE.json',dict(title='Die Landschaft Wagrien mit dem Hochstift Lübeck oder Eutin, Nro 300',
        author='Franz Johann Joseph von Reilly',date='circa 1790–1795; not exactly 1776',url=url,
        catalogue='https://www.vintage-maps.com/en/antique-maps/europe/germany/von-reilly-germany-schleswig-holstein-wagrien-1795::464',
        institutional_copy='Schleswig-Holsteinische Landesbibliothek, 2017-1-13 / dc00018389',
        rights='Historic engraving public domain. Reproduction courtesy Götzfried Antique Maps; retain catalogue attribution link.',
        sha256=core.sha(path),dimensions=Image.open(path).size,
        use='Pre-1803 outline corroboration only; chronology and institutional rights independently checked against NLA Best.30.'))
    print(path,Image.open(path).size)


def inspect():
    from PIL import ImageColor
    b=load('BASELINE.json');bmp=core.packed(OUT/'provinces_before.png')
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    x0,y0,x1,y1=BOX;local=bmp[y0:y1,x0:x1]
    arr=np.full((*local.shape,3),(170,204,225),dtype=np.uint8)
    palette={'HOL':'#99b899','SCH':'#e7d188','LUB':'#b392cf','HAM':'#ee9585','MEC':'#a8bacb'}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for color in np.unique(local):
        tag=owners.get('x'+format(int(color),'06X'),['',''])[1]
        if tag:arr[local==color]=ImageColor.getrgb(palette.get(tag,'#ccc'))
    image=Image.fromarray(arr).resize(((x1-x0)*20,(y1-y0)*20),Image.Resampling.NEAREST)
    draw=ImageDraw.Draw(image)
    for x in range(x0,x1,2):
        draw.line(((x-x0)*20,0,(x-x0)*20,image.height),fill='#999999')
        draw.text(((x-x0)*20,0),str(x),font=font,fill='black')
    for y in range(y0,y1,2):
        draw.line((0,(y-y0)*20,image.width,(y-y0)*20),fill='#999999')
        draw.text((0,(y-y0)*20),str(y),font=font,fill='black')
    for color in np.unique(local):
        rgb='x'+format(int(color),'06X');yy,xx=np.where(local==color)
        tag=owners.get(rgb,['',''])[1]
        if tag:draw.text((int(np.median(xx))*20,int(np.median(yy))*20),rgb+' '+tag,font=font,fill='black')
    image.save(OUT/'CURRENT_READING.png')
    loc=[r for r in r9.locators(bmp) if x0<=r['X']<x1 and y0<=r['Y']<y1]
    dump('NATIVE_LOCATORS.json',loc)
    print('Region owners',[r for r in b['inventory']['owners'] if r['key'][1]==REGION])
    print('Population',[r for r in b['inventory']['regional_pop'] if r['key'][0]==REGION])
    print('Locators',loc)
    print('World population',sum(r['count'] for r in b['inventory']['pops']))


def reading():
    im=Image.open(OUT/'EVIDENCE/REILLY_WAGRIEN_300.jpg')
    for name,box in [('EUTIN',(300,340,870,675)),('SCHWARTAU',(530,685,830,1020))]:
        crop=im.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2))
        draw=ImageDraw.Draw(crop);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
        for x in range((box[0]//50+1)*50,box[2],50):
            draw.line(((x-box[0])*2,0,(x-box[0])*2,crop.height),fill='#4477cc')
            draw.text(((x-box[0])*2,0),str(x),fill='blue',font=font)
        for y in range((box[1]//50+1)*50,box[3],50):
            draw.line((0,(y-box[1])*2,crop.width,(y-box[1])*2),fill='#4477cc')
            draw.text((0,(y-box[1])*2),str(y),fill='blue',font=font)
        crop.save(OUT/(name+'_SOURCE_READING.png'))


def geometry():
    """Conservative inner Eutin envelope, not a cadastral or certified projection."""
    from map2l_franconia import inside
    b=load('BASELINE.json');before=core.packed(OUT/'provinces_before.png')
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    # Town symbols read on Reilly 300; geographic coordinates from retained
    # GeoNames data. The Baltic diagnostic is EXTRAPOLATED, never certified.
    controls=[('Kiel',[116,255],[10.13489,54.32133]),
        ('Eutin',[495,528],[10.61148,54.13503]),
        ('Ploen',[332,578],[10.42765,54.16202]),
        ('Neustadt',[826,592],[10.81450,54.10707]),
        ('Luebeck',[710,950],[10.68729,53.86893])]
    def target(ll):
        lon,lat=ll
        return [4092.4925269824366+23.057991056249843*lon,
                2410.485279266792-30.99674943247102*lat]
    source=np.array([[*s,1] for _,s,_ in controls]);targets=np.array([target(ll) for _,_,ll in controls])
    matrix=np.linalg.lstsq(source,targets,rcond=None)[0]
    residuals=np.linalg.norm(source@matrix-targets,axis=1)
    # Correct only the measured technical offset at the existing Kiel hub.
    # This is a consistency anchor, not surveyed proof of city placement.
    kiel=np.array([4325.842285,726.857910]);delta=kiel-targets[0];matrix[2]+=delta
    polygon=[[333,535],[400,555],[460,555],[490,510],[485,480],[492,440],
        [500,360],[550,358],[600,370],[651,394],[740,400],[795,407],[815,438],
        [808,465],[780,482],[750,490],[735,512],[740,560],[754,590],[804,603],
        [812,623],[782,643],[750,652],[670,655],[630,638],[580,618],[520,621],
        [480,624],[450,645],[435,649],[420,630],[420,615],[375,608],[315,603],[320,580]]
    x0,y0,x1,y1=BOX;yy,xx=np.mgrid[y0:y1,x0:x1];cells=np.column_stack((xx.ravel()+.5,yy.ravel()+.5))
    src=(cells-matrix[2])@np.linalg.inv(matrix[:2]);envelope=inside(src,polygon).reshape(xx.shape)
    # Rasterize the documented perimeter at cell centres, without an arbitrary
    # pixel shift or enlargement. This B envelope is NOT a cadastral boundary.
    core_mask=envelope
    full=np.zeros(before.shape,bool);full[y0:y1,x0:x1]=core_mask
    permitted={'x64824C','x60809F'}
    full &= np.isin(before,[int(s[1:],16) for s in permitted])
    # No separate city-cell enlargement, no access to Ahrensboek or Schwartau.
    full[738:]=False
    assert full.sum()>=4
    # The Bosau spur may rasterize into isolated cells. Keep only the actual
    # Eutin-bearing component; never manufacture a connecting corridor.
    town=np.array([495,528,1])@matrix
    town_cell=(int(town[1]),int(town[0]))
    parts=core.components(full)
    selected=next((p for p in parts if town_cell in p),None)
    assert selected is not None,'The Eutin town symbol must remain inside the installed nucleus'
    excluded_cells=int(full.sum())-len(selected)
    full[:]=False
    for y,x in selected:full[y,x]=True
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    parents=sorted('x'+format(int(v),'06X') for v in np.unique(before[full]))
    after=before.copy();assignments=[];new=[];counter=0;used=set(np.unique(before).tolist())
    for parent in parents:
        sid,old=owners[parent];assert sid==REGION
        native=before==int(parent[1:],16)
        for take,tag in [(native&~full,old),(native&full,'HLB')]:
            if not take.any():continue
            parts=core.components(take)
            # Keep the original on the largest retained native component.
            biggest=max(range(len(parts)),key=lambda i:len(parts[i]))
            for i,part in enumerate(parts):
                selected=np.zeros_like(take)
                for y,x in part:selected[y,x]=True
                rgb=parent
                if tag=='HLB' or i!=biggest:
                    while 0xEDB200+counter in used:counter+=1
                    value=0xEDB200+counter;counter+=1;used.add(value);rgb='x'+format(value,'06X')
                    new.append(dict(rgb=rgb,parent_rgb=parent))
                cy,cx=np.where(selected);after[selected]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=old,
                    owner=tag,pixels=int(selected.sum()),cells=[[int(x),int(y)] for y,x in zip(cy,cx)],
                    source_zone=1 if tag=='HLB' else 0))
    for loc in load('NATIVE_LOCATORS.json'):
        x,y=int(loc['X']),int(loc['Y']);assert before[y,x]==after[y,x],'No hub rebinding in this nucleus'
    Image.fromarray(np.stack(((after>>16)&255,(after>>8)&255,after&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('TRACING.json',dict(source='EVIDENCE/REILLY_WAGRIEN_300.jpg',polygon=polygon,
        controls=[dict(name=n,source=s,geographic_lon_lat=ll,diagnostic_target=target(ll),fit_residual_px=float(e)) for (n,s,ll),e in zip(controls,residuals)],
        source_to_bitmap_matrix=matrix.tolist(),kiel_technical_offset_px=delta.tolist(),
        eutin_symbol_estimate=town.tolist(),excluded_disconnected_cells=excluded_cells,
        historical_class='B; source perimeter generalized at bitmap cell centres',native_erosion_cells=0,
        warning='No independently certified native georeferencing here. Geographic extrapolation, source distortions and hub offsets remain. Fit errors are NOT validation errors. No arbitrary one-cell enlargement or shrinkage. Chapter parcels remain unresolved.'))
    dump('GEOMETRY.json',dict(status='MAP2Q_EUTIN_B_CORE_ONLY',parents=parents,assignments=assignments,
        new_provinces=new,hub_rebindings=[],candidate_sha256=core.sha(OUT/'provinces_candidate.png'),
        tracing_sha256=core.sha(OUT/'TRACING.json'),changed_pixels=int((after!=before).sum()),
        limitations=['Schwartau and dispersed chapter possessions not transferred.','No certified city error bound; source-traced inner envelope is a game-scale approximation B.']))
    im=Image.open(OUT/'EVIDENCE/REILLY_WAGRIEN_300.jpg').convert('RGB');draw=ImageDraw.Draw(im)
    draw.line([tuple(p) for p in polygon]+[tuple(polygon[0])],fill='blue',width=2)
    for r in assignments:
        if r['owner']!='HLB':continue
        for x,y in r['cells']:
            corners=(np.array([[x,y],[x+1,y],[x+1,y+1],[x,y+1],[x,y]])-matrix[2])@np.linalg.inv(matrix[:2])
            draw.line([tuple(p) for p in corners],fill='#118811',width=1)
    im.save(OUT/'EUTIN_SOURCE_SELECTION.png')
    print('B nucleus',sum(r['pixels'] for r in assignments if r['owner']=='HLB'),'cells;',len(new),'new RGBs;',parents)
    print('Fit residuals only',residuals.tolist())


def extra_files(files, migration):
    import re
    b=load('BASELINE.json');assert 'HLB' not in b['inventory']['countries']
    defs='HLB = { color = { 186 113 95 } country_type = recognized tier = principality cultures = { north_german } religion = protestant capital = STATE_SCHLESWIG_HOLSTEIN }\n'
    files['common/country_definitions/1776_map2q_eutin.txt']=defs
    text=(ROOT/'common/history/countries/hol - holstein.txt').read_text(encoding='utf-8-sig')
    text=text.replace('c:HOL','c:HLB').replace('effect_starting_politics_conservative = yes','''activate_law = law_type:law_land_based_taxation
        activate_law = law_type:law_hereditary_bureaucrats
        activate_law = law_type:law_peasant_levies
        activate_law = law_type:law_no_police
        activate_law = law_type:law_guild_system
        activate_law = law_type:law_tenant_farmers
        activate_law = law_type:law_no_workers_rights
        activate_law = law_type:law_autocracy
        activate_law = law_type:law_theocracy
        activate_law = law_type:law_aor1776_eutin_customs
        activate_law = law_type:law_aor1776_eutin_free_status''')
    files['common/history/countries/hlb - eutin.txt']=text
    laws=(ROOT/'common/laws/1776_map2l_osnabruck_start_variants.txt').read_text(encoding='utf-8-sig').replace('c:WPO','c:HLB').replace('osnabruck','eutin')
    files['common/laws/1776_map2q_eutin_start_variants.txt']=laws
    files['common/government_types/00_1776_map2q_eutin.txt']='''gov_aor1776_eutin = {
 transfer_of_power = dictatorial
 male_ruler = "RULER_TITLE_PRINCE_BISHOP"
 female_ruler = "RULER_TITLE_PRINCE_BISHOP"
 possible = { c:HLB ?= this has_law = law_type:law_theocracy }
 on_government_type_change = { change_to_dictatorial = yes }
 on_post_government_type_change = { post_change_to_dictatorial = yes }
}
'''
    files['common/coat_of_arms/coat_of_arms/1776_map2q_eutin.txt']='''# Simplified historical episcopal gold cross on blue; not a reconstructed quartered dynastic achievement.
AOR1776_HLB = { pattern = "pattern_solid.tga" color1 = blue colored_emblem = { texture = "ce_cross_couped.dds" color1 = yellow instance = { position = { 0.5 0.5 } scale = { 0.8 0.8 } } } }
'''
    files['common/flag_definitions/1776_map2q_eutin.txt']='HLB = { flag_definition = { coa = AOR1776_HLB priority = 100 allow_overlord_canton = no } }\n'
    # Native union shares OLD's existing ruler; do not create a second monarch.
    files['common/history/diplomacy/99_1776_map2q_eutin_union.txt']='DIPLOMACY = { c:OLD ?= { create_diplomatic_pact = { country = c:HLB type = personal_union } } }\n'
    rel='common/diplomatic_actions/22_subject_personal_union.txt'
    assert not (ROOT/rel).exists(),'Review any existing override before altering it'
    original=(core.qa.GAME/rel).read_text(encoding='utf-8-sig')
    # Only the target-country maintenance condition is extended, not all
    # theocracies, and not OLD's own monarchy requirement.
    old='''scope:target_country = {
					country_has_monarchy_law = yes
					NOT = { has_law = law_type:law_bakufu }'''
    new='''scope:target_country = {
					# MAP2Q: approved episcopal union; every other native condition retained.
					OR = {
						country_has_monarchy_law = yes
						AND = { c:HLB ?= this has_law = law_type:law_theocracy overlord ?= { c:OLD ?= this } }
					}
					NOT = { has_law = law_type:law_bakufu }'''
    assert original.count(old)==1
    files[rel]=original.replace(old,new)
    dump('PERSONAL_UNION_EXCEPTION.json',dict(native_file=str(core.qa.GAME/rel),native_sha256=core.sha(core.qa.GAME/rel),old=old,new=new,
        approval='User explicitly chose native personal union under OLD; 2026-10-16',
        invariant='Replacing this exact new block with old reconstructs the entire native file. No global theocratic-union permission.'))
    names={
        'HLB':('Prince-Bishopric of Lübeck','Principauté épiscopale de Lübeck'),
        'HLB_ADJ':('Eutinian','Eutinois'),
        'gov_aor1776_eutin':('Prince-bishopric','Principauté épiscopale'),
        'gov_aor1776_eutin_desc':('The Protestant prince-bishop rules the temporal lands from Eutin. Friedrich August also rules Oldenburg through a personal union; the two imperial estates remain distinct. The Free City of Lübeck is a separate state.','Le prince-évêque protestant gouverne ses terres temporelles depuis Eutin. Frédéric-Auguste règne aussi sur Oldenburg par une union personnelle ; les deux États impériaux restent distincts. La ville de Lübeck constitue un autre État.'),
        'law_aor1776_eutin_customs':('Episcopal customs','Douanes épiscopales'),
        'law_aor1776_eutin_customs_desc':('Regulated early-modern commerce without granting later technology.','Commerce réglementé d’Ancien Régime, sans accorder de technologie tardive.'),
        'law_aor1776_eutin_free_status':('Free legal status','Statut juridique libre'),
        'law_aor1776_eutin_free_status_desc':('1776 legal status; tenancy and serfdom remain separate laws.','Statut juridique de 1776 ; le régime foncier et le servage relèvent de lois distinctes.')}
    for lang,i in [('english',0),('french',1)]:
        files[f'localization/{lang}/1776_map2q_eutin_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[i]+'"\n' for k,v in names.items())
    migration.update(new_members=['HLB'],free_cities=[],country_additions={n.key:core.qa.signature(n) for n in core.cw.parse(defs)})
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'


def prepare():
    """Reuse reviewed allocation logic, with a new isolated baseline adapter."""
    # The legacy preparer reads BASELINE.json. Supply only its missing backup
    # field in memory, never rewrite the immutable file on disk.
    b=load('BASELINE.json');assert economy.runtime_hashes()==b['hashes']
    class ScopedJSON:
        @staticmethod
        def loads(s,*args,**kwargs):
            value=json.loads(s,*args,**kwargs)
            if isinstance(value,dict) and value.get('git_index_sha256')==b['git_index_sha256'] and 'inventory' in value and 'originals' in value:
                value['bitmap_backup']=(OUT/'provinces_before.png').relative_to(ROOT).as_posix()
            return value
        dumps=staticmethod(json.dumps)
    previous=core.json
    previous_emit=core.emit
    def reviewed_emit(files,name):
        dump('EXPECTED_TEXT.json',files)
        return previous_emit(files,name)
    try:
        core.OUT=OUT;core.REGIONS={REGION};core.json=ScopedJSON;core.PREPARE_EXTRA_FILES=extra_files;core.emit=reviewed_emit
        # No building file enters the allocation source. Preserve every
        # installed building, PM, economic ownership and recruitment exactly.
        core.prepare()
    finally:
        core.json=previous;core.emit=previous_emit
    plan=load('PLAN.json')
    # Store exact expected texts independently for guarded installation.
    patch=(OUT/'HISTORY.patch').read_text(encoding='utf-8')
    print('Review generated HISTORY.patch before applying; no runtime writes yet')


def install():
    b=load('BASELINE.json');g=load('GEOMETRY.json');plan=load('PLAN.json')
    current=economy.runtime_hashes()
    for p,text in load('EXPECTED_TEXT.json').items():
        assert (ROOT/p).read_text(encoding='utf-8-sig').rstrip('\r\n')==text.lstrip('\ufeff').rstrip('\r\n'),p
    changed={p for p,h in current.items() if b['hashes'].get(p)!=h}
    assert changed==set(plan['files'])&set(current),(changed,set(plan['files']))
    assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    assert core.sha(OUT/'provinces_candidate.png')==g['candidate_sha256']
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    shutil.copyfile(OUT/'province_terrains_candidate.txt',ROOT/'map_data/province_terrains.txt')
    print('Installed guarded Eutin bitmap and inherited terrains')


def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files)
    core.OUT=OUT;changes=core.emit(files,'IMPERIAL.patch')
    dump('IMPERIAL_FILES.json',dict(files=changes,all_compiled_files=list(files)))
    print('Prepared',len(changes),'imperial runtime updates')


def compiler_preservation():
    """Recompile the PRE-lot constitutional inputs to detect template drift."""
    import map2k_imperial_system as compiler
    b=load('BASELINE.json');dump('PRE_LOT_REGISTRY.json',b['registry'])
    original_inventory=compiler.qa.inventory;original_path=compiler.active_registry_path;original_members=compiler.additional_members
    import map2l_registry as registry
    original_registry_members=registry.additional_members
    compiler.MEMBERS=[t for t in compiler.MEMBERS if t!='HLB'];compiler.OUT=OUT
    try:
        compiler.qa.inventory=lambda:b['inventory']
        compiler.active_registry_path=lambda:OUT/'PRE_LOT_REGISTRY.json'
        compiler.additional_members=lambda:[t for t in original_members() if t!='HLB']
        registry.additional_members=compiler.additional_members
        previous=compiler.compile_system()
    finally:
        compiler.qa.inventory=original_inventory;compiler.active_registry_path=original_path
        compiler.additional_members=original_members;registry.additional_members=original_registry_members
    results=[]
    for path,expected in previous.items():
        actual=(ROOT/path).read_text(encoding='utf-8')
        results.append(dict(file=path,unchanged_pre_lot_template=actual.lstrip('\ufeff')==expected.lstrip('\ufeff')))
    dump('IMPERIAL_COUNTERFACTUAL_COMPARISON.json',results)
    assert all(r['unchanged_pre_lot_template'] for r in results),[r for r in results if not r['unchanged_pre_lot_template']]
    print(len(results),'pre-lot compiler outputs match the still-installed pre-lot imperial files')


def previews():
    from PIL import ImageColor
    b=load('BASELINE.json');before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    new=dict(old);new.update({r['rgb']:r['owner'] for r in load('GEOMETRY.json')['assignments']})
    def panel(bmp,owners,box,title):
        x0,y0,x1,y1=box;local=bmp[y0:y1,x0:x1];scale=32
        arr=np.full((*local.shape,3),(187,215,233),dtype=np.uint8)
        colors={'HOL':'#99b899','LUB':'#b392cf','SCH':'#e7d188','HLB':'#c97855','MEC':'#a8bacb','HAM':'#ee9585'}
        for value in np.unique(local):
            tag=owners.get('x'+format(int(value),'06X'))
            if tag:arr[local==value]=ImageColor.getrgb(colors.get(tag,'#ddd'))
        im=Image.fromarray(arr).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST)
        out=Image.new('RGB',(im.width,im.height+110),'white');out.paste(im,(0,35));d=ImageDraw.Draw(out)
        font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
        d.text((8,8),title,fill='black',font=font)
        for x in range(x0,x1):d.line(((x-x0)*scale,35,(x-x0)*scale,35+im.height),fill='#6a7374')
        for y in range(y0,y1):d.line((0,(y-y0)*scale+35,im.width,(y-y0)*scale+35),fill='#6a7374')
        d.text((8,im.height+42),'HOL vert / LUB violet / HLB terre cuite',fill='black',font=font)
        d.text((8,im.height+65),'Raster B : approximation, pas un cadastre.',fill='black',font=font)
        d.text((8,im.height+86),f'X {x0}–{x1-1} ; Y {y0}–{y1-1}',fill='black',font=font)
        return out
    for name,box in [('EUTIN',(4328,725,4346,739)),('SCHWARTAU',(4332,736,4349,749))]:
        panels=[panel(before,old,box,'AVANT MAP-2Q'),panel(after,new,box,'APRES : '+('noyau Eutin' if name=='EUTIN' else 'Schwartau inchange'))]
        im=Image.new('RGB',(sum(p.width for p in panels),panels[0].height),'white')
        im.paste(panels[0]);im.paste(panels[1],(panels[0].width,0));im.save(OUT/(name+'_BEFORE_AFTER.png'))


def maps():
    # Membership/RGB subdivision changes, but the imperial extent is identical.
    # Preserve the main-map mask; regenerate only journal internal boundaries.
    import render_map2k_imperial_map as journal
    journal.OUT=OUT;journal.render()


def validate():
    from map2l_registry import approved_lot_dirs,apply_territorial_migrations,expected_country_definitions
    from map_1776_audit import effective
    b=load('BASELINE.json');g=load('GEOMETRY.json');plan=load('PLAN.json');inv=core.qa.inventory();checks=[]
    def check(name,passed,detail=None):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
        if not passed:print('FAIL',name,detail,flush=True)
    before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    oldowners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    # Initial Q preserves population only because its allocation was technical.
    # An explicit subsequent demographic lot can change the world total; test
    # its signed delta and profiles, never a permanently fixed world constant.
    demographic=None;demographic_expected={}
    demographic_file=OUT/'CONTINUATION_R2/APPLIED_DEMOGRAPHY.json'
    if demographic_file.exists():
        demographic=json.loads(demographic_file.read_text(encoding='utf8'))
        db=json.loads((demographic_file.parent/'BASELINE.json').read_text(encoding='utf8'))
        de=json.loads((demographic_file.parent/'EXPECTED_POPULATION.json').read_text(encoding='utf8'))
        check('R2 demographic scope and approved estimate',demographic['lot']=='MAP2Q_R2' and demographic['state']==REGION and demographic['tag']=='HLB' and demographic['after']==7600 and demographic['delta']==-3725)
        check('R2 immutable baseline and installed text match',core.sha(demographic_file.parent/'BASELINE.json')==demographic['baseline_sha256'] and core.sha(ROOT/demographic['file'])==demographic['expected_source_sha256'] and (ROOT/demographic['file']).read_text(encoding='utf-8-sig')==de['text'])
        check('R2 starts from the original Q population text',db['original_pops'].strip()==load('EXPECTED_TEXT.json')[demographic['file']].lstrip('\ufeff').strip())
        cultures={n.key:core.cw.scalar(n.one('religion','UNRESOLVED_DEFAULT')) for p in effective(ROOT,core.qa.GAME,'common/cultures') for n in core.cw.parse(p.read_text(encoding='utf-8-sig'))}
        for key in ['pops','resolved_demographics']:
            expected_counter=core.qa.counter(b['inventory'][key])
            for row in demographic['profiles']:
                religion=row['religion']
                if religion=='DEFAULT':religion='DEFAULT:'+row['culture'] if key=='pops' else cultures[row['culture']]
                expected_counter[row['culture'],religion]+=row['delta']
            demographic_expected[key]=+expected_counter
    world_delta=demographic['delta'] if demographic else 0
    check('World variation equals the authorized demographic delta',sum(r['count'] for r in inv['pops'])-sum(r['count'] for r in b['inventory']['pops'])==world_delta)
    for key in ['pops','resolved_demographics','buildings','building_levels_written','units','errors','duplicates']:
        check('Authorized demographic profiles '+key,core.qa.counter(inv[key])==demographic_expected[key]) if key in demographic_expected else check('Exact preservation '+key,inv[key]==b['inventory'][key])
    check('Preexisting anomalies remain 44 duplicated RGB and 12 references',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    check('Only approved country HLB added',inv['countries']==expected_country_definitions(b['inventory']['countries'],[load('REGISTRY_MIGRATION.json')]))
    check('No preexisting State_ID changed',all(inv['geometry'].get(rgb)==sid for rgb,sid in b['inventory']['geometry'].items()))
    expected_owners=[r for r in b['inventory']['owners'] if r['key'][0] not in g['parents']]+[dict(key=[r['rgb'],r['state'],r['owner']],count=1) for r in g['assignments']]
    check('Every owner exactly equals declared delta',core.qa.counter(inv['owners'])==core.qa.counter(expected_owners))
    check('One owner and state for each new RGB',all(owners[r['rgb']][0]==REGION and inv['geometry'][r['rgb']]==REGION for r in g['new_provinces']))
    expected=before.copy()
    for r in g['assignments']:
        check('RGB connected '+r['rgb'],len(core.components(after==int(r['rgb'][1:],16)))==1)
        check('RGB cell count '+r['rgb'],int((after==int(r['rgb'][1:],16)).sum())==r['pixels'])
        for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
    check('Bitmap exactly replays approved cells, no outside edit',np.array_equal(expected,after))
    check('Bitmap recolouring count matches manifest',int((before!=after).sum())==g['changed_pixels'])
    transferred=[r for r in g['assignments'] if r['owner']=='HLB']
    check('31 sovereignty transfers: 19 LUB and 12 HOL',C.Counter({tag:sum(r['pixels'] for r in transferred if r['previous_owner']==tag) for tag in ['LUB','HOL']})=={'LUB':19,'HOL':12})
    country_mask=np.isin(after,[int(r['rgb'][1:],16) for r in transferred])
    check('Eutin political nucleus is connected',len(core.components(country_mask))==1)
    point=load('TRACING.json')['eutin_symbol_estimate'];check('Source town symbol lies in HLB',bool(country_mask[int(point[1]),int(point[0])]))
    check('Capital State_ID 66 owned by HLB',[REGION,'HLB'] in inv['states'] and 'capital = STATE_SCHLESWIG_HOLSTEIN' in (ROOT/'common/country_definitions/1776_map2q_eutin.txt').read_text())
    check('Schwartau and southern city territory untouched',np.array_equal(before[738:745,4337:4347],after[738:745,4337:4347]))
    check('Schleswig, Elbe and all other regions unchanged',all(inv['geometry'].get(r['rgb'])==REGION for r in g['new_provinces']) and all(r['state']==REGION for r in g['assignments']))
    regional=core.qa.counter(b['inventory']['regional_pop'])
    for alloc in plan['allocations']:
        check('Integer allocation conserved '+alloc['source']+'/'+alloc['profile'],sum(alloc['after'].values())==alloc['before'] and all(isinstance(v,int) and v>=0 for v in alloc['after'].values()))
        culture,religion=alloc['profile'].split('/');religion='DEFAULT:'+culture if religion=='DEFAULT' else religion
        regional[REGION,alloc['source'],culture,religion]-=alloc['before']
        for tag,n in alloc['after'].items():regional[REGION,tag,culture,religion]+=n
    if demographic:
        for row in demographic['profiles']:
            religion=row['religion'] if row['religion']!='DEFAULT' else 'DEFAULT:'+row['culture']
            regional[REGION,'HLB',row['culture'],religion]+=row['delta']
    check('Every population region/profile equals allocation plus approved historical delta',+regional==core.qa.counter(inv['regional_pop']))
    check('HLB equals the approved population stage',sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='HLB')==(demographic['after'] if demographic else 11325))
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf-8'))
    migration=load('REGISTRY_MIGRATION.json')
    expected_ledger=sorted([r for r in b['registry'] if r['state']!=REGION]+migration['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    check('508 province rights exactly replay MAP2Q on the validated pre-lot registry',ledger==expected_ledger and len(ledger)==508 and sorted(migration['previous'],key=lambda r:r['rgb'])==sorted([r for r in b['registry'] if r['state']==REGION],key=lambda r:r['rgb']))
    oldmask=np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]);newmask=np.isin(after,[int(r['rgb'][1:],16) for r in ledger])
    check('World imperial extent pixel-exact',np.array_equal(oldmask,newmask))
    check('Main-map imperial mask unchanged',core.sha(ROOT/'gfx/map/map_painting/aor1776_hre_mask.dds')==b['hashes']['gfx/map/map_painting/aor1776_hre_mask.dds'])
    previous_registry={r['rgb']:r for r in b['registry']}
    check('Other imperial rights byte-equivalent as objects',all(r==previous_registry[r['rgb']] for r in ledger if r['state']!=REGION))
    for loc in load('NATIVE_LOCATORS.json'):
        x,y=int(loc['X']),int(loc['Y']);check('Native hub unchanged '+loc['Kind']+'/'+str(loc['ID']),before[y,x]==after[y,x])
    for path in load('IMPERIAL_EXPECTED.json'):
        check('Imperial compiler exact '+path,(ROOT/path).read_text(encoding='utf-8-sig')==load('IMPERIAL_EXPECTED.json')[path].lstrip('\ufeff'))
    check('Pre-lot compiler had no template drift',all(r['unchanged_pre_lot_template'] for r in load('IMPERIAL_COUNTERFACTUAL_COMPARISON.json')))
    union=load('PERSONAL_UNION_EXCEPTION.json');p='common/diplomatic_actions/22_subject_personal_union.txt';text=(ROOT/p).read_text(encoding='utf-8-sig')
    check('Union override equals native except one explicit OLD/HLB maintenance clause',text.count(union['new'])==1 and text.replace(union['new'],union['old'])==Path(union['native_file']).read_text(encoding='utf-8-sig'))
    check('OLD native source itself untouched',core.sha(Path(union['native_file']))==union['native_sha256'])
    check('Exactly one OLD to HLB native personal union','country = c:HLB type = personal_union' in (ROOT/'common/history/diplomacy/99_1776_map2q_eutin_union.txt').read_text())
    check('No synthetic duplicate ruler created',not (ROOT/'common/history/characters/1776_map2q_eutin.txt').exists())
    for path,text in load('EXPECTED_TEXT.json').items():
        if path.startswith('docs/') or path in load('IMPERIAL_EXPECTED.json'):continue
        if demographic and path==demographic['file']:text=de['text']
        check('Prepared text installed '+path,(ROOT/path).read_text(encoding='utf-8-sig').rstrip('\r\n')==text.lstrip('\ufeff').rstrip('\r\n'))
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');import re
    terrain_map=dict(re.findall(r'(?im)^\s*(x[0-9a-fA-F]{6})\s*=\s*"([^"\n]+)"',terrain))
    for r in g['new_provinces']:check('Inherited terrain '+r['rgb'],terrain_map[r['rgb']]==terrain_map[r['parent_rgb']])
    # Parse all changed Clausewitz files, and verify direct law/technology/asset references.
    current=economy.runtime_hashes();changed={p for p,h in current.items() if b['hashes'].get(p)!=h}
    allowed=(set(plan['files'])|set(load('IMPERIAL_FILES.json')['files'])|{'map_data/provinces.png','map_data/province_terrains.txt','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'})
    check('No unrelated runtime file written',changed<=allowed,sorted(changed-allowed))
    for path in sorted(changed):
        if path.endswith('.txt'):
            try:core.cw.parse((ROOT/path).read_text(encoding='utf-8-sig'));valid=True
            except Exception:valid=False
            check('Clausewitz parse '+path,valid)
    for prefix in ['common/history/buildings/','common/history/military_formations/','common/history/characters/']:
        check('Every installed file preserved '+prefix,all(current.get(p)==h for p,h in b['hashes'].items() if p.startswith(prefix)))
    for folder in ['common/laws','common/technology/technologies']:
        ids={n.key for path in effective(ROOT,core.qa.GAME,folder) for n in core.cw.parse(path.read_text(encoding='utf-8-sig'))}
        history=(ROOT/'common/history/countries/hlb - eutin.txt').read_text(encoding='utf-8-sig')
        refs=re.findall(r'activate_law\s*=\s*law_type:(\w+)',history) if folder.endswith('laws') else re.findall(r'add_technology_researched\s*=\s*(\w+)',history)
        check('New country references exist '+folder,set(refs)<=ids,sorted(set(refs)-ids))
    for lang in ['english','french']:
        p=ROOT/f'localization/{lang}/1776_map2q_eutin_l_{lang}.yml';text=p.read_text(encoding='utf-8-sig')
        keys=re.findall(r'^ (\w+):',text,re.M)
        check('Localized HLB name, adjective and government description '+lang,{'HLB','HLB_ADJ','gov_aor1776_eutin','gov_aor1776_eutin_desc'}<=set(keys) and len(keys)==len(set(keys)) and p.read_bytes().startswith(b'\xef\xbb\xbf'))
    check('Native heraldic cross texture exists',(core.qa.GAME/'gfx/coat_of_arms/colored_emblems/ce_cross_couped.dds').exists())
    # All older report artifacts are protected, except the explicitly versioned active ledger.
    ledger_rel=core.active_registry_path().relative_to(ROOT).as_posix()
    prior_changed=[p for p,h in b['prior_report_hashes'].items() if p!=ledger_rel and (not (ROOT/p).exists() or core.sha(ROOT/p)!=h)]
    check('Every older baseline/report preserved',not prior_changed,prior_changed)
    check('Bridge and isolated prototype untouched',all((ROOT/p).exists() and core.sha(ROOT/p)==h for p,h in b['bridge_and_prototype_hashes'].items()))
    check('Git HEAD untouched',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index untouched',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    a=core.qa.counter(b['inventory']['regional_pop']);z=core.qa.counter(inv['regional_pop'])
    pop=[dict(State_ID=k[0],Owner_TAG=k[1],Culture=k[2],Religion=k[3],Before_people=a[k],After_people=z[k],Difference_people=z[k]-a[k]) for k in sorted(a.keys()|z.keys()) if k[0]==REGION]
    dump('TABLE_DATA.json',dict(population=pop))
    status=('MAP2Q_PARTIAL_SCHWARTAU_AND_CHAPTERS_UNRESOLVED' if demographic else 'MAP2Q_PARTIAL_HISTORICAL_POPULATION_UNRESOLVED') if all(r['passed'] for r in checks) else 'MAP2Q_STATIC_FAILURE'
    dump('VALIDATION.json',dict(status=status,checks=checks,passed=sum(r['passed'] for r in checks),total=len(checks),
        native_runtime_test='NOT_RUN; user required',historical_scope='B Eutin nucleus only; C Schwartau and chapter parcels unresolved',
        population_policy='Historical 1776 population overrides fixed world total; user decision 2026-10-16. No forced compensation elsewhere.',
        historical_population_status='7600: user-accepted historical approximation; plausible working envelope 6500-9000, not a census or a confidence interval; see CONTINUATION_R2.' if demographic else 'UNRESOLVED: 11325 is provisional game allocation, NOT a historical population. No supported 1776 total for the installed nucleus has been found.',
        population_world_before=sum(r['count'] for r in b['inventory']['pops']),population_world_after=sum(r['count'] for r in inv['pops']),
        preexisting_duplicate_RGBs=inv['duplicates'],preexisting_reference_errors=inv['errors'],
        runtime_files_changed=sorted(changed),new_RGBs=g['new_provinces'],sovereignty_transferred_cells=31,
        ColGrep=dict(agent_calls=1,reported_elapsed_seconds=92.5,result='No valid location; irrelevant inspected files; rg fallback',exact_quota_savings='not measurable')))
    dump('INSTALLED_MANIFEST.json',dict(functional_files={p:current[p] for p in sorted(changed)},registry_sha256=core.sha(core.active_registry_path())))
    print(status,sum(r['passed'] for r in checks),'/',len(checks),flush=True)
    if not all(r['passed'] for r in checks):raise SystemExit(1)


def unit_tests():
    import os,time
    suites=['test_map2l_registry','test_map2m_r8','test_map2m_r9','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(ROOT/'tools'),'GIT_OPTIONAL_LOCKS':'0'}
    start=time.monotonic()
    result=subprocess.run([sys.executable,'-B','-X','utf8','-m','unittest',*suites],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    dump('UNIT_TESTS.json',dict(command=[sys.executable,'-B','-X','utf8','-m','unittest',*suites],
        seconds=round(time.monotonic()-start,2),exit_code=result.returncode,output=result.stdout+result.stderr,
        scope='Existing registry and earlier boundary regression unit tests; not an engine test'))
    print(result.stdout+result.stderr)
    if result.returncode:raise SystemExit(result.returncode)


def tables():
    b=load('BASELINE.json');g=load('GEOMETRY.json');after=core.packed(ROOT/'map_data/provinces.png');before=core.packed(OUT/'provinces_before.png')
    data=load('TABLE_DATA.json')
    data['CURRENT_PROVINCES.csv']=[dict(RGB=r['key'][0],State_ID=r['key'][1],Owner_before=r['key'][2],Before_cells=int((before==int(r['key'][0][1:],16)).sum()),After_same_RGB_cells=int((after==int(r['key'][0][1:],16)).sum()),Source='BASELINE.json / actual bitmap') for r in b['inventory']['owners'] if r['key'][1]==REGION]
    data['TERRITORIAL_CHANGES.csv']=[dict(RGB=r['rgb'],Parent_RGB=r['parent_rgb'],State_ID=r['state'],Owner_before=r['previous_owner'],Owner_after=r['owner'],Cells=r['pixels'],Historical_class='B' if r['owner']=='HLB' else 'Retained',Applied='yes',Source='Reilly 300 / GEOMETRY.json') for r in g['assignments']]
    data['POPULATION_VALIDATION.csv']=data.pop('population')
    data['1776_TERRITORIAL_INVENTORY.csv']=[
        dict(Territory='Eutin temporal core',Institution='Prince-bishop',TAG='HLB',Historical_class='B',Applied='31 cells',Population_1776_people=None,Population_status='11325 technical only; historical target unresolved',Source='https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2633'),
        dict(Territory='Schwartau / Amt Kaltenhof',Institution='Prince-bishop',TAG='HLB',Historical_class='C geometry',Applied='no',Population_1776_people=None,Population_status='unresolved; do not double count Eutin',Source='https://www.kuladig.de/Objektansicht/KLD-290005'),
        dict(Territory='Luebeck Free City',Institution='Municipal republic',TAG='LUB',Historical_class='Preserved city core',Applied='19 northern cells removed; city retained',Population_1776_people=None,Population_status='Urban counts are not country totals',Source='https://bekanntmachungen.luebeck.de/dokumente/d/1936/inline'),
        dict(Territory='Cathedral chapter lands',Institution='Domkapitel',TAG=None,Historical_class='C',Applied='no blanket transfer',Population_1776_people=None,Population_status='Separate jurisdiction and counting scope',Source='https://arcinsys.schleswig-holstein.de/arcinsys/showClassificationPointDetails?classificationPointId=21'),
        dict(Territory='Eutin collegiate chapter lands',Institution='Kollegiatstift',TAG=None,Historical_class='C',Applied='no blanket transfer',Population_1776_people=None,Population_status='Separate counting scope',Source='https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2633'),
        dict(Territory='Oldenburg',Institution='Duchy; shared ruler',TAG='OLD',Historical_class='Dynastic link established',Applied='Native personal union OLD to HLB; no land transfer',Population_1776_people=None,Population_status='unchanged; no population fusion',Source='https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2633')]
    data['UNRESOLVED.csv']=[
        dict(Item='Historical population of HLB in 1776',Status='BLOCKS_FULL_COMPLETION',Missing='Dated count with matching installed territorial scope',Current_action='11325 explicitly provisional; no false historical total',Next_action='Read contemporary census or defensible near-1776 estimate'),
        dict(Item='Schwartau / Kaltenhof boundary',Status='C_NOT_APPLIED',Missing='Jurisdictional polygon separating bishop chapter and city',Current_action='Unchanged; no artificial city-cell enlargement',Next_action='Targeted local source only'),
        dict(Item='Chapter and private dispersed estates',Status='C_NOT_APPLIED',Missing='High jurisdiction versus landed property, 1776 scope',Current_action='No 1803 blanket incorporation',Next_action='Classify evidence without manufacturing microstates'),
        dict(Item='Native map placement accuracy',Status='B_APPROXIMATION',Missing='Independent local native physical controls',Current_action='Source perimeter rasterized; no certified independent accuracy claimed',Next_action='Inspect in game; do not confuse fitting error with accuracy'),
        dict(Item='Personal union J30',Status='RUNTIME_PENDING',Missing='Manual fresh-start month simulation',Current_action='Narrow native maintenance exception installed',Next_action='Verify shared ruler and union survival'),
        dict(Item='Preexisting map anomalies',Status='UNCHANGED',Missing='44 duplicated RGB and 12 invalid references from older lots',Current_action='Preserved separately from new regressions',Next_action='Out of scope')]
    dump('CSV_TABLES.json',data)
    print('Five typed CSV datasets prepared for independent tabular verification')


def reconcile():
    import re,difflib
    expected=load('EXPECTED_TEXT.json')
    # Formatting-only cleanup of two blank lines introduced by this lot;
    # preserve all preexisting whitespace and collaborators' unrelated edits.
    rules={
        'common/history/states/00_states.txt':('\n\t\ncreate_state = { country = c:HLB','\n\ncreate_state = { country = c:HLB'),
        'common/history/pops/00_west_europe.txt':('\n\t\n\t\tregion_state:HLB','\n\n\t\tregion_state:HLB')}
    for p,(old,new) in rules.items():
        assert expected[p].count(old)==1
        expected[p]=expected[p].replace(old,new)
        assert (ROOT/p).read_text(encoding='utf-8-sig')==expected[p]
    dump('EXPECTED_TEXT.json',expected)
    a=load('UNIT_TESTS.json');b=load('UNIT_TESTS_PRE_LOT.json')
    current=re.findall(r'^FAIL: .*?\(([^)]+)\)',a['output'],re.M)
    known=b['failures'];additional=sorted(set(current)-set(known))
    assert len(known)==3 and len(current)==6 and len(additional)==3
    dump('UNIT_TEST_RECONCILIATION.json',dict(old_suites_tests=68,current_passed=62,current_failed=6,
        reproduced_on_pre_lot_baseline=known,later_stage_snapshot_assumptions=additional,
        explanation='Three old R8/R9 snapshot assertions already fail on the exact pre-MAP2Q bitmap. Three more compare whole-world bitmap or an old-only ledger after an authorized additive lot. MAP2Q exact cell replay and pre-lot owner/rights preservation are checked separately. Earlier test files and baselines were NOT rewritten or marked PASS.',
        map2q_specific_tests=load('UNIT_TESTS_MAP2Q.json')))
    baseline=load('BASELINE.json');new=expected
    added_whitespace=[]
    for p,raw in baseline['originals'].items():
        if p not in new:continue
        a=raw.splitlines();z=new[p].splitlines()
        for op,_,_,start,end in difflib.SequenceMatcher(None,a,z).get_opcodes():
            if op not in {'insert','replace'}:continue
            added_whitespace.extend([dict(file=p,line=i+1) for i in range(start,end) if z[i].rstrip()!=z[i]])
    dump('WHITESPACE_VALIDATION.json',dict(new_added_trailing_whitespace=added_whitespace,
        git_diff_check_all_workspace='Preexisting trailing whitespace remains in older changed blocks; not reformatted',
        cleanup='Only two newly introduced blank lines trimmed'))
    assert not added_whitespace
    print('Reconciled legacy snapshot failures; no new trailing whitespace')


if __name__=='__main__':
    globals()[sys.argv[1]]()
