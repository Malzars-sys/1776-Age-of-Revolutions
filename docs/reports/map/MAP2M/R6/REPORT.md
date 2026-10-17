# MAP-2M-R6 — Deux pilotes locaux, sans transfert arbitraire

Date cible : **1er janvier 1776**. Résultat : **MAP-2M-R6_PARTIAL**.

R6 apporte un correctif réel à la lecture hydrographique, un nouveau contrôle final non utilisé pour ajuster le modèle, des lectures locales de limites anciennes et une analyse de résolution. **La chaîne permettant un transfert politique fiable n'est toutefois démontrée sur aucun des deux pilotes. Aucun fichier fonctionnel n'est modifié.** R7 n'est pas lancé automatiquement.

## Résultats distincts

| Pilote | Résultat concret | Limite déterminante | Installation |
| --- | --- | --- | --- |
| A : ouest de Wolgast–Peenestrom | Lecture de la rive continentale sur Mayer ; sections de l'eau LUNG mesurées ; absence d'homologue natif du détroit documentée | Pas de nouveau calage source→réel local accepté, ni de contrôle natif des deux rives | 0 cellule ; 18 anciennes B restent B |
| B : Bromberg–Fordon | Vistule correctement extraite ; coude physique contrôlé ; liseré fluvial et texte de propriété distingués du candidat politique méridional | Tracé souverain daté et conversion source→réel non acceptés ; un seul coude schématique ne certifie pas toutes les cellules | 0 cellule ; 18 anciennes candidates directement adjacentes au noyau restent C |

Les 149 candidates supplémentaires de R5 ne sont pas importées. Les autres districts de la Netze ne sont pas repris. Cinq des 36 centres de cellules examinés sont hors du support convexe du profil R5 ; ils sont signalés individuellement, sans prétendre étendre son domaine.

## 1. Erreur technique identifiée dans R5

Le filtre des rivières de R5 retenait les indices de palette 3 à 11. Le fichier installé `C:/Games/Victoria 3/game/common/defines/jomini/rivers.txt`, ligne 5, prévoit **13 valeurs de largeur**. La palette native les porte aux indices **3 à 15** ; l'indice 15 vert n'est pas le marqueur de source d'indice 0.

Dans la fenêtre Bromberg–Fordon, R6 récupère **17 pixels d'indice 15**, soit **45 pixels de largeur** au lieu de 28. La Vistule n'est donc pas discontinue comme pouvait le faire croire l'image filtrée. Les fichiers R5 restent intacts : la correction est implémentée et réutilisable dans `pilot.py::physical_masks`, avec audit de palette et empreintes.

Les fenêtres des anciens contrôles Warta–Oder et Narew–Vistule ont aussi été inspectées : pas d'indice 15 dans leur voisinage de 7×7 pixels. Cela ne revalide pas toute la projection R5, mais évite d'attribuer automatiquement à ce filtre tous ses écarts. Aucun réajustement des mêmes anciens points n'est effectué.

## 2. Contrôle final nouveau, sans sélection a posteriori

`FROZEN_PROTOCOL.json` fixe les objets, fenêtres et règles d'extraction avant le calcul des nouveaux écarts. Il précise que les images ont déjà été explorées : ce n'est pas une expérience aveugle. **Aucun modèle n'est ajusté dans R6**, et ces contrôles ne servent pas à en sélectionner un autre.

Le minimum de longitude de la Vistule dans la fenêtre géographique fixée donne **18,142334 E ; 53,114765 N**. Le modèle R5 figé prédit **X=4510,8183 ; Y=764,1002**, dans son support. Le milieu déterministe des cinq cellules natives les plus occidentales est **4510,5 ; 763,5**, soit **0,6794 pixel** de désaccord.

**Ce chiffre n'est pas une précision locale certifiée de 0,68 pixel.** Le coude natif comporte un plateau de cinq cellules, et non une pointe unique. Son ambiguïté de lecture exige un rayon diagnostique de **2,5 pixels**, supérieur au rayon de 1,5 prévu au protocole. Cet écart au protocole est conservé explicitement. Les quatre variantes héritées donnent des désaccords au milieu allant de 0,68 à 1,52 pixel ; aucune n'est sélectionnée sur cette base. Aucune moyenne à plusieurs points n'est inventée à partir de ce seul contrôle mesurable.

À Wolgast, les deux rives du détroit ne sont pas distinguables dans les masques natifs de la fenêtre examinée. Les pixels d'eau présents appartiennent au contour côtier simplifié ; aucune largeur de rivière n'y dessine le chenal. Le contrôle final est **non mesurable**, avec résidu vide, et non « erreur nulle ». Une distance à la mer la plus proche ne le remplace pas.

## 3. Lecture historique : ce qui est identifié et ce qui ne l'est pas

Les polylignes dans `SOURCE_LINE_OBSERVATIONS.json` sont des **lectures en coordonnées des scans**, avec rayon de lecture. Les points géographiques restent vides dans le CSV lorsqu'aucune conversion source→réel n'est acceptée. Elles ne sont pas des frontières installées.

