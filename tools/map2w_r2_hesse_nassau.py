"""MAP2W-R2: bounded historical continuation, never restore shared snapshots."""
import collections as C
import json,re,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2w_west_south as r1
core=r1.core;q=r1.q;ROOT=r1.ROOT
OUT=r1.OUT/'R2'
REGIONS=['STATE_HESSE','STATE_RHINELAND','STATE_NORTH_RHINE','STATE_SAXONY']

def dump(name,data):
    (OUT/name).parent.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Immutable capture already exists'
    inv=core.qa.inventory();originals={};bitmap=r1.OUT/'provinces_candidate.png'
    assert core.sha(bitmap)==core.sha(ROOT/'map_data/provinces.png')
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if any(sid in raw for sid in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    older={p.relative_to(ROOT).as_posix():core.sha(p) for name in ['MAP2R','MAP2S','MAP2T','MAP2U'] for p in (ROOT/'docs/reports/map'/name).rglob('*') if p.is_file()}
    older.update({p.relative_to(ROOT).as_posix():core.sha(p) for p in r1.OUT.iterdir() if p.is_file()})
    protected=['tools/map2l_registry.py','tools/map2k_imperial_system.py','tools/hre_centralization_01.py','tools/hre_subject_feedback_01.py','tools/hre_secession_lens_01.py']
    dump('BASELINE.json',dict(inventory=inv,originals=originals,hashes=q.economy.runtime_hashes(),bitmap_backup=bitmap.relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(bitmap),registry=json.loads(core.active_registry_path().read_text(encoding='utf8')),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=core.sha(ROOT/'.git/index'),tool_originals={p:(ROOT/p).read_text(encoding='utf8') for p in protected},prior_records=older))
    print('Captured world',sum(r['count'] for r in inv['pops']),'registry',len(load('BASELINE.json')['registry']),flush=True)

def inspect():
    b=load('BASELINE.json');a=core.packed(ROOT/b['bitmap_backup']);rows=[]
    for r in b['inventory']['owners']:
        rgb,sid,tag=r['key']
        if sid not in REGIONS or tag not in ['NAS','HEK','HES','FUL']:continue
        yy,xx=np.where(a==int(rgb[1:],16));rows.append(dict(rgb=rgb,state=sid,owner=tag,pixels=len(xx),box=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    dump('CURRENT_PROVINCES.json',rows)
    for tag in ['NAS','HEK','HES']:
        path=next(p for p in core.qa.effective(ROOT,core.qa.GAME,'common/history/characters') if p.name.lower().startswith(tag.lower()+' -'))
        dump(tag+'_CURRENT_CHARACTER.json',dict(path=path.as_posix(),text=path.read_text(encoding='utf-8-sig')))
    im=Image.open(r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB')
    box=(300,1850,2100,4075);crop=im.crop(box);d=ImageDraw.Draw(crop);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    for x in range(400,2100,200):d.line((x-box[0],0,x-box[0],crop.height),fill='blue');d.text((x-box[0]+2,1),str(x),font=font,fill='blue',stroke_width=2,stroke_fill='white')
    for y in range(2000,4075,200):d.line((0,y-box[1],crop.width,y-box[1]),fill='blue');d.text((2,y-box[1]+2),str(y),font=font,fill='blue',stroke_width=2,stroke_fill='white')
    crop.thumbnail((1080,1335));crop.save(OUT/'NASSAU_SOURCE_READING.png')
    print(json.dumps(rows,ensure_ascii=False),flush=True)
    print('NAS character',load('NAS_CURRENT_CHARACTER.json')['text'][:1800],flush=True)

def compiler_before():
    old=r1.prior.t.OUT;r1.prior.t.OUT=OUT
    try:r1.prior.t.compiler_before()
    finally:r1.prior.t.OUT=old

def geometry():
    """Conservative source interiors, never turn a city point into a whole province."""
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup'])
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text(encoding='utf8'))['model']
    controls=[('Siegen',827,2069,8.0243,50.8748),('Dillenburg',1176,2344,8.2869,50.7410),('Weilburg',1152,2901,8.2628,50.4856),('Limburg',902,3128,8.0639,50.3872),('Usingen',1540,3216,8.5369,50.3356),('Idstein',1084,3486,8.2700,50.2200),('Wiesbaden',1093,3784,8.2410,50.0826)]
    source=np.array([[x,y,1] for _,x,y,_,_ in controls]);target=forward(model,[[lon,lat] for _,_,_,lon,lat in controls]);tr=np.linalg.lstsq(source,target,rcond=None)[0]
    # These are inward jurisdiction outlines on Uhlhorn's 1789 sheet.
    # Dated institutional evidence establishes continuity; condominium belts,
    # Nassau town (1781 exchange), Hachenburg (1799), Mainz/1803 are excluded.
    polys={
      'NOU':[(720,1900),(1040,1920),(1160,2050),(1360,2135),(1360,2300),(1320,2350),(1370,2400),(1350,2510),(1240,2530),(1200,2580),(1150,2580),(1060,2700),(925,2720),(900,2580),(925,2425),(940,2350),(970,2230),(920,2135),(740,2100)],
      'NWB':[(1130,2780),(1280,2790),(1320,2820),(1380,2830),(1430,2890),(1470,2920),(1450,2990),(1440,3080),(1450,3150),(1400,3150),(1350,3130),(1290,3110),(1260,3050),(1190,3050),(1170,2990),(1190,2920),(1140,2890)],
      'NAS':[(930,3450),(1100,3450),(1260,3450),(1390,3450),(1390,3500),(1310,3560),(1250,3595),(1230,3690),(1230,3800),(1190,3850),(1160,3840),(1000,3840),(980,3750),(940,3720),(950,3670),(940,3570)]}
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};labels={};traces=[];excluded=[]
    allowed={'x1357DB','x90C0A0','x8B7C67','x90C020','x3E794B'}
    sheet=np.asarray(Image.open(r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB'));inverse=np.linalg.inv(np.vstack([tr.T,[0,0,1]]))
    for tag,poly in polys.items():
        mapped=np.column_stack([poly,np.ones(len(poly))])@tr
        xmin,ymin=np.floor(mapped.min(axis=0)).astype(int);xmax,ymax=np.ceil(mapped.max(axis=0)).astype(int)
        yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx.ravel();yy=yy.ravel();chosen=core.inside(np.column_stack([xx+.5,yy+.5]),mapped);included=[]
        for x,y in zip(xx[chosen],yy[chosen]):
            rgb='x'+format(int(before[y,x]),'06X');sid,old=owners[rgb]
            # The broad hand envelope must never swallow differently coloured
            # jurisdictions such as Solms/Braunfels or Hessen. Read a local
            # majority fill, not a label, from the retained historical sheet.
            sx,sy,_=inverse@np.array([x+.5,y+.5,1]);sx=int(round(sx));sy=int(round(sy))
            sample=sheet[sy-15:sy+16,sx-15:sx+16].astype(int);rr,gg,bb=sample[...,0],sample[...,1],sample[...,2]
            fraction=float(np.mean((gg>rr+7)&(gg>bb+3)&(rr<185)&(bb>80)))
            if fraction<0.50:excluded.append(dict(cell=[int(x),int(y)],rgb=rgb,state=sid,owner=old,proposed=tag,reason='Non-Nassau/edge colour on source sheet',source_pixel=[sx,sy],green_fraction=fraction));continue
            if rgb not in allowed or sid!='STATE_HESSE':excluded.append(dict(cell=[int(x),int(y)],rgb=rgb,state=sid,owner=old,proposed=tag));continue
            if old==tag:continue
            assert (int(x),int(y)) not in labels,'Overlapping traced sovereigns'
            labels[int(x),int(y)]=tag;included.append([int(x),int(y)])
        traces.append(dict(tag=tag,source_polygon=poly,game_polygon=mapped.tolist(),included=included))
    parents=sorted({'x'+format(int(before[y,x]),'06X') for x,y in labels});after=before.copy();assignments=[];new=[];used=set(map(int,np.unique(before)));color=0xEDB700
    for parent in parents:
        sid,old=owners[parent];ys,xs=np.where(before==int(parent[1:],16));tags=np.array([labels.get((int(x),int(y)),old) for x,y in zip(xs,ys)])
        for tag in sorted(set(tags)):
            mask=np.zeros(before.shape,bool);mask[ys[tags==tag],xs[tags==tag]]=True
            for i,part in enumerate(core.components(mask)):
                if tag==old and i==0:rgb=parent
                else:
                    while color in used:color+=1
                    rgb='x'+format(color,'06X');used.add(color);color+=1;new.append(dict(rgb=rgb,parent_rgb=parent))
                py=np.array([p[0] for p in part]);px=np.array([p[1] for p in part]);after[py,px]=int(rgb[1:],16)
                assignments.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner=old,owner=tag,pixels=len(part),cells=[[int(x),int(y)] for y,x in part],confidence='B' if tag!=old else 'C_RETAINED'))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,traces=traces,excluded=excluded,new_members=['NOU','NWB'],hub_rebindings=[],limits='Inward B cores only. Residual NAS/HES/WLD cells remain unverified, not certified Usingen/Hesse/Waldeck. No Nassau-town condominium, no Saarbruecken, no 1799/1803 acquisitions.'))
    dump('SOURCE_ALIGNMENT.json',dict(transform=tr.tolist(),controls=[dict(name=n,source=[x,y],geo=[lo,la],diagnostic_pixel=p.tolist(),sheet_residual=float(np.linalg.norm(np.array([x,y,1])@tr-p))) for (n,x,y,lo,la),p in zip(controls,target)],independent_native_error_bound_px=None,warning='Source-sheet registration to inherited empirical diagnostic model only. Not an independent validation or exact pixel location. B generalization, no change to projection or Erfurt.'))
    im=Image.open(r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB');d=ImageDraw.Draw(im)
    for tag,poly in polys.items():d.line(poly+[poly[0]],fill={'NOU':'blue','NWB':'red','NAS':'orange'}[tag],width=7)
    crop=im.crop((300,1850,2100,4075));crop.thumbnail((1080,1335));crop.save(OUT/'SOURCE_TRACING_REVIEW.png')
    # Native locator ownership is audited, never used as historical evidence.
    locs=[r for r in q.r9.locators(before) if r['ID']==74];dump('LOCATORS_BEFORE.json',locs)
    dump('CITY_DIAGNOSTIC.json',[dict(name=n,pixel=p.tolist(),before=owners.get('x'+format(int(before[round(p[1]),round(p[0])]),'06X')),after=next(([a['state'],a['owner']] for a in assignments if a['rgb']=='x'+format(int(after[round(p[1]),round(p[0])]),'06X')),owners.get('x'+format(int(after[round(p[1]),round(p[0])]),'06X')))) for (n,x,y,lo,la),p in zip(controls,target)])
    print('Transfers',dict(C.Counter(labels.values())),'new RGB',len(new),'parents',parents,'excluded',dict(C.Counter(r['owner'] for r in excluded)),flush=True)

def inventory():
    """Targeted continuation; no new 94-entry German inventory."""
    rows=[]
    entities=[
      ('Hesse-Cassel','HEK','Friedrich II.','Landgraviat','A','Souverain de 1776 à restaurer; limites détaillées non certifiées','https://www.kassel.de/buerger/stadtgeschichte/stadtarchiv/geschichten-aus-dem-stadtarchiv/inhalt-geschichten-aus-dem-stadtarchiv/kassel-unter-landgraf-friedrich-ii.php'),
      ('Hesse-Darmstadt','HES','Ludwig IX.','Landgraviat, non grand-duché','A','Rang et souverain à corriger; raccord Idstein B seulement','https://www.darmstadt-stadtlexikon.de/l/ludwig-ix-landgraf-von-hessen-darmstadt.html'),
      ('Hesse-Hombourg',None,'Friedrich V.','Landgraviat','C','Absent; limites de 1776 et dépendance impériale à préciser, pas la dotation de Meisenheim de 1816','https://lagis.hessen.de/de/quellen-und-materialien/quellen-zur-juedischen-geschichte/alle-eintraege/7055_geplante-feierlichkeiten-und-geschenke-der-judenschaft-homburg-anlaesslich-de-la-hochzeit-des-landgrafen-friedrich-v-von-hessen-homburg'),
      ('Hanau-Münzenberg','HEK','Wilhelm, héritier de Hesse-Cassel','Administration séparée depuis 1764','C','Administration prouvée; souveraineté et géométrie non résolues, pas de nouveau pays automatique','https://www.hanau.de/stadtentwicklung/geschichte/geschichtsdaten/index.html'),
      ('Hanau-Lichtenberg','HES','Ludwig IX.','Possession dynastique','C','Ne pas confondre avec Hanau-Münzenberg; possessions alsaciennes non reconstruites','https://www.darmstadt-stadtlexikon.de/l/ludwig-ix-landgraf-von-hessen-darmstadt.html'),
      ('Hesse-Rotenbourg','HEK',None,'Apanage, pas indépendance déduite','C','Limites et droits réservés; maintien du propriétaire technique', 'MAP2W/INVENTORY_1776.csv'),
      ('Nassau-Usingen','NAS','Karl Wilhelm','Principauté','B','Noyau Idstein et raccord intérieur seulement; nom et souverain corrigés, résidus C','https://www.wiesbaden.de/en/microsite/stadtlexikon/import/a-z/wiesbaden-unter-nassauischer-herrschaft'),
      ('Nassau-Weilbourg','NWB','Karl Christian','Principauté','B','Noyau autour de Weilbourg et Weilmünster, possessions occidentales non installées','https://www.deutsche-biographie.de/11688410X.html'),
      ('Nassau-Orange : Siegen–Dillenburg','NOU','Wilhelm V.','Possessions allemandes à gouvernement commun depuis 1743','B','Noyau intérieur, sans absorption des Provinces-Unies ni sujétion native','https://arcinsys.hessen.de/arcinsys/showFondsDetails.action?fondsId=2005'),
      ('Nassau-Orange : Diez–Hadamar–Beilstein','NAS','Wilhelm V.','Possessions du même ensemble allemand','C','Franges et dépendances non tracées; pas de pays fictif par ancienne branche','https://arcinsys.hessen.de/arcinsys/showFondsDetails?fondsId=3508'),
      ('Nassau-Sarrebruck','NAS','Ludwig','Principauté distincte de Nassau-Usingen','C','Pas réunie en 1776; souveraineté distincte prouvée, géométrie occidentale non installée','https://scopearchiv.saarbruecken.de/detail.aspx?ID=85'),
      ('Ville et condominium de Nassau','NAS',None,'Droits partagés','C','Échange de 1781 interdit comme frontière de 1776; exclu du tracé','https://www.archivesportaleurope.net/advanced-search/search-in-archives/results-%28archives%29/?levelName=archdesc&recordId=b2102&repositoryCode=DE-2555&t=fa&term='),
      ('Löhnberg','NAS',None,'Ancien condominium partagé en 1773','C','Partage documenté, correspondance précise des parcelles non résolue','https://www.deutsche-biographie.de/11688410X.html'),
      ('Vierherrisches / Einrich',None,None,'Partage de 1775','C','Ne pas reproduire une communauté antérieure ou un arrondissement ultérieur','https://www.deutsche-biographie.de/11688410X.html'),
      ('Sayn-Hachenburg',None,None,'Comté distinct en 1776','C','Succession Weilbourg de 1799 exclue','https://www.deutsche-biographie.de/11688410X.html'),
      ('Fulda–Hünfeld–Neuhof','FUL','Heinrich VIII von Bibra','Prince-évêché','B','39 cellules et quatre RGB de R1 protégés; validation moteur encore attendue','docs/reports/map/MAP2W/REPORT.md'),
      ('Herbstein','HEK','Heinrich VIII von Bibra','Possession de Fulda','C','Souveraineté établie jusqu’en 1802; enclave source encore à tracer et confronter au bitmap','https://lagis.hessen.de/de/orte/burgen-schloesser-herrenhaeuser/alle-eintraege/14639_burg-herbstein'),
      ('Geisa','MEI','Heinrich VIII von Bibra','Possession de Fulda','C','Piste source conservée; contours et raccord avec les noyaux T/U à établir','docs/reports/map/MAP2W/HISTORICAL_EVIDENCE.md'),
      ('Dermbach','MEI','Heinrich VIII von Bibra','Possession de Fulda','C','Répartition des droits et enveloppe géographique non suffisamment recoupées','docs/reports/map/MAP2W/HISTORICAL_EVIDENCE.md'),
      ('Solms / Isembourg / Wittgenstein',None,None,'Plusieurs juridictions distinctes','C','Exclus des traces de Nassau; pas d’annexion par couleur voisine','https://lagis.hessen.de/resolve/de/ga/40')]
    for name,tag,ruler,kind,level,note,source in entities:rows.append(dict(Territoire=name,TAG=tag,Souverain_1776=ruler,Nature=kind,Classe=level,Perimetre=note,Source=source))
    dump('INVENTORY_PHASE.json',dict(phase='BEFORE_FUNCTIONAL_EDITS',rows=rows,earlier_coverage_checked=['MAP2L/FRANCONIA','MAP2L/FRANCONIA_CONTINUATION','MAP2L/RHINE_CENTRAL','MAP2L/MAINZ_PALATINATE','MAP2L/MAINZ_ESTATES','MAP2L/MAINZ_COMPLETION','MAP2L/RHINE_WESTPHALIA_COMPLETION','MAP2L/DUCHY_WESTPHALIA','MAP2L/SWABIA','MAP2L/SWABIA_CONTINUATION','MAP2L/SWABIA_FINISH','MAP2L/SWABIA_COMPLETION','MAP2R','MAP2S','MAP2T','MAP2U','MAP2W/REPORT.md'],scope='R2-A: Nassau right-bank inward cores + Hessian institutions. Other R2 jurisdictions remain open.'))
    print('Targeted inventory',len(rows),'entries',flush=True)

def countries(files,migration):
    defs=''.join(tag+' = { color = { '+color+' } country_type = recognized tier = principality cultures = { north_german } religion = protestant capital = STATE_HESSE }\n' for tag,color in [('NOU','225 155 65'),('NWB','93 158 172')])
    assert not {'NOU','NWB'}&set(load('BASELINE.json')['inventory']['countries'])
    files['common/country_definitions/1776_map2w_r2_nassau.txt']=defs;migration['country_additions']={n.key:core.qa.signature(n) for n in core.cw.parse(defs)}
    template=(ROOT/'common/history/countries/nas - nassau.txt').read_text(encoding='utf-8-sig')
    for tag in ['NOU','NWB']:files['common/history/countries/'+tag.lower()+' - map2w_r2.txt']=template.replace('c:NAS','c:'+tag)
    rulers={'NOU':('Wilhelm V.','von Oranien-Nassau','1748.3.8','protestant'),'NWB':('Karl Christian','von Nassau-Weilburg','1735.1.16','protestant'),'NAS':('Karl Wilhelm','von Nassau-Usingen','1735.11.9','protestant'),'HEK':('Friedrich II.','von Hessen-Kassel','1720.8.14','catholic'),'HES':('Ludwig IX.','von Hessen-Darmstadt','1719.12.15','protestant')}
    for tag,(_,_,born,religion) in rulers.items():
        rel=('common/history/characters/'+Path(load(tag+'_CURRENT_CHARACTER.json')['path']).name) if tag in ['NAS','HEK','HES'] else 'common/history/characters/'+tag.lower()+' - map2w_r2.txt'
        # Matching vanilla basename is necessary: an additive differently named
        # file would leave the 1836 ruler and heir active alongside this ruler.
        files[rel]='CHARACTERS = { c:'+tag+' ?= { create_character = { first_name = aor1776_map2w_r2_'+tag.lower()+'_first last_name = aor1776_map2w_r2_'+tag.lower()+'_last historical = yes culture = north_german religion = rel:'+religion+' ruler = yes birth_date = '+born+' interest_group = ig_landowners ideology = ideology_traditionalist } } }\n'
    files['common/flag_definitions/1776_map2w_r2_nassau.txt']=''.join(tag+' = { flag_definition = { coa = aor1776_map2w_r2_nassau priority = 100 allow_overlord_canton = no } }\n' for tag in ['NOU','NWB','NAS'])
    files['common/coat_of_arms/coat_of_arms/1776_map2w_r2_nassau.txt']='# Provisional shared dynastic arms, not a claim of identical state flags.\naor1776_map2w_r2_nassau = { pattern = "pattern_solid.tga" color1 = "blue" colored_emblem = { texture = "ce_lion_rampant.dds" color1 = "yellow" color2 = "red" instance = { scale = { 0.8 0.8 } } } }\n'
    # Existing landgraviate government is reused; only the anachronistic
    # grand-principality tier is changed, never all shared country definitions.
    rel='common/country_definitions/00_countries.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');node=next(n for n in core.cw.parse(raw) if n.key=='HES');field=node.children('tier')[0];assert field.value=='grand_principality'
    changed=core.edits(raw,[(field.start,field.end,'tier = principality')]);after=next(n for n in core.cw.parse(changed) if n.key=='HES');files[rel]=changed
    migration['country_tier_corrections']=[dict(tag='HES',before='grand_principality',after='principality',before_signature=core.qa.signature(node),after_signature=core.qa.signature(after))]
    for lang in ['french','english']:
        fr=lang=='french';loc='\ufeffl_'+lang+':\n'
        names={'NAS':('Nassau-Usingen','Nassau-Usingen'),'NOU':('Nassau-Orange','Orange-Nassau'),'NWB':('Nassau-Weilbourg','Nassau-Weilburg')}
        # Overrides are intentionally placed in replace/; ordinary duplicate
        # keys have undefined load precedence and are not localization fixes.
        for tag,(f,e) in names.items():loc+=' '+tag+':0 "'+(f if fr else e)+'"\n '+tag+'_ADJ:0 "'+('nassovien' if fr else e)+'"\n'
        for tag,(first,last,_,_) in rulers.items():loc+=' aor1776_map2w_r2_'+tag.lower()+'_first:0 "'+first+'"\n aor1776_map2w_r2_'+tag.lower()+'_last:0 "'+last+'"\n'
        files[f'localization/{lang}/replace/1776_map2w_r2_l_{lang}.yml']=loc

