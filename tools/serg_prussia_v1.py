"""Scoped Prussia V1 work, based on the actual workspace; no Git mutations."""
from pathlib import Path
import collections
import hashlib
import json
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective, values
from map2l_belgium import packed, components

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reports/map/SERG_CLOSURE/PRUSSIA_V1_2026_11_02'
CANON = OUT.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def runtime_hashes():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for folder in ('common', 'events', 'map_data', 'gfx', 'localization')
            for p in (ROOT / folder).rglob('*') if p.is_file()}


def capture():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'BASELINE.json').exists(), 'Never overwrite a captured baseline'
    inv = qa.inventory()
    import serg_closure_roadmap as roadmap
    state = roadmap.load_json(CANON / 'ROADMAP_STATE.json')
    git = {}
    for label, args in [('head', ['rev-parse', 'HEAD']), ('branch', ['branch', '--show-current']),
                        ('git_dir', ['rev-parse', '--absolute-git-dir']), ('status', ['status', '--porcelain=v1'])]:
        p = subprocess.run(['git', '--no-optional-locks', *args], cwd=ROOT, capture_output=True, text=True)
        git[label] = dict(returncode=p.returncode, output=p.stdout.strip(), stderr=p.stderr.strip())
    gd = Path(git['git_dir']['output'])
    git['index_sha256'] = sha(gd / 'index')
    dump('BASELINE.json', dict(runtime=runtime_hashes(), inventory=inv, git=git,
         canonical_check=roadmap.check(), progress=roadmap.progress(state),
         canonical_hashes={p.name: sha(p) for p in CANON.glob('*') if p.is_file()},
         archived_proofs={p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / 'docs/reports/map').rglob('*')
                          if p.is_file() and OUT not in p.parents and CANON not in p.parents}))
    (OUT / 'ROADMAP_STATE_BEFORE.json').write_bytes((CANON / 'ROADMAP_STATE.json').read_bytes())
    print(json.dumps(dict(progress=roadmap.progress(state), runtime_files=len(runtime_hashes()),
                          canonical=roadmap.check()['status']), ensure_ascii=False))


def inspect():
    inv = qa.inventory()
    owners = {r['key'][0]: r['key'][2] for r in inv['owners']}
    bmp = packed(ROOT / 'map_data/provinces.png')
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    palette = {'PRU': '#769bc2', 'SAX': '#96ba70', 'PLC': '#dfa2b1', 'AUS': '#dfc788',
               'ANH': '#d38b56', 'SWE': '#e8d55f', 'BRA': '#a5a167', 'HAN': '#bc985c',
               'MST': '#bc82b6', 'MEC': '#ad78a5', 'NET': '#d9a365', 'KPF': '#a278b4'}
    for name, box, scale in [('SILESIA', (4370, 790, 4500, 900), 9),
                             ('PRUSSIA_EAST', (4340, 670, 4660, 880), 5),
                             ('PRUSSIA_WEST', (4210, 730, 4330, 850), 8)]:
        x0, y0, x1, y1 = box
        local = bmp[y0:y1, x0:x1]
        a = np.full((*local.shape, 3), 235, dtype=np.uint8)
        for val in np.unique(local):
            key = 'x' + format(int(val), '06X')
            color = palette.get(owners.get(key), '#cfc9be')
            a[local == val] = tuple(bytes.fromhex(color[1:]))
        im = Image.fromarray(a).resize(((x1-x0)*scale, (y1-y0)*scale), Image.Resampling.NEAREST)
        d = ImageDraw.Draw(im)
        # Province labels are technical references, not historical city placements.
        for val in np.unique(local):
            key = 'x' + format(int(val), '06X')
            ys, xs = np.where(local == val)
            if key not in owners or len(xs) < 20:
                continue
            d.text((int(np.mean(xs)*scale), int(np.mean(ys)*scale)), key[1:]+' '+owners[key],
                   font=font, fill='black', stroke_width=1, stroke_fill='white')
        im.save(OUT / (name + '_CURRENT.png'))
    rows = []
    for row in inv['owners']:
        rgb, sid, owner = row['key']
        if owner != 'PRU' and sid != 'STATE_LOWER_SILESIA':
            continue
        ys, xs = np.where(bmp == int(rgb[1:], 16))
        rows.append(dict(rgb=rgb, state=sid, owner=owner, pixels=len(xs),
                         box=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None))
    dump('PRUSSIAN_INVENTORY_CURRENT.json', rows)
    for r in rows:
        if r['state'] in ('STATE_LOWER_SILESIA', 'STATE_BRANDENBURG', 'STATE_ANHALT', 'STATE_BRUNSWICK'):
            print(r)


def source_grids():
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    for name in ('UPPER_1758', 'LOWER'):
        im = Image.open(OUT / 'EVIDENCE' / (name + '.jpg')).convert('RGB').resize((1500, 1432 if name == 'UPPER_1758' else 1400))
        d = ImageDraw.Draw(im)
        for x in range(0, im.width, 100):
            d.line((x, 0, x, im.height), fill='#385bc2')
            d.text((x+3, 50), str(x), font=font, fill='blue', stroke_width=2, stroke_fill='white')
        for y in range(0, im.height, 100):
            d.line((0, y, im.width, y), fill='#385bc2')
            d.text((30, y+3), str(y), font=font, fill='blue', stroke_width=2, stroke_fill='white')
        im.save(OUT / (name + '_GRID.jpg'))


