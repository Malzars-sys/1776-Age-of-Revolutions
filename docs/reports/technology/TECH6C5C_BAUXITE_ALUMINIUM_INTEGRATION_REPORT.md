# TECH6C5C — Intégration alliages, bauxite et aluminium

## Source auditée

Le bloc a été audité dans le mod local Steam Workshop **[1.13] Tech & Res** (`tech.res`, version 1.6, atelier `3472248460`). Le second passage couvre désormais le bâtiment d'alliages complet : bien `alloys`, production de base, production électrique, branche aluminium simultanée et tous les consommateurs de la source qui existent réellement dans le fork. Les systèmes contemporains absents du fork ne sont pas importés.

## Chaîne technologique retenue

- `alloysworking`, **Élaboration des alliages**, est importé comme technologie de Production d'ère II, avec `shaft_mining` pour parent comme dans la source. Il débloque l'usine d'alliages et sa fusion de base : la chaîne n'attend donc plus l'électricité tardive pour exister.
- `bauxite_processing`, **Procédé Wöhler-Deville**, passe en ère VI et requiert `alloysworking` avec `industrial_alkalis`. Elle révèle les gisements, débloque la mine de bauxite et le premier procédé chimique d'aluminium.
- `bayer_process`, **Procédé Bayer**, passe en ère X et requiert `bauxite_processing` avec `electrical_capacitors`. Elle débloque le procédé Hall-Héroult et les usages tardifs de l'aluminium.
- `electric_arc_process` conserve son rôle existant d'ère X et débloque la seconde méthode de production des alliages.

## Extraction et répartition mondiale

La ressource n'est pas inscrite directement dans les fichiers de régions. Lors de la première recherche mondiale de `bauxite_processing`, un effet protégé par une variable globale révèle une seule fois les potentiels suivants :

| Palier | États | Potentiel par État | Trait |
|---|---:|---:|---|
| Nano | 53 | 10 | aucun |
| Petit | 72 | 25 | aucun |
| Moyen | 24 | 50 | +5 % de rendement |
| Grand | 9 | 120 | +10 % de rendement |
| Immense | 3 | 200 | +10 % de rendement |
| **Total** | **161** | — | — |

Les 161 identifiants d'État de la source existent tous dans la carte actuelle et aucun État n'est présent dans deux paliers.

La mine dédiée conserve les paliers d'extraction de la source : pics et pelles (20), pompe atmosphérique (40), pompe à condensation (60), pompe Diesel (85), nitroglycérine (+12) et dynamite (+20). Le carburant léger absent de 1776 est remplacé par le bien existant `refined_fuels`. Une concentration du minerai compatible avec les systèmes du fork ajoute 16 bauxites contre outils et produits chimiques industriels. Les variantes de ventilation, d'automatisation à vapeur et de transport ferroviaire propres à cette mine reprennent le comportement des PM communs, mais exigent aussi `bauxite_processing` : aucune méthode de la mine ne peut ainsi précéder le déblocage du bâtiment.

## Usine, transformation et débouchés

- L'ancien bâtiment partiel `building_non_ferrous_metallurgy_works` est remplacé par le bâtiment source `building_alloys_plant`, débloqué par `alloysworking`.
- Son premier PMG produit 60 alliages par fusion au charbon, puis 90 alliages par four électrique. `commonores` est adapté en fer, cuivre et plomb ; aucun minerai générique supplémentaire n'est créé.
- Son second PMG est simultané et commence par `pm_no_aluminium_production`. Le procédé Wöhler-Deville consomme 50 bauxites, 3 explosifs et 3 soufres, retire 10 unités à la capacité d'alliages et produit 55 aluminium.
- Le procédé Hall-Héroult consomme 40 bauxites, 10 produits chimiques industriels et 20 électricités, retire 15 unités à la capacité d'alliages et produit 80 aluminium.
- Articles ménagers en aluminium : débouché ajouté aux verreries.
- Voitures voyageurs en aluminium : débouché ajouté au PMG ferroviaire existant, avec 5 aluminium pour 20 Transportation.
- Avions entièrement métalliques : débouché conservé et désormais rattaché au `bayer_process`.
- Conducteurs en aluminium : substitution tardive au cuivre dans les centrales, rattachée au `bayer_process`.

Tous les consommateurs d'alliages du mod source ayant un PM homonyme actif dans le fork ont été adaptés : construction à ossature d'acier et construction structurelle moderne, ateliers de meubles mécanisés, outils en acier et à poignées en caoutchouc, arcades et éclairage public, navires métalliques et soudés, automobiles, fusils à répétition et à verrou, ainsi que les trois paliers tardifs d'artillerie. Lorsque la source substituait les alliages à une partie de l'acier, du fer ou du bois, cette substitution a été conservée afin de ne pas dégrader artificiellement la rentabilité.

Les biens propres à Tech & Res absents du fork (`commonores`, `advancedores`, `electroniccomponents`, `water`, `gas`, `light_fuel`) ne sont pas créés. Les deux procédés d'alliages futuristes qui en dépendent et les consommateurs postérieurs à l'horizon de l'arbre (missiles, robotique, électronique contemporaine, réacteurs de fusion, chars modernes et véhicules intelligents) restent exclus. Ce choix évite d'introduire des biens sans chaîne autonome uniquement pour satisfaire une copie littérale.

## Correction connexe — ingénierie structurelle moderne

`arc_welding` conserve son ID pour la compatibilité, mais ses localisations anglaise et française sont forcées dans les dossiers `replace` sous les noms **Modern Structural Engineering** et **Ingénierie structurelle moderne**. `pneumatic_tools` est ajouté à ses parents, avec `electric_arc_process` et `reinforced_concrete`. Le PM de construction associé est localisé comme **Modern Structural Construction** / **Construction structurelle moderne**.

## Validation statique

- trois technologies de chaîne, sans cycle et avec leurs parents attendus ;
- définitions uniques des biens, bâtiments, PMG, PM et modificateurs ;
- 161 États distribués, zéro doublon et zéro identifiant inconnu ;
- recettes, portes technologiques et 18 débouchés source compatibles vérifiés ;
- causalité bâtiment/PM vérifiée, avec zéro méthode disponible avant la mine de bauxite ;
- références PMG/PM et biens résolues ;
- ressources graphiques présentes ;
- localisations anglaises et françaises présentes avec BOM UTF-8 ;
- aucun ajout direct de bauxite aux fichiers de régions ;
- `git diff --check` sans erreur.

Un runtime avec rechargement complet reste nécessaire pour confirmer l'affichage et le déclenchement du reveal en jeu.
