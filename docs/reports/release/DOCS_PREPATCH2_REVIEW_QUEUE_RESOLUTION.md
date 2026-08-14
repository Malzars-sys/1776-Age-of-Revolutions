# DOCS-PREPATCH-2 — Resolve Review Queue & Freeze Release Documentation

## 1. Résultat

La file de revue ouverte par DOCS-PREPATCH-1 est résolue. Le diagnostic Maratha possède un identifiant unique et un statut historique explicite, le document Industrial Chains est décontaminé au byte près, les recherches technologiques préliminaires sont conservées sans être promues comme autorités, et les deux reliquats `_index` non suivis ont été retirés.

```text
DOCUMENTATION_FREEZE_READY = YES
DOCS_NEED_USER_DECISION = 0
GAMEPLAY_FILES_CHANGED = 0
STAGED_FILES = 0
```

## 2. Baseline

```text
BRANCH = cleanup-post-release
HEAD = 2c2ae7d2e4acf010dc5a3e75134ff038110cc33c
DOCS_PREPATCH1 = PASS
PRE_GAMEPLAY_FILE_COUNT = 877
PRE_GAMEPLAY_TREE_SHA256 = 7319D86F6EB2AAB9181BD32A95D8D498FAFE1BDAEF57127EB83FF3E864C0A80F
```

La modification suivie de [CLEANUP-2B3](../cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md) est conservée sans changement supplémentaire. Son verdict reste `KEEP_MODIFICATION_AND_COMMIT`.

## 3. Diagnostic Maratha

Le fichier non suivi conflictuel :

```text
docs/reports/cleanup/CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md
```

a été renommé en :

```text
docs/reports/cleanup/CLEANUP1C1_MARATH_NAVAL_CREW_DIAGNOSTIC.md
```

Le nouveau nom place le diagnostic après le FAIL de CLEANUP-1C et avant la correction canonique CLEANUP-1D. Le document porte maintenant :

```text
STATUS = HISTORICAL_DIAGNOSTIC_SUPPLEMENT
```

Ses observations sur la confusion entre Naval Logistics Center et Naval Administration sont conservées. L'affirmation BOM est corrigée sans réécrire le diagnostic : l'état `EF BB BF` est identifié comme une observation temporaire, tandis que le HEAD courant commence par `23 20 4D`.

Les autorités finales sont explicitement [CLEANUP-1D Naval Administration Correction](../cleanup/CLEANUP1D_MARATH_NAVAL_ADMIN_CORRECTION.md) et [CLEANUP-1E Final Acceptance](../cleanup/CLEANUP1E_MARATH_FINAL_ACCEPTANCE.md). Elles documentent la vraie Administration navale, le grant temporaire d'`admiralty`, le test runtime A/B et la clôture de CLEANUP-1.

### Huit références mises à jour

- `CLEANUP2B1_MAJOR_1776_RULER_RECONSTRUCTION.md`
- `CLEANUP2B2_EUROPE_1776_RULER_RECONSTRUCTION.md`
- `CLEANUP2C0_COMPLETE_NON_EUROPE_ACTIVE_COUNTRY_AUDIT.md`
- `CLEANUP2C1B_RUNTIME_NAMES_TITLES_AND_CHARTERED_COMPANIES_HOTFIX.md`
- `CLEANUP2C1C_CHARTERED_COMPANY_TIBET_AND_TITLE_DUPLICATION_HOTFIX.md`
- `CLEANUP2D0_WORLD_MILITARY_NAVAL_1776_BASELINE_AUDIT.md`
- `CLEANUP2D2_V3_HISTORICAL_CONVERSION_AND_GLOBAL_BALANCE_MODEL.md`
- `CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md`

```text
MARATH_DIAGNOSTIC_CONFLICT = RESOLVED
MARATH_REFERENCE_UPDATES = 8
```

Les deux mentions de l'ancien nom dans les livrables DOCS-PREPATCH-1 restent des preuves historiques de la décision initiale, pas des liens actifs.

## 4. Industrial Chains

La contamination commençait au texte `Tu travailles dans le mod Victoria 3` et finissait au dernier `Ne commit pas automatiquement.` avant les ressources de C01. Seule cette sous-chaîne et le saut de ligne surnuméraire démontré ont été retirés. Les 32 chaînes n'ont pas été reformulées.

```text
INDUSTRIAL_CHAINS_SHA256_BEFORE = 88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410
INTERMEDIATE_SHA256_MISSING_FINAL_LF = EEA138A0F0786DC7119E38480C28358EE19CDCCDE638771C0C0F94D16D6EC4F1
AUTHORIZED_FINAL_LF_BYTES_APPENDED = 1
INDUSTRIAL_CHAINS_SHA256_AFTER = 981A0C119D02C5A5F795C41800B678DDBEC9AD91890CDE4588DF36A98D011799
HOTFIX_CONTAMINATION_MARKERS_REMAINING = 0
```

Une simulation en lecture seule a prouvé qu'un unique octet `0A` final transformait le hash intermédiaire en hash attendu. Après autorisation explicite de reprise, exactement cet octet a été ajouté. Le fichier final fait 18 077 octets et correspond au hash propre enregistré par les anciens rapports Sepoy.

