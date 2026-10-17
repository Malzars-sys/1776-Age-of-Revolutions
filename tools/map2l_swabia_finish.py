"""Bounded final Swabian jurisdictions; immutable prior-lot baseline."""
import json,sys,csv,re
from PIL import Image,ImageDraw,ImageFont
import map2l_swabia_continuation as previous
import map2l_mainz as core
import map2l_minden_ravensberg as parts
import numpy as np

OUT=core.ROOT/'docs/reports/map/MAP2L/SWABIA_FINISH'
core.OUT=OUT
core.BACKUP=previous.OUT/'provinces_candidate.png'
core.REGIONS={'STATE_BADEN','STATE_WURTTEMBERG','STATE_BAVARIA'}
if hasattr(core,'PREPARE_EXTRA_FILES'):del core.PREPARE_EXTRA_FILES
parts.OUT=OUT
TAGS=['SLM','SWW','SWF','SWX','SWY','SKC']

def configure():
    inherited=json.loads((previous.OUT/'TRACING.json').read_text())['calibrated_sources'][0]
    # Cross-map town correspondences, not surveyed ground control. Keep the
    # previous game's correspondence instead of silently shifting old cores.
    pairs=[('Konstanz',[2890,5280],[1655,2235]),('Ravensburg',[3560,4990],[1990,2080]),('Salem',[2930,5010],[1655,2045]),('Waldsee',[3790,4660],[2050,1820]),('Leutkirch',[4300,4700],[2415,2030])]
    source=np.array([s for _,s,_ in pairs]);target=np.array([[*h,1] for _,_,h in pairs])@np.array(inherited['matrix'])
    matrix=np.linalg.lstsq(np.column_stack((source,np.ones(len(source)))),target,rcond=None)[0]
    controls=[dict(name=n,source=s,game=g.tolist(),role='FIT',basis='Approximate cross-map town, NOT surveyed bitmap ground control') for (n,s,_),g in zip(pairs,target)]
    residuals=np.linalg.norm(np.column_stack((source,np.ones(len(source))))@matrix-target,axis=1)
    core.dump('ATLAS_CORRESPONDENCE.json',dict(pairs=pairs,matrix=matrix.tolist(),cross_map_fit_residual_px=residuals.tolist(),physical_accuracy_certified=False,warning='Fit residuals are NOT independent geographic position errors; retained source uncertainty remains.'))
    poly=[
        dict(owner='SLM',territory='Salem: conservative Salmannsweiler temporal mainland, excluding Heiligenberg and Meersburg',points=[[2925,4960],[3005,4965],[3020,5035],[3090,5060],[3080,5100],[3040,5130],[2990,5120],[2945,5070],[2910,5040],[2900,5000]]),
        dict(owner='SWW',territory='Waldburg-Wolfegg-Waldsee: Waldsee branch mainland, Austrian landvogtei and town enclaves excluded',points=[[3770,4560],[3860,4530],[3910,4600],[3890,4680],[3900,4735],[3790,4740],[3780,4700],[3735,4670],[3745,4610]]),
        dict(owner='SWF',territory='Waldburg-Wolfegg-Wolfegg: Wolfegg mainland, not reunited with Waldsee until 1798',points=[[3790,4800],[3860,4770],[3930,4800],[3990,4780],[4050,4810],[4030,4880],[4080,4890],[4040,5010],[3990,5030],[3975,5050],[3915,5030],[3880,5070],[3840,5000],[3790,4960],[3800,4900]]),
        dict(owner='SWX',territory='Waldburg-Zeil-Wurzach: Wurzach mainland excluding Zeil and Austrian lands',points=[[4020,4520],[4110,4490],[4200,4500],[4290,4550],[4290,4650],[4230,4680],[4200,4720],[4100,4710],[4050,4650],[4020,4620]]),
        dict(owner='SWY',territory='Waldburg-Zeil-Trauchburg: conservative Zeil mainland; Trauchburg succession 1772, external fringes deferred',points=[[4150,4770],[4210,4700],[4280,4700],[4320,4740],[4320,4800],[4250,4840],[4180,4830],[4150,4810]]),
        dict(owner='SKC',territory='Prince-bishopric of Constance: Meersburg temporal office K11, not Austrian Constance city nor diocese',points=[[3005,5160],[3070,5165],[3095,5220],[3100,5255],[3065,5270],[3000,5225],[2980,5205]]),
        dict(owner='SKC',territory='Prince-bishopric of Constance: Markdorf temporal office K10 conservative core',points=[[3160,5095],[3225,5100],[3250,5130],[3260,5180],[3220,5210],[3165,5180],[3150,5140]])]
    # Discover all intersected provisional old-country parents; never target
    # the exact protected RGBs of earlier restored estates.
    from map2l_belgium import packed
    from map2l_franconia import inside
    b=json.loads((OUT/'BASELINE.json').read_text());bmp=packed(core.ROOT/b['bitmap_backup']);parents=set();findings=[]
    for p in poly:
        found=[]
        for row in b['inventory']['owners']:
            rgb,sid,owner=row['key']
            if sid not in core.REGIONS or owner not in {'BAD','WUR','BAV'}:continue
            ys,xs=np.where(bmp==int(rgb[1:],16));local=(np.column_stack((xs,ys))+.5-matrix[2])@np.linalg.inv(matrix[:2]);count=int(inside(local,p['points']).sum())
            if count:found.append(rgb);parents.add(rgb);findings.append(dict(territory=p['territory'],parent=rgb,state=sid,before=owner,after=p['owner'],cells=count))
        p.update(source='AT',parents=found)
    core.dump('CANDIDATE_INTERSECTIONS.json',findings)
    core.dump('TRACING.json',dict(historical_date='1776-01-01',method='Conservative atlas jurisdiction envelopes, corroborated by primary 1765 Salem perimeter; approximate correspondence inherited without moving restored cores',calibrated_sources=[dict(key='AT',path='EVIDENCE/HABW_06_13.jpg',matrix=matrix.tolist(),controls=controls)],parents=sorted(parents),rgb_start=0xEDAF00,native_anchors='NATIVE_ANCHORS.json',hub_rebinding_parents=[],preview_box=[4285,909,4340,938],polygons=poly,limitations=['1790 atlas not automatically equivalent to 1776: only established branch cores traced; 1785 Friedberg-Scheer sale and 1798 Wolfegg reunion explicitly excluded.','Cross-map fit is not independent physical calibration. Broad conservative envelopes at game scale, not cadastral tracing.','All restored prior owner cores are excluded by country, only provisional BAD/WUR/BAV fringes may change.','No enlargement of subpixel cities; Montbeliard, Weingarten and complex outlying domains remain open. No Erfurt edits.']))
    cfg=json.loads((OUT/'TRACING.json').read_text());cfg['hub_rebinding_parents']=['xDBB84C'];core.dump('TRACING.json',cfg)
    print(json.dumps(findings,ensure_ascii=False));print('Cross-map fit residuals only',residuals.tolist())

