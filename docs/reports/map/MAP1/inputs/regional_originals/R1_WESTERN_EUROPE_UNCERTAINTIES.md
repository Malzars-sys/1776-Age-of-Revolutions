# R1_WESTERN_EUROPE — rapport de recherche et incertitudes territoriales

**Date historique obligatoire : 1776-01-01.**  
**État du rapport : 2026-10-10.**  
**Périmètre : R1_WESTERN_EUROPE uniquement.**  
**Règle de gestion : propositions documentaires ; aucune modification de la carte, de la population, des bâtiments, des fichiers historiques ou du dépôt Git.**

## 1. Résumé exécutable par la synthèse centrale

L'inventaire `MAP_1776_9_REGIONS.csv` contient exactement **82 couples `Owner_TAG + State_ID`**, **73 `State_ID` distincts**. La baseline principale contient **615 attributions de provinces RGB** dans ces couples. Le fichier `R1_WESTERN_EUROPE_COVERAGE.csv` possède **82 lignes de données**, une par couple, sans fusionner les co-propriétaires d'une même State Region. La vérification des fichiers CSV a relevé **35 recommandations territoriales/institutionnelles**, **43 références bibliographiques** et les statuts suivants :

| Statut de couverture | Nombre de couples | Sens strict |
|---|---:|---|
| `CHANGE_PROPOSED` | 6 | Une correction historique ou juridictionnelle mérite une étude de mapping ; **aucun transfert RGB approuvé**. |
| `UNRESOLVED` | 16 | Frontière, souveraineté, effet des enclaves ou correspondance nécessitant arbitrage ou preuve supplémentaire. |
| `REVIEWED_NO_CHANGE` | 60 | Aucune correction justifiée par les éléments examinés ; **ne signifie pas** que toutes les provinces ont été validées une par une. |

**Restriction fondamentale :** aucun bitmap de frontières des provinces, aucune superposition géoréférencée entre les cartes d'époque et les polygones du jeu n'étaient fournis. Les IDs RGB mentionnés dans les notes proviennent exclusivement de la baseline et des issues connues. Aucune recommandation ne renseigne `Province_ID` ou `Province_IDs` : les **35 recommandations portent `Mapping_Status=MAPPING_REQUIRED`** et proposent d'abord `A_EXISTING_PROVINCES` lorsque le problème exige un découpage, sinon `NONE` ou une option provisoire. Il n'est **jamais** demandé de passer en `C_GEOMETRY` sans preuve d'insuffisance des polygones existants.

Le tableau de couverture s'appuie sur une confrontation ciblée des sources historiques et des anomalies signalées. Il ne remplace pas la revue cartographique exhaustive des 615 provinces, ni l'examen de la propriété effective des villages enclavés. Le mot « reviewed » qualifie ici le couple de l'inventaire et non chacune de ses subdivisions.

## 2. Priorités critiques

### P0 — Luxembourg et Wallonie, `xD001A0`

- **Fait établi :** le duché de Luxembourg appartient aux Pays-Bas des Habsbourg d'Autriche, sous Marie-Thérèse au 1er janvier 1776. Il dispose cependant d'une histoire juridictionnelle propre, d'un Conseil provincial et souverain, d'États et d'une documentation cadastrale : ces institutions ne suffisent pas à conclure à une souveraineté indépendante. Les Archives nationales de Luxembourg décrivent les fonds correspondants (`R1_WESTERN_EUROPE-S001` à `S003`).
- **Fait cartographique distinct :** la baseline attribue effectivement `xD001A0` à `LUX` dans `STATE_WALLONIA`. On sait **que le RGB existe et est attribué**, non **ce que représentent ses contours**. Le mapping duché historique ↔ province du jeu doit vérifier l'espace entre Luxembourg-ville, Arlon, Bastogne, Chiny, Saint-Hubert et le pays de Trèves, non se déduire de `STATE_WALLONIA`.
- **Question historique séparée :** la documentation luxembourgeoise sur des limites contestées autour de 1776 (plans CP-A-45/46, dossier A-XI-11-02 daté du **2 mai 1776**) montre que la frontière n'est pas mécaniquement linéaire ni entièrement stabilisée. Une pièce de mai n'est pas une preuve de situation au 1er janvier sans chronologie.
- **Autres autorités dans la Wallonie moderne :** principauté de Liège, principauté abbatiale de Stavelot-Malmedy, duché de Bouillon, principautés et enclaves diverses. Les planches Ferraris, datées 1770–1778, et l'atlas wallon reconstitué vers 1789 les distinguent, mais les détails de frontières nécessitent corroboration (`S004`, `S005`, `S035`, `S041`, `S042`). Bouillon se prévaut d'une souveraineté ducale sous La Tour d'Auvergne, est protégé militairement par la France, et fait l'objet de prétentions liégeoises : **ne pas arbitrer cette souveraineté par le nom `BEO`**.
- **Issues techniques** `MAP0-0178`/`0185` (références de bâtiments orphelines), `MAP0-0208` (le candidat supprimerait la seule province `LUX`) et `MAP0-0207` (**−37 881** habitants dans un candidat) sont **des avertissements d'intégrité des données, pas des preuves historiques**. Ne redistribuer aucun habitant, bâtiment ou capitale sans validation séparée de la synthèse.
- **Arbitrage demandé :** géoréférencer les cartes du cadastre, Ferraris et plans frontaliers avec le bitmap ; décider si `LUX` doit être un sujet, une province régionale du pouvoir habsbourgeois ou autre compromis sans effacer l'administration distincte. `R1_WESTERN_EUROPE-0001` à `0004` et `0035`.

