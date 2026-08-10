# WORKSHOP_PREP_1E — BEO BASE COA, DOCUMENTATION REORGANIZATION AND FINAL RUNTIME QA

## État

- Phase : `WORKSHOP_PREP_1E_BEO_BASE_COA_DOCUMENTATION_REORGANIZATION_AND_FINAL_RUNTIME_QA`
- Branche : `workshop-prep-frontend-objectives`
- HEAD d’entrée : `a25ecf7128bdd254e0296947220b3d33ca27ba09`
- Runtime humain autorisé : `1`
- Runtime humain effectué : `1 / 1`
- État courant : `COMPLETE`

## Correction BEO

L’interface des objectifs appelle `CountryDefinition.GetBaseFlag`. Le fork possédait des règles dynamiques `BEO` fondées sur les variantes `BEL`, mais aucun CoA de base nommé exactement `BEO`, ce qui produisait la présentation blanche observée en PREP1D.

Un seul bloc de base `BEO` a été ajouté dans `common/coat_of_arms/coat_of_arms/03_new.txt`. Il utilise exclusivement des composants distribués avec Victoria 3 : le champ noir-jaune du CoA autrichien et les armes couronnées du Brabant déjà présentes dans `BEL_subject`. Il s’agit d’un équivalent statique de présentation combinant l’autorité habsbourgeoise et l’identité brabançonne, pas de la revendication d’un nouveau drapeau national exact.

