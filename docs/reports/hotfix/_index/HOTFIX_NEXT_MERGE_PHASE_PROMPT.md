# Phase HOTFIX-6A.9R — Audit de la chaîne ottomane Tanzimat en 1776

## Nature

Audit strictement documentaire. Aucun gameplay ne doit être modifié et aucun
runtime n’est requis.

Codex ne lance jamais Victoria 3 ou le launcher, ne pilote jamais l’interface,
n’utilise jamais la console et ne crée aucun commit automatique.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée

- `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_STATIC_PASS`
- `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_RUNTIME_PASS`
- `GREAT_EASTERN_CRISIS_SIX_HUNK_1_13_ALIGNMENT_COMPLETE`
- `GREAT_EASTERN_CRISIS_GEOGRAPHY_VISIBILITY_AND_PINNING_VALIDATED`
- `OTTOMAN_TANZIMAT_1776_ROUTE_REQUIRES_DOCUMENTARY_AUDIT`
- `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md`

6A.8F doit avoir été commitée manuellement avant de commencer.

## Préflight obligatoire

Exiger :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport et verdicts 6A.8F présents dans le HEAD ;
- worktree suivi et index staged propres ;
- seuls `bject` et les sept fichiers technologiques non suivis ;
- stash exact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, dowser ou Paradox ;
- huit hashes protégés identiques à 6A.8F.

En cas d’écart, arrêter avec un verdict précis. Ne jamais utiliser reset,
restore, checkout, clean, merge, rebase, amend ou une opération de stash.

## Objet de l’audit

Le runtime 6A.8F a prouvé :

- visibilité impliquée ottomane conforme ;
- visibilité contextuelle britannique conforme ;
- aucun pinning automatique chez l’observateur ;
- aucune clé brute ;
- diagnostic ciblé de un à zéro ;
- progression du 1er janvier au 8 avril 1776.

Il a aussi révélé que l’Empire ottoman ne commence pas avec
`L’homme malade de l’Europe` ou les entrées Tanzimat.

L’audit doit déterminer si cette absence est :

1. une divergence 1776 intentionnelle à préserver ;
2. une omission fonctionnelle à corriger ;
3. un contenu vanilla 1836 à adapter plutôt qu’à restaurer ;
4. une décision de design distincte des huit migrations API de
   `00_sick_man.txt`.

## Fichiers obligatoires en lecture seule

Comparer intégralement dans fork, source et vanilla :

1. `common/history/countries/tur - ottoman empire.txt`
2. `common/journal_entries/00_sick_man.txt`
3. `common/journal_entries/05_great_eastern_crisis.txt`

Lire également :

4. `events/sick_man_events.txt`
5. `events/tanzimat_events.txt`
6. les on-actions, lois et stratégies IA référençant `je_sick_man_*`
7. les localisations françaises et anglaises correspondantes
8. les rapports de sélection 6A.4 à 6A.8F
9. les inventaires trois voies et les changelogs
10. les logs 6A.8F, uniquement comme preuve historique en lecture seule.

Le fork hérite des deux fichiers d’événements vanilla ; ne pas les copier.

## Hashes de référence

### Histoire ottomane