### P0 — Lombardie, `x867A90` et `x9AC196`

- **Fait établi :** Venise gouverne depuis l'époque moderne les territoires de Bergame, Brescia et **Crema**, cette dernière constituant une enclave de la Terre Ferme vénitienne. Les dossiers institutionnels de Lombardia Beni Culturali décrivent administration, fiscalité et justice sous domination vénitienne (`S008`). En parallèle, les terres milanaises, Pavie, Lodi, Crémone, Como et les domaines habsbourgeois constituent la Lombardie autrichienne, avec des spécificités historiques à Mantoue (`S009`, `S010`, `S037`).
- **Problème technique :** `x867A90` est déjà attribué à **VEN dans main**, tandis qu'un candidat non fusionné contient une **double attribution AUS/VEN** (`MAP0-0148`). Le RGB `x9AC196` existe également sous **VEN dans main**, et le candidat en change le propriétaire. `MAP0-0194` reflète un écart de catalogue concernant VEN. **Ne pas adopter le candidat comme nouveau fait historique**.
- **Arbitrage demandé :** identifier, dans le polygone du jeu, les rives de l'Adda, les frontières entre Brescia/Crémone, le territoire de Bergame et l'îlot de Crema avant toute correction. Préserver absolument les historiques spéciaux **VEN et GEN** (`S008`–`S010`). `R1_WESTERN_EUROPE-0008` à `0010`.

### P0 — Interfaces avec R2, droits impériaux et Alpes

- Une principauté savoyarde n'est pas un duché français en 1776 ; la **maison de Savoie** règne sur le royaume de Sardaigne avec des possessions alpines et ligures. La république de Gênes a des possessions discontinues, et des **fiefs impériaux** sont présents dans l'Apennin ligure. Il faut distinguer principauté, fief, souveraineté revendiquée et contrôle effectif.
- La **Gueldre** est particulièrement délicate : depuis 1713, la partie supérieure a été divisée entre les États généraux néerlandais, les Habsbourg d'Autriche, le roi de Prusse et les possessions du duché de Juliers. Les comtés et enclaves ne sont pas réductibles au seul binôme BEO/NET (`S034`, `S043` ; étude spécialisée Berkvens, 2004, pp. 151–190 à consulter intégralement avant détermination). Les territoires prussiens/Juliers ne deviennent **pas** automatiquement des couples R1 supplémentaires.
- Sont à transmettre à **R2_NORTHERN_CENTRAL_EASTERN_EUROPE** : limites du Luxembourg avec Trèves, Haut-Gueldre vers les puissances orientales, Alpes savoyardes, districts vénitiens orientaux et frontières impériales du Mantouan, domaines savoyards et fiefs ligures. Les 11 lignes portant `Cross_Region_Conflict=COORDINATION_REQUIRED` identifient les interfaces ; les recommandations R1 demeurent **la responsabilité de R1**, et R2 relit uniquement l'interface.

### P1 — Enclaves pontificales et souverainetés péninsulaires

