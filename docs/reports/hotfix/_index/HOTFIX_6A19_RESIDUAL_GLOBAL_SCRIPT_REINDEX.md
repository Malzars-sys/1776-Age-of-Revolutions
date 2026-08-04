
# HOTFIX-6A.19 — Réindexation résiduelle des scripts globaux

Date : 4 août 2026
Branche : `hotfix-dlc-audit`
HEAD d’entrée réel : `9a3363deb5886b523ae227dd9f721d35bae4c3a4` — `Format hotfix report dependency map`
HEAD fonctionnel précédent : `044656e` — `Defer Egyptian crisis runtime to Middle East flavor`

## 1. Résultat

La phase documentaire 6A.19 est terminée. Les 161 lignes historiques ont été
reconstruites dans les trois arbres, rapprochées des phases 6A.4 à 6A.18Q3 et
reclassées dans l’unique registre canonique
`HOTFIX_MERGE_REMAINING_WORK.csv`. Aucun fichier gameplay n’a changé et aucun
runtime n’a été lancé.

Le HEAD diffère du HEAD déclaré par le prompt parce que l’opérateur a demandé,
avant la reprise, le commit isolé du reformatage sémantiquement neutre de
`HOTFIX_REPORT_DEPENDENCY_MAP.csv`. Le commit `9a3363d` contient
`044656e` et `78e562f` dans son ascendance. Cette instruction humaine
explicite autorise la reprise sans réécrire l’histoire Git.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| racine Git | chemin de travail attendu |
| branche | `hotfix-dlc-audit` |
| HEAD | `9a3363d`, dérogation opérateur documentée |
| ancêtre Q3 | `044656e` présent |
| ancêtre VOC | `78e562f` présent |
| changements suivis avant 6A.19 | aucun |
| index Git | vide |
| `git diff --check` | propre |
| Victoria 3 / Dowser / launcher Paradox | aucun processus |
| stash NAVY-3C-3 | intact, `518df704fa14599c0f254fae13859210663dd976` |
| runtime 6A.19 | aucun |

Les seuls non-suivis sont restés protégés et n’ont pas été ouverts :

- `bject` ;
- `docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` ;
- `docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md` ;
- `docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` ;
- `docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` ;
- `docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` ;
- `docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv` ;
- `docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md`.

## 3. Documents lus

Documents de navigation et registres :

- `docs/reports/hotfix/INDEX.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_MERGE_REMAINING_WORK.csv` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Rapports de sélection, audit et correction :

```text
HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md
HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md
HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md
HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md
HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md
HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md
HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md
HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md
HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md
HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md
HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT.md
HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md
HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT.md
HOTFIX_6A14H_HBC_DOUBLE_DEFINITION_RESOLUTION_AUDIT.md
HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT.md
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT.md
HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT.md
HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT.md
HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT.md
HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION.md
HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT.md
HOTFIX_6A18F1_RETIRE_OBSOLETE_DECLARED_INTEREST_HISTORY.md
HOTFIX_6A18F2_EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_ALIGNMENT.md
HOTFIX_6A18R3_INDOCHINA_LEGACY_INTEREST_LOGIC_1_13_AUDIT.md
HOTFIX_6A18Q2_COMBINED_DECLARED_INTEREST_EVENT_RUNTIME_QA.md
HOTFIX_6A18Q3_EGYPTIAN_CRISIS_RUNTIME_DEFERRAL.md
HOTFIX_MINI_VOC_COMPANY_ICON.md
```

## 4. Méthode trois voies

Pour chaque chemin historique, la présence, la taille et le SHA-256 ont été
recalculés dans le fork, la source hotfix et la vanilla 1.13. Les différences
larges ont ensuite été relues par objet ou hunk ; l’égalité de fichier n’a
jamais été utilisée pour autoriser un remplacement global.

| Relation brute actuelle | Lignes |
| --- | ---: |
| fork, source et vanilla tous différents | 114 |
| deux fichiers custom présents et différents | 17 |
| fork absent, source et vanilla présents mais différents | 10 |
| fork égal à la source | 2 |
| fork égal à la vanilla | 15 |
| fichier custom présent seulement dans la source | 3 |
| **Total** | **161** |

Ces relations sont des preuves de provenance, pas des classifications de merge.
Chaque ligne conserve sa relation dans `difference_type` et sa disposition
6A.19 dans `notes`.

## 5. Diagnostics courants et rotations