```text
INDUSTRIAL_CHAINS_CONTAMINATION = REMOVED
INDUSTRIAL_CHAINS_SHA256 = 981A0C119D02C5A5F795C41800B678DDBEC9AD91890CDE4588DF36A98D011799
```

## 5. Recherches technologiques préliminaires

La doctrine de reprise demande de minimiser les changements avant release. Les trois fichiers suivants restent donc à leur emplacement actuel ; ils n'ont été ni déplacés ni modifiés :

- `docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv`
- `docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md`

Le [README technologique](../../research/technology/README.md) les classe désormais `PRELIMINARY / UNVERIFIED` et avertit explicitement que leurs citations, mappings de sources, dates, origines et niveaux de confiance ne sont pas validés. Ils sont conservés uniquement pour leur structure et leur idéation.

Le patch de release ne dépend d'aucune donnée provenant de ces trois fichiers.

```text
UNVERIFIED_TECH_RESEARCH_FILES = 3
UNVERIFIED_TECH_DRAFTS_MOVED = 0
TECH_RESEARCH_USED_BY_RELEASE_GAMEPLAY = 0
```

## 6. Reliquats `_index`

Avant suppression, les autorités ont été reconfirmées :

- army : `docs/reports/hotfix/runtime/military/army.md`, fichier canonique existant de 9 940 octets et destination attestée par le manifeste de réorganisation ;
- DEI : `docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv`, 23 enregistrements et zéro différence champ par champ avec le reliquat.

Les deux copies non suivies suivantes ont ensuite été retirées :

- `docs/reports/hotfix/_index/army.md`
- `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv`

Les anciennes mentions `old_path` dans les manifestes et instantanés historiques ne sont pas falsifiées. Aucun lien actif ne ciblait les copies retirées.

```text
REDUNDANT_INDEX_LEFTOVERS = 0
```

## 7. Hash HOTFIX-6A9R

Le rapport `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md` contenait une seule occurrence du hash mal formé `88D090A496C1C3DDB8...`. Vingt occurrences documentaires indépendantes attestent le hash historique correct `88D090A496C1C3CDB8...`.

Un seul caractère a été corrigé dans la ligne concernée. Ce hash reste une preuve de l'état contaminé historique ; il n'est pas remplacé par le nouveau hash `981A...`.

```text
HOTFIX_6A9R_MALFORMED_HASH = CORRECTED
```

## 8. Index documentaires

Les index créés par DOCS-PREPATCH-1 sont conservés. Les changements de phase sont limités à :

- ajout de CLEANUP-1C.1 dans l'index Cleanup et clarification de l'autorité CLEANUP-1D/1E ;
- classement technologique entre recherche de design utilisable et matériel préliminaire/non vérifié ;
- ajout des deux livrables DOCS-PREPATCH-2 dans l'index release ;
- remplacement, dans l'index de recherche, du renvoi vers la file de revue par le présent rapport de gel.

Les trois fichiers préliminaires restant en place, aucun ancien chemin technologique actif n'a besoin d'être réécrit.

## 9. Validation des liens

Tous les liens Markdown sous `docs/` ont été résolus relativement à leur document source. Les chemins historiques conservés dans du texte ou des colonnes `old_path` ne sont pas traités comme des liens actifs.

```text
BROKEN_MARKDOWN_LINKS = 0
FILES_REFERENCED_BY_MARKDOWN_BUT_ABSENT = 0
```

## 10. Protection gameplay

La même procédure d'empreinte trie les fichiers de `common/`, `events/`, `map_data/`, `localization/` et `gfx/`, associe chaque chemin relatif à son SHA-256, puis hash le manifeste résultant.

```text
POST_GAMEPLAY_FILE_COUNT = 877
POST_GAMEPLAY_TREE_SHA256 = 7319D86F6EB2AAB9181BD32A95D8D498FAFE1BDAEF57127EB83FF3E864C0A80F
GAMEPLAY_TREE_CHANGED = 0
GAMEPLAY_FILES_CHANGED = 0
TECHNOLOGY_GAMEPLAY_FILES_CHANGED = 0
```

Aucun fichier de technologie Victoria 3 n'a été modifié. Les seuls changements liés au sujet technology sont documentaires sous `docs/research/technology/`.

## 11. Liste exacte des fichiers documentaires à stage

Aucun de ces fichiers n'est stagé par DOCS-PREPATCH-2. La future commande de staging devra nommer explicitement les 32 chemins suivants :

