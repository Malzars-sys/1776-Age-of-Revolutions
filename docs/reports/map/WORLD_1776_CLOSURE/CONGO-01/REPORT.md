# CONGO-01 — Bas Congo, Kongo et Angola occidental

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
| LNG | unrecognized | 6 | CONGO |
| TKE | unrecognized | 5 | CONGO |
| YKA | unrecognized | 7 | BAS_CONGO |
| KSN | unrecognized | 7 | EAST_ANGOLA |
| SYO | unrecognized | 7 | BAS_CONGO |
| KKG | unrecognized | 6 | CONGO |
| NGY | unrecognized | 6 | CONGO |
| MTM | unrecognized | 7 | EAST_ANGOLA |
| MBL | unrecognized | 7 | SOUTH_ANGOLA |
| BIE | unrecognized | 7 | EAST_ANGOLA |
| DMB | decentralized | 4 | NORTH_ANGOLA |
| KIS | decentralized | 4 | EAST_ANGOLA |
| MYU | decentralized | 5 | GABON |

Les profils sont expliqués individuellement dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json). Une loi locale de coutumes commerciales réutilise les effets du mercantilisme et le prérequis de relations internationales. Elle évite de distribuer l'assurance pour justifier les marchés locaux. Les usages ruraux, artisanaux, commerciaux et militaires sont distingués ; aucune modification du graphe TECH, des recettes ou des PM communs.

Le premier contrôle technique a identifié cinq dépendances agricoles manquantes. Elles ont été fermées par la capacité d'élevage de petit bétail documentée par Proyart, 1776, p. 32 ; le rapprochement avec le Tio intérieur demeure une inférence régionale explicitée. [COMPATIBILITY_AND_LABEL_REPAIR.json](COMPATIBILITY_AND_LABEL_REPAIR.json) conserve les entrées immédiates et la correction. Les anciens résultats restent dans RUN01_*.json. Ce choix n'atteste pas un secteur bovin développé.

## Population et données conservées

Monde : **837,328,539 → 837,328,539**, delta **0**. Chaque cohorte conserve ses attributs culturels, religieux et serviles ; répartition technique par provinces natives uniques, arrondis entiers conservatifs. Ce ne sont pas des recensements historiques. Les six totaux régionaux restent identiques ; détails : [POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv).

| Pays/agrégat touché | Avant | Après |
|---|---:|---:|
| BIE | 0 | 13 048 |
| CHK | 195 708 | 173 962 |
| DMB | 0 | 51 632 |
| KIS | 0 | 61 739 |
| KKG | 0 | 7 099 |
| KON | 937 936 | 728 661 |
| KSN | 154 344 | 29 277 |
| LNG | 214 696 | 49 698 |
| MBL | 0 | 34 149 |
| MTM | 0 | 34 676 |
| MYU | 0 | 154 348 |
| NGY | 0 | 34 571 |
| OVM | 203 036 | 223 521 |
| POR | 5 122 927 | 5 142 983 |
| SYO | 0 | 108 525 |
| YKA | 327 120 | 307 878 |

Tous les niveaux bâtis, sélections de PM, types et effectifs militaires sont conservés. Seule la propriété des portions partagées est répartie. Aucun raffinement de bâtiment ni recette de flavor. Les cultures bakongo/ovimbundu héritées servent parfois de proxys, notamment pour les Mbundu ; aucune conversion des habitants n'est effectuée.

## Contrôles et concurrence

- [VALIDATION.json](VALIDATION.json) : **189/189 contrôles statiques**. Attribution exacte, absence de nouveau doublon, capitales, continuité des nouveaux noyaux centralisés, cohortes et données hors blocs possédés.
- **13 profils** : PASS_STATIC_ONLY. Dix pays témoins existants : aucune nouvelle incompatibilité P0/P1. Les dettes héritées de KON et autres témoins ne sont pas effacées par une distribution de technologies.
- 8 fichiers existants ciblés et 14 ajouts fonctionnels. Les anciens lots WORLD, SERG, TECH/ECON et les Amériques sont préservés. Deux changements concurrents de libellés Sacramento correspondent au manifeste américain courant ; [EXTERNAL_COMPOSITION_REVIEW.json](EXTERNAL_COMPOSITION_REVIEW.json). Aucun retour à une baseline, Git/vanilla/SERG non écrits.
- Contrôle documentaire final : [DELIVERY_VALIDATION.json](DELIVERY_VALIDATION.json), empreintes : [DELIVERY_MANIFEST.json](DELIVERY_MANIFEST.json).

## Limites et suite

Les noyaux et corridors utilisent des cellules entières, pas un cadastre 1776. Noms de hubs natifs, drapeaux, budgets, chargement, lois effectivement actives, recrutement, fronts, ravitaillement et sauvegarde/rechargement restent à voir au **test africain groupé**. Aucun test intermédiaire demandé, aucune validation humaine créée. Les composants portugais maritimes hérités ne sont pas assimilés à des enclaves terrestres nouvelles ; OVM reste un agrégat plural, partiellement séparé par les nouveaux royaumes et corridors.

Cette passe ne clôt ni tout le bassin congolais ni P3-05 : domaines Luba/Lunda/Kuba/Kazembe, interfaces du Congo intérieur, répartition fine des principautés du Kongo et certains sobados restent à examiner. WORLD demeure **10/320 (3,13 %)**, aucun critère entier nouveau. Suite autorisée : interfaces intérieures vers le Zambèze, autres possessions portugaises/Mozambique, puis Afrique australe et établissements néerlandais/VOC. Aucun lissage cosmétique lancé.
