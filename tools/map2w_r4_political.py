"""Passau political pilot; option 1 is installed, archived candidates are not current state."""
import collections as C
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2w_r2b_completion as prior

ROOT=Path(__file__).resolve().parents[1]
R4=ROOT/'docs/reports/map/MAP2W/R4'
OUT=R4/'POLITICAL_REPRESENTATION/PASSAU'
BOX=(4385,880,4420,916)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def snapshot():
    assert not (OUT/'BASELINE.json').exists(),'Never overwrite capture'
    inv=prior.core.qa.inventory();h=prior.q.economy.runtime_hashes()
    dump('BASELINE.json',dict(inventory=inv,hashes=h,registry_sha256=sha(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),registry_tool_sha256=sha(ROOT/'tools/map2l_registry.py'),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=sha(ROOT/'.git/index'),source_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in [R4/'EVIDENCE/BSB_1791_READING.jpg',R4/'EVIDENCE/PASSAU_HLB_BOUNDARIES.jpg',R4/'EVIDENCE/PASSAU_HLB.html',R4/'CALIBRATION.json',R4/'GEOGRAPHIC_ASSESSMENT.json']}))
    print('Fresh political baseline, world',sum(r['count'] for r in inv['pops']),flush=True)
def packed():return prior.core.packed(ROOT/'map_data/provinces.png')
def native():
    b=load(OUT/'BASELINE.json');assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    a=packed();rivers=np.array(Image.open(ROOT/'map_data/rivers.png'));x0,y0,x1,y1=BOX;s=25
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};values,counts=np.unique(a[y0:y1,x0:x1],return_counts=True)
    rows=[]
    for v,c in zip(values,counts):
        rgb='x'+format(int(v),'06X');full=a==v;parts=prior.core.components(full);ys,xs=np.where(full)
        rows.append(dict(rgb=rgb,state=owners.get(rgb,[None,None])[0],owner=owners.get(rgb,[None,None])[1],window_cells=int(c),all_cells=int(full.sum()),components=[len(p) for p in parts],bbox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
    dump('NATIVE_RGB_INVENTORY.json',dict(box=BOX,provinces=rows,warning='Window inventory, not a transfer of all these RGBs'))
    im=Image.new('RGB',((x1-x0)*s+315,(y1-y0)*s+95),'#faf9f4');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',10)
    d.text((20,10),'Passau — bitmap actif, coordonnées X/Y (0 en haut à gauche)',font=font,fill='black')
    arr=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'))[y0:y1,x0:x1];im.paste(Image.fromarray(arr).resize(((x1-x0)*s,(y1-y0)*s),Image.Resampling.NEAREST),(50,60));d=ImageDraw.Draw(im)
    for y in range(y0,y1):
        for x in range(x0,x1):
            u=50+(x-x0)*s;v=60+(y-y0)*s;d.rectangle((u,v,u+s,v+s),outline='#777777',width=1)
            if 3<=rivers[y,x]<=15 or rivers[y,x] in [0,1,2]:d.rectangle((u+7,v+7,u+s-7,v+s-7),fill='#2d88db',outline='white')
    for x in range(x0,x1):d.text((50+(x-x0)*s,42),str(x),font=small,fill='black')
    for y in range(y0,y1):d.text((9,64+(y-y0)*s),str(y),font=font,fill='black')
    for k,r in enumerate(rows):
        col=tuple(int(r['rgb'][i:i+2],16) for i in [1,3,5]);u=(x1-x0)*s+70;v=65+k*54;d.rectangle((u,v,u+18,v+18),fill=col,outline='black');d.text((u+23,v),r['rgb']+' / '+str(r['owner']),font=font,fill='black');d.text((u+23,v+21),str(r['window_cells'])+' cellules dans la fenêtre',font=small,fill='black')
    d.text((60,(y1-y0)*s+68),'Carrés bleus : rivières natives ; couleurs : RGB actuels. Aucune hypothèse installée.',font=font,fill='black');im.save(OUT/'NATIVE_GRID_RGB.png')
    print(json.dumps(rows,ensure_ascii=False),flush=True)

def source_preview():
    im=Image.open(R4/'EVIDENCE/BSB_1791_READING.jpg').convert('RGB');box=(1220,400,2100,1485);crop=im.crop(box);d=ImageDraw.Draw(crop);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for x in range(1250,2100,50):d.line((x-box[0],0,x-box[0],crop.height),fill='#537fab');d.text((x-box[0]+1,1),str(x),font=f,fill='#154b89',stroke_width=1,stroke_fill='white')
    for y in range(400,1485,50):d.line((0,y-box[1],crop.width,y-box[1]),fill='#537fab');d.text((1,y-box[1]+1),str(y),font=f,fill='#154b89',stroke_width=1,stroke_fill='white')
    crop.save(OUT/'PASSAU_SOURCE_GRID.png')

def candidates():
    b=load(OUT/'BASELINE.json');assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    a=packed();doc=load(OUT/'POLITICAL_CHOICES.json');own={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};x0,y0,x1,y1=BOX
    ys,xs=np.mgrid[y0:y1,x0:x1];xs=xs.ravel();ys=ys.ravel();points=np.column_stack([xs+.5,ys+.5]);out=[]
    all_values,all_counts=np.unique(a,return_counts=True);counts={int(v):int(c) for v,c in zip(all_values,all_counts)}
    donor_rgb=[int(r['key'][0][1:],16) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_BAVARIA','BAV']]
    donor_cells=sum(counts.get(v,0) for v in donor_rgb)
    donor_mask=np.isin(a,donor_rgb);donor_components=[len(p) for p in prior.core.components(donor_mask)]
    donor_pops=[r for r in b['inventory']['regional_pop'] if r['key'][:2]==['STATE_BAVARIA','BAV']]
    for spec in doc['options']:
        hit=prior.core.inside(points,spec['polygon_native']) if spec['polygon_native'] else np.zeros(len(points),bool);cells=[];excluded=[]
        for x,y in zip(xs[hit],ys[hit]):
            rgb='x'+format(int(a[y,x]),'06X');region,owner=own[rgb];why=None
            for ex in doc['common_exclusions']:
                xx0,yy0,xx1,yy1=ex['native_box']
                if xx0<=x<xx1 and yy0<=y<yy1:why=ex['id']
            if rgb not in spec['allowed_parents']:why='UNREVIEWED_PARENT_OR_NEIGHBOUR'
            if why:excluded.append(dict(cell=[int(x),int(y)],parent_rgb=rgb,current_owner=owner,reason=why));continue
            assert region=='STATE_BAVARIA' and owner=='BAV' and not rgb.startswith('xED')
            cells.append(dict(x=int(x),y=int(y),parent_rgb=rgb,state=region,State_ID=71,owner_before=owner,owner_proposed='PAS',classification=spec['class'],installed=False))
        mask=np.zeros(a.shape,bool)
        for r in cells:mask[r['y'],r['x']]=True
        components=[len(p) for p in prior.core.components(mask)];parent_rows=[]
        for parent in sorted({r['parent_rgb'] for r in cells}):
            pmask=a==int(parent[1:],16);rem=pmask&~mask
            parent_rows.append(dict(parent_rgb=parent,total_parent_cells=int(pmask.sum()),proposed_transfer=sum(r['parent_rgb']==parent for r in cells),remaining_original_owner_cells=int(rem.sum()),remaining_components=[len(p) for p in prior.core.components(rem)],candidate_components=[len(p) for p in prior.core.components(pmask&mask)]))
        allocation=[]
        for p in donor_pops:
            count=p['count'];n=len(cells);moved=(count*n+donor_cells//2)//donor_cells
            allocation.append(dict(profile=p['key'][2:],before_BAV=count,proposed_PAS=moved,remaining_BAV=count-moved,historical_census=False))
        remaining_country_parts=prior.core.components(donor_mask&~mask)
        out.append(dict(id=spec['id'],name=spec['name_fr'],classification=spec['class'],installed=False,cell_count=len(cells),cells=cells,components=components,parent_rows=parent_rows,excluded_by_screen=excluded,donor_region='STATE_BAVARIA',donor_tag='BAV',donor_region_cell_count=donor_cells,donor_state_components_before=donor_components,donor_state_components_after=[len(p) for p in remaining_country_parts],small_donor_fragments_after=[dict(cells=[[int(x),int(y)] for y,x in p],size=len(p)) for p in remaining_country_parts if len(p)<40],population_allocation_preview=allocation,proposed_population=sum(p['proposed_PAS'] for p in allocation),actual_population_transferred=0,buildings_moved=0,units_moved=0,new_active_RGBs=0))
    dump('CANDIDATES.json',dict(status='MAP2W_R4_AWAITING_PLAYER_CARTOGRAPHIC_DECISION',options=out,installed_transfers=[],new_active_countries=[],geographic_precision_claim=False))
    for r in out:print(r['id'],r['cell_count'],'cells',r['components'],'population preview',r['proposed_population'],'parents',r['parent_rows'],flush=True)

def maps():
    a=prior.core.packed(ROOT/load(OUT/'PREPARE_CONTEXT.json')['bitmap_backup']) if (OUT/'PREPARE_CONTEXT.json').exists() else packed();b=load(OUT/'BASELINE.json');doc=load(OUT/'POLITICAL_CHOICES.json');g=load(OUT/'CANDIDATES.json');rivers=np.array(Image.open(ROOT/'map_data/rivers.png'))
    owners={int(r['key'][0][1:],16):(r['key'][1],r['key'][2]) for r in b['inventory']['owners']};x0,y0,x1,y1=BOX;s=17
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11);title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',20)
    panel_w=650;panel_h=780;canvas=Image.new('RGB',(panel_w*3,875),'#faf9f5');d=ImageDraw.Draw(canvas)
    common=set((r['x'],r['y']) for r in g['options'][0]['cells']);options=[]
    for k,opt in enumerate(g['options']):
        panel=Image.new('RGB',(panel_w,panel_h),'#faf9f5');pd=ImageDraw.Draw(panel);top=85;left=43;cells={(r['x'],r['y']) for r in opt['cells']}
        pd.text((20,12),['1 — RETENUE / INSTALLÉE (B)','2 — ÉCARTÉE (C)','3 — Référence sans transfert'][k],font=title,fill='#173143');pd.text((20,42),[f"{len(cells)} cellules installées — test moteur à faire",f"{len(cells)} cellules envisagées — aucune appliquée",'Carte antérieure — option non retenue'][k],font=f,fill='#a44725')
        for y in range(y0,y1):
            for x in range(x0,x1):
                state,owner=owners[int(a[y,x])];color=(227,217,177) if owner=='BAV' else (212,209,226) if state=='STATE_BOHEMIA' else (207,218,221)
                if (x,y) in cells:color=(63,153,199) if (x,y) in common else (229,160,64)
                u=left+(x-x0)*s;v=top+(y-y0)*s;pd.rectangle((u,v,u+s,v+s),fill=color,outline='#b0ada5',width=1)
                if (x,y) not in cells and int(a[y,x])!=int(a[y,x-1]):pd.line((u,v,u,v+s),fill='#6e6654',width=2)
                if int(a[y,x])!=int(a[y-1,x]):pd.line((u,v,u+s,v),fill='#6e6654',width=2)
                if 3<=rivers[y,x]<=15 or rivers[y,x] in [0,1,2]:pd.ellipse((u+5,v+5,u+s-5,v+s-5),fill='#2372ce',outline='white')
        for x in range(x0,x1):
            if x%2==0:pd.text((left+(x-x0)*s-5,top-18),str(x),font=small,fill='black')
        for y in range(y0,y1):
            if y%2==0:pd.text((3,top+(y-y0)*s+2),str(y),font=small,fill='black')
        def xy(x,y):return (left+(x-x0)*s,top+(y-y0)*s)
        for ex in doc['common_exclusions']:
            xx0,yy0,xx1,yy1=ex['native_box'];xx0=max(xx0,x0);yy0=max(yy0,y0);xx1=min(xx1,x1);yy1=min(yy1,y1)
            if xx0>=xx1 or yy0>=yy1:continue
            u,v=xy(xx0,yy0);uu,vv=xy(xx1,yy1);pd.rectangle((u,v,uu,vv),outline='#b12e3a',width=2)
            for yy in range(int(v),int(vv),8):pd.line((u,yy,min(u+15,uu),min(yy+15,vv)),fill='#b12e3a',width=1)
        # Geographic labels describe relations/sectors; no exact town dots.
        for text,x,y in [('BOHÊME / AUS',4406,882),('BAVIÈRE',4386,886),('Abteiland nord',4400,890),('Hals : exclusion',4386,897),('Passau : confluent',4401,904),('AUTRICHE',4408,911)]:
            u,v=xy(x,y);pd.text((u,v),text,font=small,fill='#363126',stroke_width=1,stroke_fill='white')
        u,v=xy(4400.5,902.5);pd.ellipse((u-5,v-5,u+5,v+5),outline='#9a2632',width=2)
        pd.text((20,top+(y1-y0)*s+15),'Parent proposé : xB08021, BAV, État 71',font=f,fill='black')
        pd.text((20,top+(y1-y0)*s+39),['212 cellules du parent restent BAV','Aurait laissé 169 cellules et des fragments BAV','252 cellules avant la sélection'][k],font=f,fill='black')
        canvas.paste(panel,(k*panel_w,0));options.append(panel)
    d=ImageDraw.Draw(canvas)
    d.text((20,790),'Bleu : noyau 1 installé | Orange : extension 2 écartée | Beige : BAV résiduel dans chaque hypothèse | Gris/violet : AUS conservé',font=f,fill='#222222')
    d.text((20,818),'Rouge hachuré : secteurs exclus / indécidables, PAS limites exactes. Points bleus : rivières natives.',font=f,fill='#222222')
    d.text((20,846),'Seule la solution 1 est installée. Formes politiques schématiques : aucune précision cadastrale ni position urbaine exacte certifiée.',font=f,fill='#222222')
    canvas.save(OUT/'OPTIONS_COMPARISON.png')
    for k,p in enumerate(options[:2]):p.save(OUT/f'OPTION_{k+1}_GRID.png')
    # Historical annotation is on the source sheet, NOT falsely registered onto
    # the game. Arrows identify jurisdictions and the scope of the alternatives.
    source=Image.open(R4/'EVIDENCE/BSB_1791_READING.jpg').convert('RGB').crop((1220,400,2100,1485));dest=Image.new('RGB',(1350,1180),'#faf9f5');dest.paste(source,(15,40));dd=ImageDraw.Draw(dest)
    dd.text((15,10),'Passau — relations politiques attestées, feuille de 1791 contrôlée par la chronologie R4',font=title,fill='#173143')
    annotations=[('Bohême : hors propositions',(1910,470)),('Wolfstein / Freyung : option 2',(1800,850)),('Bavière à l’ouest : conservée',(1500,900)),('Abteiland méridional : option 1',(1810,1170)),('Hals : souveraineté bavaroise',(1655,1260)),('Passau, siège du prince-évêque',(1695,1340)),('Rentamt séparé : exclu ici',(1470,1340)),('Autriche à l’est : conservée',(2010,1110))]
    for k,(text,(sx,sy)) in enumerate(annotations):
        v=90+k*110;u=930;px=15+sx-1220;py=40+sy-400;dd.text((u,v),text,font=f,fill='#173143');dd.line((u-10,v+9,px,py),fill='#173143',width=2);dd.ellipse((px-4,py-4,px+4,py+4),fill='#173143')
    dd.text((930,1000),'Flèches = secteurs de lecture.',font=f,fill='#333333');dd.text((930,1025),'Aucun calage du scan sur le jeu.',font=f,fill='#333333');dd.text((15,1140),'1782 : Obernberg/Vichtenstein cédés après la date de départ ; non reconstitués automatiquement depuis cette feuille.',font=f,fill='#333333');dest.save(OUT/'HISTORICAL_JURISDICTIONS.png')
    print('Political overlays generated without editing runtime bitmap',flush=True)

def compiler_before():
    import map2k_imperial_system as compiler
    files=compiler.compile_system();checks=[]
    for rel,raw in files.items():checks.append(dict(path=rel,passed=(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff')))
    dump('COMPILER_BEFORE.json',dict(passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks));print('Compiler baseline',sum(r['passed'] for r in checks),'/',len(checks),flush=True)
    assert all(r['passed'] for r in checks)

def prepare_installation():
    """Prepare only the politically reviewed 40-cell minimal core."""
    import re
    core=prior.core;b=load(OUT/'BASELINE.json');candidate=load(OUT/'CANDIDATES.json')['options'][0]
    assert candidate['id']=='OPTION_1_MINIMAL' and candidate['cell_count']==40 and candidate['components']==[40]
    assert candidate['donor_state_components_before']==[3444,5,3] and candidate['donor_state_components_after']==[3404,5,3]
    assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    assert 'PAS' not in b['inventory']['countries']
    backup=prior.OUT/'provinces_candidate.png';assert sha(backup)==b['hashes']['map_data/provinces.png']
    before=core.packed(backup);after=before.copy();new='xEDBA00';parent='xB08021';sid='STATE_BAVARIA'
    assert int(new[1:],16) not in np.unique(before) and new not in b['inventory']['geometry']
    for r in candidate['cells']:
        assert int(before[r['y'],r['x']])==int(parent[1:],16);after[r['y'],r['x']]=int(new[1:],16)
    rows=[]
    for rgb,tag in [(parent,'BAV'),(new,'PAS')]:
        yy,xx=np.where(after==int(rgb[1:],16));assert len(core.components(after==int(rgb[1:],16)))==1
        rows.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner='BAV',owner=tag,pixels=len(xx),cells=[[int(x),int(y)] for x,y in zip(xx,yy)],confidence='B_POLITICAL_APPROXIMATION' if tag=='PAS' else 'C_RETAINED_NOT_CERTIFIED'))
    geo=dict(parents=[parent],assignments=rows,new_provinces=[dict(rgb=new,parent_rgb=parent)],new_members=['PAS'],free_cities=[],hub_rebindings=[],classification='B_POLITICAL_APPROXIMATION',selected_option='OPTION_1_MINIMAL',historical_cadastral_precision=False)
    dump('GEOMETRY.json',geo)
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    files={};originals={}
    rel='common/history/states/00_states.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert sha(ROOT/rel)==b['hashes'][rel];originals[rel]=raw
    n=core.state(raw,sid);text='\n create_state = { country = c:PAS owned_provinces = { '+new+' } }\n';files[rel]=core.edits(raw,[(n.end-1,n.end-1,text)])
    rel='map_data/state_regions/00_west_europe.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert sha(ROOT/rel)==b['hashes'][rel];originals[rel]=raw
    n=next(n for n in core.cw.parse(raw) if n.key==sid);ops=[];bindings=[]
    for name in ['provinces','prime_land']:
        for f in n.children(name):
            old=core.values(n,name);updated=[]
            for rgb in old:updated.extend([parent,new]) if rgb==parent else updated.append(rgb)
            if updated!=old:
                ops.append((f.start,f.end,name+' = { '+' '.join('"'+v+'"' for v in updated)+' }'))
                if name=='prime_land':bindings.append(dict(state=sid,field=name,before=old,after=updated))
    # Existing hub pixels are physically outside this core; do not move them.
    hubs=[r for r in prior.q.r9.locators(before) if r['ID']==71]
    assert all(before[int(r['Y']),int(r['X'])]==after[int(r['Y']),int(r['X'])] for r in hubs)
    files[rel]=core.edits(raw,sorted(ops))
    rel='common/history/pops/00_west_europe.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert sha(ROOT/rel)==b['hashes'][rel];originals[rel]=raw
    n=core.region(raw,sid,'BAV');weights={'BAV':candidate['donor_region_cell_count']-40,'PAS':40};ops=[];moved=[];alloc=[]
    for pop in n.children('create_pop'):
        f=pop.children('size')[0];amounts=core.allocate(int(f.value),weights);ops.append((f.start,f.end,'size = '+str(amounts['BAV'])))
        if amounts['PAS']:
            piece=raw[pop.start:pop.end];moved.append(core.edits(piece,[(f.start-pop.start,f.end-pop.start,'size = '+str(amounts['PAS']))]))
        alloc.append(dict(state=sid,source='BAV',culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:'+pop.one('culture')),before=int(f.value),after=amounts))
    files[rel]=core.append(core.edits(raw,sorted(ops)),sid,'PAS','\n'.join(moved))
    dump('ALLOCATION.json',dict(weights=weights,profiles=alloc,method='TECHNICAL_PROFILE_CONSERVATION_NOT_CENSUS',historical_population=None,buildings='All existing BAV levels/PM/investors retained at surviving subdivision',units='All formations and recruitment unchanged',PAS_population=sum(r['after']['PAS'] for r in alloc)))
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert sha(ROOT/rel)==b['hashes'][rel];originals[rel]=raw
    tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)};files[rel]=raw.rstrip()+'\n'+new+'="'+tm[parent.upper()]+'"\n'
    defs='PAS = { color = { 181 73 67 } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = STATE_BAVARIA }\n'
    files['common/country_definitions/1776_map2w_r4_passau.txt']=defs
    source='common/history/countries/eic - franconian estate.txt';assert sha(ROOT/source)==b['hashes'][source]
    files['common/history/countries/pas - map2w_r4.txt']=(ROOT/source).read_text(encoding='utf-8-sig').replace('c:EIC','c:PAS')
    files['common/history/characters/pas - map2w_r4.txt']='CHARACTERS = { c:PAS ?= { create_character = { first_name = aor1776_pas_first last_name = aor1776_pas_last historical = yes culture = south_german religion = rel:catholic ruler = yes age = 67 interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    files['common/government_types/00_1776_map2w_r4_passau.txt']='gov_aor1776_passau = { transfer_of_power = dictatorial male_ruler = "RULER_TITLE_PRINCE_BISHOP" female_ruler = "RULER_TITLE_PRINCE_BISHOP" possible = { c:PAS ?= this has_law = law_type:law_theocracy } on_government_type_change = { change_to_dictatorial = yes } on_post_government_type_change = { post_change_to_dictatorial = yes } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2w_r4_passau.txt']='aor1776_passau = { pattern = "pattern_solid.tga" color1 = "white" textured_emblem = { texture = "te_aor1776_passau.dds" instance = { scale = { 0.8 0.8 } position = { 0.5 0.5 } } } }\n'
    files['common/flag_definitions/1776_map2w_r4_passau.txt']='PAS = { flag_definition = { coa = aor1776_passau priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french';desc=('Le prince-évêque exerce l’autorité temporelle sur les terres de Passau. Le chapitre cathédral élit le titulaire de cette principauté ecclésiastique de l’Empire.' if fr else 'The prince-bishop exercises temporal authority over the lands of Passau. The cathedral chapter elects the ruler of this ecclesiastical principality of the Empire.')+'\\n\\n$TRANSFER_OF_POWER_NAME_DESC$'
        pairs={'PAS':'Passau','PAS_ADJ':'passavien' if fr else 'Passau','aor1776_pas_first':'Leopold Ernst','aor1776_pas_last':'von Firmian','gov_aor1776_passau':'Principauté épiscopale de Passau' if fr else 'Prince-Bishopric of Passau','gov_aor1776_passau_desc':desc}
        files[f'localization/{lang}/1776_map2w_r4_passau_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    previous=[r for r in b['registry'] if r['state']==sid];updated=[r for r in previous if r['rgb']!=parent]+[dict(rgb=r['rgb'],state=sid,beneficiary=r['owner'],basis='MAP2W-R4 Passau: minimal political representation B, NOT cadastral; deferred peripheral jurisdictions; see MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/REPORT.md') for r in rows]
    ledger=sorted([r for r in b['registry'] if r['state']!=sid]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files['docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json']=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    migration=dict(replaced_regions=[sid],previous=previous,updated=updated,new_members=['PAS'],free_cities=[],new_provinces=geo['new_provinces'],geometry='MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[],country_additions={n.key:core.qa.signature(n) for n in core.cw.parse(defs)})
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files);dump('PREPARE_CONTEXT.json',dict(bitmap_backup=backup.relative_to(ROOT).as_posix(),selected_cells=candidate['cells'],hubs=hubs));core.OUT=OUT;core.emit(files,'HISTORY.patch')
    print('Prepared minimal core: 40 cells, xEDBA00, PAS; population',sum(r['after']['PAS'] for r in alloc),'imperial RGB',len(ledger),flush=True)

def install_bitmap():
    b=load(OUT/'BASELINE.json');assert sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    for rel,raw in load(OUT/'EXPECTED_TEXT.json').items():assert (ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'),rel
    (ROOT/'map_data/provinces.png').write_bytes((OUT/'provinces_candidate.png').read_bytes())
    from build_saint_gobain_icon import dds_bytes
    emblem=Image.open(OUT/'PASSAU_FLAG_EMBLEM.png').convert('RGBA');p=ROOT/'gfx/coat_of_arms/textured_emblems/te_aor1776_passau.dds';assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(dds_bytes(emblem))
    print('Installed exact 40-cell bitmap and vector-derived flag DDS',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files);prior.core.OUT=OUT
    patches=[]
    for i,(rel,raw) in enumerate(files.items()):
        if (ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'):continue
        name=f'IMPERIAL_{i}.patch';prior.core.emit({rel:raw},name);patches.append(name)
    dump('IMPERIAL_PATCHES.json',patches);print('Imperial changed files',len(patches),'/',len(files),flush=True)

def journal():
    import render_map2k_imperial_map as render
    render.OUT=OUT;render.render()

def delivery():
    """Export current delivery evidence, without editing game files."""
    b=load(OUT/'BASELINE.json');g=load(OUT/'GEOMETRY.json');v=load(OUT/'VALIDATION.json');t=load(OUT/'TESTS.json')
    assert v['passed']==v['total'] and t['passed']
    before=prior.core.packed(ROOT/load(OUT/'PREPARE_CONTEXT.json')['bitmap_backup']);after=packed()
    x0,y0,x1,y1=BOX;s=19;w=(x1-x0)*s;h=(y1-y0)*s
    canvas=Image.new('RGB',(2*w+90,h+145),'#faf9f5');d=ImageDraw.Draw(canvas)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for k,(a,label) in enumerate([(before,'AVANT — xB08021 : 252 cellules BAV'),(after,'APRÈS — 40 PAS / 212 BAV')]):
        rgb=np.stack([(a>>16)&255,(a>>8)&255,a&255],axis=-1).astype('uint8')[y0:y1,x0:x1]
        left=30+k*(w+30);canvas.paste(Image.fromarray(rgb).resize((w,h),Image.Resampling.NEAREST),(left,50));d=ImageDraw.Draw(canvas)
        d.text((left,15),label,font=f,fill='#173143')
        for x in range(x1-x0+1):d.line((left+x*s,50,left+x*s,50+h),fill='#535353')
        for y in range(y1-y0+1):d.line((left,50+y*s,left+w,50+y*s),fill='#535353')
        d.text((left,65+h),f'Fenêtre X [{x0},{x1}[ ; Y [{y0},{y1}[ — couleurs RGB réelles',font=f,fill='black')
    d.text((30,h+110),'Seuls 40 pixels du bitmap changent. Abstraction politique B ; pas de frontière cadastrale certifiée.',font=f,fill='black');canvas.save(OUT/'BEFORE_AFTER.png')
    dump('DECISION.json',dict(status=v['status'],date='2026-10-18',selected='OPTION_1_MINIMAL',classification='B_POLITICAL_APPROXIMATION',reason='Documented southern temporal core; existing physical junction and historical neighbours; single connected PAS and retained BAV parent. Precise boundaries not demonstrated.',rejected_option_2='83 cells would generate a 52-cell Bavarian island and three new one-cell Bavarian islands, without historical support. No transfer installed.',no_arbitration_required='Only option 1 remains defensible after topology and political review; option 2 is not a competing accepted attribution.',installed_cells=40,new_RGB='xEDBA00',parent_RGB='xB08021',State_ID=71,owner_before='BAV',owner_after='PAS',population=14267,population_is_historical_census=False,tests=t['run'],checks=v['total'],runtime_test='NOT_EXECUTED',pending_sectors='NEXT_SECTORS.md',geodetic_precision_claim=False))
    changed=[r for r in g['assignments'] if r['owner']!=r['previous_owner']]
    dump('TERRITORIAL_CHANGES.json',dict(classification='B',changes=changed,unchanged_parent=[r for r in g['assignments'] if r['owner']==r['previous_owner']],not_complete_Hochstift=True))
    rows=['# Transferts installés — Passau (B)','',
          '| RGB parent | RGB installé | State_ID / région | Avant | Après | Cellules |',
          '| --- | --- | --- | --- | --- | ---: |',
          '| xB08021 | xEDBA00 | 71 / STATE_BAVARIA | BAV | PAS | 40 |','',
          'Le parent conserve 212 cellules BAV. Souveraineté temporelle attestée ; contour schématique non cadastral. Exclusions : UNRESOLVED.md. Coordonnées bitmap, origine en haut à gauche, X vers la droite et Y vers le bas.','',
          '| X | Y | Avant | Après | Classe |','| ---: | ---: | --- | --- | --- |']
    rows += [f'| {x} | {y} | BAV / xB08021 | PAS / xEDBA00 | B |' for r in changed for x,y in sorted(r['cells'],key=lambda p:(p[1],p[0]))]
    (OUT/'TERRITORIAL_CHANGES.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
    files=load(OUT/'FILES_MODIFIED.json');paths=set(files['runtime_files']+files['tools']+files['workshop_generated'])
    paths|={p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'}
    paths|={'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json','docs/reports/map/MAP2W/REPORT.md','docs/reports/map/MAP2W/R4/REPORT.md'}
    dump('DELIVERY_MANIFEST.json',dict(files=[dict(path=p,sha256=sha(ROOT/p),bytes=(ROOT/p).stat().st_size) for p in sorted(paths)],git_head_unchanged=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'],git_index_unchanged=sha(ROOT/'.git/index')==b['git_index_sha256'],engine_executed=False))
    print('Passau delivery evidence exported',flush=True)

def validate_installation():
    import re
    import map2l_registry as reg
    from map2k_patch import ELECTORS
    core=prior.core;b=load(OUT/'BASELINE.json');g=load(OUT/'GEOMETRY.json');m=load(OUT/'REGISTRY_MIGRATION.json');inv=core.qa.inventory();checks=[]
    def check(name,value,detail=None):
        checks.append(dict(name=name,passed=bool(value),detail=detail))
        if not value:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/load(OUT/'PREPARE_CONTEXT.json')['bitmap_backup']);after=packed();expected=before.copy()
    for row in g['assignments']:
        for x,y in row['cells']:expected[y,x]=int(row['rgb'][1:],16)
        check('One connected assigned RGB '+row['rgb'],len(core.components(after==int(row['rgb'][1:],16)))==1 and int(np.count_nonzero(after==int(row['rgb'][1:],16)))==row['pixels'])
    check('Exact full bitmap: only 40 selected cells change',np.array_equal(expected,after) and int(np.count_nonzero(before!=after))==40)
    eo=counter(b['inventory']['owners']);eo['xEDBA00','STATE_BAVARIA','PAS']=1;check('Exact unique owners, no unowned or multiply owned new province',counter(inv['owners'])==eo)
    eg=dict(b['inventory']['geometry']);eg['xEDBA00']='STATE_BAVARIA';check('Exact economic-region mapping',inv['geometry']==eg)
    ec=dict(b['inventory']['countries']);ec.update(m['country_additions']);check('Only PAS country added; old definitions unchanged',inv['countries']==ec)
    et=dict(b['inventory']['state_types']);et['STATE_BAVARIA|PAS']='incorporated_default';check('Only new PAS subdivision',inv['state_types']==et)
    check('New RGB was unused',not np.any(before==0xEDBA00))
    for key in ['pops','resolved_demographics','buildings','building_levels_written','units','duplicates','errors']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    ep=counter(b['inventory']['regional_pop']);alloc=load(OUT/'ALLOCATION.json')
    for r in alloc['profiles']:
        ep[r['state'],r['source'],r['culture'],r['religion']]-=r['before']
        for tag,n in r['after'].items():ep[r['state'],tag,r['culture'],r['religion']]+=n
        check('Conserved integer profile '+r['culture']+'/'+r['religion'],sum(r['after'].values())==r['before'] and all(isinstance(n,int) and n>=0 for n in r['after'].values()))
    check('Exact regional population transfers',counter(inv['regional_pop'])==ep)
    check('World 835801255 unchanged',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in b['inventory']['pops'])==835801255)
    check('PAS 14267 conserved people, not invented census',sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='PAS')==alloc['PAS_population']==14267)
    for rel,old in load(OUT/'TEXT_BEFORE.json').items():
        if '/history/' in rel:
            raw=(ROOT/rel).read_text(encoding='utf-8-sig');nodes=lambda s:{n.key:core.qa.signature(n) for n in core.cw.walk(core.cw.parse(s)) if n.key.startswith('s:STATE_') and n.key!='s:STATE_BAVARIA'}
            check('All other state histories preserved '+rel,nodes(old)==nodes(raw))
        if rel.startswith('map_data/state_regions/'):
            oldnodes={n.key:n for n in core.cw.parse(old)};newnodes={n.key:n for n in core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))}
            for sid,n in oldnodes.items():
                exclude={'provinces'} if sid=='STATE_BAVARIA' else set();check('ID/resources/hubs/traits retained '+sid,[core.qa.signature(c) for c in n.children() if c.key not in exclude]==[core.qa.signature(c) for c in newnodes[sid].children() if c.key not in exclude])
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    check('New terrain inherits parent once',tm['XEDBA00']==tm['XB08021'] and len(re.findall(r'(?im)^\s*xEDBA00\s*=',terrain))==1)
    registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json');check('568 unique imperial RGBs',len(registry)==len({r['rgb'] for r in registry})==568)
    wanted=sorted([r for r in b['registry'] if r['state']!='STATE_BAVARIA']+m['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    check('Exact registry migration',registry==wanted)
    check('Imperial physical extent unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in registry])))
    check('Narrow migration guard last, no R3 reinstated',reg.approved_lot_dirs()[-1]==OUT and R4.parent/'R3' not in reg.approved_lot_dirs())
    check('One new member, nine electors unchanged',m['new_members']==['PAS'] and len(ELECTORS)==9 and 'PAS' not in ELECTORS.values() and not m['free_cities'])
    for rel,raw in load(OUT/'EXPECTED_TEXT.json').items():
        check('Reviewed scoped text '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
        if rel.endswith('.txt'):core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    compiled=load(OUT/'IMPERIAL_EXPECTED.json')
    for rel,raw in compiled.items():check('Cumulative compiler '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    country=core.cw.parse((ROOT/'common/history/countries/pas - map2w_r4.txt').read_text())[0].children()[0]
    techs=set();laws=set()
    for folder in [ROOT/'common/technology/technologies',Path('C:/Games/Victoria 3/game/common/technology/technologies')]:
        for p in folder.glob('*.txt'):techs.update(n.key for n in core.cw.parse(p.read_text(encoding='utf-8-sig')))
    for folder in [ROOT/'common/laws',Path('C:/Games/Victoria 3/game/common/laws')]:
        for p in folder.glob('*.txt'):laws.update(n.key for n in core.cw.parse(p.read_text(encoding='utf-8-sig')))
    check('All starting technologies exist',all(n.value in techs for n in country.children('add_technology_researched')))
    check('All starting laws exist',all(n.value.removeprefix('law_type:') in laws for n in country.children('activate_law')))
    check('Theocracy and hereditary bureaucracy initialized','law_type:law_theocracy' in [n.value for n in country.children('activate_law')] and 'law_type:law_hereditary_bureaucrats' in [n.value for n in country.children('activate_law')])
    keys=[]
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_map2w_r4_passau_l_{lang}.yml';raw=p.read_text(encoding='utf-8-sig');ks=set(re.findall(r'^\s*([A-Za-z0-9_.-]+):0',raw,re.M));keys.append(ks)
        check('Localization BOM/header '+lang,p.read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':'))
        counts=C.Counter(k for fp in (ROOT/'localization'/lang).rglob('*.yml') for k in re.findall(r'^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s',fp.read_text(encoding='utf-8-sig'),re.M) if k in ks)
        check('Six new keys unique '+lang,len(ks)==6 and all(counts[k]==1 for k in ks))
        check('Dynamic succession retained '+lang,'$TRANSFER_OF_POWER_NAME_DESC$' in raw)
    check('FR/EN key sets identical',keys[0]==keys[1])
    flag=ROOT/'gfx/coat_of_arms/textured_emblems/te_aor1776_passau.dds';check('DDS flag readable and colour-correct',np.array_equal(np.array(Image.open(flag).convert('RGBA')),np.array(Image.open(OUT/'PASSAU_FLAG_EMBLEM.png').convert('RGBA'))))
    current=prior.q.economy.runtime_hashes();ours=set(load(OUT/'EXPECTED_TEXT.json'))|{p for p,r in compiled.items() if current.get(p)!=b['hashes'].get(p)}|{'map_data/provinces.png',flag.relative_to(ROOT).as_posix(),'gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));other=sorted(set(changed)-ours)
    dump('CONCURRENT_OBSERVATION.json',dict(files=[dict(path=p,before=b['hashes'].get(p),after=current.get(p)) for p in other],not_written_by_MAP=True))
    check('No unexpected runtime write outside MAP scope',not other,other)
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('All original source evidence and diagnostic profiles preserved',all(sha(ROOT/p)==s for p,s in b['source_hashes'].items()))
    check('44 old duplicate RGBs and 12 invalid references, no new ones',len(inv['duplicates'])==44 and len(inv['errors'])==12 and inv['duplicates']==b['inventory']['duplicates'] and inv['errors']==b['inventory']['errors'])
    result=dict(status='MAP2W_R4_READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2W_R4_STATIC_REVIEW_REQUIRED',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,classification='B_POLITICAL_APPROXIMATION',selected_option='OPTION_1_MINIMAL',installed_cells=40,new_RGBs=['xEDBA00'],new_countries=['PAS'],world_before=835801255,world_after=sum(r['count'] for r in inv['pops']),PAS_population=14267,registered_RGBs=len(registry),preexisting_duplicate_RGBs=44,preexisting_invalid_references=inv['errors'],new_errors=[e for e in inv['errors'] if e not in b['inventory']['errors']],engine_test_executed=False,manual_validation_status='NOT_TESTED_NEW_PASSAU_CORE',geodetic_precision_claim=False)
    dump('VALIDATION.json',result);dump('POPULATION_VALIDATION.json',dict(world_before=835801255,world_after=result['world_after'],transferred_from_BAV_to_PAS=14267,profiles=alloc['profiles'],profiles_conserved=counter(inv['pops'])==counter(b['inventory']['pops']),buildings_and_owners_conserved=inv['buildings']==b['inventory']['buildings'],units_conserved=inv['units']==b['inventory']['units'],historical_census=False))
    dump('FILES_MODIFIED.json',dict(runtime_files=sorted(p for p in changed if p in ours),concurrent_files=other,tools=['tools/map2w_r4_political.py','tools/map2w_r4_passau_flag.mjs','tools/test_map2w_r4_political.py','tools/map2l_registry.py','tools/test_map2w_r2b_completion.py'],workshop_generated=['workshop_assets/source/map2k_hre_registered_map.png']))
    print('Installed Passau validation',result['passed'],'/',result['total'],result['status'],flush=True);assert all(r['passed'] for r in checks)

def tests():
    import io,unittest
    modules=['test_map2w_r4_political','test_map2w_r4_bavaria','test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration']
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
    dump('TESTS.json',dict(run=result.testsRun,passed=result.wasSuccessful(),failures=[dict(test=str(t),traceback=s) for t,s in result.failures],errors=[dict(test=str(t),traceback=s) for t,s in result.errors],output=stream.getvalue(),engine_execution=False,modules=modules));print(stream.getvalue(),flush=True);assert result.wasSuccessful()

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