- **Mayer 1763 :** la rive occidentale du Peenestrom au droit de Wolgast est suivie séparément du contour d'Usedom. L'interprétation continent suédois / Usedom prussienne ne suffit pas à choisir une cellule lorsque le raccord géométrique reste incertain. La reproduction BSB « après 1763 » est une aide de lecture de la même famille, pas une seconde preuve politique indépendante.
- **Manuscrit N 1146/1 :** la note rouge désigne des villes et villages appartenant à la générale von Skorzewska. Elle ne donne pas leur souveraineté. Le liseré de la rive occidentale de la Vistule près de Fordon n'est pas accepté comme frontière internationale automatique ; il peut distinguer des ensembles administratifs ou un état de tracé dont la fonction et la datation doivent encore être établies.
- **Güssefeld/Homann 1775 :** un segment de liseré méridional, au sud de Bromberg et distinct du liseré de Fordon, est identifié comme candidat politique pertinent. Il reste à le raccorder au manuscrit et à des homologues réels contrôlés. Sa couleur, commune à d'autres limites de la planche, n'est pas à elle seule une preuve.

Le contexte municipal de Chełmno confirme son passage à la Prusse en 1772 ([histoire officielle, paragraphe historique](https://chelmno.pl/historia-chelmna/)). La notice institutionnelle de Fordon mentionne aussi son annexion en 1772 ([administration pénitentiaire polonaise](https://sw.gov.pl/aktualnosc/areszt-sledczy-w-bydgoszczy-fordonska-izba-pamieci-poswiecona-kobietom-podziemia-niepodleglosciowego)) ; son contenu n'a été disponible ici que par l'extrait indexé, l'ouverture complète ayant échoué. Ces indications corroborent le contexte, **pas une attribution de toutes les berges à partir de deux villes**. L'inférence négative reste bornée : ne pas convertir ce liseré entier en frontière Prusse–Pologne sans preuve supplémentaire.

Les anciennes croix ambiguës de Pfau à Inowrocław/Pakość ne sont pas réoptimisées. Aucun tracé de 1778 n'est substitué à celui du 1er janvier 1776.

## 4. Résolution et Peendamm

Le profil R5 donne vers 54,05 N environ **2,83 km par pixel en X**, **3,59 km en Y**, soit **10,18 km² par cellule**. C'est une échelle locale approximative du modèle, pas la surface exacte de toute province.

Les sections horizontales de l'eau LUNG près de Wolgast correspondent à environ **0,04–0,49 pixel en largeur projetée**. Elles décrivent l'eau moderne et des coupes horizontales, pas une largeur perpendiculaire certifiée du chenal de 1776. Cela explique une partie de sa disparition à la résolution native, sans en faire une preuve de l'emplacement historique des rives.

Les cinq repères urbains d'Anklam couvrent toujours **0,152×0,203 pixel**. Dans le modèle figé, quatre tombent en (4408,741), le moulin en (4408,740), près d'une limite de cellule. Cette séparation de grille n'est pas robuste face aux incertitudes : elle ne démontre ni la surface ni la représentabilité exacte de tout Peendamm. Son polygone historique n'est pas établi. **Aucune enclave d'une cellule entière n'est créée.**

L'absence d'un chenal dans le raster n'interdit pas de dessiner une frontière politique entre deux RGB. Elle empêche ici d'en vérifier localement la position physique. Une frontière continentale généralisée pourrait être proposée au joueur comme **approximation assumée**, sans élargir Peendamm ; elle ne doit pas être installée sous couvert de classe A.

## 5. Préservation et tests

**Validation statique finale : PASS, 49/49 contrôles.** Le détail est dans `VALIDATION.json`. Elle compare les **2 169 fichiers fonctionnels**, les empreintes des **264 fichiers R1–R5**, le bitmap, l'inventaire démographique/économique/militaire effectif, HEAD et l'index.

Référence conservée : `x567452` **357 SWE**, `xEDB010` **85 PRU**, `xFCC7B7` **142 PLC**, population mondiale **835 804 980**. Aucun nouveau RGB, population artificielle, déplacement de bâtiments/PM/propriétaires économiques, infrastructure ou unité. Thorn est exclu. Les **44 doublons RGB et 12 références invalides hérités** restent séparés des nouvelles régressions.

Il n'y a **aucune validation moteur R6** revendiquée et aucun nouveau correctif territorial à tester en partie. La validation manuelle R3 n'est pas réattribuée à R6.

## 6. Recherche locale et conclusion

ColGrep a été invoqué deux fois : refus du verrou d'index en environnement restreint, puis succès avec autorisation d'accès à l'index. Le résultat `R1/NETZE/REPORT.md:5` et `:9` a été vérifié aux lignes 1–24 ; il rappelle notamment les limites de datation de l'autre planche Homann. Il ne livre pas de nouveau calage. Pas de changement d'intégration, de télémétrie GPU capturée ni d'économie exacte de tokens mesurée.

Commande : `colgrep.exe --agent "Locate the already retained Gussefeld Homann 1775 map image and source metadata for Bromberg Fordon, and any local Wolgast Peenestrom high resolution historical map or physical control observations not in R5. Return only verified repository paths and useful line ranges. Search only; do not modify files or repeat projection searches." .`

La méthode d'extraction hydrographique est corrigée ; **la méthode complète de transfert de frontières n'est pas encore démontrée**. La meilleure suite n'est pas un R7 automatique : choisir entre une approximation politique explicitement autorisée pour Wolgast et l'apport de nouveaux ancrages locaux réellement homologués ; pour Bromberg, identifier/calibrer le seul segment méridional retenu avant toute nouvelle cellule.

Aucun commit, merge, push, reset, changement de branche ou modification de l'index Git.
