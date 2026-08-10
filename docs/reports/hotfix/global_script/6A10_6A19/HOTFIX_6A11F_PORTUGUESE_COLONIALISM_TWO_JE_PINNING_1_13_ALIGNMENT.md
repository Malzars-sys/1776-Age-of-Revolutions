# HOTFIX-6A.11F — Alignement Victoria 3 1.13 de deux pinning du colonialisme portugais

Date : 30 juillet 2026 — runtime humain effectué le 29 juillet 2026  
Branche : `hotfix-dlc-audit`  
HEAD initial : `a4716fd` — `Select Portuguese colonialism journal entry pinning alignment`  
HEAD final : `a4716fd` — aucun commit créé

## 1. État de la phase

Les deux substitutions d'API autorisées sont appliquées. Les contrôles
statiques et le runtime humain passent. Les nouveaux logs confirment la
disparition des deux diagnostics ciblés. Les anomalies adjacentes observées
sont documentées sans être corrigées.

`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_STATIC_PASS`  
`PORTUGUESE_COLONIALISM_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`  
`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_RUNTIME_PASS`  
`PORTUGUESE_COLONIALISM_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`  
`PORTUGUESE_COLONIALISM_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`  
`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`  
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| Racine | fork exact |
| Branche | `hotfix-dlc-audit` |
| Rapport 6A.11 dans `HEAD` | PASS |
| Quatre verdicts d'entrée dans `HEAD` | PASS |
| 6A.11 commitée manuellement | PASS, commit `a4716fd` |
| Worktree suivi initial | propre |
| Index staged initial | vide |
| Non-suivis initiaux | uniquement `bject` et `docs/research/technology/` |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Victoria 3, `dowser`, Paradox | aucun processus |
| `git diff --check` initial | propre |

État Git initial :

```txt
?? bject
?? docs/research/technology/
```

Aucune commande Git destructive, aucun accès au contenu du stash, aucun
commit, aucun lancement ou pilotage du jeu n'a été effectué.

## 3. Sources lues

Ont été lus intégralement :

- les rapports 6A.11, 6A.10F et 6A.10;
- la roadmap et les deux CSV canoniques;
- les versions fork, source hotfix et vanilla du fichier cible;
- les localisations vanilla anglaise et française IP4;
- `debug.1.log`, `debug.2.log`, `debug.3.log`, `debug.log`, `error.log`,
  `game.log` et `system.log`.

La source hotfix et vanilla sont restées strictement en lecture seule.

## 4. Hashes trois voies

| Preuve | SHA-256 initial | État |
| --- | --- | --- |
| Fork cible | `6FEF16A90E2E133CC82A912F40944E50E26B65FD524B5898086CF47557DA2894` | PASS |
| Source hotfix | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` | PASS |
| Vanilla 1.13 | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` | PASS |
| Fork attendu après correction | `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20` | atteint |

Source et vanilla utilisent exactement
`should_be_pinned_by_default_uninvolved_or_context = yes` dans les deux objets.
Leurs différences globales de hash ne sont pas importées.

## 5. Hashes protégés

| Élément | SHA-256 | État |
| --- | --- | --- |
| BIC | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | PASS |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` | PASS |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` | PASS |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` | PASS |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` | PASS |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` | PASS |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` | PASS |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` | PASS |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` | PASS |

## 6. Snapshot avant correction

| Ligne initiale | Objet | Propriété |
| ---: | --- | --- |
| 6 | `je_portuguese_colonialism` | `should_be_pinned_by_default = yes` |
| 181 | `je_the_pink_map` | `should_be_pinned_by_default = yes` |

Snapshot structurel :

- ancienne propriété : exactement 2;
- propriété moderne : 0;
- objets racine : exactement les deux objets attendus;
- accolades : `95/95`;
- encodage : UTF-8 avec BOM `EF BB BF`;
- fins de ligne : 305 LF, zéro CRLF;
- saut final : présent.

