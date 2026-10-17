"""Swabian macro-jurisdictions in 1776; staged minimal differential workflow."""
import csv
import io
import json
import sys
import re
import urllib.request
from PIL import Image,ImageDraw,ImageFont,ImageColor
import map2l_rhine_completion as previous
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/SWABIA'
core.OUT=OUT
core.BACKUP=OUT.parent/'RHINE_WESTPHALIA_COMPLETION/provinces_candidate.png'
core.REGIONS={'STATE_BADEN','STATE_WURTTEMBERG','STATE_BAVARIA'}
if hasattr(core,'PREPARE_EXTRA_FILES'):del core.PREPARE_EXTRA_FILES
previous.previous.preceding.OUT=OUT

TAGS=['HSG','SUU','SAG','SKE']
GOVERNMENT_DESCRIPTIONS={
    'gov_aor1776_ulm_council_desc':('A free imperial city, Ulm is governed by its municipal council. Its civic institutions administer the city and its possessions independently of a territorial prince.','Ville libre du Saint-Empire, Ulm est administrée par son conseil urbain. Ses institutions municipales exercent le gouvernement de la ville et de ses possessions, sans dépendre d’un prince territorial.'),
    'gov_aor1776_baden_margraviate_desc':('The margrave rules the Baden possessions reunited under one dynasty since 1771. As a prince of the Holy Roman Empire, he exercises territorial authority within the imperial constitutional framework.','Le margrave gouverne les possessions badoises réunies sous une même dynastie depuis 1771. Prince du Saint-Empire, il exerce son autorité territoriale dans le cadre des institutions impériales.'),
    'gov_aor1776_swabian_principality_desc':('A branch of the House of Hohenzollern rules this hereditary imperial principality. Its prince exercises authority over his own possessions, distinct from those of the other dynastic branches.','Une branche de la maison de Hohenzollern gouverne cette principauté héréditaire du Saint-Empire. Le prince exerce son autorité sur ses propres possessions, distinctes de celles des autres branches de la dynastie.')}

