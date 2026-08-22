# TECH-3B1 — Compatibility Alias Visibility Fix

## Statut

`TECH3B1_ALIAS_VISIBILITY_STATIC_PASS_RUNTIME_PENDING`

La validation runtime n'est pas déclarée réussie. Elle reste à effectuer manuellement dans Victoria 3.

## Problème runtime observé

TECH-3B avait correctement neutralisé 38 anciennes technologies consommées avec `can_research = no` et reconnecté toutes les dépendances actives vers leurs propriétaires TECH-3A. Le runtime a néanmoins montré que certains de ces alias restaient affichés comme cartes, notamment :

- `navigation` ;
- `standing_army` / Armée permanente.

Des traits visuels pouvaient également rester dessinés vers des cartes consommées, ce qui produisait des segments orphelins ou des technologies visuellement isolées.

## Cause technique

Le fichier vanilla `gui/tech_tree.gui` a été inspecté directement depuis l'installation Victoria 3 locale, branche moteur `release/1.13.11`.

Le conteneur d'une carte utilise :

```text
Technology.ShouldShow(GetPlayer.Self)
```

`can_research = no` interdit la recherche directe, mais ne force pas `Technology.ShouldShow` à retourner faux. Lorsqu'un pays possède déjà l'ancienne technologie par son historique ou par un script, l'alias peut donc rester affiché comme technologie acquise.

Le conteneur des lignes ne vérifiait pas non plus que la technologie cible devait être affichée. Il choisissait seulement l'apparence de la ligne selon l'état de recherche de la cible. Une carte cachée sans filtre équivalent sur les lignes aurait donc laissé des segments visibles.

## Fichiers inspectés