def geometry():
    """Read political outlines on two primary sheets; retain native-model uncertainty."""
    from georeference.model import forward
    from map2l_franconia import inside
    b = json.loads((OUT / 'BASELINE.json').read_text(encoding='utf-8'))
    assert runtime_hashes() == b['runtime'], 'Reassess any concurrent functional change'
    bmp = packed(ROOT / 'map_data/provinces.png')
    (OUT / 'provinces_before.png').write_bytes((ROOT / 'map_data/provinces.png').read_bytes())
    model = json.loads((ROOT / 'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    # Approximate hand readings on the 1500-wide review copies. No native fit,
    # no optimization of old controls, and no historical precision claim.
    sheets = {
      'UPPER_1758': dict(
        controls=[('Bautzen',725,659,14.423,51.182),('Gorlitz',1096,667,14.989,51.157),
                  ('Lauban',1311,712,15.289,51.119),('Hoyerswerda',622,352,14.252,51.437),
                  ('Zittau',1000,1007,14.807,50.898)],
        checks=[('Spremberg',702,250,14.377,51.571),('Lobau',880,774,14.667,51.096)],
        outline=[(171,300),(333,291),(430,320),(495,338),(538,311),(568,279),(586,255),(635,252),(691,267),(724,253),(744,290),(779,352),(808,409),(837,433),(868,415),(901,420),(924,433),(955,417),(989,416),(1003,359),(1000,304),(1011,275),(1038,267),(1049,229),(1100,231),(1140,219),(1192,244),(1208,271),(1223,315),(1257,358),(1264,402),(1295,411),(1323,401),(1344,412),(1342,471),(1351,491),(1347,537),(1376,561),(1378,588),(1339,596),(1377,607),(1387,642),(1380,678),(1376,700),(1330,713),(1320,754),(1327,818),(1295,852),(1270,871),(1235,850),(1208,881),(1201,915),(1170,940),(1153,977),(1118,1024),(1127,1070),(1098,1094),(1025,1094),(983,1080),(948,1088),(889,1063),(865,1005),(832,975),(843,923),(818,904),(822,877),(792,875),(758,865),(751,837),(735,833),(737,795),(754,774),(780,770),(800,742),(839,745),(861,731),(871,680),(886,660),(877,630),(855,616),(834,617),(808,624),(762,664),(742,667),(712,713),(688,740),(659,744),(633,764),(622,800),(609,818),(583,813),(576,789),(607,741),(613,697),(636,675),(632,622),(609,610),(574,671),(530,690),(437,700),(389,706),(371,725),(300,697),(277,664),(270,646),(239,628),(209,600),(219,573),(234,529),(227,520),(241,503),(250,441),(240,408),(218,390),(167,370),(160,342)]),
      'LOWER': dict(
        controls=[('Lubben',433,476,13.895,51.942),('Luckau',274,583,13.717,51.852),
                  ('Guben',1032,615,14.715,51.953),('Calau',420,724,13.953,51.746),
                  ('Sorau',1272,948,15.138,51.642),('Spremberg',692,1077,14.377,51.571)],
        checks=[('Cottbus',673,758,14.334,51.760),('Peitz',774,667,14.412,51.858),('Forst',918,837,14.645,51.744)],
        outline=[(441,324),(494,333),(614,325),(650,297),(688,328),(714,352),(736,351),(755,329),(792,329),(817,280),(818,216),(902,211),(906,300),(909,340),(898,412),(885,429),(875,495),(881,552),(957,567),(1022,550),(1089,548),(1134,522),(1175,537),(1206,541),(1220,529),(1235,539),(1287,549),(1328,550),(1334,611),(1351,667),(1354,758),(1376,822),(1373,952),(1359,1012),(1325,1081),(1292,1094),(1188,1113),(1132,1097),(1059,1104),(996,1091),(943,1088),(910,1108),(876,1094),(835,1104),(789,1101),(767,1076),(732,1083),(709,1106),(660,1098),(625,1102),(615,1088),(578,1083),(552,1097),(532,1105),(500,1099),(490,1107),(468,1107),(433,1104),(402,1106),(382,1121),(348,1119),(325,1126),(292,1113),(249,1115),(225,1109),(197,1120),(161,1120),(143,1101),(125,1095),(120,971),(147,914),(174,888),(174,855),(171,835),(194,807),(192,766),(187,729),(207,704),(200,672),(195,650),(210,632),(213,613),(174,602),(156,594),(156,551),(159,499),(181,471),(191,458),(216,454),(268,450),(304,437),(334,451),(349,437),(379,440),(397,433),(430,432),(421,410),(402,386),(401,355),(416,338)],
        prussian_hole=[(617,626),(650,579),(693,567),(740,579),(771,549),(800,546),(819,559),(860,554),(891,558),(883,589),(875,620),(881,651),(927,672),(944,690),(942,710),(923,722),(925,754),(954,782),(946,812),(934,855),(934,886),(925,926),(915,959),(887,992),(909,1007),(912,1030),(874,1047),(853,1044),(808,1072),(789,1061),(779,1032),(767,1024),(739,1027),(724,1014),(690,1021),(664,1007),(622,1001),(606,971),(584,950),(570,931),(565,897),(559,874),(560,845),(550,823),(533,824),(519,852),(512,895),(504,912),(500,914),(508,922),(502,930),(503,956),(478,964),(463,952),(469,929),(478,903),(476,878),(490,840),(495,801),(503,760),(505,726),(516,707),(510,681),(534,653),(572,647),(602,634)])}
    # Final close readings: the uncoloured Muskau lordship belongs to Saxon
    # Upper Lusatia too. District colouring is not a sovereignty boundary.
    sheets['UPPER_1758']['additional_saxon_jurisdiction']=[(724,253),(780,268),(830,260),(900,237),(1049,229),(1038,267),(1011,275),(1000,304),(1003,359),(989,416),(955,417),(924,433),(901,420),(868,415),(837,433),(808,409),(779,352),(744,290)]
    # Neuzelle abbey and the northern Pforten lordship are also uncoloured
    # on this district map, but Saxon. Read their external Oder/Neumark border,
    # not the edge of the adjacent green district. This closes the spurious
    # Prussian corridor north of Cottbus/Peitz.
    sheets['LOWER']['additional_saxon_jurisdiction']=[(906,230),(950,243),(1015,255),(1043,280),(1065,330),(1077,344),(1067,360),(1053,370),(1064,375),(1075,385),(1075,398),(1064,410),(1064,428),(1062,440),(1073,452),(1102,458),(1115,468),(1136,494),(1142,505),(1130,514),(1091,524),(1064,520),(1022,547),(957,567),(881,552),(875,495),(885,429),(898,412),(909,340),(906,300)]
    # This replaces the initial coarse reading, not a native-model fit.
    # See COTTBUS_BOUNDARY_READING.jpg (global 1500-wide source coordinates).
    sheets['LOWER']['prussian_hole']=[(642,580),(689,567),(716,548),(732,549),(749,567),(762,574),(780,564),(795,551),(808,545),(845,548),(880,552),(912,555),(905,575),(889,594),(883,616),(881,636),(889,648),(906,655),(912,670),(907,683),(894,699),(875,707),(867,720),(868,733),(878,744),(868,755),(861,769),(850,784),(850,800),(859,818),(865,830),(860,839),(846,851),(849,870),(846,892),(838,900),(846,912),(853,928),(843,943),(822,947),(796,953),(785,965),(766,957),(740,952),(721,961),(700,947),(678,949),(654,944),(625,946),(610,936),(592,921),(579,912),(567,905),(563,881),(563,852),(552,824),(542,814),(530,816),(518,840),(514,869),(505,889),(502,892),(490,891),(482,874),(487,852),(493,833),(505,795),(512,778),(505,765),(497,747),(487,725),(484,704),(487,690),(476,676),(474,655),(470,637),(478,628),(493,619),(521,624),(540,627),(565,623),(595,628),(612,624),(624,604),(636,586)]
    yy, xx = np.mgrid[780:845, 4395:4460]
    chosen = np.zeros(xx.shape, dtype=bool)
    for name, s in sheets.items():
        c = s['controls']
        design = np.array([[x,y,1] for _,x,y,_,_ in c])
        target = forward(model, [[lon,lat] for _,_,_,lon,lat in c])
        matrix = np.linalg.lstsq(design, target, rcond=None)[0]
        s['source_to_native_matrix'] = matrix.tolist()
        s['fit_residuals_px'] = np.linalg.norm(design@matrix-target, axis=1).tolist()
        checks = s['checks']
        s['check_residuals_px'] = np.linalg.norm(np.array([[x,y,1] for _,x,y,_,_ in checks])@matrix-forward(model,[[lon,lat] for _,_,_,lon,lat in checks]),axis=1).tolist()
        polygon = np.c_[np.array(s['outline']), np.ones(len(s['outline']))]@matrix
        s['native_outline'] = polygon.tolist()
        points = np.c_[(xx+.5).ravel(), (yy+.5).ravel()]
        mask = inside(points, polygon).reshape(xx.shape)
        if s.get('additional_saxon_jurisdiction'):
            poly=np.c_[np.array(s['additional_saxon_jurisdiction']),np.ones(len(s['additional_saxon_jurisdiction']))]@matrix
            s['native_additional_saxon_jurisdiction']=poly.tolist()
            mask |= inside(points,poly).reshape(xx.shape)
        if s.get('prussian_hole'):
            hole=np.c_[np.array(s['prussian_hole']),np.ones(len(s['prussian_hole']))]@matrix
            s['native_prussian_hole'] = hole.tolist()
            mask &= ~inside(points, hole).reshape(xx.shape)
        chosen |= mask
        im=Image.open(OUT/'EVIDENCE'/(name+'.jpg')).convert('RGB').resize((1500,1432 if name=='UPPER_1758' else 1400))
        d=ImageDraw.Draw(im);d.line(s['outline']+[s['outline'][0]],fill='blue',width=3)
        if s.get('additional_saxon_jurisdiction'):d.line(s['additional_saxon_jurisdiction']+[s['additional_saxon_jurisdiction'][0]],fill='purple',width=3)
        if s.get('prussian_hole'):d.line(s['prussian_hole']+[s['prussian_hole'][0]],fill='red',width=3)
        for label,x,y,_,_ in c+checks:
            d.ellipse((x-4,y-4,x+4,y+4),fill='magenta');d.text((x+5,y),label,fill='black',stroke_width=1,stroke_fill='white')
        im.save(OUT/(name+'_TRACING_REVIEW.jpg'))
    # Explicit interface: only the Prussian Lusatian parents. Native Saxon,
    # Austrian, Polish and all other sovereignty cells are protected.
    parents=['xDF4020','x60BF20','xB90BFF','x76EF4E','x1B72C9','x614121','x272E48']
    local=bmp[780:845,4395:4460]
    chosen &= np.isin(local,[int(p[1:],16) for p in parents])
    candidate=bmp.copy();assignments=[];new_provinces=[]
    owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    idx=0xEEC000
    used=set(int(v) for v in np.unique(bmp))
    for p in (ROOT/'map_data/state_regions').glob('*.txt'):
        import re
        used.update(int(v,16) for v in re.findall(r'\bx([0-9a-fA-F]{6})\b',p.read_text(encoding='utf-8-sig')))
    for parent in parents:
        sid,owner=owners[parent];assert owner=='PRU'
        mask=(local==int(parent[1:],16))&chosen
        if parent=='x614121':
            # Entire existing Hoyerswerda/Spremberg/Muskau footprint lies in
            # Saxon Upper/Lower Lusatia or the adjoining Saxon Meissen fringe.
            # The uncoloured Muskau lordship and the western Meissen portion
            # are not Prussian exceptions. Retaining the atlas colour gaps
            # would manufacture five Prussian islands (including Muskau).
            # Cottbus/Peitz lie in xDF4020, independently kept Prussian.
            mask=local==int(parent[1:],16)
        parts=components(mask)
        # Reject isolated one-cell tracing slivers, never enlarge the selection.
        for part in parts:
            if len(part)<3:
                for y,x in part:mask[y,x]=False
        ys,xs=np.where(mask);cells=[[int(x+4395),int(y+780)] for y,x in zip(ys,xs)]
        total=int((bmp==int(parent[1:],16)).sum())
        if not cells:continue
        rgb=parent
        if len(cells)<total:
            while idx in used:idx+=1
            rgb='x'+format(idx,'06X');used.add(idx);idx+=1
            new_provinces.append(dict(rgb=rgb,parent_rgb=parent))
        for x,y in cells:candidate[y,x]=int(rgb[1:],16)
        assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner='PRU',owner='SAX',pixels=len(cells),cells=cells))
        if len(cells)<total:
            ys,xs=np.where((candidate==int(parent[1:],16)))
            assignments.append(dict(rgb=parent,parent_rgb=parent,state=sid,previous_owner='PRU',owner='PRU',pixels=len(xs),cells=[[int(x),int(y)] for y,x in zip(ys,xs)]))
    Image.fromarray(np.stack([(candidate>>16)&255,(candidate>>8)&255,candidate&255],axis=-1).astype(np.uint8)).save(OUT/'provinces_candidate.png')
    dump('TRACING.json',dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,
         native_model='docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json',
         warning='Source fitting/checks do not measure independent native geographical accuracy. No native refit. Both Lotter exemplars catalogued after 1758, exact issue year unspecified; Bern MUE Ryh 4410:15 and :17.',sheets=sheets))
    g=dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,
           selected_option='PRIMARY_LUSATIAN_OUTLINES_COTTBUS_PEITZ_RETAINED',parents=sorted({r['parent_rgb'] for r in assignments}),
           new_provinces=new_provinces,assignments=assignments,hub_rebindings=[],
           candidate_sha256=sha(OUT/'provinces_candidate.png'))
    dump('GEOMETRY.json',g)
    for r in assignments:print(r['parent_rgb'],r['rgb'],r['state'],r['owner'],r['pixels'])
    for n,s in sheets.items():print(n,'fit',s['fit_residuals_px'],'checks',s['check_residuals_px'])


