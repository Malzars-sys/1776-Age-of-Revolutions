"""Final major Swabian jurisdictions; preserve immutable preceding baseline."""
import csv,json,sys,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2l_swabia_finish as previous
import map2l_mainz as core
import map2l_minden_ravensberg as parts

OUT=core.ROOT/'docs/reports/map/MAP2L/SWABIA_COMPLETION'
core.OUT=OUT;core.BACKUP=previous.OUT/'provinces_candidate.png'
core.REGIONS={'STATE_BADEN','STATE_WURTTEMBERG','STATE_BAVARIA'}
if hasattr(core,'PREPARE_EXTRA_FILES'):del core.PREPARE_EXTRA_FILES
parts.OUT=OUT
TAGS=['SAC','SKI','SRT','SBI','SMM','SRQ','SWG']
CITIES=TAGS[:-1]

def configure():
    b=json.loads((OUT/'BASELINE.json').read_text());assert not set(TAGS)&set(b['inventory']['countries'])
    inherited=json.loads((previous.OUT/'TRACING.json').read_text())['calibrated_sources'][0]
    hm=json.loads((OUT.parent/'SWABIA_CONTINUATION/TRACING.json').read_text())['calibrated_sources'][0]
    controls=[dict(name=n,source=s,game=g,role='FIT') for n,s,g in [('Stuttgart',[2805,2560],[4307.691,894.881]),('Ulm',[4140,3530],[4322.459,909.464]),('Konstanz',[2890,5280],[4302.231,925.839])]]
    north=np.linalg.lstsq(np.array([[*r['source'],1] for r in controls]),np.array([r['game'] for r in controls]),rcond=None)[0].tolist()
    sources=[dict(**{k:v for k,v in inherited.items() if k not in ['path','key']},key='AT',path='../SWABIA_FINISH/EVIDENCE/HABW_06_13.jpg'),dict(key='AN',path='../SWABIA_FINISH/EVIDENCE/HABW_06_13.jpg',matrix=north,controls=controls),dict(**{k:v for k,v in hm.items() if k not in ['path','key']},key='HM',path='../SWABIA/HOMANN_SWABIA_3500.jpg')]
    polygons=[
      dict(source='AN',owner='SES',territory='Free imperial city Esslingen: conservative municipal jurisdiction, not Wurttemberg hinterland',points=[[3070,2715],[3105,2695],[3140,2730],[3165,2760],[3145,2790],[3120,2775],[3090,2775]]),
      dict(source='AN',owner='SRT',territory='Free imperial city Reutlingen: municipal mainland and Wannweil core',points=[[2820,3230],[2850,3210],[2870,3215],[2870,3250],[2900,3270],[2930,3260],[2940,3235],[2970,3225],[3010,3260],[3010,3310],[2940,3330],[2880,3310],[2830,3290]]),
      dict(source='AN',owner='SBI',territory='Free imperial city Biberach: conservative temporal municipal mainland, not neighbouring abbey properties',points=[[3780,4210],[3850,4200],[3885,4240],[3860,4265],[3890,4290],[3890,4320],[3830,4320],[3795,4290],[3790,4250]]),
      dict(source='AN',owner='SMM',territory='Free imperial city Memmingen: mainland municipal jurisdiction, excluding Ottobeuren abbey',points=[[4470,4430],[4520,4425],[4545,4460],[4550,4510],[4535,4560],[4490,4570],[4470,4530],[4460,4500]]),
      dict(source='AT',owner='SRQ',territory='Free imperial city Ravensburg: conservative mainland, separate from Weingarten and Landvogtei',points=[[3430,4910],[3500,4935],[3530,4965],[3550,4995],[3530,5035],[3470,5030],[3440,4990]]),
      dict(source='AT',owner='SWG',territory='Weingarten abbey: explicitly mapped abbatial administered mainland, not entire Austrian high-jurisdiction Landvogtei',points=[[3585,4900],[3610,4895],[3650,4930],[3660,4990],[3595,5005],[3565,4970],[3570,4935]]),
      dict(source='AT',owner='AUS',territory='Austrian Landvogtei: conservative Baienfurt-Baindt adjacent office 9; abbey office 45 excluded',points=[[3670,4805],[3720,4800],[3770,4840],[3780,4890],[3725,4910],[3670,4880]])]
    # Player explicitly authorises one cell for each important subpixel city.
    for tag,point,territory in [('SAC',[4342,910],'Augsburg free city: user-authorised one-cell urban abstraction'),('SKI',[4324,928],'Kempten free city: user-authorised one-cell urban abstraction, abbey retained')]:
        x,y=point;polygons.append(dict(source='PX',owner=tag,territory=territory,points=[[x,y],[x+1,y],[x+1,y+1],[x,y+1]],requested_city_cell=point))
    sources.append(dict(key='PX',path='../SWABIA/HOMANN_SWABIA_3500.jpg',matrix=[[1,0],[0,1],[0,0]],controls=[],basis='Explicit one-cell abstraction at approximate inherited Homann city positions, not cadastral footprint'))
    from map2l_belgium import packed
    from map2l_franconia import inside
    bmp=packed(core.ROOT/b['bitmap_backup']);matrices={s['key']:np.array(s['matrix']) for s in sources};parents=set();findings=[]
    for p in polygons:
        found=[];t=matrices[p['source']]
        for row in b['inventory']['owners']:
            rgb,sid,owner=row['key']
            if sid not in core.REGIONS or (owner not in {'BAD','WUR','BAV'} and not(p['owner']=='SKI' and rgb=='xEDAD0D' and owner=='SKE')):continue
            ys,xs=np.where(bmp==int(rgb[1:],16));local=(np.column_stack((xs,ys))+.5-t[2])@np.linalg.inv(t[:2]);count=int(inside(local,p['points']).sum())
            if count:found.append(rgb);parents.add(rgb);findings.append(dict(territory=p['territory'],parent=rgb,state=sid,before=owner,after=p['owner'],cells=count))
        p['parents']=found
    core.dump('TRACING.json',dict(historical_date='1776-01-01',method='Reused temporal atlas envelopes; explicit user-approved one-cell urban abstractions; no Erfurt recalibration',calibrated_sources=sources,parents=sorted(parents),rgb_start=0xEDB000,native_anchors='NATIVE_ANCHORS.json',hub_rebinding_parents=sorted(parents),preview_box=[4293,888,4349,938],polygons=polygons,limitations=['One-cell Augsburg and Kempten are explicitly authorised urban abstractions, not expanded historical cadastral boundaries.','Atlas 1790 is used only for compatible 1776 named jurisdiction cores; source-map/native locator correspondence is approximate, not independently verified survey accuracy.','Weingarten administered abbatial lands distinct from Austrian high jurisdiction; overlapping rights are an explicit game-model simplification.','Protected prior owner cores excluded except exactly one Kempten cell authorised by user; no Montbeliard or Erfurt transfer.']))
    core.dump('CANDIDATE_INTERSECTIONS.json',findings);print(json.dumps(findings,ensure_ascii=False))