def extra_files(files,migration):
    import validate_diplomacy_ottoman_1776 as parser
    b=json.loads((OUT/'BASELINE.json').read_text());assert not set(TAGS)&set(b['inventory']['countries'])
    defs=''.join(tag+' = { color = { '+color+' } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = '+sid+' }\n' for tag,color,sid in [('SLM','108 155 186','STATE_BADEN'),('SWW','211 162 71','STATE_WURTTEMBERG'),('SWF','182 119 64','STATE_WURTTEMBERG'),('SWX','197 160 103','STATE_WURTTEMBERG'),('SWY','199 123 84','STATE_WURTTEMBERG'),('SKC','127 133 200','STATE_BADEN')])
    geometry=json.loads((OUT/'GEOMETRY.json').read_text())
    for tag in TAGS:assert any(r['owner']==tag for r in geometry['assignments']),'Empty estate '+tag
    files['common/country_definitions/1776_map2l_swabia_finish.txt']=defs
    replacement={'law_aor1776_imperial_customs':'law_aor1776_swabia_finish_customs','law_aor1776_imperial_no_slavery':'law_aor1776_swabia_finish_free_status'}
    source=(core.ROOT/'common/laws/1776_map2l_franconian_start_variants.txt').read_text(encoding='utf-8-sig');laws=[]
    for node in parser.parse(source):
        if node.key not in replacement:continue
        text=source[node.start:node.end]
        for old,new in replacement.items():text=text.replace(old,new)
        text=re.sub(r'OR = \{ c:ANS \?= this c:FBM \?= this c:WZB \?= this c:NUR \?= this c:EIC \?= this \}', 'OR = { '+' '.join('c:'+t+' ?= this' for t in TAGS)+' }',text);laws.append(text)
    files['common/laws/1776_map2l_swabia_finish.txt']='\n'.join(laws)+'\n'
    for tag in TAGS:
        base='FBM' if tag in {'SLM','SKC'} else 'ANS'
        text=(core.ROOT/f'common/history/countries/{base.lower()} - franconian estate.txt').read_text(encoding='utf-8-sig').replace('c:'+base,'c:'+tag)
        for old,new in replacement.items():text=text.replace(old,new)
        files[f'common/history/countries/{tag.lower()} - swabia finish.txt']=text
    files['common/history/characters/1776_map2l_swabia_finish.txt']='CHARACTERS = { c:SLM ?= { create_character = { first_name = aor1776_slm_first last_name = aor1776_slm_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1713.1.9 interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    governments=''
    for tag in TAGS:
        power='dictatorial' if tag in {'SLM','SKC'} else 'hereditary';law='law_theocracy' if tag in {'SLM','SKC'} else 'law_monarchy'
        title='RULER_TITLE_PRINCE_BISHOP' if tag=='SKC' else 'aor1776_salem_abbot_title' if tag=='SLM' else 'aor1776_waldburg_count_title';female=title if tag in {'SLM','SKC'} else 'aor1776_waldburg_countess_title'
        governments+='gov_aor1776_'+tag.lower()+' = { transfer_of_power = '+power+' male_ruler = "'+title+'" female_ruler = "'+female+'" possible = { c:'+tag+' ?= this has_law = law_type:'+law+' } on_government_type_change = { change_to_'+power+' = yes } on_post_government_type_change = { post_change_to_'+power+' = yes } }\n'
    files['common/government_types/00_1776_map2l_swabia_finish.txt']=governments
    coas='';flags=''
    for tag in TAGS:
        coas+='AOR1776_'+tag+' = { pattern = "pattern_solid.tga" color1 = '+('blue' if tag=='SLM' else 'yellow')+' colored_emblem = { texture = "'+('ce_cross_couped.dds' if tag=='SLM' else 'ce_eagle.dds')+'" color1 = '+('white' if tag=='SLM' else 'black')+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
        flags+=tag+' = { flag_definition = { coa = AOR1776_'+tag+' priority = 100 allow_overlord_canton = no } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_swabia_finish.txt']=coas;files['common/flag_definitions/1776_map2l_swabia_finish.txt']=flags
    names={'SLM':('Imperial Abbey of Salem','Abbaye impériale de Salem'),'SWW':('County of Waldburg-Wolfegg-Waldsee','Comté de Waldburg-Wolfegg-Waldsee'),'SWF':('County of Waldburg-Wolfegg-Wolfegg','Comté de Waldburg-Wolfegg-Wolfegg'),'SWX':('County of Waldburg-Zeil-Wurzach','Comté de Waldburg-Zeil-Wurzach'),'SWY':('County of Waldburg-Zeil-Trauchburg','Comté de Waldburg-Zeil-Trauchburg'),'aor1776_slm_first':('Anselm','Anselme'),'aor1776_slm_last':('Schwab','Schwab'),'aor1776_salem_abbot_title':('Imperial Abbot','Abbé impérial'),'aor1776_waldburg_count_title':('Count','Comte'),'aor1776_waldburg_countess_title':('Countess','Comtesse')}
    for tag in TAGS:
        names[tag+'_ADJ']=('Salemian','Salémien') if tag=='SLM' else ('Waldburgian','Waldbourgeois')
        names['gov_aor1776_'+tag.lower()]=('Imperial abbey','Abbaye impériale') if tag=='SLM' else ('Imperial county','Comté impérial')
        names['gov_aor1776_'+tag.lower()+'_desc']=('The imperial abbot governs the temporal lands of Salem, distinct from the diocese of Constance.','L’abbé impérial gouverne les terres temporelles de Salem, distinctes du diocèse de Constance.') if tag=='SLM' else ('This branch of the House of Waldburg governs its own county. In 1776 the branches are separate and have not yet received their later princely titles.','Cette branche de la maison de Waldburg gouverne son propre comté. En 1776, les branches sont distinctes et ne portent pas encore leurs titres princiers ultérieurs.')
    names['SKC']=('Prince-Bishopric of Constance','Principauté épiscopale de Constance')
    files['common/history/characters/1776_map2l_swabia_finish.txt']=files['common/history/characters/1776_map2l_swabia_finish.txt'].rstrip()[:-1]+' c:SKC ?= { create_character = { first_name = aor1776_skc_first last_name = aor1776_skc_last historical = yes culture = south_german religion = rel:catholic ruler = yes age = 58 interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    names['aor1776_skc_first']=('Maximilian Christoph','Maximilien-Christophe')
    names['aor1776_skc_last']=('von Rodt','de Rodt')
    names['SKC_ADJ']=('Constantian','Constantien')
    names['gov_aor1776_skc']=('Prince-bishopric','Principauté épiscopale')
    names['gov_aor1776_skc_desc']=('The prince-bishop governs the temporal offices of Meersburg and Markdorf. Austrian Constance and the spiritual diocese are distinct jurisdictions.','Le prince-évêque gouverne les domaines temporels de Meersburg et Markdorf. La ville autrichienne de Constance et le diocèse spirituel constituent des juridictions distinctes.')
    for law in replacement.values():names[law]=('Imperial estate start','Départ d’État impérial');names[law+'_desc']=('1776 legal variant; no later technologies granted.','Variante juridique de 1776 ; aucune technologie ultérieure accordée.')
    for lang,i in [('english',0),('french',1)]:files[f'localization/{lang}/1776_map2l_swabia_finish_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+key+':0 "'+values[i]+'"\n' for key,values in names.items())
    migration.update(new_members=TAGS,free_cities=[],country_additions={n.key:core.qa.signature(n) for n in parser.parse(defs)})
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

core.PREPARE_EXTRA_FILES=extra_files

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for source,name,box,step in [('EVIDENCE/HABW_06_13.jpg','LAKE',(2700,4550,4750,5700),100),('EVIDENCE/HABW_06_13.jpg','LEGEND',(70,5700,4950,6770),200),('EVIDENCE/SALEM_1765.jpg','SALEM',(0,0,3250,2594),200)]:
        image=Image.open(OUT/source).convert('RGB').crop(box);d=ImageDraw.Draw(image)
        for x in range((box[0]//step+1)*step,box[2],step):
            d.line((x-box[0],0,x-box[0],image.height),fill='blue');d.text((x-box[0]+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//step+1)*step,box[3],step):
            d.line((0,y-box[1],image.width,y-box[1]),fill='blue');d.text((0,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        image.save(OUT/(name+'_READING.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:core.dump('NATIVE_ANCHORS.json',[r for r in csv.DictReader(f) if r['State_ID'] in core.REGIONS])
    from pypdf import PdfReader
    pdf=PdfReader(OUT/'EVIDENCE/HABW_6_13.pdf')
    print('Atlas PDF',len(pdf.pages),'pages')
    for i,page in enumerate(pdf.pages):
        text=page.extract_text()
        if any(term in text.lower() for term in ['waldburg','weingarten','salmanns','mömpelgard','montbéliard']):
            print('PAGE',i+1)
            for line in text.splitlines():
                if any(term in line.lower() for term in ['waldburg','weingarten','salmanns','mömpelgard','montbéliard','1785','1772']):print(line)

def sources():
    from map2l_belgium import sha
    data={
        'atlas':dict(file='EVIDENCE/HABW_06_13.jpg',date='Historical territorial snapshot 1790; scholarly publication 1987',url='https://www.leo-bw.de/media/kgl_atlas/current/delivered/bilder/HABW_06_13.jpg',catalogue='https://www.lgl-bw.de/Produkte/Karten/Historische-Karten/Historischer-Atlas-von-Baden-Wuerttemberg/index.html',title='Herrschaftsgebiete und Ämtergliederung in Südwestdeutschland 1790',authors='Gerd Friedrich Nüske and Joseph Kerkhoff, after Helmut Kluge; Kommission für geschichtliche Landeskunde and Landesvermessungsamt',use='Bounded named temporal jurisdiction cores only; not automatic backprojection of 1790 ownership into 1776.'),
        'salem':dict(file='EVIDENCE/SALEM_1765.jpg',date='1765',url='https://upload.wikimedia.org/wikipedia/commons/2/27/Salem_Mappa_1765.jpg',catalogue='https://www.schule-bw.de/faecher-und-schularten/gesellschaftswissenschaftliche-und-philosophische-faecher/geschichte/unterrichtsmaterialien/sekundarstufe-I/mittelalter/salem/politik.html',title='Geometrische Mappa: Salem high-jurisdiction boundary stones 1–129',use='Primary corroboration of Salmannsweiler temporal perimeter; not spiritual diocesan border.',license='Public domain historic map'),
        'montbeliard':dict(file='EVIDENCE/FALLOT_MONTBELIARD_1750.jpg',date='1750',catalogue='https://catalogue.bnf.fr/ark:/12148/cb406304901',title='Carte géographique de la Principauté de Montbélliard et dépendances',author='Joseph-Frédéric Fallot; BnF GE C-1623, ark btv1b53027864j',use='Preserved targeted evidence only. NO transfer: patrimonial ownership versus French sovereignty and bitmap alignment remain unresolved.',license='Public domain historic map'),
        'chronology':[
            'https://www.gemeinde-waldburg.de/gaeste/die-waldburg/geschichte',
            'https://www.leo-bw.de/fr/detail-gis/-/Detail/details/ORT/labw_ortslexikon/20306/Waldburg%2BRV',
            'https://www.koeblergerhard.de/ZIER-HP/ZIER-HP-06-2016/AAAKoeblerGerhardWaldburginderdeutschenLandesgeschichte20161116%20-%20123.htm',
            'https://www.salem.de/wissenswert-amuesant/persoenlichkeiten/anselm-ii-schwab/',
            'https://erdteilallegorien.univie.ac.at/personen/anselm-ii-schwab',
            'https://www.rosgartenmuseum.de/%EF%BB%BFkonstanzer-kostbarkeiten-maximilian-christoph-von-rodt-1717-1800/',
            'https://archivesdiplomatiques.diplomatie.gouv.fr/ark%3A/14366/ghrpcz4xsdb7'
        ]}
    for key in ['atlas','salem','montbeliard']:
        data[key]['sha256']=sha(OUT/data[key]['file']);data[key]['dimensions']=list(Image.open(OUT/data[key]['file']).size)
    core.dump('SOURCES.json',data)

def preview(bmp,rows,name):
    # Route prior renderer to this lot, never overwrite prior-lot previews.
    original=previous.OUT
    try:previous.OUT=OUT;previous.preview(bmp,rows,name)
    finally:previous.OUT=original
    from PIL import ImageColor
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),225,dtype=np.uint8)
    colors={'BAD':'#dec459','WUR':'#72a46b','AUS':'#b3a6d8','BAV':'#79afeb','SFU':'#ee9269','SEW':'#887ac4','SAG':'#d88892','SKE':'#a284b9','SLM':'#6c9bba','SWW':'#d3a247','SWF':'#b67740','SWX':'#c5a067','SWY':'#c77b54','SKC':'#7f85c8','SUU':'#e6dec4','HSG':'#6babb5'}
    for row in rows:arr[local==int(row['key'][0][1:],16)]=ImageColor.getrgb(colors.get(row['key'][2],'#ddd'))
    edge=np.zeros(local.shape,dtype=bool);edge[1:]|=local[1:]!=local[:-1];edge[:,1:]|=local[:,1:]!=local[:,:-1];arr[edge]=55
    im=Image.fromarray(arr).resize((local.shape[1]*20,local.shape[0]*20),Image.Resampling.NEAREST);canvas=Image.new('RGB',(im.width,im.height+100),'white');canvas.paste(im);d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    d.text((8,im.height+5),name+' | Swabia 1776: conservative jurisdiction cores, not a cadastre',fill='black',font=font)
    for i,tag in enumerate(['SLM','SWW','SWF','SWX','SWY','SKC']):
        xx=8+(i%3)*360;yy=im.height+32+(i//3)*27;d.rectangle((xx,yy,xx+15,yy+15),fill=colors[tag]);d.text((xx+20,yy),tag+' '+{'SLM':'Salem','SWW':'Waldburg-Waldsee','SWF':'Waldburg-Wolfegg','SWX':'Waldburg-Wurzach','SWY':'Waldburg-Zeil','SKC':'Constance: Markdorf'}[tag],fill='black',font=font)
    canvas.save(OUT/(name+'.png'))

core.preview=preview

def finish_whitespace():
    original=previous.OUT
    try:previous.OUT=OUT;previous.finish_whitespace()
    finally:previous.OUT=original

def compact_diagnostics():
    # These two PNGs are generated reading copies, never authoritative sources,
    # immutable baselines, province bitmaps, or files supplied by the player.
    for name in ['AT_OVERLAY','SALEM_READING']:
        source=OUT/(name+'.png');target=OUT/(name+'.jpg')
        if source.exists():
            assert source.resolve().parent==OUT.resolve()
            image=Image.open(source).convert('RGB');image.save(target,quality=92)
            assert Image.open(target).size==image.size
            print('Verified compact diagnostic',name,source.stat().st_size,'->',target.stat().st_size,'bytes; original PNG retained until explicit cleanup')

def summary():
    from map2l_belgium import sha
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION','SWABIA','SWABIA_CONTINUATION','SWABIA_FINISH']
    allowed={'No commit or staging mutation','HEAD and Git index unchanged','Git HEAD and index unchanged'};rows=[]
    for name in names:
        report=json.loads((OUT.parent/name/'VALIDATION.json').read_text());failed=[r['name'] for r in report['checks'] if not r['passed']];rows.append(dict(lot=name,raw_status=report['status'],passed=sum(r['passed'] for r in report['checks']),checks=len(report['checks']),failed=failed,data_checks_passed=not(set(failed)-allowed),manual_runtime_status=report.get('runtime_status','NOT_YET_TESTED'),automatic_engine_test=False))
    b=json.loads((OUT/'BASELINE.json').read_text());import subprocess
    head=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=core.ROOT,text=True).strip();index=sha(core.ROOT/'.git/index');main=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text());ok=all(r['data_checks_passed'] for r in rows) and head==b['git_head'] and index==b['git_index_sha256'] and all(r['passed'] for r in main['checks'])
    core.dump('NON_REGRESSION.json',dict(status='PASS_STATIC_WITH_AUTHORIZED_HISTORICAL_GIT_DIFFERENCE' if ok else 'FAIL',suites=rows,HEAD=head,index_sha256=index,git_unchanged=head==b['git_head'] and index==b['git_index_sha256'],old_raw_git_failures_retained=True,automatic_engine_testing=False,new_sublot_runtime_status='NOT_YET_TESTED',bitmap_sha256=sha(core.ROOT/'map_data/provinces.png'),registry_sha256=sha(core.active_registry_path()),main_map_checks=sum(r['passed'] for r in main['checks'])))
    g=json.loads((OUT/'GEOMETRY.json').read_text());cfg=json.loads((OUT/'TRACING.json').read_text());records=[]
    for r in g['assignments']:
        row={k:r[k] for k in ['rgb','parent_rgb','state','previous_owner','owner','pixels']};z=r['source_zone'];row.update(territory=cfg['polygons'][z-1]['territory'] if z else 'Retained provisional fringe',historical_date='1776-01-01',approximation='Conservative game-scale jurisdiction core, not a cadastre' if z else 'Old attribution retained; not new historical certification');records.append(row)
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    report=json.loads((OUT/'VALIDATION.json').read_text());report.update(runtime_status='NOT_YET_TESTED',territorial_completion='CORE_CORRECTIONS_APPLIED_REMAINING_JURISDICTIONS_OPEN',inherited_duplicate_RGB_count=len(report['inherited_duplicate_RGBs']),inherited_reference_error_count=len(report['inherited_reference_errors']),checkpoint='No new checkpoint, commit or push authorized for this lot');core.dump('VALIDATION.json',report)
    print(json.dumps(rows,ensure_ascii=False));print('Cumulative data checks:',ok)

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'sources':sources,'configure':configure,'geometry':core.geometry,'prepare':core.prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps,'patch-parts':parts.patch_parts,'finish-whitespace':finish_whitespace,'compact-diagnostics':compact_diagnostics,'summary':summary}[sys.argv[1]]()