- `docs/README.md`
- `docs/reports/INDEX.md`
- `docs/reports/README.md`
- `docs/reports/cleanup/README.md`
- `docs/reports/cleanup/CLEANUP1C1_MARATH_NAVAL_CREW_DIAGNOSTIC.md`
- `docs/reports/cleanup/CLEANUP2B1_MAJOR_1776_RULER_RECONSTRUCTION.md`
- `docs/reports/cleanup/CLEANUP2B2_EUROPE_1776_RULER_RECONSTRUCTION.md`
- `docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md`
- `docs/reports/cleanup/CLEANUP2C0_COMPLETE_NON_EUROPE_ACTIVE_COUNTRY_AUDIT.md`
- `docs/reports/cleanup/CLEANUP2C1B_RUNTIME_NAMES_TITLES_AND_CHARTERED_COMPANIES_HOTFIX.md`
- `docs/reports/cleanup/CLEANUP2C1C_CHARTERED_COMPANY_TIBET_AND_TITLE_DUPLICATION_HOTFIX.md`
- `docs/reports/cleanup/CLEANUP2D0_WORLD_MILITARY_NAVAL_1776_BASELINE_AUDIT.md`
- `docs/reports/cleanup/CLEANUP2D2_V3_HISTORICAL_CONVERSION_AND_GLOBAL_BALANCE_MODEL.md`
- `docs/reports/cleanup/CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md`
- `docs/reports/hotfix/README.md`
- `docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md`
- `docs/reports/release/README.md`
- `docs/reports/release/DOCS_PREPATCH1_DOCUMENTATION_CLEANUP_AUDIT.md`
- `docs/reports/release/DOCS_PREPATCH1_LEFTOVER_FILE_DECISIONS.csv`
- `docs/reports/release/DOCS_PREPATCH2_REVIEW_QUEUE_RESOLUTION.md`
- `docs/reports/release/DOCS_PREPATCH2_FINAL_DOCUMENTATION_MANIFEST.csv`
- `docs/research/README.md`
- `docs/research/economy/README.md`
- `docs/research/military/README.md`
- `docs/research/technology/README.md`
- `docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md`
- `docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv`
- `docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md`
- `docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv`
- `docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md`

## 12. Dette documentaire explicitement différée

- reconstruire et valider source par source la bibliographie technologique ;
- revoir les dates, origines, scores et mappings Sxx de la base d'innovations ;
- revalider les conclusions historiques du rapport approfondi ;
- confirmer les conclusions d'Industrial Chains qui dépendent de ces sources ;
- concevoir et implémenter la future refonte Tech Tree dans une phase gameplay distincte.

Cette dette est hors patch et ne bloque pas la release. Les livrables DOCS-PREPATCH-1 restent des rapports historiques : leurs anciennes classifications, anciens chemins et hashes ne sont pas réécrits pour simuler l'état final.

## 13. Git et verdict final

```text
 M docs/README.md
 M docs/reports/INDEX.md
 M docs/reports/README.md
 M docs/reports/cleanup/CLEANUP2B1_MAJOR_1776_RULER_RECONSTRUCTION.md
 M docs/reports/cleanup/CLEANUP2B2_EUROPE_1776_RULER_RECONSTRUCTION.md
 M docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md
 M docs/reports/cleanup/CLEANUP2C0_COMPLETE_NON_EUROPE_ACTIVE_COUNTRY_AUDIT.md
 M docs/reports/cleanup/CLEANUP2C1B_RUNTIME_NAMES_TITLES_AND_CHARTERED_COMPANIES_HOTFIX.md
 M docs/reports/cleanup/CLEANUP2C1C_CHARTERED_COMPANY_TIBET_AND_TITLE_DUPLICATION_HOTFIX.md
 M docs/reports/cleanup/CLEANUP2D0_WORLD_MILITARY_NAVAL_1776_BASELINE_AUDIT.md
 M docs/reports/cleanup/CLEANUP2D2_V3_HISTORICAL_CONVERSION_AND_GLOBAL_BALANCE_MODEL.md
 M docs/reports/cleanup/CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md
 M docs/reports/hotfix/README.md
 M docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md
?? docs/reports/cleanup/CLEANUP1C1_MARATH_NAVAL_CREW_DIAGNOSTIC.md
?? docs/reports/cleanup/README.md
?? docs/reports/release/DOCS_PREPATCH1_DOCUMENTATION_CLEANUP_AUDIT.md
?? docs/reports/release/DOCS_PREPATCH1_LEFTOVER_FILE_DECISIONS.csv
?? docs/reports/release/DOCS_PREPATCH2_FINAL_DOCUMENTATION_MANIFEST.csv
?? docs/reports/release/DOCS_PREPATCH2_REVIEW_QUEUE_RESOLUTION.md
?? docs/reports/release/README.md
?? docs/research/README.md
?? docs/research/economy/README.md
?? docs/research/military/README.md
?? docs/research/technology/README.md
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

```text
git diff --check = PASS
STAGED_FILES = 0
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
VICTORIA_3_LAUNCHED = NO

DOCS_NEED_USER_DECISION = 0
MARATH_DIAGNOSTIC_CONFLICT = RESOLVED
MARATH_REFERENCE_UPDATES = 8
INDUSTRIAL_CHAINS_CONTAMINATION = REMOVED
UNVERIFIED_TECH_RESEARCH_FILES = 3
REDUNDANT_INDEX_LEFTOVERS = 0
BROKEN_MARKDOWN_LINKS = 0
GAMEPLAY_FILES_CHANGED = 0
TECHNOLOGY_GAMEPLAY_FILES_CHANGED = 0
DOCUMENTATION_FREEZE_READY = YES
```