Contexte préservé dans les deux objets :

```txt
	group = je_group_historical_content
	icon = "gfx/interface/icons/event_icons/event_military.dds"

	should_be_pinned_by_default = yes
	transferable = no
	weight = 10000
```

```txt
	group = je_group_historical_content
	icon = "gfx/interface/icons/event_icons/event_map.dds"

	should_be_pinned_by_default = yes
	transferable = no
	weight = 10000
```

Baseline des logs 6A.10F avant correction : 376 diagnostics globaux dans 141
fichiers, dont 2 dans le fichier cible.

## 7. Deux substitutions exactes

Hunk 1, `je_portuguese_colonialism`, ancienne ligne 6 :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Hunk 2, `je_the_pink_map`, ancienne ligne 181 :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Le diff gameplay contient exactement un fichier, deux objets, deux hunks
unifiés, deux suppressions et deux additions.

## 8. Snapshot après correction

| Ligne | Objet | Propriété |
| ---: | --- | --- |
| 6 | `je_portuguese_colonialism` | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| 181 | `je_the_pink_map` | `should_be_pinned_by_default_uninvolved_or_context = yes` |

Résultat :

- ancienne propriété : `2 → 0`;
- propriété moderne : `0 → 2`;
- hash final :
  `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`;
- accolades : `95/95`;
- BOM UTF-8, 305 LF, zéro CRLF et saut final préservés;
- aucune ligne adjacente modifiée.

## 9. Exclusions adjacentes

N'ont pas été importés depuis la source :

- `region_equatorial_africa` et `region_east_africa`;
- le filtre de culture portugaise;
- `geographic_region_iberia_old`;
- la prise en charge de `c:IBE`;
- commentaires, espaces ou reformattage adjacents.

Aucun scope, trigger, rôle, tooltip, visibilité, DLC, géographie, poids,
transfert, progression, condition, localisation ou autre journal entry n'a été
modifié.

## 10. Localisations

Les quatre clés nécessaires existent dans les fichiers vanilla anglais et
français `ip4_portuguese_colonialism` :

- `je_portuguese_colonialism`;
- `je_portuguese_colonialism_reason`;
- `je_the_pink_map`;
- `je_the_pink_map_reason`.

Aucun fichier de localisation n'est modifié.

## 11. Protections

DEI/VOC, Java, NAVY, MARATH, SAT, KHP, Travancore, Inde/BIC/Sepoy/Bombay,
ADMIN, Japon, Russie, Autriche/Croatie/Suisse, révolutions américaine et
française, technologies, recherche, agriculture, alimentation, industrie,
Tanzimat, Sick Man, Grande Crise orientale, Balkans clos et Romania restent
intacts. Merchant Banking et Navigation Acts n'ont pas été commencés.

BIC conserve :

```txt
activate_law = law_type:law_frontier_colonization
```

`law_colonial_exploitation` n'a pas été restaurée.

## 12. Validations statiques

| Contrôle | Résultat |
| --- | --- |
| Hash cible exact | PASS |
| Ancienne propriété `2 → 0` | PASS |
| Moderne `0 → 2` | PASS |
| Un fichier gameplay | PASS |
| Deux objets | PASS |
| Deux hunks `@@` | PASS |
| Diff `2 additions / 2 suppressions` | PASS |
| Lignes adjacentes inchangées | PASS |
| Accolades `95/95` | PASS |
| BOM, LF et saut final | PASS |
| Quatre clés EN/FR | PASS |
| Source hotfix et vanilla | inchangées |
| BIC, `bject`, sept recherches | inchangés |
| Stash NAVY-3C-3 | intact |
| `git diff --check` | propre |
| Index staged | vide |
| Processus Victoria 3, `dowser`, Paradox | aucun |

## 13. Rollback exact

Dans les deux objets seulement, remplacer :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

par :

```txt
should_be_pinned_by_default = yes
```