def review():
    from georeference.model import forward
    g=json.loads((OUT/'GEOMETRY.json').read_text());b=json.loads((OUT/'BASELINE.json').read_text())
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text())['model']
    before=packed(OUT/'provinces_before.png');after=packed(OUT/'provinces_candidate.png')
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']}
    afterowners=owners|{r['rgb']:r['owner'] for r in g['assignments']}
    towns=[('Cottbus',14.334,51.760,'PRU'),('Peitz',14.412,51.858,'PRU'),('Guben',14.715,51.953,'SAX'),('Forst',14.645,51.744,'SAX'),('Sorau',15.138,51.642,'SAX'),('Gorlitz',14.989,51.157,'SAX'),('Lauban',15.289,51.119,'SAX'),('Hoyerswerda',14.252,51.437,'SAX'),('Spremberg',14.377,51.571,'SAX'),('Luckau',13.717,51.852,'SAX'),('Lubben',13.895,51.942,'SAX'),('Senftenberg',14.003,51.519,'SAX'),('Sagan',15.315,51.617,'PRU'),('Muskau',14.720,51.546,'SAX')]
    rows=[]
    for name,lon,lat,wanted in towns:
        x,y=forward(model,[[lon,lat]])[0];rgb='x'+format(int(after[int(y),int(x)]),'06X')
        rows.append(dict(name=name,x=float(x),y=float(y),rgb=rgb,owner=afterowners.get(rgb),expected=wanted,certified_position=False))
    dump('TOWN_DIAGNOSTICS.json',rows)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    panels=[]
    final_title='APRES - INSTALLE' if (OUT/'INSTALLATION.json').exists() else 'PROPOSITION'
    for title,bmp,own in [('AVANT',before,owners),(final_title,after,afterowners)]:
        local=bmp[790:840,4395:4460];a=np.full((*local.shape,3),220,dtype=np.uint8)
        for val in np.unique(local):a[local==val]={'PRU':(118,155,194),'SAX':(150,186,112),'AUS':(223,199,136)}.get(own.get('x'+format(int(val),'06X')),(220,220,220))
        im=Image.fromarray(a).resize((780,600),Image.Resampling.NEAREST)
        canvas=Image.new('RGB',(780,660),'white');canvas.paste(im,(0,40));d=ImageDraw.Draw(canvas)
        d.text((10,10),title+' - Bleu : Prusse / Vert : Saxe / Ocre : Autriche',font=font,fill='black')
        for r in rows:
            x,y=(r['x']-4395)*12,(r['y']-790)*12+40
            d.ellipse((x-2,y-2,x+2,y+2),fill='red');d.text((x+3,y),r['name'],font=font,fill='black',stroke_width=1,stroke_fill='white')
        d.text((10,644),'Repères géographiques diagnostiques ; généralisation politique B.',font=font,fill='black');panels.append(canvas)
    out=Image.new('RGB',(1560,660),'white');out.paste(panels[0]);out.paste(panels[1],(780,0));out.save(OUT/'BEFORE_AFTER.png')
    for r in rows:print(r['name'],r['owner'],'wanted',r['expected'])


