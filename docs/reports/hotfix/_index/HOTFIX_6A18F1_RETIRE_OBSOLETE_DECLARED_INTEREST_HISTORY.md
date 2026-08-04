# HOTFIX-6A.18F1 — Retrait de l'historique obsolète des intérêts déclarés

## 1. Phase, date et résultat

- phase : `HOTFIX_6A18F1_RETIRE_OBSOLETE_DECLARED_INTEREST_HISTORY`;
- date : 4 août 2026;
- branche : `hotfix-dlc-audit`;
- HEAD initial et final :
  `290e34fff9abe23c586b602e4ff117752345b646`;
- message du HEAD :
  `Audit declared interest initialization mechanism for 1.13`;
- gameplay : suppression manuelle d'un seul fichier obsolète;
- runtime : une seule session humaine, sans lancement ni pilotage par Codex;
- commit automatique : aucun.

La suppression de `common/history/interests/00_interests.txt` passe les
contrôles statiques et le runtime de non-régression. Les 91 diagnostics issus
de ce fichier disparaissent, les six implications autrichiennes naturelles
restent identiques et aucune implication n'apparaît au Sud de la Chine ou au
Canada. Aucune erreur de fichier ou de dossier manquant n'est produite.

## 2. Décision humaine canonique

L'opérateur a arrêté la décision de design suivante :

```text
RETIRE_OBSOLETE_FIXED_DECLARED_INTEREST_HISTORY
DELETE_ACTIVE_00_INTERESTS_FILE
PRESERVE_FILE_ONLY_IN_GIT_HISTORY
DO_NOT_RECREATE_91_FIXED_INTERESTS
```

Cette décision n'est pas réinterprétée dans F1. Victoria 3 1.13 calcule les
implications durables depuis des sources naturelles. `add_involvement` ne
fournit qu'une impulsion sur la valeur courante; recréer les 91 entrées par des
territoires, revendications, forces, traités, pactes ou sujets modifierait le
gameplay et l'équilibrage.

## 3. Préflight et état Git initial

Le préflight obligatoire a confirmé :

| Contrôle | Résultat |
| --- | --- |
| racine | fork exact |
| branche | `hotfix-dlc-audit` |
| HEAD | `290e34fff9abe23c586b602e4ff117752345b646` |
| message | exact |
| rapport 6A.18R2 dans le HEAD | présent, dix verdicts présents |
| delta suivi | uniquement `D common/history/interests/00_interests.txt` |
| suppression | non stagée |
| index staged | vide |
| non suivis | seulement `bject` et sept recherches technologiques protégées |
| `git diff --check` | PASS |
| processus Victoria 3 / Dowser / launcher Paradox | aucun |

Le stash protégé est resté exact :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 4. Preuve du blob historique

Le contenu a été relu directement depuis le blob Git du HEAD, sans restauration
dans le worktree :

```text
path = common/history/interests/00_interests.txt
blob Git = 727c5efa349b04717d43351599aa94eed3b84037
size = 4415 octets
SHA-256 = A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD
actions actives = 91
pays = 28
noms de régions distincts = 45
```

Le fichier et le dossier `common/history/interests/` sont absents du
worktree. Le diff est une suppression complète sans renommage :

```text
delete mode 100644 common/history/interests/00_interests.txt
numstat = 0 insertion, 158 suppressions
```

Le blob existe dans le parent du HEAD et dans l'historique du chemin. Un
rollback byte-identique reste donc théoriquement possible par Git, mais aucun
rollback ni aucune restauration n'a été exécuté.

## 5. Validation statique

Les contrôles ont établi :

- le vanilla 1.13 ne possède pas de dossier `common/history/interests`;
- le fork actif ne contient aucune autre copie de `00_interests.txt`;
- aucune autre racine active `INTERESTS` n'est destinée à ce chargeur;
- aucune référence hors documentation n'exige physiquement le fichier;
- `descriptor.mod` ne déclare ni le fichier ni son dossier;
- la suppression est le seul delta gameplay suivi et n'est pas un renommage;
- les références CSV existantes sont des inventaires historiques, pas des
  listes de chargement.

Il reste exactement deux effets legacy, exclus de F1 :