Le rollback doit restaurer exactement le hash
`6FEF16A90E2E133CC82A912F40944E50E26B65FD524B5898086CF47557DA2894`.
Aucune commande Git destructive ne doit être employée.

## 14. Fichiers modifiés

Au handoff statique, seuls le fichier gameplay et ce rapport étaient
modifiés. Après le PASS runtime, les quatre documents de navigation autorisés
ont également été finalisés :

1. `common/journal_entries/06_portuguese_colonialism.txt`;
2. ce rapport;
3. `docs/reports/hotfix/INDEX.md`;
4. `HOTFIX_REPORT_INDEX.csv`;
5. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
6. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` est resté inchangé.

État Git au handoff statique :

```txt
 M common/journal_entries/06_portuguese_colonialism.txt
?? bject
?? docs/reports/hotfix/global_script/6A10_6A19/HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

## 15. Fiche et compte rendu runtime humain

La fiche demandait à l'opérateur humain de :

1. lancer le launcher Paradox;
2. confirmer le montage de `1776_Age_of_Revolutions_fork` et `dlc014_ip3`;
3. lancer Victoria 3;
4. commencer une partie neuve avec le Portugal au 1er janvier 1776;
5. confirmer que l'écran de jeu est atteint;
6. ouvrir le journal puis les entrées potentielles;
7. rechercher les entrées liées au colonialisme portugais et à la Carte rose;
8. vérifier titres et raisons lisibles, sans clé brute;
9. vérifier l'absence d'anomalie visible de pinning, visibilité, géographie ou
   progression;
10. avancer jusqu'au 2 janvier 1776;
11. prendre une capture si possible;
12. fermer normalement le jeu puis le launcher;
13. confirmer explicitement leur fermeture.

Ne pas utiliser la console et ne pas forcer l'activation d'une entrée
indisponible.

Compte rendu demandé :

- pays joué;
- dates initiale et finale;
- écran de jeu atteint;
- journal potentiel accessible;
- entrées portugaises visibles ou non;
- titres et raisons lisibles ou non;
- clé brute éventuelle;
- anomalie de pinning, visibilité, géographie ou progression;
- capture éventuelle;
- confirmation explicite que jeu et launcher sont fermés.

Compte rendu reçu :

| Élément | Résultat |
| --- | --- |
| Pays | Portugal |
| Date initiale | 1er janvier 1776 |
| Date finale | 2 janvier 1776 |
| Écran de jeu | atteint |
| Journal potentiel | accessible |
| Entrée ciblée | `Além-mar africain` visible |
| Titre et conditions | lisibles |
| Clé brute | aucune |
| Pinning | aucune anomalie visible |
| Carte rose | non visible au départ; aucune activation forcée |
| Capture | deux captures fournies |
| Jeu et launcher | fermeture explicite confirmée |

La capture détaillée montre aussi une répétition de « Royaume de Portugal »
dans le texte de condition. Elle est séparée du correctif de pinning.

## 16. Nouveaux logs et rotations

La session courante est répartie entre `debug.1.log`, qui contient le
démarrage, le parsing et les montages, et `debug.log`, continuation de la même
session. Les anciennes preuves ont été décalées dans `.2` à `.5`.

| Log courant | SHA-256 | Rôle |
| --- | --- | --- |
| `debug.1.log` | `1F25D03EAE1B45C68A84BE77CC36F8D8F8CCD9F540104CA5D7CE52B1F1C3194B` | démarrage, parser, montages |
| `debug.log` | `31E79BBDA56B49BA16E2F07800D39CB7C579B622FA68E5BB92C67976265B1298` | continuation |
| `error.log` | `1D761021E38CC35578BB273E1DD82E7665D6EE8011F2D25370592FA808D311C8` | erreurs runtime |
| `game.log` | `04C9BC554C4A34D045291D5CD830BBE8D606923AE03F4F71E002202B28550C99` | jeu |
| `system.log` | `CA73FC2FC88D7E720083742B3C673812614065C90C58A808DDB0EDB78D2CF34E` | système |