- `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
- `docs/reports/technology/TECH3B_ERA_VI_VII_SEAM_AUDIT.csv`
- `docs/reports/technology/TECH3B_VANILLA_BRIDGE_MATRIX.csv`
- `docs/reports/technology/TECH3B_VANILLA_SEAM_RECONNECTION_REPORT.md`
- Victoria 3 installé : `game/gui/tech_tree.gui`
- Victoria 3 installé : `game/common/technology/technologies/10_production.txt`
- logs runtime locaux : `logs/gui.log`, `logs/error.log`, `logs/debug.log`

## Correction implémentée

Un override minimal de `gui/tech_tree.gui` a été ajouté au mod. Il est copié depuis le fichier installé `release/1.13.11`; la comparaison avec ce fichier vanilla ne contient que deux changements fonctionnels :

1. le conteneur de carte conserve `Technology.ShouldShow`, puis exclut explicitement les 38 IDs consommés ;
2. le conteneur de ligne exclut toute ligne dont la technologie cible est l'un de ces 38 IDs.

Les comparaisons utilisent les objets techniques `GetTechnology('<tech_id>')`, jamais les noms localisés. Elles fonctionnent donc de la même façon en français et en anglais.

Tous les alias conservent :

- leur définition et leur ID technique ;
- `can_research = no` ;
- leurs références depuis les événements, historiques, IA et journal entries ;
- leur payload existant, sans modification d'effet ou d'unlock gameplay.

Le fichier de compatibilité technologique n'a pas été modifié davantage pendant TECH-3B1. La topologie validée par TECH-3B reste identique.

## Alias traités

- Alias consommés audités : 38
- Échecs runtime explicitement rapportés : 2 (`navigation`, `standing_army`)
- Alias présents exactement une fois dans le filtre des cartes : 38/38
- Alias présents exactement une fois dans le filtre des lignes : 38/38
- Alias manquants dans un filtre : 0

Le détail individuel est disponible dans `TECH3B1_ALIAS_VISIBILITY_AUDIT.csv`.

Les cas obligatoires sont tous couverts par les deux filtres :

- `navigation` ;
- `standing_army` ;
- `rationalism` ;
- `urbanization` ;
- `urban_planning` ;
- `modern_sewerage`.

## Traitement des lignes et segments orphelins

TECH-3B garantit déjà qu'aucune technologie active n'utilise un alias consommé comme prérequis. TECH-3B1 masque en plus chaque ligne dont la cible est un alias consommé. Cette combinaison couvre les deux causes possibles de segments fantômes :

- aucune nouvelle ligne active ne mène vers un alias ;
- les anciennes lignes internes aux alias de compatibilité ne sont plus rendues.

Les bridges Era VI → post-1836 validés par TECH-3B ne sont pas filtrés, car leurs cibles sont des technologies conservées et non les alias consommés.

## Fichiers modifiés par TECH-3B1

- `gui/tech_tree.gui`
- `docs/reports/technology/TECH3B1_ALIAS_VISIBILITY_AUDIT.csv`
- `docs/reports/technology/TECH3B1_RUNTIME_VISIBILITY_FIX_REPORT.md`

Le diff global du working tree contient toujours les changements TECH-3B non commités dans `90_tech3a_vanilla_post1836_compatibility.txt` et ses trois rapports. Ils ont été préservés.

## Validation statique finale

| Validation | Résultat |
|---|---:|
| `VISIBLE_CONSUMED_ALIASES_RUNTIME_TARGET` | 0 ciblé statiquement ; runtime pending |
| `VISIBLE_KNOWN_FAILURES_TARGET` | 0 ciblé statiquement ; runtime pending |
| `DANGLING_VISIBLE_EDGE_STUBS` | 0 ciblé statiquement ; runtime pending |
| `ERA_VII_UNINTENDED_ROOTS` | 0 |
| `CONSUMED_TECHS_USED_AS_ACTIVE_PREREQUISITES` | 0 |
| `BROKEN_PREREQUISITE_REFERENCES` | 0 |
| `PREREQUISITE_CYCLES` | 0 |
| `LATER_ERA_PREREQUISITE_INVERSIONS` | 0 |
| `DUPLICATE_TECH_IDS` | 0 |
| `LOCALIZATION_CHANGES` | 0 |
| `UNLOCK_CHANGES` | 0 |
| `TECH3A_ERA_I_VI_GAMEPLAY_CHANGES` | 0 |

Contrôles supplémentaires :

- 276 définitions technologiques parsées ;
- 38/38 alias toujours non recherchables ;
- 38 lignes dans l'audit TECH3B1 ;
- parenthèses et crochets équilibrés dans les deux expressions GUI ;
- structure d'accolades du fichier GUI équilibrée ;
- comparaison du GUI modifié avec le GUI installé : deux expressions de visibilité seulement, plus leurs commentaires ;
- aucune modification des localisations anglaises ou françaises ;
- aucune modification des fichiers technologiques Era I-VI.

## Risques restants

- Le résultat visuel doit être confirmé en jeu ; la présente validation ne peut pas exécuter `Technology.ShouldShow` dans le moteur.
- `gui/tech_tree.gui` est un override complet du fichier vanilla et peut entrer en conflit avec un autre mod qui remplace le même fichier.
- L'override est aligné sur Victoria 3 `release/1.13.11`. Après une mise à jour du jeu modifiant le tech tree GUI, il faudra resynchroniser le fichier puis réappliquer les deux filtres TECH3B1.
- Les alias restent techniquement acquis par certains pays, ce qui est intentionnel pour la compatibilité scriptée ; seul leur rendu dans l'arbre est supprimé.

## Checklist runtime utilisateur

- Vérifier la disparition de `navigation`.
- Vérifier la disparition de `standing_army` / Armée permanente.
- Vérifier la disparition de `rationalism`.
- Vérifier la disparition de `urbanization`, `urban_planning` et `modern_sewerage`.
- Parcourir les trois branches et confirmer qu'aucun des 38 alias consommés n'apparaît comme carte.
- Vérifier l'absence de carte fantôme ou d'emplacement interactif invisible.
- Vérifier l'absence de trait ou de segment menant à une carte absente.
- Vérifier la continuité visuelle Era VI → VII.
- Vérifier la progression normale VII → VIII → IX.
- Charger plusieurs pays possédant historiquement différents anciens IDs.
- Vérifier l'absence d'erreur scriptée liée aux alias conservés.

Ne pas promouvoir le statut en runtime pass avant la fin de ces vérifications.