def extra_files(files,migration):
    import validate_diplomacy_ottoman_1776 as parser
    from map2a_patch import edits
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    assert not set(TAGS)&set(baseline['inventory']['countries'])
    specs={'HSG':('STATE_WURTTEMBERG','catholic','107 171 181'),'SUU':('STATE_WURTTEMBERG','protestant','221 203 144'),'SAG':('STATE_BAVARIA','catholic','216 136 146'),'SKE':('STATE_BAVARIA','catholic','162 132 185')}
    definitions=''.join(tag+' = { color = { '+color+' } country_type = recognized tier = principality cultures = { south_german } religion = '+religion+' capital = '+capital+' }\n' for tag,(capital,religion,color) in specs.items())
    files['common/country_definitions/1776_map2l_swabian_estates.txt']=definitions
    rel='common/country_definitions/00_countries.txt';raw=(core.ROOT/rel).read_text(encoding='utf-8-sig');wur=next(n for n in parser.parse(raw) if n.key=='WUR');tier=wur.children('tier')[0]
    assert parser.scalar(tier.value)=='kingdom'
    corrected=edits(raw,[(tier.start,tier.end,'tier = principality')]);files[rel]=corrected
    after=next(n for n in parser.parse(corrected) if n.key=='WUR')
    migration['country_tier_corrections']=[dict(tag='WUR',before='kingdom',after='principality',before_signature=core.qa.signature(wur),after_signature=core.qa.signature(after))]
    # Dedicated variants; no law/government file from an older lot is edited.
    source=(core.ROOT/'common/laws/1776_map2l_franconian_start_variants.txt').read_text(encoding='utf-8-sig');laws=[]
    replacements={'law_aor1776_imperial_customs':'law_aor1776_swabian_customs','law_aor1776_imperial_no_slavery':'law_aor1776_swabian_free_status','law_aor1776_imperial_city_republic':'law_aor1776_ulm_council'}
    for node in parser.parse(source):
        if node.key not in replacements:continue
        text=source[node.start:node.end]
        for old,new in replacements.items():text=text.replace(old,new)
        text=re.sub(r'OR = \{ c:ANS \?= this c:FBM \?= this c:WZB \?= this c:NUR \?= this c:EIC \?= this \}', 'OR = { c:HSG ?= this c:SUU ?= this c:SAG ?= this c:SKE ?= this }',text)
        text=text.replace('c:NUR ?= this','c:SUU ?= this')
        assert 'c:NUR' not in text and 'c:FBM' not in text
        laws.append(text)
    files['common/laws/1776_map2l_swabian_start_variants.txt']='\n'.join(laws)+'\n'
    for tag in TAGS:
        base_tag='NUR' if tag=='SUU' else 'ANS' if tag=='HSG' else 'FBM'
        template=(core.ROOT/f'common/history/countries/{base_tag.lower()} - franconian estate.txt').read_text(encoding='utf-8-sig').replace('c:'+base_tag,'c:'+tag)
        for old,new in replacements.items():template=template.replace(old,new)
        if tag=='SUU':template=template.replace('law_state_religion','law_freedom_of_conscience')
        files[f'common/history/countries/{tag.lower()} - swabian estate.txt']=template
    files['common/history/characters/1776_map2l_swabian_rulers.txt']='''CHARACTERS = {
 c:HSG ?= { create_character = { first_name = aor1776_hsg_first last_name = aor1776_hsg_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1724.1.9 interest_group = ig_landowners ideology = ideology_traditionalist } }
 c:SAG ?= { create_character = { first_name = aor1776_sag_first last_name = aor1776_sag_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1739.9.28 interest_group = ig_devout ideology = ideology_traditionalist } }
 c:SKE ?= { create_character = { first_name = aor1776_ske_first last_name = aor1776_ske_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1726.9.20 interest_group = ig_devout ideology = ideology_traditionalist } }
}
'''
    files['common/government_types/00_1776_map2l_swabia.txt']='''gov_aor1776_ulm_council = {
 transfer_of_power = presidential_elective
 new_leader_on_reform_government = no
 male_ruler = "aor1776_city_councillor_title"
 female_ruler = "aor1776_city_councillor_title"
 possible = { c:SUU ?= this has_law = law_type:law_aor1776_ulm_council }
 on_government_type_change = { change_to_presidential_elective = yes }
 on_post_government_type_change = { post_change_to_presidential_elective = yes }
}
gov_aor1776_baden_margraviate = {
 transfer_of_power = hereditary
 male_ruler = "aor1776_baden_margrave_title"
 female_ruler = "aor1776_baden_margravine_title"
 possible = { c:BAD ?= this has_law = law_type:law_monarchy }
 on_government_type_change = { change_to_hereditary = yes }
 on_post_government_type_change = { post_change_to_hereditary = yes }
}
'''
    coas='';flags=''
    for tag in TAGS:
        ground,ink,emblem={'HSG':('white','black','ce_eagle.dds'),'SUU':('white','black','ce_eagle.dds'),'SAG':('red','white','ce_cross_couped.dds'),'SKE':('blue','yellow','ce_cross_couped.dds')}[tag]
        coas+='AOR1776_'+tag+' = { pattern = "pattern_solid.tga" color1 = '+ground+' colored_emblem = { texture = "'+emblem+'" color1 = '+ink+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
        flags+=tag+' = { flag_definition = { coa = AOR1776_'+tag+' priority = 100 allow_overlord_canton = no } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_swabian_flags.txt']=coas
    files['common/flag_definitions/1776_map2l_swabian_flags.txt']=flags
    names={'HSG':('Hohenzollern-Sigmaringen','Hohenzollern-Sigmaringen'),'HSG_ADJ':('Sigmaringian','Sigmaringeois'),'SUU':('Imperial City of Ulm','Ville impériale d’Ulm'),'SUU_ADJ':('Ulmian','Ulmois'),'SAG':('Prince-Bishopric of Augsburg','Principauté épiscopale d’Augsbourg'),'SAG_ADJ':('Augsburgian','Augsbourgeois'),'SKE':('Prince-Abbey of Kempten','Abbaye-principauté de Kempten'),'SKE_ADJ':('Kemptenian','Kemptenois'),'HOH':('Hohenzollern-Hechingen','Hohenzollern-Hechingen'),'HOH_ADJ':('Hechingenian','Hechingeois'),'aor1776_hsg_first':('Karl Friedrich','Charles-Frédéric'),'aor1776_hsg_last':('von Hohenzollern-Sigmaringen','de Hohenzollern-Sigmaringen'),'aor1776_sag_first':('Clemens Wenzeslaus','Clément-Wenceslas'),'aor1776_sag_last':('von Sachsen','de Saxe'),'aor1776_ske_first':('Honorius','Honorius'),'aor1776_ske_last':('Roth von Schreckenstein','Roth von Schreckenstein'),'gov_aor1776_ulm_council':('Patrician city council','Conseil urbain patricien'),'gov_aor1776_baden_margraviate':('Margraviate','Margraviat'),'aor1776_baden_margrave_title':('Margrave','Margrave'),'aor1776_baden_margravine_title':('Margravine','Margravine'),'law_aor1776_swabian_customs':('Early-modern imperial customs','Douanes impériales d’Ancien Régime'),'law_aor1776_swabian_free_status':('Free status in the imperial estates','Statut libre dans les États impériaux'),'law_aor1776_ulm_council':('Patrician imperial republic','République impériale patricienne'),'law_aor1776_swabian_customs_desc':('Local regulated commerce, without granting later technology.','Commerce réglementé local, sans technologie tardive accordée.'),'law_aor1776_swabian_free_status_desc':('Free legal status at start; serfdom is separate.','Statut juridique libre de départ ; servage distinct.'),'law_aor1776_ulm_council_desc':('Established imperial city council, not a modern national republic.','Conseil d’une ville impériale établie, pas une république nationale moderne.')}
    names.update({key:value for key,value in GOVERNMENT_DESCRIPTIONS.items() if key!='gov_aor1776_swabian_principality_desc'})
    for lang,i in [('english',0),('french',1)]:files[f'localization/{lang}/1776_map2l_swabia_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[i]+'"\n' for k,v in names.items())
    migration['new_members']=TAGS;migration['free_cities']=['SUU']
    migration['country_additions']={n.key:core.qa.signature(n) for n in parser.parse(definitions)}
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

core.PREPARE_EXTRA_FILES=extra_files

def preview(bmp,rows,name):
    import numpy as np
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1]
    palette={'BAD':'#dec459','WUR':'#72a46b','HOH':'#b6b6b6','HSG':'#6babb5','AUS':'#b3a6d8','SUU':'#e6dec4','SAG':'#d88892','SKE':'#a284b9','BAV':'#79afeb','KMZ':'#be5448','KPF':'#d7aa32','SWI':'#c97b73','FRM':'#ed996a'}
    arr=np.full((*local.shape,3),225,dtype=np.uint8)
    for r in rows:arr[local==int(r['key'][0][1:],16)]=ImageColor.getrgb(palette.get(r['key'][2],'#dddddd'))
    border=np.zeros(local.shape,dtype=bool);border[1:]|=local[1:]!=local[:-1];border[:,1:]|=local[:,1:]!=local[:,:-1];arr[border]=60
    scale=12;im=Image.fromarray(arr).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST);canvas=Image.new('RGB',(im.width,im.height+70),'white');canvas.paste(im)
    draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    draw.text((8,im.height+4),name+' | Swabia 1776: named macro-jurisdiction cores, not a cadastre',font=font,fill='black')
    draw.text((8,im.height+25),'Baden gold / Wurttemberg green / Austria violet / Sigmaringen teal / Ulm cream',font=font,fill='black')
    draw.text((8,im.height+46),'Augsburg bishopric pink / Kempten purple / old provisional fringes preserved',font=font,fill='black');canvas.save(OUT/(name+'.png'))