def weights():
    b=json.loads((OUT/'BASELINE.json').read_text());pop={(r['key'][0],r['key'][1],r['key'][2]+'/'+r['key'][3].replace('DEFAULT:south_german','DEFAULT')):r['count'] for r in b['inventory']['regional_pop']}
    catholic=pop['STATE_BAVARIA','BAV','south_german/DEFAULT'];protestant=pop['STATE_BAVARIA','BAV','south_german/protestant']
    core.POPULATION_ALLOCATION_WEIGHTS={('STATE_BAVARIA','BAV','south_german/DEFAULT'):{'BAV':catholic-12000,'SAC':12000},('STATE_BAVARIA','BAV','south_german/protestant'):{'BAV':protestant-14000,'SAC':10000,'SKI':4000},('STATE_BAVARIA','BAV','ashkenazi/DEFAULT'):{'BAV':1}}
    for row in b['inventory']['regional_pop']:
        if row['key'][:2]==['STATE_BAVARIA','SKE']:
            profile=row['key'][2]+'/'+('DEFAULT' if row['key'][3].startswith('DEFAULT:') else row['key'][3]);core.POPULATION_ALLOCATION_WEIGHTS['STATE_BAVARIA','SKE',profile]={'SKE':1}
    core.BUILDING_ALLOCATION_WEIGHTS={('common/history/buildings/00_west_europe.txt','STATE_BAVARIA','BAV','building_food_industry'):{'SAC':1},('common/history/buildings/98_build_start_1776_world_redistribution.txt','STATE_BAVARIA','BAV','building_livestock_ranch'):{'BAV':9,'SKI':1}}
    core.dump('URBAN_ALLOCATION_WEIGHTS.json',dict(population=[dict(state=k[0],source=k[1],profile=k[2],weights=v) for k,v in core.POPULATION_ALLOCATION_WEIGHTS.items()],buildings=[dict(file=k[0],state=k[1],source=k[2],type=k[3],weights=v) for k,v in core.BUILDING_ALLOCATION_WEIGHTS.items()],warning='Explicit gameplay-scale urban allocations from existing source profiles, NOT a 1776 census; zero new inhabitants or buildings. Kempten abbey population retained; 4000 existing Bavarian Protestants form the independent city.'))

