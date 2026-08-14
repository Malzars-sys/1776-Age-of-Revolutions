# DOCS-PREPATCH-1 — Documentation Cleanup, Indexing & Leftover Audit

## 1. Résumé

L'audit couvre exactement les 11 reliquats documentaires demandés : 4 hors technologie et 7 fichiers de recherche technologique. Aucun contenu des sept fichiers technologiques n'a été modifié, déplacé ou renommé.

Résultat : un changement suivi est prêt à conserver, deux fichiers `_index` sont des reliquats remplacés à ne pas stage, trois fichiers de recherche de design sont prêts à conserver, et cinq documents demandent une décision ou une correction avant commit. La recherche problématique n'est pas supprimée.

```text
DOCUMENTATION_AUDIT = PASS
DOCS_FILES_AUDITED = 11
TECH_RESEARCH_FILES_AUDITED = 7
NON_TECH_LEFTOVERS_AUDITED = 4
```

## 2. Préflight Git

```text
CURRENT_BRANCH = cleanup-post-release
CURRENT_HEAD = 2c2ae7d2e4acf010dc5a3e75134ff038110cc33c
STAGED_FILES = 0
GIT_DIFF_CHECK = PASS
```

Le worktree initial contenait exactement le changement suivi `CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md`, le rapport Maratha non suivi, les deux reliquats non suivis de `_index/` et les sept fichiers non suivis sous `docs/research/technology/`.

## 3. Matrice des 11 décisions

Les `reference_count` ci-dessous sont les comptes de base mesurés avant création des présents index et livrables. Ils excluent le fichier cible lui-même. Pour les deux reliquats `_index`, le compte utilise le chemin exact, pas le seul nom de fichier qui désignerait aussi la copie canonique.

