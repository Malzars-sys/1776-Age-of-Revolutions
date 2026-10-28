"""Interior territorial evidence and bounded delivery checks, no engine claims."""
import json,csv,shutil,argparse
from collections import Counter,deque
from decimal import Decimal,ROUND_HALF_UP
import world1776_interior01 as h
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
 for r in h.load('COMPATIBILITY_REPAIR.json')['files']:rows[r['file']]['after']=r['after']
 return rows

def evidence():
    before=h.load('APPLY_BEFORE.json');plan=h.load('PLAN.json');a=Counter();z=Counter()
    for path in h.b.tech.effective('common/history/pops'):
        rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
        z.update(old.portions(h.raw(path)))
        a.update(old.portions(h.raw(LOT/'apply_inputs'/rel) if rel in before['scope'] else h.raw(path)))
    states={r['state'] for r in plan};tags={r['source'] for r in plan}|{r['target'] for r in plan}|set(h.p.COUNTRIES)
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
    after={r['TAG']:r for r in h.load('STARTING_TECH_NEW_COUNTRIES.json')+h.load('STARTING_TECH_EXISTING_AFTER.json')}
    countries='\n'.join('| '+t+' | '+r.get('fr',t)+' | '+r['kind']+' | '+str(len(after[t]['technologies']))+' | '+r['capital'].replace('STATE_','')+' |' for t,r in h.p.COUNTRIES.items())
    pops='\n'.join('| '+r['TAG']+' | '+f"{r['before']:,}".replace(',',' ')+' | '+f"{r['after']:,}".replace(',',' ')+' |' for r in pop['countries'])
    states=', '.join(r['state'].removeprefix('STATE_') for r in pop['state_totals'])
    doc('REPORT.md',f'''# INTERIOR-01 — Congo intérieur, Grands Lacs et Mozambique

**28 octobre 2026 — référence : 1er janvier 1776.** Statut **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Demande directe conservée dans USER_REQUEST.txt. Corrections territoriales et initialisation nécessaire ; aucun personnage ni raffinement des bâtiments. L'Afrique australe est la passe suivante, non commencée ici. Courbes et finition cosmétique reportées par le joueur.

## Territoires installés

**369 RGB natifs réattribués en 40 groupes, 11 régions moteur** : {states}. Aucun nouveau RGB, pixel recoloré, terrain, ressource ou locator modifié. Liste exhaustive dans [PLAN.json](PLAN.json), coordonnées dans [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json), cartes [avant](BEFORE.png) / [après](AFTER.png). Les coordonnées servent à retrouver des cellules, pas à certifier un cadastre de 1776.

- **Lunda, Luba, Kazembe, Kuba** : noyau Luba recentré sur Upemba/Lualaba ; Kazembe sur Luapula/Mweru, distinct des communautés du cuivre et Hemba. La capitale régionale LND passe d'EAST_ANGOLA à KATANGA, autour de Mussumba/Kapanga. Le **Kanyok** a un noyau autonome et doit un tribut au Luba ; le **Kazembe** reste autonome, tributaire du Lunda. Les liens natifs traduisent une suzeraineté souple, sans certifier le taux d'un tribut historique. Le noyau Bushong/Kuba est distingué des communautés du Kasaï/Sankuru et Luba du Kasaï ; le Maniema n'est pas annexé par anticipation aux expansions luba ultérieures.
- **Zambèze et Malawi** : réduction des grandes enveloppes Barotse/Bemba/Maravi. Le noyau de la plaine Luyana est conservé, les communautés des plateaux et Luvale/Lwena sont séparées. Le Bemba garde un noyau ancien ; Lungu/Mambwe, Bisa, Tumbuka et Ngonde sont distingués, sans reproduire ses conquêtes du XIXe siècle. Le nom Maravi devient **Kalonga** pour sa cour résiduelle ; **Undi et Lundu**, ainsi que les communautés chewa, yao, makua, lomwe et sena, ne sont plus administrés comme une seule province maravi. L'enveloppe Maseko/Ngoni anachronique disparaît de ce secteur.
- **Grands Lacs** : Busoga séparé du Buganda comme ensemble de principautés, sans monarchie unitaire de Kyabazinga. Noyaux **Gisaka, Bugesera, Buha du Nord, Buha du Sud, Kiziba, Kyamutwara/Ihangiro** distingués. Ce dernier reste un agrégat de deux pouvoirs à la résolution disponible. Kigali reste rwandais. Buddu et les chronologies royales contradictoires ne servent pas de prétexte à inventer une nouvelle frontière.
- **Mozambique** : les enclaves et arrière-pays commerciaux sont distingués des royaumes africains. Ibo/Quirimbas, Mozambique/Mossuril, Quelimane, Sena/Tete et Sofala sont préservés ; Zumbo reçoit un raccord de trois cellules au corridor portugais existant. **Inhambane passe au Portugal** sur une cellule côtière attestant le poste antérieur à 1776 ; la province reste beaucoup plus vaste que le comptoir. **Delagoa/Maputo passe aux autorités du Tembe**, avant l'installation autrichienne de 1777 et le dispositif portugais de 1781–1782. Uteve est distingué de la possession portugaise de Sofala. La présence commerciale européenne antérieure n'est pas niée ; elle n'est pas assimilée à l'administration directe de toute la baie.

Tous les noyaux centralisés examinés sont contigus et ont un voisin centralisé ; aucune nouvelle enclave centralisée entourée uniquement de pays décentralisés. Les agrégats de communautés peuvent avoir plusieurs composants, explicités dans GEOMETRY_CHECK.json ; le Portugal garde ses établissements maritimes séparés. Les corridors de Zumbo et les contours royaux sur cellules entières sont des approximations politiques, non une preuve de contrôle de chaque village.

## Institutions et technologies

**23 nouveaux TAG et 5 TAG natifs activés**, soit **28 profils explicites contrôlés** ; neuf profils existants conservés. Aucun dirigeant ajouté. Deux pactes tributaires seulement : LND → KZM et LBA → KNY. La royauté luyana est historiquement attestée, mais **LZO conserve sa catégorie décentralisée native** dans ce lot cartographique : elle n'est pas transformée en enclave centralisée et aucun corridor arbitraire vers le Portugal n'est créé. C'est une limite du modèle politique, pas une négation de son histoire.

| TAG | Nom ajouté ou TAG natif | Catégorie moteur | Technologies connues | Capitale régionale |
|---|---|---|---:|---|
{countries}

Les justifications individuelles figurent dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json). Capacités rurales, artisanales, commerciales, militaires et minières sont distinguées. Les communautés du cuivre reçoivent uniquement la capacité minière préindustrielle nécessaire au modèle local ; aucun moteur ni industrie moderne. Les bâtiments nommés building_railway utilisent ici le PM de **réseau routier traditionnel**, avec réseau ferré et trains de voyageurs désactivés.

Les neuf anciens profils gardent toutes leurs connaissances. Deux seuls ajouts ciblés : **international_relations à BMB et MNC**, avant l'activation des lois, pour leurs contacts politiques/commerciaux documentés et la loi privée de coutumes commerciales. Cette loi reprend les effets du mercantilisme sans distribuer l'assurance commerciale. **Aucun graphe TECH, recette ou PM commun modifié.** Les dettes déjà présentes (dont certains centres de commerce et lois demandées) restent énumérées dans TECH_NON_REGRESSION.json ; elles ne sont pas certifiées fonctionnelles par ce lot. Le contrôle HMB supplémentaire porte sur les données reçues et sa version actuelle, sans fabriquer un audit antérieur.

La première exécution a révélé une culture inexistante, une mauvaise région capitale CHW et deux prérequis de loi. Correction conservée dans [COMPATIBILITY_REPAIR.json](COMPATIBILITY_REPAIR.json), anciens résultats dans RUN01_*.json. **tonga** sert de proxy moteur large aux cultures nationales TCH/TMP ; ce n'est pas une reconstruction de l'identité tsonga/chopi/tembe et aucune culture de POP n'a été changée. CHW a sa capitale en ZAMBEZIA, qu'il possède effectivement.

## Population et conservation

Population mondiale : **{pop['world_before']:,} → {pop['world_after']:,}**, delta **{pop['delta']}**. Les onze totaux régionaux et chaque ventilation culturelle, religieuse et servile sont conservés. Répartition technique de chaque cohorte par nombre de provinces natives uniques de sa portion, avec arrondis entiers conservatifs : **ce ne sont pas des recensements historiques**. Les valeurs nationales ci-dessous ont le même périmètre global avant/après ; elles ne mesurent pas les seuls comptoirs ou capitales.

| TAG touché ou profil revu | Avant | Après |
|---|---:|---:|
{pops}

Détails : [POPULATION_LEDGER.json](POPULATION_LEDGER.json), [CSV](POPULATION_BEFORE_AFTER.csv). Aucun habitant créé, supprimé, converti ou transféré entre catégories culturelles/religieuses. Niveaux bâtis et sélections explicites de PM, types et effectifs militaires conservés ; la propriété des portions territoriales est seule ventilée.

## Contrôles, concurrence et limites

- **{v['passed']}/{v['total']} contrôles statiques** dans VALIDATION.json : attribution exacte, unicité, capitales, cultures référencées, continuité des noyaux, cohortes, niveaux/PM et conservation hors blocs autorisés.
- **28 profils nouveaux/activés PASS_STATIC_ONLY** ; 24 témoins existants comparés, aucun nouveau P0/P1. Les deux grants ciblés sont les seules différences de connaissances autorisées. HMB est vérifié en complément comme receveur.
- **12 fichiers existants ciblés et 35 ajouts fonctionnels**. Hashes d'entrée immédiate, réparation et version finale conservés séparément. Anciennes installations WORLD, interfaces Congo-01/Corne, SERG, TECH/ECON et travaux américains préservés ; aucune écriture Git, vanilla ou suivi SERG, aucun retour à une ancienne baseline.
- Carte native irrégulière, agrégats pluriels, subdivisions de la baie de Maputo, empreinte exacte des prazos et datation de certaines expansions restent approximatifs. Les noms et points de hubs natifs ne sont pas tous révisés : en particulier le locator Inhambane et sa correspondance de cellule doivent être observés en jeu. Pas de certification cadastrale, démographique, budgétaire ou de contrôle provincial uniforme.
- Chargement, drapeaux, capitales affichées, lois effectivement actives, marchés, approvisionnement, fronts et sauvegarde/rechargement : **NOT_RUN**, à intégrer au **test africain groupé**. Aucun test intermédiaire demandé et aucun reçu humain ajouté. Le journal de preuves final est DELIVERY_VALIDATION.json ; empreintes dans DELIVERY_MANIFEST.json.

WORLD reste **10/320 (3,13 %)** : aucun critère entier nouveau pour cette restauration partielle. **Prochaine passe : Afrique australe et établissements néerlandais/VOC**, depuis la version courante. Rozvi/Zimbabwe, Botswana/Tswana, interfaces du sud et chronologies du Cap restent à examiner ; ils ne sont pas déclarés déjà restaurés.
''')
    doc('SOURCES.md','''# Sources et niveau de lecture — INTERIOR-01

Consultation le 28 octobre 2026 ; référence territoriale 1er janvier 1776. Les chapitres universitaires ci-dessous sont téléchargés et extraits dans sources/. Seuls les passages indiqués ont été lus ; aucun volume complet n'est déclaré lu. Les cartes ont des dates et des résolutions différentes : leur correspondance aux RGB est une interprétation explicite dans PLAN.json.

1. **Ndaywel è Nziem**, « Le système politique luba et lunda : émergence et expansion », *Histoire générale de l'Afrique*, V, ch.20, p.643–663. [PDF](https://bokundoli.org/wp-content/uploads/2021/12/T5-22.pdf), UNESCO_LUBA_LUNDA.pdf/.txt. P.649 et 655–660 lues : Kanyok, expansion luba, organisation impériale et autonomie du Kazembe. Cartes **20.3 p.649, PDF7** et **20.7 p.655, PDF13** rendues et examinées (MAP_LUBA.png, MAP_LUNDA.png). La première inclut des évolutions du XIXe siècle ; la seconde des limites de 1790. Elles localisent les noyaux et les liens, sans fournir le cadastre de 1776. Aucune expansion tardive entière n'est copiée.

2. **K.M.Phiri, O.J.M.Kalinga, H.H.K.Bhila**, « La zone au nord du Zambèze », même ouvrage, ch.21 p.665–696. [PDF](https://bokundoli.org/wp-content/uploads/2021/12/T5-23.pdf), UNESCO_NORTH_ZAMBEZIA.pdf/.txt. Passages p.681–687 et 691–693 lus : Ngonde et Kyungu Kasyombe vers1750, décomposition maravi, autonomie makua/lolo, circulation bisa/yao. P.691 évoque la réputation bisa dès1775 ; les campagnes bemba1820–1840 ne sont pas projetées en1776. Une carte a été rendue dans MAP_NORTH_ZAM.png mais n'est pas revendiquée comme carte visuellement examinée.

3. **J.B.Webster, B.A.Ogot, J.P.Chrétien**, « La région des Grands Lacs de1500 à1800 », ch.26 p.843–896. [PDF](https://bokundoli.org/wp-content/uploads/2021/12/T5-28.pdf), UNESCO_GREAT_LAKES.pdf/.txt. P.855/862 : pluralité du Busoga ; p.869–870 et 886–890 : royaumes riverains, Gisaka, Bugesera et deux dynasties buha. Carte **26.2 p.872, PDF30**, fin XVIIe siècle et regroupements régionaux1700–1850, rendue/examinée dans MAP_LAKES_17C.png. C'est un cadre de localisation, pas une frontière1776 exacte. Les conflits de chronologie sur Jjunju/Buddu sont laissés ouverts ; pas de nouvelle conquête datée arbitrairement.

4. **H.H.K.Bhila**, « La région au sud du Zambèze », ch.22 p.697–741. [PDF](https://bokundoli.org/wp-content/uploads/2021/12/T5-24.pdf), UNESCO_SOUTH_ZAMBEZI.pdf/.txt. P.708–718 lues : prazos, Zumbo1710, Manica/Manyika, Uteve et rapports aux pouvoirs intérieurs. Carte **22.7 p.712, PDF16** des prazos, rendue/examinée dans MAP_PRAZOS.png ; modèle régional sans cadastration de janvier1776. Carte22.8 p.715 des Rozvi examinée comme contexte : aucune restauration rozvi dans ce lot. P.722–726 lues pour les capacités rurales/artisanales, sans rééquilibrage des bâtiments.

5. **Olga Iglésias**, « Reorganização do espaço na Colónia de Moçambique. Estudo do fenómeno urbano », *Africana Studia*9(2006), p.299–333. [Article](https://ojs.letras.up.pt/index.php/AfricanaStudia/article/download/7283/6672/23961), DELAGOA_URBANISM.pdf/.txt. Table **Delagoa p.316/PDF18**, regimento25.11.1781 et installation1782, et table **Inhambane p.320/PDF22**, installation1727–1730/carta9.5.1761, rendues et examinées dans MAP_DELAGOA_TABLE.png/MAP_INHAMBANE_TABLE.png. La mention d'une reconquête1730 à Delagoa témoigne de présences/prétentions antérieures ; elle ne prouve pas une administration portugaise permanente de toute la baie en1776. Les dates urbaines ne justifient pas les populations de provinces entières.

6. **Andrew Roberts**, « Chronology of the Bemba (N.E.Zambia) », *Journal of African History*11(2),1970 p.221–240. [Résumé universitaire consulté](https://library.au.int/chronology-bemba-ne-zambia-8) : Chitimukulu probablement XVIIe siècle, antérieur à Kazembe ; limites des généalogies avant la fin du XVIIIe siècle. Résumé seulement, article complet non revendiqué. **Mutumba Mainga**, *A History of the Lozi People to1900*, thèse1968, [notice/résumé SOAS](https://soas-repository.worktribe.com/output/390296/a-history-of-the-lozi-people-to-1900), monarchie probablement milieuXVIIe siècle. **Hogan**, thèse2015, [PDF Kent](https://kar.kent.ac.uk/48707/1/156Hogan%20-%20The%20ends%20of%20Slavery%20in%20Barotseland%2C%20Western%20Zambia%20%28c.1800-1925%29.pdf) : exemplaire LOZI_HOGAN.pdf téléchargé ; introduction du ch.5, PDF77/p.65, consultée sur le noyau de vallée et les récits de l'expansion. Pas de limites1776 certifiées par ces résumés ou cette introduction.

7. **Mandla Mathebula**, « Some notes on the early history of the Tembe,1280AD–1800AD », *New Contree*78(2017) p.42–57. [Notice universitaire](https://repository.nwu.ac.za/items/ceda749a-06d5-43db-84c2-dd6de0480341) : résumé lu, apogée de la puissance tembe à la fin du XVIIIe siècle au sud de Maputo. Article intégral non revendiqué. Le petit noyau est un choix politique à la résolution native ; les subdivisions Mpfumo/Maputo ne sont pas résolues.

8. Contrôles complémentaires effectivement consultés au niveau de notices/passages indexés : [HPIP Inhambane](https://hpip.org/en/Contents/Place/324) (carta1761, reconnaissance1763 et vila1764) ; [Ibo, recherche patrimoniale](https://www.ibo-rotadocafe.org/pt/a-ilha-do-ibo/historia/historia-ibo/) (fort1754, vila1761, capitale1764) ; [Alpers2021, JAMH5](https://brill.com/view/journals/jamh/5/1/article-p1_1.pdf), passage indexé p.8 sur l'indépendance makua après la désagrégation maravi (PDF403, pas de lecture intégrale) ; [Hedges, thèse](https://emandulo.apc.uct.ac.za/collection/FHYA%20Depot/Theses%20and%20Dissertations/Hedges_Thesis.pdf), passage indexé p.109 sur le commerce saisonnier (non téléchargée) ; [article universitaire2024](https://www.tandfonline.com/doi/full/10.1080/03057070.2024.2436329), passage indexé sur Inhambane1729 et Delagoa1799, non lu intégralement. Les dates d'un poste, d'un fort et d'un établissement permanent ne sont pas confondues. L'article ISCTE/Cadernos30 sur les municipalités n'a pas pu être téléchargé : simple corroboration indexée, pas preuve intégrale.

9. [Chronologie de la maison royale du Buganda](https://buganda.or.ug/wp-content/uploads/2025/04/Final-Print-BRIEF-HISTORY-OF-THE-KINGDOM-OF-BUGANDA-3.pdf), passage indexé p.16 : Junju1780–1797 ; divergence avec les dates du chapitre UNESCO. Aucun arbitrage définitif ni transfert de Buddu installé. **W.R.Ochieng'**, ch.27 p.897–920, [PDF](https://bokundoli.org/wp-content/uploads/2021/12/T5-29.pdf) conservé dans UNESCO_EAST_INTERIOR.pdf/.txt, passages contextuels sur échanges et communautés : aucune réécriture Kenya/Rift/Zanzibar depuis une carte ethnique.

Les dossiers MAP1/R7 et leurs inventaires ont servi de pistes, jamais de preuve des propriétaires courants. Les entrées réelles sont BASELINE.json, APPLY_BEFORE.json et apply_inputs/. L'absence de précision cadastrale, de chronologie royale ou de données ethniques fiables reste une incertitude, pas une frontière ni un habitant inventé. Les cultures moteur servent parfois de proxys ; les POP natifs ne sont pas convertis.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# Contrôle africain groupé — INTERIOR-01

NOT_RUN. Aucun reçu humain ni demande de test intermédiaire.

Nouvelle partie1776 : vérifier noyaux Lunda/Luba/Kazembe/Kuba, Kanyok et les deux liens tributaires ; distinction des agrégats locaux et du noyau Luyana, maintien des ports du Congo-01. Vérifier Grands Lacs (Kigali conservé, Busoga distinct, Gisaka/Bugesera/Buha/Kiziba/Kyamutwara), Malawi et disparition de Maseko dans le secteur, puis Makua/Lomwe/Yao/Sena, Angoche, Uteve/Tembe, Inhambane et raccord de Zumbo. Examiner le locator natif Inhambane, les noms de hubs et les capitales ; le rapport ne certifie pas leurs déplacements visuels.

Contrôler lois réellement actives, profils technologiques visibles, ressources accessibles, construction/recrutement, niveaux/PM et effectifs hérités. Observer marchés, budgets, ravitaillement et fronts pendant la simulation groupée, sauvegarder puis recharger. Conserver des témoins Congo-01, Corne/Nil/Sahel/Maghreb/Balkans et Amériques/SERG. Noter version, durée et observations effectivement effectuées ; aucune durée ou réussite n'est préremplie. Finition des courbes différée par le joueur.
''')
    doc('REPRODUCE.md','''# Reproduction en lecture seule

Depuis le dépôt avec Python configuré :

`python tools/world1776_interior01.py --tech --validate`

`python tools/world1776_interior01_closeout.py --final`

Ne pas relancer --apply, --tracking ni le survey initial. Les entrées et reçus archivés ne sont pas une baseline à réinstaller. Un changement concurrent doit être rapproché de sa preuve, jamais annulé pour satisfaire un test. --evidence régénère uniquement cartes, correspondances et bilans dans le dossier du lot ; --reports écrit ses rapports. Ces commandes ne lancent pas le moteur. Les reçus historiques des autres lots restent des preuves de leur version passée.
''')
    doc('USER_REQUEST.txt','''Demande directe de la mission :
« OK. Tu peux passer à l'interface intérieure avec les tribus des Grands Lacs et le Mozambique. On passera ensuite l'Afrique australe. »

Périmètre interprété depuis la suite Congo-01 : Congo intérieur/Luba-Lunda-Kuba-Kazembe, interfaces Zambèze et Grands Lacs, Mozambique. Référence1janvier1776. Afrique australe pour la prochaine passe, pas lancée ici. Frontières et initialisation nécessaire, pas de personnages ni raffinement de bâtiments ; courbes différées. Pays vassaux et degrés d'autonomie autorisés si justifiés. Aucune nouvelle enclave centralisée entourée de pays décentralisés ; pas de corridor historique inventé. Tests africains groupés sans demande intermédiaire. Git/vanilla/suiviSERG non écrits ; travaux TECH/ECON et Amériques protégés. Aucune nouvelle validation humaine déduite de cette autorisation.
''')

