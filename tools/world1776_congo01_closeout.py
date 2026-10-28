"""Congo territorial evidence and bounded delivery checks, no engine claims."""
import json,csv,shutil,argparse
from collections import Counter,deque
from decimal import Decimal,ROUND_HALF_UP
import world1776_congo01 as h
import world1776_sahel0205_closeout as old
import localization_duplicate_audit as loc
ROOT,LOT=h.ROOT,h.LOT
WORLD=LOT.parent
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']
def doc(name,text):h.save(LOT/name,text)
def write(path,value):h.save(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def read(path):return json.loads(path.read_text('utf-8-sig'))
def delivered():
 rows={r['file']:dict(r) for r in h.load('FILES_MODIFIED.json')}
 for r in h.load('COMPATIBILITY_AND_LABEL_REPAIR.json')['files']:rows[r['file']]['after']=r['after']
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
    h.dump('GEOGRAPHIC_CROSSWALK.json',dict(cells=cross,new_RGBs=0,pixels_recolored=0,historical_date='1776-01-01',coordinates_are_navigation_not_cadastre=True))
    h.geometry(h.raw(LOT/'apply_inputs'/h.ST));(LOT/'BEFORE.png').write_bytes((LOT/'PROPOSED.png').read_bytes())
    h.geometry(h.raw(ROOT/h.ST));(LOT/'AFTER.png').write_bytes((LOT/'PROPOSED.png').read_bytes())

def reports():
    pop=h.load('POPULATION_LEDGER.json');v=h.load('VALIDATION.json');tech=h.load('TECH_NON_REGRESSION.json')
    countries='\n'.join('| '+t+' | '+r['kind']+' | '+str(len(r['tech']))+' | '+r['capital'].replace('STATE_','')+' |' for t,r in h.p.COUNTRIES.items())
    pops='\n'.join('| '+r['TAG']+' | '+f"{r['before']:,}".replace(',',' ')+' | '+f"{r['after']:,}".replace(',',' ')+' |' for r in pop['countries'])
    doc('REPORT.md',f'''# CONGO-01 — Bas Congo, Kongo et Angola occidental

Passe commencée le 27 octobre et clôturée le **28 octobre 2026**. Référence : **1er janvier 1776**. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Autorisation directe « ok commence directe », puis « ok fini ». Frontières et initialisation nécessaire uniquement ; finition des courbes reportée par le joueur.

## Corrections installées

- **69 RGB natifs dans 19 groupes**, six régions moteur : CONGO, BAS_CONGO, NORTH_ANGOLA, SOUTH_ANGOLA, EAST_ANGOLA et GABON. Aucun nouveau RGB, pixel, terrain, ressource ou locator. Liste exhaustive : [PLAN.json](PLAN.json), coordonnées et correspondance : [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json).
- Le noyau **KON** conserve Mbanza Kongo ; sa région capitale devient NORTH_ANGOLA, où se trouve cette ville. Soyo/Mpinda est séparé du domaine royal. Kakongo/Malemba et Ngoyo/Cabinda sont distingués au nord de l'estuaire. Cabinda ne devient pas une possession portugaise de 1783 au départ de 1776.
- **Loango, Tio/Teke, Yaka et Kasanje** reçoivent une représentation étatique. Matamba est séparé de Kasanje. Bailundo et Bié reçoivent des noyaux distincts au plateau, tandis que les autres communautés ovimbundu restent agrégées. Aucune hégémonie uniforme sur toutes les communautés voisines n'est certifiée.
- Dembos, Kisama/Libolo et Mayumba/chefferies côtières sont des **agrégats décentralisés**, sans roi unificateur inventé. La séparation du littoral gabonais retire l'administration directe par Loango, sans prétendre que chaque cellule était une province de Mayumba ou de culture homogène.
- Le Portugal garde Luanda, Novo Redondo et Benguela ; les points fortifiés de la vallée du Kwanza, Encoje et Caconda sont reliés à ses possessions. **Ces corridors de cellules entières sont une approximation politique et de continuité demandée par le joueur. Leur largeur excède le rayon d'une garnison ; ils ne prouvent pas une administration portugaise uniforme des villages traversés.** Ambriz reste hors possession portugaise. Les grands arrière-pays et royaumes du plateau ne sont pas annexés à la Couronne.

## Institutions et technologies

Neuf TAG nouveaux : SYO, KKG, NGY, MTM, MBL, BIE, DMB, KIS, MYU. Quatre TAG natifs changent de catégorie politique : LNG, TKE, YKA, KSN. Les dix pays centralisés de cet ensemble sont des monarchies non reconnues ; les trois agrégats décentralisés gardent les institutions locales. Aucun nouveau dirigeant, personnage, tribut, traité ou vassal automatique. La vassalité ne sert pas à transformer un commerce ou une prétention portugaise en souveraineté.

| TAG | Catégorie | Technologies explicites | Capitale moteur |
|---|---|---:|---|
{countries}

Les profils sont expliqués individuellement dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json). Une loi locale de coutumes commerciales réutilise les effets du mercantilisme et le prérequis de relations internationales. Elle évite de distribuer l'assurance pour justifier les marchés locaux. Les usages ruraux, artisanaux, commerciaux et militaires sont distingués ; aucune modification du graphe TECH, des recettes ou des PM communs.

Le premier contrôle technique a identifié cinq dépendances agricoles manquantes. Elles ont été fermées par la capacité d'élevage de petit bétail documentée par Proyart, 1776, p. 32 ; le rapprochement avec le Tio intérieur demeure une inférence régionale explicitée. [COMPATIBILITY_AND_LABEL_REPAIR.json](COMPATIBILITY_AND_LABEL_REPAIR.json) conserve les entrées immédiates et la correction. Les anciens résultats restent dans RUN01_*.json. Ce choix n'atteste pas un secteur bovin développé.

## Population et données conservées

Monde : **{pop['world_before']:,} → {pop['world_after']:,}**, delta **{pop['delta']}**. Chaque cohorte conserve ses attributs culturels, religieux et serviles ; répartition technique par provinces natives uniques, arrondis entiers conservatifs. Ce ne sont pas des recensements historiques. Les six totaux régionaux restent identiques ; détails : [POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv).

| Pays/agrégat touché | Avant | Après |
|---|---:|---:|
{pops}

Tous les niveaux bâtis, sélections de PM, types et effectifs militaires sont conservés. Seule la propriété des portions partagées est répartie. Aucun raffinement de bâtiment ni recette de flavor. Les cultures bakongo/ovimbundu héritées servent parfois de proxys, notamment pour les Mbundu ; aucune conversion des habitants n'est effectuée.

## Contrôles et concurrence

- [VALIDATION.json](VALIDATION.json) : **{v['passed']}/{v['total']} contrôles statiques**. Attribution exacte, absence de nouveau doublon, capitales, continuité des nouveaux noyaux centralisés, cohortes et données hors blocs possédés.
- **13 profils** : {'PASS_STATIC_ONLY' if tech['all_new_profiles_pass'] else 'À CORRIGER'}. Dix pays témoins existants : aucune nouvelle incompatibilité P0/P1. Les dettes héritées de KON et autres témoins ne sont pas effacées par une distribution de technologies.
- 8 fichiers existants ciblés et 14 ajouts fonctionnels. Les anciens lots WORLD, SERG, TECH/ECON et les Amériques sont préservés. Deux changements concurrents de libellés Sacramento correspondent au manifeste américain courant ; [EXTERNAL_COMPOSITION_REVIEW.json](EXTERNAL_COMPOSITION_REVIEW.json). Aucun retour à une baseline, Git/vanilla/SERG non écrits.
- Contrôle documentaire final : [DELIVERY_VALIDATION.json](DELIVERY_VALIDATION.json), empreintes : [DELIVERY_MANIFEST.json](DELIVERY_MANIFEST.json).

## Limites et suite

Les noyaux et corridors utilisent des cellules entières, pas un cadastre 1776. Noms de hubs natifs, drapeaux, budgets, chargement, lois effectivement actives, recrutement, fronts, ravitaillement et sauvegarde/rechargement restent à voir au **test africain groupé**. Aucun test intermédiaire demandé, aucune validation humaine créée. Les composants portugais maritimes hérités ne sont pas assimilés à des enclaves terrestres nouvelles ; OVM reste un agrégat plural, partiellement séparé par les nouveaux royaumes et corridors.

Cette passe ne clôt ni tout le bassin congolais ni P3-05 : domaines Luba/Lunda/Kuba/Kazembe, interfaces du Congo intérieur, répartition fine des principautés du Kongo et certains sobados restent à examiner. WORLD demeure **10/320 (3,13 %)**, aucun critère entier nouveau. Suite autorisée : interfaces intérieures vers le Zambèze, autres possessions portugaises/Mozambique, puis Afrique australe et établissements néerlandais/VOC. Aucun lissage cosmétique lancé.
''')
    doc('SOURCES.md','''# Sources consultées — CONGO-01

Consultation et installation 27–28 octobre 2026 ; référence 1er janvier 1776.

1. **J. Vansina**, à partir d'une contribution de T. Obenga, « Le Royaume du Kongo et ses voisins », *Histoire générale de l'Afrique*, V, chapitre 19, p. 601–642. [PDF public](https://bokundoli.org/wp-content/uploads/2021/12/T5-21.pdf), copie et extraction dans sources/UNESCO_V_VANSINA_KONGO.pdf/.txt. Passages lus sur Soyo, les royaumes côtiers, les routes et les mutations du XVIIIe siècle ; carte **19.19, p. 641, PDF 41**, rendue et examinée dans sources/MAP_19_19.png. Elle localise les pouvoirs et marchés, sans fournir leurs limites cadastrales de janvier 1776. P. 635 : Encoje 1759, Cabinda 1783 ; p. 636 : Mayumba après 1750, Loango/Tio ; p. 642 : Kasanje, Yaka, Bailundo/Bié. La coquille de date « 1664–1672 » pour Sousa Coutinho n'est pas reprise : les archives contemporaines de 1769 contrôlent sa chronologie.

2. **Estevam C. Thompson**, « Fontes coloniais para uma história pré-colonial de Benguela, séculos XVII a XIX », *Africana Studia*, 25 (2015), p. 33–69. [Article universitaire](https://ojs.letras.up.pt/index.php/AfricanaStudia/article/download/7863/7214/25490), copie intégrale/extraction sources/AFRICANA_STUDIA25.pdf/.txt. Passages effectivement lus : **p. 42–43, PDF 10–11**. Ils distinguent les postes, leurs environs, les autorités locales et les prétentions coloniales. Les corridors installés sont une approximation du maillage et une réponse à la règle de continuité du joueur, pas une affirmation de contrôle effectif partout.

3. **Liévin-Bonaventure Proyart**, *Histoire de Loango, Kakongo et autres royaumes d'Afrique*, Paris/Lyon, **1776**, chapitre VI, **p. 31–33, notamment p. 32, PDF 38**. [Fac-similé public consulté](https://www.clist.eu/Textes/royaume-kongo/Proyart%201776%20(Histoire%20de%20Loango,%20Kakongo,%20et%20autres).pdf). Élevage de porcs, chèvres, moutons et volaille : preuve du petit élevage côtier, pas d'une économie pastorale bovine étendue. Lecture du passage par l'outil web ; livre entier non lu et non téléchargé. L'application au Tio intérieur est une inférence régionale minimale liée au parent agricole du graphe local.

4. **Arquivo Histórico Ultramarino/DGLAB**, catalogue Angola, notice **4956**, lettre de Sousa Coutinho, **30 novembre 1769**, AHU-Angola cx.53 doc.76. [Catalogue public](https://ahu.dglab.gov.pt/wp-content/uploads/sites/24/2018/04/PT-AHU-CU-ANGOLA-Parcial1602-1799.pdf), notice indexée lue p.865/1286 : fortification de Novo Redondo, commerce et communication terrestre Luanda–Benguela. La notice est consultée, pas le manuscrit de la lettre ; elle ne démontre pas une occupation continue de la côte.

5. **HPIP / Património de Influência Portuguesa**, [Caconda](https://hpip.org/pt/Contents/Place/251), [Sumbe/Novo Redondo](https://hpip.org/pt/Contents/Place/306). Notices savantes indexées effectivement lues : déplacement de Caconda en 1769 vers Catala, fondation pombaline de Novo Redondo en 1769. Accès direct web502 et téléchargement local refusé par vérification du certificat ; aucune copie intégrale de ces pages revendiquée. Les dates sont aussi corroborées par l'article Thompson consulté.

6. **Royal Museum for Central Africa**, [The Kongo kingdom](https://www.africamuseum.be/en/discover/history_articles/kongo-kingdom), page effectivement ouverte : Mbanza Kongo et distinction entre diffusion culturelle et souveraineté. Carte vers1650 signalée comme antérieure ; aucune frontière1650 transplantée mécaniquement en1776.

7. **MAP1**, R7_SUBSAHARAN_AFRICA : inventaires/recommandations et dossiers 0032/0139 disponibles, lus comme pistes. Leurs anciens chiffres RGB et leurs catalogues non consultés ne sont pas des preuves de l'état courant. BASELINE.json/CURRENT_INVENTORY.json enregistrent le vrai workspace.

## Interprétation et incertitudes

Les correspondances RGB sont des choix d'implémentation expliqués dans PLAN.json, comparés au bitmap, aux rivières et aux localités. Aucun partage par distance à une capitale ou frontière rectangulaire automatique. Les petits royaumes ne sont pas reconstitués jusqu'au dernier sobado. Les cultures et populations héritées ne sont pas des estimations historiques validées. Dembos, Kisama/Libolo et les chefferies côtières restent pluriels. Les titres de « vassal » dans les archives coloniales ne déclenchent pas automatiquement de dépendance diplomatique dans le jeu.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# Contrôle africain groupé — CONGO-01

Statut NOT_RUN. Aucune attestation humaine nouvelle, aucun test intermédiaire demandé.

Lors du test groupé : nouvelle partie1776 ; vérifier Kongo/MbanzaKongo, Soyo, Kakongo/Ngoyo et Cabinda non portugaise, Loango/Tio/Yaka/Kasanje, Matamba et plateau Bailundo/Bié. Vérifier les agrégats Dembos/Kisama/Mayumba, le raccord des postes portugais à la côte et Ambriz hors Portugal. Aucun territoire centralisé nouvellement isolé dans les chefferies.

Vérifier portraits/drapeaux/noms et capitales sans prétendre que les hubs natifs ont été déplacés. Contrôler lois réellement actives, technologies visibles, construction/recrutement et maintien des niveaux/PM hérités. Observer accès au marché, approvisionnement, budgets et fronts, puis sauvegarder/recharger. Garder des témoins Sahel/Nil/Corne/Maghreb et Amériques/SERG. Noter la version exacte, les observations et la durée réellement testée ; ne pas les déduire du présent protocole. Courbes irrégulières déjà signalées : finition reportée, pas validée.
''')
    doc('REPRODUCE.md','''# Reproduction en lecture seule

Depuis le dépôt, avec Python configuré :

`python tools/world1776_congo01.py --tech --validate`

`python tools/world1776_congo01_closeout.py --final`

Ne pas relancer --apply, --tracking ni le survey initial. Les entrées et reçus sont immuables ; un changement concurrent doit être rapproché de son manifeste, jamais annulé pour faire passer un test. Les anciens reçus de sous-lots sont historiques. Aucun lancement moteur dans ces commandes. La validation bornée ne remplace pas le contrôle joueur groupé.
''')

def tracking():
    assert not (LOT/'TRACKING_PATCHES.json').exists(),'Tracking already updated.'
    hashes={n:h.b.a.sha(WORLD/n) for n in TRACK}
    for n in TRACK:
        dest=LOT/'tracking_inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORLD/n,dest)
    data=read(WORLD/'ROADMAP_STATE.json')
    assert not any(r['id']=='CONGO-01' for r in data['lots'])
    for phase in data['phases']:
        for region in phase['subregions']:
            if region['id']=='P3-05':
                for key,c in region['criteria'].items():
                    if c['status']=='STATIC_VERIFIED':continue
                    c.update(status='PARTIAL' if key!='V' else 'NOT_STARTED',evidence='CONGO-01/REPORT.md' if key!='V' else 'CONGO-01/GROUPED_RUNTIME_ITEMS.md',remaining='Lot occidental installé ; noyaux intérieurs Luba/Lunda/Kuba/Kazembe, limites fines, démographie historique et moteur non certifiés. Aucun point entier.')
        count=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values())
        phase['progress'].update(technical_verified=count,technical_percent=float((Decimal(count)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
    total=sum(p['progress']['technical_verified'] for p in data['phases']);assert total==10 and data['progress']['criteria_total']==320
    data['progress'].update(technical_verified=total,technical_percent=3.13)
    data['lots'].append(dict(id='CONGO-01',date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',existing_files_modified=8,new_files=14,new_tags=9,reviewed_profiles=13,native_RGBs_transferred=69,new_RGBs=0,pixels_recolored=0,world_population_delta=0,receipt='CONGO-01/FILES_DELIVERED.json',credited_criteria=[],runtime='NOT_RUN'))
    data['steering_history'].append(data['current_steering'])
    data['current_steering']=dict(date='2026-10-28',authority='CONGO-01/USER_REQUEST.txt',scope='User-authorized African territorial continuation; western Congo/Kongo and Angola lot installed',last_lot='CONGO-01',next_pass='Interior interfaces Luba/Lunda/Kuba/Kazembe towards Zambezi, remaining Portuguese possessions/Mozambique, then southern Africa and VOC',cosmetic_smoothing_deferred=True,autonomous_subjects_authorized=True,intermediate_player_tests_requested=False,runtime_validation_timing='GROUPED_AFRICA',full_V_credit=False)
    entry='''\n\n## CONGO-01 — 28 octobre 2026\n\nBas Congo/Kongo et Angola occidental : 69 RGB natifs réattribués, aucun nouveau pixel/RGB. Soyo, Kakongo, Ngoyo, Matamba, Bailundo/Bié et agrégats Dembos/Kisama/Mayumba ; Loango/Tio/Yaka/Kasanje centralisés. MbanzaKongo reste KON et devient région capitale correcte. Postes portugais reliés par corridors natifs explicitement approximatifs ; Ambriz hors Portugal. Neuf TAG nouveaux, 13 profils contrôlés ; huit fichiers existants ciblés,14 ajouts. Cohortes/niveaux/PM/armées conservés, delta mondial nul. Rapports et limites CONGO-01/REPORT.md ; aucune clôture des interfaces Luba/Lunda/Kuba/Kazembe. Deux libellés Sacramento concurrents rapprochés du manifeste américain courant, préservés. Courbes et tests africains groupés différés ; aucun reçu humain ni point entier, WORLD10/320(3,13%).\n'''
    assert all(h.b.a.sha(WORLD/n)==v for n,v in hashes.items())
    write(WORLD/'ROADMAP_STATE.json',data)
    for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
    h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## CONGO-01 — limites ouvertes, 28 octobre\n\nCorridors et noyaux sur cellules natives, pas cadastre1776 ; contrôle portugais discontinu traduit par corridor à cause de la règle joueur, largeur supérieure aux garnisons. Kongo provincial, sobados, arrière-pays Tio/Yaka, cultures proxys et chefferies côtières agrégées restent approximatifs. Luba/Lunda/Kuba/Kazembe et Congo intérieur non clôturés. Budget, marchés, chargement/lois/capitales/hubs, fronts et sauvegarde à vérifier au test africain groupé, NOT_RUN. Aucun critère V/point nouveau. Dettes techniques héritées des pays témoins conservées, pas de grant pour les masquer.\n''')
    h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## CONGO-01 — périmètre installé, 28 octobre\n\nSix nœuds d'états/POPs CONGO/BAS_CONGO/NORTH_ANGOLA/SOUTH_ANGOLA/EAST_ANGOLA/GABON, portions de bâtiments SCOPES.json, seuls c:KSN/LNG/TKE/YKA d'histoire nationale ; définitions privées incluant seule capitale KON. Neuf TAG propres, loi/effet et FR/EN. Aucun pixel, terrain, locator, recette commune, militaire ou suiviSERG écrit. Versions américaines courantes préservées, dont retouche de libellé Sacramento rapprochée en EXTERNAL_COMPOSITION_REVIEW.json. Reçu initial FILES_MODIFIED.json et correction technique COMPATIBILITY_AND_LABEL_REPAIR.json conservés ; version finale FILES_DELIVERED.json.\n''')
    h.save(WORLD/'NEXT_ACTION.md','''# Prochaine action — après CONGO-01\n\nLot occidental Congo/Kongo–Angola installé. Lire CONGO-01/REPORT.md, SOURCES.md, PLAN.json, VALIDATION.json, TECH_NON_REGRESSION.json et FILES_DELIVERED.json. Les corridors portugais et les noyaux sur cellules natives sont une approximation explicite ; ni contrôle uniforme, ni fermeture de tout le bassin congolais certifiés.\n\nSuite déjà autorisée : interfaces intérieures Luba/Lunda/Kuba/Kazembe vers le Zambèze, autres possessions portugaises/Mozambique, puis Afrique australe et établissements néerlandais/VOC. Délimiter chaque lot depuis la version courante et préserver Congo-01, Sahel/Nil/Corne/Maghreb/Balkans, SERG, TECH/ECON et les Amériques. Frontières et initialisation nécessaire uniquement, aucun flavor. Ne pas étendre les postes européens à tout l'arrière-pays.\n\nCourbes reportées ; tests africains groupés, aucun test intermédiaire demandé. Aucun nouveau reçu humain. WORLD10/320(3,13%), aucun critère entier crédité pour un noyau partiel.\n''')
    concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['CONGO-01']=dict(receipt='CONGO-01/CONCURRENT_CHANGES.json',external_review='CONGO-01/EXTERNAL_COMPOSITION_REVIEW.json',existing_functional_files_modified=8,new_files=14,native_RGBs_transferred=69,pixels_recolored=0,new_RGBs=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False);write(WORLD/'CONCURRENT_CHANGES.json',concurrent)
    h.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=h.b.a.sha(WORLD/n)) for n in TRACK])

def final():
    rows=delivered();checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    for rel,r in rows.items():ck('delivered_hash.'+rel,h.b.a.sha(ROOT/rel)==r['after'])
    h.dump('FILES_DELIVERED.json',list(rows.values()));ck('22_functional_files',len(rows)==22)
    ck('territorial_static_pass',h.load('VALIDATION.json')['status']=='PASS')
    for r in h.load('STARTING_TECH_NEW_COUNTRIES.json'):ck('profile.'+r['TAG'],r['status']=='PASS_STATIC_ONLY')
    for r in h.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:ck('no_new_P0_P1.'+r['TAG'],not r['introduced'])
    pop=h.load('POPULATION_LEDGER.json');ck('population_world',pop['delta']==0)
    for r in pop['state_totals']:ck('population_region.'+r['state'],r['before']==r['after'])
    ck('all_profiles_populated',all(any(r['country']==t and r['after']>0 for r in pop['portions']) for t in h.p.COUNTRIES))
    colors=[c for r in h.load('PLAN.json') for c in r['RGBs']];ck('69_unique_transfers',len(colors)==len(set(colors))==69)
    language=[];sets={}
    for lang in ['french','english']:
        allkeys=loc.entries(lang,replacement=True);own={k:v for k,v in allkeys.items() if any(path.name==h.PREFIX+'_l_'+lang+'.yml' for path,n,t in v)};sets[lang]=set(own)
        language.extend(dict(check=lang+'.'+k,passed=len(v)==1) for k,v in own.items())
    language.append(dict(check='same_bilingual_keys',passed=sets['french']==sets['english']))
    h.dump('LOCALIZATION_CHECK.json',dict(status='PASS' if all(r['passed'] for r in language) else 'FAIL',checks=language,render_runtime='NOT_RUN'));ck('localization',all(r['passed'] for r in language))
    certified={r['file']:r['after'] for r in h.load('EXTERNAL_COMPOSITION_REVIEW.json')['files']}
    outside=[r for r,v in h.load('APPLY_BEFORE.json')['protected'].items() if r not in rows and h.b.a.sha(ROOT/r)!=v and h.b.a.sha(ROOT/r)!=certified.get(r)]
    ck('outside_files_preserved_or_sourced_external',not outside,outside)
    data=read(WORLD/'ROADMAP_STATE.json');technical=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED'];human=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
    ck('canonical_progress',len(technical)==10 and not human and data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320)
    h.dump('PROGRESS_CALCULATION.json',dict(credited=technical,user_validated=human,numerator=10,denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
    needed=['REPORT.md','SOURCES.md','PLAN.json','GEOGRAPHIC_CROSSWALK.json','POPULATION_LEDGER.json','POPULATION_BEFORE_AFTER.csv','COUNTRY_PROFILES.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','TECH_NON_REGRESSION.json','VALIDATION.json','CONCURRENT_CHANGES.json','LOCALIZATION_CHECK.json','BEFORE.png','AFTER.png','GROUPED_RUNTIME_ITEMS.md','FILES_DELIVERED.json','COMPATIBILITY_AND_LABEL_REPAIR.json','EXTERNAL_COMPOSITION_REVIEW.json','TRACKING_PATCHES.json','PROGRESS_CALCULATION.json']
    for n in needed:ck('evidence.'+n,(LOT/n).is_file())
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False);h.dump('DELIVERY_VALIDATION.json',result)
    files=[ROOT/r for r in rows]+[LOT/n for n in needed]+[LOT/'DELIVERY_VALIDATION.json']+[WORLD/n for n in TRACK]+[ROOT/'tools'/('world1776_congo01'+s+'.py') for s in ['', '_plan','_inspect','_closeout']]+[p for p in (LOT/'sources').iterdir() if p.is_file()]
    h.dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():h.b.a.sha(p) for p in files})
    print('Delivery',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']]);return result['status']=='PASS'

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ['evidence','reports','tracking','final']:p.add_argument('--'+k,action='store_true')
    a=p.parse_args()
    if a.evidence:evidence()
    if a.reports:reports()
    if a.tracking:tracking()
    if a.final:raise SystemExit(0 if final() else 1)