def prepare():
    """Produce reviewable exact-byte candidates, never install them here."""
    import re
    from map2a_patch import edits
    from map2b_patch import state,region,append
    from map2l_belgium import allocate
    from map2l_registry import active_registry_path
    b=json.loads((OUT/'BASELINE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text())
    before={};files={};allocations=[]
    def read(rel):
        data=(ROOT/rel).read_bytes();assert sha(ROOT/rel)==b['runtime'].get(rel,sha(ROOT/rel)),rel
        before[rel]=data.decode('utf-8');return before[rel]
    bm=packed(OUT/'provinces_before.png');candidate=packed(OUT/'provinces_candidate.png')
    sids=sorted({r['state'] for r in g['assignments']})
    original_owners={r['key'][0]:(r['key'][1],r['key'][2]) for r in b['inventory']['owners']}
    weights={}
    for sid in sids:
        total=sum(int((bm==int(r['key'][0][1:],16)).sum()) for r in b['inventory']['owners'] if r['key'][1:]==[sid,'PRU'])
        moved=sum(r['pixels'] for r in g['assignments'] if r['state']==sid and r['owner']=='SAX')
        weights[sid]={'PRU':total-moved,'SAX':moved};assert 0<moved<total
    rel='common/history/states/00_states.txt';raw=read(rel)
    for sid in sids:
        s=state(raw,sid);src=next(n for n in s.children('create_state') if cw.scalar(n.one('country'))=='c:PRU');field=src.children('owned_provinces')[0]
        transferred={r['rgb'] for r in g['assignments'] if r['state']==sid and r['owner']=='SAX'}
        owned=[r for r in values(src,'owned_provinces') if r not in transferred]
        raw=edits(raw,[(field.start,field.end,'owned_provinces = { '+' '.join(owned)+' }')])
        s=state(raw,sid);assert not any(cw.scalar(n.one('country'))=='c:SAX' for n in s.children('create_state'))
        raw=edits(raw,[(s.end-1,s.end-1,'\n\t\t# Prussia V1: Saxon Lusatian territory; political generalisation B.\n\t\tcreate_state = { country = c:SAX owned_provinces = { '+' '.join(sorted(transferred))+' } }\n\t')])
    files[rel]=raw
    # Only references that actually contain their native hub are rebound.
    import map2m_r9 as old
    locs=old.locators(bm)
    g['hub_rebindings']=[]
    for rel in ['map_data/state_regions/00_west_europe.txt','map_data/state_regions/02_east_europe.txt']:
        raw=read(rel)
        for sid in sids:
            nodes=[n for n in cw.parse(raw.lstrip('\ufeff')) if n.key==sid]
            if not nodes:continue
            # Parse with the original BOM so byte-relative text offsets remain valid.
            s=next(n for n in cw.parse(raw) if n.key==sid);ops=[]
            added=[r['rgb'] for r in g['new_provinces'] if original_owners[r['parent_rgb']][0]==sid]
            field=s.children('provinces')[0];ops.append((field.end-1,field.end-1,' '+' '.join('"'+r+'"' for r in added)+' '))
            for kind in ['city','farm','mine','wood','port']:
                fields=s.children(kind)
                if not fields:continue
                field=fields[0];parent=cw.scalar(field.value)
                if parent not in g['parents']:continue
                actual=[r for r in locs if r['Kind']==kind and r['ID']==int(s.one('id'))]
                assert len(actual)==1,(sid,kind,actual)
                x,y=actual[0]['X'],actual[0]['Y'];assert 'x'+format(int(bm[int(y),int(x)]),'06X')==parent
                rgb='x'+format(int(candidate[int(y),int(x)]),'06X')
                if rgb!=parent:
                    ops.append((field.start,field.end,kind+' = "'+rgb+'"'))
                    g['hub_rebindings'].append(dict(state=sid,field=kind,before=parent,after=rgb,point=[x,y],pixel=[int(x),int(y)],locator_moved=False))
            for field in s.children('prime_land'):
                additions=[r['rgb'] for r in g['new_provinces'] if r['parent_rgb'] in values(s,'prime_land')]
                if additions:ops.append((field.end-1,field.end-1,' '+' '.join('"'+r+'"' for r in additions)+' '))
            raw=edits(raw,ops)
        if raw!=before[rel]:files[rel]=raw
    # Culture/religion/profession fragments retained exactly; counts are a
    # conservative scenario allocation, never a newly claimed 1776 census.
    for folder in ['common/history/pops','common/history/buildings']:
        for path in (ROOT/folder).glob('*.txt'):
            original=path.read_bytes().decode('utf-8')
            if not any('s:'+sid in original for sid in sids):continue
            rel=path.relative_to(ROOT).as_posix();raw=read(rel);ops=[];moved=collections.defaultdict(list)
            for sid in sids:
                try:src=region(raw,sid,'PRU')
                except StopIteration:continue
                if '/pops' in folder:
                    for pop in src.children('create_pop'):
                        v=pop.children('size')[0];counts=allocate(int(v.value),weights[sid]);frag=raw[pop.start:pop.end]
                        ops.append((v.start,v.end,'size = '+str(counts['PRU'])))
                        if counts['SAX']:moved[sid].append(edits(frag,[(v.start-pop.start,v.end-pop.start,'size = '+str(counts['SAX']))]))
                        allocations.append(dict(file=rel,state=sid,kind='population',culture=pop.one('culture'),religion=pop.one('religion','DEFAULT'),before=int(v.value),after=counts))
                else:
                    for building in src.children('create_building'):
                        kind=cw.scalar(building.one('building'))
                        # Existing arms, military and institutional installations
                        # stay with Prussia; only divisible civil output is split.
                        if kind not in {'building_logging_camp','building_livestock_ranch','building_rye_farm','building_coal_mine','building_iron_mine','building_lead_mine','building_paper_mill','building_railway'}:continue
                        levels=[v for v in cw.walk(building.children()) if v.key=='levels' and isinstance(v.value,str)]
                        bytag=collections.defaultdict(list);totals=collections.Counter();frag=raw[building.start:building.end]
                        for v in levels:
                            counts=allocate(int(v.value),weights[sid])
                            for tag,count in counts.items():bytag[tag].append((v.start-building.start,v.end-building.start,'levels = '+str(count)));totals[tag]+=count
                        if not totals['SAX']:continue
                        fragments={}
                        for tag in ['PRU','SAX']:
                            if not totals[tag]:continue
                            part=edits(frag,bytag[tag]);zero=[]
                            for own in cw.parse(part)[0].children('add_ownership'):
                                for holder in own.children():
                                    if holder.one('levels')=='0':zero.append((holder.start,holder.end,''))
                            fragments[tag]=edits(part,zero)
                        ops.append((building.start,building.end,fragments.get('PRU','')))
                        moved[sid].append(fragments['SAX'])
                        allocations.append(dict(file=rel,state=sid,kind=kind,before=sum(int(v.value) for v in levels),after=dict(totals),economic_owners_and_PM_preserved=True))
            raw=edits(raw,ops)
            for sid,pieces in moved.items():raw=append(raw,sid,'SAX','\n'.join(pieces))
            if raw!=original:files[rel]=raw
    rel='map_data/province_terrains.txt';raw=read(rel)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    for row in g['new_provinces']:raw+='\n'+row['rgb']+' = "'+terrain[row['parent_rgb'].upper()]+'"'
    files[rel]=raw+'\n'
    registry=active_registry_path();rel=registry.relative_to(ROOT).as_posix();ledger=json.loads(read(rel));parents=set(g['parents'])
    previous=[r for r in ledger if r['state'] in sids]
    updated=[r for r in previous if r['rgb'] not in parents]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='Prussia V1: Lotter Lusatia sheets, political generalisation B; exact 1776 cadastre not certified; see PRUSSIA_V1_2026_11_02/REPORT.md') for r in g['assignments']]
    ledger=sorted([r for r in ledger if r['state'] not in sids]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files[rel]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    migration=dict(replaced_regions=sids,previous=previous,updated=updated,new_members=[],free_cities=[],country_additions={},new_provinces=g['new_provinces'],region_reference_changes=g['hub_rebindings'],extent_added_cells=[],extent_removed_cells=[])
    dump('GEOMETRY.json',g);dump('REGISTRY_MIGRATION.json',migration)
    # Append an explicit, bounded layer to the existing registry chain.
    rel='tools/map2l_registry.py';raw=read(rel)
    anchor='    return result\n\ndef provincial_membership_overrides'
    if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
    assert raw.count(anchor)==1
    guard='''    prussia=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIA_V1_2026_11_02'
    if (prussia/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((prussia/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((prussia/'GEOMETRY.json').read_text(encoding='utf8'))
        assert teschen in result
        assert m['replaced_regions']==['STATE_BRANDENBURG','STATE_LOWER_SILESIA']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert set(g['parents'])=={'xDF4020','x60BF20','xB90BFF','x76EF4E','x1B72C9','x614121','x272E48'}
        assert all(r['state'] in m['replaced_regions'] and r['previous_owner']=='PRU' and r['owner'] in {'PRU','SAX'} for r in g['assignments'])
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items() if k not in g['parents'])
        assert len(new)==len(old)+len(g['new_provinces'])
        assert {(r['rgb'],r['state'],r['beneficiary']) for r in m['updated'] if r['rgb'] not in old or r['rgb'] in g['parents']}=={(r['rgb'],r['state'],r['owner']) for r in g['assignments']}
        result.append(prussia)
'''
    files[rel]=raw.replace(anchor,guard+anchor)
    for rel,raw in files.items():
        if rel.endswith('.txt'):cw.parse(raw.lstrip('\ufeff'))
    # Preserve each file's BOM and line endings; unrelated bytes remain intact.
    for rel,raw in list(files.items()):
        old=before[rel]
        if '\r\n' in old and old.count('\n')==old.count('\r\n'):raw=raw.replace('\r\n','\n').replace('\n','\r\n')
        files[rel]=raw
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files)
    dump('PLAN.json',dict(allocations=allocations,weights_by_state=weights,files=sorted(files),runtime_installed=False,
          population_method='Exact integer technical redistribution of current profiles; not a historical census',preserved_PRU_arms_levels=6))
    print('Prepared',len(files),'files;',sum(r['pixels'] for r in g['assignments'] if r['owner']=='SAX'),'ownership cells; no installation')