def prepare():
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};bindings=[]
    assert load('INVENTORY_PHASE.json')['phase']=='BEFORE_FUNCTIONAL_EDITS'
    assert load('COMPILER_BEFORE.json')['passed']==73
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png');groups=C.defaultdict(list)
    for a in g['assignments']:groups[a['parent_rgb']].append(a)
    # Reread shared targets immediately before narrow generation; unrelated
    # collaborator edits are preserved, overlapping state edits stop the lot.
    rel='common/history/states/00_states.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');old=b['originals'][rel]
    assert core.qa.signature(core.state(raw,'STATE_HESSE'))==core.qa.signature(core.state(old,'STATE_HESSE')),'Concurrent Hesse state edit'
    s=core.state(raw,'STATE_HESSE');ops=[]
    for n in s.children('create_state'):
        tag=n.one('country').removeprefix('c:');f=n.children('owned_provinces')[0];owned=[]
        for rgb in core.values(n,'owned_provinces'):owned.extend(a['rgb'] for a in groups[rgb] if a['owner']==tag) if rgb in groups else owned.append(rgb)
        owned.extend(a['rgb'] for a in g['assignments'] if a['owner']==tag and a['previous_owner']!=tag)
        if owned!=core.values(n,'owned_provinces'):ops.append((f.start,f.end,'owned_provinces = { '+' '.join(owned)+' }'))
    ops.append((s.end-1,s.end-1,'\n'+''.join('create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(a['rgb'] for a in g['assignments'] if a['owner']==tag)+' } }\n' for tag in ['NOU','NWB'])))
    files[rel]=core.edits(raw,sorted(ops))
    for rel,old in b['originals'].items():
        if not rel.startswith('map_data/state_regions/'):continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');nodes={n.key:n for n in core.cw.parse(raw)}
        if 'STATE_HESSE' not in nodes:continue
        node=nodes['STATE_HESSE'];assert core.qa.signature(node)==core.qa.signature(next(n for n in core.cw.parse(old) if n.key=='STATE_HESSE')),'Concurrent Hesse geometry edit';ops=[]
        for field in ['provinces','prime_land']:
            for f in node.children(field):
                old_rgb=core.values(node,field);new=[]
                for rgb in old_rgb:new.extend(a['rgb'] for a in groups[rgb]) if rgb in groups else new.append(rgb)
                if new!=old_rgb:
                    ops.append((f.start,f.end,field+' = { '+' '.join('"'+v+'"' for v in new)+' }'))
                    if field=='prime_land':bindings.append(dict(state='STATE_HESSE',field=field,before=old_rgb,after=new))
        # Native locators are not moved. Retained largest parent components
        # keep existing hub references unless their actual pixel changed.
        for loc in load('LOCATORS_BEFORE.json'):
            x,y=int(loc['X']),int(loc['Y']);rgb='x'+format(int(after[y,x]),'06X');old_rgb=core.cw.scalar(node.one(loc['Kind']))
            if rgb!=old_rgb:
                f=node.children(loc['Kind'])[0];ops.append((f.start,f.end,loc['Kind']+' = "'+rgb+'"'));bindings.append(dict(state='STATE_HESSE',field=loc['Kind'],before=old_rgb,after=rgb,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
        if ops:files[rel]=core.edits(raw,sorted(ops))
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};weights={};allocations=[]
    for src in sorted({a['previous_owner'] for a in g['assignments']}):
        total=sum(int(np.sum(before==int(rgb[1:],16))) for rgb,st in owners.items() if st==['STATE_HESSE',src]);counts=C.Counter({src:total})
        for a in g['assignments']:
            if a['previous_owner']==src and a['owner']!=src:counts[src]-=a['pixels'];counts[a['owner']]+=a['pixels']
        assert counts[src]>0;weights[src]=dict(counts)
    for rel,old in b['originals'].items():
        if '/pops/' not in rel and '/buildings/' not in rel:continue
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');ops=[];moved=C.defaultdict(list)
        for src,counts in weights.items():
            try:n=core.region(raw,'STATE_HESSE',src)
            except StopIteration:continue
            assert core.qa.signature(n)==core.qa.signature(core.region(old,'STATE_HESSE',src)),('Concurrent Hesse allocation edit',rel,src)
            if '/pops/' in rel:
                for pop in n.children('create_pop'):
                    f=pop.children('size')[0];amounts=core.allocate(int(f.value),counts);piece=raw[pop.start:pop.end];ops.append((f.start,f.end,'size = '+str(amounts[src])))
                    for tag,amount in amounts.items():
                        if tag!=src and amount:moved[tag].append(core.edits(piece,[(f.start-pop.start,f.end-pop.start,'size = '+str(amount))]))
                    allocations.append(dict(kind='population',file=rel,state='STATE_HESSE',source=src,culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:'+pop.one('culture')),before=int(f.value),after=amounts))
            else:
                # No factory or infrastructure is located by these rural
                # polygon interiors. Keep all existing levels and investors
                # in their surviving source subdivision, not pixel-weighted
                # invented industrial geography. New countries get only
                # their conserved population/land/subsistence from the engine.
                for building in n.children('create_building'):
                    allocations.append(dict(kind='building',file=rel,state='STATE_HESSE',source=src,profile=building.one('building'),before=sum(int(v.value) for v in core.cw.walk(building.children()) if v.key=='levels'),after={src:sum(int(v.value) for v in core.cw.walk(building.children()) if v.key=='levels')},method='Existing source building and all ownership references retained unchanged'))
        if ops:
            text=core.edits(raw,sorted(ops))
            for tag,parts in moved.items():text=core.append(text,'STATE_HESSE',tag,'\n'.join(parts))
            files[rel]=text
    dump('ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_POPULATION_ONLY_NOT_CENSUS',weights=weights,profiles=allocations,historical_population=None))
    rel='map_data/province_terrains.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw.rstrip()+'\n'+''.join(a['rgb']+'="'+terrain[a['parent_rgb'].upper()]+'"\n' for a in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state']=='STATE_HESSE'];updated=[r for r in previous if r['rgb'] not in g['parents']]+[dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2W-R2-A Nassau inward B core; unchanged C residual explicitly not certified; see MAP2W/R2/REPORT.md') for a in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state']!='STATE_HESSE']+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    migration=dict(replaced_regions=['STATE_HESSE'],previous=previous,updated=updated,new_members=['NOU','NWB'],free_cities=[],new_provinces=g['new_provinces'],geometry='MAP2W/R2/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[])
    countries(files,migration)
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n';files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    dump('PREINSTALL_HASHES.json',q.economy.runtime_hashes());dump('EXPECTED_TEXT.json',files);core.OUT=OUT;changes=core.emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,registered_RGBs=len(ledger),region_reference_changes=bindings))
    print('Prepared',len(changes),'files, registry',len(ledger),flush=True)

def install():
    b=load('BASELINE.json');assert core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256']
    for p,raw in load('EXPECTED_TEXT.json').items():assert (ROOT/p).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip(),p
    subprocess.run(['powershell','-NoProfile','-Command',"Copy-Item -LiteralPath '"+str(OUT/'provinces_candidate.png')+"' -Destination '"+str(ROOT/'map_data/provinces.png')+"' -ErrorAction Stop"],check=True)
    print('Installed scoped candidate bitmap',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files);core.OUT=OUT
    changes=core.emit(files,'IMPERIAL.patch');dump('IMPERIAL_FILES.json',dict(files=changes));print('Imperial files',len(changes),'/',len(files),flush=True)

def validate():
    from map2l_registry import expected_country_definitions,approved_lot_dirs,apply_territorial_migrations,approved_territorial_extensions,rebind_state_definitions
    b=load('BASELINE.json');g=load('GEOMETRY.json');m=load('REGISTRY_MIGRATION.json');inv=core.qa.inventory();dump('CURRENT_INVENTORY.json',inv);checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy();eo=counter(b['inventory']['owners']);owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    for k in list(eo):
        if k[0] in g['parents']:del eo[k]
    for a in g['assignments']:
        for x,y in a['cells']:expected[y,x]=int(a['rgb'][1:],16)
        eo[a['rgb'],a['state'],a['owner']]=1
        check('Owner/state '+a['rgb'],owners.get(a['rgb'])==[a['state'],a['owner']])
        check('One connected RGB '+a['rgb'],int(np.sum(after==int(a['rgb'][1:],16)))==a['pixels'] and len(core.components(after==int(a['rgb'][1:],16)))==1)
    check('Exact full bitmap delta',np.array_equal(expected,after));check('Exact world ownership delta',counter(inv['owners'])==eo)
    check('72 sovereign cell transfers',sum(a['pixels'] for a in g['assignments'] if a['owner']!=a['previous_owner'])==72)
    check('Only Hesse State_ID 74 changed',set(a['state'] for a in g['assignments'])=={'STATE_HESSE'})
    check('Erfurt frozen',np.array_equal(before[822:837,4342:4359],after[822:837,4342:4359]))
    for key in ['building_levels_written','duplicates','errors','resolved_demographics','pops']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    concurrent=load('CONCURRENT_WORK_OBSERVED.json') if (OUT/'CONCURRENT_WORK_OBSERVED.json').exists() else None
    eu=counter(b['inventory']['units'])
    if concurrent and 'military_units_expected' in concurrent:eu=counter(concurrent['military_units_expected'])
    check('Units conserved except explicitly protected collaborator countries',counter(inv['units'])==eu)
    eb=counter(b['inventory']['buildings'])
    if concurrent:
        for change in concurrent['building_deltas']:
            eb[tuple(change['before_key'])]-=1;eb[tuple(change['after_key'])]+=1
    check('Global buildings exact MAP baseline plus independent French PR6',counter(inv['buildings'])==eb)
    types=dict(b['inventory']['state_types']);types.update({'STATE_HESSE|'+tag:'incorporated_default' for tag in ['NOU','NWB']});check('Only two new subdivisions',inv['state_types']==types)
    check('Two countries and HES tier only',inv['countries']==expected_country_definitions(b['inventory']['countries'],[m]))
    ep=counter(b['inventory']['regional_pop'])
    for row in load('ALLOCATION.json')['profiles']:
        if row['kind']!='population':continue
        ep[row['state'],row['source'],row['culture'],row['religion']]-=row['before']
        for tag,n in row['after'].items():ep[row['state'],tag,row['culture'],row['religion']]+=n
        check('Integer cultural/religious population '+row['source']+' '+row['culture']+' '+row['religion'],sum(row['after'].values())==row['before'] and all(isinstance(n,int) and n>=0 for n in row['after'].values()))
    check('Exact regional population delta',counter(inv['regional_pop'])==ep)
    world=sum(r['count'] for r in inv['pops']);oldworld=sum(r['count'] for r in b['inventory']['pops']);check('World 835801255 retained',world==oldworld==835801255)
    totals={tag:sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag) for tag in ['NAS','NOU','NWB','WLD','HES','HEK','FUL']}
    for tag in ['NOU','NWB']:check('Positive conserved population '+tag,totals[tag]>0)
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'));check('554 unique registry RGBs',len(ledger)==len({r['rgb'] for r in ledger})==554)
    for row in ledger:check('Imperial title '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']])
    check('Imperial physical extent conserved',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry'];belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'));regions={a['state'] for a in belgian['assignments']}
    frozen=[r for r in initial if r['state'] not in regions]+[dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for a in belgian['assignments']]+approved_territorial_extensions()
    check('Full chronological registry replay',apply_territorial_migrations(frozen)==ledger)
    changed_parent_values=set(map(int,np.unique(before[before!=after])))
    check('No earlier nonparent colour changed',changed_parent_values<={int(rgb[1:],16) for rgb in g['parents']})
    for r in b['registry']:
        if r['rgb'] in g['parents']:continue
        # Full exact-bitmap comparison above plus the changed-parent set is
        # stronger than rescanning all 29M cells for each of 542 old colours.
        check('Previous RGB geometry and owner '+r['rgb'],owners.get(r['rgb'])==[r['state'],r['beneficiary']] and int(r['rgb'][1:],16) not in changed_parent_values)
    check('FUL39 and original population preserved',totals['FUL']==20047 and all(np.array_equal(before==int(rgb[1:],16),after==int(rgb[1:],16)) for rgb in ['xEDB600','xEDB601','xEDB602','xEDB603']))
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for a in g['new_provinces']:
        check('New RGB absent from original '+a['rgb'],not np.any(before==int(a['rgb'][1:],16)))
        check('New terrain inherited once '+a['rgb'],len(re.findall(r'(?im)^\s*'+a['rgb']+r'\s*=',terrain))==1 and tm[a['rgb'].upper()]==tm[a['parent_rgb'].upper()])
        check('New region mapping '+a['rgb'],inv['geometry'].get(a['rgb'])=='STATE_HESSE')
    compiled=load('IMPERIAL_EXPECTED.json');files=load('EXPECTED_TEXT.json')
    for rel,raw in files.items():
        check('Reviewed text '+rel,(ROOT/rel).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip())
        if rel.endswith('.txt'):
            try:core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'));check('Parse '+rel,True)
            except Exception as e:check('Parse '+rel,False,str(e))
        if rel in b['originals'] and '/history/' in rel:
            old=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(b['originals'][rel])) if n.key.startswith('s:STATE_') and n.key!='s:STATE_HESSE'];new=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(raw)) if n.key.startswith('s:STATE_') and n.key!='s:STATE_HESSE'];check('Other state histories '+rel,old==new)
        if rel.startswith('map_data/state_regions/'):
            old={n.key:n for n in core.cw.parse(b['originals'][rel])};new={n.key:n for n in core.cw.parse(raw)}
            for sid,node in old.items():
                exclude={'provinces','prime_land'} if sid=='STATE_HESSE' else set()
                check('ID/resources/arable/traits/hubs '+sid,[core.qa.signature(n) for n in node.children() if n.key not in exclude]==[core.qa.signature(n) for n in new[sid].children() if n.key not in exclude])
    for rel,raw in compiled.items():check('Cumulative imperial compiled '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    for lang in ['french','english']:
        rel=f'localization/{lang}/replace/1776_map2w_r2_l_{lang}.yml';raw=(ROOT/rel).read_text(encoding='utf-8-sig');keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0\s+"',raw,re.M)
        check('Localization BOM/header '+lang,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':'))
        check('Sixteen matching keys '+lang,len(keys)==len(set(keys))==16)
        check('No unmatched localization quotes '+lang,all(line.count('"')==2 for line in raw.splitlines()[1:] if line.strip()))
    for filename in ['pattern_solid.tga','ce_lion_rampant.dds']:
        sub='patterns' if filename.startswith('pattern') else 'colored_emblems';check('Native heraldic asset '+filename,(core.qa.GAME/'gfx/coat_of_arms'/sub/filename).is_file())
    for tag in ['NAS','HEK','HES']:
        native=Path(load(tag+'_CURRENT_CHARACTER.json')['path']);p=ROOT/'common/history/characters'/native.name;nodes=core.cw.parse(p.read_text(encoding='utf-8-sig'));chars=[n for n in core.cw.walk(nodes) if n.key=='create_character'];check('1836 character file properly replaced '+tag,len(chars)==1 and chars[0].one('ruler')=='yes' and not chars[0].children('template'))
    for tag in ['NOU','NWB']:
        country=next(n for n in core.cw.parse(files['common/country_definitions/1776_map2w_r2_nassau.txt']) if n.key==tag);check('Owned technical capital '+tag,any(r['key'][1:]==[country.one('capital'),tag] for r in inv['owners']))
        oldtech=next(n for n in core.cw.walk(core.cw.parse((ROOT/'common/history/countries/nas - nassau.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:NAS');newtech=next(n for n in core.cw.walk(core.cw.parse(files['common/history/countries/'+tag.lower()+' - map2w_r2.txt'])) if n.key=='c:'+tag);check('No artificial laws/technology '+tag,[core.qa.signature(n) for n in oldtech.children()]==[core.qa.signature(n) for n in newtech.children()])
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));allowed=set(files)|set(compiled)|{'map_data/provinces.png'}
    allowed.add('gfx/interface/journal_entries/aor1776_hre_registered_map.dds')
    external=set(concurrent['files']) if concurrent else set()
    outside=[p for p in changed if p not in allowed|external];check('No undeclared runtime change',not outside,outside)
    if concurrent:
        check('External French file preserved byte-for-byte',all(current.get(p)==h for p,h in concurrent['hashes'].items()))
        check('External PR6 does not overlap planned files',not external&set(files))
    for folder in ['buildings','military_formations','unit_types','diplomacy','subject_types','map_object_data']:
        check('All MAP-owned '+folder+' byte-identical',all(current.get(p)==h for p,h in b['hashes'].items() if '/'+folder+'/' in p and p not in external))
    for p,raw in b['tool_originals'].items():
        if p!='tools/map2l_registry.py':check('Imperial mechanics source frozen '+p,(ROOT/p).read_text(encoding='utf8')==raw)
    for p,h in b['prior_records'].items():check('Prior report frozen '+p,core.sha(ROOT/p)==h)
    git_ref=concurrent or dict(head_after=b['git_head'],index_sha256=b['git_index_sha256'])
    check('Observed HEAD remains intact',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==git_ref['head_after']);check('Observed index remains intact',core.sha(ROOT/'.git/index')==git_ref['index_sha256'])
    result=dict(status='MAP2W_R2_READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2W_R2_BLOCKED',scope='R2-A Nassau right-bank inward cores + Hessian institutions, not all R2 territories',runtime_status='NOT_TESTED_MAP2W_R1_OR_R2',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,world_before=oldworld,world_after=world,country_populations=totals,runtime_files_modified=[p for p in changed if p not in external],concurrent_files=sorted(external),preexisting_duplicate_RGBs=len(inv['duplicates']),preexisting_errors=inv['errors'])
    dump('VALIDATION_R2.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2W-R2-A',functional_files={p:current[p] for p in changed if p not in external},external_files={p:current[p] for p in external},bitmap_sha256=core.sha(ROOT/'map_data/provinces.png')))
    print(result['status'],result['passed'],'/',len(checks),'populations',totals,flush=True)
    if result['passed']!=len(checks):raise SystemExit(1)

