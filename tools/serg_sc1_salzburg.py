"""SC1-SALZBURG: guarded evidence, installation and cumulative validation."""
import collections as C
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import map2w_r4bc as prior

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reports/map/SERG_CLOSURE/SC1-SALZBURG'
core = prior.core
sha = prior.pas.sha

def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(name, data):
    (OUT/name).parent.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf8')

def snapshot():
    assert not (OUT/'BASELINE.json').exists(), 'Immutable baseline already exists'
    OUT.mkdir(parents=True, exist_ok=True)
    hashes = prior.pas.prior.q.economy.runtime_hashes()
    inv = core.qa.inventory()
    shutil.copyfile(ROOT/'map_data/provinces.png', OUT/'provinces_before.png')
    dump('BASELINE.json', dict(hashes=hashes, inventory=inv,
        registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        git_index_sha256=sha(ROOT/'.git/index'),
        tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*') if p.is_file() and p.name!='serg_sc1_salzburg.py'},
        roadmap=load(ROOT/'docs/reports/map/SERG_CLOSURE/ROADMAP_STATE.json')))
    print('Baseline captured:',len(hashes),'runtime files,',len(inv['owners']),'owner rows')

def audit():
    b=load(OUT/'BASELINE.json'); a=core.packed(OUT/'provinces_before.png')
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    cal=load(ROOT/'docs/reports/map/MAP2W/R4/CALIBRATION.json')
    M=np.array(cal['matrix']); diagnostics={name:(np.array([lon,lat,1])@M).tolist() for name,lon,lat in [
        ('Salzburg',13.045,47.800),('Hallein',13.095,47.683),('Berchtesgaden',13.004,47.630),
        ('Laufen',12.930,47.940),('Tittmoning',12.768,48.061),('Reichenhall',12.881,47.724),
        ('Werfen',13.190,47.475),('Zell',12.797,47.324)]}
    x0,y0,x1,y1=4370,910,4430,965;s=16
    im=Image.new('RGB',((x1-x0)*s+70,(y1-y0)*s+120),'#faf9f5');d=ImageDraw.Draw(im)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    rivers=np.array(Image.open(ROOT/'map_data/rivers.png'))
    for y in range(y0,y1):
        for x in range(x0,x1):
            v=int(a[y,x]);u=55+(x-x0)*s;w=60+(y-y0)*s
            d.rectangle((u,w,u+s,w+s),fill=((v>>16)&255,(v>>8)&255,v&255),outline='#666666')
            if rivers[y,x]<=15:d.ellipse((u+5,w+5,u+10,w+10),fill='#147bdf',outline='white')
    for x in range(x0,x1,2):d.text((55+(x-x0)*s,40),str(x),font=f,fill='black')
    for y in range(y0,y1,2):d.text((2,60+(y-y0)*s),str(y),font=f,fill='black')
    for name,(x,y) in diagnostics.items():
        u=55+(x-x0)*s;v=60+(y-y0)*s
        d.ellipse((u-4,v-4,u+4,v+4),outline='white',width=2)
        d.text((u+5,v),name+' ?',font=f,fill='black',stroke_width=2,stroke_fill='white')
    d.text((12,10),'SC1-SALZBURG — grille native AVANT. Cercles : diagnostics R4 NON valides comme villes/frontieres.',font=f,fill='black')
    d.text((12,im.height-35),'Points bleus : rivieres natives. Aucune translation ni optimisation de projection.',font=f,fill='black')
    im.save(OUT/'NATIVE_AUDIT.png')
    vals,counts=np.unique(a[y0:y1,x0:x1],return_counts=True)
    rows=[]
    for v,n in zip(vals,counts):
        rgb='x'+format(int(v),'06X');yy,xx=np.where(a==v)
        rows.append(dict(rgb=rgb,owner=owners.get(rgb),window_cells=int(n),total_cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    dump('NATIVE_AUDIT.json',dict(box=[x0,y0,x1,y1],diagnostics=diagnostics,diagnostic_only=True,rows=rows))
    print(json.dumps(dict(diagnostics=diagnostics,rows=rows),ensure_ascii=False,indent=2))

def sources():
    from urllib.request import Request, urlopen
    from concurrent.futures import ThreadPoolExecutor
    urls={
        'ORTSLEXIKON.pdf':'https://www.oeaw.ac.at/fileadmin/subsites/Institute/VID/PDF/Publications/diverse_Publications/Historisches_Ortslexikon/Ortslexikon_Salzburg.pdf',
        'GREATER_SALZBURG.pdf':'https://www.salzburg.gv.at/fileadmin/Dateien/Salzburg/publikation-dasgroesseresalzburg.pdf',
        'REILLY_MANIFEST.json':'https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb00090512/manifest',
        'COLLOREDO_BIO.html':'https://www.deutsche-biographie.de/sfz8627.html',
        'COLLOREDO_SEAL.html':'https://gams.uni-graz.at/o:epis.sa-189/sdef:LIDO/get?context=context:epis.Salzburg.Hieronymus1772&mode=object',
        'ARCHIVE.html':'https://www.salzburg.gv.at/themen/salzburg/landesarchiv/historischesarchiv-zentralbehoerden'}
    def fetch(pair):
        name,url=pair;p=OUT/'EVIDENCE'/name;p.parent.mkdir(exist_ok=True)
        try:
            if not p.exists():
                with urlopen(Request(url,headers={'User-Agent':'1776-map-research/1.0'}),timeout=35) as response:p.write_bytes(response.read())
            return dict(file=name,url=url,sha256=sha(p),bytes=p.stat().st_size,success=True)
        except Exception as e:return dict(file=name,url=url,success=False,error=str(e))
    rows=list(ThreadPoolExecutor(max_workers=4).map(fetch,urls.items()))
    mf=OUT/'EVIDENCE/REILLY_MANIFEST.json'
    if mf.exists():
        m=load(mf)
        for i,c in enumerate(m['sequences'][0]['canvases']):
            url=c['images'][0]['resource']['service']['@id']+'/full/2500,/0/default.jpg'
            rows.append(fetch((f'REILLY_{i+1}.jpg',url)))
    dump('SOURCES_FETCH.json',rows)
    for r in rows: print(r['file'],r['success'],r.get('bytes',r.get('error')))

def candidates():
    a=core.packed(OUT/'provinces_before.png');b=load(OUT/'BASELINE.json')
    opts=[('CITY_ONLY',[[4385,923],[4389,923],[4389,927],[4385,927]]),
          ('BASIN_CORE',[[4385,923],[4389,923],[4390,927],[4390,931],[4387,931],[4386,928],[4385,926]]),
          ('WHOLE_NATIVE_PROVINCE',None)]
    donor=np.isin(a,[int(r['key'][0][1:],16) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_BAVARIA','BAV']])
    rows=[]
    for name,poly in opts:
        mask=a==0x6EA29B
        if poly is not None:
            yy,xx=np.where(mask);inside=core.inside(np.column_stack([xx+.5,yy+.5]),np.array(poly));mask[:]=False;mask[yy[inside],xx[inside]]=True
        yy,xx=np.where(mask);cells=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
        rows.append(dict(id=name,polygon=poly,cells=cells,count=len(cells),components=[len(c) for c in core.components(mask)],
            residual_parent_components=[len(c) for c in core.components((a==0x6EA29B)&~mask)],
            BAV_components_after=[len(c) for c in core.components(donor&~mask)],
            hubs_affected=[r for r in prior.pas.prior.q.r9.locators(a) if mask[int(r['Y']),int(r['X'])]]))
    dump('CANDIDATES.json',dict(parent='x6EA29B',before_cells=65,BAV_components_before=[len(c) for c in core.components(donor)],options=rows))
    for r in rows:print(r['id'],r['count'],r['components'],r['residual_parent_components'],r['BAV_components_after'],r['hubs_affected'])

def compiler_baseline():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT
    files=compiler.compile_system()
    current={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in files}
    differences=[p for p in files if current[p]!=files[p].lstrip('\ufeff')]
    dump('COMPILER_BEFORE.json',dict(expected=files,actual=current,differences=differences))
    print('Compiler baseline',len(files)-len(differences),'/',len(files), 'divergences',differences)

def prepare():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png')
    assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    assert 'SLZ' not in b['inventory']['countries']
    assert 'xEDBB00' not in b['inventory']['geometry'] and not np.any(a==0xEDBB00)
    choice=load(OUT/'CANDIDATES.json')['options'][0]
    assert choice['id']=='CITY_ONLY' and choice['count']==12 and choice['residual_parent_components']==[53]
    after=a.copy()
    for x,y in choice['cells']: assert a[y,x]==0x6EA29B;after[y,x]=0xEDBB00
    rows=[]
    for rgb,tag in [('x6EA29B','BAV'),('xEDBB00','SLZ')]:
        yy,xx=np.where(after==int(rgb[1:],16));cells=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
        rows.append(dict(rgb=rgb,parent_rgb='x6EA29B',state='STATE_BAVARIA',previous_owner='BAV',owner=tag,pixels=len(cells),cells=cells,
            confidence='B_POLITICAL_APPROXIMATION' if tag=='SLZ' else 'RETAINED_NOT_HISTORICALLY_CERTIFIED'))
    geo=dict(parents=['x6EA29B'],assignments=rows,new_provinces=[dict(rgb='xEDBB00',parent_rgb='x6EA29B')],new_members=['SLZ'],free_cities=[],
        selected_option='CITY_ONLY',classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,hub_rebindings=[])
    defs='SLZ = { color = { 188 145 61 } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = STATE_BAVARIA }\n'
    previous=[r for r in b['registry'] if r['state']=='STATE_BAVARIA']
    updated=sorted(previous+[dict(rgb='xEDBB00',state='STATE_BAVARIA',beneficiary='SLZ',basis='SC1-SALZBURG: residence nucleus B; see SERG_CLOSURE/SC1-SALZBURG/REPORT.md; no complete Erzstift boundary')],key=lambda r:r['rgb'])
    migration=dict(replaced_regions=['STATE_BAVARIA'],previous=previous,updated=updated,new_members=['SLZ'],free_cities=[],new_provinces=geo['new_provinces'],
        geometry='SERG_CLOSURE/SC1-SALZBURG/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],
        country_additions={'SLZ':core.qa.signature(core.cw.parse(defs)[0])})
    files={};originals={}
    def old(rel):
        assert sha(ROOT/rel)==b['hashes'][rel], 'Concurrent change: '+rel
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');originals[rel]=raw;return raw
    p='common/history/states/00_states.txt';raw=old(p);n=core.state(raw,'STATE_BAVARIA')
    files[p]=core.edits(raw,[(n.end-1,n.end-1,'\n\t\t# SC1-SALZBURG: documented political residence nucleus.\n\t\tcreate_state = { country = c:SLZ owned_provinces = { xEDBB00 } }\n\t')])
    p='map_data/state_regions/00_west_europe.txt';raw=old(p);n=next(n for n in core.cw.parse(raw) if n.key=='STATE_BAVARIA');f=n.children('provinces')[0]
    assert 'x6EA29B' not in core.values(n,'prime_land')
    fragment=raw[f.start:f.end];assert fragment.count('"x6EA29B"')==1
    files[p]=core.edits(raw,[(f.start,f.end,fragment.replace('"x6EA29B"','"x6EA29B" "xEDBB00"'))])
    p='map_data/province_terrains.txt';raw=old(p);assert not re.search('xEDBB00',raw,re.I)
    terrain=dict((k.upper(),v) for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw))
    files[p]=raw.rstrip()+'\n'+'xEDBB00="'+terrain['X6EA29B']+'"\n'
    p='common/history/pops/00_west_europe.txt';raw=old(p);n=core.region(raw,'STATE_BAVARIA','BAV')
    pops=[p for p in n.children('create_pop') if p.one('culture')=='south_german' and p.one('religion') is None and p.one('pop_type') is None]
    assert len(pops)==1;f=pops[0].children('size')[0];amount=int(f.value);assert amount>16000
    raw=core.edits(raw,[(f.start,f.end,'size = '+str(amount-16000))])
    files[p]=core.append(raw,'STATE_BAVARIA','SLZ','\n\t\t\tcreate_pop = { culture = south_german size = 16000 }\n').replace('\t\n\t\tregion_state:SLZ','\n\t\tregion_state:SLZ')
    files['common/country_definitions/1776_sc1_salzburg.txt']=defs
    files['common/history/countries/slz - sc1_salzburg.txt']=(ROOT/'common/history/countries/pas - map2w_r4.txt').read_text(encoding='utf-8-sig').replace('c:PAS','c:SLZ')
    files['common/history/characters/1776_sc1_salzburg.txt']='CHARACTERS = {\n c:SLZ ?= { create_character = { first_name = aor1776_slz_first last_name = aor1776_slz_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1732.5.31 interest_group = ig_devout ideology = ideology_reformer } }\n}\n'
    files['common/government_types/00_1776_sc1_salzburg.txt']='gov_aor1776_salzburg = { transfer_of_power = dictatorial male_ruler = "aor1776_slz_ruler" female_ruler = "aor1776_slz_ruler_female" possible = { c:SLZ ?= this has_law = law_type:law_theocracy } on_government_type_change = { change_to_dictatorial = yes } on_post_government_type_change = { post_change_to_dictatorial = yes } }\n'
    # An independent archiepiscopal court needs its own administration. This is
    # one explicit new level, not a confiscation of Bavaria's only written level.
    files['common/history/buildings/1776_sc1_salzburg.txt']='BUILDINGS = { s:STATE_BAVARIA = { region_state:SLZ = { create_building = { building = "building_government_administration" add_ownership = { country = { country = "c:SLZ" levels = 1 } } reserves = 1 activate_production_methods = { "pm_professional_bureaucrats" "pm_religious_bureaucrats" "pm_simple_organization" } } } } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_sc1_salzburg.txt']='aor1776_salzburg = { pattern = "pattern_vertical_split_01.tga" color1 = "yellow" color2 = "red" colored_emblem = { texture = "ce_lion_rampant.dds" color1 = "black" color2 = "red" instance = { scale = { 0.42 0.78 } position = { 0.25 0.5 } } } colored_emblem = { texture = "ce_solid.dds" color1 = "white" instance = { scale = { 0.5 0.2 } position = { 0.75 0.5 } } } }\n'
    files['common/flag_definitions/1776_sc1_salzburg.txt']='SLZ = { flag_definition = { coa = aor1776_salzburg priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french'
        pairs={'SLZ':'Salzbourg' if fr else 'Salzburg','SLZ_ADJ':'salzbourgeois' if fr else 'Salzburg',
            'aor1776_slz_first':'Hieronymus','aor1776_slz_last':'von Colloredo',
            'aor1776_slz_ruler':'Prince-archevêque' if fr else 'Prince-Archbishop',
            'aor1776_slz_ruler_female':'Princesse-archevêque' if fr else 'Princess-Archbishop',
            'gov_aor1776_salzburg':'Principauté archiépiscopale' if fr else 'Prince-Archbishopric',
            'gov_aor1776_salzburg_desc':('Le prince-archevêque gouverne les possessions temporelles de l’Église de Salzbourg. Le chapitre cathédral élit le prélat, qui exerce une autorité distincte de celle des princes voisins.' if fr else 'The prince-archbishop governs the temporal possessions of the Church of Salzburg. The cathedral chapter elects the prelate, whose authority is distinct from that of the neighbouring princes.')+chr(92)+'n'+chr(92)+'n$TRANSFER_OF_POWER_NAME_DESC$'}
        files[f'localization/{lang}/1776_sc1_salzburg_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    rel='docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json';originals[rel]=(ROOT/rel).read_text(encoding='utf-8-sig')
    assert load(ROOT/rel)==b['registry']
    # Select by identity, never by incidental lexical order in the region.
    ledger=sorted(b['registry']+[r for r in updated if r['rgb']=='xEDBB00'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[rel]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration)
    dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(target=16000,range=[15000,18000],source_city_1771=16066,rounding='Rounded estimate for residence nucleus, not full Erzstift',
        territory_1772_comparator_not_installed=177030,donor_before=amount,donor_after=amount-16000,method='Historical urban magnitude, not bitmap surface ratio',
        culture='south_german',religion='DEFAULT:south_german = catholic',minority_counts='Not independently quantified for this nucleus'))
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
        if rel not in originals:assert not (ROOT/rel).exists(), 'Collision '+rel
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    print('Prepared 12 cells, SLZ, 16000 people, one new administrative level; registry',len(ledger))

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');originals=load(OUT/'TEXT_BEFORE.json')
    current=prior.pas.prior.q.economy.runtime_hashes()
    changed=[p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p)]
    assert not changed, 'Review concurrent runtime changes: '+str(changed)
    assert sha(ROOT/'.git/index')==b['git_index_sha256']
    for rel,raw in files.items():
        p=ROOT/rel
        if rel in originals:assert p.read_text(encoding='utf-8-sig')==originals[rel]
        else:assert not p.exists()
    for rel,raw in files.items():
        p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
        bom=p.exists() and p.read_bytes().startswith(b'\xef\xbb\xbf')
        p.write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'))
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Installed scoped functional core; imperial integration next')

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT
    before=load(OUT/'COMPILER_BEFORE.json');assert not before['differences']
    files=compiler.compile_system();changed={}
    for rel,raw in files.items():
        if raw.lstrip('\ufeff')==before['actual'][rel]:continue
        p=ROOT/rel
        assert p.read_text(encoding='utf-8-sig')==before['actual'][rel], 'Concurrent imperial edit: '+rel
        changed[rel]=raw
    dump('IMPERIAL_EXPECTED.json',files)
    for rel,raw in changed.items():
        p=ROOT/rel;bom=p.read_bytes().startswith(b'\xef\xbb\xbf')
        p.write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'))
    dump('IMPERIAL_FILES.json',list(changed))
    print('Integrated membership/rights:',len(changed),'changed files,',len(files),'compiler contracts')

def journal():
    import render_map2k_imperial_map as render
    render.OUT=OUT;render.render()

def maps():
    b=load(OUT/'BASELINE.json');before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners['xEDBB00']='SLZ'
    colors={'BAV':'#e5d7af','AUS':'#abbfca','SLZ':'#c79c3c'}
    x0,y0,x1,y1=4379,917,4397,936;s=25;pw=510
    im=Image.new('RGB',(1530,655),'#faf8f1');d=ImageDraw.Draw(im)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    options=load(OUT/'CANDIDATES.json')['options']
    rivers=np.array(Image.open(ROOT/'map_data/rivers.png'))
    for k,(a,title) in enumerate([(before,'AVANT : noyau attribue a BAV'),(after,'INSTALLE B : residence SLZ, 12 cellules'),(before,'ECARTE C : extension et province entiere')]):
        ox=k*pw;d.text((ox+12,12),title,font=f,fill='#15313b')
        for y in range(y0,y1):
            for x in range(x0,x1):
                rgb='x'+format(int(a[y,x]),'06X');u=ox+45+(x-x0)*s;v=68+(y-y0)*s
                d.rectangle((u,v,u+s,v+s),fill=colors.get(owners.get(rgb),'#d7d4c9'),outline='#9d9989')
                if rivers[y,x]<=15:d.ellipse((u+9,v+9,u+15,v+15),fill='#1b78c7',outline='white')
        for x in range(x0,x1,2):d.text((ox+45+(x-x0)*s,47),str(x),font=small,fill='black')
        for y in range(y0,y1,2):d.text((ox+3,68+(y-y0)*s),str(y),font=small,fill='black')
        if k==2:
            for opt,col in [(options[2],'#a46ca3'),(options[1],'#ac2946')]:
                for x,y in opt['cells']:
                    u=ox+45+(x-x0)*s;v=68+(y-y0)*s
                    d.rectangle((u+3,v+3,u+s-3,v+s-3),outline=col,width=2)
            d.text((ox+10,565),'Rouge : 28 cellules, nouvelle poche BAV de 24.',font=small,fill='#a51c38')
            d.text((ox+10,588),'Violet : 65 cellules, juridictions distinctes confondues.',font=small,fill='#703b70')
        else:
            d.text((ox+10,565),'Ocre : SLZ / beige : BAV / bleu gris : AUS.',font=small,fill='black')
            d.text((ox+10,588),'Points bleus : rivieres natives, pas centres urbains.',font=small,fill='black')
    d.text((12,625),'B : noyau politique generalise de la residence, pas cadastre ni restitution complete. Berchtesgaden et peripheries non installes.',font=f,fill='#15313b')
    im.save(OUT/'BEFORE_AFTER.png')
    source=Image.open(OUT/'EVIDENCE/REILLY_1.jpg').convert('RGB')
    source.crop((740,300,1460,900)).save(OUT/'REILLY_RESIDENCE_DETAIL.png')
    print('Scoped before/after and source detail created')

def validate():
    import map2l_registry as reg
    from map2k_patch import ELECTORS
    from map_1776_audit import effective
    b=load(OUT/'BASELINE.json');inv=core.qa.inventory();checks=[]
    def ck(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail)
    counter=lambda rows:C.Counter({tuple(r['key']) if isinstance(r['key'],list) else r['key']:r['count'] for r in rows})
    before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy()
    geo=load(OUT/'GEOMETRY.json');migration=load(OUT/'REGISTRY_MIGRATION.json');files=load(OUT/'EXPECTED_TEXT.json')
    for r in geo['assignments']:
        mask=after==int(r['rgb'][1:],16)
        ck('Exact connected RGB '+r['rgb'],int(mask.sum())==r['pixels'] and len(core.components(mask))==1)
        for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
    ck('Global bitmap equals approved 12-cell change',np.array_equal(after,expected) and np.count_nonzero(before!=after)==12)
    ck('Only unsurveyed BAV parent subdivided',set(map(int,before[before!=after]))=={0x6EA29B})
    ck('No map-object locator moved',prior.pas.prior.q.r9.locators(before)==prior.pas.prior.q.r9.locators(after))
    eo=counter(b['inventory']['owners']);eo['xEDBB00','STATE_BAVARIA','SLZ']=1
    eg=dict(b['inventory']['geometry']);eg['xEDBB00']='STATE_BAVARIA'
    ec=reg.expected_country_definitions(b['inventory']['countries'],[migration])
    et=dict(b['inventory']['state_types']);et['STATE_BAVARIA|SLZ']='incorporated_default'
    for name,wanted in [('owners',eo),('geometry',eg),('countries',ec),('state_types',et)]:
        ck('Exact cumulative '+name,(counter(inv[name]) if name=='owners' else inv[name])==wanted)
    for key in ['pops','resolved_demographics','units','duplicates','errors']:
        ck('Global invariant '+key,inv[key]==b['inventory'][key])
    rp=counter(b['inventory']['regional_pop']);rp['STATE_BAVARIA','BAV','south_german','DEFAULT:south_german']-=16000
    rp['STATE_BAVARIA','SLZ','south_german','DEFAULT:south_german']=16000
    ck('Exact historically sized demographic transfer',counter(inv['regional_pop'])==rp)
    ck('Population source is urban, not entire territory',load(OUT/'DEMOGRAPHY.json')['target']==16000 and load(OUT/'DEMOGRAPHY.json')['source_city_1771']==16066)
    admin=core.region(files['common/history/buildings/1776_sc1_salzburg.txt'],'STATE_BAVARIA','SLZ').children('create_building')[0]
    eb=counter(b['inventory']['buildings']);eb['STATE_BAVARIA','SLZ',core.qa.signature(admin)]+=1
    ck('Existing buildings and owners unchanged; one explicit SLZ administration',counter(inv['buildings'])==eb)
    levels=counter(b['inventory']['building_levels_written']);levels['building_government_administration']+=1
    ck('Exactly one additional administrative level',counter(inv['building_levels_written'])==levels)
    ck('New court owned by SLZ',admin.children('add_ownership')[0].children('country')[0].one('country')=='"c:SLZ"')
    ck('No invented army or transferred recruitment',inv['units']==b['inventory']['units'] and not any(r['key'][0]=='SLZ' for r in inv['units']))
    donor_colors=[int(r['key'][0][1:],16) for r in inv['owners'] if r['key'][1:]==['STATE_BAVARIA','BAV']]
    ck('BAV has no new disconnected pocket',[len(c) for c in core.components(np.isin(after,donor_colors))]==[3362,5,3])
    for rel,old in load(OUT/'TEXT_BEFORE.json').items():
        new=(ROOT/rel).read_text(encoding='utf-8-sig')
        if rel=='common/history/states/00_states.txt':
            n=core.state(new,'STATE_BAVARIA');added=[n for n in n.children('create_state') if n.one('country')=='c:SLZ'];ck('Exactly one new owned state',len(added)==1)
            clean=core.edits(new,[(added[0].start,added[0].end,'')]);ck('All preexisting state histories preserved',core.qa.signature(core.cw.parse(clean)[0])==core.qa.signature(core.cw.parse(old)[0]))
        if rel=='map_data/state_regions/00_west_europe.txt':
            oldnodes=core.cw.parse(old);newnodes=core.cw.parse(new)
            for x,y in zip(oldnodes,newnodes):
                skip={'provinces'} if x.key=='STATE_BAVARIA' else set()
                ck('State ID/resources/hubs preserved '+x.key,[core.qa.signature(c) for c in x.children() if c.key not in skip]==[core.qa.signature(c) for c in y.children() if c.key not in skip])
    ledger=load(reg.active_registry_path());wanted=sorted(b['registry']+[r for r in migration['updated'] if r['rgb']=='xEDBB00'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    ck('Exact additive registry, 574 unique RGB',ledger==wanted and len(ledger)==len({r['rgb'] for r in ledger})==574)
    ck('Registry chain consumes exact preceding region',sorted(migration['previous'],key=lambda r:r['rgb'])==sorted([r for r in b['registry'] if r['state']=='STATE_BAVARIA'],key=lambda r:r['rgb']))
    ck('Physical imperial extent unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    ck('Strict cumulative manifest accepted',reg.approved_lot_dirs()[-1]==OUT)
    ck('SLZ member, no new elector or free city','SLZ' in reg.additional_members() and 'SLZ' not in reg.additional_free_cities() and 'SLZ' not in ELECTORS.values() and len(ELECTORS)==9)
    for rel,raw in files.items():ck('Scoped installed text '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    for rel,raw in load(OUT/'IMPERIAL_EXPECTED.json').items():ck('Cumulative imperial compiler '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    game=Path('C:/Games/Victoria 3/game');sets={}
    for folder in ['common/technology/technologies','common/laws','common/production_methods','common/ideologies']:
        sets[folder]={n.key for p in effective(ROOT,game,folder) for n in core.cw.parse(p.read_text(encoding='utf-8-sig'))}
    country=core.cw.parse(files['common/history/countries/slz - sc1_salzburg.txt'])[0].children()[0]
    ck('All starting laws exist',all(c.value.removeprefix('law_type:') in sets['common/laws'] for c in country.children('activate_law')))
    ck('All starting technologies exist',all(c.value in sets['common/technology/technologies'] for c in country.children('add_technology_researched')))
    ck('Administrative PMs exist',all(p in sets['common/production_methods'] for p in ['pm_professional_bureaucrats','pm_religious_bureaucrats','pm_simple_organization']))
    ck('Reformer ideology exists','ideology_reformer' in sets['common/ideologies'])
    ruler=core.cw.parse(files['common/history/characters/1776_sc1_salzburg.txt'])[0].children()[0].children('create_character')[0]
    ck('One historical ruler, correct birth and confession',ruler.one('birth_date')=='1732.5.31' and ruler.one('historical')=='yes' and ruler.one('religion')=='rel:catholic' and ruler.one('ruler')=='yes')
    ck('Capital refers to own incorporated residence state',('STATE_BAVARIA','SLZ') in map(tuple,inv['states']) and 'capital = STATE_BAVARIA' in files['common/country_definitions/1776_sc1_salzburg.txt'])
    for asset in ['patterns/pattern_vertical_split_01.tga','colored_emblems/ce_lion_rampant.dds','colored_emblems/ce_solid.dds']:ck('Native coat asset '+asset,(game/'gfx/coat_of_arms'/asset).exists())
    keysets=[]
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_sc1_salzburg_l_{lang}.yml';raw=p.read_text(encoding='utf-8-sig');ks=set(re.findall(r'^ ([A-Za-z0-9_]+):0 ',raw,re.M));keysets.append(ks)
        counts=C.Counter(k for fp in (ROOT/'localization'/lang).rglob('*.yml') for k in re.findall(r'^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s',fp.read_text(encoding='utf-8-sig'),re.M) if k in ks)
        ck('Eight unique localized keys '+lang,len(ks)==8 and all(counts[k]==1 for k in ks))
        ck('BOM/header/dynamic succession '+lang,p.read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':') and raw.count('$TRANSFER_OF_POWER_NAME_DESC$')==1 and chr(92)*2+'n' not in raw)
    ck('FR/EN localization parity',keysets[0]==keysets[1])
    for rel in files:
        if rel.endswith('.txt'):core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    ck('All installed scoped scripts parse',True)
    current=prior.pas.prior.q.economy.runtime_hashes()
    allowed=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    unexpected=sorted(set(changed)-allowed)
    dump('CONCURRENT_OBSERVATION.json',dict(unexpected_runtime_files=unexpected,not_restored=True))
    ck('All other runtime files byte-identical to immediate baseline',not unexpected,unexpected)
    tool_changes=[p for p,h in b['tools'].items() if sha(ROOT/p)!=h]
    ck('Prior tests/calibration/tools preserved',set(tool_changes)<={'tools/map2l_registry.py','tools/serg_closure_roadmap.py'},tool_changes)
    ck('HEAD/index/branch unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and sha(ROOT/'.git/index')==b['git_index_sha256'] and subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()==b['git_branch'])
    ck('No new duplicate RGB or invalid reference',inv['duplicates']==b['inventory']['duplicates'] and inv['errors']==b['inventory']['errors'])
    result=dict(task_ids=['SC1-SALZBURG'],status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(c['passed'] for c in checks) else 'STATIC_REVIEW_REQUIRED',
        passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,
        engine_executed=False,automated_engine_test=False,runtime_validation='PENDING_USER',world_before=sum(r['count'] for r in b['inventory']['pops']),world_after=sum(r['count'] for r in inv['pops']),
        inherited_duplicate_RGBs=len(inv['duplicates']),inherited_invalid_references=len(inv['errors']))
    dump('VALIDATION.json',result)
    dump('FILES_MODIFIED.json',dict(runtime_files=changed,sha256={p:current[p] for p in changed},tools=tool_changes+['tools/serg_sc1_salzburg.py','tools/test_serg_sc1_salzburg.py'],registry_sha256=sha(reg.active_registry_path())))
    print('Static validation',result['passed'],'/',result['total'],result['failed'])
    assert not result['failed']

def tests():
    import io, unittest
    names=['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01',
        'test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion',
        'test_map2w_r3_franconia','test_map2w_r3_calibration','test_map2w_r4_bavaria','test_map2w_r4_political',
        'test_map2w_r4bc','test_serg_closure_roadmap']
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    (OUT/'TESTS.log').write_text(stream.getvalue(),encoding='utf8')
    failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
    dump('TESTS.json',dict(total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,skipped=[str(t) for t,_ in result.skipped],engine_executed=False))
    print('Cumulative suite',result.testsRun,'failures',len(failures),'skipped',len(result.skipped))
    for f in failures:print(f['id'],f['traceback'][-1200:])

def scoped_tests():
    import io,unittest
    names=['test_serg_sc1_salzburg','test_serg_closure_roadmap']
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    (OUT/'SCOPED_TESTS.log').write_text(stream.getvalue(),encoding='utf8')
    failures=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors]
    data=dict(task_ids=['SC1-SALZBURG'],status='PASS' if not failures else 'FAIL',total=result.testsRun,passed=result.testsRun-len(failures)-len(result.skipped),failed=failures,
        skipped=[dict(id=t.id(),reason=reason) for t,reason in result.skipped],automated_engine_test=False)
    dump('SCOPED_TESTS.json',data)
    print('Scoped/roadmap tests:',data['passed'],'passed,',data['total'],'total,',len(result.skipped),'initial-only skipped')
    assert not failures

def update_tracking():
    import serg_closure_roadmap as rm
    p=rm.OUT/'ROADMAP_STATE.json';state=load(p);base=load(OUT/'BASELINE.json')['roadmap']
    assert state==base,'Concurrent tracker changes: merge explicitly before updating'
    v=load(OUT/'VALIDATION.json');assert v['passed']==v['total'] and not v['failed']
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    t=next(t for t in state['tasks'] if t['id']=='SC1-SALZBURG');assert t['status']=='NOT_STARTED'
    before=rm.progress(state)
    t.update(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        historical_sources=t['historical_sources']+[prefix+'SOURCES.md:1'],
        implementation_report=[prefix+'REPORT.md'],installed_lots=['SERG_CLOSURE/SC1-SALZBURG'],
        static_tests=dict(status='PASS',evidence=[prefix+'VALIDATION.json']),
        runtime_validation=dict(required=True,status='PENDING',attestation=None,scope='SC1-SALZBURG: SLZ residence nucleus, 12 cells xEDBB00, 16000 people, new court, imperial integration; new 1776 game, one month, save/reload',new_details_invented=False),
        decision=dict(classification='B_POLITICAL_APPROXIMATION',evidence=[prefix+'SOURCES.md',prefix+'GEOMETRY.json',prefix+'REPORT.md'],authority='Implementation authorized by current user request; agent selection documented, not a user runtime approval'),
        residual_uncertainty='Noyau de résidence B seulement; point/libellé de capitale et viabilité économique à inspecter en jeu. Berchtesgaden, Rupertiwinkel, Mühldorf, Pinzgau/Pongau/Lungau, possessions tyroliennes et autres périphéries non reconstitués; résidus BAV/AUS non certifiés. Démographie urbaine arrondie, minorités non quantifiées.',
        current_delivery_note='Noyau B SLZ installé (12 cellules, 16 000 habitants, Colloredo, administration et droits impériaux); contrôles statiques réussis. Validation joueur absente; zéro point acquis, périphéries non restituées.')
    state['mission_status']='SC1_SALZBURG_INSTALLED_PENDING_USER_VALIDATION'
    state['runtime_validation_hold']=dict(task_id='SC1-SALZBURG',protocol=prefix+'PLAYER_TEST_PROTOCOL.md',
        next_implementation_candidate='SC2-BOHEMIA',source=prefix+'AUTHORIZATION.md',reason='User explicitly requests pending runtime status and preparation without automatically starting another lot')
    after=rm.progress(state)
    assert (before['earned_weight'],before['total_weight'],before['percent'])==(after['earned_weight'],after['total_weight'],after['percent'])==(60,235,'25.53')
    state['events'].append(dict(id='SERG-RM-0003',date='2026-10-18',kind='SCOPED_IMPLEMENTATION',scope_version=state['scope_version'],source=prefix+'AUTHORIZATION.md',
        changes=[dict(task_id='SC1-SALZBURG',before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],before_percent=before['percent'],after_percent=after['percent'],
        before_weight=before['earned_weight'],after_weight=after['earned_weight'],total_weight=after['total_weight'],
        evidence=[prefix+'REPORT.md',prefix+'VALIDATION.json',prefix+'TESTS.json',prefix+'SCOPED_TESTS.json',prefix+'PLAYER_TEST_PROTOCOL.md'],
        note='Salzbourg : noyau B de résidence installé, 12 cellules BAV vers SLZ, 16 000 habitants transférés, Colloredo, un niveau administratif nouveau et intégration impériale. Registre 573→574, emprise physique inchangée. 209/209 contrôles statiques; suite historique 284 réussites/288, trois anciennes assertions de dernière couche et une exclusion initiale documentées; 12 contrats SC1 réussis. Aucun reçu humain ni opération Git d’écriture; socles et travaux concurrents conservés. Progression inchangée 60/235 = 25,53 %. Prochaine action : test joueur Salzbourg; SC2-BOHEMIA préparé, non commencé.'))
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(p,state);rm.render()

def tracker_check():
    import serg_closure_roadmap as rm
    result=rm.check();dump('TRACKER_VALIDATION.json',result)
    state=load(rm.OUT/'ROADMAP_STATE.json');b=load(OUT/'BASELINE.json')['roadmap']
    unchanged=[t for t in state['tasks'] if t['id']!='SC1-SALZBURG']==[t for t in b['tasks'] if t['id']!='SC1-SALZBURG']
    assert unchanged and state['events'][:-1]==b['events'] and state['source_manifest']==b['source_manifest']
    assert result['status']=='PASS' and result['progress']['percent']=='25.53' and result['progress']['next_task']=='SC1-SALZBURG'
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_identical=True,old_events_identical=True,old_source_manifest_identical=True,
        scoped_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',new_user_receipt=False,earned_weight=60,total_weight=235,before_percent='25.53',after_percent='25.53'))
    print('Tracker PASS: all other 80 tasks unchanged; 60/235; next action player Salzburg')

def repair_localization_escapes():
    files=load(OUT/'EXPECTED_TEXT.json')
    for rel,old in list(files.items()):
        if '1776_sc1_salzburg_l_' not in rel:continue
        p=ROOT/rel;raw=p.read_text(encoding='utf-8-sig');assert raw==old.lstrip('\ufeff')
        raw=raw.replace(chr(92)*2+'n',chr(92)+'n')
        p.write_text('\ufeff'+raw,encoding='utf8');files[rel]='\ufeff'+raw
    dump('EXPECTED_TEXT.json',files)
    print('Scoped FR/EN newline escape correction installed')

def review_tests():
    t=load(OUT/'TESTS.json')
    old={'test_map2w_r2b_completion.HesseNassauCompletion.test_registry_guard_accepts_current_layer',
         'test_map2w_r4_political.PassauPoliticalPilot.test_registry_current_layer',
         'test_map2w_r4bc.FreisingRegensburg.test_current_cumulative_tail_not_previous_last'}
    assert {f['id'] for f in t['failed']}==old
    scoped=load(OUT/'SCOPED_TESTS.json');assert not scoped['failed'] and scoped['passed']==39 and scoped['total']==40
    dump('TEST_REVIEW.json',dict(task_ids=['SC1-SALZBURG'],unexplained_failures=[],historical_final_layer_assertions=sorted(old),
        classification='SUPERSEDED_FINAL_LAYER_ASSERTION',raw_failure_logs_preserved=True,old_tests_not_modified=True,
        replacements=['test_serg_sc1_salzburg.SalzburgContracts.test_exact_cumulative_tail','VALIDATION.json: exact additive registry and old runtime conservation'],
        initial_only_skip='Initial no-edit check only; future authorized edits must not fail old snapshots',
        scoped_passed=39,scoped_total=40,scoped_failed=[],scoped_skipped=scoped['skipped'],engine_executed=False))
    print('Three legacy assertions reviewed; no unexplained failure; 39 current scoped/roadmap tests passed')

def delivery():
    import difflib,serg_closure_roadmap as rm
    v=load(OUT/'VALIDATION.json');assert v['passed']==v['total'] and not v['failed']
    assert rm.check()['status']=='PASS'
    originals=load(OUT/'TEXT_BEFORE.json');new_whitespace=[]
    for rel,old in originals.items():
        new=(ROOT/rel).read_text(encoding='utf-8-sig')
        delta=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=0))
        new_whitespace.extend(dict(path=rel,line=line[1:]) for line in delta if line.startswith('+') and not line.startswith('+++') and line[1:].rstrip()!=line[1:])
    dump('DIFF_CHECK.json',dict(new_trailing_whitespace=new_whitespace,
        baseline_pop_whitespace_lines=sum(line.rstrip()!=line for line in originals['common/history/pops/00_west_europe.txt'].splitlines()),
        final_pop_whitespace_lines=sum(line.rstrip()!=line for line in (ROOT/'common/history/pops/00_west_europe.txt').read_text(encoding='utf-8-sig').splitlines()),
        inherited_git_diff_check_note='Older modified population sections retain their original whitespace; no broad cleanup of concurrent work',
        git_writes=False))
    assert not new_whitespace
    modified=load(OUT/'FILES_MODIFIED.json');paths=modified['runtime_files']+modified['tools']
    state=load(rm.OUT/'ROADMAP_STATE.json');b=load(OUT/'BASELINE.json')
    assert sha(ROOT/'.git/index')==b['git_index_sha256']
    paths += [str((rm.OUT/name).relative_to(ROOT).as_posix()) for name in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json']]
    dump('DELIVERY_MANIFEST.json',dict(task_ids=['SC1-SALZBURG'],date='2026-10-18',status='READY_FOR_SCOPED_RUNTIME_VALIDATION',
        before_percent='25.53',after_percent='25.53',earned_weight=60,total_weight=235,sha256={p:sha(ROOT/p) for p in paths},
        git_head=b['git_head'],git_branch=b['git_branch'],git_index_sha256=b['git_index_sha256'],git_writes=False,
        runtime_user_validation=False,next_action='PLAYER_TEST_SC1_SALZBURG',next_implementation_candidate='SC2-BOHEMIA',candidate_started=False,
        validation=dict(passed=v['passed'],total=v['total']),scoped_tests=load(OUT/'SCOPED_TESTS.json'),test_review='TEST_REVIEW.json'))
    print('Delivery complete:',len(modified['runtime_files']),'functional files, 209/209 checks, no new whitespace, Git unchanged')

if __name__=='__main__': globals()[sys.argv[1]]()