| file | git_status | category | purpose | reference_count | recommended_action | recommended_destination | safe_to_commit | notes |
|---|---|---|---|---:|---|---|---|---|
| `docs/reports/cleanup/CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md` | `??` | cleanup report | Diagnostic de l'échec de recrutement naval Maratha | 8 | `REVIEW_REQUIRED` | `docs/reports/cleanup/`, sous un identifiant distinct après correction | NO | Recherche diagnostique unique, mais doublon d'identifiant CLEANUP-1D et conclusion BOM non présente dans HEAD |
| `docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md` | `M` | cleanup closure | Clôture de la reconstruction historique européenne | 7 | `KEEP_AND_COMMIT` | chemin actuel | YES | Le diff ajoute uniquement la preuve runtime finale et remplace l'attente de test par `CLEANUP2B3_RUNTIME=PASS` |
| `docs/reports/hotfix/_index/army.md` | `??` | hotfix index leftover | Note humaine de provenance sur la copie des fichiers d'armée | 4 | `DISCARD_AS_REDUNDANT` | aucune ; autorité : `docs/reports/hotfix/runtime/military/army.md` | NO | `_index` n'est pas la destination canonique ; le manifeste confirme le déplacement historique vers le rapport militaire détaillé |
| `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv` | `??` | hotfix index leftover | Matrice DEI 6A.3 | 4 | `DISCARD_AS_REDUNDANT` | autorité existante : `docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv` | NO | 23 lignes de données et 20 colonnes sémantiquement identiques ; seules la mise en forme et l'espacement diffèrent |
| `docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `??` | `BUILDING_PRODUCTION_CANDIDATES` | 8 bâtiments, 24 PM et 6 rejets | 27 | `KEEP_AND_COMMIT` | chemin actuel | YES | Matrice structurée, IDs uniques, décisions et justifications non dupliquées |
| `docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md` | `??` | `INDUSTRIAL_CHAIN_MODEL` | 32 chaînes causales industrielles | 27 | `REVIEW_REQUIRED` | chemin actuel après décontamination | NO | Un brief HOTFIX-5C2E4B2 complet a été inséré entre C01 et ses ressources ; restauration exacte récupérable |
| `docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `??` | `HISTORICAL_RESEARCH` | Synthèse 800-1936 et plan de refonte | 27 | `REVIEW_REQUIRED` | chemin actuel après revue des citations | NO | Contenu conceptuel riche et unique, mais ses références Sxx dépendent d'une bibliographie dont les associations source-sujet ne sont pas fiables |
| `docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `??` | `INNOVATION_DATABASE` | Base de 130 innovations | 27 | `REVIEW_REQUIRED` | chemin actuel après revue des données | NO | Schéma complet sans cellules vides, mais dates/origines/scores sont appliqués par blocs et les IDs de sources tournent mécaniquement avec de nombreux appariements sans rapport |
| `docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `??` | `BIBLIOGRAPHY` | Registre S01-S117 | 27 | `REVIEW_REQUIRED` | chemin actuel après reconstruction bibliographique | NO | 117 poignées reposent sur un petit ensemble de sources répétées ; plusieurs sujets sont manifestement incompatibles avec la source citée |
| `docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv` | `??` | `RESOURCE_CANDIDATES` | 30 biens et ressources scorés | 27 | `KEEP_AND_COMMIT` | chemin actuel | YES | Comparatif de design cohérent, IDs uniques, scores et représentations recommandées |
| `docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `??` | `VANILLA_GAP_ANALYSIS` | Comparaison vanilla/fork datée du 14 juillet 2026 | 27 | `KEEP_AND_COMMIT` | chemin actuel | YES | Instantané utile pour la future refonte ; doit rester présenté comme audit daté, pas comme état courant perpétuel |

La matrice CSV machine-readable associée contient exactement les mêmes 11 décisions.

## 4. Analyse du rapport Maratha CLEANUP-1D

Le document a été produit après le FAIL runtime de CLEANUP-1C. Sa distinction entre **Naval Logistics Center** et **Naval Administration**, son diagnostic de la porte technologique `admiralty` et ses observations sur le recrutement restent historiquement utiles.

Il n'est toutefois pas un rapport final exact pour HEAD : il affirme que la seule correction de dépôt fut l'ajout d'un BOM à `common/character_templates/country_marath.txt`, alors que ce fichier commence actuellement par `23 20 4D`, pas `EF BB BF`. Les rapports suivis [CLEANUP-1D Naval Administration Correction](../cleanup/CLEANUP1D_MARATH_NAVAL_ADMIN_CORRECTION.md) et [CLEANUP-1E Final Acceptance](../cleanup/CLEANUP1E_MARATH_FINAL_ACCEPTANCE.md) documentent le correctif final réel : un grant temporaire d'Admiralty validé par A/B runtime.

Le document non suivi est cité par huit rapports ultérieurs et ne doit donc pas être supprimé silencieusement. Avant commit, il faut lui donner un identifiant non conflictuel, corriger la prétention de BOM et mettre à jour ses huit références.

## 5. Diff sensible CLEANUP-2B3

Le diff suivi contient 31 ajouts et 3 suppressions concentrés en fin de rapport. Il :

- remplace `USER_RUNTIME_REQUIRED = YES` par `NO` ;
- remplace l'autorisation d'un test futur par `SINGLE_FINAL_EUROPE_RUNTIME = COMPLETED` ;
- ajoute un compte rendu daté du 20 janvier 1776 avec fermeture normale ;
- enregistre les PASS de Sakharam, Charlotte, Lucca, Ireland et des résidus de dirigeants ;
- conserve explicitement la limite visuelle sur Karl Wilhelm, la capture Baden ayant montré une autre personne ;
- conclut `CLEANUP2B3_RUNTIME = PASS` sans demander un nouveau test.

Ces lignes ferment une exigence déjà annoncée par la version HEAD et ne changent aucune conclusion gameplay. Verdict secondaire demandé par le brief : `KEEP_MODIFICATION_AND_COMMIT`.

## 6. Reliquats Hotfix `_index`

`_index/README.md` réserve ce dossier aux index globaux actifs. Les deux fichiers audités n'en sont pas.

Pour `army.md`, le [manifeste de réorganisation](../DOCUMENTATION_REORGANIZATION_MANIFEST.csv) mappe l'ancien chemin `_index/army.md` vers `runtime/military/army.md`. La petite note non suivie actuelle n'est pas la copie historique déplacée et n'apporte pas de preuve technique au rapport canonique.

Pour la matrice DEI, `Import-Csv` donne 23 enregistrements et 20 colonnes dans les deux copies. La comparaison champ par champ donne zéro différence. Le hash brut diffère seulement parce que la copie `_index` est un export à colonnes visuellement rembourrées. Les liens actifs de l'index Hotfix et du catalogue pointent déjà vers `global_script/6A01_6A09/`.

Aucune suppression n'est exécutée pendant DOCS-PREPATCH-1. Ces deux chemins sont simplement classés `DOCS_DO_NOT_STAGE`.

## 7. Cartographie et dépendances technologiques

```text
BIBLIOGRAPHY
    -> HISTORICAL_RESEARCH
    -> INNOVATION_DATABASE
