# HOTFIX-6A.21 — Sélection résiduelle globale post-Pologne

Date : 5 août 2026
Branche : `hotfix-dlc-audit`
HEAD d'entrée : `da31d6654169d6731a84575ab36ead17c0fde45b`
Mode : documentaire et statique uniquement

## 1. Objet et garde-fous

Cette phase réindexe les diagnostics produits par la QA 6A.20Q, confirme que
le bloc Pologne reste clos et revoit les douze fichiers encore classés
`VANILLA_1_13_ALIGNMENT_REQUIRED`. Elle ne modifie aucun fichier gameplay,
ne lance ni Victoria 3 ni le launcher et ne commence pas la phase sélectionnée.

Les fichiers non suivis protégés et le stash NAVY-3C-3 restent hors périmètre.
Les blocs Russie, DEI/VOC, HBC/NAVY, BIC/Inde/Sepoy, France, Tanzimat,
Amériques, Ibérie custom et Égypte reportée ne sont pas rouverts.

## 2. État d'entrée

- branche : `hotfix-dlc-audit` ;
- commit 6A.20Q : `da31d6654169d6731a84575ab36ead17c0fde45b` ;
- message : `Validate Poland journal entry pinning runtime for 1.13` ;
- index et worktree suivis propres ;
- huit non-suivis protégés connus seulement ;
- stash NAVY-3C-3 :
  `518df704fa14599c0f254fae13859210663dd976` ;
- aucun processus Victoria 3, dowser ou launcher au début de l'analyse.

La succession canonique est donc :

`6A.20F → 6A.20Q → 6A.21 → 6A.22 (sélectionnée, non commencée)`.

## 3. Générations de logs séparées

La génération fraîche 6A.20Q est constituée de `debug.1.log` et `debug.log`.
`debug.2.log` est la rotation immédiatement antérieure ; `debug.3.log` à
`debug.5.log` sont des rotations plus anciennes. Les diagnostics sont
normalisés puis dédupliqués par génération, message, chemin et ligne.

| génération | fichiers | SHA-256 de référence | diagnostics bruts | diagnostics dédupliqués | chemins | messages normalisés |
|---|---|---|---:|---:|---:|---:|
| fraîche 6A.20Q | `debug.1.log` + `debug.log` | `109EBCACE21F5663AD917C7FA59DBDD61BB225BA9C9681AC25DE827A637B6CC1` + `FFEFFAF26F69C1A0E09F6EB4F1C9FD1723FBA9DF793967F26CF26159725BD4D8` | 614 | 614 | 190 | 45 |
| immédiatement antérieure | `debug.2.log` | `B401921CD7FF354A3D0D82E385DD514C5C28585638400908C5E98F6DC1D4DF40` | 616 | 616 | 191 | 45 |
| rotations anciennes | `debug.3.log` à `debug.5.log` | `34269BB6…ED5B9` + `6D9F5BDD…5BBF6` + `FFCBB6F9…9E8C5` | 616 | 616 | 191 | 45 |

La différence exacte de deux diagnostics et d'un chemin correspond à la
disparition de `common/journal_entries/00_poland.txt`. Ce fichier passe de deux
rejets historiques à zéro ; aucune erreur fraîche ne lui est attribuée. Le
bloc des deux pinning Pologne reste donc clos et n'est pas reclassé parmi les
résidus.

## 4. Cohorte `VANILLA_1_13_ALIGNMENT_REQUIRED`

Le registre canonique contient 512 chemins et exactement douze lignes dans
cette cohorte. Les 12 chemins sont uniques. Les nombres de rotations ci-dessous
sont dédupliqués sur les rotations et ne sont jamais additionnés au courant.

