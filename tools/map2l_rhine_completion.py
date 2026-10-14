"""Explicit continuation of retained Rhine/Westphalia evidence, no other MAP lot."""
import csv
import json
import sys
from PIL import Image, ImageDraw, ImageFont
import map2l_duchy_westphalia as previous
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/RHINE_WESTPHALIA_COMPLETION'
core.OUT=OUT
core.BACKUP=OUT.parent/'DUCHY_WESTPHALIA/provinces_candidate.png'
core.REGIONS={'STATE_HANNOVER','STATE_WESTPHALIA'}
previous.preceding.OUT=OUT

def extra_files(files,migration):
    import validate_diplomacy_ottoman_1776 as parser
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    assert 'WPO' not in baseline['inventory']['countries']
    definition='WPO = { color = { 213 181 104 } country_type = recognized tier = principality cultures = { north_german } religion = protestant capital = STATE_HANNOVER }\n'
    files['common/country_definitions/1776_map2l_osnabruck.txt']=definition
    template=(core.ROOT/'common/history/countries/fbm - franconian estate.txt').read_text(encoding='utf-8-sig')
    files['common/history/countries/wpo - osnabruck.txt']=template.replace('c:FBM','c:WPO').replace('law_aor1776_imperial_customs','law_aor1776_osnabruck_customs').replace('law_aor1776_imperial_no_slavery','law_aor1776_osnabruck_free_status').replace('law_state_religion','law_freedom_of_conscience')
    source=(core.ROOT/'common/laws/1776_map2l_franconian_start_variants.txt').read_text(encoding='utf-8-sig')
    import re
    laws=[]
    for node in parser.parse(source):
        if node.key not in {'law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery'}:continue
        raw=source[node.start:node.end].replace('law_aor1776_imperial_customs','law_aor1776_osnabruck_customs').replace('law_aor1776_imperial_no_slavery','law_aor1776_osnabruck_free_status')
        raw=re.sub(r'OR = \{ c:ANS \?= this c:FBM \?= this c:WZB \?= this c:NUR \?= this c:EIC \?= this \}', 'c:WPO ?= this',raw)
        assert 'c:FBM' not in raw
        laws.append(raw)
    files['common/laws/1776_map2l_osnabruck_start_variants.txt']='\n'.join(laws)+'\n'
    # Nominal prince-bishop, aged twelve on 1776-01-01. No fictional adult,
    # no retroactive annexation, and no invented personal-union mechanic.
    files['common/history/characters/1776_map2l_osnabruck_ruler.txt']='CHARACTERS = { c:WPO ?= { create_character = { first_name = aor1776_wpo_first last_name = aor1776_wpo_last historical = yes culture = north_german religion = rel:protestant ruler = yes age = 12 interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_osnabruck.txt']='AOR1776_WPO = { pattern = "pattern_solid.tga" color1 = yellow colored_emblem = { texture = "ce_ship_wheel.dds" color1 = red instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
    files['common/flag_definitions/1776_map2l_osnabruck.txt']='WPO = { flag_definition = { coa = AOR1776_WPO priority = 100 allow_overlord_canton = no } }\n'
    names={'WPO':('Prince-Bishopric of Osnabruck','Principauté épiscopale d’Osnabrück'),'WPO_ADJ':('Osnabruckian','Osnabrückois'),'aor1776_wpo_first':('Frederick Augustus','Frédéric-Auguste'),'aor1776_wpo_last':('of Brunswick-Luneburg','de Brunswick-Lunebourg'),'law_aor1776_osnabruck_customs':('Early-modern episcopal customs','Douanes épiscopales d’Ancien Régime'),'law_aor1776_osnabruck_free_status':('Free status in Osnabruck','Statut libre à Osnabrück'),'law_aor1776_osnabruck_customs_desc':('Local regulated commerce; no later technology is granted.','Commerce local réglementé ; aucune technologie tardive accordée.'),'law_aor1776_osnabruck_free_status_desc':('Starting free legal status; serfdom is handled separately.','Statut juridique libre de départ ; servage traité séparément.')}
    for lang,i in [('english',0),('french',1)]:
        files['localization/'+lang+'/1776_map2l_osnabruck_l_'+lang+'.yml']='\ufeffl_'+lang+':\n'+''.join(' '+key+':0 "'+value[i]+'"\n' for key,value in names.items())
    migration['new_members']=['WPO']
    migration['country_additions']={node.key:core.qa.signature(node) for node in parser.parse(definition)}
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

