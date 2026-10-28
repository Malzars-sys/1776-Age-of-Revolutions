"""Traceable closeout for the installed territorial lot; WORLD tracking only."""
import argparse
import csv
import io
import json
from collections import Counter,defaultdict
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_sahel0205 as m

ROOT,LOT=m.ROOT,m.LOT
WORLD=LOT.parent

def doc(name,text):m.save_text(LOT/name,text)
def jload(path):return json.loads(path.read_text('utf8'))
def dump_path(path,data):m.save_text(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def review_external():
    """Verify another lot's current receipts; never modify its installation."""
    assert not (LOT/'EXTERNAL_COMPOSITION_REVIEW.json').exists(), 'External update already reviewed.'
    source=ROOT/'docs/reports/map/NORTH_AMERICA_1776/NORTHWEST-01'
    patch=jload(source/'PATCH.json');baseline=m.load('APPLY_BEFORE.json')
    own={r['file']:r['after'] for r in m.load('FILES_MODIFIED.json')}
    records=[]
    for rel,after in patch['output_sha256'].items():
        old=patch['input_sha256'][rel]
        assert m.s.b.a.sha(ROOT/rel)==after and m.s.b.a.sha(source/'patch'/rel)==after, rel
        if old is not None:
            assert m.s.b.a.sha(source/'before'/rel)==old, rel
            if rel in baseline['protected'] or rel in own:
                assert old==(own.get(rel) or baseline['protected'][rel]), rel
        records.append(dict(file=rel,before=old,current=after,current_matches_external_patch=True,attributed_to_this_task=False))
    before_text=m.raw(source/'before'/m.ST);after_text=m.raw(source/'patch'/m.ST)
    a={n.key:before_text[n.start:n.end] for n in m.s.b.walk(m.s.b.parse(before_text)) if n.key.startswith('s:STATE_')}
    b={n.key:after_text[n.start:n.end] for n in m.s.b.walk(m.s.b.parse(after_text)) if n.key.startswith('s:STATE_')}
    changed=[k for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)]
    assert not set(changed)&set(baseline['scope'][m.ST])
    assert all(k in {'s:STATE_ALASKA','s:STATE_ARIZONA','s:STATE_BAJA_CALIFORNIA','s:STATE_BRITISH_COLUMBIA','s:STATE_CALIFORNIA','s:STATE_CHIHUAHUA','s:STATE_DURANGO','s:STATE_NEVADA','s:STATE_NEW_MEXICO','s:STATE_OREGON','s:STATE_RIO_GRANDE','s:STATE_SINALOA','s:STATE_SONORA','s:STATE_TEXAS','s:STATE_UNALASKA_TRADING_POST','s:STATE_WASHINGTON'} for k in changed)
    # Actual pixel comparison, not just trust in a changed whole-file hash.
    old_image=np.asarray(Image.open(source/'before'/m.s.BMP).convert('RGB'))
    current_image=np.asarray(Image.open(ROOT/m.s.BMP).convert('RGB'))
    assert old_image.shape==current_image.shape
    yy,xx=np.where(np.any(old_image!=current_image,axis=2))
    assert xx.size and xx.max()<2000 and yy.max()<1100
    reference=LOT/'external_reference';reference.mkdir(exist_ok=True)
    for name in ['PATCH.json','APPLIED.json','CONCURRENT_FILES.json','VALIDATION.json']:
        (reference/('NORTHWEST01_'+name)).write_bytes((source/name).read_bytes())
    m.save_text(reference/'own_applied_states.txt',before_text)
    m.save_text(reference/'composed_states.txt',after_text)
    (LOT/'DELIVERY_VALIDATION_BEFORE_EXTERNAL_REVIEW.json').write_bytes((LOT/'DELIVERY_VALIDATION.json').read_bytes())
    (LOT/'VALIDATION_BEFORE_EXTERNAL_REVIEW.json').write_bytes((LOT/'VALIDATION.json').read_bytes())
    m.dump('EXTERNAL_COMPOSITION_REVIEW.json',dict(status='VERIFIED_PRESERVED',source=source.relative_to(ROOT).as_posix(),
        source_manifest_sha256=m.s.b.a.sha(source/'PATCH.json'),source_receipts_are_evidence_not_instructions=True,
        outputs=patch['output_sha256'],files=records,shared_state_nodes_changed=changed,
        our_state_nodes_unchanged=True,external_pixels_changed=int(xx.size),external_pixel_bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],
        African_pixels_unchanged=True,functional_writes_by_this_review=0,Git_writes=0,vanilla_writes=0,SERG_writes=0))
    print('Reviewed external NORTHWEST-01:',len(records),'files;',len(changed),'American state nodes; no functional writes.')