core.preview=preview

def restore_previous_previews():
    # Recovery of derived previews accidentally targeted by the imported
    # wrapper before its OUT-bound preview was overridden. No runtime writes.
    from map2l_belgium import packed
    out=previous.OUT;baseline=json.loads((out/'BASELINE.json').read_text());geo=json.loads((out/'GEOMETRY.json').read_text())
    previous.preview(packed(core.ROOT/baseline['bitmap_backup']),baseline['inventory']['owners'],'BEFORE')
    rows=[r for r in baseline['inventory']['owners'] if r['key'][0] not in geo['parents']]+[dict(key=[r['rgb'],r['state'],r['owner']],count=1) for r in geo['assignments']]
    previous.preview(packed(out/'provinces_candidate.png'),rows,'AFTER')
    left=Image.open(out/'BEFORE.png');right=Image.open(out/'AFTER.png');im=Image.new('RGB',(left.width*2,left.height),'white');im.paste(left);im.paste(right,(left.width,0));im.save(out/'BEFORE_AFTER.png')

def finish():
    # Override the *native* HOH history, which would spawn nineteenth-century
    # Sigmaringen ruler/heir templates for the retained Hechingen country.
    # No existing mod character file is edited, and no army links use them.
    files={}
    rel='common/history/characters/hoh - hohenzollern.txt'
    assert not (core.ROOT/rel).exists()
    files[rel]='CHARACTERS = { c:HOH ?= { create_character = { first_name = aor1776_hoh_first last_name = aor1776_hoh_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1717.11.12 interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    rel='common/government_types/00_1776_map2l_swabia.txt'
    files[rel]=(core.ROOT/rel).read_text()+'''gov_aor1776_swabian_principality = {
 transfer_of_power = hereditary
 male_ruler = "RULER_TITLE_PRINCE"
 female_ruler = "RULER_TITLE_PRINCESS"
 possible = { OR = { c:HOH ?= this c:HSG ?= this } has_law = law_type:law_monarchy }
 on_government_type_change = { change_to_hereditary = yes }
 on_post_government_type_change = { post_change_to_hereditary = yes }
}
'''
    for lang,first,last,title in [('english','Joseph Friedrich Wilhelm','von Hohenzollern-Hechingen','Principality'),('french','Joseph-Frédéric-Guillaume','de Hohenzollern-Hechingen','Principauté')]:
        rel=f'localization/{lang}/1776_map2l_swabia_l_{lang}.yml';files[rel]=(core.ROOT/rel).read_text(encoding='utf-8')+' aor1776_hoh_first:0 "'+first+'"\n aor1776_hoh_last:0 "'+last+'"\n gov_aor1776_swabian_principality:0 "'+title+'"\n'
        files[rel]+=' gov_aor1776_swabian_principality_desc:0 "'+GOVERNMENT_DESCRIPTIONS['gov_aor1776_swabian_principality_desc'][0 if lang=='english' else 1]+'"\n'
    # Trim only newly inserted whitespace compared with the immutable baseline.
    import difflib
    for rel in ['common/history/states/00_states.txt','common/history/pops/00_west_europe.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']:
        base=json.loads((OUT/'BASELINE.json').read_text())['originals'][rel].splitlines();raw=(core.ROOT/rel).read_text(encoding='utf-8-sig');lines=raw.splitlines()
        for tag,_,_,start,end in difflib.SequenceMatcher(None,base,lines,autojunk=False).get_opcodes():
            if tag in {'insert','replace'}:
                for i in range(start,end):lines[i]=lines[i].rstrip()
        cleaned='\n'.join(lines)+'\n'
        if cleaned!=raw:files[rel]=cleaned
    changes=core.emit(files,'FINISH.patch');plan=json.loads((OUT/'PLAN.json').read_text());plan['files']=list(dict.fromkeys(plan['files']+changes));plan['native_history_overrides']=['common/history/characters/hoh - hohenzollern.txt'];core.dump('PLAN.json',plan)