Les fichiers `debug*.log`, `error*.log` et `game*.log` ont été lus sans
produire de nouvelle génération. La clé de déduplication est :

```text
génération + message normalisé + chemin + ligne
```

Les diagnostics script attribuables aux 161 lignes apparaissent dans
`debug*.log`. Aucun diagnostic supplémentaire de ce format et de ce
périmètre n’a été extrait des générations `error*.log` ou `game*.log`.

| Génération | Horodatage | brut | dédupliqué | chemins |
| --- | --- | ---: | ---: | ---: |
| `debug.log` | 2026-08-04 19:43:32 | 107 | 107 | 19 |
| `debug.1.log` | 2026-08-04 19:38:06 | 74 | 74 | 19 |
| `debug.2.log` | 2026-08-04 19:28:08 | 0 | 0 | 0 |
| `debug.3.log` | 2026-08-04 19:27:30 | 181 | 181 | 38 |
| `debug.4.log` | 2026-08-04 19:11:15 | 0 | 0 | 0 |
| `debug.5.log` | 2026-08-04 19:08:14 | 181 | 181 | 38 |

SHA-256 courant : `debug.log =
6D9F5BDDB58E9C151C411F4A5192961786E1BF88C51B1043B4A05BE470B5BBF6`,
`error.log =
98944B1D99C4FC25AC5A17C2D0C5EFDD12C4CCE3F6D1AC9AF0739E24B713AED8`,
`game.log =
E0736653DA140BEC97C369C5A8CE9C623F20D3BFFF26FE315866DC5E012169A4`.

Le courant contient notamment 52 pinning obsolètes dans le tutoriel, 9
diagnostics dans le fichier custom Pologne-Lituanie, 7 diagnostics mixtes en
Corée, 6 au Portugal, 4 en Afrique espagnole, 3 en Grande Colombie et 2 dans
chacun des fichiers Pologne, Printemps des peuples, Afghanistan et Question
d’Orient. Les diagnostics Canada, Fascisme et unification allemande ne
subsistent que dans les rotations disponibles. L’absence courante n’est pas
interprétée comme une validation fonctionnelle.

## 6. Reclassification

| Classification | historique | 6A.19 |
| --- | ---: | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 | 0 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 15 | 13 |
| `ALREADY_MERGED` | 19 | 23 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 | 2 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 | 14 |
| `PROTECTED_CONCURRENT_WORK` | 19 | 20 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 | 86 |
| **Total** | **161** | **161** |

Changements expliqués :

- GEN et VEN passent de delta requis à intégré après 6A.13F.
- GBR passe en travail protégé à cause des collisions NAVY/BIC ; HBC, NBS,
  ONT et ORA passent au backlog de design HBC/Navigation Acts.
- Les alignements Balkan, Yougoslavie, Italie, Grèce, Grande crise orientale,
  Sick Man, Roumanie, colonialisme portugais et Coup passent à intégrés.
- `07_poland_lithuania_mod.txt`, auparavant considéré fusionné avec la
  source, passe à alignement 1.13 requis : source et fork conservent huit clés
  obsolètes et le log courant en rejette huit, plus deux autres API.
- Imperialism of Promise passe d’alignement générique à inconnu : son pinning
  est invalide, mais les hunks de vivier et de rôles restent dépendants d’une
  décision de design déjà exclue.
- `00_interests.txt` passe d’inconnu à obsolète après F1/Q2.
- `egyptian_crisis_events.txt` passe d’inconnu à intégré pour le merge, avec
  le statut secondaire `FLAVOR_EXTENSION_ONLY` et aucun succès runtime
  inventé.
- les trois overrides australiens restent des divergences 1776 volontaires ;
  les dix refontes Amérique/France/technologie restent des backlogs.

Les 87 groupes historiquement inconnus ont tous reçu une revue individuelle
dans le registre. Deux en sortent : l’historique des intérêts devient obsolète
et la crise égyptienne devient intégrée avec report flavor. Les 85 autres
restent inconnus faute de delta objet par objet prouvé. Imperialism of Promise
entre parallèlement dans cette catégorie, d’où le total courant de 86.

## 7. Matrice P0/P1