INNOVATION_DATABASE
    -> INDUSTRIAL_CHAIN_MODEL
HISTORICAL_RESEARCH + INDUSTRIAL_CHAIN_MODEL
    -> VANILLA_GAP_ANALYSIS
VANILLA_GAP_ANALYSIS
    -> RESOURCE_CANDIDATES
    -> BUILDING_PRODUCTION_CANDIDATES
```

Les fichiers de candidats sont des matrices de design, pas des affirmations d'implémentation. L'analyse des écarts reste pertinente comme instantané daté. Le noyau historique ne doit en revanche pas être promu comme autorité avant réparation de ses sources.

### Contamination prouvée et récupération

Dans `TECH_TREE_INDUSTRIAL_CHAINS.md`, la ligne C01 se termine actuellement par `capital.Tu travailles...`, puis le brief HOTFIX-5C2E4B2 occupe les lignes 14 à 344. Deux anciens rapports Sepoy enregistrent le hash propre antérieur :

```text
981A0C119D02C5A5F795C41800B678DDBEC9AD91890CDE4588DF36A98D011799
```

Les rapports ultérieurs enregistrent le hash contaminé actuel :

```text
88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410
```

Une simulation en mémoire, sans écriture, prouve la restauration exacte : retirer la sous-chaîne commençant par `Tu travailles dans le mod Victoria 3` et finissant par le dernier `Ne commit pas automatiquement.`, puis retirer le saut de ligne surnuméraire, restitue exactement le hash `981A...`. Cette correction est recommandée dans une phase autorisant l'édition des fichiers technologiques ; elle n'est pas appliquée ici.

### Qualité des sources

La bibliographie contient des associations manifestement erronées, par exemple une page WHO sur la vaccination utilisée pour le télégraphe ou l'acier, et une page UNESCO sur l'imprimerie utilisée pour le moteur Newcomen ou l'adoption de l'électricité. La base de 130 innovations propage ces IDs suivant un cycle mécanique et emploie des plages de dates et origines identiques pour des blocs entiers. Ces fichiers conservent une valeur de structure et d'idéation, mais exigent une revue source par source.

## 8. Références

### Références propres aux rapports Cleanup

`CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md` est cité par :

- `CLEANUP2B1_MAJOR_1776_RULER_RECONSTRUCTION.md`
- `CLEANUP2B2_EUROPE_1776_RULER_RECONSTRUCTION.md`
- `CLEANUP2C0_COMPLETE_NON_EUROPE_ACTIVE_COUNTRY_AUDIT.md`
- `CLEANUP2C1B_RUNTIME_NAMES_TITLES_AND_CHARTERED_COMPANIES_HOTFIX.md`
- `CLEANUP2C1C_CHARTERED_COMPANY_TIBET_AND_TITLE_DUPLICATION_HOTFIX.md`
- `CLEANUP2D0_WORLD_MILITARY_NAVAL_1776_BASELINE_AUDIT.md`
- `CLEANUP2D2_V3_HISTORICAL_CONVERSION_AND_GLOBAL_BALANCE_MODEL.md`
- `CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md`

`CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md` est cité par sept rapports : CLEANUP-2C1B, 2C1C, 2C1, 2D0, 2D2, 2D3A et 2D5.

### Références exactes aux anciens chemins `_index`

Chacun des deux chemins est mentionné dans quatre documents : `DOCUMENTATION_REORGANIZATION_MANIFEST.csv`, CLEANUP-2D0, CLEANUP-2D2 et CLEANUP-2D3A. Le manifeste décrit explicitement un ancien chemin ; les trois rapports CLEANUP sont des instantanés historiques du worktree. Aucun lien de navigation actif ne cible ces reliquats.

### Ensemble commun des 27 références technologiques

Les sept noms de fichiers sont cités ensemble par les mêmes 27 rapports :

- six rapports Cleanup : CLEANUP-1B, CLEANUP-1C, le CLEANUP-1D non suivi, CLEANUP-2C1B, CLEANUP-2D0 et CLEANUP-2D3A ;
- dix-neuf rapports `hotfix/global_script` : 6A6F, 6A6, 6A7F, 6A7, 6A9F, 6A9R, 6A10F, 6A10, 6A11F, 6A11, 6A12F, 6A13F, 6A13, 6A14R, 6A16R, 6A17, 6A18R, 6A18 et 6A19 ;
- deux rapports Sepoy : `HOTFIX_5C2E4C1C_SEPOY_HARNESS_RUNTIME_TEST.md` et `HOTFIX_5C2E4C1C1_SEPOY_HARNESS_BOM_RETEST.md`.

La plupart de ces mentions sont des inventaires de protection/hash, pas des liens sémantiques. Elles prouvent néanmoins l'identité historique du paquet.

## 9. Liens, anciens chemins et chemins Windows

L'audit de tous les liens Markdown sous `docs/` donne :

```text
BROKEN_MARKDOWN_LINKS_BEFORE = 0
FILES_REFERENCED_BY_MARKDOWN_BUT_ABSENT = 0
```

Avant les nouveaux index, 174 occurrences de chemins Windows absolus existent dans 89 fichiers Markdown. Elles sont presque toutes des preuves historiques d'environnement de test. Parmi les 11 reliquats :

- le chemin vanilla dans les rapports CLEANUP-1D et CLEANUP-2B3 est un contexte historique conservé, pas un lien portable ;
- les trois chemins Windows du fichier de chaînes appartiennent au brief HOTFIX contaminant et disparaîtront avec sa future excision.

Les anciens chemins `_index` du manifeste ne doivent pas être réécrits : ils sont les colonnes `old_path` d'une opération historique. Les liens actifs utilisent déjà les destinations canoniques.

Une incohérence de hash supplémentaire est relevée sans correction automatique : `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md:42` contient `88D090A496C1C3DDB8...`, avec un `D` surnuméraire ; le hash historique contaminé attesté est `88D090A496C1C3CDB8...`.

### Corrections nécessaires, par ordre

1. Décontaminer `TECH_TREE_INDUSTRIAL_CHAINS.md` avec la coupe exacte validée par le hash `981A...`.
2. Refaire l'appariement source-sujet de `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md`, puis corriger les IDs `sources` de la base d'innovations.
3. Réviser les dates, origines, scores et niveaux de confiance appliqués par blocs dans la base d'innovations.
4. Revalider ensuite les citations Sxx du rapport historique approfondi.
5. Corriger et renommer le diagnostic Maratha, puis mettre à jour ses huit références.
6. Corriger le hash mal formé de HOTFIX-6A9R dans une phase documentaire autorisant la rectification d'anciens rapports.
7. Après accord utilisateur, retirer les deux reliquats `_index` du futur staging ; aucune réécriture des anciens chemins de manifeste n'est requise.

## 10. Structure documentaire et index

Les zones initialement sans index étaient `docs/reports/cleanup/`, `docs/reports/release/`, `docs/research/`, `docs/research/military/`, `docs/research/economy/` et `docs/research/technology/`. Elles possèdent maintenant un README d'entrée. `docs/README.md`, `docs/reports/README.md`, `docs/reports/INDEX.md` et le README Hotfix ont été raccordés à cette structure.

README créés :

- `docs/reports/cleanup/README.md`
- `docs/reports/release/README.md`
- `docs/research/README.md`
- `docs/research/military/README.md`
- `docs/research/economy/README.md`
- `docs/research/technology/README.md`

README modifiés :

- `docs/README.md`
- `docs/reports/README.md`
- `docs/reports/hotfix/README.md`

L'index non-README `docs/reports/INDEX.md` a également été complété.

## 11. Plan exact de staging futur

Ce plan décrit l'état documentaire ; aucune commande `git add` n'a été exécutée. Les fichiers de la liste A sont approuvés, mais le commit documentaire global doit attendre la résolution de la liste B afin de ne pas publier un index pointant vers un paquet incomplet.

### A. DOCS_READY_TO_STAGE

- `docs/README.md`
- `docs/reports/README.md`
- `docs/reports/INDEX.md`
- `docs/reports/cleanup/README.md`
- `docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md`
- `docs/reports/hotfix/README.md`
- `docs/reports/release/README.md`
- `docs/reports/release/DOCS_PREPATCH1_DOCUMENTATION_CLEANUP_AUDIT.md`
- `docs/reports/release/DOCS_PREPATCH1_LEFTOVER_FILE_DECISIONS.csv`
- `docs/research/README.md`
- `docs/research/military/README.md`
- `docs/research/economy/README.md`
- `docs/research/technology/README.md`
- `docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv`
- `docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv`
- `docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md`

### B. DOCS_NEED_USER_DECISION

- `docs/reports/cleanup/CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv`
- `docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md`

### C. DOCS_DO_NOT_STAGE

- `docs/reports/hotfix/_index/army.md`
- `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv`

## 12. Protections et validation finale

La phase n'a modifié aucun fichier sous `common/`, `events/`, `map_data/`, `localization/` ou `gfx/`. L'empreinte SHA-256 de l'arbre gameplay complet est comparée au snapshot initial dans la validation finale.

```text
PRE_GAMEPLAY_FILE_COUNT = 877
POST_GAMEPLAY_FILE_COUNT = 877
PRE_GAMEPLAY_TREE_SHA256 = 198176EB7B29D694B15D3195C37A24C644897BF68747B6485507B7DAC2AB1878
POST_GAMEPLAY_TREE_SHA256 = 198176EB7B29D694B15D3195C37A24C644897BF68747B6485507B7DAC2AB1878
GAMEPLAY_FILES_CHANGED_BY_DOCS_PREPATCH_1 = 0
TECHNOLOGY_GAMEPLAY_FILES_CHANGED = 0
MILITARY_FILES_CHANGED = 0
ECONOMY_GAMEPLAY_FILES_CHANGED = 0
BROKEN_LINKS_INTRODUCED = 0
STAGED_FILES = 0
VICTORIA_3_LAUNCHED = NO
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
```

Les valeurs de clôture protégées restent celles des rapports finaux, sans réexécution ni modification de validateur :

```text
LAND_FORMATIONS = 214
GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214
FLEETS = 41
NAVAL_UNITS = 370
FINAL_FIXED_HISTORICAL_ADMIRALS = 26

GEN_POPULATION = 510000
GEN_TRADE_CENTER = 6
VEN_TRADE_CENTER = 8
VEN_ISTRIA_TRADE_CENTER = 3
RIALTO_WORKFORCE = 700
SAN_GIORGIO_WORKFORCE = 600
```