def extra_files(files,migration):
    parser=core.cw
    geometry=json.loads((OUT/'GEOMETRY.json').read_text())
    capitals={tag:next(r['state'] for r in geometry['assignments'] if r['owner']==tag) for tag in TAGS}
    colors=['196 137 72','120 165 209','172 197 102','167 119 167','223 188 103','119 177 166','115 153 91']
    defs=''.join(tag+' = { color = { '+color+' } country_type = recognized tier = principality cultures = { south_german } religion = '+('catholic' if tag in {'SAC','SWG'} else 'protestant')+' capital = '+capitals[tag]+' }\n' for tag,color in zip(TAGS,colors))
    # Biberach/Ravensburg are confessionally mixed/parity cities; do not
    # convert transferred population profiles to the state's default religion.
    defs=defs.replace('SBI = { color = { 167 119 167 } country_type = recognized tier = principality cultures = { south_german } religion = protestant','SBI = { color = { 167 119 167 } country_type = recognized tier = principality cultures = { south_german } religion = catholic').replace('SRQ = { color = { 119 177 166 } country_type = recognized tier = principality cultures = { south_german } religion = protestant','SRQ = { color = { 119 177 166 } country_type = recognized tier = principality cultures = { south_german } religion = catholic')
    files['common/country_definitions/1776_map2l_swabia_completion.txt']=defs
    replacements={'law_aor1776_ulm_council':'law_aor1776_completion_city_council','law_aor1776_swabian_customs':'law_aor1776_completion_customs','law_aor1776_swabian_free_status':'law_aor1776_completion_free_status'}
    source=(core.ROOT/'common/laws/1776_map2l_swabian_start_variants.txt').read_text(encoding='utf-8-sig');laws=[]
    for n in parser.parse(source):
        text=source[n.start:n.end]
        for old,new in replacements.items():text=text.replace(old,new)
        if n.key=='law_aor1776_ulm_council':text=text.replace('c:SUU ?= this','OR = { '+' '.join('c:'+tag+' ?= this' for tag in CITIES)+' }')
        else:text=re.sub(r'OR = \{ c:HSG \?= this c:SUU \?= this c:SAG \?= this c:SKE \?= this \}', 'OR = { '+' '.join('c:'+tag+' ?= this' for tag in TAGS)+' }',text)
        laws.append(text)
    files['common/laws/1776_map2l_swabia_completion.txt']='\n'.join(laws)+'\n'
    for tag in TAGS:
        if tag in CITIES:
            text=(core.ROOT/'common/history/countries/suu - swabian estate.txt').read_text(encoding='utf-8-sig').replace('c:SUU','c:'+tag)
            for old,new in replacements.items():text=text.replace(old,new)
        else:
            text=(core.ROOT/'common/history/countries/fbm - franconian estate.txt').read_text(encoding='utf-8-sig').replace('c:FBM','c:'+tag).replace('law_aor1776_imperial_customs','law_aor1776_completion_customs').replace('law_aor1776_imperial_no_slavery','law_aor1776_completion_free_status')
        files[f'common/history/countries/{tag.lower()} - swabia completion.txt']=text
    governments=''
    for tag in TAGS:
        city=tag in CITIES;power='presidential_elective' if city else 'dictatorial';law='law_aor1776_completion_city_council' if city else 'law_theocracy';title='aor1776_city_councillor_title' if city else 'aor1776_completion_abbot_title'
        governments+='gov_aor1776_'+tag.lower()+' = { transfer_of_power = '+power+' new_leader_on_reform_government = no male_ruler = "'+title+'" female_ruler = "'+title+'" possible = { c:'+tag+' ?= this has_law = law_type:'+law+' } on_government_type_change = { change_to_'+power+' = yes } on_post_government_type_change = { post_change_to_'+power+' = yes } }\n'
    files['common/government_types/00_1776_map2l_swabia_completion.txt']=governments
    # The documented abbot is Dominicus Schnizer (1745–1784), not the
    # successor Anselm Rittler. No unverified age/birth date is invented.
    files['common/history/characters/1776_map2l_swabia_completion.txt']='CHARACTERS = { c:SWG ?= { create_character = { first_name = aor1776_swg_first last_name = aor1776_swg_last historical = yes culture = south_german religion = rel:catholic ruler = yes interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    coas='';flags=''
    for tag in TAGS:
        coas+='AOR1776_'+tag+' = { pattern = "pattern_solid.tga" color1 = '+('green' if tag=='SWG' else 'white')+' colored_emblem = { texture = "'+('ce_cross_couped.dds' if tag=='SWG' else 'ce_eagle.dds')+'" color1 = '+('yellow' if tag=='SWG' else 'black')+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
        flags+=tag+' = { flag_definition = { coa = AOR1776_'+tag+' priority = 100 allow_overlord_canton = no } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_swabia_completion.txt']=coas;files['common/flag_definitions/1776_map2l_swabia_completion.txt']=flags
    towns={'SAC':('Augsburg','Augsbourg'),'SKI':('Kempten','Kempten'),'SRT':('Reutlingen','Reutlingen'),'SBI':('Biberach','Biberach'),'SMM':('Memmingen','Memmingen'),'SRQ':('Ravensburg','Ravensbourg')}
    names={'SWG':('Imperial Abbey of Weingarten','Abbaye impériale de Weingarten'),'SWG_ADJ':('Weingartenian','De Weingarten'),'aor1776_swg_first':('Dominicus','Dominicus'),'aor1776_swg_last':('Schnizer','Schnizer'),'aor1776_completion_abbot_title':('Imperial Abbot','Abbé impérial')}
    for tag,town in towns.items():names[tag]=('Free Imperial City of '+town[0],'Ville libre impériale de '+town[1]);names[tag+'_ADJ']=(town[0]+' municipal','De '+town[1])
    for tag in TAGS:
        names['gov_aor1776_'+tag.lower()]=('Patrician city council','Conseil urbain patricien') if tag in CITIES else ('Imperial abbey','Abbaye impériale')
        names['gov_aor1776_'+tag.lower()+'_desc']=('The free imperial city governs its municipal territory through its own urban council, independently of neighbouring princes or abbeys.','La ville libre impériale gouverne son territoire municipal par son propre conseil urbain, indépendamment des princes ou abbayes voisins.') if tag in CITIES else ('The imperial abbot governs the temporal lands administered by Weingarten; Austrian high-jurisdiction rights and the neighbouring city of Ravensburg remain distinct.','L’abbé impérial gouverne les terres temporelles administrées par Weingarten ; les droits de haute justice autrichiens et la ville voisine de Ravensbourg restent distincts.')
    for law in replacements.values():names[law]=('Imperial estate start','Départ d’État impérial');names[law+'_desc']=('1776 legal variant; no later technologies granted.','Variante juridique de 1776 ; aucune technologie ultérieure accordée.')
    for lang,i in [('english',0),('french',1)]:files[f'localization/{lang}/1776_map2l_swabia_completion_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+key+':0 "'+value[i]+'"\n' for key,value in names.items())
    migration.update(new_members=TAGS,free_cities=CITIES,country_additions={n.key:core.qa.signature(n) for n in parser.parse(defs)},core_exceptions=[dict(preceding_lot='SWABIA',rgb='xEDAD0D',previous_owner='SKE',new_owner='SKI',cells=[[4324,928]],reason='User explicitly authorised one-cell independent city; abbey retains sixteen cells and its population')])
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

core.PREPARE_EXTRA_FILES=extra_files

def prepare():
    weights();core.prepare()

def preview(bmp,rows,name):
    from PIL import ImageColor
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1];arr=np.full((*local.shape,3),220,dtype=np.uint8)
    colors={'BAD':'#dec459','WUR':'#72a46b','AUS':'#b3a6d8','BAV':'#79afeb','SAG':'#d88892','SKE':'#a284b9','SAC':'#c48948','SKI':'#78a5d1','SRT':'#acc566','SBI':'#a777a7','SMM':'#dfbc67','SRQ':'#77b1a6','SWG':'#73995b'}
    for row in rows:arr[local==int(row['key'][0][1:],16)]=ImageColor.getrgb(colors.get(row['key'][2],'#ccc'))
    im=Image.fromarray(arr).resize((local.shape[1]*18,local.shape[0]*18),Image.Resampling.NEAREST);canvas=Image.new('RGB',(im.width,im.height+95),'white');canvas.paste(im);d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    d.text((5,im.height+5),name+' | 1776 conservative cores, not cadastral boundaries',fill='black',font=font)
    for i,tag in enumerate(TAGS):
        xx=5+(i%4)*250;yy=im.height+30+(i//4)*27;d.rectangle((xx,yy,xx+15,yy+15),fill=colors[tag]);d.text((xx+20,yy),tag+' '+(dict(SAC='Augsburg',SKI='Kempten',SRT='Reutlingen',SBI='Biberach',SMM='Memmingen',SRQ='Ravensburg',SWG='Weingarten')[tag]),fill='black',font=font)
    canvas.save(OUT/(name+'.png'))

core.preview=preview

def summary():
    """Derived report tables; never rewrite immutable baselines or Git state."""
    from map2l_belgium import sha
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION','SWABIA','SWABIA_CONTINUATION','SWABIA_FINISH','SWABIA_COMPLETION']
    run=json.loads((OUT/'CUMULATIVE_RUN.json').read_text());assert len(run)==16 and all('Traceback' not in r['output'] for r in run)
    allowed={'No commit or staging mutation','HEAD and Git index unchanged','Git HEAD and index unchanged'};rows=[]
    for name in names:
        data=json.loads((OUT.parent/name/'VALIDATION.json').read_text());failed=[r['name'] for r in data['checks'] if not r['passed']];rows.append(dict(lot=name,raw_status=data['status'],passed=sum(r['passed'] for r in data['checks']),checks=len(data['checks']),failed=failed,data_checks_passed=not(set(failed)-allowed),manual_runtime_status=data.get('runtime_status','NOT_YET_TESTED'),automatic_engine_test=False))
    assert all(r['data_checks_passed'] for r in rows),'Do not promote a data regression to a Git-only exception'
    core.dump('NON_REGRESSION.json',dict(status='PASS_STATIC_WITH_AUTHORIZED_HISTORICAL_GIT_DIFFERENCES',phase='AFTER_SWABIAN_MAP_BEFORE_EXPLICIT_PRUSSIAN_INDUSTRY_ADDITION',suites=rows,passed=sum(r['passed'] for r in rows),checks=sum(r['checks'] for r in rows),historical_git_only_failures=sum(len(r['failed']) for r in rows),old_raw_failures_retained=True,automatic_engine_testing=False,registry_sha256=sha(core.active_registry_path()),bitmap_sha256=sha(core.ROOT/'map_data/provinces.png')))
    g=json.loads((OUT/'GEOMETRY.json').read_text());cfg=json.loads((OUT/'TRACING.json').read_text());records=[]
    for r in g['assignments']:
        row={k:r[k] for k in ['rgb','parent_rgb','state','previous_owner','owner','pixels']};zone=r['source_zone'];row.update(territory=cfg['polygons'][zone-1]['territory'] if zone else 'Retained provisional fringe',historical_date='1776-01-01',ownership_changed=r['owner']!=r['previous_owner'],approximation='Explicit authorised urban abstraction' if zone and cfg['polygons'][zone-1]['source']=='PX' else 'Conservative municipal/temporal jurisdiction core; retained fringe not historically certified');records.append(row)
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    core.dump('COLGREP_METRICS.json',dict(agent_attempts=2,successful_agent_executions=1,failures_before_startup=1,successful_elapsed_seconds=218.66,successful_exit_code=0,executable='C:/Users/simeo/.cargo/bin/colgrep.exe',arguments=['--agent','Locate retained original MAP-1 R1 R2 historical research and source references for the free imperial cities Augsburg Kempten Esslingen Reutlingen Memmingen Biberach and the temporal lands of Weingarten. Return relevant existing paths and lines, prioritising original research over recent Swabia implementation reports. Read-only search: do not edit files or settings.',str(core.ROOT)],model_configuration='Existing local ColGrep-Agent-2B; not modified',independently_verified_GPU_execution=False,codex_task_tokens=None,classic_search_count=None,classic_search_count_note='Not instrumented accurately; exact identifiers and known files read directly; no artificial comparison run',useful_new_documents_found=0,verified_irrelevant_leads=['MAP1_CASE_DOSSIERS/R1_WESTERN_EUROPE-0001.md: Luxembourg','MAP1_CASE_DOSSIERS/R1_WESTERN_EUROPE-0002.md: Liege','Known map1_packet_builder.py and map2l_swabia_continuation.py'],quota_saving='No exact comparison possible; limited practical benefit for this query'))
    base=json.loads((OUT.parent/'CHECKPOINT_RHINE_SWABIA_USER_VALIDATED.json').read_text());delta=json.loads((OUT.parent/'CHECKPOINT_RHINE_SWABIA_METADATA_FINALIZED.json').read_text());assert delta['parent']==base['commit'] and delta['commit']=='cadb544c7de706707532e26bdf19998cf7601cec'
    core.dump('CHECKPOINT_READ_ONLY_VERIFICATION.json',dict(date='2026-10-14',remote_branch='backup/1776-checkpoints',observed_remote_commit=delta['commit'],remote_read='git ls-remote origin refs/heads/backup/1776-checkpoints; exit 0',prior_full_restoration_receipt=base['status'],prior_incremental_receipt=delta['status'],fresh_full_restore_performed=False,new_archive_created=False,new_push_performed=False,new_lot_included=False,missing_local_current_manifest='docs/backups/CURRENT_CHECKPOINT_MANIFEST.json is absent locally; retained remote restoration receipts were used, not silently regenerated'))
    closure_path=OUT.parent/'CLOSURE_STATUS.json';closure=json.loads(closure_path.read_text())
    closure.update(latest_local_territorial_lot='SWABIA_COMPLETION',latest_local_territorial_changes={'ownership_cells':16,'new_RGBs':13,'registered_RGBs':498,'imperial_extent_cells':62580},latest_local_runtime_status='NOT_YET_TESTED',major_swabian_work_status='MAJOR_PASSES_APPLIED_WITH_BOUNDED_RESIDUALS_NOT_EXHAUSTIVE_HISTORICAL_CERTIFICATION',latest_static_validation={'new_lot_passed':570,'new_lot_checks':570,'cumulative_lots':len(rows),'cumulative_raw_passed':sum(r['passed'] for r in rows),'cumulative_raw_checks':sum(r['checks'] for r in rows),'historical_git_only_differences':sum(len(r['failed']) for r in rows),'all_data_checks_passed':True,'automated_engine_test':False,'phase':'Before separately validated player-requested Prussian +13 building levels'},open_swabian_jurisdictions=['Montbeliard separated Wurttemberg dependencies','Esslingen Kaufbeuren Isny Lindau residual representation','Weingarten external/overlapping temporal rights','Scattered Waldburg Salem Furstenberg Ellwangen holdings','Constance Meersburg and northern Augsburg bishopric temporal fringes','Untraced Baden Wurttemberg Austrian fringes'],open_details='SWABIA_COMPLETION/UNRESOLVED.csv',next_gate='New-game tests of the six additional free cities, Weingarten, map layers and explicit Prussian industry addon; do not automatically start another region')
    for field,item in [('manual_runtime_receipts','RUNTIME_USER_VALIDATION_SWABIA_FINISH.json'),('latest_user_validated_scope','SWABIA_FINISH')]:
        if item not in closure[field]:closure[field].append(item)
    core.emit({closure_path.relative_to(core.ROOT).as_posix():json.dumps(closure,ensure_ascii=False,indent=2)+'\n'},'CLOSURE.patch')
    print('Cumulative',sum(r['passed'] for r in rows),'/',sum(r['checks'] for r in rows),'with',sum(len(r['failed']) for r in rows),'historical Git-only differences')

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    for source,name,box in [('../SWABIA_FINISH/EVIDENCE/HABW_06_13.jpg','CITIES',(2200,2500,4900,4600)),('../SWABIA_FINISH/EVIDENCE/HABW_06_13.jpg','WEINGARTEN',(3350,4750,3880,5230)),('../SWABIA/HOMANN_SWABIA_3500.jpg','AUGSBURG',(2700,1260,3090,1580)),('../SWABIA/HOMANN_SWABIA_3500.jpg','KEMPTEN',(2380,2100,2630,2350))]:
        image=Image.open(OUT/source).convert('RGB').crop(box);draw=ImageDraw.Draw(image)
        for x in range((box[0]//50+1)*50,box[2],50):draw.line((x-box[0],0,x-box[0],image.height),fill='blue');draw.text((x-box[0]+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//50+1)*50,box[3],50):draw.line((0,y-box[1],image.width,y-box[1]),fill='blue');draw.text((0,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        image.save(OUT/(name+'_READING.jpg'),quality=92)
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:core.dump('NATIVE_ANCHORS.json',[r for r in csv.DictReader(f) if r['State_ID'] in core.REGIONS])
    source=Image.open(previous.OUT/'EVIDENCE/HABW_06_13.jpg').convert('RGB')
    for name,box in [('ULM',(4000,3400,4330,3660)),('ESSLINGEN',(3000,2660,3250,2900)),('REUTLINGEN',(2450,3200,2850,3450)),('BIBERACH',(3670,4160,3990,4460)),('MEMMINGEN',(4300,4390,4680,4640)),('WEIN_BAINDT',(3400,4780,3750,5040))]:
        im=source.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2));d=ImageDraw.Draw(im)
        for x in range((box[0]//25+1)*25,box[2],25):d.line(((x-box[0])*2,0,(x-box[0])*2,im.height),fill='blue');d.text(((x-box[0])*2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//25+1)*25,box[3],25):d.line((0,(y-box[1])*2,im.width,(y-box[1])*2),fill='blue');d.text((0,(y-box[1])*2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        im.save(OUT/(name+'_DETAIL.jpg'),quality=92)

if __name__=='__main__':{'capture':core.capture,'inspect':inspect,'configure':configure,'geometry':core.geometry,'prepare':prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps,'patch-parts':parts.patch_parts,'summary':summary}[sys.argv[1]]()