| ID | fichiers | objet/lignes | fonction | relation 3 voies | avant | 6A.19 | preuve statique | runtime courant | rotation seule | gravité | statut merge | atomicité | dépendances | protection | runtime futur | décision humaine | confiance | traitement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| POL-BASE-2 | `00_poland.txt` | `je_christ_of_nations` 59 ; `je_poland_lithuania` 131 | pinning | tous différents ; source/vanilla convergent sur la clé | VAI | VAI | 2 anciennes clés contre 2 nouvelles | 2 rejets | non | moyenne | bloquant bornable | un fichier, deux objets | logique géographique divergente | non | non pour audit | non | haute | **audit 6A.20** |
| POL-CUSTOM-9 | `07_poland_lithuania_mod.txt` | 8 JE, lignes 238–596 | pinning + API custom | fork/source différents ; vanilla absente | merged | VAI | 8 anciennes clés dans fork et source | 9 rejets | non | moyenne | requis mais large | huit objets | contenu PLC custom | non | après correction | oui par objet | haute | audit futur séparé |
| TUTORIAL-52 | `00_tutorial.txt` | 52 lignes | tutoriel/JE | tous différents | VAI | VAI | 52 clés obsolètes | 52 rejets | non | moyenne | requis | trop large | nombreux objets | non | ciblé ultérieur | non sur API | haute | scinder |
| KOR-7 | `03_korea.txt` | 3 pinning + 4 `is_ruler` | chaîne coréenne | tous différents | VAI | VAI | API 1.13 disponible | 7 rejets | non | élevée | requis | mixte | rôles et événements | Japon exclu adjacent | après correction | oui pour rôles | haute | audit borné ultérieur |
| POR-6 | `06_portugal_politics.txt` | 6 JE | pinning | tous différents | VAI | VAI | 6 clés obsolètes | 6 rejets | non | moyenne | requis | six objets | politique portugaise | non | après correction | non sur API | haute | scinder |
| SPA-4 | `06_spanish_africa.txt` | 4 JE | pinning | tous différents | VAI | VAI | 4 clés obsolètes | 4 rejets | non | moyenne | requis | quatre objets | flavor ibérique | non | après correction | non sur API | haute | scinder |
| GCO-3 | `02_gran_colombia.txt` | lignes 72/135/229 | pinning | tous différents | VAI | VAI | 3 clés obsolètes | 3 rejets | non | moyenne | requis | trois objets | Amérique adjacente | refonte Amérique exclue | après correction | oui sur frontière | haute | ne pas sélectionner |
| PPS-2 | `00_peoples_springtime_je.txt` | lignes 324/478 | pinning | tous différents | VAI | VAI | 2 clés obsolètes | 2 rejets | non | moyenne | requis | deux objets | France/Printemps | refonte France exclue | après correction | oui sur frontière | haute | ne pas sélectionner |
| AFG-2 | `03_afghanistan.txt` | lignes 2/1826 | pinning | tous différents | VAI | VAI | 2 clés obsolètes | 2 rejets | non | moyenne | requis | deux objets éloignés | grand fichier | non | après correction | non sur API | haute | audit préalable |
| EASTQ-2 | `05_eastern_question.txt` | lignes 130/137 | pinning | tous différents | VAI | VAI | 2 clés obsolètes | 2 rejets | non | moyenne | requis | proche | Tanzimat adjacent | Tanzimat exclu | après correction | oui sur séparation | haute | différer |
| CAF-GER | 3 fichiers | 4/3/5 pinning | JE nationales | tous différents | VAI | VAI | source/vanilla convergent | aucun | oui, 36 cumuls générationnels | moyenne | requis | fichier par fichier | chaînes nationales | non | après correction | non sur API | moyenne | après les erreurs courantes |
| HBC-NAV | 4 pays + GBR | lois initiales | Navigation Acts | tous différents | required | backlog/protégé | audits 6A.14R/H | aucun ciblé | historique | élevée | non bloquant 6A.19 | non atomique | HBC, GBR, BIC, NAVY | oui | après design | **oui** | haute | backlog séparé |
| IOP | `04_imperialism_of_promise.txt` | ligne 140 + rôles/vivier | disponibilité JE | tous différents | VAI | inconnu | pinning invalide, design mixte | 1 rejet | anciens rôles | moyenne | bloc clos | hunk mixte | BIC/Inde | oui | après décision | **oui** | haute | ne pas rouvrir |
| COUP-EVT | deux fichiers événement | 16 API historiques | Coup | tous différents | inconnu | inconnu | audit 6A.16R | aucun | oui | inconnue | bloc clos | sept objets | lobby/sponsor | bloc clos | non défini | oui | haute | ne pas rouvrir |
| AM-FR | 10 lignes | JE/événements | refontes flavor | relations mixtes | backlog | backlog | deltas présents | 12 rejets courants sur 4 fichiers | oui ailleurs | variable | non bloquant | large | refontes | oui | flavor | oui | haute | post-merge |
| PROTECTED | fichiers Autriche/Metternich/Inde | plusieurs lignes | contenus concurrents | relations mixtes | protégé | protégé | délimitation 6A.4+ | 5 rejets courants | oui ailleurs | variable | hors merge auto | non | NAVY/Inde/Autriche | oui | séparé | oui | haute | préserver |

