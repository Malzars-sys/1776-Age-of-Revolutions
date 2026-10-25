# ECON-ALLOYS-1776 — REFONTE DES ALLIAGES TRADITIONNELS

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` — 24 octobre 2026.

La production précoce est conservée en ère II. Les nouveaux débouchés sont une alternative d'artillerie en bronze, une très faible substitution domestique et quatre PM secondaires d'ustensiles. Aucun bien, besoin général ou nœud technologique supplémentaire. Aucune validation humaine ou moteur n'est déclarée.

## Production traditionnelle

`building_alloys_plant` → `pmg_alloys_process` → `pm_basic_smelting_process`.

| Par niveau pleinement employé, par semaine | Avant | Après |
|---|---:|---:|
| Fer | 25 | 3 |
| Cuivre | 15 | 4 |
| Plomb | 10 | 1 |
| Charbon | 10 | 2 |
| Alliages produits | 60 | 20 |
| Emplois du PM | 5 000 | 2 200 |
| Coût des intrants aux prix de base | 2 450 £ | 420 £ |
| Valeur de la production | 3 000 £ | 1 000 £ |
| Marge avant salaires | 550 £ | 580 £ |

Le PM devient **Fabrication traditionnelle d'alliages / Traditional Alloy Making**. Production −66,7 %, pollution 5 → 2. Emplois : 100 commerçants, 2 000 ouvriers, 100 machinistes ; suppression des 250 ingénieurs de cette méthode primitive.

Les salaires ne sont pas oubliés : à un salaire annuel de référence d'ouvrier de 10 £ et aux coefficients natifs des professions, le PM seul donne environ **+108,85 £/semaine**, contre −772,12 auparavant. Le bâtiment avec les premières entrées actuelles de ses autres groupes, notamment les données industrielles, donne +285,31 £/semaine dans cette même approximation. Ce ne sont pas des profits observés dans une sauvegarde. Voir [BALANCE_REVIEW.md](BALANCE_REVIEW.md).

Toutes les autres recettes existantes d'alliages et d'aluminium sont conservées. L'arc électrique produit toujours 90 alliages ; ses entrées, ses emplois, ses technologies et ses automatismes n'ont pas été rééquilibrés.

## Artillerie

Ajout de `pm_aor1776_bronze_artillery` dans `pmg_foundries`, à côté de `pm_cannons` : **10 fer + 10 bois dur + 4 alliages → 25 artillerie**. Les canons en fer conservent **15 fer + 10 bois dur → 25 artillerie**. Les deux options coûtent 1 000 £ d'intrants aux prix de base, avec les mêmes 5 000 emplois ; le bronze n'ajoute aucun cuivre brut. Aucun bonus militaire n'est inventé.

Déblocage du bronze : `standardized_field_artillery` (III) et `alloysworking` (II). Le fer reste disponible selon sa condition native. Les méthodes ultérieures sont intactes.

## Manufacture de meubles : un groupe indépendant

`pmg_aor1776_utensils` est ajouté uniquement à `building_furniture_manufactory`, après le groupe des meubles de luxe. Les PM principaux et de luxe restent inchangés. Intrants et production supplémentaires utilisent les modificateurs natifs `workforce_scaled`, emplois supplémentaires en `level_scaled`.

| Méthode | Intrants supplémentaires | Meubles supplémentaires | Technologie existante requise | Emplois supplémentaires |
|---|---|---:|---|---|
| Aucune fabrication | Aucun | 0 | Aucune | 0 |
| Fer forgé | Fer 1 | 2 | `organized_workshops` (I) | Ouvriers 50 |
| Cuivre et laiton | Fer 1, cuivre 0,5, alliages 0,5 | 5 | `organized_workshops` + `alloysworking` (II) | Ouvriers 100, machinistes 10 |
| Ustensiles usinés | Acier 1, cuivre 0,5, plomb 0,5, alliages 0,5 | 8 | `mechanical_tools` (V) + `alloysworking` | Ouvriers 100, machinistes 50, ingénieurs 10 |
| Ustensiles industrialisés | Acier 1, cuivre 0,75, plomb 0,5, alliages 0,75, aluminium 1 | 16 | `mechanical_tools` + `bayer_process` (X) | Ouvriers 120, machinistes 50, ingénieurs 30 |

Il y a quatre PM actifs, plus le PM neutre placé en premier suivant le modèle des groupes secondaires natifs. Le nombre de matières passe de 1 à 3, 4 puis 5 ; le rapport valeur produite/coût des matières progresse de **1,50 → 1,67 → 2,00 → 2,18**. La dernière recette contient bien les cinq métaux demandés, avec l'acier à la place du fer.

Précision terminologique confirmée pendant le travail : les nouveaux débouchés métallurgiques et la demande des POPs portent sur le bien **alliages**, pas sur le bien acier. Les deux PM tardifs consomment l'acier en complément des alliages ; les POPs ne reçoivent aucune entrée d'acier.

Les meubles supplémentaires représentent un assortiment d'objets domestiques, sans redéfinir tous les meubles du jeu : chaudronnerie en cuivre, bougeoirs et ferrures en alliage, pièces en acier, ustensiles en aluminium et poids en plomb. Les différentes matières ne désignent pas une unique composition d'alliage ni une vaisselle contenant systématiquement du plomb. Aucun mercure.

Les premiers paliers ajoutent 2 ou 5 meubles à une base artisanale de 45. Le dernier ajoute 16 à une base mécanisée de 110. Ce groupe n'applique aucun multiplicateur général. Le joueur peut revenir au PM neutre.

## Besoins domestiques

Une entrée `alloys` dans `popneed_household_items` : poids **0,02**, part d'offre minimale **0,01**, maximale **0,05**. Le besoin commence au palier de richesse **10** des paniers actuellement utilisés. Meubles, verre et papier gardent leurs paramètres. Aucun autre besoin modifié.

Ces paramètres bornent les coefficients de substitution ; ils ne sont pas une obligation d'acheter 1 % ou un plafond de dépense littéral de 5 %. Le modèle simplifié tiré des commentaires natifs borne le poids relatif normalisé des alliages sous 0,991 %, grâce au plancher déjà présent des meubles. La demande absolue mondiale et les effets des prix restent à observer. Voir [POP_CONSUMPTION_CHANGES.md](POP_CONSUMPTION_CHANGES.md).

## Technologies et départ 1776

`alloysworking` reste en II avec ses parents actuels `shaft_mining` et `organized_workshops`. Aucun fichier technologique ni profil national n'a été édité. Aucun coke distribué. L'aluminium industriel reste tardif : `bayer_process`, en X, conserve `bauxite_processing` et `electrical_capacitors`.

L'inventaire des scripts trouve douze profils contenant `alloysworking`, dont certains profils conditionnels : AUS, BEO, CHI, FRA, GBR, MGL, PRU, RUS, SAX, SWE, XIN, YUN. Cela ne prouve pas que tous ces pays existent sur la carte au départ. Les conditions des ustensiles cuivre/laiton sont présentes dans ces profils. L'artillerie en bronze est accessible avec les technologies recensées pour AUS, BEO, CHI, MGL, PRU, SAX, XIN et YUN ; FRA, GBR, RUS et SWE ne possèdent pas `standardized_field_artillery` dans cet inventaire. On conserve ces choix nationaux de TECH-R2. Lois, présence du pays, accès au marché et main-d'œuvre restent déterminés par le moteur. Détail : `STARTING_ACCESS.json`.

## Fichiers et localisations

Six fichiers existants de gameplay/localisation reçoivent des changements ciblés :

- `common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt` : seul PM traditionnel.
- `common/buildings/01_industry.txt` : une association de groupe.
- `common/production_method_groups/01_industry.txt` : une alternative dans les fonderies.
- `common/pop_needs/00_pop_needs.txt` : une entrée dans les objets domestiques.
- `localization/french/tech6c5c_aluminium_l_french.yml` et son équivalent anglais : nom et description du PM traditionnel.

Quatre fichiers créés : `1776_alloys_utensils.txt` dans les dossiers PM et PMG ; `1776_alloys_utensils_l_french.yml` et `_l_english.yml` dans leurs dossiers de langue. Treize nouvelles clés par langue, UTF-8 avec BOM, sans collision recensée dans le mod ou le vanilla. Icônes existantes réutilisées.

Outils : `tools/econ_alloys_1776.py`, `tools/test_econ_alloys_1776.py`, et mise à jour du seul invariant de recette primitive dans `tools/tech6c5c_validate.py`. Inventaire avec empreintes : `FILES_MODIFIED.json`.

## Vérifications et coexistence

**15 tests ciblés réussis**, couvrant syntaxe, références, coûts, emplois, progression, neutralité, association du groupe, combinaison avec les meubles de luxe, langues, BOM, absence de nouveau bien/technologie et invariants des fichiers partagés. Voir `TEST_RESULTS.json`.

L'ancien validateur donne les **mêmes quatre erreurs avant et après** : trois assertions sur le groupe de trains de voyageurs absent et une ancienne attente de parent unique pour `alloysworking`. Aucun nouvel échec de ce validateur. Ses résultats et ses empreintes de carte sont conservés avant/après ; les empreintes territoriales diffèrent du fait du chantier concurrent.

Un premier contrôle global des empreintes a signalé l'ajout de contenu ragusain et la modification de six fichiers territoriaux pendant l'intervention. La première exécution est archivée dans `INITIAL_TEST_RESULTS.json`. Le contrôle final sépare ces différences externes de nos invariants ; il ne les certifie pas et ne les réécrit pas. `CONCURRENT_CHANGES.json` les énumère. Aucun commit, staging, restauration de baseline, changement de HEAD ou de l'index Git.

Le code de cette mission n'écrit ni carte, ni population, ni diplomatie, ni registre impérial, ni ancien fichier de validation humaine. Les changements concurrents restent présents. Les contrôles économiques ne valent pas validation du chantier territorial.

## ColGrep et mesure

Un appel local `colgrep --agent` a terminé avec le code 0. Il a trouvé `common/pop_needs/00_pop_needs.txt:152-178`, emplacement exact vérifié avant modification ; le second extrait, lignes 180-538, est trop large et concerne surtout d'autres besoins. Aucun validateur utile n'a été livré par cette recherche ; les outils ont été retrouvés/inspectés directement.

Le modèle attendu est le 2B déjà configuré. La sortie conservée ici n'expose ni compteurs de tokens ni preuve de l'accélération GPU ; aucune vitesse d'inférence n'est inventée. Durée globale locale non instrumentée de façon fiable. Un minimum de onze invocations `rg` ciblées a été relevé dans la seconde partie de l'intervention, mais le total de toute la mission n'a pas été instrumenté. Les compteurs de tokens Codex ne sont pas disponibles. Aucune comparaison A/B : **pas d'économie de quota chiffrable**. Une localisation exacte utile, mais un apport modeste pour ce lot où de nombreux chemins étaient déjà connus. Pas de reconstruction d'index ; les nouveaux fichiers seront pris par la mise à jour incrémentale à la prochaine recherche qui en a besoin. Voir `COLGREP_METRICS.json`.

## À valider en jeu / différé

Lire [PLAYER_TEST_PROTOCOL.md](PLAYER_TEST_PROTOCOL.md) : nouvelle partie, vérification du groupe neutre, choix des PM, un mois de simulation puis sauvegarde/rechargement. La demande POP réelle, les choix de l'IA, le niveau des salaires et le rendu des nouveaux choix restent non testés dans le moteur.

La rentabilité du PM électrique isolé était déjà faible à certains salaires de référence. Ses recettes sont conservées conformément au périmètre ; son volume de 90 et sa productivité physique par emploi restent supérieurs. Pas de promesse de supériorité de marge à tous prix. Aucun ajout automatique de technologies nationales, aucune nouvelle matière « étain » ou « ustensiles », aucune reconstitution exacte des formulations de bronze/laiton.
