"""Bounded continuation after the user-validated Swabian cores."""
import csv,json,sys
from PIL import Image,ImageDraw,ImageFont,ImageColor
import numpy as np
import map2l_swabia as previous
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/SWABIA_CONTINUATION'
core.OUT=OUT
core.BACKUP=previous.OUT/'provinces_candidate.png'
core.REGIONS={'STATE_BADEN','STATE_WURTTEMBERG','STATE_BAVARIA','STATE_FRANCONIA'}
if hasattr(core,'PREPARE_EXTRA_FILES'):del core.PREPARE_EXTRA_FILES
previous.previous.previous.preceding.OUT=OUT
TAGS=['SFU','SEW']

def extra_files(files,migration):
    import re
    import validate_diplomacy_ottoman_1776 as parser
    baseline=json.loads((OUT/'BASELINE.json').read_text());assert not set(TAGS)&set(baseline['inventory']['countries'])
    defs='SFU = { color = { 238 146 105 } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = STATE_BADEN }\nSEW = { color = { 136 122 196 } country_type = recognized tier = principality cultures = { south_german } religion = catholic capital = STATE_FRANCONIA }\n'
    files['common/country_definitions/1776_map2l_swabia_continuation.txt']=defs
    replacement={'law_aor1776_imperial_customs':'law_aor1776_swabia_continuation_customs','law_aor1776_imperial_no_slavery':'law_aor1776_swabia_continuation_free_status'}
    source=(core.ROOT/'common/laws/1776_map2l_franconian_start_variants.txt').read_text(encoding='utf-8-sig');laws=[]
    for node in parser.parse(source):
        if node.key not in replacement:continue
        text=source[node.start:node.end]
        for old,new in replacement.items():text=text.replace(old,new)
        text=re.sub(r'OR = \{ c:ANS \?= this c:FBM \?= this c:WZB \?= this c:NUR \?= this c:EIC \?= this \}', 'OR = { c:SFU ?= this c:SEW ?= this }',text)
        assert not any('c:'+tag in text for tag in ['ANS','FBM','WZB','NUR','EIC']);laws.append(text)
    files['common/laws/1776_map2l_swabia_continuation.txt']='\n'.join(laws)+'\n'
    for tag,base in [('SFU','ANS'),('SEW','FBM')]:
        text=(core.ROOT/f'common/history/countries/{base.lower()} - franconian estate.txt').read_text(encoding='utf-8-sig').replace('c:'+base,'c:'+tag)
        for old,new in replacement.items():text=text.replace(old,new)
        files[f'common/history/countries/{tag.lower()} - swabia continuation.txt']=text
    files['common/history/characters/1776_map2l_swabia_continuation.txt']='''CHARACTERS = {
 c:SFU ?= { create_character = { first_name = aor1776_sfu_first last_name = aor1776_sfu_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1728.3.21 interest_group = ig_landowners ideology = ideology_traditionalist } }
 c:SEW ?= { create_character = { first_name = aor1776_sew_first last_name = aor1776_sew_last historical = yes culture = south_german religion = rel:catholic ruler = yes age = 64 interest_group = ig_devout ideology = ideology_traditionalist } }
}
'''
    governments=''
    for key,tag,law,power,title in [('furstenberg_principality','SFU','law_monarchy','hereditary','RULER_TITLE_PRINCE'),('ellwangen_provostry','SEW','law_theocracy','dictatorial','aor1776_prince_provost_title')]:
        female='RULER_TITLE_PRINCESS' if tag=='SFU' else 'aor1776_prince_provost_title'
        governments+='gov_aor1776_'+key+' = { transfer_of_power = '+power+' male_ruler = "'+title+'" female_ruler = "'+female+'" possible = { c:'+tag+' ?= this has_law = law_type:'+law+' } on_government_type_change = { change_to_'+power+' = yes } on_post_government_type_change = { post_change_to_'+power+' = yes } }\n'
    files['common/government_types/00_1776_map2l_swabia_continuation.txt']=governments
    coas='';flags=''
    for tag,ground,ink,emblem in [('SFU','white','blue','ce_eagle.dds'),('SEW','red','white','ce_cross_couped.dds')]:
        coas+='AOR1776_'+tag+' = { pattern = "pattern_solid.tga" color1 = '+ground+' colored_emblem = { texture = "'+emblem+'" color1 = '+ink+' instance = { position = { 0.5 0.5 } scale = { 0.65 0.65 } } } }\n'
        flags+=tag+' = { flag_definition = { coa = AOR1776_'+tag+' priority = 100 allow_overlord_canton = no } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2l_swabia_continuation.txt']=coas;files['common/flag_definitions/1776_map2l_swabia_continuation.txt']=flags
    names={'SFU':('Principality of Fürstenberg','Principauté de Fürstenberg'),'SFU_ADJ':('Fürstenbergian','Fürstenbergeois'),'SEW':('Prince-Provostry of Ellwangen','Prévôté princière d’Ellwangen'),'SEW_ADJ':('Ellwangenian','Ellwangeois'),'aor1776_sfu_first':('Joseph Wenzel','Joseph-Wenceslas'),'aor1776_sfu_last':('zu Fürstenberg','de Fürstenberg'),'aor1776_sew_first':('Anton Ignaz','Antoine-Ignace'),'aor1776_sew_last':('von Fugger-Glött','de Fugger-Glött'),'aor1776_prince_provost_title':('Prince-Provost','Prince-prévôt'),'gov_aor1776_furstenberg_principality':('Principality','Principauté'),'gov_aor1776_furstenberg_principality_desc':('An imperial prince rules the Fürstenberg possessions reunited in 1744, including territories separated by other imperial estates.','Le prince gouverne les possessions de Fürstenberg réunies en 1744, dont plusieurs domaines sont séparés par les terres d’autres États impériaux.'),'gov_aor1776_ellwangen_provostry':('Prince-provostry','Prévôté princière'),'gov_aor1776_ellwangen_provostry_desc':('The prince-provost governs the temporal estate of Ellwangen as an immediate imperial ruler. This territory is distinct from neighbouring free cities and princely domains.','Le prince-prévôt gouverne le domaine temporel d’Ellwangen en qualité de seigneur immédiat de l’Empire. Ses terres sont distinctes des villes libres et principautés voisines.'),'law_aor1776_swabia_continuation_customs':('Imperial estate customs','Douanes des États impériaux'),'law_aor1776_swabia_continuation_customs_desc':('Local regulated commerce at the 1776 start; no later technology is granted.','Commerce réglementé local au départ de 1776 ; aucune technologie tardive accordée.'),'law_aor1776_swabia_continuation_free_status':('Free legal status','Statut juridique libre'),'law_aor1776_swabia_continuation_free_status_desc':('Free legal status; tenancy and serfdom remain separate institutions.','Statut juridique libre ; le régime foncier et le servage restent des institutions distinctes.')}
    for lang,i in [('english',0),('french',1)]:files[f'localization/{lang}/1776_map2l_swabia_continuation_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+key+':0 "'+values[i]+'"\n' for key,values in names.items())
    migration.update(new_members=TAGS,free_cities=[],country_additions={n.key:core.qa.signature(n) for n in parser.parse(defs)})
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(core.ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)

core.PREPARE_EXTRA_FILES=extra_files

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    src=Image.open(previous.OUT/'HOMANN_SWABIA_3500.jpg').convert('RGB');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for name,box in [('NORTH',(1800,500,2950,1250)),('FURST',(650,1500,1650,2150)),('LAKE_DETAIL',(1500,1900,2300,2240))]:
        im=src.crop(box);d=ImageDraw.Draw(im)
        for x in range((box[0]//100+1)*100,box[2],100):
            d.line((x-box[0],0,x-box[0],im.height),fill='#4466cc');d.text((x-box[0]+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        for y in range((box[1]//100+1)*100,box[3],100):
            d.line((0,y-box[1],im.width,y-box[1]),fill='#4466cc');d.text((0,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
        im.save(OUT/(name+'_READING.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as f:
        core.dump('NATIVE_ANCHORS.json',[r for r in csv.DictReader(f) if r['State_ID'] in core.REGIONS])

def preview(bmp,rows,name):
    cfg=json.loads((OUT/'TRACING.json').read_text());x0,y0,x1,y1=cfg['preview_box'];local=bmp[y0:y1,x0:x1]
    colors={'BAD':'#dec459','WUR':'#72a46b','HOH':'#b6b6b6','HSG':'#6babb5','AUS':'#b3a6d8','SUU':'#e6dec4','SAG':'#d88892','SKE':'#a284b9','BAV':'#79afeb','KMZ':'#be5448','KPF':'#d7aa32','SWI':'#c97b73','SFU':'#ee9269','SEW':'#887ac4'}
    arr=np.full((*local.shape,3),225,dtype=np.uint8)
    for r in rows:arr[local==int(r['key'][0][1:],16)]=ImageColor.getrgb(colors.get(r['key'][2],'#ddd'))
    edge=np.zeros(local.shape,dtype=bool);edge[1:]|=local[1:]!=local[:-1];edge[:,1:]|=local[:,1:]!=local[:,:-1];arr[edge]=55
    im=Image.fromarray(arr).resize((local.shape[1]*12,local.shape[0]*12),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(im.width,im.height+55),'white');canvas.paste(im);d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    d.text((8,im.height+4),name+' | Swabia continuation: approximate jurisdiction cores, not cadastre',font=font,fill='black')
    d.text((8,im.height+28),'Furstenberg salmon / Ellwangen violet; previously restored estates preserved',font=font,fill='black');canvas.save(OUT/(name+'.png'))

core.preview=preview

def capture():
    receipt=core.ROOT/'docs/reports/map/MAP2L/CHECKPOINT_RHINE_SWABIA_USER_VALIDATED.json'
    assert receipt.exists() and json.loads(receipt.read_text())['status']=='PASS_REMOTE_EXACT_RESTORATION','Verify checkpoint before starting territorial changes'
    core.capture()

def intersections():
    """Bind explicitly drawn source envelopes to only uncorrected live parents."""
    from map2l_belgium import packed
    from map2l_franconia import inside
    b=json.loads((OUT/'BASELINE.json').read_text());cfg=json.loads((OUT/'TRACING.json').read_text());bmp=packed(core.ROOT/b['bitmap_backup']);matrix=np.array(cfg['calibrated_sources'][0]['matrix'])
    previous_geo=json.loads((previous.OUT/'GEOMETRY.json').read_text())
    protected={r['rgb'] for r in previous_geo['assignments'] if r['source_zone']}
    found=[]
    for row in b['inventory']['owners']:
        parent,sid,tag=row['key']
        if sid not in core.REGIONS or parent in protected or tag not in {'BAD','WUR','HOH','BAV'}:continue
        y,x=np.where(bmp==int(parent[1:],16));pts=(np.column_stack((x,y))+.5-matrix[2])@np.linalg.inv(matrix[:2])
        for i,p in enumerate(cfg['polygons']):
            take=inside(pts,p['points']);n=int(take.sum())
            if n:found.append(dict(polygon=i,territory=p['territory'],parent=parent,state=sid,owner=tag,pixels=n))
    core.dump('CANDIDATE_INTERSECTIONS.json',found)
    print(json.dumps(found,ensure_ascii=False,indent=2))

def imperial():
    old=json.loads((OUT/'IMPERIAL_FILES.json').read_text()) if (OUT/'IMPERIAL_FILES.json').exists() else {'files':[]}
    core.imperial();new=json.loads((OUT/'IMPERIAL_FILES.json').read_text());new['last_patch_files']=new['files'];new['files']=list(dict.fromkeys(old['files']+new['files']));core.dump('IMPERIAL_FILES.json',new)

def finish_whitespace():
    import difflib
    b=json.loads((OUT/'BASELINE.json').read_text());files={}
    for rel in ['common/history/states/00_states.txt','common/history/pops/00_west_europe.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']:
        before=b['originals'][rel].splitlines();raw=(core.ROOT/rel).read_text(encoding='utf-8-sig');lines=raw.splitlines()
        for tag,_,_,start,end in difflib.SequenceMatcher(None,before,lines,autojunk=False).get_opcodes():
            if tag in {'insert','replace'}:
                for i in range(start,end):lines[i]=lines[i].rstrip()
        cleaned='\n'.join(lines)+'\n'
        if cleaned!=raw:files[rel]=cleaned
    core.emit(files,'WHITESPACE.patch')

def summary():
    import subprocess
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION','SWABIA','SWABIA_CONTINUATION']
    allowed={'No commit or staging mutation','HEAD and Git index unchanged','Git HEAD and index unchanged'};rows=[]
    for name in names:
        report=json.loads((OUT.parent/name/'VALIDATION.json').read_text());failed=[r['name'] for r in report['checks'] if not r['passed']]
        rows.append(dict(lot=name,raw_status=report['status'],passed=sum(r['passed'] for r in report['checks']),checks=len(report['checks']),failed=failed,data_checks_passed=not(set(failed)-allowed),manual_runtime_status=report.get('runtime_status','NOT_YET_TESTED'),automatic_engine_test=False))
    b=json.loads((OUT/'BASELINE.json').read_text());head=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=core.ROOT,text=True).strip();index=core.sha(core.ROOT/'.git/index');main=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text());authorized=json.loads((OUT.parent/'RHINE_WESTPHALIA/AUTHORIZED_GIT_EVENT.json').read_text())['authorized_head']
    ok=all(r['data_checks_passed'] for r in rows) and head==b['git_head']==authorized and index==b['git_index_sha256'] and all(r['passed'] for r in main['checks'])
    core.dump('NON_REGRESSION.json',dict(status='PASS_STATIC_WITH_AUTHORIZED_HISTORICAL_GIT_DIFFERENCE' if ok else 'FAIL',suites=rows,HEAD=head,index_sha256=index,git_unchanged=head==b['git_head'] and index==b['git_index_sha256'],old_raw_git_failures_retained=True,automatic_engine_testing=False,new_sublot_runtime_status='NOT_YET_TESTED',prior_runtime_receipt='RUNTIME_USER_VALIDATION_RHINE_SWABIA.json',bitmap_sha256=core.sha(core.ROOT/'map_data/provinces.png'),registry_sha256=core.sha(core.active_registry_path()),main_map_checks=sum(r['passed'] for r in main['checks'])))
    g=json.loads((OUT/'GEOMETRY.json').read_text());cfg=json.loads((OUT/'TRACING.json').read_text());records=[]
    for r in g['assignments']:
        row={k:r[k] for k in ['rgb','parent_rgb','state','previous_owner','owner','pixels']};zone=r['source_zone'];row['territory']=cfg['polygons'][zone-1]['territory'] if zone else 'Provisional fringe retained, not certified';row['historical_date']='1776-01-01';row['approximation']='Conservative game-scale envelope, not cadastre' if zone else 'Unmodified attribution, no new historical claim';records.append(row)
    with (OUT/'TERRITORIAL_CHANGES.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    report=json.loads((OUT/'VALIDATION.json').read_text());report.update(runtime_status='NOT_YET_TESTED',territorial_completion='PARTIAL_REMAINING_JURISDICTIONS_OPEN',checkpoint='Prior validated version only; this continuation not pushed',inherited_duplicate_RGB_count=len(report['inherited_duplicate_RGBs']),inherited_reference_error_count=len(report['inherited_reference_errors']));core.dump('VALIDATION.json',report)
    print(json.dumps(rows,ensure_ascii=False));print('Cumulative data checks:',ok)

if __name__=='__main__':
    {'capture':capture,'inspect':inspect,'intersections':intersections,'geometry':core.geometry,'prepare':core.prepare,'install':core.install,'imperial':imperial,'maps':core.maps,'patch-parts':previous.previous.previous.preceding.patch_parts,'finish-whitespace':finish_whitespace,'summary':summary}[sys.argv[1]]()