def compile_prepare():
    from unittest.mock import patch
    import difflib
    import map2k_imperial_system as compiler
    # The compiler asks the same immutable territorial questions per RGB.
    # Cache only within this preparation process; source files stay untouched.
    import functools
    import map2l_registry as registry_module
    for name in ['approved_territorial_migrations','territorial_holder_overrides']:
        setattr(registry_module,name,functools.lru_cache(maxsize=1)(getattr(registry_module,name)))
    compiler.territorial_holder_overrides=registry_module.territorial_holder_overrides
    files=json.loads((OUT/'EXPECTED_TEXT.json').read_text());before=json.loads((OUT/'TEXT_BEFORE.json').read_text())
    compiler.OUT=OUT
    base=compiler.compile_system()
    oldread=Path.read_text
    def candidate_read(path,*args,**kwargs):
        try:rel=path.relative_to(ROOT).as_posix()
        except ValueError:return oldread(path,*args,**kwargs)
        if rel in files:
            raw=files[rel]
            return raw.lstrip('\ufeff') if kwargs.get('encoding')=='utf-8-sig' else raw
        return oldread(path,*args,**kwargs)
    with patch.object(Path,'read_text',candidate_read):candidate=compiler.compile_system()
    drift=[];changed=[]
    for rel,raw in candidate.items():
        old=(ROOT/rel).read_bytes().decode('utf-8')
        norm=lambda s:s.lstrip('\ufeff').replace('\r\n','\n')
        if norm(raw)==norm(base[rel]):continue
        if norm(old)!=norm(base[rel]):drift.append(rel);continue
        before[rel]=old
        raw=('\ufeff' if old.startswith('\ufeff') else '')+raw.lstrip('\ufeff')
        if '\r\n' in old and old.count('\n')==old.count('\r\n'):raw=raw.replace('\r\n','\n').replace('\n','\r\n')
        files[rel]=raw;changed.append(rel)
    dump('COMPILER_PREFLIGHT.json',dict(concurrent_overlap=drift,generated_territorial_changes=changed,
          unaffected_compiler_outputs_preserved=True))
    assert not drift,'Concurrent compiler output changed: preserve and reconcile '+str(drift)
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files)
    lines=[]
    for rel,raw in files.items():lines.extend(difflib.unified_diff(before[rel].splitlines(True),raw.splitlines(True),fromfile=rel,tofile=rel,n=3))
    (OUT/'REVIEW.diff').write_text(''.join(lines),encoding='utf-8')
    print('Prepared imperial derivatives:',len(changed),'changed files;',len(files),'total text files; no installation')


def install():
    b=json.loads((OUT/'BASELINE.json').read_text());before=json.loads((OUT/'TEXT_BEFORE.json').read_text());files=json.loads((OUT/'EXPECTED_TEXT.json').read_text())
    assert not (OUT/'INSTALLATION.json').exists(),'Installation already recorded'
    for rel in files:assert (ROOT/rel).read_bytes().decode('utf-8')==before[rel],rel
    assert sha(ROOT/'map_data/provinces.png')==b['runtime']['map_data/provinces.png']
    changes=[]
    for rel,raw in files.items():
        assert (ROOT/rel).read_bytes().decode('utf-8')==before[rel],rel
        old=sha(ROOT/rel);(ROOT/rel).write_bytes(raw.encode('utf-8'));changes.append(dict(file=rel,before=old,after=sha(ROOT/rel)))
    rel='map_data/provinces.png';old=sha(ROOT/rel)
    assert old==b['runtime'][rel]
    (ROOT/rel).write_bytes((OUT/'provinces_candidate.png').read_bytes())
    changes.append(dict(file=rel,before=old,after=sha(ROOT/rel)))
    dump('INSTALLATION.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',completed_on='2026-11-05',changes=changes,
         human_validation=None,vanilla_modified=False,git_mutation=False))
    print('Installed',len(changes),'files; runtime validation required')


