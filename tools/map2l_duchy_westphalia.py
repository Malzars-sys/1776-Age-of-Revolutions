"""Cologne's Westphalian duchy: bounded continuation, no other MAP sector."""
import csv
import json
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
import map2l_minden_ravensberg as preceding
import map2l_mainz as core

OUT=core.ROOT/'docs/reports/map/MAP2L/DUCHY_WESTPHALIA'
core.OUT=OUT
core.BACKUP=OUT.parent/'MINDEN_RAVENSBERG/provinces_candidate.png'
core.REGIONS={'STATE_WESTPHALIA','STATE_RUHR'}
preceding.OUT=OUT

def inspect():
    OUT.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for source,stem,crops in [
        (OUT.parent/'RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg','VAUGONDY',[
            ('ARNSBERG',(1120,285,1360,415)),('BRILON',(1400,230,1560,345)),
            ('SIEGEN',(1200,620,1360,750)),('COLOGNE',(710,550,840,640)),
            ('BONN',(735,710,870,820)),('DUSSELDORF',(600,390,740,480)),('SAUERLAND',(1080,170,1660,710)),('VEST',(680,100,1110,245))]),
        (OUT.parent/'RHINE_WESTPHALIA/SCHENK_WESTPHALIA_1710_FULL.jpg','SCHENK',[
            ('ARNSBERG',(1330,1790,1510,1920)),('BRILON',(1610,1670,1790,1840)),
            ('SIEGEN',(1390,2070,1610,2220)),('SAUERLAND',(1420,1700,1978,2140))])]:
        image=Image.open(source).convert('RGB')
        for name,box in crops:
            crop=image.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3))
            draw=ImageDraw.Draw(crop)
            for x in range((box[0]//20+1)*20,box[2],20):
                draw.line(((x-box[0])*3,0,(x-box[0])*3,crop.height),fill='#5577e0')
                draw.text(((x-box[0])*3+2,0),str(x),font=font,fill='blue',stroke_width=1,stroke_fill='white')
            for y in range((box[1]//20+1)*20,box[3],20):
                draw.line((0,(y-box[1])*3,crop.width,(y-box[1])*3),fill='#5577e0')
                draw.text((0,(y-box[1])*3+2),str(y),font=font,fill='blue',stroke_width=1,stroke_fill='white')
            crop.save(OUT/(stem+'_'+name+'.png'))
    with (core.ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv').open(encoding='utf-8-sig',newline='') as stream:
        anchors=[r for r in csv.DictReader(stream) if r['State_ID'] in core.REGIONS]
    core.dump('NATIVE_ANCHORS.json',anchors)
    image=Image.open(OUT.parent/'RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg').convert('RGB')
    for name,box in [('RHINE_CLEAN',(420,70,920,850)),('SAUERLAND_CLEAN',(1080,170,1660,710))]:
        image.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2)).save(OUT/(name+'.png'))

core.preview=preceding.preview

def geometry():
    core.geometry()
    result=json.loads((OUT/'GEOMETRY.json').read_text())
    result['status']='SOURCE_TRACED_COLOGNE_WESTPHALIAN_CORES_GAME_SCALE'
    core.dump('GEOMETRY.json',result)

def summary():
    names=['BELGIUM','PIEDMONT','FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA']
    git_checks={'No commit or staging mutation','HEAD and Git index unchanged','Git HEAD and index unchanged'}
    rows=[]
    for name in names:
        report=json.loads((OUT.parent/name/'VALIDATION.json').read_text())
        failed=[row['name'] for row in report['checks'] if not row['passed']]
        rows.append(dict(lot=name,raw_status=report['status'],passed=sum(bool(row['passed']) for row in report['checks']),checks=len(report['checks']),failed=failed,gameplay_static_checks_passed=not(set(failed)-git_checks),manual_runtime_status=report.get('runtime_status'),automated_engine_test=False))
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    authorization=json.loads((OUT.parent/'RHINE_WESTPHALIA/AUTHORIZED_GIT_EVENT.json').read_text())
    head=subprocess.check_output([core.GIT,'rev-parse','HEAD'],cwd=core.ROOT,text=True).strip()
    index=core.sha(core.ROOT/'.git/index')
    unchanged=head==baseline['git_head'] and index==baseline['git_index_sha256']
    authorized=head==authorization['authorized_head']
    main=json.loads((OUT/'MAIN_MAP/VALIDATION.json').read_text())
    map_ok=all(r['passed'] for r in main['checks']) and main['registry_sha256']==core.sha(core.active_registry_path())
    result=dict(status='PASS_STATIC_WITH_AUTHORIZED_HISTORICAL_GIT_DIFFERENCE' if all(r['gameplay_static_checks_passed'] for r in rows) and unchanged and authorized and map_ok else 'FAIL',suites=rows,current_workspace_HEAD=head,current_workspace_index_sha256=index,current_workspace_git_unchanged=unchanged,historical_git_commit_explicitly_authorized=authorized,old_raw_git_failures_retained=True,main_map_passed=sum(r['passed'] for r in main['checks']),main_map_checks=len(main['checks']),new_sublot_runtime_tested=False,automatic_engine_testing=False,manual_scope_receipt='../RUNTIME_USER_VALIDATION.json',bitmap_sha256=core.sha(core.ROOT/'map_data/provinces.png'),registry_sha256=core.sha(core.active_registry_path()),assistant_git_mutating_commands=[])
    core.dump('NON_REGRESSION.json',result)
    print(result['status']);print(json.dumps(rows,ensure_ascii=False))

if __name__=='__main__':
    {'capture':core.capture,'inspect':inspect,'geometry':geometry,'prepare':core.prepare,'install':core.install,'imperial':core.imperial,'maps':core.maps,'patch-parts':preceding.patch_parts,'summary':summary}[sys.argv[1]]()
