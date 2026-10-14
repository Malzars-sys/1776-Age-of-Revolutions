"""Bounded Rhine/Westphalia implementation using retained map evidence.

Immutable source stage; no projection refitting of Erfurt or earlier Mainz lots.
Runtime text changes are emitted as apply_patch payloads, not installed silently.
"""
import csv
import json
import re
import difflib
import subprocess
import sys
import urllib.request
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageColor
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/RHINE_WESTPHALIA'
core.OUT=OUT
core.BACKUP=OUT.parent/'FRANCONIA_CONTINUATION/provinces_candidate.png'
core.REGIONS={'STATE_NORTH_RHINE','STATE_RUHR','STATE_WESTPHALIA'}

def extra_files(files,migration):
    """Two distinct continuing ecclesiastical estates, no elective titles added."""
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    assert not {'WPM','WPD'}&set(baseline['inventory']['countries'])
    import validate_diplomacy_ottoman_1776 as parser
    definitions=('WPM = { color = { 135 180 104 } country_type = recognized tier = principality cultures = { north_german } religion = catholic capital = STATE_WESTPHALIA }\n'
                 'WPD = { color = { 224 144 112 } country_type = recognized tier = principality cultures = { north_german } religion = catholic capital = STATE_WESTPHALIA }\n')
    files['common/country_definitions/1776_map2l_westphalian_estates.txt']=definitions
    template=(core.ROOT/'common/history/countries/fbm - franconian estate.txt').read_text(encoding='utf-8-sig')
    for tag in ['WPM','WPD']:
        files['common/history/countries/'+tag.lower()+' - westphalian estate.txt']=template.replace('c:FBM','c:'+tag).replace('law_aor1776_imperial_customs','law_aor1776_westphalian_customs').replace('law_aor1776_imperial_no_slavery','law_aor1776_westphalian_free_status')
    # Same early-modern legal mechanism as the existing Franconian countries,
    # but independent scope: existing laws and governments are not edited.
    source=(core.ROOT/'common/laws/1776_map2l_franconian_start_variants.txt').read_text(encoding='utf-8-sig')
    laws=[]
    for node in parser.parse(source):
        if node.key not in {'law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery'}:continue
        text=source[node.start:node.end]
        text=text.replace('law_aor1776_imperial_customs','law_aor1776_westphalian_customs').replace('law_aor1776_imperial_no_slavery','law_aor1776_westphalian_free_status')
        text=re.sub(r'OR = \{ c:ANS \?= this c:FBM \?= this c:WZB \?= this c:NUR \?= this c:EIC \?= this \}', 'OR = { c:WPM ?= this c:WPD ?= this }',text)
        assert 'c:FBM' not in text
        laws.append(text)
    files['common/laws/1776_map2l_westphalian_start_variants.txt']='\n'.join(laws)+'\n'
    files['common/history/characters/1776_map2l_westphalian_rulers.txt']='''CHARACTERS = {
c:WPM ?= { create_character = { first_name = aor1776_wpm_first last_name = aor1776_wpm_last historical = yes culture = north_german religion = rel:catholic ruler = yes age = 67 interest_group = ig_devout ideology = ideology_traditionalist } }
c:WPD ?= { create_character = { first_name = aor1776_wpd_first last_name = aor1776_wpd_last historical = yes culture = north_german religion = rel:catholic ruler = yes age = 68 interest_group = ig_devout ideology = ideology_traditionalist } }
}
'''
    files['common/coat_of_arms/coat_of_arms/1776_map2l_westphalian_flags.txt']='''AOR1776_WPM = { pattern = "pattern_solid.tga" color1 = yellow colored_emblem = { texture = "ce_cross_couped.dds" color1 = red instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }
AOR1776_WPD = { pattern = "pattern_solid.tga" color1 = red colored_emblem = { texture = "ce_cross_couped.dds" color1 = yellow instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }
'''
    files['common/flag_definitions/1776_map2l_westphalian_flags.txt']='WPM = { flag_definition = { coa = AOR1776_WPM priority = 100 allow_overlord_canton = no } }\nWPD = { flag_definition = { coa = AOR1776_WPD priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['english','french']:
        names={'WPM':('Prince-Bishopric of Munster','Principauté épiscopale de Münster'),'WPD':('Prince-Bishopric of Paderborn','Principauté épiscopale de Paderborn'),'WPM_ADJ':('Munsterian','Münstérois'),'WPD_ADJ':('Paderbornian','Paderbornois'),
               'aor1776_wpm_first':('Maximilian Friedrich','Maximilian Friedrich'),'aor1776_wpm_last':('von Koenigsegg-Rothenfels','von Königsegg-Rothenfels'),'aor1776_wpd_first':('Wilhelm Anton','Wilhelm Anton'),'aor1776_wpd_last':('von der Asseburg','von der Asseburg'),
               'law_aor1776_westphalian_customs':('Early-modern episcopal customs','Douanes épiscopales d’Ancien Régime'),'law_aor1776_westphalian_free_status':('Free status in the episcopal estates','Statut libre dans les principautés épiscopales'),
               'law_aor1776_westphalian_customs_desc':('Local regulated commerce; no later technology is granted.','Commerce local réglementé ; aucune technologie tardive n’est accordée.'),'law_aor1776_westphalian_free_status_desc':('Starting free legal status; serfdom is handled separately.','Statut juridique libre de départ ; le servage est traité séparément.')}
        i=0 if lang=='english' else 1
        files['localization/'+lang+'/1776_map2l_westphalia_l_'+lang+'.yml']='\ufeffl_'+lang+':\n'+''.join(' '+key+':0 "'+value[i]+'"\n' for key,value in names.items())
    migration['new_members']=['WPM','WPD']
    migration['country_additions']={n.key:core.qa.signature(n) for n in parser.parse(definitions)}
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

