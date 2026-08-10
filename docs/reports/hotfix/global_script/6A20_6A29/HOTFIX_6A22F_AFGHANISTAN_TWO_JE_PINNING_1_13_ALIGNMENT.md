# HOTFIX-6A.22F — Alignement 1.13 des deux pinning Afghanistan

Date : 5 août 2026
Branche : `hotfix-dlc-audit`
HEAD d'entrée : `bcb079bbea93aa39458074472c556cbd8b7156c5`
Commit d'audit 6A.22 : `bcb079bbea93aa39458074472c556cbd8b7156c5`
Mode : correction byte-level statique, aucun runtime

## 1. Préflight

Le HEAD porte le message exact
`Audit Afghanistan journal entry pinning for 1.13` et contient le rapport
6A.22 avec la preuve d'atomicité et la sélection de 6A.22F. La branche est
`hotfix-dlc-audit`, l'arbre suivi et l'index sont propres à l'entrée, les huit
non-suivis protégés connus sont seuls présents, aucun processus Victoria 3,
Dowser ou launcher Paradox n'est actif et le stash NAVY-3C-3 vaut
`518df704fa14599c0f254fae13859210663dd976`.

## 2. Identité d'entrée

Le seul fichier gameplay autorisé est
`common/journal_entries/03_afghanistan.txt`.

| propriété | valeur d'entrée |
|---|---|
| encodage | UTF-8 |
| BOM | UTF-8 présent |
| fins de ligne | LF uniquement |
| octets | 36 769 |
| lignes LF | 1 877 |
| anciennes propriétés | 2 |
| nouvelles propriétés | 0 |
| SHA-256 | `D24333CE06C2DE801F91462000713DCEB430822A2167F7336341E9071B19F988` |
| blob Git HEAD/worktree | `d93ccfce1cea248e24c4919ed1e11fdecfd8e775` / identique |

Les deux anciennes propriétés utilisent une tabulation, sont à profondeur
racine et précèdent immédiatement `icon` :

- `je_consolidate_afghanistan`, ligne historique 2 ;
- `je_unify_afghanistan`, ligne historique 1826.

## 3. Méthode et diff exact

La correction remplace au niveau byte exactement deux séquences ASCII, sans
sérialisation, reformatage, normalisation de lignes ni fichier temporaire :

```diff
 je_consolidate_afghanistan = {
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
 	icon = "gfx/interface/icons/event_icons/event_map.dds"

 je_unify_afghanistan = {
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
 	icon = "gfx/interface/icons/event_icons/waving_flag.dds"
```

Le diff gameplay est exactement un fichier, deux objets, deux hunks, deux
lignes ajoutées et deux lignes supprimées. Aucun autre fichier gameplay ne
change.

## 4. Identité finale et inversion

| propriété | entrée | résultat statique |
|---|---:|---:|
| octets | 36 769 | 36 813 |
| lignes LF | 1 877 | 1 877 |
| CRLF / CR isolé | 0 / 0 | 0 / 0 |
| anciennes propriétés | 2 | 0 |
| nouvelles propriétés | 0 | 2 |
| BOM UTF-8 | présent | présent |
| SHA-256 | `D24333CE06C2DE801F91462000713DCEB430822A2167F7336341E9071B19F988` | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` |

Le remplacement inverse des deux nouvelles séquences produit 36 769 octets
et restitue exactement le SHA-256 d'entrée. Comme le diff Git ne contient que
les deux lignes ciblées et que l'inversion reconstitue le contenu d'entrée,
tous les autres octets sont inchangés.

## 5. Inspection fonctionnelle de `je_consolidate_afghanistan`

L'objet conserve ses bornes lignes 1–1823 et une seule nouvelle propriété de
pinning. La relecture intégrale confirme l'invariance de :

- l'icône `event_map.dds` et `je_group_foreign_affairs` ;
- la visibilité lobby GBR/DLC et la visibilité inactive propre au fork ;
- les douze boutons `je_consolidate_afghanistan_*` ;
- l'invalidation et l'impulsion hebdomadaire ;
- l'événement `gg_afghanistan.1` ;
- les effets immédiats et toutes les conditions `possible` ;
- la condition et les effets de complétion ;
- le délai `365`, tous les effets d'expiration et le poids `1001`.

## 6. Inspection fonctionnelle de `je_unify_afghanistan`

L'objet conserve ses bornes lignes 1825–1877 et une seule nouvelle propriété
de pinning. La relecture intégrale confirme l'invariance de :

- l'icône `waving_flag.dds` et `je_group_foreign_affairs` ;
- la visibilité lobby et les conditions `possible` fondées sur
  `sr:region_persia`, `cu:pashtun` et `cu:tajik` ;
- les deux appels scriptés à la Russie et à la Grande-Bretagne ;
- la condition de formation d'AFG ;
- le tooltip et l'événement `gg_afghanistan.4` ;
- la description du résultat et le poids `1000`.

Régions stratégiques ou géographiques, frontières, états, Great Game, boutons,
visibilité, conditions, progression, tooltips, pays, sujets, cultures,
religions, personnages, rôles, technologies, événements, effets, récompenses,
modificateurs, scopes et variables restent tous hors du diff.

## 7. Baseline des logs et runtime ultérieur

Les logs existants restent une baseline historique non modifiée :

```text
Unexpected token: should_be_pinned_by_default
common/journal_entries/03_afghanistan.txt
lignes historiques 2 et 1826
2 diagnostics dédupliqués
```

Aucun passage `2 → 0` n'est revendiqué en 6A.22F. La phase humaine distincte
`HOTFIX_6A22Q_AFGHANISTAN_TWO_JE_PINNING_1_13_RUNTIME_QA` devra effectuer une
seule ouverture, produire une génération fraîche sans forcer les entrées,
fermer jeu et launcher avant analyse, vérifier `2 → 0`, zéro nouvelle erreur
liée au fichier et les hashes gameplay. L'UI ne sera validée que si les
entrées sont naturellement visibles.

## 8. Fichiers de la phase

Gameplay :

- `common/journal_entries/03_afghanistan.txt`.

Documentation autorisée :

- `docs/reports/hotfix/global_script/6A20_6A29/HOTFIX_6A22F_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_REMAINING_WORK.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

`git diff --check` passe, l'index Git reste vide, le HEAD reste
`bcb079bbea93aa39458074472c556cbd8b7156c5`, aucun commit automatique n'est
créé et le stash NAVY-3C-3 reste intact.

## 9. Verdicts

```text
HOTFIX_6A22F_AFGHANISTAN_TWO_JE_PINNING_1_13_STATIC_PASS
AFGHANISTAN_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_APPLIED
AFGHANISTAN_TWO_JE_PINNING_OLD_PROPERTIES_2_TO_0
AFGHANISTAN_TWO_JE_PINNING_NEW_PROPERTIES_0_TO_2
AFGHANISTAN_TWO_JE_PINNING_GAMEPLAY_DIFF_2_PLUS_2_MINUS
AFGHANISTAN_TWO_JE_PINNING_SHA256_MATCH
AFGHANISTAN_TWO_JE_PINNING_OTHER_BYTES_UNCHANGED
AFGHANISTAN_GREAT_GAME_GEOGRAPHY_BUTTONS_SCOPES_EVENTS_AND_EFFECTS_UNCHANGED
NO_RUNTIME_EXECUTED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A22Q_AFGHANISTAN_TWO_JE_PINNING_1_13_RUNTIME_QA
```