- **Avignon et Comtat Venaissin** : enclave du pape malgré l'occupation par la France en 1768–1774 ; au 1er janvier 1776, l'administration pontificale est restaurée. L'annexion **1791** est postérieure. Sources : `S016`, `S017`, `S018`. L'emprise pourrait se trouver dans `STATE_PROVENCE` et, selon la géométrie du mod, un autre état avoisinant ; une recommandation séparée `STATE_RHONE` demeure `UNRESOLVED` et n'autorise aucun transfert sans vérification.
- **Bénévent et Pontecorvo** : possessions pontificales enclavées dans le royaume de Naples ; l'ouvrage d'Isernia, **tome II, p. 229**, donne la restitution de Bénévent le **23 mars 1774**, et celle de Pontecorvo au cours de 1774. Références `S019`, `S020`. Ni leur occupation bourbonienne antérieure ni la situation après 1776 ne justifient une annexion `SIC` au 1er janvier.
- **Noli** : république ligure historiquement distincte, liée à Gênes sans que l'alliance soit équivalente à son annexion administrative ; nécessite un statut précis de protection et des polygones (`S011`, `S036`). **Oneglia** et **Loano** sont des enclaves savoyardes ; la vente de Finale à Gênes date de 1713.
- **Saint-Marin** : république autonome enclavée dans les États pontificaux ; preuve de continuité institutionnelle UNESCO (`S015`), pas de contour provincial 1776.
- **Piombino, Elbe** : principauté de Piombino sous Boncompagni-Ludovisi ; **ne pas** lui attribuer uniformément l'île d'Elbe car Portoferraio et Porto Longone relèvent d'histoires et de juridictions particulières (`S014`).
- **Massa–Carrare** : l'identité territoriale et judiciaire est attestée, mais la relation entre **Marie-Thérèse Cybo-Malaspina**, Modène et les droits dynastiques/impériaux est plus complexe que la seule existence d'institutions (`S012` / `S013`). Les deux sources ne prouvent pas de la même manière l'indépendance externe. **Conserver `UNRESOLVED`** pour une qualification définitive de souveraineté et `NEW_TAG_REQUIRED` comme hypothèse seulement. Aucune redistribution à Modène, Lucques ou Toscane sans étude.

### P2 — Souveraineté effective, unions et îles

- **Minorque** britannique au 1er janvier 1776, rétrocédée à la Grande-Bretagne après la guerre de Sept Ans (1763) ; distinguer des autres Baléares espagnoles. `R1-0028`/`0029`, `S025`. La reconquête espagnole de 1782 est **postérieure**.
- **Gibraltar** : le traité d'Utrecht, **article X**, cède ville, château, port, fortifications, mais limite explicitement l'extension de juridiction sur le sol voisin (`S024`). L'occupation militaire ne justifie pas la souveraineté sur tout `STATE_UPPER_ANDALUSIA`, et la micro-province `xBC6ED3` n'est pas validée cartographiquement.
- **Corse** : contrôle militaire et administration française effectifs après 1769 ; le traité de Versailles 1768 avec Gênes comporte des ambiguïtés sur le titre et la permanence de la cession (`S028`). Ne présenter ni la propriété française de l'île comme antérieure à la conquête ni comme une vente simple.
- **Naples/Sicile** : deux royaumes distincts avec même souverain bourbonien en 1776 (`S021`). Ne pas fusionner immédiatement les territoires `SIC` continentaux avec le `GR3` insulaire ; un TAG de jeu ne vaut pas preuve d'un État souverain distinct.
- **Irlande** : royaume doté de son Parlement, sous le même roi que Grande-Bretagne et fortement dépendant de Londres ; union parlementaire **1801** postérieure (`S023`). Ni souveraineté pleinement indépendante de `IREK`, ni annexion constitutionnelle complète en 1776.
- **Malte** : gouvernement hospitalier sous **Emmanuel de Rohan-Polduc**, grand maître 1775–1797 ; occupation napoléonienne en **1798**, postérieure (`S026`, `S027`).
- **Açores** : capitainerie générale portugaise instituée en 1766 (`S031`, `S032`), mais hiatus dans la liste des titulaires entre 1774 et 1776 : **ne pas deviner** le titulaire en fonction le 1er janvier.

## 3. Contradictions et qualité des preuves — ne pas trancher silencieusement