Ce choix évite le tricolore belge de 1830 et le pavillon marchand des Pays-Bas autrichiens approuvé après la date de départ. Le contexte politique est cohérent avec le règne de Marie-Thérèse sur les Pays-Bas autrichiens depuis Vienne ([Archives de l’État en Belgique](https://www.arch.be/index.php?e=maria-theresia-en-de-oostenrijkse-nederlanden-een-afstandelijke-heerschappij&l=nl&m=nieuws&r=studiedagen)). Les composants héraldiques sont également cohérents avec les insignes autrichiens et brabançons d’époque conservés par le [Kunsthistorisches Museum](https://www.khm.at/en/artworks/das-oesterreichische-erbpanier-100671) et son [tabard du Brabant de 1715](https://www.khm.at/en/artworks/tabard-for-the-king-at-arms-and-herald-of-the-archduchy-of-brabant-100720).

Résultats statiques :

```text
BEO_BASE_COA_EXISTS = yes
BEO_BASE_COA_UNIQUE = yes
BEO_BASE_COA_REFERENCES_RESOLVE = yes
BEO_FLAG_DEFINITION_REMAINS_VALID = yes
BEO_HISTORY_UNCHANGED = yes
BEL_HISTORY_UNCHANGED = yes
TUTORIAL_RECOMMENDED_TAGS_UNCHANGED = SWE BEO DAI DENNOR
BEO_BASE_COA_STATIC_PASS
```

## Réorganisation documentaire

Baseline :

```text
TOTAL_DOC_FILES_BEFORE = 295
HOTFIX_INDEX_ROOT_FILES_BEFORE = 94
WORKSHOP_REPORT_FILES_BEFORE = 15
BROKEN_LINKS_BEFORE = 0
REPORT_INDEX_ROWS_BEFORE = 160
```

Les rapports 6A sont maintenant regroupés sous `docs/reports/hotfix/global_script/`, les deux inventaires transversaux sous `global_script/inventories/`, les preuves militaires sous `runtime/` et les opérations anciennes sous `archive/`. Les livrables Workshop PREP1 à PREP1E sont regroupés par phase sous `docs/reports/workshop/frontend/`.

Le manifeste exhaustif est `docs/reports/DOCUMENTATION_REORGANIZATION_MANIFEST.csv`. Il contient `103` déplacements et leurs hashes. Les fichiers déplacés dont un chemin actif a dû être corrigé sont signalés par `references_updated = true` et `content_changed = true`; leurs conclusions historiques n’ont pas été reformulées.

État après création des index et des livrables PREP1E :

```text
TOTAL_DOC_FILES_AFTER = 305
HOTFIX_INDEX_ROOT_FILES_AFTER = 7
FILES_MOVED = 103
FILES_DELETED = 0
REPORT_INDEX_ROWS_AFTER = 160
REPORT_INDEX_ROWS_LOST = 0
REPORT_INDEX_DUPLICATE_PHASE_IDS = 0
REPORT_INDEX_BROKEN_PATHS = 0
EXACT_OLD_PATH_REFERENCES_OUTSIDE_MANIFEST = 0
BROKEN_LOCAL_DOC_LINKS_AFTER = 0
NEW_BROKEN_LOCAL_DOC_LINKS = 0
DOCUMENTATION_FILE_LOSS = 0
```

## Runtime ciblé

- Fiche opérateur : `WORKSHOP_PREP_1E_OPERATOR_RUNTIME_CHECKLIST.md`
- Matrice : `WORKSHOP_PREP_1E_RUNTIME_TEST_MATRIX.csv`
- Résultats : `WORKSHOP_PREP_1E_RUNTIME_RESULTS.csv`
- Baseline et preuves de logs : `WORKSHOP_PREP_1E_LOG_MANIFEST.csv`

L’opérateur a effectué exactement une ouverture, puis a enregistré la fiche et fermé Victoria 3 ainsi que le launcher. Le contrôle de processus après session donne `0`.

```text
Runtime matrix = 18 PASS / 0 FAIL / 0 NOT_RUN

TRAFALGAR_LOADING_SCREEN = PASS
DELAWARE_FRONTEND = PASS
CANTUS_FIRMUS_STARTS = PASS
TUTORIAL_RECOMMENDATIONS = PASS
BEO_BASE_FLAG_VISIBLE = yes
BEO_BASE_FLAG_NOT_BLANK = yes
BEO_BASE_FLAG_PERIOD_APPROPRIATE = yes
BEO_BASE_COA_RUNTIME = PASS
TUTORIAL_TEXTS = PASS
NO_RAW_KEYS = PASS
NO_MAJOR_OVERFLOW = PASS
BIC_FLAG_REMAINS_PASS
VOC_FLAG_REMAINS_PASS
FRA_BOURBON_FLAG_REMAINS_PASS
OBJECTIVE_ART_REMAINS_PASS
GAME_ENTRY_SMOKE = PASS
WORKSHOP_PREP_1E_HUMAN_RUNTIME_LAUNCHES = 1
```

## Observation BIC et Treize Colonies

Les captures prises après l’entrée en jeu montrent un canton britannique sur les drapeaux de la BIC et des Treize Colonies, alors que leurs cartes d’objectif montrent leurs CoA de base. Cette différence est expliquée par deux chemins de présentation existants : les cartes appellent `CountryDefinition.GetBaseFlag`, tandis que les règles dynamiques des deux sujets ont `allow_overlord_canton = yes` et autorisent la superposition du canton du suzerain.

L’enseigne BIC de la carte d’objectif, le drapeau BIC dynamique et le drapeau dynamique des Treize Colonies ont tous été rendus sans texture blanche, clé brute ou erreur. Aucun trigger n’est modifié dans PREP1E. L’écart base/dynamique est donc enregistré comme `EXPECTED_BASE_VS_SUBJECT_FLAG_CONTEXT`, non comme une régression du correctif BEO.

## Logs frais

Les neuf logs surveillés ont reçu une entrée `after` avec taille, date UTC et SHA-256. `error.log` contient zéro correspondance ciblée pour BEO, le système CoA, `03_new.txt`, les objectifs, le frontend ou Cantus Firmus.

`debug.log` signale un token malformé `@canton_scale_denmark_y` dans `common/flag_definitions/07_NM_Flags.txt`. Ce fichier est inchangé par PREP1E et le diagnostic ne vise ni le nouveau bloc BEO ni ses quatre composants. Les doublons de localisation déjà présents ne se sont pas matérialisés en clé brute pendant la session.

```text
NEW_WORKSHOP_PREP_1E_ATTRIBUTABLE_ERRORS = 0
```

## Protections

```text
STASH_NAVY_3C_3_INTACT = yes
TECH_RESEARCH_FILES_INTACT = yes
BJECT_ABSENT = yes
NO_AUTOMATIC_COMMIT
NO_AUTOMATIC_PUSH
PREP2_NOT_STARTED
```

## Verdict final

```text
WORKSHOP_PREP_1E_BEO_BASE_COA_DOCUMENTATION_REORGANIZATION_AND_FINAL_RUNTIME_QA_COMPLETE

BEO_BASE_COA_STATIC_PASS
BEO_BASE_COA_RUNTIME_PASS
BEO_TUTORIAL_FLAG_NO_LONGER_BLANK
BEO_PERIOD_PRESENTATION_PASS

TRAFALGAR_LOADING_SCREEN_REMAINS_PASS
DELAWARE_FRONTEND_REMAINS_PASS
CANTUS_FIRMUS_REMAINS_PASS
BIC_FLAG_REMAINS_PASS
VOC_FLAG_REMAINS_PASS
OBJECTIVE_ART_REMAINS_PASS
TUTORIAL_TEXTS_REMAIN_PASS

DOCUMENTATION_REORGANIZATION_COMPLETE
DOCUMENTATION_FILE_LOSS = 0
HOTFIX_INDEX_DECLUTTERED
HOTFIX_REPORT_INDEX_PATHS_PASS
NEW_BROKEN_LOCAL_DOC_LINKS = 0
DOCUMENTATION_REORGANIZATION_MANIFEST_COMPLETE

NEW_WORKSHOP_PREP_1E_ATTRIBUTABLE_ERRORS = 0
WORKSHOP_PREP_1_FRONTEND_OBJECTIVES_FULLY_RUNTIME_VALIDATED = YES

NO_UNRELATED_GAMEPLAY_CHANGED
ONE_HUMAN_RUNTIME_ONLY
STASH_NAVY_3C_3_INTACT
TECH_RESEARCH_FILES_INTACT
NO_AUTOMATIC_COMMIT
NO_AUTOMATIC_PUSH

NEXT_PHASE = WORKSHOP_PREP_2_THUMBNAIL_METADATA_AND_DESCRIPTION
```

PREP2 n’est pas commencé dans cette exécution.