core.PREPARE_EXTRA_FILES=extra_files

def compact_imperial_patch():
    """Keep every edit; reduce generated unchanged context to three lines.

    apply_patch still applies all runtime text changes explicitly. This avoids
    transporting large unchanged province tables through the tool output.
    """
    lines=(OUT/'IMPERIAL.patch').read_text(encoding='utf-8').splitlines()
    result=['*** Begin Patch'];section=[];header=[''];pieces=[];pending=[]
    def save_piece():
        if pending:
            pieces.append('*** Begin Patch\n'+header[0]+'\n'+'\n'.join(pending)+'\n*** End Patch\n')
            pending.clear()
    def flush():
        if not section:return
        changes=[i for i,line in enumerate(section) if line.startswith(('+','-'))]
        windows=[]
        for index in changes:
            start=max(0,index-3);end=min(len(section),index+4)
            if windows and start<=windows[-1][1]:windows[-1][1]=max(windows[-1][1],end)
            else:windows.append([start,end])
        for start,end in windows:
            if header[0].endswith('1776_imperial_voting.txt'):
                # Identical button closing lines cannot locate a pure insertion
                # uniquely: retain its preceding named button header as well.
                for index in range(start-1,-1,-1):
                    if section[index].startswith(' aor1776_hre_vote_'):
                        start=index;break
            body=['@@',*section[start:end]]
            if pending and sum(len(line)+1 for line in pending+body)>18000:save_piece()
            pending.extend(body);result.extend(body)
        section.clear()
    for line in lines[1:]:
        if line.startswith('*** Update File:'):
            flush();save_piece();header[0]=line;result.append(line)
        elif line.startswith('@@'):flush()
        elif line=='*** End Patch':flush()
        else:section.append(line)
    result.append('*** End Patch')
    save_piece();core.dump('IMPERIAL_PARTS.json',pieces)
    text='\n'.join(result)+'\n';(OUT/'IMPERIAL_COMPACT.patch').write_text(text,encoding='utf-8')
    original_signed=[line for line in lines if line.startswith(('+','-'))]
    compact_signed=[line for line in result if line.startswith(('+','-'))]
    assert original_signed==compact_signed,'Patch edits must not change during compaction'
    print('All signed edits retained; compact patch characters:',len(text),'parts:',len(pieces),'largest:',max(map(len,pieces)))

def clean_new_whitespace():
    """Emit cleanup of newly inserted whitespace only, never whole-file trim."""
    baseline=json.loads((OUT/'BASELINE.json').read_text());files={}
    for rel in ['common/history/states/00_states.txt','common/history/pops/00_west_europe.txt']:
        before=baseline['originals'][rel].splitlines()
        text=(core.ROOT/rel).read_text(encoding='utf-8-sig');lines=text.splitlines()
        for tag,_,_,start,end in difflib.SequenceMatcher(None,before,lines,autojunk=False).get_opcodes():
            if tag in {'insert','replace'}:
                for index in range(start,end):lines[index]=lines[index].rstrip()
        cleaned='\n'.join(lines)+'\n'
        if cleaned!=text:files[rel]=cleaned
    print('New whitespace cleanup patch:',core.emit(files,'WHITESPACE.patch'))