| Dossier | Sources / preuves confrontées | Conclusion admissible | Point restant `UNRESOLVED` |
|---|---|---|---|
| Luxembourg indépendant ? | `S001` plans frontaliers; `S002/S003` institutions/cadastre; `S034` traités | Institution ducales distinctes sous souveraineté habsbourgeoise | Statut optimal `LUX` dans le moteur; contours exacts de `xD001A0`; administration locale ≠ souveraineté indépendante. |
| Haut-Gueldre | `S034` traité 1713; `S043` Berkvens pp.151–190 (notice bibliographique, **non intégralement dépouillée**); `S033` fonds néerlandais | Pluralité de souverains certaine | Délimitation de Venlo, Roermond, Geldern, Erkelenz, Weert et lieux communaux au 1776-01-01. |
| Bouillon | `S041` atlas wallon, droits contestés et appui français; `S042` rapport vers 1780, pp.441–467 | Administration locale ducale et protection militaire française attestées | Souveraineté de jure controversée entre La Tour d'Auvergne, Liège et cadre impérial; limite exacte. |
| Massa-Carrare | `S012` Treccani décrit réduction d'indépendance dynastique; `S013` archives décrivent des organes distincts | État administratif particulier | Indépendance externe, sujétion, union, compétences réelles en 1776. |
| Piombino/Elbe | `S014` notice princière | Piombino juridiction distincte | Ne prouve pas toute l'île d'Elbe; distinguer présides espagnols/bourboniens et places toscanes. |
| Corse | `S028` musée régional, conquête 1769 et caractère provisoire du traité de 1768 | France contrôle effectivement en 1776 | Nature du titre transmis par Gênes ; compatibilité juridique de la « cession provisoire ». |
| Ferraris vs date-cible | `S005/S006` levés 1770–78; `S004` atlas reconstitué 1789 | Supports de toponymie et d'organisation régionale | Modifications 1776–89 et biais du cartographe mandaté par puissance habsbourgeoise. |
| Royaume des Deux-Siciles | `S021` Département d'État américain | En 1776, Naples et Sicile séparés juridiquement sous un roi | Date/acte d'unification cité tantôt 1815, tantôt 1816, **sans effet** sur la cible 1776. |
| Avignon | `S016/S017` catalogue/étude de l'annexion 1791; `S018` historique d'occupation antérieure | Pape souverain en 1776 | Délimitation exacte, statut des enclaves et centres co-administrés. |

**Classification méthodologique :** traités et archives d'administration fondent de préférence les compétences juridiques ; cartes de l'époque aident à localiser, mais la couleur géographique ne prouve pas seule l'impôt ou la souveraineté ; cartes de synthèse modernes servent de comparaison, non de source primaire. Les pages bibliographiques encore non consultées sont clairement indiquées dans `SOURCES.csv`.

## 4. OUTSIDE_BASELINE — entités manquantes dans l'inventaire des TAGs R1

Les entités suivantes **ne possèdent pas leur propre TAG dans la liste de 20 TAGs fournie**. Elles ne sont ni créées, ni ajoutées comme provinces à la baseline, ni attribuées par supposition à une province RGB. Leur inscription vise la **synthèse centrale** pour décider qui doit les représenter et si des polygones existants les couvrent :

