"""MAP2W bounded continuation; captures are immutable and earlier lots stay frozen."""
import collections as C
import json, re, subprocess, sys, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
import map2u_thuringia as prior
core=prior.core; q=prior.q; ROOT=prior.ROOT
OUT=ROOT/'docs/reports/map/MAP2W'
REGIONS=['STATE_HESSE','STATE_SAXONY']

def dump(name,data):
    (OUT/name).parent.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Do not replace the original capture'
    inv=core.qa.inventory();originals={}
    for folder in ['common/history','map_data/state_regions']:
        for p in (ROOT/folder).rglob('*.txt'):
            raw=p.read_text(encoding='utf-8-sig')
            if any(sid in raw for sid in REGIONS):originals[p.relative_to(ROOT).as_posix()]=raw
    bitmap=prior.OUT/'provinces_candidate.png'
    assert core.sha(bitmap)==core.sha(ROOT/'map_data/provinces.png'),'Capture changed bitmap separately before proceeding'
    paths=['tools/map2l_registry.py','tools/map2k_imperial_system.py','tools/hre_centralization_01.py','tools/hre_subject_feedback_01.py','tools/hre_secession_lens_01.py']
    dump('BASELINE.json',dict(inventory=inv,originals=originals,hashes=q.economy.runtime_hashes(),bitmap_backup=bitmap.relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(bitmap),registry=json.loads(core.active_registry_path().read_text(encoding='utf8')),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=core.sha(ROOT/'.git/index'),tool_originals={p:(ROOT/p).read_text(encoding='utf8') for p in paths}))
    print('Captured world',sum(r['count'] for r in inv['pops']),'registry',len(load('BASELINE.json')['registry']),'core',core.__file__,flush=True)

def fetch():
    evidence=OUT/'EVIDENCE';evidence.mkdir(parents=True,exist_ok=True)
    url='https://www.lagis-hessen.de/de/api/idrecng/sn/geschichtlicher-atlas-von-hessen/id/40'
    data=json.loads(urllib.request.urlopen(url,timeout=30).read())
    dump('EVIDENCE/LAGIS_40_metadata.json',data)
    source='https://www.lagis-hessen.de'+data['sheetData']['path']
    dest=evidence/'Hessen_1789_Uhlhorn.jpg'
    if not dest.exists():dest.write_bytes(urllib.request.urlopen(source,timeout=40).read())
    im=Image.open(dest);print(source,im.size,flush=True)
    im.thumbnail((1235,1634));im.save(evidence/'Hessen_1789_overview.png')

def compiler_before():
    old=prior.t.OUT;prior.t.OUT=OUT
    try:prior.t.compiler_before()
    finally:prior.t.OUT=old