| Fichier | Ligne | Effet | SHA-256 |
| --- | ---: | --- | --- |
| `events/egyptian_crisis_events.txt` | 187 | `add_declared_interest = region_arabic` | `EE2A0881C43A14118E0347001FAA423FABA40080C106883BAD0CC6E5715A3168` |
| `events/indochina.txt` | 346 | `add_declared_interest = region_indochina` | `177A6446668E9274260FCA90B0F7B0802280CA7E086CC1290E15C862E845B2BB` |

Les deux fichiers sont restés byte-identiques. La crise égyptienne dispose
d'un hunk vanilla 1.13 directement comparable; l'Indochine demeure une
décision séparée.

```text
DECLARED_INTEREST_HISTORY_FILE_DELETION_STATIC_PASS
OBSOLETE_HISTORY_FILE_REMOVED_FROM_ACTIVE_MOD
TWO_EVENT_LEGACY_OCCURRENCES_REMAIN_SEPARATE
```

## 6. Préparation du runtime humain unique

Avant le lancement, le jeu et le launcher étaient fermés, la suppression était
isolée et les tailles, dates et hashes des journaux avaient été capturés.
Codex n'a ni lancé ni piloté Victoria 3 ou le launcher.

L'opérateur a confirmé :

1. seul le fork était activé;
2. l'Autriche a été sélectionnée au 1er janvier 1776;
3. la partie est restée en pause;
4. aucun intérêt, traité, pacte, déploiement, loi ou pays n'a été modifié;
5. Victoria 3 et le launcher ont été fermés après l'observation.

Un seul runtime a été demandé et exécuté.

## 7. Observations UI

Les six implications naturelles autrichiennes sont inchangées :

| Région stratégique | Implication |
| --- | ---: |
| Balkans | 6324 |
| Europe centrale | 4176 |
| Europe de l'Est | 3969 |
| Europe du Sud | 3320 |
| Europe de l'Ouest | 2300 |
| Europe du Nord | 1500 |

Les panneaux du Sud de la Chine et du Canada affichent tous deux
`Aucune implication Autrichienne`. Le retrait des 91 effets inopérants ne
change donc pas l'état réel observé avant la suppression.

## 8. Journaux avant et après

Les trois journaux courants ont changé de hash et de date; la nouvelle session
est ainsi isolée de la baseline 6A.18Q.

| Journal | Session | Octets | Lignes lues | Dernière écriture UTC | SHA-256 |
| --- | --- | ---: | ---: | --- | --- |
| `debug.log` | avant | 337201 | 2484 | `2026-08-04T11:35:11.1251862Z` | `9DE3CD6BE2E2A6CEBB3E647A9A97893059C4D4E920D5B02EB39DB12DD8881D3A` |
| `error.log` | avant | 124945 | 2367 | `2026-08-04T11:35:00.3799882Z` | `A43B489AAAA0610532DC167B76E0FAABE295BFEABDD5865E8F0EF39D0EE47938` |
| `game.log` | avant | 427780 | 8967 | `2026-08-04T11:35:00.3799882Z` | `6D9F2D88FA999EAA819579830CFF513A8F8ACFE136C49ED6424D17C251B83A8D` |
| `debug.log` | après | 432311 | 3585 | `2026-08-04T13:05:07.1597980Z` | `845F94DF093F51727829CF648ABA1ECB1746A2D32383491E35F5A68F39E40830` |
| `error.log` | après | 131040 | 2551 | `2026-08-04T13:04:51.2557049Z` | `048CA0B89ED62DFE32FCF2C8F876993CC56289654CAE0F0DA845FBD824AEBC5B` |
| `game.log` | après | 114575 | 2195 | `2026-08-04T13:04:51.2557049Z` | `C9A35DCEBBCEBD212BB9E04A68B71FDE33A4A31A6EF671AC6A75A4D43BD1CAE1` |

## 9. Diagnostics de la nouvelle session

Les trois journaux ont été lus intégralement. La déduplication ciblée utilise
le tuple `(session, timestamp, message, chemin, ligne)`.