| Entité historique | Localisation / State_ID candidat non validé | Preuve et difficulté | Transmission |
|---|---|---|---|
| Principauté de Liège | Vallée de Meuse, autour de Liège–Huy–Dinant ; `STATE_WALLONIA` BEO candidat | `S004/S005/S035`; juridiction distincte des Pays-Bas autrichiens ; pas de TAG liégeois | `R1-0002` ; cartographie centrale. |
| Principauté de Stavelot-Malmedy | Stavelot (50.40N,5.93E), Malmedy (50.43N,6.03E) ; Wallonie | `S005/S035`; territoire abbatial discontinu, frontière de l'Empire | `R1-0003`, interface R2 si nécessaire. |
| Duché de Bouillon | Bouillon (49.80N,5.07E), vallée de Semois ; Wallonie | `S041/S042`, La Tour d'Auvergne, protection française, prétentions liégeoises ; pas de TAG | `R1-0035`; statut externe non résolu. |
| Principauté de Monaco | Monaco (43.74N,7.42E), Menton/Roquebrune à étudier ; Provence/Piémont candidat **non validé** | `S040` : État souverain indépendant sous protection militaire française **en 1776** ; source explicitement contemporaine par sa datation historique, mais institutionnelle rétrospective | Arbitrage R1/R2 et synthèse sur polygones azuréens ; **aucun Change_ID appliqué à un couple incertain**. |
| République de Noli | Noli (44.21N,8.41E), Ligurie | `S011/S036`; indépendant/lié à Gênes ; pas de TAG | `R1-0012`. |
| République de Saint-Marin | Mont Titano (43.93N,12.45E), Romagne | `S015`, continuité institutionnelle ; pas de TAG | `R1-0022`. |
| Principauté de Piombino | Piombino (42.92N,10.53E) et secteurs d'Elbe ; Toscane | `S014` ; droits sur Elbe non homogènes | `R1-0023`. |
| Duché de Massa et principauté de Carrare | Massa/Carrare côte apuane, Toscane/Émilie candidates | `S012/S013`, entité particulière mais suzeraineté litigieuse | `R1-0024`, à laisser `UNRESOLVED`. |
| Enclaves pontificales Avignon/Comtat | Avignon, Carpentras, Cavaillon, Valréas ; Provence/Rhône candidats | `S016`–`S018`; propriété pontificale, annexion France seulement 1791 | `R1-0016`/`0017`, TAG `PAP` existant donc pas de nouveau TAG. |
| Enclaves pontificales Bénévent/Pontecorvo | Bénévent (41.13N,14.78E) et Pontecorvo (41.46N,13.67E), Campanie candidate | `S019`/`S020`, restitutions 1774 ; TAG `PAP` déjà existant | `R1-0018`/`0019`. |
| Fiefs impériaux ligures et apennins | Pays de Montferrat, haut Apennin, ligurie orientale ; Piémont/Émilie possibles | `S011/S036/S038` : souverainetés composites ; inventaire parcellaire manquant | R1↔R2, lot **OUTSIDE_BASELINE** s'ils sont absents des 82 couples. |

Territoires **explicitement hors de notre périmètre** malgré les métropoles occidentales : colonies ultramarines de GBR/FRA/SPA/POR/NET ; domaines vénitiens de Dalmatie et d'Istrie si classés en R2 ; toutes les possessions administratives d'un empire au-delà de l'inventaire R1. Leur appartenance à la métropole **ne suffit jamais à les intégrer à R1**.

## 5. Confrontation aux issues techniques et gel des candidats

| Issue_ID | Observation du registre | Décision R1 |
|---|---|---|
| `MAP0-0148` | Candidat collaborateur attribue `x867A90` à AUS **et** VEN | Refuser déduction historique de ce doublon ; cartographie nécessaire (`R1-0008/0009`). |
| `MAP0-0178` | Bâtiment LUX orphelin, `00_west_europe.txt` | Ne modifier aucun bâtiment tant que le dossier territorial Luxembourg n'est pas arbitré. |
| `MAP0-0185` | Bâtiment LUX orphelin, `98_build_start_1776_world_redistribution.txt` | Même gel, vérifier références après éventuelle décision de synthèse. |
| `MAP0-0194` | Écart de couple propriétaire VEN dans le catalogue | Ne pas effacer VEN ; baseline main seule référence technique de l'étude. |
| `MAP0-0207` | Candidat entraîne variation nette **−37 881 habitants** en Wallonie | Pas de migration de population ni compensation fictive ; revue dédiée si une carte est approuvée. |
| `MAP0-0208` | Candidat ôte à LUX sa seule province `xD001A0` | Bloquer jusqu'à décision politique/cartographique et plan de migration des scopes historiques. |

Le candidat `georg3mx` **n'est pas fusionné dans `main`**. Toutes les propositions ont été construites sur les lignes de **main** telles que fournies, pas sur la présence ou l'absence de syntaxe dans le candidat.

## 6. Feuille de transmission à la synthèse centrale

**À exécuter avant une éventuelle modification du mod, hors mandat R1 :**