def tracking():
    assert not (LOT/'TRACKING_PATCHES.json').exists(),'Tracking already updated.'
    hashes={n:h.b.a.sha(WORLD/n) for n in TRACK}
    for n in TRACK:
        dest=LOT/'tracking_inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORLD/n,dest)
    data=read(WORLD/'ROADMAP_STATE.json');assert not any(r['id']=='INTERIOR-01' for r in data['lots'])
    for phase in data['phases']:
        for region in phase['subregions']:
            if region['id'] not in ['P3-05','P3-06','P3-07']:continue
            for key,c in region['criteria'].items():
                if c['status'] in ['STATIC_VERIFIED','USER_VALIDATED']:continue
                if key!='V':c['status']='PARTIAL'
                c.setdefault('additional_evidence',[]).append('INTERIOR-01/REPORT.md' if key!='V' else 'INTERIOR-01/GROUPED_RUNTIME_ITEMS.md')
                c['INTERIOR-01_limit']='Noyaux politiques installés sur cellules natives ; frontières fines, démographie historique, institutions détaillées et moteur non certifiés. Pas de point entier.'
                if region['id']=='P3-05' and key!='V':c['remaining']='Congo-01 et INTERIOR-01 installés ; cadastre provincial, sobados, données historiques fines et moteur non clos. Aucun point entier.'
        count=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values())
        phase['progress'].update(technical_verified=count,technical_percent=float((Decimal(count)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
    total=sum(p['progress']['technical_verified'] for p in data['phases']);assert total==10 and data['progress']['criteria_total']==320
    data['progress'].update(technical_verified=total,technical_percent=3.13)
    data['lots'].append(dict(id='INTERIOR-01',date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',existing_files_modified=12,new_files=35,new_tags=23,activated_existing_tags=['MKU','LMW','UYA','SNA','CHW'],new_or_activated_profiles=28,preserved_existing_profiles=9,native_RGBs_transferred=369,transfer_groups=40,new_RGBs=0,pixels_recolored=0,world_population_delta=0,receipt='INTERIOR-01/FILES_DELIVERED.json',credited_criteria=[],runtime='NOT_RUN'))
    data['steering_history'].append(data['current_steering']);data['current_steering']=dict(date='2026-10-28',authority='INTERIOR-01/USER_REQUEST.txt',scope='Interior interfaces, Great Lakes and Mozambique installed; southern Africa follows in a separate pass',last_lot='INTERIOR-01',next_pass='Southern Africa, Rozvi/Zimbabwe and southern interfaces, Dutch/VOC settlements',cosmetic_smoothing_deferred=True,autonomous_subjects_authorized=True,intermediate_player_tests_requested=False,runtime_validation_timing='GROUPED_AFRICA',full_V_credit=False)
    entry='''\n\n## INTERIOR-01 — 28 octobre2026\n\nCongo intérieur, Grands Lacs et Mozambique : 369 RGB natifs/40 groupes/11 régions, aucun nouveau pixel/RGB. Noyaux Luba/Lunda/Kazembe/Kuba, communautés autonomes des plateaux/Malawi et Grands Lacs distingués ; Kazembe tributaire du Lunda, Kanyok du Luba. 23 TAG nouveaux et5 activés,28 profils explicites ; neuf connaissances anciennes conservées avec deux seuls grants diplomatiques ciblés BMB/MNC. Inhambane portugais, Delagoa/Maputo rendu au Tembe, raccord natif de Zumbo ; limites locales des prazos non certifiées. Luyana reste de catégorie décentralisée, royauté historique reconnue dans les limites du modèle. 12 fichiers ciblés+35 ajouts,631 contrôles statiques réussis, populations/cohortes/niveaux/PM/armées conservés, delta mondial0. Sources, incertitudes et reçus INTERIOR-01/REPORT.md ; première exécution et correction archivées. Aucun test moteur ou humain nouveau, aucun point entier : WORLD10/320(3,13%). Afrique australe pour la passe suivante ; finition des courbes différée.\n'''
    assert all(h.b.a.sha(WORLD/n)==v for n,v in hashes.items())
    write(WORLD/'ROADMAP_STATE.json',data)
    for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
    h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## INTERIOR-01 — limites ouvertes,28octobre2026\n\nContours natifs, corridors et agrégats pluriels non cadastraux ; chronologies Buddu/Jjunju contradictoires, subdivisions Maputo/Tembe ouvertes. Noyau luyana conservé avec catégorie moteur décentralisée pour éviter une nouvelle enclave ; cultures nationales parfois proxys, POP inchangés. Exacte empreinte des prazos et uniformité du contrôle portugais non certifiées. Locator Inhambane/hubs/capitales/drapeaux, lois effectives, marchés, budgets, fronts et sauvegarde à vérifier au test africain groupé. Anciennes dettes techniques explicites des témoins maintenues, pas de grant industriel pour les masquer. P3-05/06/07 restent partiels ; Afrique australe non traitée par ce lot. Aucun point ou reçu humain nouveau.\n''')
    h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## INTERIOR-01 — périmètre installé,28octobre2026\n\nOnze nœuds d'états EAST_ANGOLA/KASAI/KATANGA/KAZEMBE/ZAMBIA/CONGO_ORIENTALE/UGANDA/TANGANYIKA/MOCAMBIQUE/ZAMBEZIA/LOURENCO_MARQUES, portions POP/bâtiments SCOPES.json. Huit nœuds d'histoire nationale existants ciblés, BMB natif surchargé dans son propre fichier, 23nouveaux TAG et5profils natifs activés, définitions/effets/loi propres,2pactes tributaires et FR/EN. Liste exhaustive PLAN.json ; entrées immédiates apply_inputs/, réparation séparée COMPATIBILITY_REPAIR.json, version finale FILES_DELIVERED.json. Aucun pixel, terrain, ressource, locator, personnage, recette commune, graphe TECH, militaire ou suiviSERG écrit. Kenya/Rift/Zanzibar et noyaux côtiers Congo-01 conservés. Les cellules Maseko et la portion TSW du Mozambique seulement sont concernées ; Botswana/Zimbabwe/Rozvi/sud restent à la passe australe. Travaux américains et autres portions partagées conservés.\n''')
    h.save(WORLD/'NEXT_ACTION.md','''# Prochaine action — après INTERIOR-01\n\nLot Congo intérieur–Grands Lacs–Mozambique installé. Lire INTERIOR-01/REPORT.md, SOURCES.md, PLAN.json, GEOGRAPHIC_CROSSWALK.json, VALIDATION.json, TECH_NON_REGRESSION.json, DELIVERY_VALIDATION.json et FILES_DELIVERED.json. Les noyaux/corridors utilisent des cellules natives ; ni cadastre1776, ni catégorie politique parfaite, ni économie observée ne sont certifiés.\n\nSuite demandée par le joueur : Afrique australe et établissements néerlandais/VOC, dans une nouvelle passe depuis l'état courant. Examiner notamment Rozvi/Zimbabwe, Botswana/Tswana, interfaces du sud, royaumes locaux et chronologie1776 des établissements du Cap. Ne pas confondre une prétention coloniale avec le contrôle de tout l'intérieur ; pas de frontière ou de corridor arbitraire. Aucun autre secteur n'est lancé automatiquement.\n\nFrontières et initialisation nécessaire uniquement. Préserver INTERIOR-01, Congo-01, Sahel/Nil/Corne/Maghreb/Balkans, SERG, TECH/ECON et les Amériques ; pas de retour à une ancienne baseline. Courbes et tests africains groupés différés, aucune demande de test intermédiaire. Aucun reçu humain nouveau ; WORLD10/320(3,13%), aucun critère entier nouveau pour cette passe partielle.\n''')
    concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['INTERIOR-01']=dict(receipt='INTERIOR-01/CONCURRENT_CHANGES.json',existing_functional_files_modified=12,new_files=35,native_RGBs_transferred=369,pixels_recolored=0,new_RGBs=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False);write(WORLD/'CONCURRENT_CHANGES.json',concurrent)
    h.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=h.b.a.sha(WORLD/n)) for n in TRACK])

def final():
    rows=delivered();checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    for rel,r in rows.items():ck('delivered_hash.'+rel,h.b.a.sha(ROOT/rel)==r['after'])
    h.dump('FILES_DELIVERED.json',list(rows.values()));ck('47_functional_files',len(rows)==47)
    ck('territorial_static_pass',h.load('VALIDATION.json')['status']=='PASS')
    for r in h.load('STARTING_TECH_NEW_COUNTRIES.json'):ck('profile.'+r['TAG'],r['status']=='PASS_STATIC_ONLY')
    for r in h.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:ck('no_new_P0_P1.'+r['TAG'],not r['introduced'])
    base={r['TAG']:r for r in h.load('STARTING_TECH_BEFORE.json')}
    for r in h.load('STARTING_TECH_EXISTING_AFTER.json'):
        wanted=set(base[r['TAG']]['technologies'])|set(h.p.COUNTRIES.get(r['TAG'],{}).get('targeted_grants',[]))
        ck('knowledge_preserved_with_only_documented_grant.'+r['TAG'],set(r['technologies'])==wanted)
    for t in ['BMB','MNC']:
        body=h.country_body(t);ck('technology_before_law_activation.'+t,body.index('add_technology_researched = international_relations')<body.index('effect_aor1776_interior01_politics'))
    ck('Hemba_receiver_no_asset_gate',not h.load('ADDITIONAL_RECEIVER_TECH_CHECK.json')['newly_installed_asset_gate_findings'])
    pop=h.load('POPULATION_LEDGER.json');ck('population_world',pop['delta']==0)
    for r in pop['state_totals']:ck('population_region.'+r['state'],r['before']==r['after'])
    ck('all_profiles_populated',all(any(r['TAG']==t and r['after']>0 for r in pop['countries']) for t in h.p.COUNTRIES))
    colors=[c for r in h.load('PLAN.json') for c in r['RGBs']];ck('369_unique_transfers',len(colors)==len(set(colors))==369)
    language=[];sets={}
    for lang in ['french','english']:
        allkeys=loc.entries(lang,replacement=True);own={k:v for k,v in allkeys.items() if any(path.name==h.PREFIX+'_l_'+lang+'.yml' for path,n,t in v)};sets[lang]=set(own)
        language.extend(dict(check=lang+'.'+k,passed=len(v)==1) for k,v in own.items())
    language.append(dict(check='same_bilingual_keys',passed=sets['french']==sets['english']))
    h.dump('LOCALIZATION_CHECK.json',dict(status='PASS' if all(r['passed'] for r in language) else 'FAIL',checks=language,render_runtime='NOT_RUN'));ck('localization',all(r['passed'] for r in language))
    certified={}
    outside=[r for r,v in h.load('APPLY_BEFORE.json')['protected'].items() if r not in rows and h.b.a.sha(ROOT/r)!=v and h.b.a.sha(ROOT/r)!=certified.get(r)]
    ck('outside_files_preserved_or_sourced_external',not outside,outside)
    data=read(WORLD/'ROADMAP_STATE.json');technical=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED'];human=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
    ck('canonical_progress',len(technical)==10 and not human and data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320)
    h.dump('PROGRESS_CALCULATION.json',dict(credited=technical,user_validated=human,numerator=10,denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
    needed=['REPORT.md','SOURCES.md','PLAN.json','GEOGRAPHIC_CROSSWALK.json','POPULATION_LEDGER.json','POPULATION_BEFORE_AFTER.csv','COUNTRY_PROFILES.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','TECH_NON_REGRESSION.json','VALIDATION.json','CONCURRENT_CHANGES.json','LOCALIZATION_CHECK.json','BEFORE.png','AFTER.png','GROUPED_RUNTIME_ITEMS.md','FILES_DELIVERED.json','COMPATIBILITY_REPAIR.json','TRACKING_PATCHES.json','PROGRESS_CALCULATION.json','USER_REQUEST.txt','REPRODUCE.md','ADDITIONAL_RECEIVER_TECH_CHECK.json']
    for n in needed:ck('evidence.'+n,(LOT/n).is_file())
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False);h.dump('DELIVERY_VALIDATION.json',result)
    files=[ROOT/r for r in rows]+[LOT/n for n in needed]+[LOT/'DELIVERY_VALIDATION.json']+[WORLD/n for n in TRACK]+[ROOT/'tools'/('world1776_interior01'+s+'.py') for s in ['', '_plan','_inspect','_closeout']]+[p for p in (LOT/'sources').iterdir() if p.is_file()]
    h.dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():h.b.a.sha(p) for p in files})
    print('Delivery',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']]);return result['status']=='PASS'

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for k in ['evidence','reports','tracking','final']:parser.add_argument('--'+k,action='store_true')
    args=parser.parse_args()
    if args.evidence:evidence()
    if args.reports:reports()
    if args.tracking:tracking()
    if args.final:raise SystemExit(0 if final() else 1)