Rotations historiques identifiées :

| Rotation | SHA-256 |
| --- | --- |
| `debug.2.log` | `72E998A9E079984DB6D93B24F1CD4E6B13F2755FF2640E81BA660A01DE417899` |
| `debug.3.log` | `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` |
| `debug.4.log` | `38B2B29FAD0922C6192B27CB69BC202F0C431F1DC9FDF5427C3835EBFDD75C35` |
| `debug.5.log` | `78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5` |

Montages dans `debug.1.log` :

- ligne 80 : `C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3`;
- ligne 87 : chemin exact de `1776_Age_of_Revolutions_fork`.

## 17. Résultats parser

| Mesure | Avant | Après | Verdict |
| --- | ---: | ---: | --- |
| Diagnostics globaux legacy | 376 | 374 | attendu |
| Fichiers uniques | 141 | 140 | attendu |
| Diagnostics dans le fichier cible | 2 | 0 | PASS |
| Rejets de la propriété moderne cible | 0 | 0 | PASS |

`debug.1.log` porte 373 diagnostics dans 139 fichiers et `debug.log` la
dernière occurrence, dans `99_test_global_je.txt`. Leur somme de session est
donc exactement 374 diagnostics dans 140 fichiers. Les diagnostics Tanzimat
connus restent séparés et inchangés.

## 18. Anomalies adjacentes hors périmètre

L'ouverture de l'entrée potentielle déclenche dans `error.log` :

- 186 occurrences de clé invalide `region_congo`, ligne gameplay 11;
- 186 occurrences de clé invalide `region_zanj`, ligne gameplay 14;
- 373 retours de scope `sr` non défini sur ces deux lignes.

Ces deux régions appartiennent aux différences adjacentes explicitement
exclues de 6A.11F. Elles existaient avant les deux substitutions et leur
correction importerait une dette géographique distincte. La répétition
visuelle de « Royaume de Portugal » constitue de même une anomalie de
texte/tooltip séparée. Aucune de ces anomalies n'est corrigée ou utilisée pour
étendre cette phase.

La géographie et la progression sont donc inchangées par les deux hunks de
pinning, sans prétendre que la dette adjacente préexistante est saine.

## 19. Contrôles finaux

| Contrôle | Résultat |
| --- | --- |
| Un fichier gameplay, deux objets, deux hunks, `2/2` | PASS |
| Hash gameplay cible | PASS |
| Diagnostics ciblés `2 → 0` | PASS |
| Baseline `376/141 → 374/140` | PASS |
| Dette adjacente importée | aucune |
| Source hotfix et vanilla | intactes |
| BIC, `bject`, sept recherches | intacts |
| Stash NAVY-3C-3 | intact |
| CSV | valides |
| `git diff --check` | propre |
| Index staged | vide |
| Processus Victoria 3, `dowser`, Paradox | aucun |
| Interaction Codex avec le jeu | aucune |
| Commit automatique | aucun |
| Phase suivante commencée | non |

État Git final :

```txt
 M common/journal_entries/06_portuguese_colonialism.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A10_6A19/HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

Les six fichiers de phase sont exactement ceux autorisés. Les deux autres
éléments non suivis sont les protections préexistantes autorisées.

## 20. Décision de commit

Le HEAD initial et final reste `a4716fd`. Aucun commit automatique n'est créé.
La décision de commit manuel appartient à l'opérateur. Une sélection
documentaire distincte sera nécessaire après ce commit; elle n'est pas
commencée ici.

## 21. Verdicts finaux

`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_STATIC_PASS`  
`PORTUGUESE_COLONIALISM_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`  
`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_RUNTIME_PASS`  
`PORTUGUESE_COLONIALISM_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`  
`PORTUGUESE_COLONIALISM_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`  
`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`  
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