| candidat | path | file_count | object_count | current_log_count | rotated_log_count | fork_vs_source | fork_vs_vanilla | source_vs_vanilla | functional_delta | auto_exclusion | protected_collision | audit_scope | exact_report_scope | required_runtime | priority | disposition |
|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|
| Canada/Australie | `common/journal_entries/00_canada_australia.txt` | 1 | 4 | 4 | 4 | différent | différent | différent, clés identiques | 4 anciennes clés de pinning et hunks adjacents | Amériques | oui | quatre objets séparés | pinning seulement, futur rapport distinct | non | P1 | différé |
| Fascisme | `common/journal_entries/00_fascism.txt` | 1 | 3 | 3 | 3 | différent | différent | différent, clés identiques | 3 anciennes clés et logique d'idéologie adjacente | non | non | trois objets séparés | audit atomique futur | non | P1 | admissible mais plus large |
| Unification allemande | `common/journal_entries/00_german_unification.txt` | 1 | 5 | 5 | 5 | différent | différent | différent, clés identiques | 5 anciennes clés et progression d'unification | non | non | cinq objets séparés | audit atomique futur | non | P1 | admissible mais plus large |
| Printemps des peuples | `common/journal_entries/00_peoples_springtime_je.txt` | 1 | 2 | 2 | 2 | différent | différent | différent, clés identiques | 2 anciennes clés et chaînes révolutionnaires | France | oui | deux objets | exclure tout scope France | non | P1 | exclu de la sélection |
| Tutoriel | `common/journal_entries/00_tutorial.txt` | 1 | 52 | 52 | 52 | différent | différent | différent, clés identiques | 52 anciennes clés distribuées | non | non | 52 objets | subdivision préalable obligatoire | non | P0 | trop large pour un audit borné |
| Grande Colombie | `common/journal_entries/02_gran_colombia.txt` | 1 | 3 | 3 | 3 | différent | différent | différent, clés identiques | 3 anciennes clés et formation régionale | Amériques | oui | trois objets | pinning seulement après levée de protection | non | P1 | exclu de la sélection |
| Afghanistan | `common/journal_entries/03_afghanistan.txt` | 1 | 2 | 2 | 2 | différent | différent | différent, mêmes 2 clés 1.13 | 2 anciennes clés ; vastes hunks Great Game adjacents | non | non | exactement 2 propriétés dans 2 objets | `je_consolidate_afghanistan` et `je_unify_afghanistan`, pinning uniquement | non | P0 | sélectionné, non commencé |
| Corée | `common/journal_entries/03_korea.txt` | 1 | 3 | 7 | 7 | différent | différent | différent | 3 pinning et 4 `is_ruler` | Japon/rôles | oui | trois objets et deux API | séparer pinning des rôles | non | P0 | subdivision préalable |
| Question d'Orient | `common/journal_entries/05_eastern_question.txt` | 1 | 2 | 2 | 2 | différent | différent | différent, clés identiques | 2 anciennes clés et logique ottomane | Tanzimat | oui | deux objets | hors bloc Tanzimat | non | P1 | exclu de la sélection |
| Politique portugaise | `common/journal_entries/06_portugal_politics.txt` | 1 | 6 | 6 | 6 | différent | différent | différent, clés identiques | 6 anciennes clés et politique ibérique | Ibérie custom | oui | six objets | audit futur protégé | non | P1 | exclu de la sélection |
| Afrique espagnole | `common/journal_entries/06_spanish_africa.txt` | 1 | 4 | 4 | 4 | différent | différent | différent, clés identiques | 4 anciennes clés et conquêtes coloniales | Ibérie custom | oui | quatre objets | audit futur protégé | non | P1 | exclu de la sélection |
| Pologne-Lituanie custom | `common/journal_entries/07_poland_lithuania_mod.txt` | 1 | 8 | 9 | 9 | différent | vanilla absent | sans objet | 8 pinning plus 2 types de rejet, avec décisions de design | custom Pologne | oui | huit objets et API mixtes | audit de design séparé | non | P0 | exclu de la sélection |

Les trois groupes Canada/Australie, Fascisme et Unification allemande étaient
précédemment décrits sans preuve runtime courante. La génération fraîche 6A.20Q
les reproduit respectivement 4, 3 et 5 fois : seule leur preuve change, pas
leur classification fonctionnelle ni les comptes globaux du registre.

## 5. Preuve trois voies du candidat afghan

| arbre | lignes | SHA-256 | ancien pinning | nouveau pinning |
|---|---:|---|---:|---:|
| fork | 1 877 | `D24333CE06C2DE801F91462000713DCEB430822A2167F7336341E9071B19F988` | 2 | 0 |
| source hotfix | 1 184 | `2C4427D13C0AECEE9E89D872CF8CA9B61B491F843D921166D642DCE8F06E9C2F` | 0 | 2 |
| vanilla 1.13 | 1 526 | `386E57394FA9A57E406B1CC1C234856D46E4901159D689D8AE54126140F81266` | 0 | 2 |

Les deux objets existent dans les trois arbres. Le fork emploie
`should_be_pinned_by_default = yes` aux lignes 2 et 1826. Source et vanilla
emploient toutes deux
`should_be_pinned_by_default_uninvolved_or_context = yes` dans les mêmes
objets. Les deux diagnostics frais confirment l'obsolescence des deux clés.

Cette convergence ne justifie aucun remplacement de fichier. Les différences
adjacentes couvrent notamment régions stratégiques, frontières, Great Game,
boutons scriptés, visibilité, conditions, progression, événements, personnages
et effets. La phase suivante ne pourra qu'auditer les deux propriétés de
pinning, calculer un patch théorique et prouver l'invariance de tout le reste.

## 6. Avertissement de compatibilité `1.12.5`

L'avertissement frais est :

`Mod 1776 - Age of Revolutions, Total Conversion Mod () version 1.12.5 does not match game version 1.13.0.`

La valeur provient de `.metadata/metadata.json`, champ
`supported_game_version`. Elle ne provient ni de `descriptor.mod` ni de
`1776_age_of_revolutions_fork.mod`, qui déclarent tous deux
`supported_version="1.*"`.

Il s'agit d'un avertissement de métadonnées de compatibilité, distinct des
diagnostics de scripts et sans lien avec les deux pinning Pologne. Le jeu a
monté le fork et chargé une partie 1.13 malgré cet avertissement : il ne bloque
donc pas le merge du hotfix. Un audit metadata/descriptor borné reste recommandé
avant publication ou tag de release, mais il n'est ni sélectionné ni commencé
ici et ne doit pas être confondu avec un correctif gameplay.

## 7. Sélection

Une seule phase est sélectionnée :

`HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT`

Périmètre exact : un fichier, deux objets, deux propriétés de pinning, audit
statique seulement. La phase 6A.22 devra rester en lecture seule, produire un
rapport autonome et ne pourra ni appliquer la correction ni lancer un runtime.
Tous les hunks Great Game, frontières, régions, boutons, personnages, rôles,
événements, progression et effets sont explicitement exclus.

La phase 6A.22 est seulement sélectionnée. Elle n'est pas exécutée par 6A.21.

## 8. Verdicts

```text
HOTFIX_6A21_POST_POLAND_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A20Q_FRESH_DIAGNOSTICS_REINDEXED
POLAND_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
RESIDUAL_VANILLA_1_13_ALIGNMENT_COHORT_REVIEWED
RESIDUAL_CURRENT_AND_ROTATION_ONLY_DIAGNOSTICS_SEPARATED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
DESCRIPTOR_1_12_5_WARNING_CLASSIFIED_SEPARATELY
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT
```