def inspect():
    im=Image.open(OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB')
    box=(2750,2130,3700,3180);crop=im.crop(box);d=ImageDraw.Draw(crop)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for x in range(2800,3700,100):
        d.line((x-box[0],0,x-box[0],crop.height),fill='blue');d.text((x-box[0]+2,0),str(x),font=f,fill='blue',stroke_width=2,stroke_fill='white')
    for y in range(2200,3180,100):
        d.line((0,y-box[1],crop.width,y-box[1]),fill='blue');d.text((0,y-box[1]+2),str(y),font=f,fill='blue',stroke_width=2,stroke_fill='white')
    crop.save(OUT/'EVIDENCE/FULDA_READING.png')
    b=load('BASELINE.json');a=core.packed(ROOT/b['bitmap_backup']);owner={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    rows=[]
    for color in np.unique(a[830:861,4305:4339]):
        rgb='x'+format(int(color),'06X');ys,xs=np.where(a==color)
        rows.append(dict(rgb=rgb,owner=owner.get(rgb),pixels=len(xs),box=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]))
    dump('CURRENT_PROVINCES.json',rows)
    dump('LOCATORS_BEFORE.json',[r for r in q.r9.locators(a) if r['ID']==74])
    print(json.dumps(rows,ensure_ascii=False),flush=True)

def inventory():
    """Historical worklist, not a claim of an exhaustive cadastre or new research."""
    b=load('BASELINE.json');inv=b['inventory'];rows=[]
    from map2l_registry import approved_lot_dirs
    migrations=[(p,json.loads((p/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))) for p in approved_lot_dirs()]
    groups=[
     ('Rhin–Westphalie','MAP2L/RHINE_WESTPHALIA_COMPLETION','Électorat de Cologne|Electorate of Cologne|Kurköln|KCL|électorat ecclésiastique;Électorat de Trèves|Electorate of Trier|Kurtrier|KTR|électorat ecclésiastique;Palatinat électoral|Electoral Palatinate|Kurpfalz|KPF|électorat laïque;Duché de Clèves|Duchy of Cleves|Herzogtum Kleve|PRU|possession prussienne;Comté de la Mark|County of Mark|Grafschaft Mark|PRU|possession prussienne;Comté de Ravensberg|County of Ravensberg|Grafschaft Ravensberg|PRU|possession prussienne;Principauté de Minden|Principality of Minden|Fürstentum Minden|PRU|possession prussienne;Gueldre prussienne|Prussian Guelders|Preußisch Geldern|PRU|possession prussienne;Duchés de Juliers et Berg|Duchies of Jülich and Berg|Jülich-Berg|JUB|possession dynastique palatine;Duché de Westphalie|Duchy of Westphalia|Herzogtum Westfalen|KCL|possession de Cologne;Vest Recklinghausen|Vest Recklinghausen|Vest Recklinghausen|KCL|possession de Cologne;Principauté épiscopale de Münster|Prince-Bishopric of Münster|Hochstift Münster|WPM|principauté ecclésiastique;Principauté épiscopale de Paderborn|Prince-Bishopric of Paderborn|Hochstift Paderborn|WPD|principauté ecclésiastique;Principauté épiscopale d’Osnabrück|Prince-Bishopric of Osnabrück|Hochstift Osnabrück|WPO|principauté ecclésiastique;Principauté de Liège|Prince-Bishopric of Liège|Hochstift Lüttich|LGE|principauté ecclésiastique;Comté de Lingen|County of Lingen|Grafschaft Lingen|PRU|possession prussienne;Comté de Tecklenburg|County of Tecklenburg|Grafschaft Tecklenburg|PRU|possession prussienne;Principauté de Lippe|Principality of Lippe|Lippe|LIP|comté en 1776, rang princier ultérieur;Comté de Schaumbourg-Lippe|County of Schaumburg-Lippe|Schaumburg-Lippe|SCM|comté immédiat;Comté de Bentheim|County of Bentheim|Bentheim||comté gagé au Hanovre;Comté de Steinfurt|County of Steinfurt|Steinfurt||comté immédiat;Comté de Rietberg|County of Rietberg|Rietberg||comté immédiat;Abbaye de Corvey|Imperial Abbey of Corvey|Reichsabtei Corvey||abbaye, pas évêché de 1792;Abbaye d’Essen|Imperial Abbey of Essen|Reichsstift Essen||abbaye immédiate;Abbaye de Werden|Imperial Abbey of Werden|Reichsabtei Werden||abbaye immédiate;Dortmund|Free Imperial City of Dortmund|Reichsstadt Dortmund||ville impériale'),
     ('Hesse–Nassau','MAP2Q/R3/HRE_REGIONS_INVENTORY_UPDATED.csv','Électorat de Mayence|Electorate of Mainz|Kurmainz|KMZ|électorat ecclésiastique;Hesse-Cassel|Hesse-Kassel|Hessen-Kassel|HEK|landgraviat;Hesse-Darmstadt|Hesse-Darmstadt|Hessen-Darmstadt|HES|landgraviat, pas grand-duché;Hesse-Hombourg|Hesse-Homburg|Hessen-Homburg||landgraviat;Hesse-Rotenbourg|Hesse-Rotenburg|Hessen-Rotenburg||apanage sous souveraineté de Cassel;Principauté épiscopale de Fulda|Prince-Bishopric of Fulda|Hochstift Fulda||principauté ecclésiastique;Waldeck|Waldeck|Waldeck|WLD|principauté;Francfort|Free Imperial City of Frankfurt|Reichsstadt Frankfurt|FRM|ville impériale;Nassau-Usingen|Nassau-Usingen|Nassau-Usingen|NAS|principauté, TAG agrégé;Nassau-Weilbourg|Nassau-Weilburg|Nassau-Weilburg|NAS|principauté, TAG agrégé;Nassau-Sarrebruck|Nassau-Saarbrücken|Nassau-Saarbrücken|NAS|principauté, TAG agrégé;Nassau-Orange|Orange-Nassau|Oranien-Nassau|NAS|possessions allemandes distinctes des Provinces-Unies;Solms|Solms counties|Solms||plusieurs comtés immédiats;Isembourg|Isenburg counties|Isenburg||plusieurs branches immédiates;Wittgenstein|Wittgenstein counties|Wittgenstein||plusieurs comtés immédiats;Wetzlar|Free Imperial City of Wetzlar|Reichsstadt Wetzlar||ville impériale;Worms|Prince-Bishopric of Worms|Hochstift Worms||territoire temporel distinct du diocèse;Spire|Prince-Bishopric of Speyer|Hochstift Speyer||territoire temporel distinct du diocèse'),
     ('Franconie','MAP2L/FRANCONIA_CONTINUATION','Würzburg|Prince-Bishopric of Würzburg|Hochstift Würzburg|WZB|principauté ecclésiastique;Bamberg|Prince-Bishopric of Bamberg|Hochstift Bamberg|FBM|principauté ecclésiastique;Ansbach|Margraviate of Ansbach|Brandenburg-Ansbach|ANS|margraviat, union personnelle avec Bayreuth;Bayreuth|Margraviate of Bayreuth|Brandenburg-Bayreuth|ANS|margraviat distinct, même souverain depuis 1769;Nuremberg|Free Imperial City of Nuremberg|Reichsstadt Nürnberg|NUR|ville impériale;Eichstätt|Prince-Bishopric of Eichstätt|Hochstift Eichstätt|EIC|principauté ecclésiastique;Hohenlohe|Hohenlohe principalities|Hohenlohe||plusieurs branches, pas un État unifié;Castell|Castell counties|Castell||plusieurs branches;Wertheim|Wertheim counties|Löwenstein-Wertheim||branches confessionnelles distinctes;Schweinfurt|Free Imperial City of Schweinfurt|Reichsstadt Schweinfurt||ville impériale;Rothenbourg|Free Imperial City of Rothenburg|Reichsstadt Rothenburg||ville impériale;Windsheim|Free Imperial City of Windsheim|Reichsstadt Windsheim||ville impériale;Wissembourg en Franconie|Free Imperial City of Weißenburg|Reichsstadt Weißenburg||ville impériale'),
     ('Souabe','MAP2L/SWABIA_COMPLETION','Wurtemberg|Duchy of Württemberg|Herzogtum Württemberg|WUR|duché;Bade|Margraviate of Baden|Markgrafschaft Baden|BAD|margraviat réuni en 1771, pas grand-duché;Hohenzollern-Hechingen|Hohenzollern-Hechingen|Hohenzollern-Hechingen|HOH|principauté;Hohenzollern-Sigmaringen|Hohenzollern-Sigmaringen|Hohenzollern-Sigmaringen|HSG|principauté;Fürstenberg|Principality of Fürstenberg|Fürstenberg|SFU|principauté;Ellwangen|Prince-Provostry of Ellwangen|Fürstpropstei Ellwangen|SEW|prévôté princière;Salem|Imperial Abbey of Salem|Reichsabtei Salem|SLM|abbaye;Weingarten|Imperial Abbey of Weingarten|Reichsabtei Weingarten|SWG|abbaye;Constance|Prince-Bishopric of Constance|Hochstift Konstanz|SKC|principauté ecclésiastique, pas ville autrichienne;Évêché d’Augsbourg|Prince-Bishopric of Augsburg|Hochstift Augsburg|SAG|principauté ecclésiastique;Ville d’Augsbourg|Free Imperial City of Augsburg|Reichsstadt Augsburg|SAC|ville impériale;Abbaye de Kempten|Prince-Abbey of Kempten|Fürststift Kempten|SKE|abbaye distincte de la ville;Ville de Kempten|Free Imperial City of Kempten|Reichsstadt Kempten|SKI|ville impériale;Ulm|Free Imperial City of Ulm|Reichsstadt Ulm|SUU|ville impériale;Reutlingen|Free Imperial City of Reutlingen|Reichsstadt Reutlingen|SRT|ville impériale;Biberach|Free Imperial City of Biberach|Reichsstadt Biberach|SBI|ville impériale;Memmingen|Free Imperial City of Memmingen|Reichsstadt Memmingen|SMM|ville impériale;Ravensbourg|Free Imperial City of Ravensburg|Reichsstadt Ravensburg|SRQ|ville impériale;Waldburg-Wolfegg|Waldburg-Wolfegg|Waldburg-Wolfegg|SWW|comté;Waldburg-Waldsee|Waldburg-Waldsee|Waldburg-Waldsee|SWX|comté;Waldburg-Wurzach|Waldburg-Wurzach|Waldburg-Wurzach|SWY|comté;Waldburg-Friedberg-Scheer|Waldburg-Friedberg-Scheer|Waldburg-Friedberg-Scheer|SWF|comté;Montbéliard|County of Montbéliard|Grafschaft Mömpelgard|WUR|possession séparée du Wurtemberg;Oettingen|Oettingen counties and principalities|Oettingen||branches distinctes;Esslingen|Free Imperial City of Esslingen|Reichsstadt Esslingen||ville impériale;Kaufbeuren|Free Imperial City of Kaufbeuren|Reichsstadt Kaufbeuren||ville impériale;Isny|Free Imperial City of Isny|Reichsstadt Isny||ville impériale;Lindau|Free Imperial City of Lindau|Reichsstadt Lindau||ville impériale'),
     ('Bavière','MAP2Q/R3/HRE_REGIONS_INVENTORY_UPDATED.csv','Bavière électorale|Electorate of Bavaria|Kurbayern|BAV|électorat, pas royaume;Freising|Prince-Bishopric of Freising|Hochstift Freising||principauté ecclésiastique;Passau|Prince-Bishopric of Passau|Hochstift Passau||principauté ecclésiastique;Évêché de Ratisbonne|Prince-Bishopric of Regensburg|Hochstift Regensburg||principauté ecclésiastique;Ville de Ratisbonne|Free Imperial City of Regensburg|Reichsstadt Regensburg||ville impériale;Saint-Emmeran|Imperial Abbey of Saint Emmeram|Reichsabtei Sankt Emmeram||abbaye;Berchtesgaden|Prince-Provostry of Berchtesgaden|Fürstpropstei Berchtesgaden||prévôté princière;Ortenbourg|County of Ortenburg|Reichsgrafschaft Ortenburg||comté immédiat;Salzbourg|Prince-Archbishopric of Salzburg|Erzstift Salzburg|SAL|principauté ecclésiastique')]
    urls={'Rhin–Westphalie':'https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=160&url_tabelle=tab_karte','Hesse–Nassau':'https://lagis.hessen.de/resolve/de/ga/40','Franconie':'MAP2L/FRANCONIA/GEOGRAPHIC_EVIDENCE.md; MAP2L/FRANCONIA/REPORT.md','Souabe':'https://www.leo-bw.de/themen/historischer-atlas-von-baden-wurttemberg','Bavière':'https://www.historisches-lexikon-bayerns.de/'}
    for sector,doc,entities in groups:
        for entry in entities.split(';'):
            fr,en,de,tag,kind=entry.split('|');exists=tag in inv['countries'];lots=[p.relative_to(ROOT/'docs/reports/map').as_posix() for p,m in migrations if tag and (tag in m['new_members'] or any(r.get('beneficiary')==tag for r in m['updated']))]
            installed=exists and bool(lots);states=sorted({r['key'][1] for r in inv['owners'] if tag and r['key'][2]==tag})
            status='NOYAU_INSTALLE_RESIDUS_NON_CERTIFIES' if installed else 'PRESENT_NON_RECONSTRUIT' if exists else 'ABSENT_OU_ABSTRAIT_A_VERIFIER'
            if tag=='NAS':status='AGREGATION_DE_BRANCHES_A_RESOUDRE'
            if fr=='Montbéliard':status='C_GEOGRAPHIE_DIFFEREE'
            sovereign={'Bavière électorale':'Maximilien III Joseph','Palatinat électoral':'Charles Théodore','Principauté épiscopale de Fulda':'Heinrich VIII von Bibra','Hesse-Cassel':'Frédéric II','Hesse-Darmstadt':'Louis IX','Bade':'Charles-Frédéric','Wurtemberg':'Charles-Eugène','Ansbach':'Christian Frédéric Charles Alexandre','Bayreuth':'Christian Frédéric Charles Alexandre'}.get(fr,'Non vérifié dans cette passe')
            rows.append(dict(Secteur=sector,Nom_FR=fr,Nom_EN=en,Nom_DE=de,Nature_1776=kind,Souverain_1776=sovereign,Statut_imperial='Territoire du Saint-Empire; statut propre et droits non déduits du TAG',TAG_actuel=tag if exists else None,Regions_actuelles=';'.join(states),Representation=status,Classe='B' if installed else 'C',Lots_installation=';'.join(lots),Documentation='docs/reports/map/'+doc,Source_historique=urls[sector],Limite='Noyaux antérieurs protégés; pas une certification complète des frontières' if installed else 'Attribution détaillée et correspondance RGB non établies; aucune modification automatique'))
    # Verify branch names against the actual installed, localized definitions.
    actual={'SWW':('Waldburg-Wolfegg-Waldsee','Waldburg-Wolfegg-Waldsee'), 'SWF':('Waldburg-Wolfegg-Wolfegg','Waldburg-Wolfegg-Wolfegg'), 'SWX':('Waldburg-Zeil-Wurzach','Waldburg-Zeil-Wurzach'), 'SWY':('Waldburg-Zeil-Trauchburg','Waldburg-Zeil-Trauchburg')}
    for row in rows:
        if row['TAG_actuel'] in actual:
            name=actual[row['TAG_actuel']][0];row.update(Nom_FR=name,Nom_EN=name,Nom_DE=name)
        if row['Nom_FR']=='Duchés de Juliers et Berg':
            row.update(TAG_actuel='KPF',Representation='NOYAUX_INSTALLES_SOUS_SOUVERAIN_PALATIN',Classe='B',Documentation='docs/reports/map/MAP2L/RHINE_WESTPHALIA/REPORT.md',Limite='Duchés distincts sous le souverain palatin; ne pas créer un TAG fictif JUB.')
        # A tag can own dozens of unrelated territories. Its participation in
        # one migration never validates all jurisdictions bearing that tag.
        if row['Nom_FR'] in ['Duché de Clèves','Comté de la Mark','Gueldre prussienne','Hesse-Cassel','Hesse-Darmstadt','Waldeck','Francfort','Montbéliard','Bavière électorale']:
            row.update(Classe='C',Representation='PRESENT_OU_AGREGE_SECTEUR_NON_RECONSTRUIT',Lots_installation=None,Limite='Pays présent, mais pas de reconstruction dédiée de ce territoire établie; préserver la situation existante en attendant une preuve ciblée.')
        if row['TAG_actuel']=='LGE':row.update(Classe='B',Representation='NOYAU_BELGE_ANTERIEUR_PROTEGE',Lots_installation='MAP2L/BELGIUM',Documentation='docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json',Limite='Ne pas reprendre le lot belge; les franges ne sont pas toutes certifiées.')
        if row['Nom_FR']=='Comté de Schaumbourg-Lippe':row['Limite']='Pays distinct préservé; pas une certification de toutes les frontières.'
        if row['TAG_actuel']=='LIP':row.update(Nom_FR='Comté de Lippe',Nom_EN='County of Lippe',Nom_DE='Grafschaft Lippe')
    # Every requested entity remains explicit even where no independent detailed
    # work has been completed. A catalog link is a lead, not a boundary proof.
    discrepancies=[dict(Entite=r['Nom_FR'],Secteur=r['Secteur'],TAG=r['TAG_actuel'],Etat=r['Representation'],Probleme=('Limites périphériques restent approximatives, ne pas refaire le noyau' if r['Classe']=='B' else 'Absence, agrégation ou représentation encore non vérifiée'),Action='PROTEGER' if r['Classe']=='B' else 'DIFFERER_SOUS_LOT_CIBLE',Source=r['Documentation']) for r in rows]
    for row in discrepancies:
        if row['TAG'] in ['BAV','BAD','HES']:
            row['Probleme']+='; rang natif '+('kingdom' if row['TAG']=='BAV' else 'grand_principality')+' encore anachronique pour 1776; ne pas confondre rang technique et titre historique'
    unresolved=[dict(Secteur=r['Secteur'],Entite=r['Nom_FR'],Classe='C',Probleme=r['Limite'],Suite='Sous-lot ciblé; pas de transfert MAP2W sans preuve territoriale',Source=r['Documentation']) for r in rows if r['Classe']=='C']
    unresolved.append(dict(Secteur='Erfurt–Eichsfeld',Entite='Mayence',Classe='C',Probleme='Calage non validé, translation 7,20 pixels rejetée',Suite='Aucun changement',Source='MAP2L/ERFURT_EICHSFELD'))
    tables={'INVENTORY_1776.csv':rows,'DISCREPANCIES.csv':discrepancies,'UNRESOLVED.csv':unresolved}
    dump('CSV_TABLES.json',{name:dict(fields=list(r[0]),rows=r) for name,r in tables.items()})
    if not (OUT/'INVENTORY_PHASE.json').exists():dump('INVENTORY_PHASE.json',dict(phase='BEFORE_FUNCTIONAL_EDITS',entities=len(rows),protected_core_entries=sum(r['Classe']=='B' for r in rows),remaining_entries=sum(r['Classe']=='C' for r in rows),historical_inventory_limit='Identified principal jurisdictions only; groups such as Hohenlohe/Solms require branch inventories. Not an exhaustive microstate register.',baseline_head=b['git_head']))
    print('Historical/documentation worklist',len(rows),'entities',flush=True)

def geometry():
    from georeference.model import forward
    b=load('BASELINE.json');before=core.packed(ROOT/b['bitmap_backup'])
    model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text(encoding='utf8'))['model']
    controls=[('Fulda',3128,2747,9.6808,50.5558),('Hünfeld',3258,2472,9.7674,50.6725),('Neuhof',3047,2949,9.6175,50.4528),('Geisa',3502,2362,9.95,50.7156),('Gersfeld',3500,2966,9.9196,50.4499),('Schlitz',2965,2486,9.5611,50.6744)]
    source=np.array([[x,y,1] for _,x,y,_,_ in controls]);target=forward(model,[[lon,lat] for _,_,_,lon,lat in controls]);tr=np.linalg.lstsq(source,target,rcond=None)[0]
    # An inward core, never the complete 1789 purple extent: omit Geisa,
    # Dermbach, detached Herbstein, Tann and noble/knightly jurisdictions.
    poly=[(3100,2450),(3190,2410),(3280,2490),(3350,2550),(3310,2640),(3400,2735),(3360,2800),(3315,2860),(3370,2910),(3320,2990),(3200,2975),(3140,3010),(3100,2990),(3070,3050),(2990,3040),(2910,2960),(2910,2870),(2900,2810),(2940,2740),(2940,2690),(2990,2660),(3090,2620),(3075,2570)]
    mapped=np.column_stack([poly,np.ones(len(poly))])@tr
    xmin,ymin=np.floor(mapped.min(axis=0)).astype(int);xmax,ymax=np.ceil(mapped.max(axis=0)).astype(int)
    yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx.ravel();yy=yy.ravel();selected=core.inside(np.column_stack([xx+.5,yy+.5]),mapped)
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']};labels={};excluded=[]
    for x,y in zip(xx[selected],yy[selected]):
        rgb='x'+format(int(before[y,x]),'06X');sid,tag=owners[rgb]
        if (sid=='STATE_HESSE' and tag=='HEK' and rgb=='xD04121') or (sid=='STATE_SAXONY' and tag=='MEI' and rgb=='xD0C021'):
            labels[int(x),int(y)]='FUL'
        else:excluded.append(dict(cell=[int(x),int(y)],rgb=rgb,state=sid,owner=tag))
    assert labels,'No justified Hesse cells intersect the conservative core'
    parents=sorted({'x'+format(int(before[y,x]),'06X') for x,y in labels});after=before.copy();assignments=[];new=[];used=set(map(int,np.unique(before)));color=0xEDB600
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
    dump('GEOMETRY.json',dict(parents=parents,assignments=assignments,new_provinces=new,traces=[dict(tag='FUL',name='Fulda–Hünfeld–Neuhof inward core',source_polygon=poly,game_polygon=mapped.tolist(),included=[list(p) for p in labels],excluded=excluded)],new_members=['FUL'],hub_rebindings=[],protected_saxon_new_RGB='xEDB40F',residual_extension='Only unchanged C residual xD0C021, never the reviewed GOT enclave xEDB40F or other MAP2T/U nuclei'))
    dump('SOURCE_ALIGNMENT.json',dict(transform=tr.tolist(),controls=[dict(name=n,source=[x,y],geo=[lon,lat],diagnostic_pixel=p.tolist(),sheet_residual=float(np.linalg.norm(np.array([x,y,1])@tr-p))) for (n,x,y,lon,lat),p in zip(controls,target)],independent_native_error_bound_px=None,warning='Sheet fit only. Native diagnostic uncertainty remains; no recalibration or 7.20px shift.',source='Uhlhorn 1962, Hessen 1789, HIL CC BY-SA 4.0; conservative main core only, not later annexations'))
    im=Image.open(OUT/'EVIDENCE/Hessen_1789_Uhlhorn.jpg').convert('RGB');d=ImageDraw.Draw(im);d.line(poly+[poly[0]],fill='blue',width=6);im.crop((2750,2130,3700,3180)).save(OUT/'EVIDENCE/FULDA_TRACING_REVIEW.png')
    print('Fulda core',len(labels),'cells; parents',parents,'new RGB',len(new),'excluded old owners',dict(C.Counter(r['owner'] for r in excluded)),flush=True)