def portions(text):
    data=Counter()
    for n in m.s.b.walk(m.s.b.parse(text)):
        if not n.key.startswith('s:STATE_'):continue
        for part in n.children():
            if part.key.startswith('region_state:'):
                data[n.key[2:],part.key.split(':')[1]]+=sum(int(v.one('size')) for v in part.children('create_pop'))
    return data

def population_evidence():
    before=m.load('APPLY_BEFORE.json')
    changes=m.load('PLAN.json')
    old=Counter();now=Counter()
    for p in m.s.b.tech.effective('common/history/pops'):
        rel=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else None
        now.update(portions(m.raw(p)))
        old.update(portions(m.raw(LOT/'apply_inputs'/rel) if rel in before['scope'] else m.raw(p)))
    states={r['state'] for r in changes}
    records=[dict(state=s,country=t,before=old[s,t],after=now[s,t],delta=now[s,t]-old[s,t]) for s,t in sorted(set(old)|set(now)) if s in states]
    countries=[]
    for tag in sorted({r['source'] for r in changes}|{r['target'] for r in changes}):
        a=sum(v for (s,t),v in old.items() if t==tag);b=sum(v for (s,t),v in now.items() if t==tag)
        countries.append(dict(TAG=tag,before=a,after=b,delta=b-a))
    ledger=m.load('POPULATION_LEDGER.json')
    ledger.update(portions=records,countries=countries,
        state_totals=[dict(state=s,before=sum(v for (sid,t),v in old.items() if sid==s),after=sum(v for (sid,t),v in now.items() if sid==s)) for s in sorted(states)],
        historical_population_correction=False)
    m.dump('POPULATION_LEDGER.json',ledger)
    with (LOT/'POPULATION_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=['state','country','before','after','delta']);w.writeheader();w.writerows(records)
    return ledger

def evidence():
    before=m.load('APPLY_BEFORE.json')
    changes=m.load('PLAN.json')
    population_evidence()
    image=np.asarray(Image.open(ROOT/m.s.BMP).convert('RGB'))
    pack=image[:,:,0].astype('uint32')*65536+image[:,:,1].astype('uint32')*256+image[:,:,2]
    rows=[]
    for r in changes:
        for c in r['RGBs']:
            yy,xx=np.where(pack==int(c[1:],16))
            rows.append(dict(state=r['state'],RGB=c,before=r['source'],after=r['target'],pixels=int(xx.size),
                bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],
                pixel_centroid=[round(float(xx.mean()),2),round(float(yy.mean()),2)],
                source_basis=r['historical_basis'],precision=r['precision']))
    m.dump('GEOGRAPHIC_CROSSWALK.json',dict(historical_date='1776-01-01',new_RGBs=0,pixels_recolored=0,
        note='Pixel coordinates locate unchanged native provinces; they are not reconstructed cadastral limits.',cells=rows))
    render_maps(pack,before['inventory']['owners'],m.s.b4.inventory()['owners'])
    new=m.load('STARTING_TECH_NEW_COUNTRIES.json');existing=m.load('STARTING_TECH_EXISTING_AFTER.json')
    prior={r['TAG']:r for r in m.load('STARTING_TECH_BEFORE.json')}
    review=[]
    for row in existing:
        # Historical-profile certification is deliberately left open, and is
        # distinct from the technical gate comparison captured before transfer.
        oldset={json.dumps(f,sort_keys=True) for f in prior[row['TAG']]['findings'] if f['priority'] in ['P0','P1']}
        newset={json.dumps(f,sort_keys=True) for f in row['findings'] if f['priority'] in ['P0','P1']}
        review.append(dict(TAG=row['TAG'],inherited_remaining=[json.loads(f) for f in sorted(oldset&newset)],
            resolved=[json.loads(f) for f in sorted(oldset-newset)],introduced=[json.loads(f) for f in sorted(newset-oldset)],
            historical_profile_certification='NOT_RECERTIFIED_BY_THIS_TERRITORIAL_LOT'))
    assert all(not r['introduced'] for r in review)
    assert all(r['status']=='PASS_STATIC_ONLY' for r in new)
    m.dump('TECH_NON_REGRESSION.json',dict(new_profiles=len(new),all_new_profiles_pass=True,existing_country_comparison=review,
        shared_graph_changes=0,shared_recipe_changes=0,human_validation=False))