| Arbre | SHA-256 |
| --- | --- |
| Fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` |
| Source hotfix | `15FC3CA4F1185B714B821EEE7B3DF400325AFEFA19C26BD92091B375D8C72375` |
| Vanilla | `93D02B1F8732205F8DCE570639B220CF32DF58A43741FC68D6604B4DED8EBF09` |

### Entrées Sick Man/Tanzimat

| Arbre | SHA-256 |
| --- | --- |
| Fork | `DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8` |
| Source hotfix | `E48405BFABB52F6CE757880E436C8D44C67111E246AF3215FD3F96EC4F3477F9` |
| Vanilla | `1EAD43BE40DAF22D585712442AFD379C893C3075007CDA0AADDB126CCF1DCA41` |

### Grande Crise orientale après 6A.8F

Fork :

`96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A`

### Événements hérités

- `events/sick_man_events.txt` :
  `D110D1FD83CD98E131D4C2769B606CC908F17844EFF88EF65F51FEBF313A0C2B`
- `events/tanzimat_events.txt` :
  `F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30`

Arrêter avec `BLOCKED_THREE_WAY_EVIDENCE_CHANGED` si les hashes diffèrent.

## Baseline factuelle

Dans le fork :

```txt
#		trigger_event = {
#			id = sick_man.1
#		}
#		add_modifier = {
#			name = sick_man_of_europe
#			months = -1
#		}
#		add_modifier = {
#			name = outmoded_bureaucracy
#			months = -1
#		}
```

La source hotfix conserve la même omission commentée. Vanilla active ces
éléments dans son setup.

L’événement hérité `sick_man.1` :

- initialise les variables ;
- ajoute `je_sick_man_main` ;
- ajoute ensuite les six entrées Tanzimat secondaires.

La Grande Crise orientale conserve deux voies indépendantes :

1. `nationalism` recherché et sécession ottomane à au moins 50 % ;
2. échec de `je_sick_man_main` ou `je_sick_man_separatism`.

L’absence de Tanzimat supprime la seconde voie mais pas la première.

`00_sick_man.txt` contient huit occurrences fork de :

`should_be_pinned_by_default = yes`

Source et vanilla emploient huit occurrences de :

`should_be_pinned_by_default_uninvolved_or_context = yes`

## Analyses obligatoires

### A. Intention du setup 1776

Déterminer :

- pourquoi fork et source commentent ensemble la chaîne vanilla ;
- si les commentaires et changelogs prouvent une intention 1776 ;
- si une entrée conçue pour le départ vanilla doit apparaître en 1776 ;
- si son timeout de 30 ans et ses objectifs sont cohérents avec le setup ;
- si les lois, technologies, territoires et adversaires de 1776 permettent
  réellement ses sous-objectifs ;
- si les textes ou modificateurs seraient anachroniques ou trompeurs ;
- si une activation différée serait préférable à une activation au départ.

### B. Accessibilité de la Grande Crise orientale

Prouver séparément :

- que la voie nationalisme plus sécession reste atteignable ;
- que la voie échec Tanzimat est inaccessible sans ajout de la chaîne ;
- si la première voie suffit au design 1776 ;
- si l’absence de la seconde constitue un défaut, une simplification ou une
  divergence intentionnelle ;
- si les pays impliqués et les variables peuvent être initialisés sans
  `sick_man.1`.

Ne pas déclarer la crise « impossible » tant que la première branche existe.

### C. Huit migrations de pinning

Pour chacun des huit objets `je_sick_man_*`, publier :

- lignes fork/source/vanilla ;
- visibilité et propriétaire attendu ;
- ancienne et nouvelle propriété ;
- convergence source/vanilla ;
- dépendance à l’activation de la chaîne ;
- classification exclusive ;
- risque et rollback.

Décisions autorisées :

- `REQUIRED_1_13_ALIGNMENT`
- `REQUIRED_HOTFIX_DELTA`
- `INTENTIONAL_1776_DIVERGENCE`
- `DEFER_REQUIRES_DESIGN_DECISION`
- `ALREADY_EQUIVALENT`

Déterminer si ces huit migrations API peuvent être corrigées indépendamment de
la décision de démarrer Tanzimat en 1776.

### D. Dépendances

Cartographier :

- `sick_man.1` ;
- `je_sick_man_main` et les six sous-entrées ;
- variables `sick_man_var`, `sick_man_separatist_var`,
  `failed_sick_man_main`, `failed_sick_man_separatism` ;
- modificateurs `sick_man_of_europe` et `outmoded_bureaucracy` ;
- événements Tanzimat ;
- lois et stratégies IA ;
- Grande Crise orientale et Grand Effondrement ;
- DLC requis ;
- localisations.

## Décision finale obligatoire

Choisir exactement une structure :

### Option A

Préserver l’absence de Tanzimat au départ 1776 et sélectionner séparément une
correction API des huit pinning.

### Option B

Préserver l’absence au départ mais concevoir une future activation différée
propre à 1776 ; séparer strictement cette phase de design de la correction API.

### Option C

Restaurer la chaîne vanilla au départ seulement si toutes les preuves gameplay,
historiques et textuelles montrent qu’elle est cohérente avec 1776.

### Option D

Bloquer sur une décision humaine de design avec les choix et conséquences
exactement documentés.

Ne commencer aucune correction pendant 6A.9R.

## Périmètre d’écriture fermé

Uniquement :

1. `docs/reports/hotfix/_index/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md`
2. `docs/reports/hotfix/INDEX.md`
3. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
4. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
6. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Tout gameplay est strictement en lecture seule.

## Rapport requis

Le rapport doit contenir :

- préflight et hashes ;
- comparaison trois voies ;
- cause exacte de l’absence Tanzimat ;
- preuve des deux voies de la Grande Crise ;
- analyse 1776 ;
- tableau des huit objets ;
- dépendances et localisations ;
- classifications exclusives ;
- options comparées ;
- décision atomique ;
- éventuelle future correction sélectionnée ;
- protections et rollback futur ;
- état Git final ;
- verdicts.

## Contrôles finaux

Confirmer :

- zéro gameplay modifié ;
- exactement six documents de phase ;
- sources et vanilla inchangées ;
- 6A.8F non rouverte ;
- huit hashes protégés et stash intacts ;
- aucun fichier staged ;
- CSV valides ;
- `git diff --check` propre ;
- jeu et launcher non lancés ;
- aucun commit automatique ;
- future phase préparée mais non commencée.