def prepare():
    b=load('BASELINE.json');g=load('GEOMETRY.json');files={};bindings=[]
    assert (OUT/'INVENTORY_PHASE.json').exists(),'Inventory must precede functional edits'
    assert load('COMPILER_BEFORE.json')['passed']==73
    current=q.economy.runtime_hashes();ref=load('REFINEMENT_CAPTURE.json') if (OUT/'REFINEMENT_CAPTURE.json').exists() else None;reference=ref['runtime_hashes'] if ref else b['hashes'];drift=[p for p in set(current)|set(reference) if current.get(p)!=reference.get(p)]
    assert not drift,'Unexpected concurrent runtime changes: '+str(drift)
    assert 'FUL' not in b['inventory']['countries']
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png')
    groups=C.defaultdict(list)
    for a in g['assignments']:groups[a['parent_rgb']].append(a)
    rel='common/history/states/00_states.txt';raw=b['originals'][rel];ops=[]
    for sid,tag in [('STATE_HESSE','HEK'),('STATE_SAXONY','MEI')]:
        s=core.state(raw,sid);donor=next(n for n in s.children('create_state') if n.one('country')=='c:'+tag);f=donor.children('owned_provinces')[0];owned=[]
        for rgb in core.values(donor,'owned_provinces'):owned.extend(a['rgb'] for a in groups[rgb] if a['owner']==tag) if rgb in groups else owned.append(rgb)
        ops.extend([(f.start,f.end,'owned_provinces = { '+' '.join(owned)+' }'),(s.end-1,s.end-1,'\ncreate_state = { country = c:FUL owned_provinces = { '+' '.join(a['rgb'] for a in g['assignments'] if a['owner']=='FUL' and a['state']==sid)+' } }\n')])
    files[rel]=core.edits(raw,sorted(ops))
    locs=[r for r in q.r9.locators(before) if r['ID'] in [73,74]];dump('LOCATORS_BEFORE.json',locs)
    for rel,raw in b['originals'].items():
        if not rel.startswith('map_data/state_regions/'):continue
        ops=[]
        for node in core.cw.parse(raw):
            if node.key not in REGIONS:continue
            for field in ['provinces','prime_land']:
                for f in node.children(field):
                    old=core.values(node,field);new=[]
                    for rgb in old:new.extend(a['rgb'] for a in groups[rgb]) if rgb in groups else new.append(rgb)
                    if old!=new:
                        ops.append((f.start,f.end,field+' = { '+' '.join('"'+c+'"' for c in new)+' }'))
                        if field=='prime_land':bindings.append(dict(state=node.key,field=field,before=old,after=new))
            for loc in locs:
                if loc['ID']!={'STATE_HESSE':74,'STATE_SAXONY':73}[node.key]:continue
                x,y=int(loc['X']),int(loc['Y']);rgb='x'+format(int(after[y,x]),'06X');old=core.cw.scalar(node.one(loc['Kind']))
                if old!=rgb:
                    f=node.children(loc['Kind'])[0];ops.append((f.start,f.end,loc['Kind']+' = "'+rgb+'"'));bindings.append(dict(state=node.key,field=loc['Kind'],before=old,after=rgb,pixel=[x,y],bitmap_before='x'+format(int(before[y,x]),'06X')))
        if ops:files[rel]=core.edits(raw,sorted(ops))
    owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    weights={};allocations=[]
    for sid,tag in [('STATE_HESSE','HEK'),('STATE_SAXONY','MEI')]:
        total=sum(int(np.sum(before==int(rgb[1:],16))) for rgb,st in owners.items() if st==[sid,tag]);count=sum(a['pixels'] for a in g['assignments'] if a['owner']=='FUL' and a['state']==sid);weights[sid]={tag:total-count,'FUL':count}
    for rel,raw in b['originals'].items():
        if '/pops/' not in rel:continue
        ops=[];pieces=C.defaultdict(list)
        for sid,tag in [('STATE_HESSE','HEK'),('STATE_SAXONY','MEI')]:
            try:node=core.region(raw,sid,tag)
            except (StopIteration,IndexError):continue
            for pop in node.children('create_pop'):
                f=pop.children('size')[0];amounts=core.allocate(int(f.value),weights[sid]);ops.append((f.start,f.end,'size = '+str(amounts[tag])))
                if amounts['FUL']:pieces[sid].append(core.edits(raw[pop.start:pop.end],[(f.start-pop.start,f.end-pop.start,'size = '+str(amounts['FUL']))]))
                allocations.append(dict(state=sid,donor=tag,culture=pop.one('culture'),religion=pop.one('religion','DEFAULT:'+pop.one('culture')),before=int(f.value),after=amounts))
        if ops:
            text=core.edits(raw,sorted(ops))
            for sid,parts in pieces.items():text=core.append(text,sid,'FUL','\n'.join(parts))
            files[rel]=text
    assert allocations
    dump('POPULATION_ALLOCATION.json',dict(method='PROVISIONAL_TECHNICAL_REDISTRIBUTION_NOT_1776_CENSUS',weights=weights,profiles=allocations,historical_population=None,warning='Existing cultural/religious profiles retained; not a demographic reconstruction of Catholic Fulda.'))
    rel='map_data/province_terrains.txt';raw=ref['expected_text'][rel] if ref else (ROOT/rel).read_text(encoding='utf-8-sig')
    if ref:
        for a in ref['geometry']['new_provinces']:raw=re.sub(r'(?im)^'+a['rgb']+r'\s*=\s*"[^"\n]+"\s*\n?','',raw)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw+'\n'+''.join(a['rgb']+'="'+terrain[a['parent_rgb'].upper()]+'"\n' for a in g['new_provinces'])
    previous=[r for r in b['registry'] if r['state'] in REGIONS];updated=[r for r in previous if r['rgb'] not in g['parents']]+[dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2W-R1 Fulda-Hünfeld-Neuhof inward B core; C residual preserved; see GEOMETRY.json.') for a in g['assignments']]
    ledger=sorted([r for r in b['registry'] if r['state'] not in REGIONS]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    defs='FUL = { color = { 152 107 182 } country_type = recognized tier = principality cultures = { north_german } religion = catholic capital = STATE_SAXONY }\n'
    files['common/country_definitions/1776_map2w_fulda.txt']=defs
    files['common/history/countries/ful - map2w.txt']=(ROOT/'common/history/countries/wzb - franconian estate.txt').read_text(encoding='utf-8-sig').replace('c:WZB','c:FUL')
    files['common/history/characters/ful - map2w.txt']='CHARACTERS = { c:FUL ?= { create_character = { first_name = aor1776_map2w_heinrich last_name = aor1776_map2w_bibra historical = yes culture = north_german religion = rel:catholic ruler = yes birth_date = 1711.8.22 interest_group = ig_devout ideology = ideology_traditionalist } } }\n'
    files['common/government_types/00_1776_map2w_fulda.txt']='gov_aor1776_map2w_fulda = { transfer_of_power = dictatorial male_ruler = "RULER_TITLE_PRINCE_BISHOP" female_ruler = "RULER_TITLE_PRINCE_BISHOP" possible = { c:FUL ?= this has_law = law_type:law_theocracy } on_government_type_change = { change_to_dictatorial = yes } on_post_government_type_change = { post_change_to_dictatorial = yes } }\n'
    # Reuse the native black cross asset. This is a provisional plain banner,
    # not a fabricated full heraldic reconstruction of Heinrich von Bibra.
    files['common/flag_definitions/1776_map2w_fulda.txt']='FUL = { flag_definition = { coa = aor1776_map2w_fulda priority = 100 allow_overlord_canton = no } }\n'
    files['common/coat_of_arms/coat_of_arms/1776_map2w_fulda.txt']='aor1776_map2w_fulda = { pattern = "pattern_cross.dds" color1 = "white" color2 = "black" }\n'
    for lang in ['french','english']:
        fr=lang=='french';desc=('Le prince-évêque exerce l’autorité temporelle sur les possessions de Fulda. Le chapitre élit le titulaire de cette principauté ecclésiastique de l’Empire.' if fr else 'The prince-bishop exercises temporal authority over the possessions of Fulda. The chapter elects the ruler of this ecclesiastical principality of the Empire.')
        name='Principauté épiscopale de Fulda' if fr else 'Prince-Bishopric of Fulda';gov='Principauté épiscopale' if fr else 'Prince-bishopric'
        files[f'localization/{lang}/1776_map2w_l_{lang}.yml']='\ufeffl_'+lang+':\n FUL:0 "'+name+'"\n FUL_ADJ:0 "'+('de Fulda' if fr else 'Fuldan')+'"\n aor1776_map2w_heinrich:0 "Heinrich VIII."\n aor1776_map2w_bibra:0 "von Bibra"\n gov_aor1776_map2w_fulda:0 "'+gov+'"\n gov_aor1776_map2w_fulda_desc:0 "'+desc+'\\n\\n$TRANSFER_OF_POWER_NAME_DESC$"\n'
    migration=dict(replaced_regions=REGIONS,previous=previous,updated=updated,new_members=['FUL'],free_cities=[],new_provinces=g['new_provinces'],geometry='MAP2W/GEOMETRY.json',region_reference_changes=bindings,extent_added_cells=[],extent_removed_cells=[],country_additions={n.key:core.qa.signature(n) for n in core.cw.parse(defs)})
    files[core.active_registry_path().relative_to(ROOT).as_posix()]=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    files[(OUT/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(migration,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
        if rel in b['originals']:assert (ROOT/rel).read_text(encoding='utf-8-sig')==((ref['expected_text'].get(rel,b['originals'][rel])).lstrip('\ufeff') if ref else b['originals'][rel]),rel
    dump('EXPECTED_TEXT.json',files);core.OUT=OUT;changes=core.emit(files,'HISTORY.patch');dump('PLAN.json',dict(files=changes,registered_RGBs=len(ledger),region_reference_changes=bindings))
    print('Prepared',len(changes),'files; population',sum(r['after']['FUL'] for r in allocations),'registry',len(ledger),flush=True)

def install():
    b=load('BASELINE.json');ref=load('REFINEMENT_CAPTURE.json') if (OUT/'REFINEMENT_CAPTURE.json').exists() else None
    assert core.sha(ROOT/'map_data/provinces.png')==(ref['bitmap_sha256'] if ref else b['bitmap_sha256'])
    for p,raw in load('EXPECTED_TEXT.json').items():assert (ROOT/p).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip(),p
    subprocess.run(['powershell','-NoProfile','-Command',"Copy-Item -LiteralPath '"+str(OUT/'provinces_candidate.png')+"' -Destination '"+str(ROOT/'map_data/provinces.png')+"' -ErrorAction Stop"],check=True)
    print('Installed reviewed bitmap; earlier captures retained.',flush=True)

def imperial():
    old=prior.t.OUT;prior.t.OUT=OUT
    try:prior.t.imperial()
    finally:prior.t.OUT=old

def journal():
    import render_map2k_imperial_map as render
    render.OUT=OUT;render.render()

def repair_terrain():
    files=load('EXPECTED_TEXT.json');g=load('GEOMETRY.json');rel='map_data/province_terrains.txt';raw=files[rel]
    assert (ROOT/rel).read_text(encoding='utf-8-sig')==raw,'Concurrent terrain edit'
    for a in g['new_provinces']:raw=re.sub(r'(?im)^'+a['rgb']+r'\s*=\s*"[^"\n]+"[ \t]*\n?','',raw)
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw.rstrip()+'\n'+''.join(a['rgb']+'="'+terrain[a['parent_rgb'].upper()]+'"\n' for a in g['new_provinces'])
    dump('EXPECTED_TEXT.json',files);core.OUT=OUT;core.emit({rel:files[rel]},'TERRAIN_REPAIR.patch')

def validate():
    from map2l_registry import expected_country_definitions,approved_lot_dirs,apply_territorial_migrations,approved_territorial_extensions
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
        check('Exact connected RGB '+a['rgb'],int(np.sum(after==int(a['rgb'][1:],16)))==a['pixels'] and len(core.components(after==int(a['rgb'][1:],16)))==1)
    check('Exact full bitmap delta',np.array_equal(expected,after));check('Exact world ownership delta',counter(inv['owners'])==eo)
    check('Only 39 owner transfers',sum(a['pixels'] for a in g['assignments'] if a['owner']!=a['previous_owner'])==39)
    check('Erfurt rectangle frozen',np.array_equal(before[822:837,4342:4359],after[822:837,4342:4359]))
    for key in ['units','buildings','building_levels_written','duplicates','errors','resolved_demographics','pops']:
        check('Global invariant '+key,inv[key]==b['inventory'][key])
    types=dict(b['inventory']['state_types']);types.update({sid+'|FUL':'incorporated_default' for sid in REGIONS});check('Only two new regional subdivisions',inv['state_types']==types)
    check('Only FUL country added',inv['countries']==expected_country_definitions(b['inventory']['countries'],[m]))
    ep=counter(b['inventory']['regional_pop'])
    for row in load('POPULATION_ALLOCATION.json')['profiles']:
        ep[row['state'],row['donor'],row['culture'],row['religion']]-=row['before']
        for tag,amount in row['after'].items():ep[row['state'],tag,row['culture'],row['religion']]+=amount
        check('Integer population conservation '+row['culture']+' '+row['religion'],sum(row['after'].values())==row['before'] and all(isinstance(n,int) and n>=0 for n in row['after'].values()))
    check('Exact regional populations',counter(inv['regional_pop'])==ep)
    world=sum(r['count'] for r in inv['pops']);oldworld=sum(r['count'] for r in b['inventory']['pops']);check('Measured world unchanged',oldworld==world==835801255)
    ful=sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='FUL');check('FUL 20047 technical inhabitants',ful==20047)
    check('Fulda diagnostic point belongs to FUL',owners['x'+format(int(after[843,4322]),'06X')]==['STATE_SAXONY','FUL'])
    check('Actual prior Gotha enclave untouched',owners['xEDB40F']==['STATE_SAXONY','GOT'] and np.array_equal(before==int('EDB40F',16),after==int('EDB40F',16)))
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'));check('545 unique registry entries',len(ledger)==len({r['rgb'] for r in ledger})==545)
    for row in ledger:check('Imperial title '+row['rgb'],owners.get(row['rgb'])==[row['state'],row['beneficiary']])
    check('Imperial physical extent conserved',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in ledger])))
    initial=json.loads((ROOT/'docs/reports/map/MAP2L/BASELINE.json').read_text(encoding='utf8'))['de_jure_registry'];belgian=json.loads((ROOT/'docs/reports/map/MAP2L/BELGIUM/GEOMETRY.json').read_text(encoding='utf8'));regions={a['state'] for a in belgian['assignments']}
    frozen=[r for r in initial if r['state'] not in regions]+[dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for a in belgian['assignments']]+approved_territorial_extensions()
    check('Full chronological registry replay',apply_territorial_migrations(frozen)==ledger)
    for r in b['registry']:
        if r['rgb'] in g['parents']:continue
        check('Previous imperial RGB protected '+r['rgb'],owners.get(r['rgb'])==[r['state'],r['beneficiary']] and int(np.sum(before==int(r['rgb'][1:],16)))==int(np.sum(after==int(r['rgb'][1:],16))))
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tm={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    for a in g['new_provinces']:
        check('New terrain inherited once '+a['rgb'],len(re.findall(r'(?im)^\s*'+a['rgb']+r'\s*=',terrain))==1 and tm[a['rgb'].upper()]==tm[a['parent_rgb'].upper()])
        check('New RGB absent from original '+a['rgb'],not np.any(before==int(a['rgb'][1:],16)))
        check('New RGB state mapped '+a['rgb'],inv['geometry'].get(a['rgb'])==next(r['state'] for r in g['assignments'] if r['rgb']==a['rgb']))
    for rel,raw in load('EXPECTED_TEXT.json').items():
        check('Reviewed text '+rel,(ROOT/rel).read_text(encoding='utf-8-sig').rstrip()==raw.lstrip('\ufeff').rstrip())
        if rel.endswith('.txt'):
            try:core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'));check('Parse '+rel,True)
            except Exception as e:check('Parse '+rel,False,str(e))
        if rel in b['originals'] and '/history/' in rel:
            old=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(b['originals'][rel])) if n.key.startswith('s:STATE_') and n.key[2:] not in REGIONS];new=[core.qa.signature(n) for n in core.cw.walk(core.cw.parse(raw)) if n.key.startswith('s:STATE_') and n.key[2:] not in REGIONS];check('Other state histories '+rel,old==new)
        if rel.startswith('map_data/state_regions/'):
            old={n.key:n for n in core.cw.parse(b['originals'][rel])};new={n.key:n for n in core.cw.parse(raw)}
            for sid,node in old.items():
                exclude={'provinces','prime_land'} if sid in REGIONS else set()
                check('ID/resources/arable/traits/hubs '+sid,[core.qa.signature(n) for n in node.children() if n.key not in exclude]==[core.qa.signature(n) for n in new[sid].children() if n.key not in exclude])
    for rel,raw in load('IMPERIAL_EXPECTED.json').items():check('Compiled imperial '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    from map2k_patch import ELECTORS
    check('No new elector',len(ELECTORS)==9 and 'FUL' not in ELECTORS.values())
    check('No native imperial vassal added','create_diplomatic_pact' not in (ROOT/'common/history/countries/ful - map2w.txt').read_text(encoding='utf8'))
    from localization_duplicate_audit import entries
    for lang in ['french','english']:
        rel=f'localization/{lang}/1776_map2w_l_{lang}.yml';raw=(ROOT/rel).read_text(encoding='utf-8-sig');keys=re.findall(r'^\s*([A-Za-z0-9_.-]+):0\s+"',raw,re.M);found=entries(lang)
        check('BOM/header '+lang,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':'))
        for key in keys:check('Unique localization '+lang+' '+key,len(found.get(key,[]))==1)
        check('Six matching country/government/ruler keys '+lang,len(keys)==6)
    check('Native flag pattern exists',Path('C:/Games/Victoria 3/game/gfx/coat_of_arms/patterns/pattern_cross.dds').exists())
    check('Wood locator stays HEK',owners['x'+format(int(after[850,4313]),'06X')]==['STATE_HESSE','HEK'])
    current=q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));allowed=set(load('EXPECTED_TEXT.json'))|set(load('IMPERIAL_EXPECTED.json'))|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    outside=[p for p in changed if p not in allowed];check('No unreviewed runtime changes',not outside,outside)
    for folder in ['buildings','military_formations','diplomacy','subject_types','map_object_data']:
        check('All prior '+folder+' files byte-identical',all(current.get(p)==h for p,h in b['hashes'].items() if '/'+folder+'/' in p))
    for p,raw in b['tool_originals'].items():
        if p!='tools/map2l_registry.py':check('Imperial mechanics source frozen '+p,(ROOT/p).read_text(encoding='utf8')==raw)
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head']);check('Index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    result=dict(status='MAP2W_READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'MAP2W_BLOCKED',scope='MAP2W-R1 Fulda-Hünfeld-Neuhof core only; global inventory is not global completion',runtime_status='NOT_TESTED_MAP2W',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,world_before=oldworld,world_after=world,population_FUL=ful,runtime_files_modified=changed,preexisting_duplicate_RGBs=len(inv['duplicates']),preexisting_errors=inv['errors'])
    dump('VALIDATION.json',result);dump('INSTALLED_MANIFEST.json',dict(lot='MAP2W-R1',status=result['status'],functional_files={p:current[p] for p in changed},bitmap_sha256=core.sha(ROOT/'map_data/provinces.png')))
    print(result['status'],result['passed'],'/',len(checks),flush=True)
    if result['passed']!=len(checks):raise SystemExit(1)

def maps():
    from georeference.model import forward
    b=load('BASELINE.json');g=load('GEOMETRY.json');before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');old={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};new=dict(old)
    for a in g['assignments']:new[a['rgb']]=a['owner']
    palette={'FUL':'#986bb6','HEK':'#bd5766','HES':'#91b7ce','KMZ':'#d7ac79','MEI':'#8fae91','WZB':'#c48db2','COB':'#c1ac80','BAV':'#b7c0c8','NAS':'#adab79','FRM':'#e5cd68','WLD':'#b3c887','PRU':'#8e9aab'}
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
    box=(4304,830,4338,859);x0,y0,x1,y1=box;scale=19
    def panel(a,owners,title):
        local=a[y0:y1,x0:x1];rgb=np.zeros((*local.shape,3),dtype='uint8')
        for c in np.unique(local):rgb[local==c]=ImageColor.getrgb(palette.get(owners.get('x'+format(int(c),'06X')),'#d6d5ce'))
        im=Image.fromarray(rgb).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST);p=Image.new('RGB',(im.width,im.height+210),'#fcfaf5');p.paste(im,(0,42));d=ImageDraw.Draw(p);d.text((12,8),title,font=bold,fill='#243747')
        for a2 in g['assignments']:
            if a2['owner']!='FUL':continue
            for x,y in a2['cells']:d.rectangle(((x-x0)*scale,(y-y0)*scale+42,(x-x0+1)*scale-1,(y-y0+1)*scale+41),outline='white',width=2)
        model=json.loads((ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json').read_text(encoding='utf8'))['model']
        towns=[('Fulda',9.6808,50.5558,15,-28),('Neuhof',9.6175,50.4528,-90,20),('Hünfeld',9.7674,50.6725,10,-25),('Geisa (différé)',9.95,50.7156,-55,-38),('Schlitz (exclu)',9.5611,50.6744,-130,-10)]
        for n,lon,lat,dx,dy in towns:
            x,y=forward(model,[[lon,lat]])[0];x=(x-x0)*scale;y=(y-y0)*scale+42;d.ellipse((x-3,y-3,x+3,y+3),fill='black');d.line((x,y,x+dx,y+dy+8),fill='#555555');d.text((x+dx,y+dy),n,font=small,fill='#202b32',stroke_width=2,stroke_fill='white')
        for i,(tag,color) in enumerate(palette.items()):
            xx=12+(i%6)*105;yy=im.height+55+(i//6)*27;d.rectangle((xx,yy,xx+13,yy+13),fill=color);d.text((xx+18,yy-2),tag,font=small,fill='black')
        for i,line in enumerate(['39 cellules → FUL : HEK 16 + résidu MEI 23. Cadres blancs.','Points : projection diagnostique, position native non certifiée.','Noyaux antérieurs et WZB protégés. Contours B généralisés.','Le noyau installé ne représente pas tout le prince-évêché.']):d.text((12,im.height+115+i*21),line,font=small,fill='#343434')
        return p
    a=panel(before,old,'AVANT MAP-2W');z=panel(after,new,'APRÈS : noyau Fulda–Hünfeld–Neuhof');out=Image.new('RGB',(a.width+z.width+20,a.height),'#fcfaf5');out.paste(a,(0,0));out.paste(z,(a.width+20,0));out.save(OUT/'WEST_SOUTH_GERMANY_BEFORE_AFTER.png')
    guide=Image.new('RGB',(1100,800),'#fcfaf5');d=ImageDraw.Draw(guide);d.text((25,15),'Où vérifier MAP-2W-R1 dans Victoria 3',font=bold,fill='#243747')
    overview=(4250,795,4380,905);ox,oy,ex,ey=overview;local=after[oy:ey,ox:ex];arr=np.zeros((*local.shape,3),dtype='uint8')
    for c in np.unique(local):arr[local==c]=ImageColor.getrgb(palette.get(new.get('x'+format(int(c),'06X')),'#d6d5ce'))
    guide.paste(Image.fromarray(arr).resize((780,660),Image.Resampling.NEAREST),(20,60));d=ImageDraw.Draw(guide)
    for tag,x,y in [('Fulda FUL',4321,845),('Francfort FRM',4300,856),('Würzburg WZB',4322,862),('Nuremberg NUR',4352,877),('Hesse-Cassel HEK',4316,827)]:
        px=20+(x-ox)*6;py=60+(y-oy)*6;d.ellipse((px-4,py-4,px+4,py+4),fill='black');d.text((px+8,py-10),tag,font=font,fill='#182c38',stroke_width=2,stroke_fill='white')
    d.rectangle((20+(4319-ox)*6,60+(840-oy)*6,20+(4326-ox)*6,60+(848-oy)*6),outline='#63238a',width=3)
    notes=['Nouvelle partie au 1er janvier 1776.','Chercher le pays FUL, au nord-est','des possessions de Mayence.','Deux régions : Hesse et Saxe.','Capitale technique : STATE_SAXONY.','Aucun locator urbain ajouté.','','Vérifier gouvernement et souverain,','population et accès au marché,','subsistance et statut impérial.','','Laisser passer au moins un mois.','Aucun test moteur automatisé.']
    for i,line in enumerate(notes):d.text((820,80+i*35),line,font=small,fill='#293d49')
    d.text((25,750),'Schéma des souverainetés installées. Le cadre indique seulement le nouveau noyau de 39 cellules.',font=font,fill='#293d49');guide.save(OUT/'PLAYER_LOCATION_GUIDE.png')
    print('Both requested maps generated',flush=True)

def tables():
    tables=load('CSV_TABLES.json');v=load('VALIDATION.json');g=load('GEOMETRY.json');p=load('POPULATION_ALLOCATION.json')
    for row in tables['INVENTORY_1776.csv']['rows']:
        if row['Nom_FR']=='Principauté épiscopale de Fulda':row.update(TAG_actuel='FUL',Regions_actuelles='STATE_HESSE;STATE_SAXONY',Representation='MAP2W_R1_NOYAU_INSTALLE_39_CELLULES',Classe='B',Lots_installation='MAP2W-R1',Source_historique='https://lagis.hessen.de/resolve/de/ga/40; https://www.hs-fulda.de/hlsb/en/forschen-publizieren/citizen-science/fulda-faces-fulda-places/heinrich-von-bibra',Limite='Fulda–Hünfeld–Neuhof seulement; Geisa/Herbstein et franges non installés; population technique')
    for row in tables['DISCREPANCIES.csv']['rows']:
        if row['Entite']=='Principauté épiscopale de Fulda':row.update(TAG='FUL',Etat='CORRIGE_PARTIELLEMENT_MAP2W_R1',Probleme='Noyau restauré; reste du territoire différé',Action='TESTER_NOYAU_ET_CONSERVER_RESERVES',Source='MAP2W/GEOMETRY.json')
    for row in tables['UNRESOLVED.csv']['rows']:
        if row['Entite']=='Principauté épiscopale de Fulda':row.update(Probleme='Une cellule WZB de la trace exclue. Geisa, Dermbach et Herbstein non restitués; franges et démographie non certifiées.',Suite='Sous-lot ultérieur ciblé, sans réattribuer les noyaux saxons protégés',Source='MAP2W/GEOMETRY.json; SOURCE_ALIGNMENT.json')
    changes=[]
    for a in g['assignments']:
        changes.append(dict(Territoire='Fulda–Hünfeld–Neuhof' if a['owner']=='FUL' else 'Résidu technique conservé',Avant=a['previous_owner'],Apres=a['owner'],State_ID=a['state'],ID_numerique=74 if a['state']=='STATE_HESSE' else 73,RGB_avant=a['parent_rgb'],RGB_apres=a['rgb'],Cellules=a['pixels'],Population_deplacee=sum(r['after']['FUL'] for r in p['profiles'] if r['state']==a['state']) if a['owner']=='FUL' else 0,Classe=a['confidence'],Source='Uhlhorn 1962 Hessen 1789; LAGIS Fulda; GEOMETRY.json',Approximation='Noyau intérieur, anciens noyaux et WZB exclus; pas tout le Hochstift'))
    populations=[]
    for row in p['profiles']:
        for tag,n in row['after'].items():populations.append(dict(State_ID=row['state'],TAG=tag,Culture=row['culture'],Religion=row['religion'],Avant=row['before'] if tag==row['donor'] else 0,Apres=n,Delta=n-(row['before'] if tag==row['donor'] else 0),Methode=p['method']))
    populations.append(dict(State_ID='MONDE',TAG=None,Culture='Toutes',Religion='Toutes',Avant=v['world_before'],Apres=v['world_after'],Delta=0,Methode='Total mesuré, pas cible historique imposée'))
    for name,rows in [('TERRITORIAL_CHANGES.csv',changes),('POPULATION_VALIDATION.csv',populations)]:tables[name]=dict(fields=list(rows[0]),rows=rows)
    dump('CSV_TABLES.json',tables)

def unit_tests():
    import unittest,io,time
    groups={'MAP2W_targeted':['test_map2w_west_south'],'cumulative_contracts':['test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01'],'earlier_stage_snapshots':['test_map2t_saxony','test_map2u_thuringia']};results={}
    for name,modules in groups.items():
        suite=unittest.TestLoader().loadTestsFromNames(modules);stream=io.StringIO();start=time.monotonic();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);results[name]=dict(modules=modules,tests=r.testsRun,failures=[test.id() for test,_ in r.failures],errors=[test.id() for test,_ in r.errors],seconds=round(time.monotonic()-start,2),output=stream.getvalue());print(name,r.testsRun,'tests',len(r.failures),'failures',len(r.errors),'errors',flush=True)
    dump('UNIT_TESTS.json',results)
    if any(results[name]['failures'] or results[name]['errors'] for name in ['MAP2W_targeted','cumulative_contracts']):raise SystemExit(1)

def reports():
    v=load('VALIDATION.json');g=load('GEOMETRY.json');tables=load('CSV_TABLES.json');tests=load('UNIT_TESTS.json');b=load('BASELINE.json')
    counts=C.Counter(r['Representation'] for r in tables['INVENTORY_1776.csv']['rows'])
    dump('COVERAGE_SUMMARY.json',dict(entries=len(tables['INVENTORY_1776.csv']['rows']),representation_counts=dict(counts),not_exhaustive_cadastre=True,already_installed_not_rebuilt=['MAP2L/FRANCONIA','MAP2L/FRANCONIA_CONTINUATION','MAP2L/RHINE_CENTRAL','MAP2L/MAINZ_PALATINATE','MAP2L/MAINZ_ESTATES','MAP2L/MAINZ_COMPLETION','MAP2L/RHINE_WESTPHALIA','MAP2L/MINDEN_RAVENSBERG','MAP2L/DUCHY_WESTPHALIA','MAP2L/RHINE_WESTPHALIA_COMPLETION','MAP2L/SWABIA','MAP2L/SWABIA_CONTINUATION','MAP2L/SWABIA_FINISH','MAP2L/SWABIA_COMPLETION'],stale_inventory_warning='MAP2Q/R3 inventory predates MAP2T and MAP2U; older UNRESOLVED entries can have been resolved by later migrations.'))
    changes='\n'.join('| '+a['parent_rgb']+' | '+a['state']+' | '+a['previous_owner']+' → '+a['owner']+' | '+a['rgb']+' | '+str(a['pixels'])+' |' for a in g['assignments'])
    testlines='\n'.join('- '+name+': '+str(r['tests'])+' tests, '+str(len(r['failures']))+' échecs, '+str(len(r['errors']))+' erreurs.' for name,r in tests.items())
    files='\n'.join('- `'+p+'`' for p in v['runtime_files_modified'])
    text=f'''# MAP-2W — Inventaire et premier sous-lot Fulda

17 octobre 2026. Date historique : 1er janvier 1776.

**{v['status']}**. Ce statut concerne exclusivement le noyau MAP2W-R1. Les 94 entrées de l’inventaire ne signifient pas que toute l’Allemagne occidentale et méridionale est achevée. Aucun test moteur MAP2W n’a été exécuté.

## Le risque de refaire les mêmes zones était réel

Le prompt recoupe des territoires déjà travaillés. La lecture chronologique des migrations et des derniers rapports évite de traiter les anciennes listes d’incertitudes comme l’état actuel :

| Secteur | Travail existant conservé | Ce que cela ne certifie pas |
| --- | --- | --- |
| Franconie | FRANCONIA puis FRANCONIA_CONTINUATION : Ansbach/Bayreuth, Bamberg, Würzburg, Nuremberg, fragments Eichstätt/Cobourg | Hohenlohe, Castell, Wertheim, villes secondaires et résidus bavarois |
| Rhin central/Mayence/Palatinat | RHINE_CENTRAL, MAINZ_PALATINATE, MAINZ_ESTATES, MAINZ_COMPLETION | Toutes les juridictions de Hesse ou toutes les possessions de Mayence |
| Rhin–Westphalie | Münster, Paderborn, Juliers–Berg sous souverain palatin, Minden/Ravensberg, Westphalie et Vest de Cologne, Osnabrück, Niederstift, Lingen/Tecklenburg | Gueldre prussienne, limites fines Clèves/Mark, petits comtés/abbayes, toutes les branches de Nassau |
| Souabe | SWABIA, CONTINUATION, FINISH, COMPLETION : Fürstenberg, Ellwangen, Salem, Weingarten, Waldburg, Constance/Markdorf, Augsbourg et Kempten distincts, villes libres | Montbéliard, Oettingen, dépendances et condominiums, toutes les franges ecclésiastiques |
| Saxe/Thuringe | MAP2T puis MAP2U : nouveaux noyaux, Reuss, Sondershausen | Les résidus laissés C ne deviennent pas des possessions saxonnes historiquement certifiées |

Liège et la Belgique restent protégés ; leur absence éventuelle d’une migration tardive ne signifie pas absence de travail. Eutin, Anhalt, Poméranie et possessions suédoises, Emden, les papeteries et Erfurt–Eichsfeld ne sont pas modifiés.

L’inventaire compare les pays effectifs à des juridictions identifiées et aux dossiers conservés. Il contient également des groupes (Solms, Isembourg, Hohenlohe, Oettingen...) dont les branches restent à inventorier. Les lignes sans souverain vérifié ou sans carte précise restent C. Un lien de catalogue dans ces lignes est une piste, pas une preuve de frontière. Une participation d’un TAG à un lot ne valide pas tous ses territoires.

## Correction réellement installée

**Un nouveau pays : FUL, prince-évêché de Fulda, Heinrich VIII von Bibra.** Noyau intérieur de Fulda–Hünfeld–Neuhof : **39 cellules transférées**, quatre nouveaux RGB. Les limites sont une généralisation B tirée de la carte institutionnelle de Hesse 1789, sous réserve de continuité du noyau sous le même souverain depuis 1759 ; pas un cadastre de 1776.

| Parent RGB | Région économique | Propriétaire avant/après | RGB après | Cellules |
| --- | --- | --- | --- | ---: |
{changes}

Le parent xD0C021 était un résidu MEI inchangé, classé non certifié lors de MAP2T. La cellule historique GOT xEDB40F, ainsi que tous les autres nouveaux noyaux T/U, restent intacts. Le découpage de Fulda traverse deux régions économiques natives : Hesse/74 et Saxe/73. Cela n’attribue pas toute la Saxe à Fulda et ne rouvre pas la reconstruction thuringienne. Capitale technique : STATE_SAXONY ; aucun locator déplacé.

Les RGB parents comptaient 345 cellules : toutes sont conservées. 39 changent de souveraineté et 46 changent de couleur ; sept cellules HEK résiduelles sont seulement séparées en composantes RGB connexes. Une cellule de Würzburg touchée par le polygone est exclue. Geisa, Dermbach, Herbstein et les franges restent ouverts.

La nouvelle appartenance impériale, le registre de jure et la carte du journal sont intégrés par le compilateur existant. Les neuf électeurs et les règles des sujets ne changent pas. FUL n’est pas créé comme sujet natif de l’empereur. Le drapeau à croix noire est provisoire. Lois/technologies : modèle du prince-évêché de Würzburg, abstraction technique documentée.

## Population et économie

Population FUL : **20 047**, dont 14 240 prélevés à HEK/Hesse et 5 807 à MEI/Saxe. Redistribution technique provisoire, **pas** recensement historique. Les profils culturels et religieux restent identiques à l’échelle mondiale ; leurs éventuels défauts historiques ne sont pas corrigés par invention.

Population mondiale : **{v['world_before']:,} → {v['world_after']:,}**, delta zéro. Bâtiments, PM, propriétaires économiques, unités, recrutements et infrastructures existants sont conservés, sans industrie artificielle. Les données de départ ne permettent pas d’assigner historiquement des installations du reste de la Hesse/Saxe à ce petit noyau ; aucun bâtiment n’est déplacé arbitrairement. La subsistance et la viabilité de FUL restent à vérifier en jeu.

## Vérifications

Contrôles statiques actuels : **{v['passed']}/{v['total']}**. Détail dans VALIDATION.json. Sont vérifiés : bitmap et propriétaires exacts, connexité, références RGB/régions, ressources/capacités inchangées, démographie entière par profil, bâtiments/unités, capitales, localisations FR/EN, références de personnage/gouvernement/drapeau, relecture cumulative du registre et compilation impériale.

{testlines}

Les anciennes suites MAP2T/U restent exécutées comme photographies d’étape : leurs attentes « monde exact après mon seul lot » et « seulement mes nouveaux pays » ne peuvent inclure FUL ni les lots ultérieurs. Les échecs ne sont ni effacés ni convertis en PASS ; UNIT_TESTS.json conserve les noms et sorties. Les éventuelles divergences économiques/militaires par rapport à ces anciennes baselines sont contrôlées séparément contre la baseline immédiate MAP2W, où elles sont déjà présentes. Aucune attente historique n’est réécrite.

Sur les 39 anciens tests, 30 passent et neuf échouent : sept attentes globales d’étape obsolètes et deux comparaisons économiques/militaires déjà divergentes avant MAP2W. EARLIER_TEST_DIAGNOSTICS.json documente chaque cas. Les 17 tests ciblés et les 60 contrats cumulatifs actuels passent tous. REFERENCE_VALIDATION.json confirme séparément les technologies, lois, culture, religion, groupe d’intérêts et idéologie utilisés par FUL.

Anomalies héritées : **44 doublons RGB et 12 sélecteurs invalides**, identiques à la capture initiale. Aucun accroissement n’est autorisé. Ce PASS local ne signifie donc pas que le mod entier est exempt d’erreurs.

MAP2T, MAP2U et les papeteries : attestation manuelle de l’utilisateur enregistrée séparément dans PREVIOUS_LOTS_RUNTIME_USER_ATTESTATION.json. Elle n’est ni un test automatisé ni une certification historique, et ne valide pas MAP2W.

HEAD conservé : `{b['git_head']}`. Empreinte de l’index identique. Aucun staging, commit, push, merge, reset, changement de branche ou modification de l’installation du jeu. La modification nord-américaine des formations militaires déjà présente au départ reste byte-identique et n’est pas un changement MAP2W.

## Suite proposée, sans la commencer automatiquement

1. MAP2W-R2 : Hesses/Nassau, différences de branches et compléments de Fulda après validation du noyau.
2. MAP2W-R3 : Hohenlohe, Castell, Wertheim et villes franconiennes encore absentes ; préserver les noyaux déjà validés.
3. MAP2W-R4 : Freising, Passau, Ratisbonne et principales juridictions bavaroises ; Bavière et Palatinat ont encore des souverains distincts au 1er janvier 1776.
4. Compléments souabes ciblés seulement avec preuves nouvelles : ne pas recommencer les quatre passes déjà installées.

## Fichiers fonctionnels modifiés/ajoutés

{files}

Outillage et preuves : tools/map2w_west_south.py, tools/map2w_tables.mjs, tools/test_map2w_west_south.py, garde étroite dans tools/map2l_registry.py, ce dossier de rapport et l’image source de la carte du journal dans workshop_pack/source. La liste fonctionnelle est comparée à la capture immédiate et n’inclut pas à tort tous les fichiers sales de Git.

## ColGrep

Deux tentatives d’appel de `C:/Users/simeo/.cargo/bin/colgrep.exe --agent` : première bloquée par le verrou d’index hors workspace, seconde relancée avec accès à l’index existant. Une actualisation incrémentale et une session agent (réflexion et commandes de localisation) ont été observées. La sortie finale ne fournit pas de localisation exploitable et vérifiée utilisée pour cette livraison. Recherche documentaire finale par fichiers déjà connus et identifiants exacts. Pas de reconstruction complète d’index ni de changement de modèle. Temps et tokens exacts non récupérés, aucune économie de quota chiffrée revendiquée.
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf8')
    (OUT/'RUNTIME_TEST_PLAN.md').write_text('''# Test manuel MAP2W-R1

Nouvelle partie au 1er janvier 1776, pas une ancienne sauvegarde.

1. Retrouver FUL au nord-est de Mayence, autour de Fulda–Hünfeld–Neuhof ; consulter PLAYER_LOCATION_GUIDE.png et le comparatif. Vérifier ses deux portions économiques Hesse et Saxe, sans attribuer les régions entières au nouveau pays.
2. Vérifier Heinrich VIII von Bibra, prince-évêque catholique ; nom et description du gouvernement en français et anglais si disponibles. La succession canonique et le drapeau complet restent des abstractions.
3. Contrôler environ 20 047 habitants techniques au départ, absence de population dupliquée, accès au marché, subsistance, emploi et bâtiments. Aucun bâtiment nouveau n’est attendu ; signaler une éventuelle absence de viabilité sans la masquer par des constructions artificielles.
4. Vérifier l’appartenance impériale et la carte du journal, sans nouveau droit électoral ni sujétion native automatique. Les États antérieurs doivent rester distincts, notamment Gotha xEDB40F.
5. Comparer les frontières protégées de Mayence/Würzburg et celles des lots saxons ; Erfurt n’a pas été corrigé. Ne pas considérer les seules couleurs du jeu comme preuve historique.
6. Laisser passer au moins un mois et vérifier absence de crash, d’erreurs nouvelles de scripts, de disparition d’un pays ou de rupture des mécanismes impériaux.

À l’issue seulement, l’utilisateur peut attester PASS_RUNTIME_USER_VALIDATED pour les éléments inspectés. Le statut actuel reste NOT_TESTED_MAP2W.
''',encoding='utf8')
    dump('DELIVERY_CHECK.json',dict(status=v['status'],static_checks=dict(passed=v['passed'],total=v['total']),tests={name:{k:r[k] for k in ['tests','failures','errors']} for name,r in tests.items()},git_head_unchanged=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'],git_index_unchanged=core.sha(ROOT/'.git/index')==b['git_index_sha256'],runtime_user_validation=False,entities=94,new_countries=1,cells_transferred=39,new_RGBs=4,world_population_delta=v['world_after']-v['world_before']))
    print('Report, test plan and delivery record written',flush=True)

def final_checks():
    import csv
    b=load('BASELINE.json');v=load('VALIDATION.json');inv=load('CURRENT_INVENTORY.json');tests=load('UNIT_TESTS.json');legacy=[]
    for name in tests['earlier_stage_snapshots']['failures']:
        economy='economic_and_military' in name
        reference=prior.t.load('BASELINE.json')['inventory'] if name.startswith('test_map2t') else prior.load('BASELINE.json')['inventory']
        evidence={k:dict(already_different_at_MAP2W_start=b['inventory'][k]!=reference[k],preserved_by_MAP2W=inv[k]==b['inventory'][k]) for k in ['buildings','building_levels_written','units']} if economy else dict(reason='Earlier single-stage global bitmap/country delta excludes explicitly documented later lots, including FUL')
        legacy.append(dict(test=name,classification='PREEXISTING_SNAPSHOT_ECONOMIC_MILITARY_DIVERGENCE' if economy else 'OBSOLETE_SINGLE_STAGE_GLOBAL_EXPECTATION',evidence=evidence))
    dump('EARLIER_TEST_DIAGNOSTICS.json',dict(failed=9,obsolete_global_expectations=7,preexisting_economic_military_expectations=2,records=legacy,old_test_sources_modified=False))
    tables=load('CSV_TABLES.json');check=[]
    for name,data in tables.items():
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        assert len(rows)==len(data['rows']) and list(rows[0])==data['fields'],name
        assert all(row[k]==('' if original.get(k) is None else str(original[k])) for row,original in zip(rows,data['rows']) for k in data['fields']),name
        check.append(dict(file=name,rows=len(rows),sha256=core.sha(OUT/name)))
    pop=tables['POPULATION_VALIDATION.csv']['rows'];assert sum(r['Delta'] for r in pop)==0
    changes=tables['TERRITORIAL_CHANGES.csv']['rows'];assert sum(r['Cellules'] for r in changes if r['Avant']!=r['Apres'])==39
    assert sum(r['Population_deplacee'] for r in changes)==20047
    refs=load('REFERENCE_VALIDATION.json');assert refs['passed']
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==b['git_head'];assert core.sha(ROOT/'.git/index')==b['git_index_sha256']
    current=q.economy.runtime_hashes();assert all(current.get(p)==h for p,h in load('INSTALLED_MANIFEST.json')['functional_files'].items()),'Post-validation runtime drift'
    assert all(current.get(p)==h for p,h in b['hashes'].items() if p not in v['runtime_files_modified']),'Unreviewed post-validation drift'
    for p in ['REPORT.md','RUNTIME_TEST_PLAN.md','WEST_SOUTH_GERMANY_BEFORE_AFTER.png','PLAYER_LOCATION_GUIDE.png','PREVIOUS_LOTS_RUNTIME_USER_ATTESTATION.json']:assert (OUT/p).is_file(),p
    dump('FINAL_DELIVERY_INTEGRITY.json',dict(status='PASS',csvs=check,typed_tables=load('CSV_VALIDATION.json')['status'],all_five_previews_and_two_maps_visually_reviewed=True,reference_validation='PASS',legacy_classification='7 obsolete global-stage expectations; 2 preexisting economic/military baseline discrepancies',functional_hashes_preserved=True,HEAD=head,index_sha256=core.sha(ROOT/'.git/index'),runtime_test='NOT_EXECUTED'))
    print('Final integrity PASS; 5 CSV round-trips, 2 maps, runtime hashes and Git untouched.',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