def verify():
    import map2l_registry as registry
    import serg_closure_roadmap as roadmap
    b=json.loads((OUT/'BASELINE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text());installation=json.loads((OUT/'INSTALLATION.json').read_text())
    inv=qa.inventory();dump('INVENTORY_AFTER.json',inv)
    before=packed(OUT/'provinces_before.png');after=packed(ROOT/'map_data/provinces.png')
    checks=[]
    def ck(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
    ck('Installed bitmap equals reviewed candidate',sha(ROOT/'map_data/provinces.png')==g['candidate_sha256'])
    ck('Exact 811 sovereignty cells',sum(r['pixels'] for r in g['assignments'] if r['owner']=='SAX')==811)
    beforeowners=qa.counter(b['inventory']['owners']);wanted=beforeowners.copy()
    for r in b['inventory']['owners']:
        if r['key'][0] in g['parents']:del wanted[tuple(r['key'])]
    for r in g['assignments']:wanted[r['rgb'],r['state'],r['owner']]+=1
    ck('Exact worldwide province ownership delta',qa.counter(inv['owners'])==wanted)
    ck('Existing ownership duplicate debt unchanged',inv['duplicates']==b['inventory']['duplicates'])
    ck('No new wrong-state or orphan references',inv['errors']==b['inventory']['errors'])
    ck('Six free RGB references added',len(g['new_provinces'])==6 and all(inv['geometry'][r['rgb']]==inv['geometry'][r['parent_rgb']] for r in g['new_provinces']))
    allowed=np.isin(before,[int(r[1:],16) for r in g['parents']])
    ck('All pixels outside seven reviewed parents preserved',np.array_equal(after[~allowed],before[~allowed]))
    for r in g['assignments']:
        cells={(x,y) for x,y in r['cells']};ys,xs=np.where(after==int(r['rgb'][1:],16))
        ck('Exact cells '+r['rgb'],cells==set(zip(xs.tolist(),ys.tolist())) and len(cells)==r['pixels'])
    ck('Entire pre-1815 Saxon Hoyerswerda/Spremberg/Muskau footprint',next(r for r in g['assignments'] if r['rgb']=='x614121')['owner']=='SAX' and int((after==0x614121).sum())==260)
    rows=json.loads((OUT/'TOWN_DIAGNOSTICS.json').read_text())
    ck('Fourteen coarse town diagnostics consistent',all(r['owner']==r['expected'] for r in rows),'Not independent certified city positions')
    ck('Native city/port/farm/mine/wood locators never moved',all(not r['locator_moved'] for r in g['hub_rebindings']))
    pru_mask=np.isin(after,[int(r['key'][0][1:],16) for r in inv['owners'] if r['key'][2]=='PRU'])
    pru_parts=components(pru_mask)
    cottbus=next(c for c in pru_parts if (808,4424) in c)
    ck('Prussian Cottbus enclave has no artificial corridor to Berlin',(787,4400) not in cottbus)
    for r in g['hub_rebindings']:
        x,y=r['point'];ck('Hub RGB contains actual locator '+r['state']+'/'+r['field'],int(after[int(y),int(x)])==int(r['after'][1:],16))
    ck('Global population cultures and religions conserved',inv['pops']==b['inventory']['pops'] and inv['resolved_demographics']==b['inventory']['resolved_demographics'])
    ck('Worldwide written population preserved',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in b['inventory']['pops']))
    regional=qa.counter(inv['regional_pop']);oldregional=qa.counter(b['inventory']['regional_pop']);plan=json.loads((OUT/'PLAN.json').read_text())
    sids=set(plan['weights_by_state'])
    ck('All populations outside two regions preserved',{k:v for k,v in regional.items() if k[0] not in sids}=={k:v for k,v in oldregional.items() if k[0] not in sids})
    for sid in sids:
        expected=sum(r['after']['SAX'] for r in plan['allocations'] if r['kind']=='population' and r['state']==sid)
        ck('New Saxon population '+sid,sum(v for k,v in regional.items() if k[0:2]==(sid,'SAX'))==expected)
    ck('No military formation or recruitment change',inv['units']==b['inventory']['units'])
    ck('All country definitions unchanged',inv['countries']==b['inventory']['countries'])
    def profiles(inventory):
        out=collections.Counter()
        def without_levels(n):return [n[0],n[1],[without_levels(c) for c in n[2] if c[0]!='levels']] if isinstance(n[2],list) else n
        def levels(n):return int(n[2]) if n[0]=='levels' else sum(levels(c) for c in n[2]) if isinstance(n[2],list) else 0
        for r in inventory['buildings']:
            sid,owner,body=r['key'];n=json.loads(body);out[sid,json.dumps(without_levels(n),ensure_ascii=False,separators=(',',':'))]+=levels(n)*r['count']
        return out
    ck('Buildings, levels, PMs and economic holders conserved by profile',profiles(inv)==profiles(b['inventory']))
    ck('World building level declarations conserved',inv['building_levels_written']==b['inventory']['building_levels_written'])
    ck('All buildings outside two regions preserved',[r for r in inv['buildings'] if r['key'][0] not in sids]==[r for r in b['inventory']['buildings'] if r['key'][0] not in sids])
    ck('Prussian arms and institutional buildings retained',[r for r in inv['buildings'] if r['key'][0]=='STATE_BRANDENBURG' and 'building_arms_industry' in r['key'][2]]==[r for r in b['inventory']['buildings'] if r['key'][0]=='STATE_BRANDENBURG' and 'building_arms_industry' in r['key'][2]])
    ledger=json.loads(registry.active_registry_path().read_text());migration=json.loads((OUT/'REGISTRY_MIGRATION.json').read_text())
    oldledger=json.loads(json.loads((OUT/'TEXT_BEFORE.json').read_text())['docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'])
    ck('587 unique imperial titles, six additional subdivisions',len(ledger)==587 and len({r['rgb'] for r in ledger})==587 and len(oldledger)==581)
    ck('Physical imperial extent unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in oldledger]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    ck('Only reviewed imperial title changes',sorted([r for r in oldledger if r['state'] not in sids]+migration['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))==ledger)
    ck('Ordered territorial chain appended without deleting older layers',registry.approved_lot_dirs()[-1]==OUT)
    from map2k_patch import ELECTORS
    ck('Nine electors preserved',len(ELECTORS)==9)
    for row in installation['changes']:ck('Exact installed file '+row['file'],sha(ROOT/row['file'])==row['after'])
    now=runtime_hashes();allowed_paths={r['file'] for r in installation['changes']}
    drift=[p for p in set(now)|set(b['runtime']) if now.get(p)!=b['runtime'].get(p) and p not in allowed_paths]
    ck('Concurrent and protected runtime files preserved',not drift,drift)
    beforetexts=json.loads((OUT/'TEXT_BEFORE.json').read_text())
    for rel in beforetexts:
        if rel not in allowed_paths:continue
        if rel.endswith('.txt'):cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    ck('Changed game scripts parse',True)
    ck('No new country or technology',not migration['new_members'] and not migration['country_additions'] and not any('/technology/' in p or '/countries/' in p for p in allowed_paths))
    for label,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current'])]:
        p=subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,capture_output=True,text=True)
        ck('Git '+label+' preserved',p.returncode==0 and p.stdout.strip()==b['git'][label]['output'])
    gd=Path(b['git']['git_dir']['output']);ck('Git index bytes preserved',sha(gd/'index')==b['git']['index_sha256'])
    state=roadmap.load_json(CANON/'ROADMAP_STATE.json');canonical=roadmap.check();dump('CANONICAL_AFTER.json',canonical)
    ck('Canonical validator passes',canonical['status']=='PASS',canonical['errors'])
    ck('Progress stays 93/235, no fake runtime credit',canonical['progress']['earned_weight']==93 and canonical['progress']['total_weight']==235 and canonical['progress']['percent']=='39.57')
    prior=json.loads((OUT/'ROADMAP_STATE_BEFORE.json').read_text());targets={'SC3-BRANDENBURG','SC3-SILESIA-LUSATIA'}
    ck('Other 79 tasks and attestations unchanged',[t for t in state['tasks'] if t['id'] not in targets]==[t for t in prior['tasks'] if t['id'] not in targets])
    ck('Previous events kept exactly',state['events'][:len(prior['events'])]==prior['events'])
    errors=[r for r in checks if not r['passed']]
    dump('VALIDATION.json',dict(status='PASS' if not errors else 'FAIL',completed_on='2026-11-05',passed=len(checks)-len(errors),total=len(checks),failed=errors,checks=checks,engine_test=False,human_attestation=None))
    print('Static validation',len(checks)-len(errors),'/',len(checks));print(json.dumps(errors,ensure_ascii=False))
    if errors:raise SystemExit(1)