def render_maps(pack,before,after):
    cat=m.s.b.a.catalog('common/country_definitions')
    colors={}
    for tag,(node,p) in cat.items():
        try:colors[tag]=tuple(int(v) for v in m.s.ids(node,'color'))
        except ValueError:continue
    try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    except OSError:font=ImageFont.load_default()
    for name,states in [('SENEGAMBIA',['STATE_SENEGAL']),('MALI',['STATE_EASTERN_MALI','STATE_TIMBUKTU','STATE_WESTERN_MALI']),('HAUSA',['STATE_HAUSALAND','STATE_OUTER_HAUSALAND','STATE_EAST_HAUSALAND','STATE_NIGERIA','STATE_NORTH_CAMEROON'])]:
        chosen={c for c,v in after.items() if any(s in states for s,t in v)}
        yy,xx=np.where(np.isin(pack,[int(c[1:],16) for c in chosen]))
        box=[max(0,int(xx.min())-5),max(0,int(yy.min())-5),min(pack.shape[1],int(xx.max())+6),min(pack.shape[0],int(yy.max())+6)]
        crop=pack[box[1]:box[3],box[0]:box[2]]
        scale=max(2,min(6,900//crop.shape[1]))
        width,height=crop.shape[1]*scale,crop.shape[0]*scale
        out=Image.new('RGB',(width*2+50,height+140),'#19232d');draw=ImageDraw.Draw(out)
        for j,owners in enumerate([before,after]):
            rgb=np.zeros((*crop.shape,3),dtype=np.uint8)+38
            visible=defaultdict(list)
            for value in np.unique(crop):
                c='x'+f'{int(value):06X}';parts=owners.get(c,[])
                if not parts:continue
                tag=parts[-1][1]
                if c not in chosen:continue
                rgb[crop==value]=colors.get(tag,(110,110,110));visible[tag].append(int(value))
            # Ownership boundaries, not every native province border.
            border=np.any(rgb[1:,:,:]!=rgb[:-1,:,:],axis=2)
            rgb[1:,:,:][border]=(20,25,30)
            border=np.any(rgb[:,1:,:]!=rgb[:,:-1,:],axis=2)
            rgb[:,1:,:][border]=(20,25,30)
            panel=Image.fromarray(rgb).resize((width,height),Image.Resampling.NEAREST)
            left=15+j*(width+20);out.paste(panel,(left,45))
            draw.text((left,12),name+' — '+('AVANT' if j==0 else 'APRÈS'),fill='white',font=font)
            used=[]
            for tag,values in sorted(visible.items(),key=lambda item:-np.isin(crop,item[1]).sum()):
                ys,xs=np.where(np.isin(crop,values));cx,cy=xs.mean(),ys.mean()
                idx=np.argmin((xs-cx)**2+(ys-cy)**2);x=left+int(xs[idx])*scale;y=45+int(ys[idx])*scale
                # Compact tag labels, shifted only to avoid overlapping text.
                for unused in range(12):
                    if all(abs(x-ox)>40 or abs(y-oy)>20 for ox,oy in used):break
                    y+=19
                used.append((x,y));draw.text((x-17,y-9),tag,fill='white',font=font,stroke_width=2,stroke_fill='#182029')
        draw.text((15,height+65),'1er janvier 1776 | Enveloppes politiques par provinces natives, limites approximatives.',fill='white',font=font)
        draw.text((15,height+93),'Tchad / Bornou conservés. Aucun pixel ni hub redessiné. Légende des TAG dans REPORT.md.',fill='#cbd2d8',font=font)
        out.save(LOT/(name+'_BEFORE_AFTER.png'))

def reports():
    v=m.load('VALIDATION.json');ledger=m.load('POPULATION_LEDGER.json')
    composition=''
    if m.external_review():
        composition='''\nUne installation concurrente NORTHWEST-01 est arrivée après le premier contrôle de livraison. Ses 23 sorties courantes correspondent exactement à son manifeste, ses entrées aux versions que nous avions préservées ; 16 nœuds américains sont modifiés, sans changement d'un de nos huit nœuds africains. Les pixels retouchés sont exclusivement au nord-ouest de l'Amérique. Aucune restauration ni écriture fonctionnelle lors de la réconciliation : [EXTERNAL_COMPOSITION_REVIEW.json](EXTERNAL_COMPOSITION_REVIEW.json). Les 460 contrôles antérieurs du noyau sont complétés par les comparaisons de composition courante. Une ancienne assertion exigeait un ensemble de doubles propriétaires strictement identique ; elle est corrigée pour interdire toute nouvelle double attribution tout en permettant les résolutions externes prouvées par la comparaison exacte des propriétaires. Le premier résultat de composition est conservé dans VALIDATION_EXTERNAL_FIRST_RUN.json.\n'''
    countries='\n'.join('| '+r['TAG']+' | '+format(r['before'],',').replace(',',' ')+' | '+format(r['after'],',').replace(',',' ')+' |' for r in ledger['countries'])
    profiles='\n'.join('| '+tag+' | '+d['fr']+' | '+d.get('kind','unrecognized')+' | '+str(len(d['tech']))+' |' for tag,d in m.planmod.COUNTRIES.items())
    doc('REPORT.md',f'''# SAHEL-02-05 — Sénégambie, Mali et royaumes haoussa

27 octobre 2026. Référence : **1er janvier 1776**. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Frontières et souverainetés ; Tchad et Nil différés sur la dernière consigne du joueur. Aucun test joueur acquis pour ce lot.

## Corrections installées

- Sénégambie : deux provinces du Baol (BAO) détachées du Jolof ; district côtier/Ndiambour rendu au Cayor ; Sine (SRR) séparé du Saloum (SLU). Cayor, Jolof, Boundou, Sine et Kaabu sont représentés comme royaumes non reconnus, plutôt que territoires décentralisés. Les noyaux Waalo/Fouta, Saint-Louis britannique et Gorée française de SAHEL-01 restent identiques.
- Mali : Ségou retrouve son noyau, dont le hub natif x2A6A2D, et sa capitale régionale passe à EASTERN_MALI. Le Macina des Ardo conserve son noyau et son autonomie sous tribut à Ségou ; il n'est pas assimilé à la Diina de 1818. Les communautés sénoufo (SNU) restent décentralisées au sud, sans inventer le royaume ultérieur de Sikasso. Tombouctou (TMB), Gao (GAO réactivé) et les approches sous influence Kel Tademekkat (TDM) remplacent l'extension prématurée du Macina dans TIMBUKTU. Kaarta reste distinct et inchangé.
- Haoussa : l'extension initiale de Sokoto, postérieure à 1776, est répartie entre Gobir (HAU), Kebbi (KEB), Zamfara (ZAM), Katsina (KTS), Daura (DAU), Kano (KNN), Zazzau (ZAZ) et Nupe (NUP), avec des communautés voisines décentralisées ZRM/GWR/BCH/BTA. Aucun émirat futur de Bauchi ou d'Adamawa préinstallé. La définition dormante de SOK est conservée pour les contenus ultérieurs. Bornou (BOR), Borgu (BRG), Bamum et les frontières tchadiennes ne changent pas.

**225 RGB existants réattribués, 26 groupes de transfert, aucun nouveau RGB ni pixel recoloré.** Huit régions natives touchées. Aucun terrain, ressource, trait régional, hub ou locator modifié. Le détail exhaustif cellule/propriétaire/coordonnées/raison est dans [PLAN.json](PLAN.json) et [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json). Il s'agit d'enveloppes politiques sur le maillage existant, pas de frontières cadastrales certifiées.

## Institutions et compatibilité initiale

16 TAG nouveaux et GAO réactivé. Aucun nouveau personnage. Les monarchies sont initialisées avec les lois traditionnelles et une oligarchie de notables, approximation du pouvoir royal et des lignages ; les cinq agrégats communautaires restent décentralisés. Une variante commerciale privée, aux mêmes coefficients que le mercantilisme courant, est limitée à ces royaumes et débloquée par international_relations. Elle évite d'accorder artificiellement l'assurance maritime. Les profils antérieurs gardent leurs autres lois et connaissances ; leurs restrictions héritées restent signalées.

Le Macina reçoit seulement religion animiste de sa définition pré-Diina, relation tributaire et suppression des quatre modèles natifs de personnages du XIXe siècle. Hamadou-Amina III déjà présent est conservé ; aucun remplacement de dirigeant ajouté. Une référence de recrutement d'un unique conscrit MSN passe de Tombouctou à EASTERN_MALI, sans changer type, service ou effectif.

Les nouveaux profils comportent 5 à 9 connaissances locales explicites : agriculture, élevage, ateliers, alimentation, textile et diplomatie selon le pays ; capacité militaire traditionnelle lorsque les installations héritées l'exigent. Tombouctou conserve ses établissements de sel et de commerce avec shaft_mining et organized_financial_institutions, capacités de premier âge sans parent dans le graphe courant. Gobir reçoit seulement organized_military_establishments pour ses casernes héritées. Aucun paquet technologique par niveau, aucune modification de graphe TECH-R1/R2/R3 ou de recette ECON-ALLOYS/quincaillerie.

| TAG | Pays / agrégat | Type moteur | Technologies |
|---|---|---|---:|
{profiles}

Profils et justifications : [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json). Les 17 profils nouveaux/réactivés passent le contrat statique avec prérequis fermés. Sur les huit pays existants, aucune nouvelle incompatibilité P0/P1 ; les demandes héritées d'esclavage pour dettes et de mercantilisme sans leurs gates restent ouvertes, sans leur attribuer des connaissances constitutionnelles ou d'assurance pour masquer la dette technique. La certification historique exhaustive de leurs anciens profils n'est pas prétendue.

## Populations et bâtiments

Monde avant/après : **{ledger['world_before']:,} → {ledger['world_after']:,}**, variation **0**. Toutes les cohortes, religions/cultures explicites et statuts d'esclavage sont conservés. Allocation par nombre de provinces transférées au sein de chaque portion source : règle technique de conservation, **pas estimation de densité ni recensement historique**. Les zéros nationaux du tableau signalent un TAG auparavant inactif dans le scénario, pas un territoire historiquement inhabité. Aucun changement démographique historique revendiqué.

| TAG | Habitants avant | Habitants après |
|---|---:|---:|
{countries}

Ventilation par État dans [POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv). Tous les niveaux et toutes les recettes/PM préexistants sont conservés. Le rattachement politique des établissements suit les portions nouvelles ; les installations existantes du noyau Macina restent au Macina, les établissements de sel/textile/commerce de Tombouctou suivent TMB. Aucun bâtiment supplémentaire ni raffinement de production. Ressources et hubs restent régionaux et partagés selon le moteur ; leur allocation exacte et les budgets demandent l'observation en jeu.

## Sources et limites

[SOURCES.md](SOURCES.md) distingue les cartes réellement vues, les passages consultés et leurs dates. Les cartes comparatives c.1780/c.1800 guident les voisinages sans transformer leurs contours en cadastre de 1776. Les villes haoussa, le Niger et les noyaux royaux servent d'ancrages ; aucun partage par distance à une capitale ou frontière rectangulaire générée.

Cartes de contrôle : [Sénégambie avant/après](SENEGAMBIA_BEFORE_AFTER.png), [Mali avant/après](MALI_BEFORE_AFTER.png), [Haoussa avant/après](HAUSA_BEFORE_AFTER.png). Les couleurs des provinces servent à localiser le résultat installé, pas à prouver une source historique.

La Gambie (deux provinces SIL), les limites fines Galam/Khasso, l'estuaire Sine/Saloum et les franges exactes des royaumes restent ouverts. Les interfaces touarègues sont mobiles et disputées : TDM est une approximation politique, aucune exclusivité foncière ni suzeraineté uniforme imposée à Gao/Tombouctou. Cultures sérère, nupe, gbagyi et certains peuples de la Bénoué absentes du catalogue : identifiants régionaux natifs utilisés comme proxies ; aucune précision ethnographique ou conversion des POPs inventée. Les agrégats décentralisés ne représentent pas un État unifié.

## Vérifications et concurrence

{v['passed']}/{v['total']} contrôles statiques territoriaux/conservation réussis ; premier passage 361/361 archivé, puis détection supplémentaire d'un champ Sine mal décalé et de branches conditionnelles non pertinentes. Réparation bornée et traçable dans [COMPATIBILITY_REPAIR.json](COMPATIBILITY_REPAIR.json), sans effacer le résultat initial. Les 17 contrats des nouveaux profils passent ; les dettes anciennes sont séparées dans [TECH_NON_REGRESSION.json](TECH_NON_REGRESSION.json).

Versions courantes conservées hors nœuds attribués, y compris Amérique du Nord, SERG, Maghreb/Gibraltar, Siwa et Fezzan à 78 provinces, Balkans, fortifications/génie et TECH/ECON. Empreintes et comparaison hors portée dans [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json). 13 fichiers fonctionnels existants modifiés, 24 ajouts ; aucun Git d'écriture, aucun vanilla ni suivi SERG écrit.
{composition}

Commandes effectivement exécutées : installation avec `world1776_sahel0205.py --apply --validate`, réparation avec `--repair-compatibility --validate`, contrats collect_snapshot/audit_country, puis contrôles de livraison. Les outils réutilisés ne lancent pas le moteur. Les anciennes assertions d'ownership MSN/SOK ne sont pas présentées comme tests actuels de ces frontières.

Tests en jeu **NOT_RUN** ; [GROUPED_RUNTIME_ITEMS.md](GROUPED_RUNTIME_ITEMS.md) prépare le contrôle groupé, sans demande intermédiaire. WORLD reste **10/320, 3,13 %** ; aucun point pour une région partiellement couverte et aucune attestation humaine créée.

Prochaine action : contrôle cartographique groupé de ce lot et des limites signalées ; Tchad puis Nil restent pour une passe ultérieure. Pas de flavor entrepris.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# Contrôle groupé Sahel — version SAHEL-01 + SAHEL-02-05

NOT_RUN. Aucun reçu humain. Ne pas demander ce protocole après chaque sous-lot.

À la fin du groupe autorisé, ouvrir une nouvelle partie au 1er janvier 1776. Comparer les trois cartes avant/après et la liste des TAG du rapport : Baol/Sine/Saloum ; Ségou/Macina/Kaarta/Gao/Tombouctou ; royaumes haoussa séparés. Vérifier les noyaux SAHEL-01, Bornou et Borgu témoins. Aucun Sokoto initial ni territoire centralisé accidentellement isolé dans les agrégats décentralisés.

Observer les capitales et hubs générés, drapeaux, lois effectives, suzeraineté SGU→MSN, absence des personnages natifs du XIXe siècle supprimés. Contrôler quelques profils techniques, mines/commerce TMB et casernes Gobir ; ne pas confondre restriction de construction et arrêt de production. Les lois conditionnelles restantes des anciens profils sont un passif documenté, pas une panne observée.

Vérifier population et emploi des nouvelles portions, leurs ressources partagées, accès au marché et budget. Les transferts statiques ne prouvent ni rentabilité ni allocation moteur exacte. Jouer un mois, sauvegarder/recharger, consigner seulement les observations réellement faites. Témoins : détroit Ceuta/Gibraltar, Siwa, Fezzan, Balkans, territoires SERG et Amérique du Nord. Version/empreintes livrées : FILES_DELIVERED.json et DELIVERY_MANIFEST.json.

Tchad, Darfour et Nil non testés au titre de cette passe et non modifiés. Aucune réussite n'étend la validation à ces régions ou à tout WORLD.
''')
    doc('USER_REQUEST.txt','ok on y vas pour le royaume de senegambiiens, malie haoussa puis plus tard tchad et nil\n')
    doc('REPRODUCE.md','''# Reproduire les vérifications

Depuis le workspace courant, Python du runtime local :

`python tools/world1776_sahel0205.py --validate`

`python tools/world1776_sahel0205_closeout.py --evidence --reports --final`

Les commandes de validation n'appliquent aucune frontière. L'installation et la réparation sont gardées contre le rejeu. Captures apply_inputs et repair_inputs, reçus originaux FILES_MODIFIED et COMPATIBILITY_REPAIR restent immuables. Les réexécutions actualisent les preuves du seul dossier SAHEL-02-05 ; un futur changement territorial légitime doit faire l'objet d'une réconciliation explicite, pas d'un retour à ces frontières.

Contrats techniques : `validate_starting_technology_1776.collect_snapshot()` puis `audit_country` pour chaque profil de COUNTRY_PROFILES.json. Aucun lancement de jeu et aucune opération Git d'écriture.
''')

def tracking():
    path=WORLD/'ROADMAP_STATE.json';data=jload(path)
    assert not any(x['id']=='SAHEL-02-05' for x in data['lots']), 'Tracking already appended.'
    names=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']
    for name in names:
        target=LOT/'tracking_inputs'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((WORLD/name).read_bytes())
    hashes={name:m.s.b.a.sha(WORLD/name) for name in names}
    evidence='SAHEL-02-05/REPORT.md'
    for phase in data['phases']:
        if phase['id']=='P3':
            for r in phase['subregions']:
                if r['id'] not in ['P3-01','P3-02','P3-04']:continue
                for key,c in r['criteria'].items():
                    if key=='V':c.update(status='NOT_STARTED',evidence='SAHEL-02-05/GROUPED_RUNTIME_ITEMS.md');continue
                    if c['status']=='STATIC_VERIFIED':continue
                    c.update(status='PARTIAL',evidence=evidence,remaining='Noyaux installés seulement ; limites régionales, profils historiques complets et test groupé ouverts. Aucun crédit régional entier.')
        n=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values())
        phase['progress'].update(technical_verified=n,technical_percent=float((Decimal(n)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
    score=sum(p['progress']['technical_verified'] for p in data['phases'])
    assert score==10 and data['progress']['criteria_total']==320 and data['progress']['runtime_user_validated']==0
    data['progress'].update(technical_verified=score,technical_percent=3.13)
    data['lots'].append(dict(id='SAHEL-02-05',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope=['Remaining Senegambian royal cores','Segou / Macina / Timbuktu and Gao','Pre-Sokoto Hausa polities and adjacent decentralised communities'],excluded=['Chad/Bornu territorial work','Nile','Flavour and economic refinement'],runtime='NOT_RUN',files_modified=37,existing_files_modified=13,new_files=24,new_tags=16,activated_existing_tags=['GAO'],native_RGBs_transferred=225,new_RGBs=0,pixels_recolored=0,world_population_delta=0,receipt='SAHEL-02-05/FILES_DELIVERED.json',credited_criteria=[]))
    data['steering_history'].append(data['current_steering'])
    data['current_steering']=dict(date='2026-10-27',scope='Senegambian kingdoms, Mali, Hausa; Chad and Nile later',authority='SAHEL-02-05/USER_REQUEST.txt',last_lot='SAHEL-02-05',next_pass='Grouped territorial review of delivered cores; Chad and Nile deferred',intermediate_player_tests_requested=False,runtime_validation_timing='GROUPED_SAHEL',full_V_credit=False)
    assert all(m.s.b.a.sha(WORLD/n)==h for n,h in hashes.items()), 'Concurrent WORLD documentation update; reread.'
    dump_path(path,data)
    entry='''\n\n## SAHEL-02-05 — 27 octobre 2026\n\nSénégambie/Mali/Haoussa installés sur consigne directe ; Tchad et Nil différés. Baol/Saloum séparés, Ségou restauré, Macina pré-Diina distingué, Gao/Tombouctou et Kel Tademekkat représentés, Sokoto initial remplacé par royaumes haoussa et communautés décentralisées. 225 RGB natifs réattribués, aucun pixel ni hub redessiné. 16 nouveaux TAG, GAO réactivé ; 13 fichiers existants ciblés, 24 ajouts, aucun personnage ajouté. Populations et cohortes conservées, monde 837 328 539, delta 0. 460/460 contrôles statiques et 17 profils nouveaux PASS_STATIC_ONLY ; lois héritées non corrigées hors périmètre. Sources, approximations politiques et limites Gambie/estuaire/franges documentées dans SAHEL-02-05/REPORT.md. Aucun test moteur ou humain, aucun crédit régional supplémentaire : WORLD 10/320 (3,13 %).\n'''
    for name in ['ROADMAP.md','PROGRESS_HISTORY.md']:m.save_text(WORLD/name,m.raw(WORLD/name).rstrip()+entry)
    m.save_text(WORLD/'BLOCKERS.md',m.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## SAHEL-02-05 — 27 octobre 2026\n\nNoyaux territoriaux installés, pas clôture régionale. Gambie SIL et limites fines Galam/Khasso, Sine/Saloum, franges des royaumes et zones touarègues restent approximatives. Proxies culturels pour les identifiants absents ; pas de recensement historique reconstruit. Bâtiments/POPs redistribués à total constant ; hubs, ressources par portion, lois effectives et budgets non validés en moteur. Les dettes de lois des profils existants restent héritées, aucune nouvelle incompatibilité P0/P1. Contrôle joueur groupé, aucune demande intermédiaire. Tchad/Darfour/Nil différés par la dernière consigne ; ne pas lancer une autre région ou du flavor pour combler les limites du fond.\n''')
    m.save_text(WORLD/'OWNERSHIP_BOUNDARIES.md',m.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## SAHEL-02-05 — 27 octobre 2026\n\nSeuls huit nœuds régionaux Senegal/Eastern Mali/Timbuktu/Hausaland/Outer Hausaland/East Hausaland/Nigeria/North Cameroon des états, POPs et bâtiments listés dans FILES_DELIVERED.json ; c:MSN militaire (une référence de recrutement), c:CAY/JLF/BND/SRR/KBU politique et c:HAU (unique grant de capacité militaire traditionnelle). Définitions SGU/MSN et cinq autres royaumes dans une surcharge propre, 16 nouveaux TAG et GAO réactivé. Aucune frontière BOR/BRG/BMM, aucun pixel/terrain/hub/ressource, recette commune, graphe TECH ou suivi SERG écrit. Les versions courantes Fezzan/Siwa/Gibraltar, Balkans et Amérique du Nord sont protégées ; pas de reprise d'ancienne baseline. Ensemble de RGB exact : SAHEL-02-05/PLAN.json.\n''')
    m.save_text(WORLD/'NEXT_ACTION.md','''# Prochaine action — après SAHEL-02-05\n\nDernière consigne : royaumes sénégambiens, Mali et Haoussa maintenant ; **Tchad et Nil plus tard**. SAHEL-02-05 est installé et contrôlé statiquement. Lire son REPORT.md, PLAN.json, VALIDATION.json, TECH_NON_REGRESSION.json et FILES_DELIVERED.json. SAHEL-01 reste acquis dans son périmètre, sans nouvelle validation joueur.\n\nPréparer la vérification cartographique groupée du lot livré. Limites encore documentées : Gambie SIL, détails Galam/Khasso/estuaire Sine-Saloum et franges politiques, juridictions touarègues mouvantes. Ne pas prolonger ces incertitudes en inventant des frontières ni en ajoutant personnages, bâtiments ou flavor. Bornou, Tchad/Darfour et Nil ne sont pas lancés par cette livraison.\n\nTests joueur regroupés, aucun test intermédiaire demandé. Population mondiale conservée ; TECH/ECON, SERG, Balkans, Maghreb/Gibraltar, Siwa, contour Fezzan à 78 provinces et versions américaines concurrentes à préserver sur fichiers courants. Protocole SAHEL-02-05/GROUPED_RUNTIME_ITEMS.md, statut NOT_RUN. WORLD 10/320 (3,13 %), aucun nouveau crédit régional ou humain.\n''')
    concurrent=jload(WORLD/'CONCURRENT_CHANGES.json');concurrent['SAHEL-02-05']=dict(receipt='SAHEL-02-05/CONCURRENT_CHANGES.json',repair='SAHEL-02-05/COMPATIBILITY_REPAIR.json',existing_functional_files_modified=13,new_files=24,native_RGBs_transferred=225,new_RGBs=0,pixels_recolored=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False)
    dump_path(WORLD/'CONCURRENT_CHANGES.json',concurrent)
    m.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=m.s.b.a.sha(WORLD/n)) for n in names])

def final():
    checks=[]
    def ck(name,result,detail=None):checks.append(dict(check=name,passed=bool(result),detail=detail))
    original=m.load('FILES_MODIFIED.json');repair=m.load('COMPATIBILITY_REPAIR.json')
    delivered={r['file']:dict(r) for r in original}
    for r in repair['files']:
        if r['file'] in delivered:delivered[r['file']]['after']=r['after']
        else:delivered[r['file']]=r
    review=m.external_review()
    if review:
        delivered[m.ST].update(own_only_after=delivered[m.ST]['after'],after=review['outputs'][m.ST],composition_evidence='EXTERNAL_COMPOSITION_REVIEW.json')
        for rel,h in review['outputs'].items():ck('reviewed_external_version_preserved.'+rel,m.s.b.a.sha(ROOT/rel)==h)
    for rel,r in delivered.items():ck('delivered_functional_hash.'+rel,m.s.b.a.sha(ROOT/rel)==r['after'])
    ck('37_functional_files',len(delivered)==37)
    m.dump('FILES_DELIVERED.json',list(delivered.values()))
    validation=m.load('VALIDATION.json');ck('territorial_static_pass',validation['status']=='PASS')
    new=m.load('STARTING_TECH_NEW_COUNTRIES.json')
    for r in new:ck('new_initial_knowledge_contract.'+r['TAG'],r['status']=='PASS_STATIC_ONLY' and not r['findings'])
    for row in m.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:ck('no_new_P0_P1.'+row['TAG'],not row['introduced'])
    ledger=m.load('POPULATION_LEDGER.json');ck('world_conserved',ledger['delta']==0)
    for r in ledger['state_totals']:ck('regional_population_conserved.'+r['state'],r['before']==r['after'])
    ck('all_new_countries_nonempty',all(any(p['country']==t and p['after']>0 for p in ledger['portions']) for t in m.planmod.COUNTRIES))
    # Protected scope still compared against the actual own-apply snapshot.
    b=m.load('APPLY_BEFORE.json');outside=[]
    for rel,h in b['protected'].items():
        if rel in delivered:continue
        current=m.s.b.a.sha(ROOT/rel) if (ROOT/rel).exists() else None
        if current!=h and not m.reviewed_external(rel,current):outside.append(rel)
    ck('outside_scope_current_preservation_with_verified_external_composition',not outside,outside)
    state=jload(WORLD/'ROADMAP_STATE.json')
    credited=[r['id']+'/'+k for p in state['phases'] for r in p['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED']
    human=[r['id']+'/'+k for p in state['phases'] for r in p['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
    ck('canonical_progress_calculation',len(credited)==10 and not human and state['progress']['technical_verified']==10 and state['progress']['criteria_total']==320)
    m.dump('PROGRESS_CALCULATION.json',dict(credited=credited,user_validated=human,numerator=len(credited),denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
    required=['REPORT.md','SOURCES.md','GEOGRAPHIC_CROSSWALK.json','POPULATION_BEFORE_AFTER.csv','GROUPED_RUNTIME_ITEMS.md','COUNTRY_PROFILES.json','TECH_NON_REGRESSION.json','SENEGAMBIA_BEFORE_AFTER.png','MALI_BEFORE_AFTER.png','HAUSA_BEFORE_AFTER.png']
    for name in required:ck('evidence_exists.'+name,(LOT/name).is_file())
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False)
    m.dump('DELIVERY_VALIDATION.json',result)
    paths=[ROOT/r for r in delivered]+[LOT/n for n in required]+[LOT/n for n in ['VALIDATION.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','FILES_DELIVERED.json','COMPATIBILITY_REPAIR.json','DELIVERY_VALIDATION.json','PROGRESS_CALCULATION.json']]+[ROOT/'tools'/n for n in ['world1776_sahel0205.py','world1776_sahel0205_plan.py','world1776_sahel0205_closeout.py']]
    if review:paths+=[LOT/'EXTERNAL_COMPOSITION_REVIEW.json',LOT/'external_reference/own_applied_states.txt',LOT/'external_reference/composed_states.txt']
    paths+=[WORLD/n for n in ['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']]
    paths+=[LOT/n for n in ['TRACKING_PATCHES.json','TRACKING_COMPOSITION_PATCHES.json'] if (LOT/n).exists()]
    m.dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():m.s.b.a.sha(p) for p in paths})
    print('Delivery:',result['status'],result['passed'],'/',result['total']);print('FAIL:',[r for r in checks if not r['passed']])
    return result['status']=='PASS'

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for key in ['evidence','reports','tracking','final','review-external','population']:a.add_argument('--'+key,action='store_true')
    args=a.parse_args()
    if args.review_external:review_external()
    if args.population:population_evidence()
    if args.evidence:evidence()
    if args.reports:reports()
    if args.tracking:tracking()
    if args.final:raise SystemExit(0 if final() else 1)