La priorité ne suit pas automatiquement la gravité. POL-BASE-2 est préféré à
des chaînes plus visibles parce que son invalidité courante est prouvée, son
périmètre est petit et l’audit peut séparer sans risque le pinning de la
géographie 1776.

## 8. Périmètres explicitement exclus

NAVY, ADMIN, MARATH/SAT/KHP, stash NAVY-3C-3, BIC, hunks GBR croisant
NAVY/BIC, Inde, Sepoy, Bombay, Travancore, localisations françaises massives,
recherche technologique, sauvegardes, descripteurs, HBC/Navigation Acts, Coup
clos, Imperialism of Promise, Tanzimat, Merchant Banking, Japon, Mamluk Iraq,
DEI/VOC, intérêts déclarés, refontes Amérique/France/technologies.

La loi BIC `law_frontier_colonization` n’a pas été touchée et
`law_colonial_exploitation` n’a pas été restaurée.

## 9. Prochaine phase sélectionnée

`HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT` est sélectionnée,
sans être commencée.

- type : audit statique et fonctionnel ;
- fichier : `common/journal_entries/00_poland.txt` ;
- SHA-256 fork : `DD2696FACF3D7988A933E7541D00D989E3E4B813574493D28A2BCA7AA1DACFD0` ;
- SHA-256 source : `9B01C5DBFA033492753278F044DC20BF3C1F1AC8701C95E6AEA51C82B65B930F` ;
- SHA-256 vanilla : `8BF208D5A89595E76131B69D30BD3DE26ECC92A76F623D3040CBC11349B76A78` ;
- objets : `je_christ_of_nations` et `je_poland_lithuania` ;
- cible : deux `should_be_pinned_by_default = yes` rejetés aux lignes 59 et
  131 ;
- preuve : deux diagnostics courants ; source et vanilla utilisent la clé
  1.13 aux deux objets ;
- garde-fou : les hunks géographiques, qui divergent entre les trois arbres,
  sont hors correction automatique ;
- modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé ;
- lancements Victoria 3 minimaux : 0 pour l’audit ;
- toute correction et tout runtime ultérieurs nécessitent une phase distincte.

## 10. Fichiers documentaires 6A.19

- création : `HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX.md` ;
- mise à jour : `HOTFIX_MERGE_REMAINING_WORK.csv` ;
- mise à jour : `HOTFIX_REPORT_INDEX.csv` ;
- mise à jour : `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- mise à jour : `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- mise à jour : `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` ;
- mise à jour : `docs/reports/hotfix/INDEX.md`.

Le registre global de 534 lignes n’a pas été modifié afin d’éviter un second
registre de classification des 161 lignes.

## 11. Validation

Le registre restant contient 512 lignes, 20 colonnes, 512 chemins uniques et
161 dispositions 6A.19 exactement. La somme des classifications vaut 161.
`HOTFIX_REPORT_INDEX.csv` contient une seule entrée 6A.19 et les identifiants
de bloc restent uniques. L’index Git demeure vide, le stash est intact, aucun
gameplay n’a changé, aucun runtime n’a été lancé et la phase 6A.20 n’a pas été
commencée.

```text
HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX_COMPLETE
POST_6A18Q3_RESIDUAL_DIAGNOSTICS_REINDEXED
RESIDUAL_161_LINE_REGISTRY_RECONCILED
RESIDUAL_87_UNKNOWN_GROUPS_REVIEWED
RESIDUAL_THREE_WAY_CLASSIFICATION_UPDATED
RESIDUAL_CANDIDATE_PRIORITY_MATRIX_COMPLETE
EGYPTIAN_CRISIS_RUNTIME_DEFERRAL_PRESERVED
DECLARED_INTEREST_BLOCK_REMAINS_CLOSED
DEI_VOC_BLOCK_REMAINS_CLOSED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_RESIDUAL_PHASE_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT
```