def summary():
    """Keep raw failed Git attestation; separate it from gameplay checks."""
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA']
    rows=[]
    for name in names:
        report=json.loads((OUT.parent/name/'VALIDATION.json').read_text())
        failed=[row['name'] for row in report['checks'] if not row['passed']]
        git_only=all(re.search(r'HEAD|commit or staging',name,re.I) for name in failed)
        rows.append(dict(lot=name,raw_status=report['status'],passed=sum(bool(row['passed']) for row in report['checks']),checks=len(report['checks']),failed=failed,gameplay_checks_passed=git_only,engine_tested=report['engine_tested']))
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    head=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=core.ROOT,text=True).strip()
    parent=subprocess.check_output([core.GIT,'rev-parse','HEAD^'],cwd=core.ROOT,text=True).strip()
    git=dict(baseline_head=baseline['git_head'],current_head=head,current_parent=parent,
             baseline_index_sha256=baseline['git_index_sha256'],current_index_sha256=core.sha(core.ROOT/'.git/index'),
             observed_last_commit=subprocess.check_output([core.GIT,'show','-s','--format=%H%n%an%n%aI%n%s','HEAD'],cwd=core.ROOT,text=True).splitlines(),
             assistant_git_mutating_commands_run=[],warning='HEAD/index changed outside this workflow. Baselines were not rewritten and raw attestation failures are retained.')
    main=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text())
    core.dump('NON_REGRESSION.json',dict(status='PASS_GAMEPLAY_STATIC_EXTERNAL_GIT_ACTIVITY_ENGINE_PENDING' if all(row['gameplay_checks_passed'] for row in rows) and all(row['passed'] for row in main['checks']) else 'FAIL_GAMEPLAY_CHECK',
        suites=rows,git_activity=git,main_map_checks_passed=sum(row['passed'] for row in main['checks']),main_map_checks=len(main['checks']),
        bitmap_sha256=core.sha(core.ROOT/'map_data/provinces.png'),registry_sha256=core.sha(core.active_registry_path()),engine_tested=False))
    print(json.dumps(rows,ensure_ascii=False));print('Observed external Git head:',head)

def fetch_westphalian_source():
    # One bounded supplement to the already identified R2 atlas evidence.
    # LWL also reproduces this exact period map on its 1648-1770 history page.
    original='original' in sys.argv[2:]
    target=OUT/('SCHENK_WESTPHALIA_1710_FULL.jpg' if original else 'LWL_WESTPHALIAN_CIRCLE_1710.jpg')
    assert not target.exists(),'Retained sources must not be overwritten'
    url=('https://upload.wikimedia.org/wikipedia/commons/5/5b/Reichskreis_Niederrhein-Westfalen_1710.jpg' if original
         else 'https://www.lwl.org/westfaelische-geschichte/kar/normal/kar51.jpg')
    request=urllib.request.Request(url,headers={'User-Agent':'HistoricalMapResearch/1.0'})
    with urllib.request.urlopen(request,timeout=25) as response:raw=response.read(12_000_001)
    assert len(raw)<=12_000_000
    import io
    Image.open(io.BytesIO(raw)).verify();target.write_bytes(raw)
    core.dump(target.stem+'.SOURCE.json',dict(url=url,sha256=core.sha(target),
        institution='Landschaftsverband Westfalen-Lippe / Internet-Portal Westfaelische Geschichte',
        context='https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=33&url_tabelle=tab_websegmente',
        historical_date='1710/1730 (portal caption); Schenk map',size=list(Image.open(target).size),
        use='Macro-jurisdiction comparison with retained 1780 R2 atlas and continuing authority in 1776; not automatic 1710 sovereignty',
        limitations='Exclude post-1710 Gueldre acquisitions and every uncorroborated border mutation. No exact cadastral claim.'))
    print(target.name,Image.open(target).size)

