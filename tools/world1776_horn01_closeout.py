"""Evidence, additive WORLD tracking and delivery checks; no engine launch."""
import argparse,csv,json
from collections import Counter
from decimal import Decimal,ROUND_HALF_UP
import world1776_horn01 as h
import world1776_sahel0205_closeout as old
import localization_duplicate_audit as loc
ROOT,LOT=h.ROOT,h.LOT
WORLD=LOT.parent
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def doc(name,text):h.save(LOT/name,text)
def read(path):return json.loads(path.read_text('utf8'))
def write(path,data):h.save(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def delivered():
    rows={r['file']:dict(r) for r in h.load('FILES_MODIFIED.json')}
    for name in ['FORMATTING_REPAIR.json','POP_ALLOCATION_REPAIR.json','PLURAL_LABELS_REPAIR.json']:
        for r in h.load(name)['files']:rows[r['file']]['after']=r['after']
    return rows

def evidence():
    before=h.load('APPLY_BEFORE.json');plan=h.load('PLAN.json');a=Counter();z=Counter()
    for path in h.b.tech.effective('common/history/pops'):
        rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
        z.update(old.portions(h.raw(path)))
        a.update(old.portions(h.raw(LOT/'apply_inputs'/rel) if rel in before['scope'] else h.raw(path)))
    states={r['state'] for r in plan};tags={r['source'] for r in plan}|{r['target'] for r in plan}
    rows=[dict(state=s,country=t,before=a[s,t],after=z[s,t],delta=z[s,t]-a[s,t]) for s,t in sorted(set(a)|set(z)) if s in states]
    ledger=dict(world_before=sum(a.values()),world_after=sum(z.values()),delta=sum(z.values())-sum(a.values()),portions=rows,countries=[dict(TAG=t,before=sum(v for (s,c),v in a.items() if c==t),after=sum(v for (s,c),v in z.items() if c==t)) for t in sorted(tags)],state_totals=[dict(state=s,before=sum(v for (c,t),v in a.items() if c==s),after=sum(v for (c,t),v in z.items() if c==s)) for s in sorted(states)],historical_population_correction=False,method='Conservative splitting of each inherited cohort by enumerated unique native provinces in each source portion, integer remainder allocation. Not historical density/census; cultures, religions and slave attributes unchanged.')
    h.dump('POPULATION_LEDGER.json',ledger)
    with (LOT/'POPULATION_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=['state','country','before','after','delta']);w.writeheader();w.writerows(rows)
    cells={r['RGB']:r for r in h.load('GEOMETRY_CELLS.json')};cross=[]
    for r in plan:
        for c in r['RGBs']:
            cell=cells[c];cross.append(dict(RGB=c,state=r['state'],before=r['source'],after=r['target'],pixels=cell['pixels'],bbox=cell['bbox'],centroid=cell['centroid'],historical_basis=r['historical_basis'],precision=r['precision']))
    h.dump('GEOGRAPHIC_CROSSWALK.json',dict(cells=cross,new_RGBs=0,pixels_recolored=0,duplicate_removed='x2D75F4',historical_date='1776-01-01',coordinates_are_navigation_not_cadastre=True))
    h.geometry(h.raw(LOT/'apply_inputs'/h.ST));(LOT/'BEFORE.png').write_bytes((LOT/'PROPOSED.png').read_bytes())
    h.geometry(h.raw(ROOT/h.ST));(LOT/'AFTER.png').write_bytes((LOT/'PROPOSED.png').read_bytes())

def reports():
    v=h.load('VALIDATION.json');pop=h.load('POPULATION_LEDGER.json');files=delivered()
    countries='\n'.join('| '+t+' | '+r['kind']+' | '+str(len(r['tech']))+' | '+r['capital'].replace('STATE_','')+' |' for t,r in h.p.COUNTRIES.items())
    pops='\n'.join('| '+r['TAG']+' | '+format(r['before'],',').replace(',',' ')+' | '+format(r['after'],',').replace(',',' ')+' |' for r in pop['countries'])
    doc('REPORT.md',f'''# HORN-01 — Empire éthiopien et Corne de l'Afrique

27 octobre 2026. Date cible : **1er janvier 1776**. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Passe cartographique autorisée après [SAHEL-GEOCHECK-01](../SAHEL-GEOCHECK-01/REPORT.md). Le joueur reporte la finition des courbes et autorise les vassalités/autonomies nécessaires. Aucun nouveau test moteur de cette version, aucune attestation humaine inventée.

## Résultat territorial

- ETH conserve la cour impériale et son noyau de Gondar/Begemder autour du lac Tana. TGR (Tigré), GJM (Godjam) et WLO (Wollo/Lasta agrégé) deviennent des pouvoirs provinciaux autonomes **tributaires** de la couronne. Ce lien moteur représente l'appartenance impériale nominale, pas une administration uniforme ou un tribut exactement quantifié dans une archive. L'hégémonie Yejju de 1786 n'est pas préinstallée.
- SHW retrouve le noyau Choa/Ankober-Menz-Yifat, sans les conquêtes du XIXe siècle. HAR (Harar/Charcar), AWS (Awsa et basse vallée de l'Awash), KFA (Kaffa), WLT (Wolayta) et YJR (Yem/Janjero) sont distincts et indépendants. Les îlots de domination impériale prématurée au sud sont supprimés. Aucun souverain exact de janvier reconstitué pour du flavor.
- Le noyau haut-plateau d'Asmara/Hamasien-Seraye rejoint TGR. Les ports ottomans dont Massawa restent TUR ; les communautés de l'Ouest/Bedja (BJA) et afar côtières et désertiques (AFR) sont distinguées. AFR est **un agrégat de pouvoirs locaux**, dont une portion septentrionale séparée, pas un grand royaume afar unique annexé à Awsa. Ni Djibouti français ni Érythrée coloniale créés.
- Les communautés de Wallaga/Gibe (WLG), Oromo de l'Est (ARS), Borana/Guji (BRN), Hadiya/Kambata (HDY), Omo (OMO) et communautés somalies (OGD) restent autonomes sous agrégats décentralisés. Ces étiquettes ne signifient ni absence d'institutions ni population ethniquement homogène. Pas de royaumes de Jimma, Leqa-Naqamte ou Limmu-Enarya du XIXe siècle préinstallés.
- HRI représente l'enveloppe confédérale hiraab et Mogadishu, distincte du noyau riverain Geledi GLD conservé à l'intérieur. L'extension prématurée du MJT dans le centre côtier/Hobyo est retirée ; noyaux nord-est MJT, Warsangali WSG et Isaaq ISQ préservés. La double occurrence MJT de x2D75F4 est supprimée. Aucun sultanat ultérieur de Hobyo créé, aucune annexion omanaise directe déduite de relations commerciales.

**280 provinces natives réattribuées, 27 groupes de transfert ; un doublon interne résolu. Aucun nouveau RGB, aucun pixel, terrain, ressource ou hub modifié.** Énumération et motifs : [PLAN.json](PLAN.json), [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json). Les indices de la carte d'inspection sont des repères, les RGB sont canoniques. Cartes : [avant](BEFORE.png), [après](AFTER.png). Courbes et angles non lissés, conformément au report demandé.

## Initialisation minimale et compatibilité

3 nouveaux TAG (AFR/HRI/YJR), 15 TAG natifs activés. Les capitales régionales sont adaptées aux portions réellement possédées, notamment TGR/GJM/WLO vers GONDER. Monarchie/oligarchie est une approximation des cours et notables ; trois liens tributaires seulement. Aucune monarchie future attribuée aux communautés Gadaa. Les anciennes définitions culturelles/religieuses sont conservées sauf changements explicites de type et religions de certains agrégats ; elles restent des proxies de catalogue, **pas un audit ethnographique certifié**. Harari, Yem ou certaines langues omotiques n'ont pas d'identifiant propre : cette limite n'autorise pas à convertir les cohortes POP.

| TAG | Type moteur | Technologies minimales | Capitale régionale |
|---|---|---:|---|
{countries}

Les connaissances sont des profils minimaux explicitement justifiés dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json), 4 à 7 par pays : agriculture, élevage, ateliers/alimentation, textile, échanges et organisation militaire traditionnelle selon la société. Ce n'est pas une certification exhaustive de tout le savoir local. Pas de paquet technologique par âge. Une variante privée de coutumes commerciales reprend les coefficients du mercantilisme et sa gate locale d'échanges ; aucune assurance maritime ou autre technologie ajoutée pour masquer un défaut de loi.

Les 18 contrats statiques passent sans constat. Sur neuf pays existants, aucun nouveau P0/P1 ; dettes techniques héritées conservées : [STARTING_TECH_NEW_COUNTRIES.json](STARTING_TECH_NEW_COUNTRIES.json), [TECH_NON_REGRESSION.json](TECH_NON_REGRESSION.json). Aucun graphe TECH-R1/R2/R3, recette ECON-ALLOYS/quincaillerie ou PM commun retouché.

Sept fichiers de personnages natifs 1836 sont neutralisés par surcharge homonyme pour les TAG réactivés ; **aucun nouveau personnage**. L'empereur et le général ETH déjà présents sont conservés. Les références des 4 dragons, 12 irréguliers et 23 conscrits ETH recrutés dans AMHARA passent à GONDER, seule correction nécessaire à la perte de cette portion ; les 25 conscrits GONDER antérieurs restent identiques. Types, comptes, services et formations conservés. Les administrations impériales existantes d'AMHARA sont replacées à la cour de GONDER, à niveaux et PM strictement constants ; autres installations et recettes conservées dans leurs nouvelles portions. Aucun raffinement de bâtiments ou nouvelle troupe.

## Population

**{pop['world_before']:,} → {pop['world_after']:,}, delta 0.** Chacune des cinq régions conserve son total ; chaque cohorte conserve ses attributs culturels, religieux et serviles. Partage technique par provinces uniques de chaque portion source, avec restes entiers : **pas un recensement ni une estimation de densité historique**. Le poids du doublon MJT est exclu. Les zéros initiaux désignent des TAG inactifs, pas des terres historiquement vides.

| TAG | Avant | Après |
|---|---:|---:|
{pops}

[POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv) et [POPULATION_LEDGER.json](POPULATION_LEDGER.json). Ressources/hubs partagés, choix implicites de PM, emplois, budgets et rendu des capitales/flags ne sont pas prouvés par ces totaux.

## Sources, portée et incertitudes

[SOURCES.md](SOURCES.md) distingue sources lues, cartes vues et références seulement consultées en extrait. La carte Bahru c.1800 fournit les voisinages et localités ; elle n'est pas un contour de 1776 à recopier. Les cartes Haberland c.1500/c.1700 ne prouvent pas une possession de 1776. Aucun partage automatisé par distance à une capitale, aucune frontière rectangulaire générée.

Les pouvoirs provinciaux de l'ère des Princes, limites Semien/Tigré/Wollo, confins bas-pays de Wallaga, emprises de Kaffa/Yem/Wolayta, contacts oromo-somalis et ressorts afar restent approximatifs. Les affiliations de clans varient ; HRI n'est pas une administration centralisée de tous les villages de la côte. **Merca/Barawe et les autres pouvoirs locaux du Benaadir méridional restent agrégés aux communautés locales : leurs emprises urbaines séparées ne sont pas certifiées ici.** OGD est nommé « Communautés somalies » et ne prétend pas que toute la côte de la Jubba appartient au seul groupe ogaden. Le proxy Afgooye est la portion riveraine voisine du RGB partagé du site natif de Mogadishu ; il ne certifie pas la limite urbaine entre les deux villes. Ces limites empêchent une clôture régionale complète.

Le doublon MJT est résolu ; les deux conflits hérités de KENYA x9A78B7 / x5C1ADA restent explicitement **hors de ces cinq nœuds**, pour le lot côtier/oriental suivant. Aucun arbitrage de ces cellules sans rapprochement historique. La finition esthétique du Sahel et des frontières américaines est différée par le joueur, sans écrire dans les lots américains ou SERG.

## Contrôles, concurrence et suite

**{v['passed']}/{v['total']} contrôles territoriaux statiques**, 18 profils compatibles, contrôle de livraison/localisation séparé dans DELIVERY_VALIDATION.json. Commandes : `world1776_horn01.py --preflight`, `--apply --tech --validate`, puis `--validate` après corrections bornées. Premier contrôle archivé : 445/458, treize retours à la ligne hors nœud corrigés sans changement sémantique ; nouvelle allocation POP par provinces uniques et libellés pluriels documentés dans leurs reçus. Les vérifications finales portent sur la version effectivement livrée.

{len(files)} fichiers fonctionnels : 20 fichiers existants ciblés, 18 nouveaux. [FILES_DELIVERED.json](FILES_DELIVERED.json), [DELIVERY_MANIFEST.json](DELIVERY_MANIFEST.json). Comparaison des blocs extérieurs et empreintes des autres fichiers : [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json). SAHEL-01/02-05/06-07, Maghreb, Balkans, Siwa/Fezzan/Gibraltar, SERG, TECH/ECON et versions américaines courantes préservés. Aucun retour à une ancienne baseline, aucune écriture Git/vanilla/SERG.

Test de cette version **NOT_RUN** ; protocole [GROUPED_RUNTIME_ITEMS.md](GROUPED_RUNTIME_ITEMS.md), aucun test intermédiaire demandé. Le retour joueur sur la présence du lot Tchad/Nil ne valide pas HORN-01. WORLD **10/320 (3,13 %)** inchangé, aucun crédit pour régions partielles. Suite déjà autorisée : Congo/Kongo et Angola, puis possessions portugaises et Afrique australe/VOC, en lots distincts ; la finition des courbes reste une passe ultérieure.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# Contrôle groupé HORN-01 — NOT_RUN

Nouvelle partie 1776 : comparer BEFORE/AFTER. Vérifier ETH/Gondar ; liens tributaires TGR/GJM/WLO et autonomie diplomatique ; Choa/Ankober, Harar, Awsa, Kaffa, Wolayta et Yem indépendants ; absence de monarchies Gibe/Leqa du XIXe siècle. Examiner les portions afar (agrégat volontairement pluriel), Asmara/TGR et Massawa/TUR.

Somalie : Mogadishu/HRI, noyau intérieur Geledi, communautés somalies et noyaux nord-est MJT/WSG/ISQ. Ni Hobyo ultérieur ni grande annexion omanaise. Merca/Barawe et limites des clans restent ouverts ; ne pas transformer cette vérification en attestation de cadastre. Les deux conflits KENYA non traités restent des témoins connus.

Contrôler capitales/labels/flags, lois réellement actives, technologies, bâtiments, parcelles et ressources partagées. ETH : types/effectifs militaires inchangés, recrutement déplacé à GONDER et administrations transférées sans nouveaux niveaux. Comparer populations régionales au ledger, emploi et budgets. Jouer un mois, sauvegarder/recharger, consigner uniquement les observations réelles et la version livrée. Le protocole est groupé, sans demande intermédiaire. Courbes volontairement non lissées. Témoins : Sahel/Nil, Maghreb, Balkans, SERG et versions américaines courantes.
''')
    doc('USER_REQUEST.txt',"C'est aussi présent pour les autres sous-agents qui sont en train de bosser sur l'Amérique. Ils font des frontières découpées au cutter. Mais je pense qu'on fera, qu'on repassera pour revoir les frontières plus tard. Je pense que tu peux refaire une passe pour vérifier la conformité géographique sur toute cette région. Puis on va directement passer à l'Empire éthiopien et toute la corne de l'Afrique, avant de continuer vers le sud, vers le Congo, les colonies portugaises et tout le sud de l'Afrique avec les colonies néerlandaises.\n\nN'hésite pas à créer des vaisseaux avec différents degrés d'autonomie si nécessaire.\n\nInterprétation du second message dans son contexte : vassaux et autonomies, pas construction de navires.\n")
    doc('REPRODUCE.md','''# Reproduire les contrôles

`python tools/world1776_horn01.py --validate`

`python tools/world1776_horn01_closeout.py --evidence --reports --final`

Ne pas rejouer --apply ni --tracking. apply_inputs et les trois réparations conservent les reçus antérieurs. La validation écrit seulement les preuves, ne lance pas le moteur et ne change pas les frontières. Une modification future légitime exige une comparaison de composition courante, jamais une restauration de nos frontières précédentes. L'audit antérieur du Sahel est borné dans SAHEL-GEOCHECK-01 et ne se rejoue pas comme si l'extension suivante à ERITREA était une régression.
''')

def tracking():
    path=WORLD/'ROADMAP_STATE.json';data=read(path);assert not any(r['id']=='HORN-01' for r in data['lots'])
    hashes={n:h.b.a.sha(WORLD/n) for n in TRACK}
    for n in TRACK:
        dest=LOT/'tracking_inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((WORLD/n).read_bytes())
    for phase in data['phases']:
        if phase['id']=='P3':
            for region in phase['subregions']:
                if region['id']=='P3-04':region['criteria']['V'].update(status='PARTIAL',evidence='SAHEL-GEOCHECK-01/USER_TEST_OBSERVATION.json',remaining='Présence rapportée en jeu, défaut visuel signalé ; version/durée/sauvegarde non attestées, pas de V entier.')
                if region['id']!='P3-06':continue
                for k,c in region['criteria'].items():
                    if c['status']=='STATIC_VERIFIED':continue
                    if k=='V':c.update(status='PARTIAL',evidence='SAHEL-GEOCHECK-01/USER_TEST_OBSERVATION.json + HORN-01/GROUPED_RUNTIME_ITEMS.md',remaining='Retour joueur borné au Tchad/Nil ; HORN-01 NOT_RUN, aucun critère V entier.');continue
                    prior=c.get('evidence');ev='HORN-01/REPORT.md'
                    if prior and ev not in prior:ev=prior+' + '+ev
                    c.update(status='PARTIAL',evidence=ev,remaining='Noyaux politiques installés ; frontières fines, Benaadir méridional, interfaces KENYA, profils complets et test groupé ouverts. Aucun crédit régional entier.')
        n=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values())
        phase['progress'].update(technical_verified=n,technical_percent=float((Decimal(n)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
    score=sum(p['progress']['technical_verified'] for p in data['phases']);assert score==10 and data['progress']['criteria_total']==320 and data['progress']['runtime_user_validated']==0
    data['progress'].update(technical_verified=10,technical_percent=3.13)
    data['lots'].append(dict(id='SAHEL-GEOCHECK-01',status='BOUNDED_REVIEW_COMPLETE_WITH_LIMITATIONS',functional_writes=0,receipt='SAHEL-GEOCHECK-01/VALIDATION.json',credited_criteria=[],cosmetic_smoothing='DEFERRED_BY_USER'))
    data['lots'].append(dict(id='HORN-01',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope=['Ethiopian imperial/provincial and southern royal cores','Afar/Beja and Somali political envelopes'],files_modified=38,existing_files_modified=20,new_files=18,new_tags=3,activated_existing_tags=15,native_RGBs_transferred=280,new_RGBs=0,pixels_recolored=0,duplicate_owner_resolved=['x2D75F4'],world_population_delta=0,runtime='NOT_RUN',receipt='HORN-01/FILES_DELIVERED.json',credited_criteria=[]))
    data['steering_history'].append(data['current_steering']);data['current_steering']=dict(date='2026-10-27',scope='Sahel geographic review, Ethiopia and Horn, then Congo/Portuguese possessions/southern Africa and Dutch colonies',authority='HORN-01/USER_REQUEST.txt',last_lot='HORN-01',next_pass='Congo/Kongo and Angola territorial work; then remaining Portuguese and southern African/VOC sectors',cosmetic_smoothing_deferred=True,autonomous_subjects_authorized=True,intermediate_player_tests_requested=False,runtime_validation_timing='GROUPED_AFRICA',full_V_credit=False)
    assert all(h.b.a.sha(WORLD/n)==v for n,v in hashes.items()),'Concurrent WORLD tracking update.'
    write(path,data)
    entry='''\n\n## SAHEL-GEOCHECK-01 et HORN-01 — 27 octobre 2026\n\nRetour joueur conservé : pays présents au test, formes irrégulières signalées ; version précise/durée/sauvegarde non fournies, aucun V entier. La finition des courbes est reportée explicitement. Audit Sahel–Nil sans écriture fonctionnelle : 452/452 contrôles bornés, aucune nouvelle permutation de noyau démontrée, approximations et poches résiduelles conservées comme limites. Transition directe Éthiopie/Corne autorisée, avec vassaux/autonomies si nécessaires, puis Congo, possessions portugaises et Afrique australe/VOC.\n\nHORN-01 installé : ETH/Gondar, Tigré/Godjam/Wollo tributaires, Choa/Harar/Awsa/Kaffa/Wolayta/Yem indépendants, communautés régionales autonomes et enveloppe hiraab/Mogadishu distincte de Geledi. 280 RGB natifs réattribués, un doublon MJT résolu, aucun pixel/hub/ressource redessiné. Trois TAG nouveaux, quinze activations natives ; 20 fichiers existants ciblés, 18 ajouts. Cohortes/niveaux/PM conservés, références militaires et administrations impériales replacées à GONDER. 18 profils PASS_STATIC_ONLY, aucune nouvelle incompatibilité existante P0/P1. Preuves VALIDATION.json, TECH_NON_REGRESSION.json et DELIVERY_VALIDATION.json. Benaadir méridional agrégé, interfaces KENYA et frontières fines ouvertes ; test HORN NOT_RUN. WORLD 10/320 (3,13 %), aucun nouveau crédit régional.\n'''
    for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
    h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## HORN-01 — limites ouvertes\n\nAutonomies provinciales 1776 traduites par liens tributaires, sans certification de tous les tributs/règlements. Interfaces Semien/Tigré/Wollo, hauts/bas-pays de l'Ouest, noyaux méridionaux et affiliations somalies approximatifs. Merca/Barawe restent dans l'agrégat de communautés locales, pas des juridictions urbaines séparées certifiées. Afgooye/Mogadishu proches dans le maillage ; AFR agrège des pouvoirs disjoints. Deux conflits KENYA x9A78B7/x5C1ADA hérités, hors des cinq nœuds de ce lot, à examiner historiquement dans la suite orientale. Cartes c.1700/c.1800 ne valent pas cadastre 1776. Proxies culturels/religieux et démographie technique, capitales/hubs/flags, lois effectives, emploi/budgets à vérifier au test groupé. Les courbes sont délibérément reportées, pas déclarées conformes. Aucun verrou humain nouveau ni test intermédiaire demandé ; Congo et suite australe déjà autorisés.\n''')
    h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## HORN-01 — périmètre installé\n\nCinq nœuds ERITREA/GONDER/AMHARA/OROMIA/SOMALILAND des états et leurs seules portions POP/bâtiments listées dans SCOPES.json. c:ETH militaire : trois références régionales vers GONDER, comptes/types/services conservés. Administrations ETH à total constant vers la cour. Treize histoires de TAG natifs réactivés ciblées ; cinq histoires nouvelles, définitions propres, effets/loi, trois liens tributaires, sept neutralisations de modèles de personnages 1836, noms FR/EN. Aucun nouveau personnage, province, pixel, terrain, ressource, locator ou recette commune. KENYA non écrit. Anciennes preuves et mises à jour américaines courantes préservées ; aucun suivi SERG ni vanilla ni Git écrit. Énumération canonique HORN-01/PLAN.json, reçus FILES_DELIVERED.json et réparations séparées.\n''')
    h.save(WORLD/'NEXT_ACTION.md','''# Prochaine action — après HORN-01\n\nConsigne : conformité géographique de la bande Sahel/Nil, puis Éthiopie/Corne ; finition des courbes reportée. Ces deux passes sont livrées dans SAHEL-GEOCHECK-01 et HORN-01. Lire REPORT.md, SOURCES.md, PLAN.json, VALIDATION.json, TECH_NON_REGRESSION.json et FILES_DELIVERED.json de HORN-01. Retour joueur antérieur borné à la présence et au défaut visuel Tchad/Nil ; cette nouvelle version reste NOT_RUN.\n\nSuite déjà autorisée : **Congo/Kongo et Angola**, puis autres possessions portugaises et Afrique australe avec établissements néerlandais/VOC. Réutiliser MAP1 sans prendre ses catalogues comme preuves lues. Limiter les Européens aux possessions effectivement tenues en 1776 ; aucune annexion de tout un arrière-pays par commodité. Frontières seulement, initialisations nécessaires, aucun flavor ou raffinement de bâtiments. Préserver les autonomies et suzerainetés appropriées.\n\nLimites HORN : Benaadir méridional agrégé, frontières fines, Afgooye/Mogadishu, interfaces KENYA et certaines dépendances ; pas de clôture historique totale. Contrôles joueur groupés, aucun test intermédiaire. Préserver toutes les versions courantes du Sahel/Nil, Maghreb, Balkans, SERG, TECH/ECON et Amériques ; aucun retour à une ancienne baseline. WORLD 10/320 (3,13 %), aucun nouveau critère entier/humain.\n''')
    concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['HORN-01']=dict(receipt='HORN-01/CONCURRENT_CHANGES.json',existing_functional_files_modified=20,new_files=18,native_RGBs_transferred=280,pixels_recolored=0,new_RGBs=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False);write(WORLD/'CONCURRENT_CHANGES.json',concurrent)
    h.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=h.b.a.sha(WORLD/n)) for n in TRACK])

def final():
    rows=delivered();checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    for rel,r in rows.items():ck('current_delivered_hash.'+rel,h.b.a.sha(ROOT/rel)==r['after'])
    h.dump('FILES_DELIVERED.json',list(rows.values()));ck('38_functional_files',len(rows)==38)
    ck('territorial_static_pass',h.load('VALIDATION.json')['status']=='PASS')
    for r in h.load('STARTING_TECH_NEW_COUNTRIES.json'):ck('new_profile.'+r['TAG'],r['status']=='PASS_STATIC_ONLY' and not r['findings'])
    for r in h.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:ck('no_new_P0_P1.'+r['TAG'],not r['introduced'])
    pop=h.load('POPULATION_LEDGER.json');ck('world_population_conserved',pop['delta']==0)
    for r in pop['state_totals']:ck('regional_population_conserved.'+r['state'],r['before']==r['after'])
    ck('all_profiles_populated',all(any(r['country']==t and r['after']>0 for r in pop['portions']) for t in h.p.COUNTRIES))
    transfers=[c for r in h.load('PLAN.json') for c in r['RGBs']];ck('280_unique_transferred_RGBs',len(transfers)==len(set(transfers))==280)
    language_checks=[];sets={}
    for lang in ['french','english']:
        replacements=loc.entries(lang,replacement=True);own={k:v for k,v in replacements.items() if any(path.name==h.PREFIX+'_l_'+lang+'.yml' for path,n,t in v)};sets[lang]=set(own)
        for k,v in own.items():language_checks.append(dict(check=lang+'.unique_replacement_key.'+k,passed=len(v)==1))
    language_checks.append(dict(check='same_bilingual_keys',passed=sets['french']==sets['english']))
    h.dump('LOCALIZATION_CHECK.json',dict(status='PASS' if all(r['passed'] for r in language_checks) else 'FAIL',checks=language_checks,intentional_native_overrides=['WLG','ARS','BRN','HDY','OGD'],render_runtime='NOT_RUN'))
    ck('localization_bilingual_unique_replacements',all(r['passed'] for r in language_checks))
    before=h.load('APPLY_BEFORE.json');outside=[]
    for rel,v in before['protected'].items():
        if rel in rows:continue
        if not (ROOT/rel).exists() or h.b.a.sha(ROOT/rel)!=v:outside.append(rel)
    ck('all_preexisting_outside_scope_files_preserved',not outside,outside)
    data=read(WORLD/'ROADMAP_STATE.json');technical=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED'];human=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
    ck('canonical_progress',len(technical)==10 and not human and data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320)
    h.dump('PROGRESS_CALCULATION.json',dict(credited=technical,user_validated=human,numerator=10,denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
    needed=['REPORT.md','SOURCES.md','PLAN.json','GEOGRAPHIC_CROSSWALK.json','POPULATION_LEDGER.json','POPULATION_BEFORE_AFTER.csv','COUNTRY_PROFILES.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','TECH_NON_REGRESSION.json','VALIDATION.json','CONCURRENT_CHANGES.json','LOCALIZATION_CHECK.json','BEFORE.png','AFTER.png','GROUPED_RUNTIME_ITEMS.md','FILES_DELIVERED.json','FORMATTING_REPAIR.json','POP_ALLOCATION_REPAIR.json','PLURAL_LABELS_REPAIR.json','TRACKING_PATCHES.json','PROGRESS_CALCULATION.json']
    for n in needed:ck('evidence_exists.'+n,(LOT/n).is_file())
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False)
    h.dump('DELIVERY_VALIDATION.json',result)
    files=[ROOT/r for r in rows]+[LOT/n for n in needed]+[LOT/'DELIVERY_VALIDATION.json']+[WORLD/n for n in TRACK]+[ROOT/'tools'/n for n in ['world1776_horn01.py','world1776_horn01_plan.py','world1776_horn01_inspect.py','world1776_horn01_closeout.py','world1776_sahel_geocheck01.py']]
    files+=[p for p in (LOT/'sources').iterdir() if p.is_file()]+[p for p in (WORLD/'SAHEL-GEOCHECK-01').iterdir() if p.is_file()]
    h.dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():h.b.a.sha(p) for p in files})
    print('Delivery:',result['status'],result['passed'],'/',result['total']);print('FAIL:',[r for r in checks if not r['passed']])
    return result['status']=='PASS'

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for k in ['evidence','reports','tracking','final']:a.add_argument('--'+k,action='store_true')
    args=a.parse_args()
    if args.evidence:evidence()
    if args.reports:reports()
    if args.tracking:tracking()
    if args.final:raise SystemExit(0 if final() else 1)