def report():
    import serg_closure_roadmap as roadmap
    g=json.loads((OUT/'GEOMETRY.json').read_text());plan=json.loads((OUT/'PLAN.json').read_text())
    install=json.loads((OUT/'INSTALLATION.json').read_text());v=json.loads((OUT/'VALIDATION.json').read_text())
    b=json.loads((OUT/'BASELINE.json').read_text());current=qa.inventory()
    pop={s:sum(r['after']['SAX'] for r in plan['allocations'] if r['kind']=='population' and r['state']==s) for s in plan['weights_by_state']}
    tests=json.loads((OUT/'TEST_RESULTS.json').read_text()) if (OUT/'TEST_RESULTS.json').exists() else None
    table=['| Parent | Saxe | Prusse conservée |','| --- | ---: | ---: |']
    for parent in g['parents']:
        rows=[r for r in g['assignments'] if r['parent_rgb']==parent]
        table.append('| '+parent+' | '+str(sum(r['pixels'] for r in rows if r['owner']=='SAX'))+' | '+str(sum(r['pixels'] for r in rows if r['owner']=='PRU'))+' |')
    testline=(str(tests['passed'])+' réussites, '+str(tests['skipped'])+' exclusion(s), '+str(tests['failures'])+' échec(s), '+str(tests['errors'])+' erreur(s), sur '+str(tests['total'])+' tests canoniques et contrats de migration. L’exclusion concerne uniquement le contrôle ancien d’initialisation sans modification ; la conservation actuelle est contrôlée séparément.') if tests else 'Suite canonique à consigner dans TEST_RESULTS.json.'
    text=f'''# SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %

Passe Prusse commencée le 2 novembre et finalisée le 5 novembre 2026 dans le worktree **massa-carrara-finalisation**. **Sous-lots lusaciens installés, IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; aucune validation humaine nouvelle.** L'ensemble des frontières prussiennes n'est pas déclaré exact ou terminé.

## Résultat concret

**811 cellules PRU → SAX** : 393 dans la région technique Brandebourg, 418 dans la région technique Basse-Silésie. La carte restitue les ensembles saxons de Luckau/Lübben, Guben/Forst/Sorau, Hoyerswerda/Spremberg/Muskau et Görlitz/Lauban. Cottbus/Peitz reste une possession prussienne distincte ; Sagan et les portions silésiennes orientales sont conservées à la Prusse.

Les deux feuilles Lotter conservées à Berne ont été réellement lues. Leurs districts non coloriés, dont Muskau et Neuzelle/Pforten, ont été distingués des frontières de souveraineté. La décision et le tracé sont de **catégorie B** : limites généralisées à la résolution du jeu, sans garantie cadastrale. [Sources, lectures et incertitudes](SOURCES.md).

![Comparaison réellement installée](BEFORE_AFTER.png)

{chr(10).join(table)}

Six RGB nouveaux `xEEC000` à `xEEC005`, un parent réattribué entier (`x614121`, 260 cellules), sept parents concernés. **551 cellules sont recolorées**, les 260 autres gardent leur RGB et changent de propriétaire dans l'historique. Le raccord de la référence minière de Basse-Silésie suit son point natif ; aucun locator déplacé. Les ressources, capacité agraire, terrains parents, capitales et frontières des régions économiques sont conservés. Le nombre de titres impériaux passe de **581 à 587** par subdivision ; leur **étendue physique reste identique**. Aucun nouveau pays, membre ou électeur ; les titres des portions restituées appartiennent à SAX.

## Populations et économie

Redistribution technique conservatrice : **{pop['STATE_BRANDENBURG']}** habitants vers SAX/Brandebourg et **{pop['STATE_LOWER_SILESIA']}** vers SAX/Basse-Silésie, soit **{sum(pop.values())}** habitants existants. Chaque profil écrit est conservé mondialement. Total mondial écrit : **{sum(r['count'] for r in current['pops'])}**, delta zéro. Ces nombres ne sont pas un recensement historique des Lusaces.

Un niveau d'élevage de Basse-Silésie est réaffecté à la portion saxonne. Pour l'infrastructure traditionnelle du Brandebourg, chacune des deux déclarations historiques concernées passe de cinq niveaux PRU à quatre PRU et un SAX ; ces couches ne sont pas présentées comme deux niveaux moteur additionnels. Les recettes, PM et détenteurs économiques sont conservés. Les six niveaux d'armement prussiens, toutes les unités et tous les recrutements restent inchangés. Aucune révision technologique ou économique autonome.

## Vérifications réellement exécutées

- Contrôle différentiel sur le workspace actuel : **{v['passed']}/{v['total']}**, statut **{v['status']}** ; [résultats](VALIDATION.json).
- {testline} [Résultats bruts](TEST_RESULTS.json).
- Préparation des sorties impériales comparée d'abord au générateur sur l'état courant ; aucune divergence concurrente écrasée. [Précontrôle](COMPILER_PREFLIGHT.json), [différence révisable](REVIEW.diff).
- Propriétaires, références, populations, bâtiments/PM/détenteurs, unités, acquis extérieurs aux sept parents et fichiers concurrents contrôlés. Les anomalies techniques héritées restent celles de la capture, sans nouveau défaut de scope ou de référence.
- Aucun test moteur exécuté par l'agent. Aucun reçu humain créé. Git HEAD, branche et index conservés ; aucune opération Git d'écriture ni modification du vanilla.
- `git diff --check` : code de sortie zéro ; seules les informations de conversion LF/CRLF du workspace sont émises. Aucun ancien rapport n'est nettoyé pour les supprimer.

Les premières lectures provisoires et leur candidat rejeté sont conservés sous `PRELIMINARY_REJECTED_*`. Ils n'ont jamais été installés. Les modifications installées exactes et leurs empreintes sont dans [INSTALLATION.json](INSTALLATION.json).

## Portée restante et prochaine action

`SC3-BRANDENBURG` et `SC3-SILESIA-LUSATIA` restent **BLOCKED** pour leurs obligations régionales ; leurs sous-lots installés attendent le joueur. Le correctif ne clôt pas Magdebourg/Halberstadt, le nord de l'électorat saxon devenu prussien en 1815, toutes les franges de Glatz/Silésie, les limites occidentales, ni Netze/Thorn/Inowrocław. Les anomalies polonaises restent identifiées dans MAP2M/R9 ; aucun transfert de leurs grands RGB depuis un seul nom de ville.

**Prochaine action : [test joueur groupé de cette installation prussienne](PLAYER_TEST_PROTOCOL.md)**. Ensuite, poursuivre uniquement les grands écarts prussiens encore ouverts, notamment la frontière saxonne septentrionale et la frontière polonaise. Aucune Bavière commencée. Les micro-États sortent de la file active selon l'instruction utilisateur ; leurs obligations, preuves, statuts et points ne sont pas effacés.

Progression avant/après : **93/235 → 93/235**, **39,57 % → 39,57 %**, **32/81 tâches qualifiées**. Le dénominateur, les 81 tâches et le périmètre 1.0.0 sont conservés. Une livraison territoriale non reçue n'apporte aucun point de validation.

La livraison fonctionnelle est dans **{ROOT.as_posix()}**. Les autres copies du mod et le hotfix ne sont pas synchronisés automatiquement ; le protocole demande de vérifier le chemin de la copie effectivement lancée.
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')


def tracker():
    import serg_closure_roadmap as roadmap
    assert json.loads((OUT/'VALIDATION.json').read_text())['status']=='PASS'
    before=(CANON/'ROADMAP_STATE.json').read_bytes();state=json.loads(before)
    prior=json.loads((OUT/'ROADMAP_STATE_BEFORE.json').read_text());assert state==prior,'Concurrent tracker change: reconcile, never overwrite'
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    targets={'SC3-BRANDENBURG':('PR-V1-LOWER-LUSATIA',393,'Luckau/Lübben, Guben/Forst et raccord Neuzelle/Pforten ; Cottbus/Peitz PRU conservé',
                              'Le sous-lot lusacien est installé ; Magdebourg/Halberstadt, les limites restantes du Brandebourg et les autres cessions saxonnes de 1815 ne sont pas clôturés.'),
             'SC3-SILESIA-LUSATIA':('PR-V1-UPPER-LUSATIA',418,'Sorau, Hoyerswerda/Spremberg/Muskau, Görlitz/Lauban ; Sagan PRU conservé',
                              'Le sous-lot lusacien est installé ; les autres franges de Silésie/Glatz et la couverture historique/démographique régionale restent ouvertes.')}
    changes=[]
    for task in state['tasks']:
        if task['id'] not in targets:continue
        lot,count,scope,block=targets[task['id']];changes.append(dict(task_id=task['id'],before=task['status'],after='BLOCKED'))
        task.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
          implementation_report=[prefix+'REPORT.md',prefix+'SOURCES.md'],installed_lots=['SERG_CLOSURE/PRUSSIA_V1_2026_11_02'],
          installed_sub_lots=[dict(id=lot,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope=scope,cells=count,attestation=None)],
          static_tests=dict(status='PASS',evidence=[prefix+'VALIDATION.json']),
          runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope=lot,new_details_invented=False,protocol=prefix+'PLAYER_TEST_PROTOCOL.md'),
          blocking_reason=block,residual_uncertainty='Généralisation politique B, pas un cadastre ; aucune réception humaine et aucune clôture de l’ensemble régional.',
          current_delivery_note=str(count)+' cellules PRU→SAX, installation partielle documentée dans '+prefix+'REPORT.md')
        task['historical_sources'].append(prefix+'SOURCES.md')
    state['release_focus']=dict(authority='Instruction explicite du joueur dans ce chat : Prusse visible avant les micro-États ; Bavière seulement ensuite si décision.',
       active_country='PRU',started_on='2026-11-02',delivery_on='2026-11-05',microstates_removed_from_active_queue=True,
       unchanged_accounting_scope=True,no_deferred_approved_credit=True,bavaria_started=False,
       previous_runtime_validation_hold=state.get('runtime_validation_hold'),report=prefix+'REPORT.md')
    state['runtime_validation_hold']=dict(task_id='SC3-BRANDENBURG',pending_task_ids=list(targets),protocol=prefix+'PLAYER_TEST_PROTOCOL.md',
       reason='Installation prussienne groupée à tester avant toute nouvelle passe ; priorité utilisateur PRU.',
       next_implementation_candidate=None,scope_note='Ne pas reprendre micro-États, Massa, Teschen ou Bavière automatiquement ; anciennes obligations conservées.')
    state['mission_status']='PRUSSIA_V1_LUSATIAN_CORRECTIONS_INSTALLED_PENDING_RUNTIME'
    progress_before=roadmap.progress(prior);progress_after=roadmap.progress(state)
    eid='SERG-RM-'+format(max(int(e['id'].rsplit('-',1)[1]) for e in state['events'])+1,'04d')
    state['events'].append(dict(id=eid,date='2026-11-05',kind='PRUSSIA_V1_LUSATIAN_CORRECTIONS_INSTALLED',scope_version=state['scope_version'],
      source=prefix+'REPORT.md',changes=changes,before_weight=progress_before['earned_weight'],after_weight=progress_after['earned_weight'],
      total_weight=progress_after['total_weight'],before_percent=progress_before['percent'],after_percent=progress_after['percent'],
      note='Priorité utilisateur Prusse ; 811 cellules PRU→SAX, 393 Brandebourg et 418 Basse-Silésie ; Cottbus/Peitz/Sagan conservés. Sous-lots prêts à tester, deux régions BLOCKED, zéro reçu humain et zéro point supplémentaire. Micro-États hors file active sans effacement comptable ; aucune Bavière.',
      evidence=[prefix+'INSTALLATION.json',prefix+'VALIDATION.json',prefix+'PLAYER_TEST_PROTOCOL.md']))
    tracked={name:(CANON/name).read_bytes().decode('utf-8') for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md']}
    dump('TRACKER_BEFORE.json',tracked)
    header='''## Priorité utilisateur — Prusse V1, livraison du 5 novembre 2026