core.PREPARE_EXTRA_FILES=extra_files

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    image=Image.open(OUT.parent/'RHINE_WESTPHALIA/SCHENK_WESTPHALIA_1710_FULL.jpg').convert('RGB')
    image.crop((1200,1080,1420,1250)).resize((1100,850)).save(OUT/'OSNABRUCK_TOWN_CLEAN.png')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for name,box in [('NIEDERSTIFT',(730,480,1520,1190)),('OSNABRUCK',(990,950,1460,1360)),('RAVENSBERG',(1240,1190,1580,1440))]:
        crop=image.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2));draw=ImageDraw.Draw(crop)
        for x in range((box[0]//50+1)*50,box[2],50):
            draw.line(((x-box[0])*2,0,(x-box[0])*2,crop.height),fill='#5577dd');draw.text(((x-box[0])*2+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//50+1)*50,box[3],50):
            draw.line((0,(y-box[1])*2,crop.width,(y-box[1])*2),fill='#5577dd');draw.text((0,(y-box[1])*2+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'_READING.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as stream:
        core.dump('NATIVE_ANCHORS.json',[r for r in csv.DictReader(stream) if r['State_ID'] in core.REGIONS])

def preview(bmp,rows,name):
    # Use the established political palette, with an explicit distinct Osnabruck.
    import numpy as np
    from PIL import ImageColor
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1]
    colors={'PRU':'#609ab6','KCL':'#737db9','WPM':'#87b468','WPD':'#e09070','WPO':'#d5b568','LIP':'#bb8aab','SCM':'#dec588','HAN':'#bbc0b2','OLD':'#dba47a','NET':'#d8945d'}
    arr=np.full((*local.shape,3),220,dtype=np.uint8)
    for row in rows:arr[local==int(row['key'][0][1:],16)]=ImageColor.getrgb(colors.get(row['key'][2],'#cccccc'))
    edge=np.zeros(local.shape,dtype=bool);edge[1:]|=local[1:]!=local[:-1];edge[:,1:]|=local[:,1:]!=local[:,:-1];arr[edge]=50
    scale=10;im=Image.fromarray(arr).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(im.width,im.height+65),'white');canvas.paste(im);draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    draw.text((8,im.height+5),name+' | Osnabruck gold / Munster green / Prussia blue / Hanover gray',font=font,fill='black')
    draw.text((8,im.height+30),'Period-map macro envelopes; unmodified fringes remain unresolved.',font=font,fill='black')
    canvas.save(OUT/(name+'.png'))

core.preview=preview

def clean_new_whitespace():
    import difflib
    rel='common/history/pops/00_west_europe.txt'
    original=json.loads((OUT/'BASELINE.json').read_text())['originals'][rel].splitlines()
    raw=(core.ROOT/rel).read_text(encoding='utf-8-sig');lines=raw.splitlines()
    for tag,_,_,start,end in difflib.SequenceMatcher(None,original,lines,autojunk=False).get_opcodes():
        if tag in {'insert','replace'}:
            for i in range(start,end):lines[i]=lines[i].rstrip()
    core.emit({rel:'\n'.join(lines)+'\n'},'WHITESPACE.patch')

def summary():
    import subprocess
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION']
    git_checks={'No commit or staging mutation','HEAD and Git index unchanged','Git HEAD and index unchanged'}
    rows=[]
    for name in names:
        report=json.loads((OUT.parent/name/'VALIDATION.json').read_text())
        failed=[r['name'] for r in report['checks'] if not r['passed']]
        rows.append(dict(lot=name,raw_status=report['status'],passed=sum(r['passed'] for r in report['checks']),checks=len(report['checks']),failed=failed,gameplay_static_checks_passed=not(set(failed)-git_checks),manual_runtime_status=report.get('runtime_status'),automatic_engine_test=False))
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    head=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=core.ROOT,text=True).strip();index=core.sha(core.ROOT/'.git/index')
    authorized=json.loads((OUT.parent/'RHINE_WESTPHALIA/AUTHORIZED_GIT_EVENT.json').read_text())['authorized_head']
    main=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text())
    passed=all(r['gameplay_static_checks_passed'] for r in rows) and head==baseline['git_head']==authorized and index==baseline['git_index_sha256'] and all(r['passed'] for r in main['checks'])
    core.dump('NON_REGRESSION.json',dict(status='PASS_STATIC_WITH_AUTHORIZED_HISTORICAL_GIT_DIFFERENCE' if passed else 'FAIL',suites=rows,current_workspace_HEAD=head,current_workspace_index_sha256=index,current_workspace_git_unchanged=head==baseline['git_head'] and index==baseline['git_index_sha256'],historical_git_commit_explicitly_authorized=head==authorized,old_raw_git_failures_retained=True,main_map_passed=sum(r['passed'] for r in main['checks']),main_map_checks=len(main['checks']),new_sublot_runtime_tested=False,automatic_engine_testing=False,bitmap_sha256=core.sha(core.ROOT/'map_data/provinces.png'),registry_sha256=core.sha(core.active_registry_path()),assistant_git_mutating_commands=[],territorial_completion='PARTIAL_REMAINING_SOVEREIGNTIES_OPEN'))
    # Enrich the per-RGB transfer list with explicit evidence, including retained
    # zero-zone fringes. No historical claim for unmodified allocations.
    geometry=json.loads((OUT/'GEOMETRY.json').read_text());tracing=json.loads((OUT/'TRACING.json').read_text());data=[]
    for r in geometry['assignments']:
        row={key:r[key] for key in ['rgb','parent_rgb','state','previous_owner','owner','pixels']}
        zone=r['source_zone'];row['territory']=tracing['polygons'][zone-1]['territory'] if zone else 'Unmodified unresolved fringe'
        row['historical_date']='1776-01-01';row['source']='Retained Schenk sheet + continuity references in REPORT.md' if zone else 'No new historical attribution';row['approximation']='Macro mainland envelope, not cadastral' if zone else 'Prior attribution retained, not certified'
        data.append(row)
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    report=json.loads((OUT/'VALIDATION.json').read_text())
    report['territorial_completion']='PARTIAL_REMAINING_SOVEREIGNTIES_OPEN'
    from map2l_runtime_receipt import annotate
    annotate(report,OUT.name)
    report['manual_runtime_status']=report.get('runtime_status','NOT_YET_TESTED')
    report['inherited_duplicate_RGB_count']=len(report['inherited_duplicate_RGBs']);report['inherited_reference_error_count']=len(report['inherited_reference_errors'])
    core.dump('VALIDATION.json',report)
    print(json.dumps(rows,ensure_ascii=False));print('Non-regression:',passed)

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'geometry':core.geometry,'prepare':core.prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps,'patch-parts':previous.preceding.patch_parts,'clean-new-whitespace':clean_new_whitespace,'summary':summary}[sys.argv[1]]()