def source_crops():
    image=Image.open(OUT/'SCHENK_WESTPHALIA_1710_FULL.jpg').convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for name,box in [('SCHENK_SOUTH',(150,1310,1800,2370)),('SCHENK_CENTRE',(620,700,1960,1670)),('SCHENK_PADERBORN',(1280,1370,1978,2190)),('SCHENK_RHINE_CITIES',(190,1790,1030,2400))]:
        crop=image.crop(box);draw=ImageDraw.Draw(crop)
        for x in range((box[0]//100+1)*100,box[2],100):
            draw.line((x-box[0],0,x-box[0],crop.height),fill='#5599e9');draw.text((x-box[0]+1,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            draw.line((0,y-box[1],crop.width,y-box[1]),fill='#5599e9');draw.text((0,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'.png'))
    for name,box in [('PAD_TOWN',(1460,1470,1680,1670)),('RHINE_TOWNS',(420,1880,820,2320))]:
        crop=image.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3));draw=ImageDraw.Draw(crop)
        for x in range((box[0]//20+1)*20,box[2],20):
            draw.line(((x-box[0])*3,0,(x-box[0])*3,crop.height),fill='#5599e9');draw.text(((x-box[0])*3,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//20+1)*20,box[3],20):
            draw.line((0,(y-box[1])*3,crop.width,(y-box[1])*3),fill='#5599e9');draw.text((0,(y-box[1])*3),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'.png'))

def inspect():
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as stream:
        anchors=[row for row in csv.DictReader(stream) if row['State_ID'] in core.REGIONS|{'STATE_HANNOVER','STATE_HESSE','STATE_GELRE','STATE_RHINELAND'}]
    core.dump('NATIVE_ANCHORS.json',anchors)
    print(json.dumps([{k:row[k] for k in ['State_ID','Hub_Type','Hub_Name','Locator_X','Locator_Y','Locator_Sampled_RGB']} for row in anchors],ensure_ascii=False))
    source=OUT.parent/'RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg'
    image=Image.open(source).convert('RGB')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for name,box in [('VAUGONDY_NORTH',(440,70,1690,880))]:
        crop=image.crop(box);draw=ImageDraw.Draw(crop)
        for x in range((box[0]//50+1)*50,box[2],50):
            draw.line((x-box[0],0,x-box[0],crop.height),fill='#618fee');draw.text((x-box[0]+1,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//50+1)*50,box[3],50):
            draw.line((0,y-box[1],crop.width,y-box[1]),fill='#618fee');draw.text((0,y-box[1]+1),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        crop.save(OUT/(name+'.png'))

def preview(bmp,rows,name):
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1]
    owners={int(r['key'][0][1:],16):r['key'][2] for r in rows}
    tags=np.array([owners.get(int(value),'?') for value in local.ravel()]).reshape(local.shape)
    colors={'PRU':'#609ab6','KPF':'#d7aa32','KCL':'#737db9','WPM':'#87b468','WPD':'#e09070','LIP':'#bb8aab','SCM':'#dec588','HAN':'#bbc0b2','NAS':'#df9468','BEO':'#d4bf97','LGE':'#bd6389','STM':'#6bac78','NET':'#d8945d'}
    arr=np.full((*local.shape,3),220,dtype=np.uint8)
    for tag,color in colors.items():arr[tags==tag]=ImageColor.getrgb(color)
    scale=8;image=Image.fromarray(arr).resize((local.shape[1]*scale,local.shape[0]*scale),Image.Resampling.NEAREST);draw=ImageDraw.Draw(image)
    for y,x in zip(*np.where(tags[1:]!=tags[:-1])):draw.line((x*scale,(y+1)*scale,(x+1)*scale,(y+1)*scale),fill='#282828',width=1)
    for y,x in zip(*np.where(tags[:,1:]!=tags[:,:-1])):draw.line(((x+1)*scale,y*scale,(x+1)*scale,(y+1)*scale),fill='#282828',width=1)
    canvas=Image.new('RGB',(image.width,image.height+70),'white');canvas.paste(image)
    draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    draw.text((8,image.height+4),name+' | Rhin-Westphalie: retained sources / game-scale approximation',font=font,fill='black')
    draw.text((8,image.height+25),'Prusse bleu / Palatinat or / Cologne violet / Munster vert / Paderborn saumon',font=font,fill='black')
    draw.text((8,image.height+46),'No cadastral or sub-two-pixel precision claimed.',font=font,fill='black')
    canvas.save(OUT/(name+'.png'))

core.preview=preview

def geometry():
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    assert core.sha(core.ROOT/'map_data/provinces.png')==baseline['bitmap_sha256'],'Geometry must be staged before installation, never recut the live result'
    core.geometry()
    result=json.loads((OUT/'GEOMETRY.json').read_text())
    result['status']='SOURCE_TRACED_RHINE_WESTPHALIA_GAME_SCALE_APPROXIMATION'
    core.dump('GEOMETRY.json',result)

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'fetch-westphalian-source':fetch_westphalian_source,'source-crops':source_crops,'geometry':geometry,'prepare':core.prepare,'compact-imperial':compact_imperial_patch,'clean-new-whitespace':clean_new_whitespace,'summary':summary,
     'install':core.install,'imperial':core.imperial,'maps':core.maps}[sys.argv[1]]()