**811 cellules PRU → SAX installées**, dont 393 dans le Brandebourg technique et 418 en Basse-Silésie. Cottbus/Peitz et Sagan restent prussiens. [Rapport](PRUSSIA_V1_2026_11_02/REPORT.md), [protocole joueur groupé](PRUSSIA_V1_2026_11_02/PLAYER_TEST_PROTOCOL.md).

Les sous-lots sont `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` ; **SC3-BRANDENBURG et SC3-SILESIA-LUSATIA restent BLOCKED** pour leurs obligations régionales. Aucune nouvelle validation humaine. **93/235 = 39,57 %, 32/81**. Registre 587 titres, étendue impériale inchangée ; six RGB supplémentaires ne donnent aucun point.

Les micro-États sont retirés de la file active selon la demande du joueur, sans supprimer leurs tâches, preuves ou blocages et sans crédit de report. Prochaine action : test de cette livraison prussienne, puis grands écarts prussiens encore ouverts ; **aucun lancement automatique de Bavière**, de Massa ou de Teschen. Les sections plus anciennes reproduites ci-dessous sont archivées dans leur contexte et ne remplacent pas cette priorité.

'''
    updated={}
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        raw=tracked[name];split=raw.find('\n');raw=raw[:split+1]+'\n'+header+raw[split+1:]
        if name=='NEXT_ACTION.md':raw=raw.replace(raw.splitlines()[0],'# Prochaine action — test de la livraison prussienne V1',1)
        if name=='BLOCKERS.md':
            for tid in targets:raw=raw.replace(tid+' `NOT_STARTED`',tid+' `BLOCKED`')
        if name=='ROADMAP.md':
            for tid in targets:
                start=raw.index('#### '+tid+' —');end=raw.find('\n#### ',start+1)
                if end<0:end=len(raw)
                section=raw[start:end].replace('`NOT_STARTED`','`BLOCKED`',1)
                section=section.replace('\nRégion/périmètre :','\nSous-lot prussien installé, en attente du joueur ; [livraison](PRUSSIA_V1_2026_11_02/REPORT.md). La région reste incomplète.\n\nRégion/périmètre :',1)
                raw=raw[:start]+section+raw[end:]
        updated[name]=raw
    updated['PROGRESS_HISTORY.md']=tracked['PROGRESS_HISTORY.md']+'\n\n## '+eid+' — 5 novembre 2026 — Prusse V1, sous-lots lusaciens installés\n\n811 cellules PRU→SAX, 393 Brandebourg et 418 Basse-Silésie ; Cottbus/Peitz/Sagan protégés. Deux tâches régionales NOT_STARTED→BLOCKED avec installations partielles prêtes au test joueur. Aucun reçu humain, aucun point : 93/235 et 39,57 %, 32/81. Les 79 autres tâches, événements et reçus sont conservés. Priorité Prusse explicite, micro-États hors file active sans effacement ni crédit, Bavière non commencée. [Rapport](PRUSSIA_V1_2026_11_02/REPORT.md).\n'
    assert (CANON/'ROADMAP_STATE.json').read_bytes()==before
    (CANON/'ROADMAP_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,raw in updated.items():
        assert (CANON/name).read_bytes().decode('utf-8')==tracked[name],name
        (CANON/name).write_bytes(raw.encode('utf-8'))
    roadmap.write_json(CANON/'PROGRESS_SNAPSHOT.json',roadmap.progress(state))
    dump('TRACKER_CHANGE.json',dict(event=eid,changes=changes,before=progress_before,after=roadmap.progress(state),human_receipts_added=0))
    result=roadmap.check();dump('CANONICAL_AFTER.json',result)
    assert result['status']=='PASS',result
    print(eid,result['progress']['percent'],result['progress']['earned_weight'],'/',result['progress']['total_weight'])


if __name__ == '__main__':
    globals()[sys.argv[1]]()