1. Géoréférencer la baseline des **615 provinces RGB** avec les planches Ferraris (en notant leur date exacte), les atlas italiens et les archives locales. Enregistrer les appariements géométriques vérifiés et les zones incomplètes.
2. Réviser en priorité `R1-0001/0002/0003/0004/0035` (Wallonie, Luxembourg, Liège, Stavelot, Bouillon), puis `R1-0008/0009/0010` (Lombardie VEN/AUS).
3. Résoudre les interfaces R2 **sans doublonner** les recommandations et, pour les territoires extérieurs à la baseline, attribuer la charge de recherche au responsable régional compétent.
4. Vérifier la portée des juridictions et droits de souveraineté avec des archives/tables fiscales, traités, garnisons et tribunaux, en distinguant **de jure**, **de facto** et **contrôle militaire**.
5. Pour chaque éventuel transfert, faire approuver `Requires_New_Tag`, `Requires_State_Split`, `Gameplay_Approximation` et le lot séparé sur population/bâtiments/capitales/ports/sujets. **VEN/GEN : historiographies spécifiques protégées.**
6. Documenter les décisions par `Change_ID`, références `Source_IDs`, preuve de correspondance et statut de validation. Une contradiction demeure **UNRESOLVED** jusqu'au traitement explicite des sources opposées.

## 7. Index intégral des recommandations

Chaque `Change_ID` ci-dessous renvoie à la ligne complète du CSV avec sources, statut de correspondance, nature de contrôle, conclusion historique, approximation gameplay et incertitude. Les lignes de simple maintien institutionnel servent à éviter qu'un événement postérieur (1791, 1797, 1801, 1815/1816, 1798) soit projeté rétrospectivement sur 1776.

<!-- INDEX_GENERATED_BELOW -->