def imperial():
    old=json.loads((OUT/'IMPERIAL_FILES.json').read_text()) if (OUT/'IMPERIAL_FILES.json').exists() else {'files':[]}
    core.imperial()
    new=json.loads((OUT/'IMPERIAL_FILES.json').read_text());new['last_patch_files']=new['files'];new['files']=list(dict.fromkeys(old['files']+new['files']));core.dump('IMPERIAL_FILES.json',new)

def summary():
    import subprocess
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION','SWABIA']
    allowed={'No commit or staging mutation','HEAD and Git index unchanged','Git HEAD and index unchanged'};rows=[]
    for name in names:
        report=json.loads((OUT.parent/name/'VALIDATION.json').read_text());failed=[r['name'] for r in report['checks'] if not r['passed']]
        rows.append(dict(lot=name,raw_status=report['status'],passed=sum(r['passed'] for r in report['checks']),checks=len(report['checks']),failed=failed,data_checks_passed=not(set(failed)-allowed),manual_runtime_status=report.get('runtime_status'),automatic_engine_test=False))
    base=json.loads((OUT/'BASELINE.json').read_text());head=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=core.ROOT,text=True).strip();index=core.sha(core.ROOT/'.git/index');main=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text());authorized=json.loads((OUT.parent/'RHINE_WESTPHALIA/AUTHORIZED_GIT_EVENT.json').read_text())['authorized_head']
    ok=all(r['data_checks_passed'] for r in rows) and head==base['git_head']==authorized and index==base['git_index_sha256'] and all(r['passed'] for r in main['checks'])
    core.dump('NON_REGRESSION.json',dict(status='PASS_STATIC_WITH_AUTHORIZED_HISTORICAL_GIT_DIFFERENCE' if ok else 'FAIL',suites=rows,HEAD=head,index_sha256=index,git_unchanged=head==base['git_head'] and index==base['git_index_sha256'],old_raw_git_failures_retained=True,historical_head_authorized=head==authorized,runtime_tested=False,automatic_engine_testing=False,checkpoint_created=False,bitmap_sha256=core.sha(core.ROOT/'map_data/provinces.png'),registry_sha256=core.sha(core.active_registry_path()),main_map_checks=sum(r['passed'] for r in main['checks']),territorial_coverage='CONSERVATIVE_CORE_SUBLOT_FRINGES_OPEN'))
    from map2l_runtime_receipt import annotate
    report=json.loads((OUT/'VALIDATION.json').read_text());report.update(territorial_coverage='CONSERVATIVE_CORE_SUBLOT_FRINGES_OPEN',inherited_duplicate_RGB_count=len(report['inherited_duplicate_RGBs']),inherited_reference_error_count=len(report['inherited_reference_errors']),manual_test_policy='Scoped manual receipt; later additions and repaired UI descriptions require separate checks',checkpoint_created=False);annotate(report,OUT.name);core.dump('VALIDATION.json',report)
    geo=json.loads((OUT/'GEOMETRY.json').read_text());trace=json.loads((OUT/'TRACING.json').read_text());records=[]
    for r in geo['assignments']:
        row={k:r[k] for k in ['rgb','parent_rgb','state','previous_owner','owner','pixels']};zone=r['source_zone'];row['territory']=trace['polygons'][zone-1]['territory'] if zone else 'Unmodified provisional fringe';row['historical_date']='1776-01-01';row['source']='Homann circa 1693; continuity references in REPORT.md' if zone else 'Prior allocation retained, not certified';row['approximation']='Named conservative game-scale envelope' if zone else 'No new attribution';records.append(row)
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    core.dump('COLGREP_METRICS.json',dict(agent_calls=1,successful_calls=1,elapsed_seconds=192.2108563,query='Locate retained MAP1 R1/R2 and MAP2L research, historical map source manifests and implementation dependencies for reconstructing Swabia 1776: Wurttemberg, reunited Baden, Hohenzollern Hechingen Sigmaringen, Further Austria, Augsburg bishopric, Kempten and free cities. Do not conduct historical research or edit files. Return at most twelve relevant file paths with line ranges, favor existing territorial mapping evidence over general documentation.',executable='C:/Users/simeo/.cargo/bin/colgrep.exe',verified_leads=['docs/reports/map/MAP2L/MAINZ_COMPLETION/REGISTRY_MIGRATION.json:1-393','tools/map2l_franconia.py:67-87','docs/reports/map/MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_UNCERTAINTIES.md:1-100'],new_ready_swabian_geometry_found=False,classic_search_total=None,codex_token_counter=None,quota_savings_measured=False,reason='Useful old architecture leads, but not a new usable Swabian border source; no controlled comparison or exhaustive classic-search counter',integration_changed=False,index_rebuilt=False))
    print('Non-regression:',ok);print(json.dumps(rows,ensure_ascii=False))