| Cible | Avant | Après | Résultat |
| --- | ---: | ---: | --- |
| diagnostics `00_interests.txt` | 91 | 0 | PASS |
| mentions actives `00_interests.txt` | 91 | 0 | PASS |
| mentions `common/history/interests` | 91 | 0 | PASS |
| erreur de fichier/dossier manquant | 0 | 0 | PASS |
| `INTERESTS` dans les nouveaux logs | n/a | 0 | PASS |

Les deux diagnostics legacy restants sont distincts :

| Session | Heure | Message | Chemin | Ligne |
| --- | --- | --- | --- | ---: |
| F1 | `14:58:18` | `Unknown effect add_declared_interest` | `events/egyptian_crisis_events.txt` | 187 |
| F1 | `14:58:18` | `Unknown effect add_declared_interest` | `events/indochina.txt` | 346 |

`debug.log` contient sept diagnostics `Unknown effect` au total : les deux
lignes ci-dessus et cinq effets étrangers au système d'intérêts. `error.log`
et `game.log` ne contiennent aucun diagnostic ciblé. Les recherches exactes
`File not found` et `Could not open` retournent zéro résultat dans les trois
journaux.

`debug.log` contient aussi 23 échecs de PostValidate du trigger actuel
`has_interest_marker_in_region`, déjà présents dans la baseline et étrangers à
la suppression. Les uniques mentions de `region_south_china` et
`region_canada` proviennent de diagnostics parser dans
`common/ai_strategies/00_default_strategy.txt`; elles ne mentionnent ni le
fichier retiré ni son chargeur. Aucun diagnostic nouveau n'est attribuable à
la suppression.

## 10. Résultat runtime et phase suivante

Les onze critères de validation passent : le fork monte, la partie charge, les
implications naturelles ne régressent pas, les deux contrôles hors région
restent négatifs, les 91 diagnostics tombent à zéro, aucun message de fichier
ou dossier manquant n'apparaît, les événements exclus et le stash restent
inchangés.

La seule phase suivante sélectionnée est :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A18F2_EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_ALIGNMENT
```

F2 devra remplacer uniquement l'occurrence de la crise égyptienne par le hunk
vanilla 1.13. Aucune correction Indochine n'est sélectionnée et F2 n'est pas
commencée dans ce rapport.

## 11. Documents modifiés

- création du présent rapport;
- mise à jour de `docs/reports/hotfix/INDEX.md`;
- mise à jour de `HOTFIX_REPORT_INDEX.csv`;
- mise à jour de `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- mise à jour de `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- sélection de F2 dans `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun autre document et aucun autre fichier gameplay n'est créé ou modifié.

## 12. État Git final

Les contrôles finaux ont confirmé :

- branche et HEAD initiaux inchangés;
- suppression gameplay unique non stagée;
- seulement les cinq mises à jour documentaires autorisées et le nouveau
  rapport;
- index staged vide;
- `git diff --check` PASS;
- huit éléments non suivis protégés plus le nouveau rapport autorisé;
- stash exact;
- événements exclus aux hashes consignés;
- Victoria 3 et launcher Paradox fermés;
- aucun commit, push, stash ou rollback automatique.

```text
branch = hotfix-dlc-audit
HEAD = 290e34fff9abe23c586b602e4ff117752345b646
tracked gameplay delta = D common/history/interests/00_interests.txt
tracked documentation deltas = 5
new authorized report = 1
staged files = 0
git diff --check = PASS
game processes = 0
```

## 13. Verdicts finaux

```text
HOTFIX_6A18F1_RETIRE_OBSOLETE_DECLARED_INTEREST_HISTORY_COMPLETE
DECLARED_INTEREST_HISTORY_FILE_DELETION_STATIC_PASS
OBSOLETE_HISTORY_FILE_REMOVED_FROM_ACTIVE_MOD
DECLARED_INTEREST_OBSOLETE_HISTORY_RETIREMENT_RUNTIME_PASS
DECLARED_INTEREST_FILE_DIAGNOSTICS_91_TO_0
DECLARED_INTEREST_NATURAL_INVOLVEMENT_NON_REGRESSION_PASS
TWO_EVENT_LEGACY_OCCURRENCES_REMAIN_SEPARATE
NO_ADDITIONAL_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A18F2_EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_ALIGNMENT
```