| Change_ID | Couple Owner/State | Institution / territoire | Décision de recherche | Confiance | Sources |
|---|---|---|---|---|---|
| `R1-0001` | `LUX` / `WALLONIA` | Duché de Luxembourg et comté de Chiny | Maintien provisoire et vérification locale | `HIGH` | S001|S002|S003|S034 |
| `R1-0002` | `BEO` / `WALLONIA` | Principauté épiscopale de Liège | Hypothèse de transfert / nouvel acteur | `HIGH` | S004|S005|S035 |
| `R1-0003` | `BEO` / `WALLONIA` | Principauté abbatiale de Stavelot-Malmedy | Hypothèse de transfert / nouvel acteur | `MEDIUM` | S005|S035 |
| `R1-0004` | `BEO` / `WALLONIA` | Pays-Bas autrichiens — provinces méridionales | Maintien provisoire et vérification locale | `MEDIUM` | S004|S005|S006|S034 |
| `R1-0005` | `BEO` / `GELRE` | Quartier supérieur de Gueldre, partie autrichienne | Souveraineté ou mapping à résoudre | `UNRESOLVED` | S004|S034 |
| `R1-0006` | `NET` / `GELRE` | Gueldre des Provinces-Unies et terres de la Généralité | Souveraineté ou mapping à résoudre | `UNRESOLVED` | S033|S034|S043 |
| `R1-0007` | `BEO` / `FLANDERS` | Comté de Flandre, Pays-Bas autrichiens | Maintien provisoire et vérification locale | `MEDIUM` | S005|S006|S034 |
| `R1-0008` | `VEN` / `LOMBARDY` | Terraferma veneta: Bergamo, Brescia, Crema | Maintien provisoire et vérification locale | `HIGH` | S008 |
| `R1-0009` | `AUS` / `LOMBARDY` | État de Milan et duché de Mantoue | Maintien provisoire et vérification locale | `HIGH` | S009|S010|S037 |
| `R1-0010` | `VEN` / `VENETIA` | République de Venise, Domini di Terraferma | Maintien provisoire et vérification locale | `MEDIUM` | S008|S038 |
| `R1-0011` | `GEN` / `PIEDMONT` | République de Gênes, Riviere ligures et Finale | Maintien provisoire et vérification locale | `HIGH` | S011|S036 |
| `R1-0012` | `GEN` / `PIEDMONT` | République de Noli | Hypothèse de transfert / nouvel acteur | `MEDIUM` | S011|S036 |
| `R1-0013` | `SAR` / `PIEDMONT` | Enclaves savoyardes de Oneglia et Loano | Maintien provisoire et vérification locale | `HIGH` | S011|S036 |
| `R1-0014` | `SAR` / `SAVOY` | Duché de Savoie, États de Savoie | Maintien provisoire et vérification locale | `MEDIUM` | S011|S029 |
| `R1-0015` | `SAR` / `PROVENCE` | Comté de Nice, États sardes | Maintien provisoire et vérification locale | `MEDIUM` | S011|S036 |
| `R1-0016` | `FRA` / `PROVENCE` | Avignon et Comtat Venaissin (enclaves pontificales) | Hypothèse de transfert / nouvel acteur | `HIGH` | S016|S017|S018 |
| `R1-0017` | `FRA` / `RHONE` | Interface Avignon/Comtat avec les provinces françaises du Rhône | Souveraineté ou mapping à résoudre | `UNRESOLVED` | S007|S016|S017 |
| `R1-0018` | `SIC` / `CAMPANIA` | Enclave pontificale de Benevento | Hypothèse de transfert / nouvel acteur | `HIGH` | S019|S020 |
| `R1-0019` | `SIC` / `CAMPANIA` | Enclave pontificale de Pontecorvo | Hypothèse de transfert / nouvel acteur | `MEDIUM` | S019|S020 |
| `R1-0020` | `GR3` / `SICILY` | Royaume de Sicile, couronne bourbonienne | Maintien provisoire et vérification locale | `HIGH` | S021 |
| `R1-0021` | `SIC` / `ABRUZZO` | Royaume de Naples, Abruzzes | Maintien provisoire et vérification locale | `HIGH` | S021 |
| `R1-0022` | `PAP` / `ROMAGNA` | République de Saint-Marin | Hypothèse de transfert / nouvel acteur | `HIGH` | S015 |
| `R1-0023` | `TUS` / `TUSCANY` | Principauté de Piombino | Hypothèse de transfert / nouvel acteur | `HIGH` | S014 |
| `R1-0024` | `TUS` / `TUSCANY` | Duché de Massa et principauté de Carrare | Souveraineté ou mapping à résoudre | `UNRESOLVED` | S012|S013 |
| `R1-0025` | `LUC` / `EMILIA` | République de Lucques et interface de Massa-Carrara | Maintien provisoire et vérification locale | `MEDIUM` | S012|S013 |
| `R1-0026` | `MOD` / `EMILIA` | Duché de Modène et Reggio | Maintien provisoire et vérification locale | `MEDIUM` | S012|S013 |
| `R1-0027` | `PAR` / `EMILIA` | Duché de Parme et de Plaisance | Maintien provisoire et vérification locale | `MEDIUM` | S009|S021 |
| `R1-0028` | `GBR` / `BALEARIC_ISLANDS` | Minorque, possession britannique | Maintien provisoire et vérification locale | `HIGH` | S025 |
| `R1-0029` | `SPA` / `BALEARIC_ISLANDS` | Majorque, Ibiza et Formentera, Couronne d Espagne | Maintien provisoire et vérification locale | `MEDIUM` | S025|S030 |
| `R1-0030` | `GBR` / `UPPER_ANDALUSIA` | Gibraltar, forteresse cédée en 1713 | Maintien provisoire et vérification locale | `HIGH` | S024|S039 |
| `R1-0031` | `FRA` / `CORSICA` | Corse sous administration militaire française | Maintien provisoire et vérification locale | `MEDIUM` | S007|S028 |
| `R1-0032` | `MLT` / `MALTA` | État des Hospitaliers de Saint-Jean à Malte | Maintien provisoire et vérification locale | `HIGH` | S026|S027 |
| `R1-0033` | `IREK` / `LEINSTER` | Royaume d Irlande, dépendant de la Couronne britannique | Maintien provisoire et vérification locale | `HIGH` | S023 |
| `R1-0034` | `POR` / `AZORES` | Capitania-Geral dos Açores, couronne du Portugal | Maintien provisoire et vérification locale | `HIGH` | S031|S032 |
| `R1-0035` | `BEO` / `WALLONIA` | Duché de Bouillon sous La Tour d Auvergne | Souveraineté ou mapping à résoudre | `UNRESOLVED` | S041|S042 |

**Traçabilité :** les identifiants complets conservés dans les CSV sont de la forme `R1_WESTERN_EUROPE-0001` et `R1_WESTERN_EUROPE-S001`. Les abréviations `R1-0001` et `S001` du présent rapport sont des alias lisibles et ne doivent pas remplacer les identifiants CSV.