def fetch_source():
    target=OUT/'HOMANN_SWABIA_3500.jpg'
    assert not target.exists(),'Never overwrite retained source'
    manifest_url='https://www.e-rara.ch/i3f/v20/29527171/manifest'
    with urllib.request.urlopen(manifest_url,timeout=30) as response:manifest=json.load(response)
    service=manifest['sequences'][0]['canvases'][0]['images'][0]['resource']['service']['@id']
    with urllib.request.urlopen(service+'/full/3500,/0/default.jpg',timeout=30) as response:raw=response.read(30000001)
    assert len(raw)<=30000000
    Image.open(io.BytesIO(raw)).verify();target.write_bytes(raw)
    core.dump('HOMANN_SOURCE.json',dict(manifest_url=manifest_url,manifest=manifest,image_service=service,sha256=core.sha(target),size=list(Image.open(target).size),catalogue='https://www.e-rara.ch/bes_1/content/titleinfo/29527171',institution='Universitaetsbibliothek Bern, Ryhiner collection',use='Bounded supplement to retained R2 inventory; named jurisdiction envelopes, dated sovereignty separately checked',warning='Map predates target: no automatic ownership from colour; reunited Baden represented as one country.'))
    print(target.name,Image.open(target).size)

def inspect():
    image=Image.open(OUT/'HOMANN_SWABIA_3500.jpg').convert('RGB');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for name,box in [('WEST',(500,750,1500,2200)),('CENTRE',(1000,950,2100,2000)),('EAST',(2300,1300,3350,2700)),('LAKE',(1400,1800,2900,2650))]:
        crop=image.crop(box);draw=ImageDraw.Draw(crop)
        for x in range((box[0]//100+1)*100,box[2],100):
            draw.line((x-box[0],0,x-box[0],crop.height),fill='#4466cc');draw.text((x-box[0]+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            draw.line((0,y-box[1],crop.width,y-box[1]),fill='#4466cc');draw.text((0,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'_READING.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as stream:core.dump('NATIVE_ANCHORS.json',[r for r in csv.DictReader(stream) if r['State_ID'] in core.REGIONS])
    for name,box in [('ULM',(2000,1100,2450,1500)),('STUTTGART',(1360,950,1550,1120)),('KONSTANZ',(1530,2180,1740,2300)),('FREIBURG',(540,1580,760,1740))]:
        crop=image.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3));draw=ImageDraw.Draw(crop)
        for x in range((box[0]//25+1)*25,box[2],25):
            draw.line(((x-box[0])*3,0,(x-box[0])*3,crop.height),fill='#4466cc');draw.text(((x-box[0])*3+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//25+1)*25,box[3],25):
            draw.line((0,(y-box[1])*3,crop.width,(y-box[1])*3),fill='#4466cc');draw.text((0,(y-box[1])*3+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'_TOWN.png'))

if __name__=='__main__':
    {'capture':core.capture,'fetch-source':fetch_source,'inspect':inspect,'geometry':core.geometry,'prepare':core.prepare,'install':core.install,'imperial':imperial,'maps':core.maps,'patch-parts':previous.previous.preceding.patch_parts,'restore-previews':restore_previous_previews,'finish':finish,'summary':summary}[sys.argv[1]]()