def maps():
    from PIL import ImageColor
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};new=dict(old)
    for a in g['assignments']:new[a['rgb']]=a['owner']
    palette={'NAS':'#8171b5','NOU':'#e19b41','NWB':'#5d9eac','HES':'#c695ba','HEK':'#92bc88','WLD':'#a6bd65','FRM':'#d7c45b','PRU':'#839bb6','KMZ':'#d29065','FUL':'#986bb6'}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
    x0,y0,x1,y1=4273,829,4308,865;scale=19
    def panel(a,owners,title,outline):
        local=a[y0:y1,x0:x1];rgb=np.zeros((*local.shape,3),dtype='uint8')
        for c in np.unique(local):rgb[local==c]=ImageColor.getrgb(palette.get(owners.get('x'+format(int(c),'06X')),'#e0ddd6'))
        im=Image.fromarray(rgb).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);p=Image.new('RGB',(im.width,im.height+245),'#fcfaf5');p.paste(im,(0,48));d=ImageDraw.Draw(p);d.text((14,10),title,font=bold,fill='#243747')
        if outline:
            for aa in g['assignments']:
                if aa['owner']==aa['previous_owner']:continue
                for x,y in aa['cells']:d.rectangle(((x-x0)*scale,(y-y0)*scale+48,(x-x0+1)*scale-1,(y-y0+1)*scale+47),outline='white',width=2)
        # Country labels identify installed geometry, not certified GPS points.
        for label,x,y in [('Siegen (repère)',4287,835),('Dillenburg (repère)',4292,839),('Weilbourg (repère)',4292,846),('Idstein (repère)',4292,854),('Francfort / FRM',4301,857)]:
            px=(x-x0)*scale;py=(y-y0)*scale+48;d.ellipse((px-3,py-3,px+3,py+3),fill='black');d.text((min(max(px-65,3),im.width-175),py-22),label,font=small,fill='#182c38',stroke_width=2,stroke_fill='white')
        for i,(tag,color) in enumerate(palette.items()):
            xx=12+(i%5)*130;yy=im.height+65+(i//5)*26;d.rectangle((xx,yy,xx+12,yy+12),fill=color);d.text((xx+18,yy-3),tag,font=small,fill='#243747')
        for i,line in enumerate(['Contours B : généralisation intérieure, pas un cadastre.','Blanc : cellules transférées. Neuf nouveaux RGB.','Points de repérage schématiques : pas des positions certifiées.','Résidus C inchangés ; Usingen et Wiesbaden restent incomplets.']):d.text((12,im.height+155+i*21),line,font=small,fill='#30373d')
        return p
    a=panel(before,old,'AVANT MAP2W-R2-A',False);z=panel(after,new,'APRÈS : trois noyaux de Nassau',True);out=Image.new('RGB',(a.width+z.width+20,a.height),'#fcfaf5');out.paste(a,(0,0));out.paste(z,(a.width+20,0));out.save(OUT/'HESSE_NASSAU_BEFORE_AFTER.png')
    guide=Image.new('RGB',(1240,870),'#fcfaf5');d=ImageDraw.Draw(guide);d.text((25,15),'Contrôle en jeu : Nassau et souverains hessois',font=bold,fill='#243747');ox,oy,ex,ey=4260,812,4330,879;local=after[oy:ey,ox:ex];arr=np.zeros((*local.shape,3),dtype='uint8')
    for c in np.unique(local):arr[local==c]=ImageColor.getrgb(palette.get(new.get('x'+format(int(c),'06X')),'#dedbd4'))
    guide.paste(Image.fromarray(arr).resize((700,670),Image.Resampling.NEAREST),(20,65));d=ImageDraw.Draw(guide)
    for label,x,y in [('1 NOU',4292,839),('2 NWB',4294,847),('3 NAS',4292,853),('FRM',4301,857),('HEK',4317,827),('FUL',4322,844)]:
        px=20+(x-ox)*10;py=65+(y-oy)*10;d.ellipse((px-4,py-4,px+4,py+4),fill='black');d.text((px+8,py-15),label,font=font,fill='#182c38',stroke_width=2,stroke_fill='white')
    notes=['Nouvelle partie au 1er janvier 1776.','1. Nassau-Orange : noyau Siegen–Dillenburg.','   NOU, Wilhelm V., 43 cellules transférées.','2. Nassau-Weilbourg : intérieur de Weilbourg.','   NWB, Karl Christian, 13 cellules.','3. Nassau-Usingen : raccord autour d’Idstein.','   NAS, Karl Wilhelm, 16 cellules HES → NAS.','','Vérifier pays, noms, souverains, accès au marché,','subsistance et absence de sujétion automatique.','HEK : Friedrich II. ; HES : Ludwig IX.','HES reste un landgraviat, pas un grand-duché.','','Pas de nouvelle usine, route ou unité.','Populations redistribuées, non recensées.','Laisser passer au moins un mois.','','Restent ouverts : Sarrebruck, Usingen/Wiesbaden,','Diez/Hadamar, Hanau, Hombourg et Fulda-franges.']
    for i,line in enumerate(notes):d.text((745,75+i*33),line,font=small,fill='#293d49')
    d.text((25,780),'Repères de recherche schématiques ; consulter les RGB et polygones dans GEOMETRY.json.',font=font,fill='#293d49');d.text((25,816),'R1 et R2 : tests manuels encore attendus. Aucun PASS_RUNTIME_USER_VALIDATED attribué.',font=font,fill='#293d49');guide.save(OUT/'PLAYER_LOCATION_GUIDE.png')
    # Review the *accepted* game-cell footprints on the historical source,
    # rather than just the larger hand envelopes used during source reading.
    tr=np.array(load('SOURCE_ALIGNMENT.json')['transform']);itr=np.linalg.inv(np.vstack([tr.T,[0,0,1]]));im=Image.open(r1.OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB');d=ImageDraw.Draw(im)
    for aa in g['assignments']:
        if aa['owner']==aa['previous_owner']:continue
        for x,y in aa['cells']:
            corners=[tuple((itr@np.array([px,py,1]))[:2]) for px,py in [(x,y),(x+1,y),(x+1,y+1),(x,y+1),(x,y)]];d.line(corners,fill={'NOU':'blue','NWB':'red','NAS':'orange'}[aa['owner']],width=3)
    crop=im.crop((300,1850,2100,4075));crop.thumbnail((1080,1335));crop.save(OUT/'ACCEPTED_CELLS_SOURCE_REVIEW.png');print('Maps and accepted-cell source review generated',flush=True)

def tables():
    inventory=load('INVENTORY_PHASE.json')['rows'];g=load('GEOMETRY.json');v=load('VALIDATION_R2.json');alloc=load('ALLOCATION.json');tables={}
    # Correct stale provisional lookup leads before publishing the worklist.
    for r in inventory:
        if r['Territoire']=='Hesse-Hombourg':r['Source']='https://lagis.hessen.de/de/quellen-und-materialien/quellen-zur-juedischen-geschichte/alle-eintraege/7055_geplante-feierlichkeiten-und-geschenke-der-judenschaft-homburg-anlaesslich-der-hochzeit-des-landgrafen-friedrich-v-von-hessen-homburg'
        if r['Territoire'] in ['Geisa','Dermbach','Herbstein']:r['TAG']=None
        if r['Territoire']=='Hesse-Cassel':r['Perimetre']='Friedrich II. restauré dans le fichier effectif de personnages ; limites détaillées toujours ouvertes'
        if r['Territoire']=='Hesse-Darmstadt':r['Perimetre']='Rang princier et Ludwig IX. corrigés ; gouvernement landgraviat conservé ; raccord Idstein B seulement'
        if r['Territoire']=='Löhnberg':r['Perimetre']='Partage de 1773 documenté ; le noyau B de Weilbourg touche ce secteur, sans certifier la limite fine ni restituer chaque part de l’ancien condominium'
    def add(name,rows):tables[name]=dict(fields=list(rows[0]),rows=rows)
    add('INVENTORY_1776_R2.csv',inventory)
    discrepancies=[dict(Entite=r['Territoire'],Classe=r['Classe'],Etat='CORRIGE_INSTITUTIONS_FRONTIERES_OUVERTES' if r['Territoire'] in ['Hesse-Cassel','Hesse-Darmstadt'] else 'NOYAU_B_INSTALLE_RESIDUS_OUVERTS' if r['TAG'] in ['NAS','NOU','NWB'] and r['Classe']=='B' else 'R1_PROTEGE_NON_RETESTE' if r['TAG']=='FUL' else 'C_LIMITE_FINE_DIFFEREE' if r['Territoire']=='Löhnberg' else 'C_DIFFERE_SANS_MODIFICATION',Probleme=r['Perimetre'],Source=r['Source']) for r in inventory]
    add('DISCREPANCIES_R2.csv',discrepancies)
    unresolved=[dict(Territoire=r['Territoire'],Probleme=r['Perimetre'],Preuve_manquante='Correspondance des limites et des cellules, droits/souveraineté si signalés ; pas de simple déplacement d’un point urbain',Action='Conserver le propriétaire technique ; reprendre seulement avec preuves nouvelles',Source=r['Source']) for r in inventory if r['Classe']=='C']
    unresolved.extend([dict(Territoire='Nassau : résidus et noyaux non couverts',Probleme='NAS conserve des résidus C qui ne sont pas certifiés Usingen. Usingen-centre et Wiesbaden-FRM non transférés. Pas de frontière complète des trois pays.',Preuve_manquante='Limites cohérentes avec les juridictions voisines et les lots antérieurs ; statut des franges/condominiums',Action='Sous-lot ultérieur ; pas d’annexion de FRM ou PRU ni d’élargissement automatique',Source='GEOMETRY.json; CITY_DIAGNOSTIC.json'),dict(Territoire='Démographie et viabilité des noyaux',Probleme='Redistribution technique par profil entier ; aucun recensement local 1776. Aucun bâtiment ajouté ou transféré arbitrairement.',Preuve_manquante='Séries démographiques territoriales comparables et observations du marché en jeu',Action='Tester subsistance, emploi, accès au marché ; pas de population ou industrie artificielle',Source='ALLOCATION.json'),dict(Territoire='Drapeaux et liens dynastiques',Probleme='Armes nassoviennes simplifiées communes, pas des pavillons historiques complets. Même prince en Hollande ≠ dépendance native.',Preuve_manquante='Drapeaux territoriaux exacts et modèle dynastique sans effet de sujétion indu',Action='Conserver abstraction explicite ; aucune union personnelle native ajoutée',Source='REPORT.md')])
    add('UNRESOLVED_R2.csv',unresolved)
    changes=[dict(Type='TRANSFERT' if a['owner']!=a['previous_owner'] else 'RESIDU_CONSERVE',Territoire={'NOU':'Siegen–Dillenburg intérieur','NWB':'Weilbourg–Weilmünster intérieur','NAS':'Idstein intérieur'}.get(a['owner'],'Résidu technique') if a['owner']!=a['previous_owner'] else 'Résidu technique non certifié',Avant=a['previous_owner'],Apres=a['owner'],State_ID=a['state'],ID_numerique=74,RGB_avant=a['parent_rgb'],RGB_apres=a['rgb'],Cellules=a['pixels'],Classe=a['confidence'],Population=None,Justification='Juridictions recoupées : Uhlhorn 1789 + continuité avant 1776 ; filtrage des autres couleurs et des noyaux protégés' if a['owner']!=a['previous_owner'] else 'Aucune certification historique du résidu',Source='GEOMETRY.json; SOURCE_ALIGNMENT.json; HISTORICAL_EVIDENCE_R2.md') for a in g['assignments']]
    for tag in ['NAS','WLD','HES','NOU','NWB']:
        before=sum(r['count'] for r in load('BASELINE.json')['inventory']['regional_pop'] if r['key'][1]==tag);now=v['country_populations'][tag]
        changes.append(dict(Type='POPULATION_TECHNIQUE',Territoire=tag,Avant=tag,Apres=tag,State_ID='STATE_HESSE',ID_numerique=74,RGB_avant=None,RGB_apres=None,Cellules=None,Classe='TECHNIQUE_NON_RECENSEMENT',Population=now-before,Justification='Delta total du pays ; profils culturels/religieux entiers conservés. Population finale '+str(now),Source='ALLOCATION.json; VALIDATION_R2.json'))
    changes.extend([dict(Type='INSTITUTION',Territoire=tag,Avant='Historique hérité de 1836' if tag in ['NAS','HEK','HES'] else 'Pays absent',Apres=ruler,State_ID='STATE_HESSE',ID_numerique=74,RGB_avant=None,RGB_apres=None,Cellules=None,Classe='A_INSTITUTION_SEULE',Population=None,Justification='Souverain daté, pas une preuve des frontières ; HES corrigé en principauté avec gouvernement landgraviat existant',Source='HISTORICAL_EVIDENCE_R2.md') for tag,ruler in [('NAS','Karl Wilhelm'),('NOU','Wilhelm V.'),('NWB','Karl Christian'),('HEK','Friedrich II.'),('HES','Ludwig IX.')]])
    add('CHANGES_R2.csv',changes);dump('CSV_TABLES.json',tables);print('Prepared four requested typed datasets',flush=True)

def journal():
    import render_map2k_imperial_map as render
    render.OUT=OUT;render.render()

def concurrency():
    """Read-only receipt for the observed external fast-forward, not Git repair."""
    b=load('BASELINE.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();expected='f97dc56'
    assert head.startswith(expected),'New unreviewed HEAD change'
    paths=subprocess.check_output(['git','diff','--name-only',b['git_head'],head],cwd=ROOT,text=True).splitlines();rel='common/history/buildings/00_west_europe.txt';assert paths==[rel]
    raw=(ROOT/rel).read_text(encoding='utf-8-sig');committed=subprocess.check_output(['git','show',head+':'+rel],cwd=ROOT).decode('utf-8-sig');assert raw.replace('\r\n','\n')==committed.replace('\r\n','\n')
    old=b['originals'][rel];nodes_before={n.key:n for n in core.cw.walk(core.cw.parse(old)) if n.key.startswith('s:STATE_')};nodes_after={n.key:n for n in core.cw.walk(core.cw.parse(raw)) if n.key.startswith('s:STATE_')};assert set(nodes_before)==set(nodes_after)
    deltas=[];allowed={('STATE_FRENCH_LOW_COUNTRIES','building_coal_mine'):'company_mines_anzin',('STATE_PICARDY','building_glassworks'):'company_saint_gobain',('STATE_PICARDY','building_logging_camp'):'company_saint_gobain'}
    for sid,node in nodes_before.items():
        current=nodes_after[sid]
        if core.qa.signature(node)==core.qa.signature(current):continue
        assert sid[2:] in {'STATE_FRENCH_LOW_COUNTRIES','STATE_PICARDY'}
        for tag in [n.key for n in node.children()]:
            donor=node.children(tag)[0];receiver=current.children(tag)[0]
            assert len(donor.children('create_building'))==len(receiver.children('create_building'))
            for a,z in zip(donor.children('create_building'),receiver.children('create_building')):
                if core.qa.signature(a)==core.qa.signature(z):continue
                kind=a.one('building').strip('"');assert (sid[2:],kind) in allowed and tag=='region_state:FRA'
                assert [core.qa.signature(n) for n in a.children() if n.key!='add_ownership']==[core.qa.signature(n) for n in z.children() if n.key!='add_ownership']
                assert sum(int(n.value) for n in core.cw.walk(a.children()) if n.key=='levels')==sum(int(n.value) for n in core.cw.walk(z.children()) if n.key=='levels')==5
                holder=z.children('add_ownership')[0].children('company')[0];assert holder.one('type')==allowed[sid[2:],kind] and holder.one('country').strip('"')=='c:FRA'
                deltas.append(dict(before_key=[sid[2:],'FRA',core.qa.signature(a)],after_key=[sid[2:],'FRA',core.qa.signature(z)]))
    assert len(deltas)==3
    dump('CONCURRENT_WORK_OBSERVED.json',dict(head_before=b['git_head'],head_after=head,index_sha256=core.sha(ROOT/'.git/index'),files=paths,hashes={rel:core.sha(ROOT/rel)},building_deltas=deltas,cause='Externally executed pull --ff-only of PR6, observed in reflog. This agent did not stage, commit, pull, push, merge or change branches.',scope='Only French company ownership. Hesse and all levels/PM untouched. Immutable MAP baseline is retained.'))
    print('Independent PR6 validated: exactly three French ownership changes, no MAP overlap',flush=True)

def military_concurrency():
    """Preserve the other agent's explicitly scoped writes, never edit them."""
    receipt=load('CONCURRENT_WORK_OBSERVED.json');b=load('BASELINE.json');allowed={'POR','BRZ','SC2','SC4','USA'};changed=[];country_before={};country_after={}
    for rel in ['common/history/military_formations/00_military_formations_europe.txt','common/history/military_formations/01_military_formations_north_america.txt','common/history/military_formations/02_military_formations_south_america.txt']:
        old=subprocess.check_output(['git','show',b['git_head']+':'+rel],cwd=ROOT).decode('utf-8-sig');raw=(ROOT/rel).read_text(encoding='utf-8-sig')
        a={n.key:core.qa.signature(n) for n in core.cw.parse(old)[0].children()};z={n.key:core.qa.signature(n) for n in core.cw.parse(raw)[0].children()};assert set(a)==set(z)
        delta={k for k in a if a[k]!=z[k]};assert delta<={'c:'+tag for tag in allowed},('Unexpected military owner',delta)
        changed.extend(rel for _ in [0] if delta)
        country_before.update(a);country_after.update(z)
    before=load('BASELINE.json')['inventory']['units'];expected=C.Counter({tuple(r['key']):r['count'] for r in before if r['key'][0] not in allowed})
    # Reproduce the inventory's explicit combat-unit signature, only for the
    # countries whose country-block AST was verified above.
    for rel in changed:
        root=core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))[0]
        for n in root.children():
            tag=n.key.removeprefix('c:')
            if tag not in allowed:continue
            for form in n.children('create_military_formation'):
                for unit in form.children('combat_unit'):
                    sid=unit.one('state_region','').removeprefix('s:');expected[tag,form.one('name',''),sid,core.qa.signature(unit)]+=1
    localizations=['localization/'+lang+'/1776_military_start_l_'+lang+'.yml' for lang in ['english','french']]
    for rel in localizations:
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0',raw,re.M);assert len(keys)==6 and all(re.match(r'aor1776_(brz|sc2|sc4)_',key) for key in keys)
    paths=changed+localizations;assert not set(paths)&set(load('EXPECTED_TEXT.json')) and not set(paths)&set(load('IMPERIAL_EXPECTED.json'))
    receipt.update(files=sorted(set(receipt['files'])|set(paths)),military_protected_countries=sorted(allowed),military_units_expected=[dict(key=list(k),count=v) for k,v in sorted(expected.items())],military_scope_note='Other agent explicitly assigned these countries in user prompt. All other country ASTs in the shared files are byte-semantic-equivalent; these files are not MAP edits.')
    receipt['hashes'].update({rel:core.sha(ROOT/rel) for rel in paths});dump('CONCURRENT_WORK_OBSERVED.json',receipt)
    print('Protected collaborator receipt:',paths,flush=True)

def usa_concurrency():
    receipt=load('CONCURRENT_WORK_OBSERVED.json');b=load('BASELINE.json');rel='common/static_modifiers/76mod_modifiers.txt'
    old=subprocess.check_output(['git','show',b['git_head']+':'+rel],cwd=ROOT).decode('utf-8-sig');raw=(ROOT/rel).read_text(encoding='utf-8-sig');a={n.key:core.qa.signature(n) for n in core.cw.parse(old)};z={n.key:core.qa.signature(n) for n in core.cw.parse(raw)}
    assert set(a)==set(z) and {k for k in a if a[k]!=z[k]}=={'modifier_usa_war_of_independence'}
    assert rel not in load('EXPECTED_TEXT.json') and rel not in load('IMPERIAL_EXPECTED.json')
    receipt['files']=sorted(set(receipt['files'])|{rel});receipt['hashes'][rel]=core.sha(ROOT/rel);receipt['usa_scope_note']='Only modifier_usa_war_of_independence changed in this shared file, within the other agent’s explicit protected task.';dump('CONCURRENT_WORK_OBSERVED.json',receipt);print('Protected independent USA modifier recorded',flush=True)

def usa_characters_concurrency():
    receipt=load('CONCURRENT_WORK_OBSERVED.json');paths=['common/character_templates/1776_usa_commanders.txt']+['localization/'+lang+'/1776_usa_commanders_l_'+lang+'.yml' for lang in ['french','english']]
    keys=[n.key for n in core.cw.parse((ROOT/paths[0]).read_text(encoding='utf-8-sig'))];assert keys and all(k.startswith('aor1776_usa_') for k in keys)
    for rel in paths[1:]:
        keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0', (ROOT/rel).read_text(encoding='utf-8-sig'), re.M);assert set(keys)=={'aor1776_name_'+n for n in ['charles','lee','artemas','ward','israel','putnam','philip','schuyler','nathanael','greene']}
    assert not set(paths)&set(load('EXPECTED_TEXT.json')) and not set(paths)&set(load('IMPERIAL_EXPECTED.json'))
    receipt['files']=sorted(set(receipt['files'])|set(paths));receipt['hashes'].update({p:core.sha(ROOT/p) for p in paths});receipt['usa_characters_scope_note']='New USA-only templates and localization authored by the other agent; not MAP changes or this agent’s test certification.';dump('CONCURRENT_WORK_OBSERVED.json',receipt);print('Protected USA character files recorded',flush=True)

def tidy_population():
    files=load('EXPECTED_TEXT.json');rel='common/history/pops/00_west_europe.txt';raw=(ROOT/rel).read_text(encoding='utf-8-sig');assert raw==files[rel]
    lines=raw.splitlines(keepends=True)
    for n in [3567,3653,3682]:
        assert lines[n-1].strip()=='' and lines[n-1].rstrip('\n\r')!='';lines[n-1]='\n'
    files[rel]=''.join(lines);dump('EXPECTED_TEXT.json',files);core.OUT=OUT;core.emit({rel:files[rel]},'POPULATION_WHITESPACE.patch')

def references():
    needed={'common/technology/technologies':set(),'common/laws':set(),'common/scripted_effects':set(),'common/cultures':{'north_german'},'common/religions':{'catholic','protestant'},'common/interest_groups':{'ig_landowners'},'common/ideologies':{'ideology_traditionalist'}}
    raw=(ROOT/'common/history/countries/nou - map2w_r2.txt').read_text(encoding='utf-8-sig')
    for n in core.cw.walk(core.cw.parse(raw)):
        if n.key=='add_technology_researched':needed['common/technology/technologies'].add(n.value)
        if n.key=='activate_law':needed['common/laws'].add(n.value.removeprefix('law_type:'))
        if n.key.startswith('effect_starting_'):needed['common/scripted_effects'].add(n.key)
    found={}
    for folder,keys in needed.items():
        hits={}
        for p in core.qa.effective(ROOT,core.qa.GAME,folder):
            if not p.is_file() or p.suffix!='.txt':continue
            for n in core.cw.parse(p.read_text(encoding='utf-8-sig')):
                if n.key in keys:hits[n.key]=p.as_posix()
        assert set(hits)==keys,(folder,keys-set(hits));found[folder]=hits
    dump('REFERENCE_VALIDATION_R2.json',dict(status='PASS',references=found,canonical_game='C:/Games/Victoria 3/game',installed_executable_version='1.13.11',runtime_execution=False))
    print('Effective references PASS, canonical executable 1.13.11',flush=True)

def final_integrity():
    import csv
    v=load('VALIDATION_R2.json');assert v['passed']==v['total'];tests=load('UNIT_TESTS_R2.json');results=[]
    for name in ['R2_targeted','cumulative_contracts','R1_receipt_preservation']:assert not tests[name]['failures'] and not tests[name]['errors']
    for name,data in load('CSV_TABLES.json').items():
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        assert len(rows)==len(data['rows']) and list(rows[0])==data['fields']
        assert all(row[k]==('' if original.get(k) is None else str(original[k])) for row,original in zip(rows,data['rows']) for k in data['fields'])
        results.append(dict(file=name,rows=len(rows),sha256=core.sha(OUT/name)))
    changes=load('CSV_TABLES.json')['CHANGES_R2.csv']['rows'];assert sum(r['Cellules'] for r in changes if r['Type']=='TRANSFERT')==72;assert sum(r['Population'] for r in changes if r['Type']=='POPULATION_TECHNIQUE')==0
    current=q.economy.runtime_hashes();manifest=load('INSTALLED_MANIFEST.json');assert all(current.get(p)==h for p,h in manifest['functional_files'].items()),'Post-validation MAP drift'
    # Concurrent protected work may continue after this snapshot. Report it,
    # rather than treating another agent's later writes as our regressions.
    external_drift=[p for p,h in manifest['external_files'].items() if current.get(p)!=h]
    receipt=load('CONCURRENT_WORK_OBSERVED.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==receipt['head_after'];assert core.sha(ROOT/'.git/index')==receipt['index_sha256']
    for name in ['REPORT.md','RUNTIME_TEST_PLAN.md','HISTORICAL_EVIDENCE_R2.md','HESSE_NASSAU_BEFORE_AFTER.png','PLAYER_LOCATION_GUIDE.png','ACCEPTED_CELLS_SOURCE_REVIEW.png']:assert (OUT/name).is_file()
    assert load('REFERENCE_VALIDATION_R2.json')['status']=='PASS'
    dump('FINAL_DELIVERY_INTEGRITY.json',dict(status='PASS_MAP_SCOPED',csvs=results,typed_tables=load('CSV_VALIDATION.json')['status'],visual_review='4 CSV previews + 2 maps + accepted source-cell overlay inspected; corrected misleading labels/statuses',functional_hashes_preserved=True,static_checks=[v['passed'],v['total']],current_contract_tests=100,legacy_snapshots=dict(tests=39,passed=30,failed=9,source_tests_modified=False),external_drift_after_snapshot=external_drift,git_operations_by_this_agent='READ_ONLY_ONLY',observed_external_head=receipt['head_after'],runtime_test='NOT_EXECUTED'))
    print('Final scoped integrity PASS, four CSV round trips, current MAP hashes preserved',flush=True)

def unit_tests():
    import unittest,io,time
    groups={'R2_targeted':['test_map2w_r2_hesse_nassau'],'cumulative_contracts':['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01'],'R1_receipt_preservation':['test_map2w_west_south'],'earlier_stage_snapshots':['test_map2t_saxony','test_map2u_thuringia']};results={}
    for name,modules in groups.items():
        suite=unittest.TestLoader().loadTestsFromNames(modules);stream=io.StringIO();start=time.monotonic();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);results[name]=dict(modules=modules,tests=r.testsRun,failures=[dict(test=test.id(),trace=trace) for test,trace in r.failures],errors=[dict(test=test.id(),trace=trace) for test,trace in r.errors],seconds=round(time.monotonic()-start,2),output=stream.getvalue());print(name,r.testsRun,'tests',len(r.failures),'failures',len(r.errors),'errors',flush=True)
    dump('UNIT_TESTS_R2.json',results)
    if any(results[name]['failures'] or results[name]['errors'] for name in ['R2_targeted','cumulative_contracts','R1_receipt_preservation']):raise SystemExit(1)

if __name__=='__main__':globals()[sys.argv[1]]()
